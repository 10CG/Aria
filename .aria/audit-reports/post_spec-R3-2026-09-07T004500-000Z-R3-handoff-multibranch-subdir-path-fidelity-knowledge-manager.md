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
timestamp: 2026-09-07T04:10:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [knowledge-manager]
---

# post_spec R3 单席报告 — knowledge-manager (handoff-multibranch-subdir-path-fidelity)

本席为 R3 新席位, 不继承 R1/R2 结论。全部事实均对真文件实读/实跑核验 (proposal 自述一律不采信); 本轮只审不改, 审后 `git status --porcelain` 主仓与 aria 子模块均为空。

## 审计结论

### Decisions

- [minor] documentation/R2 三条 critical + 十条 major 的正文落地: 逐条核对**全部落进正文而非批注** —— `6f8fa9f7` → §2.5 缺键行 + 警示块 + Task 2.5(b) + SC-15 布局 3 + SC-10 补 `test_p1_layer_h`; `d1f01126` → §2.5 可达性块 + Impact.Risk 限定 + 待复议 2 代价重述; `88a49037` → SC-15 细则布局 2 (顶层留非-active 件) 且 (f) 已移除; `885edf34` → 头部改判 + rule6_note 反证 1; `d02ec3f0` / `db0db697` → SC-2 走 `freeze_corpus.py:29` 八字段投影 + hermetic 固定分支集 + SC-16; `cecc06af` → §5 collision 行改写 + 三条处方性消费方入表; `e3ca1e1a` → Task 4.1 删除 `:1125` 订正项 + SC-7 标注特性化测试; `3cb2cf2b` → §What.2 第三条订正 + SC-13 删「不折叠」; `fc925710` → SC-1/5/14/15 两个 error 面消歧; `112b4299` → SC-12 拆 12a/12b; `94935605` → §6.6 + Task 4.4; `d58dfb65` → Task 5.1 十六行表 + 删除错误兜底句。9 条 minor 亦全数落地。两条落地不完整 (94935605 覆盖面 / 4835b148 只 neutralize 一半) 已单列为下方 Issues (证据: proposal.md:15-16,124-145,174-193,216-259)
- [minor] testing/载重事实独立机械复核: 五模块在真 checkout `/home/dev/Aria/aria` (HEAD 实测 `301641b1c893477f387a1f85d1e90d105ebf0db9`) 实跑得 `Ran 102 tests ... OK`, 与 SC-10 一致; `aria-plugin-benchmarks/ab-suite/state-scanner.json` 实测 17551 B、`tracks_multibranch` 命中 1 处 (`:214`, 该 prompt 的 (C) 把 `collision.kind` 值写死在题面 ⇒ 结构上测不到 collector 输出变化)、`handoff_multibranch` / `basename` / `legacy` 三词均 0; Task 5.1 十六个版本点抽验 9 处 (CLAUDE.md:139,141 · README.md:8,242 · README.zh.md:3,10,244 · VERSION:24 · system-architecture.md:189 · version-scheme.md:23) 行号与取值全对; `.aria/probes/main-project-version-consistency.py:39-49` 的 POINTS 确实全是主项目版本行, 「10 处零机械兜底」成立 (证据: 上列各文件行号)
- [minor] documentation/头部机械判据与规则合规: `proposal.md:6` 逐字节核为 `> **Linked Issue**: ` + inline code span `10CG/Aria#195`, 行首无空白、`>` 后恰一空格、两侧各两星号、ASCII 冒号 ⇒ spec-drafter 写法三条全过 (`spec-drafter/SKILL.md:414-421`); Rule #6 落 SOT 判据表第四行「拿不准 ⇒ 照跑」并按 §4 留 `rule6_note` 引用本规范, 与 `standards/conventions/skill-benchmark-exemption.md:24-28,60-64` 一致, 无 AI 自创豁免理由; 审计计划与 `.aria/config.json` 的显式 off 对齐, 落 Rule #10 白名单第一类
- [minor] architecture/事实底座抽验: 本席另行实读复核 30 余处新引用无误 —— `latest_md_writer.py:89-95,143,151,164,259` · `collision.py:480-486` collidable 过滤 · `handoff_multibranch.py:14-22,42,177-178,313-322,521-524,586-596,593,748,753` · `handoff.py:263-266,282-288,397-404,438-451` · `test_p1_layer_h.py:230-240,270` · `session-closer/SKILL.md:90` · `phase-1-collectors.md:95,104` · `handoff-mechanics.md:4,116-121` · `advanced-rules.md:443-444,511-512,544` · `RECOMMENDATION_RULES.md:28,31` · `state-snapshot-schema.md:46-48,1070,1108,1110,1125,1128,1136,1156-1168` · `docs/handoff/latest.md:104-107`。另实测 `_LATEST_POINTER_RE` (`handoff.py:263-266`) 对降级横幅不匹配 ⇒ SC-15 布局 2 的 (e) 在「顶层留一份非-active 件」夹具下确有鉴别力, R2 `88a49037` 的处置机制上成立

### Issues

- [major] documentation/§6.3 + Task 4.2 + SC-11(d) — `json-diff-normalizer.md:241`: 本文把该行称作「显式枚举的键集」并令其补 `unreadable_count`。实读该行落在 `### tests/fixtures/reference-snapshot-aria.json` 一节 (`:196`) 里 **2026-07-18 resample 的历史记述** (`:204` 起, `:235-241` 是「两处有意偏离」的第 2 条, 过去时描述当时把 tracks 截到前 5 条「以便 `branches_scanned / legacy_count / collision / errors / exists` 仍可见」)。该文档全篇无 `tracks_multibranch` 的规范性键集 (Rule 1-10 均不涉及)。照令实施 = 往一段有日期的历史记录里写入该 fixture 不可能含有的字段 (即 R2 `e3ca1e1a` 判 major 的同一类「照做即写入一条错误勘正」), 而 SC-11(d) 只 `grep -q` ⇒ 假绿。该文档对 schema 变更的既有口径是 **resample fixture + 记一条带日期的 resample 注** (`:204-215` 先例), 本 spec 既未做也未声明 defer (证据: json-diff-normalizer.md:196,204,235-241; proposal.md:178,254)
- [major] documentation/§6 文档同步 (Rule #3) 覆盖面 — 「单 active track ⇒ 写真指针」共 5 处未覆盖: R2 `94935605` 只修到 standards 的一处。机械枚举同义断言面: (1) `standards/conventions/session-handoff.md:171-173` (Task 4.4 已覆盖); (2) 同文件 `:97`「写入后**自动**更新 latest.md pointer(单 track 场景)或 deprecation banner(多 track 场景)」—— 未覆盖; (3) `state-scanner/references/layer-l-integration.md:103`「单 track: 更新 latest.md pointer」—— 未覆盖; (4) `latest_md_writer.py:288-291` docstring 的 Scenarios 表「active count == 1 → "pointer" action」—— 未覆盖; (5) `latest_md_writer.py:140,159` 是**写进 latest.md 正文**的那句「自 v1.22.x 起, 本 pointer 仅在单 active track 场景下写真实指针」—— 未覆盖, 落地后子目录采用方的 latest.md 会同时印着这句和「(pointer 不可用)」。另 `phase-d-closer/references/handoff-mechanics.md:116` 的 Single-track 行本文已登记并交 owner, 属已披露 (证据: 上列各行; proposal.md:180-184,255)
- [major] architecture/§2.5 + Task 2.5(d) — 守卫的机读面仍是静默降级: `write_latest_md` 在 `n_active == 1` 时**无条件**置 `action = "pointer"` (`latest_md_writer.py:301-303`), 而返回契约只有三值 (`:277-281` docstring + `references/phase-1-collectors.md:102` 逐字 `{action: "pointer"|"banner"|"skipped", ...}`)。§2.5 / Task 2.5 定义了第四种结局却没给它 `action` 取值, 也没把这两处契约面列入 §6 ⇒ 未来接线的调用方读到 `action == "pointer"` 是**假阳性**; 消费侧同样无信号: 降级横幅不匹配 `_LATEST_POINTER_RE` (`handoff.py:263-266`, 实测不命中) ⇒ `latest_source` 退回 `"mtime"` 且**零 soft_error** (SC-15 的 (e) 正是断言这份静默)。本 spec 的立论 (§Why F2「静默漏扫无任何信号」、§5「两个 collector 互相矛盾而无任何信号」) 与此自相矛盾: 「必须写明原因, 不得静默退化」目前只在人读面成立 (证据: latest_md_writer.py:277-281,288-291,301-303; phase-1-collectors.md:102; proposal.md:129-133,225)
- [major] documentation/§6.5 + SC-11(e) — CHANGELOG 条目口径与同 collector 上一周期不一致: 本文只要求「Fixed 三条 + Changed 两条」, SC-11(e) 也只查这五条。但本 spec 新增 `rel_path` 与 `unreadable_count` 两个**永久机读契约字段**, 且触碰 schema / json-diff-normalizer / collector docstring / (Task 4.4 落地时) standards 四类文档面。同一 collector 家族的上一周期 v1.70.0 的成文口径是: 新增的恒存在机读字段列 `### Added` (`aria/CHANGELOG.md:93-97`, 例 `tracks_multibranch.collision.identity_advisories[]`), 全部触碰文档 (含 standards session-handoff.md, 标 Amended) 列 `### Changed` (`:99-100`)。照本文写法, 版本 SOT 里将查不到这两个新字段 (证据: aria/CHANGELOG.md:93-100; proposal.md:186,253)
- [major] documentation/决策单 §落地约束 与正文的矛盾只 neutralize 了一半: 头部 (`proposal.md:16`) 就 `relpath → rel_path` 声明「决策单原文写 relpath, 以本文为准」, 但同一节 (`.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` §落地约束, 标题写明「Phase B 必须遵守」) 另有两条载重错项未 neutralize: (a) 第 2 条逐字要求「写侧守卫的判据用 `relpath != filename`」—— 正是正文 §2.5 明禁的缺键恒降级写法 (R2 critical `6f8fa9f7`); (b) 第 4 条要求 SC-15 断言「子目录 track 走守卫分支且**不产生** `handoff_pointer_target_missing`」—— 在归档-only 夹具下恒绿 (R2 critical `88a49037`)。该决策单在正文中被当作规范来源引用 (SC-16 写「决策单 §落地约束第 1 条要求」, 待复议 2 请 owner 追认的对象也是它) ⇒ 属 memory `feedback_spec_inherits_upstream_dec_errors` 的形态, 且勘正只做一半比不做更危险 (证据: 决策单 §落地约束 4 条; proposal.md:16,83,278,315)
- [major] architecture/头部 Level 字段与 v4 实际变更面不符: R2 rework 新增的 Task 4.4 把变更面扩到 `standards/` 子模块 (本文自述「是**第二条**同类链路」, 需独立 commit + 本地 merge + 双推 ls-remote + 主仓 gitlink bump), 加上 aria 子模块与主仓的 16 个版本点, 已构成跨两子模块 + 主仓。owner 在 10 天前对同 collector 家族的相邻 spec 用的正是这条判据: 「**owner 2026-09-05 裁定升 Level 3** (判据: cross-module 成立, aria + standards 两子模块)」, Level 3 交付 = proposal + tasks.md + detailed-tasks.yaml + post_planning 收敛审计。本 spec 头部仍写 Level 2, 目录内无 tasks.md, proposal.md 已达 97729 B, 且 §待 owner 复议六条里没有 Level 这一条 (证据: openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/proposal.md:3 与其目录三文件; spec-drafter/LEVEL_GUIDE.md:155-163 跨模块自动提升; proposal.md:3,216; 目录 ls 仅 proposal.md)
- [minor] implementation/Tasks 段序号顺序: 列出顺序为 1.1 → 1.2 → 2.0 → **2.5** → 2.1 → 2.2 → 2.3 → 2.4 → … → 5.1 → **5.5** → 5.2 → 5.3 → 5.4。2.5 (消费 `rel_path` 的写侧守卫) 排在产出该字段的 2.1/2.2 之前, 按列出顺序推进则守卫与 SC-15 都无字段可读; 5.5 (AB) 排在 5.2 (合并双推) 之前亦与 Phase 顺序相反 (证据: proposal.md:224-226,244-248)
- [minor] documentation/§5 的动作项无承接 + 规则 1.53 未登记: §5 对 `advanced-rules.md:443-444,511-512,544` 与 `RECOMMENDATION_RULES.md:28,31` 写「须一并复核措辞」, 但 §6 与 Tasks 全无对应条目 ⇒ 该动作无人执行也无从验收。另 `RECOMMENDATION_RULES.md:30` 的规则 1.53 (`multi_terminal_handoff_dual`, 条件含「leader pointer 仍在 latest.md」) 同样被守卫影响 (守卫命中时 latest.md 不再含真指针), §5 只登记了 `:28` 与 `:31` (证据: RECOMMENDATION_RULES.md:28-31; proposal.md:167-171)
- [minor] documentation/pointer 排除口径的「未成文」表述不准: §What.1 与 §6.1 称该口径「今天未成文」, 实读 `state-snapshot-schema.md:1114` 已成文 —— 「the navigation pointer (`docs/handoff/latest.md`) is excluded from `_list_handoff_files` … it never appears as a `TrackEntry`」, 只是它写的是**顶层**路径, 与实际的任意深度行为不符。因此 Task 4.1 的动作性质是**勘正一处会误导的既有句**, 不是纯新增; 按现措辞实施可能新增一句而把原句留在原地 (证据: state-snapshot-schema.md:1114; proposal.md:106,176)

### Risks

- 本轮无独立的 risk 类结论。上列 major 3 (机读面静默降级) 与 major 6 (Level 判据) 若由 owner 判为可接受, 应在 §待 owner 复议里成文为已裁事项, 而不是留在正文的推荐默认里 —— Rule #10 禁止以「变更小 / 代价目前无人在付」作为自行降级的理由。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **6** / Minor **3** (另 4 条 decision 为核实通过项, 不计入)。

rationale: A′ 骨架 (filename 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git-show 失败不再伪造 legacy + 写侧守卫) 本席无异议; R2 的 3 critical + 10 major 逐条落进正文且未见回填错误, 三项载重机械事实 (102 tests / ab-suite 命中形态 / 16 个版本点) 本席独立复跑一致, 因此本轮**无 critical**。6 条 major 全部落在知识与文档一致性这一面, 且全部可在 Phase A 内改 spec 消解, 不需推翻方案:

1. **写入错误内容的必做项 1 条** (`json-diff-normalizer.md:241` 是历史 fixture 记述而非键集契约) —— 与 R2 `e3ca1e1a` 同型, 是本轮唯一「照 spec 做就会把文档改错」的条目。
2. **Rule #3 同步面枚举不全 2 条** —— 「单 active track ⇒ 真指针」在 5 处未覆盖 (含写进 latest.md 正文的那句); CHANGELOG 缺 Added / Changed 两类条目, 与同 collector 上一周期成文口径不符。
3. **契约面缺口 1 条** —— 守卫新增第四种结局但 `action` 契约不变、消费侧零信号, 使「不得静默退化」只在人读面成立。
4. **上游文档只 neutralize 一半 1 条** —— 决策单 §落地约束仍逐字要求正文明禁的守卫写法与已被证伪的 SC-15 断言。
5. **Level 判据 1 条** —— Task 4.4 引入第二子模块后与 owner 10 天前的升级判据同形, 而头部仍 Level 2、无 tasks.md、待复议清单未列。

3 条 minor (任务序号顺序 / §5 动作项无承接 / 「未成文」表述不准) 为措辞与编排层面, 顺手改即可。

按 `verdict-format.md` 判定规则: 0 Critical + ≥1 Major ⇒ **PASS_WITH_WARNINGS**; 本席票型 **REVISE**。post_spec `blocking: false`, 不硬阻断流程, 但 major 6 (Level) 与 major 5 (决策单) 都需要 owner 或 R4 拍板后再进 Phase B。

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 — Conclusions 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6), Vote REVISE 5 / PASS 0, verdict FAIL
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 2 (承前)

- Agents: 5/5 — Conclusions 31 去重后 (Critical 3 / Major 10 / Minor 9 + Decisions 9), Vote REVISE 5 / PASS 0, verdict FAIL; conflicted 项 `cecc06af` 已由 rework 的 hermetic 实跑闭合 (`collision.kind` none → cross_owner), 连带把 Rule #6 由 substitute 改判照跑
- 来源: `.aria/audit-reports/post_spec-R2-2026-09-07T004500-000Z-R2-handoff-multibranch-subdir-path-fidelity-aggregated.md` + 同前缀 5 份单席报告 + scratchpad rework 记录

### Round 3

- Agents: knowledge-manager (本席, 五席之一; 本报告只覆盖本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (扫描面: `openspec/changes/` 8 个在制 spec 中引用 `Aria#195` 的仅本 spec; 全 `openspec/changes/` grep `handoff_multibranch` / `latest_md_writer` 亦仅本 spec)
- Conclusions 数: 13 (Issues 9 = Major 6 + Minor 3; Risks 0; Decisions 4)
- Vote: **REVISE**
