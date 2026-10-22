# Tasks — layer-l-sweep-safety-and-recovery

> Spec: [proposal.md](./proposal.md) | Linked: `10CG/Aria#233` + `10CG/aria-plugin#167` | 执行轨: interactive

- [x] 1. `lib/constants.py`: `SWEEP_TTL_CROSS = 604800` + 分层依据注释
- [x] 2. `lib/claim_schema.py`: ClaimRecord +`swept_by`/`swept_at` (additive; parse 校验 ISO / serialize 条件发射)
- [x] 3. `lib/gc.py`: `sweep_stale_active(container_id, cross_ttl_seconds)` 分层 + provenance 写入 (`operator` 回退)
- [x] 4. `lib/claim_lifecycle.py`: `_latest_swept_record` + heartbeat/release 二次查找 → `claim_swept` (legacy 无出处降级 not_found) + `restore_swept_claim` (仅本容器)
- [x] 5. `scripts/phase1_gate.py`: self-resume 路径刷心跳 (真仓 E2E 验证: hb 32Z→55Z) + heartbeat 输出 `swept_by`/`swept_at` additive 键
- [x] 6. `scripts/release_gate.py`: `--sweep-stale` 分层接线 (identity 注入) / `--sweep-stale-all` (operator 模式) / `--restore` + released.swept_by/swept_at + `restore` 结果面; CLI 互斥校验
- [x] 7. SKILL.md ×2: phase-d-closer D.2b (分层语义 + released.error 三分 + restore 路径) / state-scanner (心跳分层 + 长会话 ≤12h 义务 + claim_swept 信号与恢复)
- [x] 8. SC substitute: `tests/test_sweep_safety.py` 17 SC 全绿 (stdlib runner; 基线反事实验证: stash lib/scripts 后全塌)
- [ ] 9. Rule #6 场景 1 AB: `ab-results/2026-10-22-layer-l-sweep-safety/` (3 evals × 2 臂; claim_swept 解读 / 邻居 30h 处置 / 长会话心跳义务)
- [ ] 10. 发版 v1.77.1 (与轨 A 同 release train): 五文件同步面 + 主仓 gitlink + badge + arch 版本行
- [ ] 11. C 阶段: PR + 本地合并 + 双推 + ls-remote 核验; 关 #233 (+#167 留言); D 阶段: 归档 + handoff
