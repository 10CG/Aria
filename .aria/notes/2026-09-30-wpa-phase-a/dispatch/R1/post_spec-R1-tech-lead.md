你是 Aria 仓 (`/home/dev/Aria`) **post_spec convergence 审计第 1 轮** 的 **tech-lead** 席。被审对象是 WP-A Spec `secret-net-l3-and-bypass-paths` 的 proposal **v1** (主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上的提交 `47aa15f`, 未推送)。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 你要审的

- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` (全文)
- 同目录下 proposal 引用的证据文件 (基线探针脚本及其输出; 以目录实际内容为准)

## 审计锚点 (Step 0, 本审计周期不变)

- primary_goal: 补上 secret 防护网在 10CG/aria-plugin#154 / 10CG/aria-plugin#203 / 10CG/Aria#221 暴露的洞 —— L3 (secret-scan.sh) 的 Read 读取失明与键形 / INI 赋值 / 头部参数形缺口、误报白名单与日志指纹, L1 (secret-guard.sh) 的服务端配置文件、项目级扩展入口、路径经 shell 变量间接、进程表列举与两处误拦 —— 维持「检测 + 告警」与「命令拦截」两层架构, 不引入任何安全回退
- in_scope: 方案取舍是否成立 / 范围与 Level 2 是否相称 / 每条 SC 是否可证伪 (基线红、目标绿、坏实现红) / 误报与漏报面 / Rule #6 与 Rule #7 申报 / 文档同步面 / 与在飞轨 (10CG/Aria#199) 的接缝 / 外向动作与 owner 等待点
- out_of_scope: 凭据轮换本身 (owner 2026-09-30 决策单第 2 项: 全部延后、先头脑风暴, 期间不逐条提示); WP-B (10CG/Aria#223 与 10CG/aria-plugin#207); 10CG/Aria#199 本身的内容
- source_sha: `47aa15f`

## 背景事实 (派单时主控实测)

- 四仓 master 两端一致: 主仓 `0748dbc` / aria `268da8f` (aria-plugin v1.74.1) / standards `2bc1c4c` / aria-orchestrator `237045a`。被审提交 `47aa15f` 在分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上, 基于 `0748dbc`。
- 本仓 audit config: `post_spec` / `post_planning` = convergence, `max_rounds` 5; 其余检查点 off。收敛判据 (本仓先例口径): 相邻两轮 Critical+Major 键集相等 且 全票 PASS。
- A.1 认领: track `secret-net-l3-and-bypass-paths-023236f2` @ simonfish/023236f2 (phase1_gate A.1 advisory, 2026-09-30T17:57:13Z, `linked_issue_overlap == []`), 协调 ref 推后 `ls-remote` 核验一致。
- 竞品 Spec 探针 (本轮入口实跑): `sibling_spec_probe.py` status=ok / verdict=no_sibling_found, github 156 份 / origin 161 份 proposal 完整扫描, 无 cap; 本轮已完整扫描, 未发现同 issue 竞品。
- 与双子星的接缝 (主控开工前实测): 双子星 simonfish/bfe8285d 在做 10CG/Aria#199 (尚未开 B.1 分支); 它的计划不改任何 hooks 文件, 只断言 `aria/hooks/hooks.json` 与 `.aria/config.json` 不含字面 `completeness_gate`; 两轨都要改 aria 发版文件, 按「串行发版、取号前协商」处理。
- 执笔: v1 由新派的 tech-lead 执笔实例出稿 (读 agent team 四份研究笔记 + 主控范围裁定), 主控独立核验: 结构化输出与执笔母本逐字节一致; 在 aria 268da8f + standards 2bc1c4c 的新副本上连跑两次 baseline_probe.py, stdout 与 baseline-evidence.md 内嵌输出逐字节相同 (sha256 前 16 位 1ab63a323da13f45, 41873 字节), 基线形态 holds; 头部四行、Linked Issue 探针、裸引用检查、带圈数字均过。执笔自报薄弱点与待 owner 复议项写在 proposal 的「执笔自报薄弱点」与「待 owner 复议」两节 —— 请逐条明确表态 (可接受 / 不可接受 + 理由), 不要当作「新发现」重复报。
- 本轮是第 1 轮, 审全文。

## 必读

1. 被审文件全文 (proposal.md 与它引用的证据文件)。
2. 三个 issue 的正文与全部评论: `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-154.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-203.md`、`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/Aria-221.md`。
3. owner 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` (全文)。
4. `CLAUDE.md` 的不可协商规则 #6 / #7 / #10 与「多远程推送 — 两条硬约束」。
5. 你的视角需要的源码与规范 (`aria/hooks/secret-guard.sh`、`aria/hooks/secret-scan.sh`、`aria/hooks/hooks.json`、`aria/hooks/tests/`、`standards/conventions/secret-hygiene.md`、`standards/conventions/skill-benchmark-exemption.md` 等; 实读, 引用 `file:line` 以你实读为准)。
6. 主控整理的四份研究笔记 (背景材料, 不是被审对象; 与源码冲突时以源码为准): `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/` 下的 `secret-guard.md`、`secret-scan.md`、`precedent.md`、`cc-hooks.md`。

## 你的视角

分层职责与方案取舍。L1 (PreToolUse 命令拦截, secret-guard.sh) 与 L3 (PostToolUse 输出检测, secret-scan.sh) 的分工是否清楚: 哪些缺口在 L1 补, 哪些承认 L1 按命令文本结构上堵不住而交给 L3, 两层判据是否互相矛盾; 进程表列举选「拒绝 / 要求配脱敏过滤 / 改写命令 (PreToolUse updatedInput)」的取舍是否有平台事实支撑; 项目级扩展入口的形态、读取失败时 fail-open 还是 fail-closed; 范围与 Level 2 是否相称 (有无该拆出去的); 版本定级 (PATCH / MINOR) 与发版面、与 10CG/Aria#199 串行发版的接缝; 有没有被遗漏的同族旁路 (例如进程环境 /proc/<pid>/environ、其他服务的含密配置文件)。

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
- 需要实跑时, 只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R1-tech-lead/` 下操作: 先 `cp -a /home/dev/Aria/aria` (以及需要的话 `cp -a /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths`) 到你的目录再跑; 运行 hook 时把 HOME 指向你目录下的 `home/`。
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
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: <你写完报告时的 UTC ISO 8601 毫秒, 如 2026-09-30T20:30:00.123Z>
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
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
