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

## §0.5 四个推荐工作流 — 执行序建议与实况

> 本段补写于 2026-09-08。`/state-scanner` 阶段 2 给出四个推荐工作流后, 我按下面的序执行, **但当时没有把这个序作为交付物写下来** —— 只是隐式做了。这里补上判据, 供复议与下个 session 接手。

### 我建议的序 (及判据)

| # | 工作流 | 序 | 判据 |
|---|---|---|---|
| **【1】** | C.2 集成: `feature/a1-entry-claim-duplicate-work-guard` → master | **第 1** | **它是唯一阻塞别人的**。该分支未合时, aria 子模块与主仓 gitlink 处于分叉态; 后面任何动版本面的工作都会在一个陈旧基线上做。且它已 40/40 完成, 只差合并 —— **成本最低、解除阻塞最多**。 |
| **【3】** | H3: 把 `DEFECTS.md` 的 24+ 条 AB 缺陷开成 issue | **第 2** | **纯外向、零代码耦合**, 与 2/4 的文件域完全 disjoint, 可与后面并行。放在前面是因为它有**信息半衰期** —— DEFECTS.md 的观测随套件演进失效, 越晚开单越可能已经对不上 (实测: 开单时 13 处需要订正)。 |
| **【2】+【4】** | H2 类级 sweep + M2 SKILL.md 漂移 | **第 3, 且合并为一个 Spec** | 见下。 |

### 为什么把【2】和【4】合并而不是串行做两个 Spec

state-scanner 把它们列为两条, 但实测**它们是同一个缺陷的两半**:

- 【4】 M2 说的是 `openspec-archive/SKILL.md` 声称「自动修正 CLI bug」而本仓从未装该 CLI;
- 【2】 H2 说的是这条漂移**不止一处** —— 它散在 SKILL.md 14 处 + `phase-d-closer` + 两份 README。

若分成两个 Spec: 【4】改一处、【2】改其余, 两者共用同一个 SC-1 判据、同一次 AB、同一次发版。按 memory `split-makes-seams`「拆 Spec 缩 scope 会自造接缝缺陷 (实现无归属 / 引用悬空 / 单侧修复)」, **拆开的成本高于收益**。

⇒ 合并为 `archive-gate-registration-class-and-skill-drift`, 一次 Spec / 一次审计 / 一次发版。

### 实况 (2026-09-08 实测)

| # | 状态 | 证据 |
|---|---|---|
| 【1】 | ✅ **完成** | PR `10CG/Aria#202` `merged=True`, merge commit `9f25a666`; Spec 已归档 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard` |
| 【3】 | ✅ **完成** | `10CG/aria-plugin` 看板上 AB 缺陷单 10 张在册 |
| 【2】+【4】 | **52/69**, 未完成的 17 项**全在 TG-E** | 卡两个 owner 门 (见 §2) |

### 偏离建议序的地方 (如实登记)

1. **Part A 被拆出去了**, 不在原计划内。起草后实测其生产触达为 **0/18**, 按 owner 裁定拆成 `10CG/aria-plugin#188`, 本 Spec 收缩到漂移收口。
2. **审计轮次远超预期**。原以为 Level 3 Spec 走 post_spec + post_planning 各 3 轮左右; 实际两个检查点各用满 `max_rounds=5` 仍 `converged=false`, post_planning R5 是 FAIL。**这是本 cycle 最大的时间去向**, 判据与教训见 §4 第 1 条。
3. **Phase B 交付物又追加了一轮 agent team 复审** (不在原序里)。理由: 那批东西是我单线做的, 而本 cycle 自己的证据是单线产物缺陷率高。事后证明必要 —— 抓到 28 条, 含三处会静默 ship 的硬编码版本号。

### 若两个门解除, 剩余 17 项的执行序

**E-1 → E-2 → E-3 → E-4 → E-4a → E-5 → E-6a → E-6b → E-6c** ⟨此处是 E-0 的边界⟩ **→ E-7a → E-7b → E-8 → E-9 → E-10 → E-11**

- E-1 必须在**带 `ARIA_COORDINATION_NO_PUSH=1` 启动的会话**里才能往下走 (门 2)
- E-6c 之后是 E-0 的硬边界: **未得 SC-11 裁定不得进入 E-7a** (门 1) —— E-7b 是子模块双推, 不可逆
- E-4 的取号必须**重跑三腿**, 不得照抄 §2 里那个 `v1.73.0` (并发轨在动)

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

**Phase B 落地复审 (2026-09-08, agent team)** —— 提交 `d650f8d` (子模块) / `539f875` (主仓):

上面那批 TG-B/TG-C/TG-D 交付物**全部是主控单线做的, 没有第二双眼睛看过**。按本 session 自己刚沉淀的判据 (「席位都看过前几轮时 0C+PASS 不是收敛证据」), 拉了 6 席 agent team 按交付域复审 (58 agent / 6.1M subagent token), **5 席 FAIL**, 37 条原始 → 33 去重 → **28 条存活**, 全部处置。

抓到的实缺陷里最要命的四条:
- **三处硬编码 `v1.72.0`** 落在 SKILL.md 正文 —— 正是 proposal 逐字 ⛔ 禁止、并发轨 `10CG/Aria#195` 正在争的号, 且它**不在 E-5 的 13 文件同步清单里、六个版本 check 也够不着** ⇒ 会静默 ship。
- **Step 3/4 的守卫对真实失败态失明**: 实测 `git mv src dst` 当 dst 已存在为目录时**返回 rc 0** 并把 src 嵌进去, 而我写的三条断言在该坏结果上**全为真**。已加 Step 3 两条前置 + Step 4 断言 4。
- **Step 7 的校验行排在创建 issue 之前**, 而 `{number}` 此刻无绑定 ⇒ 逐字执行必 rc 2, 而同段自己规定 rc≠0 判 FAIL。已整段后移并绑定来源。
- **`check_bare_issue_refs.py` 自称 fail-CLOSED 却有三个 fail-OPEN 洞** (路径伪装被当全限定 / 白名单整行豁免 / 项目专属字面硬编码进分发脚本)。已逐条封死并把白名单外置到 `.aria/bare-issue-ref-allowlist.txt`。

另有一条**被反驳席杀错、我自己复核后判成立**的: C-3/C-8/C-10 三项验收逐字写「留证」, 我勾了框但**仓内零输出**。已补 `evidence/phase-b-probe-runs.md` (12 态, 由脚本重新实跑生成)。

对外订正四条追评论, 其中 `10CG/Aria#208` 是**根因写错了** —— 举证物是个已交付的 Python 文件, 真因是「符号名→定义」的解析方式而非交付物语言。

**TG-E 推进到 E-6c (2026-09-08)** —— 提交 `129c85d` (子模块 v1.73.0 发版) + 主仓:

**先撤销了一道我自己造的阻塞。** 我在 post_planning R5 给 E-1 加了「必须带 `ARIA_COORDINATION_NO_PUSH=1` 启动会话」这个前置, 并据此把 E-2 起全部步骤自我阻塞。实测两条独立证据推翻它:
- SOT `AB_TEST_OPERATIONS.md` §场景 1 的触发条件是**按套件名封闭枚举**的, `openspec-archive.json` **不在其中**;
- 判据本体 (「能触达 `phase1_gate`/`release_gate`」) 实测不成立 —— 该 SKILL.md 里 5 处提及**全在示例输出块**, 零处是调用。

根因: 我把「摸到真仓树」与「推协调 ref」两个不同的风险混成了一条。R5 的 tech-lead 席指出「eval 2 无 `project_root`」这个**事实是对的**, 但它推出的结论不成立, 而我采纳时没有验证推理链。**教训: `exact-exception-condition` 是双向的 —— 既不能松引豁免, 也不能凭一个「事实正确但推理断裂」的 finding 加一道 SOT 没有的闸门。**

**E-2/E-3 Rule #6 AB** (动态工作流 `w1wr6ganw`, 4 臂 + 2 grader): v_new **6/6** vs v_old **6/6**, `delta.pass_rate = 0`, 有区分力的 expectation **0**。**与 Spec 起草期登记的预期逐字吻合。** 六项改动逐条对照无一被现有 expectation 承接; grader 另发现一条结构性缺口: `description` 因评测台把 SKILL_MD 路径直接喂给 ARM, **触发面按构造被绕过, 本套件永远测不到它** —— 而 Rule #6 第二行恰恰是「`description` 变动一律照跑 AB」, 两者之间有个洞。已追进 `10CG/aria-plugin#190`。

运行纪律实测: 仓内零意外写入, 子模块干净, **协调 ref 跑前跑后逐字节相同 (`e13ef10a`)** —— 独立佐证上面那条撤销。

**E-4/E-5 发版面**: `<vNEXT>` = **`v1.73.0`** (三腿实跑避开并发轨在争的 `v1.71.2`/`v1.72.0`)。版本串同步**实测 21 处 / 12 文件, 与起草基线逐字一致**; 残留 `1.71.1` 恰 2 处, 均为 append-only 历史记录。

**E-6**: 五个仓内 check **5/5 全绿** (后 bump 树上直接实跑); `plugin-cache-currency` **`STALE installed=1.71.1 sot=1.73.0` rc=1**, 符合 E-6b 预期且未算进全绿。
> ⚠️ 过程中差点记下一个**陈旧的绿**: 首次读的是 bump 前 85 分钟的 snapshot, 那里所有版本串还一致是 1.71.1, 五个 check 当然全绿但证明不了 bump 后的状态。已改为直接实跑。

**⇒ 任务完成度 52/69 → 61/69。剩余 8 项全部卡在 `SC-11` 一道门上。**

---

## §2 未完成 / Carry-forward — **两个门, 都要 owner**

### 门 1 — `SC-11 owner 裁定` — **⚠️ 2026-09-08 重新定性: 它的阻塞那一半已被测量闭合**

SC-11 原本混着两件事, 现在必须分开看:

**(1) Rule #6 完备性** —「本 Spec 跨三个 Skill, 是不是三个套件都得跑?」 ✅ **已由测量闭合, 与裁定无关**

依据 SOT §2 决策表**第四行**「拿不准 ⇒ **照跑** (宁跑勿豁)」, 主控**无条件**执行了分支 (b) 而非等裁定。实测三套件矩阵:

| 套件 | v_old SKILL.md sha256 | v_new sha256 | `--numstat` | 处置 |
|---|---|---|---|---|
| `openspec-archive` | `5593508c…` | `edba8c5e…` | 63+/34− | ✅ 已跑 (E-2/E-3) |
| `phase-d-closer` | `550f33b7…` | `4b432573…` | 2+/2− | ✅ 已跑 (E-0b) |
| `state-scanner` | `cf5257599672ee04…` | `cf5257599672ee04…` | **0+/0−** | ⛔ 两臂**逐字节相同** |

`state-scanner` 不跑的理由是**结构性的**: 两版 SKILL.md 逐字节相同、`description` 零变动 ⇒ 它的 AB 是两个完全一样的臂, 不可能产生任何区分信号 (SOT §3 点名的测量剧场)。⇒ **分支 (b) 已满足到物理极限; 分支 (a) 则是多做了。**

**(2) 規范空白** —「SOT §1『整个变更』的跨 Skill 作用域该怎么写进 SOT」 ⏳ **仍待裁, 但不 gate 发布**

SOT 全文 76 行 (v1.0.0) 实读确认: §1 那句「整个变更就照跑」通篇语境是**文件内部**的描述性/处方性并存, 从未提跨 Skill; §5 五个成文样例**全是单 Skill**; §6「已知局限」讲的是 AB 测量有效性 (baseline 污染) 而非作用域。**该空白真实存在**, 值得写进 SOT §5 —— 但无论怎么裁, AB 该做的都已做完。

> ⛔ **主控没有据此自行把 SC-11 判成满足。** 剩余 7 项卡的不再是 Rule #6, 而是 **`E-7b` 的不可逆性** —— 它把 `v1.73.0` 打 tag 并双推到两个公共 remote。那需要 owner 明确授权。

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

**`<vNEXT>` = `v1.73.0` —— 已于 2026-09-08 实取并落盘** (E-4 已执行, `plugin.json` SOT 现为 `1.73.0`) (E-4 三腿实跑: 两 remote 已发布最高 `v1.71.1`; 两条并发轨 `10CG/Aria#195` 与 `10CG/Aria#199` 的 proposal 都出现 `v1.71.2` 与 `v1.72.0`; 全 handoff 面扫 12 份零未来号声明)。**该值随并发轨推进而变, E-4 执行时必须重跑三腿。**

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
| `10CG/Aria` (主仓) | `338436d` … `f2e83fc` `7cf81a3` **`539f875`** | R4/R5 审计 + 类级 sweep + Phase B + **落地复审修复** | **未推** (feature 分支) |
| `10CG/aria-plugin` (aria) | `2b67ac6` **`d650f8d`** | TG-B 18 hunk + TG-C 三探针 + **复审修复** | **未推** (feature 分支, E-7b 才双推) |
| `10CG/aria-standards` | — | 本 cycle 未改 | — |

---

## §6 Next session 入口

1. ⭐ **`{id: archive-gate-registration-class-and-skill-drift, desc: TG-E 发版, 卡两个 owner 门}`** —— 进入前先按 §3 第 4 条刷一次 heartbeat; 先确认两个门是否已裁, 再决定从 E-1 还是 E-0 起步。**若要跑 AB, 必须以 `ARIA_COORDINATION_NO_PUSH=1 claude ...` 启动会话。**
2. 并发轨 `10CG/Aria#195` / `10CG/Aria#199` 都在 post_spec 轮次中, 与本轨共享整个发版面 —— 动版本串前必读它们当前的自报号。
