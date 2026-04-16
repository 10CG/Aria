# aria-2.0-m0-prerequisite — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-020](../../../docs/requirements/user-stories/US-020.md)
> **Total**: 96.5h (Core 86.5h + Buffer 10h)

## Task 工时基线

| ID | Task | 工时 | 依赖 | 验收 |
|---|---|---|---|---|
| **T0** | US-020 头部 Estimated 字段同步 (80h → 96.5h) | 0.1h | — | §文档对齐 |
| **T1** | Legal 前置闸门 (5 项 Legal Memo) | 4.5h | — | T1.done |
| **T2** | A3 NFS + Nomad bind mount 实测 | 4.5h | — | T2.done |
| **T3** | A1 Dockerfile + headless plugin + GLM smoke | 10h | T1.pass, T2.pass | T3.done |
| **T4** | Hermes Spike (详见 spike Spec) | 52h | T1.pass | T4.done |
| **T5** | AD1-AD12 收敛 (含 AD3 回填) | 8h | T4.done | T5.done |
| **T6** | M0 Report + handoff.yaml + PRD patch PR 起草 | 7.5h | T1-T5 | T6.done |

---

## T0 — US-020 头部同步

**先决**: 本 Spec 归档前零散工作的第一步, 与 review log 保持一致。

- [x] US-020.md 头部 `Estimated: ~96.5h / 2 weeks` 已同步 (执行时已在 Round 4 收敛后立即完成)
- [x] Agent Team review log status: `converged`, rounds_completed: 4

---

## T1 — Legal 前置闸门 (4.5h, Day 0-1)

> **重要**: T1 是 Day 0-1 前置闸门, T3/T4 启动条件 = `T1.status == done && T1.new_concerns == ∅`; T1 `awaiting_external` 时 T2 可启动, T3/T4 hold。

**状态 (2026-04-15 回填)**: T1 substantive work 已于 2026-04-14 完成 (Memo v1.1), T3/T4 解锁。产品负责人 final signoff 仍为 `awaiting_external`, 不阻塞 T5/T6, 由 T6 M0 Report 交付时一并完成。

- [x] **T1.1** License 兼容性查证 (1.5h) — 2026-04-14 完成
  - Spike 第 5 维度执行 `license-checker` + `pip-licenses` 全量扫描, 产出 `aria-orchestrator/spikes/hermes-route/license-matrix.json` (477 packages direct+transitive)
  - 结果: GPL/AGPL 直接依赖 **0**; LGPL direct **0**; Unknown direct **0** — fork 路径未自动降级 (但最终由 Spike 量化结论 → Option C Extension-only, 非 fork)
  - 详见 Legal Memo IS-1 + `aria-orchestrator/spikes/hermes-route/license-scan-report.md`
- [x] **T1.2** GLM 5.1 ToS 自动化条款查证 (0.5h) — 2026-04-14 完成
  - WebSearch + WebFetch 未定位官方 ToS 自动化条款级文本 ("信息不可得")
  - 产品负责人锁定策略 = **路径 B (被动 pending + 自承诺签字)**, 写入 M0 Report R9 章节
  - 详见 Legal Memo IS-2 + §5 结论性质汇总
- [x] **T1.3** Luxeno 代理授权 + 数据流合规 (0.5h) — 2026-04-14 完成 (v1.1 澄清)
  - 产品负责人澄清: **Luxeno = silknode (10CG 自有品牌, 不落地存储)**, 不构成第三方代理合规风险, 无需 DPA
  - 详见 Legal Memo IS-3
- [x] **T1.4** 跨境合规 (1h, 仅风险提示深度) — 2026-04-14 完成
  - 基于 IS-3 澄清 (10CG→silknode→GLM 为内部系统 API 透传, 无数据出境存储), **不触发**中国数据出境合规义务
  - 详见 Legal Memo IS-4
- [x] **T1.5** Docker pull 事实分发审计 (0.5h) — 2026-04-14 完成
  - 主仓库 grep 确认: M0 文档无 `docker pull aria-runner` 示例, 仅含本地 `docker build` + 构建时 `DEPLOY_ENV` 门控
  - 详见 Legal Memo IS-5
- [x] **T1.6** Aether 节点物理归属查证 (0.5h) — 2026-04-14 完成 (v1.1 澄清)
  - 产品负责人澄清: **Aether heavy-80/81/82 为 10CG 自有集群**, R10 风险项 **不触发**, 无需第三方 DPA
  - 失效触发: 未来若引入第三方托管节点 (burst / 混合部署) → Memo 失效, 须重新评估并触发 R10 流程
  - 详见 Legal Memo IS-6
- [x] **T1 交付物**:
  - `aria-orchestrator/docs/r1-legal-memo.md` v1.1 (使用 `standards/legal/scoped-memo-template.md`, 含司法辖区 / Out of Scope / 风险提示 vs 合规结论边界 / 失效条件 §6 / 免责声明 §7)
  - `aria-orchestrator/spikes/hermes-route/license-matrix.json` (T1.1 产出)
  - R9 三态章节写入: T6.1 M0 Report 起草时合并
- [ ] **T1 final signoff** (awaiting_external, 不阻塞 T5/T6)
  - Memo §8 `Final approver signature` pending, 由 T6 M0 Report 交付时一并完成

**时序约束**:
- T1 ≤ 4.5h (硬边界)
- T1 升级邮件确认 → timebox ≤ 5 工作日, 超时按 No-Go 处理
- T1 完成前 T3/T4 hold

---

## T2 — A3 NFS + Nomad Bind Mount 实测 (4.5h)

> **R8 决策**: Spec 原假设 NFS 栈被 T2.1 实测推翻, 改用 virtiofs + Nomad docker driver `config.volumes` (W 方案, 零 client.hcl 侵入)。详见 [`artifacts/t2/decision-r8-virtiofs-vs-nfs.md`](./artifacts/t2/decision-r8-virtiofs-vs-nfs.md)。

- [x] **T2.1** Aether 存储挂载现状调查 (1h) — 2026-04-15
  - ~~查证 heavy-80/81/82 是否挂载 `nfs-fastpool-aether`~~ → 无 NFS, 实际是 virtiofs `aether-share` 透传
  - 产出 [`artifacts/t2/nfs-status.md`](./artifacts/t2/nfs-status.md) (节点 × 挂载点矩阵 + Nomad agent user 结论)
  - 原始 probe: [`artifacts/t2/raw/heavy-{80,81,82}-probe.txt`](./artifacts/t2/raw/)
- [x] **T2.2** Nomad parameterized dispatch 实测 (2h) — 2026-04-15
  - [`aria-storage-smoke.hcl`](./artifacts/t2/aria-storage-smoke.hcl) (W 方案, 用 `config.volumes` 替代 host_volume)
  - 通过 Nomad HTTP API 验证 (本地无 Nomad CLI, 替代 `nomad alloc exec`)
  - 3 次 dispatch 覆盖 heavy-1/2/3 各一次, 容器内写 UUID + alloc_id + md5 到 `/opt/aria-outputs/smoke-<smoke_id>.txt`, 全部 exit 0
  - 证据: [`artifacts/t2/t2.2-dispatch-log.txt`](./artifacts/t2/t2.2-dispatch-log.txt)
- [x] **T2.3** 宿主侧 md5 双向校验 (1h, 核心部分) — 2026-04-15
  - Nomad agent 以 **root (UID 0)** 运行 (systemd 无 `User=`, `ps -o user,comm` 显示 root), UID 推断步骤简化
  - 容器内 md5 `c681d046...` ↔ 宿主 md5 `c681d046...` 字节级一致 (bind mount 无漂移)
  - 跨 3 节点 md5 交叉校验: 9 个值全一致 (3 节点 × 3 文件)
  - 权限: bind mount 目录 0777 root:root, 容器写入文件 0644 root:root
  - **延后到 M1 US-022**: 非 root 容器 UID (如 1000) 写入 + virtiofs 并发 locking + 三节点同写 last-writer-wins (M0 探针已证通路)
- [x] **T2.4** Nomad meta 边界测试 (0.5h) — 2026-04-15
  - 宽扫 1K→1M + 二分 120K→150K, 定位边界 **131048 bytes (max) / 131049 bytes (first fail)** per meta key
  - 根因: **Linux kernel `MAX_ARG_STRLEN = 131072` (128 KiB)**, 不是 Nomad 限制
  - PRD R7 "64KB" 假设偏保守, 实际约 128 KiB — 缓解方案 (prompt 走文件) 保持不变, 修订后约束 `len(v) < 100KB` per key
  - 证据: [`artifacts/t2/t2.4-meta-boundary.md`](./artifacts/t2/t2.4-meta-boundary.md)
- [x] **T2 交付物** (含 R8 override):
  - [x] [`nfs-status.md`](./artifacts/t2/nfs-status.md)
  - [x] [`aria-storage-smoke.hcl`](./artifacts/t2/aria-storage-smoke.hcl) (原 `aria-nfs-smoke.hcl`, R8 改名)
  - [x] [`storage-validation-report.md`](./artifacts/t2/storage-validation-report.md) (原 `nfs-validation-report.md`, R8 改名, 结论: **A3 假设 PASS**)
  - [x] [`decision-r8-virtiofs-vs-nfs.md`](./artifacts/t2/decision-r8-virtiofs-vs-nfs.md)
  - [x] [`t2.4-meta-boundary.md`](./artifacts/t2/t2.4-meta-boundary.md)
  - 原 fallback "单节点 constraint pin heavy-80" 不再适用: W 方案已零侵入全节点验证

**T1 No-Go 下的处置**: T2 产出部分有效 (基础设施事实), knowledge-manager 在 M0 Report 对涉及 GLM/luxeno 的段落做 strikethrough 标注, phase-c-integrator 在 pre_merge 检查点验证。

---

## T3 — A1 Dockerfile + headless plugin + GLM smoke (10h)

> **前置**: T1.done (T3.4/T3.5 依赖合规结论), T2.pass ✅ (bind mount 路径已确认)
> **T3.1-T3.3 + T3.6 合规中性**: 不触碰 GLM/luxeno, 不依赖 T1, 可并行推进

- [x] **T3.1** Dockerfile 初版 (3h) — 2026-04-16
  - `aria-orchestrator/docker/aria-runner/Dockerfile` + `entrypoint.sh`
  - 基于 `node:20-bookworm-slim` + `@anthropic-ai/claude-code@latest` (npm global)
  - aria-plugin 加载: build-time `COPY aria/ /opt/aria-plugin/` + runtime `--plugin-dir` flag (AD2)
  - DEPLOY_ENV 构建时门控 (Dockerfile RUN 层 + CI workflow 双重验证)
  - CI: `.forgejo/workflows/build-aria-runner.yaml` (Aether CI 规范, Forgejo Registry push)
- [ ] **T3.2** Headless plugin 加载验证 (2h)
  - 验证脚本: `aria-orchestrator/docker/aria-runner/tests/t3-verify.sh` §T3.2
  - 容器内 `claude -p --plugin-dir /opt/aria-plugin "列出可用 aria skills"` 期望触发 plugin
  - 判定: stdout 包含 ≥3 个已知 skill 名称 (state-scanner / spec-drafter / brainstorm 等)
  - 证据归档到 `/opt/aether-volumes/aria-runner/outputs/t3-evidence/`
- [ ] **T3.3** Read-only rootfs + bind mount 共存验证 (1.5h)
  - 验证脚本: `aria-orchestrator/docker/aria-runner/tests/t3-verify.sh` §T3.3a-T3.3d
  - T3.3a: `--read-only --tmpfs /tmp -v ...outputs:/opt/aria-outputs` 下 bind mount 可写
  - T3.3b: `/tmp` tmpfs 可写
  - T3.3c: rootfs 写入被正确拒绝
  - T3.3d: `claude -p` 在 read-only 模式下运行 (需 tmpfs 覆盖 `~/.claude` / `~/.npm` / `~/.config`)
- [ ] **T3.4** GLM smoke test (1.5h)
  - 从 `aria-plugin-benchmarks/ab-suite/glm-smoke/templates/*.j2.md` 模板生成 5 条合成 prompt (禁止真实采样)
  - 用 GLM 5.1 API 生成拟人任务描述
  - 每条 prompt 跑 `claude -p` 触发 state-scanner
  - 二值化判定: ≥4 条触发且返回非空 YAML (grep `current_phase:`) = pass
  - 失败 → 升级 R8 评估
  - **所有 5 条样本** 归档到 `ab-suite/glm-smoke/failed-samples/<timestamp>-<seq>.yaml`
  - Schema: `{prompt, failure_mode, raw_output, expected_grep, glm_model_version, status: pass|fail}`
  - `failure_mode` 枚举: `not_triggered | triggered_empty_yaml | triggered_invalid_yaml | partial_response | timeout`
  - 产出 `summary.yaml` 含 5 条索引
- [ ] **T3.5** Fixture 模板二审 (1h)
  - ai-engineer 审核 5 个模板占位符 (禁含业务纹理)
  - **legal-advisor (人类) 最终签字** 写入 `templates/REVIEW.md`
  - AI agent 意见仅 audit trail, 不构成放行依据
- [ ] **T3.6** `image_sha256` 记录 (0.5h)
  - 验证脚本: `aria-orchestrator/docker/aria-runner/tests/t3-verify.sh` §T3.6
  - `docker inspect --format='{{.Id}}'` → `t3-evidence/t3.6-image-sha256.txt`
  - CI workflow 也在 step summary 中记录 SHA256
- [ ] **T3.7** 缓冲 (0.5h)

**T3 触发阈值**: 实测 > 16h → A1 失败评估, 可能触发 R8

---

## T4 — Hermes Spike (52h, 详见 Spike Spec)

详见 [aria-2.0-m0-spike-hermes/tasks.md](../aria-2.0-m0-spike-hermes/tasks.md).

本任务在本 Spec 中仅作为占位 + 工时预算登记, 具体步骤与验收在 Spike Spec 内定义。

**触发阈值**: 实测 > 60h 启动评估, > 72h 强制终止 Spike

**T4 产出消费**: T5 (AD3 回填) + T6 (M0 Report 引用)

### T4 完成标记 (2026-04-15)

- [x] **T4.done** — Spike 已完成
- **实际工时**: ~4.5h (原估 52h, 节省 47.5h / 91%)
- **裁决推荐**: `recommendation: option-c-extension-only` (Option C Extension-only tool pack)
- **Spike Report (主引用)**: [`../aria-2.0-m0-spike-hermes/spike-report.md`](../aria-2.0-m0-spike-hermes/spike-report.md)
- **Spike 代码路径**: [`aria-orchestrator/spikes/hermes-route/`](../../../aria-orchestrator/spikes/hermes-route/)
  - `option-c-poc/` — POC 源码 (286 LoC 业务 + 176 LoC 测试, 18/18 tests pass)
  - `license-matrix.json` / `license-scan-report.md` — 477 packages 扫描
  - `rebase-log.md` — upstream velocity 实测 (1931 commits/月)
  - `upstream-structure.md` — hermes v0.9.0 源码结构分析
  - `meta-knowledge-v0.1.md` — 元知识 prompt + tiktoken 实测
- **对 PRD v2.0 AD3 的影响**: PRD 原假设 "v0.7 不支持扩展 API, fork 是唯一路径" 被 3 条独立数据证伪, 需要 `prd_patch_pr` 反转 AD3
- **合规性 flag (spike-report.md §6)**: 需要产品负责人显式接受 2 项缩减 (ST2.1/2.2 rebase 实操跳过 + ST3 自研原型跳过)
- **下一步**: T5 (AD 收敛, T5.4 AD3 回填) + T6 (M0 Report 撰写 + `m0-handoff.yaml` 填写)

---

## T5 — AD1-AD12 收敛 (8h)

- [x] **T5.1** AD 索引草表 (0.5h, Day 1 前置) — 2026-04-15 完成
  - `aria-orchestrator/docs/architecture-decisions.md` 已含 AD1-12 + AD-M0-1~7 完整标号 + 标题 + 一行决策
  - 命名与 PRD v2.0 §架构决策 table 完全一致, 无需产品负责人二次锁定
- [x] **T5.2** 每项 AD 完整撰写 (6h) — 2026-04-15 完成
  - `aria-orchestrator/docs/architecture-decisions.md` v0.2
  - AD1/AD2/AD4-AD12 全量填充 (每项含: 决策 / 背景 / Alternatives Considered / 选型理由 / 风险 / 回滚路径)
  - AD3 由 T5.4 先行回填 (2026-04-15), 主引用 `spike-report.md`
  - R7 (Nomad meta 64KB) 已写入 AD4 §风险 #2, 作为 M1 Layer 1→2 协议硬约定 (meta 只传 ISSUE_ID, prompt 走 bind mount 文件)
  - AD-M0-1 ~ AD-M0-7 (7 项治理决策) 完整撰写, 主引用 2026-04-14 Agent Team review log
  - 文档版本历史已更新到 v0.2
- [x] **T5.3** CLAUDE.md 修订草案 (1h, 不提交) — 2026-04-15 完成
  - `aria-orchestrator/docs/claude-md-revision-draft.md` 已创建
  - 8 处 diff 完整起草 (Diff 1-8), 严格遵守 AD11 硬约束 (不修改 6 条不可协商规则本体)
  - Diff 7 新增 "Aria 2.0 运行时" 章节草案 ≤ 50 行
  - 含 US-026 执行检查清单, 推迟到 US-026 正式提交
- [x] **T5.4** AD3 回填 (0.5h, T4.done 后) — 2026-04-15 完成
  - Spike Report 结论直接写入 AD3 段落, 含: 选型 / 量化数据 / 回滚路径
  - 产出: `aria-orchestrator/docs/architecture-decisions.md` (新建, AD3 完整填充 + 其余 AD 留 stub 待 T5.2 撰写)
  - AD3 决议: `option-c-extension-only` (Extension-only tool pack via hermes entry-point plugin API)
  - 含: 决策 / 背景 (3 条 PRD 原假设反证) / 3 alternatives (A fork / B 自研 / R8) / 选型理由 (8 维度对比表) / 5 风险项 + 缓解 / 3 级回滚路径 / PRD v2.0 反转建议 / 合规性 flag (需产品负责人接受 2 项缩减)
  - 主引用: `openspec/changes/aria-2.0-m0-spike-hermes/spike-report.md`

---

## T6 — M0 Report + Handoff + PRD Patch (7.5h)

- [ ] **T6.1** M0 Report 撰写 (3h)
  - `aria-orchestrator/docs/m0-report.md`
  - 含: 架构决策摘要 / Spike 结论 / 5 项假设验证结果 / 风险确认 / M1 精确路径
  - **R9 三态章节** (`received / pending / declined`)
  - 签字位 footer 统一表述
- [ ] **T6.2** `m0-handoff.yaml` 生成 (1h)
  - Schema v1.1 12 字段完整填写
  - 作为 M0 Report 机读附件
  - `image_sha256` 来自 T3.6, `glm_smoke_passed` 来自 T3.4, `spike_code_path` 来自 T4, `ad3_conclusion` 来自 T5.4
- [ ] **T6.3** PRD patch PR 起草 (1.5h, 仅在产品负责人 Go-with-revision 时触发)
  - 若产品负责人裁决含局部 PRD 修订 → 起草 `prd_patch_pr`
  - 记录 PR 号到 `m0-handoff.yaml.prd_patch_pr`
  - PR 必须 3 工作日内合并, 否则冻结 US-021 启动
- [ ] **T6.4** 产品负责人评审 (0.5h)
  - 提交 M0 Report 给 10CG Lab 产品负责人
  - 等待 Go/No-Go 签字
- [ ] **T6.5** T1 No-Go 处置 (条件性, 0.5h)
  - 若 T1 最终 No-Go → knowledge-manager 在 M0 Report 对 T2 涉及 GLM/luxeno 段落做 strikethrough
  - phase-c-integrator 在 pre_merge 检查点验证 strikethrough 已完成
- [ ] **T6.6** Handoff schema 校验 (0.5h)
  - audit-engine pre_merge 检查 `m0-handoff.yaml` schema 完整性
  - `prd_patch_pr` 缺失或空 → block US-020 关闭
  - `r9_status == pending` 且无 `r9_signoff` → block
- [ ] **T6.7** 缓冲 (0.5h)

---

## Buffer (10h)

全局备用, 由产品负责人审批拨付到超时 task:
- T3 超 16h → 最多 +5h
- T4 超 60h → 最多 +5h (T4 硬终止 72h, buffer 不可超)
- T6 超 8.5h → 最多 +1.5h

## 收敛后状态

| 状态 | 动作 |
|---|---|
| Go (AD3 fork) | US-021 task-planner 启动, 继承 Spike fork 路径, 进入 M1 MVP |
| Go (AD3 自研) | US-022 重新规划 Layer 1 实现路径, M1 照常启动 (US-021 不变) |
| Go (双 acceptable, 默认 fork) | 同 Go (fork) |
| No-Go | R8 退出策略: CLI-only 降级模式; PRD 整体重写启动 |

## 关联文档

- [proposal.md](./proposal.md)
- [US-020](../../../docs/requirements/user-stories/US-020.md)
- [Spike Spec](../aria-2.0-m0-spike-hermes/)
- [Agent Team review log](../../../.aria/decisions/2026-04-14-us020-agent-team-review.md)
