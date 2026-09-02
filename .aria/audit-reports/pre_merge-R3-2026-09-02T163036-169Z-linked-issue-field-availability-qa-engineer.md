---
checkpoint: pre_merge
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T17:10:00.000Z
context: PR #190 linked-issue-field-availability (main fdfb183 / aria d1caa66 / standards ffed204)
agents: [qa-engineer]
---

# PR #190 pre_merge 收敛审计 — Round 3 — qa-engineer (fresh 席)

> 镜头: 测试与证据真实性。方法论: 未读 R1/R2 各席个人报告 (仅聚合报告) 前先独立复跑核心命令, 随后才读三份已在案的 R3 姊妹报告 (code-reviewer / knowledge-manager / tech-lead) 做交叉核对 —— 三席已独立发现下方 finding 1 的同一根因 (三种不同严重度判定), 本报告的证据链是我自己重新实跑得出, 与他们的证据部分重叠部分互补 (§5 表另两行 `2.0.1` / `B1–B7` 为本席独有证据), 严重度取值最终与 tech-lead / knowledge-manager 一致 (major), 是独立收敛而非采信。

## 审计结论

- [major] documentation/docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md: R2 对 major `a3bfd693` 的「类级」清账声称 (聚合报告逐字「标题 / 一句话 / §0-2 / §2 H1 行 / §3 风险行 / §5 三行 / §6 第 1-2 条 / 不应该做的 / footer 全部对正」) **不成立, 第三轮同形残余**。四处独立证据 (前两处与 tech-lead/km 重合, 后两处为本席独有): (a) **footer 自相矛盾**: `:178`(末行) `**Status**: Active — 下个 session 第一件事 = owner 推送授权 → C.2 + PR → D` 与 `:14` `> **Status**: Active — H1 四处推送完成; PR #190 pre_merge 收敛审计 R1/R2 已清账…` 同一字段名两个相反取值; (b) §5 表 OpenSpec 行仍 `tasks.md 22/25`, 实测 `grep -c '^\s*- \[x\]' tasks.md`=**24**; (c) §5 表「架构文档」行仍 `system-architecture.md 2.0.1`, 实测该文件当前 `> **Version**: **2.0.2**` (Version History 967 行有 2.0.2 条目, 且该条目正是 R2 自己在同一 commit `fdfb183` 里新增的 — 与 §5 表本应同批更新的信息在同一 commit 内不同步); (d) §5 表「Decision memos」行仍 `追记 §B 期 B1–B7`, 文末 Cross-references `(§B 期追记 B1–B7)` 同款未更新, 但决策单实际已到 `B8/B9/B9-补/C1–C7` (`grep -c '^| B[0-9]\|^| C[0-9]' 决策单` 现为 16 行条目)。用 `git show fdfb183 -- docs/handoff/…` 逐 hunk 核对: R2 该 commit 对 §5 表只动了 3 行 (Standards / Skill docs / CHANGELOG), (b)(c)(d) 三行在 diff 里完全未出现 —— 证实「§5 三行」的字面意思就是「只改了 3 行, 非全表」, 与聚合报告「口径对正」的表述不符。**判定与合并安全无关** (纯文档记录与实物脱节, 不影响探针/lib/测试/gitlink 的正确性, 详见下方核验记录逐条实测), 但作为 Rule #9 canonical handoff, 若原样并入 master 会把一份内部自相矛盾的记录永久冻结 (type=issue) finding_id=a3bfd693
- [minor] documentation/openspec/changes/linked-issue-field-availability/tasks.md: `:5` Status 行「测试 53/53 + state-scanner 1462 + run_all_tests 1889 全绿」混用两个时间点 —— 前两个数字是 v1.68.1 PATCH 后的值 (与我独立实跑 `Ran 1462` 逐字一致), 但 `run_all_tests.sh` 聚合数「1889」是 PATCH 前 (v1.68.0) 的旧值; 本轮独立实跑 `bash aria/skills/run_all_tests.sh` 聚合数为 **1894** (= 1889 + 5, 与 state-scanner 净增 1462−1457=5 吻合, 其余 8 个 skill 套件数未变), 未随 53/1462 同步勘正。`aria/CHANGELOG.md` 的「1889」在 `## [1.68.0]` 段 (版本化历史记录, 冻结正确, 非本 finding 对象); handoff `:11`/`:40` 的「1889」是带时刻的历史行, 同理不计入。纯数字精度问题, 不影响任何机制判定, 与 R1 已接受的「`Ran` vs 静态 `def test_` 差 16」(finding `6cdc6077`) 同类同等对待 (type=issue) finding_id=62285020

### R1/R2 carry 项独立复核 (未变更, 不重报; 逐条我自己的核验方式)

| id | R2 处置 | 本轮独立核验 | 结论 |
|---|---|---|---|
| `ae4f1c9f`/`2ed89c8a` (minor×2, 探针 archive 不可读 + `stdout.reconfigure` 过覆盖 `--emit-arg`) | carry v1.68.2 候选 (C7 最高优先) | 读当前 `linked_issue_field_probe.py:82-234` 源码确认两处代码现状仍如 R2 所述: archive 目录 `is_dir()` 前无 try/except; `sys.stdout.reconfigure(errors="replace")` 在 `main()` 顶部无条件执行 (含 `--emit-arg` 分支) | 描述仍准确, 未再报 |
| `a2a4165f` (minor, proposal §4/TASK-008/009 未回写) | carry, 随 B3 下次触碰 proposal 同批 | `grep -n "UNREADABLE\|root+emit-arg 互斥" openspec/changes/.../proposal.md` 零命中, 与 CLI 实测行为 (`test_unreadable_proposal_is_fail_not_crash` / `test_root_positional_with_emit_arg_is_exit2` 均绿) 确有落差 | 未回写属实, 未再报 |
| `d91f074e` (minor, 新 check 无专属回归测试) | carry, 与其余 13 条同现状 | `grep -rln "plugin-version-arch-docs-match" aria/skills/state-scanner/tests/*.py` 零命中; `grep -rln "m6-version-badge-match\|i18n-readme-translation-currency" 同目录` 同样零命中 (对照组) | 描述准确, 非本 PR 独有退步, 未再报 |
| `5da757d0` (minor, spec-drafter `, ` 与 `,` 并存接受为设计) | 决策单 C4 接受 | 读 proposal §3 E4「按逗号 split 后 strip」逐字确认两种写法皆合法; state-checks fix 文案含括注 | 未再报 |
| `5333fe78`/`6ab01600` (minor, CI workflow paths / coordination claim) | carry-forward C1/C2 | 未变更, 非本 PR scope | 未再报 |

## Verdict

PASS_WITH_WARNINGS — Critical **0** / Major **1** / Minor **1** (新增去重后; carry 项 5 条不计入本轮新增计数)。

## 投票

**PASS**

理由: 上述 major/minor 均为「文档记录 vs 实物」脱节, 不改变任何机制/测试/gitlink 的正确性判定 —— 下方核验记录逐条独立实跑证明: 53 条新测试对坏实现 (mutant) 100% 判别力、SC-5(d) 夹具隔离两条断言均判别、新 state-check 四态 (OK/DRIFT/MISSING/SKIP) 皆 fail-closed、`--emit-arg` 对母 Spec 产出精确 13 字节无换行、探针真实语料 `OK (9 份在范围内, 6 条在册)`、Spec 三文件 `[x]`24 == yaml done 24、B9-补 自纠诚实且与本轮子模块零推送一致。这些是决定「合并是否安全」的核心事实, 全部成立。finding 1 (major) 唯一实质风险是「一份自相矛盾的 canonical handoff 被冻结进 master」, 属文档卫生而非合并安全, 与 code-reviewer / knowledge-manager / tech-lead 三席独立判断一致 (三席均投 PASS, 严重度判定不同但均未认为构成合并阻塞)。**不构成 REVISE**, 但明确: 本轮 C∪M ≠ ∅ (= {a3bfd693}), 故 R3 不可声称收敛, R4 仍需清账后确认。

## R2 两条 major 清账完整性专项核验 (本轮主要任务)

1. **`ee23ca88`** (Spec 三文件口径): **基本完整但有 1 处残留** (即上方 finding 2, `1889` vs `1894`) —— `d1caa66` / `ffed204` / `53` / `1462` 四个数字在 proposal.md `:3`、tasks.md `:5`、`detailed-tasks.yaml:66` 三处均一致且与我独立实跑一致; 唯 `1889` 未同步重算。
2. **`a3bfd693`** (handoff 全文对正): **不完整** —— 见上方 finding 1, 四处证据。
3. **`[x]`=24=yaml done 数**: `grep -c '^\s*- \[x\]' tasks.md` = 24; `grep -c '^\s*status: done' detailed-tasks.yaml` = 24; 唯一非 done 条目 `status: in_progress` (TASK-025, 对应 tasks.md 未勾的第 25 条) —— 一致。
4. **B9-补 自纠诚实性**: 决策单 `:108` B9-补 承认「该推送是按『通过后合并』**类推**自授权, 不是字段级匹配」并引 memory `sync≠push-auth`/`exact-exception-condition`, **不撤已推内容** (撤 = 再一次外向动作) 且「自此本审计循环内不再推任何子模块 commit」—— 核对 `git -C aria log --oneline d1caa66 -1` 与 `git -C standards log --oneline ffed204 -1` 仍是 R1 时点的 SHA (R2/R3 均未再推子模块), 符合自述; 措辞未淡化过失 (逐字「接受批评, 自纠」), 与 memory `sync≠push-auth`(「保持同步」≠推送授权, 外向不可撤销须显式确认) 及 `exact-exception-condition`(援引豁免须字段级匹配, 类推不算) 两条一致, 判定**诚实**。

## 核验记录 (逐字命令与关键输出)

### 1. 基础回归 (声称 vs 实测)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
.....................................................
Ran 53 tests in 2.023s
OK

$ cd aria/skills/state-scanner/tests && python3 run_tests.py
Ran 1462 tests in 73.596s
OK

$ grep -rhE '^\s*def test_' aria/skills/state-scanner/tests/*.py | wc -l
1478
$ python3 -c "AST FunctionDef/AsyncFunctionDef count over all test_*.py" → total: 1478   # 与 grep 交叉核一致

$ bash aria/skills/run_all_tests.sh   (~74s, 独立后台跑完)
...
state-scanner                                  OK (1462 tests)
tdd-enforcer/examples/python                   OK (14 tests)
workflow-runner                                OK (38 tests)
──────────────────────────────────────────────
skill 套件: 9 OK / 0 FAIL / 0 SKIP   (累计 1894 个测试)     # ⚠️ 与 tasks.md:5「1889」不符, 见 finding 2
```

53 / 1462 / 1478 三个数字与 CHANGELOG 1.68.1 段、proposal.md `:3`、tasks.md `:5`、`detailed-tasks.yaml` 逐字核对一致; `1889` 不一致 (见上)。

### 2. 53 条抽样恒真性核验 (≥6 条, 新旧混合, 全部对抗性验红, 无一恒真)

方法: `unittest.TestLoader().loadTestsFromName` 精确点名单个测试方法, monkeypatch 目标符号 (`extract_linked_issue_field` 或 `_PROBE` 常量指向的探针脚本副本) 为已知有缺陷的实现, 断言该测试从绿转红; 全程未改动仓内文件, mutant 脚本另存 scratchpad, 通过 symlink `lib/` 保证 sys.path 解析正确 (首次未 symlink 时误判为「路径问题掩盖真实判别力」, 已重做修正)。

| # | 测试 (新/旧) | 坏实现 | 结果 |
|---|---|---|---|
| 1 | `TestSC2TokenStart.test_sc2_markdown_link_form_is_no_token` (旧, v1.68.0) | `_BAD_EXTRACTORS["first_code_span_anywhere"]` | 真实impl PASS → 坏impl **FAIL** (`BAD_TOKEN` != `NO_TOKEN`) |
| 2 | `TestSC3MultiValue.test_sc3b_second_element_invalid_bad_token` (旧) | `_BAD_EXTRACTORS["first_element_only"]` | 真实impl PASS → 坏impl **FAIL** (`OK` != `BAD_TOKEN`) |
| 3 | `TestSC9EmitArg.test_sc9c_real_token_emits_first_element_no_trailing_newline` (旧) | mutant: `emit_arg(fv)` 输出后追加 `\n` | 真实impl PASS → 坏impl **FAIL** (`'10CG/a#1\n' != '10CG/a#1'`) |
| 4 | `TestSC5ProbeHardening.test_allowlist_entry_normalization_and_dedupe` (新, v1.68.1) | mutant: `_normalize_entry` 不去 `./`/尾斜杠 | 真实impl PASS → 坏impl **FAIL** (`FAIL 1 项` != `OK`) |
| 5 | `TestSC5ProbeHardening.test_unreadable_proposal_is_fail_not_crash` (新) | mutant: `except OSError: continue` (静默跳过而非记违规) | 真实impl PASS → 坏impl **FAIL** (`0 != 1`) |
| 6 | `TestSC5ProbeHardening.test_root_positional_with_emit_arg_is_exit2` (新) | mutant: 删除互斥检查 | 真实impl PASS → 坏impl **FAIL** (`0 != 2`) |
| 7 | `TestSC5ProbeHardening.test_check_mode_survives_ascii_stdout` (新) | mutant: 删除 `stdout.reconfigure` | 真实impl PASS → 坏impl **FAIL** (UnicodeEncodeError, `1 != 0`) |
| 8 | `TestSC6Template.test_sc6_template_field_and_usage_note_and_reference` (新, SC-6(iii) 英文化) | mutant: 模板 Usage Notes 段删去 EN/CJK 两组「不留空/不删行」措辞, 保留 `` `none` `` | 真实impl PASS → 坏impl **FAIL** (「缺「不留空 / do not leave」」) |
| 9 | `TestSC5ProbeCheckMode.test_sc5_d_degraded_missing_collision_module_is_skip` (SC-5(d), 见 §3) | mutant: 降级路径误判 `OK (0 份, 0 条)` 而非 `##SKIP##` | 真实impl PASS → 坏impl **FAIL** (`False is not true`) |

9/9 全部判别力成立, 无恒真项。抽样覆盖 old (SC2/SC3/SC9) + new (SC5ProbeHardening ×4 + SC5(d) + SC6) 两类, 超出「≥6 条含新旧」要求。

### 3. SC-5(d) 夹具隔离性独立复现 (两条断言分别验证, 非仅信任 docstring)

断言 (1) —— import 失败精确点名 `lib.collision` (而非旧夹具误炸的 `lib.claim_lifecycle`):
```
# 复现「旧 (pre-R1) 夹具」形态: 只拷 __init__.py + linked_issue_field.py (不拷完整 lib/)
$ python3 -c "import sys; sys.path.insert(0,'<scratch>/old_fixture'); import lib.linked_issue_field"
ModuleNotFoundError: No module named 'lib.claim_lifecycle'      # 不含 "lib.collision" — 证明若测试仍用旧夹具, assertIn("lib.collision", …) 会红, 即该断言确有判别力
```
真实测试 (`test_sc5_d_degraded_missing_collision_module_is_skip`) 在真实仓上执行时用的是新夹具 (拷完整 lib/ 只删 collision.py), 其 import 报错精确点名 `lib.collision` (测试内部子进程验证, 通过) —— 两相对照证实修复真实。

断言 (2) —— 探针对该降级态判 `##SKIP##` 而非 `OK`:
```
mutant: main() 的 import-except 分支从 "print ##SKIP##; return 0" 改为 "print OK (0 份在范围内, 0 条在册); return 0"
$ 用该 mutant 跑 test_sc5_d_degraded_missing_collision_module_is_skip
AssertionError: False is not true   # _first_line(stdout).startswith("##SKIP##") 为 False → 判别力成立
```

### 4. 新 state-check `plugin-version-arch-docs-match` 四态 (含 SKIP, 未改动仓内文件)

```
# STATE OK (scratch 副本, 未改动)
OK plugin=1.68.1 (2 arch doc rows match)   exit=0
# STATE DRIFT (sed 改 scratch 副本 system-architecture.md 版本行)
DRIFT plugin=1.68.1 vs system-architecture.md=1.68.0   exit=1
# STATE MISSING (sed 删 scratch 副本 version-scheme.md aria-plugin 行)
MISSING version-scheme.md aria-plugin 行   exit=1
# STATE SKIP (scratch 副本无 aria/.claude-plugin/plugin.json)
##SKIP## aria/.claude-plugin/plugin.json 不可读   exit=0
```
Parser 确认注册: `_parse... yaml` (`yaml.safe_load` 直读) → `total checks: 14`, `plugin-version-arch-docs-match enabled: True`。

### 5. `--emit-arg` 母 Spec 接缝 (精确字节数)

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py --emit-arg openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md > out.bin
$ wc -c out.bin
13 out.bin
$ od -c out.bin | tail -2
0000000   1   0   C   G   /   A   r   i   a   #   1   7   4
```
13 字节, 精确无尾换行, 与母 Spec `:13` `` `10CG/Aria#174` `` 逐字一致。

### 6. 探针真实语料 + 白名单

```
$ python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt
OK (9 份在范围内, 6 条在册)   exit=0
$ wc -l .aria/linked-issue-field-grandfathered.txt (非注释非空行) → 6 (与探针输出「6 条在册」一致)
```

### 7. AB 产物追注 (RESULT.md / SUBSTITUTE.md)

```
$ grep -n "1457\|1462\|1473\|1478" .../RESULT.md .../SUBSTITUTE.md
RESULT.md:63:  … `Ran 1457` 与静态 `def test_` 1473 差 16 = test_collision.py …
SUBSTITUTE.md:44:Ran 1457 tests in 58.354s
SUBSTITUTE.md:48:1473  # = 基线 1425 + 新增 48; 与 Ran 1457 差 16 …
```
两处均为 AB 跑测当时 (v1.68.0 时点) 的历史值, 正确标注「两数并列不可互换」, 与 CHANGELOG 1.68.1 段的当前值 (53/1462/1478) 不矛盾 (不同时间点各自准确)。
决策单 B8 引 proposal D2「定位谓词=行首depth-1+fence排除+文档序第一条」核对 `proposal.md:491` 逐字存在, RESULT.md §2 第5点引用无误。

### 8. §5 表 diff 精确定位 (finding 1 证据 c/d 的直接来源)

```
$ git show fdfb183 -- docs/handoff/2026-09-02-....md | sed -n '/OpenSpec/,/架构文档/p'
 | OpenSpec | yes | 字段 Spec proposal Status 行 + tasks.md 22/25 + yaml 状态回写; ...   # 未在 diff 中出现 (无 -/+ 前缀), 证明本行 R2 未动
-| Standards / conventions | yes | ... (未推) | ...
+| Standards / conventions | yes | ... ffed204, R1 清账 ... | ...
-| Skill docs | yes | ... `aria/CHANGELOG.md` 1.68.0 |
+| Skill docs | yes | ... `aria/CHANGELOG.md` 1.68.0 + 1.68.1 |
 | Auto-memory | yes | ... | 见 §8 |
 | Decision memos | yes | `...split.md` 追记 §B 期 B1–B7 | 主仓 `989d14c` |   # 未在 diff 中出现, 证明本行 R2 未动
 | Audit reports | yes | ... |
-| CHANGELOG | yes | aria `## [1.68.0] - 2026-09-02` | aria `8eb8876` |
+| CHANGELOG | yes | aria `## [1.68.0]` + `## [1.68.1]` ... |
 | 架构文档 | yes | `system-architecture.md` 2.0.1 | ...   # 未在 diff 中出现, 证明本行 R2 未动
```
确认「§5 三行」= 精确 3 行 (Standards / Skill docs / CHANGELOG), OpenSpec / Decision memos / 架构文档 三行原样未动。

```
$ grep -n "^| B[0-9]\|^| C[0-9]" .aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md | wc -l
16   # B1-B9 + B9-补 + C1-C7 = 16 条目, 远超 handoff 仍写的「B1–B7」
$ grep -n "^> \*\*Version" docs/architecture/system-architecture.md
3:> **Version**: 2.0.2
```

### 9. 工作树核验 (未留改动)

```
$ git status --short && git -C aria status --short && git -C standards status --short
 M aria-orchestrator     # 会话起始既有的有意停泊状态, 非本轮改动
(aria/standards 均干净)
```
所有 mutant / scratch 文件均在 `/tmp/claude-1000/.../scratchpad/pr190/` 下, 未触碰仓内任何文件。
