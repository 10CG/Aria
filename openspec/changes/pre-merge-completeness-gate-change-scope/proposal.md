# pre_merge Completeness Gate 加 change 维度: 按被审 change 匹配报告 + 显式 not_applicable 三态 (Aria #199 / aria-plugin #161)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-06
> **Linked Issue**: `10CG/Aria#199, 10CG/aria-plugin#161`
> **Issue**: [Aria#199](https://forgejo.10cg.pub/10CG/Aria/issues/199) (2026-09-06 立案, aria-report 自动生成; triage 22288: confirmed / major / next-cycle) · [aria-plugin#161](https://forgejo.10cg.pub/10CG/aria-plugin/issues/161) (同缺陷在插件仓的记录, 标题「audit-engine pre_merge completeness gate 按文件名 glob 不按 spec_id 匹配 — 历史 spec 报告使门恒通过 (真实漏拦案例)」, open, 起草时 `forgejo GET` 复核)
> **认领**: 已于 2026-09-06T14:47Z 经 `phase1_gate.py --phase A.1 --mode advisory` 认领, track_id `pre-merge-completeness-gate-change-scope-bfe8285d`, `linked_issue_overlap=[]`, `unknown_schema_claims=0`
> **基线冻结**: aria 子模块 `origin/master` **`301641b`** (= v1.71.1); 本文所有行号对此 SHA (实读副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`, R1 rework 时对 `execution-modes.md` / `audit-engine/SKILL.md` / `phase-c-integrator/SKILL.md` / `report-storage.md` / `pre-write-validation.md` / `report-format.md` 六文件与 `git show 301641b:` 逐字 diff 为空)。**行号有效范围 (R1 勘正, 原文写成「全部触点文件 diff 为空」过宽)**: `git diff --stat 0545f86 301641b` 对上述**代码/规程六文件**为空, 行号在两 SHA 通用; 但 `CHANGELOG.md` (+71 行, 完整性门条目 @`0545f86` 在 `:2949` / @`301641b` 在 `:3020`)、`.claude-plugin/plugin.json`、`VERSION`、`README*.md`、`state-scanner/scripts/lib/spec_complete.py` (改 25 行, `if name == "SKILL.md":` @`301641b` 是 `:924` / @`0545f86` 是 `:903`) **均非空** —— 这几处的行号**只对 `301641b`** 成立, 追引用必须先 checkout 到 `301641b`。
> **gitlink 现况 (R1 实测勘正)**: 远端主仓 `master` 的 `aria` gitlink **已是 `301641b`** (forgejo `GET /repos/10CG/Aria/contents/aria?ref=master`), 同伴 v1.71.1 的主仓同步 PR **#202 已 merged/closed** —— 原文「gitlink 仍指 `0545f86`, 本 spec 的 bump 排在其后」是**幻影排队**, 已删除该前置。本地 checkout 仍停在 `0545f86` 且本地 master 与 origin/master 已分叉: **Phase B/C 开工前必须先 `git fetch` + 对齐到 `origin/master`, 否则主仓同步会把 gitlink 回退到 v1.70.0**。Phase B 在 `301641b` 起分支
> **代码落点**: `aria/skills/audit-engine/references/execution-modes.md` (§Pre-merge gate Step 3-5 + 校验失败输出) · `aria/skills/audit-engine/SKILL.md` (输入参数表 + Bash 调用块 + 配置注释) · **新增** `aria/skills/audit-engine/scripts/completeness_gate.py` + `tests/test_completeness_gate.py` · `references/report-storage.md` §向后兼容 · `references/pre-write-validation.md` 关联行 · `aria/skills/phase-c-integrator/SKILL.md` (C.2 pre_hook 传 change_id; `:157` 旧 schema 勘正) · `aria/CHANGELOG.md` + 版本引用点 · `aria-plugin-benchmarks/ab-suite/audit-engine.json` (+1 定向 eval) + `version.yaml`。Spec 落主仓 (Rule #5)
> **Rule #6 判定**: `execution-modes.md` Step 3-5 与 SKILL.md 调用块是**处方性 · 运行时指令面** (audit-engine 规程由 AI 编排执行)。**档位争议不影响执行面 (R1 rework)**: 一席判第二行 (照跑 AB)、两席判第三行 (套件覆盖外 + substitute), 本 spec **取两读法的并集, 不取任何豁免** —— 既照跑全部相关既有套件验漂移, 又补定向 fixture + 缺口 issue (rule6_note 见文末; 档位标签本身列 待 owner 复议 #5)。相关套件实读: `ab-suite/audit-engine.json` 文件内 `version` 字段 = **`1.0.0`** (2 evals, 全是竞品探针场景, `grep -i "completeness\|missing_checkpoint\|allow_incomplete"` 零命中), `ab-suite/phase-c-integrator.json` (3 evals) 与 `ab-suite/phase-c-integrator-pre-merge-gate.json` 亦实存且本 spec 改其处方面 —— 三者全部照跑。**注**: `1.3.0` / `1.4.0` 是 `ab-suite/version.yaml` 的**套件**版本 (现值实测 1.4.0), 与 `audit-engine.json` 文件内 `version` 是两个不同的 `version`, 全文点名区分。脚本 + schema + 勘正 = 描述性 ⇒ substitute = SC-1~SC-13 结构化测试
> **A.1.0 头脑风暴**: 未跑 — `audit.checkpoints.post_brainstorm = off` (Rule #10 白名单第一类)
> **审计计划**: post_spec convergence 5 席 (config enabled) → post_planning convergence (config enabled); mid_implementation / post_implementation / pre_merge / post_closure 均 config off (白名单第一类)
> **审计轨迹**: post_spec R1 (2026-09-06) 票型 REVISE 5 / PASS 0 (单席 verdict FAIL 4 + PASS_WITH_WARNINGS 1), 缺陷计数 **C5 / M9 / m10** (另 7 条 decision 不计入), 聚合报告 `post_spec-R1-2026-09-06T155000-000Z-R1-pre-merge-completeness-gate-change-scope-aggregated.md` ⇒ 本文为 **v2 (R1 rework 后)**, 逐条处置记录见 rework 清单; 三条 conflicted / 档位分歧转 待 owner 复议 #5-#7

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
| case-2 (本仓语料模拟) | 本仓 `.aria/audit-reports/` 780 条目 (778 `.md` + 2 目录; **R1 rework 时已长到 786 `.md`** —— 本轮 post_spec 五席 + 聚合各写 1 份, 语料是活体, 见 SC-2 的冻结产物要求), 假想新 change (自身零份报告) | `post_spec-*.md` 命中 **499** / `post_planning-*.md` **209** / `post_implementation-*.md` **3** (归属 `state-scanner-mechanical-t3` / `aria-secret-guard-plugin-default-orchestrator` / `audit-drift-guard`); 属于假想 change 的 **0** 份 → 按原文三者均「通过」 | match |
| issue 报告方 | 37 份他人 `post_implementation-*.md`, 被审 change `synth-honesty-gaps` Phase A-only 自身 0 份 | 门 PASS; 编排者靠人工核对报告归属才发现 PASS 无效, 改按「Phase A-only ⇒ post_implementation 不适用」独立论证放行 (**没有采信门的绿**) | 同型 |

**根因有两层**:

1. **匹配面无 change 维度**: 门问的是「目录里有没有这个 checkpoint 的任何报告」, 与被审 change 无关。项目历史越长越必然 PASS —— 与它要防的失效 (「该跑的没跑」) 同型: 零相关证据也判绿。
2. **change_id 在 pre_merge 根本没被投递**: `audit-engine/SKILL.md:49-54` 输入参数只有 `checkpoint / mode / context / agents_config`, 没有 `change_id`; `report-storage.md:18` 说 `{spec_id}` 「从 dispatch context」取, `pre-write-validation.md:14` 说 change_id「从调用方 context 读取」—— 而 phase-c-integrator 在 pre_merge 传的 `context` 是 **`PR diff (branch_name vs base)`** (`phase-c-integrator/SKILL.md:136`; `:137` 是「5. 处理 verdict」—— R1 勘正, 原写 `:137`), 不是 spec 路径。post_spec 那条链是通的 (`phase-a-planner/SKILL.md:250` 传 `openspec/changes/{spec_id}/proposal.md`; R1 勘正, 原写 `:248`), pre_merge 这条链结构上就没有 change_id 可用。Step 4 不带 change 维度不是疏忽, 是**没有输入**。

### 起草期实读补充的事实 (issue / triage 没写, 改变修法形态)

| # | 事实 | 出处 | 含义 |
|---|---|---|---|
| F1 | 本仓 `audit.checkpoints.pre_merge = "off"` | `.aria/config.json` audit 块 (起草时 `python3 -c json.load`) | 该门在 Aria 自身**从不执行** (触发条件 `execution-modes.md:32` 仅 pre_merge)。triage 注「本仓 pre_merge 目前只会把 post_spec 纳入校验」漏了这一层; 且本仓 `post_planning = convergence`, 若开 pre_merge, Step 3 会纳入 post_spec **和 post_planning** 两项。⇒ 本 spec 的活体验证只能手动跑脚本 (SC-11), 不能靠生产 pre_merge 调用 |
| F2 | 真实文件名**不服从** `report-storage.md:8` 的 5-field schema | 本仓语料 `ls .aria/audit-reports \| sed 's/[0-9]+/N/g' \| uniq -c`: 时间戳段有 epoch ms (`1787379154696`) / ISO (`2026-05-23T0900Z`) / 纯日期 (`2026-05-23`) / 小整数 (`R4-4-…`); round 段有 `R5.5` / `R1prime` / `FINAL`; role 段有席位前缀 `A1-tech-lead`、`aggregated` / `aggregate` / `orchestrator` / `usN-mN`; `post_spec-*` 499 份中 24 份不匹配 `-R\d+-`, post_planning 2 / pre_merge 1 / mid_implementation 1 | triage 修法 1 写的 `{checkpoint_name}-*-{change_id}-*.md` 按**位置**取 spec_id 不可靠; 匹配必须是**连字符界定的子串**, 不解析段序。**R1 勘正**: 原文写「子串 `-{change_id}-` … 不依赖前后段形态」自相矛盾 —— 双侧连字符恰恰依赖「id 后面还有一段」。真实语料里 id 落**末段** (`…-{id}.md`, 无 role 段) 的报告有 **62 份**, 故归属谓词必须**左侧连字符界定 + 右侧连字符或字符串末尾**二选一 (见 §1.2 规则 2)。先例同向: state-scanner `collectors/audit.py:62-69` 只合成**首**连字符做左侧界定, 正是为了不假设尾段存在 (`_CHECKPOINT_PREFIX` + `"-" + name[m.end():]`) |
| F3 | change_id 集 `C` 现有 **152** 个 (`openspec/changes` **9** 目录 + `openspec/archive` **143** 目录去 `YYYY-MM-DD-` 前缀; `archive/` 下第 144 个条目是 `README.md` 不是 change —— R1 勘正, 原文写「7 + 144 = 150」两处都错)。其中**前缀碰撞 1 对** (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`), **后缀碰撞 0 对, 中缀碰撞 0 对** (R1 全枚举实测) | R1 rework 时 python 全枚举 | 子串规则须加「有界包含排除」: 存在更长的 `c' ∈ C` 使 `-{id}-` 是 `-{c'}-` 的子串时, 命中 `c'` 的文件**不计入** `id`。现存实例只有前缀型, 但规则发给所有采用方 ⇒ 谓词须对称覆盖前缀/后缀/中缀三型 (见 §1.2 规则 3) |
| F4 | 旧 schema `{checkpoint}-{timestamp}.md` 无 spec_id, 本仓实测 **6 份**; 而「不含任何 `-{c}-` 子串」的报告实测 **238 份** (= 6 份真 legacy + 62 份 id 落末段 + **170 份 id 段不在 `C`**: 截断/别名/自造 id, 如 `post_planning-R2-CONVERGED-dispatch-input-delivery.md` 之于 `aria-2.0-m6-dispatch-input-delivery`) | `report-storage.md:37` (reader 视为 R1/legacy) + R1 rework 全枚举 | 「无 change 段」≠「旧 schema」, 差 **39.7 倍**。故输出必须**拆两个计数**: `excluded_legacy_count` 只统计真 2-field `{checkpoint}-{timestamp}.md`; `unattributed_count` 统计「有 id 段但该 id 不在 `C`」并把文件名列进 audit trail。混成一个数会把归属失败伪装成历史包袱 (R-a 的显影缓解会反向失效) |
| F5 | phase-c-integrator 已有 `not_applicable` 语义 = 「被审对象结构性不存在, 没有可等的 CI」(`phase-c-integrator/SKILL.md:252,260,299`; `path_coverage.py:8,547-549`), 且 C.2.4 步骤 6 规定 green 来源为 not_applicable 时**必须 surface 警告行** (`:265`) | 实读 | 本 spec 的 `not_applicable` 沿用同一语义边界: 只在「对象整个未产生」时产生, 且必须进 audit trail; 与 CLAUDE.md Rule #10 白名单第四类「闸门自身的结构性前提不成立」(`configured-gate-authority.md:38`) 同义, 其边界注「A.2 没做 = 合法; A.2 做了但很简单 = 不合法」(`:40`) 直接约束本 spec 的判据设计 |
| F6 | audit-engine 已有**机械化 diff 判据**: file-scope 二次过滤 `changed_files = git diff --name-only $(git merge-base HEAD <base>)`, 全部 ⊆ `audit.scope_skip_paths` ⇒ docs/ops-only (`audit-engine/SKILL.md:403-419`; `DEFAULTS.json:118-123` 已注册 `scope_skip_paths` = `deploy/` `docs/` `.forgejo/workflows/` `.github/workflows/` `*.md`) | 实读 | **只复用 diff 取法, 不复用 `scope_skip_paths` 谓词 (R1 rework 反转)**: 该键的 SOT 语义唯一 —— `SKILL.md:398-400` #58 DEC-4 明写「**降级非 skip**」, 且实证 deploy 脚本改动 challenge 能抓到真退化。把同一谓词提升为整个 checkpoint 免检, 后果从「少跑一档」变成「零审计通过」; 叠加缺省含 `*.md` 而 aria-plugin 产品本体即 markdown 处方 ⇒ 纯 `.md` Skill 变更会常态「零自身证据也 PASS」= 与被修 bug 同型的新假绿。§1.3(b) 已改用与「对象未产生」同义的判据, `scope_skip_paths` 在本 spec **零消费** |
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
  --repo-path "<主仓 root>" --diff-repo-path "<C.2 合并目标仓 root>" --base "<main_branch>" \
  [--change-id <id> ...] [--no-spec]
```

- `--repo-path`: **锚点面 = 主仓根**, 承载三样东西: 报告目录 `.aria/audit-reports/`、config、`openspec/{changes,archive}/` 锚点链。
- `--diff-repo-path`: **diff 面 = 本次 C.2 实际合并的目标仓根**, 只用于 `git diff` / `merge-base`。缺省 = `--repo-path`。
- **为什么必须拆 (R1 rework)**: `phase-c-integrator/SKILL.md:252` 的执行上下文契约明写同类脚本「在执行 C.2 合并的**目标仓根**内调用 (子模块合并 → 子模块根)」, 而**子模块 PR 正是本项目 pre_merge 的主力场景**; 实测 `aria/` 子模块内 `openspec/` 与 `.aria/` **均不存在** (`test -d` 两项皆假)。单参数两个方向都坏: 传子模块根 ⇒ 零报告 + S1 恒 `change_id_unanchored` exit 2 (该错**不受** `allow_incomplete_checkpoints` 豁免) 的假红; 传主仓根 ⇒ diff 取错仓 (本 cycle 主仓 diff 全是 `openspec/**` 而代码全在子模块) 的假绿。
- **fail-closed 附加条款**: `--diff-repo-path != --repo-path` 时 (跨仓形态), `not_applicable` 的 (b) 通道 **禁止触发** —— 主仓 diff 的路径形态无法代表子模块内的实现工序; 一律走 `present`/`missing`。同理, diff 中出现 gitlink/submodule 条目时 (b) 亦不触发。
- config 一律经 **config-loader** 读取 (不直读 `<repo>/.aria/config.json`), 见 §1.4「config 读取」。
- `--base`: 主干真实名 (本项目 `master`), 供 diff; **不提供缺省 `main`** (#137 教训, `phase-c-integrator/SKILL.md:253`)。
- `--change-id` (可重复): 显式作用域; `--no-spec`: Level 1 声明 (见 1.1 S3)。

#### 1.1 change 作用域解析 (S1 → S4, first-match)

| 步 | 条件 | 结果 |
|---|---|---|
| S1 | `--change-id` 给出 | 每个 id 必须有锚点: `openspec/changes/{id}/proposal.md` 或 `openspec/archive/*-{id}/proposal.md` (复用 `pre-write-validation.md:20-26` 锚点链, 逐字目录名); 任一无锚 → `error_kind=change_id_unanchored`, exit 2 (拼写错不能变成「零报告 → missing」的假红, 也不能变成假绿) |
| S2 | 无显式 id | 从 `git diff --name-only $(git merge-base HEAD <base>)` (与 `audit-engine/SKILL.md:406` 同命令) 取路径前缀 `openspec/changes/<id>/` 的去重 id 集; 非空 → 作用域, `scope_source=diff` |
| S3 | S2 为空且 `--no-spec` | 机械交叉核验: diff **不触** `openspec/changes/**` (触了即与声明矛盾 → `error_kind=no_spec_contradicted`, exit 2); 通过 → 全部纳入校验的 checkpoint 记 `not_applicable(reason=level1-no-spec)` (Level 1 无 spec ⇒ 报告文件名无 spec_id 可写, `pre-write-validation.md:28-30` 会拒绝写盘 ⇒ 对象结构性不存在), `scope_source=no_spec`; audit trail 必须留 `[INFO]` 行 (见 1.4) |
| S4 | 其余 | `error_kind=change_scope_unresolved`, exit 2, 文案给三个 fix: 传 `--change-id` / 在分支里带上 change 目录变更 / Level 1 加 `--no-spec`。**不放行** (零证据不当正证据) |

`allow_incomplete_checkpoints=true` 时 S4 / missing 均降为 `verdict=bypassed` + exit 0, S1/S3 的 `error` 不被豁免 (输入矛盾不是「不完整」)。

**豁免文案 (R1 勘正 —— 原稿造了第三种拼法)**: 现行 SOT 有两种字面, `execution-modes.md:44` = `[WARN] incomplete checkpoint gate bypassed by config` (无 missing 列表), `:82` = `[WARN] incomplete checkpoint gate bypassed: missing={checkpoint_names}`。本 spec **不新造措辞**, 统一为 `:82` 的形态并把两处 SOT 对齐成同一句 (列入 §4 同步表, SC-13 逐字 grep):

```
[WARN] incomplete checkpoint gate bypassed: missing={cp}@{change_id},... ; scope_unresolved={0|1}
```

`scope_unresolved=1` 即 S4 被豁免的那一路。**S4-bypassed 的字段取值 (原稿未定义)**: `verdict=bypassed`, exit 0, `error_kind=null`, `scope_source=null`, `change_ids=[]`, `checked_checkpoints` 照常枚举, `results=[]` (无作用域 ⇒ 无逐对结果), `bypassed=true`。

#### 1.2 报告归属匹配规则 (改前 → 改后)

改前 (`:57-60`): `{checkpoint_name}-*.md` 或 `{checkpoint_name}-*-*.md` 任意命中 → 通过。

改后, 文件 `f` 归属 `(checkpoint, change_id)` 当且仅当**全部**成立:

1. `f.startswith(f"{checkpoint}-")` 且 `f.endswith(".md")`;
2. **双侧界定 或 末段界定** (R1 rework 放宽): 令 `stem = f[:-3]` (去 `.md`), 则 `f` 命中 `change_id` 当且仅当 `f"-{change_id}-" in f` **或** `stem.endswith(f"-{change_id}")`。**逐字**, 大小写敏感, 不做归一化 (`openspec/changes/<id>` 目录名就是契约, 写侧 `report-storage.md:18` 也逐字取)。
   > **为什么改 (本轮 5/5 全席独立命中的 Critical)**: 原稿只写「含 `-{change_id}-`」, 漏掉 change_id 落**末段**的 `…-{id}.md` 形态 (无 `agent_role` 段)。本仓实测该形态 **62 份**, 覆盖 **25 个 (checkpoint, change_id) 组合的全部自有报告** —— 这些 change 明明跑过审计却会被判 `missing` 假红**阻断合并**。含在飞 change (`aria-2.0-m6-release-closeout` / `aria-2.0-m6-cost-acceptance` / `aria-2.0-m6-e2e-resilience`) 与**全部 3 份 `post_implementation` 报告** (其中 `post_implementation-R1-2026-06-11-audit-drift-guard.md` 正是本文 case-2 表格自己点名归属的那份); 该形态仍在产生 (最新一例 `post_spec-R2-2026-06-25-session-closer-synthesis.md`)。左侧连字符界定与 `collectors/audit.py:62-69` 的单侧合成先例同向。
3. **有界包含排除 (对称, R1 rework)**: 令 `C` = `openspec/changes/*` ∪ `openspec/archive/*` (去 `YYYY-MM-DD-` 前缀) 的 id 集。若存在 `c' ∈ C`, `c' != change_id`, 使 `f"-{change_id}-"` 是 `f"-{c'}-"` 的子串 (等价: `c'` 以 `{change_id}-` **开头**、以 `-{change_id}` **结尾**、或含 `-{change_id}-`), 且 `f` 按规则 2 命中 `c'`, 则 `f` **不**归属 `change_id`。
   > 原稿只写 `c'.startswith(change_id + "-")` 即**只挡前缀扩展**, 后缀型与中缀型碰撞下他人 change 的报告仍会计入本 change —— 与被修 bug **同型** (假绿方向)。本仓现存 152 个 id 中前缀碰撞 1 对、后缀 0 对、中缀 0 对 (R1 全枚举), 故这是**潜在缺陷而非现存实例**; 但规则是发给所有采用方的通用契约, 必须对称封死并由 SC-3 锁定不变量。

不要求 `-R\d+-` 段, 不解析时间戳与 role (F2: 位置不可信)。

**两个排除计数 (R1 rework 拆分, 原稿合并成一个 `excluded_legacy_count` 会掩盖 Critical 1)**:

| 计数 | 定义 | 本仓实测 | 输出义务 |
|---|---|---|---|
| `excluded_legacy_count` | 真 2-field 旧 schema: `f` 匹配 `^{checkpoint}-[0-9TZ:.\-]+\.md$` 且不含任何 `C` 中 id (F4) | **6** | 计数即可 |
| `unattributed_count` | 以 `{checkpoint}-` 开头、按规则 2 对**任何** `c ∈ C` 都不命中、且不属于上一行 | **170** (截断/别名/自造 id) | 计数 **+ 文件名列表进 audit trail** (`[WARN] unattributed reports: …`), 供采用方发现自己的写侧偏离 |

> 原稿定义「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」= 本仓 **238 份**, 会把上面那 62 份**真报告**吞进 legacy 计数 ⇒ R-a 依赖的「legacy 计数显影」不但不显影, 反而把归属 bug 伪装成历史包袱, 编排者读到「legacy 不计入: N」会得出相反结论。

#### 1.3 per (checkpoint, change_id) 三态 (改前: 二态 通过 / missing)

**Step 3 枚举 (`:46-52`) 追加一条排除: `mid_implementation`** (R1 rework)。它与已排除的 `mid_post_spec` **同因** —— `DEFAULTS.json` 里 `audit.mid_implementation = {trigger: task_progress, threshold: 50, unit: percent_tasks_completed}`, `audit-engine/SKILL.md:63` 标「条件触发」: 启用但任务进度未过 50% 阈值时**合法不产出报告**, 落 `execution-modes.md:51-52` 的「启用即会误阻」原句。原稿把它交给 1.3(b) 兜底, 但 (b) 只在「diff 全是 docs」时生效, 而最常见场景恰是「code diff + 进度未过阈值」⇒ 仍判 `missing` 假红。排除条款与 `mid_post_spec` 同构书写。另有一条候选追加 `post_brainstorm` (待 owner 复议 #1)。

对每个纳入的 checkpoint × 作用域内每个 change_id:

| 状态 | 判据 (按序 first-match; 全部是机械结构事实, 无 AI 价值判断) |
|---|---|
| `present` | 1.2 规则命中 ≥ 1 份 |
| `not_applicable` | (a) `scope_source=no_spec` (S3); 或 (b) checkpoint = `post_implementation` **且** `--diff-repo-path == --repo-path` **且** diff 非空 **且** 全部变更文件路径都在 `openspec/changes/**` ∪ `openspec/archive/**` 之下 (即 **Phase A-only PR**: B.2 实现工序整个未发生) → reason `phase-a-only-no-implementation`; 或 (c) checkpoint = `post_planning` 且**不存在任何 A.2 产物**: `openspec/changes/{id}/tasks.md` 与 `detailed-tasks.yaml` 都不存在 **且** `proposal.md` 无 `^#{2,}\s*Tasks` 小节 (归档态取 `archive/*-{id}/`) → reason `no-a2-artifact` (Rule #10 `:38` 的原例) |
| `missing` | 其余 (含 diff 为空: `SKILL.md:410` 防 vacuous-true 同款, 空集不放行) |

**(b) 为什么不再用 `scope_skip_paths` (R1 rework, 反转原设计)**: 见 F6 含义列 —— 该键 SOT 语义是「降级非 skip」(DEC-4), 缺省又含 `*.md`, 用作 checkpoint 免检会给 aria-plugin 这类「产品本体即 markdown 处方」的仓造出与被修 bug 同型的新假绿, 且落在 Rule #10 白名单第四类的**禁止侧** (`configured-gate-authority.md:40`「存在但简单」不算)。改用的新判据与 issue 报告方**自己独立论证放行的那一格逐字同义** (「`synth-honesty-gaps` 是 Phase A-only ⇒ post_implementation 不适用」), 属于「对象整个未产生」的合法侧。跨仓形态下禁触发 (见 §1 fail-closed 条款)。

**(c) 为什么改成「任何 A.2 产物」(R1 rework)**: 原稿只看 `tasks.md`/`detailed-tasks.yaml` 两个**文件**。但 Level 2 的 A.2 产物结构上就是**内联**的 —— `standards/openspec/project.md:118` 规定 Level 2 输出 = `proposal.md` (tasks.md 是 Level 3), `templates/proposal-minimal.md:27-31` 自带 `## Tasks` 小节。按文件判 ⇒ **每个 Level 2 change 恒成立** ⇒ 自动豁免采用方已 enabled 的 post_planning, 正是 Rule #10 要禁的形态。**本 spec 自身即此形态** (内联 `## Tasks`、无 `tasks.md`, 却在头部声明跑 post_planning): 按原稿判据本 spec 会给自己发一张 not_applicable 免检票 —— 自相矛盾。改后本 spec 走 `present`/`missing`, 与头部声明一致。非真空: 本仓归档语料实测「三样 A.2 产物全无」的 change 有 **37** 个 (52 个无 A.2 文件的 change 中 15 个有内联 `## Tasks`), (c) 在它们上仍会正常触发。

`post_spec` 无 not_applicable 通道 (有 change_id 即有 proposal, 对象必存在)。「做了但很简单」(如 tasks.md 只有 3 行、内联 Tasks 只有 2 条) 恒 `present`/`missing`, 不进 not_applicable (`configured-gate-authority.md:40`)。

#### 1.4 路由 + stdout 契约 (改前: `:63-65` 二路由 + `:70-80` 单一 ERROR 模板)

**config 读取 (R1 rework)**: 一律经 **config-loader** (`execution-modes.md:37-38` Step 1 与 `phase-c-integrator/SKILL.md:130` 步骤 1 两处 SOT 都明写走 config-loader), **不直读** `<repo>/.aria/config.json`。原稿的直读绕过了旧配置兼容映射 (`config-loader/SKILL.md` §旧配置兼容层: `experiments.agent_team_audit=true` 且无 `audit` 块 ⇒ 逐项映射 `checkpoints.post_spec/post_implementation/pre_merge = "convergence"`) —— 这类采用方直读时 `audit` 块不存在 ⇒ `checked_checkpoints=[]` ⇒ 恒 `verdict=pass` 的真空绿, 正是本 spec 要修的失效同型。**config 文件缺失**时: 按 config-loader 的缺省 (audit 全 off) ⇒ 落下面的空集短路, 不静默 pass。
**两个 `allow_*` 键的缺省源 (R1 勘正)**: `allow_incomplete_checkpoints` / `allow_dangling_change_ids` 实测**不在** `DEFAULTS.json` 的 audit 键集内 (F8), 故「缺省值与 DEFAULTS.json 一致」对它们**无源** —— 唯一出处是 `audit-engine/SKILL.md:385-388` 散文「默认 false」。本 spec 按该散文取 `false`, 并把「补进 DEFAULTS.json」写进 F8 的 Phase D 缺口 issue。

- 任一 `missing` → `verdict=fail`, exit **1**; 全部 `present`/`not_applicable` → `verdict=pass`, exit 0; 豁免 → `verdict=bypassed`, exit 0; 输入/环境错 → `verdict=error`, exit **2**。
- **空集短路 (R1 rework, 原稿缺此路)**: `checked_checkpoints == []` (config 全 off / 无 audit 块 / config 缺失) ⇒ **不判 pass**, 而是 `verdict=error` + `error_kind=no_checkpoints_configured`, exit **2**, 并输出 `[ERROR] completeness gate: 纳入校验的 checkpoint 为空 (audit 未启用或全 off) — 零证据不当正证据`。理由与 §1.4 已有的「diff 空集不放行」、`SKILL.md:410` 防 vacuous-true 同款。**例外**: `audit.enabled=false` 时门本就不该被调用 (`phase-c-integrator/SKILL.md:131` 步骤 2 早退), 脚本若仍被调用则照上述 error 处置, 由调用方早退负责不触发。
- stdout 恰一个 JSON (`schema_version "1"`, `gate "completeness_gate"`), 顶层键集**逐字**为: `schema_version` / `gate` / `verdict` / `error_kind` (str|null, 封闭集 `change_id_unanchored` / `no_spec_contradicted` / `change_scope_unresolved` / `no_checkpoints_configured` / `git_failed` / `config_unreadable`) / `scope_source` (`explicit`|`diff`|`no_spec`|null) / `change_ids` [] / `checked_checkpoints` [] / `results` [{`checkpoint`, `change_id`, `status`, `reason`, `matched` [文件名], `matched_count`}] / `excluded_legacy_count` / `unattributed_count` / `unattributed` [文件名] / `bypassed` bool / `elapsed_ms`。`results` **恒为 list**, 消费方不得从 `matched == []` 推断 (与 `execution-modes.md:185` 探针条款同构)。
- **两个计数的作用域 (R1 勘正, 原稿未定义)**: `excluded_legacy_count` / `unattributed_count` / `unattributed` 是**全局单值**, 统计面 = `.aria/audit-reports/` 下以**任一纳入校验的 checkpoint** 名开头的文件的并集 (不含未纳入的 checkpoint 的文件)。`checked_checkpoints` 的顺序 = **`sorted()` 字典序** (不是 config key 序), 使断言可逐字比对。
- **消费方 fail-closed 义务** (写进 execution-modes.md): exit≠0 或 stdout 非 JSON 或 `schema_version` 未知 ⇒ 按 `fail` 处置 (拒绝执行 pre_merge 审计, 输出 ERROR), 不得按 PASS。
- 三态各有 audit trail 行 (取代 `:70-80` 单模板):
  - missing: `ERROR: pre_merge audit 前序 checkpoint 报告缺失: {cp}@{change_id} 配置 "{mode}" 但未找到 .aria/audit-reports/ 下含 "-{change_id}-" 或以 "-{change_id}.md" 结尾的 {cp} 报告 (真 legacy 不计入: N; 归属不明: M, 见下方清单)` + Fix 三项 (补跑 / 改 off / allow_incomplete);
  - `unattributed_count > 0` 时另起一行 `[WARN] unattributed reports ({cp}): <文件名逐个>` —— 让写侧命名偏离当场显影, 不与 legacy 混计;
  - not_applicable: `[INFO] completeness gate: {cp}@{change_id} not_applicable ({reason}); 依据 = <机械事实: diff N 文件全部在 openspec/changes|archive 下 (Phase A-only) | 无 tasks.md/detailed-tasks.yaml 且 proposal.md 无 ## Tasks 小节 | --no-spec 且 diff 不触 openspec/changes/>` — **必须 surface**, 不得折叠进「校验通过」;
  - present: `[OK] {cp}@{change_id}: N 份` (逐行, 使「通过」可核对归属)。
- 一个 PR 含多个 change (S1 多值 / S2 多 id): 逐 (checkpoint, change_id) 评估, **全部**非 missing 才 pass; ERROR 逐对列出。

### 2. audit-engine 接线 (SKILL.md)

- `## 输入参数` 表 (`:49-54`) additive 加 `change_id` (string | list, 否, 「被审 change 的 openspec 目录名; pre_merge 必传, 缺失时脚本走 S2-S4」)。
- `## 执行流程` (`:75-81`) 第 (2) 阶段描述改为「经 `completeness_gate.py` 机械执行, 三态 + fail-closed」; **新增 fenced bash 调用块** (F7, 与 `:123-125` 探针块并列)。
- `## 配置依赖` (`:385-388`) `allow_incomplete_checkpoints` 注释补「豁免 missing / scope_unresolved, 不豁免输入矛盾」。
- `execution-modes.md` §Pre-merge (`:23-82`): 互补说明 (`:25-30`) 补一句「#26 自本 spec 起带 change 维度」; **Step 1 (`:37-38`) 保留 config-loader 表述** (脚本据此实现, 不直读 config); Step 3 (`:46-52`) **追加 `mid_implementation` 排除条款** (与 `mid_post_spec` 同构书写, 见 §1.3); Step 4-5 改为调用行 + 1.2 规则 + 1.3 三态表 + 1.4 契约; `:68-80` 校验失败输出改三态模板; **`:44` 与 `:82` 两处豁免文案统一为同一句** (§1.1 的形态, 消除现存两种拼法)。

### 3. phase-c-integrator (调用方)

- `SKILL.md:133-136` pre_hook 步骤 4 (步骤 4 的正文占 `:133-136`, `:137` 是「5. 处理 verdict」) 追加两行: `- change_id: 本 cycle 的 spec 目录名 (来自 A.1 spec 路径 / claim track 的 spec dir; Level 1 传 no_spec=true)` 与 `- repo_path / diff_repo_path: 锚点面恒主仓根, diff 面 = 本次 C.2 合并的目标仓根 (子模块合并 → 子模块根, 与 :252 的执行上下文契约一致)`; 步骤 5 前插「4.5 completeness gate 三态处置: fail → 阻塞并输出 ERROR; not_applicable → workflow report 必带 `[INFO]` 行; `unattributed_count > 0` → 必带 `[WARN]` 行」(镜像 `:265` 的 surface 义务写法)。
- `:157` `audit_report: ".aria/audit-reports/pre_merge-{timestamp}.md"` 是旧 schema 残留 → 勘正为 `report-storage.md` 的 5-field 形态 (描述性, 顺手)。

### 4. 文档同步面 (Rule #3)

| 文件 | 位置 (@301641b) | 改动 |
|---|---|---|
| `audit-engine/references/execution-modes.md` | `:23-82` (含 `:37-38` / `:46-52` / `:44` / `:82`) | §2 所述; 删除 `{checkpoint_name}-*.md` 两行通配; Step 3 加 `mid_implementation` 排除; `:44` 与 `:82` 豁免文案统一 |
| `audit-engine/SKILL.md` | `:49-54` / `:75-81` / `:385-388` / `:427-433` 相关文档 | 输入参数 + 调用块 + 配置注释 + 相关文档加 `completeness_gate.py` 契约指针 |
| `audit-engine/references/report-storage.md` | `:34-39` §向后兼容 | 追加「completeness gate 归属匹配认**含 `-{spec_id}-` 或以 `-{spec_id}.md` 结尾**的文件 (末段形态是本仓 62 份真实报告的实际形态); 真 2-field 旧 schema 不计入并以 `excluded_legacy_count` 显影; 有 id 段但 id 不在 `openspec/{changes,archive}` 内的以 `unattributed_count` + 文件名清单显影 —— 两者**不得**混计」 |
| `audit-engine/references/pre-write-validation.md` | `:3` 关联行 | #26 互补描述补 change 维度 |
| `phase-c-integrator/SKILL.md` | `:133-136` / `:157` | §3 |
| **旧 report schema 散文残留 (R1 rework 补全, 形态族穷举)** | `phase-a-planner/SKILL.md:267` / `phase-b-developer/SKILL.md:204` / `phase-b-developer/SKILL.md:277` | 三处与 `phase-c-integrator:157` **逐字同构** (`.aria/audit-reports/{cp}-{timestamp}.md`), 一并勘正为 `report-storage.md:8` 的 5-field 形态。原稿只改 1 处 ⇒ 修完仍留三份误导性范例。全仓该形态实测恰 **4 处** (`grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/`); `report-storage.md:37,43` 与 `report-format.md:5` 的 `{checkpoint}-{timestamp}.md` 是**合法的向后兼容描述**, 不动 |
| `aria/CHANGELOG.md` + 版本引用点 | — | PATCH **v1.71.2** (bump 前 `ls-remote --tags` + 读同伴 handoff `<vNEXT>`, memory 并行发版撞号); 主仓 14 版本字符串点 + gitlink (Aria#177 口径) |
| `aria-plugin-benchmarks/ab-suite/audit-engine.json` | `evals[]`; 文件内 `version` 字段现值 **1.0.0** | 新增定向 eval id 3 (descriptive 形态与 id 1/2 一致)。文件内 `version` 是否随 eval 增补而 bump: **随 catalog 惯例, 本 spec bump 到 1.1.0** 并在 PR 描述点名 (原稿未说明该字段动不动) |
| `aria-plugin-benchmarks/ab-suite/version.yaml` | `version` (**套件**版本, 现值实测 **1.4.0**) + `changelog[]` | 1.4.0 → **1.5.0**。**并发预案 (R1 rework)**: 在飞同伴轨 `a1-entry-claim-duplicate-work-guard` 的 `tasks.md:26` 把 `version.yaml` 列为**串行**编排对象且计划在 `state-scanner.json` 内新增 eval, 双方都会指向下一个 MINOR ⇒ 改这两个文件前先 `git fetch --all` + 读同伴 tasks/handoff, 撞号则顺延为 1.6.0; `skills_covered` / `total_eval_cases` 按程序化重算, 不手填 |

### 5. 向后兼容 (消费方 grep, 起草时全 skill 树 + 主仓)

- `allow_incomplete_checkpoints` / `missing_checkpoint` / `Completeness Gate` 的消费方: 仅 `execution-modes.md` / `audit-engine/SKILL.md` / `pre-write-validation.md` / `CHANGELOG.md:3020` (历史条目) — 全 skill 树 `--include=*.py --include=*.json --include=*.yaml` **零代码消费方**; 主仓外仅 `ab-results/2026-04-23-v1.16.2-patch/` 历史 benchmark (不动)。
- 文件名 schema 消费方: `state-scanner/scripts/collectors/audit.py:52,62-114` (只挑 `-aggregated.md`/`-aggregate.md` 候选 + token 正则解析时间戳) 与 `aria-dashboard/references/parse-rules.md:79-103` (glob `*.md` + 文件名前缀 fallback checkpoint) — 本 spec **只读**文件名, 不改 writer schema, 两者零影响。
- config 键: 零新增; 读 `audit.checkpoints` / `audit.allow_incomplete_checkpoints` (经 config-loader)。**R1 rework 后 `audit.scope_skip_paths` 不再被本 spec 消费** —— (b) 判据已换成 Phase A-only, 故原稿「脚本自带一份与 DEFAULTS.json 一致的 `scope_skip_paths` 缺省」这个**第二副本连同其漂移风险一并消失**, 无需再为它写相等性 SC。
- audit-engine 输入 `change_id` additive 可选; 其它 checkpoint 调用方 (phase-a-planner / task-planner / phase-b-developer / phase-d-closer) 不受影响 (门仅 pre_merge 触发, `execution-modes.md:32`)。
- 行为变化面: 只有 `audit.enabled=true ∧ checkpoints.pre_merge != off` 的采用方 (本仓不在其中, F1)。对这些采用方共 **三条**行为变更 (原稿只列第一条):
  1. 曾经的假绿会变成 `missing` 阻断 —— 这是修复本身;
  2. **`allow_incomplete_checkpoints` 的豁免面被收窄**: `execution-modes.md:41-44` 原义是「跳过校验, 继续执行」(整门不算), 本 spec 改为「仍逐对评估三态并全部留痕, 只把 missing / S4 降为 `bypassed`; S1/S3 的输入矛盾错**不被豁免**」⇒ 已开该旗标的采用方会新看到 exit 2 的 `change_id_unanchored` / `no_spec_contradicted`;
  3. **空 `checked_checkpoints` 从「静默 pass」变成 exit 2** (`no_checkpoints_configured`) —— 影响「开了 pre_merge 但其余 checkpoint 全 off」的采用方。
  三条迁移文案全部写进 CHANGELOG (「若历史 change 报告用旧 schema, 需补跑或临时 allow_incomplete」+ 上面 2/3 两条的处置)。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 门的 PASS 与被审 change 相关: 其他 change 的报告不再构成证据; 「缺失」与「不适用」可分辨且各有 audit trail 行; change_id 在 pre_merge 有了输入通道; 规程可测 (hermetic 红转绿) |
| **Risk** | R-a 采用方历史 change 报告**不服从写侧命名约定** → 收窄后转 missing (假红形态)。**R1 rework 改写了量级**: 本仓 786 份报告里, 归属不明 (`unattributed`) 实测 **170 份**、真旧 schema 只有 **6 份** —— 这不是「少量历史包袱」, 而是写侧散文约定的真实执行水平 (读侧机械化了, 写侧仍是散文)。缓解: `excluded_legacy_count` 与 `unattributed_count` **分开显影** + `unattributed` 文件名进 audit trail + CHANGELOG 迁移文案 + `allow_incomplete_checkpoints` 既有豁免。**写侧强制**不在本 spec 范围, 记 Phase D 缺口 issue |
| **Risk** | R-b `--no-spec` 是调用方声明, 交叉核验只到「diff 不触 openspec/changes/」; Level 2 PR 若 proposal 早已在 master 且分支不碰 change 目录, 声明 `--no-spec` 可绕过。缓解: 声明进 audit trail (`scope_source=no_spec` + `[INFO]` 行) 可事后核对; 更强核验 待 owner 复议 #2 |
| **Risk** | R-c `post_brainstorm` / `mid_implementation` 为条件性产物, 采用方若启用且本 change 未触发, 新规则下转 missing (旧规则被他人报告掩盖)。缓解: `mid_implementation` **已在 Step 3 显式排除** (R1 rework, 与 `mid_post_spec` 同构 —— 原稿让它走 1.3(b) 不成立: (b) 只在 diff 全是 docs 时生效, 而最常见的「code diff + 进度未过 50% 阈值」仍会假红); `post_brainstorm` 见 待 owner 复议 #1 |
| **Risk** | R-d 脚本引入 subprocess (git diff / merge-base) — 与 file-scope 过滤同命令, 失败落 `git_failed` exit 2 (fail-closed), 不 crash |
| **Risk** | R-e (R1 rework 新增) 跨仓形态: 子模块 PR 时锚点面与 diff 面不同仓, 单参数会两个方向都坏 (详见 §1)。缓解: `--repo-path` / `--diff-repo-path` 分离 + 跨仓时禁用 (b) 通道 + SC-17 |

## Tasks

- [ ] **B.0 语料冻结产物** (SC-2 前置): 生成 `corpus-freeze.md` 落**本 spec 目录内**, 内容 = 取样时刻的 `.aria/audit-reports/` 全量文件名 + 每份的**独立人工标注真实归属** (change_id 或 `legacy` / `unattributed`) + 取样命令与时刻。SC-2/SC-4 的期望值从这份产物的**人工标注列**取, 固化成字面数字, **不得**由被测谓词现算
- [ ] TDD RED: `tests/test_completeness_gate.py` 先写 SC-1~SC-10 + SC-15~SC-17 (含 issue case-1 / 本仓 case-2 两条 hermetic 复现), baseline 全红
- [ ] 实现 `scripts/completeness_gate.py` (stdlib only; `--repo-path` / `--diff-repo-path` 分离 / 作用域 S1-S4 / 匹配规则含末段形态与对称排除 / 三态 / 两个排除计数 / 空集短路 / stdout 契约 / exit code; config 经 config-loader)
- [ ] 改写 `execution-modes.md` §Pre-merge: Step 3 加 `mid_implementation` 排除 + Step 4-5 + 三态输出模板 + 消费方 fail-closed 义务 + `:44`/`:82` 豁免文案统一
- [ ] audit-engine SKILL.md: 输入参数 `change_id` + fenced bash 调用块 + 配置注释 + 相关文档指针
- [ ] phase-c-integrator SKILL.md: pre_hook 传 change_id / repo_path / diff_repo_path + 4.5 三态处置 + `:157` 勘正
- [ ] **旧 schema 散文残留形态族清扫 (4 处)**: `phase-a-planner:267` / `phase-b-developer:204,277` / `phase-c-integrator:157`; 清扫后重跑 `grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` 应为 0 命中
- [ ] report-storage.md §向后兼容 + pre-write-validation.md 关联行
- [ ] AB (**两读法并集, 不取豁免**): (1) **照跑**既有相关套件验漂移 —— `audit-engine.json` (2 evals) + `phase-c-integrator.json` (3 evals) + `phase-c-integrator-pre-merge-gate.json`; (2) `audit-engine.json` 新增定向 eval id 3 + `version.yaml` bump (先查同伴撞号); (3) 经 `/skill-creator` 真跑, 结果落 `ab-results/<date>-pre-merge-completeness-gate-change-scope/`; (4) 套件缺口 issue (aria-plugin)
- [ ] 活体 dogfood: 在本仓对本 spec 自身与一个假想 id 各跑一次脚本 (SC-11), 证据抄进 handoff
- [ ] **ship 前基线重取**: `git fetch --all` + 确认主仓 `origin/master` 的 `aria` gitlink 现值 (R1 实测已是 `301641b`, 同伴 PR #202 已合), 本地 master 与 origin/master 已分叉须先对齐 —— 防止主仓同步把 gitlink 回退到 v1.70.0
- [ ] 版本 v1.71.2: aria 5 文件 + 主仓版本点 + gitlink (**无前置排队**, 原稿的「排在同伴 v1.71.1 主仓同步之后」是幻影); 归档门 (SC-12)
- [ ] Phase D: #199 / aria-plugin#161 回帖 + 关闭; F8 config 注册面缺口立 issue (含把两个 `allow_*` 键补进 DEFAULTS.json); **写侧命名约定无强制** 另立 issue (R-a 的 170 份 unattributed 是它的实证); 复议项 #1-#7 结论回写本 spec

## Success Criteria (可证伪; 每条自问「机制没实现会红吗」)

| SC | 断言 | 核验 |
|---|---|---|
| SC-1 | **hermetic case-1 (issue 复现)**: tmp 仓 (`git init -b master` —— **必须显式 `-b master`**, 现代 git `init.defaultBranch` 可能是 `main`, 否则 `--base master` 的 merge-base 解析失败落 `git_failed`; 一次 commit; feature 分支改 `openspec/changes/x/tasks.md` + `src/a.py`), **fixture 必须同时建锚点 `openspec/changes/x/proposal.md`** (否则按 S1 直接 `change_id_unanchored` exit 2, 与本条期望的 exit 1 冲突 —— R1 勘正), config `post_implementation=convergence`, 目录放 37 份 `post_implementation-R1-<ts>-other-{i}-code-reviewer.md` + 4 份 `post_spec-…-x-…`, `--change-id x` → `results` 含 `{post_implementation, x, missing}`, `verdict=fail`, exit 1, stderr/stdout 文案含 `post_implementation@x`。反事实: 把规则退回 `{checkpoint}-*.md` 通配 → 判 present → 红 | `test_completeness_gate.py::test_issue_case1_other_change_reports_do_not_count` |
| SC-2 | **hermetic case-2 (本仓文件名形态, R1 全面重写)**: fixture 语料取自 **B.0 冻结产物 `corpus-freeze.md`** (spec 目录内, 可追溯), **按名形态族穷举**, 每族至少 3 份: (F-a) 末段族 `…-{id}.md` 无 role 段; (F-b) role 后缀族 `…-{id}-{role}.md`; (F-c) `-aggregated`/`-aggregate` 族; (F-d) 无 `-R\d+-` 族 (`CONVERGED` / `FINAL` / `R5.5` / `R1prime` / `usN-mN` / `A1-` 席位前缀); (F-e) 真 2-field legacy 族; (F-f) unattributed 族 (截断/别名 id)。**期望值 = 冻结产物里的独立人工标注归属**, 逐字等值 (非 ≥1), **不得由被测谓词现算** —— 原稿写「= 清单中含 `-{id}-` 的份数」是由被测规则自身推导的**自指恒绿**, 规则漏掉多少形态它都绿 (本轮 Critical 1 正是被它放过)。**选样硬约束**: 所选 id 在 fixture 中**必须同时有 F-a 与 F-b 两族样本** —— 原稿选的 `pre-merge-gate-no-run-for-branch` 实测 72/72 份全是中缀形态、末段形态 **0 份**, 对唯一会红的形态族结构上失明。**两条反事实**: (1) 把规则 2 退回纯中缀 `-{id}-` → F-a 族少计 → 红; (2) 位置解析 (按第 4 段取 spec_id) 在 `A1-` 与 `R5.5` 形态上少计 → 红 | 同文件 `::test_real_corpus_shapes_token_bounded_match` |
| SC-3 | 有界包含排除 (F3), **三型各一 case** (R1 补后缀/中缀): (1) **前缀型** id 集 {`aria-orchestrator`, `aria-orchestrator-divestiture`} —— 只有后者的报告在场 → 前者 `missing`; 两者各有报告 → 各 `present` 且 `matched` 互不交叉; (2) **后缀型** {`gate-scope`, `pre-merge-gate-scope`} —— 只有后者的报告在场 → 前者 `missing`; (3) **中缀型** {`gate`, `pre-merge-gate-scope`} 同上。**反事实**: 谓词退回原稿的 `c'.startswith(id + "-")` 单向写法 → case (2)(3) 判 present → 红 (锁死「与被修 bug 同型的假绿」这条不变量) | `::test_bounded_containment_excludes_all_three_shapes` |
| SC-4 | **两个计数分离** (R1 重写): fixture config **明确写** `{post_spec: convergence, post_planning: convergence}` (两 checkpoint 都纳入, 消除「计数是全局还是纳入集并集」的歧义 —— 契约见 §1.4「两个计数的作用域」)。语料放: 真 2-field `post_spec-2026-04-11T0530Z.md` + `post_planning-2026-04-11T0530Z.md`; 末段形态 `post_spec-R1-2026-05-01-x.md` (x 在 `C` 内); 截断 id `post_planning-R2-CONVERGED-trunc-id.md` (`trunc-id` 不在 `C`) → `excluded_legacy_count == 2` **且** `unattributed_count == 1` **且** `unattributed == ['post_planning-R2-CONVERGED-trunc-id.md']` **且** 末段那份计入 `x` 的 `matched` (不进任何排除计数)。**反事实**: 用原稿的合并定义 (「不含任何 `-{c}-`」) → `excluded_legacy_count` 变 4 → 红 | `::test_legacy_vs_unattributed_counts_split` |
| SC-5 | not_applicable (b) **新判据** (R1 重写): diff 仅 `openspec/changes/x/proposal.md` + `openspec/changes/x/tasks.md` (Phase A-only) → `post_implementation@x` = `not_applicable/phase-a-only-no-implementation`, `verdict=pass`, stdout 含 `[INFO]` 与 `not_applicable`。**四条反事实, 每条独立断言红** (原稿只有一条 `src/a.py`, 结构上测不到 markdown 那格): (1) diff 加 `src/a.py` → `missing` + fail; (2) **diff 加 `aria/skills/audit-engine/SKILL.md`** (纯 `.md` 的处方性 Skill 变更, 落在旧 `scope_skip_paths` 的 `*.md` 里) → **必须 `missing`**, 不得 not_applicable —— 这是本轮 Critical 3 点名的那一格; (3) diff 加 `docs/x.md` → `missing` (`docs/` 亦不再豁免); (4) diff 为空 → `missing` (空集不放行); (5) 跨仓形态 `--diff-repo-path != --repo-path` 且 diff 仅 openspec → **仍 `missing`** (§1 fail-closed 条款) | `::test_phase_a_only_not_applicable` / `::test_md_and_docs_diff_still_missing` / `::test_empty_diff_is_missing` |
| SC-6 | not_applicable (c) **新判据** (R1 重写): `post_planning=convergence`。(1) change 目录仅 `proposal.md` 且该 proposal **无 `## Tasks` 小节** → `not_applicable/no-a2-artifact`; (2) 放一份 3 行 `tasks.md` → `missing` (「做了但简单」不豁免); (3) **无 `tasks.md` 但 `proposal.md` 含 `## Tasks` 内联清单 (Level 2 标准形态, `templates/proposal-minimal.md:27-31`) → `missing`, 不得 not_applicable** —— 这条是本轮 Critical 4 的红线, 缺它则每个 Level 2 change 都自动豁免 post_planning; (4) 归档态 `archive/2026-01-01-x/` 同样三分支。**反事实**: 判据退回原稿「只看两个文件是否存在」→ case (3) 判 not_applicable → 红。**自证**: 对本 spec 自身目录跑 (3) 分支 (本 spec 正是内联 `## Tasks` 无 tasks.md) 必须得 `missing`/`present`, 与头部「审计计划: post_planning convergence」一致 | `::test_post_planning_a2_artifact_includes_inline_tasks` |
| SC-7 | 作用域: 无 `--change-id`、diff 触 `openspec/changes/{a,b}/` → `scope_source=diff`, `change_ids=[a,b]`, 逐对评估, `b` 缺一项即 fail; 都不触且无 `--no-spec` → exit 2 `change_scope_unresolved`; `--no-spec` 且 diff 触 change 目录 → exit 2 `no_spec_contradicted`; `--no-spec` 合法 → 全部 `not_applicable/level1-no-spec` + `scope_source=no_spec`; `--change-id typo` → exit 2 `change_id_unanchored` (归档态 `archive/2026-01-01-x/` 也算锚) | `::test_scope_resolution_matrix` |
| SC-8 | Step 3 枚举 (R1: 补 `mid_implementation` 与排序契约): config `{post_spec: convergence, post_planning: on, mid_post_spec: convergence, mid_implementation: convergence, post_closure: convergence, pre_merge: challenge, post_implementation: off}` → `checked_checkpoints == ['post_planning', 'post_spec']` (**`sorted()` 字典序**, §1.4 已定义, 消除「config key 序 vs sorted」的实现歧义; 字符串 `on` 纳入; `off` 与**四个**排除项 `pre_merge`/`post_closure`/`mid_post_spec`/`mid_implementation` 不纳入)。**注**: 本 fixture 不含 `post_brainstorm` 键 —— 待 owner 复议 #1 无论怎么裁, 本条断言都不变; #1 的两个分支各自的 SC 见 SC-18 | `::test_step3_enumeration` |
| SC-9 | 豁免 **三路全断言** (R1 补 S4-bypassed + 文案对齐): (1) `allow_incomplete_checkpoints=true` + 一项 missing → `verdict=bypassed`, exit 0, `bypassed=true`, 文案逐字含 `[WARN] incomplete checkpoint gate bypassed: missing=` (**与 `execution-modes.md:82` 同字面** —— 原稿造的 `bypassed by config: missing=` 是 SOT 两种拼法之外的第三种, 已删); (2) **S4-bypassed**: 同旗标 + 无法解析作用域 → `verdict=bypassed`, exit 0, `error_kind=null`, `scope_source=null`, `change_ids=[]`, `results=[]`, 文案含 `scope_unresolved=1`; (3) 同旗标下 `change_id_unanchored` 仍 exit 2 (`verdict=error`) | `::test_bypass_semantics` |
| SC-10 | 契约: 四种 verdict 下 stdout 均可 `json.loads`, 顶层键集逐字 = 1.4 列表 (含新增的 `unattributed_count` / `unattributed`), `results` 恒 list; `--base` 缺失 → argparse exit 2; 坏 config JSON → `config_unreadable` exit 2 | `::test_stdout_contract` |
| SC-11 | **活体**: 在本仓 (post_spec 审计 CONVERGED 后) `--change-id pre-merge-completeness-gate-change-scope --base master` → post_spec `present` (**≥6**: R1 五席 + 聚合各 1 份, 实测该 6 份文件名全为 role/aggregated 后缀族) 且 post_planning **`present` 或 `missing`** —— **不得**是 `not_applicable/no-a2-artifact` (本 spec 有内联 `## Tasks`, 见 SC-6 case 3; 原稿把 `not_applicable` 写进期望是 Critical 4 的自钉恒绿); 另断言 `unattributed_count > 0` 且 `unattributed` 非空 (本仓真实语料实测 170 份, 用来验证 R-a 显影确实工作); 假想 id `zz-not-a-change` → exit 2 `change_id_unanchored`; 输出抄进 handoff。此为手动 dogfood (F1: 本仓 pre_merge off, 生产不会调) | 命令 + handoff 证据 |
| SC-12 | 既有测试全绿: `cd aria/skills/audit-engine/tests && python3 -m unittest discover -s . -p 'test_*.py' -v`; 跨 skill 消费方 `cd aria/skills/state-scanner/tests && python3 -m unittest discover -s . -p 'test_*.py'` (collectors/audit.py 语料测试) 与 `aria/skills/phase-c-integrator/tests` 同命令 — 三者 0 failure; 归档门对本 spec `spec_complete.py` 判 `completeness_gate.py` alive (SKILL.md bash 块, F7), 无 dead-code block | 命令 |
| SC-13 | 文档机检 (R1 勘正): `grep -c '{checkpoint_name}-\*\.md' execution-modes.md` = 0; `grep -c 'completeness_gate.py' audit-engine/SKILL.md` ≥ 1 且命中行在 ```` ```bash ```` 块内; `grep -c 'change_id' phase-c-integrator/SKILL.md` 较基线 +≥1; **`grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` = 0 命中** (四处残留全清, 非只 `phase-c-integrator:157`); `grep -c '不计入' report-storage.md` ≥ 1; `execution-modes.md` 内 `bypassed` 两处文案逐字相同; **调用串机械护栏 = 计数恰 2** (`grep -c 'completeness_gate.py' ` 在 SKILL.md fenced bash 块与 execution-modes.md 各 1, 照 `execution-modes.md:152` 竞品探针「SC-17 计数恰 2」先例) —— 原稿写「三份文件的调用串逐字相同」不可执行: §1 只规定**两处**调用串, §3 给 phase-c-integrator 的是参数与 4.5 处置、不含调用串 | grep |
| SC-14 | Rule #6 **两读法并集** (R1 改写): (a) **照跑既有套件** —— `audit-engine.json` (2 evals) + `phase-c-integrator.json` (3 evals) + `phase-c-integrator-pre-merge-gate.json` 各跑一次 with/without 臂, 结果落 `ab-results/`, 无回归; (b) **定向 fixture** —— eval id 3 登记进 `audit-engine.json` (descriptive 形态: 给定目录清单 + config + change_id, 要求写出调用命令行、三态逐对结果、`[INFO]`/`[WARN]`/ERROR 措辞; expectations 含「不得把其它 change 的报告当证据」「末段形态 `…-{id}.md` 必须计入」「not_applicable 必须 surface」三条) + `version.yaml` bump; 真跑一次, 回退本 spec 后该 eval 的 with 臂应转差 (可证伪实证写进 ab-results README); (c) **套件缺口 issue** 号写回本 spec | 文件 + issue |
| SC-15 | **空集短路** (R1 新增, 原稿无此格): config 为 `{}` / 无 `audit` 块 / 文件不存在 三种 fixture → `checked_checkpoints == []` 且 `verdict=error`, `error_kind=no_checkpoints_configured`, exit **2**, 文案含「零证据不当正证据」。**反事实**: 去掉短路 → 变 `verdict=pass` exit 0 → 红。另一格: 旧配置 `{experiments: {agent_team_audit: true, agent_team_audit_points: ['post_spec','pre_merge']}}` 且无 `audit` 块 → 经 config-loader 兼容映射后 `checked_checkpoints == ['post_spec']` (**非空**), 证明未绕过映射; 反事实: 直读 `.aria/config.json` 的实现 → 空集 → 红 | `::test_empty_checkpoint_set_short_circuits` / `::test_legacy_config_mapping_via_loader` |
| SC-16 | **`mid_implementation` 排除** (R1 新增): config `{mid_implementation: convergence, post_spec: convergence}`, diff 含 `src/a.py` (**非** docs-only, 即旧 (b) 通道不生效的最常见形态), 目录只有 post_spec 报告 → `checked_checkpoints` **不含** `mid_implementation`, `verdict=pass`。**反事实**: 不加排除条款 → `mid_implementation@x = missing` + fail → 红 (阈值未触发的合法不产出被当缺失) | `::test_mid_implementation_excluded` |
| SC-17 | **跨仓执行上下文** (R1 新增): 造主仓 tmpA (含 `.aria/audit-reports/` + `openspec/changes/x/`) 与子模块 tmpB (无 `openspec/` 无 `.aria/`, diff 含 `skills/foo/SKILL.md`)。(1) `--repo-path tmpA --diff-repo-path tmpB --change-id x` → 锚点解析成功 (不报 `change_id_unanchored`)、报告在 tmpA 找、diff 取自 tmpB; (2) 缺省 `--diff-repo-path` 时等于 `--repo-path` (向后兼容); (3) 跨仓时 (b) 通道禁用 (见 SC-5 case 5)。**反事实**: 单参数实现传 tmpB → exit 2 `change_id_unanchored` → 红; 传 tmpA → diff 取错仓, (b) 误判 not_applicable → 红 | `::test_split_repo_and_diff_paths` |
| SC-18 | **复议项可证伪化** (R1 新增, 防「owner 裁完仍无测试证伪」): 待 owner 复议 #1 (`post_brainstorm` 排除) 两个分支各配一条 case —— 采纳: config 含 `post_brainstorm: convergence` → `checked_checkpoints` 不含它; 不采纳: 含它且零报告 → `missing` + fail。Phase B 按 owner 裁决**只保留其一**并删掉另一条, 不得两条都不写 | `::test_post_brainstorm_exclusion_decision` |

## rule6_note (Rule #6 — 判据表第三行, SOT `standards/conventions/skill-benchmark-exemption.md` §2-§3)

> **R1 rework 说明**: 档位本身在 post_spec R1 出现 **1 席判第二行 / 2 席判第三行**的分歧 (双方对事实无分歧: 套件 2 evals、关键词零命中, 三席实测一致; 分歧在「套件覆盖外」的解释)。本 spec **不靠裁决取豁免**, 改为**执行两读法的并集** —— 第二行要求的「照跑」和第三行要求的「三义务」全做。档位标签本身仍列 待 owner 复议 #5, 但无论怎么裁, Phase B 的动作集不变。

- **处方性 · 运行时指令面 (第二行动作: 照跑, 零裁量)**: `execution-modes.md` §Pre-merge Step 3-5 + 三态模板 + 消费方 fail-closed 义务; `audit-engine/SKILL.md` 调用块与 `change_id` 参数; `phase-c-integrator/SKILL.md` pre_hook 4/4.5。**照跑面 (R1 补全, 原稿只算了 audit-engine 一个套件)**: `ab-suite/audit-engine.json` (文件内 `version` 1.0.0, 2 evals) + `ab-suite/phase-c-integrator.json` (3 evals) + `ab-suite/phase-c-integrator-pre-merge-gate.json` —— 后两个**实存**且本 spec 改其处方面 (pre_hook 步骤 4/4.5), 原 rule6_note 对它们零评估, 这是**独立于档位分歧的漏评点**, 无论裁决如何都要补。
- **第三行三义务 (同时做)**: (1) 点名行为 — A. 编排者在 pre_merge 入口用**被审 change 的作用域**调用 `completeness_gate.py` 并按三态路由, 不再把「目录里有同 checkpoint 报告」当通过; B. `not_applicable` 必须以 `[INFO]` 行 surface 其机械依据, 不得折叠进「校验通过」; C. `unattributed_count > 0` 时必须以 `[WARN]` 行列出文件名。**为什么现有套件测不到**: `audit-engine.json` 的 2 evals 全是 per-round 竞品探针场景 (id 1 sibling_found 渲染 / id 2 not_established 措辞), 无一进入 pre_merge gate (`grep -ic 'completeness\|missing_checkpoint\|allow_incomplete'` = 0)。(2) 定向 fixture — eval id 3 (SC-14b), 可证伪: 回退 SOT 后 with 臂对 A/B/C 三 expectation 应失分; (3) 套件缺口 — aria-plugin 立 issue「audit-engine AB 套件零覆盖 pre_merge completeness gate」(Phase D 任务; SOT §3 第 3 条要求成文缺口 —— 「套件的盲区是债, 不是豁免理由」)。同族先例走第三行且三义务齐备: `archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:282-284` (缺口挂 aria-plugin#127)。
- **描述性 / 纯代码** (脚本 / 测试 / report-storage 注 / 四处 `{timestamp}` 勘正 / CHANGELOG): substitute = SC-1~SC-10 + SC-13 + SC-15~SC-17。`description` 字段零变动。

## 待 owner 复议

1. **Step 3 是否追加排除 `post_brainstorm`** (R-c): 它与 `mid_post_spec` 同为条件性产物 (brainstorm 是 A.0.5 可选, `audit-engine/SKILL.md:60`), 且其产物 (`docs/decisions/DEC-*` / `.aria/brainstorm-*`) 与 change_id 无机械关联。**推荐默认: 追加排除**, 理由与 `:51-52` #79 条款同构 (「启用即会误阻」)。**R1 勘正**: 原文写「不采纳则 SC-8 的排除集少一项」不成立 —— SC-8 的 fixture config 本就不含 `post_brainstorm` 键, 两个分支都不改 SC-8。两分支各自的可证伪断言已补进 **SC-18**, owner 裁完 Phase B 只保留其一。**注**: `mid_implementation` 已不在本条范围 —— 它在 R1 rework 中直接排除了 (与 `mid_post_spec` 同因同构, 见 §1.3), 不作为复议项。
2. **`--no-spec` 交叉核验强度** (R-b): 现设计 = 「diff 不触 `openspec/changes/**`」。可选加固: 同时要求 `refs/aria/coordination` 无本容器 active claim 指向某 spec dir (需读 state-scanner claim 契约, 跨 skill 依赖)。**推荐默认: 本 spec 不加固**, 声明进 audit trail 可事后核对; 加固另案。
3. **可配置下界 N** (issue 修法 3, 候选 C): **推荐默认: 不做**, 按 change 收窄后 N=1 即「≥1 份属于本 change」; 若要, 需先补 F8 的 audit 段 config 注册面。
4. **版本号**: PATCH v1.71.2 (SOT 规程 + 脚本, 无新 Skill)。若同伴容器先占 v1.71.2, 顺延 (bump 前 ls-remote tags)。`ab-suite/version.yaml` 的**套件**版本同理 (与在飞轨 `a1-entry-claim-duplicate-work-guard` 同面, 见 §4)。

**以下三条为 post_spec R1 审计留下的 conflicted / 分歧项 (R1 rework 新增)**:

5. **Rule #6 档位标签** (`d94ee0bc` vs `55a7db0e`, 1 席 vs 2 席): 走判据表第二行 (处方性·运行时指令面 ⇒ 照跑 AB, 零裁量) 还是第三行 (套件覆盖外 ⇒ substitute + 三义务)。双方对事实无分歧, 分歧在「套件覆盖外」是指「本轮套件没有 eval 到达该状态」(第三行成立, 有归档先例 `2026-08-23-pre-merge-gate-no-run-for-branch:282-284`) 还是「只有结构性不可测才算, 覆盖缺口应照跑并补」(第二行, SOT §2 附加约束「指令流程变动 ⇒ 一律第二行」)。**本 spec 的处置: 不等裁决, 两读法并集执行** (照跑三个既有套件 + 补定向 fixture + 缺口 issue), 故裁决不改变 Phase B 动作集, 只影响 rule6_note 的标签写法。**推荐默认: 保留第三行标签 + 并集执行**。
6. **§1.3(c) 判据口径** (`4e504aa5` vs `368b926b`, conflicted): 两侧量的不是同一件事 —— code-reviewer 量「已有 post_planning 报告却被判 not_applicable」的**已观测误放** = 0 例; backend-architect / knowledge-manager 量「A.2 确已执行但产物内联 ⇒ 判据说未执行」的**结构性入口** = 每个 Level 2 change。两组数字不互斥 (那些 change 本就没跑 post_planning, 不会进 code-reviewer 的反例集)。**本 spec 的处置: 已按 fail-closed 方向改成「任何 A.2 产物 (含内联 `## Tasks`)」** —— 收窄豁免面在 Rule #10 下永远是安全侧, 不需等裁决; 若 owner 认为「内联 Tasks 也不算 A.2 产物」, 那是**放宽**豁免面, 须由 owner 明示 (AI 不得自行放宽)。
7. **§1.3(b) 是否保留任何 diff 类 not_applicable 通道** (`8c7972ce`): R1 已把基于 `scope_skip_paths` 的原判据**删除**, 换成「Phase A-only PR」(与 issue 报告方独立论证放行的那格同义)。knowledge-manager 更进一步认为 (b) **没有合法触发场景** (文档型 diff 下 post_implementation 仍会照跑并产出报告 ⇒ 命中 present, (b) 唯一被触发的时刻就是「本该跑却被跳了」)。**推荐默认: 保留改写后的 (b)** —— 它对应 issue 里真实发生过的 Phase A-only PR 场景, 且 SC-5 的五条反事实把放行面钉死; 若 owner 认同「零合法触发场景」的论证, 则整条 (b) 删除, SC-5 相应改为「Phase A-only 亦 missing」。两分支都不影响其余条款。

## References

- SOT (@`301641b`): `aria/skills/audit-engine/references/execution-modes.md:23-82,37-38,44,51-52,82,152,185` · `audit-engine/SKILL.md:47-54,75-81,105,123-125,381-388,403-419` · `references/report-storage.md:8-39` · `references/pre-write-validation.md:11-31` · `references/report-format.md:5` · `phase-c-integrator/SKILL.md:126-157,252-265,299` · `phase-c-integrator/scripts/path_coverage.py:1-50,547-549` · `agent-team-audit/references/audit-points.md` (checkpoint 触发定义) · `state-scanner/scripts/collectors/audit.py:52-114` (文件名 token 解析先例) · `state-scanner/scripts/lib/spec_complete.py:924-930` (liveness 分类; **该行号只对 `301641b`**, @`0545f86` 是 `:903`) · `config-loader/DEFAULTS.json:118-123` (`scope_skip_paths` 缺省; audit 键集**不含**两个 `allow_*`) · `config-loader/SKILL.md` §旧配置兼容层 (`experiments.agent_team_audit` ⇒ `checkpoints.*=convergence` 映射) · `phase-a-planner/SKILL.md:250,267` · `phase-b-developer/SKILL.md:204,277` (旧 schema 散文残留)
- 规范: `standards/conventions/skill-benchmark-exemption.md` §2-§3 (Rule #6; `:25-33` 判据表 + `:35` 附加约束) · `standards/conventions/configured-gate-authority.md:28-40` (Rule #10 白名单第四类及其边界) · `standards/openspec/project.md:114-118` (Level 2 = proposal.md only, tasks.md 属 Level 3) · `standards/openspec/templates/proposal-minimal.md:27-31` (Level 2 模板自带内联 `## Tasks`)
- 先例: `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md` (同类 Level 2 标杆; `not_applicable` 语义封闭集 §Why `:55-57`「归进 not_applicable = fail-open, 污染 #122 钉死的语义封闭集」—— 本 spec 的 (b)/(c) 收窄与该裁定同向; `:282-284` 第三行三义务先例) · `openspec/archive/2026-09-04-sibling-spec-probe/` (audit-engine 脚本 + stdout 契约 + 消费措辞三档形态) · `openspec/archive/2026-07-31-phase-c-gate-path-coverage-not-applicable/` (#122 not_applicable 原始定义)
- 现场: Aria#199 issue 原文 · `.aria/triage-comment-199.md` / `.aria/triage-report-199.json` (2/2 复现) · aria-plugin#161 · aria-plugin#127 (第三行先例) · 本仓语料统计 (F2/F3/F4 数字 = **R1 rework 时 python 全枚举**, 786 份 `.md` / `C`=152)
- 审计: `.aria/audit-reports/post_spec-R1-2026-09-06T155000-000Z-R1-pre-merge-completeness-gate-change-scope-{aggregated,tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md` (R1 五席 + 聚合)
