# 项目状态扫描 + README Skill 一致性检查

扫描方式: `scan.py` 机械采集 (退出码 0, `errors[]` 为空, snapshot schema 1.0, 生成于 2026-09-27T17:09:29Z)。README 的 Skill 数量 / 列表比对不在 scan.py 采集范围内, 是扫描成功后我另外读 README 和 `aria/skills/` 目录做的比对 (只读, 没改任何文件)。

---

## 先说结论 (你的前提有一处对不上)

**仓库里的 aria-plugin 不是 v1.14.0, 是 v1.73.3。**

- `aria/.claude-plugin/plugin.json` 的 `version` = `1.73.3` (版本 SOT)
- `aria/CHANGELOG.md` 最新条目 = `[1.73.3] - 2026-09-13`; `[1.14.0]` 是 2026-04-12 的旧条目
- aria 子模块当前 HEAD `b181678` = `v1.73.3` 之后 9 个提交, 全是 `10CG/Aria#195` 的 state-scanner 改动, **没有新增任何 Skill 目录**
- 本地 tag 里也没有 `v1.14.0`

所以「刚发布 v1.14.0、新增 3 个 Skill」在这个工作区里找不到对应物。可能是: 你说的是别的仓库 / 别的 checkout, 或者版本号记错了。下面的检查结果按仓库真实状态 (v1.73.3) 给出。

三项检查的结果:

| 检查项 | 结果 |
|--------|------|
| README 中 Skill **数量** vs 实际目录 | 一致: 42 = 35 user-facing + 7 internal |
| README 中 Skill **列表**是否完整 | **不完整**: 漏 2 个 (见下) |
| plugin badge 版本 vs plugin.json | 一致: 都是 1.73.3 |

---

## 1. 当前状态

- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (即 `10CG/Aria#195` 那条轨), 无 upstream 跟踪
- 最近提交: `4f91772 docs(openspec): 10CG/Aria#195 台账记 owner 2026-09-27 裁定与 feature 双推`
- 未提交变更 3 处: 子模块指针 `aria` (1cb3872 -> b181678)、`standards` (940cb5b -> d86fc91) 未暂存; 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- git 中间态: 无 (没有暂停中的 rebase / merge)
- 中断恢复: 无 (`.aria/workflow-state.json` 不存在)
- UPM: 未配置 (本仓本来就没有运行时 UPM)
- 上次 handoff: `2026-09-24-session-close-199-post-planning-converged.md` (60.3h 前, via pointer)。它的 §6 入口写的是: 先查 claim 心跳年龄; `#195` (就是当前分支这条) 当时 `yielded`、B.1 待起, 是 `#199` 的入口前置; 不要擅自推送。当前分支上已有 `#195` 组 3/组 4 完成的提交, 说明那之后已经有人接手推进了。

## 2. 变更分析

- 变更类型: code 0 / test 0 / docs 0 / config 0 / other 3 (全是子模块指针 + AB 结果目录)
- 复杂度: Level 2 (scan.py 判定)
- 架构影响: 无; SKILL.md 变更: 未检出 (所以不需要 Skill 变更 AB 状态块)

## 3. 需求状态

- 已配置; PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

## 4. 架构状态

- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-09-02, 需求链路完整 (v1 + v2 两份 PRD)

## 5. OpenSpec 状态

- 活跃变更 8 个, 全部 approved: `aria-2.0-m6-cost-model-telemetry` / `aria-2.0-m6-dispatch-input-delivery` / `aria-2.0-m6-e2e-resilience` / `aria-2.0-m6-release-closeout` / `aria-2.0-m7-agent-lifecycle` / `aria-2.0-m7-fleet-aggregation` / `handoff-multibranch-subdir-path-fidelity` / `pre-merge-completeness-gate-change-scope`
- 已归档 146 个; 待归档 0 个
- 设计未实施: 5 个 (approved 但长期未开工): m6-cost-model-telemetry 79 天 / m6-e2e-resilience 77 天 / m6-release-closeout 124 天 / m7-agent-lifecycle 100 天 / m7-fleet-aggregation 70 天

## 6. 审计状态

- 审计系统已启用; 上次审计: `post_planning` R7, PASS, 已收敛 (2026-09-24, `pre-merge-completeness-gate-change-scope`)

## 7. 自定义检查

16 项全部通过, 0 失败。跟你这次问题直接相关的几项:

- `m6-version-badge-match`: OK, badge=1.73.3 (主项目 README 的 Plugin badge 与 plugin.json 一致)
- `i18n-readme-translation-currency`: OK, 3 份 i18n README 都标记为 @ 1.73.3
- `plugin-version-arch-docs-match`: OK, 2 处架构文档版本行一致
- `plugin-cache-currency`: OK, 已安装插件缓存 = 1.73.3
- `main-project-version-consistency`: OK, 主项目 1.7.5, 9 处引用一致

**注意: 没有任何一项自定义检查覆盖「README 的 Skill 列表是否完整」**, 所以下面那个漏项在全绿之下一直没被发现。

## 8. 同步状态

- 当前分支: 无 upstream (`no_upstream`), ahead/behind 无法计算
- 多远程 parity: `overall_parity = true`。主仓 `4f91772` 在 origin / github 两端一致; 子模块 standards `d86fc91` / aria `b181678` / aria-orchestrator `237045a` 两端都一致; gitlink 完整性 6/6 为 ok
- README 版本一致性: `aria/README.md` 的 readme_version = 1.73.3 = plugin_version, `version_match = true`
- 插件依赖: standards 子模块已注册且已初始化
- Forgejo 配置: 检测到 forgejo remote, 但 `forgejo_config` 缺失 (可用 `/forgejo-sync` 引导创建)

### README Skill 数量 / 列表 / badge 详细比对

**实际目录**: `aria/skills/` 下有 44 个条目, 其中:
- 42 个是带 `SKILL.md` 的 Skill 目录
- `run_all_tests.sh` 是脚本, 不算
- `issue-triage-workspace/` 没有 `SKILL.md`, 不算 Skill
- 42 个里 `user-invocable: false` 的正好 7 个: agent-router / agent-team-audit / arch-common / aria-token-telemetry / audit-engine / config-loader / git-remote-helper -> 35 + 7 = 42

**数量声明 (全部与实际一致)**:

| 位置 | 写的是 | 对不对 |
|------|--------|--------|
| `aria/.claude-plugin/plugin.json` description | 42 个 Skills (35 user-facing + 7 internal) | 对 |
| `aria/README.md` 第 7 行 + `### Skills` 标题 | 35 + 7 = 42 | 对 |
| 主项目 `README.md` `### Skills` 标题 / 目录树 / 版本块 | 42 | 对 |
| `README.zh.md` / `README.ja.md` / `README.ko.md` | 42 | 对 |

**列表完整性 (有漏项)**:

| 文件 | 列出的 Skill | 漏掉的 |
|------|--------------|--------|
| `aria/README.md` | 40 个 | `issue-triage` (v1.20.0 新增)、`session-closer` (v1.50.0 新增) |
| `aria/README.zh.md` | 同上 | `issue-triage`、`session-closer` |
| 主项目 `README.md` 的 Skills 表 | 41 个 (34 user-facing + 7 internal) | `session-closer` |
| `README.zh.md` / `README.ja.md` / `README.ko.md` | 同上 | `session-closer` |

也就是说: 标题写 42, 但列表里实际只数得出 40 (插件 README) 或 41 (主项目 README)。这两个 Skill 分别是好几个版本之前加的, 不是这次发版造成的。

**顺带发现的两处小的标注不一致** (`aria/README.md`):
- `agent-router` 在 frontmatter 里是 `user-invocable: false`, 顶部 internal 名单里也有它, 但在「Dev Tools」列表里没有标 *(internal, non-user-invocable)*, 其他 internal Skill 都标了
- `agent-team-audit` 也是 internal, 列表里只标了 *(disabled by default...)*, 没标 internal

**badge / 版本**:
- 主项目 `README.md` 第 8 行 badge: `Plugin-v1.73.3` = plugin.json `1.73.3`, 一致
- 主项目 `README.md` 版本块: `Plugin Version: 1.73.3 (aria-plugin, 42 Skills + 11 Agents)`, 一致
- `aria/README.md` 第 5 行: `**Version**: 1.73.3 | **Released**: 2026-09-13`, 与 plugin.json 和 CHANGELOG 一致

所以你担心的「badge 还是旧的」在当前仓库里不成立; 真正的问题是 Skill 列表漏项。

## 9. Open Issues

- open 共 49 个: 10CG/Aria 20 / 10CG/aria-plugin 20 / 10CG/aria-standards 7 / 10CG/aria-orchestrator 2; 带 bug 标签 4 个
- 最新几条: `#221` secret-guard 进程列举旁路 (bug) / `#220` latest.md History prepend 声明问题 / `#219` 只读机读进度接口 / `#218` handoff 无指针时按 mtime 判最新

## 10. 推荐工作流

**先要注意的背景**: 当前工作区在 `#195` 的 feature 分支上, 还有未提交的子模块指针和未跟踪的 AB 结果目录; `tracks_multibranch.collision.kind = self_multi_container` (同一 owner 两个容器 `simonfish/023236f2` 与 `simonfish/bfe8285d` 都在活动)。README 修复是跟 `#195` 无关的文档修复, **不应该混进这条分支**, 也不要在这个脏工作区里直接 checkout 切分支。

**[1] (推荐) Level 1 文档修复, 单独走一条小轨**
- 内容:
  - `aria/README.md` + `aria/README.zh.md`: 在对应分类补上 `issue-triage` 和 `session-closer`; 顺手给 `agent-router`、`agent-team-audit` 补 internal 标注
  - 主项目 `README.md` + 3 份 i18n: Skills 表补 `session-closer` (属于正文实质变更, 按 #140 B 档 i18n 要同步)
- 步骤: B.1 (aria 子模块从 master 开 docs 分支; 主仓用独立 worktree 或等 #195 这边提交完再开分支) -> B.2 (改完用上面的比对方法复核: 列表数 = 42) -> C.1 (Conventional Commits, `docs(readme): ...`) -> C.2 (子模块**本地 merge + 双推**, 不走 Forgejo 服务端合并; 推后对两个 remote 逐个 `git ls-remote` 核 SHA)
- 跳过: A.1 (Level 1 不需要 OpenSpec) / Rule #6 benchmark (README 不是 SKILL.md, 不影响 AI 运行时行为)
- 理由: 数量和 badge 都对, 只差列表条目, 是纯描述性修复; 版本号无需 bump 到新的 minor, 可随下一次 PATCH 发布带出

**[2] 修复 + 补机械兜底**
- 在 [1] 的基础上, 给 `.aria/state-checks.yaml` 加一项自定义检查 (例如 `readme-skill-list-completeness`): 枚举 `aria/skills/*/SKILL.md`, 断言每个 Skill 名在 `aria/README.md` 和主项目 README 里都出现, 并断言标题里的数量 = 实际数量
- 理由: 这次漏项之所以存在很多个版本, 就是因为现有 16 项检查只管版本号不管列表。新增检查属于新需求, 按 Rule #1 需要 Level 2 OpenSpec, 工作量比 [1] 大
- 该检查写好后要先对「修复前」的 README 跑一遍确认会报 FAIL, 否则可能是恒绿

**[3] 只记 issue, 暂不修**
- 在 `10CG/aria-plugin` 开一个 issue 记录两个漏项 + 两处标注不一致, 等下次发版一起修
- 理由: 不打断 `#195` 当前的进度; 代价是 README 继续对外少列 2 个 Skill

**[4] 先确认版本前提**
- 如果你确实在别处发了一个「v1.14.0 + 3 个新 Skill」的版本 (别的仓库、别的 checkout 或别的分支), 请告诉我路径, 我对那个位置重新扫描; 当前工作区的结果对那个版本不适用

置信度: [1] 不到自动执行阈值 (且 `auto_execute_enabled` 默认关闭), 需要你确认。

**如果选 [1] 或 [2] 进入 Phase B**: 因为 `collision.kind` 非空且 coordination 默认开启, 进入 Phase B 前按流程要调一次 advisory 认领闸门。本次评测只写出命令, **没有执行**:

```bash
python3 "<plugin>/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<新建的 README 修复轨 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
```

另外, 若本会话持有 active claim, 每次入口还要跑一次心跳 (`phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path "/home/dev/Aria"`)。本次同样**没有执行**; 上一份 handoff 也特别提醒过开工先查 claim 心跳年龄。

请回复 [1] / [2] / [3] / [4], 或自定义组合 (例如「只改 aria/README.md, 主项目 README 先不动」)。
