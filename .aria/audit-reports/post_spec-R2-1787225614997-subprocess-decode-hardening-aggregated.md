---
round: R2 (+ v3/v3.1 收敛确认轮)
checkpoint: post_spec
spec: subprocess-decode-hardening
seats: [A1-backend-architect, A2-qa-engineer, A3-code-reviewer]
verdicts_r2: {A1: PASS, A2: REVISE, A3: PASS}
verdicts_final: {A1: PASS, A2: PASS, A3: APPROVE}
converged: true
verdict: PASS
rounds_total: 2
timestamp: 2026-08-20T04:05:00Z
---

# post_spec R2 聚合 — subprocess-decode-hardening (aria-plugin#147) — 收敛

## R2 本轮 findings (全部编辑级, 0 Critical)

- A1: 0C/1M/1m — SC-9 L2 层机械化边界措辞过度承诺 (M) / 排除谓词对 examples 类目录的裁决未记录 (m)
- A2: 0C/2M/2m — SC-4 行号锚定含不流向 sink 的 :150 并列 leg (M, 与 A3-R2-M1 同源) / SC-6 文件级 multiset 存在站点互换盲区 (M) / 测试点补验无留痕 + SC-2「混用」无定义 (m×2)
- A3: 0C/1M/4m — 同 SC-4 leg (M) / 13 文件计数、脚注 ² 口径、SC-9 边界、L2 括注 (m×4)

**Q1/Q2 复判亮点**: A1 自证其 R1 对 SC-8 的处方错误 (裸抛默认更贴合 dev-time CLI 语义); A2 自证其 R1 对 SC-6 的原处方 (函数级锚定) 比 v2 的简化更对, v2 简化被回退。

## v3 / v3.1 处置与确认

- v3: 上述 9 条全落 (SC-4 符号锚定重写 / SC-6 键改 (文件,函数,站点序号) / SC-9 机制边界声明 / SC-2 删「混用」/ L2 括注 :476-480 / 脚注 ² 词法限定 / examples 不排除显式裁决 / 测试点 30/30 留痕入 census 笔记)。
- **v3 修订自身引入 1 处新错** (勘正引错模式再现, A2/A3 双席独立命中): 符号锚定编造了不存在的函数名 `_query_run`/`_probe_capability` → v3.1 换回真名 `_run_with_retry`(:164)/`_verify_in_flight_flag`(:139), 闭合口径 `grep -c` = 0, A2/A3 各自独立重验通过。
- 确认轮三席均已在各自 R2 报告追加「v3 收敛确认」节并同步 frontmatter。

## 收敛判定

R1 (3×REVISE, 9 实质点) → R2 (0C, 编辑级) → 确认轮 3/3 PASS ⇒ **converged: true, 共 2 轮** (符合 L2 基线)。方案本体 (B/B′ + 16 处迁移 + 排除式谓词防再长) 两轮均未被动摇。

**下一步**: 待 owner 批准进 A.2 (task-planner 分解 detailed-tasks.yaml, post_planning checkpoint 亦为 enabled 须跑)。B′ 精化 (backslashreplace 单步) 已标注待 owner 确认条款于 spec §What Changes 2。
