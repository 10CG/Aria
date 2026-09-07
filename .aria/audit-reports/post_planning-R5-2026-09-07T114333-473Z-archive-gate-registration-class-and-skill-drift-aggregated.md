---
checkpoint: post_planning
round: 5
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 2C/12M/9m (五席原始 26 → 去重 16 → 反驳后存活 15; 另完备性批评席 6 条含 1C; 另主控 2 条)
clusters: 2C
teams: [aria:tech-lead, aria:qa-engineer, aria:backend-architect, aria:code-reviewer, aria:knowledge-manager, aria:context-manager(完备性批评)]
sibling_probe: **found_2** — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195) + pre-merge-completeness-gate-change-scope (10CG/Aria#199)
timestamp: 2026-09-07T11:43:33.474Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/tasks.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 5
---

# post_planning R5 — archive-gate-registration-class-and-skill-drift

## 结论: **FAIL, converged=false, `max_rounds=5` 用满**

R4 是 0C/1M、两席 PASS。R5 换上两席从未看过本 Spec 的新眼睛 + 一个全新镜头, 结果 **三席 FAIL**, 缺陷数**反向暴涨**。

⇒ **R4 的「收敛」是陈旧眼睛的产物, 不是真收敛。** 这正是 memory `stop-adding-rounds` 的判据:「加轮判据是 major 数是否还在降… **换新鲜眼睛 > 加轮**」。

| 轮 | Critical | Major | 席位 |
|---|---|---|---|
| R1 | 1 | ~20 | 4 席 |
| R2 | 2 | 3 | — |
| R3 | 1 | 2 | — |
| R4 | **0** | **1** | 3 席 (全是看过前几轮的) |
| **R5** | **2** | **12** | **5 席 + 完备性批评席, 其中 3 席全新** |

## 逐席

| 席 | verdict | findings |
|---|---|---|
| aria:tech-lead (实现者试派生, **新鲜眼睛**) | **FAIL** | 9 |
| aria:qa-engineer (验收可证伪性, **新鲜眼睛**) | PASS_WITH_WARNINGS | 3 |
| aria:backend-architect (PP-4 四态专审) | **FAIL** | 3 |
| aria:code-reviewer (R4 修订面 + fix 造 fix) | **FAIL** | 6 |
| aria:knowledge-manager (Rule #10 / #6 终检) | PASS_WITH_WARNINGS | 5 |
| aria:context-manager (**完备性批评**) | `ready_for_phase_b: **false**` | 6 (含 1C) |

26 条原始 → 16 条去重 → 逐条反驳 (Critical 3 票 / Major 1 票) → **存活 15, 证伪 1**。

## 两条 Critical

### C1 — C-3 的 `CLAUDE_PLUGIN_ROOT` 是惰性指令 (4 席独立命中, 反驳 0/3)

C-1 明令探针用 `parents[3]` 且「不用 `CLAUDE_PLUGIN_ROOT`」, 而同文件 2 行之后的 C-3 要求「其余四态用 `CLAUDE_PLUGIN_ROOT` 指向 scratchpad 夹具」。反驳席自己按 C-1 逐字实现探针后重跑: **设与不设 env 的 ROOT / 锚点数 / 输出 / rc 逐字节相同**, 夹具从未被读到。

后果三选一, 没有一条能产出 SC-5 要求的可证伪留证: (a) 目标态当场 FAIL 卡住; (b) 「锚点数≠1」与「坏实现」两态**恰好返回期望的 rc ⇒ 假绿**; (c) 执笔者发现 env 无效后, 唯一看得见的路径是**直接改仓内 `spec_complete.py`** —— 而它是本 Spec 明文非目标, 已知风险 5 正在预警这个动作。

**这是我 R4 期间 PP-4 改动的半修**: 我把设计改成 `parents[3]` 并同步了 proposal Part C1 / SC-5 / tasks C-1 / C-3 的态表, 却**把 `:25` 与 `:81` 的 env 跑法留在原地**; 正确跑法 (同构插件树) 我在 R4 报告里写过, **从没写进任何 Spec 文件** —— 反驳席实测 `grep -c '同构插件树'` 在两份 Spec 里**均为 0**。

### C2 — TG-B 内部不是 disjoint, 12 条任务互相移动对方的绝对行号 (完备性批评席)

tasks 逐字写「其余 TG-B / TG-C 任务文件域 disjoint, 可并行」。实测 **12 条 B 任务用绝对行号打同一个 `openspec-archive/SKILL.md`** (`:4 :17 :40 :47 :56 :87 :247 :251 :259 :318 :588 :607`)。

**照字面执行会坏, 主控独立复算确认**: `:251-257` 是 7 行, B-8a 换成 3 行 ⇒ 下方上移 4 行 ⇒ 原 `:263-265` 的 **Step 6** 恰落到 `:259-261`, 而 B-8b 正按绝对 `:259-261` 下手 ⇒ **删掉的是 Step 6, 真正的 Step 5 原封不动**。

**批评席的元判断值得记**: proposal 自己在「Part B 自身会移动行号」处早就知道这件事, 但该洞见被 R1 用来修 B-V3、R3 用来修 SC-1 区段、R5 用来修 B-V7 —— **三轮都只修被审的那一个实例, 从没回头看 B 任务本身**。`fix-the-class` 本 cycle 第七次。

## 主控在 R5 期间自行补做、五席结构上看不见的一条 Critical

R5 全部席位审的是**本地树**, 而 `origin/master` 上有**两份同期 Level 2 Spec** —— 它们与本轨共享整个发版面, 且**互相看得见、都看不见本轨**。

- 本轨 E-4 逐字写「版本 bump → `1.72.0`」
- `10CG/Aria#195` 的 `proposal.md:352` 正推荐给自己「MINOR / `v1.72.0`」
- `10CG/Aria#199` 在 `:315` 枚举并发轨时写「真正在飞的是 Aria#195」—— **没有本轨**

代码落点三方零交叠, 碰撞全在发版面 ⇒ git 不报冲突 (memory `same-value-merge-silent` 已有四处静默合成已发布号的实证)。同型事故就发生在本 Spec 起草**前一天**, 本仓 handoff 开篇第一句即「本 session 最该记住的一件事: 两个容器并行发版会撞版本号」, 代价记作「他们的 5 文件 + 同步面全部重做」。

⇒ **R4 报告里 `sibling_probe: no_sibling_found` 是错的**, 因为我只扫了本地树。本轮更正为 `found_2`。印证 memory `combined-mode-sister-spec-audit-value`「single-Spec 漏率 100%」。

## 被反驳席证伪的 1 条

`proposal.md:98` 「删 SKIP 的论据从未被真实『文件缺失』场景验证过」—— 反驳席指出提出者跑的**不是**四态表所测的那个探针, 而是他自己手写的 15 行稻草人; 原型脚本带显式 missing-file 守卫, 在真「文件不存在」的同构树上重跑得 `FAIL 目标文件缺失 (插件损坏?)` / rc 1, 是受控 FAIL。**证伪成立**。

## 处置 — 23 条全部落地

五席 15 条 + 批评席 6 条 + 主控 2 条 (并发轨撞号 Critical / `rc 2` vs `rc 1` 三方不符), 共 **23 条已逐条改进 Spec**, 落 29 处编辑。类级 sweep 而非逐实例:

- **C-3 环境变量类**: `:25` / `:81` 换成同构插件树跑法 + 仓内只读护栏; 「其余四态」→「其余三态」; C-V4「五态」→「四态」; proposal Rule #6 表「SC-5 (C1 五态)」→「四态」
- **TG-B 寻址类**: 更正 disjoint 声明 + 强制护栏「每条落盘前 `sed -n '<N>p'` 逐字核对该行内容, 不符即停」(与执行顺序无关, 是唯一对移位免疫的判据) + 推荐自下而上执行序
- **裸 issue 引用类 (第四次复发)**: 探针判据从**单字符前瞻**换成 **fail-CLOSED 全限定匹配 + 封闭白名单** —— 原判据对半限定的 `Aria#195` 与反引号裹的裸号双双 fail-OPEN (memory `invariant-needs-failclosed-default`); 改后两份 Spec rc 0, 负控仍抓得到
- **验收维度不匹配类**: C-V3「status 非 `error`」→「`status == "pass"`」(实读 `custom_checks.py:379` 确认 rc 非零一律映射 `fail`, 原判据把红当绿); B-V7 三条断言改按内容不按行号; 新增 B-V9 (B-13 此前**零验收覆盖**)
- **我自己前一次修订引入的**: E-4 腿 (b) 正向枚举 fail-OPEN → 改全量普查 + 两条已知轨作自检基线; 腿 (c) 实测**恒空** → 改全 handoff 面扫描 + 零命中须显式登记; SC-9 的 21/12 常量 → 程序性判据; `<vNEXT>` 替换范围歧义 → 区分 Spec 内占位符与交付物字符串

## 为什么 max_rounds 用满仍不宣告收敛

按 memory `marginal-return-negative` 的拐点判据 (「本轮 fix 引入的 major 占比 > 1/2」): R5 的 15 条存活里, 我前两次修订引入的是 **5 条 ≈ 1/3**, **未过拐点** —— 另外 10 条是四轮陈旧眼睛从没看见的既有缺陷。**边际产出仍为正, 因为变的是 finding 来源 (新眼睛 + 新镜头), 不是轮数。**

但 `max_rounds=5` 是 owner 的配置决定。按 Rule #10, 我**既不自行宣告收敛, 也不自行加开 R6**。⇒ 如实记 `converged=false`, 经 handoff 上呈复议 (Rule #10 §5「AI 任何自作主张的流程判断必须写进 handoff 请复议」)。

批评席给的 `ready_for_phase_b: false` 判据是可证伪的:「只要 tasks 还用绝对行号 `:251-257`/`:259-261` 且中间没有按内容定位或固定顺序的指令, 这条就成立」。**本轮已补上按内容核对的强制护栏与执行序**, 该具体判据已消解; 但 `converged=false` 不因单条消解而改变。
