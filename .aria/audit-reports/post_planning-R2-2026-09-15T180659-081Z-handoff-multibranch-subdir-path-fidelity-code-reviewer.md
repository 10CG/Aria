---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T19:34:34.788Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer 席 — handoff-multibranch-subdir-path-fidelity (A.2/A.3 v2 `0f50239`)

## 审计结论

### 实读范围

- 审计对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` (145 行) / `detailed-tasks.yaml` (783 行) / `sc11-predicate-validation.py` (123 行), 主仓 master `0f50239` (本地未推送)。
- 依据: R1 聚合报告 (处置表 PP1-M1..M13 / m1..m14) 与本席 R1 报告 F-01..F-13; `git diff 07e0a6e 0f50239 -- <change 目录>` 全文 (tasks.md 127 行变动 / yaml 413 行变动 / 验证脚本新增); proposal.md 按行切片读 :9 / :21 / :152 / :308 / :320 / :322 / :326 / :330-331 / :353 / :368-386 / :403-407 / :415-433 (SC-1..SC-18 行); 决策单 2026-09-12 §2 的 10CG/Aria#195 表 8 行、§3、§5; 决策单 2026-09-07 「落地约束」节 (:56-61); `aria/skills/task-planner/DUAL_LAYER_SPEC.md`; `aria/skills/openspec-archive/SKILL.md` Step 1-4 / Step 7; `aria/skills/phase-d-closer/SKILL.md` :41-43 / :65 / :210-225; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` :196-240 / :552-556; `standards/conventions/content-integrity.md` §4.4 / §4.5。
- 代码真值 (aria `1cb3872`, 工作树干净): `scripts/collectors/handoff_multibranch.py` 1-130 / 170-756 行; `scripts/writers/latest_md_writer.py` 1-60 / 100-175 / 255-320 行; `references/state-snapshot-schema.md` :1066-1138 (含 :1081 / :1105 / :1124 / :1128 / :1134 / :1138 / :1158 锚点); `references/phase-1-collectors.md:102`; `references/layer-l-integration.md` :95-110; `scripts/renderers/track_board.py` :50-80 / :736-760; `scripts/lib/spec_complete.py` :180-430 / :775-806 / :1125-1340 / :1565-1823; `phase-d-closer/references/handoff-mechanics.md` :112-125。
- 未读取同轮其他席位的 R2 报告 (保持独立)。

### 实跑命令与关键输出 (模拟改动一律在 scratchpad 副本上; 一律 `python3 -B`)

1. 用 PyYAML 从 yaml `metadata.sc11_baseline_predicates` 逐字抽出 19 条 (标签 a1 a2 b c1 c2 f1 f2 g i1 i2 j1 j2 j3 j4 j5 k l1 l2 l3), 每条包成 `if <谓词>; then echo PASS; else echo FAIL; fi`, cwd = `aria/skills/state-scanner`: **19 条全部 FAIL**, stderr 为空 —— 基线全假属实。
2. `python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py` → 矩阵与 yaml:88-108 `measured_2026_09_15_at_1cb3872` 逐格一致, rc=0; 用 `ast` 取出脚本 `PRED` 字典与 yaml 抽出的 19 条逐字比较: 键序与内容完全相同。
3. 本席自建 6 份副本 (复用脚本内的 `rep` / `code_changes` / `collector_docs` / `writer_docs` / `schema_docs` 等函数, 另写改动):

   ```
   pred  target  alt_j3_anchor  alt_j2_anchor  alt_j5_reflow  bad_a2_prose_only  bad_scenarios_missing
   j2    PASS    PASS           FAIL           PASS           PASS               PASS
   j3    PASS    FAIL           PASS           PASS           PASS               PASS
   j5    PASS    PASS           PASS           FAIL           PASS               PASS
   a2    PASS    PASS           PASS           PASS           PASS               PASS
   l1    PASS    PASS           PASS           PASS           PASS               PASS
   (其余 14 条在 6 份副本上均 PASS)
   ```

   `alt_*` = 语义正确但与脚本不同的写法 (假红检验); `bad_a2_prose_only` / `bad_scenarios_missing` = 脚本没模拟过的漏改 (漏检检验), 详见 N-01 / N-07 / N-08。
4. 对 N-01 的建议谓词做三态: 基线 FAIL / 脚本 target PASS / bad_a2_prose_only FAIL。
5. 复制验证脚本, 仅把 `PRED["a2"]` 换回 v1 的整文件形态 `grep -q unreadable_count references/state-snapshot-schema.md` 后运行: a2 在 bad_changelog 与 bad_partial 两列变 PASS, **`mutant rc=0`** (N-02)。
6. 归档门: change 目录复制到 scratchpad 的 `openspec/changes/` 结构下, `sed -i 's/^- \[ \]/- [x]/' tasks.md` (26 个全勾, 0 个未勾), `sys.path.insert(0, "aria/skills/state-scanner/scripts")` 后 `from lib import spec_complete`, 把 `_find_project_root` 指向 `/home/dev/Aria`, 调 `gate_result`: `complete: True | tasks.md 全 [x] (26 task(s), 无 carry-forward/defer 注释)` / `verdict: warn` / `blocking: []` / unverified_claims 3 条 (2.2 行 `symbol 'HEALTHY_TRACKS' unclassified reference form`; 4.4 行 `no extractable symbol (fail-soft)`; 4.3 行 `dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在`) / `d_payload` 非 None (deferred 0 / unverified 3) / `soft_errors: []`; `_iter_task_items` 26 项, parent 集合 1.1..5.6 与 yaml 26 个 parent 相等; 含集成关键词的勾选行只有 2.2 / 4.4。另在当前真实目录只读跑 TASK-032 的 CLI 原句 `python3 -B aria/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/handoff-multibranch-subdir-path-fidelity`: rc=0, JSON 合法 (`complete False / verdict pass`, 25/26 unchecked), 前后 git status 不变。
7. `classify_artifact_claim` 对 5.5 行三种形态 (原样 / 占位括号换成具体目录 / 父目录 token 一并替换) 实跑, 结果见 N-06。
8. SC-5 基线探针: scratchpad hermetic 仓 (顶层一份带 frontmatter 的 .md, `git update-ref refs/remotes/origin/master HEAD`, `GIT_CONFIG_GLOBAL=/dev/null`), monkeypatch `_read_file_content` 返回错误, 用 1cb3872 collector 实跑, 输出见 N-04。
9. yaml 结构脚本: 34 任务, 必需字段齐; parent 全部匹配 `^\d+\.\d+$`; 依赖无悬空、无环; `est_hours` 合计 100.0; agent 计数 qa-engineer 14 / backend-architect 10 / knowledge-manager 10 —— 与 metadata 一致; 传递闭包下 (TASK-033, TASK-019) / (TASK-033, TASK-020) / (TASK-033, TASK-023) 均无序, (TASK-033, TASK-024) 有序, (TASK-025, TASK-026) 无序。`detailed_tasks.parse_detailed_tasks` → `parse_ok True, 34 task(s) parsed` (pending 33 / done 1); 两文件 carry-forward 注释均为 `[]`。
10. 写法自检: `check_bare_issue_refs.py` 对三份文件均输出「裸 issue 引用: 0」rc=0; content-integrity §4.5 自查命令对三份文件无输出; 逐字符扫描: 字面 U+FFFD 0 行、C0/C1 控制字符 0、希腊字母 0、CRLF 0。
11. 跨仓 diff 演示: 主仓 `git diff 1b9734a~1 1b9734a -- aria/CHANGELOG.md | wc -l` = 0 (该提交 gitlink fcbc8ac→1cb3872); `git -C aria diff fcbc8ac 1cb3872 -- CHANGELOG.md | wc -l` = 41; 主仓 `git diff 1cb3872 -- <两份冻结语料路径>` → `fatal: bad revision '1cb3872'` rc=128 (N-10)。
12. `git log --oneline origin/master..master` = 0f50239 / 07e0a6e; `git ls-tree -r --name-only origin/master -- openspec/changes/handoff-multibranch-subdir-path-fidelity/` 只有 proposal.md (N-11)。
13. 偏移复核: `git -C aria diff -U0 f314785 1cb3872` 对 schema 为 `@@ -1062 +1062` / `@@ -1064 +1064,3` / `@@ -1168,0 +1171`, layer-l `@@ -84,0 +85,2`, phase-1-collectors `@@ -59 +59`; CHANGELOG `grep -n '^## \[1.70.0\]'` = :200, 其下 Fixed / Added / Changed 在 :202 / :209 / :215 —— 与读前必看第 8 条、`shifts.changelog_md` 一致。
14. 事后: 主仓 `git status --short` 仅有他席 R2 报告; aria / standards 工作树干净; `find aria/skills/state-scanner aria/skills/openspec-archive -name '*.pyc' -newer <本席首个 scratch 文件>` 无输出; `refs/aria/coordination` 仍为 `4fd07f9` (与 metadata.claim 一致)。

### R1 处置落地核验 (本席 R1 F-01..F-13)

| 本席 R1 | 并入簇 | 处置声称的改法 | 落地与否 | 证据 |
|---|---|---|---|---|
| F-01 | PP1-M2 | 谓词定位到目标行 + 五份副本三态实跑 | 落地, 有残留 | yaml:65-83 全部改为区段 / AST / 非表格行定位; 脚本矩阵复现一致。残留: (a2) 仍可被同一 Fail-soft 行的散文满足 (N-01); (l1) 不覆盖 Scenarios (N-08)。(a2) 与 (l1) 的现形态正是本席 R1 建议的写法, 本席 R1 建议本身不够, 此处更正 |
| F-02 | PP1-M1 | TASK-020 补 collector 五处、TASK-019 补 schema :1134, 新增 (j4)(j5), 读前必看第 1 条逐处点名 | 落地 | yaml:498 (:1134) / yaml:513 与 :518 (:58-61 / :93-96 / :355 / :490-492 / :716-717) / tasks.md:18; 全 state-scanner 非测试文件 grep `four-level\|four levels\|dictionary-max\|filename then branch` 只命中 collector 与 schema, 「整类」边界成立 |
| F-03 | PP1-M7 | TASK-026 按手册场景 1 三步; rule6_note 删「SHA 不变」 | 落地 | yaml:631-633 与 AB_TEST_OPERATIONS.md:226-228 的 env 名 / `"push_skipped": true, "push_skipped_reason": "env_var"` / `git fetch origin +refs/aria/coordination:refs/aria/coordination` 字面一致; yaml:121 已改指 TASK-026 |
| F-04 | PP1-M5 | TASK-032 归档前只读预演 + Step 7 列入外向授权 + 不改写措辞 | 落地, 有残留 | yaml:775-776 / hard_constraints yaml:113。残留: 预演来源只写 4.3 / 4.4, 实测 3 条 (N-05) |
| F-05 | PP1-M6 | TASK-025 加 (g); mv 日语义只进 CHANGELOG; 范围边界表同步 | 落地 | yaml:614-615; tasks.md:61-62 |
| F-06 | PP1-M2 | (i) 拆 (i1)(i2), (k) 改为正向判据 | 落地 | 脚本 target 的 Change history 行含旧公式、writer docstring 保留 "when the filename cannot be" ⇒ i1 / i2 / k 均 PASS, 假红消除 |
| F-07 | m8 | SC 映射表 SC-11 行归属 | 落地 | tasks.md:133 与 yaml:63-64 归属注释、各 TASK「为真」声明逐项一致 (见下文「核对无误」) |
| F-08 | m13 | TASK-002 命令 3 覆盖 ref 集, 命令 4 注明结构性成立 | 落地 | yaml:165-166 |
| F-09 | m11 | 写法自检分两次 | 部分落地 | PR 正文 (TASK-031)、主仓同步面文字 (TASK-030) 在第二次自检前已发布 / 合并; RESULT.md 与套件缺口 issue 两次都不覆盖 (N-13) |
| F-10 | PP1-M4 / PP1-M7 | TASK-026 依赖补 TASK-023; 目录名不含版本号 | 落地 | yaml:626 / yaml:628 |
| F-11 | PP1-M7 | phase-d-closer 落编辑 ⇒ AB 追加 | 落地 | yaml:121 / yaml:595; `aria-plugin-benchmarks/ab-suite/phase-d-closer.json` 存在, 追加有落点 |
| F-12 | PP1-M5 | 勾选 5.5 时写入具体目录 | 落地但改法不充分 | 按最字面做法 (填占位括号) 抽验仍恒过 (N-06) |
| F-13 | PP1-M7 | RESULT.md 区分力按「落地前已证 / ship 态边际」分写 | 落地 | yaml:634 |

### 实施者试派生 (只看 yaml 的 TASK-001 / 019 / 020 / 028 / 032 与其引用文件)

- **TASK-001**: 41 触点导出、两份 diff、19 条谓词形态均可照做, 行号与命令实跑可复现。卡点: 「先重跑验证脚本, 三态不符先修谓词」依赖脚本退出码, 而退出码只核 3 列 (N-02); 主仓 feature 分支「从 origin/master 起」在 A.2/A.3 提交未推送时不可照做, 且取 SHA 未要求 fetch (N-11)。
- **TASK-019**: 字段块 :1081-1103、TrackEntry :1105-1113、:1116 / :1124 / :1128 / :1134 / :1138 / :1158 逐处实读对得上, 可无歧义落笔。判完成时 (a2) 对「只改散文不改形状」无鉴别力 (N-01); 改写 :1124 时若换掉 "compound key" 字样, (j2) 假红且无处置口径 (N-07); 与 TASK-033 无序 (N-03)。
- **TASK-020**: 行号表 (按冻结基线) 与 authoring_rules 足够落笔; (j5) 的行邻接约束已成文。卡点: 与 TASK-033 同文件却无依赖边 (N-03); 注释块首行若去掉 "finalized", (j3) 假红 (N-07)。
- **TASK-028**: 范围与检查项清楚; 主仓侧「本 cycle diff」的基线 SHA 未指明, PR 正文 / RESULT.md 不在范围 (N-13)。
- **TASK-032**: 预演命令原句实跑可用; 预期来源少一条 (N-05); 归档 `git mv` 之后三个子步骤「记台账」的路径未定义 (N-12)。

### Findings

#### N-01 [Major] type=issue · category=testing · scope=metadata.sc11_baseline_predicates (a2) yaml:66 / TASK-019 yaml:495 与 :499 · v2 返工引入: 是

**证据**:
- yaml:66 `(a2) grep '^\*\*Fail-soft\*\*' references/state-snapshot-schema.md | grep -q unreadable_count` 按整行匹配。schema:1138 这一行同时承载形状 dict 与散文「Per-branch `git ls-tree` / `git show` / `git log` failures are accumulated into the track's own `errors` and do not abort the scan of other branches.」(实读)。
- TASK-019 yaml:499 要求「写明 git show 失败不再产生 legacy 行」; :1138 这句散文在实现后本身就过期 (git show 失败改走 soft_error + `unreadable_count`), 是最自然的落笔处。
- 副本 `bad_a2_prose_only`: 除 a2 的形状编辑外与脚本 target 相同, 另把该句改为「... a `git show` failure no longer yields a legacy row — it is reported as a soft_error and counted in `unreadable_count`.」⇒ 19 条谓词全部 PASS, 其中 **a2 PASS**; 而形状 dict 仍是 `{"exists": false, "tracks": [], "branches_scanned": 0, "legacy_count": 0, "collision": {"kind": "none", "groups": []}, "errors": [...]}`。
- 验证脚本 bad_partial 对 a2 的模拟是整句不改 (script:86 `skip=("a2", ...)`), 不是这个真实坏形态, 故矩阵测不到 (memory adversarial-fixture: 坏实现须像真实坏情形)。

**照计划执行会出的错**: 漏补 fail-soft 形状 (proposal §4 / TASK-012 立的「恒存在不变量在错误路径上也成立」的文档面) 时, TASK-019 / TASK-021 / TASK-029 全部按 (a2) 验收通过 —— R1 PP1-M2 要堵的假绿在最可能出现的写法下仍在。

**建议改法**: 定位到反引号内的形状 dict (本席三态实跑: 基线 FAIL / 脚本 target PASS / bad_a2_prose_only FAIL):

```
grep '^\*\*Fail-soft\*\*: branch-list' references/state-snapshot-schema.md | grep -oE '→ `\{[^`]*\}`' | grep -q '"unreadable_count": 0'
```

同时把 bad_a2_prose_only 形态加入验证脚本的坏态。

#### N-02 [Major] type=issue · category=testing · scope=sc11-predicate-validation.py:121-123 / TASK-001 yaml:148 / metadata.sc11_predicate_validation.expected yaml:87 · v2 返工引入: 是

**证据**:
- script:122 `bad = [k for k in PRED if not (res["base"][k] == "FAIL" and res["target"][k] == "PASS" and res["bad_codeonly"][k] == "FAIL")]`, :123 `sys.exit(1 if bad else 0)` —— 退出码只核 5 列中的 3 列; yaml:87 与脚本 docstring :7-13 另声明了 bad_changelog_only / bad_partial 两列的期望。
- 变异实验 (实跑命令第 5 项): 只把 (a2) 换回 R1 PP1-M2 判为假绿的整文件形态, a2 在两列与 expected 相反, **退出码仍为 0**。
- TASK-001 yaml:148: 「若 B.1 基线与 1cb3872 在谓词读取的 5 个文件上有 diff, 先重跑 sc11-predicate-validation.py, 三态不符同样先修谓词」—— 该脚本是 B.1 时唯一的再验证工具。
- 附带: script:121 `shutil.rmtree(TMP)` 不在 try/finally 中, docstring :14 所说「原文不匹配时断言失败」时临时目录残留。

**照计划执行会出的错**: B.1 时若 schema / collector 已被并发轨改动而需要重写模拟或谓词, 执行者看 rc=0 判「三态相符」, 谓词对「只加 Change history 行」「只改一半」重新失去鉴别力而验证器给出绿灯 (memory test-claims-vs-verifies / check-runs-at-baseline-first)。

**建议改法**: 脚本内嵌 5 列期望矩阵 (即 yaml:89-108 那张表), 任一格不符即 rc=1 并打印差异格; 或 TASK-001 验收改为「脚本输出与 `measured_2026_09_15_at_1cb3872` 逐格 diff 为空」。顺手加 try/finally。

#### N-03 [Major] type=issue · category=architecture · scope=TASK-033 yaml:393-408 与 TASK-019 / TASK-020 / TASK-023 的 dependencies · v2 返工引入: 是

**证据**:
- TASK-033 deps `[TASK-013, TASK-014]`; TASK-019 / TASK-020 deps `[TASK-012, TASK-013, TASK-014]`; TASK-023 deps `[TASK-013]`。传递闭包实算: (TASK-033, TASK-019) / (TASK-033, TASK-020) / (TASK-033, TASK-023) 三对无序。
- TASK-033 yaml:406: 「提交前 `git -C aria status` 的改动面恰为组 2 交付物 (handoff_multibranch.py / scan.py / latest_md_writer.py / test_scan_integration.py …), 提交后工作树干净」。
- TASK-019 改 aria `references/state-snapshot-schema.md`; TASK-023 改 aria `references/layer-l-integration.md` (另改 standards); TASK-020 改 `handoff_multibranch.py` —— 正是 TASK-033 要提交的文件。TASK-023 只依赖 TASK-013, 可在 TASK-011 / 012 / 014 仍在改 collector 时开工。yaml:9 与 tasks.md:74 声明执行序以依赖为准。

**照计划执行会出的错**: 按依赖图就绪即派发 (memory workflow-file-domain: 文件集不相交即并行) 时, TASK-019 / TASK-023 很可能先于 TASK-033 落盘 ⇒ TASK-033 两条验收必有一条红: 连文档一起提交则「改动面恰为组 2」不成立, 不提交则「提交后工作树干净」不成立。TASK-020 与 TASK-033 并发时, 主控提交的是知识席半改状态的 collector, 组 3 反事实副本的检出源混入未完成的文档编辑 (同文件未串行)。DUAL_LAYER_SPEC.md:61 的默认「1.x → 2.x → 3.x」本可遮住它, 但本 yaml 已声明依赖为执行序 SOT, 且多处跨组排序不按组号 (如 TASK-024 依赖 TASK-017)。

**建议改法**: TASK-019 / TASK-020 / TASK-023 的 dependencies 各补 TASK-033 (TASK-024 已经经 TASK-017 排在其后)。

#### N-04 [Major] type=issue · category=testing · scope=TASK-007 yaml:262 / metadata.rule6_note yaml:121 / tasks.md:45 (清单第 8 条) 与 :79 (1.2) / SC 映射表 SC-4 · SC-5 行 · v2 返工引入: 是

**证据**:
- yaml:262 无条件规定「SC-1 / SC-3 / SC-4 后半 / SC-5 / SC-8 后半 / SC-17 的 proposal 反事实 … 即基线形态, 台账逐条写明『本 RED 记录即该反事实的实跑』」; 同时 TASK-003 / TASK-004 明文接受「直接索引 KeyError」为合格 RED 形态, 并要求 `data["unreadable_count"]` 用直接索引。
- proposal:419 SC-5 断言四项: kind 存在 / `tracks[]` 不含对应行 / `legacy_count` 不增 / `unreadable_count == 1`; 反事实原句「保留旧降级分支 ⇒ tracks 多一行 ⇒ 红」只指向第二、三项。
- 基线探针 (实跑命令第 8 项) 输出: `kinds: ['handoff_multibranch_git_show_failed']` (第一项在基线上本就为真) / `tracks rows: 1 ['legacy:master:2026-05-09-x.md']` / `legacy_count: 1` / `unreadable_count: KeyError 'unreadable_count'`。基线同时有三个失败源, unittest 在第一个失败断言处停, 记下哪一个取决于断言书写顺序。
- 基线 = 全部组件同时回退; proposal 的反事实 = 在其余正确实现上只回退一个组件。两者只在「首个失败断言恰是反事实所指那条」时等价。SC-4 后半同型: 若用例按 `rel_path` 定位行, 基线先 KeyError, 走不到「`updated_at` 为空串」那条。

**照计划执行会出的错**: SC-5 的 RED 记录若是 `KeyError 'unreadable_count'`, 台账仍按 yaml:262 标成「保留旧降级分支反事实的实跑」, 而「`tracks[]` 不含该行 / `legacy_count` 不增」两条断言的鉴别力从未被证明 —— Rule #6 substitute 证据出现假绿 (memory test-claims-vs-verifies: 每条测试必答「它怎么会红」)。

**建议改法**: yaml:262 加前提「RED 记录的首个失败断言须正是 proposal 反事实所指的断言 (SC-5: `tracks[]` / `legacy_count`; SC-4 后半: `updated_at` 非空), 否则该条改入 TASK-018, 在 TASK-033 SHA 上只回退该组件按三步法实跑」; 或在 TASK-004 规定这两条用例的断言顺序。rule6_note、清单第 8 条、映射表同步。

#### N-05 [Minor] type=issue · category=documentation · scope=TASK-032 yaml:775-776 / tasks.md:48 (清单第 11 条) · v2 返工引入: 是

**证据**: 实跑命令第 6 项 —— 全勾副本 `verdict: warn`, unverified_claims 三条: 2.2 行 (「调用」命中) `symbol 'HEALTHY_TRACKS' unclassified reference form`、4.4 行 `no extractable symbol (fail-soft)`、4.3 行 dogfood 无产物路径; `d_payload` 非 None。本席 R1 F-04 当时即列三条。yaml:775 写「来源为 4.3 行的 dogfood 声称与 4.4 行的文件名子串 integration」, 清单第 11 条也只写 4.3 / 4.4, yaml:776「两类检查器假阳性另报」。实现落地后 `HEALTHY_TRACKS` 仍只在 tests/ 定义, 这一条不会自行消失。

**照计划执行会出的错**: D.2 预演出现计划未预期的第三条, 要么被当真问题去改写 2.2 措辞 (与「不为过检查器改写」冲突), 要么落在「另报」清单之外; 请 owner 授权的外向清单少一类。

**建议改法**: yaml:775 与清单第 11 条补上 2.2 行 (测试专用常量无生产定义 ⇒ unclassified ⇒ warn), 「两类」改「三类」。

#### N-06 [Minor] type=issue · category=testing · scope=TASK-026 yaml:639 / tasks.md:114 (5.5) · v2 返工引入: 是 (F-12 处置不充分)

**证据**: `classify_artifact_claim` 实跑 (具体目录用不存在的 `aria-plugin-benchmarks/ab-results/2026-10-01-handoff-multibranch-rule6/`): 原样 → `verified: True, linked artifact exists: aria-plugin-benchmarks/ab-results/`; 把「(勾选时本行写入具体目录)」换成具体目录、父目录 token 仍在行内 → tokens `['aria-plugin-benchmarks/ab-results/', 'aria-plugin-benchmarks/ab-results/2026-10-01-handoff-multibranch-rule6/']`, **仍 `verified: True`** (`spec_complete.py` 的 token 循环遇第一个存在的路径即返回); 连父目录 token 一并替换 → `verified: False`。

**照计划执行会出的错**: 按「本行写入具体目录」最字面的做法 (填占位括号) 执行, 归档门对 5.5 的产物抽验仍恒过, AB 结果目录缺失时漏检, R1 F-12 原样保留。

**建议改法**: 5.5 行与 yaml:639 写明「勾选时把行内 `aria-plugin-benchmarks/ab-results/` 整个替换为具体结果目录, 行内不得残留父目录 token」。

#### N-07 [Minor] type=risk · category=testing · scope=谓词 (j2) yaml:76 / (j3) yaml:77 / authoring_rules yaml:109 · v2 返工引入: 是

**证据**: 在脚本 target 副本上只做语义正确的改写: 注释块首行去掉 "finalized" (加第 5 级后该词已不准) 为 `# Tie-break (round 4, 10CG/Aria#195; extends the round-3 key): the sort key is FIVE levels, all` ⇒ **j3 FAIL**; schema 键序句 "compound key" 改为 "sort key" ⇒ **j2 FAIL**; 其余谓词均 PASS。v1 谓词块曾有注释「(j2)(j3) 用内容锚点 ('compound key' 句 / 'Tie-break, finalized' 注释块) … 锚点句若被改写, 判据同批改」, v2 删除后 authoring_rules 只约束 (j4)(j5)(k)。对照: (j5) 的行邻接约束已写进 authoring_rules, 本席 reflow 副本 j5 FAIL 属已告知的书写约束, 不另计。

**照计划执行会出的错**: TASK-019 / TASK-020 改写键序句时顺手换掉锚点词, 谓词假红, 计划没有处置口径 (改回措辞还是改谓词)。

**建议改法**: authoring_rules 补「schema 键序句保留 `compound key` 字样; collector 注释块首行保留 `# Tie-break, finalized` 前缀」, 或把 (j3) 锚点换成本次不会改写的区段边界。

#### N-08 [Minor] type=issue · category=testing · scope=谓词 (l1) yaml:81 / TASK-013 yaml:373 / tasks.md 读前必看表 · v2 返工引入: 是

**证据**: TASK-013 yaml:373 要求「Scenarios (:287-290) 补第四种结局」; proposal:425 SC-11(l) 原文要求 `:32` / `:279` / `:287-290` 三处各有命中, proposal:331 第 (4) 项点名 Scenarios 表是「单 active track ⇒ 写真指针」无条件断言的成文面之一。(l1) 只要求模块 docstring 与 `write_latest_md` docstring 各含 `degraded_reason`, 验证脚本 `writer_docs` (script:49-53) 也没有 Scenarios 编辑。副本 `bad_scenarios_missing` (Scenarios 块仍只有 0 / 1 / >=2 三行) ⇒ **l1 PASS**。另: proposal SC-11(k) 的两条 `! grep -q` 旧句判据在 v2 被取消 (R1 F-06 处置), 读前必看表只对 (j) 列了差异 (tasks.md:18), (a)(b)(i)(k)(l) 的判据替换未列入, 仅清单第 12 条笼统提及。

**照计划执行会出的错**: Scenarios 表漏补第四种结局时 SC-11 全绿; 按 proposal SC-11 原文复核的人会与 yaml 谓词得出相反结论。

**建议改法**: (l1) 追加 Scenarios 区段定位 (取 `write_latest_md` docstring 中 `Scenarios:` 之后的文本, 要求含 `degraded_reason` 或 `target_in_subdir`), 验证脚本 target 补该编辑; 读前必看表加一行「SC-11 以 yaml 19 条定位谓词为准: (k) 不再要求删除旧句, (l) 由三处合计改为两段 docstring + Scenarios 区段」。

#### N-09 [Minor] type=issue · category=testing · scope=hard_constraints yaml:119 / TASK-011 yaml:340 / rule6_note yaml:121 · v2 返工引入: 是

**证据**: yaml:119「反事实一律三步: 从 TASK-033 记录的实现 SHA 检出一次性 git worktree 副本 → …」; 同文件 yaml:121 与 yaml:262 又规定 SC-1 / 3 / 4 / 5 / 8 / 17 由基线 RED 承担、SC-14 由中间态承担, 与「一律」字面冲突。TASK-011 yaml:340 的兜底分支「若已转绿 …, 在一次性副本上删去早退 dict 的该键按三步法补跑」: TASK-011 是 TASK-033 的祖先 (TASK-033 → 014 → 012 → 011), 执行 TASK-011 时 TASK-033 SHA 尚不存在。

**照计划执行会出的错**: 兜底分支触发时, 执行者要么在 feature 工作树上直接改 (违 hard_constraints), 要么挂到 TASK-033 之后却没有任务承接; 按「一律」核查的复核者会把 TASK-007 / TASK-011 的证据判为不合规。

**建议改法**: yaml:119 限定为「组 3 (TASK-015..018) 的反事实一律三步; 其余证据来源见 rule6_note」; TASK-011 兜底分支改为「记台账, 并入 TASK-018 在 TASK-033 SHA 上补跑」。

#### N-10 [Minor] type=issue · category=testing · scope=TASK-021 yaml:539 · v2 返工引入: 否 (v1 原句, R1 未报; v2 在同一 bullet 追加了 `git -C aria` 形态但前半未改)

**证据**: yaml:539 前半「git diff <B.1 基线> -- aria/skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json .aria/repro/handoff-tracks-frozen-2026-09-05.json 为空」把子模块内路径与主仓路径放进同一条 git diff。实跑命令第 11 项: 超级仓对子模块内部路径的 diff 恒为 0 行 (同一区间子模块内实为 41 行); 以 aria SHA 作 revision 则 `fatal: bad revision` rc=128。

**照计划执行会出的错**: 在主仓用主仓 SHA 跑, aria 那份冻结语料即使被重生成也输出「为空」(恒绿); 用 aria SHA 跑则报错。实际兜底只剩 `test_collision_frozen_corpus.py:111` 的行数断言 (只覆盖 aria 那份, 且要求重生成改变了行数), 故列 Minor。

**建议改法**: 拆成两条 —— `git -C aria diff <aria B.1 基线> -- skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与主仓 `git diff <主仓 B.1 基线> -- .aria/repro/handoff-tracks-frozen-2026-09-05.json`, 两个基线 SHA 分别取自 TASK-001 台账。

#### N-11 [Minor] type=issue · category=implementation · scope=tasks.md:30 (读前必看第 13 条) / scope_repos 主仓 branch_base yaml:39 / TASK-001 yaml:145 · v2 返工引入: 是

**证据**: 实跑命令第 12 项 —— A.2/A.3 两个提交只在本地 master, origin/master 的 change 目录只有 proposal.md。第 13 条与 yaml:39 要求主仓 feature 分支「从 B.1 实测的 origin/master 起」; 全计划没有「B.1 前把 A.2/A.3 提交推上 origin/master」的任务, 而推共享 master 属 hard_constraints yaml:113 的外向动作 (memory sync≠push-auth)。另 yaml:145「实测 origin/master」未要求先 fetch, 读到的是本地远端跟踪 ref (memory freshness-must-be-fetched)。

**照计划执行会出的错**: 照字面从 origin/master 起主仓分支, 工作树里没有 tasks.md / yaml / 验证脚本, 台账无处落; 执行者只能临场二选一 (从本地 master 起 = 违第 13 条; 未经规划推 master = 计划外外向动作)。

**建议改法**: 第 13 条对主仓改为「从包含 A.2/A.3 提交的 master 起; 届时若未推送, 推送列为 B.1 前置并进外向授权清单」; TASK-001 取三处 SHA 前先 `git fetch` (或直接 `git ls-remote origin master`)。

#### N-12 [Minor] type=issue · category=documentation · scope=TASK-032 yaml:778 / metadata.verification_ledger.path yaml:22 / tasks.md:113 (5.4) · v2 返工引入: 是

**证据**: yaml:778「tasks.md 5.4 在归档前勾选; release_gate / 回帖 / handoff 三个子步骤的完成证据记台账」; 台账路径固定为 `openspec/changes/handoff-multibranch-subdir-path-fidelity/verification-ledger.md` (yaml:22); openspec-archive SKILL.md Step 3 `git mv openspec/changes/{change_name} openspec/archive/{YYYY-MM-DD}-{change_name}`、Step 4 断言 2「openspec/changes/{change_name}/ 已不存在」; phase-d-closer SKILL.md:41-43 / :65 顺序为 D.2 归档 → D.2b claim 释放 → D.3 handoff —— 三个子步骤都发生在台账被移走之后。「5.4 在其子步骤完成前勾选」是主控的流程判断, 未进 tasks.md「AI 流程判断清单」(Rule #10 §5)。

**照计划执行会出的错**: 按 metadata 路径写入会在 `openspec/changes/` 下重建一个只有台账、没有 proposal.md 的目录; 按归档路径写入则改写已归档目录, 计划没说哪一种; 归档件里 5.4 为 [x], 其子步骤仍可能随后失败。

**建议改法**: TASK-032 写明归档后台账路径为 `openspec/archive/<日期>-handoff-multibranch-subdir-path-fidelity/verification-ledger.md` (或子步骤证据只进周期 handoff); 清单追加一条「5.4 为满足归档门在子步骤前勾选」请 owner 复议。

#### N-13 [Minor] type=issue · category=documentation · scope=TASK-028 yaml:677 / TASK-032 yaml:781 / TASK-031 yaml:758-759 / TASK-026 · v2 返工引入: 是 (R1 F-09 处置部分落地)

**证据**: 第一次自检范围「aria 与 standards 的 feature 分支 + 主仓本 Spec 目录」(yaml:677); 第二次「周期 handoff、10CG/Aria#195 回帖、台账追加与主仓同步面文字 … 自检后再落笔 / 发帖」(yaml:781, 位于 TASK-032)。本席 R1 F-09 点名的 TASK-031 PR 正文: TASK-031 验收无自检项, 且 PR 在 TASK-032 之前就已发布并合并; TASK-030 的主仓同步面文字同样在第二次自检前已合并, 「自检后再落笔」对它们不可能成立。TASK-026 的 RESULT.md (`aria-plugin-benchmarks/ab-results/` 下) 与套件缺口 issue 正文不在任何一次范围内 (TASK-025 的 issue 有「引用全部写 <org>/<repo>#<n>」, TASK-026 的没有)。第一次自检主仓侧「本 cycle diff」的基线 SHA 未指明。

**照计划执行会出的错**: PR 正文、AB RESULT.md、套件缺口 issue 中的裸引用 / 带圈编号不经自检就对外发布。

**建议改法**: TASK-031 验收补「PR 正文发布前按 §4.4 / §4.5 自检」; TASK-026 补 RESULT.md 与 issue 正文自检; TASK-028 写明主仓 diff 基线 = TASK-001 记录的主仓 SHA。

### 核对无误的部分 (不计 finding)

- 三处归属逐项一致: yaml:63-64 归属注释 ((c1)(c2) TASK-009 · (i1) TASK-010 · (k)(l1) TASK-013 · (a1)(a2)(b)(f1)(f2)(g)(i2)(j2) TASK-019 · (j1)(j3)(j5)(l2) TASK-020 · (j4) TASK-019 与 TASK-020 · (l3) TASK-023 · 复跑 TASK-021 / TASK-029) ↔ tasks.md:133 SC-11 行 (2.1 / 2.2 / 2.5 / 4.1 / 4.2 / 4.1 与 4.2 / 4.4 / 4.3 / 5.2) ↔ 各 TASK verification 的「为真」声明 (yaml:300 / :318 / :373 / :501 / :521 / :576 / :538 / :698) 无一不符; TASK-020 要求保持为真的 (c1)(c2)(i1) 分属其祖先 TASK-009 / TASK-010。
- 新增 TASK-033 (parent 2.7) / TASK-034 (parent 5.2) 与 tasks.md 2.7 / 5.2 对应; 26 个 parent ↔ tasks.md 26 个 checkbox; 组 5 标题执行序与依赖图一致 (TASK-025 / TASK-026 无序, 其后 027→028→029→034→030→031→032 串行); metadata 计数 34 / 100 / 14·10·10 与实算一致。
- 读前必看第 1 / 3 / 7 / 12 / 13 条引用的 proposal 行号 (:308 / :320 / :330 / :353 / :370 / :421 / :426 / :9 / :21) 实读含对应原文; 第 8 条偏移与 `git diff -U0` hunk 头一致。
- 归档门: 全勾后 `complete=True`、`blocking=[]`, 不会误 BLOCK; `parse_detailed_tasks` 对 v2 yaml 解析成功。
- TASK-026 场景 1 三步、通过判据 (AB_TEST_OPERATIONS.md:552-556)、phase-d-closer AB 追加落点均与手册 / 仓内事实一致。
- 写法自检、U+FFFD 与控制字符: 三份审计对象全部干净 (实跑命令第 10 项)。
- 第 5 级键实现字面、SC-14 中间态反事实的失败机理 (中间态下仅 `unreadable_count` 直接索引 KeyError, 与 proposal SC-14 反事实原句一致) 属实。

## Verdict

0 Critical / 4 Major / 9 Minor ⇒ **PASS_WITH_WARNINGS**

## Vote

**REVISE** —— 4 条 Major 全部由 v2 返工引入 (4/4): 定位谓词 (a2) 在最可能的漏改写法下仍假绿 (N-01)、验证脚本退出码只核 5 列中的 3 列 (N-02)、新增 TASK-033 与组 4 文档任务无依赖边 (N-03)、「基线 RED 即反事实」的等价声明无条件成立不了 (N-04)。均可在 tasks.md / yaml / 验证脚本内定点修订, 不涉及 proposal 设计取舍。按 R1 聚合报告「收敛判断」自定的条件 (R2 Major 过半由本轮修订引入 ⇒ R3 前换执笔人), 本席计数已满足该条件。

## 轮次记录

Round 2 (code-reviewer, convergence): REVISE — 0C/4M/9m (4M 全部 v2 引入); 19 条谓词基线全假、验证矩阵与 yaml 逐格一致、三处谓词归属一致属实, 但 (a2) 可被同行散文满足、验证脚本 rc 不核 bad_changelog_only / bad_partial、TASK-033 与 TASK-019/020/023 无序、SC-5 基线 RED 不必然是反事实; R1 本席 13 条处置 9 条完整落地、2 条有残留、F-09 / F-12 部分落地。
