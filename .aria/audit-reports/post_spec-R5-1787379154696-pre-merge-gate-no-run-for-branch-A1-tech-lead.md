---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T09:32:45.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 1
minor_count: 6
---

## 摘要

**我 R4 的三条 Major 有两条真闭, 第三条 (簇 #1 telemetry 根) 的 fix 修好了根的派生, 却把 SC-13 钉到了一个**结构上产生不了 #152 形态**的仓。** 这轮我没有读文本, 全部实跑/实测: 探针三态跑通 (warn/warn/pass, 见 #3 证据块)、主仓三个 workflow 的 `on:` 块逐个 parse + `_workflow_covers` 逐组合枚举、`git ls-files aria` 证明子模块挂载点下不可能有超级仓文件。

结论一句话: **簇 #2 / #3 closed 且我能复现它们的红窗与绿窗; 簇 #1 partial —— 派生规则对了 (telemetry 根 = `dirname(--state-file)` 恰等于探针解析根), 但由它带出的 SC-13「主仓根执行」这句与主仓真实 workflow 拓扑冲突: 主仓两个带 paths 过滤的 workflow, paths 全部指向 submodule 挂载点 (`aria/skills/issue-triage/**` · `aria-orchestrator/docker/aria-runner/**`), 而超级仓树里根本不可能有这两个前缀下的文件 (`git ls-files aria` = 1 条 gitlink)。⇒ SC-13 自己写的「path-matched 变更」在主仓不可达, `workflow-trigger-matched` 档取不到, 只能退到 `workflow-files-changed` 档, 而那一档 `dispatchable_workflows` 恒 `[]` (设计限制) + 处方 (b) 指向的 paths 同样落在子模块里 ⇒ 两条处方双双是死路。**

讽刺的是修法已经在 v5 手里了: 既然 telemetry 已经从 `--state-file` 派生, gate 就**不必**跟 state 文件同仓 —— gate 照旧在 aria-plugin 跑 (那里 `skills/issue-triage/**` 是真文件、push 无 branches 白名单、第二次 push 能真触发 ⇒ 处方 (b) 可验), CLI 传**绝对路径**的主仓 state 文件即可。v5 却在派生 fix 之外又加了一道「主仓根执行」的同仓约束, 等于用旧假设 (必须同仓) 去配新机制 —— 而且**SC-13 因此从不检验那条 fix 的承重命题**「gate cwd 与 state 文件位置是两回事」。这是 memory `fixes_contradict_each_other_across_clusters` 的形状: 两个 fix 各自对, 后一个违反了前一个的隐含前提。

Major 数 R2 6(+1C) → R3 6 → R4 3 → **R5 1**, 仍在降; 且这一条依旧不在 #152 本体 (backend / gate / CLI / 时间轴 / 处方文案), 而在活体验收的**场地选择**上。修法是 SC-13 一句话, 不动任何设计。Vote **REVISE** (按「残余仅 minor」的字面判据), 但见 Verdict: 我不建议再开第五席轮。

---

## R4 处置核对

| 簇# | 来源 | 状态 | 证据 (本轮实测) |
|---|---|---|---|
| **#1** | A1-R4-M2 telemetry 分区根未定 | **partial** | **闭的一半**: §3.1 路径改为 `<dirname(state-file)>/gate-state-telemetry.jsonl`。我实跑确认这与探针解析根**恰好对齐** —— 探针 `spec_complete.py:1263 → _find_project_root(spec_dir)` 把 `partition` 解析到 **spec 所在仓根** (主仓), 而主仓 state 文件 `.aria/workflow-state.json` 的 dirname 就是主仓 `.aria/` ⇒ 同一个文件 ✓。派生还顺手治了 SC-11(d)「telemetry 两行」的 flaky (单测 state 文件在 tmpdir ⇒ 分区天然隔离, 结构上碰不到真实仓分区) ✓。§5 那行已标明是**主仓** `.gitignore`, 我核 `:19-21` 正是既有三条 telemetry 分区 ✓。SC-13 加了「主仓 `.aria/workflow-state.json`」「**主仓** `.aria/gate-state-telemetry.jsonl`」双断言 ✓。**未闭的一半**: 「主仓根执行」这句与主仓 workflow 拓扑冲突 → **M1**; 「workflow-runner 恒传主仓 state 文件」这个不变量只写在散文里, CLI 默认是 cwd 相对 → **m5** |
| **#2** | A1-R4-M3 `--source` 特权缺省 | **closed** | §3.1 逐字「**`--source` 无缺省, 必填** (`production\|test`; 缺失 → exit 2)」+ 签名行 `--source {production\|test}` (必填) + SC-11(d)「**缺 `--source` exit 2**」三处一致 ✓。§3.2 两条 CLI 行都带 `--source production`, 步骤 2 经「同 3c' 全旗标」继承 ✓。比我 R4 建议的 (a)/(c) 还强一档: 分区路径派生自 `--state-file` 之后, 单测**结构上**够不着真实分区 —— 就算某条单测忘带 `--source test` 写成 production, 它也只会污染自己的 tmpdir。fail-open 的缺省与「纪律代替结构」两个批评点同时消解 ✓ |
| **#3** | A1-R4-M1 SC-16 与归档契约互斥 | **closed** | SC-16 拆三条, 三条我逐条实跑复现 (证据块见下)。(a) 前置可达 — 我在源码里定位到那个早退: `spec_complete.py` tasks.md 缺席分支下, **仅当** `detailed-tasks.yaml` 在场才 `_fold_probe_and_build_payload(...)`, 否则逐字注释「两文件皆缺 (proposal-only) → 维持 v1.54.0 designed 零评估早退」⇒ 「A.2 产出 detailed-tasks.yaml」确是硬前置 ✓。(b)(c) 见下表, **`runtime_probe` 键在 `--gate` stdout JSON 里始终在场 (pass 态也在)**, 所以「机读 gate JSON, 不依赖 frontmatter 落盘」这句成立 ✓ —— 我 R4 M1 指控的那半 (「归档 frontmatter 留 probe 结果」) 已从 SC 里删干净 ✓。附带: (b) 的红窗**真能红**且能被 (c) 的绿窗区分, 「静默蒸发」态 (无 yaml) 与 pass 态也能被 (b) 区分 (蒸发时压根没有 `runtime_probe` 键 ⇒ (b) 必红) —— 三条互为红窗, 自洽 ✓ |
| **#6** | 我的 6 条 minor | **partial (4 closed / 2 partial)** | **m1 (第八个早退) partial** → §2.1 已改「**第七个**早退 return 点 (现六点八变体之外新增一点)」✓, 但 §2.3 还留着「既有**七个**早退落点键集逐字不变」→ 新 **m1**。**m2 (`<pr_branch>` 回填 + 尖括号) partial** → 回填已落进 §2.1 末段伪码 ✓, 但 2.3 表里的 dispatch 模板仍写 `{o}/{r}` 而同一格文字说「占位用尖括号」→ 新 **m2**; 且回填这个新行为零 SC 覆盖 → 新 **m3**。**m3 (14 点断句) closed** → 「主仓侧 **14 个版本字符串点 + gitlink**」✓。**m4 (exit 2 双义 + 恢复路径循环) closed** → 3d 改成「CLI **退出码** 2 → surface 错误 → 直接 abort (终止分支; 不再调 reset — reset 同样会退 2)」, 比我建议的更硬, 终止分支写死 ✓。**m5 (episode 边界) closed** → §3.1 表内补了「= 一个 `gate_state` 生命期: `is_first` 创建 → green/fail/abort 终态; 终态 state 可被下一 workflow 覆盖 = 新 episode, schema §3.3」; 我核 `workflow-state-schema.md` §3.3 = `:308-319` Cleanup 段, 我 R4 引的 `:316` 正在其内 ⇒ 引用准确 ✓。**m6 (false ⇒ 常量亦不引入) closed** → §3.5 删除面加了「`DISPATCH_VIABLE` 常量本身」+「不留零消费方字段/常量」+「Impact/CHANGELOG 相应不提」✓ |

**统计 (归我席 4 簇)**: closed 2 / partial 2 / not_addressed 0。

### #3 证据块 — 探针三态实跑 (spec 副本 + 全 done `detailed-tasks.yaml`, 命令 `python3 aria/skills/state-scanner/scripts/lib/spec_complete.py --gate <spec_dir>`)

| 分区状态 | `verdict` | `runtime_probe` | `unverified_claims` |
|---|---|---|---|
| 缺失 (SC-13 之前的真实态) | **warn** | `{outcome: warn, count: 0, reason: "production telemetry partition missing: .aria/gate-state-telemetry.jsonl", symbol: record}` | 1 条 `{claim: "runtime_probe:record", reason: <同左, **含 partition 路径字面**>, symbols: ["record"]}` |
| 只有 `source=test` 一行 | **warn** | `{outcome: warn, count: 0, reason: "no production-sourced 'record' record found …"}` | 1 条 (claim 同上) |
| 再加一行 `source=production` | **pass** | `{outcome: pass, count: 1, reason: "1 recent production 'record' record(s) within 14d"}` | **0 条**, `d_payload: null` |

⇒ SC-16(b)「`unverified_claims` 含本 partition 条目」在**分区缺失**这一实际红窗态下逐字成立 (reason 字面就带 partition 路径); SC-16(c) 的 `outcome == "pass"` 从 stdout JSON 直读 ✓。

---

## 新 Findings

### [A1-R5-M1] Major — SC-13 被钉到主仓根, 但主仓**结构上产生不了** `workflow-trigger-matched` × 零 run: 两个 paths 过滤 workflow 的 paths 全指向 submodule 挂载点; 退而求其次的 `workflow-files-changed` 档下两条处方双双是死路

**锚点**: SC-13 (「throwaway 分支首推 **path-matched** 变更 → … 经 workflow-runner 路径 (**主仓根**执行, state 文件 = 主仓 `.aria/workflow-state.json`) … 处置后轮询至非 `not_found` 或 600s」) · §3.5 TASK-0a (「**aria-plugin** throwaway 分支」) · §2.3 表 trigger-matched 档与 `workflow-files-changed` 档 · §3.3 处方 (a)(b)

**实测 (本轮, 全部可复跑)**

1. 主仓 workflow 清单与触发面 (`_find_workflow_files('.')` + `_parse_workflow` 实跑):

| workflow | 自动触发 paths | 可被主仓树变更命中? |
|---|---|---|
| `.forgejo/workflows/issue-triage-tests.yml` | push/pull_request `['aria/skills/issue-triage/**']` (push 另有 `branches: [master, feature/aria-issue-triage-sop]` 白名单) | **否** |
| `.forgejo/workflows/build-aria-runner.yaml` | push `['aria-orchestrator/docker/aria-runner/**']` (branches 白名单 `[feature/aria-2.0-m0-prerequisite]`, 无 pull_request) | **否** |
| `.forgejo/workflows/submodule-gate-tripwire.yml` | 仅 `workflow_dispatch` | 不适用 |

2. **为什么「否」**: `aria` 与 `aria-orchestrator` 都是 submodule 挂载点 —— `git ls-files aria` 返回**恰好 1 条** (`aria` 这个 gitlink 本身), 超级仓索引里不可能存在 `aria/skills/...` 前缀的文件; 一次 gitlink bump 的 `git diff --name-only` 输出实测就是裸 `aria` (查 `dfae7e5`)。

3. `_workflow_covers` 逐组合枚举 (实跑, 12 组):

| changed_files | issue-triage-tests | build-aria-runner | tripwire |
|---|---|---|---|
| `['aria']` (gitlink bump) | False | False | False |
| `['docs/foo.md']` | False | False | False |
| `['aria/skills/issue-triage/x.py']` (**主仓树内不可构造**) | True | False | False |
| `['.forgejo/workflows/issue-triage-tests.yml']` | False | False | False |

⇒ 主仓 throwaway 分支的可达终态只有两个: 普通变更 → 规则 8 `not_applicable` (短路放行, **根本进不到 `not_found` 分支**); 改 `.forgejo/workflows/**` → 规则 3 `covered` / `workflow-files-changed`。

**按 v5 实施会怎样错**

- 实施者照 SC-13 字面去主仓造「path-matched 变更」, 会先撞上「这个 paths 前缀在超级仓里写不进去」这堵墙, 然后**必须临场改设定**, 而 spec 没给方向。三条岔路各自有代价:
  - (i) 改 `.forgejo/workflows/**` 走 `workflow-files-changed` 档 —— gate 侧的核心断言 (`not_found` / kind / obs 计数 / telemetry / 第 3 次 prompt) 都还成立, 但**处方两条全死**: (a) 该档 `dispatchable_workflows` 恒 `[]` 是**明写的设计限制** ⇒ 不渲染 dispatch 行; (b) 「被改 workflow 自己声明的 paths」= `aria/skills/issue-triage/**` ⇒ 又回到子模块里, 推不出去。SC-13 的「处置后轮询至非 `not_found`」只能挂到 600s。活体验收里唯一验「处方真能解锁 CI」的那条腿蒸发。
  - (ii) 按 TASK-0a 的先例跑去 **aria-plugin** (那里 `skills/issue-triage/**` 是真文件、push 无 branches 白名单、第二次 push 是普通 diff ⇒ 处方 (b) 可验) —— 但若沿用相对 `--state-file`, telemetry 落 `aria/.aria/`, SC-16(c) 恒 warn。**这个岔路会被 SC-16(c) 抓住** (诚实标注: 所以不是「无 SC 能区分」的纯形态), 代价是在 D.2 前才发现并返工。
  - (iii) 造一个删掉 gitlink、在 `aria/skills/issue-triage/` 下放真文件的 throwaway 分支 —— 能凑出 trigger-matched, 但这是破坏性构造, spec 从未授权。
- 更要命的是**证据质量**: SC-13 的产出要「抄进 traps §6」当仓内 SOT。走 (i) 得到的记录是「主仓 workflow-files-changed × 零 run」, 而 traps §6 的标题是 #152 (新分支首推 × paths 过滤) 的实证 —— 形态不同却同栏登记, 是往经验 SOT 里塞一条错标签的事实 (memory `cross_doc_claim_verify_at_target` 的反向: 这次是**写进**目标文档的东西本身失真)。

**为什么这是 v5 新引入的**: v4 的 SC-13 不指仓 (那正是我 R4-M2 的第一条指控)。v5 为了让 telemetry 落到探针看得见的根, 同时做了两件事 —— **(A)** 把分区路径从 cwd 改为 `dirname(--state-file)` 派生, **(B)** 把 SC-13 钉到主仓根。**(A) 一做完, (B) 就不再必要**: 派生之后 gate 的 cwd 与 state 文件位置已经解耦 (§3.1 自己逐字这么写)。(B) 是拿旧假设 (必须同仓) 去配新机制, 结果把活体验收搬到了一个产生不了目标场景的仓。而且——**SC-13 因此从不检验 (A) 的承重命题**: 现在 gate 与 state 文件同在主仓, 「后者从不随子模块走」这句在活体里根本没被拉扯过。memory `fixes_contradict_each_other_across_clusters` + `verify_predicate_inputs_exist` (判定机制的输入到底能不能被生成)。

**建议 (一句话, 不动设计)**: SC-13 改为「gate 在 **aria-plugin** 工作树内跑 (`cd aria`; 满足 `path_coverage.py:17` 的 cwd 契约, 且**只有**该仓能构造 `workflow-trigger-matched` × 零 run: `skills/issue-triage/**` 是真文件、push 无 branches 白名单), CLI record 传**绝对路径** `--state-file /home/dev/Aria/.aria/workflow-state.json` ⇒ telemetry 落主仓分区 ⇒ SC-16(c) 可 pass。**这一步同时是 §3.1『gate cwd 与 state 文件位置两回事』的活体证明**」。附带把「删分支」保留、把 600s 兜底保留。若 owner 更愿意留在主仓, 那就把 SC-13 明写为 `workflow-files-changed` 档并**删掉**「处置后轮询至非 `not_found`」这条腿 (诚实交付一半, memory `mechanization_knob_must_match_granularity`), 同时在 traps §6 标明形态差异 —— 但那样就少验一条处方腿, 我不推荐。

---

### 次要 (minor) — 「还能挑」, 单独或全部不改都不阻塞 A.2

- **[A1-R5-m1]** (m1 未闭的残片) §2.3 第 2 个 bullet 仍写「既有**七个**早退落点键集逐字不变 (SC-7)」, 而 §2.1 已改「第七个早退 return 点 (现**六**点八变体之外新增一点)」、SC-7 也逐字「**六个**早退 return 点 (八个变体)」。三处口径两套。我对源码复核过 SC-7 的枚举本体是对的 (`:418/:428/:434/:454/:489/:512` 引的是各早退的**守卫行**, 对应 return 在 `:419/:429/:436/:465/:490/:513`; `:363`/`:376`、`:455`/`:458` 两组变体也对), 所以只是 §2.3 那个「七」没跟上。典型 `fix_the_class_not_the_instance`: R4 改了 §2.1 一处, 同一句式的兄弟位置漏了。
- **[A1-R5-m2]** (m2 未闭的残片) 2.3 表 trigger-matched 档: 命令模板逐字仍是 `forgejo POST /repos/**{o}/{r}**/actions/workflows/<basename(file)>/dispatches`, 而同一格的括注说「占位用**尖括号**, 避免 `.format()` 花括号雷」。文字与它自己给的模板互斥, 实施者照模板抄就把花括号留在 message 里。改 `<owner>/<repo>` 即可 (payload 里 `-d '{"ref":"<pr_branch>"}'` 的花括号是 JSON 本体, 另说, 但值得在括注里点一句以免被一并「修掉」)。
- **[A1-R5-m3]** `<pr_branch>` 事后回填 (§2.1 末段, 本轮新增的行为) **零 SC 覆盖**: SC-2 走 `compute_verdict` 直调 (message 里必然还留着占位符, 它的 dispatch 子项也只断言 `workflows/x.yml/dispatches` 子串), SC-5 只断言「六键俱在 / 档位对」, SC-10 只断言「核验失败」子串 —— 没有一条断言端到端 message **不含**字面 `<pr_branch>`。实施者跳过 `.replace(...)` 全绿。与 A2-R4-M1 (`DISPATCH_VIABLE`/basename 零覆盖) 是同一形状, 那次补了 SC-2 子项, 这次的新行为没补。一句话修: SC-5(a) 加「message 不含 `<pr_branch>` 字面且含实际分支名」。后果轻 (人多填一个占位符), 故 minor。
- **[A1-R5-m4]** `reset --retry-count` 的语义两处轻微张力: §3.1 写「`reset [--observations] [--retry-count]` (至少一个旗标; **只动指定字段**)」, 而 §3.2 exit condition 2 写「`reset --retry-count` **同时置 `started_at=now`**」, SC-11(d) 又逐字断言「`reset --retry-count` 后 `started_at` 更新」。SC 是权威且钉死了行为, 所以不会分叉; 但「只动指定字段」这句话现在不准确。建议 §3.1 改「只动指定字段 (`--retry-count` 连带 `started_at`, 二者是同一计时语义的两半)」。
- **[A1-R5-m5]** 「workflow-runner **恒传**主仓 `.aria/workflow-state.json`」这个不变量只活在散文里, 没有落到默认值或命令行: `gate_state_helper.py` 现有 API 是 `load_state(path=".aria/workflow-state.json")` / `atomic_write_state(..., path=".aria/workflow-state.json")` —— **cwd 相对**; §3.2 的 3c' 与步骤 2 两条 CLI 行**都没写 `--state-file`**。而 C.2.4 gate 按 `path_coverage.py:17` 必须在被合并仓 (子模块) 的树内跑, 于是同一轮里两条命令的合理 cwd 不同。若 record 恰在子模块 cwd 下执行, R3 #7 补的「state 文件不存在时**先创建骨架**」会把这个错误从「报错」变成「**静默**另起一份 state + 另一个 telemetry 分区」(且插件 `.gitignore` 只有 `**/.aria/cache/`, 那个文件会以 untracked 身份留在子模块里)。memory `invariant_needs_failclosed_default`: 不变量写进文档 ≠ 写进兜底默认值。一句话修: 3c'/步骤 2 显式带 `--state-file <项目根绝对路径>/.aria/workflow-state.json`, 并在 §3.1 注明「CLI 默认相对 cwd, 子模块 cwd 下会静默分叉, 故运行时接线一律传绝对路径」。(与 M1 的建议是同一根线, 一起改成本更低。)
- **[A1-R5-m6]** 2.3 trigger-matched 档把「零 run」的成因封闭成两种 (#152 新分支首推 × paths 过滤 / run 未被领), 漏了第三种**结构性**成因: **workflow 的 `branches:` 白名单不含本分支**。`path_coverage.py` 只建模 `paths` (`AUTO_TRIGGER_KEYS` + `_extract_paths`), 对 `branches:` 完全不感知 —— 我实跑 `_parse_workflow` 主仓 `issue-triage-tests.yml`, 输出 `triggers` 只有 key/paths 两字段, branches 白名单 `[master, feature/aria-issue-triage-sop]` 被整段丢弃。诚实标注影响面: **今天的生产流程不受影响** —— C.2.3 先建 PR, 而两仓那个 paths 过滤 workflow 的 `pull_request` 触发都**没有** branches 过滤 ⇒ PR 在场就会建 run; 真正会撞上的是「push-only 无 PR」场景 (恰好就是 SC-13 自己)。但 message 是**给人读的诊断**, 而本 spec 的立项理由逐字是「带着**准确诊断**交人」; 断言一个在某些拓扑下为假的成因, 是把 #152 的误诊风险搬了个家。一句话修: 该档 message 追加「或 workflow 的 `branches:` 过滤不含本分支 (覆盖评估不建模 branches)」, 处方 (b) 相应限定「若因 branches 过滤, 推 commit 无效, 改用 (a) 或改 workflow」。

---

## Verdict

**verdict: PASS_WITH_WARNINGS · vote: REVISE** (critical 0 / major 1 / minor 6)

**#152 本体连续两轮我判可以进 A.2, 这轮没有任何新账落在它身上。** backend 单行 / 第七个早退 / compute_verdict 插入点 / CLI 签名与 `--source` / 810s 时间轴 / `DISPATCH_VIABLE` 与 basename 守卫 / 版本引用点 —— R4 我按源码复算过一遍, R5 抽查的部分 (SC-7 六点八变体的行号、schema `:123`/`:125`、`.gitignore:19-21`、runtime-probe-declaration 预言句位置、workflow-state-schema §3.3) 逐个对得上。簇 #2 与 #3 我能同时复现红窗和绿窗, 判 closed 有底。

**唯一的 Major 是「活体验收放错了仓」, 不是设计问题, 也不是 #152 本体。** 而且它是 R4 那条 fix 的副产品: 派生规则 (A) 一落地, 「主仓根执行」(B) 就成了多余的约束, 却没人回头删 —— 结果 (B) 把 SC-13 搬到一个 `workflow-trigger-matched` 结构上不可达的仓, 顺手让 (A) 的承重命题失去活体检验。这是我这轮唯一想请主控/owner 看一眼的东西, 因为它**恰好落在 R5 被要求盯的那个接缝上** (簇 #1 与 `path_coverage.py:17` cwd 契约的关系), 而前四轮 5 席 × 4 = 20 份报告里「branches」出现 **0 次**、主仓 workflow 拓扑从未被任何一席实读过 (我 grep 核过)。memory `stop_adding_rounds_when_major_count_flattens` 的另一半正是这个: **换新鲜眼睛 > 加轮** —— 这次的新鲜眼睛不是新席位, 是「去读那个仓真实的 workflow 文件」这个动作。

**收敛建议 (与我 R4 一致, 不改口径)**: 我的 Major 数 6(+1C) → 6 → 3 → **1**, 每轮都在降, 且本轮 fix 引入的 major 占比 = 1/1 —— 按 `marginal_return_negative` 的判据 (「本轮 fix 引入的 major 占比 > 1/2 即到拐点」) 这个数字**已经到拐点**了, 意思是: 再开一轮五席的产出预期主要还是「上一轮 fix 的副作用」, 不是新缺陷。所以我的建议是 **不要开 R6 五席轮**:

1. 落 M1 的一句话 (SC-13 改 aria-plugin 跑 + 绝对 `--state-file`) + m5 同一根线的一句话, 顺手把 m1/m2/m4 三处措辞对齐 (m3/m6 各加一行断言/一个分句, 可选);
2. 由**单席** (我或任一席) 只复核 SC-13 / §3.1 那两处替换文本, 或 owner 直批进 A.2;
3. m3/m6 若不改, 请在 tasks 里留 `rule6_note` 之外的一条实施注记, 别让它们在 B.2 现场变成临场判断 (Rule #10 的边)。

如果主控判定「活体验收场地写错、实施者到现场会自己发现并适配」达不到 Major 门槛 (这个判定我认为是合理的 —— SC-16(c) 确实能兜住最坏那条岔路), 那么把 M1 降为 minor, 我的票即为 **PASS**, v5 可直接进 A.2。我把这个降级条件写明, 是为了不让「一条一句话可修的窄项」独自消耗掉 owner 加的第二轮配额。
