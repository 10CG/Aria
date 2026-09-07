---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T04:45:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — handoff-multibranch-subdir-path-fidelity (Round 3)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文**逐字**落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager); 五份 frontmatter 15 字段齐全 (机械核验: 逐文件 awk 抽 frontmatter 后计 `^[a-z_]+:` = 15/15/15/15/15), **0 份需补齐**。缺席 0, `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (本轮实际执行, 与 R1 / R2 聚合报告同规则, 供 Round 4 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 / 同一 Task (本轮实例: 「Task 4.4 写进 standards 的第三态无实现路径」与「§6 同步面漏另外 4 处」是两条; 「SemVer 版本级别」与「OpenSpec Level 字段」是两条)。
5. 席位**报告正文有、结构化清单未列**的条目**不计入** `found_by`, 但在相应条目内注明, 以免 Round 4 丢失该信号。本轮共 6 处: backend-architect 正文 decision「`collision.kind` 翻转的窗口限定」; qa-engineer 正文 decisions「A′ 与来源一致性」「hermetic 可构造性」「冻结语料不受影响」与两条正文 risks; code-reviewer 正文 decision「A′ 骨架代码级成立」; knowledge-manager 正文 decision「事实底座抽验」。
6. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (33 条全部唯一, 0 碰撞)。scope 归一为小写写法后入哈希与 keys。
7. 本轮去重前 **51** 条 (tech-lead 11 / backend-architect 9 / qa-engineer 8 / code-reviewer 11 / knowledge-manager 12), 去重后 **33** 条。
8. severity 计数**不含** decision 类 (与 R1 / R2 同口径)。

---

## 审计结论

### Critical (0)

本轮 **无 Critical**。五席各自独立判定 Critical = 0; R2 的 3 条 critical (`6f8fa9f7` / `d1f01126` / `88a49037`) 经五席逐条复核**全部落进 v4 正文而非批注**, 无一条被本轮重开 (见 decision `97c1c287`)。

> 汇总席记一条**待 owner / R4 复议的定级分歧** (不代替裁决, 不计入本轮 critical): code-reviewer 就 `90e3b4b8` (SC-11(c) grep 恒绿) 自述「按『SC 恒绿 ⇒ critical』的字面口径它够 critical, 本席据爆炸半径下调为 major …若汇总席按字面口径上调为 critical, 本席不反对」。按合并规则 1「severity 取各席**报告值**的最高者」, 唯一提出席位报的是 major, 汇总席不自行上调。

### Major (19)

- `a7536535` [major] testing/Task 2.1 `_list_handoff_files` 返回契约 / SC-10 点名集 — **found_by: tech-lead, backend-architect, code-reviewer (3/5)**
  Task 2.1 与 §What.1「契约变更」行要求 `_list_handoff_files` 从 `tuple[list[str], str | None]` 改成能携带 per-item 错误 (proposal 举例「第三个返回位」), 但**全文零处登记该契约的既有 mock 消费方**: `tests/test_max_branches_resolver.py:286,300,316,332` 四处 `mock.patch.object(hmb, "_list_handoff_files", return_value=([], None))` 后真调 `collect_handoff_multibranch`, 而主循环 `handoff_multibranch.py:619` 是二元解包 ⇒ 改三元组即四条现绿用例抛 `ValueError`, 与 collector 自述 "Never raises" 相悖。三席各自实跑该模块基线 `Ran 39 tests … OK`; tech-lead 另 grep 确认它是**除 collector 自身外唯一引用四个被改私有函数的测试模块**, backend-architect 实测全文提及次数 `grep -c` = 0。该模块不在 SC-10 五模块点名集, 只靠尾句「全量 discover 另跑」兜底 —— 与 R2 `7cba5aa4` 判 `test_p1_layer_h` 时否决的是同一种兜底。
  *修法 (三席一致)*: SC-10 点名集补 `test_max_branches_resolver`; 或 Task 2.1 明写「保持 2-tuple + 注入 reporter (带默认值)」这条不破契约的实现路径 (code-reviewer 指出该路径下四处 mock 不破, 但 spec 未点名触点 ⇒ 选型后果对实施者不可见)。

- `92565b30` [major] architecture/§2.5 / Task 2.5 守卫的 `write_latest_md` 返回契约与机读信号 — **found_by: tech-lead (implementation), code-reviewer (architecture), knowledge-manager (architecture) (3/5)**
  写侧守卫落在 `_render_pointer`, 而 `write_latest_md` 在 `n_active == 1` 分支**无条件**置 `action = "pointer"` (`latest_md_writer.py:301-304`), 与内部是否回退到 `_render_pointer_unavailable` 无关。公开返回契约只有三值 (`latest_md_writer.py:277-290` docstring + `references/phase-1-collectors.md:102` 逐字 `{action: "pointer"|"banner"|"skipped", ...}`), §2.5 / Task 2.5 定义了**第四种结局**却没给它 `action` 取值, 也没把这两处契约面列入 §6。⇒ 子目录 track 会写出「(pointer 不可用)」正文却仍回报 `action="pointer"`。
  消费侧同样零信号 (knowledge-manager 实测): 降级横幅不匹配 `_LATEST_POINTER_RE` (`handoff.py:263-266`) ⇒ `latest_source` 退回 `"mtime"` 且**零 soft_error**。三席一致的判词: §2.5 的 (a)-(d) 与 SC-15 三布局**全部只断文件内容**, 「不得静默退化 / 诚实降级」目前只在**人读面**成立, 机读半边仍在说谎; 而守卫的全部价值恰在 writer 未来于 D.3 被接线之后, 那时调用方读的正是 `action` (`handoff-mechanics.md:114-124` 子步骤 2 判的就是「pointer 更新了没有」)。
  tech-lead 另核: 修法成本极低 (加一个 action 取值或 reason 键 + SC-15 布局 2 加一条断言), 且**不打红**既有 `test_p1_layer_h.py:264` 的 `assertEqual(result["action"], "pointer")` —— 该用例 track 无 `rel_path`, 走缺键兜底照写真指针。
  *修法 (code-reviewer 列出三选一, 请在 spec 内裁)*: 新增 action 取值 / 加 `degraded_reason` 键 / 明写「action 保持 pointer 是有意为之」并同步两处契约文档。
  *category 分歧注*: tech-lead implementation、code-reviewer / knowledge-manager architecture ⇒ 取多数 architecture。

- `ebaad4a5` [major] documentation/legacy `track_id` 机读格式四处未同步 (§6 / Task 4.1 / Task 4.2) — **found_by: backend-architect, code-reviewer (2/5)**
  §What.2 与 SC-13 把 legacy id 从 `legacy:<branch>:<basename>` 改成 `legacy:<branch>:<rel_path>` (SC-13 直接断言 `legacy:<branch>:archive/x.md`), 但既有格式声明四处 —— `handoff_multibranch.py:36` (TrackEntry 契约) · `:332` (`_make_legacy_track_id` **自身** docstring「Format: ``legacy:<branch>:<filename>``」) · `:493-496` (dedupe 的「legacy track_id 已内嵌 branch+filename」论据句) · `state-snapshot-schema.md:1104` (TrackEntry 表) —— **无一进入 §6 同步清单、Task 4.1/4.2 逐项或 SC-11 的八条 grep**。其中 `:332` 就在 Task 2.2 要改的函数头上, 改代码不改它等于当场留一条自相矛盾的注释; 落地后 schema SOT 会对子目录采用方陈述一条假公式 (Rule #3)。
  *席位差异 (不构成分歧)*: backend-architect 列四处含 `:332`, code-reviewer 列三处 (`:36` / `:493-496` / `schema:1104`), 并集为四处。

- `b5a94a9c` [major] documentation/`rel_path` 记入错误 docstring 块 (Task 4.2 / SC-11(c)) — **found_by: backend-architect (major), code-reviewer (minor) (2/5)**
  collector 模块 docstring 有两个独立块: **顶层返回键表** `:16-31` (`exists` / `tracks` / `branches_scanned` / `legacy_count` / `collision` / `errors`) 与 **TrackEntry 块** `:33-44` (`filename` 在 `:42`)。`unreadable_count` 是顶层键, 记进前者正确; 而 `rel_path` 按本 spec 自身定义 (§7) 是**每行 track 多一个键**, 归属后者。Task 4.2 写「`:14-31` 键表补 `unreadable_count` + `rel_path`」, SC-11(c) 更把它固化成验收断言 ⇒ **照正确位置写文档的实现判红**, 照 SC 写的实现则在机读契约里声明一个并不存在的顶层键。§6 第 2 条原文只对 `:14-31` 提 `unreadable_count` (正确), 漂移发生在 Task 与 SC 这两层把两个字段合并成一句时。
  *severity 分歧注*: backend-architect major (「与 R2 `d02ec3f0` 断言在采纳的设计下自我打红同族」)、code-reviewer minor ⇒ 按规则 1 取最高 major。

- `120e1171` [major] testing/rule6_note 与 SC-15 的 baseline-failing 资格归因 ((e)(g) 恒绿) — **found_by: qa-engineer (major/testing), tech-lead (minor/testing), code-reviewer (minor/documentation) (3/5)** — **conflicted: true**
  rule6_note 写「SC-15 的资格改由布局 2 的 (d)(e) + 布局 3 的 (g) 撑住」。三席各自推演/实跑得同一结论: 全量回退 (无 collector 修复) 下 **(e) 与 (g) 都是绿的** —— 布局 2 的归档件恒降级 legacy ⇒ `n_active == 0` ⇒ `write_latest_md` 走 `_render_zero_tracks` (`latest_md_writer.py:226-235,298-300`) 返回 `action="skipped"` 写零 track 占位页 ⇒ 既无 `**Latest**: [` 也不产生 `handoff_pointer_target_missing`, `collect_handoff` kinds `[]` / `latest_source="mtime"`; 布局 3 (八字段无 `rel_path` 的 dict) 基线下 `_render_pointer` 无守卫必写真指针 ⇒ (g) 绿。真正在基线转红的只有 (d) 的后半句 (文案须含「目标在子目录」的具体原因)。
  qa-engineer 判词最重并连带一条: Task 1.2「新测试文件对 `301641b` **全红**且红在正确断言上」对 `::test_pointer_roundtrip_toplevel` 与 `::test_pointer_written_when_rel_path_key_absent` **不可满足**。
  **conflicted 的那半 —— (e) 是否有鉴别力**: knowledge-manager 在其正文 decision「事实底座抽验」中实测 `_LATEST_POINTER_RE` (`handoff.py:263-266`) 对降级横幅不匹配, 据此判「SC-15 布局 2 的 (e) 在『顶层留一份非-active 件』夹具下**确有鉴别力**, R2 `88a49037` 的处置机制上成立」; 三席则判 (e) 在**全量回退**下恒绿。汇总席记: 两侧的**反事实前提不同** —— KM 论的是「collector 已修、只拿掉守卫」, 三席论的是「机制整个没实现」; 是否矛盾可由 R4 一次 hermetic 跑闭合 (布局 2 + 顶层留非-active 件, 分别在 (a) 全量回退、(b) 仅拿掉守卫 两种代码态下取 (e) 的真值)。KM 该条为正文-only (规则 5), 故不计入 found_by, 但 conflicted 标记保留以免 R4 丢信号。
  *修法 (三席一致, 零设计改动)*: 把 (e)(g) 与布局 1 按本文既有口径标成「过修守卫 / 回归锁」(与 SC-7、SC-4 前半、SC-8 前半同级, 不计入 baseline-failing 实体), 并把 Task 1.2 的「全红」限定到它自己列举的四族。
  *category / severity 分歧注*: category tech-lead / qa-engineer testing、code-reviewer documentation ⇒ 取多数 testing; severity qa-engineer major、其余两席 minor ⇒ 取最高。

- `2af687f5` [major] architecture/Task 4.4 / §6.6 standards 第三态无实现路径 — **found_by: tech-lead (1/5)**
  Task 4.4 把第三态 (单 active track 但文件在子目录 ⇒ 降级 + 写明原因) **无条件**写进共享子模块 SOT `standards/conventions/session-handoff.md:171-173`, 而本 spec 自己已确立: 机械 `write_latest_md` **零生产调用点**, 生产 D.3 指针由 AI 按 `handoff-mechanics.md:116-121` 手改, 且该处方表本 spec **明说不改** (推给待复议 2 第 (4) 问)。⇒ 落地后 Rule #9 SOT 对所有采用方规定一条**无任何执行路径实现**的行为, 正是本 spec 立意要修的「契约陈述 ≠ 实现」那一类。
  *修法 (tech-lead 给两条互斥支)*: 把第三态限定到「机械 writer 路径」并注明处方路径待裁; 或与 `handoff-mechanics.md` 同 PR 一并动。
  *与 `3dd75e12` 的关系 (规则 4 保留两条)*: tech-lead 该条另点出同文件 `:97` 第二处两态表述未登记, 与 knowledge-manager 的枚举条目在该点重合; 两条的**主张与修法不同** (本条是「写进去的内容不可实现」, `3dd75e12` 是「同义断言另有 4 处未纳入同步面」), 故不合并, R4 若判为同一缺陷可自行并轨。

- `3dd75e12` [major] documentation/§6 同步面覆盖不全 — 「单 active track ⇒ 写真指针」5 处 — **found_by: knowledge-manager (1/5)**
  R2 `94935605` 只修到 standards 的一处。机械枚举同义断言面: (1) `standards/conventions/session-handoff.md:171-173` (Task 4.4 已覆盖); (2) 同文件 `:97`「写入后**自动**更新 latest.md pointer(单 track 场景)或 deprecation banner(多 track 场景)」未覆盖; (3) `state-scanner/references/layer-l-integration.md:103`「单 track: 更新 latest.md pointer」未覆盖; (4) `latest_md_writer.py:288-291` docstring 的 Scenarios 表未覆盖; (5) `latest_md_writer.py:140,159` —— **写进 latest.md 正文**的那句「自 v1.22.x 起, 本 pointer 仅在单 active track 场景下写真实指针」未覆盖, 落地后子目录采用方的 latest.md 会**同时印着这句和「(pointer 不可用)」**。另 `handoff-mechanics.md:116` 的 Single-track 行本文已登记并交 owner, 属已披露。

- `b57e3209` [major] implementation/`scan.py:186` 的 `rel_path` 缺键契约 (§3 / Task 2.2 / SC-6) — **found_by: backend-architect (1/5)**
  §2.5 用四行为 writer 定死了缺键兜底 (`rel = track.get("rel_path") or track.get("filename")`), 但同一批改动的**第二个**新字段消费方 `scan.py:186` 只写「必须显式改读新的 `rel_path` 字段」, 缺键行为空白。唯一覆盖它的 `test_scan_integration.py::TestSnapshotSelfConsistencyAC5` (11 tests, 该席实跑 OK) 夹具 `HEALTHY_TRACKS` 是三键手搓 dict、**无 `rel_path`**, 且 `_mock_run` 对任何 `git log -1` 返回同一 SHA、**完全不看路径参数** ⇒ 两个方向都坏: 写 `t["rel_path"]` 或 `if not rel: continue` 则今绿用例翻红; 写 `.get()` 则用例照绿但**结构上无法分辨** `filename` 与 `rel_path` 谁被拼进命令行。该模块同样不在 SC-10 点名集。
  *该席自加的诚实限定*: 生产路径 `tracks_data` 恒来自本次 collector 输出 (`scan.py:388`), 缺键不可达 ⇒ 这是 Phase B 实施面与回归面缺口, **不是生产缺陷**; 正因不可达, spec 应显式写明「此处不需要 writer 那样的兜底」并把模块纳入点名集, 否则实施者只能猜。

- `4608f5b2` [major] documentation/dedupe build-order 不变量三处文档 (`schema:1126` / `:396` / `:436-450`) — **found_by: tech-lead (issue/major/documentation), backend-architect (risk/minor/architecture) (2/5)**
  A′ 保留 basename 后, 「同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同」两行的四级键 `(parse_ok, updated_at, filename, branch)` **全部并列**, `max()` 回退迭代顺序。backend-architect 探针实证: 正序选中顶层那行 (`status=active`), 逆序选中 `archive/` 那行 (`status=done`); 改前两行逐字段相同故选谁都一样, 改后代表行的 `status` / `phase` 真会不同并经共享 dedupe 传导到 collision 与 track_board。
  该不变量在**三处**成文: 模块注释 `handoff_multibranch.py:396`「invariant to the order tracks is built/passed in」· `_dedupe_sort_key` docstring `:436-452` · `state-snapshot-schema.md:1126`。proposal 已在 §5 / Impact.Risk / 待复议 4 附问三处承认不变量被打破, 但**待复议 4 的推荐默认是「不改排序键」**, 而 Task 4.1 (schema 同步清单) 与 Task 4.2 (docstring 勘正清单) 均无一条把这三处条件化 ⇒ 按推荐默认落地即 ship 一条已知为假的文档断言 (Rule #3)。
  tech-lead 另作关键消歧: 这与 R2 正确删除的 `:1125` 订正是**两条不同的句子** —— `:1125` (日期前缀 tie-break 论据) 在 A′ 下仍为真, `:1126` / `:396` / `:436-450` 才是被 A′ 打破的那条。
  *修法 (backend-architect)*: 默认支加一条文档订正项 (把不变量限定为「同 `rel_path` 前提下」), 与「改排序键」支互斥。
  *正文-only 相邻信号 (规则 5)*: qa-engineer 正文 risk 同判此面, 并补一句叠加影响 —— 与 `17f270f5` (collision.kind 零覆盖) 叠加后, **collision 侧的行为变化在本轮完全没有测试面**。
  *type / category / severity 分歧注*: type tech-lead issue / backend-architect risk, 1-1 平票取席位序在先者 ⇒ issue; category 同理平票 ⇒ documentation; severity 取最高 ⇒ major。

- `f658ae7e` [major] architecture/待复议 6 版本**级别** (PATCH vs MINOR) / Task 5.1 发布面 — **found_by: tech-lead (1/5)**
  待复议 6 只写「版本号: PATCH …候选 v1.71.2」并只请 owner 复核**撞号**, 未论证级别。而本 spec 自己引用的两条先例反向: (a) `state-snapshot-schema.md:1070` 逐字「Semantic change (non-shape; **carried by plugin MINOR v1.46.0**, NOT a `snapshot_schema_version` bump)」; (b) `aria/CHANGELOG.md:84` 的 `[1.70.0]` 标题逐字「owner 裁定 D5: §2.3.5 **对采用方是行为变更 ⇒ MINOR**」—— 那一轮形态与本轮同型 (恒存在 additive 字段 `identity_advisories[]` + collision 判定变化 + 改同一份 `standards/session-handoff.md`)。本 spec 新增 `rel_path` / `unreadable_count` 两个机读字段、收窄 `legacy_count`、可使 `collision.kind` 由 `none` 翻 `cross_owner`、改 `exists` / `len(tracks)`, Impact 自述「子目录采用方可能**突然开始**看到并发碰撞告警」⇒ 按先例应为 MINOR (v1.72.0)。级别一旦定错, Task 5.1 的 16 个版本点、tag、CHANGELOG 标题全部连坐。
  *与 `019ff413` 的关系 (规则 4 保留两条)*: 本条论 SemVer **版本级别**, `019ff413` 论 OpenSpec **Level 字段**, 是两个不同的量。

- `019ff413` [major] architecture/头部 OpenSpec Level 字段 / Task 4.4 第二子模块面 — **found_by: knowledge-manager (1/5)**
  R2 rework 新增的 Task 4.4 把变更面扩到 `standards/` 子模块 (本文自述「是**第二条**同类链路」, 需独立 commit + 本地 merge + 双推 ls-remote + 主仓 gitlink bump), 加上 aria 子模块与主仓 16 个版本点, 已构成跨两子模块 + 主仓。owner 在 10 天前对同 collector 家族的相邻 spec 用的正是这条判据:「**owner 2026-09-05 裁定升 Level 3** (判据: cross-module 成立, aria + standards 两子模块)」, Level 3 交付 = proposal + tasks.md + detailed-tasks.yaml + post_planning 收敛审计。本 spec 头部仍写 Level 2, 目录内无 tasks.md, proposal.md 已达 97729 B, 且 §待 owner 复议六条里**没有 Level 这一条** (证据: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/proposal.md:3` 与其目录三文件; `spec-drafter/LEVEL_GUIDE.md:155-163` 跨模块自动提升)。

- `56845091` [major] testing/SC-10 既有测试基线的日历时效性 (Layer H 30 天窗) — **found_by: qa-engineer (1/5)**
  SC-10 把 `Ran 102 tests … OK` 钉成验收判据并明写「出现任何失败都要逐条 `git log -- <file>` 归因, **不得预先豁免**」。但点名集里 `test_handoff_multibranch_collision_dedupe.py` 有两条测试**只靠墙上时钟**: 夹具 `:381-382` 写死 `2026-08-15` / `2026-08-10`, 调用处 `:386` 未 pin `now`, 而 `lib/collision.py:225-241` 的 `layer_h_is_fresh` 按 `LAYER_H_ACTIVE_WINDOW_DAYS = 30` (`lib/constants.py:88`) 丢弃过窗行。该席实测: 今天 (2026-09-07) 21/21 OK; 把 `lib.collision.datetime.now` 换成 **2026-09-09** 后 **2 条转红** (`TestCrossOwnerRealCollisionSurvivesDedupe::test_both_latest_active_different_owners_still_reports_cross_owner` 得 `'none' != 'cross_owner'`; `TestBoardAndCollectorAgreeOnCollisionCount::test_real_collision_produces_matching_board_collision_line_count`), 零代码改动。⇒ Phase B 若在 2026-09-09 之后执行, **SC-10 结构上不可满足**, 而它给的归因手段 (`git log -- <file>`) 只能证明「本 cycle 没碰这个文件」, 说不出为什么红 —— 最省事的出路正是本文自己警告过的「顺手削断言」。
  *修法*: SC-10 基线口径补第三类既有失败的归因路径 (Layer H 30 天窗 + 夹具未 pin `now`, 附复现法), 并明确该类红**不阻断本 spec**; 是否顺手给这两条测试补 `now=` 属另一变更面, **交 owner 裁** (Rule #10, 不得由实施者临场判)。

- `17f270f5` [major] testing/SC 集缺 `collision.kind` 覆盖 — **found_by: qa-engineer (1/5)**
  本文把 `collision.kind` 由 `none` 翻 `cross_owner` 列为 (a) Rule #6 从 substitute 改判**照跑**的唯一新证据、(b) 一条独立 Impact.Risk、(c) §5 中 `SKILL.md:149/153` 闸门 / `advanced-rules.md:544` 规则 1.54 / `fetch_gate.py:175-188` 三个处方消费方的**触发条件本体**。该席独立复跑确认翻转为真 (临时仓: 顶层 `simonfish/c1` active + `archive/` `aria-runner-bot/c2` active, 同 track_id, `now=2026-09-05`; 改前 `kind=none / groups=0 / legacy_count=1 / 1 条 git_show_failed`, 枚举层交相对路径后 `kind=cross_owner / groups=1 / legacy_count=0 / 零 soft_error`)。**但 SC-1…SC-16 无一条断言 `collision.kind`, Tasks 亦无对应条目** —— 全 spec 唯一涉 collision 的 SC-7 还被明标为「假想输入的特性化测试」。⇒ 一个自认会改动、且改动面直通闸门的量, 验收上零覆盖。
  *修法*: 补 SC-17 (顶层 + 归档同 track_id 异 owner 的 hermetic 仓, 改前 `none` / 改后 `cross_owner`, **必须 pin `now`**, 入参已存在于 `handoff_multibranch.py:559`), 并记进 rule6_note 的 baseline-failing 实体。
  *正文-only 相邻信号 (规则 5)*: backend-architect 正文 decision 实测该翻转只在归档行 `updated_at` 落在 30 天窗内时成立 (把日期改到 2026-05-02 则 `kind` 回到 `none`), 并判 proposal 用「**可能**突然开始…」措辞没有过度承诺 —— 该窗口限定正是「断言必须 pin `now`」的机制根据, 两席不矛盾。

- `1ad9b4ed` [major] testing/SC-13(b) / SC-4 夹具提交日期未 pin — **found_by: qa-engineer (1/5)**
  SC-13(b) 断言「两行 `updated_at` 各自等于自己那条路径的提交日, 互不相同」, 括注只写「两文件在不同提交里落盘, 提交日期不同」, 没说怎么做到。本仓现成夹具模板 `_GIT_ENV` (`test_handoff_multibranch_collision_dedupe.py:174-183`) 只 pin 姓名/邮箱、**不 pin `GIT_AUTHOR_DATE`**, 而 `%aI` 是秒级: 该席实测同一脚本内先后两次 commit, `git log -1 --format=%aI` 对顶层与归档两条路径返回**同一值** ⇒ 基线 (拼顶层 basename 路径) 读到的也是同一日期 ⇒ (b) 在改前**也成立**, 从 baseline-failing 退化成恒绿。SC-4 的三条断言 (顶层 2026-05-09 → `git mv` 2026-08-15) 同样依赖逐 commit 可控日期。
  *修法*: 在 SC-4 / SC-13 的夹具描述里显式要求逐 commit 设 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`。

- `90e3b4b8` [major] testing/SC-11(c) 文档同步机检恒绿 (跨行 grep 零命中) — **found_by: code-reviewer (1/5)**
  SC-11(c) 用 `grep -q 'callers compose the full git-object path' collectors/handoff_multibranch.py` **无命中**来验证旧契约句已删, 但该句在基线上**就是跨行的** —— `:246` 结尾是 "so callers", `:247` 才是 "compose the full git-object path as needed."。该席实测基线 `grep -c` = **0** (并用 python 侧确认单行子串不存在、跨行形态存在) ⇒ **该判据恒绿**, 实现即使原样保留旧句也照过。它正是 v1「`grep -c basename` 计数」那条被判「不定位」的代理判据的替代品, 替代后反而更弱 (「加固动作自身重开同类洞」形态)。
  *修法*: 改 grep 单行子串 (例 `'Returns only the basename'`) 或多行匹配, 并加一条「新契约句存在」的正向断言。
  *定级备注*: 见本节 Critical 段的「待 owner / R4 复议的定级分歧」。

- `7d909571` [major] documentation/SC-15 细则布局 2 机制句是 A 案残留 — **found_by: code-reviewer (1/5)**
  `proposal.md:288` 写「去掉守卫时 writer 会写出 `[archive/x.md](./archive/x.md)`, `_parse_latest_pointer` **剥成** `x.md` 在候选集里查不到」。A′ 下 `_render_pointer` 读的是 `track.get("filename")` = basename (`latest_md_writer.py:116,143`), 无守卫时写出的是 `[x.md](./x.md)`, **没有目录段可剥**; 该 kind 仍会出现 (候选集只有 `2026-05-01-old.md`), 故**结论不变, 但机制与字面双错**。危害: 该段被本文自己声明为「夹具组成是判据的一部分」, 实施者照字面写反事实断言会断言一个永不出现的字符串, 或反向「修」成让 writer 输出 rel_path —— **那等于把 A′ 在 pointer 面上悄悄改回 A**。

- `db126eff` [major] documentation/§6.3 / Task 4.2 / SC-11(d) — `json-diff-normalizer.md:241` 是历史记述非键集契约 — **found_by: knowledge-manager (1/5)**
  本文把该行称作「显式枚举的键集」并令其补 `unreadable_count`。实读该行落在 `### tests/fixtures/reference-snapshot-aria.json` 一节 (`:196`) 里 **2026-07-18 resample 的历史记述** (`:204` 起, `:235-241` 是「两处有意偏离」的第 2 条, 过去时描述当时把 tracks 截到前 5 条)。该文档全篇无 `tracks_multibranch` 的规范性键集。照令实施 = 往一段有日期的历史记录里写入该 fixture **不可能含有**的字段 (与 R2 `e3ca1e1a` 判 major 的「照做即写入一条错误勘正」同类), 而 SC-11(d) 只 `grep -q` ⇒ **假绿**。该文档对 schema 变更的既有口径是「resample fixture + 记一条带日期的 resample 注」(`:204-215` 先例), 本 spec 既未做也未声明 defer。

- `e854a801` [major] documentation/§6.5 / SC-11(e) — `aria/CHANGELOG.md` 条目口径 — **found_by: knowledge-manager (1/5)**
  本文只要求「Fixed 三条 + Changed 两条」, SC-11(e) 也只查这五条。但本 spec 新增 `rel_path` 与 `unreadable_count` 两个**永久机读契约字段**, 且触碰 schema / json-diff-normalizer / collector docstring / (Task 4.4 落地时) standards 四类文档面。同一 collector 家族上一周期 v1.70.0 的成文口径是: 新增的恒存在机读字段列 `### Added` (`aria/CHANGELOG.md:93-97`, 例 `tracks_multibranch.collision.identity_advisories[]`), 全部触碰文档 (含 standards session-handoff.md, 标 Amended) 列 `### Changed` (`:99-100`)。照本文写法, **版本 SOT 里将查不到这两个新字段**。

- `334e62dc` [major] documentation/决策单 §落地约束 只 neutralize 一半 — **found_by: knowledge-manager (1/5)**
  头部 (`proposal.md:16`) 就 `relpath → rel_path` 声明「决策单原文写 relpath, 以本文为准」, 但同一节 (`.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` §落地约束, 标题写明「Phase B 必须遵守」) 另有两条载重错项未 neutralize: (a) 第 2 条逐字要求「写侧守卫的判据用 `relpath != filename`」—— 正是正文 §2.5 明禁的缺键恒降级写法 (R2 critical `6f8fa9f7`); (b) 第 4 条要求 SC-15 断言「子目录 track 走守卫分支且**不产生** `handoff_pointer_target_missing`」—— 在归档-only 夹具下恒绿 (R2 critical `88a49037`)。该决策单在正文中被当作规范来源引用 (SC-16 写「决策单 §落地约束第 1 条要求」, 待复议 2 请 owner 追认的对象也是它) ⇒ 属 memory `feedback_spec_inherits_upstream_dec_errors` 形态, **勘正只做一半比不做更危险**。

### Minor (7)

- `73c20653` [minor] architecture/§5 消费方枚举完整性 / 动作项无承接 — **found_by: backend-architect (risk/architecture), qa-engineer (issue/architecture), knowledge-manager (issue/documentation) (3/5)**
  §5 自称「起草时 grep 全 skill 树 + 主仓; R1 rework 逐行复核」, 且 §7「向后兼容」以该表完整性为**唯一支撑**。三席各自点出不同的未登记面, 合为一族:
  (a) backend-architect — `collision.identity_advisories`: `identity_drift_advisories` 对 `status == "legacy"` 行直接 `continue`, 故 §4 删假 legacy 行不动它 (减法为零), 但**加法有** —— 子目录件转成带真 `owner_container` 的 track 后可新增/改写 advisory (含 `first_seen` / `last_seen`); 其处方性消费面 `references/rules/advanced-rules.md:574` 与 `references/layer-l-integration.md:29` 未登记 (与 R2 `cecc06af` 同判据)。
  (b) qa-engineer — `collectors/handoff_worktrees.py`: `:82` 直接 import 复用 `handoff.py::_resolve_latest`, `:291` 对每个 worktree 调用, `:59-60` 明记会按 worktree 路径前缀发出同一条 `handoff_pointer_target_missing` ⇒ pointer 往返有**两个**读侧消费面, §5 与 SC-15 只覆盖 `collect_handoff` 一个。
  (c) knowledge-manager — §5 对 `advanced-rules.md:443-444,511-512,544` 与 `RECOMMENDATION_RULES.md:28,31` 写「须一并复核措辞」, 而 §6 与 Tasks **全无对应条目** ⇒ 该动作无人执行也无从验收; 另 `RECOMMENDATION_RULES.md:30` 的规则 1.53 (`multi_terminal_handoff_dual`, 条件含「leader pointer 仍在 latest.md」) 同样被守卫影响却未登记。
  *type / category 分歧注*: type backend-architect risk、其余两席 issue ⇒ 取多数 issue; category 两席 architecture、knowledge-manager documentation ⇒ 取多数 architecture。三席均记 minor。

- `719bf0ab` [minor] documentation/Task 4.4 / 5.2 standards 子模块链路缺基线冻结 — **found_by: tech-lead (1/5)**
  头部把 aria 基线冻结到 `301641b` 并附「两 SHA 增量实况」「五触点零 diff」实测, 严谨度很高; 但 Task 4.4 引入的**第二条子模块链路 standards** 全文无基线 SHA (该席实测 `git -C standards rev-parse origin/master` = `21748d4` = 主仓 `ls-tree HEAD standards`)。R1 / R2 各出现过一次 gitlink 相关 conflicted (`4c05b95a` / `9f7d9aff`), 根因都是缺一个写死的起点; 同型风险在 standards 侧未封。

- `cc313a28` [minor] testing/SC-10 点名模块集完整性 — **found_by: qa-engineer (1/5)**
  R2 把 `test_p1_layer_h` 补进点名集的判据是「它是唯一 import `write_latest_md` 的测试, 也是改动落点」。同一判据下仍漏: `tests/test_collision.py:439,460` (端到端真 `collect_handoff_multibranch`, 且 `:445` pin `set(coll.keys())`) · `tests/test_max_branches_resolver.py` · `tests/test_scan_integration.py` (读 `tracks_multibranch`, 而本 spec 改 `scan.py:186`)。三者目前只被尾句「全量 discover 另跑」兜底 —— 与被点名的五模块不是同一强度的判据。
  *与 `a7536535` / `b57e3209` 的关系 (规则 4 保留三条)*: 本条论**点名判据的一致性**, 那两条论「特定契约改动会确定性打红特定模块」, 主张与修法不同。

- `5e527b66` [minor] testing/SC-2 用例名与判据口径 — **found_by: code-reviewer (1/5)**
  判据已按 R2 `d02ec3f0` 改成走 `freeze_corpus.py:29` 的八字段投影 (不含 `rel_path`), 核验列的用例名却仍是 `test_flat_repo_byte_identical_to_frozen_baseline`。名字里的「byte identical」正是那条在 A′ 下恒红的旧口径, 留着会诱导后来者改回整字典比对。

- `982541e2` [minor] testing/冻结语料重生成 (risk) — **found_by: code-reviewer (1/5)**
  §7 把「两份冻结语料不需重生成」写成省事结论, 实际是**硬约束**: `tests/test_collision_frozen_corpus.py:51` 断言 `payload["fields"] == [八字段]`, `:112` 断言每行 key 集恰为那八个。若 Phase B 觉得「新增字段就该刷新语料」而用改后代码重生成, 这两条立刻红, 且该模块不在 SC-10 点名集。
  *修法*: 在 §7 或 Task 4.3 明写「不得重生成 (会打红 `test_collision_frozen_corpus`)」。
  *正文-only 相邻信号 (规则 5)*: qa-engineer 正文 decision 独立复核冻结语料 996 行 / 八字段 / 零斜杠 / 零非 ASCII, 与 `freeze_corpus.py:29` 一致 —— 支持「不重生成」是正确处置。

- `5eecd0d7` [minor] implementation/Tasks 段序号顺序 — **found_by: knowledge-manager (1/5)**
  列出顺序为 1.1 → 1.2 → 2.0 → **2.5** → 2.1 → 2.2 → 2.3 → 2.4 → … → 5.1 → **5.5** → 5.2 → 5.3 → 5.4。2.5 (消费 `rel_path` 的写侧守卫) 排在产出该字段的 2.1/2.2 之前, 按列出顺序推进则守卫与 SC-15 都无字段可读; 5.5 (AB) 排在 5.2 (合并双推) 之前亦与 Phase 顺序相反。

- `a7b3807d` [minor] documentation/§What.1 / §6.1 pointer 排除口径「未成文」表述 — **found_by: knowledge-manager (1/5)**
  §What.1 与 §6.1 称该口径「今天未成文」, 实读 `state-snapshot-schema.md:1114` **已成文** ——「the navigation pointer (`docs/handoff/latest.md`) is excluded from `_list_handoff_files` … it never appears as a `TrackEntry`」, 只是它写的是**顶层**路径, 与实际的任意深度行为不符。⇒ Task 4.1 的动作性质是**勘正一处会误导的既有句**, 不是纯新增; 按现措辞实施可能新增一句而把原句留在原地。

### Decisions (7 — 全部 minor; 按 R1 / R2 同规则**不计入**上表缺陷 severity 计数)

- `97c1c287` [minor] testing/R2 3 critical + 10 major 正文落地复核 — **found_by: tech-lead (architecture), backend-architect (testing), qa-engineer (testing), code-reviewer (testing), knowledge-manager (documentation) (5/5)**
  本轮唯一 **5/5 全席独立复核**的结论: R2 的 3 critical + 10 major (knowledge-manager / qa-engineer 另核 9 条 minor) **全部落进 v4 正文而非批注**, 未见「改一处引入另一处矛盾」的回填。抽验命中集五席一致: `6f8fa9f7` → §2.5「`rel_path` 缺失语义」行 + Task 2.5(b) + SC-15 布局 3 + SC-10 并入 `test_p1_layer_h`; `d1f01126` → §2.5 生产可达性块 + Impact.Risk 缓解范围限定 + 待复议 2 第 (4) 问; `88a49037` → SC-15 收敛为三布局 + 表后细则小节 + (f) 移出改记述性; `885edf34` → 头部 Rule #6 行与 rule6_note 双双改判照跑 + Task 5.5; `d02ec3f0` / `db0db697` → SC-2 走 `freeze_corpus.py:29` 八字段投影 + hermetic 固定分支集 + SC-16; `cecc06af` → §5 collision 行改写 + 三条处方性消费方入表; `e3ca1e1a` → Task 4.1 删 `:1125` 订正项 + SC-7 标注特性化测试; `3cb2cf2b` → §What.2 第三条订正 + SC-13 删「不折叠」; `fc925710` → SC-1/5/14/15 两个 error 面消歧; `112b4299` → SC-12a/12b 拆分; `94935605` → §6.6 + Task 4.4 + SC-11(h); `d58dfb65` → Task 5.1 十六点表 + 删除「漏改必转红」错误陈述。
  字面口径亦自洽 (tech-lead / code-reviewer 各自核): 全文守卫判据统一为 `track.get("rel_path")`, `\brelpath\b` 全树零命中, 头部保留的 `relpath` 字面只剩两处必要证据句。
  *限定 (knowledge-manager)*: 两条落地**不完整**已单列为 major (`3dd75e12` 覆盖面 / `334e62dc` 只 neutralize 一半) —— 与本 decision 不矛盾 (落地位置对, 覆盖面不足)。
  *category 多数注*: testing 3 / architecture 1 / documentation 1 ⇒ 取 testing。

- `c0d1887e` [minor] testing/载重事实独立复跑 — **found_by: tech-lead (testing), backend-architect (architecture), qa-engineer (testing), knowledge-manager (testing) (4/5)**
  四席各自实跑 (非引用), 结果互相一致且与 proposal 陈述一致: (1) SC-10 五模块在**真 checkout** `/home/dev/Aria/aria` (HEAD 实测 `301641b1c893477f387a1f85d1e90d105ebf0db9`) 得 `Ran 102 tests … OK`; (2) `ab-suite/state-scanner.json` = **17551 B**, `tracks_multibranch` 命中 **1** (`:214`, 该 prompt 的小问把 `collision.kind` 取值写死在题面 ⇒ 结构上测不到 collector 输出变化), `handoff_multibranch` / `legacy` / `basename` 均 **0**; `git show 5697477^:` = 15518 B / 0 命中, `813e82c` = 17551 B / 1 命中 ⇒ rule6_note 的机械闭合叙述准确; (3) 两份冻结语料各 996 行 / 恰八字段 / `filename` 含 `/` 为 0 / 非 ASCII 为 0, `freeze_corpus.py:29` `FIELDS` 不含 `rel_path`; (4) `git diff --name-status 0545f86 301641b` = 29 (5 A + 24 M), 同区间五触点 `--stat` 输出为空; (5) Task 5.1 的 16 个版本点逐处 `grep -n` 命中且值均 `1.71.1`; `.aria/probes/main-project-version-consistency.py:39-49` 的 POINTS 全是主项目版本行 ⇒「10 处零机械兜底」成立; (6) backend-architect 另跑 hermetic 对照: `git ls-tree` 默认对非 ASCII 名加引号 + 八进制转义而 `-z` 原样、pathspec `-- docs/handoff` 不外泄 `docs/handoff-extra/`、两条同 id legacy 行 2 进 2 出不折叠; qa-engineer 另跑 F2 静默漏扫复现与子目录仓 `scan.py` exit 10 / 假 legacy / `updated_at` 空串。
  *时效性限定 (qa-engineer, 已单列 `56845091`)*: 第 (1) 项的 102 OK 是**今日**事实, 2026-09-09 起该模块自动转红 2 条。
  *code-reviewer 计入注*: 该席把同一批机械核验并进其 `97c1c287` 条目 (标题为「R2 缺陷落地与机械底座复核」), 依规则 1 只计一次 found_by, 故本条 4/5; 其复跑结果与本条逐项一致。
  *category 多数注*: testing 3 / architecture 1 ⇒ 取 testing。

- `ed48ea12` [minor] architecture/ship 顺序 / gitlink 归属 — **found_by: tech-lead (1/5)**
  实测 `git -C /home/dev/Aria rev-parse HEAD` = `f634d837`, `git ls-tree HEAD aria` = `301641b` = `git -C aria rev-parse origin/master`, `standards` gitlink = `21748d4` = 其 origin/master; `git -C aria tag --list 'v1.7*'` 最高 `v1.71.1` ⇒ Task 5.2「gitlink 从 `301641b` 前进、严禁回退 `0545f86`」与待复议 6 的候选号未被占用两点均成立。另核 `aria-plugin-benchmarks/` **不是子模块** (`.gitmodules` 仅 standards / aria / aria-orchestrator 三条), AB 结果落主仓, **不引入第三条 gitlink 链路**。
  *与 `f658ae7e` 无矛盾*: 本条核的是版本**号**未撞与 gitlink 起点, 该 major 论的是版本**级别**。

- `a0cb3407` [minor] architecture/越界面 / 同伴容器在飞轨 — **found_by: tech-lead (1/5)**
  触点集合不含 `phase1_gate.py` / `claim_lifecycle` / `spec-drafter` / `phase-a-planner` / AB 套件本体 —— Task 5.5(b) 只**开缺口 issue**, 不改 `ab-suite/state-scanner.json`; Task 5.3 只开 issue, 不改 `handoff.py` 本体。`docs/handoff/latest.md` track 表内 `simonfish/023236f2` 各轨均 done, 在飞的只有本容器 `aria-runner-bot/bfe8285d` 的 M6 轨 (aria-orchestrator, 与本 spec 五触点零交集)。**无越界**。

- `506f2f47` [minor] architecture/A′ 骨架与真代码结构对得上 — **found_by: backend-architect (1/5)**
  自 grep 复核: 四个 git 路径消费方 (`handoff_multibranch.py:301` / `:321` / `:329-336` / `scan.py:186`) 确为全部, **无第五处硬编码前缀**; `filename` 的代码消费方恰为六处 (`scan.py:180,193,209` · `latest_md_writer.py:116,143,213`) 加 dedupe 排序键 `:455`; `legacy_count` 在 `tests/` 外零代码消费方; 全树无对 `tracks_multibranch` 精确 key set 的断言, `validate_schema_doc.py:8-23` 自述只做顶层 key 粒度 ⇒ 新增 `unreadable_count` / `rel_path` **不会机械打红既有断言**。
  *正文-only 相邻信号 (规则 5)*: code-reviewer 正文 decision「A′ 骨架代码级成立」同判 —— 守卫判据 `rel = track.get("rel_path") or track.get("filename")` 后比 `rel == filename` 对缺键、平铺、子目录三态均给出正确分支, 明言「本席不主张推翻骨架」。

- `9653395d` [minor] implementation/行号与符号引用复核 — **found_by: code-reviewer (1/5)**
  逐条实读 30 余处引用**全部命中且行号准确**: `handoff_multibranch.py` 19 处 · `handoff.py` 7 处 · `latest_md_writer.py` 7 处 · `scan.py` 6 处 · `_common.py:312-313,411-412` · `track_board.py` 5 处 · `state-snapshot-schema.md` 8 处。`_check_handoff_ancestry` 全树零命中 (R1 订正属实), `_same_branch_head_unreachable_tracks` 三处 (定义 `:126` / 拼串 `:186` / 调用 `:255`) 逐字对上。
  *正文-only 相邻信号 (规则 5)*: knowledge-manager 正文 decision「事实底座抽验」另行复核 30 余处新引用无误, 命中集与本条互补 (含 `session-closer/SKILL.md:90` · `phase-1-collectors.md:95,104` · `handoff-mechanics.md:4,116-121` · `advanced-rules.md` · `RECOMMENDATION_RULES.md` · `docs/handoff/latest.md:104-107`); 该正文条目内另有一条与 `120e1171` 相关的 conflicted 半句, 已在该 major 条目内标注。

- `c9d5df48` [minor] documentation/头部机械判据 / Rule #6 选行 / Rule #10 — **found_by: knowledge-manager (1/5)**
  `proposal.md:6` 逐字节核为 `> **Linked Issue**: ` + inline code span `10CG/Aria#195`, 行首无空白、`>` 后恰一空格、两侧各两星号、ASCII 冒号 ⇒ spec-drafter 写法三条全过 (`spec-drafter/SKILL.md:414-421`); Rule #6 落 SOT 判据表第四行「拿不准 ⇒ 照跑」并按 §4 留 `rule6_note` 引用规范, 与 `standards/conventions/skill-benchmark-exemption.md:24-28,60-64` 一致, **无 AI 自创豁免理由**; 审计计划与 `.aria/config.json` 显式 off 对齐, 落 Rule #10 白名单第一类。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **19** / Minor **7** (另 7 条 decision 不计入)。

按 `references/report-storage.md §Verdict 计算` 的 SOT 规则: `0 Critical + >=1 Major ⇒ PASS_WITH_WARNINGS`。`drift_terminated: false`, 无 override。

rationale: 本轮是三轮里**质量拐点最明显的一轮** —— R1 (2 critical) → R2 (3 critical) → R3 (**0 critical**), 且五席各自独立判定 Critical = 0。R2 的 3 critical + 10 major 经 5/5 全席逐条复核**全部落进正文而非批注、未见回填矛盾** (decision `97c1c287`), 与 R2 的交集为 **0** —— 本轮 26 条缺陷类**无一是重开 R1 / R2 已闭合项**。方案骨架 (A′ = `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git show 失败不再伪造 legacy + 写侧守卫) 被四席从不同透镜独立复核成立, 无席位主张推翻。

19 条 Major 集中在**三族**, 全部可在 Phase A 内改 spec 消解, 无一触碰设计骨架:

1. **契约改了但消费面没走完 (6 条)** — `a7536535` (`_list_handoff_files` 返回契约打红 `test_max_branches_resolver` 39 tests) · `b57e3209` (`scan.py:186` 缺键契约空白且其测试对路径无鉴别力) · `92565b30` (`write_latest_md` 的 `action` 在守卫降级后仍报 pointer) · `ebaad4a5` (legacy track_id 四处格式声明零同步项) · `b5a94a9c` (`rel_path` 被指派到错误 docstring 块并被 SC 固化) · `4608f5b2` (A′ 打破的 build-order 不变量三处文档无订正项)。
2. **验收判据自身失效 (5 条)** — `90e3b4b8` (SC-11(c) grep 在基线上零命中 ⇒ 恒绿) · `120e1171` (SC-15 的 (e)(g) 在全量回退下恒绿) · `1ad9b4ed` (SC-13(b) 在同秒双 commit 下退化恒绿) · `56845091` (SC-10 的固定基线在 2026-09-09 起结构上不可满足) · `17f270f5` (自认最要紧的行为变化 `collision.kind` 零 SC 覆盖)。
3. **文档 / 上游一致性与流程判据 (8 条)** — `db126eff` (照令即往历史记述里写错字段) · `334e62dc` (决策单 §落地约束只 neutralize 一半, 剩两条载重错项仍标「Phase B 必须遵守」) · `3dd75e12` + `2af687f5` (「单 active track ⇒ 真指针」同步面与 standards 第三态可达性) · `e854a801` (CHANGELOG 缺 Added / Changed 口径) · `7d909571` (SC-15 细则机制句是 A 案残留) · `f658ae7e` (SemVer 级别 PATCH vs MINOR 与两条先例冲突) · `019ff413` (OpenSpec Level 2 vs owner 10 天前的同型升 Level 3 判据)。

不判 FAIL 的依据: 无一条构成「方案错误」「生产消费方被打断」或「critical 级假绿」—— 第 2 族的恒绿判据均**不掩盖机制缺失本身** (每条都另有 baseline-failing 断言或可低成本补上), 第 1 族的打红面全部落在**实施期回归**而非生产路径 (`scan.py:186` 一条经 backend-architect 明确限定为「缺键在生产不可达」)。

`post_spec` 为 `blocking: false` (见 `report-format.md §阻塞行为`), 本 verdict **不阻断**后续流程; 但按 Rule #10, 上述 major 不得由实施者以「代码面小 / Level 低 / session 已长」自行降格、跳过或改序。其中 **4 条须 owner 或 R4 拍板后才进 Phase B**: `f658ae7e` (版本级别) · `019ff413` (Spec Level) · `334e62dc` (决策单勘正) · `56845091` (是否顺手给既有测试补 `now=` 属另一变更面)。

---

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 33 去重后 (Critical 2 / Major 15 / Minor 10 / Decisions 6), 去重前 60
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 2 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 31 去重后 (Critical 3 / Major 10 / Minor 9 / Decisions 9), 去重前 55; 与 R1 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**; conflicted 项 1 (`cecc06af`, 已由 rework 的 hermetic 实跑闭合, 连带把 Rule #6 由 substitute 改判照跑)
- 来源: `.aria/audit-reports/post_spec-R2-2026-09-07T004500-000Z-R2-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 3

- **Agents**: 5/5 (缺席 0; `round_incomplete: false`, `skipped_agents: []`) — tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (五席逐席自述一致; knowledge-manager 另给扫描面 —— `openspec/changes/` 8 个在制 spec 中引用 `Aria#195` 的仅本 spec, 全 `openspec/changes/` grep `handoff_multibranch` / `latest_md_writer` 亦仅本 spec)
- **Conclusions**: 去重前 **51** (tech-lead 11 / backend-architect 9 / qa-engineer 8 / code-reviewer 11 / knowledge-manager 12) → 去重后 **33** (Critical 0 / Major 19 / Minor 7 / Decisions 7)
- **Delta vs 上轮 (R2, 31 条)**: `+33 / -31` —— 四元组集合**交集 0**。R2 的 3 critical + 10 major 全部闭合 (decision `97c1c287`, 5/5 复核); 本轮 26 条缺陷类**全部为新增**, 其中 3 条是 R2 已定型缺陷族在新契约面上的复发 (`a7536535` / `b57e3209` / `cc313a28` 同属「点名集不含被改动契约的消费方测试」), 5 条落在 R2 rework 自身的下游文本 (`90e3b4b8` 是 R1 加固动作的产物; `7d909571` / `b5a94a9c` / `120e1171` / `3dd75e12` 落在 R2 新写的段落), 其余 18 条是前两轮未测到的机械事实
- **Vote 票型**: REVISE **5** / PASS **0** ⇒ `unanimous_pass = false`
- **conflicted**: 1 条 (`120e1171` —— (e) 是否有鉴别力, 两侧反事实前提不同, 可由 R4 一次 hermetic 跑闭合)
- **收敛判定 (汇总席实算, 最终由编排脚本裁决)**: `conclusions_stable = (R3 keys == R2 keys)` = **false** (33 vs 31, 交集 0); `unanimous_pass` = **false** ⇒ **`converged = false`**
- **振荡检测**: `keys_R3 == keys_R1`? **false** —— R1 为 Critical 2 / Major 15 / Minor 10 / Decisions 6, R3 为 Critical 0 / Major 19 / Minor 7 / Decisions 7, severity 分布即不相等 ⇒ `oscillation = false`
- **Duration**: N/A (编排脚本未向汇总席传递计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 3 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| 需补齐 frontmatter 的席位报告 | 0 / 5 (机械核验 15/15/15/15/15 字段) |
| 去重前/后 conclusions | 51 / 33 |
| Critical / Major / Minor | 0 / 19 / 7 |
| Decisions (不计入 severity) | 7 |
| conflicted 条目 | 1 (`120e1171`) |
| finding id 碰撞 | 0 / 33 (python3 sha256 实算) |
| 与上轮四元组交集 | 0 (R3 33 条 vs R2 31 条) |
| 收敛轮次 | N/A (未收敛) |

### 席位票型与自报计数

| 席位 | Vote | 自报 verdict | 自报 C / M / m | 结构化条目数 |
|------|------|--------------|----------------|--------------|
| tech-lead | REVISE | PASS_WITH_WARNINGS | 0 / 5 / 2 | 11 |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 2 | 9 |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 4 | 8 |
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0 / 5 / 4 | 11 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0 / 6 / 3 | 12 |

---

## Rework 清单

Critical **0** 条; Major **19** 条, 逐条列出 (id / 提出席位 / 建议动作)。动作取自各席报告原文, 汇总席**不裁决**、不新增修法。

| # | id | 席位 | 建议动作 |
|---|----|------|----------|
| 1 | `a7536535` | tech-lead · backend-architect · code-reviewer | SC-10 点名集补 `test_max_branches_resolver`; 或 Task 2.1 明写「保持 2-tuple + 注入 reporter (带默认值)」这条不破契约的实现路径, 使选型后果对实施者可见。 |
| 2 | `92565b30` | tech-lead · code-reviewer · knowledge-manager | 在 spec 内裁定三选一 (新增 `action` 取值 / 加 `degraded_reason` 键 / 明写「保持 pointer 是有意为之」); 同步 `latest_md_writer.py:277-290` docstring 与 `references/phase-1-collectors.md:102` 两处契约面; SC-15 布局 2 补一条对返回值的断言。 |
| 3 | `ebaad4a5` | backend-architect · code-reviewer | 把四处 legacy `track_id` 格式声明 (`handoff_multibranch.py:36,332,493-496` · `state-snapshot-schema.md:1104`) 纳入 §6 同步清单与 Task 4.1/4.2, 并加一条 SC-11 grep。 |
| 4 | `b5a94a9c` | backend-architect · code-reviewer | 把 `rel_path` 从「顶层键表 `:14-31`」改到 TrackEntry 块 `:33-44`, Task 4.2 与 SC-11(c) 两层同步改, 只留 `unreadable_count` 在顶层表。 |
| 5 | `120e1171` | qa-engineer · tech-lead · code-reviewer | 把 SC-15 的 (e)(g) 与布局 1 标成「过修守卫 / 回归锁」(不计入 baseline-failing 实体), rule6_note 账目相应订正; Task 1.2 的「全红」限定到其自列的四族。**并**用一次 hermetic 跑闭合 conflicted (布局 2 + 顶层留非-active 件, 分别在「全量回退」与「仅拿掉守卫」两种代码态下取 (e) 真值)。 |
| 6 | `2af687f5` | tech-lead | 二选一: 把 standards 第三态限定到「机械 writer 路径」并注明处方路径待裁; 或与 `phase-d-closer/references/handoff-mechanics.md` 同 PR 一并动。 |
| 7 | `3dd75e12` | knowledge-manager | §6 / Task 4.4 补入另外 4 处同义断言面 (`session-handoff.md:97` · `layer-l-integration.md:103` · `latest_md_writer.py:288-291` docstring · `latest_md_writer.py:140,159` 写进 latest.md 正文的那句)。 |
| 8 | `b57e3209` | backend-architect | 在 §3 / Task 2.2 显式写明 `scan.py:186` 的缺键口径 (「生产不可达, 此处不需 writer 那样的兜底」), 并把 `test_scan_integration` 纳入 SC-10 点名集。 |
| 9 | `4608f5b2` | tech-lead · backend-architect | 「不改排序键」默认支下加一条文档订正项: 把 `handoff_multibranch.py:396` / `:436-452` / `state-snapshot-schema.md:1126` 的 build-order 不变量限定为「同 `rel_path` 前提下」, 与「改排序键」支互斥。注意勿波及 `:1125` (A′ 下仍为真)。 |
| 10 | `f658ae7e` | tech-lead | 待复议 6 补论版本**级别**: 按 `state-snapshot-schema.md:1070` 与 `aria/CHANGELOG.md:84` 两条先例应为 MINOR (v1.72.0); 级别改动连坐 Task 5.1 的 16 个版本点 / tag / CHANGELOG 标题。**须 owner 裁**。 |
| 11 | `019ff413` | knowledge-manager | 把「Level 2 vs Level 3」列入 §待 owner 复议; 若升 Level 3 则补 tasks.md + detailed-tasks.yaml + post_planning 收敛审计。**须 owner 裁**。 |
| 12 | `56845091` | qa-engineer | SC-10 基线口径补第三类既有失败的归因路径 (Layer H 30 天窗 + 夹具未 pin `now`, 附复现法) 并明确该类红不阻断本 spec; 是否给既有测试补 `now=` 属另一变更面, **须 owner 裁** (Rule #10)。 |
| 13 | `17f270f5` | qa-engineer | 补 SC-17: 顶层 + 归档同 track_id 异 owner 的 hermetic 仓, 改前 `collision.kind = none` / 改后 `cross_owner`, **必须 pin `now`** (入参 `handoff_multibranch.py:559`); 并把它记进 rule6_note 的 baseline-failing 实体。 |
| 14 | `1ad9b4ed` | qa-engineer | 在 SC-4 / SC-13 的夹具描述里显式要求逐 commit 设 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`。 |
| 15 | `90e3b4b8` | code-reviewer | SC-11(c) 改 grep 单行子串 (例 `'Returns only the basename'`) 或多行匹配, 并加一条「新契约句存在」的正向断言。定级分歧 (major vs critical) 待 owner / R4 复议。 |
| 16 | `7d909571` | code-reviewer | 订正 `proposal.md:288` 的机制句: A′ 下无守卫时写出的是 `[x.md](./x.md)` (无目录段可剥), kind 仍出现是因候选集只有 `2026-05-01-old.md`; 勿让实施者据 A 案字面写断言或把 writer 改回输出 rel_path。 |
| 17 | `db126eff` | knowledge-manager | §6.3 / Task 4.2 / SC-11(d) 撤回「往 `json-diff-normalizer.md:241` 补 `unreadable_count`」; 该行是 2026-07-18 的历史 resample 记述, 正确口径是「resample fixture + 记一条带日期的 resample 注」(`:204-215` 先例) 或显式声明 defer。 |
| 18 | `e854a801` | knowledge-manager | §6.5 / SC-11(e) 按 v1.70.0 成文口径补 `### Added` (`rel_path` / `unreadable_count` 两个恒存在机读字段) 与 `### Changed` (全部触碰文档, 含 standards 标 Amended)。 |
| 19 | `334e62dc` | knowledge-manager | 对决策单 §落地约束第 2 条 (判据写 `relpath != filename`) 与第 4 条 (SC-15 断言在归档-only 夹具下恒绿) 补 neutralize —— 与已做的字段名 neutralize 同处; 该节标题为「Phase B 必须遵守」, 半截勘正比不勘正更危险。**建议由非原作者执笔** (memory `feedback_author_and_verifier_must_differ_for_corrections`)。 |

> **Minor 与 Decisions 不进 Rework 清单** (7 条 minor 见上文 `### Minor (7)` 各条内附修法; 7 条 decision 为核实通过项, 无动作)。
