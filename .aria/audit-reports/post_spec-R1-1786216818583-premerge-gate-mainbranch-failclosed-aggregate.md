---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T19:20:18.583Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R1 汇总 — premerge-gate-mainbranch-failclosed

> 本文件是 **audit-engine 编排层的汇总**, 非某个席位的报告。五份席位原始报告见同目录 `post_spec-R1-*-{role}.md`。

## 配置解析 (Rule #10 留痕)

| 项 | 值 | 来源 |
|---|---|---|
| audit.enabled | true | `.aria/config.json` |
| checkpoints.post_spec | `convergence` | config 显式 (非 adaptive 推导) |
| max_rounds | 4 | config |
| 席位 | 5 (tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager) | `audit.teams.post_spec` |
| max_parallel_agents | 2 | agent-team-audit 默认 (config 未覆盖) |
| drift-checker | **未启用** | `audit.drift_guard` 配置块不存在 ⇒ `convergence_mode` 默认 false。**非 AI 裁量** |
| file-scope 二次过滤 | 不降级 | `scope_skip_paths` 未配置; 且 convergence 已是底 |
| #26 前序完整性 gate | 不适用 | checkpoint ≠ pre_merge |
| #27 change_id 锚点 | 通过 | `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` 存在 |

**本轮无任何席位被跳过、无降级、无改序。** 5/5 席位全部返回, 零 spawn 失败、零超时 ⇒ `incomplete: false`。

## Anchor (Step 0, 固化于 R1 启动前)

- **primary_goal**: 把 Rule #8 pre-merge gate 的『main 分支无 in-flight CI run』这条腿从 fail-OPEN 改为 fail-CLOSED —— 去掉 pre_merge_gate.py 两处指向 'main' 的缺省 (:300 签名 / :427 CLI), 未显式传参时从 remote HEAD 解析真值且解析失败即 abort, 并在查 in-flight 前独立核验该分支在目标 remote 上存在。
- **source_sha**: `98ad1f5` | **anchor_source**: `proposal_why_goal`
- drift-checker 未启用 ⇒ 本轮不计算 `drift_ratio` (`drift_check_skipped: true`)。anchor 仍固化留档供后续轮次使用。

## 投票与 verdict

| 席位 | VOTE | VERDICT | 原始 finding 数 |
|---|---|---|---|
| tech-lead | REVISE | FAIL | 2C + 6M + 3m = 11 |
| backend-architect | REVISE | FAIL | 2C + 3M + 1m = 6 |
| code-reviewer | REVISE | FAIL | 3C + 5M + 4m = 12 |
| qa-engineer | REVISE | FAIL | 1C + 5M + 4m = 10 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0C + 3M + 2m = 5 |

- **unanimous_pass**: false (5/5 REVISE)
- **conclusions_stable**: 不适用 (R1 无前序轮)
- **converged: false**
- **聚合 verdict: FAIL** (≥1 Critical)

## 去重后结论集 (comparison_key = {type, severity, category, scope})

原始 44 条 → 按 `{category, scope}` 去重、severity 取最高 → **21 条** (5 Critical + 10 Major + 6 Minor)。
`finding_id = sha256(category:scope:severity:type)[:8]`, 供 R2 做机械四元组比较。

### Critical (5)

| ID | key | type | category | scope | 席位 | summary |
|---|---|---|---|---|---|---|
| `ed5ffb63` | C1 | issue | architecture | phase-c-integrator verdict 枚举 + workflow-runner 消费侧 | 2席 (CO/QA) | verdict 新增第四态 error, 但 gate_state_helper 只有 WAITING/GREEN/FAIL 三常量且 :147 原样写入无校验; 消费侧无 catch-all ⇒ gate 层 fail-CLOSED 而 fail-OPEN 从下游复发 |
| `3c5a1695` | C2 | issue | documentation | aria/skills/phase-c-integrator/SKILL.md:167,243 | 3席 (TE/CO/QA) | Spec 唯一 SKILL.md 改动落在 :242 (含 path_coverage 契约句), 而 (b) 腿自己的指令行 :243 硬编码 `--branch main` 且标注无条件执行, 连同 :167 均不在枚举内 ⇒ 按 Spec 实施会改错行并留下真正的 main 字面 |
| `696e87f5` | C3 | issue | testing | aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py | 4席 (TE/BA/CO/QA) | §Impact「既有用例逐字不改」证伪: 24/24 gate_check 调用点零显式传 main_branch, test_sc12 硬断言 'main' 必红; 且新增 symbolic-ref/ls-remote 无打桩接缝会真发网络 |
| `b279d170` | C4 | issue | architecture | aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:354-366 (main_branch 双消费者) | 4席 (TE/BA/CO/QA) | main_branch 同时喂给 evaluate_path_coverage(更早消费)与 in-flight 查询; 「只治(b)腿/不动 path_coverage/无行为面扩大」三处声称与代码矛盾; 解析插入时序未钉死, None 流入会拼出非法 rev-range |
| `3a464e42` | C5 | issue | architecture | proposal.md §2/§3 的 <remote> 占位符 + gate_check 签名 | 4席 (TE/BA/CO/QA) | <remote> 全篇未绑定为参数/config/决策/SC, 代码库 gate_check 与 CLI 均无该参数; 本仓 origin(Forgejo)/github 双 remote 且 HEAD symref 状态不同, 取谁决定 green vs error |

### Major (10)

| ID | key | type | category | scope | 席位 | summary |
|---|---|---|---|---|---|---|
| `93ff2b40` | M1 | issue | implementation | proposal.md §3/SC-6 ls-remote 重试与超时参数 | 4席 (TE/BA/CO/QA) | 重试次数/退避/超时完全未定, 仓内已并存三套口径(aether RETRY_BACKOFF 5/15/45 · primitive_call_timeout 30s · path_coverage _GIT_TIMEOUT 15); 两实施者必得不同结果, 且单测可能真耗 60s+ |
| `a78f3121` | M2 | issue | documentation | SKILL.md:264-279 Output schema + workflow-runner gate_state 持久化 | 4席 (TE/BA/CO/KN) | main_branch_resolved 在哪些输出分支在场未定, 撞 #122 成文的「早退分支保持六键不变」契约与 _OLD_KEYS 守护测试; workflow-runner 侧 schema 亦无该字段位置, wait 轮询会静默丢弃 ⇒ D5 在最需要的早退绿上落空 |
| `09ca9745` | M3 | risk | architecture | aria/skills/phase-d-closer/scripts/fetch_gate.py:108-128 (+ state-scanner sync.py) | 2席 (TE/CO) | 同 plugin 内已有两份默认分支解析器, 其一第三级兜底逐字是 ('master','main') 字面回落 = D2 明令禁止的那件事; Spec 未提, Phase B 照抄即精确复活要治的恒绿; 同类 fail-OPEN 兄弟位置未处置 |
| `2017a421` | M4 | decision | documentation | proposal.md §Rule #6 rule6_note (Rule #6 判据适用) | 2席 (TE/KN) | 把全部 hunk 归入判据表第一行 substitute; 但存在专属 AB 套件 phase-c-integrator-pre-merge-gate.json(v1.1.0/7 fixtures), 且 SKILL.md:243 是处方性运行时指令行 ⇒ 应落第二行「照跑 AB, 零裁量」。援引的 db2e983 裁定明文限定不适用; v1.65.0(#122) 同类先例结论相反 |
| `e960755e` | M5 | risk | architecture | pre_merge_gate.py:328 解析/核验的插入位置 vs 早退分支 | 1席 (TE) | 置于 enabled=false / no_ci_fallback / skip_with_warning 早退之前, 会把 owner 关闭的闸门与既有降级变 error(违反 §非目标第 5 条); 置于 path_coverage 之后则 (a) 腿钉死 unknown。Spec 未规定 |
| `8377173a` | M6 | issue | implementation | proposal.md §3/D4/SC-4 vs SC-6 的判别信号 | 1席 (BA) | 「分支不存在」(SC-4) 与「查询失败」(SC-6) 的区分信号未钉死(实测 exit 2 vs 128 可区分但 Spec 未言明); 网络不可达时 ls-remote 实测挂起且无内建超时 |
| `6f421741` | M7 | risk | documentation | proposal.md:50,86 承重引用容器本地 memory | 1席 (KN) | 两个核心决策(D1/D2)的承重依据是容器本地 memory 名; 同日新写的 feedback_memory_store_is_container_local_not_shared 明确警告不要这样做, 本 Spec 未做该文件建议的任一缓解 |
| `707d3e4d` | M8 | risk | documentation | proposal.md:168-169 ship target vs 并发姊妹 Spec 版本 SOT | 1席 (KN) | v1.65.6 PATCH 与并发的 linked-issue-normalization(目标 v1.66.0 MINOR)共享同一版本 SOT 且未声明落地顺序; 对方先落地则 v1.65.6 成不可执行的非单调版本号 |
| `9598079c` | M9 | risk | testing | proposal.md SC-1 (CLI 路径可测性) | 1席 (QA) | main() 内联构建 parser 无可独立调用的工厂; SC-1「CLI 不传」若不经 main()/argv 端到端验证(111 既有用例从未有此形态), 有 collapse 成浅层 argparse-default 断言的风险 |
| `b23662a2` | M10 | risk | testing | proposal.md SC-3/SC-7 (负控的新增依赖) | 1席 (QA) | 存在性核验对显式传参路径同样生效 ⇒ 负控 SC-3/SC-7 在修复后隐含新增一次 ls-remote 调用; 未言明 mock 需求会致负控打真网络或伪红(负控伪红= 零信息量) |

### Minor (6)

| ID | key | type | category | scope | 席位 | summary |
|---|---|---|---|---|---|---|
| `0e6d9748` | m1 | issue | documentation | proposal.md SC-2 函数名 | 2席 (CO/QA) | SC-2 点名 run_gate(...), 该函数在 phase-c-integrator 不存在(真实为 gate_check@:298); run_gate 实为 state-scanner/phase1_gate.py 的函数 ⇒ 自称唯一覆盖内部调用路径的 SC 指向了另一个 skill |
| `635acec6` | m2 | issue | documentation | pre_merge_gate.py:21 模块 docstring | 1席 (TE) | docstring 仍写 [--main-branch main], 是同文件第三处 main 字面; §Impact 只列「两处缺省」 |
| `b9a9130f` | m3 | issue | documentation | path_coverage.py:19 模块 docstring | 1席 (TE) | 携带与 SKILL.md:242 同义的契约句, 落地后同样陈旧, 不在 Impact 枚举内 |
| `bb02d5ff` | m4 | issue | documentation | aria-plugin issue #137 body (外部记录) | 2席 (CO/KN) | 订正只存在于 comment(id 18015), body 首段仍逐字保留被推翻的「两条腿都失败为绿」; proposal:58「正文已同批评论订正」字面成立但易误导只读 body 者 |
| `3e2a58c1` | m5 | issue | architecture | ci_backends/base.py:29 not_found 槽位 | 1席 (CO) | backend 契约已有 not_found 枚举槽(SKILL.md:279 逐字承认 gate 目前不产生), D3 论证存在性核验放 gate 层时未与之对话, 该枚举将继续是死值 |
| `d9535094` | m6 | risk | architecture | proposal.md §2/D2/SC-5 refs/remotes/<remote>/HEAD 可用性 | 1席 (CO) | 该 ref 只在 clone/set-head 时写, fetch 不更新; Layer 2 容器脚本化 checkout 可能无此 ref ⇒ D2 在健康常态下 abort = 恒红对偶。建议 ls-remote --symref 取权威值, 本地 symbolic-ref 作快路径 |

## severity 跨席位冲突 (6 条, 去重时取最高)

去重算法规定「相同 {category, scope} → 合并 found_by, 取最高 severity」。以下 6 条各席位判定不一致, 已按规则归一 —— **这是规则动作, 不是收敛**:

| ID | key | 各席位判定 | 归一为 |
|---|---|---|---|
| `3c5a1695` | C2 | critical / critical / minor | **critical** |
| `696e87f5` | C3 | major / critical / critical / major | **critical** |
| `b279d170` | C4 | critical / major / major / minor | **critical** |
| `3a464e42` | C5 | major / critical / major / major | **critical** |
| `93ff2b40` | M1 | minor / major / major / major | **major** |
| `a78f3121` | M2 | major / minor / major / minor | **major** |

> ⚠️ **对 R2 的影响**: severity 属 comparison_key 的一部分。若 R2 各席位对同一问题给出不同的 severity 组合, 四元组会变化并显示为「结论不稳定」, 而实际可能只是措辞/判定口径漂移。R2 判定收敛时必须先看**归一后**的 key 集合。

## 编排层独立复核 (5 条)

编排层对承重断言做了独立复跑, 不全盘采信席位结论:

| 断言 | 复核方法 | 结果 |
|---|---|---|
| 存在专属 AB 套件 | `ls aria-plugin-benchmarks/ab-suite/` + 读 JSON | ✅ `phase-c-integrator-pre-merge-gate.json` v1.1.0, **7 fixtures** |
| `SKILL.md:243` 硬编码 `--branch main` | `sed -n '243p'` | ✅ 逐字命中, 且标注「无条件执行」 |
| 24 处 `gate_check` 调用零传 `main_branch` | 配对括号解析全部调用点 | ✅ **24/24, 0 显式传参** (backend-architect 报 23, 少 1) |
| `run_gate` 不在 phase-c-integrator | `grep -rn '^def .*gate'` | ✅ 真实为 `gate_check@:298`; `run_gate` 属 `state-scanner/phase1_gate.py` |
| verdict 消费侧封闭三态 | 读 `gate_state_helper.py:28-40,:147` | ✅ 仅 WAITING/GREEN/FAIL 三常量, `:147` 原样写入无校验 |

**一条被编排层否决未纳入**: qa-engineer 提「111 tests 是三文件汇总非单文件」(minor)。编排层复核 46+25+40=111 ✅ —— **Spec 原文表述准确**, 该提醒针对的是派发任务书的旁注措辞, 非 Spec 缺陷, 故不计入结论集。

**一条席位间事实分歧**: qa-engineer 称 `run_gate`「仅存在于子模块回滚检测 bash 测试中」, 与编排层实测 (`state-scanner/scripts/phase1_gate.py` 内的真实 Python 函数) 不符。两席对结论 (SC-2 点名的函数不在本 skill) 一致, 编排层采信实测。

## 超出本 Spec 修复范围的项 (需 owner 裁定)

- **M4 (Rule #6 判据适用)** —— 涉及 CLAUDE.md 规则 #6 与规则 #10。Spec 自评 substitute; 两席 + 编排层实测指向「照跑 AB」。**AI 不得自行改判**, 上报。
- **M8 (版本非单调)** —— 与并发姊妹 Spec 的落地顺序是排期决定。
- **M7 (memory 承重引用可移植性)** —— CLAUDE.md / 成文规范引 memory 名是 owner 领地的已知未决问题。
- **m4 (#137 body 未编辑)** —— 需在 issue 上操作, 属外向动作。

## 轮次记录

| 轮 | 席位 | vote | 去重 C+M+m | converged |
|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | 5C + 10M + 6m = 21 | false |

**下一步**: 未收敛且有余量 (R1/4)。按流程应 R1-fix → R2。R1-fix 的范围与 owner 裁定项见上节。
