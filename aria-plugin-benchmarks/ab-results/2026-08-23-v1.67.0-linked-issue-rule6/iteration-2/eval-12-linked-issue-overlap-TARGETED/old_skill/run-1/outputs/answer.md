依据 state-scanner skill 的 SKILL.md (以及 references/layer-l-integration.md、docs/coordination-ref-schema.md) 的文字回答, 未跑命令、未读 lib/ 源码。

## (1) 传 `--linked-issue 'aria-plugin #152'` 会不会把那条 claim 报出来? 比较规则是什么?

**说明文档里没有写出比较规则, 所以我无法从 skill 文本断言"一定会"或"一定不会"。**

SKILL.md 对这个功能只有一句话 (Layer L Phase B 集成一节, Part B1):

> phase1_gate 另支持可选 `--linked-issue` (Part B1): 写入 claim 并在输出 JSON 追加 additive 键 `linked_issue_overlap[]` — 同 issue 不同 track-id 的「同一件事两个名字」advisory 告警, 渲染为 🔴 提示但不阻断。

能确定的只有这些:
- 告警的触发语义是 **"同一个 issue + 不同 track-id"**。你的 track-id `ci-gate-first-push-fix` 和对方的 `pre-merge-gate-no-run-for-branch` 确实不同, 这一半条件满足。
- 另一半"是否算同一个 issue", 取决于你传的 `aria-plugin #152` 这种写法 (裸仓名、无 org 前缀、`#` 前带空格) 和 claim 里的 `10CG/aria-plugin#152` 会不会被视为相等。**SKILL.md 和 references/ 对 linked_issue 的归一化 (大小写、空格、org 前缀补全、仓名缩写) 只字未提。** 文档里唯一提到归一化的是 track_id (`derive()`: 小写 → `/._` 换成 `-` → 截 64 字符), 那是针对 track_id 的, 不适用于 linked_issue。

所以老实的结论: 如果实现做的是**字面串精确比较**, `aria-plugin #152` 和 `10CG/aria-plugin#152` 不相等, 这条 claim **不会**被报出来 (同一件事被两个名字漏过); 如果实现做了归一化 (去空格、补 org、按仓名+号码比), 则会报。文档不足以裁定, 要确认得读 `lib/` 源码或实跑 — 按你的约束我没做。**保险做法是照 claim 里已有的写法原样传 `10CG/aria-plugin#152`**, 两种实现下都能命中。

## (2) 如果传的是 `10CG/Aria#152` 呢?

这是**另一个仓库的 #152** (主仓 10CG/Aria 的 issue 152, 不是 10CG/aria-plugin 的 152)。即便实现做了归一化, 只要比较的是"仓 + 号码"而不是只看号码, 它和 `10CG/aria-plugin#152` 也是两个不同的 issue, **不应当**被报为重叠。如果它被报了出来, 那说明实现只比了号码 (`#152`), 那是误报, 值得提 issue。同样, 文档没写, 这是按"同 issue"字面语义的推断。

## (3) 这个告警会阻断我进 Phase B 吗?

**不会。** SKILL.md 明确写了两层:
- `linked_issue_overlap[]` 是 additive 键, 性质是 **advisory 告警, "渲染为 🔴 提示但不阻断"**。
- 整个 phase1_gate 在生产默认 `mode=advisory` 下的语义是 "放行 + 写推自己 claim + 返回 surface 告警" (advisory-over-hardlock); 只要输出 JSON 的 `proceed == true` (outcome ∈ passed / advisory_proceed / user_takeover / user_override_proceed), 就进 Phase B。最终仲裁交给 reconcile (earliest claimed_at 胜), 那是之后 fetch 时的事。

另外提醒: 那条 active claim 的 track_id 与你的不同, 但同属 owner simonfish 且是另一个容器, 会落入 `tracks_multibranch.collision.kind` 的 self_multi_container 场景, 同样是 advisory surface (🔴 occupied 提示, 回显对方 carry-id 供 copy), 也不阻断。真正会让 CLI 退化为 abort 的只有显式配置 `state_scanner.coordination.mode = block`, 默认不是。
