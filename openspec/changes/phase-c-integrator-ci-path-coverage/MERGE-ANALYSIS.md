# 归并分析 — aria-plugin #122 双 Spec 碰撞

> ## ✅ 已裁决 (owner, 2026-07-30): **以 R 为准**
>
> owner 采纳 §5 推荐路线 —— R 为 Spec 基线 + 并入 L 的发现 + 用 L 的任务骨架重建 A.2/A.3。
>
> **执行状态**:
> - ✅ L 已标记 [SUPERSEDED](./proposal.md) (保留目录: 10 份审计报告是证据轨迹, 27 任务骨架待复用)
> - ✅ R 已并入 **3 条真缺口 + 1 条欠定** (R 的 §修订记录 A1)。⚠️ **与本文 §5 原推荐的差异**: 逐条核实后 **L-6 / L-7 未并入** —— R 已用别的方式解决同一问题 (独立 tempdir / paths-ignore 存在即 covered), 详见 A1「未并入」段。本文 §3/§5 写作时未做这层核实, 以 A1 为准。
> - ⏸️ **A.2/A.3 重建待 post_spec 闸门裁决** (A1 是实质 Spec 变更, Rule #10 不自行豁免; 见 R 文末「闸门待裁」)
> - ↗️ L-1 (catch-all fail-OPEN) 转独立 issue, 不阻塞
>
> **性质**: 本文原为 owner 裁决的**输入**; 裁决已作出, 现转为决策留痕。
> **产出时间**: 2026-07-27, 主仓 `92943ca` (rebase 后)
> **被比较的两份**:
> - **L (local)** = `openspec/changes/phase-c-integrator-ci-path-coverage/` — 本容器 `aria-runner-bot/023236f2`, 创建 2026-07-25
> - **R (remote)** = `openspec/changes/phase-c-gate-path-coverage-not-applicable/` — `simonfishgit`, 落地 2026-07-27 11:52 (`257a20d`)

## 0. 结论摘要

两份**不是同一设计的两种写法, 是两种架构**。核心分歧在「先查 CI 还是先判覆盖」, 由此派生出改不改 backend、状态模型几维、`compute_verdict` 怎么改三处连锁差异。

**因此「把 L 的 27 任务嫁接到 R 的 proposal 上」不是机械改名** —— 27 条里约 6 条要删、9 条要改写、10 条可复用、另需为 R 独有的 SC 新增任务。

## 1. 流程状态对比

| | L | R |
|---|---|---|
| Status | 📝 Draft (R4-fix), **`converged: false` + `overridden_by_user: true`** | ✅ **Approved + owner 签字**, R4 qa PASS 0/0/0 **真收敛** |
| post_spec | R1→R4 (5/5/3/2 席), critical 5→4→1→**1 (两席争议未决)** | R1→R4 (5/5/2/1 席), critical 4→1→0→**0** |
| post_planning | ✅ R1→R6 (2/3/2/2/2/2 席), critical 2→2→1→0→0→0, major 6→7 持平 (owner 裁定接受) | ❌ 未跑 |
| A.2/A.3 | ✅ `detailed-tasks.yaml` 27 任务 / 18 波 / 5 lane, TDD 9 对 RED/GREEN | ❌ 无任务文件 |
| 验收面 | AC-1~15 (含子标号约 30 条) | SC-1~28 |
| 规模 | proposal 551 行 + tasks 66KB | proposal 209 行 |

**流程账**: R 在 Spec 层是**干净的**(真收敛 + 已签字); L 在 Spec 层**欠账**(max_rounds 耗尽靠 owner override 收场, R4 还留一条 critical/major 定性争议), 但在**任务层**是唯一有产出的。

## 2. 三处架构分歧 (实质, 非文字)

### 分歧 1 — 评估时机: 「先查 CI」 vs 「先判覆盖」

- **L**: 改 `AetherBackend._normalize_pr_ci_status([])` 由 `"pending"` → `"not_found"`, **先查 CI**; 只有拿到零 run (`not_found`) 才进覆盖评估。
- **R**: **不改 backend** (D1, `CIStatus` Literal 不动)。评估插在 (a) PR CI 查询**之前**, 判 `not_applicable` 就**根本不查**。

**权衡**:
- R 更 additive (零破坏性面), 省一次 CI 查询。
- **L 在一个场景下更保守**: 路径无覆盖、但 CI 因 `workflow_dispatch` 手动触发**确实有 run 在跑**时 —— L 会看到 run (state=pending/failing) 而**不进评估**, 按真实 CI 状态判; R 会在查询前就 `not_applicable` 跳过, **看不见那个 run**。
- 代价方向相反: L 的改动**关不掉** (自述破坏性面第 2 项 —— `_normalize_pr_ci_status` 是 `@staticmethod`, 关掉 `path_coverage_aware` 也不能回滚; 直接消费 `ci_backends` 而不经 `gate_check` 的调用方仍见新值)。

### 分歧 2 — 状态模型: 二维 vs 一维三态

- **L**: `{covered: bool, confident: bool, ...}` 二维 + gate 侧**四重合取** (`¬covered ∧ confident ∧ workflows_seen≥1 ∧ changed_files_count≥1`)。
- **R**: `{decision: "covered"|"not_applicable"|"unknown", ...}` 一维三态 + **8 条互斥穷尽判定规则** + **reason 字面值封闭集** (7 个终态 reason)。

**可测性上 R 明显占优, 且 L 自己承认了**: L 的 AC-12 注记写着「单出口成立时后三项由 term 1 蕴含 ⇒ AC-11 恰恰保证它们永不是判定因素 ⇒ **删掉/写反/`.get()` 拿 None 全部测试仍绿**」—— 即四重合取里**三项冗余且不可证伪**。R 的封闭 reason 集则可与测试矩阵做满射核对 (SC-28 就是为补满射而加的)。

### 分歧 3 — `compute_verdict` 改法

- **L**: **极性反转 catch-all** — `elif pr_ci_status not in ("passing", "not_applicable"): verdict = WAIT`,把原来的 `else → GREEN` 兜底翻成 fail-CLOSED。
- **R**: **新增显式 `elif pr_ci_status == "not_applicable":` 分支** (BA-8), catch-all `else → GREEN` **保持不变**。

**这是 L 独有的实质安全收益**: L 的 AC-10 有实跑证据 —— `compute_verdict([], "not_found")` / `([], "wat")` / `([], "")` 在 v1.64.0 上**全返回 `green`**。R 的 proposal 全文未涉及这条 catch-all。

**公平记法**: R 不改 backend ⇒ `not_found` 不上岗 ⇒ 该 catch-all 对 R 而言**仍不可达**, 不是 R 新引入的缺陷。但它是**既有 latent fail-OPEN**, 值得独立修 (无论哪份为准)。

## 3. 各自独有的实质发现

### L 独有 (R 缺失, 值得移植)

| # | 发现 | 证据强度 |
|---|------|---------|
| L-1 | `compute_verdict` catch-all `else→GREEN` 的 fail-OPEN | **实跑 3/3** (`"not_found"`/`"wat"`/`""` 全 green) |
| L-2 | 列 0 `---` 的 YAML **文档起始标记** vs 多文档分隔语义 | R4 实跑: 朴素读法致该仓**任何变更恒 wait**, 且 AC-7b 不钉真值 ⇒ **零测试会红** = 静默失效 |
| L-3 | anchor 命中判据必须**位置式**不能子串式 | R4 实跑: 子串读法在 4 份真实语料**命中 3 份** (`- 'skills/issue-triage/**'` 等) ⇒ 恒 wait 复发 |
| L-4 | `git diff -z` 输出**含尾随 NUL**, 朴素 split 多出空元素 | R2 实测 |
| L-5 | AB 套件三处勘正: 裸名 `phase-c-integrator` 命中**无关 parent 套件** / `latest` symlink 解析到 **state-scanner** 归档 / `structural_metrics.measured` 是 **int** 非 str | R2 **5/5 席实地核实** |
| L-6 | `_match_coverage` 拆纯函数 — 否则 fixture 在 Aria 仓内会让 `git -C` **成功并返回 Aria 自己的 changed files**, 断言在错误输入上求值且失败模式不对称 | R2 3 席 |
| L-7 | `paths-ignore` 极性反转 (P5): 「匹配更多」⇒ `¬match` 更少 ⇒ **covered 更小** ⇒ 更容易 skip | R2 3 席 + 实跑证伪 |

### R 独有 (L 缺失)

| # | 发现 | 备注 |
|---|------|------|
| R-1 | **D10 / 规则 3**: changed_files 含 workflow 目录下任一文件 → **强制 covered** ("对 CI 配置动刀的 PR 永不 not_applicable") | R1 QA-1 Critical「workflow 自身变更反向假绿」。**L 全文无此规则** |
| R-2 | SC-21 NIE 交叉不变量: stub backend 的 `NotImplementedError` 经 (b) 照常 propagate, 不被 not_applicable 吞 | 直接对应 CLAUDE.md Rule #8 「stub backend 抛 NIE 时 gate 必须 abort」。**是 R 架构 (先评估后查) 自引入的风险, R 自己封住了**; L 架构 (先查后评估) 结构上不会有 —— 非 L 遗漏 |
| R-3 | SC-22 卫生断言: 既有 62 测试运行期间**零真实 git 子进程** | |
| R-4 | SC-19 gitlink-only bump **正证 fixture** (合成 paths 含 `aria` 精确 token → covered, 验证 gitlink 按不透明单段路径参与匹配不展开) | L 只有反证 |
| R-5 | SC-26 在主仓根对子模块分支名评估 → `unknown` (cwd 错仓的自然安全网) | |
| R-6 | **KM-5 先存档后改写**: 改 `_lane` 前先把 2026-07-25 owner 裁决全文抽 `docs/decisions/DEC-*` | L 的 TASK-025b 只改不存档 |
| R-7 | **TL-5 co-land 硬时序**: `_lane` 退役编辑必须与 gitlink bump **同一个主仓 commit** — 消除「规则已退、pinned 子模块无机制」的裸奔窗口 | L 无此约束 |
| R-8 | `--no-renames` 显式加 (rename 呈现为 delete+add, 保守保持 covered) | L 未提 rename 策略 |

## 4. 27 任务的嫁接成本 (若以 R 为准)

| 处置 | 任务 | 说明 |
|------|------|------|
| ❌ **删** (6) | TASK-001, 001b(spike), 002(owner 证否分支), 013, 014, 015, 016 | R 用 cwd 契约不透传 `repo_root` ⇒ spike 及其 owner 分支不需要; R 不改 backend ⇒ `not_found` 契约两任务整删 |
| ⚠️ **改写** (9) | TASK-005/006 (parser — L 规则更细, 可**升级** R), 007/008 (事件分类: L 封闭黑名单 vs R 精确白名单), 009/010 (聚合: 二维 units → 一维 8 规则, **改动最大**), 019/020 (接线: 四重合取 → decision 三态), 022 (文档同步 11 处 → R §6 逐处清单) | |
| ⚠️ **改方向** (2) | TASK-017/018 | L 是 catch-all 极性反转, R 是加 elif。**建议两者都做** (见 §5) |
| ✅ **可复用** (10) | TASK-003/004 (glob matcher), 011/012 (薄壳), 021 (全量回归), 023/024 (AB 套件 + Rule #6 — **L-5 三处勘正是净资产**), 025a (发版), 025b (CLAUDE.md/_lane — 需并入 R-6/R-7) | |
| ➕ **新增** | R 独有 SC-16/18/19/21/22/23/24/25/26/27/28 对应任务 | 尤其 R-1 (D10) 和 R-2 (NIE 不变量) |

粗估: 27 → 约 22-25 条, 其中约 11 条需实质改写。**TDD 9 对 RED/GREEN 的配对结构可保留**(那是 post_planning 6 轮打磨的成果, 与具体状态模型无关)。

## 5. 给 owner 的裁决选项

**推荐: 以 R 为 Spec 基线, 把 L 的 §3 全部 7 条发现作为修订并入, 用 L 的任务骨架重建 A.2/A.3。**

理由:
1. **流程账干净**: R 真收敛 + 已签字; L 靠 override 收场且 R4 争议未决。以 L 为准等于把一份未收敛的 Spec 推进 Phase B。
2. **可测性**: R 的封闭 reason 集 + 8 条互斥穷尽规则可满射核对; L 的四重合取有三项**自认不可证伪**。
3. **风险面**: L 改 backend 且**关不掉**; R 纯 additive。
4. L 的价值主要在 **§3 的 7 条实跑发现 + 27 任务骨架**, 两者都可移植到 R 上 —— 而 R 的流程正当性无法移植到 L 上。

**必须并入的最低集** (否则 R 会带着 L 已证实的坑上线): L-2 (`---` 语义) / L-3 (位置式 anchor) / L-4 (`-z` 尾随 NUL) / L-5 (AB 套件三处勘正)。这四条都有实跑证据且 R 的 SC 集合结构上抓不到。

**独立建议 (与裁决正交)**: L-1 的 catch-all fail-OPEN 是既有 latent 缺陷 (`compute_verdict([], "wat") → green`), 建议**无论哪份为准都单独修**, 可作为独立小 PR 先落。

### 备选

- **B. 以 L 为准** — 代价: 需补跑 post_spec 至真收敛 (R4 争议未决), 且要接受 backend 改动关不掉的破坏性面。收益: 27 任务零改写。
- **C. 两份都作废, 用两轮审计的合集重写第三份** — 代价最高, 收益是拿到两边全部 20 条发现的干净基线。**不推荐** (两份 Spec 各自 4 轮审计的沉没成本, 且 R 已签字)。

## 6. 方法论留痕 (Rule #10 请复议)

本次碰撞是 `feedback_concurrent_duplicate_audit_fetch_before_start` 的**第四次实证**, 且这次的形态最贵: **两份各跑 4 轮 post_spec, 合计 10 轮 / 33+ agent 实例, 没有任何一轮的入口断言包含「远端是否已出现同 issue 的竞品 Spec」**。

⇒ 闸门审的是**产物质量**, 不审**产物是否该存在**。建议在 `audit-engine` 的 post_spec 入口断言里加一条机械检查: 对 spec 的 `关联 Issue` 字段, fetch 后 grep `openspec/changes/*/proposal.md` 是否已有同 issue 引用。此建议属流程变更, **须 owner 裁, 本文只提出不实施**。
