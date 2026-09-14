#!/usr/bin/env bash
# v5: 自然措辞扩张敏感度 (预登记见 trigger-results-v5/PREREGISTRATION.md); 三臂同批, 全部 claude-opus-5
S=/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad
R=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator
OUT=$S/trigger-results-v5; mkdir -p $OUT
export PATH="$S/bin:$PATH" PYTHONPATH="$R"; unset CLAUDECODE
NEW='归档已完成的 OpenSpec 变更到 openspec/archive/ 目录，并做归档后落点校验。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"'
MILD='归档已完成的 OpenSpec 变更与相关文档到 archive/ 目录，整理项目收尾材料，并做归档后落点校验。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"、"整理归档文档"、"收尾整理"'
NEG='对一个事项做处理。'
run() { local name=$1; local desc=$2; local root=$S/trigger-proj-v5-$name; mkdir -p $root/.claude; cd $root || return 2
  echo "=== $name start $(date -u +%FT%TZ)" >> $OUT/run.log
  python3 -m scripts.run_eval --eval-set $S/trigger-eval-openspec-archive.json --skill-path $S/neutral-skill --description "$desc" --runs-per-query 3 --num-workers 1 --timeout 120 --model claude-opus-5 --verbose > $OUT/$name.json 2>> $OUT/$name.err
  echo "=== $name rc=$? end $(date -u +%FT%TZ)" >> $OUT/run.log; }
run mildcreep "$MILD" & run new "$NEW" & run negctrl "$NEG" & wait
echo ALL_DONE >> $OUT/run.log
