# 决策: DEC-20261022-001 — pi-durable 评估轨 Phase-1 结果 (双 PoC) 与底座策略

> **日期**: 2026-10-22 | **模式**: evaluation-result (DEC-20261018-002 评估轨的
> Phase-1 交付物; 该 DEC 预告「结论以未来新 DEC 落地」— 本 DEC 即其第一批)
> **参与者**: owner (simonfish) 批准试水 (2026-10-21 heavy / 2026-10-22 light) |
> AI 执行 | **状态**: Confirmed (证据与 Phase-1 结论; 换底座决策**仍开放**)

## 背景

DEC-20261018-002 立项 Layer 1 底座评估轨 (Hermes vs pi durable 等), 框架含六个评估
维度。本次试水交付其中两个维度的**一手实测证据**:

- **维度 1 (durable execution 语义与可靠性)**: 双 PoC 判据化实测
- **(新增维度) 部署形态**: heavy docker / light exec 双轨

## 证据摘要 (全部判据先行, 详见 pi-durable-poc/README.md)

### PoC-H (heavy-2, docker driver, job `pi-durable-poc`)

@earendil-works/pi-durable 1.3.0, SQLite WAL, NOMAD_ALLOC_DIR。判据 A1-A6 全绿:
mid-gather docker kill → 已提交 chunk `MEMO-HIT` 值逐字同、cycle 补完 (A3);
mid-wait kill → 续睡原 deadline、醒在 +14ms (A4); 重启不重复建 task (A5)。

### PoC-L (light-4, exec driver, 零 Docker, job `pi-durable-poc-light`)

同一 sentinel 逻辑。判据 L1-L5 全绿 (证据与 A3/A4 同形; L4 醒在 +2ms)。cgroup
115.9MB (含 cache) / 工作集 ~40MB, 1GiB 节点不构成约束。

### 锐边台账 (两 PoC 合计 11 条, 生产化输入)

库侧: `sleepUntil` 是 main 分支 API / phase fault 默认静默 (须自挂 onReport) /
chord unref 定时器 (host 须自持 keep-alive) / graceful stop 断 cycle /
memo at-least-once / storage 不可写容器可写层 (必须 NOMAD_ALLOC_DIR)。
平台侧: artifact getter 不支持 file:// / tar 解包 4096 文件上限 (Node 官方包须裁,
依赖树须剥 provider SDK) / .tgz 后缀必须真 gzip。

## 最终选择 (Phase-1 结论)

| 结论 | 内容 |
|------|------|
| **C1 底座现役不动** | Hermes orchestrator 主链 (Lark/cron/skills) 不迁移 — 评估轨剩余维度 (多 harness 适配 / Layer L 接驳 / 迁移共存) 未做, 不构成换底座证据 |
| **C2 pi-durable 清障通过 (底座层)** | 耐久语义 + 双部署形态实测成立; 按 DEC-20261018-001 的底座中立设计, **新增 ops-tier 动词可选 pi-durable 承载** (轻档先行: 收录告知/打标类) |
| **C3 部署形态矩阵** | heavy 默认 docker (bundle 复杂度由镜像层吸收); light 可 exec (代价 = bundle 工程化: 裁剪/压缩/文件数管理, 见锐边) — 按节点资源分场景, 不一刀切 |
| **C4 Hermes 止损先行** | 镜像构建 CI 化 (build-aria-orchestrator workflow, 独立交付) — 消灭 #232 式手工 docker commit; 这与底座选择正交 |

## 理由

1. 证据边界诚实: 双 PoC 验证的是**耐久执行模型与部署可行性**, 不是 cost-sentinel
   业务正确性, 更不是「pi-durable 能接管 Hermes 全部职责」;
2. C2 的支点不是 pi-durable 更强, 而是 DEC-001 底座中立契约使新动词的承载选择
   变成**可逆的局部决策**;
3. PoC-L 证明「无 Docker」可行但代价显性化 — 把隐性的镜像层复杂度换成了显性的
   bundle 工程量, 没有免费的轻。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| Experimental 库 (API 无 notice 变更) | 钉精确版本 (1.3.0); 锐边已固化在 README; 升级视为评估重启 |
| light exec 分发通道 (现本机 http.server) | 生产化候选 Forgejo generic + token 不落明文方案, 未解前 light 轨不扩 |
| PoC job 长跑漂移 (两个 job 持续运行) | 无害资源占用 (~40MB 工作集 ×2); 后续或转真实业务 (M6 cost snapshot 的 pi-durable 版) 或收编下线 |

## 后续 (Phase-2 候选, 未排期)

ops-tier 轻档动词试点 (issue-groomer 收录/打标) 承载于 pi-durable → 验证剩余维度
(多 harness 适配 / Layer L claim 接驳); M6 cost snapshot 的 pi-durable 重写为
可选对照面 (业务 = Zhipu 30d 阈值告警 + Luxeno 量下限 + 飞书卡片, 非 Forgejo 用量)。
