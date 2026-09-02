---
checkpoint: pre_merge
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T16:19:24.000Z
context: PR #190 linked-issue-field-availability (main 17ae85e / aria d1caa66 / standards ffed204)
agents: [knowledge-manager]
---

## 审计结论

- [major] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: R1 对 finding `a3bfd693` 的清账**不完整** —— 只刷新了 frontmatter `phase:`/`updated-at:` 与顶部 `> **Status**:`/§7, 但同一文档 §2 H1 行 (`:56`) 与 §6 入口第 1 条 (`:126`) **仍描述 H1 为待办**: `:56` 写「推送授权 (四处, 全部外向): (a) aria master `fe32441` + tag `v1.68.0` 双推… (c) 主仓 feature 分支推 origin → TASK-025 PR」, `:126` 写「拿 owner 推送授权后按序执行 H1 (a)→(b)→(c)→(d) … → 主仓 feature 推 + TASK-025 PR … → owner `/plugin update` 刷到 1.68.0」——而顶部 `> **Status**:` 已明写「H1 (a)(b)(c)(d) 四处推送已完成并核验 (2026-09-02 owner 授权); 剩 PR #190 owner merge」, PR #190 确实已存在且 open (head 17ae85e)。同一文档四处 (frontmatter / Status / §2 / §6) 对「H1 是否完成」给出两种矛盾陈述, 且 §6 目标版本仍写 1.68.0 (现网 1.68.1) —— 证据: `sed -n '56p;126p' docs/handoff/….md` 与 `sed -n '9,10p'` (Status 行) 逐字比对 (type=issue) finding_id=a3bfd693
- [minor] documentation/aria/skills/spec-drafter/SKILL.md: R1 (knowledge-manager 自己) 原始 raw 16 条 finding 之一 (「三处写入侧文档教 `, ` 逗号+空格分隔, lib E4 实测接受裸逗号无空格」) 在 R1 聚合报告去重 16→12 时被**静默丢弃**, 未出现在 12 条清账表任何一行、也未获任何处置记录 (非 carry-forward / 非「记入口径注」/ 非「接受」)。当前状态复核: 三处写入侧文档 (`standards/openspec/templates/proposal-minimal.md:56`「separated by `, `」/ `aria/skills/spec-drafter/SKILL.md:349`「用 `, ` 分隔」/ `.aria/state-checks.yaml:363`「多个用 ", " 分隔」) 仍逐字写「, 」为分隔符, `lib/linked_issue_field.py:147` E4 (`token_str.split(",")` 逐元素 `.strip()`) 实测对裸逗号同样判 OK —— 文档比库更严格 (不误导使用者、不产生假阴性/假阳性), 不阻塞合并, 但作为独立 finding 应在聚合表里有一行处置记录而非消失 — 证据: 实跑 `extract_linked_issue_field('# X\n\n> **Linked Issue**: \`10CG/a#1,10CG/b#2\`\n')` → verdict='OK', token_elements=('10CG/a#1','10CG/b#2') (本轮核验记录 §3); R1 聚合报告 `grep -c '5da757d0\|逗号\|separated'` 全 0 命中 (type=issue) finding_id=5da757d0

## Verdict

Critical: 0 · Major: 1 · Minor: 1 → **PASS_WITH_WARNINGS**

## 投票

**PASS**

理由: 两条 finding 均非「必须在合并前修」。major 项 (handoff §2/§6 残留矛盾) 是会话交接文档的内部不同步, 与 a3bfd693 原判同理: 窗口期短 (PR #190 merge 后 phase-d-closer 归档该 Spec 时该 handoff 即被新文档取代), 且顶部 frontmatter + Status 已给出准确入口 (「新 session 优先读 §0」指向的读者会先看到已刷新的 Status, 不会被 §2/§6 的残留旧文本误导到重新走一遍推送授权流程的低概率场景可通过下次触碰同批清); 不影响本 PR 交付的代码/机制正确性。minor 项是文档比代码更严格的无害偏差 (不产生误判), 唯一值得记录的是聚合流程本身丢了一条 finding 未处置 —— 但该条内容本身依然只是文档精度问题, 不构成阻塞。

## 核验记录

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 2.029s
OK

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt; echo EXIT=$?
OK (9 份在范围内, 6 条在册)
EXIT=0

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c | head -5
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4
0000015

# --- §1 R1 disposition 逐条核验 (已修确认, 不再列 finding) ---

R1-e4cde200 (qa major, SC-5(d) 夹具误述) 已修, 核验: test_linked_issue_field.py 现 53 条 (原 48), 全绿; CHANGELOG 1.68.1 逐字描述同一修复。

R1-9ac5533a (tech-lead major, SKILL.md 顺序条款无机械宿主) 已由决策单 B8 裁定 (设计而非缺陷) 并落地, 核验:
$ python3 -c "
import sys; sys.path.insert(0, 'aria/skills/state-scanner')
from lib.linked_issue_field import extract_linked_issue_field
lines = ['# Proposal'] + [f'> continuation blockquote filler line {i}' for i in range(2, 61)]
lines.append('> **关联 Issue**: \`10CG/aria-plugin#137\`')
text = '\n'.join(lines) + '\n'
fv = extract_linked_issue_field(text)
print(fv.verdict, fv.line_no, fv.token_str)
"
OK 61 10CG/aria-plugin#137   # 位置无关证据成立, D2 判据属实
$ grep -n "位置不限" .aria/linked-issue-field-grandfathered.txt .aria/state-checks.yaml
  两处均含 "位置不限 — 探针按 E0 取文档序第一条 depth-1 命中, 与行号无关" (白名单头注 + fix 文案已按 B8 补齐)
$ grep -n "必须.*对齐" aria/skills/spec-drafter/SKILL.md
  341: "必须含一行 Linked Issue 字段, 与 SOT 模板头部逐行对齐" — 措辞确未软化 (B8: 延后, Rule #6 门槛未过), 与裁定一致, 无矛盾

R1-ac44ace3 (tech-lead major, arch 文档漂移) 已修 + 类级兜底, 核验:
$ PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
  A=$(grep -m1 -oP '^\| aria-plugin \| v\K[0-9.]+' docs/architecture/system-architecture.md)
  B=$(grep -m1 -oP '^\| \*\*aria-plugin\*\* \|[^|]*\| v\K[0-9.]+' docs/architecture/version-scheme.md)
  echo $PLUGIN $A $B
1.68.1 1.68.1 1.68.1   # 三处一致
新 check plugin-version-arch-docs-match 三态实测 (本机独立复现, 非引用):
  - OK 态: 三值一致 → "OK plugin=1.68.1 (2 arch doc rows match)" exit 0
  - DRIFT 态 (手工把 system-architecture.md 改回 v1.68.0): "DRIFT plugin=1.68.1 vs system-architecture.md=1.68.0" exit 1
  - SKIP 态 (删 plugin.json): "##SKIP## aria/.claude-plugin/plugin.json 不可读" exit 0
  17ae85e 对这两文件的实际 diff (29c1e4f..17ae85e) 仅各一行版本号变更, 与决策单「两行」描述吻合 (128 行的更大改动来自合并 c423281 的架构文档 2.0.1 复审, 非本轮引入)

R1-ae4f1c9f / R1-2ed89c8a / R1-a0ff4897 (code-reviewer minor ×3) 已修, 核验: TestSC5ProbeHardening 5 条测试 (归一/去重/UNREADABLE/root+--emit-arg互斥/ascii stdout) 全部包含在上方 53 条全绿结果内; 白名单文件 6 条实测均已归一 (无尾斜杠/无 ./ 前缀/无重复)。

R1-4605dc4d (code-reviewer minor, 模板 CJK) 已修, 核验: standards/openspec/templates/proposal-minimal.md 现全英文 Usage Note, 无中文 alias 提及; CRLF 保持——
$ total=$(git -C standards show HEAD:openspec/templates/proposal-minimal.md | wc -l)
  crlf=$(git -C standards show HEAD:openspec/templates/proposal-minimal.md | grep -c $'\r$')
  echo total=$total crlf=$crlf
total=63 crlf=63   # 全文件 CRLF, 无破坏

R1-6cdc6077 (qa minor, 1457 vs 1473 计数差 16) 已记入口径注, 核验: CHANGELOG 1.68.1 与 SUBSTITUTE.md 均含「差 16 = test_collision.py 16 个 pytest 风格裸函数不被 unittest 收集」同一措辞; 本轮实跑 run_tests.py (无过滤) Ran=1462, 静态 def test_ 计数=1478, 差值仍为 16 (裸函数数量未变, 口径一致):
$ cd aria/skills/state-scanner/tests && python3 run_tests.py 2>&1 | grep "^Ran"
Ran 1462 tests in 66.972s
$ grep -rE "^\s*def test_" ../tests/*.py | wc -l   # (aria/skills/state-scanner 根下)
1478

R1-46b1df1a / R1-5333fe78 / R1-6ab01600: carry-forward / 接受, 决策单 C1–C3 逐条留痕, 未见反证, 不重报。

# --- §2 CLAUDE.md 卫生复核 ---
$ wc -l CLAUDE.md; wc -c CLAUDE.md
151 CLAUDE.md
13316 CLAUDE.md
$ ROLL=$(grep -cE '^> 前次|^\*\*更新\*\*:|^\*\*最近更新\*\*:' CLAUDE.md); echo $ROLL
0
# 全部达标 (≤200 行 / ≤24000 字节 / 无滚动 changelog); state-check claude-md-changelog-free 会 OK
$ git diff 0e9619c 17ae85e -- CLAUDE.md
# 仅两处: 发布同步面一行扩写 (+arch 两文档 +新 check 名) / 「项目状态」段版本号 1.68.0→1.68.1 ×2; 无 skill 设计术语流入 (#116)

# --- §3 跨文档一致性抽样核验 (数字/SHA/版本) ---
CHANGELOG aria/CHANGELOG.md [1.68.1]: "48 → 53"/"Ran 1462"/"静态 …1473 → 1478" — 逐字与本轮实跑一致 (见上)。
aria VERSION 两行账本: 1.68.1 (当前) + 1.68.0 (旧), 摘要数字与 CHANGELOG 逐字同源。
主仓 CLAUDE.md / VERSION / README.md(badge+Plugin Version) / README.{zh,ko,ja}.md(各 3 点) 全部 = 1.68.1, 逐一 grep 核对; i18n 三份 diff (0e9619c..17ae85e) 各自恰好 3 处改动 (translated-from / badge / Plugin Version), 无正文改动 (#140 B 档合规)。
PR #190 body (`forgejo GET /repos/10CG/Aria/pulls/190`): head=17ae85e, base=c423281a9b, mergeable=true; body 末尾含「## pre_merge 收敛审计」段, 逐字描述 R1 清账后的 aria d1caa66/v1.68.1、standards ffed204、「gitlink → aria d1caa66 / standards ffed204; 14 点 → 1.68.1」, 与当前状态一致 (初读前 3000 字符只看到「本 PR 携带」段的历史叙述 fe32441/fad8b4b, 完整读到 4193 字节后确认末段已更新, 不构成 finding)。
决策单 §B 期 B1–B7 + B8/B9 + C1–C3: 逐条核对判据可证伪点 (parents[4] / 位置无关测试 / arch 两行 diff / 14 点计数与 commit message 措辞一致, 非矛盾) 均属实, B8/B9 裁定站得住。
proposal.md:3 / tasks.md:5,80,81 的 Status 行仍写 aria `fe32441`(v1.68.0)/standards `fad8b4b` (B.2 完成时的快照), 未随 R1 清账更新到 d1caa66/ffed204/v1.68.1 —— 判断: tasks.md 5.6 (主仓 PR) 仍为 `[ ]` 未完成态, 此二文件预期在 5.6 完成 + phase-d-closer 归档前最后一次编辑时统一勘正, 本轮不单独立 finding (与 handoff 的差异在于: handoff 顶部已自称「完成」而细节段矛盾, Spec 文件顶部与细节都还没更新到「完成」, 内部不矛盾, 只是滞后)。

# --- §4 append-only / R1 报告不可变性核验 ---
$ git diff origin/master...HEAD -- .aria/audit-reports/linked-issue-field-availability-audit-trail.md | grep -E '^[+-]' | grep -v '^+++|^---' | cut -c1 | sort | uniq -c
     47 +
$ git diff origin/master...HEAD -- ".aria/decisions/2026-09-01-*.md" | grep -E '^[+-]' | grep -v '^+++|^---' | cut -c1 | sort | uniq -c
     22 +
# 两文件均 100% 追加, 零删改
$ git log --oneline -- ".aria/audit-reports/pre_merge-R1-2026-09-02T131710-919Z-linked-issue-field-availability-{aggregated,code-reviewer,knowledge-manager,qa-engineer,tech-lead}.md"
# 5 份均只有一次提交 (17ae85e), 未被二次改动

# --- §5 latest.md / handoff-mechanics ---
docs/handoff/latest.md 仍指向本 session 收尾时的 2026-09-02 handoff 且未反映 R1 清账/PR open 状态; 依 standards/conventions/session-handoff.md §1.3+§2.1, latest.md pointer 只由 phase-d-closer / session-closer 两个正交收尾入口写入, pre_merge 审计属周期内检查点非收尾事件 ⇒ 保持不动是**预期行为**, 不构成 finding (PR body 已注明 merge 后 phase-d-closer 归档该 Spec, latest.md 届时随之更新)。

# --- §6 对抗性核验 (坏输入/边界) ---
$ mkdir -p /tmp/probetest/openspec/changes/foo && printf '# Foo\nno field here\n' > /tmp/probetest/openspec/changes/foo/proposal.md
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py /tmp/probetest --grandfathered /tmp/probetest/.aria/does-not-exist.txt; echo EXIT=$?
FAIL 1 项
openspec/changes/foo/proposal.md:- NO_FIELD 缺字段行 (E0 三谓词无命中)
(白名单文件缺失, 视为空集)
EXIT=1
# 白名单文件不存在 (非空文件, 是路径本身缺失) 仍 fail-CLOSED 视为空集, 与文档声明一致, 非静默放行
```
