---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-23T11:40:00Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 (重写 v2 + C1/C2 落版) — qa-engineer

**verdict (body, 项目惯例)**: REVISE — 0 Critical, 但本席 R1 的 4 Major + 4 Minor **全部**仍未落地, 另加聚合报告 5 条 Major (M2–M7 中 6 条) 及 2 条 Minor 仍未落地, 外加本轮新查出 1 条 Major。(frontmatter `verdict` 受 verdict-format.md 枚举限制填 `PASS_WITH_WARNINGS` — 0 Critical + ≥1 Major 的机械映射, post_spec 本身 `blocking: false`, 语义等价「未收敛, 建议继续处理」)
**scope_ok**: true
**counts (本席)**: critical=0 major=12 minor=6

> **审计对象**: 主仓 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`。工作树 HEAD `1205ec3`；该文件相对 HEAD 有**未提交修改**（`git status --short` = `M`），内容即 Status 行自称的「rework 第 3 轮」落盘态（共 475 行）；上一个提交 `86540f2`（C1/C2 owner 裁定回填）。审计对象 = 工作树当前内容（未提交），非 `1205ec3` 提交态。
> **aria 子模块**: `cb6bd5d`（分支 `fix/issue-batch-149-151-155-134`，与 R1 时一致；#149/#151/#155 三件同批并行改动进行中，未触及本 Spec 引用的任何文件路径，非异常）。`lib/collision.py` 相关事实另核 `origin/master@ca52d1c`（v1.67.0，`linked-issue-normalization` 已合并，2026-08-23T09:14:07Z，确认早于本轮 proposal.md 落盘）。
> **方法**: (1) 逐条重跑本席 R1 报告 8 findings (F1–F8) 与聚合报告 5 Critical + 10 Major，对每条现在实读代码/文档判定 closed/still-open；(2) 对本轮新写内容（C1/C2 落版段、两处「请 owner 复议」段、事实断言逐条实读清单、Impact 表、rule6_note）做独立事实核验；(3) 已读同批次 R2 其余两席报告（`post_spec-R2-1787481000000-a1-entry-claim-rewrite-{tech-lead,backend-architect}.md`）作交叉印证，凡引用处均标注「TL/BA 独立复核一致」，凡本席独立命中且未见于另两席处标注「本席独立命中」——不代替本席核实，仅供聚合去重参考。全程只读，未修改任何仓库文件。

---

## 一、R1 finding 逐条 closed / open

### 聚合报告的 5 个 critical 簇

| 簇 | 状态 | 证据 |
|---|---|---|
| **C1** 两落点 `allowed-tools` 不支持本机制 | ✅ **CLOSED** | owner 裁 (a) 扩权已完整落版 (`:224-234`)；两条 owner 裁定原文经 `git show 86540f2` 逐字比对**确认一致**（本席独立 diff，无偏差）；Impact 表 `:421`/`:423` 两行逐字标明变更前后；实读 `aria/skills/phase-a-planner/SKILL.md:9`=`Read, Write, Glob, Grep, Task, Skill`、`spec-drafter/SKILL.md:10`=`Read, Write, Glob, Grep, AskUserQuestion`（当前仍是变更前状态，符合 Spec 阶段预期，与 Impact 表记载的目标值一致） |
| **C2** heartbeat 只换匹配键、无人调 | ✅ **CLOSED（设计面）** | owner 裁 (ii)+(iii)，具体入口钉为 `phase1_gate.py --heartbeat-only`，Impact 补两行 (`:418`)，SC-20/SC-21 是真正的 runtime-invocation 断言（本席复核 SC-20 算术：`STALE_TTL=1800` 现状下 23h 未刷新 `age_seconds(82800) > STALE_TTL(1800)` 为真 ⇒ 必红 ✅）。**残留**: (iii) 的落版理据本身被本轮新写内容证伪并正确上呈 owner 复议（非 finding，见「三」）；另见本轮新增 **R2-QE-M1**（该复议段的风险分析单向） |
| **C3** §1 字段格式对真实语料 0/13 匹配 | ❌ **STILL OPEN** | §1.3 (`:72-78`) 仍只给「候选」正则并显式承认「本 Spec 现有措辞不足以实现」，抽取规则本身留白 defer 到 A.2。**TL 席独立复核一致**（`R2-TL-C1`，empirical retest：候选正则实测在真实 13 篇语料上**只救 4/13**，`§1.2`「单一裸形」原文未随之调和，本 Spec 自身头部仍无该字段）——本席未独立重跑该项 4/13 实测，但从文本层面独立确认「留白未填」与 TL 结论方向一致，故计入 still-open；严重度本席取 **Major**（TL 评 Critical，留聚合裁定） |
| **C4** `_TERMINAL` 事实断言与代码相反 | ✅ **CLOSED（正文）** | §2.4 (`:180-182`) 订正准确：`unknown` 与 `yielded` 处置均正确，实读 `origin/master:collision.py:268` 逐字确认 | 
| **C5** D6「无任何函数支持释放别人 claim」为假 | ✅ **CLOSED** | `:172` 订正为「只有无差别 sweep，没有定向 release」，实读 `release_gate.py:225` help 文本「跨 container」逐字确认 |
| **C6** `include_terminal` 传递链漏第 0 段 | ✅ **CLOSED** | §2.4 item 0 (`:186`) 补 `linked_issue_overlaps` 增 keyword-only 形参；Impact 表新增 `lib/collision.py` 一行 (`:415`)；实读现签名三参数确认未加该形参（符合 Spec 描述的「待加」状态） |

### 聚合报告的 10 个 Major 簇

| 簇 | 状态 | 证据 |
|---|---|---|
| **M1** 两 Spec 间归一能力职责真空 | ✅ **CLOSED** | Impact 表已补 `lib/collision.py` 一行 + §2.2/§2.4 两处「与前置 Spec 的边界」讨论；`origin/master:collision.py:178` `normalize_linked_issue()` 确认为公开可引用函数 |
| **M2** §5「放弃必 release」× §2.1「id 不含 slug」互相拆台 | ❌ **STILL OPEN — 本席独立命中，TL/BA 报告均未见此项** | 全文 grep「三个方向」「连坐」「release_claim_by_track」在 §5/§2.1 上下文**零处理**。本席实读 `aria/skills/state-scanner/lib/claim_lifecycle.py:377-405`（`release_claim_by_track` docstring 逐字）：「若几个 active claim 匹配同一 (container, track_id) ... **ALL matching active claims are released**」——这是**故意设计**（为解决「同一 track 跨 session 重复认领」的另一个缺陷），但 §2.1 (`:111-124`) 的 track-id 派生公式对**同一容器同一 issue 的所有方向**（无论几个 proposal 草稿）都产出**同一** track_id（因为公式只含 `basename-number-container_uuid`，不含 spec-slug）。⇒ §5 (`:264`) 描述的场景「A.1 试三个方向弃两个」——若三个方向各自独立走 A.1 认领（各自新 session，`identity.py:252` 确认每次调用新 session_id）——会产生 3 条 active claim，**共享同一 track_id**。按 §5 的处置「判定不起该 Spec 时必须调 `release_gate.py --status abandoned`」，该调用内部走 `release_claim_by_track`（实读 `release_gate.py:122-124` 确认），**会释放全部 3 条**，包括容器想保留的那 2 个方向。**后果比 M2 原判更重**：`abandoned` 属 `_TERMINAL` 默认被跳过，被误伤方向的 claim 从此在其他容器眼中「消失」——直接复现本 Spec 自己要防的重复劳动风险，且是本 Spec §2.1 自己的设计选择导致的 |
| **M3** §4 探针「同 issue」匹配谓词全文未定义 | ❌ **STILL OPEN** | §4 (`:238-259`) 详述扫描范围/时机/fetch 代价/规模上限/exit code/盲区，唯独不说「怎么判定两份 proposal.md 谈的是同一个 issue」——未提及是否复用 `normalize_linked_issue()`/`_linked_issue_matches()`。TL 独立复核一致（`R2-TL-M4`：「全文 grep『谓词』3 命中，无一在 §4」） |
| **M4** 「进模板」只做了一半 | ❌ **STILL OPEN** | Impact 表 (`:409-432`) 全文 grep `standards/` 或 `proposal-minimal` **零命中**——`standards/openspec/templates/proposal-minimal.md`（spec-drafter 实际引用的模板 SOT，实读 `aria/skills/spec-drafter/SKILL.md:429` 确认引用路径）不在变更面，本席独立读该模板全文 (40 行) 确认**当前仍无「关联 Issue」字段**。TL (`R2-TL-M6`) / BA (`Major#3`) 均独立复核一致 |
| **M5** `phase1_gate.py` 的 `if args.linked_issue:` 门控整块 + §6 缺口表未列 | ❌ **STILL OPEN，且自相矛盾未解** | 本席实读确认门控实际在 `:1230`（非 R1 原引的 `:1229`，本 Spec 未引用此行号，故无引用误差需订正）。§2 (`:103`) 明写「该已知限须写进 §6 缺口表」，但 §6 表 (`:270-276`) 实际 4 行中**没有**这一行（无字段场景 = 9% 有字段/91% 无字段这一最大人群的空白覆盖）。TL 独立复核一致（`R2-TL-M7`：「自相矛盾加重」） |
| **M6** `except → []` 才是零证据当正证据的真实落点 | ❌ **STILL OPEN** | 本席实读确认 `except Exception as exc:` 在 `:1236`，`out["linked_issue_overlap"] = []` 在 `:1238`（非 R1 原引的 `:1235-1237`，本 Spec 未引用此区间）。§2.5 (`:196-199`) 「fetch 降级须进 `error` 契约」只覆盖 `GateResult.error`（`fetch_coordination_ref` 一条腿），结构上不覆盖 `_main()` 内这个独立的 `try/except`（`linked_issue_overlaps()` 调用本身异常时静默吞成 `[]`，不设置任何 error 标记）。SC-10 (`:368`) 未增子例覆盖此路径。TL 独立复核一致（`R2-TL-M8`） |
| **M7** §4 只扫默认分支，「各自默认分支」取法未定义 | ⚠️ **STILL OPEN（本轮新证据更重）** | §4 (`:256`) 仍只写「各自默认分支 (非全部ref)」一句，无解析方式/降级条款。**BA 本轮独立实测**（`Major#2`）在 aria 子模块内验证：`git -C aria symbolic-ref refs/remotes/origin/HEAD` 有值，但 `git -C aria symbolic-ref refs/remotes/github/HEAD` 直接 `fatal: not a symbolic ref`——即 CLAUDE.md 明文要求双推的 `github` 这个 remote，若 `sibling_spec_probe.py` 用最直观的本地符号引用读法会直接报错或返回空，且此路径无 SC 覆盖。本席未独立重跑该实测，采信 BA 的直接命令行证据 |
| **M8** (= 本席 F1) | ❌ **STILL OPEN** | 见下「本席 R1 findings」F1 |
| **M9** (= 本席 F2) | ❌ **STILL OPEN** | 见下「本席 R1 findings」F2 |
| **M10** (= 本席 F3) | ❌ **STILL OPEN** | 见下「本席 R1 findings」F3 |

### 本席 R1 report（F1–F8）逐条

| id | 摘要 | 状态 | 证据 |
|---|---|---|---|
| **F1** (=M8, MAJOR) | §3 双落点是核心杠杆，SC 零覆盖 | ❌ **STILL OPEN** | 全文 grep `spec-drafter` 无一处出现在任何 SC 行或 rule6_note 的「点名行为 (a)(b)(c)」/「建可证伪定向 fixture」条目中；三条 fixture 仍泛称「A.1」不分入口；§6 (`:273`)「一方跳过 A.1 直调 /spec-drafter — §3 双落点已覆盖」仍是**未经机械断言支撑的设计声称**，本仓已有的 `test_phase_b_require_claim_present` 双落点断言模式仍未被复用 |
| **F2** (=M9, MAJOR) | SC-9/SC-14 标「代码」，实测对象是 SKILL.md 散文 | ❌ **STILL OPEN** | SC-9 (`:367`)、SC-14 (`:377`) 标签均未变。本轮 rule6_note (`:333`) 新增「substitute = SC-9」的表述解决的是 Rule #6 benchmark 豁免归类问题，**未解决** F2 的核心问题（SC-9 唯一可核实途径仍是 SKILL.md 文本存在性，非运行时行为）；SC-14 未被任何新内容触及。TL 独立复核一致（`R2-TL-M10` 部分并入 SC-9；对 SC-14 明确「本席不重复报，QA 原判仍成立」） |
| **F3** (=M10, MAJOR) | SC-8/SC-10 把 CLI 可验证字段与消费层措辞捆绑 | ❌ **STILL OPEN** | SC-8 (`:366`)「措辞按 status 分档」、SC-10 (`:368`)「消费面渲染『未能核实』」两处均未拆分，文本逐字未变 |
| **F4** (MAJOR) | SC-13 被测对象大概率是通用 custom-check runner 而非该 check 自身解析逻辑 | ❌ **STILL OPEN** | Impact 表 (`:429`) 仍只有 `.aria/state-checks.yaml` 一行，未提出独立可测脚本方案（对照 `issue-cache-freshness` 走独立脚本 + 专属测试的既有先例）；`.aria/state-checks.yaml` 内两种既有 check 模式（独立脚本 vs 内嵌 bash）仍双双存在，F4 引用的两个先例（`issue-cache-freshness`/`silknode-contract-deferral-expiry`）本席复核仍在文件内 |
| **F5** (MINOR) | SC-19(b) 与其宿主机制（§4 探针）词汇错配 | ❌ **STILL OPEN** | SC-19(b) (`:382`) 文本逐字未变，仍用 `claim`/`track_id` 词汇混在 §4 探针语境 |
| **F6** (MINOR) | SC-13~19 整表缺「怎么会红」列 | ❌ **STILL OPEN** | `字段可得性/生命周期/探针` 表 (`:372-382`) 表头仍只有 `SC / 场景 / 期望` 三列 |
| **F7** (MINOR) | SC-11/SC-12「双臂可分辨」假设未经 spike 验证 | ❌ **STILL OPEN** | 无新增 spike 或引用；SC-11/SC-12 (`:369-370`) 文本未变 |
| **F8** (MINOR) | SC-4 标题夸大 + D6「两步人工」措辞安全阀缺专属 SC | ⚠️ **部分缓解，仍判 STILL OPEN** | SC-4 标题 (`:350`)「四个被推翻版本的红窗」仍未改；**但** §2.3 选项文案 (`:170`) 现已把「两步人工」四字直接写入选项标签本身（`「我去释放对方的 claim 后再开始 (两步人工)」`）——文案层面的巧合缓解，非通过新增 SC 达成，仍无任何 SC 钉住「实现者不得把选项文案简化成『接手』二字」这一要求。整体判定仍为 open（未通过 F8 建议的机制解决，只是运气性文本对齐） |

### 原「Minor（选列）」中经本席复核仍开的两条（来自聚合报告，非本席独占）

| 摘要 | 状态 | 证据 |
|---|---|---|
| §4 exit code 契约与 SC-18 不齐（原 CR/QA 联合发现） | ❌ **STILL OPEN** | §4 (`:257`)「非 0 仅用于探针自身失败」vs SC-18 (`:381`)「无远端 ⇒ exit 非 0」——「无远端」是否算「探针自身失败」未澄清，文本逐字未变。TL 独立复核一致（`R2-TL-m4`） |
| `layer-l-integration.md:45` 声称的 `update_heartbeat()` 全仓不存在（原 TL 发现） | ❌ **STILL OPEN，且因 C2 落版更易误导** | 本席实读 `aria/skills/state-scanner/references/layer-l-integration.md:45` 逐字确认仍写 `lib/claim_lifecycle.py::update_heartbeat()`；全仓 `grep -rn update_heartbeat` 仅此一处命中，实际函数名为 `heartbeat()`（`claim_lifecycle.py:178`）。C2 落版后 heartbeat 机制成为本 Spec 重点实现对象，A.2 实现者若依此表描述去 grep/引用 `update_heartbeat` 会直接扑空。TL 独立复核一致（`R2-TL-m5`） |

**未发现回归**：C1–C6 六项核心事实修复均保持正确，无一项从「已修」退回「未修/错误」。

---

## 二、本轮新写内容独立核验

对 C1/C2 落版段（`:137-236`）、两处「请 owner 复议」段（C2 一处 `:161`，C1「实读订正」一处 `:234`）、事实断言逐条实读清单（`:281-306`，17 条）、Impact 表新增行、rule6_note 重写段——本席对其中的 17 条「事实断言」逐条独立重新实读（未直接采信原文声称的行号/取值，全部用 `grep -n`/`git show` 独立核实），结果：

**17/17 逐条通过**，无一处虚报：`phase-a-planner/SKILL.md:9`、`spec-drafter/SKILL.md:9-10`、`collision.py`（`cb6bd5d` 与 `origin/master@ca52d1c` 两份坐标系）的 `_TERMINAL`/`linked_issue_overlaps` 签名/`if not own_linked_issue`/`if c.track_id == own_track_id`、`phase1_gate.py:1232-1233`、`claim_lifecycle.py:178/377/387-393/425`、`identity.py:191/222/242/247/252`、`GateResult.error` docstring `:210`（`fetch_degraded` 仅声明未赋值）、`constants.py:28/32/36/40-44/50/51`、`gc.py:341`（`stale_ttl_seconds: int = SWEEP_TTL`）、`release_gate.py:141/225`、`state-scanner/SKILL.md:149/176`、`layer-l-integration.md:15`、`phase-d-closer/SKILL.md:56`、`_run_gate_impl` 边界 `:335`–`:1032`、`ca52d1c` 合并时间戳 `2026-08-23T09:14:07Z` 与 `diff --stat` 文件数（1 个 test 文件）——全部逐字或逐值核对无误。**两处 owner 裁定原文** 经 `git show 86540f2` 独立 diff 比对，`§2.2`/`§3` 两段 blockquote 均**逐字一致**，确认这一轮真正修复了上一轮「整段删除换 AI 转述」的问题。

AB 套件核验：`aria-plugin-benchmarks/ab-suite/phase-a-planner.json` / `spec-drafter.json` 各 **2** eval case（本席独立 `python3 -c "json.load..."` 计数确认），`state-scanner.json` 存在且 **11** eval case；`880060d` 提交确认对 `state-scanner/SKILL.md:176` 跑过 AB，与 rule6_note 引用一致。

**事实核验层面本轮质量高，无新增事实性缺陷**——问题不在「新写的话是否属实」，而在「新写的话覆盖到的范围太窄，聚合报告的 Major 池与本席自己的 R1 findings 几乎原封不动」。

---

## 三、「请 owner 复议」段核验（非 finding，按任务指令排除，此处仅记录核验结论）

C2 (iii) 的「⚠️ 实读订正 · 请 owner 复议」段 (`:161`) 所依据的事实——`--sweep-stale` 实际阈值恒为 `SWEEP_TTL`（24h）与 `STALE_TTL` 取值无关——本席独立复核 `gc.py:341` 默认参数 `stale_ttl_seconds: int = SWEEP_TTL` 与 `release_gate.py:141` 未传覆盖值，**确认成立**。该段正确地把「改判 vs 维持 (iii)」的决定权交还 owner，未自行代裁，符合 Rule #10——**不算 finding**。

---

## 四、本轮新 findings

### 🟠 Major

#### R2-QE-M1 — §2.2「残余风险」分析单向：只讨论「活 claim 被误判 stale」方向，未讨论反方向「真死 claim 的 advisory takeover-eligible 窗口从 30min 延后到 24h」的代价

- **位置**: `proposal.md:156`（「落版后的准确效果」段，紧接同段 `:161` 的「请 owner 复议」之前）
- **evidence**: 该段枚举的「残余风险」只有一个方向——「(ii) 的 `/state-scanner` 编排层调用连续缺席超过 ~24h」导致**活跃**claim 被误判 stale。本席实读 `aria/skills/state-scanner/lib/reconcile.py:154-163`（`_is_stale()`）与其调用点 `:255/:283/:328`（`stale_takeover_eligible` 软信号，docstring 明写「caller decides whether to acquire」——即这是提示其他容器「可以接手」的唯一软信号通道）：把 `STALE_TTL` 从 30min 放宽到 24h 量级，意味着一个**真正崩溃/未优雅释放**的 claim，在被 reconcile 标记「可接手」之前的等待窗口，从 30 分钟延长到接近 24 小时——这是 (iii) 改动的**另一半代价**，与该段已充分讨论的「保护活 claim 不被误判」方向恰好相反，且直接影响 owner 对「是否仍采 (iii)」的复议判断（`:161`「请 owner 确认」紧跟在这段之后，owner 极可能只看到该段呈现的单向收益）。
- **危害**: owner 在 `:161` 复议 (iii) 时，其决策输入（`:156` 段）系统性省略了一个真实存在的代价维度；若 owner 据此维持 (iii)，是在信息不完整的情况下确认，而这正是本 Spec 全篇反复强调、且刚在同一小节里正确执行过一次（`:161` 本身）的「不得让 owner 在事实不全的基础上裁决」原则，在紧邻的上一段落里未被同等对待。
- **建可证伪定向**: 补一句「该延长同时使真正废弃的 claim 的 advisory takeover-eligible 窗口从 30min 延至 24h，此代价与「保护活 claim」方向相反，一并供 owner 复议时参考」；或在 `:161` 的复议问题里显式并列两个方向的取舍。
- **处方方向**: 补全 `:156` 段的双向风险枚举，不改变已定的 (ii)/(iii) 落版内容本身。
- **自检**: 危害是「owner 复议输入不完整」，处方是「补全同一段落缺失的另一半分析」——方向一致，判 Major（不阻断，但直接关系到一个正在等待 owner 拍板的活跃复议项的信息完整性）。

---

## scope_ok

**true。** 全部 finding 落在被审对象（`proposal.md` 本身及其对既有代码/文档的事实断言）范围内；无一条要求本 Spec 修改非目标范围内的代码；审计对象包含本轮新写的全部五处新增内容（C1/C2 落版段、两处「请 owner 复议」段、事实断言逐条实读清单、Impact 表新增行、rule6_note 重写段），均已核验。无 OUT_OF_SCOPE 项。

---

## 一句话结论

**REVISE** —— 本轮在「新写内容的事实准确性」上交出三轮以来最高质量的答卷（17/17 事实断言逐条复核无一虚报，两处 owner 裁定原文逐字恢复，C1–C6 五个 critical 簇全部真正闭环、无回归），**但**除了这五个 critical 簇之外，聚合报告的 10 条 Major 中有 6 条（M2–M7）、本席自己 R1 报告的全部 4 Major + 4 Minor（F1–F8）、以及原「Minor 选列」中的 2 条，**三轮 rework 一字未动**——其中最重的一条是本席独立发现（TL/BA 两席均未命中）：§5「探索性放弃」× §2.1「track-id 不含 slug」的组合会导致同一容器为同一 issue 尝试的多个方向共享同一 track_id，`release_gate.py --status abandoned` 内部调用的 `release_claim_by_track`（docstring 明写「ALL matching active claims are released」）在放弃一个方向时会**连坐释放全部方向**，直接复现本 Spec 自己要防止的重复劳动风险。**建议 R3 优先处理 M2（本报告新证据）与 TL 报告标记为「本轮 fix 自己引入」的新缺陷，其余六个「一字未动」的 Major 建议指定专门任务逐条处理，而非继续依赖同一执笔者在补 owner 裁定落版的同时顺带覆盖。AI 不预判裁决。**
