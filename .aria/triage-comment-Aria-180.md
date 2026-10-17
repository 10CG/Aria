本评论是按 owner 2026-09-30 决策单第 6 项 (10CG/Aria 仓 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`, issue 卫生清扫) 做的 triage 核验。该项把本单与 10CG/aria-plugin#107 记为重复, 并要求先核验再评论 / 关闭; 核验结论: 两单同根因但范围不同, 本单不是重复, 保持 open, 作为症状级总单。10CG/aria-plugin#107 跟踪心跳接线 (相当于本单修法 (b) 的挂载点), 本单跟踪症状本身 (对方心跳停摆超过 30 分钟后, 同名通道的 advisory 碰撞面静默) 以及修法 (a) / (c); 10CG/aria-plugin#107 的 to-do 全部完成也不等于本单症状已解。关闭不等于已修: 在 aria-plugin v1.74.1 上症状仍完整复现 (见 case-1 / case-2 / case-9)。

## Triage Report

**Verdict**: `partial-repro` | **Severity**: `major` | **Recommended Action**: `next-cycle`

> 保持 open, 不关闭 (Recommended Action 表示排期, 不表示关闭)。关联 issue: 10CG/aria-plugin#107 (心跳接线) / 10CG/aria-plugin#168 (审计轮内不刷心跳) / 10CG/aria-plugin#202 (同容器换 session 重复认领); 三单都已在各自正文或评论里引用本单。

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.65.5` (正文另注 `1.63.0` 亦同; collector 把两个版本粘成了 `1.65.5（1.63.0`) |
| Current | `1.74.1` (10CG/aria-plugin 仓 master `268da8f`; origin / github 两端均为该 SHA, `git ls-remote` 实测) |
| Gap | behind (minor 号 1.65 → 1.74) |

issue 所述在 v1.65.5 (`af87cae`, 该提交处 `plugin.json` 为 1.65.5) 上核对属实: `heartbeat()` 定义在 `claim_lifecycle.py:178`, 非测试代码里没有调用 (只剩 def / 注释 / docstring), `constants.py:43` 自陈「NO production heartbeat loop exists」。此后心跳的生产路径已在 v1.71.0 落地 (见 Git History), 但这只让根因 1 / 4 部分失效, 症状没有消失。

### Code Path

路径约定: 下文以 `lib/` / `scripts/` / `references/` / `tests/` / `SKILL.md` 开头的路径, 均为 10CG/aria-plugin 仓 `skills/state-scanner/` 目录内的相对路径 (在 10CG/Aria 主仓里对应 `aria/skills/state-scanner/`); 以 `openspec/` / `docs/` / `.aria/` 开头的属 10CG/Aria 主仓。

collector 对 issue 的三处引用都报 `file not found` (相对仓根解析不到, 文件实际在上述目录内; 同一类 monorepo 布局下的路径解析问题另见 10CG/Aria#200, 那张在版本发现一侧)。已手工对照 v1.74.1:

- `lib/claim_lifecycle.py:178` `heartbeat()`: 现为 `:179`。docstring 里关于必须传入 acquire 时那个 Identity 实例的说明 (原 `:196-205` 一带) 现为 `:202-206`, 文字未变; `get_identity()` 仍每次生成新 session_id (`lib/identity.py:353`)。
- `lib/constants.py:40-50`: 现为 `:38-58`。注释已改写 (`:43-45` 写明历史上没有生产心跳的前提已不成立), 但 `STALE_TTL = 1800` (`:36`) 与 `SWEEP_TTL` 24h (`:58`) 都没变, 且 `:48-57` 明写 SWEEP_TTL 不因入口心跳而放宽 (不再进入 scanner 的会话就不再刷新), 并把「心跳变成定时器而非入口钩子」列为重新评估 24h 的前提。
- `lib/reconcile.py:154-163` `_is_stale()`: 仍是 `return age_seconds > STALE_TTL`, 未变。它被 Rule 6 (`:255` / `:328`, stale 的 winner 移入 superseded, 即对 reconcile 而言可接管、不再计入竞争者) 与 Rule 5.1 (`:283`, 只取新鲜候选做 clock-skew 判定) 共用。
- 闸门一侧: `scripts/phase1_gate.py:791-793` 的 7d 分支仍写「No prompt needed: stale / terminal tracks are safe to acquire」; `AdvisorySurface.kind` 只有 `occupied` / `clock_skew` / `push_failed` (`:187-191`)。
- 文档与实现不符 (未见 issue 跟踪): `references/layer-l-integration.md:35` 仍写「heartbeat 周期设置 (10min, 由 phase-b-developer mid-cycle 调用)」, 而 phase-b-developer 的 `SKILL.md` 里没有任何 heartbeat / 心跳字样, 同文件 `:46` 已改写为「每次调用 (非定时器)」。`:35` 会让读者以为长任务有 10 分钟周期心跳, 宜随修法 (b) 一并订正。

### Git History

collector 的 `likely_fix_candidates` 为空 (Step 4 因路径未解析而 skipped)。手工 `git log -S` 找到心跳生产路径的三个提交; 三者都是 10CG/aria-plugin 仓 master 的祖先 (`git merge-base --is-ancestor` 对 `268da8f` 成立, origin / github 两端 master 均为 `268da8f`), 随 `v1.71.0` (`985e629`, 2026-09-06; 该 tag 两端都在) 发布:

| SHA | 日期 | 内容 |
|-----|------|------|
| `0ae207f` | 2026-09-05 | `heartbeat_by_track()`: 按 (container, 归一 track_id) 刷全部 active claim, 与 session 无关 |
| `9c00aa5` | 2026-09-05 | `phase1_gate.py --heartbeat-only` 模式 (生产调用点 `scripts/phase1_gate.py:1160`) |
| `ab3dbd0` | 2026-09-05 | state-scanner `SKILL.md`「Layer L A.1 heartbeat 集成」段 (每次 `/state-scanner` 入口触发) |

来源是 10CG/Aria 主仓的归档 Spec `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/` (立项 issue 为 10CG/Aria#174)。该 Spec 的 `proposal.md` 对本单这样处理:

- `:266` 是 owner 2026-08-22 的裁定原文 (当时为 (ii)+(iii) 组合), 称该裁定把本单的「heartbeat 零调用」一并解; `:293` 是同一句在 2026-08-23 落版小节里的复述。
- `:295` / `:308` 记载 owner 2026-08-23 撤销 (iii): `STALE_TTL` 维持 30 分钟不改 (`:651` 的 SC-20 随之撤销, `:687` 再次写明「不改 STALE_TTL」)。
- `:197` / `:251` / `:538` 直接用本单的编号指代同名通道因心跳停摆加 30 分钟 `STALE_TTL` 而静默这一现象; `:340` 把「同名通道 (7c) 只在 30min 内有效」与「主检测责任由 overlap 通道承担」写成成文残余风险, 并写明该 Spec 不再对这一权衡提出断言。
- 也就是说, 该 Spec 只解了 heartbeat 零调用这一项, 没有解本单的症状; 归档时本单也没有被关闭。

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (10CG/Aria 与 10CG/aria-plugin 两仓开放 PR 均为 0, forgejo API 实查) |
| Local branches | none |
| Worktrees | 仅主工作树 |

10CG/Aria 仓的 `openspec/changes/` 下没有以本单为锚的在制 Spec。

### Reproduction

**Mode**: `auto` | **Hit rate**: `5/9` (复现 = 该缺陷/缺口仍在)

实验均在隔离副本里完成 (10CG/aria-plugin 仓 `268da8f` 的副本 + 临时 git 仓 + 本地 bare origin + 独立 HOME; 多数为真实 CLI, 少数为库调用或静态核对, 见各 case), 未触碰真仓与生产协调 ref。triage 与独立复核各自复现, 本单症状都在心跳年龄超过 30 分钟时出现; 终稿前又直接调用 `reconcile()` 纯函数 (内存构造 claim, 不落盘) 复核分界: 心跳年龄 29 / 30 分钟仍有 winner, 31 分钟起 winner 为空, `reason=sole_active+stale_takeover_eligible`。相关既有测试在隔离副本里复跑全绿 (`test_heartbeat_by_track` 12 · `test_heartbeat_only_cli` 7 · `test_release_by_track` 53 · `test_phase1_gate_advisory` 13 · `test_reconcile_golden_table` 58 · `test_coordination_default_lockin` 26)。

- case-1 (复现): issue 复现步骤 1-3, 真 CLI —— A 认领后心跳停在 35 分钟前, 之后无任何心跳; B (另一容器) 跑 `phase1_gate.py --mode advisory`: `outcome=passed` / `competing_winner=null` / `surface=null`, 与 issue 的「实际行为」逐字一致。对照组 (A 闲置 5 分钟) 得 `outcome=advisory_proceed` + `surface.kind=occupied`。
- case-2 (复现): 库调用 `run_gate(mode=advisory)`, 扫描 A 的闲置时长: 1 / 10 / 29 分钟 → `occupied`; 31 / 120 / 1439 / 1500 分钟 → `passed` / `competing_winner=null` / `surface=null` (reconcile Rule 6 把 A 判为 stale-takeover-eligible, 闸门走 7d 直接放行), 分界恰在 `STALE_TTL=1800s`。1500 分钟已超过 24h 的 `SWEEP_TTL`, 但没有人跑过 `--sweep-stale`, claim 仍是 active。
- case-3 (未复现): 同容器的全新 session 经真 CLI `phase1_gate.py --heartbeat-only` 刷新 A 的 claim (`outcome=refreshed`, 心跳 120 → 0 分钟, claim 数仍为 1) 后, B 收到 `occupied`。issue 根因 1 所说 `heartbeat_at`「永久冻结在 acquire 时刻」, 对走入口刷新的容器在 v1.74.1 上不再成立。
- case-4 (复现): 接 case-3, 刷新之后再过 31 分钟、期间没有再次 `/state-scanner` 入口, B 再跑 advisory 闸门: `outcome=passed` / `surface=null` (A 的心跳年龄 31.0 分钟)。保护只延续到下一次入口刷新为止, 之后静默复现 (独立复核同结论): 心跳是入口钩子, 不是定时器。
- case-5 (未复现): 根因 4。一条 26 小时前的 active claim, 由同容器的全新 session 分别调 `heartbeat()` 与 `heartbeat_by_track()`: 前者 `success=false` / `claim_not_found` (旧函数行为未变, 且在 state-scanner 的 `lib/` 与 `scripts/` 的全部历史里都没有过生产调用方, `git log -G` 实测), 后者 `success=true`、claim 数仍为 1、心跳年龄 1560 → 0 分钟 —— 该障碍已被 by-track 变体绕开 (`lib/claim_lifecycle.py:475-579`, docstring 写明 `session_id` 在此无关)。
- case-6 (未复现): 根因 1 静态核对。v1.65.5 零调用属实; v1.74.1 多出 1 处真实调用 `scripts/phase1_gate.py:1160` (`heartbeat_by_track`), `heartbeat()` 本身仍零调用。
- case-7 (复现): 修法 (c) 未实现: 7d 分支仍写「No prompt needed」, `AdvisorySurface.kind` 只有 occupied / clock_skew / push_failed, CLI 输出里没有任何 stale 相关字段。
- case-8 (未复现): A.1 形态 track-id (含容器段, 两容器不同) + 同一 `--linked-issue`, A 闲置 48 小时: 同名通道静默, 但不做新鲜度过滤的 `linked_issue_overlap` 命中对方的 48 小时前 claim (`lib/collision.py` 的 `linked_issue_overlaps()`, `:365-440`)。前提是双方 claim 都带同一 `linked_issue` (该 flag 可选); 对方 claim 未带时, 即使 B 带了也是 `linked_issue_overlap=[]`, 双通道皆静默 (独立复核实测)。
- case-9 (复现): 同一 track-id (无容器段) + 同一 `--linked-issue`, A 闲置 48 小时: `passed` / `surface=null` / `linked_issue_overlap=[]` —— 同 track-id 被 overlap 通道显式排除 (`lib/collision.py:426-427`「same-name collision — reconcile's job」), 而 reconcile 已判 stale, 双通道皆静默; 对照组 (A 闲置约 5 分钟) 得 `occupied`。即 issue 所述缺陷在「同名 track-id」路径上仍完整存在。

**Deviation note**: issue 所述症状 (30 分钟后 collision surface 静默) 在 v1.74.1 上完整复现 (case-1 / 2 / 9 与 issue 的「实际行为」逐字一致), 但 issue 写的根因与现状实质偏离: 根因 1 (heartbeat 零生产调用点、`heartbeat_at` 永久冻结) 已因 v1.71.0 的入口心跳部分失效 (case-3 / 6), 根因 4 (须同一个 Identity 实例) 已被 `heartbeat_by_track` 绕开 (case-5); 9 个 case 中 5 个复现、4 个不复现。残余窗口的机制是「心跳是入口钩子而不是定时器」(case-4), 与 issue 的「零生产调用点」「永久冻结」不同, 修复不应按原根因设计。

### 子项状态

| 子项 | 状态 | 要点 |
|------|------|------|
| 根因 1: `heartbeat()` 零生产调用点, `heartbeat_at` 永久冻结 | 部分修复 | v1.71.0 起 `--heartbeat-only` → `heartbeat_by_track` 是生产刷新路径 (`scripts/phase1_gate.py:1160`); 但 `heartbeat()` 本身仍零调用, 且刷新只在 `/state-scanner` 入口触发, 不再进入 scanner 的容器其 `heartbeat_at` 仍会停摆 (case-4) |
| 根因 4: 须同一个 Identity 实例 | 已绕开 | `heartbeat_by_track` 与 session 无关 (case-5); acquire 侧同类问题 (self-resume 仍按 session 判) 见 10CG/aria-plugin#202 |
| 修法 (b): 接上 heartbeat loop | 未修 | 入口钩子不是循环 (case-4); `SKILL.md:182` 的触发条件仍是「本会话持 active claim」, 10CG/aria-plugin#107 的 2026-09-27 评论已指出并提出改为「本容器」, 尚未落地; 审计轮内不刷见 10CG/aria-plugin#168 |
| 根因 2 / 3 + 预期行为: 30 分钟后 advisory 碰撞面静默 | 未修 | v1.74.1 仍复现 (case-1 / 2 / 9); 归档 Spec 记为成文残余风险, owner 2026-08-23 裁定 `STALE_TTL` 维持 30 分钟 |
| 修法 (a): takeover 判定改用 `SWEEP_TTL` / `COLLISION_TTL` | 未实现 | owner 2026-08-23 的裁定 (作用域是归档 Spec) 是不改 `STALE_TTL`, 是否对本单永久适用待 owner 裁定。另非「一行常量」: `_is_stale` 同时服务 Rule 6 与 Rule 5.1 (`lib/reconcile.py:283`), `track_board` 另用 `STALE_TTL` 区分黄 / 红 (`scripts/renderers/track_board.py:293-297`), `tests/test_reconcile_golden_table.py` 的 Case 3.x 钉住 `STALE_TTL` 边界的语义 |
| 修法 (c): 对 stale claim 单独降级提示 | 未实现 | case-7; 检索未见任何 issue 跟踪它 (见处置) |
| SilkNode 2026-08-09 重复实现 | 不适用 | 外部项目的历史事件, 无法复现也无可关闭的验收项。今天的预防面: 仅当双方 claim 都带同一 `linked_issue` 且 track-id 不同时, 由 overlap 通道覆盖 (case-8); 同一 track-id (case-9) 或任一方未带 `linked_issue` 时仍静默。对方会话根本没跑认领属纪律问题, 机制覆盖不到 |

### Verdict Rationale

本单与 10CG/aria-plugin#107 同根因 (心跳不刷 → `heartbeat_at` 停摆 → 30 分钟 `STALE_TTL` 判 stale → 同名 advisory 通道静默), 但范围不同, 不是重复。10CG/aria-plugin#107 的标题与三条 to-do (self-resume 刷新 / phase 转换点刷新 / 收回 `SWEEP_TTL`) 跟踪的是心跳接线; 其中前两条是事件钩子, 不是定时器, 第三条动的是 durable sweep 的 `SWEEP_TTL`, 与 advisory 用的 `STALE_TTL` 无关。三条全部做完后, 一个长 Phase B.2 内既没有 `/state-scanner` 入口、也没有 phase 转换时, 同名通道仍会在最后一次刷新 30 分钟后静默 (case-4)。本单的验收项 (对方心跳停摆超过 30 分钟时, B 仍收到 occupied) 以及修法 (a) / (c) 都不在 10CG/aria-plugin#107 的任何 to-do 里, 所以 10CG/aria-plugin#107 的 to-do 全部完成也不等于本单症状已解; 10CG/aria-plugin#107 可以按自身范围关闭, 症状仍会原样存在。

维护方自己的文本也以本单为这一症状的锚点: 10CG/aria-plugin#168 正文把长审计轮期间的「7c occupied surface 静默」称为 10CG/Aria#180 的窗口, 并写明 10CG/aria-plugin#168 自己是 10CG/aria-plugin#107 覆盖不到的第二个窗口; 归档 Spec 的 `proposal.md:197` / `:251` / `:538` 同样以本单的编号指代同名通道静默; 10CG/aria-plugin#202 把根因 4 的 acquire 侧 (self-resume 仍按 session 判, 同容器换 session 会新建第二条 active claim) 单列。分工: 心跳各挂载点由 10CG/aria-plugin#107 (入口触发条件 / self-resume / phase 转换点)、10CG/aria-plugin#168 (审计轮内)、10CG/aria-plugin#202 (acquire 侧 session 匹配) 承接; 症状本身与修法 (a) / (c) 只在本单。10CG/aria-plugin#107 已在 owner 决策单第 6 项的 P1 批内, 本单的症状级验收项不随它自动落地。

verdict 取 `partial-repro` 而不是 `confirmed`: 症状完整复现, 但 issue 写的根因与现状已有实质偏离 (根因 1 部分失效, 根因 4 被绕开, 9 个 case 中 4 个不复现), 修复不应再按原根因 (接上 `heartbeat()`、传同一个 Identity) 设计, 见上面的 Deviation note。严重度取 `major`: 有 workaround (开工前先在 issue 上留认领评论; 会话开场手动补刷心跳), 但 advisory 机制对长任务这一主场景不生效, 且 issue 正文记载的 SilkNode 事件 (两个会话对同一 spec 的三个任务做了整块重复实现) 发生在这类窗口里。

### 处置

保持 open, 不关闭; 本评论不代为裁定。

1. 关闭条件 (建议, 待 owner 确认): 对方心跳停摆超过 30 分钟时, 另一容器的 advisory 闸门不再完全静默 (给出 occupied, 或给出对 stale claim 的降级提示; 即修法 (a) / (b) 的定时器形态 / (c) 之一兑现); 或 owner 明确裁定接受这一 30 分钟窗口并记为 wont-fix, 且修法 (c) 有归属。
2. 待 owner 裁定 (已提请 owner 决定): 修法 (a) —— owner 2026-08-23 在归档 Spec 内裁定不改 `STALE_TTL`, 这一裁定是否对本单永久适用 (即 (a) 记为 wont-fix), 还是可以复议; 修法 (c) —— 是否排期、由哪张 issue 跟踪。两仓 (10CG/Aria 139 条、10CG/aria-plugin 121 条, open + closed 全量翻页) 的 issue 检索里, COLLISION_TTL / 降级提示 / stale claim 这几个检索词只命中本单, 未见跟踪 (c) 的 issue。单列新 issue、改 10CG/aria-plugin#107 的正文或标题, 都超出 owner 2026-09-30 决策单第 4 项的一次性授权范围 (feature 分支推送 / 开 PR / issue 评论 / issue 关闭), 本评论不代为操作。
3. 采用方注意: 引用本单的规避做法 (10CG/SilkNode#987 与 10CG/SilkNode#988 两个 handoff PR 记载: 在本单修好之前, 开工前先在 issue 上留认领评论是唯一可靠的防撞信号) 在 v1.74.1 上仍应保留; 本单被 triage 不代表症状已修。

---

*Generated by `/issue-triage` v1.74.1 — Ref: 10CG/Aria#180*
