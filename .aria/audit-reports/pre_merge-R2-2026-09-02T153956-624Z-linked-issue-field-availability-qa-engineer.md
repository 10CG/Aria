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
timestamp: 2026-09-02T16:10:15.000Z
context: PR #190 linked-issue-field-availability (main 17ae85e / aria d1caa66 / standards ffed204)
agents: [qa-engineer]
---

# Round 2 — qa-engineer 独立重审 (测试与证据真实性, 清账后)

## 方法论

未读过 R1 各席个人报告, 只读了 R1 聚合报告 (12 条去重 finding + 处置表) 与本简报, 然后对清账后状态做独立重跑/独立重推导, 不信任何一处「声称」— 见下方核验记录逐条命令与输出。

## 审计结论

本轮**未发现任何 critical/major**。四个镜头任务 (SC-5(d) 隔离性 / TestSC5ProbeHardening 4红1绿 / SC-6(iii) 恒真性 / 53 条抽样红绿 / 回归数字 / 新 state-check 三态 / AB 追注一致性 / 决策单 B8-B9 站得住性) 全部独立复现成立, 详见核验记录。仅 1 条新 minor:

- [minor] testing/.aria/state-checks.yaml: 新 check `plugin-version-arch-docs-match` 无专属回归测试断言「已提交的 system-architecture.md/version-scheme.md 当前能被该 check 判 OK」(memory `feedback_validator_repo_drift_guard_test.md` 的 drift-guard-test 模式缺失) — 证据: 3 态 (OK/DRIFT/MISSING) 均需本轮由我手工临时构造验证, 仓内无自动化持续保护; 但**与该文件另外 13 条既有 check 现状一致** (`grep -rln 'm6-version-badge-match\|i18n-readme-translation-currency' aria/skills/state-scanner/tests/*.py` 零命中), 非本 PR 独有退步, 不建议单独阻塞合并 (type=risk) `finding_id=d91f074e`

## R1 finding 核验记录 (已修/已裁, 不重报; 每条附我自己的复核方式)

| R1 id | R1 处置 | 本轮核验方式 | 结论 |
|---|---|---|---|
| `e4cde200` (major, SC-5(d) 夹具) | aria v1.68.1 复制完整 lib/ 只删 collision.py + ImportError 点名断言 | 独立在 scratch 目录复现同一夹具 (非跑仓内测试, 自己手搭): `import lib.linked_issue_field` 报错精确点名 `lib.collision`; 探针在该 copy 上 `##SKIP##` exit 0 | 修复成立, 未再报 |
| `a3bfd693` (major, handoff frontmatter) | 刷新 + merge origin/master 29c1e4f | `head -20 docs/handoff/2026-09-02-...md` frontmatter updated-at=2026-09-02T14:27:14Z; `git merge-base --is-ancestor 29c1e4f HEAD` → true | 修复成立, 未再报 |
| `9ac5533a` (major, hunk A 顺序条款) | 决策单 B8: 位置无关是设计, 白名单头注+fix文案补位置说明, SKILL.md 软化 carry | 读 Spec `:491` D2 原文核对 B8 引用无误; `head` 白名单文件 / `sed -n` state-checks.yaml fix 文本均含「位置不限」「E0 取文档序第一条」措辞; `spec-drafter/SKILL.md:341` 仍写「必须…逐行对齐」(裁定明确 carry, 非本 PR 修) | 裁定站得住 (D2 引用准确, 证据文本确实落地), 未再报 |
| `ac44ace3` (major, arch 文档漂) | 两行 → 1.68.1 + CLAUDE.md 同步面 + 新 check | 独立三态实测 (见下), CLAUDE.md:81 已列两文件为同步点, `main-project-version-consistency` 类 check 新增第 14 条经 `_parse_state_checks_yaml` 解析确认注册 | 修复成立, 未再报 |
| `ae4f1c9f`/`2ed89c8a`/`a0ff4897` (minor×5, 探针加固) | 白名单归一/fail-closed/archive非glob/编码/互斥/注释 | diff 旧探针(fe32441)vs新探针逐处比对 + `grep -n archive` 确认 `d.name.endswith("-"+slug)` 非 glob + `grep is_sentinel` 注释已改真实用途 + `grep CONTRACT` 零命中 | 修复成立, 未再报 |
| `4605dc4d` (minor, 模板 CJK) | standards ffed204 英文化 | `head -60 standards/openspec/templates/proposal-minimal.md` 实读: 「do not leave the value empty and do not delete the line」逐字存在 | 修复成立, 未再报 |
| `6cdc6077` (minor, Ran vs 静态口径) | 记入 CHANGELOG/SUBSTITUTE/RESULT | 独立 AST 计数 (非 grep) 全仓 `test_*.py`: 1478; `run_tests.py` 实跑 Ran 1462; 1478-1462=16; 独立确认 `test_collision.py` 恰 16 个模块级裸函数且 `unittest.defaultTestLoader.loadTestsFromName('test_collision')` 实测收集 0 个 | 口径注准确, 未再报 |
| `46b1df1a` (minor, PREDICTION 时序) | 接受为方法论留痕 | 读 PREDICTION.md 全文与 RESULT.md §1「测前预期 vs 实测」表逐行核对, 可证伪分支确与实测吻合 | 接受成立, 未再报 |
| `5333fe78`/`6ab01600` (minor, C1/C2 carry) | carry-forward | 未变更, 决策单 C1/C2 仍在案 | 未再报 |

## 本轮四镜头任务独立核验 (核心)

### 任务 1 — SC-5(d) 隔离性 + TestSC5ProbeHardening 4红1绿 + SC-6(iii) 恒真性 + 53条抽样

见下方核验记录逐条命令。结论: 全部成立, 无恒真项。

### 任务 2 — 回归声称 vs 实测

`run_tests.py` Ran=1462 (实跑) 与 CHANGELOG 1.68.1「1462 全绿」逐字一致; 独立 AST 计数 1478 与「静态 def test_ 1473→1478」逐字一致 (1473 为 v1.68.0 旧值, 现态 1478); 16 差额用 `unittest.defaultTestLoader` 直接验证「0 个被收集」而非仅推断。

### 任务 3 — `plugin-version-arch-docs-match` 三态 + fail-closed

`_parse_state_checks_yaml` 解析出 14 条 check, 该条 `enabled: true`; 在独立 scratch 副本 (从不改动仓内文件) 上实跑三态: OK (未改动) exit 0 / DRIFT (改 system-architecture.md 版本行) exit 1 精确文案 `DRIFT plugin=1.68.1 vs system-architecture.md=1.68.0` / MISSING (删 version-scheme.md 该行) exit 1 精确文案 `MISSING version-scheme.md aria-plugin 行`。SOT (`plugin.json`) 不可读时 `##SKIP##` exit 0 (设计如此, 非 fail-open — 与仓内其余探针同形, 描述里显式写明); 三个可判定分支 (DRIFT/MISSING/OK) 均 fail-closed 正确。缺口: 见上方 minor `d91f074e`。

### 任务 4 — AB 产物追注一致性

RESULT.md §2 第 5 点 (B8 追注) 引 Spec D2 原文核对无误; 其「作用域 9 份既有 proposal 0/9 符合该顺序也都不被判红」用真实探针对当前仓重跑复核 (`OK (9 份在范围内, 6 条在册)`, 与 SUBSTITUTE.md §2 命令输出逐字对齐)。RESULT.md/SUBSTITUTE.md §4 的「Ran 1457 / 静态 1473 / 差 16」是历史值 (v1.68.0 时点, R1 commit diff 确认该行是 R1 新增追注但描述的是**跑 AB 时**的旧值, 非现态) —— 用 `git show 17ae85e -- .../RESULT.md .../SUBSTITUTE.md` 核对这两处正是 R1 commit 唯一新增的两处文本, 无其他改动被夹带。

## Verdict

PASS_WITH_WARNINGS — 0 Critical / 0 Major / 1 Minor。

## 投票

**PASS**

## 核验记录 (逐字命令与关键输出)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 2.031s

OK

$ cd aria/skills/state-scanner/tests && python3 run_tests.py
Ran 1462 tests in 70.397s
OK

$ grep -rhE '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l   # (独立 grep 交叉核, AST 版见下)
1478
```

AST 独立计数 (非 grep, 全 test_*.py, ast.FunctionDef + AsyncFunctionDef):
```
total: 1478   (test_linked_issue_field.py: 53, test_collision.py: 16, ... 完整逐文件表已核对, 与 grep 数一致)
```

SC-5(d) 隔离性独立复现 (未跑仓内测试代码, 自建 scratch 目录):
```
$ mkdir -p $SCRATCH/copy/lib && cp aria/skills/state-scanner/lib/*.py $SCRATCH/copy/lib/ && rm $SCRATCH/copy/lib/collision.py
$ python3 -c "import sys; sys.path.insert(0,'$SCRATCH/copy'); import lib.linked_issue_field"
ModuleNotFoundError: No module named 'lib.collision'      # 精确点名 collision, 非 claim_lifecycle 等其他符号
$ python3 $SCRATCH/copy/scripts/linked_issue_field_probe.py $SCRATCH/proj --grandfathered $SCRATCH/proj/does-not-exist.txt
##SKIP## 归一 SOT 不可导入 ...    exit=0
```

TestSC5ProbeHardening 对 fe32441 (v1.68.0) 旧探针 4红1绿独立复现:
```
$ git -C aria show fe32441:skills/state-scanner/scripts/linked_issue_field_probe.py > $SCRATCH/state-scanner-old/scripts/linked_issue_field_probe.py
$ cd $SCRATCH/state-scanner-old/tests && python3 -m unittest test_linked_issue_field.TestSC5ProbeHardening -v
test_allowlist_entry_normalization_and_dedupe ... FAIL
test_check_mode_survives_ascii_stdout ... FAIL
test_detail_lines_bad_token_and_no_token ... ok      # 细节行本就绿, 与 CHANGELOG 声称一致
test_root_positional_with_emit_arg_is_exit2 ... FAIL
test_unreadable_proposal_is_fail_not_crash ... FAIL
Ran 5 tests in 0.492s
FAILED (failures=4)   # 4 红 1 绿, 与 CHANGELOG 1.68.1「对 v1.68.0 探针实测 4 红 1 绿」逐字吻合
```

SC-6(iii) 恒真性对抗核验 (合成负控字符串, 不改仓内文件):
```
"no wording at all (adversarial)" -> (False, False, False)   # 两个 assertTrue 均会 AssertionError, 非恒真
"has `none` but no leave/delete wording" -> (True, False, False)
"real template excerpt" -> (True, True, True)
"CJK only" -> (True, True, True)
```

53 条抽样 4 条 monkeypatch 坏实现验红 (复用测试文件自带 `_bad_*` 参考实现, 替换 `test_linked_issue_field.extract_linked_issue_field` 后单独跑对应测试方法):
```
test_sc1f_plural_spelling_rejected with _bad_loose_plural: wasSuccessful=False
test_sc4c_ascii_none_ok with _bad_chinese_only: wasSuccessful=False
test_sc4e_na_is_bad_token with _bad_na_as_sentinel: wasSuccessful=False
test_sc1h_unicode_homoglyph_rejected with _bad_unicode_fold: wasSuccessful=False
--- 真实实现下 sanity: 全部 wasSuccessful=True ---
```

新 state-check 三态独立实测 (scratch 副本, 未改动仓内文件):
```
$ (cd $SCRATCH_CHECK && bash -c "$CMD")   # 未改动副本
OK plugin=1.68.1 (2 arch doc rows match)   exit=0
$ sed -i 's/| aria-plugin | v1.68.1 |/| aria-plugin | v1.68.0 |/' $SCRATCH_CHECK/docs/architecture/system-architecture.md
$ (cd $SCRATCH_CHECK && bash -c "$CMD")
DRIFT plugin=1.68.1 vs system-architecture.md=1.68.0   exit=1
$ sed -i '/\*\*aria-plugin\*\*/d' $SCRATCH_CHECK/docs/architecture/version-scheme.md
$ (cd $SCRATCH_CHECK && bash -c "$CMD")
MISSING version-scheme.md aria-plugin 行   exit=1
```

Parser 确认注册:
```
$ python3 -c "... _parse_state_checks_yaml(open('.aria/state-checks.yaml').read())['checks'] ..."
total checks: 14
found (name='plugin-version-arch-docs-match'): 1, enabled: true
```

版本同步面独立巡检 (全部命中 1.68.1, 无遗漏):
```
VERSION(主仓) / aria/VERSION / aria/.claude-plugin/plugin.json / marketplace.json / README.md(badge+正文)
/ README.zh.md / README.ko.md / README.ja.md / docs/architecture/system-architecture.md:189
/ docs/architecture/version-scheme.md:23 / CLAUDE.md (§81 同步面清单 + §139/141 项目状态段)
```

探针真实运行 (对当前仓真实状态, 非合成夹具):
```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)   exit=0
```

R1 清账 commit 精确改动面核对 (确认 RESULT.md/SUBSTITUTE.md 追注是 R1 唯一新增文本, 无夹带):
```
$ git show 17ae85e -- .../RESULT.md      # 仅新增 §2 第5点 + §4 一行口径注
$ git show 17ae85e -- .../SUBSTITUTE.md  # 仅 §2 一行末尾追加口径注
```

Decision record B8/B9 引用核对:
```
$ grep -n "D2" openspec/changes/linked-issue-field-availability/proposal.md   # :491 「定位谓词=行首depth-1+fence排除+文档序第一条」与 B8 引述一致
$ grep -n -A5 "### 2.3" standards/conventions/version-management.md          # 「文档错误修正/链接修复/小改进」与 B9 引述一致
```

无 finding 的自证 (fixture 恒真性): `TestBadImplementationMatrix.test_each_adversarial_fixture_has_a_discriminating_bad_impl` 对全部非豁免夹具跑 13 个坏实现取差异 (仓内既有机制, 本轮抽样复核未发现例外)。
