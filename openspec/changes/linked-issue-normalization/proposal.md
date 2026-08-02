# Proposal: linked-issue-normalization

> **Status**: 📝 **Draft (A.1)** — 待 post_spec 闸门
> **Created**: 2026-08-02
> **Spec Level**: 2 (单域 — `lib/collision.py` 的一个比较谓词; blast radius 限 `linked_issue_overlaps` 的匹配行为)
> **关联 Issue**: 无 (由 `a1-entry-claim-duplicate-work-guard` 的 post_spec R1 发现, 该 Spec 已 spike-first 挂起)
> **代码落点**: `aria/` 子模块 `skills/state-scanner/lib/collision.py`; Spec 落主仓 (Rule #5)
> **ship target**: aria-plugin v1.66.0 (MINOR — 修复既有机制的匹配语义, 行为面扩大)

> **📌 本 Spec 的来历 (owner 2026-08-02 裁定 A+B)**: 母 Spec `a1-entry-claim-duplicate-work-guard` 经 **post_spec R1 (5 席) → R2 (新眼睛) → R3 (第三双新眼睛)** 三轮, 同口径 major **4→6 上升**, 判定**不收敛**。owner 裁定拆分: **本 Spec = 从母 Spec 抽出的、唯一被三轮审计反复确认「可直接实现」的一块**, 独立交付; 母 Spec 其余部分转 spike-first 挂起 (见 `../a1-entry-claim-duplicate-work-guard/proposal.md`)。
>
> **它为什么能独立成立**: 见 §Why —— 该缺陷**不依赖任何未落地的机制**, 它现在就在生产中让一个**已 ship 的**机制静默失效。

---

## Why

### 缺陷 (R1 四席独立命中 + 主控实跑复验)

`aria/skills/state-scanner/lib/collision.py:217` 的 `linked_issue` 匹配是**裸字符串 `!=`**:

```python
if c.linked_issue != own_linked_issue:
    continue
```

而生产数据里**三个格式族并存**:

| 族 | 形态 | 来源 | 实测 |
|---|---|---|---|
| A | `aria-plugin#122` | CLI 直传 (裸形) | ref 中 **4** 条 |
| B | `10CG/aria-plugin#110` | CLI 直传 (org 限定); `phase1_gate` help 示例即此形 | ref 中 **9** 条 |
| C | `10CG/aria-plugin #122` | **proposal 头部「关联 Issue」字段的书写格式** —— AI 逐字照抄即得 | ref 中 0, 但**它是最自然的复制源** |

⇒ 轨 A 认领 B 族、轨 B 认领 A 族 ⇒ `linked_issue_overlap` **恒 `[]`** ⇒ 与「真没人在做」**不可区分**。

### 为什么这是 live 缺陷, 不是未来的事

**`linked_issue_overlaps` 已经在生产中被调用** —— `phase1_gate.py:1232`, 由 Phase B 入口的认领路径经 CLI 触达 (`phase-b-developer/SKILL.md:88-93` 的 `[--linked-issue]`)。⇒ **该机制今天就在跑, 今天就在因格式失配而漏报。**

这与母 Spec 的其余部分不同: 那些依赖尚未落地的 A.1 接线; **本条不依赖任何新机制**。

### 它是「已 ship ≠ 能用」的实例

`linked_issue_overlaps` 代码存在、有测试、被调用过、返回值合法 —— **只是它的匹配谓词对真实数据恒假**。这是 memory `feedback_completion_signals_vs_runtime_invocation` 最有迷惑性的一种形态: 所有表面信号都是绿的。

---

## What Changes

### 归一规则 (钉到字符级)

比较键 = `(repo_basename.casefold(), issue_number: int)`:

1. 剥首尾空白; 按**最后一个** `#` 拆为 `left` / `number_str`;
2. `number_str` 必须能解析为非负整数, 否则该值**不可解析** (见 4)。解析为 **`int`** 后比较 (故 `#007` ≡ `#7`);
3. `left` 剥尾部空白 (处置 C 族); 若含 `/`, 取**最后一段**为 `repo_basename`, 其前为 `org`; 否则 `repo_basename = left`, `org = None`。`repo_basename` 空 ⇒ 不可解析;
   - **⭐ `repo_basename` 内的 `.` 与 `_` 一律译为 `-` (spike S5 追加)**: `10cg.local` ≡ `10cg-local` ≡ `10cg_local`。
     > **为什么必须加 (S5 实测)**: 既有 `derive_track_id` (`track_id.py:71`) 已经把 `/` `.` `_` 全译成 `-`。若本 Spec 只做 casefold, **两层归一不一致** —— `10cg.local#20` 与 `10cg-local#20` 在**本 Spec 判不同仓**, 却在 `derive_track_id` 后**塌成同一 track_id**。
     > **且这不是理论风险**: `10CG/10cg.local` 是**真实仓** (Forgejo API 实测, **11 个 open issue**, 本项目 handoff 引用过 `10cg.local #20`)。post_spec R3 曾判此类为「dormant, 本组织无含 `.`/`_` 的仓名」—— **R3 的仓名清单不完整**, S5 穷举时发现。
     > **副作用是正收益**: 它顺带修好了「同仓两种拼写」这一类别名的一个**真实子集** (`.`/`_`/`-` 互换), 而无需引入别名表 (S4 已判别名表不划算)。
4. **不可解析的值** ⇒ **不参与归一, 退回原字符串精确比较** —— 绝不因解析失败就判「不匹配」而静默放行;
5. 匹配当且仅当 `repo_basename.casefold()` 相等 **且** `number` 相等。**`org` 不参与匹配**。

### 极性: org 轴 fail-toward-reporting, basename 轴是已知限

**org 轴**: 本机制是 advisory。漏报 = 静默无用 (昂贵, 已致 5 次重复劳动); 误报 = 多一行告警 (便宜, 人一眼可辨) ⇒ **fail toward reporting**, org 不参与匹配。代价: `otherorg/aria-plugin#122` 与 `10CG/aria-plugin#122` 会误配 ⇒ **surface 必须回显双方 `linked_issue` 原始串**, 让人一眼判别。

**basename 轴 (诚实标注, R2/M2)**: `repo_basename` 用**精确相等**, 对真实别名**恒漏** —— R2 语料统计 `aria-orch` **24 次** vs `aria-orchestrator` **10 次**。⇒ **本机制在 basename 轴是 fail-toward-silence, 与 org 轴方向相反**。

**本 Spec 不解决 basename 别名** (那需要别名表或书写强制, 属母 Spec 的 spike 范围)。此处**只做两件事**: (a) 把该限度**写进 SC-5 作为断言**, 防它被误读成「已覆盖」; (b) 在 surface 文案中不暗示「已穷尽核实」。

### 存量数据不迁移

归一发生在**比较时**, 13 条已有记录原样有效。改写共享 ref 是外向且难撤销动作, **非本 Spec 范围**。

### 接口面

`linked_issue_overlaps` 的签名与返回 schema **不变**; 只改内部比较谓词。⇒ Phase B 现有调用方**零改动**, 行为变化仅为「原本漏报的现在能报出来」。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 比较键 = `(basename.casefold(), int(number))` | R2 已用 18 元语料**穷举验证**: 自反 / 对称 / 传递**零违例**, 是良定义的等价关系 |
| D2 | `org` 不参与匹配 | advisory 下漏报昂贵、误报便宜 ⇒ fail-toward-reporting; 代价由「回显原串」兜 |
| D3 | 不可解析值退回**原串精确比较** | R2 复核: 两类不可能跨类相等, **论域被干净划分, 不破坏传递性** (此结论撤销了母 Spec R1-fix 自己的担忧) |
| D4 | basename 轴的 fail-toward-silence **成文为已知限**, 不在本 Spec 解决 | 别名表 / 书写强制均需语料决策 ⇒ 属 spike 范围 (母 Spec) |
| D5 | 存量 ref 不迁移 | 归一在比较时发生; 改写共享 ref 外向难撤销 |
| D6 | 签名与 schema 不变 | Phase B 现有调用方零改动 |

**Rule #6 (rule6_note)**: 改动面为 `lib/collision.py` 的一个内部比较谓词 + 其测试, **零 SKILL.md / 零 description / 零 AI 指令面** ⇒ 判据表**第一行「描述性 (命令 / 勘正)」** ⇒ **substitute: SC 级 baseline-failing 结构化测试替代** (SC-1~6 均在现状代码上可红)。与 v1.65.2 (#124 纯脚本修复) 同一判据路径。**不申请豁免。**

> **框定合规 (owner 2026-08-02 裁定 `db2e983`)**: 本条走 **substitute 框定** —— 判据表某一行 + 对应处置, **不**声称「Rule #6 不适用 / Rule #10 白名单第四类」。owner 该次裁定确立: **提供 substitute 与声称「不适用」逻辑上二选一**, 前者才对 (先例 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/`)。**substitute 须实证而非声称** —— SC-1~6 的 baseline-failing 状态在 Phase B 须实跑留证 (同该裁定要求的「全部实跑, 非声称」)。

---

## Success Criteria

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-1** | 三族两两配对: `aria-plugin#122` × `10CG/aria-plugin#122` × `10CG/aria-plugin #122` | **两两互相命中** | 现状裸 `!=` 在**全部三对**上必红 |
| **SC-2** | `10CG/Aria#147` × `10CG/aria-plugin#147` (同 org 同号, **不同仓**) | **不得**命中 | 「只比 number」的退化实现必红 |
| **SC-3** | `10CG/aria-plugin#1` × `otherorg/aria-plugin#1` (**两侧都有 org 且不同**) | **命中** (org 不参与) | **唯一能区分「org 不参与」与「两侧有 org 才比 org」两种实现的用例** (R2/M1: SC-1/SC-2 都无法区分) |
| **SC-4** | `#007` × `#7` | **命中** (number 解析为 int) | 字符串比较必红 |
| **SC-5** | `10CG/aria-orch#5` × `10CG/aria-orchestrator#5` (**截断型**别名) | **不命中**, 且该结果**被显式记为已知限** | 锁定 basename 轴 fail-toward-silence, 防被误读成已覆盖。**spike S4 实测: 该形态在真实输入总体 (「关联 Issue」字段值) 中实例数 = 0** ⇒ 已知限而非待修项 |
| **SC-5b** ⭐ (spike S5) | `10CG/10cg.local#20` × `10CG/10cg-local#20` × `10CG/10cg_local#20` (**分隔符型**别名, 真实仓) | **两两命中** | 只做 casefold 的实现必红。**与 SC-5 是两类**: 分隔符型**能**归一 (与 `derive_track_id` 对齐), 截断型不能 —— 两者的处置不同, SC 须分开钉 |
| **SC-6** | 不可解析值 (`no-hash-here` / `repo#abc` / `#5` / `10CG/#7`) | 退回**原串精确比较**; 不抛异常; **不因解析失败判「不匹配」** | 解析失败即 `return False` 的实现必红 |
| **SC-7** | 等价关系性质: 对语料全集断言自反 / 对称 / 传递 | 三性质零违例 | 非等价关系的实现 (如单向前缀匹配) 必红 |
| **SC-8** | 既有调用方回归 | `linked_issue_overlaps` 签名与返回 schema 逐字段不变; Phase B 路径行为除「原漏报现能报」外无差异 | 改了 schema 的实现必红 |

---

## 非目标

- **不改** `phase1_gate.py` 的 CLI / `run_gate` 签名 (本 Spec 只动 `collision.py` 内部谓词);
- **不做** A.1 入口认领前移 —— 那是母 Spec 的范围, 已 spike-first 挂起;
- **不做** basename 别名归一 (D4 已成文为已知限);
- **不改写**存量 coordination ref 数据 (D5);
- **不动** `_TERMINAL` 的 skip 语义 (`include_terminal` 属母 Spec, 且 R3 已证其接线点描述有误);
- **不引入** track-id 形态变更 (母 Spec 范围, R3 判其有碰撞域风险)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/state-scanner/lib/collision.py` | 归一比较谓词 (§What Changes 五步); 签名与 schema 不变 |
| `skills/state-scanner/tests/` (既有宿主) | 扩展 — SC-1~8 |
| 发版 5 文件 + 主仓 gitlink | v1.66.0 MINOR |

测试基线: state-scanner 现 **1322** tests, 本 change 新增按 SC 子用例下界 **≥12**。全量跨 skill 套件须绿 (`run_all_tests.sh`)。

---

## 审计资产继承

本 Spec 的内容**已经过三轮审计**, 作为母 Spec 的 §0 章节:

| 轮 | 席位 | 对本内容的结论 |
|---|---|---|
| R1 | 5 席 | **发现**该缺陷 (4 席独立命中) |
| R2 | type-design-analyzer | **穷举验证**比较键是良定义等价关系 (18 元语料, 零违例); **撤销**了「不可解析值破坏传递性」的担忧; 指出 org 轴与 basename 轴极性不同 (已吸收为 D4/SC-5); 指出 SC 无法区分两种 org 实现 (已吸收为 SC-3) |
| R3 | code-architect | 「§0 四步归一算法钉到字符级…**`collision.py` 改动核心逻辑可直接照写, 不需要实现者猜**」—— 在其可实现性评估表中是**唯一无缺口**的核心项 |

⇒ 本 Spec 的 post_spec 应聚焦**抽出过程本身**是否引入偏差 (措辞漂移 / SC 遗漏 / 与母 Spec 的边界是否干净), 而非重审已被三轮确认的算法本体。

---

## ⚠️ 闸门待裁 (Rule #10 — AI 不自行判定)

`.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 (非 config off / 无 adaptive_rules 映射 / 无成文 lane / 结构性前提成立) ⇒ **默认应跑 post_spec**。

**但本 Spec 的情形特殊, 提请 owner 一并裁**: 其内容已经过 R1/R2/R3 三轮审计并被逐轮确认 (见上表)。可选处置: (1) 照跑完整 post_spec; (2) **定向轮 —— 只审「抽出过程」** (措辞是否随抽出漂移 / SC 是否遗漏母 Spec 已有的约束 / 与母 Spec 的边界是否干净), 不重审算法本体; (3) 判定审计资产可继承、免跑并留痕请复议。

**AI 不预判。** 本 Spec 在裁决前不进 A.2/A.3。
