# 项目状态扫描结果 (state-scanner)

scan.py 已执行，退出码 0 (全部采集成功，`errors[]` 为空)。扫描前 scan.py 对 origin / github 两个 remote 的主仓 + 3 个子模块都做了实时 fetch (8 条 fetch 全部成功，证据等级 `fresh`，远程 ref 年龄 1 分钟)，所以下面的同步结论是基于最新远程状态，不是陈旧缓存。

## 先说结论：和你描述的情况对不上

**扫描结果显示两个 remote 当前完全同步，没有任何一侧落后。** 同时有两点和你的描述不一致，需要你先确认一下：

1. **当前 aria-plugin 版本是 v1.73.3，不是 v1.15.0。** `aria/.claude-plugin/plugin.json` = `1.73.3`，aria/README 版本 = `1.73.3` (一致)。
2. **`v1.15.0` 这个 tag 在本地和两个 remote 上都不存在。** 我用只读的 `git ls-remote --tags` 分别查了 origin 和 github：两边都只返回 `v1.73.3` (同一个 SHA `b29d434`)，没有 `v1.15.0`。本地 aria 子模块的 tag 列表里也没有它。

所以可能是：(A) 版本号记错了 (你指的其实是最近的 v1.73.3 发布)；(B) 那次推送是在另一台机器 / 另一个 checkout 上做的，还没反映到这个工作区；(C) 你推的是某个分支而不是 master/tag。见文末的选项。

---

## 📍 当前状态

- 分支：`feature/handoff-multibranch-subdir-path-fidelity` (主仓 HEAD `4f91772`)
- 未提交变更 3 项：`aria` / `standards` 两个子模块指针 (gitlink) 有改动未提交，外加 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 无中断的工作流 (`interrupt.status = none`)，无进行中的 git rebase/merge
- 当前 feature 分支没有配置 upstream 跟踪 (`no_upstream`)，但远程上存在同名分支，多远程比对按本地远程 ref 做了 (见下)

## 🔄 同步状态 (本次重点)

多远程检查已启用，受检 remote：`github`、`origin`。**`overall_parity = true`，`has_pending_push = false`，`has_unreachable_remote = false`。**

### 当前分支 (各仓当前检出分支) 逐个 remote 比对

| 仓库 | 当前分支 | 本地 HEAD | origin (Forgejo) | github (GitHub) |
|------|----------|-----------|------------------|-----------------|
| 主仓 `.` | feature/handoff-multibranch-subdir-path-fidelity | `4f91772` | ✅ 一致 `4f91772` (领先 0 / 落后 0) | ✅ 一致 `4f91772` (领先 0 / 落后 0) |
| `aria` (aria-plugin) | feature/handoff-multibranch-subdir-path-fidelity | `b181678` | ✅ 一致 `b181678` | ✅ 一致 `b181678` |
| `standards` | feature/handoff-multibranch-subdir-path-fidelity | `d86fc91` | ✅ 一致 `d86fc91` | ✅ 一致 `d86fc91` |
| `aria-orchestrator` | master | `237045a` | ✅ 一致 `237045a` | ✅ 一致 `237045a` |

### master 分支 (发布所在分支) 补充核对

发布一般落在 master，所以我另外用只读 `git ls-remote` 直接问了两个 remote 的 master：

| 仓库 | 本地 master | origin master | github master |
|------|-------------|---------------|---------------|
| 主仓 | `c454e35` | ✅ `c454e35` | ✅ `c454e35` |
| `aria` | `1cb3872` (v1.73.3 合并提交) | ✅ `1cb3872` | ✅ `1cb3872` |
| `standards` | `940cb5b` | ✅ `940cb5b` | ✅ `940cb5b` |
| `aria-orchestrator` | `237045a` | ✅ `237045a` | ✅ `237045a` |

### 子模块指针可达性 (gitlink integrity)

检查「主仓在某 remote 上已发布的提交所引用的子模块 SHA，在该子模块同名 remote 上是否拿得到」——这正是「只推了 Forgejo 忘推 GitHub」最会出事的地方 (GitHub 上 `clone --recursive` 会断)。

| 子模块 | origin | github |
|--------|--------|--------|
| aria | ✅ ok | ✅ ok |
| standards | ✅ ok | ✅ ok |
| aria-orchestrator | ✅ ok | ✅ ok |

没有 `orphaned` (悬空指针)。

### 子模块指针与工作区

- `aria`：主仓记录的指针 = `1cb3872` (= 远程 master，v1.73.3)；子模块工作区 HEAD = `b181678` (feature 分支上的新提交)。即主仓有一个**未提交的**指针变更，不是推送问题。
- `standards`：同理，指针 `940cb5b`，工作区 HEAD `d86fc91`，未提交。
- `aria-orchestrator`：指针 = 工作区 = 远程，无漂移。

### 条件子项

- 📝 README 版本一致性：✅ aria 子模块 plugin.json `1.73.3` = README `1.73.3`
- 📦 standards 子模块：✅ 已注册、已初始化
- 🔗 Forgejo 配置：⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少本地 forgejo 配置块，建议运行 `/forgejo-sync` 引导创建 (需确认)

## 其他区块 (简要)

- 🛡️ 审计：已启用；最近一次 `post_planning` 审计 PASS，已收敛 (2026-09-24)
- 🔧 自定义检查：16 项全部通过，0 失败
- 📄 UPM：未配置
- 📚 handoff：最新交接 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (由 latest.md 指针确定，约 60 小时前)
- ⚪ 多容器提示：检测到同一身份 (simonfish / aria-runner-bot) 在多个容器上的并发轨 (`self_multi_container`)。协调默认开启，进入 Phase B 时由认领闸门处理，这里只是提示，与本次推送问题无关。

---

## 修复命令

**就当前扫描结果而言：没有需要修复的 remote，不需要执行任何推送。** origin 和 github 在主仓和三个子模块上都一致。

如果你确认确实有一次发布只推到了 Forgejo (例如在另一台机器上做的，或者版本号就是 v1.73.3 只是记错了)，按下面的顺序补推。**顺序很重要：先推子模块，再推主仓**，否则 GitHub 上主仓会引用一个 GitHub 子模块里还不存在的提交 (悬空指针，`clone --recursive` 失败)。

```bash
# 0. 先拉最新远程状态 (在做发布的那个工作区里执行)
git -C aria fetch origin --tags
git fetch origin

# 1. 先补推子模块 (aria-plugin) 到 GitHub：分支 + 发布 tag
git -C aria push github master
git -C aria push github v1.15.0        # 把 v1.15.0 换成实际的发布 tag 名

# 2. 如果 standards 也随发布更新过，同样补推
git -C standards push github master

# 3. 再补推主仓 (包含子模块指针 bump 的那个提交) 到 GitHub
git push github master
git push github --tags                  # 若主仓也打了 tag

# 4. 逐个 remote 用 ls-remote 核验，不要只看 push 的回执
for r in origin github; do
  echo "$r aria:      $(git -C aria ls-remote $r refs/heads/master | cut -c1-7)"
  echo "$r main:      $(git ls-remote $r refs/heads/master | cut -c1-7)"
  echo "$r aria tag:  $(git -C aria ls-remote --tags $r v1.15.0 | cut -c1-7)"
done
echo "local aria:  $(git -C aria rev-parse --short master)"
echo "local main:  $(git rev-parse --short master)"
# 两个 remote 的 SHA 都要和本地一致才算推送成功；ls-remote 本身失败就重试几次再下结论
```

注意事项：
- 子模块的合并要在本地做 (`git merge` 后双推)，不要用 Forgejo 网页 / API 的服务端合并——服务端合并的提交只存在于 Forgejo，本地和 GitHub 都没有，正是这类「一边有一边没有」的根源。
- 如果 push 被拒 (non-fast-forward)，说明 GitHub 上有你本地没有的提交 (镜像分叉)，**不要直接 force**，先 `git fetch github` 比对再处理。
- 以后发布建议每次都双推：`git push origin && git push github`，然后做第 4 步核验。

---

## 🎯 推荐工作流

**[1] 无需修复，确认版本号 (推荐)**
- 理由：实时 fetch 后两个 remote 在主仓 + 三个子模块上完全一致，gitlink 全部可达；v1.15.0 tag 在任何地方都不存在，当前版本是 v1.73.3 且已在两个 remote 上。
- 步骤：告诉我你实际指的发布版本号 / 在哪台机器上推送的，我再针对性核对。
- 跳过：所有推送步骤。

**[2] 在做过发布的那个工作区重新扫描**
- 理由：如果那次推送发生在另一个 checkout / 另一台机器，本工作区看不到它的本地提交 (但只要推到了 Forgejo，这里 fetch 后应该能看到 origin 领先 github——而实际没有，所以这个可能性较低)。
- 步骤：在那个工作区运行 `/state-scanner`，看同步区块里 github 是否显示「落后」。

**[3] 按上面的修复命令手动补推 GitHub**
- 仅当你确认存在一个只在 Forgejo 上的提交或 tag 时才用。按「子模块 → 主仓 → ls-remote 核验」顺序执行。

**[4] 继续当前 feature 分支的工作**
- 当前主仓有 `aria` / `standards` 两个子模块指针变更未提交 + 1 个未跟踪的 benchmark 结果目录；这与推送问题无关，是当前 feature 分支 (10CG/Aria#195) 的在途工作。可走 C.1 提交 (提交后再按双推 + ls-remote 核验推送)。

也可以自定义组合步骤 (例如「B.2 + C.1」)。请选择 [1]-[4]。
