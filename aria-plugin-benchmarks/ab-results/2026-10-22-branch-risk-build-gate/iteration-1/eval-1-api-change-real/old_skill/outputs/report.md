# branch-manager 模式决策报告

任务描述: 「API 接口变更: 重写鉴权 endpoint 契约」 | 文件 6 个 (backend+frontend 跨目录) | 任务数 4 | 无并行需求

```
risk_level: high
score_breakdown: file_count=+1 (6 个文件落在 4-10 档) | cross_directory=+2 (backend+frontend 跨目录) | task_count=+1 (4 个任务落在 4-8 档) | risk_level=+3 (high) | parallel_needed=+0 (无并行需求)
total_score: 7
mode: Worktree
rationale: 依据 SKILL.md §模式选择算法 (v2.0.0) + internal/MODE_DECISION_LOGIC.md §Scoring Algorithm 五维评分。风险等级经 detect_risk_level 关键词检测: 描述小写化后「api 接口变更: 重写鉴权 endpoint 契约」命中高风险关键词表 (refactor / rewrite / architecture / api / breaking / 重构 / 架构 / 破坏性 / 核心) 中的 "api" ("重写" 亦语义对应 "rewrite"), 无低风险关键词 (typo/format/lint/config/doc...) 命中, 故 risk_level=high → +3。其余维度: file_count=6 属 4-10 文件档 +1; 文件横跨 backend 与 frontend 两个目录, directories>1 → cross_directory +2; task_count=4 属 4-8 任务档 +1; parallel_needed=false +0。总分 1+2+1+3+0=7, 决策阈值「score >= 3 → Worktree, score < 3 → Branch」, 7 >= 3 → Worktree 模式 (隔离开发环境)。与 SKILL.md 示例 3 (跨模块功能: 6 文件 backend+frontend, 4 任务, high, 评分 1+2+1+3+0=7 → Worktree) 完全同型。
```
