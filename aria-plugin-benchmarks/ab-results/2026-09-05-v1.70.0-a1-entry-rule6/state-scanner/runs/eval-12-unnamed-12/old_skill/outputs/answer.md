按你的要求，没有跑任何命令，下面全部依据 state-scanner SKILL.md 中 `--linked-issue` / `linked_issue_overlap[]` 那段说明（「claim 生命周期闭环 (coordination-claim-lifecycle-and-overlap Part C)」）来回答。

## 结论速览

| 问题 | 答案 |
|------|------|
| 【1】`aria-plugin #152`（裸仓名 + 空格）会报出那条 claim 吗 | **会**。归一后两边都是 `aria-plugin#152`，且 track-id 不同 |
| 【2】改成 `10CG/Aria#152` 呢 | **不会**。归一后是 `aria#152`，仓名与 `aria-plugin` 不同 |
| 【3】会阻断进 Phase B 吗 | **不会**。它是 advisory 🔴 提示，不阻断 |

---

## 【1】`--linked-issue 'aria-plugin #152'` — 会报出来

### 比较规则（SKILL.md 原文的四条归一 + 一条兜底）

告警不是按你写的原始字符串比对的，而是**先把两边都归一成 `<repo>#<n>` 再比**：

1. **仓名取 `/` 后最后一段** —— `10CG/aria-plugin` → `aria-plugin`
2. **org 前缀不参与比较** —— 有没有 `10CG/` 这个前缀不影响判定
3. **大小写不影响**，**各段首尾空白不影响** —— 你 `#` 前面那个空格属于仓名段的尾部空白，会被吃掉
4. **`.` 和 `_` 视同 `-`** —— `aria.plugin` / `aria_plugin` 与 `aria-plugin` 等价
5. **兜底**：值**不可解析**成 `<repo>#<n>` 时，回落为**原串精确比较**（你这两个值都可解析，走不到这条）

### 套到你这两个值上

| | 原始值 | 归一后 |
|---|---|---|
| 已有 claim（container `023236f2`，track `pre-merge-gate-no-run-for-branch`） | `10CG/aria-plugin#152` | `aria-plugin#152` |
| 你要传的 | `aria-plugin #152` | `aria-plugin#152` |

- 你少写的 `10CG/` 前缀：**不影响**（规则 1 + 2，org 前缀本来就不参与）。
- 你多写的那个空格：**不影响**（规则 3，段首尾空白被剥掉）。

两边归一后**完全相等**，而 track-id 是两个不同的串（`ci-gate-first-push-fix` vs `pre-merge-gate-no-run-for-branch`），正好命中 `linked_issue_overlap[]` 要抓的那个形状 —— **「同一件事两个名字」：同一个 issue，被两个不同 track-id 认领**。

所以 phase1_gate 会在输出 JSON 的 additive 键 `linked_issue_overlap[]` 里带上那条 claim，state-scanner 阶段 2 推荐区把它渲染成 🔴 提示行。

> 顺带说明范围：SKILL.md 只写了判定形状是「同 issue 不同 track-id」，没有逐字规定要拿哪些状态的 claim 来比。你给的这条是 `status: active`，无论怎么理解都在比较范围内，不影响本题结论。

---

## 【2】改传 `10CG/Aria#152` — 不会报出来

同样走归一：

| | 原始值 | 归一后 |
|---|---|---|
| 已有 claim | `10CG/aria-plugin#152` | `aria-plugin#152` |
| 你传的 | `10CG/Aria#152` | `aria#152` |

- 仓名取 `/` 后最后一段 → `Aria`；大小写不影响 → `aria`。
- `aria` ≠ `aria-plugin`（`.`/`_`→`-` 那条也救不了，这是两个字面不同的仓名）。
- **org 相同（都是 `10CG`）帮不上忙** —— org 前缀根本不参与比较。
- **issue 号相同（都是 152）也不够** —— 比的是整个 `<repo>#<n>`，不是光比编号。

结论：归一后不相等 ⇒ **不触发** `linked_issue_overlap[]` 告警。

这其实是规则想要的正确行为：`10CG/Aria#152`（主仓 Aria 的 152 号）和 `10CG/aria-plugin#152`（插件仓的 152 号）本来就是两个不同的 issue，只是编号撞了。

⚠️ 但要注意方向反过来的风险：如果你真正想关联的是**插件仓**那个 152，却写成了 `10CG/Aria#152`，那你就是**用错值把告警绕过去了** —— 告警没报不代表没重叠，只代表你告诉 gate 的是另一个 issue。你的裸仓名写法（问题 1）反而是能被正确识别的那个。

---

## 【3】不会阻断你进 Phase B

两个层面都不阻断：

1. **`linked_issue_overlap[]` 本身按设计就不阻断**。SKILL.md 明写它是「渲染为 🔴 提示但不阻断」的 advisory 告警，是追加在输出 JSON 上的 additive 键，不参与放行判定（放行看的是 `proceed` / `outcome`）。

2. **那条 claim 也不会以「被占用」的方式挡你**。占用类冲突是按 **track-id** 判的，对方占的是 `pre-merge-gate-no-run-for-branch`，你要 acquire 的是 `ci-gate-first-push-fix`，是两个不同的 track。而且生产默认 `state_scanner.coordination.mode == advisory`：advisory 的语义就是**放行 + 写推自己的 claim + 返回 surface 告警**，最终仲裁交给 reconcile（earliest `claimed_at` 胜）。

所以预期结果是：phase1_gate exit 0、`proceed == true`，你照常进 Phase B，只是推荐区多一行 🔴 的 linked_issue 重叠提示。

**不过这行 🔴 值得当回事**：它提示的正是「你和 container `023236f2`（owner 也是 simonfish）可能在给同一个 issue #152 干活，只是各自起了不同的 track-id」。机制不拦你，但建议你先确认一下这两条 track 是不是同一件事 —— 是的话应该统一 track-id 或者放弃一条，而不是并行跑两条 claim。

---

**补充（与本题相关的两个已知边界）**：

- CLI 形态下 `mode=block` 会退化成安全默认 abort（单次 JSON I/O 传不了活体 user_decision 回调），所以生产默认就是 advisory；只有你显式把 `coordination.mode` 设成 `block` 时，才会遇到「因为闸门而进不去」的情形，而那也是 claim 闸门造成的，不是 linked_issue 重叠告警造成的。
- `state_scanner.coordination.enabled` 缺省为 `true`（opt-out）；只有显式设成 `false` 才会完全不调 phase1_gate —— 那种情况下这个重叠告警自然也不会产生。
