---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-05-29T02:10:21.457Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [backend-architect]
---

# post_spec R1 — backend-architect 审计报告
# 目标: aria-context-monitor (openspec/changes/aria-context-monitor/proposal.md)

---

## 审计结论

### [major] M-1 — 缓存文件 schema 缺少 `schema_version` 字段，无版本化契约
**类别**: data-layer / cache-schema
**范围**: `.aria/cache/context-window.json` (Task 1.1 / 1.2)

提案第90-106行给出的输出结构中没有 `schema_version` 字段。对比已有模式 `.aria/cache/issues.json`，该文件顶层含 `"schema_version": "1.1"`，作为 schema drift 防御的基线。

`context-window.json` 是 statusLine stdin 的转存，该 stdin schema 的变动在历史上已有先例（Spike 第4次推翻了 transcript-based 方案，statusLine 数据丰富度超出预期）。若运行时未来修改字段名称或添加 breaking change，无版本标记的 cache 被 `token_telemetry.py` 静默读取，将产生错误数据而不是可检测失败。

**要求**: `context-window.json` 必须含顶层 `"schema_version"` 字段（如 `"1.0"`），`token_telemetry.py` 读取时验证版本号，不匹配时报 `confidence=estimate` 并回退 transcript 路径。

---

### [major] M-2 — relay 写操作的原子性未规范，部分写入产生 corrupt JSON
**类别**: data-integrity / concurrency
**范围**: statusLine relay 行 / `setup_relay.sh` (Task 1.3) → `token_telemetry.py` 读取 (Task 1.2)

提案第85-86行描述 relay 为 "1 行写 `.aria/cache/context-window.json`"，statusLine 每次渲染时触发。Claude Code 渲染频率可为连续（尤其 Phase B 密集输出期）。

单行 `echo ... > file` 或 `jq ... > file` 的重定向在 shell 层面是非原子操作——open/truncate 与 write/close 之间，若另一进程（`token_telemetry.py` 读取或并发 statusLine 触发）在 truncate 后 write 完成前读取，拿到的是空文件或截断 JSON，会触发 `json.JSONDecodeError`。

提案 "Backward compat" 节（第124行）提到 "skill 仍返回 ... unavailable, 不报错"，但未说明是否将此归为 corrupt-JSON 场景，也未要求 `token_telemetry.py` 对 `JSONDecodeError` 做防御处理。

**对比**: `issues.json` 通过 Python `json.dump` + `rename` 模式（原子替换）写入，规避此问题；relay 行是 shell 写入，缺少此保护。

**要求**:
1. relay 行写法改为原子 `tmp → rename`：`jq -c '...' > /tmp/ctxwin.$$.json && mv /tmp/ctxwin.$$.json .aria/cache/context-window.json`
2. `token_telemetry.py` 读取 cache 时捕获 `JSONDecodeError` / `OSError`，返回 `{"source": "unavailable", "confidence": null}` 而非抛出异常
3. Task 1.7 测试场景明确覆盖 "corrupt cache JSON" (当前仅列"陈旧"和"无 statusLine")

---

### [major] M-3 — window-source 4 档解析链的决定性顺序与 DEC 文档存在不一致
**类别**: data-layer / resolution-chain
**范围**: `token_telemetry.py` fallback 路径 (Task 1.2 / 1.6)

提案第79行描述 fallback 3 档 window size 解析链为：
```
relay-cached size > config window_tokens > observed-peak 下界 > 200K 默认
```

DEC-20260529-001 决策文档（第63行）表述一致，同为这 4 档。

问题在于第 2 档（`config window_tokens`）的 config key 路径未在 proposal 任何位置规范：
- `config.json` 现有结构（已审查）中无 `context_monitor` 命名空间
- `config.template.json` 中同样没有对应字段
- proposal 第79行仅写 `config window_tokens`，不给出 JSON path（如 `context_monitor.window_tokens`）

这意味着 Task 1.2 实现者需自行决定 config key，形成实现与 Spec 的合同裂缝，回归测试（Task 1.7）对此无法验证正确性。

对比 `resolve_forgejo_hosts` 模式（`_common.py` 第77行明确写出 JSON path `state_scanner.issue_scan.platform_hostnames.forgejo`），context-monitor 解析链第2档缺少同等精度的规范。

**要求**: 在 proposal 或 SKILL.md 契约中明确 config key 的完整 JSON path（建议 `context_monitor.window_tokens`），并在 `config.template.json` 新增对应可选字段注释。

---

### [major] M-4 — `observed-peak 下界` 的持久化机制未定义
**类别**: data-layer / fallback-semantics
**范围**: `token_telemetry.py` fallback 路径 (Task 1.2)

4 档 fallback 第3档 `observed-peak 下界` 语义为"见过的最大 input_tokens 值"，但 proposal 未定义：
1. 该 peak 存储在哪里（session 内易失 vs 持久化至 `.aria/cache/` ）
2. 跨 session 是否复用（DEC 第79行"relay-cached size 复用 (见过即持久)"隐含持久，但 proposal 正文不对应）
3. 与 relay-cached size 的关系：若第1档 cache 文件存在但过期（staleness_seconds 超阈值），是否仍复用其中的 `context_window_size` 字段作为 "relay-cached size"（第1档降级为 size-only 复用）？

第2档 config 和第3档 peak 之间的优先级本质上假定 config 更可靠（显式配置 > 经验推断），但若用户配了错误的 `window_tokens`（如 200000 实际跑 1M window），peak 反而更准。该设计选择未在 proposal 中说明，会导致实现者对"允许哪种形式的 override"产生分歧。

**要求**:
1. 明确 observed-peak 持久化策略（建议持久化到 `.aria/cache/context-window-peak.json` 或合并入 cache 主文件）
2. 明确 stale relay cache 中 `context_window_size` 字段是否可作为 size-only source（与 used_percentage 分离复用）

---

### [minor] m-1 — `staleness_seconds` 的阈值未规范，skill 判断标准不统一
**类别**: data-layer / staleness-semantics
**范围**: Task 1.6 / SKILL.md (Task 1.4)

输出结构中含 `staleness_seconds` 字段，但 proposal 未规定：
- 何值以下为 "fresh"（用于高置信度输出）
- 何值以上强制降级至 transcript fallback
- 阈值是否可 config（类似 `cache_ttl_seconds: 900` 在 issues.json 模式）

statusLine 渲染触发频率与用户行为强相关（密集对话 vs 空闲等待），没有固定的 staleness budget。不同消费场景（phase-b 决策 vs 用户查询）可接受的 staleness 也不同。

**要求**: 在 SKILL.md 或 proposal 中给出默认 staleness 阈值（建议 300s）并允许 config override，明确超阈值行为（confidence 降级而非 source 切换，保留 context_window_size 复用）。

---

### [minor] m-2 — `lib/token_telemetry.py` 放置路径与共享 lib 惯例冲突
**类别**: data-layer / modularity
**范围**: Task 1.2 (提案第84行)

提案定义 collector 路径为 `aria/skills/state-scanner/scripts/lib/token_telemetry.py`。但该 lib 的设计意图是被两个独立 skill 复用（context-monitor + #18 estimator）——将其放在 `state-scanner/scripts/lib/` 下，意味着 `aria-context-monitor` 和未来 `#18 estimator` 需跨 skill 目录引用，形成非显式依赖。

已有模式是 `state-scanner/lib/`（coordination_ref.py / claim_schema.py 等）用于 state-scanner 自身基础设施，不跨 skill 共享。

将一个真正跨 skill 的 collector 藏在 `state-scanner/scripts/lib/` 是错误的归属信号，可能导致 #18 estimator 实现时将其复制而非复用，重蹈 #57 式数据层重复。

**建议**: 路径改为 `aria/lib/token_telemetry.py`（顶层共享 lib）或 `aria/skills/_shared/token_telemetry.py`（共享 skill 库），并在 proposal 中给出 import 路径示例。此为建议性非阻塞，但强烈推荐在实施前确认。

---

### [minor] m-3 — `jq` 硬依赖在 relay 行，但 doctor 检测时机晚于写入失败
**类别**: operability
**范围**: setup_relay.sh (Task 1.3) / aria-doctor (Task 1.5)

提案第86行明确 `jq` 为硬依赖，doctor 负责检测。但依赖检测（Task 1.5）在 relay 安装（Task 1.3）之后执行；若 `jq` 缺失，relay 行每次 statusLine 渲染时静默失败（shell exit non-zero），cache 文件不更新，skill 静默回退 fallback——用户无明确错误提示。

**要求**: `setup_relay.sh` 在注入 relay 行之前主动检测 `jq`，缺失时拒绝注入并打印安装指引，而不是依赖 doctor 事后发现。

---

## Verdict

| 类别 | 数量 |
|------|------|
| Critical | 0 |
| Major | 4 (M-1 schema versioning, M-2 atomicity, M-3 config key path, M-4 peak persistence) |
| Minor | 3 (m-1 staleness threshold, m-2 lib path, m-3 jq preflight) |

**总体**: PASS_WITH_WARNINGS

4 个 major 均可在 Task 1.1-1.3 实施前通过补充 proposal 规范解决，无需推翻架构。核心数据流（statusLine relay → cache → skill）和 fallback 3 档设计从后端架构角度正确；major 集中在"已有正确意图但规范不足"而非"方向错误"。

---

## Verdict 依据

### 通过的核心设计

1. **statusLine relay 架构正确**: 零计算主路径（runtime 直接给 size+%），3 档 fallback 覆盖无 statusLine 场景，与 resolve_forgejo_hosts 3 层模式对齐（精度差见 M-3）
2. **Q2=a 决策正确**: `token_telemetry.py` 只解析 raw counts，不内置 window% 计算，单一职责，estimator 复用无耦合
3. **portability split 正确**: data schema（statusLine stdin）通用；relay 抓取配置相关；3 档 fallback 正确分离两个可变性维度
4. **`data schema universal / relay config-dependent` 划分**: 与 DEC-20260529-001 完全一致，架构上无歧义

### 主要风险点

1. **M-2 原子性风险**: 实际 Phase B 密集场景中 statusLine 渲染可频繁触发，partial write 概率非零，且 `json.JSONDecodeError` 未被覆盖；这是实施层面的数据完整性 gap
2. **M-3/M-4 规范不足**: 两个 fallback 档的实现细节（config key path、peak 持久化）若在 Task 1.2 实施前不固化，实现会自行决定，导致 Task 1.7 测试无法验证正确性

---

## 轮次记录

| 轮次 | 时间 | Agent | Verdict |
|------|------|-------|---------|
| R1 | 2026-05-29T02:10:21Z | backend-architect | PASS_WITH_WARNINGS (0C 4M 3m) |
