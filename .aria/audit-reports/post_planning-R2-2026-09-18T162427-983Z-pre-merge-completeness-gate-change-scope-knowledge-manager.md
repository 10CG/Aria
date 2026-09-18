---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-18T17:33:51.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (全文, 224 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (全文, 1613 行, 含 `metadata` 全部子键与 `tasks:` 下 TASK-001~031 全部 31 项)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (全文, 565 行, 逐段读: Why / What §1.0–§5 / Impact / Tasks 17 项 / Success Criteria SC-1~SC-22 / rule6_note / 待 owner 复议 条目 0 + #1–#13 / References)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文, §1–§5)
- `CLAUDE.md` (系统提示内嵌全文, 「多远程推送」两条硬约束、不可协商规则 #3/#6/#8/#10、§版本管理)
- `standards/conventions/content-integrity.md` §4.4 / §4.5 (实读, standards 当前 checkout `940cb5b`)
- `.aria/state-checks.yaml` 相关条目: `main-project-version-consistency` (:325–352)、`m6-version-badge-match` (:124–138)、`i18n-readme-translation-currency` (:177–211 区)、`plugin-version-arch-docs-match` (:408–433)、`no-unresolved-version-placeholder` (:28–46)
- `.aria/probes/main-project-version-consistency.py` (全文 POINTS 清单)
- `VERSION` (主仓根, 全文 37 行)
- `aria/skills/phase-c-integrator/SKILL.md` 实读行 :50-60 / :125-140 / :748-758 (aria 子模块 `1cb3872`)
- `aria/skills/audit-engine/SKILL.md` 实读行 :415-428
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` 实读 `_CHECKBOX_ANY_RE` 定义与 `_iter_task_items`
- `aria/skills/audit-engine/references/execution-modes.md` 实跑 grep 核对 `sc13_baseline` 数字 (`adaptive_rules` 计数、`跳过校验, 继续执行 pre_merge 审计` 计数、`Step N:` 行分布)
- 实跑 `git -C aria diff --shortstat 301641b 1cb3872 -- <七个代码/规程文件>` 与 `git -C aria diff --stat 301641b 1cb3872 -- spec_complete.py multi_remote.py` 核对 `metadata.baseline_rebase`
- `git submodule status aria standards aria-orchestrator` 核对三个子模块当前 checkout 与 metadata 声明一致性
- `.aria/audit-reports/` 内多份历史审计报告 (grep 定位, 用于核 `main-project-version-consistency` 的语义边界, 未作为本轮 finding 依据, 仅作背景核验)

## Findings

| id | severity | type | category | scope | 摘要 | 证据 | 失败场景 | 建议修法 |
|---|---|---|---|---|---|---|---|---|
| `638d2a0f` | minor | issue | documentation | `detailed-tasks.yaml TASK-029` | TASK-029 把 `main-project-version-consistency` 与另外 4 个版本类 custom check 并列写进「复跑…为 OK」清单, 但该 check 验的是与本 spec 无关的另一条版本轴 (主项目版本, 现值 1.7.5), 不提供本 spec「16 个版本点」(aria-plugin 版本) 的任何机械覆盖, 并列写法易被读成它也覆盖 16 点 | `main-project-version-consistency.py:39-49` 的 `POINTS` 清单逐条为: `VERSION`(`## 版本号` 块 / `## 对应 Tag` 块, 两条均为主项目版本 1.7.5) / `CLAUDE.md`(`主项目 v(...)`) / 4×README(`Project Version:`) / 两处架构文档(`Aria main repo` 行) —— 9 点全部与 aria-plugin 版本 (`plugin.json`) 无关; `.aria/state-checks.yaml:333-334` 该 check 自身 description 逐字「既有两条 version check (m6-version-badge-match / i18n-readme-translation-currency) 也只比插件版本」, 未提及此 check 覆盖 aria-plugin 版本面; `VERSION:24` (本 spec 唯一真正改动的 VERSION 内版本行, 供子模块 `aria (插件)` 用) 不在该 9 点清单内 (清单只含 `VERSION` 的 `:6-10` 与 `:30-34` 两块, 两块都写主项目版本 1.7.5, 与本 spec 要改的 `:24` 是同文件不同行不同轴) | 执行者照 TASK-029 字面跑 5 个 check, `main-project-version-consistency` 必然 OK (因为它检的 9 点全都不受本 spec 触碰); 若执行者据此认为「16 个版本点已有机械兜底确认」, 会误判覆盖面 —— 但 TASK-029 verification 第 3 条本身已单独用 grep 直接核对 16 点取值一致, 故该误判不会造成漏检或错误提交, 只是文本表述层面的精度问题 | 在 TASK-029 该行末尾补一句「main-project-version-consistency 验的是主项目版本轴 (与 16 点的 aria-plugin 版本轴正交), 列入只作常规回归复核, 不作为 16 点覆盖证据」, 或直接从该行移出、只保留 `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `no-unresolved-version-placeholder` 四个与本 spec 相关的 check |

**其余五项视角逐一核验结论 (均未发现 major/critical, 证据见下)**:

1. **Rule #3 同步面**: proposal §4 (文档同步面表, `:356` 起) 与 §5 (向后兼容表, `:370` 起) 列出的每个文档触点均能在 yaml 找到对应 TASK 的 deliverables ——`execution-modes.md`→TASK-014、`audit-engine/SKILL.md`→TASK-015、`phase-c-integrator/SKILL.md`→TASK-016、`report-storage.md`/`pre-write-validation.md`/`phase-a-planner/SKILL.md`/`phase-b-developer/SKILL.md`→TASK-017、`aria/CHANGELOG.md`+版本引用点→TASK-025、`ab-suite/audit-engine.json`+`version.yaml`→TASK-023。反向核: TASK-014~017、023、025、029 改动的每个文件均能在 proposal §2/§3/§4/§5 或 CLAUDE.md §版本管理找到依据, 未发现无依据的改动。读前必看第 19 条扩出的 `phase-c-integrator/SKILL.md:57` 与 `:754` 经直读源码确认逐字为 `audit.checkpoints.pre_merge != "off"` (与 `:132` 步骤 3 同一字面键判断), `audit-engine/SKILL.md:423` 逐字为 `pre_merge checkpoint != off` (语义同构) —— 三处确属「同形」, 扩出正确, 且已在 TASK-015/016 落地并被 `metadata.v2_state_runs` 的 N8 三态实跑验证 (baseline N8=False, target N8=True, 三个坏态各自 N8=False)。
2. **发布同步面**: CLAUDE.md §版本管理列出的全部 6 类同步点 (aria 5 文件 / 主仓 gitlink / 主仓 VERSION / root README badge / i18n README / 两处架构文档 aria-plugin 行) 均被 TASK-025 (aria 5 文件) 与 TASK-029 (gitlink + 16 个版本点) 完整覆盖; 16 个版本点清单 (README.md 2 处 + 3×i18n README 各 3 处 + VERSION:24 + CLAUDE.md 2 处 + 两处架构文档 = 2+9+1+2+1+1=16) 与 CLAUDE.md 原文逐一对应。custom check 覆盖面: `plugin-version-arch-docs-match` 覆盖两处架构文档 aria-plugin 行、`m6-version-badge-match` 覆盖 README badge、`i18n-readme-translation-currency` 覆盖 i18n README 的 `translated-from` 标记 —— 三者与 CLAUDE.md §版本管理原文列出的机械兜底清单逐字一致。`main-project-version-consistency` 不在该清单内 (其 POINTS 是另一条版本轴, 见上表 finding), 列为独立 finding。
3. **两张映射表**: 「内联 Tasks 17 项 ↔ 新编号」全表 17 项逐项核对新编号指向的 TASK 均存在且内容匹配; 抽样 5 个内容最密的内联项 (`:409` B.0 语料冻结 / `:430` fixture 前提回扫 / `:432` 实现脚本 / `:439-446` AB 两读法并集 / `:451` Phase D) 逐子句对照, 全部子句在 TASK-002 / TASK-003 / TASK-008~012 / TASK-021+023+024+031 / TASK-031 中均有落点, 未发现遗漏子句, 亦未发现无依据新增。
4. **13 条裁定**: `metadata.rulings_applied` 13 条逐条与决策单 §2 `#199` 表 13 行比对, 内容、结论、回退条件均一致, 未发现转述走样。裁定 9 的落点仓从决策单原文「aria-plugin-benchmarks」改为「10CG/Aria」的偏离已在 tasks.md 读前必看第 10 条显式记录理由 (`forgejo GET` 得 404; `git ls-files` 确认该目录属主仓非独立仓, 非子模块), 偏离本身经核实成立、且已充分披露, 不计入 finding。
5. **读前必看 22 条**: 抽样并直读原文核对 >10 条 (含全部 23 项中的 1/2/3/4/5/6/7[9 处子引用]/9/11/12/13/14/15/16/17/18/19/20/22, 共逾 20 项), 全部行号与内容描述逐字命中, 无一处失实。
6. **写法规范**: `content-integrity.md` §4.4/§4.5 逐字核对, `tasks.md` 与 `detailed-tasks.yaml` 全文 `#[0-9]+` 扫描结果全部合规 (issue/PR 引用均带 `org/repo#n` 全限定前缀; 内部编号一律用 `第 N 项/条`、`TASK-0NN` 等普通写法; `Rule #N` 系例外白名单命中); 带圈/带框字符正则扫描两文件零命中; `tasks.md` 的 checkbox 行 (如 `- [ ] 3.2 ...`) 经 `spec_complete.py` 的 `_CHECKBOX_ANY_RE` 正则实测确可解析出 `parent_id="3.2"`, 与 `metadata.sc12_liveness`/`metadata.a2_state_runs` 依赖的 `_iter_task_items` 用法一致, 且已被 `a2_state_runs` 的三态实跑 (`integration_claims=['3.1','3.2','3.3']`) 独立证实工作正常。

## 对执笔人自报薄弱点的表态

- **(a) `stage_cells` 的 39 格「在 P6 之前以终局结束」按求值总序推出、实现前无法验证**: **可接受**。理由: 该分类若真的错配 (某格提前分给了实际依赖后续阶段的逻辑), 后果是该格在对应 TASK 的 `stage_cells` 命令下合法地报 `fail` (不是静默假绿, `metadata.v2_state_runs` 的 C1 block 已实跑证明 `cell_status.py` 能正确区分 pass/fail/not-run/执行两次四态), 执行者会得到清晰的诊断信号去调整颗粒度或改判分配, 有合法下一步; 且最终正确性的硬门槛是 TASK-012「SC 方法级全绿」, 不依赖这套阶段子格分类本身正确, 该分类只是提前观测的脚手架。抽样核对 39 格分布 (TASK-008:13/TASK-009:8/TASK-010:2/TASK-011:16) 与各任务所实现的 P 阶段 (P0/P1、P2a/P2、P3/P4、P5) 逐一对齐, 未发现明显错配。
- **(b) `coord_ref_precheck` / `commit_attribution` 偏严, 方向 fail-closed**: **可接受**。这与 CLAUDE.md 不可协商规则 #10 (已启用闸门不得 AI 自行放宽) 及 hard_constraints 里「新写 claim、release_gate 的 release/sweep/gc…仍逐项授权」的既定基调完全同向; 代价只是多几次停下请裁, 不产生错误的自动放行。
- **(c) 三态脚本第 99 行仍 `git fetch /home/dev/Aria`**: **可接受**。已直读 `metadata.v2_state_runs.script` 的 `n6_block()` 确认该行只存在于本次 A.2 自证用的一次性验证脚本内, 用于给临时裸仓灌入真实协调 ref 历史; **实际生产复用脚本 `metadata.coord_ref_precheck.code` 内的 `git("fetch","origin",...)` 用的是 `origin`, 不含任何硬编码本机路径** —— Phase B–D 各 TASK (TASK-001/024/031 等) 调用的都是后者, 不受该行影响。风险面完全封闭在「换机器想原样重放本次验证脚本」这一处, 不影响本计划的实际执行。
- **(d) `metadata.coord_ref_precheck.own_claim_files` 与 fixture 自造 claim 并列可能读成矛盾**: **可接受, 建议一句澄清**。逐一核对 TASK-001 (读真实 claim 文件)、TASK-024、TASK-031 对 `coord_ref_precheck` 的调用文字, 均明确指向「读本容器真实 active claim」, 未发现任何 TASK 文本要求执行者去仿照 `v2_state_runs` 的 `raw = "zz-precheck-own-" + uuid.uuid4().hex[:8]` 自造合成 id —— 没有找到会导致误执行的具体路径, 純属并列陈述在纸面上的可读性风险。建议在 `own_claim_files` 字段末尾加一句「本字段描述生产调用点 (TASK-001/024/031) 的用法; `metadata.v2_state_runs` 的 N6 验证脚本使用独立自造的合成 claim id, 不读本字段」以消除潜在误读。

## 风险 / 疑问

- `main-project-version-consistency` 的 9 点清单与本 spec 的 16 点清单在 `VERSION` 文件内共享同一文件但完全不同的行区间 (`:6-10`/`:30-34` 主项目版本 vs `:24` aria-plugin 版本), 已通过直读 `VERSION` 全文与探针源码确认两者正交、互不覆盖 —— 已按 finding `638d2a0f` 记录, 不再重复。
- `ab-plugin-benchmarks/ab-results/` 的最终目录名 (proposal 字面写 `<date>-pre-merge-completeness-gate-change-scope`, yaml TASK-024 的 `deliverables` 写 `<YYYY-MM-DD>-pre-merge-completeness-gate-rule6`) 两处字面不同, 但 tasks.md 自身已声明「5.9 勾选时换成本次结果目录全路径」, 即当前两处都只是占位, 非绑定值; yaml 的写法更贴合既有先例命名惯例 (`<date>-v<版本>-<slug>-rule6`, 已核 `ab-results/` 下 8 个历史目录逐一验证)。不计入 finding, 供执笔人 5.9 落笔时参考。
- 本轮未独立复核 tech-lead / backend-architect / qa-engineer / code-reviewer 四席视角 (按纪律不读其报告), 若其余席位从各自专精角度发现与我视角重叠的问题, 以聚合报告为准; 本报告仅代表知识管理/文档同步/写法规范/裁定转述四类视角的独立核验结果。

## Verdict

**PASS** (0C / 0M / 1m) — **Vote: PASS**

## 是否足以开始 Phase B

**足以**。从 Rule #3 文档同步面、CLAUDE.md 发布同步面、内联 Tasks↔新任务映射、13 条裁定转述、22 条读前必看引用、`content-integrity.md` 写法规范六个视角逐一核验, 均未发现会导致执行者「做错/做漏/卡住」的 critical 或 major 缺陷; 唯一记录的 minor finding (`638d2a0f`) 是纯文本精度问题, 不影响执行, 且不阻塞归档 (可在 Phase B 任一顺手时机补一句澄清, 或留待 Phase D)。
