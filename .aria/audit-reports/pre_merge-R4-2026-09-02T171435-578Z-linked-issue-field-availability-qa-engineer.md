---
checkpoint: pre_merge
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T17:31:24.000Z
context: PR #190 linked-issue-field-availability (main 265a5f9 / aria d1caa66 / standards ffed204)
agents: [qa-engineer]
---

# PR #190 pre_merge 收敛审计 — Round 4 (稳定性确认轮) — qa-engineer (fresh 席)

> 镜头: 测试与证据真实性。方法论: 先读 R1/R2/R3 三份聚合报告 (未读各席个人报告) 建立处置期望, 再独立重跑核心命令 + 对抗性验证, 最后逐行核对 R3 声称的「机械扫描残余=0」— 该核对**推翻了这项声称**, 是本轮主发现。

## 审计结论

- [major] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: R3 对 `a3bfd693` 的「改类 + 机械扫描残余=0」声称**不成立, 第四轮同形残余** —— 同一份文档内, 三处仍写「R1/R2 已清账, R3/R4 稳定性确认」/「R3 (+R4 稳定性确认) → 合并」, 与同文件内已正确的「R1-R3 已清账, R4 确认」矛盾。证据: `:4`(frontmatter phase) = `R1 0C/4M、R2 0C/2M、R3 0C/1M 已清账, R4 稳定性确认` (正确) vs `:14`(Status 字段) = `R1/R2 已清账, R3/R4 稳定性确认后按 owner 指令合并` (**错**, 遗漏 R3) vs `:126`(§6 下一步) = `R1/R2 已清账, **R3 (+R4 稳定性确认) → 合并**` (**错**, 把已完成的 R3 与未开始的 R4 并列成「都待确认」) vs `:152`/`:178`(footer) = `R1–R3 清账、R4 稳定性确认` (正确)。四处同一事实, 三种取值 (`R1-R2` / `R1-R3` / `R3 待定`), 同一份 canonical handoff 内自相矛盾。逐字核对 `git diff fdfb183 265a5f9 -- docs/handoff/...` 确认 R3 commit 未触碰 `:11`/`:14`/`:126` 三处 (只改了 `:4`/`:12`/`:108`/`:113`/`:116`/`:136-137`/`:152`/`:178`); R3 聚合报告 (`pre_merge-R3-...-aggregated.md:28`) 逐字列出「三条人工判为历史/正确陈述: `:82`/`:152`/`:12`」——**`:14`/`:126` 从未被扫描器考虑过**, 「机械扫描」这一说法本身缺代码宿主 (无脚本产物/无完整输出留痕, 仅聚合报告一句话断言), 与 memory `no-code-host-no-assertion`/`pasted-evidence-is-derived` 同形。判定**仍与合并安全无关**(纯记录, 不影响探针/lib/测试/gitlink), 但这是同一 finding_id 连续第 4 轮命中同一份文档, 且导致的具体后果从「过时」升级为「文档内部相互矛盾」——比 R1-R3 各轮的残余更严重一档 (type=issue) finding_id=a3bfd693
- [minor] documentation/openspec/changes/linked-issue-field-availability/detailed-tasks.yaml: `:66` `status:` 字段仍写「TASK-025 in_progress (主仓 PR #190, pre_merge 收敛审计 R1/R2 已清账)」, 未随 R3 清账同步 (R3 commit `265a5f9` 未触碰本文件, `git log --oneline -- .../detailed-tasks.yaml` 显示最后一次改动是 R2 清账 commit `fdfb183`)。与 tasks.md `:5`(已在本轮更新为「测试 53/53 + state-scanner 1462 + run_all_tests 1894」, 但同样未提及具体到 R3) 及 proposal.md `:3`(「R2 清账 → 文档口径对正; 收敛后合并」, 同样未提及 R3) 属同类同批遗漏, 三份 Spec SOT 文件中只有 yaml 是**明确写错轮次数**(literal 「R1/R2」而非只是笼统未提及), 故单独列出; 不影响 `[x]`=24=`status: done`=24 的机械一致性 (归档门消费的核心不变量未受影响, 已复核), 纯叙事精度问题, 与 R1 已接受的「`Ran` vs 静态 `def test_` 差 16」同等对待 (type=issue) finding_id=95f02272

### R1–R3 carry 项独立复核 (未变更, 不重报)

| id | 处置 | 本轮独立核验方式 | 结论 |
|---|---|---|---|
| `ae4f1c9f`/`2ed89c8a`/`a2a4165f` (探针 archive 不可读 / `stdout.reconfigure` 过覆盖 / proposal 未回写 `UNREADABLE`+互斥) | carry v1.68.2 候选 (C7) | `git -C aria log --oneline -3` 头仍 `d1caa66` (R1 后零提交, 代码未变); `grep -n "UNREADABLE\|互斥" proposal.md` 零命中 (未变) | 未再报 |
| `ae4f1c9f`(C9 新形态, rglob 吞 PermissionError) | carry v1.68.2 候选 (C9) | 同上 (`linked_issue_field_probe.py` 零改动) | 未再报 |
| `d91f074e` (新 check 无专属回归测试) | carry | `grep -rln "plugin-version-arch-docs-match" aria/skills/state-scanner/tests/*.py` 零命中 (与 `m6-version-badge-match` 等对照组同现状) | 未再报 |
| `5333fe78`/`6ab01600` (CI workflow paths / coordination claim) | carry-forward | 非本 PR scope, 未变更 | 未再报 |
| `5da757d0` (spec-drafter `, ` 与 `,` 并存) | 接受为设计 | `aria` 零改动 (未再报) | 未再报 |

## Verdict

PASS_WITH_WARNINGS — Critical **0** / Major **1** / Minor **1**。

## 投票

**PASS**

理由: 本轮 major 与前三轮 `a3bfd693` 同一性质 (canonical handoff 记录与实物脱节, 现已升级为文档内部自相矛盾), 与合并是否安全 (探针正确性 / 测试 / gitlink / 版本面) 无关联; 下方核验记录逐条独立实跑证明核心机制全部成立: 53 条测试全绿 + 1 条真实产品模块对抗性 mutant (fence 排除, 非 R3 已测范围) 判别力成立、四态 state-check (OK/DRIFT/MISSING/SKIP) 用独立 scratch 副本复现全部四态、`--emit-arg` 精确输出、真实语料 `OK (9 份在范围内, 6 条在册)`、gitlink/16 版本点/3 份 i18n README 全部收敛到 1.68.1、B9-补「本循环不再推子模块」自 R1 起持续成立 (aria/standards HEAD 三轮零移动)。**不构成 REVISE**。

但明确: **本轮 C∪M ≠ ∅** (= {`a3bfd693`, `95f02272`}), 故 R4 不满足「稳定性确认」判据 (决策单「收敛口径」行要求 C∪M=∅ 且四票 PASS), 需 R5。并建议 R5 清账不要再用「人工过一遍已知问题行号」式的所谓机械扫描 (三轮实践已证明这种「扫描」漏了 `:11`/`:14`/`:126` 三处), 改用可重放的 grep/脚本、把完整命令与完整输出 (非仅摘要) 贴进聚合报告, 否则「机械扫描零残余」这句话本身就是下一轮要抓的证据不实 finding。

## 核验记录 (逐字命令与关键输出)

### 1. 基础回归

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
.....................................................
Ran 53 tests in 2.125s
OK

$ cd aria/skills/state-scanner/tests && python3 run_tests.py
Ran 1462 tests in 72.440s
OK

$ grep -rhE '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l
1478

$ bash aria/skills/run_all_tests.sh
...
state-scanner                                  OK (1462 tests)
...
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1894 个测试)
```

53 / 1462 / 1478 / 1894 四个数字与 CHANGELOG `## [1.68.1]` 段 (53/1462/1478)、tasks.md `:5` (53/1462/1894, 本轮已改)、PR #190 body (53/1462/1894)、handoff `:9`/`§5` 隐含数字均一致核对无误。CHANGELOG `## [1.68.0]` 段与 SUBSTITUTE.md/RESULT.md 的 1457/1473/1889 是 v1.68.0 时点历史值, 正确标注不可互换, 未计入本轮不一致。

### 2. 对抗性 mutant 验证 — 直接 monkeypatch 生产模块 (非仅测试内部 reference 实现)

对生产模块 `aria/skills/state-scanner/lib/linked_issue_field.py` 的 `_FENCE_RE`(E0 谓词 2, fence 排除) 原地打入「永不匹配」的坏正则 (纯内存 monkeypatch, 未改动任何仓内文件), 用真实测试方法直接跑:

```
$ cd aria/skills/state-scanner/tests && python3 -c "
import sys, re; sys.path.insert(0,'.'); sys.path.insert(0,'..')
import lib.linked_issue_field as m
m._FENCE_RE = re.compile(r'(?!x)x')          # 永不匹配 -> fence 排除失效
import test_linked_issue_field as t, unittest
suite = unittest.TestSuite()
suite.addTest(t.TestSC1Location('test_sc1b_fenced_example_not_field'))
suite.addTest(t.TestSC1Location('test_sc1d_blockquote_nested_fence_not_field'))
unittest.TextTestRunner(verbosity=2).run(suite)
"
test_sc1b_fenced_example_not_field ... FAIL   (AssertionError: 'OK' != 'NO_FIELD')
test_sc1d_blockquote_nested_fence_not_field ... FAIL   (AssertionError: 'OK' != 'NO_FIELD')
FAILED (failures=2)
```

坏实现 (fence 排除失效) 下两条测试从绿转红, 且是对**真实生产函数** `extract_linked_issue_field` 的 monkeypatch (调用方式与真实测试文件逐字一致, 非测试自带的 `_ref_extract` 影子实现), 判别力成立。选此样本是因为 R3 qa-engineer 的抽样覆盖 SC2/SC3/SC9/SC5ProbeHardening×4/SC5(d)/SC6, 未覆盖 E0 fence 排除这一支, 本轮补上。

### 3. 新 state-check `plugin-version-arch-docs-match` 四态 (scratch 副本, 未改动仓内文件)

```
# OK (repo 当前态实测, 非 scratch)
$ PLUGIN=1.68.1; A=1.68.1 (system-architecture.md); B=1.68.1 (version-scheme.md) → OK plugin=1.68.1 (2 arch doc rows match)

# DRIFT (scratch 副本 sed 改 system-architecture.md 行为 v1.68.0)
DRIFT plugin=1.68.1 vs system-architecture.md=1.68.0

# MISSING (scratch 副本删 version-scheme.md 的 aria-plugin 行)
MISSING version-scheme.md aria-plugin 行 -> exit 1

# SKIP (scratch 副本 plugin.json 路径不存在)
##SKIP## aria/.claude-plugin/plugin.json 不可读 -> exit 0
```

```
$ python3 -c "import yaml; d=yaml.safe_load(open('.aria/state-checks.yaml')); print(len(d['checks']))"
14
$ python3 -c "... 找 plugin-version-arch-docs-match ..." → enabled=True severity=warning timeout=5
```

### 4. `--emit-arg` 母 Spec 接缝 + 真实语料

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
10CG/Aria#174   exit=0
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)   exit=0
$ grep -vc '^\s*#\|^\s*$' .aria/linked-issue-field-grandfathered.txt
6   (与「6 条在册」一致)
```

### 5. 版本面 / gitlink / i18n 核验

```
$ git ls-tree HEAD aria standards
160000 commit d1caa66cb375c2799f55def453ca232c66a18c22	aria
160000 commit ffed2040dff7964cf9d137e85e174173d2c685b9	standards

$ grep -n "1.68.1" CLAUDE.md README.md VERSION docs/architecture/system-architecture.md docs/architecture/version-scheme.md
(全部命中, 逐一确认见上)
$ grep -rln "1\.68\.1" README.*.md
README.ja.md / README.zh.md / README.ko.md   (3/3, 无遗漏)

$ cd aria && git log --oneline -3 | head -1 && git rev-parse HEAD
d1caa66...  (R1 后零新提交)
$ cd standards && git rev-parse HEAD
ffed204...  (R1 后零新提交, B9-补自纠承诺持续成立)
```

### 6. 「机械扫描零残余」声称核验 (本轮主发现的证据来源)

```
$ git diff fdfb183 265a5f9 -- docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md | grep -E '^[+-]' | grep -c .
(R3 commit 只改了 frontmatter phase/updated-at, 「产品级待owner」句, §5 三行, 「不应该做的」段, footer Tags/PR 行, 末行 Status —— 共 8 处 hunk)

$ sed -n '11p;14p;126p' docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md
11: ... → **R2** 0C/2M/9m 清账 (本文与 Spec 三文件对正 v1.68.1 口径) → R3/R4 稳定性确认后合并。
14: > **Status**: Active — H1 四处推送完成; PR #190 pre_merge 收敛审计 R1/R2 已清账, R3/R4 稳定性确认后按 owner 指令合并 → D 归档
126: 1. ⭐ ... PR #190 pre_merge 收敛审计: R1/R2 已清账, **R3 (+R4 稳定性确认) → 合并** ...

$ sed -n '4p' docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md   # frontmatter (yaml, 行号含 --- 分隔符)
phase: C.2 (... R1 0C/4M、R2 0C/2M、R3 0C/1M 已清账, R4 稳定性确认; 收敛后合并)
$ sed -n '152p;178p' docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md
152: **Tags published**: ... **PR open**: Aria #190 (gate green; pre_merge 收敛审计 R1–R3 清账、R4 稳定性确认后按 owner 指令合并 → ...)
178: **Status**: Active — H1 四处推送已完成; PR #190 pre_merge 收敛审计 R1–R3 已清账, R4 稳定性确认后按 owner 指令合并 → D 归档 (...)
```

三处 (`:11`/`:14`/`:126`) vs 两处 (`:4`/`:152`/`:178`, 实为三处) 对同一事实给出不同取值, 逐行 `sed -n` 直接反驳 R3 aggregated report `:28` 「机械扫描残余=0」的字面声称。

### 7. detailed-tasks.yaml / proposal.md / tasks.md 三文件轮次口径独立扫描

```
$ git log --oneline -- openspec/changes/linked-issue-field-availability/detailed-tasks.yaml | head -3
fdfb183 docs(pr190): pre_merge 收敛审计 R2 清账 ...   ← 最后一次改动, R3 未再碰
$ sed -n '66p' openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
status: "... TASK-025 in_progress (主仓 PR #190, pre_merge 收敛审计 R1/R2 已清账); ..."

$ grep -c "R3" openspec/changes/linked-issue-field-availability/proposal.md openspec/changes/linked-issue-field-availability/tasks.md
proposal.md:1   (仅出现在 M4「R2 的 C-A」等无关上下文, `:3` Status 行本身未提 R3 清账)
tasks.md:1      (`:5` Status 行「测试 53/53...」未提具体到 R3, 但未写错数字, 与 yaml 的「literal R1/R2」不同级)

$ grep -c '^\s*- \[x\]' openspec/changes/linked-issue-field-availability/tasks.md
24
$ grep -c '^\s*status: done' openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
24
```

`[x]`=24=`status: done`=24 一致 (归档门核心不变量未受影响); yaml `:66` 叙事字段单独滞后, 不影响该不变量。

### 8. 工作树核验 (未留改动)

```
$ git status --short
 M aria-orchestrator   (会话既有停泊状态, 非本轮改动)
$ git -C aria status --short && git -C standards status --short
(均干净)
```

所有 mutant / scratch 文件在 `/tmp/claude-1000/.../scratchpad/pr190-qa-r4/`, 未触碰仓内任何文件。
