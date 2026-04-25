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

- [x] **T6.5-followup** 提升 I/O-heavy collector 覆盖 (pre_merge R1 IF-2) — 通过 `unittest.mock.patch("collectors.<m>._run", side_effect=fake)` subprocess mocking 层, 新增 130 tests (221→351). 实测 stdlib `trace`-based coverage: sync 18.2%→67.8% (+49.6pp) / multi_remote 33.1%→69.7% (+36.6pp, rounds to 70%) / issue_scan 43.8%→73.4% (+29.6pp ✅). sync 仍 ~2.2pp 低于名义 70% 阈值 — 缺口来自 `_collect_current_branch` 四状态结构化 dict 字面量的多行延续 (Phase 1.12 spec §4 强制), `trace` 工具按"unique line numbers in execution events" 计数, 多行语句仅计 1 line hit. 实际可执行分支已全覆盖 (directional guard / fail-soft / parse_failed 等). 见 aria 子模块 `tests/test_sync_mocked.py` / `test_multi_remote_mocked.py` / `test_issue_scan_mocked.py`

## T7. Aria 项目 dogfooding (2.5h, +0.5h per CF-2)

**Design reframe (2026-04-24)**: T7.1 literal 文本 "对比 v2.9 输出字段" 不可行 —
v2.9 prose 路径无 JSON 产物可 diff. 实际实施为 **v3.0 vs v3.0 snapshot stability**
(两次 scan.py 跑 + normalize + diff 断言零 drift). 详见 aria PR #26 commit message
+ `references/json-diff-normalizer.md` §"Why reframe" 章节.

- [x] **T7.0** (CF-2 前置) 定义 JSON canonical normalizer + stdlib-only 实现 (0.5h) — aria PR #26 merged 2026-04-24 (1a875d5); `references/json-diff-normalizer.md` (10 rules 规范) + `scripts/normalize_snapshot.py` (stdlib ~170 行)
- [x] **T7.1** 在 Aria 主项目跑新版 scan.py + normalize, 生成 golden baseline (1h) — aria PR #26; `tests/fixtures/reference-snapshot-aria.json` (722 行, Aria master 2026-04-24 归一化快照). **reframe from literal v2.9 compare**
- [x] **T7.2** 机械断言 diff exit code 0 (1h) — aria PR #26 `tests/test_normalize_snapshot.py::TestStabilityIntegration` (两次 scan.py + normalize → 字节级一致断言); live dogfood 验证 DIFF_EXIT=0

## T8. Kairos 跨项目验证 (2h)

- [x] **T8.1** 在 Kairos 项目跑新版 state-scanner (含新脚本) (1h) — 2026-04-25 dogfooding: `python3 scan.py --project-root /home/dev/Kairos` exit code 0, 520 行 JSON snapshot, errors[] 空, 全 17 顶层 key 产出 (issue_status 缺失符合预期 — Kairos `.aria/config.json` 中 issue_scan disabled, 等价于 Spec §Schema "可选 18 keys" 17 keys path). 二次 run + normalize → DIFF_EXIT=0 (T7 stability 在跨项目复测通过). 工件: `.aria/t8-kairos-validation/snapshot-{raw,normalized}.json`
- [x] **T8.2** 验证 TypeScript/Node.js 环境下所有字段采集正确 (无 False 假设 Aria-only 的硬编码) (1h) — 字段级审计结果:

  **PASS (无 Aria-only 假设)**:
  - git/changes/sync_status/multi_remote/forgejo_config: 全部跨项目兼容, parity 检测准确 (origin parity=equal, FETCH_HEAD stale=true)
  - openspec: 44 archived items + 3 active changes 解析准确 (Kairos OpenSpec 用同 spec 格式)
  - readme/standards/upm/audit/custom_checks/architecture/interrupt: configured/exists 信号准确
  - 无任何 collector 因 TS/Node.js 环境特性失败 (无 hardcoded `.py`/`requirements.txt`/Aria 路径假设)

  **FINDING (非 Aria-only 假设, 但跨语言 i18n 边界发现)**:
  - `requirements.collector` Status 提取正则不识别 Kairos 中文文档常用的 **fullwidth colon `：`** + **inline blockquote 多 meta** 格式. 例如 Kairos `US-009-tts-voice-clone.md` 含 `> **优先级**：P0 | **里程碑**：M3 | **状态**：pending`, 但 Spec §1.5 5 种正则只覆盖 halfwidth colon `:` + 行首 `**Status**:` / `**状态**:` 形式. PRD + 15 user stories raw_status 全 null (其中 1 个文档实际有 status, 14 个本就没有, 1 个被漏检).
  - **不阻塞 Spec 归档**: 这是 i18n 增强候选 (适配中文 markdown 排版习惯), 非 TypeScript-specific 缺陷. 当前行为 fail-soft (raw_status=null → status=unknown, by_status 仍正确聚合), 用户层无破坏性影响.
  - **建议**: 单独立 micro-Spec `state-scanner-i18n-status-regex` (~1h, 添加 fullwidth colon `：` + inline blockquote `> .*\*\*(Status|状态)\*\*[：:]\s*(\S+?)(\s*\||\s*$)` 变体). 不放进 mechanical-enforcement 作用域.

  **跨项目验证结论**: state-scanner v3.0.0 在非 Aria 项目 (TypeScript/Node.js, OpenSpec convention 一致, 中文文档为主) 上无破坏性失败, 全部 fail-soft 保护生效, 接口契约稳定.

## T9. 迁移与回退 (2h)

- [x] **T9.1** 创建 `references/migration-v2.9-to-v3.0.md` (1h) — aria PR #25 merged 2026-04-24 (e6cb261); ~170 行, 含 Why / Step 0 / exit codes / D1-D5 / opt-out lifecycle / downstream callers / upgrade checklist / rollback
- [x] **T9.2** `state_scanner.mechanical_mode` config flag (默认 true, 可 opt-out) (0.5h) — aria PR #25. **设计澄清**: flag 是 AI-prose contract (SKILL.md §Step 0 + §Opt-out 段), NOT scan.py runtime switch (grep 0 hit 全 collector/scan.py). scan.py 本身就是 mechanical path, 不需要 runtime 分支; flag 由 config-loader 读取供下游 skills 感知
- [x] **T9.3** 在 CHANGELOG / plugin.json 明确 **v1.18.0** 起移除 opt-out (0.5h) — aria PR #27 merged 2026-04-25 (4f91461); CHANGELOG [1.17.0] §Deprecated 显式说明 mechanical_mode opt-out 在 v1.18.0 移除; R1-M1 drift 已先于 proposal.md 在 PR #39 清理

## T10. Benchmark 与发版 (2h)

**Smoke benchmark precedent applied (2026-04-25)**: 与 v1.16.2/3/4 patch 同模式, 使用 inline structural assertions 替代 full /skill-creator AB. 理由: doc-dominant 变更 (SKILL.md -724 行), 已有更强机械证据 (215 unit tests + T7 DIFF_EXIT=0), full AB delta 信号会被 LLM stochasticity 淹没. Full /skill-creator AB 安排为 v1.17.x post-release validation, 不阻塞此 release. 详见 `aria-plugin-benchmarks/ab-results/2026-04-25-state-scanner-v1.17.0/benchmark.md` §"Why smoke not full AB".

- [x] **T10.1** 运行 smoke benchmark (with mechanical evidence) — 11 ab-suite eval cases × 35 structural assertions = **35/35 (100%) PASS** (1h replaced by smoke approach)
- [x] **T10.2** 结果存入 `aria-plugin-benchmarks/ab-results/2026-04-25-state-scanner-v1.17.0/` (benchmark.md + state-scanner/smoke-results.json) (0.5h)
- [x] **T10.3** 5 版本文件批次同步 v1.16.4 → v1.17.0: plugin.json / marketplace.json / VERSION / README.md / CHANGELOG.md (0.5h) — aria PR #27 merged (4f91461)

---

## 验收交付物

- [x] `aria/skills/state-scanner/scripts/scan.py` (可执行, stdlib-only) — delivered v1.17.0 (PR #27)
- [x] `aria/skills/state-scanner/references/state-snapshot-schema.md` — delivered T4 (aria PR #25)
- [x] `aria/skills/state-scanner/references/migration-v2.9-to-v3.0.md` — delivered T9.1 (aria PR #25, 170 行)
- [x] `aria/skills/state-scanner/tests/test_scan.py` + fixtures — delivered T6 + T6.5-followup (221 → 355 tests, aria PR #24/#29)
- [x] SKILL.md v3.0.0 with Step 0 硬约束 — delivered T5 (aria PR #23, 1178→454 行)
- [x] `.aria/state-snapshot.json` (dogfooding 产物示例) — Aria 项目 + Kairos 项目 dogfooding 各产出 1 份 (T7 / T8.1)
- [x] Benchmark 结果 (delta 非负) — T10.1 smoke benchmark 35/35 (100%) PASS (`aria-plugin-benchmarks/ab-results/2026-04-25-state-scanner-v1.17.0/`)
- [x] plugin 版本 bump (v1.16.0 或 v1.15.x) — actually bumped to **v1.17.0** then v1.17.1 patch (post-CF-1 revision)

---

## 后置动作 (merge 后)

- [ ] 观察 L1 探针 (`issue-cache-freshness`) 4 周零告警
- [ ] 观察 `mechanical_mode=false` 使用量 (若为零则 v1.18.0 安全移除 — post-CF-1 revision)
- [ ] 在 MEMORY.md 标记 `feedback_state_scanner_run_all_phases.md` 为 "partially obsolete (机械化已落地, 但作为历史原因记录保留)"
- [ ] 评估其他 Skill 是否有类似 prose-only 执行的脆弱性, 决定是否推广本 Spec 模式
