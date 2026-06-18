# M7 Spec Tasks — Fleet Cross-Project Read-Only Aggregation (MVP)

> **Spec**: [aria-2.0-m7-fleet-aggregation](./proposal.md)
> **Level**: 3 (Full)
> **Status**: **Draft** (pending Phase A.2 audit → approval; tasks 待 A.2 收敛后进 Phase A.3 agent 分配 → Phase B.1)
> **Created**: 2026-06-18
> **Brainstorm Source**: `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md` (§2-§8) + D1-D6 (`.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`)
> **Estimated total**: ~26h impl (~11h TG-A + ~9h TG-B + ~6h TG-C); Phase A audit overhead ~1h
> **Agents**: (待 Phase A.3 分配) backend-architect (TG-A 取数+聚合 lead) + backend-architect/qa-engineer (TG-B 降维+接口) + knowledge-manager (TG-C workspace+文档)

---

## Phase B precondition (hard gate — 不满足不得开 Phase B)

D3 时机门 (D1-D6 approved): **M6 release-closeout 已 ship** 后方可开本 Spec Phase B。
开 Phase B 前确认:

```bash
# 1. M6 sequential Spec 已归档 (D3 时机门)
ls openspec/archive/ | grep -i 'aria-2.0-m6-release-closeout'   # 须存在
# 2. aria-orchestrator extension host 就绪 (hermes-extensions/aria-layer1 既有 pattern)
ls aria-orchestrator/hermes-extensions/aria-layer1/             # 须存在 (extension 承载证据)
```

若 M6 未 ship → Phase B 阻塞 (D3: NOT before M6)。

---

## Task Group Overview

| Group | Topic | Scope ref | Est | Agent |
|-------|-------|-----------|-----|-------|
| TG-A-scaffold | tool pack 骨架 + config loader (L2 注入边界) | §What A.1, C.1 | ~2h | backend-architect |
| TG-A-read | ①读 取数 + snapshot_age (mtime 权威) | §What A.2 | ~2.5h | backend-architect |
| TG-A-refresh | ②刷新 scan.py 调用 + 退出码契约 + 幂等回归 | §What A.3 | ~3.5h | backend-architect |
| TG-A-aggregate | 跨项目汇总引擎 + fail-soft | §What A.4 | ~3h | backend-architect |
| TG-B-health | 健康/卡点降维 (7 信号防御式访问) | §What B.1 | ~4h | qa-engineer |
| TG-B-readonly | 只读契约守卫 + no-cross-action | §What B.2 | ~1.5h | qa-engineer |
| TG-B-toolpack | fleet_status/project/blocked 接口 + data+text | §What B.3 | ~3.5h | backend-architect |
| TG-C-yaml | projects.yaml schema + config 校验 | §What C.1 | ~2h | knowledge-manager |
| TG-C-schemaver | 跨 plugin schema 版本容忍 | §What C.2 | ~1.5h | knowledge-manager |
| TG-C-docs | 三层映射 README + D1-D6 + Q-1..Q-5 | §What C.3 | ~2.5h | knowledge-manager |

---

## TG-A — 取数与聚合引擎 (L1 核心, ~11h)

- [ ] **TA-scaffold-1** (FIRST task — 创建 extension host): 创建 `aria-orchestrator/extensions/aria-fleet/`
  目录 (recon 确认 `extensions/` 当前不存在, D5 规划位置)。落地骨架:
  `aria_fleet/{__init__,config,acquire,health,aggregate,toolpack}.py` + `tests/` + `README.md`。
  复用 `hermes-extensions/aria-layer1/` extension pattern。stdlib + PyYAML only。
  **验证**: `from aria_fleet import toolpack` 可 import。 [AC-1]
  - deps: (Phase B precondition gate)

- [ ] **TA-scaffold-2** `config.py` projects.yaml loader (L2 注入边界): 读 projects.yaml →
  返回 `{projects[], refresh_threshold_hours, scan_script_path}`。所有 host 路径 / scan.py 路径
  从 yaml 注入, **L1 代码零 hardcode** (D1-D6 hard constraint #1/#2)。缺字段给明确校验错误。
  单测: 合法 yaml / 缺 projects / 缺 path 字段。
  - deps: TA-scaffold-1

- [ ] **TA-read-1** `acquire.read_snapshot(project)` ①读 默认快路径: 读
  `<path>/.aria/state-snapshot.json` → 解析 JSON → 计算 `snapshot_age` (**文件 mtime 权威**,
  CAVEAT-age: snapshot 顶层无 generated_at)。不触网不跑 scan。无快照项目 → `{available:false,
  reason:"no-snapshot"}` fail-soft。mtime stat 失败 → age=null。
  单测: 有快照 / 无快照 / mtime-fail(null age)。 [AC-2]
  - deps: TA-scaffold-2

- [ ] **TA-read-2** snapshot 解析防御: 顶层缺键 / JSON 损坏 → fail-soft 标 reason, 不抛。
  确认 `issue_status` 用 `in` 检测顶层键 (未配置 issue 扫描的项目可能缺失; **无 enabled 子字段**, caveat-3); post-v1.0 additive 字段
  (design_deferred/pending_archive/coordination_fetch/handoff_worktrees) 全 `.get()` 访问 (abi_compat #2)。
  单测: 损坏 JSON / 缺 issue_status / 缺 additive 字段。
  - deps: TA-read-1

- [ ] **TA-refresh-1** `acquire.refresh_snapshot(project, reason)` ②刷新: age>threshold 或显式请求 →
  在项目 checkout 跑 `python3 <scan_script_path> ` (路径来自 L2 config, 非 hardcode)。
  **退出码契约** (recon 确认): `EXIT_OK=0`/`EXIT_SCAN_PARTIAL=10` → 重读快照 (10 记 warning);
  `EXIT_HARD_PRECONDITION=20` → `available:false`; `EXIT_INTERNAL_BUG=30` → `refresh_failed`。
  单测 (mock subprocess rc): rc=0/10/20/30 各路径。 [AC-3]
  - deps: TA-read-1

- [ ] **TA-refresh-2** 幂等安全回归 (abi_compat #1): 真 git fixture (隔离 tempdir worktree,
  memory `feedback_test_worktree_fixture_isolated_tmpdir`) 跑 scan.py 刷新 → 断言项目
  `git status` 刷新前后**零变化** (不碰代码/git)。CAVEAT-host: 无 checkout 项目 →
  `available:false, reason:"no-checkout"`。
  单测: 幂等 git-status 不变 / no-checkout 路径。 [AC-3, AC-6]
  - deps: TA-refresh-1

- [ ] **TA-refresh-3** refresh_threshold 默认值 (Q-1, L2 可配, 默认 24h 占位): 阈值语义不写死,
  从 config 读; age 比较逻辑 (age>threshold 触发)。"自动刷 vs 仅提示" 留 Q-1 标定 (Phase A.2),
  代码做成可配 flag。
  - deps: TA-refresh-1, TA-scaffold-2

- [ ] **TA-aggregate-1** `aggregate.collect_fleet(projects)` 跨项目汇总: 遍历 projects → ①读
  (必要时 ②刷新) → 调 `health.derive` 降维 → 汇总 `{generated_at, project_count, projects[],
  summary{ok,warn,blocked,unavailable}}`。**fail-soft** (复用 dashboard 多源装配): 单项目失败 =
  标 available:false 不传播 (memory 镜像 "missing source = empty section")。
  单测: 混合输入 (有快照/待刷新/无 checkout/scan 失败) → 完整 projects[] + 正确 summary。 [AC-4]
  - deps: TA-read-1, TA-refresh-1, TB-health-1

---

## TG-B — 健康降维与 tool pack 接口 (L1 契约, ~9h)

- [ ] **TB-health-1** `health.derive(snapshot)` 7 信号降维 (memo §3, 精确路径 recon 实测确认):
  | 信号 | 路径 |
  | custom_checks 失败 | `custom_checks.failed>0` / `results[].status=="fail"` (severity `.get("severity","warning")`) |
  | 在飞中断 | `interrupt.status != "none"` |
  | 设计未实施 | `openspec.design_deferred` 非空 (`.get([])`) |
  | sync 不齐 | `sync_status.multi_remote.overall_parity == false` |
  | handoff 陈旧 | `handoff.age_hours` + `openspec.carry_forward_inventory.total>0` |
  | 待归档 | `openspec.pending_archive` 非空 (`.get([])`) |
  | 审计 FAIL | `audit.last_audit.verdict == "FAIL"` (`.get` 防 null) |
  phase ← `upm.current_phase`+`current_cycle` (**值可 null**: upm.configured=false 时走 fallback 链 openspec-active→git-branch→"n/a", 见 proposal §B.1)。降维: blocked>warn>ok; blockers[] 中文叙述。
  **全防御式访问** (abi_compat #2)。
  - deps: TA-read-1

- [ ] **TB-health-2** 7 信号各单测 + null/缺字段防御: 每信号触发/不触发 case; `handoff.age_hours`
  null case (caveat-6); 缺 additive 字段旧 snapshot 不抛 (caveat-7 severity `.get`); 对本 Aria
  **live snapshot** (interrupt:none, audit:PASS) 产确定判定 (dogfood, deterministic Rule #6 substitute); **必测 upm.configured=false case** (Aria 自身 fixture → phase fallback 链不撞未定义)。 [AC-5]
  - deps: TB-health-1

- [ ] **TB-health-3** parity 多 remote 仲裁注解 (caveat-5): `overall_parity==false` 含
  behind/diverged/unknown 多义; B.1 降维只读 bool 不展开仲裁 (Q-2 阈值标定时细化); 注释指向
  state-snapshot-schema.md §overall_parity worked examples。
  - deps: TB-health-1

- [ ] **TB-readonly-1** 只读契约守卫 (abi_compat #1+#3): 静态审查 tool pack 无 git mutate /
  无项目源码写 / 无 ship-审批接口; 唯一 FS 写 = ②刷新 scan.py 派生快照。测试断言:
  除 scan.py 调用外无 subprocess 写; no_cross_project_action。 [AC-6]
  - deps: TA-refresh-2

- [ ] **TB-toolpack-1** `fleet_status()`: 全项目一行健康 (`{name,phase,health,snapshot_age}` +
  summary)。返回 `{data, text}` (text=中文默认渲染, 复用 channels-as-render-outputs)。
  单测: 多项目 status + summary 计数。
  - deps: TA-aggregate-1, TB-health-1

- [ ] **TB-toolpack-2** `fleet_project(name)`: 单项目钻取 (完整 derive + blockers[] + age +
  available)。不存在名 → 明确 not-found 不抛。返回 `{data, text}`。
  单测: 存在/不存在/unavailable 项目。 [AC-7]
  - deps: TA-aggregate-1, TB-health-1

- [ ] **TB-toolpack-3** `fleet_blocked()`: filter `health in {warn,blocked}`。返回 `{data, text}`。
  Hermes 接入边界 (Q-4): 接口做纯函数 (输入 yaml 路径 → 输出 data+text), 接入层留 thin adapter
  (AD3 entry-point POC 复用待 Phase A.2 协调)。
  单测: 全 ok→空 / 含 warn+blocked→正确过滤。 [AC-7]
  - deps: TA-aggregate-1, TB-health-1

---

## TG-C — workspace 切片与三层文档 (L2 + 三层落地, ~6h)

- [ ] **TC-yaml-1** `projects.yaml` schema (memo §3, 5-20 行): `{name, path, branch}` 最小集 +
  `refresh_threshold_hours` + `scan_script_path`。含 ≥1 真实样例 (Aria 自身 path=/home/dev/Aria
  branch=master)。所有 host 路径/Forgejo 配置进 yaml (L2), 非 L1 代码。Q-3 来源=手维护 (MVP;
  auto-discover DEFERRED)。
  - deps: TA-scaffold-2

- [ ] **TC-yaml-2** config 校验: config.py 解析 projects.yaml → projects[]+threshold+scan_path;
  缺字段/类型错给明确校验错误。单测: 合法/缺 name/缺 path/threshold 非数。 [AC-8]
  - deps: TC-yaml-1

- [ ] **TC-schemaver-1** 跨 plugin schema 版本容忍 (Q-5): 读 `snapshot_schema_version`; major
  不匹配 "1.0" → 标 `schema_drift` warning 但尽力 derive (additive 漂移降级)。精确策略
  (拒绝/降级/告警) Q-5 待标定; MVP = 记录+additive 降级+标 drift。
  单测: 同版本/additive 漂移/major 漂移混合聚合不崩。 [AC-9]
  - deps: TB-health-1

- [ ] **TC-docs-1** `extensions/aria-fleet/README.md` 三层映射 (memo §5): L1 通用 (tool pack
  框架, 零 10CG hardcode) / L2 workspace (projects.yaml + 阈值 + Forgejo/host 配置) / L3 instance
  (各项目 state-snapshot.json + checkout)。
  - deps: TC-yaml-1

- [ ] **TC-docs-2** README 补 D1-D6 引用 + 复用清单 (state-scanner scan.py / snapshot schema /
  aria-dashboard 渲染思路 / channels-as-render-outputs) + 新建清单 (projects.yaml / 聚合引擎 /
  健康降维 / 接口 / 刷新-on-stale) + Q-1..Q-5 指向 Phase A 标定。**不改 standards submodule**
  (本 Spec 纯 orchestrator extension + 项目 OpenSpec)。 [AC-10]
  - deps: TC-docs-1

---

## Precision Items (Open Questions → Phase A.2 标定)

| Q | 主题 | 来源 memo §8 | 影响 Task |
|---|------|------|------|
| Q-1 | 刷新触发策略 (自动 vs 提示, 24h 阈值, N×scan 延迟) | §8.2 | TA-refresh-3 |
| Q-2 | 健康/卡点阈值标定 (blocked vs warn, handoff/snapshot age, behind count) | §8.1 | TB-health-1, TB-health-3 |
| Q-3 | projects.yaml 来源 (手维护 MVP vs auto-discover) | §8.3 | TC-yaml-1 |
| Q-4 | Hermes tool pack 接入 (AD3 POC, AD7 元知识边界) | §8.4 | TB-toolpack-3 |
| Q-5 | 跨 plugin schema 版本容忍 | §8.5 | TC-schemaver-1 |

---

## Ordering Dependencies

```
[Phase B precondition: M6 release-closeout shipped (D3)]
        │
        ▼
   TA-scaffold-1 ──► TA-scaffold-2 ──┬──► TA-read-1 ──► TA-read-2
                                     │         │
                                     │         ├──► TA-refresh-1 ──► TA-refresh-2
                                     │         │                 └──► TA-refresh-3
                                     │         │
                          TB-health-1 ◄────────┘ (derive 依赖 read 产出的 snapshot dict)
                                     │
        ┌────────────────────────────┼──────────────────────────┐
        ▼                            ▼                           ▼
   TA-aggregate-1            TB-health-2/3              TB-readonly-1
   (依赖 read+refresh             (单测+注解)            (依赖 refresh-2)
    +health-1)
        │
        ▼
   TB-toolpack-1/2/3 (依赖 aggregate + health-1)
        │
        ▼
   TG-C (yaml + schemaver + docs; yaml 依赖 scaffold-2, schemaver 依赖 health-1)
```

**并行边界**: TG-A-read 与 TG-A-refresh 在 read-1 后可并行; TB-health-2/3 (测试/注解) 与 TB-readonly-1
独立; TG-C 三 task 在 scaffold-2 + health-1 就绪后大体可并行 (docs-2 依赖 docs-1)。
强依赖核心代码 (acquire/health/aggregate) 主 loop 亲自边验零回归; 文档 + 单测落点交 workflow agent
并行 (memory `feedback_agent_team_dynamic_workflow_division`)。

---

## Status

- **Phase A.1** (spec-drafter): Draft 产出 2026-06-18 (本 tasks.md + proposal.md)。
- **Phase A.2** (待): post_spec audit → R1.. 收敛 → Approved 后填 Q-1..Q-5 标定决议 + AD-M7-* slot 确认。
- **Phase A.3** (待): agent 分配 (上表 Agents 列为候选)。
- **Phase B** (待): D3 时机门 (M6 release-closeout shipped) 后开。
