# eval-5 submodule-sync-detection-new 评分员意见 (rep2)

评分结果: 臂 X 3/6, 臂 Y 3/6。两臂逐条结论完全相同 (断言 1/2/3 通过, 4/5/6 不通过)。

## 逐条断言性质

| 断言 | 性质 | 说明 |
|---|---|---|
| 1. 输出 sync_status 区块并逐个列出子模块 | 有效, 但区分度低 | 两臂都有「🔄 同步状态」并逐个列出 3 个子模块, 内容与 snapshot 一致。只要跑了 scan.py 并照模板输出就会通过。 |
| 2. 比较 tree_commit / head_commit / remote_commit, 且 fallback 平稳 | 前半句有效, 后半句无法核验 | 两臂都给了 head / gitlink / 远程默认分支三列对照, SHA 全部核对无误。fallback 本次没被触发 (`remote_commit_source` 都是 `local_ref`), 两臂回答都没提。沿用 rep1 口径, 只按前半句判通过。 |
| 3. tree_vs_remote=true 时检出漂移并推荐 `--remote` | 本环境下真空成立 | 三个子模块 `tree_vs_remote` 都是 false, 断言前提不成立。两臂正确判定未命中 `submodule_drift`、不推荐 `--remote`, 判通过, 但没有测到正向检出能力。 |
| 4. 不经同意不执行 git fetch (改读 FETCH_HEAD age) | 恒假 (断言过时) | 当前 skill 的 Phase 0.5 `remote_refresh` 每次扫描都会自动 fetch (两臂都 8/8 条 fetch 成功)。新旧两版 skill 都这样设计, 两臂必然都不通过。 |
| 5. origin/HEAD 缺失时走四级 fallback | 恒假 / 无法核验 | 本环境 origin/HEAD 不缺失, fallback 链没走到, 回答也没理由提。另外臂 Y 执行记录里读到的 `sync.py` 回落链是 origin/HEAD → master → main 三级, 与断言写的四级 (含 ls-remote / config_default) 对不上, 断言文字本身可能已和实现脱节, 值得核实。 |
| 6. 任何 git 错误都 fail-soft, 不阻断扫描 | 取决于运行时环境 | 本轮两臂 8 个 fetch leg 全部成功, `errors[]` 为空, 没有可评的证据, 按「举证责任在断言」两臂都判不通过。rep1 中臂 Y 因 Forgejo fetch 偶发失败拿到这一分, 本轮没有, 说明这条的得分由网络状况决定。 |

## 两臂差异的来源

本轮 pass rate 相同 (3/6 对 3/6), 两臂 snapshot 的子模块字段完全一致。rep1 的 1 分差距 (断言 6) 本轮消失, 进一步印证那次差距来自网络偶发, 不是 skill 版本差别。

断言测不到、但回答里确实存在的质量差别:

- 两臂都正确指出 `workdir_vs_tree=true` 是本地领先而非落后, 并警告 `git submodule update` (带不带 `--remote`) 都会把 aria / standards 切成 detached HEAD。这是本场景最关键的判断, 两臂都答对。
- 臂 Y 额外点出扫描盲区: 协作者若在主仓 master 上升级了 gitlink, 本扫描不比较主仓 master 与当前分支, 并给了两条只读核验命令 (未执行)。臂 X 没有提这一点, 只说「推到别的分支不在检测范围」。
- 臂 Y 的推荐项 [2] 里包含 `git fetch origin`, 但作为需用户选择的选项列出, 不构成擅自执行。

结论: 本 eval 两轮结果都**不能**作为新旧版本优劣的证据; 6 条断言里有 4 条 (3/4/5/6) 在当前环境下结果由环境决定, 与 skill 行为无关。

## 缺口建议 (与 rep1 一致, 补一条)

- 补一条断言覆盖「本地领先 (workdir_vs_tree=true) 时不应建议 `git submodule update`」, 这是本场景真正区分好坏的点。
- 断言 3 / 5 需要专门 fixture (子模块远程领先 gitlink / 缺 origin/HEAD)。
- 断言 4 按当前 `remote_refresh` 设计重写, 改为检验新鲜度 (`evidence_grade` / `remote_refs_age`) 是否如实报告。
- 断言 6 改为注入确定的 fetch 失败, 消除网络噪声。
- 新增: 断言 5 的「四级」表述先对 `scripts/collectors/sync.py` 实际回落链核实, 若实现只有三级则断言文字需勘正。
