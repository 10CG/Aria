---
checkpoint: post_spec
round: 1
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R1 — a1-entry-claim-duplicate-work-guard (重写版 v2)

> **席位**: 5/5 · **5/5 REVISE** · `scope_ok` 5/5 true
> **counts (各席)**: TL 3C/6M/4m · BA 2C/3M/1m · QA 0C/4M/5m · CR **6C/9M/5m** · KM 2C/2M/1m
> **timestamp**: 1785710000000 · 审计对象: 主仓 `c6aa29a`
> **注**: 这是**重写版的首轮**, 与原版 R1/R2/R3 不构成同一序列。

## 判定

**REVISE。** 去重后 **5 个 critical 簇**, 四条经主控实读复验。

### 🔑 本轮的形状 (TL 与 CR 各自独立指出, 主控认同)

**三条最重的 critical 都不是「设计想错了」, 而是「设计对了但对既有代码的事实断言与实读不符」** —— 与 R3/C2 同形。重写把**设计**修对了, 却**没有逐条实读验证它引用的每一个代码事实**。

⇒ CR 的处方值得采纳: 下一版补**「Spec 事实断言逐条实读清单」**。

---

## Critical 簇 (去重后 5 条)

### C1 — 两个 A.1 落点的 `allowed-tools` 结构性不支持本机制
**4 席独立命中** (TL / BA / CR + QA 的 F1 相关) + **主控实读复验**

| Skill | `allowed-tools` 实读 | 缺 |
|---|---|---|
| `phase-a-planner` | `Read, Write, Glob, Grep, Task, Skill` | **无 `Bash`, 无 `AskUserQuestion`** |
| `spec-drafter` | `Read, Write, Glob, Grep, AskUserQuestion` | **无 `Bash`** |

⇒ §2 的核心 bash 命令**在两个指定宿主上都跑不了**; §2.3 的 `AskUserQuestion` 请裁在 `phase-a-planner` 上也跑不了。**Impact 表零覆盖该字段。**

**这是最简单也最致命的一条** —— 整份 Spec 的主机制在它自己指定的执行位置上**不可调用**, 而三轮审计 + 六条 spike 都没查过 frontmatter。

### C2 — §2.2 只换了 heartbeat 的匹配键, 没指定**谁调、何时调**
**TL + BA + CR 三席**

`heartbeat()` 生产调用点仍为 **0** (`constants.py:43-44` 自陈)。换匹配键**不产生刷新者** ⇒ 保护窗实质仍是 24h ⇒ **SC-5~7 可以全绿而问题原样存在**。

**spike S1 §6 明确把「谁在什么时机调」交还给 Spec** (「属 Spec 范围不属 spike」), 而重写**没有接住**。

**CR 补了一刀**: 判否「再调 phase1_gate」的理由 (依赖 AI 记性) **原样适用于**被采纳的 heartbeat —— 若 heartbeat 也靠 AI 记得调, 两者没有区别。

### C3 — §1 的字段格式对**真实语料 0/13 匹配**
**TL + CR 两席实跑**

TL 实跑 141 篇: 13 篇有「关联 Issue」字段者, 在前置 Spec 的归一下 **OK = 0 / UNPARSEABLE = 13**。原因: 真实写法是 markdown 链接形 (`[10CG/aria-plugin #122](https://...)`), 而 §1 规定 `<org>/<repo>#<n>` 裸形且**未给提取规则**。

⇒ (a) custom check 上线**即恒红** (129 篇存量恒黄); (b) 若照抄字段值传 `--linked-issue`, 收到的是**整个 markdown 链接** ⇒ 前置 Spec 要治的格式病**在上一层复现**。

**且本 Spec 自己头部仍无该字段** (KM/m1 + CR/m4 的 dogfood 缺口)。

### C4 — 对 `_TERMINAL` 的事实断言与代码相反
**CR + KM + TL 三席** + **主控实读复验**

实读 `collision.py:210`: `_TERMINAL = ("done", "abandoned", "unknown")`

- **不含 `yielded`** —— 而 §2.4 说它含。⇒ `yielded` **今天就已可见**, SC-8 的该子例 **baseline 即绿**;
- **含 `unknown`** —— 而 §2.4 **完全没讨论**它;
- 连带: R2/M3 (`yielded` 归属) 在重写中**丢失**。

### C5 — D6「无任何函数支持释放别的容器的 claim」**为假**
**CR** + **主控实读复验**

实读 `release_gate.py --help`:

> `--sweep-stale   顺带扫描: active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)`

⇒ 跨容器写别人 claim 的路径**存在**。D6 的「两步人工」定案建立在一个假前提上。**与 C2 复合更危险**: 若 heartbeat 仍无人调 (C2), 所有 claim 30min 后即 stale ⇒ `--sweep-stale` 对**几乎所有并发轨可达** (CR 判为数据破坏级)。

### C6 (KM) — `include_terminal` 传递链漏了第 0 段
**主控实读复验**: `linked_issue_overlaps` 的签名是 `(claims, own_track_id, own_linked_issue)` —— **无 `include_terminal` 形参**。§2.4 的「三段传递链」从 CLI flag 讲到 `_main()` 调用处, 却**没说要先给函数加这个参数** ⇒ 按字面实现在 `_main():1232` 直接 `TypeError`。**Impact 表零覆盖 `lib/collision.py`。**

---

## Major 簇 (去重后 10 条)

| # | 簇 | 席位 | 要点 |
|---|---|------|------|
| **M1** | 两 Spec 间**归一能力职责真空** | TL / KM | 姊妹 Spec 明写「只改内部谓词、签名不变」, 本 Spec Impact **无 `collision.py`**, 却两处依赖调用它 |
| **M2** | §5「放弃必 release」× §2.1「id 不含 slug」**互相拆台** | CR | 同 issue 三个方向共享 track_id ⇒ `release_claim_by_track` 释放**全部** active claim ⇒ 放弃一个方向**连坐** abandon 掉保留的方向 |
| **M3** | §4 探针的「同 issue」**匹配谓词全文未定义** | TL / CR | 按最可能的实现, 它在自己的 motivating case (#122 两份 proposal) 上**失效** |
| **M4** | 「进模板」只做了一半 | TL / BA / CR | R1/M1 要的是 `standards/openspec/templates/proposal-minimal.md` (模板 SOT), 而机械校验只落主仓 `.aria/state-checks.yaml` ⇒ **两条腿都不是 plugin-wide**, 采用方只得到「会退化」的那一半 |
| **M5** | `phase1_gate.py:1229` 的 `if args.linked_issue:` 门控整块 | TL / CR | 按 §1 自己的 9% 统计, **无字段是多数路径** ⇒ 主机制与探针**同时无输入**; §6 缺口表未列这最大一项 (R3 minor 亦丢失) |
| **M6** | `:1235-1237` 的 `except → []` 才是「零证据当正证据」的**真实落点** | CR | §2.5 只治了 `GateResult.error` ⇒ **SC-10 可绿而病仍在** |
| **M7** | §4 只扫默认分支 ⇒ **in-flight 竞品结构性不可见** | CR / BA | 与自述盲区及 §6 的覆盖归功不符; 且「各自默认分支」取法未定义, 实测朴素做法在第二 remote 上直接失效 |
| **M8** | §3 双落点是本版核心杠杆, **SC 零覆盖** | QA | 本仓已有同型先例 `test_phase_b_require_claim_present` 未套用 |
| **M9** | SC-9/SC-14 标「代码」但实测对象是 **SKILL.md 散文** | QA | 会退化成文本存在性检查; SC-14 更与既有机制 `test_release_abandoned_roundtrips` 重复, 恒真 |
| **M10** | SC-8/SC-10 把「CLI 可验证字段」与「消费层措辞」**捆在一条断言里** | QA | CLI 只吐 JSON 不产文案; SC-8 的可见性核心有扎实先例可执行 (`TestPhase1GateLinkedIssueCli` subprocess 模板) |

**另**: `coordination.enabled` 未在 `DEFAULTS.json` 注册, 本仓已有两个相反的缺键默认 ⇒ SC-9 极性两读 (CR/M8) · SC-1「改名 id 不变」无分支限定, 对 91% 无 issue 场景为假, **与 SC-15 断言相反** (CR/M1) · §2.3 强制请裁与 AD10 冲突, Layer 2 无人值守未定义 (CR/M5) · KM: `session-handoff.md` (track_id 自称的 SOT) 与 `coordination-ref-schema.md` 均未入 Impact 表

## Minor (选列)

`release_gate.py --status abandoned` 省略必需的 `--raw-track-id`, 单独调用会被 argparse 拒绝 (BA) · SC-13~19 整表**缺「怎么会红」列** —— 恰是本版最新最少被审的内容 (QA) · `layer-l-integration.md:45` 声称的 `update_heartbeat()` **全仓不存在** (TL) · §4 exit code 契约与 SC-18 不齐, 「无远端」恒非 0 (CR/QA) · 本 proposal 自身缺「关联 Issue」字段 (KM/CR, dogfood 缺口) · S3 spike 自身对 `identity.py:244` 有 2 行误差 (实为 `:242`, 未传导入正文) (KM)

---

## 经实测确认**成立**的部分 (下轮免重复)

1. **✅ SC-1~4 四个历史钉子全部钉住** (QA 用 `git show` 取三个真实历史版本原文逐字构造实现验证): SC-1/2/3 **必红**; SC-4 逻辑上也钉住, 只是标题略夸大 (它钉的是规格空白而非「曾实现又撤销的版本」);
2. **✅ spike 转述逐条忠实** (TL + KM 双席独立核对六份 spike): **未发现把「三选一」写成定论** —— S1/S3 的三选一在 spike 内部就已自行收敛为定案, 转述准确;
3. **✅ 被点名的 9 个代码行号引用全部准确** (CR 逐个实读) —— 失效的是**行号背后的语义断言** (C4/C5), 不是行号本身;
4. **✅ 数字全部核实通过** (KM): 141/13/9%/128 (算术亦核)、9 vs 2、13.8s、16⁸、R1-R3 counts、SC 7→15→19 演进;
5. **✅ 三轮 finding 吸收率高** (TL 逐条核对 R1 的 8 major + R3 的 6 major): **丢失 3 条** (R2/M3、R3 minor `:1229`、R1/M1 的 `standards/` 一半), 已分别落 C4/M5/M4;
6. **✅ `identity.py` 新增 accessor 可行** (BA 核实无缺陷);
7. **✅ §2.2「照抄 `release_claim_by_track`」在实现层可行** (BA) —— 障碍不在移植, 在 C2 的「谁调」。

---

## 收敛提示

**本轮是重写版首轮**, 不与原版 R2→R3 的 4→6 并列。

**两条积极信号**:
- TL: 「三条 critical **没有一条是『设计想错了』**, 全部是『设计对了但缺一层落地条件』, 修法皆为**加法**且**彼此正交** —— 这是重写相对打补丁的实质改善」;
- 四个历史钉子**全部钉住** ⇒ 第五版不会再踩前四版的坑。

**一条形状警告** (CR): 6 条 critical 中 **C1/C4/C5 同属「对既有代码的事实断言与实读不符」**, 与 R3/C2 同形; **C2/M1(SC-1)/M4 同源于「track-id 去 slug」决策的下游未穷举** (放弃 / 改名 / 终态三个动词)。

⇒ **CR 的两条处方值得写进下一版**: (i)「Spec 事实断言逐条实读清单」; (ii)「track-id 形态 × 生命周期动词影响矩阵」。

**AI 不预判裁决。**
