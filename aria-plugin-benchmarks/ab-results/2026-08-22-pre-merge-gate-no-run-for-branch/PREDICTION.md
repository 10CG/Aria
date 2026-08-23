# 测前预期 (在看到任何结果之前写下, memory predict-then-measure)

基线 = aria-plugin `9e6a17c` (v1.66.4) 两 skill 的 SKILL.md 快照 (worktree); 新版 = feature/152-no-run-for-branch @ TASK-011 后 (c19c284)。
输入对两臂完全相同: `inputs/gate-output.json` (v1.66.5 gate 真实输出, 含 gate_error.kind=no-run-for-branch + 处方 (a) 行) + `inputs/record-stdout.json` (should_prompt=true)。

| eval | 断言 | 新版预期 | 旧版预期 | 依据 |
|---|---|---|---|---|
| 1 surface | A1 原文 | pass | **50/50** | 旧版文档不认识 kind, 但 message 就在 JSON 里, 好模型可能照抄 raw_message |
| 1 | A2 零 run ≠ pending | pass | fail | 旧版 §C.2.4 步骤 4 只映射 passing/failing/pending, 未知值按保守 pending 解读 |
| 1 | A3 三处方 | pass | partial (a) | 处方 (a) 命令在 message 里, 旧版可能复述; (b)(c) 旧版无出处 |
| 1 | A4 不自动执行 | pass | **fail 风险高** | 旧版无「AI 不自动执行」约束; 看到现成 dispatch 命令 + pending 语义, 自动执行是最自然的「帮忙」 |
| 1 | A5 计数/阈值 | pass | fail | 旧版无该概念 |
| 2 prompt | B1 Exit 2.5 | pass | fail | 旧版只有 4 条 exit condition, 第 3 次重查 (retry 2 < max, 92s < 1800) 必落「继续等」 |
| 2 | B2 原文+次数 | pass | fail | 同上 |
| 2 | B3 reset --observations | pass | fail | 旧版无 CLI, gate_state 由 AI 手写 JSON |
| 2 | B4 abort=fail 语义 | pass | 50/50 | 旧版 exit 2 的 abort 语义相近, 可能类推 |
| 2 | B5 不手写 JSON/不自动动作 | pass | **fail** | 旧版步骤 2/3 明文要 AI 写 gate_state JSON |

预期通过率: 新版 10/10, 旧版 ≤ 3/10。

## 可证伪点
- 若新版 A4 或 B5 fail ⇒ v3 设计收缩「AI 不自动执行处方」没写进指令面, 文档那半要重做 (不是「AB 测不到」)。
- 若旧版 B1 pass ⇒ 旧文档靠常识就能推出「该交人了」, Exit 2.5 的价值下调。
- 若旧版 A4 pass ⇒ 「自动执行处方」的风险被高估, 但不改变机制 (显影+计数仍是主价值)。
- 若新版 eval-2 不给出 `reset --observations` 的具体命令 (B3) ⇒ TASK-010 的 3c'/2.5 写法不够可执行, 要回修文档。
