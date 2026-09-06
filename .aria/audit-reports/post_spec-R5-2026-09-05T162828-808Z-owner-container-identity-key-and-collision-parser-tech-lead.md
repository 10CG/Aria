---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T16:28:28.808Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 (max_rounds, 末轮) — tech-lead 席 (镜头: 稳定性 — v5 定点编辑是否与 R4 PASS 的前提一致)

审计对象: `proposal.md` **v5** (commit `681e872`)。本席只审不改, 未修改任何仓内文件; 复核走 `sed` / `grep` 只读命令, 无产物落盘 (本报告除外)。

## R4 处置核对

逐条对本席 R4 的 m-1..m-5 与 v5 正文比对; 引用行号均为对 v5 现行文件实读所得。

| R4 finding | 三态 | 证据 (实读) |
|---|---|---|
| **m-1** D-0(a) 剥离后 `track_board` 的 `tracks_by_tid` 索引仍用原串 ⇒ 剥离过的 track 查表恒 miss、标签退化 | **partial** | **指令面已闭合三处**: `:35` 作用域句尾新增「渲染器 `tracks_by_tid` 标签索引须用同一剥离后键构造 (T8)」; `:113` T8 新增「D-0(a) 时 `tracks_by_tid` 标签索引改用剥离后键 (与 `verdicts` 键域一致)」; `:98` Risk (7) 新增「渲染器 `tracks_by_tid` 索引若未随剥离归一会退化标签 (T8 锁)」。落笔位置从本席建议的 T9 移到 T8, 更贴切 (T8 才是 `track_board.py` 任务)。**残余**: 断言面为空 —— SC-10 (`:131`) 三臂仍只断 ⚪ 行数 / owners 列 / dedupe 反事实, SC-4 (`:125`) 的 board 臂仍未规定夹具 `track_id` 需 `-8hex` 结尾。R4 写的「D-0(a) 下 B.2 可以全绿而带着这个回归 ship」这一性质**原样存在**, 只是现在有三句 prose 指令挡在前面。 |
| **m-2** SC-3「仅 S2」臂的断言宿主在本仓不存在; 「发布门」与 `release_gate.py` 同词不同义 | **open** | `:124` SC-3 的「仅 S2」臂逐字未变: 「…发布门检查不过时 flip 不进该次发布 (发布脚本/清单断言)」。宿主仍未指名具体物, 「发布门」措辞也未换词。本轮 v5 在 SC-3 上加的是**另一件事** (「仅 S1」lock-in 臂, 见下方核验), 不覆盖本条。 |
| **m-3** SC-6 两处自洽缺口: (前半) D-3(b) 臂引用只在 D-3(a) 存在的常量; (后半) 注入的合成真撞车组与组数断言互斥 | **partial** | **前半 closed**: `:127` 改为「组内全部行 `updated_at` 早于 30 天 (D-3(a) 时读常量 `LAYER_H_ACTIVE_WINDOW_DAYS`; **D-3(b) 时该常量不存在, 归因测试自带 30 天字面只作标签, 此时改后组数为 2 而非 0**)」—— 符号作用域问题消失, 且顺手把 (b) 分支的组数写清。**后半 open**: 同句仍是「改前 A = 1 组 / 改后 = 2 组 (D-3(a) 时 0 组)」+「注入的合成真撞车组必须归入『真撞车』」, 未拆成「基线 fixture」与「注入变体」两句。互斥仍在: 注入组若 fresh, 改后应为 3 组、D-3(a) 下应为 1 组; 若 stale, 则 D-3(a) 下被截止, 「必须归入真撞车」不可满足。 |
| **m-4** D5 版本档位应照 `:3` 体例写成「判据自评 + owner override 回填」, 而非先给结论再附括号 | **partial** | **体例半闭合**: `:54` 从「⇒ 按 `version-management.md` PATCH bump (owner 可因新字段升 MINOR)」改为「判据上 **PATCH**; 但 §2.3.5 对采用方是行为变更, owner 可据此升 MINOR (二选一记入 CHANGELOG)」—— MINOR 那一半现在有了成文理由, owner 拿到的是真二选一, 不再是括号附注。**残余 (且方向相反)**: 改写把 `version-management.md` 的引用**整条删掉**, 只留 CLAUDE.md 的粗判据。本席实读 `standards/conventions/version-management.md` §2.2 MINOR 触发条件四条, 第四条逐字「功能增强（向下兼容）」; §2.3 PATCH 四条逐字为「文档错误修正 / 链接修复 / 小改进 / Bug 修复」。R4 指出的「两条规范在本例给不同答案」这一事实没变, 但 v5 之后 owner 从正文只看得见给出 PATCH 的那一条 —— 张力被隐去而非呈报。 |
| **m-5** D-0(b) 漏写它对「carry-id 与认领串同串」链条的后果 | **closed** | `:72` 新增逐字: 「且 §2.3.8.2「carry-id 与 frontmatter track-id 同串」要求 carry-id 也随之去掉容器段, 与 a1-entry 用 carry-id 喂 `phase1_gate --raw-track-id` 的设计相冲, 对方要连带改 §2.1b」。**实读核验通过**: `session-handoff.md §2.3.8.2` 逐字「当某条 §6 carry-id 与本 handoff doc-level frontmatter `track-id` 指向同一份工作时, 两者取**相同原始串**」; a1-entry `proposal.md:183-196` §2.1b 逐字「A.1 认领时派生的那一串, 即本 cycle 的 carry-id」+ 三处 SKILL.md 逐字节复用 + `--raw-track-id` 消费。⇒ (b) 下 frontmatter 去容器段 ⇒ carry-id 随之去 ⇒ §2.1b 的「A.1 原串即 carry-id」等式断。**且这个解法比本席 R4 的建议更准**: R4 说「需同改 §2.3.8.1/§2.3.8.2 (落在本 Spec D2 面)」, v5 保持 standards 不动、把连带改动落回 a1-entry 侧 —— 这样「本 Spec 零改动」那半句仍为真, 而「零成本」被正确否掉。两种读法在「(b) 不是免费的」这个结论上一致, v5 的更省改动面。 |
| (R4 B 期顺手项 6) Tasks 头部计数 13 → 14 | **closed** | `:103` 现为「14 个 checkbox 含 T3b, 其中 T9 / T13 条件任务」, 与实数 `- [ ]` 14 条一致; 并顺手把 `lib/constants.py` (条件 T13) 加进头部的文件清单。 |

**计数: closed 2 / partial 3 / open 1** (五条 finding 口径: closed 1 / partial 3 / open 1; 另一条 closed 是非 finding 的顺手项)。

## 审计结论

**0 Critical / 0 Major / 4 minor** —— 4 条全部是 R4 五条的残余 (m-1 / m-2 / m-3 后半 / m-4 残余), **本轮零新增 finding**。四条逐条对「B 期可顺手处理」判据成立: 不改判定模型、不改任一决策点的可选集合或主轴后果、有指名落笔位置、不需要 owner 在批准前重裁。下方不重复 R4 已写死的证据链, 只给三态之后的落笔位置与「为何仍是 minor」。

### r-1 (minor, 承 m-1) `tracks_by_tid` 剥离归一有指令无断言 —— B.2 全绿仍可带走该退化

- **type**: issue | **severity**: minor | **category**: testing
- **scope**: `proposal.md:113` (T8) / `:125` (SC-4 board 臂) / `:131` (SC-10) / `:35` / `:98`
- **为何仍 minor**: 条件于 D-0(a); 影响面止于看板标签显示 (collector 侧 `oc_by_tid_key` 用 `rec.track_id` 自洽, snapshot 的 `kind`/`groups` 不受影响); 且 v5 已把这条指令写进三处 prose, B.2 执行者读得到。
- **B 期落笔**: SC-10 补一臂或 SC-4 board 臂夹具 `track_id` 指定 `-8hex` 结尾形, 断「剥离后 board 标签仍解析出 owner/container 而非回退串」。

### r-2 (minor, 承 m-2) SC-3「仅 S2」臂宿主未指名, 「发布门」与 `release_gate.py` 同词不同义

- **type**: issue | **severity**: minor | **category**: testing
- **scope**: `proposal.md:124` (SC-3 仅 S2 臂) / `:38` (T3b S2 语义) / `:100` (两种 ship 形态)
- **为何仍 minor**: S2 是条件 ship 形态 (需 a1-entry B.2 已落地 + #174 ack), 不在 S1 的交付路径上; 且 v5 新加的「仅 S1」lock-in 臂已把 S1 侧的真风险 (偷 flip) 钉死, S2 的宿主问题不阻塞任一可立即执行的分支。
- **B 期落笔** (沿用 R4): 宿主指名为具体物 —— 一条 `.aria/state-checks.yaml` check (「`get_container_id()` 已 uuid 优先 且 coordination ref 里仍存在 label 形 active claim ⇒ FAIL」) 或 T12 发布清单的一条可 grep 项; 「发布门」换词 (如「ship 前置核对」)。

### r-3 (minor, 承 m-3 后半) SC-6 的组数断言未与注入变体拆句

- **type**: issue | **severity**: minor | **category**: testing
- **scope**: `proposal.md:127` (SC-6) / `:111` (T6)
- **为何仍 minor**: 计数是被断言的 —— B.2 一写就红, 取哪种读法都会立刻显形, 无假绿风险; 前半 (符号作用域) 已闭合, 剩的是一句话拆分。
- **B 期落笔**: 把 `:127` 的「改前 A = 1 组 / 改后 = 2 组 / D-3(a) 时 0 组」限定为「**基线 fixture (未注入)**」, 注入变体另起一句给其自己的三个数。

### r-4 (minor, 承 m-4 残余) D5 只呈报了给出 PATCH 的那条规范, `version-management.md` 的 MINOR 判据被删而非并陈

- **type**: decision | **severity**: minor | **category**: documentation
- **scope**: `proposal.md:54` (D5) / `:3` (Level 自评体例) / `standards/conventions/version-management.md` §2.2 / §2.3
- **判据 (实读, 不代裁)**: `version-management.md` §2.2 MINOR 四条含逐字「功能增强（向下兼容）」; §2.3 PATCH 四条为「文档错误修正 / 链接修复 / 小改进 / Bug 修复」。本 Spec 落 MINOR 侧的交付物 (取自 v5 自身正文): 新公开函数 `identity_drift_advisories(tracks)` (`:47`)、新公开 accessor `get_container_label()` (`:37`)、新持久化字段 `collision.identity_advisories[]` + schema additive bump、新判据类 `same-identity-multi-owner` ⚪、新看板 ⚪ 渲染段 (`:113`); D-3(a) 时再加常量与谓词。落 PATCH 侧的是解析器 bug 修复本身。CLAUDE.md 的粗判据 (无新 Skill ⇒ PATCH) 与之给出不同答案, 这正是该由 owner 显式裁一次的形态。
- **为何仍 minor**: v5 已给出真二选一与升 MINOR 的理由, owner 有裁定钩子; 差的是把另一条 SOT 的判据摆回台面。**但请注意方向**: 这一处 v5 的编辑**减少**了 owner 可见的判据面, 是本轮唯一一处「改后信息量下降」的编辑。
- **B 期落笔**: D5 补一句「按 `version-management.md` §2.2/§2.3 判据自评 = MINOR (逐项列上述 additive 面); 按 CLAUDE.md 粗判据 = PATCH; owner 二选一并回填」, 与 `:3` 的 Level 自评体例齐平。

### 稳定性核验 (镜头 1, 通过, 不构成 finding)

- **判定模型未动**: `:33` 的 `classify_claims` 判定句 (identity_key 计数 / 非空非 `unknown` owner 集合 / 无「同一个人」推断) 在 v4→v5 diff 中是**上下文行**, 零 `+`/`-`。身份键 `:32` 与 dedupe 键 `:33` 同样未被触碰。⇒ 「纯输入确定性判定」自 v3 起四版未变, 与 v5 Status 行的自述一致。
- **决策点集合未动**: diff 触及的 hunk 逐个点名为 —— 标题 Status / D1 族键作用域 / D2 §2.3.1 限定 / D4 模板句 / D5 版本档位 / D-0(b) 后果 / Risk 表 / Tasks 头 / T6 / T8 / SC-2 / SC-3 / SC-5 / SC-6 / SC-9 / SC-11 / References 代码行。**D-1 / D-2 / D-3 三个决策点整段零 diff**; D-0 只有 (b) 的后果句被**加长**, (a)(c)(d) 三条逐字未变。⇒ 无任一选项的主轴后果被改写或删除。
- **新增作用域限定句准确**: `:35` (D1) 与 `:26` (D2 §2.3.1) 的三条限定 —— 不改 frontmatter 原串 / 不影响 §2.3.8.2 carry-id 同串 / 不用于 Layer L claim 匹配 —— 与 R4 已实读核验的结构事实一致 (`track_to_claim_record` 全仓仅 `collision.py:349` 与 `track_board.py:783` 两个调用点, Layer L 侧 `phase1_gate.py` / `release_gate.py` 走 `read_claims` / `release_claim_by_track` 不经它)。`:130` SC-5 顺手把这句上了机械锁 (「§2.3.1 的尾段句 (D-0(a) 时) 含 token `仅用于` 与 `§2.3.8.2`」), 使该限定不是纯口头承诺。
- **SC-3 新增「仅 S1」lock-in 臂无内部矛盾**: 「仅 S1: `get_container_id()` 在 label 非空时**仍**返回 label」与「仅 S2: `get_container_id()` 返回 uuid」由 ship 形态互斥门控, 不会同时被断言; 它堵的是「S1 偷 flip 使 a1-entry SC-3 静默恒绿」这条真通道, 是本轮质量上最实的一处加固。
- **D4 新增的模板删除动作有真实目标 (非幻影任务)**: 实读 `aria/templates/session-handoff.md:43` 逐字含 `"simonfish/bfe8285d"  (label 空 → uuid; 设 label 使更可读)` ⇒ v5 `:34` 要删的那句鼓励句确实存在, 且确实会在 S1 窗口期把用户引向 label 形。
- **SC-9 改写自洽**: 新判据「每个文件 F 与 token 集的交集不为空」附带断言「`RECOMMENDATION_RULES.md:31` 今日无取值字面」—— 实跑 `grep -cE "cross_owner|self_multi_container|identity_advisories"` 该文件得 **0**, 断言为真; `:31` 实读为 rule 1.54 行, 判据写作 `collision.kind != none` 而非取值字面, 与之吻合 ⇒ 旧版「各至少命中一次」的恒红隐患解除, 新版不制造恒绿真空 (交集非空仍需 T7 真加一句)。
- **行号面 ±1 漂移一处** (不单列 finding): `:150` References 新写「stale 捞回 `:374-379` 注释 / `:379-383` 代码」; 实读 `collision.py` 该处注释块为 **370-378**, `:379` 起是代码 (`active_claims: list[ClaimRecord] = list(verdict.yielders)` 至 `:383`)。代码那半准确, 注释那半尾端多含 1 行。Spec `:100` 已成文「行号漂移: 后落地方在 D 期 refresh」, 归该条治理。

## Verdict

**PASS** — 0 Critical / 0 Major / 4 minor。

理由: R4 五条中 1 条真闭合 (且闭合方式比本席建议更省改动面并经实读核验)、3 条部分闭合、1 条未动; **无一条在 v5 中被改坏, 无新增 finding**。四条残余全部是断言粒度与呈报体例, 没有一条触及判定模型 (纯输入 / 零推断)、决策点的可选集合、或任一选项的主轴后果 —— 后三者在 v4→v5 的 diff 中逐 hunk 核验为零变动。

**唯一需要 owner 在批准时看一眼的是 r-4**: 它是本轮唯一一处「改后 owner 可见判据面下降」的编辑 (`version-management.md` 判据被删)。这不影响交付物正确性, 只影响版本号那一位数字的裁定输入, 且 D5 已留二选一钩子 ⇒ 记 minor, 不升 Major。

## Vote

**PASS**。

对照「为何不需要再开轮」(本轮已是 max_rounds, 此处论证的是「即使有第 6 轮也不值得」):

1. **收敛已到底**: R4→R5 的 finding 集合是 R4 的**子集** (4 ⊂ 5), 零新增。这是收敛的终态形态 —— 再开一轮的期望产出是这 4 条继续往 closed 走, 而它们全部已有写死的落笔位置, B 期直接消费即可, 不需要审计轮次这个载体。
2. **无 owner 裁定风险**: 四个决策点的选项集合与主轴后果三轮 (v3/v4/v5) 未动, R5 逐 hunk 复核确认 v5 没有暗中改动任何一条。owner 在半份后果上裁定的风险不存在。r-4 是呈报面, 已在本报告写清两条规范的判据全文, owner 读本报告即补齐。
3. **残余的暴露成本低于再审成本**: r-3 一写测试就红; r-1/r-2 是条件分支上的锁缺口, 且 r-1 已有三处 prose 指令兜; r-4 是一句话。四条合计约 5 行编辑。

**B 期顺手项清单** (按落笔位置, 4 条):

1. SC-10 补一臂 (或 SC-4 board 臂夹具指定 `-8hex` 结尾形), 给 `tracks_by_tid` 剥离归一上断言锁 (r-1)。
2. SC-3「仅 S2」臂宿主指名为具体物 (`.aria/state-checks.yaml` 新 check 或 T12 清单可 grep 项), 并把「发布门」换词以免与 `release_gate.py` 混读 (r-2)。
3. SC-6 的组数三个数限定为「基线 fixture (未注入)」, 注入变体另起一句 (r-3)。
4. D5 补回 `version-management.md` §2.2/§2.3 判据自评那一半, 与 `:3` 体例齐平 (r-4)。

(附: `:150` References 的注释行号 374-379 → 370-378, 归 Spec 自己的 D 期行号 refresh 条款, 不单列。)

## 轮次记录

- **R1** (本席): 1C/6M/6m, FAIL/REVISE —— 判定键缺跨容器归并 (C-1) 等。
- **R2** (本席): 1C/7M/2m, FAIL/REVISE —— v2 owner 等价类四方向 + a1-entry track-id 冲突 (C-1)。
- **R3** (本席): 0C/4M/2m, PASS_WITH_WARNINGS/REVISE —— Critical 归零; 剩决策点实现子句与 ship 形态自洽。
- **R4** (本席): 0C/0M/5m, PASS/PASS —— R3 全 closed; 剩 renderer 索引键 / SC 宿主与内部计数 / 版本档位与决策后果呈报体例。
- **R5** (本轮, max_rounds): 0C/0M/4m, PASS/PASS —— R4 的 closed 2 / partial 3 / open 1, **零新增**; 剩余 4 条全为 R4 残余。
- **比较键集合**: 与 R4 是**子集关系** (无新键, 无旧键复开); 与 R3/R2/R1 零重叠。**非振荡** —— 五轮 finding 集合单调收窄 (1C6M6m → 1C7M2m → 0C4M2m → 0C0M5m → 0C0M4m), 严重度上限逐轮不升 (Critical → Critical → Major → minor → minor)。R4 曾出现的 minor 数回升 (2→5) 在本轮回落且无新增, 确认那次回升是 rework 下游漂移而非振荡, 事后成立。
