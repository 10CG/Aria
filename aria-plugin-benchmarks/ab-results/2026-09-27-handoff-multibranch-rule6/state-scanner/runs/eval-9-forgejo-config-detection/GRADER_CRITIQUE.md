# eval-9 forgejo-config-detection 评分批注

两臂得分: X = 5/7, Y = 5/7, 逐条判定完全相同。

## 逐条断言性质

| 序号 | 断言 | 性质 | 说明 |
|------|------|------|------|
| 1 | 通过 git remote URL 识别 Forgejo 远程 | 在本环境恒真 | 两臂的 `forgejo_config` collector 源码完全相同 (评分时 diff 过, 零差异), scan.py 必然输出 `forgejo_remote_detected=true`, 臂只要照抄 snapshot 就过, 区分不了版本 |
| 2 | 检查 CLAUDE.local.md 是否存在 | 在本环境恒真 | 理由同上, `config_status=missing` 由脚本直接给出 |
| 3 | 文件存在时检查其中有没有 `forgejo:` 块 | 在本环境恒假 / 无法核验 | Aria 仓根目录没有 CLAUDE.local.md, 这个条件分支结构上跑不到。两臂都描述了「围栏内 `forgejo:` 会被忽略」的逻辑, 但描述不等于执行, 两臂都判 FAIL |
| 4 | 输出 forgejo_config 段和 config_status | 基本恒真 | 字段由脚本产出, 臂只需转述。能测到的只有「回答里有没有把状态值说出来」, 两臂都说了 |
| 5 | 缺配置时建议运行 /forgejo-sync | 基本恒真 | snapshot 的 `suggestion` 字段原样写着这句话, 转述即可通过 |
| 6 | 扫描时不自动创建 CLAUDE.local.md (只读) | 在本评测约束下恒真 | 评测环境本身就禁止写仓, 两臂无论 skill 怎么写都不会创建; 只有在无写限制的环境里才有区分度 |
| 7 | 非 Forgejo 项目跳过检测 | 恒假 / 无法核验 | 本项目有 Forgejo 远程, 跳过分支跑不到; 两臂都判 FAIL |

结论: 7 条里 5 条在本环境下恒真 (1/2/4/5/6), 2 条恒假 (3/7)。这一组断言在当前 fixture 上对两个版本**零区分度**, 5/7 对 5/7 是断言结构决定的, 不反映 skill 质量差异。

## 两臂差异是否来自断言测得到的东西

不是。两臂在断言层面完全一致, 可观察到的差异都在断言覆盖范围之外:

- X 把 Issue 数据来源写成 `live`, snapshot 实为 `cache` (事实小错)。Y 写对了 (「数据来源是缓存」)。
- X 对围栏内 `forgejo:` 的后果说「仍会报 incomplete」, 与 collector 源码一致; Y 说「仍然是未配置」, 不够准确 (源码是 incomplete, 不是 missing)。
- 两臂都额外发现 CLAUDE.local.md 未被 .gitignore 覆盖; Y 多给了 `.git/info/exclude` 这种不改仓库的做法, 并提示 forgejo-sync 模板缺 `api_token` 与其必需配置自相矛盾; X 在推荐项里也提到 `.git/info/exclude`。
- handoff 归属解读不同: X 提醒「10CG/Aria#195 由另一容器持有, 先确认持有方」; Y 判断 handoff §6 已过时、以分支进度为准。两种解读各有依据, 断言不测。

这些差异更可能来自单次运行的随机性, 而不是 skill 版本差异 (forgejo_config collector 两臂一致)。

## 改进建议

1. 断言 3 和 7 需要专门的 fixture: 一个含 CLAUDE.local.md (分别放真实 `forgejo:` 块 / 只有围栏示例 / 无块) 的仓库, 和一个无 Forgejo 远程的仓库; 否则永远恒假, 白白拉低两臂分数。
2. 断言 6 要有区分度, 需要在允许写仓的环境里跑, 然后检查 CLAUDE.local.md 没被创建。
3. 可加一条能测出质量差异的断言: 「回答中关于 Issue 数据来源、config_status 值等事实与 snapshot 一致」, 本次就能抓到 X 的 live/cache 错误。
