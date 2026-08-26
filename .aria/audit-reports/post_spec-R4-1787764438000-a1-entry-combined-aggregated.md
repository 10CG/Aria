---
checkpoint: post_spec
round: 4
converged: false
overridden_by_user: false
incomplete: false
verdict: REVISE
---

# post_spec R4 (combined) — a1-entry rework v3 + 两份子 Spec

> **模式**: convergence · **席位 5/5, 全部为 R3 未用过的新镜头** (owner 2026-08-25 裁定方向 a「换新席」)
> **对账 SHA**: 席 1-3 审 `322f280`; 席 4-5 审 `322f280` + 主控审计中途的部分改动 (**主控流程失误, 见文末**), 现全部固定于 `ca9d362`
> **基线**: aria 子模块 `origin/master` = `d50f9c3`
>
> | 席 | 镜头 | verdict | counts |
> |---|---|---|---|
> | `code-explorer` | 跨文件追踪与事实核验 | REVISE (轻) | 0C/1M/1m |
> | `code-architect` | 实现蓝图可行性 | REVISE | 1C/6M/1m (S-1 经主控实读由 C 降 M) |
> | `silent-failure-hunter` | 静默失败/降级路径 | REVISE | 4C/12M/7m |
> | `pr-test-analyzer` | 验收断言覆盖质量 | REVISE | 4C/11M/6m |
> | `type-design-analyzer` | 类型与契约设计 | REVISE | 3C/13M/3m |

## 判定

**REVISE, 未收敛, 且方向为发散。** 去重后 **约 9 个 critical 簇**。

| 轮次 | critical 簇 | major 簇 |
|---|---|---|
| R2 | 3 | 17 |
| R3 | 3 (**内容全换**) | 19 |
| **R4** | **≈9 (内容再次全换)** | **≈20+** |

**critical 数首次上升, 且升幅接近 3 倍。** memory `feedback_stop_adding_rounds_when_major_count_flattens` 与
`feedback_audit_marginal_return_goes_negative` 两条判据**同时且明确命中**;
**两个独立席位 (silent-failure-hunter / pr-test-analyzer) 各自主动给出「已过拐点, 不要再加通用审计轮」的建议。**

### 🔑 本轮的形状: 9 条 critical 中 **8 条是 R3 清账动作自身引入或未真正修复的**

R3 的 3 条 critical (C-B 未闭 / allowlist×分发面 / E0–E6 无归属) **本身都已处理**, 但处理动作各自生出新的 critical。

## 去重后的 critical 簇 (9)

| # | 簇 | 席位 | 要点 (主控已逐条实读复核) |
|---|---|---|---|
| **K1** ⭐ | **`spec_slug`/`track_form` 活不过第一次 heartbeat** | type-design A-C1 | `heartbeat()` 在 `claim_lifecycle.py:244-256` **逐字段重建** `ClaimRecord` (显式列 11 个字段, 含 `linked_issue=existing.linked_issue`), **非** `dataclasses.replace` ⇒ 不同步改这段, 新字段每次心跳被抹掉。而本 Spec 的核心正是「每次 `/state-scanner` 都跑 heartbeat」⇒ **C1 的修复是空的, 且 C-C 回归**。`linked_issue` 先例实测需 **17 处透传 / 5 个文件**, 本 Spec Impact 只列 5 行 |
| **K2** ⭐ | **`track_form=None` 的处置自相矛盾, 且是 fail-OPEN** | type-design A-C2 · silent-failure | §5.1 写「退回 ALL matching」, §5.3 写「只释放三元组匹配」—— **同一条 legacy claim 两个相反答案** (实跑: `[s1,s2,s3]` vs `[s2]`)。且「退回 ALL matching」**正是 §5.3 自己逐字否决过的「接受连坐」**; 被命名为 fail-CLOSED 实为 **fail-OPEN**; **上线当天全部存量 claim 都走这条路径**; SC 区 grep `track_form` **零命中** |
| **K3** ⭐ | **SC-2 恒绿未解 —— 派生无代码宿主** | pr-test C-1 · architect C-1 | 实跑 `d50f9c3`: 臂(i) 绿, **主控新加的负控臂(ii) 也绿** —— 因为该负控断言的是「overlap 变空」而今天本就如此。夹具手写字符串, **全程不执行任何派生逻辑**。主控的订正只换了夹具出处措辞, **没换被测的量** (memory `redfix-change-quantity`), 且臂(ii) 仍留「compose」字样 |
| **K4** | **`spec_slug`/`track_form` 无写入路径** | pr-test C-3 | Impact 只给 `release_gate.py` 加 `--spec-slug`; `phase1_gate.py` 无对应 flag 且 Spec 明写「不碰 `run_gate`/`_run_gate_impl` 签名」⇒ **SC-27(C) 的 CLI 全链路夹具不可构造**; 降到 lib 层则测试绿而生产连坐原样存在。SC-1/SC-15 同被抽空 |
| **K5** | **`unknown_schema_claims` 没有失败态 —— R2/M-4 在它自己的修复里复发** | silent-failure #1 | 它与 `linked_issue_overlap` 共用 `phase1_gate.py:1231-1238` 的同一个 `try`, 而 `except` **只赋后者** ⇒ 异常时新键**静默缺席**, 四态表把「键缺席」定义为「未检测」, 消费方 `.get(k,0)` 读成「0 条 unknown」。memory `feedback_fix_recurs_in_its_own_fallback_path` |
| **K6** | **`abandoned` 有两种来源, Spec 只认一种** | silent-failure #2 | `gc.py:324` 逐字「stale active claims **rewritten to** `status='abandoned'`」, `ClaimRecord` **无 swept 标记** ⇒ GC 产物与自愿退出不可分; 而 §2.3 把 `abandoned` 一律渲染成「对方已显式退出 / 无冲突 / **接着做**」。**连带**: 「overlap 通道新鲜度免疫」只在 `SWEEP_TTL`(24h) 内成立, 而事故窗实测 48–72h |
| **K7** | **「skip + log」是空信号** | silent-failure #3 | `def log(` 全仓**零命中**; `phase1_gate.py:56` 的 logger **无 handler** (`basicConfig` 只在 `scan.py`) ⇒ 独立 subprocess 的 `logger.*` 全丢。叠加 R3/TL-M2 禁写 production 遥测 + SC-28 正向断言计数不增 ⇒ **「跑了但 skip」与「根本没挂载」在任何持久化产物里逐字节相同**, 连续三天静默 skip 无一处会红 |
| **K8** | **SOT 模板 placeholder 复现 NEW-01, 且触发条件比 `无` 更弱** | type-design B-C1 | 模板给的是 `` `{<org>/<repo>#<n>}` ``, 判 `BAD_TOKEN`; 而 **E6 只对 `无` 设门** ⇒ 未填写的 placeholder 被**逐字节**喂进 `--linked-issue`。实跑真实 `linked_issue_overlaps` 确认**两份无关 Spec 互相命中** —— NEW-01 原样复现, 且「什么都不做就中」比 `无` 更容易触发。探针侧同时中招 |
| **K9** | **SC-5(e) 在本仓自相矛盾, 且教出真 fail-open** | silent-failure #4 · type-design B-M3 | 主控写的「白名单文件不存在 ⇒ 正常判定 ⇒ **不得 exit 1**」在本仓必然为假 (文件今天不存在 + 作用域 9 份含 6 份 `NO_FIELD` ⇒ 必然 exit 1)。**按字面消解矛盾的实现 = `rm` 一条命令永久静默整条 enabled check** |

## 本轮实读**证实**的部分 (下轮免重复)

- **跨文档承接零丢弃** (code-explorer 逐条): 母 SC-13→字段 §5 · SC-16→探针 SC-1 · SC-17→探针 SC-2 · SC-18→探针 SC-3/4 · SC-19(a)(c)→探针 SC-5/6 · **SC-19(b)→母 SC-29**, 双向对齐;
- **约 95 条 `文件:行号` 断言零漂移** (三席各自抽样合计), 除已订正的 2 条 (伪引文 / `fetch_gate.py:23→:21`);
- **四态映射接缝双向闭合** —— type-design 判为「三份里质量最高的一块: 全函数、无歧义」;
- **SC-29 是最规范的 baseline-绿回归守卫** (pr-test: 「三条 finding 的处方就是照它抄」);
- **SC-22 锚点依据逐条实读复现**; **SC-7 的补强生效** (by-track 变体确不存在 ⇒ 第二臂 baseline 必红);
- Rule #6 判据表三件套**结构成立**, Phase B.1 前置断言未自判豁免 (符合 Rule #10)。

## 🔴 根因判断 (主控综合五席, 供 owner 裁方向用)

**9 条 critical 里有 5 条 (K1/K3/K4 + 部分 K2/K5) 指向同一处: 本机制的核心状态没有代码宿主。**

track-id 派生、`spec_slug`/`track_form` 的写入, 目前全部活在**两份 SKILL.md 的散文模板里**, 由 AI 照着拼字符串。§2.1a 当初「成文交付『拼接无代码宿主』这一半」是一次诚实的选择 (memory `knob-granularity`), 但它的代价现在完全显形了:

- 任何「代码类」SC 落到它上面都**结构性不可测** (SC-1/2/4/15/23/27(C) 全中);
- 任何新增的 claim 字段都**没有写入者**, 只能靠再写一段散文;
- 而 claim 记录的字段透传实测需要 **17 处 / 5 文件** (`linked_issue` 先例), 散文无法承载这种精度。

⇒ **这不是「再修一轮就能收敛」的缺陷集合, 而是一个结构性选择在反复产生同形缺陷。**

## 收敛判定 (convergence, `max_rounds=5`)

- 字面还剩 **R5 一轮**。
- 但 critical **3 → 3 → 9**, 且 **8/9 由上一轮修复动作引入**; 两个独立席位主动建议停止加轮。
- ⇒ **主控判定: 继续加通用审计轮的边际产出为负。** 按 Rule #10, **AI 不自行决定下一步**, 呈请 owner 裁。

## 主控处置建议 (非裁定 — **AI 不自行选**)

| 选项 | 内容 | 代价 / 风险 |
|---|---|---|
| **(a)** 继续 R5 | 先清 9 条 critical 再跑最后一轮 | 前三轮实证: 每轮清账都生出等量或更多同形 critical。**本轮 8/9 如此** |
| **(b)** 收缩交付面 | 两子 Spec 降级为 backlog issue, 母体只保留已收敛的部分 | 部分回撤方向 b; 但 K1/K3/K4 落在母体, 收缩救不了它们 |
| **(c)** 直接进 A.2 | 9 条 critical 转为 A.2 的承重任务 | 它们多为实现层归属问题, A.2 拆解时天然成形; 风险是把未收敛的 Spec 推进下一阶段 |
| **(d)** ⭐ **给派生/写入一个真正的代码宿主** (**本轮新识别, 此前未呈给 owner**) | 新增一个小模块 (compose track-id + 写 `spec_slug`/`track_form` + 供 CLI 调用), 并按 `linked_issue` 先例**逐条枚举 17 处透传点** | 推翻 §2.1a「本 Spec 不新增拼接函数」的既有取舍 (须 owner 复议); 但可**一次性**让 K1/K3/K4 与部分 K2/K5 变得可测 —— 是唯一一个针对根因而非症状的选项 |
| **(e)** owner 另裁 | | |

## ⚠️ 主控本轮的两项流程失误 (Rule #10 留痕)

1. **审计进行中就地改被审文件** —— 席 4/5 仍在审时主控落了 6 项修复 (`git diff` 3 files/+64/-5)。type-design 席明确告警「被审对象是移动靶」并逐条重锚定 (除 A-M7 外全部仍成立)。主控在 R3 时守过这条纪律, 本轮自己破了。**下轮必须固定 SHA 后再动手。**
2. **一次伪引文** —— 母 §5.3 曾把 `release_claim_by_track` 的 docstring 引成「(same session)」, 原文实为「same container re-claimed a track **across sessions** — the NORMAL case」。成因: 用 `sed | grep` 取证时 grep 过滤掉了中间两行, 主控把非相邻的两行**拼接**成一句。已订正 (订正后该处论证反而更强)。memory `delegate-verify` 已追记「grep 只能定位不能取证」。
