---
checkpoint: post_planning
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-22T15:18:48.596Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R6 — tech-lead 席 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v2.5)

> 被审对象: 主仓 `37335d4` (计划三文件的 v2.5 在 `e7a1782`)。本席实测 `git ls-remote origin master` 与 `git ls-remote github master` 均为 `37335d4f78ea90ebfc5292999f1b15b88117d86b`, 与本地 HEAD 一致; 子模块 aria `1cb3872` / standards `940cb5b` / aria-orchestrator `237045a`。
> 本席未打开任何他席 R6 报告。真仓内零 git 写操作; 实跑全部在 `scratchpad/audit-R6-tech-lead/` (共享副本 `state-base` 先 `cp -a` 为 `state-copy`, 并把该拷贝主仓与 aria 的 push URL 改成无效路径后才跑)。未派子代理。对共享副本只做过只读查看 (`ls` / `git log` / `git status`, 仅 `state-base`, 从未进入 `base/Aria`); 收尾以 `find -newer .marker-before-dispatch -type f` 核验两份共享副本零普通文件变动 (只有若干 `.git` 目录的 mtime 变化, git 取锁再删锁即会如此), `state-base` HEAD 仍为 `a563192`、其 aria 仍为 `1cb3872`。

## 已实读文件

派单 sha256[:16] = 2c93e42302ca9b95

- 派单原件 `scratchpad/r6-prompts/tech-lead.md` 全文 (108 行)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (240 行)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1982 行, 含 metadata 全部键、两份三态脚本与输出、31 个 TASK)。
- `git diff b686185 e7a1782`: tasks.md 逐词 diff 全文; yaml 的 hunk 清单与 metadata 段逐 hunk (hard_constraints 第 4 / 14 条、owner_gates 第 2 / 6 / 13a / 13b / 14 / 15 / 16 / 17 项、sc12_liveness、coord_ref_precheck、commit_attribution、crlf_guard)。
- `.aria/audit-reports/post_planning-R5-2026-09-22T034038-000Z-...-aggregated.md` 全文 (Major 簇 / Minor / Conflicted / 流程记录)。
- proposal.md: §1.0 `:103-152`, 内联 Tasks `:439-451` (python 切片)。
- 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (116 行)。
- `CLAUDE.md` 多远程两条硬约束与不可协商规则 #3 / #6 / #8 / #10 (会话上下文内)。
- aria 源码 (实读, 行号以本席读到为准): `phase-c-integrator/SKILL.md` `:100-200` (C.2 / C.2.4 / C.2.4.5 摘要)、`:406-596` (C.2.4.5 全段)、`:600-643` (C.2.5); `phase-c-integrator/scripts/submodule_gate.sh` 全文 (335 行); `state-scanner/scripts/release_gate.py` `:1-260`; `state-scanner/scripts/phase1_gate.py` `:1125-1200` (`_heartbeat_only`)、`:1415-1510` (argparse); `state-scanner/lib/coordination_ref.py` `:1332-1372`; `state-scanner/lib/failure_handlers.py` 的 `resilient_push` 与 `health_check_fetch`; `state-scanner/lib/constants.py` `:20-58`; `state-scanner/lib/identity.py` `:192-242`; `state-scanner/SKILL.md` `:114-200`; `state-scanner/references/layer-l-integration.md` `:51-100`; `state-scanner/scripts/collectors/remote_refresh.py` `:405-440`; `state-scanner/scripts/lib/spec_complete.py` `:851-908`; `branch-manager/SKILL.md` `:520-560`、`:615-645`; `git-remote-helper/scripts/push_all_remotes.sh` `:19-125`; `config-loader/DEFAULTS.json` `:1-20`; `hooks/hooks.json`、`hooks/submodule-gate-telemetry.sh` 全文、`hooks/session-start-check.sh` (检索); `aria/.gitignore`; `session-closer/scripts/handoff_autofill.py` `:391-470`; `phase-d-closer/references/handoff-mechanics.md` `:86-97`。
- standards: `conventions/skill-benchmark-exemption.md` `:12-60`; `conventions/content-integrity.md` §4.5。
- 主仓: `.aria/state-checks.yaml` (计划复跑的八条 check 的 command)、`.aria/config.json` 的 `phase_c_integrator` 段、`.gitignore`、`.forgejo/workflows/` 两个 workflow 的触发段、`docs/handoff/latest.md` track 表、轨级 handoff `docs/handoff/2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md` 的「执笔实例提请裁定 (十条, v2.5)」节、`openspec/archive/2026-09-17-rule6-description-change-trigger-eval-lane/proposal.md` (T4 / version.yaml 检索)。
- 协调 ref (只读): `git ls-tree -r refs/aria/coordination` 下 `claims/bfe8285d/*` 共 14 条的 track_id / status / heartbeat_at。
- 本席实跑 (均在自有 scratch): `a2_v2_checks.py` (N4 / C1 / N6 / N7 / N8 / N9 / N10 / N11) 与嵌入输出 diff = 逐字节一致; `a2_state_runs.py` 与嵌入输出 diff = 逐字节一致; `gen_yaml.py` 以嵌入脚本与输出为输入重生成, `cmp` = 逐字节一致; 定向实验 `exp_release_diverged.py` (见 m2); 引用解析脚本 `refs.py` (见 m1); 空目录 `unittest discover` 退出码实测 (Python 3.11.2, `Ran 0 tests ... OK`, rc=0)。

## R5 对账

| R5 条目 | 结论 | 本席亲验证据 |
|---|---|---|
| R5-M1 `9c294cca` (第 13 项同批与 latest.md diff 时序冲突) | **closed** | owner_gates 拆为 13a (yaml `:218`, release 之前请, 只含 release 推送) 与 13b (`:219`, latest.md 单独提交产生之后请, 附其 diff); TASK-031 的 claim 条 (`:1975`) 只请 13a, latest.md 单独提交条 (`:1981`) 与末条 (`:1982`) 在该提交之后请 13b, 请求时点与 diff 产生时点不再冲突。脚本全文检索未拆分的「第 13 项 / 等待点 13」: tasks.md 与 yaml (去掉 revision_log) 只剩「原第 13 项 / 原等待点 13」历史叙述与无关表格行。 |
| R5-M2 `3e6a8483` (claim 只在 TASK-001 核一次存活) | **closed** | hard_constraints 第 4 条 (`:194`) 改为每个 Phase B–D 会话入口做「解析 → 前置检查 → 强制对齐后重解析 → 心跳 + coord_push_verify」; 第 14 项挂载扩到任意会话与 TASK-031 的 release (`:220`); TASK-031 release 遇 `claim_not_found` 单列 (`:1975`)。源码核对: `_heartbeat_only` 自述「no fetch of its own」(`phase1_gate.py:1136`); `fetch_coordination_ref` 用非强制 refspec `refs/aria/coordination:refs/aria/coordination` (`coordination_ref.py:1367`); `release_gate` 对 `claim_not_found` 记 benign、退出 0 (`release_gate.py:16`、`:67`、`:153`)。N11 在本席副本复跑逐字节一致。新面见 m2 (强制对齐未推广到 release 路径), 不影响本条闭合。 |
| R5-M3 `3782becc` (C.2.4.5 已启用闸被漏) | **closed** | TASK-030 新增 C.2.4.5 条 (`:1944`) 与第 17 项 (`:223`)。对 `submodule_gate.sh` 逐项核: 退出码表 `:20-27` 与计划一致; `MODE="${ARIA_SUBMODULE_GATE_MODE:-block}"` (`:33`) 而头注释 `:15-16` 写「读 config、缺省 warn」—— 执笔「以代码为准」成立; 无 `.gitmodules` 打印 trivially passes 并退出 0 (`:224-227`)、目录缺失打印 skipping (`:231-233`); 结论行格式 `OK:` (`:259`) / `GATE:` (`:263`) / `PASS:` (`:267`) / `BLOCK:` 走 stderr (`:308`); 遥测写 `aria/metrics/*.jsonl`, 被 `aria/.gitignore:12-13` 忽略。`.aria/config.json` 无 `submodule_gate` 键 ⇒ 缺省 block 成立。 |
| R5-M4 `c287d217` (同族「空输出即通过」两处) | **closed** | TASK-027 第 4 步 (b) (`:1873`) 两端点先 `cat-file -e`、diff 退出码非 0 即停; `guard_config_hooks` (`:329`) 写成 `git -C <主仓根> grep … ; echo "rc=${PIPESTATUS[0]}"`, 判据 rc ∈ {0,1} 且其前无输出; TASK-021 SC-12 三条改放子 shell (`:1748`)。N10 复跑一致: 从 `aria/skills/audit-engine/tests` 跑且 config 含符号时 v2.5 命令 rc=0 hits=1 停, v2.4 命令 0 行放行; `<主仓根>` 非仓时 rc=128 停。 |
| R5-M5 `76921ca3` (aria 侧工作区污染递归检索) | **closed** | 工作区改为只放主仓 `aria-plugin-benchmarks/ab-workspace/` (TASK-024 `:1810`)。本席核三个递归面都碰不到它: 主仓 `.gitignore:37` 忽略该目录 (`git check-ignore -v` 命中); `no-unresolved-version-placeholder` 只扫 `aria/`; 归档门分类器 `_grep_symbol_occurrences` 首选 `git grep --recurse-submodules`, 只搜已追踪文件 (`spec_complete.py:866-892`)。另实测本机已存在的 `aria/skills/issue-triage-workspace/` (被 `aria/.gitignore:7` 忽略) 不含两类命中: SC-13 递归检索仍 4 处、`<vNEXT>` 检索 rc=1 零命中 —— 基线不受其污染, 且它确会让 (b) 修法的「断言无 `*-workspace` 目录」误停, 选 (a) 的理由成立。 |
| `1453c41f` (TASK-027 第 4 步只比上游一侧) | **closed** | 新增 (c) feature 一侧 (`:1873`): W、feature 现值、TASK-024 结果提交三者先 `cat-file -e`, 再比 aria 两个 skill 目录 `W..<feature>` 与主仓 `ab-suite/audit-engine.json` (结果提交对工作树); TASK-024 末条补记结果提交 SHA (`:1816`)。 |
| `118d1d64` (TASK-031 deliverables 缺 latest.md) | **closed** | TASK-031 deliverables 第 5 项为 `docs/handoff/latest.md` (`:1964`)。 |
| `ac2e8dcb` (owner-container 空值) | **closed** | 周期 handoff 起稿条 (`:1977`) 要求先看退出码、非 0 或空按 handoff-mechanics 回退; 自校验条 (`:1978`) 另加值非空检查。源码核对: `--owner-container` 分支 `print(oc if oc is not None else "")` + `return 0 if oc is not None else 1` (`handoff_autofill.py:463-466`); 回退句在 `handoff-mechanics.md:92`。 |
| `11c3a29f` (`aria_shifted` 第 6 条非路径) | **closed** | 原条拆成三条 (`:77-79`); TASK-001 基线复核条 (`:1355`) 新增「每个文件先 `cat-file -e <端点>:<文件>`, 两端都不存在即停」。本席逐条核 `aria_shifted` 八条与 `standards_files` 八条的「冒号前」均为单一路径。 |

## Findings

无 critical, 无 major。

### m1 — `6ad0a84b` · minor · issue · documentation · scope `detailed-tasks.yaml hard_constraints 第 4 条 / TASK-001`

**summary**: v2.5 新写的两处「TASK-024 末条」指错条目 (所指内容在第 12 条, 末条是第 13 条); 同族的「TASK-023 末条」三处 (v2.3 插入 trailer 条之后即已错位, 前轮无人报) 实指第 5 条, 末条是第 7 条。

**证据** (引用解析脚本 `refs.py` 的输出与 v2.4 / v2.5 两版 TASK-024 条目清单):
- TASK-024 在 `b686185` 与 `e7a1782` 都是 13 条; 第 12 条 (`:1815`) =「结束后先取第二次快照 … 退出 0 才按场景 1 第 3 步强制对齐 … 换不带该变量的会话继续, 该会话第一步是 hard_constraints 第 4 条的会话入口 claim 核验」; 第 13 条 (`:1816`) =「结果目录与台账由主控在主仓 feature 分支提交, 提交 SHA 记台账 …」。
- v2.5 新写: hard_constraints 第 4 条 (`:194`)「由其末条让 AB 之后的第一个普通会话先做入口核验」; TASK-001 心跳条 (`:1351`)「git fetch origin +refs/aria/coordination:refs/aria/coordination (即 TASK-024 末条所引 AB_TEST_OPERATIONS.md 场景 1 第 3 步的命令, 须退出 0)」—— 两处所指都是第 12 条。同一 v2.5 里 revision_log 的「TASK-024 末条补记结果提交 SHA」指的又确实是第 13 条: 「末条」在同一版本里指两条不同条目。
- 既有: owner_gates 第 6 项 (`:211`)「feature 并入 aria origin/master 时冲突 (TASK-023 末条 / TASK-025)」、TASK-024 第 3 条 (`:1806`)「(TASK-023 末条已并入)」—— 所指的上游并入在 TASK-023 第 5 条 (`:1787`), 末条第 7 条 (`:1789`) 是「主控在主仓 feature 分支提交」。R4 tech-lead 报告 `:185` 沿用了「TASK-023 末条」这一错误称呼, 未报。与执笔自报请裁第 9 条 (「TASK-001 第 1 条」应为第 2 条) 同族。

**失败场景**: 执行者按 hard_constraints 第 4 条或 TASK-001 心跳条的指针去 TASK-024 末条找「AB 之后第一个普通会话做入口核验」与「场景 1 第 3 步命令」, 读到的是结果目录提交条, 得在前后条目里自己再找。因为 hard_constraints 第 4 条自身已写明要做入口核验、第 12 条原文也在, 执行者最终不会漏做 —— 不改变执行者会做什么, 故 minor。

**建议修法**: 这类条目序号引用在长文档里每次插条就集体腐坏 (本计划已第三次出现: 「TASK-001 第 1 条」「TASK-023 末条」「TASK-024 末条」), 改成锚点式引用, 如「TASK-024 的『结束后先取第二次快照』条」「TASK-023 的『开 AB 会话之前 … 并入』条」, 三组一并改。

### m2 — `2c2e8931` · minor · issue · implementation · scope `detailed-tasks.yaml TASK-031 release`

**summary**: v2.5 的「强制对齐」只加在会话入口心跳一处, 没推广到同样由计划发起的 TASK-031 release: 前置检查 exit 0 覆盖「与 origin 分叉、但本地只领先本轨心跳」态, 此态下照 TASK-031 写法 (前置检查 → 直接 `release_gate`) 会把 release 写在本地、推送失败, 留下与第 13a 项「不写仅本地的 release」相反的本地 release 提交。

**证据**:
- 计划原文: TASK-031 claim (D.2b) 条 (`:1975`)「获授权后先跑 metadata.coord_ref_precheck, 退出 0 才跑 … release_gate.py … release 的推送按 metadata.coord_push_verify 核验 …, 任一不成立 ⇒ 停下上报 owner_gates 第 15 项」—— 没有对齐步。v2.5 给心跳加对齐的理由 (TASK-001 `:1351`, tasks.md 判断清单第 41 条): 「resilient_push 的重取用非强制 refspec, 分叉即被拒」—— 这条理由对 release 的推送同样成立。
- 前置检查在分叉态判 exit 0: N6 嵌入输出 `[remote advanced + local own heartbeat (diverged)] exit=0 verdict=ok` (`:1281`, 本席复跑一致)。
- 源码: `release_gate` 第 1 步 `fetch_coordination_ref` 失败时「proceeding with local view」(`release_gate.py:122-129`), 第 2 步照样写本地 release (`:143-157`), 第 5 步才推 (`:205-216`); fetch 用非强制 refspec (`coordination_ref.py:1367`), 分叉即被拒。
- 本席定向实验 (`exp_release_diverged.py`, 临时裸仓, aria `1cb3872` 的 state-scanner 脚本, 与 N11 同法造态: 本轨认领并推送 → 另一克隆推一条别的 claim → 本地在落后值上心跳、推送失败, 形成分叉), 原样输出:
  ```
  [as-written] heartbeat on stale local: outcome=refreshed push_success=False (local now has an unpushed own heartbeat, diverged)
      [before release] precheck exit=0 verdict=ok kinds=['own-heartbeat']
      [release_gate] exit=0 fetch_success=False released.success=True push_success=False push_skipped=False hard_error=None
      [after release] remote_equals_local=False
      [after release (local-only release commit present)] precheck exit=1 verdict=stop kinds=['own-heartbeat', 'other']
  [aligned-first] ...
      [before alignment] precheck exit=0 verdict=ok kinds=['own-heartbeat']
      [release_gate after alignment] exit=0 fetch_success=True released.success=True push_success=True hard_error=None
      [after release] remote_equals_local=True
  ```

**三态**: 基线态 (本地与 origin 相等或只是落后) —— 照原写法可行, `release_gate` 自带的快进 fetch 兜住; 坏态 (本地分叉、只领先本轨心跳) —— 原写法 `push_success=False`, 本地留下 release 提交; 目标态 (前置检查 exit 0 后先强制对齐) —— 同一分叉态下 `push_success=True`、远端等于本地。

**失败场景**: 会话入口核验在会话开头对齐过; 同一会话稍后有一次协调 ref 写入没推出去 (可达来源: `/state-scanner` 入口心跳按 fail-soft 在 fetch 降级时「照常写本地, push 尝试一次即止」, `layer-l-integration.md` 的 degraded 处置段; 或第 15 项自带的降级路径「心跳加 --no-push」), 期间 origin 前进 ⇒ 本地分叉。TASK-031 获 13a 授权 → 前置检查 exit 0 → `release_gate` 写本地 release、推送失败 → 第 15 项。此后: 本地已有一条「只在本地的 release」, 与第 13a 项的承诺相反; 之后每次前置检查都 exit 1, TASK-031 latest.md 子步骤 2 要求的「过前置检查后跑 /state-scanner」无法进行; hard_constraints 第 4 条「release 之后不再做入口核验」在「本地已 release、origin 仍 active」时语义不明。方向是 fail-closed (停在第 15 项, owner 裁定是合法下一步), 且需要同一会话里先有一次失败的协调推送, 可达性偏低 —— 故 minor。

**建议修法**: TASK-031 release 条改为「前置检查 exit 0 → 强制对齐 (同 TASK-001 心跳条的命令, 须退出 0) → 重跑三元组解析 (0 条 active 直接走本条的 claim_not_found 分支) → release_gate」; 并在 `coord_ref_precheck` 用法注释里把「退出 0 = 可推送」改成「退出 0 = 可强制对齐 (对齐后才可推送)」—— 分叉态直接推必失败。第 14 项的重认领在会话入口路径上紧跟对齐之后, 不受影响; 若重认领与对齐之间隔了其它写入, 同理先对齐。

## 对执笔人自报薄弱点的表态

1. **会话入口强制对齐依赖前置检查无盲区 —— 可接受**。本席逐行读 `coord_ref_precheck`: 合并提交的 `diff-tree` 为空 ⇒ `bool(files)` 假 ⇒ other; 任何非 `heartbeat_at:` 的改动行、任何 own 集以外的文件 ⇒ other; v2.5 起 `rev-parse FETCH_HEAD` / `rev-list` 失败退出 2; 循环内 git 失败落成空列表 ⇒ other —— 各失败形态都是 fail-closed, N6 / N11 复跑一致。它的问题不在盲区, 在只用在了心跳一处 (m2)。
2. **会话间隔超过 24h 只能事后发现 —— 可接受**。心跳只挂在入口而非定时器是插件的既定设计 (`lib/constants.py:43-57` 注释明写)。补充一个事实: `STALE_TTL = 1800` 秒 (`lib/constants.py:36`), 他容器按 advisory 语义把本轨视为「可接手」从心跳后 30 分钟就开始, 入口核验真正防住的是 24h 的持久 sweep; 多周周期里每个超过 24h 的间隔多一次第 14 项往返, 代价如实。
3. **13a 批、13b 不批的中间态只记台账 —— 可接受**。两个决定都由 owner 做出, 状态对 owner 可见; 要从机制上消除它只能把 D.2b 挪到 D.3 之后, 与 phase-d-closer 的子步顺序相反。
4. **C.2.4.5 放行判据绑定脚本输出行格式 —— 可接受**。方向 fail-closed; 本席对 `submodule_gate.sh:224-313` 逐行核过当前格式。注意 `BLOCK:` 行走 stderr, 台账须同时收两路输出 (计划写「完整输出原样记台账」, 已覆盖)。
5. **同族扫描靠词形生成候选 —— 可接受 (附一处实例)**。本席换方法 (逐条枚举「两命令输出相比较」与「失败后远程跟踪 ref 停旧值」形态) 复扫, 未发现通则第 14 条兜不住的真空通过; 但「逐处写进条目」并不完整: TASK-030 调 C.2.5 前对三个子模块「各自 fetch origin 与 github, 断言本地 master 等于 HEAD 等于 origin/master 等于 github/master」(`:1947`) 没像第 2 项 / TASK-001 那样写明 fetch 须退出 0 —— github fetch 失败时 `github/master` 停在旧值, 断言可能照样成立。这一形态落在通则 (1) 的「fetch 为 0」里, 故不立 finding。
6. **通则第 14 条依赖执行者知道结果码 —— 可接受**。所列集合覆盖了本计划实际用到的命令; `python3 -c` 单行默认 0 也能按通则读。
7. **「Ran 数不得少于基线」在上游合法删测试时误停 —— 可接受 (fail-closed)**。建议 TASK-001 在 B.1 当时的 aria 起点重测一次三套 Ran 数作为基线 —— 现在的基线是 A.2 在 `1cb3872` 的数, 离执行越久越容易误停。
8. **N11 是合成态 —— 可接受**。N11 支撑的是状态逻辑 (落后本地仍显示 active、对齐后显示 abandoned、心跳得 `claim_not_found`、release 记 benign), 与生产时序无关; 本席复跑逐字节一致, 并用同法造态做了 m2 的定向实验。
9. **同体自检 —— 可接受**。R1 判据 (本轮 2/5 未过半) 不触发换人; 本轮本席打出的两条仍在「修法带出的新面」上 (m1 是 v2.5 新写的引用, m2 是 v2.5 新机制未推广), 与已知盲区同型。

## 风险 / 疑问

1. **已知项 (A) 重新评估: 维持 minor, 不立 finding**。TASK-031 周期 handoff 条 (`:1977`) 仍写「track-id 写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项」, 而 `commit_attribution` 只在 TASK-001 / TASK-030 调用; v2.5 新加的值非空检查 (`:1978`) 只查非空、不查取值, 13b 的请求只附 latest.md 的 diff —— 写错的 track-id 没有任何一步会拦。后果是一份归属错的 handoff (可事后改), 不是外向误推。廉价修法: 自校验条加一条 `head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope'` 须为 1。
2. **执笔实例十条请裁 (B) 表态**: 第 1 条 (a) 选址 —— 同意, 证据见 R5 对账 R5-M5 行; 第 2 条新立第 17 项 —— 同意, 另见下条; 第 3 条强制对齐与两处例外 —— 同意用于心跳, 但应推广到 release (m2); 第 4 条中间态只记台账 —— 同意; 第 5 条通则范围 —— 同意, 措辞不过宽; 第 6 条 (c) 比到工作树 —— 同意, 能收住主仓侧未提交的 TASK-026 改动; 第 7 条 History 节恢复与否交 13b —— 同意; 第 8 条 guard 第三个调用点 —— 同意 (TASK-027 第 7 步复跑 L2, 与 TASK-021 同理); 第 9 条序号差一 —— 应顺手改, 且同族还有 m1 的两组; 第 10 条 `no-unresolved-version-placeholder` 的反转写法 —— 计划侧已兜住, 检查本身的修改宜另开单交维护该检查的轨。
3. **C.2.4.5 的一个前提措辞不准, 不改变动作**。判断清单第 42 条与 TASK-030 写「主仓 PR 走 Forgejo 合并, 不经 branch-manager merge action, 不会被自动触发」; 实读 `branch-manager/SKILL.md:528-533` 与 `:630-634`, merge action 本身就是调 Forgejo API 合并 —— 若执行者经 phase-c-integrator 继续到 branch-manager 合并, C.2.4.5 会再自动跑一遍 (重复但无害); 另有 PostToolUse 钩子 `hooks/submodule-gate-telemetry.sh` 在每个触碰 gitlink 的 `git commit` 后以 WARN 模式跑该脚本 (只记遥测、会 `git fetch origin`), TASK-029 的 gitlink 提交会触发它。计划「合并前显式跑一次」的动作在两种路径下都成立。
4. **C.2.4.5 放行条件里「aria 须为 GATE + PASS forward bump」偏窄**: 若 TASK-028 推送后、主仓 PR 合并前他轨又发了 aria (其合并含本轨提交) 并 bump 了主仓 gitlink, 同步后本 PR 的 aria 变为 `OK: unchanged`, 按字面缺 PASS 行会停在第 17 项。概率低, fail-closed, 由 owner 裁即可。
5. **Rule #6 substitute 的举例与 SOT 字面有距离**: TASK-027 第 4 步 (c) 把描述性 hunk 的 substitute 举例为「TASK-026 的写法自检或 TASK-018 的文档机检」; SOT `skill-benchmark-exemption.md:28` 要求「SC 级 baseline-failing 单元/集成测试, 必须在场」, `:33` 另要求 SKILL.md 的事实性同步在 spec 里逐行点名并声明非指令语义变更。写法自检是结构化检查但不是本 spec 的 SC; 建议在该条补一句「找不到覆盖该 hunk 的 SC 级检查 ⇒ 按拿不准照跑」。
6. **读前必看第 4 条对 10CG/Aria#211 的引用行号已漂移**: #211 已于 2026-09-17 归档, T4 标 deferred (归档 proposal `:136`, SC-4 在 `:149`), 计划仍写「其 proposal `:135` / `:146`」。执行口径 (TASK-023 读 `origin/master` 上的文件、合并后复读) 不受影响。
7. **`commit_attribution` 在空区间上真空成立**: `kinds == []` 时 `all(...)` 为真 ⇒ `verdict ok, commits 0`。三个调用点里空区间都意味着「无可推 / 无可审」, 实际无害; 但 N9 没有这一态, 写进 `cannot_catch` 更完整。
8. **TASK-018 的四份 frontmatter 比较以 `<aria 起点>` 为基准**: TASK-025 / TASK-027 把上游并入后照样复跑; 若上游在 Phase B 期间合法改了这四份之一的 frontmatter, 会被当成本轨改动而停 (fail-closed 误停)。概率低, 记此备查。
9. **入口门事实未变**: `docs/handoff/latest.md` 的 track 表把 10CG/Aria#195 记为 `yielded (2026-09-17 交接) — A.2/A.3 已收口, B.1 待起`, owner_gates 第 1 项未满足。

## Verdict

**verdict: PASS** —— counts **0C/0M/2m**。

**Vote: PASS**

## 是否足以开始 Phase B

不足以: 就本席所审的分解、执行序、外向动作登记与发布段而言, v2.5 已无 major 缺陷, 但入口门 owner_gates 第 1 项 (10CG/Aria#195 完成 C.2 或 owner 明示改序) 仍未满足, 下一步是 owner 门而不是 B.1。
