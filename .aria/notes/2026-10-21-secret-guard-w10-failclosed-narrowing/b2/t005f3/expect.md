# 5f3 预期 (先写后跑)
## prove5f3.sh
- 能红 (PATH bash 5.2.15, MODE relax, W1n 除外): good FAIL [] PASS 13; v33fn FAIL [fghijkl] (空表/叠 autofs/目录当表/noglob/failglob 应红, 另 000 与 0311 两条也红); nox FAIL [k]; order FAIL [m] ([platform] [time]); w1e-a FAIL [em] (W1e [closed], W1m [control]); w1e-b FAIL [e] ([open] [closed])
- 测试侧判据对照 (3.2.57/5.0.18/5.1.16/5.2.15/5.3.20): 12 种情形 0 不一致; hook 结论 host 0, autofs 0, late 1, none 0, stacked 0, empty 1, unreadable 1, dir 1, noglob 1, failglob 0, nosearch 1, listless 1; stderr 全 0
- 变异生成: mutants.py rc 0 (57 个坏实现, 7 个扰动); w14-mutants.py rc 0
- commentsync: target / baseline / proto GREEN; 四个构造 RED (计数与 5f2 的 77/59/58/57 接近, hook 两个可能因站点 1 多一个新单元而变)
## runall3.sh
- perf-good (4 个放宽 bash): TIMED ok ok, 墙钟 < 0.1 s; perf-v33fn: TIMED ok bad, 墙钟约 2 s (负载首尾 < 2 时才算数)
- w10 过滤轮: 5.x 四轮无 FAIL/MISSING; 3.2.57 放宽用例 SKIP [platform], W1a-m PASS
- full-path: 无 FAIL, 计数 990 (无 zsh 984) 与头注释一致; full-wsl: 放宽用例 SKIP [platform], 其余 PASS
- sc-cases: 无 FAIL/MISSING; run-mutants 两种模式: 全部 CAUGHT, P-0 GREEN; w14: 与上一段同 (not judged 0)
