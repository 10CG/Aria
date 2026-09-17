---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T11:13:42.244Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer 席 (证据与命令的可执行性)

被审: `openspec/changes/pre-merge-completeness-gate-change-scope/{tasks.md, detailed-tasks.yaml}` @ 主仓 `97c3515`; aria `1cb3872`; standards `8b49562`。

## 已实读文件

- `tasks.md` 全文 (207 行); `detailed-tasks.yaml` 全文 (1056 行)
- 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文
- `proposal.md` (按行切片): `:3-19`、`:58`、`:103/:122/:130-149`、`:153-340` 中被引行、`:356-392` (§4 / §5 全部)、`:407-451`、`:462/:465/:467/:468/:469/:470/:471/:473`、`:480-486`
- aria @ `1cb3872`: `state-scanner/scripts/lib/spec_complete.py` (`:186-290`、`:320-592`、`:637-1128`、`:1129-1340`、`:1565-1790`)、`state-scanner/scripts/phase1_gate.py` (`:1125-1204`、`:1415-1560`)、`release_gate.py` (`:235-330`)、`lib/failure_handlers.py:95-107`、`lib/claim_lifecycle.py:475-` (docstring)、`state-scanner/SKILL.md:178-192`、`openspec-archive/SKILL.md` (`:101-300`、`:326-380`)、`phase-c-integrator/SKILL.md` (`:42/:57/:98-160/:600-640/:754`)、`audit-engine/SKILL.md` (`:1-12/:115-130/:378-435`)、`audit-engine/references/{execution-modes.md:1-95, report-storage.md:1-50, report-format.md:1-8, pre-write-validation.md:1-12}`、`phase-a-planner:246/:267`、`phase-b-developer:204/:214/:255/:277`、`task-planner:123`、`brainstorm:141`、`run_all_tests.sh:24-60`、`git-remote-helper/scripts/push_all_remotes.sh:95-125`、`config-loader/DEFAULTS.json:1-140`、`CHANGELOG.md`/`VERSION` 被引行
- 主仓: `.aria/config.json` (audit / state_scanner.coordination / phase_c_integrator 段)、`.aria/state-checks.yaml` (`:29-46`、`:124-151`、`:325-354` 与 name 清单)、`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:159-240`、`ab-suite/{audit-engine,phase-c-integrator,phase-c-integrator-pre-merge-gate}.json`、`ab-suite/version.yaml`、`ab-results/2026-08-16-v1.66.0-137-rule6/{RESULT.md, eval-3.../answer.md}` 开头、`openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md:1-8/:135/:146`、`standards/openspec/project.md:114-119`、`standards/openspec/templates/proposal-minimal.md:26-33`、`standards/conventions/content-integrity.md:189-215`、16 个版本点所在行
- `refs/aria/coordination` (`be2ba7e`, 与 `git ls-remote origin` 相同) 下 `claims/023236f2/` 全部 10 个条目的关键字段

### 附 1: 三态证据复跑 (逐字节比对)

- 做法: `cp -a` 执笔人副本到 `scratchpad/audit-R1-code-reviewer/Aria`; 用 PyYAML 从 yaml 取 `metadata.a2_state_runs.script` 与 `.output` 落为文件 (取出的脚本与 `p199/a2_state_runs.py` 也逐字节相同); 按 `command` 执行 `env -u ARIA_COORDINATION_NO_PUSH python3 -B a2_state_runs.py <副本根> <本目录 tasks.md> <本目录 detailed-tasks.yaml>`。
- 结果: rc=0, stderr 0 字节, `cmp run.out expected.out` → **BYTE-IDENTICAL** (两边都是 2396 字节)。跑完副本 `git status` 与 `git -C aria status` 均为空 (脚本复原生效)。
- 补充 (计划没有贴出的部分): 用脚本自身的函数复现 C 态, 直接执行 `metadata.sc12_liveness.code`: 全勾选时 `{"L1": true, "L2": true, "L3": true, "status": "alive", "alive_categories": ["aria_plugin_integration"], "gate_verdict": "warn", ...}`; 未勾选时 L3=false, 加 `--force-checked` 后变为 true —— 代码可直接运行。
- 归档门预演: C 态全量输出 `complete=True` (`tasks.md 全 [x] (31 task(s), 无 carry-forward/defer 注释)`), `verdict=warn`, `blocking_reasons=[]`, `warnings=[]`, `soft_errors=[]`, 唯一的 `unverified_claims` 是 4.4 行 (`dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在`), `d_payload` 非空 (deferred 0 / unverified 1)。这与计划声称的「warn, 来源是 4.4 dogfood」一致。按 `openspec-archive/SKILL.md:287-296`, Step 7 在 `d_payload != null` 时会自动建 tracker (headless 默认), 计划已把它登记为 owner_gates 第 11 项 —— **已登记**。

### 附 2: 引用精度抽查 (35 处)

| 序 | 引用 (出处) | 实读 | 一致 |
|---|---|---|---|
| 1 | tasks.md:18 proposal `:10`「在 `f314785` 起分支」 | `:10` 逐字含「Phase B 在 `f314785` 起分支」 | 是 |
| 2 | tasks.md:17 `:4` / `:18` 排在 10CG/Aria#195 之后 | 两行均含 | 是 |
| 3 | tasks.md:19 `:16`/`:366`/`:450` 的 v1.73.1 / v1.74.0 | 三行均含 | 是 |
| 4 | tasks.md:29 F7 注 `:58` | `:58` 为 F7 表行 (proposal 自己在 `:468` 写成 `:56`, 计划的 `:58` 才对) | 是 |
| 5 | tasks.md:25 `:122` 的 adaptive 例外清单漏列几格 | 清单 = SC-7(d)(e) / SC-9(4) / SC-15(6) / SC-20(1)-(7); SC-9(2) 第二跑写明 `mode:'adaptive'` (`:465`), SC-15(5) 写明 `mode:'convergence'` (`:471`), 均未列 | 是 |
| 6 | tasks.md:23 `:340` Step 2 改写句 | `:340` 含该句, 豁免集不含 no_spec_unverifiable | 是 |
| 7 | tasks.md:38 `:409-451` 共 17 个 checkbox | 实数 17 (`:409`、`:429-439`、`:447-451`) | 是 |
| 8 | tasks.md:31 SC-6 `:462` 自证句 | 一致 | 是 |
| 9 | tasks.md:32 SC-11 `:467`「`present` 或 `missing`」 | 一致 | 是 |
| 10 | tasks.md:29 `:468` liveness 子句已删 + 恢复条件 | 一致 | 是 |
| 11 | tasks.md:38 `spec_complete.py:273` | `boxes = _CHECKBOX_RE.findall(tasks_text)` (is_spec_complete 内) | 是 |
| 12 | yaml:72 `spec_complete.py :924 / :1642 / :1636` | `if name == "SKILL.md":` / `return result  # 两文件皆缺 …` / DEC 注释 | 是 |
| 13 | yaml:73 `multi_remote.py:107-113` | F1′/F4′ freshness 注释块 | 是 |
| 14 | yaml:75-76 CHANGELOG `:104`/`:200`/`:3136`、`301641b` 上 `:3020`、VERSION `:7`/`:8` | 全部一致; 四个 shifted 文件 `--shortstat` 合计 127+/7−, 与各条之和相符 | 是 |
| 15 | yaml:44-70 aria_zero_diff 27 个文件 | 逐个 `git diff --shortstat 301641b 1cb3872` 为空, 文件均存在 | 是 |
| 16 | tasks.md:35 / TASK-016 phase-c-integrator `:42`/`:57`/`:131`/`:132`/`:157`/`:754` | 均为所述内容 | 是 |
| 17 | tasks.md:33 `phase-b-developer/SKILL.md:214` | `AND audit.checkpoints.mid_post_spec != "off"` | 是 |
| 18 | TASK-017 `phase-a-planner:267`、`phase-b-developer:204,277` | 三处 `{timestamp}` 形态 | 是 |
| 19 | TASK-031 转引决策单四个调用方 `:246`/`:123`/`:255`/`:141` | 四处均为字面键早退 | 是 |
| 20 | TASK-014 execution-modes `:9`/`:10`/`:15`/`:25-30`/`:34`/`:43`/`:44`/`:66`/`:82` | 均一致 | 是 |
| 21 | TASK-015 SKILL.md `:381-384`/`:385-388`/`:427-433` | 一致 (`:427` 为 `## 相关文档`) | 是 |
| 22 | TASK-017 report-storage `:8`/`:37`/`:43`、report-format `:5`、pre-write-validation `:3` | 一致 | 是 |
| 23 | 重写 b `project.md:117`、`proposal-minimal.md:28-32` | 一致 (后者为 CRLF 文件) | 是 |
| 24 | TASK-003 `run_all_tests.sh:41-46` | `is_pytest_suite()` 全函数 | 是 |
| 25 | TASK-021 `test_pre_merge_gate.py:266` | `def test_case_e_malformed_aether_main_leg_routes_fail` | 是 |
| 26 | c25 `phase-c-integrator/SKILL.md:603`/`:612-623`/`:613`/`:614`/`:625-630`/`:638` | 一致 | 是 |
| 27 | c25 `push_all_remotes.sh:103-119` | push 在 `:107`, 判据在 `:119`, `:103` 为空行 | 基本一致 |
| 28 | c25「`.aria/config.json` 的 multi_remote 段」 | 该段不存在 | **否** (m5) |
| 29 | TASK-002「C 的大小 (A.2 时 153)」 | 实测 154 | **否** (m1) |
| 30 | TASK-029 16 个版本点 | README.md `:8`/`:242`; zh/ja/ko 各 `:3`/`:10`/`:244`; CLAUDE.md `:139`/`:141`; VERSION:24 (`v1.73.0`); system-architecture.md:189; version-scheme.md:23 —— 共 16 处 | 是 |
| 31 | 读前必看第 4 条 10CG/Aria#211 proposal `:135`/`:146` | T4 / SC-4 | 是 |
| 32 | 读前必看第 10 条「远端仓不存在」 | `git ls-remote ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin-benchmarks.git` → `Forgejo: Cannot find repository` | 是 |
| 33 | metadata.sc13_baseline 各计数 | 逐项 grep 一致 (2 / 0 / 3 / 八个 0 / 三个 0 / 3 / 0 / 1 / 0; `{timestamp}` 残留恰 4 处, 即 TASK-016/017 的四个修改点) | 是 |
| 34 | metadata.test_runner 基线 | 副本实跑: audit-engine `Ran 104 OK`; phase-c-integrator `Ran 148 OK`; state-scanner 不带变量 `Ran 1605 OK (skipped=1)`, 带 `=1` 时 `FAILED (failures=1, skipped=1)`, 失败用例就是 `test_refresh_without_no_push_publishes_to_remote`; catalog 三条命令 `Ran 9 OK`; 字面 NEG-1 node id `FAILED (errors=1)` | 是 |
| 35 | metadata.claim | `s-86f7@1836.yaml`: track / status / phase / heartbeat 均一致; 本地与 origin 的 `refs/aria/coordination` 都是 `be2ba7e` | 是 |

另外只读试跑并通过: TASK-015 的 awk frontmatter 断言 (`1cb3872` 与当前文件都是 `7116d9f0…`, 改 description 后为 `06187dc8…`); TASK-007 的 `run_all_tests.sh --list` (audit-engine 显示 `(unittest)`); `check_bare_issue_refs.py --repo-root=… tasks.md detailed-tasks.yaml` → `裸 issue 引用: 0`; §4.5 自查命令零命中, 两份文件也没有希腊字母; `phase1_gate.py` / `release_gate.py` / `check_bare_issue_refs.py` 的 CLI 参数与计划命令一致; 重写 b 的计数在 `a563192` 上复算为 154 / 54 / 17 / 37, 在 `97c3515` 上为 53 / 16, 与计划一致; yaml 的 agent 计数 (15/8/7/1)、工时合计 (97-143)、依赖都指向已有任务且无前向依赖, 31 个 parent 与 tasks.md 的 checkbox 逐一对应。

## Findings

### Critical

无。

### Major

**M1 · `3884ee1f` · major / issue / implementation · scope `detailed-tasks.yaml TASK-025/TASK-027`**
- **结论**: aria feature 分支从 B.1 到 5.5 合并前没有任何「并入 `origin/master`」的步骤。Phase B 期间只要 aria 发过一版, TASK-027 第 5 步就会在版本五文件上冲突; 而计划字面给出的恢复是「从第 1 步重走」, 重走会再次冲突, 不收敛。
- **证据**:
  - TASK-025 (yaml:918-920): 取号只做 fetch, 然后读 `plugin.json` 现值与远端 tag; 五个版本文件直接在 feature 分支上改, CHANGELOG 用 `grep -n '^## \['` 定位插入点。
  - TASK-027 第 4 步 (yaml:956): ec72175 先例 (把 origin/master 并入 feature) 只在「origin/master 相对取号时 SHA 已前进」时才触发。
  - 第 5 步 (yaml:957): 冲突 ⇒ abort 后停。owner_gates 第 6 项 (yaml:120): 「owner 确认后从第 1 步重走」。
  - 判断清单第 19 条 (tasks.md:73) 把合并冲突归入「罕见并发路径」。
  - 实测发版节奏: aria 在 09-12 至 09-13 两天内发了 v1.73.1 / v1.73.2 / v1.73.3 三版 (`44f00d1` / `5a973e7` / `1cb3872`)。本计划 Phase B 估时 97-143h (yaml:18)。
- **失败场景**: 在 TASK-001 与 TASK-025 之间, 任一容器发了 aria 新版。TASK-025 看了远端 tag, 号本身算得对, 但五个文件是在旧基线上改的。到 TASK-027: 第 3 步把 master 快进到新的 `origin/master` 得到 S3; 第 4 步 S3 等于取号时 SHA, 不触发恢复; 第 5 步在 `plugin.json` 的 version 行、VERSION 头部、CHANGELOG 顶部三处同位修改上冲突 → abort 并停 → 按字面「从第 1 步重走」→ 再次冲突。唯一写明的恢复动作挂在第 4 步, 这个场景下触发不到。
- **修法**:
  1. TASK-025 取号前加一步: `git -C aria merge origin/master` 进 feature 分支 (不 rebase), 冲突即停; 合并后重跑 TASK-021 的回归。
  2. 第 5 步冲突的恢复指针与第 4 步统一为 ec72175 先例。
  3. 判断清单第 19 条把「Phase B 期间 aria 已发版」从罕见路径中移出。

**M2 · `bf0ecef8` · major / issue / implementation · scope `detailed-tasks.yaml metadata.owner_gates#14 / TASK-001 / TASK-024`**
- **结论**: owner_gates 第 14 项的「未授权」分支自相矛盾。它要求本轨心跳也加 `--no-push`, 但 state-scanner 入口的自动心跳加不上; 而 TASK-024 的强制对齐又会把仅在本地的重认领静默抹掉。
- **证据**:
  - yaml:128: 未授权 ⇒ 加 `--no-push` 只写本地; 获授权前本轨心跳也加 `--no-push`; 「推送随下一次获授权的协调 ref 推送发生」。
  - `state-scanner/SKILL.md:182`: 「本会话持 active claim 且 `coordination.enabled == true` 的每次 `/state-scanner` 入口都调用一次」。`:187-189` 的命令行不带 `--no-push`。
  - 本仓 `.aria/config.json` 实读 `state_scanner.coordination.enabled = true`。
  - `phase1_gate.py:1176-1183`: 不带 no_push 时调用 `resilient_push`, 推的是整个协调 ref。
  - 会话内唯一能让入口心跳不推的办法是在启动时带 `ARIA_COORDINATION_NO_PUSH`, 但 TASK-001 / TASK-021 (yaml:447 / :837) 要求组 1–4 的会话不带该变量。
  - TASK-024 (yaml:899) 结束时按 `AB_TEST_OPERATIONS.md:228` 执行强制 fetch `+refs/aria/coordination:refs/aria/coordination`。计划只提到这会回退 `--no-push` 心跳。
- **失败场景**: 进 B.1 时本轨 claim 已被扫成 abandoned (SWEEP_TTL 为 24h; gate 1 要等 10CG/Aria#195 走完 C.2, 间隔很可能超过 24h), 且 owner 未授权推送, 于是本地重认领。之后两种走向:
  - (a) 任意后续会话的 `/state-scanner` 入口心跳把这条新 claim 推上 origin, 成为未授权的外向推送;
  - (b) 若一直没有触发入口心跳, TASK-024 的强制对齐会把这条仅本地的 claim 删掉。之后心跳返回 `outcome=error`, TASK-031 的 `release_gate` 找不到 active claim; 台账只记「对齐前后的值」, 不会判出 claim 丢失。
- **修法**: 二选一:
  1. 未授权分支改为「不重认领, 停在 B.1 等授权」(最简单);
  2. 或写明「该期间所有会话都以 `ARIA_COORDINATION_NO_PUSH=1` 启动, SC-12 的 state-scanner 命令另开会话跑」。

  另外, TASK-024 强制对齐前应先断言: 本地协调 ref 相对远端没有本轨的仅本地提交 (对 `claims/023236f2/` 做 `git log <远端 SHA>..refs/aria/coordination`), 有则停。

**M3 · `69707662` · major / issue / documentation · scope `detailed-tasks.yaml TASK-025`**
- **结论**: CHANGELOG 迁移文案的第 2 条会与裁定 11 矛盾。读前必看第 7 条的连带清单漏了 proposal §5 第 2 条。
- **证据**:
  - `proposal.md:378` (§5 第 2 条) 写「只把 missing / S4 / `spec_level_undetermined` 降为 `bypassed` …; S3 的输入矛盾错与 S1 的 `change_id_unanchored` 不被豁免」, 豁免集不含 `no_spec_unverifiable`。
  - TASK-025 (yaml:920) 只要求改写第 10 条。tasks.md:23 (第 7 条) 的连带清单列了「§5 第 10 条」, 没有列 §5 第 2 条。
  - 对照:
    - 决策单 `:90` (裁定 11): `allow_incomplete_checkpoints` 覆盖 `no_spec_unverifiable`;
    - TASK-015 (yaml:715) 的 SKILL.md 注释已包含 `no_spec_unverifiable`;
    - §4 表 `:360` 的 Step 2 串同样缺这一项, 但 TASK-014 指向的是第 7 条的逐字句, 不受影响。
- **失败场景**: 执行者按 TASK-025 照 §5 第 1–12 条写 CHANGELOG, 结果同一版说明里:
  - 第 2 条说「只把 missing / S4 / spec_level_undetermined 降级」;
  - 第 10 条说 `no_spec_unverifiable` 可以被豁免。

  两条自相矛盾, 且与 execution-modes.md 的 Step 2、SKILL.md 注释不一致。SC-13 / N1 / N2 都不检查 CHANGELOG, 会恒绿放行。
- **修法**: 读前必看第 7 条的清单补上「§5 第 2 条 (`:378`)」; TASK-025 写明第 2 条的豁免集同步加上 `no_spec_unverifiable`。

**M4 · `4f60db5b` · major / issue / implementation · scope `detailed-tasks.yaml TASK-016/TASK-017/TASK-018`**
- **结论**: 两份要改的 SKILL.md 是 CRLF 行尾, 计划没有任何行尾保护或机检, 验收会放过整文件行尾改写。
- **证据**:
  - `git -C aria ls-files --eol` → `i/crlf w/crlf skills/phase-b-developer/SKILL.md`、`i/crlf w/crlf skills/phase-c-integrator/SKILL.md`。两份文件分别是 1070/1070 行、1096/1096 行 CRLF。aria 没有 `.gitattributes`, `core.autocrlf=false`。
  - TASK-016 / 017 要编辑这两份文件, 但计划全文 grep `CRLF|行尾` 零命中。
  - TASK-018 只核 grep 计数与 porcelain 为空。
  - TASK-015 的 frontmatter 不变断言只作用于 LF 文件 `audit-engine/SKILL.md`。同一条 awk 对 CRLF 文件输出为空 (实跑 `awk '…' phase-c-integrator/SKILL.md | wc -l` = `0`), 所以若照搬到 CRLF 文件, 两侧都是空串, sha 相等, 恒绿。
- **失败场景**: subagent 用 Python `read_text`/`write_text`, 或按 LF 插入新行 → 结果是整文件 1096 / 1070 行的 diff 或混合行尾, description 的字节也随之改变。SC-13 grep 与 porcelain 断言全绿, 照样放行。这还会放大 M1: TASK-027 第 5 步遇到任何并发改动这两份文件的提交, 都会变成整文件冲突。本仓 memory `preserve-crlf` 记过同类前科。
- **修法**:
  1. TASK-016 / 017 编辑前后各跑一次 `git ls-files --eol`, 要求仍为 `i/crlf w/crlf`, 且 `git diff --numstat` 的删除行数只等于被替换的行数。
  2. TASK-018 把这两条纳入机检。
  3. 若要断言这两份文件的 description 不变, 切 frontmatter 前先 `tr -d '\r'`。

**M5 · `ed0d0fd8` · major / issue / testing · scope `detailed-tasks.yaml TASK-014/TASK-015/TASK-018`**
- **结论**: SC-13「两侧调用串逐字相等」没有钉死怎么抽取调用串、要不要做归一化, 计划也没有给代码和三态实跑。
- **证据**:
  - TASK-015 (yaml:714) 与 TASK-018 (yaml:771) 只写了「逐字相等 (含续行与参数序)」。`metadata.new_checks` 只有 N1–N3, `a2_state_runs` 也没有跑这一条。
  - execution-modes.md 实读: Step 1–5 同在 `:34` 开、`:66` 闭的一个围栏内; `Step 4:` 行缩进 2 空格, 内容缩进 4–6 空格 (`:54-61`)。
  - SKILL.md 的先例调用串在 ```` ```bash ```` 块内顶格 (`:123-125`)。
- **失败场景**:
  - TASK-014 按该节既有缩进写调用串 (行首多 4–6 空格)。TASK-018 若不剥缩进, 会对正确实现判红, 流程卡住; 若剥缩进, 那是执行者的临场决定, 换一个执行者可能判相反。
  - 反过来, 如果为了过检查把调用串顶格塞进缩进块, 就成了「为迁就检查器改内容」。
  - 「调用串」的起止 (`\` 续行算到哪一行) 同样没有定义。
- **它怎么会红**:
  - 基线 (两侧都没有调用串): 「恰 1」计数先红, 相等性无定义;
  - 目标实现: 红绿取决于未钉死的缩进约定;
  - 坏实现 (参数换序): 只有在抽取规则钉死后才会稳定判红。
- **修法**: 在 `metadata.new_checks` 增加 N4:
  1. 在各自切片内, 从含 `scripts/completeness_gate.py` 的行起, 连续取以 `\` 结尾的行, 到第一条不以 `\` 结尾的行为止;
  2. 逐行 `strip()` 后比较两个列表;
  3. 在副本上跑三态 (基线 / 目标 / 参数换序) 并贴出输出。

### Minor

- **m1 · `df035824` · minor / issue / documentation · `detailed-tasks.yaml TASK-002`**
  - yaml:465 写「C 的大小 (A.2 时 153)」。
  - 实测: 在 `a563192` 与 `97c3515` 上, `openspec/changes/*` 加上去掉日期前缀的 `openspec/archive/*`, 目录名集合都是 **154** (树与工作区两种口径一致; 去掉本 spec 自身才是 153)。
  - 计划重写 b 自己也写了「有 `proposal.md` 的 change 154 个」, C 不可能比它小。
  - 执行者照字面比对会误以为语料变了。修法: 改为 154, 或写明计数口径。
- **m2 · `c8cab993` · minor / issue / implementation · `detailed-tasks.yaml TASK-019`**
  - 三步法 (yaml:788) 在「只回退该组件后再跑, 红」之后直接 `git -C aria worktree remove`, 此时 worktree 仍带补丁。
  - scratch 实测: `fatal: '../cf-x' contains modified or untracked files, use --force to delete it`, rc=128。
  - 修法: 先记下 diff, 再 `git -C <wt> checkout -- .` 后 remove; 或明写 `--force`。
- **m3 · `3c67b96e` · minor / issue / testing · `detailed-tasks.yaml TASK-024 前置核验`**
  - yaml:892 用 `[ -n "${ARIA_COORDINATION_NO_PUSH+x}" ]` 判断「会话带了变量」, 这只看变量是否已设置。
  - CLI 的判据是取值属于 `1`/`true`/`yes` (`lib/failure_handlers.py:95-107`: 「Anything else (`0`, `false`, `no`, empty, ...) … is OFF」)。
  - 三态: 未设置 → 假 (正确); `=1` → 真 (正确); `=0` → 真 (错误, 此时推送并未被抑制)。
  - 后果: 这种情况只能靠事后的 transcript `push_skipped` 核对发现。
  - 修法: 改用与 CLI 同一判据, 例如 `python3 -c` 调用 `no_push_requested_by_env()`。TASK-001 / 021 方向相反, 用 `+x` 反而更严, 可以保留。
- **m4 · `403abab2` · minor / issue / testing · `detailed-tasks.yaml TASK-024 副作用快照`**
  - yaml:893 规定: 两个远端 master 的 `ls-remote` 一有变化就停下上报。
  - 本轮审计期间实测: 两端 master 已是 `e4874d4`, 本地 `origin/master` 仍是 `8a9fe35`, 本地甚至没有 `e4874d4` 这个对象 —— 远端并发推进是常态。
  - 后果: 5–8h 的 AB 期间, 别人的推送会造成假停。
  - 修法: 远端有变化时, 先核新提交是否含本会话产物, 而不是一律停。
- **m5 · `f0e0d6b8` · minor / issue / documentation · `detailed-tasks.yaml metadata.c25_five_questions`**
  - yaml:428 引用「`.aria/config.json` 的 multi_remote 段」。实读本仓 config: 顶层没有 `multi_remote`, `phase_c_integrator` 下也没有 `multi_remote_push` (只有 `_comment` / `_lane` / `_not_ci_backends_empty` / `pre_merge_gate`)。
  - 结论 (`fail_on_partial_push` 为 true、`read_only_remotes` 为空) 只来自 `config-loader/DEFAULTS.json:7-14`, 本身成立。
  - 后果: TASK-030 按这条「逐条核事实」时会找不到该段。修法: 改引 DEFAULTS.json。
- **m6 · `0d4431bd` · minor / issue / implementation · `detailed-tasks.yaml TASK-027/TASK-029`**
  - 本仓已启用检查 `no-unresolved-version-placeholder` (`.aria/state-checks.yaml:29-44`), 专查 aria 交付面残留的 `<vNEXT>`, 起因正是 v1.73.0 发布时的残留。
  - 本计划大量使用 `<vNEXT>` 占位, 但 TASK-027 第 7 步 (打 tag 前) 与 TASK-029 的 custom checks 清单都没有列这条。
  - 修法: 在第 7 步加跑该检查的 `command`。
- **m7 · `4803c0ca` · minor / issue / documentation · `tasks.md 读前必看第 19 条 / TASK-015`**
  - 第 19 条只把 `phase-c-integrator:57` / `:754` 算作同形位置。
  - 同一个 hotfix lane 条件在 `audit-engine/SKILL.md:423` 还有一处: 「仅 `audit.enabled=true` 且 pre_merge checkpoint != off 时降级」。TASK-015 没有覆盖它。
  - 这句按优先级链也能读通, 影响低。建议 TASK-015 顺带改成与 `:754` 新写法同一句, 避免两处描述分叉。
- **m8 · `749f8d15` · minor / issue / implementation · `detailed-tasks.yaml TASK-030`**
  - yaml:1026 要求「`merge --ff-only origin/master` 后, 断言 HEAD 等于 Forgejo 回执里的合并提交」。
  - 合并与 fetch 之间若有他人推送 (m4 已实测到这种并发), HEAD 会超前于合并提交, 导致判停。
  - 修法: 改为断言「合并提交是 HEAD 的祖先, 且其第二父等于 feature 分支 HEAD」, 这样也钉住了本次新产生的对象。
- **m9 · `cf10b012` · minor / issue / implementation · `detailed-tasks.yaml TASK-001`**
  - 心跳命令带了 `--phase B`, 但 `heartbeat_by_track` 只写 `heartbeat_at` (`lib/claim_lifecycle.py:475` 起的 docstring: 「`heartbeat_at` is the only field written」)。
  - 结果: claim 的 phase 在 B–D 全程仍是 `A.2` (当前 `s-86f7@1836.yaml` 就是 `phase: A.2`)。
  - 建议在台账注明 track board 会一直显示 A.2, 免得把 `--phase B` 误读成「已切到 B」。
- **m10 · `43d9539f` · minor / issue / implementation · `detailed-tasks.yaml metadata.owner_gates#2`**
  - owner_gates 第 2 项 (推送主仓规划提交) 没有写执行步骤。
  - 此刻的实测状态: 本地 master `97c3515` 基于 `8a9fe35`, 两端 master 已是 `e4874d4` ⇒ 直接推送会被拒。
  - 建议写明: fetch → 判断本地 master 与 `origin/master` 的关系 → merge (不 rebase) → 双推 → 逐 remote `ls-remote`。
- **m11 · `4d6e2a29` · minor / issue / documentation · `detailed-tasks.yaml metadata.title`**
  - yaml:1 的头注释与 yaml:6 的 `title` 仍写「v1」。
  - tasks.md:6 写的是 v1.1, 而 v1.1 改的正是本文件的 owner_gates 与 hard_constraints。
  - 只是标签不一致, 不影响执行。

## 对执笔人自报薄弱点的表态

- **(a) 读前必看第 7、8 条的取值由执笔人钉定 —— 可接受。**
  - 我逐项核过: 第 7、8 条与 TASK-006 的 SC-17(5)(c)、TASK-011 的取值一致。
  - `checked_checkpoints` 的 explicit-only 规则与 SC-9(2) 先例同形。
  - 取值钉死后测试才可判定, 且已列入判断清单第 8 条请 owner 复议。
  - 缺口不在这两条本身, 在于连带面漏了 §5 第 2 条 (M3)。
- **(b) 组 5 发布前提偏重 —— 部分可接受。**
  - 5.8 要求三个子模块与两端完全一致: 不满足只会停下, 不会误推他轨内容, 可接受。
  - 5.2 结束后强制对齐回退心跳: 单独看可接受, 下个会话的入口心跳会补上。
  - 不可接受的是这一点与 owner_gates 第 14 项未授权分支叠加时, 会静默抹掉仅本地的重认领 (M2)。
- **(c) N1/N2 仍是文本谓词; SC-11 收紧为 `present`; SC-6 快照放活体 —— 可接受。**
  - N1/N2/N3: 三态逐字节复跑一致, 且 `new_checks.code` 与脚本内同名函数对两份输入的判定相同。
  - SC-11 收紧为 `present`: 合理。本 spec 已有 4 份 post_planning R1 报告落盘, 文件名命中规则 2。
  - SC-6 快照放到活体运行: 合理。
  - 但同属文本谓词的 SC-13「两侧逐字相等」既没有代码也没有三态 (M5)。

## 风险 / 疑问 (不计入 finding)

1. **AB 在真仓、无沙箱运行**:
   - `phase-c-integrator.json` 的 eval 3 题面是「请执行 Multi-Remote Push Enforcement: 主动推送所有 enforced remote」, eval 1 是「Execute Phase C C.1: Generate conventional commits」。
   - `ARIA_COORDINATION_NO_PUSH` 只抑制协调 ref 的推送, 计划对其他推送只做事后快照。
   - 先例 `2026-08-16-v1.66.0-137-rule6` 的产出是描述性的 (`REPO=/path/to/aria`), 所以这里只记风险。
   - 更强的做法是 AB 会话前把 remote 的 pushurl 指向不可达地址; 这是配置改动, 须 owner 同意。
2. **L2 另有一处盲区**:
   - `_is_hooks_or_config_path` 会把任一 `*/.aria/config.json` 或 `hooks.json` 中出现的符号名 (包括 `_comment` 里的) 判为 `aria_plugin_integration` (`spec_complete.py:733-744`, `:955-958`)。
   - 当前仓内这类文件共 3 个, `git grep` 均不含 `completeness_gate`, 本计划也不改 config, 所以只是理论风险。`sc12_liveness.blind_spots` 没有列这一项。
3. **TASK-023 的计数可能在合并后过期**: 两个计数是在 feature 分支上重生成的。若合并前 10CG/Aria#211 T4 已经推进了 `ab-suite/trigger/` 与 `version.yaml`, 合并后计划只复核 `version`, 不复核 `skills_covered` / `total_eval_cases`。
4. **16 个版本点合并后未复核**: TASK-030 合并后没有复跑这 16 处的 custom checks。「这个值现在该是什么」只问了 `version.yaml`。
5. **远端已前进到本地没有的对象**: 两端 master 已到 `e4874d4`, 内容未知。TASK-001 会重测, 但 `metadata.scope_repos.head_at_a2` 已过时。
6. **归档会改写 proposal**: 归档 Step 2 的 warn_overlay 会向 `proposal.md` 写入 frontmatter 并改 Status (`openspec-archive/SKILL.md:180-246`)。TASK-022 用的 sha256 取自 `git show a563192`, 不受影响; 但周期 handoff 宜注明归档后 proposal 的哈希会变。

## Verdict

**PASS_WITH_WARNINGS** — counts **0C / 5M / 11m** — **Vote: REVISE**

## 是否足以开始 Phase B

**现在还不足以开始。** 5 条 major 都是局部修补:

1. 取号前加一步 merge (M1);
2. 改 owner_gates 第 14 项的未授权分支 (M2);
3. 补 §5 第 2 条这一处连带 (M3);
4. 加行尾机检 (M4);
5. 加 N4 机检 (M5)。

这些都不动任务结构。修完即可进 B.1 (B.1 本身仍受 owner_gates 第 1 项约束)。
