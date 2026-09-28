# eval-2 user-options-display 评分员意见

两臂 (匿名 X / Y) 都是 2/2 通过。

## 逐条断言

1. `Should show numbered options for user selection`: **恒真**
   - 两臂都输出 [1]~[4] 四个编号选项, 并以「选择 [1-4]」收尾。
   - skill 的 output-formats 模板本身就规定了 `[N]` 编号格式, 只要照模板输出就会通过。
   - 断言只看有没有编号, 不看选项内容是否与 snapshot / handoff 的实际状态相符。
2. `Should mention custom input option`: **恒真**
   - 模板固定含「[N] 自定义组合」一行和「或输入自定义」提示, 两臂都照抄了。
   - 区分度为零。

没有恒假的断言, 也没有「无法从产出核验」的断言; 两条都能直接从 answer.md 核验。

## 两臂差异是否来自断言测得到的东西

否。两臂在断言层面完全一样 (都是 2/2)。实际差异都在断言测不到的地方:

- **handoff 事实正确性**
  - X 发现工作树的 `latest.md` 落后, 用 `git show origin/master:` 读到了 09-27 的最新 handoff。经核验, 这是对的。
  - Y 只读了工作树里的 handoff, 断言「09-25 以后 10CG/Aria#195 的进度只记在台账里，没有对应的 handoff」。这是错的: origin/master 上已有 `2026-09-27-session-close-195-task025-legacy-issue-204.md`。
- **推荐内容**: 两臂的 [1] 都是 TASK-026 AB, [2] [3] 则不同。
  - X 的 [2] 是「刷心跳 → TASK-027」, [3] 是「续做 US」。
  - Y 的 [2] 是「进 Phase C」, [3] 是「10CG/Aria#199 待裁项 + 补 handoff」。
  - Y 额外提示「AB 可能落到未被有效测试, 需 owner 裁定」。
  - X 额外指出「AB 会话 (NO_PUSH=1) 按 handoff 应跳过心跳」。
- **入口心跳命令**: 两臂都只写出命令、没有执行, 这是评测约束所致, 不扣分。
- **只读**: 两臂都满足只读。Y 说明 scan.py 的 remote_refresh 按设计会 fetch refs。

## 建议

- 本 eval 的两条断言只测格式, 对任何 state-scanner 版本 (包括 collector 改坏的版本) 都会通过, 不能作为 Rule #6 的区分信号。
- 如果要测本轨 (handoff 多分支 / 子目录路径保真) 的改动, 应加事实类断言。例如: 「当工作树 latest.md 落后于 master 时, 回答指出最新 handoff 并以其为推荐依据」。
- 可再加一条: 「推荐项与 snapshot 中的 active claim / 下一任务一致」。
