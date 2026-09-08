---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T16:03:43.101Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [backend-architect]
---

# post_spec 审计报告 — pre-merge-completeness-gate-change-scope (Round 1, backend-architect)

## 核验基线

- aria 子模块 `origin/master` = `301641b` (v1.71.1), 与插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` 逐字比对: `execution-modes.md` / `audit-engine/SKILL.md` / `phase-c-integrator/SKILL.md` / `collectors/audit.py` 四文件 **IDENTICAL** ⇒ proposal.md:9 的冻结声明成立, 本报告行号与其同基线。
- 本席位所有数字均为实测 (`/home/dev/Aria/.aria/audit-reports/` 778 份 `.md` + `openspec/changes` 9 + `openspec/archive` 143 目录), 未采信 proposal 自述。
- 复核为真的自述 (逐条实测通过, 不再单列): F1 (`.aria/config.json` `pre_merge=off` / `post_planning=convergence`) · F2 计数 (post_spec 24 / post_planning 2 / pre_merge 1 / mid_implementation 1 份不匹配 `-R\d+-`) · F3 前缀碰撞对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`, 恰 1 对) · F5 (`path_coverage.py:8` not_applicable 定义 + `phase-c-integrator/SKILL.md:265` surface 义务) · F6 (`SKILL.md:403-419` file-scope + DEFAULTS `scope_skip_paths` = `deploy/ docs/ .forgejo/workflows/ .github/workflows/ *.md`, 故 SC-5 的 `openspec/changes/x/proposal.md ⊆ skip_paths` 经 `*.md` 后缀项成立) · F7 (`spec_complete.py:924-930`) · F8 (template 无 audit 块; DEFAULTS audit 键集无两个 allow_*) · §5 零代码消费方 (`grep --include=*.py/json/yaml` 零命中) · case-2 计数 (499/209/3) · SC-13 三个 grep 基线均非零 (2 / 3 / 0, 可证伪)。

## 审计结论

### Decisions

- [critical] architecture/proposal §1.2 归属规则第 2 条 (子串边界): 规则要求 `f` 含 `-{change_id}-`, 但真实语料把 spec_id 放**末段** (`…-{id}.md`, 无 agent_role 后缀) 的有 62 份, 覆盖 **25 个** (checkpoint, change_id) 组合的**全部**自有报告 (`mid=0`), 含两个**活跃** change: `aria-2.0-m6-release-closeout` 9 份 post_spec、`aria-2.0-m6-e2e-resilience` 1 份 → 新规则一律判 `missing` = 假红阻断。修法: 边界取 `("-" + f[:-3] + "-")` 内找 `-{id}-`, 把 `.md` 也当右边界。(证据: proposal.md:98,101,186; 实测 `.aria/audit-reports/` 例 `post_spec-R2-qa-2026-05-25-aria-2.0-m6-release-closeout.md`)
- [critical] architecture/proposal §1.3(c) `not_applicable/no-a2-artifact`: Level 2 的 A.2 产物**内联在 proposal.md 的 `## Tasks` 段** (模板 `standards/openspec/templates/proposal-minimal.md:28`; `standards/openspec/project.md:118` 只对 Level 3 要求 tasks.md), 结构上不产 `tasks.md`/`detailed-tasks.yaml` ⇒ 判据对**每个 Level 2 change 恒成立**, 把本仓已 enabled 的 post_planning 自动豁免。本 spec 自己就是这形态 (proposal.md:168-179 有 11 条 Tasks、无 tasks.md, 而 :13 声明 post_planning 会跑) —— 自相矛盾。实证: 2026-07-04 (post_planning enabled 日) 后归档的 9 个 Level 2 change 全部零 A.2 文件、零 post_planning 报告, 抽查 3 个 proposal 各有 11/13/12 条内联 checkbox (含 `2026-08-21-subprocess-decode-hardening/proposal.md:114` 「A.2 细化为 detailed-tasks.yaml; 此处为骨架」)。对象存在而非不存在 ⇒ 落在 `configured-gate-authority.md:40` 明禁的那一侧。(证据: proposal.md:110,190)
- [major] architecture/proposal §1.2 归属规则第 3 条: 最长匹配排除只写了 `c'.startswith(change_id + "-")` (前缀型)。后缀型 (`c'` 以 `-{id}` 结尾) 与中缀型 (`c'` 含 `-{id}-`) 同样使别人的报告被算成自己的 —— **假绿方向**, 正是本 spec 要根治的失效。实测当前 152 个 id 里后缀/中缀对为 **0** (故是潜在缺陷, 非现存实例), 但判据应写成对称的有界包含; SC-3 亦只测前缀。(证据: proposal.md:99,187)
- [major] implementation/proposal §1.2·§1.4 `excluded_legacy_count`: 定义「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」并不等于「旧 schema」。本仓按该口径 = **238** 份, 其中真正的 2-field legacy (`{checkpoint}-{timestamp}.md`) 只有 **6** 份 (如 `post_planning-2026-04-11T0530Z.md`), 另 62 份是上面的末段形态、176 份是 id 不在 `C` (截断/改名/子任务, 如 `post_planning-R2-CONVERGED-dispatch-input-delivery.md`、`post_spec-2026-04-28T1700Z-us022-m2-layer1.md`)。R-a 的缓解「`excluded_legacy_count` 显影」因此失效 —— 一个 238 的数字既不指向 schema 问题也不指向文件; SC-4 只造 2 份恒绿。建议拆 `excluded_legacy_count` (真 2-field) 与 `unattributed_count` (有 id 段但不在 C, 列名进 audit trail)。(证据: proposal.md:101,163,188)
- [major] architecture/proposal §1 config 读取 + §1.4 空集: 脚本规定直读 `<repo>/.aria/config.json`, 绕过 SOT 两处明写的 config-loader (`execution-modes.md:37-38` Step 1、`phase-c-integrator/SKILL.md:130` 步骤 1)。config-loader 的语义包含**旧配置兼容映射** (`config-loader/SKILL.md:305-331`: `experiments.agent_team_audit=true` 且**无 audit 块** ⇒ `audit.enabled=true` + `agent_team_audit_points` 逐项映射为 `checkpoints.*="convergence"`, 含 `pre_merge`)。这类采用方在直读下 `audit.checkpoints` 整个缺失 ⇒ `checked_checkpoints=[]` ⇒ `verdict=pass` **零证据判绿**, 与本 spec 要根治的失效同型; 而 §1.4 对空 diff 写了「空集不放行」(1.3 missing), 却没有对空 `checked_checkpoints` 的同款短路。(证据: proposal.md:76,111,117)

### Issues

- [minor] documentation/Rule #6 判定 · rule6_note · Why 根因 2 的引用: (a) 称固定套件为 `ab-suite/audit-engine.json` **v1.3.0** —— 实测该 json 自身 `version` = `1.0.0`, 套件 `ab-suite/version.yaml` = `1.4.0` (§4 表里的 `1.4.0 → 1.5.0` 才对); 「仅 2 evals 且全是竞品探针场景」的实质判断实测为真 (id 1 sibling_found 渲染 / id 2 not_established 措辞, `grep -i completeness|missing_checkpoint|allow_incomplete` 零命中)。(b) `phase-c-integrator/SKILL.md:137` 引作「context = PR diff」, 实际在 `:136`, `:137` 是「5. 处理 verdict」; §3 的改动区间 `:133-137` 同此偏移。(证据: proposal.md:11,40,202)
- [minor] testing/SC-13: 「三份文件的调用串逐字相同」与 §1「SKILL.md fenced bash 块 + execution-modes.md **各一份**」矛盾 —— §3 给 phase-c-integrator 的是 `change_id` 与 4.5 处置, 不含调用串, 故不存在第三个比对对象, 该子断言不可执行。建议照 `execution-modes.md:152` 竞品探针的先例写成「机械护栏计数恰 2」。(证据: proposal.md:68,135,197)
- [minor] testing/SC-9: §1.1 把 `allow_incomplete_checkpoints` 的豁免面从既有的 missing (`execution-modes.md:42-44,82`) 扩到 S4 `change_scope_unresolved`, 但 SC-9 只断言「missing → bypassed」与「同旗标下 unanchored 仍 exit 2」, S4-bypassed 这一路 (verdict/scope_source/error_kind 各取何值) 无断言。(证据: proposal.md:89,193)

### Risks

- [major] architecture/§1.2 第 3 条的后缀·中缀碰撞 (同上 Decisions 第三条, 现为潜在风险: 当前语料 0 实例, 随新 change 命名随时可现)。
- 观察 (不计 finding): §1.1 S2 从 `git diff` 取 `openspec/changes/<id>/` 前缀时, Phase D 归档分支上被 `git mv` 走的旧 change 目录同样以旧路径出现在 `--name-only` 里, 会把已归档 change 拖进作用域。§3 规定 phase-c 显式传 `change_id` (走 S1) 后此路少用, 但若 C-1 未修, 老 change 的末段形态报告会在这条路上叠加成假红。
- 观察 (不计 finding): §1.3(b) 引 `audit-engine/SKILL.md:105` 作「diff 类 = {mid_implementation, post_implementation}」, 该行实际列三项 (含 pre_merge); 因 Step 3 已排除 pre_merge, 集合等价, 不影响判定。

## Verdict

**FAIL** — Critical 2 / Major 3 / Minor 3。

rationale: 两条 critical 都落在**判据本体**而非表述: (1) 归属谓词的连字符边界对本仓 62 份真实报告判错 (25 个组合的自有报告全数落空, 含 2 个活跃 change), 而 SC-2 的「冻结 40 个真实形态」按 timestamp/round/role 三段的变体选样、SC-11 的活体 dogfood 又只跑当前写法 (最近 12 份报告实测均为完整 5-field), **两条 SC 都测不到这个形态** ⇒ 全绿而规则错; (2) `no-a2-artifact` 判据把「Level 2 的 A.2 产物内联」误读成「A.2 未执行」, 给本仓已 enabled 的 post_planning 造了一条自动豁免通道 —— 一份修「误放」的 spec 自己新开了一个误放口, 且 SC-6 把它钉成绿。按横切原则「数据可用性 (Aria #54)」的 verdict 载重条款, 语料核实与断言不符必须 REVISE/FAIL, 故本席位判 FAIL。

方向本身 (机械执行器 + 按 change 收窄 + 三态 + fail-closed 契约 + 零新增 config 键) 站得住, 候选方案 A/C/D 的否决理由经核也成立; 上述两条 critical 是判据边界问题, 不需推翻方案 B。

## 轮次记录

### Round 1

- Agents: backend-architect (五席之一, 本报告仅本席位视角)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 8 (Critical 2 / Major 3 / Minor 3)
- Vote: REVISE
