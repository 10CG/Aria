I have verified every load-bearing claim. Producing the edit list.

## 编辑清单 — `a1-entry-claim-duplicate-work-guard` (重写版 v2) · R1-fix 综合

> **口径**: 全部行号来自本轮实读 (`/home/dev/Aria` @ `c6aa29a`, aria 子模块 `af87cae`)。凡镜头 `corrected_change` 与原修法冲突处, 已按下文「裁断」覆盖并点名。
> **被修文件**: `/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (327 行)

---

### [FIX-01] C1 — `spec-drafter` allowed-tools 行号错一行 + 表下补取证命令

**位置**: §3.1 (R1-fix 新增的「宿主能力」表, 位于 §3 内)
**原文** (fix 计划中的表格第二行): `` | `spec-drafter/SKILL.md:11` | `Read, Write, Glob, Grep, AskUserQuestion` | `Bash` | **扩容为** … | ``
**改为**: 宿主格改为 `` `spec-drafter/SKILL.md:10` ``; 并在表格正下方追加一行:

```markdown
> **本表行号口径 (可一条命令复核)**: `grep -n "^allowed-tools:" aria/skills/{phase-a-planner,spec-drafter}/SKILL.md`。frontmatter 增删行会使行号漂移 —— **SC-20 断言的是字段内容而非行号**, 行号仅供导航。
```

**依据**: 实读 `aria/skills/spec-drafter/SKILL.md` — `:9 user-invocable: true` / `:10 allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` / `:11 ---`。`phase-a-planner/SKILL.md:9` 正确。self-recurrence 与 fact-check 两镜头独立命中同一格, 我实读复验为真。C1 自己把行号声明为「可被下一席一条命令证伪」的证伪装置 —— 装置在它唯一新写的那格失灵。
**顺带核实为真 (不改)**: `phase-b-developer:10` / `phase-c-integrator:10` / `phase-d-closer:12` / `audit-engine:17` / `state-scanner:11` 均持 `Bash`; `aria-report:13 = Bash, Read, AskUserQuestion` (C1 引的先例成立); `phase-a-planner:66 skip_if has_openspec: true` 成立。

---

### [FIX-02] C6 — 「实读现签名」代码块与真实文本不符, 会抹掉三处类型标注

**位置**: §2.4 传递链「第 0 段」(R1-fix 新增)
**原文** (fix 计划): 标为「实读现签名 (`collision.py:177-181`)」的一行 `def linked_issue_overlaps(claims, own_track_id, own_linked_issue) -> "list[dict]":`
**改为**: 两个代码块逐字换成真实形态 —

现签名 (实读 `collision.py:177-181`):
```python
def linked_issue_overlaps(
    claims: "list[ClaimRecord]",
    own_track_id: str,
    own_linked_issue: Optional[str],
) -> "list[dict]":
```
改为:
```python
def linked_issue_overlaps(
    claims: "list[ClaimRecord]",
    own_track_id: str,
    own_linked_issue: Optional[str],
    *,
    include_terminal: bool = False,
) -> "list[dict]":
```
并在承重说明追加第三项: 「**既有三个形参的类型标注逐字节保留** —— `Optional` 已在模块内 import, 删标注会引入未使用导入与一次未声明的类型降级」。

**依据**: 实读 `collision.py:177-181` 为五行带完整标注。fact-check 镜头命中, 我复验为真。C6 的价值主张是「实现者无需推断、可直接落笔」, 照现文落笔即降级。

---

### [FIX-03] C4 — `unknown` 结构性无法经 `linked_issue_overlap[]` 表达 ⇒ 改走独立 additive 键 ⭐ 承重

**位置**: §2.4 表格第三行 + SC-24 + Impact 表
**原文** (fix 计划): §2.4 表格第三行诊断为「`unknown` 被 skip, 原因是 `_TERMINAL`」, 处置为「**无论 `--include-terminal` 与否都必须显出**」; SC-24 断言「该 claim **出现在** `linked_issue_overlap[]`」。
**改为** — 三处一起改, 缺一 SC-24 恒红:

(a) §2.4 表格第三行「本 Spec 处置」格全文替换为:
```markdown
`unknown` **不能**经 `linked_issue_overlap[]` 通道表达 —— **两道门都会丢它**, 且第二道与 `_TERMINAL` 无关:
① `collision.py:213` 的 `_TERMINAL` (含 `"unknown"`);
② `collision.py:215` 的 `if not getattr(c, "linked_issue", None): continue` —— `parse_claim` 的 unknown 分支 (`claim_schema.py:219-230`) 构造 sentinel 时**根本没传 `linked_issue`**, dataclass 默认 `None` (`claim_schema.py:127`) ⇒ 即便把 `unknown` 移出 `_TERMINAL`, 下一行立刻丢弃, **行为逐字节不变**。
③ 且 sentinel 的 `track_id`/`container`/`claimed_at` 全为空串 ⇒ 即使强行放行, §2.3 要求的「对方 track-id / owner-container / claimed_at」三项全是空字符串。
⇒ **处置 = 另开一条 additive 输出键**, 见下。
```

(b) §2.4 末尾新增一小段:
```markdown
**`unknown` 的独立通道 (additive, 不并入 overlap)**: `phase1_gate` 输出新增键 `unknown_schema_claims: int` —— 值 = `read_claims(repo).claims` 中 `status == "unknown"` 的条数, **不经 `linked_issue` 匹配** (它读不到)。
- **门控**: 该键**仅在传 `--include-terminal` 时**出现。A.1 模板恒带该 flag ⇒ 恒有; Phase B 两个入口都不带 ⇒ **输出逐字节不变**, 与 §非目标「不动 Phase B 入口现有认领」自洽。
- **实现落点**: 把 `phase1_gate.py:1229` 的 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`, 块内 `read_claims(repo)` 只调一次, 然后分别按 `args.linked_issue` / `args.include_terminal` 各自填键。
- **消费面措辞**: 「**未能核实**: ref 内有 N 条本读者读不懂 schema 版本的 claim (存在性已确认, 内容未知)」。**不得**并入 `linked_issue_overlap[]`, **不得**与 `done`/`abandoned` 同档。
- **已知限 (成文)**: 本轮**不给**这 N 条提供路径/身份 —— `read_claims` 的 `ReadClaimsResult` (`coordination_ref.py:119-139`) 只有 `claims/errors/ref_exists`, unknown 记录进 `claims` 时**既无 path 也不入 `errors`** (`:706-711`)。提供路径需改 `ReadClaimsResult` 字段 ⇒ 转 follow-up, 不在本 Spec。
```

(c) SC-24 全文替换:
```markdown
| **SC-24** (代码, **CLI 全链路**) | 夹具写入一份 `schema_version: "2"` 且带匹配 `linked_issue` 的 claim blob, 经 CLI 跑 (带 `--include-terminal`) | 输出含 `unknown_schema_claims >= 1`; **且 `linked_issue_overlap[]` 中不出现该条** (避免空串字段污染告警面) | 现状 (无该键) 必红; 试图经 `linked_issue_overlap[]` 输出的实现在真实 `parse_claim` 路径下**恒空**, 也必红 |
```

(d) Impact 表: `phase1_gate.py` 那一行的「变更」列追加 `; Part B1 块门控改为 or include_terminal + 新增 unknown_schema_claims 键`。**不新增** `lib/claim_schema.py` 行。

**依据 / 三镜头裁断**:
- self-recurrence 与 fact-check 独立给出同一结论 (走独立键), cross-clause 给出**第三方案** (新加 `include_unverifiable` keyword-only flag, 仍走 `linked_issue_overlap[]`) —— **驳回 cross-clause 的这一支**: 我实跑证伪了它的前提。实测 (`python3` 直调 lib):
  `parse_claim({... 'schema_version':'2', 'linked_issue':'10CG/aria-plugin#122' ...})` → `ClaimRecord(..., status='unknown', ..., linked_issue=None)`; `linked_issue_overlaps([rec],'my-track','10CG/aria-plugin#122')` → `[]`。⇒ **无论加多少 flag, 该通道恒空**, 除非同时改 `parse_claim` 保留 sentinel 的 `linked_issue` (schema 读取语义变更, blast radius 超本 Spec)。
- self-recurrence 版本要求输出 `paths` —— 我实读 `coordination_ref.py:654-713` 确认 unknown 记录的路径**不被保留**, 供路径必须改 `ReadClaimsResult`。⇒ 采 fact-check 的 count-only 版, 路径转 follow-up 并**成文声明**这一半没给 (memory `knob-granularity`: 诚实交付一半 + 说明哪半是哪半)。
- 门控条件 (`or args.include_terminal`) 与「仅在 `--include-terminal` 时出现」是我的综合裁断, 两镜头都未指定 —— 因为两者的写法都会把新键泄漏到 Phase B 输出, 违反 §非目标:272。**这是本轮新表面, 见文末。**

---

### [FIX-04] C2 — 删除 `A1_SWEEP_TTL` 72h 分档; §2.2 改写为「保护窗由 `--include-terminal` 提供」⭐ 承重, 三镜头分歧点

**位置**: §2.2 (:105-114) + D4 (:202) + SC-5/6/7 (:242-244) + Impact 表
**原文** (:107-109):
```
事故窗实测 **48–72h**, 而 `STALE_TTL` = 30min、`SWEEP_TTL` = 24h ⇒ 保护窗短于事故窗。
**处置 = heartbeat 匹配键改 `(container_id, normalized track_id)`**, 刷新**全部**匹配的 active claim。
```
(R1-fix 在此基础上加了 `A1_SWEEP_TTL` = 72h 常量 + `gc.sweep_stale_active` 按 `phase == "A.1"` 分档)

**改为** — §2.2 标题下整段替换:
```markdown
#### §2.2 保护窗 — 由 `--include-terminal` 提供, **不动 GC 路径**

原版把「保护窗」误当成**可见性**问题, 于是想去改 TTL。实读三条事实推翻该框架:

1. §2 的 A.1 调用模板**恒带** `--include-terminal` (本文 §2 模板第 4 行);
2. `linked_issue_overlaps` 体内**唯一**的 status 过滤器就是 `_TERMINAL` (`collision.py:207-233` 全文实读, 无第二处) ⇒ `include_terminal=True` 时 `abandoned` 条目**照样出现**;
3. `archive_done_claims` **只归档 `status == 'done'`** (`gc.py:146`) ⇒ 被 sweep 判死的 `abandoned` 记录**永久留在 ref 里**。

⇒ **sweep 不会让竞品 claim 从本 Spec 的消费面消失, 它只是把 status 改写了。** 保护窗不需要延长, 也不需要 heartbeat 刷新者 —— **本 Spec 不改 `gc.py` / `constants.py`, 不引入 `A1_SWEEP_TTL`**。

**真正的残余缺陷 (改写口径后浮出)**: sweep 产出的 `abandoned` 与 `release_claim_by_track` 产出的 `abandoned` 在 overlap 返回的 7 个字段上**逐字段相同** (`gc.py:396-408` vs `claim_lifecycle.py:437-449`; 返回字段见 `collision.py:222-232`, **无 `heartbeat_at`、无 `phase`**) ⇒ 消费面**无法分辨**「对方主动放弃」与「GC 超时判死」。处置见 SC-8b: **`abandoned` 一律不得渲染为放行语**。
```

**同时**:
- **D4 (:202) 整行删除** (「heartbeat 匹配键改 `(container, track_id)`」不再是本 Spec 的决策), 或改为: `| D4 | 保护窗由 `--include-terminal` 提供, 不动 heartbeat / GC | 实读: `_TERMINAL` 是 overlap 唯一 status 过滤器 + `--include-terminal` 恒带 ⇒ sweep 只改写不隐藏; 改 GC 是跨容器生产路径且零审计记录 |`
- **SC-5 / SC-6 / SC-7 (:242-244) 三行删除**;
- Impact 表**不新增** `gc.py` / `constants.py` 行; **删除**既有 `claim_lifecycle.py` 那一行 (:283) 或改为「(本轮不动 — 见 §2.2)」;
- SC-8b (R1-fix 新增) 的 `abandoned` 档措辞改为: `` `abandoned` → 「对方轨**已停止**(可能主动放弃, 也可能被 GC 超时判定) —— **未能核实**, 请人工确认」`` ; 红条件加一句「渲染成任何形式放行语 (『对方已放弃 / 可以开始』) 的实现必红」。

**依据 / 三镜头裁断**:
- **cross-clause 与 self-recurrence 正面冲突**。cross-clause 主张全删; self-recurrence 主张保留 72h 分档只改措辞; fact-check (C5) 则默认分档会落地并要求三处文档同步到它。
- **裁断: 采 cross-clause (删)。** 三条前提我逐条实读复验为真 (proposal.md:84 / collision.py:207-233 全文 / gc.py:146)。cross-clause 的推理成立: R1-fix 的 C2 用来立论的那条因果链 (「swept→abandoned→∈`_TERMINAL`→从 overlap 消失」) 被**同一批的 C6/SC-8a** 直接证伪 —— C6 亲手打开 `include_terminal` 让它不消失。为一个在本 Spec 唯一消费面上不成立的前提, 去改一条跨容器、`phase-d-closer` 每周期都在跑、零审计记录的生产 GC 路径, 是本轮最大且最不必要的新承重面。
- self-recurrence 的 (1) (SC-8b 措辞非正向) **保留并采纳** —— 它是删掉分档后仍然成立的那一半。
- self-recurrence 的 (2) (`superseded_from = "gc:sweep_stale_active"` provenance + overlap dict 增字段) **本轮不做**: 它与姊妹 Spec `linked-issue-normalization` SC-8 (`openspec/changes/linked-issue-normalization/proposal.md:112`「`linked_issue_overlaps` 签名与返回 schema **逐字段不变**」) 正面冲突。转 deferred, 见文末。
- **⚠️ 不确定项**: 删 D4/SC-5/6/7 等于把 spike S1 的产出整块移出本 Spec。见文末「需 owner 裁的不确定项 U-1」。

---

### [FIX-05] C5 — `--sweep-stale` 阈值误写是**三处**不是两处, 漏的第三处危害最大

**位置**: C5 的 blockquote ⚠️ 行 + Impact 表
**原文** (fix 计划): 「**两处**文档把阈值写错成 STALE_TTL(30min): `release_gate.py:225` 的 help 与 `state-scanner/SKILL.md:176`」
**改为**:
```markdown
⚠️ **三处**文档把 `--sweep-stale` 的阈值误写成 `STALE_TTL`(30min), 真值是 `SWEEP_TTL`(24h):
1. `aria/skills/state-scanner/scripts/release_gate.py:225` (CLI help);
2. `aria/skills/state-scanner/SKILL.md:176` (skill 概览);
3. **`aria/skills/phase-d-closer/SKILL.md:56`** —— **危害最大**: 它是 D.2b 执行者读的运行时说明, 而 `:52` 的命令每周期都在跑。
```
Impact 表相应新增/改写为一行:
`` | `skills/state-scanner/scripts/release_gate.py` + `skills/state-scanner/SKILL.md` + `skills/phase-d-closer/SKILL.md` | `--sweep-stale` TTL 措辞勘正 STALE_TTL→`SWEEP_TTL`(24h), **三处逐字节相同** | **R1/C5** | ``

**依据**: 实读 `phase-d-closer/SKILL.md:56` 逐字含 `heartbeat 超 STALE_TTL 的 active claim 标 abandoned`; 代码真值 `gc.py:341 stale_ttl_seconds: int = SWEEP_TTL` + `release_gate.py:141 sw = sweep_stale_active(repo, now=ts)` (未覆写 TTL) + `constants.py:51 SWEEP_TTL: int = 86400`。全仓 `grep -rn STALE_TTL aria/skills --include=*.md` 只有这三处 + `coordination-ref-schema.md:198` (后者是常量定义清单, 说法正确, **不改**)。fact-check 镜头命中, 我复验为真。
**注**: 因 FIX-04 删掉了 A.1 分档, C5 原 fix 中「并同步 C2 的 A.1 档」一句必须**删除**, 三处统一措辞为「heartbeat 超 `SWEEP_TTL`(24h) 的 active claim → abandoned (跨 container)」, 不含任何 phase 分档。

---

### [FIX-06] C3-a — 语料统计数字全文回灌 (12 / 129 / 8.5%), 消除同文档两套数字

**位置**: :58 / :73 / :199 / :275
**原文 → 改为** (四处):

| 行 | 原文片段 | 改为 |
|---|---|---|
| :58 | `**「关联 Issue」字段在 141 篇 proposal 语料中只有 13 篇有 —— 9%。**` | `**「关联 Issue」字段在 141 篇 proposal 语料中只有 12 篇有 —— 8.5%。**` |
| :73 | `4. **不追溯**: 存量 128 篇无字段的 proposal 不回填 (多为已归档)。` | `4. **不追溯**: 存量 **129** 篇无字段的 proposal 中, `openspec/archive/` 下的**不回填**; `openspec/changes/` 下的**一并补齐** (见 FIX-07 的作用域段)。` |
| :199 | `**S4**: 141 篇语料仅 13 篇有该字段 (9%)` | `**S4 (R1/C3 复核勘正)**: 141 篇语料仅 **12** 篇有该字段 (**8.5%**)` |
| :275 | `- **不回填**存量 128 篇无「关联 Issue」字段的 proposal。` | `- **不回填** `openspec/archive/` 下无「关联 Issue」字段的存量 proposal (**122 篇**); `openspec/changes/` 下的 7 篇在本 Spec 交付范围内补齐。` |

并在 §1.2 首次给出数字处加一句口径注:
```markdown
> **统计口径 (可一条命令复核)**: `grep -rl '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l` = **12**; `find openspec -name proposal.md | wc -l` = **141**。S4 spike 记的「13 篇」为误计 (第 13 个命中是散文提及而非字段), **spike 记录不追改**, 本 Spec 以本口径为准。
```

**依据**: 我实跑复核 —— 141 总数 / 12 有字段 (10 在 `archive/`, 2 在 `changes/`) / 129 无字段; 12÷141 = 8.51%。fact-check 镜头命中「fix 换用 12 但没指示回灌」, self-recurrence 独立指出同一处 —— 若不回灌, 落笔即在同一文档内造出 12↔13 / 128↔129 两套数字 (正是三轮不收敛的典型形状)。
**算术核对**: `archive/` 132 份 proposal − 10 有字段 = 122; `changes/` 9 − 2 = 7; 122 + 7 = 129 ✓。

---

### [FIX-07] C3-b — 「限 `changes/` ⇒ 上线即绿」是假; 作用域段整段换成实测数 + 回填 6 篇 ⭐ 承重

**位置**: §1 第 3 条末尾的作用域段 (R1-fix 新增) + Impact 表 + §非目标
**原文** (fix 计划): 「限 `changes/` 后上线当日待判对象仅 3 篇 (`linked-issue-normalization` / `phase-c-integrator-ci-path-coverage` / 本 Spec), **三篇全在本 Spec 交付范围内改到合规 ⇒ check 上线即绿**, 不产生「129 篇恒黄」。」
**改为**:
```markdown
> **作用域 (承重条款)**: check 只扫 `openspec/changes/**/proposal.md`, **不扫 `openspec/archive/`**。
>
> **实测当前作用域内共 9 份** (不是 3 份; 口径 `find openspec/changes -name proposal.md`):
>
> | proposal | 现状 | 本 Spec 处置 |
> |---|---|---|
> | `a1-entry-claim-duplicate-work-guard` (本 Spec) | 无字段 | 本 Spec 头部补 (dogfood, FIX-19) ⇒ PASS |
> | `linked-issue-normalization` | 有字段, 值 `无` (裸写) | 补 code span ⇒ PASS |
> | `aria-2.0-m6-{cost-model-telemetry,dispatch-input-delivery,e2e-resilience,release-closeout}` | **无字段 ×4** | 头部各补一行 `> **关联 Issue**: \`无\`` ⇒ PASS |
> | `aria-2.0-m7-{agent-lifecycle,fleet-aggregation}` | **无字段 ×2** | 同上 ⇒ PASS |
> | `phase-c-integrator-ci-path-coverage` | 有字段但 markdown-link 形 (`:18`), 且已 **⛔ SUPERSEDED** (`:3-5`, owner 裁定「不再修订」) | **不改** ⇒ **上线当日已知 1 条 warning** |
>
> ⇒ **上线当日 8/9 PASS + 1 条具名 warning**, 不是「即绿」, 也不是「129 篇恒黄」。这 1 条的收敛路径 = 该目录随 `phase-c-gate-path-coverage-not-applicable` 归档后自然离开作用域。
```

**同时**: Impact 表新增一行
`` | `openspec/changes/aria-2.0-m{6,7}-*/proposal.md` ×6 + `linked-issue-normalization/proposal.md` | 头部各补/修 一行 `> **关联 Issue**: \`无\`` (纯文本, 零逻辑) | **R1/C3** | ``

**依据 / 三镜头裁断**:
- 三个镜头全部命中「3 篇」为假, 我实跑复核: `openspec/changes/` 下 **9 份** proposal, 只有 2 份有字段。
- **cross-clause 主张 diff 作用域** (`git diff --name-only <base>...HEAD`) —— **驳回**: 我实读 `.aria/state-checks.yaml:3` 确认 checks 由「state-scanner Phase 1.11 串行执行」的本地 shell `command:` 块跑, **没有 PR / merge base 可用**, `<base>` 在该宿主上未定义。
- **self-recurrence 的方案 B** (按 `git log --diff-filter=A` 首次入库时间切) 在该宿主上可算, 但引入 git-history 依赖 (rename/submodule 陷阱) 且会**永久静默豁免**那 6 份在制 Spec。
- **裁断: 采方案 A (回填 6 份 + 显式声明 1 条已知 warning)** —— 6 次单行编辑、零逻辑、可当场证伪, 且不新增任何机制表面。
- **cross-clause 关于「不得无协调编辑并发轨产物」的顾虑**: 我实读 `phase-c-integrator-ci-path-coverage/proposal.md:3-11` 确认它 **⛔ SUPERSEDED** (commit `8e76d4c`), **不是并发在制轨** —— cross-clause 与 self-recurrence 在这一点上的事实断言均**不成立**, 已按实读修正 (本 Spec 不碰它)。6 份 M6/M7 是 aria-orchestrator 轨的活跃 Spec, 补一行 `无` 是纯文本、不改其语义, 但**仍属跨轨编辑** —— 见文末 U-2。

---

### [FIX-08] C3-c — 「canonical token = 第一个 inline-code span」在真实语料上抽错; 且 token 串/元素术语自相矛盾

**位置**: §1.2 提取器规则 (R1-fix 新增) 第 1/2/4/5 条 + §1 第 3 条 check 判据 + SC-13
**原文** (fix 计划要点): 第 1 条「canonical token = `**关联 Issue**:` 之后的第一个 inline-code span」; 第 2 条「token 合法值二选一: 字面 `无`, 或归一可解析的 `<org>/<repo>#<n>`」; 第 4 条「多 issue 用 `,` 分隔, 取第一个 token」; 第 5 条「`--linked-issue` 实参 = canonical token **逐字节**」。
**改为** — 四点:

(1) **提取规则改为「首个非空白 token 必须是 code span」**:
```markdown
1. **canonical token 串**: 该行 `**关联 Issue**:` 之后的**第一个非空白内容必须是 inline-code span**, 即形如 `> **关联 Issue**: \`<token 串>\` — 可选说明`。若冒号后第一个非空白内容不是 code span (含: 裸文本 / markdown 链接 / 先出现别的 code span) ⇒ 记 **`NO_TOKEN`** (不合规, warning)。
```
> **为什么必须钉「第一个非空白」而非「第一个 code span」**: 实测反例 `openspec/changes/linked-issue-normalization/proposal.md:6` —— `> **关联 Issue**: 无 (由 \`a1-entry-claim-duplicate-work-guard\` 的 post_spec R1 发现…)`, 按「第一个 code span」会抽出 `a1-entry-claim-duplicate-work-guard`。同形反例另有 3 处 (`archive/2026-07-19-…:14` / `archive/2026-07-31-…:6` / `archive/2026-07-22-…:6`, 首个 code span 均为 `` `confirmed` ``)。

(2) **术语二分, 消除第 4/5 条互斥**:
```markdown
2. 术语: code span 内的整串称 **token 串**; 按 `,` split 后每一段称 **token 元素**。
   - **token 串合法** ⟺ 逐字节等于 `无`, **或**其每个 token 元素都可被前置 Spec 的归一解析;
   - **多 issue**: token 串内用 `, ` 分隔 (实测语料 1/11 篇为真多 issue: `archive/2026-07-11-secret-guard-bash3-multiline-hardening/proposal.md:24`, 4 个 issue);
   - **`--linked-issue` 实参 = 第一个 token 元素逐字节**, 不做二次加工。
```

(3) **§1 第 3 条 check 判据同步**: 「值可被归一解析」改为「token 串按元素逐个校验」。

(4) **SC-13 期望列补多值子例** (现无红条件):
```markdown
| **SC-13** (代码) | ① 无字段 ② 字段值非 code span 起头 ③ `\`10CG/a#1, 10CG/b#2\`` ④ `\`10CG/a#1, [b](url)\`` ⑤ `\`无\`` | ①②④ → **warning**; ③⑤ → 通过 | 只校验「有没有字段」的实现在 ②④ 上必红; 只取整串解析的实现在 ③ 上必红 |
```

**依据**: self-recurrence 镜头指出 C3 的 risk 自评援引了「token 紧跟冒号」的缓解却**没写进 exact_change**, 并给出 1 个反例; 我实跑扩到 **4 个反例** (见上)。cross-clause 独立命中第 2/4/5 条术语互斥。两者不冲突, 合并采纳。

---

### [FIX-09] ⭐ NEW-01 (整合者实测新发现) — `无` 绝不可作为 `--linked-issue` 实参, 否则任意两份无关 Spec 互相误报

**位置**: §1.2 (紧接 FIX-08) + §2 模板 (:79-86) + §2.1 (:92)
**原文**: §2 模板恒写 `--linked-issue "<org>/<repo>#<n>" \`; C3 fix 第 5 条写「`--linked-issue` 实参 = canonical token 逐字节」。二者叠加 ⇒ token 为 `无` 时会传 `--linked-issue 无`。
**改为** — §2 模板下新增一段:
```markdown
> **⚠️ token 为 `无` 时: 整个 `--linked-issue` 参数必须省略, 绝不可传 `--linked-issue 无`。**
> 实测: `linked_issue_overlaps` 只在 `own_linked_issue` falsy 时短路 (`collision.py:207-208`), `"无"` 是 truthy ⇒ 两份**毫无关系**的 Spec 只要都写 `无`, 就会互相命中 overlap。实跑复现:
> ```
> linked_issue_overlaps([claimA(linked_issue='无'), claimB(linked_issue='无')], 'spec-a-uuid1', '无')
> → [{'track_id': 'spec-b-uuid2', ..., 'linked_issue': '无', ...}]   # 误报
> ```
> ⇒ **`无` 的语义是「已核实无关联」(正证据), 不是一个可参与相等比较的 token**。此时 track-id 走 §2.1 的回落形 `<spec-slug>-<container_uuid>`, 主机制对该轨**不产生输入** —— 这条已知限须写进 §6 缺口表 (见 FIX-12)。
```

**依据**: 我实跑验证 (read-only, 直调 lib), 输出见上。**三个镜头都没有报到这条** —— M3 只在 §4 探针层处理了 `无` 的归属, 没有下移到 §2 的 CLI 实参层。这是 C3 第 5 条 (`逐字节`) 与 M3 第 1.5 条 (`无 ⇒ ∅`) 之间的接缝, 属「多条 fix 互相拆台」的第二类形状。

---

### [FIX-10] M3 — 探针「同 issue」谓词对 `无` 归属未定义 (多数路径上两读相反)

**位置**: §4 (R1-fix 新增的匹配谓词 bullet) + SC-26
**原文** (fix 计划): 「1. canonical 层: …产出 `<org>/<repo>#<n>` 集合 … 2. URL 回落层 (仅探针用): canonical 层为 `NO_TOKEN` 时 … 3. 两层皆空 ⇒ 对探针不可见」
**改为** — 在第 1 与第 2 层之间插入 1.5, 并改第 2 条触发条件:
```markdown
1.5 **`无` 的归属 (承重, 勿省)**: canonical token 串逐字节等于 `无` ⇒ 该 proposal 的 issue 集合为 **空集 ∅**, 且**不触发**第 2 层 URL 回落。`无` 的语义是「已核实无关联」(正证据), 与 `NO_TOKEN` 的「读不到」(零证据) 是两回事, **不得**合并处置。∅ 与任何集合无交集 ⇒ 两份 `无` proposal **永不互相命中**。

2. **URL 回落层 (仅探针用)**: canonical 层为 `NO_TOKEN` 时 (**且仅当**; token 串为 `无` 不进本层) …
```
SC-26 增两条臂:
```markdown
| **SC-26b** | 两份 proposal 的 token 串均为 `无` | 探针判**不命中** | 把 `无` 当普通 token 参与求交的实现必红 |
| **SC-26c** | 一份 `无`、另一份 `10CG/aria-plugin#122`, 且 `无` 那份散文里含任意 issue URL | **不命中**, 且 `无` 那份**不得**进 URL 回落 | 回落触发条件写成「canonical 集合为空」而非「== `NO_TOKEN`」的实现必红 |
```
**依据**: self-recurrence 镜头。SC-26 现只用两份真实 #122 proposal 做夹具, **两种读法都能过** ⇒ 形同无断言 (memory `spec-underdetermination`)。实测语料佐证 `无` 会是多数 token (`changes/` 下补齐后 7/9 为 `无`)。

---

### [FIX-11] M1 — 姊妹 Spec SC-8 的字面禁止加 keyword-only 形参 ⇒ 这是**必需编辑**, 不是「登记」

**位置**: §0 跨 Spec 契约表 (R1-fix 新增) + Impact 表
**原文** (fix 计划): 「姊妹 SC-8 的可验语义是『既有调用方零改动』; `*, include_terminal: bool = False` 对既有 3 位置实参调用点逐字节无影响 ⇒ **该 SC 仍绿**。这是本 Spec 单方面的读法 ⇒ A.2 须交叉登记。」
**改为**:
```markdown
| `linked_issue_overlaps` 签名 | 姊妹 SC-8 (`openspec/changes/linked-issue-normalization/proposal.md:112`) **逐字**要求「签名与返回 schema **逐字段不变**」; 加 keyword-only 形参**违反其字面** (`inspect.signature` 前后不等)。「Phase B 现有调用方零改动」在姊妹 `:79` 是由「签名不变」**推出的结论**, 不是判据本身 (原文 `⇒` 明示方向) ⇒ **不能拿结论当判据**。 | **本 Spec 的合并前置 = 对姊妹 Spec 的一处必需编辑**: 其 SC-8 期望列改写为「既有 **3 个位置实参**调用点逐字节不变 + 返回 dict schema 逐字段不变; **允许 additive keyword-only 形参**」, D6 (`:92`) 同步。**该改写须随姊妹 Spec 一同 ship** —— 合并序是「姊妹先 ship」, 其 SC-8 测试会先落地并绿, 本 Spec 的 C6 再把它变红。 |
```
Impact 表新增:
`` | `openspec/changes/linked-issue-normalization/proposal.md` | SC-8 期望列 + D6 放开 additive keyword-only 形参 (**本 Spec 合并前置**) | **R1/M1** | ``

**依据**: fact-check 镜头, 我实读姊妹 `:79 / :92 / :112` 三处逐字复验为真。cross-clause 在 C4 条目下也指出 M1 「只登记了签名, 没把行为改动纳入」—— 该顾虑经 FIX-03 (unknown 走独立键 + 仅 `--include-terminal` 时出现) 后**不再成立** (Phase B 输出逐字节不变), 无需额外条款。

---

### [FIX-12] M5 — 三态扩为四态: `unknown` 的证据方向与 error/degraded **相反**, 措辞不得合并; §6 缺口表补最大一项

**位置**: §2.5 (:137-140) / M5 新增的三态表 / SC-8b / SC-10b / §6 缺口表 (:184-189)
**原文** (fix 计划): M5 三态表 + C4 + M10 的 SC-8b/SC-10b 把 `unknown` / `linked_issue_overlap_error` / `fetch_degraded` **三者措辞统一为「未能核实」**。
**改为** — (a) 三态表扩为四态:
```markdown
| 信号 | 含义 | 消费面措辞 |
|---|---|---|
| 键**缺席** | 未检测 (未传 `--linked-issue`) | 「本轮**未检测**」 |
| `linked_issue_overlap == []` | 已检测, 无碰撞 | 「无碰撞」 |
| `unknown_schema_claims > 0` | **已确认存在** N 条竞品 claim, 但本读者读不懂其 schema 版本 | 「**已检测到 N 条本读者无法解析的 claim** —— 存在性已确认、内容未知, **按存在处理**」 |
| `linked_issue_overlap_error` 非空 / `error == "fetch_degraded"` | **本轮未取到任何证据** | 「**未能核实** (本轮未取到证据), 建议重试」 |
```
(b) SC-8b / SC-10b 双臂改写: 「把『已确认存在竞品』与『本轮没取到证据』渲染成同一句的实现**必红**」。
(c) §2.3 处置分流: `unknown_schema_claims > 0` 与 overlap 非空走**同一条**请裁路径; error/degraded 走「未能核实 + 重试」路径。
(d) §6 缺口表**新增首行** (M5 的原意, 但数字与措辞按本轮实测改):
```markdown
| **本轨 token 为 `无`** (补齐后 `changes/` 下 7/9) | 无界 | **无** —— `phase1_gate.py:1229` 门控整块, 无 `--linked-issue` 则主机制零输入; §4 探针同样按 ∅ 处理 (FIX-10)。这是主机制**最大的单项缺口**, 成文而非假装覆盖 |
```

**依据**: cross-clause 镜头 (M5 条目)。我实读 `claim_schema.py:95-96` 确认 `"unknown" is a reader-only sentinel … never written by a live session` ⇒ 它一定对应一个**真实存在**的 claim 文件 ⇒ 是正证据。把正证据降格成零证据, 是 §2.5 未改动条款「零证据不得当正证据」的镜像形态。

---

### [FIX-13] M8 — SC-21 的断言形态对「塞进 YAML 列表」免疫; 且 `### B.0` 全文不存在

**位置**: SC-21 (R1-fix 新增) + §2 触发时机 (:88) + §3
**原文 (:88)**: `作为**独立标题级步骤** (仿 \`phase-b-developer\` 的 \`### B.0\`)`
**原文 (fix 计划 SC-21)**: 期望列「两者各自含独立标题级认领步骤, 锚点字面 `A.0 - REQUIRE claim`」+ 加注「取 `A.0` 与 Phase B 的 `B.0` 对称 (`phase-b-developer/SKILL.md:86`)」, 宿主套用 `test_phase_b_require_claim_present`。
**改为** — 三处:

(1) **:88 括号内引用替换**:
```
作为**独立标题级步骤** (仿 `branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim`), **不塞进现有 A.1 的 YAML 动作列表**
```
> 追加脚注: 「**注**: `phase-b-developer/SKILL.md:86` 的 `B.0 - REQUIRE claim` 是 ```` ```yaml ```` 块内的 **YAML 键、不是标题** (`:85` 是围栏起始, `:83` 才是标题 `### 步骤执行`); 该文件全文 `^#+ ` 标题里**无任何 `B.0`**。原文的『仿 `### B.0`』引用了一个不存在的锚点, 不可作为『标题级』样板。」

(2) **SC-21 期望列全文替换**:
```markdown
| **SC-21** (代码) | `phase-a-planner/SKILL.md` 与 `spec-drafter/SKILL.md` 各自的 A.1 认领步骤 | ① 断言形态必须为 `assertRegex(text, r"(?m)^#{2,4}[ \t]+A\.0 - REQUIRE claim\b")`, **且该匹配行不在 ``` 围栏内** (最省实现: 先按 ``` 切段, 只在围栏外的段跑正则); ② 步骤块内含 `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` 四个字面量; ③ 步骤块内含 `check:` + `if_missing:` (或等价的「本 session 已跑过 phase1_gate 则跳过」谓词), 措辞与 `phase-b-developer/SKILL.md:88-89` 对齐 | **裸 `assertIn` 明确不可接受** —— 子串检查对「把 `A.0 - REQUIRE claim` 原样塞进 A.1 现有 ```yaml 动作列表」这一种失败**免疫**, 而那正是 §2:88 明令禁止、§Why 引 R3/M6 论证过的原病; 两个落点都无条件调用 (一次 A.1 写两条 claim + 两次外向推送) 的实现必红 |
```

(3) **宿主与「扩它不另起文件」保留, 但写明扩法**:
```markdown
> 宿主 = `state-scanner/tests/test_coordination_default_lockin.py`, **扩它, 不另起文件**。但注意: 先例 `test_phase_b_require_claim_present` (`:53-56`) 的两条**裸 `assertIn` 是不该抄的那一半**。新增 `test_phase_a_require_claim_headed` 用上述正则形态, docstring 写明「与 `test_phase_b_require_claim_present` 的断言强度差异是有意的: B.0 的 YAML-键形态是既有欠缺, 另开 issue, 不在本 Spec 修」。
```
**同时 §3 双落点列表补分工**:
```markdown
> **两落点同时命中时谁让步**: `phase-a-planner` 是主路径 (`:63-64` 的 `A.1 - Spec 管理: skill: spec-drafter` 会主动委派); `spec-drafter` 落点只在 (a) 未经 phase-a-planner 直接调用, 或 (b) phase-a-planner 因 `skip_if: has_openspec: true` (`:66`) 未走到认领 时生效。幂等谓词 (SC-21 第 ③ 项) 保证正常委派路径上**只写一条 claim**。
```

**依据 / 两镜头合并**: self-recurrence 给断言形态 + `### B.0` 不存在的实证; cross-clause 给幂等谓词的缺失。两者**互补不冲突**, 全部采纳。我实读复验: `phase-b-developer/SKILL.md` 标题清单 (`grep -n "^#\+ "`) 无 `B.0`; 唯一 `B.0` 命中在 `:86`, 上一行 `:85` 是 ```` ```yaml ````; `branch-manager/SKILL.md:146` 确为 `### 前置: REQUIRE claim (Part A1, MUST …)`; `test_coordination_default_lockin.py:53-56` 确为裸 `assertIn`; `phase-b-developer:88-89` 确为 `check:` / `if_missing:`。

---

### [FIX-14] M2 — §5 漏了最常见的退出路径「A.1 成功并走完循环」, D.2b 匹配不到 A.1 的 claim

**位置**: §5 表格 (:176-180) + Impact 表
**原文 (:180)**: `| **D.2b 对偶** | 只有**走完循环**的轨才到 D.2b; 上面两条**不经过它**, 故各自显式 release |`
**改为** — 表格新增第四行, 并二选一钉死 (推荐 A):
```markdown
| **A.1 成功并继续走循环** | **A.1 派生的原串即本 cycle 的 carry-id, B.0 与 D.2b 逐字节复用** —— 否则 D.2b 的 `release_claim_by_track` 按 `(container, track_id)` 定位 (`claim_lifecycle.py:422-428`) **匹配不到** A.1 那条 claim, 成功轨的 A.1 claim 无任何显式释放路径 |
```
并在 §2 模板下补一句: 「本串 (`<basename>-<number>-<container_uuid>`) **即本 cycle 的 carry-id**, `phase-b-developer` B.0 (`:92`) 与 `phase-d-closer` D.2b (`:52`) 逐字节复用。」
Impact 表新增三行 (三处模板措辞同步): `skills/phase-b-developer/SKILL.md` / `skills/branch-manager/SKILL.md` / `skills/phase-d-closer/SKILL.md`。
新增 SC:
```markdown
| **SC-27** (代码) | A.1 认领 → 走完循环 → D.2b `release_gate.py --raw-track-id <A.1 原串>` 之后 | 该 A.1 claim 不再 active | 现状 (A.1 原串 ≠ carry-id ⇒ 匹配不到 ⇒ claim 悬挂到 sweep) 必红 |
```
**同时**: M2 的 `why_it_closes` 中「由 §2.2 的 72h sweep 兜底」一句**必须删除** (该分档已按 FIX-04 删除), 改为「由本行的显式 carry-id 复用兜底; sweep 只是 GC, 不是设计中的释放路径」。

**依据**: cross-clause 镜头。我实读复验: `phase-b-developer/SKILL.md:92` = `--raw-track-id "<本 cycle carry-id/Spec id>"`; `phase-d-closer/SKILL.md:52` = `--raw-track-id "<本 cycle 的 carry-id 原始串>"`, `:55` 明写两端同一原始串; `track_id.py:61-77` 归一四步 (lower / `/._`→`-` / 截断 64 / sha 回落) **不含**任何去容器段逻辑 ⇒ A.1 原串与 carry-id 归一后确为两个不同 track_id。
**方案 B (备选, 若不动 Phase B/D 三处)**: §5 该行改为「D.2b **额外**用 A.1 原串再调一次 `release_gate.py --raw-track-id "<A.1 原串>" --status done`」, 同样入 Impact。→ 见 U-3。

---

### [FIX-15] 另/CR-M1 — SC-1/SC-15 的二分谓词被 M2 打破, 换成「track-id 形态是否含 slug」

**位置**: SC-1 (:233) / SC-15 (:257) / §5「slug 改名」行 (:179)
**原文 (:233)**: `| **SC-1** | 原始版 (spec-slug ⇒ 改名孤儿) | slug 改名前后 track-id **不变** |`
**原文 (:257)**: `| **SC-15** (代码) | 无关联 issue 的回落分支改名 | release 旧 + acquire 新两步后无孤儿 |`
**改为**:
```markdown
| **SC-1** | 原始版 (spec-slug ⇒ 改名孤儿) | track-id 为 **issue 派生形** (`<basename>-<n>-<uuid>`, **不含 slug**) 的轨: slug 改名前后 track-id **不变** |
```
```markdown
| **SC-15** (代码) | track-id 为**回落形** (`<spec-slug>-<uuid>`, **含 slug**) 的轨 —— 含无关联 issue 者**与 M2 规定的同 issue 后起 Spec** —— 改名 | release 旧 + acquire 新两步后无孤儿 |
```
M2 规则末尾追加: 「后起 Spec 因此落在**含-slug 形**, **继承 SC-15 的两步改名义务**。」§5 (:179)「slug 改名」行同步用同一谓词措辞。

**依据**: cross-clause 镜头。原 fix 用「是否有关联 issue」二分, 但同批 M2 造出第三类 (**有** issue 却必须走含-slug 回落分支的后起 Spec): SC-1 谓词字面命中它们但断言为假, SC-15 场景列字面排除它们。换成「形态是否含 slug」后三处 (SC-1 / SC-15 / §5) 用同一个可机械判定的属性。

---

### [FIX-16] 另/CR-M5 — 无人值守判据「AskUserQuestion 不可用」被 C1 亲手抹平

**位置**: §2.3 的无人值守分支 (R1-fix 新增) + §3.1 表 + Impact 表 + SC
**原文** (fix 计划): `> **判据 (可机械)**: \`AskUserQuestion\` 不可用 ⇒ 走本分支`
**改为**:
```markdown
> **判据 (可机械)**: `state_scanner.coordination.unattended == true` (config-loader SOT 新增 key, type boolean, **default false**; 由 aria-runner 容器镜像 / Nomad task env 显式置 true) ⇒ 走本分支。
> **不得**以「`AskUserQuestion` 看起来没人应答」做运行期推断 —— `allowed-tools` 是随 plugin 分发的**静态 frontmatter**, Layer 2 容器加载同一份 SKILL.md, 声明面完全相同; 且 C1 已把 `AskUserQuestion` 加进 `phase-a-planner` ⇒ 两个宿主都声明持有该工具, 该谓词求值恒为「可用」, 本分支**永不进入**。
```
**同时三处配套** (缺一即互相拆台):
- Impact 表新增: `` | `skills/config-loader/SKILL.md` | 新增 `state_scanner.coordination.unattended` (boolean, default false) 登记 | **R1/CR-M5** | `` (现有那行只登记了 coordination 的 A.1 skip 语义);
- §3.1 表加一句: 「给 `phase-a-planner` 加 `AskUserQuestion` **不**在 Layer 2 新增人类参与点 (AD10) —— 该分支由 `unattended` 谓词在**调用前**短路」;
- 新增行为类 SC (并把 rule6_note 第 2 条的 fixture 清单从 3 条扩到 4 条):
```markdown
| **SC-28** (行为) | `unattended == true` 且 overlap 非空 | **零** `AskUserQuestion` 调用 + handoff 待复议段出现 `awaiting_owner` | 定向 fixture; 「照问不误」的臂可分辨 |
```

**依据**: cross-clause 镜头。我实读复验 `phase-a-planner/SKILL.md:9` 与 `spec-drafter/SKILL.md:10` 的 allowed-tools 现值, 并确认 C1 的扩容会使两者都持有 `AskUserQuestion`。config-loader 现有 `coordination.enabled` 登记在 `SKILL.md:134-137` (default true), 新 key 落同一节。

---

### [FIX-17] 另/KM — `coordination-ref-schema.md` **存在**, 条件形去掉, 改断言形并给锚点

**位置**: M1 / 另-KM 两处 exact_change + Impact 表 + new_surfaces
**原文** (fix 计划): 「`coordination-ref-schema.md` **若存在**, 否则记为不适用并说明」+ new_surfaces 记「是否存在未经实读」
**改为**: Impact 表行改为断言形 —
`` | `aria/skills/state-scanner/docs/coordination-ref-schema.md` **§3.2 (:129-140)** | 在 reader 侧 unknown 行为枚举 (现 5 条) 后追加第 6 条: unknown claim 在 A.1 消费面的可见性与措辞语义 (经独立键 `unknown_schema_claims`, 措辞「已检测到 N 条无法解析的 claim」, **不得**并入 done/abandoned 档) | **R1/KM + R1/C4** | ``
「若它不存在, 落笔时应改为记为不适用 + 说明 `claim_schema.py:16` 的引用是悬空的」整句**删除** (前提已证伪); new_surfaces 对应条目改为「已实读确认存在 (10990 bytes), 锚点 §3.2」。

**依据**: fact-check 镜头。我实读复验 `ls -la` 该文件存在 (10990 bytes, 2026-05-22); `:129-140` §3.2 逐条枚举 reader 侧 unknown 行为 5 条 (`:133` must not crash / `:134` must return status="unknown" / `:135` skipped by reconcile / `:137` never written by a live session / `:139` should emit soft_error), **通篇不涉 overlap 面** ⇒ FIX-03 新增的义务确实是对该 SOT 的语义增补, 不写进去就是新造一条无 SOT 的不变量。
**并入**: 另/KM 的 `session-handoff.md` 入 Impact 一项**原样保留** (无镜头修正)。

---

### [FIX-18] MINOR — S3 spike 的 `identity.py:244` 是「补」不是「改」, 且替换项本身也错

**位置**: §2.1 表格 `container_uuid` 行的「依据」格 (:98)
**原文** (fix 计划第 4 条): 「删去 §2.1 里的 `identity.py:244`, 换成 `:191` + `:218-222`」
**改为** — 整条改写:
```markdown
**§2.1 `container_uuid` 依据格现无任何行号 ⇒ 是「补」不是「改」** (实跑 `grep -n "244\|identity\.py" proposal.md` 唯一命中 `:284` 的 Impact 行, 无行号)。补入三处实读出处:
- `identity.py:191` (`get_container_id` 定义)
- `identity.py:218-222` (label 优先 / uuid 兜底取值)
- **`identity.py:242`** (`return _hostname()`, 对应 §2.1 正文「hostname 兜底分支」)

并在该格末尾加一句: 「(S3 spike `:72` 记『`:244` 是 hostname 兜底』为行号误记 —— 实读 `:242` 才是 `return _hostname()`, `:244` 是 `return uuid` 新生成路径。spike 记录不追改, 本 Spec 引用 S3 时以此处为准。)」
```
**依据**: fact-check 镜头。我实读复验 `identity.py:236-244`: `:242 return _hostname()` / `:244 return uuid`; `.aria/spikes/2026-08-02-S3-track-id-derivation.md:72` 逐字含「`:244` 是 hostname 兜底」。原 fix 的替换对 (`:191` + `:218-222`) 恰好把**最需要行号支撑的 hostname 兜底分支**丢掉了 —— 而 §2.1 正文 (:100) 与 Impact (:284) 都明写该分支。

---

### [FIX-19] dogfood — 本 Spec 自身补「关联 Issue」字段

**位置**: proposal.md 头部 (:3-8 的 blockquote 内, 建议放在 `> **Spec Level**: 2` 之后)
**原文**: (无该字段)
**改为**: 新增一行
```markdown
> **关联 Issue**: `无` — 本 Spec 源自 5 次并发起草事故的直接观察 (§Why), 无独立 issue 号。
```
**同时**: `openspec/changes/linked-issue-normalization/proposal.md:6` 的裸 `无` 加 code span → `> **关联 Issue**: \`无\` (由 …)` (与 FIX-08 的提取规则对齐, 与 FIX-07 的回填一并落)。
**依据**: R1 的 KM/m1 + CR/m4 dogfood 缺口。写法必须符合 FIX-08 的「冒号后第一个非空白必须是 code span」规则, 否则本 Spec 自己的 check 会判自己 warning (memory `feedback_validator_repo_drift_guard_test`)。

---

## 本轮 deferred (明确不修, 各带理由与去处)

| # | 事项 | 不修的理由 | 去处 |
|---|---|---|---|
| **D-a** | `sweep` 与自愿 `abandon` 的 **provenance 可分辨** (`superseded_from = "gc:sweep_stale_active"` 或新增 `abandoned_by`, 并在 overlap 返回 dict 增字段) | 与姊妹 Spec SC-8「返回 schema **逐字段不变**」(`linked-issue-normalization/proposal.md:112`) 正面冲突; FIX-11 已经在动姊妹 Spec 的**签名**一侧, 再动**返回 schema** 一侧会把两 Spec 的耦合面翻倍 | 本轮由 FIX-04 的 SC-8b 非正向措辞兜住 (「已停止 — 未能核实」); provenance 开独立 issue |
| **D-b** | `unknown_schema_claims` 的**路径/身份**信息 | `ReadClaimsResult` (`coordination_ref.py:119-139`) 无 path 字段, unknown 记录既不入 `errors` 也不带 path (`:706-711`) ⇒ 供路径 = 改 NamedTuple, blast radius 超本 Spec | FIX-03 已成文声明「本轮只给 count, 不给身份」; follow-up |
| **D-c** | `phase-b-developer` B.0 的 **YAML-键形态**升级为标题级 | 既有欠缺, 与本 Spec 的 A.0 落点正交; 拉平会扩大 Phase B 改动面, 撞 §非目标:272 | FIX-13 的 docstring 已写明「有意的强度差异」+ 另开 issue |
| **D-d** | `layer-l-integration.md:45` 声称的 `update_heartbeat()` **全仓不存在** | 已在 Impact 表 (:291) 覆盖该文件, 但 fix 计划未点名这一行 | 建议在该 Impact 行的「变更」列补「顺带勘正 `:45` 的 `update_heartbeat()` 悬空引用」—— 我实跑 `grep -rn update_heartbeat aria/` 只命中该文档行 |
| **D-e** | `collision.py:307` 的**第二个** `_TERMINAL = ("done", "abandoned")` (2 值, 不含 `unknown`) 与 `:210` 的 3 值版本并存 | 属 `reconcile` 侧, 与本 Spec 的 overlap 面正交; 但**两个同名局部常量语义不同**是真实的可读性陷阱 | 不在本 Spec 修; 建议记为 minor / follow-up |
| **D-f** | `owner-container` 与 claim container 段口径统一 | 原 §3 已记为 follow-up (属 standards 变更) | 保持 |

---

## 本轮引入的新表面 (未审)

1. **`unknown_schema_claims` 输出键 + `if args.linked_issue or args.include_terminal:` 门控改写** (FIX-03) —— **这是我的综合裁断, 三个镜头都没提出这个具体形态**。它改的是 `phase1_gate` 的输出契约与调用条件: `--include-terminal` 时会**多跑一次 `read_claims`** (git ls-tree + 每文件 git show)。虽然 `read_claims` 在 `_run_gate_impl:486` 已经跑过一次 (这是既有的双读, 非本轮引入), 但门控放宽后 A.1 的 `无` 路径会新增一次读。**未测其耗时**。
2. **`state_scanner.coordination.unattended` 新 config key** (FIX-16) —— 新的配置面 + 新的 Layer 1/2 env 传递腿 (memory `feedback_env_propagation_3_leg_contract`: write + HCL declare + consumer import, **缺 import 静默 fallback**)。本轮只写了 config-loader 登记, **消费侧接线未定义**。
3. **回填 6 份 M6/M7 proposal 头部** (FIX-07) —— 跨轨 (aria-orchestrator) 文档编辑, 纯文本零逻辑, 但仍是对别人在制产物的写入。
4. **对姊妹 Spec `linked-issue-normalization` 的两处编辑** (FIX-11 的 SC-8/D6 + FIX-19 的 `:6` code span) —— 姊妹 Spec 已 Draft 待 post_spec, 编辑它会改变它自己的审计基线。
5. **SC 编号扩到 SC-28** (原 19 → R1-fix 加到 ~26 → 本轮 +SC-27/28, 同时删 SC-5/6/7) —— **净变化与重编号未核**, 落笔时须逐条对号, 否则会出现 SC 编号空洞或重号 (memory `feedback_audit_trajectory_placeholder_footgun` 同族)。
6. **FIX-09 是本轮新发现的缺陷**, 未经任何席位审 —— 它同时改动 §1.2 / §2 模板 / §2.1 / §6 四处。

---

## 需 owner / 主控裁的不确定项

| # | 事项 | 我的倾向 | 为什么不由我拍板 |
|---|---|---|---|
| **U-1** ⭐ | **FIX-04 删掉 `A1_SWEEP_TTL` 分档, 连带删 D4 / SC-5 / SC-6 / SC-7 与 `claim_lifecycle.py` heartbeat-by-track 改动** —— 等于把 **spike S1 的全部产出移出本 Spec** | 倾向删 (三条前提我逐条实读为真; 保留则要为一个在本 Spec 消费面上不成立的前提, 改一条跨容器生产 GC 路径) | 三个镜头在这里**正面分歧** (cross-clause 删 / self-recurrence 留 / fact-check 假定它落地); 且 owner 为 S1 spike 付过成本, 删它是范围决策不是事实判断。**备选**: 保留 heartbeat-by-track 作为**正交既有缺陷修复**, 但必须 (a) 不再声称它是本 Spec 的保护窗, (b) 成文写明「`heartbeat()` 至今零生产调用点 (`constants.py:43-44` 自陈), 改匹配键不产生刷新者」—— 否则是 memory `feedback_paper_fix_antipattern` 的 paper fix |
| **U-2** | **FIX-07 回填 6 份 aria-orchestrator M6/M7 proposal** | 倾向回填 (6 次单行、零逻辑, 换来「上线即绿」可当场证伪) | 那 6 份属另一条在制轨 (`aria-orchestrator` feature 分支进行中), 编辑它们属跨轨动作。memory `feedback_concurrent_feature_collision_claim_before_build` + `sync≠push-auth`: 对他人在制产物的写入不能自我授权。**替代**: 不回填, 如实声明「上线当日 7 条 warning, 收敛日期 <待定>」并删掉「上线即绿」 |
| **U-3** | **FIX-14 选 A (统一 carry-id, 改 3 个 SKILL.md) 还是选 B (D.2b 额外再调一次 release)** | 倾向 A (一处定义, 三处复用; B 是在收尾处打补丁) | A 要动 `phase-b-developer` / `branch-manager` / `phase-d-closer` 三个 SKILL.md 的模板措辞 —— 与 §非目标:272「不动 Phase B 入口现有认领」**字面冲突** (虽然改的是 carry-id 取值口径不是 gate 语义)。需 owner 判这算不算「动」 |
| **U-4** | **`phase-c-integrator-ci-path-coverage` 那条已知 warning** | 倾向不改它 (owner 已裁定 SUPERSEDED「不再修订」), 只在作用域段具名声明 | 也可以改一行让它合规 (纯文本), 但那与 owner 的「不再修订」裁定字面冲突。属 Rule #10 面 |
| **U-5** | **FIX-11 要求先改姊妹 Spec 的 SC-8/D6 并随姊妹一同 ship** | 倾向照做 (否则姊妹的 SC-8 测试先落地, 本 Spec 的 C6 把它变红, 两 Spec 在时间轴上必撞) | 这是对**另一份待闸门 Spec** 的实质编辑, 会改变它的 post_spec 基线。需两 Spec 的 owner 同意 |
| **U-6** | **FIX-16 的 `unattended` key 消费侧接线本轮定不定** | 倾向本轮只登记 config key + 加 SC-28, 接线转 A.2 | 若不定, `unattended` 就是又一个「有记录无路由」的字段 (memory `fix-recurs-in-fallback`: 无人消费的诊断字段 = 静默); 若定, 会把 Layer 1/2 env 三腿契约拉进本 Spec |

---

## 原修法计划中**无镜头修正**、按原样 carry-forward 的条目 (供主控对号, 勿误删)

`M4` (进模板落 `standards/openspec/templates/proposal-minimal.md` SOT —— 我实读确认该模板现**无**该字段, 且 `spec-drafter/SKILL.md:429` 指向它, `:110`/`:134` 仍写 `standards/openspec/changes/` 属既有 Rule #5 违规, 不在本 Spec 修) · `M6` (`phase1_gate.py:1235-1237` 的 `except → []` 才是「零证据当正证据」的真实落点; 实读复验为真, 注意其措辞须按 FIX-12 的四态表走 error 档而非 unknown 档) · `M7` (§4 只扫默认分支 ⇒ in-flight 竞品不可见) · `M9` (SC-9/SC-14 的「代码」标签与实测对象错配) · `M10` 中除 SC-8b/SC-10b 外的部分 · R1 minor 中的 `release_gate.py --status abandoned` 缺 `--raw-track-id` (实读 `:236-237` 确为三选一必需项, 成立) · SC-13~19 缺「怎么会红」列 · §4 exit code 与 SC-18 不齐。