依据 state-scanner SKILL.md「claim 生命周期闭环 (Part C)」一段对 `--linked-issue` 的说明 (未跑命令、未读源码):

**比较规则原文要点**: `phase1_gate --linked-issue` 会把值写入 claim, 并在输出 JSON 追加 additive 键 `linked_issue_overlap[]`, 用于报「同 issue、不同 track-id」的"同一件事两个名字"告警。比较方式: **按归一后的 `<repo>#<n>` 比较, org 不参与**; **不可解析的值回落为原串精确比较**。告警渲染为 🔴 提示, **不阻断**。

**(1) 传 `aria-plugin #152` 会不会报出那条 claim?**

取决于这个带空格的裸仓名能否被解析, 分两种情况:

- 如果解析器能把 `aria-plugin #152` 识别为 repo=`aria-plugin`、n=152, 那它归一成 `aria-plugin#152`; 对方 claim 的 `10CG/aria-plugin#152` 去掉 org 后同样是 `aria-plugin#152` → 两者相同, 而 track_id 不同 (`ci-gate-first-push-fix` vs `pre-merge-gate-no-run-for-branch`) → **会报** 到 `linked_issue_overlap[]`。org 有没有 (`10CG/`) 不影响结果, 因为规则明说 org 不参与比较。
- 如果 `#` 前的空格让它成为"不可解析值", 就退回原串精确比较: `aria-plugin #152` 与 `10CG/aria-plugin#152` 字面不等 → **不会报**。

SKILL.md 没有写明空格是否被容忍, 所以单凭 skill 文本无法百分之百断定走哪条路。稳妥做法: 去掉空格, 写 `aria-plugin#152` 或 `10CG/aria-plugin#152`, 这样一定走归一路径, 一定会被报出来。

**(2) 传 `10CG/Aria#152` 呢?**

归一后是 `Aria#152`, 对方是 `aria-plugin#152`, repo 名不同 → **不会报**。org 相同、issue 号相同都不够, 判据是 repo + 编号都一致; 而 `Aria` 和 `aria-plugin` 本来就是两个不同仓库 (主仓 vs 插件仓), 不算同一个 issue。

**(3) 这个告警会阻断进 Phase B 吗?**

**不会**。SKILL.md 明说它是 advisory 告警, "渲染为 🔴 提示但不阻断"。放行与否由 `proceed` / `outcome` 决定 (默认 `mode=advisory`: 放行 + 写推自己的 claim + surface 告警); `linked_issue_overlap[]` 只是额外追加的 additive 键, 提醒你和 023236f2 那个容器可能在用两个 track-id 做同一件事 (#152), 要不要合流由你判断。
