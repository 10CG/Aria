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
