---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T10:31:30.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席 — 10CG/Aria#199 A.2/A.3 v1.1 (source_sha `97c3515`)

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (207 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1056 行), 另用 `yaml.safe_load` 机读 DAG、agent 计数与工时
- `proposal.md`: `:1-22` 头部; `:100-324` (§1 `--base` 条款、§1.0–§1.4 全文); `:325-399` (§2–§5、Impact 前半); `:407-451` Tasks 全文; SC 表 `:457-478` 中 SC-2/4/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22 全文; `:480-486` rule6_note; 另用脚本全文检索 `no_spec_unverifiable` / `post_brainstorm` / 「降为」等字样
- 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (116 行)
- `CLAUDE.md` 多远程两条硬约束、Rule #3/#6/#8/#10 (会话已注入)
- aria (`1cb3872`) 源码: `skills/phase-c-integrator/SKILL.md` `:40-58`、`:128-157`、`:252-253`、`:600-640`、`:752-756`; `skills/git-remote-helper/scripts/push_all_remotes.sh` `:1-140`; `skills/git-remote-helper/SKILL.md` (verify_parity_post_push 条目); `skills/state-scanner/scripts/lib/spec_complete.py` `:256-290`、`:681-692`、`:880-1100`; `skills/state-scanner/scripts/phase1_gate.py` `:1125-1200`、`:1425-1510`; `skills/state-scanner/lib/failure_handlers.py:282-350`; `release_gate.py` CLI 段; `skills/state-scanner/SKILL.md` 中 fetch/heartbeat 段; `skills/phase-b-developer/SKILL.md:204,210-216,277`; `skills/phase-a-planner/SKILL.md:267`; `skills/audit-engine/references/execution-modes.md:1-100`; `skills/run_all_tests.sh:36-50`; `skills/phase-d-closer/SKILL.md` 步骤表与 `:224-245`; `skills/openspec-archive/SKILL.md` Step 7 段; `skills/ai-native-estimator/SKILL.md` 存储段; `skills/config-loader/DEFAULTS.json` (multi_remote / phase_c_integrator / audit)
- 主仓: `.aria/config.json`、`.gitmodules`、`.aria/state-checks.yaml:295-330` 与各 check 名、`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:150-260`、`ab-suite/phase-c-integrator.json` 与 `ab-suite/audit-engine.json` 全部 eval 题面、`ab-suite/version.yaml` 头部、`ab-results/2026-08-16-v1.66.0-137-rule6/` (RESULT / PREDICTION / eval-3)、`ab-results/2026-04-12-v1.15.0/eval-int-3-.../with_skill/outputs/result.md` 头部、`standards/conventions/content-integrity.md:161-212`、10CG/Aria#195 的 `detailed-tasks.yaml:177,205,922` 与 `tasks.md` 相关行、10CG/Aria#211 proposal 头部与 `:135/:146`
- 实跑 (均在 `scratchpad/audit-R1-tech-lead/` 或只读命令): 执笔人 `a2_state_runs` 脚本在本席独立副本上复跑, 输出与 yaml 嵌入**逐字节一致** (`diff` 空); 全勾选副本上 `spec_complete.py --gate` 得 `complete: true` / `verdict: warn`; catalog 三条命令 OK、字面坏 node id `FAILED (errors=1)`; 重写 b 的语料计数在 `a563192` 复算为 154/54/17/37、在 `97c3515` 为 154/53/16/37; SC-13 基线计数复算与 `metadata.sc13_baseline` 一致; 16 个版本点与 6 个 custom check 名逐一 grep 命中; 三个子模块 HEAD / master / origin / github 四方相等 (aria-orchestrator 为 detached 的 `237045a`); `git ls-remote origin refs/aria/coordination` = 本地 `be2ba7e`; 在 scratch 裸仓实测 `ls-remote <r> refs/heads/master 'refs/tags/vX*'` 会同时列出附注 tag 与 `^{}` 行

## Findings

### Critical

无。

### Major

**M1** · id `78655dd9` · major · issue · testing · scope `detailed-tasks.yaml TASK-008~TASK-011`

- **summary**: 组 2 各任务的「转绿」清单与测试方法粒度、§1.0 求值总序不相容 —— 多数被点名的 SC 方法含依赖后序 P 阶段 (尤其 P6) 的断言, 在该任务完成时结构上仍红。
- **证据**:
  - yaml `:587` TASK-008「转绿: SC-10 / SC-21 / SC-15(1)(4)」。proposal `:466` SC-10 要求「四种 verdict 下 stdout 均可 `json.loads`」—— `fail` 只能来自 P6 的 missing; proposal `:471` SC-15(4) 断言 `checked_checkpoints == ['post_spec']` (P4, TASK-010) 与「落格 B 判 pass」(P5, TASK-011), 两格同在一个方法 `test_legacy_config_mapping_inlined`。
  - yaml `:605` TASK-009「SC-7 (除 (c)(d)) / SC-17 (除 (5))」。proposal `:463` SC-7 的主方法含「`b` 缺一项即 fail」(P6)、「`--no-spec` 合法 → 全部 `not_applicable`」(P4+P6)、(e) 格 D (P3–P5); `:473` SC-17(1)「报告在 tmpA 找」(P6)。
  - yaml `:625` TASK-010「SC-7(c)(d) / SC-16 / SC-20」。proposal `:472` SC-16 期望 `verdict=pass` (须 P6 判 post_spec present); `:476` SC-20(7)「`results` 恰 1 条 (`{post_spec, b, present}`)」(P6); SC-7(c)「按零报告评估 (⇒ `missing` …)」(P6)。
  - yaml `:640` 把「missing → bypassed」放进 P5 任务 TASK-011, `:643` 又要求它转绿 SC-9 (proposal `:465` (1)「一项 missing → bypassed」) 与 SC-15(5) (三对 missing ⇒ fail) —— missing 在 P6 (TASK-012) 才产出。
  - yaml `:662` TASK-012 才写「至此 … 全绿」。
- **失败场景**: 执行者按 TASK-008~011 的 verification 验收 → 所列方法必红 → 要么越界提前实现 P6 (破坏按 §1.0 切的任务边界), 要么把「转绿」当可忽略项 (中间验收失去意义), 要么停住。
- **它怎么会红**: 基线 (无脚本) 全红; 目标实现在 TASK-008 完成、P2–P6 未写时所列方法仍红; 坏实现同样红 ⇒ 该时点这条检查对好坏实现零区分, 恒红。
- **建议修法**: 中间任务的验收改为「本段可独立断言的子格 (`subTest` 或直接调用该阶段函数) 为绿, 其余红属预期」并逐格点名; 或把 SC 级转绿统一挪到 TASK-012; missing 的豁免降级挪到 TASK-012 (它是 P6 之后的路由, 属 §1.4)。

**M2** · id `fba6ae11` · major · issue · architecture · scope `detailed-tasks.yaml TASK-013 / TASK-014~TASK-017`

- **summary**: DAG 允许组 3 与 2.2–2.6 并行, 与 TASK-013「不带路径的 porcelain 为空」断言冲突; tasks.md 组号 1→5 的顺序与 DAG 也不一致。
- **证据**: yaml `:686` / `:707` / `:725` / `:742` 四个任务的 dependencies 只有 `TASK-008`; 本席机读 DAG 分层, 第 8 层 = TASK-009 与 TASK-014/015/016/017 并列, TASK-013 在第 12 层。yaml `:678`「只 add scripts/completeness_gate.py 与 tests/test_completeness_gate.py 并提交; 提交后不带路径的 `git -C aria status --porcelain` 为空」。组 3 的七个文件与组 2 同在 aria 工作树, 到 TASK-018 才提交。
- **失败场景**: 按 DAG (yaml 是依赖 SOT) 把组 3 并行派给 knowledge-manager → 到 TASK-013 时 aria 工作树有组 3 未提交改动 → 只 add 两个文件后 porcelain 非空 → TASK-013 验收红, 且无合法下一步 (计划禁 stash, 组 3 又不属本任务提交面)。
- **建议修法**: TASK-014~017 加依赖 `TASK-013` (串行); 或把 TASK-013 的断言改为带路径 `git -C aria status --porcelain -- <这两个文件>` 为空, 并在 tasks.md 写明组 2 / 组 3 可并行。

**M3** · id `b6496cbf` · major · issue · testing · scope `detailed-tasks.yaml TASK-024 / metadata.owner_gates 5`

- **summary**: `delta.pass_rate` 的处置在 TASK-024 与 owner_gates 第 5 项之间口径不一; 聚合范围未定义; 若按套件算, phase-c-integrator 套件在健康态下就会触发, 是恒红。
- **证据**: yaml `:897` 的阻断条件只列「判回归或 eval 3 未转差」; `:898` 对「delta.pass_rate > 0」只要求 RESULT.md「如实登记是否达成」; yaml `:119` 与 tasks.md `:88` 却把「delta.pass_rate ≤ 0」列为阻断 TASK-025 的 owner 裁定; yaml `:106` 要求各任务条目与 owner_gates 一致。`phase-c-integrator.json` 三条 eval 实读为 C.1 提交 / C.2 冲突 / C.2.5 多远程, 均不触本 spec 改的步骤 3、4、4.5; 先例 `ab-results/2026-08-16-v1.66.0-137-rule6/RESULT.md` 中不相关 eval「无 delta」。proposal `:470` SC-14(a) 对照跑套件只要求「无回归」。
- **它怎么会红**: 按套件算, phase-c-integrator 健康态期望 delta≈0 ⇒「≤ 0」恒触发, 坏实现 (真回归) 同样触发 ⇒ 零区分力; 两套件合并算则被 eval 3 拉正, 反而可能盖住 phase-c-integrator 套件的真实回归。两个执行者按两种聚合口径会得出相反的「要不要停」。
- **建议修法**: 写死: 照跑套件只判「逐 eval 无回归」; `delta > 0` 只对 audit-engine 套件 (含定向 eval 3) 要求; 同步改 owner_gates 5 与 tasks.md 表第 5 行; PREDICTION.md 逐套件预测。

**M4** · id `70a663d6` · major · issue · documentation · scope `detailed-tasks.yaml TASK-025 / tasks.md 读前必看第 7 条`

- **summary**: 裁定 11 的连带清单漏了 proposal §5 第 2 条, TASK-025 会把与裁定 11 矛盾的迁移文案写进 CHANGELOG。
- **证据**: proposal `:378` §5 第 2 条原文「只把 missing / S4 / `spec_level_undetermined` 降为 `bypassed` …; S3 的输入矛盾错与 S1 的 `change_id_unanchored` **不被豁免**」(排他列举, 无 `no_spec_unverifiable`)。tasks.md `:23` 第 7 条列的连带位置是「§1.1 末段、§1.0 短路、`:340` Step 2 改写句、§5 第 10 条、§1.1b 第 4 行、SC-17(5)」, 没有 §5 第 2 条。yaml `:920`「迁移文案十三条 = proposal §5 第 1–12 条 (第 10 条按裁定 11 改写 …)」。决策单 §2 #199 第 11 行:「`allow_incomplete_checkpoints` 覆盖 `no_spec_unverifiable`」。
- **失败场景**: 执行者照 §5 第 2 条原文写 CHANGELOG → 采用方读到排他的豁免列表, 与同一节改写后的第 10 条自相矛盾; SC-13 与 N1/N2 都不查 CHANGELOG, 没有检查会拦住。
- **建议修法**: 第 7 条补上「§5 第 2 条」(以及 §4 表 execution-modes 行里 `:43` 改写的摘要句), TASK-025 写明第 2 条的豁免列表要补 `no_spec_unverifiable`; 按「修一类而非一处」对 proposal 全文检索「降为」「不被豁免」, 把完整清单列出来。

**M5** · id `e5afda8d` · major · risk · testing · scope `detailed-tasks.yaml TASK-024 副作用防护`

- **summary**: TASK-024 在真仓无沙箱跑题面为「执行」口吻的 phase-c-integrator.json, 只有事后快照没有事前防护; `ARIA_COORDINATION_NO_PUSH` 挡不住 `git push`; 快照面不全。
- **证据**: `ab-suite/phase-c-integrator.json` 实读: eval 1「Execute Phase C C.1: Generate conventional commits from staged changes」; eval 3「请执行 Multi-Remote Push Enforcement: 主动推送所有 enforced remote 并做 post-push SHA 验证」; 两条都未声明产出形态。`AB_TEST_OPERATIONS.md:224-226`: 该变量只让 phase1_gate / release_gate 跳过推送。yaml `:893` 快照面 = 主仓与 aria 的 HEAD / porcelain / 分支列表 /「两个远端 master」/ 协调 ref, 不含 standards 与 aria-orchestrator 的远端、tag、Forgejo PR 状态。tasks.md `:68` 判断 15 已承认「eval 在真仓无沙箱运行」。主仓本地 master 现领先 origin 1 个提交 (`97c3515`); owner_gates 2 未授权时 B.1 后仍会如此。
- **失败场景**: with_skill 臂按题面实跑 C.2.5 → `push_all_remotes.sh` 把本地 master (含未授权的规划提交) 与子模块 master 推到 origin 与 github; 事后快照发现也撤不回。eval 1 可能在 feature 分支上对暂存区 `git commit`。
- **缓和与定级理由**: 两次先例 (2026-04-12、2026-08-16) 的产出都是描述性的 (前者自述「不执行实际 push」), 属概率性风险, 故定 major 不定 critical。
- **建议修法**: TASK-024 明写: 两套件一律按 descriptive 形态下发 (手册 `:170` 规则 1「未声明视为 descriptive」), 执行器提示逐字加「不得执行任何 git 写命令、不得调用 forgejo 写接口」; 或在 remote URL 改为本地裸仓的一次性 clone 里跑; 快照面补三个子模块两端的 `ls-remote`、`ls-remote --tags` 与 PR 列表。

**M6** · id `357aaef4` · major · risk · architecture · scope `detailed-tasks.yaml TASK-001 / TASK-024 / metadata.owner_gates 14`

- **summary**: 协调 ref 上两处「整条 ref」操作 (B.1 免授权心跳推送、AB 后强制对齐) 只考虑了本轨自己的本地写入, 没处理他轨尚未获授权的本地写入 —— 第 14 项的推理只用在了自己身上。
- **证据**: `phase1_gate.py:1183` 心跳写入后调 `resilient_push`; `aria/skills/state-scanner/lib/failure_handlers.py:289` 注释「Push refs/aria/coordination」—— 推的是整条 ref。yaml `:128` owner_gates 14 正是据此推出「新 claim 未授权期间心跳也加 `--no-push`」, 但只覆盖本轨重新认领。yaml `:445` TASK-001 只写「不等则经 state-scanner (非强制 fetch) 对齐」: 本地领先远端时非强制 fetch 对不齐, 计划没有给这一分支。同伴轨 10CG/Aria#195 的计划 (`handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml:205`) 在未授权时用 `--no-push` 写本地 claim, `:177` release 推送未授权则停在该步; 本计划 owner_gates 1 只要求 #195 完成 C.2, 不要求其 Phase D 推送完成。yaml `:899` TASK-024 按手册 `:228` 执行 `git fetch origin +refs/aria/coordination:refs/aria/coordination`, 强制覆盖本地 ref。
- **失败场景**: #195 已完成 C.2, 但它的 `--no-push` claim 或待授权的 release 还留在本地 → #199 TASK-001 的免授权心跳把整条 ref 推上远端, 等于替 #195 发布了 owner 未授权的协调写入 (owner 09-17: 新写 claim、release 仍逐项授权)。反方向: TASK-024 结束时的强制对齐把 #195 仍待授权的本地写入整个抹掉 (与 memory「fetch-then-write」同形)。
- **建议修法**: TASK-001 以及每次心跳前加一步: 比较本地与 `ls-remote` 的协调 ref SHA, 本地领先时列出领先提交涉及的 claim 文件; 其中有非本轨写入 ⇒ 心跳加 `--no-push` 并停下请授权。TASK-024 强制对齐前同样列出本地领先内容, 有他轨写入 ⇒ 停下上报, 不直接覆盖。

**M7** · id `db4e9988` · major · issue · implementation · scope `detailed-tasks.yaml TASK-001 / TASK-030`

- **summary**: 主仓 PR 没有提交范围核验, 而主仓分支起点可能回落为本地 master。
- **证据**: yaml `:448` TASK-001「否则从含 P 的本地 master 起」, 不核 `origin/master..P` 之间每个提交的归属; yaml `:1023` TASK-030 只核 `git status --porcelain` (工作树), 不核 `git log origin/master..HEAD`; tasks.md `:154` 写了「提交面有范围核验」, 但 yaml (SOT) 没有可执行的判据。本仓惯例在本地 master 上提交会话收尾与审计报告 (如 `7926e6f`、`8a9fe35`)。
- **失败场景**: B.1 时本地 master 上有他轨或其他会话未推的提交 → feature 分支继承 → TASK-030 推分支并经 PR 合入共享 master; owner_gates 9 的授权是在看不到提交清单的情况下给的 (memory「sync≠push-auth」)。
- **建议修法**: TASK-001 回落时记录 `git log --oneline origin/master..<起点>` 并逐条标归属, 有非本轨提交 ⇒ 停下请 owner 裁; TASK-030 开 PR 前再跑一次同一命令, 清单原样记台账, 并随授权请求一起给 owner。

**M8** · id `76955ceb` · major · issue · testing · scope `detailed-tasks.yaml TASK-024 / TASK-027`

- **summary**: AB 实测的树与最终合并树之间没有一致性约束, 取号复核的恢复路径也不重跑 AB。
- **证据**: yaml `:895` with_skill = feature 分支工作树 (起点 = B.1 时的 aria `origin/master`); yaml `:918` TASK-025 只记录取号时的 `origin/master` SHA, 不要求 feature 已包含它; yaml `:956` 第 4 步只比较「TASK-025 之后」是否前进, 恢复动作「merge origin/master、重新取号、重跑 TASK-021 与 TASK-026」不含 TASK-024; yaml `:959` 第 7 步合并树回归只含 TASK-021 / TASK-018 / L2。Phase B 预估 97–143h, 期间 aria 有他轨发版的现实可能 (`bfe8285d` 另开了 10CG/aria-plugin#196–#198, v1.73.3 即其中之一)。
- **失败场景**: (a) B.1 到 TASK-025 之间 aria 发了版 → 第 5 步合并必然在版本 5 文件上冲突 → 停, 而恢复指针只挂在第 4 步, 这种情况没有成文恢复路径; (b) 上游改了 audit-engine 或 phase-c-integrator 的 SKILL.md, 但没有版本冲突 → 合并静默成功, 最终发布的处方文本组合从未过 Rule #6 AB。
- **建议修法**: TASK-024 开跑前断言 `git -C aria merge-base --is-ancestor origin/master <feature>`, 不成立就先 merge origin/master 并重跑 TASK-021; TASK-027 第 4 步改为与 AB 开跑时的 SHA 比较, 恢复时若 `git diff <AB 时 SHA>..origin/master -- skills/audit-engine skills/phase-c-integrator` 非空则重跑 TASK-024; without 臂的「起点 SHA」随之改为合入后的 `origin/master`。

### Minor

**m1** · id `c7460344` · minor · issue · documentation · scope `detailed-tasks.yaml TASK-014 / TASK-015` —— yaml `:695` 与 `:714` 互相要求调用串「与对方逐字相同」, 但两处都没给 canonical 串; 两任务在 DAG 上并行, 可能由不同实例执笔, 不一致要到 TASK-018 才发现, 造成返工。修法: 在 metadata 钉一份 canonical 调用串 (`a2_state_runs` 里的 `CALL` 即可), 两任务照抄。

**m2** · id `f0e0d6b8` · minor · issue · documentation · scope `detailed-tasks.yaml metadata.c25_five_questions` —— yaml `:428` 写「fail_on_partial_push 缺省与本仓 config 均为 true」「read_only_remotes 为空 (… `.aria/config.json` 的 multi_remote 段)」。实读 `.aria/config.json` 顶层键为 `[_comment, version, workflow, state_scanner, tdd, benchmarks, experiments, audit, orchestrator, phase_c_integrator]`, 既无 `multi_remote` 段, `phase_c_integrator` 下也无 `multi_remote_push`; 有效值全部来自 DEFAULTS.json (`read_only_remotes: []`、`fail_on_partial_push: true`)。结论不变, 引用不准。修法: 改为「本仓未覆盖, 取 DEFAULTS」。其余四问我逐条核过: `SKILL.md:603/613/614/625-630/638` 与 `push_all_remotes.sh:101-127` 均与表述相符; 主仓 parity 核验确实走 `ls-remote` (`git-remote-helper/SKILL.md:40`), 子模块只比本地 remote-tracking ref。

**m3** · id `fd08b259` · minor · issue · implementation · scope `tasks.md 读前必看第 8 条` —— tasks.md `:24` 的括注「在 P6 之前终止的运行 (error / bypassed / 格 B–E)」把 bypassed 整体列入; 但 missing 被豁免的那一类 bypassed 要走完 P6 (§1.1「仍逐对评估三态并全部留痕」), 不应 `results=[]`; SC-9(1) 不锁 `results`, 误读不会被测试拦下。修法: 括注改为「S4 / spec_level_undetermined / no_spec_unverifiable 被豁免的 bypassed」。

**m4** · id `9dc5dd0a` · minor · issue · implementation · scope `detailed-tasks.yaml TASK-031` —— TASK-031 手写 Phase D, 没说明与 phase-d-closer 的关系: 漏了 D.4 estimator capture (`phase-d-closer/SKILL.md:44`、`:224-236`; 本仓未设 `ai_native_estimator.enabled=false`, 默认会采集, 写本地 `.aria/estimator/`); D.1 以「无 UPM」跳过也没留痕。若执行者改走 phase-d-closer, 其 D.2b 默认命令带 `--sweep-stale --gc` (`phase-d-closer/SKILL.md:51-52`), 与 owner 09-17 裁定 (sweep / gc 逐项授权) 冲突。修法: 写明「不调 phase-d-closer, 逐步对应: D.1 跳过 / D.2 / D.2b 去掉 sweep 与 gc / D.3 / D.4 照跑」。

**m5** · id `ea958583` · minor · issue · documentation · scope `tasks.md AI 流程判断清单` —— 清单漏了计划实际做出的五项判断:
1. TASK-024 的「delta ≤ 0 请裁」、「复跑两次、三取二」回归判据, 以及用 old_skill 充当 without 臂。
2. TASK-003 给没有 checkpoint 配置的格钉 `checkpoints: {post_spec: convergence}`。SC-22(1) 按 §1.0 硬约束 (1)(3) 取 manual 后纳入集为空, 会落格 C, 与其期望的「other 那对 missing」冲突。这是对 proposal 的补定, 也应进读前必看表。
3. TASK-029 把已启用的 custom check `plugin-cache-currency` 出现 STALE 预先当作预期。
4. TASK-031 手写 Phase D, 且 release_gate 不带 sweep / gc。
5. TASK-027 第 4 步给了恢复指针, 与判断 19「不写自动恢复流程」的表述不一致。

修法: 这五项补进清单, 并在周期 handoff 照录。

**m6** · id `2bc10001` · minor · risk · testing · scope `detailed-tasks.yaml TASK-019 / TASK-020` —— yaml `:789` 反事实补丁由 qa-engineer 构造, 而测试文件也由 qa-engineer 执笔 (TASK-004~006)。计划只保证「非实现者」, 没保证「非测试作者」(memory「adversarial-fixture」: 坏态须由非作者独立构造)。补丁内容多数已被 proposal SC 原文钉死, 故定 minor。修法: 写明 TASK-019/020 用与 TASK-004~006 不同的新实例。

**m7** · id `a9ac36a7` · minor · issue · documentation · scope `detailed-tasks.yaml metadata.rule6_note` —— rule6_note (yaml `:129`) 的点名行为只有 proposal 的 A/B/C, 没交代计划新增的 `phase-c-integrator/SKILL.md:57` 与 `:754` 两处处方性改写 (tasks.md `:35` 第 19 条) 归到判据表哪一行。实际靠 phase-c-integrator.json 照跑兜底, 而该套件不覆盖 hotfix lane。修法: rule6_note 补一句这两处改动的归类与兜底方式。

**m8** · id `c2513059` · minor · issue · documentation · scope `detailed-tasks.yaml TASK-023` —— yaml `:875`「已被占 (含 10CG/Aria#211 的 T4) ⇒ 顺延」只有读 `origin/master` 这一种判法, 看不见尚未合并的 #211; 真正兜底的是合并冲突与合并后复读。修法: 写明「在飞轨不可见, 以合并冲突或合并后复读为准」, 免得执行者去猜 #211 会取哪个号。

## 对执笔人自报薄弱点的表态

- **(a) 读前必看第 7、8 条的取值由执笔人钉定 —— 可接受。** 第 7 条的降级取值与 §1.1 末段「S4-bypassed 的字段取值」同构, 另加 `[WARN] bypassed: no_spec_unverifiable` 一行, 能与 S4 区分; 第 8 条的非判定键取值与 §1.0 短路语义一致; TASK-006 里改写后的 SC-17(5) 四格与三条反事实可证伪。只有括注措辞有歧义, 见 m3。
- **(b) 组 5 发布前提偏重 —— 5.8 的四方相等断言可接受; 5.2 强制对齐只有一半可接受。** 5.8: 本席实测今天就成立 (aria-orchestrator detached 于 `237045a`, 本地 master 与两端同值; standards `8b49562` 同), 它是防止 C.2.5 顺带推出他轨内容的必要前置, 不成立时停下上报方向正确。5.2: 回退本轨自己的 `--no-push` 心跳可接受 (有第 14 项兜底); 但同一操作会抹掉他轨尚未授权的本地写入, 这一半不可接受, 见 M6。
- **(c) N1/N2 是按行切片的文本谓词、SC-11 收紧为 present、SC-6 快照放活体 —— 可接受。** N1/N2 只是补充的落点检查, 语义由 SC-16 / SC-18 / SC-17(5) 的运行时断言守, 三态实跑本席已独立复现 (与嵌入输出逐字节一致)。SC-11 收紧为 `present` 是对的: 届时本轮报告已在顶层, 规则 2 能命中本 id。SC-6 快照格放活体可以接受, 通用规则由单测的 (3) 格守; 代价是合并树回归 (TASK-027 第 7 步) 不复跑快照格, 建议在周期 handoff 注明。

## 风险 / 疑问 (不计入 finding)

- Phase B 期间主仓工作树长期停在 feature 分支, 同容器其他会话 (会话收尾、#195 的 Phase D) 的提交会落到哪条分支, 计划没写; 与 M7 相关。
- 心跳节奏: Phase B 预估百余小时, 计划只在 TASK-001 显式心跳一次, 其余依赖各会话入口 state-scanner 的心跳; 会话中断超过 STALE_TTL 时走第 14 项。
- `.aria/config.json` 里 `_open_question_no_ci_fallback` 仍待 owner 定; TASK-030 若遇到 probe=False, 会按 `skip_with_warning` 放行, 建议届时在台账与 handoff 点名。
- TASK-022「stderr 不含 base ref 陈旧」对规定命令恒真, 计划已自述只防命令被改回裸 `master`, 不计 finding。
- 重写 a 的反事实成立: `spec_complete.py:924-930` 对非 SKILL.md 的 `.md` 一律判散文, 测试路径整体跳过 (`:1071`), 所以 execution-modes.md 的围栏调用串与测试文件都不会让 L2 误绿; 已知盲区只有 phase-c-integrator/SKILL.md 的 bash 块, yaml `:198` 已声明。

## Verdict

- **verdict**: PASS_WITH_WARNINGS
- **counts**: `0C/8M/8m`
- **Vote: REVISE**

## 是否足以开始 Phase B

**还不足以开始。** 除了 B.1 本来就要等 10CG/Aria#195 完成 C.2 之外, M1 与 M2 会让组 2 的逐任务验收和按 DAG 并行的调度在实现一开始就红或卡住; M5、M6、M7 三条涉及外向动作的防护与授权面。这五条须先在 A.2/A.3 修订里改掉, M3、M4、M8 可以同批修。
