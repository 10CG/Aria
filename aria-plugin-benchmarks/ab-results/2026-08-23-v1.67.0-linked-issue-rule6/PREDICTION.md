# 测前预期 (在看到任何结果之前写下)

**被测 hunk**: `skills/state-scanner/SKILL.md:176` 括注 —— 「(按归一后的 `<repo>#<n>` 比较, org 不参与; 不可解析值回落原串精确比较)」。
**新版** aria `0fe2e0d` (feature/linked-issue-normalization) vs **基线** `9e6a17c` (v1.66.4)。

| eval | 预期 delta | 依据 |
|---|---|---|
| 1-11 (既有套件) | **全部无 delta** | 11 条 eval 没有一条触及 Layer L claim / `--linked-issue` 段; hunk 只改这一段的一个括注 |
| 12 定向 (linked_issue 跨格式重叠) | **应有 delta** | 旧版只说「同 issue 不同 track-id」, 未说明怎么算「同 issue」; 新版明写归一键 + org 不参与 + 回落规则 |

## 可证伪点

- **若 eval-12 无 delta** ⇒ 两种可能: (a) 旧版模型凭常识也答「会归一比较」—— 则括注价值下调, 但实现已由 SC 测试钉住, 不影响 ship; (b) 新版也没答对 ⇒ 括注措辞没传达到, 须改写后重跑。
- **若 eval-1..11 出现 delta** ⇒ 有未预料外溢或 flaky, 须逐条查 (预期为 0)。
- 旧版在 eval-12 上最可能的失败形态: 把 `10CG/aria-plugin#152` 与 `aria-plugin #152` 判为「不同 issue 字符串 ⇒ 不会告警」, 或不确定; 以及把 `10CG/Aria#152` (不同仓) 误判为重叠。
