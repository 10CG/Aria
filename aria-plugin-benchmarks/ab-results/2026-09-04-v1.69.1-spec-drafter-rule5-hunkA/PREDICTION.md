# PREDICTION — Rule #6 AB `spec-drafter` (v1.69.1 Level 1 批次), 写于八臂派出前 (memory `predict-then-measure`)

- 改动两处, 性质均为**处方性 · 运行时指令面**: (1) A.1.4 生成路径 `standards/openspec/changes/{feature}/` → `openspec/changes/{feature}/` + Rule #5 理由三行 + 预览骨架 `Location:` 行同改; (2) hunk A 措辞软化 (B8): 「**必须**含字段, 与 SOT 模板头部**逐行对齐**」→「**必须**含字段; 顺序**建议**与模板一致 —— 从模板起草自然满足」+ 新增一段「位置不影响机械判定」的 why。
- 套件: `ab-suite/spec-drafter.json` v1.4.0 (4 evals)。**eval 4 是本批新建的定向 fixture** —— 原 3 个 eval 对 A.1.4 路径面零覆盖 (Rule #6 判据表第三行), 套件缺口随 eval 一并闭合。
- 臂: `with_skill` = aria `fix/level1-batch-v1.69.1` 工作树; `old_skill` = aria master `2eca24b` 快照 (`ab-workspace/2026-09-04-spec-drafter-rule5-path-hunkA/skill-snapshot`)。
- 形态: 全部 `descriptive`; 任一臂实跑 git / 写文件 ⇒ 该 eval 不计入 delta。

## 逐断言预测

| eval | 断言 | with | old | 依据 |
|---|---|---|---|---|
| 1 level-judgment | 1 判 Level 1 / 2 说明理由 | PASS / PASS | PASS / PASS | 两版 Level 判定段逐字相同, **零区分度** (本改动不碰该面) |
| 2 bilingual | 1–3 双语解析 / 英文产出 / 保意图 | 全 PASS | 全 PASS | 同上, 不碰 |
| 2 bilingual | 4 `> **Linked Issue**:` 行 / 5 值为 `none` | PASS / PASS | PASS / PASS | 两版 hunk A 都保留「**必须**含字段」+ 三条写法; 软化只动「顺序」半句 |
| 3 TARGETED | 1–3 字段行 / `none` / 非链接形 | PASS / PASS / PASS | PASS / PASS / PASS | 同上 |
| 3 TARGETED | **4 头部四行顺序 Level→Status→Created→Linked Issue** | **PASS (但这是本改动的风险点)** | PASS | ⚠️ 软化后「逐行对齐」降为「顺序建议」, 理论上 with 臂可能不再排序 ⇒ 该断言转 FAIL。**预测仍 PASS**: 软化文本里逐字保留了四字段顺序且写明「从模板起草时自然满足」, 而起草路径本身就是照模板。若实测 FAIL, **不改 eval 迁就**, 原样上呈 (B8 的软化与 eval 3-A4 的存续二选一, 交 owner) |
| 3 TARGETED | 5 不改字段名 | PASS | PASS | 不碰 |
| **4 location (新)** | 1 落点 = 项目仓 `openspec/changes/` | **PASS** | **FAIL (60%)** | old 臂 SKILL.md 逐字给 `standards/openspec/changes/{feature}/`; 但历史 5 个 run 曾各自独立发现该矛盾并 override ⇒ 有 ~40% 概率 old 臂靠 CLAUDE.md 里的 Rule #5 自纠 |
| 4 location | 2 全文不推荐 `standards/openspec/changes/` | PASS | FAIL (60%) | 同上 |
| 4 location | 3 理由点到共享子模块 / Rule #5 | PASS | FAIL (70%) | 新版把理由写进了 SKILL.md; old 臂即使路径蒙对也多半只给路径不给这层理由 |
| 4 location | 4 字段行 + `none` | PASS | PASS | 两版同 |

## 汇总预测

- with_skill **12/12 (100%)**; old_skill **9/12 (75%)**; delta **+0.25**
- WITHOUT_BETTER: **0**
- 最可能的意外: (a) eval 3-A4 在 with 臂转 FAIL (软化过头) ⇒ delta 降到 +0.17 且需上呈; (b) old 臂在 eval 4 自纠 ⇒ delta 降到 0, 说明「SKILL.md 写错路径」在有 CLAUDE.md 兜底时区分度不足 —— 那也是真实结论, 照记不修
- 若 delta ≤ 0: **不改 expectations 迁就, 不降级**, 原样上呈 owner (Rule #10 / TASK-017 同款纪律)
