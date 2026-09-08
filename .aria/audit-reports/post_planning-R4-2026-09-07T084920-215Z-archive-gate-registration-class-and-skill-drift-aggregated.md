---
checkpoint: post_planning
round: 4
mode: convergence
verdict: PASS_WITH_WARNINGS
converged: false
scope_ok: true
counts: 0C/1M/0m (三席原始 1 条; 两席零 finding)
clusters: 0C
teams: [aria:code-reviewer, aria:backend-architect, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T08:49:20.216Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/tasks.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 4
---

# post_planning R4 — archive-gate-registration-class-and-skill-drift

## 逐席 verdict — **首次 0 Critical**

| 席 | verdict | findings | 结论 |
|---|---|---|---|
| aria:code-reviewer (R3 修订核验 + 「fix 造 fix」追问) | PASS_WITH_WARNINGS | 1M | 5/5 落地; 「可以进 Phase B」 |
| aria:backend-architect (Phase B 阻塞性) | **PASS** | **0** | 「tasks.md 现在可以进 Phase B 开工」 |
| aria:knowledge-manager (Rule #10 终检) | **PASS** | 0 | 全文 11 处豁免类措辞逐条判读, **未发现跳过本该阻塞的判定** |

## 唯一的 Major — 又是半修 ( 第六次)

R3 拆 E-6 时**只改了 tasks 一侧**: proposal 「机械兜底须全绿」六件套与 SC-9 「六个版本类 custom check 全绿」原封未动, 而 tasks E-6b 逐字写「**不得把它算进「全绿」**」。
⇒ 执笔者走到 E-6 时面对一条自相矛盾的验收, 只剩「把红的算成绿」或「卡死」两条路 —— 正是本 Spec 要治的病。

**已订正**: proposal 两处同步拆成「五个仓内 check 须全绿 + `plugin-cache-currency` 期望 STALE 并贴实跑输出」; SC-9 的版本串数字同步为 **21 处 / 12 文件**。

## R4 GOV 席对主控派的判断题给出的答案 (值得记录)

主控问: 「E-6b 那个必红的闸门, 『如实登记 + handoff 点名』算不算合法处置? 还是仍需 owner 先裁?」

GOV 席的判断 (主控采纳):
- **不严格落入 `configured-gate-authority.md` 白名单四类** —— 不是「结构性前提不成立」(该类要求「审的对象整个未产生」, 而两个比较对象都存在、检查也真实产出准确的 STALE 结果); 也不是「config 显式 off」(它是 `severity: warning` 启用态)。
- **更贴近 memory `session-level-precondition`** (会话内补不上的执行条件), 而非规则豁免。
- **关键区分 (主控自己没画出来的)**: `plugin-cache-currency` 测的是**本会话本地插件缓存的新鲜度**, 与本 Spec 代码变更本身的正确性**无关** —— 拿它阻塞 C.2 **不会多防住任何真实缺陷**。而 SC-11 直接关系「代码有没有被 AB 充分验证」, 性质不同。⇒ 只有后者该阻塞。
- ⇒ 如实登记是合法处置, tasks 未把它设计成阻塞项**是合理选择, 不是自行豁免**。

## 三条「fix 造 fix」追问 — 全部实测清白

- 拆 E-6 后**无任务/验收引用旧编号**; 操作边界三处表述 (主句 E-7a / 脚注 E-7a / 逃生舱 E-6c) 同向, 不构成第二个边界。
- E-6b 在逃生舱路径上**可完成** —— 它的验收是「贴 STALE 实跑输出证明红的原因」而非「让它绿」。
- E-5 数字全文**无残留旧值「22」**。

## 顺带复验干净的

67 个 checkbox / ID 零重复零缺口 / TG-B「18 条」与实际 18 个定义行相符 (**R2 F-1 的静默丢失形状未复发**) / tasks 引用的 20 处承重行号**逐条实读全部对得上** / SC-1 基线区段外仍 15 / 五个仓内 check + plugin-cache-currency 基线 6/6 全绿。

BLOCK 席另外自查并**用脚本实跑证伪**了两个疑点: (a) proposal SC-9 与 tasks E-6b 的措辞冲突 (即上面那条 Major, 独立发现); (b) C-8 行的 `#201`/`#185`/`#186` 会不会让 D-V2 恒红 —— 实测因整体被反引号包住而被判据 (b) 豁免, **不会**。

## 主控在 R4 期间自查并落地的设计改动 (审计席不可能发现 —— 脚本还没落盘)

**PP-4: C-1 落盘后 SKIP 态会变成不可达。**

实测 `aria/skills/state-scanner/scripts/<probe>.py` 的 `Path(__file__).resolve().parents[3]` == 插件根, 两个目标文件从那儿必然可达。⇒ 该换成 `parents[3]` (更稳, 不依赖 env, 对 marketplace 安装的采用方同样正确)。

**但那会让「插件源码不可见 → SKIP」永不触发** —— 保留它就得用 `CLAUDE_PLUGIN_ROOT=/nonexistent` 人为构造生产中不可能的场景 = **测量剧场**。判据同 memory `false_green_dual_is_permanent_red`「该信号在健康常态下应是什么值」: 健康常态下永不出现的态, **不该是一个态**。

**处置**: 五态改**四态**, 目标文件缺失直接 FAIL (插件损坏是真异常, 不是「不适用」)。proposal Part C1 + SC-5 与 tasks C-1 + C-3 同步改。

**改完先测再写**: 在 scratchpad 造同构插件树实跑四态 —— 基线 FAIL rc1 / 目标 PASS rc0 / 坏实现「两侧同改回 Step2」FAIL rc1 / 目标文件缺失 FAIL rc1, 全部符合; `parents[3]` 解析正确; 仓内零写入。

## 收敛趋势

| 轮 | Critical | Major | 性质 |
|---|---|---|---|
| R1 | 1 | ~20 | 转写丢承重限定词 + 顺序/时点 |
| R2 | 2 | 3 | 两条 Critical 全是 R1 修订引入 |
| R3 | 1 | 2 | 三条 finding **全部**是 R1/R2 修订引入 |
| **R4** | **0** | **1** | 唯一一条仍是 R3 修订的另一半 (只改 tasks 未改 proposal) |

**首次 0 Critical, 两席 PASS。** 按 Rule #10 `max_rounds=5` 未用满、全票 PASS 未达成 ⇒ **R5 照开**。
