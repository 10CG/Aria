# aria-2.0-m0-spike-hermes — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-020](../../../docs/requirements/user-stories/US-020.md)
> **Total**: ~52h (timeboxed 1 sprint, 硬边界 > 60h 评估, > 72h 终止)

## Task 分解

| ID | Task | 工时 | 依赖 |
|---|---|---|---|
| ST1 | Hermes upstream 源码分析 + fork 骨架 | 6h | T1.pass (父 Spec) |
| ST2 | fork 路径: 1 次 rebase 实操 + license 扫描 | 10h | ST1 |
| ST3 | 自研路径: gateway + SQLite 状态机原型 | 20h | — |
| ST4 | 5 状态 4 转换演示 (双路径各实现 1 次) | 6h | ST1, ST3 |
| ST5 | 元知识 prompt v0.1 起草 + 实跑 | 3h | ST3 |
| ST6 | 量化数据收集 + Spike Report 撰写 | 5h | ST2, ST3, ST4, ST5 |
| ST7 | 缓冲 | 2h | — |
| **Total Core** | | **50h** | |
| **+ Buffer** | | **2h** | |
| **Grand Total** | | **52h** | |

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

- [ ] **ST2.1** 第 1 次 rebase 实操 (4h)
  - `git fetch upstream && git rebase upstream/main`
  - 解决所有冲突, 跑 upstream 测试套件确认通过
  - **记录每步工时** (每 0.5h 精度) 到 `spikes/hermes-route/rebase-log.md`
  - 量化指标: 总工时, 冲突文件数, 冲突段数
- [ ] **ST2.2** 单次 rebase × 1.5 月度估算 (0.5h)
  - 月度估算 = ST2.1 实测工时 × 1.5 (固定系数)
  - 产品负责人可上调至 ×2.0 (裁决时), > ×2.0 需 tech-lead 第二签字
  - 附 ST1.4 upstream velocity 数据作为上调依据参考
- [ ] **ST2.3** License 扫描 - JS 依赖 (2h)
  - `cd hermes-fork && npm ls --all`
  - `license-checker --production --json --out license-js.json`
  - 识别 direct + transitive 全量, 输出 GPL/AGPL/LGPL/Unknown 分类
- [ ] **ST2.4** License 扫描 - Python 依赖 (如有) (1h)
  - `pip-licenses --format=json --with-system --output-file license-py.json`
  - 同 ST2.3 分类处理
- [ ] **ST2.5** License matrix 汇总 (1.5h)
  - 合并 ST2.3 + ST2.4 到 `spikes/hermes-route/license-matrix.json`
  - 全表: direct / transitive / package / license / risk_level
  - 汇总: `gpl_count`, `agpl_count`, `lgpl_count`, `unknown_count`
  - **触发条件**:
    - `gpl_count + agpl_count > 0` 或 `unknown_count ≥ 1` → fork 路径自动降级 (标记到 Spike Report)
    - `lgpl_count > 0` → 人类 legal-advisor 研判, 不自动降级
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
