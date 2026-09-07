---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T03:12:47.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead]
---

# post_spec R3 单席报告 — tech-lead (handoff-multibranch-subdir-path-fidelity, Aria #195)

本席为 R3 新席位, **不继承 R1/R2 结论**。全部载重断言经实读插件缓存 `1.71.1` 副本 (= aria `origin/master` `301641b`) 与真 checkout `/home/dev/Aria/aria` 复核, 行号一律以该副本为准。本轮**只审不改**, 未编辑仓库任何文件。

## 审计结论

### Decisions

- [minor] architecture/R2 3 critical + 10 major 的正文落地复核: 逐条复核, **全部落在正文而非批注, 未见「改一处引入另一处矛盾」的回填**。抽验: `6f8fa9f7` → §2.5 新增「`rel_path` 缺失语义」行 + Task 2.5 (b) + SC-15 布局 3 + SC-10 并入 `test_p1_layer_h`; `d1f01126` → §2.5 生产可达性块 + Impact.Risk 缓解范围限定 + 待复议 2 第 (4) 问; `88a49037` → SC-15 收敛为三布局 + 表后细则小节 + (f) 移出改记述性; `885edf34` → 头部 Rule #6 行与 rule6_note 双双改判照跑 + Task 5.5; `d02ec3f0` → SC-2 走 `freeze_corpus.py:29` 八字段投影 + 新增 SC-16; `112b4299` → SC-12a/12b 拆分; `94935605` → Task 4.4; `d58dfb65` → Task 5.1 十六点表 + 删除「漏改必转红」错误陈述。**字面口径亦已自洽**: 全文守卫判据统一为 `track.get("rel_path")`, 未见残留 `track.get("relpath")` (证据: proposal.md:12,124-146,226,283-296)
- [minor] architecture/ship 顺序 / gitlink 归属: 实测 `git -C /home/dev/Aria rev-parse HEAD` = `f634d837`, `git ls-tree HEAD aria` = `301641b` = `git -C aria rev-parse origin/master`, `standards` gitlink = `21748d4` = 其 origin/master; `git -C aria tag --list 'v1.7*'` 最高 `v1.71.1`。⇒ Task 5.2「gitlink 从 `301641b` 前进、严禁回退 `0545f86`」与待复议 6 的候选号未被占用两点均成立。另核 `aria-plugin-benchmarks/` **不是子模块** (`.gitmodules` 仅三条: standards / aria / aria-orchestrator), AB 结果落主仓, 不引入第三条 gitlink 链路 (证据: .gitmodules:1-9; proposal.md:245-246)
- [minor] architecture/越界面 / 同伴容器在飞轨: 触点集合不含 `phase1_gate.py` / `claim_lifecycle` / `spec-drafter` / `phase-a-planner` / AB 套件本体 —— Task 5.5 (b) 只**开缺口 issue**, 不改 `ab-suite/state-scanner.json`; Task 5.3 只开 issue, 不改 `handoff.py` 本体。`docs/handoff/latest.md` track 表内 `simonfish/023236f2` 各轨均 done, 在飞的只有本容器 `aria-runner-bot/bfe8285d` 的 M6 轨 (aria-orchestrator, 与本 spec 五触点零交集)。**无越界** (证据: proposal.md:243-249; docs/handoff/latest.md:8-14)
- [minor] testing/载重数据可用性机械核验 (audit-points 横切「数据可用性」条款): 五项逐条实跑, **全部与 proposal 陈述一致** —— (1) SC-10 五模块真 checkout `Ran 102 tests in 17.242s … OK`; (2) 两份冻结语料均存在、各 996 行、恰八字段、`filename` 含 `/` 为 0、非 ASCII 为 0; (3) `ab-suite/state-scanner.json` 实测 **17551 B**, `tracks_multibranch` 命中 **1** (`:214`, prompt 小问 (C) 逐字把「`collision.kind` 是空的」写死在题面), `handoff_multibranch` / `legacy` / `basename` 均 **0**; (4) `git diff --name-status 0545f86 301641b` = **29** (5 A + 24 M), 同区间五触点 `--stat` **输出为空**; (5) `freeze_corpus.py:29` `FIELDS` 确为八字段、不含 `rel_path`。⇒ 该条款不载重 REVISE

### Issues

- [major] testing/Task 2.1 `_list_handoff_files` 返回契约变更 / SC-10 点名集: §What.1「契约变更」行与 Task 2.1 都要求把返回签名从 `tuple[list[str], str | None]` 改成能携带 per-item 错误 (第三返回位或注入 reporter), 但**全文零处登记该契约的既有 mock 消费方** —— `tests/test_max_branches_resolver.py` 四处 `mock.patch.object(hmb, "_list_handoff_files", return_value=([], None))` 仍是 2-tuple, 主循环改成三值解包后**必抛解包错**。该模块实跑现绿 (`Ran 39 tests … OK`), 且 grep 确认它是**除 collector 自身外唯一引用四个被改私有函数的测试模块**; SC-10 点名集 (5 模块 102 tests) 不含它, 只靠尾句「全量 discover 另跑」兜底 —— 与 R2 `7cba5aa4` 判 `test_p1_layer_h` 时否决的正是同一种兜底 (证据: handoff_multibranch.py:240,619; tests/test_max_branches_resolver.py:286,300,316,332; proposal.md:104,227,271)
- [major] architecture/Task 4.4 与 §6.6 的 standards 第三态: Task 4.4 把第三态 (单 active track 但文件在子目录 ⇒ 降级 + 写明原因) **无条件**写进共享子模块 SOT `standards/conventions/session-handoff.md:171-173`, 而本 spec 自己已确立: 机械 `write_latest_md` **零生产调用点**, 生产 D.3 指针由 AI 按 `handoff-mechanics.md:116-121` 手改, 且该处方表本 spec **明说不改** (推给待复议 2 第 (4) 问)。⇒ 落地后 Rule #9 SOT 对所有采用方规定一条**无任何执行路径实现**的行为, 正是本 spec 立意要修的「契约陈述 ≠ 实现」那一类。另: 同文件 `:97` 有第二处两态表述 (「写入后**自动**更新 latest.md pointer(单 track 场景)」), Task 4.4 未登记, 改一处留一处会新造文内不一致。可行的收敛: 把第三态限定到「机械 writer 路径」并注明处方路径待裁, 或与 `handoff-mechanics.md` 同 PR 一并动 (证据: standards/conventions/session-handoff.md:97,171-173; handoff-mechanics.md:4,116-121; proposal.md:139-141,177-179)
- [major] documentation/dedupe build-order 不变量的三处文档未纳入同步项: A′ 保留 basename 后, 「同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同」两行的四级键**全部并列**, `max()` 回退迭代顺序, 而该结论在**三处**成文: 模块注释 `handoff_multibranch.py:396`「now a pure function of the candidate rows' own field values, invariant to the order tracks is built/passed in」、`_dedupe_sort_key` docstring `:436-450`、`state-snapshot-schema.md:1126`。proposal 已在 §5 / Impact.Risk / 待复议 4 附问里**承认该不变量被打破**, 但待复议 4 的推荐默认是「不改排序键」, 而 Task 4.1 (schema 同步清单) 与 Task 4.2 (docstring 勘正清单) **均无一条**把这三处条件化 ⇒ 按推荐默认落地即 ship 一条已知为假的文档断言, 违反 Rule #3。注意这与 R2 正确删除的 `:1125` 订正是**两条不同的句子**: `:1125` 在 A′ 下仍为真, `:1126` / `:396` / `:436-450` 才是被 A′ 打破的那条 (证据: handoff_multibranch.py:396,436-450; state-snapshot-schema.md:1126; proposal.md:164,209,219,330)
- [major] architecture/待复议 6 的版本**级别** (非号码) 与本仓两条先例冲突: 待复议 6 只写「版本号: PATCH …候选 v1.71.2」并只请 owner 复核**撞号**, 未论证级别。而本 spec 自己引用的先例反向: (a) `state-snapshot-schema.md:1070` 逐字「Semantic change (non-shape; **carried by plugin MINOR v1.46.0**, NOT a `snapshot_schema_version` bump)」; (b) `aria/CHANGELOG.md:84` 的 `[1.70.0]` 标题逐字「owner 裁定 D5: §2.3.5 **对采用方是行为变更 ⇒ MINOR**」—— 那一轮的形态与本轮同型 (恒存在 additive 字段 `identity_advisories[]` + collision 判定变化 + 改同一份 `standards/session-handoff.md`)。本 spec 新增 `rel_path` / `unreadable_count` 两个机读字段、收窄 `legacy_count`、可使 `collision.kind` 由 `none` 翻到 `cross_owner`、改 `exists` / `len(tracks)`, Impact 自述「子目录采用方可能**突然开始**看到并发碰撞告警」⇒ 按先例应为 MINOR (v1.72.0)。级别一旦定错, Task 5.1 的 16 个版本点、tag、CHANGELOG 标题全部连坐 (证据: proposal.md:333; state-snapshot-schema.md:1070; aria/CHANGELOG.md:84; proposal.md:198,203)
- [major] implementation/§2.5 守卫只覆盖渲染面, 未覆盖 `write_latest_md` 的机读返回契约: `write_latest_md` 返回 `{"action", "path", "content_lines"}` (latest_md_writer.py:316-319), `action` 在 `n_active == 1` 分支恒被赋 `"pointer"` (`:302-304`), 与 `_render_pointer` 内部是否回退到 `_render_pointer_unavailable` **无关**。守卫落地后, 子目录 track 会写出「(pointer 不可用)」正文却仍回报 `action="pointer"`。§2.5 的四条硬要求 (a)-(d) 与 SC-15 布局 2 的 (d)(e) **全部只断文件内容**, 没有一条约束返回值 ⇒ 「诚实降级」在机读面上不成立; 而守卫的全部价值恰恰在 writer 未来被接线之后, 那时的调用方读的正是 `action`。修法成本极低 (加一个 action 取值或 reason 键 + SC-15 布局 2 加一条断言), 且不打红既有 `test_p1_layer_h.py:264` 的 `assertEqual(result["action"], "pointer")` —— 该用例的 track 无 `rel_path`, 走缺键兜底照写真指针 (证据: latest_md_writer.py:298-319; proposal.md:130-136,226,290-292)
- [minor] testing/rule6_note 的 SC-15 baseline-failing 归因不准: rule6_note 写「SC-15 的资格改由布局 2 的 (d)(e) + 布局 3 的 (g) 撑住」。实读机制后**(e) 与 (g) 在全量回退下都是绿的**: 全量回退 ⇒ 无 collector 修复 ⇒ 子目录件恒 legacy ⇒ `n_active == 0` ⇒ `write_latest_md` 走 `_render_zero_tracks` (latest_md_writer.py:226-235,298-300), 该占位文本既无 `**Latest**: [` 也不产生 `handoff_pointer_target_missing` ⇒ (e) 绿; 无守卫时缺键 track 本来就照写真指针 ⇒ (g) 绿。真正在全量回退下转红的只有 (d) 的后半句 (要求文案含「目标在子目录」的具体原因)。(e)(g) 是**针对部分实现 / 错误实现**的反事实, 价值成立, 但不该记进「机制没实现会变红」那一档的支撑 (证据: latest_md_writer.py:226-235,298-300; proposal.md:288,296,306)
- [minor] documentation/standards 链路缺基线冻结: 头部把 aria 基线冻结到 `301641b` 并附「两 SHA 增量实况」「五触点零 diff」的实测, 严谨度很高; 但 Task 4.4 引入的**第二条子模块链路 standards** 全文无基线 SHA (本席实测 `git -C standards rev-parse origin/master` = `21748d4` = 主仓 `ls-tree HEAD standards`)。R1 / R2 各出现过一次 gitlink 相关 conflicted (`4c05b95a` / `9f7d9aff`), 根因都是缺一个写死的起点; 同型风险在 standards 侧未封 (证据: proposal.md:9-10,141,247; 实测 `git -C standards rev-parse origin/master`)

### Risks

- 本席未新增独立 Risk 条目。上轮已登记的两条主要风险 (`collision.kind` 由 `none` 翻 `cross_owner`; A′ 打开 dedupe tie 可观测性) 均已在 Impact.Risk 与 §5 成文, 本席复核**机制陈述属实**; 其中第二条的**文档同步**缺口已按 Issue 第三条载重, 不重复计。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **5** / Minor **2** (另 4 条 decision, 按 R1/R2 同规则不计入 severity 计数)。

rationale: R2 的 3 critical + 10 major **逐条落在正文而非批注**, 且未见回填矛盾 —— 这一轮的缺陷**无一是重开 R1/R2 已闭合项**, 全部落在 v4 增量的下游 (Task 2.1 契约变更未扫测试消费方 / Task 4.4 新引入的 standards 面 / A′ 打破的不变量三处文档 / 待复议 6 的级别判断 / 守卫的机读返回面)。五条 major 全是**设计缺口与事实性冲突**, 无一条构成「方案错误」或「SC 恒绿导致假绿」, 故不判 FAIL; 但其中 Task 2.1 的解包破坏与待复议 6 的级别冲突属机械可证、成本极低的补漏, 应在 R4 前落地。post_spec 为 `blocking: false`, verdict 不阻断后续流程, 仅载重 REVISE 票。

## 轮次记录

### Round 3

- **Agents**: tech-lead (本席; 五席之一, 其余四席独立出报告)
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品
- **Conclusions 数**: 11 (issue 7 = major 5 + minor 2; decision 4, 全部 minor 不计入)
- **Vote**: REVISE
- **本轮实跑清单 (可复现)**:
  1. `cd /home/dev/Aria/aria/skills/state-scanner/tests && python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories test_p1_layer_h` → `Ran 102 tests … OK` (SC-10 基线独立复核通过)
  2. 同目录 `python3 -m unittest test_max_branches_resolver` → `Ran 39 tests … OK` (Issue 第一条的基线)
  3. `grep -rln "_list_handoff_files|_read_file_content|_get_file_commit_date|_make_legacy_track_id" tests/ scripts/` → 命中集仅 `tests/test_max_branches_resolver.py` + collector 自身
  4. `git -C aria diff --name-status 0545f86 301641b` → 29 (5 A + 24 M); 同区间五触点 `--stat` 输出为空
  5. 两份冻结语料 `json.load` 统计 → 各 996 行 / 恰八字段 / `filename` 含 `/` 为 0 / 非 ASCII 为 0
  6. `wc -c ab-suite/state-scanner.json` = 17551; 四词 `grep -c` → 1 / 0 / 0 / 0; `sed -n '214p'` 确认 `collision.kind` 值写死题面
  7. `git rev-parse HEAD` = `f634d837`; `git ls-tree HEAD aria standards` = `301641b` / `21748d4`; `git -C aria tag --list 'v1.7*'` 最高 `v1.71.1`
  8. 逐处实读: `latest_md_writer.py:70-95,143-169,226-235,298-319` · `handoff_multibranch.py:240-292,396,426-455,619` · `scan.py:126-210` · `track_board.py:248-262,552-566` · `state-snapshot-schema.md:46-48,1070,1120-1136` · `session-handoff.md:97,171-173` · `handoff-mechanics.md:105-130` · `skill-benchmark-exemption.md:1-80` · `freeze_corpus.py:20-40`
