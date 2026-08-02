# post_spec R1 (重写版 v2) — backend-architect

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=3 minor=1

> 审计对象: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (重写 v2, 全文 328 行, 未提交)。
> 全部结论基于实读代码 (`aria/skills/state-scanner/scripts/phase1_gate.py` 全文 1246 行 · `lib/claim_lifecycle.py` 全文 472 行 · `lib/identity.py` 全文 286 行 · `lib/collision.py` 全文 345 行 · `lib/claim_schema.py` · `lib/track_id.py` · `lib/constants.py` · `lib/reconcile.py` · `scripts/release_gate.py` · `scripts/collectors/{multi_remote,handoff_multibranch,remote_refresh}.py` · `phase-a-planner/SKILL.md` · `spec-drafter/SKILL.md` · `phase-b-developer/SKILL.md` · `branch-manager/SKILL.md` · `audit-engine/SKILL.md` + `references/execution-modes.md` · `config-loader/DEFAULTS.json` · `standards/openspec/templates/proposal-minimal.md` · `.aria/state-checks.yaml`) + spike 原文 (`.aria/spikes/2026-08-02-S1-heartbeat-feasibility.md` / `-S2-S4-S5-S6-batch.md` / `-S3-track-id-derivation.md`) + 一次本仓真实 `git symbolic-ref`/`git remote -v` 现场取证。未修改任何文件, 未 commit。

---

## Findings

### [CRITICAL] A.1 两个指定落点的 `allowed-tools` 都不含 `Bash`, `phase-a-planner` 还不含 `AskUserQuestion` —— §2 的核心命令与 §2.3 的请裁机制在其指定宿主上均不可执行

- **位置**: `proposal.md:79-86` (§2 `python3 phase1_gate.py ...` 命令块) · `:118` (§2.3 要求 `AskUserQuestion` 请裁) · `:146-148` (§3 D8 双落点) · Impact 表 `:287-288`。
- **实读证据**:
  ```
  aria/skills/phase-a-planner/SKILL.md:9   allowed-tools: Read, Write, Glob, Grep, Task, Skill
  aria/skills/spec-drafter/SKILL.md:10     allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
  aria/skills/phase-b-developer/SKILL.md:10 allowed-tools: Bash, Read, Write, Glob, Grep, Task, Skill  ← 对照组: 今天唯一真跑 phase1_gate 的落点, 有 Bash
  ```
  `grep -n "AskUserQuestion" aria/skills/phase-a-planner/SKILL.md` 零命中。
- **问题**: §2 要求 A.1 起草前"作为独立标题级步骤"跑一条 `python3 .../phase1_gate.py ...` 命令 —— 这需要 `Bash`。`phase-a-planner` 和 `spec-drafter` 两个指定落点 (D8) **都没有 `Bash`**。§2.3 进一步要求 overlap 非空时"经 `AskUserQuestion` 请裁", 而 `phase-a-planner`(主落点)**没有 `AskUserQuestion`**(`spec-drafter` 有, 但它不是主入口)。Impact 表 `:287-288` 两行只写正文变更("独立标题级认领步骤 + overlap 消费 + release 义务 + skip"/"第二落点 + 模板增字段"), 完全没提两处 `allowed-tools` 需要修订。
  这个结论直接决定了 Q1/Q2/Q3 的答案基础: 无论 §2.1 track-id 派生、§2.2 heartbeat、§2.4 `include_terminal` 的内部逻辑打磨得多精确, 只要它们挂在一个不能被调用的入口上, 都不会在生产中发生——而失败是**静默**的(Claude Code 不会因为工具不在 `allowed-tools` 白名单而报错并提示"这条指令做不到", 它会跳过或改用别的近似方式继续)。
- **建议修法**: Impact 表补两行 `allowed-tools` 修订 (`phase-a-planner` `+Bash, +AskUserQuestion`; `spec-drafter` `+Bash`); 或显式写委派路径 (`phase-a-planner` 已有 `Skill`/`Task`, 可转 `state-scanner` 或子 agent 代跑 CLI 并回传 JSON, 自己只做请裁), 二选一必须在本轮定, 不留给 A.2。并加一条断言型 SC:"两落点 SKILL.md frontmatter 含执行 §2 命令与 §2.3 请裁所需的全部工具"——现状必红。

### [CRITICAL] §2.2 heartbeat 改了匹配键, 但全文未指定"谁调、什么时机调"——保护窗实质仍是 24h, 且这条恰是 spike S1 明确点名"归还给 Spec"却未被接住的问题 (回答 Q1)

- **位置**: `proposal.md:105-114` (§2.2 全段) · D4 `:202` · SC-5/6/7 `:242-244` · Impact `:283`。
- **"照抄" 本身的可行性 (Q1 前半)**: 实读 `claim_lifecycle.py:377-471`(`release_claim_by_track`)与既有 `heartbeat()`(`:178-271`)后确认——两者除"改哪个字段"(前者改 `status`, 后者该改 `heartbeat_at`)外, 脚手架**逐行同构**: 同一套 `_resolve_identity` → `derive_track_id(raw_track_id)` 归一 → `read_claims` → `[rec for rec in ... if rec.container==... and rec.track_id==norm and rec.status=="active"]` 过滤 → 按 `claimed_at` 排序遍历 → 逐条 `write_claim`、失败即返回(已成功的保留, 幂等可重跑)的模式(`:422-428` 过滤条件, `:425` 逐字 `if rec.container == resolved.container_id`)。**"照抄"在实现层完全可行, 没有被"写回语义不同"卡住**——因为需要变的只是被重建的 `ClaimRecord` 里哪个字段取新值、哪个字段保持原值, 循环与匹配谓词可以逐字复用。这部分 Spec 的技术判断是对的。
- **但"照抄"到位后, 没人调它 (Q1 真正的坑)**: 全仓 `grep -rn "heartbeat("` 结果只有函数定义/docstring/类型注释, **生产调用点 = 0**。`lib/constants.py:43-45` 逐字自陈:「and in reality NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either), so every live claim's heartbeat_at is frozen at acquire time」——`phase1_gate.py:511-526` 的 self-resume 分支(7a)代码注释同样写"heartbeat_at is NOT refreshed here"。
  Spec 全文对"heartbeat"的 11 处提及(`:60/:105-114/:202/:242-244/:283/:322`)**没有一处**说明新的 by-track 变体会被**哪个 SKILL.md 的哪一步、按什么节律**调用; Impact 表 `:283` 只写"`claim_lifecycle.py` | heartbeat 增 by-track 变体", `:287` 的 `phase-a-planner` 行不含 heartbeat 字样。
  更关键的是: `.aria/spikes/2026-08-02-S1-heartbeat-feasibility.md` §6 逐字:「**heartbeat 该由谁在什么时机调 —— 这是 SKILL.md 指令面设计, 属 Spec 范围不属 spike**」——spike 明确把这个问题验收标准交还给 Spec, 而重写版的 proposal.md 正文没有接住它。
  即使想把它接进现有的 self-resume 分支(7a), 这条路也不是"顺手加一行调用"就够: `_self_resume()`(`phase1_gate.py:264-279`)要求 `verdict.winner.session == identity.session_id` 精确匹配, 而 `identity.py:247-263`(`get_session_id`) docstring 逐字"Fresh on every call"——`_main()` 每次 CLI 子进程调用都走 `get_identity()` 生成全新 session, 两次独立的 `phase1_gate.py` 调用**永远不会**在 session 段相等。也就是说, 若真要让 heartbeat-by-track 在 A.1 期间的多次 CLI 调用间起作用, 还需要同时改 `_run_gate_impl` 的分支判定逻辑本身(把"是不是自己"的判据从 session 换成 container+track_id)——这是对 `phase1_gate.py` 核心 9 步决策流的改动, Impact 表完全没有覆盖(它对 `phase1_gate.py` 的改动只列了 `--include-terminal` 一项, 见下条 Major)。
- **危害**: §2.2 开篇写的问题("事故窗 48–72h > SWEEP_TTL 24h")在按 Impact 表字面实现后**原样存在**; 更直接的自相矛盾——`:114` 写"heartbeat 为主, 再调作冗余, 不可只靠后者", 而按当前 Spec 文本能落地的**只有**"再调"(AI 记得再调用 phase1_gate 自然续期), 即 Spec 自己点名要避免的那个状态。SC-5/6/7 若实现为对 `heartbeat_by_track()` 的直接单测, 会在零调用者下全绿, 掩盖保护窗未关闭的事实。
- **建议修法**: §2.2 补"调用者+触发点+节律"条款并写回 Impact 表对应 SKILL.md 行(例如: A.1 期间每次实质推进前, 或距上次心跳 > `HEARTBEAT_INTERVAL` 即调); 增一条 runtime-invocation 型 SC(仿 `.aria/state-checks.yaml` 里 `coordination-gate-invocation` 的活体探针思路: 生产 telemetry 里至少一条 heartbeat-by-track 被真调用的记录), 与函数级 SC-5/6/7 并列而非替代; 若 A.2 阶段决定 A.1 不设周期回路(可以是合理的范围裁剪), 则必须把"保护窗仍=24h"显式写回 §6 缺口表, 撤回 §2.2 现在"处置"二字给读者的"已解决"印象。

### [MAJOR] §2.4 `include_terminal` 的传递链遗漏 `lib/collision.py`; 且 Spec 对 `_TERMINAL` 成员的描述与代码相反 (回答 Q3)

- **位置**: `proposal.md:125-135`(§2.4 全段) · Impact `:285` · SC-8 `:245`。
- **实读证据**: `collision.py:210` 逐字 `_TERMINAL = ("done", "abandoned", "unknown")`, `:213` `if c.status in _TERMINAL: continue`——**这是全仓唯一一处**决定"哪些状态被隐藏"的代码。`--include-terminal` 要落地, 除了 §2.4 已经交代清楚的"`_main()` 新增 flag + `:1232` 调用处加关键字参数"外, **必然还需要改 `linked_issue_overlaps()` 自身的签名和 `:213` 这行判断**(接收新参数、按参数决定是否继续 `continue`)——否则调用处传的关键字参数根本没有函数签名可接。但 Impact 表(`:281-294`)从头到尾**没有 `lib/collision.py` 这一行**。§2.4 的原话"不碰 `run_gate`/`_run_gate_impl` 签名"这句本身是对的(我验证 `_run_gate_impl` 是 `phase1_gate.py:334` 起始的函数体, 对 `linked_issue_overlaps` 字符串 grep 命中 0), 但它只保护了两个函数, 没有说清楚 `collision.py` 也要动, Impact 表因此漏了一整个文件。
- **`_TERMINAL` 成员描述本身有误**: proposal 正文说"`done`/`abandoned`/`yielded` 的同 issue claim 必须可见……`_TERMINAL` 会直接 skip 它们"(`:127`)。但代码里 `_TERMINAL` 是 `("done", "abandoned", "unknown")`——**不含 `yielded`**, 却**含 `unknown`**(Spec 未提)。独立核实 `lib/reconcile.py:57-59` 逐字:「NB: "yielded" is NOT terminal — it is a voluntarily PAUSED session that ... remains an active candidate」——"yielded" 在本代码库的既有设计里**本来就该保持可见**, 不属于要被 `--include-terminal` "放行"的对象; 它今天就没被 `_TERMINAL` 过滤, `--include-terminal` 对它是 no-op。这意味着 SC-8"`_TERMINAL` skip 的现状必红"这句对 yielded 子例不成立——现状对 yielded 已经是绿的, 违反 SC 表自己"怎么会红"一栏的设计前提; 而真正被过滤、Spec 却完全没讨论的 `unknown`(schema 版本不识别时的哨兵状态), `--include-terminal` 要不要放行它, 全文没有定义。
- **建议修法**: Impact 表补一行 `lib/collision.py`(`linked_issue_overlaps` 新增 `include_terminal` 参数 + `tests/test_collision.py` 相应用例); §2.4 改写为"`done`/`abandoned`(/`unknown`) 由 `--include-terminal` 放行; `yielded` 本就不在 `_TERMINAL` 内, 无需此 flag 即可见"; SC-8 拆两条覆盖 terminal 三态与 yielded 各自的真实红/绿基线。

### [MAJOR] §4"只扫 `enforced_remotes` × 各自默认分支"未定义"默认分支"怎么取——朴素做法在本仓自己的第二个 remote 上当场失败 (回答 Q4)

- **位置**: `proposal.md:152-172`(§4 全段, 尤其 `:170`"只扫 `enforced_remotes` × 各自默认分支") · SC-19 `:261`。
- **`enforced_remotes` 本身有实锚**: 确认这不是凭空引入的概念——`aria/skills/config-loader/DEFAULTS.json:7/13/59` 与 `scripts/collectors/multi_remote.py:255`(`resolve_enforced_remotes`)已经是既有、可直接复用的配置解析函数, 这一半没问题。
- **"各自默认分支"没有可执行的取法, 且我在本仓现场验证了朴素做法会失效**:
  ```
  $ git remote -v
  github  git@github.com:10CG/Aria.git (fetch/push)
  origin  ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (fetch/push)

  $ git symbolic-ref refs/remotes/origin/HEAD
  refs/remotes/origin/master              ← 有值

  $ git symbolic-ref refs/remotes/github/HEAD
  fatal: ref refs/remotes/github/HEAD is not a symbolic ref   ← 无值
  ```
  原因: `refs/remotes/<remote>/HEAD` 这个符号引用只在 `git clone` 时对**被克隆的那个 remote**(通常是 `origin`)自动写入; 后续用 `git remote add`(本仓 `github` 就是这么加的)加进来的 remote **不会**自动获得这个符号引用, 除非显式跑一次需要联网查询的 `git remote set-head github --auto`。而 `github` 恰恰是本仓 CLAUDE.md 明文要求双推的**两个** `enforced_remotes` 之一——即"各自默认分支"这个概念要处理的**典型场景**里就有一个会让最直观的实现方式(读本地 `refs/remotes/<remote>/HEAD`)直接报错或返回空。
  正确做法(如 `git ls-remote --symref <remote> HEAD`, 不依赖本地 clone 历史、直接问远端)是存在的, 但 Spec 全文、以及给出 fetch 代价实测的 spike S2, 都没有提到需要用这类"问远端"的方式, 也没有讨论"若某 remote 从未 `set-head` 过, 如何降级"。若实现者顺手用了本地符号引用这条路, 会在这条 Spec 明确点名要覆盖的多远程场景上产生一个**没有被任何 SC 覆盖、也不会报错**的静默欠扫描——与 §4 自己"超限须 `log()` 披露、no silent caps"的原则(`:170`)方向相反, 只是触发条件从"分支数超限"换成了"第二 remote 没有本地 HEAD 符号引用"。
- **建议修法**: §4 补一句"默认分支解析方式": 用 `git ls-remote --symref <remote> HEAD` 取值(与既有 fetch 预算同属一次网络往返, 不额外增加 S2 实测代价的数量级), 无法解析时按 `degraded` 处置并 `log()` 披露(与 SC-18 的降级契约同款), 不得静默假设为固定分支名。

### [MAJOR] `.aria/state-checks.yaml` 是本仓项目级文件, 不随 aria-plugin 分发; §1 论证"必须机械校验而非只改模板"的理由在 Aria 之外的每个采用者身上都不成立 (回答 Q5 的时序/可写性之外, 补一个范围维度)

- **位置**: `proposal.md:68-76`(§1 全段, 尤其 `:75` 逐字"模板只影响新建, 且 AI 可以删。本 Spec 的 §Why 自证「AI 会遗漏步骤」—— 无机械回声的义务会退化。") · Impact `:293`(`.aria/state-checks.yaml`)/`:288`(`spec-drafter/SKILL.md`)。
- **Q5 本题(check 能不能写、时序成不成立)**: 参照 `.aria/state-checks.yaml` 现有 10 条 check 的形态(`name`/`description`/`command`/`severity`/`fix`/`timeout_seconds`/`enabled`, 由 state-scanner Phase 1.11 串行跑 shell/python 片段, exit code 判定), "proposal 有该字段且值可被前置 Spec 归一解析, 或显式为`无`"这条**可以**写成同形态的一条 check(用一个 for 循环遍历 `openspec/changes/*/proposal.md` 并调用前置 Spec 提供的归一函数)。时序上, 只要遵守本 Spec 头部"`linked-issue-normalization` 必须先 ship"的前置声明, 到本 Spec 自己 Phase B.2 时该函数应已存在——**但这个顺序约束目前只是 proposal 头部的一句文档承诺**, `phase-a-planner`/`task-planner` 里的 `depends_on` 字段(`phase-a-planner/SKILL.md:80/91`)只用于**同一个 Spec 内部** A.1→A.2→A.3 的顺序, 不是跨 Spec 依赖机制, 全仓没有查到任何机械阻止"先动手实现本 Spec 再实现前置 Spec"的东西。多容器并发场景下(本项目自己的 memory `feedback_concurrent_duplicate_audit_fetch_before_start` 记录过多次同类复发)这不是零概率。
- **额外发现(范围维度)**: `.aria/state-checks.yaml` 文件头部自己写明"项目级自定义健康检查", 全仓搜索确认**没有**任何 `state-checks.yaml` 模板/示例随 `aria/` 子模块分发(对照确有模板的 `config.template.json`); 而 §1.1 要改的 `proposal` 模板改动落在 `spec-drafter/SKILL.md`——这是**随 aria-plugin 分发给所有采用者**的文件。也独立核实了 CLAUDE.md 里提到的"标准模板 SOT" `standards/openspec/templates/proposal-minimal.md`(Level 2 模板, 全 repo README 指定的官方复制路径), 读其全文 1-30 行: 字段只有 `Level`/`Status`/`Created`, 同样**没有**"关联 Issue"字段, 且 Impact 表完全没提这个文件。
  ⇒ §1 用来论证"必须校验而非只改模板"的理由(`:75`"模板只影响新建, 且 AI 可以删……无机械回声的义务会退化")对 Aria 自己成立(有 `.aria/state-checks.yaml` 兜底), 对其余每一个 aria-plugin 采用者(CLAUDE.md 记载的 Kairos 等)**都不成立**: 它们拿到新模板字段, 却没有任何随插件分发的机制校验它有没有被填, 恰好复现了 §1 自己要防的那个退化。
- **建议修法**: Impact 表补 `standards/openspec/templates/proposal-minimal.md`(模板字段本身)一行; 对机械回声, 要么明确接受"本 Spec 的校验只覆盖 Aria 自身, 其余项目仅有模板"并记为已知限(不用"机械校验"这个不加限定的措辞掩盖覆盖边界), 要么给 `spec-drafter` 自身加一段可随插件分发的轻量自检(不依赖消费方是否配置了 `.aria/state-checks.yaml`)。

### [MINOR] §5"调 `release_gate.py --status abandoned`"省略了必需的 `--raw-track-id`, 单独这么调会被 argparse 拒绝 (回答 Q6)

- **位置**: `proposal.md:178`(§5 表格"探索性放弃"行)。
- **实读证据**: `scripts/release_gate.py:236-237` 逐字:
  ```python
  if not args.raw_track_id and not args.sweep_stale and not args.gc:
      parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")
  ```
  `--status` 的 `choices=["done", "yielded", "abandoned"]`(`:216-221`)只是修饰"释放成什么状态", 不满足"至少给一个动作"的前提。exploratory-abandon 场景明确是要释放**这一条**当前 claim, 正确调用形态是 `release_gate.py --raw-track-id "<carry-id>" --status abandoned`(还原 `--raw-track-id` 后, D6/D14/SC-14 的语义都成立, 我没有发现别的问题)。
- **问题**: proposal 在 §2 给主机制的调用形态是完整贴出的 bash 代码块(含全部必需参数), 而 §5 这一行是压缩成表格单元格的自然语言引用, 省掉了必需参数——单独按这行字面"调 `--status abandoned`"操作会在 CLI 层直接报错退出(exit 2), 不会写出预期的 `abandoned` claim。严重度低, 因为 Phase B 实现该义务时几乎必然会去读 `release_gate.py` 本体或已有的 D.2b 调用惯例, 属于文档精度问题而非设计缺陷。
- **建议修法**: §5 该行改为完整命令引用(或至少补齐 `--raw-track-id "<本轨 carry-id>"`), 与 §2 的精确度对齐。

---

## 附一: 逐题速览 (对应审计任务给定的 6 问)

| # | 问题 | 结论 | 对应 |
|---|------|------|------|
| 1 | heartbeat 改 `(container, track_id)` 照抄是否可行 | **机械改写可行**(脚手架逐行同构), 但**无人调用**是独立于"能不能抄"的更大问题 | Critical #2 |
| 2 | identity.py 新增直取 uuid 的 accessor 是否可行 | **可行, 无阻碍**——`get_container_id()`(`identity.py:191-244`)可原样复用同一套"读文件→`_parse_container_file`→regenerate→hostname 兜底"骨架, 只需把 `:222` 的 `return label if label else uuid` 换成 `return uuid`; hostname 兜底(`:242`)分支两者共享同一降级条件, 无需特殊处理。**未发现缺陷**, 建议实现时提取共享私有 helper 避免两份文件 I/O 逻辑漂移, 但这是实现建议不是 Spec 缺陷 | 见下"经核实无碍" |
| 3 | §2.4 三段传递链是否可行、是否真的不碰 `run_gate`/`_run_gate_impl` | 对这两个函数的保护**属实**, 但 Impact 表漏了必须一起改的 `lib/collision.py`, 且 `_TERMINAL` 成员描述与代码相反 | Major #1 |
| 4 | `sibling_spec_probe.py` 按描述能否实现, "各自默认分支"在 git 层面怎么做 | 范围定义(`enforced_remotes`)有实锚, 但"默认分支"解析机制未定义, 本仓实测朴素做法(本地符号引用)在第二 remote `github` 上失效 | Major #2 |
| 5 | §1 custom check 能否写成、依赖前置 Spec 代码的时序是否成立 | 能写成同形态 check; 时序**目前只是文档承诺**, 无跨 Spec 依赖的机械阻断; 且该 check 的覆盖范围只到 Aria 自己, 与面向全体采用者的模板改动范围不对等 | Major #3 |
| 6 | `release_gate.py --status abandoned` 真实 CLI 形态 | 需 `--raw-track-id <id> --status abandoned`; 单独 `--status` 不满足 argparse 的"至少一个动作"前提, 会报错退出 | Minor #1 |

## 附二: 已验证为非问题的一点

- **Q2 identity.py accessor 的可行性**(细节见上表): 逐行读完 `get_container_id()`(`:191-244`)全部三条路径(读取成功 / corrupt-then-regenerate / 写失败兜底 hostname)后, 新 accessor 与现有函数的唯一行为差异就是最终返回值选 `uuid` 还是 `label`, 不存在会导致两个函数在同一进程内产生不一致 uuid 的竞争路径(先调用的一方若触发首次生成, 后调用的一方会读到同一份已落盘文件)。判定: 按 Spec 字面实现没有阻碍。

---

**未修改任何仓库文件, 未 commit。** 本报告涉及的一次 `git symbolic-ref`/`git remote -v` 取证为只读命令, 未产生任何本地 ref 变更。
