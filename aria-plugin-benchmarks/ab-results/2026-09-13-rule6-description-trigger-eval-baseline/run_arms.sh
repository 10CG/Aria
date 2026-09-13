#!/usr/bin/env bash
S=/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad
R=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator
OUT=$S/trigger-results; cd $S/trigger-proj || exit 2
export PATH="$S/bin:$PATH" PYTHONPATH="$R"; unset CLAUDECODE
OLD='归档已完成的 OpenSpec 变更到正确的 archive/ 目录，自动修正 CLI bug。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"'
NEG='对一个已完成的事项做收尾处理，并核对处理结果。'
run() { # name, [description]
  local name=$1; shift
  echo "=== $name start $(date -u +%FT%TZ)" >> $OUT/run.log
  if [ $# -gt 0 ]; then
    python3 -m scripts.run_eval --eval-set $S/trigger-eval-openspec-archive.json --skill-path /home/dev/Aria/aria/skills/openspec-archive --description "$1" --runs-per-query 3 --num-workers 4 --timeout 120 --model claude-fable-5-1 --verbose > $OUT/$name.json 2>> $OUT/run.log
  else
    python3 -m scripts.run_eval --eval-set $S/trigger-eval-openspec-archive.json --skill-path /home/dev/Aria/aria/skills/openspec-archive --runs-per-query 3 --num-workers 4 --timeout 120 --model claude-fable-5-1 --verbose > $OUT/$name.json 2>> $OUT/run.log
  fi
  echo "=== $name rc=$? end $(date -u +%FT%TZ)" >> $OUT/run.log
}
run new
run old "$OLD"
run negctrl "$NEG"
echo ALL_DONE >> $OUT/run.log
