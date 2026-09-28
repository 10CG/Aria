# exec_notes (r11y)

## 实际执行的命令

1. 读取 SKILL.md 并列 references 目录:
   `cat .../old-arm-1cb3872/skills/state-scanner/SKILL.md; ls .../references`
2. scan.py (Step 0), 工作目录 /home/dev/Aria:
   `python3 /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/old-arm-1cb3872/skills/state-scanner/scripts/scan.py --output /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r11y/state-snapshot.json > .../runs/r11y/scan_stdout.log 2> .../runs/r11y/scan_stderr.log`
   **退出码: 0** (stdout/stderr 均为空; errors[] 为空)
3. 用 python3 读 state-snapshot.json 的各字段 (remote_refresh / sync_status / multi_remote / git / changes / openspec / audit / custom_checks / handoff / tracks_multibranch / issue_status 等), 共 5 次只读解析。
4. 读 reference: `grep -n ... references/sync-detection.md RECOMMENDATION_RULES.md`; `sed -n 480,660p references/sync-detection.md`
5. 补充只读核验 (snapshot 只比当前分支, 不含 master): 对 /home/dev/Aria、aria、standards、aria-orchestrator 执行
   `git -C <repo> rev-parse --short --verify -q refs/heads/master|refs/remotes/origin/master|refs/remotes/github/master`
   (第一次用不带 --verify 的写法报 "Needed a single revision", 改写后重跑)。不 fetch, 不写。

## 未执行 (按评测约束)
- phase1_gate.py (Phase B 认领 / 心跳) 与 release_gate.py: 仅在回答中写出命令行。
- 未 commit/push/checkout 等, 未改仓库文件。注: scan.py 自身的 Phase 0.5 remote_refresh 会 git fetch 更新 remote-tracking ref (属 scan.py 内置行为)。
