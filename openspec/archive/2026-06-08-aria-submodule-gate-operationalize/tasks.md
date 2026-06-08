# Tasks — aria-submodule-gate-operationalize

> Spec: `aria-submodule-gate-operationalize` (Level 2)
> Target: aria-plugin v1.40.0 + 主仓 v1.7.1
> 两 TG 可并行 (无交叉依赖)

## TG-1 (R-fix-1) — gate 在 git-直驱 ship 也执行 + 记 telemetry

- [x] **1.0** OQ1 裁定调用面 (pre-push hook (a) / standalone CLI (b) / convention (c)); 倾向 (a)
- [x] **1.1** 实现选定调用面: submodule pointer 变更时跑 `submodule_gate.sh` (warn 模式) + 写 `aria/metrics/submodule-gate-{warns,blocks,...}.jsonl`,覆盖 git-直驱 ship
- [x] **1.2** 不改道 git-直驱经 phase-c-integrator skill (约束); telemetry 路径与 parent 一致
- [x] **1.3** 单测: fixture 含 submodule pointer 变更的 push/ship → 断言 telemetry jsonl 新增正确行 (Rule #6 substitute)
- [x] **1.4** 单测: 无 submodule 变更 → 不写 telemetry (避免噪音)。**增量 (R1 qa)**: 相对既有 T-replay-6 (no-change 路径仅断言 exit 0 + "unchanged" 串), 本测新增 **jsonl 行数=0 断言** (扩展 T-replay-6 而非全新重复 fixture)

## TG-2 (R-fix-2) — tripwire runner 可成功运行

- [x] **2.0** Phase B step 0 (必办先行): 经可达手段确认 tripwire 实际失败 step + 错误 (验证/推翻 SSH-auth 假设); 记录证据。**降级 (R1 qa info)**: 若日志全不可达 (SSH 不通 + runner 日志不可达 + forgejo web 不可用) → 以 .gitmodules SSH URL + workflow 静态分析 + 5/5 一致失败 为据, 把 SSH-auth 列为 **tentative-confirmed** + 显式记风险 (非 Spec 阻塞); OQ2 据此保守选 (b)/(c) (不依赖 runner reach forgejo)
- [x] **2.1** OQ2 裁定修复路径 (token-rewrite (a) / 免-checkout 重写 (b) / host-cron 迁移 (c)); 依 2.0 结果 + CF-Access 可达性
- [x] **2.2** 实施修复
- [x] **2.3** dogfood: dispatch tripwire (dry_run) → 确认 run 成功完成 (clean 或正确 detect),非 failure
- [x] **2.4** dogfood: 非 dry-run dispatch → 确认写 `submodule-gate-misses.jsonl` last_run record (首个真实 tripwire telemetry)

## 收尾 (Phase C/D)
- [x] **D1** 5+1 SOT bump aria-plugin v1.39.0→v1.40.0 (若 TG-1 改 aria-plugin) + 主仓 v1.7.1 (tripwire) + gitlink
- [x] **D2** 全量测试零回归 + Phase C 双远程 parity
- [x] **D3** 归档 Spec + handoff (Rule #9); 更新 block-flip defer 决策记录 (gate 已可运营, 可重启)

## 验收 (AC)

> AC-1/AC-2 写**路径无关抽象形式** (Rev1, per R1 qa 2 major); OQ1/OQ2 裁定后在 tasks 具体化, 防 downstream drift。

- **AC-1** (路径无关): submodule pointer 变更的 ship 后 `aria/metrics/` 出现 gate telemetry ≥1 行 — R-fix-1 闭环 (0→可累积)。**验证机制随 OQ1**: 选 (a) hook → 端到端 fixture (真实 `git push` 触发 hook → 断言 jsonl, 验**触发面**); 选 (b) CLI → 直接调用验 gate 写入 + 触发覆盖靠 convention (AC-1 不声称 hook 级自动触发)。
- **AC-2** (路径无关): tripwire 能**成功执行一次** (clean 或正确 detect, status != failure) — R-fix-2 闭环 (5/5 fail→可运行)。触发方式随 OQ2: dispatch (a/b) 或 cron job 首次成功执行 (c)。
- **AC-3**: 新单测全绿 + 现有 phase-c-integrator/submodule-gate 测试零回归
- **AC-4**: gate 默认仍 warn (未 flip); 向后兼容
- **AC-5** (说明性/程序性, **不可自动化** — R1 qa minor): 修复后**文档说明**如何累积 ≥3 真实 executions + tripwire 验活 → 满足 deferred block-flip 重启前置。归属: handoff §next-step + 更新 `.aria/decisions/2026-06-07-v1.40.0-block-flip.md` (gate 已可运营, 可重启), 非自动化 gate。
