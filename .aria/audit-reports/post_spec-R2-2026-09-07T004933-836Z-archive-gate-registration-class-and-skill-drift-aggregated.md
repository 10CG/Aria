---
checkpoint: post_spec
round: 2
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 4C/14M/7m (四席原始 25 条; 反驳席推翻 3, 另报约 19 条含 6 Major)
clusters: 4C
teams: [aria:backend-architect, aria:code-reviewer, aria:qa-engineer, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T00:49:33.840Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: true
max_rounds: 5
rounds_total: 2
---

# post_spec R2 — archive-gate-registration-class-and-skill-drift (aggregated)

## ⚠️ degraded=true 的原因 (诚实登记)

计划 5 席, **第 5 席 (FACT 引用与数字核验, aria:tech-lead) 在启动 13 分钟后停止输出, 静默 41 分钟后由主控 TaskStop 终止**。
其余 4 席 + 4 反驳席全部完成。终止判据: (a) 已取得 4 席实质结论且反驳席全部完成; (b) 缺的 FACT 镜头
正是主控全程在做的事 —— proposal 里几乎每个数字主控都独立复核过 (R1 报告与本报告的每条实测均有命令与输出)。
**这不是「跑满了」, 是「跑了 4/5 并说明为什么停」。**

## Round 2

- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (`no_sibling_found`, own_key = `aria-plugin#186`; github 154 / origin 158)
- **镜头设计依据** memory `rewrite≠cleanup` (结构重写后 86% finding 落在当轮新文本): 实现者试派生 / R1 修复验证 / 定稿谓词拒绝能力 / 新文本引用核验 (未完成) / 治理面
- **收敛趋势**: R1 存活 8 Major + 1 Critical(被假推翻) → R2 **约 14 Major + 4 Critical**。
  按 memory `stop-adding-rounds` (加轮判据是 major 数是否还在降): **不收敛, 在涨**。

### 逐席 verdict

| 席 | verdict | 原始条数 |
|---|---|---|
| aria:backend-architect (实现者试派生) | PASS_WITH_WARNINGS | 6 (5M/1m) |
| aria:code-reviewer (R1 修复验证) | **FAIL** | 12 (1C/7M/4m) |
| aria:qa-engineer (定稿谓词拒绝能力) | **FAIL** | 4 (2C/1M/1m) |
| aria:knowledge-manager (治理面) | **FAIL** | 3 (1C/1M/1m) |
| aria:tech-lead (新文本引用核验) | — | **未完成 (卡住已终止)** |

## 四条 Critical — 主控逐条独立复核结果

| id | 内容 | 主控复核 |
|---|---|---|
| **GOV-1 / R1V-3** | 删除 Rule #6 跨 Skill 上呈项所依据的「两次先例」证据链有假 | **成立。** `aria/CHANGELOG.md` 逐字: v1.71.1「纯代码, **零 SKILL.md / description 变更**」= 单 Skill, **不是**跨 Skill 先例; 只有 v1.69.1 是。按 memory `exact-exception-condition`「N 次非正式援引 ≠ 成文 lane」, **一次先例不构成 Rule #10 豁免白名单里的 lane** ⇒ **上呈项已恢复** |
| **PRED-1** | 包段锚取 `definition_paths` 全集并集, 迁移类交付物让已不存在的旧包名也获锚定资格 | **成立。** 实测 `-m old_pkg.tick_runner` → True |
| **PRED-2** | 包段锚只比 basename, 落在 `scripts/` 等通用目录时名存实亡 | **成立。** 实测 `-m scripts.coordination_probe` → True。修法 V4 (包段目录须含 `__init__.py`) 实测判别力: `aria_layer1/` 有, `state-scanner/scripts/` 没有 |
| **R1V-1** | Part B「类级补齐」再次漏类 | **成立且比它说的更多。** 加宽 grep 实跑: 漏的是 `SKILL.md:17` (「修复 CLI 归档位置 bug」—— **逃出了 SC-4 自己的 grep 模式**) + `phase-d-closer/SKILL.md:41` (跨 Skill)。类规模从 5 → 12 → **20 行跨三个 Skill** |
| **PRED-refuter MISS-1** | SC-1 在生产调用链上不可满足 | **成立, 且是本轮最重的一条** — 见下 |

## 决定性测量: Part A 的生产触达为 0

主控沿生产链实测 (不再自传 `definition_paths`, 走 `extract_claim_symbols`):

| 测量 | 结果 |
|---|---|
| 7 个活跃 spec 抽出的符号 | **0 个** (C 分级闸对它们根本不启动) |
| 最近 59 个 spec (含归档) 抽出的符号 | 18 个 |
| 其中 `definition_paths` 为空 | 0 个 |
| 其中父目录是**真 Python 包** (谓词唯一能锚定的形态) | **0 / 18** |
| 全仓 `-m <点分路径>` 命中分布 | 20 处**全在** `aria-orchestrator/hermes-extensions/aria-layer1/` |
| 有 spec 声称过该包里的符号吗 | **没有** |

⇒ Part A 会带着全绿测试 ship 而生产触达为 0 (memory `completion_signals_vs_runtime_invocation`)。
次生问题: 断言语料住在 `aria-orchestrator` (aria-plugin 的非分发仓), 测试却要住在 aria-plugin ⇒ 跨子模块依赖对采用方不成立。

## 处置: owner 裁定拆分 (2026-09-07)

- **Part A → `10CG/aria-plugin#188`** —— V4 设计 + 三处接入 + 21 个对抗用例 + 基线三态 + 零触达测量全部随迁, 可直接实施。
- **本 Spec 收缩为** openspec-archive 漂移类级收口 (20 行跨三个 Skill) + 两个机械兜底 + 九条开单 + 发版。proposal 275 → **227 行**。
- 拆分不制造接缝: 余下部分对 Part A **零实现/零引用/零导出依赖** (原声称的「共用 `spec_complete.py`」已在 R1 被证伪)。
- **顺手修** `10CG/aria-plugin#187` 的最小止血: `phase-d-closer/tests/conftest.py`, 使该套件从 `OK (0 tests)` 变 `OK (11 tests)`, 全套件 2111 → **2122**。那 11 个测试含一条**从未跑过**的 Rule #7 凭证不泄漏守卫。

## R2 其余 Major 的处置 (已并入 227 行修订版)

R1V-2 (C2 强制调用仍在失效通道) → **诚实登记不假装解决, 开 D9** · R1V-6 (SC-7 的 AB 可预测零区分) → **照跑但 RESULT.md 须显式记录零区分力** ·
R1V-7 (C1 锚点唯一性依赖 `:318` 而 B2 正要改它) → **B2 新文案硬约束不得以「填入」结尾 + 落地后重跑锚点唯一性** ·
R1V-8 (issue 号仓限定被自己违反 7 次) → **头部消歧段 + 全文带仓限定** · GOV-2 (漏改 CHANGELOG/README) → **已核: 架构文档零命中, README 名册在册, 只需 skill CHANGELOG** ·
ID-3 (Step 5 落地形态未定 + 漏 `:394`) → **B8/B10 已钉死** · ID-5/MISS-4 (SC-4 区段 (ii) 无机械锚) → **锚定 `## 变更历史` (`:627`), 且本版初稿写的「## 版本历史」经实测不存在已订正** ·
MISS-5 (SC-9 写「三仓」找不到第三个) → **改两仓**。

## 主控自查: 本轮我自己犯的两个错

1. **直接采信了 subagent 的先例声称而未核**。R1 的 KM-refuter 报「已有两次 shipped 先例」, 我据此**删掉了一个上呈 owner 的项**, 没去 CHANGELOG 逐字核。核了才发现其中一条根本不是那个形状。同 memory `delegate-verify` 形状; 危害方向最坏 —— 它让我**少问了 owner 一个本该问的问题**。
2. **SC-1 的区段锚点名手写未核**。写「`## 版本历史`」, 实测该标题不存在 (真名 `## 变更历史`), 解析器返回 None 会让 `:632` 误落区段外。**第一版机械判据自己就是坏的** —— 同 memory `check-runs-at-baseline-first`。
