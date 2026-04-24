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

- [ ] **G.1** L1 探针告警计数或用户显式启动信号已记录
- [ ] **G.2** 确认 Activation Gate 触发原因 (告警 / 显式 / 演化压力)
- [ ] **G.3** 确认 state-scanner 当前版本, 评估是否需要重估 §工时估算
- [ ] **G.4** 确认 Spec Status 从 Draft → Approved

---

## T1. 脚本骨架与 Phase 1.1-1.5 (6h)

- [ ] **T1.1** 创建 `aria/skills/state-scanner/scripts/scan.py` 骨架 (argparse / logger / exit codes) (1h)
- [ ] **T1.2** 实现 Phase 0 中断检测 (读 `.aria/workflow-state.json`, git_anchor 验证) (1h)
- [ ] **T1.3** 实现 Phase 1 Git 状态采集 (status / branch / recent_commits / staged/unstaged) (1.5h)
- [ ] **T1.4** 实现 Phase 1 项目状态 (phase_cycle from UPM / active_module / openspec_status 摘要) (1h)
- [ ] **T1.5** 实现 Phase 1 变更分析 (file_types / complexity Level 1-3 启发式 / skill_changes detection) (1.5h)

## T2. Phase 1.6-1.10 (5h)

- [ ] **T2.1** 实现 Phase 1.5 需求状态扫描 (扫 `docs/requirements/`, 5 种 Status 正则) (1h)
- [ ] **T2.2** 实现 Phase 1.6 OpenSpec 扫描 (changes/ + archive/, Status 字段提取) (1h)
- [ ] **T2.3** 实现 Phase 1.7 架构状态 (system-architecture.md header + 链路完整性) (1h)
- [ ] **T2.4** 实现 Phase 1.8 README 同步检查 (版本 / 日期 / Skill 数量) (1h)
- [ ] **T2.5** 实现 Phase 1.9 + 1.10 standards + audit 扫描 (audit-reports/ 最新报告解析) (1h)

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

## T4. Schema 文档与版本化 (2h, AD-SSME-6 降级)

- [ ] **T4.1** 创建 `aria/skills/state-scanner/references/state-snapshot-schema.md` 作为 **source-of-truth** (手维), 明示 `snapshot_schema_version` (顶层) vs `issue_status.schema_version` (Phase 1.13 内嵌) 的作用域分离 (1h)
- [ ] **T4.2** scan.py 定义 `SNAPSHOT_SCHEMA_VERSION = "1.0"` 常量 → JSON 输出顶层 `snapshot_schema_version` (CF-3 rename), 加载时 SKILL.md 硬断言 (0.5h)
- [ ] **T4.3** schema.md 与 scan.py 一致性 validator: `scripts/validate_schema_doc.py` 读取 schema.md 字段表 + scan.py `SNAPSHOT_SCHEMA_VERSION` + 抽样输出 key 对齐, CI 可调用 (0.5h, 降级自"docstring 自动生成")

## T5. SKILL.md 重构 (3h)

- [ ] **T5.1** 在 SKILL.md `## 执行流程` 章节开头插入 **Step 0 机械指令** 块 (0.5h)
- [ ] **T5.2** 将 Phase 1.1-1.14 的 prose 描述精简为"字段由 scan.py 产出, 语义见 state-snapshot-schema.md" (1h)
- [ ] **T5.3** Phase 2 入口断言: 读 `.aria/state-snapshot.json`, 验证 `schema_version == "1.0"`, 缺失或不匹配直接 abort (0.5h)
- [ ] **T5.4** Phase 3/4 保持不变 (AI prose 路径) (0h)
- [ ] **T5.5** 更新 SKILL.md 顶部 "版本" 为 v3.0.0 (0.5h)
- [ ] **T5.6** 更新 `aria/skills/state-scanner/references/*.md` 中引用 SKILL.md prose 字段的地方 (0.5h)

## T6. 测试套件 (8h)

- [ ] **T6.1** 创建 `tests/test_scan.py` + pytest 配置 (1h)
- [ ] **T6.2** 创建 `tests/fixtures/` — minimal git repo / openspec / audit reports / config 变体 (2h)
- [ ] **T6.3** Phase 0 + Phase 1 (git/project/changes) 单元测试 (1.5h)
- [ ] **T6.4** Phase 1.5-1.10 (需求/openspec/arch/readme/standards/audit) 单元测试 (1.5h)
- [ ] **T6.5** Phase 1.11-1.14 (custom/sync/issue/forgejo) 单元测试, 含 mock Forgejo API (2h)
- [ ] **T6.6** schema_version mismatch abort 路径测试 (0h, 归并 T5.3)

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
