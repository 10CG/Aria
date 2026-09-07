---
track-id: archive-gate-registration-class-and-skill-drift
owner-container: simonfish/023236f2
phase: B
status: active
updated-at: 2026-09-07T14:54:10Z
---

# Aria — Session Handoff (2026-09-07) — Phase B 三个任务组落地, TG-E 停在两个 owner 门

> **一句话**: 把 `archive-gate-registration-class-and-skill-drift` 从 post_planning R4 推到 **Phase B 51/69**, TG-B (18 个文档 hunk) / TG-C (3 个探针 + 单测 + 夹具) / TG-D (6 张单) 全部完成并验收, TG-E **停在 E-1 与 E-0 两个门**, 不自行降级。
> **本 session 最该记住的一件事**: **R4 那轮「0 Critical, 两席 PASS」是陈旧眼睛的产物。** R5 换上三席新眼睛加一个全新镜头 (执行期时间维度), 缺陷从 0C/1M 反弹到 **2C/12M**, 三席 FAIL。两条 Critical 都不是新写坏的, 是**四轮陈旧眼睛从没看见的既有缺陷**。memory `stop-adding-rounds`「换新鲜眼睛 > 加轮」在这里是字面兑现的。

---

## §0 入口 (新 session 优先读)

1. `openspec/changes/archive-gate-registration-class-and-skill-drift/tasks.md` —— **51/69 已勾**, 剩余 18 项全在 TG-E, 顶部有 🛑 阻塞登记段
2. `.aria/audit-reports/post_planning-R5-*-aggregated.md` —— **verdict=FAIL, converged=false, max_rounds=5 用满**
3. 本文 §2 的两个门 —— 两者都需要 owner 动作, AI 补不上

---

## §1 已完成 (本对话, UTC)

**post_planning R4 + R5 两轮审计** (提交 `338436d` `cfa182e` `91acb1d` `567aa1e`):
- R4: 0C/1M, 首次两席 PASS
- **R5: 五席 + 完备性批评席, 三席 FAIL, 2C/12M**, 23 条 finding 全部落地 (29 处编辑, 一律类级 sweep)
- R5 后按 owner 裁定做**定向类级 sweep** (不开 R6): 四条「Spec 自己写下却只应用到发现处」的洞见逐条查漏, 产出集中在「基线该断言为红」—— 17 个验收项里 11 条没标基线色, 且抓到 **B-V7(a) 恒绿**

**Phase B** (提交 `2b67ac6` 子模块 / `d2d93da` `f2e83fc` 主仓):
- **TG-B 18 个 hunk**: openspec-archive 从「自动修正 CLI bug」全面改为 git mv + 归档后校验; Step 5 并入 Step 3; Step 7 SHA 回链占位串 `Step2` → `Step 7`; 退役 `keep_changes_copy`; 同步 phase-d-closer 与两份 README
- **TG-C 三个探针全落盘 + 注册 + 6 个单测 + 4 份冻结夹具**: C-3 四态 / C-8 五态 / C-10 三态全部实跑符合
- **TG-D 6 张单**: `10CG/aria-plugin#190` `10CG/aria-plugin#191` `10CG/aria-plugin#192` `10CG/aria-plugin#193` · `10CG/aria-standards#21` · `10CG/Aria#208`, 全部回读核验
- 验收: SC-1 区段外 **15 → 0** / SC-2 命中 1 / SC-3 (a)0行 (b)3行 (c)4/4 / SC-4 全落新小节 / C-V1 `openspec-archive OK (6 tests)` (基线该行不存在) / C-V3 `status == pass` / 全套件 **2122 → 2128**, 11 OK / 0 FAIL

---

## §2 未完成 / Carry-forward — **两个门, 都要 owner**

### 门 1 — `SC-11 owner 裁定` (⛔ 阻塞 E-7a 起全部步骤, 含子模块合并双推)

Rule #6 SOT §1「任一 hunk 处方性且在测量范围内 ⇒ **整个变更**照跑」在「一个 Spec 跨多个 Skill」时**作用域无明文**。本 Spec 的判定不依赖对它的解读 (逐 hunk 走 §2 明文映射), 但需 owner 二选一:
- **(a)** ratify v1.69.1 的形状为成文 lane 并写进 SOT §5 ⇒ 本 Spec 只跑 openspec-archive 一个套件即可合并
- **(b)** 另裁 ⇒ 按其裁定补跑 phase-d-closer / state-scanner 套件后方可合并

> R4 的 GOV 席指出: 上一版把此项写成「advisory, 不阻塞发版」是**一种新形态的自行豁免** —— 它不在 `configured-gate-authority.md` 白名单四类内。已改为阻塞。

### 门 2 — `ARIA_COORDINATION_NO_PUSH` 会话级前置 (⛔ 阻塞 E-2 起全部步骤)

本会话**未设置**该变量, 而它是**进程级**前置, 会话内 export 改不了 subagent 继承环境。两个承重事实已逐字实证:
- eval 1 `correct-archive-path` 带 `project_root=/workspace/my-project` (合成, 不触真仓)
- eval 2 `already-archived-detection` **无 `project_root`**, 两个路径均为仓相对 ⇒ 真仓 cwd 下落到真仓树

⇒ **须由 owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 重启会话再跑 E-2**。E-2/E-3 阻塞 ⇒ 按 Rule #6, E-4 起全部阻塞。**非规则豁免, 是执行条件不具备** (memory `session-level-precondition`)。

### 待复议项 — `keep_changes_copy 声明接口移除`

B-9 退役了该配置项。三条实证: 全仓仅 SKILL.md 出现 2 次、零代码消费方 / 零测试 / 零 eval; `changes/` 与 `archive/` slug 零重叠 ⇒ 历史从未行使; 若行使则同一 spec 同时在两处, 被 `collectors/openspec.py` 计成幽灵活跃变更并永挂 `pending_archive`。
**这是声明接口移除, 请 owner 复议。** 该选项从未实现 (零代码宿主) ⇒ 移除不构成运行时破坏性变更 ⇒ 仍 MINOR; owner 若裁定保留则 B9 撤销, 版本级别不变 ⇒ **发版不阻塞于该复议**。

### `post_spec converged=false` 与 post_planning converged=false

两个检查点**均以 `max_rounds=5` 用满而未达全票 PASS 收场**。post_planning R5 verdict = **FAIL** (三席 FAIL)。
按 Rule #10 我**既不自行宣告收敛, 也不自行加开 R6** —— 如实登记并经本 handoff 上呈复议 (Rule #10 §5)。
判据说明: 按 memory `marginal-return-negative` 的拐点判据 (本轮 fix 引入的 major 占比 > 1/2), R5 的 15 条存活里我前两次修订引入的只有 **5 条 ≈ 1/3**, **未过拐点** —— 另外 10 条是四轮陈旧眼睛从没看见的既有缺陷。**边际产出仍为正, 因为变的是 finding 来源 (新眼睛 + 新镜头), 不是轮数。**

### `plugin-cache-currency` — 如实登记 (Rule #10 §5 强制披露)

该 check 是 `severity: warning` 的**启用态** custom check。版本 bump 后它期望 **STALE 而非绿**: 它比的是运行时 `~/.claude/plugins/installed_plugins.json` 与 SOT `plugin.json`, bump 后立刻转红且**在本 cycle 任何位置都转不绿** —— 转绿要 owner 终端跑 `/plugin marketplace update` + `/plugin update` + 重启 session。
tasks 把它设计成「如实登记 STALE + handoff 点名」而非阻塞项。**这是 AI 的流程判断, 请复议。** R4 GOV 席的支持理由: 它测的是本会话本地插件缓存的新鲜度, 与本 Spec 代码变更本身的正确性无关 —— 拿它阻塞 C.2 不会多防住任何真实缺陷; 而 SC-11 直接关系「代码有没有被 AB 充分验证」, 性质不同。

### `<vNEXT>` — 并发轨三方抢号 (本轨对另两轨结构性不可见)

**本时刻推得 `<vNEXT>` = `v1.73.0`** (E-4 三腿实跑: 两 remote 已发布最高 `v1.71.1`; 两条并发轨 `10CG/Aria#195` 与 `10CG/Aria#199` 的 proposal 都出现 `v1.71.2` 与 `v1.72.0`; 全 handoff 面扫 12 份零未来号声明)。**该值随并发轨推进而变, E-4 执行时必须重跑三腿。**

⚠️ **本轨对那两条轨结构性不可见**: 本 Spec 的 `proposal.md` 只在**未推送的 feature 分支**上 (他们 `git show origin/master:` 取不到); 协调板 claim 的 `linked_issue` 在**另一个仓** (`10CG/aria-plugin#186` vs 他们的 `10CG/Aria#195` / `10CG/Aria#199`) ⇒ `linked_issue_overlap` 对本轨返回 `[]`。**本段的 `<vNEXT>` 声明是他们能看见本轨的唯一通道。**

### `D-6 定时风险`

已开 `10CG/Aria#208`。**起草时的前提被 Phase B 实跑推翻**: 原写「`:353` 全仓相对路径 ⇒ dead ⇒ block」, 实测 `verdict=warn`, `blocking=0`, 两种引用形态都落 `unclassified`。真实缺陷是**归档闸门 C 分级死码检查对非 Python 符号结构性失明**。⏰ 定时性在于 `aria-2.0-m6-e2e-resilience` 归档时会撞上它。

---

## §3 关键风险 / 已知陷阱

1. **`aria-orchestrator` 指针全程 dirty** (他轨 `feature/m6-cost-model-telemetry`) —— 本 Spec 全程不动它, 每次提交前核 `git status` 确认未卷入。本 session 已核, 未卷入。
2. **aria 子模块 HEAD `2b67ac6` 未推任何 remote** —— 停在 `feature/archive-gate-registration-class-and-skill-drift`。主仓 gitlink 已 bump 指向它。E-7b 才双推。
3. **主仓本地 master 落后 origin/master 9 个 commit** (并发轨在飞)。每次实质 git 动作前必 fetch。
4. **协调板 claim 曾静默 17.5 小时** (`STALE_TTL=1800s`), 距 `SWEEP_TTL` 扫成 abandoned 只剩 6.5h 时被发现。已刷心跳并 `ls-remote` 独立回读核验。**长会话须定期刷心跳。**

---

## §4 实战教训

1. **陈旧眼睛会制造假收敛。** R4 的三席都看过前几轮, 报 0C/1M; R5 换三席新眼睛 + 一个全新镜头, 报 2C/12M 三席 FAIL。两条 Critical 都是既有缺陷, 不是新引入的。**加轮不解决这个, 换人才解决。**
2. **「Spec 自己写下却只应用到发现处的洞见」是一个可穷举的缺陷类。** 两条 Critical 同形状: proposal 早写着「Part B 自身会移动行号」和「不用 env」, 但只被用来修发现它的那个验收项, 从没回头 sweep 兄弟位置。定向 sweep 该类是高产的 (17 个验收项里揪出 11 个没标基线色 + 1 个恒绿)。
3. **对外动作前实读源码救回了一张会写错的单。** D-6 起草时的前提在 Phase B 实跑下两半皆被推翻 —— 若照起草稿开单, 会给 owner 一个错误的根因。
4. **我修东西时会把一个恒真换成另一个恒真。** B-V7(a) 原写「不以『填入』结尾」基线已满足; R5 我改成「`grep -c '填入\"'` == 1」, 基线实测也已是 1。两版都是恒绿。判据应该是「这个量本次会不会变」。
5. **自下而上 + 逐行内容核对的护栏当场生效。** TG-B 若按原顺序执行会把 Step 6 删掉 (B-8a 使 7 行变 4 行, 下方上移, B-8b 的绝对 `:259-261` 恰落到 Step 6)。护栏挡住了。

---

## §5 提交清单

| 仓 | SHA | 说明 | 推送状态 |
|---|---|---|---|
| `10CG/Aria` (主仓) | `338436d` `cfa182e` `91acb1d` `567aa1e` `d2d93da` `f2e83fc` | R4/R5 审计 + 类级 sweep + Phase B | **未推** (feature 分支) |
| `10CG/aria-plugin` (aria) | `2b67ac6` | TG-B 18 hunk + TG-C 三探针 | **未推** (feature 分支, E-7b 才双推) |
| `10CG/aria-standards` | — | 本 cycle 未改 | — |

---

## §6 Next session 入口

1. ⭐ **`{id: archive-gate-registration-class-and-skill-drift, desc: TG-E 发版, 卡两个 owner 门}`** —— 进入前先按 §3 第 4 条刷一次 heartbeat; 先确认两个门是否已裁, 再决定从 E-1 还是 E-0 起步。**若要跑 AB, 必须以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 启动会话。**
2. 并发轨 `10CG/Aria#195` / `10CG/Aria#199` 都在 post_spec 轮次中, 与本轨共享整个发版面 —— 动版本串前必读它们当前的自报号。
