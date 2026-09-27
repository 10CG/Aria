# SCORES — Rule #6 AB `state-scanner` · `10CG/Aria#195` (TASK-026)

> 由 `tools/score.py` 从两臂 `grading.json` 直接汇总, **不经人工转述** (复跑: `python3 tools/score.py`)。`-rep2` / `-rep3` 是逐 eval 回归判据要求的复跑, 不计入 delta。

| eval | 类别 | with | old | with − old |
|---|---|---|---|---|
| eval-1-basic-state-collection | 主样本 | 3/3 | 3/3 | +0 |
| eval-2-user-options-display | 主样本 | 2/2 | 2/2 | +0 |
| eval-3-readme-sync-detection | 主样本 | 2/3 | 2/3 | +0 |
| eval-4-config-awareness | 主样本 | 3/3 | 3/3 | +0 |
| eval-5-submodule-sync-detection-new | 主样本 | 3/6 | 4/6 | -1 |
| eval-5-submodule-sync-detection-new-rep2 | 复跑 | 3/6 | 3/6 | +0 |
| eval-5-submodule-sync-detection-new-rep3 | 复跑 | 3/6 | 3/6 | +0 |
| eval-6-upstream-behind-detection-new | 主样本 | 2/6 | 1/6 | +1 |
| eval-7-issue-awareness-opt-in-new | 主样本 | 4/8 | 4/8 | +0 |
| eval-8-readme-skill-count-badge-check | 主样本 | 5/8 | 5/8 | +0 |
| eval-9-forgejo-config-detection | 主样本 | 5/7 | 5/7 | +0 |
| eval-10-multi-remote-parity-drift | 主样本 | 6/12 | 6/12 | +0 |
| eval-11-submodule-push-github-sync-miss | 主样本 | 4/9 | 4/9 | +0 |
| eval-12-unnamed-12 | 主样本 | 5/5 | 5/5 | +0 |
| eval-13-a1-heartbeat-on-entry-TARGETED | 主样本 | 6/6 | 6/6 | +0 |

主样本 eval 数 = 13; 断言合计 with 50/78 · old 50/78
mean(with pass_rate) = 0.7141; mean(old pass_rate) = 0.7141
delta.pass_rate = +0.0000
主样本中 with < old 的 eval: ['eval-5-submodule-sync-detection-new']
  eval-5-submodule-sync-detection-new: 样本 3 个, 其中 with < old 的 1 个 ⇒ 不判回归
