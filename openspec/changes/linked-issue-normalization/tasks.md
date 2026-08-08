# Tasks — `linked-issue-normalization`

> **Status**: 📝 Draft (A.2 未跑 —— 本文件由 R3′ 的 C1 手术创建, 目的是给 Q5 裁定的 AB 任务一个落地载体)
> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)
>
> **为什么本 Spec 从 Level 2 升 Level 3**: Q5 裁定 (owner 2026-08-06) 要求 `SKILL.md:176` 的 hunk **照跑 AB, 不走 substitute**, 并写明「本条须进 `tasks.md` 作为独立任务」。而本 Spec 当时是 Level 2 (按 CLAUDE.md 只产出 `proposal.md`) ⇒ **owner 亲裁的 Rule #6 处置唯一落地载体不存在** (R3′ 两席独立命中)。本文件解决它。

---

## Phase B — 实施

| # | 任务 | 落点 | 验收 |
|---|---|---|---|
| B-1 | 实现归一比较谓词 (§归一规则 五步) | `lib/collision.py::linked_issue_overlaps` | SC-1 / 1b / 2 / 3 / 4 / 5 / 5b / 5c / 6 / 6b / 10 / 11 / 13 / 14 / 15 全绿 |
| B-2 | 导出纯函数 `normalize_linked_issue(value) -> tuple[str,int] \| None` | `lib/collision.py` | **SC-12** (返回契约: 三类不可解析各返回 `None`) |
| B-3 | 回显字段冻结 | 不改 `collision.py:228` | **SC-9** —— ⚠️ 它是 D2 极性论证的**唯一**守护, 见 SC 表内说明 |
| B-4 | docstring 同步 ×2 | `collision.py:182-206` · `claim_schema.py:107-114` | 措辞不得暗示「已穷尽核实」; 走 **substitute** |
| B-5 | **`SKILL.md:176` 括注同步 + 照跑 AB** | `skills/state-scanner/SKILL.md:176` | ⛔ **必须用 `/skill-creator` 跑 AB, 不申请豁免、不走 substitute** (Q5 裁定)。**时点: 实施该 hunk 之后、发版之前** |
| B-6 | 测试落盘 | `tests/test_release_by_track.py` | 新增子用例 **≥45** (逐项推导见 proposal §Impact); 既有 6 条逐字不改; 全量 `run_all_tests.sh` 绿 |

## Phase C/D — 发版

| # | 任务 | 说明 |
|---|---|---|
| C-1 | 发版同步面 **5 项** | aria 子模块 5 文件 + 主仓 gitlink + 主仓 `VERSION` + root README badge + i18n README 的 `translated-from` 标记 (#140 B 档)。**后两项由 enabled custom check 守着** (`m6-version-badge-match` / `i18n-readme-translation-currency`) |
| C-2 | 版本 | v1.66.0 **MINOR** (行为面扩大) |

---

## ⚠️ Phase B 开工前必读 — 三条已知限 (不修, 成文)

按 R3′ 的结构性教训, 以下三条**已知洞不修** —— 修它们会按同一规律再生成一批缺陷。Phase B 实施者知道它们的存在即可, **不要在本 Spec 内解决**:

| 工具 | 已知洞 | 影响 |
|---|---|---|
| `.aria/repro/spec-consistency-check.py` | C1/C3/C4 + C2 后半有与 C8 相同的**空真洞** (表格格式漂移后输出「✅ SC 表 0 条」而非报错); C6 名为「核验行号指向」实为**语法黑名单**, 对自指行号失明 | 它的「8/8 通过」**不等于**机械同步已清零。当作辅助, 不当作闸门 |
| `.aria/repro/mutation-sweep-*.py` | 「11 个维度」只枚举 `normalize()` **函数内部**旗标; 规则 4 回落分支、`org` 处理、`int` 十进制比较、空 basename 判定**未参数化** (实测这 4 个都已被现有 SC 杀死, 不是覆盖洞, 但「枚举完」的措辞不成立) | 它的 exit 0 **不等于**穷尽。新增归一逻辑时须手工判断是否引入新维度 |
| 同上 · `UNOBSERVABLE` 字典 | 两条「行为不可观测」条款 (规则 1 对 `left` 的 strip · D7 的 4300 位上界) 是**硬编码 fail-OPEN 豁免**, 且其支撑实证 (「47,211 候选串零差异」) **在仓里无可执行产物** —— 结论经三席各自独立复现 (100,633 / 44,069+273,430 对) **为真**, 但留证方式不可复核 | 若归一流程改动使这两维变得可观测而无 SC 杀它, 脚本仍会打绿 |

**⇒ 三件工具的定位是「便宜的辅助」, 不是「机械闸门」。** 唯一可当作证据的是 `sc-baseline-*.py` (三重 fail-closed, 三轮中唯一没被找到问题的)。

---

## ✅ 与母 Spec 的接缝 — 已关闭 (owner 裁定 2026-08-08)

母 Spec `a1-entry-claim-duplicate-work-guard:172` 逐字请求「在前置 Spec 的非目标处加一句『`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面』」并标注「**该协调项须 owner 确认**」。

**owner 2026-08-08 同意, 该句已落 [proposal.md §非目标](./proposal.md)。** ⇒ D6/§接口面 的「签名不变」自此限定于本 Spec 变更面; 母 Spec 追加 keyword-only 形参不视为违反、不构成回归。

*(R2′ 曾把它记为「随 Q6 消失」—— 那只消掉了测试层冲突; R3′/tech-lead M7 指出协调项本体一处未动。至此关闭。)*
