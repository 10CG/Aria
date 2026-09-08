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
timestamp: 2026-09-06T16:08:09.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead]
---

# post_spec 审计报告 — pre-merge-completeness-gate-change-scope (Round 1, tech-lead 席)

## 审计结论

### Decisions

- [minor] architecture/候选方案取舍 (B over A/D): 采纳「机械执行器 + 三态」而非纯散文修法**成立** —— 散文规程结构上没有红转绿测试面 (triage 实测 `grep -rl allow_incomplete_checkpoints aria/skills --include=*.py` 零命中), 形态镜像 `sibling_spec_probe.py` (stdout JSON + exit code + 消费方 fail-closed) 有本仓先例; F7 的 liveness 处置正确 (证据: `state-scanner/scripts/lib/spec_complete.py:924-927` 只认 SKILL.md 内 fenced bash 真调用, `references/*.md` 一律 prose)。
- [minor] documentation/§5 向后兼容面: 「零代码消费方」实测成立 —— `aria/` 全树对 `allow_incomplete_checkpoints|missing_checkpoint|Completeness Gate` 的 `.py/.json/.yaml` 零命中, 仅 3 份 `.md` (CHANGELOG / execution-modes / SKILL)。F2 的 499 份与 24 份不含 `-R\d+-`、post_planning 2 / pre_merge 1 / mid_implementation 1、F3 的唯一前缀碰撞对、F8 的 config 注册缺口 (`config.template.json` 无 audit 块; DEFAULTS.json 无两个 `allow_*` 键), 本席逐条复算**全部一致** (证据: `state-scanner/scripts/collectors/audit.py:52,62-114`, `config-loader/DEFAULTS.json:118-123`)。

### Issues

- [critical] implementation/§1.2 报告归属匹配规则: 规则 2 要求文件名含子串 `-{change_id}-` (**尾随连字符**), 但实测本仓 `.aria/audit-reports/` 778 份报告中 **247 份**对 152 个现存 change id **全部零命中**, 其中 63 份以 `-{id}.md` 结尾 (缺 role 段); **21 个 change** 的 post_spec 报告**全部**落在该形态; 偏离仍在发生 (2026-09 共 25 份, 例 `post_planning-R4-1788184755899-a1-entry-combined-A1-tech-lead.md` 属**在飞**轨 `a1-entry-claim-duplicate-work-guard`, 写侧用了缩写 id)。而真 legacy 形态 (`{checkpoint}-{timestamp}.md`) 实测只有 **7 份** ⇒ `excluded_legacy_count` 会把 247 份贴上「旧 schema」标签, 把「本 change 的报告没被识别」伪装成历史包袱, R-a 的量级被低估约 35 倍。**根因层判断**: 本 spec 机械化了**读侧**, 写侧仍是散文约定 (triage 已证「无可打补丁的脚本」), 门的判据因此建立在一个**无强制**的命名约定上 —— 32% 的实测偏离率就是这条约定的真实执行水平。修法: 匹配前给文件名补一个合成尾部连字符 (镜像 `collectors/audit.py:65-69` 的合成首连字符), 并把方案 D 降级为**二级归属通道**复议 (实测 398 份报告 frontmatter `context:` 是 `openspec/...` 路径形态) (证据: proposal.md:98-101,163,186; collectors/audit.py:62-69)
- [critical] architecture/§1.3(b) not_applicable 判据: 复用 `audit.scope_skip_paths` 把「diff 全是 md/ops」判为 `post_implementation` 不适用, 三处冲突: (1) #58 DEC-4 明写「**降级非 skip**」且实证 deploy 脚本改动 challenge 能找到真退化 (`audit-engine/SKILL.md:398-400`) —— 同一谓词被源决策**明确拒绝**用作跳过; (2) Rule #10 白名单第四类边界「A.2 做了但很简单**不是**豁免理由」(`configured-gate-authority.md:40`) —— docs-only diff 是「对象存在但简单」, 不是「对象整个未产生」; (3) 默认 `scope_skip_paths` 含 `*.md` (`DEFAULTS.json:118-123`), 而本仓 Rule #6 判据表恰恰认定处方性 `.md` 变更**影响 AI 行为**。合起来: aria-plugin 主力的纯 `.md` Skill 变更会拿到「零自身报告也 PASS」, 与被修 bug 同型的**新假绿**; SC-5 的反事实只加 `src/a.py`, 结构上测不到这一类。建议改用与「对象未产生」同义的判据 (如「diff 仅触本 change 的 `openspec/` 目录」= issue 的 Phase A-only 真实场景) (证据: proposal.md:110,189)
- [major] architecture/跨仓执行上下文: `phase-c-integrator/SKILL.md:252` 的执行上下文契约明写「在执行 C.2 合并的**目标仓根**内调用 (子模块合并 → 子模块根)」, 而 `aria/` 子模块实测**既无 `openspec/` 也无 `.aria/`** —— 锚点链、S2 的 diff 前缀、报告目录三者**全在主仓**。于是子模块 PR 上: S1 恒 `change_id_unanchored` exit 2 (§1.1 明示该错**不受** `allow_incomplete_checkpoints` 豁免), 或 S2 恒空 → S4 exit 2。而 aria-plugin 子模块 PR 正是本项目 pre_merge 的主力场景。脚本缺「reports/spec 根」与「diff 根」分离的参数 (证据: proposal.md:76,84-87; phase-c-integrator/SKILL.md:252)
- [major] implementation/§1.4 空集与缺 config 路由: `checked_checkpoints` 为空时按「全部 present/not_applicable」→ `verdict=pass`, **无空集短路也无留痕**; 而 `.aria/config.json` **不存在**时的行为未定义 —— 按「缺省值与 DEFAULTS.json 一致」推导即 audit 全 off ⇒ 真空 pass (与上一条的子模块根场景直接叠加)。另: 两个 `allow_*` 键实测**不在** DEFAULTS.json (F8 自己也这么说), 「缺省值与 DEFAULTS.json 一致」对它们无源, 唯一出处是 `SKILL.md:385` 散文。SC-10 只测坏 JSON, SC-8 只测非空枚举 —— 空集这一格无 SC (证据: proposal.md:76,117,192,194; DEFAULTS.json audit 块)
- [major] implementation/§1.2 规则 3 最长匹配: 谓词只覆盖**前缀扩展** (`c'.startswith(change_id + "-")`), 不覆盖 `c'` 以 `-{change_id}` 结尾或含 `-{change_id}-` 的包含关系 —— 那两种下他人 change 的报告仍会计入本 change, 与被修 bug **同型**。本仓实测今日只有 1 对前缀碰撞、0 对后缀/中缀, 但这条规则是发给所有采用方的通用契约, 而 SC-3 只测前缀。修法: 谓词改为「不存在 `c' != id` 使 `-id-` 是 `-c'-` 的子串」(证据: proposal.md:99,187)
- [major] architecture/ship 顺序与 gitlink 归属: 「主仓 `aria/` gitlink 仍指 `0545f86`, 同伴 v1.71.1 的主仓同步 PR 未合, 本 spec 的 gitlink bump 排在其后」**实测不成立** —— 远端主仓 `master` 的 `aria` 子模块 sha 已是 `301641b` (forgejo `GET /repos/10CG/Aria/contents/aria?ref=master` 实读), 同伴主仓同步 PR #202 已 closed。本地 checkout 停在 `0545f86` 且本地 master 与 origin/master **已分叉**。后果: 排队前置是幻影 (拖慢 ship), 且若照本地基线做主仓同步会把 gitlink **回退**到 v1.70.0 (证据: proposal.md:9,178; `git submodule status` vs contents API)
- [major] testing/rule6_note 档位与套件面: SOT 决策表第二行的判据就是「**处方性 · 运行时指令面 ⇒ 能 ⇒ 照跑 AB, 零裁量**」, 且 §2 附加约束明写「`description` 或**指令流程变动 ⇒ 一律第二行**」; 第三行的「不能」指的是**行为类结构性落在套件测量范围外** (典型 authoring 向导), 而本改动治的是 audit-engine 的 **runtime** 行为 —— 提案自己新建同形态 descriptive eval id 3 恰恰证明套件**测得到**, 那是覆盖缺口 (SOT: 「套件的盲区是债, 不是豁免理由」), 不是结构性不可测; 落「拿不准」也应照跑。同族先例的正确写法是**两者并存**: 照跑既有套件验漂移 + 定向 fixture 验新行为 (`openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:412`)。另: 提案改了 `phase-c-integrator/SKILL.md` 的处方面 (pre_hook 步骤 4/4.5), 而 `ab-suite/phase-c-integrator.json` (3 evals) 与 `phase-c-integrator-pre-merge-gate.json` **实存**, rule6_note 对它们零评估 (证据: skill-benchmark-exemption.md:29-33,37-41; proposal.md:11,135,202-203)
- [major] testing/SC-2 可证伪性: 期望值写成「= 冻结清单中含 `-pre-merge-gate-no-run-for-branch-` 的份数」, 即**由被测规则自身定义**, 与文件的真实归属无关 ⇒ 无论规则漏掉多少命名形态该断言都绿 (C1 的 247 份漏配正是被它放过), 其「反事实: 位置解析会少计」只证伪了另一种实现, 没证伪本规则。应改为独立人工标注那 40 个文件的**真实归属**作期望集 (证据: proposal.md:186)
- [minor] documentation/基线冻结段: 「`git diff --stat 0545f86 301641b` 对本 spec **全部触点文件**为空 ⇒ 两 SHA 上行号一致」实测不成立 —— CHANGELOG.md +71 行 (完整性门条目从 `:2946` 移到 `:3020`)、`.claude-plugin/plugin.json`、VERSION、README.md 均有 diff, 而 CHANGELOG 与版本引用点都在 §4 触点表内。引用的 `CHANGELOG.md:3020` 只在 `301641b` 成立, 而当前工作树 checkout 是 `0545f86`。代码面三文件 (execution-modes / audit-engine SKILL / phase-c-integrator SKILL) 的 diff 确为空, 行号可用 (证据: proposal.md:9,147,152)
- [minor] documentation/AB 套件版本引用: 两处称 `ab-suite/audit-engine.json` 为 **v1.3.0**, 实测该文件 `version` 字段 = `"1.0.0"`; 1.3.0 是 `ab-suite/version.yaml` 的**套件**版本 (其 changelog 记「1.3.0 … audit-engine.json 新建」)。实质结论 (2 evals 全是探针场景, `completeness|missing_checkpoint|allow_incomplete` 命中数 0) 复算成立 (证据: proposal.md:11,202)

### Risks

- [minor] architecture/ab-suite 共享面并发: `ab-suite/version.yaml` (含「程序化重算」的 `skills_covered` / `total_eval_cases` 与 changelog 列表) 与在飞同伴轨 `a1-entry-claim-duplicate-work-guard` 同面 —— 该轨 tasks.md:26 明确把 `ab-suite/version.yaml` 列为**串行**编排对象, 且计划在 `state-scanner.json` 内新增 eval; 双方都会指向下一个 MINOR。提案处理了插件版本号撞号 (`ls-remote --tags` + 读同伴 `<vNEXT>`), 但没给套件版本/changelog 的撞车预案 (证据: proposal.md:148,211; 同伴 tasks.md:26)
- [观察, 不计入 finding] 提案自陈的 R-a/R-b/R-c/R-d 四条风险本席认可其存在性; 但 R-a 的**量级**被 C1 推翻 (不是「历史旧 schema 少量」, 而是本仓 32% 的报告名 + 在飞轨), 复议时应连同 R-a 一并改写。

## 核验记录 (机械核实, 数据可用性 Aria #54 载重)

| 断言 | 结果 |
|---|---|
| F1 本仓 `pre_merge=off` / `post_planning=convergence` / `post_implementation=off` | ✅ 成立 (`.aria/config.json` json.load) |
| F2 post_spec 499 / 24 份无 `-R\d+-`; post_planning 2 / pre_merge 1 / mid_implementation 1 | ✅ 逐个复算一致 |
| F3 唯一前缀碰撞对 `aria-orchestrator` ⊂ `aria-orchestrator-divestiture` | ✅ 152 id 全枚举, 恰 1 对 (且无后缀/中缀对) |
| F5 `phase-c-integrator` not_applicable 语义与 `:265` surface 义务 | ✅ 成立 (`:252,260,265,299`) |
| F6 file-scope 二次过滤命令与 `scope_skip_paths` 已注册 | ✅ 成立 (`SKILL.md:403-419`; `DEFAULTS.json:118-123`) |
| F7 liveness 只认 SKILL.md fenced bash | ✅ 成立 (`spec_complete.py:924-927`) |
| F8 template 无 audit 块 / DEFAULTS 无两个 `allow_*` 键 | ✅ 成立 |
| §5 零代码消费方 | ✅ 成立 |
| 方案 D 「78 份报告有 spec_id/change_id 行」 | ✅ 精确 78 |
| **报告名对 change id 的可归属率** (提案未测的轴) | ❌ 247/778 不可归属, 63 份以 `-{id}.md` 结尾 → C1 |
| **基线「全部触点文件 diff 为空」** | ❌ CHANGELOG/plugin.json/VERSION/README 均非空 → minor |
| **主仓 gitlink 现状** | ❌ 远端已 `301641b`, PR #202 已合 → M4 |
| 竞品 spec (同 issue #199 / aria-plugin#161) | 无 —— `openspec/changes/*` 9 个目录中仅本 spec 引用该 issue; 远端分支列表无同题分支 |

## Verdict

**FAIL** — Critical 2 / Major 6 / Minor 3 (Decisions 2 条不计入 severity 计数)。

rationale: 两条 Critical 都指向同一类失效 —— **修完的门仍留有「零自身证据也判绿 / 有证据却判红」的通道**, 且现有 SC 集结构上抓不到它们 (SC-2 用规则自身定义期望值, SC-5 的反事实避开了 `.md`-only 这一格)。C1 有本仓 247 份/21 个 change/在飞轨的实测支撑, C2 有 #58 DEC-4 与 Rule #10 边界两条成文规则的正面冲突, 二者都不是措辞问题, 必须在进 Phase B 前改判据与 SC。post_spec 为 `blocking: false`, 但按 audit-points.md 横切原则「数据可用性核实不符 ⇒ 该 agent verdict 必须 REVISE/FAIL」, 本席投 REVISE。

建议的最小 rework 面 (不扩大 spec 范围): §1.2 匹配谓词 (合成尾连字符 + 包含关系全覆盖) · §1.3(b) 判据换成与「对象未产生」同义的形态 · §1.1/§1.4 补空集与缺 config 短路 · 加 `--reports-root`/`--spec-root` 或成文「仅主仓根调用」 · SC-2 期望值改独立标注 · rule6_note 改第二行并纳入 phase-c-integrator 套件 · 基线段与 gitlink 段按实测订正。

## 轮次记录

### Round 1

- Agents: tech-lead (五席之一, 本报告为单席视角)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 13 (Decisions 2 / Issues 10 / Risks 1)
- Vote: REVISE
