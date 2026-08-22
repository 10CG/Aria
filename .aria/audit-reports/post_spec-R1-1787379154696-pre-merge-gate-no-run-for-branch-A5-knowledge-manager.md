---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T06:44:15.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 4
minor_count: 2
---

## 摘要

A5 席 (knowledge-manager 透镜) 对 `pre-merge-gate-no-run-for-branch` proposal.md 的文档一致性 / SOT 对齐 /
方法论合规 / 知识沉淀四方面复核。**Level 判定、Status 行机读格式、Rule #10 brainstorm 豁免、BA-8/#122/#126/#137
引用** 四项实读核验均**准确**, 无发现。但发现 **4 条 Major**, 集中在「本 spec 会让既有知识资产变得更不准确, 而
spec 自己的同步面清单没安排修正」这一类: (1) issue #152 自己引的 `DEC-20260731-001` 核心语义声明被本 spec
证伪, spec 全文零处引用/修正该 DEC; (2) F3 (aria-plugin `pull_request` 触发面因硬约束 1 结构性死亡) 满足
traps 文件收录判据但未列入拟议第六节, 随 proposal 归档即从活文档消失; (3) 本 session 独立探针实测推翻了
project 既有 canonical reference memory 的一句关键断言 (`workflow_dispatch` 路由存在, 而非「不可用」), 而
该断言正是 AD-5 处方 1 生效的前提, spec 未安排纠正; (4) 版本同步面措辞沿用 CLAUDE.md 已被 Aria#177 判定
「文件数口径」有误的「5 文件」框架, 亲测 `marketplace.json` 确有 2 个 version 字段印证 #177 的指控。另有
2 条 Minor (kind 命名体系消歧 / issue #152 归档时机的收尾留言未安排)。

## Findings

### [A5-M1] Major — Issue #152 引用的 `DEC-20260731-001` 核心语义声明被本 spec 证伪, proposal 全文零引用/零修正

**锚点**: `docs/decisions/DEC-20260731-001-c24-wait-adjudication-retirement.md` §退役裁定; 对照
`openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` 全文 (`grep -c "DEC-" proposal.md` = 0)。

**问题**: `DEC-20260731-001` 是本项目「决策存档」类文档 (性质与 append-only 的 VERSION/CHANGELOG 不同 ——
它写的是**现行语义声明**, 不是历史流水账), 其 §退役裁定原文逐字断言:

> 「此后 **verdict=wait 真正意味着「CI 在跑或该跑没跑完」**, 按 workflow-runner wait 正常处理。」

而本 spec 所修的 issue #152 正文自己就写着 (本 spec Why 段完整复核过该 issue):

> 「`DEC-20260731-001` 的语义「verdict=wait = CI 在跑或该跑没跑完」在此组合下**不成立** —— 没有任何东西在跑或会跑。」

也就是说: **issue #152 的存在本身就是对 `DEC-20260731-001` 核心声明的一次反例, 而本 spec 是修复该反例的
正式变更**。但 proposal.md 的 Design Decisions / Cross-references / Success Criteria 全文**零处**提及
`DEC-20260731-001`。对照 `phase-c-gate-path-coverage-not-applicable` (#122) 先例 —— 那次 Spec 落地后, 项目
主动**创建了** `DEC-20260731-001` 本身去存档并退役此前的过渡规则; 本 spec 处在完全对称的位置 (它进一步限缩
了 `DEC-20260731-001` 刚确立的语义), 却没有对称地处理。

**实测证据**: `grep -rn "DEC-20260731" openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` 零命中；
`docs/decisions/DEC-20260731-001-*.md` 本身也没有 (也不可能有, 因为它写于 2026-07-31, 早于 #152 立案)。

**按 spec 实施会怎样错**: v1.66.4 ship 后, `DEC-20260731-001` 作为项目「判例链」的一环继续原样存在, 其
「verdict=wait 真正意味着 CI 在跑或该跑没跑完」的断言对新增的 `no-run-for-branch` 场景**不再完整成立**
(此时 `wait` 还可能意味着「结构性零 run, 处方待执行」)。未来任何人 (含 AI agent) 排查「gate 又卡在 wait」
时若信了这条 DEC 的字面 (它是被刻意写成「退役裁定」= 定案语气, 不像临时笔记那样自带「可能过时」的心理预期),
会重蹈 2026-08-19/20 的「误诊为 runner 停摆」覆辙 —— 而这正是 #152 本欲根治的那类事故。DEC 文档因此发生
**永久性文档-事实漂移** (Rule #3 精神: 架构/决策文档须与系统行为一致), 且不会被任何机制标记出来 (DEC 目录
无 custom check 覆盖)。

**建议**: 在 Cross-references 新增一条指向 `DEC-20260731-001`, 并在 §5 文档同步面里加一项: 于该 DEC 文件
追加一段仿照 `version-management.md` 「🔴 2026-08-16 更正」/ memory 「⚠️ 更正」的**同款就地纠偏批注**
(不改写原文, 只追加「2026-08-2X 补充: 本声明在 `no-run-for-branch` 组合下不完整, 见 aria-plugin#152 / 本
proposal」), 使判例链不因本次修复而悄悄断裂。

---

### [A5-M2] Major — F3 (`pull_request` 触发面结构性死亡) 满足 traps 文件收录判据, 但未列入拟议第六节, 随 proposal 归档即从活文档消失

**锚点**: proposal.md「起草期复核补充的三条事实」表 F3 行; 对照 `aria/skills/phase-c-integrator/references/pre-merge-gate-empirical-traps.md` 现有五节 + 本 spec §5 对第六节的拟议措辞。

**问题**: proposal.md 自己论证 F3 (「aria-plugin 自 2026-07-20 起按 CLAUDE.md 硬约束 1 本地合并不开 PR ⇒
`pull_request` 触发面在本流程结构性死亡, 只剩 `push` 事件, 盲区对 aria-plugin 是每条新分支恒中, 不是偶发」)
是「issue 没写、改变修法落点」的三条关键事实之一, 且其出处是**本 session 实查** Forgejo PR 历史 (`forgejo
GET .../pulls?state=closed`) —— 本席已独立复核, `#115` (2026-07-19 merged) 确为最近一次合并, 之后无任何新
PR, 与 F3 描述一致。

但 §5「文档同步面」给 `pre-merge-gate-empirical-traps.md` 新增第六节拟定的内容是:

> 「F1 + `/actions/tasks` 只列已领任务 + Forgejo 新分支 push 不评 paths」

**F3 不在这三项里。** 而 traps 文件自己的收录判据 (文件头逐字): 「每一条都是实测踩出来的, 没有一条能靠读
代码想出来」—— F3 恰好满足: 它不是读 `pre_merge_gate.py` 能推出来的, 而是要去 Forgejo API 拉 PR 历史才知道
的运营事实, 且它是本 issue 「为什么这个盲区对 aria-plugin 特别致命 (每条新分支恒中)」的**根因性**解释,
比第六节现有三条更贴近「为什么会有 #152」这一节 (对比 traps 文件既有「五、这道 gate 的根本形状」一节的写法
——那正是给 #137 的根因写的独立小节, F3 之于 #152 是同等地位的角色)。

**按 spec 实施会怎样错**: proposal.md 归档后 (`openspec/archive/`), F3 这条事实只存在于一份不会再被主动
翻阅的归档文档里。未来工程师 (或 AI) 遇到「这条新分支的 gate 又卡住了」时, 会去读 `pre-merge-gate-empirical-traps.md` (SKILL.md 明文指引「改这段代码前先读」), 但读不到「为什么这在 aria-plugin 上是常态而非偶发」
这一关键背景, 只能重新去查一遍 PR 历史才能重新拼出 F3 —— 这正是 traps 文件存在的目的 (省下这次重新调查)
被本次遗漏抵消。

**建议**: 第六节内容补 F3 一条 (可与「Forgejo 新分支 push 不评 paths」合并成因果链: 「本仓只剩 push 触发
(因本地合并不开 PR) → push 触发面偏偏是新分支首推会被静默跳过的那个」), 使第六节完整覆盖 issue 论证链而
非只覆盖症状层。

---

### [A5-M3] Major — 本 session 独立探针推翻既有 canonical reference memory 的关键断言, 而该断言正是 AD-5 处方 1 生效的前提; spec 未安排修正

**锚点**: memory `reference_forgejo_new_branch_paths_filter_no_run.md` (2026-08-20 写入) 一句 ——
「`workflow_dispatch` API 在 gitea-1.22 系不可用」; 对照 proposal.md AD-5 (「处方优先 `workflow_dispatch`」)
与 Risks §R-c (「本 session 探针: body `{"ref":""}` → HTTP 400 `ref is empty`, 证实路由与参数名」)。

**问题**: 我独立重跑了 R-c 描述的探针 (只读/无副作用的路由存在性验证, 未真正触发 dispatch):

```
GET  /repos/10CG/aria-plugin/actions/runs        → HTTP 404 (list 端点确认不存在)
GET  /repos/10CG/aria-plugin/actions/workflows   → HTTP 404 (list 端点确认不存在)
POST /repos/10CG/aria-plugin/actions/workflows/issue-triage-tests.yml/dispatches
     -d '{"ref":""}'                              → HTTP 400 {"message":"ref is empty", ...}
```

三个结果与 proposal.md R-c 的描述**完全一致** —— **dispatch 路由确实存在** (400 是参数校验失败, 不是路由
不存在的 404)。这与项目现有 memory `reference_forgejo_new_branch_paths_filter_no_run.md` (2026-08-20, 即
#152 立案当天写入, 被列为本次审计基线材料之一) 的断言**直接矛盾**: 该 memory 写「`workflow_dispatch` API
在 gitea-1.22 系不可用」, 未加限定, 读起来是对整个 API 的否定, 而非仅对 list 端点的否定。

两者的合理调和: 2026-08-20 写 memory 时大概率是探测了 `GET /actions/workflows` (试图先列出 workflow 再选,
即 AD-5 附带说明里提到的「不能先列表再选」那条自然写法) 得到 404, 就把「dispatch 不可用」当成结论写下 ——
**混淆了「列表端点不存在」与「dispatch 端点不存在」两件事**, 而这正是 R-c 段专门警告的坑
(「`workflow_id` 按文件名寻址, 因 `/actions/workflows` 列表端点 404 —— 处方 1 须直接用
`path_coverage.dispatchable_workflows` 里的文件名, 不能先列表再选」)。

**按 spec 实施会怎样错**: AD-5 (「处方优先 `workflow_dispatch`, 次选实质 commit」) 的整个优先级设计**建立在
「dispatch 可用」这一前提上**。该 memory 作为 `reference_*` 类型 (项目定义为「速查参考」, 会被后续 session
直接信任引用 —— 本次我自己就是被要求以它作基线材料之一), 若不修正, 未来任何 session (含实现本 spec 的
Phase B session) 读到它会认为「`workflow_dispatch` 反正不可用, AD-5 处方 1 走不通」, 从而**跳过处方 1 直接
落处方 2 (推实质 commit)**, 使本 spec 精心设计的「零历史污染」优先级 (AD-5 原文语) 在实现阶段被这条未修正
的 memory 悄悄架空 —— 且这不会报错, 只会安静地退化成「每次都推测试 commit」, 审计也很难从代码本身看出这
是因为一条 memory 断言错了。

**建议**: §5 文档同步面加一项 —— 更新该 memory, 把断言收窄为「`GET /actions/workflows` (列表) 与
`GET /actions/runs` (列表) 在 gitea-1.22 系 404; `POST .../workflows/{file}/dispatches` (单个 dispatch,
按文件名寻址) **存在且校验参数** (2026-08-22 复测, HTTP 400 非 404)」, 并保留原「误诊」教训段不变。

---

### [A5-M4] Major — 版本同步面措辞沿用 CLAUDE.md 已被 Aria#177 判定「文件数口径」有误的「5 文件」框架

**锚点**: proposal.md §5 「`aria/CHANGELOG.md` + 5 文件版本同步面 (PATCH: 行为修复, 无新 Skill)」与 Impact
「版本: aria-plugin PATCH (v1.66.4)」; 对照 CLAUDE.md §版本管理「发布同步面: aria 子模块 5 文件 + …」一行;
对照 `forgejo GET /repos/10CG/Aria/issues/177` (本席实读, open)。

**问题**: Aria#177 (open, 未关) 逐条实测指控 CLAUDE.md 那一行「四错一行」, 其中明确点名 **aria 子模块侧**:

> 「另: aria 子模块侧「5 文件」同样是文件数口径 —— `.claude-plugin/marketplace.json` 含 **2** 个 `version`
> 字段 (`:3` / `:16`); 且 `aria/VERSION` 与 `aria/CHANGELOG.md` 是 append-only 发布账本 …它们的不变量与
> 普通引用文件不同, 不能同口径处理。」

我独立核验 `aria/.claude-plugin/marketplace.json`, 确认 `:3`(顶层 `version`) 与 `:16`
(`plugins[].version`) 两处均为 `"1.66.3"` —— #177 的指控**属实**。本 spec 的 Impact/§5 原样沿用「5 文件」
这个已被开 issue 挂起未修的口径, 没有按 #177 指出的正确维度 (版本**引用点**数, 而非文件数) 重新表述, 也
没有专门点出 `marketplace.json` 内部两处引用点这一具体已知坑。

**按 spec 实施会怎样错**: 执行 Phase C/D 版本 bump 时, 若操作者 (AI 或人) 按字面「5 文件」逐**文件**过一遍
(而非逐**引用点**过一遍), `marketplace.json` 算一个文件、「改完」就划勾, 但该文件内两处 `version` 字段中
若只 sed/手改了一处 (`:3` 顶层, 常见于只改「看得见」的那处), 另一处 (`:16`, 嵌套在 `plugins[]` 里) 会静默
残留 `1.66.3`。现有机械兜底 `m6-version-badge-match` / `i18n-readme-translation-currency` 两条 custom
check **只查主仓 README/i18n**, 对 aria 子模块自己文件内部的双字段一致性**零覆盖** —— #177 原文同一句话点
名的「假绿」在这里同样成立: 没有任何检查会告诉你 `marketplace.json` 内部两处漂移了。这与 #177 描述的
「三次复发、每次都只修当次实例」是同一形状的第四次机会。

**建议**: §5 该行改写为「`aria/CHANGELOG.md` 新条目 + 版本引用点同步 (`plugin.json` SOT / `marketplace.json`
**两处** `version` 字段 `:3`+`:16` / `VERSION` / `README.md` `**Version**:` 行), 按 Aria#177 指出的引用点
口径逐点核对, 不按文件数打勾」, 并在 Cross-references 挂 `Aria#177` 说明本 spec 的版本 bump 步骤有意采用
#177 的更正口径而非 CLAUDE.md 现有措辞。

---

### [A5-m1] Minor — `gate_error.kind` 命名体系: `not_found`(backend 态) / `*-not-found`(kind 族) 同词异义, 若采纳 A1 的 `pr-branch-not-found` 会形成三个易混词

**锚点**: proposal.md §2 `pr_ci_status` 新增值 `not_found`; 既有 `gate_error.kind` 枚举
`main-branch-not-found` / `main-branch-verify-failed`; 本 spec 新增 `no-run-for-branch`。

**问题**: 同一个英文短语「not found」在两层被用来表达**不同的存在性对象**:

| 层 | 值 | 「not found」修饰的对象 | 该分支真实语义 |
|---|---|---|---|
| backend (`CIStatus.state`) | `not_found` | CI **run** | 分支存在, 只是零 run |
| gate_error kind (既有) | `main-branch-not-found` | **main 分支引用** | 分支本身在远端不存在 |
| gate_error kind (若采纳 A1 建议) | `pr-branch-not-found` | **PR 分支引用** | 分支本身在远端不存在 |
| gate_error kind (本 spec 新增) | `no-run-for-branch` | 分支上的 **run** | 分支存在, 只是零 run (与 backend `not_found` 同义, 换了个词序) |

`not_found`(backend, 主语=run) 与 `main-branch-not-found`/`pr-branch-not-found`(kind, 主语=分支) 用相同
词根表达**正交的两件事** (「run 有没有」vs「分支有没有」), 而本 spec 新 kind 刻意选了 `no-run-for-branch`
(把「run」放前面) 来避免和「分支不存在」撞车 —— 这个设计选择本身是对的, 但若 A1 建议的 `pr-branch-not-found`
被采纳, 四个 kind 里会同时出现 `main-branch-not-found` / `pr-branch-not-found` (风格一致, 都是「分支不存在」)
和 `no-run-for-branch` (风格不同, 是「分支存在但零 run」) —— 一个只看词形不看词序的读者 (或者未来做字符串
包含判断的代码) 容易把 `no-run-for-branch` 和 `*-branch-not-found` 归成一类。

**按 spec 实施会怎样错**: 未来排查 (含本 issue 已发生过一次的「误诊为 runner 停摆」) 时, 若工程师看到日志里
一个 `*branch*not-found*` 形状的 kind 就假定「分支不存在」而去查分支名/权限, 而不细读具体是 `no-run-for-branch`
还是 `pr-branch-not-found`, 会走错排查方向 —— 与 #126 修复的问题 (`internal-error` 必须自成一档、不能被
笼统归类) 是同一类风险,只是换了个位置。

**建议**: SKILL.md 在 `gate_error.kind` 枚举文档处加一张两维消歧小表 (「分支是否存在」×「run 是否存在」),
明确 `no-run-for-branch` 位于「分支存在, run 不存在」象限, 与「分支不存在」两个 kind 正交; 若 A1 的
`pr-branch-not-found` 被采纳, 命名规则建议统一改为 `{subject}-missing` vs `{subject}-has-no-runs` 这类更
不易望文生义混淆的词根, 而非都挤在 "not-found"/"no-run" 这两个高度相似的短语里。

---

### [A5-m2] Minor — Issue #152 归档时的收尾留言未在 spec 中安排

**锚点**: proposal.md 全文 vs `forgejo GET /repos/10CG/aria-plugin/issues/152` (当前 0 条评论, open)。

**问题**: 抽查同类先例 #137 与 #122 (均 100% 命中): 两者都在机制 ship 后, 于原 issue 下**补一条总结评论**
(引用交付 commit SHA、说明「已随 vX.Y.Z 落地」)。#152 目前 0 评论。本 spec 的 owner 裁定 `A′` 是「issue 原
三候选之外的合并项」——这一点对未来只看 issue、不看归档 proposal 的读者尤其重要 (issue 正文的「修法候选
(未定)」段仍原样挂着 A/B/C 三项, 不会自动更新), 若不专门留言说明「最终既不是 A 也不是 B/C, 而是 A′」,
issue 历史会显得「有三个候选, 却查不到选了哪个/ 为什么」。

**建议**: proposal.md 的 Cross-references 或 D.2 环节提醒补一条 issue 评论, 内容至少包含: 与三候选的关系
(比照 A 但去掉 `not_applicable` 放行、借用 B 的处方文字)、交付 SHA、`gate_error.kind` 最终命名。此项不违反
任何成文规则 (无强制条款), 按经验先例列为 Minor 建议而非 Major。

## 未发现问题但已核验的点

- **Level 判定与 `standards/openspec/project.md` 一致**: Level 2 → 交付物 = `proposal.md` (无 `tasks.md`)
  —— proposal.md 确实只产出这一份文档, 与 project.md 「Level 2 | Minimal | … | proposal.md」逐字一致。
- **Status 行机读可解析**: 实读 `aria/skills/state-scanner/lib/collectors/_status.py` 的
  `_STATUS_PATTERNS`/`_status_lifecycle_head`/`_normalize_status` — proposal.md 的
  `> **Status**: 📝 **Draft (v1)** — A.1 起草, 待 post_spec convergence 审计` 命中 pattern 3
  (`^>\s*\*\*Status\*\*[：:]\s*(.+?)\s*$`), lifecycle-head 分离在首个 em-dash 处截断为
  `📝 **Draft (v1)**`, 含 `draft` token → 归一化为 `pending`。与先例 `secret-guard-manifest-precision`
  (#179) 的 Status 行 (`Draft (v3) — post_spec CONVERGED …`) 走同一路径, 无格式风险。
- **Rule #10 「未跑 brainstorm」自述是否构成自行豁免 — 结论: 不构成, 且引用恰当**: 核对
  `standards/conventions/configured-gate-authority.md` §1 「适用面: 审计检查点 (audit checkpoints)、
  CI/pre-merge gate、必跑的 review、强制的测试套件」—— brainstorm A.0.5 是 workflow-runner 编排里的
  **可选** 步骤 (触发依据是需求是否含糊, 非「config 声明为开」的闸门), 不落在 Rule #10 §2 白名单四类的
  讨论范围内 (它甚至不是 Rule #10 管辖的那类对象), 因此谈不上「该按哪一类白名单豁免」这个问题本身;
  `.aria/config.json` 的 `audit.checkpoints.post_brainstorm: "off"` 管的是「brainstorm 产物**事后审计**」
  这另一件事, 也不是「brainstorm 该不该跑」。但该文档 §5「配套习惯」明文要求「AI **任何**自作主张的流程
  判断…无论是否落在 §2 白名单内, 都必须在 session handoff 中显式写出」—— proposal.md 头部「此为 AI 流程
  判断, handoff 留痕请复议 (Rule #10)」正是履行这条 §5 义务 (handoff 尚未写是因为本 session 未收尾, 非
  遗漏)。结论: **该自述做法正确, 引用「Rule #10」在精神上站得住 (§5 与 Rule #10 同源同文件), 但严格讲更
  精确的引用应指向 configured-gate-authority.md §5 而非笼统写「Rule #10」—— 未达到需要单独开 finding 的
  程度**。
- **`BA-8` 引用准确**: 核对 `openspec/changes/phase-c-integrator-ci-path-coverage/REMEDIATION-DESIGN-A3.md:192` —— `BA-8` 原始定义正是「`compute_verdict` 写显式分支, 不依赖 fallthrough 隐式兜底」,
  本 spec 「新增显式分支 (BA-8 同款)」援引准确, 场景同构 (`not_applicable` → `not_found`)。
- **`#122`/`#126`/`#137` 三个 issue 引用均准确**: 逐条向 Forgejo 实读确认 —— #122 = path coverage
  `not_applicable` 语义 SOT (已 closed, v1.65.0 ship 记录完整); #126 = `internal-error` 自成一档可辨性
  原则 (已 closed, v1.65.3 ship); #137 = main 分支存在性核验 + `gate_error` 副本通道 (open, v1.66.0 已修
  一半, traps 文件 §五末段明确留痕「本次修复只加固了 `gate_check()` 这一份实现, SKILL.md 散文流程那份未
  修, 不得认为 #137 已闭环」——本 spec 未触碰该遗留缺口, 在 Out of Scope 范围内, 不构成新问题)。
- **`aria-plugin#115` 是硬约束 1 生效后 (2026-07-20) 最后一次合并 PR 的说法准确**: 实读
  `GET /repos/10CG/aria-plugin/pulls?state=closed&sort=id&direction=desc` 前 10 条, `#115`
  (2026-07-19T16:15:12Z merged) 后再无任何 PR, 与 F3 论证一致。
- **`docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md` §教训 4 引用准确**:
  实读该文件 §3「事故与教训」第 4 条, 文字与 proposal.md 附注（`/actions/tasks` 只列已被领走任务）逐句对应。
- **`aria/CHANGELOG.md` 当前版本 (`1.66.3`) 与 `plugin.json`/`VERSION`/`README.md` 现状一致**: 实读确认
  升版起点无误, PATCH → `v1.66.4` 的目标版本号计算正确 (无新 Skill, 纯行为修复)。

## Verdict

**verdict**: PASS_WITH_WARNINGS (0 Critical / 4 Major / 2 Minor)
**vote**: REVISE

4 条 Major 有一个共同形状: **本 spec 的存在本身会让另外几份已发布的知识资产 (一份 DEC、一条 traps 文件、
一条 canonical memory、CLAUDE.md 的版本同步措辞) 变得更不准确, 而 spec 自己规划的「文档同步面」清单没有
覆盖到这几处**。这类遗漏不影响代码是否能正确工作 (backend/gate 逻辑本身的问题已由 A1-A4 报过), 但会在
ship 后留下静默的知识漂移, 且往往正是「误诊」的温床 —— 本 issue 的起源就是一次误诊。建议 R2 前补齐
§5 同步面的这四处, 其余 Minor 建议顺手带上。
