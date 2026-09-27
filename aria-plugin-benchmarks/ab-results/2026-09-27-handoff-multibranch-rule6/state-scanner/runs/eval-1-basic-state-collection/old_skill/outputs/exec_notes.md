# exec_notes (r01x)

实际执行过的命令 (全部只读, 未对 /home/dev/Aria 做任何写操作):

1. cat SKILL.md + ls references/ (skill 根 /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/old-arm-1cb3872/skills/state-scanner)
2. cd /home/dev/Aria && python3 /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/old-arm-1cb3872/skills/state-scanner/scripts/scan.py --output /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r01x/state-snapshot.json > .../r01x/scan_stdout.log 2> .../r01x/scan_stderr.log
   -> 退出码 0; stdout/stderr 均为空; snapshot 947070 字节
3. git -C /home/dev/Aria status --short (确认仓内无新增文件)
4. cat references/recommendation-stages.md / RECOMMENDATION_RULES.md / sed -n 1,200p references/output-formats.md
5. 多次 python3 -c 读 snapshot JSON 各段 (git/openspec/requirements/issue_status/tracks_multibranch/sync_status 等)
6. python3 -c 读 /home/dev/Aria/.aria/config.json 的 state_scanner / workflow / audit 段
7. ls docs/handoff; head -30 docs/handoff/latest.md
8. git ls-tree -r --name-only origin/master -- docs/handoff ; 同 HEAD; git log --oneline origin/master 等 (定位 master 上更新的 handoff)
9. git show origin/master:docs/handoff/latest.md ; git show origin/master:docs/handoff/2026-09-27-session-close-195-task025-legacy-issue-204.md
10. echo $ARIA_COORDINATION_NO_PUSH (=1); ls ab-results/2026-09-27-handoff-multibranch-rule6/; git rev-parse refs/aria/coordination origin/master HEAD; git merge-base HEAD origin/master

未执行 (只写出命令):
- phase1_gate.py --heartbeat-only ... (A.1 心跳) —— 评测约束禁止 + handoff 要求 AB 会话跳过
- phase1_gate.py --phase B --mode advisory ... (Phase B 入口闸) —— 同上, 且 handoff 明确不对本轨再跑认领闸 (aria-plugin#202)
- git ls-remote origin refs/aria/coordination —— 未跑, 在答复中列为 TASK-026 前置待核
