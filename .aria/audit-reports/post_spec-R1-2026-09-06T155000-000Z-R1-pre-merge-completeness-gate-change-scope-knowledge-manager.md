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
timestamp: 2026-09-06T16:42:26.904Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [knowledge-manager]
---

# post_spec 审计报告 — knowledge-manager (Round 1)

被审对象: `/home/dev/Aria/openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`
席位透镜: 知识与文档一致性 (头部机械判据 / Rule #3 同步面 / 与 standards + CLAUDE.md 规则冲突 / 术语与归档口径 / 引用真实性)

核验方式: proposal 自述一律不采信。所有 SOT 行号对插件缓存副本 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`, 并已用 `git show 301641b:<path>` 与该副本逐字节 diff (execution-modes.md / audit-engine SKILL.md / phase-c-integrator SKILL.md / report-storage.md / pre-write-validation.md / collectors/audit.py 六份**全部 SAME**), 基线冻结声明成立。

---

## 审计结论

### Decisions

- [decision] documentation/头部机械判据: `Linked Issue` 行合规。`cat -A` 核: `> **Linked Issue**: `\``10CG/Aria#199, 10CG/aria-plugin#161`\``, 满足 spec-drafter 写法三条 (同一 code span 内 `, ` 分隔 / 非 markdown 链接形 / `>` 后恰一空格)。紧随的 `> **Issue**:` 不在字段名封闭集 (`Linked Issue` / `关联 Issue`), 不会抢 E0 首条命中 (证据: /home/dev/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/skills/spec-drafter/SKILL.md:420-426)
- [decision] architecture/Rule #10 审计计划: 合规。`.aria/config.json` 实读 `post_brainstorm/mid_implementation/post_implementation/pre_merge/post_closure = off`, `post_spec/post_planning = convergence`, 与 proposal.md:12-13 声明逐项一致; 属白名单第一类 (配置显式关闭), 无自行豁免 (证据: /home/dev/Aria/.aria/config.json audit 块)
- [decision] testing/Rule #6 选行: **不构成 finding**。判据表第三行在本项目已有归档先例支撑同型情形 (套件存在但无 eval 到达该状态 ⇒ 照跑=测量剧场), 见 `openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:282-284` (3 evals + 7 fixtures + 2 evals 无一到达 `not_found`, 走第三行 + 三义务 + 缺口 issue #127)。本 spec 三义务齐备且 `ab-suite/audit-engine.json` 实测 2 evals、`grep -i "completeness|missing_checkpoint|allow_incomplete"` 零命中, 均已复核为真
- [decision] documentation/引用真实性: 全部命中。`10CG/Aria#199` (open) / `10CG/aria-plugin#161` (open, 标题与 proposal 引用逐字一致) / `10CG/aria-plugin#127` (open) / `10CG/Aria#177` (open) 经 `forgejo GET` 实查存在; 三条归档先例目录均存在; `.aria/triage-comment-199.md` 与 `triage-report-199.json` 存在且 case-1/case-2 与 proposal §Why 表述一致
- [decision] documentation/语料统计: F1 / F2 / F8 复核全部为真。`pre_merge=off` ✓; `.aria/audit-reports` 780 entries (778 `.md`), `post_spec` 499 / `post_planning` 209 / `post_implementation` 3 (三者归属 id 与 proposal 逐字一致) ✓; 非 `-R\d+-` 计数 24/2/1/1 逐项吻合 ✓; `aria-orchestrator` 与 `aria-orchestrator-divestiture` 为唯一前缀碰撞对 ✓; `.aria/config.template.json` 无 `audit` 块、`config-loader/DEFAULTS.json` 的 audit 键集不含 `allow_incomplete_checkpoints` / `allow_dangling_change_ids` ✓
- [decision] documentation/术语与归档口径: `not_applicable` reason 采 kebab-case、`error_kind` 采 snake_case, 分别与 `path_coverage.py` 的 `no-triggering-paths` 与 `sibling_spec_probe` 的 `auth_403` 族一致; 脚本级 `verdict` 用本地封闭集 (非报告的 PASS/FAIL 体系) 亦有 `sibling_spec_probe` 先例, 不构成术语碰撞

### Issues

- [critical] implementation/proposal.md §1.2 归属匹配规则: 匹配只认双侧连字符 `-{change_id}-`, 漏掉 change_id 落在**末段**的 `...-{change_id}.md` 形态。对本仓 778 份 `.md` 实跑归属判定: **63 份 (8.1%) 命中不了**, 其中包含**全部 3 份 `post_implementation` 报告** (`post_implementation-R1-2026-04-24T1000Z-state-scanner-mechanical-t3.md` 等), 以及 `pre_merge-R1-2026-04-24T0000Z-state-scanner-mechanical.md` 等。更糟: 按 §1.2 末句对 `excluded_legacy_count` 的定义 (「以 `{checkpoint}-` 开头但不含任何 `-{c}-`」), 这 63 份会被**记成 legacy**, 于是 R-a 的缓解手段 (legacy 计数显影) 反而把误判藏起来。SC-2 选的 id `pre-merge-gate-no-run-for-branch` 实测 72 份报告 **72/72 均为双侧形态**, 该 fixture 结构上不可能红 (证据: proposal.md:98,101,186; /home/dev/Aria/.aria/audit-reports/)
- [critical] architecture/proposal.md §1.3 not_applicable 判据 (b): 复用 `audit.scope_skip_paths` 判 `post_implementation` / `mid_implementation` 为 not_applicable, 等于**放行一个 owner 已 enabled 的闸门**。三重冲突: (1) 该键 SOT 只有一种语义 —— 「**降级非 skip** (DEC-4): issue #58 实证 deploy script 改动 challenge 能找到真退化 → deploy 不能全 skip, convergence 保留安全网」; (2) (b) 自带前提「diff 非空」⇒ 被审对象**已产生**, 落在 Rule #10 白名单第四类的**禁止侧** (「A.2 做了但很简单」不合法); (3) 默认 `scope_skip_paths` 含 `*.md` 与 `deploy/` —— 对 aria-plugin 这种**产品本体就是 markdown 处方**的仓, (b) 会成为常态通道。且既有 owner 裁定已就同型问题判过: 「归进 `not_applicable` = 合并未经 CI 的 path-matched 变更 = fail-open, 且污染语义封闭集」, 而本 spec 恰恰引用该归档作标杆。逻辑上 (b) 也**没有合法触发场景**: 文档型 diff 下 post_implementation 仍会按 convergence 正常跑并产出报告 ⇒ 命中 `present`; (b) 唯一会被触发的时刻就是「本该跑却被跳了」(证据: /home/dev/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/skills/audit-engine/SKILL.md:398-400,412-419; /home/dev/Aria/standards/conventions/configured-gate-authority.md:38,40; /home/dev/Aria/openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:29,57; DEFAULTS.json:118)
- [major] architecture/proposal.md §1.3 not_applicable 判据 (c): 「`tasks.md` 与 `detailed-tasks.yaml` 都不存在 ⇒ A.2 未执行」的代理判据未对真实值域校准。post_planning 启用日 (2026-07-04, config `_comment` 记载) 之后归档的 **28 个 change 里 9 个 (32%)** 两文件皆无, 抽查其中 3 个却都有 inline `## Tasks` 勾选清单 (`2026-07-11-secret-guard-bash3-multiline-hardening` 9 条且自标 Spec Level 3 / `2026-07-16-state-scanner-snapshot-stderr-secret-leak` 14 条 / `2026-08-21-subprocess-decode-hardening` 11 条)。**本 spec 自身**也是这一形态 (10 条 inline 任务, 无 tasks.md), 却在 proposal.md:13 声明要跑 post_planning —— 即「A.2 做了, 产物在 proposal.md 里」, 正是 Rule #10 边界注禁止当豁免的那一侧。SC-11 把 post_planning 的期望写成「`present` 或 `not_applicable`」二选一, 无法区分这两种状态 (证据: proposal.md:110,190,195; /home/dev/Aria/openspec/archive/2026-08-21-subprocess-decode-hardening/proposal.md)
- [major] documentation/proposal.md §4 文档同步面 (Rule #3) + SC-13: 旧 report schema 的散文残留全仓共 **4 处**, 本 spec 只勘正 1 处。未列入的三处形态逐字同构: `phase-a-planner/SKILL.md:267` (`post_spec-{timestamp}.md`) / `phase-b-developer/SKILL.md:204` (`mid_implementation-{timestamp}.md`) / `:277` (`post_implementation-{timestamp}.md`); SC-13 的机检也只钉 `phase-c-integrator:157`, 修完仍留三份误导性范例 (符号清扫须穷举形态族)。另: (b) 实质给 `audit.scope_skip_paths` 加了第二个、且更强的消费语义, 而该键的用户文档 SOT `config-loader/config-example.md:365-367` 明文写着「降级 ... **不 skip**」, 未进同步表 (此条随 (b) 的处置而定) (证据: proposal.md:136,142-148,197; 四处残留经 `grep -rn "audit-reports/[a-z_]*-{timestamp}"` 全树枚举)
- [minor] documentation/proposal.md 头部与 §Why: 5 处引用失准, 均不影响结论但影响可核对性。(1) 根因 2 称 pre_merge 的 context 在 `phase-c-integrator/SKILL.md:137`, 实为 `:136` (`:137` 是「5. 处理 verdict」); (2) 称 post_spec 链在 `phase-a-planner/SKILL.md:248` 传 proposal 路径, 实为 `:250`; (3) F3 写「archive 144 去日期」, 实为 143 个目录 + 1 份 `README.md`, 与其自报总数 150 也对不上; (4) 两处称 `ab-suite/audit-engine.json` 为 v1.3.0, 该文件自身 `version` 字段是 **1.0.0**, 1.3.0 是 `ab-suite/version.yaml` 里引入它的那条 changelog (§4 写的 1.4.0 → 1.5.0 才是套件版本, 两处口径不一致); (5) 基线冻结行断言「`git diff --stat 0545f86 301641b` 对本 spec 全部触点文件为空 ⇒ 两 SHA 行号一致」, 但触点之一 `aria/CHANGELOG.md` 在两 SHA 间 +71 行, §5 引的 `CHANGELOG.md:3020` 在 `0545f86` 上实为 `:2949` (证据: proposal.md:9,11,40,48,152)

### Risks

- [risk] documentation/文件名归属的固有有损性: 除上述 63 份末段形态外, 另有 **184 份**报告文件名不含任何现存 change_id 的连字符界定形态 —— 抽样可见写侧曾写入**截断/别名 id** (`dispatch-input-delivery` 之于 `aria-2.0-m6-dispatch-input-delivery`, `phase-c-gate-path-coverage`, `us024-m4`, `agent-router-injection`)。这些既非旧 schema 也不可归属, 却会一律进 `excluded_legacy_count`。建议 Phase B 给该计数**再拆一档** (`unattributable_count`) 并在 audit trail 分列, 否则「legacy 不计入: N」这行会同时吸收三类完全不同的成因
- [risk] architecture/R-b 自证强度 (proposal 已自认): `--no-spec` 的交叉核验只到「diff 不触 `openspec/changes/**`」。本仓常态是 spec 先落 master、代码后跟, 该形态下 Level 2 分支同样不触 change 目录 ⇒ 误声明可通过。proposal 的缓解 (进 audit trail 事后核对) 只在有人真去核对时成立
- [risk] documentation/Rule #6 第三行的可证伪实证口径: SC-14 写「回退本 spec 后该 eval 的 with 臂**应转差**」, 而 SOT §3 第 2 条要求「必须**转红**」。descriptive + LLM-judge 形态下「转红」无二值定义, 建议在 ab-results README 里预先写死判据 (哪条 expectation 失分即算红), 否则该实证事后可被任意解释

### 待 owner 复议 (本席新增, 与 proposal 已列 4 条并列)

1. **not_applicable 通道是否整体保留**: 若采纳 Critical-2 / Major-1, 建议只保留一条真正结构性的通道 —— 「本分支 diff **仅**触 `openspec/changes/{id}/**`」(纯 Phase A, Phase B 整个未发生), 删除 (b), 并把 (c) 的判据从「A.2 产物文件是否存在」改为「是否存在**任何** A.2 产物 (含 proposal.md 的 `## Tasks` 小节)」。issue 修法 2 原文要的也正是「Phase A-only 的 PR」这一窄义, 是 triage 与本 spec 逐级放宽到了 `scope_skip_paths`
2. **excluded_legacy_count 是否拆档**: 见 Risks 第 1 条; 拆档会改 §1.4 stdout 契约顶层键集 (SC-10 逐字断言), 属需要 owner 拍板的契约面变更
3. **同类旧 schema 残留的清扫边界**: 三处他 Skill 残留 (`phase-a-planner:267` / `phase-b-developer:204,277`) 是随本 spec 一并勘正 (描述性, substitute 已覆盖), 还是另开 Level 1

---

## Verdict

**FAIL** — Critical 2 / Major 2 / Minor 1。

rationale: 两条 Critical 均**不是措辞问题, 而是会让新门在真实语料上失效**, 且都用本仓真数据机械复核过:

- Critical-1 打的是本 spec 的**核心资产** (归属匹配规则)。规则在本仓 778 份语料上漏判 63 份、含全部 3 份 `post_implementation`, 修完之后的门会对这些 change 判假红拒绝合并, 而 `excluded_legacy_count` 这条本来用来兜 R-a 的显影反而把误判伪装成「旧 schema」。SC-2 因取样 id 的报告 72/72 都是双侧形态, 结构上不可能把它测出来 —— 这是「SC 对着规则自身写、而非对着 ground truth 写」的恒绿型。
- Critical-2 打的是**方案的正当性**: 用一个 SOT 明文「降级非 skip」的判据去放行 owner 已 enabled 的 checkpoint, 落在 Rule #10 白名单的禁止侧, 且与本 spec 自己引作标杆的那份 owner 裁定 (2026-08-22, 「该跑而没跑」不得归 not_applicable 放行) 正面相反。按审计要点「横切检查原则 · 数据可用性」的载重条款, 这类事实/前提性错误必须对 verdict 载重, 不能只记一笔。

post_spec 为 `blocking: false`, 该 FAIL 不硬阻断流程, 但按 Rule #10 不得被 AI 自行降格处理: Critical-1 需改匹配规则并重做 SC-2 的 fixture 形态族; Critical-2 与 Major-1 需要 owner 就「not_applicable 通道是否保留 / 收窄到什么形态」拍板后再进 Phase B。Major-2 与 Minor 可在下一轮随稿修订。

肯定面 (不因 FAIL 抹掉): 基线冻结做到了逐字节可核 (六份 SOT 副本与 `301641b` diff 全空), F1/F2/F8 的语料数字与 issue/precedent 引用**全部经独立复核为真**, Rule #6 选行有归档先例支撑, Rule #10 审计计划合规。这份 spec 的事实底盘扎实, 问题集中在两个判据的形态设计与一处 SC 自指。

---

## 轮次记录

### Round 1

- Agents: knowledge-manager (五席之一, 本报告仅本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 11 条 (Decisions 6 / Issues 5); 另附 Risks 3 条与待 owner 复议 3 条, 均不计入 finding 计数
- Vote: REVISE (Critical 2 + Major 2 > 0)
