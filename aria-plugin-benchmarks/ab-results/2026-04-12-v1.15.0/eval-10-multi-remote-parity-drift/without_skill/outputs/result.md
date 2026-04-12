# 多远程同步状态扫描报告

**扫描时间**: 2026-04-12
**工作目录**: /home/dev/Aria
**扫描范围**: 主项目 + aria 子模块 + standards 子模块

---

## 扫描结论

检测到 **1 处 remote 落后** (aria 子模块 → github)。主项目 Aria 和 standards 子模块两端已同步。

---

## 各仓库 Remote 同步状态

### 1. 主项目 Aria (/home/dev/Aria)

| Remote | URL | HEAD SHA | 状态 |
|--------|-----|----------|------|
| origin (Forgejo) | ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git | `5b7a5f7` | 已同步 |
| github (GitHub)  | git@github.com:10CG/Aria.git                 | `5b7a5f7` | 已同步 |
| local HEAD       | (feature/v1.15.0-multi-remote-parity)        | `5b7a5f7` | 与两 remote 一致 |

- origin/master 与 github/master 在同一 commit。
- 本地 feature/v1.15.0-multi-remote-parity 分支有未提交变更 (modified: CLAUDE.md, aria submodule pointer 等)，但与 remote 比对的是 master 分支 HEAD，因此**不存在落后 remote**。

### 2. aria 子模块 (/home/dev/Aria/aria) — 插件仓库，用户发布 v1.15.0 的目标

| Remote | URL | HEAD SHA | 状态 |
|--------|-----|----------|------|
| origin (Forgejo) | ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git | `19f2861` | **领先 github 2 个 commit** |
| github (GitHub)  | git@github.com:10CG/aria-plugin.git                 | `f55e130` | **落后 origin 2 个 commit** |
| local HEAD (feature/v1.15.0-multi-remote-parity) | — | `19f2861` | 与 origin 一致 |

**github/master 缺失的 commits** (`git log github/master..origin/master`)：

```
19f2861  Merge pull request 'release: v1.14.0 — 版本号同步 + Skill 数量修正' (#12) from release/v1.14.0 into master
06a0edf  release: v1.14.0 — Phase 1.8 README 检查增强 + Phase 1.14 Forgejo 配置检测
```

> 说明: 虽然任务描述中用户提到"v1.15.0 子模块更新"，但当前 aria 子模块实际 HEAD 为 `19f2861` (v1.14.0 release merge)。v1.15.0 仍在 feature 分支开发中，尚未合并 master，也尚未打 tag。drift 实际上是 v1.14.0 release 未推到 GitHub。无论哪个版本，修复方式一致。

### 3. standards 子模块 (/home/dev/Aria/standards)

| Remote | URL | HEAD SHA | 状态 |
|--------|-----|----------|------|
| origin (Forgejo) | ssh://forgejo@forgejo.10cg.pub/10CG/aria-standards.git | `af300d5` | 已同步 |
| github (GitHub)  | git@github.com:10CG/aria-standards.git                 | `af300d5` | 已同步 |
| local HEAD (detached) | — | `af300d5` | 一致，工作区干净 |

---

## Drift 矩阵总览

| 仓库 | origin (Forgejo) | github (GitHub) | Drift |
|------|-----------------:|----------------:|:------|
| Aria (主项目)        | 5b7a5f7 | 5b7a5f7 | OK (同步) |
| aria (子模块/插件)   | 19f2861 | f55e130 | **GitHub 落后 2 commit** |
| standards (子模块)   | af300d5 | af300d5 | OK (同步) |

---

## 修复命令

### 必需: 将 aria 子模块 github remote 追上 origin

```bash
# 从 Aria 主项目根目录执行，使用 git -C 避免 cd 链
git -C /home/dev/Aria/aria push github master
```

执行后 github/master 应前进到 `19f2861`，两个 remote 达成 parity。

### 可选验证 (推荐在修复后立即执行)

```bash
# 再次 fetch 并比对两 remote 的 HEAD
git -C /home/dev/Aria/aria fetch origin
git -C /home/dev/Aria/aria fetch github
git -C /home/dev/Aria/aria rev-parse origin/master github/master
# 期望输出两行相同的 SHA: 19f28619f216ff16364591380255165e9e176c50
```

### 无需操作

- 主项目 Aria: origin 与 github 一致，无需推送 master。
- standards 子模块: origin 与 github 一致，无需推送。

---

## 附注 / 运维提示

1. **CLAUDE.md 规则 Source of Truth**: 版本发布检查清单中明确要求"多远程推送 (Forgejo + GitHub)"三步都要执行，本次漏推 github 正是该 checklist 第二步未完成的典型案例。
2. **Memory feedback_git_minus_c_for_submodule_push**: 多仓库 git 操作必须用 `git -C <path>`，本报告中的修复命令已遵循此规则。
3. **"Everything up-to-date" 必须验证**: 执行 `git push github master` 后，务必用 `git rev-parse origin/master github/master` 确认 SHA 一致，而不是只看 push 命令的输出文字。
4. 当 v1.15.0 正式 release 并合入 aria 子模块 master 后，同样的 parity 检查需再跑一次，确保 tag 也推送到两个 remote (`git -C aria push origin v1.15.0 && git -C aria push github v1.15.0`)。
