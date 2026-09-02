---
checkpoint: pre_merge
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T13:41:43.592Z
context: PR #190 linked-issue-field-availability (main 0e9619c / aria fe32441 / standards fad8b4b)
agents: [knowledge-manager]
---

## 审计结论

- [major] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: frontmatter `phase` 字段仍写「C.2 推送/PR 待 owner 授权」且 `updated-at` 停在 `08:26:00Z`, 但同一 PR 的 commit `0e9619c` (`09:18:53Z`) 已把正文 §Status/§7 改为「H1 (a)(b)(c)(d) 四处推送已完成并核验; 剩 PR #190 owner merge」—— 机读锚字段与正文内容不同步 — 证据: `git diff f12647d 0e9619c -- docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md` 显示只改了 `> **Status**:` 行与 §7 提交清单, frontmatter 5 行 (`:1-7`) 零改动; `sed -n '1,10p'` 现状核对 `phase:` 与 `updated-at:` 仍为旧值 (type=issue)
- [minor] documentation/aria/skills/spec-drafter/SKILL.md: 三处写入侧文档 (SKILL.md hunk A `:344` / `standards/openspec/templates/proposal-minimal.md` Usage Note / `.aria/state-checks.yaml:362`) 均教「多个 issue 用 `, ` (逗号+空格) 分隔」, 但 `lib/linked_issue_field.py` 的 E4 (`token_str.split(",")` 后逐元素 `.strip()`) 实测接受任意逗号 (无需跟随空格) 也判 OK —— 文档比库更严格 (不误导, 但非「完全一致」) — 证据: 实跑 `extract_linked_issue_field('# X\n\n> **Linked Issue**: \`10CG/a#1,10CG/b#2\`\n')` → `FieldVerdict(verdict='OK', token_elements=('10CG/a#1', '10CG/b#2'), ...)` (无空格版同样 OK) (type=issue)

## Verdict

Critical: 0 · Major: 1 · Minor: 1 → **PASS_WITH_WARNINGS**

## 投票

**PASS**

理由: 两条 finding 均为文档精度问题, 不影响本 PR 交付的代码/机制正确性 (三处写入侧文档与 lib 实际接受语法逐条核对完全一致, 除分隔符宽松度这一处「库更宽松, 文档更严格」的无害偏差外无矛盾)。major 项 (F1) 是会话 handoff 的 frontmatter 未随正文二次编辑同步刷新, 窗口期短 (merge + phase-d-closer 归档后该 handoff 即被新文档取代), 且正文本身信息完整准确 (只有单独消费 `phase:` 字段而不读正文的场景才会被误导, 未见证据表明现有机制如此消费); 判断不构成「必须在合并前修」的阻塞项, 建议 owner 决定是否在本 PR 或下一次触碰该文件时顺手补一行 frontmatter 更新。

## 核验记录

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 48 tests in 2.072s
OK

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)
EXIT: 0
# 交叉核: find openspec/changes -name proposal.md | wc -l = 9; grandfathered 文件 6 行数据行 (grep -c 不含注释) — 与 proposal :474 声称「9 份作用域, 3 OK + 6 具名在册」逐字一致

$ python3 <emit-arg adversarial fixtures>
case_multi  (`10CG/a#1, 10CG/b#2`)         → OK, emit-arg = "10CG/a#1"
case_na     (`N/A`)                        → BAD_TOKEN, emit-arg = "" (exit 0)
case_tbd    (`TBD`)                        → BAD_TOKEN
case_dash   (`-`)                          → BAD_TOKEN
case_bare_wu (裸 `无`, 无 code span)       → NO_TOKEN
case_link   (markdown 链接形)               → NO_TOKEN
case_alias_field (`> **关联 Issue**:` 字段名 alias) → OK
case_placeholder (`{<org>/<repo>#<n>}`)     → BAD_TOKEN, emit-arg = "" (SC-9(a) 精确复现)
两空格 `>  **Linked Issue**:`               → NO_FIELD (验证「>后恰一个空格」)
全角冒号 `**Linked Issue**：`                → NO_FIELD
单星号 `*Linked Issue*:`                    → NO_FIELD
逗号无空格 `` `10CG/a#1,10CG/b#2` ``        → OK, elements=('10CG/a#1','10CG/b#2') (F2 证据)
全部与 proposal.md SC-4/SC-9/E0-E6 逐条声称一致

# CRLF 一致性 (SKILL.md)
$ git -C aria show HEAD:skills/spec-drafter/SKILL.md | grep -c $'\r$'   # 457
$ git -C aria show HEAD:skills/spec-drafter/SKILL.md | wc -l            # 457  (100% CRLF, 与 d69091d baseline 438/438 同比例)
$ (同法) standards/openspec/templates/proposal-minimal.md: HEAD 63/63 CRLF vs 334c609 baseline 57/57

# 相对链接解析 (SKILL.md hunk A → SOT 模板)
$ cd aria/skills/spec-drafter && realpath -m ../../../standards/openspec/templates/proposal-minimal.md
/home/dev/Aria/standards/openspec/templates/proposal-minimal.md  (存在; 与同文件既有 :448 References 链接同一相对路径, 非新写法)

# 三处写入侧文档互相比对: 字段名拼写 (Linked Issue / 关联 Issue alias-读取侧)、哨兵 (none/无, N/A·TBD·- 全部判非哨兵)、code span 形、", " 分隔 (除 F2 宽松度外) — 三处逐条一致, 无矛盾

# 跨文档声称一致性 (逐项实跑/实读，非转述)
$ forgejo GET /repos/10CG/Aria/pulls/190  → base c423281 / head 0e9619c / mergeable=true; body 逐段核对
$ git ls-tree HEAD aria standards   → fe324414f.. / fad8b4b64.. (与 gitlink bump commit e5947fe 一致)
$ git -C aria ls-remote origin master   → fe32441...  (MATCH)
$ git -C aria ls-remote github master   → fe32441...  (MATCH)
$ git -C standards ls-remote origin/github master → fad8b4b... (MATCH 两端)
$ git -C aria ls-remote origin refs/tags/v1.68.0 → tag object 存在
$ git ls-remote origin/github master (主仓) → c423281...  (MATCH 两端; 与 handoff §7「rebased on 882707f」核实: git merge-base --is-ancestor 882707f c423281 → true)
$ git ls-remote origin feature/linked-issue-field-availability → 0e9619c (MATCH HEAD)
$ forgejo GET /repos/10CG/aria-plugin/issues/117/comments → id 20573 命中, 内容与决策单 B5/PR body 描述一致

$ cd aria/skills/state-scanner/tests && python3 run_tests.py   # 全量
Ran 1457 tests in 78.545s
OK
$ grep -rn "^\s*def test_" --include="*.py" aria/skills/state-scanner/tests/ | wc -l   # 1473 (与 CHANGELOG「1425→1473」现值一致)
$ cd aria && bash skills/run_all_tests.sh
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1889 个测试)   # 与 PR body / CHANGELOG / proposal Status 行「1889」三处一致

$ python3 -c "from lib.collision import normalize_linked_issue; print(normalize_linked_issue('10CG/a#1, 10CG/b#2'))"
('b', 2)   # 与决策单 B3「实测 normalize_linked_issue(...) → ('b', 2)」逐字一致

$ grep -c "phase1_gate" aria/skills/spec-drafter/SKILL.md   # 0，与决策单 B6 一致
$ find aria/skills/audit-engine -iname "*sibling*"   # 空，确认 sibling-spec-probe 尚未落地，TASK-013/015 verification 里对它的 seam 引用是前瞻性记录非当前断链

# Spec 三文件自洽
$ grep -c '^\s*- \[x\]' / '- \[ \]' tasks.md   → 24 / 1
$ python3 -c "yaml Counter(status)"            → {'done': 24, 'in_progress': 1}
metadata.status 文案 / proposal.md Status 行 (:5) 均写「24/25」「TASK-025 in_progress」—— 四处一致

# TASK-005 parents[4] 勘正
$ grep -n "parents\[" aria/skills/state-scanner/tests/test_linked_issue_field.py   → :85 _MAIN_REPO_ROOT = parents[4]
$ grep -n "parents\[4\]" test_architecture.py:311 / test_spec_complete.py:94       → 均命中，与 yaml TASK-005 verification 注 + 决策单 B1 引用行号逐字一致
$ python3 -c "Path(test_file).resolve().parents[4]"  → /home/dev/Aria (正确解析主仓根)

# CLAUDE.md 卫生 (本 PR diff 只 2 行版本串)
$ git diff c423281 HEAD -- CLAUDE.md   → 仅 :139 / :141 两行版本号变更
$ wc -l / wc -c CLAUDE.md   → 151 行 / 13139 字节 (< 200 / < 24000)
$ 实跑 claude-md-changelog-free 检查体 (ROLL/LINES/BYTES 三判据)   → OK (no rolling changelog; 151 lines, 13139 bytes)

# i18n 三份 README
$ git diff c423281 HEAD -- README.zh.md README.ja.md README.ko.md --stat  → 各 6 行 (3+/3-)
$ 逐份 diff 内容核对：仅 translated-from 标记 + badge + Plugin Version 三点，无正文改动
$ 实跑 i18n-readme-translation-currency 检查体 → OK (3 i18n READMEs current @ 1.68.0)
$ 实跑 m6-version-badge-match / main-project-version-consistency / m6-claude-md-version 三条 check 体 → 全部 OK (main-project-version-consistency: "主项目版本 1.7.5 — 9 个引用点全部一致")

# 审计轨 / 决策单 append-only
$ git diff origin/master...HEAD -- .aria/audit-reports/linked-issue-field-availability-audit-trail.md | grep -E '^-[^-]'   → 空 (纯追加, 起点 :95 之后)
$ git diff origin/master...HEAD -- '.aria/decisions/2026-09-01-...md' --stat   → 1 file changed, 12 insertions(+)  (纯追加)

# .aria/state-checks.yaml 新条目
$ grep -c '^  - name:' .aria/state-checks.yaml   → 13 (与 TASK-011 verification「== 13」一致)
条目仅用 name/description/command/severity/fix/timeout_seconds/enabled 既有 7 键，零新键

# handoff frontmatter 5 字段 + latest.md 联动
$ sed -n '1,10p' docs/handoff/2026-09-02-*.md   → track-id/owner-container/phase/status/updated-at 五字段齐全
$ git diff c423281 HEAD -- docs/handoff/latest.md   → pointer 行 + track 表该行 + 追加一段「2026-09-02 更新」段落，格式与既有全部历史条目 (08-16 至 08-31, 十余条) 完全同构
```

**latest.md「History」机制说明 (非 finding, 澄清)**: `aria/skills/phase-d-closer/references/handoff-mechanics.md` §latest.md 维护 子步骤 1 规定的格式是 `- {date HH:MM} — [{name}](./{filename}) ({scope-note} — {summary})` 的 bullet 列表, 但本仓 `docs/handoff/latest.md` 全部历史 (可追溯至 08-16, 与本 PR 无关) 走的是「pointer 行 + track 表 + 逐次追加的 `> **{date} 更新** (...)` 散文段」惯例, 从未采用文档规定的 bullet 格式。这是**先于本 PR 存在的既定惯例**, 非本 PR 引入的偏离; 本 PR 的 d58c439 commit 严格按该既定惯例新增了一段 (pointer 更新 + track 表行更新 + 一段「2026-09-02 更新」, 且文中显式写明「08-31 那份 handoff 由本份接替 Latest」以替代 sub-step 2 的「前一 Latest 标记」义务), 内部自洽、与既往条目同构。是否要把 `handoff-mechanics.md` 的 SOT 描述改成反映实际惯例, 或反过来让 latest.md 改用文档格式, 属于另一件与本 PR 无关的 Level 1 change, 未计入本报告 finding 计数。
