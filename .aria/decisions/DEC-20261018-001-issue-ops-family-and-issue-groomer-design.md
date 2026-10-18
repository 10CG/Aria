# 决策: DEC-20261018-001 — issue-ops 能力族定位与 issue-groomer skill 设计裁定

> **日期**: 2026-10-18 | **模式**: problem (brainstorm v2.0, 三轮 AskUserQuestion + 五段设计逐段确认)
> **参与者**: owner (simonfish) 逐项裁定 + AI 执笔 | **状态**: Confirmed (owner) → post_brainstorm R1→R5 (5/5 轮, R4+R5 干净轮集合相等 + 全票 PASS) → **CONVERGED · verdict PASS** (聚合报告: `.aria/audit-reports/post_brainstorm-R5-1792301620523-DEC-20261018-001-aggregated.md`; 修订史见 §修订记录)
> **裁定编号**: 裁定-1 ~ 裁定-13 (spec 引用键 = 「DEC-20261018-001 裁定-N」)

## 背景

本地 22 个开发项目仓实测 (2026-10-18): 18 仓有 open issue 共 **378 条** (Aether 97 / aria-plugin 92 / SilkNode 63 / Aria 51 / nexus 26 / 10cg.local 16 …)。**两份落盘快照**: 全量 `scratchpad/issues-open-full-18repos-2026-10-18.json` (18 仓/378 条) + Aria 系 4 仓 dogfood 语料 `scratchpad/issues-open-2026-10-18.json` (150 条)。aria-plugin 既有能力对 issue 只有「单条核对」(issue-triage) 与「单项目快照渲染」(state-scanner **Phase 1.13 issue_scan collector**, 非插件版本号), 组合面「定期·批量·分类·排序」零覆盖。同日手工 dogfood 150 条 (Aria 系 4 仓, 支撑 10CG/Aria#235 接单): 高价值动作 = 疑似已修可关单交叉核验 + owner 决策面抽取 (均需项目上下文, 机械做不到); 机械部分 (fetch/分页/计数) 可脚本化。外部实践 (2026): AI backlog grooming 已成熟 — 重复检测/severity/stale 清理/路由已有行业指南与研究报告 ([Augmentcode AI Backlog Grooming guide](https://www.augmentcode.com/guides/ai-backlog-grooming), 页面实测口径: grooming 占 sprint 容量 5-10%、自动化估计 30-40%; 2025-07 arXiv GenAI backlog grooming 研究有 45% 量级时间降声称 — **转引未一手复核, 数字不进 spec 引用面, 仅方向性参考**)。管线先例: M7 aria-fleet aggregation (Approved, D3 时机门) 回答「哪个项目卡了」(7 类健康信号均为 snapshot 降维, R1 审计核验不含 issue 内容级分析), 不回答「哪些 issue 该先修」。

## 命名消歧 (两个 Tier 轴)

| 轴 | 名称 | 含义 | 隐含映射 |
|---|---|---|---|
| **分类层轴** | Tier A / Tier B | 梳理产物的两层: 机械粗分 / 语义评估 | — |
| **reply 执行档轴** | ops-tier / dev-tier | 回复动作的两档执行成本与模型 | ops-tier ≈ 消费契约面 (Tier A 原料+模板); dev-tier ≈ 消费 Tier B 语义面 |

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 架构 | 多 harness 横向扩展 (owner 首要新增约束: 兼容 pi durable 等 AI 工具) | 形态必须是独立触发 + harness-agnostic 脚本核, 不能埋进 state-scanner 编排层 |
| 架构 | AD7: Layer 1 不加载 aria-plugin | 自主定期跑若走 Layer 1 须消费脚本核而非 skill 层 |
| 方法论 | Rule #6: 新 skill = MINOR+ + AB; Aria#213 trigger 套件债 (该单 title 自述 41 skill 无套件) | 新 skill 有真实边际成本; **完整档位矩阵见裁定-11** |
| 实证 | org 现状: issue 分类编码在 title 前缀, label 几乎全空 | Tier A 的 title-前缀解析是主要存量信号源; label 体系经本能力反向立起 |
| 时机 | M6 在制 (Blocker 3/4 压 owner/infra 门) | 本设计纯对内零底座依赖, 不受 M6 阻塞也不反噬 |

## 考虑的方案 (逐项裁定记录)

| 议题 | 选项 | 裁定 |
|------|------|------|
| 首要目的 (裁定-1) | a.owner 决策支持 / **b.AI 接活入口** / c.积压防腐化 / d.跨项目视图 | **b** (服务十步循环 A.0/A.2, 像 state-scanner 推荐工作流那样推荐「下一个该处理的 issue」) |
| 作用域 (裁定-2) | **a.项目内卫星仓** / b.全局跨项目 / c.项目内先行预留 fleet | **a** (复用 state_scanner.issue_scan 多仓配置; 跨项目留给 M7 fleet) |
| 触发节奏 (裁定-3) | a.每次 scan 常驻轻信号 / **b.显式独立触发深梳** / c.两层 | **b** + 独立触发约束 (多 harness) |
| 输出契约 (裁定-4) | **a.JSON 报告+渲染层** / b.可选写回 / c.纯会话 | **a** (v1 不写回) |
| 标签 (裁定-5) | 写回 / **只产不写** | **只产不写**: 产出含明确标签信息 (suggested_labels + apply_payload), 供后续 forgejo 打标动作零歧义读取 |

## 最终设计 (裁定-6 ~ 裁定-13, owner 逐段确认 + R1 修订)

**裁定-6 形态**: 独立 skill `issue-groomer` (命名可议) + 机械核 `groom.py` (stdlib-only, 复刻 scan.py/triage.py 模式, 产 schema 版本化 additive-only JSON) + SKILL.md 仅为 Claude Code 适配层。链路定位: **groomer (组合面: 选哪个) → issue-triage (单条: 真伪/复现) → 十步循环 Phase A/B**。

**裁定-7 分类两层契约** (诚实精度): **Tier A 机械粗分** = groom.py, 只用显式编码信号 (title 前缀/label/staleness 档/活跃度), **confidence = 逐信号枚举** (每条列出命中信号集, 非聚合分数; 无显式信号 → `category=unknown` + 溯源空集, **不做语义猜测** — 负面 fixture 钉为 SC 必测); **Tier B 语义评估** = AI 层 (各 harness 自己的模型 + 项目上下文), 产独立 `assessment` 面带 provenance (疑似已修/优先级 vs 在制轨/owner 决策面)。多 harness 诚实主张: 可移植 = 事实面 + Tier A; Tier B 质量随 harness 模型与上下文获取能力而变, 契约只保证面存在且格式稳定。fixture 从真 Forgejo 响应形态构造 (语料 = 两份 issue-list 端点快照: 全量 378 条 + Aria 系 dogfood 150 条; + **body/comments 端点形态样本** `scratchpad/issues-sample-body-comments-2026-10-18.json` [5 issue body + 6 comment 含 created_at/updated_at 真形态 — 指纹① body 与 comments 分量的语料来源], 防形态脱节假绿)。

**裁定-8 标签信息契约**: `labels: {existing, suggested, apply_payload{repo, number, add, idempotent}}`; **`add` 基准 = suggested − existing 差集** (幂等断言按 forgejo 对已有 label 的 add 为 no-op 构造); schema 禁 remove 字段 (只加不删为结构面, 可机械验证)。项目级 taxonomy 配置 (labels.yaml, 分类键→forgejo label 规范名, 不 hardcode, 对齐 M7 L1-无硬编码哲学); **落点待裁** (候选: 项目级 `.aria/labels.yaml` 优先于插件内置默认 taxonomy; 精确优先级与分发面 spec 阶段定, 在此显式标注为待定项); taxonomy 一致性检查挂载点 = groom.py 运行时自检 (+ 可选挂 state-checks)。

**裁定-9 增量设计** (R1 三席修订后):
- **指纹三面** (输入字段封闭枚举 + 显式排除, v3): ① issue 面 = title/body/labels hash **+ comments 最新 updated_at** (评论流变化触发重评 — plugin#208 自证评论是评估关键输入); **显式排除**: assignee/milestone/due_date 不入指纹 (变化不触发重评; 若 spec 阶段裁定纳入须加对应 fixture); ② 上下文面 = `openspec/changes/` **全树内容级 hash (含 proposal/tasks/design/specs delta, 非文件名级** — 在制 spec 任何实质修订必须触发重评) — **`openspec/archive/` 显式排除** (归档时 changes/ 目录消失已天然触发; 历史 archive 修订不影响在制轨判断) **+ 主仓与卫星仓 git HEAD** (覆盖无 OpenSpec 的 Level 1 hotfix 代码变更) + handoff 权威信号 = **latest.md pointer (非 mtime**, 对齐本项目 collector 以 pointer 为语义权威的既有教训) + **labels.yaml taxonomy hash** (taxonomy 变 ⇒ suggested 变 ⇒ 须重评); ③ provenance 面 = harness + model id (**取值源待裁**: 模型 API 回报 vs 执行方自报、id 是否版本化标识符 — 同 id 经路由层静默升级的例证须覆盖; spec 阶段钉死)。
- **复用规则**: Tier A 复用的是「分类输出 + 其判据输入快照」; **判据输入含时间敏感字段 (staleness/活跃度), 跨档即触发重分类**; Tier B assessment 仅 **provenance 相同 (同 harness+model)** 才可复用, 否则标记 `stale-assessment` 待重评 — 杜绝跨 harness 静默复用 (R1 TL-M2)。
- **diff 段**: 新增/已关闭 = 集合差 (机械); 优先级漂移**仅在有新评估的条目上报告**; 上下文全量重评时漂移面=全体 → 报告带 top-N 上限防爆量; **首跑/状态文件缺失 = baseline run, diff 段标记 no-diff (语义显式定义)**。
- **SC 必测 fixture 矩阵** (**10 态**, v3 扩; 钉为 spec 验收面): ① 新条目 / ② 未变 / ③ 上下文变 / ④ 已关闭 / ⑤ **已关闭后重开** (钉死: 走新条目路径重评, 不恢复既有记录) / ⑥ 编辑但内容等价 / ⑦ rebase 后 updated_at 变 / ⑧ 时间敏感字段跨档 / ⑨ provenance 变 / ⑩ **issue 内容面正向态: label 人工增删 / title/body 实质编辑 / comments 最新 updated_at 变 (新评论) — 任一发生 ⇒ 必判变触发重评** (内容 hash 与 comments 分量各自的核心反事实 — 任一分量实现退化成常量时本态必红; 与 apply_payload 自写 label 后的下轮判变同 fixture 覆盖)。**第 11 态候选 (spec 裁定项)**: 并发写 last-writer-wins — 状态文件单一固定路径复刻了 plugin#180 另一半前提 (原子写 temp+rename 只防 torn read, 不防互相顶掉 baseline), spec 阶段二选一: per-terminal 后缀路径隔离, 或显式声明 last-writer-wins 语义 + 并发 fixture 态。
- 状态文件 `.aria/cache/groom-state.json` 原子写 (temp+rename)。原子写依据: aria-plugin#180「快照写入非原子——并发扫描互相截断 (AB 20+ 臂实证)」(2026-10-18 live API 复核 title 逐字吻合; R1 KM 席所报归因冲突系其子进程 wrapper 404 故障, 已澄清, 见其报告落盘补记; **R2 KM 席指出 #180 教训的另一半「输出路径钉死单一固定路径」由本设计的前提复刻 — 处置见第 11 态候选**)。全量分页 fetch (修 plugin#208 limit=50 静默丢数据)。
- 依据精确化: 「评估翻转」现象 = issue 本体不动、修复性 spec 落地使其转为「疑似已修」候选 — 实证为 aria-plugin#110 (sync_status 陈旧 ref 假 parity, open) 由 state-scanner-stale-refs spec (F3′/F4′ freshness) 落地而转「疑似已修」, 现象佐证另见 2026-09-30 owner rulings「疑似已修未关」清单 (KM 席核验)。

**裁定-10 reply 两档 + 动词全景**:
- reply 拆 **ops-tier** (收录/归类/打标告知; 轻模型或纯模板, Layer 1 级) / **dev-tier** (技术反馈; 高模型+项目上下文, Layer 2 级); JSON 带 `tier` 字段供执行主体路由; 喂 M6 cost-model 遥测维度。此拆分 = v2.0 两层分工 (AD1/AD7) 在 reply 动词上的投影, 亦是底座可竞争的前提。
- **裁定-13 (R1 新增, v3 补) ops-tier 载体可及性**: ops-tier 动作的资产分两类 — **契约面资产** (groom-report JSON + reply 模板定义 + label apply 薄 CLI [P2 资产, P1 期契约面实际仅 JSON]) 全部 **plugin 外可及** (脚本/契约层, 任何 harness 与 Layer 1 直接消费); issue-triage 模板族扩展**仅为 Claude Code 侧适配**。AD7 由契约面满足, 不依赖 plugin 加载。**契约面资产落点待裁** (reply 模板定义 / label apply CLI 的仓内位置, 比照 labels.yaml 待定惯例); **双源同步义务**: 契约面 reply 模板定义与 issue-triage CC 适配模板族是两份资产, 同步义务 (一处改动须同步另一处) 预告入 spec, 防静默分叉。
- 动词全景修正: 对外 = report 立单 (各项目自身 tracker + dashboard issue form 多 backend; **aria-report 是 Aria 自身 meta 通道, 移出通用集**) / reply (两档) / label (apply_payload 消费者); 对内 = groom (本设计) / triage (已有)。
- **「aria bot」= 动词 × 执行主体的装配体, 非新单体**。里程碑: P1 issue-groomer MVP (纯对内) → P2 label apply + reply 模板化 (tracker 面, 授权门) → P3 Layer 1/fleet 自主驱动 (bot 成形, 时机门内)。

**裁定-11 Rule #6 完整档位矩阵** (R1 修订, QA-M1):
| 变更面 | Rule #6 义务 | 现状缺口 |
|---|---|---|
| groom.py (Tier A, 纯代码) | 场景 1 + **SC 级结构化测试替代** (判据表第一行) | 无 (新建测试) |
| SKILL.md 适配层指令逻辑 | 场景 1 AB (判据表第二行) | 走既有 AB 机制 |
| **skill description (新 skill 必然 yes)** | **场景 1 + 场景 4b 地板守卫** (SOT §4.1 皆必填) | **ab-suite/trigger/ 实测 0 套件 (2026-10-18, 锚 Aria#213) — 结构性填不出合规 rule6_note** |
| Tier B 语义行为 (prose) | 判据表第三行: 点名行为 + 可证伪定向 fixture + 套件缺口开 issue | 待建 fixture |

**行动项 (立项时执行, 非「随评估」时点承诺)**: ① 开 **trigger 套件缺口 issue** (4b/description 面, 锚 Aria#213, 含 owner 审 20 条 query 解锁路径); ② 开 **Tier B 行为套件缺口 issue** (场景 1 覆盖外 fixture); 两条缺口**是两个不同单** (是否合并开单 spec 阶段定)。**档位终裁随 OpenSpec spec 的 rule6_note 成文** (skill-benchmark-exemption SOT §4 机制), DEC 只预告矩阵 — 不留临场判断。P2 扩展 issue-triage 模板族 = 对既有 skill 的逻辑修改, **同样触发 Rule #6**, 成本已预告。**执行轨声明 (v3, SOT §2 附加条款)**: issue-groomer 是必然 description_changed=yes 的新 skill — 按 SOT 自主运行时条款, unattended (Layer 2 自主轨) 下禁新增 skill/description 变动, **本项目立项/实施显式走 interactive 轨** (owner 主导会话), 不得派发 Layer 2 自主执行 (除非 owner 显式修订 SOT)。

**裁定-12 下游**: spec-drafter 起 OpenSpec (proposal 引用本 DEC 裁定-1~13); 上述两条套件缺口 issue; P1 零底座依赖即可开工。

## 理由

1. 需求真实且量化 (378 条/18 仓; 今日手工成本与价值构成直接证据);
2. 空位明确且不与既有能力重叠 (issue-triage 单条 / Phase 1.13 快照面 / fleet 跨项目健康度 — 三者边界 R1 审计核验);
3. 多 harness 约束经两层契约 + 脚本核设计获得诚实满足 (可移植面显式声明, 不夸大语义层保证);
4. 增量设计含上下文指纹 + provenance 指纹 + 评论流指纹的完整翻转源集合 (R1 修订), 未变复用不会静默侵蚀契约诚实性。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 分类语义主观 / 两层混淆 | 两层分字段 + provenance + 逐信号 confidence; Tier A 不声称语义; 命名消歧表 |
| 多终端并发梳理冲突 | 状态文件原子写; advisory 哲学 (与 Layer L 一致) |
| Rule #6 测试面 | 裁定-11 完整矩阵 + 两条缺口 issue 行动项 + 10 态 fixture 矩阵钉为 spec 验收面 |
| 增量机制侵蚀契约诚实性 (跨 harness 复用 / 漏翻转源) | 裁定-9 三面指纹 + provenance 复用规则 + 10 态 SC 必测 (R1 三 major + R2/R3 comments 分量的直接对策) |
| 标签 taxonomy 漂移 | labels.yaml 为 SOT + groom.py 运行时一致性自检 |
| 与 fleet 未来重叠 | 裁定-2 项目内作用域 + 脚本核被 fleet 复用显式预留; DEC-20261018-002 底座评估轨同日立项 (与本轨解耦) |

## 修订记录

| 版本 | 日期 | 内容 |
|---|---|---|
| v1 | 2026-10-18 | owner brainstorm 五段确认后初稿 |
| v2 | 2026-10-18 | post_brainstorm R1 (TL 0C/3M/3m · QA 0C/3M/5m · KM 0C/1M/7m) REVISE → 轮间修订: +裁定-13 ops-tier 可及性; 裁定-9 重写 (三面指纹/复用规则/diff 语义/8 态 fixture); 裁定-11 完整 Rule#6 矩阵+两缺口行动项; #110 精确化 + #180 核验补记; 外部源补标; 命名消歧表; 裁定编号化; labels.yaml 落点标注待裁; DEC-002 表格修复 |
| v3 | 2026-10-18 | R2 (TL 0C/0M/4m · QA 0C/1M/2m · KM 0C/1M/2m) REVISE → 修补: 快照名实修正 (补落盘全量 378/18 仓快照, 双快照括注); fixture 矩阵 8→10 态 (+内容面正向反事实态 /+关闭重开态) + 第 11 态候选 (last-writer-wins, #180 另一半教训); 上下文面 hash 输入集穷举 (changes/ 全树 + archive 显式排除 + taxonomy hash 入面); issue 面显式排除声明 (assignee/milestone/due_date); provenance 取值源标注待裁; 外部数字对源修正 (Augmentcode 实测口径 5-10%/30-40%, 45% 降级为转引不进 spec); 裁定-13 落点待裁+双源同步义务; 裁定-11 +执行轨声明 (interactive, SOT §2) |
| v4 | 2026-10-18 | R3 (TL 0M/3m · QA 1M/1m · KM 0M/2m) → 修补: ⑩ 态扩 comments 分量 (label/title/body/comments 任一⇒必判变); 补落盘 body/comments 端点形态语料样本 (5 issue/6 comment); 风险表两处 8 态→10 态同步; 删 v3 编辑残留的重复原子写行 |
