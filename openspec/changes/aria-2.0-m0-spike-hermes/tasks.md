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

- [ ] **ST1.1** 克隆 NousResearch/hermes-agent v0.7+ upstream (0.5h)
  - 推到 `forgejo.10cg.pub/10CG/hermes-agent` (fork)
  - 添加 `github` remote 指向 upstream (tracking)
- [ ] **ST1.2** 源码结构分析 (2h)
  - 识别 core/extension/plugin 边界
  - 确认 fork 安全扩展路径 (预期 `internal/aria/` 独立目录)
  - 产出 `spikes/hermes-route/upstream-structure.md`
- [ ] **ST1.3** Fork 骨架建立 (2h)
  - 在 `internal/aria/` 创建 Layer 1 状态机骨架
  - 最小文件: `state_machine.py`, `gateway.py`, `dispatcher.py`, `tests/test_transitions.py`
  - 确保 fork build + upstream test pass 不受影响
- [ ] **ST1.4** Upstream changelog 采集 (1h)
  - `git log --since="6 months ago" --oneline upstream/main | wc -l`
  - 记录到 `spikes/hermes-route/upstream-velocity.txt`
  - 月度中位数: `<count> / 6`
- [ ] **ST1.5** 缓冲 (0.5h)

---

## ST2 — Fork 路径: Rebase 实操 + License 扫描 (10h)

> **ST2 更新 (2026-04-15)**: ST2.3/2.4/2.5 完成 (实际 ~1.5h, 原估 4.5h, 节省 3h)。Primary scan 结果触发 fork 路径自动降级 (AGPL=1 from `ua-parser-js@2.0.9` via browser 子图)。ST2.1/2.2 **有条件推迟**到 ST3.5 Option C POC 结束后, 依据 POC 结果决定是否跑完整 rebase 或缩减为"仅记录"。详见 [license-scan-report.md §8](../../../aria-orchestrator/spikes/hermes-route/license-scan-report.md)。

- [ ] **ST2.1** 第 1 次 rebase 实操 (4h) — **推迟至 ST3.5 POC 后**
  - `git fetch upstream && git rebase upstream/main`
  - 解决所有冲突, 跑 upstream 测试套件确认通过
  - **记录每步工时** (每 0.5h 精度) 到 `spikes/hermes-route/rebase-log.md`
  - 量化指标: 总工时, 冲突文件数, 冲突段数
  - **条件**: 若 ST3.5 Option C POC 成功, 本任务缩减为"仅记录 upstream velocity + 粗估工时", 不执行完整 rebase
- [ ] **ST2.2** 单次 rebase × 1.5 月度估算 (0.5h) — **推迟至 ST3.5 POC 后**
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
- [ ] **ST2.6** 缓冲 (1h)

---

## ST3 — 自研路径: Gateway + SQLite 状态机原型 (20h)

- [ ] **ST3.1** 项目骨架 (1h)
  - `spikes/hermes-route/self-built/` 目录
  - Python 3.11+, pyproject.toml, pytest 配置
  - SQLite schema v0 (dispatches 表, WAL mode)
- [ ] **ST3.2** Gateway stub (飞书 API 最小调用) (4h)
  - 最小飞书 webhook 调用封装
  - Human gate 卡片发送 + approve/reject callback
  - 最小配置: token / chat_id / secret
- [ ] **ST3.3** SQLite 状态持久化 (3h)
  - Active dispatches 表
  - State transition 原子写 (temp file + rename)
  - Crash recovery 扫描逻辑
- [ ] **ST3.4** 9 状态 (简化为 5 状态) 基础实现 (6h)
  - S0_IDLE / S_DISPATCHED / S_RUNNING / S_AWAITING_HUMAN / S_RESUMED / S_FAIL
  - 状态定义 + 合法 transition 表 + 异常处理
- [ ] **ST3.5** 单元测试 (3h)
  - 100% transition 覆盖 (PRD NFR: 状态机单元测试 100%)
  - 跑 `pytest --cov` 确认覆盖率
- [ ] **ST3.6** LoC 统计 (0.5h)
  - `cloc --include-lang=Python --exclude-dir=.venv,__pycache__,migrations .`
  - 业务 LoC vs 测试 LoC 分列
  - 记录到 `spikes/hermes-route/self-built-loc.json`
- [ ] **ST3.7** 实测开发工时记录 (持续, 0.5h 记录)
  - 每个子任务开始/结束打卡
  - 汇总到 `spikes/hermes-route/self-built-hours.md`
- [ ] **ST3.8** 缓冲 (2h)

---

## ST3.5 — Option C POC: Extension-only tool pack (8h, ST1 新发现)

> **背景**: ST1 纸面结构分析发现 hermes-agent v0.9.0 有公开的 `ToolRegistry` 扩展 API (`tools/registry.py` 的 `register()` 方法, 支持外部 Python 包独立注册 tool 而无需 fork core)。本 POC 验证该路径的可行性。

### 前置

- ST2 已完成 (本地 clone hermes-agent) **或** 独立 clone (不依赖 ST2 完成状态)
- Python 3.11+ 环境

### 任务

- [ ] **ST3.5.1** (2h) 搭建 `aria-hermes-tools` Python 包骨架
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

- [ ] **ST3.5.2** (3h) 实现 `aria_hello_world` tool 并验证注册
  - 编写最小 tool, 调用 `hermes_agent.tools.registry.register()` 在模块 import 时注册
  - 本地 `pip install -e .` 到 hermes-agent 虚拟环境
  - 启动 hermes-agent, 验证 `aria_hello_world` 出现在 `/tools` CLI 命令列表中
  - 通过 AIAgent 发送 "call aria hello world" 指令, 验证 tool 被调用
  - **pass 条件**: hermes-agent 日志中看到 `aria_hello_world` 被调用的 trace

- [ ] **ST3.5.3** (2h) 实现 `aria_state_transition` tool + SQLite 集成
  - 定义 SQLite schema: `dispatches(trace_id, state, timestamp, metadata_json)`
  - tool `aria_state_transition(trace_id, from_state, to_state)` 原子写 SQLite
  - 状态合法性校验 (只允许 proposal.md §3 定义的 5 states 4 transitions)
  - 单元测试: 3 次成功转换 + 1 次非法转换 reject
  - **pass 条件**: pytest 通过 + SQLite 文件含正确历史记录

- [ ] **ST3.5.4** (1h) 端到端验证: AIAgent 通过 tool 完成 1 个状态转换序列
  - 场景: AIAgent 接收 "dispatch issue 123" 指令
  - 预期行为: AIAgent 调用 `aria_state_transition(trace_id=123, idle → dispatched)`
  - 验证: SQLite 记录 state=dispatched, AIAgent 返回成功消息
  - **pass 条件**: 1 次完整的 AIAgent → tool → SQLite → 响应 闭环

### ST3.5 验收标准

- [ ] Option C POC 的 4 个子任务全部完成且 pass
- [ ] aria-hermes-tools 包代码量记录 (cloc), 纳入 ST6 量化指标
- [ ] 产出 `spikes/hermes-route/option-c-poc-report.md`, 含:
  - 实现代码路径
  - hermes-agent ToolRegistry API 的使用体验 (有无限制 / 有无坑)
  - AIAgent 调用 external tool 的稳定性观察 (是否触发 prompt caching 问题)
  - 建议: Option C 是否应该成为首选路径

### ST3.5 失败判定

若以下任一发生 → Option C POC 失败, 退回 Option A (fork) 裁决流程:
- ToolRegistry 的 `register()` 抛出异常或需要修改 core 代码
- hermes-agent 启动时无法发现外部注册的 tool
- AIAgent 调用时触发 prompt caching 破坏
- 跨 session 持久化 (SQLite) 与 hermes-agent 的 session 模型冲突

---

## ST4 — 5 状态 4 转换演示 (6h)

**必含转换** (hardcoded):
```
idle → dispatched → running → awaiting_human → resumed
```
覆盖正常路径 + 1 个 human-in-loop。

- [ ] **ST4.1** 双路径各实现演示脚本 (4h)
  - `spikes/hermes-route/demo-fork.py` (基于 ST1 fork 骨架)
  - `spikes/hermes-route/demo-self-built.py` (基于 ST3 自研)
  - 每个脚本独立跑通 5 状态 4 转换, 产出 JSON 日志
- [ ] **ST4.2** 对比报告 (1.5h)
  - 代码量 / 运行时行为 / 扩展性差异
  - 记录到 `spikes/hermes-route/demo-comparison.md`
- [ ] **ST4.3** 缓冲 (0.5h)

---

## ST5 — 元知识 Prompt v0.1 起草 + 实跑 (3h)

- [ ] **ST5.1** 起草 ~1K token 元知识 prompt (1h)
  - 基于 PRD §元知识 (line 260-282) 示例
  - 核心: Aria 方法论摘要 + 十步循环 + OpenSpec 三档 + 不可协商规则
  - Token 计数工具: `tiktoken` (GPT-4 encoding 近似), 目标 ≤ 1200 token
- [ ] **ST5.2** 在 Spike gateway (ST3) 实跑 (1.5h)
  - 将 prompt 注入到 GLM 5.1 调用 (使用合成 fixture, 禁真实数据)
  - 验证 token 预算 + prompt 格式可行性
  - 产出 `spikes/hermes-route/meta-knowledge-v0.1.md` + 实跑日志
- [ ] **ST5.3** 缓冲 (0.5h)

---

## ST6 — 量化数据收集 + Spike Report (5h)

- [ ] **ST6.1** 量化数据汇总 (1.5h)
  - 从 ST2 (fork rebase 实测), ST3.6 (自研 LoC), ST3.7 (自研工时), ST1.4 (velocity) 汇总到 `spikes/hermes-route/metrics.json`
- [ ] **ST6.2** 裁决矩阵填写 (0.5h)
  - 应用 proposal.md 裁决规则:
    - fork: `monthly_rebase_hours ≤ 20 && gpl_agpl_count == 0 && unknown_count == 0`
    - 自研: `cloc_python_loc ≤ 1000 && dev_hours ≤ 60`
  - 输出: `fork_verdict`, `self_verdict`, `recommendation`
- [ ] **ST6.3** Spike Report 撰写 (2h)
  - `openspec/changes/aria-2.0-m0-spike-hermes/spike-report.md`
  - 章节: 背景 / 方法 / 量化数据 / 裁决矩阵 / 推荐 / AD3 修订建议 / 风险与限制
  - LGPL 出现时, 额外章节 "legal-advisor 人工研判待定"
- [ ] **ST6.4** AD3 修订建议起草 (0.5h)
  - 若 Spike 结论与 PRD AD3 一致 → 无需 patch
  - 若矛盾 → 起草 AD3 patch 文本, 待父 Spec T6 PRD patch PR 使用
- [ ] **ST6.5** 缓冲 (0.5h)

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

- [ ] 所有 ST1-ST6 任务完成且有证据归档
- [ ] `metrics.json` 完整
- [ ] `spike-report.md` 产出, 含裁决矩阵 + 推荐
- [ ] 裁决结论 (`fork` / `self-built` / `hybrid` / `r8_exit`) 回填到父 Spec `m0-handoff.yaml.ad3_conclusion`
- [ ] 若触发 PRD AD3 修订 → patch 文本已起草 (父 Spec T6.3 使用)
- [ ] Spike Report 路径在 `m0-handoff.yaml.spike_code_path` 记录

## 关联文档

- [proposal.md](./proposal.md)
- [父 Spec](../aria-2.0-m0-prerequisite/)
- [US-020](../../../docs/requirements/user-stories/US-020.md)
