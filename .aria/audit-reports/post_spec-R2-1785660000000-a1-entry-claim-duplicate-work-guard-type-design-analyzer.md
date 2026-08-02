---
checkpoint: post_spec
round: 2
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R2 (新鲜眼睛, 定向) — type-design-analyzer

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=4 minor=4

> **席位**: 1/1 (定向轮, 类型与契约设计视角) · 未参与 R1
> **审计对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (工作树 08-02 13:11 版, 317 行)
> **方法**: 所有引用行号均实读; 所有 finding 均配可复跑证据 (4 个只读探针脚本 + 真实 `refs/aria/coordination` 语料 + 139 篇 proposal prose 语料统计)。零写入、零 commit。

---

## 三处新承重逻辑的契约评估

| 逻辑 | 契约是否良定义 | 依据 |
|---|---|---|
| **§0 `linked_issue` 归一 — 等价关系本体** | ✅ **是** (本轮唯一完全过关的一处) | 18 元语料穷举 permutations: 自反 / 对称 / **传递** 零违例。传递性不被「可解析→键比较 / 不可解析→原串精确比较」的双语义破坏, 因为跨类相等要求原串完全相同, 而原串相同则解析性必相同 ⇒ 论域被干净划分为两个不相交子集, 各自内部是等价关系。**R1-fix 的 §299 担心「会不会破坏传递性」—— 不会, 这条设计对了。** |
| **§0 归一 — 边界/极性/欠定** | ⚠️ **部分** | 键 `(basename.casefold(), number)` 本身良定义, 但 (a) `number` 按 str 还是 int 比较未定 (`#007` vs `#7` 两解相反); (b) `#` 前空白剥、`#` 后空白不剥, 处理不对称; (c) 声明的 fail-toward-reporting 极性**只在 org 轴成立**, basename 轴是精确匹配 ⇒ 对语料里真实存在的仓名别名恒漏 (M2); (d) 最重的「org 不参与匹配」**零 SC 覆盖**, 两种相反实现同过 SC-1a+SC-1b (M1)。 |
| **`include_terminal` 参数** | ❌ **否 — 生产路径上不可达** | `linked_issue_overlaps` 全仓**唯一生产调用点** = `phase1_gate.py:1232`, 位置在 `_main()` 内, Phase B 与 A.1 走**同一条** CLI 路径。CLI 无 `--include-terminal`, `_main` 无按 phase 分支, 而 §非目标:242 + Impact:255 把 `phase1_gate.py` 的改动范围**穷举为「只加 error 契约」**。⇒ 「A.1 调用点传 True」在本 Spec 声明的 scope 内没有载体, SC-5 只能被 lib 层单测满足 (C2)。附带: 「默认 False 保既有调用方语义不变」字面属实但**论证是空的** —— 既有调用方只有 1 个, 且正是 A.1 要复用的那一个。 |
| **issue 派生 track-id** | ❌ **否 — 与主机制的信号通道互斥** | `<basename>-<number>` 使两个容器对同一 issue 得到**同一个** `track_id`, 而 `collision.py:219` 按设计排除 `c.track_id == own_track_id` (committed 测试 `test_same_track_not_flagged` 逐字钉住该契约) ⇒ `linked_issue_overlap` 恒 `[]`。§0 归一与 `include_terminal` 在这条路径上**全部失效**。唯一残余通道 (reconcile 7c `occupied` surface) 在 **STALE_TTL=30min** 后熄灭 —— 与 SC-10 要求的 ≥72h 差 144 倍 (C1)。 |

**必审项 — 与既有 SC 的一致性结论**:

| SC | 钉住了吗 | 说明 |
|---|---|---|
| SC-1a | 部分 | 能杀「裸 `!=`」的现状; 但**不能**区分「org 不参与匹配」与「两侧都有 org 才比 org」两种实现 (M1 实证) |
| SC-1b | ✅ | 有效负控, 能杀「只比 number」的退化实现 |
| SC-1c | 部分 | 三个不可解析用例正确; 漏 `#007` / `repo# 122` 两个欠定分支 (m2) |
| SC-5 | ❌ | 在 §1 强制的同 track-id 形态下, 被 `:219` 先行排除, `include_terminal` 根本轮不到生效 (C1); 且只能在 lib 层验, 无 CLI 层断言 (C2) |
| SC-10 | ❌ 谓词选错 | 钉的是 `status == active`, 而 §1 形态下的检出判据是 **heartbeat 新鲜度** (`_takeover_eligible`)。claim 可以既 `active` 又对两条轴同时不可见 ⇒ 恒绿 |
| SC-11 | 部分 | (b) 「issue 派生 track-id 改名前后不变」按构造恒真 (该串不以 slug 为输入); 真正危险的是**无 issue 的 slug 回落分支**, 无 SC 覆盖 —— 本 Spec 自己的 live claim 就在这条分支上且已成孤儿 (m3) |
| **缺失** | — | `yielded` 状态在 SC-2 (active) 与 SC-5 (done) 之间**无归属** (M3) |

---

## Findings

### [CRITICAL] C1 — §1 的 issue 派生 track-id 与 `linked_issue_overlaps` 的 `own_track_id` 排除互斥, 主机制信号通道恒空; 残余通道 30min 熄灭, 与 SC-10 的 ≥72h 直接矛盾

- **位置**:
  - `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:125` (§1 `--raw-track-id` 取值订正)
  - `aria/skills/state-scanner/lib/collision.py:219`
  - `aria/skills/state-scanner/scripts/phase1_gate.py:648-676` (7c `occupied` 分支) / `:282-293` (`_takeover_eligible`)
  - `aria/skills/state-scanner/lib/constants.py:36` (`STALE_TTL = 1800`)
  - `proposal.md:231` (SC-10)

- **问题**: `linked_issue_overlaps` 的语义**按设计**是「同 issue、**不同名字**」—— docstring:182 写 `under a DIFFERENT track_id`, `:219-220` 写 `same-name collision — reconcile's job, not ours`。§1:125 把 A.1 的 track-id 从「spec-slug / carry-id」改成「issue 派生的稳定串」, 恰恰**消灭了「不同名字」这个前提**: 两个容器对同一 issue 必然算出同一个 `track_id` ⇒ 命中 `:219` 被 `continue` ⇒ 返回 `[]`。

  §0 的归一 (C1 修复) 与 `include_terminal` (C2 修复) 在这条路径上**都白修** —— 无论 `linked_issue` 是否归一成功、无论终态是否放行, 都在 `:219` 前功尽弃。

  唯一残余检出通道是 reconcile 轴 (同 track_id 由 `reconcile_all` 分组, advisory 模式下产生 `surface.kind="occupied"`)。但该通道有两个致命属性:
  1. **它按 heartbeat 新鲜度门控, 不按 status**: `:649-652` 要求 `not _takeover_eligible(verdict)`, 而 `_takeover_eligible` 在 `verdict_reason` 含 `stale_takeover_eligible` 时为 True, 阈值是 **`STALE_TTL = 1800s = 30 分钟**。`constants.py:38-51` 的注释已明写「**NO production heartbeat loop exists** … every live claim's heartbeat_at is frozen at acquire time」(grep 复核: `heartbeat()` 定义在 `claim_lifecycle.py:178`, 零生产调用点)。⇒ A.1 claim 打下后 **30 分钟**, `occupied` surface 就不再触发。
  2. **它的 JSON 投影不含 SC-2 要求的字段**: `_gate_result_to_dict` (`:1150-1156`) 的 `competing_winner` 只有 `{owner, container}`; `surface` (`:1141-1149`) 只有 `{kind, message, carry_id, winner_owner_container, winner_heartbeat_age_min, max_clock_skew_seconds, push_error_kind}`。**没有** `claimed_at`、**没有** `status`、**没有** `linked_issue`、`carry_id` 等于自己的 track_id。而 SC-2 (`:223`) 要求告警含「对方 track-id / owner-container / **claimed_at** / 双方 linked_issue 原始串 / **status**」。

  合起来: §1 把保护窗从「status 驱动的 24h」(overlap 轴, 只看 `status not in _TERMINAL`, 不看 heartbeat) 降级成「heartbeat 驱动的 30min」(reconcile 轴)。**方向与 C3/SC-10 完全相反, 且是在同一次 R1-fix 里同时引入的。**

  这条与 R1 的 C1 是同一个失败形状 (「机制存在、返回值合法、恒空」), 只是这次的成因不是格式失配而是**命名策略**。且它有自我加剧性: 越多轨采用 §1 的命名约定, 主机制越瞎 —— 历史 claim (spec-slug 命名) 反而还看得见。

- **证据** (可复跑):

  1. 归一做到完美也返回 `[]`:
     ```
     L.track_id = 'aria-plugin-122'   R.own_track_id = 'aria-plugin-122'
     overlap (current code, no normalisation)                = []
     overlap (even with §0 normalisation, identical strings)  = []
     overlap (pre-M1-CR design, track_id='sha256-0d6bc21…')   = [{...'aria-plugin#122'...}]   ← 只有名字不同才看得见
     ```
  2. **committed 测试逐字钉住该契约**: `aria/skills/state-scanner/tests/test_release_by_track.py:232-234`
     ```python
     def test_same_track_not_flagged(self):
         claims = [self._claim("mine", "cB", linked="A#7")]
         self.assertEqual(linked_issue_overlaps(claims, "mine", "A#7"), [])
     ```
     ⇒ 不是实现瑕疵, 是被测试固化的设计意图。§1 与它正面冲突, 而 Spec 全文未提。
  3. 残余通道 30 分钟熄灭 (纯函数 `reconcile` + `_takeover_eligible`, 无写入):
     ```
     STALE_TTL = 1800s (30 min)   SWEEP_TTL = 86400s (24 h)
     L age     5 min: reason='sole_active'                         → 7c 'occupied' fires: True
     L age    29 min: reason='sole_active'                         → 7c 'occupied' fires: True
     L age    31 min: reason='sole_active+stale_takeover_eligible' → 7c 'occupied' fires: False
     L age  1440 min: reason='sole_active+stale_takeover_eligible' → 7c 'occupied' fires: False
     L age  4320 min: reason='sole_active+stale_takeover_eligible' → 7c 'occupied' fires: False   ← SC-10 目标 72h
     ```
  4. Spec 全文对 TTL 只提 `SWEEP_TTL` (`:151`, `:231`), **零处提 `STALE_TTL`** —— §3a 的「保护窗 24h vs 事故窗 48-72h」分析选错了绑定阈值: 在它自己 §1 造出的同 track-id 形态下, 绑定阈值是 30 分钟。

- **建议修法** (Phase A.2 二选一定死, 与「危害=检出通道被命名策略掐断」方向一致):
  - **(i) 放弃 §1:125 的 issue 派生 track-id**, A.1 仍用 spec-slug / carry-id, 让 overlap 轴 (status 驱动, 天然覆盖 24h 直到 sweep) 承担检出; §3c 的改名孤儿改用「release-then-acquire 两步」解决 (§3c 本来就并列给了这条)。**代价最小, 且让 §0 + `include_terminal` 两项修复真正生效。**
  - **(ii) 保留 issue 派生 id**, 则必须同时:
    - 把 A.1 消费面从「只读 `linked_issue_overlap[]`」改为「**reconcile 轴 ∪ overlap 轴**」, 并在 §1 写死两轴各自的触发条件;
    - 把 `claimed_at` / `status` / 对方 `track_id` / `linked_issue` 补进 `competing_winner` 的 JSON 投影 —— 这是 `phase1_gate.py` 的**结构性改动**, 必须写进 §Impact 与 §非目标:242 的 scope 枚举, 否则 SC-2 的字段清单无实现载体;
    - §3a 的 heartbeat 方案必须按 **STALE_TTL=30min** 设计 (每 ≤30min 一次), 不是按 SWEEP_TTL=24h; 并注明 `heartbeat()` 目前**零生产调用点**, 这是 greenfield 而非「接上既有回路」。
  - 无论走哪条, **SC-10 的谓词必须换**: 从「`status` 仍为 `active`」换成「**72h 后再跑一次 A.1 认领, 断言告警仍被渲染**」(端到端可证伪, 而非字段值)。现写法在 (ii) 下恒绿。

---

### [CRITICAL] C2 — `include_terminal=True` 在唯一生产调用路径上不可达, SC-5 只能被单测满足

- **位置**: `proposal.md:132` (「A.1 调用点传 True」) vs `proposal.md:242` (§非目标 scope 枚举) + `proposal.md:255` (Impact 表 `phase1_gate.py` 行) + `proposal.md:226` (SC-5); 实现侧 `aria/skills/state-scanner/scripts/phase1_gate.py:1229-1237`

- **问题**: 全仓 grep (`aria/` + `standards/`) 确认 `linked_issue_overlaps` 的**生产调用点只有一处** —— `phase1_gate.py:1232`, 在 `_main()` 里, 参数是位置传参 `(claims, result.track_id, args.linked_issue)`。Phase B 认领与 §1 的 A.1 认领**走的是同一条 CLI 路径**, 二者在代码里唯一的区别是 `--phase` 这个自由字符串的值。

  而 Spec 明确把 `phase1_gate.py` 的改动范围锁死为「fetch 降级进 JSON `error` 契约」:
  - `:255` Impact 行: 「**R1-fix/M7**: fetch 降级进 JSON `error` 契约 (SC-13)」— 无第二项;
  - `:242` §非目标: 「改为: 只改 `lib/collision.py` 的匹配谓词与 `include_terminal` 参数 **+ `phase1_gate` 的 `error` 契约 (M7)**」— 穷举式措辞。

  ⇒ 在 Spec 声明的 scope 内, **没有任何机制能把 `include_terminal=True` 送到 A.1 那次调用**。SC-5「主机制: 同 issue 他轨 claim 状态为 `done` ⇒ 可见」只能靠直接调 lib 函数的单测通过, 而生产 CLI 输出的 `linked_issue_overlap` 仍然对 `done` 失明。这正是本 Spec 自己援引的 `feedback_completion_signals_vs_runtime_invocation` 的形状 (「代码存在、有测试、被调用过」≠ 生产路径上被调用), 也正是 R1 用来推翻本 Spec 核心卖点的同一把尺子。

  **类型设计层面的附带问题**: 「默认 False 保持既有调用方语义不变」这句在字面上属实 (加 keyword-only 默认参数对 1 个生产调用点 + 4 处单测确实零影响), 但**论证是空的** —— 「既有调用方」就是 A.1 要复用的那一个。更根本的是, 这个布尔开关让返回值的**含义**随参数漂移: `list[dict]` 在 False 时是「活跃竞品」, 在 True 时是「任意历史 claim」, 而返回类型完全相同, 调用方无法从类型上分辨自己拿到的是哪一种, 只能靠自己重新按 `status` 分档 —— 而 §1 恰恰要求按 `status` 分出三种措辞。

- **证据**:
  - `grep -rn "linked_issue_overlaps" aria/ standards/` 命中: 定义 1 (`collision.py:177`) + import 2 (`phase1_gate.py:81,119`) + 生产调用 1 (`:1232`) + 单测 5 (`test_release_by_track.py`) + 文档 3。无第二个生产调用点。
  - `phase1_gate.py:1198-1205` 的 `--linked-issue` 定义旁**无** `--include-terminal`; `:1229-1237` 的调用为三位置参数, 无 kwarg 穿线点。
  - `phase1_gate.py:1189-1191`: `--phase` 是 `required=True` 的自由字符串 (对照 `--mode` 在 `:1195` 有 `choices`) —— 若实现者选择按 `--phase` 隐式分派, 见 M4。

- **建议修法** (与危害「参数在生产路径不可达」方向一致):
  1. §Impact 的 `phase1_gate.py` 行与 §非目标:242 的 scope 枚举**各补一项**: 新增 `--include-terminal` (store_true, 默认 False) 并穿线到 `:1232`; A.1 的 SKILL.md 命令模板显式带该 flag。**不要**按 `--phase` 字符串隐式分派 (见 M4)。
  2. **SC-5 升级为 CLI 层断言**: 跑真实 `phase1_gate.py … --linked-issue <x> --include-terminal`, 断言 stdout JSON 的 `linked_issue_overlap` 含该 `done` 条目 —— lib 层单测保留但不作为 SC-5 的宿主。仓内已有 CLI 层测试先例 (`test_release_by_track.py:529` 那组「lib 层测试锁不住 kwarg 穿线拼写错」的 CLI 测试), 逐字复用其结构即可, 无新宿主成本。
  3. **类型层可选简化** (若 A.2 愿意): 既然生产调用点只有 1 个, 「保既有语义」的收益为零 —— 可让函数**恒返回全部同 issue claim** (每条已带 `status`), 把 active/terminal 的分档与措辞放到唯一的渲染层。这样开关消失, C2 的不可达问题从源头不存在, 且 §1 要求的三档措辞天然落在正确的层。代价: Phase B 的现有渲染面也会看到 `done` 条目, 与 §非目标:244「Phase B 照旧」冲突 ⇒ 若不接受此代价, 走方案 1。

---

### [MAJOR] M1 — SC-1a/1b 无法区分「org 不参与匹配」与「两侧都有 org 才比 org」, §0 论证最重的一条规则零覆盖

- **位置**: `proposal.md:100` (§0 步骤 3 「**`org` 不参与匹配**」) + `:103` (整段极性论证) vs `:220` (SC-1a) / `:221` (SC-1b)

- **问题**: §0 花了一整段 (`:103`) 论证「org 不参与匹配」是深思熟虑的 fail-toward-reporting 取舍, 但 SC 表里**没有任何一条能证伪它的反面实现**。一个「两侧都有 org 时才比较 org, 有一侧缺 org 就忽略」的实现 —— 这是拿到 §0 文字后相当自然的第二种读法 —— 会**同时通过 SC-1a 与 SC-1b**, 而在 §0 唯一点名的分歧案例上给出相反结果。

  这落在 `feedback_spec_underdetermination_two_implementer_test` 的形状上: 两个独立实现者同规格得相反结果 = 欠定实证。而 §0 自称「钉到字符级」。

- **证据** (穷举验证):
  ```
  实现                            SC-1a pass   SC-1b pass
  §0 (org ignored)                   True         True
  org-when-both (违反 §0 步骤 3)      True         True
  唯一分歧点 (无任何 SC 覆盖):
    10CG/aria-plugin#122 × evil/aria-plugin#122
      §0            -> True   (按 §0:103 这是**故意**的误报, 靠回显原串人工判别)
      org-when-both -> False  (静默漏报 —— 正是 §0 极性论证要避免的那一半)
  ```
  SC-1a 的三个配对 (A×B, A×C, B×C) 中, B 与 C 的 org 都是 `10CG` (相等), A 无 org (被当通配) ⇒ 两种实现在这三对上行为完全一致。

- **建议修法**: SC 表增 **SC-1d (C1 正控)**: `10CG/aria-plugin#122` × `otherorg/aria-plugin#122` ⇒ **必须命中**, 且返回条目回显双方 `linked_issue` 原始串。「怎么会红」= 任何比较 org 的实现必红。这条与 SC-1b (同 org 不同仓不得命中) 构成正交的二维负控/正控对, 才真正把 `(basename, number)` 这个键钉死。

---

### [MAJOR] M2 — §0 声明的 fail-toward-reporting 极性只在 org 轴成立; basename 轴是精确匹配, 对语料里真实存在的仓名别名恒漏, 且取样语料与实际输入语料不是同一个

- **位置**: `proposal.md:86-94` (三族实测表, 取样自 `refs/aria/coordination`) + `:100` (步骤 3) + `:103` (极性论证) vs `:127` + `:262` (M1 规定输入来自 proposal 「关联 Issue」prose 字段)

- **问题**: §0 的极性论证只覆盖了 `org` 这一维 (「多一行告警是便宜的」)。但比较键的另一维 `basename` 用的是 **casefold 后精确相等** —— 任何缩写、别名、少写前缀都会**静默漏报**, 方向与声明的极性**相反**。

  这不是理论风险: R1-fix 的三族表取样自 **`refs/aria/coordination` 的 13 条机器写入记录**, 而 §1:127 + M1 (`:262`) 规定 `--linked-issue` 的取值来自 **proposal 头部「关联 Issue」prose 字段** (M1 要把它写进模板)。两个语料不是同一个。对 139 篇 proposal + `docs/` 的 prose 语料实测, 至少有**两个仓**在日常书写里有两套名字:

  | 仓 | 写法 A | 出现次数 | 写法 B | 出现次数 | §0 判定 |
  |---|---|---|---|---|---|
  | aria-orchestrator | `aria-orch #16` | **24** | `aria-orchestrator #10` | **10** | ❌ 不匹配 (漏报) |
  | aria-standards | `standards #9` | 13 | (真名 `aria-standards`) | — | ❌ 不匹配 (漏报) |

  ⇒ 两个容器一个写 `aria-orch #16`、一个写 `aria-orchestrator #16`, 归一后仍然互不可见 —— **C1 要根治的漏报, 在 basename 轴上原样存活**。

- **证据**:
  - `grep -rhoE '\baria-orch[a-z]* ?#[0-9]+' openspec/ docs/ | sed -E 's/ ?#[0-9]+//' | sort | uniq -c` → `24 aria-orch` / `10 aria-orchestrator`
  - `standards #9` / `standards#5` / `standards #4` … 共 13 处, 而 Forgejo 仓名是 `10CG/aria-standards`
  - 对照: `Aria` vs `aria` 的 casefold 论断 (`:105`) **经语料复核属实** —— 主仓一律写 `Aria#8` / `Aria #124`, 零处裸 `aria#N`。这半条设计对了。

- **建议修法** (二选一, 与危害「声明极性与 basename 轴实际极性相反」方向一致):
  - (a) §0 增第 5 步: basename 先经一张**成文别名表**归一 (仅 4 个 Lab 仓, 表极小), 并加 SC: `aria-orch#16` × `aria-orchestrator#16` 必须命中;
  - (b) 若不做归一, 则 §0:103 的极性论证必须**收窄措辞**为「fail toward reporting **仅在 org 维**成立; basename 维是精确匹配, 别名/缩写属已知漏报」, 并把这条写进 §4 残余缺口表 (与该节「no silent caps」原则一致), 同时 A.1 消费面在零命中时措辞为「未发现**同名仓**的同 issue claim」而非「无碰撞」。
  - 无论哪条, §0 的三族表应注明取样来源是 ref (13 条), 并补一行 prose 语料里最高频的族 (见 m4)。

---

### [MAJOR] M3 — `yielded` 状态在 SC-2 (active) 与 SC-5 (done) 之间无归属; §0 归一一旦落地, 历史 `yielded` 记录会以「活跃竞品」形态触发 AskUserQuestion

- **位置**: `aria/skills/state-scanner/lib/collision.py:210` (`_TERMINAL` 不含 `yielded`) + `aria/skills/state-scanner/lib/claim_schema.py:56` (`STATUS_ENUM` 含 `yielded`) vs `proposal.md:223` (SC-2, 措辞「active claim」) / `:226` (SC-5, 「`done`」) / `:130-131` (消费面: overlap 非空 ⇒ 🔴 + `AskUserQuestion` 请裁)

- **问题**: `STATUS_ENUM = {active, yielded, done, abandoned, unknown}`, 而 `_TERMINAL = ("done","abandoned","unknown")` —— **`yielded` 既不终态也不 active**, 它落在 `include_terminal=False` 的**放行**一侧。`yielded` 的语义是「我主动让出了这条轨」, 恰恰是「对方不在做」。

  今天这个洞是隐形的 (格式失配导致恒空)。**§0 归一修好之后它立刻显形**: 消费面 §1:130-131 规定「overlap 非空 ⇒ 🔴 + `AskUserQuestion` 请裁」, 于是一堆早已让出的历史记录会把 A.1 打断成请裁。

  这是 C1 修复的**已知副作用**, 而 SC 表没有任何一条覆盖 `yielded`: SC-2 说 active, SC-5 说 done, 中间这一档无人认领。

- **证据** (对真实 `refs/aria/coordination` 跑 §0 归一后的重实现, 25 条 claim / 15 条带 linked_issue):
  ```
  --- A.1 for 'aria-plugin#110'  (§1 track_id='aria-plugin-110')
     include_terminal=False: [(…,'yielded','10CG/aria-plugin#110','B'),
                              (…,'yielded','10CG/aria-plugin#110','B'),
                              (…,'yielded','10CG/aria-plugin#110','B')]
     include_terminal=True : [(…,'done',…), + 上面 3 条]
  ```
  即: 归一生效后, 一次针对 `aria-plugin#110` 的 A.1 认领会在 `include_terminal=False` 下就返回 **3 条 `yielded`**, 全部来自同一 container / 同一 track / phase B, 而该工作实际已 `done`。⇒ 3 行几乎相同的 🔴 + 一次不必要的请裁。

- **建议修法**: §1 消费面补一张 **status 分档矩阵**, 并各配 SC:

  | status | 可见性 | 措辞 | 是否 `AskUserQuestion` |
  |---|---|---|---|
  | `active` | 是 | 🔴 同 issue 有活跃轨 | **是** (SC-2 已覆盖) |
  | `yielded` | 是 | ⚠️ 曾有轨认领后让出 | **否** (仅提示) ← **新增 SC** |
  | `done` | `include_terminal=True` 时是 | ⚠️ 该 issue 可能已被解决 | 否 (SC-5 已覆盖可见性, 补措辞断言) |
  | `abandoned` | 同上 | ⚠️ 曾有轨放弃 / 被 sweep | 否 |

  另: 返回条目按 `(track_id, container)` 去重或折叠 (`:232` 现按 `(track_id, owner, container)` 排序但不去重), 避免同轨多 session 刷屏。

---

### [MAJOR] M4 — §0 的键归一 (casefold) 与既有 `derive_track_id` 的归一 (lower + `/._`→`-`) 未组合, §0 判为「不同 issue」的值会映射到同一 track_id; 且 `--phase` 自由字符串正被推向承重的分派角色

- **位置**: `proposal.md:96-101` (§0 键归一) + `:125` (§1 track-id 派生) + `:158` (§3a 方案 ii「为 `phase` 以 `A` 开头的 claim 单独配置更长 TTL」) vs `aria/skills/state-scanner/lib/track_id.py:154-170` (`derive_track_id` 四步) + `aria/skills/state-scanner/scripts/phase1_gate.py:1189-1191` (`--phase` 无 `choices`)

- **问题 (a) — 两套归一未组合**: §0 的 basename 归一只做 `casefold()`; 而 `<basename>-<number>` 这个串随后要过 `derive_track_id`, 它额外做 `.lower()` + `str.maketrans({"/":"-", ".":"-", "_":"-"})` + 64 截断 + 非 ASCII/超长走 sha256。⇒ **§0 认为不同的 issue, track-id 层认为相同**。

- **问题 (b) — `--phase` 被推向承重分派**: C2 若走「隐式分派」路线 (按 `--phase` 判断是否 `include_terminal`), 以及 §3a 方案 (ii) (按 `phase` 以 `A` 开头配长 TTL), 都会让 `--phase` 从「写进 claim 的自由描述串」变成**控制流判别式**。而 D6 (`:193`) 明确把「`--phase` 无 `choices` 约束」当作本方案的承重前提。一个既无枚举域、又无校验、且被文档化为「自由字符串」的字段, 同时承担两处分支语义 ⇒ `a.1` / `Phase A.1` / `A1` 全部合法输入且**静默走错分支**。生产 ref 里现存的 phase 值已有 `A` / `A.1` / `B` / `C` / `D` / `D.2` 六种写法。

- **证据**:
  ```
  '10CG/aria_plugin#122'     §0 key=('aria_plugin', '122')  ->  §1 track_id='aria-plugin-122'
  '10CG/aria.plugin#122'     §0 key=('aria.plugin', '122')  ->  §1 track_id='aria-plugin-122'
  '10CG/aria-plugin#122'     §0 key=('aria-plugin', '122')  ->  §1 track_id='aria-plugin-122'
  ```
  三个 §0 判定为**不同** issue 的值, 塌成**同一个** track_id ⇒ 既不出 overlap 告警 (§0 说不同), 又在 reconcile 轴上互相抢占 (track-id 说相同)。两条轴给出**相反**的身份判定。
  `derive_track_id` 侧另一条: `casefold()` 与 `.lower()` 并非同一函数 (`'ß'.casefold()=='ss'` vs `'ß'.lower()=='ß'`), 同一「大小写归一」概念在两处用了两个实现。

- **建议修法**:
  - (a) §1:125 把派生串写死为 `derive_track_id(f"{basename}-{number}")`, **且 §0 的 basename 归一改为与 `derive_track_id` 同款** (casefold → `lower`, 并同样 translate `/._`→`-`), 使两套归一可组合; 加一条**双向** SC: 「§0 key 相等 ⟺ §1 track-id 相等」。若 C1 采纳方案 (i) (放弃 issue 派生 track-id), 本条 (a) 自动消解, 只需保留「§0 用 `lower` 还是 `casefold`」的字面钉死。
  - (b) **禁止按 `--phase` 隐式分派**。`include_terminal` 用显式 `--include-terminal` flag (见 C2); §3a 若选方案 (ii), 也须用独立的显式参数或在 claim 里存一个受控枚举字段, 不要给 `--phase` 加语义 —— 否则 D6 的「自由字符串」前提与新的分支语义直接互斥。

---

### [MINOR] m1 — §1 承诺的 `unknown` 分档措辞不可达

- **位置**: `proposal.md:132` (「`abandoned` / `unknown` 同样回显但措辞区分」) vs `aria/skills/state-scanner/lib/claim_schema.py:219-230` + `aria/skills/state-scanner/lib/collision.py:215`
- **问题**: `status="unknown"` 只由 `parse_claim` 的 schema-version sentinel 分支产生 (`claim_schema.py:219-230`), 该 `ClaimRecord` **不传 `linked_issue`** ⇒ 取默认 `None` (`claim_schema.py:127`)。而 `collision.py:215` 在 status 判定**之后**、比较**之前**就把无 `linked_issue` 的 claim `continue` 掉。⇒ 无论 `include_terminal` 是 True 还是 False, `unknown` 条目**永远不可能**出现在 overlap 列表里。
- **证据**: `claim_schema.py:219-230` 的 `ClaimRecord(...)` 构造 kwargs 逐字核对: `schema_version / track_id / owner / container / session / phase / status / claimed_at / heartbeat_at / superseded_from` —— 无 `linked_issue`。
- **建议修法**: 删掉 `unknown` 的措辞承诺 (它不是一个可达分支); 若确实想暴露「有 claim 但 schema 读不懂」, 改成独立契约: `read_claims` 的 degraded 计数进 `error` 字段 (与 M7 的 fetch 降级同一处), 消费面报「N 条 claim 无法解析, 本次核对不完整」。

---

### [MINOR] m2 — §0 自称「钉到字符级」但两处欠定: `number` 的 str/int 比较, 与 `#` 两侧空白处理不对称

- **位置**: `proposal.md:98` (步骤 1「`number` 必须是纯数字」) + `:99` (步骤 2「`left` 剥尾部空白」) vs `:222` (SC-1c 的三个用例)
- **问题**:
  - `#007` vs `#7`: 两者都过「纯数字」判定, 但比较是字符串还是整数未定 ⇒ 两个独立实现者得相反结果。
  - 空白规则只对 `left` 剥尾部, 对 `number` 侧**完全不剥** ⇒ `repo #122` 能解析、`repo# 122` **落进不可解析分支**走原串精确比较。同一个「书写时多打一个空格」的错误, 位置不同结果类别不同。
  - 「纯数字」用 `str.isdigit()` 还是 `str.isdecimal()` 还是 `int()` 亦未定 (三者对 Unicode 数字/上标行为不同)。
- **证据**:
  ```
  '#007' vs '#7' : str-compare -> False | int-compare -> True
  '10CG/aria-plugin #122' vs 'aria-plugin#122' -> True
  'aria-plugin# 122'      vs 'aria-plugin#122' -> False
  ```
- **建议修法**: §0 步骤 1 改为「`number = number.strip()`; 用 `str.isdecimal()` 判定; 比较用 `int(number)`」(或明确选字符串比较, 二选一但必须写死); 步骤 2 的 strip 同时作用于 `left` 与 `number` 两侧。SC-1c 增两个用例: `aria-plugin#007` × `aria-plugin#7` (按选定语义断言) 与 `aria-plugin# 122` × `aria-plugin#122`。

---

### [MINOR] m3 — §闸门待裁:315 的自认领声明与 ref 实据不符; 且该 claim 现在就是一条 §3c 描述的孤儿, 落在 SC-11 未覆盖的那半

- **位置**: `proposal.md:315` (「已按 §1 的形态为本轨补认领, track-id 用 §1 订正后的 issue 派生形」) vs `refs/aria/coordination:claims/023236f2/s-550f@1309.yaml`
- **问题**: ref 实据:
  ```yaml
  claimed_at: '2026-08-02T13:09:53Z'
  container: 023236f2
  phase: A.1
  status: active
  track_id: aria-a1-entry-claim-guard
  ```
  (a) **无 `linked_issue` 字段** ⇒ 该 claim 对所有未来的 A.1 探测**不可见** (`collision.py:215` 直接 skip), 主机制对本轨零保护;
  (b) `aria-a1-entry-claim-guard` **不是** issue 派生形 (本 Spec 头部本就无「关联 Issue」, 按 §1 应走 slug 回落 —— 声明措辞与实际不符);
  (c) 它也**不是**本 Spec 的 slug (`a1-entry-claim-duplicate-work-guard`) ⇒ 若走到 D.2b, `release_claim_by_track` 按 slug 定位会 `claim_not_found`, 这条 active claim 会一直挂到 24h sweep。**§3c 描述的改名孤儿, 在 R1-fix 当天就现场发生了一例。**
- **建议修法**: 订正 `:315` 措辞为实况 (「已补认领, 但走 slug 回落且未传 `--linked-issue`」—— 这本身是比原文更强的自指论据); **SC-11 增 (c)**: 无关联 issue 的 spec 走 slug 回落分支时, track-id 与 spec-slug 不一致或发生改名 ⇒ 必须 release-then-acquire, 断言旧 track 无残留 active claim。现 SC-11(b) 只覆盖了「issue 派生」这条**按构造就不会出问题**的分支 (该串不以 slug 为输入, 恒真), 真正会出事的回落分支无人认领。

---

### [MINOR] m4 — §0 三族表漏了 prose 语料里最高频的一族 (取样口径未标注)

- **位置**: `proposal.md:86-94` (三族表 + 「实测条数」栏)
- **问题**: 三族表取样自 `refs/aria/coordination` (13 条), 但 §1:127 + M1 (`:262`) 规定实际输入来自 proposal prose。prose 语料里**最高频**的写法是「裸仓名 + 空格 + `#`」: `Aria #124` (78×) / `aria-plugin #113` (17×) / `aria-plugin #122` (16×) —— 既非族 A (`aria-plugin#122`, 无空格) 也非族 C (`10CG/aria-plugin #122`, 带 org)。
  **四步规则本身能正确处理它** (strip → rsplit(`#`) → `left.rstrip()` → basename), 这不是缺陷; 缺陷在于族表让读者以为输入语料只有 13 条 ref 记录, 从而漏掉了 M2 那类只在 prose 里出现的问题。
- **证据**: `grep -rhoE '[A-Za-z0-9._/-]*[Aa]ria[A-Za-z0-9._-]*[ ]?#[0-9]+' openspec/ docs/ | sort | uniq -c | sort -rn` → top: `78 Aria #124`, `24 Aria #165`, `17 aria-plugin #113`, `16 aria-plugin #50`, `16 aria-plugin #122`。
- **建议修法**: 族表增一行「D: `aria-plugin #122` (裸仓名 + 空格) · 来源 proposal prose · 实测 139 篇语料中最高频」, 并在表头标注两个取样面 (ref 13 条 / prose 139 篇) 各自的条数口径。

---

## OUT_OF_SCOPE (与本轮三处新逻辑无关, 仅供 owner 参考, 不计入 counts)

- `aria/skills/state-scanner/scripts/release_gate.py:225` 的 `--sweep-stale` help 写「heartbeat 超 **STALE_TTL** → abandoned」, 而 `lib/gc.py:341,355-359` 的实现默认是 **SWEEP_TTL (24h)** 且注释明写「NOT STALE_TTL (30min)」。help 文案与实现相差 48 倍。这条与本 Spec 无关 (非 R1-fix 引入), 但它是 §3a 作者读到的第一手资料, 可能正是 §3a 只讨论 SWEEP_TTL、完全没提 STALE_TTL 的原因之一。

---

## 经核实**设计正确**的部分 (下轮免重复审)

1. **§0 的比较键是良定义的等价关系** —— 自反 / 对称 / **传递**在 18 元语料上穷举 permutations 零违例。R1-fix `:297-299` 担心的「不可解析值退回精确比较会不会破坏传递性」**不会**: 可解析与不可解析两类之间不可能跨类相等 (跨类相等要求原串完全相同, 而原串相同则解析性必相同), 论域被干净划分。**这处设计对了, 且是本轮唯一完全过关的契约。**
2. **「按最后一个 `#` 拆分」对现实语料无害** —— GitHub/Forgejo 仓名不允许 `#`; 139 篇 prose 语料零反例。R1-fix `:297` 点名的这个担心可以关闭。
3. **`Aria` vs `aria` 的 casefold 论断 (`:105`) 属实** —— 语料复核: 主仓一律写 `Aria#8` / `Aria #124`, 零处裸 `aria#N`; `10CG/Aria#147` × `10CG/aria-plugin#147` 的负例保护也确实成立。
4. **SC-1b 是有效负控** —— 能杀掉「只比 number」的退化实现 (穷举验证)。
5. **「`include_terminal` 默认 False 不影响既有调用方」字面属实** —— 全仓 1 个生产调用点 + 5 处单测引用, 加 keyword-only 默认参数确实零影响。(但该事实同时说明 back-compat 论证是空的 —— 见 C2。)
6. **同 track-id 不会造成 claim 互相覆盖写** —— 存储键是 `claims/<container>/<session>.yaml`, 与 track_id 无关。§1 的 issue 派生 id 不引入写冲突, 只引入检出失明 (C1)。
7. **§0「存量数据不迁移」的裁决对** —— 归一在比较时发生, 13 条记录原样有效; 且改写共享 ref 是外向难撤销动作。R1 的「同时归一存量 ref 数据」建议被 R1-fix 收窄成「只在比较时归一」, 这个收窄是正确的。

---

## 复现方式

本轮 4 个只读探针脚本 (纯函数 + 只读 `read_claims`, 零写入) 位于
`/tmp/claude-1000/-home-dev-Aria/622639d7-c716-4c28-9cb1-8679549e38e9/scratchpad/probe{1,2,3,4}.py`。
运行前置: `sys.path.insert(0, "/home/dev/Aria/aria/skills/state-scanner")`。

**AI 不预判下一轮裁决。**
