---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T15:50:52.857Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — tech-lead 席 (镜头: 稳定性核查 — v4 是否已收敛到「只剩 B 期可顺手处理的 minor」)

审计对象: `proposal.md` **v4** (commit `addc8a1`)。本席只审不改, 未修改任何仓内文件; 复核脚本走 `python3 -c` 一次性执行, 未落盘产物到仓内。

## R3 处置核对

逐条对本席 R3 报告的 M-1..M-4 / m-1 / m-2 与 v4 正文比对; 可机械验证的实跑复核, 代码断言实读行号。

| R3 finding | 三态 | 证据 (实读 / 实跑) |
|---|---|---|
| **M-1** D-0(a) 族键「仅当该 8hex 是语料中出现过的 identity_key」把语料依赖装回判定键 | **closed** | v4 `:35` 改为「对 `ClaimRecord.track_id` 做**纯形状**剥离: 尾段匹配 `-[0-9a-f]{8}$` 即剥。**行内确定, 不查语料**」; `:71` 的 (a) 后果句同步改写。本轮对冻结语料重跑纯形状变体复核 v4 写下的三个数字, 逐字一致: 996 行 / 117 个 distinct `track_id` / 形状命中恰 1 个 (`aria-plugin-113-gate-result-yaml-20260719`) / 剥后合并组 `{}` (零合并)。已知限制 (日期形尾段被剥) 进 `:35` 正文 + `:98` Risk (7) + SC-2 反例夹具。 |
| **M-2** 族键落点未指名 (三个 `track_id` 分组点), 落错会改到 Layer L 仲裁 | **closed** | v4 `:35` 指名「在 **`track_to_claim_record` 一处**」并写「Layer L claim 不经它」。实读核验该断言为真: `grep -n track_to_claim_record` 全仓只有两个调用点 —— `lib/collision.py:349` 与 `scripts/renderers/track_board.py:783`, 两者 import 同一函数 (`track_board.py:108` / 兜底 `:133`); Layer L 侧 `scripts/phase1_gate.py` 与 `scripts/release_gate.py` 走 `read_claims` / `release_claim_by_track`, 不经该函数。⇒ 族键结构上到不了 Layer L 仲裁与 `linked_issue_overlaps`。**残余**: 落点周边的 tid 级索引未覆盖 (本轮 m-1, 不是本条未闭合)。 |
| **M-3** S1 两条缓解不成立 (⚪ 结构上覆盖不到 label 形态; T3b「拒绝本次运行 flip」不可实现) | **closed** | 可证伪的缓解句已删并反向写死: `:97` Positive 现为「**label 陷阱结构性消除只在 S2 形态成立**; S1 形态下 label 形态**既无 flip 也无 ⚪** (⚪ 只对 uuid key), 只有 T3b 的 inventory 告警」。T3b 重定义为两态 (`:38`): S1 = 纯 inventory 告警、**无抑制**; S2 = 发布前置而非运行期开关, 并逐字承认「静态语义无法按进程『拒绝』」。SC-3 (`:124`) 拆「S1/S2 共同」与「仅 S2」两臂; Rule #6 substitute 集 (`:101`) 同步标注「SC-3 (S1 臂; flip 臂仅 S2)」。**残余**: S2 臂的断言宿主 (本轮 m-2)。 |
| **M-4** D-3(a) 零交付面 (Tasks / SC / collector-renderer 同源 / 常量四处全空) | **closed** | 四处全部补齐: 条件任务 T13 (`:118`) 给出共享谓词 `layer_h_is_fresh(row, now, days)` + 常量 `LAYER_H_ACTIVE_WINDOW_DAYS` (与 `STALE_TTL` 分名分量纲) + 「collector/renderer 同一调用」; SC-11 (`:132`) 三臂断言「被截止的行不出现在 groups 任一组」「两处同结论」「谓词只有一个实现 (grep 断言无第二份)」。`:89` 的机制描述 (记录构造阶段截止, 不与 `:374-379` 叠成三档) 与 R3 核验过的插入点一致。 |
| **m-1** D-2(c) 缺 `cross_owner` 可达性句 | **closed** | `:85` 现为「`cross_owner` 可达但**不可解释** (每次身份变动都可能制造一次 🔴, 无法区分真撞车与漂移)」, 三选项在同一维度上齐了。 |
| **m-2** 「两人同机同 track → none」漏报镜像未进 Risk | **closed** | `:98` Risk (6) 逐字收录:「**两个真人在同一 uuid 容器上认领同一 track → `none`** (owner 不参与同一性的镜像漏报), 只有 ⚪ 提示」。 |

**计数: closed 6 / partial 0 / open 0。** R3 的 4 条 Major 全部真闭合, 且闭合动作没有引入新矛盾 (T3b 两态与 SC-3 两臂互相对齐; 族键落点与 Layer L 隔离经代码核验成立)。

## 审计结论

0 Critical / 0 Major / 5 minor。以下五条全部满足「B 期可顺手处理」判据: 不改变判定模型、不改变任一决策点的可选集合或其主轴后果、有指名的落笔位置、且不需要 owner 在批准前重裁。

### m-1 (minor) D-0(a) 族键剥离后, `track_board` 的 **tid 级**索引与展示 tid 仍用原串 —— 剥离生效的是同一个函数, 但函数外那张按 `track_id` 建的表没跟着归一

- **type**: issue
- **severity**: minor
- **category**: implementation
- **scope**: `proposal.md:35` (「Layer H 两条路径…同源」) / `:36` (board 标签只点名 `track_board.py:412-417`) / `:114` (T9) / `:125` (SC-4) / `scripts/renderers/track_board.py:336, :410, :789-793` / `lib/collision.py:345-356`
- **summary**: v4 把剥离放进 `track_to_claim_record` 是对的 —— 两个调用点共享同一函数, 所以**调用**这一面确实同源 (M-2 已闭合)。但 `track_board` 在调用点旁边另建了一张 `tracks_by_tid`, 键取的是**原始** `t.get("track_id")`; `verdicts` 的键在剥离后是**剥后**串。两把键不同源 ⇒ 剥离过的 track 在渲染时查表恒 miss。
- **evidence**:
  - `track_board.py:789-793` 逐字建表: `for t in all_collidable: tid = t.get("track_id") or ""` → `tracks_by_tid.setdefault(tid, []).append(t)`; 紧接着 `:795` `verdicts = reconcile_all(claim_records, now=now)` —— `claim_records` 来自 `:783` `_track_to_claim_record(t)`, 即剥后串。
  - 查表侧 `:410` `for t in (tracks_by_track_id.get(tid) or []):` (形参 `:336`), `tid` 来自 `verdicts` 的键 ⇒ 剥后串查原串表 → 空 → `oc_by_key` 空 → `_label()` 回退到 `f"{claim.owner}/{claim.container}/{claim.session}"`。在 T1 两段式解析下 session 为空、`track_to_claim_record` 归一为 `"unknown"` ⇒ 板上显示 `simonfish/bfe8285d/unknown`, 正是 SC-4 (`:125`) 声称要修的「board 对两段式串回显原串」那一类失配的另一半。附带: `display_tid` 显示剥后串, 与上方可视表格里逐行渲染的原串对不上。
  - 对照面: `lib/collision.py:345-356` 的同名索引 `oc_by_tid_key` 用的是 `rec.track_id` (剥后), 与 `:376` 的查表键同源 ⇒ collector 侧自洽, **只有 renderer 侧分叉**。这正是 `track_board.py:158-165` 注释里记着的、已被修过两次的 collector/renderer 分叉病的同形复发面。
  - 现有 SC 抓不到: T9 的三条夹具 (`:114`) 断的是**分组**; SC-4 的 board 臂 (`:125`) 没规定夹具 `track_id` 需以 `-8hex` 结尾。⇒ D-0(a) 下 B.2 可以全绿而带着这个回归 ship。
- **为什么记 minor 而非 Major**: 条件于 D-0(a); 不改变 owner 在 D-0 上看到的任何后果 (可达性、已知限制、跨 Spec 依赖三条主轴不变); 持久化 snapshot 的 `kind`/`groups` 不受影响 (collector 侧自洽), 影响面止于看板显示; 修法是一处一行 (建 `tracks_by_tid` 时用同一剥离结果) + 一条 SC 臂。
- **B 期落笔**: T9 补一句「`track_board` 的 `tracks_by_tid` 建表键与 `display_tid` 同用剥后串」; SC-4 board 臂的夹具 `track_id` 指定为 `-8hex` 结尾形。

### m-2 (minor) SC-3「仅 S2」臂的「发布脚本/清单断言」在本仓没有宿主; 且「发布门」与既有 `release_gate.py` 同词不同义

- **type**: issue
- **severity**: minor
- **category**: testing
- **scope**: `proposal.md:38` (T3b S2 语义) / `:108` (T3b) / `:124` (SC-3 仅 S2 臂) / `scripts/release_gate.py:1-30, :132-134` / `.aria/state-checks.yaml`
- **summary**: S2 语义本身经核验是**可实现的** (见证据 1), R3 M-3 的方向性问题已解决。剩下的是验证握把: SC-3 用「(发布脚本/清单断言)」指认宿主, 而本仓不存在发布脚本 —— 发布同步面是 CLAUDE.md 文档流程 + 主仓 custom check 兜底。另有一处易混: T3b 把检查挂到 `release_gate.py`, 而该文件的自我定义是「Layer L claim 释放 CLI」, 与 S2 语义里的「发布门」(aria-plugin 发版前置) 不是一回事。
- **evidence**:
  - 可实现性核验通过: `release_claim_by_track` 的签名 (`lib/claim_lifecycle.py:377-384`) 第三形参就是 `identity: Optional[Identity] = None`, 而 `release_gate.py:132-134` 今天只传 `raw_track_id/status/repo_path/now` ⇒ v4 写的「import identity + `get_container_label()` + `read_claims` 枚举 + 传 `identity=` 覆盖」逐项对得上真代码 (R3/BA-M7 的闭合成立)。`read_claims` 读的是共享 coordination ref, 所以「发版机上跑一次就能看见别的容器还在用 label 形」在机制上成立。
  - 宿主缺位: 仓内 `find -name "*release*"` 只命中 `aria/release-notes` / `docs/release-notes-*.md` / 审计报告, 无发布脚本。机械发布面是 `.aria/state-checks.yaml` 的 14 条 custom check (实数 14 条 `- name:`, 与 SC-7 `:128` 写的「主仓 14 state-check」一致), 其中 `m6-version-badge-match` (`:88`) 就是同形的「发版同步没做完就红」探针。
  - 同词不同义: `scripts/release_gate.py:2` 自述「Layer L claim 释放 CLI …把本 cycle 的 carry-id 对应 claim 标记 terminal」。
- **B 期落笔**: SC-3 的 S2 臂把宿主指名为具体物 (建议: 新增一条 `.aria/state-checks.yaml` check —— 「`get_container_id()` 已 uuid 优先 且 coordination ref 里仍存在 label 形 active claim ⇒ FAIL」, 或写成 T12 发布清单的一条可 grep 项); 并把 S2 语义换个词 (如「ship 前置核对」) 以免与 `release_gate.py` 混读。

### m-3 (minor) SC-6 的两处自洽缺口: D-3(b) 臂引用了只在 D-3(a) 才存在的常量; 注入的合成真撞车组与该 SC 自己的组数断言互斥

- **type**: issue
- **severity**: minor
- **category**: testing
- **scope**: `proposal.md:127` (SC-6) / `:111` (T6) / `:118` (T13 条件任务) / `:89` (D-3(a))
- **summary**: SC-6 的机械归因判据以 `LAYER_H_ACTIVE_WINDOW_DAYS` 为阈值, 并注明「D-3(b) 时仍用此值只作标签」; 但该常量由**条件任务 T13** 引入, 而 T13 只在 D-3(a) 执行 ⇒ (b) 分支下这个符号没有定义。另一处: 组数断言与注入样本无法同时满足。
- **evidence**:
  - `:118` 逐字: 「T13 (条件, D-3(a)) `layer_h_is_fresh` 共享谓词 + `LAYER_H_ACTIVE_WINDOW_DAYS` 常量 + …」; `:127` 逐字: 「组内全部行 `updated_at` 早于 `LAYER_H_ACTIVE_WINDOW_DAYS` (缺省 30, **D-3(b) 时仍用此值只作标签**)」。两句只在 D-3(a) 下相容。
  - 组数臂: `:127` 写「改前 A = 1 组 / 改后 = 2 组 (D-3(a) 时 0 组)」, 同一条 SC 又要求「注入的合成真撞车组必须归入『真撞车』」, 而 T6 (`:111`) 把注入描述为对同一份 fixture 做的动作。若注入行是 fresh 的: 改后应为 3 组、D-3(a) 下应为 1 组 (不是 0); 若注入行是 stale 的: D-3(a) 下它被截止掉, 「必须归入真撞车」不可满足。两种读法都与写下的数字冲突。
- **为什么记 minor**: 两处都会在 B.2 写测试时立刻显形 (计数是被断言的, 取错读法即红), 无假绿风险; 修法是把常量声明移出条件任务 (或在 T6 的测试内定义本地阈值), 并把「基线 fixture 的组数」与「注入变体的组数」拆成两句。

### m-4 (minor) T12/D5 的 PATCH 定性与 standards 自身的 MINOR 判据不对齐 —— 建议照 `:3` 的 Level 自评体例写成「判据 vs owner override」, 而不是先给结论再附一句括号

- **type**: decision
- **severity**: minor
- **category**: documentation
- **scope**: `proposal.md:54` (D5) / `:117` (T12) / `:3` (Level 自评体例) / `standards/conventions/version-management.md:49-80` / `CLAUDE.md §版本管理`
- **summary**: 本席不替 owner 定版本档位, 只给判据与两条规范之间的张力。v4 写「本 Spec 是 bug 修复 + additive 字段 ⇒ 按 `version-management.md` PATCH bump (owner 可因新字段升 MINOR)」, 但该 SOT 的 MINOR 触发条件里就有「**功能增强 (向下兼容)**」, 而本 Spec 的交付面正是一组向下兼容的新增能力。
- **判据 (实读 SOT, 不代裁)**:
  - `version-management.md:49-62` MINOR 触发条件四条, 第四条逐字「功能增强（向下兼容）」; `:64-72` PATCH 触发条件四条逐字为「文档错误修正 / 链接修复 / 小改进 / Bug 修复」。
  - 本 Spec 落在 MINOR 侧的交付物 (全部来自 v4 自身正文): 新公开函数 `identity_drift_advisories(tracks)` (`:47`)、新公开 accessor `get_container_label()` (`:37`)、新持久化字段 `collision.identity_advisories[]` + schema additive bump (`:47`/`:106`)、新判据类 `same-identity-multi-owner` ⚪ (`:42`)、新看板 ⚪ 渲染段 (`:113`); D-3(a) 时再加一个新常量与新谓词 (`:118`)。落在 PATCH 侧的是解析器 bug 修复本身。
  - 反向张力 (owner 需要看到的另一半): CLAUDE.md §版本管理的 Aria 粗判据是「新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH」—— 本 Spec 无新增 Skill, 按这条读得出 PATCH。两条规范在本例上给出不同答案, 这本身就该由 owner 显式裁一次。
- **B 期落笔**: 把 D5 改成与 `:3` 同体例的一句「按 `version-management.md:49-72` 判据自评 = MINOR (逐条列上面五项 additive 面); owner 维持 PATCH 即显式 override, 请在批准时回填」。

### m-5 (minor) D-0 的选项后果在一处不对称: (b) 漏写它对 §2.3.8.1/§2.3.8.2「carry-id 与认领串同串」链条的后果

- **type**: decision
- **severity**: minor
- **category**: documentation
- **scope**: `proposal.md:70-75` (D-0 全表) / `standards/conventions/session-handoff.md §2.3.8.1 (id 字段行) / §2.3.8.2 (:234)`
- **summary**: 镜头要求核对 D-0 四选项是否对称穷尽。(a)(c)(d) 三条的后果句本席核验为公平陈述; (b) 少一条后果 —— 它不只是「依赖对方返工」, 它还会拆掉 standards 里另一条已成文的同串约束。
- **evidence**:
  - (b) 逐字 (`:72`):「请 a1-entry 把容器段留在 claim raw id, **不写进 frontmatter `track-id`** …后果: 本 Spec 零改动, 依赖对方返工。」
  - 但 §2.3.8.1 的 `id` 字段定义逐字是「稳定 slug, **喂 Layer L 认领闸门的 `raw_track_id`**」, §2.3.8.2 (`:234`) 又要求 carry-id 与 frontmatter `track-id` 取**相同原始串**。两条串起来 ⇒ frontmatter `track-id` = carry-id = 认领用的 `raw_track_id`。(b) 让 claim raw id 保留容器段而 frontmatter 不保留, 这条等式即断, 需要同时修 §2.3.8.1 或 §2.3.8.2 —— 而这个改动落在**本 Spec 的 D2 交付面**上 (standards 侧), 不是「本 Spec 零改动」。
  - 另三条核验通过: (a) 的后果三句 (规范多一句 / 日期形尾段被剥 / 两容器认领同一 Spec 时 Layer H 仍可报) 与本席实跑一致; (c) 的「只剩接棒功能」与 Layer L overlap 分工陈述准确; (d) 的「范围膨胀到 40+ 任务」经核实为保守真值 —— a1-entry 的 `tasks.md` 实数 40 个 checkbox, 加本 Spec 的 14 个即 54, 「40+」成立且不夸大。
- **B 期落笔**: (b) 的后果句补一句「且需同改 §2.3.8.1/§2.3.8.2 的同串约束 (落在本 Spec 的 D2 面), 非零改动」。

### 反事实与稳定性核验 (通过, 不构成 finding)

- **族键剥离不会弄红 a1-entry 自己的 SC** (镜头 2(a)): 剥离只发生在 `track_to_claim_record` 产出的 `ClaimRecord.track_id` 上, frontmatter 原串与 claim raw id 都不动。逐条对 a1-entry 的断言核验: 其 **SC-2** 钉的是 `linked_issue_overlaps` 经 CLI 的行为 —— 该路径是 `phase1_gate` → `derive_track_id(raw)` → 写 claim → `read_claims` → `linked_issue_overlaps(claims, own_track_id, …)`, 全程不经 `track_to_claim_record`, 其负控「两串相同 ⇒ 双方 overlap 均为空 (`lib/collision.py:278-279` 自排除)」赖以成立的「两串不同」前提在 Layer L 上原样保留; 其 **SC-3** 是 `get_container_uuid()` 的 accessor 单测 (与族键无关, 受影响的是 flip, 已由 S1/S2 + #174 ack 治理); 其 **SC-22** 是文本层。⇒ v4「只落 `track_to_claim_record` 一处」这个收窄, 正是让反事实为负的原因。
- **advisory 的 legacy 排除口径无隐患**: `:47` 用 `owner_container == "unknown"` 定义 legacy 行不参与。实读 collector (`handoff_multibranch.py:638-644, :680-686`) 确认两个 legacy 分支都硬写 `"owner_container": "unknown"` ⇒ 两个谓词由构造同延, 不存在「status 是 legacy 但 owner_container 可归属」的漏网行。
- **T2 点名改写的两条测试确为全部**: `grep` 全测试目录, 锁死 collector 层 collision 键集的断言恰两处 —— `tests/test_collision.py:274` (`set(coll.keys()) == {"kind", "groups"}`, 属 `test_real_collector_emits_cross_owner_collision`) 与 `:290` (`coll == {"kind": "none", "groups": []}`, 属 `test_real_collector_no_collision_is_none`), 与 v4 `:106` 点名的两条逐字一致。`test_collision.py` 里另外 6 处 `== {"kind": "none", "groups": []}` 断的是 `classify()` 的返回值, 而 `:47` 明写 `classify()` 签名不变、新字段由 collector 写入 snapshot ⇒ 那 6 处不受影响, SC-7「点名改写后零回归」与 SC-8「恒存在」不再互斥 (R3/QA-M5 闭合成立)。
- **行号面**: `handoff_multibranch.py:522` (dedupe 键) / `:709` (dedupe 调用) / `claim_lifecycle.py:377` / `track_board.py:783, :744` 逐个实读命中; `collision.py:347` 指的是 `for t in collidable:` 循环头 (调用在 `:349`), `track_board.py:412-417` 指的是 `oc_by_key` 建表段 (实际 `:409-415`) —— ±2 行的漂移, v4 `:100` 已写「行号漂移: 后落地方在 D 期 refresh」, 不单列。
- **Tasks 头部计数** (`:103` 写「13 个 checkbox」, 实数 14 个 `- [ ]`: T1/T2/T3/T3b/T4..T13): 与 R3 同位的顺手项, 归入下方 B 期清单, 不单列 finding。

## Verdict

**PASS** — 0 Critical / 0 Major / 5 minor。

R3 的 4 条 Major + 2 条 minor 全部 closed (0 partial / 0 open), 且闭合动作经代码核验没有引入新矛盾: 族键落点与 Layer L 的隔离是**结构性**的 (只有两个调用点, Layer L 不经该函数), T3b 两态与 SC-3 两臂互相对齐, D-3(a) 的四处交付面补齐。本轮 5 条 minor 没有一条触及判定模型 (纯输入、零推断)、决策点的可选集合、或任一选项的主轴后果 —— 它们分别是一处 renderer 索引键、一处 SC 宿主指名、一处 SC 内部计数与符号作用域、一处版本档位判据体例、一处决策选项后果补句。

## Vote

**PASS**。

理由 (对照「为何不再需要一轮」): 本轮无 Major, 因此不存在「owner 在半份后果上裁定」的风险 —— 四个决策点的选项集合、后果主轴、以及执笔建议都已稳定 (v4 相对 v3 只改落点与判据精度, 判定模型三轮未动)。五条 minor 全部有指名的落笔位置且都不需要重新征求 owner 意见 (m-4/m-5 是**呈报方式**的补句, 不改变可选集合本身)。继续开轮的边际收益低于 B.1 前多一次 rework 的成本; 本报告已把五条的落笔位置写死, B 期可直接消费。

**B 期顺手项清单** (按落笔位置):

1. T9 补一句: `track_board` 的 `tracks_by_tid` 建表键与 `display_tid` 同用剥后串; SC-4 board 臂夹具 `track_id` 指定为 `-8hex` 结尾形 (m-1)。
2. SC-3 的「仅 S2」臂指名断言宿主 (新增一条 `.aria/state-checks.yaml` check 或 T12 清单可 grep 项), 并把「发布门」换词以免与 `release_gate.py` 混读 (m-2)。
3. `LAYER_H_ACTIVE_WINDOW_DAYS` 的声明移出条件任务 T13 (或 SC-6 在测试内定义本地阈值); SC-6 的组数断言拆成「基线 fixture」与「注入变体」两句 (m-3)。
4. D5/T12 改成与 `:3` 同体例的「判据自评 = MINOR + owner override 回填位」(m-4)。
5. D-0(b) 后果补一句「需同改 §2.3.8.1/§2.3.8.2 同串约束, 非零改动」(m-5)。
6. `:103` Tasks 头部计数 13 → 14 (实数 `- [ ]` 14 条)。

## 轮次记录

- **R1** (本席): 1C/6M/6m, FAIL/REVISE —— 判定键缺跨容器归并 (C-1) 等。
- **R2** (本席): 1C/7M/2m, FAIL/REVISE —— v2 owner 等价类四方向 + a1-entry track-id 冲突 (C-1)。
- **R3** (本席): 0C/4M/2m, PASS_WITH_WARNINGS/REVISE —— Critical 归零; 剩余为决策点实现子句 (D-0 语料依赖 / D-0 作用域 / D-3 零交付面) 与 ship 形态自洽 (S1 两条缓解不成立)。
- **R4** (本轮): 0C/0M/5m, PASS/PASS —— R3 全 closed; 剩余为 renderer 索引键 / SC 宿主与内部计数 / 版本档位与决策后果的呈报体例。
- **比较键集合**: 与 R3 零重叠 (R3 四簇的承载文本全部改写, 无一复发); 与 R2/R1 零重叠。**非振荡** —— 四轮 finding 集合单调收窄 (1C6M6m → 1C7M2m → 0C4M2m → 0C0M5m), 且严重度上限逐轮下降 (Critical → Critical → Major → minor); 本轮 minor 数回升不构成振荡: 它们全部指向 v4 的**新增文本** (T9/T13/SC-3/SC-6/T12 五处 rework 产物), 是 rework 下游漂移的常见形态, 无一条是被判过 closed 的旧簇重开。
