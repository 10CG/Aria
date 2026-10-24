# 主控独立复核 T002b — 实测前写下的预期 (2026-10-24 05:2x UTC)
依据: T002b 报告第 4 节与第 4.6 节; 被测 hook 直接取 worktree (af4658b6f935), 不用 agent 的 work/impl.sh 副本。
1. 实现 x 5.2.15 全量, 低负载: PASS 137, FAIL 0, SKIP 0, MISSING 0, 末行有 "timing batch: judged"。
2. 基线 x 5.2.15 (默认 59e333c): PASS 24, FAIL 39, MISSING 74。
3. run-mutants.sh 全量 (designated): 57/57 CAUGHT, 无 MISSED / WRONG-REASON; P-0 GREEN; 6 个常量扰动 CAUGHT。
4. SC_BASH 指向不存在文件: 输出 SETUP, 退出码 3。
5. sc-direct.sh 启动即崩: FAIL V0-H1 与 FAIL V0-H2, 退出码 1。
6. commentsync target: 实现 GREEN (105); 基线+插字符绕过 RED (64); 基线+整块删除 RED (57); 原型 target RED (13)。
7. 另做抽查 (报告没声称的): 坏实现的 hook 文件确与实现不同 (变异确实落盘), 指定用例的 FAIL 行确带 reasons.tsv 的原因标签。
