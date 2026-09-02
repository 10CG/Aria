---
checkpoint: pre_merge
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS
timestamp: 2026-09-02T17:57:38.000Z
context: PR #190 linked-issue-field-availability (main 0db60cc / aria d1caa66 / standards ffed204)
agents: [knowledge-manager]
---

## 审计结论

- [minor] testing/.aria/repro/handoff-current-state-scan.py: R4 入库的「派生文档陈旧扫描器」白名单 (`HIST_OK`) 按**整行**匹配而非围绕命中 `STALE` token 的局部上下文匹配, 对抗测试证明: 当一条真正陈旧的轮次声称与任意无关的常见白名单词 (`已完成`/`已推`/`前一` 等) 出现在**同一行**, 该行会被错误判定为「历史记述」而放行, 即便 `STALE` 部分本身是假的。三条合成对抗输入全部被吞: `"H1 四处推送已完成; PR #190 pre_merge 收敛审计 R3/R4 稳定性确认后合并"` (含 R4 major a3bfd693 原文的失效措辞) / `"推送授权已于同日给出, R1/R2 已清账 剩 R3/R4 待跑"` / `"H1 (a)-(d) 已完成, R4 稳定性确认"` —— 三例均 `MISSED`。**当前被审文档本身未受影响** (见下方核验记录, `residual=0` 且我逐份人工复读 handoff/latest.md/proposal/yaml/PR body 无遗漏), 故非当前状态缺陷; 但该扫描器正是 R4 专为「杜绝 a3bfd693 第 5 次复发」新写的机械宿主, 其检测能力存在可证伪的方向性漏洞 (memory `invariant-dimension` / `adversarial-fixture`: 验断言要验拒绝能力非当前取值), R4 聚合报告仅报告了「正例 (真实文档) 扫描 residual=0」, 未做坏输入三态验证 (memory `check-runs-at-baseline-first`) — 证据: 见下方核验记录 §1 逐字 python3 会话输出 (type=issue) finding_id=d711ce91
- [minor] documentation/VERSION: 主仓 `VERSION` 文件「子模块版本」表 `:24` 写 `standards | v2.2.3`, 但 `standards/openspec/project.md` 自身头部 `:3` 写 `> **Version**: 2.2.2` —— 两处都自称是「standards 当前版本」的唯一来源却互不一致。**非本 PR 引入**: `git diff c423281 0db60cc -- VERSION` 只改了 aria 那一行 (`v1.67.2`→`v1.68.1`), standards 行两端均为 `v2.2.3`; `standards/openspec/project.md` 的 `2.2.2` 由更早的 `9df1722`(与本 Spec 无关)写入, `ffed204` (本 PR 唯一 standards 侧改动) 只碰了 `templates/proposal-minimal.md` 2 行, 未触碰 `project.md`。与决策单 B4/handoff M3 (「`version-management.md:254` 声称的 standards 独立 tag 版本方案与仓实况不符」) 相关但**不是同一条事实** —— M3 讲的是「文档措辞暗示存在不存在的版本化机制」, 本条讲的是「两份都存在、都在正常更新的文件, 数字本身对不上」, 记为该漂移面的第二个具体实例, 建议归入 M3 同批下次触碰时一并勘正, 不阻塞本 PR 合并 — 证据: `sed -n '3p' standards/openspec/project.md` = `> **Version**: 2.2.2` vs `sed -n '24p' VERSION` = `| standards | v2.2.3 | ...` (type=issue) finding_id=e11b8aa8

## Verdict

Critical: 0 · Major: 0 · Minor: 2 → **PASS**

## 投票

**PASS**

- `d711ce91` (扫描器白名单过宽) — **不阻塞合并** (否): 当前被审 PR 的实际文档内容已逐份人工 + 机械核验零残余; 该发现指向的是「未来某次编辑可能不被扫描器抓到」的工具健壮性缺口, 不是本 PR 交付物里存在的缺陷。建议随 aria v1.68.2 候选或 `.aria/repro/` 下一次触碰时把 `HIST_OK` 改为围绕 `STALE` 命中位置的局部窗口匹配 (而非整行), 并补 3 条对抗测试固化本次发现的三个反例。
- `e11b8aa8` (VERSION vs project.md 版本号不一致) — **不阻塞合并** (否): 确认为本 PR 提交范围之外的既存漂移 (两处均未被 `c423281..0db60cc` 任何一个 commit 触碰), 与已裁定的 B4/M3 carry-forward 同类, 按同一先例处置 (carry, 下次触碰同批勘正)。

综合: 0 Critical / 0 Major, 无一条「必须在合并前修」的 finding; 我的一票投 **PASS**。

## 核验记录

```
# --- 前置强制命令 ---
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 3.580s
OK

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt; echo EXIT=$?
OK (9 份在范围内, 6 条在册)
EXIT=0

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c | head -3
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4

# --- 现状锚点 (与 R5 简报一致) ---
$ git rev-parse HEAD; git -C aria rev-parse HEAD; git -C standards rev-parse HEAD; git status --short
0db60ccfc21c84835e6a84ae2d6b9afe6e9db045
d1caa66cb375c2799f55def453ca232c66a18c22
ffed2040dff7964cf9d137e85e174173d2c685b9
 M aria-orchestrator   # 有意停泊, 非本 PR scope

# --- §1 R4 类级修法 (a3bfd693 ×4 → 指针口径 + 扫描器) 核验 ---
## 1a. 扫描器官方跑法 (与 R4 聚合报告贴的命令逐字一致)
$ python3 .aria/repro/handoff-current-state-scan.py docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md --pr 190 --extra docs/handoff/latest.md openspec/changes/linked-issue-field-availability/tasks.md openspec/changes/linked-issue-field-availability/detailed-tasks.yaml openspec/changes/linked-issue-field-availability/proposal.md
residual = 0
$ echo $?
0

## 1b. 独立人工复读 (不依赖扫描器的自证): handoff 全文 grep 'R1|R2|R3|R4|轮次|aggregated' 逐行读, latest.md / proposal.md / tasks.md / yaml / PR body 逐份读 —
## 结论: 全部剩余 R1-R4 字面提及均为「某轮某席发现了什么」型历史归因 (如「R1 tech-lead 抓出」「R3 code-reviewer」「决策单 …R1 B8/B9…R3 C8–C9」), 无一处断言「当前只完成到 R_n, 后续待跑」这一 a3bfd693 的原始形态; PR body 保留 R1/R2/R3 三段完整历史叙述 + 一句「后续轮次: 轮次与结果以…最新一份为准」指针, 同一模式。

## 1c. 扫描器本身对抗测试 (白名单是否过宽 — R5 简报明确要求项)
$ python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("scan", ".aria/repro/handoff-current-state-scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bad_cases = [
    "PR #190 pre_merge 收敛审计 R1/R2 已清账, R3/R4 稳定性确认后合并",
    "还有 22/25 未推",
    "推送授权尚未给出",
    "state-scanner Ran 1457 tests",
    "aria v1.68.0 fe32441 是最新版本",
]
for t in bad_cases:
    print("CAUGHT" if m.scan_text("synthetic", t) else "MISSED", "->", t)
EOF
CAUGHT -> PR #190 pre_merge 收敛审计 R1/R2 已清账, R3/R4 稳定性确认后合并
CAUGHT -> 还有 22/25 未推
CAUGHT -> 推送授权尚未给出
CAUGHT -> state-scanner Ran 1457 tests
CAUGHT -> aria v1.68.0 fe32441 是最新版本
# 单独出现时全部命中 — 基本判据成立

$ python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("scan", ".aria/repro/handoff-current-state-scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
tricky = [
    "H1 四处推送已完成; PR #190 pre_merge 收敛审计 R3/R4 稳定性确认后合并",
    "推送授权已于同日给出, R1/R2 已清账 剩 R3/R4 待跑",
    "H1 (a)-(d) 已完成, R4 稳定性确认",
]
for t in tricky:
    print("CAUGHT" if m.scan_text("synthetic", t) else "MISSED(whitelist swallowed it)", "->", t)
EOF
MISSED(whitelist swallowed it) -> H1 四处推送已完成; PR #190 pre_merge 收敛审计 R3/R4 稳定性确认后合并
MISSED(whitelist swallowed it) -> 推送授权已于同日给出, R1/R2 已清账 剩 R3/R4 待跑
MISSED(whitelist swallowed it) -> H1 (a)-(d) 已完成, R4 稳定性确认
# 与 STALE token 同行的无关 HIST_OK 词 (已完成/已推) 会整行免检 ⇒ finding d711ce91

# --- §2 三仓事实交叉核验 (版本 / SHA / 测试计数 / task 计数 / #117 comment / PR 状态) ---
$ cd aria/skills/state-scanner/tests && timeout 60 python3 run_tests.py test_linked_issue_field 2>&1 | tail -5
Ran 53 tests in 3.580s
OK
$ python3 run_tests.py 2>&1 | grep -E '^Ran|^OK$'   # 全量, 后台跑完
Ran 1462 tests in 119.342s
OK
$ grep -rc "^\s*def test_" aria/skills/state-scanner/tests/*.py | awk -F: '{s+=$2} END{print s}'
1478
$ cd aria && bash skills/run_all_tests.sh 2>&1 | tail -3
state-scanner                                  OK (1462 tests)
tdd-enforcer/examples/python                   OK (14 tests)
workflow-runner                                OK (38 tests)
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1894 个测试)
# 53 / 1462 / 1478 / 1894 四个数字全部自己实跑复现, 与 aria/CHANGELOG.md ## [1.68.1] 段 / tasks.md :5 / PR #190 body 逐字一致

$ grep -cE '^\s*- \[x\]' openspec/changes/linked-issue-field-availability/tasks.md; grep -cE '^\s*- \[ \]' openspec/changes/linked-issue-field-availability/tasks.md
24
1
$ python3 -c "
import yaml
from collections import Counter
d = yaml.safe_load(open('openspec/changes/linked-issue-field-availability/detailed-tasks.yaml'))
print(Counter(t.get('status') for t in d.get('tasks', [])))"
Counter({'done': 24, 'in_progress': 1})
# 24/25 (tasks.md checkbox) 与 yaml status 计数一致

$ python3 -c "
data = open('standards/openspec/templates/proposal-minimal.md','rb').read()
print('CRLF:', data.count(b'\r\n'), 'LF-only:', data.count(b'\n') - data.count(b'\r\n'))"
CRLF: 63 LF-only: 0
# CRLF 63/63, R1 以来未变

$ forgejo GET /repos/10CG/aria-plugin/issues/117/comments  # (JSON 保存后 python3 过滤 id==20573)
FOUND id=20573, created= 2026-09-02T08:18:45Z
内容首行: "第二实例 (Aria Spec `linked-issue-field-availability`, aria-plugin v1.68.0 ship 批, 2026-09-02)" — 与决策单 B5 / handoff §7「Issue 动作: aria-plugin#117 comment 20573 (已回读核验)」一致

$ forgejo GET /repos/10CG/Aria/pulls/190  # (JSON 保存后 python3 解析)
TITLE: feat(state-scanner/spec-drafter): linked-issue-field-availability — proposal.md「Linked Issue」字段可得性 (aria-plugin v1.68.0 → v1.68.1 + standards 模板 + check 注册)
STATE: open MERGED: False
HEAD SHA: 0db60ccfc21c84835e6a84ae2d6b9afe6e9db045   # 与本仓 HEAD 一致
BASE SHA: c423281a9b1e5d04ebf62bd3132cc63eecd366f1
BODY 末段「R3 (fresh 四席): 0C / 1M / 4m」— 与 R3 聚合报告 Verdict「0 Critical / 1 Major / 4 Minor」逐字一致 (R4 knowledge-manager 曾发现的「5m」错误已被 R4 clean-up 改正)

# --- §3 版本账本交叉核验 (发现 finding e11b8aa8) ---
$ grep -m1 '"version"' aria/.claude-plugin/plugin.json
  "version": "1.68.1",
$ git ls-tree HEAD aria | awk '{print $3}'; git ls-tree HEAD standards | awk '{print $3}'
d1caa66cb375c2799f55def453ca232c66a18c22
ffed2040dff7964cf9d137e85e174173d2c685b9
$ grep -n '1\.68\.1' CLAUDE.md README.md README.zh.md README.ja.md README.ko.md VERSION
CLAUDE.md:139/141; README.md:8/242; README.zh.md:10/244 (+ :3 translated-from); README.ja.md 同构; README.ko.md 同构; VERSION:子模块表 aria 行
# 5 处同步面全部对齐 1.68.1 (README×4 各 2 处 + translated-from ×3, CLAUDE.md ×2, VERSION ×1)

$ sed -n '3p' standards/openspec/project.md
> **Version**: 2.2.2
$ sed -n '24p' VERSION
| standards | v2.2.3 | https://github.com/10CG/aria-standards |
# 不一致 (finding e11b8aa8)

$ git diff c423281 0db60cc -- VERSION
-| aria (插件) | v1.67.2 | https://github.com/10CG/aria-plugin |
+| aria (插件) | v1.68.1 | https://github.com/10CG/aria-plugin |
 | standards | v2.2.3 | https://github.com/10CG/aria-standards |   # 本 PR 未改这行
$ cd standards && git log --oneline -3 -- openspec/project.md
9df1722 docs(openspec): project.md 2.2.2 — 「完成的真实性」补运行时证据可选维度   # 与本 Spec 无关的更早提交
$ git show --stat 334c609..ffed204 | head -8   # standards 本 PR 唯一改动范围
 openspec/templates/proposal-minimal.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
# project.md 未被 ffed204 触碰 ⇒ e11b8aa8 确系本 PR 之外的既存漂移, 非新引入

# --- §4 写入侧三处 (SOT 模板英文化 / spec-drafter hunk A+B / state-checks fix 文案) vs lib/probe 行为逐条对照 ---
$ sed -n '55,60p' standards/openspec/templates/proposal-minimal.md
**Linked Issue header line (required for Level 2 / Level 3)**:
- Value is an inline code span ... several issues go in the same code span separated by `, `
- No related issue (verified): write exactly `none` ...
- Extraction rules (E0–E6) ... always write the English canonical field name and sentinel exactly as shown above
$ sed -n '341,351p' aria/skills/spec-drafter/SKILL.md | grep -n 'Linked Issue\|逐行对齐\|关联 Issue'
341: ... 必须含一行 `Linked Issue` 字段, 与 SOT 模板 … 头部逐行对齐 …   # B8 裁定: 顺序条款措辞软化延后 (处方性, 待 Rule #6 批次), 本轮不动, 符合裁定, 非新 finding
351: ... 读取侧另认中文 alias `关联 Issue` / `无`, 但新写一律用英文 canonical。
$ grep -n '位置不限\|裸逗号亦被 E4 接受' .aria/state-checks.yaml
362: 探针按 E0 取文档序第一条 depth-1 命中, 与行号无关 …
363: … 多个用 ", " 分隔 (裸逗号亦被 E4 接受, 推荐带空格) …
$ sed -n '10,30p' aria/skills/state-scanner/lib/linked_issue_field.py | grep -n 'first matching line\|document order'
21: (3) first matching line in document order wins.
$ sed -n '147p' aria/skills/state-scanner/lib/linked_issue_field.py
    token_elements = tuple(e.strip() for e in token_str.split(","))  # E4
# split(",") 后逐元素 strip() ⇒ 裸逗号与 ", " 均合法, 与 check fix 文案「裸逗号亦被接受」逐字对照一致; E0 「文档序第一条」与 fix 文案「与行号无关」一致
$ python3 -c "
import sys; sys.path.insert(0, 'aria/skills/state-scanner')
from lib.collision import normalize_linked_issue
print(normalize_linked_issue('10CG/a#1, 10CG/b#2'))"
('b', 2)
# 独立复算 B3 理据勘正引用的实测值, 与决策单 B3 行逐字一致

# --- §5 CLAUDE.md 卫生 + i18n ---
$ wc -l CLAUDE.md
151 CLAUDE.md
$ sed -n '/^## 项目状态/,/^---$/p' CLAUDE.md | sed -n '/```/,/```/p' | wc -l
13   # 代码块含首尾栏共 13 行 (内容 11 行), 15-20 行预算内, 与 R4 一致未变
$ sed -n '/^## 项目状态/,/^---$/p' CLAUDE.md | grep -inE 'SC-[0-9]|E0-E6|E0–E6|finding_id|hunk [AB]'
# 空 — 无 skill 设计术语泄漏

# --- §6 append-only 核验 (R1-R4 报告 + 决策单 + 审计轨未被改写) ---
$ git diff 265a5f9 0db60cc -- .aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md | grep -nE '^-[^-]'
# 空 — 纯追加 (3b277328 / C9-补 / 记录 三行均为新增, 未删旧文本)
$ git diff c423281 0db60cc -- .aria/audit-reports/linked-issue-field-availability-audit-trail.md | grep -nE '^-[^-]'
# 空
$ for f in .aria/audit-reports/pre_merge-R{1,2,3,4}-*-linked-issue-field-availability-{aggregated,code-reviewer,knowledge-manager,qa-engineer,tech-lead}.md; do n=$(git log --oneline -- "$f" | wc -l); [ "$n" != "1" ] && echo "ANOMALY: $f: $n"; done
# 无输出 — 20 份报告各恰 1 commit

# --- §7 H1b 呈 owner 措辞完整性核验 (memory narrow-owner-options) ---
$ sed -n '255,284p' aria/skills/audit-engine/SKILL.md
## 降级策略
当 max_rounds 耗尽且未收敛:
1. 展示摘要 ...
2. 三路径选择 (AskUserQuestion):
   [1] 接受当前结论 → converged: false, overridden_by_user: true → 继续后续流程
   [2] 增加轮次 → max_rounds += 2 → 继续审计循环
   [3] 降级为单轮 → 取最后轮结论作为最终结果 → converged: false, degraded: true
$ grep -n 'H1b' docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md
57: ... ⇒ **降级策略由 owner 选**: [1] 接受当前结论 override 合并 / [2] 加轮 / [3] 降级单轮 | 一句话 | 决策单 R4 行
# 三选项逐一对照 SOT `references` 无遗漏无添加无隐性倾向措辞; H1b 未预设推荐, 中立列出
```
