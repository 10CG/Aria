# eval-5 submodule-sync-detection-new 评分员意见 (rep3)

评分结果: 臂 X 3/6, 臂 Y 3/6。两臂逐条判定完全相同。

## 逐条断言性质

| 断言 | 性质 | 说明 |
|---|---|---|
| 1. 输出 sync_status 区块并逐个列出子模块 | 有效, 区分度低 | 两臂都有「同步状态」区块和逐子模块表。只要跑了 scan.py 并照模板输出, 基本都会通过。 |
| 2. 比较 tree_commit / head_commit / remote_commit, 且 fallback 平稳 | 前半句有效, 后半句无法核验 | 两臂都给出三列对比, 数据与 snapshot 一致。fallback 本次没被触发 (remote_commit_source 全是 `local_ref`), 产出里核不到, 只按前半句判通过。 |
| 3. tree_vs_remote=true 时检出漂移并推荐 `--remote` | 本环境下真空成立 | 三个子模块 tree_vs_remote 全为 false, 前提不成立。两臂都正确判「不落后」且明确不建议 `--remote`, 判通过, 但没测到正向检出能力。 |
| 4. 不经用户同意不执行 git fetch (改读 FETCH_HEAD age) | 恒假 (断言过时) | 当前 skill 的 remote_refresh 阶段每次扫描都自动 fetch (两臂 snapshot 都是 8 路 fetch_ok=true, remote_refs_age=1m)。新旧两个 skill 版本都这样设计, 任何照 skill 执行的臂都必然不通过。 |
| 5. origin/HEAD 缺失时走四级 fallback | 恒假 / 无法核验 | 本环境 origin/HEAD 不缺失, fallback 链从没走到, 回答也没理由提它。 |
| 6. 任何 git 错误都 fail-soft, 不阻断扫描 | 取决于运行时环境 | 本轮两臂 scan.py 都 exit 0、errors[] 为空、8 路 fetch 全部成功, 没有任何 git 错误可供观察, 两臂都按「举证责任在断言」判不通过。(臂 X 自己手敲的一条 `git rev-parse --short origin/master github/master` 报 exit 128, 那是臂的命令写法问题, 不是扫描器行为, 不计入。) 上一轮 (rep 前一次) 两臂在此条上的差异来自一次偶发的 Forgejo fetch 失败, 本轮网络稳定, 差异消失, 印证它是噪声。 |

## 两臂差异是否来自断言测得到的东西

**不是。** 两臂 snapshot 的子模块字段 (tree/head/remote commit、drift 各字段) 逐项相同, 六条断言判定也逐条相同。能测到的三条 (1/2/3) 两臂都过; 测不到或恒假的三条 (4/5/6) 两臂都不过。本轮 3/6 对 3/6 不含任何版本优劣信号。

断言之外观察到的质量差别 (没有断言覆盖):

- 两臂都答对了本场景的核心: `aria` / `standards` 是 workdir 领先 gitlink (9 / 2 个提交), 不是落后, 此时跑 `git submodule update` 会把子模块切成 detached HEAD、离开 feature 分支。两臂都用只读 git 命令核验了方向 (评分员对照 snapshot 复核属实)。
- 臂 X 额外做了多远程一致性表 (主仓 + 3 子模块 × origin/github), 并给出子模块合并须本地做 + 双推 + 逐个 ls-remote 核验的 Phase C 路径。
- 臂 Y 输出更完整地套用了 skill 的多区块模板 (OpenSpec / Issues 等), 并指出最新 handoff 属于 10CG/Aria#199 轨道而当前分支是 10CG/Aria#195 轨道。
- 两臂都主动提出「协作者推的若是非默认分支则不在比对范围内」, 把盲区交还给用户。

## 缺口建议 (与前一轮一致, 再次确认)

- 本场景真正的难点 (本地领先 gitlink 时不应执行 `git submodule update`) 没有断言覆盖, 建议补一条。
- 断言 3、5 需要专门 fixture (子模块远程领先 gitlink / 缺 origin/HEAD), 否则永远只能真空成立或无法核验。
- 断言 4 需按当前 remote_refresh 设计重写, 例如改为「如实报告远程引用新鲜度 (evidence_grade / remote_refs_age)」。
- 断言 6 应改为注入一次确定的 git/fetch 失败, 消除网络偶发噪声。
