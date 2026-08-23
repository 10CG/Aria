---
checkpoint: post_spec
round: 2
converged: false
overridden_by_user: false
incomplete: false
verdict: REVISE
---

# post_spec R2 — a1-entry-claim-duplicate-work-guard (重写版 v2 + R1-fix + C1/C2 裁定落版 + 3 轮 rework)

> **席位**: 5/5 · **4 REVISE + 1 PASS_WITH_WARNINGS** · `scope_ok` 5/5 true
> **counts (各席)**: TL 1C/10M/6m · BA 0C/3M/1m · QA 0C/12M/6m · CR 1C/15M/10m · KM 2C/6M/1m
> **timestamp**: 1787481000000 · 审计对象: 主仓工作树 proposal.md (基线 `1205ec3` + rework r1–r3, 未提交) · aria 子模块 `a0fe720` (v1.66.5)
> **编排**: 动态工作流 (5 席并行, 各自实读源码; 报告 `post_spec-R2-1787481000000-a1-entry-claim-rewrite-{role}.md`)
> **R1 基线**: `post_spec-R1-1785710000000-…-aggregated.md` — 5 critical 簇 / 17 major 簇

## 判定

**REVISE, 未收敛。** 去重后 **3 个 critical 簇 + 17 个 major 簇**; major 簇数与 R1 持平 (17 → 17), critical 从 5 降到 3 但其中 2 簇是 R1 遗留、1 簇新发现。

### 🔑 本轮的形状 (CR 独立指出, 主控按 editlist 复核属实)

**Spec 三处自述「R1-fix 已全量吸收」, 实际 R1 聚合的 10 个 major 簇有 9 条未动** (`post_spec-R1-fix-editlist-a1-entry-claim.md` 的 FIX-03/06/07/08/10/12/13/14/15/16/17/19 均未落)。本轮 rework 只处理了 C1/C2 裁定落版 + 两轮核验席 findings, 没有回到 R1 editlist。⇒ R2 的 major 里**约 2/3 是 R1 still-open**, 不是本版新造; 但「自述已吸收」本身是 R2-CR-M4 (self-description-accuracy), 与 memory `past-summary≠measurement` 同形。

## Critical 簇 (3)

| # | 簇 | 席位 | 状态 | 要点 |
|---|---|---|---|---|
| C-A | §1 承重「抽取规则」defer 到 A.2 ⇒ check 上线恒红 | TL-C1 · CR-C1 · QA-C3 | **R1/C3 still-open** | Spec 自给候选正则实测只救 4/13 语料 (TL 放宽规则可达 12/13); §1.2「单一形态」与 §1.3「抽出 token」未调和; check 作用域 / 无 issue / 多 issue 未定义 |
| C-B | track-id 无方向区分符 ⇒ 探索性放弃一个方向, `release_claim_by_track` 连坐释放同 (container, track) 全部 claim | KM-C1 · QA-M2 · CR R1-M2 | **R1/M2 still-open** (升 critical) | §2.1 track-id = basename-number-container_uuid, 不含 spec-slug; §5「探索性放弃必 release」与之直接冲突 |
| C-C | A.1 track-id (含 container_uuid) 与 Phase B / D.2b 既有 carry-id (不含容器段; phase-b-developer:92 / branch-manager:149 / phase-d-closer:52,55) 不一致 ⇒ happy path 走完循环时 B-entry 认领与 D.2b 释放找不到 A.1 的 claim | KM-C2 | **新** | 三处宿主独立复读确认; 这是比 C-B 更早发作的断链 |

## Major 簇 (17; 标 ★ = R1 still-open)

| # | 簇 | 席位 |
|---|---|---|
| M-1 ★ | §4 探针「同 issue」匹配谓词全文未定义 (前置 Spec 已 ship `normalize_linked_issue()` 可直接钉) | TL-M4 · QA-M3 · CR |
| M-2 ★ | `standards/openspec/templates/proposal-minimal.md` (跨项目 SOT) 未入 Impact; 机械回声只覆盖 Aria 仓 | TL-M6 · BA-M3 · QA-M4 · KM-M4 · CR |
| M-3 ★ | §6 缺口表缺 NEW-01「无字段」行; `phase1_gate.py:1230 if args.linked_issue:` 门控 (键缺失而非空列表) 全文零提及 | TL-M7 · QA-M5 · CR |
| M-4 ★ | `phase1_gate.py:1236-1238 except → out["linked_issue_overlap"]=[]` 零证据当正证据, 在 out 层不受 `GateResult.error` 覆盖; SC-10 可绿病仍在 | TL-M8 · QA-M6 · KM-M5 · CR |
| M-5 ★ | §4「各自默认分支」取法未定义 (本仓 `github` remote 无 symbolic-ref 复现); 只扫默认分支 ⇒ in-flight 竞品结构性不可见, 盲区声明未勘正 | BA-M2 · QA-M7 · KM-M6 · CR |
| M-6 | rule6_note: audit-engine 列「覆盖外」档但点名行为 (a)(b)(c) 无一是 audit-engine 的; `ab-suite/audit-engine.json` 不存在 ⇒ 按判据表「缺一照跑」该档不成立; SC-9 作描述性 substitute 无效 (断言对象是 SKILL.md 散文) | TL-M9 · TL-M10 · BA-M1 · QA-F2 |
| M-7 | (ii) 落版把 heartbeat 写成「无条件每次 /state-scanner 必跑」⇒ 只读型命令每次写 claim + 推远端, 绕过 `coordination.enabled`; §2.5 的 opt-out 条款未下移 | TL-M2 · CR-M2 |
| M-8 | (iii) STALE_TTL→24h 漏第三消费者 `track_board::_freshness_status` (行为面) / `_takeover_eligible`; 抹掉 constants.py:40-42 两级顺序; 残余风险分析单向 | TL-M1 · CR-M3 · QA-M1 |
| M-9 | §2.4 `_TERMINAL` 事实订正未同步 SC-8; `unknown` 哨兵 `linked_issue=None` 被第二道过滤丢弃 ⇒ 「按未能核实呈现」结构性不可达 | TL-M3 · CR-M5 · KM-M2 |
| M-10 | §1.3 custom check 无实现宿主 (既有 check 都指向 scripts/*.py 或 .aria/probes/*.py); SC-13 零验证宿主 | TL-M5 · QA-F4 |
| M-11 ★ | §3 双落点 (phase-a-planner + spec-drafter) 是核心杠杆, SC 全表零覆盖; 两落点同时命中的幂等分工未定义 | QA-F1 · CR |
| M-12 | `--heartbeat-only`「只刷本容器本 track」的 track 来源未定义; claim 按 (container, session) 键控, 跨 subprocess 不可判定 | CR-M1 |
| M-13 | Spec 自述「R1-fix 已全量吸收」不实 (editlist 12 项未落) | CR-M4 |
| M-14 | Impact 零覆盖 `session-handoff.md` (track_id.py 自称 SOT) 与 `coordination-ref-schema.md` (claim 结构 SOT) | KM-M1 |
| M-15 ★ | §2.3「起草前经 AskUserQuestion 请裁」与 Layer 2 无人值守 (AD10 唯一人类参与点在 S7) 冲突, 无 unattended 降级路径 | KM-M3 · CR |
| M-16 ★ | SC-9/SC-14 标「代码」实测对象是 SKILL.md 散文; SC-8/SC-10 把 CLI 可验字段与消费层措辞捆在一条断言 | QA-F2/F3 · CR |
| M-17 ★ | §2.1 拼接无代码落点 (SC-1/SC-4 无被测对象); §2.2「改」匹配键 × Impact「增并存变体」两读; 终态可见后 §2.3 选项集未随动; §4 无 stdout 契约; `coordination.enabled` 未在 DEFAULTS.json 注册 | CR (合簇) |

## 收敛判定 (convergence 模式, max_rounds=4)

- R1 → R2: critical 5 → 3 簇 (2 still-open + 1 新); major 17 → 17 簇 (≈11 still-open + 6 新, 其中 4 条由本轮 C1/C2 落版引入: M-7 / M-8 / M-12 / M-6 的 audit-engine 部分)。
- **未收敛**; 且 major 数**持平**而非下降 — memory `stop-adding-rounds-when-major-count-flattens` 的判据命中: 每轮 fix 引入 ≈ 等量同形缺陷 (本轮 4/6 新 major 来自落版文字自身)。
- 本轮另有一项**上呈 owner 的复议** (§2.2「⚠️ 实读订正 · 请 owner 复议」): C2 (iii) 的理据「STALE_TTL→24h 使漏跑扫描不暴露在 --sweep-stale 下」经实读证伪 (`gc.py:341` sweep 默认 `SWEEP_TTL`=24h, 与 STALE_TTL 无关); 是否维持 (iii) 待 owner。

## 主控处置建议 (非裁定, Rule #10 留痕)

按 config `max_rounds=4` 字面还可 R3/R4; 但 major 持平 + R1-fix 未真落 + 3 critical 中 2 个是结构性 (C-B/C-C 涉 track-id 形态, 牵动 Phase B/D 既有 carry-id 契约) ⇒ **建议 owner 先裁方向再决定是否加轮**: (1) R1 editlist + R2 三 critical 由**换人执笔**一次性处理后再 R3 (memory fix-writer-bottleneck); (2) 缩 scope — §4 探针 (M-1/M-5 两簇) 与 §1 抽取规则 (C-A) 各自独立成小 Spec, 主机制只留 A.1 认领 + track-id 契约 (C-B/C-C); (3) 维持/撤销 (iii)。**AI 不自行选。**
