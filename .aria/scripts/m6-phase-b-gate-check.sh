#!/bin/bash
# M6 Phase B gate check — auto-scheduled 2026-05-30 (owner-requested reminder).
# Runs the 3-day-rolling-history validator ON light-1, because the cost snapshots
# are node-local (/root/Aria/aria-orchestrator/.aria/cost-snapshots/) — Blocker #2:
# running the validator on this dev box reads dev's empty dir.
# One-shot: removes its own crontab line after running.
#
# Background: docs/handoff/2026-05-30-m6-cost-snapshot-hotfix-deployed.md
#             .aria/notes/2026-05-30-m6-phase-b-blocker-chain-cost-snapshot.md
set +e
export PATH="/home/dev/.local/bin:/usr/local/bin:/usr/bin:/bin"
export NOMAD_ADDR="http://192.168.69.70:4646"

OUT="/home/dev/Aria/.aria/notes/2026-06-01-m6-phase-b-gate-result.md"
NODE="root@192.168.69.90"
SSH="ssh -o ConnectTimeout=20 -o BatchMode=yes"
# --snapshots-dir → durable host volume (Blocker #2 fix, m6-cost-snapshot-durable-volume).
# Snapshots are written by the cost-sentinel cron to the host volume (same as the DB),
# NOT the node git checkout. Requires the cost-sentinel redeploy + snapshot migration to
# have completed (TASK-005~007); before that the volume dir is empty.
SNAPSHOTS_DIR="/opt/aether-volumes/aria-layer1/data/cost-snapshots"
VALIDATOR="/opt/aria-orchestrator/venv/bin/python /root/Aria/aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history --snapshots-dir $SNAPSHOTS_DIR"

{
  echo "# M6 Phase B Gate Check — auto-run $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "> 自动任务 (2026-05-30 设的 crontab one-shot)。在 light-1 上跑 3-day rolling history 闸门。"
  echo "> snapshot 是 node-local (Blocker #2),故 validator 必须在 light-1 上跑。"
  echo ""
  echo '## 1. 3-day rolling history check (validator on light-1)'
  echo '```'
  $SSH "$NODE" "$VALIDATOR; echo EXIT=\$?" 2>&1
  echo '```'
  echo ""
  echo '## 2. snapshot files on node'
  echo '```'
  $SSH "$NODE" "ls -la $SNAPSHOTS_DIR/cost-*.json 2>&1"
  echo '```'
  echo ""
  echo '## 3. cost-sentinel cron 近期运行 (exit 状态)'
  echo '```'
  nomad job status aria-layer1-cost-sentinel 2>&1 | grep -iE "Status|Periodic|Children|dead|complete|failed" | head -10
  echo '```'
  echo ""
  echo "## 结论"
  echo "- section 1 见 \`EXIT=0\` → ✅ 3-day 闸门 PASS,M6 e2e-resilience Phase B 可启动。"
  echo "- \`EXIT≠0\` → 看 section 2/3:缺哪天 snapshot / cron 是否某日 exit≠0(若某天 dead 非 complete)。"
  echo ""
  echo "_下一步详见 docs/handoff/2026-05-30-m6-cost-snapshot-hotfix-deployed.md §6_"
} > "$OUT" 2>&1

# one-shot: 跑完移除自身 crontab 行 (避免每年 6/1 重跑)
crontab -l 2>/dev/null | grep -v "m6-phase-b-gate-check.sh" | crontab - 2>/dev/null
exit 0
