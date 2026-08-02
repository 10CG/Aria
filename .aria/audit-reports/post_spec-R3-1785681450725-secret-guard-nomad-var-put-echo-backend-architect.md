---
verdict: REVISE
agent: backend-architect
round: R3
critical_count: 0
major_count: 1
minor_count: 0
r2_resolved: 2/2
---

# post_spec R3 审计报告 — secret-guard-nomad-var-put-echo (convergence, 收敛终验)

## 审计对象与方法

`/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`（owner 裁定缩到最小范围后版本：零豁免、仅一条新 pattern）。方法：在 scratchpad 建真实 688 行 `secret-guard.sh` 的补丁副本（唯一改动 = 按 §What 2 原文插入新 pattern 于 `:406` 相邻位置），用与生产 hook 完全一致的调用形态（`jq -n '{tool_name:"Bash", tool_input:{command:$c}}' | hook`）逐条实测，不修改仓库任何文件。

## 任务 1 — R2 两条 Major 处置核验

**M-1（`$pattern_hint` unbound）— 确认完全归零**：proposal 全文 grep `pattern_hint` 仅剩 2 处，均在"不做/转出"语境（§What 5 决策行 + §转出 5），且转出条目原文引用了我 R2 的实测结论（"未初始化会让**全部** BLOCKED 文案崩成 unbound variable"）。本版**不改任何提示文案**，heredoc 代码路径零改动 ⇒ R2 发现的 nounset 崩溃面在结构上不存在触发条件（没有新赋值语句，也没有新的条件分支进入该 heredoc）。判定：解决，且是最强形态的解决（不是"修好了"而是"改动面消失了"）。

**M-2（stderr 撤销规则误伤 `grep -v`）— 确认已转出，关键警告完整保留**：§转出 2 原文：「**注意**: 修法须锚定 curl 语境, 裸扫 `-v` 会撞既有 `grep -v` credit (R2 backend M-2)」——与我 R2 报告的核心结论（"检测锚定到同一个 curl 调用内，而非裸 `-v`/`--trace` token 扫描"）语义一致，且明确点名来源（R2 backend M-2），避免未来实现者重新踩坑时无迹可寻。判定：解决。

**r2_resolved: 2/2**。

## 任务 2 — 唯一生产改动技术复核

对象：`nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)`，用 `[[ "$command" =~ $pat ]]`（与 L648-654 生产代码完全一致的匹配机制，非子进程 `grep`）在补丁副本上实测。

- **尾边界有效性**：`nomad var putty foo` → exit=0（不误配，R1 m-2 场景确认已堵）；`nomad var put path/x @f` → exit=2（真实调用仍被拦）；`nomad var put` 后接空白或行尾均命中，接非空白非行尾（如引号字符）不命中——边界语义与 §What 2 描述完全一致。
- **与既有 140 条交叠/遮蔽**：把 141 条 pattern（含新增）整体载入独立 bash 会话，对 5 条 `nomad var put` 系测试命令逐条过全量数组扫描，**仅新 pattern 命中，其余 140 条无一命中**——不存在遮蔽，`[secret-guard] BLOCKED: ... Matched pattern: $pat` 消息在 nomad-put 场景下必然精确指向新 pattern 本身，不受循环遍历顺序或"首次命中即 exit"语义影响（因为压根没有第二个候选）。
- **数组字面量安全性**：单引号包裹、无内嵌单引号/反斜杠，补丁副本可正常被 bash 解析执行（多次实测无语法错误），无转义顾虑。
- **`:406` 相邻位置的匹配顺序影响**：确认为零——由上一条"零交叠"结论直接推出，插入位置只影响代码可读性分组，不影响任何命中/放行/消息归属语义。

判定：技术实现正确，无缺陷。

## 任务 3 — SC-2 四个安全形态逐条实测（零豁免后的唯一出路）

在补丁副本上按 SC-2 原文逐条实跑：

| 形态 | 命令 | 结果 | 符合 SC-2 预期 |
|------|------|------|------|
| `>/dev/null` | `nomad var put path/x @f >/dev/null` | exit=0 | 是 |
| `-o /dev/null` | N/A（curl 专用，SC-2 原文已标注跳过） | — | 是（正确跳过） |
| `&>/dev/null` | `nomad var put path/x @f &>/dev/null` | exit=0 | 是 |
| `-out=none` + `>/dev/null` | `nomad var put -out=none path/x @f >/dev/null` | exit=0 | 是 |

零豁免设计下 `has_filter` credit 确实完全覆盖 SC-2 声称的四个（实为三个可测）安全出路，无一失效。同时复核 SC-1（五条改后 exit=2）与 SC-6（读向 `get`/`list` 不回归、`jq 'keys'` credit 仍生效）：**全部实测通过**，与 proposal 描述一致。

## 任务 4 — 缩范围是否引入新问题：**发现一条新 Major**

### SC-4 三条 FP 示例命令，实测与 proposal 声称不符（2/3 不可复现）

proposal SC-4 原文断言 `grep -rn 'nomad var put' aria/` / `echo "改用 nomad var put"` / `git commit -m "fix: nomad var put 回显"` 三条 **改后均 exit=2**（"本 spec 接受该 FP"）。用与真实 Bash 工具调用完全一致的形态（引号是命令字符串的一部分，非 shell 解释后再传入 hook）逐条实测：

```
grep -rn 'nomad var put' aria/       → exit=0   (声称 exit=2, 实测不符)
echo "改用 nomad var put"            → exit=0   (声称 exit=2, 实测不符)
git commit -m "fix: nomad var put 回显" → exit=2   (声称 exit=2, 实测相符)
```

**根因**：R1 m-2 修复引入的尾边界 `([[:space:]]|$)` 要求 "put" 后紧跟空白或行尾。前两条示例里 "put" 后紧跟的是引号字符（`'` / `"`），既非空白也非字符串真正的行尾（引号后还有更多字符）——不满足边界条件，pattern 不命中，故不拦截。第三条示例里 "put" 后是空格（引号内还有更多文字），满足边界，命中拦截。

**连带发现**：proposal 用以论证"非新增行为类别"的对照论据也不严谨。既有 `(get|list)` 条**没有尾边界**，同样的引号包裹写法确实会拦（实测 `grep -rn 'nomad var get' aria/` → exit=2）；但新 `put` 条因为多了尾边界，同构写法反而**不拦**。也就是说新旧两条 pattern 的 FP 触发面并不对称——新 pattern 的 FP 面比 `(get|list)` 窄，"故非新增行为类别"这一句的"同一类"表述不够精确（方向上更安全，但与 SC-4 具体断言矛盾）。

**风险路径（为何判 Major 而非 Minor）**：Tasks 1.2 要求"先记录每条 baseline exit code, 再实现"。若实现者照抄 SC-4 三条示例逐字写断言（`want=2` × 3），前两条会在实现后立即测红——这不是静默地雷（会被立刻测出），但测红后存在具体的回归诱因：为了让这两条"看起来应该被拦"的 FP 示例真的 exit=2，实现者可能被诱导去**削弱刚由 R1 m-2 钉死的尾边界**（例如去掉 `$` 分支或整体放宽匹配），这会重新放开 `nomad var putty` 之类的误配——恰好重开 R1 m-2 已解决的那个 Major。这是"文本断言 vs 已修复安全边界"两者互相拉扯的具体路径，不是抽象担忧。

**建议**（纯文本修正，不涉及范围/设计返工）：
1. Tasks 1.2 落地前修正 SC-4：要么改用真正会触发边界（"put" 后紧跟空白/行尾）的示例（如去掉包裹引号，或在引号内 "put" 后补一个字符），要么如实拆分三条各自的预期结果（前两条 exit=0、第三条 exit=2），不要三条统一断言 "改后 exit=2"。
2. 建议在 Tasks 1.2 补一句："各 FP 示例的期望 exit code 须逐条实测校准, 不得从 spec 文本直接照抄——尤其注意尾边界与引号相邻位置的语义。"
3. 明确提醒实现者：**尾边界是 R1 m-2 的已核销修复, SC-4 测红时禁止通过放宽/删除尾边界来强行凑合 exit=2**，只能改 SC-4 断言本身。

此修正不改变 §What 2 的技术方案（pattern 本身已确认正确，见任务 2），不改变零豁免的架构决策，属于 SC 文本层面的一处事实性订正，预期 R4 可快速收敛。

## 总结

R2 两条 Major（`pattern_hint` unbound / stderr 撤销误伤）核验结果 2/2 已解决，且解法质量高（前者消除改动面、后者转出时完整保留关键警告）。唯一生产改动（新 pattern）技术复核五项全部通过：尾边界有效、零交叠遮蔽、数组字面量安全、位置不影响匹配顺序语义、`[[ =~ ]]` 语义正确。SC-2 四个安全形态在零豁免设计下逐条实测全部放行，零豁免架构本身成立。但在核对"缩范围是否引入新问题"时，实测发现 SC-4 的三条 FP 示例命令有 2/3 与 proposal 断言的 exit code 不符（根因是 R1 m-2 尾边界的正确副作用），若实现阶段处理不当存在具体的"为凑 SC-4 而放宽边界、重开 R1 m-2"路径。此为新发现的 Major，修正为纯文本层面（订正 SC-4 断言或示例，不涉及范围/设计变更），故判 REVISE。
