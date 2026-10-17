> 本评论是按 owner 2026-09-30 决策单第 6 项 (10CG/Aria 仓 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 的「记入待办」一节: 疑似已修未关的 issue 先 triage 核验, 再评论 / 关闭) 做的卫生清扫核验, 结论基于 aria-plugin v1.74.1 (`268da8f`) 与 10CG/Aria 主仓 `0748dbc`。核验全程只读: 复现在隔离实验目录的合成 fixture 上完成, 未改动任何仓内文件, 未做 git 写操作, 未对真仓执行 scan; 结论另经一位独立席位对抗核验。

## Triage Report

**Verdict**: `fixed-in-X` | **Severity**: `minor` | **Recommended Action**: `backlog`

**结论**: issue 报告的核心缺陷 (本地 remote-tracking ref 陈旧时, `sync_status` 谎报 `parity=equal` / `overall_parity=true`) 已在 aria-plugin v1.60.0 / v1.62.0 修复; 拆出的姊妹 Spec B / C 已分别在 v1.58.0 / v1.57.0 ship, 三个 Spec 均已归档。相关提交全部位于 aria-plugin 的 `origin/master` 与 `github/master` (两端 `git ls-remote` 均为 `268da8f`)。

但本单**不满足「全部诉求已修」, 建议保持 open, 暂不关闭**。共 7 项未了结 (下文「未修子项」同号):

1. 全局 deadline 在生产路径不生效 —— 新发现, 已复现, 尚无 issue 跟踪。
2. Spec B 的 lint 对同名变量有盲区 —— 新发现, 当前没有泄漏 (潜在盲区), 尚无 issue 跟踪。
3. v1.62.0 为本单加入的 AC-5 检测器, 在「主仓单 remote + 子模块多 remote」布局下对健康仓库恒报 `snapshot_consistency_inconclusive`、退出码恒为 10 —— 已由 10CG/Aria#176 跟踪, v1.74.1 上仍存在。

另有 4 项已知残余 (下文第 4 到 7 项: AC-5 裁决级、`_aggregate_flags` 零生产调用点、AC-15 防饥饿、两项人工审计产出), 均已挂在 10CG/Aria#168。

**Severity / Recommended Action 的含义**: 评的是核验后**仍未解决的部分** —— 单项均无假绿、无数据损坏, 按 minor 评估, 所以 Recommended Action 取 `backlog` 而不是 `close`。原缺陷本身 (已修) 按量表属 major: 功能错误, 评论 16240 记录过一次约 2 小时 / 9 个 subagent 的重复劳动代价。

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.56.0` (collector 从正文 "v1.56.0 / v1.56.1" 抽取首个; 实际缺陷基线是 v1.56.1 = `0964496`) |
| Current | `1.74.1` (`268da8f`) |
| Gap | behind (18 个 minor) |

issue 创建于 2026-07-12, 早于全部修复; 修复效果在现行 master 上保持 (见 Reproduction)。

### Code Path

路径约定: 下文未标注仓名的文件路径, 均为 10CG/aria-plugin 仓内相对路径 (该仓在 10CG/Aria 主仓里以子模块 `aria/` 挂载)。collector 对 `scan.py` / `multi_remote.py` / `DEFAULTS.json` / `sync-detection.md` 报 "file not found", 是它没有把 issue 里的裸文件名解析到 monorepo 路径, 不是代码缺失。实际位置: `scan.py` 在 `skills/state-scanner/scripts/`; `multi_remote.py` / `remote_refresh.py` / `sync.py` 在 `skills/state-scanner/scripts/collectors/`; `sync-detection.md` 在 `skills/state-scanner/references/`; 测试在 `skills/state-scanner/tests/`; `DEFAULTS.json` 在 `skills/config-loader/` (不在 state-scanner 下)。

手工核对:

- 基线 `0964496` (v1.56.1) 上 issue 所引行号全部属实: `scan.py:106` (sync) 早于 `:119` (coordination fetch 的真 fetch); `multi_remote.py:371` 的 `_aggregate_flags` 只读 parity; `:130-142` 的 `_fetch_head_age_hours` 在 FETCH_HEAD 缺失时返回 None, `:497` 据此判「不陈旧」; `:494-507` 的 `local_refs_stale` 仅咨询; 非测试 `.py` 对 `enforced_remotes` 的引用为 0 处 (只有 `DEFAULTS.json` 声明)。
- 当前 `268da8f`: Phase 0.5 的 `collect_remote_refresh` (`scan.py:321`) 先于 `collect_git_state` (`:322`)、`collect_multi_remote` (`:340`)、`collect_sync_state` (`:341`), Phase 1.16 降为纯派生 (`:356`); `_overall_parity` (`multi_remote.py:1128`) 的存在性子句要求 `parity==equal` 且 `evidence_grade=="fresh"`; `_fetch_head_age_hours` 与 `local_refs_stale` 已退役 (`multi_remote.py:46`、`:325` 的退役说明); `enforced_remotes` 在非测试 `.py` 里有 32 处引用 (如 `remote_refresh.py:302-311`、`multi_remote.py:1375-1388`), `sync-detection.md:530` 已如实描述。

### Git History

collector 的 `likely_fix_candidates` 只命中开票提交 `8cc43ab` (10CG/Aria 主仓的 docs 提交, 非修复)。手工 `git log` 在 aria-plugin 仓找到实际修复, 均为 `268da8f` 的祖先, 同时包含于 `origin/master` 与 `github/master`:

| 内容 | 版本 | 提交 |
|------|------|------|
| Spec C: 快照 `generated_at` + `issue-cache-freshness` 重定义 | v1.57.0 | `a9e8652` |
| Spec B: git stderr 类型化通道 (Rule #7) | v1.58.0 | `cae92e8` |
| 主 Spec Phase 0: `resolve_enforced_remotes` / `sync_freshness.*` 键 / 谓词域表 | v1.59.0 | `e2a2b22`, 发版 `a537e7d` |
| 主 Spec 核心: `remote_refresh` (Phase 0.5) / `evidence_grade` 双角色谓词 / gitlink 可达性 / sync.py 消费新鲜度 | v1.60.0 | `099c63c` `e8499fa` `a984bfe` `64f6e84` `ec2eff8`, 发版 `e162f7b` |
| 主 Spec Phase 4: enforced / read_only 接进裁决 / 退役 ls_remote / 非交互 git / AC-5 检测 | v1.62.0 | `c7a5400` `5603e52` `ee3e388` `bacb4a0`, 合并 `9af7b21` (10CG/aria-plugin#115) |
| session-closer 的 handoff 对 `stale_unverified` 下的 `parity=equal` 不再静默 | v1.62.1 | `6e1eb24` |
| 删除死配置键 `warn_after_hours` + 跨 skill 测试入口 | v1.62.2 | `aadd56e` |

注: v1.57 到 v1.62 各版本在两端 remote 上都没有对应的 git tag (v1.57 到 v1.65 之间没有任何 tag, 下一个 tag 是 v1.66.0), 版本归属以 `CHANGELOG.md` 条目与 `chore(release)` 发版提交为准。

主仓侧 (10CG/Aria): 三个 Spec 均已归档到 `openspec/archive/` (2026-07-16 的 `state-scanner-snapshot-stderr-secret-leak` 与 `state-scanner-issue-cache-freshness-assertion`, 2026-07-19 的 `state-scanner-stale-refs-false-parity`); 主仓 `origin/master` 与 `github/master` 均为 `0748dbc`, gitlink 指向 `268da8f`。

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (10CG/aria-plugin / 10CG/Aria / 10CG/aria-standards / 10CG/aria-orchestrator 四仓 open PR 均为 0) |
| Local branches | collector 只查主仓, 得 none; 但 aria-plugin 仓 (主仓里的 `aria/` 子模块) 残留本 Spec 的分支 `feature/state-scanner-stale-refs-false-parity`: 本地 `a537e7d` / origin `3be481c` / github `e2a2b22`, 三者均为 `268da8f` 的祖先, 无未合并工作 |
| Worktrees | 仅主工作树 (与本 issue 无关) |

协调板 (Layer L) 上链到本 issue 的 claim 均已不是 active: 3 条 `yielded` (2026-07-14) 与 1 条已归档的 `done` (2026-07-17)。没有任何在飞的 Spec 或计划依赖本单保持 open。

相关 open issue: 10CG/Aria#168 (主 Spec 归档 deferred 项 tracker)、10CG/Aria#169 (AC-5 位置重构)、10CG/Aria#176 (AC-5 检测器恒红, 见未修子项第 3 项)、10CG/Aria#165 (预防侧, 与本单正交)、10CG/aria-plugin#109 (协调层, disjoint)、10CG/aria-plugin#157 (AB 断言的得分路径会把 Phase 0.5 强制 fetch 推回去, 见下「相关风险」)、10CG/aria-plugin#184 (`state_scanner.sync_check.*` 死配置, 与本单正文的「死配置 + 假文档」同族)。

### Reproduction

**Mode**: `auto` | **Hit rate**: `1/12` (match=true 表示缺陷在当前版本仍复现; 唯一命中的 case 10 属于方案里的子项, 不是 issue 报告的症状本身)

方法: 隔离实验目录 (env -i, 独立 HOME), 本地裸仓充当 remote, 无网络、无凭据; 每个场景用基线 `0964496` (v1.56.1) 与当前 `268da8f` (v1.74.1) 各扫一份互相独立的 fixture 副本。基线必须先复现出缺陷 (证明 fixture 有判别力), 当前的结果才有意义。

| case | 场景 | 基线 v1.56.1 | 当前 v1.74.1 | 仍复现 |
|------|------|--------------|--------------|--------|
| 1 | 落后 4 commit, FETCH_HEAD 回拨 14h (事故形态) | `overall_parity=True`, 两 remote `equal`, `current_branch.behind=0` | `False`, 两 remote `behind` (`evidence_grade=fresh`), `current_branch.behind=4` | 否 |
| 2 | 同上, FETCH_HEAD 回拨 7 天 (评论 16240 形态) | `True` + `local_refs_stale` (仅咨询) | `False`, `behind` | 否 |
| 3 | 7 天前的缓存 + remote 不可达 | `True`, `has_unreachable_remote=False` | `False`, `has_unreachable_remote=True`, 两腿 `expired` / `not_refreshed` | 否 |
| 4 | 从未 fetch + remote 不可达 | `True`, 两 remote `equal` | `False`, `fetched_at=null` 判 `expired` | 否 |
| 5 | 子模块挂分支、从未 fetch、上游前进 3 commit | `True` (sub `equal`) | `False` (子模块被 fetch, `behind`) | 否 |
| 6 | 已发布 gitlink 在镜像上不可达 (2026-07-12 事故形态) + 健康对照 | `True`, 无 `gitlink_integrity` | `False`, github/sub=`orphaned`; 对照组 `True`, ok/ok | 否 |
| 7 | Rule #7: 假哨兵经 git stderr 回显 | `errors[].detail` 与 stderr 均含哨兵 | 均无, 仅有界标签 | 否 |
| 8 | `enforced_remotes` / `read_only_remotes` 配置 | 代码零消费 | 配置改变参与集与 fetch 范围 | 否 |
| 9 | 并行 + per-host 限流 (每次 fetch 人为 2s, 8 腿同 host) | - | limit=4: 7.5s (串行约 18s); limit=2: 11.4s | 否 |
| 10 | 全局 deadline (deadline=1s, 每次 fetch 2s) | - | 4 腿 limit=1: 4/4 全部 fetch, `skipped_count=0`, 10.6s; 8 腿 limit=2: 8/8, 11.4s | **是** |
| 11 | Spec C: `generated_at` / `issue-cache-freshness` | 无 `generated_at` | 有; 真仓最近快照上探针 OK, check pass | 否 |
| 12 | pin 测试判别力 (3 个变异: 改回正向枚举 / 去掉 fresh 门 / 破坏 unreachable 判定) | - | 3 个变异均被抓 (failures 分别为 3 / 1 / 1+1) | 否 |

核验阶段的补充复核 (不计入命中率):

1. **deadline 进程内复核**: 把 `_do_fetch_leg` 替换成 sleep 2s 的桩 (不触网、不落盘), 直接调 `remote_refresh._run_schedule`。4 腿同 host、limit=1: deadline=1s 耗时 8.0s 且 4/4 腿准入; deadline=0.05s 结果相同; deadline=1 微秒 4 腿全部 not_attempted。核验席位用 git shim 独立复现 (deadline=1s, 4 腿 10.8s, 4/4 fetch), shim 日志显示后三条腿分别在约 +2.0 / +4.1 / +6.1s 才起跑, 均晚于 1s deadline 却没被切。
2. **Spec B lint**: 见未修子项第 2 项 (25 个站点 / 12 个未被检查 / 按函数粒度重跑零违规)。
3. **AC-5 检测器在单 remote 主仓 + 双 remote 子模块布局下恒红**: 核验席位在 `268da8f` 上用合成 fixture 复现: 主仓仅 `origin`、子模块 `origin` + `github`, 结果 `overall_parity=true` 而 exit code 10, 唯一错误是 `snapshot_consistency_inconclusive` (remote=`github`); 去掉子模块 github 的对照组 exit 0。代码侧见未修子项第 3 项。
4. **真仓最近一次真实扫描** (v1.74.1, `generated_at=2026-09-30T17:40:14Z`; 10CG/Aria 主仓工作副本的 `.aria/state-snapshot.json`, git 忽略的本地产物, 只读): 含 8 条腿 (主仓 + 3 个子模块, 各 origin / github) 的 `fetched_at` / `fetch_ok` / `error_kind`, `skipped_count=0`。其中 aria/github 一腿本次 fetch 失败 (`error_kind=other`, 上次成功 14:20:53Z, `consecutive_unverified=1`), 降为 `stale_unverified`; `gitlink_integrity` 里 github/aria 为 `orphan_unverified` (按设计暂不阻断: 计数到 `k_eff`, 默认 3, 才升级为阻断)。`overall_parity` 仍为 true 而 `has_unreachable_remote=true` (可达性与新鲜度两轴独立); `issue-cache-freshness` 检查 pass。
5. **全套件**: state-scanner `1650 tests OK (skipped=13)` (带 git 父根的隔离副本实跑; 无 git 父根时有 2 个依赖环境的测试失败, 与本单无关)。

### 未修子项 (建议保持 open)

**1. 全局 deadline 在生产路径不生效 (新发现, 已复现, 尚无 issue 跟踪)**

- 来源: 本 issue 正文「影响面」一节对行为变更的描述 (「并行, per-host 限流, 全局 deadline」); 主 Spec (10CG/Aria 仓 `openspec/archive/2026-07-19-state-scanner-stale-refs-false-parity/`) 的 F3′「网络成本必须有硬上界」(`proposal.md:343`) 与 tasks 3.5a′「已起跑的 fetch 允许跑完, 只砍未起跑腿」(`tasks.md:90`)。归档 tasks.md 里 1.9 / 3.5a′ / 3.5c 均已勾选。
- 实测 (case 10 与上面的补充复核): `refresh_deadline_seconds=1`、每次 fetch 2s、4 腿 (limit=1) 耗时 10.6s, 4/4 腿全部 fetch, `skipped_count=0`; 8 腿 (limit=2) 11.4s, 8/8。只有测试专用 seam `ARIA_SCAN_FETCH_BUDGET` 才会切腿。对照 (排除「配置没被读取」): deadline 设为 1 微秒时 4 腿全部被切, 说明配置被读取且在准入处比较; 设为 0.05 秒时 4 腿仍全部 fetch, 即准入循环耗时在微秒量级, 任何实际取值都触发不了。
- 根因: `remote_refresh.py:508-518` 的准入循环在 `submit()` (`:515`) 之前顺序调用 `_should_stop_admitting` (`:510` 调用, 定义在 `:450`), 而 `ThreadPoolExecutor.submit` 不阻塞, 所有腿在 t 约等于 0 就被准入, 生产分支 `elapsed >= deadline` 结构性不可达。`tests/test_remote_refresh.py:460-495` 用 mock 的 `time.monotonic` 序列 `[100.0, 100.0, 100.0, 100.0, 200.0]` 阶跃驱动该分支, 所以全绿 —— seam 与 mock 时钟都绕开了真实触发条件。
- 影响: 不会造成假绿 (多 fetch 只会更新鲜); 但 `refresh_deadline_seconds` 对扫描耗时没有约束力: 同一 host 的腿数超过 `per_host_fetch_limit` (默认 4) 时, 排在队列里的腿本应被 deadline 砍掉却照常执行, 最坏耗时约「该 host 腿数 / limit 向上取整」乘以 `fetch_timeout_seconds` (默认 30s)。同 host 腿数不超过 limit 时所有腿 t=0 同时起跑, 无论准入是否生效都不会有腿被砍 —— 本仓 8 腿 (每 host 4 腿) 属此类, 所以 dogfood 没有暴露 (这一点由代码推断, 未另行实测)。
- 同样失真的文字: `state-snapshot-schema.md:614` / `:621` 与 `output-formats.md:642` 所述「被 `refresh_deadline_seconds` 砍掉」及 `skipped_count`、`CHANGELOG.md:898` (v1.60.0 条目的「deadline-bounded ... Legs cut by the deadline report `not_attempted`」)、`remote_refresh.py:5` 模块 docstring 的「wall-clock-deadline-bounded」; 这些情形在任何实际取值下都不会出现 (只有微秒量级的取值才会切腿)。同一归档目录下的 `dogfood-evidence.md` 4.2 节只记了「本仓 6-8 腿, 未触及 deadline 砍腿」, 没有披露该分支在生产路径不可达。
- 建议: 让准入按 worker 实际空闲的节奏发生 (每 host 信号量 / 有界队列, 在腿真正起跑前判 deadline), 并补一条不 mock 时钟、用慢 fetch (如 git shim) 的真实时间测试。修它会让第 6 项 (3.16 / 3.5d) 从休眠变为生效, 宜一并考虑。
- 「尚无 issue 跟踪」的依据: 2026-09-30 对 10CG/aria-plugin 与 10CG/Aria 两仓全部 issue (含已关闭, 不含 PR; 共 260 条) 及其评论 (共 340 条) 做了关键词全文扫描 (`refresh_deadline` / `_should_stop_admitting` / `not_attempted` / `skipped_count` / `deadline` 等), 未见对应记录; 仅有的字面命中来自截止日期、issue_scan 分页、Layer L 状态集等无关议题。

**2. Spec B 的 lint 对同名变量有盲区 (新发现, 潜在, 尚无 issue 跟踪)**

- `skills/state-scanner/scripts/lint_stderr_typed_channel.py:46` 以变量名作 dict 键 (`out[third.id] = func`): 同一文件里多个函数对 `_run` 返回值的第三个元素用同名变量 (典型是 `err`) 时, 只检查最后一个函数。合成源码复现: 两个函数共用 `err`, 泄漏写在前一个函数里 lint 不报 (返回空列表), 写在后一个函数里才报。
- 实测 4 个 in-scope 文件 (`git.py` / `sync.py` / `handoff_multibranch.py` / `handoff_worktrees.py`, 均在 `skills/state-scanner/scripts/collectors/`) 共 25 个 `_run` stderr 赋值点, 其中 12 个因同名被覆盖而未被 lint 检查; 按函数粒度重跑同一规则, 当前零违规 —— 即现在没有隐藏的泄漏, 属潜在盲区。
- 该盲区不在 Spec B 已声明的 known gaps 里 (整元组透传 / 已结构化的 reason 字段分类器 / 经中间变量再发射), 且属本单正文列出的 Spec B (Rule #7) 范围; 同样没有 issue 跟踪。

**3. AC-5 检测器在「主仓单 remote + 子模块多 remote」布局下恒红 (已跟踪: 10CG/Aria#176, open)**

- 症状: 健康仓库每次扫描都在 `errors[]` 里得到 `snapshot_consistency_inconclusive`, 退出码从 0 钉死在 10; 该检测器是 v1.62.0 (`bacb4a0`, 10CG/aria-plugin#115) 为本单加入的。这正是本单正文「对偶不变量」要防的形态 (假绿的反面是恒红), 出现在检测层而不是 parity 裁决层。
- 代码: `scan.py:192` 遍历的 `enforced_remotes_resolved` 是 `multi_remote.py:1529` 对主仓与各子模块的 remote 名取的并集, 没有按主仓实际存在的 remote 过滤; 子模块独有的 `github` 在主仓里不存在, `git log github/<branch>` 返回 128, 被记成 inconclusive。判定集与检测集不一致, 违反 `_same_branch_head_unreachable_tracks` docstring 自己写的「Detection set and verdict set must be the same set」。
- 状态: 10CG/Aria#176 创建于 2026-08-08 (报告版本 aria-plugin 1.63.0), 至今 open、零评论; 核验席位在 `268da8f` 上复现 (见上补充复核第 3 条)。

**4. AC-5 裁决级未实现 (已跟踪: 10CG/Aria#168; 位置重构 10CG/Aria#169)**: `scan.py:394-403` 只向 `errors[]` 追加 `snapshot_self_contradiction`, 不改 `overall_parity`、不写 reason; `CHANGELOG.md:838` 已如实标「advisory 级, 非裁决级」。该 kind 也未写入 `state-snapshot-schema.md` 与 `output-formats.md` (两份文档零命中; 另仅 CHANGELOG 与 `tests/test_scan_integration.py` 提及), 且 `output-formats.md` 不渲染 `errors`, 使用者侧与未实现不易区分。原事故的根因 (顺序倒置) 已消除, 所以这是兜底检测层的缺口, 不是事故复发。

**5. `_aggregate_flags` 零生产调用点** (task 5.5, 已跟踪: 10CG/Aria#168): `multi_remote.py:1169` 只剩定义, 被 `tests/test_multi_remote.py` / `tests/test_multi_remote_mocked.py` 引用, docstring 已标为遗留参考实现; 删除或保留待 owner 裁定。

**6. AC-15 防饥饿的两个失效源** (task 3.16 `k_eff` 的 `observed_rotation` 持久化 DEFERRED、task 3.5d 永久失败 leg 退避未做; 已跟踪: 10CG/Aria#168, 该 tracker 已写明「不得记 AC-15 已完全满足」)。受第 1 项影响目前处于休眠态 (生产中没有腿被砍, 防饥饿的前提场景不出现)。

**7. 人工审计产出 3.10 / 13.7** (15 个 collector 的先后依赖核对表、gitlink contains 性能实测附表; 已跟踪: 10CG/Aria#168)。归档 tasks.md 里另外未勾的 7.2 与 11.1 已在 10CG/Aria#168 的评论 16363 / 16389 中结案, 不计入残余。

**相关风险 (不属本单诉求, 但与本单的修复存续相关)**:

- 10CG/aria-plugin#157 评论 22501 指出: state-scanner 的 AB 断言 A4 (10CG/Aria 仓 `aria-plugin-benchmarks/ab-suite/state-scanner.json:96`, 2026-09-30 核对仍在, suite v1.7.0) 唯一的得分路径是去读已 DEPRECATED 的 `remote_refs_age`, 按 AB 分数做优化会把 Phase 0.5 的强制 fetch 拆掉, 即把本单的修复推回去; 该评论已建议升 P0, 尚未见裁定。
- 10CG/aria-plugin#184: `state_scanner.sync_check.*` 是死配置, 268da8f 上仍由 `skills/config-loader/DEFAULTS.json:38` 下发、`skills/config-loader/SKILL.md:67-75` 仍在教用户配置, 与本单正文的「死配置 + 假文档」同族。

### 已核实已修的子项 (摘要)

1. 症状与四条根因: 顺序倒置 (Phase 0.5 先 fetch)、陈旧度不参与裁决 (`evidence_grade` 进入 `_overall_parity`)、子模块零覆盖与「从未 fetch 当最新鲜」(子模块纳入 `remote_refresh`, `fetched_at=null` 判 `expired`)、无 per-remote 新鲜度信号 (改为获取, 每腿记录 `fetched_at` / `fetch_ok` / `error_kind`)。见 case 1 到 5。并行 fetch + per-host 限流见 case 9。
2. `enforced_remotes` 死配置 + 假文档: 现为承重, 文档已更正 (case 8)。`sync.py` 这个第三个平行的 ref 读取点: `current_branch` 与子模块 drift 现带 `evidence_grade` (`collectors/sync.py:124` / `:293`), 与 `multi_remote` 同向, US-008 方向护栏逐字节未动。
3. **子模块镜像 —— 部分修复, 字面症状按设计保留**: 有害形态 (已发布 gitlink 在镜像上不可达, `clone --recursive` 会断) 现被 `gitlink_integrity` 报出并阻断, 且健康对照下 `overall_parity` / `gitlink_integrity` 不过冲成恒红 (case 6; 真仓 dogfood 时该正向腿曾为 vacuous, 此处为端到端实证; 相邻 AC-5 检测层的恒红见第 3 项未修子项)。按 DEC-20260712-001 D14 (10CG/Aria 仓 `docs/decisions/`, owner 终审 2026-07-15) 与 AC-17(d), 「镜像纯落后而 gitlink 仍可达」不报警, 实测 `overall_parity=True`、gitlink ok, 与规格一致。所以正文「镜像落后 32 commit 完全没报」的字面症状, 在 gitlink 仍可达的形态下按设计保留。这不等于该形态无害: 同一份 DEC 的 D7 盲区注记 (`DEC-20260712-001-state-scanner-stale-refs-false-parity.md:203`) 写明镜像领先本身即危害 (镜像陈旧 / 市场版本滞后 / `clone --recursive` 断裂), D14 只覆盖其中 `clone --recursive` 断裂这一面; 若 owner 认为纯镜像落后也须报出, 应另起诉求。
4. Spec B (case 7): `test_stderr_typed_channel` 16 测 OK, lint 对当前树 exit 0; lint 的同名变量盲区见未修子项第 2 项。
5. Spec C (case 11): `test_issue_cache_freshness` 22 测 OK; 10CG/Aria 仓的 `.aria/state-checks.yaml` 已使用 `issue-cache-freshness`, 最近快照上该 check 为 pass。
6. fail-CLOSED 不变量机制化 (case 12): `tests/test_mainspec_phase1_f1_f4.py:138-160` 用代码里不存在的 reason 值 (timeout / network / permission_denied / git_error) 必须判 blocking; 三个变异均被抓。
7. 评论 16240 (7 天陈旧窗口, follower 容器): 见 case 2, 两条治本路径 (fetch 前置 `scan.py:321` / 陈旧参与裁决 `multi_remote.py:1128`) 均已落地。评论 15789 (与预防侧 10CG/Aria#165 正交、合起来才闭环): 10CG/Aria#165 仍 open, 由它自行跟踪; 检测侧的 orphaned-gitlink 谓词已落地。
8. 下游 `aria-2.0-m7-fleet-aggregation` (10CG/Aria 仓 `openspec/changes/`): CAVEAT-age / CAVEAT-parity 已同步 (提交 `36050cc` / `78057be`); 小瑕疵: `proposal.md:149` 的 CAVEAT-parity 仍写「待合并/归档」。
9. 流程项: 主 Spec 终态 Approved v10 (R9 PASS-with-fixes, owner 终审 2026-07-15), DEC-20260712-001 Approved。

### Verdict Rationale

按 issue 原形态 (14h / 7 天陈旧、从未 fetch 的子模块、镜像上 orphaned 的 gitlink、remote 不可达) 逐一复跑, 基线 `0964496` 全部复现假绿, 当前版本全部据实报出, 所以 issue 报告的核心缺陷已修, verdict 为 `fixed-in-X`。但同一轮核对发现, 方案里的「全局 deadline」在生产路径并未生效 (case 10), Spec B 的 lint 有未声明的盲区, 本单修复引入的 AC-5 检测器在特定布局下恒红 (10CG/Aria#176), 且 AC-5 裁决级、AC-15 防饥饿、`_aggregate_flags` 处置、两项人工审计产出仍是已跟踪的未完成项, 因此建议保持 open。

下一步: 保持 10CG/aria-plugin#110 open。第 1、2 项两项新发现尚无 issue 跟踪, 新开 issue 超出 owner 2026-09-30 决策单第 4 项的一次性授权范围 (feature 分支推送 / 开 PR / issue 评论 / issue 关闭), 已提请 owner 决定: 新开 issue (建议在 10CG/aria-plugin 单独立项), 或并入 10CG/Aria#168。在这两项有了跟踪之前不宜关闭本单, 否则它们会从视野里消失; 其余残余已分别由 10CG/Aria#168 / 10CG/Aria#169 / 10CG/Aria#176 跟踪, 所以这两项有了跟踪之后, 按现有证据本单即可按 `fixed-in-X` 关闭 (是否关闭、何时关闭由 owner 定)。
