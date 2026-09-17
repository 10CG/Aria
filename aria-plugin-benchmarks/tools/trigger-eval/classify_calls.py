#!/usr/bin/env python3
"""逐调用健康检查 — 场景 4b (description 地板守卫) 的故障识别。

背景: skill-creator 的 run_eval.py 把 `claude -p` 的报错、超时、非零退出都记成一次「未触发」,
输出 json 里与「真没触发」分不开。claude 垫片 (claude-shim.sh) 为每次调用另存一份输出流
(`<id>.jsonl`) 与 query 原文 (`<id>.query`); 本脚本逐次判断调用是否正常完成, 再判断不健康的
调用能不能改变本臂的判定。触发与否仍以 run_eval.py 的输出为准。

单次调用健康 = 垫片起止记录齐全, 且输出流里有 run_eval.py 据以下判定的事件 (tool_use 开始 /
  message_stop / 含 tool_use 的 assistant 消息 / 结果帧), 且没有报错的结果帧 (is_error 为真或
  subtype 以 error 开头), 且耗时小于「超时阈值 - TIMEOUT_MARGIN_S」。

把调用对到 query: 用 `.query` 文件的原文对 run_eval 输出里的 query。有调用对不上, 或某条 query
  的日志数不等于它的 runs ⇒ void。

不健康的调用能不能改变判定: 它的真实结果未知, 按「触发」「没触发」两种可能都算。输出流里出现过
  tool_use 的不健康调用, run_eval 可能已把它记成触发; 没出现过的, run_eval 只可能记成未触发。
  于是每条 query 的真实触发次数落在 [triggers - 可能被记成触发的不健康数, triggers + 不健康数] 里。
  --role evaluated: 各 query 都取最不利一端门仍通过 ⇒ pass; 取最有利一端门仍不通过 ⇒ fail; 其余 ⇒ void。
  --role negctrl: should-trigger 命中数 (触发率 ≥ 阈值的条数) 的上界 ≤ --negctrl-max-hits ⇒ valid, 否则 void。

退出码: 0 = 判定不受不健康调用影响 (pass / fail / valid); 1 = void; 2 = 无法判定 (输出 json 或日志目录读不了)。
"""
import argparse
import json
import sys
from pathlib import Path

# run_eval.py 的读循环每轮最多等 1 秒, 超时后才 kill 进程; 留 1 秒余量, 宁可判不健康。
TIMEOUT_MARGIN_S = 1.0
# 只有这两类事件能让 run_eval.py 判「触发」; 输出流里一次都没出现过, run_eval 只可能记成未触发。
TRIGGER_CAPABLE = ("tool_use_start", "assistant_tool_use")


def classify_file(path, timeout):
    start = end = None
    decisive = []
    errored = False
    frames = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        if ev.get("shim") == "start":
            start = ev.get("ns")
            continue
        if ev.get("shim") == "end":
            end = ev.get("ns")
            continue
        frames += 1
        kind = ev.get("type")
        if kind == "stream_event":
            se = ev.get("event") or {}
            if se.get("type") == "content_block_start" and (se.get("content_block") or {}).get("type") == "tool_use":
                decisive.append("tool_use_start")
            elif se.get("type") == "message_stop":
                decisive.append("message_stop")
        elif kind == "assistant":
            content = (ev.get("message") or {}).get("content") or []
            if any(isinstance(c, dict) and c.get("type") == "tool_use" for c in content):
                decisive.append("assistant_tool_use")
        elif kind == "result":
            decisive.append("result")
            if ev.get("is_error") or str(ev.get("subtype", "")).startswith("error"):
                errored = True
    reasons = []
    duration = None
    if start is None or end is None:
        reasons.append("缺垫片起止记录")
    else:
        duration = (end - start) / 1e9
        if duration >= timeout - TIMEOUT_MARGIN_S:
            reasons.append("耗时达到超时阈值")
    if not decisive:
        reasons.append("无判定事件")
    if errored:
        reasons.append("result 帧报错")
    try:
        query = path.with_suffix(".query").read_text(encoding="utf-8")
    except OSError:
        query = None
    return {
        "file": path.name,
        "query": query,
        "frames": frames,
        "first_decisive": decisive[0] if decisive else None,
        "may_be_recorded_true": any(d in TRIGGER_CAPABLE for d in decisive),
        "duration_s": None if duration is None else round(duration, 2),
        "healthy": not reasons,
        "reasons": reasons,
    }


def judge(results, rows, role, threshold, negctrl_max_hits):
    by_query = {r["query"]: r for r in results}
    tally = {q: {"n": 0, "u_false": 0, "u_maybe": 0} for q in by_query}
    unmapped = 0
    for c in rows:
        t = tally.get(c["query"])
        if t is None:
            unmapped += 1
            continue
        t["n"] += 1
        if not c["healthy"]:
            t["u_maybe" if c["may_be_recorded_true"] else "u_false"] += 1
    mismatch = sum(1 for q, t in tally.items() if t["n"] != int(by_query[q]["runs"]))
    per_query = []
    for q, r in by_query.items():
        t = tally[q]
        runs, trig = int(r["runs"]), int(r["triggers"])
        lo = max(0, trig - t["u_maybe"])
        hi = min(runs, trig + t["u_false"] + t["u_maybe"])
        if r["should_trigger"]:
            worst, best = lo / runs >= threshold, hi / runs >= threshold
        else:
            worst, best = hi / runs < threshold, lo / runs < threshold
        per_query.append({"query": q, "should_trigger": r["should_trigger"], "runs": runs, "triggers": trig,
                          "unhealthy": t["u_false"] + t["u_maybe"], "triggers_range": [lo, hi],
                          "pass_worst": worst, "pass_best": best})
    out: dict = {"unmapped_calls": unmapped, "count_mismatch_queries": mismatch}
    if role == "evaluated":
        out["gate_recorded"] = all(r["pass"] for r in results)
        if unmapped or mismatch:
            verdict = "void"
        elif all(x["pass_worst"] for x in per_query):
            verdict = "pass"
        elif not all(x["pass_best"] for x in per_query):
            verdict = "fail"
        else:
            verdict = "void"
    else:
        st = [x for x in per_query if x["should_trigger"]]
        out["hits_recorded"] = sum(1 for x in st if x["triggers"] / x["runs"] >= threshold)
        out["hits_min"] = sum(1 for x in st if x["triggers_range"][0] / x["runs"] >= threshold)
        out["hits_max"] = sum(1 for x in st if x["triggers_range"][1] / x["runs"] >= threshold)
        verdict = "void" if (unmapped or mismatch or out["hits_max"] > negctrl_max_hits) else "valid"
    out["verdict"] = verdict
    return out, per_query


def main(argv=None):
    ap = argparse.ArgumentParser(description="场景 4b 逐调用健康检查")
    ap.add_argument("--log-dir", required=True, help="本臂的垫片日志目录 (TRIGGER_EVAL_CALL_LOG_DIR, 每臂新建的空目录)")
    ap.add_argument("--eval-output", required=True, help="本臂 run_eval.py 的输出 json")
    ap.add_argument("--timeout", type=float, required=True, help="本臂 run_eval.py 的 --timeout")
    ap.add_argument("--role", required=True, choices=("evaluated", "negctrl"), help="本臂是被评臂还是负控臂")
    ap.add_argument("--trigger-threshold", type=float, default=0.5, help="与 run_eval.py 的 --trigger-threshold 相同")
    ap.add_argument("--negctrl-max-hits", type=int, default=5, help="负控 should-trigger 命中数上限")
    ap.add_argument("--report", help="把逐调用与逐 query 明细写进这个 json 文件")
    a = ap.parse_args(argv)
    try:
        results = json.loads(Path(a.eval_output).read_text(encoding="utf-8"))["results"]
        for r in results:  # 字段缺失或类型不对 ⇒ 无法判定 (退出码 2)
            _ = (int(r["runs"]), int(r["triggers"]), r["query"], r["should_trigger"], r["pass"])
        log_dir = Path(a.log_dir)
        if not log_dir.is_dir():
            raise OSError("日志目录不存在: %s" % log_dir)
        files = sorted(log_dir.glob("*.jsonl"))
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("UNDECIDABLE: %s" % e, file=sys.stderr)
        return 2
    rows = [classify_file(f, a.timeout) for f in files]
    verdict, per_query = judge(results, rows, a.role, a.trigger_threshold, a.negctrl_max_hits)
    reasons = {}
    for r in rows:
        for x in r["reasons"]:
            reasons[x] = reasons.get(x, 0) + 1
    summary = {"role": a.role, "expected_calls": sum(int(r["runs"]) for r in results), "logged_calls": len(files),
               "unhealthy_calls": sum(1 for r in rows if not r["healthy"]), "unhealthy_reasons": reasons}
    summary.update(verdict)
    if a.report:
        Path(a.report).write_text(json.dumps({"summary": summary, "queries": per_query, "calls": rows},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if summary["verdict"] == "void" else 0


if __name__ == "__main__":
    sys.exit(main())
