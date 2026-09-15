#!/usr/bin/env python3
"""逐调用健康检查 — 场景 4b (description 地板守卫) 的故障识别。

背景: skill-creator 的 run_eval.py 把 `claude -p` 的报错、超时、非零退出都记成一次「未触发」,
输出 json 里与「真没触发」分不开。claude 垫片 (claude-shim-logging.sh) 为每次调用另存一份
输出流; 本脚本逐次判断这次调用有没有正常走到 run_eval.py 据以下判定的那一步。
本脚本不判触发与否, 触发判定仍以 run_eval.py 的输出为准。

判定事件 (与 run_eval.py 的提前返回点一一对应), 输出流里出现任一即算:
  - stream_event 的 content_block_start, 且 content_block.type 为 tool_use
  - stream_event 的 message_stop
  - assistant 消息里含 tool_use
  - result 帧
单次调用健康 = 垫片起止记录齐全, 且有判定事件, 且没有报错的 result 帧 (is_error 为真,
  或 subtype 以 error 开头), 且耗时小于「超时阈值 - TIMEOUT_MARGIN_S」。
一臂健康 = 日志数等于 run_eval 输出里各 query 的 runs 之和, 且每次调用都健康
  (日志少了 = 有调用没走到垫片, 例如找不到 claude 时 run_eval 的 Popen 直接失败)。

退出码: 0 = 全部健康; 1 = 有不健康调用或日志数不符; 2 = 无法判定 (输出 json 或日志目录读不了)。
"""
import argparse
import json
import sys
from pathlib import Path

# run_eval.py 的读循环每轮最多等 1 秒, 超时后才 kill 进程; 留 1 秒余量, 宁可判不健康。
TIMEOUT_MARGIN_S = 1.0


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
    return {
        "file": path.name,
        "frames": frames,
        "first_decisive": decisive[0] if decisive else None,
        "duration_s": None if duration is None else round(duration, 2),
        "healthy": not reasons,
        "reasons": reasons,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="场景 4b 逐调用健康检查")
    ap.add_argument("--log-dir", required=True, help="本臂的垫片日志目录 (TRIGGER_EVAL_CALL_LOG_DIR)")
    ap.add_argument("--eval-output", required=True, help="本臂 run_eval.py 的输出 json")
    ap.add_argument("--timeout", type=float, required=True, help="本臂 run_eval.py 的 --timeout")
    ap.add_argument("--report", help="把逐调用明细写进这个 json 文件")
    a = ap.parse_args(argv)
    try:
        out = json.loads(Path(a.eval_output).read_text(encoding="utf-8"))
        expected = sum(int(r["runs"]) for r in out["results"])
        log_dir = Path(a.log_dir)
        if not log_dir.is_dir():
            raise OSError("日志目录不存在: %s" % log_dir)
        files = sorted(log_dir.glob("*.jsonl"))
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("UNDECIDABLE: %s" % e, file=sys.stderr)
        return 2
    rows = [classify_file(f, a.timeout) for f in files]
    bad = [r for r in rows if not r["healthy"]]
    reasons = {}
    for r in bad:
        for x in r["reasons"]:
            reasons[x] = reasons.get(x, 0) + 1
    summary = {
        "expected_calls": expected,
        "logged_calls": len(files),
        "unhealthy_calls": len(bad),
        "unhealthy_reasons": reasons,
        "healthy": len(files) == expected and not bad,
    }
    if a.report:
        Path(a.report).write_text(
            json.dumps({"summary": summary, "calls": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["healthy"] else 1


if __name__ == "__main__":
    sys.exit(main())
