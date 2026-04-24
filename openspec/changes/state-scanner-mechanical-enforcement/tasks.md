# state-scanner-mechanical-enforcement — Tasks

> **Status**: Approved (2026-04-23, Activation Gate 条件 2 触发)
> **Level**: Full (Level 3)
> **预估工时 (原)**: 46h (含 20% buffer)
> **预估工时 (post-audit revision)**: ~52h (CF-2 +0.5h, CF-4 +2.5h, IF-1 Target Version 对齐 +2h, Buffer 20%)
> **触发条件**: L1 探针亮红 ≥ 2 次 / 用户显式要求 / Phase 1.x 新增第 15 个阶段

---

## T0. Pre-B.2 Revisions (audit 注入, 2026-04-23)

来自 post_spec Agent Team 4/4 一致投票 `activate_with_revisions`, B.2 开工前必须完成:

- [x] **T0.1** CF-1 Target Version 追齐 v1.17.0 + AD-SSME-5 v1.18.0 (proposal.md header 已更新)
- [x] **T0.2** CF-3 snapshot_schema_version 命名决议 — scan.py SNAPSHOT_SCHEMA_VERSION="1.0" 常量 + 顶层字段已落地; references/state-snapshot-schema.md 已创建 stub 明示命名隔离 (R1-C5 修)
- [x] **T0.3** CF-4 T4.3 revise 选型: **(b) 降级为手维 schema.md** — proposal AD-SSME-6 已更新, tasks.md T4 已重写, schema.md stub 已创建 (R1-C5 修)
- [x] **T0.4** CF-2 新增 T7.0 JSON canonical normalizer (jq -S + float 精度 + null/absent 归并) 作为 T7.1 前置 — T7 章节已加入 T7.0 条目

---

## 激活前置 (Gate)

- [x] **G.1** L1 探针告警计数或用户显式启动信号已记录 — Activation Gate 条件 2 (用户显式请求) 2026-04-23 触发, post_spec audit 4/4 PASS_WITH_WARNINGS + activate_with_revisions
- [x] **G.2** 确认 Activation Gate 触发原因 (告警 / 显式 / 演化压力) — 用户显式触发; post_spec Agent Team 共识
- [x] **G.3** 确认 state-scanner 当前版本, 评估是否需要重估 §工时估算 — Target Version 追齐 v1.17.0; §工时估算在 post_spec audit 内已 revised (CF-1/CF-4)
- [x] **G.4** 确认 Spec Status 从 Draft → Approved — 2026-04-23 完成 (见 proposal.md header)

---

## T1. 脚本骨架与 Phase 1.1-1.5 (6h)

- [x] **T1.1** 创建 `aria/skills/state-scanner/scripts/scan.py` 骨架 (argparse / logger / exit codes) (1h) — PR #33 merged 2026-04-24
- [x] **T1.2** 实现 Phase 0 中断检测 (读 `.aria/workflow-state.json`, git_anchor 验证) (1h) — PR #33
- [x] **T1.3** 实现 Phase 1 Git 状态采集 (status / branch / recent_commits / staged/unstaged) (1.5h) — PR #33
- [x] **T1.4** 实现 Phase 1 项目状态 (phase_cycle from UPM / active_module / openspec_status 摘要) (1h) — PR #33
- [x] **T1.5** 实现 Phase 1 变更分析 (file_types / complexity Level 1-3 启发式 / skill_changes detection) (1.5h) — PR #33

## T2. Phase 1.6-1.10 (5h)

- [x] **T2.1** 实现 Phase 1.5 需求状态扫描 (扫 `docs/requirements/`, 5 种 Status 正则) (1h) — PR #33 merged 2026-04-24
- [x] **T2.2** 实现 Phase 1.6 OpenSpec 扫描 (changes/ + archive/, Status 字段提取) (1h) — PR #33
- [x] **T2.3** 实现 Phase 1.7 架构状态 (system-architecture.md header + 链路完整性) (1h) — PR #33
- [x] **T2.4** 实现 Phase 1.8 README 同步检查 (版本 / 日期 / Skill 数量) (1h) — PR #33
- [x] **T2.5** 实现 Phase 1.9 + 1.10 standards + audit 扫描 (audit-reports/ 最新报告解析) (1h) — PR #33

## T3. Phase 1.11-1.14 (6h, 含 mid_impl + pre_merge audit 遗留 IDs)

**显式承接的 deferred findings** (R1-M1 code-reviewer audit 要求):
- TL-1 (mid_impl): scan.py 1073 行单文件 → 拆 collectors/ 包 (~1h, T3 开工前先做)
- TL-2 (mid_impl): Phase 1.5 `complexity` 阈值硬编码, 标注 `advisory_from_collector`
- CR-I1 (mid_impl): docstring schema.md 死链 → T4.1 文档落地 (pre_merge R1 已补 stub)
- CR-I2 (mid_impl): CLI --output 双写 → pre_merge R1-I3 已 in-session 修复
- CR-I3 (mid_impl): --log-level 无 validation → T3 开工前用 argparse choices=[] 收紧
- CR-I4 (mid_impl): T7.0 canonical normalizer → T7.0 独立任务已加入
- R1-I1 (pre_merge): snapshot_schema_version additive-change 规则 → schema.md stub 已记录, T4.1 细化
- R1-I2 (pre_merge): exit code 消费协议 → schema.md stub 已记录, T5.3 SKILL.md 吸收

- [x] **T3.1** 实现 Phase 1.11 自定义检查 (读 `.aria/state-checks.yaml` + 串行执行 + 超时守卫) (1.5h) — `collectors/custom_checks.py`, stdlib-only YAML subset parser, 4 negative-path cases pass (missing file / malformed YAML / version mismatch / timeout+rc127+disabled mix); aria 项目实测捕获 issue-cache-freshness MISSING
- [x] **T3.2** 实现 Phase 1.12 同步检测 (FETCH_HEAD age / submodule drift 方向性守卫) (1.5h) — `collectors/sync.py` 430 行; 方向性守卫 update/push/manual_check 三态; R2 BA-I1 fix: aligned submodule 显式 0 而非 null; R2 audit: `post_implementation-R1-...` §QA-I1+BA-I1
- [x] **T3.3** 实现 Phase 1.12 多远程 parity (v1.15.0+, local_refs / ls_remote 模式) (1.5h) — `collectors/multi_remote.py` 504 行; 5 种 parity + overall_parity 精确语义; R2 QA-C1 critical fix: overall_parity 要求至少一个 equal 证据; R2 QA-I1: ls-remote 空输出 → `remote_branch_missing, reachable=True`
- [x] **T3.4** 实现 Phase 1.13 Issue 感知 (Forgejo/GitHub 平台检测 + 缓存 + 10 种 fetch_error 枚举) (1h) — `collectors/issue_scan.py` 801 行; v1.1 schema + submodule 聚合; R2 QA-C2 critical fix: Forgejo `/issues` endpoint 返 PR → 客户端过滤 `pull_request` key + URL 含 `/pulls/`; 已知 Forgejo 自带 `type=issues` 过滤不可靠
- [x] **T3.5** 实现 Phase 1.14 Forgejo 配置检测 (CLAUDE.local.md forgejo 块) (0.5h) — `collectors/forgejo_config.py` 127 行; 4 状态; R2 QA-I3 fix: fenced code block `forgejo:` 不算 configured (mask ```...``` 后再匹配); R2 CR-M1: 补 collect_forgejo_config 函数级 docstring
- [x] **T3.6** Helper consolidation (4-agent audit consensus) (~1h, audit-driven add-on) — `collectors/git.py` 扩展 `_current_branch(timeout)` / `_is_shallow(timeout)` / `_enumerate_submodule_paths()`; sync.py / multi_remote.py / issue_scan.py 改为 import, 净减 24 行重复代码; byte-parity 验证

## T4. Schema 文档与版本化 (2h, AD-SSME-6 降级)

- [x] **T4.1** 创建 `aria/skills/state-scanner/references/state-snapshot-schema.md` 作为 **source-of-truth** (手维) (1h) — Full Schema authored 2026-04-24: 18 top-level keys documented (含 4 个新 T3 顶层 key); BA-R*-I1 (main_repo.path / items[].heuristic) / BA-R*-M1 (ERR_AUTH_MISSING reserved) / BA-R*-M2 (single-remote ahead-only 10-scenario worked examples table) / QA-C2 PR filter 全部文档化
- [x] **T4.2** scan.py 定义 `SNAPSHOT_SCHEMA_VERSION = "1.0"` 常量 → JSON 输出顶层 `snapshot_schema_version` (CF-3 rename) (0.5h) — 已在 b8db9a0 commit 实现 (scan.py:56 常量 + line 116 输出); SKILL.md 硬断言归 T5.3
- [x] **T4.3** schema.md 与 scan.py 一致性 validator: `scripts/validate_schema_doc.py` (0.5h) — 3 check 新 validator: 版本常量对齐 / 文档 required keys 在 live 输出中存在 / live keys 都被文档化. 本项目实测 3/3 PASS (18 keys matched)

## T5. SKILL.md 重构 (3h)

- [x] **T5.1** 在 SKILL.md `## 执行流程` 章节开头插入 **Step 0 机械指令** 块 (0.5h) — aria PR #23 merged 2026-04-24 (a02ddfe)
- [x] **T5.2** 将 Phase 1.1-1.14 的 prose 描述精简为"字段由 scan.py 产出, 语义见 state-snapshot-schema.md" (1h) — aria PR #23 (-724 net lines, 1178→454)
- [x] **T5.3** Phase 2 入口断言: 读 `.aria/state-snapshot.json`, 验证 `snapshot_schema_version == "1.0"` (post-CF-3 rename), 缺失或不匹配直接 abort (0.5h) — aria PR #23
- [x] **T5.4** Phase 3/4 保持不变 (AI prose 路径) (0h) — aria PR #23 (no change confirmed)
- [x] **T5.5** 更新 SKILL.md 顶部 "版本" 为 v3.0.0 + 底部版本行一致 (0.5h) — aria PR #23
- [x] **T5.6** 更新 `aria/skills/state-scanner/references/*.md` 中引用 SKILL.md prose 字段的地方 (0.5h) — N/A, references 已在 T4 阶段对齐 scan.py 契约, 仅 schema.md 引用 scan.py/snapshot_schema_version 为 source-of-truth 设计意图 (aria:code-reviewer R1 确认)

## T6. 测试套件 (8h)

**Design deviation (2026-04-24)**: 使用 stdlib `unittest` 而非 pytest. 理由: scan.py
是 stdlib-only (proposal.md §Constraints), 测试必须匹配部署目标 (Aether light 节点
无 pip). `run_tests.py` 提供 pytest-like UX + stdlib `trace` 覆盖报告. AD-SSME-1 一致.
T6 audit (pre_merge R1 aria:code-reviewer) 确认此偏移文档化充分, MERGE_WITH_FIXES.

- [x] **T6.1** 创建 `tests/test_*.py` + stdlib unittest 配置 (run_tests.py) (1h) — aria PR #24 merged 2026-04-24 (b747a85). 原 "test_scan.py" 拆为每 collector 一个 test_*.py + `test_scan_integration.py` 承担 E2E
- [x] **T6.2** 创建 `tests/_helpers.py` 工厂函数 (tmp_repo / tmp_project / make_openspec / make_audit_report / make_config / make_state_checks) (2h) — aria PR #24. **偏移**: 未创建 `tests/fixtures/` 目录, 改为 `_helpers.py` 工厂函数模式 (更灵活, 支持 tempfile 隔离). code-reviewer IF-1 确认功能等价, 仅目录命名不同
- [x] **T6.3** Phase 0 + Phase 1 (git/changes/upm/interrupt) 单元测试 (1.5h) — aria PR #24 (45 tests: interrupt 9 / git 14 / changes 11 / upm 11)
- [x] **T6.4** Phase 1.5-1.10 (需求/openspec/arch/readme/standards/audit) 单元测试 (1.5h) — aria PR #24 (57 tests: requirements 7 / openspec 23 / architecture 9 / readme 8 / standards 4 / audit 6)
- [x] **T6.5** Phase 1.11-1.14 (custom/sync/multi_remote/issue_scan/forgejo) 单元测试 (2h) — aria PR #24 partial (68 tests, 純函数 + 负向路径). 见 T6.5-followup I/O 覆盖待提升
- [x] **T6.6** schema_version mismatch abort 路径测试 (0h, 归并 T5.3) — aria PR #24 `test_scan_integration.py::test_schema_version_constant` writer 侧; reader 侧在 SKILL.md §阶段 2 入口断言 (AI prose, 非单元测试范围)

- [ ] **T6.5-followup** 提升 I/O-heavy collector 覆盖至 ≥70% (~3h, pre_merge R1 IF-2) — sync (18→70) / multi_remote (33→70) / issue_scan (44→70) 需要 subprocess mocking 层. 不阻塞 T7-T10 推进, 可并行或后置

## T7. Aria 项目 dogfooding (2.5h, +0.5h per CF-2)

- [ ] **T7.0** (CF-2 前置) 定义 JSON canonical normalizer: `jq -S --sort-keys`, float 精度 6 位, null/absent 字段统一归并, timestamp 字段白名单容忍差异, 输出到 `references/json-diff-normalizer.md` (0.5h)
- [ ] **T7.1** 在 Aria 主项目跑新版 scan.py, 通过 T7.0 normalizer 对比 v2.9 输出字段 (1h)
- [ ] **T7.2** 差异分析 + 修复 (字段命名 / 顺序 / 类型漂移), 机械断言 diff exit code 0 (1h)

## T8. Kairos 跨项目验证 (2h)

- [ ] **T8.1** 在 Kairos 项目跑新版 state-scanner (含新脚本) (1h)
- [ ] **T8.2** 验证 TypeScript/Node.js 环境下所有字段采集正确 (无 False 假设 Aria-only 的硬编码) (1h)

## T9. 迁移与回退 (2h)

- [ ] **T9.1** 创建 `references/migration-v2.9-to-v3.0.md` (1h)
- [ ] **T9.2** 实现 `state_scanner.mechanical_mode` config flag (默认 true, 可 opt-out) (0.5h)
- [ ] **T9.3** 在 CHANGELOG / plugin.json 明确 v1.17.0 起移除 opt-out (0.5h)

## T10. Benchmark 与发版 (2h)

- [ ] **T10.1** 运行 `/skill-creator` benchmark with/without AB 对比 (1h)
- [ ] **T10.2** 结果存入 `aria-plugin-benchmarks/ab-results/` + 审阅 delta 为正 (0.5h)
- [ ] **T10.3** 更新 plugin.json / marketplace.json / README / VERSION / CHANGELOG (0.5h)

---

## 验收交付物

- [ ] `aria/skills/state-scanner/scripts/scan.py` (可执行, stdlib-only)
- [ ] `aria/skills/state-scanner/references/state-snapshot-schema.md`
- [ ] `aria/skills/state-scanner/references/migration-v2.9-to-v3.0.md`
- [ ] `aria/skills/state-scanner/tests/test_scan.py` + fixtures
- [ ] SKILL.md v3.0.0 with Step 0 硬约束
- [ ] `.aria/state-snapshot.json` (dogfooding 产物示例)
- [ ] Benchmark 结果 (delta 非负)
- [ ] plugin 版本 bump (v1.16.0 或 v1.15.x)

---

## 后置动作 (merge 后)

- [ ] 观察 L1 探针 (`issue-cache-freshness`) 4 周零告警
- [ ] 观察 `mechanical_mode=false` 使用量 (若为零则 v1.17.0 安全移除)
- [ ] 在 MEMORY.md 标记 `feedback_state_scanner_run_all_phases.md` 为 "partially obsolete (机械化已落地, 但作为历史原因记录保留)"
- [ ] 评估其他 Skill 是否有类似 prose-only 执行的脆弱性, 决定是否推广本 Spec 模式
