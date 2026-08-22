---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:45:05.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 3
minor_count: 6
---

## 摘要

**#152 的交付面这轮干净了。** 我 R3 的 6 条 Major 里 5 条真闭 (CLI 签名 / 消毒 / 810s / DISPATCH_VIABLE 运行时通道 / .gitignore), 归我席的 6 个簇 closed 5 / partial 1。我对承重项逐条实算复核而非读文本: `write_gate_state` 的 `is_first`/retry 语义下 SC-11(d) 的 `[5,7]` 与 obs 1→2/retry 0→1 **算得出来**; 810s 时间轴逐轮重算成立且 `wait_timeout_seconds=1800` 下确有余量 (`retry_count > max` 那个 `max` 在 `DEFAULT_CONFIG` 里根本不存在, 唯一实际上界就是 elapsed, 既有缺陷不归本 spec); SC-7 的「六个 return 点 / 八个变体」我对着源码逐个数 —— `:419/:429/:436/:465/:490/:513` 六个 return, `:363`/`:376` 与 `:455`/`:458` 各加一变体 = 8, **计数法这轮自洽了**; cluster #8 的 14 个版本引用点我 grep 实核, 逐个对得上。

**残余全部集中在 cluster #1 那台被换掉的机器上, 且三条都是「引了先例/下游但没去源码核它到底怎么成立」** (memory `delegate-verify` / `cite≠apply` 的同一形状, 第三次出现在同一簇):

1. **SC-16 的第三句与 openspec-archive 的成文契约互斥** —— 我实跑三态证明探针本体是好的 (partition 缺 → warn / 只有 `source=test` → warn / 加一条 production → **pass**), 但 `openspec-archive/SKILL.md:234` 逐字写「pass/skipped 两态本身也**不落盘**」。SC-16 同时要 `pass` 又要「归档 frontmatter 留 probe 结果」, 这两半在 pass 分支上不可能同真。
2. **telemetry 分区的根没定, 而探针的根是钉死的** —— 我实测探针把 partition 解析到 **spec 所在仓的根** (从 `/home/dev/Aria` 跑、传 `$TMP` 下的 spec, 它读的是 `$TMP/.aria/…`)。而 `path_coverage.py:17` 逐字要求「调用方须在执行 C.2 合并的仓内运行」⇒ SC-13 若照 TASK-0a 在 **aria-plugin** 跑, 生产记录落 `aria/.aria/`, 主仓探针永远看不见, SC-16 **结构上不可 pass**。
3. **`--source` 默认 production 是 fail-open**, 而「镜像 `coordination-telemetry` anti-spoof 结构」这句对着先例源码不成立 (先例是**两个文件** + 公共 API **没有** source 形参 + 一个专门的 lock 测试文件)。

诚实标注: 我的 Major 数 R2 6(+1C) → R3 6 → **R4 3**, 在降; 且**没有一条落在 #152 本体** (backend / gate / CLI / 时间轴 / 处方), 全在那个**可拆卸的归档探针配件**上 —— 那正是我 R3 建议整段切除、聚合选择「换机制」的那一块。所以最短距离有两条, 都不需要再开五席: 补 3 句话, 或者删掉 `runtime_probe:` 声明只留 SC-13→traps §6 的 tracked 证据 (那一半独立成立)。Vote **REVISE** (按「残余仅 minor」的字面判据), 但见 Verdict 末段的收敛建议。

---

## R3 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| **#1** (liveness 恒红 / 无 source 分区 / 探针跨仓 / .gitignore) | **partial** | **闭的**: 常驻 state-check 已整段切除, 换成 frontmatter `runtime_probe:` 一次性归档门 —— 我实跑 `spec_complete.py --gate` 三态确认声明合规且探针真能红 (见下 M1 证据块); 记录加 `source`/`ts` ✓; `.gitignore` `:19-21` 我实核就是那三条 telemetry 分区 (`coordination-telemetry` / `-nonprod` / `-release`), 位置对 ✓; SC-13 活体证据抄 traps §6 (tracked, 解了「gitignored 分区评审不可见」) ✓; 「恒红」问题随常驻切除而消失 ✓。**未闭的三个接缝** → 新 M1 / M2 / M3 |
| **#2** (CLI 缺 `--name`/`--intervals`, wait≠waiting, 无 gate_error 时解引用, 缺 elapsed_seconds) | **closed** | 签名封闭表逐项对得上被调函数: `--name` 默认 `pre_merge` 匹配 `write_gate_state(*, name)` 必填 keyword-only 与 schema 现值 ✓; `--intervals` 默认 `DEFAULT_INTERVALS_SECONDS` 且明写「调用方传 config `wait_check_intervals`」✓; `wait→waiting` 映射写死 —— 我核 `gate_state_helper.py:141` 的 bump 条件是 `verdict == GATE_STATUS_WAITING and existing.get("status") == GATE_STATUS_WAITING`, 传字面 `"wait"` 确实恒不 bump, 映射是必需的 ✓; 3c' 「两旗标仅 out 含 gate_error 时传」✓; stdout 五键含 `elapsed_seconds` ✓。SC-11(d) 我按 `[5,7]` 逐轮算: 调用1 是 is_first → retry 0 / next=+5 / obs 1; 调用2 name 相同且两侧 waiting → retry 1 / next=+intervals[min(1,1)]=+7 / obs 2 —— **断言里的每个数都对** |
| **#3** (verify_note / gate_error 分支外读取 UnboundLocalError; detail 未消毒) | **closed** | 2.1 伪码 `verify_note = ""` 哨兵在 if 之前 ✓; 2.2 注释明写「`gate_error` 在函数开头初始化为 None (哨兵)」✓; `verify_note = _sanitize_for_json(f" (PR 分支存在性核验失败: {detail})")` —— 消毒挪到了拼接**之前**, 与既有 main 侧 `:456-465`「先拼后 sanitize 再 build」同构 ✓。我 R3-M4 那条「对安全串消毒对危险串不消毒」的倒置已消除 |
| **#4** (210→810 算错; exit 2 continue 只 reset retry_count 致 30s 内双 prompt; 「禁手写 JSON」下 reset 无 CLI) | **closed** | 810 我逐轮重算成立 (t=0/30/90 prompt → continue obs 归 0 retry 留 2 → 210/510/**810** 第二次)。交叉核对 exit 2 的上界: `DEFAULT_CONFIG` 里**没有** `max_retries` 键 (`:57-70` 实读), 所以「`retry_count > max`」是既有 SKILL 的悬空引用, 实际唯一上界 = `elapsed > 1800` ⇒ **810 < 1800, 2.5 不会被 exit 2 吃掉**, spec 的这个论断成立 ✓。`reset --retry-count --observations` 两旗标 ✓, exit 2 continue 两者都归零 ✓ |
| **#5** (`dispatch_viable` 运行时无通道 / 相对路径拼 URL 404 / 2xx-无 run 无布尔映射 / false 时 §4 零消费方) | **closed** | `DISPATCH_VIABLE` 落成 `pre_merge_gate.py` 模块常量, 由 `_no_run_gate_error(path_coverage, threshold)` 读 —— **运行时可达性我复核成立**: pc 由 `gate_check` 一路传进 `compute_verdict`, `dispatchable_workflows` 是 pc 的 additive 键, 常量与函数同模块, 两个输入都在作用域内, 不再依赖「AI 恰好读过 references」✓; basename 钉死 ✓; `dispatch_viable := 600s 内观测到 run` + `queued-unobserved` 证据标 ✓; false 分支的删除面逐项枚举 ✓ (残一处 → m6) |
| **#10** (含我 4 条 minor: verify-failed 象限 / SC-7 计数法 / 包装 timeout 默认 / 新名桩放 mixin / Why 段 ~2/3) | **closed** | 二维消歧表加了「分支存在性未知 (核验失败) 归并此象限, message 带后缀 —— 封闭表成员 + 可选后缀」✓ (我 R3-m2 的两个出路里选了「表改口径」那条, 自洽); SC-7 计数法改「六个早退 return 点 (八个变体)」并列出 `:363`/`:376` 与 `:455`/`:458` 两组变体 —— **我对源码逐个数, 六个 return 与八个变体都对**, 且 `not_applicable` 短路 `:498` 明标「非早退, 由 SC-6 覆盖」✓; 包装保留 `timeout=_LS_REMOTE_TIMEOUT` 默认 ✓; 新名桩进 mixin ✓; Why 段改「15-19 条 (34%-43%, R3 A5 逐簇点算)」✓ (残一处 → m1) |

**统计**: closed 5 / partial 1 / not_addressed 0 (归我席 6 簇)。非我席簇抽查: #6 empty-diff 去分支名 ✓ · #7 骨架创建 + reset/clear exit 2 + SC-11(d) 独立重读 ✓ · #8 14 点我 grep 实核逐个对得上 (见 m3) · #9 catalog 我实读 `version: 1.1.0` + `fixtures` **7** 条, 与 rule6_note 的「7 fixtures」一致 ✓。

---

## 新 Findings

### [A1-R4-M1] Major — SC-16 的两个断言在 `pass` 分支上互斥: openspec-archive 契约逐字写「pass/skipped 两态本身**不落盘**」, 而 SC-16 同时要 `pass` 与「归档 frontmatter 留 probe 结果」

**锚点**: SC-16 (「D.2 归档门对本 spec `runtime_probe:` 声明评估 = `pass` … ; 在 SC-13 之前 = `warn` (探针真能红); **归档 frontmatter 留 probe 结果**」)

**实读下游契约** (`aria/skills/openspec-archive/SKILL.md`, 本轮实读非引用)
- `:180-181` warn_overlay **触发条件** = `gate_result.verdict == "warn"` —— 这是 frontmatter 写入的**唯一**入口 (「真写入 proposal.md frontmatter … 全新字段」)。
- `:228-236` 「runtime_probe 键内容归属条件」逐字: 「是否写入 runtime_probe 键取决于**探针自身** `outcome ∈ {"warn","invalid"}` … 只要探针自身 outcome ∈ {"pass","skipped"}, `runtime_probe` 键依然**不写** … **pass/skipped 两态本身也不落盘** (干净归档零噪音 … pass 观测改由 SC-7 closure 报告/handoff 承载, 声明本身仍随 proposal.md 归档可见)」。
- `:205` 落盘的 outcome 值域逐字标注「`"warn"|"invalid"` (**仅此两态会落到此处**)」。

**实跑佐证** (本轮; 复制 spec 到 tmp repo + 补一个全 done 的 `detailed-tasks.yaml` 以满足评估前置)

| 分区状态 | gate verdict | `runtime_probe` | `unverified_claims` |
|---|---|---|---|
| 缺失 | `warn` | `{outcome: warn, count: 0, reason: "production telemetry partition missing: .aria/gate-state-telemetry.jsonl", symbol: record}` | 1 条 (`claim: "runtime_probe:record"`) |
| 只有 `source=test` 一行 | `warn` | `{outcome: warn, count: 0, reason: "no production-sourced 'record' record found …"}` | 1 条 |
| 再加一行 `source=production` | **`pass`** | `{outcome: pass, count: 1, reason: "1 recent production 'record' record(s) within 14d"}` | **0 条** |

第三行是关键: `pass` ⇒ `unverified_claims` 空 ⇒ `verdict == "pass"` ⇒ **warn_overlay 根本不触发** ⇒ 归档 proposal.md frontmatter 一个字都不写。

**按 v4 实施会怎样错**: 实施者拿 SC-16 去验收, 只有两条路 —— (i) 承认拿不到 frontmatter 证据, 把 SC-16 标绿而它的第三句从未被满足 (paper acceptance, memory `falsifiable_evidence_for_binary_acceptance`); (ii) 认为归档门有 bug, 去改 `openspec-archive` 的落盘条件 —— 那是本 spec 之外的 #95 交付面, scope 爆炸, 且会撞上那条明写的「干净归档零噪音」裁决。两条都不是本 spec 想要的。

**这是 `delegate-verify` 的教科书形状**: spec 写「归档 frontmatter 留 probe 结果」= 把义务移交给 openspec-archive, 但没去它源码核「它真做吗 / 在哪个分支做 / 失败会发红吗」。

**建议** (SC-16 拆成三条, 每条都能答「它怎么会红」):
- **SC-16a** (pass 面, 机读): SC-13 之后跑 `python3 …/spec_complete.py --gate <spec_dir>` → stdout JSON 的 `runtime_probe.outcome == "pass"` 且 `count >= 1`。**证据落 handoff/closure 报告** (契约 `:235` 逐字指定的家), 不是 frontmatter。
- **SC-16b** (红窗, 这才是可落盘可评审的那半): SC-13 **之前** 同一命令 → `outcome == "warn"` 且 `verdict == "warn"` 且 `unverified_claims` 含 `claim == "runtime_probe:record"`; 此时若执行归档, warn_overlay 会把 `outcome/count/ts` **merge-append 进作者的 `runtime_probe:` mapping** (契约 `:213-221`, 「带声明 spec 必然命中」)。
- **SC-16c** (前置可达性, 见 M2): A.2 必须产出 `detailed-tasks.yaml`, 否则探针**零痕迹蒸发** —— 我实跑当前 spec (proposal-only) 的 gate, 输出里**根本没有 `runtime_probe` 键**, `verdict=pass`, 没有任何 warn。这个「静默蒸发」态与「pass」在 verdict 上同形, 必须有一条断言把它们分开。

---

### [A1-R4-M2] Major — telemetry 分区的**根**始终没定, 而探针的根是钉死在 spec 所在仓的; SC-13 又没说在哪个仓跑 —— 照 TASK-0a 的 aria-plugin 跑, 生产记录落到探针看不见的地方, SC-16 结构上不可 pass

**锚点**: frontmatter `partition: .aria/gate-state-telemetry.jsonl` · §3.1 (「telemetry 分区 `.aria/gate-state-telemetry.jsonl`: append-only, `.gitignore` 登记」, 无根定义; CLI 只有 `--state-file`, 无 `--telemetry-file`) · §3.5 TASK-0a (「**aria-plugin** throwaway 分支」) · SC-13 (「throwaway 分支首推 path-matched 变更 → `pre_merge_gate.py --main-branch master --pr-branch <b>`」—— **不指仓**) · §5 `.gitignore` 行

**两个根, 实测都定死了, 但不是同一个**
1. **探针侧 = spec 所在仓的根。** `spec_complete.py:1262-1263` 单点派生 `project_root = _find_project_root(spec_dir)`, 而 `_find_project_root` (`:754-772`) 找 `openspec` 段的上一级。本 spec 在主仓 ⇒ partition 恒解析为 `/home/dev/Aria/.aria/gate-state-telemetry.jsonl`。**实测确证**: 我从 `/home/dev/Aria` 发起命令、把 spec 副本放 `$TMP` 下, 探针读的是 `$TMP/.aria/…` 而不是 cwd 的 —— 根来自 spec 位置, 与 cwd 无关。
2. **生产者侧 = 被合并那个仓的工作树。** `path_coverage.py:17` 逐字: 「仓根 = 本进程 cwd 的 `git rev-parse --show-toplevel`; **调用方须在执行 C.2 合并的**[仓内运行]」; `_verify_main_branch_exists` 的 `git ls-remote` 也不带 `cwd=` (继承进程 cwd)。所以要复现 #152 (aria-plugin 的 paths 过滤 workflow), `pre_merge_gate.py` 必须**在 aria-plugin 工作树里**跑。

**冲突**: `gate_state_helper.py` 现有约定是 cwd 相对 (`load_state(path=".aria/workflow-state.json")`, `:66`), CLI 的 `--state-file .aria/workflow-state.json` 也是相对。于是 SC-13 在 aria-plugin 里跑 ⇒ telemetry 落 `/home/dev/Aria/aria/.aria/gate-state-telemetry.jsonl` ⇒ **主仓探针永远 count=0 ⇒ SC-16 恒 warn**。附带两个实核后果: (a) `aria/.aria/` **目前不存在** (`ls` 确认), 会被凭空创建; (b) 插件 `.gitignore` 只有 `**/.aria/cache/`, **不覆盖**这个文件, 而主仓 `.gitignore` 的 `.aria/gate-state-telemetry.jsonl` 带斜杠 ⇒ 锚定在主仓根, 管不到子模块内 ⇒ 子模块里多一个 untracked 文件 (state-scanner submodule drift 会报, 且有被误提交的口)。

**两实施者必然分叉且无 SC 能区分**: 实施者甲读 TASK-0a「aria-plugin throwaway 分支」, 把 SC-13 也放 aria-plugin ⇒ SC-16 恒红; 实施者乙注意到主仓自己也有 paths 过滤 workflow (`/home/dev/Aria/.forgejo/workflows/issue-triage-tests.yml`, 我实核存在) ⇒ 在主仓跑 ⇒ SC-16 pass。SC-13 的文字对两者都成立。

**建议** (两句话):
- SC-13 明写「活体在**主仓 Aria** 跑 (主仓 `.forgejo/workflows/issue-triage-tests.yml` 同样带 paths 过滤, 足以复现 #152 形态), 使 telemetry 落 `/home/dev/Aria/.aria/`, 与本 spec frontmatter `partition` 的解析根一致」。TASK-0a 留在 aria-plugin 无妨 —— 它不写 telemetry。
- §3.1 明写 telemetry 路径的派生规则 = **`--state-file` 的同目录**同级 (`Path(state_file).parent / "gate-state-telemetry.jsonl"`), 而非 cwd。理由不只是根一致: SC-11(d) 断言「telemetry **两行**」, cwd 相对时单测会往真实仓分区里追加、跨次运行累积 ⇒ 那条断言天然 flaky; 派生自 `--state-file` 则单测在 tmpdir 里天然隔离。先例也是这么做的 —— `phase1_gate.py:950-953` `_telemetry_path(repo, source)` 收一个**显式的 `repo: Path`**, 从不用 cwd。
- 顺带在 §5 那行标明是**主仓** `.gitignore` (现在夹在一串插件路径中间, 读者会猜错仓)。

---

### [A1-R4-M3] Major — `--source` 默认 `production` 是 fail-open 的分区默认值; 且「镜像 `coordination-telemetry` anti-spoof 结构」这句对着先例源码不成立 (先例是两个**文件** + 公共 API **没有** source 形参 + 一个专职 lock 测试)

**锚点**: §3.1 (「`[--source production|test]` (**默认 production**)」/「单测一律 `--source test` (探针只计 `source == production`, **镜像 `coordination-telemetry` anti-spoof 结构**)」)

**实读先例** (本轮实读)
- `phase1_gate.py:950-953`: `def _telemetry_path(repo, source)` → docstring 逐字「Return the **source-partitioned** telemetry file (**structural, not spoofable**)」; 实现是**选文件**: `_PROD_TELEMETRY_FILE if source == _PRODUCTION_SOURCE else _NONPROD_TELEMETRY_FILE` —— 主仓 `.gitignore:19` 与 `:20` 那两条正是这一对。
- `:972` 记录里的 `"source": source or "library"` 注释逐字「structural partition tag (**non-spoofable default**)」—— 缺省值是**非特权**的 `library`, 不是 `production`。
- 特权值只能从私有 `_gated(_source="production")` 到达; 公共 `run_gate` **没有** source 形参, `run_gate_synthetic` 强制 harness; `tests/test_phase1_gate_telemetry.py` 整个文件就是锁这条 (「anti-spoof lock」), 而它是上一轮审计判 Major 才补出来的。

**v4 与之的差**: 一个文件 + 一个**公共 CLI 旗标**, 且缺省落在**特权值**上。三处不同, 每处都在削 anti-spoof:

| 维度 | 先例 | v4 | 后果 |
|---|---|---|---|
| 分区载体 | 两个文件 (结构选择) | 一个文件 + 记录内字段 | 尚可 (探针按字段过滤) |
| 特权值可达性 | 只有私有入口 | **任何 CLI 调用者** | 纪律代替结构 |
| 缺省方向 | 非特权 (`library`) | **特权 (`production`)** | **fail-OPEN** |
| 机械锁 | 专职 lock 测试文件 | 无 | 忘了旗标不会发红 |

**按 v4 实施会怎样错**: 将来任何一条新单测 (或一次手工 smoke) 忘了 `--source test`, 就往生产分区写一条 production 记录 ⇒ 探针 pass ⇒ 「CLI 真被生产调用」这个信号变成假绿。而这个信号**正是** cluster #1 (以及它上游的 R2-C1「helper 运行时零消费方」) 唯一要产出的东西。memory `invariant_needs_failclosed_default` (「枚举分区必须 fail-CLOSED, 正向枚举对新值天然 fail-OPEN」) + `false_green_dual_is_permanent_red`。

**建议** (三选一, 一句话; 我推荐第一条):
- (a) **缺省翻向非特权**: `--source` 默认 `test`; 只有 workflow-runner SKILL 里那条运行时接线命令显式带 `--source production`, 并在 SKILL 该行旁注明「这是探针唯一的合法生产入口」。忘了 → 探针 warn (fail-closed, 零信息但不撒谎)。
- (b) **照抄先例的两文件**: 生产 `.aria/gate-state-telemetry.jsonl` / 非生产 `.aria/gate-state-telemetry-nonprod.jsonl` (两条都进 `.gitignore`), 并加一条 SC「不带 `--source production` 的任何 CLI 调用都不得写生产文件」的**拒绝能力**断言 (memory `adversarial-fixture`: 验断言要验它拒绝坏实现, 不是验当前取值)。
- (c) 最省: 保留现签名, 但加一条 SC 锁死「测试套件内全部 CLI 调用均带 `--source test`」的机械断言 (grep 式)。

**给 owner 的诚实标注**: 三条 Major 里这条是**唯一可降 minor 的** —— 采纳 (c) 一行 SC 即可, 其余两条 (M1/M2) 必须改文本。把它列 Major 是因为「fail-open」在本轮 Major 判据里逐字在列, 且「镜像 anti-spoof 结构」这句会误导实施者以为结构保证已经存在。

---

### 次要 (minor)

- **[A1-R4-m1]** §2.1 标题仍写「PR 分支存在性消歧作为**第八个早退**」, 但 SC-7 按 R3 #10 勘正后的计数法是「**六个** early-return 点 (八个变体)」⇒ 新增那个是**第七个 return 点 / 第九个变体**。「第八」是 v3 旧计数法的残留。跨条款标号矛盾 (memory `fixes_contradict_each_other_across_clusters`: 逐条吸收后要做条款间交叉检查), 无行为影响, 但读者按「第八」去数会找不到位置。
- **[A1-R4-m2]** `<pr_branch>` 占位符的理由只成立一半。「compute_verdict 不知道分支名」为真, 但 **`gate_check` 知道** —— 而且 §2.1 伪码**已经**在对 `out["gate_error"]["message"]` 做事后 `+=` (verify_note)。既然事后改写这条路本 spec 自己在用, 就该顺手把 `<pr_branch>` 也填掉, 只把 `{o}/{r}` 留给 AI (那个 gate 确实不知道)。另: `{o}` / `{r}` 这对花括号在会被 `.format()`/f-string 二次处理的消费方手里是雷, 建议改 `<owner>/<repo>` 与 message 里其它占位符统一成尖括号。
- **[A1-R4-m3]** 「主仓侧 **14 点**」后面跟的清单实际列了 **15 项** (`CLAUDE.md:139` `:141` / `VERSION:24` / `README.md:8` `:242` / i18n 9 / **gitlink**)。我 grep 实核: 版本**字符串**点恰好 14 个 (逐个对得上, 内容判定完全正确 ✓), gitlink 不是字符串点。所以数字没错、断句有歧义 —— 改成「主仓侧 14 个版本字符串点 + gitlink」即可。这条本身是 cluster #8 的收尾, 不影响实施。
- **[A1-R4-m4]** 「exit 2」在 §3.2 里同时指 **CLI 退出码 2** 和 **exit condition 2 (timeout prompt)**, 3d 那句「CLI exit 2 → surface 错误并按 exit 2 user prompt 处理」两个词义各出现一次。更实际的问题是这条恢复路径的循环性: exit condition 2 的 `continue` 动作**本身就是**一次 CLI 调用 (`reset --retry-count --observations`), 而 `reset` 在 state 文件缺失时也 exit 2 (§3.1 逐字) ⇒ 「CLI 坏了」的处方是「再调一次 CLI」。建议改写为「CLI **退出码** 2 → surface stderr 并触发 exit condition 2 的 user prompt; 若随后的 `reset` 亦退 2 → **abort** (不得回退手写 JSON)」, 把终止分支写死。
- **[A1-R4-m5]** `no_run_observations` 定义为「本 **episode** 内连续…」, 但 spec 从头到尾没定义 episode 边界, 而 2.5 的 `abort` 又明写「保留 gate_state」。我追到 `workflow-state-schema.md` 才确认边界是安全的 —— `:316` 「`session.status` 是 `failed` … 可被下一个 workflow **覆盖**」+ 并发检测算法「`completed` 或 `failed` → Proceed, **overwrite allowed**」⇒ 下一个 workflow 整体重写 state 文件 ⇒ `is_first=True` ⇒ obs 归 1 ✓。**结论是对的, 但读者得跑到另一个仓的另一份 schema 才能确认**。建议 §3.1 补半句「episode 边界 = workflow-state 文件生命周期 (schema §3.3: failed/completed 允许被下一个 workflow 覆盖); 2.5 abort 保留 gate_state 只作 audit trail, 不会被下一次 wait 继承」。
- **[A1-R4-m6]** §3.5 说条件 scope「**只此一处**」, 紧接着枚举了 §4 整段 + SC-8 + SC-9 部分 + Impact/CHANGELOG —— 自相矛盾的措辞 (实际枚举是完整的, 所以只是措辞)。**真正漏的一处**: `dispatch_viable=false` 时 §4 删掉 ⇒ `dispatchable_workflows` 不存在 ⇒ 2.3 的渲染条件整句消失 ⇒ `DISPATCH_VIABLE` 常量**自己**成了零消费方, 但 Impact「新 artifact」仍无条件列着它。这正是本簇要治的「有记录无路由」在自己的 false 分支上复现 (memory `fix_recurs_in_its_own_fallback_path`)。补半句「false ⇒ 常量亦不引入」即可。

---

## Verdict

**verdict: PASS_WITH_WARNINGS · vote: REVISE** (critical 0 / major 3 / minor 6)

**#152 本体我判可以进 A.2。** backend 单行改 + 第八个早退 + compute_verdict 插入点 + CLI 签名 + 810s 时间轴 + DISPATCH_VIABLE 运行时通道 + 版本引用点 —— 这一轮我全部按源码复算而不是读文本, 没有一条留着 Major。R1/R2/R3 反复复发的三个点 (时间轴 off-by-N / 插入点 / CLI 承重参数) 这轮同时钉住了。

**三条 Major 全在同一个可拆卸配件上**: cluster #1 用 `runtime_probe:` 归档门换掉常驻 liveness —— 方向对 (我实跑证明探针本体三态都对、红窗真实、anti-spoof 在探针那一侧确实生效), 但**换机制时只接了声明面, 三个接缝各自没去源码核**: 向上游生产者的路径根 (M2) / anti-spoof 的缺省方向 (M3) / 向下游归档写盘的契约 (M1)。同一形状第三次出现在同一簇, 值得记一句: **「镜像先例」这个动作本身需要一份逐项对照表**, 否则每轮都会漏掉先例里承重的那一半。

**最短距离两条 (请一并上呈 owner, 我推荐 ①)**

1. **删 `runtime_probe:` 声明, 只留 SC-13 → traps §6 的 tracked 活体证据** (= 我 R3 的建议 (a))。一次删除同时消掉 M1+M2+M3+R-f, 且不损失任何东西 —— traps §6 那半本来就独立成立、可评审、跨容器可见 (探针那半反而受制于 gitignored 分区的容器本地性: 若 D.2 在另一个容器/工作副本执行, 分区不存在 ⇒ 恒 warn, 而本 spec 认领行明写 `self_multi_container` 在场)。代价: 放弃「首个采用者」这个附加价值。
2. **保留声明 + 补 3 处文字**: SC-16 拆三条 (M1 建议) · SC-13 钉死在主仓跑 + telemetry 路径派生自 `--state-file` (M2 建议) · `--source` 缺省翻 `test` 或加一条 grep 式 SC (M3 建议 (a) 或 (c))。预计 diff < 15 行, 不动任何设计。

**关于收敛**: 我的 Major 数 R2 6(+1C) → R3 6 → R4 3, **在降**, 且本轮零条落在 #152 本体 —— 按 memory `stop_adding_rounds_when_major_count_flattens` 的判据 (「加轮判据是 major 数是否还在降」) 这不是不收敛, 是收敛中。但按 R4「PASS = 残余仅 minor」的字面判据我只能投 REVISE。**建议主控/owner 不要再开第五席轮**: 上述两条路径都不需要新的审计视角, 落 ① 是一次删除、落 ② 是三处已经写好的替换文本; 落完由**单席**复核 SC-16/SC-13/§3.1 那三处 (或 owner 直批) 即可 —— 同一批眼睛对同一台机器的边际产出已经明显转负 (memory `marginal-return-negative`)。
