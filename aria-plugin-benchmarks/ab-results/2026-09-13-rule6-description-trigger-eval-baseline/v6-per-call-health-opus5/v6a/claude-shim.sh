#!/usr/bin/env bash
# claude 垫片 (场景 4b): 给 run_eval.py 调起的每次 `claude -p` 追加 --setting-sources project,
# 并把这次调用的输出流另存一份, 供 classify_calls.py 逐调用判断是否正常完成。
# run_eval.py 看到的 stdout 经 tee 原样转交, 不增不改; stderr 本来被 run_eval.py 丢弃, 这里另存。
# 用 exec 让真 claude 接管本进程号: run_eval.py 超时或提前判定后 kill 的就是真 claude。
set -u
d="${TRIGGER_EVAL_CALL_LOG_DIR:?TRIGGER_EVAL_CALL_LOG_DIR 未设置}"
id="$(date +%s%N)-$$"
f="$d/$id.jsonl"
printf '{"shim":"start","ns":%s}\n' "$(date +%s%N)" > "$f"
exec 2>> "$d/$id.err"
exec > >(tee -p -a "$f"; printf '{"shim":"end","ns":%s}\n' "$(date +%s%N)" >> "$f")
exec "${TRIGGER_EVAL_REAL_CLAUDE:-/home/dev/.local/bin/claude}" "$@" --setting-sources project
