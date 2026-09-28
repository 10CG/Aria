下面只依据 state-scanner 的 SKILL.md 回答（「Layer L Phase B 集成」一节里的「claim 生命周期闭环」和「JSON 消费 + surface 渲染」两段），没有运行任何命令。

## (1) 传 `--linked-issue 'aria-plugin #152'`：会报出来

**会。** 这条 claim 会出现在 `linked_issue_overlap[]` 里。

**比较规则**（SKILL.md 原文）：`--linked-issue` 的重叠检测找的是「同一个 issue、不同 track-id」，也就是「同一件事起了两个名字」。两边的值都先归一成 `<repo>#<n>` 再比较：
- 仓名只取最后一个 `/` 之后的那一段，**org 前缀不参与比较**
- 不区分大小写，每一段首尾的空白都忽略
- `.` 和 `_` 都当成 `-`
- 解析不出来的值，退回用原字符串精确比较

套到你的情况上：

| 值 | 归一过程 | 归一结果 |
|----|----------|----------|
| 你传的 `aria-plugin #152` | 没有 `/`，仓名就是 `aria-plugin `；去掉 `#` 前段末尾的空格 | `aria-plugin#152` |
| 已有 claim 的 `10CG/aria-plugin#152` | 丢掉 org `10CG/`，取 `aria-plugin` | `aria-plugin#152` |

两边归一后相等。track-id 也不一样（你的是 `ci-gate-first-push-fix`，对方是 `pre-merge-gate-no-run-for-branch`），而且对方 `status: active`，正好是这条告警要抓的「同一件事两个名字」。所以漏写 org 前缀、`#` 前多一个空格，都不影响命中。

说明：这条 claim 的 `claimed_at` 是 2026-08-22，已经一个多月了。如果在这期间它被 `--sweep-stale` 扫成了 `abandoned`（心跳超过 STALE_TTL），就不再是 active。SKILL.md 没有写清楚非 active 的 claim 是否参与重叠比较，只提到有 `--include-terminal` 这个开关。按你给的内容（`status: active`），它会被报出来。

## (2) 改传 `10CG/Aria#152`：不会报出来

归一后是 `aria#152`（丢掉 org `10CG`，`Aria` 转成小写）。它和 `aria-plugin#152` 的仓名不同，所以不算重叠。org 前缀本来就不参与比较，要比的是仓名，而 `Aria` 和 `aria-plugin` 是两个仓。

这个结果是对的：`Aria#152` 和 `aria-plugin#152` 本来就是两个不同的 issue。反过来也要提醒：如果你这条轨道实际做的就是 aria-plugin#152，却写成了 `10CG/Aria#152`，那么这次碰撞会被**静默漏掉**，重叠检测没办法替你纠正仓名写错。

## (3) 会不会阻断进 Phase B：不会

SKILL.md 写的是：`linked_issue_overlap` 属于 advisory 告警，「渲染为 🔴 提示但不阻断」。能不能进 Phase B 只看 phase1_gate 输出里的 `proceed`：`proceed == true`（outcome 是 passed / advisory_proceed / user_takeover / user_override_proceed 之一）就放行。默认 `mode=advisory` 的做法是放行、写入并推送自己的 claim、同时返回告警。最终谁胜出，由 reconcile 按最早的 `claimed_at` 来定。

但「不阻断」不等于「可以不管」。看到这条 🔴 之后，应该先确认两条轨道是不是在做同一件事，再决定是合并、让路，还是继续。另外有两点要注意：
- 这条 claim 的 track-id 和你的不同，所以它不会触发 `surface.kind == "occupied"`（那个是同一个 carry-id 被别人认领时才出的告警）。你看到的只会是 linked-issue 重叠这一条。
- 如果输出里 `linked_issue_overlap` 是 `null`，同时 `linked_issue_overlap_error` 不为空，意思是**这一轮没能核实**，应该显示「未能核实，建议重试」，不能当成「没有碰撞」。`[]` 才表示检测过了、确实没有碰撞；这个键不存在则表示没传 `--linked-issue`、没做检测。

另外，按 SKILL.md，phase1_gate 由 AI 编排层在你确认进 Phase B 之后调用，前提是 `coordination.enabled`（默认 true）为真，并且 snapshot 里 `tracks_multibranch.collision.kind` 不为空。你要执行的命令大致是（本次没有运行）：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "ci-gate-first-push-fix" --phase B --mode advisory \
  --repo-path "/home/dev/Aria" --linked-issue 'aria-plugin #152'
```
