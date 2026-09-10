---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-10T17:22:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — pre-merge-completeness-gate-change-scope (Round 3)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文逐字落盘于同目录 `post_spec-R3-2026-09-10T172200-000Z-R3-pre-merge-completeness-gate-change-scope-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)。五份 frontmatter 均 15 字段齐全, **0 份需补齐**; `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (与 Round 1 / Round 2 同一套, 供 Round 4 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (结论相反, 非同一缺陷的不同 severity) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。
4. `scope` 语义不同则不合并 —— 即使锚在同一节。
5. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, scope 取归一写法 (trim + 折叠空白 + ASCII 小写), 用 python3 实算 (42 条全部唯一, 无碰撞)。
6. tech-lead 与 qa-engineer 的 `### Decisions` 有条目只在报告正文出现、未进结构化清单 (本轮 qa-engineer 的「R2 落地复核」即是), 依 Round 1 / Round 2 先例一并纳入 —— 否则会不对称地丢掉该席的正面记录。
7. 一条单席 finding 同时载有两个不同 scope 的论断时 (本轮 tech-lead 的头部基线条目), 分别计入两条合并条目的 `found_by`, 并在两条内互相点名; 去重前计数仍按单席原始条目数计。

**汇总席本轮的机械复算** (只对席位间数字分歧做只读复核, 不改变任何 finding 的 severity 与处置):

- `git show 301641b:CHANGELOG.md | sed -n '3020p'` 取到的行, 在 `git show f314785:CHANGELOG.md` 中位于 **`:3045`**; 两版行数 3777 → 3802。⇒ code-reviewer 的 `:3045` 与实测一致, tech-lead 同一条内写的 `:3042` 差 3 行 (两席对「已漂移」这一结论一致)。
- 对 `openspec/{changes,archive}/*/proposal.md` **153** 份跑 `Level\s*\**\s*[:：].*?([123])`: 零命中 **9**; 首命中行 >15 的 **6** 份 (>20 亦为 6, >30 为 2, >40 为 2); 首命中行号区间 **2–58**; 首命中行含 `Spec Level` 的 **15**; 行首形态 `> **` 138 / `- **` 3 / `##` 2 / 其他 1。⇒ tech-lead (9 / 15 / 2–58 / >20 六份 / >30 两份)、backend-architect (9 / 6 份 >15)、code-reviewer (15 份 = 9.8%)、knowledge-manager (9 / 2 份 >L40) 四席数字**互洽且逐项命中**; 仅 knowledge-manager 的「L3–L58」下界应为 L2、「字段形态 3 种」按行首前缀枚举为 4 类 —— 两处细节偏差不改变该条结论。

---

## 审计结论

### Critical (3)

- `2d7cccbe` [critical] implementation/§1.3 Step 3 Level N 取法 (窗口/字段形态未定义, 真实语料 15/153 落 spec_level_undetermined exit 2 且无逃生口) — **found_by: tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5)**
  R2 Critical `ca4cd11f` 的修法 (Step 3 过 SOT 优先级链) 引入了一个**必经的新输入** —— 从 `openspec/changes/{id}/proposal.md` 解析 Level N —— 而这个新机械判据未对真实数据值域验证。四席各自全枚举本仓 153 份 proposal, 数字互洽 (汇总席已复算, 见上): **9 份**全文无可解析 Level 行, 另 **6 份**首命中行落在第 15 行之后 (最深 `2026-09-06-a1-entry-claim-duplicate-work-guard` 的 **L58**, 四天前刚归档的当代 proposal), 合计 **15 份 = 9.8%** 在任何 head-window 实现下都判 `spec_level_undetermined` **exit 2**。三条独立的判据缺口: (a) **窗口未定义** —— 散文只写「头部 Level 行」, 无锚正则与 head-window 两种合法实现对同一份 SOT **判决相反** (tech-lead: 这正是 §1.2b 为子目录边界成文时给出的理由, 在此未闭合); (b) **字段形态未定义** —— 首命中行含 `Spec Level` 的有 15 份, 按 `^>\s*\*\*Level\*\*` 实现会整批漏掉, knowledge-manager 另指字段形态多于一种; (c) **无逃生口** —— §1.1 (`:97`) 的豁免面只列 S4 / missing, 该 `error_kind` 不在其中, 经 §1.4 消费方 fail-closed + `on_fail: 阻塞合并` ⇒ 与刚被判 Critical 的 `fdb30703`「无逃生口硬阻」**同结构**。可证伪性同时失守: SC-20(3) (`:300`) 只锁「全文无 Level 行 ⇒ exit 2」一格, 对窗口与字段名两条边界零覆盖。code-reviewer 另补两条下游: 该硬阻是采用方行为变更, 而 §5 (`:239`) 自称穷举的「五条」不含它 (也不含「adaptive_rules 新纳入的 checkpoint 使 missing 变多」); knowledge-manager 另指本仓同类字段已有反向裁定 —— `spec-drafter/SKILL.md:426` 明写「只扫头部 N 行的加固已被真实语料实测否决」, 本 spec 的写法与该裁定冲突。
  *category 分歧注*: tech-lead 记 architecture, backend-architect / code-reviewer / knowledge-manager 记 implementation ⇒ 取多数 implementation。*severity 分歧注*: tech-lead 记 critical, 其余三席记 major ⇒ 按规则取最高 critical。
  *汇总席记*: code-reviewer 该条的落点写在「未入 §5 行为变更枚举」, 其证据链 (9.8% 真实语料硬阻) 与另三席同源, 依规则 1 合并; §5 枚举缺口作为本条的下游子项保留。

- `7877bac6` [critical] architecture/§1.3 Step 3 枚举链只覆盖 mode=adaptive (convergence/challenge 落空纳入集 ⇒ 格 B 盖章放行) — **found_by: qa-engineer, code-reviewer (2/5)**
  与 R2 `ca4cd11f` **同四元组复发**: 修法把优先级链写进了 Step 3, 但级 2 判据逐字只处理 `audit.mode == "adaptive"`, 其余 mode 值全落级 3 默认 `off`。而 `audit.mode` 是四值枚举, SOT (`config-loader/config-example.md:276-278`) 对 `convergence` / `challenge` 写的是「**所有检查点强制使用该模式**」。两席各自实测**本仓 `.aria/config.json` 自身即 `mode="convergence"`** ⇒ 采用方写 `{"audit":{"enabled":true,"mode":"convergence"}}` 而不写 `checkpoints` 块时, 八键全判 off ⇒ 纳入集空 ⇒ 落进 R2 另一条 Critical (`fdb30703`) 的修法新加的**格 B**, 判 `verdict=pass` + `[INFO] 依 audit.checkpoints/adaptive_rules 的配置放行 (Rule #10 白名单第一类)` —— owner 明明把所有 checkpoint 打开了, 门却盖章说「配置显式关闭, 非零证据判绿」。**方向与被修 bug 同型 (零相关证据判绿), 且比原 bug 多一层误导性留痕**。SC 面同样失守: SC-15(3) 的格 B fixture 用 `mode:'manual'`, SC-20 三格只覆盖 adaptive 场景 B/C ⇒ **没有任何 SC 会红**。
  *汇总席记*: 本条与 `2d7cccbe` 同根 (都出自 `ca4cd11f` 修法), 但一条是假绿一条是假红, 依规则 4 不合并。R2 `fdb30703` 的方向 (空集 ⇒ error 硬阻) 本轮已翻转为「空集 ⇒ pass 盖章」, 四元组不同, 不计入持存。

- `34507656` [critical] architecture/§1.1 S3 交叉核验的真空成立 (跨仓子模块 diff 面 / 空 diff ⇒ --no-spec 零证据放行) — **found_by: tech-lead, qa-engineer (2/5)**
  `--no-spec` 通道的**唯一机械守卫**是 S3 的「diff 不触 `openspec/changes/**`」, 两席从两个不同入口证明它会**真空成立**, 后果同一: 全部纳入校验的 checkpoint 记 `not_applicable/level1-no-spec` + `verdict=pass` = 整门旁路。(a) **跨仓入口** (tech-lead): diff 面按 `:81` 恒取自 `--diff-repo-path`, 实测 `test -d aria/openspec` 与 `test -d aria/.aria` **两项皆假** ⇒ 子模块 PR (proposal `:82` 自述「子模块 PR 正是本项目 pre_merge 的主力场景」) 下该谓词**恒真**, 调用方误判 Level 1 传 `--no-spec` 无任何机械阻力; §1 (`:83`) 的跨仓 fail-closed 条款只禁 (b) 通道, 对 (a) 零条款, SC-17 (`:297`) 无跨仓 `--no-spec` 格。(b) **空 diff 入口** (qa-engineer): `--base` 指向已含 HEAD 的 ref 时 diff 为 0 行, 谓词真空成立; 同一文档的 `missing` 行已按 `audit-engine/SKILL.md:410`「防 vacuous-true 空集误触」显式不放行, **S3 没有对称短路**; SC-5 case(4) 的空 diff 只覆盖 `--change-id` 路径。tech-lead 另指对 owner 的二次影响: R-b (`:253`) 把该守卫记为「交叉核验只到 X」(强度有限), 复议 #2 (`:315`) 据此推荐「本 spec 不加固」—— owner 将在「守卫有部分强度」的前提上裁决, 而在主力场景它的强度是 0。
  *category 分歧注*: tech-lead 记 architecture, qa-engineer 记 testing ⇒ 1:1 平票, 按席位序取 tech-lead 的 architecture。*severity 分歧注*: tech-lead critical / qa-engineer major ⇒ 取最高 critical。

### Major (12)

- `3fa67e89` [major] documentation/头部 :16 的 v1.73.1 版本目标未回灌 §4:229 / Tasks:274 / 复议 #4:317 (三处仍写 v1.71.2) — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5)**
  2026-09-10 的头部基线复核只改了头部。四席各自实读: `:16` 已宣告「PATCH 候选改为 **v1.73.1**」, 而 `:229` §4 同步表 / `:274` Tasks 版本项 / `:317` 待 owner 复议 #4 三处仍逐字 **v1.71.2**, 失效断言处无 inline neutralize 标记; `aria/.claude-plugin/plugin.json` 实测 **1.73.0** 且 tag `v1.73.0` 实存。⇒ §4 是 Phase B 的照单, 照执行会把 aria 5 文件 + 主仓 16 个版本点**回退**到 1.71.2 (code-reviewer: 机械 check 只比派生面与 plugin.json 一致, 拦不住倒退; qa-engineer: `plugin-version-arch-docs-match` 等兜底会转红), CHANGELOG 与 tag 序同时乱。复议 #4 交给 owner 的两个候选号 (v1.71.2 vs #195 的 v1.72.0) **双双作废** —— v1.72.x 与 v1.73.0 均已发布, owner 拿到的是失效决策项; code-reviewer 另引 `aria/CHANGELOG.md` 的 `[1.73.0]` 段自述「版本号取号避开并发轨 #195/#199 正在争的 v1.71.2/v1.72.0」为佐证。
  *汇总席记*: tech-lead 的同一条 finding 另载「`:16` 的行号全称句为假」, 依规则 7 分别计入本条与 `5c478b7a`。

- `3f817a3b` [major] testing/SC-13「completeness_gate.py 计数恰 2」与 §2:210 / §4:224 的写入规定互斥 — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer (4/5)**
  v3 自造的内部矛盾, 与 R2 已判 major 的 `13c973b9` 同型 (Phase B 必红一条)。SC-13 (`:293`) 断言 `grep -c 'completeness_gate.py'` 计数**恰 2** (SKILL.md fenced bash 块 1 + execution-modes.md 1), 而同一份 spec 的 §2 (`:210`) 要求在 `audit-engine/SKILL.md` 的 `## 执行流程` **散文**里写「经 `completeness_gate.py` 机械执行」、§4 (`:224`) 又要求在 `:427-433` 相关文档加「`completeness_gate.py` 契约指针」—— 两处都落在 fenced bash 块之外 ⇒ 实现 §2/§4 即令 SC-13 与其「命中行须在 bash 块内」两条同时必红 (backend-architect: 至少 4 命中)。四席另一致指出**所引先例不支持裸文件名计数**: 实测 `sibling_spec_probe.py` 在 `execution-modes.md` **3 处** (`:90`/`:121`/`:159`) / `SKILL.md` **1 处**, 先例锁的是更长的**整条调用串**且相关文档条目**刻意不写脚本名** (tech-lead 据此指出现行 `:427-433` 的 sibling 先例可作 Phase B 的消歧路径)。
  *category 分歧注*: qa-engineer 记 documentation, tech-lead / backend-architect / code-reviewer 记 testing ⇒ 取多数 testing。*severity 分歧注*: tech-lead 记 minor, 其余三席记 major ⇒ 取最高 major。
  *与 `c41592b4` 的关系*: 四席在本条内指出的是先例的**读法**不同, knowledge-manager 另就先例**锚点行号**错误单开一条 (`:152` 是 blockquote), scope 不同, 依规则 4 不合并。

- `d442a8c0` [major] architecture/§1.4 格 B 的人群论证与 SC-20(2) 互斥 (场景 B 在 Level 2/3 下纳入集非空) — **found_by: backend-architect, qa-engineer (2/5)**
  §1.4 (`:188`) 论证格 B 时把官方 `config-example.md:402-417` **场景 B** 列为「落进空纳入集」的合法采用方 (§5 行为变更第 3 条 `:242` 与待 owner 复议 #8 `:325` 同口径), 但按本 spec **自己新定的** Step 3 优先级链, 场景 B (adaptive 且无 `checkpoints` 块) 对 Level 2/3 的 change 解析出的纳入集**非空** —— SC-20(2) (`:300`) 正是这么断言的 (`checked_checkpoints` 非空且全部 `enabled_by == 'adaptive:level_3'`)。只有 `adaptive_rules.level_1="off"` 的 Level 1 才落格 B, 而 Level 1 走 `--no-spec`/S3, 本就无可校验对象。⇒ 同一份文档里两句互斥, **且错的那句正是请 owner 拍板 #8 时的人群依据** —— 受影响的「合法采用方人群」被高估, owner 在被高估的证据面上裁决。

- `3b8bf6dd` [major] architecture/§1.3(b) 放行白名单的语料证据错配 (2c8eaa6 实为 .aria/decisions/) 与 Phase A 产物族未纳入 — **found_by: tech-lead, code-reviewer (2/5)**
  R2 `b9e07647` 的修法把 (b) 的路径集收窄为 `openspec/changes/{id}/**` ∪ `.aria/audit-reports/**`, 并以三个提交为语料证据。两席各自 `git show --name-only` 实读: `813e82c` (12/12) 与 `f634d83` (6/6) 的 `.aria` 文件确在 `audit-reports/` 下 ✓, 但 **`2c8eaa6` 的那 1 份是 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`**, 不在 `audit-reports/` 下 ⇒ 收窄后它**仍不满足** (b), 三个举证里**一个是反证而非支持**。code-reviewer 另指 triage 类产物实际落 `.aria/` 根 (本文 References `:333` 自引 `.aria/triage-comment-199.md`), tech-lead 另指复议 #1 (`:311`) 自己列出的 DEC / brainstorm 产物族 (`docs/decisions/DEC-*` / `.aria/brainstorm-*`) 亦未纳入。⇒「(b) 在本仓规范工作流里可达」只部分成立, R-f (`:257`) 与复议 #7 (`:319`) 交给 owner 的存废估价随之偏。方向仍是 fail-closed (假红不假绿)。
  *汇总席记*: R2 `b9e07647` 争的是判据 species (路径形状 vs 对象未产生), 本条争的是收窄后白名单的**证据与覆盖面**, scope 已换 ⇒ 依规则 4 不视为同四元组持存, 但属同节复发。

- `506ce733` [major] implementation/§1.4 空纳入集三格与 §1.1 S1-S4 的求值顺序未定义 (SC-15 三格 fixture 不可满足) — **found_by: backend-architect, knowledge-manager (2/5)**
  R2 两条 Critical 的修法各自新增一段判据, 但**两段谁先执行全文未声明** (knowledge-manager 另指 Tasks `:264` 的实现清单把作用域 S1-S4 列在三格之前, 即倾向「作用域先」)。SC-15 的格 A / 格 B / 格 C 三条 fixture 都只给 config, **不给 `--change-id`、不建锚点、不给 diff** ⇒ 在「作用域先」这一合法实现下先落 S2→S4 `change_scope_unresolved` **exit 2**, 与断言的 `audit_not_enabled` / `pre_merge_not_enabled` / `verdict=pass exit 0` 直接冲突 —— 期望值随实现顺序红绿翻转, 尤其把 R2 Critical `fdb30703` 专门要保护的官方场景 A/B 采用方那一格 (格 B) 变成**不可满足**。backend-architect 另指一格循环依赖: 格 B/C 的 `resolved(pre_merge)` 在 adaptive 且 `pre_merge` 无显式值时需要 change 的 Level, 而 Level 依赖作用域解析。knowledge-manager 点名这是 R2 已修过的同族缺陷 (minor `5f8e4dfb`, 当时清扫了 SC-16 与 SC-5(4)(5)) 在**新写的 SC-15 上复发**; backend-architect 另指 SC-19 / SC-20 / SC-22 亦未补作用域声明。
  *category 分歧注*: backend-architect 记 implementation, knowledge-manager 记 testing ⇒ 1:1 平票, 按席位序取 backend-architect 的 implementation。

- `1b189d49` [major] implementation/§1.4 stdout 15 键封闭契约与 SC-5/SC-15 的 [INFO] trail 通道不可同绿 — **found_by: backend-architect (1/5)**
  与 R2 `13c973b9` **同四元组复发**: 键集从 13 补到 15 消解了 SC-10 × SC-19 的互斥, 但 **audit trail 的输出通道全文仍未定义**。`:197` 规定「stdout 恰一个 JSON」且顶层键集**逐字 15 项**、`results` 元组字段亦为封闭集, 无任何消息字段; 而 SC-5 断言「stdout 含 `[INFO]` 与 `not_applicable`」、SC-15(3) 断言「stdout/trail 含 `[INFO]`」⇒ 与 SC-10「四种 verdict 下 stdout 均可 `json.loads` 且键集逐字 15 项」结构上不可能同绿。更坏的一支: 若实现为满足 SC-5 把 `[INFO]` 打进 stdout, `:199` 的消费方 fail-closed 条款 (「stdout 非 JSON ⇒ 按 fail 处置」) 会把**每次 not_applicable 运行判成 fail**。本 spec 自称镜像的先例把人读行放 stderr、stdout 只出 JSON (`sibling_spec_probe.py:148-151,684`)。

- `54db6bfd` [major] architecture/§1.1 S1 allow_dangling_change_ids 逃生舱在 adaptive 档被 Level 取法抵消 — **found_by: backend-architect (1/5)**
  与 R2 `5a57d0e0` **同四元组复发, 形态为「修法只做了一半」**: S1 (`:92`) 已按 R2 结论继承 `allow_dangling_change_ids`, 让锚点缺失在该键为 true 时降为 `[WARN]` 并「按该 id 零报告继续评估」; 但**同一轮**新增的 Step 3 优先级链在 adaptive 档要读**该 id 的** `proposal.md` 取 Level —— 无锚点即无 `proposal.md`, 必然解析不到 ⇒ 仍 `spec_level_undetermined` exit 2。⇒ 迁移期逃生舱恰好对 adaptive 采用方 (官方场景 B/C, 也就是 `ca4cd11f` 修法要保护的那批) 失效, 只是换了个 `error_kind`; SC-7(c) (`:287`) 的 fixture 走显式 checkpoints, 测不到这一格。

- `36cf2e53` [major] testing/adaptive 缺省改变「config 未写 checkpoint」语义, 既有 SC fixture 前提 (SC-8 等) 未回扫 — **found_by: qa-engineer (1/5)**
  R2 引入枚举链后, 脚本内联缺省 `mode="adaptive"` + `adaptive_rules.level_2="convergence"` 使「config 里没写的 checkpoint」由 off 变为**启用** (`config-example.md:442` 逐字「其余检查点按 adaptive_rules 推导」)。后果两条: (1) SC-8 (`:288`) 期望 `checked_checkpoints == ['post_planning','post_spec']` **与其自带的注**「本 fixture 不含 `post_brainstorm` 键 ⇒ 两个分支都不改 SC-8」**同时失效** —— 缺该键现在等于「按 level_2 启用」; (2) 其余未钉 `audit.mode` 或 proposal 头部 Level 行的 fixture 会在 Level 解析处落 exit 2, 与各自期望的 exit 0/1 冲突, 只有 SC-20 自己钉了 Level。波及面按该席枚举为 SC-1/3/4/5/6/7/8/9/16/17/19/22。
  *与 `2d7cccbe` / `506ce733` 的关系*: 三条同属「一次 rework 改了输入端语义却未回扫下游 fixture」, 但缺陷对象分别是 Level 判据本体 / 求值顺序 / 既有 SC 的期望值, scope 不同, 依规则 4 不合并。

- `c4610d6b` [major] implementation/§1 --base 绑定的失效方向论证错 (陈旧 base ⇒ diff 超集假红, 非偏小假绿), 真实方向无 SC — **found_by: qa-engineer (1/5)**
  与 R2 `eb21d182` **同四元组复发**: 绑定本身已按 R2 结论改成远程跟踪 ref 并补进 §3 接线, 但**论证方向仍是错的**, 且真实方向零覆盖。该席 hermetic 实跑 (本地 `master` 停在 c1、`origin/master` 前进到 c3、feature 从 c3 开出) 反证: 陈旧 base ⇒ merge-base 更旧 ⇒ diff 是**超集** (3 文件 vs 远程跟踪 ref 的 1 文件), 而非 `:85`/`:253`/`:302` 三处所写的「diff 偏小 ⇒ S3 假通过 ⇒ 假绿」。真实后果**反向**: S2 把他人 `openspec/changes/other/` 卷进作用域 ⇒ 那些 id 零自有报告 ⇒ `missing` 假红阻断合并; `--no-spec` 下则误报 `no_spec_contradicted` exit 2。SC-22(1) 的断言本身仍可证伪, 但守的是一个不存在的失效方向。

- `affceac8` [major] testing/Tasks B.0 双列标注在无人值守下无仲裁者, SC-2 期望值来源不可执行 — **found_by: qa-engineer (1/5)**
  R2 minor `21de127e` 建议的缓解 (标注列改由机械源交叉、不一致者单列供人裁) 已被采纳写进 B.0 (`:262`), 但**在真实语料上落不了地**, 且与同段自述的「Phase B 是无人值守」直接冲突 —— 无仲裁者, 也未写不一致时是阻断还是降级。该席实跑量级: 825 份报告中 570 份有 `context:`/`spec_id:` (文中只写「78 份有」, **低估了独立源**), 255 份两者皆无; 60 份随机抽样两列不一致 **14 份 (23%)**; SC-2 硬约束下唯一两族各 ≥3 的样本 id `state-scanner-mechanical` 的 15 份报告**全部无 frontmatter**, 其 git 历史列给出写盘时刻的目录名 `state-scanner-mechanical-enforcement` (归档后改名) ⇒ **15/15 两列不一致**。
  *汇总席记*: R2 该条记为 `risk|minor|testing`, 本轮升为 `issue|major|testing` —— type 与 severity 双升, 四元组不等, 不计入持存; 属「R2 缓解被采纳后暴露出不可执行」。

- `868def3b` [major] testing/新测试文件的 pytest node-id 写法与 audit-engine/tests 既有 unittest 分类守卫冲突 — **found_by: code-reviewer (1/5)**
  本轮唯一一条落在「新增文件对既有目录的影响」这一前两轮未触及面上的缺陷。全部 SC 的核验列用 pytest node-id 写法 (`::test_issue_case1_...` 等裸函数名, `:281-302`), 而 SC-12 (`:292`) 只跑 `python3 -m unittest discover`; 同目录既有 `test_sibling_spec_probe.py` 有**两条守卫**锁「audit-engine/tests 恒 unittest 套件」(`:303-316` 禁顶层 `import pytest`, `:319-336` 断言 `run_all_tests.sh --list` 分类为 unittest)。两个分支都坏: 裸 pytest 函数且不 import pytest ⇒ unittest 收集 **0 个** = 整套新测试假绿; 加 `conftest.py` 或 `import pytest` ⇒ 既有两条守卫转红且无 pytest 时全套 SKIP。先例 spec (`archive/2026-09-04-sibling-spec-probe/proposal.md:544`) 明写过该约束, 本文 Tasks / SC **零提及**测试风格。

- `3bd0562f` [major] architecture/版本级别 PATCH vs MINOR 未提请裁决 (§5 五条行为变更含两条配置行为反转) — **found_by: tech-lead (1/5)**
  待 owner 复议 #4 (`:317`) 只请 owner 复核**撞号**, 把**级别**写死 PATCH 并给理由「SOT 规程 + 脚本, 无新 Skill」—— 该理由未与本 spec 自己的 §5 对账。§5 (`:239-244`) 自述五条采用方行为变更, 其中第 2 条收窄 `allow_incomplete_checkpoints` 的既有豁免面、第 5 条把坏 config JSON 从 config-loader 的「警告 + 返默认值」改成 `config_unreadable` exit 2, 两者都是对**现有配置**的行为反转, 与 CLAUDE.md「向后兼容 (破坏性变更须 MAJOR)」直接相关。同仓先例两向: v1.73.0 (新增三个机械兜底脚本 + CLI 收口) 走 **MINOR** (`aria/VERSION:4`), v1.71.1 (既有脚本补一个谓词) 走 PATCH; 本 spec 形态 (新增可执行脚本 + 重写闸门 Step 3-5 + 新增输入参数) 贴近前者。并发轨 #195 (`proposal.md:382`) 因**同一问题**已把「PATCH vs MINOR」升为 owner 拍板项并推荐改 MINOR, 本 spec 对同类问题只问号不问级。

### Minor (13)

- `08c2a7d5` [minor] documentation/§3:216 --base「与 :253/#137 同源」标注与被引行相反 (真出处 audit-engine/SKILL.md:404-405) — **found_by: tech-lead, code-reviewer (2/5)**
  §3 (`:216`) 用「与 `:253`/#137 同源」支撑「base = 主干的**远程跟踪 ref** (本项目 `origin/master`, **不是裸 `master`**)」, 两席各自实读 `phase-c-integrator/SKILL.md:252-253`: 逐字规定的正是**裸 `master`**(「取本项目主干真实名字 —— 本项目是 `master`」/「`main_branch` 显式传真值 (本项目 `master`)」, 供 `aether ci status --branch` 查远端分支名), 方向与所引结论相反。同源的只是「无缺省、显式传真值」那一半; 远程跟踪 ref 的真出处是 §1 (`:85`) 已正确引用的 `audit-engine/SKILL.md:404-405` (`git symbolic-ref refs/remotes/origin/HEAD`, fallback `origin/main`→`origin/master`)。结论本身成立, 只是 §3 的支撑引错。

- `4217d903` [minor] documentation/引用行号锚点漂移 (#195 proposal.md:352 / proposal-minimal.md:27-31) — **found_by: code-reviewer, knowledge-manager (2/5)**
  与 R2 `79ce6cfe` 同四元组 (实例已换)。两席实读: §4 (`:231`) 与复议 #4 (`:317`) 引 `#195 proposal.md:352` 佐证「推荐改走 MINOR v1.72.0 待 owner 拍板」, 而该行实为「(f) 的处置 (R2 `88a49037` 改写)」/「布局 3 — 老快照缺 `rel_path` 键」, 与版本无关 —— 版本级别项已随 #195 的 R4 rework (`cf6f56a`) 移到 `:382`(-386); 结论仍真, 锚点已漂。code-reviewer 另加一处: §1.3(c) (`:170`) 与 References (`:331`) 引 `templates/proposal-minimal.md:27-31` 为「模板自带 `## Tasks` 小节」, 实读该小节为 `:28-32` (`:27` 是 Impact 表末行)。

- `961080d1` [minor] implementation/§1/§1.3(b) gitlink/submodule 子句不可判定且不可达 (git diff --name-only 无 mode 信息, 无 SC) — **found_by: backend-architect, code-reviewer (2/5)**
  `:83`/`:165` 规定「diff 中出现 gitlink/submodule 条目时 (b) 不触发」, 两席各自判该子句**既无可触发面也无从判定**: (1) 不可达 —— (b) 的路径集已收窄为 `openspec/changes/{id}/**` ∪ `.aria/audit-reports/**`, gitlink 条目 (如顶层 `aria`) 必然落集外, 同格的路径集判据已先行否决; (2) 不可判定 —— §1.1 (`:93`) 指定的 `git diff --name-only --no-renames` 结构上不输出 mode 信息 (要判定需 `--raw` 的 160000 mode)。无 SC 覆盖 ⇒ 恒绿死条款。当前零行为后果。
  *type 分歧注*: backend-architect 记 risk, code-reviewer 记 issue ⇒ 1:1 平票, 按席位序取 backend-architect 的 risk。

- `5c478b7a` [minor] documentation/头部 :16「本文全部行号继续有效」全称句过宽 (CHANGELOG.md:3020 已漂到 :3045) — **found_by: tech-lead, code-reviewer (2/5)** — **`conflicted: true`** (与 decision `83b200e6` 中 knowledge-manager 的写法)
  `:16` 称「实测 diff 输出为空 …… 没有一个落在本 spec 的触点上 ⇒ **本文全部行号**在 `f314785` 上继续有效」。两席各自实测该全称句为假: `git diff --name-only 301641b f314785` 含 `CHANGELOG.md` / `README{,.zh}.md` / `VERSION` / `plugin.json` / `marketplace.json`, CHANGELOG 顶部 +25 行 (3777→3802), 而 §5 (`:235`) 逐字引用 `CHANGELOG.md:3020`、§4 (`:229`) 明列 `aria/CHANGELOG.md` 为触点 ⇒ 该引用行号已漂。两席同判「已漂移」, 新行号写法不同 (tech-lead `:3042` / code-reviewer `:3045`); **汇总席实跑复核为 `:3045`** (见文首机械复算)。tech-lead 另指 `:9` 在 R1 恰恰勘正过同一句 (原文「全部触点文件 diff 为空」过宽), `:16` 又把它写了回来; code-reviewer 另指其与 `:9` 自带的 carve-out (「CHANGELOG 行号只对 `301641b` 成立」) 自相矛盾 —— **勘正逃逸的同型复发** (memory `feedback_author_and_verifier_must_differ_for_corrections`)。
  *汇总席记 (不裁决)*: 与本条构成 conflicted 的是 `83b200e6` 内 knowledge-manager 的表述「触点**与被引文件** diff 全空 ⇒ :16 的基线断言成立」; backend-architect / code-reviewer / qa-engineer 三席的同类 decision 用的是**更窄**的写法 (只断言「触点文件」diff 为空), 与本条不冲突。分歧可由一条命令闭合, 汇总席已实跑并把输出记在文首, 处置留 Phase B / owner。

- `6f7fb809` [minor] documentation/头部 :10 与 Tasks:273 仍写 gitlink=301641b 起分支, 与 :16 复核分叉 — **found_by: backend-architect (1/5)**
  头部 (`:10`) 仍写 `git ls-tree HEAD aria` = `301641b` 与「Phase B 在 `301641b` 起分支」, Tasks 基线重取项 (`:273`) 同写 gitlink = `301641b`; 但 `:16` 的复核已认定 aria 到 `f314785` (v1.73.0), 实测主仓 gitlink 也确是 `f314785` ⇒ 照头部起分支 = 从落后 21 个提交的点开分支再 bump v1.73.1, CHANGELOG / VERSION / plugin.json 会带着陈旧内容进合并。
  *与 `3fa67e89` / `5c478b7a` 的关系*: 三条同锚在「09-10 头部复核未回灌」这一根因上, 但对象分别是版本号 / 行号全称句 / 起分支基线 SHA, scope 不同, 依规则 4 不合并。

- `5410d633` [minor] implementation/§1.4 matched / unattributed 的 list 顺序未定义 (SC-4 字面比对 flaky) — **found_by: backend-architect (1/5)**
  §1.4 (`:197`) 只给 `checked_checkpoints` 钉了 `sorted()` 字典序 (且明写「使断言可逐字比对」), `matched` 与 `unattributed` 的顺序未定义, 而扫描面用的是 `iterdir()` (顺序随文件系统); SC-4 (`:284`) 对 `unattributed` 断言字面 list 相等, 元素多于一个时会 flaky。

- `d081c6d9` [minor] implementation/§1.1 --change-id 与 --no-spec 并存语义未定义 — **found_by: backend-architect (1/5)**
  两参数同时给出时契约未定义 —— S1 first-match 会静默吞掉 `--no-spec`, S3 的 `no_spec_contradicted` 矛盾检测随之失效 (调用方误声明 Level 1 时不再有任何机械反证); 无 SC 覆盖 (`:88-95`)。

- `94c6bfb1` [minor] testing/SC-3 / SC-4 / SC-9 fixture 未声明作用域来源 (同族清扫未穷举) — **found_by: qa-engineer (1/5)**
  与 R2 `5f8e4dfb` 同四元组 (SC 实例已换)。R2 只给 SC-16 与 SC-5(4)(5) 补了 `--change-id` 与锚点, 同族的 SC-3 (`:283`) / SC-4 (`:284`) / SC-9 (`:289`) 仍未声明作用域来源 ⇒ 按 §1.1 会先落 S4 `change_scope_unresolved` exit 2, 与各自的计数 / 排除 / 豁免断言冲突。

- `27d0cc71` [minor] testing/§1.2 unattributed 截断到 20 的文案与量级无 SC — **found_by: qa-engineer (1/5)**
  §1.2 (`:126`) 把「按字典序前 20 个 + 其余 K 份」论证为 R-a 显影缓解的量级需要 (本仓 170 份), 但无任何 SC 断言该截断与逐字文案 (SC-11 只断言 `count > 0`) ⇒ 实现一次倒 170 行、或干脆不列名单, 都不会红。

- `871fe615` [minor] architecture/§1.4 格 C 的作用域两读 (无条件 vs 仅空集) 决定 SC-11 活体 dogfood 红绿 — **found_by: qa-engineer (1/5)**
  格 C (`:194`) 的「`audit.enabled=true` 但 `resolved(pre_merge)=="off"` ⇒ error exit 2 (调用方步骤 3 本该早退)」写成**前置条件语气**, 但按小节标题只作用于纳入集为空时。本仓实测 `pre_merge="off"` 且纳入集非空 (`post_spec`/`post_planning` = convergence) ⇒ SC-11 (`:291`) 的活体 dogfood 必须依赖「只在空集时判 error」这一读法才跑得通; 两种读法只由一个手动步骤区分, 实现者取无条件读法则 SC-11 当场红。

- `d3eeec78` [minor] implementation/§1.3 纳入集迭代口径两读 (:156 逐对 vs :160 叉乘) — **found_by: code-reviewer (1/5)**
  `:156` 定义纳入为 per (checkpoint, change_id) 逐对求值并用 `enabled_by` 记「这对为什么没被查」, `:160` 却写「对每个纳入的 checkpoint × 作用域内每个 change_id」= 并集叉乘。混合 Level 的多 change PR 下两读法结果不同 (叉乘会对 off 的那一对判 missing 假红); SC-7 只测同 Level 多 change, SC-20 只测单 change。

- `c41592b4` [minor] documentation/SC-13 的「SC-17 计数恰 2」先例锚错 (execution-modes.md:152 是 blockquote) — **found_by: knowledge-manager (1/5)**
  SC-13 (`:293`) 把该先例锚到 `execution-modes.md:152`, 实读该行是竞品探针节的 blockquote (「本节是探针 stdout 契约 + exit code + 消费措辞的权威可执行版」), 不含计数断言; 真实出处是 `openspec/archive/2026-09-04-sibling-spec-probe/proposal.md:513` (另 `:387`/`:397` 写明「恰 2 次是有意的保守」)。
  *与 `3f817a3b` 的关系*: 那条争先例的**读法** (裸文件名 vs 整条调用串), 本条争先例的**锚点行号**, scope 不同, 依规则 4 不合并; Phase B 宜一并处置。

- `19d2710f` [minor] documentation/check_bare_issue_refs.py 对本 proposal 报 55 条裸 #N (未启用闸, 同伴轨已当自检) — **found_by: knowledge-manager (1/5)**
  v1.73.0 随插件 ship 的新脚本 `aria/skills/state-scanner/scripts/check_bare_issue_refs.py` 对本 proposal 实跑报 **55** 条裸 `#N` (同伴 #195 报 18 条)。该 check 目前**未被**任何 `SKILL.md` / `.aria/state-checks.yaml` / `standards/` 引用 ⇒ 不是已启用闸门, 该席**明确不判违规** (符合 Rule #10 的闸门归属判据: 已启用才不得豁免, 未启用不得代 owner 加闸); 但同伴轨已把「对 proposal.md 与 tasks.md 跑该脚本 rc==0」当自检写进 tasks (`archive/2026-09-08-archive-gate-registration-class-and-skill-drift/tasks.md:145`), Phase D 若沿用会红。

### Decisions (14, 不计入缺陷 severity 计数)

- `42c4015f` [minor] documentation/R2 的 2 Critical + 9 Major 逐条落进正文而非批注 — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  本轮唯一 5/5 全席独立命中的条目。五席各自逐条到正文定位, 一致确认 R2 的 11 条 C/M **全部落在判据本体而非批注**: 空纳入集三格 (`:188-196`) + `no_prior_checkpoints`、Step 3 优先级链 (`:143-156`) + `enabled_by` + SC-20、stdout 键集 13→15 (`:197`, 实数逐字 15 项, SC-10 × SC-19 结构性互斥已消)、config 直读 + 内联 (`:176-180`) + SC-21 相等性、照跑面收敛 (`:308`) + 复议 #9、`--base` 绑定 (`:85`) + §3 接线 + SC-22、(b) 两处收窄 (`:165`) + SC-5(6)(7) + 复议 #7、SC-19 换真能翻转的反事实并补 (c) 格 (`:299`)、S1 继承 `allow_dangling_change_ids` (`:92`) + SC-7(c)、§1.2b 落点点名 (`:225`) + SC-13 两条 grep、version.yaml 现值订正 (实测仍 1.5.0, 未再撞号)。**无一条以「已知悉」方式敷衍**。qa-engineer 在同一条内附加限定:「三条修法之间未互相对账」, 对应本轮 `7877bac6` / `36cf2e53` / `d442a8c0`。
  *category 分歧注*: backend-architect 记 testing, code-reviewer 记 implementation, tech-lead / knowledge-manager / qa-engineer 记 documentation ⇒ 取多数 documentation。

- `e5f35a2f` [minor] documentation/语料事实底盘独立复算 (末段族 62 / unattributed 170·160 / legacy 6 / |C|=152 / 碰撞 1-0-0) — **found_by: backend-architect, qa-engineer, code-reviewer, knowledge-manager (4/5)**
  与 R2 `635039c2` 同四元组持存。四席各自写脚本全枚举 (三席对冻结快照 `3f4b379`, 一席另在当前树复算), 载重数字**逐个精确命中**: 末段形态族 **62** / `unattributed` **170** (全 8 checkpoint 口径) 与 **160** (`{post_spec,post_planning}` 口径) / 真 2-field legacy **6** / 原稿合并口径 **238** / `|C|` = **152** (9 changes + 143 archive dirs + README) / 前缀碰撞 **1** 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`)、后缀 **0**、中缀 **0** / post_spec **499** · post_planning **209** · post_implementation **3** / 「全部自有报告皆末段形态」的组合 **25** / 缺 `-R\d+-` 计数 24-2-1-1 / 含 `spec_id:`/`change_id:` 的报告 **78** / audit-reports 780 条目 (778 `.md` + 2 子目录) / `*-audit-trail.md` 恰 5 份且成员名逐字同集 / archive 无重名 id。qa-engineer 另复算 §1.3(c)「三样 A.2 产物全无」的 change = **37** 个, 且碰撞枚举在 `3f4b379`/`813e82c`/HEAD 三快照均为 1-0-0。
  *category 分歧注*: backend-architect 记 implementation, qa-engineer 记 architecture, code-reviewer / knowledge-manager 记 documentation ⇒ 取多数 documentation。
  *与缺陷群的关系 (延续 R1/R2 的注)*: 事实底盘扎实与本轮缺陷群不矛盾 —— 问题不在数字对不对, 而在 R2 rework **新写的判据**未对真实语料值域验证 (`2d7cccbe`)、或未回灌下游断言 (`1b189d49` / `d442a8c0` / `506ce733` / `36cf2e53`)。

- `8a5e771c` [minor] documentation/SOT 引用行号逐条实读全部命中 — **found_by: code-reviewer, knowledge-manager (2/5)**
  两席各自逐文件 awk 取行比对, 三十余处引用**全部命中所述内容**: `execution-modes.md` (`:15/:23-82/:32/:37-38/:44/:46-52/:54-61/:63-65/:82/:152/:185`)、`audit-engine/SKILL.md` (`:49-54/:60/:63/:75-81/:123-125/:381-391/:398-400/:403-419/:410-411`)、`report-storage.md` (`:8/:18/:34-39`)、`pre-write-validation.md` (`:14/:16-18/:20-26/:28-30`)、`phase-c-integrator/SKILL.md` (`:131/:132/:133-137/:157/:252/:253/:260/:265/:299`)、`collectors/audit.py` (`:52/:62-69/:245`)、`spec_complete.py:924-930`、`DEFAULTS.json:118-123` (audit 键集确无两个 `allow_*`)、`config-loader/SKILL.md` (`:8-10/:37/:305-331`)、`config-example.md` (`:280/:381-400/:402-417/:419-440`)、`project.md:117,118`、`configured-gate-authority.md:35,38-40`、`skill-benchmark-exemption.md:26-31,33,35`。⇒ R2 minor `79ce6cfe` 点名的两处 SOT 行号偏移已修复; 本轮新发现的锚点问题只在**非 SOT 的交叉引用**上 (见 `4217d903`)。

- `83b200e6` [minor] architecture/基线冻结 301641b→f314785 触点文件 diff 为空 + 主仓 16 个版本字符串点 — **found_by: backend-architect, code-reviewer (2/5)** — **`conflicted: true`** (与 issue `5c478b7a`; 冲突面仅限 knowledge-manager 在其 `8a5e771c` 条目内的更宽写法)
  与 R2 `9e41ad88` 同四元组持存 (SHA 区间已换)。两席各自实跑 `git -C aria diff --stat 301641b f314785 -- <本 spec 的代码/规程触点>` 输出**为空** (期间全量 21 files / 895+ / 63-), 即 audit-engine / phase-c-integrator / phase-a-planner / phase-b-developer / report-storage / pre-write-validation 六面全部未变 ⇒ 本文对这些文件的行号在当前 gitlink 上继续有效, 基线不需重取。code-reviewer 另逐行复核 §4 (`:229`) 列的 **16** 个主仓版本字符串点在当前 HEAD 全部命中 (`README.md:8,242` + `README.{zh,ja,ko}.md:3,10,244` + `VERSION:24` + `CLAUDE.md:139,141` + `system-architecture.md:189` + `version-scheme.md:23`) —— R2 minor `5210d3a6` 的 14→16 订正已落地。
  *汇总席记 (不裁决)*: 本条的**窄写法** (只断言「触点文件」) 与 `5c478b7a` 不冲突; 冲突的是 knowledge-manager 在其 SOT 条目内写的「触点**与被引文件** diff 全空 ⇒ :16 的基线断言成立」—— `CHANGELOG.md` 既被 §5 `:235` 引用又确实变更 (汇总席实跑: 该行 `:3020`→`:3045`)。依规则 3 保留双方, 汇总席不裁决。

- `4a81578b` [minor] architecture/§5 消费方接缝与枚举完整性 (只读文件名, 零代码消费方) — **found_by: tech-lead, backend-architect (2/5)**
  与 R2 `6705654c` 同四元组持存。两席各自 grep 复核成立: 全插件树对 `allow_incomplete_checkpoints` / `missing_checkpoint` / `Completeness Gate` **零代码消费方** (命中全在 CHANGELOG 与另一个同名 archive-completeness-gate 语境); 文件名 schema 消费方恰为 `collectors/audit.py` 与 `aria-dashboard/references/parse-rules.md` 两处, 且都**只读文件名、不改 writer schema**; `aria-orchestrator/.../extension.py:615,661` 对 `.aria/audit-reports/` 的命中是 `cron-tick-skip-*.log` 注释, 不落 `.md` 扫描面。tech-lead 另逐行验证三条推论: `collectors/audit.py:52` 的 `_AGGREGATE_SUFFIXES` 只挑 `-aggregated.md`/`-aggregate.md`; `:62-69` 确实只合成**首**连字符做左界 (F2 引它作「不假设尾段存在」的先例准确); `spec_complete.py:924-930` 逐字规定 `SKILL.md` 内有真 bash 调用才 alive ⇒ F7 对「调用行必须落 SKILL.md fenced bash 块」的推论正确。

- `2dd386b5` [minor] implementation/§1.2 规则 2+3 归属谓词与 rename 语义代入/实跑验证 — **found_by: backend-architect, code-reviewer (2/5)**
  与 R2 `f5ffa2b3` 同四元组持存 (本轮覆盖面从规则 3 扩到规则 2+3 与 rename)。两席各自逐例代入前缀 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`) / 后缀 (`gate-scope` ⊂ `pre-merge-gate-scope`) / 中缀三型, 含末段族与 role 后缀族: 他人报告被正确排除、本 change 真报告不被误排除, 规则 3 写成「f 按规则 2 命中 c'」而非纯中缀比对恰好覆盖末段分支; code-reviewer 在 778 份真语料上实跑得**多归属文件 = 0**。code-reviewer 另在 tmp 仓复现 `git mv` 归档移动, 确认默认 rename 检测只输出目的侧路径、`--no-renames` 才两侧齐 ⇒ R2 minor `700576c5` 的处置成立。

- `d0014734` [minor] testing/SC-7(a) / SC-19(b)(c) 反事实实跑真能翻转 — **found_by: qa-engineer (1/5)**
  hermetic 实测: `git diff --name-only` 对 `git mv` 默认只输出目的侧路径、加 `--no-renames` 输出两侧 ⇒ SC-7(a) 的反事实真翻转; SC-19(b) 的 R2 新变异体 (去掉 `unattributed` 定义里的 checkpoint 前缀条件 ⇒ 0→1) 与新增的 SC-19(c) 亦真翻转 ⇒ **R2 major `16935cfe` 的修法成立** (该条是 R2 唯一被机械代入证伪的 SC 守卫, 本轮确认已闭合)。

- `65b2cd11` [minor] architecture/§Why 两层根因与候选方案 A/B/C/D 取舍成立 — **found_by: tech-lead (1/5)**
  与 R2 `3df50ff2` 同四元组持存。两层根因经 SOT 实读成立: `execution-modes.md:46-65` 的 Step 3-5 全节无 change 维度、`:64` 「missing 为空即通过」; `audit-engine/SKILL.md:49-54` 输入参数表只有 checkpoint/mode/context/agents_config, 无 `change_id`; `phase-c-integrator/SKILL.md:136` 传 `context: PR diff (branch_name vs base)` 而 `phase-a-planner/SKILL.md:250` 传 `openspec/changes/{spec_id}/proposal.md`。方案 B 对两层各有落点 = 治根因非治标; A (纯散文) / C (可配置下界 N) / D (frontmatter 归属) 的否决理由逐条成立。

- `cbc6c524` [minor] architecture/同伴在飞面零交叠与 ship 顺序 (version.yaml 1.5.0 未被占 / {timestamp} 恰 4 处 / gitlink 已对齐) — **found_by: tech-lead (1/5)**
  与 R2 `db663a86` 同四元组持存, 并**闭合 R2 的 5/5 全席缺陷 `31f29cf3`**: `ab-suite/version.yaml` 现值实测仍 `1.5.0` (`last_modified: 2026-09-05`) ⇒ 目标 1.6.0 未被占, 撞号已真解。另: 当前 `openspec/changes/` 8 轨中唯一带代码落点的并发轨 #195 落在 `state-scanner/collectors/handoff_multibranch.py` / `scan.py:186`, 与本 spec 触点**零交叠**; 全仓 `{timestamp}` 旧 schema 残留实测**恰 4 处** (`phase-a-planner:267` / `phase-b-developer:204,277` / `phase-c-integrator:157`), 与 §4 逐字一致; gitlink 已对齐 (主仓 `fe703c5`, `git submodule status aria` 无 `+` 前缀, `git -C aria rev-parse HEAD master origin/master` 三者同值) ⇒ R2 minor `a1933752` 的「本地 checkout 陈旧/分叉」幻影已清。

- `3d2287b0` [minor] testing/SC-12 既有测试三套件实跑全绿 (104 / 148 / 1593) — **found_by: qa-engineer (1/5)**
  与 R2 `3a3ccc8e` 同四元组持存。本轮唯一实跑测试套件的席位: `audit-engine/tests` **104** OK / `phase-c-integrator/tests` **148** OK / `state-scanner/tests` **1593** OK, 三者 0 failure ⇒ **无既有失败项需在 spec 内 carve-out**, SC-12 的三命令口径可原样沿用。
  *与 R2 的对照*: R2 在 `301641b` 上测得 104 / 148 / **1575**, 本轮 1593 —— 差额 18 条来自 v1.71.1→v1.73.0 期间 state-scanner 的新增测试, 非回归。
  *与 `868def3b` 的关系*: 该 major 争的是**新增**测试文件用 pytest node-id 写法能否被 `unittest discover` 收集, 与本条「既有套件全绿」不矛盾。

- `b261f601` [minor] testing/SC-2 选样面实测极薄 (全语料仅 4 个 id 符合硬约束) — **found_by: qa-engineer (1/5)**
  SC-2 的「同时具 F-a 与 F-b 族」硬约束**可满足但样本面极薄**: 全语料仅 4 个 id 符合 (`state-scanner-mechanical` 6/8 · `state-scanner-inter-cycle-surfacing` 2/3 · `secret-guard-per-segment-evaluation` 2/37 · `linked-issue-normalization` 1/29), 其中只有 1 个两族各 ≥3。
  *与 `affceac8` 的关系*: 本条只记选样面事实, 那条记 B.0 双列标注在该样本上 15/15 不一致 ⇒ 两条互补不矛盾。

- `d9ad60ac` [minor] architecture/Rule #6 档位取两读法并集 + Rule #10 未自行删闸 — **found_by: knowledge-manager (1/5)**
  判据表附加约束 (`skill-benchmark-exemption.md:33`「指令流程变动一律第二行」) 下, 本 spec 取两读法**并集** (照跑 `audit-engine.json` 2 evals + `phase-c-integrator.json` 3 evals + 定向 fixture + 缺口 issue), **严于任一单读法**; `phase-c-integrator-pre-merge-gate.json` 经 `json.load` 实读确无 `evals` 键 (`type=workflow_skill_subextension`, 8 `fixtures[]`, `issue=10CG/Aria#60`), 认定权挂复议 #9 而**未自行删闸** ⇒ 符合 Rule #10。**闭合 R2 major `4f360230`** (照跑面收敛)。
  *与 R2 `6529a8d9` 的关系*: 同主题但 R2 记 testing、本轮记 architecture ⇒ 四元组不等, 不计入持存。

- `803f7ccf` [minor] documentation/Level 2 定级与内联 Tasks 形态与归档口径一致 — **found_by: knowledge-manager (1/5)**
  同类 audit-engine 脚本型 spec 归档实测均为 Level 2 (`2026-09-04-sibling-spec-probe` / `2026-08-23-pre-merge-gate-no-run-for-branch` / `2026-07-31-phase-c-gate-path-coverage-not-applicable`), 内联 `## Tasks` 无 `tasks.md` 的形态亦有先例 ⇒ 本 spec 的定级与形态与归档口径一致, 不构成缺陷。

- `7560bcd5` [minor] documentation/头部 Linked Issue 字段过 spec-drafter 机械判据 — **found_by: knowledge-manager (1/5)**
  与 R2 `d188f0b8` 同四元组持存。`> **Linked Issue**: \`10CG/Aria#199, 10CG/aria-plugin#161\`` 过 `spec-drafter/SKILL.md:414-426` 的写法三条 (单 code span + `, ` 分隔 + 行首无空白 + 非 markdown 链接形); 紧邻的 `> **Issue**:` 行字段名不在 E0 谓词 1 的两拼写集合内, 不遮蔽第一条命中。合规。

---

## Verdict

**FAIL** — Critical 3 / Major 12 / Minor 13 (缺陷类 = issue + risk; 另有 14 条 minor decision 不计入)。

rationale: 按 `report-storage.md §Verdict` 计算, ≥1 Critical ⇒ **FAIL**。post_spec 的阻塞行为是 `blocking: false` (report-format.md 阻塞行为表), 故本 FAIL **不硬阻断**流程; 但按 Rule #10, 该判定不得由 AI 自行降格。

**本轮的性质与 R2 一致, 程度更集中**: 五席逐条复核后 5/5 一致确认 R2 的 2 Critical + 9 Major **全部落在判据本体而非批注** (`42c4015f`), 事实底盘四席独立全枚举**逐个精确命中** (`e5f35a2f`), SOT 三十余处行号实读全中 (`8a5e771c`), 既有测试三腿全绿 (`3d2287b0`), 消费方接缝零破坏 (`4a81578b`), 方案 B 方向正确 (`65b2cd11`), 撞号与照跑面两条 R2 缺陷已真闭合 (`cbc6c524` / `d9ad60ac`)。**本轮 28 条缺陷中没有一条是 R1/R2 结论的原样重复提出** —— 全部锚在 R2 rework 新写的文本 (Step 3 优先级链 / 空纳入集三格 / (b) 收窄 / SC-13 新增 grep / `--base` 绑定 / 09-10 头部基线复核) 与一个前两轮未触及的面 (新增测试文件对既有 tests 目录 runner 分类的影响) 上。

三条 Critical 有一个共同根因: **R2 的修法各自成立, 彼此没有对账, 且新引入的机械判据没有对真实数据值域验证**。

- `2d7cccbe` (4/5 席): `ca4cd11f` 修法引入的 Level 解析是新判据的**必经输入**, 但窗口与字段形态都没定义, 对真实语料 **15/153 = 9.8%** 落 `spec_level_undetermined` exit 2 且**豁免面不覆盖该 error_kind** —— 与刚被判 Critical 的 `fdb30703`「无逃生口硬阻」同结构, 且与本仓同类字段的既有裁定 (`spec-drafter/SKILL.md:426`) 正面冲突。
- `7877bac6` (2/5 席): 同一条修法只机械化了四值 `audit.mode` 中的 `adaptive` 一支; 本仓 `.aria/config.json` 自己跑的正是 `convergence` ⇒ 空纳入集被送进 `fdb30703` 修法新加的格 B, **盖章判 pass 并留下「配置显式关闭」的误导性 INFO** = 与被修 bug 同型的假绿, 且比原 bug 多一层留痕误导。**这是 R2 `ca4cd11f` 的同四元组复发**。
- `34507656` (2/5 席): `--no-spec` 通道的唯一机械守卫在两个入口 (跨仓子模块 diff 面 / 空 diff) 上真空成立 ⇒ 整门旁路; 而 `missing` 行早已按 `audit-engine/SKILL.md:410` 做了防真空短路, S3 没有对称处理。owner 还将在 R-b/复议 #2 给出的「守卫有部分强度」这一错误前提上裁决。

十二条 Major 分四类: (a) **v3 自造的内部矛盾** —— `3f817a3b` (4/5 席, SC-13 计数护栏与 §2/§4 的三处写入互斥, Phase B 必红一条)、`d442a8c0` (格 B 人群论证与 SC-20(2) 互斥, 且错的那句正是复议 #8 的人群依据)、`506ce733` (两段判据的求值顺序未定义, 使新写的 SC-15 三格不可满足)、`3fa67e89` (4/5 席, 版本目标三处分叉且 §4 是 Phase B 照单)。(b) **R2 修法只做了一半** —— `1b189d49` (键集补到 15 后互斥换到 trail 通道)、`54db6bfd` (S1 豁免继承了却被新 Level 判据抵消)、`c4610d6b` (绑定改对了但论证方向仍错、真实方向零 SC)、`36cf2e53` (枚举链改变了「config 未写 key」的语义却未回扫既有 fixture)。(c) **证据与落点错配** —— `3b8bf6dd` ((b) 白名单的三例语料里一例是反证, 其自述要覆盖的 DEC/triage 产物族不在新路径集内)、`affceac8` (R2 建议的双列标注被采纳后在真实语料上 15/15 不一致且无仲裁者)。(d) **未被前两轮触及的新面** —— `868def3b` (新测试文件的 pytest 写法与既有 unittest 分类守卫两个分支一个假绿一个连坐红)、`3bd0562f` (版本级别 PATCH vs MINOR 未提请裁决, 而 §5 自述含两条配置行为反转)。

十三条 Minor 有两个共性: 过半 (4 条) 仍锚在「2026-09-10 头部复核只改头部、未回灌下游」这一根因上 (`5c478b7a` / `6f7fb809` 及其关联的 `3fa67e89` / `4217d903`), 与 R2 已点名的 memory `feedback_author_and_verifier_must_differ_for_corrections` 形态一致 (R1 勘正过的同一句在 `:16` 又被写回); 另有三条是「写进契约但无法机械核验、也无 SC」的条款 (`961080d1` / `27d0cc71` / `871fe615`)。

计算依据:
- Critical issues: 3
- Major issues: 12 (12 issue + 0 risk)
- Minor issues: 13 (10 issue + 3 risk)
- Decisions (不计入): 14
- Conflicted 对: 1 (`5c478b7a` ↔ `83b200e6`, 汇总席已实跑记录机械证据, 不裁决)

---

## 轮次记录

### Round 3

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`; frontmatter 15/15 字段齐全 5 份, 0 份需补齐
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (五席各自独立报同一结论; tech-lead 另以 `grep -rl 'Aria#199\|aria-plugin#161' openspec/{changes,archive}/` 复核, 仅命中本 spec 与同伴 release tasks 的交叉引用)
- Conclusions: 42 (去重前 70) —— Critical 3 / Major 12 / Minor 13 / Decisions 14
- Delta vs 上轮: 上轮 39 keys, 本轮 42 keys, **字面集合不等且交集为 0 ⇒ `stable_vs_prev: false`**。归一到语义层后 **14 条四元组持存**, 其中 **8 条是正面记录 (decision)** —— `e5f35a2f`≡R2 `635039c2` (语料底盘)、`3d2287b0`≡`3a3ccc8e` (SC-12 基线)、`4a81578b`≡`6705654c` (§5 消费方接缝)、`65b2cd11`≡`3df50ff2` (方案 B 取舍)、`cbc6c524`≡`db663a86` (同伴在飞轨)、`83b200e6`≡`9e41ad88` (基线冻结, SHA 区间已换)、`2dd386b5`≡`f5ffa2b3` (归属谓词)、`7560bcd5`≡`d188f0b8` (头部字段); **6 条是同 scope 上的缺陷复发** —— `7877bac6`≡`ca4cd11f` (枚举源只覆盖 1/4 mode)、`54db6bfd`≡`5a57d0e0` (S1 豁免被新判据抵消)、`c4610d6b`≡`eb21d182` (--base 论证方向)、`1b189d49`≡`13c973b9` (stdout 键集 × SC 互斥换通道)、`4217d903`≡`79ce6cfe` (引用行号锚点, 实例已换)、`94c6bfb1`≡`5f8e4dfb` (SC fixture 作用域声明, SC 实例已换)。R2 的 11 条 C/M 去向: **4 条同四元组复发** (上列前四条)、**3 条换对象/换方向复发** (`fdb30703` 空集判决由 error 翻转为 pass 盖章 → `7877bac6`; `b9e07647` 判据 species → `3b8bf6dd` 证据错配; `31f29cf3` version.yaml 撞号已闭合而版本对象换成 plugin 版本目标 → `3fa67e89`)、**4 条判为真闭合** (`84d49ad0` config 直读+SC-21、`4f360230` 照跑面收敛、`16935cfe` 新反事实经实跑确认翻转、`2bf48619` §1.2b 落点点名 —— 但该修法自身造出新 major `3f817a3b`)。R2 的 conflicted 对 = 0, **本轮 conflicted 对 = 1** (`5c478b7a` ↔ `83b200e6`, 见该两条的汇总席记)
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: FAIL 2 (tech-lead C2M3m2 / qa-engineer C1M7m3) + PASS_WITH_WARNINGS 3 (backend-architect C0M6m4 / code-reviewer C0M6m5 / knowledge-manager C0M3m3); 后三席虽自判 PASS_WITH_WARNINGS 仍按横切检查原则载重投 REVISE
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 3 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 70 / 42 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 3 / 12 / 13 |
| 其中 issue / risk | 25 / 3 |
| Decisions (不计入缺陷计数) | 14 |
| Conflicted 对 | 1 (`5c478b7a` ↔ `83b200e6`) |
| 5/5 全席独立命中 | 0 finding + 1 decision (`42c4015f`) |
| 4/5 席命中 | 3 findings (`2d7cccbe` / `3fa67e89` / `3f817a3b`) + 1 decision (`e5f35a2f`) |
| unanimous_pass | false |
| stable_vs_prev (四元组集合逐条相等) | false (39 vs 42, 字面交集 0; 语义持存 14 条, 其中 8 条为 decision) |
| converged | false (集合不等 且 unanimous_pass=false) |
| 收敛轮次 | N/A |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `2d7cccbe` | critical | tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5) | Level 取法钉到可实现程度: (a) **扫描窗口**成文 (建议全文件扫描 + 取文档序第一条, 与 `spec-drafter/SKILL.md:426` 对同类字段的既有裁定一致); (b) **字段形态集**成文 (至少覆盖 `Level` 与 `Spec Level` 两种字面、`> **` / `- **` / `##` 三种行首); (c) 给 `spec_level_undetermined` 一个逃生口 (纳入 `allow_incomplete_checkpoints` 或另开键)。SC-20 补两条反事实 (Level 行在 L40+ 仍须解析成功 / `Spec Level:` 形态须命中); §5 的「五条行为变更」补入本条与「adaptive_rules 新纳入 checkpoint 使 missing 变多」 |
| 2 | `7877bac6` | critical | qa-engineer, code-reviewer (2/5) | Step 3 枚举链补齐 `audit.mode` 四值语义: `convergence` / `challenge` 按 SOT (`config-example.md:276-278`)「所有检查点强制使用该模式」纳入, 而非落默认 off; 并给格 B 加分支「非 manual/adaptive 模式下空纳入集必须判 error 而非 pass」。补一条以本仓 `.aria/config.json` (`mode="convergence"`, 无 `checkpoints` 块) 为 fixture 的 SC。**若 owner 认为应保留现语义, 属 Rule #10 的语义选择, 须与复议 #8 合并请裁** |
| 3 | `34507656` | critical | tech-lead, qa-engineer (2/5) | S3 的两条真空面各自显式短路: (a) **跨仓** —— §1 的 fail-closed 条款把 (a) 通道一并覆盖 (跨仓时拒绝 `--no-spec`, 或改到 `--repo-path` 侧取一次 diff 做核验); (b) **空 diff** —— 比照 `audit-engine/SKILL.md:410` 的防 vacuous-true 写法给 S3 加对称短路。SC-17 补跨仓 `--no-spec` 一格、SC-5 补 `--no-spec` + 空 diff 一格。同时订正 R-b (`:253`) 与复议 #2 (`:315`) 对该守卫强度的描述 —— **owner 现在拿到的是「守卫有部分强度」的错误前提** |
| 4 | `3fa67e89` | major | tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5) | 把 §4 (`:229`) / Tasks (`:274`) / 复议 #4 (`:317`) 三处 v1.71.2 订正为 v1.73.1 并对失效断言加 inline neutralize; 复议 #4 的并发面论证整段重写 (v1.71.2 与 v1.72.0 两候选均已作废)。**优先随手闭合** —— 它是 Phase B 照单, 照执行即版本回退 |
| 5 | `3f817a3b` | major | tech-lead, backend-architect, qa-engineer, code-reviewer (4/5) | 三选一并成文: 把 SC-13 的护栏改成**带前缀的整条调用串**计数 (与 `sibling_spec_probe.py` 先例同法); 或把 §2/§4 的两处提及改为不含脚本名的指针 (先例 `:427-433` 即如此); 或放宽计数并改断言「fenced bash 块内恰 1 处」。**必须在进 A.2 前修掉** (否则 TDD RED 阶段结构性必红一条)。顺带订正先例锚点 (见 `c41592b4`) |
| 6 | `d442a8c0` | major | backend-architect, qa-engineer (2/5) | §1.4 (`:188`) / §5 (`:242`) / 复议 #8 (`:325`) 的「格 B 合法人群」重写: 官方场景 B 在 Level 2/3 下纳入集非空 (SC-20(2) 自证), 落格 B 的只有 Level 1、而 Level 1 走 `--no-spec`/S3。**owner 复议 #8 的人群依据须随之重给**, 否则是在被高估的证据面上裁决 |
| 7 | `506ce733` | major | backend-architect, knowledge-manager (2/5) | 显式声明 §1.1 S1-S4 与 §1.4 三格的求值顺序 (Tasks `:264` 已倾向「作用域先」), 并按该顺序重写 SC-15 三格 fixture (补 `--change-id` / 锚点 / diff), 使 R2 Critical 要保护的场景 A/B 那一格可满足; 同时定义格 B/C 的 `resolved(pre_merge)` 与 Level 解析的循环依赖如何拆。SC-19 / SC-20 / SC-22 一并补作用域声明 |
| 8 | `1b189d49` | major | backend-architect (1/5) | 定义 audit trail 的输出通道: 建议比照先例把人读行 (`[INFO]`/`[WARN]`) 打 **stderr**、stdout 只出 JSON, 并把 SC-5 / SC-15(3) 的断言改到 stderr; 否则须放宽 `:197` 的 15 键封闭契约与 `:199` 的消费方 fail-closed 条款 —— 三者当前不可能同绿 |
| 9 | `54db6bfd` | major | backend-architect (1/5) | `allow_dangling_change_ids=true` 时, Level 解析失败须与锚点缺失走**同一条降级路径** (WARN + 按该 id 零报告继续), 而非换个 `error_kind` 继续硬阻; 补一条 adaptive 档 + dangling id 的 SC (现有 SC-7(c) 走显式 checkpoints, 测不到) |
| 10 | `36cf2e53` | major | qa-engineer (1/5) | 回扫**全部**既有 SC 的 fixture 前提: SC-8 的期望值与其自带的注按新语义 (「config 未写的 key 经 adaptive_rules 推导」) 重算; 其余 fixture 逐条钉 `audit.mode` 或 proposal 头部 Level 行。这是 `2d7cccbe` / `506ce733` 的同族清扫, 建议一次做完并在 Tasks 里记为单独一项 |
| 11 | `c4610d6b` | major | qa-engineer (1/5) | 改写 `:85` / R-b (`:253`) / SC-22(1) (`:302`) 的失效方向论证 (陈旧 base ⇒ diff **超集** ⇒ 他人 change 被卷进作用域 ⇒ missing 假红 / `no_spec_contradicted` 误报), 并补一条作用域膨胀的负向 SC —— 当前真实方向零覆盖 |
| 12 | `affceac8` | major | qa-engineer (1/5) | B.0 (`:262`) 收窄为「只对 SC-2/SC-4 采样到的族做双列标注」, 并明写无人值守下两列不一致时的**机械处置规则** (阻断 / 降级 / 记 WARN 二选一), 不得留「供人裁」而无仲裁者; 同时订正「78 份有独立源」的低估 (实测 570/825) |
| 13 | `868def3b` | major | code-reviewer (1/5) | 新测试文件的风格成文: 按 `audit-engine/tests` 既有两条守卫 (`test_sibling_spec_probe.py:303-336`) 写成 **unittest** 套件, 全部 SC 的核验列由 pytest node-id 改为 `unittest` 方法路径; 或显式说明为何改用 pytest 并同步处置那两条守卫 (后者属改既有闸门, **须 owner 明示**) |
| 14 | `3bd0562f` | major | tech-lead (1/5) | 复议 #4 增列**版本级别**一问 (PATCH vs MINOR), 并把 §5 自述的两条配置行为反转 (收窄 `allow_incomplete_checkpoints` 豁免面 / 坏 config 由「返默认值」改 exit 2) 作为定级依据一并交 owner; 参照同仓 v1.73.0 (MINOR) 与并发轨 #195 的同类处置。**待 owner 复议** |
| 15 | `3b8bf6dd` | major | tech-lead, code-reviewer (2/5) | **待 owner 复议** (与复议 #7 同面, 建议合并裁决): 订正 (b) 的三例语料证据 (`2c8eaa6` 是 `.aria/decisions/` 反证, 不是支持), 并决定是否把 DEC (`.aria/decisions/**`、`docs/decisions/DEC-*`) 与 triage (`.aria/triage-*`) 两类 Phase A 产物纳入放行路径集 —— 现状是 (b) 在本仓规范工作流里只部分可达; 保留则须补对应反事实 SC |

Minor 13 条与 Decisions 14 条不入 rework 清单, 随稿修订即可。其中四条建议优先随手闭合 (成本一条命令或一处改写): `5c478b7a` 的 `:16` 全称句收窄 (CHANGELOG 引用行 `:3020`→`:3045`, 汇总席已实跑核对)、`6f7fb809` 的头部/Tasks 起分支 SHA (`301641b`→`f314785`)、`4217d903` 的两处引用锚点 (`#195 :352`→`:382-386`、`proposal-minimal :27-31`→`:28-32`)、`c41592b4` 的先例锚 (`execution-modes.md:152`→`archive/2026-09-04-sibling-spec-probe/proposal.md:513`)。另按 memory `feedback_author_and_verifier_must_differ_for_corrections`, **本轮 minor 的勘正批建议再次换非 v3 执笔者复核** —— `5c478b7a` 正是 R1 已勘正过、在 `:16` 又被写回的同一句。
