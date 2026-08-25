---
checkpoint: post_spec
round: 3
role: tech-lead
verdict: REVISE
scope_ok: true
counts: 3C/10M/4m
combined_verdict: REVISE
per_spec:
  a1-entry-claim-duplicate-work-guard: {round: 3, verdict: REVISE, counts: "1C/6M/2m", scope_ok: true}
  linked-issue-field-availability:     {round: 1, verdict: REVISE, counts: "1C/2M/1m", scope_ok: true}
  sibling-spec-probe:                  {round: 1, verdict: REVISE, counts: "1C/2M/1m", scope_ok: true}
---

# post_spec R3 — a1-entry rework v3 (combined) — tech-lead

**轮次**: 母 Spec `a1-entry-claim-duplicate-work-guard` 第 **3** 轮 (convergence 续审) / 两份子 Spec
`linked-issue-field-availability` 与 `sibling-spec-probe` 第 **1** 轮 (新文件, 从未进闸门)。
本席镜头 = **架构与跨 Spec 一致性**。每份 Spec 的 verdict 与 counts 分开给, 末尾给 combined。

## 审计对象与实读环境

```
$ git log --oneline -1
027a50f docs(spec): a1-entry rework v3 — owner 方向 b 落版 (...)
$ git status --short
 M aria-orchestrator                     # 三份 proposal.md 均干净, 已提交于 027a50f
$ git -C aria log --oneline -1 origin/master
d50f9c3 test(secret-guard): SC-8 性能闸 相对+50% → 绝对 ms/call 双腿
$ git cat-file -t cc1bdef
commit                                   # 探针 Spec 的钉桩 SHA 可达 ✅
```

实读一律 `git -C aria show d50f9c3:<path> | sed -n '<N>p'`; 主仓语料一律工作树 (= `027a50f`)。

---

## 一 · R2 findings 逐条判 (母 Spec 第 3 轮; 迁走项去子 Spec 判「是否真被接住」)

| R2 簇 | 归属 | 本轮判定 | 依据 |
|---|---|---|---|
| **C-A** 抽取规则 defer ⇒ check 恒红 | 迁 field | **closed** | field §3 E0–E6 七条钉到字符级 + 四态表; D1 |
| **C-B** 连坐 release | 留母 | **⛔ still-open (换臂复发)** | 见 **TL-C1** —— §5.1 只修「探索性放弃」臂, D.2b 臂原样 |
| **C-C** carry-id 断链 | 留母 | **closed** | §2.1b + SC-23 + Impact 三行 SKILL.md + session-handoff.md 行 |
| M-1 同 issue 谓词未定义 | 迁 probe | **closed (但实现无归属)** | probe §3 层 0/1/1.5/2/3 + SC-7~SC-11; **实现归属见 TL-P1** |
| M-2 跨项目 SOT 模板未入 Impact | 迁 field | **closed** | field §1 + Impact `proposal-minimal.md` 行 |
| M-3 键缺席 vs 空列表 | 留母 | **closed** | §2.5 第 2 点 + §2.4b 四态表第 1 行 + §6 缺口表首行 |
| M-4 `except → []` 零证据当正证据 | 留母 | **closed (代码面)** / **⚠️ 引入 TL-M3** | §2.4b + SC-25; 但 Phase B 消费面未处置且 §非目标否认 |
| M-5 默认分支取法 + 盲区声明 | 迁 probe | **closed** | probe §4 步骤 1–4 (fail-closed) + §10 B1–B6 |
| M-6 rule6_note audit-engine 档 / SC-9 substitute | 拆两边 | **closed** | 母 §rule6_note 6 档表 + 新 substitute; probe rule6_note 三条逐条 |
| M-7 heartbeat 无视 opt-out | 留母 | **closed (门控)** / **⚠️ 见 TL-M1** | §2.2 (ii) 门控段 + SC-28; 但挂载点覆盖面另有结构缺口 |
| M-8 (iii) 消费者 / 两级顺序 | 留母 | **closed (前提消失)** | (iii) 已撤销; §2.3 残余风险改双向 |
| M-9 `_TERMINAL` 订正未同步 SC | 留母 | **closed** | SC-8 场景列删 `yielded` + §2.4a 独立键 + SC-24 |
| M-10 check 无实现宿主 | 迁 field | **closed** / **⚠️ 引入 TL-F1** | field §4 宿主 = plugin 分发面; 白名单与该宿主冲突 |
| M-11 双落点零 SC | 留母 | **closed** | SC-22 (正则 + 非围栏 + 四字面量 + 幂等谓词) |
| M-12 `--heartbeat-only` track 来源 | 留母 | **partial** | 三级回落已定; 但 ① 的先例被误引, 见 **TL-M6** |
| M-13 自述不实 | 留母 | **closed** | FIX-01…19 逐条对账表, 全文无「已全量吸收」句 |
| M-14 Impact 漏两 SOT | 留母 | **closed** | `session-handoff.md` + `coordination-ref-schema.md` 两行 |
| M-15 无人值守 | 留母 | **closed** | `unattended` config key + SC-26 + AD10 句 |
| M-16 SC 类别 / 捆绑 | 留母 | **closed** | SC-8/10 拆单断言; SC-9/SC-14 类别订正 |
| M-17 五子项 | 拆两边 | **closed** | 母收 1/2/3/5 (§2.1a / D16 / §2.3 分档 / DEFAULTS.json 行), probe 收 4 (§7 stdout 契约) |

**迁出项无一「两边都落空」**——每条都在子 Spec 找到实体条款。**但迁出把两类东西留在了缝里**: ①
E0–E6 的**实现归属** (TL-P1); ② §6 缺口表在迁出时丢掉的「部分」限定词 (TL-M5)。

### 主控点名的三条已修接缝 — 本席复核

| # | 修法 | 复核 |
|---|---|---|
| ① SC-19(b) → 新起 SC-29 | 母 SC-29 (`:570`) + probe `:69` 声明「不迁入」 | ✅ **修得对**。两侧结论一致无孤儿; SC-29 自陈 baseline 绿并给了负控 (删 `collision.py:278-279`)。实读该两行逐字 `if c.track_id == own_track_id:` / `continue  # same-name collision — reconcile's job, not ours` ⇒ 负控可构造, 坏实现 (把 `--include-terminal` 实现成跳过全部 `continue`) 在该条必红 |
| ② 四态 → 三态 ⇒ 逐格映射 | probe §3 `:107-116` 五行映射表 | ⚠️ **修了 §3 没修 §7** —— 见 **TL-P2** (`"bad_token"` 泄漏出 `own_layer` 枚举) |
| ③ 探针层 0 改为逐字采纳姊妹 E0 | probe `:87-89` | ⚠️ **条款修对了, SC 没跟上** —— 见 **TL-P3** (SC-18 三臂无一验谓词 2) |

---

## 二 · 母 Spec `a1-entry-claim-duplicate-work-guard` (R3) — 本轮新 findings

### 🔴 TL-C1 (Critical · architecture) — **C-B 未闭: 连坐 release 在 D.2b 臂原样存在**

**定位**: §5.1 表第 1 行 (`:399`) ↔ §5.2 表第 4 行 (`:418`) ↔ §5.2 表第 5 行 (`:419`) ↔ SC-27 (`:568`)

**证据 (实跑)**:
```
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py | sed -n '377,432p'
def release_claim_by_track(...)
    """... If several active claims match (same
    container re-claimed a track across sessions — the NORMAL case ...),
    **ALL matching active claims are released** (review I1: ...)"""
    matches = [ rec for rec in read_result.claims
        if rec.container == resolved.container_id
        and rec.track_id == norm
        and rec.status == "active" ]
```

**论证** (只有把 §5.1 与 §5.2 并排读才看得见):

1. §5.1 定 **issue 派生形** 的语义单元 = **(container, issue)**, 且 §5 首段 `:391` 自陈「同一容器在
   同一 issue 下试三个方向时, 三个方向派生的是**同一个** track_id」;
2. §5.2 第 4 行 (`:418`) 规定「A.1 成功并走完循环 ⇒ D.2b 的 `release_claim_by_track` 能匹配到 A.1
   **那条** claim」——**单数**。而按 1., 该 `(container, 归一 track_id)` 下是**全部方向**的 claim;
3. 实读证明 `release_claim_by_track` 释放 **ALL matching** ⇒ **方向 1 走完循环到 D.2b, 会把仍在做的
   方向 2/3 一并释放** —— 与 §5.1 第 1 行「换一个方向不改变『本容器在做这个 issue』这个事实」直接相反;
4. §5.2 第 5 行 (`:419`)「D.2b 对偶」逐条列了**不经过** D.2b 的三条路径, 恰好证明「多方向中的一个走完
   循环」这一形态**从未被考虑**;
5. **SC-27 结构性抓不到**: 它只有 (A)「放弃一个方向」/ (B)「放弃整个 issue」两臂, 没有「一个方向走完
   循环、其余仍在」这一臂 ⇒ 照本 Spec 实现并跑 SC-27 全绿, 而 C-B 原样存在。

这是 memory `fix-the-class`: 修了实例 (显式 release 臂), 没问「这形状还有几个兄弟位置」。

**处方 (字符级)**:
- §5.2 表第 4 行拆两档, 逐字加: 「**issue 派生形**且该 issue 下**仍有其他 active 方向**时, D.2b **不得**
  调 `release_claim_by_track` —— 它按 `(container, 归一 track_id)` 释放**全部**匹配 (`claim_lifecycle.py:385-399`
  docstring 逐字 `ALL matching active claims are released`), 会连坐掉仍在做的方向」;
- 给出该档的替代动作 (二选一并写死): (a) D.2b 跳过 release, 由最后一个方向收尾时释放; (b) 引入
  per-direction 的 claim 粒度并**同步撤回** §5.1 的 (container, issue) 语义单元 (二者不可兼得);
- **SC-27 加第三臂 (C)**: 「issue 派生形轨, 同 issue 下 3 个方向各有 active claim, 方向 1 走完循环跑
  D.2b `release_gate.py --raw-track-id <A.1 原串>` ⇒ 方向 2/3 的 claim **仍 active**」。**必须与 (A)(B)
  分开列**——只有 (A)(B) 的测试在本形态上恒绿;
- 若技术上做不到, 按 §6 体例成文为已知限, **不得**留在「C-B 已解」的自述里 (Status 段 `:6` 现写「已解」)。

---

### 🟠 TL-M1 (Major · architecture) — heartbeat 的**唯一**挂载点在审计轮期间结构性缺席, 残余风险段把常态写成了例外

**定位**: §2.2 (ii) `:205-210` / §2.3 残余风险段 `:270` / §6 缺口表 (`:423-431`, 缺该行)

**证据 (实跑)**:
```
$ git -C aria show d50f9c3:skills/audit-engine/references/execution-modes.md | sed -n '84,125p'
## Convergence 模式
Round N:
  1. 调用 agent-team-audit 单轮引擎
  2. 汇总引擎处理
  3. 收敛判定
  4. 路由
## Challenge 模式
Round N (一个完整周期):
  Step 1: 讨论组 spawn → discussion_output
  ...
```
⇒ **两个模式块的轮内步骤里都没有任何 `/state-scanner` 调用**。姊妹探针 Spec §5(e) 从另一路径独立
实读同一事实 (`remote_refresh` 缓存唯一写入点在 `scan.py:312` = Phase 0.5 `/state-scanner` 入口,
「audit-engine 的轮间**没有任何机制保证跑过 `/state-scanner`**」)。

**论证**: §2.2 (ii) 把 heartbeat 的**全部**触发面放在 `/state-scanner` 入口。而本 Spec 保护的事故窗
(§2.2 首段自陈 **48–72h**) 的绝大部分, 正是 A.1 认领之后的多轮审计期 —— 那段时间里 `/state-scanner`
**结构上不会被调用**。(iii) 已撤销 ⇒ `STALE_TTL` 维持 1800 (30min)。合起来: A.1 claim 在进入审计轮
后 30 分钟即 takeover-eligible, 且**没有任何机制**能刷新它。
§2.3 现在的措辞是「编排层**漏跑一次** (>30min) 即被标 takeover-eligible」——「漏跑一次」把**常态**
写成了**例外**, 读者会以为这是操作失误而非结构缺口。这是 memory `feedback_completion_signals_vs_runtime_invocation`
的同形: 「已落版的一段编排契约」≠「在需要它的那个阶段真会被调用」。

**处方 (字符级)**: §2.3 残余风险段「信号 A」条目末尾逐字追加 ——
> **⚠️ 且该窗口在审计轮期间是常态而非例外**: 实读 `skills/audit-engine/references/execution-modes.md`
> 的 Convergence `Round N:` (`:88` 起) 与 Challenge `Round N (一个完整周期):` (`:117` 起) 两块,
> **轮内步骤均不调用 `/state-scanner`** ⇒ A.1 认领后进入多轮审计时 heartbeat **零触发**, 30min 后必然
> takeover-eligible。本 Spec **不覆盖**该窗口。

并在 §6 缺口表新增一行: `A.1 认领后至下次 /state-scanner 之间 (典型: 多轮审计期) | ≥30min, 无界 | 无`。

---

### 🟠 TL-M2 (Major · architecture) — `--heartbeat-only` 可能把 **enabled** 的 `coordination-gate-invocation` check 变成恒绿

**定位**: Impact 表 `phase1_gate.py` 第二处变更行 (`:605`) —— 该行逐字「**复用其 identity/fetch/push 管道**」

**证据 (实跑)**:
```
$ sed -n '221,241p' .aria/state-checks.yaml
  - name: "coordination-gate-invocation"
    description: |
      ... 生产 telemetry 分区 (.aria/coordination-telemetry.jsonl) 必须含 ≥1 条 **14 天内** 的
      source=production 记录 —— 证明 run_gate() 近期真经 CLI 生产入口被调 (非死代码 / 非陈旧一次性记录)。
    severity: warning
    enabled: true
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | grep -n '_source=_PRODUCTION_SOURCE\|ONE production call site'
1212:    # This is the ONE production call site — it invokes the PRIVATE _gated with
1222:        _source=_PRODUCTION_SOURCE,
```

**论证**: `_main()` 是**唯一**能写生产 telemetry 分区的调用点 (`:1212-1222`)。本 Spec 把
`--heartbeat-only` 定义为「同一 CLI 文件下的两个独立模式」, 入口同样是 `_main()`, 并要求「复用既有
identity/fetch/push 管道」——**但全文没有一句划定 telemetry 边界**。两种实现都符合本 Spec 字面:
- (a) `--heartbeat-only` 在 `_gated(...)` **之前**分支 ⇒ 不写生产 telemetry ⇒ check 语义不变;
- (b) 走同一个 `_gated(_source="production")` 包装 (「复用管道」的自然读法) ⇒ **每次 `/state-scanner`
  都写一条生产记录** ⇒ 该 check 从此**恒绿**, 无论真正的 A.1 / B-entry acquire 闸门是否还被调用。

(b) 恰好摧毁该 check 的**唯一存在理由**(description 逐字:「证明 run_gate() 近期真经 CLI 生产入口被调 —
非死代码」)。这是 memory `feedback_false_green_dual_is_permanent_red` + `no-self-exempt-gates` 的交点:
一个 enabled 的闸门被一次 Spec 变更**静默抽空**, 而它连 Impact 表都没进。

**处方 (字符级)**:
- Impact 表 `phase1_gate.py` 第二处变更行末逐字追加: 「**⛔ `--heartbeat-only` 不得进入
  `_gated(_source=_PRODUCTION_SOURCE)` 路径** (`scripts/phase1_gate.py:1215-1222`) —— 它不是 acquire
  闸门的调用, 写生产 telemetry 会把 `.aria/state-checks.yaml:221` 的 `coordination-gate-invocation`
  变成恒绿。分支须在 `:1215` 的 `_gated` 调用之前」;
- Impact 表新增一行 `.aria/state-checks.yaml` (只读依赖, 说明为何不改但必须核);
- **新增一条 SC (负控)**: 「跑 `--heartbeat-only` N 次后, `.aria/coordination-telemetry.jsonl` 的
  `source=production` 条数**不变**」——把 (b) 判红。

---

### 🟠 TL-M3 (Major · consistency) — §非目标「Phase B 输出逐字节不变」与 R2/M-4 的修复自相矛盾

**定位**: §非目标 `:581` vs 「本轮引入的新表面」#6 (`:692`) / 「本轮未做」#5 (`:707`)

**实读 `:581` 逐字**: 「**不动** Phase B 入口现有认领 —— `include_terminal` 默认 `False` 保既有语义
**逐字节不变**」。

**论证**: R2/M-4 的修复 (§2.4b `:314`) 改的是 `scripts/phase1_gate.py:1236-1238` 的 `except` 分支,
它**不受 `--include-terminal` 门控**, 对**所有**调用者生效。Phase B 两个入口都会传 `--linked-issue`
(实读 `phase-b-developer/SKILL.md:93` 的 `[--linked-issue "<repo>#<n>"]`) ⇒ 异常路径上 Phase B 会
收到 `linked_issue_overlap == null` + 新键 `linked_issue_overlap_error`。本 Spec 自己在新表面 #6 逐字
承认「**Phase B 的消费面也会看到 `null`**」。
⇒ §非目标那句是一条**未加限定的假断言**。一个只读 §非目标的实现者 (这正是它的用途) 会认为 Phase B
零处置; 而两处自陈埋在文末 700 行处。这是 memory `fixes-contradict`: 逐条看都对, A 违反 B 的隐含前提。

**处方 (字符级)**: `:581` 该条改为 ——
「**不动** Phase B 入口现有认领 —— `include_terminal` 默认 `False` 保 acquire 语义与 `unknown_schema_claims`
键的**输出逐字节不变**; **⚠️ 例外: R2/M-4 对 `:1236-1238` `except` 分支的修复不受该 flag 门控, Phase B
的异常路径同样会收到 `linked_issue_overlap == null` + `linked_issue_overlap_error`, 其消费面处置本 Spec
未定 (见新表面 #6 / 未做 #5)**」。

---

### 🟠 TL-M4 (Major · architecture) — §5.1 的二分谓词自称「可机械判定」, 但无判定式且存在反例

**定位**: §5.1 `:402` 逐字「这是一个**可机械判定**的属性 (看串里有没有 slug 段), 不依赖『这条轨有没有
关联 issue』这种需要外部上下文的判断」; 同句在 SC-1 (`:520`) / SC-15 (`:544`) / D12 (`:462`) 复用

**论证**: 两种形态归一后是同构的字符串:
- issue 派生形: `<basename>-<str(int(n))>-<uuid>` → 例 `aria-plugin-149-bfe8285d`
- 回落形: `<spec-slug>-<uuid>` → 例 `fix-issue-149-bfe8285d`

`derive_track_id` 只做 lower / `./_`→`-` / 截断 / sha256 回落 (F-28), **不保留段边界信息**。任何从串反推
形态的判定式 (最自然的是「倒数第二段是否全数字」) 在 slug 以数字段结尾时给出**错误**答案 —— 而
`fix-issue-149` / `us-023` / `m6-b4` 这类 slug 在本仓语料里是常见形态。Spec **没有给出任何判定式**。
若改为「形态在 A.1 派生时记入上下文」, 则它**恰好和被否决的谓词一样依赖外部上下文** ⇒ `:402` 声称的
那条优势消失, D12 的选型理由随之失效。
**三条 SC 结构性免疫**: SC-1 / SC-15 / SC-27 的夹具都**预先标注**了形态 (「track-id 为 issue 派生形的
轨」), 判定过程从未被执行 ⇒ 歧义不可能被测出 (memory `test-claims-vs-verifies`)。

**处方 (二选一, 必须落其一)**:
- (a) §5.1 逐字给出判定式 + 其误判集, 例: 「判定式 = `re.fullmatch(r'.+-[0-9]+-[0-9a-f]{8}', tid)` 命中
  即 issue 派生形。**已知误判**: slug 以纯数字段结尾的回落形 (如 `fix-issue-149`) 会被误判为 issue 派生
  形 ⇒ 该轨改名时不 release, 留下孤儿 claim。成文, 不假装覆盖」; 并给 SC-1 / SC-15 各加一条**歧义臂**
  夹具 (`fix-issue-149-<uuid>`);
- (b) 改为「形态由 A.1 派生时写入 carry-id 上下文, **不从串反推**」, 并**同步删除** `:402` 里
  「不依赖…外部上下文」这半句与 D12 依据栏的同款措辞 (否则理由与做法相反)。

---

### 🟠 TL-M5 (Major · cross-spec) — §6 缺口表在迁出时丢掉了「部分」这个限定词, 现文读作全覆盖

**定位**: §6 缺口表 `:429` (legacy 轨) 与 `:430` (竞品已归档)

**实读对比**:
- 旧文 (被本行自己引用): 「§4 探针**部分**覆盖」
- 新文 `:429`: 「**原写「§4 探针部分覆盖」—— §4 已迁出** ⇒ 现由 `sibling-spec-probe` 承担, **它 ship
  前该缺口无覆盖**」——「部分」二字随迁出消失, 剩下的对照是「ship 前无覆盖 / ship 后承担」。

**探针 Spec 自己的实测** (`sibling-spec-probe` §10, 独立实读): B3 「实测量级: `cc1bdef` 的 147 篇语料中
**133 篇落 `no_field` (90.5%)** —— 探针今天只对 **13** 篇可见」; B1 「非默认分支上的 in-flight 竞品
**结构性不可见**」; `:371` 逐字「探针实际覆盖的是…(b)『对方已 ship 并归档』, 以及 (a)『对方没走 claim』
中**其 Spec 已进默认分支**的那一部分」。

⇒ 探针 ship 之后, 母 Spec 这两行缺口仍是**部分覆盖** (需同时满足「已进被扫默认分支」**且**「proposal 有
合规「关联 Issue」字段」)。§6 表头自称「成文, 不假装覆盖」——现文正在假装。这是 memory
`narrow-owner-options` 的近亲: 迁出动作**悄悄放宽**了一条对自己不利的限定。

**处方 (字符级)**: `:429` / `:430` 两行的「覆盖它的机制」列改为 ——
「由 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md) **部分**承担 —— 仅覆盖竞品 Spec **已进被扫
默认分支** 且其 proposal **有合规「关联 Issue」字段** 者。探针 Spec §10 实测 147 篇语料 **133 篇 (90.5%)
无字段 ⇒ 探针不可见**; 非默认分支上的 in-flight 竞品 (其 B1) **结构性不可见**。⇒ 该缺口**即使探针 ship
后也只被部分覆盖**, 其余无覆盖」。

---

### 🟠 TL-M6 (Major · delegate-verify) — 对 R2-CR-M1 的承重反驳引错了先例: `check:` 是布尔谓词, 不携带 track_id

**定位**: §2.2 `:212` + 其下 `:218` 的「⚠️ 对 R2-CR-M1 反对意见的正面答复」

**实读**:
```
$ git -C aria show d50f9c3:skills/phase-b-developer/SKILL.md | sed -n '88p'
  check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)
```

**论证**: `:212` 逐字称「**这不是新机制, Phase B 已有逐字先例**: 实读 `phase-b-developer/SKILL.md:88`
… A.1 的 heartbeat 用**同一个** telemetry 通道取 track_id」。实读该行: 它的括注逐字是「**本 session 是否
已跑 phase1_gate**」——一个**布尔**谓词, 只回答「跑没跑过」, **不返回跑的是哪条 track**。
⇒ 「用同一个通道取 `track_id`」比该先例**多要一个字段**, 那个字段今天不存在。`:218` 的整段反驳建立在
「① 是编排层 telemetry, 与 Phase B 的 `check:` 谓词**同一机制**」之上 —— 前提不成立, 则 ① 塌缩成 ②
(handoff §6 carry-id) 或 ③ (跳过), 而 R2-CR-M1 的原意见 (「指定 track 来源等于回到依赖 AI 记性」) 对
② 是否成立需要重新论证 (memory `delegate-verify`: 引一行说「X 本就做这件事」须确认那行讲的就是这件事)。

**处方 (字符级)**: `:212` 逐字改为 ——
「**① 本 session 已跑过的 `phase1_gate` 的 `track_id` (编排层 telemetry)** —— **⚠️ 这是对既有先例的
扩展, 不是复用**: 实读 `skills/phase-b-developer/SKILL.md:88` 的 `check: phase1_gate telemetry / 编排层
记忆 (本 session 是否已跑 phase1_gate)` 是**布尔**谓词, **不携带 track_id**。本 Spec 要求编排层**额外
记录**本 session 传给 `phase1_gate` 的 `raw_track_id` —— 该字段今天不存在, 属本 Spec 新增面, 已列入
「本轮引入的新表面」」; 并在「新表面」段补该条; §2.2 `:218` 的反驳段同步把「同一机制」改为「同一层,
新增一个字段」。

---

### minor (母 Spec)

- **m1** — Impact 表 `branch-manager/SKILL.md` 行 (`:613`) 引 `:146` (标题行), 但 carry-id 占位串实读在
  **`:149`** (`phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory`)。指针指向块首而非落点,
  A.2 会多一次定位。建议写 `:146 起的块内 :149`。
- **m2** — Status 段 `:6` 逐字「C-B … 已解」。按 TL-C1, 该自述在 D.2b 臂上不成立; 建议改为「C-B 的显式
  release 臂已解, D.2b 臂待处置」——本 Spec 已对 M-13 立过「零容忍自述不实」的标准, 该句同标准。

**scope_ok**: ✅ true。变更面严格落在 A.1 入口认领 + track-id 契约 + heartbeat 编排层; §1/§4 已整节迁出且
Impact 表对应行标 ⛔; 无溢出。

**母 Spec verdict: REVISE (1C / 6M / 2m)**

---

## 三 · 子 Spec `linked-issue-field-availability` (R1)

### 🔴 TL-F1 (Critical · cross-decision) — `GRANDFATHERED` 硬编码在**随 plugin 分发**的脚本里 ⇒ 每个采用方注册后**首跑必 FAIL**

**定位**: D3 (`:382`, round-2 宿主改判) ↔ D6 (`:385`) ↔ §4 判据分割表第 4 行 (`:318`) ↔ check 骨架的
`fix:` 段 (`:303-304`) ↔ Impact `:441`

**论证** (单看每条决策都对, 只有把 D3 和 D6 并排读才看得见):

1. **D3** 把宿主从 `.aria/probes/` 改判到 **`aria/skills/state-scanner/scripts/linked_issue_field_probe.py`**,
   全部理由都是「随 aria-plugin **分发到每个采用方**」;
2. **D6 + Impact `:441`** 把 `GRANDFATHERED` 白名单**放进那个脚本**——内容是 **Aria 本仓**的 6 条具名路径
   `openspec/changes/aria-2.0-m{6,7}-*/proposal.md`;
3. **§4 表第 4 行**规定陈旧守卫**无条件**逐条断言, 子情形 **(a) 该路径当前不存在 ⇒ `FAIL allowlist 陈旧`
   + exit 1**;
4. ⇒ 任何采用方 (有 `openspec/changes/` 且注册了这条 check 的那些, 即本 Spec 的目标读者) 一跑, 那 6 条
   Aria 路径**在他们仓里当然不存在** ⇒ **exit 1, 每次都红**。而 `fix:` 段 (`:303-304`) 给他们的处置逐字是
   「删除 `skills/state-scanner/scripts/linked_issue_field_probe.py` 的 `GRANDFATHERED` 里那一行」——**让采用
   方去改 plugin 分发件**;
5. **SC-5(c) 把这个失败模式断言成了期望行为**: 「(c) `GRANDFATHERED` 含一条已不在作用域的 path ⇒ **exit 1**
   且文案含「allowlist 陈旧」」⇒ 一个在采用方仓恒红的实现在 SC-5 上**全绿**。

这是 memory `feedback_false_green_dual_is_permanent_red` (恒红 = 零信息) + `knob-granularity` (开关作用域
≠ 情形集: 白名单的情形集是「Aria 本仓的 6 份存量」, 而它被放进了一个作用域为「全部采用方」的载体)。
**它直接摧毁 D3 这条 round-2 改判的全部收益** —— 脚本到得了采用方, 但到了就是红的。

**处方 (字符级, 二选一)**:
- (a) **白名单出脚本**: `GRANDFATHERED` 改为**项目侧**数据 (随 check 注册传入, 例
  `command: python3 aria/.../linked_issue_field_probe.py . --grandfathered .aria/linked-issue-grandfathered.txt`;
  文件缺席 ⇒ 空白名单)。骨架同步改, Impact 新增该文件一行;
- (b) **白名单留脚本但加仓域守卫**: 逐字「陈旧守卫仅当**白名单条目所属仓 == 当前 project root**时启用;
  非本仓一律视为空白名单 (不 FAIL, 不静默豁免——`##SKIP##` 并在文案里说明)」;
- **两种都必须给 SC-5 加第五臂**: 「(e) 在一个**不含**那 6 条路径的仓 (采用方场景) 上跑 ⇒ **不得 FAIL**」。
  没有这一臂, (a)/(b) 都无法被证伪。

---

### 🟠 TL-F2 (Major · cross-spec) — E0–E6 只有一个实现宿主, 且它**不可被探针消费** (与 TL-P1 同一条, 两侧各记)

见下方 **TL-P1** 的完整论证。**本 Spec 侧的义务**: Impact 表现在只有
`linked_issue_field_probe.py` 一行 (`:441`), 该脚本是**项目根扫描的 CLI check** (入参 `argv[0]` = project
root, 输出 `OK`/`FAIL`/`##SKIP##`), **无可被外部 import 的 per-file 四态 API**, 且 D5 明确**只扫
`openspec/changes/`**。探针 Spec 要的是「对**远端 ref 上的任意 blob** (含 `archive/`) 求四态」——**本 Spec
今天不产出那个东西**, 而探针被本 Spec 的姊妹条款禁止自己写。

**处方**: Impact 表新增一行 ——
`aria/skills/state-scanner/lib/linked_issue_field.py` (**新建**) | **把 E0–E6 抽成纯函数**
`classify(text: str) -> tuple[str, str | None, int | None]` (verdict / token 串 / 行号), **不含 I/O、不含
作用域、不含白名单**; `linked_issue_field_probe.py` 与 `audit-engine/scripts/sibling_spec_probe.py`
**各自 import 同一份** | **消解与 `sibling-spec-probe` 的实现归属接缝**
—— 落 `lib/` 而非 `scripts/` 的理由与 D4 对 `normalize_linked_issue` 的处置**同款**且已被本 Spec 实测过
(§4 的「包父目录 + `from lib.collision import`」两写法对跑)。并给 SC 表加一条断言该纯函数可从 `lib` 导入。

---

### 🟠 TL-F3 (Major · fact-discipline · 由迁出造成) — D2 与 SC-1(c) 引的「真实语料实例」在审计基线上**不存在**

**定位**: §Why `:58` / D2 `:381` / SC-1 `:409` 末句

**实读 (审计基线 = `027a50f`, 工作树干净)**:
```
$ sed -n '88p' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
## What Changes
$ grep -rnE '^[ \t]*> ?> ?\*\*关联 Issue\*\*|^[ \t]+> \*\*关联 Issue\*\*' --include=proposal.md openspec/
openspec/changes/linked-issue-field-availability/proposal.md:301:        > **关联 Issue**: `<org>/<repo>#<n>`      # 多个用 ", " 分隔
```
⇒ 母 Spec `:88` 现在是 `## What Changes`; **母 Spec 全文已无任何 depth-2「关联 Issue」行** (它随旧 §1 迁出
一并消失)。全语料唯一的 depth-2/缩进形态实例, 是**本 Spec 自己 `fix:` 块内的示例** (`:301`)。

同时 §Why 的三组数在 HEAD 上实测为:
```
$ grep -rn '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l              # 39  (Spec 记 37)
$ grep -rnE '\*\*关联 Issue\*\*' --include=proposal.md openspec/ \
    | grep -vE ':[0-9]+:> \*\*关联 Issue\*\*' | cut -d: -f1 | sort | uniq -c
      2 .../a1-entry-claim-duplicate-work-guard/proposal.md      # Spec 记 3
     11 .../linked-issue-field-availability/proposal.md          # Spec 记 11 ✅
      7 .../sibling-spec-probe/proposal.md                       # Spec 记 4
```
本 Spec `:31` 的「数字是当日观测」声明**覆盖计数漂移**, 但**不覆盖一条具名的行号证据** —— D2 的依据栏
逐字写「母 Spec `:88` 是**真实的**假阳性实例」, SC-1 逐字写「(c) 的形状**在真实语料上有实例**: 母 Spec
`:88`」。二者在审计基线上均为假。这是 memory `feedback_cross_doc_claim_verify_at_target`: 文档 A 写「B 里
有 X」必去 B 实测 —— 而这里更尖锐: **母 Spec 的迁出动作亲手删掉了本 Spec 引以为据的那一行**。

**处方 (字符级)**:
- §Why `:55-59` 的示例改引一个**钉在 committed SHA 上**的实例 (与探针 Spec 同款做法, 它引
  `cc1bdef:...:75`, 本席实读确认**该引用有效**): 逐字改为「母 Spec 在 `cc1bdef` 上的 `:75` (旧 §1 迁出前)
  —— 复核命令 `git show cc1bdef:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | sed -n '75p'`。
  ⚠️ 该实例在 `027a50f` 之后已随迁出消失, **当前工作树语料上 depth-2 实例数 = 0**」;
- D2 依据栏与 SC-1 末句同步换锚点, 并逐字补「⇒ 谓词 1 现在是**前瞻性**约束 (合成夹具证伪), 不是当前
  语料的实证需求」——这不削弱谓词 1, 但把断言与事实对齐。

### minor (field Spec)

- **m1** — `Spec Level: 2` 但交付面横跨**三个仓** (`standards/` 跨项目 SOT + `aria/` 两处 + 主仓两处), 且
  本 Spec「新表面」#4 自陈「交付顺序与 gitlink bump 次序**未排**」。gitlink bump 次序正是 CLAUDE.md 多远程
  硬约束 1/2 治的那类 (Aria #165 三次复发)。建议在 §闸门状态待裁表加一项 O-4: 「三仓交付是否仍按 Level 2
  出 (不产 `tasks.md`) 由 owner 裁」——**不由本席判**, 只点名它没被问。

**scope_ok**: ✅ true。§1–§5 全部落在「字段可得性 / 抽取规则 / 机械校验」内; 非目标逐条排除了母 Spec 与
探针 Spec 的面; Impact 无溢出。

**field Spec verdict: REVISE (1C / 2M / 1m)**

---

## 四 · 子 Spec `sibling-spec-probe` (R1)

### 🔴 TL-P1 (Critical · cross-spec seam) — **E0–E6 的实现无归属**: 三条约束不可同时满足, 且「姊妹非阻塞」在实现层为假

**定位**: probe `:70` (依赖方向 3) / `:85` (上游 SOT 点名) / `:87-89` (层 0) / `:133` (⛔ 不得内含第二份) /
`:462` (非目标) / `:482` (Impact 不改 state-scanner) / `:484` (跨 skill 复用只定两项)
↔ field `:441` (Impact 唯一实现宿主) / field D5 (`:384`, 作用域只含 `changes/`)

**论证** (**只有跨两个文件读才看得见**):

三条约束逐字并列 ——
| # | 约束 | 出处 (逐字) |
|---|---|---|
| A | 层 0/层 1 的 SOT = 姊妹 E0–E6, **逐字采纳** | probe `:85` `:87` |
| B | **不得内含第二份抽取实现 (E0–E6 一条都不复制)** | probe `:133` / `:462` / P4 |
| C | **不改** `skills/state-scanner/**` | probe Impact `:482` |

而姊妹侧 E0–E6 的**唯一**实现宿主 (field Impact `:441`) 是
`aria/skills/state-scanner/scripts/linked_issue_field_probe.py` —— 一个**项目根扫描的 CLI check**:
入参 `argv[0]` = project root、遍历**本地工作树**的 `openspec/changes/`、输出 `OK`/`FAIL`/`##SKIP##` 文本
+ exit code、作用域由 **D5 明确排除 `archive/`**。它**不导出**任何 per-file 四态 API。

探针需要的是: 对**远端 ref 上的任意 blob** (`git show <refs/aria/sibling-probe/...>:openspec/archive/<slug>/proposal.md`)
求 `(verdict, token 串)`。**其全部 6 份立项证据都在 `archive/` 下** (probe §2 `:76` 逐字「实测三个同 key 簇
的 6 份 proposal 全部在 `archive/` 下, `changes/` 下为 0」)。

⇒ **A ∧ B ∧ C 不可同时满足**: 照 A 要 E0–E6, 照 B 不能自己写, 照 C 不能去姊妹那边加导出面。而
probe `:484` 的「跨 skill 复用形态待 A.2 定」只点名了 `normalize_linked_issue` 与
`resolve_enforced_remotes` **两项**, **E0–E6 不在其中** —— 即三份 Spec 里**没有任何一份**的 Impact 表承担
「让 E0–E6 可被 audit-engine 调用」。这正是母 Spec「本轮未做」#6 预警的形状:「若某条在两边都落空, 本轮的
『迁出』就变成了『丢弃』」。

**`:70` 的「非阻塞」断言在实现层为假**。probe `:134` 的辩护 (「姊妹未 ship 时四态里只有 `NO_FIELD`/`NO_TOKEN`
会出现 … 这就是今天的状态」) 说的是**数据**状态 (今天没有 canonical token), **不是代码状态** —— 分类器本身
仍必须存在才能产出 `NO_FIELD`/`NO_TOKEN`。两者是不同的依赖: **规则依赖**(定义) 确实非阻塞, **实现依赖**(代码)
是硬阻塞。辩护把二者混为一谈。

**处方 (字符级, 二选一, 两侧同批改)**:
- **(A) 抽纯函数** ⭐ 推荐: 姊妹 Spec 的 Impact 新增
  `aria/skills/state-scanner/lib/linked_issue_field.py` (新建) —— 纯函数
  `classify(text: str) -> tuple[str, str | None, int | None]`, 无 I/O / 无作用域 / 无白名单;
  `linked_issue_field_probe.py` 与 `sibling_spec_probe.py` **各自 import 同一份**。本 Spec 侧:
  `:482` Impact 行改为「**不改** `skills/state-scanner/**` 的既有文件; **依赖姊妹 Spec 新建的
  `lib/linked_issue_field.py`**」; `:484` 的跨 skill 复用清单**追加 E0–E6 一项**并写明「归一与抽取
  **一律 import 不复制**」; `:70` 依赖方向 3 改为「姊妹 Spec 的 **`lib/linked_issue_field.py` 是本 Spec 的
  阻塞前置** (E0–E6 的唯一实现); 其**字段写入侧规范与 check 注册**才是能力上限提升项, 非阻塞」;
- **(B) 显式阻塞**: 若不抽纯函数, `:70` 必须逐字改为「姊妹 Spec **是**本 Spec 的阻塞前置」, 并在两侧
  §闸门状态记 ship 顺序约束。
**不得**留在现状 —— 现状下 A.2 拆任务时第一条就无法派生。

---

### 🟠 TL-P2 (Major · contract) — `"bad_token"` 泄漏出 §7 的 `own_layer` / `hits[].layer` 枚举 (主控修法 ② 的漏传导)

**定位**: §3 分派表 `:111` 末列 ↔ §7 stdout 表 `:293`

**实读 (逐字)**:
```
$ grep -n 'bad_token' openspec/changes/sibling-spec-probe/proposal.md
111:| **`BAD_TOKEN`** | — | **层 1 与层 2 都跑, 取并集** | ... | `"bad_token"` |
$ sed -n '293p' openspec/changes/sibling-spec-probe/proposal.md
| `own_layer` | `str` | 本轨 proposal 走了哪一层: `"canonical"` \| `"wu_empty"` \| `"url_fallback"` \| `"no_token_no_url"` \| `"no_field"` |
```
⇒ §3 分派表要求 BAD_TOKEN 行产出 `layer == "bad_token"`, 而 §7 的枚举**只有 5 个值且不含它**。

**论证**: 这是主控为消解 SEAM-2 而给 §3 补的逐格映射**没有传导到 §7 输出契约**的直接结果
(memory `fixes-contradict`: 每条单独看都对, A 违反 B 的隐含前提)。两个独立实现者会得到**相反**结果
(memory `spec-underdetermination`): 照 §7 写 schema 的实现会拒绝 / 折叠该值, 照 §3 写的会发出枚举外的值。
**现有 SC 全部免疫**: SC-11 只断言 `wu_empty` vs `no_field` 可辨; SC-15 只断言「含表中全部必填键」+ 可
`json.loads`, 不校验取值域; §9 消费面按 `verdict` 分档、不看 `layer` ⇒ 不会发红。

**处方 (字符级)**: §7 `:293` 的 `own_layer` 取值域逐字改为
`"canonical" \| "wu_empty" \| "url_fallback" \| "bad_token" \| "no_token_no_url" \| "no_field"` (**六值**),
并在 §7 表下补一句「`hits[].layer` 取同一枚举」; **SC-11 加第三份夹具**: 一份 `BAD_TOKEN` (`` `10CG/a#1, TBD` ``)
⇒ 其 `layer` 必须逐字为 `"bad_token"`, 与 `"canonical"` / `"url_fallback"` 三者两两可辨。

---

### 🟠 TL-P3 (Major · verifiability) — 新采纳的 E0 谓词 2 (围栏排除) 在本 Spec 内**零 SC 覆盖**, 且 SC-18 臂标签已与 §3 层 0 不一致 (主控修法 ③ 的漏传导)

**定位**: §3 层 0 `:89` (三谓词) ↔ SC-18 `:454` (三臂)

**实读**: SC-18 三臂逐字 = 「(a) 行首 `> ` 规则 (**本 Spec 采用**); (b) 宽松「行内任意位置」规则;
(c) 行首 + 「只在首条 `---` 之前找」」。而 `:89` 起「本 Spec 采用」的是**三条**谓词 (行首锚定 + **围栏
排除** + 取首条)。

**论证**:
1. **标签失真**: arm (a) 现在描述的是**采纳前**的规则。`:101` 自陈「谓词 2 是本 Spec 采纳姊妹的, **不是
   本席实测的**: 本席三臂里没有围栏臂」——三臂表是修法 ③ **之前**的产物, 没跟着改;
2. **更实的问题**: 姊妹侧已实测「加与不加围栏谓词在真实语料上**判定差异 = 0**」(`:101` 逐字, 两次逐份
   对跑 147 / 149 份均为 0) ⇒ **SC-18 三臂在「实现了谓词 2」与「漏实现谓词 2」两种实现上取值完全相同**。
   一个漏掉围栏状态机的探针在 SC-18 全绿 ⇒ 本 Spec 对自己**刚采纳的那条谓词**没有任何护栏
   (memory `check-runs-at-baseline-first` / `adversarial-fixture`: 要验的是**拒绝能力**, 不是当前取值);
3. 姊妹侧 SC-1(b)(d) 确实覆盖围栏, 但宿主是 `state-scanner` 的测试面, **不是** `audit-engine/tests/`
   —— 探针自己的层 0 实现不受它约束 (TL-P1 若按 (A) 抽纯函数解, 该覆盖才传导过来; 若按 (B) 解则不传导)。

**处方 (字符级)**:
- SC-18 arm (a) 的标签逐字改为「(a) **行首锚定 + 围栏排除 + 取文档序第一条** 三谓词 (= §3 层 0, 本 Spec 采用)」;
- **加第四臂 (d)** (合成夹具, 不打真语料): 一份 proposal, 全文**无** depth-1 字段行, 但在一个 blockquote
  内的围栏块里含一行逐字 `> **关联 Issue**: \`other/repo#999\`` ⇒ 期望 `own_layer == "no_field"`,
  `own_keys == []`。**漏实现围栏状态机 (或围栏正则漏 `(?:> ?)?`) 的实现在该臂抽出 `other/repo#999` ⇒ 必红**;
- docstring 补一句「(d) 臂在真实语料上判定差异为 0, 故**必须**用合成夹具 —— 这是它存在的理由, 不是缺陷」。

### minor (probe Spec)

- **m1** — §4 步骤 1 (`:179-186`) 复用 `resolve_enforced_remotes`, 但实读该函数返回**二元组**:
  ```
  $ git -C aria show d50f9c3:skills/state-scanner/scripts/collectors/multi_remote.py | sed -n '255,269p'
  def resolve_enforced_remotes(configured, actual_remotes, read_only=()) -> tuple[list[str], list[str]]:
      """... Returns ``(enforced, no_matching)``: ...
      - ``no_matching``: configured names absent from ``actual_remotes`` — recorded as
        ``no_matching_remote`` observability, NEVER fetched as ghost fail legs."""
  ```
  本 Spec 只为 `enforced` 定义了处置 (`:186` 空集 ⇒ skipped), **`no_matching` 全文无归宿**, §7 的
  `remotes[]` 也没有对应字段 ⇒ 一个 `enforced_remotes` 里配了不存在 remote 的采用方, 该信号被静默丢弃
  (而上游 docstring 逐字要求它被记为 observability)。处方: §7 顶层加 `no_matching_remotes: list[str]`,
  §4 步骤 1 写明「非空 ⇒ 进 stdout, 不 fetch, 不降 `status`」, SC-14 加一臂。

**scope_ok**: ✅ true。§1–§10 全部落在探针面; 非目标逐条排除 claim/track-id 语义与抽取规则定义;
P11 的扩 scope 冲动已按 owner 缩 scope 裁定留痕上呈而未自行执行 (符合 Rule #10)。

**probe Spec verdict: REVISE (1C / 2M / 1m)**

---

## 五 · 跨三份的必答题 (主控点名)

**Q1 — 三份之间还有没有只有跨文件看才看得见的矛盾?**
有, **四条**, 均在上文:
1. **TL-P1 / TL-F2** (同一条, 两侧记): E0–E6 的**实现归属**掉进缝里 —— 探针禁止自写、姊妹不产出可 import
   的单元、双方 Impact 都不承担。**这就是主控要的「第四条接缝」, 且是本轮唯一的跨 Spec Critical。**
2. **TL-M5**: 母 §6 缺口表在迁出时丢掉「部分」限定词, 与探针 §10 自测的 90.5% 不可见率正面冲突。
3. **TL-F3**: 母 Spec 的迁出**亲手删掉了**姊妹 Spec D2/SC-1 引以为据的那一行 (`:88` depth-2 实例), 姊妹
   未在母 Spec 落盘后复核。
4. **TL-M1**: 探针 Spec §5(e) 实读出的事实 (audit-engine 轮间无 `/state-scanner`) **正好证伪**母 Spec §2.3
   对 heartbeat 覆盖窗的乐观措辞 —— 两侧各自都对, 没人把它们连起来。

**Q2 — 每条「迁往 X」的义务, X 那边真的接住了吗?**
**条款层面: 全部接住** (逐条对账见第一节表格, 无一落空)。**实现层面: 一条落空** —— E0–E6 (TL-P1)。
另有一条**在接住时被悄悄放宽**: §6 缺口表的覆盖度断言 (TL-M5)。

**Q3 — 母 Spec 声明两子 Spec「不是阻塞前置」, 这个断言在三份的条款下真的成立吗?**
- 母 ← field: ✅ **成立** (字段缺席 ⇒ `phase1_gate.py:1230` 整块门控 ⇒ 已定义的退化)。
  ⚠️ **但只覆盖「字段缺席」, 不覆盖「字段在场且非 canonical」** —— 后者是今天 100% 的存量写法
  (field §Why: 14/14 直喂归一得 `None`)。母 §2 要求 A.1 传 `--linked-issue "<org>/<repo>#<n>"`,
  SC-12 要求「spec 有『关联 Issue』但未传 ⇒ 判红」, 而**抽取规则整节已迁出** ⇒ 字段在场但值是 markdown
  链接形时, 母 Spec **没有任何规则**说怎么取那个实参, 实现者最可能照抄整串 ⇒ 把脏串喂进匹配面 (正是姊妹
  Spec `linked-issue-normalization` 刚治好的病)。**这不是「零输入退化」, 是未定义行为。**
  → **处方**: 母 §6 缺口表首行的触发条件由「token 为 `无` 或字段缺席」扩为「token 为 `无` / 字段缺席 /
  **字段在场但不满足 `linked-issue-field-availability` §3 的 E2 (冒号后首个非空白不是 code span)**」,
  第三种情形的处置逐字写「**同样省略 `--linked-issue`**, 不得照抄字段值」; SC-12 同步加该臂。
  (本条与 TL-M5 同族, 计入母 Spec TL-M5 的处方, 不另计数。)
- 母 ← probe: ✅ **成立** (母的正确性不消费探针输出)。
- probe ← field: ❌ **不成立** —— TL-P1。**母 Spec 只审了母↔子两个方向, 从未声明子↔子方向**, 而真正的
  阻塞恰在那一条上。三份的依赖方向声明集**不完整**。

**Q4 — 有没有条款落在接缝之间没人认领?**
有, 三处: (i) **E0–E6 实现** (TL-P1); (ii) **`linked_issue_overlap == null` 的 Phase B 消费面** (TL-M3 ——
母 Spec 自陈未处置, 两子 Spec 都不碰 `phase1_gate.py`, 无人认领); (iii) **`resolve_enforced_remotes` 的
`no_matching` 返回值** (probe m1)。

**Q5 — §2.1b 是否实质改动 Phase B/D 既有契约? 与 §非目标相容吗?**
**结论: 相容, 母 Spec 的边界划法成立** —— 但理由与它自己写的不同, 建议补强。
实读三处宿主:
```
$ git -C aria show d50f9c3:skills/phase-b-developer/SKILL.md | sed -n '86,93p'
B.0 - REQUIRE claim (...):
  precondition: 进入 B.1 前, 本 (container) 必须已有一条本 session 的 active claim
  check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)
  if_missing:
    - MUST 先跑 ...
      python3 ".../phase1_gate.py" \
        --raw-track-id "<本 cycle carry-id/Spec id>" --phase B --mode advisory \
$ git -C aria show d50f9c3:skills/phase-d-closer/SKILL.md | sed -n '55p'
- carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串 (归一在 CLI 内部, 两端一致)。
```
- **调用形态 / 参数集 / 判定语义**: 三处都不变 ✅;
- **`check:` 谓词是 per-session 布尔** ⇒ A.1 在 S1 认领、Phase B 在 S2 运行时, B.0 照旧 `if_missing` 重跑
  —— **与现状行为逐字节相同** ✅ (每 session 重认领本就是既有语义, `release_claim_by_track` docstring 逐字
  称之为 `the NORMAL case`);
- **真正被改的是「carry-id 的定义源」**: `phase-d-closer:55` 现在把 carry-id **定义为** 「Phase B-entry
  时传给 phase1_gate 的那一串」, §2.1b 把定义源前移到 A.1。这是**定义面**的改动, 不是**行为面**的改动;
  对未走 A.1 的 session, §2.1b 的「沿用 Spec id」分支保持旧行为 ✅。
⇒ 与 §非目标「不动 Phase B 入口现有认领」**不冲突**。
**但建议补强**: §2.1b 的 U-3 边界段现在只写「改取值口径不改闸门语义」, 论证偏薄。逐字补上面第 2 点
(「`phase-b-developer:88` 的 `check:` 是 per-session 布尔谓词, A.1 早于 B 认领不改变 B.0 的
`if_missing` 走向 —— 每 session 重认领是 `release_claim_by_track` docstring 逐字称的 `the NORMAL case`」),
和第 4 点 (`phase-d-closer:55` 是**定义源**前移而非行为改动) —— 这两条把「相容」从断言变成可核对的论证,
owner 在 R3 确认时才有据。**⚠️ 注意: §非目标的真正问题不在 carry-id, 在 TL-M3 的 Phase B 异常路径。**

---

## 六 · 经本轮实读确认成立的部分 (下轮免重复)

| 断言 | 复核命令与结果 |
|---|---|
| `collision.py:278-279` = `if c.track_id == own_track_id:` / `continue  # same-name collision…` | `sed -n '265,292p'` ✅ 逐字一致 |
| `release_claim_by_track` 释放 **ALL** 匹配 | docstring `:385-399` + `matches` 过滤 `:422-427` ✅ |
| `DEFAULTS.json` 的 `state_scanner` 段**无** `coordination` | `json.load` 得 8 键, `coordination present: False` ✅ (母 rule6_note substitute 的 baseline 必红成立) |
| `config-loader/SKILL.md:134`/`:140` = `state_scanner.coordination.enabled:` / `.mode:` | ✅ 逐字一致 |
| `DEFAULTS.json:124-128` `adaptive_rules.level_3 = "challenge"` | ✅ 逐字一致 (probe §8 双落点论证成立) |
| `audit-engine` 在 `d50f9c3` 上无 `scripts/` 无 `tests/` (8 文件) | `git ls-tree -r` ✅ |
| `execution-modes.md` `## Convergence 模式`=`:84` / `## Challenge 模式`=`:113`; 插入锚点行准确 | ✅ (probe §8 表可直接实施) |
| `resolve_enforced_remotes` 在 `multi_remote.py:255`, 二元组返回 | ✅ (probe 引 `:255-286` 准确) |
| probe 引 `cc1bdef:...:75` 的 depth-2 假阳性行 | `git show cc1bdef:… \| sed -n '75p'` ✅ **该引用有效** (钉 committed SHA 是对的做法) |
| 三份 Spec 的 dogfood 字段均过 E0 (`changes/` 下严谓词命中恰 3 份) | `grep -rlE '^> \*\*关联 Issue\*\*:' openspec/changes/` = 母/field/probe ✅ |
| 母 SC-29 的负控可构造且能判红坏实现 | 逻辑核: `if not own_linked_issue: return []` 是 `return` 不是 `continue`, 「跳过全部 continue」的坏实现会放出自身 claim ⇒ SC-29 红 ✅ |

## 七 · 本席**没能核实**的部分 (诚实声明)

1. **`phase1_gate.py` 的 7c / 7d 分支具体行号**未实读 (母 Spec「未做」#2 已声明) —— TL-M1 的论证不依赖它;
2. **`--heartbeat-only` 是否会走 `_gated(_source=production)`** —— 这是**尚未存在的代码**, 本席只能证明
   Spec 未划定该边界 (TL-M2), 无法证明实现会走哪条; 处方按 fail-CLOSED 写;
3. **`sys.path` 绑定 `lib` → `state-scanner/lib` 后 audit-engine 侧的模块解析冲突** —— 未实跑; TL-P1 的
   论证不依赖它 (只依赖三条约束的字面不可满足性);
4. **三份 Spec 的审计轨文件内容**本轮未逐字比对 (「搬运是否无损」不在本席镜头; 只核了 proposal 侧的指针
   链接与切分声明存在);
5. **field Spec §Why 的 `NO_FIELD 132 / NO_TOKEN 14 / OK 3` 规则原型判定**未复跑 (需实现 E0–E6 原型);
   只复跑了其 grep 口径 (结果见 TL-F3)。

---

## 八 · Combined verdict

| Spec | 轮次 | verdict | counts | scope_ok |
|---|---|---|---|---|
| `a1-entry-claim-duplicate-work-guard` | **R3** | **REVISE** | 1C / 6M / 2m | ✅ |
| `linked-issue-field-availability` | **R1** | **REVISE** | 1C / 2M / 1m | ✅ |
| `sibling-spec-probe` | **R1** | **REVISE** | 1C / 2M / 1m | ✅ |
| **三份合计 (combined)** | — | **REVISE** | **3C / 10M / 4m** | ✅ |

**一句话结论**: 三份 Spec 的**条款层迁出无一落空**、拆分本身是对的; 但 (i) 母 Spec 的 **C-B 只修了显式
release 臂, D.2b 臂上的连坐原样存在且 SC-27 结构性抓不到**; (ii) 两份子 Spec 之间存在一条**母 Spec 从未
声明过的方向** —— 探针对姊妹的 **E0–E6 实现依赖**, 而三份的 Impact 表**都不承担它**; (iii) 姊妹 Spec 把
Aria 本仓的白名单硬编码进了**随 plugin 分发**的脚本, 使 D3 改判的收益在采用方侧变成恒红。这三条都是
**只有跨文件读才看得见**的形状, 各自都能在 A.2 拆任务的第一条上卡住。
