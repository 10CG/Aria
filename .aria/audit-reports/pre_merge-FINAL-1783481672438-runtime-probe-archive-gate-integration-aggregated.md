# pre_merge FINAL — runtime-probe-archive-gate-integration (aggregated)

> **Checkpoint**: pre_merge | **Verdict**: **PASS (CONVERGED)** | **收敛轨迹**: R1 → R1-fix → R2 → R2-fix → R3 (零新 finding 稳定性确认轮)
> **审计对象**: aria-plugin feature/runtime-probe-archive-gate-integration `93b7406..2273eb0` (7 commits) + standards project.md 2.2.2 + 主仓 spec SOT 回传
> **团队**: 4 独立视角 — aria:code-reviewer (two-phase) / pr-review-toolkit:silent-failure-hunter / aria:qa-engineer (SC 覆盖矩阵) / aria:tech-lead (五方契约一致性)
> **日期**: 2026-07-08 | **主控**: main-loop (aria-runner-bot/023236f2, session s-646d)

## R1 (4 视角并行, code-grounded)

| 视角 | verdict | findings |
|---|---|---|
| code-reviewer | PASS | 0C / 1I (references L2 前置缺失) / 4M; Phase 1 spec compliance TASK-001~017 全 ✓ + 三层硬裁决 ✓; 四项 B.2 主控裁决独立论证均正确 (merge-append 判「唯一自洽解」) |
| silent-failure-hunter | REVISE | **1C** (L2 声明蒸发 — 合法 L2+声明交集 R3 裁决未演算) / 3I (E2E 静默追加同名键 / tab 缩进静默截断 / crash 持久痕倒挂) / 4M |
| qa-engineer | REVISE | 2I (max_age_days fencepost 零锁定 / SC-4 config-missing 编排层零覆盖) / 5M; SC-1~10 覆盖矩阵重建 |
| tech-lead | REVISE | 1I (proposal SOT 落后 merge-append 裁决) / 3M (exception 窄化未入 SOT / flow-style 残边 / CLAUDE.md 计数) |

**主控裁决 (cross_agent_verdict_independent_verify)**: C-1 severity 分歧 (SFH C vs CR I) — 行为 per proposal §What 3 R3 裁决明文 designed, 按 SFH 方案③处置 (SOT 披露 + 作者文档 L3 前置条件 + 测试锁定), 行为原判上报 owner 可复议 (见 PR #97 签字注意项)。

## R1-fix (`ae35d19`)

- 代码 4 修: FIX-1 tab 缩进→声明无效 (frontmatter_block) / FIX-2 (OSError,ValueError) NUL 防御 / FIX-3 _load_config unparseable 分型 reason / FIX-4 薄壳 outcome==warn 守卫 + COUPLING LOCK
- SOT 三处回传: proposal §What 3 (merge-append 全段 + L2 披露 + crash known-limitation) + detailed-tasks TASK-009/016 + SKILL.md 降级路径条款
- 测试锁: python 968 (tab/CRLF/NUL/config reason/fencepost/SC-4 编排层/CLI fallback 键缺席/count 精确/block+crash/L2 蒸发) + E2E 44→59 (三路分叉 merge/degraded/hard-fail + flow-style + 顶键注释) + CLI 9+skip 入账

## R2 (4 视角复核)

- code-reviewer **PASS** (I1 判「超预期」闭合; 新 2M 测试层) / qa **PASS** (7/7 CONFIRMED 真锁住; 新 3M) / tech-lead **PASS** (F1-F4 RESOLVED, F3 判「优于建议」; 新 2 非阻塞观察) / silent-failure-hunter **REVISE 窄幅** (R1 全项验收关闭; 唯一残留 **I-R2-1**: E2E 降级判据窄于 prose SOT — 裸 inline scalar `runtime_probe: enabled` 误归 hard-fail; 与 CR M-r1 同源双确认)

## R2-fix (`dee3a6a`)

- E2E (b) 判据放宽「任意非空 top_value 即降级」+ §12 裸 scalar 案例 8 断言 (59→67, 含写入步 exit code 首个显式断言)
- 顺手收编: CLI unreadable 判别断言 (锁 COUPLING LOCK 风险, 9→10) + E2E staleness 3 天判别式 (CR M-r2) + references tab 拒绝行 (TL N1)

## R3 (SFH 单点稳定性确认)

**CONVERGED** — I-R2-1 code+fixture+docstring 三位一体关闭 (非 paper fix); delta 快扫零新 finding。轨迹 R1 (1C+3I+4M SFH 口径) → R2 (1I) → R3 (0)。

## 终态验证面 (R3 时点独立复现)

python 968 全绿 / E2E 67 / CLI 10 (0 skipped 非 root) / resweep 124 spec diff=0 + required-corpus 守卫 3/3 / dogfood SC-7 (TASK-018 claim 真调 + TASK-019 真分区 probe=pass @2026-07-07T15:14:53Z)

## Backlog (双确认非阻塞, 不入本 cycle)

1. probe 结果结构化 sub-reason (替代 reason 子串耦合; CR M1) — 已 COUPLING LOCK 注释 + CLI 判别断言兜底
2. coordination_probe 未知 outcome 防御地板零测试 (qa new-1, 结构上不可达)
3. references last-wins 条款零测试 (qa new-3, dict 语义保证)
4. resweep 基线路径非 CI 复现 (qa 附带观察, 仓库级流程项)
5. E2E helper 顶键行裸 inline value 不在 references 拒绝表 (SFH R3 可选 polish, 「承认的形态」已隐式覆盖)

## Owner 复议项 (PR #97 签字注意)

1. [SFH R1 C-1] L2 声明蒸发行为维持 R3 裁决原判 (三面补课完成); 改行为需 spec 修订另启
2. merge-append 同名键裁决 (B.2 主控 2026-07-08)
3. crash 不入 D tracker known-limitation (归错 owner 论证)
