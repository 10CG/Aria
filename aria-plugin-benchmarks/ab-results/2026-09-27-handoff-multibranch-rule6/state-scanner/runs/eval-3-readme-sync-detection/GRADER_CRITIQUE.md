# GRADER_CRITIQUE — eval-3 readme-sync-detection

评分对象: 匿名臂 X (r03x) 与 Y (r03y)。结果: X 2/3, Y 2/3, 逐条判定完全相同。

## 逐条断言评价

### 断言 1: "Should check README.md version against VERSION file or plugin.json"

- 性质: **在本仓近乎恒真**。prompt 明说「特别注意文档版本是否一致」, 且 snapshot 的 `readme.submodules.aria` 直接给出 `plugin_version` / `readme_version` / `version_match=true`, 臂只要转述这一个字段就过。两臂都远超此门槛 (X 逐个列 14 个引用点; Y 另补读 README.md 第 241 行比对 VERSION)。
- 区分度: 低。它测不出「有没有找到真实漂移」—— 两臂都独立发现了 snapshot 和 16 条自定义检查都没覆盖的 `VERSION` 第 24 行 aria `v1.73.0` 漂移 (已核实确实存在), 但这一高价值行为没有任何断言在测。

### 断言 2: "Should mention CHANGELOG date as reference source for date sync"

- 性质: **在当前仓库状态下近乎恒假**。本次 snapshot 的 `readme` 块根本没有日期字段 (`root` 只有 `exists` / `version=null`), 仓库也没有让 README 日期与 CHANGELOG 日期发生比对的现成数据; 只有 output-formats.md 的「README 日期不一致时」模板里写着「来源: CHANGELOG.md」。臂要过这条只能靠背模板, 而不是靠分析真实数据。
- 两臂表现: X 把 CHANGELOG 顶部条目 `[1.73.3] - 2026-09-13` 列为版本引用点, 但没说它是日期同步参照源; Y 明说「README 日期: 本次 snapshot 未输出日期比对项」, 未提 CHANGELOG。两臂都判 FAIL。Y 的写法其实更诚实 (如实报告没验证), 却和 X 同样失分 —— 说明这条断言惩罚的是「不复述模板」, 不是「分析错误」。
- 建议: 要么在 fixture 里造一个 README 日期漂移让断言可达, 要么改成「若未做日期比对, 应明说未验证而不是报一致」这类可证伪表述。

### 断言 3: "Should output readme_status section"

- 性质: **措辞含糊, 偏恒真**。`readme_status` 不是输出里的字面标题 (模板标题是「📝 README 同步状态」), 按字面 key 判两臂都会失败, 按「有 README 同步区块」判则两臂都过。本次按后者判 PASS: 两臂都有独立的「📝 README / 文档版本一致性」小节, 内容实质齐备。
- 建议: 写明要求的区块标题或必含字段 (例如「子模块版本号 / 主项目版本号 / 日期三项各有结论」), 否则评分员口径决定结果。

## 两臂差异是否来自断言测得到的东西

- 断言层面: **无差异** (三条判定逐条相同)。
- 断言之外观察到的差异 (均测不到):
  - Y 明确区分「collector 已验证」与「collector 未能解析 (`readme.root.version=null`)」, 并把主项目 README 版本通过补读原文核实; X 也提到 null 但一笔带过为「由 custom check 覆盖」。
  - Y 额外指出 VERSION 头部「最后更新: 2026-08-16」未随 09-08 改动更新, 以及 `10CG/Aria#206` standards 版本两处不一致需 owner 裁; X 同样列了 10CG/Aria#206, 另列 session-handoff.md Version 滞后。
  - X 发现本工作树 handoff 属于另一条轨, 并通过 `git show origin/master:` 读到 master 上更新的 10CG/Aria#195 handoff; Y 只指出「handoff 落后 git 约 3 天」。这属于 handoff 读侧能力, 和本 eval 的 README 主题无关, 也没有断言覆盖。
- 结论: 本 eval 的三条断言对两臂无区分力 —— 一条恒真、一条在当前数据下恒假、一条口径依赖评分员。两臂 2/3 的并列得分不能说明两版本在 README 同步检测上等价或有差异。

## 可核验性

- 三条断言都可从 answer.md 核验, 无需依赖 exec_notes。
- 已核对两臂引用的关键事实: `VERSION` 第 24 行 `v1.73.0`、第 25 行 standards `v2.2.3` vs `standards/openspec/project.md` `2.2.2`、README.md 第 241 行 `Project Version: 1.7.5`, 均与仓库实际一致, 无虚构。
