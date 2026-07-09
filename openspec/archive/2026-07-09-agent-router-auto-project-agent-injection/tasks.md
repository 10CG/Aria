# Tasks — agent-router-auto-project-agent-injection

> **Spec**: [proposal.md](./proposal.md) (Level 3, Rev4)
> **约定**: 完成勾选 `[x]`; 未做完不勾 (archive gate #95/#134 消费本文件)

## TG-A ROUTING_RULES.md §CAP (proposal §2)

- [x] TASK-001 §CAP 2.1 required_caps: 显式传参 (第 0 优先) + L1 + L2-negation 恒时 + L2-addition 净值门控/上界
- [x] TASK-002 §CAP 2.2 归一 (off-tax 惰性) + 2.3 评分公式 (match_rate / precision 分母=valid_caps / 零分不入池)
- [x] TASK-003 §CAP 2.4 两段式 auto 决策 (Stage 1 基线侧候选间 <0.1 / Stage 2 R-a precision 门 + R-b 有序四分支 [R-c 并入近分支] + decision_path 通则 / B12 消歧段) + 2.5 平局 + 2.6 recommend 混排 (decision 级单值 decision_path)
- [x] TASK-004 L3 文首版本 1.0.0→1.1.0 + 维护指南规则类型枚举五类 (FP/TT/关键词/技术栈/CAP)

## TG-B SKILL.md 主链接入 (proposal §1/§3/§4/§6)

- [x] TASK-005 SKILL.md §205 step 3 忠实 4+1 (3e 六款: 门控最先/扫描+缓存见§4/健壮性/同名 B12 含吸收+警告/归一/评分零分不入池) + step 4 侧别聚合 + step 5 三分支骨架 (auto 两段式; manual 注释修正)
- [x] TASK-006 §393 改写 (D4 rationale 保留 / 删"已生效"暗示 / 缓存子段 §4 新语义 / 基线-项目级措辞修正 / §277 legacy 标注)
- [x] TASK-007 §145 输出契约 (agent_source + decision_path 单值+赋值通则 + required_caps_trace + off_taxonomy_tags + warnings 断言载体, 收窄范围) + 连带 10 段 (§35/§47/§93/§132 required_caps 参数/§145/§250/§305/§323/§383/§438)
- [x] TASK-008 L17 header 整行 (含邻接日期/说明) + L449 footer 统一 1.2.0

## TG-C 配置与周边 (proposal §5/§6)

- [x] TASK-009 `.aria/config.template.json` 补 agent_router 块 (3 key + 注释) 〔主仓文件〕
- [x] TASK-010 `aria/references/capabilities-taxonomy.yaml` 头注释补 agent-router 消费者
- [x] TASK-011 US-011.md AC-4/D4/Scope 三锚点 errata + DEC-20260621-001 **两处**勘误 (按实文措辞) 〔主仓文件〕

## TG-D 验证 (proposal AC)

- [x] TASK-012 structural fixture harness (9 类): proj-a / proj-empty / 宽标签 (valid caps 8) / 同名 backend-architect / **双 R-a specialist** (AC-10) / **单标签 specialist** (AC-2b) / broken frontmatter / off-taxonomy / 纯插件 =0.1 边界对 (AC-13) + 新/旧双文本 runner 变体 (旧=git show 93b7406) + AC-14 隔离副本
- [x] TASK-013 裁决类 AC 实跑: **AC-1, AC-2, AC-4..AC-8, AC-10..AC-14, AC-16** (AC-3 不在本 task, 归 TASK-014; 全部显式传参 required_caps; 双跑, 不一致=fail 回炉)
- [x] TASK-014 AC-3 零回归三支基线对照 (旧 SKILL 文本 vs 新, 结构化字段级; 含 (b) plugin_only×同名组合) — **AC-3 唯一归属本 task**
- [x] TASK-015 AC-15 推断层专项 (L1 词边界 + negation; 不断言 L2-addition 语义)

## TG-E 发版 + 终核 (proposal §6)

- [x] TASK-016 aria-plugin v1.54.0: plugin.json (SOT) + marketplace.json 两处 + VERSION + CHANGELOG.md + README.md
- [x] TASK-017 **AC-9a 插件侧**机械核对 (SKILL/ROUTING_RULES/taxonomy/插件 5 文件 grep 断言; **在 TASK-016 后执行**)
- [x] TASK-018 主仓侧: US-011 三锚点 + DEC L13/L90 勘误落地 + 主仓 VERSION + root README badge + **submodule pointer bump** (gitlink) + **AC-9b 主仓侧核对** (于本 task 末执行, R4 918a4d69); i18n 免重译 (#140 B 档) 〔主仓文件, Phase C 执行〕

## 执行顺序

TG-A → TG-B (§CAP 先在, SKILL cross-ref 有落点) → TG-C, TG-D 前半 TASK-012 (main-loop 顺序无关) → TASK-013∥014∥015 (subagent 真并行) → TG-E: TASK-016 → TASK-017 → TASK-018 (主仓, Phase C)。
主仓文件 (TASK-009/011/018) 随 Phase C 主仓分支落地, 其余在 aria 子模块分支。
