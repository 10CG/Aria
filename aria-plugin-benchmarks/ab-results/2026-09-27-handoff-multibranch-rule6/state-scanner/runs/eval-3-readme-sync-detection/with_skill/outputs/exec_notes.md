# exec_notes r03x

所有命令在 /home/dev/Aria 下执行 (或用 git -C), 均为只读; 未修改仓库任何文件, 未调用 phase1_gate.py / release_gate.py。

## scan.py
- `python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r03x/state-snapshot.json > .../r03x/scan_stdout.log 2> .../r03x/scan_stderr.log`
  - 退出码: **0** (stdout/stderr 均为空, errors[] 为空)

## 读取 skill 定义与参考
- `cat /home/dev/Aria/aria/skills/state-scanner/SKILL.md; ls .../references`
- `sed -n 1,200p references/recommendation-stages.md`
- `sed -n 1,140p references/output-formats.md; grep -n 'README|插件依赖|版本一致' references/output-formats.md`

## 解析 snapshot (python3 -c json.load 读 scratchpad 内 state-snapshot.json)
- 各顶层字段大小 / errors / git / readme
- upm, changes, architecture, audit, standards, forgejo_config, handoff, handoff_worktrees, interrupt, coordination_fetch, remote_refresh, sync_status, custom_checks
- openspec, requirements, tracks_multibranch (含 #195 过滤), issue_status

## 只读补充核对 (snapshot 之后读外部文件, SKILL.md 允许)
- `git -C aria show 1cb3872:.claude-plugin/plugin.json | grep version`; 同 b181678
- `git -C aria log --oneline 1cb3872..b181678`; `git -C standards log --oneline 940cb5b..d86fc91`; `git -C aria diff --stat 1cb3872 b181678`
- `head -20 README.md | grep badge`; `grep -n 版本 VERSION`
- `grep version aria/.claude-plugin/marketplace.json`; `head -5 aria/VERSION`; `grep '^## ' aria/CHANGELOG.md`; i18n README translated-from 标记; system-architecture.md aria-plugin 行
- `ls -t docs/handoff | head`; `head -3 docs/handoff/latest.md`
- `cat docs/handoff/2026-09-24-session-close-199-post-planning-converged.md | head -150`
- `git log -3 origin/master`; `git ls-tree --name-only origin/master docs/handoff/`; `git rev-list --count origin/master..HEAD` (13) / `HEAD..origin/master` (12)
- `git show origin/master:docs/handoff/2026-09-27-session-close-195-task025-legacy-issue-204.md | head -120`; `git show origin/master:docs/handoff/latest.md | head -8`
- `python3 -c` 读 .aria/config.json (audit / issue_scan / workflow 段); `git status --short`
- `sed -n 20,30p VERSION`; `sed -n 1,5p standards/openspec/project.md`; `git -C standards show 940cb5b:openspec/project.md`; `grep Version standards/conventions/session-handoff.md`
- `grep -n '1.7x.x' VERSION`; `git show origin/master:VERSION | grep 'aria (插件)'`; `git log -S'v1.73.0' --oneline -- VERSION`; README*/version-scheme.md 中 plugin 版本; aria/README.md 版本行
- `ls standards; git tag` (standards 无 tag/CHANGELOG); aria-orchestrator 版本文件 (无)
- `git -C aria-orchestrator tag --points-at 86bb684` (无 tag); `git -C aria tag --sort=-v:refname | head -2` (v1.73.3)

## 未执行 (仅在答复中列出)
- phase1_gate.py (Phase B-entry advisory 认领) —— 评测约束禁止; 且本会话未持 claim、handoff 要求 AB 会话跳过心跳
