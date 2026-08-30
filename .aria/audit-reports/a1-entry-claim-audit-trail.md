# 审计轨 — `a1-entry-claim-duplicate-work-guard`

> **⚠️ 这份文件不是 Spec, 也不是 Spec 的一部分。**
>
> - **append-only**: 只追加, 不回改。历史记述保持它被写下时的样子。
> - **显式不维护与 Spec 的一致性**: 二者不一致时**以 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 为准**。**不得**因本文件的记述去回改 Spec。
> - **不受一致性检查器约束**: Spec 侧的机械检查只检查 Spec, 不检查本文件。
>
> **为什么切出来 (rework v3, 2026-08-25; 仿姊妹 Spec `linked-issue-normalization` 于 2026-08-07 的 owner 裁定「交付面与审计史切开」先例, 见 [其审计轨](linked-issue-normalization-audit-trail.md))**: 本 Spec 经旧版 R1/R2/R3 三轮 + 重写 v2 的 R1/R2 两轮, 同口径 major **17 → 17 持平** (R2 聚合报告判定「每轮 fix 引入 ≈ 等量同形缺陷」)。append-only 的审计叙事与收敛型交付面同居一文, 是 memory `audit-trail-not-in-spec` 点名的耦合形状 —— **处方 = 切开不重写**。
>
> **本文件承接全部「规定是怎么来的」。** 内容为 proposal.md 的**机械搬运 (按字节, 未重写)**; 唯一新增的是本文件的标题与各节标题。
>
> **⚠️ 本次切分是主控的流程判断, 非 owner 裁定 —— 已标请 owner 复议 (rework v3 说明书 D-J)。**

---

## 目录

1. [审计与 spike 轨迹 (原 proposal §审计与 spike 轨迹)](#1-审计与-spike-轨迹)
2. [§2.2 C2 (iii) 落版原文 (2026-08-23 owner 撤销前)](#2-22-c2-iii-落版原文-2026-08-23-owner-撤销前)
3. [§2.2「⚠️ 实读订正 · 请 owner 复议」原文 (已闭环)](#3-22-实读订正--请-owner-复议原文-已闭环)
4. [§3「⚠️ 实读订正 · 请 owner 复议」原文 (已闭环)](#4-3-实读订正--请-owner-复议原文-已闭环)
5. [事实断言逐条实读清单 (原 proposal §事实断言逐条实读清单, 2026-08-25 主控裁定切出)](#5-事实断言逐条实读清单)

---

## 1. 审计与 spike 轨迹

> 搬运自 proposal.md 的 `## 审计与 spike 轨迹` 整节 (rework v3 前的 `:440-461`), **逐字节未改**。

## 审计与 spike 轨迹

| 阶段 | 产出 |
|---|---|
| post_spec R1 (5 席) | 4C/8M/7m — 发现 `linked_issue` 无归一 (主机制静默失效) |
| R1-fix | 全量吸收, SC 7→15 |
| post_spec R2 (新眼睛, type-design-analyzer) | 2C/4M/4m — **两条 critical 都在 R1-fix 自己写的逻辑上** |
| R2-fix | 全量吸收, SC 15→19 |
| post_spec R3 (第三双新眼睛, code-architect) | 2C/6M/3m — **同口径 major 4→6 上升 ⇒ 判定不收敛** |
| **owner 裁定 A+B** | §0 抽出独立交付; 其余转 spike |
| **spike S1–S6** | 六条全完成; **S4/S5 各推翻一条上游审计结论** |
| **重写 v2** | 据 spike 结论重写 (非打补丁) |
| **post_spec R1 (rewrite v2, 5 席: TL/BA/QA/CR/KM)** | **5/5 REVISE** — 去重后 **5 个 critical 簇**; **三条最重 critical 都是「设计对了但对既有代码的事实断言与实读不符」** (与旧版 R3/C2 同形) |
| **R1-fix** | 全量吸收 (C1~C6 事实订正 + NEW-01), **C1 (allowed-tools 阻塞) / C2 (heartbeat 谁调) 两项转 owner 裁定, 未即时落版** |
| **owner 裁定 C1/C2 (2026-08-22)** | C1=(a) 扩 allowed-tools / C2=(ii)+(iii) heartbeat 挂 state-scanner 编排层 + STALE_TTL 放宽 (30min→24h 量级, (iii) 收窄版: 只到 24h 不无限延长) |
| **rework 第 1 轮** | C1/C2 落版 + 新增「事实断言逐条实读清单」(R1 聚合报告处方) |
| **上一轮核验 (6 findings: 3 major/2 minor/1 待归属确认)** | rule6_note 四处 SKILL.md 分类内部矛盾 / heartbeat 无 SC 或 fixture 钉住 / collision.py 协调项已过期 (sibling 分支已合并) / STALE_TTL 方向词误写 / 「附注」悬空引用 / R1 报告第二条处方 (ii) 未处置 |
| **rework 第 2 轮** | 逐条处理上一轮 6 findings: rule6_note 改四处二档 + 新增 (d) 点名行为; 新增 SC-20/SC-21 (追加编号, 不重排既有 SC); collision.py 协调项按 `origin/master@ca52d1c` (已合并, 早于本文件落盘) 改写为已解事实 + 补 master 行号; 方向词/悬空引用订正; R1 报告 (ii) 处方 defer 到 A.2 并写明理由 |
| **上一轮核验 (第 2 轮独立核验, 8 findings: 4 major/4 minor)** | owner 裁定原文两处被整段删除换 AI 转述且与原文有实质偏差 (major-3, 最重) / heartbeat 具体 CLI 入口未点名 (major-1) / `lib/collision.py` 缺 Impact 表行 (major-2) / rule6_note 能力面 hunk 误判「不单独申请豁免」而两套件实存 (major-4) / constants.py 三处过期注释未列 (minor-1) / mtime 引用会漂移 + diff --stat 文件数误记 (minor-2) / rule6_note「四处」计数漏 config-loader (minor-3) / `_run_gate_impl` 行号误记 (minor-4) |
| **rework 第 3 轮 (本次)** | 逐条落实上一轮 8 findings: §2.2/§3 两处 owner 裁定原文按 `git show 86540f2` 逐字恢复 (blockquote), 下接「落版 (AI)」与「⚠️ 实读订正 · 请 owner 复议」两段 (major-3, 含 STALE_TTL/sweep 理据矛盾请 owner 复议 + Rule #6 措辞误改已撤销); heartbeat 具体入口钉为 `phase1_gate.py --heartbeat-only` (major-1, 同步改 §2.2/(d)/SC-21/Impact 表); Impact 表补 `lib/collision.py` 行 (major-2); rule6_note 能力面附注按逐 hunk 判重写为「两套件均实存 ⇒ 照跑」, Impact 表 AB 行拆两行 (major-4); constants.py 行补三处过期注释 (minor-1, 含标题订正); mtime 引用改相对表述 + diff --stat 订正为一个 test 文件 (minor-2); rule6_note「四处」改「五处」补 config-loader 描述性档 (minor-3, 含 STALE_TTL/SWEEP_TTL 混用第三处引用); `_run_gate_impl` 行号订正为 `:335`–`:1032` (minor-4); 事实清单新增 #17 — **待 post_spec R2 (convergence 续审)** |

报告: 旧版三轮 `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-duplicate-work-guard-*` (`b7c4933` 之前) · **重写 v2 R1** `.aria/audit-reports/post_spec-R1-1785710000000-a1-entry-claim-rewrite-*` (5 席 + 聚合 + R1-fix editlist) · spike: `.aria/spikes/2026-08-02-*`

---

## 2. §2.2 C2 (iii) 落版原文 (2026-08-23 owner 撤销前)

> 搬运自 proposal.md `§2.2` 的 `(iii) STALE_TTL 30min → 24h 量级` 落版段 (rework v3 前的 `:154-157`), **逐字节未改** (含原有的 `> ` blockquote 前缀)。
> **现状**: owner 2026-08-23 裁定 **(iii) 撤销, 只采 (ii)**, `STALE_TTL` 维持 `1800`。以下内容**仅为历史记述**, 不再是 Spec 的一部分; Spec 侧的回撤见 proposal.md §2.2 / §2.3 / SC-20 / Impact 表 `lib/constants.py` 行 / 闸门状态 item 3 四处。

> **(iii) `STALE_TTL` 30min → 24h 量级** —— **实读落点 = `lib/constants.py:36`** (`STALE_TTL: int = 1800  # seconds`)。
> - **⚠️ 事实订正 (rework, 主控实读 aria@cb6bd5d)**: §2.3 原版称「所有 claim 在 `STALE_TTL`=30min 后即 stale ⇒ `--sweep-stale` 对几乎所有并发轨可达」, **这条因果链不成立**。实读 `lib/gc.py:341`—— `sweep_stale_active` 的 `stale_ttl_seconds` 默认值是 **`SWEEP_TTL`** (`lib/constants.py:51`, 86400s/24h), **不是** `STALE_TTL`; 且 `release_gate.py:141`(`sweep_stale_active(repo, now=ts)`) **未传** `stale_ttl_seconds` 覆盖, 故 `--sweep-stale` 的实际清扫阈值从来就是 24h, 与 `STALE_TTL` 的取值**无关**。`STALE_TTL` 实际控制的是 `reconcile._is_stale()` (`lib/reconcile.py:154-163`) 判定的「takeover-eligible」软信号 —— advisory、可在下次 read 时逆转 (`lib/constants.py:40-42` 逐字), 与 `--sweep-stale` 的**不可逆**改写是两回事。⇒ `release_gate.py:225` 的 help 文本 (`「顺带扫描: active 且 heartbeat 超 STALE_TTL → abandoned」`) 与 `state-scanner/SKILL.md:176` 的同款描述本身用词不准 (把 `SWEEP_TTL` 的行为记成了 `STALE_TTL`) —— 本 Spec 沿用了这处不准确描述, 现订正; 文档措辞本身的勘正**不在本 Spec 变更面** (非目标, 留 follow-up)。
> - **落版后的准确效果**: `STALE_TTL` 30min→24h 把 reconcile 的「stale/可 takeover」软信号窗口, 从「30min 未刷新即标 stale」**放宽**对齐到与 `SWEEP_TTL` 同量级 (owner 采 (iii) 的**收窄版**: 只到 24h, 不无限延长 —— 「收窄」修饰的是 (iii) 候选本身相对「无限延长」的克制, 不是 `STALE_TTL` 数值方向; `STALE_TTL` 数值本身是**放宽/变大**) —— 不再出现「heartbeat 编排层偶尔漏跑一次 (\<24h) 就被判 takeover-eligible」的假阳性。`--sweep-stale` 的**破坏性**清扫窗口本就是 24h, 不因本次改动而变。两个信号收敛到同一量级后, **残余风险**: 若 (ii) 的 `/state-scanner` 编排层调用**连续缺席超过 ~24h** (即 `SWEEP_TTL`), claim 仍会被 (a) reconcile 标 takeover-eligible 且 (b) `--sweep-stale` 清成 `abandoned` —— 但只要两次 `/state-scanner` 间隔 **≤24h**, claim 不 stale, 也不进 sweep 候选;
> - **不变量注释处置** (R1 rework 核验 minor-1 改标题 —— 原标题「TTL 变更量化的 sweep 语义代价」与内容不符: 内容讲的是常量注释同步, 不是 sweep 代价): `lib/constants.py:32` 现有注释断言不变量「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」(`HEARTBEAT_INTERVAL=600s`, `:28`) —— 若只改 `STALE_TTL` 不动 `HEARTBEAT_INTERVAL`, 该注释所述不变量将不再成立, 须在 B 阶段二选一: 显式改写注释承认「不变量在 heartbeat 编排层落地后已由『AI 编排层调用节律』替代『HEARTBEAT_INTERVAL 常量』」, 或按比例调 `HEARTBEAT_INTERVAL`。**sweep 语义代价 = 0**(阈值是 `SWEEP_TTL`, 见上方「落版后的准确效果」) —— 这里唯一要处理的是**文档不变量注释**要不要同步改, 与 sweep 行为本身无关。**本 Spec 不预判**, 留 A.2 任务项;

---

## 3. §2.2「⚠️ 实读订正 · 请 owner 复议」原文 (已闭环)

> 搬运自 proposal.md `§2.2` (rework v3 前的 `:161`), **逐字节未改**。
> **闭环**: owner 已于 2026-08-23 回应 —— 裁定 (iii) 撤销, 只采 (ii)。该复议项**不再未决**。

> **⚠️ 实读订正 · 请 owner 复议** (R1 rework 核验 major-3(a)): owner 裁定原文的理据——「`STALE_TTL` 30min → 24h 量级收窄版兜底, 使『漏跑一次扫描』不至于立即暴露在 `--sweep-stale` 下」——**与实读不符**: 上方「⚠️ 事实订正」已确认 `--sweep-stale` 的实际阈值从来就是 `SWEEP_TTL` (24h), 从未读取过 `STALE_TTL`; 改 `STALE_TTL` 对 `--sweep-stale` **零影响**, 其真实效果只是把 `reconcile._is_stale()` 的 advisory「takeover-eligible」软信号窗口从 30min 放宽到 24h。⇒ 裁定理据所指向的风险 (「漏跑一次扫描就暴露在不可逆清扫下」) 本来就不成立 —— 无论改不改 `STALE_TTL`, `--sweep-stale` 的不可逆窗口一直是 24h; 真正因 (iii) 改善的是 advisory 软信号面, 不是理据描述的那个 sweep 风险。**请 owner 确认**: 订正后是否仍采 (iii) (改 `STALE_TTL` 至 24h 量级, 效果落在 advisory/takeover-eligible 面, 是把两个原本量级悬殊的软硬信号对齐的一个自洽改动, 与原理据描述的 sweep 风险无关), 还是改为只采 (ii) (heartbeat 编排层每次 `/state-scanner` 必跑落地后, 30min 的 advisory 窗口触发面已收窄, 或许不必再动常量)? **AI 不替裁**, 本版按「暂按裁定字面 (iii) 落版, 标 pending owner」处理 —— 上方「落版」段的 (iii) 内容维持不变, 待 owner 回应后再定是否回撤。

---

## 4. §3「⚠️ 实读订正 · 请 owner 复议」原文 (已闭环)

> 搬运自 proposal.md `§3` (rework v3 前的 `:236`), **逐字节未改**。
> **闭环**: 该条自陈「核实结论与 owner 原话字面本就一致, 技术处置无需另行复议」, 仅为上一轮偏差的订正留痕; owner 2026-08-23 裁定未对其提出异议。

> **⚠️ 实读订正 · 请 owner 复议** (R1 rework 核验 major-3(b)): 上一轮把 owner 原话「落版义务: ... + Rule #6 按能力面变更申报 benchmark」改写成「不单独申请豁免、也不需要单独判据」, 二者语义相悖 (原话要求「去申报/跑 benchmark」, 改写读作「不需要单独判据、可并入覆盖外档定向 fixture 同批带过」) 且未经复议即落版 —— 已按上方「落版执行」项 2 撤销该改写。**所幸核实结论 (两套件实存 ⇒ 应照跑) 与 owner 原话字面 (「申报 benchmark」) 本就一致**, 本项技术处置**无需另行复议**, 此处仅记录订正过程供 owner 核对上一轮偏差; 如 owner 认为「申报 benchmark」另有所指 (例如指走一遍 `/skill-creator` 完整流程, 而非本版采用的「现有两套件全量跑一遍, 零裁量」), 请指出。

---

## 5. 事实断言逐条实读清单

> 搬运自 proposal.md 的 `## 事实断言逐条实读清单` 整节 (rework v3 主控裁定 2026-08-25), **逐字节未改**, 只加了本节标题与这条搬运说明。
> **为什么搬**: 它是**核验证据**不是交付面 —— 与本 Spec 2026-08-07 姊妹先例「交付面与审计史切开」同类; 且可由 `verify_line_refs.py` 随时重新生成。
> **⚠️ append-only**: 本表反映的是搬运当时 (aria `d50f9c3` / 主仓 `cc1bdef`) 的实读结果。它**不随代码演进更新**; 与 proposal 不一致时**以 proposal 为准**, 并用表头给出的复核命令重新实读。

## 事实断言逐条实读清单 (rework, R1 聚合报告处方; **rework v3 整表重新实读**)

> **触发**: post_spec R1 聚合报告 (`.aria/audit-reports/post_spec-R1-1785710000000-a1-entry-claim-rewrite-aggregated.md`) 判定「三条最重 critical 都是设计对了但对既有代码的事实断言与实读不符」⇒ 下一版须补本清单。该聚合报告实际给出**两条** CR 处方: (i) 本清单 (已落, 见下表); (ii) **track-id 形态 × 生命周期动词影响矩阵** —— **rework v3 已部分落地**: §5.1 的二分表 (issue 派生形 / 回落形 × 放弃一个方向 / 改名) 与 §5.2 的退出路径表合起来就是该矩阵的**已定形那一半**; 剩下的 acquire / heartbeat / sweep / gc 三个动词仍随 A.2 任务成形后补 (它们的调用点/参数在任务拆解前未定形)。
> **⚠️ 实读基线换了 (rework v3)**: 上一版的实读环境是 aria `cb6bd5d` (+ `collision.py` 另核 `ca52d1c`), **已过期**。本表**整表基线 = aria 子模块 `d50f9c3`** (= v1.67.1 `58a49e7` 之后 2 个 commit: `e1be8f3` 测试守卫 / `d50f9c3` secret-guard SC-8)。**复核方法逐字**: `git -C aria show d50f9c3:<path> | sed -n '<N>p'` —— 本表每一行的「现在实读结果」都由该命令产出, 未经推断。
> **⚠️ 主仓 gitlink 落后**: 主仓当前 gitlink 指向 `58a49e7` (= v1.67.1), 落后 `origin/master` (`d50f9c3`) 2 个 commit —— 那两个 commit **不触及**本表引用的任何文件行, 故两个基线在本表范围内等价; 但 A.2 实施前须重新 fetch 复核 (memory `feedback_concurrent_duplicate_audit_fetch_before_start`)。
> **方法**: 本表逐条列出 Spec 全文引用的 `文件:行号` 事实断言, 与**现在实读**结果比对。行号漂移是预期内的; **不一致的已在正文对应处订正**, 本表汇总一份可核对的清单, 不重复正文的完整论证。**§1 / §4 迁出后, 原属那两节的事实断言随该节迁至子 Spec, 本表相应行标「已随该节迁出」。**

| # | 断言原文 (Spec 引用) | 现在实读结果 (aria `d50f9c3`) | 一致性 |
|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md:9` — `allowed-tools: Read, Write, Glob, Grep, Task, Skill` | `:9` 逐字一致 | ✅ 一致 |
| 2 | `spec-drafter/SKILL.md:10` — `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion`; `:9` — `user-invocable: true` | `:10` / `:9` 逐字一致 | ✅ 一致 |
| 3 | `collision.py` 的 `_TERMINAL = ("done", "abandoned", "unknown")`, 在 `linked_issue_overlaps` 内 | **`:268`** 逐字一致 (旧版引 `cb6bd5d:210`, 已随姊妹 Spec 合并下移)。**附注**: 同文件另有第二处同名 `_TERMINAL`, 在 `classify()` 内且**不含** `unknown` —— 属**不同函数的局部变量**; **rework v3 未复核其行号 ⇒ 本表不给该行号** (零发明行号), 记于此仅为避免后续实现者看错函数 | ✅ 一致 → 正文已改引 `:268` |
| 4 | `linked_issue_overlaps` 现签名 `(claims, own_track_id, own_linked_issue)`, 无 `include_terminal` 形参 | **`:230-234`** 逐字一致, **三参数**, 无该形参 | ✅ 一致 |
| 5 | `if not own_linked_issue: return []` (`无` token 会 truthy 穿透的依据) | **`:265`** / **`:266`** 逐字一致 | ✅ 一致 → 正文已改引 `:265-266` |
| 6 | `if c.track_id == own_track_id: continue` (自排除, §2.1 容器段的依据) | **`:278`** / **`:279`** 逐字一致; `:279` 完整为 `continue  # same-name collision — reconcile's job, not ours` | ✅ 一致 → 正文已改引 `:278-279` |
| 7 | `phase1_gate.py` 中 `_main()` 调用 `linked_issue_overlaps` 的行 | **`:1233-1235`** = `out["linked_issue_overlap"] = linked_issue_overlaps(` / `claims, result.track_id, args.linked_issue` / `)`。旧版曾误记 `:1232` (那是前一行 `claims = read_claims(repo).claims`), 上一轮已订正为 `:1233`; 本轮进一步给出完整三行区间 | ✅ 一致 (区间已细化) |
| 8 | `claim_lifecycle.py` `heartbeat()` 按 `(container_id, session_id)` 匹配 | `def heartbeat(` 在 **`:178`**; 匹配行 **`:228`** 逐字 `if rec.container == resolved.container_id and rec.session == resolved.session_id:` | ✅ 一致 (匹配行号本轮新钉) |
| 9 | `release_claim_by_track` docstring 逐字引用 (「locates by (normalized track_id, container) and ignores session」) | `def release_claim_by_track(` 在 **`:377`**; 并存的 `def release_claim(` 在 **`:274`** (§2.2「增并存变体」的形态依据) | ✅ 一致 |
| 10 | `claim_lifecycle.py:425` — `release_claim_by_track` 只匹配调用者自己的 container | **`:425`** 逐字 `if rec.container == resolved.container_id` | ✅ 一致 |
| 11 | `identity.py` — `get_container_id()` label 优先, 无「只取 uuid」的 accessor | `def get_container_id(` **`:191`**; label 优先 return **`:222`** (`return label if label else uuid`); hostname 兜底 **`:242`** (`return _hostname()`); 新生成 uuid 路径 **`:244`** (`return uuid`)。全文无独立的「跳过 label 只返回 uuid」accessor ⇒ 「需新增」判断成立 | ✅ 一致 (本轮补齐 `:242`/`:244` 两处出处 — 旧版 §2.1 该格无任何行号) |
| 12 | `GateResult.error` docstring 预留 `"fetch_degraded"` token 但从未被赋值 | `phase1_gate.py:210` 逐字 `Possible values: "not_a_git_repo", "identity_error", "fetch_degraded",`; 全文无 `error=` 赋值用到它 | ✅ 一致 |
| 13 | `STALE_TTL` = 30min, 定义处 | `lib/constants.py:36` — `STALE_TTL: int = 1800  # seconds`; 同文件 `:51` `SWEEP_TTL: int = 86400  # seconds (24h)`; `:32` `# Invariant: STALE_TTL == 3 * HEARTBEAT_INTERVAL.` (`HEARTBEAT_INTERVAL: int = 600` 在 `:28`) | ✅ 一致 — **(iii) 已撤销 ⇒ 本 Spec 不再对该常量提出任何断言**; Impact 表只保留与 TTL 数值无关的注释同步项 |
| 14 | 「所有 claim 在 `STALE_TTL`=30min 后即 stale ⇒ `--sweep-stale` 对几乎所有并发轨可达」 | **不一致 (结论维持上一轮)**: `lib/gc.py:338-344` — `def sweep_stale_active(` 的 `stale_ttl_seconds: int = SWEEP_TTL` (**默认 `SWEEP_TTL` 非 `STALE_TTL`**); `scripts/release_gate.py:141` — `sw = sweep_stale_active(repo, now=ts)` **未传覆盖** ⇒ `--sweep-stale` 的实际阈值从来是 24h, 与 `STALE_TTL` 无关。`STALE_TTL` 实际控制 `lib/reconcile.py:154-163` 的 `_is_stale()` (`return age_seconds > STALE_TTL`, advisory 可逆) | ❌ 不一致 → **已订正** (§2.3 残余风险表)。**代码库既有的措辞缺陷** (`release_gate.py:225` help / `phase-d-closer/SKILL.md:56` 逐字都写「超 STALE_TTL」) **不在本 Spec 变更面** —— 记 follow-up |
| 15 | `state-scanner/SKILL.md:149` + `references/layer-l-integration.md:15` — B-entry「接线点 = AI 编排层, 不是 `scan.py`」/「Design A 条件触发」 | 两处逐字一致。`SKILL.md:149` 完整触发条件 = `state_scanner.coordination.enabled == true` **且** `tracks_multibranch.collision.kind` 非空 —— **这正是 §2.2 (ii) 按 R2/M-7 修正「无条件」语义的依据** | ✅ 一致 (本轮承重点从「挂载层」扩到「触发条件的两个合取项」) |
| 16 | 姊妹 Spec `linked-issue-normalization` 是否已改 `linked_issue_overlaps` 签名 / 协调项状态 | **已 ship 并归档** (`openspec/archive/2026-08-23-linked-issue-normalization/`)。实读 `sed -n '256,260p'` 得 `:257` 「⭐ `include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面 (owner 裁定 2026-08-08)」+ `:260` 「母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**」 | ✅ **协调项完全闭环** —— editlist FIX-11 要求的姊妹侧编辑**已由姊妹自己在 ship 前完成**, 本轮**不改归档件** |
| 17 | `_run_gate_impl` 对 `linked_issue_overlaps` grep 命中 0 | `def _run_gate_impl(` 在 **`:335`**, 下一个顶层定义 `def run_gate(` 在 **`:1032`**, `def _main(` 在 **`:1173`**。grep 命中 0 的结论成立 | ✅ 一致 (旧版误记 `334-1075`, 上一轮已订正) |
| **18** (新) | `phase1_gate.py` 的 `--linked-issue` 门控是「整块」的 (R2/M-3 的依据) | **`:1230`** 逐字 `if args.linked_issue:` ⇒ 不传实参时 `linked_issue_overlap` **键缺席**, 不是空列表 | ✅ 新钉 (旧版全文零提及, 是 R2/M-3 命中点) |
| **19** (新) | `phase1_gate.py` 的 overlap 异常路径把零证据写成正证据 (R2/M-4 的依据) | **`:1236`** `except Exception as exc:  # fail-soft: overlap advisory must not break the gate` / **`:1237`** `logger.warning("phase1_gate: linked_issue overlap check skipped (%s)", exc)` / **`:1238`** `out["linked_issue_overlap"] = []` | ✅ 新钉 → §2.4b 已给逐字修复 (`None` + `linked_issue_overlap_error`) |
| **20** (新) | `unknown` sentinel 的 `linked_issue` 为 `None` ⇒ overlap 通道结构性不可达 (editlist FIX-03 的依据) | `lib/claim_schema.py:165` `def parse_claim(raw: dict)`; unknown sentinel 构造在 **`:222-229`** 一带 (`ClaimRecord(` … `status="unknown",`), **构造时不传 `linked_issue`**; dataclass 默认 `lib/claim_schema.py:130` = `linked_issue: Optional[str] = None`。第二道门 `lib/collision.py:274` = `if not getattr(c, "linked_issue", None):` | ✅ 新钉 (**实测复现另见 §2.4a**: 直调 lib 得 `linked_issue=None` / overlap `[]`) |
| **21** (新) | `linked_issue_overlaps` 全函数不做新鲜度过滤 (§2.1 D-A 第 3 点 + §2.3 残余风险的依据) | 函数体 **`:265-292`** (`:292` = `return out`), 通篇无任何 heartbeat / stale 判断 ⇒ **对 stale claim 同样可见** | ✅ 新钉 |
| **22** (新) | 7c/7d 同名碰撞通道对 stale 竞品零 surface (§2.1 备选方案证伪的依据) | `def _takeover_eligible(verdict)` 在 **`:283-294`**, 判据 = `"stale_takeover_eligible" in reason or reason in {"no_active_candidates", "empty_claims"}` | ✅ 新钉。**7c/7d 两个分支的具体行号本轮未逐行实读 ⇒ 本表不给** (零发明行号); A.2 须补钉 |
| **23** (新) | `heartbeat()` 生产调用点为 0 (§2.1 备选证伪第 2 点 + §2.2 的前提) | `lib/constants.py:43-44` 逐字 `# and in reality NO production heartbeat loop exists (heartbeat() has zero` / `# production call sites; phase1_gate self-resume does not refresh either),` | ✅ 一致 |
| **24** (新) | `derive_track_id` 归一四步**不含**去容器段逻辑 (§2.1b carry-id 契约的依据) | `lib/track_id.py:61` `def derive_track_id(raw_id: str) -> str:`; `:70-76` 逐字四步 = lower / `/`·`.`·`_`→`-` / 截断 `MAX_TRACK_ID_LENGTH` (**`:18`** = `64`) / 非 ASCII 或超长走 sha256 回落。**无任何拼接或去段语义** | ✅ 新钉 |
| **25** (新) | Phase B / D.2b 的 carry-id 落点 (§2.1b + Impact 表三行的依据) | `phase-b-developer/SKILL.md`: ```` ```yaml ```` 起于 **`:85`**, `B.0 - REQUIRE claim (…)` 在 **`:86`** (**是 YAML 键不是标题** —— 实跑 `git show d50f9c3:skills/phase-b-developer/SKILL.md \| grep -n '^#\+ ' \| grep -c 'B\.0'` = **0**), `check:` **`:88`** (逐字 `check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)` —— **这是 §2.2 (ii) heartbeat track 来源第 ① 级的先例依据**), `if_missing:` **`:89`**, `--raw-track-id "<本 cycle carry-id/Spec id>"` **`:92`**; `branch-manager/SKILL.md:146` = `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)` (**实存标题级锚点**); `phase-d-closer/SKILL.md`: D.2b 表行 **`:42`**, `release_gate.py` 调用 **`:51-52`**, **`:55`** 逐字「carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串」, **`:56`** 含 `超 STALE_TTL` 误写 (见 #14, follow-up) | ✅ 新钉 → editlist FIX-13(1) / FIX-14 的落点全部实读钉死 |
| **26** (新) | `DEFAULTS.json` 未注册 `coordination` (R2/M-17 第 5 项的依据) | `git show d50f9c3:skills/config-loader/DEFAULTS.json` 的 `state_scanner` 段键 = `['confidence_threshold', 'auto_execute_enabled', 'auto_execute_rules', 'audit_log_path', 'sync_check', 'issue_scan', 'multi_remote', 'sync_freshness']` —— **无 `coordination`**; 而 `config-loader/SKILL.md:134` 登记 `state_scanner.coordination.enabled:` / `:140` 登记 `state_scanner.coordination.mode:` | ❌ **登记与注册不一致** → Impact 表新增 `DEFAULTS.json` 行; **这也是 rule6_note 新 substitute 的被测对象** (baseline 必红) |
| **27** (新) | SC-22 的宿主与先例强度 (editlist FIX-13(2)(3) 的依据) | `skills/state-scanner/tests/test_coordination_default_lockin.py:53` `def test_phase_b_require_claim_present(self):`; `:55` / `:56` 是**裸 `assertIn`** (`assertIn("B.0 - REQUIRE claim", …)` / `assertIn("REQUIRE claim", …)`) ⇒ **先例的断言强度不该抄**, SC-22 的正则+围栏外形态是有意的强化 | ✅ 新钉 |
| **28** (新) | `coordination-ref-schema.md` 存在且其 §3.2 不涉 overlap 面 (editlist FIX-17 的依据) | `skills/state-scanner/docs/coordination-ref-schema.md:129` = `### 3.2 Reader downgrade on unknown version`; `:133-139` 枚举 reader 侧 unknown 行为 **5 条** (must not crash / must return `status="unknown"` / skipped by reconcile / never written by a live session / should emit `soft_error`), **通篇不涉 overlap 面** | ✅ 新钉 → Impact 表按**断言形** (非「若存在」条件形) 登记追加第 6 条 |
| **29** (新) | AB 套件实存性 (rule6_note 的依据) | `aria-plugin-benchmarks/ab-suite/` 实测: `phase-a-planner.json` ✅ (`evals` = **2**) · `spec-drafter.json` ✅ (**2**) · `state-scanner.json` ✅ (**12**) · **`audit-engine.json` ❌ 不存在** | ✅ 新钉 → `audit-engine` 档**随 §4 迁出**, rule6_note 不再列它 |
| **30** (新) | 语料口径 (§⭐ 真正的瓶颈) | 主仓 `cc1bdef` 实跑: `find openspec -name proposal.md` = **147**; `grep -rl '**关联 Issue**' openspec --include=proposal.md` = **15** (14 在 `archive/`, 1 在 `changes/`); `find openspec/changes -name proposal.md` = **7** | ❌ 旧版的 `141 / 13 / 9%` **已作废** → 正文已换实测口径, 并写明「15」含形状假阳 |

| **31** (新) | `release_gate.py` 的必需参数三选一 (§5.2 命令形态订正的依据) | `git show d50f9c3:skills/state-scanner/scripts/release_gate.py \| sed -n '236,237p'` → `if not args.raw_track_id and not args.sweep_stale and not args.gc:` / `parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")` | ❌ 旧版全文写的裸 `release_gate.py --status abandoned` **会 `parser.error` 退出** → **已订正** (§5.1/§5.2/SC-14 三处补 `--raw-track-id`) |
| **32** (新) | `release_claim_by_track` 只匹配 **active** claim (§2.3 `done` 档「释放对方 claim 不可达」+ SC-27 的依据) | `lib/claim_lifecycle.py:425-427` 三个合取条件逐字 = `if rec.container == resolved.container_id` / `and rec.track_id == norm` / **`and rec.status == "active"`**; `:429-430` = `if not matches:` / `return AcquireResult(success=False, record=None, error="claim_not_found")` | ✅ 新钉 —— 使 §2.3 `done` 档的结论**从推理升级为实读断言** |
| **33** (新) | `layer-l-integration.md:45` 的 `update_heartbeat()` 是**悬空函数名** (Impact 表该行 ② 的依据, rework v3 新发现) | `:45` 逐字 = `` \| `heartbeat` \| `phase-b-developer` mid-cycle \| 每 10min (caller 负责调度) \| `lib/claim_lifecycle.py::update_heartbeat()` \| ``; `git grep -n 'update_heartbeat' d50f9c3` **全 aria 只命中这一行自身** ⇒ 该函数不存在 (真名 `heartbeat()`, `lib/claim_lifecycle.py:178`)。同行的 caller/节律 (`phase-b-developer` 每 10min) 与 `lib/constants.py:43-44`「zero production call sites」**直接矛盾** | ❌ **既有缺陷 (非本 Spec 引入), 但本 Spec 必须同步该文件** ⇒ 已点名进 Impact 表 (函数名 + caller/节律两处) |
| **34** (新) | `coordination_fetch` 的新鲜度谓词 (§2.2 (ii) heartbeat 复用 fetch 的依据) | `references/state-snapshot-schema.md:1029-1041` 声明该区块自 F6′ 起「**不再独立发起网络 I/O**」, 是 Phase 0.5 `remote_refresh` 的纯派生; `:1043` 逐字 `success: bool  # Reflects FETCH 1 (branch heads, load-bearing);`; `:1049-1051` `refs_fetched` 注释逐字「coordination ref only when Fetch 2 succeeded」; `:1056` `coordination_ref_present: bool \| null`; `:1061-1064` 其三态语义 (`true` 已取到 / `false` benign absent / `null` unknown) | ⚠️ **执笔席实读订正**: 主控口述判据「`coordination_fetch.success == false` ⇒ degraded」按 schema 是 **fail-OPEN** (`success` 只反映 Fetch 1 分支头, 与 coordination ref 无关; 二者可 `success=true` 而 `coordination_ref_present=false/null` 并存) ⇒ 本 Spec 改用 **fail-CLOSED** 合取谓词 `success == true` **且** `coordination_ref_present == true` |

**未逐条实读的低风险断言**: S1/S3/S4/S6 各 spike 报告内部的一次性历史测量 (事故窗 48-72h、入口覆盖 9 vs 2 等) 非可重复 grep 的代码事实, 不纳入本清单; spike 报告本身的可信度已由 owner 2026-08-02 的 A+B 裁定认可。**S2 的 fetch 耗时与 S5 的 `10cg.local` 仓实证随 §4 / §1 迁出, 由对应子 Spec 承担。**


---

## 6. 2026-08-30 owner 六项裁定与 1A 移出原文 (rework v4, append-only)

> **本节由 rework v4 (2026-08-30) 追加。** 裁定见决策单 `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md` (1A 恒用 slug 形 / 2b 不建派生宿主 / 3b 加跑 R6 / 4i 单独修 AB 推生产 ref / 5 采纳 SC-15·SC-2 重分类 / 6i 哨兵 `{none, 无}` + 否决「只认中文的机器 token」)。
> 下列块是 rework v4 用带锚点的编辑脚本从 `proposal.md` **替换或移出的原文** (块名 = 脚本锚点名; 替换后的新文本以 `proposal.md` 为准)。**本节 append-only, 不维护与 proposal.md 的一致性; 不得据此回改 proposal.md。**
> 其中随 1A **整体消失**的机制 (旧 §2.1 issue 派生形 / §5.1 二分谓词与 `track_form` 判定式 / §5.3 `spec_slug` 三元组 / K1 透传面 / K2 legacy 悬崖 / K3 四条 SC 降级 / K4 写入端 flag / D12 / SC-30·31 / Impact 四行) 在此完整保留, 供日后复议 1A 时对照。
> 同时移出的还有 rework v3 与 R3 清账轮的两份「新表面 (未审)」清单与「本轮未做 / 存疑」表 (它们的存活条目已在 proposal.md 尾部重列)。


<!-- ===== removed block: §2.1 head+basename+number ===== -->

#### §2.1 track-id 派生 (spike S3 定案)

`<归一后 basename>-<str(int(number))>-<container_uuid>`; 无关联 issue 时回落 `<spec-slug>-<container_uuid>`。

| 段 | 规则 | 依据 |
|---|---|---|
| `basename` | 经前置 Spec 归一 (含 S5 追加的 `./_ → -`) | 与 `derive_track_id` 两层对齐 |
| `number` | **`str(int(number))`** | 否则 `#007` 与 `#7` 派生两个 id ⇒ 自排除失效 ⇒ 自己较早的 claim 被误判为他人碰撞 |


<!-- ===== removed block: §2.1a SC-1/SC-4 两层表 ===== -->

⇒ **SC-1 / SC-4 的被测对象分两层, 缺一即无被测对象** (旧版把它们标成无宿主的断言, 是 R2/M-17 的命中点):

| 层 | 被测对象 | 宿主 | 怎么会红 |
|---|---|---|---|
| **文本层 (可机械)** | 两处 SKILL.md 的 A.1 步骤块里, `--raw-track-id` 占位串**字面**含 `<container_uuid>` 段, 且 number 段写作 `str(int(number))` 而非裸 `<number>` | `state-scanner/tests/test_coordination_default_lockin.py` (与 SC-22 同宿主, 扩它) | 当前两处 SKILL.md **根本没有** A.1 步骤块 ⇒ baseline 必红; 写成 `<basename>-<number>-<uuid>` (漏 `str(int())`) 的实现也红 |
| **行为层 (定向 fixture)** | AI 实际拼出的串是否遵守该规则 (`#007` → `7`; label 不参与) | 定向 AB fixture (rule6_note 覆盖外档) | 「照抄 `#007`」的臂与「归一成 `7`」的臂可分辨 |



<!-- ===== removed block: K3 块 ===== -->

> ## 🔴 K3 (R4) — 「不新增拼接函数」的**另一半代价**必须一并成文 (2026-08-27 补, 未经审计轮)
>
> **R4 实跑证据**: SC-2 的两臂在 `d50f9c3` 上**都是绿的** —— 臂(i) 含容器段绿; 主控 R3 加的负控臂(ii)
> 「容器段置空 ⇒ overlap 必须变空」**也绿**, 因为今天的代码本来就这样。根因: **夹具手写字符串**,
> **全程不执行任何派生逻辑** —— 而派生逻辑**没有代码宿主可执行**。
> (R3 主控还一度把 SC-2 的夹具约束写成「必须由 §2.1a 的 compose 函数派生」, 而本节明说不存在该函数 ——
> 那是「要求调一个不存在的函数」, 已订正。)
>
> **⇒ 交付一半是允许的, 但必须把另一半的代价写下来** (memory `knob-granularity` 只写了前半):
>
> **本 Spec 声明: 只要 track-id 派生没有代码宿主, 以下 SC **不能是代码类**, 一律降级为**行为类定向 fixture**,
> 并**明说它们只能由 AB eval 覆盖、不冒充结构化测试**: **SC-1 / SC-2 / SC-4 / SC-15**。
> - 降级**不是**放弃: 每条仍须在 rule6_note 的「覆盖外」档建**可证伪定向 fixture** (双臂须能分辨 AI 是否按 §2.1 规则拼串);
> - **禁止**把它们写成「代码 (CLI 全链路)」—— 那是本项目 R1/C4 点名过的「把 SC 挂在不存在的宿主上」;
> - **若 owner 采纳 R4 的选项 (d)「给派生一个代码宿主」, 本段连同这四条 SC 的类别一并回滚为代码类** —— 届时它们才真有牙齿。
>
> **未降级的相邻条目 (仍是代码类, 因为它们的被测对象确实存在)**: SC-23 (release CLI 往返) / SC-27 / SC-29 / **SC-30** / **SC-31**。



<!-- ===== removed block: §5 整节 ===== -->

### §5 claim 生命周期 — A.1 引入的新退出路径

> **⚠️ 本节整体按 R2/C-B 重写 (owner 点名必须在此解)**。**旧版的缺陷**: §2.1 的 track-id 不含 slug ⇒ 同一容器在**同一 issue 下试三个方向**时, 三个方向派生的是**同一个** track_id; 而 §5 旧版又写「探索性放弃必须 `release_gate.py --status abandoned`」(该命令形态本身也是错的, 见 §5.2 的命令形态订正)—— 一调即**连坐释放**该 `(container, track_id)` 下的**全部** claim (实读 `lib/claim_lifecycle.py:377` `def release_claim_by_track(` 按 `(container, 归一 track_id)` 定位, `:425` `if rec.container == resolved.container_id`), 把还在做的另外两个方向一并抹掉。

#### §5.1 二分谓词 —— **track-id 形态是否含 slug** (editlist FIX-15; §5 / SC-1 / SC-15 三处**必须用同一句谓词措辞**)

**release 的语义单元, 按 track-id 形态分档**:

| track-id 形态 | 语义单元 | 探索性放弃**一个方向** | **改名** |
|---|---|---|---|
| **issue 派生形** `<basename>-<n>-<uuid>` (**不含 slug**) | **(container, issue)** | **不 release** —— claim 表示「**本容器在做这个 issue**」, 换一个方向不改变该事实; **只有放弃整个 issue** 才调 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned` (必需参数见 §5.2 命令形态订正) | track-id **不变** (SC-1) |
| **回落形** `<spec-slug>-<uuid>` (**含 slug**) | **(container, spec)** | **必须 release** —— 每个方向自成 slug、自成一条 track | **release 旧 + acquire 新**两步 (SC-15) |

**判据一句话 (三处逐字复用)**: **「track-id 形态是否含 slug」** —— 含 slug ⇒ 语义单元是 (container, spec); 不含 slug ⇒ 语义单元是 (container, issue)。

> **⚠️ 判定式 (R3/TL-M4 补 —— 原文自称「可机械判定」却没给判定式)**:
>
> **两个看似显然的判定式都不成立, 逐条否决**:
> 1. **从 track_id 字符串反推** —— **有歧义**。反例逐字: `fix-issue-149-a1b2c3d4` 既可读成 `<basename=fix-issue>-<149>-<uuid>` (issue 派生形), 也可读成 `<spec-slug=fix-issue-149>-<uuid>` (回落形)。
> 2. **读 `claim.linked_issue` 是否非空** —— **对第三类给出相反答案**。本表 D12 的原依据 (editlist FIX-15) 已经点名过这一类: **「有 issue 却走回落形的后起 Spec」** —— 同 issue 的第二份 Spec 因 issue 派生形的 track_id 已被占用而落在**含-slug 形**, 它的 `linked_issue` **非空**却是回落形。
>    > **⚠️ 留痕 (主控 2026-08-25)**: 本轮修 TL-M4 时**一度采用了 (2)**, 并在恢复 D12 第三列时才发现原依据早已否决它 —— 即 memory `feedback_rationale_formula_contradiction_is_signal`「理据↔公式矛盾时别默认公式对, 理据常在保护公式漏掉的场景」。该误判已撤, 留此记形状。
>
> ⇒ **落版判定式 = 把形态显式记进 claim**: claim 增 additive 字段 **`track_form: "issue" | "slug"`**, 由**派生代码在 acquire 时按自己走的分支写入** (它当然知道自己走了哪支), 消费侧**零推断**。
> - 与 §5.3 的 `spec_slug` 同批引入, 同为 additive、同不 bump `schema_version`;
> - 旧 claim 无该字段 ⇒ 读作 `None`。**⚠️ K2 (R4) 订正 —— 此处原写「fail-CLOSED」是错的命名, 且与 §5.3 相反**:
> 「退回 ALL matching」正是 §5.3 自己逐字否决过的**连坐**, 它是 **fail-OPEN** (更危险的方向), 不是 fail-CLOSED;
> 且 §5.3 同时写着「只释放三元组匹配」⇒ **同一条 legacy claim 两个相反答案** (实跑: 释放 `[s1,s2,s3]` vs `[s2]`)。
> **落版 (2026-08-27, 未经审计轮)**: `track_form is None` ⇒ **不释放, 报错退出并点名该 claim**,
> 要求操作者显式传 `--spec-slug` 或 `--force-legacy-release-all` 二选一。理由: 上线当天**全部存量 claim** 都走这条路径,
> 让它默认走「释放全部」等于**默认连坐**; 而 release 是可重试的, 报错的代价远小于误释放。
> **新增 SC-31 (代码)**: 对一条无 `track_form` 的 legacy claim 跑 D.2b release ⇒ **非零退出 + 输出点名该 claim + 零 claim 被改写**;
> 带 `--force-legacy-release-all` 重跑 ⇒ 释放全部匹配。**怎么会红**: 默认释放全部的实现在第一臂必红。**baseline 必红**。
>
> 「含 slug」保留为**人类可读的名字**, `track_form` 字段是它的**机械定义**; SC-1 / SC-15 / SC-27 三处一律按该字段判, 夹具**不得预标形态**, 而应**跑派生代码让它自己写** (R3/TL-M4 点名: 预标形态的夹具对本缺陷免疫)。

#### §5.2 退出路径表 (按 §5.1 的谓词分档)

> **⚠️ 命令形态订正 (rework v3 实读)**: 旧版全文写的 `release_gate.py --status abandoned` **会直接 `parser.error` 退出** —— 实读 `git -C aria show d50f9c3:skills/state-scanner/scripts/release_gate.py | sed -n '236,237p'` 得
> ```python
>     if not args.raw_track_id and not args.sweep_stale and not args.gc:
>         parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")
> ```
> ⇒ 本节所有 release 调用**一律带 `--raw-track-id "<本轨 A.1 原串>"`** (`--status abandoned` 只指定写入的状态值, 不满足「三选一」)。**这条 baseline 即可证伪**: 照旧版字面写的实现连 CLI 都进不去。

| 路径 | 处置 |
|---|---|
| **探索性放弃一个方向** (A.1 试三个方向弃两个) | **按 §5.1 分档**: issue 派生形 ⇒ **不 release** (claim 继续代表「本容器在做这个 issue」); 回落形 ⇒ **必须**调 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`。义务写进 SKILL.md + **SC-27** (两臂可辨) |
| **放弃整个 issue** (不再做这个 issue 的任何方向) | **两种形态都必须** `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned` |
| **slug 改名** | **issue 派生形** (判定式 = `claim.track_form == "issue"`, 见 §5.1; **既不从 track_id 反推、也不看 `linked_issue`**): track-id 不含 slug ⇒ **改名不改 id**, 问题从源头消失 (SC-1)。**回落形 (含 slug)**: 须走 **release 旧 + acquire 新** 两步 (SC-15) —— `release_claim_by_track` 按 `(container, 归一 track_id)` 定位、**不依赖 session**, 可直接照字面实现 |
| **A.1 成功并走完循环** (最常见, R2/C-C) | **A.1 原串即 carry-id, B.0 与 D.2b 逐字节复用** (§2.1b) ⇒ D.2b 的 `release_claim_by_track` 能匹配到 A.1 那条 claim。**由 SC-23 钉住**。**不靠 sweep 兜底** —— sweep 只是 GC, 不是设计中的释放路径 ⚠️ **但 release 的作用域有缺陷 —— 见 §5.3 (R3/TL-C1)** |
| **D.2b 对偶** | 只有**走完循环**的轨才到 D.2b; 上面「探索性放弃 / 放弃整个 issue / 回落形改名」三条**不经过它**, 故各自显式 release。⚠️ **issue 派生形下 D.2b 的 release 会连坐同 issue 的其他在制方向 —— 处置见 §5.3** |

#### §5.3 D.2b 的 release 作用域 —— C-B 的另一半 (R3/TL-C1)

> **R3 判定 C-B「只闭一半」**: §5.1/§5.2 解决了「探索性放弃**一个方向**不 release」, 但**漏了对偶路径** ——
> 方向 1 **走完循环**到 D.2b 时, `release_claim_by_track` 的 docstring 逐字写着
> 「If several active claims match (**same container re-claimed a track across sessions — the NORMAL case, since every session mints a fresh session_id and B.0 REQUIRE-claim runs per session**), **ALL matching active claims are released**」
> (`lib/claim_lifecycle.py`, `release_claim_by_track` docstring; 实读基线 `d50f9c3`)。
>
> **⚠️ 引文订正 (R4/code-explorer 抓, 主控复核确认自己错了)**: 本段上一版把该 docstring 引成「If several active claims match **(same session)**, ALL matching…」。**原文没有「same session」这四个字** —— 实读 `claim_lifecycle.py:396-399` 逐字为上方新引文。**错法**: 主控当初跑的是 `sed -n '387,400p' | grep -iE "all|matching"`, grep **丢掉了不含关键词的 `:397-398` 两行**, 而主控把返回的 `:396` 与 `:399` 当作相邻行**拼接**成了一句 —— 造出一句原文不存在、且语义方向相反的引文。**机械核验器对此天然免疫** (两行都真实存在), 这是「该行存在 ≠ 该断言属实」的又一实例。
>
> **⇒ 订正后 C1 的结论不但不弱, 反而更强**: 原文明说多条 claim 匹配同一 track 是「**同一容器跨 session 重新认领 — the NORMAL case**」, 因为每个 session 都生成新 session_id 且 B.0 每 session 都跑 ⇒ **同 track 多 claim 是常态而非边角**, D.2b 的 ALL-matching 释放因此**几乎必然**触及仍在制的其他方向。
> 而 issue 派生形下, 同 issue 的 N 个方向**共用同一个 track_id** (各自 session 不同) ⇒
> **方向 1 收尾会把仍在制的方向 2/3 的 claim 一并释放**。SC-27 原本只有两臂, 结构性抓不到这条。

**处置 (落版) — claim 增 additive 字段 `spec_slug`, release 按 (container, 归一 track_id, spec_slug) 定位**:

| 项 | 内容 |
|---|---|
| **新增字段** | claim schema 增 `spec_slug: Optional[str]` (**additive**, 与 Part B1 引入 `linked_issue` 同款: 旧 reader 忽略未知字段, 不 bump `schema_version`) |
| **写入点** | A.1 acquire 时写入本 Spec 的目录名 (`openspec/changes/<slug>/`); 回落形的 track_id 本就含 slug, 该字段与其冗余但**不矛盾** |
| **release 定位** | D.2b 传 `--spec-slug "<本 cycle 的 spec 目录名>"` ⇒ 只释放 `(container, 归一 track_id, spec_slug)` 三元组匹配的 claim; **未传该参数时行为逐字节不变** (= 现状 ALL matching), 故 **Phase B/D 既有调用零影响** |
| **为什么不用 track_id 承载方向** | 把方向塞进 track_id 会同时破坏 C-B 的第一半 (三方向变三条 track ⇒ 同 issue 的 overlap 检测退化) 与 C-C (carry-id 一致性)。`spec_slug` 作**独立字段**让 track_id 继续只承载「哪条 issue」, release 另有维度可用 |

> ## 🔴 K1/K4 (R4) — 两个新字段的**透传面**与**写入路径** (2026-08-27 补, 未经审计轮)
>
> **R4/type-design A-C1 实读**: `heartbeat()` 在 `lib/claim_lifecycle.py:244-256` **逐字段重建** `ClaimRecord`
> (显式列 11 个字段, 含 `linked_issue=existing.linked_issue`), **不是** `dataclasses.replace`。
> ⇒ 不同步改这一段, `spec_slug`/`track_form` **每次 heartbeat 都被抹掉** —— 而本 Spec 的核心正是
> 「每次 `/state-scanner` 跑 heartbeat」⇒ **字段活不过第一次心跳, §5.3 的 release 三元组永不匹配, C-C 回归**。
>
> **R4/pr-test C-3 实读**: Impact 原只给 `release_gate.py` 加 `--spec-slug` (**读取端**),
> 而 `phase1_gate.py` 无对应 flag、Spec 又明写「不碰 `run_gate`/`_run_gate_impl` 签名」⇒ **写入端缺失**,
> SC-27(C) 的 CLI 全链路夹具**不可构造**。
>
> ### 透传面逐条枚举 (照 `linked_issue` 先例; **不枚举就等于没做**)
>
> 先例实测: `git -C aria grep -c "linked_issue=" d50f9c3 -- skills/state-scanner/` ⇒
> `claim_lifecycle.py:4` · `claim_schema.py:1` · `gc.py:1` · `phase1_gate.py:5` · `tests/test_release_by_track.py:6`
> = **17 处 / 5 个文件**。两个新字段**各自**需要同等覆盖:
>
> | # | 落点 | 动作 |
> |---|---|---|
> | 1 | `lib/claim_schema.py` `ClaimRecord` | 加两个 `Optional[str] = None` 字段 + `parse_claim` 读取 + `to_dict`/序列化写出 |
> | 2 | `lib/claim_lifecycle.py::acquire_claim` | **写入**两字段 (`track_form` 由派生分支自己写) |
> | 3 | **`lib/claim_lifecycle.py::heartbeat` `:244-256` 的逐字段重建** | **必须加两行** `spec_slug=existing.spec_slug` / `track_form=existing.track_form` —— **K1 的本体** |
> | 4 | `lib/claim_lifecycle.py::release_claim` / `release_claim_by_track` | 同样的重建/写回路径逐一核 (凡逐字段构造 `ClaimRecord` 的地方都要加) |
> | 5 | `lib/gc.py` (`sweep_stale_active` 改写 status 时) | 同上 |
> | 6 | **`scripts/phase1_gate.py` 的 A.1 acquire 路径** | **新增 `--spec-slug` CLI flag** 并透传给 `acquire_claim` —— **K4 的本体**; `track_form` 由派生逻辑内部决定, 不走 CLI |
> | 7 | `scripts/release_gate.py` | 已有 `--spec-slug` (读取端) |
> | 8 | `tests/` | 两字段各自的往返测试 (见 SC-30) |
>
> **⚠️ 关于「不碰 `run_gate`/`_run_gate_impl` 签名」**: 该承诺**维持** —— `--spec-slug` 与 `--include-terminal` 同款,
> 在 `_main()` 内解析并传给 `acquire_claim`, **不进** `run_gate` 的公开签名。若 A.2 发现无法绕开, 属**超出本 Spec 承诺**, 须上呈。
>
> **新增 SC-30 (代码, 往返)**: acquire (带 `--spec-slug`) → **跑一次 heartbeat** → 读回 claim ⇒ 两字段**逐字节不变**。
> **怎么会红**: 不改 `:244-256` 逐字段重建的实现, heartbeat 后两字段变 `None` ⇒ 必红。**baseline 必红** (字段今天不存在)。
> **这条是 K1 的验收本体, 缺它则 K1 的修复无法证伪。**

> **⛔ 已考虑并否决的替代**: 「不加字段, 接受连坐 —— 幸存方向在下一次 B-entry 的 `phase1_gate` 会自动重新 acquire」。
> **否决理由**: 从 D.2b 到下一次 B-entry 之间, 幸存方向**处于无 claim 状态** ⇒ 对其他容器不可见 —— 这正是本 Spec 存在要关闭的那个窗口。
> 用「事后自愈」换「窗口期不可见」是**本 Spec 自我否定**。该替代方案与其残余窗口一并成文, 供 R4 复核本裁断。

> **⚠️ 本条是 rework v3 之后新增的设计裁断 (主控 2026-08-25), 未经任何审计轮** —— 请 R4 优先审它。




<!-- ===== removed block: 四个被推翻版本 intro ===== -->

> **⚠️ 被测对象与宿主 (R2/M-17 第 1 项补 —— 旧版这四条没有宿主, 是「无被测对象的 SC」)**: §2.1 的拼接**没有代码宿主** (见 §2.1a), 故 SC-1~SC-4 一律**分两层**: **文本层**断言两处 SKILL.md 的 A.1 步骤块里 `--raw-track-id` 占位串的**字面**, 宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py` (与 SC-22 同宿主); **行为层**断言 AI 实际拼出的串, 宿主 = 定向 AB fixture。


<!-- ===== removed block: SC-1 ===== -->

| **SC-1** | 原始版 (spec-slug ⇒ 改名孤儿) | track-id 为 **issue 派生形** (`<basename>-<n>-<uuid>`, **不含 slug** —— 与 §5.1 / SC-15 **逐字同一句谓词**) 的轨: slug 改名前后 track-id **不变** | 文本层 + 行为层 | 占位串写成 `<spec-slug>-…` (含 slug) 的实现必红; 当前两处 SKILL.md **根本没有** A.1 步骤块 ⇒ baseline 必红 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |


<!-- ===== removed block: SC-2 ===== -->

| **SC-2** | R1-fix 版 (纯 issue 派生 ⇒ 主机制死) | 两**不同容器**同 issue 各自 A.1 认领 ⇒ 双方 `linked_issue_overlap` **各含对方** | 代码 (CLI 全链路) | 去掉容器段的实现被 `lib/collision.py:278-279` 自排除 ⇒ 双方 overlap 恒空 ⇒ 必红 **⚠️ 恒绿风险已堵 (R3/QA-F2)**: QA 席实读 `tests/test_release_by_track.py:533` 的 `test_linked_issue_written_and_overlap_surfaced` —— 它传**两个手写的、不含容器段的** track 名, **今天就绿** ⇒ 若 SC-2 的夹具照它写, 本条**测不出**「容器段被丢弃」这个它声称钉住的 R1-fix 回归。 ⇒ **SC-2 的夹具硬约束**: 两条 track-id **按 §2.1 规则手写拼接**(**R4/C-1 订正 —— 主控担责**: 上一版写「必须由 §2.1a 的 compose 函数派生」, 而 §2.1a `:164` 逐字写着「**本 Spec 不新增拼接函数**」, 全文 grep `compose` 仅命中 SC-2 自身 ⇒ **SC-2 引用了一个本 Spec 明说不存在的函数**, 实现者写夹具时字面上找不到可 import 的对象 —— 正是本项目三次最重 critical 的同一形状, 这次由主控 R3 清账时引入。**订正后**: 夹具手写字面串是**允许且必要的** (拼接无代码宿主是 §2.1a 成文交付的一半); 归一仍走 `lib/track_id.py::derive_track_id`), 且断言**两层**: (i) 双方 overlap 各含对方; (ii) **把 compose 的 container 段置空重跑同一夹具 ⇒ 双方 overlap 必须变空** (负控)。缺 (ii) 的实现视为未满足本条 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |


<!-- ===== removed block: SC-4 ===== -->

| **SC-4** | R3 指出的 number 表示不一致 | `#007` 与 `#7` 派生**同一** track-id | 文本层 (占位串须字面写 `str(int(number))`) + 行为层 | 占位串写裸 `<number>` 必红; 行为臂上「照抄 `007`」与「归一成 `7`」两臂可辨 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |


<!-- ===== removed block: SC-15 ===== -->

| **SC-15** (代码) | track-id 为**回落形** (`<spec-slug>-<uuid>`, **含 slug** —— 与 §5.1 / SC-1 **逐字同一句谓词**) 的轨改名 —— 含「无关联 issue 者」**与「同 issue 后起 Spec 落在回落形者」** | release 旧 + acquire 新两步后**无孤儿** (旧 track 不再 active, 新 track active) | 只 acquire 不 release 的实现留下孤儿 claim ⇒ 必红; 用「有没有关联 issue」做谓词的实现在「有 issue 却走回落形」的第三类夹具上必红 **⚠️ 类别 (R4/K3)**: **行为 (定向 fixture)** —— K3 降级 —— 派生无代码宿主 ⇒ 本条**不得**写成代码类; 它只能由 AB eval 分辨「AI 是否按 §2.1 规则拼串」, **不冒充结构化测试** |


<!-- ===== removed block: SC-22 ===== -->

| **SC-22** (新) | 代码 | `phase-a-planner/SKILL.md` 与 `spec-drafter/SKILL.md` **各自**的 A.1 认领步骤 (R2/M-11: 双落点是核心杠杆却零 SC 覆盖) | ① `assertRegex(text, r"(?m)^#{2,4}[ \t]+前置: REQUIRE claim\b")` **且匹配行不在 ``` 围栏内** (最省实现: 先按 ``` 切段, 只在围栏外的段跑正则); ② 步骤块内含 `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` **四个字面量**; ③ 步骤块内含幂等谓词 `check:` + `if_missing:` (或等价的「本 session 已跑过 phase1_gate 则跳过」)。**宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py`, 扩它不另起文件** | 两处 SKILL.md 现**均无** A.1 步骤块 ⇒ baseline 必红。**裸 `assertIn` 明确不可接受** —— 子串检查对「把 `前置: REQUIRE claim` 原样塞进 A.1 现有 ```yaml 动作列表」这一种失败**免疫**, 而那正是 §2 明令禁止、§Why 引 R3/M6 论证过的原病。**docstring 须写明**: 与先例 `test_phase_b_require_claim_present` (`:53`, `:55-56` 两条**裸 `assertIn`**) 的断言强度差异**是有意的** —— B.0 的 YAML-键形态是既有欠缺, 另开 issue, 不在本 Spec 修。缺 ③ 的实现 (一次 A.1 写两条 claim + 两次外向推送) 也必红 **⚠️ 锚点换名 (R3/QA-F1)**: 原用 `A.0 - REQUIRE claim`, 但 `A.0` 在 `spec-drafter/SKILL.md` 已被占用为 **state-scanner** 步骤标签 (`:30` `- 查询项目状态 → 使用 \`state-scanner\` (A.0)`, `:369` 流程图同名, 另有 `A.0.5` = brainstorm) ⇒ 同名不同义。 现改用 **`### 前置: REQUIRE claim`** —— 与 `branch-manager/SKILL.md:146` 的既有真实标题 `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)` **同体例**, 该锚点是 editlist FIX-13 本来就点名的先例。正则相应改为 `r"(?m)^#{2,4}[ \t]+前置: REQUIRE claim\b"` |


<!-- ===== removed block: SC-27 ===== -->

| **SC-27** (新) | 代码 (CLI 全链路) | **三臂**: (A) track-id 为 **issue 派生形**的轨, 在同一 issue 内**放弃一个方向**后; (B) 同一条轨**放弃整个 issue** 后 (R2/C-B) | (A) claim 仍 **`active`**; (B) claim 为 **`abandoned`** | 旧版「探索性放弃必 release」的实现在 (A) 臂上会把 claim 释放掉 ⇒ 必红 (这正是连坐)。**两臂必须可辨** —— 只做 (B) 的测试恒绿, 抓不到连坐 **(C) (R3/TL-C1 补)**: 同 issue 下**两个方向各自持有 active claim** (同 track_id, 不同 `spec_slug`), 对方向 1 跑 D.2b 的 `release_gate.py --raw-track-id <原串> --spec-slug <方向1 slug>` ⇒ **方向 2 的 claim 仍 `active`**; **不传 `--spec-slug` 的实现会把方向 2 一并释放 ⇒ 必红** (baseline 必红: 该参数今天不存在) |


<!-- ===== removed block: D12 ===== -->

| **D12** (新) | **release 的语义单元按 track-id 形态分档**; **形态的机械判定式 = 读 claim 的 additive 字段 `track_form`** (R3/TL-M4: 从 track_id 字符串反推**有歧义** —— 反例 `fix-issue-149-<uuid>`; 读 `linked_issue` 则对「有 issue 却走回落形的后起 Spec」**给相反答案**; 两者均已否决, 见 §5.1), 含 slug ⇒ (container, spec) 必 release; 不含 slug ⇒ (container, issue) | **R2/C-B** + **editlist FIX-15** (谓词选「是否含 slug」而非「有没有关联 issue」—— 后者对「**有 issue 却走回落形的后起 Spec**」这第三类给出相反答案) + **R3/TL-M4** (该谓词的机械判定式 = 新增 additive 字段 `track_form`, 见 §5.1) |


<!-- ===== removed block: rule6_note 表 ===== -->

**本 Spec 涉及的 SKILL.md / frontmatter 改动 = 实数 6 处**, 逐档列清 (**不写「五处」之类未逐项列的计数**):

| # | 落点 | 性质 | 判据表落档 | 处置 |
|---|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md` frontmatter `allowed-tools` (`:9`, 加 `Bash, AskUserQuestion`) | **能力面** (影响该 skill **全部**运行场景, 含既有 eval case) | 第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」 | **照跑现有 `ab-suite/phase-a-planner.json`** (实测存在, `evals` = 2) |
| 2 | `spec-drafter/SKILL.md` frontmatter `allowed-tools` (`:10`, 加 `Bash`) | 同上 | 同上 | **照跑现有 `ab-suite/spec-drafter.json`** (实测存在, `evals` = 2) |
| 3 | `phase-a-planner/SKILL.md` 正文新增「前置: REQUIRE claim」认领步骤 | 处方性 · **套件覆盖外** | 第三行 | 点名行为 (a)(b)(c) + 定向 fixture, 见下 |
| 4 | `spec-drafter/SKILL.md` 正文新增「前置: REQUIRE claim」认领步骤 (第二落点) | 同上 | 同上 | 同上 |
| 5 | `state-scanner/SKILL.md` 新增「Layer L A.1 heartbeat 集成」小节 | 处方性 · 运行时指令面 | 第二行「照跑 AB, 零裁量」 | **照跑现有 `ab-suite/state-scanner.json`** (实测存在, `evals` = 12) + 在**该既有套件内新增 1 个 eval case** 钉点名行为 (d) |
| 6 | `config-loader/SKILL.md` 登记 `coordination` 的 A.1 skip 语义 + `unattended` 新 key | **描述性** (登记既有/新增字段, 不改任何 AI 决策路径) | 第一行「描述性 / 不适用 / substitute」 | **substitute 见下方 (已换, 旧 SC-9 无效)** |



<!-- ===== removed block: Impact claim_schema ===== -->

| `skills/state-scanner/lib/claim_schema.py` | **新增两个 additive 字段 `spec_slug: Optional[str] = None` 与 `track_form: Optional[str] = None`** (`"issue"`/`"slug"`; 缺省 `None` ⇒ 形态未知 ⇒ fail-CLOSED 退回现状并 log) (与 Part B1 引入 `linked_issue` 同款: 旧 reader 忽略未知字段, **不 bump `schema_version`**) —— C-B 另一半 (`spec_slug`) 与其形态判定式 (`track_form`, R3/TL-M4) 的载体 | **R3/TL-C1** (§5.3) |


<!-- ===== removed block: Impact claim_lifecycle 第二处 (spec_slug) ===== -->

| `skills/state-scanner/lib/claim_lifecycle.py` (第二处变更) | `acquire_claim` 写入 `spec_slug` **与 `track_form`** (后者由派生分支自己写, 消费侧零推断); `release_claim_by_track` 增 **keyword-only** `spec_slug: Optional[str] = None` —— 传值时按 `(container, 归一 track_id, spec_slug)` 三元组过滤, **不传时行为逐字节不变** (= 现状 ALL matching) ⇒ Phase B/D 既有调用零影响 | **R3/TL-C1** (§5.3) |


<!-- ===== removed block: Impact release_gate --spec-slug ===== -->

| `skills/state-scanner/scripts/release_gate.py` | 新增 CLI flag `--spec-slug`; 透传至 `release_claim_by_track` | **R3/TL-C1** (§5.3) |


<!-- ===== removed block: Impact phase-d-closer --spec-slug ===== -->

| `skills/phase-d-closer/SKILL.md` (第二处变更) | D.2b 的 `release_gate.py` 命令模板增 `--spec-slug "<本 cycle 的 spec 目录名>"` —— 不加则 issue 派生形下会连坐同 issue 其他在制方向 | **R3/TL-C1** (§5.3) |


<!-- ===== removed block: Impact schema spec_slug row ===== -->

| `skills/state-scanner/docs/coordination-ref-schema.md` (第二处变更) | §2.1 字段表增 `spec_slug` 行 + §2.2 说明其与 `track_id` 的分工 (track_id 承载「哪条 issue」, `spec_slug` 承载「哪个方向」) | **R3/TL-C1** (§5.3) |


<!-- ===== removed block: Impact heartbeat_by_track ===== -->

| `skills/state-scanner/lib/claim_lifecycle.py` | heartbeat **增 by-track 并存变体** —— **签名 (R4/C-2 补, 镜像 `release_claim_by_track`)**: `def heartbeat_by_track(raw_track_id: str, identity: Optional[Identity] = None, repo_path: Optional[Path] = None, *, spec_slug: Optional[str] = None, now: Optional[datetime] = None) -> AcquireResult` (仿同文件 `release_claim` `:274` / `release_claim_by_track` `:377` 的并存模式; **既有 `heartbeat()` 的 `(container, session)` 匹配键 `:228` 不动** — D16) | **S1** (原版 Impact 表零覆盖) |


<!-- ===== removed block: Impact tests row ===== -->

| `skills/state-scanner/tests/` (既有宿主) | SC-2 / SC-3 / SC-5~8 / SC-10 / SC-14(a) / SC-15 / **SC-22** (扩 `test_coordination_default_lockin.py`, 同时承载 SC-1/SC-4 的**文本层**) / **SC-23** / **SC-24** / **SC-25(代码臂)** / **SC-27** / **SC-29** + rule6_note 的 **`DEFAULTS.json` ↔ `config-loader/SKILL.md` 一致性 substitute 测试**。**⚠️ SC-20 已撤销, 从本行移除** | R1/C4 + rework v3 |


<!-- ===== removed block: Impact phase-a-planner ===== -->

| `skills/phase-a-planner/SKILL.md` | A.1 **独立标题级** `前置: REQUIRE claim` 步骤块 (锚点形态见 SC-22) + overlap/`unknown` 消费 (§2.3 按 status 分档的选项集) + release 义务 (§5.2 按形态分档) + `coordination.enabled` skip + `unattended` 分支 | R3/M6 + R2/C-B + R2/M-15 |


<!-- ===== removed block: Impact AB 照跑行 ===== -->

| AB 套件 — `phase-a-planner.json` / `spec-drafter.json` (能力面 hunk, **照跑档**) | `allowed-tools` 扩权 hunk 影响全场景; **两套件均实存** (rework v3 实核: `evals` 各 **2**) ⇒ **现有 AB 全量照跑, 零裁量**; 验「扩权后既有 eval 场景行为是否漂移」 | rule6_note 能力面附注 |


<!-- ===== removed block: editlist FIX-15 ===== -->

| FIX-15 | CR-M1 — SC-1/SC-15 二分谓词换「track-id 形态是否含 slug」 | **本轮落 (三处逐字同一句)** | grep `形态是否含 slug` (§5.1 + SC-1 + SC-15) |


<!-- ===== removed block: 头部 dogfood 行 ===== -->

> **关联 Issue**: `无` — 本 Spec 源自 5 次并发起草事故的直接观察 (§Why), 无独立 issue 号。


<!-- ===== removed block: 尾部三段 (rework v3 新表面 + R3 清账轮新表面 + 未做/存疑 + 旧闸门状态) ===== -->

## 本轮 (rework v3) 引入的新表面 (未审)

> 按硬约束「不新增未被要求的机制; 任何新表面必须列出」逐条声明。**本段是给 R3 审计席的输入, 不是完成度自述。**

1. **`.aria/audit-reports/a1-entry-claim-audit-trail.md` 新文件 + 本文件头部的四条切分声明** —— 流程判断, 非 owner 裁定, **已标请 owner 复议** (D-J)。风险: 审计轨与 Spec 的指针若失效, 历史会变成孤儿; 缓解 = 审计轨内每节都标了它搬自哪个行区间。
2. **§2.3 的「按 status 分档的选项集」表** (R2/M-17 第 3 项的处置) —— **三个镜头都没提出这个具体形态**, 是本轮执笔的综合裁断。它把 §2.3 的选项面从 3 项扩到 4 档 × 2-3 项, **扩大了 AI 在 A.1 的决策面**。
3. **SC-1~SC-4 新增「宿主 / 怎么会红」两列, 并把它们拆成「文本层 + 行为层」** (R2/M-17 第 1 项的处置) —— 本轮裁断。它**没有**新增代码机制, 但把「拼接无代码宿主」这件事显式写成了交付面的一部分。
4. **rule6_note 的新 substitute (`DEFAULTS.json` ↔ `config-loader/SKILL.md` 一致性测试)** —— 新的测试面; 已在基线亲跑确认**当前必红** (清单 #26), 但**未验证**「它对一个坏实现 (只注册两键漏 `unattended`) 是否也红」—— A.2 须补该负控 (memory `adversarial-fixture`)。
5. **§2.1b 对三处 SKILL.md 占位措辞的改动** —— 与 §非目标「不动 Phase B 入口现有认领」的边界靠**成文定义**划开 (改取值口径不改闸门语义), **该划法本身未经审计席确认**, 已标请 owner 在 R3 确认。
6. **`linked_issue_overlap == null` 这个新的返回形态** (R2/M-4 的修复) —— 把该键的类型从「恒为 list」放宽为「list | null | 缺席」。**下游消费者未逐一核查**: 本 Spec 只核了 A.1 消费面; Phase B 消费面因不传 `--include-terminal` 且异常路径同样会走到 (它也调 `--linked-issue`) ⇒ **Phase B 的消费面也会看到 `null`**, 这一点**本轮未在 Phase B 侧做任何处置**, 是已知的未审边。
   > **⚠️ R3/BA-M3 订正 (主控 2026-08-25)**: 本条原自述「Phase B 两个入口都不带该参数」—— 那句话说的是 **`--include-terminal`**, 与本条的 **`--linked-issue`** **是两个不同的 flag, 被混为一谈**。 实读 `skills/phase-b-developer/SKILL.md:93` 逐字 `[--linked-issue "<repo>#<n>"] --repo-path "<repo root>"` ⇒ **Phase B 可选传 `--linked-issue`**, 传了就会走到本 Spec 改动的那段 (`phase1_gate.py:1230` 门控块) 并可能拿到 `null` 形态。 ⇒ **该消费路径真实存在, 不是理论风险**: Impact 表已补 `state-scanner/SKILL.md:176` 的四态契约同步行; 且 §非目标「不动 Phase B 入口现有认领」须按此**限定**为「不改 Phase B 的 **acquire 路径与默认参数**」, **不包括** advisory 键的类型放宽。
7. **`unknown_schema_claims` 输出键 + 门控改为 `or args.include_terminal`** (editlist FIX-03, 该 editlist 已自陈是其综合裁断) —— `--include-terminal` 时会**多跑一次 `read_claims`** (git ls-tree + 每文件 git show)。**未测其耗时。**

---


---

### R3 清账轮 (2026-08-25, owner 方向 a) **新引入且未经任何审计**的表面 — 请 R4 优先审

> 本段由主控在 R3 之后、R4 之前追加。下列每一条都是**为修 R3 的 critical 而新造的**, 因此**没有任何一轮审计看过它们**。

1. **claim schema 增两个 additive 字段 `spec_slug` / `track_form`** (§5.3 / §5.1) —— 是本轮最大的新表面。风险面: (a) 两个字段与既有 `linked_issue` 三者的**职责边界**是否真的互不重叠; (b) 旧 claim 无字段时的 fail-CLOSED 退化 (退回 ALL matching + log) 是否**真的比连坐更安全**; (c) 不 bump `schema_version` 的判断是否与 `coordination-ref-schema.md` §3 的演进契约相容。
2. **`release_claim_by_track` 增 keyword-only `spec_slug` 过滤** —— 声称「不传时行为逐字节不变」, **未实测**。
3. **`lib/linked_issue_field.py` 新模块 + `extract_linked_issue_field(text)` 纯函数** (字段 spec C3) —— 新的跨 Spec 复用面; 输入从「路径」改成「文本 blob」这个决定**未经审计**。
4. **`.aria/linked-issue-field-grandfathered.txt` 仓本地数据文件** (字段 spec C2) —— 新的数据面; 「文件不存在 ⇒ 空集而非错误」这条 fail-open 方向的选择**与本 Spec 别处的 fail-CLOSED 取向相反**, 需专门审它是否是对的例外。
5. **`--heartbeat-only` 的遥测分区隔离** (§2.2, R3/TL-M2) —— 新增一个 `_source` 取值或跳过遥测; 对既有 `coordination_probe` 计数口径的影响**只做了推理未实测**。
6. **锚点从 `A.0 - REQUIRE claim` 改为 `前置: REQUIRE claim`** (R3/QA-F1) —— 改了 SC-22 的正则与 5 处概念提法; **是否还有第 6 处兄弟位置未扫到**, 请复核。
7. **主控在本轮的一次误判留痕** (§5.1 判定式段): 一度把形态判定式换成被原依据明确否决过的「读 `linked_issue`」, 恢复 D12 第三列时才发现。⇒ 请 R4 特别检查**其余被我改动的条款里, 有没有同样覆盖掉了某条原依据**。

## 本轮未做 / 存疑 (给 R3 审计席)

> **写在这里而不是省略**: 隐瞒未做项会让下一轮审计在错误的完成度假设上工作 (memory `past-summary≠measurement`)。

| # | 未做 / 存疑 | 影响 |
|---|---|---|
| 1 | **editlist FIX-18 的 S3 勘误注已落**, 但 **`.aria/spikes/2026-08-02-S3-track-id-derivation.md:72` 本轮未实读复核** —— 该行号与内容沿用 editlist 的记述, 未自行验证 (零发明行号的边界: 引的是 editlist 的断言, 非本轮实读) | 若 editlist 记错了 spike 的行号, §2.1 的勘误注会指向错误位置; 勘误的**结论** (`:242` 是 hostname 兜底) 已由本轮实读独立确认, 不受影响 |
| 2 | **7c / 7d 两个分支的具体行号未实读** —— §2.1 的备选证伪引用了 7c 的条件表达式与 7d 的注释**原文**, 但**没有给行号** (清单 #22 已声明) | 论证成立与否不受影响 (引的是逐字原文), 但 A.2 实施时须先定位这两个分支 |
| 3 | **`phase-a-planner/SKILL.md` 内部的委派动作 / skip 条件行号未实读** —— §3 幂等分工段只给了语义, 没给锚点 (已在该段显式声明) | A.2 拆任务时须补钉 |
| 4 | **rule6_note 新 substitute 的负控未验** —— 只验了「baseline 必红」, 未验「对『只注册两键、漏 `unattended`』这种坏实现是否也红」 | 见「新表面」#4 |
| 5 | **`linked_issue_overlap == null` 对 Phase B 消费面的影响未处置** | 见「新表面」#6 —— 这是本轮**已知未闭**的一条 |
| 6 | **两个子 Spec 的内容本轮未读、未核** —— `linked-issue-field-availability` / `sibling-spec-probe` 由另外的执笔席并行起草, 本文件只给了**指针与依赖方向**, **未核对**它们是否真的接住了迁出的 C-A / M-1 / M-5 / M-6(audit-engine 档) / M-10 / M-17(§4 stdout) / FIX-06/07/08/10 | 若某条在两边都落空, 本轮的「迁出」就变成了「丢弃」。**R3 须跨三份 Spec 联审这一点** (memory `feedback_combined_mode_sister_spec_audit_value`) |
| 7 | **SC-2 与 SC-23 是一对负控, 但未验证它们不会同时为真** —— SC-2 要求 track-id 含容器段 (两轨可辨), SC-23 要求 A.1 原串与 carry-id 一致 | 二者在设计上相容 (carry-id 就是含容器段的那一串), 但**没有一条测试断言这个相容性**; A.2 须补 |

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 ⇒ **本版按默认跑 post_spec, 不豁免**。

**已裁事实** (rework v3 更新):

1. **重写 v2 的 post_spec R1 (5 席) 已跑完**, 判定 **5/5 REVISE**, 去重后 5 个 critical 簇 —— **不是豁免, 是走了正常闸门**;
2. **R2 (5 席) 已跑完**, 判定 **REVISE 未收敛**: 3 个 critical 簇 + **17 个 major 簇 (与 R1 持平)**。**⚠️ 本条取代旧版第 2 点的「R1-fix 已全量吸收」自述** —— 该自述**不实** (R2/CR-M4 命中: editlist 12 项未落), 现已删除并替换为上方「**R1-fix editlist 逐条对账**」段的逐项状态表 (FIX-01…19), **不再有任何无锚点的总结句**;
3. **owner 已于 2026-08-22 下裁 C1/C2**: C1 采 (a) 扩权; **C2 原采 (ii)+(iii), 2026-08-23 owner 复议后 (iii) 撤销, 只采 (ii)** —— `STALE_TTL` 维持 `1800` 不改, 四个落点已在 rework v3 逐一回撤 (SC-20 / Impact `lib/constants.py` 行 / §2.3 残余风险段 / 本段);
4. **owner 已于 2026-08-23 下裁方向 b (缩 scope)**: §1 → `linked-issue-field-availability`, §4 → `sibling-spec-probe`, 主体只留 A.1 入口认领 + track-id 契约 (C-B/C-C 必须在此解), **换人执笔**一次性清 R1 editlist 残项后再 R3;
5. **下一步**: 本版进 **post_spec R3 (convergence 续审, `max_rounds` 剩 2)**。**AI 不预判 R3 的裁决结果。**

**本轮的 AI 流程判断 (Rule #10 — 请 owner 复议, 不自行落定)**:

| # | 判断 | 为什么须复议 |
|---|---|---|
| 1 | **切出审计轨** (D-J): 把「审计与 spike 轨迹」整节 + 两处已闭环的「请 owner 复议」叙事 + (iii) 撤销前落版原文, 按字节搬到 `.aria/audit-reports/a1-entry-claim-audit-trail.md` | 仿姊妹 Spec 的 owner 2026-08-07 先例, 但**本 Spec 没有对应的 owner 裁定**; 搬运无损, 撤回成本低 |
| 2 | **carry-id 统一采 editlist 选项 A** (改三处 SKILL.md 占位串取值口径) | editlist U-3 明写「需 owner 判这算不算『动 Phase B』」; 本版按「owner 要求主体必须解 C-C」推定采 A, **推定本身未经确认** (§2.1b 边界段) |
| 3 | **§2.3 选项集按 status 分档** | 三个审计镜头都没提出该形态, 是执笔的综合裁断, 且它扩大了 A.1 的决策面 (见「本轮引入的新表面」#2) |

本 Spec 在 R3 通过并经 owner 批准前不进 A.2/A.3。

---

## 7. 2026-08-30 post_spec R6 (owner 加轮) 清账清单 (rework v4.1), append-only

> R6 五席 (config team, 全新镜头) 判 REVISE: CR 3C/11M/13m · BA 0C/2M/1m · TL 6C/9M/7m · QA 0C/3M/2m · KM 0C/3M/2m (PASS); 去重 7 个 critical 簇 + 20 条 major; 聚合与逐条处置见 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md`。本节只记母 Spec 侧「改了什么、为什么」, 原文由 git 历史保留 (`git log -p -- openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`)。

| 落点 | 改动 | 来源 |
|---|---|---|
| 头部 `Linked Issue` | 哨兵 `none` → 真 token `10CG/Aria#174` (生产 claim 的 `linked_issue`); FIX-19 行 / §Why `:83` / 字段 §5 表同步 | KM m2 |
| 头部前置依赖 | 新增 aria-plugin `--no-push` 修复为硬前置 (分支未推、非 origin/master 祖先) | TL M5 |
| §Why `:78/:83` | 两拼写 grep 命令 + 「当日观测」口径; 「真阳」句纠正 | CR M5 / TL M6 / QA M1 |
| §2 NEW-01 门 + 新「两阶段取值」段 | 省略门扩为「不产生合法 canonical 值」四态; `--emit-arg` 存在 ⇒ stdout / 否则 E6 手工判, 模板行归母 Impact | CR 接缝 C1 / TL C4+C5 |
| §2 触发时机 / rule6 #8 / Impact branch-manager | 撤回 `Part A1`→`Part B1` 改名 (部件名非 Phase A.1) | CR M1 |
| §2.1 spec-slug 行 + §6 新行 | `derive_track_id` >64 或非 ASCII ⇒ 整串 sha256 回落; slug 过长已知限 | TL M1 |
| §2.2 引文出处 / basicConfig | `phase1_gate.py:1047-1049` + `coordination_probe.py:18-21`; basicConfig 范围限定 | CR M6 / KM 母 M1 / CR m6 |
| §2.3 `active` 档 | 「我去释放对方 claim」改为人工协作动作 + 无命令声明; 并轨语义 | TL M3 |
| §2.4b 四态表第 1 行 | 键缺席 = 未传 `--linked-issue` (与 `--include-terminal` 正交) | TL M2 |
| §2.5 | Level 1 例外 bullet | CR 母 C1 |
| §5.2 | 枚举方向机制 (overlap 不按 container 过滤); 新增「并轨」「复用对方产出」两行 | TL M3 / M4 |
| §6 首行 | 四态措辞 | CR 接缝 C1 |
| D4 / D17 | D4 引用锚点; D17 重写 (适用范围 + 围栏边界规则 + 引用者须声明落了哪几件) | CR m6 / TL 字段 M9 / CR m1 |
| rule6_note | 12 hunk (新增 #12 `:168` 键集描述性档); #8 撤回改名; #10 加存在断言; (a) 加 Level 1/enabled 零调用 + 两阶段取值 | CR m5 / M1 / TL M8 / 母 C1 |
| SC 表 | SC-9 两臂; SC-11 措辞; SC-12 场景改写 + 第二臂; SC-14(a)/SC-23 改 baseline 即绿守卫; SC-15 负控夹具前缀; **SC-22 ①–⑦** (⑤ 切片外、⑦ 完整命令行含续行折叠、标题落点钉死); SC-32 坏实现 1; **新增 SC-34** (三处占位串文本层) | 五席 |
| 非目标 | 争点句改「主要」+ 两处描述性勘正; argparse 第二处限定 | CR m4 / TL C3 |
| Impact | phase1_gate 第一处「零改动」限定 + 六处; 第二处 **⑦** `--raw-track-id` 条件必需 (钉死落法 (a)); tests 行 + SC-34; phase-a-planner 行 (标题落点 / 七字面量 / `:67`); branch-manager 行撤回改名; schema 行号; follow-up 第 7 行 (swept 标记) | BA M1 / TL C3 / CR M4 / M7 / m6 |
| editlist / 未做 / 闸门状态 | FIX-04 自指 / FIX-19 真 token / 未做 #2 `:67` / 未做 #6 升格 / 新表面标题标「R6 已审」/ 闸门 item 5-6 (R6 结果 + 2 项新待裁) / 流程判断表 #7 #8 | CR m6 / TL M5 / 主控 |
