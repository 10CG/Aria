---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-10T17:26:18.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead]
---

# post_spec R3 单席报告 — tech-lead (架构与范围透镜)

本席为 Round 3 新席位, 不继承 R1/R2 结论。所有事实断言均对真文件实读 / 实跑核验后写入; proposal 自述一律不采信。行号: 被审 proposal 用当前工作树; SOT 用插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b`)。

**先说结论**: 方案本体 (机械执行器 + 三态 + 显式 change 作用域) 在架构上成立, 两层根因都有落点, 消费方接缝零破坏, 同伴在飞面无越界。R2 的 2 Critical + 9 Major 全部落进正文。但 **R2 两条修复各自新写的文本里各留了一个新失效**, 且都在「零证据判绿 / 无逃生口硬阻」这条本 spec 自己要封的轴上 —— 与 memory `feedback_multiround_audit_catches_fix_introduced_regression` 同型。另有一条 2026-09-10 基线复核行未回灌下游, 会让 Phase B 照单把版本号写回已被越过的 v1.71.2。

---

## 审计结论

### Decisions

- [minor] architecture/§Why 两层根因与候选方案取舍: 两层根因经 SOT 实读成立 —— `execution-modes.md:46-65` Step 3-5 全节无 change 维度、`:64` 「missing 为空即通过」; `audit-engine/SKILL.md:49-54` 输入参数表只有 checkpoint/mode/context/agents_config; `phase-c-integrator/SKILL.md:136` 传 `context: PR diff (branch_name vs base)` 而 `phase-a-planner/SKILL.md:250` 传 `openspec/changes/{spec_id}/proposal.md`。方案 B 对两层各有落点, 非治标; A (纯散文) / C (可配置下界 N) / D (frontmatter 归属) 的否决理由逐条成立 (证据: `execution-modes.md:46-65`, `audit-engine/SKILL.md:49-54`, `phase-c-integrator/SKILL.md:136`, `phase-a-planner/SKILL.md:250`)
- [minor] architecture/§5 消费方接缝: 「只读文件名, 不改 writer schema」成立。`collectors/audit.py:52` `_AGGREGATE_SUFFIXES` 只挑 `-aggregated.md`/`-aggregate.md`; `:62-69` `_CHECKPOINT_PREFIX = ^[^-]+-` + `"-" + name[m.end():]` 确实只合成**首**连字符做左界 —— F2 引它作「不假设尾段存在」的先例准确。`aria-dashboard/references/parse-rules.md:79` 是 `Glob ".aria/audit-reports/*.md"` + 文件名前缀 fallback, 与新门无写侧交集。`spec_complete.py:924-930` 逐字: `SKILL.md` 内有真 bash 调用才 alive, 其余 `.md` 一律 prose ⇒ F7 对「调用行必须落 SKILL.md fenced bash 块」的推论正确 (证据: `collectors/audit.py:52,62-69`, `parse-rules.md:79-103`, `spec_complete.py:924-930`)
- [minor] architecture/同伴在飞面与 ship 顺序: 无越界。当前 `openspec/changes/` 8 轨, 唯一带「代码落点」行的并发轨 #195 落在 `state-scanner/collectors/handoff_multibranch.py` / `scan.py:186`, 与本 spec 触点零交叠 (§4 该判断成立)。全仓 `grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` 实测**恰 4 处** = `phase-a-planner:267` / `phase-b-developer:204,277` / `phase-c-integrator:157`, 与 §4 逐字一致。`ab-suite/version.yaml` 现值仍 `1.5.0` (`last_modified: 2026-09-05`) ⇒ 目标 1.6.0 未被占, R2 的 5/5 撞号缺陷已真解。gitlink 已对齐: 主仓 `fe703c5`, `git submodule status aria` = ` f314785…` 无 `+` 前缀, `git -C aria rev-parse HEAD master origin/master` 三者同值 (证据: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md:11`, `ab-suite/version.yaml:1`, `git submodule status`)
- [minor] documentation/R2 缺陷处置落地核验: 2 Critical + 9 Major **11 条全部落进 proposal 正文** (非批注)。逐条复算成立的有: §1.4 stdout 顶层键集实数 **15 项**; `find skills/config-loader -name '*.py'` = **0** 且 `SKILL.md:8-10` 为 `user-invocable:false` / `allowed-tools: Read, Glob`; 三份 AB 文件结构 (`audit-engine.json` v1.0.0 / 2 evals / completeness 关键词 0 命中, `phase-c-integrator.json` 3 evals, `phase-c-integrator-pre-merge-gate.json` `type=workflow_skill_subextension` / 无 `evals` 键 / 8 fixtures / `issue=10CG/Aria#60`, 全 32 文件 `sum(len(evals))=84`); `config-example.md` 场景 A `:381-400` / B `:402-417` / C `:419-440` 行号与内容; `DEFAULTS.json` audit 八 checkpoint 全 `off`、无两个 `allow_*` 键; 主仓 16 个版本字符串点逐点复算 (`README.md:8,242` + `README.{zh,ja,ko}.md:3,10,244` + `VERSION:24` + `CLAUDE.md:139,141` + `system-architecture.md:189` + `version-scheme.md:23`)。残留缺陷只出现在 `ca4cd11f` 与 `b9e07647` 两条修复**新写的文本**里 (证据: `proposal.md:194`, `config-loader/DEFAULTS.json`, `ab-suite/*.json`, `config-example.md:381-440`)

### Issues

- [critical] architecture/§1.3 Step 3 优先级链 · Level N 取法: Level 谓词未对真实数据值域验证, 而它是 R2 Critical `ca4cd11f` 修复新引入的**必经输入**。对本仓 153 份 `proposal.md` 实跑 `Level\s*\**\s*[:：].*?([123])`: (1) **9 份零命中** (如 `archive/2026-06-10-handoff-frontmatter-enforcement/proposal.md`, 全文只有 Status 行里的「Level 2 链路」无冒号) ⇒ `error_kind=spec_level_undetermined` exit 2, 而 §1.1 (`:97`) 的豁免面只列 S4 / missing, 该 error_kind **不在其中** ⇒ 与刚被判 Critical 的 `fdb30703`「无逃生口硬阻」同结构; (2) **15 份**首命中行是 `Spec Level:` 而非 `Level:` —— 散文只写「头部 Level 行」, 按字段名实现 (`^>\s*\*\*Level\*\*`) 会全部漏掉; (3) 首命中行号分布 **2–58**, **6 份 >20 行、2 份 >30 行**, 其中 `archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:58` 是四天前刚归档的当代 proposal ⇒ 「头部」按任何窗口实现都判 exit 2 硬阻, 按无锚正则实现则解析成功 —— **同一份 SOT 两种实现判决相反**, 正是 §1.2b 为子目录边界成文时给出的那条理由, 在此未闭合 (仓内 `parse-rules.md:83` 的「前 30 行」窗口先例也覆盖不了)。SC-20(3) (`:300`) 只锁「无 Level 行 ⇒ exit 2」, 对窗口与字段名两条边界零覆盖 (证据: `proposal.md:156,97,300`; 实跑 153 份 proposal 语料)
- [critical] architecture/§1.1 S3 交叉核验 · §1 跨仓 fail-closed 条款: `--no-spec` 的唯一机械守卫在本项目主力场景下**结构性真空**。S3 (`:94`) 的核验是「diff 不触 `openspec/changes/**`」, 而 diff 面按 `:81` 恒取自 `--diff-repo-path`; 实测 `test -d aria/openspec` 与 `test -d aria/.aria` **两项皆假** ⇒ 子模块 PR (proposal `:82` 自述「子模块 PR 正是本项目 pre_merge 的主力场景」) 下该谓词**恒真**, 调用方误判 Level 1 传 `--no-spec` 无任何机械阻力, 结果是**全部**纳入校验的 checkpoint 记 `not_applicable/level1-no-spec` = 整门旁路 —— 比 (b) 通道宽一个量级的假绿通道。§1 (`:83`) 的跨仓 fail-closed 条款只禁 (b), 对 (a) 零条款; SC-17 (`:297`) 只测锚点/报告/diff 三面路由与 (b) 禁用, 无跨仓 `--no-spec` 格 ⇒ 无 SC 能证伪。R-b (`:253`) 把它记为「交叉核验只到 X」(强度有限), 复议 #2 (`:315`) 据此推荐「本 spec 不加固」—— owner 将在「守卫有部分强度」的错误前提上做裁决, 而在主力场景它的强度是 0 (证据: `proposal.md:94,83,81,82,253,297,315`; `test -d aria/openspec` = 假)
- [major] documentation/头部基线复核 `:16` vs §4 `:229` / Tasks `:274` / 复议 #4 `:317`: 2026-09-10 的基线复核只改了头部, 未回灌下游。(1) `:16` 声明「PATCH 候选改为 **v1.73.1**」, 但 `:229` §4 同步表 / `:274` Tasks 版本项 / `:317` 复议 #4 三处仍写 **v1.71.2** —— 该号已被 v1.72.x / v1.73.0 越过, Phase B 照 Tasks 照单执行即写回退版本号。(2) `:16` 的「实测 diff 输出为空 …… 没有一个落在本 spec 的触点上 ⇒ 本文全部行号在 `f314785` 上继续有效」实测为假: `git diff --name-only 301641b f314785` 含 `CHANGELOG.md` / `README.md` / `README.zh.md` / `VERSION` / `plugin.json` / `marketplace.json`, 而 §4 (`:229`) 明列「`aria/CHANGELOG.md` + 版本引用点」为触点; CHANGELOG 由 3777 行长到 3802 行, §5 (`:235`) 引的 `CHANGELOG.md:3020` 现已移到 `:3042`。`:9` 在 R1 恰恰勘正过同一句 (原文写成「全部触点文件 diff 为空」过宽), `:16` 又把它写了回来 —— 勘正逃逸的同型复发 (证据: `proposal.md:16,9,229,235,274,317`; `git diff --name-only 301641b f314785`; `git show f314785:CHANGELOG.md | grep -n completeness`)
- [major] architecture/§1.3 not_applicable (b) 放行白名单与其证据: (b) 判据把 `.aria/audit-reports/**` 纳入放行集, 理由是「本仓真实 Phase A 分支惯例把审计报告与 triage 一并落该目录 (实测 `813e82c` 12/2, `f634d83` 6/1, `2c8eaa6` 1/1)」。实读三个提交: 前两个的 `.aria` 文件确实全在 `audit-reports/` 下 (12/12, 6/6) ✓; 但 **`2c8eaa6` 的那 1 份是 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`**, 不在 `audit-reports/` 下 ⇒ 扩容后它**仍不满足** (b), 三个举证里一个是反证而非支持。后果不是假绿 (方向仍 fail-closed), 而是判据的白名单与它自己引的语料不闭合: DEC / brainstorm 产物族 (复议 #1 `:311` 自己列出的 `docs/decisions/DEC-*` / `.aria/brainstorm-*`) 是常规 Phase A 产物, 未纳入 ⇒「(b) 在本仓规范工作流里可达」只部分成立, R-f (`:257`) 与复议 #7 (`:319`) 交给 owner 的存废估价随之偏 (证据: `proposal.md:165,257,319,311`; `git show --name-only 2c8eaa6`)
- [major] architecture/版本级别判定 (待 owner 复议 #4): #4 (`:317`) 只请 owner 复核**撞号**, 把**级别**写死为 PATCH 并给理由「SOT 规程 + 脚本, 无新 Skill」—— 该理由未与本 spec 自己的 §5 对账。§5 (`:239-244`) 自述**五条**采用方行为变更, 其中第 2 条收窄 `allow_incomplete_checkpoints` 的既有豁免面、第 5 条把坏 config JSON 从 config-loader 的「警告 + 返默认值」改成 `config_unreadable` exit 2, 两者都是对**现有配置**的行为反转, 与 CLAUDE.md「向后兼容 (破坏性变更须 MAJOR)」直接相关。同仓先例两向: v1.73.0 (新增三个机械兜底探针脚本 + CLI 收口) 走 **MINOR** (`aria/VERSION:4`), v1.71.1 (既有脚本补一个谓词) 走 PATCH —— 本 spec 是「新增一个可执行脚本 + 重写一道闸门的 Step 3-5 + 新增输入参数」, 形态贴近前者。并发轨 #195 `proposal.md:382` 因**同一问题**经 R3 major 已把「PATCH vs MINOR」升为 owner 拍板项并推荐改 MINOR; 本 spec 对同类问题只问号不问级 (证据: `proposal.md:317,239-244`; `aria/VERSION:4`; `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md:382`)
- [minor] documentation/§3 phase-c-integrator 接线 `--base` 依据错引: `:216` 用「与 `:253`/#137 同源」支撑「主干的**远程跟踪 ref** (本项目 `origin/master`, 不是裸 `master`)」, 但 `phase-c-integrator/SKILL.md:253` 逐字规定的是「`<MAIN_BRANCH>` 取本项目主干真实名字 —— **本项目是 `master`**」= 裸本地名 (供 `aether ci status --branch` 查远端分支名), 方向与所引结论相反。真实依据是 §1 (`:85`) 已正确引用的 `audit-engine/SKILL.md:404-405` (`git symbolic-ref refs/remotes/origin/HEAD`, fallback `origin/main`→`origin/master`, 全是远程跟踪 ref)。结论本身成立, 只是 §3 的支撑引错 (证据: `proposal.md:216,85`; `phase-c-integrator/SKILL.md:253`; `audit-engine/SKILL.md:404-405`)
- [minor] testing/SC-13「调用串机械护栏 = 计数恰 2」与 §4 自身指令冲突: SC-13 (`:293`) 断言全仓 `completeness_gate.py` 字面**恰 2 处** (SKILL.md fenced bash 块 1 + execution-modes.md 1), 而 §4 (`:224`) 同时要求在 `audit-engine/SKILL.md:427-433 相关文档` 再加一条「`completeness_gate.py` 契约指针」—— 指针若含脚本名即变 3 处, SC-13 必红, 与 R2 已判 major 的 `13c973b9` (SC-10 vs SC-19 结构性互斥) 同型。所引先例的读法也不同: `execution-modes.md:152` 的「机械护栏 SC-17 计数恰 2」指的是**该文件两个模式围栏块内各 1 条**、并明写「本节不复用那个前缀」, 该文件 `sibling_spec_probe.py` 实测 **3 处** (`:90` / `:121` / `:159`), SKILL.md 1 处 —— 先例不是「跨两文件各 1」。现行 `相关文档` 段 (`:427-433`) 的 sibling 先例只指向 references 章节、不含脚本名, 可作 Phase B 的消歧路径 (证据: `proposal.md:293,224`; `audit-engine/SKILL.md:427-433`; `execution-modes.md:90,121,152,159`)

### Risks

- 本席未新增独立 risk 条目。上面 Issues 1 与 2 覆盖的两条通道 (`spec_level_undetermined` 硬阻 / 跨仓 `--no-spec` 真空) 若 owner 选择不在本 spec 内闭合, 应各自升为 Impact 段的显式 Risk 并配可证伪 SC, 而不是留在正文单句里 —— 这两条目前既不在 R-a…R-g 任何一格, 也无 SC 承接。

---

## Verdict

**FAIL** — Critical 2 / Major 3 / Minor 2 (另 4 条 decision 不计入缺陷计数)。

rationale: post_spec 为 `blocking: false`, verdict 不阻断流程, 但按 verdict-format.md 判定规则 ≥1 Critical 即 FAIL。两条 Critical 都不是「方案方向错」, 而是 **R2 修复新写文本里的失效**, 且方向恰好一正一反地落在本 spec 自己定义的两条红线上: Issue 1 是「合法输入被无逃生口硬阻」(与刚修完的 `fdb30703` 同结构), Issue 2 是「零证据判绿在主力场景重新打开」(与被修 bug 同型)。两条都可在正文内闭合, 不需要推翻方案 B: Issue 1 需要把 Level 取法的**窗口**与**字段名**两条边界成文 (建议全文件扫描 + `(Spec )?Level` 两种字面, 并把 `spec_level_undetermined` 纳入 `allow_incomplete_checkpoints` 或另给逃生口), 并给 SC-20 补两条反事实; Issue 2 需要在 §1 的跨仓 fail-closed 条款里把 (a) 通道一并覆盖 (跨仓时拒绝 `--no-spec`, 或改到 `--repo-path` 侧取一次 diff 做核验), 并给 SC-17 补一格。Major 3 条与 Minor 2 条均为文档/照单口径, 随稿可改。

按上一轮聚合的合并规则复算, 本席与 R2 无重叠条目: R2 的 11 条 C/M 逐条实读均已在正文落地 (见 Decisions 第 4 条), 本轮 7 条缺陷中 5 条锚在 R2 rework **新写**的段落 (§1.3 优先级链块 / §1.3(b) 收窄 / §3 `--base` 行 / SC-13 新增护栏 / 头部 09-10 复核行), 2 条锚在未随之更新的下游 (§4 版本行 / 复议 #4)。

---

## 轮次记录

### Round 1: post_spec (2026-09-06)

- Agents: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5 席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 缺陷 C5 / M9 / m10 (另 7 条 decision), 聚合报告 `post_spec-R1-2026-09-06T155000-000Z-R1-…-aggregated.md`
- Vote: REVISE 5 / PASS 0 (单席 verdict FAIL 4 + PASS_WITH_WARNINGS 1) ⇒ proposal v2

### Round 2: post_spec (2026-09-07)

- Agents: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5 席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 缺陷 C2 / M9 / m16 (另 12 条 decision, conflicted 0), 聚合报告 `post_spec-R2-2026-09-07T044500-000Z-R2-…-aggregated.md`
- Vote: REVISE 5 / PASS 0 (单席 verdict FAIL 3 + PASS_WITH_WARNINGS 2) ⇒ proposal v3 (执笔席非原作者、非 R1/R2 任何审计席位)

### Round 3: post_spec (2026-09-10) — 本席

- Agents: tech-lead (本报告为五席之一, 其余席位另行落盘)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 11 条 (缺陷 C2 / M3 / m2 + decision 4)
- Vote: REVISE

---

## 附: 本席实跑核验清单 (可复算)

| # | 命令 / 对象 | 结果 |
|---|---|---|
| 1 | `git -C aria rev-parse HEAD master origin/master` · `git submodule status aria` | 三者 `f314785`, 无 `+` 前缀; `git describe --tags` = `v1.73.0-1-gf314785` |
| 2 | `git -C aria diff --name-only 301641b f314785` | 21 文件, 含 `CHANGELOG.md` / `README{,.zh}.md` / `VERSION` / `plugin.json` / `marketplace.json`; audit-engine / phase-c-integrator / phase-a-planner / phase-b-developer / report-storage / pre-write-validation **全部未变** |
| 3 | `git show {301641b,f314785}:CHANGELOG.md \| wc -l` + 完整性门条目定位 | 3777 → 3802 行; 条目 `:3020` → `:3042` |
| 4 | 153 份 `openspec/{changes,archive}/*/proposal.md` 跑 Level 正则 | 零命中 9; 首命中行是 `Spec Level:` 的 15; 首命中行号 2–58, >20 行 6 份, >30 行 2 份 |
| 5 | `\|C\|` 与碰撞全枚举 (当前树) | 8 changes + 145 archive dirs = **153**; 前缀碰撞 1 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`), 后缀 0, 中缀 0 ⇒ SC-3「潜在缺陷非现存实例」的不变量仍成立 |
| 6 | `.aria/audit-reports/` 现况 | 825 `.md` + 2 目录 (R1 取样时 786) ⇒ B.0 冻结产物要求正确 |
| 7 | `test -d aria/openspec` · `test -d aria/.aria` | 两项皆假 (Critical 2 的前提) |
| 8 | `git show --name-only {813e82c,f634d83,2c8eaa6,62de051}` | 12/12 与 6/6 在 `audit-reports/` 下; `2c8eaa6` 唯一 `.aria` 文件在 `.aria/decisions/`; `62de051` 三文件全在 `openspec/archive/` 下 (SC-5(6) 的形态正确) |
| 9 | `ab-suite/{audit-engine,phase-c-integrator,phase-c-integrator-pre-merge-gate}.json` + `version.yaml` | 2 evals / 3 evals / 无 `evals` 键+8 fixtures+`issue=Aria#60`; 32 文件 `sum(len(evals))=84`; version.yaml 仍 `1.5.0` |
| 10 | `config-loader/DEFAULTS.json` audit 子集 · `find … -name '*.py'` | 八 checkpoint 全 `off`, `adaptive_rules` 三档 (`level_1="off"`), 无两个 `allow_*` 键; `.py` 计数 = 0 |
| 11 | 主仓 `1.73.0` 字符串点枚举 (排除子模块/openspec/handoff/.aria/ab-results) | **16** 处, 与 §4 逐点一致 |
| 12 | `grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` | 恰 4 处, 与 §4 / Tasks 逐字一致 |
| 13 | `grep -rl 'Aria#199\|aria-plugin#161' openspec/{changes,archive}/` | 仅本 spec + 同伴 release tasks 的并发轨交叉引用 ⇒ 无竞品 spec |
