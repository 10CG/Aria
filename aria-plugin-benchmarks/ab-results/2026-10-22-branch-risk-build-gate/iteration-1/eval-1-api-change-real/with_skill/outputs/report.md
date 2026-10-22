risk_level: high
score_breakdown: file_count=+1 (6 个文件, 落 4-10 档) | cross_directory=+2 (backend+frontend 跨目录) | task_count=+1 (4 个任务, 落 4-8 档) | risk_level=+3 (high) | parallel_needed=0 (无并行需求)
total_score: 7
mode: Worktree
rationale: 按 SKILL.md「模式选择算法」(5 维度评分, 阈值 score >= 3 → Worktree)。风险等级依「风险等级自动检测」判定顺序逐级短路: 第 1 步高风险 flat 表 (refactor/rewrite/architecture/breaking/重构/架构/破坏性) — 描述「API 接口变更: 重写鉴权 endpoint 契约」lower 后不含其中任一词 (含「重写」, 但 flat 表收录的是英文 rewrite 与中文「重构」, 不命中); 第 2 步 API 共现规则 — api 类词 (api/接口/endpoint) 命中「API」「接口」「endpoint」, 变更类词 (变更/change/breaking/重构/重写/迁移/删除/移除/deprecat) 命中「变更」「重写」, 两类同时出现 → high (与 SKILL.md 示例「API 接口变更」→ high 一致, 即 10CG/Aria#231 的「变更语义共现」判定)。逐维代入评分表: 1 + 2 + 1 + 3 + 0 = 7 >= 3 → Worktree 模式 (隔离开发环境)。
