---
checkpoint: post_planning
mode: convergence
rounds: 8
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-29T10:07:56.572Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = e526fb126bc78071

- 派单 `/tmp/claude-1000/-home-dev-Aria/cbe6f623-7c3c-4217-8ccb-fd07680a5525/scratchpad/p199-r8/prompts/code-reviewer.md`,全文 112 行。
- `git diff 320d523 7ef09ea -- openspec/changes/pre-merge-completeness-gate-change-scope/`,两文件全部 hunk 都读了:tasks.md 166 行,yaml 529 行。长行用 difflib 做词级比对,逐段复算。
- 被审两文件 (`7ef09ea`):
  - tasks.md 读了头部、读前必看第 3–8、16、24 条、重写 a、判断清单第 6、11、19、24–28、38、40–64 条、等待点表,以及 1.1 / 3.5 / 4.3 / 4.4 / 5.1 / 5.3 / 5.5 / 5.7–5.9 行。
  - yaml 读了 `metadata` 的这些键:`baseline_rebase` 全部、`hard_constraints`、`owner_gates`、`rule6_note`、`sc12_liveness`、`a2_state_runs`、`stage_cells`、`c25_five_questions`、`coord_push_verify`、`commit_attribution`、revision_log 的 v2.7 十三条、`v2_state_runs`。
  - yaml 读了这些 TASK 的全文:TASK-001、005、008、018、019、022、023、024、025、027、029、030、031。
- proposal:`:162`、`:170`、`:251`、`:314`、`:467`。
- 两份决策单:
  - 2026-09-27 那份全文 82 行。
  - 2026-09-12 那份读了 §2 表、§3–§5 (`:55-116`)。
- R2–R6 聚合的 Minor 节,R7 聚合全文。
- 这轮的执笔报告全文 551 行、v2.7 派单全文。按流程在独立复算做完之后才读。
- CLAUDE.md 的多远程两条硬约束与规则 #3 / #6 / #8 / #10 (本会话已载入)。
- 源码 (aria `5215cf2`;下列文件在 `1cb3872..5215cf2` 区间实测零 diff):
  - `submodule_gate.sh:60-160, :263, :296-297`
  - `push_all_remotes.sh:18-26, :43-52, :100-122`
  - `lib/collision.py:365-422`
  - `lib/claim_lifecycle.py:316-320, :407-411`
  - `lib/failure_handlers.py:478, :544`
  - `phase1_gate.py:1455-1600`
  - `collectors/custom_checks.py:310-395`
  - `scripts/lib/spec_complete.py:715-750`
  - `sibling_spec_probe.py` 里 `elapsed_ms` 各处
  - `state-scanner/references/state-snapshot-schema.md` 的区间 diff
- 主仓配置与探针:`.aria/state-checks.yaml` (16 条全部)、`.aria/probes/plugin-cache-currency.py` 全文、`main-project-version-consistency.py` 的 POINTS、`issue_cache_freshness_probe.py` 的 SKIP 分支。
- 其他:
  - standards `2bc1c4c`:`git-commit.md:185-200`、`session-handoff.md` 节目录与 `940cb5b..2bc1c4c` 的 diff。
  - 10CG/Aria#195 归档:`tasks.md` 第 34–36 条、`detailed-tasks.yaml:777-866`。
  - 收尾 handoff `docs/handoff/2026-09-28-session-close-195-cycle-done-standards20-closed.md:36-54`。
  - 10CG/Aria#211 归档 proposal 的 T4 / SC-4 行。
  - 工具 README。
  - v2.6 执笔报告的「序号引用清单」位置。

### 实跑记录 (视角第 1–5 项)

所有改动性实跑都在 `…/scratchpad/audit-R8-code-reviewer/` 下的 `cp -a` 副本或临时仓里做。

**第 1 项,三态证据复跑。** 脚本全文从 `7ef09ea` yaml 的 `script` 字段取出,按 `command` 跑,输出与 `output` 做 `cmp`:

| 跑 | 环境 | 结果 |
|---|---|---|
| a2 | `state-base` 的 `cp -a` 副本 (主仓 `a563192` + aria `1cb3872`) | 退出 0,2396 字节,**逐字节一致**;副本已自复原 |
| v2,不带种子 | 同上 | 退出 0,**逐字节一致** |
| v2,带种子 | 种子为共享 `base/Aria` (只读 fetch) | 退出 0,**逐字节一致**;共享副本的 `refs/aria/coordination` 仍是 `8013d3b` |

- 另外对 v2.6 与 v2.7 的嵌入输出做了机器比对:a2 输出与脚本都不变;v2 输出除去 N13 块后与 v2.6 完全相同。
- `coord_ref_precheck`、`crlf_guard`、`new_checks`、`canonical_call`、`stage_cells` 不变。`commit_attribution.code` 只改了一行注释。
- 在自建副本里按工具 README 重跑生成器,得到 `REGEN_IDENTICAL`,产物与真仓文件也逐字节相同。

**第 2 项,引用精度抽查。** 共 29 处,aria 侧读 `5215cf2` (所列文件在 `1cb3872..5215cf2` 均零 diff),主仓侧读 `90a1351` / `7ef09ea`:

| 引用 | 实读 | 一致 |
|---|---|---|
| proposal `:162` | §1.1 末段:「S4 / missing / spec_level_undetermined 均降为 bypassed」 | 是 |
| proposal `:170` | S4-bypassed 字段取值 | 是 |
| proposal `:251` | §1.3 的逃生口,没有给字段取值 | 是 |
| proposal `:314` | 16 键里 `elapsed_ms` 列在最末,没有类型 | 是 |
| `lib/collision.py:416` / `:420` | `_TERMINAL = ("done", "abandoned", "unknown")`;`if not include_terminal and c.status in _TERMINAL: continue` | 是。路径是 `skills/state-scanner/lib/`,计划写的是简写 |
| `claim_lifecycle.py:318` / `:409` | `frozenset({"done", "yielded", "abandoned"})` | 是 |
| `push_all_remotes.sh:49` / `:107` / `:112` / `:119` | 分别是 `PRE_LOCAL_HEAD=…rev-parse HEAD`、push、读 `refs/remotes`、比较;全文 ls-remote 0 处;`BRANCH` 缺省 `master` | 是 |
| standards `git-commit.md:196` | `Spec: standards/openspec/changes/{feature}/spec.md` | 是 |
| aria `CHANGELOG.md:138` / `:234` / `:3170` | `[1.73.0]` / `[1.70.0]` / 完整性门条目 (与 `301641b:3020` 同文) | 是 |
| aria `VERSION:8` / `:9` | v1.73.0 minor 行、v1.71.1 patch 行 | 是 |
| aria `CHANGELOG` 小节数 | `5215cf2` 上 139 个,`1cb3872` 上 138 个 | 是 |
| 主仓 `CLAUDE.md:138` / `:142`、`VERSION:24` | 都是 1.74.0 | 是 |
| README `:8` / `:242`;三份 i18n README 各 `:3` / `:10` / `:244`;`system-architecture.md:189`;`version-scheme.md:23` | 16 处全是 1.74.0 | 是 |
| `spec_complete.py:733-744` | `_is_hooks_or_config_path` | 是 |
| `custom_checks.py:356-357` / `:377` | 取首个非空行;`lstrip().startswith("##SKIP##")` | 是 |
| `failure_handlers.py:544` | `write_claim(record, repo, …)` | 是 |
| `state-scanner/SKILL.md:182` / `:191`、`lib/constants.py:58` | 触发条件、fail-soft、`SWEEP_TTL = 86400` | 是 |
| `submodule_gate.sh:101` / `:263` / `:297` | `git log -1 --format=%B HEAD`、`GATE:`、`ALLOW: … overridden by per-PR marker` | 是 |
| `AB_TEST_OPERATIONS.md` 被引三处 | 计划只按节名引用,不写行号;场景 1 第 3 步 228→229、验收 219→220,文字逐字未变 | 是 |

**第 3 项,命令可执行性。**
- `head -8 | tr -d '\r' | grep -cxF …`:CRLF 下的正确取值,交互 shell 的 grep (包装函数) 得 1,`/usr/bin/grep` 得 0;先去 CR 后两者都是 1。子进程里的 `grep` 是 `/usr/bin/grep`,包装函数不导出。
- 六条 check 用运行器的 `_run_check` 在副本上跑:
  - 主仓根:前五条首行都以 `OK` 开头;`plugin-cache-currency` 首行 `STALE …`,退出 1。
  - 从 `aria/skills/audit-engine/tests` 起跑:`plugin-version-arch-docs-match` 打 `##SKIP##` 退出 0;占位符检查首行 `UNVERIFIED`,退出 1;其余四条退出 1 / 1 / 2 / 2。
  - 以上与 TASK-029 所记逐值一致。
- 16 条 check 里带 `##SKIP##` 哨兵的恰好 6 条,与计划一致。
- phase_d_sot 六个文件的 `git -C aria diff --shortstat 1cb3872 5215cf2 -- <文件>` 都退出 0 且输出为空。
- `sc12_liveness` 代码与守卫正则都能跑。

**第 4 项,git 序列 (v2.7 只动了 TASK-029 的并入)。** 在临时仓造了这样一个态:子模块工作树已前进到本轨合并提交、台账有未提交改动、`origin/master` 上他轨已 bump 子模块与 VERSION。

实测 `git merge-base --is-ancestor origin/master feature` 得 1,随后 `git merge origin/master` 退出 0。合并后:
- HEAD 的 gitlink 取他轨值,子模块工作树不动;
- 「只前进」断言退出 0;
- 未提交的台账保留;
- `fetch` 只更新远程跟踪 ref,不覆盖本地未推的 ref。

按 `commit_attribution` 的代码 (第二父是 base 的祖先),这个合并提交判 `sync-merge`。

**第 5 项,归档门预演。** 用 a2 脚本在 `7ef09ea` 副本上重放各态:
- C 态 (目标态) 仍是 `verdict=warn`,退出 0,warn 来源仍是 4.4 行 dogfood 那一条 `unverified_claim`;
- D / D2 / E 三个坏态 L2 为假,F 态 L3 为假;
- L1 与 status 在各态都不再有区分力,与 v2.7 的新前提说明一致;
- Step 7 仍受 `owner_gates` 第 11 项管,未变。

## Findings

### Major

**M1 · `69707662` · major · issue · documentation · scope `detailed-tasks.yaml TASK-025`**

**一句话**:v2.7 基线平移把 aria 的 `README.zh.md` 认定为「近几次发版都改它」的版本文件并写进 `aria_shifted`,但发版任务的文件集仍是五个。结果是 `README.zh.md` 头部版本行会停在旧号,计划里任何判据都拦不住。

**证据**:
- v2.7 新增 `detailed-tasks.yaml:80`:`'README.zh.md: 版本号 (v2.7 补入, 此前漏列: 近几次发版都改它; 1cb3872..5215cf2 +1 / -1, …)'`。
- 发版任务的文件集是五个,以下三处都是 v2.6 原文、v2.7 未碰:
  - `:2055-2060` TASK-025 的 deliverables 只有 plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md;
  - `:2066`「五文件改为新号 (逐处 grep -n 实测后改), 改后复验五处取值一致且都等于新号」;
  - `:2105` TASK-027「第 6 步 取号终核: 五文件取值等于台账记录的新号」;
  - `tasks.md:200` 5.3「改版本 SOT 5 文件」。
- 实跑确认版本面实为六个文件:
  - `git -C aria grep -l -F '1.74.0' 5215cf2` 恰好得六个:`.claude-plugin/marketplace.json`、`.claude-plugin/plugin.json`、`CHANGELOG.md`、`README.md`、`README.zh.md`、`VERSION`。
  - `git -C aria show 5215cf2:README.zh.md` 第 5 行是 `> **版本**: 1.74.0 | **发布日期**: 2026-09-28`。
  - `git -C aria log -- README.zh.md` 最近四条就是 v1.73.1 / v1.73.2 / v1.73.3 / v1.74.0 四次 `chore(release)`。
- 上一个发版周期已撞过同一件事,并有 owner 裁定。10CG/Aria#195 归档 `tasks.md:72` 第 34 条:「TASK-027 提交面由五个文件扩为六个 (…owner 2026-09-27 当场裁定) … 按五个文件提交会让中文 README 停在旧号, 现有 custom check 不读这一行、不会报出。owner 裁「带上, 六个文件一次提交」」。
- 该轨收尾 handoff (提交 `90a1351`,正是 v2.7 平移到的基线) 第 50 行:「CLAUDE.md §版本管理写「aria 子模块 5 文件」, 但 … 四次发版实际都改了 6 个文件 (多 `aria/README.zh.md`) … 计划与 CLAUDE.md 都按 5 写, 下次还会撞。建议 owner 定 …」。
- 本计划要跑的六条 custom check 都不读这一行:我逐条读了命令,它们读的是主仓根的四份 README、架构文档、VERSION、CLAUDE.md,以及 plugin.json 与插件缓存。
- v2.7 派单与执笔报告 D4 都只把它当作「TASK-001 多比一个文件」,没有连到 5.3。

**失败场景**:
- 执行者照 TASK-025 字面只改五个文件并提交;TASK-027 第 6 步「五文件等于新号」通过;TASK-029 六条 check 全按预期。
- 发版后,随插件分发的 aria `README.zh.md` 仍写「版本: 1.74.0」,没有任何机检报出。
- 另一种走向:执行者读到 `aria_shifted` 的新记录后起疑,但计划没有对应的等待点,只能像 10CG/Aria#195 那样计划外停下请裁。

**它怎么会红** (以 TASK-027 第 6 步作为判据):

| 态 | 第 6 步结果 |
|---|---|
| 基线 (未改号) | 红 |
| 目标 (六个文件都改号) | 绿 |
| 坏实现 (漏改 `README.zh.md`) | 仍绿 —— 对这一漏改结构上不会红 |

**建议修法** (二选一,都是小改):
- (a) 按 10CG/Aria#195 的 owner 先例把 aria 版本文件集写成六个:TASK-025 的 deliverables 与第 3 条、TASK-027 第 6 步、tasks.md 5.3 同改,并登记进判断清单。
- (b) 若 owner 要先定通用的发版面口径,就在 5.3 之前登记一个 owner 裁定点,附上 10CG/Aria#195 第 34 条与收尾 handoff 那一行,裁定之前不改号。

无论哪条,终核判据都要覆盖最终定下的文件集。

**定级理由**:属统一口径里的「漏掉文档同步面」。反方理由我也核了:CLAUDE.md 仍写「aria 子模块 5 文件」,通用口径还待 owner 定。但 owner 对同一文件最近一次的裁定是「带上」,v2.7 自己的新记录也已认定它随每次发版变动;计划既不改文件集也不登记待裁,照字面执行的结果就是静默漏改。

### Minor

**m1 · `5e83496e` · minor · issue · documentation · scope `tasks.md 3.5`**

**一句话**:v2.7 把 TASK-018 标题改成「文档机检 (SC-13、N1–N4 / N7 / N8 与四份 frontmatter) 与组 3 提交」(yaml `:1898`),但 `tasks.md:187` 的 3.5 行仍是「SC-13 全部条目与 N1 / N2 / N4 / N7 / N8」,两层在 N3 上不一致了。

**证据**:v2.6 时标题「SC-13 + N1 / N2」与 3.5 行都不含 N3,两层在这一点上是一致的。v2.7 只在标题补了 N3,这个接缝是本轮造成的。执笔报告「范围外观察」第 7 条已看到这一点但定为范围外;我不同意,因为 tasks.md 在本轮可写集内。

**失败场景**:不影响执行 —— TASK-018 第 2 条与 TASK-008 都要求 n3 为真。只影响按粗层核进度的读者。

**修法**:3.5 行补上 N3。

**m2 · `0c227bd6` · minor · issue · documentation · scope `detailed-tasks.yaml metadata.sc12_liveness`**

**一句话**:`blind_spots` 与 revision_log 记的是「90a1351 实跑脚本缺失态: status=alive, L1 真, L2 与 L3 假」,但没注明是「未勾选」那一态。a2 证据里脚本缺失有未勾选 (A) 与已勾选 (B) 两态,B 态下 L3 为真。

**证据**:在 `7ef09ea` 副本上跑 `sc12_liveness` 代码:
- 不加 `--force-checked`:`{"L1": true, "L2": false, "L3": false, "status": "alive", "alive_categories": ["code_reference", "generic_path_call"], …}`;
- 加 `--force-checked`:`"L3": true`,其余相同;
- 用 a2 脚本重放:A 态 `L3=False`,B 态 `L3=True`。

L3 与脚本在不在无关,只取决于 3.2 行有没有勾选。

**失败场景**:不影响执行,L2 / L3 的验收口径已实测不变。复核者若按 B 态去复现这条记录会得到 L3 真,可能误判记录失实。

**修法**:两处改写为「未勾选、脚本缺失态」,或把 B 态一并记上。

## 对账

### (i) R7 六簇

| 键 | 判定 | 亲验证据 |
|---|---|---|
| `6be9db6a` | closed | 16 条 check 中带 `##SKIP##` 的恰好 6 条 (按运行器解析器逐条核命令与被调探针);TASK-029 改成前缀比较;两个目录下的实跑首行与计划逐值一致;占位符检查按 `0ed4a31` 的三种首行描述,与源码一致 |
| `76949787` | closed | revision_log 的 v2.7 第 1 条勘正了 29325b2c;前 43 条与 v2.6 逐项相等 (机器比对为 True) |
| `6e4535a3` + `ab143d74` | closed | 两种 grep 实测:不去 CR 时 1 / 0,去 CR 后 1 / 1;`commit_attribution` 的 `\s*$` 接受 CR,口径一致 |
| `ce6f31fc` | closed | 独立扫描 yaml (不含 revision_log、代码块) 与 tasks.md 里的前置检查前提子句,共 13 处。凡属「写或推之前」的前提都带了对齐;不带的只有「不通过」分支和对齐动作本身。TASK-001 重新认领段先重解析,N13 的分叉态一对已复跑 |
| `bdce52c6` | closed | 第 47 条已改写,revision_log 在 v2.7 条目里补勘正了 6ad0a84b;v2.6 执笔报告 `:156` 确有「序号引用清单」,共 342 处 |
| `3de4b245` | closed | owner_gates 第 17 项、TASK-030、等待点第 17 行、第 58 条都写了代价。源码 `:152-158` 与 `:296-297` 显示:标签按固定名、对每个回退的子模块都放行 |

### (ii) B 组 21 行

每行都核了「落点确实改了、修法对题」,视角内的行做了实跑。

| 行 | 键 | 判定 | 核验 |
|---|---|---|---|
| B1 | R2 TASK-018 | closed | 标题已改;接缝见 m1 |
| B2 / B16 | cr/m1 · `d931db51` | closed | `CLAUDE.md:138` / `:142` 实读 |
| B3 | km | closed | POINTS 恰 9 点,与 16 点正交 |
| B4 | tl/m1 | closed | C.2.5 条只剩「以执行当时实测为准」 |
| B5 | cr/m4 | closed | 四个行号实读 |
| B6 | tl/m3 | closed | `version.yaml` 为 1.5.0 / 32 / 84,`a563192..90a1351` 零 diff;10CG/Aria#211 的 T4 已 deferred,记在 10CG/Aria#213 |
| B7 | cr/m5 | closed | TASK-022 第 1 条与第 4 条不冲突 |
| B8 | qa | closed | 分类器与守卫的谓词实测 (`.aria/<子目录>/config.json` 分叉);被跟踪的只有 4 个文件 |
| B9 | cr/m3 | closed | 带种子、不带种子两跑都逐字节一致 |
| B10 | `31b4c0f1` | closed | 四处落点都改了;`:196` 实读 |
| B11 / B17 | `a5996c58` · `0dd2d3f2` | closed | 在 `7ef09ea` 上重放 a2 属实;精度问题见 m2 |
| B12 | `af5e1e47` | closed | `--include-terminal` 只影响 `linked_issue_overlaps` 与计数 (`phase1_gate.py:1542-1556`) |
| B13 | `a2d80059` | closed | latest.md 行首 `track-id` 0 处,无 frontmatter |
| B14 | `a090f077` | closed | proposal 四个行号实读 |
| B15 | `9c0dcb27` | closed | N13 复跑一致,与 `measured` 散文逐项相符 |
| B18 | `ea958583` | closed | 第 61、62 条与 `rule6_note` 实值相符 |
| B19 | `34b92188` | closed | 与 sibling probe 的 `int((monotonic()-t0)*1000)` 同形;`SC-10.error-verdict-keyset` 在 TASK-008 格表里 |
| B20 | `27cee280` | closed | 临时仓实测并入可行 |
| B21 | `ae4753f5` | closed | 冻结点属实 (v2.4–v2.6 三个提交的 gitlink 都是 `1cb3872`);本轨交付物不触及那六个文件 |

## 对 10 条实质改动候选的逐条判断

| # | 判断 | 与未改动文本的接缝 |
|---|---|---|
| 1 `27cee280` | 改法正确 (临时仓实测) | TASK-023「以 TASK-030 合并时的冲突为准」:`version.yaml` 若冲突,现在会先在 TASK-029 出现,处置同为停下上报,执行者动作不变 |
| 2 `ae4753f5` | 改法正确 | 无;本轨交付物不含那六个 SOT,5.9 的比对不会被自己触发 |
| 3 `34b92188` | 改法正确 | 无;P1 同仓判定必起两个 git 子进程,1 ms 下界不会误红 |
| 4 `9c0dcb27` | 改法正确 (复跑一致) | 无 |
| 5 CR 两键 | 改法正确 (实测) | 无 |
| 6 `ce6f31fc` | 改法正确 | 无;扫描无遗漏 |
| 7 `3de4b245` + C1 | 改法正确 (对照闸源码) | 无;标签存在性见风险 1 |
| 8 `6be9db6a` + C3 | 改法正确 (实跑) | 无 |
| 9 C2 | 改法正确,与决策单第 3b 项第 2 个决定逐字相符 | 无 |
| 10 D 组 | **有问题** | 平移数字全部复现,但 `README.zh.md` 只进了基线记录、没进发版文件集,与未改动的 TASK-025 / 027 / 5.3 构成接缝,即 M1 |

## 对执笔人自报薄弱点的表态

1. 可接受。我对 FIX 与 OK 两类都做了抽查,没发现判错;但 M1 在这两份清单之外。
2. 可接受。补充一点:D3 的检索词是记录时点类词汇,「五文件」这种集合表述在 10CG/Aria#195 的裁定之后已经过时,却不在检索面里,M1 就是这样漏掉的。
3. 可接受。Ran 数在 B.1 / TASK-021 会重新记录,差值逐条归因。
4. 可接受。该条不在六条之列,且合 Rule #7。
5. 可接受。闸的逻辑已由源码佐证;另见风险 1 (标签存在性)。
6. 可接受。P1 必起子进程,sibling probe 也是同样的截断取整。
7. 可接受。停下是明示的;计划里已有同类无编号停点。
8. 可接受。与 hard_constraints 第 4 条的通则一致,有 N13 实证。
9. 可接受。这是 v2.5 的措辞,条目内已写明退出 1,不改变执行。
10. 可接受。我独立复算,新增的数目字全部复现。

## 对执笔请裁 11 条的表态

1. 无意见。owner 已为 v2.7 开 R8,按本轮结论处置即可。
2. 赞成执笔取舍。5.5 的命令自带断言;5.7 跑六条,保留前置能在第一步就停下。
3. 赞成执笔取舍。与 `commit_attribution` 口径一致,handoff 按模板以 LF 写出。
4. 赞成执笔取舍。避免 10CG/aria-plugin#202 那种双 claim。
5. 赞成执笔取舍。与 sibling probe 同形,三态可区分。
6. 赞成执笔取舍。重做内容记台账,外向动作仍逐项授权。
7. 赞成执笔取舍。但授权请求应一并写明「标签不存在时先建标签」(见风险 1)。
8. 赞成执笔取舍。该族文件现在为零,放宽会改动 N10 的证据。
9. 赞成执笔取舍。遵守头部「不写字面版本号」。
10. 赞成执笔取舍。
11. 赞成执笔取舍。

## 风险 / 疑问

以下不计入 finding。

1. **标签可能尚不存在**。只读 `forgejo GET /repos/10CG/Aria/labels` 得 `['aria-auto', 'bug', 'feature', 'post-m0', 'stale']`,没有 `submodule-rollback-approved`;组织级标签因令牌 scope 返回 403,读不到。若组织级也没有,「主控在授权下打标签」之前要先建标签,这是另一个外向动作。
2. **占位符检查命令里有 `exit`**。`0ed4a31` 之后命令含 `exit 0` / `exit 1`;TASK-027 第 7 步连跑多条检查时若把它内联进同一段 shell,会提前终止后续命令。宜经运行器或 `bash -c` 跑。
3. **「grep -r 不认 .gitignore」只对 GNU grep 成立**。交互 shell 的 grep 包装带 `--ignore-files`,会遵守 .gitignore。v2.7 C 组复述那两句「仍然成立」只对运行器 (`/bin/sh`) 成立。今天两者在真仓 aria 上计数一致:timestamp 模式都是 4,`<vNEXT>` 都是 0。
4. **`tracks_multibranch` 的产出方有改动**。`1cb3872..5215cf2` 改了它 (新增 `rel_path`、`unreadable_count`,git show 失败不再伪造行)。TASK-031 判定表用到的字段形状未变,而且是经 `/state-scanner` 取得,会自动跟进。
5. **hard_constraints 第 3 条的前提现在包含「对齐后重跑解析」**。解析到 0 条 active 这种情况,第 4 条与 TASK-001 已明确转到第 14 项;单读第 3 条有被误读转到第 15 项的可能,风险低。
6. **TASK-029 并入后没有显式断言**。没有写 `merge-base --is-ancestor origin/master HEAD` 这类结果断言;「只前进」断言与 TASK-030 的归属核验间接兜住了。
7. **共享副本的时间戳说明 (流程透明)**。
   - 我早期对两份共享副本各跑过只读的 `git status` 等命令。它们的 `.git` 目录 mtime 在 09:35:13,晚于派单标记,但三个 `.git/index` 的 mtime 在 09:30:13–14,早于标记,内容未被改写。
   - 共享 `base/Aria` 里 `.aria/probes/__pycache__/main-project-version-consistency.cpython-311.pyc` (09:47:14) 与 `.git/modules/{aria,standards}` (09:57:46) 的变化,按时间线判断不是本席造成的:我的实跑都在自己的副本里,自己副本里也没有这个 `__pycache__`。
   - 真仓只跑了只读命令 (含 `ls-remote` 与 `status`),HEAD 仍是 `7ef09ea`,工作区干净。

## Verdict

PASS_WITH_WARNINGS · counts `0C/1M/2m` · **Vote: REVISE**

## 是否足以开始 Phase B

按本轮口径不足以:还有 1 条 major (M1)。它只影响 5.3 / 5.5 的 aria 发版文件集,修法是小改 (五文件改为六文件,或登记 owner 裁定点);若 owner 选择先开 B.1、在 5.3 之前修掉,不会造成 Phase B 返工。