# Tasks — `linked-issue-normalization`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)
> **Level**: 3 | **Status**: ✅ **A.2 + A.3 complete** (2026-08-08) — 细粒度任务 + agent 分配见 [detailed-tasks.yaml](./detailed-tasks.yaml); 待 post_planning 闸门
> **Scope**: 单域 — `aria/skills/state-scanner/` (`lib/collision.py` 一个比较谓词 + 一个导出单元)
> **ship target**: aria-plugin **v1.66.0** (MINOR — 行为面扩大)

> **为什么本 Spec 从 Level 2 升 Level 3**: Q5 裁定 (owner 2026-08-06) 要求 `SKILL.md:176` 的 hunk **照跑 AB, 不走 substitute**, 并写明「本条须进 `tasks.md` 作为独立任务」。而本 Spec 当时是 Level 2 (按 CLAUDE.md 只产出 `proposal.md`) ⇒ **owner 亲裁的 Rule #6 处置唯一落地载体不存在** (R3′ 两席独立命中)。本文件解决它 —— 见 **4.1**。

> **📌 本文件 2026-08-08 由 A.2 重写为 OpenSpec 标准 checkbox 形态。** 前一版是 R3′ 的 C1 手术产物 (`B-1..B-6` / `C-1..C-2` **表格**), 非 A.2 产出。**编号不可变约束不受影响** —— 前一版的 `B-n` 从未被任何 `detailed-tasks.yaml` 的 `parent` 引用 (该文件此前不存在), 故无引用关系被破坏。
>
> **顺带修掉一个机械盲区**: 前一版用表格而非 `- [ ]`, 导致 `handoff_autofill` 的 unfinished 扫描**完全看不见本 Spec** (2026-08-08 handoff §2 实证: 159 条 unfinished 里本 Spec 零条)。本版恢复 checkbox 后该盲区对本 Spec 消失。**该 backstop 对非 checkbox 形态 tasks 的失明本身仍是插件侧待修项**, 不在本 Spec 范围。

---

## Task Group Overview

| Group | 主题 | 依据 |
|-------|------|------|
| **1** | 测试先行 (RED) — 17 条 SC 全量落盘 | proposal §Success Criteria |
| **2** | 实现 (GREEN) — 归一谓词 + 导出单元 + 守卫 | proposal §What Changes 五步 · D7 · D9 |
| **3** | 文档同步 ×3 (两处 substitute + 一处 AB) | proposal §Impact · rule6_note 逐 hunk 表 |
| **4** | Rule #6 AB (⛔ 不豁免) | Q5 裁定 (owner 2026-08-06) |
| **5** | 回归 + 发版同步面 | proposal §Impact 发版同步面行 |

**排序依据**: 组 1 → 组 2 是 RED-first (SC 的 baseline-failing 状态已于 A.1 实跑留证, 见 proposal baseline 表 —— 组 1 落盘后应立即复现那 8 条红)。组 3 可与组 2 并行 (不同文件), 但 **3.3 必须在 4.1 之前** (AB 测的是该 hunk 的行为影响)。组 5 gate 在组 1–4 全绿之后。

---

## 1. 测试先行 (RED) — `tests/test_release_by_track.py`

> 宿主为既有文件; **既有 6 条 (`:206-247` 4 条 + `:527-575` 2 条) 逐字不改**, 回归由全量套件承担。
> 每项括注为该项贡献的**子用例下界**, 全组加总 = **45**, 与 proposal §Impact 的逐条推导独立吻合 (两处任一变动须同批重算)。

- [ ] 1.1 SC-1 / SC-1b / SC-2 / SC-3 / SC-4 — 跨族两两配对 + 三个切分点各自 strip + 不同仓负控 + org 不参与 + int 十进制比较 **(13)**
- [ ] 1.2 SC-5 / SC-5b / SC-5c — basename 轴三态: 截断型**不**归一 (已知限) / 分隔符型 `./_→-` 归一 / 段内空格**不**译码 **(5)**
- [ ] 1.3 SC-6 / SC-6b / SC-10 — 不可解析值退回原串精确比较 + `number_str` 边界五类 + **一条畸形毒不死整批** **(15)**
- [ ] 1.4 SC-11 / SC-13 / SC-15 / SC-14 — 切分方向双轴 (`#` 取最后 / `/` 取最后) + `casefold` 维度 + `number` 相等这一必要条件 **(8)**
- [ ] 1.5 SC-9 — 命中条目回显**未归一原始串** **(1)**
- [ ] 1.6 SC-12 — 导出单元返回契约: 可解析返回 `(basename, number)`, 三类不可解析各返回 `None` **(3)**

## 2. 实现 (GREEN) — `lib/collision.py`

- [ ] 2.1 导出纯函数 `normalize_linked_issue(value: str) -> tuple[str, int] | None` — §归一规则五步; `None` 与规则 4 的不可解析枚举一一对应 (D9)
- [ ] 2.2 `linked_issue_overlaps` 内部比较谓词切换为归一键 `(normalize(basename), int(number))` — **签名与返回 schema 不变** (D6)
- [ ] 2.3 解析守卫与异常隔离 — 不含 `#` 先判不可解析 (不得无守卫拆分) · `int()` 必包 `try/except ValueError` · `limit = sys.get_int_max_str_digits()` 且**仅当 `limit > 0`** 时比长度 (D7)

## 3. 文档同步

- [ ] 3.1 `lib/collision.py` docstring `:182-206` — 说明按归一后 `<repo>#<n>` 比较、org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** (走 substitute)
- [ ] 3.2 `lib/claim_schema.py:107-114` — `ClaimRecord.linked_issue` 字段文档两处失准同批修 (SAME → same normalized key; active → 实际跳 `_TERMINAL` 且不含 `yielded`) (走 substitute)
- [ ] 3.3 `skills/state-scanner/SKILL.md:176` 括注 — 补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」

## 4. Rule #6 AB (⛔ 不申请豁免、不走 substitute)

- [ ] 4.1 用 `/skill-creator` 对 **3.3 的 hunk** 照跑 AB — 时点: **3.3 实施之后、发版之前**; 依据 Q5 裁定 + `skill-benchmark-exemption.md §4`「决策表之外不得自创理由, 落『拿不准』格默认照跑」

## 5. 回归与发版

- [ ] 5.1 全量回归 — state-scanner 基线 **1322** tests + 本 change 新增 **≥45**; 跨 skill `run_all_tests.sh` 全绿
- [ ] 5.2 aria 子模块 **5 文件** bump 到 **v1.66.0** — `plugin.json` (版本 SOT) / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`
- [ ] 5.3 主仓同步面 **3 项** — `gitlink` + `VERSION` 的子模块版本表行 + root `README.md` 的 Plugin badge (后者由 enabled check `m6-version-badge-match` 守着)
- [ ] 5.4 `README.{zh,ja,ko}.md` 的 `translated-from` 标记 ×3 — #140 B 档: 正文无实质变更时**只更标记不重译**; 由 enabled check `i18n-readme-translation-currency` 守着 (**任何** bump 都会让三份判 STALE)

> **⚠️ 5.2–5.4 合计 9 处落点**, 原 proposal 早期版本写「5 文件 + gitlink」会漏 3 处并触发两条 **enabled** custom check (R1′/tech-lead-M5 展开)。**收尾时必须跑不带路径的 `git status` 核验实际落地面** (memory `feedback_scoped_git_add_splits_claim_from_landing` —— 该形状在本项目一天内两次实证)。

---

## ⚠️ Phase B 开工前必读 — 三条已知限 (不修, 成文)

按 R3′ 的结构性教训, 以下三条**已知洞不修** —— 修它们会按同一规律再生成一批缺陷。Phase B 实施者知道它们的存在即可, **不要在本 Spec 内解决**:

| 工具 | 已知洞 | 影响 |
|---|---|---|
| `.aria/repro/spec-consistency-check.py` | C1/C3/C4 + C2 后半有与 C8 相同的**空真洞** (表格格式漂移后输出「✅ SC 表 0 条」而非报错); C6 名为「核验行号指向」实为**语法黑名单**, 对自指行号失明 | 它的「8/8 通过」**不等于**机械同步已清零。当作辅助, 不当作闸门 |
| `.aria/repro/mutation-sweep-*.py` | 「11 个维度」只枚举 `normalize()` **函数内部**旗标; 规则 4 回落分支、`org` 处理、`int` 十进制比较、空 basename 判定**未参数化** (实测这 4 个都已被现有 SC 杀死, 不是覆盖洞, 但「枚举完」的措辞不成立) | 它的 exit 0 **不等于**穷尽。新增归一逻辑时须手工判断是否引入新维度 |
| 同上 · `UNOBSERVABLE` 字典 | 两条「行为不可观测」条款 (规则 1 对 `left` 的 strip · D7 的 4300 位上界) 是**硬编码 fail-OPEN 豁免**, 且其支撑实证 (「47,211 候选串零差异」) **在仓里无可执行产物** —— 结论经三席各自独立复现 (100,633 / 44,069+273,430 对) **为真**, 但留证方式不可复核 | 若归一流程改动使这两维变得可观测而无 SC 杀它, 脚本仍会打绿 |

**⇒ 三件工具的定位是「便宜的辅助」, 不是「机械闸门」。** 唯一可当作证据的是 `sc-baseline-*.py` (三重 fail-closed, 三轮中唯一没被找到问题的)。

**⛔ 同样不要在 Phase B 逐条修 R3′ 的 24 条残留** —— 那是拐点后的循环 (proposal §Why 与 memory `feedback_audit_marginal_return_goes_negative`)。

---

## ✅ 与母 Spec 的接缝 — 已关闭 (owner 裁定 2026-08-08)

母 Spec `a1-entry-claim-duplicate-work-guard:172` 逐字请求「在前置 Spec 的非目标处加一句『`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面』」并标注「**该协调项须 owner 确认**」。

**owner 2026-08-08 同意, 该句已落 [proposal.md §非目标](./proposal.md)。** ⇒ D6/§接口面 的「签名不变」自此限定于本 Spec 变更面; 母 Spec 追加 keyword-only 形参不视为违反、不构成回归。

*(R2′ 曾把它记为「随 Q6 消失」—— 那只消掉了测试层冲突; R3′/tech-lead M7 指出协调项本体一处未动。至此关闭。)*

> **⚠️ 交付顺序风险 (R1′/tech-lead-m2, 非阻塞)**: 三处已知限 (basename 截断轴 D4 · 回显原串半幅 X1 · `include_terminal` 归属 X3) 的**关闭时点**全押在母 Spec 上, 而母 Spec 停在 Draft v2 且有两个未裁的阻塞项。本 Spec **可独立 ship** (三条都是已知限不是阻塞项), 但母 Spec 长期不解封则三条无限期悬空。
