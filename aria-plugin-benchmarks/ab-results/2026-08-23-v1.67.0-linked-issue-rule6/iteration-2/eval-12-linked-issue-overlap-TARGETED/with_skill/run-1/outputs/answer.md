依据 state-scanner SKILL.md「Layer L Phase B 集成」一节 (claim 生命周期闭环 / Part B1 段落) 的说明回答:

## (1) 会报出来。比较规则是「归一化后的 `<repo>#<n>` 相等」

phase1_gate 的 `--linked-issue` 会把值写进自己的 claim, 并在输出 JSON 里追加 `linked_issue_overlap[]`, 专门抓「同一个 issue 挂在不同 track-id 下」这种同一件事两个名字的情况。比较前两边都先归一成 `<repo>#<n>`, 规则是:

- 仓名只取 `/` 后最后一段, org 前缀不参与比较
- 大小写不影响, 各段首尾空白不影响
- `.` / `_` 视同 `-`
- 解析不出来的值才回落成原串精确比较

套到你的场景:

| 来源 | 原始值 | 归一后 |
|------|--------|--------|
| 对方 claim | `10CG/aria-plugin#152` | `aria-plugin#152` (剥掉 org `10CG/`) |
| 你传的 | `aria-plugin #152` | `aria-plugin#152` (`#` 前的空格属于段首尾空白, 被去掉) |

两者相等, 而你的 track-id `ci-gate-first-push-fix` 和对方的 `pre-merge-gate-no-run-for-branch` 不同, 正好命中「同 issue、不同 track-id」, 那条 active claim 会出现在 `linked_issue_overlap[]` 里, 推荐区渲染为一条红色提示。裸仓名和 `#` 前的空格都不会让它漏报。

## (2) 传 `10CG/Aria#152` 则不会报

`10CG/Aria#152` 归一后是 `aria#152`: 仓名取最后一段 `Aria`, 再大小写不敏感。对方是 `aria-plugin#152`。`aria` 和 `aria-plugin` 是两个不同的仓名 (规则只是把 `.`/`_` 等价成 `-`, 不会把 `aria-plugin` 截成 `aria`), 所以按规则这是两个不同仓库的 #152, 不算重叠, 不会报出那条 claim。

顺带提醒: 这里 #152 实际是 aria-plugin 仓的 issue (对方 claim 写的就是 `10CG/aria-plugin#152`), 你如果真要指同一件事, 传 `aria-plugin#152` 或 `10CG/aria-plugin#152` 才对; 写成 `10CG/Aria#152` 属于仓名写错, 告警恰好因此失效, 而不是「没冲突」。

## (3) 不会阻断

SKILL.md 明确写的是「渲染为红色提示但不阻断」。整个 phase1_gate 在默认的 `advisory` 模式下本来就是放行 + 写推自己的 claim + 回传 surface 告警 (advisory-over-hardlock), `linked_issue_overlap[]` 只是在输出 JSON 上追加的一个 additive 键, 性质同样是提示。是否进 Phase B 看的是 `proceed == true` (outcome 为 passed / advisory_proceed 等), 这个字段不受 linked_issue 重叠影响。真正的仲裁仍是 reconcile 那一层 (最早 claimed_at 胜), 也不是在这里硬挡。

所以: 告警会弹出来让你看见「#152 已经有人在 `pre-merge-gate-no-run-for-branch` 这条轨道上认领了」, 但进不进 Phase B 由你自己决定; 建议先读对方 claim 和 handoff 确认是不是同一件事, 再决定是换 track-id 继续、还是直接接手对方轨道。
