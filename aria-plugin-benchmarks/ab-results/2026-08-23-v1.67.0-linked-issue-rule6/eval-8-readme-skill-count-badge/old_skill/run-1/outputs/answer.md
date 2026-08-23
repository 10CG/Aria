# 项目状态扫描 (state-scanner v3.1.1, scan.py exit 10)

> scan.py 退出码 10 = 部分软错误, snapshot 可用。唯一软错误: `snapshot_consistency` 对 164 条 handoff track 的 AC-5 远端核验 (github remote) git 命令失败, 因此 `overall_parity=true` 这一条**按未验证处理**, 其余区块不受影响。

## 先纠正一个前提

你说的「刚发布 v1.14.0、新增 3 个 Skill」与仓库实际不符:

| 数据源 | 实际值 |
|--------|--------|
| `aria/.claude-plugin/plugin.json` (版本 SOT, 当前 worktree) | **1.66.4** |
| aria 远端 origin/master + github/master (a0fe720) | **1.66.5** (刚由 #152 轨合并, 本地 aria checkout 落后 15 commit) |
| 主仓 README badge (`README.md:8`) | `Plugin-v1.66.4` |
| 主仓 README 文字版本行 (`README.md:242`) | `1.66.4 (aria-plugin, 42 Skills + 11 Agents)` |

v1.14.0 是很久以前的版本 (git-remote-helper 在 v1.15.0 加入)。下面的检查都按**真实现状**做, 不按 v1.14.0 的假设。

## 📍 当前状态

- 分支: `feature/linked-issue-normalization` (upstream origin 同名, ahead 0 / behind 0, 证据等级 fresh)
- 工作区: `M aria` (子模块 workdir 0fe2e0d 在 feature 分支上, 领先 gitlink 9e6a17c) + 1 个未跟踪 AB 结果目录; 无 git 中间态操作, 无工作流中断 (`interrupt=none`)
- UPM: 未配置 (本项目不用 UPM, 属已知)
- 关联 OpenSpec: `openspec.active` 为空, 待归档 0

## 📊 变更分析

- 变更 2 个文件, 类型 other (子模块指针 + 未跟踪目录), Level 1, 无架构影响, 无 Skill 变更检出 (AB 状态: 无需 benchmark)

## 📄 需求状态 / 🏗️ 架构状态

- PRD: v1 Active / v2 Approved (snapshot 归一为 pending, 属 Status 字段格式问题, 非真实滞后)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1
- 架构文档存在 (2026-05-27, 88 天), `chain_valid=false`: 文档没有 `parent_prd` 链接, 需求链路不完整 (老问题, 与本次无关)

## 🛡️ 审计状态

- 审计系统 enabled; 最近审计轨迹 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (post_planning R5 两席 FAIL 后 owner override 进 Phase B, Rule #10 已留痕, 见最近提交 826b356)

## 🔧 自定义检查: 10/10 通过

与你关心的三项直接相关的两条:

- `m6-version-badge-match`: OK, badge=1.66.4 与 plugin.json 一致
- `i18n-readme-translation-currency`: OK, 3 个 i18n README 均在 1.66.4

## 你点名的三项核对 (scan 之后我直接读了 README / plugin.json / skills 目录)

### 1. Skill 数量 — 一致

- 实际目录: `aria/skills/` 下 42 个含 `SKILL.md` 的目录 (另有 `issue-triage-workspace/` 是被 `.gitignore` 忽略的 benchmark 残留, 不是 Skill; `run_all_tests.sh` 是脚本)
- 其中 `user-invocable: false` 的内部 Skill 7 个: agent-router, agent-team-audit, arch-common, aria-token-telemetry, audit-engine, config-loader, git-remote-helper
- `aria/README.md:44`「35 user-facing + 7 internal = 42 total」、主仓 `README.md:133/222/242`、`plugin.json` description「42个 Skills (35+7)」— 四处数字全部一致, 也与目录一致。**数量没问题。**

### 2. Skill 列表完整性 — aria/README.md 漏了 2 个

把 `aria/README.md` Skills 区块的 bullet 列表与目录逐项比对:

- bullet 共 40 条 (含 7 个内部 Skill 重复出现在 bullet 里), 对应 33 个 user-facing
- **目录里有、列表里没有 (user-facing)**: `issue-triage`、`session-closer`
- 列表里有、目录里没有: 无

也就是「35 user-facing」这个总数写对了, 但枚举列表只列了 33 个, 漏了 2 个 (不是 3 个)。`session-closer` 是 v1.50.0 加入, `issue-triage` 更早, 两者在 aria/README.md 里一次都没出现。

主仓 `README.md` 的分类表已含 `issue-triage` (第 142 行 Requirements & Issues), 但同样**没有 `session-closer`**。

### 3. Plugin badge 版本 — 与当前 plugin.json 一致, 但远端已经是 1.66.5

- 主仓 badge `v1.66.4` = 主仓 gitlink 指向的 plugin.json (1.66.4) = 当前 aria workdir plugin.json (1.66.4)。**就当前 checkout 而言一致**, custom check 也是绿的。
- 但 aria 远端 master 已合并 v1.66.5 (`f90881b chore(release): v1.66.5`)。主仓还没 bump gitlink 到 a0fe720, 所以 badge / `README.md:242` / 主仓 VERSION / i18n README 下一步都要随 gitlink bump 一起升到 1.66.5。这不是「badge 漏改」, 而是「发布同步面尚未做到主仓」— 属 #152 轨的 Phase D 收尾项, 不是本轨的事。

## 🔄 同步状态

- 当前分支与 origin 持平
- 子模块 `standards`: 与远端一致
- 子模块 `aria`: workdir 与 gitlink 不同 (本轨 feature 分支), 远端 master 领先本地 15 commit (提示 `git submodule update --remote aria`, 但你在 feature 分支上**先别动**, 等本轨合并时 rebase/merge 处理)
- 多远程 parity: 报 true, 但因 github remote 核验命令失败, **视为未验证** (软错误)

## 🌲 多终端协同

`tracks_multibranch.collision.kind = self_multi_container`: 同一 owner 在多个容器有活动轨 (dev-claude / aria-runner-bot 等)。按 SKILL 约定, 进 Phase B 时应走 phase1_gate advisory claim; 本次是只读扫描, 未调用。

## 🎯 推荐工作流

实际发现的是一个**文档漏项**: `aria/README.md` 缺 `issue-triage`、`session-closer` 两条 (主仓 README 缺 `session-closer`)。数量、badge 都没错。

- **[1] 推荐: Level 1 文档修复 (quick_fix, 置信度 ~85%)**
  - 在 aria 子模块 `aria/README.md` Skills 列表补两条 (issue-triage 归「Requirements & Issues」类, session-closer 归「Ten-Step Cycle Core」旁的会话收尾类), 同步主仓 `README.md:142` 附近的分类表补 `session-closer`, 并跟 i18n README 同步 (仅正文实质变更才重译, #140 B 档 — 这是列表补项, 要同步)
  - 步骤: B.1 新分支 (aria 子模块, 合并走本地 merge + 双推, 不用 Forgejo 服务端 merge) → C.1 提交 `docs(readme): ...` → C.2 PR
  - 跳过: A.1-A.3 (Level 1 免 OpenSpec), Rule #6 benchmark (README 不是 Skill 指令面, 不影响 AI 行为)
  - 注意: 你当前在 `feature/linked-issue-normalization` 上, 且 aria 远端已是 1.66.5。建议从 aria `origin/master` (a0fe720) 切新分支做这个修复, 不要混进 linked-issue 轨; 发布时随下一 PATCH 一起带出
- **[2] 并入 #152 轨的 Phase D 收尾**: 主仓 gitlink bump 到 1.66.5 + badge / VERSION / i18n 同步时顺手把这两条补上 (少开一个 PR, 但依赖那条轨的进度)
- **[3] 仅记录不动手**: 把漏项写进本轨 handoff 的待办, 继续 linked-issue-normalization 的 Phase B
- **[4] 自定义组合**

选 [1] 的话我会先确认分支基点再开始; 本次扫描为只读, 未触碰任何文件或 workflow-runner。
