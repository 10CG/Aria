# rule6-4b-routing-should-not-sot-revision — 4b 单技能沙箱对「路由类 should-not」结构性失效的 SOT 修订

> **Level**: Analysis + Decision Request (Phase A 产物; 实施另立执行 spec)
> **Status**: Draft (2026-10-22) — **修订方向待 owner 裁定** (本轨只做分析, 不改 SOT)
> **Created**: 2026-10-22
> **Linked Issue**: `10CG/Aria#243` (同族: `10CG/Aria#214` 自主运行时 description 处理)
> **证据**: `aria-plugin-benchmarks/ab-results/2026-10-19-issue-groomer-rule6/RESULT.md` + 三轮 trigger 套件 (`ab-results/2026-10-19-issue-groomer-trigger/{real-v1-prefix,real-v2-broad,real}/`)

## 问题定性 (Phase A recon)

**结构性失效, 非套件质量问题**: 场景 4b 沙箱 = 项目根仅含被评合成技能 (`run_eval.py --setting-sources project`, 无用户插件) ⇒ 兄弟 skill (issue-triage / state-scanner) 不在场。issue-groomer description 已明写负面边界 (「不适用: 单条→issue-triage / 快照→state-scanner」) 且前移 (v1→v2), should-not 误触仍 9/10 — 含 #13 纯状态查询 (与 groomer 能力零交集): **唯一在场的技能承接一切路由, description 路由边界无从生效**。

对照有效基线 (openspec-archive 套件 2026-09-13): 其 should-not 有效系近邻为**能力外**任务 (changelog 成文 / 目录整理), 不依赖兄弟路由 — **两种 should-not 设计前提不同, 现行 SOT 未区分**:

| should-not 类型 | 语义 | 单技能沙箱可评? |
|----------------|------|----------------|
| **能力外** (out-of-capability) | 「这不是该 skill 做的事, 且没有别的 skill 接」 | ✅ 可评 (被评 skill 独立可拒) |
| **路由边界** (routing-boundary) | 「这是兄弟 skill 的活, 该让位」 | ❌ 结构性不可评 (兄弟不在场, 拒了也没人接) |

SOT 现文 (`standards/conventions/skill-benchmark-exemption.md` + `AB_TEST_OPERATIONS.md` §场景 4b) 对 should-not 只有一句「以近似误触为主」— 两类混同, 路由类在单技能沙箱里恒假阴性负载 (误触率虚高 ≠ description 差, = 沙箱缺位)。

## 修订方向 (二选一或合并, 待 owner 裁)

### 方向 A: 沙箱补位 (工程修) — 4b 沙箱含兄弟 skill 占位

- `run_eval.py` 增 `--sibling-placeholders <list>`: 项目根额外放置兄弟 skill 的合成 description (仅 frontmatter, 不含指令体), 使路由边界可评。
- 成本: runner 改动 + 每个被评 skill 的套件须声明兄弟名单 + 占位 description 的维护义务 (兄弟 description 变更须同步 — 新增一类双源同步)。
- 收益: 路由类 should-not 变为可证伪; 沙箱更接近真实路由环境。
- 风险: 占位 description 与真实兄弟 description 漂移 → 评的是「占位的路由性」非真实路由 (需 pinned snapshot 或 hash 校验); 合成占位本身的保真度是新变量。

### 方向 B: SOT 分类显式化 (语义修) — should-not 二分, 只对能力外设门

- SOT §场景 4b 增分类定义 (上表), 套件条目须标 `type: capability|routing`; 门判据只计 capability 类; routing 类移入**观察面** (报告但不判 fail)。
- 成本: 纯文档 + 套件 schema 一字段; 零 runner 改动。
- 收益: 立即消除恒假阴性负载; 诚实反映 4b 的地板守卫边界 (与 §92 既有边界注「只承诺已验证的两类破坏」精神一致)。
- 风险: 路由边界回归到「无门」状态 — 靠场景 1 (完整插件环境的 AB) 兜底? 场景 1 的 WITH/WITHOUT 臂都在完整插件环境, 兄弟在场, 路由可评 — **但场景 1 测的是指令变更影响, 不是 description 路由面**; description 变更的路由回归将无门 (承认盲区并显式记录, 优于假装有门)。

### 方向 C (合并): B 立即 + A 作为 P2 跟进

B 先落 (快, 消除假阴性), A 立 issue 作 runner 增强轨 (P2), A ship 后 routing 类恢复设门。

## 建议

**方向 C** (B 立即 + A P2 跟进)。理由: B 是零工程量的语义诚实化, 与 4b「地板守卫」的自我定位一致 (SOT §92 已注明其判据边界); A 的双源维护义务与占位保真风险需要独立 spec 论证, 不宜与紧急的语义修正捆绑。

## Owner 裁定项

1. 方向 A / B / C 取舍 (建议 C)。
2. 若 B/C: routing 类在 rule6_note 是否新增字段 (如 `scenario4b_routing: observed-only`)? (建议: 套件内标注 + 报告呈现, note 字段不动 — additive 最小)
3. 既有已 ship 套件 (openspec-archive 等) 是否回溯标注分类? (建议: 不回溯, 下次触碰该套件时标 — 避免全量返工)

## Impact (实施时, 属执行 spec)

- `standards/conventions/skill-benchmark-exemption.md` (SOT, standards 子模块) + `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b
- `ab-suite/trigger/*.json` schema (+type 字段, version.yaml 升版)
- 关联 #214 (自主运行时 description 处理) 的边界讨论一并引用
