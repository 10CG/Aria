---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T02:05:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — handoff-multibranch-subdir-path-fidelity (Round 2)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文**逐字**落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager); 五份 frontmatter 15 字段齐全 (机械核验: 逐文件 awk 抽 frontmatter 后 `grep -c '^[a-z_]*:'` = 15/15/15/15/15), **0 份需补齐**。

**合并规则 (本轮实际执行, 与 R1 聚合报告同规则, 供 Round 3 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 (例: 本轮「SC-12 子目录仓半条的判据强度」与「Impact 首行 vs SC-12 的 exit 0 承诺」是两条)。
5. 席位**报告正文有、结构化清单未列**的条目 (本轮: backend-architect 正文 Decisions 的「F1 与四处硬编码前缀复核」「Rule #6 结论侧复核」、正文 Risks 的两条 minor; tech-lead 正文的 A′ 骨架 decision 与 `relpath` 契约 risk) **不计入** `found_by`, 但在相应条目内注明, 以免 Round 3 丢失该信号。
6. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (31 条全部唯一, 0 碰撞)。
7. 本轮去重前 **55** 条 (tech-lead 10 / backend-architect 11 / qa-engineer 11 / code-reviewer 11 / knowledge-manager 12), 去重后 **31** 条。

---

## 审计结论

### Critical (3)

- `6f8fa9f7` [critical] implementation/§2.5 守卫判据 relpath 缺失语义 / Task 2.5 / SC-15 / SC-10 回归范围 — **found_by: backend-architect (issue/critical/implementation), tech-lead (issue/major/implementation), code-reviewer (issue/major/implementation), knowledge-manager (risk/major/architecture) (4/5)**
  Task 2.5 把守卫判据钉死为 `relpath != filename` 并禁用字符串嗅探, 但**四席一致指出 spec 未定义 `relpath` 键缺失时的行为** —— 缺键取 `None`, 判据恒真 ⇒ 走 `_render_pointer_unavailable`, 而该函数只渲染 track_id 不含文件名 (`latest_md_writer.py:151-169`)。backend-architect 是唯一做了执行探针的席位: 用 `tests/test_p1_layer_h.py:230-240` 的 `_active_track` 形状 (八字段 dict, 无 `relpath`) 跑打了守卫的 `write_latest_md`, 输出行变成 `**Latest**: (pointer 不可用) — track=my-spec`, `:270` 的 `assertIn("2026-05-20-my-spec.md", content)` 由绿转红; 该模块当前基线为绿 (三席各自实跑 `Ran 24 tests … OK`)。
  三层后果, 四席分别给出不同触发路径: (a) 既有夹具翻红, 而 **SC-10 点名的 4 个模块不含 `test_p1_layer_h.py`** —— 它恰是全树唯一 import `write_latest_md` 的测试, 也正是 §2.5 的改动落点 (tech-lead / backend-architect / code-reviewer); (b) **跨版本读盘**: `session-closer/SKILL.md:90` 明确允许「跑 scan.py 取 snapshot **或读既有 `.aria/state-snapshot.json`**」, 升级前写下的快照每行 track 都没有 `relpath` ⇒ 平铺仓 (含 Aria 自身) 每条 active track 被判「在子目录」, 真指针被吞、写出理由为假的降级横幅, `handoff.py` 随即由 pointer 退回 mtime —— knowledge-manager 判其**重开 H5「pointer 是语义权威」那条既有修复**, 与 R1 critical `63d1ce08` 同族, 只是触发条件从「子目录布局」换成「快照跨版本」; (c) SC-15 的两个布局都在同一次运行里由新 collector 端到端产出, `relpath` 恒在 ⇒ **结构上覆盖不到缺失分支** (backend-architect / knowledge-manager)。
  code-reviewer 另点出一处 Task 2.5 未列的契约变更: `_render_pointer_unavailable(track_id, now)` (`latest_md_writer.py:151`) 现签名与硬编码原因文案 (`:164`) 装不下「目标在子目录」的新原因, 必须改签名或新增函数 (backend-architect 正文 Risks 有同判条目, 依规则 5 未计入 found_by)。
  *type / category / severity 分歧注*: type 三席 issue、knowledge-manager risk ⇒ 取 issue; category 三席 implementation、knowledge-manager architecture ⇒ 取 implementation; severity backend-architect critical、其余三席 major ⇒ 按规则 1 取最高。
  *修法 (四席各提, 汇总席不裁决)*: §2.5 明写「`relpath` 缺失 ⇒ 按 `relpath = filename` 处理 (老快照即平铺世界), 照写真指针」; SC-15 补第三条断言 (无 `relpath` 键的 track ⇒ 仍写真指针); SC-10 点名集并入 `test_p1_layer_h`; Task 2.5 补 `_render_pointer_unavailable` 签名变更。

- `d1f01126` [critical] architecture/latest_md_writer 生产可达性 / §2.5 守卫落点 / 待复议 2 代价陈述 — **found_by: tech-lead (issue/critical), backend-architect (issue/major), code-reviewer (issue/major), qa-engineer (risk/minor) (4/5)**
  §2.5 写侧守卫加在 `write_latest_md` 上, 而该函数**全插件树零生产调用点** —— 四席各自 grep 得同一命中集: 函数自身 / `writers/__init__.py` 的再导出 / `tests/test_p1_layer_h.py` / 两份 reference 文档, 排除 `tests/` 后为空。这不是遗漏而是既有设计决定: `references/phase-1-collectors.md:95` 逐字写「`latest_md_writer` 是 **deliberately D.3-scoped** —— 不在 scan.py 内自动触发, **不在 P1 内引入 production call-site**」, `:104` 把 D.3 集成推给「TASK-029 或独立 follow-up」(至今未落地), `references/layer-l-integration.md:101,107` 同。**生产 D.3 的 pointer 写入是 AI 按处方指令手改**: `phase-d-closer/references/handoff-mechanics.md:114-124` 的 3 行决策表, 且 `:4` 声明该文档是 phase-d-closer 与 session-closer 共享的 handoff-write 机制 SOT; 两个 closer 目录对 writer 零引用 (tech-lead)。code-reviewer 另举本仓自证: `docs/handoff/latest.md:103-107` 明记「机械 `latest_md_writer` 当前不可用」并声明这是一处对约定的有意偏离。
  四席一致的后果: proposal 通篇以「D.3 写出的 pointer」为既成时态描述失败面, 据此把 pointer 往返定为「本 spec 引入的新失败面」、据此裁 A′、据此把 SC-15 计入 rule6_note 的第十条 baseline-failing 实体、据此向 owner 要「子目录采用方只拿降级 pointer」的代价确认 —— 而**这个代价目前无人在付** (qa-engineer), Impact.Risk 的缓解承诺「使这类指针压根不写出」在生产路径上为假 (tech-lead, 属 memory `feedback_completion_signals_vs_runtime_invocation` 形态)。
  *席位分歧 (不构成 conflicted, 无席位主张相反结论)*: code-reviewer 与 qa-engineer 明记「守卫本身依然值得做 (writer 是已发布的公开 API / 一旦接线即命中)」, 只要求写明可达性; tech-lead 走得更远 —— 它认为可达性同时决定「Task 2.5 该不该做」与「若要真修生产面, 落点是 `handoff-mechanics.md` 的处方决策表 = **运行时指令面** ⇒ Rule #6 须照跑 AB」, 而 rule6_note 的免跑论据只 grep 了 state-scanner `SKILL.md`, 从未审视 phase-d-closer / session-closer 指令面。该 Rule #6 侧的推论与 `cf0c9dcb` (knowledge-manager 判 substitute 成立) 前提不同 (TL 论的是假设扩大后的范围, KM 论的是当前范围), 汇总席不判其矛盾, 但两者应一并交 owner。
  *severity 分歧注*: tech-lead critical / backend-architect / code-reviewer major / qa-engineer minor(risk) ⇒ 取最高 critical; type 三席 issue、qa-engineer risk ⇒ 取 issue。

- `88a49037` [critical] testing/SC-15 子目录布局夹具组成 / (e)(f) 断言与反事实 — **found_by: qa-engineer (critical), tech-lead (major), code-reviewer (major) (3/5)**
  SC-15 是 A′ + 写侧守卫这次 AI 裁定的**唯一端到端验收**, 但它只写「唯一 active track 的文件在 `archive/`」, 未规定顶层是否仍留 `.md` —— 三席各自指出两种夹具下断言含义相反, 而按字面取最小夹具 (归档-only) 时两条断言同时失效:
  (a) **(e) 恒绿, 其反事实为假**: `handoff.py::_scan_md_files` 非递归且过滤 `latest.md` (`:300,318,323`) ⇒ `canonical_files` 为空 ⇒ `collect_handoff` 在 `:438-451` 早返回, `_resolve_latest` (`:455`) 根本不执行 ⇒ `handoff_pointer_target_missing` (`:397-404`) 结构上不可能产生, 与守卫有没有实现无关。SC-15 写明的反事实「去掉 §2.5 守卫 ⇒ (e) 因该 soft_error 出现而红」被证伪。qa-engineer 做了 hermetic 实测 (subdir-only + 指向 `archive/x.md` 的 latest.md): `handoff.exists=False`, `latest_source=None`, **soft errors=[]**。
  (b) **(f) 恒红且不可满足**: 路径修好后子目录件变成真 track ⇒ `tracks_multibranch.exists=True`, 而非递归扫描使 `handoff.exists=False` ⇒ 「两个 collector 的 exists 不互相矛盾」在有守卫时**仍为假** (守卫只管 latest.md 写什么)。这正是 R1 critical 里那条「零 soft_error 自相矛盾」, 本文自己已把它推给 Task 5.3 另开 issue。tech-lead 另指 (f) 未给可执行谓词, 「不互相矛盾」由实施者自定 ⇒ 不可证伪。
  qa-engineer 的裁断口径最重: **本轮新增的机制, 其验收既抓不住机制缺失 (e 恒绿), 又要求实现做到方案明说不做的事 (f 恒红)**, 而 (f) 恒红正是「改断言就范」的诱因。tech-lead 另指 rule6_note 已把 SC-15 计入 baseline-failing 实体第十条, 该计数随之失准。
  *修法 (三席一致)*: 夹具明确成 §5 的 sub-case (a)「子目录 active + 顶层另有一份非-active `.md`」使候选集非空; 或把 (f) 改写成「矛盾时必须有信号」这类可满足谓词。
  *severity 分歧注*: qa-engineer critical / tech-lead / code-reviewer major ⇒ 取最高。

### Major (10)

- `885edf34` [major] documentation/rule6_note 套件覆盖实测 / 头部 Rule #6 判定行 (ab-suite 四词零命中) — **found_by: tech-lead (testing), backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  头部 Rule #6 行 (proposal.md:12) 与 rule6_note (:244) 两处均称 `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` **四词零命中**。**五席各自 grep, 无一例外测到 `tracks_multibranch` 命中 1 次** (`aria-plugin-benchmarks/ab-suite/state-scanner.json:214`), 另三词确为 0; 命中处是协调闸门用例的 prompt, 问「本次扫描的 `tracks_multibranch.collision.kind` 是空的 —— 这会改变 (A) 的答案吗」。本轮唯一 **5/5 全席独立命中**的 finding。
  文件层面: 现为 17551 B (tech-lead / backend-architect / knowledge-manager 各自实测), 由 commit `5697477` (2026-09-05T14:12Z) 引入该用例; R1 decision `0f9dc120` 记的「四席实测全 0 / 文件 15518 B」与现场两项都对不上 ⇒ R1 的四席交叉核验失效, v3 原样继承 (memory `feedback_spec_inherits_upstream_dec_errors`)。
  *席位对「R1 为何测错」的解释分歧 (不构成 conflicted, 结论一致)*: qa-engineer 记「15518 B 正是该 commit 前的版本 ⇒ R1 四席与本 spec 都是对**改前副本**测的」; knowledge-manager 记「在 `813e82c` (R1 审计所见树) 上同样为 1」, backend-architect 记「最后提交早于 R1」⇒ 指向 R1 席位读了陈旧的插件 cache 副本。两种解释相容, 均可在 R3 用一条 `git show <R1 树>:` 机械闭合。
  *结论侧 (四席一致, qa-engineer 附条件)*: substitute 判定本身仍站得住 —— 命中句问的是 heartbeat/闸门触发条件, 本 spec 不改 `collision.kind` (`lib/collision.py:483-486` 的 collidable 过滤本就排除 `owner_container == "unknown"`, 三席各自复核)。**但 qa-engineer 要求把它与 `cecc06af` (闸门面是否受影响) 一并重判「照跑 vs 豁免」** (CLAUDE.md Rule #6「拿不准 → 照跑」/ Rule #10 不得以价值评估自行豁免)。knowledge-manager 给了具体改写: 证据句改成「唯一命中落在闸门面 `SKILL.md:149/153`, 而本 spec 三处均不改」。四席一致按 audit-points 横切「数据可用性」条款载重 REVISE, 不能只记一笔。
  *category 分歧注*: tech-lead 记 testing, 其余四席记 documentation ⇒ 取多数 documentation。

- `d02ec3f0` [major] testing/SC-2 / SC-12 零差异断言与 A′ 新键 relpath 豁免清单 — **found_by: backend-architect, code-reviewer (2/5)**
  2026-09-07 的 A′ 修订给**每一行** TrackEntry 新增 `relpath`, 但两条「零差异」断言没跟着改: SC-12 (proposal.md:234) 逐字写「除 `unreadable_count` 新键外**零差异**」, SC-2 (:224) 写「`tracks[]` / `legacy_count` **逐字段相等**」且用例名为 `test_flat_repo_byte_identical_to_frozen_baseline`, Impact.Risk 第 6 条 (:191) 同写「与改前**逐字节相同**」。改前基线由无 `relpath` 的旧代码产出 ⇒ 三处断言在**采纳的设计下恒红**, 与其自称的反事实「解析写错才红」相矛盾 (memory `feedback_spec_rework_leaves_downstream_ac_drift`)。
  code-reviewer 另给唯一逃生口与其缺口: 除非 baseline 与改后输出都经 `tests/fixtures/freeze_corpus.py:29` 的八字段投影 (`FIELDS` 硬编码, 不含 `relpath`), 而 SC-2 只说「用它的形态」没说走投影; 并指出决策单 §落地约束第 1 条要求「平铺仓 `relpath == filename` 要有一条 SC 钉住」, 现 SC 集**无任何一条承接** (tech-lead 正文 Risks 有同判条目, 依规则 5 未计入 found_by)。code-reviewer 警示这类假红最危险的下场是实施者顺手削断言。

- `db0db697` [major] testing/SC-2 / SC-12 基线的 origin 时变性 — **found_by: backend-architect (risk) (1/5)**
  R1 `37de67cd` 把基线从活文件改成「同工作区双跑」, 但没治时变的**根**: collector 枚举全部 `refs/remotes/origin/*` (`handoff_multibranch.py:202-208`, 按 committerdate 排序取 cap), `tracks[]` 从不去重、每 (branch, file) 一行 (模块 docstring `:14`,`:54`)。主仓 `docs/handoff/` 现有 190 份顶层 `.md` (实测) ⇒ Phase B 一旦把 feature 分支推上 origin, 「改后」那次扫描就凭空多约 190 行; 同伴容器往 master 推交接同样加行, 而 Phase 0.5 `remote_refresh` 的 `fetch --prune` 保证看到最新态。SC-12 的「零差异」与 SC-2 的活体变体因此仍会假红。修法: 固定分支集 (离线模式 / 只比 before 分支集内的行 / hermetic 临时仓), 而非只换基线的落盘位置。
  *scope 不合并注*: 与 `d02ec3f0` 锚在同一对 SC, 但语义不同 (前者是「新键未豁免 ⇒ 恒红」, 本条是「环境噪声 ⇒ 假红」), 依规则 4 保留两条。

- `cecc06af` [major] architecture/§5 消费方枚举 / 闸门面结论 / §7 向后兼容 — **found_by: backend-architect, qa-engineer (2/5)** — **conflicted: true**
  两席一致: §5 消费方枚举表不完整, 而**该表的完整性正是 §7「向后兼容」的唯一支撑** (backend-architect)。§4 把「读不到」的行移出 `tracks[]` 会同时改动 `exists` (= `len(tracks) > 0`, `handoff_multibranch.py:748`) 与 `len(tracks)`, 而 §5 与 §7 只讨论了 `filename` / `track_id` / `legacy_count` / `unreadable_count`。两席合计点出的未列消费方 (全部是**处方性 AI 判定面**): `references/rules/advanced-rules.md:443-444` (`multi_terminal_follower_detected`, 触发条件 = `exists: true` + `len(tracks) >= 2`) 与 `:511-512` (D.3 follower 规则同条件) 与 `:544`; `RECOMMENDATION_RULES.md:28,31` (规则 1.51 / 1.54); `phase-d-closer/references/handoff-mechanics.md:116-121` 的 D.3 pointer 决策表 (读 `exists` / `len(tracks)` / 「其他 container 有 status==active」, 三个量本 spec 全动); `phase-d-closer/scripts/fetch_gate.py:175-188` (吃 `collision_kind` 出 verdict)。
  **conflicted 的那半 —— 闸门面是否受影响**: qa-engineer 判 §5 与 rule6_note 的「闸门面 (`SKILL.md:149`/`:153`) 不受影响」**不成立**, 理由是该结论只算了删掉的假 legacy 行 (`owner_container` 恒 unknown, 被 collidable 过滤排除), **没算新增的真 track** —— 路径修好后子目录里带合法 frontmatter 的交接会带着真 owner_container 进入 collidable; hermetic 实测: 同一 track_id 下「顶层 simonfish/… active + `archive/` aria-runner-bot/… active」今天是 `collision.kind = none`, 修好后是 `cross_owner` (groups 两个成员), 而 `collision.kind` 非空正是闸门触发条件本身。backend-architect 就同一命题在其 Decisions 第 5 条判**核验通过**:「`lib/collision.py:483-486` 的 collidable 过滤确实排除 `owner_container == "unknown"` ⇒ 删掉假 legacy 行不动 `collision.kind`, 闸门面不受影响 —— 该结论成立」; tech-lead 在 `d1f01126` 条目内、knowledge-manager 在 `cf0c9dcb` 的选行论据里各持同一表述。
  *汇总席记 (不代替裁决)*: 双方对**机制事实**无分歧 —— 都同意删掉的假 legacy 行不动 `collision.kind`; 分歧在**是否穷举了改动的方向**: 一侧只量了「减法」(删假行), 另一侧还量了「加法」(新增真 track 带真 owner_container)。这是**可机械闭合**的冲突: R3 在一个含「顶层 + `archive/` 同 track_id 异 owner_container」的临时仓上跑一次改前/改后 `collision.kind` 即可定案。若 qa-engineer 成立, 则 `885edf34` 的 Rule #6 substitute 判定须连带重判。
  *type / category 注*: 两席均记 issue/architecture, 无分歧; conflicted 来自 backend-architect 的 decision 侧表述与 qa-engineer 的 issue 相反。

- `e3ca1e1a` [major] documentation/Task 4.1 / SC-7 / Task 3.2 的 A 案遗留 (schema :1125 tie-break 论据) — **found_by: tech-lead (architecture/major), code-reviewer (documentation/major), qa-engineer (documentation/minor) (3/5)**
  A′ 下 `tracks[].filename` 恒为日期前缀 basename, 因此 `state-snapshot-schema.md:1125` 原句「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one among same-day files」**并未变假** (tech-lead / code-reviewer 各自实读原文)。但 **Task 4.1 (proposal.md:209) 仍把「`:1125` tie-break 论据订正」写成无条件必做项** ⇒ 照做等于把一条正确不变量改成错的 / 往 schema 里写一条错误勘正。§6 第 1 条与 Impact.Risk 第 1 条已条件化成「A 案下」, §5 dedupe 行已标「A′ 案下无此面」, **任务面没跟上** —— memory `feedback_spec_rework_leaves_downstream_ac_drift` 的典型形态。
  同族第二半: **SC-7 / Task 3.2** 要求构造 `filename = "archive/2026-07-19-x.md"` 的 track 行, 而该取值在 A′ 的真实输出里**结构上不可能产出** (三席一致) ⇒ SC-7 退化成对手搓 dict 的行为记录。修法 (三席一致): SC-7 与 Task 3.2 显式标注「假想输入的特性化测试」或随 A 案一并删除; Task 4.1 的 `:1125` 订正改成条件式或删除。qa-engineer 补一句风险口径:「留着不算有害 (dedupe 键与 track_board 共享), 但理由需改写, 否则 Phase B 会照一个已失效的前提改 schema」。
  *category / severity 分歧注*: category tech-lead architecture、code-reviewer / qa-engineer documentation ⇒ 取多数 documentation; severity 两席 major、qa-engineer minor ⇒ 取最高。

- `3cb2cf2b` [major] testing/SC-13 legacy dedupe 反事实 — **found_by: qa-engineer (1/5)**
  SC-13 (proposal.md:235) 的「`dedupe_latest_per_track_container` **不折叠**」断言与其反事实「沿用 basename ⇒ 两行同 id ⇒ 折叠成一条 ⇒ 红」被代码直接证伪: `status == "legacy"` 的行在 `handoff_multibranch.py:521-524` 被 `continue` 掉、**从不进入分组**, 所以两条 id 完全相同的 legacy 行今天也不会折叠 (实测: 2 行进 → 2 行出, `legacy_passthrough=2`)。该行为在 docstring `:493-499` 与 `state-snapshot-schema.md:1128` 都是明文契约。
  连带: §What.2 第三条 (proposal.md:113)「今天会产生同一个 `legacy:<branch>:x.md`, **被 `dedupe_latest_per_track_container` 当成同一 track 折叠**」是**事实错误** —— 前半对, 后半不成立。SC-13 尚靠「两条不同 `track_id`」那半保住 baseline-failing 资格, 但 rule6_note 把它列进 substitute 实体时依据的是被证伪的那半。
  *与 R1 的关系*: SC-13 本身是 R1 `7d76ccad` 的处置产物 —— 属「加固动作自身重开同类缺口」形态 (memory `feedback_multiround_audit_catches_fix_introduced_regression`)。

- `fc925710` [major] testing/SC-1 / SC-5 / SC-14 / SC-15 的 errors[] 指代 — **found_by: qa-engineer (1/5)**
  本 collector 有两个同名 error 面, 而 SC 表全部裸写 `errors[]`: `tracks_multibranch.errors[]` (= `r.data["errors"]`, `handoff_multibranch.py:753`) 只装**消息串**; soft_error 的 kind 只进 `CollectorResult.errors` (`_common.py:312-313` 的 `{"error": kind, "detail": …}`), 最后由 `scan.py:382-383` 汇进顶层 `errors[]`。qa-engineer 实测 `data["errors"][0]` = `"[master/…] git show failed: git show failed for origin/master:docs/handoff/… (other, rc=128)"` —— **不含** `handoff_multibranch_git_show_failed` 字面。
  按 §Why/§4 的上下文实施者最可能读成前者, 于是 SC-5 (:227)「`errors[]` **含** `handoff_multibranch_git_show_failed`」**不可满足 (恒红)**, SC-1 (:223)「**不含**」在 `301641b` 上即为真 (**恒绿**, 违反 Task 1.2「对 301641b 全红且红在正确断言上」)。SC-15 的 (c)(e) 又指的是 `collect_handoff` 的 `CollectorResult.errors` (其 `data` 根本没有 errors 键) ⇒ 同一张表里两种含义。

- `112b4299` [major] testing/SC-12 子目录仓半条 (恒绿断言 + 非判据式失败模式) — **found_by: qa-engineer (1/5)**
  两处失效。(1) 「soft_error 里…也无 `handoff_pointer_target_missing`」在全子目录布局下**结构上不可能产生** (与 `88a49037` 同机制: `handoff.py:438-451` 提前返回) ⇒ 恒绿断言; 若改成有顶层旧件的布局才有鉴别力, 但 SC 未写。(2) 「**断言 exit 0**; 若实跑非 0, 逐条抄下 kind 并在 handoff 说明 (不得改断言就范)」—— 失败模式是「记录」不是「转红」, 该半条因此**不是验收判据**。
  修法: 顶层布局断言 exit 0, 子目录布局只断言「不出现 `handoff_multibranch_git_show_failed`」, pointer 相关断言全部让给 SC-15。
  *scope 不合并注*: 与 `90a5604b` (Impact 首行 vs SC-12 的 exit 0 承诺) 锚在同一条 SC, 但一条是判据强度、一条是上下游指示相反, 依规则 4 保留两条。

- `94935605` [major] documentation/§6 文档同步 (Rule #3) — standards SOT 缺失 — **found_by: knowledge-manager (1/5)**
  Rule #9 的 SOT (`standards/conventions/session-handoff.md:171-173`) 把 latest.md 派生行为写成**穷尽两态**: 「单 track 场景 (1 active track): `latest.md` 写当前 track 指针」/「多 track 场景 (≥2 active): 仅 deprecation banner」。§2.5 的写侧守卫引入**第三态** (单 active track 但文件在子目录 ⇒ 不写真指针, 走降级并写明原因) ⇒ 落地后该无条件表述对子目录采用方即为假。§6 的五条同步清单与 Task 4.1/4.2 **全部只覆盖 aria 插件内文档, 无一条指向 `standards/`**; 该文件在共享子模块内, 影响所有采用方。
  修法: 纳入 §6 与 Tasks; 若判定本轮不改 standards, 也须在 spec 内显式写成 deferred 并说明理由 (Rule #5 允许规范自身变更落 standards 仓, 但会带出 standards 版本与 gitlink 同步面, 属实施面成本, 应在 Tasks 里可见)。

- `d58dfb65` [major] documentation/Task 5.1 发布同步面 + 三条 check 兜底断言 — **found_by: knowledge-manager (1/5)**
  本仓 aria-plugin 版本引用点实测共 **16 处** (`CLAUDE.md:139,141` · `README.md:8,242` · `README.zh/ja/ko.md:3,10,244` 各 3 处 · `VERSION:24` · `system-architecture.md:189` · `version-scheme.md:23`), 与上次发版 commit `4c3c826` 自述的「16 处版本点」逐一对上。**Task 5.1 只列其中 7 处**, 漏: 主仓 `VERSION:24` (CLAUDE.md:81「发布同步面」逐字列出「主仓 VERSION」) / `CLAUDE.md:139,141` / 三份 i18n README 的 badge (`:10`) 与正文版本行 (`:244`) 共 6 处 (Task 5.1 对 i18n 只提 `translated-from` marker)。
  更要紧的是**兜底断言不成立**: `m6-version-badge-match` 的命令是 `grep -m1 … README.md` 只看首个 badge; `i18n-readme-translation-currency` 只正则 `translated-from`, 不读 i18n 正文 (与 memory `feedback_version_checks_blind_to_i18n_readme_body` 完全同型); `plugin-version-arch-docs-match` 只比两处架构行; 另一条 `main-project-version-consistency` 的 POINTS 清单全是**主项目 1.7.5** 那条线, 不含插件版本行 ⇒ 含 `README.md:242` 在内的 **10 处零机械兜底**, 「漏改必在归档闸转红」这句会给实施者假安全感 (证据: `.aria/state-checks.yaml:88-102,141-182,289-316,372-399`; `.aria/probes/main-project-version-consistency.py:39-49`)。
  *与 R1 的关系*: R1 `6b713e2f` 已要求补该同步面, v3 补了 7 处但未补全, 且新增的「三条 check 兜底」断言本身是新引入的错误陈述。

### Minor (9)

- `28f9d80c` [minor] testing/SC-1 / SC-8 保留 A / A′ 双分支断言 (未就地 neutralize) — **found_by: tech-lead (testing), knowledge-manager (documentation) (2/5)**
  A′ 已裁定 (Task 2.0 勾选, 决策单在案), 但 SC-1 (:223) 与 SC-8 (:230) 仍并列两套断言取值, 唯一消歧句在候选表下方的裁定注 (:91)「保留双分支供复议对照, 实施以 A′ 为准」。tech-lead: 对 §Why / §5 的**记述面**成立, 但**验收判据保留二义会让实施者可挑低约束那支**, SC 应单值化到 A′。knowledge-manager: 审计要点里 amendment 的 neutralize 要求正是针对这一失效模式 —— 读者停在原文断言处不会回头看上游说明; 建议就地划除或加「见裁定注」标记。
  *category 平票注*: tech-lead testing / knowledge-manager documentation, 1-1 平票, 按席位序取 testing。

- `e03d8a32` [minor] documentation/schema :1136 fail-soft 形状 drift / Task 4.1 / §6 文档同步 — **found_by: backend-architect, qa-engineer, knowledge-manager (3/5)**
  Task 4.1 要在 `state-snapshot-schema.md:1136` 的 fail-soft 形状补 `unreadable_count`, 但该行现把 `collision` 写作 `{"kind": "none", "groups": []}`, 而代码早退 dict 实为 `{"kind", "groups", "identity_advisories"}` (`handoff_multibranch.py:593`) ⇒ 改到同一行却把既有漂移原样留下, 与本 spec「契约与实现对齐」的立意相左 (三席一致; qa-engineer 补「本 spec 正是为『恒存在不变量在错误路径上要成立』才动这一行, 只补一半会留下另一个错误形状」)。
  knowledge-manager 另有同条目第二半 (依规则 1 并入本条, 保留记述): `state-snapshot-schema.md` 的 `## Change history` 表既有口径是**每次 schema 变更加一行** (H5 pointer / #134 / #141 / Task 10.1 逐条在列), 本 spec 新增 `unreadable_count` 与 `relpath` 却未把该行列入同步项 (证据: `:1156-1168`)。

- `7cba5aa4` [minor] testing/SC-10 回归模块清单漏 test_p1_layer_h — **found_by: code-reviewer (1/5)**
  SC-10 点名的 4 模块 code-reviewer 实跑复核为 `Ran 78 tests ... OK` (与 proposal 一致, R1 `60e465ad` 的修复有效), 但 v3 新增的 Task 2.5 改的是 `latest_md_writer.py`, 而全树唯一 import `write_latest_md` 的测试是 `tests/test_p1_layer_h.py` (24 tests, 实跑 OK), **不在这 4 个模块里**; 现只靠 SC-10 尾句「全量 discover 另跑并与改前基线逐条对比」兜底。建议并入点名集 —— 它正是 `6f8fa9f7` 会翻红的地方。
  *scope 不合并注*: tech-lead 与 backend-architect 在 `6f8fa9f7` 条目内附带点出同一事实, 但其 scope 主体是守卫判据语义; 本条 scope 主体是 SC-10 点名集本身, 依规则 4 单列, found_by 只计 code-reviewer。

- `90a5604b` [minor] documentation/Impact 首行 vs SC-12 的 exit 0 承诺 — **found_by: tech-lead (1/5)**
  Impact 第 1 条 Positive (proposal.md:184) 仍写「不能承诺不再恒 exit 10 …… 该承诺的最终范围由待复议 2 的裁决决定」, 而待复议 2 已在 v3 裁定 (A′ + 守卫) 且 SC-12 (:237) 已改成「断言 exit 0」⇒ 裁定后未回头同步该行, 实施者拿到两条相反指示。

- `b5d25ad4` [minor] documentation/§7 additive 声明 / 待 owner 复议 2 — **found_by: backend-architect (1/5)**
  「A 案改既有字段取值语义**不属 additive**, 与 `snapshot_schema_version` 保持 1.0 不相容」与 SOT 自身不符: `state-snapshot-schema.md:46-48` 的 Additive/Breaking 两档只列「新增键 / 改名 / 改类型 / 删键 / 可选转必填」, 取值语义变更**不在任一档**; `:1070` 更有既有先例 (`coordination_fetch.success` 语义翻转, 明记「carried by plugin MINOR, NOT a schema_version bump」)。A 未被采纳故不载重, 但该论据同时出现在决策单第 2 条与 §待复议 2, **会污染 owner 的复议判断**。
  *与 R1 的关系*: 这是 R1 `109b412c` 里「additive 契约声明自相冲突」那半的反向复核 —— R1 判 proposal 的 additive 声明与改字段语义不相容, 本轮 backend-architect 判该「不相容」论据本身与 schema SOT 不符。两轮不构成矛盾 (R1 论的是 A 案下的声明, 本轮论的是判它「不 additive」的依据), 但 owner 复议时应一并看。

- `e9f28dc8` [minor] testing/SC-9 / 新增 soft_error kind 命名 — **found_by: knowledge-manager (1/5)**
  本 collector 现有四个 kind 全为 `handoff_multibranch_*` (`branch_list_failed` / `branch_cap` / `ls_tree_failed` / `git_show_failed`, `handoff_multibranch.py:587,607,623,643`), 是机读契约的一部分。§What.1 的前缀守卫要新增一条 per-item 错误, 但全文未给它命名, SC-9 (:231) 也只断言「计一条 soft_error」⇒ 实现若直接复用 `handoff_multibranch_ls_tree_failed`, **SC-9 仍绿而消费方无法区分**「整支分支 ls-tree 失败」与「单行前缀异常」。建议在 §What.1 定名 (例 `handoff_multibranch_unexpected_path_prefix`), SC-9 断言 kind 字面, 并加进 §6 的 schema 同步项。

- `4835b148` [minor] documentation/新机读字段名 relpath 的命名口径 — **found_by: knowledge-manager (1/5)**
  本 schema 多词键一律下划线分词 (`legacy_count` / `owner_container` / `branches_scanned` / `updated_at` / `identity_advisories` / `latest_filename`, 连本 spec 自己新增的 `unreadable_count` 也是), `relpath` 是唯一连写例外; `grep -rn '\brelpath\b'` 在插件 1.71.1 全树零命中 (无先例可援)。字段一旦 ship 即为永久机读契约名 (schema 文档 + collector docstring + `scan.py` + writer 四处消费), 现在改成 `rel_path` 成本为零 (证据: `state-snapshot-schema.md:1080-1111`)。

- `bf0d93cb` [minor] documentation/Task 4.2 docstring 勘正清单 (committer vs author date) — **found_by: code-reviewer (1/5)**
  `_get_file_commit_date` 的 docstring `:313` 写 "ISO 8601 UTC **committer** date", 而实现用 `%aI` = author date (`:316` 自己就写了 author date, `:322` 是命令行), 模块 docstring `:40` 与 `state-snapshot-schema.md:1108` 同错。与 Task 4.2 已收入的 `:20` legacy_count 注释、`:177` trailing slash 属同一族「既有 code/doc 不一致, 顺手勘正」, 且 §Why 与 SC-4 的全部日期结论都建立在 author date 语义上, 建议一并纳入。

- `16e07a83` [minor] architecture/§5 dedupe 行「A′ 案下无此面」 — **found_by: code-reviewer (risk) (1/5)**
  A′ 保留 basename 后, 同 `(track_id, identity_key)`、同 `updated_at`、同 `branch`、同 basename 而目录不同的两行, 四级键 `(parse_ok, updated_at, filename, branch)` (`handoff_multibranch.py:428-455`) **全并列**, `max()` 回退到迭代顺序 —— 与 `_dedupe_sort_key` docstring `:438-452` 与 schema `:1126` 宣称的「a pure function of the row's own fields / invariant to build order」相悖 (那正是 round 3 finding [M1] 建立的不变量)。改前两行因串读逐字段相同, 选谁都一样; 改后 `relpath` 与真实 frontmatter 不同 ⇒ 代表行的 `status` / `phase` 可能不同 ⇒ 经共享 dedupe 传导到 collision 与看板。触发窄但不是不可达 (schema `:1125` 自述本仓真出现过同日 date-only 并列)。建议 §5 该行改成「A′ 消除字典序翻转风险, 但把 tie 的可观测性打开了」, 并在待复议 4 附问是否把 `relpath` 加进排序键。
  *与 tech-lead decision 的关系 (不构成 conflicted)*: tech-lead 在其正文 decision 判「`_dedupe_sort_key:428-455` 第 3 级仍吃 basename ⇒ tie-break 面确实不受影响」——两席量的是不同谓词 (字典序**翻转**风险 vs tie 的**可观测性**), code-reviewer 自己的措辞与 tech-lead 相容。

### Decisions (9 — 全部 minor; 按 R1 同规则**不计入**上表缺陷 severity 计数)

- `bff62d7d` [minor] testing/SC-10 基线 78 / fail-soft 六键形状核验 — **found_by: tech-lead, backend-architect (2/5)**
  **核验通过**。backend-architect 在真 git checkout 跑 SC-10 那条命令得 `Ran 78 tests in 4.695s / OK`, 单跑 `test_p1_layer_h` 得 `Ran 24 tests / OK`; tech-lead 静态 `def test_` 计数 21+27+25+5 = **78**, 与 SC-10 分模块拆分逐项相符 ⇒ R1 `60e465ad` 的 73→78 订正属实且已落地。tech-lead 另核 fail-soft 早退 dict (`handoff_multibranch.py:588-595`) 与 schema `:1136` 同为六键 ⇒ §4 与 Task 2.4 / SC-14 的前提成立 (qa-engineer / code-reviewer / knowledge-manager 各自也复跑得 78 OK, 但记在其 R1 落地复核条目内, 见 `9f82ca4a`)。

- `9f82ca4a` [minor] testing/R1 critical/major 正文落地复核 — **found_by: qa-engineer, code-reviewer, knowledge-manager (3/5)**
  **三席各自逐条复核: R1 的 2 critical + 15 major (+ knowledge-manager 另核 10 minor) 全部落进正文而非批注, 且未见「改一处引入另一处矛盾」的回填错误**。抽验交叉一致: SC-10 豁免已删并改记真仓 checkout 口径; `_check_handoff_ancestry` → `_same_branch_head_unreachable_tracks` 三处 (`scan.py:126` 定义 / `:186` 拼串 / `:255` 调用); §What.2 mv 归因重写; SC-8 拆前后半; SC-9 补 (b); 新增 SC-13/14/15 与 Task 2.4/4.2/5.1; 头部 29 文件 (5 added + 24 modified) 与 5 触点零 diff; References 已删 `#182`; SC-11 已换成定位断言。knowledge-manager 另记唯一 partial (`109b412c` 的 `snapshot_schema_version` 处置) 在 A′ 下事实上已收敛 (纯 additive ⇒ 保持 `"1.0"`)。
  *category 分歧注*: qa-engineer / code-reviewer testing、knowledge-manager documentation ⇒ 取多数 testing。
  *汇总席记*: 本条与 code-reviewer 的「Delta vs 上轮」一致 —— **本轮无任何席位重开 R1 的 33 条中任何一条**, 新缺陷全部是 v3 增量 (A′ 裁定 + §2.5 守卫 + 新增 SC) 的下游, 或 R1 五席未测到的机械事实。

- `9f7d9aff` [minor] architecture/主仓 gitlink 实况 / 基线冻结 / R1 conflicted `4c05b95a` 闭合 — **found_by: tech-lead, backend-architect (2/5)**
  **R1 的 conflicted `4c05b95a` 本轮已机械闭合**: 两席各自 `git ls-tree origin/master aria` = `301641b` = `git -C aria rev-parse origin/master`, 主仓 `ls-tree HEAD aria` 同值 ⇒ Task 5.2「从 `301641b` 前进, 严禁回退 `0545f86`」成立。tech-lead 另核头部「主仓实况」记的 `ecb6296` 已被本轨自身 commit 推进 (tech-lead 观测 `2c8eaa6`, knowledge-manager 观测 `8da3518` —— 两席观测时点不同, 均标为快照, 载重结论不变), 远端最高 tag = `v1.71.1` ⇒ §待复议 6 的 `v1.71.2` 未被占用; 两条 ahead>0 的 aria 远端分支 (`feat/69-exfil-coverage-corpus` 末次 2026-05-30 / `feature/secret-guard-per-segment-evaluation` 末次 2026-08-16) 均为陈旧分支, **非同伴容器在飞轨**, 与本 spec 触点无竞用。

- `0fdb01ab` [minor] implementation/平铺仓零行为变化前提 / 冻结语料 — **found_by: backend-architect (1/5)**
  **核验通过**: 主仓 `docs/handoff/` 无子目录、190 份顶层 `.md`; `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 996 条 track 中 `filename` 含 `/` 为 0、非 ASCII 为 0 ⇒ §7「冻结语料不需重生成」的数据前提成立 (qa-engineer 另记两份冻结语料实测存在, 见 `c547678a`)。

- `c547678a` [minor] architecture/事实底座 hermetic 复验 / 行号引用复核 — **found_by: qa-engineer (architecture), code-reviewer (implementation) (2/5)**
  **两席独立 hermetic 复跑, 五项事实底座与 §Why / SC-4 陈述全部一致**: (1) 子目录件今天产 `handoff_multibranch_git_show_failed` + 假 legacy 行且 `updated_at` 为空; (2) 非 ASCII 名被 `git ls-tree` 整条加引号, `Path(path).name` 带尾引号, 在 `.endswith(".md")` 处静默丢弃; (3) 顶层与 `archive/` 两个 `latest.md` 今天都已被排除; (4) 同名不同目录两行逐字段相同 (归档副本读到顶层内容); (5) mv 过的无 frontmatter 文件在旧 basename 路径 / 新相对路径 / `--follow` 三种写法下都返回 mv 提交日 `2026-08-15T12:00:00+00:00`, 而「从未在顶层存在」的文件错误路径返回空串、正确路径返回真日期。code-reviewer 另逐条打开 30 余个 文件:行号 引用 (`handoff_multibranch.py` / `handoff.py` / `latest_md_writer.py` / `track_board.py` 全部命中) 并报**无一处错误**。
  *category 平票注*: qa-engineer architecture / code-reviewer implementation, 1-1 平票, 按席位序取 architecture。

- `f8c1092a` [minor] implementation/F1 四处硬编码前缀枚举 — **found_by: tech-lead (1/5)**
  **F1 成立, 无第五处**: `grep -rn '"docs/handoff|docs/handoff/{' --include=*.py scripts/ lib/` 全命中集 = `handoff.py:34,254` (display 常量) · `handoff_multibranch.py:178` · `latest_md_writer.py:271` (docstring) · `scan.py:186` (唯一在 collector 之外用 `tracks[].filename` 拼 git 对象路径的消费方); `handoff_worktrees.py:83,285` 复用 `handoff.py::_scan_md_files`, 不消费 `tracks[].filename`。
  *found_by 补注*: backend-architect 正文 Decisions 第 4 条有同判条目 (`scan.py:186` 拼串逐字一致 / `:126` 定义 / `:255` 调用 / `:199-200` 空 SHA `continue` 并注释判为「a real answer」), 未列入其结构化清单, 依规则 5 未计入 found_by。

- `cf0c9dcb` [minor] documentation/Rule #6 判据表选行 — **found_by: knowledge-manager (1/5)**
  **核实通过**: 变更为纯代码 + schema 描述性文档, 无 `description` 与 SKILL.md 指令面变动 (SKILL.md 三处 `tracks_multibranch` 均不改), 与 SOT 已裁样例「纯代码 collector 层 ⇒ substitute」同形 (`standards/conventions/skill-benchmark-exemption.md:28,63-64`; `state-scanner/SKILL.md:117,149,153`)。
  *found_by 补注 + 待 owner 复议的两处张力*: backend-architect 正文 Decisions 第 5 条有同判条目 (结论侧成立), 依规则 5 未计入。但本条的成立**受两条 issue 牵制**: (a) `885edf34` 的支撑证据句为假 (四词零命中不成立, 5/5 席实测); (b) `cecc06af` 若 qa-engineer 成立 (闸门面受影响), 与 `d1f01126` 中 tech-lead 的「真修生产面须动 `handoff-mechanics.md` 处方指令面 ⇒ 照跑 AB」一并, 会改变本行的选行前提。三者应交 owner 一并裁, 汇总席不裁决。

- `17d36ecd` [minor] documentation/Rule #10 闸门权限 — **found_by: knowledge-manager (1/5)**
  **合规**。汇总席另行实读 `.aria/config.json` 复核: `audit.checkpoints` = post_brainstorm off / post_spec **convergence** / post_planning convergence / mid_implementation · post_implementation · pre_merge · post_closure off; `audit.teams.post_spec` = `[aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]` (5 席); `audit.max_rounds` = 5 —— 与 proposal 头部「审计计划」「A.1.0 未跑头脑风暴」逐项一致, 全部落 Rule #10 白名单第一类 (config 显式 off), 无 AI 自行豁免。tech-lead 在其轮次记录内作同判 (未列为 finding)。

- `3e302f4f` [minor] documentation/头部 Linked Issue 机械判据 — **found_by: knowledge-manager (1/5)**
  **三条写法全过**: 值为 inline code span `` `10CG/Aria#195` ``, 行首无空白、`>` 后恰一空格、字段名两侧各两星号、ASCII 冒号, 字段序与 SOT 模板一致; 紧邻的 `> **Issue**: [Aria#195](url)` 链接行字段名不在 E0 封闭集合内, 不干扰抽取 (`proposal.md:6-7`; `spec-drafter/SKILL.md:414-421`; `standards/openspec/templates/proposal-minimal.md:6,55-58`)。

---

## Verdict

**FAIL** — Critical 3 / Major 10 / Minor 9 (缺陷类 = issue + risk, 共 22 条; 另有 9 条 decision 不计入)。

rationale: 三条 Critical **全部落在 v3 的增量上** —— 即 2026-09-07 那次 A′ 裁定与 §2.5 写侧守卫, 也就是 R1 唯一 critical `63d1ce08` 的处置本身。没有一条 Critical 指向方案骨架: A′ 的核心 (filename 保持 basename + additive `relpath` + 四个 git 路径消费方改读 `relpath`) 经多席实读与 issue/triage 原案一致, 五席无一要求推翻。

- **`6f8fa9f7` (实现面, 4/5 席)**: Task 2.5 把判据钉死为 `relpath != filename` 且禁用替代写法, 却没定义 `relpath` 缺失时的语义 —— 缺键取 `None` 判据恒真。这不是推理: backend-architect 用既有夹具形状跑打了守卫的 `write_latest_md`, 指针行退化成「(pointer 不可用)」, 一条**当前为绿**的既有断言 (`test_p1_layer_h.py:270`) 转红; 而 SC-10 点名的四个模块恰好不含这个唯一覆盖 `write_latest_md` 的模块, SC-15 又因端到端产出恒带 `relpath` 覆盖不到缺失分支。knowledge-manager 另指出真实的生产触发路径: `session-closer/SKILL.md:90` 允许读既有快照, 升级前的快照全无 `relpath` ⇒ 平铺仓每条真指针被吞、退回 mtime, **正好重开 H5「pointer 是语义权威」那条既有修复**。「按 spec 字面实现就会坏」是本轮最硬的一条。
- **`d1f01126` (可达性, 4/5 席)**: 守卫加在 `write_latest_md` 上, 而该函数全插件树**零生产调用点** —— 且这是 `phase-1-collectors.md:95` 白纸黑字的既有设计决定 (deliberately D.3-scoped, 不引入 production call-site), 生产 D.3 的 pointer 由 AI 按 `handoff-mechanics.md:114-124` 的处方决策表手改, 本仓 `docs/handoff/latest.md:103-107` 甚至自记「机械 writer 当前不可用」。于是 Impact.Risk 的缓解承诺「使这类指针压根不写出」在生产上为假, 而 owner 正被要求为一个**目前无人在付**的代价签字 (待复议 2)。四席都不主张撤掉守卫, 但都要求把可达性写明 —— 它决定 owner 看到的代价估算对不对, tech-lead 另指它还决定 Rule #6 的判定该不该改判。
- **`88a49037` (判据面, 3/5 席)**: SC-15 是这次裁定的唯一端到端验收, 而按字面取最小夹具时 (e) 恒绿 (其反事实被 `handoff.py:438-451` 的早返回证伪, qa-engineer hermetic 实测 soft errors=[]), (f) 恒红且结构上不可满足 (守卫管不到两个 collector 的 `exists` 自相矛盾 —— 本文自己已把它推给 Task 5.3 另开 issue)。**新增的机制, 其验收既抓不住机制缺失, 又要求实现做到方案明说不做的事**; (f) 恒红正是「改断言就范」的诱因。

10 条 Major 分四类, **全部可在 Phase A 内改 spec 消解, 不需推翻 A′ 骨架**:

1. **判据可证伪性 (5 条)**: SC-2/SC-12 的新键豁免清单没跟上 A′ (`relpath` 未豁免 ⇒ 恒红, `d02ec3f0`); 二者的基线仍随 origin 分支集变动 (Phase B 自己推分支即加约 190 行 ⇒ 假红, `db0db697`); SC-13 的反事实被 dedupe 对 legacy 行的透传契约证伪, 连带 §What.2 第三条是事实错误 (`3cb2cf2b`); SC-1/5/14/15 的裸 `errors[]` 在两个同名面之间摇摆, 一边恒绿一边不可满足 (`fc925710`); SC-12 子目录半条既含恒绿断言又含「失败就记录」的非判据式失败模式 (`112b4299`)。
2. **裁定后的下游漂移 (1 条)**: Task 4.1 无条件要求「订正」一条 A′ 下仍为真的 schema 论据 (照做即写入错误勘正), SC-7 / Task 3.2 钉一个 A′ 下不可能产出的取值 (`e3ca1e1a`)。
3. **影响面枚举 (1 条, conflicted)**: §5 消费方表漏掉 `exists` / `len(tracks)` 的处方性消费方 (两条推荐规则 + D.3 指针决策表 + fetch_gate); 且两席在「闸门面是否受影响」上结论相反 —— 一侧只量了删掉的假 legacy 行, 另一侧还量了新增的真 track 使 `collision.kind` 从 `none` 翻到 `cross_owner` (`cecc06af`)。
4. **同步面与证据面 (3 条)**: Rule #6 的「四词零命中」被 **5/5 席**各自 grep 推翻 (`885edf34`); §6 漏 Rule #9 的 standards SOT, 而 §2.5 引入的第三态使该 SOT 的无条件两态表述失真 (`94935605`); Task 5.1 只列 16 个版本点中的 7 个, 且「三条 check 兜底」断言经实读不成立 —— 10 处零机械兜底 (`d58dfb65`)。

按 report-storage.md §Verdict 计算, ≥1 Critical ⇒ **FAIL**。post_spec 的阻塞行为是 `blocking: false`, 故本 FAIL **不硬阻断**流程; 但按 Rule #10, 该判定不得由 AI 自行降格 —— conflicted 项 `cecc06af` 与其牵连的 `885edf34` / `cf0c9dcb` (Rule #6 照跑 vs 豁免) 需 owner 或 Round 3 拍板后再进 Phase B。

正面记录 (不因 FAIL 抹掉): **R1 的 33 条本轮无一被重开** —— 三席 (`9f82ca4a`) 逐条复核 R1 的 2 critical + 15 major (+ 10 minor) 全部落进正文而非批注, 且未见回填错误; R1 的两处 conflicted 均已机械闭合 (`4c05b95a` 由 `9f7d9aff` 的 `ls-tree origin/master aria` = `301641b` 定案; `24165c1c` 的 SC-10 豁免已删且 78 tests 在真仓 checkout 四席各自跑绿, 见 `bff62d7d`)。事实底座五项 hermetic 结论两席独立复跑全部一致 (`c547678a`), code-reviewer 逐条打开 30 余个 文件:行号 引用报无一处错误, F1 四处前缀无第五处 (`f8c1092a`), 平铺仓与冻结语料零子目录零非 ASCII (`0fdb01ab`), Rule #10 与头部机械判据合规 (`17d36ecd` / `3e302f4f`)。code-reviewer 的判词概括了本轮形态: 缺陷「集中在同一处 rework 的下游」, 是 memory `feedback_multiround_audit_catches_fix_introduced_regression` 说的**加固动作自身重开同类缺口**, 不在调研质量。

计算依据:
- Critical: 3 (3 issue + 0 risk)
- Major: 10 (9 issue + 1 risk)
- Minor: 9 (8 issue + 1 risk)
- Decisions (不计入): 9 (全部 minor)

---

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 — Conclusions 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6), Vote 票型 REVISE 5 / PASS 0, verdict FAIL, `converged: false`
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md` (汇总席本轮实读全文并逐条抽取四元组)

### Round 2

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`; frontmatter 15 字段齐全 5/5, 0 份需补齐
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (五席各自独立报同一结论; code-reviewer 与 knowledge-manager 另列扫描面 —— `openspec/changes/` 8 个在制 spec 中引用 `Aria#195` 的仅本 spec, 全仓 grep `10CG/Aria#195` 无第二份 proposal, 触及 `handoff_multibranch` / `latest_md_writer` 的 proposal 亦仅本 spec; tech-lead 另扫 aria 远端两条 ahead>0 分支均为陈旧分支, 非同伴在飞轨)
- Conclusions: **31** (去重前 55) —— Critical 3 / Major 10 / Minor 9 / Decisions 9
- Delta vs 上轮: **集合完全不同 —— 交集 0 条** (汇总席用 python3 对 R1 33 条与本轮 31 条的四元组做集合比较, `set(R1) == set(R2)` 为 `False`, `len(R1 & R2)` = 0)。按语义 (忽略 scope 写法差异) 复核, 仅 3 条 decision 可对位 (`17d36ecd` ≈ R1 `270a0181` Rule #10 闸门权限 · `3e302f4f` ≈ R1 `6709ffb4` 头部 Linked Issue · `f8c1092a` ≈ R1 `b14f94c8` F1 复核), 其余 28 条全新; R1 的 27 条缺陷类**无一条在本轮被重开**。本轮新缺陷的来源分布: 13 条 Critical/Major 中 8 条是 v3 增量 (A′ 裁定 + §2.5 守卫 + 新增 SC-13/14/15) 的下游, 5 条是 R1 五席未测到的机械事实 (ab-suite 四词 / writer 可达性 / standards SOT / Task 5.1 版本点 / errors[] 二义)。⇒ `conclusions_stable = false`
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: FAIL 3 (tech-lead / backend-architect / qa-engineer) + PASS_WITH_WARNINGS 2 (code-reviewer / knowledge-manager); 后两席各自 Critical=0, 仍按 audit-points 横切「数据可用性」条款载重投 REVISE
  - 两席判 Critical=0 与三席判 Critical≥1 的差异**不是矛盾意见**: code-reviewer / knowledge-manager 对 `6f8fa9f7`(守卫判据) 与 `d1f01126`(可达性) 都提了同一条 finding, 只是记 major; severity 依规则 1 取最高, 已在各条目内注明原始标注
- `converged`: **false** — `conclusions_stable`(false) AND `unanimous_pass`(false) 双条件均不成立 (最终由编排脚本裁决)
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 2 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 55 / 31 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 3 / 10 / 9 |
| 其中 issue / risk | 20 / 2 |
| Decisions (不计入缺陷计数) | 9 (全部 minor) |
| Conflicted 对 | 1 (`cecc06af` 闸门面是否受影响 —— 可机械闭合) |
| 5/5 全席独立命中的 finding | 1 (`885edf34`) |
| 4/5 席命中的 finding | 2 (`6f8fa9f7` · `d1f01126`) |
| finding id 碰撞 | 0 (31 条全部唯一, python3 实算) |
| unanimous_pass | false |
| conclusions_stable vs R1 | false (交集 0 / 33 · 0 / 31) |
| converged | false (R2: `conclusions_stable=false` 且 `unanimous_pass=false`) |
| 收敛轮次 | N/A (max_rounds = 5, 实读 `.aria/config.json`) |
| R1 缺陷被重开数 | 0 / 27 |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的条目按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `6f8fa9f7` | critical | backend-architect, tech-lead, code-reviewer, knowledge-manager (4/5) | §2.5 与 Task 2.5 明写「`relpath` 缺失 ⇒ 按 `relpath = filename` 处理 (老快照即平铺世界), 照写真指针」; SC-15 补第三条断言 (无 `relpath` 键的 track ⇒ 仍写真指针) 覆盖该分支; SC-10 点名集并入 `tests/test_p1_layer_h.py`; Task 2.5 补 `_render_pointer_unavailable(track_id, now)` 的签名变更 |
| 2 | `d1f01126` | critical | tech-lead, backend-architect, code-reviewer, qa-engineer (4/5) | **待 owner 复议**: 在 §2.5 / §5 / Impact.Risk / 待复议 2 四处写明可达性 —— `write_latest_md` 当前零生产调用点 (`phase-1-collectors.md:95` 的既有设计决定), 生产 D.3 指针由 AI 按 `handoff-mechanics.md:114-124` 手改; 据此重述「子目录采用方本轮拿降级 pointer」的代价 (目前无人在付), 并请 owner 一并裁 tech-lead 的推论「若要真修生产面须动处方指令面 ⇒ Rule #6 照跑 AB」是否成立 (与 #4 / `cf0c9dcb` 同批) |
| 3 | `88a49037` | critical | qa-engineer, tech-lead, code-reviewer (3/5) | SC-15 的子目录夹具明确成 §5 sub-case (a)「子目录 active + 顶层另有一份非-active `.md`」使 `canonical_files` 非空, 让 (e) 恢复鉴别力; (f) 改写成可满足且可执行的谓词 (例「两 collector 的 exists 矛盾时必须有 soft_error 信号」) 或随 Task 5.3 的另开 issue 移出本 SC; 同步修正 rule6_note 的 baseline-failing 实体计数 |
| 4 | `885edf34` | major | 5/5 全席 | 头部 Rule #6 行 (:12) 与 rule6_note (:244) 两处按实测改写 —— `tracks_multibranch` 在 `ab-suite/state-scanner.json:214` 命中 1 次 (文件今 17551 B, 由 `5697477` 2026-09-05 引入), 另三词为 0; 证据句改成「唯一命中落在闸门面 `SKILL.md:149/153`, 而本 spec 三处均不改」; 并按 #7 的裁决结果重判「照跑 vs 豁免」(Rule #6「拿不准 → 照跑」) |
| 5 | `d02ec3f0` | major | backend-architect, code-reviewer | SC-2 / SC-12 / Impact.Risk 第 6 条的「零差异 / 逐字段相等 / 逐字节相同」把 `relpath` 一并纳入豁免清单 (或明写走 `freeze_corpus.py:29` 的八字段投影); 另补一条 SC 钉住决策单 §落地约束 1 的不变量「平铺仓 `relpath == filename` 恒成立」 |
| 6 | `db0db697` | major | backend-architect | SC-2 / SC-12 的基线改成固定分支集 (离线模式 / 只比 before 分支集内的行 / hermetic 临时仓); 「同工作区双跑」不治时变的根 —— Phase B 推 feature 分支即新增约 190 行 |
| 7 | `cecc06af` | major | backend-architect, qa-engineer (**conflicted**) | 先用一次 hermetic 实跑定案闸门面 (含「顶层 + `archive/` 同 track_id 异 owner_container」的临时仓, 比对改前/改后 `collision.kind`); 据结果重写 §5 该行与 rule6_note; 无论结论如何, §5 枚举表补入 `exists` / `len(tracks)` 的处方性消费方: `advanced-rules.md:443-444,511-512,544` · `RECOMMENDATION_RULES.md:28,31` · `handoff-mechanics.md:116-121` · `fetch_gate.py:175-188` |
| 8 | `e3ca1e1a` | major | tech-lead, code-reviewer, qa-engineer | Task 4.1 删除或条件化「`:1125` tie-break 论据订正」—— A′ 下该句仍为真, 照做即写入错误勘正; SC-7 与 Task 3.2 显式标注「假想输入的特性化测试」或随 A 案删除 (A′ 下 collector 不会产出 `filename="archive/…"`) |
| 9 | `3cb2cf2b` | major | qa-engineer | 改写 §What.2 第三条 (proposal.md:113) —— legacy 行在 `handoff_multibranch.py:521-524` 被 `continue`、从不进入 dedupe 分组, 「被当成同一 track 折叠」不成立; SC-13 的反事实改成只依赖「两条不同 `track_id`」那半, 并同步修正 rule6_note 对它的实体计数依据 |
| 10 | `fc925710` | major | qa-engineer | SC-1 / SC-5 / SC-14 / SC-15 逐条把裸 `errors[]` 消歧成 `tracks_multibranch.errors[]` (消息串) 或 `CollectorResult.errors` / 顶层 `errors[]` (带 kind); 现写法使 SC-5 不可满足、SC-1 在 `301641b` 上恒绿 (违反 Task 1.2「对 301641b 全红」) |
| 11 | `112b4299` | major | qa-engineer | SC-12 拆开: 顶层布局断言 exit 0; 子目录布局只断言「不出现 `handoff_multibranch_git_show_failed`」, pointer 相关断言全部让给 SC-15; 删掉「若实跑非 0 就逐条抄下 kind 并在 handoff 说明」这一非判据式失败模式 |
| 12 | `94935605` | major | knowledge-manager | §6 与 Tasks 补入 `standards/conventions/session-handoff.md:171-173` —— §2.5 的守卫给 latest.md 派生行为加了第三态, 使该 SOT 的无条件两态表述失真; 若本轮不改 standards, 须在 spec 内显式写成 deferred 并说明理由 (会带出 standards 版本与 gitlink 同步面) |
| 13 | `d58dfb65` | major | knowledge-manager | Task 5.1 补齐 16 个版本点中漏掉的 9 处 (`VERSION:24` · `CLAUDE.md:139,141` · 三份 i18n README 的 `:10` badge 与 `:244` 正文行); 删除或改写「漏改必在归档闸转红」—— 实读四条 check 后含 `README.md:242` 在内的 10 处零机械兜底 |

Minor (9 条) 不逐条列入本表, 建议随上述 rework 一并顺手订正: `28f9d80c` (SC-1 / SC-8 就地单值化到 A′) · `e03d8a32` (schema `:1136` 顺带补 `identity_advisories` + `## Change history` 加行) · `7cba5aa4` (SC-10 点名集并入 `test_p1_layer_h`, 与 #1 同处) · `90a5604b` (Impact 首行同步待复议 2 的裁定结果) · `b5d25ad4` (§7 与决策单第 2 条的「不属 additive」论据按 `state-snapshot-schema.md:46-48,1070` 改写) · `e9f28dc8` (给 per-item 前缀守卫的 soft_error 定名并让 SC-9 断言 kind 字面) · `4835b148` (`relpath` → `rel_path`, 与 schema 下划线口径一致) · `bf0d93cb` (Task 4.2 纳入 `_get_file_commit_date` 的 committer/author date 勘正) · `16e07a83` (§5 dedupe 行改「A′ 消除字典序翻转风险, 但把 tie 的可观测性打开了」, 待复议 4 附问是否把 `relpath` 加进排序键)。
