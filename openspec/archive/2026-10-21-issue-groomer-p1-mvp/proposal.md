# issue-groomer P1 MVP — issue 组合面梳理 skill

> **Level**: Full (Level 3 Spec)
> **Status**: **Done (shipped v1.77.0, PR #244 `7143f3c`, 2026-10-21; 原 Approved owner 2026-10-18)** — post_spec R1-R4 CONVERGED / verdict PASS (聚合报告 `.aria/audit-reports/post_spec-R4-1792325635892-issue-groomer-p1-mvp-aggregated.md`); **Phase 0 六项裁定已裁 (owner 2026-10-18, 见 §0)** → A.2 ready
> **Created**: 2026-10-18
> **Linked Issue**: `10CG/Aria#238`
> **决策来源**: [DEC-20261018-001](../../../.aria/decisions/DEC-20261018-001-issue-ops-family-and-issue-groomer-design.md) (裁定-1~13; post_brainstorm R1-R5 CONVERGED/PASS, 聚合报告 `.aria/audit-reports/post_brainstorm-R5-1792301620523-DEC-20261018-001-aggregated.md`) + [DEC-20261018-002](../../../.aria/decisions/DEC-20261018-002-layer1-substrate-evaluation-track.md) (底座评估轨, 与本轨解耦)
> **执行轨**: interactive (裁定-11; SOT skill-benchmark-exemption §2 自主运行时禁 unattended 新增 skill)

## Why

本地 22 个开发项目仓实测 (2026-10-18): 18 仓有 open issue 共 **378 条** (Aether 97 / aria-plugin 92 / SilkNode 63 / Aria 51 / nexus 26 / 10cg.local 16; 全量快照 `scratchpad/issues-open-full-18repos-2026-10-18.json`)。aria-plugin 既有能力对 issue 仅有「单条核对」(issue-triage) 与「单项目快照渲染」(state-scanner Phase 1.13 issue_scan collector), 组合面「批量·分类·排序」零覆盖。同日 150 条手工 dogfood (Aria 系 4 仓, 支撑 10CG/Aria#235 接单) 证实: 高价值动作 (疑似已修可关单交叉核验 / owner 决策面抽取) 需项目上下文、AI 层专责; 机械部分 (fetch/分页/计数/指纹) 可脚本化。本 Spec 把该 dogfood 流程产品化为十步循环的 **issue 接活入口** (裁定-1: groomer 组合面选哪个 → issue-triage 单条核验 → Phase A/B)。

## What Changed (P1 MVP 范围, 裁定-6/7/8/9)

### 0. 裁定门 (task 0.1 — **六项已裁, owner 2026-10-18**)

| # | 裁定 | 内容 |
|---|---|---|
| ① | labels.yaml 落点 | **项目级 `.aria/labels.yaml` 优先 + 插件内置保守默认 fallback; 覆盖非合并** (项目文件存在则整体覆盖默认层; 默认层仅通用分类键 bug/feature/security/tracker)。前缀→分类键映射表随 yaml 走 |
| ② | 契约面资产落点 | groom.py 于 `scripts/`; **schema = `scripts/groom-report.schema.json`** (机器可校验 JSON Schema 文件; SKILL.md references 留指针) |
| ③ | provenance 取值源 | **分层采集**: groom.py 记 harness (调用参数自报); model id 由适配层写 assessment 时补全; 复用门比对完整拼接串 |
| ④ | 第 11 态 + assessment 存储 | **两文件各自 last-writer-wins**: 状态文件 `.aria/cache/groom-state.json` 单一固定路径; assessment 独立文件 `groom-assessments.json` (物理隔离, 无跨文件合并语义); **并发 fixture 态升为正式 SC 矩阵成员** (非候选) |
| ⑤ | 两缺口单 | **保持两张** (#239 trigger 面 / #240 Tier B 面; 解锁路径与验收面不同) |
| ⑥ | #239 未解冻 ship 语义 | **恒阻塞至解冻 (fail-closed, 无逐案放行; 唯一出路 = #213 的 owner 审阅解冻)** — 比 SC-6 草案更严, owner 2026-10-18 选定 |

### 1. 机械核 `groom.py` (harness-agnostic, stdlib-only; 允许 scripts/ 模块拆分, 契约面可及性不变)

- **双端点全分页 fetch**: issue-list **与 comments 端点**均全分页 + 终止条件 (修 plugin#208 limit=50 静默丢数据; ⚠️ 仓内先例 `issue-triage/scripts/collectors/_issue.py:93` 即单页 limit=50 — 不照抄)。**comments 端点默认按创建序返回 (首页 = 最旧 50 条)**: >50-comment issue 的最新评论结构性不可见 ⇒ 排序语义必须钉死 (sort/direction 取最新页, 或全分页取 max(updated_at)), 并补 >50-comment 截断反例 fixture。多仓面复用 `state_scanner.issue_scan` 配置形态 (作用域 = 项目内卫星仓, 裁定-2)。
- **Tier A 机械粗分** (裁定-7): 只用显式编码信号 (title 前缀 / label / staleness 档 / 活跃度); **confidence = 逐信号枚举**; 无显式信号 → `category=unknown` 不猜 (负面 fixture 钉 SC 必测); **前缀映射表入 labels.yaml** (taxonomy hash 覆盖 ⇒ 规则升级触发重分类); **staleness/活跃度判据预留确定性时钟注入 seam** (fixture 可注入 now, 防 flaky)。
- **增量三面指纹** (裁定-9): ① issue 面 = title/body/labels hash + comments 最新 updated_at (**三态: 值 / null(零评论) / unknown(fetch 失败) — 失败不冒充零评论**, 复刻 issue_scan fetch_error 纪律); 显式排除 assignee/milestone/due_date; ② 上下文面 = openspec/changes/ 全树内容级 hash + 主仓与卫星仓 git HEAD + handoff 权威 = latest.md pointer (非 mtime) + labels.yaml taxonomy hash; archive/ 显式排除; ③ provenance 面 = harness + model id (取值源 = 裁定门 ③)。
- **复用规则**: Tier A 复用 = 分类输出 + 判据输入快照 (时间敏感字段跨档触发重分类); Tier B 仅 provenance 相同可复用, 否则 `stale-assessment`。
- **Tier B assessment 持久化回路** (R1 BA 席): assessment 产自适配层 (AI), 存储面 = 独立文件 `groom-assessments.json` 或 state 专属区 (裁定门 ④); **groom.py 重写状态时必须保留非自有 assessment 键** (第二写者合并语义 + 原子性归属随裁定门 ④)。
- **diff 段**: 新增/已关闭 = 集合差; 优先级漂移仅有新评估条目报告 (top-N 上限); baseline run = no-diff (有专属 fixture)。
- **状态文件** `.aria/cache/groom-state.json` 原子写 (temp+rename; plugin#180 两半教训)。
- **输出契约**: groom-report JSON schema v1 additive-only; 文档位置随裁定门 ②。

### 2. SKILL.md 适配层 (仅 Claude Code 侧)

- **Tier B 语义评估** 流程 (裁定-7): 疑似已修可关单 / 优先级 vs 在制轨道 / owner 决策面抽取 — 产独立 `assessment` 面带 provenance; 多 harness 诚实主张 = 可移植面为事实面 + Tier A。
- **渲染层**: JSON → MD (分类汇总 / 优先级分档 / 决策面 / diff 段)。
- **双源同步义务预告** (裁定-13): P2 时契约面 reply 模板定义与 issue-triage CC 适配模板族是**两份资产, 一处改动须同步另一处** — 在此预告防静默分叉 (P1 无 reply 模板, 零执行面)。

### 3. 标签信息契约 (裁定-8, 只产不写)

`labels: {existing, suggested, apply_payload{repo, number, add=suggested−existing 差集, idempotent}}`; schema 禁 remove 字段 (additionalProperties:false 封闭键集)。**「forgejo 对已有 label 的 add 为 no-op」是外部 API 行为断言**: Phase 1 前对 10cg.local **live 实测一次** duplicate label add, 结果落 SKILL.md references; 差集断言本身 harness 无关, mock 不编码 no-op 假设 (防断言循环自证)。taxonomy 配置 labels.yaml + groom.py 运行时一致性自检。

### 4. 测试面 (task 1.3 逐 SC 映射枚举 — R1 QA 席修正: 分量级 mandate 归 Tier A lane)

- **SC 结构化测试**: 10 态 fixture 矩阵 (裁定-9 枚举 ①-⑩, 内联表见 DEC; **分量级反事实 mandate 在 1.3 执行**: ③ 态按上下文面四分量各设独立变体 / ⑨ 态按 harness 与 model id 各设变体 / ⑩ 补 comment-edit 判别 fixture — 合成 updated_at>created_at 样本, 区分 max(updated_at) vs max(created_at)/count 错误代理)
- **Tier B 定向 fixture** (判据表第三行, #240 — 仅 Tier B 语义行为; 三条移交附注中 ①② 属 Tier A 机械项已归 1.3; #240 勘正评论已发 (comment 29237), body 未改动)
- **语料**: 三份快照 (scratchpad/issues-open-full-18repos-2026-10-18.json 378 条 / scratchpad/issues-open-2026-10-18.json 150 条 / scratchpad/issues-sample-body-comments-2026-10-18.json body+comments 形态) — 不复制入库; **再生成命令** (live API 重取脚本) 附 SKILL.md references; scratchpad 单点落点风险显式接受 (清理即失, 靠再生成恢复)。

### 非范围 (P1 明确排除)

P2 (label apply CLI + reply 模板族两档 — **双源同步义务已在 §2 预告, P2 spec 须承接**) · P3 (Layer 1/fleet 自主驱动) · 跨项目全局 (M7 fleet) · 写回任何 tracker 状态。

## Key Deliverables

- `aria/skills/issue-groomer/scripts/groom.py` (最终路径随裁定门 ②; 允许 scripts/ 模块拆分)
- `aria/skills/issue-groomer/SKILL.md`
- `aria/skills/issue-groomer/tests/` (10 态 + 分量级 mandate + 逐 SC fixture + taxonomy 自检)
- groom-report JSON schema v1 (文档位置随裁定门 ②)
- 语料再生成命令 + forgejo add no-op live 实测记录

## Constraints

| 类型 | 约束 | 来源 |
|------|------|------|
| 架构 | 多 harness 横向扩展 (契约面 plugin 外可及) | 裁定-3/13; DEC-002 评估轨依赖此面 |
| 架构 | AD7: Layer 1 不加载 aria-plugin (P1 不触 Layer 1) | 裁定-11 |
| 方法论 | Rule #6 完整档位矩阵 (下节) | 裁定-11; #239/#240 |
| 方法论 | **ship 时序: dogfood (4.1) 先于发版 ship** — dogfood 发现缺陷走修复后重验, 不落 post-bump 处置 | R1 TL 席 |
| 实证 | title 前缀是主要存量分类信号 (label 几乎全空) | DEC 背景 |
| 时机 | 与 M6 在制轨 / DEC-002 评估轨互不阻塞 | DEC-001 约束表 |

## Rule #6 档位矩阵 (rule6_note 预填, 裁定-11)

| 变更面 | 义务 | 缺口单 |
|---|---|---|
| groom.py (Tier A, 纯代码) | **判据表第一行 SC substitute (替代非叠加)** + 结构化测试 | 新建测试 |
| SKILL.md 适配层指令逻辑 | 场景 1 AB (判据表第二行) | 既有 AB 机制 |
| skill description (必然 yes) | 场景 1 + 场景 4b 地板守卫 (SOT §4.1 硬义务) — **现状 ab-suite/trigger/ 0 套件 (实测, 锚 #213) ⇒ 结构性填不出合规 rule6_note** | **#239** |
| Tier B 语义行为 (prose) | 判据表第三行: 点名行为 + 定向 fixture + 缺口 issue | **#240** |

rule6_note 成文形式 (task 3.1): 按 SOT §4.1 **五字段逐变更面成条 (共四条)**; negctrl 字段口径随 3.1 预填; 不折叠成单条。

## 关键决策 (全量见 DEC-20261018-001)

| 决策 | 选择 | 引用键 |
|---|---|---|
| 首要目的 | AI 接活入口 (非决策支持/防腐化/跨项目) | 裁定-1 |
| 作用域 | 项目内卫星仓 (跨项目留 M7 fleet) | 裁定-2 |
| 触发 | 显式独立触发 (多 harness) | 裁定-3 |
| 输出 | JSON 报告 + 渲染层, v1 不写回 | 裁定-4/5 |
| 形态 | 独立 skill + 脚本核 + 适配层; groomer→triage→十步循环 | 裁定-6 |
| 命名消歧 | Tier A/B = 分类层轴; ops/dev-tier = reply 执行档轴 (P2) | 命名消歧表 |

## Success Criteria

- [ ] SC-1 10 态矩阵 + **第 11 态 (并发: 两文件各自 last-writer-wins, 裁定④)** 全绿且逐态反事实成立 + **分量级 mandate 全绿** (③ 四分量 / ⑨ 两分量 / ⑩ comment-edit 判别 + 合成样本)
- [ ] SC-2 **双端点** (issue-list + comments) 全分页零丢失: 多页 mock + 终止条件 + **>50-comment 截断反例** + comments 排序语义钉死
- [ ] SC-3 Tier A 每分类判据有独立反事实 fixture; 无显式信号 → unknown (负面 fixture); 时钟 seam 可注入
- [ ] SC-4 增量语义: baseline no-diff (专属 fixture) / 复用规则 / provenance 门 / diff top-N 上限 fixture; comments 分量三态 (值/null/unknown)
- [ ] SC-5 apply_payload = suggested−existing 差集 (harness 无关断言); no-op 前提经 live 实测记录 (mock 不编码)
- [ ] SC-6 Rule #6 **义务全集判绿 (四 facet)**: ① 场景 1 AB 照跑且 pass (矩阵第二行); ② 4b 两分支 — **套件已解冻 ⇒ 4b 照跑且 pass; 未解冻 ⇒ ship 恒阻塞至解冻 (裁定⑥ fail-closed, 无逐案放行; 唯一出路 = #213 owner 审阅解冻)**; ③ Tier B 定向 fixture 三条件齐备 (判据表第三行, task 2.2, #240); ④ rule6_note 五字段×四变更面成文且合规 (task 3.1)
- [ ] SC-7 dogfood 判绿标准: 全量条数对账 (fetch 计数 vs 快照计数) + 与 2026-10-18 手工梳理**差异逐条归因清单**; Aria 仓 + ≥1 外项目试点
- [ ] SC-8 groom-report JSON schema v1 文档化 + additive-only 契约
- [ ] SC-9 labels.yaml taxonomy 一致性自检 (前缀表 + 分类键 + label 名三层)

## Tasks

见 [tasks.md](./tasks.md) (双层架构; detailed-tasks.yaml 由 A.2 task-planner 生成)。

## Validation Note

`openspec validate issue-groomer-p1-mvp --strict` (2026-10-18, CLI 本机已装 `~/.local/bin/openspec`) 报: 缺 `specs/` delta 目录 (## ADDED Requirements + Scenario 块)。**处置**: 与近期全部归档先例同形态 (pre-merge-completeness-gate / rule6-description-change / handoff-multibranch 等均无 specs/); openspec CLI 统一口径 (是否应装/归档目录兼容/版本钉法) 是 Aria#212 owner 待裁项 — 本 Spec 不单方面引入 delta 格式, 遵循现行房规, 待 #212 裁定后全仓统一。

## Runtime Amendment (mid_post_spec, append-only, 2026-10-19 B.2 实施期发现)

> Phase B 实施期 (TASK-009) 实测发现 spec 陈述与运行实际不符, 按 Aria #79 mid_post_spec 机制 append-only 修订 (advisory, 不回改正文, 采纳后以本节为准):

1. **comments 端点分页前提修正**: §1 原文「comments 端点默认按创建序返回 (首页 = 最旧 50 条)…>50-comment issue 的最新评论结构性不可见」在本 Forgejo 实例 (11.0.16+gitea-1.22.0) **不成立** — 实测 (TASK-009 三组实验 + 主 loop 独立复验): comments 端点**忽略 limit/page 参数, 恒全量返回** (升序最旧在前; 越界页回吐同页非空)。**修正后的 fetch 契约**: comments 取回不做分页游走, 单次全量响应 + 用 issue 的 `comments` 计数字段对账, `collected ≠ count ⇒ fail-closed` 报错; SC-2 的「>50-comment 截断反例」fixture 真实形态 = **服务端忽略分页参数** (mock 层钉此形态)。
2. **no-op 前提落定 (SC-5 附注)**: live 实测 duplicate label add = 彻底 no-op (2xx + 无 updated_at 变化); fresh add 会 bump `updated_at` ⇒ `add = suggested−existing` 差集保留的实证理由 = **写放大最小化** (非 API 幂等的必要条件)。mock 不编码 no-op 纪律不变。记录: `references/forgejo-behavior-notes.md` (版本钉死)。
3. **残留披露**: 探测动作使 #238 `updated_at` 前移 (title/body/labels/comments 零变化 — 非指纹分量)。
4. **Tier B 上下文门补全 (TASK-007 席发现, 主控裁定 2026-10-19)**: 裁定-9「上下文一变 → 全量重评」的精确分层实现 — **Tier A 免重评** (分类输入 ⊆ issue_key ∪ judgement_inputs, taxonomy_hash 已在判据输入, 其余上下文分量数学上不可能改变 Tier A 分类 — 席位健全性论证采纳); **Tier B 补上下文门**: assessments entry 增必填 `context_key` (context_fingerprint 的 canonical hash), `gate_tier_b` 比对当前 context_key — 不匹配 ⇒ stale (reason `context-changed`), entry 缺 context_key ⇒ stale (reason `context-missing`, fail-closed)。「全量重评」的实现形态 = **Tier B 全量 stale 标记** (重评由适配层执行, 引擎诚实标 stale)。STALE_REASONS 枚举相应 +2。
