---
checkpoint: post_spec
round: 4
role: type-design-analyzer
lens: 类型与契约设计 (invariant strength / encapsulation / representable-illegal-states)
verdict: REVISE
scope_ok: true
counts:
  a1-entry-claim-duplicate-work-guard: { critical: 2, major: 6, minor: 1 }   # A-M7 已由并发 R4 席位闭环, 不计入 open
  linked-issue-field-availability:     { critical: 1, major: 4, minor: 1 }
  sibling-spec-probe:                  { critical: 0, major: 3, minor: 1 }
  combined:                            { critical: 3, major: 13, minor: 3 }
baseline:
  main_repo: 322f280 (读取时工作树干净; 审计期间三份被审文件被并发席位改写, 见 §0.1)
  aria_submodule: d50f9c3 (origin/master)
verify_command: 'git -C aria show d50f9c3:<path> | sed -n ''<N>p'''
---

# post_spec R4 — 类型与契约设计席 (三份 Spec 联审)

> **纪律声明**: 本报告的每一条 finding 都带「我实跑的命令 + 逐字输出」。凡我未能实跑核实的, 单列于末尾 §未核实。
> **本席未修改任何被审文件。**

## 0. 复核环境 (可重跑)

```
$ git -C /home/dev/Aria log --oneline -1
322f280 docs(spec): 声明 R3 清账轮新引入的 7 项未审表面 (给 R4 的优先审清单)
$ git -C /home/dev/Aria/aria rev-parse origin/master
d50f9c3a43c4c5804914385f638f9b29554f3659
```

为了在**真实代码**上验证契约, 我把 `d50f9c3` 的 `skills/state-scanner/lib/` 抽到 scratchpad
(`/tmp/claude-1000/-home-dev-Aria/382bee19-b637-46b5-9a6f-4baf3c702fc4/scratchpad/ss/lib/`),
以下凡标「实跑」者均在该副本上执行, 未触碰工作树。

---

## 0.1 ⚠️ 并发写入告警 + 行号再锚定 (必读)

**我的全部阅读基线 = commit `322f280`** (起点 `git status --porcelain` 只有 ` M aria-orchestrator`)。
**审计进行期间, 三份被审文件被并发的 R4 席位改写了** —— 收尾复核时:

```
$ git status --porcelain
 M aria-orchestrator
 M openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
 M openspec/changes/linked-issue-field-availability/proposal.md
 M openspec/changes/sibling-spec-probe/proposal.md
?? .aria/audit-reports/post_spec-R4-...-code-architect.md
?? .aria/audit-reports/post_spec-R4-...-pr-test-analyzer.md
?? .aria/audit-reports/post_spec-R4-...-silent-failure-hunter.md
?? .aria/audit-reports/post_spec-R4-...-type-design-analyzer.md   ← 本报告

$ git diff --stat openspec/changes/
 .../a1-entry-claim-duplicate-work-guard/proposal.md |  6 ++--
 .../linked-issue-field-availability/proposal.md     | 29 ++++++++++++++++++
 openspec/changes/sibling-spec-probe/proposal.md     | 34 ++++++++++++++++++--
 3 files changed, 64 insertions(+), 5 deletions(-)
```

**本席未写过这三个文件中的任何一个**。这本身是 memory `subagent-applies-diff` 的又一实例
(并发审计席位持有 Write/Edit 就会落盘), 也说明**本轮 R4 的「被审对象」在审计过程中是移动靶** ——
主控收敛时须以某个固定 SHA 重新对账, 否则各席的行号引用互相不可比。

**我收尾时逐条重锚定了全部承重引用**, 下表给的是**复核时刻工作树**的行号 (括号内是我阅读时的 `322f280` 行号):

| finding | 内容锚点 (grep 用) | 现行号 | 322f280 行号 | 断言是否仍成立 |
|---|---|---|---|---|
| A-C1 | `新增两个 additive 字段` (Impact claim_schema 行) | `:646` | `:642` | ✅ 成立 |
| A-C1 | Impact `claim_lifecycle.py (第二处变更)` 行 | `:647` | `:643` | ✅ 成立 (并发席位给 `heartbeat_by_track` 补了签名, **但仍未处置 `ClaimRecord` 重建点的透传**) |
| A-C2 | `fail-CLOSED: 按「形态未知」处理` | `:417` | `:417` | ✅ 成立 |
| A-C2 | `未传该参数时行为逐字节不变` | `:457` | `:453` | ✅ 成立 |
| A-C2 | `⛔ 已考虑并否决的替代` | `:460` | `:457` | ✅ 成立 |
| A-M1 | `无关联 issue 时回落` (§2.1 唯一触发条件) | `:131` | `:131` | ✅ 成立 |
| A-M1 | `有 issue 却走回落形的后起 Spec` | `:412` / `:508` | `:412` / `:504` | ✅ 成立 |
| A-M1 | `同 issue 的 N 个方向` (§5.3 相反断言) | `:448` | `:443` | ✅ 成立 |
| A-M1 | SC-15 第三类夹具 | `:590` | `:586` | ✅ 成立 |
| A-M2 | `SC-1 / SC-15 / SC-27 三处一律按该字段判` | `:419` | `:419` | ✅ 成立 |
| A-M2 | SC 表区间 (SC-1 → SC-29) | `:566`–`:616` | `:567`–`:614` | ✅ 成立 — `grep -n track_form` 现命中 `415 419 434 508 646 647 757`, **SC 区间内仍零命中** |
| A-M4 | `与 Part B1 引入 \`linked_issue\` 同款` | `:455` / `:646` | `:451` / `:642` | ✅ 成立 |
| A-M5 | `§2.2 说明其与` | `:651` | `:647` | ✅ 成立 |
| A-M6 | `Phase B/D 既有调用零影响` | `:457` / `:647` | `:453` / `:643` | ✅ 成立 (现有**两处**同措辞) |
| A-M6 | `D.2b 的 release_gate.py 命令模板增` | `:650` | `:646` | ✅ 成立 |
| **A-M7** | `same session` | — | `:441` | ❌ **已闭环** — 见下 |
| B-C1 | `E6 — --linked-issue 实参` | `:193` | `:193` | ✅ 成立 (**verdict 门仍未加**) |
| B-C1 | `只产出** canonical token` | `:269` | `:240` | ✅ 成立 |
| B-M3 | `**不得** \`exit 1\`` (SC-5(e)) | `:504` | `:478` | ✅ 成立 |
| B-M4 | `新建的 proposal 一律不在册` | `:440` | `:409` | ✅ 成立 |
| C-M1 | `"bad_token"` (§3 映射表) vs `bad_token_union` (§7) | `:111` / `:328` | `:111` / `:298` | ✅ 成立 — 两处拼写**仍然不同** |
| C-M2 | `"own_token_absent"` (§7 reason 枚举) | `:325` | `:296` | ✅ 成立 |

**⇒ 除 A-M7 外, 本报告的全部 finding 在复核时刻的工作树上逐条仍然成立。**

> **A-M7 已由并发席位闭环 (独立复现, 结论一致)**: 我收尾复核时发现主控已在 `:445` 落了一段
> 「**⚠️ 引文订正 (R4/code-explorer 抓, 主控复核确认自己错了)**」, 逐字承认「**原文没有『same session』这四个字**」,
> 并交代了错法 (`sed | grep -iE "all|matching"` 丢掉了不含关键词的 `:397-398` 两行, 然后把 `:396` 与 `:399` **拼接**成一句)。
> ⇒ **两席独立实读、独立命中、结论一致**, 这是收敛信号。**本 finding 因此不计入 open counts**,
> 但 A-M7 正文保留 —— 因为它的**第二半 (被截掉的 `review I1` 从句是反对收窄 release 作用域的理据)**
> 在订正段里**没有被处置**, 那一半仍然 open, 已并入 A-C1 的处方 3。

---

# A. 母 Spec — `a1-entry-claim-duplicate-work-guard` (R4)

**verdict: REVISE** · **counts: 2 Critical / 7 Major / 1 minor**

## A-C1 (Critical) — 两个新字段的**传播面漏了 5 个 `ClaimRecord` 重建点**; `heartbeat()` 会静默抹掉它们, D.2b 的 `--spec-slug` 过滤随之**恒不匹配**

**定位**: 母 Spec `:642`-`:643` (Impact 表 `claim_schema.py` / `claim_lifecycle.py (第二处变更)` 两行) · §5.3 `:447`-`:455`

**实跑**:

```
$ git -C aria grep -n "linked_issue=" d50f9c3 -- 'skills/state-scanner/lib' 'skills/state-scanner/scripts'
skills/state-scanner/lib/claim_lifecycle.py:157:        linked_issue=linked_issue,
skills/state-scanner/lib/claim_lifecycle.py:255:        linked_issue=existing.linked_issue,
skills/state-scanner/lib/claim_lifecycle.py:357:        linked_issue=existing.linked_issue,
skills/state-scanner/lib/claim_lifecycle.py:448:            linked_issue=existing.linked_issue,
skills/state-scanner/lib/claim_schema.py:311:        linked_issue=linked_issue,
skills/state-scanner/lib/gc.py:407:                linked_issue=record.linked_issue,
skills/state-scanner/scripts/phase1_gate.py:735:        linked_issue=linked_issue,
skills/state-scanner/scripts/phase1_gate.py:760:            linked_issue=linked_issue,
skills/state-scanner/scripts/phase1_gate.py:1025:        linked_issue=linked_issue,
skills/state-scanner/scripts/phase1_gate.py:1062:        linked_issue=linked_issue,
skills/state-scanner/scripts/phase1_gate.py:1221:        linked_issue=args.linked_issue,
```

`linked_issue` —— **母 Spec 自己援引的那个 additive 先例** —— 落地时需要 **11 处**显式透传, 横跨 4 个文件。
原因是 `ClaimRecord` 是 `@dataclass(frozen=True)` (`claim_schema.py:69-70`), 全仓**没有一处**用
`dataclasses.replace()`, 每个重建点都逐字段枚举:

```
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py | sed -n '243,256p'
    # Rebuild the record with an updated heartbeat_at; claimed_at is preserved.
    updated = ClaimRecord(
        schema_version=existing.schema_version,
        track_id=existing.track_id,
        ...
        superseded_from=existing.superseded_from,
        linked_issue=existing.linked_issue,
    )
```

而 Impact 表**只点名两处**: `claim_schema.py` (加字段定义) 与 `claim_lifecycle.py` 的
`acquire_claim` 写入 + `release_claim_by_track` 过滤。**未点名**:
`claim_lifecycle.py:244` (`heartbeat()`)、`:346` (`release_claim`)、`gc.py:396`
(`sweep_stale_active`, 逐字自陈 `Cross-container by design ... it MAY rewrite other
containers' claim files`)、`phase1_gate.py:749`、以及 `claim_schema.py` 的
`serialize_claim`(`:315`, 逐字 `if record.linked_issue is not None: out[...]`) 与
`parse_claim`(`:291-298` 的 optional 字段类型校验)。

**后果链 (承重, 不是理论)**: 母 Spec §2.2 要求新增 by-track heartbeat 变体, 并要求它
「**形态照抄 `release_claim` / `release_claim_by_track` 的并存模式**」(`:190` 一带) ——
照抄的正是上面这种逐字段枚举。SC-21 要求 `/state-scanner` **每次**调用都刷新 claim。
⇒ A.1 写入 `spec_slug`/`track_form` 的那条 active claim, **在第一次 heartbeat 后这两个字段就没了**
(`serialize_claim` 对 `None` 直接不落盘 ⇒ 读回也是 `None`)。
⇒ D.2b 传 `--spec-slug` 时三元组过滤命中 0 条 ⇒ `claim_not_found` ⇒ claim 永远 active 到 sweep。
⇒ 这**同时**打回 `release_claim_by_track` docstring 里 review I1 亲口修好的那条 (
`:399-401` 逐字 `releasing only the earliest would leave the later session-claims active and
the track would still read as occupied after ship`) —— 即 SC-23 与 C-C 一起回归。

**类型设计判定**: 不变量「acquire 写入 ⇒ release 读得到」跨越了 5 个未被守卫的 mutation point。
这是典型的 *inconsistent enforcement across mutation methods*, 与 memory
`feedback_schema_column_dataclass_field_pair` 同形 (加列必须同步每个构造点, 漏则 `getattr` 静默 `None`)。

**处方 (字符级)**:
1. Impact 表把上述 **5 个重建点 + `serialize_claim` + `parse_claim`** 逐行列出, 每行写明
   「透传 `spec_slug` 与 `track_form`」;
2. 或者 (更强, 推荐) 在 `claim_lifecycle.py` / `gc.py` 一律改用
   `dataclasses.replace(existing, heartbeat_at=ts_str)` —— 让「新增 additive 字段」在类型层
   **默认透传**, 把这一整类缺陷一次性关掉 (memory `fix-the-class`);
3. 增一条 SC (追加编号): **acquire → by-track heartbeat → D.2b `--spec-slug` release** 三步全链路,
   断言 release 后该 claim 不再 active。**baseline 必红**, 且「heartbeat 漏透传」的坏实现也必红
   —— 现有 SC-23 只走 acquire→release, 结构性抓不到中间那次 heartbeat。

---

## A-C2 (Critical) — `track_form == None` 的处置: §5.1 与 §5.3 对**同一输入**给出相反答案; 且它被标成 fail-CLOSED, 实际方向是 fail-**OPEN**

**定位**: §5.1 `:417` (「旧 claim 无该字段 ⇒ 读作 `None` ⇒ **fail-CLOSED: 按「形态未知」处理, D.2b 退回现状 (ALL matching) 并 `log()` 披露**」) vs §5.3 `:453` (「只释放 `(container, 归一 track_id, spec_slug)` 三元组匹配的 claim」) · Impact `:642` 同措辞

**实跑** (按 §5.3 逐字实现过滤谓词, 基线谓词逐字取自 `claim_lifecycle.py:422-428`):

```
A) no --spec-slug : ['s1', 's2', 's3']
   baseline       : ['s1', 's2', 's3']
B) --spec-slug dir-one : ['s2']
C) legacy-only ref, D.2b passes --spec-slug dir-one : EMPTY -> claim_not_found

§5.1 says: legacy track_form is None => fail-CLOSED => 'D.2b 退回现状 (ALL matching)' => would release ['s1', 's2', 's3']
§5.3 says: only 三元组匹配 => would release ['s2']
```

(`s1` = 上线前写的存量 claim, `spec_slug=None`/`track_form=None`; `s2`/`s3` = 同 issue 两个方向)

**三条独立缺陷, 同一根**:

1. **矛盾**: 对同一条 legacy claim, §5.1 说「释放全部」, §5.3 说「一条都不释放」。两个独立实现者
   必得相反结果 —— memory `spec-underdetermination` 的定义式形状。且措辞未说明这个回退是
   **per-claim** 还是 **per-invocation** 决定的 (一批 claim 里既有 `track_form="issue"` 又有 `None` 时怎么办, 全文无字)。
2. **「fail-CLOSED」是误标**。fail-CLOSED = 不确定时**拒绝/阻断**; 这里是不确定时**以最大作用域执行破坏性动作**。
   对本 Spec 唯一的承重不变量 ——「在制方向必须始终持有可见 claim」—— 这是彻头彻尾的 fail-**OPEN**。
   §5.3 自己 `:457-461` 逐字否决过等价方案: 「⛔ 已考虑并否决的替代: 不加字段, 接受连坐 …
   否决理由: 幸存方向**处于无 claim 状态** ⇒ 对其他容器不可见 —— 这正是本 Spec 存在要关闭的那个窗口。
   用「事后自愈」换「窗口期不可见」是**本 Spec 自我否定**」。
   ⇒ **默认值把被否决的方案设成了缺省路径**, 而且**上线当天全部存量 claim 都走这条路径**
   (它们无一例外没有 `track_form`)。
3. **零 SC 覆盖**: `grep -n "track_form"` 全文 6 命中 (`:415/:416/:419/:434/:504/:642` + 新表面段),
   **没有一条落在 SC 行的「场景 / 期望 / 怎么会红」里**。这条最危险的分支没有任何夹具会为它变红。

**处方 (字符级, 三选一, 但必须选一条并写死)**:
- (a) **`track_form is None` ⇒ 拒绝执行 release, 退出码非 0 + 点名该 claim**, 要求人显式加
  `--force-all-matching`。这才是 fail-CLOSED, 且与 Rule #10 的极性一致;
- (b) **`track_form is None` ⇒ 只释放 `spec_slug` 精确匹配的那些, 并对 `spec_slug is None` 的
  legacy claim 单独 log 一行 `legacy_claim_not_released`**, 让它随 sweep 退场 (与 §2.1b 的
  「旧轨自然随 GC 退场」措辞一致);
- (c) 若确实要保留 ALL matching, **把它从「fail-CLOSED」改称「fail-OPEN 的已知限」并写进 §6 缺口表**,
  同时删掉 §5.3 里对同一行为的否决段, 否则两段互相拆台。
- **无论选哪条**, §5.1 与 §5.3 的措辞必须**逐字统一**, 并追加一条 SC 专钉该分支
  (夹具: 一条 legacy claim + 两条新形态 claim, 断言哪些被释放)。

---

## A-M1 (Major) — `track_form` 的立论第三类「有 issue 却走回落形的后起 Spec」在 §2.1 的派生规则下**不可达**; SC-15 因此要求一个「跑派生代码造不出来」的夹具

**定位**: §5.1 `:412` · D12 `:504` · SC-15 `:586` · §2.1 `:131`

**实跑**:

```
$ sed -n '131p' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
`<归一后 basename>-<str(int(number))>-<container_uuid>`; 无关联 issue 时回落 `<spec-slug>-<container_uuid>`。

$ grep -n "后起\|已被占用" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
412:> 2. **读 `claim.linked_issue` 是否非空** —— … 「有 issue 却走回落形的后起 Spec」—— 同 issue 的第二份 Spec 因 issue 派生形的 track_id 已被占用而落在**含-slug 形**…
504:| **D12** (新) | … 读 `linked_issue` 则对「有 issue 却走回落形的后起 Spec」**给相反答案** …
586:| **SC-15** (代码) | track-id 为**回落形** … 含「无关联 issue 者」**与「同 issue 后起 Spec 落在回落形者」** |
```

§2.1 的派生规则里, 走回落形的**唯一**触发条件是「无关联 issue」。全文**没有任何一条**规则说
「track_id 已被占用 ⇒ 落回落形」。更直接的是 §5.3 `:443-444` 逐字断言了**相反**的事实:
「issue 派生形下, 同 issue 的 N 个方向**共用同一个 track_id** (各自 session 不同)」——
即同 issue 的第二份 Spec **不会**落回落形, 它就是共用那个 track_id, 靠 `spec_slug` 区分。

⇒ 三重后果:
1. §5.1 用来否决判定式 (2) 的那个反例**不存在**;
2. SC-15 明文要求第三类夹具, 而 §5.1 `:419` 同时规定「夹具**不得预标形态**, 而应**跑派生代码让它自己写**」
   —— **两条硬约束合起来使该夹具不可构造** (memory `feedback_verify_predicate_inputs_exist`:
   判定机制必须先确认「它要判的输入真会被生成」);
3. `track_form` 仍有独立理由 (判定式 (1) 反推确有歧义, 反例 `fix-issue-149-a1b2c3d4` 成立), 但
   **它的一半立论是悬空的**, R4 之后必须重新论证「值不值得为此加一个 schema 字段」。

**处方**: 二选一并写死 ——
(a) 在 §2.1 补一条真实的「issue 派生形被占用 ⇒ 落回落形」规则 (若真要这个行为), 并同批修 §5.3 的
「共用同一 track_id」措辞; 或
(b) **删掉第三类**, 把 §5.1 对判定式 (2) 的否决改为只依据判定式 (1) 的歧义反例, 并把 SC-15 的
「同 issue 后起 Spec 落在回落形者」子句一并删除。

---

## A-M2 (Major) — §5.1 声称「SC-1 / SC-15 / SC-27 三处一律按 `track_form` 判」—— 实读三条 SC, **无一提及该字段**; SC-1 / SC-15 仍在用被 §5.1 自己否决掉的字符串形态谓词

**定位**: §5.1 `:419` vs SC-1 `:573` / SC-15 `:586` / SC-27 `:610`

**实跑**:

```
$ grep -n "track_form" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | cut -d: -f1
415
416
419
434
504
642
753
```

—— SC 表的行号区间是 `:567`–`:614`, **零命中**。逐条读:

- SC-1 `:573`: 「track-id 为 **issue 派生形** (`<basename>-<n>-<uuid>`, **不含 slug** …)」← 字符串形态谓词, 正是 §5.1 判定式 (1) 判「有歧义」的那个;
- SC-15 `:586`: 「track-id 为**回落形** (`<spec-slug>-<uuid>`, **含 slug** …)」← 同上;
- SC-27 `:610` (C) 臂: 「同 track_id, 不同 `spec_slug`」← 只提 `spec_slug`, 不提 `track_form`。

⇒ R3/TL-M4 的 fix 只落在 §5.1 与 §5.2「slug 改名」那一格, **没有推广到它自己点名的三条 SC**。
这正是 memory `fix-the-class`「修实例必问这形状还有几个兄弟位置」的第 N 次复现。

**处方**: SC-1 / SC-15 / SC-27 的「场景」列逐字改为 `claim.track_form == "issue"` / `== "slug"`,
并在每条的「怎么会红」列补一句「用 track_id 字符串形态做谓词的实现在夹具
`fix-issue-149-<uuid>` 上必红」(该反例 §5.1 已给出, 直接复用)。

---

## A-M3 (Major) — 四个字段之间的一致性不变量**全部只存在于散文**; `track_form` 的值域无任何校验 ⇒ 可表示非法状态

**问题的直接回答 (R4 任务问 1(a))**: **不正交, 且存在可矛盾表达的状态。**

| # | 应成立的不变量 | 现状 |
|---|---|---|
| I-1 | `track_form == "issue"` ⇒ `linked_issue is not None` | 无任何校验; `(track_form="issue", linked_issue=None)` 可写可读 |
| I-2 | `track_form == "issue"` ⇒ `track_id` 的前两段 == `derive(linked_issue)` | 无校验; 改了 `linked_issue` 不改 `track_id` 就矛盾 |
| I-3 | `track_form == "slug"` ⇒ `track_id.startswith(spec_slug)` | 母 Spec `:452` 逐字承认「该字段与其冗余但**不矛盾**」—— 但**冗余就是可矛盾**, 无任何一处强制二者一致 |
| I-4 | `track_form ∈ {"issue","slug",None}` | **无枚举校验**。`parse_claim` 对 optional 字段只做类型检查 (`claim_schema.py:291-298` 对 `linked_issue` 那样), 且母 Spec 未要求为新字段加校验 ⇒ `track_form="banana"` 会被完整解析。全文只定义了 `None` 的处置, **第四个取值的处置未定义** —— 正向枚举天然 fail-OPEN (memory `feedback_invariant_needs_failclosed_default`) |

**实读依据**:

```
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_schema.py | sed -n '291,298p'
    # --- Step 5: validate optional linked_issue (Part B1, additive) ---
    linked_issue: Optional[str] = raw.get("linked_issue")
    if linked_issue is not None and not isinstance(linked_issue, str):
        _soft_error(...)
        return None
```
—— 先例只做 `isinstance` 检查, **没有**值域检查; 照抄先例的实现对 `track_form` 也只会做 `isinstance`。

**处方 (最省, 不引入复杂度)**:
1. Impact 表 `claim_schema.py` 行补一句: **`track_form` 落 `parse_claim` Step 5 同款校验, 且值必须 ∈ `{"issue","slug"}`, 否则整条 `return None` (与 status 越界同款处置, `:257-263` 有现成先例)** —— 这一条同时把 I-4 关成 fail-CLOSED;
2. I-1/I-3 各写成一条 `assert`-级的构造期不变量, 落在 `acquire_claim` 里 (它是唯一写入点), 并各配一条 SC 的「怎么会红」;
3. I-2 明确**不做**并成文为已知限 (强制它要在 release 侧重跑派生, 代价不划算) —— 但必须写出来, 别留在缝里。

---

## A-M4 (Major) — 不 bump `schema_version` 与 `coordination-ref-schema.md` §3.3 的**逐字**演进契约冲突; 且 Impact 没安排订正 §3 ⇒ 留下一颗「照文档办就炸」的雷

**问题的直接回答 (R4 任务问 1(c))**: **不相容 —— 与 §3.3 逐字冲突, 与 §3.1 只是「不冲突」而非「被允许」。**

**实跑**:

```
$ git -C aria show d50f9c3:skills/state-scanner/docs/coordination-ref-schema.md | sed -n '124,148p'
### 3.1 Current version lock
`schema_version: "1"` is locked. The field set defined in §2.1 is the v1 contract.
No new required fields may be added to v1 (doing so would break existing readers).
...
### 3.3 Introducing v2
Any field additions, semantic changes, or removals require:
- A new `schema_version` value (`"2"`)
- A new OpenSpec Spec proposal (at least Level 2)
- Updated reader logic in `claim_schema.py` with explicit version dispatch
```

- §3.3 逐字是 **"Any field additions ... require a new `schema_version` value"** —— **没有** optional/additive 的例外从句。
- §3.1 只禁 *required* 字段, 与 §3.3 **本身就互相矛盾**; 母 Spec 采的是 §3.1 的读法, 但**从未点名**这个矛盾, 也没引 §3.1 作依据。

**援引的先例经不起实读** (memory `exact-exception-condition` + `feedback_spec_precedent_verify_execution_history`):

```
$ git -C aria show d50f9c3:skills/state-scanner/docs/coordination-ref-schema.md | sed -n '51,62p' | grep -c linked_issue
0
```

—— `linked_issue` (母 Spec `:451` 逐字援引的「与 Part B1 引入 `linked_issue` 同款」那个先例)
**至今不在 §2.1 字段表里**。同段 §2.2 的 status 枚举 (`:64-71`) 也**没有 `abandoned`**, 而
`claim_schema.py:56` 的 `STATUS_ENUM` 有。⇒ 该「先例」不是一条被批准的 additive lane,
它只是**同一份文档已经漂移过一次**的证据。以未订正的漂移为先例, 等于把漂移制度化。

**活雷**: 文档留着 §3.3 那句, 而实际有 3 个字段活在 v1 外。下一个实现者照 §3.3 办 ⇒ 把
`schema_version` bump 到 `"2"` ⇒ `parse_claim` `:216-233` 对**每一条**老 claim 返回
`status="unknown"` 的哨兵 ⇒ 按 §3.2/§4.2 被 reconcile **全部跳过** ⇒ 整个协调机制静默死亡。

**处方 (字符级)**: Impact 表的 `coordination-ref-schema.md` 行**必须**增加 §3 的订正:
1. §3.1 与 §3.3 二选一措辞统一, 明确写出 **additive-optional 字段的演进 lane**
   (逐字建议: `Optional fields with a None default MAY be added within v1 provided (i) parse_claim
   ignores them when absent, (ii) serialize_claim omits them when None, and (iii) §2.1 is updated
   in the same change.`);
2. **回补 `linked_issue` 与 `abandoned` 两条既有漂移** —— 否则这条 lane 第一次被援引就带着两个反例;
3. 若 owner 认为 additive lane 不该开, 则本 Spec 必须走 v2 + `explicit version dispatch`,
   那是完全不同的工作量, 应上呈复议 (Rule #10)。

---

## A-M5 (Major) — Impact 表只给 `spec_slug` 安排了文档落点, `track_form` **零文档**; 且「§2.2 说明分工」指错了节

**定位**: 母 Spec Impact `:647`

```
$ sed -n '647p' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
| `skills/state-scanner/docs/coordination-ref-schema.md` (第二处变更) | §2.1 字段表增 `spec_slug` 行 + §2.2 说明其与 `track_id` 的分工 … |

$ git -C aria show d50f9c3:skills/state-scanner/docs/coordination-ref-schema.md | grep -n "^### 2\."
49:### 2.1 Field table
64:### 2.2 Status enum
73:### 2.3 Minimal complete example
87:### 2.4 Example with optional field (reconcile take-over)
102:### 2.5 Archived claim example (GC)
```

两处实质错误:
1. **`track_form` 不在任何文档变更行里** —— 两个字段同批引入, 只有一个进字段表。文档与 schema 当场不同步 (CLAUDE.md 不可协商规则 #3);
2. **§2.2 是 Status enum 表**, 不是字段语义节。把「`spec_slug` 与 `track_id` 的分工」写进状态枚举表, 是与 R3/KM-1 已经订正过的 `session-handoff.md §2.3` vs `§2.3.8` **完全同形**的引错节 (同一份 Spec 一轮内两次)。

**处方**: `:647` 逐字改为「**§2.1 字段表增 `spec_slug` 与 `track_form` 两行** (含 `track_form` 的值域
`"issue"|"slug"`, Required=NO); **§2.3 最小示例后新增 §2.6「字段分工」** 说明 `track_id` 承载「哪条 issue」、
`spec_slug` 承载「哪个方向」、`track_form` 承载「哪种派生形态」」。

---

## A-M6 (Major) — 「不传时行为逐字节不变 ⇒ Phase B/D 既有调用零影响」的**后半句为假**; `--spec-slug` 的 CLI 默认值未钉

**问题的直接回答 (R4 任务问 2)**: **前半句成立, 后半句不成立。**

**实读** `release_claim_by_track` 全函数 (`claim_lifecycle.py:377-472`):
定位谓词是 `:422-428` 的三条件列表推导 (`container` / `track_id == norm` / `status == "active"`)。
加一个 keyword-only `spec_slug: Optional[str] = None` 并在 `spec_slug is not None` 时追加一条过滤,
**对不传该参数的调用者确实逐字节不变** —— 我的实跑 A 臂与 baseline 输出完全相同 (见 A-C2 的实跑块)。
所以「函数级不变」这半是**成立**的。

**但同一行下面紧接着的 Impact 行推翻了「Phase D 零影响」**:

```
$ sed -n '646p' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
| `skills/phase-d-closer/SKILL.md` (第二处变更) | D.2b 的 `release_gate.py` 命令模板增 `--spec-slug "<本 cycle 的 spec 目录名>"` …
```

⇒ Phase D 的**唯一**生产调用路径被同一份 Spec 改成了**总是传**该参数。「Phase B/D 既有调用零影响」
在 D 那一侧是空集上的真命题, 读起来却像「D 不受影响」—— 而 D 恰恰是受影响最大的那一侧
(见 A-C2 的 C 臂: 存量 claim 直接 `claim_not_found`)。

**另一处未钉**: `release_gate.py` 新增 `--spec-slug` 的 **argparse 默认值**全文未定。若实现写
`default=""` 而非 `default=None`, 则 `spec_slug is None` 判否 ⇒ 过滤器以空串生效 ⇒ **一条都匹配不到**,
且不传参数时也如此 ⇒ 「不传时逐字节不变」当场失效。这是一个字符级的、两个实现者会写反的点。

**处方**:
1. `:453` 的「故 **Phase B/D 既有调用零影响**」逐字改为「**Phase B 侧零影响**; **Phase D 侧本 Spec 主动改模板,
   其行为变化由 SC-27(C) 与 A-C2 处方的新 SC 覆盖」;
2. `:645` 的 `release_gate.py` 行补一句逐字: 「`--spec-slug` 的 argparse **`default=None`**
   (不得用 `""`); `release_claim_by_track` 内的判据是 **`if spec_slug is not None:`** (不得用 truthiness)」。

---

## A-M7 (Major — ✅ **已由并发 R4 席位闭环, 不计入 open counts**; 保留正文因其第二半未被处置) — §5.3 里标为「逐字」的 docstring 引用是**伪造的**; 源码无 `same session` 字样, 原文语义相反, 且删掉了 review I1 的理据

**定位**: §5.3 `:441`

**实跑**:

```
$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py | grep -n "same session"
(零命中)

$ git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py | sed -n '396,400p'
    the caller passes the raw carry-id. If several active claims match (same
    container re-claimed a track across sessions — the NORMAL case, since
    every session mints a fresh session_id and B.0 REQUIRE-claim runs per
    session), **ALL matching active claims are released** (review I1: releasing
    only the earliest would leave the later session-claims active and the
```

Spec 写的是「If several active claims match (**same session**), ALL matching active claims are released」
并标「docstring **逐字**写着 … 实读基线 `d50f9c3`」。源码是「(**same container re-claimed a track
across sessions**」—— 括号里的限定词被换成了**意思相反**的一个, 而这句话正是整条 R3/TL-C1 与
新增 `spec_slug` 字段的全部依据。

**更实质的一半**: 被截掉的 `(review I1: …)` 从句正是**反对**收窄 release 作用域的理据 ——
它说明 ALL-matching 的设计意图是「同一条轨跨 session 累积的多条 claim 必须一起释放, 否则 ship
之后 track 仍读作 occupied」。母 Spec 引结论、弃理据 (memory `narrow-owner-options` 的第二形态),
而这条理据恰恰是 A-C1 里 heartbeat 掉字段之后会复发的那个缺陷。

**处方**: `:441` 三行逐字替换为上面 `sed -n '396,400p'` 的原文 (含 `review I1` 从句),
并在 §5.3 新增一段: 「**`spec_slug` 过滤不得破坏 review I1 的性质** —— 同一方向跨 session 的多条 claim
共享同一 `spec_slug`, 故仍会被一并释放; 该性质的前提是 `spec_slug` **在 claim 的整个生命周期内不被抹掉**
(见 A-C1 处方 1/2)。」

---

## A-m1 (minor) — 「新表面」7 条自述与实际不一致 2 处

`:754` 自述「`release_claim_by_track` 增 keyword-only `spec_slug` 过滤 —— 声称「不传时行为逐字节不变」,
**未实测**」。本席已实测 (见 A-M6): 函数级成立。建议把该行改为「函数级已由 R4 实测成立;
未成立的是同条的『Phase B/D 既有调用零影响』」。
`:753` (b) 自述「fail-CLOSED 退化 … 是否**真的比连坐更安全**」—— 本席判定见 A-C2: 它**就是**连坐, 措辞需改。

---

# B. 字段 Spec — `linked-issue-field-availability` (R2)

**verdict: REVISE** · **counts: 1 Critical / 4 Major / 1 minor**

## B-C1 (Critical) — §1 引入的 SOT 模板 placeholder 会判 `BAD_TOKEN`, 而 **E6 没有 verdict 门** ⇒ 未填写的模板值被逐字节喂进 `--linked-issue` ⇒ **NEW-01 原样复现, 且比 `无` 更容易触发**

**定位**: §1 `:116` / D8 `:434` / Impact `:503` (模板 placeholder) × E6 `:193` (实参规则) × `:240` (「只有它可以喂 `--linked-issue`」)

**实跑 1 — 模板 placeholder 过 E0–E6 得什么态** (E0–E6 原型按 §3 逐字实现):

```
$ python3 e0e6.py <一份从 SOT 模板复制、未填写的 proposal>
verdict/token/elems/line = ('BAD_TOKEN', '{<org>/<repo>#<n>}', ['{<org>/<repo>#<n>}'], 6)
E6 says --linked-issue arg = 第一个 token 元素逐字节 = '{<org>/<repo>#<n>}'
```

**实跑 2 — 把它喂进真实的主机制** (代码取自 `d50f9c3` 的 `lib/collision.py`, 未改一行):

```
normalize(placeholder) = None
normalize('无')        = None
overlaps(two unfilled-placeholder specs) = [{'track_id': 'spec-b-uuid2', 'owner': 'o',
  'container': 'c', 'session': 'sspec-b-uuid2', 'status': 'active',
  'linked_issue': '{<org>/<repo>#<n>}', 'claimed_at': '2026-08-25T00:00:00Z'}]
```

**机制逐字**: `collision.py:219-227` 的 `_linked_issue_matches` ——
`"""Rule 4/5: exact key equality when BOTH parse, else exact raw equality."""` ——
`own_key is None` ⇒ 回落**原串相等**。而 placeholder 是一个**所有从模板复制的 proposal 共享的常量**。
⇒ **两份毫无关系的 Spec 只要都没填模板占位符, 就会互相命中 overlap** —— 与母 Spec §2 的
NEW-01 (`无` 互相命中) **是同一个缺陷**, 而且触发条件更弱: `无` 要人主动写, placeholder 是**什么都不做**的默认。

**E6 的漏洞是字符级的**: `:193` 逐字「E6 — `--linked-issue` 实参: = **第一个 token 元素逐字节**,
不做二次加工; **且 token 串逐字节等于 `无` 时整个 `--linked-issue` 参数省略**」——
**只对 `无` 设门, 对 `BAD_TOKEN` / `NO_TOKEN` 无门**。这直接反驳了同文件 `:240` 的自述
「本 Spec 的抽取器**只产出** canonical token, 且**只有它**可以喂 `--linked-issue`」。

**跨 Spec 传播**: 探针侧同样中招 —— `sibling-spec-probe` §3 对 `BAD_TOKEN` 走「层 1 ∪ 层 2」,
层 1 对不可解析元素产出**原串键** `("r", "{<org>/<repo>#<n>}")`。两份未填模板的 proposal
⇒ 原串键逐字节相同 ⇒ 集合求交非空 ⇒ **探针报「同 issue 竞品」**。见 C-M3。

**处方 (字符级, 三条缺一不可)**:
1. **E6 增 verdict 门**, 逐字: 「**当且仅当 `verdict == "OK"` 且 token 串不逐字节等于 `无` 时**,
   `--linked-issue` 实参 = 第一个 token 元素逐字节; **其余三态 (`NO_FIELD` / `NO_TOKEN` / `BAD_TOKEN`)
   与 `无` 分支一律省略整个 `--linked-issue` 参数**」;
2. **D8 的 placeholder 换成不含 `#` 的形态** (例如 `` `TODO-org/repo-number` ``) ——
   实测 `normalize_linked_issue` 的第 (i) 类回落 (`"#" not in value`) 与第 (ii)(iii) 类同样返回 `None`,
   但**不含 `#` 的串在 E2/E3 之后仍会落 BAD_TOKEN**, 所以换 placeholder **只是减害不是根治**;
   根治靠第 1 条。二者都要;
3. **新增一条 SC** (追加编号): 夹具 = 两份从 SOT 模板复制、`关联 Issue` 行**逐字保持 placeholder** 的 proposal,
   断言 (a) 两份各判 `BAD_TOKEN`; (b) **两份都不产生 `--linked-issue` 实参**;
   (c) 经真实 `linked_issue_overlaps` 跑一遍 ⇒ **overlap 为空**。**baseline 必红** (今天没有实现),
   且「E6 不设 verdict 门」的坏实现在 (b)(c) 上必红。

---

## B-M1 (Major) — `FieldVerdict` 只在 docstring 里出现过一次, **没有类型声明、没有 per-verdict 字段填充契约** —— 而探针今天 100% 的路径依赖 `line_no` 在 `NO_TOKEN`/`BAD_TOKEN` 下必填

**定位**: §3 `:205-215` (docstring) / Impact `:501` · 探针侧 `:136` / §7 `:301`

**实跑**:

```
$ grep -n "FieldVerdict\|line_no\|token_elements\|token_str" openspec/changes/linked-issue-field-availability/proposal.md
205:> def extract_linked_issue_field(text: str) -> "FieldVerdict":
208:>     返回 FieldVerdict(verdict, token_str, token_elements, line_no)
501:| **`aria/skills/state-scanner/lib/linked_issue_field.py`** (**新建**) | …

$ grep -n "FieldVerdict\|line_no\|token_elements\|token_str\|field_line" openspec/changes/sibling-spec-probe/proposal.md
136:> **处置**: 姊妹 Spec 已同批承诺 … `extract_linked_issue_field(text: str) -> FieldVerdict` …
301:| `hits` | `list[obj]` | … 每项 … `field_line` (`int`) … |
```

⇒ 这个**跨两份 Spec 的共享类型**的全部规格 = 一行 docstring 里的四个位置参数名。缺:
`dataclass` 还是 `NamedTuple`、是否 frozen、四个字段各自的类型、**以及每个 verdict 下哪些字段有值**。

**为什么它承重**: 探针 §3 层 2 要「从该 proposal 的**字段行本身**提取 URL 片段」, 但探针被
`:133` 逐字禁止内含第二份定位实现 (「**本 Spec 不得内含第二份抽取实现 (E0–E6 一条都不复制)**」)
⇒ 它拿到字段行的**唯一**途径是 `FieldVerdict.line_no` 去切 blob。
而层 2 的触发集逐字是 `{NO_TOKEN, BAD_TOKEN}` —— 恰恰是**没有 token 的那两态**。
一个完全合规的实现返回 `FieldVerdict("NO_TOKEN", None, None, None)`, 探针层 2 就**无法实现**。
探针 `:139` 又逐字自陈「姊妹未 ship 时 … **全部依赖层 2**」且实测基线上
「冒号后第一个非空白字符是反引号的 **= 0 行**」⇒ **层 2 是今天唯一有产出的路径**。

**处方 (字符级)**: §3 的 R3/C3 段把 `FieldVerdict` 写成一张**按 verdict 分档的字段填充表**, 逐格钉死:

| verdict | `token_str` | `token_elements` | `line_no` |
|---|---|---|---|
| `NO_FIELD` | `None` | `None` | `None` |
| `NO_TOKEN` | `None` | `None` | **必填 (int, 1-based)** |
| `BAD_TOKEN` | **必填** | **必填 (非空 list)** | **必填** |
| `OK` | **必填** | **必填 (非空 list)** | **必填** |

并声明 `@dataclass(frozen=True)`; 追加一条 SC 断言这四行 (**每一格**都要断言, 含 `None` 的格 ——
否则「填了不该填的」这类实现测不出来)。

---

## B-M2 (Major) — `无` 子态只活在散文里, 四态表**没有它的格**; 而探针的层 1 / 层 1.5 二分完全靠它

**问题的直接回答 (R4 任务问 3 末段)**: **有 —— `OK` 内部的 `无` vs 真 token 二分, 只在 E5 散文与跨 Spec 对照表里出现, 从未进入本 Spec 自己的四态判定表, 也没有任何 SC 断言它借以二分的那个字段。**

**实读**: §3「四态判定 (穷尽, 无第五态)」表 (`:222-227`) 的 `OK` 行, 触发列逐字是
「E5 满足 (含 `无` 分支)」—— `无` 被**折叠**进 `OK`, 表里没有任何列区分二者。
探针 §3 `:116` 逐字要求「**`OK` 的两分靠什么区分要写死**: 靠**姊妹 E3 的 token 串本身**逐字节比 `无`」
⇒ 依赖 `FieldVerdict.token_str` 在 `OK` 下必填 —— 而这一点从未成文 (见 B-M1)。
SC-4(a) `:474` 断言的是**后果**「不产生任何 `--linked-issue` 实参」, **不是** `token_str` 的取值。

**处方**: 四态表加一列「`token_str` 取值」, `OK` 行拆成两行 (`OK · token_str == "无"` /
`OK · 其余`), 与探针 §3 的映射表**逐格同构**; SC-4(a) 的「期望」列补一句
「且 `FieldVerdict.token_str` 逐字节 == `无`」。

---

## B-M3 (Major) — SC-5(e)「白名单文件不存在 ⇒ **不得 exit 1**」在本仓语料上**为假**, 且与同文件 SC-8(c) 自陈的纪律正相反; 照字面实现会造出一个**真正的** fail-open

**定位**: SC-5(e) `:478` vs SC-8(c) `:481`

**实跑** (E0–E6 原型跑 `openspec/changes/` 全部 9 份):

```
OK         line=12    tok='无'    openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m6-cost-model-telemetry/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m6-dispatch-input-delivery/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m6-e2e-resilience/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m6-release-closeout/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md
NO_FIELD   line=None  tok=None    openspec/changes/aria-2.0-m7-fleet-aggregation/proposal.md
OK         line=6     tok='无'    openspec/changes/linked-issue-field-availability/proposal.md
OK         line=6     tok='无'    openspec/changes/sibling-spec-probe/proposal.md
```

(顺带: 这与 §5 表的 3 `OK` / 6 `NO_FIELD` **逐份一致** —— 该表本席复核通过。)

⇒ 在 **Aria 本仓**, `--grandfathered` 指向的文件不存在 ⇒ 白名单空集 ⇒ 6 份 `NO_FIELD`
落「不在册」臂 ⇒ **正确行为就是 `exit 1`**。SC-5(e) 却把「**不得 `exit 1`**」写成期望值。

同一段 SC-8(c) `:481` 逐字自陈相反纪律: 「⚠️ (c) **不断言 exit 值本身** ——
断言值就把测试绑死在当日语料上」。SC-5(e) 犯的正是它点名的病。

**更实的危害**: 一个实现者照 SC-5(e) 字面办, 最省的实现是「白名单文件缺失 ⇒ 跳过全部判定 ⇒ exit 0」
—— 那**才是**真正的 fail-open, 而且是这条 SC 亲手教出来的。

**处方 (字符级)**: SC-5(e) 的期望列逐字改为:
「⇒ 白名单视为**空集**, 探针**正常判定作用域内 proposal**; **不得**以 `##SKIP##` / 非 `{0,1}` 退出码
表达『白名单文件缺失』, **也不得**因该缺失而放行任何不合规 proposal。
**断言方式**: 同一夹具仓在 (i) 白名单文件存在且含该 path 与 (ii) 文件不存在 两种情形下,
**stdout 首行分别为 `OK` 与 `FAIL` 且 FAIL 点名该 path** —— 断言的是**两臂之差**, 不是绝对 exit 值。」

---

## B-M4 (Major) — 「新表面 #4」把自己的 fail-open **定位错了**: 「文件不存在 ⇒ 空集」是 fail-CLOSED; 真正无守卫的是 **allowlist 的增长**

**定位**: 「新表面 (未审)」第 2 条 `:527` · §4 R3/C2 段 `:335-345` · 探针判据分割表 `:365` · 母 Spec 交给 R4 的清单第 4 条

**判定 (R4 任务问 4 的直接回答)**: **「文件不存在 ⇒ 空集而非错误」不是 fail-open, 它是正确的 fail-CLOSED**
—— 空白名单 = 作用域内**所有** proposal 都必须合规 = 最严, 且在本仓会立刻变红 (上面的实跑证明:
6 份 `NO_FIELD` 无一在册)。失效模式是**吵**不是**静默**, 方向正确, 该例外**已被正当化**。

**但同一段里有一个真的 fail-open, 而 Spec 没看见它**: 白名单的**陈旧守卫**有三个子情形
(`:365` 逐字 (a) 路径不存在 / (b) 已移出作用域 / (c) 已合规), 三条**全部只检查已在册的条目**。
**没有任何一条守卫「新增条目」**。⇒ `.aria/linked-issue-field-grandfathered.txt` 是一个
**AI 可写、一行即生效、零留痕、零上限**的逐项豁免通道; 而 `:409` 的自陈
「**新建的 proposal 一律不在册, 必须合规**」是一条**纯散文不变量**, 无任何机械回声。
这与 CLAUDE.md 不可协商规则 #10 + memory `no-self-exempt-gates` 的极性正相反 ——
enabled 闸门的豁免不该有一条 AI 单方面可写的旁路。

**处方 (字符级, 低成本)**:
1. 白名单文件头部加一行**机读封印**: `# frozen-at: <ISO8601> count: 6` , 探针断言
   「实际行数 > `count`」⇒ `FAIL allowlist 增长: 新增 <path> (需 owner 批准, 见 O-1)」——
   把「只减不增」从散文变成一条会红的量 (memory `redfix-change-quantity`: 换量, 不调阈值);
2. 「新表面 #4」逐字改写为: 「『文件不存在 ⇒ 空集』经 R4 复核**是 fail-CLOSED, 方向正确**;
   本条真正未守卫的是 **allowlist 的增长**, 处置见上」;
3. O-1 的表述补一句: allowlist 的**任何新增**都须 owner 批准, 与「回填一份删一条」构成双向约束。

---

## B-m1 (minor) — `severity: warning` 下 `exit 1` 的语义未成文

`:352` 的 check 骨架是 `severity: warning`, 而探针判据表 (`:362-367`) 用 `exit 1` 表达 FAIL。
custom check 框架把 `exit 1` + `severity: warning` 渲染成什么 (阻断/黄/红) 全文未验也未引。
建议 §4 补一句实读锚点, 或在 A.2 列为验收项 —— 与「`${CLAUDE_PLUGIN_ROOT}` 是否导出」那条同款处理。

---

# C. 探针 Spec — `sibling-spec-probe` (R2)

**verdict: REVISE** · **counts: 0 Critical / 3 Major / 1 minor**

## 先回答 R4 任务问 3 的前两问

**逐格映射是全函数吗?** —— **是。** 姊妹四态 (`NO_FIELD` / `NO_TOKEN` / `BAD_TOKEN` / `OK`) 在 §3 `:107-113`
的表里共 5 行 (`OK` 按「token 串是否逐字节等于 `无`」再分二), 每个输入态**都有像**, 无遗漏。
**无歧义吗?** —— **是。** 五行的判据两两互斥, `OK` 的二分依据是一个可判定的字节比较, 且 `:116`
明文禁止用「归一结果」或「集合是否为空」来分 (后者会把 `wu_empty` 误送 URL 回落, SC-10 专钉这条)。
**⇒ 映射本身是本轮三份 Spec 里质量最高的一块。** 但它有下面三条实质缺陷。

## C-M1 (Major) — `BAD_TOKEN` 的枚举值在两节里拼写不同 (`"bad_token"` vs `"bad_token_union"`) —— R3/TL-P2 只修了一侧, 它要治的病原样存在

**实跑**:

```
$ grep -no 'bad_token_union\|"bad_token"' openspec/changes/sibling-spec-probe/proposal.md
111:"bad_token"
298:bad_token_union
```

`:111` 是 §3 映射表 —— **实现者据以产出**枚举值的那张表, 列头逐字是
「`own_layer` / `hits[].layer` 枚举值」。
`:298` 是 §7 输出契约 —— **消费方据以穷尽匹配**的那个枚举, 并逐字写着 TL-P2 的修复理由:
「该取值原未传导进本枚举 ⇒ **消费方按 5 值枚举做穷尽匹配时会落空**; 现补为第 6 值」。

⇒ 修复只落在消费侧, **产出侧仍写 `"bad_token"`** ⇒ 实现者按 §3 产出 `"bad_token"`,
消费方按 §7 穷尽匹配 6 值 ⇒ **原样落空**。TL-P2 点名的那个后果一字未改地保留了下来。
这是 memory `fix-the-class` 与 `redfix-change-quantity` 的同形复现 (改了一处, 没扫兄弟位置)。

**处方**: `:111` 最后一列逐字改为 `` `"bad_token_union"` ``; 并在 §7 的 `own_layer` 行末补一句
「**本枚举与 §3 映射表末列是同一份 SOT, 任一被改必须同批改另一侧**」;
SC-18 或新增一条 SC 加一臂: 断言 §3 表末列与 §7 枚举**字面集合相等** (可机械: 从两处 grep 出集合比对)。

## C-M2 (Major) — `wu_empty` (正证据) 被强制落 `verdict="not_established"` + `reason="own_token_absent"` —— 正是 §7 自称承重条款要防的「零证据当正证据」的镜像; 且 SC-11 只覆盖 `own_layer`, 不覆盖 `verdict`/`reason`

**定位**: §7 `:296` (`reason` 枚举) / `:307` (`verdict` 取值表) · SC-11 `:452`

**实读**: `verdict` 表逐字「`"not_established"` | 其余全部情形 —— **含 `own_keys` 为空 (本轨无可比较的输入)**…」。
`wu_empty` 的定义 (§3 层 1.5) 就是 `own_keys = ∅`。
`reason` 的枚举只有 5 个值: `"no_enforced_remote"` / `"remote_unresolved"` / `"fetch_failed"` /
`"cap_applied"` / `"own_token_absent"` —— 且 `:296` 逐字规定 `verdict == "not_established"` 时 `reason` **必非空**。
⇒ 一份写了 `` `无` `` 的 proposal (**已核实无关联** = 正证据) 只能被标成 `own_token_absent`
(**没取到 token** = 零证据)。而 §3 层 1.5 `:145` 逐字说这两者「是两回事, **不得**合并处置」,
§7 `:311` 又逐字说「让消费方从它推断结论, 就是把**零证据当正证据**」。
**同一份 Spec 在 `own_layer` 上分得清清楚楚, 在 `verdict`/`reason` 上又亲手合并了回去。**

SC-11 `:452` 的期望列逐字只到「`layer` 必须可辨: `"wu_empty"` vs `"no_field"`」——
**不覆盖** `verdict` 与 `reason`, 所以这个合并没有任何断言会为它变红。

**处方 (字符级)**:
1. `reason` 枚举增第 6 值 **`"own_no_linked_issue"`** (语义: 本轨已核实无关联 issue, 正证据),
   并在 `:296` 补一句「`own_layer == "wu_empty"` 时 `reason` **必须**取该值, **不得**取 `"own_token_absent"`」;
2. SC-11 的期望列补第二句: 「且两者的 `reason` 必须可辨: `"own_no_linked_issue"` vs `"own_token_absent"`;
   把二者折叠成同一 `reason` 的实现必红」。

## C-M3 (Major) — 层 1 的**原串键** `("r", t)` 对「常量串」无任何守卫 ⇒ SOT 模板未填写的 placeholder 会让**任意两份**未填模板的 proposal 互相命中

**定位**: §3「比较键的构造」`:164-172` · 层 1.5 `:141-148` · 姊妹 D8 `:434`

这是 B-C1 在探针侧的落点, **但需要探针侧独立修**, 故单列。

**逐字机制**: `:167-168` 的构造规则是「`键 = ("r", t)` 若 `k is None` (原串键, fail-toward-reporting)」;
`:170` 逐字「归一失败的值只与**逐字节相同**的另一个归一失败值命中」。
层 1.5 之所以存在, 正是因为 `无` 是一个**所有人都会写成同一个字节串**的常量
(`:148` 逐字「若把 `无` 当普通 token 送进比较 … `"无" == "无"` ⇒ **两份 `无` 互相命中**。
层 1.5 缺席时的失效是**必然的, 不是概率的**」)。

**姊妹 Spec 刚好又引入了第二个这样的常量**: SOT 模板的 placeholder
`` `{<org>/<repo>#<n>}` `` (姊妹 `:116` / `:434` / `:503`)。本席实跑确认它判 `BAD_TOKEN`
(见 B-C1), 于是走「层 1 ∪ 层 2」⇒ 层 1 产出原串键 `("r", "{<org>/<repo>#<n>}")`。
**任意两份从模板复制而未填写的 proposal ⇒ 键逐字节相同 ⇒ 集合求交非空 ⇒ 探针报「同 issue 竞品」。**
层 1.5 的那句「失效是必然的, 不是概率的」**逐字适用于这个新常量**。

**处方 (字符级, 与姊妹侧的修法互补而非替代)**:
1. §3「比较键的构造」增一条: 「**原串键的 `t` 逐字节命中『非标识常量集』时, 不产生任何键**
   (等同层 1.5 的 ∅ 处置)。该集合逐字 = `{"无", "TBD", "N/A", <姊妹 D8 的模板 placeholder 逐字串>}`,
   **集合本体由姊妹 Spec 的 §2 维护, 本 Spec import 之, 不另立**」;
2. 层 1.5 改名为「**非标识常量层**」并把 `无` 表述为它的第一个成员 —— 这样下一个常量出现时,
   处置位置是现成的, 不必再造一层 (memory `fix-the-class`: 修类不修实例);
3. 新增一条 SC: 两份 proposal 的字段行**都逐字保持模板 placeholder** ⇒ **不命中**,
   且两者 `own_layer` 可辨于 `canonical`。**baseline 必红**(今天的规则会命中)。

## C-m1 (minor) — §3 表末列的列头写「`own_layer` / `hits[].layer` 枚举值」, 但 `no_token_no_url` 只在括注里

`:110` 的 `NO_TOKEN` 行末列写「`"url_fallback"` (无片段时 `"no_token_no_url"`)」——
一个格里塞了两个取值, 与其余四行「一格一值」的体例不一致, 且「无片段」这个附加判据没进
「附加判据」列 (该列此处是 `—`)。建议把 `NO_TOKEN` 拆成两行 (`附加判据` = 「字段行含 ≥1 个
`/<org>/<repo>/issues/<n>` 片段」/「无片段」), 与 `OK` 的两行同构。这样表就是**逐格**的, 名副其实。

---

# D. 联审 (combined) — 跨三份 Spec 的接缝

**combined verdict: REVISE** · **combined counts: 3 Critical / 14 Major / 3 minor**

| # | 接缝 | 三份的立场 | 判定 |
|---|---|---|---|
| X-1 | 未填写的 SOT 模板 placeholder | 字段 Spec: 引入它, E6 无 verdict 门 (B-C1); 母 Spec: §2 只对 `无` 设省略规则; 探针: 原串键无常量守卫 (C-M3) | **三侧同时漏**。母 Spec §2 的 NEW-01 段与 §6 缺口表首行都只写了 `无`, 需同批补 placeholder/BAD_TOKEN 一档 |
| X-2 | `FieldVerdict` 的字段填充契约 | 字段 Spec 只给了一行 docstring (B-M1); 探针 §7 的 `hits[].field_line` 只能来自它 | **产者未承诺, 消者已依赖**。修法落在字段 Spec, 但探针 §3 须同批加一句「本 Spec 依赖 `line_no` 在 `NO_TOKEN`/`BAD_TOKEN` 下必填」 |
| X-3 | 四态 ↔ 层枚举 | 映射本身全函数、无歧义 (质量最高的一块), 但产出侧/消费侧枚举拼写不一 (C-M1) | 一个 token 的修法, 但必须两侧同批 |
| X-4 | 「fail-CLOSED」这个词在三份里指三件事 | 母 Spec: 不确定时**释放全部** (A-C2, 实为 fail-OPEN); 字段 Spec: 白名单封闭枚举 + 其余阻断 (真 fail-CLOSED); 探针: 默认分支解析不出就不扫 (真 fail-CLOSED) | 建议三份统一一句判据: 「**fail-CLOSED = 不确定时不执行有副作用的动作**」, 并按此复查每一处该词 |

**scope_ok 说明**: 三份均未越出各自声明的 scope; 母 Spec 的迁出边界 (§1/§4) 与两子 Spec 的承接
本席按 R3 遗留项 #6 抽查了 C-A (抽取规则) / M-1 (匹配谓词) 两条 —— **两条都真的被接住了**
(字段 §3 的 E0–E6、探针 §3 的层 0–3 与键构造), 不是「迁出变丢弃」。

---

# E. 我实读证伪了哪些文档断言

| # | 文档断言 | 实读结果 | 落在哪条 |
|---|---|---|---|
| 1 | 母 §5.3 `:441`「`release_claim_by_track` 的 docstring **逐字**写着『If several active claims match (**same session**)…』」 | `grep -n "same session"` 在该文件 **零命中**; 原文是「(same container re-claimed a track **across sessions**」, 且被截掉了 `review I1` 从句 | A-M7 |
| 2 | 母 §5.1 `:419`「SC-1 / SC-15 / SC-27 三处一律按该字段 (`track_form`) 判」 | `grep -n track_form` 在 SC 表区间 (`:567`-`:614`) **零命中**; 三条 SC 全在用被否决的字符串形态谓词 | A-M2 |
| 3 | 母 §5.3 `:453`「未传该参数时行为逐字节不变, 故 **Phase B/D 既有调用零影响**」 | 前半句实测**成立**; 后半句为假 —— 同表 `:646` 把 phase-d-closer 的模板改成**总是传** | A-M6 |
| 4 | 母 `:451`「与 Part B1 引入 `linked_issue` **同款**: 不 bump `schema_version`」 | 该先例**从未**回补 §2.1 字段表 (`sed -n '51,62p' \| grep -c linked_issue` = 0), §2.2 也缺 `abandoned` ⇒ 先例=既存漂移, 不是已批准 lane; 且与 §3.3 逐字「Any field additions … require a new schema_version」冲突 | A-M4 |
| 5 | 母 Impact `:647`「§2.2 说明其与 `track_id` 的分工」 | §2.2 实为 `Status enum` 表 (`grep -n "^### 2\."`), 指错节; 且 `track_form` 无任何文档落点 | A-M5 |
| 6 | 母「新表面」`:754`「`spec_slug` 过滤 … **未实测**」 | 本轮已实测: 函数级「不传时不变」成立 | A-m1 |
| 7 | 字段 §3 `:240`「本 Spec 的抽取器**只产出** canonical token, 且**只有它**可以喂 `--linked-issue`」 | E6 `:193` 逐字**只对 `无` 设门**; 实跑证明 `BAD_TOKEN` 的第一个元素照样被 E6 取作实参 | B-C1 |
| 8 | 字段「新表面 #4」「『文件不存在 ⇒ 空集』这条 **fail-open** 方向的选择」 | 它是 **fail-CLOSED** (空白名单 = 最严, 且本仓实跑会立刻红); 真正的 fail-open 是 allowlist 的**增长**无守卫 | B-M4 |
| 9 | 字段 SC-5(e)「文件不存在 ⇒ … **不得 `exit 1`**」 | 本仓实跑 6 份 `NO_FIELD` + 空白名单 ⇒ 正确行为**就是** exit 1; 且与同文件 SC-8(c) 自陈纪律相反 | B-M3 |
| 10 | 探针 §7 `:298` (R3/TL-P2)「现补为第 6 值」⇒ 隐含「穷尽匹配落空已解决」 | §3 `:111` 仍写 `"bad_token"`, 两处拼写不同, 该后果原样存在 | C-M1 |
| 11 | 字段 §5 的 9 份逐份判定表 (3 `OK` / 6 `NO_FIELD`) | **复核通过** —— E0–E6 原型实跑逐份一致 (这一条是**证实**, 不是证伪, 列此备查) | B-M3 实跑块 |

---

# F. 我没能核实的部分 (诚实声明)

1. **`phase1_gate.py` 的 `:1230` / `:1233` / `:1236-1238` 三处行号**本轮**未逐行实读** ——
   它们不在我的镜头 (类型契约) 的承重路径上, 我只核了 `collision.py` 与 `claim_lifecycle.py`
   与 `claim_schema.py`。这三处的行号断言**留给其他席位**。
2. **`--spec-slug` 过滤器的真实端到端行为**未跑 —— 我跑的是**按 §5.3 逐字实现的谓词模拟**
   (与 `claim_lifecycle.py:422-428` 的基线谓词并列对照), 不是打了 patch 的真 `release_claim_by_track`
   (它要 git orphan ref 与 `write_claim` 的完整环境)。**A-C2 的矛盾结论不依赖这一步**
   (矛盾在两段规格文本之间, 模拟只是把它可视化); 但「打完 patch 后是否还有别的副作用」我没验。
3. **`custom_checks.py` 的 minimal YAML parser 对未知键 / `severity: warning` × `exit 1` 的渲染**未跑
   —— 与字段 Spec 自己的「新表面 #6」同一条未验事实 (B-m1)。
4. **两处 SKILL.md (`phase-a-planner` / `spec-drafter`) 的 `allowed-tools` frontmatter**未复读 ——
   母 Spec 声称 rework v3 已在 `d50f9c3` 上复读且逐字未变, 我**没有独立复核**这条。
5. **AB 套件实存性** (`ab-suite/spec-drafter.json` 的 2 条 eval / `phase-a-planner.json`) 未核 ——
   属 Rule #6 镜头, 不在本席范围。
6. **审计轨三个文件** (`.aria/audit-reports/*-audit-trail.md`) 的内容与「按字节搬运」自述未核 ——
   母 Spec 自己已把 §5 的搬运性质订正为「不是纯搬运」, 我未再独立 diff。
