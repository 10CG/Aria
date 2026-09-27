# eval-8 评分员意见 (readme-skill-count-badge-check)

两臂得分: X = 5/8, Y = 5/8。两臂失分的是同样 3 条断言 (第 5、7、8 条)。

## 逐条断言性质

| # | 断言 | 性质 | 说明 |
|---|------|------|------|
| 1 | 核对 aria/README.md 版本 vs plugin.json | 接近恒真 | scan.py 的 `readme.submodules.aria.version_match` 直接给出答案, 任何照 snapshot 转述的臂都能过, 区分不出 Skill 版本 |
| 2 | 统计 Skill 时排除 `user-invocable: false` | 有区分力 | 需要臂自己读 frontmatter; 两臂都数对了 (42 = 35 + 7)。断言里举例的 5 个内部 Skill 已经过时 (实际 7 个, 另有 git-remote-helper、aria-token-telemetry) |
| 3 | 比对计数与 README 声明 | 有区分力, 但判据太粗 | 只要求「做了比对」, 不要求覆盖 `aria/README.zh.md`。Y 发现该文件写的是 `34 + 7 = 41` (真错漏), X 没发现, 两臂同样 PASS |
| 4 | 比对目录名与 README 列表 | 有区分力, 但判据太粗 | 两臂都找出 aria/README.md 漏 issue-triage、session-closer (经核实为真)。X 另外找出主项目 README.md Skills 表 (第 133 行起) 漏 session-closer; Y 反而说主项目 README「没有逐项列表」, 是事实错误。断言没点名主项目 README, 这个差异测不到 |
| 5 | `skill_list_missing` 按 info 级输出 | 当前产出下恒假 | 两个版本的 SKILL.md / references 里都搜不到 `skill_list_missing` 这个字段名 (只有 `readme_skill_count_mismatch`), scan.py 也不产出它。臂只能人工比对, 没有任何机制要求标严重级。这条考的是一个不存在的输出字段 |
| 6 | 核对主项目 README badge vs plugin.json | 接近恒真 | custom check `m6-version-badge-match` 已在 snapshot 里给出 OK, 转述即过 |
| 7 | badge 不匹配时报 warning | 无法核验 | 当前仓库 badge = 1.73.3 = plugin.json, 不匹配场景不存在; 臂也没理由凭空说明「如果不匹配会报 warning」。在本仓库状态下对任何臂恒 FAIL |
| 8 | aria 子模块缺失时优雅跳过 | 无法核验 | aria 子模块存在 (`exists: true`), 缺失路径没被触发。恒 FAIL |

## 两臂差异是否来自断言测得到的东西

没有。两臂分数完全相同, 而两臂真实的质量差异都落在断言以外:

- Y 独有的正确发现: `aria/README.zh.md` 计数写成 41 (少 1)。
- X 独有的正确发现: 主项目 README.md Skills 表漏 session-closer; 以及 aria/README.md 中 agent-router / agent-team-audit 的 internal 标注不一致。
- Y 的事实错误: 称主项目 README 没有逐项列表 (实际有)。
- 两臂都正确指出了用户说的「v1.14.0 刚发布」这个前提不成立 (实际 1.73.3), 没有断言测这一点。

这些差异来自执行时的偶然覆盖面, 不是本 eval 能区分的 Skill 版本行为。

## 改进建议

1. 第 5、7、8 条在当前仓库状态下结构上不可能通过, 应改用构造出的 fixture 仓库 (badge 故意落后、aria 子模块缺失、README 故意少列 Skill), 或者删除。
2. 第 5 条引用的 `skill_list_missing` 字段在两个版本的 Skill 里都不存在, 先核实断言的依据是否已过时。
3. 第 3、4 条应点名要覆盖的文件 (aria/README.md、aria/README.zh.md、主项目 README.md Skills 表), 这样上面的差异才测得出来。
4. 加一条断言测「识别出 v1.14.0 前提与仓库实际版本不符」—— 这是本 prompt 真正考验判断力的地方。
5. 第 2 条例子里的内部 Skill 名单应更新为当前 7 个。
