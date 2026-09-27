# eval-4 config-awareness 评分员批注

评分结果: 臂 X 3/3, 臂 Y 3/3 (同一口径, 同一评分员)。

## 逐条断言性质

1. `Should mention .aria/config.json or config-loader` —— **恒真**。用户 prompt 本身就含 `.aria/config.json` 字面, 任何回答只要复述问题就通过, 不需要 skill 的任何行为。无区分力。

2. `Should describe config fields like auto_proceed or confidence_threshold` —— **近恒真**。只要求提到字段名, 不核对值。两臂报出的值 (confidence_threshold=90 / auto_proceed=false 等) 我已对照 `.aria/config.json` 核实均正确, 但断言本身测不到对错: 编造值的回答同样通过。建议改为"正确报出 confidence_threshold=90 且 auto_proceed=false"。

3. `Should mention default values when config is absent` —— **在当前 fixture 下无法按原意核验**。本仓 `.aria/config.json` 存在, "配置缺失"场景不会自然出现, 只能按弱形式判: 回答是否给出默认值、并说明未设字段/缺失时退回默认。
   - X: "本次扫描按它的配置跑, 没有退回默认值" + confidence_threshold "与默认一致" + mechanical_mode "未设 (= 默认 true)"。
   - Y: 配置表专设"与默认值比"一列, 6 个字段标"同默认", mechanical_mode "未设置 → 默认 true"。
   - 两臂给的默认值都与 `aria/skills/config-loader/SKILL.md` 一致。两臂都判弱通过; 都没有一句完整说明"整份文件缺失时全部退默认"。要测真行为, 需要另造一个没有 `.aria/config.json` 的 fixture 仓。

## 两臂差异是否来自断言测得到的东西

**不是。** 三条断言两臂都通过, 分数差为 0。两臂真实可见的差异全部在断言覆盖面之外:

- **handoff 是否陈旧**: Y 发现工作区的 `latest.md` 已经落后, 并实读 `origin/master` 上的最新 handoff (`2026-09-27-session-close-195-task025-legacy-issue-204.md`, 已由评分员 `git show` 核实); X 停在工作区里 09-24 的 10CG/Aria#199 handoff。
- **推荐方向**: X 的推荐 [1] 是提交 aria/standards 的 gitlink 变更, 这与 master handoff 的"gitlink 前进归 TASK-030/031, 现在不要 git add"冲突; Y 推荐继续组 5 的 TASK-026, 并提示不要重跑认领闸、只刷心跳。
- 配置区块本身两臂质量相当 (Y 多了"与默认值比"一列, 更贴近断言 3 的意图, 但在二值判分下不产生差异)。

结论: 本 eval 在当前断言下对新旧 skill 没有区分力; 分数持平不代表两臂行为等价。
