---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T14:35:43.081Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — tech-lead 席 (换镜头: 对 v2 新机制做反事实与架构后果)

审计对象: `proposal.md` **v2** (commit `d23f103`)。本席只审不改, 未修改任何仓内文件; 全部实验脚本落 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/exp{1..7}.py`。

## R1 处置核对

逐条对 R1 聚合表「Critical 簇 / Major 处置」列与 v2 正文比对, 并对可机械验证的处置实跑复核。

| R1 finding | 三态 | 证据 (一句) |
|---|---|---|
| **C-1** 判定键缺跨容器 owner 归并 | **closed** | v2 `proposal.md:35` 加入步骤 3 owner 等价类; 本席按该规则在冻结语料 996 行上跑生产路径 (exp5), 得 `self_multi_container` + 两组, 与 v2 实验表 D 行逐字一致, 原「同人两机恒 🔴」不再出现; `:69` D-1(a) 后果句已重写为「靠等价类消解 / 未共现的串仍会 🔴 一次」。 |
| **M-1** SC-4 折叠与「dedupe 不改逻辑」互斥 | **closed** | `:34` 已写「**dedupe 键改为 `(track_id, identity_key)`** (`handoff_multibranch.py:518-523`, **显式改动项**, 不再「不改逻辑」)」; SC-4 (`:112`) 的「先红」判据与现码一致 (现 3 段解析下 `simonfish/bfe8285d` → `("", "simonfish", "bfe8285d")`, 键含 owner 段不折叠)。R1 附带的 `after_dedupe` 统计变化也进了实验表 (121 vs 122)。 |
| **M-2** `track_board` 建表/查表键不同源 | **closed** | `:36` 已列为**显式改动项**并点名「修掉今天就查不中的 bug」; SC-4 第三条 (`:112`) 断言 board 回显原串且注明先红。 |
| **M-3** 与 a1-entry 的语义耦合排序 | **partial** | `:91` 给出了有方向的 (i)(ii)(iii) 硬排序 —— 方向问题闭合; 但三项都只覆盖 `identity.py` flip 与行号漂移, 未覆盖 a1-entry 的 **track-id 容器段**这一条更承重的耦合 (本轮 C-1), 也没写「a1-entry 未落地时本 Spec 的 ship 形态」(本轮 M-4)。 |
| **M-4** flip 无迁移面 + 「恒 uuid」假全称 | **partial** | 迁移面闭合: `:37` 新增 T3b flip 前守卫, `:90` 列全六处消费方, SC-3 (`:111`) 覆盖守卫。假全称只闭合了**代码侧**措辞 (`:37`「不写「恒 uuid」, hostname 分支是既有降级路径」), **共享 SOT 侧未闭合** —— D2 的 `:40` 仍写「`<container-id>` 明确 = container-id 文件的 **uuid 字段** (label 不参与)」, 无降级口径 (本轮 M-7)。 |
| **M-5** 「与 #182 正交」实为依赖 | **closed** | `:47` 已改写为「是**依赖, 不是正交**」并给出 19 份 stale active 的实证; `:88` Positive 拆成「分类逻辑」与「信号可用性取决于 D-3」两段; `:123` 非目标写明依赖方向; 新增决策点 D-3 (`:79-82`) 未预设结论。 |
| **M-6** Level 判据三项全中 | **partial** | `:3` 已按 Rule #10 上呈 owner (写明 owner 指令 = Level 2 / 审计建议 Level 3 / 请复议) —— 上呈动作闭合; 但 R1 要求的「若维持 Level 2, 写明依据哪条**判据**认为不算 architecture/cross-module」未做, 给出的「可辩护理由」全是规模论证 (本轮 m-1)。 |
| **m-1** reconcile tie-break 退化 | **closed** | `:89` Risk (2) 已成文, 含触发条件、缓解与「加 SC 锁定不因此崩溃」。 |
| **m-2** advisory 产出宿主未定 | **partial** | 宿主已钉死 (`:46`「宿主是 `classify()` 的 dict, 不是 `classify_claims` 的 2-tuple」) —— 一半闭合; 但 R1 m-2 的**第二半**(渲染器需要一条与 `collision_kind` 无关的取数路径) 未处置: 渲染器不读该字段, 它自己重算 (本轮 M-6)。 |

**三态计数: closed 5 / partial 4 / open 0。** 没有一条被口头处置而正文未落地 —— 处置质量本身是高的; 本轮的 Critical/Major 全部是 v2 **新引入机制**的后果, 不是 R1 的复发。

## 审计结论

### C-1 (critical) a1-entry 的 track-id 容器段与本 Spec 的分组键冲突, 而本 Spec 把自己**硬排在它之后**: ship 后 🔴/🟡 是否还可达, 由对方容器的实现选择决定, 两个 Spec 都没定义

- **type**: risk
- **severity**: critical
- **category**: architecture
- **scope**: `proposal.md:91`「与 a1-entry 的边界 (硬排序)」/ `:40` D2 §2.3.1「闭合 a1-entry §3 的 follow-up」/ `lib/collision.py::classify:300-403` / `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md §2.1b` / `standards/conventions/session-handoff.md §2.3.8.2`
- **summary**: 本 Spec 的全部分类都在 `track_id` 内做; a1-entry 把 A.1 派生串定为 `<spec-slug>-<container_uuid>` 并规定它**就是**本 cycle 的 carry-id, 而 §2.3.8.2 要求 carry-id 与 frontmatter `track-id` 取相同原始串。两条规则一起意味着 Layer H 的 track-id 要么带上容器段 (两容器再不同组, 🔴/🟡 结构性不可达), 要么违反 §2.3.8.2 (Layer H 与 Layer L 用两个 id 指同一份工作)。硬排序 (i) 把本 Spec 排在其后, 却只分析了 `identity.py`。
- **evidence**:
  - 分组键实读: `lib/collision.py:363` `for tid in sorted(verdicts.keys())` —— `classify()` 逐 `track_id` 判定; dedupe 键第一元也是 `track_id` (`handoff_multibranch.py:518` `key = (t.get("track_id"), owner, container)`)。两容器若 track_id 不同, `classify_claims` 每组只剩 1 条 ⇒ `:145` `if len(active) < 2: return "none", ""`。
  - a1-entry `proposal.md:134`「**`<spec-slug>-<container_uuid>` —— 唯一形态**」; `:142` `container_uuid` = container-id 文件的 uuid 字段, 不截断、跳过 label; §2.1b (`:187`)「**A.1 认领时派生的那一串, 即本 cycle 的 carry-id**」+「`session-handoff.md` **§2.3.8** 结构化 `{id, desc}` 的 `id` **同为该串**」。
  - `standards/conventions/session-handoff.md:234` (§2.3.8.2)「当某条 §6 carry-id 与本 handoff **doc-level frontmatter `track-id`** (§2.3.1) 指向**同一份工作**时, 两者取**相同原始串** …… 否则同一份工作被算成两条不相关 track」。
  - a1-entry 的 Impact 表 (`:653-670`) 只列 `§2.3.8`, **不列 §2.3.1**, 且 §2.1b 内的 R3/KM-1 订正明确把改动范围从 §2.3 收窄到 §2.3.8 ⇒ 当前 plan of record 是「carry-id 带容器段, frontmatter track-id 不带」= 直接与它自己要改的 §2.3.8.2 相矛盾。
  - 实证两者今天确实相等: 冻结语料 117 个 distinct track_id 中只有 1 个以 `-<8hex>` 结尾 (`aria-plugin-113-gate-result-yaml-20260719`, 且那是日期不是容器), a1-entry 自己的 handoff 全部用裸 slug `a1-entry-claim-duplicate-work-guard` (exp1 输出)。a1-entry ship 后该轨的 carry-id 会变成 `a1-entry-claim-duplicate-work-guard-023236f2`, frontmatter 仍是裸 slug。
  - 本 Spec `:40` 声称 D2「与 Layer L claim `container` 同口径 —— 闭合 a1-entry §3 的 follow-up」。实读 a1-entry §3 结尾 (`:415`) 的 follow-up 原文只覆盖 **container 段**口径; **track-id 段**的口径分歧是 a1-entry §2.1b 新造的, 两个 Spec 都没记。
- **为什么是 critical 而不是 major**: 两条分支都伤。分支 1 (frontmatter 跟进容器段) 让本 Spec 的交付面在 ship 当天归零 —— 本 Spec 修的每一条判据都跑在「同 track_id 内」这个前提上; 分支 2 (不跟进) 让 §2.3.8 内部自相矛盾, 而**本 Spec 正是那个要改 §2.3 并自称「闭合两标识关系」的 Spec**, 由它 ship 一份已知自相矛盾的 SOT 不可接受。现在的 proposal 两条都没写, 等于把「本 Spec 有没有用」交给对方容器在 B.2 临场决定 —— 这与 R1 M-3 被接受的那条原则 (「排序规则不能留给 B.1 临场判断」) 同形。

### M-1 (major) owner 等价类的**假合并**方向未成文: 一次「两人共用过一台 uuid 容器」永久把真 cross_owner 降级为 🟡 —— 正是本 Spec 立项要修的那个 bug

- **type**: risk
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:35` (D1 步骤 3) / `:69` (D-1 (a) 后果) / `:89` (Risk 表) / `:21` (§Why 结论句) / `:88` (Positive)
- **summary**: 并查集只有合并、没有拆分, 且证据是「共现」而非「同一人」。两个真人先后在同一台 uuid 容器上写过 handoff (Lab 今天 `bfe8285d` / `023236f2` 两台都已有两个 owner 串共现) 之后, 他们的 owner 串**永久同类**, 此后在任何 track 上的真撞车都判 `self_multi_container` 🟡。D-1 的后果句只写了漏合并方向 (未共现 ⇒ 多报一次 🔴), 没写误合并方向 (共现过 ⇒ 永久少报), Risk 表三条也不含它。
- **evidence**:
  - 规则原文 `:35`「同一 uuid 容器上共现过的 owner 串两两等价」——「共现」的判据里没有任何「是不是同一个人」的信息。
  - 实跑反事实 (exp6): 语料含 `alice/aaaa1111` + `bob/aaaa1111` (共用过一台) 时, 之后的真两人两机 `alice/bbbb2222` + `bob/cccc3333` → `self_multi_container`; 同一对无共用史 → `cross_owner`。同一组输入, 结论相反。
  - 本 Spec §Why 第 1 条 (`:17`) 把「**真两人两机 → 也是 🟡 (真撞车降级)**」列为要修的病; Positive (`:88`) 承诺「真两人撞车 = 🔴 (**不再降级**)」。等价类在共用容器这一形态下把同一个降级重新引入, 只是换了成因。
  - 现实可达性不是理论: exp2 输出 `uuid->owners = {'023236f2': ['aria-runner-bot','simonfish'], 'bfe8285d': ['aria-runner-bot','simonfish']}` —— 两台 uuid 容器**都**已经有两个 owner 串共现记录。若 D-2 裁定把 `aria-runner-bot` 与人身份视为两个 owner (选项 (b)/(c) 下正是如此), 这两串已经是同一类。
  - 无衰减、无作用域: `:43`「历史 handoff **不 rewrite**」+ 等价类从全语料重建 ⇒ 一次共用事件的影响是永久且全局的 (跨全部 track)。

### M-2 (major) 等价类由「全语料」建, 而全语料随 `branches_scanned` 变化: 同一组输入在不同容器 / 不同时刻可得相反结论, 且方向是「语料越全越不告警」

- **type**: issue
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:35` (「对**全语料**……建并查集」) / `:46` (advisory 从全语料产出) / `scripts/collectors/handoff_multibranch.py` (`branches_scanned`) / `lib/reconcile.py:9`
- **summary**: collector 每次扫的语料是「本容器 fetch 到的分支集合」, 冻结快照自己就把它记成一个可变字段。等价类不持久化、不随快照传播, 每次扫描重建 ⇒ 缺一条共现证据就从 🟡 翻成 🔴。更糟的是方向: **fetch 得越全的容器告警越少**, 而落后一步的容器会对同一现实喊 🔴。
- **evidence**:
  - 冻结快照顶层字段 `branches_scanned: 10` (exp1), `note` 自述是「起草日的 Layer H 语料快照」—— 语料随分支集合变动是记录在案的事实; 实际有行的分支只有 8 个 (exp5), 两个分支零行, 说明该集合本身也在漂。
  - 实跑反事实 (exp6): group = `["aria-runner-bot/023236f2", "simonfish/bfe8285d"]`; 语料含共现行 `simonfish/023236f2` → `self_multi_container`; 语料不含 → `cross_owner`。
  - `lib/reconcile.py:9` 的公开承诺「Deterministic: identical input → identical output across all containers」在字面上不被违反 (输入确实不同), 但**系统级**属性「所有容器看到同一块看板」被打破 —— 而多终端协调这块看板的**唯一**用途就是让不同容器对齐。
  - 不可解释性 (镜头 1c) 只被**部分**覆盖: `identity_advisories[]` (`:46`) 每条带 `{identity_key, owners[]}`, 并查集的每条边都在里面, 所以 🟡 的理由**在本机语料内**可推导 —— 这一点核验通过。但推导不出的是「对方容器为什么看到 🔴」, 因为等价类既不持久化也不进 snapshot。
  - 今天的语料**没有**暴露这一点 (exp5 逐分支跑: 8 个分支子集全部把 `aria-runner-bot`/`simonfish` 合成同一类, 因为 `023236f2` 的共现行在每个分支上都复制了一份) ⇒ 这是**结构缺口不是当前红灯**, 但 SC 全表没有一条锁「等价类对语料子集的稳定性」, B.2 会全绿通过。

### M-3 (major) D-1 与 D-2 被当成独立决策点呈给 owner, 实际耦合: 执笔建议的 (a)+(a) 组合会让 `cross_owner` 在生产数据上不可达, 而 Positive 第一句是**无条件**写的

- **type**: decision
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:69` (D-1 (a)) / `:74` (D-2 (a)) / `:71` `:77` (两处执笔建议) / `:88` (Positive) / SC-2 (`:110`)
- **summary**: D-1 (a) 把 `<owner>` 钉死为 git `user.email` local-part; D-2 (a) 让所有 AI 会话署同一个 bot。两者同时成立时, 所有由 AI 写出的 handoff 的 owner 段是**同一个常量**, `owners` 集合恒为 1 ⇒ `cross_owner` 对生产数据结构性不可达, 「真两人撞车 = 🔴」只能靠合成夹具绿。D-2 (a) 的代价句写了「两位操作者的 AI 会话之间无法区分」, 但没把这句接到本 Spec 自己的判据上, owner 也就看不到「选 (a)+(a) = 主动放弃 🔴 这一态」。
- **evidence**:
  - owner 段来源实读: `session-closer/scripts/handoff_autofill.py:391-410` `owner_container()` 复用 `identity.get_identity().owner_container`; `lib/identity.py:158-186` `get_owner()` = `git config user.email` 的 local-part。⇒ 容器的 git 身份统一成 bot, 全部 handoff 的 owner 段就统一。
  - 判据实读: `lib/collision.py:150-152` `owners = {c.owner for c in active}; if len(owners) >= 2: return "cross_owner"` —— v2 只是把 `owner` 换成等价类代表, 集合恒为 1 这一点不变。
  - 冻结语料已呈现该趋势: 10 种串里 `aria-runner-bot/*` 已占 134 行 (exp1), 而 `:18` §Why 记的漂移点是 08-26/08-27 —— 也就是 D-2 (a) 事实上**已经在执行**。
  - Positive (`:88`) 的写法: 「collision **分类逻辑**第一次同时满足: 真两人撞车 = 🔴 (不再降级)、……」—— 只给「信号可用性」挂了 D-3 条件, 没给 🔴 挂 D-1/D-2 条件。
  - SC-2 (`:110`) 的 cross_owner 两臂用的是 `alice`/`bob` 合成串与「真实两段式两人两机」夹具; 在 (a)+(a) 下这两臂**永远只能靠夹具绿**, 生产数据无法命中 —— 与本仓 memory `feedback_completion_signals_vs_runtime_invocation` 记的形态同类。
- **不代裁**: 本席不建议 owner 选哪个。要求只有一条 —— D-2 的三个选项各自补一句「该选项下 `cross_owner` 在生产数据上是否可达」, 并把 Positive 第一句改成有条件句; 否则 owner 是在缺一半后果的情况下裁 D-2 (与 R1 C-1 被接受的理由同形)。

### M-4 (major) 硬排序 (i) 把本 Spec 的 flip 无限期挂在**对方容器**的 a1-entry 上, 却没写「a1-entry 未落地时本 Spec 的 ship 形态」; (ii) 的越权面被写成「知会」而非「取得同意」

- **type**: issue
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:91` (i)(ii)(iii) / `:11` (a1-entry 待 B.1, 对方容器 `023236f2`) / `:88` (Positive「label 陷阱结构性消除」) / T3 (`:98`)
- **summary**: 两个缺口。(1) a1-entry 是对方容器持 active claim 的在飞轨, 且它自己已走到 R6 仍在 B.1 前; (i) 说 flip 排在它 B.2 之后, 但没写「若它迟迟不落, 本 Spec 怎么 ship」。而 flip 不落时, Positive 承诺的「label 陷阱 (#135 08-13 形态) **结构性消除**」为假 —— `get_container_id()` 仍是 label 优先, 新 handoff 仍可能把 label 写进 container 段, 而 D1 步骤 2 的 `^[0-9a-f]{8}$` 判据正是建立在「container 段是 uuid」上的。(2) (ii) 让本 Spec「承担改写 a1-entry SC-3 的判据」并「在 #174 留言知会对方容器」—— 改的是对方容器 claim 中的 Spec 文档与测试, 只知会不取得同意。
- **evidence**:
  - a1-entry 归属实读: 本 Spec `:11`「对方容器 `023236f2`, 待 B.1」; 冻结语料里该轨 30 天内 10 条 active/superseded 行全部是 `simonfish/023236f2` (exp1/exp7), 无本容器足迹。按 memory `feedback_other_container_active_claim_is_occupied_regardless_of_heartbeat`, active claim = 占用, 与心跳新鲜度无关。
  - 阻塞面: a1-entry proposal 已到 R6 (`:743` 记 R6 五席聚合) 且仍标「待 B.1」; 它自身还挂着 `allowed-tools` 扩权 + Rule #6 照跑两套 AB (`:400-410`) ⇒ B.2 落地时间不可预期。
  - Positive 的失效点: `:88`「label 陷阱 (#135 08-13 形态) 结构性消除」与 `:37`「该 flip 的**落地时机受 §Impact 硬排序约束**」/ T3 `:98`「**排在 a1-entry B.2 后**」直接冲突 —— 不 flip 就没消除。
  - (ii) 的对象: a1-entry `proposal.md:571` SC-3 的红窗判据 + 其宿主测试 (`:668` 行「`skills/state-scanner/tests/` (既有宿主) … SC-3 …」)。本 Spec 未区分「a1-entry 已 merge 进 master (改测试属正常下游维护)」与「仍在对方分支 (跨 claim 编辑)」两种情形。
- **要求 (不含裁量)**: §Impact 补一段「a1-entry 未落地时的 ship 形态」—— 明确本 Spec 在不 flip 的前提下交付哪些 SC、Positive 哪一句要摘掉、以及 `^[0-9a-f]{8}$` 判据在 label 仍可能出现时的行为; 并把 (ii) 的前置从「知会」改成「a1-entry 已 merge 至 master」或「取得对方容器同意」二选一。

### M-5 (major) D-3 要过滤的人口被低估: `track_to_claim_record` 把 8 种非 enum status (语料 280/996 行, 含语义终态的 `superseded`/`closed`/`complete`) 静默当成 `active`; 且新阈值与 `classify:374-379` 的「捞回 stale winner」形成一套没人写过的三档行为

- **type**: issue
- **severity**: major
- **category**: implementation
- **scope**: `proposal.md:47` (D3 与 #182 的关系) / `:80` (D-3 (a) N=30) / SC-6 (`:114`) / `lib/collision.py:113-124` / `lib/collision.py:374-379` / `lib/constants.py:36,50`
- **summary**: D-3 的规模论证与 SC-6 的归因桶都只数 `status: active`。实读 `track_to_claim_record` 的 else 分支把任何非 enum 值一律映射成 `active`: 冻结语料 996 行里 280 行属此类 (`complete` 119 / `closed` 64 / `in_progress` 40 / `ship_ready` 16 / `superseded` 16 / `blocked` 10 / `paused` 8 / `partial` 7), 30 天内还有 19 行 (含 `superseded`)。也就是说参与判定的「活跃行」是 384 行而不是 104 行。另外 D-3 (a) 的截止与 `:374-379`「把被 reconcile 降级的 stale winner 重新捞回」是**反向**机制, 叠加后行为分三档 (<30 分钟 / 30 分钟-N 天 / >N 天), 三档语义无人成文; 阈值宿主也未定 (`constants.py` 已有两个不同量纲的阈值)。
- **evidence**:
  - 代码原文 `lib/collision.py:113-124`: `if status_raw in ("active", "legacy"): status = "active"` … `else: status = "active"` —— 兜底就是 active。
  - 实测分布 (exp2 / exp7): `done 612` / `active 104` / 8 种非 enum 共 280; 30 天内非 enum 19 行, 最近的是 6 天前的 `superseded a1-entry-claim-duplicate-work-guard simonfish/023236f2`。§2.3.1 (`session-handoff.md:118`) 的 enum 只有 `active`/`done`/`abandoned` ⇒ 这 280 行本身是 schema 违规, 但 collector 静默吸收。
  - D-3 与 SC-6 的口径: `:47` 只写「19 份历史 `status: active` frontmatter」; SC-6 (`:114`) 的归因桶是「真撞车 / 同人多机 / stale active (#182)」三选一, **没有第四桶**「非 enum status 被强制当 active」。
  - 反向机制原文 `lib/collision.py:374-379` 注释:「… or a 2-claim collision where the winner is stale would mis-classify as none」—— 它存在的目的就是**不让**陈旧行掉出判定, 而 D-3 (a) 的目的是让它们掉出。
  - 阈值宿主: `constants.py:36` `STALE_TTL = 1800` (advisory 接管阈值) 与 `:50` `SWEEP_TTL = 86400` (durable 改写阈值) 已并存且量纲不同 (memory `feedback_durable_rewrite_ttl_separate_from_advisory_ttl`); D-3 (a) 的 N=30 天是第三个, `:80` 只说「与 STALE_TTL 不同量纲」, 未说放 `constants.py` 还是 config, 也未说是否可配。
  - 本席实跑复核 D-3 数字 (exp5): 选 (a) N=30 ⇒ `after_dedupe` 122→94, `kind = none`, **0 组** —— SC-6 的「D-3 选 (a) 时改后 = 0 组」核验通过; 但这个 0 是把 19 行非 enum 行一并按 active 计入后仍为 0, 属**侥幸**, 不是机制保证。

### M-6 (major) `identity_advisories[]` 落在 `classify()` 的 dict 上, 而渲染器根本不读该字段 (它自己重跑 dedupe+reconcile+classify_claims): ⚪ 行要么重实现一遍并查集, 要么重开代码里明文记着的 collector/renderer 分叉

- **type**: issue
- **severity**: major
- **category**: implementation
- **scope**: `proposal.md:46` (D3 第 1 条) / T4 (`:100`「`track_board.py:412-417` 键同源 + ⚪ 行」) / `scripts/renderers/track_board.py:155-185, :430, :459-475`
- **summary**: R1 m-2 的宿主问题闭合了一半 —— advisory 放 `classify()` 的 dict 确实不动渲染器的 2-tuple 解包。但渲染器不消费持久化的 `tracks_multibranch.collision`, 它从 snapshot 的原始 `tracks` 自己 dedupe + reconcile + `classify_claims`。所以 `classify()` 里算出的等价类与 advisory 对渲染器**不可见**, 而 T4 把 ⚪ 行直接派给了 `track_board.py`。两条出路 (渲染器再实现一遍并查集 / 把等价类提升为 lib 共享函数供两边同调) 后果差别很大, Spec 未选。
- **evidence**:
  - 渲染器自算实读: `track_board.py:176-183` 导入 `dedupe_latest_per_track_container as _dedupe_tracks_for_collision`; `:430` `collision_kind, _severity = _classify_collision(active_claims)`; 全文无对 `tracks_multibranch.collision` / `identity_advisories` 的读取。
  - 该文件 `:158-165` 的注释逐字记着这类分叉的历史:「COLLISION lines and the collector's persisted `tracks_multibranch.collision` **always agree on the SAME snapshot**. Before this fix the renderer fed the … after the collector itself had already stopped reporting a collision for …」—— 即「两边各算一遍」正是被这段代码修掉的病。在渲染器里第二次实现等价类会把它原样重开。
  - `:459-475` 的 `elif collision_kind == "none": pass` 分支确认: SC-2 (`:110`) 要的「同容器双 owner → `kind == "none"` 且出 1 条 advisory」在渲染侧必须走一条与 `collision_kind` 无关的新路径 —— v2 `:46` 只写「board 渲染为 ⚪ 行」, 没写这条路径的数据来源。

### M-7 (major) D2 写进共享 SOT 的「`<container-id>` = uuid 字段」是一条与本 Spec 自己的 D1 步骤 2 互斥的全称句; 且 §2.3.1 —— 本次最承重的文本改动 —— 零 SC 覆盖

- **type**: issue
- **severity**: major
- **category**: documentation
- **scope**: `proposal.md:40` (D2 §2.3.1) / `:34` (D1 步骤 2 主机名分支) / `:37` (hostname 兜底保留) / SC-5 (`:113`) / `standards/conventions/session-handoff.md:116`
- **summary**: R1 M-4 的假全称在代码侧改对了 (`:37` 明写不写「恒 uuid」), 但 D2 要写进 standards 的那句仍是全称:「`<container-id>` 明确 = container-id 文件的 **uuid 字段** (label 不参与)」。本 Spec 自己的 identity_key 规则同时要求「主机名 / 空」这一支**长期存在** (历史 10 种串里 5 个 container 标识有 2 个是主机名), 且 `get_container_id()` 的只读 fs 兜底会继续产出 hostname。采纳方按这句实现会拒绝或误判合法的历史与降级形态。SC-5 只锁 §2.3.5 三行、§2.3.9 存在、§2.3.7/§2.3.8 diff 零 —— §2.3.1 一条断言都没有。
- **evidence**:
  - 现行 SOT 原文 `session-handoff.md:116`:「`<container-id>` = `~/.aria/container-id` 持久 short-UUID + 可选人类标签, **缺省回退 hostname**」—— 现有文本**已经**覆盖三态; D2 的改写把其中两态删掉。
  - 本 Spec 依赖主机名分支的原文 `:34`:「否则 (主机名 / 空) ⇒ `identity_key = owner + "/" + container` (主机名跨机不唯一, 保留 owner 段区分 —— 这正是既有测试 `test_owner_segment_participates_in_grouping_key` 那条不变式的成立域)」。
  - 降级路径实读: `lib/identity.py:236-242` 写文件失败 → 打 warning → `return _hostname()`; `:78-83` `_hostname()` 无任何 sanitize。
  - 语料实证 (exp1): 10 种 owner-container 串对应 5 个 container 标识, 其中 `dev-claude` (263 行含零段) / `dev-claude2` (48 行) 是主机名形 —— 占语料 31%。
  - SC 覆盖面: SC-5 (`:113`) 的三条断言对象是 §2.3.5 / §2.3.9 / §2.3.7-8, 无 §2.3.1; T5 (`:101`) 列了 §2.3.1 但箭头也指向 SC-5。

### m-1 (minor) Level 段把「维持 Level 2 的可辩护理由」写成规模论证, 与同一份文档里自认的 cross-module / breaking 事实并列, owner 拿到的是一组互相矛盾的输入

- **type**: decision
- **severity**: minor
- **category**: documentation
- **scope**: `proposal.md:3` / `:8` / `:41` / `standards/core/ten-step-cycle/phase-a-spec-planning.md:126-137`
- **summary**: 上呈动作本身合规 (写明 owner 指令 / 审计建议 / 请复议 / 不自行上下调)。但给出的三条理由 (「交付面 5 个代码文件 + 1 份规范 + 3 处消费文档」「9 个任务」「无 schema 破坏」) 全是规模与影响面, 而 SOT 判据问的是**性质** (architecture / cross-module / breaking)。同一份文档 `:8` 自陈代码落点跨 `aria/` 与 `standards/` 两个子模块 (= cross-module), `:41` 自陈 §2.3.5 是「**实质变更, 不是措辞变更**……对采用方是行为变更」(= breaking)。三条理由一条也没回应这两处自陈。
- **evidence**: `:3` 三条理由逐字; `:8`「**代码落点**: `aria/` 子模块 … + `standards/` 子模块 …」; `:41`「**实质变更, 不是措辞变更** (对 SilkNode / Kairos / nexus 等采用方是行为变更…)」; 判据流程图 `phase-a-spec-planning.md:131-137`「Is it architecture/cross-module/breaking? ├─ Yes → Level 3」。本席不裁 Level, 只要求这三条理由改成回应判据本体 (或直接标注「无判据层理由, 纯请 owner 按指令裁」)。

### m-2 (minor) `^[0-9a-f]{8}$` 是对**值的形状嗅探**, 而 provenance 在写入时是已知的; 8 位 hex 的主机名 / label 会被静默当成全局唯一 uuid

- **type**: risk
- **severity**: minor
- **category**: implementation
- **scope**: `proposal.md:34` (D1 步骤 2) / `lib/identity.py:96-98, :78-83, :222`
- **summary**: 判据与生成形态一致 (核验通过), 但它靠猜: 只读 fs 兜底返回的 hostname 若恰好是 8 位小写 hex (容器化环境里 hex 主机名并不罕见), 或用户把 label 设成 8 位 hex, 该串会被判为「uuid 全局唯一」⇒ owner 段被丢弃 ⇒ 两台不同机器折成同一个 identity_key (与 M-1 相反方向的静默错误)。写入侧本来知道自己返回的是 uuid 还是 hostname, 这个信息在 frontmatter 里被丢掉了。
- **evidence**: `lib/identity.py:96-98` `_generate_uuid()` = `secrets.token_hex(4)` ⇒ 恒 8 位小写 hex, 与 `^[0-9a-f]{8}$` 严格同形 (**镜头 2 核验通过**); `:242` `return _hostname()`, `:78-83` `_hostname()` 直接返回 `socket.gethostname()` 无 sanitize; `:222` `return label if label else uuid` ⇒ label 可为任意串。SC 全表无「8 位 hex 主机名不得被当 uuid」的负控。

### 核验通过、不构成 finding (供后续轮次省时)

- **实验表可复现**: 本席按 v2 `:34-35` 规则重实现三步判定并在冻结语料上跑生产路径 (exp5), 得 `after_dedupe = 122`, `kind = self_multi_container`, 两组 = `['simonfish/dev-claude','simonfish/dev-claude2']` 与 `['dev-claude','simonfishgit/dev-claude']` —— 与 v2 实验表 D 行**逐字一致**; A 行用真代码跑得 `996→121` / `self_multi_container` / `[['dev-claude','simonfishgit/dev-claude']]`, 也一致。SC-6 的「D-3 选 (a) 时改后 = 0 组」复现通过。
- **`identity_key` 与 a1-entry 的 `container_uuid` 同形** (镜头 2): a1-entry `proposal.md:142` 定义 `container_uuid` = container-id 文件 uuid 字段, 不截断、跳过 label ⇒ 与本 Spec 的 `^[0-9a-f]{8}$` 同一形态, 无口径冲突。
- **等价类的可解释性在本机语料内成立** (镜头 1c 的一半): `identity_advisories[]` 每条带 `{identity_key, owners[]}`, 并查集的每条边都在其中, 🟡 的成因可从 board 推导; 不成立的只有跨容器那一半 (已归 M-2)。
- **D3 告警对象数字**: `:62` 列的 `023236f2: [aria-runner-bot, simonfish]` / `bfe8285d: [aria-runner-bot, simonfish]` 与主机名容器不入等价类, 本席实跑 (exp2) 完全一致, 另有 `f9c6e8cd: [simonfish]` 单 owner 不告警。
- **零段串的判档**: 「类数 ≤1 → self_multi_container」在类数**为 0** 时 (两行 owner 段皆空) 落到 🟡 (exp6 实测) —— 谓词是全分割 (互斥且全覆盖), 无未定义格; 但「不可归属 = 🟡」是一个未明说的设计选择, 值得在 D2 §2.3.5 一句带过, 不单独记 finding。

## Verdict

**FAIL** — 1 Critical (C-1) + 7 Major (M-1..M-7) + 2 minor。计数口径: **1C/7M/2m**。

判据: Critical ≥1 即 FAIL。C-1 是承重的 —— 它决定本 Spec 的分组键在 ship 后是否还存在, 而当前两个 Spec 都没定义, 等于把「本 Spec 有没有用」交给对方容器 B.2 临场决定。M-1/M-2/M-3 是同一类形状: v2 新引入的等价类机制有三个未成文的后果 (假合并 / 语料依赖 / 与 D-2 的耦合), 每一个都单独足以让 Positive 第一句在生产上不成立, 而 owner 正要拿这三个决策点裁 D-1/D-2/D-3。M-4..M-7 是可机械补齐的成文与落点缺口。

需要说明的是 v2 的 rework 质量本身是高的: R1 的 9 条 finding 无一 open, 5 条完全闭合、4 条闭合了主体。本轮的 Critical/Major 全部来自换镜头后对**新机制**的反事实, 不是旧问题复发 —— 这符合 memory `feedback_multiround_audit_catches_fix_introduced_regression` 记的形态 (加固动作自身开新面), 属健康收敛而非振荡。

## Vote

**REVISE**

最小返工面 (按优先级, 均不含 owner 裁量):

1. **C-1**: §Impact「与 a1-entry 的边界」补第四条 —— 明确 a1-entry 的 `<spec-slug>-<container_uuid>` 是否传导到 Layer H frontmatter `track-id`, 两条分支各自的后果与本 Spec 的应对; 若判定「不传导」, 则 D2 必须同时处理 §2.3.8.2 的自相矛盾 (它正是本 Spec 要改的那一节所在文件)。
2. **M-1 / M-2 / M-3**: 决策点补后果 —— D-1 补假合并方向 (共用容器 ⇒ 永久少报) 与语料依赖 (同一组输入随 `branches_scanned` 可翻转); D-2 三个选项各补一句「该选项下 `cross_owner` 在生产数据上是否可达」; Positive 第一句改成有条件句。三条都只要求补事实, 不要求改选项集。
3. **M-4**: §Impact 补「a1-entry 未落地时本 Spec 的 ship 形态」; (ii) 的前置从「知会对方容器」改为「a1-entry 已 merge 至 master」或「取得对方容器同意」。
4. **M-5**: D-3 的人口口径按 384 行 (含 280 行非 enum status) 重述; SC-6 归因桶加第四桶; 明确 N 的宿主与三档行为 (<STALE_TTL / STALE_TTL..N / >N) 各自语义。
5. **M-6**: 钉死 ⚪ 行的取数路径 —— 等价类提升为 `lib/collision.py` 共享函数供 collector 与 renderer 同调, 或明写渲染器如何读 snapshot 字段; 不留给 B.2。
6. **M-7**: D2 §2.3.1 的 `<container-id>` 句改成覆盖三态 (uuid / label 不参与 / 只读 fs 兜底 hostname); SC-5 加一条 §2.3.1 的内容断言。

**不代裁**: D-1 / D-2 / D-3 / Level 四项本席均不给结论, 只要求把上述事实补进决策输入。

## 轮次记录

**实读文件** (全部本轮实读, 未凭记忆):

- `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` v2 (全文 135 行, commit `d23f103`)
- `.aria/audit-reports/post_spec-R1-…-aggregated.md` (全文 74 行, Critical 簇 3 + Major 11 + Minor 摘要) 与 `…-tech-lead.md` (本席 R1 全文)
- `aria/skills/state-scanner/lib/collision.py` (`split_owner_container:63-82` / `track_to_claim_record:86-140` / `classify_claims:143-166` / `classify:300-403`, 含 `:113-124` status 兜底与 `:363` 逐 track_id 循环、`:374-379` stale winner 捞回)
- `aria/skills/state-scanner/lib/identity.py` (`:78-83` `_hostname` / `:96-98` `_generate_uuid` / `:158-186` `get_owner` / `:189-244` `get_container_id` 含 `:222` label 优先与 `:236-242` hostname 兜底)
- `aria/skills/state-scanner/lib/reconcile.py` (`:1-20` 模块承诺 / `:140-165` `_tiebreak_key` / `_is_stale`)
- `aria/skills/state-scanner/lib/constants.py` (`:25-55` `HEARTBEAT_INTERVAL` / `STALE_TTL` / `SWEEP_TTL`)
- `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` (`:500-540` dedupe 键与 stats / `:695-725` 生产路径 dedupe→classify)
- `aria/skills/state-scanner/scripts/renderers/track_board.py` (`:100-185` 导入与分叉注释 / `:400-440` 标签表与 `:430` 解包 / `:455-475` `none` 分支)
- `aria/skills/session-closer/scripts/handoff_autofill.py` (`:391-410` `owner_container()` 来源)
- `standards/conventions/session-handoff.md` (§2.3.1 `:110-130` / §2.3.5 `:178-190` / §2.3.6 / §2.3.8 `:217-245` 含 §2.3.8.2 / §2.3.8.3)
- `standards/core/ten-step-cycle/phase-a-spec-planning.md:118-150` (Level 判据表 + 流程图)
- `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (`:134-148` §2.1 track-id 形态 / `:180-195` §2.1b carry-id 契约 / `:374-415` §3 含 follow-up 结尾 / `:565-578` SC-1..SC-3 / `:653-670` Impact 表)
- `.aria/repro/handoff-tracks-frozen-2026-09-05.json` (996 行 tracks + `branches_scanned` / `note` 顶层字段)

**跑过的实验** (脚本落 scratchpad, 未写入仓内):

1. `exp1.py` — 冻结语料形态: 996 行 / 10 种 owner-container / 段数分布 (900 两段 + 96 零段 + **0 三段**) / status 分布 (10 种值) / 117 个 distinct track_id / 30 天内 active 17 行。
2. `exp2.py` — 真代码跑 A 行 (`dedupe_latest_per_track_container` → `classify`): `996→121`, `self_multi_container`, 1 组; 并统计 status → ClaimRecord.status 的映射 (280 行被兜底成 active)。
3. `exp3.py` — v2 dedupe 键计数 (`996→122`, 与只修 parser 同值) + 列出 post-dedupe 有 ≥2 identity_key 的两个 track。
4. `exp4.py` — 定位本席首轮仿真偏差根因 (误用真 `track_to_claim_record` 走旧三段解析)。
5. `exp5.py` — v2 三步判定完整重实现 (两段式 ClaimRecord + identity_key dedupe + 全语料并查集 + reconcile): D 行 `122 / self_multi_container / 两组` 与 proposal 逐字一致; D-3 (a) N=30 ⇒ `94 / none / 0 组`; N=60 ⇒ `98 / none / 0 组`; 逐分支 (8 个) 重建等价类。
6. `exp6.py` — 三个反事实: 语料含/不含共现行 ⇒ 同一组 `self_multi_container` vs `cross_owner`; 共用过容器的两人 ⇒ 真撞车被吞成 `self_multi_container`; 零段串的类数 0 落档。
7. `exp7.py` — 非 enum status 行的年龄分布: 280 行总量, 30 天内 19 行 (含 6 天前的 `superseded`)。

**未做**: 未修改任何仓内文件; 未 fetch 远程 (a1-entry 以本地 checkout 的 proposal 为准, 其分支实况按本 Spec `:91` (iii) 归 B.1 起手时核); 未读 Forgejo issue 原文 (#193 / #135 以 R1 已核结论沿用)。
