#!/usr/bin/env bash
# v4: 两个反事实臂 (同 v3 隔离 + 中性名 + 单 worker)
#  overbroad  = 过宽 description, 验证 should-not 的 FAIL 分支是否可达 (qa 席 critical)
#  realroot   = v1.73.0 description, 但项目根含可探索文件 (openspec/changes/*/proposal.md 等), 验证「第一个 tool_use」判据在非空根下是否失真 (backend 席 major)
S=/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad
R=/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator
OUT=$S/trigger-results-v4; mkdir -p $OUT
export PATH="$S/bin:$PATH" PYTHONPATH="$R"; unset CLAUDECODE
OVERBROAD='处理与 openspec、spec、变更、归档、整理、收尾、文档、issue、分支、目录、报告相关的任何任务。只要用户提到 openspec/、archive、归档、整理、收尾、changes、proposal、handoff、issue、分支 中任意一个词, 都必须先使用本技能。'
NEW='归档已完成的 OpenSpec 变更到 openspec/archive/ 目录，并做归档后落点校验。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"'
run() { local name=$1; local desc=$2; local root=$S/trigger-proj-v4-$name; mkdir -p $root/.claude
  if [ "$name" = realroot ]; then
    for c in handoff-multibranch-subdir-path-fidelity aria-2.0-m6-release-closeout state-scanner-stale-refs-false-parity aria-ci-backend-abstraction aria-secret-guard-manifest-precision forgejo-hosts-parameterization aria-124-submodule-pointer-regression-gate pre-merge-completeness-gate-change-scope linked-issue-normalization a1-entry-claim-duplicate-work-guard aria-2.0-m6-e2e-resilience; do
      mkdir -p $root/openspec/changes/$c; printf '# Proposal: %s\n\n> **Status**: done\n\n## Why\n...\n' "$c" > $root/openspec/changes/$c/proposal.md; printf -- '- [x] task 1\n- [x] task 2\n' > $root/openspec/changes/$c/tasks.md; done
    mkdir -p $root/openspec/archive/2026-08-01-example-change $root/docs/handoff $root/.aria/audit-reports; printf '# Proposal: example\n' > $root/openspec/archive/2026-08-01-example-change/proposal.md; printf '# handoff\n' > $root/docs/handoff/2026-09-01-example.md; printf '# Example project\n' > $root/README.md
  fi
  cd $root || return 2
  echo "=== $name start $(date -u +%FT%TZ)" >> $OUT/run.log
  python3 -m scripts.run_eval --eval-set $S/trigger-eval-openspec-archive.json --skill-path $S/neutral-skill --description "$desc" --runs-per-query 3 --num-workers 1 --timeout 120 --model claude-fable-5-1 --verbose > $OUT/$name.json 2>> $OUT/$name.err
  echo "=== $name rc=$? end $(date -u +%FT%TZ)" >> $OUT/run.log; }
run overbroad "$OVERBROAD" & run realroot "$NEW" & wait
echo ALL_DONE >> $OUT/run.log
