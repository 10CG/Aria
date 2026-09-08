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
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T16:25:51.993Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [code-reviewer]
---

# post_spec 审计 — code-reviewer 席 (Round 1)

审计对象: `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (Level 2, Aria#199 / aria-plugin#161)。
本席透镜: 逐条打开 proposal 引用的 `文件:行号` 验真伪 · 改动是否破坏同文件其它调用路径 · 文档同步面是否列全。所有数字均为本轮实读/实跑所得, 不采信 proposal 自述。

## 审计结论

### Decisions

- [minor] documentation/引用行号逐条核验: 实读核对全部命中 — `execution-modes.md:23-82/32/42-44/46-52/54-61/63-65/185`、`audit-engine/SKILL.md:49-54/60/105/123-125/385-388/403-419/427-433`、`pre-write-validation.md:14/20-26/28-30`、`report-storage.md:8/18/34-39`、`report-format.md:5`、`phase-c-integrator/SKILL.md:137/157/252/253/265/299`、`path_coverage.py:8,547-549`、`spec_complete.py:924-930`、`collectors/audit.py:52,62-114` 无一处行号漂移或函数/分支描述错配 (证据: 逐文件 Read/sed 输出)
- [minor] architecture/1.3(c) no-a2-artifact 判据对真实值域: 实跑枚举 152 个 change — 「有 post_planning 报告却无 `tasks.md`/`detailed-tasks.yaml`」反例 **0** 例, 真无 A.2 产物 **54** 例 ⇒ 该 not_applicable 通道既非恒绿真空也无已观测误放; 与 `standards/conventions/configured-gate-authority.md:38` (白名单第四类) 与 `:40` (「做了但简单」不豁免) 逐字相符 (证据: proposal.md:113)
- [minor] documentation/语料与 issue 忠实度 (非独立 finding, 记录以供后续轮复用): 本仓 `.aria/audit-reports/` **780** 份、`post_spec-*` **499** / `post_planning-*` **209** / `post_implementation-*` **3** 与 proposal.md:34 逐字一致; F2 的 24/2/1/1 (缺 `-R\d+-`) 实测一致; F3「前缀碰撞唯一对 `aria-orchestrator` / `aria-orchestrator-divestiture`」实测一致; 候选 D 的「78 份含 `spec_id:`/`change_id:` 行」实测 78; issue 原文 (37 份他人 post_implementation / `synth-honesty-gaps` / 三条修法 / Step 3 只治误阻不治误放) 转述忠实
- [minor] implementation/Rule #10 审计计划自洽 (记录项): proposal.md:12-13 声称的 config 面逐项核对属实 — `post_brainstorm/mid_implementation/post_implementation/pre_merge/post_closure = off`, `post_spec/post_planning = convergence` (证据: `.aria/config.json` audit 块 json.load)

### Issues

- [major] implementation/1.2 归属匹配规则 + F2 语料 survey: 规则要求连字符界定的**中缀** `-{change_id}-`, 但实测 780 份语料中 **63 份**把 change_id 放在**末段** (`...-{id}.md`, 无 agent_role 后缀), 且这些文件覆盖 **20 个 change_id 的全部报告**。典型: `post_implementation-R1-2026-06-11-audit-drift-guard.md` —— 正是 proposal.md:34 case-2 表格自己点名归属 `audit-drift-guard` 的那 3 份之一。按 1.2 (proposal.md:97-99) 它不归属任何 change, 再按 `excluded_legacy_count` 定义 (:101「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」) 被**误标为 legacy** ⇒ 对这 20 个 change 判 `missing` (假红) 且把原因掩盖成「旧 schema」。F2 (:47) 枚举了 timestamp/round/role-前缀 三类形态偏差, 唯独漏掉「role 段整体缺席」这一维 —— 而它正是击穿所选规则的那一维 (证据: python 枚举 `/home/dev/Aria/.aria/audit-reports`; proposal.md:47,97-101)
- [major] architecture/`--repo-path` 单参数 vs 子模块合并: 该参数同时承载两组语义不同的路径 —— (i) `.aria/config.json` + `.aria/audit-reports/` + `openspec/changes|archive` 锚点 (只存在于**主仓**, 实测 `aria/.aria` 与 `aria/openspec` 均不存在), (ii) `git diff --name-only $(git merge-base HEAD <base>)` (必须是**被合并的目标仓**)。本项目 C.2 子模块合并时两者是两个仓, 且 `phase-c-integrator/SKILL.md:252` 明文规定同类脚本「在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)」。两个方向都坏: repo-path=子模块根 ⇒ 零报告 + S1 锚点必失败 (`change_id_unanchored` 假红); repo-path=主仓 ⇒ 本 cycle 主仓 diff 只有 `openspec/**/*.md` (gitlink bump 排在 Phase D) 全部 ⊆ `scope_skip_paths` ⇒ 1.3(b) 判 `post_implementation = not_applicable/no-auditable-code-in-diff`, 而实际代码全在子模块 = **新引入一条假绿**, 与本 spec 要消灭的失效同型。proposal 全文未出现 submodule / 多仓字样 (证据: `ls aria/`; proposal.md:76,85,110)
- [minor] documentation/基线冻结断言 proposal.md:9: 「`git diff --stat 0545f86 301641b` 对本 spec 全部触点文件**为空**」实测不成立 —— `CHANGELOG.md | 71 ++++`, 而 CHANGELOG.md 在 :10 与 :147 都被列为触点。实际行号后果: 同一条目 @`0545f86` 在 2949 行、@`301641b` 在 3020 行 (§5 引的正是 `CHANGELOG.md:3020`, 对基线 SHA 是对的)。其余触点 (`skills/audit-engine` / `skills/phase-c-integrator`) diff 确为空, 结论成立但断言写过宽 (证据: `git -C aria diff --stat 0545f86 301641b -- CHANGELOG.md skills/audit-engine skills/phase-c-integrator`)
- [minor] documentation/rule6_note AB 版本号 proposal.md:202: 称「固定套件 `ab-suite/audit-engine.json` **v1.3.0** 仅 2 evals」, 实读该 JSON 的 `version` 字段 = **1.0.0**; 1.3.0 是 `ab-suite/version.yaml` 的**套件**版本 (其 1.3.0 changelog 条目 = audit-engine.json 新建)。而 §4 表 :148 的「`version` 1.4.0 → 1.5.0」指的是 version.yaml (实测现值 1.4.0)。同一 spec 里两个「version」指两个文件, 应点名文件。其余 Rule #6 事实核验通过: evals 恰 2 条 (id 1 sibling-probe 渲染 / id 2 not_established 措辞), `grep -ic 'completeness|missing_checkpoint|allow_incomplete'` = **0**, 1.4.0 的「随 eval 闭合不另开 issue」先例引述属实
- [minor] implementation/`[WARN]` 豁免文案字面: proposal 1.1 (:89) 用 `[WARN] incomplete checkpoint gate bypassed by config: ...`, SC-9 (:193) 断言含 `... bypassed by config: missing=`; 而现行 SOT 有**两种不同字面**: `execution-modes.md:44` = `bypassed by config` (无 missing), `:82` = `bypassed: missing={checkpoint_names}`, 且 `aria/CHANGELOG.md:3020`(@301641b) 记的是后者。proposal 自称「保留 `:42-44,82` 既有语义」却造出第三种拼法, §4 文档同步表也没把 `:44` / `:82` 的对齐列进去 (SC-13 已有逐字 grep 传统, 应补一条)
- [minor] testing/SC-4 与 SC-8 判定面欠定义: SC-4 (:188) 断言 `excluded_legacy_count == 2`, 但未写该 fixture 的 `audit.checkpoints` —— 若只启用 `post_spec`, 按 :101 的「以 `{checkpoint}-` 开头」定义计数应为 1; `excluded_legacy_count` 是全局单值还是纳入校验 checkpoint 的并集, 1.4 契约 (:118) 未定义。SC-8 (:192) 断言 `checked_checkpoints == [post_spec, post_planning]` 列表逐字相等, 但排序 (config key 序 vs sorted) 同样未定义。两条都可能因实现者的合理解读而红绿翻转

### Risks

- [minor] architecture/F6 机械判据的载重提升: 1.3(b) 复用 `audit-engine/SKILL.md:403-419` 的 docs-only 判据是零新增 config 的好复用, 但那个信号在原位置只驱动 **mode 降档** (challenge → convergence, 仍然照审), 现在被提升为**整个 checkpoint 免检**。同一次假阳 (如上面 major 2 的跨仓 diff) 的后果从「少跑一档」变成「零审计通过」。建议为 (b) 补一条反事实 SC: 「diff 判 docs-only 但 change 目录声明有代码落点 ⇒ 不得 not_applicable」

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **7** (含 2 条 decision + 1 条 risk)。

rationale: 方案骨架 (机械执行器 + 三态 + change 作用域 + fail-closed 契约) 方向正确, 且**全部 SOT 行号引用逐条核验无一漂移**, 语料统计 780/499/209/3 与 24/2/1/1 实测逐字吻合, 1.3(c) 判据经真实值域验证无反例 —— 这是本轮最强的正面证据。但两处 Major 都落在「机制自己会不会假红/假绿」上: (1) 匹配规则漏了语料里 63 份 / 20 个 change 的末段形态, 而选中的 SC-2 fixture id 在语料中恰好全是中缀形态、断言又用规则自身定义期望值, 结构上测不到; (2) 单一 `--repo-path` 在子模块合并 (本 spec 自己的 C.2 形态) 下语义分裂, 主仓 diff 全 `*.md` 会把「代码在子模块的 change」判成 not_applicable —— 新造一条与被修 bug 同型的假绿。两者都是设计缺口而非实现细节, 应在 Phase B 前收口。post_spec 为 advisory (blocking: false), 不阻断流程, 但按横切检查原则的载重要求, 本席 vote = REVISE。

建议 (非 finding):
1. 1.2 匹配条件改为「`f` 含 `-{id}-` **或** `f[:-3]` 以 `-{id}` 结尾」(最长匹配优先规则同步扩展), `excluded_legacy_count` 定义同改; SC-2 fixture 必须含 ≥2 个末段形态样本 + 一条「退回纯中缀规则 ⇒ 红」的反事实。
2. 拆参数: `--repo-path` (报告/锚点面, 恒主仓) 与 `--diff-repo-path` (合并目标仓); 或在 1.3(b) 加 fail-closed 条款「diff 含 gitlink/submodule 条目 ⇒ 不判 not_applicable」并配一条 SC。
3. `checked_checkpoints == []` (纳入集为空) 目前会 `verdict=pass` 且无 audit trail 行 —— 与本 spec 自己「空集不放行」「not_applicable 必须 surface」的哲学不一致, 建议补一条 `[INFO]` 行。

## 轮次记录

### Round 1

- Agents: code-reviewer (本席, 五席之一)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 9 (Decisions 2 · Issues 6 · Risks 1)
- Vote: REVISE (Critical 0 / Major 2)
