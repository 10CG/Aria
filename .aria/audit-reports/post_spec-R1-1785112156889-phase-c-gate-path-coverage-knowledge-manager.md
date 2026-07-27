---
agent: knowledge-manager
round: R1
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 0
major_count: 5
minor_count: 3
---

# post_spec 审计 R1 — knowledge-manager

范围: proposal 全文 / phase-c SKILL.md 全文 (1055 行) / workflow-runner wait_recoverable 段 / config.json 四个注释字段 / CLAUDE.md 规则 #6 #8 / 两个 decisions 目录惯例 / 全仓 grep pr_ci_status 枚举出现次数与 config-loader 平行 schema 登记表。

## Major

**KM-1｜Impact 表遗漏 `aria/skills/config-loader/SKILL.md` (第二权威 config schema 消费方)**
:241-277 维护 pre_merge_gate.* 每键的 type/default/valid_values 登记 (v1.31.0 加 ci_backends 时同步登记过)。`path_coverage_enabled` 不登记即打破连续记录。修法: Impact 补一行 + 登记条目 (描述性内容, Rule #6 substitute 即可)。

**KM-2｜SKILL.md 内 pr_ci_status 枚举三处, proposal 只覆盖两处**
:176 紧凑 YAML 预览块 / :242-245 verdict 步骤 / :262 Output schema。:176 历史上从不随详细版同步, 照单必漏 → 同文件自相矛盾。另「五处」与正文六项计数出入。修法: 显式点名 :176 + 统一计数。

**KM-3｜SKILL.md 顶部总览配置表 (:39-53) 与 §C.2.4 内嵌表 (:272-281) 双表重复, proposal 字面「§C.2.4 同步」只覆盖后者**
顶部表在 §C.2.4 之前, 严格按标题执行会永久缺 path_coverage_enabled。修法: 两张表都点名。

**KM-4｜同一事件 (v1.64.1) 两个矛盾序数 (第 5 次 vs 第 2 次) 未注明口径**
未来读者重建判例链会卡住。修法: 注明「第 5 次 = 历史总复发人工裁决; 第 2 次 = 2026-07-25 新规确立后的手工特批」或统一口径。

**KM-5｜owner 2026-07-25 裁决唯一原件在 `_lane` JSON 注释里, Phase D 要改写的正是它**
对比 v1.49.0 block-flip 有独立 decisions 文档 + SKILL.md cross-ref。改写前不存档 = 论证原文丢失风险。修法: Phase D 改写 `_lane` 前先抽取全文存独立 DEC (docs/decisions/ 近期为 canonical, DEC-YYYYMMDD-NNN 命名), `_lane` 改写后留指针。

## Minor

**KM-6｜`_comment` / `_not_ci_backends_empty` 与 `_lane` 描述同一事故, §6 只点名 `_lane`** — Phase D 清单三字段处置都过一遍。
**KM-7｜新步骤/分支未按惯例带版本标注** — 「2.5 Path coverage 评估 (v1.65.0+)」式内联版本号。
**KM-8｜命名核查结论 (无需改动, 存档)**: 扁平 `path_coverage_enabled` 优于嵌套形 (namespace 内不再嵌套是本仓惯例); decision 枚举与既有术语体系无撞车。

## 结论

设计自洽, 问题在文档同步完整性与归档 cross-reference 完整性。REVISE 后进 Phase B, 避免实现阶段照单漏改产生新漂移。
