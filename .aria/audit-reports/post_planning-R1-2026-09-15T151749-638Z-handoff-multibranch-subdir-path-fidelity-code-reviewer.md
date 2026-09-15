---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T17:11:25.801Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer 席 — handoff-multibranch-subdir-path-fidelity

## 审计结论

### 实读范围

- 审计对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` (122 行) 与 `detailed-tasks.yaml` (684 行), 主仓 `07e0a6e`。
- 依据: 同目录 `proposal.md` (按行切片通读 §触点文件清单 / §What 1-7 / §Impact / §Tasks / §SC 表与 SC-15 细则 / rule6_note / §待 owner 复议 1-8); 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (§2 的 10CG/Aria#195 表 8 行 + §5); `aria/skills/task-planner/{SKILL.md,DUAL_LAYER_SPEC.md}`; 先例 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/{tasks.md,detailed-tasks.yaml}`; 归档门 `aria/skills/state-scanner/scripts/lib/{spec_complete.py,carry_forward.py,detailed_tasks.py}`; `aria/skills/openspec-archive/SKILL.md` (Step 1 路由 / Step 2 warn_overlay / Step 7); `aria/skills/phase-d-closer/SKILL.md` D.2; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 1; `standards/conventions/content-integrity.md` §4.4 / §4.5。
- 代码真值 (aria `1cb3872`, 工作树干净): `scripts/collectors/handoff_multibranch.py` 1-120 / 170-760 行, `scripts/writers/latest_md_writer.py` 1-175 / 255-320 行, `scripts/scan.py` 160-215 与 `--project-root` 定义, `scripts/collectors/remote_refresh.py` 405-440, `references/state-snapshot-schema.md` 1068-1171, `references/layer-l-integration.md` 95-110, `tests/test_scan_integration.py` 160-178, `tests/test_p1_layer_h.py` 180-222, `tests/fixtures/freeze_corpus.py`, `tests/run_tests.py`; standards `8b49562` 的 `conventions/session-handoff.md` 第 15 / 88 / 94 / 97 / 171-173 / 301 / 336 行。

### 实跑命令与关键输出 (模拟改动全部在 scratchpad 副本上, 未改仓内任何文件, 一律 `python3 -B`)

1. yaml `metadata.sc11_baseline_predicates` 16 条逐字抽出, 每条包成 `if <谓词>; then echo PASS; else echo FAIL; fi`, cwd = `aria/skills/state-scanner` 实跑: **16 条全部 FAIL** —— 「当前基线全为假」属实。锚点核对: `## Change history` 在 schema:1158 存在; `compound key` 在 schema 仅 :1124 一处; `# Tie-break, finalized` 在 collector:368, 其后首个 `^def ` 是 :402 `_updated_at_sort_key`, 区间不含 `_dedupe_sort_key` 函数体 —— 无恒假锚点。
2. 把 collector / writer / schema / phase-1-collectors / layer-l-integration 五个文件复制到 scratchpad, 按「正确实现」逐项改写后跑同一脚本: **16 条全部 PASS**。另造六份「只改一半 / 措辞不同」副本, 结果见 F-01 / F-02 / F-06。
3. 归档门: tasks.md + yaml 副本全部 `- [ ]` 改 `- [x]`, `sys.path` 插 `aria/skills/state-scanner/scripts` 后 `from lib import spec_complete`, 把 `_find_project_root` 指向 `/home/dev/Aria` 调 `gate_result`: `complete True | verdict warn | blocking []`, 3 条 unverified_claims, `d_payload` 非 None (详见 F-04)。`_CHECKBOX_RE` 与 `_CHECKBOX_ANY_RE` 各识别 25 个 checkbox, parent 集合与 yaml parent 集合完全相等; `_extract_carry_forward_annotations` 对两文件均为 `[]`; `detailed_tasks.parse_detailed_tasks` → `parse_ok True, 32 task(s)`, status 计数 `pending 31 / done 1`; PyYAML `safe_load` 同样解析出 32 个任务。
4. yaml 结构脚本: 32 个任务均含 id / parent / title / status / complexity / est_hours / dependencies / deliverables / agent / reason / verification; parent 全部匹配 `^\d+\.\d+$`; 依赖无悬空 TASK、无环; est_hours 合计 **92.5**, agent 计数 qa-engineer 14 / backend-architect 8 / knowledge-manager 10, 与 metadata 一致; 已存在文件的 deliverables 路径全部存在, 不存在的均为「(新建)」首次出现或由前序任务新建。`est_hours` 数值字段与 `status: done` 偏离 DUAL_LAYER_SPEC 文字, 但与仓内先例 (`est_hours:` 在用, `status: done` 39 处) 及归档门 done-family `{done, completed}` 一致, 不计 finding。
5. metadata / 读前必看表事实复核 (全部属实): `git -C aria diff --stat f314785 1cb3872 -- <proposal 触点表机械导出的 41 路径>` = `8 files changed, 109 insertions(+), 10 deletions(-)`, 类别计数 改写 12 / 改写待定 2 / 新增 1 / 引用 26; `git -C standards diff --stat 21748d4 8b49562 -- conventions/session-handoff.md` 为空; schema 实读 :1072 / :1076 / :1106 / :1110 / :1112 / :1116 / :1120 / :1124 / :1127 / :1128 / :1136 / :1138 / :1158-1171 与偏移表逐项对上; 主仓 16 个版本点实读 15 处为 1.73.3、`VERSION:24` 为 `v1.73.0`; `.aria/state-checks.yaml` 三条 name 在 :124 / :177 / :408; `grep -c 'bare-issue-ref\|check_bare_issue_refs' .aria/state-checks.yaml` = 0; `ab-suite/state-scanner.json` 的 `tracks_multibranch` 仅 :214, `handoff_multibranch` / `legacy` / `basename` 均 0; `docs/handoff` 201 份 .md、子目录 0、非 ASCII 名 0; 两份冻结语料各 996 条、filename 含 `/` 0、非 ASCII 0。
6. 测试计数 (只用 `unittest.TestLoader` 装载计数, 不执行): SC-10 九模块合计 **169**, 其中 `test_collision` = **0** (文件内 28 个顶层 `test_` 函数, 无 TestCase 类); `test_handoff_multibranch_collision_dedupe` 23 / `test_p1_layer_h` 24 / `test_scan_integration` 19 / `test_track_board_advisories` 5; `discover(pattern='test_*.py')` = **1605**; phase-d-closer `tests/test_fetch_gate.py` 静态计 11 个测试函数。`run_tests.py` 用 `discover` 自动收集, 新测试文件会被纳入。
7. yaml 引用的代码行号逐处实读: collector :36 / :42 / :177-178 / :243 / :246-247 / :277-288 / :298 / :301 / :313 / :315 / :321 / :332 / :368 / :396 / :455 / :494 / :586-596 / :619-626 / :637-658 / :665-676 / :683-700, writer :113 / :124 / :143 / :152 / :159 / :164 / :303, scan.py :180-186 / :193 / :209, `test_scan_integration.py:164-166`, `phase-1-collectors.md:102`, `layer-l-integration.md:105`, advanced-rules.md :443-444 / :511-512 / :544, RECOMMENDATION_RULES.md :28 / :30 / :31, phase-d-closer SKILL.md:218 —— 全部与 yaml / tasks.md 描述一致。
8. 引用写法自检: `check_bare_issue_refs.py` 对 tasks.md 与 yaml 均输出「裸 issue 引用: 0」rc=0; content-integrity §4.5 自查命令对两文件无输出。
9. 当前 13 个 `refs/remotes/origin/*` 逐个 `git ls-tree -r --name-only <ref> -- docs/handoff`: 子目录路径 0、带引号路径 0 (用于 F-08)。
10. 事后 `git status` (主仓 / aria / standards) 除他席报告外无变化, `find aria/skills -name '*.pyc' -mmin -120` 为 0。

### Findings

#### F-01 [Major] type=issue · category=testing · scope=metadata.sc11_baseline_predicates / TASK-001 / TASK-019 / TASK-020

**SC-11 谓词里有六条可被「非目标改动」满足; TASK-001 的「基线全 FAIL」只检验了单侧鉴别力。**

证据:
- (l1) `detailed-tasks.yaml:67` 为 `[ "$(grep -c degraded_reason scripts/writers/latest_md_writer.py)" -ge 3 ]`, 计的是整文件行数, 代码行也算。TASK-013 验收 (`detailed-tasks.yaml:327`) 要求「三分派之前初始化 `degraded_reason = None` / `n_active == 1` 支解包覆写 / 返回 dict 无条件带该键」, 这恰好是三行含该 token 的代码。scratch 副本只落这三行代码、`:32` / `:279` / `:287-290` 三处契约文字一字未改: **(l1) PASS**。TASK-020 (`detailed-tasks.yaml:459`) 用「(l1)(l2) 为真」验收三处契约文字, 而 TASK-020 依赖 TASK-013, 进入 TASK-020 时 (l1) 已为真, 对它零信号。`detailed-tasks.yaml:70` 的注释已写明 (j1) 为何只看 docstring (「函数体代码本身会出现 rel_path, 用 grep 整段会被代码满足」), 同一理由没有用到 (l1)。
- (a)(b)(j2)(f1)(f2) `detailed-tasks.yaml:54/55/63/58/59` 都是整文件 grep; TASK-019 (`detailed-tasks.yaml:439`) 自己要求新增的 `## Change history` 行「含 rel_path / unreadable_count」天然带同样的 token。三份 scratch 副本:
  - 只加 yaml 块 `unreadable_count` 字段行 + 一行 Change history, 不改 `:1138` fail-soft 形状、不加 TrackEntry `rel_path` 行 ⇒ `a PASS, b PASS`;
  - 只加一行 Change history「dedupe compound key gains a 5th level `(rel_path == filename, rel_path)`」, `:1124` 仍写 four-level ⇒ `b PASS, j2 PASS`;
  - 只在 Change history 行列出两个新 kind ⇒ `f1 PASS, f2 PASS`。
- proposal SC-11(a) 原文口径是「字段表 + :1136 fail-soft 形状各一」, (b) 是「新增 rel_path 字段行」, (l) 是「:32 / :279 / :287-290 三处各有命中」—— 谓词都丢了定位。

照计划执行会出的错: 漏改 fail-soft 形状 (proposal §4 专门立的「恒存在不变量在错误路径上也要成立」)、漏加 TrackEntry `rel_path` 行、`:1124` 仍写 four-level、writer 三处返回契约文字不改, 这四类漏做都能让对应任务按谓词验收通过 (假绿); TASK-001 按 `detailed-tasks.yaml:109`「任一 PASS 即失去鉴别力」只在基线上跑, 发现不了。

建议改法: (l1) 改成区段 / AST 定位 (模块 docstring `sed -n '1,41p'` 含 `degraded_reason` 且 `write_latest_md` 的 `ast.get_docstring` 含 `degraded_reason`, 与 (j1) 同法); (a) 拆成 `grep -q '^  unreadable_count:'` 与 `grep '^\*\*Fail-soft\*\*' ... | grep -q unreadable_count`; (b) `grep -qE '^  rel_path: +str'`; (j2)(f1)(f2) 先 `grep -v '^|'` 排除表格行。TASK-001 增一步负控: 每条谓词在「只落 Change history 行」「只落代码」两份 scratch 副本上必须 FAIL (memory check-runs-at-baseline-first / adversarial-fixture)。

#### F-02 [Major] type=issue · category=documentation · scope=TASK-019 / TASK-020 / tasks.md:18 / SC-11(j1)(j3)

**改键支的文档同步面只点名三处, 另有五处「四级键 / filename then branch」陈述未列入任何任务, (j) 谓词也看不到。**

证据 (`grep -n 'four-level\|FOUR levels\|four levels\|filename then\|filename, then'` 于 `1cb3872`):
- `handoff_multibranch.py:59-60` 模块 docstring「ties broken by dictionary-max filename then dictionary-max branch (round 3, finding [M1]; fully deterministic, input-order-invariant)」;
- `handoff_multibranch.py:355`「the row that sorts greatest under the four-level key below wins」(在 TASK-020 列的 `:368-399` 区间之外);
- `handoff_multibranch.py:491-492` `dedupe_latest_per_track_container` docstring「ties broken by dictionary-max filename, then dictionary-max branch」;
- `handoff_multibranch.py:716-717` 主循环注释「(filename then branch dictionary-max tie-break, rounds 2/3)」;
- `state-snapshot-schema.md:1134`「it inherits the `(track_id, owner, container)` grouping and the four-level sort key by construction」。

TASK-020 deliverables 注释 (`detailed-tasks.yaml:452`) 只列 `:368-399` 与 `_dedupe_sort_key` docstring; TASK-019 (`detailed-tasks.yaml:437`) 只列 `:1124 / :1127 / :1128`。tasks.md:18「三处文档改写为五级键序说明」沿用的是 proposal 为默认支 (条件化不变量句) 点名的三处, 而改键支要改的是全部键序陈述。上文第 2 项的「正确实现」副本 (其余谓词对应的改动齐备) 在键序陈述上只做了三处: `:370` 与 `:430` 的键元组补 `(rel_path == filename, rel_path)`、schema `:1124` 改 five-level —— 16 条谓词全 PASS, 同时 `grep -ciE 'four-level|four levels'` 在 collector 仍命中 3 行 (含 `:368`「the sort key is FOUR levels」锚点行本身与 `:429`「four levels」docstring 首行)、schema 仍命中 1 行 —— (j1)(j3) 只验 `rel_path` 出现, 不验「four」消失。

照计划执行会出的错: 发版后 collector docstring / 注释与 schema 各留下与实现矛盾的「四级键」陈述 (Rule #3), SC-11(j) 全绿。

建议改法: TASK-020 补 `:59-60 / :355 / :491-492 / :716-717` (`:95` 的轮次史可补一句第 5 级), TASK-019 补 `:1134`, tasks.md:18「三处」改为逐处点名; SC-11 追加负向谓词 `! grep -qiE 'four-level|four levels' scripts/collectors/handoff_multibranch.py references/state-snapshot-schema.md` —— 本席实跑: `1cb3872` 上 FAIL (collector 3 / schema 2), 上述副本上仍 FAIL, 有鉴别力。

#### F-03 [Major] type=issue · category=testing · scope=TASK-026 / metadata.rule6_note

**AB 前后的协调 ref 核验量错了对象, 且漏掉 AB 运维手册的两个必做步骤。**

证据:
- `detailed-tasks.yaml:565` TASK-026「AB 开跑前与结束后各取 `git rev-parse refs/aria/coordination`, 两值相同」; `detailed-tasks.yaml:82` rule6_note「AB 前后 refs/aria/coordination SHA 不变」。
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:224` 把 `state-scanner.json` 列为会触达 `phase1_gate` 的套件 (该套件 :201 / :214 两题即协调场景); :226「两个 CLI 读到它就跳过 push, claim 只写本地 ref」; :227 步骤 2 要求核验 transcript 含 `"push_skipped": true, "push_skipped_reason": "env_var"`; :228 步骤 3「事后清理 (必做)」`git fetch origin +refs/aria/coordination:refs/aria/coordination`。
- `1cb3872` 起 scan 的 Fetch 2 带目标 refspec (`remote_refresh.py:422-425`, 非强制), 每次扫描都会把本地 `refs/aria/coordination` 快进到远端 (`state-snapshot-schema.md:1062` / `:1066`)。
- `grep -n 'push_skipped\|+refs/aria/coordination\|AB_TEST_OPERATIONS\|ls-remote origin refs/aria' detailed-tasks.yaml tasks.md` → rc=1, 无命中。

照计划执行会出的错: eval 触达 phase1_gate / release_gate 且 NO_PUSH 正确生效时, 按手册 :226 本地 ref 会被合成 claim 改写; 并发容器更新远端时, 任一次扫描也会把本地 ref 快进 ⇒「两值相同」预期不成立 (假红), 计划没给处置; 真正该做的 transcript 核验与强制对齐不在计划里 ⇒ 合成 claim 留在本地 ref, 下一次正常会话 fetch 被 non-FF 拒绝后, push 会把它们带上生产协调 ref (手册 :224 记录的 2026-08-02 事故形态)。

建议改法: TASK-026 验收改为 (1) 开跑前 `git ls-remote origin refs/aria/coordination` 与本地一致 (本容器自己的 claim 已推送); (2) 每条 phase1_gate / release_gate 输出含 `push_skipped: true` 与 `env_var`; (3) 结束后远端 ref 若有变化, 逐 commit 核对作者容器不属 AB 会话; (4) 执行手册步骤 3 强制对齐本地 ref, 命令与前后 SHA 落台账。rule6_note 的「SHA 不变」同步改为远端口径。

#### F-04 [Major] type=issue · category=implementation · scope=TASK-032 / tasks.md 2.2 · 4.3 · 4.4 · 5.4

**按当前 tasks.md 措辞, D.2 归档门会判 verdict=warn 并自动开 Forgejo tracker issue; TASK-032 只验 complete, 没有规划这一步。**

证据 (实跑命令见上文第 3 项): 全部勾选后的 `gate_result` = `complete True | verdict warn | blocking []`, unverified_claims 三条:
- tasks.md:64 (2.2) 含「调用方」, 命中 `spec_complete.py:325` 的 `调用`; 行内反引号 `HEALTHY_TRACKS` 被抽为符号且只存在于 tests/ ⇒ `symbol 'HEALTHY_TRACKS' unclassified reference form` (同批 `scan` / `rel_path` / `filename` / `handoff_multibranch` 均判 alive, 无 block);
- tasks.md:82 (4.4) 的 `references/layer-l-integration.md` 文件名含 integration, 命中 `spec_complete.py:324`, 行内与 TASK-023 deliverables 均无代码扩展名 ⇒ `no extractable symbol (fail-soft)`;
- tasks.md:81 (4.3)「活体 dogfood」命中 `_DOGFOOD_BENCHMARK_DEPLOY_KEYWORDS`, 行内无 ab-results 路径 ⇒ `dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在`。

`openspec-archive/SKILL.md:138` 对 `complete=true ∧ verdict=warn` 放行但写 frontmatter unverified_claims (:196); :282-293 Step 7 在 `d_payload != null` 时按 headless 默认执行, 不看 ack, 经 :344-345 `forgejo POST` 创建「[Archive Tracker] {spec_id} — 归档残留待办」。`detailed-tasks.yaml:681` TASK-032 验收只写「归档门 (spec_complete.py) 判 complete」; `detailed-tasks.yaml:75` hard_constraints「外向动作 (推送 / 开 issue / 回帖) 执行前逐项请 owner 授权」。

照计划执行会出的错: D.2 时归档的 proposal.md 被写入 3 条 unverified_claims, 并在 10CG/Aria 自动开一张内容以措辞噪声为主的 tracker issue —— 计划外、未经逐项授权的外向动作; 若执行者守 hard_constraints, 则在 Step 7 卡住, 计划没有处置。

建议改法: TASK-032 验收补「归档前先跑 `spec_complete.py --gate` 预演, 记录 verdict 与 unverified_claims 清单并逐条写 ack 理由; Step 7 建 issue 列为外向动作, 事先取得 owner 授权或按预演结果决定」。不建议为过检查器改写 2.2 / 4.4 措辞 (memory author-to-match-checker); 4.3 可在勾选时补台账段落指针, 并在预期里写明 warn 来源。

#### F-05 [Major] type=issue · category=documentation · scope=TASK-025 / TASK-023 / tasks.md:20 · tasks.md:40

**两处文字承诺「并入 5.3 的 issue」, TASK-025 的正文清单没有承接。**

证据: tasks.md:40 范围边界「`handoff.py` 子目录支持 / `handoff-mechanics.md:114-124` 处方表 / mv 日语义 / `reference-snapshot-aria.json` 重采样 / schema `errors[].tracks[]` 形状 … 统一登记进 5.3 的 issue」; tasks.md:20 与 `detailed-tasks.yaml:511` (TASK-023) 要写进共享 standards SOT 的措辞「本 cycle 不同步 (owner 2026-09-12 裁定), 缺口并入遗留 issue」, 其对象是 AI 手改路径 (`handoff-mechanics.md`) 未同步第三态。`detailed-tasks.yaml:549` TASK-025 正文清单为 handoff.py 两函数 + (a)–(f) + session-handoff.md:97「自动」+ 子目录布局锚点 + exists 矛盾, 不含上述手改路径缺口, 也不含 mv 日语义。`grep -n 'mv 日\|mv 过\|handoff-mechanics' detailed-tasks.yaml` 只命中 :48 (rulings_applied) 与 :589 (CHANGELOG 已知边界)。

照计划执行会出的错: 执行者按 yaml (verification 的单一 SOT) 开单, issue 缺这两项; `standards/conventions/session-handoff.md` 新增的「缺口并入遗留 issue」指向一张不含该缺口的单 —— 悬空的跨文档承诺落在共享子模块里。

建议改法: TASK-025 清单补一条「handoff-mechanics.md:114-124 手改路径未同步第三态 (须与 handoff.py 子目录支持同做才自洽, 决策单 §2 第 2 行第 (4) 问)」; mv 日语义二选一: 补进清单, 或把 tasks.md:40 改为「由 CHANGELOG 已知边界承载, 不进 issue」(决策单 §2 第 5 行只要求 CHANGELOG)。

#### F-06 [Minor] type=risk · category=testing · scope=SC-11(i) / SC-11(k1)

**(i) 与 (k1) 在语义正确的实现下会假红。**

证据: 在「正确实现」副本上把 Change history 行写成「legacy track_id `legacy:<branch>:<filename>` → `legacy:<branch>:<rel_path>`」⇒ `i FAIL` (其余 15 条 PASS); 另一份副本保留 writer docstring 中仍然为真的「when the filename cannot be determined」, 再补上第二个原因 `target_in_subdir` ⇒ `k1 FAIL` (`k2 PASS`, `l1 PASS`)。

照计划执行会出的错: 执行者为让谓词转绿去改写本来正确的措辞。

建议改法: (i) 同样先 `grep -v '^|'` 排除 Change history 表行; (k1) 按 proposal 原意改判为「该 docstring 不再把缺 filename 写成唯一原因」, 例如要求同一段同时含 `target_in_subdir`。

#### F-07 [Minor] type=issue · category=documentation · scope=tasks.md:110 · tasks.md:80 · tasks.md:58

**SC 映射表的 SC-11 行与任务归属对不上。**

证据: tasks.md:110 SC-11 行「钉测 / 反事实 = 5.6」, 而 5.6 (TASK-028) 是 content-integrity §4.4 / §4.5 写法自检, 与 SC-11 文档同步机检无关, 全计划也没有一次对 16 条谓词的全量复跑; SC-11(c1)(c2) 在 `detailed-tasks.yaml:258` 归 TASK-009 (2.1), 表的「转绿」列没有 2.1, tasks.md:80 (4.2) 反而写「SC-11 (c)(j)(l)」; SC-11(d)(h) 由 5.4 产出 (tasks.md:90), (d) 的 issue 正文由 5.3 产出, 表中都未列。另 tasks.md:58「yaml TASK-001 列出的 SC-11 grep 判据」实际放在 `metadata.sc11_baseline_predicates`。

照计划执行会出的错: 按映射表找「谁负责 SC-11(c)」会找到 4.2 而不是 2.1; 5.6 勾完即被当成 SC-11 已钉测。

建议改法: 钉测列改为「4.3 (TASK-021 复跑全部谓词)」; 转绿列补 `2.1 (c)`、`5.3 / 5.4 (d)(h)`; 4.2 行删去 (c); 1.3 行改指 metadata。

#### F-08 [Minor] type=issue · category=testing · scope=TASK-002 / TASK-022

**TASK-002 的前置核验一条恒真、两条范围不对。**

证据: `detailed-tasks.yaml:126`「冻结语料 filename 含 / 的行数 = 0」恒真 —— 两份语料由旧 collector 产出, filename 取 `Path(path).name` (`handoff_multibranch.py:277`), 结构上不可能含 `/`; 本席实测两份各 996 条且 legacy 行为 0。`:124` / `:125` 只看工作树的 `docs/handoff`, 而 collector 与 SC-12a 扫的是全部 `refs/remotes/origin/*` (cap 20)。本席对当前 13 个 origin ref 逐个 ls-tree: 子目录 0、带引号 0 —— 前提今天成立, 不是现存损坏, 是判据测不到。另 `:127` 写「三条命令」, 第三条没有给命令。

照计划执行会出的错: 若将来某条远端分支带子目录或非 ASCII 名, TASK-002 仍全过, 到 TASK-022 才以 SC-12a「零差异」假红的形式暴露。

建议改法: 第三条改为对 TASK-022 冻结的同一 ref 集逐个 `git ls-tree -r --name-only <ref> -- docs/handoff`, 断言无 `docs/handoff/.*/` 与 `^"` 行, 命令落台账。

#### F-09 [Minor] type=issue · category=documentation · scope=TASK-028

**写法自检排在最后一批新写文字之前。**

证据: TASK-028 依赖 TASK-027 (`detailed-tasks.yaml:600`), 其后仍有新写文字: TASK-029 / TASK-031 的台账追加 (`:625` / `:664`)、TASK-030 的主仓 CLAUDE.md 与 README 版本点、TASK-031 的 PR 正文、TASK-032 的周期 handoff 与 10CG/Aria#195 回帖 (含 TASK-025 issue 引用)。`detailed-tasks.yaml:81` 的约束对象是「本 cycle 新写或改动的文字」全部。

照计划执行会出的错: 最后写的 handoff 与回帖不在自检范围内。

建议改法: 自检分两次 (子模块合并前 + D.3 handoff 落盘前), 或把自检项并入 TASK-031 / TASK-032 验收。

#### F-10 [Minor] type=issue · category=testing · scope=TASK-026 / TASK-027

**AB 可能不在 ship 内容上跑; 结果目录名依赖尚未算出的版本号。**

证据: 本席对依赖图求传递闭包, TASK-026 的祖先集不含 TASK-023; TASK-023 改 `aria/skills/state-scanner/references/layer-l-integration.md`, 该文件由 state-scanner `SKILL.md:192` / `:194` 链接。TASK-026 deliverable 目录名含 `v<vNEXT>` (`detailed-tasks.yaml:562`), 号在其后的 TASK-027 才计算 (`:586`); 并发轨 10CG/Aria#199 若先 ship, 预估的号会作废。

照计划执行会出的错: AB 结果对应的是缺一处 reference 改动的 skill; 目录名与最终发版号可能不一致, 事后按版本追溯 Rule #6 证据会对错目录。

建议改法: TASK-026 依赖加 TASK-023; 取号 (只算不 bump) 前移到 TASK-026 之前, 或目录名在 TASK-027 后按实际号重命名并记台账。

#### F-11 [Minor] type=risk · category=testing · scope=TASK-024 / metadata.rule6_note

**TASK-024 若改到 phase-d-closer SKILL.md, AB 范围扩展没有落点。**

证据: TASK-024 复核清单含 `aria/skills/phase-d-closer/SKILL.md:218` (`detailed-tasks.yaml:529`); rule6_note (`:82`) 升判据表第二行的条件只点名 advanced-rules.md / RECOMMENDATION_RULES.md; TASK-026 标题固定为 state-scanner AB。proposal rule6_note「不豁免的部分」写明改 SKILL.md 指令面时 AB 扩到 phase-d-closer / session-closer。

照计划执行会出的错: 该处若落编辑, 执行者按 yaml 只跑 state-scanner AB。

建议改法: rule6_note 与 TASK-024 验收补「phase-d-closer/SKILL.md 落编辑 ⇒ 追加 phase-d-closer AB, 并在 TASK-026 之前插入对应任务」。

#### F-12 [Minor] type=issue · category=testing · scope=tasks.md:91 (5.5) / TASK-032

**5.5 行的产物抽验永远通过。**

证据: 同一次 gate 模拟里, 5.5 行 `classify_artifact_claim` 返回 `verified=True, reason='linked artifact exists: aria-plugin-benchmarks/ab-results/'`; 行内只写了恒存在的父目录 (`spec_complete.py:1140` 的 `_ARTIFACT_PATH_TOKEN_RE` 抽到的就是它)。

照计划执行会出的错: AB 结果目录缺失时, 归档门对该声称也放行 (漏检)。

建议改法: 勾选 5.5 时把 TASK-026 的具体结果目录路径写进该行, 使抽验对象是真实产物。

#### F-13 [Minor] type=risk · category=testing · scope=TASK-026

**AB 基线臂的可读语料没有隔离。**

证据: AB 在真仓无沙箱里跑 (`AB_TEST_OPERATIONS.md:224`); 仓内 `openspec/changes/handoff-multibranch-subdir-path-fidelity/` 的 proposal.md / tasks.md 与 B 期新建的 verification-ledger.md 逐条描述目标行为; TASK-026 只约束「基线臂的输入取旧代码的输出」(`detailed-tasks.yaml:566`)。缺的证据: 本席未实跑 AB, 不能断言基线臂一定会读到这些文件。

照计划执行会出的错 (若发生): 基线臂从在制文档学到新行为, 区分力被低估, 结论不可比。

建议改法: RESULT.md 把区分力结论按「落地前已证 / ship 态边际」分开写 (memory ab-baseline-leaks-via-repo-corpus), 或基线臂在不含本 change 目录的一次性 worktree 里跑。

### 核对无误的部分 (不计 finding)

- 读前必看表 11 行与 proposal 原文、决策单 §2 第 1-8 行及 §5 逐条对上: 第 4 行附问取改键支、第 5 行 mv 日只进 CHANGELOG、第 2 行第 (2)(4) 问、第 6 行 MINOR、第 7 行 Level 3 不拆; 编号 2.0a / 2.0b 并入 2.0、5.4a → 5.6 的理由 (`_CHECKBOX_ANY_RE` 的 parent 组要求数字后跟空白) 属实。
- 第 5 级键字面 `(bucket, dt, filename, branch, (rel == filename, rel))` 在 `max()` 下「顶层优先、其余字典序取大、缺键按 filename」成立; 对 `TestDedupeTiebreakByBranchWhenUpdatedAtAndFilenameTie` 与冻结语料 (无 `rel_path`) 各行第 5 级恒为 `(True, filename)`, 不改变既有胜者; TASK-005 排序键用例在四级键下反序输入确实换赢家 (`max()` 取首个最大值, `handoff_multibranch.py:541`)。
- 依赖顺序与 tasks.md 组 5 标题的执行序一致 (5.3 / 5.5 并行, 其余串行); 2.5 的守卫排在产出 `rel_path` 的 2.2 之后; 同文件任务均串行。
- 归档门: 全部勾选后 `complete=True`, 无 carry-forward 注释, 2.2 的集成声称符号不会判 dead, 不会误 BLOCK。

## Verdict

0 Critical / 5 Major / 8 Minor ⇒ **PASS_WITH_WARNINGS**。

## Vote

**REVISE** —— 5 条 Major 集中在三类: 验收谓词对「只改一半」无鉴别力 (F-01、F-02)、执行面漏了运维手册必做步骤与归档门的外向副作用 (F-03、F-04)、跨文档承诺在 issue 清单里没有承接 (F-05)。均可在 tasks.md / yaml 内修订, 不涉及 proposal 设计取舍。

## 轮次记录

Round 1 (code-reviewer, convergence): REVISE — 0C/5M/8m; 16 条谓词基线全 FAIL 属实但六条可被非目标改动满足; 改键支漏列五处四级键陈述; AB 协调 ref 核验量错对象且漏手册必做清理; D.2 预演得 verdict=warn 并会自动建 tracker; TASK-025 未承接两处「并入 issue」承诺。
