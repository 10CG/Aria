# Handoff: state-scanner-mechanical-enforcement Phase B.2 Resume

**Session**: 2026-04-23 20:58–21:20 UTC
**Branch**: `feature/state-scanner-mechanical-enforcement` (主项目 + aria submodule)
**Spec**: `openspec/changes/state-scanner-mechanical-enforcement/`
**Status**: Approved, B.2 进行中 (T0 + T1.1–T1.3 完成，T1.4–T10 待续)

---

## 本 session 完成清单 (~4h 工作量压缩)

### Phase A
- ✅ A.0 state-scanner 扫描 (入口)
- ✅ A.1 Spec 激活 (Draft → Approved)
- ✅ A.1.5 post_spec Agent Team 审计 (4 agents 并行 1 轮收敛, 4/4 `activate_with_revisions`)
  - 报告: `.aria/audit-reports/post_spec-2026-04-23T2058Z-state-scanner-mechanical.md`
- ✅ A.2 Revisions 注入 tasks.md (T0.1–T0.4 + T4/T7 修改)
- ✅ A.3 Agent 分配 (CF-1 tech-lead / CF-2 qa-engineer / CF-3 backend-architect / CF-4 code-reviewer)

### Phase B
- ✅ B.1 分支创建 (`feature/state-scanner-mechanical-enforcement` × 2)
- ✅ B.2 T0.1 CF-1 Target Version → v1.17.0 (proposal header)
- ✅ B.2 T0.2 CF-3 `snapshot_schema_version` 命名分离 (scan.py + tasks.md)
- ✅ B.2 T0.3 CF-4 AD-SSME-6 降级为手维 schema + CI validator
- ✅ B.2 T0.4 CF-2 T7.0 JSON canonical normalizer 前置任务加入
- ✅ B.2 T1.1 scan.py 骨架 (argparse / logger / exit codes / top-level orchestration)
- ✅ B.2 T1.2 Phase 0 中断检测采集器 (`collect_interrupt_state`)
- ✅ B.2 T1.3 Phase 1 Git 采集器 (`collect_git_state`, 含 porcelain -z / upstream / recent_commits / shallow detection)
- ✅ Smoke test: scan.py on Aria repo 本身 → exit 0, schema=1.0, 无 collector 错误

### 代码文件产出
- `aria/skills/state-scanner/scripts/scan.py` (310 行, stdlib-only)
  - `SNAPSHOT_SCHEMA_VERSION = "1.0"` (CF-3 隔离)
  - 退出码: 0/10/20/30 分层
  - fail-soft 每 collector 独立 error 聚合到 `snapshot.errors[]`

---

## 剩余工作 (T1.4 → T10, ~48h 含 buffer)

| 任务组 | 剩余 | 核心风险 |
|---|---|---|
| T1.4 UPM phase_cycle + active_module 采集 | 1h | UPM 格式解析, 需找 docs/architecture 的 UPMv2-STATE |
| T1.5 变更分析 (file_types / complexity / skill_changes) | 1.5h | Level 1/2/3 启发式需基于文件路径白名单表 |
| T2. Phase 1.5–1.10 (需求/openspec/arch/readme/standards/audit) | 5h | requirements 5 种 Status 正则已在 SKILL.md 1.5 列出, 可直接抄 |
| T3. Phase 1.11–1.14 (custom-checks/sync/issue/forgejo) | 6h | **T3.3 多远程 parity 是最高风险**, 需要确定 git-remote-helper 调用模式; **T3.1 YAML 解析** 是 stdlib-only 关键抉择点 (见 IF-3) |
| T4. Schema 文档 + validator | 2h | 已降级为手维 schema.md, 较稳 |
| T5. SKILL.md 重构 Step 0 + prose 精简 | 3h | v3.0.0 bump, 需同步 marketplace.json |
| T6. 测试套件 | 8h | Phase 1.13 Forgejo API mock 是最大块 |
| T7. Aria dogfooding + JSON normalizer | 2.5h | **T7.0 normalizer 必须先做**, 否则 T7.1 无法机械断言 |
| T8. Kairos + minimal fixture 验证 | 2h | qa-engineer IF-6: minimal fixture 之前无对应任务, 需补 T8.3 |
| T9. Migration + opt-out | 2h | mechanical_mode=false 分支语义需在 T5.3 定义 |
| T10. Benchmark + 发版 | 2h | eval scenarios 设计未定 (qa IF-5 calibration 风险) |
| **小计** | **~35h** | 含 CF revisions 已吸收, 不含 IF 处理 |
| Buffer 20% | 7h | |
| **合计** | **~42h** | 约 1 周 full-time |

### Important Findings (开工 1 周内评估)
- IF-1: 工时基线校准 (v2.9 → v2.10 + scan_submodules)
- IF-2: T3 末尾插 partial-delivery gate
- IF-3: stdlib-only 边界 (YAML/git porcelain/Windows subprocess)
- IF-4: 超时预算全局表
- IF-5: Benchmark scenarios 设计
- IF-6: minimal fixture repo 跨项目验证点补任务
- IF-7: Activation Gate 计数器持久化
- IF-8: opt-out 与 Phase 2 断言互斥语义

---

## 下 session 恢复入口

1. `git checkout feature/state-scanner-mechanical-enforcement` (主项目 + aria submodule)
2. 读本文件 + `.aria/audit-reports/post_spec-2026-04-23T2058Z-state-scanner-mechanical.md`
3. 运行 `python3 aria/skills/state-scanner/scripts/scan.py` 确认骨架仍工作
4. 从 **T1.4** 开始 (UPM phase_cycle 采集) 或根据优先级决定先开 T3.3 (多远程 parity, 最高风险)
5. 完成 T1–T3 后再触发 mid_implementation audit (Agent Team 复用同样 4 agents)

**关键不变量**: `SNAPSHOT_SCHEMA_VERSION` 在落地 T4 之前保持 `"1.0"`, 任何新字段只做**增量**不**变更**已有键名/类型。

---

## 本 session 未触达但已记录的 Option 3 工作

继续 Issue triage (aria-plugin #17 Drift Guard / #18 estimator) — 作为 Option 2 handoff 后独立 Phase A.1 启动, 见 Task #7.
