# GRADER_CRITIQUE — eval-1 basic-state-collection

评分员对两臂 (匿名 X = r01x, Y = r01y) 用同一口径评分。结果: X 3/3, Y 3/3。

## 逐条断言判定

| # | 断言 | 性质 | 说明 |
|---|------|------|------|
| 1 | Output should include Git status information | 实际恒真 | 只要跑了 scan.py 或 git status, 任何状态报告都会写分支和变更。它不核对内容是否正确。本次两臂写的分支 / HEAD / 3 项变更都和 snapshot 一致, 但即使写错了, 按字面也难判失败。 |
| 2 | Should provide workflow recommendation | 实际恒真 | 只问「有没有推荐」, 不问推荐得对不对。两臂都推荐继续 TASK-026, 都给了备选项。 |
| 3 | Output should use structured format with sections | 实际恒真 | SKILL 的输出模板本身就带小节。X 用框线加 emoji 小节, Y 用 `## 1.` 到 `## 10.` 的编号标题, 两种写法都满足。 |

没有恒假的断言。三条都能从 answer.md 核验, 不需要过程证据。

## 两臂差异是否被断言测到

没有测到。两臂的实质差异都在断言覆盖范围之外:

- handoff 过时识别: 两臂都发现本分支 pointer 指向的 09-24 handoff 已经过时, 也都找到 origin/master 上 09-27 的 handoff 并以它为准。X 在 exec_notes 里多跑了 `git ls-tree origin/master -- docs/handoff`。Y 直接引用了 `tracks_multibranch` 在 master 上扫到的三份 handoff 文件名和状态。两臂 snapshot 的 `handoff.latest_path` 相同, 都是 09-24 那份 (都经 pointer 读取)。所以本 eval 看不出新旧 skill 在「多分支 / 子目录 handoff 路径保真」上的行为差别, 而这正是本次改动的目标。
- 心跳 / phase1_gate: 两臂都只写出命令, 没有执行, 并引用 handoff 的成文要求作理由。Y 写的是 `--phase B`, X 写的是 `--phase A.1`, 这个差别没有断言覆盖。
- 深度: X 列出了审计检查点和 16 项自定义检查。Y 读了协调 ref 里的 claim 文件, 核实了心跳时间。这些都不影响得分。

## 建议

新增判别性断言, 例如:
- 「指出本分支 pointer 所指 handoff 已过时, 并定位到 master 上更新的 handoff」
- 「git 变更条目与 snapshot 一致, 3 项, 含 2 个子模块指针偏移」
- 「没有执行 phase1_gate 或刷心跳, 并说明理由」

这样才能测到本次改动面。现有三条断言只能当冒烟底线, 不能作为 Rule #6 的对比依据。
