---
checkpoint: post_spec
round: 1
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R1 (重写版 v2) — a1-entry-claim-duplicate-work-guard · tech-lead 席

> **席位**: tech-lead (1/N) · **verdict**: **REVISE** · `scope_ok`: **true**
> **counts**: critical=**3** · major=**6** · minor=**4** · OUT_OF_SCOPE=0
> **timestamp**: 1785710000000
> **审计对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (重写 v2, 328 行, 未提交)
> **对照物**: `.aria/spikes/2026-08-02-S1/-S3/-S2-S4-S5-S6-batch.md` · `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-*-aggregated.md` · 原版 `git show b7c4933:.../proposal.md` · 姊妹 Spec `openspec/changes/linked-issue-normalization/proposal.md`
> **取证方式**: 全部 finding 的行号均经实读; C3 附可复现实跑脚本; 无一条基于记忆或推断

---

## 判定

**REVISE。** 重写确实解决了 R1–R3 的绝大部分具名缺陷 (逐条核对见文末「经核实正确」段, 覆盖率高于前三轮任何一版), spike 转述总体忠实。**但三条 critical 全部落在「重写引入的全新表面」上, 且都是本 Spec 三轮以来反复出现的同一形状**:

| # | 形状 | 与哪一轮同形 |
|---|---|---|
| C1 | 机制写了, 但**它的执行宿主没有执行它的权限** | R2/C2 + R3/C2 (「参数写了但生产路径不可达」) |
| C2 | 函数改对了, 但**没有人调用它** ⇒ 目标未达成而 SC 全绿 | `feedback_completion_signals_vs_runtime_invocation` (本 Spec 自己援引 3 次) |
| C3 | 校验器建好了, 但**它要判的真实语料 100% 不合格** ⇒ 恒红 | `feedback_verify_predicate_inputs_exist` + `feedback_false_green_dual_is_permanent_red` |

**最需要 owner 知道的一点**: C1 与 C2 不是「重写没做完」, 而是**重写把注意力全放在了「机制的内部正确性」上 (三处承重逻辑确实都补上了实测支撑), 却没有回头问「谁来执行它 / 它有没有权限执行」**。§闸门待裁 第 1 条自陈「三处承重逻辑现在都有实测支撑」—— 属实; 但「有实测支撑」与「能跑起来」之间还差一层, 而这层恰是前三轮反复摔倒的那层。

---

## Critical

### C1 — §2/§3 规定的两个 A.1 落点在 `allowed-tools` 上都没有 `Bash`; phase-a-planner 还没有 `AskUserQuestion` ⇒ 主机制在其指定执行宿主上不可调用

- **位置**: `proposal.md:79-86` (§2 bash 命令块) · `:118` (§2.3 `AskUserQuestion` 请裁) · `:146-148` (§3 双落点 D8) · Impact `:287-288`
- **证据 (逐字实读)**:

  | 文件:行 | `allowed-tools` |
  |---|---|
  | `aria/skills/phase-a-planner/SKILL.md:9` | `Read, Write, Glob, Grep, Task, Skill` — **无 Bash, 无 AskUserQuestion** |
  | `aria/skills/spec-drafter/SKILL.md:10` | `Read, Write, Glob, Grep, AskUserQuestion` — **无 Bash** |
  | `aria/skills/phase-b-developer/SKILL.md:10` | `Bash, Read, Write, Glob, Grep, Task, Skill` ← **今天唯一真跑 phase1_gate 的落点** (:91-93) |
  | `aria/skills/branch-manager/SKILL.md:10` | `Bash, Read, Grep` ← Phase B 第二落点 |
  | `aria/skills/audit-engine/SKILL.md:17` | `Read, Glob, Grep, Bash, Skill` ← §4 探针的宿主, **有 Bash ✅** |

  该字段在全仓 30+ 个 skill 上被一致维护 (实测枚举: 凡跑脚本的 skill 必列 Bash), 是承重字段不是装饰。补充实据: `phase-a-planner/SKILL.md` 与 `spec-drafter/SKILL.md` 今天**各自零个** ` ```bash ` 块、零个 `python3` 调用 —— 与其 `allowed-tools` 自洽; `phase-a-planner` 正文亦**零处** `AskUserQuestion`。
- **问题**: §2 的核心动作是一条 `python3 .../phase1_gate.py ...` 命令, §3 (D8, 被 spike S6 定为「真正的杠杆」) 要求它出现在 phase-a-planner **与** spec-drafter 两处。两处都无法执行该命令。§2.3 要求「经 `AskUserQuestion` 请裁」, 主落点 phase-a-planner 亦无该工具。Impact 表 `:287-288` 两行只写了正文内容变更 (「独立标题级认领步骤 + overlap 消费 + release 义务 + skip」/「第二落点 + 模板增字段」), **未提 `allowed-tools` 修订**。
- **危害**: 与 R2/C2 (「`include_terminal` 生产不可达」) 和 R3/C2 (「传递链第 2 步指错函数」) **完全同形**, 但这次落在**入口本身** —— §2.1 track-id 派生 / §2.2 heartbeat / §2.4 传递链三处打磨到实测级的逻辑, 全部挂在一个不能被调用的入口上。且失败是**静默**的: 执行时 AI 会跳过或改用别的方式, 不会报错。
- **建议修法** (与危害同向 = 让入口能被执行):
  1. Impact 表两行各补一句 `allowed-tools` 修订: `phase-a-planner` `+Bash, +AskUserQuestion`; `spec-drafter` `+Bash`;
  2. 或 —— 若不愿扩这两个 skill 的工具面 —— **显式成文委派路径** (phase-a-planner 有 `Skill`/`Task`, 可转 state-scanner 或子 agent 执行并回传 JSON), 并为委派路径单独建 SC;
  3. 二选一必须在 Spec 里写死, 不留给 A.2;
  4. 增一条断言型 SC:「两个落点的 SKILL.md frontmatter 含执行 §2 命令与 §2.3 请裁所需的全部工具」—— 该 SC 在现状必红, 且是唯一能机械挡住本类回归的验证面。

### C2 — §2.2 只改了 heartbeat 的匹配键, 全文未指定**谁调、什么时机调** ⇒ 保护窗仍是 24h, §2.2 开篇声明的问题原样存在, 而 SC-5~7 可全绿

- **位置**: `proposal.md:105-114` (§2.2) · `:202` (D4) · `:242-244` (SC-5/6/7) · Impact `:283`
- **证据**:
  - `heartbeat()` **生产调用点 = 0**。`aria/skills/state-scanner/lib/constants.py:43-44` 逐字:「**NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)**, so every live claim's heartbeat_at is frozen at acquire time」。全仓 grep `heartbeat(`: 仅函数定义 (`claim_lifecycle.py:178`) + docstring + 一条活文档行 (`layer-l-integration.md:45`, 见 m4);
  - Spec 全文 grep「heartbeat」共 11 处 (:60 / :105-114 / :202 / :242-244 / :283 / :322), **无一处**给出调用者或节律;
  - Impact 表 `:283` 只写 `claim_lifecycle.py | heartbeat 增 by-track 变体`; `:287` 的 phase-a-planner 行**不含** heartbeat;
  - spike S1 §6 逐字:「**heartbeat 该由谁在什么时机调 —— 这是 SKILL.md 指令面设计, 属 Spec 范围不属 spike**」⇒ S1 明确把这块交回给 Spec, 而 Spec 没接。
- **问题**: 改匹配键把 heartbeat 从「不可按字面实现」(R3/C1) 变成「可实现」, 但没让它「被执行」。`SWEEP_TTL = 86400` (24h) 仍 < 事故窗 48–72h ⇒ §2.2 第一句声明的「保护窗短于事故窗」**落地后一字不变**。更直接的自相矛盾: `:114` 逐字写「**heartbeat 为主, 再调作冗余, 不可只靠后者**」—— 而按当前 Spec 落地, 恰恰只剩后者 (「AI 记得再调」), 即 Spec 自己禁止的那个状态。
- **SC 层面的加重**: SC-5「heartbeat 跨 subprocess 两次调用 ⇒ 同一 track 的 claim 被刷新」是**函数级单测**, 在零调用者下必绿; SC-6/SC-7 同理。⇒ 三条 SC 全绿而保护窗未变 —— 精确复现本 Spec 自己援引了三次的 `feedback_completion_signals_vs_runtime_invocation`, 也复现 R2/C2 判过一次的形状 (「只能被单测满足, 生产不可达」)。
- **建议修法** (与危害同向 = 让 heartbeat 真的被跑):
  1. §2.2 增「调用者 + 触发点 + 节律」条款: 明确哪个 SKILL.md 的哪一步调、判据是什么 (A.1 期间每次实质推进前 / 距上次 > `HEARTBEAT_INTERVAL` 即调), 并入 Impact 表相应 SKILL.md 行;
  2. 增一条 **runtime-invocation 型** SC (与 SC-5~7 并列而非替代):「by-track heartbeat 在生产代码中至少有一个可达调用点」—— 口径可仿 aria-plugin#95 的 runtime-probe;
  3. 若判定 A.1 阶段不设周期回路 (可接受的设计选择), 则须把「保护窗仍 = 24h」明写进 §6 残余缺口表, 并撤回 §2.2 的「处置」措辞 —— 现在的写法让读者以为 48–72h 缺口已关闭。

### C3 — §1 的四条落地条款与真实语料 100% 不兼容: 13/13 现存字段值在前置 Spec 的归一下**全部不可解析**, 唯一的「无」也不合格, 而本 Spec 自己没有该字段

- **位置**: `proposal.md:68-75` (§1 四条) · `:255` (SC-13) · Impact `:293` · 本 Spec 头部 `:3-8`
- **证据 (实跑, 可复现)**: 按姊妹 Spec `linked-issue-normalization/proposal.md:53-63` 的五步规则逐字实现解析器 (剥空白 → 末个 `#` 拆分 → `int(number)` → `/` 末段取 basename), 跑遍 `openspec/{changes,archive}/*/proposal.md` 全 141 篇:

  ```
  field-bearing: 13 of 141
  OK=0   EXPLICIT_NONE=0   UNPARSEABLE=13
  ```

  失败原因分三类, 均为真实写法:

  | 类 | 实例 (逐字) | 为何不可解析 |
  |---|---|---|
  | markdown 链接 + 注解 | `[10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; triage ...)` | 末个 `#` 落在 `#122` 后, `number_str` = `122](https://...)...` |
  | URL fragment 吃掉末个 `#` | `... [issuecomment-16285](https://.../issues/113#issuecomment-16285))` | `number_str` = `issuecomment-16285))` |
  | 多 issue | `[#154](...) + [#157](...) + [#152](...) ; [#156](...) = #154 重复` / `[#94](...)/ [#95](...)` | 单值语义下无归宿 |

  另: 多篇**无 repo 段** (`Forgejo [#134](...)`, `[#154](...)`); 唯一带「无」的 (`linked-issue-normalization:6`) 写作 `无 (由 ... 发现, ...)` —— 带注解, 不满足 §1.1「**显式写 `无`**」。
  **本 Spec 头部 `:3-8` 六个字段 (Status / Created / Spec Level / 代码落点 / ship target / 前置依赖) 中没有「关联 Issue」** —— R1/M1 原文点名过「**本 Spec 自己头部就没有**」, 重写后依旧。
- **问题 (四条各自的成立性)**:
  - **§1.1 进模板** — 方向对, 但落点不全 (见 M4);
  - **§1.2 格式固定 `<org>/<repo>#<n>`** — 被表述为「固定/单一形态」, 实际是与现存 **100%** 用法的**断裂**。CLI help 示例确实是此形 (`phase1_gate.py:1202` 逐字 `'10CG/Aria#160'` ✅ 引用属实), 但 proposal 头部的真实书写惯例从来不是。多 issue 这一真实形态 (13 篇里 2 篇) 在单值 `--linked-issue` 下无处置;
  - **§1.3 机械校验 (warning)** — 上线即对 141/141 报 warning (收窄到 `changes/` 也是 8/9: 7 篇无字段 + 1 篇不可解析 + 1 篇「无」带注解仍不合格)。**恒红 = 零信息** (memory `feedback_false_green_dual_is_permanent_red`: 「假绿的反面是恒红, 同样零信息量」)。且 check 的**作用域**全文未定义 (全量 / 仅 `changes/` / 仅新增);
  - **§1.4 不追溯** — 只豁免了 **128 篇无字段**的, 对 **13 篇有字段但不合规**的**未表态** —— 而恰是这 13 篇会被 check 判红。
- **对 §1 优先级本身的评价**: **提为最高优先是对的**, S4 的 9% 是真数字, 「输入不存在则机制不存在」的判断成立。但 ⭐ 段 (`:58-62`) 的推论过强 —— 9% 里混了两种不同性质:「有 issue 但没写」(可回收) 与「本来就没有关联 issue」(不可回收, §1.1 让它写 `无`)。**没有任何 spike 测过这两者的比例**, 而机制收益只来自前者。⇒ §1 的优先级站得住, 但它对收益规模的隐含承诺没有证据支撑。
- **建议修法** (与危害同向 = 让 check 判的东西真的可判):
  1. §1.2 改为**双层定义**:「字段值必须以一个机器可解析的规范 token `<org>/<repo>#<n>` **开头**, 其后允许任意 markdown 链接与注解」—— 这与 13 篇现存写法只差一个前缀, 迁移成本最低, 且解析规则退化为「取首 token」, 字符级可钉;
  2. 明确多 issue 处置 (首个作 `--linked-issue`, 其余仅供人读; 或显式判为本 Spec 覆盖外并入 §6);
  3. §1.4 补两件事: check 的**作用域**, 与存量 13 篇的处置 (grandfather 白名单 / 一次性修 / 只对 `changes/` 生效);
  4. 本 Spec 头部补「关联 Issue」字段 (dogfood —— 它现在会是自己 check 的第一个 warning);
  5. 若要保留 §1 的最高优先定位, 补一次极廉价的语料测量 (13 篇之外, 抽样若干无字段 proposal 判其是否**本可**关联 issue), 把收益规模从假设变成数字。

---

## Major

### M1 — §2.4 把 `yielded` 说成被 `_TERMINAL` skip, 与代码相反; SC-8 的 yielded 分支在现状即为**绿**; 并丢失了 R2/M3

- **位置**: `proposal.md:127` · SC-8 `:245`
- **证据**: `aria/skills/state-scanner/lib/collision.py:210` 逐字 `_TERMINAL = ("done", "abandoned", "unknown")` —— **不含 `yielded`**, 且**含 `unknown`** (Spec 未列)。`lib/reconcile.py:57-59` 逐字:「NB: "yielded" is NOT terminal — it is a voluntarily PAUSED session that ... remains an active candidate」。
- **问题**: (a) `yielded` 今天**本来就可见**, `--include-terminal` 对它是 no-op ⇒ SC-8 的「`_TERMINAL` skip 的现状必红」对该子例不成立, 违反 SC 表自己的「怎么会红」栏, 也违反「substitute 须 baseline-failing」的纪律; (b) **R2/M3 被弄丢** —— R2 指出的真实风险方向相反:「`yielded` 在 SC-2 (active) 与 SC-5 (done) 之间无归属, 落地后历史 `yielded` 会以**活跃竞品**形态触发 `AskUserQuestion`」。重写把 yielded 归进 terminal 后, 这条风险在全文消失; (c) `unknown` 在 `_TERMINAL` 内却未被点名, `--include-terminal` 是否放行它无定义。
- **建议修法**: §2.4 改写为「`done`/`abandoned`(/`unknown`) 由 `--include-terminal` 放行; **`yielded` 本就不被 skip**」; 把 R2/M3 吸收进 §2.3 的 status 分档 (yielded ⇒「已暂停」而非「活跃」); SC-8 拆两条 —— (i) terminal 三态经 CLI 可见 (baseline 红); (ii) yielded 渲染为「暂停」措辞 (baseline 红, 因现状无分档)。

### M2 — §4 探针的「同 issue」匹配谓词全文未定义, 且按最可能的实现它在**自己的 motivating case** 上失效

- **位置**: `proposal.md:152-172` (§4 全章) · SC-16 `:258` / SC-17 `:259` / SC-19 `:261` · §6 `:189`
- **证据**: §4 开头只写「扫远端同 issue 的竞品 spec」(`:154`), 此后五个 bullet 分别定义了**扫描范围 / 触发时机 / fetch 代价 / 规模上限 / 消费面 / 盲区**, **无一句**定义匹配输入从哪取、怎么比。SC-16/17 同样只说「命中 / 无同 issue spec」。而第 5 次事故的两份真实 proposal ——
  - `openspec/changes/phase-c-integrator-ci-path-coverage/proposal.md` 字段值 `[10CG/aria-plugin #122](https://.../issues/122) ...`
  - `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/proposal.md` 字段值 `[10CG/aria-plugin #122](https://.../issues/122) ...`

  —— 在前置 Spec 的归一下**双方均不可解析** (C3 实跑已证)。⇒ 谓词若走归一, 探针在**它被造出来要抓的那一例**上恒漏; 若走原串精确匹配, 两串注解部分不同, 同样漏。
- **问题**: R1/M4「副机制只定义检测半, 未定义消费半」在重写中被判为已修 (§4 补齐了消费面 / exit code / 规模上限), 但**检测半自己的谓词**仍缺 —— 注意力被消费面吸走, 判定输入没人管, 正是 memory `feedback_verify_predicate_inputs_exist` 的形状 (「5 轮打磨公式, R5 才发现它裁决的数据不存在」)。而 §6 缺口表 `:189` 已把探针记为「部分覆盖 legacy 轨」—— 在谓词未定义的前提下声称覆盖。
- **建议修法**: §4 增「匹配谓词」小节, 钉死输入来源 (proposal 头部字段? 目录 slug? 标题?) 与比较规则, 并**复用 §1.2 定下的规范 token**; 增一条以**上述两份真实 proposal 为 fixture** 的 SC (它们是现成的可证伪语料, 且就是本 Spec 的 motivating case) —— 谓词若对它们不命中即不合格。

### M3 — 两 Spec 间存在**归一能力的职责真空**: 谁把归一暴露成可复用 callable, 两边都指给对方

- **位置**: 本 Spec `:72` (§1.3「值可被**前置 Spec 的归一**解析」) · `:96` (§2.1 basename「**经前置 Spec 归一**」) · Impact `:281-294` ‖ 姊妹 Spec `linked-issue-normalization/proposal.md:79` (§接口面) · `:92` (D6) · `:118` (非目标) · Impact `:129-135`
- **证据**: 姊妹 Spec 逐字:「`linked_issue_overlaps` 的签名与返回 schema **不变**; **只改内部比较谓词**」(:79); D6「签名与 schema 不变 ⇒ Phase B 现有调用方零改动」(:92); 非目标「**不改** `phase1_gate.py` 的 CLI / `run_gate` 签名 (本 Spec 只动 `collision.py` 内部谓词)」(:118); Impact 表只有 `collision.py` + tests + 发版文件 ⇒ **不产出任何公开归一 API**。
  本 Spec 的 Impact 表 (`:281-294`) **既无 `collision.py` 也无任何新 lib**, 却有**两处**依赖调用该归一 (§1.3 的 custom check 脚本 / §2.1 的 basename 段)。
- **问题**: 两边都把这块指给对方 = 职责真空 (审计范围 D 点名要找的那种)。落地时实现者只有两条路: 在 check 脚本里**复写**一份归一 (双实现漂移 —— 正是 S5 刚揭示的「两层归一不一致」换个位置复发), 或临时突破姊妹 Spec 的非目标。
- **建议修法**: 本 Spec 明写「新增公开 `normalize_linked_issue()` (落 `collision.py` 或新 `lib/linked_issue.py`)」并入 Impact, 同时在 §前置依赖 注明这是对姊妹 Spec「签名不变」的**增量而非违反** (新增函数不改既有签名); 或反向请 owner 裁定把该 API 划回姊妹 Spec 并同步改其 Impact 与非目标 —— **两个 Spec 有一个必须认领, 现在是零。**

### M4 — 「进模板」丢了 R1/M1 的 `standards/` 一半; 机械校验又只落主仓 ⇒ 两条腿在 plugin-wide 尺度上都不覆盖

- **位置**: `proposal.md:70` (§1.1) · Impact `:288` (spec-drafter) / `:293` (state-checks.yaml)
- **证据**:
  - **原版 Impact 表逐字**有「`skills/spec-drafter/` 模板 **+ `standards/`** | ⭐ R1-fix/M1: 「关联 Issue」进 proposal 模板并成文」(orig `:310`); R1/M1 原文亦是「**standards 与 spec-drafter 模板零定义**」。**重写只剩 spec-drafter, `standards/` 消失** —— 这是主审 C 要找的「已吸收 finding 在全量重写中丢失」的实例;
  - `standards/openspec/templates/proposal-minimal.md` 是 Level-2 proposal 的**模板 SOT** (`standards/openspec/templates/README.md:10` 与 `:38` 明列, `:51-52` 逐字 `cp standards/openspec/templates/proposal-minimal.md → changes/{feature-name}/proposal.md`), 实读该模板 1-30 行: 字段只有 Level / Status / Created, **无「关联 Issue」**; 全 standards 仓 grep「关联 Issue」仅 `conventions/git-commit.md:447` 一处无关命中;
  - `.aria/state-checks.yaml` 是**项目级 opt-in** 文件, 由 state-scanner Phase 1.11 读取 (`aria/skills/state-scanner/SKILL.md:119` 逐字「1.11 custom_checks (需 `.aria/state-checks.yaml`)」), **不随 aria-plugin 分发**。
- **问题**: (a) 走 standards 模板复制路径 (README 明写的官方路径) 的项目照样产出无字段 proposal; (b) §1 自证「模板只影响新建且 AI 可以删 ⇒ **无机械回声的义务会退化**」(`:75`) —— 而那个机械回声在 **Aria 之外的每个项目都不存在**, 该论证在本仓之外全线失效; (c) proposal 文档格式属 standards 域 (CLAUDE.md「Aria 定义…文档格式 / 流程 / 命名规范」), 漏改亦触 Rule #3。
- **建议修法**: Impact 补 `standards/openspec/templates/proposal-minimal.md` (必要时含 `standards/openspec/project.md` 的字段说明); 对 plugin-wide 机械回声另择宿主 (spec-drafter 自带校验脚本 / plugin 侧 hook), **或**显式成文「本 Spec 的机械校验只覆盖 Aria 仓, 其余项目仅有模板 (承认会退化)」并记为已知限 —— 不要以一般性的「机械校验」措辞掩盖覆盖边界。

### M5 — `--linked-issue` 缺席时 `:1229` 门控整块 overlap 逻辑; 按 §1 自己的统计那是**多数路径**, 而 §6 缺口表未列

- **位置**: `proposal.md:92` (§2.1 回落分支) · `:116-123` (§2.3) · `:129-133` (§2.4) · `:182-189` (§6)
- **证据**: `aria/skills/state-scanner/scripts/phase1_gate.py:1229` `if args.linked_issue:` 门控 `:1230-1237` **整块** ⇒ 不传该参数时输出 dict 里**根本没有** `linked_issue_overlap` 键 (不是空列表, 是键缺失), `--include-terminal` 亦静默无效。**R3 的 minor 逐字记过这条** (「`--include-terminal` 无 `--linked-issue` 时静默无效 (`:1229` 的 `if args.linked_issue:` 门控整块), 与「零裁量」基调不符」) —— **重写后该条在全文消失**, 属主审 C 的第二个丢失实例。
- **问题**: §1 实测字段覆盖率 9%, 且 §1.1 规定「无关联时显式写 `无`」—— 即使字段 100% 补齐, 写「无」的那部分仍无 issue 可传。⇒ 主机制在这条分支上产出的不是「空结果」而是「无结果键」, §2.3 的消费面与 §2.5 的降级契约都没为它定义行为, 最易被渲染成「无碰撞」—— 正是 §2.5 自己禁止的「零证据当正证据」。§6 缺口表列了 4 条, 独缺这条量级最大的。
- **建议修法**: §6 增一行「本轨无关联 issue (含显式 `无`) ⇒ 主机制零信号, 仅 §4 探针部分覆盖 | 窗口: 无界」; §2.3/§2.5 明确该分支措辞为「本轨无关联 issue, 未做同 issue 核实」而非「无碰撞」; 可选 —— 在该分支给探针一个替代输入 (spec-slug / 标题关键词)。

### M6 — `phase1_gate.py:1235-1237` 的 fail-soft `[]` 与 §2.5 的降级契约互斥, 且结构上不在 `GateResult.error` 的覆盖面内

- **位置**: `proposal.md:137-140` (§2.5 第二条) · SC-10 `:247`
- **证据**: `phase1_gate.py:1235-1237` 逐字:
  ```python
  except Exception as exc:  # fail-soft: overlap advisory must not break the gate
      logger.warning("phase1_gate: linked_issue overlap check skipped (%s)", exc)
      out["linked_issue_overlap"] = []
  ```
  该赋值发生在 `out = _gate_result_to_dict(result)` (`:1225`) **之后**, 是 `out` 上的独立键 ⇒ 把 `GateResult.error` 置为 `"fetch_degraded"` (docstring `:210` 确已预留该 token ✅, Spec 引用属实; grep 全仓确实**从未被赋值** ✅) **在结构上无法覆盖这条路径**。
- **问题**: 与 §2.5 自己写的「零证据不得当正证据」直接互斥 —— overlap 计算异常时消费面拿到 `[]`, 与「真没人在做」逐字节相同, 只留一条 logger.warning。这是 memory `feedback_fix_recurs_in_its_own_fallback_path` 的教科书形状: 要治的病在既有 except 兜底路径上原样存在, 而修复条款只覆盖了 fetch 一条腿。
- **建议修法**: §2.5 把降级契约从「fetch 降级」扩为「**任何**使 overlap 无法核实的降级」, 并指明它需要一个 **`out` 层**的可见标记 (新增 `linked_issue_overlap_error`, 或该键置 `null` 而非 `[]` —— 后者需评估既有 Phase B 消费方); SC-10 增子例:「`read_claims` 抛异常 ⇒ 消费面渲染『未能核实』」(现状 `[]` 必红)。

---

## Minor

- **m1** — `:150` 逐字「本 Spec 采用 **claim 侧口径 (uuid)**」与 §2.1 自己的实据矛盾: claim record 的 `container` 字段来自 `_resolve_identity()` → `get_container_id()`, 即 `identity.py:222` 的 **label-first** (`claim_lifecycle.py:150` `container=resolved.container_id`)。今天两容器 label 全空故二者巧合相同; 一旦有人照 `identity.py:126-140` 的模板设 label (§2.1 整个论证的前提), track_id 的容器段 (uuid) 与 `claim.container` (label) 就分叉 ⇒ 变成**三个**口径, 而 §3 的 follow-up 只记了两个。建议 §3 改为「本 Spec 为 track_id 引入 uuid 口径, 与 `claim.container` (label-first) 及 handoff `owner-container` 并存, 三者关系记为 follow-up」。
- **m2** — §4 exit code 契约内部不齐: `:171` 定「非 0 **仅**用于探针自身失败」, 而 SC-18 (`:260`) 把「**无远端**」也判 exit 非 0。无 `enforced_remotes` 是合法环境状态, 不是探针故障; 且既然 §4 明写「不阻断」, 非 0 的消费者是谁未定义。建议二选一并写死 (推荐: 无远端 ⇒ `degraded` + exit 0, 与「不阻断」自洽; exit 非 0 只留给真异常)。
- **m3** — `:132` 引「`_run_gate_impl` (334-1075 行)」上界略偏: `_run_gate_impl` 起于 `:334` 属实, 但 `run_gate` 已在 `:1031`、`run_gate_synthetic` 在 `:1066` ⇒ 其函数体上界约 `:1029`。结论 (grep 命中 0) 与修法均不受影响, 仅行号精度。
- **m4** — `layer-l-integration.md` 进了 Impact 表 (`:291`) 但只点名「闸门仅在 Phase B 触发」这一处。同文件 `:45` 另有一行把 heartbeat 记为「`phase-b-developer` mid-cycle | **每 10min** (caller 负责调度) | `lib/claim_lifecycle.py::update_heartbeat()`」—— 实测 `update_heartbeat` **在全仓不存在** (仅此一处文本), 且「每 10min」与 `constants.py:43-44` 的「零生产调用点」相反。C2 落地时该行必须一并订正, 否则活文档继续声称一个不存在的回路 (同 `feedback_cross_doc_claim_verify_at_target`)。

---

## 经核实**正确**的部分 (下轮免重复)

**spike 转述忠实性 (主审 B) —— 逐条对照, 未发现加强/削弱/曲解**:

| Spec 处 | spike 原文 | 判定 |
|---|---|---|
| §2.2 heartbeat 定 (b) | S1 §5.1 明确「C3 的处置定为 (b)」, 非三选一悬置 | ✅ 忠实 (S1 自己已收敛为定论) |
| §2.2 「照抄隔壁函数」引文 | 与 `claim_lifecycle.py:387-393` docstring 逐字核对通过 | ✅ |
| §2.2 判否 session 落盘 | S1 §3「(a) 判否, 理由不是做不到而是 (b) 更省且已有先例」 | ✅ 忠实, 未强化 |
| §2.2 「冗余/不可只靠后者」 | S1 §4「建议组合: 主用 (b), (d) 作自然冗余。**不要**只靠 (d)」 | ✅ 逐字忠实 |
| §2.1 三段派生规则 | S3 §3 + §5.1 定案形态一致 (含 `str(int(number))`、不截断、跳过 label、hostname 兜底) | ✅ |
| §2.3 「接手 = 两步人工」 | S3 §4 建议 (i) 并明示「(ii) 不建议在本 Spec 引入」 | ✅ 忠实, 未把三选一写成定论 |
| §4 fetch ~13.8s / 不称轻量 / 30s / 重试 | S2 §实测数据 + §结论四条 | ✅ 四条全数落地 |
| §4 复用缓存判否 | S2「缓存唯一写入点 `remote_refresh.py:691`, 只被 `scan.py` Phase 0.5 调用」 | ✅ |
| §6 + D10 不做登记表, 依据全换 | S6「D5 结论不变, **理由全部替换**」+ 「秒级」已作废 | ✅ 忠实执行了「论证段整体改写」 |
| §Why 表格「S4/S5 各推翻一条上游结论」 | S4 (19 vs 802, 真实输入总体 0 实例) / S5 (`10cg.local` 真实仓, 11 open issues) | ✅ 数字与定性均对得上 |
| D9 不建别名表 | S4 §结论三条 | ✅ |

**代码事实引用 —— 抽查 11 处, 全部属实**:
`collision.py:210` `_TERMINAL` 位置 ✅ (内容有误, 见 M1) · `collision.py:219-220` 自排除逐字 ✅ · `phase1_gate.py:1232` 唯一调用点 ✅ (grep 复核: 生产代码仅此一处) · `_run_gate_impl` 对 `linked_issue_overlaps` grep 命中 0 ✅ · `GateResult.error` docstring `:210` 预留 `"fetch_degraded"` 且从未赋值 ✅ · `identity.py:222` label-first ✅ / `:244` hostname 兜底 ✅ · `claim_lifecycle.py:425` 只匹配自己的 container ✅ · `spec-drafter/SKILL.md:9` `user-invocable: true` ✅ · `audit-engine/SKILL.md:85`「Round 1 启动前一次性」逐字 ✅ · `execution-modes.md` Convergence `:84-111` / Challenge `:113-144` 边界精确 ✅ · `DEFAULTS.json:124-128` `adaptive_rules.level_3 → challenge` ✅ · `phase1_gate.py:1202` help 示例 `'10CG/Aria#160'` ✅ · `.aria/config.json` `state_scanner.coordination.enabled = true` / `audit.checkpoints.post_spec = convergence` ✅ · `audit-engine` 零 `scripts/` 零 `tests/` ✅ · 语料 141 篇 / 13 篇有字段 / 128 篇无 ✅ (独立复算一致)。

**三轮 finding 的吸收率 (主审 C) —— R1 8 major + R3 6 major 逐条核对**:

| 来源 | 状态 |
|---|---|
| R1/M1 字段进模板 | ✅ 提为 §1 (但 `standards/` 一半丢失 → M4) |
| R1/M2 生命周期对偶 | ✅ §5 三条退出路径 |
| R1/M3 `coordination.enabled` | ✅ §2.5 + Impact config-loader |
| R1/M4 副机制消费半 | ✅ §4 消费面 + exit code (但检测谓词仍缺 → M2) |
| R1/M5 「Step 0.5」互斥 | ✅ §4「per-round 入口探针, 不叫 Step 0.5」+ 引 `:85` |
| R1/M6 规模/代价 | ✅ §4 规模上限 + `handoff_multibranch.py` 440 分支先例 + no silent caps |
| R1/M7 fetch 降级进 error | ✅ §2.5 (但 fail-soft `[]` 一条腿未覆盖 → M6) |
| R1/M8 layer-l 同步 + `--repo-path` | ✅ 两半均落 (`--repo-path "<主仓根>"` 已钉) |
| R1/C4 SC 测试宿主不存在 | ✅ SC 表头「验证面分层」明列真实宿主 + 行为类不冒充结构化测试 |
| R1/C4(c) Rule #6 误判 | ✅ 改判第三行, 三条件齐备, 「不申请豁免」措辞与 owner `db2e983` 裁定 (substitute 与「不适用」二选一) 一致 |
| R3/M1 `container-short` 截断 | ✅ §2.1 uuid 不截断 + SC-3 |
| R3/M2 「接手」无定义 | ✅ §2.3 两步人工 + D6 |
| R3/M3a 分隔符碰撞 | ✅ 移交姊妹 Spec (S5 追加 `./_ → -`), 边界干净 |
| R3/M3b number 表示 | ✅ §2.1 `str(int(number))` + SC-4 |
| R3/M4 探针 fetch 缓存 | ✅ §4 判否 + 实测代价 |
| R3/M5 Convergence/Challenge 双段 | ✅ §4 明写两段都改 + 引 `DEFAULTS.json` 分发论证 |
| R3/M6 插入点结构 | ✅ §2「独立标题级步骤, 不塞进 YAML 列表」 |
| **丢失** | **R2/M3 (`yielded` 无归属) → M1** · **R3/minor (`:1229` 门控) → M5** · **R1/M1 的 `standards/` 一半 → M4** |

**两 Spec 边界 (主审 D) —— 除 M3 的归一 API 真空外, 其余干净**: 前置依赖声明明确 (`:8`); 双方非目标互斥无重叠 (本 Spec `:267-268` 不改归一 / 不做截断型别名 ‖ 姊妹 `:118-123` 不做 A.1 前移 / 不动 `_TERMINAL` / 不引入 track-id 变更); 姊妹 Spec 的 SC-5b 与本 Spec §2.1 「含 S5 追加的 `./_ → -`」对齐, 无重复实现。

**§闸门待裁 (Rule #10)**: 论证成文正确, 四类封闭白名单逐条判否, 无自我豁免, 且 `:325` 主动点名「§1 是全新章节、§2.1/§2.2 措辞从未经任何席位审过」—— 该自认与本轮实际发现高度吻合 (三条 critical 中两条落在它点名的区域)。**「自认存疑」再次是真信号**, 与 R3 的同一观察一致。

---

## 给 owner 的收敛性判断

**本轮不构成「继续不收敛」的证据 —— 它是新对象的第一轮**, 与前三轮不同口径 (审的是全量重写而非补丁), 不可与 R2→R3 的 4→6 序列并列。

三条 critical 的性质值得单独看: **没有一条是「设计想错了」**, 全部是「设计对了但缺一层落地条件」(权限面 / 调用者 / 语料兼容性)。这与 R1–R3 的 critical 性质不同 (那些是逻辑互相拆台)。⇒ 修法都是**加法而非改写**, 且三条彼此正交, 不存在「修 A 破 B」的耦合 —— 这是重写相对打补丁的实质改善。

**AI 不预判裁决。**
