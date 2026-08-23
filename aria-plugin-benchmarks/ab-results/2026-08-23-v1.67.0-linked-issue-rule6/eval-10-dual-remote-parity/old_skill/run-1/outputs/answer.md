# 项目状态扫描 — 双远程 (origin / github) 同步情况

> Step 0: `scan.py` exit 10 (部分软错误, snapshot 可用)。snapshot 已写到 `eval-10-dual-remote-parity/old_skill/outputs/state-snapshot.json`。
> 软错误: `snapshot_consistency_inconclusive` — AC-5 对 `origin/feature/linked-issue-normalization` 的 164 个 track 无法评估, snapshot 里的 `overall_parity=true` 按「未验证」对待。下面的结论我额外用 `git ls-remote` 对每个 remote 独立核过 (仓内硬约束 2: 不信 push 回执, 逐 remote 比 SHA)。

## 先纠正一个前提

你说的「刚发布 aria-plugin v1.15.0」**和仓库现状对不上**:

- 本地 / origin / github 三处都**没有 `v1.15.0` 这个 tag** (`git -C aria tag -l 'v1.15*'` 为空, 两个 remote 的 `ls-remote --tags` 也没有)。
- 当前 aria 子模块的版本 SOT `aria/.claude-plugin/plugin.json` = **1.66.4**, 两个 remote 上最新 tag 都是 **v1.66.5**。

所以不存在「v1.15.0 只推到了 Forgejo」这回事。下面按真实数据讲哪些地方同步、哪些地方落后。

## 1. 当前状态

| 项 | 值 |
|----|----|
| 主仓分支 | `feature/linked-issue-normalization` @ `826b356` (upstream `origin/...` ahead 0 / behind 0) |
| 工作区 | 未提交 2 项: `aria` 子模块指针 (unstaged) + 本次 AB 结果目录 (untracked) |
| 关联 OpenSpec | 活跃变更 0 (`openspec/changes/` 无未归档项) |
| git 中间态 | 无 (无 rebase/merge 暂停) |
| 中断检测 | `interrupt.status = none` |

## 2. 变更分析

Level 1; 2 个变更文件均为 other 类 (子模块指针 + 结果目录), 无代码/测试, 无架构影响, 未检出 SKILL.md 变更。

## 8. 同步状态 (重点)

### 8.1 多远程 parity — 逐仓 / 逐 remote (`ls-remote` 实测 SHA)

| 仓库 | 分支 | origin (Forgejo) | github (GitHub) | 结论 |
|------|------|------------------|-----------------|------|
| 主仓 Aria | `master` | `1205ec3` | `1205ec3` | **已同步** |
| 主仓 Aria | `feature/linked-issue-normalization` | `826b356` | **不存在** | github 缺该分支 (feature 分支一般不要求镜像) |
| aria (插件) | `master` | `a0fe720` (v1.66.5 merge) | `a0fe720` | **已同步** |
| aria (插件) | `feature/linked-issue-normalization` | `0fe2e0d` | **不存在** | github 缺该分支 |
| aria (插件) | tags | 最新 `v1.66.5` | 最新 `v1.66.5` | **已同步** |
| standards | (detached `334c609`) | = gitlink | = gitlink | 与 origin/master 一致, parity `unknown` 仅因 detached |
| aria-orchestrator | `master` | `237045a` | `237045a` | **已同步** |

**结论: 两个 remote 的 `master` + 发布 tag 完全对齐, 不存在 Forgejo 领先 GitHub 的发布落差。** 唯一只在 origin 上的是你当前正在做的 feature 分支 (主仓 + aria 子模块各一条), 这是正常的开发中分支, 不是「漏推镜像」。

gitlink 完整性: origin 侧三个子模块全 `ok`; github 侧三条 `no_published_ref` 的意思是「github 上没有这条 feature 分支, 无可核对的已发布引用」, 不是 orphan, 不阻断。

### 8.2 真正落后的是本地, 不是 GitHub

| 项 | 状态 | 含义 |
|----|------|------|
| 本地主仓 `master` | 落后 origin/master 与 github/master **12 个提交** (ahead 0) | 本地 master 陈旧 (v1.66.5 发版在 remote 已合, 本地没拉) |
| 主仓 gitlink → aria | 记录 `9e6a17c`; origin/master 与 github/master 的 gitlink 都已是 `a0fe720` | 你的 feature 分支带的是旧 gitlink (落后 15 个提交) |
| aria 工作区 checkout | `0fe2e0d` (feature 分支), 与 gitlink `9e6a17c` 不一致 ⇒ `aria` 显示为 unstaged 修改 | 正常: 子模块内正在开发 feature 分支 |
| aria 本地 `master` | `9e6a17c`, 落后 remote master 15 个提交 | 子模块 detached/feature 时本地 master 常陈旧 (memory: push 用 `HEAD:master`, 比对前先 `branch -f master origin/master`) |

### 8.3 其他子项

- README 版本一致性: aria `plugin.json` 1.66.4 = README 1.66.4, 一致 (注意 remote 已到 v1.66.5, 你本地 checkout 的 feature 分支基于 1.66.4)。
- 跨终端 collision: `self_multi_container` (dev-claude / aria-runner-bot 两组容器在同 repo 活动), 进 Phase B 前 claim 走 advisory, 本次只读不触发。

## 修复命令 (只描述, 不代跑)

**A. 不需要为 v1.15.0 / v1.66.5 补推 github** — 两个 remote 已一致, 硬推反而可能把陈旧的本地 master 推上去。

**B. 若你的本意是「feature 分支也要镜像到 github」** (可选, 非约定要求):

```bash
# 主仓
git -C /home/dev/Aria push github feature/linked-issue-normalization
# aria 子模块
git -C /home/dev/Aria/aria push github feature/linked-issue-normalization
# 推后逐 remote 核验 (硬约束 2)
git -C /home/dev/Aria ls-remote github refs/heads/feature/linked-issue-normalization
git -C /home/dev/Aria/aria ls-remote github refs/heads/feature/linked-issue-normalization
```

**C. 把陈旧的本地 master 对齐 remote** (两仓, 建议在进入下一步开发前做):

```bash
git -C /home/dev/Aria fetch origin && git -C /home/dev/Aria branch -f master origin/master
git -C /home/dev/Aria/aria fetch origin && git -C /home/dev/Aria/aria branch -f master origin/master
```

(当前都在 feature 分支上, `branch -f` 不会动工作区; 不要对 master 做 checkout。)

**D. 以后发版时的双推标准动作** (防止下次真的漏推):

```bash
# 子模块先推 (含 tag), 再主仓 gitlink
git -C /home/dev/Aria/aria push origin HEAD:master --tags && git -C /home/dev/Aria/aria push github HEAD:master --tags
git -C /home/dev/Aria push origin master && git -C /home/dev/Aria push github master
# 逐 remote 取 SHA 比对, 全部一致才算推成功
for r in origin github; do git -C /home/dev/Aria/aria ls-remote $r master; done
for r in origin github; do git -C /home/dev/Aria ls-remote $r master; done
```

## 10. 推荐工作流

- **[1] (推荐) 无需修复动作** — 双远程发布面已对齐; 如确有「v1.15.0」这个发布, 请给出 tag 名或 commit SHA 我再核, 现有仓库里查不到。
- [2] 执行上面 B: 把 feature 分支镜像到 github (可选)。
- [3] 执行上面 C: 刷新本地 master 指针 (建议, 低风险)。
- [4] 继续当前 feature 分支开发 (linked-issue-normalization, v1.67.0 目标) — 进 Phase B 前会走 claim advisory 闸。

本次为只读扫描, 到此为止, 不启动 workflow-runner。
