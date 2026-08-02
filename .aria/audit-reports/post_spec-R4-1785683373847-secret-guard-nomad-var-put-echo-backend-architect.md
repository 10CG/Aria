---
verdict: PASS
agent: backend-architect
round: R4
critical_count: 0
major_count: 0
minor_count: 1
r3_resolved: 1/1
---

# post_spec R4 审计报告 — secret-guard-nomad-var-put-echo (convergence, 收敛验证)

## 审计对象与方法

`/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`。方法：复用本 session scratchpad (`/tmp/claude-1000/-home-dev-Aria/.../scratchpad/r4/`) 内已就绪的 `base.sh`（未改动生产 hook）/ `var.sh`（按 §What 2 原文在 `:406` 后插入新 pattern 的补丁副本）/ `run.sh`（与生产 hook 完全一致的调用形态 `jq -n '{tool_name:"Bash",tool_input:{command:$c}}' | hook`），对 SC-1~SC-7 全部断言 + R3 发现的 3 条 FP 示例逐条重新实测（31 条用例，含既有 X1-X11 交叉用例）。未修改仓库任何文件（含子模块），只读 + scratchpad 内验证。

## 任务 1 — R3 Major 核销核验

R3 Major：SC-4 三条 FP 示例中 2/3（`grep` / `echo`）声称 exit=2 但实测 exit=0，且存在"实现者为凑断言而放宽尾边界、重开 R1 m-2"的风险路径。

**当前版本 SC-4 文本**已改写为与实测一致的断言，实测复核：

```
SC4a  grep -rn 'nomad var put' aria/            exit=0  (原声称 exit=2 → 现改为"仍 exit=0 放行", 相符)
SC4b  echo "改用 nomad var put"                  exit=0  (同上, 相符)
SC4c  git commit -m "fix: nomad var put 回显"    exit=2  (原声称即相符, 保留)
SC4d  nomad var put secret/p @f (阳性对照)        exit=2  (新增, 证明拦截确由新 pattern 产生)
```

三条断言与实测**完全一致**，触发"文本 vs 实测"矛盾的根本条件已消除。

**风险路径核查**：新增的"实现约束"块（紧邻 SC-4 之下）原文：「SC-3 与 SC-4 前两条互为约束——要让 `grep 'nomad var put'` 也被拦就必须去掉尾边界，而那会立刻误配 `nomad var putty`（SC-3 转红）。在「零新增豁免」下二者不可兼得，本 spec 选择保尾边界。实施者不得为「凑」某条 FP 断言而放宽边界。」

判定：**双重核销**——(1) 断言文本本身已按实测订正，不再存在会诱导实现者"修代码去凑断言"的文本矛盾；(2) 即便如此，仍在断言正下方（实现者跑测试时第一眼可见的位置）显式写明互斥关系 + 禁止放宽边界的强约束。风险路径的触发条件（矛盾断言）与后备防线（显式禁令）同时到位，判定：**R3 Major 已完全核销，且是最强形态**（消除触发条件 + 显式禁令双重兜底）。

**r3_resolved: 1/1**。

## 任务 2 — 唯一生产改动 + SC-2 技术终检

Pattern `nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)`，位置 `:406` 紧邻 `(get|list)` 条：字面、位置、尾边界写法在当前 spec 文字下**零歧义**，用 `[[ =~ ]]` 语义在补丁副本实测全部符合描述（SC-1 五条 exit=2 / SC-3 `putty` exit=0 / SC-6 读向不回归 exit=2）。

SC-2 三条 + `-verbose` 警示注记逐条实测：

```
nomad var put ... >/dev/null              exit=0
nomad var put ... &>/dev/null             exit=0
nomad var put -out=none ... >/dev/null    exit=0
nomad var put -verbose ... >/dev/null     exit=0  (警示注记声称"仍会泄漏但 hook 侧放行", 与实测一致)
```

SC-6 投影写法（`-out=json | jq '.Items | keys'`）exit=0，负向锚点（`keys[]` 带方括号）exit=2——均与实测相符，且与 `standards/conventions/secret-hygiene.md` L182（`nomad var get -out=json nomad/jobs/myapp | jq '.Items | keys'`）逐字一致，SC-6"与 SOT 逐字一致"的断言核实无误。

判定：技术实现正确，无缺陷。

## 任务 3 — 扫本轮修订是否引入新技术问题

对 Tasks 1.3 声称"已完成"的 `secret-hygiene.md` 订正做完备性复核：

- `-out=keys` 全文两处命中均在警示语境（L163 "旧版本文档误写…会报 Invalid value"、L188 "不要用…该取值在 nomad 不存在"），零处在推荐语境——SC-7(b) 负向断言相符。
- **新发现（Minor）**：文件头 `> **Version**: 1.1.1`（L3）已按 proposal 声称的 "1.1.0→1.1.1" 更新，但 §10 版本历史表（L393-396）**只到 1.1.0 一行，无 1.1.1 变更记录行**——版本号已跳但变更条目未追加，是文件内部自身的 SOT 完备性缺口（非阻断性，不影响 hook 行为、不影响 SC-7 已声明的两处断言，纯文档表格遗漏）。建议 Task 1.3 补一行 1.1.1 changelog（订正 4 处 `-out=keys` + 反坑警示 + 与本 spec 关联），可与 Task 1.4/1.5 同批收口，不需要额外一轮审计。

未发现其余新技术问题；R3 已确认的其余技术点（尾边界互斥、零交叠、数组字面量安全、guard:ack 已知缺陷等）本轮未被触碰，保持原状。

## 总结

R3 唯一 Major（SC-4 断言与实测矛盾 + 放宽边界风险路径）已双重核销：断言本身订正为与实测一致，且显式禁令堵死"为凑断言改代码"的路径。唯一生产改动（新 pattern）与 SC-2 全部技术描述在当前 spec 文字下零歧义、逐条实测通过。本轮修订新发现一处 Minor（`secret-hygiene.md` 版本号已跳至 1.1.1 但变更历史表未补对应行），不影响生产行为、不阻断 ship，随手可修。**判定：CONVERGED（PASS）**。
