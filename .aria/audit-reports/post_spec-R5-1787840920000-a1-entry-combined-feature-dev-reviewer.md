---
checkpoint: post_spec
round: 5
role: feature-dev-code-reviewer
verdict: REVISE
scope_ok: true
counts: 1C/0M/0m
---

# post_spec R5 — a1-entry 三份 Spec — feature-dev:code-reviewer 席 (高置信度缺陷审查)

> **⚠️ 落盘说明**: 本席工具集仅 `Read/Grep/Glob` (无 `Bash`/`Write`), **无法自行写盘**, 回执以正文返回,
> 由**主控代为落盘**并逐条复核 (复核结论见各条下方)。本席以 checked-out 工作树核验 + `.git/refs/heads/master`
> 确认 HEAD = `b0c16ff`, 与任务基线一致。
> **本席自我限定**: 只做 K1–K9 闭合判定 + 新表面扫描, **未**重审 R4 的全部 major (超出本 pass 的 mandate)。

## 1. K1–K9 逐条闭合判定

| K | Verdict | 证据 |
|---|---|---|
| **K1** | **Closed** (文本层) | 新增「透传面逐条枚举」表明确点名 `heartbeat()` `:244-256` (item 3) + SC-30 往返验收。本席实读 `claim_lifecycle.py:244-256` 确认逐字段重建**确如所引**。**残余 (低severity)**: items 4/5 (`release_claim`/`release_claim_by_track`/`gc.py`) 只有泛指「逐一核」**无行号**, 且 SC-30 只断言穿越 **heartbeat** 不含 release |
| **K2** | **Still-open — 新 Critical** | 见 §2 |
| **K3** | **Closed (诚实降级, 正当)** | SC-1/2/4/15 代码类→行为类并显式声明「只能由 AB eval 覆盖、不冒充结构化测试」。原缺陷 (track-id 串被静默拼错) **在生产上仍可能发生**, 只在 Rule #6 benchmark 时才被抓、非持续 —— **但这一点被如实写出**, 且 (d) 选项留给 owner。**不是 paper-fix** |
| **K4** | **Closed** | `--spec-slug` 现在 acquire 侧 (`phase1_gate.py`, item 6) 与 release 侧 (`release_gate.py`, item 7) 都有 ⇒ SC-27(C) 夹具**可构造** |
| **K5** | **Closed** | `except` 现同时把两键赋 `None` + error token; SC-33; 四态表已随动 |
| **K6** | **Closed (诚实, 正当)** | 歧义的 `abandoned` 保守按「可能仍在制, 重新请裁」⇒ **完全关闭假阴性方向**, 代价是多几次请裁, 不冒「漏判重复劳动」的险。**真修复** |
| **K7** | **Closed** | `_source="heartbeat"` 分区 + SC-32; 本席核实它**不污染** `coordination_probe.py` 的 production 计数 (SC-28 第二臂正是断言这一点) |
| **K8** | **Closed** | E6 四态分派表 + SC-9; 跨 Spec 常量黑名单要求已正确穿到 `sibling-spec-probe` §3 层 1 + SC-19 |
| **K9** | **Closed (真修复, 非仅降级)** | SC-5(e) 拆 e1/e2 —— 消解了字面自相矛盾, 不再教出「`rm` 一下就静默」的 fail-open |

## 2. 新 Critical — K2 的修复自身内部矛盾, 且运维路径未定义 (confidence 92)

**定位**: 母 `proposal.md:450-457` (K2 的 2026-08-27 补丁) ↔ `:497` 与 `:722` (**未被该补丁触及**的邻近文本)。

- `:497` / `:722` 逐字: 「**未传 `--spec-slug` 时行为逐字节不变** (= 现状 ALL matching), 故 Phase B/D **既有调用零影响**」;
- K2 补丁 `:453-455` 无条件规定: 「`track_form is None` ⇒ **不释放, 报错退出**…要求操作者显式传 `--spec-slug` 或 `--force-legacy-release-all` 二选一」, 并自陈「**上线当天全部存量 claim 都走这条路径**」(两字段同批引入, 存量 claim 一个都没有);
- ⇒ 这是 **R4 已经抓到过一次的同一形状** (「同一条 legacy claim 两个相反答案」), 只不过这次是 **K2 补丁自己**对着未改的邻近文本**新造**的。

**后果**: ship 当天起, 任何走到 D.2b 的在制 cycle 都会从 `release_gate.py` 拿到**非零退出**, 除非调用方传 `--force-legacy-release-all`。
而 `phase-d-closer/SKILL.md` 的 Impact 行 (`:725`) **只加了 `--spec-slug`, 没规定任何重试/处置逻辑**。
AD10 规定 Layer 2 唯一人类参与点是 `S7_AWAITING_MERGE`, D.2b 是**无人值守**的 ⇒ **这是一道脚本级失败悬崖, 没有定义恢复路径**。

**另注**: 对 legacy claim 用 `--force-legacy-release-all` 会**释放全部匹配** —— 正是本 Spec 存在要修的连坐。
对**真正的** legacy claim 这可能是可接受的 (它根本没记 `spec_slug`, 无从区分), 但这意味着该修复**只保护新 claim, 不保护过渡窗口**,
而**这条残余缺口没有写进 §6 的残余缺口表**。

**处方**: (a) 调和 `:497`/`:722` 与 K2 的处置 —— 把「零影响」换成对 day-one legacy 失败模式的显式陈述;
(b) 在 `phase-d-closer/SKILL.md` 的 Impact 行里写明该错误的**无人值守处置**;
(c) 把该场景补进 §6 残余缺口表。

### 主控复核 (2026-08-27)

**本席判定成立, 三处逐字实读确认** (`:453` / `:497` / `:722`), §6 缺口表确无该行。**根因是主控 K2 补丁只改了 §5.1 的命名, 没同步 §5.3 的表格行与 Impact 行。**

**主控采纳并进一步收紧修法** (待落, R5 全席交齐后统一改): 本席指出「对真正的 legacy claim 无从区分, 报错无收益」——
主控同意, 并把判据拆成**两种情形**:
- `track_form is None` **且** `spec_slug is None` (**纯 legacy**, 存量 claim 的唯一形态): **释放全部 + 显式 warning** ——
  行为与今天**逐字节相同** ⇒ `:497`/`:722` 的「零影响」**变成真的**, day-one 悬崖消失, 且**不构成「默认连坐」**
  (那些 claim 根本不存在方向信息可保护);
- `track_form is None` **但 `spec_slug` 非空** (两字段同批引入 ⇒ 该组合**只可能来自手改/损坏**): **报错退出并点名**。
⇒ fail-closed 的守卫**保留但收窄到真正异常的那一格**, 兼顾 (a)(b)(c) 三条处方。

## 3. 新表面风险扫描

- `--force-legacy-release-all`: 见 §2 (Critical)。
- `_source="heartbeat"` 分区 + SC-32: 与 SC-28 第二臂交叉核对**一致**, 无发现。
- 常量黑名单 (探针 §3 层 1 + SC-19): 与 K8 正确交叉引用, 但两 Spec 间黑名单字面量的同步是**手工的**
  (「同源, 任一改动须同批改另一侧」) —— 属本集群已披露的接缝形态, confidence <80 不报 Critical。
- SC-30/31/33 / SC-9: 内部一致、红态清晰、baseline 正确, 无 ≥80 confidence 的问题。

## 4. A.2 实现者最可能卡住/做错的前三处

1. **D.2b 的 legacy-claim 错误路径** (§2) —— ship 当天就会变成真实的 CI/生产失败, 因为 SKILL.md 模板没给重试指令。
2. **`release_claim_by_track` 的过滤算法欠定**: Spec 点了三个交互条件 (container+track_id 匹配 / `spec_slug` 三元组过滤 / `track_form is None` 的 fail-closed 检查), 但**从未钉住求值顺序**, 也没说多条匹配项 `track_form` 取值**混合**时怎么办 —— 实现者只能自己发明。
3. **K1 透传表的 item 4/5** (`release_claim` / `release_claim_by_track` / `gc.py` 的重建) **没有任何 SC 强制验证** (SC-30 只覆盖 heartbeat) ⇒ 很可能被部分跳过, 且**漏了不会红**。
   > **主控补**: 实读这些重建点的确切行号 = `claim_lifecycle.py:146` (acquire) / `:244` (heartbeat) / `:346` (release_claim) / `:437` (release_claim_by_track) + `gc.py:396` (sweep 改写 abandoned), 共 **5 处**。透传表将逐点钉行号, SC-30 将扩为覆盖 heartbeat **与** release 两条路径。

## 收敛判断

对比 R4 (3C→9C, 且连续两轮「内容全换」): **本轮 9 个 critical 簇 8/9 已由可核验的文本级修复关闭**;
**1/9 (K2) 未闭**, 但它是 **K2 补丁自身新造的矛盾**, 不是原 R4 finding 的存活 —— 即**修复方向正确但不完整**。
除 K2 的延续外**未发现净新增 critical 簇**; 新表面扫描基本干净。

**critical 计数: 9 → 1** (相对 R4 大幅下降)。⇒ `feedback_stop_adding_rounds_when_major_count_flattens` 的判据
(数字持平/上升) **不再适用** —— 计数在**下降**。

**但 K2 未闭**, 按 Rule #10 这不是本席可以放行的。**建议: 在 K2 的 `:497`/`:722` 矛盾被调和、
且 `phase-d-closer/SKILL.md` 的 Impact 行写明无人值守重试行为之前, 不进 A.2。**
这是一处**小而定向的修复, 不是新一轮 rework** —— 大概率无需再跑一次完整五席审计。
