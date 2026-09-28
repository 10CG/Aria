# eval-10 multi-remote-parity-drift 评分批注 (grader)

结果: 臂 X 6/12, 臂 Y 6/12, 通过项和未通过项完全相同 (通过 1/2/4/6/10/11, 未通过 3/5/7/8/9/12)。

## 根本问题: 题设场景在真实仓里不存在

这个 prompt 假设「只推了 origin、漏推 github」, 但两臂都是在真实仓 `/home/dev/Aria` 上实跑 scan.py, 没有搭夹具。实跑结果 (两份 snapshot 一致): 主仓和 3 个子模块在两个 remote 上都是 `parity=equal`、`ahead_count=0`、`behind_count=0`、`evidence_grade=fresh`, `gitlink_integrity` 6 组全部 `ok`, `has_pending_push=false`, `has_unreachable_remote=false`, `overall_parity=true`。另外 `v1.15.0` 这个 tag 在哪里都不存在。

两臂都如实报了「和你说的对不上, 两个 remote 已同步」, 这是正确行为。但大部分断言测的是漂移形态下的推理, 在这个环境里变成了「恒假」或「恒真」, 测不出两个版本的差异。

## 逐条分类

| # | 断言要点 | 本环境下的性质 | 说明 |
|---|----------|----------------|------|
| 1 | 逐 remote 状态, 不合并成一个 | 可核验, 但区分度低 | 只要回答画了逐 remote 表就过, 两臂都过 |
| 2 | 列全 remote (主仓 + 子模块) | 可核验, 但区分度低 | 同上 |
| 3 | 用 ahead_count>0 量化 | **恒假** | 真实状态没有任何分歧, 只有照抄规则文字的回答才能过 |
| 4 | 不含糊地说 up-to-date, 要区分 origin 已同步和 github 未同步 | **后半句无法成立** | github 实际没落后; 按「逐 remote 给出证据、不笼统」判两臂都过。换个口径就会两臂都不过, 结论同样一致 |
| 5 | 1.35 不触发的推理 | **恒假 (缺前提)** | 前提 `parity=ahead` 没出现, 回答没有理由主动去讲 clause 4 / triggers_rule |
| 6 | 补推提示 `git -C <path> push github master` | 可核验 | 两臂都给了「假设场景」下的补推命令, 两臂都过; 模型常识就能写出来, 区分度低 |
| 7 | parity: ahead 既不阻塞也不算正向证据 | **恒假 (缺前提)** | 没有 ahead |
| 8 | parity: unknown 二分 | **恒假 (缺前提)** | 没有 unknown |
| 9 | overall_parity=true 要有正向证据 (equal+fresh) | 基本测不到 | 两臂都报了 fresh + equal 这个事实, 但都没把它表述成判据。Y 写了「不是陈旧缓存」, 措辞更接近, 但不构成规则表述。按同一口径两臂都判不过; 这条在正常态下只能测「有没有背规则」 |
| 10 | 有 unreachable 时不走六路分派; 只有 pending_push 也不告警 | **恒真 (真空成立)** | 两个标志都是 false, 什么都不说就能过 |
| 11 | gitlink 孤立因果链 | 可核验 | 两臂都在补推顺序说明里讲清了 clone --recursive 会断; 这是项目 CLAUDE.md 约束 1 自动加载进上下文的内容, 很可能是**基线污染**, 不是 skill 的功劳 |
| 12 | DISCRIMINATOR: gitlink 作为已接线路由 | **恒假 (缺前提)** | gitlink 全部 ok, 路由不会触发; 两臂都既没说「已接线」也没说「是缺口」, 判别器在这里失效 |

## 两臂差异是否来自断言测得到的东西

没有。两臂得分和通过项完全相同。能看到的差异都不在断言覆盖范围内:
- Y 多报了 forgejo_config 缺配置块、审计状态、handoff 指针等其他区块, 补推命令更全 (standards、`--tags`、ls-remote 循环), 还提醒了「子模块合并要在本地做」;
- Y 的 exec_notes 记录 `refs/remotes/{origin,github}/master` 在本地不存在, X 的 exec_notes 记录 rev-parse 过这些 ref, 两边说法有出入, 但不影响回答里的事实 (两臂的 master SHA 都来自 ls-remote, 与 snapshot 一致)。

两臂回答里的事实 (SHA、v1.73.3、tag `b29d434`、gitlink 全 ok、16 项自定义检查全过) 都和各自的 snapshot 对得上, 没有发现编造。

## 建议

1. **必须用夹具复现题设形态**: 在临时副本里造一个「origin 比 github 多一个提交」的子模块 + 主仓 gitlink bump, 只推 origin (注意 memory 里记的造副本陷阱: 子模块的绝对 gitdir 会让 `cp -a` 副本写回真仓, 本地路径 clone 要用 `file://`)。否则 3/5/7/8/12 永远是恒假, 这一整个 eval 对 Rule #6 AB 没有判别力。
2. 断言 12 (DISCRIMINATOR) 要真正起作用, 夹具里必须包含 gitlink orphan (主仓在 github 上的提交引用了 github 子模块里不存在的 SHA)。
3. 断言 4 应该拆成两条: 「不笼统说 up-to-date」和「在漏推形态下指出 github 落后」, 避免在正常态下口径两可。
4. 断言 10 是否定式断言, 前提不成立时真空成立, 建议加前提 (夹具里造 unreachable remote) 或者在正常态下剔除。
5. 断言 11 可能受 CLAUDE.md 约束 1 污染, 基线也能过, 建议改成要求引用 `gitlink_integrity` 字段/状态值, 而不只是讲出因果链。
