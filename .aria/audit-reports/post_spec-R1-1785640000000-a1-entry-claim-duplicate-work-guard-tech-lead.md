# post_spec R1 — tech-lead

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=6 minor=3

> 审的对象: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (Level 2, 全文)。
> 所有引用行号均已实读；所有行为断言均以实跑 / 生产语料 / 互斥原文为据。只读，未改任何文件。

---

## 先说写对了的部分 (不是客套，是审计结论的一半)

1. **D6/D7 的 dogfood 属实，双证核过**。`.aria/coordination-telemetry.jsonl` 末行 `2026-08-02T11:54:59Z / outcome=passed / track_id=aria-plugin-124-path-coverage-z-flag`，且 coordination ref 内 `claims/023236f2/s-b291@1154.yaml` 落盘 `phase: A.1` / `linked_issue: aria-plugin#124` / `status: active`。「`--phase A.1` 无需改 phase1_gate 代码」(D6) 与「claim 立即写并推远端」(D7) 都成立，不是推断。D7 把承重前提点名并要求实测，这个做法本身是对的。
2. **§闸门待裁 (proposal.md:169-175) 的 Rule #10 论证成文正确**。`.aria/config.json` 实测 `audit.enabled=true` / `audit.checkpoints.post_spec="convergence"`；行 171 逐字复述了封闭四类白名单并逐条排除；行 173 拒绝让「session 硬约束」与「闸门」互相授权跳过、一并上交 owner。这正是 Rule #10 §豁免白名单 + memory `no-self-exempt-gates` 要求的形状，无自我豁免。
3. **§Why 对「原建议」的证伪 (行 44-60) 是本 Spec 最强的一段**。用 `feedback_verify_predicate_inputs_exist` 的两层判据 (逻辑对吗 / 它要判的输入真会被生成吗) 杀掉自己的触发建议，方法论上正确 —— 问题在于同一把尺子没有回头量自己的两个机制 (见 MAJOR-2)。
4. **D4「盲区写进正文不藏脚注」立场正确**，§2 行 105 确实把副机制的盲区写在承诺面旁边。缺口清单不全是另一回事 (CRITICAL-2)，态度不该被否定。

---

## Findings

### [CRITICAL] 主机制的唯一 join key `linked_issue` 无归一，生产语料已两格式并存；Spec 模板与 CLI help 互斥 ⇒ 跨格式静默零命中

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:92`, `:96`, `:137`
- **问题**: 整个主机制押在 `linked_issue_overlaps()` 上，而它对 `linked_issue` 做的是**裸精确串比对**，无归一、无 fallback。Spec §1 的调用模板 (行 92) 规定 `--linked-issue "<repo>#<n>"` (裸形)，而 `phase1_gate` 自己的 CLI help 给的示例是 `'10CG/Aria#160'` (org 限定形)。两个 SOT 直接互斥，且**两种格式在生产 coordination ref 里已经同时存在**。两个容器各读一份文档 ⇒ 同一个 issue 两种写法 ⇒ overlap 恒空，而 CLI 退出码仍是 0、`linked_issue_overlap: []` 与「真的没人在做」逐字节不可区分 —— 假绿。
- **证据**:
  - `aria/skills/state-scanner/lib/collision.py:217` — `if c.linked_issue != own_linked_issue: continue` (精确比对，全函数无 normalize)。
  - `aria/skills/state-scanner/scripts/phase1_gate.py:1202` — help 原文 `"可选语义重叠信号 (Part B1, 如 '10CG/Aria#160')"`，与 proposal.md:92 的 `<repo>#<n>` 互斥。
  - 生产语料 (`git show refs/aria/coordination:claims/**`) 全量统计：org 限定形 9 条 (`10CG/Aria#147` / `10CG/Aria#165` / `10CG/aria-plugin#110`×4 / `#113`×2 / `#121`)，裸形 4 条 (`aria-plugin#116` / `#118` / `#122` / `#124`)。**同一个容器两种都用过** —— `023236f2` 在 07-19/07-22 写 `10CG/aria-plugin#113`，在 08-02 写 `aria-plugin#124`。
  - 实跑 (in-process，无写入):
    ```
    L.linked_issue='10CG/aria-plugin#122', R 传 'aria-plugin#122'      -> []        ← 静默漏
    L.linked_issue='10CG/aria-plugin#122', R 传 '10CG/aria-plugin#122' -> ['spec-L'] ← 命中
    ```
  - 附带: 人读的「关联 Issue」字段又是第三种格式，全语料 3 变体 `[10CG/aria-plugin #122]` (带空格) / `[10CG/Aria #166]` / `[#154]` (无 repo)。副机制若从该字段推导 issue token，与主机制的 token 又对不上。
- **建议修法**: 在 §1 之前先定义 `linked_issue` 的**归一规则** (建议: 小写 + 强制 `<org>/<repo>#<n>`，缺 org 时按当前 repo 的 origin 推导)，落点放 `lib/collision.py` 的比对前归一 (不触碰 `phase1_gate.py` 本体，与 §非目标 行 152 不冲突) 或新增一个 A.1 调用前的归一 helper。同步: (a) 修正 `phase1_gate.py:1202` help 示例与 §1 模板一致；(b) 新增 SC「L 用 org 限定形 / R 用裸形，同 issue ⇒ overlap 必须非空」，且该 SC 在归一落地前必须**红**；(c) 「关联 Issue」人读字段与 `--linked-issue` token 的映射规则写进 §1。

---

### [CRITICAL] A.1 claim 无 heartbeat，24h 后被 sweep 成 `abandoned`；主机制的保护窗短于它宣称能防的那次事故，且 §3 残余缺口只写了「秒级」

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:76` (反事实), `:107-113` (§3 残余缺口), `:127` (D7)
- **问题**: D7 把「claim 立即推远端」点名为承重前提并实测了 —— 但那只是**写入腿**。另一条同样承重的腿是**存活腿**: claim 在 A.1 写下后要一直可见到竞品出现为止。这条腿实测**不成立**。生产无 heartbeat 回路 (`constants.py:44` 自述「heartbeat() has zero production call sites」)，A.1 claim 的 `heartbeat_at` 冻结在 acquire 时刻；`gc.sweep_stale_active` 默认 `SWEEP_TTL=86400` (24h)，把任何 `status=active` 且 heartbeat 超时的 claim **跨容器**改写为 `abandoned`；而 `linked_issue_overlaps` 第一件事就是跳过 `abandoned`。⇒ **A.1 claim 的有效保护窗 ≤ 24h**。Spec 行 76 的反事实跨 07-25→07-27 (>48h)，行 17 描述的第 5 次事故跨 07-30→08-02 (>72h)，两者都超出保护窗。而 §3 (行 109-111) 声称「两个机制都不覆盖」的残余只有「秒级」推送窗口 —— 漏了一个数量级差 4 个的窗口，这正是 §3 自己援引的「no silent caps」要杜绝的。
- **证据**:
  - `aria/skills/state-scanner/lib/constants.py:36` `STALE_TTL=1800`; `:51` `SWEEP_TTL=86400`; `:44-47` 明文「no production heartbeat loop exists … every live claim's heartbeat_at is frozen at acquire time」。
  - `aria/skills/state-scanner/lib/gc.py:341` `stale_ttl_seconds: int = SWEEP_TTL`; `:381` 只过滤 `status != "active"`; `:403` 写 `status="abandoned"`; `:405` **保留原 heartbeat_at**; docstring `:361-363` 「Cross-container by design … MAY rewrite other containers' claim files」。
  - `aria/skills/state-scanner/lib/collision.py:210` `_TERMINAL = ("done","abandoned","unknown")`; `:213` 命中即 `continue`。实跑: L 状态置 `abandoned` ⇒ `linked_issue_overlaps(...) == []`。
  - 该 sweep **不是理论风险，是已排定的例行动作**: `aria/skills/phase-d-closer/SKILL.md:52` 的 D.2b 命令固定带 `--sweep-stale --gc`，`:59` 进一步要求「本 session 未认领时**仍建议跑** `--sweep-stale --gc`，保持 ref 卫生」—— 任何容器的任何一次周期收尾都会扫全 ref。
  - **已在本仓生产语料中发生过一次**: `claims/023236f2/s-0998@1721.yaml` = `phase: A.1` / `status: abandoned` / `claimed_at == heartbeat_at == 2026-07-12T17:21:51Z`。`heartbeat_at` 未被改写是 sweep 的**唯一签名** —— `claim_lifecycle.py:355` (`release_claim`) 与 `:446` (`release_claim_by_track`) 都会把 heartbeat_at 覆写成释放时刻，只有 `gc.py:405` 保留。⇒ 一条 A.1 claim 已被 sweep 成 abandoned。
  - 反事实的精确状态: 行 76 目前只在「48h 内全 Lab 无人跑过 D.2b sweep」时成立 —— 即它依赖本方法论自己 MANDATE 的一步**没有被执行**。
  - (次要) `phase-d-closer/SKILL.md:56` 文档写的是「heartbeat 超 **STALE_TTL**」而代码用 SWEEP_TTL，读文档实现的人会以为窗口只有 30 分钟。这是既有 doc drift，但直接放大本条风险。
- **建议修法** (三选一或组合，方向都是**延长/续期保护窗**，不是缩短 sweep):
  1. 把「每轮跑」的预算从副机制挪一部分到主机制 —— A.2/A.3 与 audit-engine 每轮入口调 `phase1_gate` 续期 (同 raw-track-id ⇒ 同 track_id，acquire 即刷新 heartbeat)，使保护窗随实际工作节奏滚动；
  2. 给 pre-B claim (phase 以 `A` 开头) 单列更长的 sweep TTL 或豁免，前提是 MAJOR-4 的显式释放路径先落地 (否则换成僵尸堆积)；
  3. 至少把「A.1 claim 的可见期上界 = SWEEP_TTL (当前 24h)，超期后主机制静默失效」**写进 §3 残余缺口**，并明说 >24h 的窗口交由副机制兜底 —— 但那要求副机制真能兜 (见 MAJOR-1)。
  4. 无论选哪条，`phase-d-closer/SKILL.md:56` 的 STALE_TTL/SWEEP_TTL 笔误应一并勘正。
- **与 MAJOR-4 的关系 (防误读)**: 本条说「claim 死太快」，MAJOR-4 说「claim 会堆积」—— 两者不矛盾，恰恰是同一把 24h 旋钮被要求同时满足两个相反需求 (memory `knob-granularity` 形状)。正解是给 A.1 补显式释放路径 (MAJOR-4)，从而**解放**这把旋钮去满足本条。

---

### [MAJOR] 副机制的 glob `openspec/changes/*/proposal.md` 排除 `openspec/archive/` —— 恰好漏掉第 5 次事故 (Spec 最强调的那次) 的实际终态

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:101`, `:140` (SC-4)
- **问题**: 竞品 Spec 一旦 ship，Phase D.2 会把它从 `openspec/changes/<slug>/` **移到** `openspec/archive/<date>-<slug>/`。Spec 行 17 自述的第 5 次事故正是这个终态: 并发轨 07-31 走完十步循环 ship 为 v1.65.0 **并归档**。按行 101 写死的 glob，今天在 origin/master 上扫 `aria-plugin#122`，真竞品**扫不到**。
- **证据** (实跑 `git grep` on `origin/master`):
  ```
  glob = openspec/changes/*/proposal.md   命中: a1-entry-claim-duplicate-work-guard/  (自己)
                                                phase-c-integrator-ci-path-coverage/   (自己那条已作废的轨)
  glob = openspec/archive/*/proposal.md   命中: 2026-07-31-phase-c-gate-path-coverage-not-applicable/  ← 真竞品
  ```
  归档竞品头部逐字: `# Proposal: phase-c-gate-path-coverage-not-applicable (aria-plugin #122)` / `> **Status**: ✅ Complete (shipped aria-plugin v1.65.0, 2026-07-31)`。
  附带: SC-7 (行 143) 只要求排除「自身 track-id / 自身目录」(单数)，而实跑显示同一作者/同一容器在 changes/ 下有**两个**目录，probe 会把自己那条作废轨报成竞品。
- **建议修法**: (a) glob 扩为 `openspec/{changes,archive}/*/proposal.md`；(b) SC-4 的期望要**区分 active 与 archived** —— archived 竞品不是弱信号而是**最强信号** (「对方已 ship，你现在做的是纯重复劳动，应当停手而非协调」)，两者的建议动作不同，不能折叠成一句「报告命中」；(c) SC-7 的排除面从「自身目录」改为「同 owner/container 名下全部目录」，并单列一条 SC 覆盖「同 owner 的另一条作废轨」。

---

### [MAJOR] 两个机制共用的谓词输入「关联 Issue」是一个无 schema、无模板、无校验、作者自控的字段，全语料基率 10% ⇒ D2 复制了它声称要修的「可选=多数人不传=机制空转」

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:96`, `:101`, `:122` (D2), `:139` (SC-3)
- **问题**: D2 的触发条件是「spec **有**『关联 Issue』字段时必传」。但这个字段在整个方法论里没有定义: `spec-drafter/SKILL.md` 全文零处提到 issue / 关联 / linked，没有模板、没有 validator、没有 frontmatter 位置。⇒ 触发条件 100% 由起草者自己决定，**省掉字段即免除义务，且省略不可观测** (没有任何东西会注意到一份 spec「本该有」关联 issue)。这与行 122 自己写的「可选=多数人不传=机制空转」是同一个失效形状，只是上移了一层。更关键: 这正是 Spec 在行 58 引用 `feedback_verify_predicate_inputs_exist` 杀掉原建议时用的那把尺子 (「它要判的输入真会被生成吗」)，没有回头量自己。
- **证据**:
  - 全语料实测: `openspec/**/proposal.md` 共 **139** 份，含「关联 Issue」字样的 **14** 份 ⇒ 基率 **10.1%**。
  - `aria/skills/spec-drafter/SKILL.md`: `grep -n "关联 Issue\|linked\|issue"` → 零命中。
  - `aria/skills/state-scanner/lib/collision.py:215` — `if not getattr(c, "linked_issue", None): continue`：没带 `--linked-issue` 的 claim 对**所有人**不可见，不只是对自己无效。
  - **本 Spec 自身就是那 90%**: proposal.md:3-9 的头部只有 Status / Created / Spec Level / 触发 / 代码落点 / ship target，**没有「关联 Issue」字段** —— 按它自己的 D2，本 Spec 免传 `--linked-issue`。coordination ref 实测也确实没有任何 claim 匹配 `a1-entry|duplicate-work`。
  - `standards/` 全目录 `grep -rn linked_issue` → 零命中，无上位 SOT。
- **建议修法**: 先补谓词、再谈义务。(a) 把「关联 Issue」定义成 spec 头部的**必填-或-显式-N/A** 字段 (spec-drafter 模板 + 一条机械 validator，与既有 `spec_complete.py` gate 家族同构)；(b) D2 的触发条件改成 **fail-CLOSED**: 「字段缺失」本身就红，只有**显式写了 `关联 Issue: N/A (纯内部重构)`** 才放行 (memory `feedback_invariant_needs_failclosed_default`)；(c) 触发条件确定后，SC-3 的被测对象才有可能明确 (见 MAJOR-3)。

---

### [MAJOR] SC-1~3 的落地载体不存在: Impact 表挂在「`skills/phase-a-planner/` 既有测试」，而该 skill 目录下**只有 SKILL.md**，全仓零测试引用它

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:164` (Impact 行), `:139` (SC-3)
- **问题**: SC-3 是 D2「条件必需」的唯一机械落实，Spec 自称「防退化成可选」。但 Impact 表把 SC-1~3 挂给「`skills/phase-a-planner/` 既有测试 → 扩展」—— **该资产不存在**。这把「扩展既有测试」(低成本、有既有断言可复用) 悄悄换成了「为一个零测试的 Skill 从头建测试目录」。更根本的是: SC-3 的被测对象是 **SKILL.md 里的 AI 执行行为**，不是一段代码 —— argparse 层 `--linked-issue` 是 `default=None` 的可选参数，而 §非目标 (行 152) 又禁止改 `phase1_gate` 自身。因此不存在任何可以「断言该参数在场」的代码位置，SC-3 目前不可能红，也不可能绿。
- **证据**:
  - `find /home/dev/Aria/aria/skills/phase-a-planner -type f` → 仅 `SKILL.md` (单文件)。
  - `grep -rln "phase-a-planner" aria --include=test_*.py` → 零命中。
  - `aria/skills/state-scanner/scripts/phase1_gate.py:1198-1200` — `parser.add_argument("--linked-issue", default=None, ...)`，argparse 层可选。
  - proposal.md:152 — 「不改 `phase1_gate` 自身代码 (只改调用点与调用参数)」。
  - 对照: proposal.md:129 的 rule6_note 已经正确判定 SKILL.md 改动是「处方性·运行时指令面 → 照跑 AB，零裁量」—— 说明 Spec 自己知道这类内容归 AB 管，但 Impact 表又把 SC-1~3 派给了单元测试。两处不一致。
- **建议修法**: 二选一并写死。(a) **归 AB**: SC-1~3 明确为 `/skill-creator` 的定向 fixture (「给定 spec 头部有关联 Issue 字段的 context，A.1 是否发起了带 `--linked-issue` 的认领」)，并在 Impact 表把这一行从「既有测试 扩展」改成「AB 定向 fixture (新增)」；(b) **归代码**: 新增一个不触碰 `phase1_gate` 的 A.1 preflight 脚本承载断言 (读 spec 头部 → 判定是否必需 → 拼参/拒绝)，此时 SC-3 才有可红对象。无论选哪条，Impact 表「既有测试」四个字必须改 —— 它现在是一句事实错误的成本估计。

---

### [MAJOR] claim 生命周期的对偶未覆盖 A.1 新增的两条退出路径；全文零处提及 release / 释放 / sweep / D.2b

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:82-97` (§1 全段), `:121` (D1)
- **问题**: D1 说「用已 ship 的 claim，不新造检查」，但 acquire 的对偶 release 是**按 Phase D 收尾时机设计**的。把 acquire 前移到 A.1，等于新增了两条 Phase D 永远到不了的退出路径，而 Spec 对此零处置 (全文 `grep -niE "release|释放|sweep|heartbeat|abandon|D\.2b|生命周期"` → **零命中**):
  - **(a) A.1 探索性放弃**: A.1 是探索性最强的阶段 —— 起草者试三个方向、弃两个是常态。每个方向若都认领，被弃的两条永远走不到 D.2b，`release_gate` 永不被调用，留下 active 僵尸 claim。
  - **(b) A.1 认领 id 与 D.2b 释放 id 错配**: §1 行 88 允许 raw-track-id 取「spec-slug **或** carry-id」，而在 A.1 起草**前** spec-slug 往往还没定稿。D.2b 用的是「本 cycle 的 carry-id 原始串」。两串不同 ⇒ `derive_track_id` 结果不同 ⇒ `release_claim_by_track` 按 `(归一 track_id, container)` 定位不到 ⇒ 返回 `claim_not_found` ⇒ 被 `release_gate` 归入 benign、`exit 0`、**完全静默**。claim 留 active。
  - 两条路径的唯一回收器都是那把 24h sweep —— 而那把 sweep 正是 CRITICAL-2 的致因。僵尸 claim 的下游代价是**误报**: 未来任何人对同一 issue 做 A.1 都会收到指向一条早已死掉的轨的 🔴，重复几次之后 AI/人就学会忽略这个告警 (advisory 机制的经典死法)。
- **证据**:
  - `aria/skills/state-scanner/lib/claim_lifecycle.py:422-430` — `matches = [rec for rec in ... if rec.container == resolved.container_id and rec.track_id == norm and rec.status == "active"]`; `if not matches: return AcquireResult(..., error="claim_not_found")`。
  - `aria/skills/state-scanner/scripts/release_gate.py:63` `_BENIGN_RELEASE_ERRORS = frozenset({"claim_not_found"})`; `:131` 标 benign; `:262` `return 1 if result["hard_error"] else 0` ⇒ 错配路径 exit 0。
  - `aria/skills/phase-d-closer/SKILL.md:48` — release 的触发前提原文是「D.2 归档完成后 (或 D.2 跳过但本 session **曾在 Phase B-entry** 经 phase1_gate 认领)」—— 文字上就把 A.1 认领排除在外。
  - `aria/skills/state-scanner/SKILL.md:176` — 现有生命周期闭环成文为「acquire (phase1_gate, **Phase B-entry**) 的对偶是 release (phase-d-closer D.2b)」。前移 acquire 而不动这句，闭环即断。
  - `release_gate.py` 本身支持 `--status abandoned` (`:219` choices)，所需原语已在，缺的只是 Spec 里的调用契约。
- **建议修法**: §1 在新增入口的同时**同段写出退出契约**: (a) A.1 起草放弃 (含试写方向被弃) 时 MUST 跑 `release_gate.py --raw-track-id "<与认领时逐字相同的原始串>" --status abandoned`；(b) 规定「A.1 认领时用的 raw-track-id 即本 cycle 的 canonical carry-id，后续 spec slug 改名**不改** raw-track-id」，并把这条写进 handoff §6 carry-id 的产生规则，使 D.2b 的释放 id 与 A.1 的认领 id 结构上同源；(c) 同步更新 `phase-d-closer/SKILL.md:48` 与 `state-scanner/SKILL.md:176` 的「Phase B-entry」措辞 (Rule #3 文档与代码同步)；(d) 新增 SC「A.1 认领后放弃 → 同 issue 的下一次 A.1 认领 overlap 为空」。

---

### [MAJOR] A.1 认领与 `state_scanner.coordination.enabled/mode` 的关系未写；两种读法各自都坏

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:82-97` (§1), `:139` (SC-3)
- **问题**: Spec 全文没有提到 `coordination.enabled` 或 `coordination.mode`。而**既有的两个 Phase B 入口都成文了 skip 条件**，A.1 入口没有 —— 两种读法都产生真问题:
  - **读法一 (继承 skip_if)**: 显式 opt-out 的项目 A.1 不认领。那么 SC-3 的「可红」必须对这些项目豁免，否则它在 opt-out 项目上恒红 —— 恒红与假绿一样零信息 (memory `feedback_false_green_dual_is_permanent_red`)。Spec 没写这个分支。
  - **读法二 (不继承)**: 显式设了 `enabled=false` 的第三方项目，会在 A.1 被推 `refs/aria/coordination` 到它自己的 origin。这恰恰是 `phase-b-developer/SKILL.md:100-102` 的 `third_party_note` 明确保护的东西 (「单人单终端项目若不想要该 ref，显式设 `state_scanner.coordination.enabled=false`」)，A.1 会绕过该保护。
  - 另外 `mode` 也没交代: §1 行 90 把 `--mode advisory` 写死在模板里，而现有 B 入口是「由 `state_scanner.coordination.mode` 决定」(`state-scanner/SKILL.md:163`)。owner 若把 mode 切到 block，A.1 会与 B 行为不一致。
- **证据**: `.aria/config.json` 实测 `state_scanner.coordination = {"enabled": true, "mode": "advisory"}`；`aria/skills/phase-b-developer/SKILL.md:98` `- coordination.enabled 显式 false (opt-out; 默认 true — config-loader SOT)`；`aria/skills/branch-manager/SKILL.md:151` `**skip 条件**: coordination.enabled 显式 false (默认 true) / 非协调项目`；`aria/skills/state-scanner/SKILL.md:163` mode 由 config 决定。
- **建议修法**: §1 增一个 `skip_if` 块，与 `phase-b-developer` B.0 **逐字一致** (`coordination.enabled` 显式 false / 非 git repo / 无 origin remote)，并显式声明「A.1 与 B.0 共用同一开关，不新增开关面」；`--mode` 从模板里的硬编码改为「读 `state_scanner.coordination.mode`，默认 advisory」；SC-3 补一条前置「仅当 coordination 未 opt-out 时适用」。

---

### [MAJOR] `--repo-path` 指向哪个仓未定；本 Spec 自述「Spec 落主仓 / 代码落 aria 子模块」，两容器各按所在仓传参即分裂成两个 ref，主机制静默零命中

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:92` (`--repo-path "<repo root>"`), `:8` (代码落点声明)
- **问题**: `refs/aria/coordination` 是**每仓一条**的 ref，`--repo-path` 决定 claim 写进哪一条。Spec 模板只写了 `"<repo root>"` —— 而本 Spec 自己就是跨仓场景: 行 8 声明「代码落点 `aria/` 子模块；Spec 落主仓」，行 96 举的 issue 又是 `<repo>#<n>` 跨仓形式 (`aria-plugin#122` 的代码在 `aria/`，spec 在主仓)。容器 A 在主仓根跑、容器 B 在 `aria/` 子模块里跑，是完全自然的两种选择，结果是两条互不可见的 ref，`linked_issue_overlap` 恒空 —— 与 CRITICAL-1 同一类假绿，但成因正交。而且 `write_claim` 的 `auto_bootstrap` 会**静默创建**新 ref 并 push (`phase-b-developer/SKILL.md:96-97` 明确「无 coordination 基础设施不是有效 skip 条件，`write_claim auto_bootstrap` 会自动建 ref 并 push」)，所以分裂不会有任何报错。
- **证据**: `git -C /home/dev/Aria/aria for-each-ref 'refs/aria/*'` → 空 (aria 子模块**目前没有**自己的 coordination ref)；主仓 `git for-each-ref` → `refs/aria` 1 条。历史语料证实跨仓 issue 全部记在主仓那条 ref 上 (主仓 ref 内存在 `10CG/aria-plugin#110/#113/#121`、`aria-plugin#116/#118/#122/#124`)。`aria/skills/state-scanner/lib/coordination_ref.py:720` `auto_bootstrap: bool = True`。
- **建议修法**: §1 钉死一条不变量: **`--repo-path` 恒等于 Spec 所在仓 (即 `openspec/changes/` 所在仓)**，与代码落点无关 —— 理由是碰撞发生在 spec 维度，join 面必须与 spec 同仓。并在 §1 明写跨仓 issue 的 `--linked-issue` 形式 (与 CRITICAL-1 的归一规则合并成一条)。补一条 SC: 「同 issue、两容器分别在主仓与子模块工作 ⇒ 仍在同一条 ref 上互相可见」。

---

### [MINOR] §Why 行 74「两轨都没走到 Phase B，所以谁都没认领过」与 coordination ref 事实相反 —— 而事实其实是更强的论据

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:74`
- **问题**: R 轨确实认领过。这不影响结论 (反事实的承重腿是 L 没认领)，但它把一个更锋利的证据浪费了: R 是在**跑完 4 轮 post_spec 之后**才认领的 —— 这是「认领点太靠后」的**直接生产实证**，比现在的「谁都没认领」更贴合本 Spec 的论点，且不依赖反事实推理。
- **证据**: `git show refs/aria/coordination:claims/bfe8285d/s-6cd0@1153.yaml` →
  ```
  claimed_at: '2026-07-27T11:53:12Z'   container: bfe8285d   owner: simonfish
  linked_issue: aria-plugin#122        phase: B              status: done
  track_id: sha256-0d6bc2125b9d88e4
  ```
  即 R (simonfish/bfe8285d) 于 07-27 11:53:12Z 以 `--phase B --linked-issue aria-plugin#122` 认领，恰在 proposal.md:32 所述「R 于 07-27 11:52 落地远端」之后 1 分钟、4 轮 post_spec 之后。
- **建议修法**: 行 74 改为事实陈述并顺势加强: 「L 全程未认领；R 认领了，但发生在它自己跑完 4 轮 post_spec **之后** (`claims/bfe8285d/s-6cd0@1153.yaml`, 07-27T11:53:12Z) —— 认领点在 Phase B，比碰撞的发生点 (A.1) 晚了整个 Phase A。」
- **附带**: 该 claim 的 `track_id` 是 `sha256-0d6bc2125b9d88e4` (raw id 超 64 字符或含非 ASCII 时 `derive_track_id` 的 SHA fallback，`lib/track_id.py:63-80`)。SC-1 (行 137) 要求告警「列出对方 track-id」，遇到这种 id 时可读性为零。建议 SC-1 的期望里补上 owner/container/claimed_at 之外的**可读线索** (例如把 raw_input_id 也带进 overlap 输出，或规定 A.1 的 raw-track-id 必须 ≤64 ASCII 字符)。

---

### [MINOR] Step 0.5 挂在一个显式「一次性」的 Step 0 旁边，与 D3「每轮跑」自相拉扯

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:101`, `:123` (D3)
- **问题**: `audit-engine/SKILL.md:85` 对 Step 0 的定义原文是「入口逻辑完成后、**Round 1 启动前一次性**执行」，且 `:99` 进一步强调 anchor「审计周期内不可变 —— mid-audit re-anchor 不支持」。把一个必须**每轮**执行的步骤命名为「Step 0.5」并挂在它「旁」，编号与位置双重暗示「跟 Step 0 一起、一次性」。D3 花了一整行论证「每轮而非仅首轮」，却把落点选在整个 Skill 里唯一被明文钉成 once-only 的位置 —— 实现者按位置直觉做成一次性的概率很高，而那恰是 D3 要防的失效。
- **证据**: `aria/skills/audit-engine/SKILL.md:85` (原文如上)；`:99`；`:77` 说明每轮循环发生在阶段 (3)/(4) 的 convergence / challenge 流程内，与 Step 0 不在同一层。
- **建议修法**: 把该步骤从 Step 0 旁移出，挂到**每轮轮首** (阶段 3/4 的 round 起点，`references/execution-modes.md` 的 convergence 4-step 入口)，并另起编号 (例如「每轮 Step R0」) 以免与 once-only 的 Step 0 语义粘连；SKILL.md 文字里显式与 Step 0 对比一句「与 Step 0 (一次性) 不同，本步每轮执行」。

---

### [MINOR] §自指注记陈旧: 代偿停在 07-30，用的正是本 Spec 论证无效的那一招；且本 Spec 自身至今无 claim

- **位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:175`
- **问题**: 三重不自洽。(a) 行 175 声称的人工代偿是「fetch 双远程 + 核实 `openspec/changes/` 无同主题 spec」—— 这**逐字就是**行 48 那条被 §Why 花整节证伪的原建议 (且按 MAJOR-1，它连 archive 都不扫)；(b) 代偿做于 2026-07-30 (SHA `4e034d2`)，而作者在 08-02 编辑本文件时新增了整个 ⭐ 段落 —— 那一段的全部内容就是「07-31 我自己没有重新 fetch」，却没有在同一次编辑里刷新这条代偿；(c) 作者在 08-02 **已经实跑过认领** (D6/D7，对 `aria-plugin#124`)，证明手上有可用工具，但**没有为本 Spec 自己的轨认领** —— coordination ref 全量实测无任何 claim 匹配 `a1-entry|duplicate-work`。也就是说本 Spec 目前对第三方并发起草**零可见性**，这正是它要根治的状态。
- **证据**: 全量 ref 扫描 `for f in $(git ls-tree -r refs/aria/coordination --name-only); do ... grep -qiE 'a1-entry|duplicate-work'; done` → 零命中；`.aria/coordination-telemetry.jsonl` 末行 08-02 的 track_id 是 `aria-plugin-124-path-coverage-z-flag`，非本 Spec。
- **建议修法**: 二选一，别留一次三天前的 fetch 当代偿。(a) 现在就为本轨认领 (`--raw-track-id a1-entry-claim-duplicate-work-guard --phase A.1 --linked-issue <本 Spec 的关联 issue>`)，把 outcome 与 `push_success` 回填进行 175；或 (b) 如实改写为「本 Spec 头部无『关联 Issue』字段，按自身 D2 免传 `--linked-issue`，**因此本轨不受主机制保护**」—— 后者虽然难看，但它把 MAJOR-2 的缺口暴露在承诺面上，与 D4「盲区写进正文」的立场一致。

---

## 收敛建议

- 两条 CRITICAL 都指向同一件事: **主机制的两个承重前提，Spec 只实测了其中一个** (D7 测了「写得进、推得出」，没测「配得上、活得久」)。R2 前建议对这两条各补一次与 D7 同规格的实测 (跨格式 overlap / 跨 24h overlap)，而不是补一段论证。
- MAJOR-2 (谓词未定义) 是 MAJOR-3、MAJOR-1 与 CRITICAL-1 的共同上游 —— 先定义「关联 Issue」字段与 issue token 归一，其余三条的修法才有落点。建议 R1-fix 从它起手。
- MAJOR-4 (退出契约) 与 CRITICAL-2 (存活窗) 必须**一起改**，单独改任一条都会把问题推到另一端。
