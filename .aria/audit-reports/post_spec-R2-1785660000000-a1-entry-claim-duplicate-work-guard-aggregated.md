---
checkpoint: post_spec
round: 2
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R2 (新鲜眼睛, 定向轮) — a1-entry-claim-duplicate-work-guard

> **席位**: 1 — `pr-review-toolkit:type-design-analyzer` (未参与 R1 五席)。**选席理由**: R1-fix 引入的三处新承重逻辑全是**谓词与契约**问题 (等价关系 / 布尔开关改变返回值含义 / 派生键的碰撞域), 该视角与 R1 五席全不重叠。
> **verdict**: **REVISE** · `scope_ok` true · **counts**: critical=2 major=4 minor=4 (+1 OUT_OF_SCOPE)
> **timestamp**: 1785660000000 · 审计对象: 主仓 `87e9738` + 未提交的 R1-fix

## 判定

**REVISE, 未收敛。** 两条 critical **都落在 R1-fix 自己新写的逻辑上**, 且第一条**当场杀死主机制**。

### C1 — 我的 R1-fix 自己杀死了主机制 (主控实读复验)

- **位置**: proposal `:125` (R1-fix 新写的 `--raw-track-id` 取值规则) vs `lib/collision.py:219-220`
- **问题**: R1-fix 为解 M1-CR (双来源无优先级) 与 §3c (改名孤儿), 规定 **A.1 一律用 issue 派生串** `<basename>-<number>` (如 `aria-plugin-122`)。而 `linked_issue_overlaps` 的 `:219-220` 是:

  ```python
  if c.track_id == own_track_id:
      continue  # same-name collision — reconcile's job, not ours
  ```

  ⇒ **两轨做同一个 issue ⇒ 派生出同一个 track_id ⇒ 互相被这一行排除 ⇒ `linked_issue_overlap` 恒 `[]`。**
- **后果**: 主机制的**唯一信号通道恒空**。R1 的 C1 是「格式不归一致漏报」, R1-fix 修好了格式, 却用另一条自己新写的规则把同一个信号又掐断了 —— **修复在自己的新逻辑上复现了要治的病**, 且这次是精确的同一个后果 (`overlap == []` 与「真没人在做」不可区分)。
- **加重**: R2 另指出残余通道 (reconcile 的同名碰撞路径) **30min 熄灭**, 与 R1-fix 刚写的 SC-10「保护窗 ≥72h」直接矛盾 —— 即 C3 的修法与 M1 的修法互相拆台。
- **修法方向**: issue 派生串**不能**做 track_id (它天然使双方同名)。track_id 必须**容器可辨** (如 `<basename>-<number>-<container-short>`), 而「同一 issue」这层关系由 `linked_issue` 承载 —— 这本来就是两个字段各自的职责。§3c 的改名孤儿问题另寻解 (如 release+acquire 两步, 而非靠 track_id 天然稳定)。

### C2 — `include_terminal=True` 在唯一生产调用路径上不可达

- **位置**: proposal §1 (R1-fix 新增) vs `phase1_gate.py` 的调用链
- **问题**: R1-fix 为解 C2 (归档失明) 给 `linked_issue_overlaps` 加 `include_terminal`, A.1 调用点传 True。但 **CLI 层没有把该参数暴露出来的路径** ⇒ 生产调用永远拿默认 False ⇒ SC-5「`done` 可见」**只能被单测满足, 生产不可达**。
- **这是 `feedback_completion_signals_vs_runtime_invocation` 的又一实例** —— 与本 Spec 自己援引的、以及 R1 用来推翻「已 ship ≠ 能用」的**同一条 memory**。R1-fix 写了参数、写了 SC, 但没写「参数怎么从 CLI 传到那一层」。

## Major (4 条)

| # | 要点 |
|---|---|
| **M1** | SC-1a/1b **无法区分**「org 不参与匹配」与「两侧都有 org 才比 org」两种实现 —— §0 论证最重的那条规则**零覆盖** |
| **M2** | fail-toward-reporting 极性**只在 org 轴成立**; **basename 轴是精确匹配**, 对语料真实别名恒漏 (`aria-orch` 24× vs `aria-orchestrator` 10×)。且取样口径有误: §0 的三族表取自 ref (13 条), 而实际输入语料是 prose (139 篇) —— **两者不是同一个总体** |
| **M3** | `yielded` 状态在 SC-2 (active) 与 SC-5 (done) 之间**无归属**; §0 落地后历史 `yielded` 会以「活跃竞品」形态触发 `AskUserQuestion` |
| **M4** | §0 的 `casefold` 归一与 `derive_track_id` 的 `lower + /._→-` 归一**未组合** —— 三个不同 issue 可塌成同一 track_id; 且 `--phase` 自由字符串正被推向承重分派角色 |

## Minor (4 条)

`unknown` 分档措辞**不可达** (sentinel 不带 `linked_issue`, 被 `:215` 先行过滤) · §0 自称「钉到字符级」但 `number` 的 str/int 比较与 `#` 两侧空白**欠定** · **§闸门待裁 的自认领声明与 ref 实据不符**, 且那条 claim 现在**自己就是一条 §3c 孤儿**, 恰落在 SC-11 未覆盖的那半 · §0 三族表**漏了 prose 语料最高频的一族**, 取样口径未标注

## OUT_OF_SCOPE (1 条)

`release_gate.py:225` 的 help 文案与 `gc.py` 实现的 TTL **相差 48 倍** —— 非本 Spec 引入, 供 owner 参考。

## 经 R2 核实**设计对了**的部分 (下轮免重复)

1. **§0 的比较键确实是良定义的等价关系** —— 自反 / 对称 / 传递在 18 元语料**穷举零违例**;
2. **R1-fix `:297-299` 自己担心的「不可解析值退回精确比较破坏传递性」不成立** —— 两类之间不可能跨类相等, 论域被干净划分。**该担忧可以撤销**;
3. 「最后一个 `#` 拆分」对现实语料无害; `Aria`/`aria` 的 casefold 论断与 SC-1b 负控**均经语料复核属实**;
4. 同 track-id **不会**造成 claim 覆盖写 (存储键是 `container/session` 而非 `track_id`) —— 这也说明 C1 的后果**仅限于 overlap 检测失效**, 不会丢数据;
5. 「存量不迁移、只在比较时归一」这个对 R1 建议的收窄**是正确的**。

---

## 轮次趋势

| 轮 | 席位 | critical | major | 性质 |
|---|---|---|---|---|
| R1 | 5 (config 全员) | 4 | 8 | 审原始 Spec |
| R2 | 1 (团队外新眼睛) | **2** | **4** | 审 R1-fix |

同口径不可比 (席位 5→1)。但**两条 critical 全部落在 R1-fix 新写的逻辑上**, 与 `phase-c-gate-path-coverage` 那条 Spec 的 A1→A2→A3 轨迹**形状完全相同**: 每一版 fix 都在自己的新条款上重犯要治的病。

**本轮最值得记的**: C1 不是「没想到的边界」, 而是**两条 R1-fix 条款互相拆台** —— 为 M1-CR 写的「issue 派生 track-id」直接违反了 C2 修法所依赖的「两轨 track_id 必须不同」这个隐含前提。R1-fix 逐条吸收了 12 个簇, **但没有做条款之间的交叉一致性检查**。

**AI 不预判裁决。**
