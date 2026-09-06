# pre_merge Completeness Gate 加 change 维度: 按被审 change 匹配报告 + 显式 not_applicable 三态 (Aria #199 / aria-plugin #161)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-06
> **Linked Issue**: `10CG/Aria#199, 10CG/aria-plugin#161`
> **Issue**: [Aria#199](https://forgejo.10cg.pub/10CG/Aria/issues/199) (2026-09-06 立案, aria-report 自动生成; triage 22288: confirmed / major / next-cycle) · [aria-plugin#161](https://forgejo.10cg.pub/10CG/aria-plugin/issues/161) (同缺陷在插件仓的记录, 标题「audit-engine pre_merge completeness gate 按文件名 glob 不按 spec_id 匹配 — 历史 spec 报告使门恒通过 (真实漏拦案例)」, open, 起草时 `forgejo GET` 复核)
> **认领**: 已于 2026-09-06T14:47Z 经 `phase1_gate.py --phase A.1 --mode advisory` 认领, track_id `pre-merge-completeness-gate-change-scope-bfe8285d`, `linked_issue_overlap=[]`, `unknown_schema_claims=0`
> **基线冻结**: aria 子模块 `origin/master` **`301641b`** (= v1.71.1); 本文所有行号对此 SHA (实读副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`, 起草时对 `execution-modes.md` / `audit-engine/SKILL.md` / `phase-c-integrator/SKILL.md` 三文件与 `git show 301641b:` 逐字 diff 为空)。主仓 `aria/` gitlink 仍指 `0545f86` (v1.70.0): 同伴容器 v1.71.1 的主仓同步 PR 未合, 本 spec 的 gitlink bump 排在其后。`git diff --stat 0545f86 301641b` 对本 spec 全部触点文件**为空** ⇒ 两 SHA 上行号一致。Phase B 在 `301641b` 起分支
> **代码落点**: `aria/skills/audit-engine/references/execution-modes.md` (§Pre-merge gate Step 3-5 + 校验失败输出) · `aria/skills/audit-engine/SKILL.md` (输入参数表 + Bash 调用块 + 配置注释) · **新增** `aria/skills/audit-engine/scripts/completeness_gate.py` + `tests/test_completeness_gate.py` · `references/report-storage.md` §向后兼容 · `references/pre-write-validation.md` 关联行 · `aria/skills/phase-c-integrator/SKILL.md` (C.2 pre_hook 传 change_id; `:157` 旧 schema 勘正) · `aria/CHANGELOG.md` + 版本引用点 · `aria-plugin-benchmarks/ab-suite/audit-engine.json` (+1 定向 eval) + `version.yaml`。Spec 落主仓 (Rule #5)
> **Rule #6 判定**: `execution-modes.md` Step 3-5 与 SKILL.md 调用块是**处方性 · 运行时指令面** (audit-engine 规程由 AI 编排执行); 固定套件 `ab-suite/audit-engine.json` v1.3.0 仅 2 evals, 全是竞品探针场景 (`grep -i "completeness\|missing_checkpoint\|allow_incomplete"` 零命中) ⇒ 结构上测不到本门 ⇒ 判据表**第三行** (rule6_note 见文末); 脚本 + schema + 勘正 = 描述性 ⇒ substitute = SC-1~SC-11 结构化测试
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类)
> **审计计划**: post_spec convergence 5 席 (config enabled) → post_planning convergence (config enabled); mid_implementation / post_implementation / pre_merge / post_closure 均 config off (白名单第一类)

---

## Why

### 症状 (issue + triage 复现 case, 起草时对 `301641b` 逐条复核)

`audit-engine` 的 pre_merge **Checkpoint Report Completeness Gate** (`execution-modes.md:23-82`, 2026-04-23 #26 落地) 判「该跑的 checkpoint 都跑了」, 但 Step 4 (`:54-61`) 的匹配模式是:

```
- {checkpoint_name}-*.md         (无 change_id 变体)
- {checkpoint_name}-*-*.md       (含 change_id 变体)
任意文件匹配 → 该 checkpoint 通过
```

两条通配都不含被审 change 的任何标识; Step 5 (`:63-65`) 只看 `missing_checkpoints` 是否为空。于是:

| case | 输入 | 实况 (起草时实读/实跑) | 判定 |
|---|---|---|---|
| case-1 (SOT 文本) | `execution-modes.md:54-61` | 与 issue 引用逐字一致; 全节不出现 `change_id` / `spec_id`; Step 3 (`:46-52`) 的排除清单 (pre_merge / post_closure / mid_post_spec) 只处理「启用但合法不产出 → 误阻」, 对「误放」零条款 | match |
| case-2 (本仓语料模拟) | 本仓 `.aria/audit-reports/` 780 文件, 假想新 change (自身零份报告) | `post_spec-*.md` 命中 **499** / `post_planning-*.md` **209** / `post_implementation-*.md` **3** (归属 `state-scanner-mechanical-t3` / `aria-secret-guard-plugin-default-orchestrator` / `audit-drift-guard`); 属于假想 change 的 **0** 份 → 按原文三者均「通过」 | match |
| issue 报告方 | 37 份他人 `post_implementation-*.md`, 被审 change `synth-honesty-gaps` Phase A-only 自身 0 份 | 门 PASS; 编排者靠人工核对报告归属才发现 PASS 无效, 改按「Phase A-only ⇒ post_implementation 不适用」独立论证放行 (**没有采信门的绿**) | 同型 |

**根因有两层**:

1. **匹配面无 change 维度**: 门问的是「目录里有没有这个 checkpoint 的任何报告」, 与被审 change 无关。项目历史越长越必然 PASS —— 与它要防的失效 (「该跑的没跑」) 同型: 零相关证据也判绿。
2. **change_id 在 pre_merge 根本没被投递**: `audit-engine/SKILL.md:49-54` 输入参数只有 `checkpoint / mode / context / agents_config`, 没有 `change_id`; `report-storage.md:18` 说 `{spec_id}` 「从 dispatch context」取, `pre-write-validation.md:14` 说 change_id「从调用方 context 读取」—— 而 phase-c-integrator 在 pre_merge 传的 `context` 是 **`PR diff (branch_name vs base)`** (`phase-c-integrator/SKILL.md:137`), 不是 spec 路径。post_spec 那条链是通的 (`phase-a-planner/SKILL.md:248` 传 `openspec/changes/{spec_id}/proposal.md`), pre_merge 这条链结构上就没有 change_id 可用。Step 4 不带 change 维度不是疏忽, 是**没有输入**。

### 起草期实读补充的事实 (issue / triage 没写, 改变修法形态)

| # | 事实 | 出处 | 含义 |
|---|---|---|---|
| F1 | 本仓 `audit.checkpoints.pre_merge = "off"` | `.aria/config.json` audit 块 (起草时 `python3 -c json.load`) | 该门在 Aria 自身**从不执行** (触发条件 `execution-modes.md:32` 仅 pre_merge)。triage 注「本仓 pre_merge 目前只会把 post_spec 纳入校验」漏了这一层; 且本仓 `post_planning = convergence`, 若开 pre_merge, Step 3 会纳入 post_spec **和 post_planning** 两项。⇒ 本 spec 的活体验证只能手动跑脚本 (SC-11), 不能靠生产 pre_merge 调用 |
| F2 | 真实文件名**不服从** `report-storage.md:8` 的 5-field schema | 本仓语料 `ls .aria/audit-reports \| sed 's/[0-9]+/N/g' \| uniq -c`: 时间戳段有 epoch ms (`1787379154696`) / ISO (`2026-05-23T0900Z`) / 纯日期 (`2026-05-23`) / 小整数 (`R4-4-…`); round 段有 `R5.5` / `R1prime` / `FINAL`; role 段有席位前缀 `A1-tech-lead`、`aggregated` / `aggregate` / `orchestrator` / `usN-mN`; `post_spec-*` 499 份中 24 份不匹配 `-R\d+-`, post_planning 2 / pre_merge 1 / mid_implementation 1 | triage 修法 1 写的 `{checkpoint_name}-*-{change_id}-*.md` 按**位置**取 spec_id 不可靠; 匹配必须是**连字符界定的子串** `-{change_id}-`, 不依赖前后段形态 (state-scanner `collectors/audit.py:62-114` 同样放弃了位置解析, 用 token 正则) |
| F3 | change_id 存在**前缀碰撞**: 语料 150 个 change_id (`openspec/changes` 7 + `archive` 144 去日期) 中 `aria-orchestrator` 是 `aria-orchestrator-divestiture` 的连字符界定前缀 (1 对) | 起草时 python 枚举 | 子串规则须加「最长匹配优先」: 语料里存在以 `{change_id}-` 开头的更长 change_id 时, 命中该更长 id 的文件**不计入**短 id |
| F4 | 旧 schema `{checkpoint}-{timestamp}.md` 无 spec_id | `report-storage.md:37` (reader 视为 R1/legacy) | 收窄后**结构上不可能**属于任何 change ⇒ 成文为「completeness gate 不计入」并在输出里计数 `excluded_legacy_count`, 不静默 |
| F5 | phase-c-integrator 已有 `not_applicable` 语义 = 「被审对象结构性不存在, 没有可等的 CI」(`phase-c-integrator/SKILL.md:252,260,299`; `path_coverage.py:8,547-549`), 且 C.2.4 步骤 6 规定 green 来源为 not_applicable 时**必须 surface 警告行** (`:265`) | 实读 | 本 spec 的 `not_applicable` 沿用同一语义边界: 只在「对象整个未产生」时产生, 且必须进 audit trail; 与 CLAUDE.md Rule #10 白名单第四类「闸门自身的结构性前提不成立」(`configured-gate-authority.md:38`) 同义, 其边界注「A.2 没做 = 合法; A.2 做了但很简单 = 不合法」(`:40`) 直接约束本 spec 的判据设计 |
| F6 | audit-engine 已有**机械化 diff 判据**: file-scope 二次过滤 `changed_files = git diff --name-only $(git merge-base HEAD <base>)`, 全部 ⊆ `audit.scope_skip_paths` ⇒ docs/ops-only (`audit-engine/SKILL.md:403-419`; `config-loader/DEFAULTS.json` 已注册 `scope_skip_paths`) | 实读 | 「diff 零触代码」的 not_applicable 判据**复用**它, 零新增 config 键 |
| F7 | 归档门 liveness 分类器只认 `SKILL.md` 内 **Bash 代码块**里的真调用为 alive, `references/*.md` 一律 prose | `state-scanner/scripts/lib/spec_complete.py:924-930` | 新脚本的调用行必须同时落在 SKILL.md 的 fenced bash 块 (sibling_spec_probe 先例 `audit-engine/SKILL.md:123-125`), 否则 D.2 判 dead-code |
| F8 | `.aria/config.template.json` **无 `audit` 块**; `config-loader/DEFAULTS.json` 的 audit 键集不含 `allow_incomplete_checkpoints` / `allow_dangling_change_ids` (仅 `audit-engine/SKILL.md:381-388` 文档化) | 实读 | 既有注册面缺口, **本 spec 不新增 config 键**以免扩大它; 缺口记 Phase D 待办 |

### 候选方案与否决理由

| 方案 | 内容 | 裁决 |
|---|---|---|
| A · 只改散文 (Step 4 通配换成 `{checkpoint}-*-{change_id}-*.md`) | issue 修法 1 的最小形态 | **否决**: (1) 仍是纯散文, 无法写 hermetic 红转绿测试, Rule #6 substitute 不成立; (2) F2 证明位置通配对真实语料不可靠; (3) 没解决根因 2 (change_id 在 pre_merge 无输入), 编排者仍要「自己猜」change_id |
| B · 机械执行器 + 三态 + 显式 change 作用域 (**本 spec**) | 新增 `completeness_gate.py` 实现 Step 3-5 (stdlib, 镜像 `sibling_spec_probe.py` 形态: stdout JSON 契约 + exit code + 消费方 fail-closed 义务); audit-engine 输入加 `change_id`; per (checkpoint, change_id) 三态 present / missing / not_applicable; not_applicable 只由机械结构事实产生 | **采用**: 修法 1 + 2 组合, 判据可测、可证伪; 修法 3 的「下界」在按 change 收窄后天然 = 「≥1 份属于本 change」 |
| C · B + 可配置下界 N (`audit.completeness_gate.min_own_reports`) | issue 修法 3 参数化 | **暂不做**: 需要新 config 键 (F8 注册面缺口会扩大); N>1 的语义不清 (一轮 convergence 5 席就是 5 份, 「份数」不是「轮数」); 留 待 owner 复议 #3 |
| D · 改用报告 frontmatter `context:` 字段做归属 | 78 份报告有 `spec_id:`/`change_id:` 行, `context:` 形态 8+ 种 (路径 / 裸 id 混用) | **否决**: 要打开每个文件读 frontmatter 且形态不统一; 文件名是 writer 侧唯一契约 (`report-storage.md:39`), 归属判定以文件名为准 |

## What

### 1. 新增 `skills/audit-engine/scripts/completeness_gate.py` (Step 3-5 的机械执行器)

**调用** (SKILL.md fenced bash 块 + execution-modes.md 各一份, 同字面):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/completeness_gate.py" \
  --repo-path "<repo root>" --base "<main_branch>" \
  [--change-id <id> ...] [--no-spec]
```

- `--repo-path`: 仓根 (不假定 cwd; config 读 `<repo>/.aria/config.json` 的 `audit.checkpoints` / `audit.allow_incomplete_checkpoints` / `audit.scope_skip_paths`, 缺省值与 DEFAULTS.json / SKILL.md 文档一致)。
- `--base`: 主干真实名 (本项目 `master`), 供 diff; **不提供缺省 `main`** (#137 教训, `phase-c-integrator/SKILL.md:253`)。
- `--change-id` (可重复): 显式作用域; `--no-spec`: Level 1 声明 (见 1.1 S3)。

#### 1.1 change 作用域解析 (S1 → S4, first-match)

| 步 | 条件 | 结果 |
|---|---|---|
| S1 | `--change-id` 给出 | 每个 id 必须有锚点: `openspec/changes/{id}/proposal.md` 或 `openspec/archive/*-{id}/proposal.md` (复用 `pre-write-validation.md:20-26` 锚点链, 逐字目录名); 任一无锚 → `error_kind=change_id_unanchored`, exit 2 (拼写错不能变成「零报告 → missing」的假红, 也不能变成假绿) |
| S2 | 无显式 id | 从 `git diff --name-only $(git merge-base HEAD <base>)` (与 `audit-engine/SKILL.md:406` 同命令) 取路径前缀 `openspec/changes/<id>/` 的去重 id 集; 非空 → 作用域, `scope_source=diff` |
| S3 | S2 为空且 `--no-spec` | 机械交叉核验: diff **不触** `openspec/changes/**` (触了即与声明矛盾 → `error_kind=no_spec_contradicted`, exit 2); 通过 → 全部纳入校验的 checkpoint 记 `not_applicable(reason=level1-no-spec)` (Level 1 无 spec ⇒ 报告文件名无 spec_id 可写, `pre-write-validation.md:28-30` 会拒绝写盘 ⇒ 对象结构性不存在), `scope_source=no_spec`; audit trail 必须留 `[INFO]` 行 (见 1.4) |
| S4 | 其余 | `error_kind=change_scope_unresolved`, exit 2, 文案给三个 fix: 传 `--change-id` / 在分支里带上 change 目录变更 / Level 1 加 `--no-spec`。**不放行** (零证据不当正证据) |

`allow_incomplete_checkpoints=true` 时 S4 / missing 均降为 `verdict=bypassed` + `[WARN] incomplete checkpoint gate bypassed by config: ...` (保留 `execution-modes.md:42-44,82` 既有语义), S1/S3 的 `error` 不被豁免 (输入矛盾不是「不完整」)。

#### 1.2 报告归属匹配规则 (改前 → 改后)

改前 (`:57-60`): `{checkpoint_name}-*.md` 或 `{checkpoint_name}-*-*.md` 任意命中 → 通过。

改后, 文件 `f` 归属 `(checkpoint, change_id)` 当且仅当**全部**成立:

1. `f.startswith(f"{checkpoint}-")` 且 `f.endswith(".md")`;
2. `f` 含子串 `f"-{change_id}-"` (**逐字**, 大小写敏感, 不做归一化 —— `openspec/changes/<id>` 目录名就是契约, 写侧 `report-storage.md:18` 也逐字取);
3. **最长匹配优先** (F3): 令 `C` = `openspec/changes/*` ∪ `openspec/archive/*` (去 `YYYY-MM-DD-` 前缀) 的 id 集; 若存在 `c' ∈ C`, `c' != change_id`, `c'.startswith(change_id + "-")` 且 `f` 含 `f"-{c'}-"`, 则 `f` **不**归属 `change_id`。

不要求 `-R\d+-` 段, 不解析时间戳与 role (F2: 位置不可信)。旧 schema `{checkpoint}-{timestamp}.md` 因无 change_id 段自然不命中 (F4), 计入 `excluded_legacy_count` (定义: 以 `{checkpoint}-` 开头但不含任何 `-{c}-`, `c ∈ C`)。

#### 1.3 per (checkpoint, change_id) 三态 (改前: 二态 通过 / missing)

Step 3 枚举 (`:46-52`) 不变 + 一条候选追加 (待 owner 复议 #1)。对每个纳入的 checkpoint × 作用域内每个 change_id:

| 状态 | 判据 (按序 first-match; 全部是机械结构事实, 无 AI 价值判断) |
|---|---|
| `present` | 1.2 规则命中 ≥ 1 份 |
| `not_applicable` | (a) `scope_source=no_spec` (S3); 或 (b) checkpoint ∈ diff 类 {`mid_implementation`, `post_implementation`} (`audit-engine/SKILL.md:105` 的归类) **且** diff 非空 **且** 全部变更文件 ⊆ `audit.scope_skip_paths` (F6 同一匹配语义: 目录项 `startswith`, 后缀项 `endswith`) → reason `no-auditable-code-in-diff`; 或 (c) checkpoint = `post_planning` 且 `openspec/changes/{id}/` 下 `tasks.md` 与 `detailed-tasks.yaml` **都不存在** (归档态取 `archive/*-{id}/`) → reason `no-a2-artifact` (Rule #10 `:38` 的原例) |
| `missing` | 其余 (含 diff 为空: `SKILL.md:410` 防 vacuous-true 同款, 空集不放行) |

`post_spec` 无 not_applicable 通道 (有 change_id 即有 proposal, 对象必存在)。「做了但很简单」(如 tasks.md 只有 3 行) 恒 `present`/`missing`, 不进 not_applicable (`configured-gate-authority.md:40`)。

#### 1.4 路由 + stdout 契约 (改前: `:63-65` 二路由 + `:70-80` 单一 ERROR 模板)

- 任一 `missing` → `verdict=fail`, exit **1**; 全部 `present`/`not_applicable` → `verdict=pass`, exit 0; 豁免 → `verdict=bypassed`, exit 0; 输入/环境错 → `verdict=error`, exit **2**。
- stdout 恰一个 JSON (`schema_version "1"`, `gate "completeness_gate"`): `verdict` / `error_kind` (str|null, 封闭集 `change_id_unanchored` / `no_spec_contradicted` / `change_scope_unresolved` / `git_failed` / `config_unreadable`) / `scope_source` (`explicit`|`diff`|`no_spec`|null) / `change_ids` [] / `checked_checkpoints` [] / `results` [{`checkpoint`, `change_id`, `status`, `reason`, `matched` [文件名], `matched_count`}] / `excluded_legacy_count` / `bypassed` bool / `elapsed_ms`。`results` **恒为 list**, 消费方不得从 `matched == []` 推断 (与 `execution-modes.md:185` 探针条款同构)。
- **消费方 fail-closed 义务** (写进 execution-modes.md): exit≠0 或 stdout 非 JSON 或 `schema_version` 未知 ⇒ 按 `fail` 处置 (拒绝执行 pre_merge 审计, 输出 ERROR), 不得按 PASS。
- 三态各有 audit trail 行 (取代 `:70-80` 单模板):
  - missing: `ERROR: pre_merge audit 前序 checkpoint 报告缺失: {cp}@{change_id} 配置 "{mode}" 但未找到 .aria/audit-reports/{cp}-*-{change_id}-*.md (legacy 不计入: N)` + Fix 三项 (补跑 / 改 off / allow_incomplete);
  - not_applicable: `[INFO] completeness gate: {cp}@{change_id} not_applicable ({reason}); 依据 = <机械事实: diff N 文件全部 ⊆ scope_skip_paths | 无 tasks.md/detailed-tasks.yaml | --no-spec 且 diff 不触 openspec/changes/>` — **必须 surface**, 不得折叠进「校验通过」;
  - present: `[OK] {cp}@{change_id}: N 份` (逐行, 使「通过」可核对归属)。
- 一个 PR 含多个 change (S1 多值 / S2 多 id): 逐 (checkpoint, change_id) 评估, **全部**非 missing 才 pass; ERROR 逐对列出。

### 2. audit-engine 接线 (SKILL.md)

- `## 输入参数` 表 (`:49-54`) additive 加 `change_id` (string | list, 否, 「被审 change 的 openspec 目录名; pre_merge 必传, 缺失时脚本走 S2-S4」)。
- `## 执行流程` (`:75-81`) 第 (2) 阶段描述改为「经 `completeness_gate.py` 机械执行, 三态 + fail-closed」; **新增 fenced bash 调用块** (F7, 与 `:123-125` 探针块并列)。
- `## 配置依赖` (`:385-388`) `allow_incomplete_checkpoints` 注释补「豁免 missing / scope_unresolved, 不豁免输入矛盾」。
- `execution-modes.md` §Pre-merge (`:23-82`): 互补说明 (`:25-30`) 补一句「#26 自本 spec 起带 change 维度」; Step 3 保留; Step 4-5 改为调用行 + 1.2 规则 + 1.3 三态表 + 1.4 契约; `:68-80` 校验失败输出改三态模板。

### 3. phase-c-integrator (调用方)

- `SKILL.md:133-137` pre_hook 步骤 4 追加 `- change_id: 本 cycle 的 spec 目录名 (来自 A.1 spec 路径 / claim track 的 spec dir; Level 1 传 no_spec=true)`; 步骤 5 前插「4.5 completeness gate 三态处置: fail → 阻塞并输出 ERROR; not_applicable → workflow report 必带 `[INFO]` 行」(镜像 `:265` 的 surface 义务写法)。
- `:157` `audit_report: ".aria/audit-reports/pre_merge-{timestamp}.md"` 是旧 schema 残留 → 勘正为 `report-storage.md` 的 5-field 形态 (描述性, 顺手)。

### 4. 文档同步面 (Rule #3)

| 文件 | 位置 (@301641b) | 改动 |
|---|---|---|
| `audit-engine/references/execution-modes.md` | `:23-82` | §2 所述; 删除 `{checkpoint_name}-*.md` 两行通配 |
| `audit-engine/SKILL.md` | `:49-54` / `:75-81` / `:385-388` / `:427-433` 相关文档 | 输入参数 + 调用块 + 配置注释 + 相关文档加 `completeness_gate.py` 契约指针 |
| `audit-engine/references/report-storage.md` | `:34-39` §向后兼容 | 追加「completeness gate 归属匹配只认含 `-{spec_id}-` 的文件; 旧 schema 不计入, 以 `excluded_legacy_count` 显影」 |
| `audit-engine/references/pre-write-validation.md` | `:3` 关联行 | #26 互补描述补 change 维度 |
| `phase-c-integrator/SKILL.md` | `:133-137` / `:157` | §3 |
| `aria/CHANGELOG.md` + 版本引用点 | — | PATCH **v1.71.2** (bump 前 `ls-remote --tags` + 读同伴 handoff `<vNEXT>`, memory 并行发版撞号); 主仓 14 版本字符串点 + gitlink (Aria#177 口径) |
| `aria-plugin-benchmarks/ab-suite/audit-engine.json` + `version.yaml` | evals[] / changelog | 新 eval id 3 (定向, descriptive 形态与 id 1/2 一致) + `version` 1.4.0 → 1.5.0 |

### 5. 向后兼容 (消费方 grep, 起草时全 skill 树 + 主仓)

- `allow_incomplete_checkpoints` / `missing_checkpoint` / `Completeness Gate` 的消费方: 仅 `execution-modes.md` / `audit-engine/SKILL.md` / `pre-write-validation.md` / `CHANGELOG.md:3020` (历史条目) — 全 skill 树 `--include=*.py --include=*.json --include=*.yaml` **零代码消费方**; 主仓外仅 `ab-results/2026-04-23-v1.16.2-patch/` 历史 benchmark (不动)。
- 文件名 schema 消费方: `state-scanner/scripts/collectors/audit.py:52,62-114` (只挑 `-aggregated.md`/`-aggregate.md` 候选 + token 正则解析时间戳) 与 `aria-dashboard/references/parse-rules.md:79-103` (glob `*.md` + 文件名前缀 fallback checkpoint) — 本 spec **只读**文件名, 不改 writer schema, 两者零影响。
- config 键: 零新增; 复用 `audit.scope_skip_paths` (DEFAULTS.json 已注册) / `audit.checkpoints` / `audit.allow_incomplete_checkpoints`。
- audit-engine 输入 `change_id` additive 可选; 其它 checkpoint 调用方 (phase-a-planner / task-planner / phase-b-developer / phase-d-closer) 不受影响 (门仅 pre_merge 触发, `execution-modes.md:32`)。
- 行为变化面: 只有 `audit.enabled=true ∧ checkpoints.pre_merge != off` 的采用方 (本仓不在其中, F1)。对这些采用方, 曾经的假绿会变成 `missing` 阻断 —— 这是修复本身; 迁移文案写进 CHANGELOG (「若历史 change 报告用旧 schema, 需补跑或临时 allow_incomplete」)。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 门的 PASS 与被审 change 相关: 其他 change 的报告不再构成证据; 「缺失」与「不适用」可分辨且各有 audit trail 行; change_id 在 pre_merge 有了输入通道; 规程可测 (hermetic 红转绿) |
| **Risk** | R-a 采用方历史 change 报告为旧 schema → 收窄后转 missing (假红形态)。缓解: `excluded_legacy_count` 显影 + CHANGELOG 迁移文案 + `allow_incomplete_checkpoints` 既有豁免 |
| **Risk** | R-b `--no-spec` 是调用方声明, 交叉核验只到「diff 不触 openspec/changes/」; Level 2 PR 若 proposal 早已在 master 且分支不碰 change 目录, 声明 `--no-spec` 可绕过。缓解: 声明进 audit trail (`scope_source=no_spec` + `[INFO]` 行) 可事后核对; 更强核验 待 owner 复议 #2 |
| **Risk** | R-c `post_brainstorm` / `mid_implementation` 为条件性产物, 采用方若启用且本 change 未触发, 新规则下转 missing (旧规则被他人报告掩盖)。缓解: 待 owner 复议 #1 (Step 3 排除 post_brainstorm); mid_implementation 走 1.3(b) |
| **Risk** | R-d 脚本引入 subprocess (git diff / merge-base) — 与 file-scope 过滤同命令, 失败落 `git_failed` exit 2 (fail-closed), 不 crash |

## Tasks

- [ ] TDD RED: `tests/test_completeness_gate.py` 先写 SC-1~SC-10 (含 issue case-1 / 本仓 case-2 两条 hermetic 复现), baseline 全红
- [ ] 实现 `scripts/completeness_gate.py` (stdlib only; 作用域 S1-S4 / 匹配规则 / 三态 / stdout 契约 / exit code)
- [ ] 改写 `execution-modes.md` §Pre-merge Step 3-5 + 三态输出模板 + 消费方 fail-closed 义务
- [ ] audit-engine SKILL.md: 输入参数 `change_id` + fenced bash 调用块 + 配置注释 + 相关文档指针
- [ ] phase-c-integrator SKILL.md: pre_hook 传 change_id + 4.5 三态处置 + `:157` 勘正
- [ ] report-storage.md §向后兼容 + pre-write-validation.md 关联行
- [ ] AB: audit-engine.json 新增定向 eval id 3 + version.yaml; 经 `/skill-creator` 真跑一次, 结果落 `ab-results/<date>-pre-merge-completeness-gate-change-scope/`; 套件缺口 issue (aria-plugin)
- [ ] 活体 dogfood: 在本仓对本 spec 自身与一个假想 id 各跑一次脚本 (SC-11), 证据抄进 handoff
- [ ] 版本 v1.71.2: aria 5 文件 + 主仓版本点 + gitlink (排在同伴 v1.71.1 主仓同步之后); 归档门 (SC-12)
- [ ] Phase D: #199 / aria-plugin#161 回帖 + 关闭; F8 config 注册面缺口立 issue; 复议项结论回写本 spec

## Success Criteria (可证伪; 每条自问「机制没实现会红吗」)

| SC | 断言 | 核验 |
|---|---|---|
| SC-1 | **hermetic case-1 (issue 复现)**: tmp 仓 (`git init` + 一次 commit 建 `master`, feature 分支只改 `openspec/changes/x/tasks.md` + `src/a.py`), config `post_implementation=convergence`, 目录放 37 份 `post_implementation-R1-<ts>-other-{i}-code-reviewer.md` + 4 份 `post_spec-…-x-…`, `--change-id x` → `results` 含 `{post_implementation, x, missing}`, `verdict=fail`, exit 1, stderr/stdout 文案含 `post_implementation@x`。反事实: 把规则退回 `{checkpoint}-*.md` 通配 → 判 present → 红 | `test_completeness_gate.py::test_issue_case1_other_change_reports_do_not_count` |
| SC-2 | **hermetic case-2 (本仓文件名形态)**: 用起草时冻结的 40 个真实文件名形态 (含 `R5.5` / `R1prime` / `FINAL` / `A1-` 席位前缀 / epoch / ISO / 纯日期 / `usN-mN`) 造空文件; `--change-id pre-merge-gate-no-run-for-branch` → post_spec `matched_count` = 冻结清单中含 `-pre-merge-gate-no-run-for-branch-` 的份数 (逐字等值, 非 ≥1), 且不含任何其它 id 的文件; 假想 id → missing。反事实: 位置解析 (按第 4 段取 spec_id) 在 `A1-` 与 `R5.5` 形态上少计 → 红 | 同文件 `::test_real_corpus_shapes_token_bounded_match` |
| SC-3 | 最长匹配 (F3): id 集 {`aria-orchestrator`, `aria-orchestrator-divestiture`}, 只有后者的报告在场 → 前者 `missing`; 两者各有报告 → 各 `present` 且 `matched` 互不交叉 | `::test_longest_change_id_wins` |
| SC-4 | 旧 schema `post_spec-2026-04-11T0530Z.md` 与 `post_planning-2026-04-11T0530Z.md` 在场 → 不计入任何 change, `excluded_legacy_count == 2` | `::test_legacy_schema_excluded_and_counted` |
| SC-5 | not_applicable (b): diff 仅 `docs/x.md` + `openspec/changes/x/proposal.md` (⊆ DEFAULTS `scope_skip_paths`) → `post_implementation@x` = `not_applicable/no-auditable-code-in-diff`, `verdict=pass`, stdout 文案含 `[INFO]` 与 `not_applicable`; 反事实: diff 加 `src/a.py` → `missing` + fail; diff 为空 → `missing` (空集不放行) | `::test_docs_only_diff_not_applicable` / `::test_empty_diff_is_missing` |
| SC-6 | not_applicable (c): `post_planning=convergence`, change 目录仅 proposal.md → `not_applicable/no-a2-artifact`; 放一份 3 行 `tasks.md` → `missing` (「做了但简单」不豁免) | `::test_post_planning_no_a2_artifact` |
| SC-7 | 作用域: 无 `--change-id`、diff 触 `openspec/changes/{a,b}/` → `scope_source=diff`, `change_ids=[a,b]`, 逐对评估, `b` 缺一项即 fail; 都不触且无 `--no-spec` → exit 2 `change_scope_unresolved`; `--no-spec` 且 diff 触 change 目录 → exit 2 `no_spec_contradicted`; `--no-spec` 合法 → 全部 `not_applicable/level1-no-spec` + `scope_source=no_spec`; `--change-id typo` → exit 2 `change_id_unanchored` (归档态 `archive/2026-01-01-x/` 也算锚) | `::test_scope_resolution_matrix` |
| SC-8 | Step 3 枚举: config `{post_spec: convergence, post_planning: on, mid_post_spec: convergence, post_closure: convergence, pre_merge: challenge, post_implementation: off}` → `checked_checkpoints == [post_spec, post_planning]` (字符串 `on` 纳入, `off` 与三个排除项不纳入) | `::test_step3_enumeration` |
| SC-9 | 豁免: `allow_incomplete_checkpoints=true` + 一项 missing → `verdict=bypassed`, exit 0, 文案含 `[WARN] incomplete checkpoint gate bypassed by config: missing=`; 同旗标下 `change_id_unanchored` 仍 exit 2 | `::test_bypass_semantics` |
| SC-10 | 契约: 四种 verdict 下 stdout 均可 `json.loads`, 顶层键集逐字 = 1.4 列表, `results` 恒 list; `--base` 缺失 → argparse exit 2; 坏 config JSON → `config_unreadable` exit 2 | `::test_stdout_contract` |
| SC-11 | **活体**: 在本仓 (post_spec 审计 CONVERGED 后) `--change-id pre-merge-completeness-gate-change-scope --base master` → post_spec `present`(≥5) 且 post_planning `present` 或 `not_applicable/no-a2-artifact` (视 A.2 是否已产出); 假想 id `zz-not-a-change` → exit 2 `change_id_unanchored`; 输出抄进 handoff。此为手动 dogfood (F1: 本仓 pre_merge off, 生产不会调) | 命令 + handoff 证据 |
| SC-12 | 既有测试全绿: `cd aria/skills/audit-engine/tests && python3 -m unittest discover -s . -p 'test_*.py' -v`; 跨 skill 消费方 `cd aria/skills/state-scanner/tests && python3 -m unittest discover -s . -p 'test_*.py'` (collectors/audit.py 语料测试) 与 `aria/skills/phase-c-integrator/tests` 同命令 — 三者 0 failure; 归档门对本 spec `spec_complete.py` 判 `completeness_gate.py` alive (SKILL.md bash 块, F7), 无 dead-code block | 命令 |
| SC-13 | 文档机检: `grep -c '{checkpoint_name}-\*\.md' execution-modes.md` = 0; `grep -c 'completeness_gate.py' audit-engine/SKILL.md` ≥ 1 且命中行在 ```` ```bash ```` 块内; `grep -c 'change_id' phase-c-integrator/SKILL.md` 较基线 +≥1 且 `:157` 不再含 `pre_merge-{timestamp}.md`; `grep -c '不计入' report-storage.md` ≥ 1; 三份文件的调用串逐字相同 (`diff <(grep -o 'completeness_gate.py.*' SKILL.md) <(grep -o … execution-modes.md)`) | grep |
| SC-14 | Rule #6 第三行三义务: eval id 3 登记进 `audit-engine.json` (descriptive 形态: 给定目录清单 + config + change_id, 要求写出调用命令行、三态逐对结果、`[INFO]`/ERROR 措辞; expectations 含「不得把其它 change 的报告当证据」与「not_applicable 必须 surface」) + `version.yaml` 1.5.0; 真跑一次结果落 `ab-results/`; 回退本 spec 后该 eval 的 with 臂应转差 (可证伪实证写进 ab-results README); 套件缺口 issue 号写回本 spec | 文件 + issue |

## rule6_note (Rule #6 — 判据表第三行, SOT `standards/conventions/skill-benchmark-exemption.md` §2-§3)

- **处方性 · 运行时指令面**: `execution-modes.md` §Pre-merge Step 3-5 + 三态模板 + 消费方 fail-closed 义务; `audit-engine/SKILL.md` 调用块与 `change_id` 参数; `phase-c-integrator/SKILL.md` pre_hook 4/4.5。**套件覆盖外**: `ab-suite/audit-engine.json` v1.3.0 的 2 evals 全是 per-round 竞品探针场景 (id 1 sibling_found 渲染 / id 2 not_established 措辞), 无一进入 pre_merge gate; 对它跑 AB = 测量剧场。
- **三义务**: (1) 点名行为 — A. 编排者在 pre_merge 入口用**被审 change 的作用域**调用 `completeness_gate.py` 并按三态路由, 不再把「目录里有同 checkpoint 报告」当通过; B. `not_applicable` 必须以 `[INFO]` 行 surface 其机械依据, 不得折叠进「校验通过」; (2) 定向 fixture — eval id 3 (SC-14), 可证伪: 回退 SOT 后 with 臂对 A/B 两 expectation 应失分; (3) 套件缺口 — aria-plugin 立 issue「audit-engine AB 套件零覆盖 pre_merge completeness gate」(Phase D 任务; `version.yaml` 1.4.0 先例「随 eval 闭合不另开」不沿用 — SOT §3 第 3 条要求成文缺口)。
- **描述性 / 纯代码** (脚本 / 测试 / report-storage 注 / `:157` 勘正 / CHANGELOG): substitute = SC-1~SC-10 + SC-13。`description` 字段零变动。

## 待 owner 复议

1. **Step 3 是否追加排除 `post_brainstorm`** (R-c): 它与 `mid_post_spec` 同为条件性产物 (brainstorm 是 A.0.5 可选, `audit-engine/SKILL.md:60`), 且其产物 (`docs/decisions/DEC-*` / `.aria/brainstorm-*`) 与 change_id 无机械关联。**推荐默认: 追加排除**, 理由与 `:51-52` #79 条款同构 (「启用即会误阻」)。不采纳则 SC-8 的排除集少一项。
2. **`--no-spec` 交叉核验强度** (R-b): 现设计 = 「diff 不触 `openspec/changes/**`」。可选加固: 同时要求 `refs/aria/coordination` 无本容器 active claim 指向某 spec dir (需读 state-scanner claim 契约, 跨 skill 依赖)。**推荐默认: 本 spec 不加固**, 声明进 audit trail 可事后核对; 加固另案。
3. **可配置下界 N** (issue 修法 3, 候选 C): **推荐默认: 不做**, 按 change 收窄后 N=1 即「≥1 份属于本 change」; 若要, 需先补 F8 的 audit 段 config 注册面。
4. **版本号**: PATCH v1.71.2 (SOT 规程 + 脚本, 无新 Skill)。若同伴容器先占 v1.71.2, 顺延 (bump 前 ls-remote tags)。

## References

- SOT (@`301641b`): `aria/skills/audit-engine/references/execution-modes.md:23-82` · `audit-engine/SKILL.md:47-54,75-81,105,123-125,381-388,403-419` · `references/report-storage.md:8-39` · `references/pre-write-validation.md:11-31` · `references/report-format.md:5` · `phase-c-integrator/SKILL.md:126-157,252-265,299` · `phase-c-integrator/scripts/path_coverage.py:1-50,547-549` · `agent-team-audit/references/audit-points.md` (checkpoint 触发定义) · `state-scanner/scripts/collectors/audit.py:52-114` (文件名 token 解析先例) · `state-scanner/scripts/lib/spec_complete.py:924-930` (liveness 分类)
- 规范: `standards/conventions/skill-benchmark-exemption.md` §2-§3 (Rule #6) · `standards/conventions/configured-gate-authority.md:28-40` (Rule #10 白名单第四类及其边界) · `standards/openspec/templates/proposal-minimal.md`
- 先例: `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md` (同类 Level 2 标杆; `not_applicable` 语义封闭集 §Why) · `openspec/archive/2026-09-04-sibling-spec-probe/` (audit-engine 脚本 + stdout 契约 + 消费措辞三档形态) · `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/` (#122 not_applicable 原始定义)
- 现场: Aria#199 issue 原文 · `.aria/triage-comment-199.md` / `.aria/triage-report-199.json` (2/2 复现) · aria-plugin#161 · aria-plugin#127 (第三行先例) · 本仓语料统计 (起草时 python 枚举, 数字见 F2/F3)
