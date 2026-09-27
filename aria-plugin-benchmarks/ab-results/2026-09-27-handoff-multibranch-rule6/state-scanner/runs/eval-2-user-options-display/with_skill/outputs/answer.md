# 项目状态扫描 (state-scanner)

scan.py 跑完，退出码 0，所有采集项都成功，errors[] 为空。snapshot_schema_version = "1.0"，入口检查通过。没有中断中的工作流 (interrupt.status = none)，也没有暂停中的 git 操作 (git_operation_in_progress.operation = none)，所以按常规规则出推荐。

---

## 1. 当前状态

- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (10CG/Aria#195)，比 master 多 13 个提交
- HEAD: `4f91772` docs(openspec): 10CG/Aria#195 台账记 owner 2026-09-27 裁定与 feature 双推
- Phase/Cycle: 本仓没有运行时 UPM (upm.configured = false)，进度按 OpenSpec + 台账看
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity` (approved，Level 3)
- 本轨进度 (来自 `verification-ledger.md`): 组 1 到组 4 全部完成 (TASK-001 至 TASK-025)，全量回归 `Ran 1627 OK`，SC-11 谓词 19/19 为真；TASK-025 已开出遗留缺口 issue `10CG/aria-plugin#204`；owner 2026-09-27 裁定已落台账。`tasks.md` 显示 1/27 勾选，这是计划本身的设计 (27 行在 Phase D 一次勾完，见 5.4)，不是没做。
- 下一个任务: TASK-026 (Rule #6 AB)。结果目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` 已有 `PREDICTION.md` 和 13 个 eval 的运行目录，说明 AB **已经开跑或正在跑**，还没有 RESULT.md。
- claim: 本容器 `simonfish/bfe8285d` 持有两条 active claim，心跳都是今天 12:35Z 前后刷新的 (距扫描约 4.4 小时，未超 24h 扫除阈值):
  - `handoff-multibranch-subdir-path-fidelity` (phase B，`claims/bfe8285d/s-48ca@0612.yaml`)
  - `pre-merge-completeness-gate-change-scope` (phase A.2，`claims/bfe8285d/s-73b9@1606.yaml`)
- 上次 handoff: `2026-09-24-session-close-199-post-planning-converged.md` (60.1 小时前，来源 pointer)

**handoff 注意**: `docs/handoff/latest.md` 落后于实际进度。它的轨道表还把 10CG/Aria#195 写成「yielded，待认领，B.1 未起」，但协调 ref 上本容器已认领 (s-48ca，phase B)，而且组 1 到组 4 都做完了。09-25 以后 #195 的进度只记在台账里，没有对应的 handoff。本会话收尾时建议补一份轨级 handoff 并更新 latest.md 那一行。

## 2. 变更分析

- 未提交变更 3 项，全部归为 other:
  - `aria` 子模块: 工作区 HEAD `b181678` (feature 分支)，主仓记录的 gitlink 是 `1cb3872`
  - `standards` 子模块: 工作区 HEAD `d86fc91` (feature 分支)，gitlink 是 `940cb5b`
  - 未跟踪目录: `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` (进行中的 AB)
- 复杂度: Level 2 (scan 判定)；架构影响: 无；测试覆盖: 本次未提交变更里没有测试文件
- 两个 gitlink 的差异是**预期的**: 按计划要等 TASK-029/034 子模块本地合并并双推之后，才在 TASK-030 前移主仓 gitlink。现在不要提交它们，否则会产生孤立 gitlink。
- 本次未提交变更里没有 SKILL.md 改动 (skill_changes.detected = false)。不过本轨改了 state-scanner 的 collector 与 references，Rule #6 AB 本来就在计划里 (TASK-026)。

## 3. 需求状态

- 配置状态: 已配置
- PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved，归一化状态为 pending)
- User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
- 优先项: US-026 (in_progress，M6 还剩 Spec #2 与 Spec #4)、US-007 (in_progress)、US-003 (pending)

## 4. 架构状态

- System Architecture: 存在，`docs/architecture/system-architecture.md`，状态 Active
- 最后更新: 2026-09-02 (custom check 报 25 天，未超阈值)
- 需求链路: 完整 (引用了 prd-aria-v1 和 prd-aria-v2)

## 5. OpenSpec 状态

- 活跃变更: 8 个，全部 approved
  - `handoff-multibranch-subdir-path-fidelity` (#195，Phase B 已完成，下一步 AB)
  - `pre-merge-completeness-gate-change-scope` (#199，post_planning 已收敛，被入口门卡住: 要等 #195 完成 C.2，或 owner 明确改顺序)
  - M6/M7 四份 + 遥测一份 (见下面「设计未实施」)
- 已归档: 146 个；待归档: 0 个
- 设计未实施: 5 个 (design_deferred)。它们都卡在 owner 或基建的门上，不是被遗漏:
  - `aria-2.0-m6-cost-model-telemetry`: approved，25/38 未勾，搁置 79 天
  - `aria-2.0-m6-e2e-resilience`: approved，25/40 未勾，77 天
  - `aria-2.0-m6-release-closeout`: approved，41/41 未勾，124 天
  - `aria-2.0-m7-agent-lifecycle`: approved，18/18 未勾，100 天
  - `aria-2.0-m7-fleet-aggregation`: approved，20/20 未勾，70 天
  - 另外 `aria-2.0-m6-dispatch-input-delivery` 虽不在该列表，但它的 claim 已是 abandoned，门在 owner/基建 (Blocker 3/4)

## 6. 审计状态

- 审计系统: 已启用
- 上次审计: `post_planning` R7，PASS，已收敛 (2026-09-24，#199 轨)
- 没有未收敛的审计

## 7. 自定义检查

16/16 全部通过，0 失败 0 跳过。包括 `m6-version-badge-match` (1.73.3)、`plugin-cache-currency` (installed=1.73.3 = sot)、`main-project-version-consistency` (1.7.5，9 个引用点一致)、`claude-md-changelog-free` (152 行)、`forgejo-app-token-liveness`、`coordination-gate-invocation` (近期有 3 次生产调用) 等。

## 8. 同步状态

- 当前分支没有设置 upstream (reason = no_upstream)，所以没有 ahead/behind 数字。不过多远程比对显示主仓 feature 分支两端都已对齐:
  - 主仓 `4f91772`: origin = github = 本地 (equal，证据 fresh)
  - `standards` `d86fc91` / `aria` `b181678` / `aria-orchestrator` `237045a`: 两端都 equal
  - overall_parity = true；gitlink 可达性 6/6 ok (没有孤立 gitlink)
- 子模块和主仓 master 相比没有落后 (tree_vs_remote 全为 false)
- README: `aria` 的 README 版本 1.73.3 = plugin.json
- 插件依赖: standards 子模块已注册并初始化
- Forgejo 配置: 检测到 Forgejo 远程 (forgejo.10cg.pub)，但缺少 `CLAUDE.local.md`。可以运行 `/forgejo-sync` 引导创建 (需要你确认；这不影响当前工作，因为 forgejo CLI wrapper 能用)
- 多终端: `tracks_multibranch.collision.kind = self_multi_container` (同一身份在多个容器下出现: 023236f2 与 bfe8285d)，附 2 条同机多身份信息 (aria-runner-bot 与 simonfish 共用 identity_key)。`coordination.enabled = true`，所以进 Phase B 时由 phase1_gate advisory 认领处理，不走规则 1.54。

## 9. Open Issues

- 共 49 个 open (数据来自缓存，抓取时间 2026-09-27T16:54Z): 10CG/Aria 20 / 10CG/aria-plugin 20 / 10CG/aria-standards 7 / 10CG/aria-orchestrator 2
- 带 bug 标签的 4 个 (没有 blocker/critical 标签，不降级推荐):
  - 10CG/Aria#221 secret-guard 缺口: 进程列举能绕过凭据保护
  - 10CG/Aria#218 state-scanner: handoff 没有 pointer 时按工作树 mtime 判最新，rebase/checkout 后会指错文件
  - 10CG/Aria#217 session-closer: handoff_autofill.py / consistency_check.py 的 stdout 随 OS locale 变化 (Windows)
  - 10CG/Aria#199 pre_merge Checkpoint Completeness Gate 缺 change_id 维度 (即本仓 #199 轨)
- 最新的未标签 issue: 10CG/Aria#220 latest.md History prepend 没有机械核验 (曾经一次整文件重写静默删掉 88 条)

## 10. 推荐工作流

先说前提: 下面 [1] 和 [2] 都属于 #195 轨，已由本容器认领 (claim s-48ca active，心跳新鲜)。按 SKILL 契约，每次入口要给持有的 claim 打一次心跳。本评测环境只读，我**没有执行**，要执行的命令是:

```bash
python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
  --heartbeat-only --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase A.1 --repo-path /home/dev/Aria
```

**[1] 收口 #195 的 Rule #6 AB (TASK-026)** (推荐)
- 执行: B.2 的末项 (计划 5.5)。先查 `ab-results/2026-09-27-handoff-multibranch-rule6/state-scanner/runs/` 下 13 个 eval 的两臂是否都跑完。**如果另一个会话还在跑，不要重复开跑。** 然后用脚本从两臂 grading.json 汇总，`delta.pass_rate = mean(with) − mean(old)` (注意官方聚合脚本的符号是反的)；with 臂劣于 old 的 eval 再复跑两次，三次里两次以上仍劣才判回归；写 RESULT.md，并按 SOT 登记场景 1 的验收条件 `delta.pass_rate > 0` 有没有达成；再开 AB 套件缺口 issue (外向动作，需要 owner 授权)。
- 跳过: A.* (spec 已 approved，post_planning 已收口)、B.1 (分支已存在)
- 理由: 台账显示组 1 到组 4 与 TASK-025 都已完成，下一步只剩 TASK-026。PREDICTION.md 已预判两臂 SKILL.md 逐字节相同、套件结构上测不到 collector 的变化，大概率会落到「未被有效测试」，**需要 owner 在 5.1 之前裁定** (Rule #6 / Rule #10: AI 不能自行豁免)。

**[2] #195 进 Phase C: 版本号与合并 (TASK-027 → 028 → 029/034 → 030 → 031)**
- 执行: aria MINOR bump + CHANGELOG 三段，并入 standards `session-handoff.md` 升 1.4.0 (owner 09-27 已裁) → 第一次引用写法自检 → 子模块**本地** `git merge --no-ff` + 打 tag + 合并树回归 → 双推 (`--atomic`，先 origin 后 github)，推后逐个 remote `ls-remote` 核验 → 主仓前移两个 gitlink + 16 个版本点 → 开 PR，经 phase-c-integrator 跑 pre-merge gate (C.2.4) → C.2.5 双推主仓并核验
- 理由: 这是 #199 的入口门。#195 完成 C.2 后，#199 才能开 B.1
- 前置: 必须等 [1] 的 AB 判定无回归、owner 裁定验收登记之后才能开始；取号前先 `ls-remote --tags` 查一下有没有并行发版撞号。子模块合并禁止用 Forgejo 服务端合并 (硬约束 1)

**[3] 处理 #199 轨的 owner 待裁项 (不进开发)**
- 执行: 整理给 owner 的裁定清单: R7 六条 minor 与各轮未处置 minor 什么时候处理 / 三批执笔请裁 (v2.4 九条、v2.5 十条、v2.6 两条) / 执笔报告和机器清单要不要落仓；顺手补写 #195 的轨级 handoff，并修正 `latest.md` 里过期的「#195 yielded 待认领」那一行
- 理由: #199 已收敛，但入口门还没满足；这些裁定可以和 #195 并行准备，不改代码
- 注意: 转述待裁项时，原文没有推荐的地方不自己编默认项

**[4] 自定义组合**
- 输入格式: 例如 "B.2 + C.1"、"Phase C"，或者指定其他轨 (比如 triage 10CG/Aria#221 secret-guard 缺口 / 10CG/Aria#218 state-scanner handoff mtime 问题，或者跑 `/forgejo-sync` 补 `CLAUDE.local.md`)

请选择 [1-4]，或者输入自定义组合。(workflow.auto_proceed = false，所以不会自动执行。)
