---
checkpoint: post_planning
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-22T15:54:30.031Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R6 — code-reviewer 席 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v2.5)

## 已实读文件

派单 sha256[:16] = a106b7adee59a169

- 派单原件全文 (115 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (240 行)
- `detailed-tasks.yaml` 全文 1-1982 行。`revision_log` 的 v2.5 八条 (776-783) 按流程应在独立复算之后读, 实际情况见下方「流程披露」
- `git diff b686185 e7a1782`: tasks.md 8 个 hunk、yaml 全部 hunk (逐行按词比对)、gen_yaml.py 45 个 hunk (逐行看非字符串字面量的改动)
- R5 聚合报告全文 (157 行); 决策单全文 (116 行); CLAUDE.md 的多远程两条硬约束与 Rule #3 / Rule #6 / Rule #8 / Rule #10 (注入上下文)
- proposal.md: 全文 sha256 + 行 4/9/10/14/16/18/23/70/77/80/103/122/130/136/140/149/267/407/409/428/429/451/453/462/467/468/469/473/480/488/510 的行首
- aria @ `1cb3872` 如下
  - phase-c-integrator: `SKILL.md` 42/57/131/132/157/160-219/406-600/603/612-638/754; `scripts/submodule_gate.sh` 全文; `scripts/pre_merge_gate.py` 508-583; `tests/test_pre_merge_gate.py:266`
  - state-scanner: `SKILL.md` 180-192; `scripts/phase1_gate.py` 1125-1204 与 1415-1470; `scripts/release_gate.py` 16/43-227/318; `lib/failure_handlers.py` 282-400 与 594-680; `lib/coordination_ref.py` 1332-1370; `lib/claim_lifecycle.py` 475-555; `lib/constants.py` 55-58; `lib/identity.py:192`; `lib/claim_schema.py` phase 字段; `scripts/lib/spec_complete.py` 268-276 / 730-745 / 860-929 / 1636-1644; `scripts/collectors/custom_checks.py` 15-45; `scripts/check_bare_issue_refs.py` 120-157
  - 其它: `session-closer/scripts/handoff_autofill.py` 391-470; `phase-d-closer/SKILL.md` 58 / 228、`references/execution-steps.md` 106-108、`references/handoff-mechanics.md` 84-135; `openspec-archive/SKILL.md` 98-356; `audit-engine/SKILL.md` 381/385/423/427、`references/execution-modes.md` 9/10/15/34/43/44/66/82、`report-storage.md:8`、`pre-write-validation.md:3`; `phase-a-planner/SKILL.md` 246/267; `phase-b-developer/SKILL.md` 204/214/255/277; `task-planner/SKILL.md:123`; `brainstorm/SKILL.md:141`; `config-loader/DEFAULTS.json:130`; `run_all_tests.sh` 41-46; `git-remote-helper/scripts/push_all_remotes.sh` 103-119; `CHANGELOG.md` (小节计数 / :104 / :200); `VERSION` 7-8; `.gitignore` 6-13
- 主仓 `37335d4`: `.aria/config.json` (audit 与 phase_c_integrator 段); `.aria/state-checks.yaml` 1-70 / 124-176 / 177-220 / 302-353 / 408-436; `.aria/probes/main-project-version-consistency.py` 关键行; `.gitignore` 28-38; `VERSION:24`; 四份 README、CLAUDE.md 与两份 architecture 文档的版本点; `docs/handoff/latest.md` (History 检索与 pointer 行); `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 87 / 160-229 / 514 及其 `a563192..HEAD` diff; `ab-suite/version.yaml`; `ab-results/2026-09-03-v1.69.0-sibling-spec-probe-rule6/PREDICTION.md:4`
- standards @ `940cb5b`: `conventions/session-handoff.md` 111-218; `conventions/content-integrity.md` §4.5; `openspec/project.md:117`; `openspec/templates/proposal-minimal.md` 28-32
- 生效的 skill-creator (`ea0a38e1d671`) `SKILL.md` 165-188 与 workspace 相关行
- 协调 ref (只用 `ls-tree` / `show` 读): 本容器前缀下本轨两条 claim
- 轨级 handoff `docs/handoff/2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md` 143-209 (含「v2.5 返修」「执笔实例提请裁定 (十条, v2.5)」两节, 在独立结论写下之后才读)
- 未打开: 本轮其它席位的 R6 报告 (工作区里已出现另三席的文件)

**流程披露 (影响独立性的两件事)**:
(1) 第一步按要求完整读派单, 所以开工时就已看到派单末尾那一节的九条薄弱点清单。当时没有看到 revision_log 与 handoff 的两节。
(2) tasks.md 与 yaml 的全部 hunk 逐个读完后、写下独立结论前, 我为查生成器用法跑了 `tail -30 gen_yaml.py`, 输出末尾正好是 revision_log 的 v2.5 八条, 等于提前看到了自述。发现后我当即把读 diff 时已形成的 12 个疑点写进 scratch (`audit-R6-code-reviewer/independent-notes.md`)。此后的结论都来自我亲跑的命令和源码实读, 没有以自述为依据。

## R5 对账

| 键 | 判定 | 亲验证据 |
|---|---|---|
| R5-M1 `9c294cca` | closed | TASK-031 第 8 条 (D.2b) 只请 13a, 第 14 条产生 latest.md 单独提交, 第 15 条才请 13b (yaml:1975 / 1981 / 1982); owner_gates 13a / 13b (yaml:218-219); 等待点表两行 (tasks.md:121-122)。两文件全文脚本检索「第 13 项 / 等待点 13」, 不带 a / b 的只剩「原第 13 项」这类历史叙述。原来「在同一批次内附一份尚不存在的 diff」的死锁已不可能出现 |
| R5-M2 `3e6a8483` | closed | hard_constraints 第 4 条 (yaml:194) 和第 14 / 15 项 (yaml:220-221) 都挂到任一会话入口; TASK-024 前后两端有处置 (yaml:1804 / 1815); TASK-031 的 release 遇 `claim_not_found` 单列 (yaml:1975)。代码事实实读: `phase1_gate.py:1136` 心跳「no fetch of its own」, `:1146` 恒退出 0; `lib/coordination_ref.py:1367` 的 fetch refspec 是非强制的 `refs/aria/coordination:refs/aria/coordination`; `release_gate.py:67 / 153 / 318` 把 claim_not_found 记为 benign 并退出 0。N11 复跑两次, 与嵌入 output 逐字节一致 |
| R5-M3 `3782becc` | closed (残余 minor 见 m1) | TASK-030 新条 (yaml:1944)、第 17 项 (yaml:223)、tasks.md 5.8 行与范围表 (tasks.md:185 / 134)。实读 `submodule_gate.sh` 全文, 与计划描述逐项相符: 退出码表 :20-27; MODE 只读环境变量, 缺省 block (:33), 头注释 :15-16 与代码不符; trivially passes 在 :224-227; directory absent 在 :231-234; 行格式 OK / GATE / PASS 在 :259 / 263 / 267。另核了「C.2.4 green 之后」这个锚点在无 backend 的降级路径下是否存在: `pre_merge_gate.py:527-535` 在 skip_with_warning 时返回 verdict=green, 所以存在 |
| R5-M4 `c287d217` | closed | TASK-027 第 4 步 (b) 先 `cat-file -e`, diff 按退出码判 (yaml:1873); guard 改为 `git -C <主仓根> grep …; echo "rc=${PIPESTATUS[0]}"`, 判据是 rc 属 {0,1} 且无命中行 (yaml:329); 三个调用点 TASK-021 / TASK-027 第 7 步 / TASK-031 同步 (yaml:1749 / 1876 / 1973)。N10 复跑逐字节一致: 从 `aria/skills/audit-engine/tests` 起跑且 config 含符号时, v2.4 命令 0 行 (旧读法放行), v2.5 为 rc=0 且 1 行 (停); 目标不是仓时 rc=128 (停)。`cat-file -e` 实测: 不存在的完整 SHA 退出 1, 带 `^{commit}` 或短 SHA 时退出 128; 计划两处用法的判据都与实际退出码相符 |
| R5-M5 `76921ca3` | closed | TASK-024: 工作区只放 ab-workspace、比较两次 find 之差、每条快照命令验退出码 (yaml:1809-1810); TASK-018 的递归检索条已注明 (yaml:1683)。补测两项: (i) 归档门的 liveness 分类器用 `git grep --recurse-submodules`, 只搜已追踪文件 (`spec_complete.py:867-892`), 被忽略的 ab-workspace 带不绿 L2; (ii) 本机已有的 `aria/skills/issue-triage-workspace/` (34 个文件, `check-ignore` 命中 `.gitignore:7`) 对 SC-13 的 timestamp 检索和 no-unresolved-version-placeholder 都是 0 命中, 两项检查当前分别为 4 处基线残留和 rc=0 |
| `1453c41f` | closed | TASK-027 第 4 步 (c) (yaml:1873) 比较两处: 两个 skill 目录的 `W..feature`, 以及 ab-suite/audit-engine.json 的「结果提交..工作树」; 非空时逐 hunk 按 Rule #6 表分类。第 6 项同步 (yaml:211); TASK-024 末条记下结果提交 SHA (yaml:1816) |
| `118d1d64` | closed | TASK-031 的 deliverables 已含 `docs/handoff/latest.md` (yaml:1964) |
| `ac2e8dcb` | closed | 起稿条 (yaml:1977) 先看退出码, 退出非 0 或输出为空时按 `handoff-mechanics.md:92` 回退手填; 实读 `handoff_autofill.py:463-466`, 失败时确为 `print("")` 加 `return 1`。值非空检查 (yaml:1978) 用样例实跑: owner-container 为空时 E1=5、新检查=4, 与计划所述一致。残余: 写成 `owner-container: ""` 时新检查仍得 5。回退规则产出的是不带引号的值, 可能性低, 不立项 |
| `11c3a29f` | closed | aria_shifted 拆为三条 (yaml:77-79), TASK-001 补「路径至少在一端存在」(yaml:1355)。实测: 旧的连写串 `git diff` 得 rc=0 且输出为空, `cat-file -e` 两端都是 128, 所以新判据会停; 四组 50 条路径两端逐条 `cat-file`, 全部至少在一端存在 |

## 视角核验

**1. 三态证据复跑**。两份共享副本 `cp -a` 到本席目录。脚本取自 yaml 的 `a2_state_runs.script` / `v2_state_runs.script` 全文 (用 python 从 yaml 抽取, 不用 scratch 文件), 按其 `command` 跑, 输入是当前 v2.5 的 tasks.md 与 yaml。
- a2: rc=0, 2396 字节, 与 `output` 逐字节一致 (cmp)。
- v2 (含 N9 / N10 / N11): rc=0, 6690 字节, 逐字节一致。再跑一次仍一致 (N6 / N11 依赖时间, 两次都稳定)。
- 副本事后复原干净; 真仓 `git status` 只多出他席报告。
- 另按工具 README 在副本里重新生成 yaml, 与 `e7a1782` 逐字节一致 (REGEN_IDENTICAL)。

**2. 引用精度抽查 (32 处, 全部实读, 全部一致)**。aria 侧对 `1cb3872` 读, 主仓 / proposal 对当前文件读:

| 引用 | 实读 | 一致 |
|---|---|---|
| state-scanner `SKILL.md:182` / `:191` | 心跳触发条件「本会话持 active claim」/ fail-soft 只记遥测 | 是 |
| `lib/constants.py:58` | `SWEEP_TTL: int = 86400` | 是 |
| `spec_complete.py:733-744` / `:273` / `:924` / `:1642` | `_is_hooks_or_config_path` / checkbox 读取 / `if name == "SKILL.md"` / 两文件皆缺早退 | 是 |
| skill-creator `SKILL.md:167` / `:186` | 「as a sibling to the skill directory」/ `cp -r <skill-path> <workspace>/skill-snapshot/` | 是 |
| `.aria/state-checks.yaml:29-46` | 该检查占 29-44, 45 空行, 46 是下一条的注释 | 是 (范围宽 2 行) |
| phase-c-integrator `SKILL.md:57` / `:754` / `:132` / `:131` / `:157` / `:42` | 字面键条件 ×2 / 步骤 3 / 步骤 2 / `pre_merge-{timestamp}.md` / 配置表缺省行 | 是 |
| audit-engine `SKILL.md:423` / `:381` / `:385` / `:427` | hotfix 条件 / 两个 allow_* 注释 / 相关文档节 | 是 |
| `execution-modes.md:9` / `:10` / `:15` / `:43` / `:44` / `:82` | 与计划所述逐一吻合 | 是 |
| `phase-a-planner:246 / 267`、`phase-b-developer:204 / 214 / 255 / 277`、`task-planner:123`、`brainstorm:141` | 同上 | 是 |
| `report-storage.md:8`、`pre-write-validation.md:3`、`DEFAULTS.json:130` | 5-field 形态 / 关联行 / `"level_1": "off"` | 是 |
| `test_pre_merge_gate.py:266`、`run_all_tests.sh:41-46` | 真实方法名 / `is_pytest_suite` | 是 |
| phase-c-integrator `SKILL.md:603 / 612-616 / 623-630 / 638`、`push_all_remotes.sh:103-119` | C.2.5 五问所引各点 | 是 |
| proposal `:77-80` | 与 canonical_call 逐行相等 (N4 复跑输出为 True) | 是 |
| proposal `:122 / 267 / 407 / 409 / 429 / 451 / 462 / 467-469 / 473 / 510` | 行首与引用语境相符; 全文 sha256 为 `d3c9b4f2…6f34`, 与 `a563192` 同 | 是 |
| standards `openspec/project.md:117`、`templates/proposal-minimal.md:28-32` | Level 2 只出 proposal.md / 模板自带 `## Tasks` | 是 |
| aria `CHANGELOG.md` `[1.73.0]:104`、`[1.70.0]:200`; aria `VERSION:7 / :8` | 与计划相符 | 是 |
| 主仓 `VERSION:24`、`README.md:8`、`README.zh.md:3 / :10`、`system-architecture.md:189` | `v1.73.0` / 各版本点 | 是 |
| `CLAUDE.md :139 / :141` | 现在在 `:138 / :142` (两处仍在, 共 16 个版本点不变) | 是 (计划已写以执行时 grep 为准) |
| `execution-steps.md` 的 E1 命令、`handoff-mechanics.md`「任何 cycle 都不可跳过」、phase-d-closer `SKILL.md:58` | :106 / :135 / push_success 条 | 是 |
| `latest.md` History 来历 (`16b5bf1` / `ecb6296`, 父提交 `3f4b379` / `9f25a66`) | History 标题计数 1 / 0 / 1 / 0, 当前 latest.md 为 0 | 是 |
| 先例 `3d3c820`、v1.69.0 `PREDICTION.md:4` | 主仓 `.gitignore` 加 ab-workspace / 旧版快照在 `ab-workspace/…/skill-snapshot` | 是 |

**3. 命令可执行性 (只读试跑)**
- 从 `sc13_baseline` 抽 12 项, 连同 timestamp 残留检索 (4 处), 在当前树复算, 计数与退出码全部相符。`grep -c` 对缺失文件的 stdout 为空、rc=2, TASK-018 新判据所据属实。
- TASK-027 第 3 步: `1cb3872` 上 CHANGELOG 的小节集合为 138 条, 与计划一致。
- TASK-026: `check_bare_issue_refs.py` 的退出码 0 / 1 / 2 与末行格式 (:129 / :139 / :146 / :150 / :153) 与计划相符; §4.5 命令遇缺文件退出 1。
- TASK-021: python 3.11.2 下对空目录跑 discover 输出 OK、rc=0, 计划所述属实; audit-engine tests 当前为 Ran 104 OK。
- TASK-001: 取容器 id 的命令可跑; 协调 ref 布局为 `claims/<容器>/<session>.yaml`, 与 N6 / N11 一致。四组 50 条路径全部至少一端存在; aria 零 diff 组 27 条仍为零 diff。main_repo 组的 `AB_TEST_OPERATIONS.md` 在 `a563192..37335d4` 已有 +36/-2 (场景 4 拆分), 但计划所引的规则 1 (:173)、场景 1 验收 (:220) 与第 2 / 3 步 (:228-229) 未动, 这属于 TASK-001 偏移表流程的正常输入。
- 重新认领的 `--phase` 取 B / C / D 可行: `phase1_gate.py:1431` 与 `claim_schema.py:92-93` 都是自由文本。
- TASK-029 的 custom checks: 见 m2。

**4. git 序列 (5.5–5.8)**
- fetch 只动远程跟踪 ref。5.5 第 1 步、C.2.4.5 闸内的 fetch (`submodule_gate.sh:189`, 各子模块 :245)、5.8 合并后的 fetch 都不会覆盖本地未推的 master / feature / tag。
- 断言的是本次新产生的对象: 5.5 第 5 步断言 `HEAD≠S3` 且 `HEAD^2=feature` (v2.5 补了两次 rev-parse 须退出 0); 5.6 逐 remote 逐行核 master / tag / `^{}`; 5.8 断言 M 是 HEAD 的祖先且 `M^2=feature HEAD`。
- 合并后问了「这个值现在该是什么」: 5.8 末条复跑 custom checks、重算 ab-suite 计数、复读 version.yaml。
- 新增的 C.2.4.5 位于 C.2.4 之后、Forgejo 合并之前, 运行时 HEAD=PR head, 与 C.2.5 的子模块断言不冲突; 三个子模块都配有 origin 与 github 两个远端 (`git remote -v` 实测)。

**5. 归档门预演**
- 用 v2.5 的 tasks.md 复跑 C 态 (全勾选 + 脚本 + SKILL.md 的 bash 块): gate 判 verdict=warn、exit 0, blocking_on_symbol=0; warn 的唯一来源是 4.4 行 dogfood 无可链接产物那条 unverified_claim; `d_payload` 非空。结果与 v2.4 同态, v2.5 改过的 4.3 / 5.5 / 5.8 / 5.9 行没有新增集成类或 dogfood 类声称。
- openspec-archive Step 7 的触发条件是 `d_payload != null`, 且不看 ack (`SKILL.md:287-296`), 所以 warn 下会自动在 Forgejo 建 tracker issue (外向动作)。计划在 D.2 之前请第 11 项裁 (yaml:216 / 1974), 已登记。

## 独立复算 vs 执笔自报的差异

**我看到而自述没提的**
1. C.2.4.5 的 override 描述与本计划的调用时机不适配, 放行判据也没收 `ALLOW:` 行 (m1)。
2. 同族残余: `plugin-version-arch-docs-match` 读不到 plugin.json 时输出 `##SKIP##` 并退出 0 (m2)。
3. N11 的「v2.5 order」段之前先跑过一次失败的 v2.4 顺序心跳, 所以它的前置检查输入是 `local_ahead=1 own-heartbeat`, 而按生产顺序会遇到的是 `local_ahead=0`。revision_log 写「按 v2.5 顺序 (前置检查退出 0、强制对齐、重解析) 为 True」, 没点出这一差别。两种输入下前置检查都退出 0, 结论不受影响。
4. C.2.4 在无 backend 降级时仍给 verdict=green (`pre_merge_gate.py:527-535`)。这是 C.2.4.5 的「green 之后」锚点在降级路径下成立的前提, 自述没有论证; 我实读后确认成立。
5. v2.5 在 TASK-031 写了「本任务自身不跑 commit_attribution」(yaml:1981), 与同任务起稿条的「track-id 写错 ⇒ 停在第 16 项」(yaml:1977) 在同一任务内明文冲突; 而且新增的值非空检查对拼错的 track-id 同样得 5。这是已知项 (A) 的新证据, 见风险节。
6. 本机已有的 issue-triage-workspace 当前对两个递归检索面都是 0 命中。自述只把它当作不选 (b) 的理由, 没说它现在是否已经造成污染。

**自述声称而产物不符, 或无法从产物复核的**
1. revision_log 的同族扫描条写「对 baseline_rebase 四组 48 条路径逐条 cat-file -e」。按 v2.5 产物计是 50 条 (27 + 8 + 7 + 8); 48 只对得上拆分前 aria_shifted 还是 6 条时的计数。产物本身没问题 (50 条全部至少一端存在), 是记录口径不准。
2. handoff 所称「160 个候选, 改 41 条 + 经所引规则改 5 条, 114 条不受影响」和「交互表 9 张」不在仓内 (revision_log 写的是「由 v2.5 执笔报告呈主控」), 从仓内产物无法复核「漏 0 多 0」。我换一套词表扫判据文本, 得到 191 个位置, 逐条看过后只在计划所引检查命令的内部找到 m2 一处。
3. 其余自述都与产物一致: 五题与两条同处 minor 的修法、N9 / N10 / N11 输出、a2 输出不变、版本标识四处与 container 字段、判断清单第 40–45 条、三段嵌入代码的改动 (gen_yaml.py 在字符串之外只改了这三段和 header)。

## Findings

**m1** · id `749f8d15` · minor · issue · implementation · `detailed-tasks.yaml TASK-030`
- summary: C.2.4.5 条与第 17 项对 override 的描述不适配本计划的调用时机; 放行判据也没收 override 生效时打印的 `ALLOW:` 行。
- 证据:
  - 第 17 项 (yaml:223) 与 TASK-030 (yaml:1944) 把 override 写成「合并提交的 Submodule-Rollback: trailer」或 PR 标签。
  - `submodule_gate.sh:101` 为 `msg=$(git log -1 --format=%B HEAD 2>/dev/null || echo "")`, 即闸读的是运行时 HEAD 的提交信息。计划规定闸在 Forgejo 合并之前、HEAD=PR head 时跑, 此时 Forgejo 的合并提交还不存在, 写在合并提交里的 trailer 闸看不见。
  - `submodule_gate.sh:296-299` 在 override 生效时打印 `ALLOW: <sub> <VERDICT> overridden ...`, 然后继续并最终退出 0; 但 yaml:1944 的放行判据只收「GATE: 加 PASS:」或「OK: … unchanged」。
- 失败场景: 某子模块判 REGRESSION 或 DIVERGENT 后停在第 17 项, owner 裁 override。若 owner 照计划措辞把 trailer 写在合并提交里, 合并前跑的闸仍然 BLOCK。若 owner 给 PR 加标签, 重跑得到退出 0 加 ALLOW 行, 字面放行判据仍不满足, 于是又回到第 17 项。执行者不会做错事 (始终 fail-closed, owner 也可以自己在 Forgejo 合并), 代价是多一轮或多轮 owner 往返。
- 建议修法: 在第 17 项与 TASK-030 该条写明: 本调用方式下 trailer 须在 PR head 提交上 (或只认 PR 标签); owner 裁 override 后, 放行判据是退出 0、被 override 的子模块有 `GATE:` 加 `ALLOW:` 行、其余子模块照旧。

**m2** · id `29325b2c` · minor · issue · testing · `detailed-tasks.yaml TASK-029`
- summary: 同族扫描的「已知形态」清单漏了 TASK-029 复跑的 `plugin-version-arch-docs-match`: 它读不到 plugin.json 时输出 `##SKIP##` 并退出 0。
- 证据:
  - `.aria/state-checks.yaml:419` 为 `[ -z "$PLUGIN" ] && { echo "##SKIP## aria/.claude-plugin/plugin.json 不可读"; exit 0; }`; `custom_checks.py:24` 把「退出 0 且首行为 ##SKIP##」映射为 skip (既不算 pass 也不算 fail)。
  - 副本实跑: 在主仓根输出 `OK plugin=1.73.3 (2 arch doc rows match)`, rc=0; 从 `aria/skills/audit-engine/tests` 起跑输出 `##SKIP## aria/.claude-plugin/plugin.json 不可读`, rc=0。
  - hard_constraints 第 14 条 (3) (yaml:204) 称已把「退出 0 仍可能没比成」的已知形态逐处写进条目, 同一条 custom checks 里为 no-unresolved-version-placeholder 补了 `test -d aria/skills` (yaml:1924), 却没有列这个检查。
- 它怎么会红 (三态): 基线 (主仓根, 版本一致) 为 OK / rc=0; 目标 (发版后在主仓根) 为 OK / rc=0; 坏态 (目录错) 为 ##SKIP## / rc=0。只看退出码时, 坏态与通过同形。
- 失败场景 (为何只是 minor): 计划要求这些检查「为 OK」且「在主仓根跑」, 照字面执行时 ##SKIP## 不等于 OK, 执行者会停下; 只有只看退出码的读法才会放过。照字面执行的结果不变, 所以这属于清单完整性问题。
- 建议修法: 在第 14 条 (3) 与 TASK-029 该条补一句: custom checks 以输出首行为 OK 判通过, ##SKIP## 视为没跑成 (或同样先跑 `test -d aria/skills`)。

## 对执笔人自报薄弱点的表态

(1) 可接受。我逐类看了 `coord_ref_precheck` 的判定: 空 diff 提交、合并提交、跨他人文件的提交、改动不止 heartbeat_at 一行的提交都判 other (fail-closed)。只有「文件属于 own 集且每个文件恰好一对 heartbeat_at 行」才判 own-heartbeat, 所以对齐丢掉的只可能是心跳时间戳。own 集取自落后的本地解析, 也不改变这一点。未见盲区。
(2) 可接受。这是 `SWEEP_TTL`=24h (`lib/constants.py:58`) 与「心跳靠会话入口触发」这一设计的固有代价, 计划已如实登记并用第 14 项兜底; 「隔日续做算新会话」也把同一会话跨日的情形纳入了。
(3) 可接受。13a 已批而 13b 未批时, 协调 ref 上的 done 反映的是执行实况, 归档与 handoff 只是晚推; owner 本人就在这个决策里, 另设机制收益小。
(4) 可接受。方向是 fail-closed。但同一判据还漏了 `ALLOW:` 行 (m1), 建议一并改。
(5) 可接受, 但有残余。我换词表独立扫描, 在计划文本面之外 (所引检查命令的内部) 找到一处同族形态 (m2), 印证了「按词形生成候选」看不见被引命令内部的行为; 该处已被正向断言兜住。
(6) 可接受。通则对未知形态 fail-closed。我核了 `cat-file -e` 的 1 与 128 之分、unittest 空集输出 OK、`grep -c` 缺文件时 rc=2, 计划各处用法都与实测一致。
(7) 可接受。方向是 fail-closed, 而且计划要求差值逐条归因, 由 owner 判。注意 TASK-021 比的是 A.2 时 `1cb3872` 上的值; B.1 起点若已前进, 需要归因的情形会更多, 但不影响正确性。
(8) 可接受。sweep 走的是生产用的 `sweep_stale_active` (拿 heartbeat_at 与 SWEEP_TTL 比较), 改时间戳只是为了加速。另见差异节第 3 条: v2.5 顺序段的前置检查输入与生产不同, 但结论不变。
(9) 可接受。同体自检的边界如自述所说。本轮我独立找到的两处 (m1 / m2) 都长在修法新建的东西与既有部分的接缝上, 但都没到 major。

## 风险 / 疑问 (不计入 finding)

1. **已知项 (A) 重新评估 (留在风险节, 不立 finding)**。新证据两条:
   - v2.5 在 TASK-031 的 latest.md 单独提交条写了「本任务自身不跑 commit_attribution (它只在 TASK-001 与 TASK-030 调用)」(yaml:1981), 与同任务起稿条的「track-id 写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项」(yaml:1977) 在同一任务内明文互斥。
   - 样例实跑: track-id 拼错一个字母时, E1 与 v2.5 新增的值非空检查都得 5。漏写会被 E1 抓到, 写错抓不到。
   我判其低于 major: 要触发, 需执行者把计划里逐字给出的串转录错; 后果是一份 handoff 的归属元数据出错, 可以事后更正。最小修法: 在值非空检查旁加一条 `head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope'` 须为 1, 并删掉起稿条里不可达的「停在第 16 项」。
2. **执笔十条请裁 (B) 表态**:
   - 第 1 条: 同意选 (a)。分类器只搜已追踪文件, ab-workspace 也不在两个递归检索面上, 均已实测。
   - 第 2 条: 同意新立第 17 项, 但放行判据需补 `ALLOW:` (m1)。
   - 第 3 条: 同意。强制对齐的安全性见表态 (1)。
   - 第 4 条: 同意只记台账。
   - 第 5 条: 通则不算过宽, 「运行目录钉死」与「子模块先确认已检出」都是低成本的前置。
   - 第 6 条: 同意比到工作树。它对应的预存缺口见本节第 3 条。
   - 第 7 条: 同意交 owner 在 13b 裁。
   - 第 8 条: 同意。TASK-027 第 7 步在合并树上复跑 L2 之前确实需要 guard。
   - 第 9 条: 建议顺手勘正。TASK-001 的 verification 第 1 条是入口前置, claim 身份是第 2 条 (实读 yaml:1347-1348)。
   - 第 10 条: 同意计划侧兜住即可, 改检查本身应另开他轨。
3. **预存缺口 (非 v2.5 引入)**。TASK-026 第一次自检若改了主仓侧已提交的本 cycle 文件 (如 ab-suite/audit-engine.json 的 eval 文本、本目录的 corpus-freeze.md、结果目录的 README), 计划里没有提交这些改动的步骤, 到 TASK-030 第 1 条「porcelain 不得有行触及本 cycle 交付物」就会停。v2.5 在 TASK-027 第 4 步 (c) 里已写明「主仓侧没有先提交 TASK-026 改动的一步」, 用比到工作树绕了过去, 但没把后果推到 TASK-030。建议在 TASK-026 或 TASK-029 补一步提交 (带 Spec trailer)。
4. **PR head 变化后是否重跑 C.2.4.5**。计划要求闸跑在「已推送的 PR head」上, 但没写闸跑完后若 PR head 又变 (例如同步合并后重新推送), 须重跑 C.2.4 与 C.2.4.5。在 merge commit 合并方式下, 同步本身不会造成指针回退, 风险低。
5. **同族扫描清单与交互表不在仓内** (见差异节), 后续审计无法从仓内产物复核「漏 0 多 0」。若 owner 看重可审计性, 可让执笔把两份清单落进工具目录。
6. **frontmatter 的 `drift_check_skipped`**。`.aria/config.json` 的 audit 段没有 drift_guard 键, convergence 模式下 drift-checker 未 opt-in, 所以本席按事实写 `true`。派单模板字面为 `false`; R5 聚合已按 `true` 重算。
7. **信息性**: main_repo 组的 `AB_TEST_OPERATIONS.md` 在 `a563192..37335d4` 已是非零 diff, B.1 复核时应进偏移表; 计划所引段落未动 (已核)。

## Verdict

**PASS** — 0C/0M/2m — **Vote: PASS**

## 是否足以开始 Phase B

不足以: 计划本身已无阻塞项 (0C/0M, R5 五题与四条关联 minor 全部 closed), 唯一阻塞是 owner_gates 第 1 项入口门 (10CG/Aria#195 尚未完成 C.2, 也没有 owner 明示改序), 该门满足后即可进 B.1。
