# Verification Record — agent-router-auto-project-agent-injection

> **约定**: detailed-tasks.yaml `metadata.verification_record` 指向本文件 (#95 archive gate 可锚)。
> **方法**: Rule #6 structural substitute — fixture runner (LLM 忠实执行器注入新/旧 SKILL+RULES 全文) × 结构化字段级机械断言 × 双跑一致性; 裁决类 AC 显式传参 `required_caps` pin (推断-裁决解耦)。
> **基线**: 旧文本 = `git show 93b7406:skills/agent-router/{SKILL,ROUTING_RULES}.md` (aria 子模块 base)。

## §TASK-013/014/015 — fixture 实跑轨迹

### Round 1 (2026-07-09, 48 runs: 24 case × 双跑)

**PASS 21/24**; FAIL 2 (AC-2a / AC-16a); 双跑不一致 1 (AC-16b)。

分诊 (三个非过项均非实现缺陷即真歧义, 全部处置):
| case | 根因 | 处置 |
|------|------|------|
| AC-2a | fixture expected 校准错 — runner 正确采 ROUTING_RULES FP-022 (canonical) 使基线 top-2 近分 (0.90/0.85) 触发**既有** <0.1 降级 → recommend; 核心意图「不误召」(database-specialist 零命中不产出) 双跑均已证 | expected 重校准 (recommend + 不误召断言保留) |
| AC-16a | fixture 任务文本含「接口」逐字命中 TT-002 触发词 → 基线 0.95 (非预期 0.85), d=0.05 落分支 (1); runner 双跑一致且正确 | fixture 任务改词去触发词 |
| AC-16b | **真文本歧义 (双跑分叉实锤, 回炉机制按设计触发)**: 基线候选池为空时 R-b 的 d 无定义 — r1 语义虚构 TT 命中凑基线, r2 保持空池但 d 未定义 | **ROUTING_RULES §CAP-4 补分支 (0.5)**: 基线池空时挑战者按 threshold 单独裁决 (≥→直派 / <→recommend, 均 R-b) + 「不得语义虚构命中」显式禁令 |

Runner 顺带抓到的新文本瑕疵 (一并修复):
- SKILL §323 示例 4 precision 数值错 (2/3≈0.67 非 1.0) → 修正 + 分母注
- 「R-b 有序四分支」计数与 (0)-(4) 实况不符 → 统一「有序分支 (0)-(4)」
- §145 v1.2.0 additive 块仅锚 auto_match 形态 → 补 recommend 适用注

### Recovery (回炉, 按 TASK-013 fail-回炉政策)

SKILL/RULES 文本被修改 → **重建全部 48 prompts → 重跑全批** (013+014+015 全体, 非仅失败项 — 防跨规则耦合静默回归)。

### Round 2 (2026-07-09, 回炉全批重跑; 中途撞 session 用量上限 → workflow resume 棘轮补跑)

**终态: PASS 24/24 case (48/48 runs), FAIL 0, 双跑不一致 0, 缺失 0** (机械断言 `assert_runs.py`, 报告 `assert_report.json`)。

- AC-1/5 (R-a 直派+堵短路) / AC-2a (不误召, 零命中不产出) / AC-2b (单标签禁令) / AC-3a-c×新旧 (零回归三支, 新旧文本对照逐字段一致, 含 plugin_only×同名组合) / AC-4a-b (跨池护栏+precision 拦宽标签) / AC-6 (recommend 混排 Top-1 项目级+agent_source) / AC-7 (frontmatter 边界 skip 不阻断) / AC-8-manual (无新字段) / AC-10 (双 R-a precision tiebreak: migration-master 1.0 > schema-wizard 0.75) / AC-11 (off-tax 惰性+off_taxonomy_tags 列出) / AC-12 (同名接管四元组: auto+baseline+project+警告) / AC-13×新旧 (纯插件 =0.1 边界不降级, 防再犯) / AC-14 (stale 缓存 stat 差异重扫, 新 caps 生效) / AC-15 (推断层: trace.l1 双 tag + negation 移除 interface-design) / AC-16a (R-b 分支2 宽标签数值直派 — Impact 已登记风险的接受实证) / AC-16b (基线池空分支 (0.5): 0.75<threshold → recommend, **回炉后双跑一致**)
- 回炉验证: AC-16b 从 R1 双跑分叉 (baseline/auto vs R-b/recommend) → R2 双跑一致 — §CAP-4 分支 (0.5) + 「不得虚构命中」禁令消歧生效

### 残余 ambiguity (runner 反馈, 均 pre-existing v1.1.x 基线层, 逐条标注「不影响本次结果」)

follow-up 素材 (不在本 spec 范围 — Stage 1 基线「既有性质, 本 change 不改变」):
1. ROUTING_RULES §关键词匹配 无词边界/子串/作用域语义 (v1.0.0 起)
2. SKILL §输入参数 task_type「自动推断」程序未定义 (v1.0.0 起)
3. SKILL §93 摘要表 `frontend/**` 行与 ROUTING_RULES FP-022 目标冲突 (v1.0.0 起; v1.2.0 §93 banner 已声明 ROUTING_RULES canonical)
4. recommend Top-3 general-purpose 0.50 兜底仅示例无条文 (v1.0.0 起)
5. threshold 比较 >= vs > 未明文 (v1.0.0 起)
建议: 开 follow-up issue 收纳 (Phase D 归档时经 D auto-issue 或手动)。

## §TASK-017 — AC-9a 插件侧机械核对

(待 TASK-016 发版后执行)

## §TASK-018 — AC-9b 主仓侧核对

(Phase C 主仓分支执行)
