# Tasks — `linked-issue-normalization`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/linked-issue-normalization-audit-trail.md)
> **Level**: 3 | **Status**: 📝 **A.2 + A.3 R1-fix** (2026-08-08) — post_planning R1 五席 5/5 REVISE / verdict FAIL (3 Critical + 12 Major); 本版为 R1-fix, 待 R2
> **Scope**: **跨两仓** — `aria` 子模块 (代码+测试+文档+版本) + 主仓 (gitlink + 版本引用面 + Spec)
> **ship target**: aria-plugin **v1.66.0** (MINOR — 行为面扩大)

> **为什么本 Spec 从 Level 2 升 Level 3**: Q5 裁定 (owner 2026-08-06) 要求 `SKILL.md:176` 的 hunk **照跑 AB, 不走 substitute**, 并写明「本条须进 `tasks.md` 作为独立任务」。而本 Spec 当时是 Level 2 (按 CLAUDE.md 只产出 `proposal.md`) ⇒ **owner 亲裁的 Rule #6 处置唯一落地载体不存在** (R3′ 两席独立命中)。本文件解决它 —— 见 **4.1**。

> **📌 编号不可变约束说明**: 2026-08-08 A.2 首次把本文件由 R3′ 手术产物 (`B-1..B-6` 表格) 重写为 checkbox 形态时, 前一版 `B-n` 从未被任何 `detailed-tasks.yaml` 的 `parent` 引用 (该文件此前不存在), 故无引用被破坏。**本次 R1-fix 只在组 5 末尾追加 5.5–5.8, 不改动任何既有编号** (1.1–1.6 / 2.1–2.3 / 3.1–3.3 / 4.1 / 5.1–5.4 语义与编号均保持)。
>
> **顺带修掉的机械盲区**: 表格形态使 `handoff_autofill` 的 unfinished 扫描完全看不见本 Spec (2026-08-08 handoff §2 实证: 159 条 unfinished 里本 Spec 零条)。checkbox 形态后该盲区对本 Spec 消失; **该 backstop 对非 checkbox 形态 tasks 的失明本身是插件侧待修项**, 不在本 Spec 范围。

---

## 范围边界 — 本文件到哪里为止 (post_planning R1 / tech-lead F3 要求显式声明)

| 阶段 | 归属 | 理由 |
|------|------|------|
| Phase B 实施 + 组 1–4 | **本文件** | change 自身的交付物 |
| **发版同步面 (组 5)** | **本文件** | 版本 bump 与版本引用面是本 change 的交付物之一 (proposal §Impact 已列), 不是 Phase C 的通用动作 |
| **Phase C**: PR 创建 / **pre-merge gate (Rule #8)** / merge | **`phase-c-integrator`**, 不在本文件 | 通用流程, 由该 Skill 的 C.2.4 承担 (CI passing + main 无 in-flight run); 本文件不复述其判据 |
| **Phase D**: cycle 进度更新 / **Spec 归档** / **周期 handoff (Rule #9)** | **`phase-d-closer`**, 不在本文件 | 同上; 归档门会消费本文件全部 checkbox 状态, 故组 5 必须真做完而非声称 |

**⚠️ 组 5 与 Phase C 的时序**: 组 5 的 aria 子模块 bump + 合并 (5.2/5.3) 必须**先于**主仓 gitlink bump (5.4) —— 否则 gitlink 指向未合并的 feature SHA, 产生 orphaned gitlink (CLAUDE.md 多远程硬约束 1, 2026-07-14 事故形状)。主仓自身的 PR 走 Phase C。

---

## Task Group Overview

| Group | 主题 | 依据 |
|-------|------|------|
| **1** | 测试先行 (RED) — 17 条 SC 全量落盘 | proposal §Success Criteria |
| **2** | 实现 (GREEN) — 归一谓词 + 导出单元 + 守卫 | proposal §What Changes 五步 · D7 · D9 |
| **3** | 文档同步 ×3 (两处 substitute + 一处 AB) | proposal §Impact · rule6_note 逐 hunk 表 |
| **4** | Rule #6 AB (⛔ 不豁免) | Q5 裁定 (owner 2026-08-06) |
| **5** | 回归 + 发版同步面 + 留证工件处置 | proposal §Impact + post_planning R1 三条 Critical |

**排序依据**: 组 1 → 组 2 是 RED-first (SC 的 baseline-failing 状态已于 A.1 实跑留证)。**例外: 1.6 (SC-12) 反向依赖 2.1** —— 被测函数 `normalize_linked_issue` 在 2.1 之前不存在, 测试连 import 都不成立, 故 1.6 排在 2.1 之后。组 3 依赖 2.2/2.3 (**3.1 与组 2 同文件, 必须串行**)。**3.3 必须早于 4.1** (AB 测的是该 hunk 的行为影响)。组 5 gate 在组 1–4 全绿之后, 内部按 5.1 → 5.2 → 5.3 → 5.4 → {5.5, 5.6} → 5.7 串。**5.8 例外: 可在 2.3 之后任意时点执行** (它自 2.2 落地即恒红, 不必等发版), 排在末位仅为阅读顺序 —— 依赖字段以 `detailed-tasks.yaml` 为准。

---

## 1. 测试先行 (RED) — `aria/skills/state-scanner/tests/test_release_by_track.py`

> 宿主为既有文件; **既有 6 条测试逐字不改**。⚠️ **锚定方式改为内容锚而非行号锚** (post_planning R1 minor): 本组会往同文件插入用例必致行号位移, 故判据是「既有 6 个 test 方法名及其函数体逐字未变」(用 `git diff` 核), 不是「`:206-247` / `:527-575` 区间未变」。
>
> 每项括注为该项贡献的**子用例场景数**, 全组加总 = **45**, 与 proposal §Impact 的逐条推导独立吻合 (两处任一变动须同批重算)。**「子用例场景」≠ unittest `Ran N` 计数的 test 方法数** —— 一个 test 方法可含多个场景 (本文件既有 `test_invalid_shapes_and_paths` 即 1 方法 4 场景), 故验收**不得**用 `Ran` 数换算, 见 5.1。

- [ ] 1.1 SC-1 / SC-1b / SC-2 / SC-3 / SC-4 — 跨族两两配对 + 三个切分点各自 strip + 不同仓负控 + org 不参与 + int 十进制比较 **(13)**
- [ ] 1.2 SC-5 / SC-5b / SC-5c — basename 轴三态: 截断型**不**归一 (已知限) / 分隔符型 `./_→-` 归一 / 段内空格**不**译码 **(5)**
- [ ] 1.3 SC-6 / SC-6b / SC-10 — 不可解析值退回原串精确比较 + `number_str` 边界五类 + **一条畸形毒不死整批** **(15)**
- [ ] 1.4 SC-11 / SC-13 / SC-15 / SC-14 — 切分方向双轴 (`#` 取最后 / `/` 取最后) + `casefold` 维度 + `number` 相等这一必要条件 **(8)**
- [ ] 1.5 SC-9 — 命中条目回显**未归一原始串** **(1)**
      > ⛔ **治理约束**: 本条 R1′ 曾被移出、R3′ 恢复。Q1 裁定「自己那一侧永不补」后, 回显对方原串成为 D2 fail-toward-reporting 的**唯一**缓解, 且它是输出里唯一携带 `org` 的通道。**不得再次移出。**
- [ ] 1.6 SC-12 — 导出单元返回契约: 可解析返回 `(basename, number)`, 三类不可解析各返回 `None` **(3)**
      > ⚠️ **本条是组 1→组 2 RED-first 排序的唯一例外**: 依赖 **2.1** (被测函数在此之前不存在)。

## 2. 实现 (GREEN) — `aria/skills/state-scanner/lib/collision.py`

- [ ] 2.1 导出纯函数 `normalize_linked_issue(value: str) -> tuple[str, int] | None` — §归一规则五步; `None` 与规则 4 的不可解析枚举一一对应 (D9)
- [ ] 2.2 `linked_issue_overlaps` 内部比较谓词切换为归一键 `(normalize(basename), int(number))` — **签名与返回 schema 不变** (D6, 限本 Spec 变更面)
- [ ] 2.3 解析守卫与异常隔离 — 不含 `#` 先判不可解析 (不得无守卫拆分) · `number_str.isascii() and number_str.isdigit()` 谓词 · `int()` 必包 `try/except ValueError` · `limit = sys.get_int_max_str_digits()` 且**仅当 `limit > 0`** 时比长度 (D7 四条)

## 3. 文档同步

- [ ] 3.1 `lib/collision.py` docstring 同步 — 说明按归一后 `<repo>#<n>` 比较、org 不参与; **措辞不得暗示「已穷尽核实 / 已覆盖全部别名」** (走 substitute)
- [ ] 3.2 `lib/claim_schema.py` `ClaimRecord.linked_issue` 字段文档两处失准同批修 (SAME → same normalized key; active → 实际跳的是 `_TERMINAL` 且不含 `yielded`) (走 substitute)
- [ ] 3.3 `skills/state-scanner/SKILL.md:176` 括注 — 补「(按归一后的 `<repo>#<n>` 比较, org 不参与)」

## 4. Rule #6 AB (⛔ 不申请豁免、不走 substitute)

- [ ] 4.1 用 `/skill-creator` 对 **3.3 的 hunk** 照跑 AB — 时点: **3.3 实施之后、组 5 发版之前**
      > **判据 (不得只判「跑了」)**: 按 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 发版前清单 —— (a) `with_skill` 表现优于 `without_skill`; (b) **无 `WITHOUT_BETTER` verdict** (有则必须修复); (c) 与上次结果比对无回归; (d) `summary.yaml` 已生成并审查。
      > **若判定该 hunk 落在套件覆盖外**: 按 CLAUDE.md Rule #6 表第三行走**三件套** —— 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue (参 aria-plugin #117 / #127); **三件缺一则照跑, 不得静默豁免** (Rule #10)。

## 5. 回归 + 发版同步面 + 留证工件处置

- [ ] 5.1 全量回归 — `cd aria/skills/state-scanner/tests && python3 run_tests.py` 报 **OK 且 0 failures/errors**; 跨 skill `bash aria/skills/run_all_tests.sh` **0 FAIL**
      > ⛔ **不得用 `Ran N` 数换算子用例**: 45 是**场景数**, `Ran` 数的是 test 方法数, 两者单位不同 (既有 `test_invalid_shapes_and_paths` = 1 方法 4 场景)。子用例齐备性判据 = **逐 SC 清单核对 17 条 SC 各自的场景全部落盘**, 与 `Ran` 数无关。
      > ⚠️ 环境陷阱: 单模块模式与 pytest 对 `test_collision.py` 会给 ImportError —— 那是 aria-plugin **#134** 的既有 bug (破 70 天), 非本 change 回归。验收一律以 `tests/` 内**全量** `run_tests.py` 为准。
- [ ] 5.2 **aria 子模块** 5 文件 bump 到 **v1.66.0** — `.claude-plugin/plugin.json` (版本 SOT) / `.claude-plugin/marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`
- [ ] 5.3 **aria 子模块分支合并 + 双远程推送** — 本地 `git merge` 到 `master` (⛔ **禁** Forgejo Web UI / API 的服务端 merge) → `git push origin && git push github` → **逐个 `git ls-remote <remote> master` 取 SHA 与本地比对, 全部一致才算成功**
      > 依据 CLAUDE.md「多远程推送 — 两条硬约束」。服务端合并会使本地 master 从未 fast-forward ⇒ 双推与 C.2.5 结构上都不触发 ⇒ 主仓随后 bump gitlink 即产生 orphaned gitlink, GitHub `clone --recursive` 断裂 (2026-07-14 事故)。**push 回执两个方向都会骗人, 必须独立 `ls-remote`。**
- [ ] 5.4 **主仓** gitlink + `VERSION` 子模块版本表行 + `README.md` **两处**版本引用 (badge + `Plugin Version:` 行)
      > gitlink 必须指向 aria 子模块 **5.3 合并后的 `master` SHA**, 不是 feature 分支 SHA。
- [ ] 5.5 **主仓 i18n README ×3** — `README.{zh,ja,ko}.md` 各 **3 处**版本引用 (`translated-from` 标记 + badge + `Plugin Version:` 行)
      > #140 B 档: 正文无实质变更时**只更这三处标记/版本, 不重译正文**。
- [ ] 5.6 **`CLAUDE.md` 两处版本引用** — 版本区间行 (`v1.52.0–v1.65.5 已 ship`) + 「版本:」行的 `插件 aria-plugin v1.65.5`
      > ⚠️ 只改这两处数字。**不得**把本 Spec 的设计术语写进 CLAUDE.md (污染 AB baseline, aria-plugin #116); 「项目状态」段是覆写非追加, 预算 15-20 行。
- [ ] 5.7 **版本引用点归零机械断言** (post_planning R1 Critical-1 的根因修法) — bump 完成后执行:
      ```
      grep -rn "1\.65\.5" README.md README.zh.md README.ja.md README.ko.md CLAUDE.md VERSION \
                          aria/.claude-plugin/plugin.json aria/.claude-plugin/marketplace.json \
                          aria/VERSION aria/README.md
      ```
      **必须零命中** (`aria/CHANGELOG.md` 显式排除 —— 它是版本史, 保留旧版本号是正确的)。
      > **为什么需要这一条**: 5.2–5.6 是按**文件**枚举, 而错误的维度是**版本引用点**。两条 enabled check 对此结构性失明 —— `m6-version-badge-match` 只比 `README.md` 的 badge, `i18n-readme-translation-currency` 只比 `translated-from` 标记 ⇒ **`README.md` 的 `Plugin Version:` 行 + i18n ×3 的 badge 与 `Plugin Version:` 行共 7 处残留 v1.65.5 时两条 check 仍全绿** (post_planning R1 实测 14 个主仓引用点)。本条是唯一**维度匹配**的判据 (memory `feedback_invariant_dimension_must_match_error_dimension`)。
      > **同时跑不带路径的 `git status`** 核验实际落地面 (memory `feedback_scoped_git_add_splits_claim_from_landing` —— 该形状本项目一天内两次实证)。
- [ ] 5.8 **`.aria/repro/sc-baseline-linked-issue-normalization.py` 处置** — 该脚本断言 8 条 SC 处于 **baseline-failing (红)** 状态; 2.2 落地后它们全部转绿 ⇒ 脚本 `:277` `sys.exit(1)` **恒红**
      > 恒红与假绿同为零信息量 (memory `feedback_false_green_dual_is_permanent_red`), 而它是 substitute 论证**唯一可复核的留证载体**。两条路择一并成文: (a) 加「post-implementation 模式」使其在实现后断言**转绿**并保留 baseline 结果为存档; (b) 显式退役并把 baseline 结果冻结成一份带 SHA 的存档报告, 脚本本身移出 `.aria/repro/`。**不得留成恒红。**

---

## ⚠️ Phase B 开工前必读 — 三条已知限 (不修, 成文)

按 R3′ 的结构性教训, 以下三条**已知洞不修** —— 修它们会按同一规律再生成一批缺陷。Phase B 实施者知道它们的存在即可, **不要在本 Spec 内解决**:

| 工具 | 已知洞 | 影响 |
|---|---|---|
| `.aria/repro/spec-consistency-check.py` | C1/C3/C4 + C2 后半有与 C8 相同的**空真洞** (表格格式漂移后输出「✅ SC 表 0 条」而非报错); C6 名为「核验行号指向」实为**语法黑名单**, 对自指行号失明 | 它的「8/8 通过」**不等于**机械同步已清零。当作辅助, 不当作闸门 |
| `.aria/repro/mutation-sweep-*.py` | 「11 个维度」只枚举 `normalize()` **函数内部**旗标; 规则 4 回落分支、`org` 处理、`int` 十进制比较、空 basename 判定**未参数化** (实测这 4 个都已被现有 SC 杀死, 不是覆盖洞, 但「枚举完」的措辞不成立) | 它的 exit 0 **不等于**穷尽。新增归一逻辑时须手工判断是否引入新维度 |
| 同上 · `UNOBSERVABLE` 字典 | 两条「行为不可观测」条款 (规则 1 对 `left` 的 strip · D7 的 4300 位上界) 是**硬编码 fail-OPEN 豁免**, 且其支撑实证 (「47,211 候选串零差异」) **在仓里无可执行产物** —— 结论经三席各自独立复现为真, 但留证方式不可复核 | 若归一流程改动使这两维变得可观测而无 SC 杀它, 脚本仍会打绿 |

**⇒ 三件工具的定位是「便宜的辅助」, 不是「机械闸门」。** 唯一可当作证据的是 `sc-baseline-*.py` —— **但见 5.8: 它在实现落地后会恒红, 必须处置。**

**⛔ 同样不要在 Phase B 逐条修 R3′ 的 24 条残留** —— 那是拐点后的循环 (memory `feedback_audit_marginal_return_goes_negative`)。

### 另一条环境陷阱 (非本 Spec 引入, 不修)

`aria/skills/state-scanner/tests/test_collision.py:29-30` 的 `sys.path` insert 顺序倒置, 该模块**只在全量 discovery 时**靠字母序更早模块的副作用才能导入; **单模块跑 (`run_tests.py collision`) 与 pytest 跑都硬失败 ImportError**, 并连带把 `test_coordination_ref_lib.py` 打成 collection error。已破 70 天 (`4d87060`), 开号 **aria-plugin #134**, Level 1 修复, **显式不并入本 Spec**。

⇒ **迭代 `lib/collision.py` 时最自然的两条命令都会给 ImportError。不要误判为自己改坏了。**

---

## ✅ 与母 Spec 的接缝 — 协调项已关闭, 但**已知限悬空风险仍在** (两件事, 不要混读)

**(1) 协调项本体: 已关闭 (owner 裁定 2026-08-08)。** 母 Spec `a1-entry-claim-duplicate-work-guard:172` 逐字请求「在前置 Spec 的非目标处加一句『`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面』」并标注「该协调项须 owner 确认」。owner 同意, 该句已落 [proposal.md §非目标](./proposal.md)。⇒ D6/§接口面 的「签名不变」自此限定于本 Spec 变更面; 母 Spec 追加 keyword-only 形参不视为违反、不构成回归。

*(R2′ 曾把它记为「随 Q6 消失」—— 那只消掉了测试层冲突; R3′/tech-lead M7 指出协调项本体一处未动。至此关闭。)*

**(2) 三处已知限的悬空风险: 仍然开着 (与 (1) 无关)。** basename 截断轴 (D4) · 回显原串半幅 (X1) · `include_terminal` 归属 (X3) —— 三条的**关闭时点**全押在母 Spec 上, 而母 Spec `proposal.md:3` 实读为「⛔ 有两个阻塞性未决项, 不具备进 A.2 的条件; 待 owner 裁」。

本 Spec **可独立 ship** (三条都是「已知限」不是「阻塞项」), 且**依赖方向正确** —— 母 Spec `proposal.md:9` 逐字写「前置依赖: `linked-issue-normalization` 必须先 ship」, 本 Spec 独立 ship **不使母 Spec 更难落地** (post_planning R1 / tech-lead 已逐项核: 签名面已裁归母 Spec · 母 §2.1 的 track-id 派生所需两个分量恰由 `normalize_linked_issue -> tuple[str,int] | None` 齐备 · X1 半幅已是 Q1(c) 终局)。

**但母 Spec 长期不解封则三条无限期悬空。** 这不是「接缝没关」, 是「关闭时点不由本 Spec 掌握」。
