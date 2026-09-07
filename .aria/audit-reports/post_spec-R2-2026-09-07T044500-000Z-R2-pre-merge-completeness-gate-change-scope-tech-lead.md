---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T04:55:47.665Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead]
---

# post_spec R2 单席报告 — tech-lead (架构与范围)

本席为 R2 新席位, **不继承 R1 结论**。全部载重断言经实读插件缓存 `1.71.1` 副本 (= aria `origin/master` `301641b`)、主仓工作树与 `git ls-tree` 冻结快照独立复核; 语料统计用自写脚本在**冻结快照 `3f4b379`** 与活体两侧各跑一遍。本轮**只审不改**, 未编辑仓库任何文件。

## 审计结论

### Decisions

- [minor] architecture/R1 缺陷落地核对: R1 的 **5 critical + 9 major 逐条落进正文而非批注**, 我按 rework 清单逐项定位改动位置并复核判据本体 —— 规则 2 末段界定 (`proposal.md:112`)、两个排除计数表 (`:119-122`)、(b) 换 Phase A-only (`:150`)、(c) 含内联 `## Tasks` (`:152`)、`--repo-path`/`--diff-repo-path` 拆分 (`:78-81`)、config-loader 路由 + 空集短路 (`:157-160`)、`mid_implementation` 排除 (`:145`)、对称有界包含 (`:114`)、四处旧 schema 清扫 (`:195`)。未见「改一处开另一处同型洞」的回归, 唯一例外是空集短路 (见 Issues 第 1 条)。
- [minor] testing/语料事实底盘独立复算: 对冻结快照 `3f4b379` 全枚举, proposal 的载重数字**逐个命中** —— 末段形态 62 份、仅末段有证据的 (checkpoint, change_id) 组合 25 个、`unattributed` 170、真 2-field legacy 6 (`post_spec-2026-04-12T0400Z.md` 等)、原稿合并口径 238、`C` = 152、(c) 非真空的「三样 A.2 产物全无」= 37。活体侧同一脚本得同样的 62/170/6/238 (总数已从 778 长到 802)。`sibling-spec-probe` 逐字子串在冻结快照命中 0 份 (§1.2b 自述属实)。
- [minor] architecture/消费方接缝零破坏: `state-scanner/scripts/collectors/audit.py:245` 是 `audit_dir.glob("*.md")`、`aria-dashboard/references/parse-rules.md:79` 是 `Glob ".aria/audit-reports/*.md"` —— **两个既有消费方都非递归**, §1.2b 选的「只扫顶层 / `iterdir()`」与它们同向而非新造分歧 (proposal 未援引这条佐证, 属漏写的正面证据)。本 spec 只读文件名不改 writer schema, §5「两者零影响」成立。`spec_complete.py:924-927` 的 liveness 分类确如 F7 所述只认 SKILL.md 内 fenced bash 真调用。
- [minor] architecture/无越界同伴在飞面: 触点集 (`audit-engine/**`、`phase-c-integrator/SKILL.md:133-136,157`、`phase-a-planner:267`、`phase-b-developer:204,277`、`ab-suite/audit-engine.json`) 与在飞 #195 的落点 (`state-scanner/collectors/handoff_multibranch.py`、`scan.py:186`、`state-snapshot-schema.md`) **零交叠**; `phase1_gate` / `claim_lifecycle` / `spec-drafter` 全未触。唯一共享面是 `ab-suite/version.yaml`, 但 #195 的 5.5 只落 `ab-results/` 与缺口 issue, 不改套件文件 ⇒ 无直接写冲突 (识别错误另见 Issues 第 2 条)。
- [minor] architecture/方案取舍成立: 根因 2 (「change_id 在 pre_merge 结构上无输入」) 经实读复核为真 —— `audit-engine/SKILL.md:49-54` 参数表确无 `change_id`, `phase-c-integrator/SKILL.md:136` 传的确是 `context: PR diff (branch_name vs base)` (R1 的 `ffd3834a` / `9a245f24` 冲突, 本席一条 `sed -n '136,137p'` 机械闭合: `:137` 是「5. 处理 verdict」, 勘正方向正确)。方案 B 用 §2/§3 接线补输入通道, 是治根因不是治症状; A/C/D 的否决理由经核成立。

### Issues

- [critical] architecture/§1.4 空集短路 / no_checkpoints_configured: 空集短路在受调用方守卫的路径上**只可能由合法配置触发**。判据链: `phase-c-integrator/SKILL.md:130-133` 步骤 2/3 保证脚本只在 `audit.enabled=true ∧ checkpoints.pre_merge != off` 时被调; Step 3 排除自身 + `post_closure` + `mid_post_spec` + (本 spec 新加) `mid_implementation` ⇒ `checked_checkpoints == []` **等价于**「audit 已启用、只开 pre_merge、其余全 off」。`config-loader/DEFAULTS.json` 的 8 个 checkpoint 缺省全 `off`, 所以「只开 pre_merge」正是最小采用形态; 旧配置 `agent_team_audit_points: ["pre_merge"]` 经兼容映射 (`config-loader/SKILL.md:323-329`, 未列出的保持 `off`) 落到同一格 —— 而这批采用方恰恰是 §1.4 引入 config-loader 路由要保护的那批。后果: `verdict=error` + exit 2 + 消费方 fail-closed「拒绝执行 pre_merge 审计」+ `on_fail: 阻塞合并` (`phase-c-integrator/SKILL.md:146`) ⇒ **合并被永久硬阻**, 且 §1.1 的豁免面只覆盖 S4/missing, `no_checkpoints_configured` 无出口; ERROR 文案「audit 未启用或全 off」对该采用方是**误诊** (audit 正启用)。改前行为是通过 (`execution-modes.md:64`「missing_checkpoints 为空 → 校验通过」) ⇒ 这是对既有消费方的硬回归。可证伪性同时失守: SC-15 的三个夹具 (`{}` / 无 `audit` 块 / 文件不存在) 经 config-loader 缺省都得 `enabled=false`, 被 `SKILL.md:131` 早退拦下, **生产路径上不可达** (§1.4 自己已承认「门本就不该被调用」); 第四格 legacy 夹具刻意用 `['post_spec','pre_merge']` 得非空 ⇒ **唯一可达的空集人群零 SC 覆盖**。按 Rule #10 白名单第四类, 「其余 checkpoint 一个都没配置」正是「闸门的结构性前提不成立」, 应走 not_applicable + 留痕, 不是整门 error。(证据: proposal.md:157-160,164; execution-modes.md:46-52,63-64; phase-c-integrator/SKILL.md:130-133,146; config-loader/DEFAULTS.json audit.checkpoints; config-loader/SKILL.md:323-329; proposal.md:283 SC-15)
- [major] architecture/§4 ab-suite/version.yaml 行 + 并发轨识别: 该行两个事实同时失效。(1) 「(**套件**版本, 现值实测 **1.4.0**) … 1.4.0 → **1.5.0**」为假 —— 主仓 master 上 `aria-plugin-benchmarks/ab-suite/version.yaml:1` 已是 `"1.5.0"`, 由 commit `5697477` 引入, 其 changelog 1.5.0 条目逐字点名 `a1-entry-claim-duplicate-work-guard`; 冻结快照 `3f4b379` 上确为 1.4.0, 即 R1 的实测在 `ecb6296` 合入 origin/master 后就已过期, 而 proposal 在 2026-09-07 00:49 的 v3 编辑中未重取。照 §4 字面执行会去改一条**已发布**的 changelog 条目。(2) 被点名的「在飞同伴轨」`a1-entry-claim-duplicate-work-guard` 已归档于 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard`, PR #202 merge `9f25a66` —— **本 proposal 自己的头部 gitlink 行就写着 #202 已 merged**, 同文档内自相矛盾。(3) 真正在飞、与本 spec 同抢 **v1.71.2** 的 `handoff-multibranch-subdir-path-fidelity` (#195, 其 proposal `:320` 明写候选 v1.71.2, 同时段在跑 R3 审计) 在本文**零提及** (`grep -c 'handoff-multibranch\|#195'` = 0)。缓解条款 (顺延 / `ls-remote --tags` / 读同伴 handoff) 本身正确, 但把实施者指向了错的轨。按 audit-points.md §横切检查原则「数据可用性」, 依赖历史/环境数据的断言经机械核实不符即对 verdict 载重。(证据: ab-suite/version.yaml:1-13; git log 5697477; openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard; proposal.md:10,196,317; handoff-multibranch-subdir-path-fidelity/proposal.md:320)
- [major] testing/SC-14(a) 与 rule6_note 的照跑面: 头部 Rule #6 行与 rule6_note、SC-14(a)、Tasks AB 项四处都把 `ab-suite/phase-c-integrator-pre-merge-gate.json` 列为「照跑」对象并要求「各跑一次 with/without 臂」。实读该文件: 顶层键 = `skill_name / version / type / parent_skill / spec / issue / release_pr / fixtures_dir / changelog / fixtures / primary_pass_gate_metric / quality_target_deferred_to_dogfood`, **无 `evals` 键**, `type: "workflow_skill_subextension"`, 内容是 8 条确定性 fixtures 且每条挂 `test_case_in_unit_tests` (如 `test_pre_merge_gate.GateCheckTests.test_case_a_green`) —— 它是绑定单测的契约夹具集, 不是 LLM AB eval 套件, 「with/without 臂」在其上无结构对应物。其 `spec` 指向 `phase-c-integrator-pre-merge-gate` / `issue: 10CG/Aria#60` (C.2.4 CI 门), 而本 spec 改的是 audit-engine pre_hook (`phase-c-integrator/SKILL.md:133-136`) 与 output schema (`:157`) —— 「本 spec 改其处方面」这条把它拉进照跑面的理由**未成立**。后果: Phase B 要么按 Rule #10 禁止的方式自行降级删掉这条, 要么用未定义的方式「跑」它然后自证通过 —— 两条都让 SC-14(a) 不可证伪。需在 spec 内定义该套件的「跑」是什么 (跑 8 条 fixture 对应的单测? 还是排除并说明理由), 不能留给实施者临场裁量。(证据: ab-suite/phase-c-integrator-pre-merge-gate.json 顶层键与 fixtures[0]; proposal.md:12,239,278,297)
- [minor] documentation/§4「主仓 14 版本字符串点」: 机械枚举 (排除子模块 / openspec / handoff / audit-reports / ab-results) 为 **16 处** —— 14 处 README×4 + VERSION:24 + CLAUDE.md:139,141 之外, 还有 `docs/architecture/system-architecture.md:189` 与 `docs/architecture/version-scheme.md:23`, 而 CLAUDE.md §版本管理「发布同步面」把这两处逐字列为发版面 (PR #190 审计补入)。并发轨 #195 对同一面独立枚举也是 16 并与上次发版 commit `4c3c826` 自述逐一对上。风险有限: 这两处正好有 `plugin-version-arch-docs-match` 机械兜底 (`.aria/state-checks.yaml:372`), 漏改会在归档门转红; 但 §4 是 Phase B 的照单, 数字应订正为 16。(证据: proposal.md:196; docs/architecture/system-architecture.md:189; docs/architecture/version-scheme.md:23; handoff-multibranch-subdir-path-fidelity/proposal.md:238-251)
- [minor] implementation/§1.1 S2 的 diff 取 id 与 rename 检测: S2 规定「从 `git diff --name-only $(git merge-base HEAD <base>)` 取路径前缀 `openspec/changes/<id>/`」, 未加 `--no-renames`, 而同一 skill 的姊妹门 `path_coverage` 刻意写成 `git diff --name-only --no-renames` (`phase-c-integrator/SKILL.md:252`) —— 同族两处取法不一致且本 spec 未说明为何不跟。具体后果: 纯归档移动的 PR (`openspec/changes/<id>/` → `openspec/archive/YYYY-MM-DD-<id>/`) 在 rename 检测开启时只输出目的侧路径, S2 取不到 `openspec/changes/<id>/` 前缀 ⇒ 落 S4 `change_scope_unresolved` exit 2。方向是 fail-closed (不造假绿), 但属未成文的假红路径, 建议 §1.1 显式选定 rename 语义并在 SC-7 加一格。(证据: proposal.md:91; audit-engine/SKILL.md:406; phase-c-integrator/SKILL.md:252)
- [minor] documentation/§1.4 两个计数的作用域与 audit trail 模板不咬合: §1.4 明写 `excluded_legacy_count` / `unattributed_count` / `unattributed` 是「**全局单值**, 统计面 = 以任一纳入校验 checkpoint 名开头的文件的并集」, 但同节的 trail 模板是 per-checkpoint 的 `[WARN] unattributed reports ({cp}): <文件名逐个>`, missing 模板又把全局 `N` / `M` 嵌进逐 (checkpoint, change_id) 的文案里。多 checkpoint 时 `{cp}` 该取哪个未定义, 逐对文案里重复同一个全局数也会误导读者以为是该对的计数。SC-4 断言的 `unattributed == ['post_planning-R2-CONVERGED-trunc-id.md']` 是全局列表形态, 与模板的 per-cp 形态对不上。(证据: proposal.md:167-170,175-179; SC-4 @ proposal.md:265)
- [minor] documentation/头部 gitlink 现况行的本地 checkout 陈述: 「本地 checkout 仍停在 `0545f86` 且本地 master 与 origin/master 已分叉」已不成立 —— `git ls-tree master aria` = `301641b`, `git submodule status aria` = ` 301641b… (v1.71.1)` (无 `+`/`-` 前缀), `git status --porcelain` 空; 分叉在 `ecb6296` (2026-09-06 17:11) 已合掉。「Phase B/C 开工前先 fetch + 对齐」的指令本身无害且仍应保留, 但把已完成的状态写成待办, 与同段「远端已是 `301641b`」并列会让读者以为还存在 gitlink 回退风险。(证据: proposal.md:10; git ls-tree master aria; git submodule status aria)

### Risks

- 本席未新增 risk 条目。proposal 现有 R-a~R-e 五条经核与实况相符 (R-a 的 170 份 `unattributed` 我在冻结快照上复算命中), 覆盖面无缺口。

## Verdict

**FAIL** — Critical 1 / Major 2 / Minor 4 (0 risk)。

rationale: 这份 v3 相比 R1 是**实质性重写而非批注**, 事实底盘经我在冻结快照上独立复算逐个命中, 消费方接缝与并发落点都干净, 方案 B 治的是真根因。但 R1 rework 为修 `9f37ec28` 而新加的**空集短路**引入了一条与被修 bug 方向相反、量级同级的新失效: 它在受调用方守卫的路径上唯一可达的人群就是「只开 pre_merge」的合法采用方 (含 config-loader 兼容映射后的 legacy 采用方 —— 恰是同一条 rework 声称要保护的那批), 对他们从「通过」变成**无豁免的永久硬阻**, 而 SC-15 的三个夹具全部落在调用方早退拦下的不可达态上, 第四格又刻意选了非空配置 ⇒ 唯一可达的格零覆盖。这是「SC 在不可达态上恒绿、可达态无断言」的经典形态, 按 critical (会破坏消费方) 计。

两条 major 各自独立: 一条是 §4 版本/并发面的实测已过期且点错了在飞轨 (真正同抢 v1.71.2 的 #195 全文零提及), 按横切检查原则「数据可用性」对 verdict 载重; 一条是 Rule #6 照跑面里塞进了一个结构上不是 AB eval 套件的 fixture 集, 使 SC-14(a) 对该项不可执行 —— 在 Rule #10 下实施者既不能自行删也无从执行。

四条 minor 均为随稿可订正项 (版本点 14→16、rename 语义、计数作用域文案、本地 checkout 陈述), 不改变方案方向。

按 report-storage.md §Verdict 计算, ≥1 Critical ⇒ FAIL; post_spec 为 `blocking: false`, 本判定不硬阻断流程, 但按 Rule #10 不得由 AI 自行降格。

计算依据:
- Critical: 1
- Major: 2
- Minor: 4
- Decisions (不计入缺陷计数): 5

## 轮次记录

### Round 2

- Agents: tech-lead (本席; 五席之一, 其余席位结论本报告不代表)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 (Issues 7 / Risks 0 / Decisions 5)
- Delta vs 上轮: R1 的 5 critical + 9 major **无一被本席重开** —— 逐条核到正文落地且判据本体正确; 本席 3 条缺陷类 (1C+2M) 全部落在 R1 rework 的**新增增量** (空集短路 / §4 版本与并发面重写 / SC-14 照跑面拆分) 或 R1 未机械核到的事实 (版本点计数、rename 语义)。R1 的 `ffd3834a` vs `9a245f24` 行号冲突已由本席一条 `sed -n '136,137p'` 机械闭合, 勘正方向正确。
- Vote: REVISE
