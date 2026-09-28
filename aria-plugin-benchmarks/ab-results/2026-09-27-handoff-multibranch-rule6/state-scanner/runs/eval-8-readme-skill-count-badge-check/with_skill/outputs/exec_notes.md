# exec_notes r08y

## scan.py
- cd /home/dev/Aria && python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r08y/state-snapshot.json > .../runs/r08y/scan_stdout.log 2> .../runs/r08y/scan_stderr.log
- 退出码: 0 (stderr 为空, errors[] 为空)
- 副作用说明: scan.py 自身刷新了 gitignored 缓存 .aria/cache/{remote-refresh,issues,context-window,gitlink-integrity}.json (collector 内置行为, 非我手写); .aria/state-snapshot.json 未被改动 (mtime 仍为 13:05); git status 前后一致。

## 其他只读命令
- cat SKILL.md; ls references/
- python3 读 snapshot 各字段 (readme/git/errors/interrupt/changes/custom_checks/upm/openspec/audit/handoff/sync_status/standards/tracks_multibranch/requirements/architecture/forgejo_config/issue_status/handoff_worktrees/coordination_fetch/remote_refresh)
- git -C /home/dev/Aria status --short
- grep version aria/.claude-plugin/plugin.json marketplace.json; cat aria/VERSION VERSION
- git -C aria log -1; git submodule status; git -C aria tag -l 'v1.14.0' 'v1.73*' 'v1.1[0-9]*'
- git -C aria log --all -S'"version": "1.14.0"' -- .claude-plugin/plugin.json (找到 06a0edf, 2026-04-12)
- ls aria/skills; 找缺 SKILL.md 的目录 (issue-triage-workspace)
- python3 比对 aria/README.md 与 aria/README.zh.md 的 Skills 段列表 vs skills/*/SKILL.md 目录集合, 统计 user-invocable:false
- grep badge / "N Skills" 于 README*.md, aria/README*.md, docs/architecture/system-architecture.md
- git -C aria log --diff-filter=A 查 session-closer / issue-triage 引入提交
- grep output-formats.md / RECOMMENDATION_RULES.md 的 README 相关规则
- find .aria -newer <prompt> (核副作用)

## 未执行
- phase1_gate.py (collision.kind=self_multi_container, Phase B-entry 才调用; 命令行已写入 answer.md, 未执行)
- 无 commit/push/checkout 等写操作
