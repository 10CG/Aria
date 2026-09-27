# 状态扫描结果 (state-scanner v3.1.1)

**Step 0**: `scan.py` 退出码 **0** (全部采集成功, `errors[]` 为空)。扫描开头的 Phase 0.5 `remote_refresh` 已对 origin / github 两个远程、主仓 + 3 个子模块共 8 路全部 fetch 成功 (`fetch_ok=true`, 远程引用约 1 分钟前刚刷新), 所以下面的比较都基于最新的远程引用。

## 先回答你的问题

**结论: 你的 feature 分支没有配置 upstream, 所以扫描器给不出「落后 upstream」的数; 但主分支确实有 12 个你没拿到的新提交。`git pull` 解决不了这个问题, 不建议执行。**

分三点说:

1. **扫描器给的 upstream 结果**: `sync_status.current_branch` = `upstream_configured: false`, `reason: "no_upstream"`, `ahead/behind: null`。也就是: 本地分支 `feature/handoff-multibranch-subdir-path-fidelity` 没有跟踪任何远程分支, 所以 ahead/behind 按规范置为 null (不是 0, 是「算不出来」)。`branch_behind_upstream` 规则 (落后 >= 5 才触发) 因此不触发。
2. **feature 分支与它在远程上的同名分支**: 多远程检查显示主仓本地 HEAD `4f91772` 与 origin、github 上的同名分支**完全一致** (`parity=equal`, `evidence_grade=fresh`, `overall_parity=true`)。所以就算你给它设了 upstream, 也是 0 落后 —— 远程上的这个分支没有别人的新提交。
3. **相对主分支 (这才是你关心的)**: 快照本身不比较「feature 与 master」, 下面这条是我在扫描之后补做的只读核对 (用的是扫描刚 fetch 的引用, 没有改动任何东西):

```
git rev-list --left-right --count HEAD...origin/master   →  13   12
                                     (github/master 结果相同: 13  12)
```

   即: 你的分支比 master 多 13 个提交, **master 比你的分支多 12 个提交** —— 两边已经分叉。分叉点是 `a52b5eb` (2026-09-25), master 上新增的 12 个提交全是文档类:
   - `docs/handoff/` 下 3 份新 handoff + `docs/handoff/latest.md` 指针更新
   - `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` (owner 2026-09-27 裁定单)
   - `.aria/notes/2026-09-17-199-a2-a3-tooling/` 派单与执笔报告
   - `.aria/state-checks.yaml` (`0ed4a31` 修复: 占位符检查与 CLAUDE.md 检查改为失败即关)
   - 1 份 post_planning 审计报告

   你的分支在分叉后只改了一个文件 `openspec/changes/handoff-multibranch-subdir-path-fidelity/verification-ledger.md`, 两边**没有任何重叠文件**, 合进来基本不会冲突。

**为什么不建议 `git pull`**: 当前分支没有 upstream, 直接 `git pull` 会报 "There is no tracking information for the current branch" 然后什么都不做; 即使设了 upstream, 拉的也是 origin 上的**同名 feature 分支** (已经一致), 不会把 master 的改动带进来。远程引用扫描时已经 fetch 过, 也不需要再手动 fetch。

## detached HEAD / 浅克隆 场景

本次两种情况**都不存在**: `git.detached_head=false`, `git.shallow=false`, `sync_status.shallow=false`, 且没有暂停中的 git 操作 (`git_operation_in_progress.operation=none`)。

若以后遇到, 扫描器的处理方式和对应做法如下:

| 场景 | 快照表现 | 含义 | 建议做法 |
|------|----------|------|----------|
| detached HEAD | `current_branch.name=null`, `reason="detached_head"`, ahead/behind 为 null, 多远程 `parity="unknown"` | 不在任何分支上, 不存在 upstream 可比 | 先 `git switch <你的分支>` 回到分支再扫; 不要在 detached 状态下 pull |
| 浅克隆 | `shallow=true`, `reason="shallow_clone"`, behind 为 null, 多远程 `parity="unknown"` | 历史不完整, 计数不可靠, 所以不给数字 (null 不等于 0) | `git fetch --unshallow` 补全历史后重扫 |
| 无 upstream (本次情况) | `reason="no_upstream"`, ahead/behind 为 null | 分支没跟踪远程分支 | 可 `git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity`; 与 master 的差距要另外比 |
| rebase/merge 暂停中 | `git_operation_in_progress.operation != none` | detached_head 仍可能是 false, 需单独看这个字段 | 先 `git <op> --continue` 或 `--abort`, 再做任何分支操作 |

---

## 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`)
- 模块 / Phase·Cycle: UPM 未配置 (`upm.configured=false`)
- 变更文件: 3 (未暂存 2: `aria`、`standards` 子模块指针; 未跟踪 1: `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`)
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity`
- 中断检测: `interrupt.status=none` (无 workflow-state 需要恢复)

## 变更分析
- 类型: other x3 (子模块指针 + 基准结果目录), 无代码 / 测试文件
- 复杂度: Level 2 | 架构影响: 否 | Skill 变更: 未检出

## 需求状态
- PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

## 架构状态
- `docs/architecture/system-architecture.md` 存在, Active, 最后更新 2026-09-02, 需求链路完整

## OpenSpec 状态
- 活跃变更含本分支对应的 `handoff-multibranch-subdir-path-fidelity`; 归档与待归档明细见快照 `openspec` 段 (本次问题不涉及, 从略)

## 审计状态
- 审计已启用; 最近一次: post_planning R7 (2026-09-24), verdict **PASS**, 已收敛

## 自定义检查
- 16 项全部通过, 0 失败
- 注意: master 上 `0ed4a31` 修改了 `.aria/state-checks.yaml` (两项检查改为出错即失败)。你的分支还是旧版检查, 合入 master 后这两项的结论可能变化, 合入后建议重扫一次。

## 同步状态
```
当前分支: feature/handoff-multibranch-subdir-path-fidelity (upstream 未配置)
远程引用: 1m 前同步
  当前分支无 upstream 配置, 无法计算 ahead/behind
  如需配置: git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity
  [补充核对] 相对 origin/master: 本分支领先 13 / 落后 12 (已分叉, 无重叠文件)
多远程一致性:
  主仓库: 所有远程一致 (origin, github) @ 4f91772
  aria 子模块: 所有远程一致 (origin, github) @ b181678
  standards 子模块: 所有远程一致 (origin, github) @ d86fc91
  aria-orchestrator 子模块: 所有远程一致 (origin, github) @ 237045a
  gitlink 完整性: 6/6 ok
子模块:
  aria:      工作区检出 b181678, 主仓记录 1cb3872 (工作区与记录不一致, 未提交的指针变更)
  standards: 工作区检出 d86fc91, 主仓记录 940cb5b (同上)
  aria-orchestrator: 同步
```
- 子模块说明: `aria` 与 `standards` 都检出在同名 feature 分支上 (补充核对: 分别比各自 master 多 9 / 2 个提交, 落后 0), 主仓还没提交新的 gitlink —— 这就是 `git status` 里 ` M aria` / ` M standards` 的来源, 不是落后远程。按项目约定, 子模块要先本地合并进 master 并双推, 主仓再提交 gitlink。
- README 版本一致 (1.73.3); Forgejo 配置文件缺失 (`forgejo_config.config_status=missing`, 可用 `/forgejo-sync` 引导创建, 与本问题无关)。

## Open Issues
- issue 扫描已启用, 最新几条: #221 secret-guard 进程列举旁路、#220 latest.md History prepend 无机械核验、#219 进度只读机读接口、#218 handoff 无指针时按 mtime 判最新 等 (均为启发式关联, 未链到本分支)

## 交接 (handoff awareness)
- 本分支上的最新 handoff: `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (经 latest.md 指针, 约 60 小时前)。
- **注意**: master 上已有 3 份更新的 handoff (2026-09-25 / 09-26 / 09-27) 和更新过的 `latest.md`, 其中 09-27 那份记录了本 feature (10CG/Aria#195) 的 TASK-025 收尾。你在本分支上读到的「最新交接」是过期的, 继续干活前建议用 `git show origin/master:docs/handoff/latest.md` 看 master 上的最新指针。

## 多终端协调提示
- `tracks_multibranch.collision.kind = self_multi_container`: 同一 owner 在多个容器 (simonfish 与 aria-runner-bot) 下有同名轨道记录 (标识 `023236f2`、`bfe8285d`)。这是提示级告警, 不阻断。
- 若你接下来确认进入 Phase B, 按流程会在进入前调用认领闸门 (本次只读, **未执行**):
  ```
  python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "<最新 handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria
  ```

---

## 推荐工作流

**[1] 把 master 合进 feature 分支 (推荐)**
- 步骤: `git merge origin/master` (本地合并, 两边无重叠文件, 预计无冲突) → 重跑 `/state-scanner` 确认自定义检查仍全绿 → 双推 feature 分支后分别 `git ls-remote origin` / `git ls-remote github` 核对 SHA
- 理由: master 的 12 个新提交里有新的 state-checks 规则和本 feature 的后续 handoff, 尽早拿到能避免按旧信息工作; 分支已推到两个远程, 用 merge 不需要改写历史

**[2] 改用 rebase 到 origin/master**
- 步骤: `git rebase origin/master` → 需要 `git push --force-with-lease` 到 origin 和 github 两个远程
- 后果: 历史更直, 但要强推已经发布的分支; 按项目多远程规范, 强推前要先做 ls-remote 核验, 风险高于选项 1

**[3] 暂不同步, 继续开发, 到 Phase C 合并前再处理**
- 理由: 两边无文件重叠, 现在不合也不会越积越难; 但要记得本分支的 handoff 和 state-checks 是旧的

**[4] 只配置 upstream**
- 步骤: `git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity`
- 作用: 以后扫描能直接给出 ahead/behind; 但它比较的是远程同名分支, **不会**告诉你 master 的新改动

**跳过项**: `git pull` (原因见上); `git fetch --unshallow` (不是浅克隆)。

请回复编号 (或自定义组合) 确认。以上所有 git 操作都需要你本人执行或确认, 我不会代你修改分支。
