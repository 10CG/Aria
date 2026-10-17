本评论是按 owner 2026-09-30 决策单 (10CG/Aria 主仓的 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`) 第 6 项「记入待办」里的 issue 卫生清扫做的核验 (先 triage 核验, 再评论 / 关闭; 该项明记评论与关闭属第 4 项的一次性授权范围), 目的是确认 `10CG/aria-plugin#194` 是否已修。结论: 已修复并已随 v1.73.1 发布, 现行 v1.74.1 仍含修复, 建议关闭; 关闭理由、重开条件与相邻发现见文末。下文 SHA 与行号以核验时 (2026-09-30) 的 aria-plugin master `268da8f` 与 10CG/Aria master `0748dbc` 为准。

## Triage Report

**Verdict**: `fixed-in-X` (X = aria-plugin v1.73.1) | **Severity**: `major` | **Recommended Action**: `close`

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.73.0` |
| Current | `1.74.1` (aria-plugin master `268da8f`, origin 与 github 两端 `git ls-remote` 一致) |
| Gap | behind |

issue 正文没写版本号, `1.73.0` 是 triage.py 从评论 23170 的文字里取到的 (该评论写有「已发布的 v1.73.0 仍是红的」与「`plugin.json` 仍 1.73.0」), 与开单日的 master 一致: tag `v1.73.0` 指向 `6726df1`, 恰是修复提交 `f314785` 的父提交, 所以 issue 复现的正是 v1.73.0 这份代码, 本次核验原样复现了它 (见 Reproduction)。此后已有 5 个发布: v1.73.1 / v1.73.2 / v1.73.3 / v1.74.0 / v1.74.1。

### Code Path

路径约定: 除注明仓名外, 下文路径均为 10CG/aria-plugin 仓内相对路径 (该仓在 10CG/Aria 主仓里是子模块目录 `aria/`)。

triage.py 在 10CG/Aria 主仓根运行时, step3 把 16 条引用路径全判为 `file not found`, step4 因此 skipped (`likely_fix_candidates: []` 是空转)。原因有两层: 仓根不对 (aria-plugin 在主仓里是子模块), 且 issue 里不少路径写的是 `skills/state-scanner/` 目录内的相对路径 (如 `lib/collision.py:232`) 或裸文件名。为交叉验证, 另从 aria-plugin 仓根运行了一次 (独立输出文件, 非正式报告): 5 个 step 均 ok, step4 机械命中 `f314785` (唯一带 issue 引用命中的候选, 其余 4 条是泛 `fix` 关键词噪声), step3 只解析到 2/16 条 (其余是上述相对写法)。所以下面是逐条人工核对, 引用与 HEAD 一致:

- `skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py`: 现状 16 个 collector 调用点全部带 `now=_FIXED_NOW` (行 276 / 327 / 363 / 388 / 436 / 483 / 547 / 642 / 683 / 729 / 783 / 828 / 951 / 1007 / 1219 / 1238; 修前 v1.73.0 这 16 处一处都不钉), `_FIXED_NOW` 在 `:173`, 回归锁类 `TestCollectorClockIsPinnedInThisFile` 在 `:1028`。
- 生产侧: `skills/state-scanner/scripts/collectors/handoff_multibranch.py:627` 的 `now` 形参一直存在 (注释逐字 `tests pin it`; 行号因文件增长, 从评论 23108 引的 `:556-560` 漂移到 `:623-628`, 透传 `:726` 现为 `:829` / `:830`); `skills/state-scanner/lib/collision.py:225` 的 `layer_h_is_fresh` 缺省回退真实墙钟 (`:232`); `skills/state-scanner/lib/constants.py:88` 的 `LAYER_H_ACTIVE_WINDOW_DAYS = 30`。与 issue 的根因描述一致, 且这些生产文件未被修复提交改动 (修复提交只改了 1 个测试文件)。
- `skills/state-scanner/tests/test_collision.py:439` / `:460` 的 `now=` 正确先例仍在。该文件另有一个与本单无关的问题, 见文末相邻项第 2 条。

### Git History

下列提交均已逐端核验 (`git ls-remote` 取两端 SHA, 再 `git merge-base --is-ancestor`, 不信 push 回执):

| 提交 | 内容 | 两端核验 |
|------|------|----------|
| `f314785` (aria-plugin, 2026-09-09) | 修复: 16 处 collector 调用点补 `now=_FIXED_NOW` + 2 条回归锁 (+82/-17, 仅 1 个测试文件, 生产码零改动) | aria-plugin origin 与 github 的 master 均为 `268da8f`, 它是祖先; `git tag --contains` 得 v1.73.1 / v1.73.2 / v1.73.3 / v1.74.0 / v1.74.1, 不含 v1.73.0 |
| `c02b0ef` (10CG/Aria 主仓, 2026-09-09) | 主仓 gitlink `6726df1` -> `f314785` | 是主仓 master `0748dbc` (origin == github) 的祖先; 所指 `f314785` 两端可达, 非 orphaned |
| `44f00d1` (aria-plugin, 2026-09-12) | `chore(release): v1.73.0 -> v1.73.1`, 改 6 个版本文件, CHANGELOG `[1.73.1]` 点名本单 | annotated tag `v1.73.1` = `83c0ffd` -> `44f00d1`, origin 与 github 两端 `ls-remote` 一致 |
| `5990b85` (10CG/Aria 主仓, 2026-09-12) | 主仓发版同步面 + gitlink `f314785` -> `44f00d1` | 是主仓 master 的祖先 |
| `9f3b05b` (aria-plugin, 2026-09-26) | 此后对该测试文件唯一的改动: 2 处 docstring 措辞 (`10CG/Aria#195` TASK-020), 修复与锁原样保留 | 在 `268da8f` 的历史上 |

`f314785` 的提交说明带 `rule6_note`: 纯测试文件改动, SKILL.md 与 `description` 零变动, 落 Rule #6 判据表第一行, substitute 为 baseline-failing 结构化测试。该 substitute 所要的 baseline-failing 证据本次独立复现了: 修前 7 红, 修后 0 红。

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (10CG/aria-plugin 与 10CG/Aria 的 open PR 均为 0, forgejo GET 实测) |
| Local branches | 无相关。triage.py 按关键词命中的两条均已并入对应 master: 主仓根运行命中 `origin/feature/owner-container-identity-key-and-collision-parser`, aria-plugin 仓根运行命中本地 `feature/reconcile-yielded-terminal-fix`。两仓其余未并入 master 的远端分支 (aria-plugin 仓: secret-guard 与 exfil 语料共两条; 10CG/Aria 仓: `aria/DEMO-001` / `aria/DEMO-002`) 与本单无关 |
| Worktrees | 仅主 checkout |

10CG/Aria 仓 `openspec/changes/` 下没有任何文件引用本单, 没有在制计划依赖本单保持 open。

重复核查: 两仓全部 issue (aria-plugin 121 条 + Aria 139 条, state=all 翻页取全) 的标题与正文, 按 `collision_dedupe` / `_FIXED_NOW` / `LAYER_H_ACTIVE_WINDOW` / 半冻结 / 按日历 / 时间旅行 / 墙钟 等关键词本地检索: 没有与本单重复的 issue, 也没有跟进单。`10CG/aria-plugin#170` 与 `10CG/Aria#193` (均已 closed) 的正文或评论只是提到了同一个 30 天常量, 缺陷不同。本单正文自列的三条相关单写作裸编号 187 / 160 / 182, 核对为 `10CG/aria-plugin#187` (仍 open: run_all_tests.sh 对裸函数套件收 0 个测试报 OK)、`10CG/aria-plugin#160` (仍 open: 同名 lib 包绑定) 与 `10CG/Aria#182` (仍 open: handoff frontmatter status 从不收口; 注意它不是 `10CG/aria-plugin#182`, 后者是 issue_scan 分页, 已 closed), 均与本单不重复。

### Reproduction

**Mode**: `auto` | **Hit rate**: `3/8`

全部在 `/tmp` 实验目录复跑: 修前 v1.73.0、发版 v1.73.1、现行 HEAD、本机已安装的 plugin 缓存 1.73.3 与 1.74.1 各一份副本, 独立 HOME, 无 remote, 真仓零写入。用到冻结时钟的用例, 冻结器先在修前树上复现了 issue 的引信表才被采信 (见 case-2)。`match: true` 表示 issue 描述的缺陷在该配置下复现, `false` 表示不复现。

- case-1 (修前 v1.73.0, 真实时钟 2026-09-30, 单文件) 复现: `Ran 21 tests`, `FAILED (failures=7)`, rc=1; 7 条红与 issue 引信表点名的集合逐条一致。
- case-2 (修前 v1.73.0, 逐日期冻结时钟) 复现, 且与引信表逐行吻合: 09-08 为 0 红 / 09-09 为 2 红 (恰为点名的两条) / 09-14 为 3 / 09-18 为 5 / 09-19 为 6 / 09-22 起稳定 7 (含 2027-09-30 与 2040-01-01)。
- case-3 (修前 v1.73.0, issue 原命令 `bash skills/run_all_tests.sh`, 基础布局: 同级 `aria-plugin-benchmarks` fixtures + 全新 git 仓) 复现: `10 OK / 1 FAIL / 0 SKIP` (累计 2142 条), `FAIL: state-scanner (1591 tests)`, exit 1, 失败集恰为那 7 条。累计数比 issue 正文的 2146 少 4: state-scanner 两边都是 1591 条, 差额落在其余 10 个套件内, 未逐套件追查, 不影响结论。
- case-4 (修后: v1.73.1 / HEAD / 已安装缓存 1.73.3 / 已安装缓存 1.74.1, 真实时钟, 单文件) 不复现: 四份均 `Ran 23 tests ... OK` (21 条原有 + 2 条回归锁)。两份缓存副本的测试文件与对应 tag 逐字节相同 (sha256 前缀 `da5606ec` 对 v1.73.3, `e6830b98` 对 v1.74.1)。
- case-5 (修后四份 x 11 个日期: 2025-01-01 / 2026-09-08 / 09-09 / 09-14 / 09-22 / 09-23 / 真实今日 / 2026-12-29 即 +90 天 / 2027-09-30 即 +1 年 / 2030-01-01 / 2040-01-01) 不复现: 44 个组合全部 23/23 绿, 满足 issue 验收的「时间旅行态」。
- case-6 (修后 HEAD, `bash skills/run_all_tests.sh`, 基础布局, 真实时钟) 不复现: `11 OK / 0 FAIL / 0 SKIP` (2201 条), exit 0, state-scanner 1650 条 OK。注意汇总行的 SKIP 只统计套件级跳过; 基础布局不含主仓语料, state-scanner 里有 13 条依赖主仓语料的用例是用例级 skipped (10 条 real-tree dogfood, 3 条主仓布局 / 跨仓检查), 这 13 条当时没有被验证。复核时改用完整布局 (在基础布局上补齐主仓 CLAUDE.md / docs / openspec / standards / `.aria` 语料) 后 0 skipped, 真实时钟、+90 天、+1 年三种时钟下均 11 OK / 0 FAIL / 0 SKIP (2201 条)。
- case-7 (本机已安装的缓存 1.74.1, 作为采用方副本的代理, 同上命令) 不复现: `11 OK / 0 FAIL / 0 SKIP`, exit 0; 1.73.3 缓存副本的该测试文件在 11 个日期均 23/23 绿。
- case-8 (类级: 评论 23108 点名的 `test_max_branches_resolver.py` 4 处与 `test_p1_layer_h.py` 3 处同样不钉 `now=`, 以及整套 harness 平移到 +90 天 / +1 年) 不复现: 这两个文件 (39 / 24 条) 在 9 个日期 (含 2040) 全绿; 整套 harness 在 +90 天与 +1 年均 `11 OK / 0 FAIL`; 同一台时间机器在修前树 +90 天上恰好复现那 7 条红 (基线自检)。

说明两点:

1. 整套 harness 最初在没有 `.git`、缺同级 `aria-plugin-benchmarks` fixtures、且设了环境变量 `ARIA_COORDINATION_NO_PUSH` 的隔离副本里跑时, `aria-token-telemetry` (8 条)、`test_normalize_snapshot` (2 条)、`test_heartbeat_only_cli` (1 条) 会红, 修前树与 HEAD 上集合完全相同; 补齐目录布局 (同级 fixtures + 全新 git 仓) 并去掉那个环境变量后全部消失。其中 `aria-token-telemetry` 与 `test_normalize_snapshot` 是隔离布局缺 fixtures / `.git` 造成的实验环境产物; `test_heartbeat_only_cli` 那 1 条 (`TestHeartbeatPush.test_refresh_without_no_push_publishes_to_remote`) 是测试自己没有屏蔽环境变量 `ARIA_COORDINATION_NO_PUSH`, 设了就红、不设就绿, 属测试自身的环境隔离缺口 (见文末相邻项第 3 条)。三者都与本单无关。
2. 只冻 `datetime`、不同步移动 `time.time()` 时, `test_sync_mocked.TestFetchHeadAgeBuckets` 的 3 条会假红 (测试用真实 `time.time()` 设置 mtime, 被测函数用被冻结的 `scan_now()`); 两者同步平移后消失, 所以它们是冻结器的半冻结假红, 不是日历腐烂。

以上结论另经独立复核 (复核方各自重写了时钟平移工具与变异脚本, 不复用上面的冻结器), 结果逐项一致: 修前树的引信表逐行复现; 修后树在 2025 到 2099 年之间的多个时间点 (每次复核 10 个以上) 均 23/23 绿; 整套 harness 在完整布局里, 修前树真实时钟 10 OK / 1 FAIL (2142 条, 失败集恰为那 7 条), HEAD 在真实时钟 / +90 天 / +1 年均 11 OK / 0 FAIL / 0 SKIP (2201 条)。

### Verdict Rationale

本单缺陷 (测试只给 renderer 钉了时钟, collector 的 16 个调用点不钉, 夹具对着 30 天活跃窗口按日历腐烂) 由 `f314785` 修复 (补钉 16 处 + 2 条回归锁, 生产码零改动), 随 v1.73.1 发布, 其后 4 个版本 (v1.73.2 / v1.73.3 / v1.74.0 / v1.74.1) 均含修复, 两仓两端 master 一致。修前树今天仍是 7/21 红且与引信表逐条吻合, 修后各份副本 (含本机已安装的缓存副本) 在多个日期上 0 红, 整套 harness 在真实时钟与 +90 天 / +1 年下 11 OK / 0 FAIL, 满足 issue 自己写的三态负控验收。

两条回归锁经变异负控证实会红: 退回 1 处、钉成 `now=None`、追加第 17 个未钉调用点、用别名绕过扫描, 都让锁 1 红 (别名绕过由「扫到 <16 个即红」的自守卫拦下); 把 `_FIXED_NOW` 单独后移 60 天则让锁 2 红 (同时那 7 条护栏一起红)。另经独立复核, 直接回应正文「这为什么是缺陷」那段: 在 HEAD 副本上对生产码做三种破坏 (dedupe 跨容器折叠 / `cross_owner` 永不触发 / 活跃窗口全部丢弃, 每种先断言确实写进了文件), 正文所说已失效的那几条 negative control 在真实时钟与 2040 年下都转红 (分别 10 / 4 / 8 条)。也就是说, 护栏已恢复拒绝能力, 不再按日历恒红。

严重度取 `major`: 纯测试基础设施缺陷 (生产码零影响), 但它让整套 harness 按日历确定性变红, 并使变红用例里自称 negative control 的护栏失去区分力 (正文统计: 当时 6 条红里有 5 条), 不是偶发; 若只按用户影响判, 取 `minor` 也说得通, 对处置 (close) 没有影响。

### 未随本单处理的相邻项 (均未被 issue 跟踪, 是否开单已提请 owner 决定)

1. 裸读时钟一类。
   - 评论 23170「相邻观察」点名的 7 处 (`skills/state-scanner/lib/collision.py:232`、`lib/claim_lifecycle.py:76`、`lib/gc.py:94`、`lib/identity.py:102`、`lib/reconcile.py:194` 与 `:367`、`scripts/lib/spec_complete.py:1500`; 原文以「等」收尾, 并非穷举) 在 HEAD 上逐行仍在, 与 `scripts/collectors/_common.py:574` 的 `scan_now()` docstring 所写的 MUST 不符。
   - 同形的裸读取另有 (本次只扫了 state-scanner 的 `lib/` 与 `scripts/` 非测试代码): `scripts/renderers/track_board.py:623`、`scripts/writers/latest_md_writer.py:344`、`scripts/coordination_probe.py:140` 与 `:150`、`scripts/release_gate.py:108`、`scripts/phase1_gate.py:482` / `:1151` / `:1233`、`lib/coordination_ref.py:309`, 以及 `time.time()` 形态的 `scripts/collectors/handoff.py:407` 与 `scripts/collectors/handoff_worktrees.py:250`。
   - 这些是否都属于 MUST 所说的新鲜度 / 年龄 / 排序计算, 需要逐处判 (例如 `scripts/collectors/handoff.py:36` 的 docstring 自述 `age_hours` 有意用 `time.time()`, `lib/coordination_ref.py:309` 只取 `%Y-%m-%d` 日期串)。承接时应按类普查, 不要按评论 23170 的那 7 处立项。
   - 承接现状: 两仓 issue 的标题与正文检索 `scan_now` 零命中; 评论里只有 `10CG/Aria#218` 的评论 27376 (2026-09-30) 顺带点名了 `handoff.py:407` 与 `handoff_worktrees.py:250` 两处没走 `scan_now()`, 该评论建议改年龄口径时一起收。10CG/Aria 仓的 `docs/handoff/2026-09-10-session-close-five-gaps-closed-and-my-own-checker-lied-three-times.md` 第 60 行留有线程 `scan-now-must-violation`, 第 133 行把「开成 issue」列为待办, 至今未兑现。
2. `skills/state-scanner/tests/test_collision.py` 的 28 条测试, 官方 runner 从不收集。
   - 事实: 该文件是 28 个模块级裸函数 (pytest 风格, 不含 TestCase); `run_tests.py collision` 为 `Ran 0 tests` 且 OK, `run_all_tests.sh` 把 state-scanner 判为 unittest 套件, 汇总的 1650 条里不含它; 单独 `pytest test_collision.py` 为 28 passed。`skills/state-scanner/tests/` 下 78 个测试文件里只有这一个是这种形态。
   - 与已有单的关系: 机制与 `10CG/aria-plugin#187` (仍 open) 相同, 但那张单写的是整个套件收 0 个测试却报 OK, 这里是 unittest 套件里的单个文件, 汇总行看不出来。目前没有 issue 跟踪这种文件级形态: 两仓 issue 与评论里提到该文件的单 (`10CG/aria-plugin#134` 已 closed, `10CG/aria-plugin#160` 仍 open, `10CG/aria-plugin#170` 已 closed) 讲的是 import 顺序与同名 lib 包绑定, 没有一条讲官方 runner 不收集它。与本单验收无关。
3. `test_heartbeat_only_cli` 的环境隔离缺口: `TestHeartbeatPush.test_refresh_without_no_push_publishes_to_remote` 在设了 `ARIA_COORDINATION_NO_PUSH` 时红、不设时绿 (在完整布局里单独跑该模块: 不设为 7 条 OK, 设了为 1 条失败), 测试没有屏蔽该环境变量。与本单无关, 也无 issue 跟踪。

以上三项均未开单。开新 issue 不在 owner 2026-09-30 决策单第 4 项的授权类内 (feature 分支推送 / 开 PR / issue 评论 / issue 关闭), 已提请 owner 决定是否开单, 本评论不代为操作。

### 关闭建议

建议关闭。理由:

1. 本单的全部诉求均已满足并在两端 master 上: 16 处补钉 `now=` (零生产改动)、三态负控验收 (基线态 / 修复态 / 时间旅行态, 含 +90 天与 +1 年)、两条回归锁、评论 23170 写明的「发版后再关本单」前置条件 (v1.73.1 已于 2026-09-12 发布)。
2. 采用方侧的依据是 owner 2026-09-12 决策单 (10CG/Aria 主仓的 `.aria/decisions/2026-09-12-v1731-number-awarded-to-issue-194.md`) 的「后果」段: 发 v1.73.1 即修到采用方, 「修复未发版, 已发布 v1.73.0 与采用方副本仍红」这条 carry-forward 可闭合。10CG/Aria 仓的 handoff (`docs/handoff/latest.md`, 核验时第 29 行) 曾把本单记为「仍 open 待采用方侧确认」, 那只是 handoff 里的过渡表述, 不是关闭条件。v1.73.1 发版之后至今 18 天, 本单没有新评论, 时间线上最后一条是发版当日的 commit 引用, 也没有采用方回报复现。作为代理, 维护者本机 (不是外部采用方) 已安装的 1.74.1 缓存副本整套 harness 实测全绿, 1.73.3 缓存副本该测试文件 23/23 绿。
3. 重开条件: 在采用方副本上仍复现。判别方法: 本缺陷的特征是 `test_handoff_multibranch_collision_dedupe` 内那 7 条随日期变红; 汇总行出现 `FAIL: state-scanner` 但失败的不是这几条, 属别的原因 (例如运行目录缺同级 fixtures, 见 Reproduction 的说明), 不属本单。仍停留在 v1.73.0 及更早的副本需先升级到 v1.73.1 或更新版本, 升级即修复, 无需额外改动。
4. 正文末尾那次 2026-09-08 transient `FAIL: state-scanner` 不在本单范围 (正文已写明证据不可恢复, 且本单缺陷在 2026-09-08 冻结态下实测全绿, 解释不了它); 本单关闭不代表它已得到解释。

核验全部在 `/tmp` 实验副本上进行, 核验过程没有对任何仓做写操作; 本评论发布后的关闭动作按 owner 2026-09-30 决策单第 4 项的一次性授权执行。
