# 状态扫描结果: 多远程同步检查

已按 state-scanner 流程运行 `scan.py` (退出码 0, `errors[]` 为空, 远程引用 1 分钟前刚刷新, 证据等级 `fresh`), 并额外对每个 remote 逐个做了 `git ls-remote` 核验。

**先说结论: 扫描结果和你描述的情况对不上。两个 remote (origin 和 github) 目前完全同步, 没有任何落后的一方, 所以现在不需要修复命令。**

另外有两处和你的描述不一致, 请留意:
- 当前 aria-plugin 版本是 **v1.73.3**, 不是 v1.15.0。本地和两个远程都没有 `v1.15.0` 这个 tag。
- 两个远程上的 `v1.73.3` tag 指向同一个对象 (`b29d434`, 解引用后是 `1cb3872`), 说明这次发布已经推到了 github。

---

## 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`), 没有配置 upstream (`no_upstream`)
- 未提交变更 3 项: `aria` 和 `standards` 两个子模块指针有改动 (工作区里的 HEAD 与主仓记录的 gitlink 不同), 另有 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 中断状态: 无 (`interrupt.status = none`); git 操作: 无 (没有暂停中的 rebase 或 merge)

## 🔄 同步状态 (本次重点)

**多远程总体一致: `overall_parity = true`**, 检查范围是 `github` 和 `origin`, 没有不可达的 remote, 没有待推送的提交 (`has_pending_push = false`)。

| 仓库 | 当前分支 | 本地 HEAD | origin | github | 结论 |
|------|----------|-----------|--------|--------|------|
| 主仓 `.` | feature/handoff-multibranch-subdir-path-fidelity | `4f91772` | `4f91772` | `4f91772` | 已同步 |
| `aria` (aria-plugin) | feature/handoff-multibranch-subdir-path-fidelity | `b181678` | `b181678` | `b181678` | 已同步 |
| `standards` | feature/handoff-multibranch-subdir-path-fidelity | `d86fc91` | `d86fc91` | `d86fc91` | 已同步 |
| `aria-orchestrator` | master | `237045a` | `237045a` | `237045a` | 已同步 |

`master` 分支我也单独用 `ls-remote` 核验了一遍:

| 仓库 | origin/master | github/master |
|------|---------------|---------------|
| 主仓 | `c454e35` | `c454e35` |
| aria | `1cb3872` (v1.73.3 合并提交) | `1cb3872` |
| standards | `940cb5b` | `940cb5b` |

**子模块 gitlink 完整性**: 3 个子模块在 2 个 remote 上一共 6 组检查, 全部为 `ok`。也就是说, 主仓在各 remote 上已发布的提交所引用的子模块提交, 在对应 remote 上都能取到, 不存在 GitHub `clone --recursive` 会失败的孤立 gitlink。

**子模块工作区偏移 (不是推送问题)**: `aria` 工作区里的 HEAD 是 `b181678`, 主仓记录的是 `1cb3872`; `standards` 工作区里的 HEAD 是 `d86fc91`, 主仓记录的是 `940cb5b`。原因是两个子模块都切到了当前的 feature 分支, 而这个 feature 分支已经推到了两个 remote。这是本地还没有提交的子模块指针改动, 不是任何一个 remote 落后。

## 🔧 自定义检查
16 项通过, 0 项失败 (其中 `m6-version-badge-match` 的结果是 `badge=1.73.3`, 和 plugin.json 一致)。

## 🛡️ 协调提示
`tracks_multibranch.collision.kind = self_multi_container`: 同一个身份 (simonfish 和 aria-runner-bot) 在多个容器里都有 track。这只是提示, 和这次的推送同步问题无关。

---

## 如果以后真的出现「只推了 origin、忘了推 github」, 修复步骤如下

按项目规范 (多远程硬约束 2), 推送之后必须对每个 remote 分别用 `ls-remote` 核对, 不能只看 push 的返回结果。多仓库操作一律用 `git -C`。**先推子模块, 再推主仓** (这样主仓 gitlink 引用的提交在 github 上一定已经存在):

```bash
# 1. 先推子模块 aria (分支 + 发布 tag)
git -C aria push github master
git -C aria push github v1.73.3          # 换成实际的发布 tag

# 2. 再推主仓
git push github master

# 3. 逐个 remote 核验 SHA (两边都和本地一致才算推送成功)
git -C aria rev-parse master
git -C aria ls-remote origin refs/heads/master
git -C aria ls-remote github refs/heads/master
git -C aria ls-remote --tags github v1.73.3
git rev-parse master
git ls-remote origin refs/heads/master
git ls-remote github refs/heads/master

# 4. 重新扫描确认
/state-scanner    # 期望 overall_parity = true, gitlink_integrity 全部为 ok
```

注意: 如果子模块处于 detached HEAD 状态, 本地 master 可能是旧的, 这时要用 `git -C aria push github HEAD:master`。不要用 force push, 除非先确认过两个镜像确实已经分叉。

---

## 🎯 推荐工作流

推送同步方面没有需要处理的事项。结合当前工作区状态, 可选的后续动作:

- **[1] (推荐) 什么都不用做**: 两个 remote 已经一致。你说的「忘记推 github」可能是别的仓库或更早的一次操作, 已经被后续的双推补上了。
- **[2] 核对你说的是不是另一个仓库或另一个版本**: 如果 v1.15.0 指的是其他项目, 请在那个项目的根目录重新运行 `/state-scanner`。
- **[3] 处理本地未提交的子模块指针改动**: `aria` 和 `standards` 的指针改动, 加上未跟踪的 AB 结果目录, 可以走 C.1 提交 (commit-msg-generator)。提交后还是要双推, 并用 `ls-remote` 核验。
- **[4] 自定义**: 告诉我你想执行哪些步骤。

我无法等待你回复, 以上选项请你自行选择。
