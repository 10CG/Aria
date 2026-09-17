你是 Aria 仓 (`/home/dev/Aria`) **post_planning convergence 审计第 1 轮** 的 **qa-engineer** 席。被审对象是 10CG/Aria#199 Spec `pre-merge-completeness-gate-change-scope` 的 A.2/A.3 计划 **v1.1** (主仓本地提交 `97c3515`, 未推送)。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 你要审的

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (A.2)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (A.3, 单一 SOT; `metadata` 含基线复核、裁定落点、三态实跑脚本与输出、C.2.5 五问)

## 审计锚点 (Step 0, 本周期不变)

- primary_goal: 把 Approved 的 10CG/Aria#199 proposal 分解为可执行的 Level 3 双层任务, 忠实落地决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` §2 的 #199 表 13 行 (连同 §5) 与 Level 3 三处连带重写 (SC-12 归档门 liveness 子句 / §1.3(c) 自证段 / SC-6 自证格)
- in_scope: 任务分解与粒度 / 依赖与执行序 / agent 分配 / 验收判据是否可证伪 / 裁定与重写的执行口径 / 基线复核记录 / 外向动作与 owner 等待点 / 发布段
- out_of_scope: proposal 的设计取舍本身 (post_spec 五轮后 owner 已裁「接受当前结论」); 13 条裁定本身对不对 (只查计划是否忠实落地)
- source_sha: `97c3515`

## 背景事实 (派单时主控实测)

- 主仓 master `97c3515` (领先 `origin/master` 1 个提交, 即本计划); aria 子模块 `1cb3872` (v1.73.3); standards `8b49562`。proposal 行号冻结于 aria `301641b`; 计划声称 `301641b..1cb3872` 对被引代码 / 规程文件零 diff。
- 本仓 audit config: `post_spec` / `post_planning` = convergence; `mid_implementation` / `post_implementation` / `pre_merge` / `post_closure` / `post_brainstorm` = off。
- owner 2026-09-17 两条当场裁定: (1) 先做本 spec 的 A.2/A.3, 同伴轨 10CG/Aria#195 的 Phase B 尚未开始 (决策单 Q3 原为「#195 先, 串行」, 计划把它落成 B.1 入口等待点); (2) 本容器已有 active claim 的心跳刷新属例行维护, 免逐次授权; 新写 claim、`release_gate` 的 release/sweep/gc、推 master/tag/gitlink 仍逐项授权。
- 执笔: v1 由新派 tech-lead 实例起草, v1.1 为主控核验返修 (只改心跳授权口径 + 等待点第 14 项)。主控已在 scratch 副本复跑 `metadata.a2_state_runs` 的脚本, 输出与嵌入逐字节一致。
- 执笔人自报的薄弱点 (你可以判它们可接受或不可接受, 但请明确表态, 不要当作「新发现」重复报): (a) 读前必看第 7、8 条的取值是执笔人钉定的, proposal 未定义; (b) 组 5 发布前提偏重 (5.8 要求 aria-orchestrator 与两端完全一致; 5.2 结束后强制对齐协调 ref 会回退 `--no-push` 心跳); (c) N1 / N2 仍是按行切片的文本谓词; SC-11 的 post_planning 期望收紧为 `present`; SC-6 快照自证放在活体运行 (4.4), 不进单测。
- 本轮为 R1, 无前轮结论。本轮入口竞品探针: `no_sibling_found` (两远端完整扫描, 无 cap)。

## 必读

1. 上面两个被审文件 (全文)。
2. `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` —— 295KB 超长行, 按你的视角分段读相关节 (Read 的 offset/limit, 或 `python3` 切片)。节目录: `## Why` `:23` / `## What` `:70` (§1.0 `:103`, §1.1 `:153`, §1.1b `:172`, §1.2 `:187`, §1.2b `:210`, §1.3 `:221`, §1.4 `:271`, §2 `:325`, §3 `:343`, §4 `:356`, §5 `:370`) / `## Impact` `:393` / `## Tasks` `:407` / `## Success Criteria` `:453` / `## rule6_note` `:480` / `## 待 owner 复议` `:488`。
3. 决策单 §1–§5 (全文 140 行左右)。
4. `CLAUDE.md` 的「多远程推送 — 两条硬约束」与不可协商规则 #3 / #6 / #8 / #10。
5. 你的视角需要的源码 (aria 子模块 `aria/skills/...`, 实读; 引用 `file:line` 以你实读为准)。

## 你的视角

验收设计与可证伪性:
1. SC-1~SC-22 每条是否都有 RED / 转绿 / 反事实或回归的承载任务; tasks.md 末尾「SC ↔ 任务映射」表与 yaml 各 TASK 的 verification 是否一致 (逐条核, 不抽查)。
2. RED 批次 (1.4–1.7) 能否在脚本不存在时以 AssertionError 形态真实红; 测试风格约束 (unittest, 禁 pytest / conftest) 是否与 `aria/skills/audit-engine/tests/test_sibling_spec_probe.py` 的两条守卫及 `aria/skills/run_all_tests.sh` 的分类逻辑相符 (实读)。
3. 反事实设计 (4.1 / 4.2): 「非实现者构造 + 三步法 (未打补丁副本绿 → 打补丁后红 → 记副本 SHA 与补丁)」是否写到可执行; 坏实现是否像真实坏情形。
4. 三处重写与新检查 N1–N3 能否真的红: 读 yaml `metadata.a2_state_runs` / `new_checks` / `sc12_liveness`; 如需实跑, 在你自己的副本里做。特别判断重写 c (SC-6 快照自证移到 4.4 活体) 与重写 a (L1/L2/L3) 的区分力是否足够。
5. B.0 语料冻结 (1.2) 的双列标注与按族分流规则是否按 proposal `:409-428` 完整落地, 标注者与实现者分离是否写到可执行。
6. SC-12 回归命令在有无 `ARIA_COORDINATION_NO_PUSH` 两种会话下的结论 (读前必看第 12 条) 是否被正确安排进任务顺序。

## 严重度口径 (统一, 请照此分级)

- **critical**: 照计划字面执行会写出错误代码并被计划自身的验收放过, 或造成难以撤销的外向后果 (误推、覆盖他人工作、泄密)。
- **major**: 照计划字面执行会卡死 (无合法下一步)、得出不可证伪 / 恒绿 / 恒红的验收结论、漏掉某个必做项 (SC / 裁定 / 文档同步面 / 外向动作登记), 或与 SOT (proposal 执行口径、决策单、CLAUDE.md 硬约束、源码事实) 矛盾。
- **minor**: 措辞、引用精度、可读性, 不改变执行者会做什么。
- 一条 finding 若**不影响「执行者会不会做错 / 做漏 / 卡住」**, 最高只能是 minor。

## 证据要求

- 每条 finding 必须附**你亲自核验的证据**: `file:line` 实读原文片段, 或你实跑的命令与输出 (输出可截断, 不得改写)。无证据的推测写进「风险 / 疑问」, 不计入 finding。
- 每条 finding 写清**失败场景**: 执行者照计划字面做了什么 → 得到什么错误结果。
- 对「检查 / 判据」类 finding, 回答「它怎么会红」—— 基线、目标、坏实现三态下各是什么值。
- finding 的 `id` 按 `sha256(f"{category}:{scope}:{severity}:{type}")[:8]` 计算 (category ∈ architecture / implementation / testing / documentation; type ∈ decision / issue / risk; scope 写受影响的文件或任务号, 如 `detailed-tasks.yaml TASK-012`)。

## 硬性纪律

- **只写一个文件**: 你的报告 `/home/dev/Aria/.aria/audit-reports/post_planning-R1-2026-09-17T100518-186Z-pre-merge-completeness-gate-change-scope-qa-engineer.md`。不改被审文件、proposal、源码或任何其他仓内文件。
- 需要实跑时, 只在 `/tmp/claude-1000/-home-dev-Aria/d05b697f-d862-4968-a61c-f7f47c49f946/scratchpad/audit-R1-qa-engineer/` 下操作 (可 `cp -a` 执笔人的副本 `/tmp/claude-1000/-home-dev-Aria/d05b697f-d862-4968-a61c-f7f47c49f946/scratchpad/p199/base/Aria` 到你自己的目录再改; **不得直接改那份共享副本**)。
- 真仓内**不做任何 git 写操作** (commit / push / fetch / pull / checkout / stash / reset / tag / update-ref 一律禁止); 需要远端事实用 `git ls-remote`。不开 issue、不发评论。
- **禁止派子代理 (不得使用 Agent 工具)** —— 同类审计里 fork 子代理曾无视「不要写文件」互相覆盖报告。
- 不要复述计划或 proposal 正文; 报告只写结论与证据。

## 报告格式

报告必须以下列 YAML frontmatter 开头 (字段全填, 不要省略):

```
---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: <你写完报告时的 UTC ISO 8601 毫秒, 如 2026-09-17T10:30:00.123Z>
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---
```

verdict 规则: 有 critical ⇒ FAIL; 无 critical 有 major ⇒ PASS_WITH_WARNINGS; 否则 PASS。

正文依次为:

1. `## 已实读文件` —— 列出读过的文件与范围。
2. `## Findings` —— 表格或分条, 每条: `id` / severity / type / category / scope / 一句话 summary / 证据 / 失败场景 / 建议修法。按 critical → major → minor 排序, 分别编号 (C1 / M1 / m1 …)。
3. `## 对执笔人自报薄弱点的表态` —— (a)(b)(c) 各一句: 可接受 / 不可接受 + 理由。
4. `## 风险 / 疑问` (不计入 finding)。
5. `## Verdict` —— verdict + counts (如 `0C/2M/3m`) + **Vote: PASS 或 REVISE** (有 major 或 critical 即 REVISE)。
6. `## 是否足以开始 Phase B` —— 一句话: 足以 / 不足以 + 理由。

完成后, 你的最终回复只需一行: 报告路径 + verdict + counts + vote。
