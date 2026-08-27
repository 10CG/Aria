---
checkpoint: post_spec
round: 5
role: code-simplifier
verdict: REVISE
scope_ok: true
counts:
  critical: 3
  major: 8
  minor: 5
---

# post_spec R5 (combined) — a1-entry rework v3 + 两份子 Spec · 席位镜头 = **简化与过度设计**

> **对账 SHA**: 主仓 `b0c16ff` (工作树 `M aria-orchestrator`, 不触及被审文件) · **基线**: aria `d50f9c3`
> **被审**: `a1-entry-claim-duplicate-work-guard` (876 行 / 157.6KB) · `linked-issue-field-availability` (606 行 / 76.8KB) · `sibling-spec-probe` (557 行 / 71.9KB) = **2039 行 / 306.3KB**
> **本席不修改任何被审文件。** 全部断言均在 `d50f9c3` / `b0c16ff` 上实读复核, 复核命令逐条给出。

---

## 0. 本席的判定前提 (与 R4 的关系)

R4 聚合已判「继续加通用审计轮的边际产出为负」, 两席主动建议停止加轮。**本席同意该判断, 并且不以「再抓几条 finding」的方式工作。**

本席只回答一个问题: **哪些东西可以合并、删除或不做, 而不损失它要防的已实证缺陷?**

⇒ 本报告的产出形态是**删除清单**, 不是修复清单。R5 之后应该做的是一次**删除轮**, 不是又一次清账轮 —— 前四轮的实证是「每轮清账生出等量或更多同形 critical」(R4: 8/9), 而删除动作**结构上不会**产生同形缺陷: 被删的条款不再有条款间接缝可落。

---

## 1. 三条 Critical (按简化镜头)

### C1 ⭐ — **两种 track-id 形态是自造的复杂度源; 取消它, `spec_slug`/`track_form` 两个字段与 K1/K2/K4 的大半一并消失**

**现状 (可 grep)**: `a1-entry-claim/proposal.md` §2.1 定义两种形态 —— issue 派生形 `<basename>-<str(int(n))>-<uuid>` 与回落形 `<spec-slug>-<uuid>` (grep `#### §2.1 track-id 派生`)。**本批三分之一的新增机制, 全部是这个二分产生的下游成本**:

| 下游条款 | grep 锚点 | 它存在的唯一理由 |
|---|---|---|
| §5.1 二分谓词 + 判定式 | `#### §5.1 二分谓词` | 「这条 track 是哪种形态」不可从字符串反推 (反例 `fix-issue-149-a1b2c3d4`) |
| **新增 claim 字段 `track_form`** | `track_form: "issue" \| "slug"` | 上一行的机械判定式 |
| **新增 claim 字段 `spec_slug`** | `#### §5.3 D.2b 的 release 作用域` | issue 派生形下同 issue 三方向**共用一个 track_id** ⇒ D.2b ALL-matching 连坐 |
| K1 (字段活不过 heartbeat) / K2 (`track_form=None` 自相矛盾) / K4 (无写入路径) | `🔴 K1/K4 (R4)` · `🔴 K2 (R4) 订正` | 上面两个字段 |
| SC-1 / SC-4 / SC-15 / SC-27(C) / SC-30 / SC-31 | 各自 SC 行 | 同上 |
| D12 / Impact 的 `claim_schema.py` 行 / `release_gate.py --spec-slug` 行 / `phase-d-closer` 第二处 / `coordination-ref-schema.md` 第二处 | Impact 表 | 同上 |

**未被呈给 owner 的第三个选项 = 只保留一种形态: 恒用 `<spec-slug>-<container_uuid>`。** 逐条核对它是否损失已实证缺陷:

| 已实证缺陷 | 单一形态下是否回来 | 依据 (实读) |
|---|---|---|
| R2/C1「主机制死」(两轨同 id ⇒ overlap 自排除) | **不回来** | `lib/collision.py:278-279` 排除的是**同 track_id**; 两容器的 slug 段可能相同但 `<container_uuid>` 段不同 ⇒ track_id 不同 ⇒ 不自排除。§2.1 论证的承重段是**容器段**, 与「issue 段 vs slug 段」无关 |
| 主机制的「同一个 issue」判定 | **不回来** | overlap 靠 `linked_issue` 匹配, **不靠 track_id**。`git -C aria show d50f9c3:skills/state-scanner/lib/collision.py \| sed -n '230,292p'` 全函数只读 `linked_issue` |
| R2/C-B 连坐 release | **不回来, 且是被结构性消灭** | 三个方向 = 三个 slug = 三个 track_id ⇒ `release_claim_by_track` 按 `(container, 归一 track_id)` 定位天然只释放自己那条。**`spec_slug` 字段不再需要** |
| R2/C-C carry-id 断链 | **不回来** | A.1 原串 `<slug>-<uuid>` 逐字节复用到 B.0/D.2b, SC-23 原样成立。且这一串**更贴近** `phase-b-developer/SKILL.md:92` 现有占位 `"<本 cycle carry-id/Spec id>"` ⇒ §2.1b 的三处 SKILL.md 措辞改动**缩水为近乎零** |
| SC-4 (`#007` vs `#7` 派生两个 id) | **消失, 因为 number 不再进 track_id** | 该缺陷是 issue 派生形独有的 |
| SC-1 (改名孤儿) | **回来一半** | slug 改名 ⇒ track_id 变 ⇒ 需 release 旧 + acquire 新。**但这正是现 SC-15 已经规定的两步**, 只是从「两档之一」变成「唯一档」⇒ 条款数减少 |
| 同容器多方向互相报 overlap | **新增一条 advisory 噪声** | 同容器三方向 track_id 互异且 `linked_issue` 相同 ⇒ 互相进 `linked_issue_overlap[]`。**这是唯一的真实代价**, 且它是**自己看见自己的另一条轨**, 在 §2.3 的告警面上一眼可辨 (owner-container 相同) |

**⇒ 净账**: 用「一条同容器 advisory 噪声」换掉 **2 个新 claim 字段 + 9 处透传 + 6 条 SC + 4 条 K-critical 的大半 + 约 27KB 规格**。
**估算删除量**: §5.1 全节 (7.1KB) + §5.3 的 `spec_slug` 处置表与 K1/K4 透传表 (约 10KB) + 6 条 SC (约 4KB) + D12 与 5 行 Impact (约 4.5KB) + §2.1 表 number 段 (约 1KB) ≈ **27KB / 母 Spec 的 17%**。

**风险声明 (必须一并呈 owner)**: 该选项**推翻的是 editlist FIX-15 与 D12 的前提**, 不是它们的结论 —— FIX-15 当初选「是否含 slug」作谓词, 是因为「有没有关联 issue」对第三类给相反答案; 单一形态下**根本没有谓词要选**。属 memory `narrow-owner-options` 点名的第三形态:「没想到『合并同根问题』这个更优解」。

---

### C2 ⭐ — **K1 的处方是「修实例」, 而 `ClaimRecord` 是 `frozen dataclass`, 类级修只要 4 行**

**现状 (可 grep)**: `🔴 K1/K4 (R4)` 段的处方是「`heartbeat` `:244-256` 的逐字段重建**必须加两行**」, 并附一张 **8 行透传枚举表**, 外加硬约束「**不枚举就等于没做**」。

**实读基线**:
```
git -C aria show d50f9c3:skills/state-scanner/lib/claim_schema.py | sed -n '69,70p'
  @dataclass(frozen=True)
  class ClaimRecord:
git -C aria grep -n "ClaimRecord(" d50f9c3 -- skills/state-scanner/lib skills/state-scanner/scripts
  claim_lifecycle.py:146  (acquire — 真·构造)
  claim_lifecycle.py:244  (heartbeat — 保留式重建)
  claim_lifecycle.py:346  (release_claim — 保留式重建)
  claim_lifecycle.py:437  (release_claim_by_track — 保留式重建)
  claim_schema.py:222/300 (parse — 真·构造)
  collision.py:129 / gc.py:396 (gc sweep — 保留式重建) / phase1_gate.py:749
```

**四处「保留式重建」逐字同形** (`:244` / `:346` / `:437` / `gc.py:396`), 每处都把 11 个字段抄一遍只为改 1-2 个。`dataclasses.replace()` 在 frozen dataclass 上正是为此存在:

```python
updated  = replace(existing, heartbeat_at=ts_str)                    # :244
released = replace(existing, status=status, heartbeat_at=ts_str)     # :346 / :437
abandoned= replace(record,   status="abandoned")                     # gc.py:396
```

**⇒ 这不是风格偏好, 它决定了 K1 会不会复发**:
- 现处方 (加两行) 修的是**这一次**的两个字段。下一个 additive 字段照样被四处重建各抹一次 —— 而 `linked_issue` 已经踩过同一个坑 (它在 `:244`/`:346`/`:437`/`gc.py:396` 各被手工补了一行);
- 类级修之后, **任何** additive 字段的真实透传面 = `ClaimRecord` 声明 + `parse_claim` 读 + `serialize_claim` 写 + `acquire_claim` 写 = **4 处**, 不是 8 行表所示的规模。

**估算删除量**: `🔴 K1/K4 (R4)` 整块的 8 行透传表与「17 处 / 5 文件」论证 (约 4KB) 缩为 4 行; **SC-30** 保留 (它验的是往返, 仍然承重且在 `replace` 下依然会红于坏实现)。

**这是 memory `fix-the-class` 的教科书形状**: 修实例必问「这形状还有几个兄弟位置」—— 答案是 4 个, 全在同一文件族里, 且 Spec 自己已经列出了其中 3 个 (透传表第 3/4/5 行) 却仍选择逐处补行。

---

### C3 ⭐ — **审计对账层与交付面再次同居, 且这次是在「已经切出去过一次」之后长回来的**

三份文档头部都写着四条切分声明 (grep `审计轨是 append-only`), 把历史叙事切到 `.aria/audit-reports/*-audit-trail.md`。**然后 R3/R4 两轮的清账动作又把新一层对账写回了交付面**:

| 段 | 母 Spec | 字段 Spec | 探针 Spec |
|---|---|---|---|
| 「R1-fix editlist 逐条对账」(19 行表) | `:779-809` **5.5KB** | — | — |
| 「本轮引入的新表面 (未审)」 | `:810-827` | `:577-589` | `:536-547` |
| 「R3 清账轮新引入且未经任何审计的表面」 | `:828-839` | — | — |
| 「本轮未做 / 存疑」 | `:840-855` | — | — |
| 「闸门状态 (Rule #10)」 | `:856-876` | `:590-606` | `:548-557` |
| **⛔ 迁出/切出占位节** (§1 / §4 / 清单 / 轨迹 四处只剩指针) | 6.5KB | 1 处 | 1 处 |
| **K1–K9 的「(2026-08-27 补, 未经审计轮)」blockquote** | 5 处 | 2 处 | 1 处 |

母 Spec 单是 `:779-876` 就 **15.6KB**, 三份合计对账层约 **35KB / 全部 306KB 的 11%**。

**它们各自的删除风险**:
- **editlist 逐条对账表 (19 行)** —— 删除**无风险**: 它防的是 R2/CR-M4「三处自述已全量吸收而 12 项未落」。该防护的正确家是 editlist SOT 文件本身 (`.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`) 里的状态列, 不是交付面。**19 行里有 8 行的状态是「⛔ 已迁出」或「不适用」** —— 纯坟头;
- **「本轮引入的新表面」×3 + 「未做/存疑」** —— 删除**有风险**, 但风险的正确处置是**转成 A.2 任务**而非留在 Spec: 母 Spec 自己已经在两处这么做了 (grep `已升格为 A.2 显式验收项`)。留在 Spec 里的部分**没有触发者** = memory `feedback_completion_signals_vs_runtime_invocation` 的形状;
- **闸门状态节 ×3** —— 三份逐字重复同一段「封闭豁免白名单四类无一适用 ⇒ 不豁免」。**合并为一句**即可;
- **⛔ 占位节 (6.5KB)** —— 「本节已迁出, 见 X」写了 4 遍, 每遍附完整迁出理由与依赖方向。**依赖方向已在文件头部声明过一次** (grep `依赖方向 (逐字, 不得读成隐式前置)`) ⇒ 二次陈述可删。

**⇒ 这正是 memory `audit-trail-not-in-spec` 说的「是 append-only 性质在造耦合」。** 切一次不够 —— 只要每轮清账都往交付面追加对账段, 耦合就会重新长出来。**结构性处方: 对账段一律落审计轨, 交付面禁止出现「本轮」二字。**

---

## 2. 问题 2 的直接回答: 合得起来什么 (跨文档 / 同文档重复)

| # | 重复项 | 出现处 (grep 可定位) | 处置 |
|---|---|---|---|
| R1 | **跨 skill import 骨架** (`_SS_ROOT = ... parents[2] / "state-scanner"` + `sys.path.insert` + 先例 `handoff_autofill.py:403-407` + 反例 `fetch_gate.py:111-112` + 同名包已知限) | 字段 Spec `:244-270`, 探针 Spec `:140-165` —— **约 1.5KB 逐字重复两遍** | 两份 Spec 各自 import 同一个新模块 ⇒ **约束写一处**, 另一处只留一行指针 |
| R2 | **`fetch_gate.py:111-112` 反例引文** | 字段 `:248` · 探针 `:144` · 探针 `:519` (第三处还给出与前两处**不同的结论**: `:519` 说「本仓既有惯例是复制而非跨 skill import」, 而 `:144` 说「先例确实存在, 本 Spec 采用 import」) | **同文档内自相矛盾** —— 见 m1 |
| R3 | **`无` 是 truthy ⇒ 两份无关 Spec 互相命中 (NEW-01)** | 母 `:104-112`(§2 模板下) · 母 `:544`(§6 缺口表首行) · 字段 `:148`(§2) · 字段 `:200-215`(K8) · 字段 SC-4 · 探针 `:183-190`(层 1.5) · 探针 SC-9 | 论证 **7 遍**。SOT 应只有**一处** (字段 Spec §2), 其余全部改为一行引用 |
| R4 | **四态 / 「零证据不得当正证据」** | 母 §2.4b 四态表 · 母 §2.5 · 母 K5 · 字段 §3 四态判定表 · 探针 §7 `verdict` 表 · 探针 §9 消费面三档表 | 母与探针是**同一条纪律在两个输出面的落点** (探针 §7 自己也这么说)。可合为一条共享条款 + 两处落点表 |
| R5 | **「模板 placeholder 会复现 NEW-01」(K8)** | 字段 `:195-215` + 探针 `:111` 的 `BAD_TOKEN` 格内嵌一整段交叉订正 | 两侧互为镜像 + 「任一改动须同批改另一侧」——**这正是拆 Spec 制造的接缝** (memory `split-makes-seams`) |
| R6 | **「只扫头部 N 行」被实测否决 + 同两份归档件 `:61`/`:45`** | 字段 D2 与 §3 · 探针 `:100` 三臂表 | 两席各自实测同一结论并各自写一遍。合并后是一条 |
| R7 | **闸门状态段** | 三份文件末尾逐字同义 | 合为一句 |

**⇒ 保守估算跨文档 + 同文档重复 ≈ 12–15KB。** 但更重要的不是字节: **R1/R2/R5 三项都带着「任一被改必须同批改另一侧」的人肉同步义务** —— 那是拆分制造出来的、原本不存在的维护面。

---

## 3. 问题 3 的直接回答: 逐项问「去掉它, 哪条已实证缺陷会回来?」

| # | 新增物 | 去掉它, 回来的缺陷 | 判定 |
|---|---|---|---|
| 1 | claim 字段 **`spec_slug`** | 无 (C1 单一形态下结构性消失) | **删** |
| 2 | claim 字段 **`track_form`** | 无 (同上) | **删** |
| 3 | `phase1_gate.py` **`--spec-slug`** flag (K4 写入端) | 无 (同上)。⚠️ 基线复核: `git -C aria show d50f9c3:skills/state-scanner/scripts/release_gate.py \| grep spec_slug` **零命中** —— K1/K4 表第 7 行「`release_gate.py` 已有 `--spec-slug`」措辞会被读成 baseline 已有 | **删** |
| 4 | `release_gate.py` **`--spec-slug`** flag (读取端) | 无 (同上) | **删** |
| 5 | **by-track heartbeat 变体 `heartbeat_by_track()`** | **会回来**: 事故窗 48–72h > `SWEEP_TTL` 24h ⇒ 自己的 claim 被 sweep 成 abandoned, 对他人不可见 | **保留** |
| 6 | **`--heartbeat-only` CLI 模式** (含三级 track 来源回落 / 遥测分区隔离 / K7 / SC-32) | **大概率不回来** —— 见 M2, 有更小的等价物 | **候选删 (带残余)** |
| 7 | `lib/identity.py` **`get_container_uuid()` accessor** | **不回来** —— 见 M1 | **删** |
| 8 | 输出键 **`unknown_schema_claims`** (+ K5 + SC-24 + SC-33 + 四态表第三行) | 回来的是「竞品跑着不同 schema 版本的 plugin」这一场景。**该场景在本 Spec 自己的语料里零实例** (Lab 实测 2 容器同版本), 且 Spec 自己已把它的「路径/身份」转 follow-up | **候选删 (转 follow-up 整条)** |
| 9 | config key **`state_scanner.coordination.unattended`** (+ D15 + SC-26 + `config-loader/SKILL.md` + `DEFAULTS.json` 两行 + 三腿契约已知限) | 见 M4 —— **当前形态下删与不删的生产行为完全相同** | **要么钉死取值路径, 要么整条删** |
| 10 | `lib/linked_issue_field.py` **跨 skill 纯函数** | **会回来**: 双实现漂移 (前置 Spec spike S5 刚治过)。**这条是真承重的** | **保留** |
| 11 | `sibling_spec_probe.py` **新脚本** | **会回来**: 第 5 次事故的形态 (对方已 ship 归档) 主机制结构性不可见 | **保留 (但见 M8 瘦身)** |
| 12 | `ab-suite/audit-engine.json` **新 AB 套件** | 这是 Rule #6 义务, 不是设计选择。**Rule #10 禁止 AI 自行豁免** | **保留, 本席不建议删** |
| 13 | `.aria/linked-issue-field-grandfathered.txt` **仓本地数据文件** (+ `--grandfathered` 参数 + 三子情形陈旧守卫 + SC-5(c)(e) + K9) | 见 M6 —— 有零新文件的等价物 | **候选删** |

---

## 4. 问题 4 的直接回答: 采纳 R4 选项 (d) 之后, 能删掉多少条款?

**(d) = 给 track-id 派生与 `spec_slug`/`track_form` 写入一个真正的代码宿主 (小模块 + CLI 入口)。**

### 4.1 (d) 直接删掉的条款 (清单)

| # | 条款 | grep 锚点 | 删除量 |
|---|---|---|---|
| 1 | **§2.1a 全节** (「本 Spec 不新增拼接函数」+ 文本层/行为层两层表) | `##### §2.1a 拼接的落点与被测对象` | ~3.5KB |
| 2 | **`🔴 K3 (R4)` 整块** (四条 SC 降级为行为类 + 「不得写成代码 (CLI 全链路)」禁令) | `🔴 K3 (R4) — 「不新增拼接函数」的**另一半代价**` | ~1.8KB |
| 3 | **SC-1 / SC-2 / SC-4 / SC-15 各自尾部的「⚠️ 类别 (R4/K3)」段** (4 处逐字重复) | `类别 (R4/K3)` | ~1.6KB |
| 4 | **SC-2 的「夹具手写字面串」硬约束整段** (含 R4/C-1 订正的自我批评) | `SC-2 的夹具硬约束` | ~1.5KB |
| 5 | **SC-1~SC-4 表头的「被测对象与宿主」两层说明** | `旧版这四条没有宿主, 是「无被测对象的 SC」` | ~0.8KB |
| 6 | **K4 的写入端论证** (`--spec-slug` 无宿主 ⇒ SC-27(C) 夹具不可构造) | `🔴 K1/K4 (R4)` 前半 | ~1.0KB |
| 7 | Impact 表 `phase1_gate.py` 第三处变更行合并进宿主模块行 | Impact 表 | ~0.5KB |
| **合计** | | | **≈ 10.7KB / 母 Spec 的 6.8%** |

**并且 (d) 让 4 条 SC 从「行为类 (只能 AB eval)」回滚为「代码类」** —— 这是 (d) 的真正价值, 不是删字节: SC-1/2/4/15 目前挂在 AB fixture 上, 而 AB fixture 是本项目实证最贵、最慢、最难证伪的验证面。

### 4.2 (d) **不能**删掉的 (owner 须知)

- **K1 (字段活不过 heartbeat)** —— (d) 给的是**写入**宿主, 不解决**保留式重建**抹字段。K1 只能由 **C2 (`dataclasses.replace`)** 解;
- **K2 (`track_form=None` 的 legacy 处置)** —— (d) 之后新 claim 有字段, 但**上线当天全部存量 claim 仍无字段**;
- **K5 / K6 / K7 / K8 / K9** —— 与派生宿主无关。

### 4.3 ⭐ (d) 与 C1 的关系 —— **这是 owner 真正要先答的那个问题**

**若先采 C1 (单一 track-id 形态), (d) 的收益会大幅缩水**:

- C1 之后, 派生逻辑 = `f"{spec_slug}-{container_id}"`, **一行**, 没有 `str(int(n))`、没有 basename 归一、没有形态分支;
- 需要写入的 additive 字段 = **0 个** ⇒ (d) 的「字段写入宿主」一半整个消失;
- 剩下的「一行拼接要不要代码宿主」是个小得多的问题 —— 它仍值得做 (让 SC-2 能跑真派生), 但**不再需要一个新模块 + CLI 入口**, 一个 `lib/track_id.py` 内的 `compose_track_id(slug, container_id)` 即可, 且它天然复用同文件已有的 `derive_track_id`。

**⇒ 建议给 owner 的提问顺序**:
1. **先问**「要不要两种 track-id 形态?」(C1) —— 这决定了删 27KB 还是不删;
2. **再问**「一行拼接要不要代码宿主?」((d) 的残余) —— C1 之后这是一个 20 行函数的问题, 不是一个架构决定。

**两问顺序颠倒的代价**: 先采 (d) 会为一个即将被 C1 删掉的双形态派生建一个模块, 然后再删。

---

## 5. 问题 5 的直接回答: 最小可交付切片

> **只允许保留一件事进 A.2, 应该是: 母 Spec 的「A.1 入口认领 + `--include-terminal`」, track-id 用既有回落形 `<spec-slug>-<container_uuid>`。**

### 为什么是它

1. **它是唯一直接对着已实证缺陷的动作。** §Why 记载 **5 次**并发起草事故; 根因逐字是「认领点在 Phase B, 只能保护『已做完 Phase A 的人』」。把认领前移到 A.1 就是那一条的直接解, 别的都是它的配件;
2. **第 5 次事故的形态恰由 `--include-terminal` 覆盖。** 竞品 claim 已 `done`, 被 `lib/collision.py:268` 的 `_TERMINAL` skip。`--include-terminal` 是让它可见的**唯一**必要改动;
3. **它的代码面全部落在 owner 已裁的范围内, 且零新表面**:

| 改动 | 规模 | 已裁? |
|---|---|---|
| `lib/collision.py::linked_issue_overlaps` 加 keyword-only `include_terminal: bool = False` | 3 行 | R1-fix/C6 |
| `phase1_gate.py` 加 `--include-terminal` (store_true) + `_main()` `:1233-1235` 传参 | 4 行 | D5 |
| `phase-a-planner/SKILL.md` + `spec-drafter/SKILL.md` 各加一个标题级「前置: REQUIRE claim」块 | 2 处 | S6 / FIX-13 |
| 两处 frontmatter `allowed-tools` 扩权 | 2 行 | **owner 2026-08-22 已裁 (a)** |
| `phase-b-developer` / `branch-manager` / `phase-d-closer` 三处 carry-id 占位措辞 | 3 行 | R2/C-C · U-3 (C1 之后近乎零改动) |

4. **零新字段 / 零新模块 / 零新脚本 / 零新数据文件 / 零新 config key / 零新 CLI 模式。**
5. **SC 面只需 4 条, 全部有既有测试宿主** (`skills/state-scanner/tests/`):
   - **SC-8** (终态可见, CLI 全链路) — baseline 红 (`_TERMINAL` skip);
   - **SC-22** (两处 SKILL.md 各有标题级认领块) — baseline 红 (两处均无);
   - **SC-23** (A.1 原串 → D.2b release 往返) — baseline 红;
   - **SC-29** (不把自己计入 overlap, 回归守卫) — baseline 绿, 负控为「删 `:278-279`」。

### 这一片**明确不含**什么 (以及各自去处)

| 排除项 | 去处 |
|---|---|
| heartbeat 变体 + `--heartbeat-only` | 独立小 Spec (它解的是 Aria #180 的「零生产调用点」, 与 A.1 认领正交) |
| `spec_slug` / `track_form` | 随 C1 消失 |
| `unknown_schema_claims` | follow-up |
| `unattended` config key | follow-up (或钉死取值路径后独立交付) |
| 字段可得性 Spec / 探针 Spec | 两份自己 ship, 依赖方向已声明为任意顺序 |

### 诚实的残余 (不假装覆盖)

- **主机制在字段缺席时零输入** —— 在制语料 9 份里 6 份 `NO_FIELD`。这一片交付后, **主机制对那 6 份不产生任何信号**。这不是新缺口, 是 §6 已成文的那条; 但**它意味着最小切片的当日实效覆盖 = 3/9**;
- **保护窗仍是 30min / sweep 24h < 事故窗 48–72h** —— 但 §2.1 自己已论证 **overlap 通道新鲜度免疫** (`lib/collision.py:265-292` 无新鲜度过滤), 而 overlap 正是主检测通道 ⇒ **最小切片的主通道不受该残余影响**; 受影响的是 7c 同名通道与 sweep, 二者都不是本机制的主路径。

---

## 6. 三份分开 — 逐份删除清单

### 6.1 `a1-entry-claim-duplicate-work-guard` (876 行 / 157.6KB)

| 级 | # | 条款 | grep 锚点 | 删了会漏掉哪个已实证缺陷 |
|---|---|---|---|---|
| **C** | C1 | 双 track-id 形态及其全部下游 (§5.1 / §5.3 spec_slug / track_form / K1 前半 / K2 / K4 / SC-1,4,15,27C,30,31 / D12 / 5 行 Impact) | `#### §5.1 二分谓词` · `#### §5.3` | **不漏** R2/C1·C-B·C-C (逐条核对见 §1)。**新增**一条同容器 advisory 噪声 |
| **C** | C2 | K1 的 8 行透传表 + 「17 处 / 5 文件」论证 | `🔴 K1/K4 (R4)` | **不漏** —— `dataclasses.replace()` 覆盖全部 4 处保留式重建, 且对未来字段免疫 |
| **C** | C3 | `:779-876` 对账层 (15.6KB) + 4 处迁出占位节 (6.5KB) + 5 处「未经审计轮」blockquote | `## R1-fix editlist 逐条对账` · `⛔ **整节已迁出**` | **不漏** —— 对账的正确家是审计轨; 未做项的正确家是 A.2 任务 |
| **M** | M1 | `lib/identity.py` 新增 `get_container_uuid()` accessor + SC-3 + §2.1 `container_uuid` 格的依据段 | `新增直取 \`uuid\` 字段的 accessor` | **基本不漏**: `acquire_claim` `:151` 已用 `resolved.container_id` (= `get_container_id()`) 作 `container` 字段, 且 claim 存储路径是 `claims/<container>/<session>.yaml` ⇒ **container-id 唯一性是全机制的既有承重不变量**。track_id 复用同一个标识反而消除「两种容器身份」的新接缝。**残余风险 (须成文)**: 两个 label 经 `derive_track_id` 的 `./_→-` 归一后可能相同 (S5 的 `10cg.local` 形状) —— 概率低, 且可用一条断言兜 |
| **M** | M2 | `--heartbeat-only` 模式全套 (三级 track 来源回落 / 遥测分区隔离 / K7 / SC-32 / `coordination_probe.py` Impact 行) —— **§2.2 共 20.7KB** | `#### §2.2 保护窗` | **更小的等价物**: 在 `/state-scanner` 入口**重跑既有 acquire 路径** (幂等; 同 session 覆写同一 `claims/<c>/<s>.yaml`)。§2.2 自己写着「每次调 `phase1_gate` 都写一条新 claim ⇒ 再调即自然续期」却把它降为「冗余」, 理由是「依赖 AI 记得再调」—— **但 `--heartbeat-only` 挂的是同一个编排层, 同样依赖同一件事** ⇒ 该理由不成立。**真实 delta 只有一条**: acquire 会判碰撞 (7c/7d prompt), heartbeat 不判。⇒ **保留 `heartbeat_by_track()` 库函数, 删掉 `--heartbeat-only` 这个新 CLI 模式**, 由编排层调既有入口 + 现有 `--mode advisory` |
| **M** | M3 | `unknown_schema_claims` 全套 (§2.4a / K5 / SC-24 / SC-33 / 四态表第三行 / D14 / Impact `phase1_gate.py` ③) ≈ 6KB | `##### §2.4a` | 回来的是「竞品跑不同 schema 版本」场景 —— **本 Spec 自己的语料零实例** (Lab 2 容器)。Spec 已把它的「路径/身份」转 follow-up ⇒ **半个机制留在交付面比整条转 follow-up 更贵** (K5 就是这半个机制自己长出来的 critical) |
| **M** | M4 | `unattended` 全套 (§2.3 blockquote / D15 / SC-26 / `config-loader/SKILL.md` / `DEFAULTS.json` / rule6 描述性档) | `unattended` | **取值路径未钉死**: §2.3 写「由 aria-runner 容器镜像 **/** Nomad task env 显式置 true」—— 前者是 `.aria/config.json` 路径 (廉价、本 Spec 内可闭环), 后者是 env 三腿 (Spec 明写**不在本 Spec**, 缺 import ⇒ 静默 fallback `false`)。**二选一混写 ⇒ 按第二条读, 该分支在生产永不进入**, SC-26 只在夹具里为真。⇒ **要么把取值路径逐字钉死为 config.json (然后它是廉价且活的), 要么整条转 follow-up**。当前形态是两者中最贵的那个 |
| **M** | M5 | §2.3 的四档 status 选项表 → **缩为 2 档** | `对方 claim 的 \`status\`` | `abandoned` 档的落版结论逐字是「一律按 `active` 同档请裁」⇒ **与 `active` 档合并即可**, 只保留告警文案里一句「该状态可能是 GC 产物」; `unknown` 档随 M3 消失。⇒ 4 档 × 2-3 项 → 2 档。Spec 自陈该表「三个镜头都没提出, 是本轮执笔的综合裁断, 扩大了 A.1 决策面」(新表面 #2) |
| **m** | m1 | Impact 表 K1/K4 第 7 行「`release_gate.py` 已有 `--spec-slug` (读取端)」 | K1/K4 表第 7 行 | 基线实测 `grep spec_slug` **零命中**。措辞会被读成 baseline 已有; 应写「由本 Spec Impact 表另一行覆盖」 |
| **m** | m2 | §2.1 表 `container_uuid` 格里的 S3 spike 勘误注 (`:242` vs `:244`) | `S3 spike 勘误` | 勘误的**结论**已进 Impact 表; 注本身属审计轨 |
| **m** | m3 | 「决策记录」表里 4 条 `⛔ 已迁出` 的坟头行 (D1/D2/D7/D11) 与 SC 表里 6 条 `⛔` 行 | `⛔ **已迁至` | 编号纪律要求保留行号 ⇒ **保留编号即可, 删理由段** |

### 6.2 `linked-issue-field-availability` (606 行 / 76.8KB)

| 级 | # | 条款 | grep 锚点 | 删了会漏掉什么 |
|---|---|---|---|---|
| **M** | M6 | `.aria/linked-issue-field-grandfathered.txt` 新数据文件 + `--grandfathered` 参数 + **三子情形陈旧守卫** + SC-5(c) + SC-5(e) + K9 ≈ 5KB | `linked-issue-field-grandfathered` | **更小的等价物**: 6 条豁免路径直接写进 `.aria/state-checks.yaml` 注册行的 `command` (如 `--exclude a,b,c`)。⇒ **零新文件 / 零新格式 / 零陈旧守卫** —— 因为注册行本身就是仓本地的, 且随 check 一起被看见。K9 (白名单文件不存在 ⇒ `rm` 一条命令静默整条 check) 这个 critical **结构性消失**: 没有可 `rm` 的文件。分发面零 Aria 路径这一诉求同样满足 (脚本里无路径, 路径在注册行) |
| **M** | M7 | E0 谓词 2 (fence 状态机) 的三条已知限 + `(?:> ?)?` 论证 ≈ 2KB | `fenced code block 排除` | **机制保留** (它挡住的假阳性是真的, 且探针席独立采纳)。删的是**论证与已知限的篇幅** —— 三条已知限 (缩进代码块 / 嵌套围栏长度 / 两层 blockquote) 全部自陈「真实语料零实例」⇒ 属审计轨 |
| **m** | m4 | §Why 的两级假阳性剔除逐条命令输出 (`:29-101`, 6.4KB) | `### 重测 — 终值` | 该节自己写着「**数字是当日观测, 口径 (命令) 才是规范**」—— 那就**只留命令**, 输出进审计轨 |
| **m** | m5 | 「与 `sibling-spec-probe` 的术语对齐」逐格比对表 + 「本席的建议映射」留痕 (`:275-291`, ≈3KB) | `与 \`sibling-spec-probe\` 的术语对齐` | 该表 8 行里 **7 行判「一致/兼容」**; 唯一实质差异 (`BAD_TOKEN`) 自陈**已闭环**。⇒ 留一行结论, 表进审计轨。**若两份 Spec 合回一份, 整表消失** |

### 6.3 `sibling-spec-probe` (557 行 / 71.9KB)

| 级 | # | 条款 | grep 锚点 | 删了会漏掉什么 |
|---|---|---|---|---|
| **M** | M8 | §6 规模上限的排序契约 + 截断点路径 + `caps_applied[]` + `status=degraded` 四件套 → 缩为「cap 触发 ⇒ `degraded` + `reason=cap_applied`」 | `### §6 规模上限` | `MAX_PROPOSALS_SCANNED = 1000` vs 本仓实测 **147 篇**。「`changes/` 排前, 字节序升序, 尾部截断」这套决定性排序契约是为一个 **6.8× 余量之外**的场景写的。**保留 cap 与披露, 删排序契约与 `dropped_from`** ⇒ SC-6 从三个断言缩为两个 |
| **m** | m1' | §3 `BAD_TOKEN` 格内嵌的 K8 交叉订正 (整段塞进一个表格单元) | `R4/C-M3 + 姊妹 K8 交叉补` | 表格单元里塞 6 行论证 —— 移出成正文小节, 或随合并消失 |
| **m** | m6 | `:519` 的「本仓既有惯例是复制而非跨 skill runtime import」与 `:144` 的「先例确实存在, 本 Spec 采用 import」**同文档自相矛盾** | `跨 skill 复用的形态待 A.2 定` | **这条不是删除建议, 是缺陷**: `:519` 是 R4 之前写的, `:144` 是 R4 之后补的, 两处未同步。按 `:144` 统一 |

---

## 7. Combined — 三份合起来的判断

### 7.1 数量对账

| 面 | 当前 | 采纳 C1+C2+C3+M1~M8 后 (估算) |
|---|---|---|
| 规格文本 | 2039 行 / 306.3KB | ≈ **1150 行 / 175KB** (−43%) |
| 新增 claim 字段 | 2 | **0** |
| 新增 CLI flag | 2 (`--include-terminal`, `--spec-slug`) + 1 模式 (`--heartbeat-only`) | **1** (`--include-terminal`) |
| 新增 lib 函数 | 3 (`heartbeat_by_track` / `get_container_uuid` / `extract_linked_issue_field`) | **2** (删 `get_container_uuid`) |
| 新增脚本 | 2 (`linked_issue_field_probe.py` / `sibling_spec_probe.py`) | **2** (均承重) |
| 新增仓本地数据文件 | 1 | **0** |
| 新增 config key | 1 (`unattended`) | **0 或 1** (取值路径钉死才留) |
| 新增 AB 套件 | 1 | **1** (Rule #6 义务, 不可自豁免) |
| 新增输出键 | 2 (`unknown_schema_claims` / `linked_issue_overlap_error`) | **1** (`linked_issue_overlap_error` 承重, 它是 R2/M-4 的本体) |
| R4 的 9 条 critical 中被**结构性**消解的 | — | **K1 (C2) · K2 (C1) · K3 ((d) 或 C1) · K4 (C1) · K5 (M3) · K7 (M2) · K9 (M6)** = **7/9**; 残留 **K6** (abandoned provenance, M5 已把它折叠) 与 **K8** (placeholder, 字段 Spec 的真承重条款) |

### 7.2 ⭐ 与 memory `no-ruling-shortens` 的对照

该 memory 记载的形状: **「112 行改动造 2838 行规格 / 85 审计 / 0 代码 / 8 天; 直接修 327 行 1 小时」**。

本批的实测比值:

| 量 | 值 | 来源 |
|---|---|---|
| 规格 | **2039 行 / 306.3KB** | `wc -l` |
| 审计轮 | R1→R5 (母) + R1 ×2 (子), 每轮 5 席 | R4 聚合 |
| 已落代码 | **0 行** | 三份均 Draft, 未进 A.2 |
| 最小可交付切片的代码面 | **约 12 行 Python + 5 处 SKILL.md 编辑** (§5) | 本席逐条核 |
| 全量交付面的代码估算 | 几百行 Python | 主控 |

**⇒ 「规格:代码」比在最小切片上是 ~170:1。** 这不是「Spec 太详细」的问题 —— 前四轮抓到的 critical 大多数是真的。这是**交付面选大了**的问题: 每加一个新表面就加一层可被审计抓的接缝, 而接缝上的 critical 又要用新条款去修, 新条款再造新接缝 (R4: **8/9 由上一轮修复引入**)。

**唯一能打断这个循环的动作是缩小交付面, 不是提高条款质量。**

### 7.3 拆 Spec 的净账 (owner 2026-08-23 方向 b 的事后核算)

**本席的判断: 拆 Spec 在本批是净负, 与 memory `split-makes-seams` / `no-ruling-shortens` 的预测一致。**

证据 (全部可 grep):
1. **自造接缝 ≥ 5 处**, 且每处都带人肉同步义务: 跨 skill import 骨架 ×2 (R1) · `fetch_gate` 反例 ×3 且结论不一致 (R2/m6) · NEW-01 论证 ×7 (R3) · K8 placeholder 两侧镜像 (R5) · 四态 ↔ 三态映射 (SEAM-2, 已闭环但花了一整轮);
2. **R3/C3 的整条 critical 就是拆分产生的** —— 逐字: 「三条约束不可同时满足 …… **E0–E6 实现无归属**, 探针那句『姊妹非阻塞』在实现层为假」。母 Spec 未拆时不存在这个问题;
3. **三份各自的「闸门状态 / 新表面 / 未审」层重复三遍** (≈15KB);
4. **母 Spec 自陈「两个子 Spec 的内容本轮未读、未核」** (未做/存疑 #6, 逐字:「若某条在两边都落空, 本轮的『迁出』就变成了『丢弃』」) —— 拆分的验证成本被显式承认未付。

**建议呈 owner: 在删除轮之后把三份合回一份。** 合并的删除量是 §2 的 R1–R7 全部 (12–15KB) **加上**三份对账层的两份 (≈10KB), 且**永久消除**五条同步义务。

---

## 8. 收敛判断

### 8.1 本席不主张「再加一轮通用审计」

R4 已判边际产出为负, 两席主动建议停止; 本席**同意**, 并补一条本轮的独立证据:

**本席这一轮抓到的 3 条 critical, 没有一条是「上一轮 fix 引入的新缺陷」——它们全部是从 R1 就一直在的结构性选择** (双形态自 §2.1 起就在; 逐字段重建自 baseline 就在; 对账层同居在切出审计轨那一刻就在长回来)。

⇒ 这说明**审计镜头的问题不是「不够多轮」, 而是前四轮的 15 个席位全部在问「这条写对了吗」, 没有一个席位问「这条需要吗」**。R4 的 5 个新镜头 (跨文件核验 / 实现蓝图 / 静默失败 / 验收覆盖 / 类型契约) 全是**正确性**镜头 —— 它们越强, 抓到的接缝越多, 而接缝数量正比于交付面大小。memory `marginal-return-negative` 逐字:「每件新手段 = 新表面」。

### 8.2 收敛的判据在本批不是「critical 归零」

按 memory `stop-adding-rounds`, 加轮判据是 **major 数是否还在降**。实测轨迹:

| 轮 | critical | major |
|---|---|---|
| R2 | 3 | 17 |
| R3 | 3 (内容全换) | 19 |
| R4 | ≈9 (内容再次全换) | ≈20+ |
| **R5 (本席, 单镜头)** | 3 (**结构性, 非上轮引入**) | 8 |

**major 三轮持平后上升, critical 内容三轮全换。** 按 memory `feedback_marginal_return_goes_negative` 的判据「本轮 fix 引入的 major 占比 > 1/2 即到拐点」—— R4 实测 **8/9**, 早已过拐点。

**⇒ 本席判定: 交付面不缩小, 任何轮次都不会收敛。** 因为收敛的定义是「本轮 fix 不引入等量新缺陷」, 而在 306KB 交付面上, 任何 fix 都必然落在某两条条款之间的接缝上。

### 8.3 本席建议的下一步 (非裁定 — Rule #10, AI 不自行选)

| 选项 | 内容 | 本席评估 |
|---|---|---|
| **(A)** ⭐ | **删除轮**: owner 就 C1 (双形态) 单点裁定 → 按裁定结果执行本报告的删除清单 → **不再跑通用审计轮**, 改跑一次**只看删除是否丢了已实证缺陷**的定向核验 (单席, 逐条对 §3 的 13 行表) | 唯一针对根因的选项。删除动作结构上不产生同形缺陷 |
| **(B)** | 采 R4 选项 (d), 不动交付面 | 删 ~10.7KB / 6.8%, 4 条 SC 回滚为代码类。**但若之后再采 C1, (d) 建的模块要重做** —— 顺序颠倒有返工成本 (§4.3) |
| **(C)** | 直接进 A.2, 让 9 条 critical 在拆任务时自然成形 | 本席**不推荐**: A.2 会把 2 个字段 × 9 处透传 + 3 个新脚本 + 1 个新数据文件全部拆成任务, 交付面在 A.2 只会变大不会变小 |
| **(D)** | 三份合回一份 (在删除轮之后) | 与 (A) 叠加执行; 单独执行价值有限 |
| **(E)** | owner 另裁 | — |

**本席明确不推荐的**: 再跑一轮 5 席通用审计。

### 8.4 若 owner 只有时间做一件事

**先答一个是非题: 「track-id 要不要两种形态?」**

- 答「不要」⇒ 27KB 规格 + 2 个 claim 字段 + 4 条 R4 critical 当场消失, 且 (d) 的必要性降为一个 20 行函数;
- 答「要」⇒ (d) 成为必需 (否则 K3 的四条 SC 永远只能挂 AB fixture), 且 K1/K2/K4 需按 C2 的类级修处置。

**这个问题目前没有被呈给 owner 过** —— R4 给的 (a)~(e) 五个选项里没有它 (memory `narrow-owner-options`: 选项都合法 ≠ 选项集完整)。

---

## 9. 本席的自我边界声明

1. **本席只跑了简化镜头**, 没有做正确性核验。本报告**不推翻**前四轮任何一条 finding —— 对 K1/K3/K4/K5/K7/K9 的处置建议都是「换一条更小的路让它结构性消失」, 不是「它不成立」;
2. **C1 (单一形态) 的逐条核对是本席实读得出的, 未经第二双眼睛。** 它推翻的是 D3/D12/FIX-15 三条既有决策的前提 ⇒ **按 Rule #10 必须呈 owner, 不得由 AI 落定**。若 owner 采纳, 建议单独派一席**只核 C1 的 7 行对照表**;
3. **M2 (`--heartbeat-only` 可删) 的「真实 delta 只有判不判碰撞」是本席推理, 未实跑验证。** A.2 采纳前须实测「编排层调既有 acquire 路径」是否真会在每次 `/state-scanner` 产生 7c/7d prompt;
4. **本席未核** `linked-issue-field-availability` §3 的 E0–E6 规则本身是否正确 (那是 R1 的事), 只核了它的**交付形态与篇幅**;
5. **删除量估算全部为字节级估算**, 未逐条试删。实际删除时可能因交叉引用而少删 10–20%。

