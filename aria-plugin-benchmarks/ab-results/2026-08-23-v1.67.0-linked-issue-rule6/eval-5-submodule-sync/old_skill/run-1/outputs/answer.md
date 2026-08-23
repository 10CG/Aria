## 状态扫描结果 (state-scanner v3.0, scan.py 机械采集)

`scan.py` 退出码 **10** (部分软错误, snapshot 可用)。唯一软错误来自 `snapshot_consistency` collector: 它对 164 条 legacy handoff track 在 `github` 远程上做 AC-5 核验时 git 命令失败, 因此它声明「本次 `overall_parity=true` 的判决视为未经核验」。这不影响下面子模块 ahead/behind 的直接数据 (那部分由 `remote_refresh` + `sync` collector 独立采集, 8 条 fetch leg 全部成功, 证据等级 `fresh`, 远程 refs 年龄 1 分钟)。

### 1. 当前状态
- 分支: `feature/linked-issue-normalization` (主仓, HEAD `826b356`), 无 git 中间态操作, 无中断的 workflow
- 未提交变更 2 项: `aria` 子模块指针 (unstaged) + 本次 AB 结果目录 (untracked)
- 活跃 OpenSpec: 0 (snapshot 未识别到活跃 change); UPM 未配置

### 2. 变更分析
- 复杂度 Level 1, 2 个文件 (均为 other 类), 无代码/测试变更, 无架构影响, 未检出 SKILL.md 变更

### 3. 需求状态
- PRD v1 Active / PRD v2 Approved (归一为 pending); User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 4. 架构状态
- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27; 需求链路 `chain_valid=false` (parent_prd 缺失)

### 5. OpenSpec 状态
- 活跃 0 / 已归档大量历史项 / 无待归档

### 6. 审计状态
- enabled; 上次审计产物 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (verdict 字段未解析出)

### 7. 自定义检查
- 10 passed / 0 failed (版本 badge 1.66.4 一致 / i18n README current / CLAUDE.md 无 changelog / coordination gate 近期有 4 次真实调用 等)

### 8. 同步状态 (你最关心的部分)

**主仓** `feature/linked-issue-normalization` vs `origin`: ahead 0 / behind 0, 一致。`github` 远程无本地跟踪 ref (parity unknown, 是 feature 分支没推 github, 正常)。

**三个子模块 (远程已 fetch 刷新, 证据 fresh)**:

| 子模块 | 工作区 HEAD | 主仓 gitlink 记录 | 远程 master | 落后远程 | 结论 |
|--------|-------------|-------------------|-------------|----------|------|
| `standards` | `334c609` (detached) | `334c609` | `334c609` | 0 | 同步 |
| `aria-orchestrator` | `237045a` (master) | `237045a` | `237045a` | 0 | 同步 |
| `aria` | `0fe2e0d` (feature/linked-issue-normalization) | `9e6a17c` | `a0fe720` | **15 commits** | **落后, 见下** |

`aria` 子模块的具体情况 (snapshot 给出 `tree_vs_remote=true`, `workdir_vs_tree=true`, hint: `git submodule update --remote aria`):
- 主仓记录的 gitlink `9e6a17c` 落后 `origin/master` (`a0fe720`) 15 个 commit —— 这就是协作者推的更新: `feature/152-no-run-for-branch` 合入 + `chore(release): v1.66.5` (aria-plugin #152 pre-merge gate 零 run 显影)。
- 工作区 HEAD `0fe2e0d` 是你自己的 feature 分支, 在 `9e6a17c` 之上多 2 个 commit (linked-issue 归一化 TASK-001..012), 且已推到 `origin/feature/linked-issue-normalization` (ahead 0 / behind 0, 工作区干净)。它**不包含** `a0fe720` 那 15 个 commit (不是祖先关系, 两边已分叉)。
- gitlink 完整性: `origin` 上三个子模块均 `ok`; `github` 上为 `no_published_ref` (feature 分支未发布到 github, 非孤儿指针)。

### 9. Open Issues
- 最新 fetch (06:24Z) 可见 Aria #188 `[bug] 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md`, 与本次 scan.py 的 exit 10 软错误和 UPM 未配置现象吻合。

### 10. 推荐

**要不要 `git submodule update`?** —— 回答: **不要直接跑 `git submodule update` (不带 `--remote`)**, 也**不建议现在裸跑 `git submodule update --remote aria`**。

原因: `standards` / `aria-orchestrator` 已与远程一致, 什么都不用做。只有 `aria` 落后, 但你在 `aria` 里正站在自己的 feature 分支上, 带着 2 个已推送的 commit:
- `git submodule update` (默认 checkout 模式) 会把 `aria` 重置回 gitlink `9e6a17c`, 丢掉你分支上 2 个 commit 的检出 (commit 还在远程, 但工作区会退回旧版本), 而且那个 `9e6a17c` 本身就比远程还旧, 解决不了「落后」。
- `git submodule update --remote aria` 会把 `aria` 切到 detached `a0fe720`, 同样离开你的 feature 分支; 你的 2 个 commit 仍未和那 15 个 commit 合并。

建议按下面顺序做 (只给命令, 不替你执行):

[1] **推荐**: 在 `aria` 子模块里把远程 master 合进你的 feature 分支, 再按约定更新主仓 gitlink
```bash
git -C aria fetch origin                       # scan 已 fetch 过, 重跑无害
git -C aria merge origin/master                # 把 #152 v1.66.5 的 15 个 commit 合进 feature/linked-issue-normalization
git -C aria push origin HEAD:feature/linked-issue-normalization
git add aria && git commit -m "chore(submodule): bump aria gitlink (merge origin/master v1.66.5 into linked-issue-normalization)"
```
合并时留意 `state-scanner` 相关文件 (你改的 `linked_issue` 归一化 vs 对方改的 `phase-c-integrator` / `workflow-runner`, 文件面不同, 冲突概率低)。

[2] 只想先看远程变了什么, 不动工作区:
```bash
git -C aria log --oneline 9e6a17c..origin/master
```

[3] 若你确定要放弃 feature 分支检出、只把子模块对齐远程 master (一般不建议): `git submodule update --remote aria`, 之后需要重新 `git -C aria checkout feature/linked-issue-normalization` 才能继续你的工作。

另外两点提醒:
- 主仓 gitlink 现在指向 `9e6a17c` 而工作区在 `0fe2e0d`, 所以 `git status` 一直显示 `aria` 为 modified; 这是你分支自己的待提交项, 与远程落后是两回事, 做完 [1] 一并解决。
- scan.py exit 10 的软错误 (164 条 legacy track AC-5 核验失败 + 对 `overall_parity=true` 的保留) 已有 Aria #188 跟踪, 本次不影响子模块同步判断。
