---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T11:17:04.285Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/13M/24m
counts_dedup: 0C/10M/20m
sibling_probe: no_sibling_found
---

# post_planning R1 聚合 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v1.1 `97c3515`)

> **对象**: tasks.md (31 项 checkbox) + detailed-tasks.yaml (31 TASK), 主仓本地提交 `97c3515` (未推送)。执笔人 = 新派 tech-lead 实例 (不是主控); v1.1 = 主控核验返修 (心跳授权口径 + 等待点第 14 项)。
> **Sibling probe (本轮入口)**: 本轮已完整扫描, 未发现同 issue 竞品 (`status=ok`, `verdict=no_sibling_found`; origin 162 份 / github 156 份 proposal, 无 cap; own_keys = `aria#199`, `aria-plugin#161`)。
> **drift-checker**: convergence 模式未 opt-in (`audit.drift_guard` 未配置) ⇒ 跳过, `drift_check_skipped: true`。
> **并发**: 默认 2 席滑动窗口 (tech-lead + backend-architect → qa-engineer → code-reviewer → knowledge-manager)。五席均只写了自己的报告 (主控每席完成后跑不带路径的 `git status --porcelain` 核验), 协调 ref 全程 `be2ba7e` 未变。
> **五席共识 (不计 finding)**: 三态实跑证据由 3 席独立复跑, 与 yaml 嵌入**逐字节一致** (tech-lead / code-reviewer 执行嵌入脚本; qa-engineer 自行重写 N1/N2 算法对基线得同值); 被引行号 35 处抽查 33 处一致 (2 处不一致见 m5 / m12); 16 个版本点、27 个零 diff 触点、SC-13 基线计数、测试基线计数 (104 / 148 / 1605) 均复现; SC-15(5) 按裁定 1 重算正确 (backend-architect 独立推导); 读前必看第 7、8 条的钉定取值五席一致判「可接受」。

## drift_metrics (Step 0 anchor 快照)

- checkpoint: post_planning
- primary_goal: 把 Approved 的 10CG/Aria#199 proposal 分解为可执行的 Level 3 双层任务, 忠实落地决策单 2026-09-12 §2 的 #199 表 13 行 (连同 §5) 与 Level 3 三处连带重写
- in_scope: 任务分解与粒度 / 依赖与执行序 / agent 分配 / 验收判据可证伪性 / 裁定与重写的执行口径 / 基线复核 / 外向动作与 owner 等待点 / 发布段
- out_of_scope_hints: proposal 设计取舍本身 (post_spec 已由 owner 裁定接受); 13 条裁定本身
- source_sha: 97c3515
- drift_ratio: null (未 opt-in)

## 判定

| 席 | verdict (按计数重算) | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/8M/8m | REVISE | 中间任务转绿恒红; DAG 并行与 TASK-013 断言冲突; AB 判据口径不一且真仓无事前防护; 协调 ref 整条推送 / 对齐波及他轨; 主仓 PR 无提交范围核验; AB 树与合并树脱节 |
| backend-architect | PASS | 0C/0M/2m | PASS | 组 2 对 §1.0–§1.4 忠实; 同文件串行; config 引用逐字属实; SC-15(5) 重算正确 |
| qa-engineer | PASS | 0C/0M/2m | PASS | SC 映射逐条一致; RED / 反事实 / 三处重写可执行且有区分力 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/5M/11m | REVISE | 发版期间 feature 未并入 origin/master 致冲突恢复不收敛; 第 14 项未授权分支自相矛盾; §5 第 2 条漏列; CRLF 无保护; SC-13 逐字相等抽取未钉 |
| knowledge-manager | **PASS** (报告 frontmatter 误标 PASS_WITH_WARNINGS, 其正文计数 0M, 按 verdict 规则重算) | 0C/0M/1m | PASS | 同步面、16 版本点、两张映射表、13 条裁定、读前必看抽核均属实; 新增同形改写缺机检 |

**合并判定: PASS_WITH_WARNINGS (0 Critical / 10 Major 簇) · Vote REVISE 2 / PASS 3 · 未收敛 (R1)。**

## Major 簇 (去重后 10) 与处置 (v2 rework)

| 编号 | 簇 | 席位 (报告内编号) | 处置 |
|---|---|---|---|
| PP1-M1 | 组 2 中间任务 (TASK-008~011) 的「转绿」清单点名的 SC 方法含依赖后序 P 阶段 (尤其 P6) 的断言, 在该任务完成时结构上恒红; missing→bypassed 放在 P5 任务却要求转绿依赖 P6 的 SC-9 / SC-15(5) | TL M1 · BA m1 (SC-7(e) 归属同根) | **接受**: 中间任务只验收「本段可独立断言的子格」并逐格点名, 其余红属预期; SC 级全绿统一在 TASK-012; missing 的豁免降级移到 TASK-012; SC-7(e) 归属改到格 D 所在任务 |
| PP1-M2 | 组 3 (TASK-014~017) 只依赖 TASK-008, DAG 允许与 2.2–2.6 并行, 与 TASK-013「不带路径 porcelain 为空」冲突, 且无合法下一步 | TL M2 | **接受**: 串行化 (组 3 依赖 TASK-013), 与决策单 Q3「单执行席串行」一致; tasks.md 组序与 DAG 对齐 |
| PP1-M3 | `delta.pass_rate` 处置在 TASK-024 与 owner_gates 第 5 项之间口径不一, 聚合范围未定义; 按套件算 phase-c-integrator 健康态即触发 (恒红) | TL M3 | **接受**: 照跑套件只判「逐 eval 无回归」; `delta > 0` 只对 audit-engine 套件 (含定向 eval 3) 要求; owner_gates 5 / tasks.md 表 / PREDICTION.md 逐套件同步 |
| PP1-M4 | 裁定 11 的连带清单漏了 proposal §5 第 2 条 (`:378`, 排他豁免列表不含 `no_spec_unverifiable`), TASK-025 会把自相矛盾的迁移文案写进 CHANGELOG, 无检查拦截 | TL M4 · CR M3 | **接受 (修类)**: 读前必看第 7 条补 §5 第 2 条; 对 proposal 全文检索「降为」「不被豁免」「豁免」列出完整连带清单; TASK-025 写明第 2 条同步 |
| PP1-M5 | TASK-024 在真仓无沙箱跑题面为「执行」口吻的 phase-c-integrator.json (eval 1 提交 / eval 3 主动推送), 只有事后快照, `ARIA_COORDINATION_NO_PUSH` 不挡 `git push`, 快照面不全 | TL M5 (+ CR 风险 1) | **接受**: 两套件按 descriptive 形态下发 (AB 手册 `:170` 规则 1), 执行器提示逐字禁止 git 写命令与 forgejo 写接口; 快照面补三个子模块两端 `ls-remote`、`ls-remote --tags` 与 PR 列表; 改 remote pushurl 属配置改动, 若采用须列为 owner 等待点 |
| PP1-M6 | 协调 ref 上的「整条 ref」操作 (免授权心跳推送、AB 后强制对齐) 只考虑了本轨写入: 心跳会替他轨 / 本轨未授权的本地写入发布, 强制对齐会抹掉它们; 第 14 项未授权分支要求心跳加 `--no-push`, 而 state-scanner 入口心跳加不上 | TL M6 · CR M2 | **接受**: 每次心跳前与强制对齐前比较本地与 `ls-remote` 的协调 ref, 本地领先时列出领先提交涉及的 claim 文件; 含任何非「本轨已授权心跳」的写入 ⇒ 心跳加 `--no-push` / 不对齐, 停下请授权; 第 14 项未授权分支改为「不重认领, 停在 B.1 等授权」(CR M2 修法 1) |
| PP1-M7 | 主仓分支起点可能回落为本地 master, 而 TASK-030 只核工作树不核 `origin/master..HEAD`, 他轨 / 其他会话的未推提交会随 PR 合入; owner 授权时看不到提交清单 | TL M7 (+ CR m10 同面) | **接受**: TASK-001 回落时与 TASK-030 开 PR 前各记录 `git log --oneline origin/master..<ref>` 并逐条标归属, 有非本轨提交即停; 清单随授权请求一起呈给 owner |
| PP1-M8 | aria feature 分支在 Phase B (97–143h) 期间从不并入 `origin/master`; 期间 aria 发版 (09-12/13 两天三版) ⇒ TASK-027 第 5 步在版本文件上冲突, 字面恢复「从第 1 步重走」不收敛; 且 AB 实测树与最终合并树之间无一致性约束, 取号恢复路径不重跑 AB | TL M8 · CR M1 | **接受**: TASK-025 取号前 `git -C aria merge origin/master` 进 feature (不 rebase), 冲突即停, 合并后重跑 TASK-021; TASK-024 开跑前断言 `origin/master` 是 feature 的祖先; 合并前若 `git diff <AB 时 SHA>..origin/master -- skills/audit-engine skills/phase-c-integrator` 非空则重跑 TASK-024; 冲突恢复指针统一为 ec72175 先例; 判断清单第 19 条把「Phase B 期间 aria 已发版」移出罕见路径 |
| PP1-M9 | `phase-b-developer/SKILL.md` 与 `phase-c-integrator/SKILL.md` 是 CRLF (1070/1096 行), 计划无行尾保护或机检; 整文件行尾改写可被 SC-13 与 porcelain 断言放过 | CR M4 | **接受**: TASK-016 / 017 编辑前后 `git ls-files --eol` 仍为 `i/crlf w/crlf`, `git diff --numstat` 删除行数等于被替换行数; TASK-018 纳入机检; 对 CRLF 文件做 frontmatter 断言前先 `tr -d '\r'` |
| PP1-M10 | SC-13「两侧调用串逐字相等」未钉抽取规则与归一化, 无代码无三态; 缩进约定未定 ⇒ 对正确实现可能判红, 或诱导「为迁就检查器改内容」 | CR M5 · TL m1 (canonical 串未钉) | **接受**: `metadata.new_checks` 增 N4 (从含脚本路径的行起连续取 `\` 续行、逐行 `strip()` 后比较列表), 副本上跑三态 (基线 / 目标 / 参数换序) 并嵌入输出; metadata 钉一份 canonical 调用串供 TASK-014 / 015 照抄 |

## Minor (去重后 20) 与处置

| 编号 | 内容 | 席位 | 处置 |
|---|---|---|---|
| m1 | TASK-012 未复述 S3 态 `results[].change_id` 须为 `None` (非占位串) | BA m2 | 接受 |
| m2 | TASK-002「另一席重跑」无第二执行体承担, 退化为自我复算 | QA m1 | 接受: 指派不同实例承担复现核对, 或如实改写为确定性自检 |
| m3 | TASK-022 对 SC-11 `present` 的例外条款 (实跑 missing ⇒ 记台账、不判失败) 未在 yaml 就地复述 | QA m2 | 接受 |
| m4 | 同形改写位置缺机检: `phase-c-integrator/SKILL.md:57` / `:754` 改没改无检查; `audit-engine/SKILL.md:423` 同一 hotfix 条件未列入 | KM m1 · CR m7 | 接受 (修类): TASK-018 补对应断言; TASK-015 顺带改 `:423` |
| m5 | `metadata.c25_five_questions` 引「`.aria/config.json` 的 multi_remote 段」, 该段不存在, 值来自 DEFAULTS.json | TL m2 · CR m5 | 接受 |
| m6 | 读前必看第 8 条括注把 bypassed 整体列为「P6 之前终止」, 但 missing 被豁免的 bypassed 要走完 P6 | TL m3 | 接受 |
| m7 | TASK-031 手写 Phase D 未交代与 phase-d-closer 的对应关系: 漏 D.4 estimator; D.1 跳过未留痕; D.2b 默认带 `--sweep-stale --gc` 与 owner 09-17 裁定冲突 | TL m4 | 接受 |
| m8 | AI 流程判断清单漏五项 (AB 判据与 old_skill 作 without 臂; TASK-003 的 checkpoint 补钉; `plugin-cache-currency` STALE 预期; 手写 Phase D; TASK-027 恢复指针) | TL m5 | 接受; 其中 TASK-003 补钉同时进读前必看表 |
| m9 | 反事实补丁构造者 (qa-engineer) 与测试作者同角色, 未保证「非测试作者」 | TL m6 | 接受: 写明用不同实例 |
| m10 | rule6_note 未交代新增的 `phase-c-integrator/SKILL.md:57` / `:754` 两处处方性改写的归类与兜底 | TL m7 | 接受 |
| m11 | 「被占 (含 10CG/Aria#211 T4) ⇒ 顺延」只能看到已合并值, 在飞轨不可见 | TL m8 | 接受: 写明以合并冲突或合并后复读为准 |
| m12 | TASK-002「C 的大小 (A.2 时 153)」实测 154 | CR m1 | 接受: 改 154 并写计数口径 |
| m13 | 三步法在带补丁 worktree 上直接 `worktree remove` 会 rc=128 | CR m2 | 接受 |
| m14 | TASK-024 用 `${VAR+x}` 判「已设置」, CLI 判据是取值 ∈ {1,true,yes}; `=0` 时误判 | CR m3 | 接受: 用与 CLI 同一判据 |
| m15 | AB 期间两个远端 master 一有变化即停, 他人推送是常态 ⇒ 假停 | CR m4 | 接受: 先核新提交是否含本会话产物 |
| m16 | TASK-027 第 7 步与 TASK-029 未跑已启用检查 `no-unresolved-version-placeholder` | CR m6 | 接受 |
| m17 | TASK-030 断言 HEAD 等于合并提交, 并发推送下会假停 | CR m8 | 接受: 改为「合并提交是 HEAD 祖先且第二父 = feature HEAD」 |
| m18 | 心跳 `--phase B` 不改 claim 的 phase (只写 `heartbeat_at`), track board 全程显示 A.2 | CR m9 | 接受: 台账注明 |
| m19 | owner_gates 第 2 项无执行步骤 (现实测本地 master 落后两端) | CR m10 | 接受: fetch → 判关系 → merge 不 rebase → 双推 → 逐 remote ls-remote |
| m20 | yaml 头注释与 `title` 仍写 v1 | CR m11 | 接受 |

**顺带 (风险项, 非 finding, v2 可低成本吸收)**: CR 风险 2 (`sc12_liveness.blind_spots` 补 `*/.aria/config.json` / `hooks.json` 盲区); CR 风险 3 与 4 (合并后复核 `ab-suite` 两个计数与 16 个版本点 —— 与 PP1-M8 同类「这个值现在该是什么」)。

## Conflicted

无。三条自报薄弱点五席表态: (a) 五席可接受; (c) 五席可接受 (CR 另指 SC-13 同类问题 → PP1-M10); (b) 三席可接受, 两席 (TL / CR) 判「对他轨 / 本轨未授权写入的强制对齐不可接受」→ 并入 PP1-M6, 不视为分歧。

## 流程记录 (不计入 verdict)

- knowledge-manager 报告 frontmatter 的 verdict 与其正文计数不符 (0M 却标 PASS_WITH_WARNINGS), 本聚合按 verdict 规则重算为 PASS; 报告原文未改。
- 本轮期间 `origin/master` 由 `8a9fe35` 前进到 `e4874d4` (并发容器 `bfe8285d` 的 10CG/Aria#211 轨, 含 `docs/handoff/latest.md` 改动), 不触本 spec 文件; 本地规划提交需再次并入后才能推送 (PP1-M7 / m19 同面)。
- PP1-M6 同时触及 owner 2026-09-17 的心跳免授权裁定: 心跳推的是整条协调 ref, 免授权前提应是「本地协调 ref 除本次心跳外无领先远端的写入」。主控已把这一前提补进该裁定的 memory 记录, 并将在会话收尾时请 owner 知悉。

## 收敛判断

R1 不收敛 (10 Major, Vote REVISE 2)。缺陷分布: 组 1 零 Major; 组 2 一簇 (M1, 验收粒度, 非实现逻辑); 组 3 三簇 (M2 / M9 / M10); 组 5 与协调面五簇 (M3 / M5 / M6 / M7 / M8) + 连带文案一簇 (M4)。处置全部为 tasks.md / yaml 内的定点修订, 不涉及 proposal 设计取舍与任务结构重排 (除 M2 的依赖边)。执笔: v2 继续由 v1 执笔实例 (非主控) 完成, 主控只核验; 若 R2 的 Major 中过半由本轮修订自身引入, R3 换新执笔实例。

## 席位报告

同目录 `post_planning-R1-2026-09-17T100518-186Z-pre-merge-completeness-gate-change-scope-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
