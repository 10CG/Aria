# issue-groomer P1 MVP — issue 组合面梳理 skill

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-10-18
> **Linked Issue**: `10CG/Aria#238`
> **决策来源**: [DEC-20261018-001](../../../.aria/decisions/DEC-20261018-001-issue-ops-family-and-issue-groomer-design.md) (裁定-1~13; post_brainstorm R1-R5 CONVERGED/PASS, 聚合报告 `.aria/audit-reports/post_brainstorm-R5-1792301620523-DEC-20261018-001-aggregated.md`) + [DEC-20261018-002](../../../.aria/decisions/DEC-20261018-002-layer1-substrate-evaluation-track.md) (底座评估轨, 与本轨解耦)
> **执行轨**: interactive (裁定-11; SOT skill-benchmark-exemption §2 自主运行时禁 unattended 新增 skill)

## Why

本地 22 个开发项目仓实测 (2026-10-18): 18 仓有 open issue 共 **378 条** (Aether 97 / aria-plugin 92 / SilkNode 63 / Aria 51 / nexus 26 / 10cg.local 16; 全量快照 `scratchpad/issues-open-full-18repos-2026-10-18.json`)。aria-plugin 既有能力对 issue 仅有「单条核对」(issue-triage) 与「单项目快照渲染」(state-scanner Phase 1.13 issue_scan collector), 组合面「批量·分类·排序」零覆盖。同日 150 条手工 dogfood (Aria 系 4 仓, 支撑 10CG/Aria#235 接单) 证实: 高价值动作 (疑似已修可关单交叉核验 / owner 决策面抽取) 需项目上下文、AI 层专责; 机械部分 (fetch/分页/计数/指纹) 可脚本化。本 Spec 把该 dogfood 流程产品化为十步循环的 **issue 接活入口** (裁定-1: groomer 组合面选哪个 → issue-triage 单条核验 → Phase A/B)。

## What Changed (P1 MVP 范围, 裁定-6/7/8/9)

### 1. 机械核 `groom.py` (harness-agnostic, stdlib-only)

- **全分页 fetch**: 修 plugin#208 limit=50 静默丢数据陷阱; 多仓面复用 `state_scanner.issue_scan` 配置形态 (作用域 = 项目内卫星仓, 裁定-2)
- **Tier A 机械粗分** (裁定-7): 只用显式编码信号 (title 前缀 / label / staleness 档 / 活跃度); **confidence = 逐信号枚举** (每条列出命中信号集, 非聚合分数); 无显式信号 → `category=unknown` + 溯源空集, **不做语义猜测** (负面 fixture 钉 SC 必测)
- **增量三面指纹** (裁定-9): ① issue 面 = title/body/labels hash + comments 最新 updated_at (显式排除 assignee/milestone/due_date); ② 上下文面 = openspec/changes/ 全树内容级 hash + 主仓与卫星仓 git HEAD + handoff 权威 = latest.md pointer (非 mtime) + labels.yaml taxonomy hash; archive/ 显式排除; ③ provenance 面 = harness + model id (取值源待裁, task 2.2)
- **复用规则**: Tier A 复用 = 分类输出 + 判据输入快照 (时间敏感字段跨档触发重分类); Tier B 仅 provenance 相同可复用, 否则 `stale-assessment`
- **diff 段**: 新增/已关闭 = 集合差; 优先级漂移仅有新评估条目报告 (top-N 上限); baseline run = no-diff
- **状态文件** `.aria/cache/groom-state.json` 原子写 (temp+rename; plugin#180 两半教训 — 第 11 态候选在 task 2.2 裁定)
- **输出契约**: groom-report JSON, `snapshot_schema_version` 同款 additive-only 演进

### 2. SKILL.md 适配层 (仅 Claude Code 侧)

- **Tier B 语义评估** 流程 (裁定-7): 疑似已修可关单 / 优先级 vs 在制轨道 / owner 决策面抽取 — 产独立 `assessment` 面带 provenance; 多 harness 诚实主张 = 可移植面为事实面 + Tier A
- **渲染层**: JSON → MD (分类汇总 / 优先级分档 / 决策面 / diff 段)

### 3. 标签信息契约 (裁定-8, 只产不写)

`labels: {existing, suggested, apply_payload{repo, number, add=suggested−existing 差集, idempotent}}`; schema 禁 remove 字段; taxonomy 配置 labels.yaml (落点待裁, task 2.2) + groom.py 运行时一致性自检。

### 4. 测试面

- **SC 结构化测试**: 10 态 fixture 矩阵 (裁定-9 枚举 ①-⑩) — 逐态反事实 (⑩ 态 = 内容 hash 与 comments 分量各自退化必红); 语料 = 三份落盘快照 (真 Forgejo 响应形态)
- **Tier B 定向 fixture** (判据表第三行, 缺口单 #240): 点名行为 + 可证伪; 附注三条移交 (既有评论编辑用例 / ③ 态四分量变体 / ⑩ 分量级先例)

### 非范围 (P1 明确排除)

P2 (label apply CLI + reply 模板族两档) · P3 (Layer 1/fleet 自主驱动) · 跨项目全局 (M7 fleet) · 写回任何 tracker 状态。

## Key Deliverables

- `aria/skills/issue-groomer/scripts/groom.py` (路径暂定, 随 task 2.2 契约面资产落点裁定)
- `aria/skills/issue-groomer/SKILL.md`
- `aria/skills/issue-groomer/tests/` (10 态 fixture + Tier A 规则反事实 + taxonomy 自检)
- groom-report JSON schema v1 (文档化于 SKILL.md references)
- 语料 fixture 接入 (三份快照的引用声明, 不复制入库)

## Constraints

| 类型 | 约束 | 来源 |
|------|------|------|
| 架构 | 多 harness 横向扩展 (契约面 plugin 外可及) | 裁定-3/13; DEC-002 评估轨依赖此面 |
| 架构 | AD7: Layer 1 不加载 aria-plugin (P1 不触 Layer 1) | 裁定-11 |
| 方法论 | Rule #6 完整档位矩阵 (下节) | 裁定-11; #239/#240 |
| 实证 | title 前缀是主要存量分类信号 (label 几乎全空) | DEC 背景 |
| 时机 | 与 M6 在制轨 / DEC-002 评估轨互不阻塞 | DEC-001 约束表 |

## Rule #6 档位矩阵 (rule6_note 预填, 裁定-11)

| 变更面 | 义务 | 缺口单 |
|---|---|---|
| groom.py (Tier A, 纯代码) | 场景 1 + SC 级结构化测试替代 (判据表第一行) | 新建测试 |
| SKILL.md 适配层指令逻辑 | 场景 1 AB (判据表第二行) | 既有 AB 机制 |
| skill description (必然 yes) | 场景 1 + 场景 4b 地板守卫 (SOT §4.1) | **#239** (trigger 0 套件, 锚 #213) |
| Tier B 语义行为 (prose) | 判据表第三行: 点名行为 + 定向 fixture + 缺口 issue | **#240** |

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

- [ ] 10 态 fixture 矩阵全绿且逐态反事实成立 (任一指纹分量实现退化成常量 ⇒ 对应态必红)
- [ ] 全分页 fetch 零丢失 (多页 mock + 终止条件测试)
- [ ] Tier A 每分类判据有独立反事实 fixture; 无显式信号 → unknown (负面 fixture)
- [ ] 增量语义落地: baseline no-diff / 复用规则 / provenance 门 / diff top-N
- [ ] apply_payload = suggested−existing 差集, 幂等可机械验证 (forgejo add no-op 构造)
- [ ] Rule #6: 场景 1 AB 照跑 + 4b 处置留痕 (#239) + Tier B fixture (#240) + rule6_note 成文
- [ ] dogfood: Aria 仓实跑 + 至少一个外项目试点 (Aether 或 SilkNode)
- [ ] groom-report JSON schema v1 文档化 + additive-only 版本契约

## Tasks

见 [tasks.md](./tasks.md) (双层架构; detailed-tasks.yaml 由 A.2 task-planner 生成)。
