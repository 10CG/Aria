---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-23T11:30:00.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 (重写 v2 + C1/C2 落版) — knowledge-manager

> **席位**: knowledge-manager · **处置**: **REVISE** (frontmatter `verdict` 按 `verdict-format.md` 机械映射填 `FAIL` —— ≥1 Critical; post_spec `blocking: false`, 仅记录不阻断, 与 R2/tech-lead 同一映射惯例对齐)
> **counts**: critical=**2** · major=**6** · minor=**1** · `scope_ok`: **true**
> **timestamp**: 1787481000000

## 审计对象与工作树

- 主仓 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` @ **`1205ec3`** (HEAD, 475 行)。
- `aria` 子模块工作树 @ **`cb6bd5d`**（分支 `fix/issue-batch-149-151-155-134`；`git status --short` 显示 `state-scanner/references/rules/operations.md` 等 6 个文件的未提交修改 + 1 个新测试文件 — 均属并行任务 #149/#151/#155 的正常在制状态, 与本次审计对象无交集, 不视为异常）。
- `origin/master`（aria）已实测 fetch 至 **`ca52d1c`**（v1.67.0, 含 `linked-issue-normalization` 合并, `2026-08-23T09:14:07Z`）；`git merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立 —— proposal.md 正文关于该分支已合并、`lib/collision.py` 行号已下移的一整段事实断言（`:178/:219/:230-234/:265-266/:268/:278-279/:366`）经本席逐行独立复读 **全部精确匹配**, 未发现任何偏差。
- 只读审计, 未做任何 git 写操作; 唯一写入为本报告文件。

## 方法

1. 逐条核对 R1 aggregated（`post_spec-R1-1785710000000-a1-entry-claim-rewrite-aggregated.md`, C1–C6 / M1–M10）与本席 R1 报告（F1–F5）在当前文本中的落地状态。
2. 找到并通读 `.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`（Aug 4, 488 行, FIX-01~19 + carry-forward 清单）—— 这是 R1 findings 到当前文本之间唯一的书面桥梁, 逐条核对其中每一条「已起草的修法」是否真的落进了当前 proposal.md。
3. 对每条被判定「未落地」的修法, 独立实读 aria 子模块当前代码（不依赖 editlist 或 proposal.md 自身的转述）复验其技术前提是否仍然成立。
4. 审「C1/C2 owner 裁定落版」段与「请 owner 复议」段本身的事实准确性（不把合规的上呈计入 finding, 除非上呈内容本身有事实错误 —— 本轮未发现此类错误, 见下「附注」）。

## 核心结论（一句话）

**R1-fix editlist 起草的修法只有一小部分真正落进了当前 proposal.md**（C1/C2 owner 裁定相关内容 + NEW-01 + 事实断言实读清单 落地扎实, 逐行核对精确无误）；**但 editlist 里标注「按原样 carry-forward」以及若干独立 FIX 条目（覆盖 R1 aggregated 的 M2/M4/M6/M7 与本席 R1 的 F1/F4/F5）在其后三轮「rework 核验」中始终未被应用**, 且三轮核验的范围都局限于「C1/C2 落版本身对不对」, 没有一轮做过「editlist 全量 vs 当前文本」的差异核对 —— 这正是本轮发现的系统性缺口, 而非某一条孤立遗漏。

---

## R1 findings 逐条 closed / open 表

### R1 aggregated（5 席去重, C1–C6 / M1–M10）

| # | 摘要 | 状态 | 证据 |
|---|---|---|---|
| C1 | 两落点 `allowed-tools` 不支持核心动作 | **✅ CLOSED** | owner 裁定 (a) 已逐字落版 §3；`phase-a-planner/SKILL.md:9`/`spec-drafter/SKILL.md:10` 现值经本席独立 `sed` 复读, 与文中引述逐字一致 |
| C2 | heartbeat 无人调, 保护窗形同虚设 | **✅ CLOSED** | owner 裁定 (ii)+(iii) 已落版 §2.2, 新增 SC-20/SC-21 钉住「两臂可辨」；`--heartbeat-only` 具体入口已点名 |
| C3 | §1 字段格式对真实语料 0/13 匹配 | **✅ CLOSED（附条件）** | §1.2 已如实标注抽取规则「本 Spec 现有措辞不足以实现」, 显式转 A.2 —— Spec 阶段透明承认而非隐藏, 可接受 |
| C4 | `_TERMINAL` 事实断言与代码相反（yielded/unknown 弄反） | **✅ CLOSED（事实层）/ 衍生新缺口** | §2.4 事实订正准确（`_TERMINAL=(done,abandoned,unknown)` 已逐字核实）；但其提出的「unknown 须按'未能核实'呈现」义务缺乏任何实现机制 —— 见下方新 **R2-KM-M2** |
| C5 | D6「无函数支持释放别的容器 claim」为假（`--sweep-stale` 存在） | **✅ CLOSED** | §2.3 已改「只有无差别 sweep, 没有定向 release」, 结论方向不变但理由已订正 |
| C6 | `include_terminal` 传递链漏第 0 段（`collision.py` 签名） | **✅ CLOSED** | §2.4 item 0 + Impact 表已补 `lib/collision.py` 一行, 与本席 R1 F2 同一簇 |
| M1 | 两 Spec 间归一职责真空 | **✅ CLOSED** | 前置 Spec 已 ship（`ca52d1c` 独立核实为真）, `collision.py` 已入 Impact 表 |
| **M2** | §5「放弃必 release」× §2.1「id 不含 slug」互相拆台（同 issue 多方向共享 track_id, 放弃一个连坐释放其余仍在进行的方向） | **❌ STILL OPEN — 提升为 CRITICAL** | editlist 未见任何 FIX 条目处理该问题（`grep "三个方向\|连坐\|共享 track_id"` 在 editlist 全文零命中）；当前 §5「探索性放弃」行原样保留问题场景本身作处置方案, 未变。见下 **R2-KM-C1**，含独立代码复验 |
| M3 | §4 探针「同 issue」匹配谓词对「无」归属未定义 | **⚠️ 未见处置, 未独立复核** | 当前 §4 全文未见「匹配谓词」的显式定义（既未定义如何判「同 issue」也未提及「无」分支归属）。本轮未做独立代码级复验（`sibling_spec_probe.py` 尚未创建, 只能核对文档层面）, 暂不计入本席 finding 计数, 留 A.2 前建议核查 |
| M4 | 「进模板」只做了一半（`standards/openspec/templates/proposal-minimal.md` 未覆盖） | **❌ STILL OPEN — MAJOR** | editlist 标注为「原修法计划中无镜头修正、按原样 carry-forward」（见 editlist:489）, 但当前 Impact 表 (`:422`) 只写 `skills/spec-drafter/SKILL.md`, 只字未提 `standards/openspec/templates/proposal-minimal.md`。见下 **R2-KM-M4**, 含独立文件复验 |
| M5 | `phase1_gate.py:1229` 的 `if args.linked_issue:` 门控整块（91% 路径无输入） | **✅ CLOSED（作为已知限, 非隐藏）** | 该 91% 缺口正是 §Why「⭐ 真正的瓶颈」的立论前提, §1 整节就是为它设计 —— 不是被忽略的盲区, 是被架构性承认并前置处理的核心问题, 不构成本轮 finding |
| M6 | `:1235-1237` 的 `except → []` 才是「零证据当正证据」真实落点 | **❌ STILL OPEN — MAJOR** | editlist 标注 carry-forward（`:489`）；本席独立实读 `phase1_gate.py:1231-1237` 确认 `except Exception` 分支仍把 `linked_issue_overlap` 静默置空且只 `logger.warning`, 未写入 `error` 字段。§2.5/SC-10 只覆盖 fetch 降级（`GateResult.error`）, 未覆盖这条独立的异常兜底路径。见下 **R2-KM-M5** |
| M7 | §4 只扫默认分支 ⇒ in-flight 竞品结构性不可见 | **❌ STILL OPEN — MAJOR** | editlist 标注 carry-forward（`:489`）；当前 §4（`:256`）仍写「只扫 `enforced_remotes` × 各自默认分支」, 未变。见下 **R2-KM-M6** |
| M8 | §3 双落点 SC 零覆盖 | **⚠️ 未独立复核** | 属测试宿主层面（Phase B 才落地）, Spec 文本本身已把 SC-11/SC-12 挂到「行为类」定向 fixture, 判据合理；未做代码级复核（tests/ 尚未写）, 不计入本席 finding 计数 |
| M9 | SC-9/SC-14 标「代码」但实测对象是 SKILL.md 散文 | **⚠️ 未独立复核** | editlist 标注 carry-forward（`:489`）; 未做独立复核, 留意但不计入本席 finding 计数 |
| M10 | SC-8/SC-10 把 CLI 可验证字段与消费层措辞捆一条断言 | **⚠️ 部分核实** | editlist 标注「除 SC-8b/SC-10b 外的部分」carry-forward; 当前文本 SC-8「断言层必须是 CLI 全链路」措辞已到位, 消费层措辞部分未见独立 SC, 与 M9 同归为「未独立复核」类 |

### 本席 R1 报告（F1–F5）

| # | 摘要 | 状态 | 证据 |
|---|---|---|---|
| **F1**（Critical） | track-id 加容器段后, A.1 claim 与 Phase B/D.2b 释放链断裂, 与 DEC-20260519-001「track-id 是脊柱」未对齐 | **❌ STILL OPEN — CRITICAL（回归）** | editlist **已起草 FIX-14**（M2 标签, `:347-365`）明确要求：§5 新增第四行「A.1 成功并继续走循环」+ 补 SC-27 + 三处 SKILL.md 措辞同步声明「本串即本 cycle 的 carry-id」。**当前 §5（:260-266）三行原封不动, 与 R1 时完全相同**；`grep "SC-27\|carry-id.*逐字节复用"` proposal.md 全文零命中。见下 **R2-KM-C2**, 含本轮独立代码复验（`phase-b-developer:92`/`branch-manager:149`/`phase-d-closer:52,55` 现状复读） |
| F2（Critical） | `include_terminal` 传递链漏第 0 段 | **✅ CLOSED** | 同 C6, 已落地 |
| F3（Major） | `_TERMINAL` 事实断言与代码相反 | **✅ CLOSED（事实层）** | 同 C4；衍生 R2-KM-M2（见下） |
| **F4**（Major） | `session-handoff.md` 与 `coordination-ref-schema.md` 均未入 Impact 表 | **❌ STILL OPEN — MAJOR（回归）** | editlist **FIX-17**（`:407-419`）已明确写「`coordination-ref-schema.md` 断言形 + 锚点」+「`session-handoff.md` 原样保留」两项要求。**当前 proposal.md 全文 `grep "session-handoff.md"` 与 `grep "coordination-ref-schema.md"` 均零命中**, 两文件都不在 Impact 表里。见下 **R2-KM-M1** |
| **F5**（Minor） | 本 Spec 自身缺「关联 Issue」字段 | **❌ STILL OPEN — MINOR（回归）** | editlist **FIX-19**（`:437-449`）已起草具体文案 `> **关联 Issue**: 无 — 本 Spec 源自 5 次并发起草事故的直接观察...`。**当前文档头部（:1-8）仍无该字段**, `grep "^\> \*\*关联"` 零命中。见下 **R2-KM-m1** |

---

## 新 findings（still-open, 按严重度排列）

### [CRITICAL] R2-KM-C1 — 「探索性放弃」场景 track-id 无方向区分符, `release_claim_by_track` 会连坐释放同 issue 下仍在进行的其他方向

- **位置**: proposal.md §2.1（:111-124）+ §5（:260-266, 「探索性放弃」行）vs `aria/skills/state-scanner/lib/claim_lifecycle.py:377-402`
- **问题**: §2.1 定义有关联 issue 时 track-id = `<basename>-<number>-<container_uuid>` —— **不含任何 spec-slug / 方向区分符**。当同一容器针对同一 issue 探索多个不同的 Spec 方向（§5 第一行「A.1 试三个方向弃两个」明写的场景）时，若这些探索跨会话进行（不同 session_id，同一 container_id + track_id），会产生**多条**（container, track_id）相同但 session 不同的 active claim。§5 规定放弃时调用 `release_gate.py --status abandoned`，而该 CLI 底层 `release_claim_by_track` 的 docstring 逐字写明（`claim_lifecycle.py:390-393`）：「若若干 active claim 匹配同一 (track_id, container)（同容器跨会话重新认领同一 track 的**正常情形**），**全部匹配的 active claim 都会被释放**」；本席独立实读 `claim_lifecycle.py:417-424` 的 `matches = [rec for rec in ... if rec.container == ... and rec.track_id == norm and rec.status == "active"]` 确认这不是文档夸大，是逐行对应的真实实现。
- **危害**: 放弃方向 1 时（调 `--status abandoned`），若方向 2/3 仍在其他会话下活跃且共享同一 track_id（同一 issue、同一容器），会被**一并**改写为 `abandoned` —— 这是数据破坏级后果（正在进行的工作的 claim 被静默判死），且恰恰发生在本 Spec §5 明确设计要支持的核心场景（探索多方向）里。本项目当前的工作模式（本次审计启动时 git status 即显示同容器 #149/#151/#155 三个并行分支在改）说明「同容器多会话并行」不是边角案例而是常态，风险面是真实的。
- **状态**: 对应 R1 aggregated M2（CR 命中），R1-fix editlist 全文（488 行）未见任何一条 FIX 处理「三个方向共享 track_id」这一具体机制，当前 proposal.md 同样未处理。
- **建议修法**: 二选一并写清楚：(a) track-id 即便在有 linked_issue 时也保留 spec-slug 作为方向区分符（如 `<basename>-<number>-<spec-slug>-<container_uuid>`），付出的代价是需要重新论证 §2.1 现有「不含 slug 故改名不产生孤儿」的依据（该依据本身建立在「不含 slug」之上，两者需要一起重新设计，不能各改一半）；或 (b) 保持 track-id 不含 slug，但为「探索性放弃」场景新增一个不经过 `release_claim_by_track`（按 track_id 定位）而是按 session 精确定位的释放路径（例如 `release_claim` 本身按 (container, session) 定位, 但需要处理其在 D.2b defect (c) 场景下已知失效的问题——两个释放路径不能互相替代, 需要在 §5 里明确哪种退出路径用哪个 CLI）。两条路径都需要新增 SC 钉住「同 track_id 多 session 场景下, 释放一个不影响其他仍 active 的会话」。

### [CRITICAL] R2-KM-C2 — A.1 track-id（含容器段）与 Phase B / D.2b 既有 carry-id（不含容器段）不一致, 成功走完循环的 happy path 上 A.1 claim 永不被显式释放

- **位置**: proposal.md §2.1（:111-113, D3）+ §5（:260-266, 「D.2b 对偶」行, 与 R1 原文逐字相同未改）+ 非目标「不动 Phase B 入口现有认领」（:402）vs `aria/skills/phase-b-developer/SKILL.md:92`、`branch-manager/SKILL.md:149`、`phase-d-closer/SKILL.md:52,55`、`docs/decisions/DEC-20260519-001-multi-terminal-coordination.md:43`
- **问题**: 本席独立复读三处现有代码确认 R1 时的判断至今未变：
  - `phase-b-developer/SKILL.md:92` = `--raw-track-id "<本 cycle carry-id/Spec id>"`（**不含容器段**）；
  - `branch-manager/SKILL.md:149` = `--raw-track-id <carry-id>`（同上, 同一原始串）；
  - `phase-d-closer/SKILL.md:52,55` = D.2b 释放时用「本 cycle 的 carry-id 原始串」, **同一份文档自陈**「carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串，两端一致」。
  三者共同确认：走完整十步循环的 track，其 carry-id 自始至终是同一个（不含容器段的）字符串。而 §2.1 定义的 A.1 track-id 是 `<basename>-<number>-<container_uuid>`（**含容器段**）—— 这是**另一个字符串**。`track_id.py:61-77` 的四步归一算法（lower / 分隔符替换 / 截断 / sha 回落）不包含任何剥离容器段的逻辑, 两个字符串经归一后仍然不同。
  §5「D.2b 对偶」行断言「只有走完循环的轨才到 D.2b；上面两条（探索性放弃/slug 改名）不经过它，故各自显式 release」—— 这句话**默认 D.2b 会释放 A.1 的 claim**, 但 D.2b 调用 `release_claim_by_track(<carry-id>)`, 传入的是不含容器段的字符串, 按 `claim_lifecycle.py:425` 的 `rec.track_id == norm` 精确匹配, **永远匹配不到** A.1 用含容器段字符串写入的那条 claim。
- **危害**: **每一条成功走完整个循环的 track**（这是最常见、非边角的路径，恰恰是「设计要保护的绝大多数情形」），A.1 阶段留下的 claim 都不会被 D.2b 释放，只能悬挂到 `SWEEP_TTL`（本轮已改为 24h 量级）才被动清理为 `abandoned`——期间它会持续出现在 `linked_issue_overlap[]`（因为它是 `active` 状态）里，对**后续**真正想认领同一 issue 的其他容器造成误报式的「已被占用」告警，直到 sweep 生效。这与本 Spec §Why 反复强调的「机制要经得起最常见路径检验」精神直接相悖。
- **关联不变量冲突**: `DEC-20260519-001:43`「track-id 是脊柱：1:1 绑分支恒成立」——本 Spec 让「同一份工作」在 A.1 与 Phase B 阶段派生出两个不同的 track-id，事实上打破了这条决策记录立下的不变量，Spec 全文未与该决策记录做过一次显式对账（无论是修订它还是记豁免）。
- **状态（回归）**: R1-fix editlist **已起草 FIX-14**（标签 M2，`editlist:347-365`），给出了具体修法（§5 新增第四行 + 补 SC-27 + 三处 SKILL.md 补一句「本串即本 cycle 的 carry-id」）并列为 owner 待裁的 U-3（A 方案改 3 个 SKILL.md vs B 方案 D.2b 额外调用）。**当前 proposal.md 的 §5 表格与 R1 时逐字相同，SC-27 不存在，U-3 从未出现在当前文档任何位置** —— 这是一条被起草过修法、却在后续 rework 中彻底丢失的 finding，而非从未被发现。
- **建议修法**: 沿用 editlist FIX-14 的方案 A（推荐）：把 A.1 派生的原串定义为本 cycle 的 carry-id，`phase-b-developer` B.0 与 `phase-d-closer` D.2b 逐字节复用该串（而非各自独立生成），并新增 SC 钉住「A.1 认领 → 走完循环 → D.2b release 之后，该 A.1 claim 不再 active」。需要先请 owner 确认这是否违反非目标「不动 Phase B 入口现有认领」的字面（FIX-14 自己也标了这一点为 U-3, 未拍板）。

### [MAJOR] R2-KM-M1 — Impact 表仍零覆盖 `session-handoff.md`（track_id.py 自称的 SOT）与 `coordination-ref-schema.md`（claim 结构 SOT）

- **位置**: proposal.md Impact 表（:411-433）vs `standards/conventions/session-handoff.md` + `aria/skills/state-scanner/docs/coordination-ref-schema.md`
- **问题**: `track_id.py:69-70` 的 docstring 明确把 `standards/conventions/session-handoff.md §2.3.1` 列为 track-id 概念的权威来源；`coordination-ref-schema.md` 是 claim YAML 结构的 schema 文档（`claim_schema.py` docstring 引用它）。本 Spec 在 A.1 阶段引入新的 track-id 构造形态（含容器段）、新的 heartbeat-by-track 语义、新的 `include_terminal`/`unknown_schema_claims` 概念 —— 均是对这两份 SOT 所描述行为的实质扩展或（如 R2-KM-C2 所示）实质冲突。本席 `grep -n "session-handoff.md"` 与 `grep -n "coordination-ref-schema.md"` proposal.md 全文均**零命中**，两文件都不在 Impact 表里。
- **状态（回归）**: R1-fix editlist **FIX-17**（`editlist:407-419`）已明确要求把 `coordination-ref-schema.md` 从「若存在」的条件形改为断言形并给出具体锚点（§3.2, :129-140），并写明「另/KM 的 `session-handoff.md` 入 Impact 一项原样保留（无镜头修正）」—— 即该文件本就该被保留在 Impact 表里，是后续被误删或从未被抄入当前版本。
- **危害**: 与本 Spec 自己已经正确列出 `layer-l-integration.md`（因为「会过时」）的处理逻辑不一致，造成「部分同步、部分遗漏」的治理不一致；尤其是 R2-KM-C2 揭示的 track-id 不一致问题，如果不在 `session-handoff.md`（它定义了第三个消费入口 —— carry-id → `phase1_gate.run_gate()`）里同步说明，后续读者会依据过时描述做出与本 Spec 冲突的假设。
- **建议修法**: 按 editlist FIX-17 原方案：Impact 表补两行，`coordination-ref-schema.md` §3.2 追加第 6 条「unknown claim 在 A.1 消费面的可见性语义」，`session-handoff.md` 补充「A.1 阶段可能出现的 track-id 构造形态及其与 carry-id 消费路径的关系」（并与 R2-KM-C2 的裁决联动）。

### [MAJOR] R2-KM-M2 — §2.4 声称「`unknown` 须按'未能核实'呈现」的义务, 在当前设计下没有任何实现机制可以兑现

- **位置**: proposal.md §2.4（:180-182）vs `aria/skills/state-scanner/lib/claim_schema.py:212-230` + `collision.py:210-217`（cb6bd5d）/ `:268-275`（origin/master）
- **问题**: §2.4 事实订正准确地指出 `_TERMINAL` 含 `unknown` 且要求「不得与 done/abandoned 合并措辞，须按'未能核实对方状态'呈现」。但本席独立实读 `claim_schema.py:219-229` 确认：schema_version 不匹配时构造的 `unknown` 状态哨兵记录**不传 `linked_issue` 字段**（`ClaimRecord(...)` 构造调用中没有该关键字参数，dataclass 默认落 `None`）。而 `linked_issue_overlaps` 除了 `_TERMINAL` 过滤（跳过 `unknown`）之外，紧接着还有一道独立的过滤 `if not getattr(c, "linked_issue", None): continue`（`collision.py:215`）——即便未来把 `unknown` 从 `_TERMINAL` 里摘出去，这第二道过滤依然会把它挡住，因为它的 `linked_issue` 恒为 `None`。⇒ **`unknown` claim 在当前的 `linked_issue_overlap[]` 通道里结构性地、双重地不可达**，§2.4 提出的呈现义务没有任何字段或 SC 去承载它：SC-8 只提 `done`/`abandoned`/`yielded` 三态；§6 残余缺口表（:270-275）四行里也没有把「unknown claim 不可见」列为已知限。
- **危害**: 这是一条写进正文的「须」字义务（规范性语言），但没有对应机制、没有 SC、也没有被诚实标记为已知限——对实现者是一个无法兑现的承诺，对审计者是一个看似「已处理」实则空转的条款。
- **状态**: R1-fix editlist 曾就此草拟过完整方案（FIX-03：新增独立 additive 键 `unknown_schema_claims: int`，配 SC-24，门控改为 `if args.linked_issue or args.include_terminal:`）——该方案本身也在 editlist 中被列为「整合者本轮新发现，三个镜头都没提出这个具体形态」的新表面，未经外部审阅，但技术前提（parse_claim 不传 linked_issue）本席本轮独立复验为真。当前 proposal.md 完全没有吸收这个方案，也没有代之以其他方案，只留下一句无法兑现的「须」。
- **建议修法**: 采纳 editlist FIX-03 的技术方向（独立 additive 计数键，不强行塞进 `linked_issue_overlap[]`），或至少把当前措辞降级为「已知限：`unknown` 状态的 claim 在 `linked_issue_overlap[]` 里不可见（parse_claim 未回填 `linked_issue`），跨版本兼容问题需要看 `phase1_gate` 的 `soft_error` 日志，不作为本 Spec 覆盖范围」，并补进 §6 表。两条路径任选其一，但不能保持当前「声称义务、零机制」的状态。

### [MAJOR] R2-KM-M3 — §2.3「起草前经 `AskUserQuestion` 请裁」与 Layer 2 无人值守（AD10 仅 1 个人类参与点）之间的冲突未解决

- **位置**: proposal.md §2.3（:165-174）vs CLAUDE.md「Aria 2.0 运行时」段（人类参与点仅 1 个: AD10, S7_AWAITING_MERGE）
- **问题**: 当前 §2.3 要求 `linked_issue_overlap[]` 非空时「在起草前经 `AskUserQuestion` 请裁」，并明确「不是 AI 渲染一行后自行决定 —— 继续起草属 owner 权限面（Rule #10）」。本项目 CLAUDE.md 明文：v2.0 运行时人类参与点**仅 1 个**（AD10, 在 S7_AWAITING_MERGE 由产品负责人签字 merge）。A.1 阶段远早于 S7，属于 Layer 2 全自主执行区间——若 Layer 2 在无人值守场景下遇到 overlap 非空，`AskUserQuestion` 无人应答，而本节又明确禁止 AI 自行放行，这个「advisory 不阻断」的机制在这一具体分支下会实质变成阻断（与非目标「不把 advisory 升级为 block」，:401，字面冲突）。
- **状态（回归）**: 该冲突正是 R1 aggregated CR-M5 的原始指控；R1-fix editlist 曾起草 **FIX-16**（`editlist:386-406`），方案是新增 `state_scanner.coordination.unattended` config key（默认 false，由容器镜像/Nomad env 显式置 true）作为判据，并配 SC-28。本席 `grep -n "unattended\|无人值守"` proposal.md 全文**零命中**（除 §2.3 本身重复出现「不硬阻断/AD10/Rule #10」这几个词，没有 unattended 分支本身）—— FIX-16 起草的整个「无人值守分支」概念在当前版本里已经不存在，不是被否决、被替换，而是完全消失，未留痕迹。
- **危害**: 若 Layer 2 无人值守环境下真的命中 overlap 非空场景（并非小概率——这正是本 Spec 存在的理由），当前设计没有定义的行为路径，会在 Phase A 阶段死等一个不会到来的人工输入，或者迫使实现者自己在 A.2/B 阶段临场发明一个未经审计的绕过逻辑。
- **建议修法**: 恢复 editlist FIX-16 的判据设计（或等价方案），至少在 §2.3 显式声明「无人值守（`unattended` 判据）时的降级行为是什么」，不能把这个分支留白交给 Phase B 实现者自由裁量。

### [MAJOR] R2-KM-M4 — 「进模板」只改了 `spec-drafter/SKILL.md` 自身引导文字, 未覆盖跨项目 SOT `standards/openspec/templates/proposal-minimal.md`

- **位置**: proposal.md §1.1（:70）+ Impact 表（:422）vs `standards/openspec/templates/proposal-minimal.md`（本席确认该文件存在）+ `aria/skills/spec-drafter/SKILL.md:429`
- **问题**: 本席独立核实 `standards/openspec/templates/proposal-minimal.md` 是真实存在的文件，`spec-drafter/SKILL.md:429` 明确把它列为「proposal-minimal 模板」链接引用（即 spec-drafter 实际生成 proposal 时依据的是这份**跨项目共享**的 standards 子模块模板，不是它自己私有的一份模板）。本席 `grep -n "关联 Issue" standards/openspec/templates/proposal-minimal.md` **零命中** —— 该模板当前确实不含「关联 Issue」字段。当前 proposal.md 的 §1.1 与 Impact 表都只提「`spec-drafter` 的 proposal 模板」/「`skills/spec-drafter/SKILL.md`」，全文对 `standards/openspec/templates/proposal-minimal.md` 零引用。
- **危害**: `standards/` 是跨项目共享子模块（CLAUDE.md 信息地图：「方法论定义」，memory `project_kairos_adopter` 记录 Kairos 是首个跨项目采用者）——若只改 `spec-drafter/SKILL.md` 里的引导措辞而不改 `proposal-minimal.md` 本身，其他采用 Aria 方法论的项目（通过 `standards` 子模块获取模板）不会拿到「关联 Issue」字段，本 Spec 「无机械回声的义务会退化」的自我警示只在 Aria 自己的仓库里生效，是一次「只字面加了一行 Impact，但没有覆盖真正 SOT」的半修复。
- **状态**: R1-fix editlist 在「原修法计划中无镜头修正、按原样 carry-forward」段（`:489`）明确列出这一条，标注为已核实成立、无需修正、应当原样落地——但当前版本没有落地。
- **建议修法**: Impact 表新增一行 `standards/openspec/templates/proposal-minimal.md`（增「关联 Issue」字段，与 §1.1 的格式规则一致），并注意这是对**共享子模块**的编辑，按本项目惯例需要独立的子模块 PR + 本地双推（CLAUDE.md「多远程推送」两条硬约束），不能和主仓改动混在一次提交里落地。

### [MAJOR] R2-KM-M5 — `phase1_gate.py:1236-1237` 的 `except Exception → out["linked_issue_overlap"] = []` 是「零证据当正证据」的另一个真实落点, 未被 §2.5/SC-10 覆盖

- **位置**: proposal.md §2.5（:196-199）+ SC-10（:368）vs `aria/skills/state-scanner/scripts/phase1_gate.py:1229-1237`（cb6bd5d）
- **问题**: 本席独立实读该段代码（见上方「审计对象与工作树」旁引用）：
  ```python
  if args.linked_issue:
      try:
          claims = read_claims(repo).claims
          out["linked_issue_overlap"] = linked_issue_overlaps(
              claims, result.track_id, args.linked_issue
          )
      except Exception as exc:
          logger.warning("phase1_gate: linked_issue overlap check skipped (%s)", exc)
          out["linked_issue_overlap"] = []
  ```
  任何异常（不限于 fetch 降级——也包括 claim 文件损坏、`linked_issue_overlaps` 自身的 bug 等）都会被这个 `except` 捕获，静默把结果置为空列表，且只写一行 `logger.warning`，**不会**出现在结构化的 `GateResult.error` 字段里。而 §2.5 目前只讨论了 `GateResult.error`（fetch 降级的契约），SC-10 的测试场景也明确写的是「fetch 降级」——两者都没有覆盖这个独立的、更靠近实际消费面的 `except` 兜底路径。「零证据（未能核实）」与「有正证据（确认无碰撞）」在这条路径上依然是同一个返回值 `[]`，与 §2.5 反复强调的「零证据不得当正证据」原则相悖。
- **危害**: SC-10 即便全绿（覆盖了 fetch 降级），这条路径依然可以在实现完全符合 SC-10 的情况下保持「一个 bug 导致 overlap 检查失败 = 静默呈现为无碰撞」的行为，AI 消费方会误判为「已核实、无碰撞」从而放心起草，重演本 Spec 反复引用的 R3/C2「零证据当正证据」同款缺陷，只是换了一个代码位置。
- **状态**: R1-fix editlist 「carry-forward」段（`:489`）明确列出（标签 M6），并特别提示「注意其措辞须按 FIX-12 的四态表走 error 档而非 unknown 档」——即当时已经想清楚了应该怎么归类，只是未被写进当前文本。
- **建议修法**: §2.5 的「error 契约」段扩展为同时覆盖两条路径：fetch 降级（已有）与 overlap 计算异常（新增）——后者应当把 `str(exc)` 或至少一个稳定的错误码写进 `out["linked_issue_overlap_error"]`（或复用 `GateResult.error` 的同一套 token 体系），消费面按同一条「未能核实」措辞处理，不能让这条 except 分支继续只留一行日志。

### [MAJOR] R2-KM-M6 — §4 探针只扫「各自默认分支」, 对其核心目的（捕获 in-flight 竞品）结构性失效

- **位置**: proposal.md §4（:238-258, 尤其 :256「规模上限」行）vs §4 自身的定位（「盲区声明」:258 只提「未 push」与「已 ship 归档」两类盲区）
- **问题**: §4「规模上限」明文「只扫 `enforced_remotes` × 各自默认分支（非全部 ref）」。但 §4 的存在理由是捕获「远端同 issue 的**竞品 spec**」——一份仍在制、尚未合并的竞品 Spec，按定义几乎总是活在一个**非默认分支**（feature branch）上，直到它合并才会出现在默认分支。若只扫默认分支：等它出现在默认分支时，它已经合并/归档，不再是「in-flight」而是既成事实——这恰恰是本 Spec §Why 开篇讲的第 5 次事故的形态（对方已经 ship 并归档才发现）。也就是说，§4 当前的扫描范围**结构性地只能捕获「已经太晚」的情形**，对「还来得及协调」的 in-flight 情形（竞品在 feature 分支上、尚未合并）反而看不见——而后者才是探针最有价值、最该覆盖的场景。§258 的「盲区声明」只列了「对方没走 claim」与「对方已 ship 并归档」两类已知盲区，**没有把「对方在非默认分支上活跃开发」列为第三类盲区**，读者会误以为默认分支扫描已经覆盖了「进行中」的竞品。
- **状态**: R1-fix editlist「carry-forward」段（`:489`）明确列出（标签 M7：「§4 只扫默认分支 ⇒ in-flight 竞品不可见」），当前文本未处理。
- **建议修法**: 至少在 §258 的盲区声明里补第三类：「对方 Spec 在非默认分支（feature branch）上进行中且未合并/未归档 —— 本机制看不见，需依赖 A.1 claim 机制（§2/§3）或人工协调」，让「探针只覆盖已完成/已归档」这一定位对读者透明；如果要真正提升覆盖率，需要评估扫描范围扩到 `enforced_remotes` 的全部活跃分支（而非仅默认分支）的代价（对照 spike S2 的 fetch 耗时数据）是否可接受。

---

### [MINOR] R2-KM-m1 — 本 Spec 自身仍未携带「关联 Issue」字段（dogfood 缺口, 回归）

- **位置**: proposal.md 头部（:1-8）vs 本 Spec §1.1 自定的规则（:70,「无关联时显式写 `无`，不留空」）
- **问题**: 本席 `grep -n "^\> \*\*关联"` proposal.md 头部区块零命中。R1-fix editlist **FIX-19**（`:437-449`）已起草具体文案（`> **关联 Issue**: 无 — 本 Spec 源自 5 次并发起草事故的直接观察...`），当前版本未落地。
- **危害**: 低（不影响机制正确性），但本 Spec 全文反复以「知道也做不到」「dogfood」为核心论据（§Why 开篇即是「提出这条纪律的人在提出后第二天违反了它」），自身仍不满足自己定的规则，是一个显眼的反证，且历经 3 轮 rework 核验都未被捕捉到。
- **建议修法**: 按 editlist FIX-19 原文案补一行。

---

## 附注 — 核实通过, 未构成 finding

- **「⚠️ 实读订正 · 请 owner 复议」段（§2.2, :161）**: 关于 `STALE_TTL` 与 `--sweep-stale` 因果关系的技术前提, 本席独立复读 `gc.py:341`（`sweep_stale_active` 默认 `stale_ttl_seconds: int = SWEEP_TTL`）与 `release_gate.py:141`（调用未传覆盖值）**逐字确认为真** —— 该复议段的事实基础准确，是合规的上呈行为，不计入 finding。
- **§3「⚠️ 实读订正 · 请 owner 复议」段（:234）**: 关于 Rule #6 措辞订正过程的记录准确，两套件 (`phase-a-planner.json`/`spec-drafter.json`) 均存在且各 2 eval case，本席独立 `python3 -c "json.load(...)"` 复核确认精确匹配。
- **`origin/feature/linked-issue-normalization` 已合并**（§2.2/§2.4 协调项）：本席独立 `git fetch` + `merge-base --is-ancestor` + 逐行 `git show ca52d1c:...collision.py` 核对全部行号引用（`:178/:219/:230-234/:265-266/:268/:278-279/:366`），**全部精确匹配**，是本轮审计中准确度最高的一段。
- **C1 owner 裁定落版**（§3, :209-234）：`phase-a-planner/SKILL.md:9`、`spec-drafter/SKILL.md:9-10` 现值经独立复读，与文中逐字引述一致；两 AB 套件 eval case 数核实精确。
- **C2 owner 裁定落版**（§2.2, :137-163）：`constants.py:36/51`（STALE_TTL/SWEEP_TTL 定义）、`gc.py:341`、`release_gate.py:141/225`、`state-scanner/SKILL.md:174-176`、`phase-d-closer/SKILL.md:54-58`、`reconcile.py:154-163` 全部独立复读，与正文逐字/逐语义一致，未发现任何事实性错误。

---

## 一句话结论

**当前文本内部的事实断言质量极高**（本轮独立复验的十余处代码引用无一失准），但**外部完整性出现了系统性回退**：R1-fix editlist（Aug 4）起草的一批修法（覆盖 R1 aggregated M2/M4/M6/M7 与本席 F1/F4/F5）从未真正落进 proposal.md，而随后三轮「rework 核验」的审查范围都收窄到「C1/C2 落版对不对」，没有一轮对着 editlist 做过一次全量差异核对，导致这批已经起草好、只差誊写的修法在 R2 时依然全部缺失——其中两条（探索性放弃连坐释放 / A.1→Phase B 释放链断裂）涉及数据破坏或核心机制在最常见路径上失效，判 REVISE，建议下一轮修订前先做一次「R1-fix editlist vs 当前文本」的逐条覆盖率核对，而非继续从「上一轮核验的几条 finding」局部展开。
