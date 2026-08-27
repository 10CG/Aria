---
checkpoint: post_spec
round: 5
role: comment-analyzer
verdict: REVISE
scope_ok: true
counts: 7C/10M/5m (combined, 单席单镜头)
---

# post_spec R5 (末轮) — a1-entry rework v3 + 两份子 Spec · 镜头 = 注释/文档准确性与长期可维护性

> **席位**: 1/1 (借用 `comment-analyzer`) · **模式**: convergence, `max_rounds=5` 末轮
> **对账 SHA**: 主仓 `b0c16ff` (工作树干净) · **基线**: aria 子模块 `d50f9c3`
> **审计对象**: 母 `a1-entry-claim-duplicate-work-guard/proposal.md` (876 行) · 子 `linked-issue-field-availability/proposal.md` (606 行) · 子 `sibling-spec-probe/proposal.md` (557 行)
> **上一轮**: `post_spec-R4-1787764438000-a1-entry-combined-aggregated.md` (9C / ~20M, REVISE 发散)

| Spec | verdict | counts |
|---|---|---|
| 母 `a1-entry-claim-duplicate-work-guard` | **REVISE** | **5C / 4M / 2m** |
| 子 `linked-issue-field-availability` | **REVISE** | **2C / 3M / 2m** |
| 子 `sibling-spec-probe` | **REVISE** | **0C / 3M / 1m** |
| **combined (去重)** | **REVISE** | **7C / 10M / 5m** |

## 本轮的形状 (一句话)

**R4 的 9 条 critical 有 4 条只闭了一半** —— 落版写进了 K1…K9 的诊断 blockquote,
**没有回灌进 §Impact 表 / Success Criteria 表 / 代码落点 三张被 A.2 消费的权威表**;
被诊断为错的原文在权威表里**原样在册**, 于是**同一份文档对同一件事同时给出两个相反规定**。
7 条 Critical 中 **6 条**落在 2026-08-27 新写的 K 段及其未回灌处 —— 即**本轮 fix 自身**。

---

## A. 母 Spec `a1-entry-claim-duplicate-work-guard` — REVISE, 5C/4M/2m

### 🔴 C-1 (Critical) — K3「诚实降级」与四处正文互斥, 且其理由对 3/4 条不成立

- **位置**: `:166-182` (K3 段) · `:642` (SC-2 行) · `:665` (SC-15 行) · `:733` (Impact `tests/` 行)
- **实跑**:
  ```
  $ sed -n '642p' …/a1-entry-claim-duplicate-work-guard/proposal.md | tr '|' '\n' | sed -n '5p'
   代码 (CLI 全链路)
  $ grep -n 'SC-15\*\* (代码)' …/proposal.md
  665:| **SC-15** (代码) | track-id 为**回落形** …
  $ sed -n '733p' …/proposal.md | cut -c1-120
  | `skills/state-scanner/tests/` (既有宿主) | SC-2 / SC-3 / SC-5~8 / SC-10 / SC-14(a) / SC-15 / **SC-22** …
  ```
- **问题**: K3 逐字宣布「**SC-1 / SC-2 / SC-4 / SC-15** …… 一律降级为行为类定向 fixture …… **禁止**把它们写成『代码 (CLI 全链路)』」。而
  (a) SC-2 的**宿主列逐字仍是 `代码 (CLI 全链路)`**; (b) SC-15 的**标题格逐字仍是 `(代码)`**; (c) Impact 表仍把 **SC-2 与 SC-15** 登记在 `skills/state-scanner/tests/` 这个代码宿主里; (d) SC-1/SC-4 的宿主列写「文本层 + 行为层」, 而 §2.1a `:161` 明写文本层「**可机械**」且宿主 = `test_coordination_default_lockin.py` —— 那就是代码类。
  ⇒ 一条 SC 同时被规定为代码类与非代码类, **新读者无法唯一确定当前有效的规定**。
- **降级正当性判定 (owner 点名要我判的第 1 项)**: **不正当, 且方向搞反了**。K3 给四条 SC 用了**同一句**理由 (「它只能由 AB eval 分辨『AI 是否按 §2.1 规则拼串』」), 但:
  - **SC-15** 断言的是「release 旧 + acquire 新两步后**无孤儿**」—— 被测对象是 `release_claim_by_track` (`lib/claim_lifecycle.py:377`, 实存), **与拼串无关**。把它降成 AB eval 等于取消本 Spec 唯一能机械抓住「只 acquire 不 release」的断言;
  - **SC-2** 同一格的 R4/C-1 订正刚写「夹具**手写字面串**是**允许且必要的**……归一仍走 `derive_track_id`」—— 手写串 + CLI 跑 overlap **就是可构造的代码断言**。降级与它自己的夹具硬约束互斥。
  ⇒ 这不是「把做不到包装成设计如此」, 是**把做得到的降级成做不到**, 且**代价未写**。
- **处方 (字符级)**: K3 段的降级名单删去 `SC-15`(理由不适用) 与 `SC-2`(与其夹具硬约束互斥), 只保留 SC-1/SC-4 的**行为层**降级并**显式说明文本层仍是代码类**; 同步把 `:642` 宿主列改 `代码 (CLI 全链路) + 行为层`、`:665` 保留 `(代码)`; `:733` 不动。若坚持降级 SC-2/SC-15, 则必须同批改 `:642` / `:665` / `:733` 三处字面, 并逐条写出各自的降级理由与代价 —— 一句话套四条不可接受。

### 🔴 C-2 (Critical) — R4/K3 点名的 `compose` 字样**至今未删**, 而订正段自称已删

- **位置**: `:642` SC-2 行负控臂 (ii) · 订正叙述在同格与 `:171`
- **实跑**:
  ```
  $ grep -n "compose" …/a1-entry-claim-duplicate-work-guard/proposal.md
  171:> (R3 主控还一度把 SC-2 的夹具约束写成「必须由 §2.1a 的 compose 函数派生」…… 已订正。)
  642:… (ii) **把 compose 的 container 段置空重跑同一夹具 ⇒ 双方 overlap 必须变空** (负控) …
  ```
- **问题**: 同一格的 R4/C-1 订正逐字写「全文 grep `compose` 仅命中 SC-2 自身 ⇒ **SC-2 引用了一个本 Spec 明说不存在的函数**……**订正后**: 夹具手写字面串是允许且必要的」。**订正只改了前半句的出处措辞, 负控臂 (ii) 里的 `compose` 原样留着** —— 实现者构造 (ii) 时**仍然找不到可 import 的对象**。
  R4 聚合报告 K3 行已逐字点名这一处 (「主控的订正只换了夹具出处措辞, **没换被测的量**……且**臂(ii) 仍留「compose」字样**」) ⇒ 这是**已被上一轮点名、清账 commit 声称已清、实际未清**的 critical (memory `fix-the-class` / `cite≠apply`)。
- **处方**: `:642` 臂 (ii) 改为「把**手写串**的 `<container_uuid>` 段置空重跑同一夹具」。

### 🔴 C-3 (Critical) — K2 的落版与 §Impact 表给出**相反**的 legacy 行为 (R4/K2 只闭一半)

- **位置**: `:450-457` (K2) vs `:721` (Impact `claim_schema.py` 行)
- **实跑**:
  ```
  $ sed -n '453p'  → **落版 (2026-08-27, 未经审计轮)**: `track_form is None` ⇒ **不释放, 报错退出并点名该 claim**, 要求操作者显式传 `--spec-slug` 或 `--force-legacy-release-all` 二选一。
  $ sed -n '721p'  → | `skills/state-scanner/lib/claim_schema.py` | …(`"issue"`/`"slug"`; 缺省 `None` ⇒ 形态未知 ⇒ **fail-CLOSED 退回现状并 log**) …
  ```
- **问题**: K2 逐字判定「此处原写『fail-CLOSED』是**错的命名**……『退回 ALL matching』正是 §5.3 自己逐字否决过的**连坐**, 它是 **fail-OPEN**」。而 §Impact 表**至今逐字写着 K2 判为错的那句**。R4/K2 的原文是「**同一条 legacy claim 两个相反答案**」—— 该缺陷只是从 §5.1↔§5.3 迁移到了 §5.1↔§Impact。
- **连带**: `--force-legacy-release-all` 全文只出现在 K2 段 (`:454`/`:457`); §Impact 的 `release_gate.py` 行 (`:724`) 只有 `--spec-slug` ⇒ 从 Impact 表派生任务会漏掉该 flag, 而 **SC-31 的第二臂正是它**。
- **处方**: `:721` 括号内改为「缺省 `None` ⇒ 形态未知 ⇒ **拒绝释放并非零退出**, 要求显式 `--spec-slug` 或 `--force-legacy-release-all`(见 §5.1 K2)」; `:724` 补 `--force-legacy-release-all`。

### 🔴 C-4 (Critical) — K1/K4 的「透传面逐条枚举」与 §Impact 表并存且不一致; K4 诊断的缺口在权威表里原样存在

- **位置**: `:514-531` (K 表 8 行) vs `:719-747` (§Impact 表)
- **逐条对账 (本席实跑 grep)**:

  | K 表 item | §Impact 表 |
  |---|---|
  | 3 `claim_lifecycle.py::heartbeat` `:244-256` 逐字段重建**必须加两行** (**K1 本体**) | 两条 `claim_lifecycle.py` 行 (`:722`/`:727`) **均未提** |
  | 5 `lib/gc.py` (sweep 改写 status 时同步) | **无 `gc.py` 行** (`grep gc.py` 在 `:719-747` 零命中) |
  | 6 `phase1_gate.py` 新增 `--spec-slug` (**K4 本体**) | 两条 `phase1_gate.py` 行 (`:731`/`:732`) ①–⑤ **无该 flag** |
  | 8 `tests/` 两字段往返测试 (SC-30) | `tests/` 行 (`:733`) 止于 SC-29 |

- **问题**: K4 自己写的诊断「**Impact 原只给 `release_gate.py` 加 `--spec-slug` (读取端)……⇒ 写入端缺失, SC-27(C) 的 CLI 全链路夹具不可构造**」—— 在 §Impact 表里**至今为真**。修复落在诊断段内的**第二张表**, 从未回灌唯一被 A.2 消费的那张。两张变更面表并存, 本身就是下一次漂移的种子。
- **处方**: 把 K 表 8 行**逐行并入** §Impact 表 (或反之), 全文只保留**一张**变更面表; K 段只留「为什么」。

### 🔴 C-5 (Critical) — SC-30 / SC-31 / SC-32 / SC-33 只存在于 K 段, **Success Criteria 三张表里一行都没有**

- **实跑**:
  ```
  $ grep -n "SC-30\|SC-31\|SC-32\|SC-33" …/proposal.md
  182:… 未降级的相邻条目 …: SC-23 … / **SC-30** / **SC-31**。
  235:… **新增 SC-32 (代码)** …            (K7 段内)
  321:… **新增 SC-33 (代码, CLI 全链路)** … (K5 段内)
  456:… **新增 SC-31 (代码)** …            (K2 段内)
  526,531:… (见 SC-30) / **新增 SC-30 (代码, 往返)** … (K1 段内)
  ```
  Success Criteria 的三张表 (`:637-644` / `:659-668` / `:678-698`) 最后一行是 **SC-29**; Impact 的测试宿主行 (`:733`) 同样止于 SC-29。
- **问题**: 本文件自己的「编号纪律」写「SC 编号**只追加**……迁出的保留行号并写明去处, 撤销的保留行号并标 ⛔, **不删行**」—— 其意图是 SC 表 = 完整清单。四条新 SC 不进表 ⇒ A.2 逐条派生验收任务时**必漏 4 条**, 其中 **SC-30 是 K1 的验收本体** (该段自陈「**缺它则 K1 的修复无法证伪**」)。
- **处方**: 在「rework v3 新增」表后追加「R4-fix 新增」小节, 把 SC-30…SC-33 按同体例 (类/场景/期望/怎么会红) 各补一行; `:733` 的测试宿主行同步补 `SC-30 / SC-31 / SC-32 / SC-33`。

### 🟠 M-1 (Major) — 轮次脚手架整体落后 1–2 轮, 交付面里塞满「给当时的审计席看」的段落

- **实跑**:
  ```
  $ grep -n "待 post_spec R3\|给 R3 审计席\|请 R4 优先审\|供 R4 复核" …/proposal.md
  3:> **Status**: … **待 post_spec R3 (convergence 续审, `max_rounds` 剩 2)**
  537:… 该替代方案与其残余窗口一并成文, 供 R4 复核本裁断。
  539:> **⚠️ 本条是 rework v3 之后新增的设计裁断 (主控 2026-08-25), 未经任何审计轮** —— 请 R4 优先审。
  812:> … **本段是给 R3 审计席的输入, 不是完成度自述。**
  828:### R3 清账轮 … **新引入且未经任何审计**的表面 — 请 R4 优先审
  840:## 本轮未做 / 存疑 (给 R3 审计席)
  ```
  另「闸门状态」item 5 逐字「**下一步**: 本版进 **post_spec R3**」。实际 R3 (`post_spec-R3-1787652625000-*`) 与 R4 (`post_spec-R4-1787764438000-*`) 均已跑完, 现为 **R5 末轮**。
- **问题 (长期可维护性, owner 点名要我判的第 4 项)**: 上述 4 段 (`:812` 新表面 / `:828` R3 清账轮 / `:840` 未做存疑 / 各处「请 R4 优先审」) 是**写给某一轮审计席的**, 不是写给实现者的; 它们既已过期又占据交付面。母 Spec 已经为同一理由把审计轨切出去 (memory `audit-trail-not-in-spec`), 而 R3/R4 的清账动作**又把同形内容追加了回来**。
- **处方**: Status 行改「待 post_spec **R5** 裁决 (末轮)」; 闸门状态 item 5 改为「R3/R4 已跑, 现 R5 末轮」; `:812` / `:828` / `:840` 三段整体移进 `.aria/audit-reports/a1-entry-claim-audit-trail.md` (新增 §6「rework v3 / R3 清账 / R4 清账 的未审表面与存疑」), 正文只留一行指针。**K1…K9 九段同理**: 「诊断 + 实跑证据」移轨, 「落版」进权威表。

### 🟠 M-2 (Major) — K6 承诺的 follow-up 没有落点

- **实跑**: `grep -n swept …/proposal.md` ⇒ **仅 `:285` 一处** (K6 段内)。§Impact 的 follow-up 表 (`:755-761`) 6 条无此项。
- **问题**: K6 逐字「给 `ClaimRecord` 加 swept 标记以真正分辨二者, **记 follow-up**, 不在本 Spec」—— 「记 follow-up」是一个**没有接收者**的自述 (memory `feedback_completion_signals_vs_runtime_invocation` 同形)。
- **K6 降级正当性判定 (owner 点名要我判的第 2 项)**: **正当**。前提经本席复核为真 —— `git -C aria show d50f9c3:skills/state-scanner/lib/claim_schema.py | sed -n '120,131p'` 显示 `ClaimRecord` 11 个字段**确无 swept**; `lib/gc.py:324` 逐字 `Number of stale active claims rewritten to ``status='abandoned'``` ✓。把不可分辨的两种来源**统一按 `active` 请裁**是「零证据不得当正证据」的正确方向, **代价也写了**(「用一次多余的请裁换不误判对方已退出」)。只欠 follow-up 落点。
- **处方**: §Impact follow-up 表补第 7 行「`ClaimRecord` 增 swept 标记以分辨 GC 产物与自愿 release (K6; 不在本 Spec: 改 schema 需与 `coordination-ref-schema.md` §3 演进契约同批评估)」。

### 🟠 M-3 (Major) — K7 的落版未回灌 Impact, 被它判为「空信号」的原文仍在权威表里

- **实跑**:
  ```
  $ git -C aria grep -n "def log(" d50f9c3 -- skills/     → 零命中 (K7 前提属实)
  $ git -C aria grep -ln "basicConfig" d50f9c3 -- skills/state-scanner/ → 仅 scripts/scan.py (属实)
  $ sed -n '732p' …/proposal.md → | `…/phase1_gate.py` (第二处变更…) | 新增 **`--heartbeat-only` 模式**… (**来源 = handoff §6 结构化 carry-id, 取不到则跳过 + log, 不猜**) …
  ```
- **问题**: K7 (`:235`) 逐字判「原文写『跳过 + `log()`』是个空信号」并落版为「**每次调用都向遥测 JSONL 追加一条 `_source="heartbeat"` 记录**」+ SC-32。§Impact `:732` **仍逐字写「取不到则跳过 + log, 不猜」**; `coordination_probe.py` 行 (`:723`) 也只写「仅口径声明/注释」, 未登记新的 `_source="heartbeat"` 分区写入方。
- **处方**: `:732` 把「跳过 + log」改为「跳过并向遥测 JSONL 追加 `_source="heartbeat"` / `outcome="skipped_no_track"` 记录 (K7; 由 SC-32 钉住)」; `:723` 补「新增 `_source="heartbeat"` 分区的写入约定」。

### 🟠 M-4 (Major) — §瓶颈 的「可当场复核」现状句复核即错

- **实跑**:
  ```
  $ grep -rlE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/changes/ | wc -l
  3        # 母 + linked-issue-field-availability + sibling-spec-probe
  $ find openspec/changes -name proposal.md | wc -l → 9      (母 :78 写 7)
  $ find openspec -name proposal.md | wc -l        → 149     (母 :76 写 147)
  ```
- **问题**: `:82` 逐字「**落盘后的现状 (可当场复核)**: ……⇒ `changes/` 下的 **1 条**命中现在是真阳」。实际 **3 条**。`:76-78` 的 `147/15/7` 标注了 `cc1bdef` 口径尚可, 但 `:82` 是**明确邀请当场复核的现在时断言**, 复核即不符。姊妹 Spec 同批已把「**口径 (命令) 才是规范, 数字是当日观测**」写成硬约束并给出 `149/17/9` —— 母 Spec 这一句是同批测量里唯一没跟上的 (memory `past-summary≠measurement`)。
- **处方**: `:82` 改为「⇒ `changes/` 下现有 3 条真阳 (母 + 两子 Spec, 均为 dogfood 的 `无`); **数字是当日观测, 复核以上方命令为准**」。

### minor

- **m-1** `:656` SC-11 逐字「措辞按 status 分档 (§2.3 选项表: `active`/`done`/`abandoned`/`unknown` **四档选项集不同**)」—— K6 已把 `abandoned` 的**选项集并入 `active` 同档**, 现为 3 个不同选项集 + 1 条附加措辞标注。照字面建 fixture 会去分辨一个已被合并的档。建议改「四档**渲染**不同, 其中 `abandoned` 与 `active` **共用选项集**、仅附加『可能是 GC 产物』标注 (K6)」。
- **m-2** `:442-460` §5.1 判定式段现由「两个判定式否决 → 主控误判留痕 → `track_form` 落版 → K2 订正落版」四层叠成, 且 D12 (`:600` 一带) 第三列还各自复述一遍。**当前有效的规定要读四段才能确定**。建议: 判定式正文只留「`track_form` 字段 + `None` ⇒ 拒绝释放并非零退出」两句, 其余三层 (含误判留痕) 移审计轨。

---

## B. 子 Spec `linked-issue-field-availability` — REVISE, 2C/3M/2m

### 🔴 C-1 (Critical) — K8 新增的 SC-9 既不在 SC 表、也不在「验证宿主」表 —— 本 Spec 自己点名的病第三次复发

- **实跑**:
  ```
  $ grep -o "\*\*SC-[0-9]*\*\*" …/linked-issue-field-availability/proposal.md | sort -u -V
  **SC-1** … **SC-8**            # 表内只有 8 条
  $ grep -n "SC-9" …/proposal.md
  213:> **新增 SC-9 (代码, CLI 全链路)**: 两份 proposal 的字段值都是模板 placeholder … (K8 段内, 唯一一处)
  ```
  `:505-517` 的「⛔ 验证宿主 (R3/QA-F6)」表列 SC-1~4 / SC-5 / SC-6 / SC-8, **无 SC-9**。
- **问题**: 该表存在的全部理由是它自己写的「R3/QA 判定: 本 Spec 的 SC-1~6 / SC-8 全部标『代码』类却**没有一条声明测试宿主** …… **同一个病在这里复发了**」。K8 又新增了一条无宿主的代码类 SC ⇒ **同一个病, 在修 R4 的动作里再复发一次**。
  更重: SC-9 的场景是「两份 proposal 经 **A.1 认领**后 `linked_issue_overlap[]` 互不命中」—— 被测对象是**母 Spec 的 CLI 全链路**, 而本 Spec `:540` 逐字「**不改** `aria/skills/state-scanner/` 下的任何一行代码 —— `collision.py` / `phase1_gate.py` 均**零改动**」⇒ 宿主与归属**两头都没有**。
- **处方**: SC 表补 SC-9 一行 (类/场景/期望/怎么会红); 「验证宿主」表补一行 —— 若宿主定在 `aria/skills/state-scanner/tests/test_linked_issue_field.py` 则须写明它**只跑纯函数 + 构造两个 verdict, 不跑 A.1 CLI**; 若确需 CLI 全链路, 则该 SC 应归母 Spec (母 Spec 拥有 `--linked-issue` 实参面, 见下条)。

### 🔴 C-2 (Critical) — K8 改写了**母 Spec 声明归自己所有**的 CLI 实参契约, 母侧至今未同步

- **位置**: 本 Spec `:195-225` (K8) vs 母 Spec `:110-122` (§2 NEW-01 blockquote) 与母 §6 缺口表首行
- **母 Spec 逐字 (`:122`)**: 「**rework v3 归属**: 『字段值为 `无` 时怎么写』归 `linked-issue-field-availability`; **『实参必须省略 `--linked-issue`』是 CLI 调用面, 留在本 Spec**」。
  本 Spec `:214` 亦逐字自陈「(母 Spec §2 的 NEW-01, **逐字引母 Spec, 本 Spec 不重定义**)」。
- **问题**: K8 把 `--linked-issue` 的门**从「等于 `无`」扩为按 verdict 四档**(`BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律省略) —— 这是 CLI 实参面的**实质重定义**, 落在被声明为「不重定义」的一侧; 而母 Spec 的 §2 blockquote 与 §6 缺口表首行**至今只覆盖「`无` 或字段缺席」**, 不含「照模板新建、还没填号 ⇒ `BAD_TOKEN` ⇒ 必须省略」这条**触发条件更弱**的新缺口 (K8 自陈「`无` 还要作者主动写, placeholder **什么都不做就中**」)。
  ⇒ 只读母 Spec 的实现者会照母 §2 只挡 `无`, 于是 R4/K8 这条 critical 在**主机制侧原样存在**。
- **处方 (两侧同批)**: 母 Spec `:110` 的 blockquote 标题改为「token 不合规 (含 `无` / placeholder / `NO_TOKEN`) 时: 整个 `--linked-issue` 参数必须省略 —— 分档判据见子 Spec E6 四态表」; 母 §6 缺口表首行的缺口描述由「token 为 `无` 或字段缺席」扩为「token 不产生合法 canonical 值 (`无` / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD`)」。

### 🟠 M-1 (Major) — 头部「代码落点」未随 R3/C3 更新, 且与 §非目标 自相矛盾

- **实跑**:
  ```
  $ sed -n '7p'  → **代码落点** (**三个仓**): `standards/…proposal-minimal.md` + `aria/` … `skills/spec-drafter/SKILL.md` 与 `skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**) + 主仓 `.aria/state-checks.yaml`
  $ sed -n '540p' → - **不改** `aria/skills/state-scanner/` 下的任何一行代码 —— `collision.py` / `phase1_gate.py` 均**零改动**;
  ```
  而 §Impact 表**首行**是 `aria/skills/state-scanner/lib/linked_issue_field.py` (**新建**, R3/C3), `.aria/linked-issue-field-grandfathered.txt` (**新建**, R3/C2) 亦不在 `:7` 的落点清单里。
- **问题**: 头部落点清单是 A.2 划分仓/任务的第一手输入, 现落后于 §Impact 两个新建文件; §非目标那句「不改 `state-scanner/` 下的任何一行代码」与「在该目录下新建一个模块」并列成文。
- **处方**: `:7` 补 `skills/state-scanner/lib/linked_issue_field.py` (新建) 与主仓 `.aria/linked-issue-field-grandfathered.txt` (新建); `:540` 限定为「**不改**该目录下**任何既有文件** (`collision.py` / `phase1_gate.py` 零改动); 新增 `lib/linked_issue_field.py` 属本 Spec 交付面 (R3/C3)」。

### 🟠 M-2 (Major) — SC-5 的臂数在同一份文档里有**三个**互不相同的值

- **实跑**:
  ```
  $ grep -n "判据分区\|判据分割" …/proposal.md
  411:**探针的判据分割 (fail-CLOSED, 五臂)**:          # 表体实测 5 行
  513:> | SC-5 (探针判据分区五臂) | …                     # 验证宿主表
  528:| **SC-5** | 代码 | **探针判据分区四臂**。(a)…(d) … **(e)** …(e1)/(e2)  # 实际 6 条断言
  ```
- **K9 降级正当性判定 (owner 点名要我判的第 3 项)**: **正当且必要**。K9 抓到的矛盾经本席复核成立 —— 本仓 `.aria/linked-issue-field-grandfathered.txt` 今天不存在, 而作用域 9 份含 6 份 `NO_FIELD` ⇒ 原措辞「文件不存在 ⇒ 不得 exit 1」在本仓**必然为假**; 「照字面消解 = `rm` 一条命令永久静默整条 enabled check」的推理正确。e1/e2 拆分把「不得因读不到白名单而中止」与「仍须对不合规项 exit 1」分开, 是**换量而非调阈值**, 代价也写清了。
- **残余问题**: 拆分**没更新臂数**, 也没把「白名单文件缺失」补进 `:411` 那张五臂判据表 ⇒ 照「四臂」建测试会漏 2 条; 照 `:411` 的表实现会缺一整臂。
- **处方**: `:528` 的「四臂」改「**六臂**」并把 (e1)(e2) 提为独立臂; `:411` 表补第 6 行「`--grandfathered` 缺省或文件不存在 ⇒ 白名单视为空集, **照常判定**(不因此报错); 其余按上方各行」; `:513` 的「五臂」同步。

### 🟠 M-3 (Major) — 轮次脚手架落后

- `:3` Status 逐字「**待 post_spec R1**」; `:242` / `:362` 两处「本条是 R3 之后新增的…… **请 R4 优先审**」。实际本文件已随母 Spec 过 R3 联审 (作为两子 Spec 的 R1, 见 `post_spec-R3-1787652625000-*`) 与 R4 (`post_spec-R4-1787764438000-*`), 现为 R5 末轮。处方同母 M-1。

### minor

- **m-1** `:409` 引「`collectors/custom_checks.py:63` 自陈…… 且 `:122-123` 逐字『This is a narrow parser — it / intentionally rejects YAML features outside the documented schema.』」。实读: `:63` ✓, 但 **`:122` 是空行**, 该句在 **`:123-124`**。改 `:123-124`。
- **m-2** 命名漂移: R3/C2 已把白名单从**脚本内常量**改为**仓本地数据文件** (`--grandfathered <path>`), 但 `:411` 判据表 (三处)、D6、check 骨架 `description` 仍把 `GRANDFATHERED` 当机制名用 (骨架逐字「存量不合规项经 **GRANDFATHERED 具名白名单**在册」)。建议全文统一为「grandfathered 清单 (**仓本地文件**, 缺省即空集)」, 避免实现者回头去脚本里找那个常量。

---

## C. 子 Spec `sibling-spec-probe` — REVISE, 0C/3M/1m

### 🟠 M-1 (Major) — `bad_token` vs `bad_token_union` 的枚举漂移**第二轮仍未修**, 处置是「声明优先级」而不是改那 6 个字符

- **实跑**:
  ```
  $ grep -n "bad_token" …/sibling-spec-probe/proposal.md
  111:| **`BAD_TOKEN`** | … | `"bad_token"` **⚠️ R4/C-M3 + 姊妹 K8 交叉补** …          # §3 映射表
  328:| `own_layer` | … | **`"bad_token_union"`** … **⚠️ R4/C-M1 拼写统一**: 本枚举值逐字为 `"bad_token_union"`; §3 映射表若出现 `"bad_token"` 一律以本表为准 (R3/TL-P2 只修了一侧) |
  ```
- **问题**: R3/TL-P2 修了一侧, R4/C-M1 发现另一侧仍错 —— 处置却是在 §7 加一句**优先级声明**, 而不是把 `:111` 的 `"bad_token"` 改成 `"bad_token_union"`。两个独立实现者从两节各自取值会写出不同的枚举字面 (memory `spec-underdetermination`: 承重算法必须钉到字符级)。**声明「以本表为准」本身就是漂移仍在的证据。**
- **处方**: 直接改 `:111` 为 `"bad_token_union"`, 并**删掉** `:328` 的优先级声明句 (保留「R4/C-M1」的订正留痕移审计轨)。

### 🟠 M-2 (Major) — K8 交叉补出的 SC-19 只在 §3 表格单元内, 且与全文 4 处「旧 SC-19」**同名不同义**

- **实跑**:
  ```
  $ grep -n "SC-19" …/proposal.md
  69:   > 母 Spec 旧 **SC-19(b)** … 不迁入本 Spec
  111:  … **新增 SC-19**: 两份 proposal 字段值均为该 placeholder ⇒ **不命中** …   # 唯一定义处, 在表格单元内
  466:  > **编号说明**: … 本 **SC-5 / SC-6** 承接旧 **SC-19** 的 (a)(c) 两项 …
  476:| **SC-5** (旧 SC-19a) | …
  477:| **SC-6** (旧 SC-19c) | …
  ```
  Success Criteria 表实体行为 **SC-1…SC-18**, 无 SC-19 行。
- **问题**: (a) 与母 Spec 的 SC-30…33、姊妹的 SC-9 **同一形状** —— R4-fix 新增的 SC 不进 SC 表, A.2 派生必漏; (b) 本文件的「编号说明」明确把 `SC-19` 用作**母 Spec 旧编号**的指代 (4 处), 现在本地命名空间又出现一个 `SC-19` ⇒ 同一份文档里 `SC-19` 有两个所指。
- **处方**: 新 SC 编号取 **SC-20** (避开与「旧 SC-19」的同名), 在 SC 表末补一行; `:111` 单元格只留一句「由 SC-20 钉住」; 「编号说明」补一句「本文出现的 `旧 SC-NN` 一律指母 Spec 编号, 本地 SC 从 SC-1 起」。

### 🟠 M-3 (Major) — 轮次脚手架落后

- `:3` Status 逐字「**待 post_spec R1**」; `:138`「本条是 R3 之后新增的订正 (未经审计轮) —— **请 R4 优先审**」。实际已过 R3 (作为子 Spec R1) 与 R4, 现 R5 末轮。处方同母 M-1。

### minor

- **m-1** `:543` 「本轮引入的新表面」#6 段首已按 R3/M7 更新为「**该风险已闭环**」, 但同段保留的原始留痕以「**这是本轮最实的跨 Spec 风险。**」结尾。两句相邻且都用现在时, 快读会取到相反结论。建议把「以下为当时的原始记述 (留痕)」整段移进 `sibling-spec-probe-audit-trail.md`, 正文只留「已闭环 + 指针」。

---

## D. 正面发现 (可作范例, 且下轮不必重查)

1. **~55 条 `文件:行号` 断言经本席逐条实读, 零漂移。** 覆盖 `collision.py` 230-234/265-266/268/272-275/278-279 · `claim_lifecycle.py` 228/244-256/274/377/396-399/425-430 · `constants.py` 32/36/40-44/50-51 · `identity.py` 191/222/242/244 · `track_id.py` 61/70-76 · `claim_schema.py` 130/165/222-229 · `gc.py` 324/338-344 · `release_gate.py` 141/225/236-237 · `coordination_ref.py` 119/596 · `phase1_gate.py` 56/210/283-294/335/1032/1173/1191/1229-1240 · `phase-b-developer/SKILL.md` 86-96 · `branch-manager/SKILL.md` 146-152 · `phase-d-closer/SKILL.md` 42/51-56 · `spec-drafter/SKILL.md` 9/10/30/369/429 · `phase-a-planner/SKILL.md` 9 · `state-scanner/SKILL.md` 119/149/176 · `layer-l-integration.md` 15/45 · `config-loader/SKILL.md` 134/140 · `coordination-ref-schema.md` 129/133-139 · `test_coordination_default_lockin.py` 53/55-56 · `test_release_by_track.py` 380/533 · `coordination_probe.py` 4-25/80-85 · `custom_checks.py` 63/399 · `handoff_autofill.py` 48-51/403-407 · `fetch_gate.py` 21/23/50-55/111-112/124-127 · `multi_remote.py` 255/286 · `run_all_tests.sh` 48/50/71 · `execution-modes.md` 84/113 · `report-format.md` 50 · `audit-engine/SKILL.md` 83/85 · `DEFAULTS.json` 124-128 · `standards/conventions/session-handoff.md` 101/217/238。
   环境侧同样零偏差: `ab-suite/*.json` **31** 个 · `phase-a-planner`/`spec-drafter` evals **2/2** · `state-scanner` evals **12** · `audit-engine.json` **不存在** · `DEFAULTS.json` 的 `state_scanner` 段**无 `coordination`** · `.aria/state-checks.yaml` **11** 条 · `audit-engine/` **8 个文件, 无 `scripts/`/`tests/`** · `sync.py` 8 个顶层 def **无 `_resolve_default_branch`** · `git -C aria grep "def log("` **零命中**。
2. **「34 行整表已切出」这条自述属实。** 实跑 `.aria/audit-reports/a1-entry-claim-audit-trail.md` §5 得 **34 行, id 1–34 连续**; 母 Spec 正文 6 处「见清单 #N」(#22/#26/#28/#29/#30/#33) **全部可解析**。这是三份文档里体量最大的一次搬运, 且**没有**留下悬空引用 —— 与本报告 C-3/C-4 的「修在别处不回灌」形成对照, 说明**整体搬运比逐条订正安全**。
3. **K8 的跨 Spec 交叉点名是唯一一处「要求他方同批改」并真的两侧都落的例子**: 姊妹 K8 (`linked-issue-field-availability:225` 一带) 要求「探针 Spec 须同批加一条: 原串键不得由 `BAD_TOKEN` 的常量串产生」, `sibling-spec-probe:111` 已含常量黑名单条款。**这是本批文档处理接缝的正确示范** (对比母 Spec C-2/C-3/C-4 的单侧修复)。
4. **child2 的 R4 行号订正逐条准确**: `fetch_gate.py:23→:21` 的订正经本席实读确认 (`:21` = `state-scanner sync.py::_resolve_default_branch (module-private, other skill).`, `:23` = `state-scanner git.py — but the original locks ``@{upstream}``;`), 且「`sync.py` 无该函数」独立成立。**订正本身没有引入新错**, 是本批订正里质量最高的一类。

---

## E. 收敛判断 (末轮要求)

### E.1 与 R4 的可比性 — 先说清口径

**不能直接相减。** R4 = **5 席 5 个镜头**, 去重后 9C / ~20M; 本轮 R5 = **1 席 1 个镜头**(注释/文档准确性), 7C / 10M / 5m。总体、范围、计数法三项都不同 (memory `critique-repeats-error`)。
**可比的只有一件事**: R4 的 9 条 critical 里, 落在本镜头内的 **K1 / K2 / K3 / K4 / K7 五条**, 本席逐条复核其清账结果。

### E.2 可比结论: R4 critical 的清账率, 本镜头内 **1/5 完全闭合**

| R4 critical | 落版是否写下 | 是否回灌权威表 | 本轮判定 |
|---|---|---|---|
| **K1** (字段活不过 heartbeat) | ✅ K 表 item 3 | ❌ §Impact 两条 `claim_lifecycle.py` 行均未提; 验收本体 SC-30 不在 SC 表 | **未闭** (C-4 / C-5) |
| **K2** (`track_form=None` fail-OPEN) | ✅ `:453` | ❌ §Impact `:721` 仍逐字写它判为错的「fail-CLOSED 退回现状」; `--force-legacy-release-all` 不在 Impact | **未闭** (C-3) |
| **K3** (SC-2 恒绿 / 派生无宿主) | ✅ `:166-182` | ❌ 宿主列/标题格/Impact 三处相反; **R4 逐字点名的「臂(ii) 仍留 compose 字样」原样未删** | **未闭且理由不成立** (C-1 / C-2) |
| **K4** (无写入路径) | ✅ K 表 item 6 | ❌ §Impact 两条 `phase1_gate.py` 行无 `--spec-slug` —— **K4 自己写的诊断至今为真** | **未闭** (C-4) |
| **K7** (skip+log 空信号) | ✅ `:235` + SC-32 | ❌ §Impact `:732` 仍写「跳过 + log」; SC-32 不在 SC 表 | **未闭** (M-3 / C-5) |
| K5 / K6 / K8 / K9 | ✅ | 部分 (K6 欠 follow-up 落点; K8 欠母侧同步; K9 欠臂数与 §4 表) | K5 **闭合**; 其余半闭 |

⇒ **本镜头内: critical 由 5 条 → 5 条 (内容未换, 形态从「设计缺陷」变成「落版未回灌」)。** 这不是下降。

### E.3 缺陷形状高度同一 —— 且是**本轮 fix 自身**造成的

本报告 7 条 Critical 中 **6 条**、10 条 Major 中 **6 条**, 落在 **2026-08-27 新写的 K 段及其未回灌处**。形状只有一个:

> **「诊断 + 落版」写进 append-only 的 K blockquote, 权威表 (§Impact / SC 表 / 代码落点) 不动 ⇒ 同一件事两个相反规定并存。**

这正是母 Spec 自己引用并据以切出审计轨的 memory `audit-trail-not-in-spec`(**是 append-only 性质在造耦合**)。**R3/R4 两次清账把同形内容又追加了回来** —— 换句话说, 这三份文档已经证明: **在收敛型交付面里用追加式订正修 finding, 每修一轮就新造一批同形缺陷。**
判据侧: memory `stop-adding-rounds`(major 持平即不收敛) 与 `marginal-return-negative`(本轮 fix 引入的 major 占比 > 1/2 即到拐点) **连续第二轮同时命中**; R4 已有两个独立席位主动建议「已过拐点, 不要再加通用审计轮」。**本席独立得出同一结论。**

### E.4 是否可进 A.2 — **不可, 但也不该再加审计轮**

**结论: 现状不可进 A.2**(权威表与 K 段对同一件事给出相反规定, A.2 从哪张表派生任务就会实现哪一版), **但剩余工作是机械的, 不是设计的**。三份 Spec 的**设计结论本身**经本轮逐条实读未发现事实错误 —— ~55 条行号断言零漂移, K6/K9 两处降级判为正当, 接缝有一处 (K8) 是正确示范。

**建议的下一步 (替代第 6 轮通用审计)**:

1. **一次机械清账 (不是审计轮)** —— 三张权威表回灌, 逐条可验:
   - §Impact 表并入 K 表 8 行 (母 C-4)、改 `:721` fail-CLOSED 措辞 (母 C-3)、`:724` 补 `--force-legacy-release-all`、`:732` 改「跳过 + log」(母 M-3)、补 follow-up swept 行 (母 M-2);
   - SC 表补 母 SC-30/31/32/33、子1 SC-9、子2 SC-20(原「新增 SC-19」);
   - 三处字面: 母 `:642` 删 `compose`(C-2)、母 `:642`/`:665`/`:733` 与 K3 名单二选一 (C-1)、子2 `:111` 改 `bad_token_union`(C 篇 M-1);
   - 两侧同批: 母 §2/§6 扩 `--linked-issue` 省略门 (子1 C-2)。
2. **验收换机械断言, 不换人眼** (memory `redfix-change-quantity`: 换量而非调阈值)。三条可当场跑的 grep 不变量:
   - `每个在正文出现的 SC-NN, 必须在 Success Criteria 表内有一行` (母/子1/子2 各跑一次, 今天分别红 4 / 1 / 1 条);
   - `每个在正文出现的 --<flag>, 必须在 §Impact 表出现至少一次` (今天红 `--force-legacy-release-all` / `--spec-slug`(phase1_gate 侧));
   - `同一枚举值在全文只有一种拼写` (今天红 `bad_token` vs `bad_token_union`)。
   三条今天**全红**, 清账后**全绿**, 且对「只改一处」的坏清账**必红** —— 这是本 Spec 反复要求的「基线亲跑三态」(memory `check-runs-at-baseline-first`)。
3. **K1…K9 与四段「给审计席」的内容移进已有的三份审计轨**, 正文只留落版与指针 —— 否则 A.2 期间每追加一条订正就会重演本轮的形状。
4. **上呈 owner 的两点** (Rule #10, 本席不自裁): (i) **K3 降级名单是否撤回 SC-2/SC-15** —— 本席判其理由不成立, 但改 SC 类别属范围决策; (ii) **是否以「机械清账 + 三条 grep 不变量」替代第 6 轮通用审计** —— 判据已连续两轮命中拐点, 但「不再加轮」本身是闸门决定, 不由 AI 落定。

**若 owner 裁定按上述 1–3 清账**: 本席认为清账后 (三条 grep 不变量全绿 + 母 §2/§6 与子1 K8 双侧同步落地) **即可进 A.2**, 不需要再跑一轮通用审计。
