---
track-id: session-close-20260924-199-post-planning-converged
owner-container: simonfish/bfe8285d
phase: D.3
status: done
updated-at: 2026-09-24T14:58:55Z
---

# Aria — Session Handoff (2026-09-21 ~ 24, 会话收尾) — `10CG/Aria#199` A.2/A.3: v2.4 → v2.6 三轮返修 + R5/R6/R7 三轮五席审计 → **post_planning 收敛**

> **一句话**: 接 09-20 那份往下, 全程一条轨 (`pre-merge-completeness-gate-change-scope`)。owner 六次裁定驱动**三版返修 (v2.4 / v2.5 / v2.6) 与三轮五席审计 (R5 / R6 / R7)**; R5 未收敛且 `max_rounds` 耗尽 → owner 选降级策略 [2] 增加轮次 (5 → 7) → R6 零 Major → v2.6 只修 minor → **R7 五席全票 PASS, `converged: true`**。16 个提交分九批双推。
>
> **本段最该记住的一件事**: 本仓 memory 原记「收敛只发生在无 Major 轮 + 下一轮**零返修**」被本轮证伪 —— 实际路径是「无 Major 轮 (R6) → 只含 **minor** 的返修 (v2.6) → R7 仍零 Major 且全票 PASS」。判据已修正为「无 Major 轮 + 下一轮无 Major 且全票 PASS」; 返修是否为零不是必要条件, 返修**只含 minor** 才是。

---

## §0 入口 (新 session 优先读)

1. 跑 `/aria:state-scanner`。主仓 master = `43e2326` (**本地领先两端 1 个提交** —— 第九批推送事实的回填提交, 待授权推); origin 与 github 均为 `3db3d23`。子模块 `aria` = `1cb3872` (v1.73.3) / `standards` = `940cb5b` / `aria-orchestrator` = `237045a`。
2. **开工第一件事: 查 claim 心跳年龄**。本轨 claim `claims/bfe8285d/s-73b9@1606.yaml` (phase A.2) 仍 `active`, 本次收尾前刷新于 `2026-09-24T01:09:38Z`。本 session 实测它曾停 **35.2h** (超 SWEEP_TTL 11 小时) 仍未被扫 —— 那是运气, 不是安全边界。
3. **本轨最新态在轨级 handoff**: [2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md](./2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md) —— 它已累积记到 R7 收敛, 待裁项与入口门以那份为权威; 本份只记会话层经过。
4. **收敛不等于可以开工**: `owner_gates` 第 1 项仍要求 `10CG/Aria#195` 已完成 C.2 合并或 owner 明示改序; 该轨仍 `yielded`、B.1 未起 ⇒ 下一步是 owner 门, 不是 Phase B。
5. 双子星 `simonfish/023236f2` 手上的 `10CG/Aria#195` 本容器不碰 (除非 owner 明示)。

---

## §1 已完成 (UTC)

| 时间 | 事件 | 证据 |
|---|---|---|
| 09-21 | owner 裁「R4 四题 Major 交执笔实例返修」+ 范围「四题 + 四条同处 minor」+「R4-M3 二选一由执笔按证据裁」→ **v2.4** (裁 (b): 工作区不入库) | `b686185` · `322c6df` · 回填 `cf05d8b` |
| 09-22 | **post_planning R5 五席**: 0C/5M/7m, 4 REVISE / 1 PASS, `converged: false`, `max_rounds` 5 耗尽; R4 四题五席一致 closed | `fffc5da` · `20bc77a` |
| 09-22 | owner 按 audit-engine 降级策略裁 **[2] 增加轮次** (本周期 `max_rounds` 5 → 7, 全局 config 不改) | 写回 `ad35d83` |
| 09-22 | owner 裁 v2.5 范围「Major + 同处 minor + 同族扫描」+ 执笔沿用 → **v2.5** (五题 + 两条同处 minor + 「空输出即通过」全计划同族扫描 160 候选改 46 条 + 9 张新建机制交互表) | `e7a1782` · `37335d4` |
| 09-22 | **post_planning R6 五席**: raw 0C/1M/4m → 聚合 0C/0M/5m, 4 PASS / 1 REVISE, 未收敛; R5 九项四席全 closed | `111d0ca` · `5f39105` |
| 09-24 | owner 裁「已知项 A 定级 minor」+「修全部五条 minor 后开 R7」→ **v2.6** (五条全闭合 + 三份机器清单: 序号引用 342 行 / 协调 ref 写入路径 8 条 / custom checks 16 条加 7 探针) | `320d523` · `9a3ac24` |
| 09-24 | **post_planning R7 五席: 全票 PASS, 0C/0M/6m ⇒ `converged: true`** —— 本周期最后一轮; R6 五条四席 closed (tl 判 `29325b2c` partially), km 自己在 R6 立的 Major 由其本人判 closed | `765b73b` · `8b596fc` · 补正 `3db3d23` · 回填 `43e2326` |

**Major 题数轨迹 (七轮)**: 10 → 5 → 4 → 4 → 5 → **0** → **0**。

---

## §2 未完成 / Carry-forward 清单

### 高优先级

| # | 项 | 说明 |
|---|---|---|
| H1 | **第十批推送** | `43e2326` (回填第九批推送事实) 仍在本地, 领先两端 1 个提交, 待 owner 授权双推 |
| H2 | **R7 六条 minor 与各轮未处置 minor 的处置时点** | 进 Phase B 之前一并做, 还是随 Phase B 首个返修一起做 |
| H3 | **三批执笔实例请裁** | v2.4 九条 / v2.5 十条 / v2.6 两条; 其中 v2.6 第 1 条 (C.2.4.5 的 override 走 trailer 还是 PR 标签) 与 R7 minor `3de4b245` 直接相关 —— 标签路不按子模块分, 一旦打上对本 PR 每个受影响子模块生效, 该代价计划里尚未写 |

### 中优先级

- **执笔报告与三份机器清单是否落仓** (R6 code-reviewer 指出的可审计性缺口): handoff 与 `revision_log` 引用的「160 个候选 / 9 张交互表」只在主控 scratch, 仓内产物无法复核「漏 0 多 0」。
- **插件侧两条 issue 候选** (是否开单待 owner): (1) state-scanner 的入口心跳触发条件写的是「本会话持 active claim」, 新会话不触发, 容器的 claim 跨会话老化无人刷; (2) 生产心跳在落后的本地协调 ref 上会静默失败 (心跳不自己 fetch, 非快进推送失败只记遥测), 与 `10CG/aria-plugin#197` 相关。
- **`submodule_gate.sh` 头注释与代码不符** (注释写「读 `.aria/config.json`, fallback warn」, 代码只读环境变量、缺省 block) —— aria 侧文档缺陷, 计划已以代码为准。

### 低优先级 / cleanup

- scratchpad 里多份约 190M 的副本 (三次返修副本 + 三轮审计共享副本 + 三态复跑环境), 随机器清理消失; 需要留存的都已落仓。

### 机械补漏 (autofill backstop)

- `unfinished` **189 条**, 分布与前两段一致 (八份 spec 的任务条目; 本轨 31 条是 A.2 计划自身的任务条目, **不是漏做**)。
- `consistency_check`: **8 条** `active_change_not_in_upm` advisory (本仓无运行时 UPM, 已知恒出)。
- `sync` 段告警两条: `[main] ahead 1 vs 两端`(= H1); **`[standards] parity=equal 但 evidence_grade=stale_unverified`** —— 本轮 `standards` 的 origin fetch 失败, 那个 `equal` 未经本轮验证, 不可当已同步。

---

## §3 关键风险 / 已知陷阱

1. **claim 心跳跨会话老化**: 实测停 35.2h 仍 `active` —— 未被扫只是那段时间没有容器跑 `--sweep-stale`。每个会话开工先查心跳年龄, 按「前置检查退出 0 → 强制对齐 → 重解析 → 心跳 → 推后核验」刷新 (v2.5/v2.6 已把该顺序写进计划)。
2. **origin (forgejo) 连接间歇失败**: 第六批推送出现**半推** (github 成功、origin `websocket: bad handshake`), 用普通快进补推修复、**未 force**; `ls-remote` 本身也会间歇取不到值 —— 重试几次再下结论, 不要据单次失败判「策略层阻断」。
3. **建隔离副本的两个陷阱**: `cp -a` 撞上瞬时 `.git/index.lock` 会非零退出, 挂在 `&&` 后的 gitdir 修正与禁推被**静默跳过**; 子模块 `standards` 的 `.git` 是**绝对** gitdir 指针, 不修则副本里的 git 操作写回真仓。修正后须在副本目录内逐个 `rev-parse --absolute-git-dir` 核验。
4. **本机 shell 的 `grep` 是 ugrep 包装**: CRLF 行尾下 `-x` 仍匹配, 与 GNU grep 相反 (R7 minor 之一; 计划里那句 CR 注解只在 GNU grep 下成立)。
5. **条目序号引用会随插条整体腐坏**: 本轨第三次 (「TASK-001 第 1 条」/「TASK-023 末条」/「TASK-024 末条」), v2.6 已改锚点式并留机器清单。

---

## §4 实战教训 (memory 沉淀来源)

1. **收敛判据被证伪并修正**: 「零 rework」不是必要条件 —— 纯 minor 返修夹在两个无 Major 轮之间不破坏收敛。
2. **返修带出新面是常态, 但可以降级**: 派单加「同族全量扫描 + 新建机制交互表」两项动作后, 下一轮的接缝类 finding 从 major 降到 minor, 且其中两处是执笔方自己在交互表里找出来的。
3. **核验者同样落在「修法带出的新面」盲区里**: 我逐项核验 v2.4 全过, R5 仍打出两条由 v2.4 修法引入的 Major。核验返修时除了问「修法落地没有」, 还要问「修法新建的东西与计划其它部分怎么交互」。
4. **多席产物的 id 不可采信**: R5 有一条席位登记的 finding id 在 288 种四元组组合下都复算不出; R7 有两席四元组完全相同而内容不同 (撞键)。聚合一律按内容四元组重算。
5. **零命中必须人工看原文**: 去重解析器三轮里三次对不同席位零命中 (三种新格式), 按规矩补族后才对上; 「零命中」当 0 条会静默丢掉整席的 finding。

---

## §5 多维度同步状态

| 维度 | 状态 |
|---|---|
| **OpenSpec** | 8 个活跃变更 (全 approved), 0 待归档; 本轨 `pre-merge-completeness-gate-change-scope` 停在 **A.2**, 计划 **v2.6**, post_planning **已收敛** |
| **User Story** | 21 份 (done 17 / in_progress 2 / approved 1 / pending 1) —— 本 session 未动 |
| **PRD / 架构** | 未动 |
| **Standards** | 未动 (`940cb5b`); 本轮 origin fetch 失败, 其 `equal` 未经验证 |
| **Skill / Plugin** | 未动 (aria `1cb3872`, v1.73.3) |
| **Memory** | 2 个新文件 + 4 处追记/修正 (见 §8) |
| **一致性 flag** | 8 条 `active_change_not_in_upm` (advisory, 本仓无运行时 UPM) |
| **Decision** | 无新决策单 (owner 六次裁定落在 handoff、聚合报告与 `revision_log` 里) |
| **CHANGELOG** | 未动 (本段零发版) |

---

## §6 Next session 入口 + 优先级建议

```
/aria:state-scanner
```

1. **先查 claim 心跳年龄**, 接近或超 24h 就按会话入口顺序刷新 (owner 2026-09-17 裁定: 本容器已有 claim 的心跳免逐次授权, 前提是前置检查退出 0 + 推后按 `coord_push_verify` 核验)。
2. **推第十批** (`43e2326`) —— 需 owner 授权。
3. **等 owner 裁的三件**: 六条 minor 与各轮未处置 minor 的处置时点 / 三批执笔请裁 (v2.4 九条、v2.5 十条、v2.6 两条) / 执笔报告与机器清单是否落仓。
4. `{id: handoff-multibranch-subdir-path-fidelity}` (`10CG/Aria#195`) —— 仍 `yielded`、B.1 待起, 是本轨 B.1 的入口前置; 谁接手谁先认领。

**不应该做的**:

- 不要把「post_planning 收敛」读成「可以开工」—— 入口门独立于审计结论。
- 不要擅自推送; 不要碰 `10CG/Aria#195` (除非 owner 明示改序)。
- 不要动 R7 未点名的各轮未处置 minor。

---

## §7 提交清单 (commit hash + multi-remote parity)

本段 **16 个提交** (`b686185` … `43e2326`), 分**九批**双推, 每批推后逐 remote 独立 `ls-remote` 核验:

| 批 | 提交 | 核验 |
|---|---|---|
| 四 | `b686185` v2.4 · `322c6df` handoff · `cf05d8b` 回填 | 两端 MATCH |
| 五 | `fffc5da` R5 产物 · `20bc77a` handoff | 两端 MATCH |
| 六 | `ad35d83` 写回 · `e7a1782` v2.5 · `37335d4` handoff | **首推半推** (github 成、origin `websocket: bad handshake`) → 快进补推修复、未 force → 两端 MATCH `37335d4` |
| 七 | `111d0ca` R6 产物 · `5f39105` handoff | 两端首次即 MATCH `5f39105` |
| 八 | `320d523` v2.6 · `9a3ac24` handoff | 两端首次即 MATCH `9a3ac24` |
| 九 | `765b73b` R7 产物 · `8b596fc` handoff · `3db3d23` 补正 | 两端首次即 MATCH `3db3d23` |

**当前**: 两端 `3db3d23`; 本地 `43e2326` 领先 1 (第十批待推, 见 §2 H1)。三个子模块 gitlink 全程未动。

---

## §8 Memory entries this session (2 new + 4 追记/修正)

**新增**:

- `feedback_git_sandbox_construction_traps` —— 造隔离副本与缺对象夹具的 git 陷阱 (子模块绝对 gitdir 使 `cp -a` 副本写回真仓; 本地路径 clone 无视 `--single-branch` 整库拷对象须用 `file://`); 后追记第三条 (`cp` 撞 `index.lock` 致 `&&` 链静默跳过隔离修正)。
- `feedback_session_scoped_heartbeat_misses_container_claim` —— state-scanner 心跳按「本会话持 claim」触发, 新会话不刷, 容器 claim 跨会话老化; 后追记 35.2h 实证。

**追记 / 修正**:

- `feedback_multiround_audit_catches_fix_introduced_regression` —— 两次追记: 核验者也会漏「修法带出的新面」(判据: 核验时逐个列新机制的读者与受影响方); 同族扫描 + 交互表两项动作见效但不消失 (严重度降到 minor)。
- `feedback_convergence_needs_zero_rework_round` —— **判据修正**: 「零 rework」不是必要条件, 关键是返修只含 minor。

**索引**: `MEMORY.md` 两处并入既有行, **零新增行**; 当前 24,385 字节, 逼近 24.4KB 硬上限 —— 下次加内容前需先合并同主题条目。

---

## Cross-references

- 轨级 handoff (待裁项与入口门的权威): [2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md](./2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md)
- 上一段会话收尾: [2026-09-20-session-close-199-r3-r4-two-rework-rounds.md](./2026-09-20-session-close-199-r3-r4-two-rework-rounds.md)
- R5 / R6 / R7 聚合: `.aria/audit-reports/post_planning-R{5,6,7}-*-pre-merge-completeness-gate-change-scope-aggregated.md`
