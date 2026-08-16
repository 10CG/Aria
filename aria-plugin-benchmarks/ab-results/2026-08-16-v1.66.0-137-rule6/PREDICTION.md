# 测前预期 (在看到任何结果之前写下, memory predict-then-measure)

| eval | 预期 delta | 依据 |
|---|---|---|
| 1 C.1 commits | **无 delta** | 本次改动完全不碰 C.1 |
| 2 C.2 conflict | **无 delta** | 同上 |
| 3 C.2.5 multi-remote | **无 delta** | 同上 |
| 4 C.2.4 定向 | **应有明显 delta** | 旧版散文里逐字写着 `--branch main`, 新版换成 `<MAIN_BRANCH>` + 就地写明「本项目是 master」 |

## 可证伪点

- **若 eval-4 无 delta** ⇒ 文档那半修复没起作用, 需重做 (不是「AB 覆盖不到」可以搪塞的)。
- **若 eval-1/2/3 出现 delta** ⇒ 说明改动有我没预料到的外溢, 须查清。
- 旧版在 eval-4 上**大概率照抄字面 `main`** —— 那正是 #137 的现场; 若旧版也答对了 master,
  说明该缺陷靠模型常识就能绕过, 那么这次文档修复的价值要下调。
