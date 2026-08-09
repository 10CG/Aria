---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T12:53:20.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R1 汇总 — premerge-gate-mainbranch-failclosed

> 被审对象 = A.2 产物 (`tasks.md` + `detailed-tasks.yaml` 19 条)。`proposal.md` 为参照物, 其 post_spec R1–R5 已 `converged:false` + owner override, 本轮不重审。

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | layer:proposal |
|---|---|---|---|---|---|
| code-reviewer | REVISE | FAIL | 3+8+5 = 16 | 5 | 1 |
| tech-lead | REVISE | FAIL | 1+9+5 = 15 | 3 | 1 |
| qa-engineer | REVISE | FAIL | 2+2+4 = 8 | 3 | 0 |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0+4+4 = 8 | **0** | 1 |
| **knowledge-manager** | **PASS** | PASS_WITH_WARNINGS | 0+2+3 = 5 | **0** | 0 |

**4 REVISE / 1 PASS** · verdict **FAIL** · `converged: false` · 零 spawn 失败。原始 52 条 → 去重 **3C + 12M + 8m = 23**。

## 三条 Critical

| ID | 席位 | 内容 | 编排层复现 |
|---|---|---|---|
| **PC1** | **3 席** | **TASK-011 的验收对 `--main-branch` 完全失明** —— 构造 `python3 "$GATE" --pr-branch "<PR_BRANCH>" --main-branch main --remote origin`, SC-1/SC-2/SC-3 得 **0/0/2 全过**。漏写该参数、写 `main`、写 `master` 三种写法都过闸, 分别致本仓恒红 / 本仓恒红 / 第三方恒红。**断言的量 (`--pr-branch`) 与病灶的量 (`--main-branch`) 不同维** | ✅ 实跑 |
| **PC2** | 1 席 | **SC 编号与既有测试全面冲突**: `test_path_coverage.py` 已占 SC 1-8/16-20/23-28, `test_pre_merge_gate.py` 已占 SC 9-13/15/21/22 ⇒ **我的 SC-1..13 十三个号一个不剩全撞**。⚠️ **该问题在 R2-fix 版曾用 `SC-M*` 前缀修好过, 重定范围时静默丢失** (当前 proposal `SC-M` 计数 = 0) | ✅ 实跑 |
| **PC3** | 1 席 | **组 0「先看到红」只覆盖 4/13 条 SC** —— SC-6~SC-13 八条**行为**断言无 owning task、无 deliverable、无红窗; 交付测试文件的只有 TASK-001/005/010, 而 TASK-008 写「SC-6/13/7/8 全绿」其 deliverables 只有 `pre_merge_gate.py`。**「TDD 接管」的裁定只落地了 grep 面** | — |

> PC1 的成因值得单记: R5 抓到「SC-3 期望 1 与 D1『两处』矛盾」后, 编排层改断言时挑了一个**不会和 D1 打架**的量 (`--pr-branch`)。**优化了文档的内部自洽, 把它与缺陷的连接优化掉了。** 对应 memory `invariant-dimension`。

## 主要 Major (去重 12 条, 摘 6)

- **`SKILL.md:262/:559/:610` 误引** (4 席独立命中, 编排层复现) —— 三行实读全是 `${ARIA_PLUGIN_ROOT:-aria}`, 而 Spec 称它们用 `CLAUDE_PLUGIN_ROOT`。该文件内 ARIA=3 / CLAUDE=1 (仅 `:737`)。**这是 spike 的输入, 输入错则 spike 做错**;
- **TASK-004 的两个「⛔不得再造」复用目标实际不可直接复用** (3 席): `aether._run_with_retry` 是私有实例方法、硬绑 `[self.binary]` 跑 aether 非 git、只捕 `TimeoutExpired`; `path_coverage._run_git` 无重试且把异常与非零退出码折成同一返回形状 ⇒ SC-7/SC-8 分流无从判别。唯一可行路径 (改 `aether.py`) 不在 `scope_repos.paths`;
- **ship_target 多处未收敛 + MAJOR 的连锁无人承接** (2 席, 编排层复现): `proposal` 抬头仍写「地板 MINOR 待裁」而 §版本 已改 MAJOR; 且 MAJOR ⇒ v2.0.0 会激活 `pre_merge_gate.py:68/:116` 自带的「removed in v2.0」弃用到期承诺, 19 条任务无一承接;
- **DAG 缺 3 处语义依赖边** (backend-architect): TASK-008 需 TASK-007 的 remote 参数 / TASK-011 需 TASK-003 定稿 / TASK-012 需 TASK-009 的 raw_message 形态 —— 而 TASK-013 同场景已正确处理, 属自身建模不一致;
- **TASK-005/TASK-008 的接缝无人复检** (3 席): TASK-005 只依赖 TASK-003 可在新 subprocess 存在前完成, 其验收「test_sc22 落地后仍 PASS」在自身执行点**恒真**; TASK-008 无一条 verification 复检它;
- **多条恒绿断言**: SC-12 对「必填参数缺失 (argparse exit 2)」恒绿 · TASK-007「同一个 remote 值」在被测面上不存在该量 · TASK-019 五条 verification 全是「issue 该写什么」, **可在零 issue 创建下自称完成**。

## 两条对编排层最有用的席位判断

**code-reviewer 的分诊**:
> 两条 Critical 的修法都是**加断言/加任务**而非改文档措辞, 与 owner「停止改文档、用 TDD 接管」同向, **不会重蹈 post_spec 五轮的 fix-引入-新-Major 形状**。依赖图与锚点类是机械低风险。另有 4 条需 owner 或 proposal 层一句裁定, 建议**一次问清再进 Phase B**。

**knowledge-manager (本轮唯一 PASS 票)**:
> 两个 Major 属「Level 3 应钉住但没钉住」的完整性缺口, **不阻塞 TG-0~TG-2 的 TDD 前置与实现**, 但必须在进入 TG-3 (合规与同步面) 前解决, 否则会在 Phase C 才暴露。Rule #5 / Rule #9 / Level 3 三件套均合规。

⇒ **两席的结论合起来给出一条可执行路径**: 本轮缺陷**集中在验收断言与依赖图**, 不在任务拆解的结构; 且**修法性质与前五轮不同** (加断言 vs 改散文)。

## 编排层本轮新增错误 (承前 16 条)

| # | 错误 | 性质 |
|---|---|---|
| 17 | SC 断言选了**不会与 D1 冲突**的量, 而非**病灶所在**的量 ⇒ 全套验收对 `--main-branch` 失明 | 维度不匹配 (`invariant-dimension`) |
| 18 | **重定范围时静默丢掉 `SC-M*` 前缀这个已付出的修复** | 新形状: 重写使已修复项归零, 无机制发红 |
| 19 | 「`:262/:559/:610` 用 `CLAUDE_PLUGIN_ROOT`」—— 核了「全仓 66 处」这个数就断言那三行, 没读那三行 | 第三次同款误引 |
| 20 | 「helper 3 个副本」—— 把同一 inode 数了两次, 又漏了三份 plugin cache | 量的定义不清 (物理拷贝 vs 访问入口) |
| 21 | §版本 改 MAJOR 但抬头与 tasks.md 未同步 | 修落一处, 声称留另一处 |
| 22 | 「TDD 接管」只给 grep 面建了红窗, 八条行为 SC 无人承接 | 执行裁定时只落地了容易的那半 |

## 轮次记录

| 轮 | 席位 | vote | 去重 | 阻塞 B | converged |
|---|---|---|---|---|---|
| R1 | 5 | 4 REVISE / 1 PASS | 3C + 12M + 8m = 23 | 6 | false |

`max_rounds` = 4 (post_planning 独立起算), 已用 **1**。处置须 owner 裁定。
