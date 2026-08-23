# Rule #6 AB 结果 — state-scanner `SKILL.md:176` 括注 (Aria spec linked-issue-normalization TASK-013)

**基线** aria `9e6a17c` (v1.66.4) vs **新版** iteration-1 `0fe2e0d` / iteration-2 `880060d` (括注补归一细则)。
执行: /skill-creator 流程, 每 eval 两臂各 1 run, 独立 subagent, 独立 grader (iteration-1) / 主控亲评落盘 (iteration-2, 仅 2 run)。
`benchmark.json` 由 `aggregate_benchmark.py` 生成 (⚠️ 其 Summary 的 Delta 符号按「Old − With」打印, 下表以 per-eval 计数为准)。

## iteration-1 (12 evals × 2 臂)

| eval | 新版 | 基线 | delta |
|---|---|---|---|
| 1 status-basic | 3/3 | 3/3 | — |
| 2 status-options | 2/2 | 2/2 | — |
| 3 doc-version-consistency | 2/3 | 2/3 | — |
| 4 config-presence | 2/3 | 2/3 | — |
| 5 submodule-sync | 4/6 | 4/6 | — |
| 6 branch-behind-upstream | 1/6 | 1/6 | — |
| 7 open-issues-scan | 5/8 | 4/8 | +1 (措辞波动: 「ttl 15m」) |
| 8 readme-skill-count-badge | 6/8 | 5/8 | +1 (措辞波动: 「info 级」) |
| 9 forgejo-config-missing | 6/7 | 6/7 | — |
| 10 dual-remote-parity | 4/12 | 4/12 | — |
| 11 github-mirror-unpushed | 2/9 | 2/9 | — |
| **12 linked-issue-overlap (定向, 新建)** | **4/5** | **2/5** | **+2 (两条承重)** |
| 合计 | 41/72 = 64.6% | 37/72 = 59.2% | +4 |

时间 332s vs 338s / token 89.9k vs 90.7k (无显著差异)。**无 WITHOUT_BETTER**; 与上次 state-scanner AB 无回归 (既有 11 条零负 delta)。

## iteration-2 (只重跑 eval-12, 括注 v2)

iteration-1 的承重断言 1 (「明确答会报, 不是不确定」) **两臂都败**: 新版 hedge「取决于 `#` 前空格能否被解析, skill 文本没写」—— 根因是括注只写了「按归一后的 `<repo>#<n>` 比较, org 不参与」, 没写空白 / 大小写 / 分隔符细则。v2 括注补全后:

| eval | 新版 v2 | 基线 |
|---|---|---|
| 12 linked-issue-overlap | **5/5** | 3/5 |

逐条 (v2 / 基线): 1 明确会报 ✅/❌ · 2 归一键 + org 不参与 ✅/❌ · 3 `10CG/Aria#152` 不命中 ✅/✅ · 4 advisory 不阻断 ✅/✅ · 5 不声称字面比较 ✅/✅ (基线本轮只做条件陈述)。

## 测前预期 vs 实测 (PREDICTION.md)

| 预期 | 实测 | |
|---|---|---|
| eval-1..11 无 delta | 9 条完全相同, 2 条 +1 (措辞) | ✅ (措辞波动在预期噪声内) |
| eval-12 有 delta | +2 → iteration-2 +2 且新版满分 | ✅ |
| 可证伪点 (b)「新版也没答对 ⇒ 括注没传达到」 | **部分命中**: iteration-1 承重断言 1 新版也败 | 已按此修括注 (v2), 这是本次 AB 的真实产出 |

## 套件覆盖缺口 (Rule #6 判据表第三行, 三件齐备)

该 hunk 落在 SKILL.md「Layer L Phase B 集成」段, 既有 11 条 eval **零覆盖** (实测无 delta 印证)。按判据表第三行处置:
1. **点名行为** = 对 `--linked-issue` 重叠告警「怎么算同一个 issue」的规则陈述 (归一键 / org 不参与 / 空白大小写分隔符 / 回落);
2. **可证伪定向 fixture** = 新建 eval-12 (已入 `ab-suite/state-scanner.json` v1.6.0; 实测基线 2/5·3/5, 新版 4/5·5/5, 有区分力);
3. **套件缺口 issue** = **aria-plugin #157** (新开; 同时记录 eval-5 A4 过时断言、eval-6/10/11 不可达路径断言恒 fail 的套件固有问题)。

⇒ 三件齐备, 且**仍照跑了**既有 11 条 (宁跑勿豁)。本次不申请任何豁免。

## 过程记录

- 24 个 regression 臂在本仓 feature 分支上跑, 每臂 snapshot 独立写入各自 outputs (避免 `.aria/state-snapshot.json` 争用); scan.py 在 feature 分支恒 exit 10 (#176 形状), 两臂同受影响, 不构成 delta。
- 跑到中途旁证: 并发轨 #152 ship v1.66.5 (aria `a0fe720`), 多臂独立报出「feature 分支落后 master 12/15」—— 与 AB 无关, 已另行合入本轨。
- 按先例只提交 PREDICTION / RESULT / benchmark / eval_metadata / grading / answer / timing; snapshot·skill 副本·静态 viewer html (12MB) 不入库。
