# exec_notes (r10x)

执行过的命令 (均在 /home/dev/Aria, 只读; 未调用 phase1_gate.py / release_gate.py; 未修改仓库文件):

1. cat /home/dev/Aria/aria/skills/state-scanner/SKILL.md; ls references/
2. mkdir -p <runs/r10x>; cd /home/dev/Aria && python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r10x/state-snapshot.json > .../scan_stdout.log 2> .../scan_stderr.log
   -> 退出码 0; 之后 git status --porcelain 确认仓库状态没有变化
3. python3 读取 snapshot 的 git / sync_status / remote_refresh / errors 等区块
4. grep plugin.json version; git -C aria show 1cb3872:.claude-plugin/plugin.json; git -C {.,aria,standards} rev-parse (HEAD, refs/remotes/{origin,github}/master); git -C aria tag -l; git -C aria log --oneline; 用 python3 读取 snapshot 其余区块
5. git -C {.,aria,standards} ls-remote {origin,github} refs/heads/master refs/heads/feature/handoff-multibranch-subdir-path-fidelity (timeout 60)
6. git -C aria ls-remote --tags {origin,github} v1.73.3 v1.15.0; git -C aria rev-parse v1.73.3^{}

说明: scan.py 在 Phase 0.5 会对远程执行 fetch, 这属于该 skill 的固有行为, 会更新本地的远程跟踪 ref, 不涉及仓库文件的改动。scan.py 输出写到了 runs 目录, 没有写 .aria/state-snapshot.json。
