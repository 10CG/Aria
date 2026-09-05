---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T15:08:25.299Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — tech-lead 席 (镜头: 架构收敛性 — v3 是否还有隐含「推断同一人」逻辑 / 决策点是否穷尽且后果对称 / 两种 ship 形态是否自洽)

审计对象: `proposal.md` **v3** (commit `91b86fb`)。本席只审不改, 未修改任何仓内文件; 实验脚本落 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/r3_exp1.py`。

## R2 处置核对

逐条对本席 R2 报告的 C-1 / M-1..M-7 / m-1 / m-2 与 v3 正文比对, 可机械验证的实跑复核。

| R2 finding | 三态 | 证据 (一句) |
|---|---|---|
| **C-1** a1-entry track-id 容器段与同 track 分组冲突, 两 Spec 都没定义 | **partial** | v3 `:66-70` 把它上呈为决策点 D-0 并写「须在 B.1 前裁定」—— 「两 Spec 都没定义」这一半闭合; 但 (a) 的实现子句「仅当该 8hex 是语料中出现过的 `identity_key`」把语料依赖装回**分组键** (本轮 M-1), 且「分组键」作用于三个 `track_id` 分组点中的哪一个未写 (本轮 M-2)。 |
| **M-1** 等价类只合不拆 (共现过 ⇒ 永久假合并) | **closed** | v3 `:4` 明写「撤销 v2 引入的 owner 等价类」; `:34` 判定改为纯输入 `identity_key` 计数 + 「非空且非 unknown 的 owner 串集合」, 并逐字写「**没有「同一个人」推断**……即使 D3 显示它们曾在同一容器共现 (那是给人看的解释, 不是判定输入)」。 |
| **M-2** 等价类由全语料建, 随 `branches_scanned` 翻转 | **closed** | 承载体已删; `classify` 侧的输入面 (`:34`) 只剩「同 track 的 active 行 (dedupe 后)」两个字段, 与 `branches_scanned` 无关。**注**: 同形失效在 D-0(a) 的族键子句上复现 (本轮 M-1), 但那是新构造, 不记为本条未闭合。 |
| **M-3** D-1/D-2 耦合未呈给 owner, Positive 无条件 | **partial** | `:72` 已标「与 D-2 **耦合**, 请一起裁」; `:78` D-2(a) 补了「`cross_owner` 结构性不可达 / 🔴 的真实含义 = 另一提交身份」; `:92` Positive 已改条件式。但 R2 要求的「**三个**选项各自补一句可达性」只做了 (a)(b), `:80` 的 (c) 没有 (本轮 m-1)。 |
| **M-4** flip 无限期挂对方容器 + 未写 ship 形态 + 「知会」非「同意」 | **partial** | `:95` 写出 S1/S2 两形态, 并把越权面改为「a1-entry B.2 已落地**且**对方在 #174 ack……未取得 ack 不动对方文本」—— 方向与授权闭合; 但 S1 形态给出的两条缓解 (T3b 检查 + ⚪) 在机制上都不成立 (本轮 M-3)。 |
| **M-5** D-3 人口低估 + 与 `:374-379` 叠成三档 | **partial** | `:46` 已把 8 种非 enum status 逐项列数 (280/996); `:84` 明写人口 = 「被映射为 active 的全部行, 含 280 行非 enum」且截止在记录构造阶段应用「**不与 `:374-379` 叠成三档** (被截止的行 reconcile 看不到)」—— 两处闭合。但 (a) 分支在 Tasks/SC 里零落点、渲染器同源路径未写、常量名与量纲仍只说「分开」(本轮 M-4)。 |
| **M-6** advisory 落 `classify()` dict 而渲染器不读该字段 | **closed** | `:45` 改为独立 lib 函数 `identity_drift_advisories(tracks)`, collector 在 dedupe 前调、渲染器「已持有原始 `tracks`」同样调, 明写「两处同源, 不重开 collector/renderer 分叉」; 实读 `track_board.py:743-747` 确认渲染器持有原始 `tracks` 并自行 dedupe, 该调用可行。 |
| **M-7** SOT 侧「`<container-id>` = uuid 字段」假全称 + §2.3.1 零 SC | **closed** | `:39` 改为三态 (「v1.22.x+ 有该文件的机器」/「无该文件的历史行 = 主机名」/「只读 fs 兜底 = hostname」), 与现行 SOT `session-handoff.md:116` 的三态口径不再互斥; SC-5 (`:119`) 增「§2.3.1 含 `identity_key` 定义与三态」断言。 |
| **m-1** Level 理由是规模论证而非判据 | **closed** | `:3` 改为逐项自评 (architecture = 否 / cross-module = **是** / breaking = 否), 结论「**判据上是 Level 3**」, 并把维持 Level 2 归为 owner 的显式 override (Rule #10), 未替 owner 决定。 |
| **m-2** `^[0-9a-f]{8}$` 形状嗅探 | **closed** | `:32` 「**已知限制** (成文)」+ `:93` Risk (4) + SC-4 (`:118`) 的 `devbox01` 对抗夹具 (8 位非 hex 主机名不折叠)。 |

**计数**: closed 6 / partial 4 / open 0。

## 审计结论

### M-1 (major) D-0(a) 的族键「仅当该 8hex 是语料中出现过的 identity_key」把语料依赖装回**判定键**, 与 v3 全篇的确定性原则互斥; 而实测表明这条语料查表在今天的数据上买不到任何东西

- **type**: issue
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:67` (D-0 (a)) / `:29` (D1「全部是纯输入函数, 不读语料历史」) / `:34` (「不是判定输入」) / `.aria/repro/handoff-tracks-frozen-2026-09-05.json`
- **summary**: 族键剥离与否直接决定两行是否落同一 `track_id`, 因而直接决定 `kind`。把剥离条件挂在「该 8hex 在语料中出现过」意味着分组键随 `branches_scanned` 变化 —— 与 R2 撤销等价类的第二条理由同形。实跑显示纯形状剥离与语料查表在冻结语料上结论完全相同。
- **evidence**:
  - v3 自设的原则原文 `:29`「**全部是纯输入函数**, 不读语料历史、不持久化状态」; `:34`「(那是给人看的解释, **不是判定输入**)」。D-0(a) 的族键是判定链上游 (分组), 却读语料。
  - 语料可变性是记录在案的字段: 冻结快照顶层 `branches_scanned` (R2 exp1 实测值 10, 其中 2 个分支零行)。两个容器 fetch 到的分支集合不同 ⇒ 「该 8hex 出现过吗」可给出不同答案 ⇒ 同一对 handoff 在两台机上分到不同组 ⇒ 一台 🔴 一台 `none`。
  - **纯形状替代的后果实测** (`r3_exp1.py`, 冻结语料 996 行 / 117 个 distinct `track_id`): 以 `-[0-9a-f]{8}$` 纯形状剥离, 命中的 `track_id` 只有 1 个 —— `aria-plugin-113-gate-result-yaml-20260719` (尾段是日期 `20260719`, 恰好全为 hex 字符); 剥离后与任何其他 `track_id` **零合并** (`shape-only strip merges distinct tids: {}`)。语料查表变体不会剥它 (`20260719` 不在 identity_key 集合 `{023236f2, bfe8285d, f9c6e8cd}` 里)。⇒ 两个变体在今天的全部真实数据上**输出一致**, 语料查表换来的只有非确定性。
  - 纯形状变体的残余代价可量化并可成文: 唯一形态是「尾段恰为 8 位 hex 的非容器后缀 (日期形) 被误剥」, 其伤害只在「剥后前缀与另一条真 track 相同」时出现 —— 今天为 0 组。这一点值得进 D-0(a) 的后果句, 让 owner 在「确定性 + 一条可量化的已知限制」与「跨容器可能给出相反结论」之间选, 而不是只看到前者的一半。
- **不代裁**: 本席不选 D-0 分支。要求是: (a) 的实现子句改为不依赖语料的判据 (形状, 或其他纯输入判据), 或在 (a) 的后果句里显式写出「分组键随本机 fetch 到的分支集合变化」这一后果, 让 owner 看到与 R2 撤销等价类时相同的那条代价。

### M-2 (major) D-0(a) 的「分组键」未指名作用于三个 `track_id` 分组点中的哪一个; 落错点会改到 Layer L 仲裁, 并与 a1-entry 主机制的设计正面相撞

- **type**: risk
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:67` / `:109` (T9) / `lib/collision.py:335-338, :347-352, :363` / `lib/reconcile.py:369-371` / `scripts/collectors/handoff_multibranch.py:522` / `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:104, :571`
- **summary**: 管线上有三处按 `track_id` 分组, 其中 `reconcile_all` 同时服务 Layer H (handoff 近似记录) 与 Layer L (真 claim)。D-0(a) 只说「分组键 = `track_id` 去掉尾部」, 没说改哪一处。落在 `reconcile_all` 或 claim 读取侧会把两容器对同一 Spec 的**真 claim** 并进一组并裁出 yielder —— 而 a1-entry 的设计是两串各自存在、靠 `linked_issue_overlaps` 互相告警。
- **evidence**:
  - 三处分组点实读: (1) dedupe 键 `handoff_multibranch.py:522` `key = (t.get("track_id"), owner, container)`; (2) `lib/reconcile.py:369-371` `grouped.setdefault(claim.track_id, []).append(claim)`; (3) `lib/collision.py:363` `for tid in sorted(verdicts.keys())`。
  - `reconcile_all` 是**跨层共用**的: Layer H 侧经 `track_to_claim_record` 喂入 (`collision.py:347-352`, 渲染器同样 `track_board.py:781-795`), Layer L 侧由 `phase1_gate` / `release_gate` 用真 claim 喂入。族键若在这一层生效, 它是层盲的。
  - a1-entry 侧的相撞面实读: 其 A.1 模板 `--raw-track-id "<spec-slug>-<container_uuid>"` (`a1-entry proposal.md:104`); 其 SC-2 的**负控**逐字是「两串**相同** (模拟容器段被丢弃) ⇒ 双方 overlap **均为空** (`lib/collision.py:278-279` 自排除)」(`:571` 所在 SC 表)。也就是说 a1-entry 把「两串不同」当成其主机制成立的前提并写了负控; 一个层盲的族键归一会同时踩到这个前提。
  - 安全落点是存在的且只有一处: 在 `track_to_claim_record` 里改写 `ClaimRecord.track_id` —— 该函数只被 Layer H 两条路径调用 (`collision.py:347`, `track_board.py:783`), Layer L 的 claim 不经它; 且渲染器 import 的就是同一个函数, 顺带保证 collector/renderer 同源。Spec 只要点名这一处即可关掉整条风险面, 但现在 T9 (`:109`) 只写「track 族键」四个字。
- **不代裁**: 与选项无关 —— 无论 D-0 选 (a) 与否, 这一句都要在 B.1 前写死。

### M-3 (major) S1 形态给出的两条缓解都不成立: ⚪ advisory 结构上不可能覆盖 label 形态; T3b 的「拒绝本次运行 flip」在 S1 无分支可触发、在 S2 跨进程不可实现且无 SC 断言

- **type**: issue
- **severity**: major
- **category**: architecture
- **scope**: `proposal.md:92` (Positive 末句) / `:36` (T3b 语义) / `:95` (S1/S2) / `:102-103` (T3/T3b) / `:117` (SC-3) / `lib/identity.py:222, :242, :266` / `aria/skills/session-closer/scripts/handoff_autofill.py:391`
- **summary**: `:92` 写「S1 形态下由 T3b 检查 + ⚪ 缓解」。⚪ 只对 **uuid** `identity_key` 产出 (`:45`), 而 label 形态产出的恰恰是**非 uuid** 的 `identity_key`, 所以 ⚪ 对该形态结构性沉默。T3b 的动作句「拒绝在本次运行 flip 语义 (走旧口径)」在 S1 下无 flip 可拒 (`get_container_id()` 未改, 旧口径本就是当前行为), 在 S2 下只能约束调用它的那个进程, 管不到写 frontmatter 的 session-closer。
- **evidence**:
  - ⚪ 的产出面逐字 `:45`:「输出每个出现 ≥2 个非空 owner 串的 **uuid** `identity_key`」。label 形态下 container 段 = label ⇒ 按 `:32` 的规则 `identity_key = owner + "/" + label` (非 uuid 形) ⇒ 该 key 不进 advisory。同一台机在 flip 前后表现为 `bfe8285d` 与 `simonfish/<label>` 两个 key ⇒ 计数 ≥2、非空 owner 集合 = 1 ⇒ 判 🟡, **且无 ⚪ 行解释**。这正是 `:92` 声称被缓解的那个形态。
  - S1 下 T3b 的动作分支不可达: `:102` T3 明写「`get_container_id()` uuid 优先 (**S2 才落**)」⇒ S1 的 `get_container_id()` 仍是 `lib/identity.py:222` 的 `return label if label else uuid`。「走旧口径」= 无条件现状, 守卫的 FAIL 分支只能打印告警。参照 memory `feedback_noop_in_test_env_hardening_needs_mechanism_assertion`: 保护分支在交付形态里是 no-op 时, 测试全绿的原因不是机制成立。
  - S2 下跨进程不可实现: flip 改的是 `get_container_id()` 本身, 六处消费方里 `handoff_autofill.py:391` `def owner_container()` 走的是 `lib/identity.py:266 get_identity()` → `get_container_id()`, 而它由 **session-closer 另一个进程**执行。`phase1_gate` 内部「本次运行走旧口径」不可能改变 session-closer 随后写出的 frontmatter ⇒ 迁移窗口内 Layer L 的 claim 目录按 label、Layer H 的 frontmatter 按 uuid, 正是 #135 08-13 孤儿 claim 的形态 —— 守卫制造了它要防的东西。且 `:36` 明确把守卫排除在 `identity.py` 之外 (为保零依赖), 所以也没有一个可传递的抑制开关。
  - SC 覆盖缺口: SC-3 (`:117`) 只断言「输出迁移告警」, **没有一条断言 flip 被抑制**; 因此上一条的不可实现性在 B.2 全绿下不会暴露。
  - 附带的 S1 自洽缺口: SC-3 第一臂 (「S2 形态: `get_container_id()` 返回 uuid」) 在 S1 不可交付, 而 `:96` Rule #6 substitute 把 **SC-3** 无条件列进「每条对当前代码先红」的替代集合。S1 下该替代集合实际缩水一条, Spec 未写。
- **不代裁**: 不建议改选 S1/S2。要求: (a) `:92` 删去或改写「⚪ 缓解」这半句 (它可证伪); (b) T3b 的动作在 S1/S2 下各写一句真实可实现的语义 (S1: 纯 inventory 告警, 无抑制; S2: 抑制的作用域到底是哪几个进程, 或改为「检查不通过则不执行 flip 这次发布」这种发布期闸而非运行期闸); (c) SC-3 分形态标注哪一臂在哪个形态成立。

### M-4 (major) D-3(a) 是四个决策点里唯一「选了就要写代码」却在 Tasks / SC / 渲染器同源三处全零的分支; 而它要落的过滤点恰好是 collector 与 renderer 各写一份的那对镜像

- **type**: issue
- **severity**: major
- **category**: implementation
- **scope**: `proposal.md:83-86` (D-3) / `:98-111` (Tasks 全表) / `:120` (SC-6) / `lib/collision.py:332-338` / `scripts/renderers/track_board.py:743-757, :781-795` / `lib/constants.py:36, :50`
- **summary**: D-0 得到条件任务 T9、D-1/D-2 由 T5 回填规范, 只有 D-3 的 (a) 分支既无 T 也无 SC —— 它在全文只以 SC-6 的一个括注「(D-3(a) 时 0 组)」出现。且它要插入的过滤点在 collector 与 renderer 里是两份并行代码, Spec 未要求同源, 而这对镜像的分叉正是渲染器注释里记着的、已被修过一次的病。
- **evidence**:
  - Tasks 全表实读 (`:100-111`): T1 解析 / T2 判定+advisory / T3 label / T3b 迁移检查 / T4 dedupe 键 / T5 规范 / T6 fixture / T7 消费面 / T8 ⚪ 渲染 / T9 D-0 裁定落地 / T10 回归 / T11 回帖 —— **无一条覆盖新鲜度截止**。T5 只写「§2.3.9 (按 D-1/D-2/D-3 裁定回填)」, 而 §2.3.9 的标题是「AI runner 提交身份」(`:41`), 不是新鲜度截止该住的地方。
  - SC 全表 (`:115-124`) 无「早于 N 天的行不参与判定」的断言; SC-6 的 `(D-3(a) 时 0 组)` 是对**结果计数**的括注, 不断言机制。
  - 插入点实读与「最不侵入」结论: `lib/collision.py:335-338` 的 `collidable = [...]` 列表推导是 `classify()` 里第一个筛子, 记录构造 (`:347-352`) 与 `reconcile_all` (`:361`) 都在其后 ⇒ 在这里加谓词, 被截止的行结构上到不了 `:370-384` 的 stale-winner 捞回, `:84` 承诺的「不叠成三档」成立。这一点核验通过。
  - 但镜像未覆盖: 渲染器有自己的 `all_collidable` (`track_board.py:754-757`) 并自建 ClaimRecords + 自跑 `reconcile_all` (`:781-795`); `collision.py:332-334` 的注释逐字写着「matches track_board.all_collidable filter」—— 两份筛子靠注释保持一致。只在 `classify()` 加截止 ⇒ collector 报 `none`、看板仍画 ⚠ COLLISION 行。渲染器注释 `:158-165` 记的就是这一类分叉「Before this fix the renderer fed the raw, undeduped tracks[] straight into collidability/reconcile……a divergence flagged in round-1 review」。v3 对 ⚪ advisory 已经用「独立 lib 函数, 两处同调」解决了同一问题 (`:45`), D-3(a) 需要同样的一句而现在没有。
  - 常量面: `:84` 只写「新增一个常量 (`lib/constants.py`, 与 `STALE_TTL` 分开命名与量纲)」—— 名字未定、单位未定、是否可配未定。同文件既有 `STALE_TTL = 1800` (`:36`) 与 `SWEEP_TTL = 86400` (`:50`) 都是秒; 若新常量以「天」为单位则打破该文件的隐含单位约定, 若以秒则是第三个易混的 TTL。
- **不代裁**: 不建议 D-3 选哪支。要求: 若 (a) 在可选集合内, 则 Tasks 需要一条条件任务 (与 T9 同形)、SC 需要一条断言截止真的生效 (含「被截止的行不出现在 groups 里」与「渲染器与 collector 同结论」两臂)、并指名截止谓词是共享函数还是两处各写。

### m-1 (minor) D-2 的三个选项里只有 (a)(b) 写了 `cross_owner` 在生产数据上是否可达, (c) 没写 —— 后果表在同一维度上不对称

- **type**: decision
- **severity**: minor
- **category**: documentation
- **scope**: `proposal.md:78` (D-2 (a)) / `:79` (b) / `:80` (c)
- **summary**: R2 M-3 的处置要求是「D-2 的三个选项各自补一句该选项下 `cross_owner` 是否可达」。(a) 写了「结构性不可达」, (b) 写了「两位操作者之间 🔴 可达」, (c)「不规定」只写了「漂移继续, ⚪ 常亮」。(c) 下 owner 段随每次 git 身份变动而变, `cross_owner` 不但可达而且**会被漂移触发**, 这正是本 Spec 立项的病 —— 该后果对 owner 的裁断至关重要, 却缺席。
- **evidence**: `:80` 逐字「(c) **不规定**。收益: 零改动。代价: 漂移继续, ⚪ 常亮」—— 无可达性句; 对照 `:78` 的「`cross_owner` 结构性不可达」与 `:79` 的「两位操作者之间 🔴 可达」。判据本体实读 `lib/collision.py:150-152` (`owners = {c.owner for c in active}`; v3 换成非空非 unknown 的 owner 串集合, 集合来源仍是 owner 段)。

### m-2 (minor) 「同一 uuid 容器上的多个 owner 串 = 同一个工作者的串行工作」是 identity_key 规则的承重假设, 其漏报后果只出现在合成用例行, 未进 Risk 表

- **type**: risk
- **severity**: minor
- **category**: documentation
- **scope**: `proposal.md:32` (身份键) / `:60` (合成用例 `erin`/`frank`) / `:93` (Risk 五条) / `:17` (§Why 病 1 的「漏报」)
- **summary**: `:32` 规定 uuid 形 ⇒ owner 不参与同一性, `:33` 的 dedupe 随之把同容器多 owner 折叠为一行 ⇒ 两个真人在同一台容器上认领同一 track 判 `none`。这是 `:17` 列为要修的那类「漏报」的镜像形态, 靠 ⚪ 缓解但 `kind` 上仍是 `none`。Risk 表五条 (判据变更 / tie-break 退化 / `oc_by_tid_key` 撞键 / 8 位 hex 嗅探 / 漂移期 🔴) 不含它。
- **evidence**: `:60` 合成用例逐字「两人先后共用一机 `erin/eeeeeeee` + `frank/eeeeeeee` → **none** (+ advisory)」—— 结果已写在用例里, 但只作为「预期输出」出现, 未在 Risk/非目标里承认它是一个被接受的漏报; `:17` 把「同人两机 → `none` (漏报)」列为要修的病, 同一个词在两处含义不同。假设本身在采用方并非恒真 (共享构建机 / 两人轮换同一容器)。

### 核验通过、不构成 finding

- **v3 判定链无残余「推断同一人」**: `:31` 解析 / `:32` 身份键 / `:33` dedupe 键 / `:34` 判定四步的输入只有单行的 `track_id` + `owner` + `container` (+ 该 track 内的行集合), 无历史、无共现、无持久状态; `:45` 明写 advisory 不回灌, `:34` 再钉一次「不是判定输入」。唯一的语料依赖是 D-0(a) 的族键子句 (已记 M-1) 与 `:40` 写进 §2.3.5 的 ⚪ 判据 (「同一 `identity_key` 在语料中出现 ≥2 个 `<owner>`」) —— 后者是 advisory 且明示不计入 collision, 本席不记 finding; 但 §2.3.5 落笔时值得加一句「⚪ 集合取决于本机扫到的语料范围」, 免得采用方把「没有 ⚪」读成「没有漂移」。
- **D-2(a) 的 bot 改名一次性漂移确实被 D3 覆盖**: 本容器 container 段是 uuid `bfe8285d` (`:7` claim 行 + `:18` 语料统计), 冻结语料 uuid 形 identity_key 实测为 `{023236f2, bfe8285d, f9c6e8cd}` (`r3_exp1.py`) ⇒ 改名后 `10cg-ci-bot/bfe8285d` 与既有两串同 key、owner 串数 ≥2, 命中 `:45` 的产出条件, ⚪ 会出。`:78` 的「一次性, D3 可解释」成立。
- **D-1/D-2 耦合的呈现方式合规**: `:72` 明写「请一起裁」, 两处执笔建议都带代价句, 未替 owner 决定; Positive `:92` 已把 🔴 的语义条件挂在 (a)+(a) 上。
- **Level 自评诚实**: `:3` 三项逐条对判据 (`standards/core/ten-step-cycle/phase-a-spec-planning.md:128-137` 的流程图与三词表), 结论「判据上是 Level 3」与流程图一致, 维持 Level 2 被明确归为 owner override 而非执笔判断 —— 符合 Rule #10。附注: `breaking = 否` 的三条理由里「§2.3.5 判据变更经 owner 决策点显式裁定」不是判据层论证 (治理动作不改变变更性质), 但因 cross-module 已经把结论钉在 Level 3, 该瑕疵不改变输出; 且 `standards/` 无 VERSION / CHANGELOG (实查目录), 无 semver 下游后果, 故不记 finding。
- **D-3(a) 的插入点可行性**: 见 M-4 evidence 第 3 条 —— `lib/collision.py:335-338` 是能同时满足「不进 reconcile」与「避开 `:370-384` 三档」的最不侵入点, `:84` 的机制描述本身成立; 记为 M-4 的是配套面 (任务 / SC / 镜像 / 常量) 不是该结论。
- **Tasks 头部计数**: `:98` 写「11 个 checkbox」, 实数 12 (T1/T2/T3/T3b/T4..T11)。与 R2 code-reviewer 的同位 minor 同一处, 属 B 期顺手改, 不单列 finding。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 4 Major / 2 minor。

R2 的 1C/7M/2m 无一 open (closed 6 / partial 4)。R2 的 Critical (a1-entry track-id 冲突) 已按「不能在本 Spec 内单方解决 ⇒ 上呈决策点」正确处置, 不再是 Critical。本轮 4 条 Major 全部落在**决策点的实现子句与后果对称性**上, 没有一条要求推翻 v3 的判定模型 —— 模型本身 (纯输入、零推断) 经本轮镜头核验成立。

## Vote

**REVISE**。

四条 Major 都不是「B 期顺手」: M-1 / M-2 改的是 D-0 的选项文本与作用域, 而 Spec 自己写了「D-0 须在 B.1 前裁定」(`:64`) —— owner 拿到的选项现在带一条与全篇原则互斥的实现子句和一个未定的作用域, 在这个状态下裁定即是在半份后果上裁定; M-3 有一句可证伪的缓解声称写在 Positive 里 (⚪ 覆盖 label 形态), 属 memory `feedback_never_write_unverified_impossibility_claims` 的反面形态, 必须在批准前改掉; M-4 决定 D-3(a) 被选中时 B.2 到底建不建、建在哪 —— 现在选它等于选一个没有交付面的分支。

改动量估计小 (四处后果句 + 一条条件任务 + 一条 SC + T9/T3b 各一句作用域), 预期 R4 可收敛。

## 轮次记录

- **R1** (本席): 1C/6M/6m, FAIL/REVISE —— 判定键缺跨容器归并 (C-1) 等。
- **R2** (本席): 1C/7M/2m, FAIL/REVISE —— v2 owner 等价类的四个方向 (假合并 / 语料依赖 / 数据通路 / SOT 假全称) + a1-entry track-id 冲突 (C-1)。
- **R3** (本轮): 0C/4M/2m, PASS_WITH_WARNINGS/REVISE —— Critical 归零 (等价类整段撤销 + 跨 Spec 冲突正确上呈); 剩余全部是决策点的实现子句 (D-0 语料依赖 / D-0 作用域 / D-3 零交付面) 与 ship 形态自洽 (S1 两条缓解不成立)。
- **比较键集合**: 与 R2 无重叠簇 (R2 的承载体已删); 与 R1 无重叠。非振荡 —— 三轮的 finding 集合逐轮收窄 (1C6M6m → 1C7M2m → 0C4M2m), 且本轮 4 条全部指向同一类物 (决策点文本), 属正常收敛路径。
