# branch-manager 模式决策报告 (old_skill)

任务: 「修 API key 列表分页」 | 文件 2 个 (src/api/keys.py, tests/test_keys.py, 同目录) | 任务数 1 | 无并行需求

```
risk_level: high
score_breakdown:
  file_count: 2 个文件 → 命中「1-3 个文件」档 → 0
  cross_directory: 不跨目录 (同目录) → 0
  task_count: 1 个任务 → 命中「1-3 个任务」档 → 0
  risk_level: high → +3
  parallel_needed: 不需要并行 → 0
total_score: 3
mode: Worktree
rationale: |
  1. 风险等级自动检测 (SKILL.md「风险等级自动检测」表 + internal/MODE_DECISION_LOGIC.md
     detect_risk_level 伪代码): 描述「修 API key 列表分页」转小写得
     「修 api key 列表分页」, 子串匹配命中 high_risk_keywords 中的 "api"
     (该表: refactor / architecture / api / breaking / 重构 / 架构 / 破坏性 / 核心 → high;
     typo / format / config / doc 等为 low; 其余 medium)。任务为修复而非重构,
     但关键词表按子串匹配, 不区分「API 变更」与「提及 API 的小修复」, 故判 high → +3。
  2. 其余维度: file_count=2 落在 1-3 档 (+0); 两文件同目录, cross_directory=false (+0);
     task_count=1 落在 1-3 档 (+0); parallel_needed=false (+0)。
  3. 决策阈值 (SKILL.md「模式选择算法」+ MODE_DECISION_LOGIC.md Decision Threshold):
     score >= 3 → Worktree; score < 3 → Branch。总分 0+0+0+3+0 = 3, 达到阈值 → Worktree 模式。
  4. 备注 (稳健性): 若按伪代码以 os.path.dirname 从路径计算 cross_directory
     (src/api 与 tests 为两个目录) 则 +2, 总分 5, 决策仍为 Worktree — 两种解读殊途同归。
