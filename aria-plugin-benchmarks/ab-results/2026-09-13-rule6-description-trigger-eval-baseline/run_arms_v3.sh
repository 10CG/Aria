#!/usr/bin/env bash
# v3: 同 v2 隔离 + 合成命令名中性化 (name: helper), 消除文件名泄漏意图
S=/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad
R=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator
OUT=$S/trigger-results-v3; mkdir -p $OUT
export PATH="$S/bin:$PATH" PYTHONPATH="$R"; unset CLAUDECODE
OLD='归档已完成的 OpenSpec 变更到正确的 archive/ 目录，自动修正 CLI bug。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"'
NEG='对一个已完成的事项做收尾处理，并核对处理结果。'
PUSHY='归档已完成的 OpenSpec 变更到 openspec/archive/ 目录，并做归档后落点校验。只要用户提到「归档 spec」「归档变更」「Phase D.2」「D.2」「把做完的 spec 收进 archive」「openspec archive」「变更完成后收尾归档」, 哪怕没有直呼技能名, 都必须使用本技能, 不要自己手工 mv。'
run() { local name=$1; shift; local root=$S/trigger-proj-v3-$name; mkdir -p $root/.claude; cd $root || return 2
  echo "=== $name start $(date -u +%FT%TZ)" >> $OUT/run.log
  if [ $# -gt 0 ]; then DESC=(--description "$1"); else DESC=(); fi
  python3 -m scripts.run_eval --eval-set $S/trigger-eval-openspec-archive.json --skill-path /tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/neutral-skill "${DESC[@]}" --runs-per-query 3 --num-workers 1 --timeout 120 --model claude-fable-5-1 --verbose > $OUT/$name.json 2>> $OUT/$name.err
  echo "=== $name rc=$? end $(date -u +%FT%TZ)" >> $OUT/run.log; }
run new & run old "$OLD" & run negctrl "$NEG" & run poscontrol "$PUSHY" & wait
echo ALL_DONE >> $OUT/run.log
