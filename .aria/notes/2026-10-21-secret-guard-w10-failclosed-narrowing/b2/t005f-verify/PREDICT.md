# TASK-005 修复轮 (5f + 5f2) 主控复核: 预期 (2026-10-25, 5f2 交回之前写下)

静态 (已做, 5f 那一版): hook 里的 `_sg_relax_nowslfs` 与准入门两行和 proposal What 1 补充 2 的代码块逐字节相同; 函数在 :838, source 闸门在 :1069 之下。5f2 交回后再核: hook 相对 2893bcc 的 diff 只有 What 1 补充 2、What 7 补充 2 的六处与 5f2 第 1 条那一行注释。

主控自己的坏实现 (mkmut.py, 不用执笔席的 B1-B9), 经 run-suite.sh 跑 `SG_W10_ONLY='^V15-'` (PATH 上的 bash 5.2.15):
- M-A 只认精确名 WSLInterop (不认前缀): V15-W1b 红 [status], 其余 V15 绿。
- M-B 挂载表读不出时返回 0 (放行方向): V15-W1d 红 [status], 其余绿。
- M-D 准入门里对函数结果取反: V15-W1e 红; 本机无 WSL, 函数返回 0 取反后 wsl 被置位、准入门关闭, 依赖准入门打开的 V15-T2 也红。
- M-E 计时器睡整个预算: V15-T1 红 [value], 其余绿。
- 实现: V15 全绿 (3 个 T 与 W1e 在 relax, W1a-d 两种模式)。
