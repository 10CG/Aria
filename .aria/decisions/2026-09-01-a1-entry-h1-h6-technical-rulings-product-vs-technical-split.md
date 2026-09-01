# 决策: a1-entry 三份 Spec 的 H1–H6 待裁项 — 按「产品级 owner / 技术级 AI」分工逐条裁定

- **日期**: 2026-09-01 | **裁定人**: AI (技术级, 按 owner 2026-09-01 分工授权) | **执行容器**: simonfish/023236f2
- **对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/` (母) · `linked-issue-field-availability/` (字段) · `sibling-spec-probe/` (探针)
- **输入**: handoff `docs/handoff/2026-08-31-a1-entry-a2-a3-landed-post-planning-r4-converged.md` §2 H1–H6 + 三份 Spec 各自「待 owner」段原文 (逐条实读, 非摘要)
- **关联**: Aria#174 (立项 issue) · 决策单 `2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md` (前一批 owner 裁定)

## 分工原则 (owner 2026-09-01 原话逐字)

> 「执行1，但是我不认为应该我来进行决策。我应该只决策产品级别，技术实现级别应该你直接决定，你的决定判断标准，应该由产品决策进行倒推，确认可以准确判断对错的标准。」

**操作化** (本文件与后续同类事项的判据):

1. **产品级** = 「要不要这个能力 / 要解决谁的什么问题 / 接受什么代价换什么」—— 只有 owner 能定, 且通常已经定过 (issue 立项 / Spec 批准 / 既有裁定)。
2. **技术级** = 给定产品决策后「怎么做才算对」—— 当且仅当能写出一条**可证伪的判据** (SOT 条文字面 / 机械检查 / 夹具红绿) 时由 AI 直接裁, 并把判据与回退方式写进决策单。
3. 写不出可证伪判据、只剩「偏好 / 节奏 / 优先级」的, 才是真正要上呈 owner 的; 上呈时选项集不得收窄 (memory `narrow-owner-options`)。
4. 本分工**不改变** Rule #10: 已启用闸门仍不得由 AI 豁免。技术级裁定只回答「怎么做」, 不跳过任何 enabled 检查点。

## 逐条裁定

| # | 事项 | 级别 | 裁定 | 判据 (倒推链) | 可证伪核验 | 落点 |
|---|------|------|------|---------------|-----------|------|
| **H1a** | 版本档 MINOR vs PATCH (三份各自) | 技术 | **三份均 MINOR** | SOT `standards/conventions/version-management.md §2.2` 触发条件第 4 条「功能增强 (向下兼容)」**字面覆盖**三份 (字段: 新 lib + 新探针脚本 + 新 check + 模板新义务; 探针: 每轮新探针 + 新 AB 套件 + 新脚本; 母: 新 CLI 模式 + 2 flag + 2 lib API + allowed-tools 扩权); §2.3 Patch 四条 (文档错误/链接/小改进/Bug) 无一覆盖。三份 Spec 自陈「两条 CLAUDE.md 判据都不字面覆盖」是因为只引了 CLAUDE.md 的缩写句, 没引 SOT §2.2。先例: v1.67.0 (lib/collision.py 一个新导出函数) / v1.65.0 (新 scripts/path_coverage.py) 均 MINOR; 纯修复批 (v1.66.x / v1.67.1 / v1.67.2) 才 PATCH | 发版时 `aria/CHANGELOG.md` 新条目首节为 `### Added` 且 plugin.json 次版本号 +1、修订号归 0 | 三份 yaml 发布任务 notes / tasks.md 待裁项 / 字段 proposal §Impact 版本行 |
| **H1b** | 三份串行 ship 各占一号 vs 合并一版 | 技术 | **各占一号** (字段 → 探针 → 母, 每次 ship 一号; 号落地时按当时 plugin.json 计算, `<vNEXT>` 占位约定不变) | (1) CLAUDE.md「版本 SOT = plugin.json, 派生文件必须一致」+ state-check `plugin-cache-currency` 的语义 (installed vs SOT) 要求**一个版本号只标识一套行为**; owner 裁定 O-4 (i) 使字段必须先合入 aria master 才能开探针 B.1, 且三份各自改运行时指令面 (spec-drafter / audit-engine / phase-a-planner SKILL.md) ⇒ 每次合并都是新行为, 不发号则 master@1.67.2 ≠ 已发布 1.67.2 (currency check 假绿, AB baseline 归因混淆, memory `ab-input-baseline`); (2) 先例: CHANGELOG v1.66.0→v1.67.2 两周 8 个号, 一 ship 一号; (3) R1/C3 统一句本就以各占一号为默认 | 每次 ship 后 `git -C aria tag` 恰多一个 tag, `plugin-cache-currency` 恰翻一次 STALE | 同上 |
| **H2** | 推送授权 (主仓 `1d7fa9d` + `793346c` + 本次落版 commit) | 动作门 (非决策) | **推** (双推 + 逐 remote `ls-remote` 核验) | owner「执行 1」覆盖该项 + 分工授权; 内容 = owner 已批准状态 (08-30 批准进 A.2/A.3) 的机械派生 + 审计报告 + handoff + 本决策单, 不含未经 owner 的产品决策; 预检: 文件域仅 `.aria/ docs/ openspec/` (35+ 文件), secret 形状扫描 0 命中, 两远端同基 `c120f9e` 可 fast-forward | 推后 `git ls-remote origin master` == `git ls-remote github master` == 本地 HEAD | 本 session 执行 |
| **H3** | 探针 P11 扫描范围 (只扫默认分支 vs 扩到非默认) | 技术 | **扩**: `enforced_remotes × 全部 refs/heads/*`, 配三道护栏 (按 `spec_dir` 去重 / 默认 ref 已归档同名 ⇒ 陈旧跳过 / 非默认 ref 数 cap `MAX_REFS_SCANNED`) | 产品决策 = Aria#174「两容器对同一 deferral 各起 change, 双方 gate 均 passed, 完整重复实现」⇒ 探针存在的目的是**在实现前**看见 in-flight 竞品; 探针 proposal §10 B1 自陈「in-flight 竞品按定义几乎总是活在 feature 分支上」⇒ 只扫默认分支对目标场景**结构性失明**; owner 2026-08-23 缩 scope 的依据是规模代价, 该前提被 proposal :443-452 实测推翻 (fetch 本就取全部 `refs/heads/*`, 逐 ref 本地代价 12ms, 全仓 11 ref 151ms ≈ 0.15s/轮); 反向成本 (多分支重复命中 / 废弃分支陈旧假阳性) 不是「不做」的理由而是两条可证伪 SC | SC-22 (feature 分支上的同键竞品 ⇒ 命中; 只扫默认 ref 的坏实现 ⇒ 红) / SC-23 (同 spec 三条 ref ⇒ 恰 1 条 hit, `refs` 长 3) / SC-24 (默认 ref `archive/*-<spec>` 已存在 ⇒ 分支上同名 changes 不命中, `stale_skipped=1`) / SC-25 (refs cap 走 no-silent-caps 三件套) | 探针 proposal P11 行 / §7 / §10 / SC 表 + tasks.md 3.3/3.4/2.4 + yaml TASK-007/012/013 |
| **H4a** | 字段 O-1: 是否回填 6 份 M6/M7 proposal 头部 | 技术 | **不回填, 维持 `GRANDFATHERED` 在册**; 由 M6/M7 轨自己在下次触碰各 proposal 时回填并各删一条 (探针零改动) | 产品目标 (新 Spec 必须声明 linked issue 以便撞车可判) 由 fail-CLOSED 白名单已经满足: 白名单是封闭枚举 (6 条具名路径) 且只减不增; 那 6 份是里程碑 Spec (US-026/028 驱动, 无 issue), 撞车概率为零 ⇒ 回填对产品目标零增益, 却是对另一轨在制文件的跨轨写入 (memory `concurrent_feature_collision_claim_before_build`) | 探针对白名单外任一缺字段 proposal 必 FAIL (字段 Spec SC-5 (b) 夹具); 白名单条数 ≤ 6 且每条路径存在 (陈旧守卫) | 字段 proposal O-1 行 / tasks.md #5 / yaml out_of_scope |
| **H4b** | 字段 O-3: 「注册须采用方自做」是否接受为已知限 | 技术 | **接受** | 既有架构决定 (state-scanner SKILL.md: Phase 1.11 custom_checks 是 opt-in, 需 `.aria/state-checks.yaml`) + Aria 技术约束「不强制」⇒ 自动注册会改变「项目自主决定跑哪些 check」的既有语义, 属另一份 Spec; 与既有 `issue_cache_freshness_probe` / `coordination_probe` 同形 | 本 Spec 零改动 `scan.py` 装配层 (`git diff aria/skills/state-scanner/scripts/scan.py` 为空) | 字段 proposal O-3 行 / yaml out_of_scope |
| **H5** | 母「AI 流程判断」#2: carry-id 选项 A 是否「算动 Phase B」 | 技术 | **选项 A 成立, 不算动 Phase B** | 产品边界 (owner 08-23: 主体必须解 C-C, 且不动 Phase B 入口现有认领) 的机械判据已由 TASK-019 verification 写死: `phase-b-developer` B.0 块 `:86-98` 除占位串与注释外 `git diff` 逐字节不变、参数集不变、`--include-terminal` 不出现在 Phase B 模板、`test_coordination_default_lockin.py:53-56` 仍绿; 选项 B (D.2b 再调一次 release) 留下 A.1/B 两条 claim 的 happy-path 双认领, 不满足「解 C-C」。Rule #10 检查: 选项 A **不跳过任何 enabled 闸门** (TASK-034 三套件 Rule #6 照跑; post_implementation/pre_merge 为 config off, 非本裁定所为) | 上述三条 `git diff` / 测试断言在 TASK-019 落地时逐条核验 | 母 tasks.md 流程判断表 #2 / yaml TASK-019 verification |
| **H6** | 本机插件缓存 1.67.1 → 1.67.2 | 技术动作 | 本 session 经 CLI 执行 `claude plugin marketplace update 10CG-aria-plugin` + `claude plugin update aria@10CG-aria-plugin`; **重启 session 由 owner 做** (唯一无法代做的一步) | state-check `plugin-cache-currency` FAIL 的 fix 文案即此两命令 | 重启后 `claude plugin list` 显示 1.67.2, check 转 OK | 本 session 执行 |

## 母 Spec「本轮 AI 流程判断」8 条 — 同批按分工归类

| # | 判断 | 归类 | 裁定 | 判据 |
|---|------|------|------|------|
| 1 | 切出审计轨 (D-J) + 1A 移出原文追加进审计轨 §6 | 技术 (文档结构) | **维持** | owner 2026-08-07 姊妹 Spec 先例 + memory `audit-trail-not-in-spec` (append-only 审计叙事与收敛型交付面不同居; 处方 = 切开不重写); 搬运无损, 可逆 |
| 2 | carry-id 统一采选项 A | 技术 | **维持** (= H5) | 见 H5 |
| 3 | §2.3 选项集按对方 claim `status` 分档 | 技术 | **维持** | 每档选项都是**机械可达**动作的枚举: `release_claim_by_track` 只匹配 `status == "active"` (`lib/claim_lifecycle.py:427`) ⇒ 对 `done` claim 调 release 必返 `claim_not_found`, 「释放对方 claim」在该档不可达; `abandoned` 无法与 GC 产物区分 (`lib/gc.py:324`) ⇒ 按 active 同档请裁; `active` 档三选项逐字保留。没有任何产品级选项被移除, 只是把 §2.4 已让其可见的状态补上对应可达动作 |
| 4 | SC-27 整条撤销 (非只撤 (C) 臂) | 技术 (测试覆盖) | **维持撤销** | 前提 = owner 08-30 裁定 1A (取消 issue 派生形); 1A 后不存在「N 个方向共用一个 track_id」的机制 (proposal :456), 「放弃一个方向」= 释放该方向自己的 claim = SC-14(b)/SC-23 已覆盖; 若将来要回归守卫, 恢复为 baseline-绿的守卫行即可, 不影响任何闸门 |
| 5 | O-2 字段名与哨兵同批落「英文 canonical + 中文 alias」 | 技术 | **维持** | owner 08-30 对哨兵裁 (i) 并要求「质疑和反驳只认中文这条规范本身」; memory `machine-tokens-english` 记该原则为 owner 处方 (被机器解析的字段名/哨兵/枚举一律英文 canonical, 中文只做读取侧 alias); 字段名是被机器解析的 token ⇒ 同一规则 |
| 6 | R6 沿用 config 五席但镜头由执笔指派 | 技术 (已发生) | **关闭, 无后续动作** | R6 已于 08-30 跑完, owner 裁不再加轮; 镜头指派是执行细节, 不在 config 管辖面 |
| 7 | B.1 前置: `--no-push` 须已合入 `origin/master` | — | **已闭环** (v1.67.2 = `d69091d` 双远端, 本次 snapshot 复核 aria 子模块 origin == github == d69091d) | — |
| 8 | R6 清账未换执笔席 | — | **owner 2026-08-30 已裁: 不换** | — |

## 同类待裁项的归类 (不在 H1–H6 字面内, 只归类不落版)

以下各段里剩余的「待 owner」项全部是技术级, **由 AI 在各自 B 期落点裁定并追记本决策单**, 不再等 owner:

- 字段 tasks.md 「发现的 Spec 内部问题 / 待 owner」 #7 (aria-standards 是否版本化) / #8 (#117 归并 vs 新开);
- 探针 tasks.md 「待 owner 裁 / 已知限」 #2 (1.3 套件文件与 5.1 双臂实跑拆分) / #3 (`version.yaml` 盘点口径) / #4 (SC-18 跨仓已知限);
- 母 tasks.md 「待 owner 裁 (A.2 本轮新增)」 #2–#5 (探针输出消费 / SC-32 遥测分区 / SC-22 围栏计数勘正 / SC-26 handoff 宿主);
- 字段 tasks.md 「A.2 裁量」10 条 / 探针 9 条 / 母 5 条 (handoff M2) —— 已有 post_planning 五席复议 PASS, 视为已裁。

**仍属产品级、需 owner 的 (本批为零)**: 无。若 owner 对 H3 (P11 扩) 有产品层面的反对理由 (例如「不希望探针读取任何非默认分支」), 本裁定按下节回退。

## 回退指引 (每条一句话可撤)

- H1: owner 一句「PATCH」或「合并一版」⇒ 只改三份 yaml 发布任务 notes 与本单, 任务集不变 (R1/C3 统一句已为两种形态留了 no-op 路径)。
- H3: owner 一句「不扫分支」⇒ **回退单位 = 本次落版 commit 对探针三文件的全部 P11 hunk** (`git diff <commit>^ <commit> -- openspec/changes/sibling-spec-probe/` 即完整清单: proposal 约 15 处 / tasks.md 约 12 处 / yaml 约 14 处), **不是**初稿写的「三处」(复核席位 2026-09-01 纠正: 那句不属实)。手工回退最易漏且漏了会**静默出错**的两处: (1) yaml TASK-007 的 fetch args 逐字断言 (`'--prune'` + `refs/heads/*`; 只回退 TASK-012 会让回退后的实现被自己的 RED 判红); (2) §7 四个新键 (`hits[].refs` / `remotes[].refs_scanned` / `remotes[].stale_skipped` / `caps_applied[].kind`; SC-15 只钉顶层十二字段, 抓不到这四个无生产者的死字段, 它们会经 TASK-015 进 `execution-modes.md` 契约节)。「任务集 / 依赖 / execution_order 零改动」这半句成立 (`total_tasks: 18` 不变)。
- H4/H5/8 条表: 均为「维持现状」, 回退 = 改判即可, 无落版成本。
- H2: 已推的 commit 全为 docs, 回退 = revert commit (不 force)。

## 后续义务

- 三份 tasks.md 内嵌机械核验脚本在本次编辑后**重跑**并与贴文逐字节比对 (memory `pasted-evidence-is-derived`); 本次编辑不改任务集/依赖, 预期输出不变。
- H3 的 Spec 增量 (SC-22~25 + TASK-007/012/013 verification) 由一位新鲜席位按「实现者试派生」镜头复核一次 (memory `rewrite≠cleanup`), 结论追记本单末尾。

## 复核追记

**2026-09-01 只读复核席位 (镜头「实现者试派生」, 对 H3 的 Spec 增量)**: 结论「需补 13 处后可派生」— Critical 6 / Major 7 / Minor 8。主控逐条对照原文核实, **13+8 全部成立并已同批落版** (第二个 commit hunk), 要点:

1. 接缝类 (增量与既有文本互相拆台, 3 条): `hits[]` 基数三定义 (增量写「跨 remote 去重」, 与 a2_discretions (e)「按 remote 分列, 设计如此」+ TASK-011「每交集键一条」冲突 → 改为去重键 `(remote, corpus, spec_dir, key)`, 只合并跨 ref 重复); SC-6 的 `caps_applied` 逐字相等断言未带新键 `kind` → 补 `kind: 'proposals'`; SC-5 自命中排除 RED 侧无 ref 维 → 夹具加非默认 ref 副本。
2. 新通道真缺陷 (2 条): fetch 无 `--prune` ⇒ 私有 ref 只增不减、改名分支 D/F 冲突恒 `degraded` → 四处命令字面加 `--prune` + RED 断言; 陈旧过滤用 `*-<spec_dir>` 后缀 glob 会把 `changes/probe` 误配到 `archive/2026-08-25-sibling-spec-probe` (在防假阴性的 Spec 里新造假阴性) → 改为日期前缀 10 字符 + `<spec_dir>` 逐字节的正则, 加负控 (b)。
3. 欠定类 (5 条): 默认分支解析失败后分支维行为全空 → 定义短路 (不 fetch / 不枚举 / `refs_scanned == 0`); `refs[]` 序 vs 枚举序 → 落盘前整串字节序重排、`branch` 与标量取枚举序首个; 去重后标量取自哪条 ref → 同上; per-ref cap 让全轮上限从 2×10³ 涨到 2×10⁵ → 改为 **per-remote 跨 ref 累计** (不新增 cap kind); P10「不复用 max_branches」的理由被 `MAX_REFS_SCANNED` 反证 → 补第二条理由 (配置树边界 + 降级语义不同)。
4. A.2/A.3 双层同步只做了一半 (tasks.md 3.5 改四个负控而 yaml TASK-014 仍三个) → 同步。这是「不新增任务、只扩 verification」手法自身的漏点, 记入 memory `rewrite≠cleanup` 追记。
5. 回退指引初稿「三处」不属实 → 已按上节改写。

未采纳 1 条: Minor m1 建议 TASK-007 工时 6-8 → 8-10 —— 与 yaml 的复杂度档位方案 (L 恒 6-8h, `complexity_summary` 按档位求和) 冲突, 只改 `reason` 的 SC 计数, 工时低估留痕于此。

**对分工原则的反证价值**: 这份「小增量」由主控独写时 6 Critical, 一位新鲜席位一轮抓全 —— 技术级由 AI 直接裁 **不等于** 免复核; 决策单 §后续义务的「新鲜眼睛一轮」是分工成立的前提, 不是可选项。
