#!/usr/bin/env bash
# v6b 重跑 (预登记修订见 PREREGISTRATION-AMENDMENT.md): 真 claude 经新垫片 (另记 query 原文) 跑原样的 run_eval.py,
# 检查脚本按角色判定 (被评 evaluated / 负控 negctrl)。用法: run_real_v6b.sh probes | full
X=/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/v6exp
S=$X/stage
R=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator
SUITE=/home/dev/Aria/aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/trigger-eval-openspec-archive.json
OUT=$X/real-v6b; mkdir -p "$OUT" "$OUT/shimbin"
cp "$S/claude-shim.sh" "$OUT/shimbin/claude"; chmod +x "$OUT/shimbin/claude"
export PATH="$OUT/shimbin:$PATH" PYTHONPATH="$R" PYTHONDONTWRITEBYTECODE=1
unset CLAUDECODE TRIGGER_EVAL_REAL_CLAUDE   # 垫片默认指向真 claude
NEW='归档已完成的 OpenSpec 变更到 openspec/archive/ 目录，并做归档后落点校验。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"'
NEG='对一个事项做处理。'
run() { # name suite desc timeout model runs role
  local name=$1 suite=$2 desc=$3 timeout=$4 model=$5 runs=$6 role=$7
  local root=$X/roots-real-v6b/$name logs=$OUT/logs/$name
  rm -rf "$root" "$logs"; mkdir -p "$root/.claude" "$logs"; cd "$root" || return 2
  echo "=== $name start $(date -u +%FT%TZ)" >> "$OUT/run.log"
  TRIGGER_EVAL_CALL_LOG_DIR=$logs python3 -m scripts.run_eval --eval-set "$suite" --skill-path "$X/neutral-skill" \
    --description "$desc" --runs-per-query "$runs" --num-workers 1 --timeout "$timeout" --trigger-threshold 0.5 \
    --model "$model" --verbose > "$OUT/$name.json" 2>> "$OUT/$name.err"
  echo "=== $name rc=$? end $(date -u +%FT%TZ)" >> "$OUT/run.log"
  python3 "$S/classify_calls.py" --log-dir "$logs" --eval-output "$OUT/$name.json" --timeout "$timeout" --role "$role" \
    --report "$OUT/$name.classify.json" > "$OUT/$name.classify.summary" 2>&1
  echo "=== $name classify rc=$? $(cat "$OUT/$name.classify.summary")" >> "$OUT/run.log"
}
case "${1:-}" in
  probes)
    run B1_bad_model "$X/suite2.json" "$NEW" 120 claude-nonexistent-model-v6 1 evaluated &
    run B2_timeout3 "$X/suite2.json" "$NEW" 3 claude-opus-5 1 evaluated &
    wait ;;
  full)
    run C1_new "$SUITE" "$NEW" 120 claude-opus-5 3 evaluated &
    run C2_negctrl "$SUITE" "$NEG" 120 claude-opus-5 3 negctrl &
    wait ;;
  *) echo "用法: $0 probes|full" >&2; exit 2 ;;
esac
echo "ALL_DONE $1 $(date -u +%FT%TZ)" >> "$OUT/run.log"
