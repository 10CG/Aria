# post_spec R1 (重写版 v2) — code-reviewer

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=6 major=9 minor=5

> **审查视角**: 欠定检测 + 条款交叉一致性 (「这份规格交给两个独立实现者, 他们会做出同一个东西吗」)。
> **被审对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (Level 2, 全文 328 行, 重写版 v2)。
> **取证纪律**: 全文引用的**每一个行号均已实读源文件核对** (见 §指针核对表); 每条 finding 给出「实现者 A / 实现者 B / 对输入 X 结论相反」的可证伪形式。
> **scope_ok 判定**: 变更面严格落在自述范围 (A.1 认领前移 + 字段可得性 + audit-engine 竞品探针), 无 scope creep。REVISE 源于**欠定与条款互斥**, 非越界。
> **对重写本身的评价**: S1–S6 六条 spike 确实清掉了原版 7 处「A.2 待办」占位符, 承重逻辑有实测支撑 — 这是真进步。但**新写的 §1 与 §2.1/§2.2 条款措辞引入了新一批互斥前提**, 形状与前三轮相同 (为 A 写的规则违反 B 依赖的隐含前提), 详见交叉一致性表。

---

## 指针核对表 (逐个实读, 无一例外)

| Spec 引用 | 实读结果 | 判定 |
|---|---|---|
| `collision.py:219-220` (§2.1 注) | `if c.track_id == own_track_id:` / `continue  # same-name collision` | ✅ 行号准确 |
| `collision.py:210` (§2.4) | `_TERMINAL = ("done", "abandoned", "unknown")` | ⚠️ **行号准确, 内容断言错** → C5 |
| `phase1_gate.py:1232` (§2.4 / D5) | `out["linked_issue_overlap"] = linked_issue_overlaps(` (位于 `_main()`, `run_gate` 返回后独立追加) | ✅ 准确 |
| `_run_gate_impl` 对其 grep 命中 0 (§2.4 注) | `_run_gate_impl` 定义于 `:334`, 函数体内零命中 | ✅ 准确 |
| `claim_lifecycle.py:425` (§2.3) | `if rec.container == resolved.container_id` | ✅ 准确 |
| `GateResult.error` docstring `:210` (§2.5) | `phase1_gate.py:210` = `Possible values: "not_a_git_repo", "identity_error", "fetch_degraded",` | ✅ 准确 (但裸指针歧义 → m1) |
| 「`fetch_degraded` 从未被赋值」(§2.5) | grep `error="fetch_degraded"` = 0 命中; `:478-481` 注释自称「warn the caller via the error field」却无赋值 | ✅ 准确 |
| `audit-engine/SKILL.md:85` (§4) | `入口逻辑完成后、**Round 1 启动前一次性**执行` | ✅ 准确 |
| `execution-modes.md:84-111` (§4) | `:84` = `## Convergence 模式`, `:111` = 代码块收尾 ``` | ✅ 准确 |
| `execution-modes.md:113-144` (§4) | `:113` = `## Challenge 模式`, `:144` = 文件末行 | ✅ 准确 |
| `DEFAULTS.json:124-128` (§4) | `:124 "adaptive_rules": {` … `:127 "level_3": "challenge"` `:128 },` | ✅ 准确 |
| `spec-drafter/SKILL.md:9` (§3) | `user-invocable: true` | ✅ 准确 |
| `phase-b-developer :88-93` / `branch-manager :149` (§Why 表) | `:88` check 行 / `:91` python3 命令 / `:149` 认领句 | ✅ 准确 |
| `remote_refresh.py:691` (§4 注) | `_write_cache_atomic(cache_file, outcomes, new_scan_generation)` — 全文件唯一主流程写入点 | ✅ 准确 (实际路径为 `scripts/collectors/remote_refresh.py`) |
| `handoff_multibranch.py` 440 分支 scan cap (§4) | `:111` 注释「(e.g. 440 remote branches)」+ `:304-331` 三层可配 cap | ✅ 准确 |
| `audit-engine 现零 scripts/` (§4) | `ls` = 仅 `SKILL.md` + `references/`; `run_all_tests.sh:50` 用 `find skills -type d -name tests` **自动发现** | ✅ 准确 |
| 「141 篇 proposal 语料」(§⭐) | `ls openspec/{changes,archive}/*/proposal.md` = **141** | ✅ 准确 |

**结论**: 9/9 被点名指针的**行号全部准确** — 这是相对前三轮的明显改进。唯一失效的是 `collision.py:210` 的**内容断言** (C5), 以及 §2.3/D6 的一条无行号事实断言 (C6)。

---

## Critical (6 条)

### C1 — §2.2 的处置解决不了 §2.2 自述的问题: `heartbeat()` **零生产调用点**, 而 Spec 未指定任何调用者

- **位置**: `proposal.md:105-114` (§2.2) + `:202` (D4) + `:242` (SC-5) + `:283` (Impact) vs `lib/constants.py:43-50` / `lib/gc.py:355-359`
- **实读逐字** (`constants.py:43-45`):
  > `and in reality NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either), so every live claim's heartbeat_at is frozen at acquire time.`
  同文件 `:50`: `Revisit when a heartbeat loop ships.` — grep 复核 `heartbeat(` 生产调用点: **0**。
- **问题**: §2.2 的论证链是「事故窗 48–72h > `SWEEP_TTL` 24h ⇒ 保护窗不够 ⇒ **处置 = heartbeat 匹配键改 `(container_id, normalized track_id)`**」。但**匹配键决定的是「找不找得到 claim」, 不是「有没有人去刷新」**。`heartbeat_at` 冻结在 acquire 时刻的根因是**没有任何东西调用它**; 换匹配键后它仍然没有任何东西调用它 ⇒ 24h 后照样被 `sweep_stale_active` durable 改写为 `abandoned`, 48–72h 窗口的后 2/3 仍然裸奔。
- **Spec 自己的话构成自证**: §2.2 判否「再调 phase1_gate」的理由是「**它依赖『AI 记得再调』—— 而那正是本 Spec 存在的理由**」。但 heartbeat 同样只能由 AI 显式调用 (无 daemon / 无 cron / 无 hook), **依赖完全相同**。判否 X 的理由原样适用于被采纳的 Y。
- **两实现者分叉 (输入 X = A.1 于 T0 认领, T0+30h 对方容器起草同 issue)**:
  - **实现者 A** 照 Impact 表 (`:283` 只写「`claim_lifecycle.py` heartbeat 增 by-track 变体」) 实现库函数 + SC-5 单测 ⇒ 生产无调用者 ⇒ T0+24h claim 已被 sweep 成 `abandoned` ⇒ 对方在 T0+30h 看到的是「已放弃」⇒ **判定无人在做, 重复劳动照发生**。
  - **实现者 B** 读 §2.2「heartbeat 为主」推断必须有调用者, 于是在 `phase1_gate` 每次调用时先 heartbeat 全部同 track active claim ⇒ 行为与 A 相反。
  - 且 B 的实现会**改变 Phase B 现有路径的写入行为**, 撞 §非目标 `:272`。
- **建议修法** (三选一, 须在 Spec 里定死, 不得留给 A.2):
  1. **指定调用者与频次**: 明写「A.1 认领步骤 + 每次 `phase1_gate` 调用 + phase 转换时各刷新一次」, 并进 Impact 表与 SKILL.md; 同时说明这仍是「AI 记得调」类保证, 诚实标注其上限;
  2. **或**改走 TTL 侧: 为 A.1 claim 引入独立的更长 `SWEEP_TTL`(≥72h), 并**同步修订 `constants.py:38-51` 的 TTL 选择理由** (该注释明写 24h 是「因为没有 heartbeat loop」);
  3. **或**显式承认保护窗只有 24h, 把「24h 后失保」写进 §6 残余缺口表。
  无论哪条, **SC-5「跨 subprocess 两次调用」都必须补一条「无人调用 heartbeat 时 T0+25h 的 claim 状态」的红窗**, 否则 SC 只能证明函数能跑, 不能证明窗口被延长 (memory `feedback_completion_signals_vs_runtime_invocation`)。

---

### C2 — §5「探索性放弃必须 release」 × §2.1「track-id 不含 slug」**互相拆台**: 放弃一个方向会连坐释放同 issue 下**正在保留**的方向

- **位置**: `proposal.md:178` (§5 探索性放弃) × `:92` (§2.1 派生规则) × `:256` (SC-14); 实现 `claim_lifecycle.py:422-462`
- **实读**: `release_claim_by_track` 的匹配集是
  ```python
  matches = [rec for rec in read_result.claims
             if rec.container == resolved.container_id
             and rec.track_id == norm
             and rec.status == "active"]
  ```
  且 `:436-462` 对 **`matches` 全体**逐条改写 (docstring `:398-401` 逐字: 「**ALL matching active claims are released**」)。
- **问题**: §2.1 定死 track-id = `<basename>-<n>-<container_uuid>` — **不含 slug**。⇒ 同一容器在同一个 issue 下探索的**三个方向共用同一个 track_id**。§5 要求「判定『不起该 Spec』时**必须**调 `release_gate.py --status abandoned`」。于是放弃方向 2 时, `release_claim_by_track` 把方向 1/3 的 active claim **一并**改写为 `abandoned`。
- **二次伤害 (与 §2.4 耦合)**: 被误 abandon 的 claim 在 §2.4 的 `--include-terminal` 下**恰恰可见**, 且状态是 `abandoned` ⇒ 并发轨读到「对方已放弃」⇒ 得到**方向相反的错误结论**。这比原来的「看不见」更坏: 假绿的反面 (memory `feedback_false_green_dual_is_permanent_red`)。
- **两实现者分叉 (输入 X = 同容器同 issue 探索 3 个方向, 放弃其中 2 个)**:
  - **实现者 A** 照 §5 字面, 每放弃一个方向调一次 release ⇒ 三条 claim 全部 `abandoned`, 保留的方向**失去认领**;
  - **实现者 B** 注意到 id 共享, 只在「整个 issue 都不做了」时才 release ⇒ claim 保留。
  - 两者对 X 的终态相反, 且 **SC-14 (`:256`)「claim 状态为 `abandoned`」在 A 和 B 上都能绿** (B 的场景不触发), SC 无法分辨。
- **建议修法**: §5 第一行的义务须按分支限定 —— 「**仅当放弃的是该 track_id 下的最后一个方向**才 release」, 或改为「release 前先断言同 (container, track_id) 无其他在建方向」。并补 SC:「同 (container, track_id) 有 2 条 active claim 时放弃其一 ⇒ 另一条**仍为 active**」(在照字面实现上必红)。

---

### C3 — §1 的字段格式与机械校验对**真实语料 0/12 匹配**, 且未给提取规则 ⇒ 校验恒黄 + `--linked-issue` 收到 markdown 链接 ⇒ 主机制重蹈前置 Spec 要治的病

- **位置**: `proposal.md:70-72` (§1.1–1.3) + `:255` (SC-13) + `:83` (§2 模板) vs 仓内 12 个真实字段实例
- **实测全量语料** (`grep "^> \*\*关联 Issue\*\*:" openspec/{changes,archive}/*/proposal.md`, 共 **12** 条):
  | 形态 | 实例 |
  |---|---|
  | markdown 链接 + 尾随括注 | `[10CG/aria-plugin #122](https://forgejo.10cg.pub/…/issues/122) (open, 0 评论, …)` |
  | **无仓名** | `Forgejo [#134](…/Aria/issues/134) (triage verdict = partial-repro)` |
  | 仓名在链接**外** | `aria-plugin [#95](…/aria-plugin/issues/95) (closed, …)` |
  | **多 issue 并列** | `[#154](…) + [#157](…) + [#152](…) ; [#156] = #154 重复, close` |
  | `无` + 括注 | `无 (由 a1-entry-claim-duplicate-work-guard 的 post_spec R1 发现, …)` |
  **符合 §1.2 所定 `<org>/<repo>#<n>` 单一形态的: 0 / 12。**
- **问题 (三重)**:
  1. **`无` 不是字面 `无`**: 仓内唯一 `无` 实例带括注。SC-13 写「显式 `无` 则通过」— 严格相等实现会 warn 它; 前缀/正则实现会放行。Spec 未说是哪一种, **也未说英文 `none`/`N/A` 算不算**;
  2. **校验对象未定义提取规则**: §1.3 只写「值可被前置 Spec 的归一解析」。前置 Spec 的算法是「按**最后一个** `#` 拆」—— 对 `[…#122](…/issues/122#issuecomment-16979)` 这类 (语料中 **5/12** 带 `#issuecomment-`), 最后一个 `#` 落在 URL 锚点里 ⇒ **不可解析** ⇒ warning。§1.4 说存量不回填, 但 §1.3 没有把 check 限定在新建/`changes/` ⇒ **对 129 篇存量恒黄**, 正是本项目判据里「恒红 = 零信息」的形状;
  3. **多 issue 形态无处置**: `--linked-issue` 是单值, claim 的 `linked_issue` 也是单字段。语料里已有 1/12 是多 issue。Spec 全文未提。
- **两实现者分叉 (输入 X = `> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open, …)`)**:
  - **实现者 A** 先剥 markdown 链接取链接文字 `10CG/aria-plugin #122` 再喂归一 ⇒ **PASS**, 且 `--linked-issue` 传 `10CG/aria-plugin #122`;
  - **实现者 B** 把冒号后整行原串喂归一 ⇒ 最后一个 `#` 之后是 `122](https://…) (open, …)` ⇒ **不可解析 ⇒ warning**, 且 `--linked-issue` 传整行原串 ⇒ 前置 Spec 的第 4 步「不可解析 ⇒ 退回原串精确比较」⇒ 两轨括注差一个字就**恒不匹配**。
  - 对同一输入, A 判 PASS + 机制可用, B 判 WARN + 机制静默失效。**这正是前置 Spec 存在的理由在上一层原样复现** (memory `feedback_fix_recurs_in_its_own_fallback_path`)。
- **建议修法**: §1 必须把**提取**与**校验**分开钉死:
  (a) 明写提取规则 — 「取字段值中第一个 markdown 链接的**链接文字**; 无链接则取首个空白/`(` 之前的 token」, 给 ≥5 组正例 (覆盖上表五种真实形态) + 3 组反例;
  (b) 明写 `无` 的判据 (是否允许尾随括注 / 是否接受 `none`);
  (c) 明写多 issue 的处置 (取首个 / 全部各写一条 claim / 判不合规);
  (d) SC-13 的 check 须显式限定生效范围 (仅 `openspec/changes/`, 或仅 mtime 晚于 ship 日的文件), 否则 §1.4「不追溯」与 §1.3「机械校验」直接互斥;
  (e) 补一条 SC: 「以**语料实测的 5 种真实形态**为 fixture, 校验与 `--linked-issue` 取值均须命中同一归一键」(在任何未定义提取规则的实现上必红)。

---

### C4 — §3 的两个落点在 `allowed-tools` 上**结构性不可执行**, Impact 表零覆盖

- **位置**: `proposal.md:146-148` (§3 双落点) + `:79-86` (§2 Bash 模板) + `:118` (§2.3 `AskUserQuestion`) + `:287-288` (Impact) vs 两个 SKILL.md frontmatter
- **实读**:
  - `phase-a-planner/SKILL.md:9`: `allowed-tools: Read, Write, Glob, Grep, Task, Skill` — **无 `Bash`, 无 `AskUserQuestion`**;
  - `spec-drafter/SKILL.md:10`: `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` — **无 `Bash`**;
  - 对照工作中的先例: `phase-b-developer/SKILL.md:10` = `Bash, Read, Write, Glob, Grep, Task, Skill`; `branch-manager/SKILL.md:10` = `Bash, Read, Grep` — **两个现有 Phase B 落点都有 `Bash`**;
  - 可委派对象 `state-scanner/SKILL.md:11` = `Read, Glob, Grep, Bash` — **有 Bash 但无 `AskUserQuestion`**。
- **问题**: §2 的主机制是一条 `python3 … phase1_gate.py …` Bash 命令, §2.3 的消费面强制 `AskUserQuestion`。**两个落点没有一个能同时做这两件事**: phase-a-planner 两样都缺, spec-drafter 缺 Bash。而 Impact 表 (`:287-288`) 对这两行只写「A.1 独立标题级认领步骤 + overlap 消费 + release 义务 + `coordination.enabled` skip」和「第二落点 + proposal 模板增字段」—— **零字提及 frontmatter `allowed-tools` 变更**。
- **两实现者分叉 (输入 X = 用户 `/spec-drafter my-feature`)**:
  - **实现者 A** 严格照 Impact 表实现 ⇒ SKILL.md 正文写了认领步骤, 但运行时 Bash 被 frontmatter 拒绝 ⇒ **步骤静默失效**, 这正是本 Spec §Why 反复痛陈的「已 ship ≠ 能用」;
  - **实现者 B** 自行补 `allowed-tools: …, Bash` ⇒ 能跑, 但这是**未被 Spec 授权的 frontmatter 变更**, 且 `allowed-tools` 属 Skill 契约面, 会牵动 Rule #6 的判定 (rule6_note `:211` 只把改动定性为「SKILL.md 正文的处方性指令面」, 未覆盖 frontmatter)。
- **建议修法**: Impact 表两行显式补「frontmatter `allowed-tools` 追加 `Bash` (两处) / `AskUserQuestion` (phase-a-planner)」; 并在 rule6_note 中说明 frontmatter 变更是否触发 AB (`description` 未变, 但工具面变了)。另补一条**结构化断言型 SC**: 「两个落点的 `allowed-tools` 必须同时包含 `Bash` 与 `AskUserQuestion`」(在当前 frontmatter 上必红, 且能防未来回退)。

---

### C5 — §2.4 对 `_TERMINAL` 的内容断言**是错的**: `yielded` 不在其中、`unknown` 在其中 ⇒ SC-8 的 `yielded` 臂恒绿, `unknown` 分支两读

- **位置**: `proposal.md:127` (§2.4) + `:245` (SC-8) vs `lib/collision.py:210` / `lib/claim_schema.py:56-59` / `lib/claim_lifecycle.py:408`
- **实读逐字**:
  - `collision.py:210`: `_TERMINAL = ("done", "abandoned", "unknown")` — **不含 `yielded`**;
  - `claim_lifecycle.py:317` 与 `:408`: `_TERMINAL_STATUSES = frozenset({"done", "yielded", "abandoned"})` — **不含 `unknown`**;
  - `claim_schema.py:56`: `STATUS_ENUM = {"active","yielded","done","abandoned","unknown"}`; `:51-52` 逐字:「`unknown` is a reader-side sentinel — it is NEVER written by a live session」; `:28-31` 逐字: reconcile **刻意** SKIP 掉 `unknown`, 理由是「unknown-version claim semantics may be incompatible」。
- **问题**: Spec 写「`done` / `abandoned` / `yielded` 的同 issue claim 必须可见 …… `collision.py:210` 的 `_TERMINAL` 会直接 skip **它们**」。事实是:
  - `yielded` **今天就已经可见** — 它不在 `collision.py` 的 `_TERMINAL` 里。⇒ SC-8 若用 `yielded` 单臂 fixture, **在现状代码上就是绿的**, 违反 SC-8 自己写的「`_TERMINAL` skip 的现状**必红**」。这条 SC 答不出「它怎么会红?」(memory `feedback_test_asserts_what_its_name_claims`);
  - `unknown` **被 skip 但 Spec 从未提及**。它是 schema 版本不认识时的 reader-side sentinel, 语义上**不是**终态。
- **两实现者分叉 (输入 X = 同 issue 他轨 claim 的 `status == "unknown"`)**:
  - **实现者 A** 把 `include_terminal=True` 实现为「`_TERMINAL` 判定整体跳过」⇒ `unknown` claim 出现在 overlap 里, 并被 §2.3 渲染成一条要 owner 裁决的告警 —— 而 reconcile 全系统对该状态的既定契约是「不可信, 跳过」;
  - **实现者 B** 按 Spec 逐字列举实现 `_TERMINAL = () if include_terminal else ("unknown",)` ⇒ `unknown` 仍被 skip。
  - 对 X, A 报告碰撞、B 不报告。**结论相反**, 且两者都能通过 SC-8 现有措辞。
- **建议修法**:
  1. 勘正 §2.4 的事实陈述 (「`_TERMINAL` 当前含 `done`/`abandoned`/**`unknown`**, **不含 `yielded`**」);
  2. **明确 `unknown` 的处置**并写理由 (建议: `include_terminal` **不**解禁 `unknown`, 与 `claim_schema.py:28-31` 的既定契约对齐);
  3. SC-8 按 status 逐臂拆开, 并对 `yielded` 臂改写「怎么会红」—— 现状已绿, 该臂应改为**回归断言** (防实现把 `yielded` 误加进 `_TERMINAL`), 不能计入「baseline-failing」;
  4. §2.3 的「措辞按 status 分档」须给出**分档表** (done / abandoned / yielded 各说什么), 否则「分档」不可验收。

---

### C6 — §2.3/D6 的承重事实断言「**无任何函数支持释放别的容器的 claim**」为假: `release_gate.py --sweep-stale` 的 help 逐字写着「跨 container」

- **位置**: `proposal.md:122` (§2.3 spike 引注) + `:204` (D6) + `:270` (§非目标) vs `scripts/release_gate.py:222-226` / `lib/gc.py:338-363`
- **实读逐字**:
  - `release_gate.py:225` help: `顺带扫描: active 且 heartbeat 超 STALE_TTL → abandoned (跨 container)`;
  - `gc.py:361-363` docstring: `Cross-container by design: sweep is a GC action, not a session action, so it MAY rewrite other containers' claim files. This intentionally relaxes the file-per-writer invariant`。
- **问题**: 存在一条**已 ship、已有 CLI 开关**的跨容器改写路径 (TTL 闸门下)。Spec 的断言应为「无**按需**释放指定他容器 claim 的函数; 只有 TTL 闸门下的 GC 式跨容器改写」—— 这与「无任何函数」是**实质不同**的事实, 而它正是 D6 与 §2.3 选项措辞的唯一依据。
- **与 C1 的复合放大**: 因为 `heartbeat_at` 冻结在 acquire (C1 实证), **任何超过 30 分钟的 A.1 claim 都满足 `--sweep-stale` 的 STALE_TTL 判据** ⇒ 该路径在实践中对**几乎所有**并发轨都可达, 不是理论边角。
- **两实现者分叉 (输入 X = owner 选了「我去释放对方的 claim 后再开始」, 对方 claim 已 45 分钟未刷新)**:
  - **实现者 A** 照 D6 字面实现「两步人工」提示语, 告诉 owner「须去对方容器执行 release」;
  - **实现者 B** 发现 `--sweep-stale` 后把该选项实现为**一键** `python3 release_gate.py --sweep-stale` ⇒ 本容器直接把对方**仍在工作**的 claim 改写成 `abandoned` (durable, `gc.py:356` 逐字「unrecoverable for the victim」)。
  - 对 X, A 不写他人数据、B 写且不可恢复。**这是数据破坏级的分叉**, 且 §非目标「不引入跨容器 release」在 B 看来并未被违反 (它没有「引入」, 它复用了既有的)。
- **建议修法**: 勘正 §2.3/D6 的断言, 并**显式禁止**在本 Spec 的消费面调用 `--sweep-stale` / `gc.sweep_stale_active` (写进 §非目标, 而非仅「不引入新函数」); AskUserQuestion 的选项文案须点名「本流程**不会**代你改写对方的 claim」。补 SC: 「overlap 消费路径不得调用任何跨容器写入 API」(结构化断言, grep 级可验)。

---

## Major (9 条)

### M1 — SC-1 与 §5/SC-15 互相拆台: 「改名不改 id」只对 **9%** 的场景成立, SC-1 却无分支限定
- **位置**: `:234` (SC-1) × `:179` (§5 slug 改名行) × `:257` (SC-15) × `:92` (§2.1 回落分支) × `:58` (S4: 9%)
- SC-1 写「slug 改名前后 track-id **不变**」, 无任何分支限定。但 §2.1 的**回落分支** `<spec-slug>-<container_uuid>` 含 slug, §5 明写该分支「须走 release 旧 + acquire 新两步」—— 即 **id 必变**。而按 §⭐ 自己的实测, **91% 的 proposal 没有关联 issue**, 全部落在回落分支。⇒ **SC-1 在绝大多数真实场景下为假**, 且与 SC-15 断言相反的事。
- **分叉**: A 写无条件不变式测试 ⇒ 回落分支必红, A 可能反向「修」掉回落分支的 slug (无可用替代); B 把 SC-1 限定在 linked-issue 分支 ⇒ 绿。两者对「改名 + 无 issue」结论相反。
- **修法**: SC-1 加分支限定「**有关联 issue 时**改名前后 track-id 不变」; 并在 §2.1 表下补一行明写「回落分支不具备改名不变性 —— 这是已知限, 由 §5 的两步 release/acquire 兜底, 覆盖 91% 的语料」。这条已知限目前**只在 §5 表格里一笔带过, §2.1 与 SC-1 都读不到**。

### M2 — §2.1 的三段拼接**没有代码落点**: SC-1/SC-4 被挂在 `state-scanner/tests/` 宿主上, 但 Impact 表里没有可测的生产对象 (R1/C4 在自己的修复里复发)
- **位置**: `:222-227` (验证面分层表) + `:286` (Impact: `tests/` 承载 SC-1~10,14,15) vs `:283-285` (Impact 的三行生产文件)
- Impact 表列的生产变更只有: `claim_lifecycle.py` (heartbeat 变体) / `identity.py` (**直取 uuid 的 accessor**) / `phase1_gate.py` (CLI flag + error 契约)。**没有任何一行提供「把 basename / `str(int(n))` / uuid 拼成 raw-track-id」的函数**。而 §2 的模板 (`:81`) 是让 **AI 在 Bash 命令里手写**这个串。
- ⇒ SC-3 (label 长字符串 ⇒ 仍用 uuid) 可测新 accessor ✅; 但 **SC-1 (改名不变) 与 SC-4 (`#007` ≡ `#7`) 没有被测对象** —— 它们断言的是「AI 拼串时的行为」, 属行为类, 却被表格归入「代码类 / 可机械断言 ✅」。
- 这与 §Success Criteria 开头自述要修的 R1/C4 (「原版把 SC 挂在**不存在的** `phase-a-planner` 测试宿主上」) **是同一形状的缺陷**。
- **分叉**: A 新增 `compose_entry_track_id()` 到 `track_id.py` 并测之 (但该文件不在 Impact 表, 且 §非目标未授权); B 只写进 SKILL.md prose, SC-1/SC-4 无处落 ⇒ 交付时被降级为「行为类」而 rule6_note 的三条 fixture (`:212`) **不含 track-id 拼接**, 于是无任何验收。
- **修法**: Impact 表补 `lib/track_id.py`(或 `identity.py`) 新增 compose 函数一行, 并把 §2 模板改成「调用该函数产出 raw-track-id」而非让 AI 手写; 或明确 SC-1/SC-4 归行为类并补第 4 条定向 fixture。

### M3 — §2.2 说「**改**匹配键」, Impact 表说「**增**并存变体」—— 两读, 对既有调用方影响相反
- **位置**: `:109` (「heartbeat 匹配键**改** `(container_id, normalized track_id)`」) + `:202` (D4 同为「改」) vs `:283` (Impact: 「heartbeat **增** by-track 变体 (仿 `release_claim_by_track` **并存**模式)」)
- `release_claim_by_track` 是与 `release_claim` **并存**的第二个函数 (`claim_lifecycle.py:274` 与 `:377`), 「仿其并存模式」= 新增 `heartbeat_by_track`, 旧 `heartbeat` 语义不动。而 §2.2/D4 的「改」= 原地修改 `heartbeat()` 的匹配键。
- **分叉**: A 原地改 ⇒ 既有 `heartbeat()` 的 `(container, session)` 语义消失, 现有测试与 docstring (`:196-205`) 全部失效, 且这是**共享 lib 的行为变更** (撞 §非目标 `:272`); B 新增变体 ⇒ 旧函数保留, 但 SC-5 的「按 `(container, session)` 匹配的**现状**必红」在 B 上退化为「新函数不存在所以红」, 失去它想钉住的红窗。
- **修法**: 二选一写死 (推荐 B「增变体」, 与 Impact 表和既有并存先例一致), 并把 §2.2/D4 的「改」改为「增」; SC-5 相应改写为对新函数的正向断言 + 对旧函数的回归断言。

### M4 — §2.4 让终态可见后, §2.3 的**选项集与抑制规则未随动** ⇒ 对任何被复用过的 issue **恒提示**
- **位置**: `:118-123` (§2.3) × `:127` (§2.4 「`done` 恰恰是最该看见的信号」)
- §2.3 的三选项「另起 / 我去释放对方的 claim 后再开始 / 并轨」全部预设**对手是 active 的**。当命中的只有 `done` claim 时:「释放对方的 claim」无意义 (已终态)、「并轨」无对象。Spec 未定义终态命中时的选项集, 也未定义**是否仍要打断起草去请裁**。
- **恒提示风险**: `done` claim 只有 `--gc` 超 retention 才归档 (`release_gate.py:229` help)。⇒ 任何针对**曾被处理过的 issue** 的新 Spec (在本仓极常见: `#95`/`#122` 各出现 2 次, 见语料) 都会在 A.1 被强制弹一次 owner 裁决。高频无信息告警 = 学会忽略 = 与本 Spec 目标背反。
- **分叉**: A 对终态命中照弹三选项 ⇒ owner 每次都要回答一个已完成的碰撞; B 对「仅终态命中」降级为渲染一行不请裁 ⇒ 不弹。对输入 X = 同 issue 只有一条 `done` claim, 两者行为相反。
- **修法**: §2.3 补一张 status × 处置矩阵 (active ⇒ 请裁三选项 / `done` ⇒ 渲染 + 「对方已完成, 建议先读其产物」两选项 / `abandoned`·`yielded` ⇒ 仅渲染不请裁), 并补 SC「仅终态命中时**不触发** `AskUserQuestion`」。

### M5 — §2.3 的强制请裁与 AD10「人类参与点仅 1 个」冲突, Layer 2 无人值守下**未定义**; 且与 §非目标「不把 advisory 升级为 block」自相矛盾
- **位置**: `:118`/`:123` (§2.3) + `:271` (§非目标) vs `CLAUDE.md` §Aria 2.0「人类参与点仅 1 个 (AD10): S7_AWAITING_MERGE」
- §2.3 自己承认「不硬阻断 (撞 §非目标与 AD10)」, 随即规定「**也不是 AI 渲染一行后自行决定**……属 owner 权限面 (Rule #10)」。对 AI 而言, **必须等 owner 回答才能继续起草** 在行为上等价于 block —— 只是阻断者从机制换成了流程。
- **v2.0 未定义**: Layer 2 是无人值守容器, `AskUserQuestion` 无人应答。Spec 全文未说该场景下 A.1 如何收敛 (超时继续? 挂起? 写 issue 请裁?)。而 A.1 正是 Layer 2 十步循环的必经点。
- **分叉**: A 在无人值守下超时后按「另起」默认继续 ⇒ 实质是 AI 自行放行 (违反 §2.3 的原文); B 挂起等待 ⇒ 168h 自主跑在此处死锁。
- **修法**: §2.3 补一段「Layer 1/2 场景处置」(建议: 无人值守时把裁决升格为 Layer 1 主管的 Feishu 审批项, 或降级为「记录 + 继续 + 在 handoff 请复议」并说明这不构成 Rule #10 自我豁免); 并明确该请裁点是否新增了 AD10 之外的人类参与点 (若是, 须 owner 裁并同步 architecture-decisions)。

### M6 — §4 探针**无 stdout 契约**, exit code 三分调用方不可判; 且 SC-18 让「无远端」判非 0 ⇒ 无远端项目恒非 0
- **位置**: `:171` (exit code 三分) + `:209` (D11) + `:259` (SC-17) + `:260` (SC-18) + `:171` (消费面「渲染 🔴 一行 + 写入聚合报告」)
- 「**0 = 无命中 / 0 = 有命中** / 非 0 仅用于探针自身失败」意味着调用方**只能靠 stdout 区分命中与否**, 而 Spec 全文**没有定义任何输出格式** (JSON? 键名? 文本行?)。可 §4 的消费面又要求机读 (渲染 + 写入聚合报告)。
- SC-18 把「探针 fetch 失败 / **无远端**」并列判为 exit 非 0。「无远端」不是失败, 是合法环境 (本地单仓项目 / 未配 `enforced_remotes`)。⇒ 这类项目**每轮审计恒非 0**, 而 §4 又说「不阻断」⇒ 一个恒为非 0 且必须被忽略的信号 = 零信息 (memory `feedback_false_green_dual_is_permanent_red`)。
- **分叉**: A 输出 `{"hits":[…],"degraded":false}` JSON 并对无远端返回 0+`skipped`; B 输出 markdown 行并对无远端返回 2。audit-engine 侧的消费代码互不兼容; 对输入 X = 无远端仓库, A 静默通过、B 每轮报错。
- **修法**: (a) 定义 stdout JSON schema (字段名 + 类型 + 命中项结构), 并把 SC-16/SC-17 的断言改写在该 schema 上; (b) 把 exit code 三分改为**四分**并区分 `degraded`(可继续) 与 `error`(探针 bug), 明确「无远端 = `skipped`, exit 0」; (c) SC-18 拆成「fetch 失败」与「无远端」两条, 期望值不同。

### M7 — §4「只扫默认分支」使 **in-flight 竞品结构性不可见**, 与其自述盲区和 §6 的覆盖归功都不符
- **位置**: `:170` (「只扫 `enforced_remotes` × **各自默认分支** (非全部 ref)」) × `:172` (盲区声明「只看得见**已 push** 的竞品」) × `:189` (§6: legacy 轨「**§4 探针部分覆盖**」)
- 本 Spec 要防的头号场景是「双方都在 Phase A, 谁都还没合并」。此时竞品 proposal 位于**功能分支** (或未 push)。只扫默认分支 ⇒ **该场景 100% 不可见**。探针实际只覆盖 §4 自述的 (b)「已 ship 并归档」。
- 盲区声明写「只看得见已 push 的」**低估了自己的盲区** —— 正确表述是「只看得见已 push **且已合入默认分支** 的」。而 §6 据此把 legacy 轨 (7/9 身份) 记作「部分覆盖」, 这个「部分」有多小没有量化。
- **分叉**: A 照字面只扫默认分支; B 读「盲区 = 只看已 push」推断应扫全部远端分支 (并撞上 §4 自己引用的 440 分支 scan cap 教训)。对输入 X = 竞品在 `origin/feature/xxx` 上, A 漏、B 命中。
- **修法**: 勘正盲区声明措辞; 在 §6 表里把「in-flight 未合并的竞品」列为**独立的残余缺口**并标注覆盖它的机制 (只有主机制的 claim, 而主机制受 C3 的 9% 输入约束); 若决定扫功能分支, 须给 cap 与代价重估 (S2 的 ~13.8s 是默认分支的数字)。

### M8 — `state_scanner.coordination.enabled` **未在 `DEFAULTS.json` 注册**, Impact 表未列该文件 ⇒ 缺键语义两读, SC-9 的极性不确定
- **位置**: `:139` (§2.5) + `:246` (SC-9) + `:292` (Impact 只列 `config-loader/SKILL.md`) vs `config-loader/DEFAULTS.json` / `config-loader/SKILL.md:134-137`
- **实读**: `DEFAULTS.json` 的 `state_scanner` 块含 `confidence_threshold` / `sync_check` / `issue_scan` / `multi_remote` / `sync_freshness` —— **无 `coordination`**。该键只在 `config-loader/SKILL.md:134-137` 有文档 (`default: true`), 且同处注明「**已知边界: `runtime_probe._resolve_enabled_when` 的缺键=off** 是通用探针契约不随动」。
- ⇒ 同一个键在本仓已经有**两个相反的缺键默认** (文档 true / 探针 off)。Spec 要在 A.1 新增一个消费点却未指明用哪一个。
- **分叉 (输入 X = 第三方项目, `.aria/config.json` 无该键)**: A 按 config-loader SKILL 的 `default: true` ⇒ A.1 **写 claim 并推 ref 到对方 origin** (§2.5 自己点名这是「对未配 coordination ref 的第三方是外向副作用」); B 按探针契约缺键=off ⇒ 零调用。两者行为完全相反, 且 A 的行为正是 §2.5 想避免的。
- **修法**: Impact 表补 `config-loader/DEFAULTS.json` (把键显式注册); §2.5 明写缺键语义并说明为何与探针契约不同; SC-9 拆成「显式 false ⇒ 零调用」与「**缺键** ⇒ ?」两条。

### M9 — §1 的「机械回声」只落主仓 `.aria/state-checks.yaml`, 而模板落 plugin (跨项目分发) ⇒ 采用方只拿到「AI 可以删的模板」, 正是 §1 自述要避免的退化
- **位置**: `:70-72`/`:75` (§1 + 「为什么校验而非仅模板」) + `:293` (Impact 只列主仓 `.aria/state-checks.yaml`) vs `.aria/state-checks.yaml` 的作用域 (项目级, state-scanner Phase 1.11 串行执行)
- §1 的论证是「模板只影响新建, 且 AI 可以删 ⇒ **无机械回声的义务会退化**」。但交付面把模板放进跨项目分发的 `spec-drafter/SKILL.md`, 把回声放进**只对 Aria 本仓生效**的 `.aria/state-checks.yaml`。⇒ 所有 aria-plugin 采用方 (Kairos 等) 拿到的**恰好是 §1 判定会退化的那一半**。
- **分叉**: A 只改主仓 state-checks (照 Impact 表); B 额外在 plugin 侧提供可复制的 check 片段 / 默认 check。对输入 X = Kairos 项目起草无字段的 proposal, A 无任何回声、B 有。
- **修法**: 二选一并写进 Spec —— (a) 明确该 check 是 **Aria 本仓 dogfood**, 跨项目回声记为 follow-up 并写进 §6 残余缺口; (b) 把 check 做成 plugin 可分发资产。当前措辞让读者以为已覆盖。

---

## Minor (5 条)

### m1 — §2.5 的裸 `(:210)` 指针歧义
`:140` 写「`GateResult.error` 的 docstring (`:210`)」。真实目标是 `phase1_gate.py:210` ✅, 但**紧邻上文 §2.4 (`:127`) 刚把 `:210` 锚定到 `collision.py`**, 且 `identity.py:210` 也存在 (`get_container_id` 参数段)。⇒ 建议补全文件名。

### m2 — §2.1 未说明合成串仍会过 `derive_track_id`, 且 >64 字符是**整串 sha256 替换**而非截断
`track_id.py:68-77` 逐字: 步骤 4「if the *original* `raw_id` was longer than 64 characters OR contained any non-ASCII character, **discard the step-1..3 result** and return `sha256-` + hexdigest[:16]」。§2.1 的表只写「与 `derive_track_id` 两层对齐」, 未说明: (a) 合成后的 raw 串会被再归一一次; (b) 超长时**三段结构整体消失**, 换成 16 位 hash。这会让 SC-3 (「track-id 仍用 uuid 字段」) 在超长输入上无法在**派生结果**层观测。建议在 §2.1 补一行长度预算 (basename ≤ N ⇒ 总长 ≤ 64) 与超限行为。

### m3 — §4 的插入点在两套不同编号体系下未定名
Convergence 段 (`execution-modes.md:88-103`) 用 `1./2./3./4.`, Challenge 段 (`:117-137`) 用 `Step 1..Step 5`。§4 只说「接在每轮循环入口」并明确「不叫 Step 0.5」, 但没说在两个块里各叫什么、插在编号前还是重排编号。两实现者会得到不同的文档结构 (影响后续 diff 与 drift-check anchor)。

### m4 — 本 proposal 自身没有「关联 Issue」字段 (dogfood 缺口)
`proposal.md:3-8` 的头部有 Status / Created / Spec Level / 代码落点 / ship target / 前置依赖 —— **无「关联 Issue」**。而 §Why 全篇围绕 `#122` 展开。§1 一旦落地, 这份 Spec 自己会被新 check 判 warning。建议起草时即补上 (并作为 §1 提取规则的第一个正例)。

### m5 — §2.5 的 `error` 是单槽位, 与既有 token 的优先级未定
`GateResult.error` 是 `Optional[str]` 单值, 现有取值含 `push_failed` / `max_retries_exhausted` / `auth_failed` 等 (`phase1_gate.py:210-212`)。当「fetch 降级」与「push 失败」**同时发生** (S2 实测本会话 github 就有 2 次瞬时 SSH 失败, 两者高度相关), 谁覆盖谁未定。⇒ SC-10「`error` 非空」在「fetch 降级 + push 失败」输入上, A 报 `push_failed`(SC-10 判绿但丢了降级信息)、B 报 `fetch_degraded`(丢了 push 信息)。建议改为 `errors: list[str]` 或明写优先级。

---

## ⭐ 条款交叉一致性检查表

> 逐对检查「A 条款为真时, B 条款依赖的隐含前提是否仍成立」。✅ = 一致 · ⚠️ = 有隐含前提未成文 · ❌ = 互相拆台

| # | 条款 A | 条款 B | A 对 B 的隐含前提 | 判定 | finding |
|---|---|---|---|---|---|
| 1 | §2.1 track-id 不含 slug | §5 探索性放弃必 release | 「一次 release 只影响一个方向」 | ❌ **假** — 同 issue 三方向共 id, `release_claim_by_track` 释放全部 | **C2** |
| 2 | §2.1 track-id 不含 slug | SC-1 改名 id 不变 | 「所有分支都不含 slug」 | ❌ **假** — 回落分支含 slug, 覆盖 91% 语料 | **M1** |
| 3 | §2.1 回落分支含 slug | §5 该分支走 release+acquire | 一致 (§5 已点名) | ✅ | — |
| 4 | §2.1 `str(int(n))` 归一 | SC-4 `#007` ≡ `#7` | 「存在一个可测的拼接函数」 | ❌ **假** — Impact 表无 compose 落点 | **M2** |
| 5 | §2.1 basename 来自前置 Spec 归一 | 前置 Spec §接口面「签名与 schema 不变, 只改内部谓词」 | 「归一是可复用的导出函数」 | ⚠️ **未成文** — 前置只改内部谓词; 本 Spec Impact 无 `collision.py` ⇒ 导出 or 重实现两读 | **M2 附论** |
| 6 | §1 字段格式 `<org>/<repo>#<n>` | §2.1 basename 来源 | 「字段值可直接切出 basename」 | ❌ **假** — 语料 0/12 为该形态, 4/12 无仓名 | **C3** |
| 7 | §1.3 校验「可被归一解析」 | §1.4 存量不回填 | 「check 有生效范围限定」 | ❌ **缺失** — check 未限定范围 ⇒ 129 篇恒黄 | **C3** |
| 8 | §1.1 显式写 `无` | SC-13 「显式 `无` 则通过」 | 「`无` 是字面精确值」 | ⚠️ 语料唯一实例为 `无 (…)`; 英文变体未定义 | **C3** |
| 9 | §2.4 `include_terminal` 解禁终态 | `collision.py:210` 的实际集合 | 「`_TERMINAL` = done/abandoned/yielded」 | ❌ **假** — 实为 done/abandoned/**unknown** | **C5** |
| 10 | §2.4 终态可见 | §2.3 三选项 + 请裁义务 | 「命中对手是 active」 | ❌ **未随动** — 终态命中无对应选项/抑制规则 ⇒ 恒提示 | **M4** |
| 11 | §2.4 终态可见 | §5 放弃即 `abandoned` | 「abandoned 只表示真放弃」 | ❌ 与 C2 复合 — 误连坐的 abandoned 会被对方读成「已放弃」 | **C2** |
| 12 | §2.2 heartbeat 换匹配键 | §2.2 自述「保护窗 48–72h」 | 「有东西会周期性调用 heartbeat」 | ❌ **假** — 零生产调用点 (`constants.py:43-44`) | **C1** |
| 13 | §2.2 「改」匹配键 | Impact「增并存变体」 | 二者互斥 | ❌ **直接矛盾** | **M3** |
| 14 | §2.2 heartbeat 刷新 | SC-7 超 `SWEEP_TTL` 仍被 sweep | 一致 (SC-7 是正确的反向守卫) | ✅ | — |
| 15 | §2.3 「无跨容器 release 函数」 | D6 / §非目标「不引入跨容器 release」 | 「事实断言为真」 | ❌ **假** — `release_gate.py --sweep-stale` 逐字「跨 container」 | **C6** |
| 16 | §2.3 强制 `AskUserQuestion` | §3 落点 `phase-a-planner` | 「该 skill 有 AskUserQuestion 权限」 | ❌ **假** — allowed-tools 无此工具 | **C4** |
| 17 | §2 Bash 调用模板 | §3 双落点 | 「两落点有 Bash 权限」 | ❌ **假** — 两者皆无 Bash | **C4** |
| 18 | §2.3 强制请裁 | §非目标「不升级为 block」+ AD10 | 「请裁不构成阻断/新人类参与点」 | ⚠️ 行为上等价于阻断; Layer 2 未定义 | **M5** |
| 19 | §2.5 `error` 携带 `fetch_degraded` | §非目标「不动 Phase B 入口现有认领」 | 「error 契约变更不影响 Phase B」 | ⚠️ Phase B 走同一 `run_gate`/CLI, 降级时 JSON 输出改变 | **m5 附论** |
| 20 | §2.5 降级不得渲染成「无碰撞」 | `phase1_gate.py:1235-1237` overlap 自身 fail-soft | 「overlap 的失败也会体现在 error」 | ❌ **假** — 该 except 把 `linked_issue_overlap` 置 `[]` 只 log, 不写 `error` ⇒ SC-10 可绿而「零证据当正证据」仍在 | **新增, 见下** |
| 21 | §2.5 `coordination.enabled` 控制 | `DEFAULTS.json` 键注册 | 「该键已在 SOT 注册且缺键=true」 | ❌ 键未注册; 本仓已有两个相反的缺键默认 | **M8** |
| 22 | §4 只扫默认分支 | §4 盲区声明「只看已 push」 | 「push 即可见」 | ❌ **假** — 未合入默认分支即不可见 | **M7** |
| 23 | §4 exit 0 = 命中亦 0 | §4 消费面「渲染 🔴 + 写聚合报告」 | 「有可机读的 stdout 契约」 | ❌ **缺失** — 全文无输出 schema | **M6** |
| 24 | §4 探针按 issue 匹配 | §⭐ 9% 字段可得性 | 「竞品也有 issue 字段」 | ⚠️ 探针与主机制**共享同一个 9% 输入瓶颈**, §6 未记 | **M7 附论 / 见下** |
| 25 | §1 模板落 plugin | §1.3 check 落主仓 | 「回声覆盖面 = 模板覆盖面」 | ❌ 不对称 — 采用方只得模板 | **M9** |
| 26 | §6 残余缺口表 4 行 | §⭐ 91% 无字段 | 「缺口表已穷举」 | ❌ **漏项** — 「字段缺失/为 `无` ⇒ 主机制与探针双双无输出」未入表 | **见下** |

**表内新暴露、未在上文单独立条的两点 (并入 M6/M7 处置)**:
- **#20**: `phase1_gate.py:1235-1237` 的 `except Exception: out["linked_issue_overlap"] = []` 是「零证据渲染成正证据」的**真实落点**, 而 §2.5 只治了 `GateResult.error`。⇒ 实现者做完 SC-10 会以为治好了。建议 §2.5 补一句「overlap 计算自身失败时须写入独立标记 (如 `linked_issue_overlap_error`), **不得**以 `[]` 表达」, 并补 SC。
- **#26**: §6 的缺口表列了 4 行, 但**最大的那个缺口 —— 「91% 的 proposal 没有 issue 字段, 主机制与 §4 探针同时无输入」—— 不在表内**。这与 §⭐ 自己把该事实提为「真正的瓶颈」直接冲突。建议 §6 补一行: 缺口=「无关联 issue (或写 `无`)」/ 窗口=「无界」/ 覆盖机制=「无 — §1 的 check 是 warning 且 `无` 是合法值」。

---

## 收敛性提示 (供主控 / owner 参考, 非本席裁决)

- 本轮 6C/9M/5m 与 R3 的 2C/6M/3m **不同口径** (R3 是定向可实现性单席, 本席是欠定 + 交叉一致性单席), 直接比数字会误导。
- **形状上的观察**: 本轮 6 条 critical 中, **C1 / C5 / C6 三条都落在「Spec 对既有代码的事实断言与实读不符」这一类**, 而这恰是 R3/C2 的形状 (R3 已抓过一次「接线点描述有误」)。重写虽然把**行号**修准了 (9/9 全对), 但**行号背后的语义断言**仍有 3 处失真。⇒ 建议下一版把「Spec 中每一条对既有代码的事实断言」列成清单逐条实读复验, 而不是只核行号。
- **C2 / M1 / M4 三条同源**: 都来自「track-id 去掉 slug」这一个决策的下游未被穷举 (放弃语义 / 改名语义 / 终态语义)。D3 只论证了它对 overlap 可辨性的**正收益**, 未列它对 claim 生命周期其余动词 (release / abandon / rename) 的影响面。⇒ 建议补一张「track-id 形态 × 生命周期动词」影响矩阵。
