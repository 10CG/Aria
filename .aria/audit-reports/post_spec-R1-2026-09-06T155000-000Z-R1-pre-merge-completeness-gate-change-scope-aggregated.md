---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T16:57:30.921Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — pre-merge-completeness-gate-change-scope (Round 1)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文逐字落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)。

**合并规则 (本轮实际执行, 供 Round 2 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 (例: §1.3(b) 的「过宽 ⇒ 假绿」与「不覆盖阈值触发 ⇒ 假红」是两条)。
5. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (31 条全部唯一, 无碰撞)。

---

## 审计结论

### Critical (5)

- `2e020006` [critical] implementation/§1.2 归属匹配规则/条款2 子串边界 — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  规则 2 要求文件名含双侧连字符子串 `-{change_id}-`, 漏掉 change_id 落**末段**的 `...-{id}.md` 形态 (无 agent_role 段)。五席独立枚举本仓 778 份报告: 该形态 62 份 (backend-architect) / 63 份 (qa-engineer · code-reviewer · knowledge-manager), 覆盖 20-25 个 (checkpoint, change_id) 组合的**全部**自有报告 —— 这些 change 明明跑过审计却会被判 `missing` 假红阻断合并。含活跃 change (`aria-2.0-m6-release-closeout` 9 份 / `aria-2.0-m6-cost-acceptance` 9 份) 与**全部 3 份 post_implementation 报告**; code-reviewer 点出其中 `post_implementation-R1-2026-06-11-audit-drift-guard.md` 正是 proposal.md:34 case-2 表格自己点名归属的那 3 份之一。形态仍在产生 (最新一例 `post_spec-R2-2026-06-25-session-closer-synthesis.md`)。tech-lead 用更宽口径 (对 152 个现存 id 全零命中) 报 247 份并测得真 legacy 形态仅 7 份。F2 (:47) 自称「不依赖前后段形态」与实况相反 —— 它依赖尾部还有一段; qa-engineer 反证其援引先例 `collectors/audit.py:107` 只做左侧界定, 正是为了不假设尾段存在。修法五席收敛一致: 匹配放宽为「含 `-{id}-` **或** `f[:-3]` 以 `-{id}` 结尾」。
  *计数口径注*: 62 / 63 / 247 三个数字源于分母定义不同 (末段形态 vs 全不可归属), 不构成互相矛盾; Phase B 须统一口径再取基线。

- `7cb877b4` [critical] implementation/§1.2 excluded_legacy_count 定义 — **found_by: qa-engineer (critical), backend-architect (major); tech-lead · code-reviewer · knowledge-manager 在各自 §1.2 条目内作同判**
  定义「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」≠ 旧 schema, 把上一条的 62/63 份**真报告**吞进 legacy 计数 ⇒ R-a (:163) 依赖的「legacy 计数显影」不但不显影, 反而把归属 bug 伪装成历史包袱, 编排者读到「legacy 不计入: N」会得出错误结论。backend-architect 实测该口径 = 238 份, 其中真 2-field legacy 仅 6 份、62 份末段形态、176 份 id 不在 C (截断/改名, 如 `post_planning-R2-CONVERGED-dispatch-input-delivery.md`); knowledge-manager 另测 184 份含截断/别名 id (`dispatch-input-delivery` 之于 `aria-2.0-m6-dispatch-input-delivery` 等)。F4 (:49)「结构上不可能属于任何 change」只对 `{checkpoint}-{timestamp}.md` 成立。SC-4 只构造 2 份, 恒绿。修法: 拆 `excluded_legacy_count` (真 2-field) 与 `unattributed_count` (有 id 段但不在 C, 列名进 audit trail)。

- `8c7972ce` [critical] architecture/§1.3(b) not_applicable/scope_skip_paths — **found_by: tech-lead (critical), knowledge-manager (critical), code-reviewer (minor risk, 同一载重论证)**
  用 `audit.scope_skip_paths` (DEFAULTS.json:118-123 含 `*.md` / `docs/` / `deploy/`) 判 post_implementation 为 not_applicable = **放行 owner 已 enabled 的闸门**。三重冲突: (1) 该键 SOT 只有「**降级非 skip**」一种语义 (#58 DEC-4, `audit-engine/SKILL.md:398-400`, 实证 deploy 脚本改动 challenge 抓得到真退化) —— 同一谓词被源决策明确拒绝用作跳过; (2) (b) 自带前提「diff 非空」⇒ 被审对象已产生, 落在 Rule #10 白名单第四类**禁止侧** (`configured-gate-authority.md:40`「存在但简单不算」); (3) 对 aria-plugin 这种产品本体即 markdown 处方的仓, 纯 `.md` Skill 变更会常态拿到「零自身证据也 PASS」= 与被修 bug 同型的新假绿, 而 SC-5 的反事实只加 `src/a.py`, 结构上测不到这一格。knowledge-manager 进一步论证 (b) **没有合法触发场景**: 文档型 diff 下 post_implementation 仍按 convergence 照跑并产出报告 ⇒ 命中 `present`, (b) 唯一被触发的时刻就是「本该跑却被跳了」; 并指出与本 spec 自己引作标杆的 owner 裁定 (archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:29,57) 正面相反。code-reviewer 从载重角度同判: 该信号原只驱动 mode 降档 (challenge→convergence, 仍照审), 现被提升为整个 checkpoint 免检, 同一次假阳的后果从「少跑一档」变成「零审计通过」, 建议补反事实 SC。
  *severity 分歧注*: code-reviewer 记 minor risk, tech-lead / knowledge-manager 记 critical issue —— 按规则取最高。

- `4e504aa5` [critical] architecture/§1.3(c) not_applicable/no-a2-artifact — **found_by: backend-architect (critical), knowledge-manager (major)** — **conflicted: true**
  「`tasks.md` 与 `detailed-tasks.yaml` 都不存在 ⇒ A.2 未执行」把 Level 2 的 A.2 产物**内联**形态误读成未执行。backend-architect: 模板 `proposal-minimal.md:28` 与 `project.md:118` 决定 Level 2 结构上不产这两个文件 ⇒ 判据对**每个 Level 2 change 恒成立**, 自动豁免本仓已 enabled 的 post_planning; 2026-07-04 后归档的 9 个 Level 2 change 全部零 A.2 文件、零 post_planning 报告, 抽查 3 个各有 11/13/12 条内联 checkbox。knowledge-manager: post_planning 启用后归档的 28 个 change 中 9 个 (32%) 两文件皆无却有 inline `## Tasks`。**本 spec 自身即此形态** (10-11 条内联任务、无 tasks.md, 却在 :13 声明跑 post_planning) —— 自相矛盾。SC-6 / SC-11 把它钉成绿 (期望写成「present 或 not_applicable」二选一, 无法区分两态)。
  *conflicted*: code-reviewer 就同一 scope 得出相反结论, 见 `368b926b`。

- `3170df8a` [critical] testing/sc-2 可证伪性 — **found_by: qa-engineer (critical), tech-lead (major), code-reviewer, knowledge-manager; backend-architect 在 Verdict rationale 作同判 (未单列 finding)**
  两层恒绿叠加。(1) **fixture 选样失明**: SC-2 选的 id `pre-merge-gate-no-run-for-branch` 的报告 42/42 (qa-engineer, post_spec 口径) 或 72/72 (knowledge-manager, 全 checkpoint 口径) 均带 `-A{n}-{role}` / `-aggregated` 尾段, 终端段形态 **0 份** ⇒ 号称覆盖「本仓真实文件名形态」的那条 SC, 对唯一会红的形态族结构上失明。(2) **期望值自指**: 期望写成「冻结清单中含 `-{id}-` 的份数」, 由**被测规则自身**推导, 与文件真实归属无关 ⇒ 规则漏掉多少形态该断言都绿 (`2e020006` 正是被它放过); 其反事实只证伪了「位置解析」这另一种实现。修法: 期望集改独立人工标注真实归属; fixture 按名形态族穷举 (终端段族 + role 后缀族 + `aggregated` 族 + 无 `-R\d+-` 族)。

### Major (9)

- `123f94cf` [major] architecture/--repo-path 跨仓执行上下文 — **found_by: tech-lead, code-reviewer**
  单一 `--repo-path` 同时承载两组语义不同的路径: (i) 报告目录 + config + openspec 锚点 (实测只在主仓 —— `aria/.aria` 与 `aria/openspec` 均不存在), (ii) `git diff` 的合并目标仓。而 `phase-c-integrator/SKILL.md:252` 明写同类脚本「在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)」, 子模块 PR 正是本项目 pre_merge 的主力场景。两个方向都坏: repo-path=子模块根 ⇒ 零报告 + S1 恒 `change_id_unanchored` exit 2 假红 (§1.1 明示该错**不受** `allow_incomplete_checkpoints` 豁免); repo-path=主仓 ⇒ 本 cycle 主仓 diff 全是 `openspec/**/*.md` (gitlink bump 排在 Phase D) ⊆ `scope_skip_paths` ⇒ 1.3(b) 判 post_implementation not_applicable 而代码全在子模块 = **新假绿**。proposal 全文无 submodule / 多仓字样。修法: 拆 `--repo-path` (报告/锚点面, 恒主仓) 与 `--diff-repo-path` (合并目标仓), 或成文「仅主仓根调用」并加 fail-closed 条款「diff 含 gitlink/submodule 条目 ⇒ 不判 not_applicable」。

- `9f37ec28` [major] implementation/§1 config 读取 + §1.4 空集短路 — **found_by: tech-lead, backend-architect**
  两条汇成同一失效面 (零证据判绿)。(a) 脚本规定直读 `<repo>/.aria/config.json`, 绕过 SOT 两处明写的 config-loader (`execution-modes.md:37-38` Step 1 / `phase-c-integrator/SKILL.md:130` 步骤 1), 丢掉旧配置兼容映射 (`config-loader/SKILL.md:305-331`: `experiments.agent_team_audit=true` 且无 audit 块 ⇒ 逐项映射为 `checkpoints.*="convergence"`, 含 pre_merge) ⇒ 这类采用方 `checked_checkpoints=[]` ⇒ `verdict=pass`。(b) §1.4 对空 diff 写了「空集不放行」, 却**没有**对空 `checked_checkpoints` 的同款短路, 也无留痕; `.aria/config.json` 不存在时行为未定义 (与 `123f94cf` 的子模块根场景直接叠加)。tech-lead 另指: 两个 `allow_*` 键实测不在 DEFAULTS.json, 「缺省值与 DEFAULTS 一致」对它们无源 (唯一出处是 `SKILL.md:385` 散文)。SC-8 只测非空枚举 / SC-10 只测坏 JSON, 空集这一格无 SC。
  *附注*: code-reviewer 建议 #3 提出同一空集问题, 但其报告明标「建议 (非 finding)」, 故未计入 found_by。

- `1e83b615` [major] architecture/§1.3 mid_implementation 阈值触发路径 — **found_by: qa-engineer**
  `mid_implementation` 是阈值条件触发 (`DEFAULTS.json` `audit.mid_implementation = {trigger: task_progress, threshold: 50}`; `audit-engine/SKILL.md:63` 标「条件触发」), 与 Step 3 已排除的 `mid_post_spec` 同因 (`execution-modes.md:51-52`「启用但合法不产出 ⇒ 启用即会误阻」)。R-c (:165) 给的缓解「走 1.3(b)」只在 diff 全部 ⊆ `scope_skip_paths` 时生效; 最常见场景是 code diff + 任务进度未过 50% 阈值 ⇒ 仍判 `missing` 假红, 全表零 SC 覆盖。需一个与 `mid_post_spec` 同构的排除条款或阈值感知通道, 并配 SC。
  *方向注*: 本条与 `8c7972ce` 同锚 §1.3(b) 但失效方向相反 (此条=假红, 那条=假绿), 二者互补而非矛盾, 故未合并。

- `eaceacdd` [major] architecture/ship 顺序与 gitlink 归属 — **found_by: tech-lead**
  proposal.md:9,178 称「主仓 `aria` gitlink 仍指 `0545f86`, 同伴 v1.71.1 的主仓同步 PR 未合, 本 spec 的 gitlink bump 排在其后」—— 实测不成立: 远端主仓 master 的 aria 子模块 sha 已是 `301641b` (forgejo `GET /repos/10CG/Aria/contents/aria?ref=master`), 同伴主仓同步 PR #202 已 closed; 本地 checkout 停在 `0545f86` 且本地 master 与 origin/master 已分叉。后果: 排队前置是幻影 (拖慢 ship), 且照本地基线做主仓同步会把 gitlink **回退**到 v1.70.0。
  *交叉核对*: backend-architect 与 knowledge-manager 均以 `origin/master = 301641b` 为基线做逐字节冻结核验 (六份 SOT 文件 SAME), 与本条实测一致 —— 分歧只在 proposal 的排队叙述, 不在冻结基线本身。

- `d94ee0bc` [major] testing/rule6_note 档位选行 — **found_by: tech-lead** — **conflicted: true**
  应走 SOT 决策表**第二行** (处方性 · 运行时指令面 ⇒ 能 ⇒ 照跑 AB, 零裁量) 而非第三行: §2 附加约束明写「`description` 或指令流程变动 ⇒ 一律第二行」; 第三行的「不能」指行为类结构性落在套件测量范围**外** (典型 authoring 向导), 而本改动治的是 audit-engine 的 **runtime** 行为 —— 提案自建同形态 descriptive eval id 3 恰证套件测得到, 那是覆盖缺口 (债), 不是豁免理由; 落「拿不准」也应照跑。同族先例的正确写法是两者并存 (照跑既有套件验漂移 + 定向 fixture 验新行为)。另: 提案改了 `phase-c-integrator/SKILL.md` 的处方面 (pre_hook 步骤 4/4.5), 而 `ab-suite/phase-c-integrator.json` (3 evals) 与 `phase-c-integrator-pre-merge-gate.json` **实存**, rule6_note 对它们零评估。
  *conflicted*: knowledge-manager 与 qa-engineer 判第三行成立, 见 `55a7db0e`。

- `261e4ca9` [major] testing/sc-2 冻结清单 provenance — **found_by: qa-engineer**
  「起草时冻结的 40 个真实文件名形态」**无产物** —— 实测该 spec 目录只有 `proposal.md` 一个文件 (汇总席复核 `ls -la` 确为单文件 34000 字节), 仓内也无该清单; 而活体语料正被本轮 post_spec 审计写入而变动 ⇒ Phase B 无法复原「起草时冻结」, 只能重新取样, 追溯性丢失。期望值 provenance 未定: 若测试用与实现同一谓词现算, 该断言退化为重言 (与 `3170df8a` 的自指同根)。修法: 清单落成 spec 目录内产物, 期望值固化为字面数字。

- `013d0274` [major] testing/§1 scope_skip_paths 缺省副本 — **found_by: qa-engineer**
  脚本 `scope_skip_paths` 缺省值「与 DEFAULTS.json / SKILL.md 文档一致」= 造出第二份副本, 但没有任何 SC 断言二者相等。该副本一旦漂移直接改 `not_applicable(b)` 的**放行面** (DEFAULTS 实为 `deploy/` `docs/` `.forgejo/workflows/` `.github/workflows/` `*.md`): 变宽 = 更多假绿, 变窄 = 更多假红。跨 skill 读 SOT 的机制 (importlib 文件直载 vs 内联复制) 也未成文。需一条「脚本缺省 == DEFAULTS.json」的相等性 SC。

- `b9e714b2` [major] documentation/§4 文档同步面/旧 schema 残留 — **found_by: knowledge-manager**
  旧 report schema 的散文残留全仓共 **4 处**, 本 spec 只勘正 1 处。未列入的三处形态逐字同构: `phase-a-planner/SKILL.md:267` (`post_spec-{timestamp}.md`) / `phase-b-developer/SKILL.md:204` (`mid_implementation-{timestamp}.md`) / `:277` (`post_implementation-{timestamp}.md`); SC-13 的机检也只钉 `phase-c-integrator:157` ⇒ 修完仍留三份误导性范例 (符号清扫须穷举形态族)。另: (b) 实质给 `audit.scope_skip_paths` 加了第二个更强的消费语义, 而该键的用户文档 SOT `config-loader/config-example.md:365-367` 明文「降级 … **不 skip**」, 未进同步表 (此条随 (b) 的处置而定)。

- `0fc78a45` [major] implementation/§1.2 规则3 最长匹配 (risk) — **found_by: tech-lead (issue/major), backend-architect (risk/major), qa-engineer (risk/minor)**
  最长匹配排除只覆盖**前缀扩展** `c'.startswith(id + "-")`, 不覆盖 `c'` 以 `-{id}` 结尾或含 `-{id}-` 的包含关系 ⇒ 他人 change 的报告仍会计入本 change, 与被修 bug **同型** (假绿方向)。三席独立枚举一致: 当前 152 个 id 中前缀碰撞 1 对、后缀/中缀 **0 对** ⇒ 潜在缺陷非现存实例; 但规则是发给所有采用方的通用契约, 且 SC-3 只测前缀, 既无守卫也无 SC 锁定该不变量。修法: 谓词改为对称有界包含 (不存在 `c' != id` 使 `-id-` 是 `-c'-` 的子串)。
  *归并注*: type 2 席记 risk / 1 席记 issue ⇒ 取多数 risk; severity 取最高 major。

### Minor (10)

- `cea63fab` [minor] documentation/头部基线冻结断言 — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager**
  「`git diff --stat 0545f86 301641b` 对本 spec **全部触点文件**为空 ⇒ 两 SHA 上行号一致」是过强的全称断言, 实测不成立。四席各举反例: `CHANGELOG.md` +71 行 (完整性门条目 @`0545f86` 在 :2949 / @`301641b` 在 :3020, 而 CHANGELOG 在 :10 与 :147 均列为触点) — tech-lead · code-reviewer · knowledge-manager; `state-scanner/scripts/lib/spec_complete.py` 两 SHA 间改 25 行, `if name == "SKILL.md":` @`301641b` 是 :924 (F7 引用正确) / @`0545f86` 是 :903 ⇒ 按当前 gitlink 追这条引用会读到 `.yaml`/`.json` 分支 — qa-engineer; tech-lead 另列 `plugin.json` / VERSION / README.md 均有 diff。代码面三文件 (execution-modes / audit-engine SKILL / phase-c-integrator SKILL) 的 diff 确为空, 结论成立但断言写过宽。

- `7f5078c1` [minor] documentation/ab-suite 版本号引用 — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  两处称固定套件 `ab-suite/audit-engine.json` 为 **v1.3.0**, 实读该文件 `version` 字段 = **1.0.0**; 1.3.0 是 `ab-suite/version.yaml` 的**套件**版本 (其 changelog 1.3.0 条即「audit-engine.json 新建」), 而 §4 表 :148 的「version 1.4.0 → 1.5.0」指的是 version.yaml (实测现值 1.4.0)。同一 spec 里两个 `version` 指两个文件, 应点名。qa-engineer 另指 §4 未说明文件内 `version` 字段该不该动。实质结论 (2 evals 全是竞品探针场景 / `completeness|missing_checkpoint|allow_incomplete` 零命中) 五席复算一致成立。

- `ffd3834a` [minor] documentation/sot 行号引用 — **found_by: backend-architect, knowledge-manager** — **conflicted: true**
  `phase-c-integrator/SKILL.md:137` 被引作「context = PR diff」, 实际在 `:136` (`:137` 是「5. 处理 verdict」), §3 的改动区间 `:133-137` 同此偏移 (backend-architect + knowledge-manager 各自实读)。knowledge-manager 另列: post_spec 链实为 `phase-a-planner/SKILL.md:250` 非 `:248`; F3「archive 144 去日期」实为 143 个目录 + 1 份 `README.md` (与其自报总数 150 也对不上)。
  *conflicted*: code-reviewer 就同 scope 判「逐条核验无一漂移」并把 `phase-c-integrator/SKILL.md:137` 明确列入命中集, 见 `9a245f24`。汇总席不仲裁 (审计轮内工作区冻结, 不为裁定去读被审对象以外的文件) —— 这是本轮唯一**可机械判定**的冲突, Round 2 一条 `sed -n '136,137p'` 即可闭合。

- `ea5a011a` [minor] testing/sc-13 调用串一致性 — **found_by: backend-architect (testing), qa-engineer (documentation)**
  SC-13 断言「三份文件的调用串逐字相同」, 但 §1 (:68) 只规定 SKILL.md fenced bash 块与 execution-modes.md 各一份 (**两处**), §3 (:135-136) 给 phase-c-integrator 的是 `change_id` 参数与 4.5 处置、不含调用串 ⇒ 第三个比对对象不存在, 该子断言不可执行。backend-architect 建议照 `execution-modes.md:152` 竞品探针先例改写成「机械护栏计数恰 2」。
  *归并注*: category 平票 (testing / documentation), 按席位序取 backend-architect 的 testing。

- `98462082` [minor] testing/sc-9/§1.1 s4 豁免语义 — **found_by: backend-architect**
  §1.1 (:89) 把 `allow_incomplete_checkpoints` 的豁免面从既有 missing (`execution-modes.md:42-44,82`) 扩到 S4 `change_scope_unresolved`, 但 SC-9 只断言「missing → bypassed」与「同旗标下 unanchored 仍 exit 2」, **S4-bypassed 这一路** (verdict / scope_source / error_kind 各取何值) 无断言。

- `dc50ea10` [minor] testing/sc-4/sc-8 判定面 — **found_by: code-reviewer, qa-engineer**
  code-reviewer: SC-4 (:188) 断言 `excluded_legacy_count == 2` 却未写该 fixture 的 `audit.checkpoints` (若只启 post_spec, 按 :101 的「以 `{checkpoint}-` 开头」定义应为 1); 该计数是全局单值还是纳入校验 checkpoint 的并集, §1.4 契约 (:118) 未定义; SC-8 (:192) 断言 `checked_checkpoints` 列表逐字相等, 但排序 (config key 序 vs sorted) 未定义 ⇒ 两条都可能因实现者的合理解读红绿翻转。qa-engineer: SC-8 的 config fixture 不含 `post_brainstorm` 键, 故「待复议 #1」所称「不采纳则 SC-8 的排除集少一项」不成立, 且该复议两个分支均无 SC 覆盖, owner 裁决后无法被测试证伪。

- `76f90716` [minor] testing/sc-1 fixture 锚点 — **found_by: qa-engineer**
  SC-1 fixture 只声明 feature 分支改 `openspec/changes/x/tasks.md` + `src/a.py`, 未声明锚点 `openspec/changes/x/proposal.md` 存在 ⇒ 按 S1 (:84) `--change-id x` 无锚即 `error_kind=change_id_unanchored` / exit 2, 与 SC-1 期望的 exit 1 + `missing` **直接冲突**。另 `git init` 建 master 需显式 `-b master` (现代 git `init.defaultBranch` 可能为 `main`), 否则 `--base master` 的 merge-base 解析失败落 `git_failed`。

- `92aaa082` [minor] implementation/[warn] 豁免文案字面 — **found_by: code-reviewer**
  §1.1 (:89) 用 `[WARN] incomplete checkpoint gate bypassed by config: ...`, SC-9 (:193) 断言含 `... bypassed by config: missing=`; 而现行 SOT 有**两种**字面: `execution-modes.md:44` = `bypassed by config` (无 missing), `:82` = `bypassed: missing={checkpoint_names}`, 且 `CHANGELOG.md:3020` (@`301641b`) 记的是后者。proposal 自称「保留 :42-44,82 既有语义」却造出**第三种**拼法, §4 同步表也未把 `:44` / `:82` 的对齐列入 (SC-13 已有逐字 grep 传统, 应补一条)。

- `07d9adc6` [minor] documentation/§5 行为变化面 — **found_by: qa-engineer**
  §1.1 (:89) 把 `allow_incomplete_checkpoints` 从 `execution-modes.md:41-44` 的「跳过校验, 继续执行」收窄成「仍评估三态; S1/S3 的 error 不被豁免」—— 这对已开该旗标的采用方是**第二条**行为变更, 而 §5 (:156) 只列了「曾经的假绿会变成 missing」, CHANGELOG 迁移文案也未覆盖。

- `ce42dbec` [minor] architecture/ab-suite 共享面并发 (risk) — **found_by: tech-lead**
  `ab-suite/version.yaml` (含程序化重算的 `skills_covered` / `total_eval_cases` 与 changelog 列表) 与在飞同伴轨 `a1-entry-claim-duplicate-work-guard` 同面 —— 该轨 tasks.md:26 明确把 version.yaml 列为**串行**编排对象, 且计划在 `state-scanner.json` 内新增 eval, 双方都会指向下一个 MINOR。提案处理了插件版本号撞号 (`ls-remote --tags` + 读同伴 `<vNEXT>`), 但没给套件版本/changelog 的撞车预案。

### Decisions (7, 不计入缺陷 severity 计数)

- `8a3ae5ab` [minor] architecture/候选方案取舍 b-over-a-d — **found_by: tech-lead**
  采纳「机械执行器 + 三态」而非纯散文修法**成立** —— 散文规程结构上没有红转绿测试面 (triage 实测 `grep -rl allow_incomplete_checkpoints aria/skills --include=*.py` 零命中), 形态镜像 `sibling_spec_probe.py` (stdout JSON + exit code + 消费方 fail-closed) 有本仓先例; F7 的 liveness 处置正确 (`spec_complete.py:924-927` 只认 SKILL.md 内 fenced bash 真调用)。backend-architect 独立同判「方向本身站得住, 候选 A/C/D 的否决理由经核成立, 两条 critical 是判据边界问题, 不需推翻方案 B」; code-reviewer 同判「方案骨架方向正确」。

- `1548cbc0` [minor] documentation/§5 向后兼容面 — **found_by: tech-lead**
  「零代码消费方」实测成立 —— `aria/` 全树对 `allow_incomplete_checkpoints|missing_checkpoint|Completeness Gate` 的 `.py/.json/.yaml` 零命中, 仅 3 份 `.md` (CHANGELOG / execution-modes / SKILL); backend-architect 以 `grep --include=*.py/json/yaml` 独立复核零命中, 一致。

- `4b86d1e8` [minor] testing/sc-12 既有测试基线 — **found_by: qa-engineer**
  三条既有测试腿**实跑**基线全绿 (@ aria `0545f86`): audit-engine 104 tests OK / phase-c-integrator 148 OK / state-scanner 1505 OK, 均 exit 0 ⇒ 无既有失败项需 carve-out, SC-12「三者 0 failure」起点成立。本轮唯一实跑测试套件的席位。

- `ba698d80` [minor] documentation/f1/f2/f3 语料统计 — **found_by: qa-engineer, tech-lead, code-reviewer, knowledge-manager**
  语料与配置事实四席独立复核一致: `.aria/audit-reports` 780 条目 (778 `.md` + 2 目录), post_spec 499 / post_planning 209 / post_implementation 3 (三者归属 id 逐字一致), 非 `-R\d+-` 计数 24/2/1/1, 152 个 change_id 中前缀碰撞唯一 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`), `.aria/config.json` `pre_merge=off` 且 `post_planning=convergence` (⇒ 本 spec 对 triage 注记「只会把 post_spec 纳入校验」的勘正正确), `config.template.json` 无 audit 块 / DEFAULTS.json audit 键集不含两个 `allow_*`。code-reviewer 另核候选 D 的「78 份含 `spec_id:`/`change_id:` 行」实测 78 (tech-lead 独立复算亦 78) 与 issue 原文转述忠实; knowledge-manager 另核四个 issue 编号 open 状态、三条归档先例目录存在、`Linked Issue` 头部机械判据合规、术语 (kebab/snake) 与既有封闭集一致。
  *与 Critical 群的关系*: 事实底盘扎实与 Critical 群不矛盾 —— 问题不在 proposal 引用的数字**对不对**, 而在这些数字**没被用来测**归属谓词的形态族 (见 `2e020006` / `3170df8a`)。

- `368b926b` [minor] architecture/§1.3(c) not_applicable/no-a2-artifact — **found_by: code-reviewer** — **conflicted: true**
  实跑枚举 152 个 change: 「有 post_planning 报告却无 `tasks.md`/`detailed-tasks.yaml`」反例 **0** 例, 真无 A.2 产物 **54** 例 ⇒ 该 not_applicable 通道既非恒绿真空也无已观测误放; 与 `configured-gate-authority.md:38` (白名单第四类) 与 `:40` (「做了但简单」不豁免) 逐字相符。
  *conflicted 解读 (汇总席记, 不代替裁决)*: 两侧量的不是同一件事 —— code-reviewer 量的是「已有报告却被判 not_applicable」(误放的**已观测实例** = 0), backend-architect / knowledge-manager 量的是「A.2 确已执行但产物内联 ⇒ 判据说未执行」(误放的**结构性入口** = 每个 Level 2 change)。两组数字不互斥: 那 9 个 change 本就没跑 post_planning, 所以不会出现在 code-reviewer 的反例集里。**待 owner 复议**: 判据该按「产物文件是否存在」还是「A.2 是否执行过 (含 proposal.md 内联 `## Tasks`)」。

- `9a245f24` [minor] documentation/sot 行号引用 — **found_by: code-reviewer** — **conflicted: true**
  实读核对 proposal 引用的全部 `文件:行号` 均命中 — `execution-modes.md:23-82/32/42-44/46-52/54-61/63-65/185`、`audit-engine/SKILL.md:49-54/60/105/123-125/385-388/403-419/427-433`、`pre-write-validation.md:14/20-26/28-30`、`report-storage.md:8/18/34-39`、`report-format.md:5`、`phase-c-integrator/SKILL.md:137/157/252/253/265/299`、`path_coverage.py:8,547-549`、`spec_complete.py:924-930`、`collectors/audit.py:52,62-114`, 无一处行号漂移或函数/分支描述错配。
  *conflicted*: 与 `ffd3834a` 就 `phase-c-integrator/SKILL.md:137` 直接相反。

- `55a7db0e` [minor] testing/rule6_note 档位选行 — **found_by: knowledge-manager, qa-engineer** — **conflicted: true**
  *来源注*: 两席均在报告正文 `### Decisions` 段明确判定 (knowledge-manager 写「**不构成 finding**」), 未列入其结构化结论清单; 依合并规则第 3 条「同 scope 矛盾意见保留双方」纳入, 以免 Round 2 丢失这条分歧。
  knowledge-manager: 第三行在本项目已有归档先例支撑同型情形 (套件存在但无 eval 到达该状态 ⇒ 照跑 = 测量剧场), 见 `archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:282-284` (走第三行 + 三义务 + 缺口 issue #127); 本 spec 三义务齐备。qa-engineer: 实读 `ab-suite/audit-engine.json` 2 evals、`grep -ic 'completeness\|missing_checkpoint\|allow_incomplete'` = 0 ⇒ 第三行判定成立。
  *conflicted 解读 (汇总席记)*: 双方对**事实**无分歧 (套件 2 evals、零关键词命中, 三席实测一致); 分歧在**判据解释** —— 「套件覆盖外」是指本轮套件没有 eval 到达该状态 (knowledge-manager / qa-engineer), 还是指只有行为类结构性不可测才算、覆盖缺口应照跑并补 (tech-lead)。tech-lead 另提的「`ab-suite/phase-c-integrator.json` 等实存却零评估」无人反驳, 属独立于该分歧的**漏评点**, 不受裁决影响。

---

## Verdict

**FAIL** — Critical 5 / Major 9 / Minor 10 (缺陷类 = issue + risk; 另有 7 条 minor decision 不计入)。

rationale: 五条 Critical 收敛在同一句话上 —— **这份 spec 修的是「门会假绿」, 而它自己新造的判据同时会假红也会假绿, 且它写的 SC 结构上测不到这两件事**。

- 假红侧 (`2e020006` + `7cb877b4`): 归属谓词要求 change_id 两侧都有连字符, 而本仓 62/63 份真实报告的 change_id 就在文件名末尾 —— 20-25 个 (checkpoint, change_id) 组合明明跑过审计却会被判 `missing` 阻断合并, 含活跃 change 与全部 3 份 post_implementation; `excluded_legacy_count` 再把这批真报告记成「旧 schema」, 于是 R-a 的「显影」缓解反过来把 bug 藏起来。五席全部独立枚举命中, 是本轮证据最硬的一条。
- 假绿侧 (`8c7972ce` + `4e504aa5`): 两条 not_applicable 通道都用「产物文件在不在」代理「工序有没有做」, 而 (b) 的判据 SOT 明写「降级非 skip」、(c) 的判据对每个 Level 2 change 恒成立 —— 落在 Rule #10 白名单的禁止侧 (「存在但简单」不算豁免)。本 spec 自身就是 (c) 的形态 (内联 `## Tasks`、无 tasks.md, 却声明跑 post_planning), 自相矛盾。
- 测试侧 (`3170df8a`): SC-2 的 fixture id 在语料里 42/42 (或 72/72) 都是中缀形态, 期望值又由被测规则自身推导 —— 对上面第一类缺陷**恒绿**。这就是「假绿测试掩护假红实现」的闭环, 不是措辞问题。

按 report-storage.md §Verdict 计算, ≥1 Critical ⇒ FAIL。post_spec 的阻塞行为是 `blocking: false` (report-format.md 阻塞行为表), 故本 FAIL **不硬阻断**流程; 但按 Rule #10, 该判定不得由 AI 自行降格 —— `4e504aa5` / `368b926b` 的冲突与 `d94ee0bc` / `55a7db0e` 的档位分歧需 owner 拍板后再进 Phase B。

正面记录 (不因 FAIL 抹掉): 本 spec 的**事实底盘**在四席独立复核下全部为真 (`ba698d80`), 基线冻结可逐字节核 (六份 SOT 副本与 `301641b` diff 全空), 既有测试三腿实跑全绿 (`4b86d1e8`), 方案骨架三席同判方向正确 (`8a3ae5ab`)。缺陷集中在两个判据的形态设计与其 SC 自指, 不在调研质量。

计算依据:
- Critical issues: 5
- Major issues: 9 (8 issue + 1 risk)
- Minor issues: 10 (9 issue + 1 risk)
- Decisions (不计入): 7

---

## 轮次记录

### Round 1

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (五席各自独立报同一结论)
- Conclusions: 31 (去重前 50) —— Critical 5 / Major 9 / Minor 10 / Decisions 7
- Delta vs 上轮: N/A (Round 1, 上轮 keys = null, 无法判定收敛)
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: FAIL 4 (tech-lead / backend-architect / qa-engineer / knowledge-manager) + PASS_WITH_WARNINGS 1 (code-reviewer); code-reviewer 虽判 PASS_WITH_WARNINGS (其席位 Critical=0) 仍按横切检查原则载重投 REVISE
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 1 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 50 / 31 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 5 / 9 / 10 |
| 其中 issue / risk | 22 / 2 |
| Decisions (不计入缺陷计数) | 7 |
| Conflicted 对 | 3 (§1.3(c) 判据 · rule6_note 档位 · SOT 行号) |
| 5/5 全席独立命中的 finding | 2 (`2e020006` · `7f5078c1`) |
| unanimous_pass | false |
| converged | false (Round 1: 上轮 keys = null) |
| 收敛轮次 | N/A |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的三条按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `2e020006` | critical | 5/5 全席 | §1.2 条款 2 匹配放宽为「含 `-{id}-` **或** `f[:-3]` 以 `-{id}` 结尾」(与 `collectors/audit.py` 单侧界定先例对齐); Phase B 先统一 62/63/247 三个口径再取基线数 |
| 2 | `7cb877b4` | critical | qa-engineer, backend-architect (+3 席同判) | 拆 `excluded_legacy_count` (只统计真 2-field `{checkpoint}-{timestamp}.md`) 与 `unattributed_count` (有 id 段但不在 C, 列名进 audit trail); SC-4 期望值随之重算 |
| 3 | `8c7972ce` | critical | tech-lead, knowledge-manager, code-reviewer | **待 owner 复议**: 删除 (b) 或换成与「对象未产生」同义的判据 (如「diff 仅触本 change 的 `openspec/changes/{id}/**`」= Phase A-only PR); 保留则须补反事实 SC「docs-only 但 change 声明有代码落点 ⇒ 不得 not_applicable」 |
| 4 | `4e504aa5` | critical | backend-architect, knowledge-manager (**conflicted** vs code-reviewer `368b926b`) | **待 owner 复议**: (c) 的判据从「A.2 产物文件是否存在」改为「是否存在任何 A.2 产物 (含 proposal.md 内联 `## Tasks`)」; 裁决前先闭合与 `368b926b` 的度量口径差 |
| 5 | `3170df8a` | critical | qa-engineer, tech-lead, code-reviewer, knowledge-manager | SC-2 期望集改**独立人工标注**真实归属 (不得由被测谓词推导); fixture 按名形态族穷举 (终端段 / role 后缀 / aggregated / 无 `-R\d+-` 四族), 并加「退回纯中缀规则 ⇒ 红」的反事实 |
| 6 | `123f94cf` | major | tech-lead, code-reviewer | 拆 `--repo-path` (报告/锚点面, 恒主仓) 与 `--diff-repo-path` (合并目标仓), 或成文「仅主仓根调用」; 另加 fail-closed 条款「diff 含 gitlink/submodule 条目 ⇒ 不判 not_applicable」并配 SC |
| 7 | `9f37ec28` | major | tech-lead, backend-architect | 改经 config-loader 读配置 (保住旧配置兼容映射); §1.4 补空 `checked_checkpoints` 短路 + audit trail 留痕; 补缺 config 时的行为条款; 两个 `allow_*` 键的缺省值另找 SOT 或写进 DEFAULTS.json |
| 8 | `1e83b615` | major | qa-engineer | 给 `mid_implementation` 加与 `mid_post_spec` 同构的排除条款 (或阈值感知的 not_applicable 通道), 并配一条覆盖「code diff + 进度未过阈值」的 SC |
| 9 | `eaceacdd` | major | tech-lead | 按实测订正 proposal.md:9,178 的 gitlink 与排队叙述 (远端已 `301641b`, PR #202 已 closed); ship 前重取本地基线, 防 gitlink 回退 |
| 10 | `d94ee0bc` | major | tech-lead (**conflicted** vs knowledge-manager + qa-engineer `55a7db0e`) | **待 owner 复议**: Rule #6 走第二行照跑 AB 还是第三行 substitute。**不受裁决影响的独立项**: `ab-suite/phase-c-integrator.json` (3 evals) 与 `phase-c-integrator-pre-merge-gate.json` 实存却零评估, 无论档位如何都须补评 |
| 11 | `261e4ca9` | major | qa-engineer | 把 SC-2 的 40 份冻结清单落成 spec 目录内产物 (可追溯), 期望值固化为字面数字 |
| 12 | `013d0274` | major | qa-engineer | 补一条「脚本 `scope_skip_paths` 缺省 == DEFAULTS.json」的相等性 SC; 并成文跨 skill 读 SOT 的机制 (importlib 文件直载 vs 内联复制) |
| 13 | `b9e714b2` | major | knowledge-manager | §4 同步表补入其余三处旧 schema 残留 (`phase-a-planner:267` / `phase-b-developer:204,277`), SC-13 机检同步扩到四处; 若保留 (b) 则把 `config-loader/config-example.md:365-367` 一并列入 |
| 14 | `0fc78a45` | major | tech-lead, backend-architect, qa-engineer | §1.2 规则 3 谓词改对称有界包含 (不存在 `c' != id` 使 `-id-` 是 `-c'-` 的子串); SC-3 补后缀型与中缀型两个 case |

Minor 10 条与 Decisions 7 条不入 rework 清单, 随稿修订即可; 其中 `ffd3834a` / `9a245f24` 的冲突建议 Round 2 用一条 `sed -n '136,137p'` 机械闭合, 无需再开一席。
