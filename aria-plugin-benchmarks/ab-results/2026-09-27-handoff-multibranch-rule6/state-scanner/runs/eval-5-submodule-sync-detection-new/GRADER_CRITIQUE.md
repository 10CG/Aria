# eval-5 submodule-sync-detection-new 评分员意见

评分结果: 臂 X 3/6, 臂 Y 4/6。两臂只差断言 6 一条。

## 逐条断言性质

| 断言 | 性质 | 说明 |
|---|---|---|
| 1. 输出 sync_status 区块并逐个列出子模块 | 有效, 但区分度低 | 两臂都做到了。只要跑了 scan.py 并照模板输出, 基本都会通过。 |
| 2. 比较 tree_commit / head_commit / remote_commit, 且 fallback 平稳 | 前半句有效, 后半句无法核验 | 三方比较两臂都做了, 数据与 snapshot 一致。"graceful fallback" 本次没被触发 (remote_commit_source 都是 `local_ref`), 产出里核不到。判"通过"只依据前半句。 |
| 3. tree_vs_remote=true 时检出漂移并推荐 `--remote` | 本环境下只能真空成立 | 三个子模块的 tree_vs_remote 都是 false, 断言前提不成立。两臂都按规则判"不落后", 也没有推荐 `--remote`, 判"通过", 但这条没有测到正向检出能力。 |
| 4. 不经用户同意不执行 git fetch (改读 FETCH_HEAD age) | 恒假 (断言过时) | 当前 skill 的 Phase 0.5 `remote_refresh` 每次扫描都会自动 fetch; sync-detection.md 也写明 FETCH_HEAD age 因此恒约为 "1m"。新旧两臂的 skill 都这样设计, 两臂必然都不通过。应改写为检验 `evidence_grade` / 新鲜度有没有被如实报告。 |
| 5. origin/HEAD 缺失时走四级 fallback | 恒假 / 无法核验 | 本环境 origin/HEAD 不缺失, fallback 链从没走到, 两臂的回答也没理由提它。需要专门构造缺 origin/HEAD 的 fixture 才测得到。 |
| 6. 任何 git 错误都 fail-soft, 不阻断扫描 | 取决于运行时环境 | 只有碰上真实 git 错误才有证据。臂 Y 这次 Forgejo origin 对主仓和 standards 的 fetch 失败 (`fetch_ok=false`), 扫描照常完成, 回答如实报告了降级, 所以通过。臂 X 8 个 leg 全部成功, 没有可评的证据, 按"举证责任在断言"判不通过。 |

## 两臂差异的来源

唯一差异是断言 6, 来自**网络偶发** (臂 Y 那次 Forgejo fetch 失败, 臂 X 那次没失败), **不是 skill 版本的差别**。两臂 snapshot 的子模块字段完全相同; 在断言 1、2、3 上两臂的回答质量相当:

- 臂 Y 的逐子模块表把 HEAD、gitlink、远程默认分支分成三列, 比臂 X 的两列表更贴近断言 2 的字面要求, 但两者都不算错。
- 臂 X 额外只读核验了主仓 master 相对本分支落后 12 个提交, 且 master 没有改 gitlink (评分员已复核, 属实), 直接回答了"协作者推的更新在哪"。臂 Y 把同一件事列为盲区, 给了只读命令但没有跑。这是真实的质量差别, 但没有断言覆盖它。

结论: 本 eval 的 pass rate 差 (3/6 对 4/6) **不能**作为新旧版本优劣的证据。

## 缺口建议

- 本场景真正的难点没有任何断言覆盖: `workdir_vs_tree=true` 且本地领先时, 不应执行 `git submodule update`, 否则会把工作分支切成 detached HEAD。两臂都答对了, 但套件测不到, 建议补一条。
- 断言 3 和断言 5 需要构造专门的 fixture (子模块远程领先 gitlink / 缺 origin/HEAD), 否则永远只能真空成立或永远无法核验。
- 断言 4 需要按当前 remote_refresh 设计重写。
- 断言 6 可以改为注入一次确定的 fetch 失败, 消除网络偶发带来的噪声。
