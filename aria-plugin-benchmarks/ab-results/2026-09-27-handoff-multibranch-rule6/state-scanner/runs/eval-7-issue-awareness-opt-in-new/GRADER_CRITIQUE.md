# eval-7 issue-awareness-opt-in-new 评分员意见

两臂 (匿名 X / Y) 得分: X 4/8, Y 4/8。两臂 scan.py 产出的 issue_status 完全相同 (49 open, label_summary={bug:4}, 两条 OpenSpec 启发式关联, linked_us 全空, fetch_error 为空, source=cache), 回答里的事实都和 snapshot 对得上。

## 逐条断言可测性

| # | 断言要点 | 性质 | 说明 |
|---|----------|------|------|
| 1 | 仅 enabled=true 时展示 Open Issues 区块 | 半边可测 | 本 eval 只给 enabled=true, 「only when」的另一半 (false 时不展示) 观察不到。两臂都展示了区块, 通过。实际上只要跑了 scan.py 且回答了就会通过, 区分力弱。 |
| 2 | 4 级优先级平台探测 | 恒假 (在本场景) | 用户已在 config 里写明 platform=forgejo, 第 1 级直接命中; 探测逻辑在 scan.py 内部, 最终回答没理由去讲另外 3 级。两臂都失败, 不反映 skill 差异。 |
| 3 | 走 forgejo CLI wrapper + 处理 10 个 fetch_error 枚举 | 恒假 (在本场景) | 抓取由 scan.py 完成, 执行臂看不到也无需说明调用方式; 联网正常时 fetch_error 为空, 10 个枚举值一个都不会出现。两臂都失败。 |
| 4 | 缓存 15 分钟 TTL, 路径 .aria/cache/issues.json | 部分可测 | TTL 与 source=cache 会出现在回答的数据来源行 (两臂都有); 路径只有执行臂主动去 ls 才会有证据。X 在 exec_notes 核验了路径所以通过, Y 没核验所以失败。**这一分差来自执行臂的核验勤勉度, 不来自 skill 版本**。 |
| 5 | skill 内不管理 API token | 恒真 | 负向断言, 执行臂正常情况下不会碰 token。两臂都通过, 无区分力。 |
| 6 | US-NNN 与 OpenSpec 启发式关联 (含词边界保护) | 部分可测 | 关联结果在 snapshot 里, 回答是否说出来取决于执行臂; 「词边界保护」无法从产出观察。X 只展示 OpenSpec 关联、没提 US 关联, 判失败; Y 两类都说了 (明写 linked_us 全空), 判通过。**这一分差同样主要来自回答的完整度, 两臂底层数据相同**。 |
| 7 | 有 blocker/critical 时推荐 triage | 前提不成立 | 真实数据里没有 blocker/critical 标签, 规则的正分支测不到; 只能看回答有没有正确说明「未触发」。两臂都正确说明了, 通过。要测正分支需要带 blocker 标签的 fixture。 |
| 8 | 离线 / CLI 缺失时 fail-soft | 恒假 (在本场景) | 活仓联网正常, 降级路径不会被触发。两臂都失败。 |

## 两臂差异是否来自断言测得到的东西

- 总分相同 (4/8), 分布不同: X 在断言 4 多拿一分, Y 在断言 6 多拿一分。
- 这两处差异都是「执行臂回答写得多全 / 是否额外核验」的差异, 两臂 scan.py 采到的 issue 数据逐字段相同。**没有证据表明差异由 skill 版本造成**。
- 8 条断言里有 3 条 (2 / 3 / 8) 在活仓联网场景下结构上恒假, 1 条 (5) 恒真, 2 条 (1 / 7) 只能观察一侧分支。这个 eval 对新旧版本之间的 issue 感知行为基本没有区分力。

## 改进建议

1. 断言 2 / 3 / 8 改成针对 scan.py 输出的 SC 级结构化测试 (伪造 config / 断网 / 移除 CLI), 而不是对最终回答打分。
2. 断言 7 需要一个带 blocker 标签 issue 的 fixture 缓存 (例如预置 .aria/cache/issues.json), 才能测到正分支。
3. 断言 1 补一个 enabled=false 的对照 eval。
4. 没有断言覆盖、但两臂都做到且对用户很有价值的点: 识别出 limit=20 导致两个仓截断 (49 只是下限), 以及指出「0 个 blocker 只代表没人打标签」。可以考虑加为断言。
