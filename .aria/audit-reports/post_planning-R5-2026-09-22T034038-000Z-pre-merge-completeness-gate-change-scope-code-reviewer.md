---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-22T04:59:43.926Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R5 — code-reviewer 席 (证据与命令可执行性 + 本轮指派的独立复算)

被审: 10CG/Aria#199 `pre-merge-completeness-gate-change-scope` A.2/A.3 v2.4 (计划三文件在 `b686185`, 主仓 `cf05d8b`; 自 `b686185` 起计划目录与工具目录零改动, 已核)。drift 三字段按 `audit-engine/references/report-format.md:145-153`「单 agent 报告默认 false、由聚合覆盖」照派单模板写 false。

## 已实读文件

派单 sha256[:16] = 26532c7c20afcfed

- 派单原件全文。**披露**: Read 工具一次返回了整份文件, 包括末尾「独立复算完成后再读」一节 (六条自报薄弱点), 工具层无法先不看; 此后我按顺序先对三文件 diff 逐 hunk 独立复算, 把结论先落盘到本席 scratch (`audit-R5-code-reviewer/independent-notes.txt`), 然后才读 yaml `revision_log` 的 v2.4 五条与轨级 handoff 的「v2.4 返修」「执笔实例提请裁定 (九条, v2.4)」两节。
- 被审文件: `tasks.md` 全文 (232 行); `detailed-tasks.yaml` 全文 (1818 行; `revision_log` 的 729-758 行在独立复算完成后才读)。
- diff: `git diff 71c500e b686185 --` 三文件全部 hunk (yaml 11 个 / tasks.md 5 个 / `gen_yaml.py` 12 个)。
- R4 聚合报告全文; R4 code-reviewer 席报告的 Findings 与 R3 对账两节 (64-175 行); R1 cr 与 R3 tl 两份只按关键词取 `SWEEP_TTL` 上下文 (查是否提过跨会话保活)。未打开任何 R5 他席报告。
- `proposal.md`: `:407` / `:453` / `:469` (SC-13) / `:473` / `:480` / `:488`, `:409-451` checkbox 计数, `a563192` 版 sha256。
- 决策单全文 (§1-§5, 116 行); `CLAUDE.md` 多远程两条硬约束与Rule #3 / Rule #6 / Rule #8 / Rule #10 (会话上下文已载)。
- 源码 (aria `1cb3872`, 实读): `phase-d-closer/SKILL.md` 全文; `phase-d-closer/references/execution-steps.md` 全文; `references/handoff-mechanics.md` 全文; `templates/session-handoff.md:1-30`; `session-closer/scripts/handoff_autofill.py:391-470`; `openspec-archive/SKILL.md:98-287` 与结构; `state-scanner/SKILL.md:170-200`; `state-scanner/lib/constants.py:20-58`; `lib/claim_lifecycle.py:300-335, 378-428, 505-560`; `scripts/collectors/handoff_multibranch.py:14-40`; `lib/spec_complete.py:55-75, 273, 733-744, 832-897`; 另逐行抽查见下表。
- 主仓: `docs/handoff/latest.md` 顶部与全文计数; `.gitignore`; `aria/.gitignore`; `.aria/config.json` audit 段; `.aria/state-checks.yaml:25-50`; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:85-88, 199-230`; 先例提交 `3d3c820` / `2a46d08` / `2892c6f` / aria `e83be99` / `71c500e`; 本地协调 ref 上本容器 claim (只读 `git show`)。
- skill-creator (生效安装 `ea0a38e1d671`): `SKILL.md:167`, `:186`。

## 视角核查结果

**1. 三态证据复跑**: 从 yaml `metadata.a2_state_runs.script` 取全文 (sha256 `8828a7ad53f451c6…`), 在 `state-base` 的 `cp -a` 副本上按其 `command` 跑, 后两个参数用真仓 v2.4 的 `tasks.md` 与 yaml ⇒ rc 0, 25 行输出与嵌入 `output` **逐字节一致** (`cmp`); 副本复原后主仓与 aria 两层 porcelain 均 0 行。另: `standards_files_derivation.script` 在 `base` 副本主仓根复跑, 逐字节一致; 以 yaml 内嵌两组 script/output 为输入重跑生成器, 产物与 yaml 逐字节一致 (REGEN_IDENTICAL)。

**2. 引用精度抽查 (37 处, 全部一致, 除注明外)**:

| 引用处 | 被引 | 实读结论 |
|---|---|---|
| yaml:1814 / tasks.md:79 | `phase-d-closer/references/execution-steps.md:105-108` E1 命令与口径注 | 一致 (逐字) |
| yaml:1814 | `standards/conventions/session-handoff.md:218` (§2.3.7 E1) | 一致 |
| yaml:1813 | `session-handoff.md:111` (§2.3.1) | 一致 |
| yaml:1813 | `handoff_autofill.py:457-466` `--owner-container` | 一致; 失败时打印空串、exit 1 (见 m3) |
| yaml:1813 | `handoff-mechanics.md:86` 机械填勿手动组装 | 一致; 同段 `:92` 有失败回退, 计划未抄 (m3) |
| yaml:1815 | `handoff-mechanics.md:106-112` History 格式 | 一致 |
| yaml:1815 | `handoff-mechanics.md:135`「任何 cycle 都不可跳过」 | 一致 |
| yaml:1816 | `handoff-mechanics.md:116-124` 三行判定表 | 一致 (「由 user 判断」写成「由 owner 判断」, 等义) |
| yaml:1816 | `handoff_multibranch.py:14-40` `exists` / `tracks[].status` | 一致 |
| tasks.md:79 | `phase-d-closer/SKILL.md:58` 须看 `push_success` | 一致 |
| yaml:1805 | `execution-steps.md:45-63` D.post 条件 / convergence / max_rounds=1 / 不阻塞 | 一致 |
| tasks.md:79 | `phase-d-closer/SKILL.md:228` D.4 触发 | 一致 |
| yaml:1813 | `templates/session-handoff.md:1-7` 五字段 frontmatter | 一致 |
| yaml:1648 | skill-creator `SKILL.md:167`「as a sibling to the skill directory」 | 一致 |
| yaml:1648 | `aria/.gitignore:6-7` 注释与规则 | 一致; `git check-ignore` 实测命中 |
| yaml:1648 | 主仓 `.gitignore:36-37`; 先例 `3d3c820` 引入该条 | 一致 |
| tasks.md:89 | 2026-04-10 后触及 ab-results 的 51 个提交零 workspace 路径; 23 个被追踪文件全出自 `2892c6f`; `2a46d08` 零 workspace | 一致 (逐提交复算) |
| revision_log R4-M3 条 | aria `e83be99` (2026-05-13) 引入 `skills/*-workspace/` | 一致 |
| revision_log R4-M3 条 | `AB_TEST_OPERATIONS.md:87` 目录用途表 | 一致 |
| yaml:1817 | `latest.md` 无 History 表、零处 `track-id:` 行 | 一致 (全文实读) |
| yaml:1815 | `71c500e` 改 track 表并在说明段顶部加一段 | 一致 |
| `c25_five_questions` | `phase-c-integrator/SKILL.md:603` / `:612-623` / `:614` / `:625-630` / `:638` | 一致 |
| `c25_five_questions` | `push_all_remotes.sh:103-119`; `config-loader/DEFAULTS.json:6-15` | 一致 |
| hard_constraints 第 4 条 | `state-scanner/SKILL.md:182` | 一致 (触发条件是「本会话持 active claim」, 见 m6) |
| TASK-003 | `run_all_tests.sh:41-46` | 一致 |
| `sc12_liveness.blind_spots` | `spec_complete.py:733-744` | 一致 |
| TASK-021 | `test_pre_merge_gate.py:266` | 一致 |
| TASK-027 第 7 步 | `.aria/state-checks.yaml:29-46` | 一致 |
| 读前必看第 17 条 | `phase-b-developer/SKILL.md:214` | 一致 |
| 读前必看第 19 条 | `phase-c-integrator/SKILL.md:57` / `:754`; `audit-engine/SKILL.md:423` | 一致 |
| TASK-031 issue (2) | `phase-a-planner:246` / `task-planner:123` / `phase-b-developer:255` / `brainstorm:141` | 一致 |
| `aria_shifted` | `CHANGELOG.md:104` / `:200` / `:3136`; aria `VERSION:7` / `:8` | 一致 |
| TASK-029 | `README.md:8/:242`; `README.zh.md:3/:10/:244`; `system-architecture.md:189`; `version-scheme.md:23`; 主仓 `VERSION:24` | 一致 (`CLAUDE.md` 两处已漂到 `:138/:142`, 即前轮 `d931db51`, 不重提) |
| 重写 b | `standards/openspec/project.md:117`; `proposal-minimal.md:28-32` | 一致 |
| tasks.md 多处 | `proposal.md` `:407` / `:453` / `:469` / `:473`; `:409-451` 共 17 个 checkbox; `a563192` 版 sha256 `d3c9b4f2…6f34` | 一致 |
| TASK-001 / TASK-024 | `lib/identity.py:192`; `lib/failure_handlers.py:95` | 一致 |
| TASK-001 / TASK-031 | `phase1_gate.py:1448` `--heartbeat-only`、`:1460` `--include-terminal`; `release_gate.py:251` `--status` | 一致 |

**3. 命令可执行性** (只读或在副本里试跑): TASK-001 基线复核三组共 48 条在真实端点上逐条跑 —— `aria_zero_diff` 27 条 rc 0 空; `aria_shifted` 5 条非空, 另 1 条冒号前不是路径 (m5); standards 8 条与 yaml:163 记录一致 (两条非空, 六条 rc 0 空); `main_repo` 7 条里 `AB_TEST_OPERATIONS.md` 在 `a563192..cf05d8b` 已有 +36/-2 (并发轨 10CG/Aria#211 所致), B.1 会命中「新出现 diff ⇒ 逐处实读」, 属设计内行为, 执行者届时要核 TASK-024 所引「规则 1」「场景 1 第 2/3 步」的位置。`cat-file -e <短 SHA>^{commit}`、`ls-tree | awk '{print $3}'`、E1、`grep -cF` 语法均可执行; `guard_config_hooks` 在仓内输出空 (真阴性), 在仓外 `git grep` 失败时同样空 (已知项 B 的形态属实); SC-13 检索在 aria `1cb3872` 基线命中 4。

**4. git 序列 (5.5-5.8)**: TASK-027/028 v2.4 未改, TASK-029 只改 deliverables 与一句括注, TASK-030 只改 extra。复看: `fetch` 只动远程跟踪 ref, 不覆盖未推的本地分支; 同名 tag 冲突时 git 拒绝 clobber, 该步失败即停 (fail-closed); 新对象断言齐全 (TASK-027 第 5 步 `HEAD≠S3` 且 `HEAD^2=feature`; TASK-028 逐 remote 对合并 SHA 与 tag 对象; TASK-030 `M` 为祖先且 `M^2=feature HEAD`); 「这个值现在该是什么」在 TASK-023 末条、TASK-030 末条、TASK-027 第 6 步都有。无新问题。

**5. 归档门预演**: 复跑 B / C 两态 `gate verdict=warn`、exit 0、`blocking_on_symbol=0`, warn 来源 = 4.4 行「dogfood/benchmark/deploy claim 无可链接产物路径」一条, 与 TASK-031 (yaml:1808) 的预期一致; 当前目录 (副本) 实跑 `complete=False` / `verdict=pass`, 与主控记录一致。warn 下 openspec-archive Step 2 写 proposal.md frontmatter (`SKILL.md:180-196`, 落在归档目录内, 属本轨路径, 无归属后果); Step 7 在 `d_payload != null` 时自动 `forgejo POST` 建 tracker (`SKILL.md:282-287`, `:344`), 复跑 C 态 `d_payload_is_null=False` ⇒ 会触发; 计划以第 11 项在 D.2 之前请 owner 裁 (yaml:213, :1810), **已登记**。

## R4 对账

| 题 | 判定 | 亲验证据 |
|---|---|---|
| **R4-M1** `d7f5b04c` | **closed** | yaml:1193 四要素齐: standards 组先 `fetch`、gitlink 取 `ls-tree` 第三字段、两端点先 `cat-file -e`、零 diff = 退出码 0 且输出为空。实跑: `cat-file -e 21748d4^{commit}` 与 gitlink 均 rc 0, `deadbee` rc 128; 把整行 `160000 commit …<TAB>standards` 喂给 `cat-file` rc 128、喂给 `diff` rc 128 且 stdout 空 —— 新判据拦下。八份 standards 在 `21748d4..940cb5b` 复跑与记录一致。临时仓实测默认 on-demand 递归 fetch 会顺带拉进子模块新 gitlink 对象 (自报 1 属实), 显式 fetch 作为冗余仍必要。残余只有 m5 (清单数据) 与已知项 B (风险段)。 |
| **R4-M2** `8d2e93ff` | **closed** | E1 与 `execution-steps.md:105-108`、`handoff-mechanics.md:97`、`session-handoff.md:218` 逐字一致; 子步骤 1 格式、「不可跳过」、子步骤 2 三行表与 `handoff-mechanics.md:106-124, 135` 一致; 判断清单第 25 条列出 D.1 / D.post / D.2 三路 / D.2b / D.3 子步 1-4 / D.4, 与 `phase-d-closer/SKILL.md:65` 及 `execution-steps.md:28-110` 一一对上; E1 反例「整份文件得 5、head -8 得 1」实跑复现。由此带出的三处更窄的新问题 (m1 / m2 / m3) 单列, 不回算本题。 |
| **R4-M3** `dec4ac57` | **closed** | TASK-030 (yaml:1779) 只剩一个 extra, 与 `commit_attribution` 用法注释 (yaml:673) 一致, 第二个 extra 无定义的问题消失; (b) 裁决所据仓内证据逐条复现 (见抽查表); `check-ignore` 实测 aria 侧工作区被忽略、手册示例路径未被忽略; 「porcelain 出现 `*-workspace/` 行」在两个已追踪 skill 目录下成立 (副本实测)。但裁决选定的 aria 侧落点引出新缺陷 **M1**, 单列 (见其 id 撞键说明)。 |
| **R4-M4** `5891aaeb` | **closed** | yaml:82 八份含 `session-handoff.md`; 求法脚本复跑逐字节一致; 把输入换成 v2.4 快照 `b686185` 复跑, 字面步直接命中 `session-handoff.md`、结果仍为 8 份 —— v2.4 新增文字没有引入集合外的 standards 依赖。 |
| `f5b3afad` | **closed** | `EXCLUDE` 含 `README.zh.md`; 复跑输出「families hit = 10; excluded = 3 (closed list); kept = 7」。 |
| `0f027861` | **closed** | 判据改为语义并配可复跑两步求法, 输出逐字节复现, R4 时「同一求法复跑得 7 与 8」的歧义消除; 第二步「内容是否被依赖」仍是判断, yaml:87 已明写。 |
| `cb1529a3` | **closed** | yaml:163 前句六文件列表与粗体句「上述六个文件」一致; tasks.md:21 同步; 全文计数清扫无残留旧数 (「七个」「七份」只出现在历史 revision_log 条目)。 |
| `f0e78a1e` | **closed** | TASK-029 deliverables 现为九项 (yaml:1745-1753, 无台账); v2.4 revision_log minor 条写明 v2.3 那句不实并勘正; 与 TASK-025 (只列提交文件) 同口径。 |

## Findings

### Critical

无。

### Major

#### M1 `76921ca3` · major · issue · implementation · scope: `detailed-tasks.yaml TASK-024 / TASK-027`

**一句话**: v2.4 为 R4-M3 裁 (b) 时, 把 skill-creator 工作区的首选落点写成 aria `skills/*-workspace/` (称其为「默认落点」), 该处被 aria `.gitignore` 忽略且注释为 kept locally —— 它躲过了 TASK-024 的两层 porcelain 快照比较, 却仍在 SC-13 的 `grep -rn … skills/` 递归检索面上 (`grep -r` 不认 `.gitignore`); TASK-027 第 7 步 (合并树原位回归, 必跑) 与 TASK-025 第 1 条 (上游前进时) 都在 AB **之后**重跑这条检索, 工作区里只要有一份含旧形态串的文件就判红, 而计划的恢复路径不清工作区, 会原地再红。

**证据**:
1. yaml:1648 (TASK-024 快照比较条) 原文: 「工作区放在已被忽略的位置 —— aria 子模块的 skills/*-workspace/ (即 skill-creator SKILL.md 所写「as a sibling to the skill directory」的默认落点; aria/.gitignore 该条注释为 kept locally, …) 或主仓 aria-plugin-benchmarks/ab-workspace/ … —— 两处都不进 porcelain」。全计划提到工作区的只有 TASK-024 第 7 条与 TASK-030 第 2 条, 都没有删除或移出工作区的步骤 (逐条扫描)。
2. yaml:1521 (TASK-018): 「grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' aria/skills/ 零命中」; `proposal.md:469` SC-13 同句 (``grep -rn … skills/` = 0 命中``); yaml:1714 (TASK-027 第 7 步): 「在该工作树跑 … TASK-018 的全部文档机检」; yaml:1672 (TASK-025 第 1 条) 合并后重跑 TASK-018。
3. **三态实测** (本席副本, aria `1cb3872`): 基线 `hits=4` (`phase-a-planner:267` / `phase-b-developer:204,277` / `phase-c-integrator:157`); 把四处改成 5-field 形态模拟组 3 完成 ⇒ `hits=0`; 再放一份 `skills/phase-c-integrator-workspace/iteration-1/eval-2/old_skill/outputs/response.md` (含旧 `:157` 一行) ⇒ `hits=1`, `git check-ignore` 命中 `.gitignore:7:skills/*-workspace/`, aria 与主仓 porcelain 均 0 行 —— 快照比较照过, SC-13 检索误红。
4. **这种内容会出现, 本仓有先例**: `aria-plugin-benchmarks/ab-results/2026-07-31-v1.65.0-122-rule6/skill-snapshot-v1.64.1-SKILL.md:155` 与 `skill-candidate-v1.65.0-SKILL.md:156` —— 正是 phase-c-integrator (本 cycle 第二个照跑套件) 上一次 Rule #6 AB 存下的旧版 / 候选版 SKILL.md, 都含 `audit_report: ".aria/audit-reports/pre_merge-{timestamp}.md"`; 计划自己引的 old_skill 先例 `2026-09-03-v1.69.0-sibling-spec-probe-rule6/PREDICTION.md:4` 把旧版快照放在 `ab-workspace/…/skill-snapshot`; skill-creator `SKILL.md:186` 对「Improving an existing skill」的标准做法就是 `cp -r <skill-path> <workspace>/skill-snapshot/`; 另有 `2026-09-05-v1.70.0-a1-entry-rule6/…/old_skill/outputs/answer.md` 这类 old_skill 输出复述该类路径的先例。
5. 同一暴露面还有 TASK-027 第 7 步与 TASK-029 复跑的 `no-unresolved-version-placeholder` (`.aria/state-checks.yaml:40`, `grep -rn '<vNEXT>' aria/ …`), 同样扫被忽略文件 (本 cycle 触发概率低, 附记)。活性分类器走 `git grep --recurse-submodules` (`spec_complete.py:885`), 不受影响。

**失败场景**: 执行者照 TASK-024 让 skill-creator 用默认落点 (with 臂 skill 目录是 `aria/skills/phase-c-integrator` ⇒ 工作区 `aria/skills/phase-c-integrator-workspace/`), 并按先例存旧版快照, 或 old_skill 臂复述了旧 `:157` → 快照比较过 → TASK-025/026 过 → TASK-027 第 7 步 SC-13 检索命中工作区文件 → 「回归不通过 ⇒ 不打 tag, 不进 TASK-028」, 停在第 6 项 → 按恢复指针 (ec72175) 从 TASK-025 重走, TASK-018 重跑同一检索, 工作区还在, 仍红。只有计划外的一句「删 / 移工作区」能解, 而 Rule #10 不允许执行者自行豁免这条已启用的检查。

**「它怎么会红」三态**: 基线 4 (红, 正确) / 目标 0 (绿, 正确) / 目标 + aria 侧工作区含旧串 ≥1 (红, **误报**)。

**建议修法** (任一): (a) 工作区只允许主仓 `aria-plugin-benchmarks/ab-workspace/` (计划引的 v1.69.0 先例正是此处), 删掉 aria 侧选项; (b) 保留两处, 但 TASK-024 在产物复制进结果目录后删除 aria 侧工作区, 并在 TASK-025 / TASK-027 第 7 步重跑文档机检之前断言 `find aria/skills -maxdepth 1 -name '*-workspace'` 退出 0 且无输出。不建议改 SC-13 检索本身 (那是 proposal 的 SC)。

**id 撞键说明**: scope 若只写 `detailed-tasks.yaml TASK-024`, 按公式得 `dec4ac57`, 与 R4-M3 定稿键相同。本条**不是 R4-M3 重开** (R4-M3 的「第二个 extra 无定义」已闭合, 见 R4 对账), 而是 (b) 裁决引出的新缺陷, 失败面在 TASK-027, 故 scope 如实写两处, 四元组 `implementation:detailed-tasks.yaml TASK-024 / TASK-027:major:issue` ⇒ `76921ca3`。聚合按内容四元组重算时请知悉。

### Minor

#### m1 `05b332ff` · minor · issue · implementation · scope: `detailed-tasks.yaml TASK-031 owner_gates 第 13 项`

**一句话**: 第 13 项是「Phase D 提交双推与 release_gate 协调 ref 推送 (同批)」; TASK-031 要求 release 在「获授权 (第 13 项) 后」执行、未获授权时「记周期 handoff」(即 D.2b 在 D.3 之前, 与 phase-d-closer 顺序一致); v2.4 又要求「latest.md 的改动 … 在 owner_gates 第 13 项的授权请求里单独点明它的 diff」—— 该 diff 在 D.3 子步 3 才产生, 按列出顺序请第 13 项时它还不存在。
**证据**: yaml:1811 (claim 条); yaml:1805 (「D.2b = release_gate … / D.3 = 下方周期 handoff 五条」); yaml:1817; yaml:215 与 tasks.md:115 (「同批」); `phase-d-closer/SKILL.md:65` (D.2 → D.2b → D.3)。
**失败场景**: 照顺序在 D.2b 请第 13 项 (无 latest.md diff 可呈) → 获批「Phase D 提交双推」→ 之后写 handoff、改 latest.md、单独提交 → 末条双推直接推出 → latest.md 改动未经 owner 过目即上远端, 与 v2.4 想落实的判断清单第 28 条「一律请裁」相反。另一走法 (把 release 挪到 D.3 之后再请第 13 项) 与「未获授权 ⇒ 记周期 handoff」冲突 (handoff 已写完)。两条路都要执行者临场改序。
**建议**: 第 13 项拆成两次请求 (13a = D.2b 的协调 ref 推送; 13b = Phase D 提交双推, 请求内附 latest.md diff), 或明写「第 13 项在 D.3 子步 3 之后一次请求, release 挪到授权之后, 结果记台账」。

#### m2 `118d1d64` · minor · issue · documentation · scope: `detailed-tasks.yaml TASK-031 deliverables`

**一句话**: v2.4 让 TASK-031 编辑并单独提交 `docs/handoff/latest.md`, 但 deliverables 四项里没有它; 而 v2.4 对 TASK-029 采用的口径正是「只列本任务提交的文件」(tasks.md:93 第 39 条)。
**证据**: yaml:1796-1800; yaml:1815-1817; tasks.md:93。v2.4 minor 条的自检「用 commit_attribution 自带的 SHARED 集按 deliverables 字面分类」仍是按 deliverables 字段扫路径 —— R4 聚合流程记录第 3(i) 条点名的同一方法盲区 (看不见只活在 verification 散文里的路径, R4-M3 就是这一形态), 这次看不见的是 v2.4 自己新加、按判据恒判 foreign 的那一次共享指针提交。
**失败场景**: 不改变执行动作 (verification 已写清); 但任何按 deliverables 复算提交归属或外向动作面的复核 (含执笔自检) 都会漏掉它。
**建议**: deliverables 补 `docs/handoff/latest.md`, 或在 TASK-031 notes 注明例外。

#### m3 `ac2e8dcb` · minor · issue · implementation · scope: `detailed-tasks.yaml TASK-031 owner-container`

**一句话**: v2.4 要求 `owner-container`「逐字粘贴 handoff_autofill.py --owner-container 的输出 (… 勿手动组装)」, 但没抄 SOT 同段的失败回退; 该命令失败时打印空串、退出 1, 贴进去得 `owner-container: ` 空值, 而计划唯一的核验 E1 只验字段在不在, 照样得 5 —— 与 R4-M1 同族 (命令失败的空输出被当成功)。
**证据**: yaml:1813; `handoff-mechanics.md:92`「best-effort: 命令失败 (空输出/exit 1) 时回退模板手填规则」; `handoff_autofill.py:463-466` (`print(oc if oc is not None else "")`, `return 0 if oc is not None else 1`); 实测: `owner-container` 为空、`track-id` 带容器后缀的样例 frontmatter, `head -8 | grep -cE '^(track-id|owner-container|phase|status|updated-at):'` 得 5。
**失败场景**: identity 解析失败 → 空串 → 贴入 → E1 得 5 通过 → 推出一份 owner-container 为空的周期 handoff (多 track 看板 owner 识别失真)。概率低, 可事后补救。
**建议**: 该条补「退出码非 0 或输出为空 ⇒ 按模板手填规则并记台账」, E1 之外另加值非空检查 (例如同一窗口内 `grep -cE '^(track-id|owner-container|phase|status|updated-at): *[^ ]'` 须 ==5)。

#### m4 `ae4753f5` · minor · risk · documentation · scope: `detailed-tasks.yaml TASK-031 phase-d-closer 映射`

**一句话**: v2.4 把手写 Phase D 做成「phase-d-closer (1cb3872 版) 全部子步的逐一落点」, 并逐字嵌入 E1 命令、History 格式与三行判定表, 但这些 SOT (`phase-d-closer/SKILL.md`、`references/execution-steps.md`、`references/handoff-mechanics.md`、`templates/session-handoff.md`、`handoff_autofill.py`) 不在 TASK-001 的 aria 复核清单里 (`aria_shifted` 第 6 条明写 `phase-d-closer/SKILL.md`「有改动但 proposal 未按行号引用」而不入 diff), TASK-031 也没有执行前比对这些文件的一步; 手写路径不调 skill, SOT 新增的子步不会自动带进来 —— 正是 R4-M2 的失败类, 换成了时间维度。
**证据**: tasks.md:79 (第 25 条); yaml:1805, :1813-1816; yaml:43-77 (aria 复核清单); `git -C aria log --since=2026-06-01 --` 上述五文件共 20 个提交, 其中 `58a61b9` (2026-06-10) 正是新增 D.3 子步 2b (E1) 的那一次 —— R4-M2 发现被手写路径漏掉的子步, 本身就是这样后加进 SOT 的。
**失败场景**: 本轨 5.9 之前 phase-d-closer 再加 / 改一个 D.2b 或 D.3 子步 (近三个半月平均每月约 5 次改动, 本轨 Phase D 还排在 10CG/Aria#195 的 C.2 之后) → 执行者照 v2.4 的冻结映射做 → 新子步静默缺失, 计划内没有任何一步会红。
**建议**: TASK-031 第 2 条之前加「`git -C aria diff --stat 1cb3872 HEAD -- skills/phase-d-closer templates/session-handoff.md skills/session-closer/scripts/handoff_autofill.py` 退出 0 且无输出才沿用第 25 条映射, 否则逐处实读、重做映射并记台账」; 或把这几个文件并入 TASK-001 的 aria 复核清单。

#### m5 `11c3a29f` · minor · issue · implementation · scope: `detailed-tasks.yaml metadata.baseline_rebase.aria_shifted`

**一句话**: `aria_shifted` 第 6 条冒号前是用 ` / ` 连起来的三个文件名, 不是一个路径; TASK-001 要求「对 … aria_shifted 各条冒号前的文件跑 git -C aria diff --shortstat …」, 字面代入得退出 0、输出为空, 在 v2.4 新判据下读成「零 diff」—— 是 v2.4「退出码判据把没比成与零 diff 分开」这一说法的反例 (路径不存在是另一种「没比成」, 退出码照样 0)。
**证据**: yaml:77; yaml:1193; 实测 `git -C aria diff --shortstat 301641b 1cb3872 -- '.claude-plugin/plugin.json / .claude-plugin/marketplace.json / README.md'` → rc 0、stdout 空, 该串在两个端点都不存在; 同清单其余 47 条路径逐条 `cat-file -e <端点>:<路径>` 核过, 均至少在一端存在。
**失败场景**: 执行者照字面记「该条零 diff」, 与 A.2 记录的「版本号有改动」不一致, 而计划只对「新出现 diff」有动作 → 不处理; 这三份是版本号文件、proposal 未按行号引用, 无下游后果, 故 minor。
**建议**: 把第 6 条拆成三条 (冒号前只放一个路径), 并在 TASK-001 判据补一句「路径须至少在一个端点存在 (`git cat-file -e <端点>:<路径>`)」。

#### m6 `9eb8b3c6` · minor · risk · implementation · scope: `detailed-tasks.yaml hard_constraints 第 4 条`

**说明**: 预先存在 (非 v2.4 引入), 本轮有新证据, 前轮未提过 (前轮只在 B.1 入口提过「claim 已被扫」, R1-cr)。
**一句话**: 计划在 B.1 之后不再显式刷心跳, Phase B-D 的 claim 保活全靠「各会话调 /state-scanner 时的入口心跳」; 该入口心跳以「本会话持 active claim」为条件, 新会话未认领时实际不触发, 而 Phase B-D 横跨多次会话与多个 owner 等待点, 超 24h 未刷即被 sweep 成 abandoned; 此后 TASK-031 的 release 按 track 只匹配 active → `claim_not_found` → `released.success` 为假 → 计划判「停在第 15 项」, 且中途他容器看不到本轨占用。
**证据**: yaml:192 (hard_constraints 第 4 条「其入口心跳会推送」); yaml:1189 是全计划唯一显式心跳 (逐条扫描 31 个 TASK 与 metadata); `state-scanner/SKILL.md:182` 触发条件原文; `lib/constants.py:58` `SWEEP_TTL = 86400` 及其注释「a session that stops entering the scanner stops refreshing」; `lib/claim_lifecycle.py:378/:428` `release_claim_by_track` 只匹配 `status == "active"`。新证据: 轨级 handoff「v2.4 返修」主控另记第 4 条实测本容器开工时 claim 心跳已 26.4h; 协调 ref 只读实读 `claims/bfe8285d/s-9762@1447.yaml` (本 spec 带容器后缀的旧认领) 为 `abandoned`; 决策单 §3 第 3 条「两条原 claim 09-10 已 sweep 为 abandoned」。
**失败场景**: B.1 心跳后, 某次等 owner 裁定超过 24h, 期间任一容器跑 `release_gate --sweep-stale` → 本轨 claim 转 abandoned → 后续会话入口心跳得 `claim_not_found` (fail-soft, 只记遥测) → 计划无分支发现 → 他容器可接手本轨 → 到 5.9 release 判红停下。
**建议**: hard_constraints 第 4 条改为「Phase B-D 每个会话入口显式跑 TASK-001 第 4-5 条 (precheck → `--heartbeat-only` → `coord_push_verify`)」, 心跳返回 `claim_not_found` ⇒ 走第 14 项; TASK-031 的 release 遇 `claim_not_found` 记台账并按第 14 项的呈递处理, 不当作推送失败。

## 独立复算 vs 执笔自报的差异

**一致 (我先独立得出, 自述也这么写)**: 四题 Major 的修法机制与落点; R4-M3 的全部仓内证据 (51 / 23 / `2892c6f` / `2a46d08` / `3d3c820` / `e83be99` / skill-creator 原文 / 手册目录表); E1 与 SOT 逐字一致及「5 与 1」反例; 求法脚本与三态证据逐字节可复现; on-demand 递归会顺带拉子模块 (自报 1); `latest.md` 无 History 表、零处 `track-id` 行; `71c500e` 的维护形态; 新增行零禁用字形, 裸 `#N` 只以 `Rule #N` 出现。

**我看到而自述没提的**:
1. **M1** —— R4-M3 条自检只核了提交归属一面 (「参数只剩本次结果目录」) 与仓内证据, 没核「工作区留在 aria/skills 下」对 AB 之后各项递归检查的影响。
2. **m1** —— 「在第 13 项授权请求里点明 latest.md diff」与 D.2b → D.3 顺序、第 13 项「同批」三者的时序冲突。
3. **m2** —— TASK-031 deliverables 未列 latest.md; 自述的按 deliverables 分类自检看不见它 (方法盲区, 与 R4 流程记录第 3(i) 条同型)。
4. **m3** —— owner-container 失败回退缺失, E1 只验存在。
5. **m4** —— 手写 Phase D 照抄 SOT 快照, 执行期不复核。
6. **m5** —— `aria_shifted` 第 6 条不是路径, 在新判据下同样假读「零 diff」。
7. **m6** —— 主控另记第 4 条看到了 claim 跨会话老化, 但没有把它连到计划的保活假设与 TASK-031 release 的判红分支。

**自述声称 vs 产物**:
- 逐条对照 v2.4 五条 revision_log 里写的每一处「改动」与 diff: **全部落地, 未见「声称改了、产物没改」**(v2.3 `f0e78a1e` 那一类)。
- revision_log minor 条「按 deliverables 字面分类 … 与 cannot_catch 的『共两组』一致」: 结论成立 (我复核 TASK-023 / TASK-029 两组), 但方法看不见 v2.4 新加的 latest.md 提交 —— 不是不实, 是覆盖面不足 (m2)。
- revision_log R4-M2 条称 latest.md 两条完成断言「可机械核对」: 子步骤 1 的 `grep -cF <新文件名>` 只有在子步骤 2 更新 pointer **之前**跑才有区分力 (pointer 更新后同样含新文件名); 计划按先 1 后 2 的顺序写, 故成立, 记为观察。
- tasks.md:6 Status 行仍写「— 待主控核验」, 主控已核完 —— 琐碎, 不立 finding。

## 对执笔人自报薄弱点的表态

1. **可接受** —— 我在临时仓复现了默认 on-demand 递归会顺带拉进子模块新对象, 前提确比 R4 原文窄, 但显式 fetch + `cat-file -e` + 退出码三件套不依赖这个前提, 且主控五态反事实显示旧判据还会把真有 diff 读成零 diff, 严重度论证不因此下调。
2. **可接受 (仅就「入不入库」的裁决)** —— 四条仓内证据与 skill-creator 原文我都复现了, 不跑整轮 AB 足以判归属; 但「工作区实际放在哪」的后果没验, aria 侧落点会污染 AB 之后的递归检查, 见 M1。
3. **可接受** —— 实读确认 latest.md 无 History 表、零处 `track-id` 行, `71c500e` 的维护形态与计划描述一致, 落点记台账且有 `grep -cF` 完成断言。
4. **可接受 (做法本身)** —— 单独成提交让 handoff 与归档的路径归属不被共享指针牵连, 也便于 owner 单看 diff; 但它带出第 13 项的时序冲突 (m1), 且其理由依赖 TASK-031 从不调用的 `commit_attribution` (已知项 A)。
5. **可接受** —— 与 TASK-025 及本任务 verification 自洽; 只是同一口径没用到 TASK-031 (m2)。全计划 deliverables 语义本就不一 (如 TASK-013 只列台账却提交脚本与测试), 不另立 finding。
6. **可接受 (作为披露)** —— 本席独立复算没有推翻任何一条 v2.4 返修结论, 出入全部落在「没看到的面」(M1 与六条 minor), 与 R4 同型: 同体自检的盲区在修法带出的新面, 不在修法本身。

## 风险 / 疑问 (不计入 finding)

- **已知项 A (TASK-031 `track-id` 停点不可达)**: 维持风险、不立 finding, 补两条新证据 —— (i) v2.4 新加的 E1 只验存在, 带容器后缀的 `track-id` 与空 `owner-container` 同样得 5 (实测), 补不上这个缺口; (ii) v2.4「latest.md 单独成提交, 使周期 handoff 与归档的归属仍由 track-id 与归档路径判定」这一理由, 同样建立在 TASK-031 从不调用的 `commit_attribution` 上。修法一行: 末条双推之前对 `origin/master..master` 跑 `commit_attribution`, 预期只有 latest.md 那一条为 foreign (已在第 13 项点明), 其余须 own。我倾向执笔请裁第 7 条选「跑」。
- **已知项 B (TASK-027 第 4 步 (b) / `guard_config_hooks`)**: 维持风险。guard: 实测仓外 `git grep` 失败时管道输出同为空, 但计划两处都写明在主仓根跑, 概率低。4(b): A 在 TASK-024 记入台账、隔会话抄回, 抄错时 stdout 空、rc 128、stderr 有 `fatal` 行; 计划写「有输出 ⇒ 停」未限定 stdout, 交互执行下 `fatal` 行多半会被当作输出而停 (fail-closed)。但 v2.4 第 36 条已立「零 diff 须验退出码、另拦 SHA 抄错」的原则, 此处口径不一, 建议顺手补 `cat-file -e <A>^{commit}` 与退出码判据。
- **过程披露**: (i) 派单 Read 一次返回全文 (见已实读文件); (ii) 检索前轮报告时, 一条 grep 的过滤只作用在输出行上, 无意中带出某份 R5 他席报告里的一句话 (涉及已知项 B), 我没有打开任何 R5 他席报告, 上面的判断独立; (iii) 在本席自有副本 `base-copy` 做 porcelain 实验时误删一个已追踪目录, 当场 `git checkout` 复原 (复原后两层 porcelain 0 行); 共享副本与真仓均未触碰, 真仓 `git status` 只多出他席报告。
- 前轮未处置的 minor 未重提 (`9c0dcb27` / `d931db51` / `0dd2d3f2` / `ea958583` 等); `d931db51` 的 `CLAUDE.md` 行号本轮抽查仍漂 (`:138` / `:142`), 按指示不重提。

## Verdict

**PASS_WITH_WARNINGS** —— counts **0C/1M/6m** —— **Vote: REVISE**

## 是否足以开始 Phase B

**不足以** —— 入口门 (owner_gates 第 1 项, 10CG/Aria#195 完成 C.2 或 owner 明示改序) 仍未满足; 计划本身除 M1 外可执行, M1 只在 5.2 之后才会咬人, 其一句话修法 (只用主仓 `ab-workspace/`, 或 AB 后删 aria 侧工作区并加断言) 宜在 owner 放行 B.1 之前、至迟 5.2 之前落地。
