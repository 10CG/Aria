不跑命令。以下全部依据 state-scanner SKILL.md 的成文规则 —— 主要是「Layer L Phase B 集成 → JSON 消费 + surface 渲染」段和其后的「claim 生命周期闭环 (coordination-claim-lifecycle-and-overlap Part B1)」。

**先给结论**: 【1】会报出来。【2】不会报。【3】不阻断。

---

## 1. 传 `--linked-issue 'aria-plugin #152'` — 会把那条 claim 报出来

**比较规则** (SKILL.md Part B1 原文): `--linked-issue` 写入 claim 并在输出 JSON 追加 additive 键 `linked_issue_overlap[]`, 内容是「同 issue **不同 track-id** 的『同一件事两个名字』advisory 告警」, 比较方式是

> 按归一后的 `<repo>#<n>` 比较: 仓名取 `/` 后最后一段、大小写与各段首尾空白不影响、`.`/`_` 视同 `-`, org 前缀不参与; 不可解析值回落原串精确比较

逐条套到你这两个值:

| 步骤 | 你传的 | 那条 active claim |
|------|--------|-------------------|
| 原始串 | `aria-plugin #152` | `10CG/aria-plugin#152` |
| 仓名取 `/` 后最后一段 | `aria-plugin #152` (无 `/`, 整串即最后一段) | `aria-plugin#152` (`10CG` 丢弃 —— org 前缀不参与) |
| 各段首尾空白 | `#` 前那个空格被吃掉 | 无空白 |
| 大小写 | 两边本来就一致 | |
| `.` / `_` → `-` | 无 `.`/`_` | 无 |
| **归一结果** | **`aria-plugin#152`** | **`aria-plugin#152`** |

两边归一后相等 ⇒ 命中。另一半触发条件也满足: 这是「同 issue **不同** track-id」的告警, 而你的 `ci-gate-first-push-fix` ≠ 它的 `pre-merge-gate-no-run-for-branch` —— 正好就是这条规则被设计出来抓的形状。所以 phase1_gate 的 stdout JSON 里 `linked_issue_overlap` 会是**非空 list**, state-scanner 阶段 2 推荐区把它渲染成一行 🔴 提示。

两点容易被忽略的:

- 你写的**裸仓名 + `#` 前空格不影响判定**, 但靠的是归一规则兜底, 不是碰巧。规则末尾那句「不可解析值回落原串精确比较」是个真悬崖: 一旦串的形状解析不出 `<repo>#<n>` (比如只写 `152`、或写成 `#152 aria-plugin`), 就退化成**原串逐字比较**, 那时 `aria-plugin #152` 与 `10CG/aria-plugin#152` 不相等 ⇒ **静默漏报**。稳妥写法仍然是标准 `<org>/<repo>#<n>`。
- **track-id 层的碰撞检测不会响**: `tracks_multibranch.collision.kind` 与 `surface.kind == "occupied"` 都是按 **track_id** 判定的, 你俩 track-id 不同, 所以这个场景里 `linked_issue_overlap` 是**唯一**会亮的信号。别指望 occupied 告警替你兜。

## 2. 如果传 `10CG/Aria#152` — 不会报

同一套归一, 但这次 org 前缀帮不上忙 (它本来就不参与比较):

- 你传的: 仓名取 `/` 后最后一段 = `Aria` → 大小写不影响 → 归一为 `aria#152`
- 那条 claim: 归一为 `aria-plugin#152`

`aria` ≠ `aria-plugin` ⇒ 不命中, **不会报出来**。(`.`/`_` 视同 `-` 的规则也拉不平这个差 —— 差的是整段后缀 `-plugin`, 不是分隔符写法。)

语义上这个结果是对的: `10CG/Aria#152` 和 `10CG/aria-plugin#152` 本来就是两个不同仓的两个不同 issue。但反过来要记住: **把 issue 写错仓, 告警就静默了** —— 「没有 🔴」不等于「没有重叠」, 它也可能是「你给的键根本没对上」。

## 3. 不阻断

三层理由, 任一层都足够:

- **规则本身写死了**: Part B1 明写这条 overlap 告警「渲染为 🔴 提示但**不阻断**」。
- **闸门默认就是 advisory**: `state_scanner.coordination.mode` 默认 `advisory`; advisory = 放行 + 写推自己的 claim + 返回 surface 告警 (advisory-over-hardlock)。是否进 Phase B 只看 `proceed` / exit code —— `proceed == true` (outcome ∈ passed / advisory_proceed / user_takeover / user_override_proceed) 即放行, exit 0 = 可进 Phase B。`linked_issue_overlap` 是 **additive 键**, 不参与 `proceed` 判定。
- **最终仲裁面不重叠**: reconcile 的仲裁 (earliest `claimed_at` 胜) 是按 **track_id** 做的; 你俩 track-id 不同, 连仲裁都碰不到一起。

### 读这个字段时必须守住的三态契约

SKILL.md 对 `linked_issue_overlap` 有明确的 **list | null | 缺席** 三态约定, 别压成一态:

- **缺席** = 本轮没检测 (没传 `--linked-issue`) —— 你这次传了, 所以不会是这态。
- **`[]`** = 已检测、无碰撞 —— 这是问题 2 的预期取值。
- **`null` 且 `linked_issue_overlap_error` 非空** = 本轮**没取到任何证据**, 必须渲染成「未能核实, 建议重试」, **不得**渲染成「无碰撞」(零证据不是正证据)。

所以别用 `.get('linked_issue_overlap', [])` 读它 —— 那个默认值恰好把 `null`(没核实) 伪装成 `[]`(核实过、干净)。同理还有 `unknown_schema_claims` (`int | null`, `null` ≠ `0`): 它 > 0 时意味着有 N 条 claim 解析不了, **存在性已确认、内容未知, 按存在处理** —— 也就是说, 即使你的 overlap 是 `[]`, 只要 `unknown_schema_claims > 0`, 就仍可能有一条你看不见的重叠 claim。

## 两个附带提醒

1. **那条 claim 的新鲜度值得顺手确认一下**: 它 `claimed_at` 是 2026-08-22, 距今约两周, 却仍是 `active`。按 Part C 的生命周期, active claim 靠 heartbeat 续命, 超 `STALE_TTL` 的会被 `release_gate.py --sweep-stale` 扫成 `abandoned` —— 一条两周没被扫掉的 active claim, 更可能是「**没人跑过 sweep**」而不是「它真的还在干活」。(SKILL.md 没有逐字写明 overlap 比较是否只看 active claim, 所以我不替它下断言; 但如果它后来被 sweep 成 abandoned, 你这条告警很可能就不再出现了 —— 别把「告警消失」当成「冲突解决」。)
2. **告警不拦你, 但它想说的事值得先答**: 同一个 owner (`simonfish`)、另一个容器 (`023236f2`)、同一个 issue `aria-plugin#152`, 两条不同 track-id。进 Phase B 前先确认: 是确实要开第二条并行轨, 还是应该接管 / 复用 `pre-merge-gate-no-run-for-branch` 那条。这正是「同一件事两个名字」这条 advisory 存在的理由。
