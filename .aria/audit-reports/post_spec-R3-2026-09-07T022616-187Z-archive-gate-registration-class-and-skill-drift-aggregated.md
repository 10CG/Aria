---
checkpoint: post_spec
round: 3
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 1C/11M/7m (四席原始 24 条; 反驳席推翻 5, 存活 19)
clusters: 1C
teams: [aria:backend-architect, aria:code-reviewer, aria:knowledge-manager, aria:qa-engineer]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T02:26:16.189Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 3
---

# post_spec R3 — archive-gate-registration-class-and-skill-drift (aggregated)

## Round 3

- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (`no_sibling_found`, own_key = `aria-plugin#186`; github 154 / origin 158)
- **对象**: R2 后拆掉 Part A 的 **227 行**收缩版
- **镜头**: 实现者试派生 / R2 修复验证 / 治理面 / 验收可证伪性 (4 席 + 4 反驳席, 全部完成)

### 逐席 verdict

| 席 | verdict | 原始条数 |
|---|---|---|
| aria:backend-architect (实现者试派生) | PASS_WITH_WARNINGS | 8 (0C/6M/2m) |
| aria:code-reviewer (R2 修复验证) | **FAIL** | 8 (2C/3M/3m) |
| aria:knowledge-manager (治理面) | **FAIL** | 3 (1C/1M/1m) |
| aria:qa-engineer (验收可证伪性) | **FAIL** | 5 (1C/3M/1m) |

### 收敛趋势 (三轮)

| 轮 | 存活 Major | Critical | 问题性质 |
|---|---|---|---|
| R1 | 8 | 1 (被反驳席假推翻, 主控实测推回) | **设计缺陷** (谓词假 alive / 类级漏枚举 / 无代码宿主) |
| R2 | ~14 | 4 | **设计缺陷 + 价值证伪** (生产触达实测为 0 ⇒ 拆分) |
| **R3** | **11** | **1** | **文档一致性 + 自宣已核未实证** —— 审计席自评「不再是设计缺陷…全部可逐条精修, 无需再动结构」 |

按 memory `stop-adding-rounds` (加轮判据 = major 数是否还在降): 14 → 11, **在降**。
按 memory `marginal-return-negative` (拐点判据 = 本轮 fix 引入的 major 占比 > 1/2): R2 修订新写文本贡献了 R3 约 **6/8** 的 finding (与 memory `rewrite≠cleanup` 预测的 86% 吻合) ⇒ **已到或接近拐点**。

## Critical (1 条) 与四条最重 Major —— 主控逐条独立复核

| id | 内容 | 复核 |
|---|---|---|
| **RFV-1** | 「诚实登记」段自造了一个不存在的 issue 号 —— 写「已开 `10CG/aria-plugin#189`」实测 404, 且同文档 D9 写「待开」、SC-8 写「D9 开单并回读核验」三处互斥 | **成立。** 已**真开** `10CG/aria-plugin#189` (回读核验通过), 三处措辞统一。**必须在 D1-D6 之前开** —— 否则那个号会被别的 issue 吃掉 |
| **ACC Critical** | C1 的第三条断言 (命中串须含 `Step 7`) **只写在 proposal 里, 探针脚本中并不存在**; 五态表第五行「挡住两侧同改回 Step2」是假的 | **成立。** grep 确认脚本里 "Step 7" 只在 docstring。已写入断言并重跑: 该坏实现 **rc 0 → rc 1** |
| **RFV-2** | GOV-2 的「已核: README 名册在册」答的是「在不在册」而非「有没有同一句措辞」 | **成立。** `aria/README.md:85` 与 `README.zh.md:85` 此刻逐字带着 `(auto-fixes CLI bugs)` /「（自动修正 CLI bug）」。**类级 sweep 第四次漏兄弟位置**, 且漏在采用者最显眼的入口 |
| **GOV-1** | Rule #6 跨 Skill 上呈项是「先执行后追认」包装成「上呈」—— 自证依据不成立后仍照此定案 | **成立。** 已重构: 三侧各按 SOT §2 的**逐 hunk 明文映射**独立判定, **不再依赖对 §1 跨 Skill 作用域的任何解读**; 上呈项降为 advisory 不阻塞 |
| **RFV-4** | SC-1 的「区段内允许命中逐行钉死 {:47,:49,:632}」用基线行号却在落地后求值, 而 Part B 自身移动行号 ⇒ 落地必假红 | **成立。** 已改为**按内容钉死** + 区段按标题文本动态定位, 不硬编码绝对行号 |
| **RFV-7** | Part E 漏「主仓 gitlink」, 六个机械兜底无一覆盖, 且仓内此刻就漂移 | **成立。** 实测主仓记 `301641b` vs aria 子模块 HEAD `3a28339`。已补入 Part E + SC-9 机械断言 |

## R3 修订 (19 条存活全部处置)

Critical 1 条 + Major 11 条 + Minor 7 条逐条落地。结构性的四项:
1. **Part B 从 15 → 17 条**: 新增 B16/B17 (`aria/README.md:85` + `README.zh.md:85`); SC-1 grep 目标从 2 文件扩到 **4 文件**, 基线区段外 13 → **15**。
2. **Rule #6 重构**: 三侧 (openspec-archive 第二行照跑 / phase-d-closer 第一行 substitute / **state-scanner 第一行 substitute** ← R3 RFV-6 补入) 各自按 §2 明文映射独立判定。
3. **SC-1 判据加固**: 区段按标题文本动态定位; 允许集合按内容钉死; 新增 **SC-1b 语义复核** (固定词表 grep 可被同义换词绕过 —— 审计席实测 `自动修正→自动纠正` 零命中)。
4. **SC-3/SC-4 补机械判据** (原先纯靠执笔者临场裁量)。

其余: B7 占位符 `{id}` → `{change_name}` (全文件既有惯例, `{id}` 从未出现过) + 三行各自给目标; B4/B13/B15 给出确切字面文案与插入点; 「SC-4」四处误指 → 「SC-1」; 通用 post-condition「改后须不再命中 SC-1 pattern」。

## 主控在 R3 修订中自己又抓到两条 (审计席未报)

1. **我为 issue 号纪律新写的机械自检自己就是坏的**。第一版 `grep -nE '(^|[^/A-Za-z0-9-])#[0-9]+'` 在当前 proposal 上报 **9** 处, 其中 6 处是 `Rule #6` / `Rule #3` 规则编号, 1 处是 B15 目标文本里逐字引用的 `#95` (SKILL.md 原文, 不该改)。
   ⇒ 改写成排除三类 (`Rule #N` / code span 内 / 已带仓限定) 的 Python 检查, **三态实测**: 当前版 **0** (rc 0) / R3 修订前版 **3** (rc 1, 恰是审计席点名的那三处, 正控成立) / 坏实现裸 grep **9** (假阳 ⇒ 判无效)。
   memory `check-runs-at-baseline-first` 的又一次实证 —— 新写的检查没在基线亲跑就写进规格。
2. **修裸引用时我把 `#140` 整个删掉了, 那不是修好而是丢信息**。核实后 `10CG/Aria#140` = 「i18n README 版本与正文严重滞后」(closed), 而 `10CG/aria-plugin#140` 是**完全不同**的 secret-guard 外壳逃逸 issue —— 该裸引用是真歧义。已补回 i18n 重译判据行并带仓限定。
   顺带发现审计席也没抓到的一条: **B17 改的是 `aria/README.zh.md` 的正文**, 属实质变更 ⇒ 「只改版本号不重译」那条对它不适用, B16/B17 须同批改到语义一致。

## 下一轮 (R4) 的定位

设计已收敛 (审计席自评 + 主控同判)。R4 应为**聚焦核验轮**: 只验 19 条 R3 修复是否落地 + 是否引入新 Critical, 不做全量重审。
若 R4 零 Critical 且无席判 FAIL, 视为 post_spec 收敛, 进 A.2。
