# state-scanner-submodule-issue-scan — Phase 1.13 Submodule Issue 扫描

> **Level**: Minimal (Level 2)
> **Status**: **Complete** ✅ (归档 2026-04-15, PR #19 已合并, v1.16.0 已发版)
> **Created**: 2026-04-15
> **Archived**: 2026-04-15
> **Delivered Version**: aria-plugin v1.16.0
> **PR**: [aria-plugin#19](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/19) (merged 8ec898a @ 2026-04-15T11:35:04Z)
> **Audit**: 5-round multi-agent pre_merge convergence (R4=R5=empty), 22 findings resolved. 详见 `.aria/audit-reports/pr19-submodule-scan/round-{1..5}/`
> **Benchmark**: `aria-plugin-benchmarks/ab-results/2026-04-15-state-scanner-submodule-issue-scan/` (+50pp pass rate delta)
> **Source**: 2026-04-15 Aria 主项目 session 中用户指出 "aria-plugin 应该也有 issue, 为什么没查看到?", 追查到 Phase 1.13 显式不递归 submodule (D6 决策)
> **Parent Spec (扩展其决策)**: `state-scanner-issue-awareness` (2026-04-09 归档) — 本 Spec 扩展其 D6 "不递归 submodule" 决策为 opt-in, 不否定原决策本体
> **Sister Spec (相关, 不合并)**: `state-scanner-mechanical-enforcement` (Draft) — 姐妹 Spec, 主题不同 (执行纪律 vs 设计假设), 单一焦点分离

---

## Why

### 问题陈述

state-scanner v2.9 的 Phase 1.13 (Issue 感知扫描) **仅扫描当前 repo 的 remote** (`git remote get-url origin`), **不递归 `.gitmodules` 中的 submodule**。这是原始 Spec `state-scanner-issue-awareness` (2026-04-09 归档) 的**显式设计决策** (D6) 与 Out of Scope 条目之一, 而非实现遗漏。

### 2026-04-15 Aria 主项目实测证据

当日 session 中, state-scanner 运行完整 Phase 1.13 后报告 "2 open issues" (均来自 `10CG/Aria` 主 repo)。用户直觉质疑 "aria-plugin 应该也有 issue", 追查结果:

| Repo | 实际 open issues | 被 Phase 1.13 扫描? |
|---|---|---|
| `10CG/Aria` (主 repo) | 2 | ✅ |
| `10CG/aria-plugin` (submodule at `aria/`) | **2** | ❌ |
| `10CG/aria-standards` (submodule at `standards/`) | 0 | ❌ |
| `10CG/aria-orchestrator` (submodule at `aria-orchestrator/`) | 1 | ❌ |

**总体漏报率**: **60%** (3 个 open issue / 5 个实际 total 未被看见)。

更关键的是漏报 issue 的**内容相关性**极高:

- **aria-plugin#18** — `feat(estimator): 引入 Token × Attention 双主轴工作量估算` (创建于今日 06:39 UTC, 直接对应 M0 T4 "原估 52h 实际 4.5h 节省 91.9%" 的估算失效现象)
- **aria-plugin#17** — `feat(audit-engine): Drift Guard 防偏移检查` (创建于今日, 直接对应 2026-04-14 Agent Team 4 轮收敛评审是否漂离 anchor 的验证需求)
- **aria-orchestrator#1** — `[Idea] 轻量化 Hermes — 自研精简版替代完整 Hermes Agent` (T4 Spike Option C 事实上已回答此 Idea, 但 Issue 未关闭, 未与 Spike 结论挂钩)

这三个 issue 与当前 session 的 M0 工作主线**直接相关**, 缺失后果:

1. **推荐决策偏差**: Phase 2 的 `open_blocker_issues` 规则基于 `items[].labels` 判断 blocker。尽管当前漏报的 3 个 issue 无 blocker label, 但未来若 submodule issue 打上 blocker label, 主流程会**完全看不到**, 推荐可能错给 Go 信号。
2. **方法论次生发现遗失**: aria-plugin#17/#18 是 M0 过程暴露的方法论次生问题, 本应在 T6 M0 Report §风险确认 章节被引用, 缺失后 M0 Report 无法完整反映 "M0 过程中的 learnings"。
3. **认知漂移**: 每次 session 的状态快照不完整, 日积月累造成 "我们以为在看的状态" 与 "真实项目状态" 的系统性偏差。

### 原设计决策 D6 的假设错配

原 Spec (`state-scanner-issue-awareness` 2026-04-09 归档) §Decision Records D6:

> **D6** | 不递归子模块 issues | **噪音控制**；独立 config 开关作为扩展点

D6 的"噪音控制"论点**基于一个隐性假设**: submodule = 第三方依赖 (vendored libraries)。在这个假设下, 如把 jQuery 作为 submodule 引入, 你**不想**被 jQuery 的 issue 污染项目状态扫描。

但 Aria 项目 (以及任何 **meta-repo / monorepo-of-submodules** 模式) 的 submodule 使用方式截然不同:

- `aria/` → `10CG/aria-plugin` (同组织, 同 Aria 方法论项目的核心代码)
- `standards/` → `10CG/aria-standards` (同组织, 方法论定义)
- `aria-orchestrator/` → `10CG/aria-orchestrator` (同组织, v2.0 运行时实现)

**全部是同组织 (`10CG/*`) 的一等协同开发 repo**, 不是 vendored 依赖。D6 的默认行为在这个模式下**反向** — 反而制造了本不应存在的信息盲区。

### 为什么不修改 D6 反转默认

虽然 Aria 场景下反转默认更合理, 但:

1. **向后兼容原则** (CLAUDE.md 不可协商规则 #4): 其他已部署 aria-plugin 的项目可能使用传统 vendored submodule 模式, 反转默认会引入无意义噪音
2. **规模不对称**: Aria 的 meta-repo 模式是 10CG Lab 内部 pattern, 不能假设其他用户同样适用
3. **opt-in 成本低**: 项目级 `.aria/config.json` 添加一行 `scan_submodules: true` 零代价, 开关粒度精准

---

## What

### 目标产出

1. **新增配置项** `state_scanner.issue_scan.scan_submodules` (boolean, 默认 `false`)
2. **扩展 Phase 1.13 执行逻辑** — 当 `scan_submodules=true` 时:
   - 读取 `.gitmodules` 枚举所有 submodule
   - 对每个 submodule 独立执行: 读取其 `origin` remote → 平台检测 → CLI 调用 → JSON normalize → 启发式关联
   - 结果合并写入 `issue_status.repos[owner/repo]` (复用现有缓存 schema)
3. **扩展缓存 schema** 到多 repo 结构 (已预留, 仅需文档化)
4. **扩展推荐规则** `open_blocker_issues` — 聚合所有 repo 的 items, 任一 blocker/critical label 触发降级
5. **调整超时预算** — 单次 API 调用超时保持 5s, 但总阶段超时从 12s 调至 20s (见 §Decision Records D3)
6. **更新 references/issue-scanning.md** — 新增 §submodule 扫描流程 章节

### 范围边界

#### In Scope

- `.gitmodules` 解析 (POSIX `git config --file .gitmodules --get-regexp` 或直接 grep)
- 每个 submodule 独立 remote URL 解析 (复用现有 `owner_repo` 提取逻辑)
- 每个 submodule 独立 platform 检测 (复用现有 4 级优先级逻辑)
- 每个 submodule 独立 CLI 调用 (串行, 非并行, 见 §Decision Records D2)
- 缓存命名空间按 `owner/repo` 隔离 (已预留 schema)
- 推荐规则聚合逻辑 (跨 repo 的 label 合并)

#### Out of Scope (本 Spec 明确不做)

- ❌ **自动反转默认** — `scan_submodules` 保持 `false` 默认
- ❌ **并行 API 调用** — 首版串行, 避免 rate limit 复杂化 (见 D2)
- ❌ **submodule 自动发现 "same-org" 启发式** — 用户必须显式设置 `scan_submodules: true`, 不做自动判断
- ❌ **跨 platform submodule 的统一认证** — 每个 submodule 依赖已配置的对应 CLI wrapper (`forgejo` / `gh`)
- ❌ **递归 submodule-of-submodule** — 只扫一层
- ❌ **.gitmodules 中 URL 的 ssh/http 协议自动转换** — 复用现有 remote URL 解析, 不改
- ❌ **per-submodule 的 label_filter 独立配置** — 全局 `label_filter` 应用到所有 repos
- ❌ **修改原 D6 决策本体** — 本 Spec 作为 D6 的**补充扩展点**, 不否定 D6, 只说明 D6 在 vendored 模式下仍然合理
- ❌ **Phase 1.14 Forgejo 配置检测的 submodule 扩展** — 独立 Spec

### 向后兼容保证 (Round 2 强化 — 回应 R1 I3 tech-lead 反馈)

1. **默认行为字节级不变**: `scan_submodules` 缺省或 `false` 时, Phase 1.13 行为与 v2.9.0 **完全一致**:
   - 同一扫描路径 (仅主 repo, 不解析 `.gitmodules`)
   - 同一超时预算 (`stage_timeout_seconds=12`, 不升到 20s — 见 D14)
   - 同一输出 schema (无 `repos` 字段, `schema_version=null` 等价于 v1.0)
   - 同一推荐规则行为 (`open_blocker_issues` 在单 repo items[] 上评估, 与 v2.9.0 一致)
2. **缓存文件向后兼容 (v1.1 schema_version 守卫)**: v2.9.0 缓存文件**没有** `schema_version` 字段; v1.16.0 reader 识别此情况为 pre-v1.1, 视为 cold cache, **一次性** re-fetch 重建缓存。此后写入的缓存含 `schema_version="1.1"`, 此后读取正常命中。详见 references/issue-scanning.md §步骤 4 cache schema 守卫。
3. **配置文件向后兼容**: 不改 `.aria/config.json` 已有字段语义, 仅新增可选字段 `scan_submodules`。`stage_timeout_seconds` 无变化 (自适应默认值, 用户显式设置被尊重)。
4. **输出 schema 向后兼容 (v1.1 双写别名)**: `issue_status.items[]` 与 `issue_status.open_issues[]` 由 writer 同步双写, v1.0 消费者读 `open_issues` 仍可用, v1.1+ 消费者优先 `items`. `open_issues` 别名将在 v2.x (至少跨 2 个 MINOR) 后移除, 正式弃用通告随 v1.16.0 CHANGELOG 发出。
5. **推荐规则向后兼容**: `open_blocker_issues` v2.10.0 语义为跨 repo 聚合, 但当 `scan_submodules=false` 时 `items[]` 只含主 repo items, 聚合逻辑**退化为单 repo 评估**, 行为与 v2.9.0 等价。

### 依赖

- 依赖 `forgejo` 和 `gh` CLI wrapper 对各 submodule repo 的访问权限已配置完毕
- 依赖 `.gitmodules` 文件语法遵循标准 (`[submodule "path"]` + `path = ...` + `url = ...`)
- 依赖每个 submodule 的 `origin` remote 已正确设置 (不依赖 `.gitmodules` 的 url, 因为实际 remote 可能已被项目级覆盖)

---

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| **D1** | `scan_submodules` 默认 `false`, opt-in | 向后兼容 (CLAUDE.md 规则 #4), 不破坏 vendored submodule 场景 |
| **D2** | **串行**扫描 submodule (非并行) | 首版最小化复杂度, 避免 rate limit 复杂化; 实测 Aria 3 submodule × 平均 2s API ≈ 6s, 在总超时预算内 |
| **D3** | ~~总阶段超时从 12s 提升到 20s~~ → **总阶段超时自适应分档** (Round 2 修复 R1 I2 + I3) | `scan_submodules=false` → 12s (不变, 向后兼容); `scan_submodules=true` → `max(20, (N+1)×api_timeout_seconds)` 按 submodule 数自动扩展; 用户显式设置覆盖自适应. 既消除了 tech-lead 指出的"非 opt-in 副作用", 又消除了 backend-architect 指出的"hardcoded 20s not scaling with N"双重问题 |
| **D4** | submodule 列表从 `.gitmodules` 提取, 不从 `git submodule status` | 前者是 source of truth 且可用无网络; 后者需要实际 checkout 状态, 在 shallow clone / CI 场景下可能失败 |
| **D5** | 每个 submodule 独立 platform 检测 | 支持未来跨平台场景 (如主 repo 在 Forgejo, submodule 在 GitHub); 首版 Aria 全部 Forgejo, 仅为扩展点预留 |
| **D6** | 缓存文件 **单文件多 repo 结构** + **schema_version 字段** (Round 2 修复 R1 C1) | 新增 `schema_version: "1.1"` 字段作为 cache migration 守卫; reader 识别缺失或低版本 schema → cold re-fetch. 原 v2.9.0 `issues.json` 实际是 `{fetched_at, platform, open_issues:[]}` 单 repo 扁平结构 (本 Spec 发现前的 Round 1 认知错误), **不是** 已预留的多 repo 结构; v1.16.0 新增 `schema_version` 字段显式管理迁移 |
| **D7** | 推荐规则 `open_blocker_issues` **聚合所有 repo** | 任一 repo 的 blocker 都应触发降级; 不按主 repo / submodule 区分 severity |
| **D8** | **不** 修改原 D6 决策本体, 作为补充扩展点 | D6 的 "vendored 场景下噪音控制" 论点仍然成立, 本 Spec 只扩展"meta-repo 场景"的开关, 两个场景解耦 |
| **D9** | 启发式关联 (`linked_us` / `linked_openspec`) **使用主 repo 的** `openspec/changes/` 目录扫描 | submodule 通常没有自己的 openspec 目录; Aria 模式下 OpenSpec 始终在主 repo; 若未来需要 per-submodule openspec 扫描, 再立独立 Spec |
| **D10** | 每个 submodule 的 API 调用失败**独立 fail-soft** | 一个 submodule 失败不影响其他 submodule 的结果; 失败的 submodule 在 `repos[owner/repo]` 下记录 `fetch_error`, `items: []` |
| **D11** | submodule URL 解析失败时**跳过该 submodule**, 不阻断整个 Phase 1.13 | 兼容 D10 fail-soft 原则 |
| **D12** | 本 Spec 不引入新 `fetch_error` 枚举值, 复用现有 10 个 + 新增 3 个 submodule-专属: `submodule_not_initialized` / `no_origin_remote` / `parse_error` (path 层) | submodule 扫描的错误语义大部分与主 repo 一致, 3 个新枚举是 submodule-only 的 path-level 错误, 不污染主 repo 错误空间 |
| **D13** | `limit: 20` 应用于**每 repo**, 非全局上限 (Round 2 新增, 回应 R1 tech-lead M5) | 每 repo 独立 limit 避免大 repo 抢占小 repo 的配额; Aria 场景: 4 repo × 20 = 80 items 上限, 实际 5 items (远低于上限). 未来如 items 膨胀到影响 UI, 可在聚合视图追加 truncate/paginate 逻辑 (本 Spec 不含) |
| **D14** | `stage_timeout_seconds` 分档行为 (Round 2 新增, 回应 R1 tech-lead I3) | `scan_submodules=false` 保留 v1.0 的 12s (不变), `scan_submodules=true` 用自适应公式 `max(20, (N+1)×5)`. 用户显式设置优先级最高. 两条路径各自的 SLA 清晰: 向后兼容用户享受相同预算, 新功能用户享受按需扩展 |
| **D15** | v1.0/v1.1 输出 schema **双写别名** `open_issues` == `items` (Round 2 新增, 回应 R1 backend-architect I1) | v1.0 消费者读 `open_issues` 仍然工作, v1.1+ 消费者读 `items` 享受 `repo` 字段。writer 双写代价可忽略 (内存引用). 别名将在 v2.x deprecate, 至少跨 2 个 MINOR 版本的 deprecation window |

---

## Impact

### 代码影响

**aria-plugin 子项目** (对应 Aria 主仓库的 `aria/` submodule):

1. `aria/skills/state-scanner/SKILL.md`
   - Phase 1.13 章节追加 `scan_submodules` 配置项说明
   - 输出 schema 追加 `issue_status.repos[]` 字段文档
   - 推荐规则 `open_blocker_issues` 描述更新 (聚合语义)

2. `aria/skills/state-scanner/references/issue-scanning.md`
   - 新增 §submodule 扫描流程 章节 (~80 行 bash 伪代码)
   - 新增 §.gitmodules 解析 章节
   - 新增 §多 repo 缓存 schema 章节 (文档化已预留结构)
   - 更新 §超时设计 (12s → 20s)
   - 更新 §安全边界 (明确 submodule 扩展不改变 "只读" 原则)

3. `aria/skills/state-scanner/RECOMMENDATION_RULES.md`
   - `open_blocker_issues` 规则描述更新 (聚合所有 repos)

**无代码变更** (state-scanner 是纯 bash-prose skill, 无独立源文件; 行为由 AI 读 SKILL.md 后执行):

实际上 state-scanner 的所有执行逻辑都在 SKILL.md + references 中描述, AI 读完后直接执行 bash 命令。本 Spec 的"代码改动"都是 Markdown 文档修改, 但行为改变是实质性的。

### 项目影响

**Aria 主项目** (本仓库):

1. 新增 `openspec/changes/state-scanner-submodule-issue-scan/proposal.md` (本文件)
2. 更新 `.aria/config.json` 在 `state_scanner.issue_scan` 块追加 `scan_submodules: true` (Aria 项目级 dogfooding)
3. 更新 `aria/` submodule pointer (aria-plugin 的 SKILL.md 修改后)

### SemVer 裁决

本 Spec 的变更性质评估:

- ✅ **不改变任何现有字段语义** (向后兼容)
- ✅ **不强制用户迁移** (opt-in, 默认 false)
- ⚠️ **新增配置项** (functional additive)
- ⚠️ **新增输出字段** `issue_status.repos[]` (schema additive)

**裁决**: **MINOR** (v1.16.0) — 符合 SemVer 的 MINOR 语义 (新功能 + 向后兼容)。

**备选方案**: 若产品负责人认为本变更属于 "纯文档 + opt-in, 实际影响面极小", 可裁决为 PATCH (v1.15.3) — 但需要豁免 /skill-creator benchmark 要求 (见下方 Risks)。

**推荐 MINOR**: 避免豁免 benchmark, 走标准发版流程。

### Benchmark 要求

按 CLAUDE.md 规则 #6 + memory `feedback_use_skill_creator_benchmark.md`:

- Skill 逻辑变更 → 必须 `/skill-creator benchmark`
- 本 Spec 改变 state-scanner 的 Phase 1.13 行为 (新增分支), 属于 Skill 逻辑变更
- **结论**: 本 Spec 的实现合并前必须跑 benchmark

**备注**: 因为这是一个纯 additive + opt-in 的变更, benchmark 的 AB 对比场景会很有趣 — `scan_submodules: true` vs `false` 的 delta 应该在有 submodule issue 的项目上为正, 在无 submodule 的项目上为零。benchmark 结果本身就是对本 Spec 价值的实证。

---

## Acceptance Criteria

### AC-1: 配置开关生效

- [ ] `scan_submodules: false` (默认) 时, Phase 1.13 行为与 v2.9.0 字节级相同
- [ ] `scan_submodules: true` 时, Phase 1.13 枚举 `.gitmodules` 并扫描所有 submodule
- [ ] 配置项在 SKILL.md 和 references/issue-scanning.md 中文档化

### AC-2: .gitmodules 解析正确

- [ ] 正确解析 `.gitmodules` 中的 `path` 和 `url` 字段
- [ ] 兼容子模块路径含空格 (如 `"my lib"`)
- [ ] 对 `.gitmodules` 不存在的场景静默降级 (回退到仅扫主 repo)
- [ ] 对 `.gitmodules` 存在但为空的场景静默降级

### AC-3: 每个 submodule 独立 fail-soft

- [ ] 某 submodule 的 API 失败不阻断其他 submodule 扫描
- [ ] 失败 submodule 在 `issue_status.repos[owner/repo]` 下记录具体 `fetch_error`
- [ ] 失败 submodule 的 `items` 为空数组, 不污染聚合视图

### AC-4: 缓存命中正确

- [ ] 缓存 TTL 内 (15 分钟) 不重复调用 API
- [ ] 缓存文件 schema 可容纳多 repo (已预留, 仅验证)
- [ ] 缓存失效后同步 refresh 并覆写

### AC-5: Aria 项目实测 ⚠️ **LIVE-DATA DEPENDENT** (Round 2 修复 R1 qa-engineer M8)

**声明**: 本 AC 依赖 2026-04-15 当日 Aria 项目的 live issue 快照, 是**烟雾测试级别**验收 (smoke test), 非**长期回归门槛** (regression gate). 一旦 aria-plugin#17/#18 或 aria-orchestrator#1 被关闭, 本 AC 将无法自动通过。长期回归应通过 benchmark eval suite 的 fixture 化数据覆盖 (见 §未完成的工作)。

- [ ] 本地运行 `/state-scanner` 后, `issue_status.repos` 应含 4 个 key (`10CG/Aria`, `10CG/aria-plugin`, `10CG/aria-standards`, `10CG/aria-orchestrator`)
- [ ] `10CG/aria-plugin` 的 items 应含 #17 / #18 (2026-04-15 快照, 若被关闭则重新评估)
- [ ] `10CG/aria-orchestrator` 的 items 应含 #1 (同上)
- [ ] `10CG/aria-standards` 的 `open_count` 为 0
- [ ] 推荐决策能看到所有 repo 的 items

### AC-6: 推荐规则聚合 ⚠️ **LIVE-DATA DEPENDENT** (Round 2 修复 R1 qa-engineer M8)

**声明**: 本 AC 的 "任一 repo blocker 触发降级" 验证要求有一个实际带 blocker/critical label 的 open issue。当前 Aria 项目的所有 open issue 均无 label (`labels: []`), 本 AC 无法以 live-data 形式验证。长期应通过 fixture-based eval 测试本规则的聚合逻辑。

- [ ] `open_blocker_issues` 规则评估时聚合所有 repos 的 items (代码路径存在性)
- [ ] 任一 repo 的 blocker label 触发降级推荐 (**需要 fixture 测试, live 场景下 untested**)
- [ ] 推荐输出显示 "来自 submodule 的 blocker" 的来源信息

### AC-9: Round 2 新增 — Backward compat regression (修复 R1 qa-engineer I9)

- [ ] `scan_submodules=false` 默认路径在 benchmark eval-backward-compat 中通过 (输出 schema 无 `repos` 字段, `items[]` 只含主 repo, 行为与 v2.9.0 一致)

### AC-7: 文档完整性

- [ ] `references/issue-scanning.md` 新增 §submodule 扫描流程 章节
- [ ] SKILL.md Phase 1.13 章节更新
- [ ] RECOMMENDATION_RULES.md 更新聚合语义

### AC-8: Benchmark 通过

- [ ] `/skill-creator benchmark` 在 Aria 测试集上执行
- [ ] 有 submodule 的项目场景: `scan_submodules=true` delta ≥ 0 (不应下降)
- [ ] 无 submodule 的项目场景: delta ≈ 0 (零影响)
- [ ] 结果存入 `aria-plugin-benchmarks/ab-results/`

---

## Rollback Plan

**Level 1 (最快回滚, 运行时降级)**: 用户/CI 设置 `scan_submodules: false`
- 零发布, 运行时降级
- 回到 v2.9.0 行为
- ⚠️ **限制 (Round 2 修复 R1 qa-engineer M7)**: Level 1 **仅在缺陷限于 `scan_submodules=true` 执行分支**时有效。若缺陷位于共享代码路径 (例如 cache writer 无条件写入 `schema_version` 字段导致 v1.0 reader 困惑), Level 1 不生效, 必须 Level 2 代码回滚。
- **判定方法**: 出现 bug 后, 先执行 `jq 'del(.state_scanner.issue_scan.scan_submodules)' .aria/config.json` 并重跑 state-scanner, 若 bug 消失 → Level 1 有效; 若 bug 仍在 → Level 2 或 Level 3

**Level 2 (代码回滚)**: 如果发现 `scan_submodules=true` 下或共享路径上有严重 bug
- 回滚 aria-plugin 的 SKILL.md / issue-scanning.md / RECOMMENDATION_RULES.md / CHANGELOG.md 到 v1.15.2 版本 (git revert aria-plugin commit 488e736+)
- 回滚 Aria 主仓库的 openspec/changes/state-scanner-submodule-issue-scan/ (git revert 主 repo commit)
- 删除 `.aria/cache/issues.json` (schema 不兼容, 重建)
- `.aria/config.json` 的 `scan_submodules` 字段保留但无效果

**Level 3 (完全撤回)**: 如果 meta-repo 模式在实测中被证明是伪需求
- 归档本 Spec 但不提交到 archive (标注 "Reverted")
- 更新 memory 记录 "meta-repo submodule 扫描场景不具普遍性"

---

## 后续 Spec 锚点

本 Spec 聚焦在 Phase 1.13 submodule 扫描。以下相关但**独立**的问题由其他 Spec 处理:

1. **Phase 1.14 Forgejo 配置检测的 submodule 扩展** — 独立 Spec (下次发现时再立)
2. **跨 repo PR 感知** — 完全独立功能, PR 感知尚未实现, 需要先立 PR-awareness Spec
3. **每个 submodule 独立的 OpenSpec changes 扫描** — Aria 模式下 OpenSpec 只在主 repo, 暂无需求
4. **submodule 自动发现 "same-org" 启发式开启** — 等待 meta-repo 模式普及度观察, 至少 3 个项目采用后再考虑
5. **Phase 1.13 机械化执行 (L3)** — 由姐妹 Spec `state-scanner-mechanical-enforcement` 处理

---

**创建**: 2026-04-15
**版本**: 0.1 (Draft)
**Level**: 2 (Minimal, proposal.md only)
**关联姐妹 Spec**: `state-scanner-mechanical-enforcement` (不合并, 单一焦点分离)
