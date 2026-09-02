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
timestamp: 2026-09-02T13:47:21.819Z
context: PR #190 linked-issue-field-availability (main 0e9619c / aria fe32441 / standards fad8b4b)
agents: [qa-engineer]
---

## 审计结论

- [major] testing/aria/skills/state-scanner/tests/test_linked_issue_field.py: `test_sc5_d_degraded_missing_collision_module_is_skip` docstring 声称隔离「`lib/collision.py` 缺失」(引用 proposal §「本轮引入的新表面」#1(a) 的未验风险), 但独立复现表明真实触发的异常与 collision.py 无关, fixture 未实际关闭它引用的那条风险 — 证据: 用契约同款「复制 skill 根到临时目录, 只带 `lib/__init__.py` + `lib/linked_issue_field.py`, 不带 collision.py」的手法独立重放 (不改仓内文件), `python3 -c "sys.path.insert(0,'<tmp>'); from lib.linked_issue_field import extract_linked_issue_field"` 抛出 `ModuleNotFoundError: No module named 'lib.claim_lifecycle'`（`lib/__init__.py:17` 的 `from .claim_lifecycle import (...)` 是包内**第一条**导入, 早于任何代码有机会执行 `linked_issue_field.py` 自身的 `from .collision import normalize_linked_issue`）; 而用**真实完整** `lib/` 目录只删 `collision.py` 一个文件复现「仅 collision.py 缺失」这个具体场景 (`rm lib/collision.py` 后跑真实 `linked_issue_field_probe.py`), 探针本身正确输出 `##SKIP## 归一 SOT 不可导入…` exit 0 — 说明**生产代码是对的**, 缺口只在于本条测试未覆盖它自称覆盖的那个具体场景 (它验证的是"lib 包内任意一个先于 collision 的子模块缺失"这个更粗的场景, 恰好也走到同一 except 分支)。(type=issue) finding_id = `e4cde200`

- [minor] testing/aria/skills/state-scanner/tests/test_collision.py: CHANGELOG / SUBSTITUTE.md / handoff 并列汇报的两个回归数字 (`run_tests.py` 全量 `Ran 1457` vs 静态 `grep '^\s*def test_' *.py` = `1473`, 差 16) 有确定成因但文档均未点破 — 证据: `python3` AST 分析确认 `test_collision.py` 里 16 个 `def test_*` 函数 (:56/:60/:65/:74/:83/:92/:101/:110/:124/:135/:145/:158/:167/:182/:261/:281) 是**模块级** pytest 风格函数、非 `unittest.TestCase` 子类方法, `run_tests.py` 用 `unittest.TestLoader().discover()`, 该 loader 只收集 `TestCase` 方法, 这 16 条从未被 `run_tests.py`/`run_all_tests.sh` 实际执行过 (可用 `python3 -m pytest test_collision.py --collect-only` 交叉证实, 本次未额外装 pytest 故用 AST 佐证)。本 PR 未触碰该文件 (`git diff d69091d fe32441 -- skills/state-scanner/tests/test_collision.py` 为空), 是预先存在的缺口, 非本 PR 引入; 新增的 `test_linked_issue_field.py` 48 个方法本身经 AST 核对全部是 `TestCase` 子类方法, 无同款遗漏。留痕以免下次有人假设 1457 == 1473 应当相等。(type=risk) finding_id = `6cdc6077`

- [minor] testing/aria-plugin-benchmarks/ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/PREDICTION.md: 「预测先于实测」的时序证据链弱 — 证据: `stat` 显示 `PREDICTION.md` / `RESULT.md` / 各 `grading.json` 的 mtime 精确到毫秒级几乎相同 (`08:30:22.9[5-7]xx`, 同一 git checkout 落盘), `git log --follow` 显示该目录全部文件属同一提交 `989d14c`, 两者均**不能**佐证章节顺序; 唯一可核验的是内容内部一致性 — 我逐条核对 PREDICTION.md「可证伪点」第三条 (「若基线也写出合规行 ⇒ … 降级为『本轮未证』」) 与 RESULT.md §2.2 的实际处置逐字吻合, 且 PREDICTION.md 全文未出现任何具体分值/token 数等后验信息, 内容本身可信但方法论上留痕: 本仓当前的 AB 留痕流程无法用外部证据 (非内容自身) 反驳「实测后回填预测」的可能性。(type=risk) finding_id = `46b1df1a`

## Verdict

Critical: 0 · Major: 1 · Minor: 2 → **PASS_WITH_WARNINGS**

## 投票

**PASS**

理由: 0 Critical、1 Major 均不构成「必须在合并前修」——Major 项 (SC-5(d)) 经独立复现证实**生产代码本身正确** (真实只删 `lib/collision.py` 一个文件, 探针照常正确降级到 `##SKIP##` exit 0), 缺口纯属该条测试 docstring 对自己实际覆盖范围的误述, 不影响任何用户可见行为、也不掩盖已知缺陷; 与本 PR 自身 B 期先例 (决策单 B3, SC-3(a) 理据不准但不改判定, 记入下次触碰) 处置口径一致, 建议同批记入 PR body / 下次触碰该测试文件时补一个真正只删 `collision.py` 的独立 fixture (或调整 docstring 措辞), 不阻塞本次合并。两条 Minor 均为观测性记录, 均非本 PR 引入的新缺陷。

## 核验记录

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
................................................
Ran 48 tests in 1.530s
OK

$ cd aria/skills/state-scanner/tests && time python3 run_tests.py     # 全量
Ran 1457 tests in 76.327s
OK

$ grep -rh '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l
1473

$ python3 <AST 脚本, 只数 ClassDef 内的 test_ 方法> aria/skills/state-scanner/tests/*.py
TOTAL(ast, class-level test_ methods): 1457     # 与 run_tests.py 的 Ran 数逐位吻合
# 差值 16 全部定位到 test_collision.py 的模块级函数 (非 class 成员), AST 逐一列出行号:
# :56 :60 :65 :74 :83 :92 :101 :110 :124 :135 :145 :158 :167 :182 :261 :281

$ timeout 590 bash aria/skills/run_all_tests.sh
... state-scanner  OK (1457 tests) ...
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1889 个测试)     # 与 CHANGELOG/handoff 声称的 "9 套件 / 1889" 逐字吻合

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt; echo EXIT=$?
OK (9 份在范围内, 6 条在册)
EXIT=0
$ find openspec/changes -maxdepth 2 -name proposal.md | wc -l   # 9, 与探针输出 n 一致
$ (白名单 6 条路径逐条 grep 'Linked Issue\|关联 Issue' 各自 proposal.md) → 全部 0 命中 (真 NO_FIELD, 陈旧守卫 (c) 不应触发, 与 OK 结果一致)
$ (作用域内剩余 3 份非白名单 proposal: a1-entry-claim-duplicate-work-guard / linked-issue-field-availability / sibling-spec-probe) → 逐条 grep 均命中合规行 (`10CG/Aria#174` 真 token 或 `none` 哨兵)

$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | od -c | head -2
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4          # 13 字节, 无尾随换行, 与 SUBSTITUTE.md 声称逐字吻合

# --- 对抗性核验: 6 条采样测试, 复制 aria/skills/state-scanner 到 scratchpad/adv, 逐次注入一个仓外坏实现, 不改仓内文件 ---
# baseline (未注入 bug): 6 条全绿
$ python3 -m unittest test_linked_issue_field.{TestSC1Location.test_sc1d_blockquote_nested_fence_not_field,TestSC4Sentinel.test_sc4f_trailing_whitespace_none_is_bad_token,TestSC5ProbeCheckMode.test_sc5_c_stale_allowlist_three_letter_forms,TestSC5ProbeCheckMode.test_sc5_d_degraded_missing_collision_module_is_skip,TestSC5ProbeCheckMode.test_sc5_e2_missing_allowlist_with_violation,TestSC9EmitArg.test_sc9a_placeholder_bad_token_emits_empty} -v
Ran 6 tests ... OK

# SC-1(d): _FENCE_RE 去掉 `(?:> ?)?` (母 Spec 命名 flaw 3) → AssertionError: 'OK' != 'NO_FIELD'  [RED 确认]
# SC-4(f): E5 哨兵判定改用 token_str.strip() (flaw 11) → AssertionError: 'OK' != 'BAD_TOKEN'  [RED 确认]
# SC-9(a): emit_arg 对非 OK 分支也 passthrough token_elements[0] (flaw 13) → AssertionError: '{<org>/<repo>#<n>}' != ''  [RED 确认, 经真实 subprocess CLI 路径]
# SC-5(c): 探针 stale-allowlist 守卫的 for 循环体替换成 `for e in []:` (静默禁用) → AssertionError: 0 != 1  [RED 确认]
# SC-5(e2): 探针「白名单文件缺失」分支改为直接 print OK + return 0 (R4/K9 回归) → AssertionError: 0 != 1  [RED 确认]
# SC-5(d): 探针 import-except 分支改为 print("OK (0 份在范围内, 0 条在册)") 而非 ##SKIP## (零证据当正证据) → AssertionError: False is not true (startswith ##SKIP##)  [RED 确认]
# 全部 6 条在对应坏实现下真实转红, 逐条改回原文件后核对 baseline 复绿 (未持久修改任何仓内文件, 全部操作发生在 /tmp/claude-1000/.../scratchpad/adv/state-scanner 与 /tmp/claude-1000/.../scratchpad/sc5d-real)

# _MATRIX_EXEMPT 独立复核 (13 个坏实现 × 3 条豁免夹具 SC1a/SC4b/SC9d, 逐一跑真实 test 模块里的 _BAD_EXTRACTORS + 13th flaw):
$ python3 -c "... for label in ('SC1a','SC4b','SC9d'): for name,fn in t._BAD_EXTRACTORS.items(): ..."
== SC1a == (none found)
== SC4b == (none found)
== SC9d == (none found)
# 13 个具名 flaw 对这 3 条夹具确无区分力, 决策单 B2 豁免站得住, 未发现被掩盖的缺陷

# SC-5(d) 具体异常来源复核 (证明 docstring 与真实触发原因不符):
$ python3 -c "sys.path.insert(0,'<copy_root 只带 __init__.py + linked_issue_field.py>'); from lib.linked_issue_field import extract_linked_issue_field"
ModuleNotFoundError: No module named 'lib.claim_lifecycle'    # 不是 collision.py

$ (真实完整 lib/ 目录只删 collision.py 一个文件, 其余不动) → 跑真实 linked_issue_field_probe.py
##SKIP## 归一 SOT 不可导入 (aria 侧 lib/collision.py 或 lib/linked_issue_field.py 缺失 / 版本 < 1.68.0)
EXIT=0     # 生产代码本身对"仅 collision.py 缺失"这个真实场景处理正确

# 跨仓 skip 核验: 主仓布局下 SC-6/SC-7a/SC-8 三类测试是否真走到断言而非 self.skipTest
$ python3 -m unittest test_linked_issue_field.TestSC6Template test_linked_issue_field.TestSC8Registration test_linked_issue_field.TestSC7aPreviewFence -v
Ran 4 tests ... OK   # 全部 "ok"，run_tests.py -v 全量输出里 grep skip 只命中 SC-5 scope-missing/degraded 两个"设计即 SKIP"用例，无意外 skip

# AB 产物逐字重算 (grading.json + timing.json → RESULT.md 两张表全部数字):
iteration-1: eval1 2/2 vs 2/2 (74.0k/92s vs 75.4k/105s); eval2 5/5 vs 5/5 (131.3k/549s vs 114.9k/358s);
             eval3 5/5 vs 5/5 (168.6k/743s vs 142.3k/504s); 合计 12/12 vs 12/12 delta=0   [全部逐位吻合]
control:     eval2 5/5 vs 3/5 (118.7k/454s) delta+2; eval3 5/5 vs 4/5 (173.3k/668s) delta+1;
             合计 10/10 vs 7/10 delta+3                                                    [全部逐位吻合]

# eval_metadata.json assertions 与 ab-suite/spec-drafter.json expectations 逐条文本比对 (3 个 eval):
eval 1/2/3: metadata assertions == suite expectations (verbatim, order-preserved)? True / True / True

# ab-suite 盘点口径重算:
$ cd aria-plugin-benchmarks/ab-suite && ls *.json | wc -l          → 31   (= version.yaml skills_covered)
$ python3 -c "sum(len(d['evals']) for ...)"                        → 74   (= version.yaml total_eval_cases;
                                                                       phase-c-integrator-pre-merge-gate.json 无 'evals' 键, 正确被排除未计入)

# aria-plugin#117 归并评论 ground-truth 核验 (非回执):
$ forgejo GET /repos/10CG/aria-plugin/issues/117/comments
→ 1 条, id=20573, url=…issuecomment-20573 (与 RESULT.md 声称逐字吻合), created_at=2026-09-02T08:18:45Z, user=simonfish,
  body 含「第二实例」「linked-issue-field-authoring-TARGETED」

# 零改动断言 (decision B-period + handoff 声称) 核验:
$ git diff d69091d fe32441 --stat -- skills/state-scanner/lib/collision.py skills/state-scanner/lib/__init__.py \
    skills/state-scanner/SKILL.md skills/state-scanner/scripts/issue_cache_freshness_probe.py \
    skills/state-scanner/scripts/coordination_probe.py
(无输出 — 五个文件全部零 diff, 与声称吻合)
```
