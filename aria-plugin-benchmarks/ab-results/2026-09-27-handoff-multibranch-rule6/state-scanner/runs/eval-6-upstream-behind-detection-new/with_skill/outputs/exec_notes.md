# exec_notes (r06y)

实际执行过的命令 (全部只读; 未 commit/push/checkout/merge/reset/stash; 未写仓库内文件; 未调用 phase1_gate.py / release_gate.py):

1. `cat /home/dev/Aria/aria/skills/state-scanner/SKILL.md; ls .../state-scanner/references`
2. `cd /home/dev/Aria && python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output $R/state-snapshot.json >$R/scan_stdout.log 2>$R/scan_stderr.log`  -> 退出码 0
   (随后 `git -C /home/dev/Aria status --porcelain` 确认仓库工作区与扫描前一致)
   注: scan.py 的 Phase 0.5 remote_refresh 自身会 fetch 远程引用 (8 路, 全部 fetch_ok)
3. `python3 -c` 读取 $R/state-snapshot.json 各段 (git / remote_refresh / errors / sync_status / 其余各 collector)
4. `grep -n ... references/sync-detection.md references/output-formats.md RECOMMENDATION_RULES.md references/recommendation-stages.md`
5. `sed -n 530,720p references/output-formats.md`
6. 补充只读核对 (快照不含 feature vs master 比较):
   `for p in . aria standards; do git -C $p rev-parse --abbrev-ref HEAD; git -C $p rev-list --left-right --count HEAD...origin/master; git -C $p rev-list --left-right --count HEAD...github/master; git -C $p log --oneline HEAD..origin/master | head -8; done`
   结果: 主仓 13/12, aria 9/0, standards 2/0
7. `git merge-base HEAD origin/master` + `git log -1` + `git diff --name-only <mb> origin/master > $R/m.txt` + `git diff --name-only <mb> HEAD > $R/f.txt` + `comm -12` (无重叠文件)
8. `cat $R/f.txt $R/m.txt; git diff --stat <mb> origin/master -- aria standards` (master 未动 gitlink)

未执行 (只写出): phase1_gate.py --raw-track-id ... --phase B --mode advisory --repo-path /home/dev/Aria (Phase B 入口才调)。

$R = /tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad/runs/r06y
