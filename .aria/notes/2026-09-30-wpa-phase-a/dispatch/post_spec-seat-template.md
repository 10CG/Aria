你是 Aria 仓 (`/home/dev/Aria`) **post_spec convergence 审计第 {ROUND} 轮** 的 **{ROLE}** 席。被审对象是 WP-A Spec `secret-net-l3-and-bypass-paths` 的 proposal **{VERSION}** (主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上的提交 `{SHA}`, 未推送)。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 你要审的

- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` (全文)
- 同目录下 proposal 引用的证据文件 (基线探针脚本及其输出; 以目录实际内容为准)

## 审计锚点 (Step 0, 本审计周期不变)

- primary_goal: {PRIMARY_GOAL}
- in_scope: 方案取舍是否成立 / 范围与 Level 2 是否相称 / 每条 SC 是否可证伪 (基线红、目标绿、坏实现红) / 误报与漏报面 / Rule #6 与 Rule #7 申报 / 文档同步面 / 与在飞轨 (10CG/Aria#199) 的接缝 / 外向动作与 owner 等待点
- out_of_scope: 凭据轮换本身 (owner 2026-09-30 决策单第 2 项: 全部延后、先头脑风暴, 期间不逐条提示); WP-B (10CG/Aria#223 与 10CG/aria-plugin#207); 10CG/Aria#199 本身的内容
- source_sha: `{SHA}`

## 背景事实 (派单时主控实测)

- 四仓 master 两端一致: 主仓 `0748dbc` / aria `268da8f` (aria-plugin v1.74.1) / standards `2bc1c4c` / aria-orchestrator `237045a`。被审提交 `{SHA}` 在分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上, 基于 `0748dbc`。
- 本仓 audit config: `post_spec` / `post_planning` = convergence, `max_rounds` 5; 其余检查点 off。收敛判据 (本仓先例口径): 相邻两轮 Critical+Major 键集相等 且 全票 PASS。
- A.1 认领: track `secret-net-l3-and-bypass-paths-023236f2` @ simonfish/023236f2 (phase1_gate A.1 advisory, 2026-09-30T17:57:13Z, `linked_issue_overlap == []`), 协调 ref 推后 `ls-remote` 核验一致。
- 竞品 Spec 探针 (本轮入口实跑): {SIBLING}
- 与双子星的接缝 (主控开工前实测): 双子星 simonfish/bfe8285d 在做 10CG/Aria#199 (尚未开 B.1 分支); 它的计划不改任何 hooks 文件, 只断言 `aria/hooks/hooks.json` 与 `.aria/config.json` 不含字面 `completeness_gate`; 两轨都要改 aria 发版文件, 按「串行发版、取号前协商」处理。
- 执笔: {WRITER_NOTE}
{ROUND_CONTEXT}

## 必读

1. 被审文件全文 (proposal.md 与它引用的证据文件)。
2. 三个 issue 的正文与全部评论: `{SP}/issues/aria-plugin-154.md`、`{SP}/issues/aria-plugin-203.md`、`{SP}/issues/Aria-221.md`。
3. owner 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` (全文)。
4. `CLAUDE.md` 的不可协商规则 #6 / #7 / #10 与「多远程推送 — 两条硬约束」。
5. 你的视角需要的源码与规范 (`aria/hooks/secret-guard.sh`、`aria/hooks/secret-scan.sh`、`aria/hooks/hooks.json`、`aria/hooks/tests/`、`standards/conventions/secret-hygiene.md`、`standards/conventions/skill-benchmark-exemption.md` 等; 实读, 引用 `file:line` 以你实读为准)。
6. 主控整理的四份研究笔记 (背景材料, 不是被审对象; 与源码冲突时以源码为准): `{SP}/research/` 下的 `secret-guard.md`、`secret-scan.md`、`precedent.md`、`cc-hooks.md`。

## 你的视角

{FOCUS}

## 严重度口径 (统一, 请照此分级)

- **critical**: 照 Spec 实现会造成安全回退 (现有的拦截或检出变成放行), 或造成难以撤销的外向后果 (泄密、误推、覆盖他人工作), 或 Spec 自身的验收会放过一个错误实现。
- **major**: 照 Spec 字面实现会卡死 (无合法下一步)、得出不可证伪 / 恒绿 / 恒红的验收结论、漏掉某个必做项 (SC / 文档同步面 / Rule #6 申报 / owner 门 / 外向动作登记), 或与 SOT (issue 诉求、决策单、CLAUDE.md、源码事实、Claude Code hook 平台事实) 矛盾; 或方案取舍存在明确更优且不扩大范围的替代, 而 Spec 没有论证为什么不选。
- **minor**: 措辞、引用精度、可读性, 不改变实现者会做什么。
- 一条 finding 若**不影响「实现者会不会做错 / 做漏 / 卡住」也不影响安全效果**, 最高只能是 minor。

## 证据要求

- 每条 finding 必须附**你亲自核验的证据**: `file:line` 实读原文片段, 或你实跑的命令与输出 (输出可截断, 不得改写)。无证据的推测写进「风险 / 疑问」, 不计入 finding。
- 每条 finding 写清**失败场景**: 实现者照 Spec 字面做了什么 → 得到什么错误结果。
- 对「检查 / 判据 / SC」类 finding, 回答「它怎么会红」—— 基线、目标、坏实现三态下各是什么值。
- finding 的 `id` 按 `sha256(f"{category}:{scope}:{severity}:{type}")[:8]` 计算 (category ∈ architecture / implementation / testing / documentation; type ∈ decision / issue / risk; scope 写受影响的节或文件, 如 `proposal.md SC-3` 或 `proposal.md What.W4`)。

## 硬性纪律

- **不写任何文件**: 你的报告作为你的最终输出返回 (结构化输出的 `report_markdown` 字段放报告全文), 由主控原样落盘。不改被审文件、源码或任何其他仓内文件。
- 需要实跑时, 只在 `{SP}/audit/post_spec-R{ROUND}-{ROLE}/` 下操作: 先 `cp -a /home/dev/Aria/aria` (以及需要的话 `cp -a /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths`) 到你的目录再跑; 运行 hook 时把 HOME 指向你目录下的 `home/`。
- 真仓内**不做任何 git 写操作** (commit / push / fetch / pull / checkout / switch / stash / reset / tag / update-ref 一律禁止); 需要远端事实用 `git ls-remote`。不开 issue、不发评论。
- **禁止派子代理 (不得使用 Agent 工具)**。
- **Rule #7**: 不读取、不打印任何真实凭据; 需要「像凭据的值」时在 Python 进程内用 `secrets` 模块运行时生成, 经 stdin 喂给 hook (`capture_output=True`), 绝不打印该值; 报告里只写退出码 / 是否告警 / 命中规则等元数据, 讨论形状时用占位写法。
- 不要复述 proposal 正文; 报告只写结论与证据。

## 报告格式

报告必须以下列 YAML frontmatter 开头 (字段全填, 不要省略):

```
---
checkpoint: post_spec
mode: convergence
rounds: {ROUND}
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: <你写完报告时的 UTC ISO 8601 毫秒, 如 2026-09-30T20:30:00.123Z>
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [{ROLE}]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---
```

verdict 规则: 有 critical ⇒ FAIL; 无 critical 有 major ⇒ PASS_WITH_WARNINGS; 否则 PASS。

正文依次为:

1. `## 已实读文件` —— 列出读过的文件与范围。
2. `## Findings` —— 每条: `id` / severity / type / category / scope / 一句话 summary / 证据 / 失败场景 / 建议修法。按 critical → major → minor 排序, 分别编号 (C1 / M1 / m1 …)。
3. `## 对执笔人自报薄弱点与请裁项的表态` —— 逐条: 可接受 / 不可接受 + 理由 (没有则写「无」)。
4. `## 风险 / 疑问` (不计入 finding)。
5. `## Verdict` —— verdict + counts (如 `0C/2M/3m`) + **Vote: PASS 或 REVISE** (有 major 或 critical 即 REVISE)。
6. `## 是否足以进入 A.2` —— 一句话: 足以 / 不足以 + 理由。

结构化输出的其余字段 (verdict / counts / vote / findings) 必须与 `report_markdown` 正文逐条一致。
