#!/usr/bin/env python3
"""场景 4b 逐调用健康检查的故障矩阵 (不调用任何 API)。

用假 claude (fake-claude) 注入各类故障, 经 claude 垫片 (claude-shim.sh) 跑原样的 skill-creator
run_eval.py, 再用 classify_calls.py 判定; 把 run_eval 的门判定、stderr 的 Warning 行数、检查脚本
的结论 (pass / fail / valid / void) 与预期逐条对照。本文件、claude-shim.sh、classify_calls.py、
fake-claude 放在同一目录。

用法: python3 fault_matrix.py [--suite 20 条套件 json] [--out 输出目录]
  SKILL_CREATOR_ROOT 环境变量指向 skill-creator 目录 (含 scripts/run_eval.py), 缺省为 DEFAULT_SKILL_CREATOR。
退出码: 0 = 全部用例符合预期; 1 = 有不符; 2 = 环境不全 (找不到套件或 run_eval.py)。
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SKILL_CREATOR = "/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator"
BASELINE_SUITE_REL = "ab-results/2026-09-13-rule6-description-trigger-eval-baseline/trigger-eval-openspec-archive.json"
NEUTRAL_SKILL = "---\nname: helper\ndescription: |\n  占位 (描述由 --description 显式传入)\n---\n# helper\n"
ERR = {"FAKE_KIND": "result_error"}


def find_suite():
    for d in [HERE, *HERE.parents]:
        if d.name == "aria-plugin-benchmarks":
            cand = d / BASELINE_SUITE_REL
            return cand if cand.is_file() else None
    return None


def path_without_claude():
    keep = [p for p in os.environ.get("PATH", "").split(":") if p and not os.access(os.path.join(p, "claude"), os.X_OK)]
    return ":".join(keep)


def classify(log_dir, eval_output, timeout, role, report):
    c = subprocess.run([sys.executable, str(HERE / "classify_calls.py"), "--log-dir", str(log_dir), "--eval-output",
                        str(eval_output), "--timeout", str(timeout), "--role", role, "--report", str(report)],
                       capture_output=True, text=True)
    try:
        return c.returncode, json.loads(c.stdout)
    except ValueError:
        return c.returncode, {"raw": c.stdout, "stderr": c.stderr}


def run_case(ctx, tag, suite_file, fake_env, timeout, shim_on_path, real_claude, role):
    out = ctx["out"]
    root, logs = out / "roots" / tag, out / "logs" / tag
    (root / ".claude").mkdir(parents=True)
    logs.mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env.update(PYTHONPATH=ctx["skill_creator"], PYTHONDONTWRITEBYTECODE="1", FAKE_SUITE=str(suite_file),
               FAKE_COUNTER=str(out / "roots" / (tag + ".counter")), TRIGGER_EVAL_CALL_LOG_DIR=str(logs),
               TRIGGER_EVAL_REAL_CLAUDE=str(real_claude or (HERE / "fake-claude")))
    env["PATH"] = str(out / ("shimbin" if shim_on_path else "emptybin")) + ":" + path_without_claude()
    env.update(fake_env)
    cmd = [sys.executable, "-m", "scripts.run_eval", "--eval-set", str(suite_file), "--skill-path", str(out / "neutral-skill"),
           "--description", "X", "--runs-per-query", "3", "--num-workers", "1", "--timeout", str(timeout),
           "--trigger-threshold", "0.5"]
    p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
    (out / (tag + ".json")).write_text(p.stdout, encoding="utf-8")
    (out / (tag + ".err")).write_text(p.stderr, encoding="utf-8")
    rc, cs = classify(logs, out / (tag + ".json"), timeout, role, out / (tag + ".classify.json"))
    try:
        rs = json.loads(p.stdout)["results"]
        gate = all(r["pass"] for r in rs)
    except (ValueError, KeyError):
        gate = None
    return {"tag": tag, "role": role, "gate": gate, "warning_lines": p.stderr.count("Warning: query failed"),
            "classify_rc": rc, "classify": cs}


def run_unmapped(ctx):
    """M1: 日志的 query 原文对不上 run_eval 输出 (直接调检查脚本, 不经 run_eval)。"""
    out = ctx["out"]
    logs = out / "logs" / "M1_unmapped_query"
    logs.mkdir(parents=True)
    (logs / "1-1.jsonl").write_text('{"shim":"start","ns":0}\n{"type":"stream_event","event":{"type":"message_stop"}}\n'
                                    '{"shim":"end","ns":1000000000}\n', encoding="utf-8")
    (logs / "1-1.query").write_text("不在输出里的 query", encoding="utf-8")
    ev = out / "M1_unmapped_query.json"
    ev.write_text(json.dumps({"results": [{"query": "输出里的 query", "should_trigger": False, "trigger_rate": 0.0,
                                           "triggers": 0, "runs": 1, "pass": True}]}, ensure_ascii=False), encoding="utf-8")
    rc, cs = classify(logs, ev, 120, "evaluated", out / "M1_unmapped_query.classify.json")
    return {"tag": "M1_unmapped_query", "role": "evaluated", "gate": True, "warning_lines": 0, "classify_rc": rc, "classify": cs}


def main(argv=None):
    ap = argparse.ArgumentParser(description="场景 4b 逐调用健康检查的故障矩阵")
    ap.add_argument("--suite", help="20 条套件 json (前 10 条 should-trigger, 后 10 条 should-not)")
    ap.add_argument("--out", help="输出目录 (缺省新建临时目录)")
    a = ap.parse_args(argv)
    skill_creator = os.environ.get("SKILL_CREATOR_ROOT", DEFAULT_SKILL_CREATOR)
    suite20 = Path(a.suite) if a.suite else find_suite()
    if suite20 is None or not suite20.is_file() or not (Path(skill_creator) / "scripts" / "run_eval.py").is_file():
        print("环境不全: 套件 %s / run_eval.py 于 %s" % (suite20, skill_creator), file=sys.stderr)
        return 2
    suite = json.loads(suite20.read_text(encoding="utf-8"))
    if [s["should_trigger"] for s in suite] != [True] * 10 + [False] * 10:
        print("套件形状不符: 须前 10 条 should-trigger、后 10 条 should-not", file=sys.stderr)
        return 2
    out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix="trigger-eval-fault-matrix-"))
    if out.exists():
        # 不删已有内容: --out 传错 (例如指到当前目录) 会毁掉整个目录 (R7 code-reviewer minor)
        if any(out.iterdir()):
            print("输出目录已存在且非空, 请换一个 --out: %s" % out, file=sys.stderr)
            return 2
    else:
        out.mkdir(parents=True)
    for sub in ("roots", "logs", "shimbin", "emptybin", "neutral-skill"):
        (out / sub).mkdir(parents=True)
    shutil.copy(HERE / "claude-shim.sh", out / "shimbin" / "claude")
    os.chmod(out / "shimbin" / "claude", 0o755)
    (out / "neutral-skill" / "SKILL.md").write_text(NEUTRAL_SKILL, encoding="utf-8")
    suite2 = out / "suite2.json"
    suite2.write_text(json.dumps([suite[0], suite[10]], ensure_ascii=False), encoding="utf-8")
    ctx = {"out": out, "skill_creator": skill_creator}
    every = {"FAKE_OUTAGE": "0-"}
    E, N = "evaluated", "negctrl"
    # (用例, 套件, 假 claude 设定, 超时, 垫片在 PATH 上, 真 claude 路径, 角色, 预期结论, 预期有 Warning, 预期 run_eval 门判定 / None 不查)
    cases = [
        ("U1_healthy_correct", suite2, {"FAKE_MODE": "correct"}, 120, True, None, E, "pass", False, True),
        ("U2_healthy_other_tool", suite2, {"FAKE_MODE": "other_tool"}, 120, True, None, E, "fail", False, False),
        ("U3_healthy_retry_frames", suite2, {"FAKE_MODE": "correct", "FAKE_RETRY_FRAMES": "1"}, 120, True, None, E, "pass", False, True),
        ("U4_healthy_never", suite2, {"FAKE_MODE": "never"}, 120, True, None, E, "fail", False, False),
        ("F1_result_error", suite2, dict(every, **ERR), 120, True, None, E, "void", False, False),
        ("F2_exit_after_init", suite2, dict(every, FAKE_KIND="exit_after_init"), 120, True, None, E, "void", False, False),
        ("F3_silent_exit", suite2, dict(every, FAKE_KIND="silent_exit"), 120, True, None, E, "void", False, False),
        ("F4_partial_then_exit", suite2, dict(every, FAKE_KIND="partial_then_exit"), 120, True, None, E, "void", False, False),
        ("F5_hang_timeout", suite2, dict(every, FAKE_KIND="hang", FAKE_HANG="5"), 3, True, None, E, "void", False, False),
        ("F6_decisive_after_timeout", suite2, dict(every, FAKE_KIND="slow_decisive", FAKE_HANG="5"), 3, True, None, E, "void", False, False),
        ("F7_real_claude_missing", suite2, {"FAKE_MODE": "correct"}, 120, True, "/nonexistent/claude", E, "void", False, False),
        ("F8_shim_not_on_path", suite2, {"FAKE_MODE": "correct"}, 120, False, None, E, "void", True, False),
        ("F9_decisive_in_timeout_margin", suite2, dict(every, FAKE_MODE="correct", FAKE_KIND="late_decisive", FAKE_HANG="2"), 3, True, None, E, "void", False, None),
        ("S1_overbroad_fault_in_shouldnot_half", suite20, dict(ERR, FAKE_MODE="all", FAKE_OUTAGE="30-"), 120, True, None, E, "void", False, True),
        ("S2_correct_fault_on_one_should_query", suite20, dict(ERR, FAKE_MODE="correct", FAKE_OUTAGE="6-8"), 120, True, None, E, "void", False, False),
        ("S3_healthy_correct", suite20, {"FAKE_MODE": "correct"}, 120, True, None, E, "pass", False, True),
        ("S4_healthy_overbroad", suite20, {"FAKE_MODE": "all"}, 120, True, None, E, "fail", False, False),
        ("S5_healthy_negctrl", suite20, {"FAKE_MODE": "never"}, 120, True, None, N, "valid", False, None),
        ("S6_one_run_fault_should", suite20, dict(ERR, FAKE_MODE="correct", FAKE_OUTAGE="6"), 120, True, None, E, "pass", False, True),
        ("S7_one_run_fault_shouldnot", suite20, dict(ERR, FAKE_MODE="correct", FAKE_OUTAGE="30"), 120, True, None, E, "pass", False, True),
        ("S8_two_run_fault_should", suite20, dict(ERR, FAKE_MODE="correct", FAKE_OUTAGE="6-7"), 120, True, None, E, "void", False, False),
        ("S9_negctrl_one_run_fault_x6", suite20, dict(ERR, FAKE_MODE="never", FAKE_OUTAGE="0,3,6,9,12,15"), 120, True, None, N, "valid", False, None),
        ("S10_negctrl_two_run_fault_x6", suite20, dict(ERR, FAKE_MODE="never", FAKE_OUTAGE="0-1,3-4,6-7,9-10,12-13,15-16"), 120, True, None, N, "void", False, None),
    ]
    with cf.ThreadPoolExecutor(9) as ex:
        futs = {ex.submit(run_case, ctx, *c[:7]): c for c in cases}
        done = {futs[f][0]: f.result() for f in cf.as_completed(futs)}
    done["M1_unmapped_query"] = run_unmapped(ctx)
    cases.append(("M1_unmapped_query", None, None, 120, True, None, E, "void", False, None))
    rows, mismatches = [], 0
    for c in cases:
        r = done[c[0]]
        cl = r["classify"] if isinstance(r["classify"], dict) else {}
        got = cl.get("verdict")
        ok = got == c[7] and (r["warning_lines"] > 0) == c[8] and (c[9] is None or r["gate"] == c[9])
        mismatches += 0 if ok else 1
        r.update(expected={"verdict": c[7], "warning": c[8], "gate": c[9]}, matches_expectation=ok)
        rows.append(r)
        print("%-38s 角色=%-9s 门=%-5s Warning=%d | 检查 rc=%s 结论=%-5s 不健康 %s %s | %s" % (
            r["tag"], r["role"], r["gate"], r["warning_lines"], r["classify_rc"], got, cl.get("unhealthy_calls"),
            cl.get("unhealthy_reasons"), "符合" if ok else "不符"))
    (out / "matrix-summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("用例 %d, 与预期不符 %d (明细: %s)" % (len(cases), mismatches, out / "matrix-summary.json"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
