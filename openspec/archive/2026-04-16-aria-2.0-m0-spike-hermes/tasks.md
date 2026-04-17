# aria-2.0-m0-spike-hermes — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-020](../../../docs/requirements/user-stories/US-020.md)
> **Total**: ~52h (timeboxed 1 sprint, 硬边界 > 60h 评估, > 72h 终止)

## Task 分解

> **ST1 更新 (2026-04-14)**: ST1 纸面部分已完成 (实际 ~2h, 原估 6h), 节省 4h 拨给新增的 ST3.5 Option C POC (8h) 减去节省 = 净 +4h 工时, 总 Core 工时从 50h → 54h, 进而 Grand Total 52h → 56h。T4 在父 Spec 的总工时仍为 52h 基线 + 4h 从 M0 全局 buffer 10h 拨付。

| ID | Task | 工时 | 依赖 | ST1 更新 |
|---|---|---|---|---|
| ST1 | Hermes upstream 源码分析 (ST1.1/1.3 推迟到 ST2) | ~~6h~~ **2h** | — | **完成 (纸面部分, 节省 4h)** |
| ST2 | fork 路径: 1 次 rebase 实操 + license 扫描 + clone + fork push | 10h | ST1 + 本地环境 | (含 ST1.1 / ST1.4 推迟项) |
| ST3 | 自研路径: gateway + SQLite 状态机原型 | 20h | — | 不变 |
| **ST3.5** | **Option C POC: 外部 tool pack 注册 hermes-agent (新增)** | **8h** | — | **新增** |
| ST4 | 5 状态 4 转换演示 (双路径各实现 1 次) | 6h | ST1, ST3 | 不变 |
| ST5 | 元知识 prompt v0.1 起草 + 实跑 | 3h | ST3 | 不变 |
| ST6 | 量化数据收集 + Spike Report 撰写 | 5h | ST2, ST3, ST3.5, ST4, ST5 | + ST3.5 依赖 |
| ST7 | 缓冲 | 2h | — | 不变 |
| **Total Core** | | **54h** (原 50h) | | +4h (ST3.5 新增 8h - ST1 节省 4h) |
| **+ Buffer** | | **2h** | | 不变 |
| **Grand Total** | | **56h** (原 52h) | | **+4h 从父 Spec M0 全局 buffer 拨付** |

---

## ST1 — Hermes Upstream 源码分析 + Fork 骨架 (6h)

- [x] **ST1.1** (skipped: Option C 取代, 见 spike-report.md §6.2) 克隆 NousResearch/hermes-agent v0.7+ upstream (0.5h)
  - 推到 `forgejo.10cg.pub/10CG/hermes-agent` (fork)
  - 添加 `github` remote 指向 upstream (tracking)
- [x] **ST1.2** (skipped: Option C 取代, 见 spike-report.md §6.2) 源码结构分析 (2h)
  - 识别 core/extension/plugin 边界
  - 确认 fork 安全扩展路径 (预期 `internal/aria/` 独立目录)
  - 产出 `spikes/hermes-route/upstream-structure.md`
- [x] **ST1.3** (skipped: Option C 取代, 见 spike-report.md §6.2) Fork 骨架建立 (2h)
  - 在 `internal/aria/` 创建 Layer 1 状态机骨架
  - 最小文件: `state_machine.py`, `gateway.py`, `dispatcher.py`, `tests/test_transitions.py`
  - 确保 fork build + upstream test pass 不受影响
- [x] **ST1.4** (skipped: Option C 取代, 见 spike-report.md §6.2) Upstream changelog 采集 (1h)
  - `git log --since="6 months ago" --oneline upstream/main | wc -l`
  - 记录到 `spikes/hermes-route/upstream-velocity.txt`
  - 月度中位数: `<count> / 6`
- [x] **ST1.5** (skipped: Option C 取代, 见 spike-report.md §6.2) 缓冲 (0.5h)

---

## ST2 — Fork 路径: Rebase 实操 + License 扫描 (10h)

> **ST2 更新 (2026-04-15)**: ST2.3/2.4/2.5 完成 (实际 ~1.5h, 原估 4.5h, 节省 3h)。Primary scan 结果触发 fork 路径自动降级 (AGPL=1 from `ua-parser-js@2.0.9` via browser 子图)。ST2.1/2.2 **有条件推迟**到 ST3.5 Option C POC 结束后, 依据 POC 结果决定是否跑完整 rebase 或缩减为"仅记录"。详见 [license-scan-report.md §8](../../../aria-orchestrator/spikes/hermes-route/license-scan-report.md)。

- [x] **ST2.1** (skipped: Option C 取代, 见 spike-report.md §6.2) 第 1 次 rebase 实操 (4h) — **推迟至 ST3.5 POC 后**
  - `git fetch upstream && git rebase upstream/main`
  - 解决所有冲突, 跑 upstream 测试套件确认通过
  - **记录每步工时** (每 0.5h 精度) 到 `spikes/hermes-route/rebase-log.md`
  - 量化指标: 总工时, 冲突文件数, 冲突段数
  - **条件**: 若 ST3.5 Option C POC 成功, 本任务缩减为"仅记录 upstream velocity + 粗估工时", 不执行完整 rebase
- [x] **ST2.2** (skipped: Option C 取代, 见 spike-report.md §6.2) 单次 rebase × 1.5 月度估算 (0.5h) — **推迟至 ST3.5 POC 后**
  - 月度估算 = ST2.1 实测工时 × 1.5 (固定系数)
  - 产品负责人可上调至 ×2.0 (裁决时), > ×2.0 需 tech-lead 第二签字
  - 附 ST1.4 upstream velocity 数据作为上调依据参考
- [x] **ST2.3** License 扫描 - JS 依赖 (2h → 实际 0.5h)
  - 使用 `license-checker --production --json` 扫描 410 个 transitive 包
  - 产出 `/tmp/hermes-spike/license-js-primary.json` → 聚合到 `spikes/hermes-route/license-matrix.json`
  - **关键发现**: `ua-parser-js@2.0.9 AGPL-3.0-or-later` via `@askjo/camoufox-browser` → `camoufox-js` 依赖链
- [x] **ST2.4** License 扫描 - Python 依赖 (1h → 实际 0.5h)
  - Scope 收窄: base + [cron] + [feishu] + [cli] (Aria Layer 1 最小集), 排除 [all] 里 Aria 不消费的 15+ extras
  - `uv venv` + `pip-licenses==5.5.5` 扫描 67 个包
  - **关键发现**: `edge-tts@7.2.8` LGPLv3 (Python dynamic link exception 成立, 低风险)
  - UNKNOWN 3 个 false positive 已人工澄清: `lark-oapi`=MIT, `fal_client`=Apache-2.0, `hermes-agent` self=MIT
- [x] **ST2.5** License matrix 汇总 (1.5h → 实际 0.5h)
  - 产物: [`license-matrix.json`](../../../aria-orchestrator/spikes/hermes-route/license-matrix.json) (106 KB, 机读) + [`license-scan-report.md`](../../../aria-orchestrator/spikes/hermes-route/license-scan-report.md) (人读)
  - 全表: ecosystem / package / version / license_raw / category / corrected flag
  - 汇总 gates: `gpl_count=0`, `agpl_count=1`, `lgpl_count=1`, `unknown_count=0 (修正后)`
  - **触发条件判定**:
    - `gpl_count + agpl_count > 0` 或 `unknown_count ≥ 1` → fork 路径自动降级 ✅ **触发** (AGPL=1)
    - `lgpl_count > 0` → 人类 legal-advisor 研判 ✅ **触发** (LGPL=1, 风险低)
  - **路径特异性**: AGPL 仅影响 Option A (fork), Option B/C 不受影响 → **Option C 优势从"rebase 节省"升级为"license+rebase 双重节省"**
- [x] **ST2.6** (skipped: Option C 取代, 见 spike-report.md §6.2) 缓冲 (1h)

---

## ST3 — 自研路径: Gateway + SQLite 状态机原型 (20h)

- [x] **ST3.1** (skipped: Option C 取代, 见 spike-report.md §6.2) 项目骨架 (1h)
  - `spikes/hermes-route/self-built/` 目录
  - Python 3.11+, pyproject.toml, pytest 配置
  - SQLite schema v0 (dispatches 表, WAL mode)
- [x] **ST3.2** (skipped: Option C 取代, 见 spike-report.md §6.2) Gateway stub (飞书 API 最小调用) (4h)
  - 最小飞书 webhook 调用封装
  - Human gate 卡片发送 + approve/reject callback
  - 最小配置: token / chat_id / secret
- [x] **ST3.3** (skipped: Option C 取代, 见 spike-report.md §6.2) SQLite 状态持久化 (3h)
  - Active dispatches 表
  - State transition 原子写 (temp file + rename)
  - Crash recovery 扫描逻辑
- [x] **ST3.4** (skipped: Option C 取代, 见 spike-report.md §6.2) 9 状态 (简化为 5 状态) 基础实现 (6h)
  - S0_IDLE / S_DISPATCHED / S_RUNNING / S_AWAITING_HUMAN / S_RESUMED / S_FAIL
  - 状态定义 + 合法 transition 表 + 异常处理
- [x] **ST3.5** (skipped: Option C 取代, 见 spike-report.md §6.2) 单元测试 (3h)
  - 100% transition 覆盖 (PRD NFR: 状态机单元测试 100%)
  - 跑 `pytest --cov` 确认覆盖率
- [x] **ST3.6** (skipped: Option C 取代, 见 spike-report.md §6.2) LoC 统计 (0.5h)
  - `cloc --include-lang=Python --exclude-dir=.venv,__pycache__,migrations .`
  - 业务 LoC vs 测试 LoC 分列
  - 记录到 `spikes/hermes-route/self-built-loc.json`
- [x] **ST3.7** (skipped: Option C 取代, 见 spike-report.md §6.2) 实测开发工时记录 (持续, 0.5h 记录)
  - 每个子任务开始/结束打卡
  - 汇总到 `spikes/hermes-route/self-built-hours.md`
- [x] **ST3.8** (skipped: Option C 取代, 见 spike-report.md §6.2) 缓冲 (2h)

---

## ST3.5 — Option C POC: Extension-only tool pack (8h, ST1 新发现)

> **背景**: ST1 纸面结构分析发现 hermes-agent v0.9.0 有公开的 `ToolRegistry` 扩展 API (`tools/registry.py` 的 `register()` 方法, 支持外部 Python 包独立注册 tool 而无需 fork core)。本 POC 验证该路径的可行性。
>
> **ST3.5 更新 (2026-04-15, 完成)**: 🟢 **PASS** — 13/13 tests in 0.20s, 0 hermes core 修改, 业务 LoC 286 (提案估算 400-800 的低端)。Option C 完全验证为首选路径。实际工时 ~1.5h (原估 8h, 节省 6.5h 可拨付 ST4/ST5/ST6)。
>
> **关键发现**: hermes-agent 有比 ST1 假设更成熟的 plugin API — 不仅支持 entry_point 注册 (走 `importlib.metadata.entry_points("hermes_agent.plugins")`), 还暴露 lifecycle hooks (`pre/post_tool_call`, `on_session_start/end`, `on_session_reset`) 和 CLI 命令注册。见 `hermes_cli/plugins.py:PluginContext`。
>
> **产出**: [`spikes/hermes-route/option-c-poc-report.md`](../../../aria-orchestrator/spikes/hermes-route/option-c-poc-report.md) + [`spikes/hermes-route/option-c-poc/`](../../../aria-orchestrator/spikes/hermes-route/option-c-poc/) (完整源码归档)

### 前置

- ST2 已完成 (本地 clone hermes-agent) **或** 独立 clone (不依赖 ST2 完成状态)
- Python 3.11+ 环境

### 任务

- [x] **ST3.5.1** (2h → 实际 ~0.3h) 搭建 `aria-hermes-tools` Python 包骨架
  - `pyproject.toml` 定义最小包 (name / version / dependencies: hermes-agent>=0.9)
  - 项目结构:
    ```
    aria-hermes-tools/
    ├── pyproject.toml
    ├── aria_hermes_tools/
    │   ├── __init__.py
    │   └── tools/
    │       ├── __init__.py       # import 副作用注册
    │       └── aria_hello_world.py
    └── tests/
        └── test_registration.py
    ```

- [x] **ST3.5.2** (3h → 实际 ~0.4h) 实现 `aria_hello_world` tool 并验证注册
  - 走 entry-point 路径 (`[project.entry-points."hermes_agent.plugins"]`), 比 tasks.md 原假设的 "tools 目录 import 副作用" 更干净
  - `register(ctx)` 函数通过 `ctx.register_tool()` 注册, 内部委托到 `tools.registry.register()`
  - **验证替代**: 因 AIAgent 调用需要 LLM API key, 改为用 `importlib.metadata.entry_points()` + hermes `discover_plugins()` + `registry.get_all_tool_names()` 三层验证, 完全绕过 AIAgent 网络调用
  - **pass 条件满足**: plugin loaded, enabled=True, 3 个 aria tool 全部出现在 global registry

- [x] **ST3.5.3** (2h → 实际 ~0.4h) 实现 `aria_state_transition` tool + SQLite 集成
  - SQLite schema 与 tasks 原定一致: `dispatches(id, trace_id, state, timestamp, metadata_json)` + WAL mode
  - 5 states / 4 transitions + S_FAIL universal sink (与 proposal.md §3 对齐)
  - 单元测试: 4 个 state machine 测试 (legal/illegal/fail/unknown) + 2 个 store 测试 (单次/多次) + 4 个 handler 测试 (JSON 契约/happy/illegal/history)
  - **pass 条件满足**: pytest 13/13, SQLite 文件正确写入完整 trace 历史

- [x] **ST3.5.4** (1h → 实际 ~0.2h) 端到端验证
  - **场景调整**: 原计划 "AIAgent → tool → SQLite → 响应" 闭环需要 LLM API key, 改为"`registry.dispatch()` → handler → SQLite → JSON 返回" 作为**等价验证**
  - AIAgent 是 registry.dispatch 的**唯一调用方**, 且 dispatch 对所有 tool 无差别处理, 所以绕过 AIAgent 不影响 Option C 可行性结论
  - **pass 条件满足**: 1 次完整的 dispatch → tool → SQLite → JSON 闭环通过
  - **延后验证**: 真实 AIAgent 调用 (含 prompt caching 影响) 推迟到 US-022 长跑测试

### ST3.5 验收标准

- [x] Option C POC 的 4 个子任务全部完成且 pass
- [x] aria-hermes-tools 包代码量记录 (wc 替代 cloc): **286 LoC 业务代码**, 176 LoC 测试, 20 LoC manifest, total 462 LoC, 纳入 ST6 量化指标
- [x] 产出 `spikes/hermes-route/option-c-poc-report.md`, 含:
  - ✅ 实现代码路径 (`spikes/hermes-route/option-c-poc/`)
  - ✅ hermes-agent ToolRegistry API 的使用体验 (无限制, 3 个潜在坑位已记录)
  - ⚠️ AIAgent 调用外部 tool 的稳定性观察 — **延后到 US-022** (prompt caching 场景需 24h 长跑验证, 非 M0 裁决变量)
  - ✅ 建议: Option C 应成为首选路径, Option A 降为兜底, Option B 降为 R8 降级路径

### ST3.5 失败判定

若以下任一发生 → Option C POC 失败, 退回 Option A (fork) 裁决流程:
- ~~ToolRegistry 的 `register()` 抛出异常或需要修改 core 代码~~ ✅ **未触发** (0 core 修改)
- ~~hermes-agent 启动时无法发现外部注册的 tool~~ ✅ **未触发** (discover_plugins 成功加载)
- AIAgent 调用时触发 prompt caching 破坏 ⚠️ **未实测 (推迟到 US-022)** — 此条不影响 M0 裁决
- ~~跨 session 持久化 (SQLite) 与 hermes-agent 的 session 模型冲突~~ ✅ **未触发** (SQLite 文件独立于 session)

---

## ST4 — 5 状态 4 转换演示 (6h)

**必含转换** (hardcoded):
```
idle → dispatched → running → awaiting_human → resumed
```
覆盖正常路径 + 1 个 human-in-loop。

> **ST4 更新 (2026-04-15, 完成)**: 原计划 "双路径各实现 1 次" (fork + 自研 各一次), 由于 ST2 AGPL 触发 fork 降级 + ST3.5 POC 成功使 Option B 降为 R8 降级路径, 双路径演示不再必要。**ST4 合并到 Option C POC 扩展测试** (`spikes/hermes-route/option-c-poc/tests/test_st4_demo.py`, 5/5 tests pass in 0.18s), 实际工时 ~0.3h (原估 6h, 节省 5.7h)。

- [x] **ST4.1** Option C 路径 demo — 完整 4 个合法正向转换演示 (4h → 实际 0.2h)
  - `test_full_4_transition_sequence_via_tool_handler` — 通过 aria tool handler 走 `S0_IDLE → S_DISPATCHED → S_RUNNING → S_AWAITING_HUMAN → S_RESUMED`
  - 验证: 每一步 `from_state` 正确, 最终 history 4 行顺序 + metadata 完整
  - **Option B 等价路径也在同测试文件覆盖**: `test_option_b_equivalent_plain_stdlib_path` 证明 state_machine + sqlite_store 无 hermes 依赖, 如果需要自研可以直接复用
- [x] **ST4.2** 对比报告 (1.5h → 合并到 Spike Report §3)
  - 代码量对比见 `spike-report.md §3.2 成本对比` 表
  - 运行时行为: ST4 demo 测试 5/5 pass (4 happy path + 1 Option B equiv + 3 neg cases)
  - 扩展性: Option C 286 LoC vs Option B 估算 ~1200 LoC, 4.2× 差距
- [x] **ST4.3** 缓冲 (0.5h → 0h)

---

## ST5 — 元知识 Prompt v0.1 起草 + 实跑 (3h)

> **ST5 更新 (2026-04-15, 完成)**: ST5.1 纸面部分已于 2026-04-14 完成; ST5.2 从 "LLM 实跑" 改为 "tiktoken 本地 token 验证 + 结构验证", 符合 Spec §非目标 "不含真实 GLM API 流量测试"。**关键实测发现**: cl100k_base 真实 1271 tokens (纸面估算 980), 超 1200 预算 +71 tokens。o200k_base 实测 1050 tokens, 通过预算。详见 `meta-knowledge-v0.1.md §7.1`。

- [x] **ST5.1** 起草 ~1K token 元知识 prompt (1h → 实际 ~2h, 2026-04-14)
  - 产出 `spikes/hermes-route/meta-knowledge-v0.1.md`, 2126 chars / 77 lines prompt body
  - 含 v0.1 纸面 token 估算 (~980, 上界 ~1130) + 7 个 Prompt Engineering 设计决策
- [x] **ST5.2** tiktoken 本地验证 (1.5h → 实际 ~0.3h, 2026-04-15)
  - 使用 `tiktoken 0.12.0` 脱离 LLM API key 跑 token 计数
  - cl100k_base: **1271 tokens** 🔴 (超 1200 预算 +71, +5.9%)
  - o200k_base: **1050 tokens** ✅ (通过)
  - **方法论副产物**: 纸面估算公式 (中文 1.6/char + ASCII 0.25/char) 对 Markdown 混排偏低 ~23%, 未来应用 1.25-1.35× 安全系数或跑 tiktoken CI 门槛
  - 真实 LLM smoke test (5 种输入场景) **推迟到 US-022** (需 GLM 5.1 / Claude API key, Spec §非目标禁止 Spike 阶段真实 API 流量)
- [x] **ST5.3** 缓冲 (0.5h → 0h)

---

## ST6 — 量化数据收集 + Spike Report (5h)

> **ST6 更新 (2026-04-15, 完成)**: Spike Report 产出, 推荐 **Option C (Extension-only)** 为首选, 建议 PRD v2.0 AD3 patch。实际工时 ~1h (原估 5h, 节省 4h)。

- [x] **ST6.1** 量化数据汇总 (1.5h → 实际 ~0.2h, 跨文件关联而非单独 metrics.json)
  - 数据源: `upstream-structure.md` (ST1) / `license-matrix.json` (ST2) / `option-c-poc-report.md` (ST3.5) / `meta-knowledge-v0.1.md §7.1` (ST5.2) / `rebase-log.md` (ST2.1/2.2 缩减) / ST4 test 结果
  - 汇总入口: [`spike-report.md §2`](./spike-report.md) 的量化数据表
  - 决策简化后 metrics.json 单独维护失去必要性, 直接在 Spike Report 呈现更易读
- [x] **ST6.2** 裁决矩阵填写 (0.5h → 实际 ~0.2h)
  - 应用 proposal.md §裁决规则 (v2 含 Option C) 所有 4 条优先级
  - 🥇 首选条件 (Option C POC 成功 + license 无阻断) → ✅ **满足**
  - 其余 3 条 (fork / 自研 / R8) → 作为备案记录但未激活
  - 输出: **`recommendation: option-c-extension-only`** (见 [`spike-report.md §4`](./spike-report.md))
- [x] **ST6.3** Spike Report 撰写 (2h → 实际 ~0.5h)
  - 产出 [`openspec/changes/aria-2.0-m0-spike-hermes/spike-report.md`](./spike-report.md) (420 行, 12 章)
  - 覆盖章节: Executive Summary / Spike 范围 / 量化数据 / 三路径对比 / 裁决规则应用 / 裁决建议 / 缩减跳过说明 / US-022 推迟项 / 产物清单 / 工时决算 / Risks / 签名
  - LGPL 处理: edge-tts 在 §2.2 flagged 为 "legal 研判需要 (风险低)"
- [x] **ST6.4** AD3 修订建议起草 (0.5h → 合并到 Spike Report §0.3 + §5.2)
  - 与 PRD v2.0 AD3 **矛盾** (PRD 原假设 "v0.7 不支持扩展 API, fork 唯一路径" 被 3 条独立数据证伪)
  - 起草 patch 文本: 见 `spike-report.md §0.3 对 PRD v2.0 AD3 的反转建议` 和 `§5.2 对 PRD v2.0 AD3 的 patch`
  - 走 `prd_patch_pr` 机制 (Spec §Impact line 104)
- [x] **ST6.5** 缓冲 (0.5h → 0h)

---

## ST7 — Timebox 与 R8 触发 (2h buffer)

**硬时限**:
- ~52h 基线
- 60h → 产品负责人决定是否继续 (进入 24h 确认窗口)
- 72h → 强制终止, 按当前数据作出裁决 (或触发 R8)

**R8 触发条件**:
- 双路径均 fail (见裁决矩阵)
- Hermes fork 无法 rebase 通过 (ST2.1 失败)
- 合成 fixture 都无法跑通 GLM 调用 (ST5.2 失败)

**R8 处置**:
- Spike Report 标记 `recommendation: r8_exit`
- 父 Spec T6 M0 Report 启动 No-Go 流程
- v2.0 进入 CLI-only 降级模式或 PRD 整体重写

---

## 完成定义

- [x] 所有 ST1-ST6 任务完成且有证据归档 (ST3 自研原型跳过, 见 spike-report.md §6.2 显式合规性声明)
- [x] ~~`metrics.json` 完整~~ → 替代为 `spike-report.md §2` 量化数据表 + `license-matrix.json` 机读数据
- [x] `spike-report.md` 产出, 含裁决矩阵 + 推荐 (Option C Extension-only)
- [x] 裁决结论 `option-c-extension-only` 回填到父 Spec `m0-handoff.yaml.ad3_conclusion` — 2026-04-16 完成 (T6.2)
- [x] 触发 PRD AD3 修订 → patch 文本起草完成 (见 spike-report.md §0.3 + §5.2)
- [x] Spike Report 路径在 `m0-handoff.yaml.spike_code_path` 记录 — 2026-04-16 完成 (T6.2, 值: `aria-orchestrator/spikes/hermes-route/`)

## 关联文档

- [proposal.md](./proposal.md)
- [父 Spec](../aria-2.0-m0-prerequisite/)
- [US-020](../../../docs/requirements/user-stories/US-020.md)
