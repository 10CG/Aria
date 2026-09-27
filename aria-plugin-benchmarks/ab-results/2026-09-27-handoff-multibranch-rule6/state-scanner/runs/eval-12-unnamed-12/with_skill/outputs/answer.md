下面只依据 state-scanner SKILL.md 的说明回答，没有运行任何命令。依据是「Layer L Phase B 集成」一节的「claim 生命周期闭环」段和「JSON 消费 + surface 渲染」段。

## (1) 传 `--linked-issue 'aria-plugin #152'`：会报出那条 claim

**比较规则**（SKILL.md 原文）：按归一后的 `<repo>#<n>` 比较：
- 仓名只取 `/` 后面的最后一段，**org 前缀不参与比较**；
- 大小写不影响，**各段首尾空白不影响**；
- `.` 和 `_` 当作 `-`；
- 解析不出来的值，退回到原串精确比较。

**套到你这个例子上**：

| 值 | 仓名段 | 编号 | 归一结果 |
|----|--------|------|----------|
| 已有 claim 的 `10CG/aria-plugin#152` | 丢掉 org `10CG`，得到 `aria-plugin` | `152` | `aria-plugin#152` |
| 你传的 `aria-plugin #152` | 本来就没有 org；`#` 前那个空格是仓名段的尾部空白，会被去掉，得到 `aria-plugin` | `152` | `aria-plugin#152` |

两边归一后相同，而你的 track-id（`ci-gate-first-push-fix`）和对方的（`pre-merge-gate-no-run-for-branch`）不同。这正是这个告警要抓的情况：「同一个 issue，两个 track-id」，也就是同一件事被起了两个名字。所以 phase1_gate 输出 JSON 里的 additive 键 `linked_issue_overlap` 会是一个**非空 list**，里面包含 container `023236f2` 的这条 claim。

有个前提要说明：上面的结论假设 `aria-plugin #152` 能按 `<repo>#<n>` 正常解析。按规则，空白只是被去掉，不会导致解析失败，所以它应该能解析。万一解析失败，就会退回原串精确比较，那时 `aria-plugin #152` 和 `10CG/aria-plugin#152` 不相等，就**不会**报出来。

## (2) 传 `10CG/Aria#152`：不会报出那条 claim

`10CG/Aria#152` 归一后是 `aria#152`（丢掉 org，`Aria` 转小写）。已有 claim 归一后是 `aria-plugin#152`。编号都是 152，但仓名段 `aria` 和 `aria-plugin` 不同，所以不算重叠，不会进 `linked_issue_overlap`。

这个结果本身是对的：`10CG/Aria#152` 和 `10CG/aria-plugin#152` 是两个不同仓里的 issue，只是编号碰巧一样。规则只忽略 org 前缀，不会把仓名的前缀部分当成相同。如果传这个值，其他地方没有别的重叠，结果应当是 `linked_issue_overlap == []`，意思是「查过了，没有碰撞」。

## (3) 这个告警会不会阻断你进 Phase B：不会

- SKILL.md 明确写了：linked_issue 重叠是 **advisory 告警**，「渲染为 🔴 提示但不阻断」。
- 能不能进 Phase B 看 `proceed` 字段：`proceed == true`（outcome 是 passed / advisory_proceed / user_takeover / user_override_proceed 之一）就放行。默认 `coordination.mode = advisory`，设计上是「放行 + 写入并推送你自己的 claim + 返回告警」；真正的最终仲裁在 reconcile 阶段，按最早的 `claimed_at` 胜出。
- 你的 track-id 和对方不同，所以这条 claim 也**不会**触发 `surface.kind == "occupied"` 那种「同一个 track 已被认领」的告警。

虽然不阻断，但 🔴 提示值得当真：它说明容器 `023236f2` 在 2026-08-22 已经以 `pre-merge-gate-no-run-for-branch` 为名认领了 `10CG/aria-plugin#152`，状态是 active。进 Phase B 之前，建议先确认你的 `ci-gate-first-push-fix` 和对方是不是在做同一件事，比如读对方的 handoff，或查这个 issue 现在的状态，避免重复劳动。

读输出时还有两点：
- `linked_issue_overlap` 有三种状态，要分开读：键缺席 = 本轮没检测；`[]` = 检测了、没有碰撞；`null` 且 `linked_issue_overlap_error` 不为空 = 这一轮没拿到任何证据，这时要显示成「未能核实，建议重试」，**不能**当成「没有碰撞」。
- `unknown_schema_claims > 0` 表示有 N 条 claim 解析不了，要当作它们存在来处理。注意 `null` 不等于 `0`。

按评测约束，我没有实际运行 phase1_gate。按 skill 流程，你要执行的命令是：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "ci-gate-first-push-fix" --phase B --mode advisory \
  --repo-path "/home/dev/Aria" --linked-issue 'aria-plugin #152'
```
