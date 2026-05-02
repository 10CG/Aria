# OD-10 — T1 实施偏离 AD3 Option C finding + 修复路径锁定

> **Date**: 2026-05-02
> **Owner**: solo-lab (uni.concept.wzfq@gmail.com)
> **Spec**: aria-2.0-m2-layer1-state-machine
> **Tasks affected**: T1.1 / T1.3 / T1.7 (reopened) + T15.1 (受其下游影响)
> **Triggers**: T15.1 deployment session 2026-05-02 (state-scanner 推进流程)
> **Discovery method**: hermes plugin spec 实测 (`/opt/aria-orchestrator/venv/lib/python3.11/site-packages/hermes_cli/plugins.py` 源码读取) + 现有 aria-orchestrator nomad job inspect

## 关键发现

T1 实施 (Phase B.2 startup, 2026-04-28~29) 的 aria-layer1 plugin 结构与 AD3 Option C 锁定的 "pip entry-point" 路径不一致, 而是采用了一个不存在的混合格式 (既不是 directory plugin 也不是 pip entry-point)。

214 unit tests pass 不能覆盖此偏移, 因为单元测试 mock 掉了 hermes 加载路径。

## 偏移对照

| 项 | AD3 锁定 | T1 实施实际 | 状态 |
|----|---------|------------|------|
| 包形态 | Python pip package | 仅源代码目录 | ❌ 偏移 |
| Entry-point 声明 | `hermes_agent.plugins` group via `setup.py` / `pyproject.toml` | 无 | ❌ 偏移 |
| Manifest 文件 | `plugin.yaml` (hermes 标准, per `hermes_cli/plugins.py`) | `plugin.json` (自创) | ❌ 偏移 |
| Register 入口 | `__init__.py` 提供 `register(ctx: PluginContext)` | 仅 `class.on_session_start` instance method | ❌ 偏移 |
| Cron 注册路径 | 通过 `ctx.register_hook("on_session_start", ...)` 钩子内调 hermes cron API | `_register_with_hermes_scheduler` = `NotImplementedError` | ❌ 偏移 + 静态 dead code |
| 部署形态 | pip install 到 `/opt/aria-orchestrator/venv` (light_exec class, raw_exec driver) | DEPLOYMENT.md 描述 docker driver + heavy-1 节点 | ❌ 偏移 |
| 状态机逻辑 (10 states + S_FAIL) | PRD §M2 line 159+ | 完整, 214 tests pass | ✅ 对齐 |
| SQLite WAL / 字段最小集 | PRD §M2 持久化 | 完整 (T2.x done) | ✅ 对齐 |
| Issue 协议 (issue_id + prompt_path) | PRD §M2 + brainstorm OD-6 | 完整 (T7 done) | ✅ 对齐 |
| 状态机 transition table | brainstorm OD-1 (10 states) | 完整 (T3 done) | ✅ 对齐 |

## 偏移根因

| # | 因素 | 证据 |
|---|------|------|
| 1 | DEPLOYMENT.md 抄写自 M1 base infra (docker + heavy-1 + aria-build), 未对齐 hermes raw_exec 模式 | DEPLOYMENT.md §Overview 明示 reuse aria-build base infra |
| 2 | 214 unit tests 全部 mock hermes 接口, 没有 integration test 验证 hermes 真实加载 | tests/test_t1_extension_integration.py 用 mock module |
| 3 | M0 Spike POC 用 `option-c-poc/` 简化结构验证可行性, 但 T1 实施未照 spike 升级到 pip package | spike-report.md ST1-ST4 + option-c-poc/ 没有 setup.py |
| 4 | post_spec audit (Phase A.1.3) 检查的是 Spec 内部一致性, 不验证实施代码与 AD3 接口契约 | audit reports 在 .aria/audit-reports/ |

## 修复路径决策 (Decision: A)

按 [A] 严格修 T1 回到 AD3 Option C, 工时估算 4-6h:

1. **添加 `pyproject.toml`**: 声明 entry-point group `hermes_agent.plugins` → `aria_layer1:register`
2. **改造 `__init__.py`**: 添加 `def register(ctx: PluginContext) -> None` 入口函数
3. **`extension.py` 重构**: cron 注册从 `_register_with_hermes_scheduler` (NotImplementedError) 改为 `on_session_start` hook 内调 hermes cron API (`hermes cron create --command ... --interval 60m`)
4. **manifest 改格式**: `plugin.json` → `plugin.yaml` (hermes 标准格式)
5. **pip install** 到 `/opt/aria-orchestrator/venv` (light-1)
6. **修改 aria-orchestrator job HCL**: 加 host volume mount (light-1: `aria-layer1-data`) + LUXENO_API_KEY env (经 Nomad Variables)
7. **重启 aria-orchestrator job**: `nomad job stop && nomad job run`
8. **验证**: `hermes plugins list` 显示 enabled + `hermes cron list` 显示 `aria_layer1_tick`

## 备选路径不选理由

- **[B] directory plugin pivot**: 偏离 AD3 owner 已签字决策, 等于反悔; 长期可维护性低 (entry-point 是 hermes 推荐主路径)
- **[C] 暂停 T15 全面回审 brainstorm**: 已完成的 T1-T14 代码 (state machine 逻辑) 没偏移, 全面 audit 是 over-correction; 工时 6-10h 不值

## Tasks 影响

| Task | 原状态 | 新状态 | 原因 |
|------|--------|--------|------|
| T1.1 | done | **reopened** | plugin 包结构需重做 (pyproject.toml + register + plugin.yaml) |
| T1.3 | done | **reopened** | `_register_with_hermes_scheduler` 是 dead code, 必须替换为 hermes cron API 调用 |
| T1.7 | done | **reopened** | DEPLOYMENT.md 错误前提 (docker / heavy-1), 必须改写为 raw_exec / light-1 / pip install |
| T1.2 / T1.4 / T1.5 / T1.6 | done | **保持 done** | 这些是状态机内部逻辑 + Forgejo / schema validator, 与 plugin 加载路径无关 |
| T2-T14 (state machine 全部) | done | **保持 done** | 214 tests pass 验证内部逻辑, 不受 plugin 包结构影响 |
| T15.1 step 1 | done (light-1 volume) | **保持 done** | 已修正 heavy-1 → light-1 |
| T15.1 step 2-5 | pending | **依赖 T1.1+1.3+1.7 重做** | 必须先有 pip-installable package |

## 工时影响

| 维度 | 原估 | 新估 | Delta |
|------|------|------|-------|
| T1 实际重做 | 0h (已 done) | +4-6h | +4-6h |
| T15.1 part 2 (image build → pip install) | 5h | 1h (大幅简化) | -4h |
| **净增加** | | | **+0~+2h** (容差范围内) |

接受 OD-8 = 156h 基线下不调整。M2 总预算仍 156h。

## 治理动作

1. **本 OD 文件**: 这份 (`.aria/decisions/2026-05-02-od-10-t1-ad3-deviation-finding.md`)
2. **AD-M2-7** 新增决议位回填: 在 `aria-orchestrator/docs/architecture-decisions.md` AD-M2-* 段加 AD-M2-7 — "Hermes Extension Plugin 实施路径锁定 (pip entry-point per AD3)"
3. **tasks.md update**: T1.1/1.3/1.7 标 reopened + 引用本 OD
4. **proposal.md note**: §What 一末尾加注 "T1 实施偏离 AD3 finding + OD-10 锁定 pip entry-point 路径"
5. **post-mortem 记忆**: 写一条 feedback memory: `feedback_unit_tests_dont_validate_plugin_loading.md` — "Plugin 类 task 必须有 integration test 验证真实加载路径, 单元测试 mock 化覆盖不到 plugin 包结构错误"

## 时间线

| 时间 | 事件 |
|------|------|
| 2026-04-28 | T1.1 实施期, 决定 plugin.json 格式 (与 AD3 偏离, 但 unit tests 全 pass 没暴露) |
| 2026-04-28 | post_spec audit (R1-R3) 通过 (audit 范围限于 spec 自身, 未交叉验证 hermes 包结构) |
| 2026-04-29 | T6.1 实施期, `_register_with_hermes_scheduler` 写为 NotImplementedError stub (vendor liaison 假设) |
| 2026-04-29 | T1.7 DEPLOYMENT.md 起草 (基于 M1 docker base infra 假设, 未实测 hermes raw_exec 模式) |
| 2026-04-29 | Phase B.2 startup commit (fde643b), T1 标 done |
| 2026-04-23~30 | T2-T14 实施完成, 214 tests pass, 没有 integration test 触及 hermes 真实加载 |
| 2026-05-02 | T15.1 deployment session, AI 通过 `nomad job inspect aria-orchestrator` + `hermes plugins list` + `hermes_cli/plugins.py` 源码读取发现偏移 |
| 2026-05-02 | OD-10 锁定 [A] 修复路径 (本 doc) |

## 后续 (T1 修复期间)

OD-10 不阻塞其他 M2 工作 — T16 patches 已完成, T16.1/2/4 仍待 T15 metrics, 路径不变。

修复完成后, T1.done 重新声明 (新增条件 "hermes plugins list 包含 aria-layer1 enabled + hermes cron list 含 aria_layer1_tick + 单次手动 tick 触发 PASS")。
