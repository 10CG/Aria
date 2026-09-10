---
checkpoint: post_spec
round: 4
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 2C/4M/0m (三席原始 12 条; 反驳席推翻 1)
clusters: 2C
teams: [aria:code-reviewer, aria:backend-architect, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T04:07:01.132Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 4
---

# post_spec R4 — archive-gate-registration-class-and-skill-drift (聚焦核验轮)

## 本轮定位

R4 **不是全量重审**: 只核验 R3 的 19 条修复是否落地 + 只报**新的** Critical/Major。3 席 + 3 反驳席, 全部完成。

- **Sibling probe**: `no_sibling_found` (github 154 / origin 158)

### 逐席 verdict

| 席 | verdict | 结论摘要 |
|---|---|---|
| aria:code-reviewer (R3 修复核验) | PASS_WITH_WARNINGS | 19 条 **14 条修对 / 5 条没到位**; **0 Critical**; 「修完 5 条后复跑本轮 6 条测量即可, 不必开 R5」 |
| aria:backend-architect (实现者试派生) | **FAIL** | 2C + 1M; 但「缺口很小…**不需要再开一轮结构审计**」 |
| aria:knowledge-manager (治理面终检) | PASS_WITH_WARNINGS | 3M (全为本轮新发现); 「**可进 Phase A.2**, 三条应在进 Phase B 前处理」 |

### 收敛趋势 (四轮)

| 轮 | Critical | Major | 问题性质 |
|---|---|---|---|
| R1 | 1 | 8 | 设计缺陷 (谓词假 alive / 类级漏枚举 / 无代码宿主) |
| R2 | 4 | ~14 | 设计缺陷 + **价值证伪** (Part A 生产触达实测 0 ⇒ 拆分) |
| R3 | 1 | 11 | 文档一致性 + 自宣已核未实证 |
| **R4** | **2** | **4** | **全部落在 R3 新写的验收判据文本上; 无一需要动结构** |

## 两条 Critical — 都是主控自己写的机械判据坏掉

| id | 内容 | 复核 |
|---|---|---|
| **R4-M1** | 头部「机械自检」落地的是**主控自己在 R3 报告里判过无效的裸 grep**。按其逐字跑得 **9** (要求 0), 且声称的负控「R3 修订前实测为 3」用同一命令跑得 **10** | **成立, 逐字复现。** 那个「3」来自 scratchpad 里三态验证过的 Python 实现, 而**写进 Spec 的是坏的那个** —— memory `pasted-evidence-is-derived` (贴进文档的脚本是派生物, 不能手抄)。已改为**只引脚本路径不复述命令**, 并把该脚本立为 **Part C3** 真落盘 |
| **R4-2** | SC-3 的「示例 1 四行逐行 diff 对目标文本精确匹配」—— **那四行的目标文本全文从未给出**, 判据不可执行 | **成立。** 已补四行完整字面 |

## R4 抓到的三组 `fixes-contradict` (逐条修法都对, 但互相违反隐含前提)

1. **IMPL-7 制造了 RFV-5 的命中**: B15 的「目标行完整字面」含 `#95`, 直接给裸 issue 号检查添了一处命中 ⇒ 检查必须排除 code span。
2. **Level 行 vs Rule #6 表**: Level 行写「两个 SKILL.md 的**指令面**变更」, 而 Rule #6 表把 phase-d-closer 判进第一行 (须为**非**指令语义变更)。两处说法相反 ⇒ Level 行已改为「openspec-archive 指令面 + phase-d-closer 与 README 的**描述性**事实同步」。
3. **B8 vs SC-3 行数**: B8 把 Step 5 压进标题行本身 (其下无正文), 而 R3 新写的 SC-3 要求「之间非空正文**恰 1 行**」⇒ 同一目标文本上两者判定相反。SC-3 已改为**恰 0 行**。

## 其余四条 Major

- **GOV-ADVISORY-NOT-BLOCKING**: 把 Rule #6 跨 Skill 上呈项降为「advisory 不阻塞」本身是**一种新形态的自行豁免** —— 不在 `configured-gate-authority.md` 白名单四类内, 也没套用 SOT §2 末行「拿不准 ⇒ 照跑」的默认。⇒ **已新增 SC-11, 该项改为阻塞 C.2 合并。**
- **PARTE-VERSION-CHECK-COVERAGE-GAP**: 逐个读六个版本类 custom check 的源码, 它们合计只覆盖 **23 处版本点里的约 6 处**; 至少 17 处 (**含全部 7 处 aria 子模块点位**) 无任何机械覆盖。⇒ Part E 已加覆盖面诚实登记 + 要求逐文件 `grep -c` 实测并贴进 tasks.md。
- **SC-9 gitlink 断言基线恒绿**: 上一版写 `git ls-tree HEAD aria` == `git -C aria rev-parse origin/master` —— 两者天然相等 (`301641b`), 与基线表登记的「红」互斥。⇒ 改为比 `git -C aria rev-parse HEAD`, 基线实测 `301641b` vs `3a28339` = **红** ✅。
- **B8 Step 4 三断言无字面** ⇒ 已补。

## R4 修复后的六条终验 (FIXV 席指定的复跑项, 全过)

| # | 项 | 结果 |
|---|---|---|
| 1 | `10CG/aria-plugin#189` 存在 | ✅ open |
| 2 | C1 探针第三条断言 (revert 夹具须 rc 1) | ✅ rc 1 |
| 3 | SC-1 四文件区段外基线 | ✅ **15** |
| 4 | B4 候选文案对 SC-1 pattern 零命中 | ✅ 0 |
| 5 | 头部机械自检 (正确实现) | ✅ rc 0 |
| 6 | SC-9 gitlink 断言基线红 | ✅ `301641b` ≠ `3a28339` |

## ⚠️ 关于是否开 R5 —— 主控按 Rule #10 而非性价比裁

三席**一致建议不必开 R5** (FIXV 逐字: 「再开一轮边际产出为负」, 引 memory `marginal-return-negative`)。

**主控不采纳该建议**, 理由:
- Rule #10 / `configured-gate-authority.md` 明写: 不得以「**性价比** / session 已长」等价值评估跳过、降级或改序已启用闸门。「边际产出为负」正是性价比判断。
- 审计席是**顾问**, 不是闸门的权威; config `max_rounds: 5` 未用满, 收敛判据 (四元组稳定 + **全票 PASS**) 亦未达成 —— 本轮仍有一席判 FAIL。
- 本轮两条 Critical 恰恰证明「看起来快收敛了」时最容易漏: 它们都是**主控自己写的机械判据坏掉**, 而前三轮无一席发现。

⇒ **R5 照开**, 定位为收敛确认轮 (验 R4 的 9 处修复 + 只报新 Critical/Major)。
