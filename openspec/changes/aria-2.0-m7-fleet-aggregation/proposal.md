# Aria 2.0 M7 Spec — Fleet Cross-Project Read-Only Aggregation (MVP 第一刀)

> **Level**: 3 (Full — 新建 tool pack 框架 + 取数模型 + 健康降维 + 接口 schema; 三个内部 task group)
> **Status**: **Draft** (pending Phase A.2 audit → approval; 当前为 A.1 spec-drafter 产出, 未经 post_spec 审计收敛)
> **Change ID**: `aria-2.0-m7-fleet-aggregation`
> **Parent US**: ⚠️ 待立项 — PRD §US 中 US-027 = "Cost routing" (语义已占用), aria-fleet **无独立 US**; 须新建 US-028+ 作 aria-fleet tracker (规范先行, Phase A.2 approval 前补)。当前上游 = #128 + 下列 memos
> **Parent PRD**: ⚠️ prd-aria-v2.md 里程碑止于 M6, **无 §M7** (实测 grep 零命中); M7 aria-fleet 尚未写入 PRD。规范先行: Phase A.2 approval 前须补 PRD M7 milestone stub 再正式立项。本 Spec 上游 = 下列 brainstorm memos + #128
> **Predecessor Spec**: aria-2.0-m6-release-closeout (M6 sequential, 消费 #2 e2e-resilience 证据; M6 ship 是 D3 时机门)
> **Sibling Spec (M7 子能力 #1)**: aria-2.0-m7-agent-lifecycle (agent 生命周期管理 download-half-loop; 同属 M7, 两 sub-Spec 各自独立 MVP 边界, 无 ship 顺序硬依赖)
> **Brainstorm Source**:
>   - `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md` (本 Spec 直接来源; §2 第一刀=聚合 tool pack / §3 MVP 构成 / §4 取数模型 ①读②刷新③推迟 / §5 三层映射 / §7 推迟项 / §8 开放问题; owner ✅ 逐项确认 2026-06-18)
>   - `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (D1-D6 Approved — 命名 / 三层 / M7 时机 / D5 tool pack 形态; M7 brainstorm 起点, 不重议 D1-D6)
>   - Forgejo Aria #128 (M7 aria-fleet tracker; **注: #128 ≠ US-027** — memo 曾误并, US-027 实为 Cost-routing per PRD)
> **D1-D6 binding** (2026-05-27 owner approved, 本 Spec 不重议):
>   - D1: 命名 `aria-fleet` (kebab-case repo/module; `aria_fleet` snake_case tool pack 模块名 per PEP 8; `/aria:fleet-*` Skills)
>   - D2: 三层 (L1 universal framework / L2 workspace config private / L3 instance runtime)
>   - D3: 时机 = M7+ (M6 ship 之后; 本 Spec Phase B 不得早于 M6 release-closeout ship)
>   - D4: workspace = `10CG/aria-workspace` private repo (本 MVP 只用 `projects.yaml` 一小片, 不整建 repo)
>   - D5: 形态 = `aria-orchestrator/extensions/aria-fleet/` Python tool pack (非独立 repo, 非 marketplace 优先)
> **L1 hard constraints** (D1-D6 post-§8 sign-off, 本 Spec 强制遵守):
>   1. L1 (`aria_fleet/` tool pack 框架) **禁止 hardcode**: forgejo.10cg.pub / Aether / 10CG secrets / Feishu webhook / simonfishgit / host 绝对路径
>   2. 所有 team-specific 值经 L2 `projects.yaml` + 集成配置注入, 不进 L1 代码
>   3. L1 不实现 Rule #5-#9 的 10CG-specific 变体 (仅框架)
> **AD allocation reservation**: AD-M7-1 / AD-M7-2 / AD-M7-3 (本 Spec; AD-M7-* 编号方案待 Phase A 确认, sibling agent-lifecycle Spec 从 AD-M7-4+ 起)
> **abi_compat hard constraints**:
>   1. `snapshot_read_only` — fleet 聚合器**绝不**改项目代码 / git / 任何非 `.aria/state-snapshot.json` 派生文件; ②刷新经 `scan.py` 幂等重生成派生快照不破此约 (caveat 见 §What B.2)
>   2. `additive_schema_defensive_access` — 消费 snapshot post-v1.0 additive 字段 (design_deferred / pending_archive / issue_status / coordination_fetch / handoff_worktrees) **必须** 防御式访问 (`.get()` / `in` 检测), 不假设存在 (注: `issue_status` 顶层键在未配置 issue 扫描的项目可能缺失 → 用 `in` 检测顶层键存在; **无 `enabled` 子字段**, gating 由 config 决定)
>   3. `no_cross_project_action` — MVP 只读; 不触发任何项目的 scan-as-action / ship / approval (区别于 ②刷新: 后者是聚合自身的取数动作, 不是对项目下指令)
> **Audit trajectory**: post_spec R1 (2026-06-18, agent-team 对抗 panel 3 lens) = PASS_WITH_WARNINGS (0 Critical / 3 Important / 多 Minor); Important 全部主 loop 落地 (upm.configured=false phase fallback + AC-5 必测 case / issue_status `in`-检测无 enabled 子字段 / US-027·§M7 悬空引用更正)。**待**: owner approval + 规范先行前置 (PRD M7 milestone stub + aria-fleet 独立 US 立项) → 之后可开 Phase A.3/B。

---

## Why

aria-fleet 的核心 essence 是把分散在多个 10CG 项目里的状态聚合成一个只读"指挥塔", 让 Layer 1 主管 (Hermes) 能一眼回答"哪个项目卡了"。在 M6 ship 之前 (D3 时机门), fleet 不应动工; M6 收口后, M7 进入 fleet 多子能力分阶段实施, 本 Spec 是 **fleet 整体 MVP 的第一刀** (owner 2026-06-18 在三候选中选定 §2)。

**为什么是聚合 tool pack 而非别的第一刀** (memo §2): 三候选中 (a) workspace repo 地基先行 = 给尚未设计的 fleet 功能预搭结构, 偏早; (b) 多 channel 富渲染先行 = 没有聚合层就没有内容可渲染, 偏早; (c) **聚合 tool pack** = 上来就有用, 复用现成 `state-snapshot.json` 快照 (零新采集基建), 依赖最小。owner 选 (c)。

**为什么现在可行** (memo §1 recon): 每个 10CG 项目经 state-scanner `scan.py` 机械产出 `.aria/state-snapshot.json` (本 Aria 实例实测: 22 个 top-level 字段, schema v1.0)。这是聚合的天然原料, 缺的只是 (1) 跨项目把这些快照读进来并降维, (2) 一份"看哪些项目"的清单 (`projects.yaml`)。aria-dashboard skill 已 dogfood 单项目渲染 (v1.1.0), 其"结构化数据 → 可插拔渲染"模式可借鉴到多项目。

**Gate role / 边界定位**: 本 Spec 是 fleet 后续所有子能力 (跨项目动作 / workspace repo 整建 / 多 channel 富渲染 / 历史趋势) 的**地基切片** — 它确立 fleet tool pack 的 L1/L2/L3 落点、取数模型、健康降维契约。后续 sub-Spec 在此之上扩展。本 Spec 与 sibling `aria-2.0-m7-agent-lifecycle` 同属 M7, 但两者作用域 disjoint (聚合 vs agent 生命周期), 无 ship 顺序硬依赖。

**前置条件**: (1) M6 release-closeout 已 ship (D3 时机门); (2) `aria-orchestrator/extensions/` 目录尚未创建 (D5 规划位置, 本 Spec Phase B 首个动作即创建之; `hermes-extensions/aria-layer1/` 既有 pattern 证明 aria-orchestrator 承载 extension 插件)。

---

## What Changes

### In scope (~26h impl 估算, 待 Phase A.2 audit 校准)

本 Spec 三个 task group: **TG-A 取数与聚合引擎** (L1 核心) / **TG-B 健康降维与 tool pack 接口** (L1 契约) / **TG-C workspace 切片与文档** (L2 + 三层落地)。所有 task group 遵守 D1-D6 + L1 hard constraints。

---

#### A. TG-A: 取数与聚合引擎 (Data Acquisition + Aggregation Engine, ~11h)

L1 通用层核心。负责按 `projects.yaml` 枚举项目、读取/刷新每项目 `.aria/state-snapshot.json`、汇总成跨项目结构。零 10CG hardcode。

##### A.1 Tool pack scaffold (D5 落点)

在 `aria-orchestrator/extensions/aria-fleet/` 新建 Python tool pack 骨架 (D1: 模块名 `aria_fleet` snake_case):

```
aria-orchestrator/extensions/aria-fleet/
├── aria_fleet/
│   ├── __init__.py
│   ├── config.py          # projects.yaml loader (L2 注入边界)
│   ├── acquire.py         # ①读 + ②刷新 取数模型 (A.2/A.3)
│   ├── health.py          # 健康/卡点降维 (TG-B)
│   ├── aggregate.py       # 跨项目汇总引擎 (A.4)
│   └── toolpack.py        # fleet_status/fleet_project/fleet_blocked 接口 (TG-B)
├── tests/
└── README.md
```

**约束**: `extensions/` 目录当前不存在 (D5 规划位置, recon 确认), 本 task 首次创建。复用 `hermes-extensions/aria-layer1/` 既有 extension pattern。`aria_fleet` 仅依赖 stdlib + PyYAML (与 scan.py stdlib-only 精神对齐, projects.yaml 解析需 yaml)。

**[AC-1]** tool pack 可被 import (`from aria_fleet import toolpack`); 目录结构落地; README 声明 L1/L2/L3 边界。

##### A.2 ①读 — 读现有快照 + 显示陈旧度 (默认快路径)

`acquire.read_snapshot(project)`: 读取项目 `<path>/.aria/state-snapshot.json`, 解析 JSON, 计算 `snapshot_age` (now − 文件 mtime, 或 snapshot 内 `generated_by` 旁的时间锚 — 注: snapshot 顶层无 `generated_at` 字段, 实测仅 `generated_by`/`project_root`/`snapshot_schema_version`, 故 age 以**文件 mtime** 为权威, fallback 见约束)。

**取数契约** (memo §4 ①):
- 默认快路径: 直接返回 cached snapshot dict + `snapshot_age` (秒/小时)。
- 不触网、不跑 scan.py。
- 项目无 `.aria/state-snapshot.json` (从未 scan 过) → 返回 `{available: false, reason: "no-snapshot"}`, 不报错 (fail-soft)。

**约束 (CAVEAT-age)**: snapshot 顶层**无** `generated_at` 字段 (recon 实测仅 `snapshot_schema_version`/`generated_by`/`project_root`)。`snapshot_age` **必须**以文件系统 mtime 为权威源; 若 mtime stat 失败 → age=null (与 handoff.age_hours 的 `float|null` 语义一致, 见 caveat-7)。

**[AC-2]** ①读 对有快照项目返回 dict + 非 null age; 对无快照项目返回 `available:false` 不抛异常。

##### A.3 ②刷新 — 陈旧超阈或按请求跑 scan.py (幂等安全)

`acquire.refresh_snapshot(project, reason)`: 当 `snapshot_age > refresh_threshold` (L2 可配, 默认见约束) **或** owner 显式请求时, 对该项目 checkout 跑 `scan.py` 重生成快照, 再 ①读。

**调用契约** (复用 state-scanner 产物, memo §4 ②):
- 在项目 checkout 根目录调用 `python3 <state-scanner>/scripts/scan.py` (路径经 L2 配置注入, 不 hardcode)。
- **退出码处理** (scan.py 契约, recon 确认): `EXIT_OK=0` (快照可用) / `EXIT_SCAN_PARTIAL=10` (软错误但快照仍可用, 记 warning 不视为失败) / `EXIT_HARD_PRECONDITION=20` (cwd 非 git repo, 快照不可用, 该项目标 `available:false`) / `EXIT_INTERNAL_BUG=30` (未捕获异常, 标 `refresh_failed`)。**rc=0 与 rc=10 都重读快照** (10 仍产出可用快照); rc=20/30 不重读。
- **幂等安全保证** (memo §4 caveat, abi_compat #1): scan.py 只从当前项目状态重生成**派生**快照, **不碰项目代码、不动 git**。②刷新技术上重写 `state-snapshot.json` 文件, 但这是聚合自身的取数动作, 不破坏"fleet 从不改项目本体"的只读聚合本质。

**约束 (CAVEAT-host)**: ①②都要求项目 checkout 在 Hermes host 上。无 checkout 的项目两者都拿不到 → 标 `available:false, reason:"no-checkout"`。这正是未来 ③推送 (DEFERRED, §Out of scope) 要解决的; MVP 假设项目都在 host 上有 checkout。

**约束 (refresh_threshold 默认)**: 默认阈值候选 24h (memo §4 ②举例), 但具体值 + "自动刷 vs 仅提示"策略是 **Q-1 开放问题** (§Out of scope / Open Questions), Phase A.2 标定; 默认值落地为 L2 可配, 代码不写死语义。

**[AC-3]** ②刷新 在 age>阈值时调用 scan.py 并按退出码契约处理 (0/10 重读, 20/30 不重读); 刷新前后项目 git working tree 无变化 (幂等性回归测试)。

##### A.4 跨项目汇总引擎

`aggregate.collect_fleet(projects)`: 遍历 `projects.yaml` 每项, 经 ①读 (必要时 ②刷新) 取每项目 snapshot, 调 TG-B `health.derive()` 降维, 汇总成 fleet-level 结构:

```python
{
  "generated_at": "<ISO-8601>",
  "project_count": N,
  "projects": [
    {"name": "...", "phase": "...", "health": "ok|warn|blocked",
     "blockers": [...], "snapshot_age": <float|null>, "available": true},
    {"name": "...", "available": false, "reason": "no-checkout"},
    ...
  ],
  "summary": {"ok": N1, "warn": N2, "blocked": N3, "unavailable": N4}
}
```

**fail-soft 原则** (复用 aria-dashboard 多源装配哲学, recon §3): 单项目取数失败 = 该项目标 `available:false` + reason, **不**让整个 fleet 聚合失败 (镜像 dashboard "missing source = empty section, not error")。

**[AC-4]** 混合输入 (有快照 / 待刷新 / 无 checkout / scan 失败) 下聚合返回完整 projects[] 含正确 available/health/summary, 无单点失败传播。

---

#### B. TG-B: 健康降维与 tool pack 接口 (Health Reduction + Tool Pack Interface, ~9h)

L1 契约层。把单项目丰富 snapshot 降维成 `{phase, health, blockers[], snapshot_age}`, 并暴露三个 Hermes 可调接口。

##### B.1 健康/卡点降维 (health.derive)

`health.derive(snapshot) -> {phase, health, blockers[]}`: 从 snapshot **现成字段** (recon 全部确认存在于 live snapshot) 推导。**所有访问防御式** (abi_compat #2)。

**信号集** (memo §3, 精确 nested path 实测确认):

| 信号 | 精确路径 | 类型 | 触发语义 |
|------|---------|------|---------|
| custom_checks 失败 | `custom_checks.failed > 0` 或 `custom_checks.results[i].status == "fail"` | int / list | blocked 候选; `results[].severity` (error/warning/info) 区分严重度, 防御 `.get("severity","warning")` (caveat-7 additive) |
| 在飞中断 | `interrupt.status != "none"` | str (none/in_progress/suspended/failed/corrupted) | 非 none = blocked |
| 设计未实施 | `openspec.design_deferred` 非空 | list[{id,status,staleness_days,reason}] | warn 候选 (additive v1.42.0+, `.get("design_deferred",[])`) |
| sync 不齐 | `sync_status.multi_remote.overall_parity == false` | bool | warn (parity 多 remote 仲裁微妙, 见 caveat-5) |
| handoff 陈旧 | `handoff.age_hours` (高) + `openspec.carry_forward_inventory.total > 0` | float\|null / int | warn (age_hours 可能 null, caveat-6) |
| 待归档堆积 | `openspec.pending_archive` 非空 | list[{id,reason}] | warn (additive v1.42.0+, bonus signal) |
| 审计 FAIL | `audit.last_audit.verdict == "FAIL"` | str\|null (PASS/PASS_WITH_WARNINGS/FAIL) | blocked verdict (`.get` 防 null) |

**phase 来源**: `upm.current_phase` + `upm.current_cycle` (keys 存在但**值可为 null**)。⚠️ **upm.configured 三态**: 当 `upm.configured == false` (方法论容器如 Aria 自身, memory `project_aria_no_runtime_upm`) → 三 upm 字段全 null。**phase fallback 链**: `upm.current_phase` → (null) openspec active change 名 → (无) git 当前分支 → (兜底) `phase="n/a"`。derive 绝不假设 upm 非 null。

**降维约定**:
- `health = "blocked"` 若任一 blocked 候选触发; `"warn"` 若任一 warn 候选触发且无 blocked; 否则 `"ok"`。
- `blockers[]` = 触发信号的人类可读列表 (中文叙述, 如 "审计 FAIL: post_spec R2"; "在飞中断: suspended")。
- **具体阈值标定** (handoff age 多少算陈旧 / behind count / snapshot age 上限) 是 **Q-2 开放问题** (§Out of scope), Phase A.2 标定; B.1 先实现信号检测 + 占位阈值 (L2 可配)。

**[AC-5]** derive 对 7 类信号各有单测 (含 null/缺字段防御); 对本 Aria live snapshot (interrupt:none, audit:PASS, design_deferred 实测内容) 产出确定 health 判定; 缺 additive 字段的旧 snapshot 不抛异常; **显式必测 case**: `upm.configured=false` 项目 (Aria 自身正是该 fixture) → phase 走 fallback 链, 不撞未定义行为。

##### B.2 只读契约守卫 (read-only invariant)

显式断言 abi_compat #1 + #3 (no_cross_project_action): tool pack 代码路径中**唯一**写文件系统的操作是 ②刷新 经 scan.py 重生成派生快照; 无任何对项目 git / 源码 / 配置的写入; 无任何"对项目下指令"(触发 ship/审批) 的接口。

**[AC-6]** 静态审查 + 测试: tool pack 除 scan.py 调用外无 subprocess 写操作; 无 git mutate; ②刷新 前后项目 `git status` 不变 (复用 A.3 幂等回归)。

##### B.3 Tool pack 接口 (Hermes 可调, memo §3)

`toolpack.py` 暴露三接口, 每个返回**结构化数据 + 默认文本渲染** (channel 由 Hermes 决定, 复用 `feedback_channels_as_agent_render_outputs`):

- `fleet_status()` — 全项目一行健康概览 (每项目 `{name, phase, health, snapshot_age}` + summary 计数)。
- `fleet_project(name)` — 单项目钻取 (完整 derive 结果 + blockers[] 详情 + snapshot_age + available)。
- `fleet_blocked()` — 只看 `health in {warn, blocked}` 的子集 (聚合 collect_fleet 后 filter)。

**输出契约**: 每接口返回 `{data: <structured>, text: <default-render>}`。`text` 是默认文本渲染 (中文叙述 + 英文 token); `data` 供 Hermes 选 channel (飞书卡片/CLI/dashboard) 重渲染。**不**做富渲染 (DEFERRED §Out of scope)。

**Hermes 接入边界 (Q-4)**: 接口如何挂进 Hermes (复用 AD3 entry-point plugin POC) + 与 Layer 1 元知识 (AD7 ~1K token 边界) 的契约是 **Q-4 开放问题**, Phase A.2 与 orchestrator 侧协调; B.3 先把接口做成纯函数 (输入 projects.yaml 路径, 输出 data+text), 接入层留 thin adapter。

**[AC-7]** 三接口各返回 `{data, text}`; `fleet_blocked()` 正确过滤 warn+blocked; `fleet_project(不存在名)` 返回明确 not-found 不抛异常。

---

#### C. TG-C: workspace 切片与三层文档 (L2 Slice + Three-Layer Docs, ~6h)

L2 workspace 配置切片 + 三层落地文档。

##### C.1 projects.yaml schema (L2 切片)

定义 `projects.yaml` 极简清单 schema (memo §3, 5-20 行):

```yaml
# L2 workspace config slice (10CG/aria-workspace 那一小片; MVP 不整建 repo)
refresh_threshold_hours: 24    # ②刷新阈值 (Q-1 待标定; L2 可配)
scan_script_path: "<state-scanner scan.py 路径>"  # L1 不 hardcode, L2 注入
projects:
  - name: "Aria"
    path: "/home/dev/Aria"      # host checkout 绝对路径 (L2, 非 L1)
    branch: "master"
  - name: "<other>"
    path: "..."
    branch: "..."
```

**约束 (Q-3)**: `projects.yaml` 来源 (手维护 vs host checkout 自动发现 vs Forgejo org 拉取) 是 **Q-3 开放问题**; MVP **手维护** (auto-discover DEFERRED §Out of scope)。schema 字段 (name/path/branch) 是 MVP 最小集; 扩展字段留 additive。

**约束 (L1/L2 边界)**: 所有 host 路径 / Forgejo 配置 / 项目清单进 `projects.yaml` (L2), 不进 `aria_fleet/` 代码 (L1, D1-D6 hard constraint #1/#2)。L1 经 `config.py` loader 读取注入。

**[AC-8]** projects.yaml 含 ≥1 真实样例 (Aria 自身); config.py 解析返回 projects[] + threshold + scan_path; 缺字段给明确校验错误。

##### C.2 跨 plugin schema 版本容忍 (Q-5)

聚合多项目时各项目 `snapshot_schema_version` 可能漂移 (additive schema 已部分缓解, 因 additive 字段不 bump 版本)。`health.derive` 防御式访问 (abi_compat #2) 已覆盖大多数情形。本 task 记录版本容忍策略: 读 `snapshot_schema_version`, 若 major 不匹配预期 (当前 "1.0") → 该项目标 `schema_drift` warning 但仍尽力 derive (additive-only 漂移可降级处理)。

**约束**: 精确容忍策略 (拒绝 / 降级 / 告警) 是 **Q-5 开放问题**; MVP 实现 "记录版本 + additive 漂移降级 derive + 标 schema_drift"。

**[AC-9]** 不同 snapshot_schema_version 的混合项目聚合不崩溃; major 漂移项目标 schema_drift 仍产出尽力 derive。

##### C.3 三层映射文档 + Spec 归档准备

`aria-orchestrator/extensions/aria-fleet/README.md` 落地三层映射 (memo §5):
- **L1 通用**: `aria_fleet/` tool pack 框架 (聚合引擎 + 健康推导 + 接口 schema + 取数模型); 复用 state-scanner; 零 10CG hardcode。
- **L2 workspace**: `projects.yaml` + refresh 阈值 + 集成配置 (Forgejo/host 路径)。
- **L3 instance**: 各项目 `.aria/state-snapshot.json` (已有) + checkout。

记录 D1-D6 引用 + 复用清单 (state-scanner scan.py / snapshot schema / aria-dashboard 渲染思路 / channels-as-render-outputs 哲学) + 新建清单 (projects.yaml schema / 聚合引擎 / 健康降维 / tool pack 接口 / 刷新-on-stale)。

**[AC-10]** README 含完整 L1/L2/L3 表 + D1-D6 + 复用/新建清单 + Q-1..Q-5 开放问题指向 Phase A 标定; 不引入 standards submodule 变更 (本 Spec 纯 orchestrator extension + 项目 OpenSpec, 无 standards 改动)。

---

### Out of scope (DEFERRED to M7+ / 明确推迟)

本 Spec 严格遵守 memo §7 推迟项 + faithfulness anchor:

1. **③推送到中央库** (memo §4 ③ / §7): 项目 scan 时推送快照到 durable volume / workspace repo 供跨主机解耦。MVP **单 Hermes host**, 假设所有项目本地 checkout; 跨主机 DEFERRED。(memory `feedback_periodic_job_acceptance_data_on_durable_volume` 为未来 ③ 落点参考)
2. **跨项目动作** (memo §7): 触发某项目 scan-as-command / ship / 审批。MVP **只读** (abi_compat #3); ②刷新 是聚合取数动作非对项目下指令。
3. **完整 workspace repo** (memo §7 / D4): integrations / playbooks / branding / artifacts 整建。MVP 只用 `projects.yaml` 一小片。
4. **多 channel 富渲染** (memo §7): 飞书富卡片 / 实时 dashboard。MVP 结构化数据 + 默认文本; channel 由 Hermes 决定。
5. **历史趋势 / risk register** (memo §7): 跨时间聚合。后话。
6. **projects.yaml auto-discovery** (Q-3): host checkout 自动发现 / Forgejo org 拉取。MVP 手维护。
7. **AB / benchmark**: 本 Spec 是 deterministic tool pack (聚合/降维/取数), Rule #6 substitute = structural fixture + unit tests + dogfood (memory `feedback_deterministic_structural_skill_rule6_substitute`), 不走 /skill-creator capability AB。
8. **sibling agent-lifecycle 的 AB/judge/telemetry/⑤吸收⑥汇总**: 不属本 Spec (那是 M7 子能力 #1 的 deferred 部分)。

### Open Questions (Phase A.2 标定; memo §8)

- **Q-1 刷新触发策略**: 自动刷 vs 仅提示; 24h 阈值是否合适; 是否默认不自动重跑 (避免 N×scan 延迟)。
- **Q-2 健康/卡点阈值标定**: 哪些信号算 blocked vs warn; handoff age / snapshot age / behind count 各阈值。
- **Q-3 projects.yaml 来源**: 手维护 (MVP) vs auto-discover (DEFERRED)。
- **Q-4 Hermes tool pack 接入**: 复用 AD3 entry-point POC; 接口契约与 AD7 元知识边界。
- **Q-5 跨 plugin 版本容忍**: snapshot_schema_version 漂移处理策略 (additive schema 部分缓解)。

### Success Criteria

AC-1..AC-10 全部 PASS (见各 §What Changes 子节)。核心: (a) tool pack 在 `aria-orchestrator/extensions/aria-fleet/` 落地且 import 可用; (b) ①读+②刷新 取数模型按 scan.py 退出码契约工作且幂等安全; (c) 7 类健康信号从 live snapshot 现成字段降维, 防御式访问无崩溃; (d) 三接口 `fleet_status/fleet_project/fleet_blocked` 返回 `{data, text}`; (e) L1 零 10CG hardcode, L2 切片注入; (f) 三层文档 + Q-1..Q-5 明确指向 Phase A 标定。

---

## Impact

**纯 additive** (Aria 原则 #4; 复用 state-scanner 产物, 不改既有 Skill / schema)。受影响清单:

| 类别 | Affected | 性质 |
|------|----------|------|
| 新 tool pack | `aria-orchestrator/extensions/aria-fleet/` (`aria_fleet/` Python 模块) | net-new (D5 落点; `extensions/` 目录首次创建) |
| 新 artifact | `projects.yaml` (L2 workspace 清单切片) | net-new (10CG/aria-workspace 那一小片) |
| 新 config | `aria_fleet` config (refresh_threshold / scan_script_path / projects[]) | additive (经 L2 注入, L1 零 hardcode) |
| 复用 (不改) | state-scanner `scan.py` + `.aria/state-snapshot.json` schema (只读消费 + ②刷新调用) | 零改动 (只读 + 幂等调用) |
| 复用 (思路) | aria-dashboard 渲染模式 (结构化数据 → 可插拔渲染) | 借鉴, 不改 |
| **不涉及** | standards submodule / 既有 Skill / 既有 schema / 项目代码·git (只读聚合 abi_compat #1/#3) | 无改动 |

**迁移路径**: 无 (net-new 聚合层, 各项目 snapshot 已存在)。**回滚**: 删 `extensions/aria-fleet/` + `projects.yaml` 即完全回退; 各项目本体零触碰。
