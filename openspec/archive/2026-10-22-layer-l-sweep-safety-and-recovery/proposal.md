# layer-l-sweep-safety-and-recovery — sweep 误伤防护: TTL/归属分层 + provenance + swept 信号 + 恢复

> **Level**: Full (Level 3 Spec)
> **Status**: **Done (shipped v1.77.1, PR #251 `d9b3852`, 2026-10-22; 原 Approved owner 2026-10-22 主案 7d)** — Rule #6 场景 1 AB PASS + 17 SC; #233/#167 已关
> **Created**: 2026-10-22
> **Linked Issue**: `10CG/Aria#233` (+ `10CG/aria-plugin#167` provenance 字段缺口)
> **执行轨**: interactive

## Why

#231 同日 recon (2026-10-22, v1.77.0 `f2e801d`) 逐条核实 #233 三因全部成立:

1. **心跳只在 `/state-scanner` 入口刷新** — `phase1_gate.py:571-581` 自认: acquire 复用路径**不**刷心跳, "no production heartbeat loop exists"; 心跳 = 入口 hook, 长会话 (带压缩跨数天) 入口之后心跳永冻。
2. **`--sweep-stale` 是例行收尾动作且跨容器** — `gc.py:sweep_stale_active` "Cross-container by design"; `phase-d-closer` D.2b 标准命令带它, 任何容器收尾都扫全 ref; `SWEEP_TTL=24h` (`constants.py:53-66`, 其注释前提「24h comfortably exceeds real interactive session lengths」对「两次刷新间隔」语义不成立)。
3. **被扫后零信号** — `claim_lifecycle.py` heartbeat/release 均 `status=="active"` 过滤; sweep 改写 `abandoned` 无 provenance 字段 (#167), 持有方收到 `claim_not_found` (benign), phase-d-closer 解释为「早已释放/未认领」。

结果: 仍在干活的轨被例行收尾静默清除, 从所有碰撞面消失, 持有方无感知 (#233 复现 4 步全真)。

## What Changed

### 1. sweep 分层化 (破坏面收窄) — `gc.py` + `release_gate.py`

| 参数 | own-container claim | cross-container claim |
|------|--------------------|----------------------|
| `--sweep-stale` (D.2b 例行, 默认) | TTL `SWEEP_TTL` (24h, 不变) | TTL **`SWEEP_TTL_CROSS` = 604800 (7d, 新)** |
| `--sweep-stale-all` (显式运维动作, 新) | 24h | 24h (旧行为, 保留给确知全 ref 死寂的 ops) |

- 新常量 `SWEEP_TTL_CROSS` (`constants.py`, 注释写明分层依据: own = 自伤可自愈; cross = 误伤他人且其无信号, 须保守)。
- `sweep_stale_active(..., cross_ttl_seconds=..., container_id=...)` 签名扩展 (向后兼容默认值 = 现行为, CLI 层接新分层); release_gate 从 identity 取 container 传入。

### 2. sweep provenance (补 #167) — `gc.py`

改写 `abandoned` 时增写两字段 (schema additive): `swept_by: <container-id>`, `swept_at: <ISO-ts>`; heartbeat_at 原样保留 (既有不变量, review C1)。无 provenance 的旧 abandoned 记录兼容 (字段缺省 = 历史扫除, 信号面按 unknown 呈现)。

### 3. swept-aware 信号 (消灭伪装 benign) — `claim_lifecycle.py` + 两 CLI + phase-d-closer

- `heartbeat_by_track` / `release_claim_by_track` 匹配不到 active 时**二次查找**同 (container, track) 的 `abandoned` 且带 `swept_at` 的记录 → 返回 `error="claim_swept"` + 新增 `swept_by` / `swept_at` 字段 (AcquireResult/ReleaseResult additive)。
- `phase1_gate.py --heartbeat-only`: outcome `error` 的 reason 分化 `claim_not_found` vs `claim_swept` (后者附 swept 元数据)。
- `release_gate.py`: released.error 同分化; `--dry-run` 不变。
- phase-d-closer SKILL.md D.2b 段: 「`claim_not_found` 是 benign (早已释放/未认领)」改为三分: `claim_not_found` (benign) / **`claim_swept` (非 benign — 本轨 claim 曾被 `<swept_by>` 于 `<swept_at>` 扫成 abandoned; 若本轨仍活跃 → 见恢复路径, 并在收尾报告记 ⚠️ 待 owner 复议)** / 其他 error。

### 4. 恢复路径 — `release_gate.py --restore`

- `release_gate.py --raw-track-id <X> --restore`: 定位本 container 的 abandoned-with-provenance 记录 → 恢复 `status=active`, `heartbeat_at=now` (swept_by/swept_at 清空), 单 commit 推 ref (失败矩阵复用 resilient_push)。
- **只允许原 container 自恢复** (identity 匹配; 无 `--force` 越权面 — 结构性防伪: 他容器恢复他人 claim 等于伪造占用)。
- 编排契约 (state-scanner SKILL.md heartbeat 段补): 收到 `claim_swept` 信号且本轨仍在干活 → 先 `--restore` 再继续; AI 不得用 restore 抢占他人轨 (restore 只回自己的 track+container)。

### 5. acquire 复用路径刷心跳 — `phase1_gate.py` (代码注释自认 follow-up)

acquire 命中本 container 已有 active claim 复用 (reuse path) 时刷新 `heartbeat_at=now`。一处小改, 直接缩小「心跳冻结」窗。

### 6. SKILL.md prose 两处 (state-scanner + phase-d-closer)

- state-scanner 心跳段: 补「长会话 (跨自然日/长 B/C 阶段) 应周期性 (≤12h 间隔) 调 `--heartbeat-only`」提示 + swept 信号 → restore 编排契约 (上文)。
- phase-d-closer D.2b: sweep 语义描述更新 (分层 TTL), `claim_swept` 三分文案 (上文)。

## rule6_note

```yaml
decision_table_row: 2        # 处方性·指令面 (SKILL.md 两处) + deterministic 代码 (lib/scripts)
scenario1: ab-results/2026-10-22-layer-l-sweep-safety/ PASS   # 3 evals × 2 臂 6/6; 三判别面精确翻转
scenario4b: not_required     # description 零变动
exemption_reason: null       # 代码面 substitute = tests/test_sweep_safety.py 17 SC (基线反事实: stash lib/scripts 全塌)
                             # + 全 state-scanner 套件回归 exit 0 + 真仓 E2E (self-resume 心跳 32Z→55Z; selftest claim 已释放)
notes: >
  AB 双 skill 臂 (phase-d-closer D.2b + state-scanner 心跳段, 快照=origin/master v1.77.0)。
  acquire 复用刷心跳由 phase1_gate 代码承载, 真仓 E2E 验证 (非 AB 面)。
```

## Key Deliverables

- `state-scanner/lib/{constants,gc,claim_lifecycle}.py` + `scripts/{phase1_gate,release_gate}.py`
- `phase-d-closer/SKILL.md` D.2b 段 + `state-scanner/SKILL.md` 心跳段
- 测试: pytest 套件扩展 (sweep 分层 / provenance / swept 信号 / restore / acquire 刷心跳, 每项含反事实) + Rule #6 处置
- 发版: 与轨 A (branch-risk-build-gate-alignment) 同 release train **v1.77.1** (同 target 多 cycle 一次发版惯例)

## Rule #6 处置

| 面 | 性质 | 处置 |
|----|------|------|
| lib/scripts 代码 | deterministic | SC 级 baseline-failing pytest 扩展 (既有套件; 逐新 SC 反事实自证) |
| phase-d-closer SKILL.md D.2b + state-scanner SKILL.md 心跳段 | 处方性·指令面 | **场景 1 AB 照跑** (定向: 邻容器 30h claim 收尾处置 / claim_swept 信号解读与动作) |
| description | 不变 | 4b 不触发 |

## Constraints

| 类型 | 约束 | 来源 |
|------|------|------|
| 行为 | 跨容器 7d 内的 active claim 例行收尾**不得**改写; 24h~7d 区间仅 `--sweep-stale-all` 可清 | #233 预期行为 |
| 兼容 | ClaimRecord 新字段 additive; 旧 abandoned 记录无 provenance 兼容读 | schema additive-only |
| 防伪 | restore 仅原 container; 无越权 flag | 结构性防伪原则 |
| 信号 | `claim_swept` 绝不落入 benign 解释; 收尾报告必须显式呈现 | #233 根因 3 |

## Impact

| 面 | 影响 |
|----|------|
| 消费方 | 全部 Layer L 多终端用户: 例行收尾不再误伤 ≤7d 活跃邻居; 误扫可见可恢复 |
| 已知代价 | 真·死亡容器 claim 的清理从 24h 延到 7d (碰撞面多挂 6d — advisory 语义下可接受; 急清走 `--sweep-stale-all`) |
| 关联 | #233 主诉全解; #167 (provenance) 顺带闭环; STALE_TTL (advisory 30min) 不动 — advisory 与 durable 改写阈值本就分离 (memory: durable_rewrite_ttl_separate_from_advisory_ttl) |

## Open Questions (owner 批 spec 时一并裁)

1. `SWEEP_TTL_CROSS` 取 7d (本 spec 主张) 还是 72h (更紧, 死 claim 清得快但保护窗短)?
2. 例行 `--sweep-stale` 对 cross-container 是否干脆**默认不扫** (只 own), 7d 兜底仅 `--sweep-stale-all`? (更保守; 代价: 死容器 claim 要等显式运维)

> 归档 SHA 回链: `665e686` (归档 mv 提交; 本行由后继钉正提交固定)
