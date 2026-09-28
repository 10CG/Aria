## 结论先说

**本次扫描没有发现需要补推的 remote。** 主仓和 3 个子模块 (standards / aria / aria-orchestrator) 在 `origin` (Forgejo) 和 `github` 两个 remote 上全部一致, `overall_parity = true`, 所有腿 `evidence_grade = fresh` (scan.py 在 Phase 0.5 刚对 8 条腿逐一 fetch 过, 全部 `fetch_ok = "true"`)。

也就是说, **2026-04-12 那种「Forgejo 已合并、GitHub 没推」的状态在当前仓库里并不存在, 这次扫描复现不出来**。下面说明判断依据, 以及真出现那种状态时 scanner 会报成什么样。

---

📍 **当前状态**
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`, 没有配置 upstream)
- 未提交变更 3 项: `aria`、`standards` (子模块 checkout 与主仓记录的 gitlink 不一致) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 中断状态: 无 (`interrupt.status = none`); 没有进行中的 git 操作
- UPM: 未配置

📊 **变更分析**
- 3 项变更都归为 other (gitlink + benchmark 结果目录), Level 2, 不涉及架构, 没有检出 SKILL.md 改动

📄 **需求状态**
- PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

🏗️ **架构状态**
- `docs/architecture/system-architecture.md` 存在, Active, 最后更新 2026-09-02, 需求链路完整

📋 **OpenSpec 状态**
- 活跃变更 8 个 (都是 approved); 已归档 146; 待归档 0
- ⚠️ 设计未实施 5 个: aria-2.0-m6-cost-model-telemetry (79 天) / m6-e2e-resilience (77 天) / m6-release-closeout (124 天) / m7-agent-lifecycle / m7-fleet-aggregation

🛡️ **审计状态**
- 已启用; 上次审计 post_planning, PASS, 已收敛 (R7, 2026-09-24)

🔧 **自定义检查**
- 16 项全部通过, 0 项失败

🔄 **同步状态 (本次重点)**

多远程一致性 (`sync_status.multi_remote`, 强制检查的 remote = `github`, `origin`):

| 仓库 | 比对的分支 | 本地 HEAD | origin (Forgejo) | github | 结论 |
|------|-----------|-----------|------------------|--------|------|
| 主仓 `.` | feature/handoff-multibranch-subdir-path-fidelity | 4f91772 | 4f91772 相同 | 4f91772 相同 | 一致 |
| standards | feature/handoff-multibranch-subdir-path-fidelity | d86fc91 | d86fc91 相同 | d86fc91 相同 | 一致 |
| aria | feature/handoff-multibranch-subdir-path-fidelity | b181678 | b181678 相同 | b181678 相同 | 一致 |
| aria-orchestrator | master | 237045a | 237045a 相同 | 237045a 相同 | 一致 |

- `overall_parity = true` / `has_pending_push = false` / `has_unreachable_remote = false`
- gitlink 可达性 (`gitlink_integrity[]`): 6 组 (2 remote × 3 子模块) 全部 `ok`, 不存在 orphaned gitlink (即 GitHub 上 `clone --recursive` 不会断)
- 当前分支: 没有 upstream (`reason = no_upstream`)
- 📝 README 版本: aria plugin 1.73.3 与 README 一致

**一个需要你知道的覆盖缺口**: 多远程比对用的是**每个仓库当前 checkout 的分支**。aria 子模块现在停在 feature 分支上, 所以 snapshot 比的是 aria 的 feature 分支, **并没有直接比 aria 的 master** —— 而 04-12 事故恰恰是 master。为了回答你的问题, 我额外读了 scan.py 刚刷新过的本地 remote-tracking ref (只读 `git rev-parse`, 不 fetch, 不替代 snapshot 字段):

| 仓库 | 本地 master | origin/master | github/master |
|------|------------|---------------|---------------|
| 主仓 | c454e35 | c454e35 | c454e35 |
| aria | 1cb3872 | 1cb3872 | 1cb3872 |
| standards | 940cb5b | 940cb5b | 940cb5b |
| aria-orchestrator | 237045a | 237045a | 237045a |

master 在两个 remote 上也全部一致。**结论不变: 没有需要补推的 remote。**

**如果 04-12 的状态真的出现, scanner 会怎么报**:
1. Phase 0.5 (`remote_refresh`) 会先对 github 腿做一次真 fetch, 所以不会像 `git push` 回执 "Everything up-to-date" 那样只看自己推的那个 remote 就算通过。
2. 本地 master 已跟上 Forgejo、GitHub 落后 → 从本地视角看 github 那条是 `parity = ahead` (本地比 github 多出合并提交), 会置 `has_pending_push = true`, 在同步区显示「github 待推送」。
3. **注意**: 按推荐规则, 单纯的 `ahead` 算「正常待推送」, 不会把 `overall_parity` 置 false, 也就不会触发 `multi_remote_drift` 告警 —— 它只在同步区露出, 不会升级成红色警告。所以这种场景要看 `has_pending_push` 和每条 remote 的 `parity`, 不能只看 `overall_parity`。
4. 如果主仓随后把 gitlink bump 到 GitHub 上并不存在的 aria 提交并推上了 GitHub, `gitlink_integrity` 会对 (github, aria) 报 `orphaned`, 这一项**会**让 `overall_parity = false`, 并给出 `git -C aria push github <branch>` 的补推建议。
5. 再加上第 1 点提到的缺口: 如果出事的是 master 而子模块 checkout 停在别的分支上, 第 2 点的比对**看不到**; 只有第 4 点的 gitlink 可达性检查能兜住 (前提是主仓已经发布了引用那个提交的 gitlink)。

🎫 **Open Issues**
- 49 个 open issue, 最近的: #221 (secret-guard 进程列举旁路, bug) / #220 (latest.md History prepend 无机械核验) / #219 (进度状态只读接口) / #218 (state-scanner handoff 按 mtime 判最新, bug) / #217 (session-closer GBK 编码崩溃, bug)

🔄 **交接 / 多终端提示**
- 最新 handoff: `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (距今约 60 小时, 来源 = pointer)
- 多分支 track 碰撞: `self_multi_container` (identity 023236f2 / bfe8285d 同时出现在 simonfish 和 aria-runner-bot 名下)。之后如果进 Phase B, 编排层会先调用 phase1_gate 做 advisory 认领; 本次评测按约束**没有执行**, 要执行的命令是:
  ```
  python3 <plugin>/skills/state-scanner/scripts/phase1_gate.py --raw-track-id "<handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria
  ```
  如果本会话持有 active claim, 每次扫描还会调用一次心跳 (`phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path /home/dev/Aria`), 这次同样没有执行。

🎯 **推荐工作流**

remote 全部一致, 不需要补推。建议的选项:

- **[1] (推荐) 不做任何推送, 仅记录结论**: 所有 remote 都一致, 04-12 状态在当前仓库复现不出来。理由: `overall_parity = true`, 所有腿都是 fresh, master 在两个 remote 上也一致。
- **[2] 在隔离副本里构造 04-12 场景做真复现**: 在 scratchpad 里 `git clone` 一份 aria, 配两个本地 bare 仓当 origin/github, 只往 origin 推合并提交, 然后对副本跑 scan.py, 核对 github 腿是否报 `parity = ahead` + `has_pending_push = true`。不碰真仓库, 也不碰真 remote。
- **[3] 把「只比当前分支」这个覆盖缺口开 issue**: 建议 multi_remote 在子模块不在 master 时额外比对默认分支 (或者对 `has_pending_push` 的腿也出告警), 否则 04-12 类事故在子模块停在 feature 分支时只能靠 gitlink 可达性检查兜底。走 `/aria-report` 或 issue-triage 先查重。
- **[4] 回到当前 feature 分支的正常收尾**: 处理 3 项未提交变更 (aria / standards gitlink + AB 结果目录), 走 C.1 提交 (Level 2, 跳过 A 阶段 spec 创建, 因为 #195 spec 已在进行中)。

也可以自定义组合, 例如「[2] + [3]」。
