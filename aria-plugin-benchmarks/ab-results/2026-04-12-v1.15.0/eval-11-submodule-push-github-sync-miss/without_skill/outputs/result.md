# Eval-11 — Submodule Push GitHub Sync Miss (without_skill)

**日期**: 2026-04-12
**场景**: 复现 2026-04-12 发版事件 — aria 子模块 Forgejo 已合并, 本地 master 同步 Forgejo, 但 GitHub mirror 未推送
**工作目录**: `/home/dev/Aria`
**方法**: 仅使用原生 git 命令 (禁用 Skill 引导)

---

## 1. 仓库清单与远程配置

| 仓库 | 路径 | origin (Forgejo) | github |
|------|------|------------------|--------|
| 主项目 Aria | `/home/dev/Aria` | `forgejo.10cg.pub:10CG/Aria.git` | `github.com:10CG/Aria.git` |
| aria 子模块 | `/home/dev/Aria/aria` | `forgejo.10cg.pub:10CG/aria-plugin.git` | `github.com:10CG/aria-plugin.git` |
| standards 子模块 | `/home/dev/Aria/standards` | `forgejo.10cg.pub:10CG/aria-standards.git` | `github.com:10CG/aria-standards.git` |
| aria-orchestrator | `/home/dev/Aria/aria-orchestrator` | Forgejo only | (无 github remote) |

---

## 2. 扫描方法

对每个带有多远程的仓库执行:

```bash
git -C <repo> fetch --all --quiet
git -C <repo> rev-list --left-right --count HEAD...origin/master
git -C <repo> rev-list --left-right --count HEAD...github/master
git -C <repo> rev-list --left-right --count origin/master...github/master
```

**关键点**: 不依赖 `git push` 的 "Everything up-to-date" 输出 (该提示只比较当前 push 的单一 remote, 无法发现跨 remote 漂移). 必须先 `fetch --all` 再 `rev-list --left-right --count` 对比每一对 ref.

---

## 3. 扫描结果

### 3.1 主项目 `/home/dev/Aria`

```
HEAD                = 5b7a5f7
local master        = 5b7a5f7
origin/master       = 5b7a5f7
github/master       = 5b7a5f7

HEAD vs origin/master   : 0 ahead / 0 behind
HEAD vs github/master   : 0 ahead / 0 behind
origin/master vs github : 0 / 0
```

状态: **同步** (OK)

---

### 3.2 aria 子模块 `/home/dev/Aria/aria` — **漂移检测命中**

```
HEAD                = 19f2861
local master        = 19f2861
origin/master       = 19f2861   (Forgejo)
github/master       = f55e130   (GitHub, 落后 2 个提交)

HEAD vs origin/master   : 0 / 0
HEAD vs github/master   : 2 ahead / 0 behind     <-- 本地领先 GitHub 2 个提交
origin/master vs github : 2 / 0                   <-- Forgejo 领先 GitHub 2 个提交
```

**GitHub 缺失的提交** (`git log github/master..origin/master`):

```
19f2861  Merge pull request 'release: v1.14.0 — 版本号同步 + Skill 数量修正' (#12) from release/v1.14.0 into master
06a0edf  release: v1.14.0 — Phase 1.8 README 检查增强 + Phase 1.14 Forgejo 配置检测
```

状态: **GITHUB MIRROR STALE** — 需补推

---

### 3.3 standards 子模块 `/home/dev/Aria/standards`

```
HEAD                = af300d5    (detached HEAD — superproject 指针)
local master        = 5311ecb    (本地 master 分支落后 HEAD 一个提交)
origin/master       = af300d5    (Forgejo)
github/master       = af300d5    (GitHub)

HEAD vs origin/master          : 0 / 0
HEAD vs github/master          : 0 / 0
origin/master vs github/master : 0 / 0
local master vs origin/master  : 0 behind 1 (本地 master 分支未跟进)
local master vs github/master  : 0 behind 1
```

状态: **两远程同步** (OK) — 但本地 `master` 分支未 fast-forward 到远程, 属独立问题 (非推送漂移).

---

### 3.4 aria-orchestrator 子模块

仅有 `origin` (Forgejo), 无 `github` remote, 不在本次漂移检测范围内.

---

## 4. 结论 — 需要补推的 remote

| 仓库 | 补推命令 | 理由 |
|------|----------|------|
| **aria 子模块** | `git -C /home/dev/Aria/aria push github master` | Forgejo 有 2 个 v1.14.0 发版提交未同步到 GitHub (`19f2861`, `06a0edf`). 这正是 Claude Code 插件市场滞后的根因. |

**不需要补推**:

- 主项目 Aria: 两 remote 已一致.
- standards 子模块: 两 remote 已一致 (本地 master 分支落后属另一问题, 建议 `git -C standards checkout master && git -C standards merge --ff-only af300d5`).
- aria-orchestrator: 无 github remote, N/A.

---

## 5. 与 "Everything up-to-date" 陷阱的对比

如果仅执行:

```bash
git -C /home/dev/Aria/aria push origin master
# => Everything up-to-date
```

`origin` (Forgejo) 确实 up-to-date, 提示**不是错误**, 但会**掩盖** GitHub 落后 2 个提交的事实. 这就是 MEMORY 中 `feedback_git_minus_c_for_submodule_push.md` 与 CLAUDE.md "多远程推送" 章节的警告.

**正确的验证模式**:

```bash
# 1. 先 fetch 所有 remote
git -C <repo> fetch --all

# 2. 对每一对 remote 做三路比较
git -C <repo> rev-list --left-right --count origin/master...github/master

# 3. 非 0/0 即为漂移, 需执行对应 push
```

---

## 6. 修复动作 (建议, 未执行)

```bash
git -C /home/dev/Aria/aria push github master
# 预期推送 2 个提交: 06a0edf, 19f2861
# 推送后再次运行 rev-list --left-right --count origin/master...github/master
# 应返回 0  0
```

---

**扫描结束**. 本次漂移定位: **aria 子模块 → github remote (落后 2 提交)**.
