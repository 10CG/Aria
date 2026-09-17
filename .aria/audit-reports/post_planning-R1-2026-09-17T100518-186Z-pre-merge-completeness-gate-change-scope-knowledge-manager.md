---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T10:48:04.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (全文, 207 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (全文, 1056 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `:1-120`(头部/Why/What §1 求值总序)、`:120-229`(§1.0 硬约束/§1.1/§1.1b/§1.2/§1.2b/§1.3 起)、`:325-406`(§2 SKILL.md 接线/§3 phase-c-integrator/§4 文档同步表/§5 向后兼容 12 条)、`:407-452`(Tasks 17 项)、`:453-471`(SC-1/SC-2/SC-13/SC-14/SC-15 逐条; 其余 SC 未逐条重读, 信任其与 TASK verification 的一致性已抽样核)、`:480-488`(rule6_note)、`:488-555`(待 owner 复议 条目 0 + #1-#13, 逐条核对已回填的裁定落款)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文
- `CLAUDE.md`「多远程推送两条硬约束」与不可协商规则 #3/#6/#8/#10 (随对话上下文提供, 未重读文件)
- `standards/conventions/content-integrity.md` `:161-210` (§4.4/§4.5)
- `aria/skills/phase-c-integrator/SKILL.md` `:50-62`、`:125-140`、`:745-760`
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` `:184-190`、`:320-430`、`:508-560`、`:920-930`、`:1030-1122`、`:1630-1645`
- `.aria/config.json`(audit 块)、`README.md` `:8,242`、`README.{zh,ja,ko}.md` `:3,10,244`、`CLAUDE.md` `:139,141`、`VERSION` `:24`、`docs/architecture/system-architecture.md` `:189`、`docs/architecture/version-scheme.md` `:23`
- `aria/skills/state-scanner/scripts/check_bare_issue_refs.py`(实跑)、`aria/skills/audit-engine/references/execution-modes.md`(grep 核数)、`aria/skills/phase-a-planner/SKILL.md:267`、`aria/skills/phase-b-developer/SKILL.md:204,277`、`aria/skills/state-scanner/scripts/collectors/multi_remote.py:105-115`
- 结构性核验 (自写 python/bash, 未落盘于仓内): checkbox 数量 (31=31)、tasks.md↔yaml `parent` 逐项顺序比对、yaml 依赖图无环/无缺失目标、`estimated_hours`/`agents` 汇总与 metadata 逐字比对、content-integrity §4.4/§4.5 自查命令实跑

## Findings

无 critical。

### Major

无。

### Minor

| id | severity | type | category | scope | summary |
|---|---|---|---|---|---|
| `27bf266b` | minor | issue | documentation | `detailed-tasks.yaml` TASK-016 / `tasks.md` 读前必看第 19 条 | `phase-c-integrator/SKILL.md:57` 与 `:754` 的「同形改写」要求缺 SC-13 机械核验背书 |

**m1 — 证据**: proposal.md `:469` (SC-13 逐字断言列表) 只锁 `:132`(步骤 3 优先级链、`mode == "convergence"`/`mode == "challenge"`/`照常调用门`)、`anchor_base`、fail-closed 义务落点等九条 grep, 通篇未出现任何针对 `:57` 或 `:754` 的字面断言; `detailed-tasks.yaml` TASK-018 (组 3 提交前机检) 的 verification 逐条复述 SC-13 清单, 同样没有补一条覆盖这两行。而 `phase-c-integrator/SKILL.md:57`(`当 audit.enabled=true 且 audit.checkpoints.pre_merge != "off" 时…`)与 `:754`(emergency hotfix 段 `仅 audit.enabled=true 且 audit.checkpoints.pre_merge != "off" 时`)本轮实读确认字面存在, 与 `:132` 同款「字面键」写法; `tasks.md` 读前必看第 19 条与 TASK-016 verification (`:57 的触发条件摘要与:754 的 hotfix 降级条件改为「pre_merge 按 C.2 pre_hook 步骤 3 的优先级链判为启用时」`) 是本轮 A.2 新增发现, proposal 原文完全未提及这两处 (grep `:57|:754` 只命中改前引用行本身), 因此也不在 proposal 的 SC-13 断言面内。

**失败场景**: 执行者按 TASK-016 改了 `:132`(有 grep 锁定, 必改对), 但漏改或错改了 `:57`/`:754`(散文摘要), TASK-018 与后续 TASK-021(回归)/TASK-027(合并树原位回归) 跑的仍是同一份 SC-13 断言集合, 全部亮绿; 归档预演 (TASK-031) 与 SC-12 liveness 复跑也不涉及这两行。结果是 `phase-c-integrator/SKILL.md` 内部出现「步骤 3 讲五档优先级链, 但 `:57`/`:754` 仍讲字面键判断」的自相矛盾, 且这个矛盾不会被本计划任何一步的机械检查标红, 只能靠人工审阅(例如下一轮 post_planning 或 post_implementation 审计)偶然发现。

**建议修法**: 在 TASK-018 (或 TASK-016 自身) 补一条形如 `grep -c 'audit.checkpoints.pre_merge != "off"' phase-c-integrator/SKILL.md` 应为 0(或按改写后的新句逐字比对)的断言, 与已有的「调用方接缝」grep 并列; 不要求回填 proposal(这是 A.2 新增而非 proposal 遗漏), 只需给 tasks.md/yaml 自己新增的这条要求配一个可证伪的核验点。

## 对执笔人自报薄弱点的表态

(a) 读前必看第 7、8 条 (裁定 11 派生字段取值、短路运行非判定键) 由执笔人钉定, proposal 未定义 — **可接受**: 这是「原稿未定义的实现细节」而非「产品级放行面扩张」, 落在 Rule #10 白名单可判范围外的技术级裁量; 取值内部自洽(与 §1.4 既有格式对齐、WARN 文案统一)、且已显式标注「执笔人钉定」不冒充 proposal 原文, 符合「owner 只裁产品级, 技术级 AI 直接裁」的分工。

(b) 组 5 发布前提偏重 (TASK-030 要求 aria-orchestrator 两端完全一致; TASK-024 结束后强制对齐协调 ref 会回退本容器 `--no-push` 心跳) — **可接受**: 两处都不是静默失败, 前者有 owner_gates 第 6 项「停下上报」兜底且不影响本轨自身分支, 后者已在 TASK-024 verification 末尾明写「对齐前后的值记台账」并要求「换不带该变量的会话继续」, 心跳会在下一会话重新刷新, 不构成数据丢失, 只是流程摩擦。

(c) N1/N2 仍是按行切片的文本谓词; SC-11 的 post_planning 期望收紧为 `present`; SC-6 快照自证放在活体运行(4.4), 不进单测 — **可接受**: N1/N2 的局限已被诚实标注在 `metadata.new_checks.cannot_catch` 且由 SC-16/SC-18/SC-17(5) 的运行时断言兜底语义正确性; SC-11 的 `present` 期望被明确要求「实跑为 missing 属新发现, 记台账上报, 不改断言」, 不是悄悄改断言掩盖问题; SC-6 快照 295KB 不适合进单测套件(不随插件分发)的判断合理, 且移到 TASK-022 活体执行并非取消验证。

## 风险 / 疑问

- TASK-024 (Rule #6 AB) 依赖 owner_gates 第 4 项「以 `ARIA_COORDINATION_NO_PUSH=1` 启动新会话」这一会话级前置, 若无人值守执行体无法在同一 session 内触发这种重启, 该步会停滞。计划已如实标注「会话内补不上」并作为 owner 等待点处理, 不是本计划的设计缺陷, 但提请下一 Phase 执行时确认这一步确有可行的会话切换机制。
- `metadata.a2_state_runs` 的三态实跑脚本与输出, 本轮做了「脚本逻辑读一遍 + 关键函数(`classify_symbol_liveness`/`extract_claim_symbols`/`_iter_task_items`)与真实源码逐段核对语义一致」的核验, 未逐行重跑该嵌入脚本本身; 语义核对未发现矛盾。

## Verdict

**PASS_WITH_WARNINGS** — 0C / 0M / 1m

**Vote: PASS**

## 是否足以开始 Phase B

足以 —— 本轮从文档同步面、发布同步面 (16 个版本点逐处核验属实)、两张映射表 (内联 17 项↔新编号、13 条裁定↔决策单 §2)、读前必看 22 条 (抽核 ≥10 条, 含多条源码 `file:line` 实读) 与写法规范 (content-integrity §4.4/§4.5 自查零命中) 五个维度未发现 critical/major 缺陷; 唯一记录的 minor (m1) 是「新增要求缺机械背书」的可完善项, 不阻塞 Phase B, 可在 TASK-016/TASK-018 执行时顺手补一条 grep 断言。
