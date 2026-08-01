# C.2.5 Multi-Remote Push Enforcement — 执行推演 (aria 子模块 PR 刚合并)

> 场景前提: aria 子模块的 PR 刚合并到本地 master; 配置了两个 remote: `origin` (Forgejo) + `github` (GitHub mirror); 主仓另有子模块关系 (aria 是 Aria 主仓的 submodule, gitlink 待 bump)。以下为描述性推演, 未实跑命令。

## 0. 前置确认: 合并形态必须是本地合并

进入 C.2.5 之前先确认这次合并是**本地 `git merge` 完成的**, 而不是 Forgejo 服务端 (Web UI / API `Do: merge`) 合并的。子模块一律禁止服务端合并——服务端合并的 merge commit 只存在于 Forgejo, 本地 master 从未 fast-forward, 后续双推和 SHA 验证在结构上根本不会触发, 主仓再 bump gitlink 就会产生 orphaned gitlink, GitHub 侧 `clone --recursive` 直接断裂。

确认方式: 本地 `git -C aria log --oneline -1 master` 看到的 HEAD 就是刚才合并产生的 merge commit (或 fast-forward 后的目标 commit), 且工作区在 master 上、干净无未提交改动。若发现合并发生在服务端而本地落后, 先 `git -C aria fetch origin && git -C aria merge --ff-only origin/master` 把本地 master 对齐, 再继续 (并记录这次偏离, 供复议)。

## 1. 枚举 enforced remotes

```bash
git -C aria remote -v
```

确认待推清单: `origin` (Forgejo, canonical) + `github` (mirror)。两个都是 enforced——多远程一致性完全靠本地双推保证, 没有服务端 mirror 同步兜底, 所以**不允许只推一个**。

## 2. 记录本地基准 SHA

```bash
LOCAL_SHA=$(git -C aria rev-parse master)
```

这是后面所有验证的比对基准。若本次发版还打了 tag (如 v1.65.0), tag 也进入推送与验证清单。

## 3. 逐个推送 (顺序执行, 不并行)

```bash
git -C aria push origin master
git -C aria push github master
# 如有 tag:
git -C aria push origin vX.Y.Z && git -C aria push github vX.Y.Z
```

要点:
- 用 `git -C aria` 显式指定仓库路径, 不依赖 cwd (多仓操作的老坑)。
- 顺序推而非 `&&` 短路后不管——即使第一个失败, 也要知道第二个的状态, 但**不要**因为第一个失败就跳过验证直接重试 force。
- push 的退出码和回执**不作为成功依据**, 只作为初步信号。两个方向都会骗人: 假阴性 (回执报错但实际推上了) 会诱发误 force; 假阳性/半推 (一个成功一个失败) 会造成镜像分叉。

## 4. Post-push SHA 验证 (核心步骤, 不可省)

对**每个** remote 独立取远端 master SHA, 与 `LOCAL_SHA` 比对:

```bash
git -C aria ls-remote origin refs/heads/master
git -C aria ls-remote github refs/heads/master
```

判定规则: **两个 remote 的 SHA 都等于本地 SHA, 才算推送成功**。任何一个不一致, C.2.5 整体判定失败, 不得进入主仓 gitlink bump。

如有 tag, 同样 `ls-remote <remote> refs/tags/vX.Y.Z` 逐个核验。

## 5. 失败处理分支

### 5.1 ls-remote 自身失败 (网络/CF Access 抖动)

不立刻下结论。重试 2-3 次 (间隔几秒); 仍失败则把该 remote 标记为「状态未知」, 停在 C.2.5, 报告 owner——未知不等于失败, 更不等于成功, 不能靠猜测继续。

### 5.2 某 remote SHA 落后于本地 (push 没生效)

最常见形态: 半推成功造成镜像分叉的前奏。处置:
1. 先 `git -C aria fetch <remote>` 拿到远端真实状态。
2. 若远端只是落后 (本地 SHA 是远端 SHA 的后代): 直接重推 `git -C aria push <remote> master`, 然后回到第 4 步重新验证。
3. 重推仍失败: 看错误类别——认证 (Forgejo PAT / CF Access 过期)、hook 拒绝 (如 GitHub Secret Scanning 扫整个 push range 挡历史 commit)、网络。逐类排查, 不盲目重试超过 3 次。

### 5.3 某 remote SHA 与本地分叉 (既非祖先也非后代)

说明有第三方写入 (并行 session / aria-runner-bot / 服务端合并残留)。这是最危险的分支:
1. **禁止直接 force push**。
2. 三项前置核验后才考虑 `--force-with-lease`: (a) fetch 后确认远端多出的 commit 内容是什么、来自谁; (b) 确认那些 commit 已被本地包含或确实应被覆盖 (例如是之前误推的坏 commit); (c) 确认没有并行 session 正在向该 remote 推送。
3. 若远端多出的是合法工作 (别的轨道推的), 改为本地 merge/rebase 吸收后重新走第 3-4 步。
4. 拿不准就停下报告 owner, 分叉处置错误的代价 (丢 commit) 远大于晚推几小时。

### 5.4 两个 remote 都失败

多半是本地侧问题 (网络断 / 凭据整体失效)。修好环境后从第 3 步重来; 期间主仓侧任何 gitlink bump 一律冻结。

## 6. 通过后的下游动作 (顺序不可倒)

只有第 4 步**全部一致**后, 才允许主仓 Aria:
1. `git add aria` bump gitlink 指向新 SHA, 提交;
2. 主仓自身同样双推 origin + github;
3. 主仓也做同样的 post-push `ls-remote` 双端验证。

顺序铁律: **子模块先落两端, 主仓 gitlink 后 bump**。倒过来就是 orphaned gitlink 窗口——GitHub 侧主仓指向一个 GitHub 上不存在的 aria commit, `clone --recursive` 断裂。

## 7. 记录

C.2.5 的验证结果 (每个 remote 的 SHA、比对结论、任何重试/异常) 写入本次 cycle 的记录; 若出现过 5.3/5.4 这类需要人工判断的分支, 无论最终是否自行恢复, 都在 handoff 里如实记录请 owner 复议 (Rule #10: enabled 闸门的任何临场处置都不算 AI 的自由裁量)。

## 一句话总结

双推是手段, **逐 remote `ls-remote` SHA 全等才是"推成功"的唯一判据**; 任何一端不一致就地熔断, 不 bump gitlink, 不信 push 回执, 分叉不盲 force。
