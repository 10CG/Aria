---
checkpoint: post_spec
round: 4
role: pr-test-analyzer
verdict: REVISE
scope_ok: true
counts:
  combined: { critical: 4, major: 11, minor: 6 }
  a1-entry-claim-duplicate-work-guard: { verdict: REVISE, scope_ok: true, critical: 4, major: 5, minor: 2 }
  linked-issue-field-availability: { verdict: REVISE, scope_ok: true, critical: 0, major: 2, minor: 2 }
  sibling-spec-probe: { verdict: REVISE, scope_ok: true, critical: 0, major: 4, minor: 2 }
---

# post_spec R4 — 验收断言覆盖质量 (pr-test-analyzer 席)

**镜头**: 三份 Spec 的 Success Criteria 作为「测试」的质量 —— 宿主是否存在 / baseline 是红是绿 (实读判定, 不采信 Spec 自述) / 它怎么会红 / 恒绿·恒红风险。
**基线**: aria `origin/master` = `d50f9c3` (`git -C aria show d50f9c3:<path>`)。主仓 HEAD `322f280`。语料基线 `cc1bdef`。
**上一轮**: `post_spec-R3-1787652625000-a1-entry-rework-v3-combined-aggregated.md`。

## 主控本轮两项补强的验收结论 (先答被点名的两条)

| R3 finding | 主控处方 | **R4 判定** |
|---|---|---|
| **SC-2 恒绿** | 夹具须由「§2.1a 的 compose 函数」派生 + 加容器段置空负控臂 | ❌ **未生效, 恒绿原样存在** (C-1, 已实跑证伪) |
| **SC-7 恒绿** | 加第二臂 (调 by-track heartbeat 变体后再 sweep) | ✅ **生效** (baseline 红, 因该变体今日不存在); 但第二臂未钉 fresh session ⇒ 分辨力不足 (M-6) |

---

# CRITICAL

## C-1 — SC-2 的「恒绿已堵」是无效补强: **两臂在 baseline 全绿 (实跑证)**

**severity: critical** · grep: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:563`

R3 判 SC-2 恒绿, 处方是「夹具必须由 compose 函数派生 + 加容器段置空的负控臂 (ii)」。我按该处方逐字构造了两臂, 在 **零生产改动的 `d50f9c3` 上实跑**:

```
$ cd /home/dev/Aria/aria/skills/state-scanner && python3 - <<'EOF'
  ... acquire_claim(B, linked_issue=ISS)  # B 容器
  ... phase1_gate.py --raw-track-id A --linked-issue ISS   # A 容器, CLI 全链路
  ... linked_issue_overlaps(read_claims(repo).claims, B, ISS)  # 反向
EOF
arm(i)  container segs PRESENT : A->['aria-plugin-122-bbbbbbbb']  B->['aria-plugin-122-aaaaaaaa']
arm(ii) container segs EMPTIED: A->[]  B->[]
```

- **臂 (i)「双方 overlap 各含对方」= 今天就绿**;
- **臂 (ii)「容器段置空 ⇒ 双方 overlap 变空」= 今天也绿**。

**为什么补强必然无效**: 补强改的是**夹具的出处措辞**, 没有换**被测的量**。SC-2 度量的仍然是 `linked_issue_overlaps` 对「两个字符串相同 / 不同」的既有行为 —— 而那两条行为在 `tests/test_release_by_track.py:224` (`test_same_issue_different_track_flagged`) 与 `:232` (`test_same_track_not_flagged`) **已被逐条覆盖且全绿** (本轮实跑 `python3 -m unittest test_release_by_track` → `Ran 53 tests ... OK`)。容器段是否存在**不被任何生产代码消费** —— 它只是 `--raw-track-id` 的一段字面。这正是 memory `redfix-change-quantity`「修恒红/恒绿别在同一个量上调阈值, 换量」的第二次实证。

**且处方引用了一个 Spec 明文否认的构件**: SC-2 要求「两条 track-id **必须由 §2.1a 的 compose 函数派生**」, 而 §2.1a (`:164`) 逐字写 —— **「本 Spec 不新增拼接函数」**, 「拼接**没有代码宿主**」, 「新增代码落点只有 `lib/identity.py` 的直取 `uuid` accessor」。Impact 表 (`:642-668`) 亦无任何 compose 落点。⇒ 处方指向的对象不存在, 实现者只能退回手写字面串 —— 即 R3 判定的原病。同 memory `feedback_fixes_contradict_each_other_across_clusters` (逐条 fix 都对, 但 A 违反 B 的隐含前提)。

**字符级处方 (二选一, 不可两条都不做)**:
- **(a) 换量到文本层**: SC-2 的可机械断言部分改为「两处 SKILL.md 的 A.1 占位串**字面含 `<container_uuid>` 段**」—— 与 SC-1 文本层同宿主 (`tests/test_coordination_default_lockin.py`), baseline 必红 (两文件今日无 A.1 步骤块, 实测 grep 0 命中)。overlap 那两条行为改标注为「**回归守卫 — baseline 即绿**」, 体例照 SC-29 逐字;
- **(b) 若坚持保留代码类**: 必须同批把 compose 变成真代码 —— 在 Impact 表新增 `lib/track_id.py::compose_track_id(basename, number, container_uuid, *, spec_slug=None)` 一行, 并撤销 §2.1a 的「不新增拼接函数」句。**不撤那句就不许在 SC 里引用 compose 函数。**

---

## C-2 — SC-23 与 SC-14(a) 在 baseline 全绿: carry-id 断链**没有任何代码宿主能承载**

**severity: critical** · grep: `proposal.md:608` (SC-23) / `:594` (SC-14)

SC-23 自述「现状 A.1 原串 ≠ carry-id ⇒ `release_claim_by_track` 匹配不到 ⇒ **必红**」。**实跑推翻**:

```
$ X="aria-plugin-122-bfe8285d"        # 含容器段的 A.1 原串
$ python3 scripts/phase1_gate.py  --raw-track-id "$X" --phase A.1 --mode advisory \
      --linked-issue 10CG/aria-plugin#122 --repo-path $REPO
A.1 acquire rc= 0
  statuses after acquire: [('aria-plugin-122-bfe8285d', 'active')]
$ python3 scripts/release_gate.py --raw-track-id "$X" --repo-path $REPO
D.2b release rc= 0 released= True
  SC-23 assertion  'claim not active' -> True   << BASELINE 绿
```

**根因**: SC-23 声称钉住的缺陷**不在代码里** —— 它在三处 SKILL.md 的**占位串措辞**里 (`phase-b-developer/SKILL.md:92` 的 `"<本 cycle carry-id/Spec id>"`、`branch-manager/SKILL.md:146` 段、`phase-d-closer/SKILL.md:52` 的 `"<本 cycle 的 carry-id 原始串>"` —— 三处行号本轮逐条实读确认存在)。`derive_track_id` 对任何原串都做同一套归一, 所以**只要测试两端传同一个串就一定绿**; 要让它红, 测试必须自己写两个不同的串 —— 而那样它红在 baseline 也红在修复后, 是恒红。同一分析逐字适用于 **SC-14(a)** (其「红点在传 A.1 原串能否匹配到」与 SC-23 同根, Spec 自陈)。

对照: `tests/test_release_by_track.py:138` 的 `test_release_abandoned_roundtrips` **今天就在做同一件事并绿**。

**字符级处方**: SC-23 增**文本层断言**并写进 Impact 的 `tests/` 行 ——
> 断言 `phase-b-developer/SKILL.md` / `branch-manager/SKILL.md` / `phase-d-closer/SKILL.md` 三处 `--raw-track-id` 后的占位串**逐字节相同**, 且该串在 `phase-a-planner/SKILL.md` 的 A.1 步骤块内出现过 (同宿主 `test_coordination_default_lockin.py`)。baseline 必红 (三处现为三种不同措辞, 实读确认)。

SC-23/SC-14(a) 的 CLI 臂保留, 但**必须重标为「回归守卫 — baseline 即绿」**, 体例照 SC-29。

---

## C-3 — `track_form` / `spec_slug` **没有写入路径**: SC-27(C) / SC-1 / SC-15 的夹具不可构造

**severity: critical** · grep: `proposal.md:415` (§5.1 判定式) / `:447-453` (§5.3) / `:642-646` (Impact)

R3 新造的两个 additive 字段, **Impact 表只登记了读侧, 没有登记写侧**:

| 字段 | 声称的写入点 | 实读核验 |
|---|---|---|
| `track_form` | 「由**派生代码在 acquire 时按自己走的分支写入** (它当然知道自己走了哪支)」(`:415`) | ❌ **不存在「派生代码」** —— §2.1a 逐字「拼接发生在 A.1 模板里, 没有代码宿主」。`acquire_claim` 收到的是一个**不透明字符串** (baseline 签名 `acquire_claim(track_id: str, phase, identity, repo_path, *, now, linked_issue)`), 它**无从知道**调用者走了哪支 |
| `spec_slug` | 「`acquire_claim` 写入 `spec_slug`」(Impact `:643`) | ❌ **无 CLI 通道**。Impact 只给 `release_gate.py` 加了 `--spec-slug` (`:645`); `phase1_gate.py` 两行 (`:661`/`:662`) 只加 `--include-terminal` 与 `--heartbeat-only`; 且 `:661` 逐字「**不碰** `run_gate` `:1032` / `_run_gate_impl` `:335` 签名」⇒ acquire 全链路的形参面被冻结 |

**后果 (三条 SC 同时失效)**:
1. **SC-27(C)** 声明为「代码 (CLI 全链路)」, 夹具要求「同 issue 下两个方向各自持有 active claim (同 `track_id`, **不同 `spec_slug`**)」—— **CLI 全链路造不出这个夹具**。降到 lib 层直调 `acquire_claim(..., spec_slug=...)` 就能绿, 但生产 A.1 路径**永远写不进该字段** ⇒ 真实 claim 的 `spec_slug` 恒为 `None` ⇒ 触发 §5.1 的 fail-CLOSED「退回现状 ALL matching」⇒ **C-B 连坐在生产上原样存在, 而 SC-27(C) 绿**。这是 memory `feedback_completion_signals_vs_runtime_invocation` + `feedback_schema_column_dataclass_field_pair` (加列不加写入点 ⇒ 静默 `None`) 的合并复发;
2. **SC-1 / SC-15** —— §5.1 `:419` 逐字「SC-1 / SC-15 / SC-27 三处一律按该字段判, 夹具**不得预标形态**, 而应**跑派生代码让它自己写**」。没有派生代码 ⇒ 这三条的夹具**按 Spec 字面不可构造**;
3. 唯一的绕法是让 AI 在模板里多传一个 `--track-form issue|slug` —— 而那**正是** §5.1 明令否决的「预标形态 / 依赖调用方自报」。

**字符级处方 (Impact 表补三行, 缺一不可)**:
```
| skills/state-scanner/scripts/phase1_gate.py (第三处变更) | 新增 CLI flag --spec-slug / --track-form (choices=["issue","slug"]); 二者透传至 acquire_claim | R3/TL-C1 + TL-M4 |
| skills/state-scanner/scripts/phase1_gate.py            | run_gate / _run_gate_impl 增 keyword-only spec_slug / track_form (默认 None) — 本行**撤销** :661 的「不碰两函数签名」限定, 该限定只对 include_terminal 成立 | 同上 |
| skills/phase-a-planner/SKILL.md + spec-drafter/SKILL.md | A.1 步骤块的 phase1_gate 命令模板增 --spec-slug "<本 Spec 目录名>" --track-form <issue|slug> | 同上 |
```
并在 SC-27 的「怎么会红」补一句: **「A.2 须以『phase1_gate CLI 不传 `--spec-slug` 时 claim 的该字段为 None』作为坏实现验证本条确实会红」** (memory `adversarial-fixture`)。

---

## C-4 — SC-28 第二臂 / SC-21 判据: 机械断言被挂在 **AB 行为宿主**上, 无代码宿主

**severity: critical** · grep: `proposal.md:614` (SC-28) / `:601` (SC-21)

- **SC-28 第二臂** (R3/TL-M2 新造): 「连跑 N 次 `--heartbeat-only` 后, `coordination_probe.py` 的 recent production 计数不变」。这是一条**纯机械断言** —— 跑 CLI N 次、读 `.aria/coordination-telemetry.jsonl`、比 `count_production_invocations()` 的返回 (实读 `coordination_probe.py:109`/`:136` 返回 `scan["recent_count"]`)。
- **但 SC-28 整条被标为「行为 (定向 fixture)」**, 且 Impact 表的宿主分配把它放进 **AB 套件行** (`aria-plugin-benchmarks/ab-suite/state-scanner.json` 行逐字「与 SC-21 / SC-28 呼应」), 而 `skills/state-scanner/tests/` 那一行的 SC 清单 (`:664`) 是 `SC-2 / SC-3 / SC-5~8 / SC-10 / SC-14(a) / SC-15 / SC-22 / SC-23 / SC-24 / SC-25(代码臂) / SC-27 / SC-29` —— **SC-28 不在其中**。
- **AB eval 观测的是模型行为轨迹, 不是磁盘上的 JSONL 计数器** ⇒ 第二臂在其被指派的宿主上**无法被断言**。
- **SC-21 同病**: 其判据逐字「= 该 CLI **被 subprocess 调用**且 `claim.heartbeat_at` **被刷新**」—— 后半句同样是磁盘断言, 宿主同样只有 AB 套件。

这是 R1/C4「把 SC 挂在**不存在的**测试宿主上」在 R3 补丁里的**原形复发** (memory `fix-the-class`: 修实例必问这形状还有几个兄弟位置)。

**字符级处方**: 把两条各自**拆成两行 SC**, 编号追加不重排 ——
- `SC-28`(保留, 行为) = 「`enabled == false` ⇒ 入口零 heartbeat 调用」, 宿主 AB;
- **`SC-30`(新, 代码 CLI 全链路)** = 「连跑 3 次 `phase1_gate.py --heartbeat-only`, `coordination_probe.count_production_invocations()` 的返回值前后相等」, 宿主 `tests/` (扩 `test_release_by_track.py` 或新建 `test_heartbeat_only.py`), **并加进 Impact 的 `tests/` 行清单**;
- **`SC-31`(新, 代码)** = 「调 `--heartbeat-only` 后本容器本 track 的 `claim.heartbeat_at` 严格大于调用前」, 宿主同上。SC-21 只保留「AI 是否在 `/state-scanner` 入口发起该调用」这一半行为断言。

---

# MAJOR

## M-1 — SC-27 三臂中 (A)(B) 双双 baseline 绿, (B) 已被既有测试逐字覆盖

**severity: major** · grep: `proposal.md:610`

- **臂 (B)**「同一条轨放弃整个 issue ⇒ claim 为 `abandoned`」: 实读 `tests/test_release_by_track.py:138` 的 `test_release_abandoned_roundtrips` —— `acquire_claim(derive_track_id("carry-dead"))` → `release_claim_by_track("carry-dead", status="abandoned")` → 断言 `["abandoned"]`。**同一场景、同一断言, 今天就绿** (本轮实跑 53/53 OK)。Spec 自己也承认「只做 (B) 的测试恒绿」, 却仍把它写成一条正式臂;
- **臂 (A)**「issue 派生形放弃一个方向后 claim 仍 `active`」: 该臂的动作是「**什么都不做**」—— 夹具 acquire 之后不调任何 release, 然后断言 claim 还 active。**一个不执行任何被测动作的断言恒真**; 它只在「实现主动去 release」时红, 而「实现」在这里是 SKILL.md 散文, 测试无从驱动它。⇒ 恒绿。
- ⇒ **SC-27 目前唯一可能红的是 (C), 而 (C) 被 C-3 判为不可构造** ⇒ 本条整体**零红臂**。

**处方**: (A) 改标「行为 (定向 fixture)」并移出代码类; (B) 改标「回归守卫 — baseline 即绿, 已由 `test_release_abandoned_roundtrips:138` 覆盖」并写明本条不重复实现; (C) 按 C-3 修好写入路径后作为**唯一**代码臂。SC-27 的场景列写「**三臂**」却只枚举 (A)(B) 两项 (见 m-1)。

## M-2 — SC-7 第二臂未钉 fresh session ⇒ 对「照抄 `(container, session)` 匹配键」的坏实现免疫

**severity: major** · grep: `proposal.md:571`

补强本身有效 (by-track 变体在 `d50f9c3` 不存在 —— 实读 `claim_lifecycle.py` 顶层只有 `heartbeat` `:178` / `release_claim` `:274` / `release_claim_by_track` `:377`, 无 by-track heartbeat ⇒ 第二臂 baseline 必红)。**但分辨力不足**: 第二臂只要求「显式调 by-track 变体后再 sweep, 断言未被 abandoned」。若夹具沿用同一 `Identity`, 一个把新变体实现成 `(container, session)` 匹配 (= 抄既有 `:228`) 的坏实现**照样绿** —— 该臂于是不比 SC-5 多覆盖任何路径。

**处方**: 第二臂的场景列逐字补 —— 「**刷新时的 `Identity` 必须使用与 acquire 时不同的 `session_id`** (仿 `:138` 的 `Identity("alice","cA","s2")` 体例); 用同一 session 的夹具视为未满足本条」。

## M-3 — SC-15 代码臂 baseline 绿; 其唯一红点被 C-3 抽空

**severity: major** · grep: `proposal.md:597`

「release 旧 + acquire 新两步后无孤儿」—— `release_claim_by_track` 与 `acquire_claim` 今天都在, 逐字实现即绿。Spec 给的红点是「用『有没有关联 issue』做谓词的实现在第三类夹具上必红」, 而该谓词按 §5.1 `:419` 必须读 `claim.track_form` —— C-3 已证该字段无写入路径, 且 §5.1 明禁夹具预标形态 ⇒ 第三类夹具不可构造。

**处方**: 与 C-3 同批修; 修好前 SC-15 应标「⚠️ 阻塞于 `track_form` 写入路径」而不是标「代码」。

## M-4 — SC-24 的负控「不出现在 overlap[]」**结构性恒真**, 未按 SC-29 体例声明

**severity: major** · grep: `proposal.md:606`

第二个断言 (unknown claim 不出现在 `linked_issue_overlap[]`) 在 **baseline 与任何正确实现下都为真** —— Spec 自己在 §2.4a `:293-296` 逐字论证过: sentinel 的 `linked_issue` 为 `None` (实读 `claim_schema.py:130` 默认值), 被 `collision.py:274-275` 的第二道门丢弃, 「**即便把 `unknown` 移出 `_TERMINAL`, 下一行立刻丢弃, 行为逐字节不变**」。⇒ 它是一条 **baseline 即绿的回归守卫**, 与 SC-29 同性质, 却被和「`unknown_schema_claims >= 1`」(baseline 红) 捆进同一条 —— **这正是 SC-29 自己 `:615` 逐字禁止的做法**:「把 baseline-红与 baseline-绿的断言捆进同一条会让『怎么会红』失去分辨力」。同 Spec 内两处相反做法 (memory `fixes-contradict`)。

**处方**: 拆 `SC-32`(新) 承接负控, 标 ⚠️ **回归守卫 — baseline 即绿**, 并按 SC-29 体例给出坏实现 (「删掉 `collision.py:274-275` 两行」) 作为 A.2 的可证伪验证。

## M-5 — SC-29 第二组夹具 (terminal own claim) 是 baseline **红**, 与第一组的 baseline 绿捆在同一条

**severity: major** · grep: `proposal.md:615`

SC-29 通篇标「⚠️ 回归守卫 — baseline 即绿」并给了很好的负控 (删 `collision.py:278-279`)。但 R3/QA-F4 追加的第二组夹具「own claim 状态为 terminal 且带 `--include-terminal` 跑」在 baseline 上**跑不起来** —— `--include-terminal` 不存在, argparse 直接报错 ⇒ 第二组 baseline 红。一条自称「baseline 即绿」的 SC 里藏了一个 baseline 红的夹具组, 破坏了它自己的分辨力声明。

**处方**: 第二组拆为 `SC-33`(新, baseline 红, 归入 `--include-terminal` 家族), SC-29 只留 active 那组并维持「baseline 即绿」的定性。

## M-6 (字段 spec) — SC-6 把 baseline-红与 baseline-绿捆一条, 且第二半今日已绿 (实测)

**severity: major** · grep: `openspec/changes/linked-issue-field-availability/proposal.md:479`

SC-6 一条里有三个可分辨的量:
1. 模板含恰一条过 E0 的字段行 —— **baseline 红** (实跑 `grep -c "关联 Issue" standards/openspec/templates/proposal-minimal.md` = **0**);
2. 模板 `## Template Usage Notes` 含指定句 —— baseline 红;
3. `spec-drafter/SKILL.md` 对模板的相对路径引用解析到存在的文件 —— **baseline 绿** (实读 `:429` = `../../../standards/openspec/templates/proposal-minimal.md`, 从 `aria/skills/spec-drafter/` 出发解析到 `/home/dev/Aria/standards/openspec/templates/proposal-minimal.md`, **实测存在**)。

第 3 项是纯粹的**回归守卫**, 与前两项性质相反。母 Spec SC-29 `:615` 已把这条规则写成文, 姊妹侧却违反它。

**处方**: 第 3 项拆 `SC-9`(新), 标「⚠️ 回归守卫 — baseline 即绿」。

## M-7 (字段 spec) — SC-8 从 `aria/` 子模块内的测试读**主仓** `.aria/state-checks.yaml`, **没有** SC-6 那样的 fail-soft 豁免 ⇒ plugin 独立分发时恒红

**severity: major** · grep: `linked-issue-field-availability/proposal.md:481` + `:459-467` (验证宿主表)

本轮新增的「验证宿主」表**只给 SC-6 授予了跨仓 fail-soft skip**, SC-8 三臂 (a)(b)(c) 同样跨仓却未获授予:
- (a) 读主仓 `.aria/state-checks.yaml`;
- (c) 实跑 `python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/...` —— 命令是**主仓相对路径**, 要求 cwd = 主仓根。

**实测**: `git -C aria ls-tree d50f9c3 -- .aria` **零输出**, `ls aria/.aria` = `No such file or directory` ⇒ **aria-plugin 仓自身没有 `.aria/`**。而这些测试正是由 `skills/run_all_tests.sh` 在 aria-plugin 仓内跑的。⇒ 在 plugin 独立 CI 上 SC-8 三臂**全部 FAIL 而非 skip** = 恒红 (memory `feedback_false_green_dual_is_permanent_red`: 恒红与假绿同样零信息)。

**处方**: 验证宿主表给 SC-8 补一行, 逐字照 SC-6 的措辞 —— 「(a)(c) 两臂在 `Path(__file__).resolve().parents[3] / '.aria' / 'state-checks.yaml'` 不存在时 **skip 并打印原因**, 不 fail」; (b) 是纯 `Path` 布局断言, 可留 fail。

## M-8 (探针 spec) — SC-18 的语料宿主是**主仓 commit `cc1bdef`**, 而测试宿主在 `aria/` 子模块内, 同样无 skip 条款

**severity: major** · grep: `openspec/changes/sibling-spec-probe/proposal.md:458` + `:439` (验证面分层)

**先给正面结论**: SC-18 的**全部数字本轮独立复测, 逐条 MATCH** —— 语料 147 (changes 7 + archive 140); 臂 (a) `no_field` **133** / `url_fallback` **13** / `no_token_no_url` **1**, 簇 **3**, `#122` 簇**不含**母 Spec; 臂 (b) `url_fallback` **14** 且 `#122` 簇**含**母 Spec (假阳性复现); 臂 (c) `url_fallback` **10**, 簇 **1**。三个簇的成员路径亦逐条对上。**这是三份 Spec 里质量最高的一条 SC。**

**但宿主不成立**: 宿主声明为 `skills/audit-engine/tests/` (在 aria-plugin 仓内), 语料是**主仓** `cc1bdef` 的 147 个 blob。plugin 独立分发/独立 CI 时既无 `openspec/` 也无该 commit ⇒ 与 M-7 同形的恒红。且 `cc1bdef` 相对主仓 HEAD `322f280` 已落后, 三份拆分产物落盘后语料已变成 149 篇 (姊妹 Spec `:82` 自测)。

**处方 (二选一)**:
- (a) 把三臂语料**冻结为仓内合成夹具目录** `skills/audit-engine/tests/fixtures/corpus-cc1bdef/` (只需保留 14 个「有字段行」的文件 + 一个计数常量), SC-18 断言改为对该 fixture 目录的分布; 或
- (b) 保留活语料, 但在 SC-18 增逐字 skip 条款: 「`parents[3]/openspec` 不存在或 `git cat-file -e cc1bdef` 失败 ⇒ **skip 并打印原因**」, 并把三个绝对数改成**相对不变量** (臂 b 的 `url_fallback` 比臂 a **恰多 1**, 且多出的那一份是 `a1-entry-claim-duplicate-work-guard`; 臂 c 的簇数 **严格小于**臂 a)。相对不变量随语料增长仍成立, 绝对数不成立。

**宿主的正面核实**: 「新建 `skills/audit-engine/tests/` 会被 `run_all_tests.sh` 自动纳入」这条**属实** —— 实读 `skills/run_all_tests.sh:48` `find "$SKILLS_DIR" -type d -name tests | sort`、`:50` 要求目录内有 `test_*.py`、`:71` 无 pytest 时走 `unittest discover`。目录今日**不存在** (实测 `ls aria/skills/audit-engine/` 只有 `SKILL.md` + `references/`)。

## M-9 (探针 spec) — SC-18 臂 (c) **欠定**: 147 篇里 62 篇无裸 `---`, 规则未定义该情形, 两种读法给出不同数字

**severity: major** · grep: `sibling-spec-probe/proposal.md:458`

臂 (c) 定义为「行首 + **只在首条 `---` 之前找**」。语料里 **62/147 篇根本没有裸 `---` 行**, 而规则对「无边界」情形沉默:
- **读法 A** (无边界 ⇒ 退化为扫全文): 得 `no_field` 136 / `url_fallback` **10** / `no_token_no_url` 1, 簇 1 —— **与 Spec 报的数字一致**;
- **读法 B** (无边界 ⇒ 一律 `no_field`): 得 `no_field` **139** / `url_fallback` **7** / 1, 簇仍 1。

两个独立实现者会得到不同的 `url_fallback` 计数 ⇒ 该臂的断言值不可复现 (memory `spec-underdetermination`: 承重算法须钉到字符级)。

**处方**: 臂 (c) 的场景列补一句逐字 —— 「**文件不含任何裸 `---` 行时, 视为边界在文件末尾 (即扫全文)**」。

## M-10 (探针 spec) — SC-14 的夹具是**本机仓库实况**而非合成夹具 ⇒ 他机/CI 上不可复现

**severity: major** · grep: `sibling-spec-probe/proposal.md:454`

SC-14 用「本仓 `probe` 实况」作夹具: 存在 `refs/remotes/probe/*` 但 `git config --get remote.probe.url` 为空。**本轮实测该事实成立** ——
```
$ git -C /home/dev/Aria for-each-ref --format='%(refname)' refs/remotes | sed 's|refs/remotes/\([^/]*\)/.*|\1|' | sort | uniq -c
      2 github
      9 origin
      1 probe
$ git config --get-regexp '^remote\..*\.url'
remote.origin.url ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git
remote.github.url git@github.com:10CG/Aria.git
```
**但这是一台开发机上的偶发残留**: 任何新 clone 都没有 `refs/remotes/probe/*`, 该测试在 CI 与他人机器上要么 skip 要么退化为恒绿。且它与 SC-12 (`git symbolic-ref refs/remotes/github/HEAD` exit **128** —— 本轮在主仓与 aria 两处均实测复现) 不同: SC-12 的条件在任何未设 HEAD 的 clone 上都成立, SC-14 的不成立。

**处方**: SC-14 场景列改为「夹具**自建**: `git init` 临时仓后 `git update-ref refs/remotes/probe/master <sha>` 而**不**写 `remote.probe.url`」, 并删去「本仓实况」的字样 (真实语料只作**举例**, 不作夹具 —— 与 SC-18 第四臂已采取的立场一致)。

---

# 逐 SC 四字段表

> 列义: **宿主** = 哪个文件真能承载它 / 它今天在不在 · **baseline** = 我实读代码判定的红绿 (不采信 Spec 自述) · **怎么会红** = 一个具体坏实现 · **风险** = 恒绿 / 恒红 / 无。
> `EXT` = 扩既有文件; `NEW` = 待建; ✅=宿主实存 ❌=宿主不存在。

## A. `a1-entry-claim-duplicate-work-guard` (母, SC-1…29)

| SC | 宿主 (实存?) | baseline | 怎么会红 | 风险 |
|---|---|---|---|---|
| **1** | 文本层 `tests/test_coordination_default_lockin.py` ✅EXT + AB `phase-a-planner.json`/`spec-drafter.json` ✅(evals=2/2) | **红** (两处 SKILL.md 无 A.1 步骤块, 实测 grep 0) | 占位串写 `<spec-slug>-…` | 文本层无风险; **但「改名前后 track-id 不变」的判定按 §5.1 须读 `track_form` ⇒ 受 C-3 牵连** |
| **2** | `tests/test_release_by_track.py` ✅EXT | **绿 (两臂, 实跑证)** | — (无坏实现能让它红) | 🔴 **恒绿 (C-1)**; 既有 `:224`/`:232`/`:533` 三条已覆盖同一量 |
| **3** | `tests/` ✅ (新 accessor 单测) | **红** (直取 `uuid` 的 accessor 不存在) | 直调 `get_container_id()` (`identity.py:191`, `:222` `return label if label else uuid` — 行号实读确认) | 无。`get_container_id(home_dir=)` 支持注入 ⇒ 夹具可设 label ✅ |
| **4** | 文本层同 SC-1 ✅EXT + AB ✅ | **红** (同 SC-1) | 占位串写裸 `<number>` | 断言对象是 SKILL.md 占位串字面 —— **已显式分两层且不冒充结构化测试**, 可接受 |
| **5** | `tests/` ✅EXT | **红** (`claim_lifecycle.py` 顶层无 by-track heartbeat; 只有 `heartbeat:178` 按 `(container,session)` `:228`) | 只保留 `heartbeat()` | 无 ✅ |
| **6** | `tests/` ✅EXT | **红** (同上) | 只刷第一条 | 无 ✅ |
| **7** | `tests/test_release_by_track.py` ✅EXT | **红** (第二臂调不存在的变体) | 不调新变体 ⇒ 第二臂红 | 🟡 **M-2**: 未钉 fresh session ⇒ 对「抄 `(container,session)` 键」的坏实现免疫。第一臂单独看被 `:380` 覆盖 (已绿) |
| **8** | `tests/` ✅EXT (CLI 全链路) | **红** (`--include-terminal` 不存在 ⇒ argparse 报错) | `collision.py:268` `_TERMINAL` skip | 🟡 m-2: baseline 红的**原因是 flag 缺失**而非可见性逻辑; 实现后须确认断言真落在可见性上。`yielded` 已按实读删除 ✅ 正确 |
| **9** | AB `phase-a-planner.json`/`spec-drafter.json` ✅ | 待建 fixture | 「无条件调用」臂 | 无 (类别 R2/M-16 已订正为行为 ✅) |
| **10** | `tests/` ✅EXT (CLI) | **红** — 实测 `grep -n "fetch_degraded" phase1_gate.py` **只命中 `:210` docstring**, 全文无 `error=` 赋该 token | `error: null` 现状 | 无 ✅ 单一断言, M-16 拆分正确 |
| **11** | AB ✅ | 待建 | 「渲染一行后自行继续」/「对 `done` 也给释放选项」 | 依赖 §2.3 的四档选项表 (未审新表面 #2) |
| **12** | AB ✅ | 待建 | 跳过 `--linked-issue` | 无。可辨性有实证: `:1230` 整块门控, `tests/test_release_by_track.py:563` 已锁「键缺席」✅ |
| **13/16/17/18/19/20** | — | — | — | ✅ 迁出/撤销行**保留编号未复用**, 编号纪律执行到位 |
| **14** | (a) `tests/` ✅EXT (b) AB ✅ | **(a) 绿 (实跑证)** / (b) 待建 | (a) 无 | 🔴 **(a) 恒绿 (C-2)** — 与 SC-23 同根 |
| **15** | `tests/` ✅EXT | **绿** (release+acquire 今天都在) | 唯一红点靠 `track_form` | 🔴 **恒绿 (M-3)** + 受 C-3 阻塞 |
| **21** | AB `state-scanner.json` ✅(evals=12) | 待建 | 未挂载 ⇒ 不触发 | 🔴 **判据含磁盘断言 (`heartbeat_at` 被刷新), AB 宿主观测不到 (C-4)** |
| **22** | `tests/test_coordination_default_lockin.py` ✅EXT | **红** — 实测两处 SKILL.md 均无 `^#{2,4}[ \t]+前置: REQUIRE claim`; 先例 `branch-manager/SKILL.md:146` 逐字存在 ✅ | 把 `前置: REQUIRE claim` 塞进 A.1 现有 ```yaml 列表 ⇒ 裸 `assertIn` 免疫、`assertRegex`+围栏过滤必红 | 无。**本轮质量最高的代码类 SC**: 断言强度差异有 docstring 声明, 锚点换名理由实读支撑 (`spec-drafter:30`/`:369` A.0 占用、`A.0.5`=brainstorm 均实测复现) ✅ |
| **23** | `tests/` ✅EXT (CLI) | **绿 (实跑证)** | 无 | 🔴 **恒绿 (C-2)** |
| **24** | `tests/` ✅EXT (CLI) | 第一断言 **红** / 负控 **恒真** | 强行放行 sentinel | 🟡 **M-4**: 负控 baseline 即绿却未按 SC-29 体例声明 ⇒ 红绿捆绑 |
| **25** | `tests/` ✅EXT (代码臂) + AB (行为臂) ✅ | **红** — 实读 `phase1_gate.py:1238` 现为 `out["linked_issue_overlap"] = []` ✅ | `except` 写 `[]` | 无 ✅ 代码臂/行为臂分层干净, 两个坏实现都点了名 |
| **26** | AB ✅ | 待建 | 「照问不误」 | 无。`unattended` 键今日未注册于 `DEFAULTS.json` (Spec 自陈清单#26) ⇒ fixture 须自带 config |
| **27** | `tests/` ✅EXT (CLI) | **(A) 绿 (无动作) · (B) 绿 (`:138` 已覆盖) · (C) 不可构造** | 只有 (C) 可红, 但 C-3 阻塞 | 🔴 **零红臂 (M-1 + C-3)** |
| **28** | 臂1 AB ✅ / **臂2 无宿主** | 臂1 待建 / 臂2 红 (flag 缺失) | 把 heartbeat 记进 production 分区 | 🔴 **C-4**: 臂2 是机械断言却挂 AB, 且不在 Impact 的 `tests/` 行清单里 |
| **29** | `tests/` ✅EXT (CLI) | **第一组 绿 (回归守卫, 已声明) / 第二组 红 (`--include-terminal` 缺失)** | 删 `collision.py:278-279` (Spec 已点名 ✅) | 🟡 **M-5**: 一条自称「baseline 即绿」的 SC 里混入 baseline-红夹具组。**除此之外这是本 Spec 对「装饰 vs 真守卫」处理最正确的一条** —— 有负控、有 memory 引用、有与 SC-2 的分列理由 ✅ |

## B. `linked-issue-field-availability` (子, SC-1…8)

| SC | 宿主 (实存?) | baseline | 怎么会红 | 风险 |
|---|---|---|---|---|
| **1** | `tests/test_linked_issue_field.py` ❌NEW (目录 ✅实存) | **红** — 实测 `lib/linked_issue_field.py` **不存在** | 松谓词在 (b)(c)(d) 上抽出 token; 漏 `(?:> ?)?` 在 (d) 上抽出 `other/repo#999` | 无。**四夹具两两可辨, (d) 专钉围栏正则前缀, 是三份里最扎实的定位断言** ✅ |
| **2** | 同上 ❌NEW | **红** | 「取行内第一个 code span」抽出 `confirmed` | 🟡 m-1: 「真实语料 **6** 条」本轮未逐条复核 (已复核其中至少 1 条: `archive/2026-07-31-…/proposal.md:6` 逐字含 `` `confirmed` ``/`` `major` ``/`` `next-cycle` ``) |
| **3** | 同上 ❌NEW | **红** | 整串直喂归一 / 只校验第一元素 / 实参取整串 | 无 ✅ 三个坏实现各被一臂拒绝 |
| **4** | 同上 ❌NEW | **红** | 把 `无` 当 token 传 `--linked-issue`; 接受裸 `无` | 无 ✅ (b) 的真实语料实例**逐字核过**: `archive/2026-08-23-linked-issue-normalization/proposal.md:6` `cat -A` = `> **关联 Issue**: 无$` |
| **5** | 同上 ❌NEW (CLI subprocess) | **红** (探针不存在) | (a) 正向枚举放行 · (c) 静默忽略陈旧条目 · (d) 零证据当正证据 · (e) 白名单文件缺失当错误 | 无。**五臂两两可辨设计正确** ((a)/(c) 同 exit 1 靠文案分, (b)/(d) 同 exit 0 靠 `##SKIP##` 首行分) ✅ 🟡 m-2: §4 骨架的 `command` **恒传** `--grandfathered`, ⇒ (e) 的「参数缺省」子情形在注册面上永不发生, 只有「文件不存在」那半可达 |
| **6** | `tests/test_linked_issue_field.py` ❌NEW (跨仓读主仓 `standards/`) | **半红半绿** — 模板 `grep -c "关联 Issue"` = **0** (红); `spec-drafter/SKILL.md:429` 引用**今日已解析到存在文件** (绿, 实测) | 模板写成裸文本/链接形; 漏 Usage Note; 引用漂移 | 🟡 **M-6 红绿捆绑**。跨仓 fail-soft skip 条款**已给** ✅ (三份里唯一给了的) |
| **7** | AB `spec-drafter.json` ✅(evals=2) | 待建 | 省略字段行 / 写成链接形 / 留空 | 无 ✅ 类别标注正确 (行为, 不冒充结构化测试) |
| **8** | `tests/test_linked_issue_field.py` ❌NEW (跨仓读主仓 `.aria/`) | **红** (三者今日都不存在) | (a) 只建脚本不注册 · (b) 放回 `.aria/probes/` · (c) traceback ⇒ stdout 空 | 🔴 **M-7 恒红**: aria-plugin 仓**无 `.aria/`** (实测), 且**未获** SC-6 那样的 skip 条款。(b) 臂本身很有价值 (钉住 D3 改判不被悄悄退回) ✅; (c) 「不断言 exit 值本身」的克制正确 ✅ |

## C. `sibling-spec-probe` (子, SC-1…18)

| SC | 宿主 (实存?) | baseline | 怎么会红 | 风险 |
|---|---|---|---|---|
| **1** | `skills/audit-engine/tests/test_sibling_spec_probe.py` ❌NEW (目录 ❌, 但 `run_all_tests.sh:48/50/71` 自动发现属实 ✅实读) | **红** (探针不存在) | 只扫 `changes/` ⇒ 本仓真实语料返回空 (实测三簇 6 份全在 `archive/`) | 无 ✅ 立项理由与断言同源 |
| **2** | 同上 ❌NEW | **红** | 「无命中」映射成非 0 exit | 无 ✅ |
| **3** | 同上 ❌NEW | **红** | verdict 算成 `no_sibling_found` / degraded 映射非 0 / 丢弃 `hits` | 无 ✅ 三个坏实现各被点名, 拆自旧 SC-18 的自相矛盾, 拆得对 |
| **4** | 同上 ❌NEW | **红** | 照旧 SC-18 字面写「无远端 ⇒ exit 非 0」 | 无 ✅ |
| **5** | 同上 ❌NEW | **红** | 不做自命中排除 | 🟡 夹具须合成 (本 Spec 合并前无真实语料), Spec 未言明 |
| **6** | 同上 ❌NEW | **红** | 静默截断 / 排序把 `archive/` 排前 / 截断后仍报 `no_sibling_found` | 无 ✅ 三个坏实现点名到位 |
| **7** | 同上 ❌NEW | **红** | 只实现层 1 canonical ⇒ 返回空 | 无 ✅ 夹具行**逐字核过**存在; `normalize_linked_issue('10CG/aria-plugin#122')` 实跑 = `('aria-plugin', 122)` ✅ |
| **8** | 同上 ❌NEW | **红** | 「行内第一个 code span」抽到 `confirmed` | 无 ✅ 实跑核过 `normalize_linked_issue('confirmed')` = `None` ⇒ 落 `("r","confirmed")` 可辨 |
| **9** | 同上 ❌NEW | **红** | 把 `无` 当普通 token 求交 | 无 ✅ 实跑核过 `normalize_linked_issue('无')` = `None` ⇒ 原串相等必命中 |
| **10** | 同上 ❌NEW | **红** | 回落条件写成「canonical 集合为空」 | 无 ✅ 断言 `layer=="wu_empty"` 而非只断言不命中 —— **换量换得对** |
| **11** | 同上 ❌NEW | **红** | 把 `wu_empty`/`no_field` 折叠成同一枚举 | 无 ✅ 正证据/零证据分离 |
| **12** | 同上 ❌NEW | **红** | 只读本地 `symbolic-ref` | 无 ✅ **实测复现**: `git -C aria symbolic-ref refs/remotes/github/HEAD` → `fatal: ... is not a symbolic ref`, exit **128** (主仓同) |
| **13** | 同上 ❌NEW (注入式 runner) | **红** | 照抄 `fetch_gate.py:55,124-127` 的 `("master","main")` 名字猜测 | 无 ✅ fail-closed 断言含「stdout 不得出现字面 master/main」这个**负控**, 写法正确 |
| **14** | 同上 ❌NEW | **红** | 用 `refs/remotes/*` glob 枚举 remote | 🟡 **M-10**: 夹具是本机实况 (实测确有 1 条 `probe` 无 url), 他机不可复现 ⇒ 恒跳过或恒绿 |
| **15** | 同上 ❌NEW | **红** | `log()` 写进 stdout | 无 ✅ |
| **16** | AB `audit-engine.json` ❌NEW (实测 `ab-suite/` 31 个 json, **无该文件**) | 待建 | 把三者任一折叠成「无竞品」 | 🟡 m-1: 宿主待建, Spec 已自陈 ✅ 诚实 |
| **17** | `audit-engine/tests/` ❌NEW | **红** — 实测 `grep -c "每轮入口: 竞品 spec 探针" references/execution-modes.md` = **0** | 只 patch Convergence ⇒ 计数 1 ⇒ 红 | 无 ✅ 两节 (`## Convergence 模式:84` / `## Challenge 模式:113`) **各含恰一个 ``` 围栏块**, 实读确认可插。「第三个模式块会误判」的保守性已写进 docstring 要求 ✅ |
| **18** | `audit-engine/tests/` ❌NEW + **主仓 `cc1bdef` 语料** | **红** (探针不存在) | 退回宽松定位 ⇒ 臂(a) 出现臂(b) 的假阳性; 「顺手加固」成只扫头部区 ⇒ 两个真簇消失; **第四臂**: 不做围栏排除 ⇒ 合成夹具被算进 `#1` 簇 | ✅ **数字全部独立复测 MATCH** (147 / 133-13-1 / 3 簇 / 14 / 10 / 1 簇, 簇成员路径亦对上)。🔴 **M-8 跨仓宿主无 skip 条款** · 🟡 **M-9 臂(c) 无 `---` 时欠定 (62/147 篇受影响, 两读法给 10 vs 7)** · 🟡 **M-11 第四臂的「活实例」措辞**: 姊妹 proposal **同时含**一条**真** (非围栏) depth-1 字段行 (`:6`, verdict `OK`/`wu_empty`), 只有 `:95`/`:116` 两行在围栏内 ⇒ **该文件整体不是第四臂要的「只有围栏内字段行」形态**, 只有那两行的**行文本**可取。Spec 写「可直接取作夹具原文」易被读成取整份文件 |

---

# 正面观察 (不是凑数, 是本轮实读认定确实做对的)

1. **编号纪律**: 母 Spec 的 SC-13/16/17/18/19/20 六行**保留行号、标明去处或 ⛔ 撤销、不复用**, 两子 Spec 各自从 SC-1 重开并在头部写明与母 Spec 旧编号的对应 —— 拆 Spec 最容易丢的东西没丢。
2. **SC-22** 是三份里最扎实的代码类 SC: `assertRegex` + 围栏外过滤明确拒绝了裸 `assertIn` 能通过的那一种坏实现; 与先例 `test_phase_b_require_claim_present:53` 的强度差异**要求写进 docstring**; 锚点换名的每一条依据 (`spec-drafter:30`/`:369` 的 A.0 占用、`branch-manager:146` 的同体例真实标题) 本轮**逐条实读复现**。
3. **SC-18** 的三臂对照 + 第四臂是「验拒绝能力而非验当前取值」的正确形态, 且**两个坏实现都是有人会真写出来的**, 不是稻草人; 全部数字独立复测 MATCH。
4. **SC-29** 是本项目文档里对「baseline 即绿的回归守卫」处理得最规范的一条: 显式标注、给出坏实现 (删 `collision.py:278-279`)、说明为何不与 SC-2 合并、引 memory `adversarial-fixture`。**M-4/M-5/M-6 三条 finding 的处方就是「照它抄」。**
5. **跨 Spec 接缝已闭合**: 探针 §3 的四态逐格映射表与字段 spec §3 的 `extract_linked_issue_field(text) -> FieldVerdict` 四态定义**双向对齐**且姊妹侧已回灌确认 —— 这是 memory `split-makes-seams` 点名的那类缺陷唯一被真正接住的一处。
6. **数字口径纪律**: 字段 spec `:86` 主动并列「总体 / 范围 / 计数法」三项解释与探针 spec 的计数差异, 而不是宣称对方错 —— 正是 memory `critique-repeats-error` 的处方。`.aria/state-checks.yaml` 条数从 10 订正为 11 (本轮实测 = **11** ✅), 并写明「口径 (命令) 才是规范, 数字是当日观测」。
7. **AB 宿主计数全部属实**: 实测 `ab-suite/` 31 个 json; `phase-a-planner.json` evals=**2**, `spec-drafter.json` evals=**2**, `state-scanner.json` evals=**12**, `audit-engine.json` **不存在** —— 与三份 Spec 的自述逐条一致。
8. **行号基线纪律**: 本轮抽查的 **全部** `文件:行号` 引用在 `d50f9c3` 上复核成立 —— `identity.py:191/222/242/244`、`constants.py:36/43`、`claim_lifecycle.py:178/228/377/425`、`collision.py:268/278-279`、`phase1_gate.py:210/1032/335/1230/1233/1238/1191(--phase required)`、`release_gate.py:237`、`run_all_tests.sh:48/50/71`、`execution-modes.md:84/113`。**零处漂移。**

---

# 建议的下一步 (给主控, 不代 owner 裁定)

1. **C-1/C-2/C-3 是同一个形状**: 三条 SC 都在用**代码类断言**去钉**住在 SKILL.md 散文/模板里的缺陷**。处方不是再加一臂, 而是**换宿主到文本层** (母 Spec 自己已在 SC-1/SC-4/SC-22 上示范了正确做法)。建议主控做一次**全表扫描**: 逐条问「这条 SC 声称钉住的东西, 是代码还是散文?」—— 按本轮结果, 至少 SC-2 / SC-14(a) / SC-15 / SC-23 / SC-27(A)(B) 六处答案是「散文」而类别标着「代码」(memory `fix-the-class`)。
2. **C-3 必须在 A.2 之前解**: 它不是断言质量问题, 是**设计缺一环** —— 两个新字段无写入路径, 落地后生产上恒为 `None`, C-B 连坐原样存在而测试全绿。
3. **M-7/M-8 同形**: 两子 Spec 各有跨仓宿主, 只有字段 spec 的 SC-6 拿到了 fail-soft 条款。建议统一成一条**三份共用的措辞**, 放进各自的「验证宿主」段。
4. **加轮判据**: 本轮 major 数 (12) 相对 R3 未见下降, 且 **4 条 critical 全部是 R3 补强动作自身引入或未修复的** (C-1/C-2 是 R3 处方无效, C-3/C-4 是 R3 新造表面)。按 memory `stop-adding-rounds` 与 `marginal-return-negative`: **本轮 fix 引入的 major 占比过半 ⇒ 已到拐点, 加轮不如换新鲜眼睛 / 由 owner 裁方向。**

---

# 附记 — 被审文件在本轮审计**进行中**被改动 (主控)

本席**未修改任何被审文件** (`git status` 中三份 proposal 的 `M` 不是本席所为)。收尾时实测:

```
$ git status --porcelain
 M openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
 M openspec/changes/linked-issue-field-availability/proposal.md
 M openspec/changes/sibling-spec-probe/proposal.md
$ git diff --stat openspec/changes/     # 6 +-  /  29 ++  /  34 ++--
```

主控已就地写入一条 `R4/C-1 订正`, 与本席 C-1 的前半 (「引用了 §2.1a 明说不存在的 compose 函数」) 结论一致。**但该订正没有解决 C-1 的承重那半**:

1. 订正把处方改为「夹具**按 §2.1 规则手写拼接**」—— 而 R3 判 SC-2 恒绿的原话正是「它传**两个手写的**、不含容器段的 track 名, **今天就绿**」。⇒ 恒绿的**量**没有变, 只是把禁止手写改回允许手写;
2. **本席的实跑证据对订正后的版本同样成立**: 手写含容器段的两串 ⇒ 双方各含对方 (绿); 手写空容器段 ⇒ 双方为空 (绿)。**两臂在 `d50f9c3` 上全绿, 与夹具是手写还是派生无关**;
3. 订正段落自身仍留有矛盾: 臂 (ii) 的措辞未同步, 仍写「把 **compose** 的 container 段置空」—— 上一句刚说明 compose 不存在。

⇒ **C-1 维持 critical**, 处方仍是本报告给的 (a)/(b) 二选一 (换量到文本层, 或把 compose 变成真代码并撤销 §2.1a 的「不新增拼接函数」句)。

**流程提示 (memory `feedback_concurrent_duplicate_audit_fetch_before_start`)**: 审计轮进行中就地改被审文件, 会让同轮各席的引用行号与结论对不同版本的文本 —— 本报告全部行号/引文对应的是**本席读取时刻**的版本 (主仓 `322f280` 工作树, 改动落盘前)。
