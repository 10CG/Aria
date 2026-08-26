---
checkpoint: post_spec
round: 4
role: silent-failure-hunter
lens: 静默失败 / 错误处置 / 降级路径
baseline_aria: d50f9c3
baseline_main: 322f280
verdict:
  a1-entry-claim-duplicate-work-guard: REVISE
  linked-issue-field-availability: REVISE
  sibling-spec-probe: REVISE
  combined: REVISE
scope_ok:
  a1-entry-claim-duplicate-work-guard: true
  linked-issue-field-availability: true
  sibling-spec-probe: true
  combined: true
counts:
  a1-entry-claim-duplicate-work-guard: {critical: 3, major: 5, minor: 3}
  linked-issue-field-availability: {critical: 1, major: 4, minor: 1}
  sibling-spec-probe: {critical: 0, major: 3, minor: 3}
  combined: {critical: 4, major: 12, minor: 7}
---

# post_spec R4 — 静默失败 / 降级路径专席 (三份联审)

**判据红线**: 「零证据不得当正证据」—— 读不到 / 取不到 / 抛异常, 一律不得渲染成「没有问题」。
本报告只审**规格所规定的失败行为**, 不改任何被审文件。所有 `文件:行号` 均已用
`git -C aria show d50f9c3:<path> | sed -n '<N>p'` 逐条实读复核; 复核命令与输出内联在每条 finding 里。

---

## 0. 行号复核结论 (先说通过的)

以下被审文档引用的落点**全部逐字复核通过**, 未发现漂移:

```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1230p;1236,1238p'
    if args.linked_issue:
        except Exception as exc:  # fail-soft: overlap advisory must not break the gate
            logger.warning("phase1_gate: linked_issue overlap check skipped (%s)", exc)
            out["linked_issue_overlap"] = []
$ git -C aria show d50f9c3:skills/state-scanner/lib/collision.py | sed -n '265,266p;268p;272,275p;278,279p'
    if not own_linked_issue: / return []
    _TERMINAL = ("done", "abandoned", "unknown")
    if c.status in _TERMINAL: / continue
    if not getattr(c, "linked_issue", None): / continue
    if c.track_id == own_track_id: / continue  # same-name collision …
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py | sed -n '228p;274p;377p;425p;427p;430p'
  (逐条与 Spec 一致: (container,session) 键 / release_claim / release_claim_by_track /
   rec.container== / rec.status == "active" / error="claim_not_found")
$ git -C aria show d50f9c3:skills/state-scanner/lib/constants.py | sed -n '36p;43,44p;51p'
STALE_TTL: int = 1800  /  "NO production heartbeat loop exists…"  /  SWEEP_TTL: int = 86400
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '210p'
        Possible values: "not_a_git_repo", "identity_error", "fetch_degraded",
```

以下两条**做得好, 明确记功** (本镜头上罕见): ① `sibling-spec-probe` §7 把 `verdict` 提为一等字段,
拒绝让消费方从 `hits == []` 推断 —— 这是本轮三份文档里对红线执行得最彻底的一处;
② 母 Spec §2.4b 对 `linked_issue_overlap` 的 `null` + `_error` 双字段修复方向正确 (R2/M-4)。
下面的 CRIT-1 恰恰是**这条修复只做了一半**。

---

## 1. `a1-entry-claim-duplicate-work-guard` (母 Spec, R4) — REVISE · 3C / 5M / 3m

### CRIT-1 · `unknown_schema_claims` 没有任何失败态 —— R2/M-4 在它自己的修复里原样复发
**定位**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:299-314` (§2.4a/§2.4b) ·
`:608` (SC-25) · `:652` (Impact `phase1_gate.py` 行 ③④) · grep 键: `unknown_schema_claims`
**severity: CRITICAL**

§2.4a 落版逐字: 门控 `:1230` 改为 `if args.linked_issue or args.include_terminal:`, **块内
`read_claims(repo)` 只调一次**, 再按两个 flag 各自填键。实读现有块结构:

```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1230,1238p'
    if args.linked_issue:
        try:
            claims = read_claims(repo).claims          # ← 两个键的共同上游
            out["linked_issue_overlap"] = linked_issue_overlaps(…)
        except Exception as exc:
            logger.warning(…)
            out["linked_issue_overlap"] = []
```

⇒ `read_claims` 抛异常时**两个键都填不上**。而 Spec 的 R2/M-4 修复 (`:317-320`) 只规定
`linked_issue_overlap = None` + `linked_issue_overlap_error`; 对 `unknown_schema_claims`
**一个字都没有**。SC-25 (`:608`) 的代码臂同样只断言这两个字段。

**这条降级路径在什么输入下会静默地把坏结果说成好结果**: A.1 带 `--include-terminal` 跑,
coordination ref 里存在 N 条 unknown-schema 竞品 claim, 而 `read_claims` 抛异常 (ref 半推 /
blob 解码失败 / `git ls-tree` 非零 / OOM) ⇒ 输出里 `unknown_schema_claims` **键缺席**。
四态表第 1 行 (`:311`) 逐字把「键缺席」定义为「**未检测** (既未传 `--linked-issue` 也未传
`--include-terminal`)」—— 这句在本路径上是**假的**, flag 传了, 只是没取到。更要命的是消费方
写这一格最自然的 Python 是 `out.get("unknown_schema_claims", 0) > 0`, 那读出来就是
**「0 条无法解析的 claim」= 零证据当正证据**, 与 FIX-12 刚刚救回来的「unknown 是正证据」
正面相反。

**处方 (字符级)**:
1. §2.4b 四态表加第 5 行: `unknown_schema_claims == null` **且** `unknown_schema_claims_error`
   非空 ⇒ 「**未能核实是否存在无法解析的 claim**」;
2. Impact `phase1_gate.py` 行 ④ 逐字改为: 「`:1236-1238` 的 `except` 分支**按已传 flag 分别**写
   失败态 —— `args.linked_issue` 为真时写 `linked_issue_overlap=None` +
   `linked_issue_overlap_error=<非空 token>`; `args.include_terminal` 为真时**同时**写
   `unknown_schema_claims=None` + `unknown_schema_claims_error=<非空 token>`;
   **任一 flag 为真而对应键未出现的实现视为违反本条**」;
3. SC-25 ① 的期望列追加: 「且当夹具带 `--include-terminal` 时,
   `unknown_schema_claims == null` 且 `unknown_schema_claims_error` 非空」。

---

### CRIT-2 · GC 清扫出的 `abandoned` 被 §2.3 渲染成「对方已显式退出」并附赠「接着做」
**定位**: `proposal.md:255` (§2.3 `abandoned` 档) · `:167-172` (§2.1 第 3 点「overlap 通道新鲜度免疫」)
· grep 键: `有人来过并放弃了` / `新鲜度免疫`
**severity: CRITICAL**

§2.3 选项表逐字: `abandoned` 档 ⇒ 选项集「**接着做 (直接认领)**」/「另起」, 理由列逐字
「**对方已显式退出 ⇒ 无冲突需处置**; 但仍须显示该信号 (它是「有人来过并放弃了」的**正证据**)」。

实读证伪「显式」二字:

```
$ git -C aria show d50f9c3:skills/state-scanner/lib/gc.py | sed -n '345p;352,360p'
    """Rewrite stale active claims (heartbeat older than TTL) to 'abandoned'.
    …no production heartbeat loop exists (heartbeat_at freezes at acquire),
    so a 30-minute threshold would abandon live parallel sessions and erase
    them from collision/overlap advisory surfaces.  See constants.SWEEP_TTL.
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_schema.py | sed -n '56p'
STATUS_ENUM: frozenset[str] = frozenset({"active","yielded","done","abandoned","unknown"})
```

`sweep_stale_active` 把 `status` 就地改写为 `'abandoned'`, `ClaimRecord` **没有任何字段**
区分「owner 自愿 release」与「24h 无心跳被 GC 清扫」。⇒ 一条**仍在活跃工作**的轨, 只要
心跳静默 (见 CRIT-3), 24h 后它的 claim 就变成 `abandoned`, 而 §2.3 会把这个 GC 产物
逐字渲染成「对方已显式退出」并请 owner 在「接着做 (直接认领)」上打勾。

**在什么输入下把坏结果说成好结果**: 容器 A 在做 issue #X (真在做), 其 heartbeat 因
`--heartbeat-only` 三级回落全落空而连续静默 skip 25 小时 ⇒ sweep 改写为 `abandoned` ⇒
容器 B 的 A.1 带 `--include-terminal` 看到该条, 按 §2.3 得到「无冲突需处置 / 接着做」⇒
**两个容器同时做同一 issue 且都相信对方已退出** —— 这正是本 Spec 立项要关闭的那个事故。

**并且它同时推翻一条承重论证**: §2.1「为什么必须含容器段」第 3 点逐字写
「overlap 通道则**新鲜度免疫** —— 实读 `lib/collision.py:265-292` 全函数体不含任何
heartbeat/新鲜度过滤, 对 stale claim 同样可见」。实读 `:268` `_TERMINAL` **含 `"abandoned"`**,
`:272-273` 无条件 `continue` ⇒ **免疫只在 `SWEEP_TTL`(24h) 窗口内成立**; 而 §2.2 自陈事故窗
实测 **48–72h**。⇒ 该承重论证在它自己声明的事故窗上不成立。

**处方 (字符级)**:
1. §2.3 `abandoned` 档「为什么不同」列逐字改为: 「对方 claim 为 `abandoned` —— **本机制无法
   区分自愿 release 与 24h 无心跳被 `sweep_stale_active` 清扫** (`lib/gc.py`, `ClaimRecord`
   无 swept 标记)。⇒ 当 `heartbeat_at` 与 `claimed_at` 之差 **≥ `SWEEP_TTL`** 时, 一律按
   `active` 档的三选项集请裁, **不得**给出「接着做 (直接认领)」」;
2. §2.1 第 3 点补限定: 「新鲜度免疫**仅在 `SWEEP_TTL` 窗口内**成立; 超窗后 claim 被改写为
   `abandoned` 并落入 `_TERMINAL` ⇒ 不带 `--include-terminal` 的通道对它同样失明。
   事故窗 48–72h > `SWEEP_TTL` 24h, 该缺口成文入 §6」;
3. §6 缺口表增一行: 「**本轨 claim 超 24h 未刷新被 sweep 改写为 `abandoned`**」/ 窗口 `> SWEEP_TTL` /
   覆盖机制「无 —— 且被 §2.3 渲染为对方自愿退出」;
4. 新增 **SC-30**(代码, CLI 全链路): 夹具造两条 `abandoned` claim, 一条 `heartbeat_at ≈ claimed_at`
   (自愿 release), 一条 `heartbeat_at` 早于 now 超 `SWEEP_TTL` (被 sweep) ⇒ 消费面措辞**必须可辨**;
   把两者渲染成同一句的实现必红。

---

### CRIT-3 · `--heartbeat-only` 的「跳过 + log(), 不猜」是完全静默的失败, 且 `log()` 不存在
**定位**: `proposal.md:216` (§2.2 三级回落 ③) · `:219` (fail-soft push) · `:612` (SC-28 第二臂)
· grep 键: `跳过 + \`log()\`, 不猜`
**severity: CRITICAL**

三个独立实读, 逐条:

```
$ git -C aria grep -n "def log(" d50f9c3 ; echo "exit=$?"
exit=1                                    # ← aria@d50f9c3 全仓零命中, log() 这个函数不存在
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | grep -n "logging\|logger ="
49:import logging
56:logger = logging.getLogger(__name__)     # ← 无 basicConfig / 无 handler
$ git -C aria grep -ln "basicConfig" d50f9c3 -- skills/state-scanner
d50f9c3:skills/state-scanner/scripts/scan.py   # ← 只有 scan.py, 与 phase1_gate 是两个进程
```

⇒ (a) Spec 规定的披露手段 `log()` 在代码库里不存在, 实现者只能自选; (b) `phase1_gate.py`
的 logger 无 handler, `logger.info` / `logger.debug` **被完全丢弃**, 只有 WARNING+ 经
`logging.lastResort` 到 stderr —— 一个照 Spec 字面写 `logger.debug("skip")` 的实现**逐字节合规
且零输出**; (c) 更关键: §2.2 的 R3/TL-M2 条款**禁止** `--heartbeat-only` 写生产遥测分区, 而
SC-28 第二臂 (`:612`) 还**正向断言** production 计数**不得**增长。

**⇒ 「heartbeat 跑了但三级回落全落空、静默 skip」与「heartbeat 编排层根本没挂载」在任何
持久化产物里逐字节相同。** 问题里那个「一个容器 heartbeat 连续三天静默 skip」的场景:
`.aria/coordination-telemetry.jsonl` 无新记录 (按设计)、非生产分区无记录 (Spec 未要求写)、
claim 的 `heartbeat_at` 冻结在 acquire 时刻、`coordination_probe` 只数 `run_gate`
production 记录 ⇒ **没有任何东西会红**。第三天该 claim 已被 sweep 成 `abandoned` (→ CRIT-2)。

**处方 (字符级)**:
1. §2.2 ③ 逐字改为: 「两级都取不到 ⇒ 跳过, 并 **`logger.warning("phase1_gate: heartbeat skipped
   (no track source: session-claim absent, handoff §6 carry-id absent)")`**」——
   点名 `logger.warning`, **不再用不存在的 `log()`**; 全文其余 `log()` 同批替换;
2. §2.2 增一条硬约束: 「`--heartbeat-only` **必须**向**非生产**分区
   (`.aria/coordination-telemetry-nonprod.jsonl`, 即 `_gated(_source="heartbeat")` 走的那条,
   实读 `phase1_gate.py:952` `_telemetry_path`) 追加**一条**记录, 字段含
   `outcome: "skipped"` + `skip_reason`; 该分区不被 `coordination_probe` 计数 (`runtime_probe.py:287`
   只认 `source=="production"`) ⇒ 与 TL-M2 的隔离要求不冲突」;
3. **SC-28 增第三臂**: 「连续 3 次在无 track 来源的环境下跑 `--heartbeat-only` ⇒
   非生产分区可数出 **3** 条 `outcome="skipped"` 记录; 静默 skip (零记录) 的实现必红」;
4. §2.2 的 push fail-soft (`:219`「push 尝试一次, 失败 fail-soft (log + 不阻断)」) 同款处置。

---

### MAJ-1 · A.1 acquire 成为 production 遥测分区的第二个写入者, 反死代码探针的分辨力被抹平
**定位**: `proposal.md:216` (TL-M2 段) · Impact 表 `coordination_probe.py` 行 (「仅注释/口径声明,
不改逻辑」) · grep 键: `coordination_probe`
**severity: MAJOR**

Spec 对 `--heartbeat-only` 用了正确论证 (TL-M2 逐字:「每次 `/state-scanner` 都会写一条 ⇒ 该
check 永远 OK …它要防的『机制接线了但没人调』正好被自己的心跳掩盖」), 但**没有对 A.1 acquire
用同一条论证**。而 A.1 acquire 走的正是同一个 `_main` → `_gated(_source="production")`:

```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1212,1214p'
    # This is the ONE production call site — it invokes the PRIVATE _gated with
    # _source="production" (the public run_gate has no source param, so no other
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '968,978p'
        record = { "ts":…, "source":…, "arm":…, "outcome":…, "track_id":…,
                   "claim_written":…, "collision_surfaced":…, "surface_kind":…, "latency_ms":… }
                                        # ← 没有 phase 字段
$ git -C aria show d50f9c3:skills/state-scanner/scripts/lib/runtime_probe.py | sed -n '287p'
        if not (isinstance(rec, dict) and rec.get("source") == "production"):
```

⇒ 探针只按 `source=="production"` + `ts` 近 14d 计数, **无法按调用点区分**。本 Spec 落地后
A.1 (每份 Spec 起草一次, 高频) 与 B-entry (低频) 写入同一分区同一形状的记录 ⇒
`coordination-gate-invocation` 这条 enabled check 之后**只能证明 `run_gate` 还活着**,
再也证明不了 **B-entry 那条接线**还活着。#95 要防的形状对 B-entry 腿变成不可达。

**在什么输入下把坏结果说成好结果**: 有人误删/改坏 `state-scanner/SKILL.md:149` 的 B-entry
挂载点 ⇒ Phase B 再也不跑闸门 ⇒ 但只要有人起草过 Spec, A.1 记录就让该 check 恒 `OK`。

**处方**: (i) Impact 表 `coordination_probe.py` 行由「仅注释/口径声明, 不改逻辑」改为
「`_emit_telemetry` 的 record **增 additive 字段 `phase`** (值即 `--phase` 实参);
`coordination_probe` 的计数口径**按 `phase` 前缀分档**声明」; (ii) 若判定超范围, **至少**在
§6 缺口表与「新表面」段逐字登记「本 Spec 使 `coordination-gate-invocation` 对 B-entry 腿失明」,
并新增 SC 断言该盲区已被成文 —— **不得**留在「不改逻辑」这句下面无人知晓。

### MAJ-2 · 「四态契约」既不穷尽也不互斥, 漏判行 3 是最自然的写法
**定位**: `proposal.md:310-315` (四态表) · `severity: MAJOR`

表里 4 行取自**两个独立键**的乘积空间 (`linked_issue_overlap` ∈ {缺席, `[]`, 非空, `null`} ×
`unknown_schema_claims` ∈ {缺席, `0`, `>0`}, 加上 CRIT-1 的 `null` 共 ≥15 组合)。具体漏判:

- **行 2 与行 3 可同时为真** (`linked_issue_overlap == []` 且 `unknown_schema_claims > 0`)。
  一个照「**四**态」写 `if/elif` 链的消费方先命中行 2 ⇒ 渲染「无碰撞」⇒ **永不检查行 3**,
  把 FIX-12 刚救回来的正证据再次丢掉。这就是「漏判其中一态会发生什么」的具体答案;
- `unknown_schema_claims == 0` (已检测、确无 unknown) 不在表里 —— 与「键缺席」在
  `.get(k, 0)` 下同值;
- §2.3 `:249` 的触发条件写作 `linked_issue_overlap[] 非空 (或 unknown_schema_claims > 0)`,
  是**并列或**语义, 与表的「四态」分档语义**不一致**, 两读并存。

**处方**: 表标题由「四态契约」改为「**两键各自的状态与措辞 (并列求值, 不是互斥分支)**」,
并在表下加一句硬约束逐字: 「**两个键必须各自独立求值、两句措辞并列输出;
禁止实现成 `if/elif` 单分支链** —— 行 2 与行 3 同时为真是正常情形。」SC-25 ② 的行为臂
增一个坏实现: 「只渲染行 2 的 if/elif 实现必红」。

### MAJ-3 · Phase B 消费同一张表时结构性只能看到两态, 且被表告知「未检测」
**定位**: `proposal.md:301` (`--include-terminal` 门控) · `:744-746` (新表面 #6 及其 BA-M3 订正)
· `severity: MAJOR`

新表面 #6 的 R3/BA-M3 订正已实读确认 `phase-b-developer/SKILL.md:93` **可选传 `--linked-issue`**
但**不传 `--include-terminal`**。⇒ Phase B 拿到的输出永远是: `linked_issue_overlap` 存在 +
`unknown_schema_claims` **键恒缺席**。按四态表行 1, 键缺席 = 「本轮**未检测**」——
可 Phase B 明明检测了 overlap。Spec 只处置了 `null` 形态对 Phase B 的影响,
**没处置 `unknown_schema_claims` 在 Phase B 上的恒缺席**。

**在什么输入下把坏结果说成好结果**: Phase B 入口带 `--linked-issue` 跑, ref 里有 N 条 unknown
竞品 claim ⇒ 输出 `linked_issue_overlap: []`, 无 `unknown_schema_claims` ⇒ 消费方读「无碰撞」,
N 条竞品从未被计数、也从未被声明为「未检测」。

**处方**: 四态表加作用域首行逐字:「**本表只对同时传 `--linked-issue` 与 `--include-terminal`
的 A.1 消费面成立**」; 另加一格「Phase B (只传 `--linked-issue`) ⇒ `unknown_schema_claims`
**恒缺席, 按『unknown 维度本轮未检测』渲染, 不得读作 0**」; 并把该行同步进 Impact 表
`state-scanner/SKILL.md:176` 的四态契约同步行。

### MAJ-4 · `track_form is None ⇒ 退回 ALL matching` 被叫做 fail-CLOSED, 实为把 TL-C1 的保护整体旁路
**定位**: `proposal.md:417` (§5.1) · `:453` (§5.3 release 定位) · `:642-643` (Impact) ·
`:753` (新表面 1(b) 自陈存疑) · grep 键: `track_form` / `ALL matching`
**severity: MAJOR**

Spec 逐字: 「旧 claim 无该字段 ⇒ 读作 `None` ⇒ **fail-CLOSED: 按「形态未知」处理, D.2b
退回现状 (ALL matching) 并 `log()` 披露**, 不猜」。

**这个命名是错的**: 相对于 TL-C1 要治的缺陷 (D.2b 连坐释放同 issue 其他在制方向),
「退回 ALL matching」**正是那个缺陷本身**。它 fail-**OPEN**: 释放得比意图多, 且后果不可逆
(claim 消失 ⇒ 对其他容器不可见 ⇒ 就是本 Spec 存在要关闭的窗口)。

**它在什么输入下恒成立**: 三条独立通道, 都不是「暂时的」——
(i) 全部**存量** claim 都无该字段, 而 §2.1b + §非目标 明写「**不改写存量 ref**」;
(ii) `release_claim_by_track` 的 `spec_slug` **缺省也是 ALL matching** (`:453` 逐字
「未传该参数时行为逐字节不变 (= 现状 ALL matching), 故 Phase B/D 既有调用零影响」) ⇒
**任何未同批更新的 D.2b 调用点**都走这条;
(iii) `:642` 明写**不 bump `schema_version`** ⇒ 跑旧版 aria-plugin 的容器写的 claim
**永远**没有该字段, 而多容器正是本 Spec 的立项前提 (§3: 9 种身份)。

**且无任何 SC 覆盖这条路径**:
```
$ grep -n "track_form" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
415, 419, 434, 504, 642, 643, 753     # ← SC 表 (:556-614) 内零命中
```
`:419` 声称「SC-1 / SC-15 / SC-27 三处一律按该字段判」, 但三条 SC 的场景列**无一含
`track_form is None` 臂**; SC-27(C) 只测 `--spec-slug` **参数**在场时的行为。
⇒ 过渡期的**运行时主导路径**零断言。

**处方 (字符级)**:
1. §5.1 该行逐字改为: 「旧 claim 无该字段 ⇒ 读作 `None` ⇒ **真 fail-CLOSED: D.2b 在
   `track_form is None` **且**未传 `--spec-slug` 时**拒绝执行**, 返回非零 + 错误 token
   `track_form_unknown`, 并 `logger.warning` 点名该 claim 的 `(container, track_id)`;
   由调用方显式传 `--spec-slug` 或 `--force-all` 二选一。**不得**静默退回 ALL matching」;
2. 若 owner 判「拒绝执行」代价过高, **退而求其次**必须做到: 退回 ALL matching 时
   `logger.warning` **点名将被释放的全部 claim 条数与 track_id**, 且 `release_gate.py` 的
   exit code 由 0 改为一个**可辨的非零值**;
3. 新增 **SC-31** (代码, CLI 全链路): 夹具 = 同 issue 两个方向、两条 **无 `track_form` 字段** 的
   active claim, 对方向 1 跑 D.2b **不传 `--spec-slug`** ⇒ 期望「方向 2 仍 `active` 或
   调用被拒绝」; 静默连坐释放的实现必红。**该条 baseline 必红**。

### MAJ-5 · `fetch_degraded` 与 exit code 脱钩, 只看退出码的编排层读不到降级
**定位**: `proposal.md:339` (§2.5 第 3 条) · `:575` (SC-10) · `severity: MAJOR`

```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/phase1_gate.py | sed -n '1240,1241p'
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if result.outcome in _PROCEED_OUTCOMES else 1
```
advisory 模式下 fetch 降级仍会 PROCEED ⇒ **exit 0**。SC-10 只断言 `GateResult.error ==
"fetch_degraded"` 这个 **JSON 字段**。而 §2 的调用形态是一条 SKILL.md 里的 `python3 …` 命令,
编排层最自然的判读就是退出码。Spec 全文没有任何一条要求编排层**必须解析 stdout JSON**。

**在什么输入下把坏结果说成好结果**: 网络降级 (双远端 fetch 失败) 下 A.1 跑闸门, exit 0,
编排层继续起草 —— 而它拿到的 claims 集合可能是空的或陈旧的, 四态表会渲染成「无碰撞」。

**处方**: §2.5 第 3 条末尾追加逐字: 「**`error` 只在 stdout JSON 里, 不进 exit code**
(`phase1_gate.py:1241` 的返回只反映 `outcome`) ⇒ A.1 / heartbeat 的编排层契约**必须**
明写「解析 stdout JSON 并检查 `error` 字段」, **不得**以 `exit == 0` 作为「已成功核实」的判据。」
SC-10 增第二臂: 「fetch 降级夹具下 **exit code 仍为 0** 且 `error == "fetch_degraded"`;
把降级实现成非零 exit 的、或把 `error` 留空的, 两臂都必红」。

### 次要 (3)
- **m-1** `:3` Status 与 `:781` 闸门状态 item 5 仍写「待 post_spec R3」/「下一步: 本版进
  post_spec R3」, 本轮是 R4 ⇒ 机读状态与现实脱钩 (memory `feedback_spec_frontmatter_reflects_reality`)。
- **m-2** §2.2 「degraded 时 push 尝试一次, 失败 fail-soft (log + 不阻断)」—— 与 CRIT-3 同款:
  push 失败意味着**本容器的 claim 没到远端 ⇒ 对其他容器不可见**, 这不是可以 fail-soft
  掉的事; 至少须与 CRIT-3 处方 2 的非生产遥测记录合并处置。
- **m-3** §2.3 `unattended` 分支「写进 handoff 待复议段并置 `awaiting_owner`」—— 无任何机械
  断言该段真被写, 也无任何消费者读 `awaiting_owner` (grep 全仓零命中)。
  memory `fix-recurs-in-fallback` 的「有记录 ≠ 有路由」形状; SC-26 是行为 fixture, 不构成运行时信号。

---

## 2. `linked-issue-field-availability` (子 Spec, R2) — REVISE · 1C / 4M / 1m

### CRIT-1 · SC-5(e) 自相矛盾, 而消解矛盾的错误方向就是「一次 `rm` 永久静默整条 check」
**定位**: `openspec/changes/linked-issue-field-availability/proposal.md:470` (SC-5 第 (e) 臂) ·
`:301-305` (§4 白名单外置段) · grep 键: `不得` + `exit 1`
**severity: CRITICAL** — 这是本镜头对三份文档提出的唯一 CRITICAL

SC-5(e) 逐字: 「`--grandfathered` 指向一个**不存在**的文件 (= 采用方首跑场景) ⇒ 白名单视为
**空集**, 探针**正常判定作用域内 proposal**, **不得** `exit 1`」。

在本仓实跑该场景 (该文件今天就不存在):

```
$ ls -la /home/dev/Aria/.aria/linked-issue-field-grandfathered.txt
ls: cannot access '…': No such file or directory
$ ls /home/dev/Aria/openspec/changes/
a1-entry-claim-duplicate-work-guard   aria-2.0-m6-cost-model-telemetry
aria-2.0-m6-dispatch-input-delivery   aria-2.0-m6-e2e-resilience
aria-2.0-m6-release-closeout          aria-2.0-m7-agent-lifecycle
aria-2.0-m7-fleet-aggregation         linked-issue-field-availability
sibling-spec-probe                                    # 9 份, §5 表判其中 6 份 NO_FIELD
```

⇒ 白名单空集 + 「正常判定」= 6 份 `NO_FIELD` 落第三臂 ⇒ **必然 `exit 1`**,
与同一句里的「**不得** `exit 1`」**直接冲突**。两个子句不可同时满足。

**实现者消解矛盾的两个方向, 一个是灾难**:
- 方向 A (对): 「不得**仅因文件缺失**而 exit 1」⇒ 本仓仍红;
- 方向 B (错, 但字面更贴 SC 措辞): 「白名单文件缺失 ⇒ 直接 exit 0」⇒
  **`rm .aria/linked-issue-field-grandfathered.txt` 一条命令让整条 enabled check 永久变绿**,
  且输出首行是 `OK (n 份在范围内, 0 条在册)` —— 零证据 (根本没读到册子) 被渲染成
  「0 条在册」这条**正断言**。红线的教科书形态。

**处方 (逐字替换 SC-5(e))**:
```
(e) `--grandfathered` 指向一个不存在的文件 (= 采用方首跑场景) ⇒ 白名单视为空集,
    探针照常判定作用域内 proposal; **不得仅因白名单文件缺失本身而 exit 1, 也不得因此
    短路成 exit 0** —— 该场景下的 exit 值完全由作用域内的违规数决定。
    夹具须用一个「作用域内全部 proposal 均合规」的临时仓验 exit 0,
    再用一个「作用域内含 1 份 NO_FIELD」的临时仓验 exit 1; 两臂缺一视为未满足本条。
    把「白名单文件缺失」实现成无条件 exit 0、当错误、或把 6 条 Aria 路径硬编码进脚本的, 三者均必红。
```

### MAJ-1 · 白名单文件缺失 = 三个原因的合流, 且陈旧守卫在缺失下结构性不可触发
**定位**: `:302` (「该参数缺省或文件不存在 ⇒ 白名单为空集, **不是错误**」) · `:363` (陈旧守卫三子情形)
· `:389` (fix 文案) · `:749` 母 Spec 新表面 4 已把它标为「与别处 fail-CLOSED 取向相反, 需专门审」
**severity: MAJOR**

三个语义完全不同的原因被合流成同一个「空集」:
(i) 有意不设白名单 (采用方首跑) · (ii) 文件被误删/改名 · (iii) 注册行漏掉 `--grandfathered` 参数。

而**陈旧条目守卫 (a)/(b)/(c) 是逐条遍历白名单条目的** ⇒ 白名单为空 ⇒ 守卫**结构上无法触发**。
⇒ 唯一的漂移护栏在「文件缺失」这一态下静默失效。

**在什么输入下把坏结果说成好结果 (且这条路径是被 fix 文案主动引导的)**: `fix` 逐字写
「被点名为「白名单陈旧条目」时: **删除本仓 `.aria/linked-issue-field-grandfathered.txt` 里那一行**」。
当 6 份 M6/M7 proposal 随开发周期陆续归档 (它们必然会) ⇒ 全部条目落子情形 (b) ⇒ 6 条 FAIL ⇒
维护者按 fix 文案「删行」的**自然过头形态**是删整个文件 ⇒ 从「6 条 allowlist 陈旧 FAIL」
一步变成 **`OK (n 份在范围内, 0 条在册)`**, 且没有任何 SC 断言该文件应当存在。

**处方**:
1. 探针区分两态并逐字成文: 「`--grandfathered` **未传** ⇒ 空集, 正常判定 (采用方默认);
   `--grandfathered` **传了但路径不存在** ⇒ 首行 `##SKIP## 白名单文件 <path> 不存在 —— 无法判定
   allowlist 是否陈旧`, exit 0」—— 把「没配」与「配了但读不到」分开, 后者**不得**渲染成「0 条在册」;
2. 新增 **SC-9** (代码, 仓本地): 「`.aria/state-checks.yaml` 里本 check 的 `command` 含
   `--grandfathered <path>` 且该 `<path>` 在**本仓**实存」—— 该断言只跑在 Aria 仓, 不进分发件;
3. `fix` 文案逐字加一句: 「**只删那一行, 不要删整个文件** —— 文件消失会使 allowlist 陈旧守卫失效。」

### MAJ-2 · `##SKIP##` 导入臂是裸 `except Exception`, 且把未经验证的因果当结论渲染
**定位**: `:368-378` (导入骨架代码块) · `:363` (五臂表第 2 行) · `severity: MAJOR`

Spec 给的字符级骨架逐字:
```python
try:
    from lib.collision import normalize_linked_issue
except Exception:
    print("##SKIP## normalize_linked_issue 不可导入 (aria 侧 lib/collision.py 缺失或版本 < v1.67.0)")
    sys.exit(0)
```

**这个 catch 会隐藏的具体错误类型** (逐条, 都不是稻草人):
- `collision.py` 或其相对依赖 `claim_schema.py` 里的 **`SyntaxError`** (import 期抛, 是 `Exception` 子类);
- `lib/__init__.py` 缺失或包结构被破坏导致的 `ImportError`/`ModuleNotFoundError` —— 与「版本旧」无关;
- **探针自己 `sys.path.insert` 拼错**目录 (Spec 同页刚论证过这里两种写法结果相反, `:380-390`);
- 传递依赖抛的 `RecursionError` / `MemoryError` / 任何模块级副作用异常;
- `PermissionError` (文件在但读不了) —— 与同库 `coordination_probe` 明确当成 **FALSE GREEN 修掉**的
  那一类**完全同形** (其 docstring `:45-52` 逐字: 「a partition that EXISTS but fails to read
  (e.g. permission denied) used to fall through … producing an `OK (-1 …)` exit-0 **FALSE GREEN**
  (#95 audit-Critical finding). It now maps to a STALE-class warn message + **exit 1**」)。

全部被渲染成同一句**未经验证的因果断言**「缺失或版本 < v1.67.0」。

**且 skip 在消费面是「可见但不压低通过率」**, 实读:
```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/collectors/custom_checks.py | sed -n '373,379p'
    if rc == 127: status = "error"
    elif rc == 0:
        status = "skip" if first_line.lstrip().startswith(SKIP_MARKER) else "pass"
    else: status = "fail"
$ … | sed -n '461,468p'
        if status == "pass": passed += 1
        elif status == "skip": skipped += 1
        else: failed += 1
```
⇒ `##SKIP##` 既不是 PASS 也不是 FAIL (Spec 这一点判断**正确**, 记功), 但它**不进 `failed` 桶**,
**不压低通过率**, 也**没有任何时限守卫** ⇒ 一个永久 skip 的 check 与一个从未注册的 check,
在 snapshot 里的唯一差别是 `results[]` 里多一行 `status:"skip"`。

**处方 (字符级, 替换该骨架)**:
```python
try:
    from lib.collision import normalize_linked_issue
except ImportError as e:                       # ← 只收 ImportError, 不吞其余
    print(f"##SKIP## normalize_linked_issue 不可导入: {type(e).__name__}: {e}")
    sys.exit(0)
except Exception as e:                         # ← 其余一律 FAIL, 不得降级为 skip
    print(f"FAIL 归一模块导入时抛出非 ImportError 异常: {type(e).__name__}: {e}")
    sys.exit(1)
```
并新增 **SC-10**: 「夹具把 `lib/collision.py` 换成一个含 `SyntaxError` 的文件 ⇒ 探针
**exit 1** 且首行以 `FAIL` 起; 判 `##SKIP##` 的实现必红 (零证据当正证据)」。

### MAJ-3 · `##SKIP##` 无时限 / 无 reason 分辨, 与同目录既有先例的处置方向相反
**定位**: `:363` 五臂表第 1 行 (「`openspec/changes/` 不存在, 或作用域内 0 份 proposal ⇒ `##SKIP##`」)
· `severity: MAJOR`

「作用域内 0 份 proposal」在本仓是**可达状态** (Phase D 归档完全部在制 Spec 后)。届时该 check
恒 skip。而 skip 既不 pass 也不 fail ⇒ 「探针本身坏了」与「本轮确实没东西可查」永久不可分辨,
也没有任何新鲜度窗口把它逼红 —— 而**同目录的 `coordination_probe` 正是用
`max_age_days`(默认 14) 解掉同一个问题的** (其 docstring `:9-15` 逐字:「counting *all-time*
production records would let ONE historical record keep the probe green forever」)。

**处方**: 把第 1 臂拆成两个可辨的 reason 串并各配 SC 臂:
`##SKIP## scope_dir_absent: openspec/changes/ 不存在` 与
`##SKIP## scope_empty: openspec/changes/ 存在但含 0 份 proposal`;
并在 `description` 里成文声明:「本 check 恒 skip **不是**健康常态 —— 若连续多轮 skip,
须人工确认是 scope 真空还是探针失效」(memory `feedback_false_green_dual_is_permanent_red`:
恒 skip 与恒红同样零信息)。

### MAJ-4 · 探针规定的「逐条点名」FAIL 明细, 在 snapshot 里只剩第一行 (实读得到, Spec 未意识到)
**定位**: `:363` 五臂表第 3/4 行 (「`FAIL` + **逐条** `path:line verdict 细节`」) ·
`:530` 新表面 #2 自陈「两条同时出现时的输出顺序/合并方式**未定义**」· `severity: MAJOR`

实读消费方对 stdout 的处置:
```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/collectors/custom_checks.py | sed -n '356,358p;385p'
        first_line = next(
            (ln for ln in (p.stdout or "").splitlines() if ln.strip()), ""
        )
        "output": first_line or f"rc={rc}",       # ← 进 snapshot 的只有第一行
```
⇒ 探针「逐条 `path:line verdict 细节`」写多少行都无所谓, **snapshot 里只保留第 1 行**。
新表面 #2 担心的「新违规 + 陈旧条目两条同时出现时怎么合并」不是排版问题, 是
**第 2 条起全部静默丢失** —— 而 `fix` 文案「在**被点名的** proposal.md 头部补一行」
对不可见的那些条根本无从执行。

**处方**: 五臂表第 3/4 行的输出列逐字改为「**首行必须是自足摘要**, 形如
`FAIL 3 份不合规: <path1>, <path2>, <path3> | 1 条 allowlist 陈旧: <path4>`
(全部被点名路径必须出现在**首行**); 明细可放后续行但**不得**依赖它们被消费方看到 ——
实读 `collectors/custom_checks.py:356-358` + `:385`, snapshot 只留首个非空行」;
SC-5(a)/(c) 的期望列同批改为断言**首行**含全部被点名 path。

### 次要 (1)
- **m-1** `:463` SC-6 跨仓已知限「必须 fail-soft 成 skip 而非 fail (零证据不当负证据)」——
  方向正确且值得记功, 但没规定 skip 的 reason token 必须稳定可 grep, 也没规定
  「读到了文件但断言失败」**不得**走同一分支 ⇒ 一个把断言失败也 catch 成 skip 的实现同样合规。

---

## 3. `sibling-spec-probe` (子 Spec, R2) — REVISE · 0C / 3M / 3m

> **先记功**: §7 把 `verdict` 提为一等字段、拒绝让消费方从 `hits == []` 推断,
> §9 给消费方定了 fail-closed 义务 (`exit != 0` / 不可解析 / 未知 `schema_version` ⇒ 一律
> `not_established`), §6 的 no-silent-caps 三件套 (stderr 披露 + `caps_applied[]` + 降 degraded),
> §4 步骤 3 拒绝 `("master","main")` 名字猜测 —— 这四条是本轮三份文档里对红线执行得最好的地方。
> 以下三条 major 都落在**已完整定义的 payload 与消费方之间的那道缝**上。

### MAJ-1 · `degraded` + 有命中 ⇒ 渲染「🔴 检测到 N 份竞品」, 覆盖不完整这件事被丢在地上
**定位**: `openspec/changes/sibling-spec-probe/proposal.md:319-323` (`verdict` 取值表) ·
`:352-356` (§9 措辞三档) · `:449` (SC-3) · `severity: MAJOR`

`verdict` 表逐字: `"sibling_found"` 的触发条件是「`hits` 非空」——**无覆盖完整性要求**;
`"no_sibling_found"` 才要求「覆盖完整」。⇒ remote A 解析成功并命中 1 条、remote B fetch 失败,
得到 `status="degraded"` + `verdict="sibling_found"` + `reason` 非空 (§7 逐字规定此时 reason 必非空)。

而 §9 的三档措辞表 **只按 `verdict` 分档**, `sibling_found` 那格逐字是
「🔴 检测到 N 份同 issue 的竞品 Spec: …」—— **`status` 与 `reason` 在消费面被整个丢弃**。

**在什么输入下把坏结果说成好结果**: 「只扫到一半、恰好找到 1 条」与「完整扫完、全世界就这 1 条」
渲染**逐字节相同**。审计席看到「检测到 1 份」会据此做协调决策, 而真实竞品可能有 3 份,
另外 2 份在那个 fetch 失败的 remote 上。这是同一条红线的「**部分证据当完整证据**」形态 ——
`verdict` 一等字段治好了 `hits==[]` 那一半, 没治这一半。

**处方 (字符级)**: §9 措辞表 `sibling_found` 那格逐字改为:
「`status == "ok"` ⇒ 「🔴 检测到 N 份同 issue 的竞品 Spec: …」;
 `status != "ok"` ⇒ 「🔴 检测到 N 份同 issue 的竞品 Spec: … —— **⚠️ 本轮覆盖不完整
 (`<reason>`), 可能还有未扫到的竞品**」。**两档不得合并**。」
SC-16 增一臂: 「`status="degraded"` 且 `hits` 非空的夹具 ⇒ 渲染中必须出现覆盖不完整的限定语;
只渲染命中数的实现必红」。

### MAJ-2 · 「每轮必跑」只靠 `execution-modes.md` 里一行散文, 没有任何运行时信号能证明它跑了
**定位**: `:330-346` (§8 落点表) · `:459` (SC-17) · `:483` (Impact「**不改** `skills/state-scanner/**`」)
· `severity: MAJOR`

§8 的落点是在 `references/execution-modes.md` 两个围栏块里各插一行字面串
`每轮入口: 竞品 spec 探针`; SC-17 断言的是**那一行在文件里出现恰 2 次**。
⇒ 断言的是「**文档里写了**」, 不是「**每轮真跑了**」。

而本 Spec 的探针**不留任何持久痕迹**: Impact 表逐字「**不改** `skills/state-scanner/**`」,
输出只有 stdout/stderr, 不写遥测、不写 ref (除 §5(f) 的 fetch 缓存 ref)。
⇒ 「audit-engine 每轮忘了跑探针」与「跑了、没命中」在事后**完全不可分辨**。
这正是同仓 `coordination_probe.py` 为 `run_gate` 造反死代码探针要防的形状
(其 docstring `:5-8` 逐字:「a gate that is *wired* but no longer *called* is the
『勾选完成 ≠ 运行现实』failure」), 而本 Spec 给自己造了同一个坑却没给自己配同一副护栏。
SC-16 是**行为 fixture**, 只在 AB 跑时可见, 不是运行时信号 (memory
`feedback_completion_signals_vs_runtime_invocation`)。

**处方**: §9 已要求把结果写进 `### Round N` —— 把它从「渲染义务」升为**机械可查的痕迹**:
1. §9 增逐字条款:「探针每轮的输出**必须**以一行固定前缀 (如 `sibling-probe: <verdict> (<reason>)`)
   落进该轮的 `### Round N` 记录; **`### Round N` 存在而该行缺席 = 本轮探针未跑**, 属缺陷不属正常」;
2. 新增 SC:「对一份多轮聚合报告计数: `### Round N` 标题条数 **==** `sibling-probe:` 行条数;
   少一条即必红」—— 宿主 = `skills/audit-engine/tests/`, 与 SC-17 同批。

### MAJ-3 · fetch 失败时未逐字禁止回落读上一轮的私有缓存 ref
**定位**: `:222-273` (§5, 私有 ref `refs/aria/sibling-probe/<remote>/<branch>`) ·
`:512` (新表面 #2 自陈「未定义 GC / 未测并发」) · `:198-215` (§4 步骤 4) · `severity: MAJOR`

§4 步骤 4 刚刚用一段很好的论证否决了本地 `refs/remotes/<R>/HEAD`, 逐字:
「用它等于**「测量新鲜度」而非「获取新鲜度」**(memory `feedback_freshness_must_be_fetched_not_measured`),
会静默给出陈旧答案」。但 §5 随即引入了本 Spec **自己的**本地缓存 ref
`refs/aria/sibling-probe/<remote>/<branch>`, 而**没有把同一条禁令下到它头上**。

**在什么输入下把坏结果说成好结果**: 第 1 轮 fetch 成功, ref 写入; 第 2 轮 fetch 失败。
实现者最自然的写法是「ref 还在, 就用上次的语料扫一遍」⇒ 得到 `hits` (来自上一轮的陈旧语料),
按 `verdict` 表 `hits` 非空 ⇒ `sibling_found`, 或者更糟: 上一轮语料里没有而这一轮新增了竞品 ⇒
`hits == []` + 若实现者同时认为「有 ref 就算覆盖完整」⇒ **`no_sibling_found`** ——
**陈旧证据被当成本轮的完整正证据**, 恰是 §4 步骤 4 花整段论证要防的病, 在下一节复发
(memory `fix-recurs-in-fallback`: 修复类 change 最易在自己新写的兜底路径重犯要治的病)。

**处方 (字符级)**: §5 增一条硬约束逐字:
「**fetch 失败时不得回落读上一轮写入的 `refs/aria/sibling-probe/…`** —— 该 ref 只是本轮
 fetch 的落点, **不是缓存**。任一 remote 的 fetch 失败 ⇒ 该 remote 记 `error_kind` 非空、
 `scanned=0`, 整体 `status="degraded"`, 且**该 remote 上的既有 ref 内容一律不参与本轮扫描**。」
SC-3 增负控臂:「夹具预置一条含匹配 proposal 的旧 `refs/aria/sibling-probe/...` ref 并让本轮
fetch 失败 ⇒ `hits` 中**不得**出现来自该 remote 的项; 复用旧 ref 的实现必红」。

### 次要 (3)
- **m-1** `:318` `reason` 是单值 `str | null`, 但 degraded 可由多因并发
  (remote A `fetch_failed` + remote B `cap_applied`) ⇒ 单值必丢一条。建议改 `list[str]` 或
  成文规定优先级顺序。
- **m-2** `:327` 「exit 非 0 时 stdout **不保证**是合法 JSON」+ §9 消费方 fail-closed ——
  方向对, 但没规定探针自身失败时**必须**向 stderr 写一个稳定可 grep 的 token,
  也没规定 audit-engine 把「探针崩了」这个事实与「探针说未能核实」在轮次记录里**分开写**。
  ⇒ 连续每轮崩溃与连续每轮 `not_established` 在报告里同形。
- **m-3** §10 B4 自陈「随机一份 proposal 落入 `own_token_absent` 的概率约**九成**」⇒
  `verdict="not_established"` 是**常态**, §9 要求每轮渲染「未能核实」⇒ 恒红面。
  本 Spec 自己在别处正确引用了 `feedback_false_green_dual_is_permanent_red`,
  但没把它用在这一处 (memory `cite≠apply`)。建议为 `reason == "own_token_absent"`
  单列一档更短的措辞, 与「真的没扫成」区分。

---

## 4. 跨三份 Spec 的接缝 (combined 专有)

以下两条**单独审任一份都看不见**, 落在角度之间 (memory `feedback_combined_mode_sister_spec_audit_value`):

- **SEAM-1 (已计入母 CRIT-2/MAJ-3)**: 母 Spec 的四态契约被三个不同消费面共用 ——
  A.1 (两 flag 全传)、Phase B (只传 `--linked-issue`)、子 Spec 探针 (完全不读 claim)。
  三者看到的键集合不同, 而契约表只有一份、无作用域限定 ⇒ 同一张表在两个消费面上给出
  错误答案。母 Spec §2.4b 需加作用域首行 (处方见 MAJ-3)。
- **SEAM-2**: 三份文档共用一个**不存在的**披露原语 `log()`
  (`git -C aria grep -n "def log(" d50f9c3` 零命中): 母 §2.2 ③/§5.1、探针 §6 no-silent-caps。
  三份都把「失败被披露」这件事托付给同一个不存在的函数。**处方**: 三份同批把 `log()`
  替换为逐字的 `logger.warning(...)` 或 `print(..., file=sys.stderr)`, 并各自成文
  「`logging.getLogger(__name__)` 在这些脚本里**无 handler**
  (`basicConfig` 只在 `scan.py`) ⇒ `logger.info`/`debug` 会被完全丢弃, **不得**用它做失败披露」。

---

## 5. 收敛判据 (给主控 / owner)

- 三份**均 REVISE**, `scope_ok` 三份均 true (未发现越界改动)。
- 母 Spec 的 3 条 critical **全部落在 R3 清账轮新引入、未经任何审计的表面上**
  (§2.4a `unknown_schema_claims` / §2.2 heartbeat 三级回落 + 遥测分区 / §5.1 `track_form`) ——
  与该 Spec 自己在 `:749` 列出的「请 R4 优先审」清单**逐条对上**, 该清单的自陈是准确的。
- 本席**不建议**继续加轮: 母 Spec 的 critical 数从 R3 的 3 条到 R4 仍是 3 条 (内容全换),
  即「每轮 fix 引入约等量同形状缺陷」(memory `stop-adding-rounds` / `marginal-return-negative`)。
  本轮 3 条 critical **全部是上一轮 fix 自己造的**, 占比 3/3 —— 按
  `feedback_audit_marginal_return_goes_negative` 的判据 (本轮 fix 引入的 major 占比 > 1/2)
  **已过拐点**。建议处置: 换执笔席直接落 CRIT-1/2/3 与 MAJ-4 的字符级处方 (它们都是逐字替换,
  无设计裁量), 不再走通用审计轮。
- 两份子 Spec 的 major 均可**逐字替换**消解, 无一需要重新设计。
