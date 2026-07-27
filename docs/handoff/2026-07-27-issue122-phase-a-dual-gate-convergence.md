---
track-id: phase-c-integrator-ci-path-coverage
owner-container: aria-runner-bot/023236f2
phase: A.3
status: active
updated-at: 2026-07-27T11:47:44Z
---

# Session Handoff (2026-07-27) — aria-plugin #122 Phase A 完结 (post_spec R1-R4 + post_planning R1-R6)

> 会话维度增量。承接 [上一份 session-close](./2026-07-22-claude-md-official-spec-diet-and-116-root-fix.md)（已 done 冻结）之后的一段。
> **本段主线 = 一次「审计比产物更值钱」的完整实证**: 为 aria-plugin #122 走完整个 Phase A, 两个 enabled 闸门跑满 **10 轮 / 33 个 agent 实例**, 抓到的**全是会让机制静默失效的真缺陷**, 每条都有实跑或反事实证据。Phase A 完结, Phase B 未起。

## §0 入口 (新 session 优先读)

- **当前态**: 主仓本地 `194a73b` / aria 本地 `3694871` —— ⚠️ **两者都 behind 远程** (主仓 3 / aria 4), 并发轨 `simonfishgit` 在本段期间 ship 了 **v1.64.1**。本段**零提交**, 12 个新文件全部 untracked。
- **产出**: `openspec/changes/phase-c-integrator-ci-path-coverage/` (proposal.md 60KB Level 2 + detailed-tasks.yaml 66KB / **27 任务 / 18 波 / 5 lane**) + `.aria/audit-reports/` 下 **10 份**聚合报告 (`post_spec-R1~R4` + `post_planning-R1~R6`)。
- **本段时序**: `/state-scanner` (exit 0) → owner 选 [1] full-cycle 走 #122 → probe-first 核实根因引用与撞车面 → A.1 起草 → **post_spec R1→R4** (max_rounds 耗尽, owner 裁 [1] 接受) → A.2/A.3 → **post_planning R1→R6** (owner 先裁 [2] 加轮至 6, R6 后裁 [1] 接受) → Phase A 完结。
- **下一步**: 见 §6 (**先读 §0.5**)。

## §0.5 🔴 附注 — 本文写完 7 分钟后发现: 本段产出与并发轨**重复**

> 时间线: 本文 frontmatter `updated-at` = 11:47:44Z → 并发轨 commit `257a20d` 落地 **11:52:18Z** → 下一 session `/state-scanner` 于 **11:56** fetch 后发现。上文 §0/§2/§5 的「behind 3」等数字是**写作当时**的真值, 保留不改; 本节是其后的增量真相。

**同一个 aria-plugin #122 上存在两份独立 Spec, 核心设计同构** (都把 `not_applicable` 从 `pending` 里分出来 / 都 fail-toward-covered / 都引同一段 `aether.py:223` 根因):

| | 本段产出 (本容器) | 并发轨 `simonfishgit` (`257a20d`) |
|---|---|---|
| 目录 | `phase-c-integrator-ci-path-coverage` | `phase-c-gate-path-coverage-not-applicable` |
| Status | 📝 Draft (R4-fix), `converged:false` + owner override | ✅ **Approved + owner 签字**, R4 qa PASS 0/0/0 真收敛 |
| post_spec | R1→R4 (5/5/3/2 席) | R1→R4 (5/5/2/1 席) |
| **A.2/A.3** | ✅ `detailed-tasks.yaml` 27 任务 / 18 波 / 5 lane + post_planning R1→R6 | ❌ **无** (目录内仅 proposal.md) |
| 规模 | proposal 551 行 + tasks 66KB | proposal 209 行 |

**两份各有对方没有的东西** — 并发轨那份 post_spec **真收敛且已签字**但没做任务分解; 本段这份 post_spec **靠 owner override 收场**但做完了 A.2/A.3 + 6 轮 post_planning。**哪份为准 / 要不要把 27 任务嫁接到已签字的 proposal 上 = owner 裁决 (Rule #10 权限面), AI 不自行决定。**

**为什么没早发现 (方法论教训)**: 本 spec proposal 头部写着「无 in-flight — 本地 fetch + Forgejo API 双核实」—— 那是 **2026-07-25 起草时**的核实, 而并发轨在本段跑 10 轮审计的**期间**落地。⇒ memory `feedback_concurrent_duplicate_audit_fetch_before_start` 的**第四次实证**: 单次起点 fetch 不够, **每次实质动作前**都要重扫。本段跑了 10 轮 / 33 agent 的审计, 没有任何一轮的入口断言包含「远端是否已出现同 issue 的竞品 Spec」—— **闸门审的是产物质量, 不审产物是否该存在**。

## §1 已完成 (本段)

1. **A.0 状态扫描** — scan.py exit 0 / errors[] 空 / 8 leg fresh fetch / custom checks 8/8 绿。顺带修了 `standards` 的 stale checkout (workdir 落后 tree 1 commit, `45a4301`→`f986a60`)。
2. **A.1 Spec (Level 2)** — `phase-c-integrator-ci-path-coverage`。核心设计: 用 `CIStatus.state` 里**已声明未生产**的 `not_found` 把「零 run」从「run 在跑」分出来 → 再做 workflow 路径覆盖判定 → `not_applicable`。**关键一格**: `not_applicable` **不旁路** main in-flight 检查 (Rule #8 的 (a)(b) 是两个独立条件, 原始 SilkNode 事故正是 (b) 类)。
3. **post_spec R1→R4** (5/5/3/2 席) — critical 轨迹 **5→4→1→1(争议)**。max_rounds 耗尽, owner 裁 [1] 接受 (`converged=false, overridden_by_user=true`)。
4. **A.2/A.3** — 27 任务 / 18 波; TDD **9 对 RED/GREEN 逐对分离** (qa 写测试 / backend 写实现); 5 lane 含 owner (Rule #10 触点 ×2)。
5. **post_planning R1→R6** (2/3/2/2/2/2 席) — critical 轨迹 **2→2→1→0→0→0**。owner 两次裁决 (加轮至 6 → 接受)。
6. **三类机械不变量脚本化并写进 TASK-020 常驻 verification** — 见 §7。
7. **B.1 前置复证就地做掉** — 见 §3 第 2 条。

## §2 未完成 / Carry-forward

**AI 内省 (load-bearing)**:

- 🔴 **工作区零提交** — 12 个新文件 untracked (2 spec 文件 + 10 份审计报告)。`aria-orchestrator` 仍 dirty (in-flight `feature/m6-cost-model-telemetry` 指针) —— **提交时必须排除它**, 那是 #165 orphaned gitlink 的事故形状。
- 🔴 **本地落后远程** — 主仓 behind 3 (`a33da6c` v1.64.1 gitlink bump / `996c944` #118+#119 triage / `e5aebb0` #116 剩余 scope), aria behind 4 (v1.64.1)。**提交前必须先 fetch + rebase**, 否则重蹈 memory `stale-local-main`。
- **Phase B 未起** — 从 **TASK-001** (blocking spike: 实测 aether CLI 的仓解析方式) 起手。它是整条 repo_root 腿的闸门, 证否则走 TASK-001b (owner 裁决)。
- **owner 待办 (Rule #10 权限面, AI 不得代劳)**: TASK-025b (CLAUDE.md 规则 #8 补一句 + `.aria/config.json` `_lane` 回改; 拟写文本已在 proposal §7 **逐字给出**供核验, 预算核算 151 行/13139 字节 → 新增一句不撞双预算) / TASK-001b (spike 证否分支)。
- **R6 的 7 条 major 已在 R6-fix 全量吸收**, 但两席建议「转入 Phase B 执行清单就地补齐」的性质保留 —— 若 B.2 期间发现文本仍有歧义, 按 R6 报告的建议修法处置, **不需要重开审计轮**。

**承前 owner 门**:

- 🔴 **凭据轮换 — 第八次 surface 无闭环**: `FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET`, **hard cap 2026-08-02, 剩 ~6 天**。唯一带硬期限的 carry, owner 亲自操作项。本段开场推荐里列了它, owner 选了 #122。
- **#165 收窗判定点**: 等 aria-orchestrator 子模块下一次真实合并走约束 1/2。
- **#116 剩余 scope**: ✅ **本段期间被并发轨做掉** (`e5aebb0` 判断标准改三臂语义分档 + 产出形态钉死 + baseline 污染面披露) —— 上一份 handoff §6 第 3 项可销。
- **未 triage**: bot 新开的 #117 / #120 / #121 / #122(已做) 中, #118+#119 已被并发轨 triage (`996c944`); 余 **#117 / #120 / #121** 仍未 triage。承前 #168 / #169 / M6 四门 / M7。

**机械补漏 (backstop)**: `handoff_autofill` 的 unfinished 列表全部来自 6 个活跃 M6/M7 spec 的 tasks.md (**本段零碰**); consistency 6 flags 全结构性 (Aria 无 UPM)。**sync 段报了 4 条 warning, 全部是真的** (见上「本地落后远程」) —— 这次机械兜底抓到了 AI 内省漏掉的东西, backstop 生效。

## §3 关键风险 / 已知陷阱 (本段新增)

1. **审计报告自述的「已修复」两次实为未修** — R2 报告处置清单 11 项里, `tdd_note` 那次 `replace` 静默失败、三条同文件域边只落两条。两者都是**下一轮 agent 实读发现的, 不是写报告的我发现的**。⇒ memory `feedback_cross_doc_claim_verify_at_target` 的新 locus: **审计报告自身**也要去目标处实测。
2. **✅ B.1 前置复证已就地做掉** — 我自己在 `metadata.scope_repo_head` 写了「B.1 建分支前必须 re-verify」, 而并发轨恰好在本段 ship 了 v1.64.1。实测 `git -C aria diff --name-only 3694871..6ffd8cd` 与本 spec 引用的 7 个文件 **零交集** ⇒ **~30 处行号引用在 `6ffd8cd` 上原样有效** (照 #113「v1.62.1 零触碰本 spec 实现点」先例记账, 已落进 metadata)。**B.1 时仍须再验一次**。
3. **⚠️ `owner-container` 的机械值是 bot 的身份** — 本 handoff frontmatter 的 `aria-runner-bot/023236f2` 是 `handoff_autofill.py --owner-container` 的**逐字输出** (模板明令勿手填, DEC-20260704-002 §4 病根 #3: 手填曾漂移出 6 种值)。溯源: 本容器 `git user.email = aria-runner-bot@10cg.pub` + `~/.aria/container-id` uuid `023236f2` (label 空)。**这意味着本容器内任何 session 都会被标为 bot 身份, 无论谁在驱动**。而本段并发 ship v1.64.1 的是 `simonfishgit <simonfish@gmail.com>` —— **不同 owner**。若这会影响 collision 分类的准确性, 建议 owner 给 `~/.aria/container-id` 设人类 label 或复议 identity 派生规则。
4. **审计的 33 个 agent 实例里, 1 个因 API 连接中断早退** (post_planning R1 的 qa-engineer)。按 audit-engine 错误处理记 `incomplete: true`; **owner 裁定「就现有 findings 做 R1-fix, 余 3 席并入 R2」** —— 这是 owner 对闸门执行序的处置, 非 AI 自行降级, 已在 R1 报告留痕。

## §5 多维度同步状态 (机械核验)

- **git**: 主仓本地 `194a73b` (**behind origin/github 各 3**) / standards `f986a60` (detached, 本段修复 stale checkout) / aria 本地 `3694871` (**behind 各 4**) / aria-orchestrator `92acce5` (`feature/m6-cost-model-telemetry`, 只读未动)。
- **custom checks**: session 起点 8/8 绿。
- **openspec**: 活跃 change **7** 个 (本段新增 `phase-c-integrator-ci-path-coverage`, 其余 6 个 M6/M7 本段零碰); `design_deferred` 仍 1 项 (`aria-2.0-m6-release-closeout`, staleness 63d)。
- **consistency flags**: 6 条全 advisory 且全结构性 (`active_change_not_in_upm` × 6 —— Aria 无 UPM, 属**恒亮**, 非本段引入)。
- **issue 面**: 本段只对 #122 做了完整 Phase A, 未开新 issue; proposal §Follow-up 的 8 条 + DUAL_LAYER_SPEC 扩展字段升 SOT 1 条 = **9 条待 TASK-024 开立** (Phase C 后)。

## §6 Next session 入口 + 优先级

1. 🔴 **凭据轮换** (第八次, hard cap **2026-08-02, 剩 ~6 天**) — owner 亲自操作项, 逾期前最后窗口。
2. **落盘本段产出** — fetch + rebase (本地 behind) → 提交 12 个新文件, **排除 `aria-orchestrator`**。
3. 🔴 **#122 双 Spec 碰撞裁决 (阻塞 Phase B, owner 出)** — 见 §0.5。在 owner 裁定哪份为准之前**不要起 Phase B**, 否则是在一份可能被作废的 Spec 上继续投入。归并分析可由 AI 先备好作为裁决输入。
4. **Phase B 起手 (受 3 阻塞)** — B.1 建分支前 (a) re-verify aria master 是否仍是 `6ffd8cd`, 若已前进则逐处 grep 复证行号; (b) 经 phase1_gate 认领 (`--linked-issue aria-plugin#122`, collision.kind=self_multi_container); (c) 从 **TASK-001 spike** 起手 —— 它 blocking, 结论决定整条 repo_root 腿是否存在。
5. **owner 门**: TASK-025b (CLAUDE.md 规则 #8, 文本已备) / TASK-001b (spike 证否分支)。
6. 未 triage: **#117 / #120 / #121**; 承前 #168 / #169 / M6 四门 / M7。

## §7 本段对方法论本身的影响 (最值钱的部分)

**两个闸门各有一条贯穿的病灶主线, 且每轮的 critical 都出现在上一轮新写的文本里。**

**post_spec —「空集/退化集真值真空」四次形变**:

```
R1  空 changed_files        ∃ 对空集恒假 ⇒ covered=False + confident=True (最高置信 skip)
R2  零 event                流式映射/找不到 on: 键 ⇒ 静默流入并集
R3  空 unit 集              全部事件落黑名单 ⇒ any([])=False / all([])=True
R4  unit 定义域结构性偏窄     ← 前置守卫检查不到 (units 非空!)
```

前三次可靠「再枚举一遍」堵, 第四次不行 —— 它是**集合的构造公式对一整类合法贡献者不可达**。收口手法最终从「枚举 `covered=False` 路径」升级为「**任何空集合必须先被显式早退拦住, 禁止 `any()`/`all()` 的语言默认值代为决策**」—— 这条不依赖枚举的完备性。

**post_planning —「承诺不在它该在的层」四次形变**:

| 形变 | 轮次 | 封它的机制 |
|------|------|-----------|
| ① 承诺存在于**散文**而非机器可读层 | R1-R3 | 三项**无向**不变量 (归档门解析器 / 同文件交集 / wave+环) |
| ② 进了机器层但**方向/作用域写反** | R5 | 三条**方向敏感**核对 (deliverable 生产者 / RED→GREEN / owner 裁决可达) |
| ③ 声明覆盖了但**没配可执行断言** | R6 | AC→verification 逐条配对 |
| ④ **状态/度量的写入时序方向** | R6 | 第四类 (d) + gate 分支**反事实图重建** |

四类现全部写进 TASK-020 的常驻 verification。**关键教训: 加了机械核对 ≠ 那类错误被封住 —— 核对的维度必须与错误的维度同构。** 三项无向不变量全绿的同时, 三条方向性错误安然存在 (R5 实证)。

**收敛判据的新认识**: post_planning critical 在 R4 就归零, 但 major 在 R5/R6 回升并**持平** (6→7)。两席独立判定「**加轮收不敛**」——「每轮修订都会新引入约等量的同形状缺陷」(R5 的 5 个 major 里 3 个是 R4-fix 引入的; R6 的 7 个里 3 个是 R5-fix 引入的, 修与引入近似 1:1)。⇒ **停止加轮的判据是 major 数是否还在降, 不是 critical 是否归零。**

**换新鲜眼睛 > 加轮**: R5 首次派入一席只审过 R1、没看过 R2-R4 的 tech-lead, **一轮抓出该轮 6 个 major 中的 5 个**。其中最典型的一条: R2 的建议「给 TASK-010 加 TASK-009 依赖」与它自己描述的危害「若 009 先完成则 AC-7 无红窗口」**相反**, 我照抄了并把 finding 原文抄进注释 —— **两句互相矛盾的话并排放了三轮**, 前三轮反复读过同一段文字的席位无一发现。

**审计抓到的是真缺陷, 不是文字问题** (每条都有实跑/反事实证据):

| 缺陷 | 证据 |
|------|------|
| 规格按字面实现会让「零 CI run 的 PR 直接放行」 | 实跑 `compute_verdict([], "not_found") → green` |
| `?` 的 glob 语义**写反** (GH filter-pattern 的 `?` = 前一字符 0/1 次) | 方向恰是误 skip |
| 为簇 A 设的决定性测试 **dict 比字符串恒假** | 无红→绿窗口 = 该修复零自动化保护 |
| 把**本项目已勘误过**的旧误传抄进新 Spec | `ARIA_AETHER_MOCK_RESPONSE_FILE`; `benchmark.md:70` 早已明文纠正 |
| 为 R2-H 写的修法**打断了消费这个文件的归档门解析器** | 反事实: 仅改名嵌套键 → `parse_ok` False→True |
| AC-7 有 `covers_ac` 却**零 verification bullet** | 三轮注意力被「它排在哪个位置」占满, 没人问「它的断言有没有被要求写出」 |

## §8 Memory entries this session (本段)

**已落 (2 条新 + 1 条更新)**:

- `feedback_invariant_dimension_must_match_error_dimension` (新) — 机械不变量的**维度**须匹配错误的维度; 无向检查 (存在/覆盖/连通) 对**方向性**与**时序**错误天然免疫, 可全绿而错误安然存在。补的是 [[feedback_invariant_needs_failclosed_default]] (极性) 与 [[feedback_validate_invariant_at_source_not_mixed_output]] (层次) 之外的**第三个正交轴**。
- `feedback_stop_adding_rounds_when_major_count_flattens` (新) — 加轮判据是 **major 数是否还在降**, 非 critical 归零; major 持平 = 每轮 fix 引入约等量同形状缺陷 = 不收敛; **换新鲜眼睛 > 加轮**。与 [[feedback_audit_convergence_pattern]] / [[feedback_3round_early_convergence]] 互补 (那些讲「何时可**早**收敛」, 本条讲「何时该**停止加轮**」)。
- `feedback_rationale_formula_contradiction_is_signal` (**更新**) — 新增第二个 locus: **审计建议自身的「危害描述」↔「建议修法」矛盾**。照抄任何建议前先把两者对着读一遍。

**本段未落 (已有覆盖)**: 「修复在自己兜底路径复发」(`feedback_fix_recurs_in_its_own_fallback_path`, 本段四次实证) / 「文档 A 说已在 B 修好必去 B 实测」(`feedback_cross_doc_claim_verify_at_target`, 新 locus = 审计报告自身, 已在 §3 记) / 「注意力被公式独占」(`feedback_verify_predicate_inputs_exist`, AC-7 案例是完美新实例) / 「两独立实现者同规格得相反结果」(`feedback_spec_underdetermination_two_implementer_test`, 多次命中)。

## §9 流程判断留痕 (Rule #10, 请复议)

- **两个 enabled 闸门全程未自行豁免**。三次 owner 裁决点 (post_spec 降级 / post_planning 加轮 / post_planning 降级) 均经 `AskUserQuestion` **显式请裁**, 未自作主张。
- post_planning R1 因 agent API 中断记 `incomplete: true`, **owner 裁定「就现有 findings 做 R1-fix, 余 3 席并入 R2」** —— owner 对闸门执行序的处置, 已在 R1 报告留痕。
- session 级硬约束「未经要求不得调用 Agent」与 Rule #10「不得自行豁免 enabled 闸门」在两处相撞 (post_spec / post_planning 入口), **均先请示后执行**, 未以任何一方为由跳过另一方。
- 团队规模在后续轮次收缩 (5→3→2) 按 #113 先例 (R1/R2 5-agent → R3 3-agent → R5 1-agent 由反对方独立复核), 非临场裁量。

## Cross-references

- 上一份 session-close: [2026-07-22-claude-md-official-spec-diet-and-116-root-fix.md](./2026-07-22-claude-md-official-spec-diet-and-116-root-fix.md)
- 并发 bot 轨 (前一段): [2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md](./2026-07-22-issue113-ship-v1.64.0-and-rule6-third-row.md)
- 本段产出: `openspec/changes/phase-c-integrator-ci-path-coverage/{proposal.md, detailed-tasks.yaml}`
- 审计轨迹 (10 份): `.aria/audit-reports/post_spec-R{1,2,3,4}-*-aggregated.md` + `post_planning-R{1,2,3,4,5,6}-*-aggregated.md`
- issue: [aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) / owner 定案留痕 主仓 `194a73b` + `.aria/config.json` `phase_c_integrator._lane`
