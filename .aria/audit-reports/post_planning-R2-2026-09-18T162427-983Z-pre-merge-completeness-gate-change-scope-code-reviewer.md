---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-18T17:17:52.905Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer 席 (证据与命令可执行性视角)

## 已实读文件

被审对象 (主仓 `5d435e9`, 两端 `ls-remote` 与本地一致):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (224 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1613 行, metadata 全部键 + 31 个 task)

对照读 (按视角取节):

- `openspec/changes/.../proposal.md` — `:4` `:9-11` `:18` `:77-80` `:118` `:122` `:130-136` `:140-149` `:162` `:181` `:267` `:285` `:338` `:340` `:360` `:366` `:368` `:378` `:386` `:407` `:409` `:414-426` `:428` `:447-451` `:462` `:467-469` `:473`
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (§1–§5)
- `CLAUDE.md` 多远程两条硬约束 + 规则 #3 / #6 / #8 / #9 / #10；`.aria/config.json` audit 块；`.aria/state-checks.yaml:29-46` 与 7 个 check 名
- aria 子模块 `1cb3872` 实读: `state-scanner/scripts/lib/spec_complete.py:273` `:733-744` `:924` `:1632-1646`、`collectors/multi_remote.py:105-115`、`state-scanner/lib/claim_lifecycle.py:475-535`、`lib/claim_schema.py:56-59`、`lib/track_id.py:61-81`、`lib/identity.py`、`scripts/phase1_gate.py:1125-1200` `:1427-1560`、`scripts/release_gate.py`、`phase-c-integrator/SKILL.md:42,57,131-133,157,603,612-623,625-630,638,754`、`audit-engine/SKILL.md:381-388,410-411,423,427-433`、`references/execution-modes.md:9-15,25-30,34,43-44,66,82`、`references/report-storage.md:8,37,43`、`report-format.md:5`、`pre-write-validation.md:3`、`config-loader/DEFAULTS.json:6-15,126-134`、`run_all_tests.sh:13-67`、`git-remote-helper/scripts/push_all_remotes.sh:103-119`、`spec-drafter/LEVEL_GUIDE.md:156-162`、`state-scanner/SKILL.md:180-184`、`openspec-archive/SKILL.md` Step 6/7、`phase-c-integrator/tests/test_pre_merge_gate.py:262-268`
- standards `940cb5b`: `openspec/project.md:114-118`、`openspec/templates/proposal-minimal.md:28-32`、`conventions/content-integrity.md §4.4/§4.5`、`conventions/skill-benchmark-exemption.md` 全文与 `8b49562..940cb5b` diff
- live 协调 ref `refs/aria/coordination` (本地 = origin `6ddf089`) 的三份本轨 claim；`docs/handoff/latest.md`

实跑 (全部在 `scratchpad/audit-R2-code-reviewer/` 下, 真仓零写入):

- `metadata.a2_state_runs.script` 全文 + `metadata.v2_state_runs.script` 全文, 按各自 `command` 在我自建副本上复跑
- `metadata.stage_cells.code` / `coord_ref_precheck.code` / `crlf_guard.code` / `commit_attribution.code` / `new_checks.code` (经 v2 脚本从 yaml 取码执行)
- audit-engine / phase-c-integrator / state-scanner 三个测试套件；catalog 的 5/8 可执行 fixture 三条命令；`check_bare_issue_refs.py`、`estimator.py`、content-integrity §4.5 自查一行命令、TASK-024 的 env 判据命令、TASK-007 的 grep 三态

### 复跑结论 (视角第 1 条, 先行给出)

| 证据块 | 结果 |
|---|---|
| `metadata.a2_state_runs` (归档门三态 + N1/N2/N3) | **逐字节一致** (`cmp` 通过, 2396 bytes) |
| `metadata.v2_state_runs` (N4/C1/N6/N7/N8/N9/N10) | **逐字节一致** (`cmp` 通过, 3449 bytes) |

两次复跑都在**与执笔容器不同的会话**里做, 副本与真仓在跑完后 `git status --porcelain` 均为空。v2.1 返修的两处不可复现 (N6 的 `own` 写死执笔容器 claim、N9 的同秒提交排序) **已确认修复**: N6 的 fixture 自造 claim 并由 `phase1_gate` 回填容器身份, N9 的 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` 钉死并每次 +60 秒, 我这边跑出的 `kinds` 顺序与嵌入值完全相同。

其余机械核验 (抽样, 全部与计划声称相符):

- `metadata.sc13_baseline` 9 项逐条重测: 通配 2 / timestamp 残留 4 / `completeness_gate.py` 0 / `change_id` 3 / `adaptive_rules` 3 / 「跳过校验…」1 / 「仍逐对评估三态并全部留痕」0 / 「不计入」0 / `anchor_base` 0 — **全中**
- `baseline_rebase`: 六个被引文件 `301641b..1cb3872` 零 diff；`spec_complete.py` 1/1、`multi_remote.py` 3/3；`CHANGELOG.md` `[1.73.0]` 现 `:104`、`[1.70.0]` 现 `:200`；`VERSION` 两条先例行现 `:7` / `:8` — **全中**
- 重写 b 的语料数字在 `a563192` 上重算 (changes + archive 并集去日期前缀): C = **154**, 有 `proposal.md` **154**, 无 A.2 文件 **54**, 其中有内联 `## Tasks` **17**, 三样全无 **37**; 当前 master 上为 53 / 16 / 37 — **与 tasks.md 重写 b 的「154 / 54 / 17 / 37, A.2 落盘后 53 / 16」逐个吻合**
- proposal sha256 在 `0a2ae53` / `a563192` / 当前 HEAD 三处相同 (`d3c9b4f2089031bd1adc…`), 内联 `## Tasks` 在 `:407`, 未勾选 checkbox 17 个 — 与读前必看第 22 条、重写 c 的快照前提一致
- `metadata.test_runner` 基线: audit-engine `Ran 104 OK`、phase-c-integrator `Ran 148 OK`、state-scanner (不带 `ARIA_COORDINATION_NO_PUSH`) `Ran 1605 … OK` — **全中**; catalog 5/8 的三条命令 `Ran 7 OK` / `Ran 1 OK` / `Ran 1 OK`, 字面 node id `FAILED (errors=1)` — **全中**
- 命令可执行性: TASK-007 的 grep 三态实测 **1 / 0 / 2** (与计划逐字相同); `check_bare_issue_refs.py --repo-root=… <file>` 可跑且对本目录两文件 0 命中; content-integrity §4.5 一行命令可跑 (我另造阳性对照文件, 确实报出命中); `estimator.py --project-root . capture --spec-slug/--spec-level/--n-tasks` 签名成立; TASK-024 的 `from lib.failure_handlers import no_push_requested_by_env` 在 `aria/skills/state-scanner` 下可导入并正确返回 1 (env 未设)
- 引用精度抽查 **60 余处** (清单见上「已实读文件」), 仅 1 处漂移 (见 m1), 其余逐条实读吻合 — 含 `spec_complete.py:924` = `if name == "SKILL.md":`、`:1642` = 两文件皆缺早退、`:273` = tasks.md checkbox 解析、`push_all_remotes.sh:103-119` 的成功判据、`DEFAULTS.json:130` = `"level_1": "off"`、`LEVEL_GUIDE:156-162` 跨模块条件、`project.md:117` Level 2 输出
- 归档门预演 (视角第 5 条): 全勾选态复跑得 `gate verdict=warn exit=0`, **warn 来源 = 唯一一条 `unverified_claims`「活体 dogfood (SC-11) 与 SC-… → dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在」** —— 与 TASK-031「预期 unverified_claims 含 4.4 行 dogfood 无可链接产物一条」及判断清单第 21 条完全一致。另实测 `d_payload` **非 null**, 而 `openspec-archive/SKILL.md:287` 的 Step 7 触发条件逐字是 `gate_result.d_payload != null` 且 headless 下不看 `--ack-unverified` ⇒ **归档 Step 7 在 warn 下确会产生外向动作 (建 issue)**, 计划已把它登记为 owner_gates 第 11 项并在 TASK-031 写明「裁不建则只跳过 Step 7」— **登记到位, 无遗漏**

## Findings

### Critical

无。

### Major

#### M1 `32076746` · major · issue · implementation · scope: `detailed-tasks.yaml TASK-001`

**一句话**: TASK-001 把本轨 claim 的容器路径写死为 `claims/023236f2/`, 而该 claim 在 v2.1 落盘前就已 `yielded`、本轨的 active claim 已转到容器 `bfe8285d`; 照字面执行既落不进「active ⇒ 心跳」也落不进「abandoned ⇒ 重认领」两个枚举分支, 且 `coord_ref_precheck` 的 `own` 集被钉在错文件上, 首跑必判 `other` 而停。

**证据 (我亲自核验)**:

计划侧 (`detailed-tasks.yaml` 四处写死同一容器):

- `:990` TASK-001 verification 逐字: `读 git show refs/aria/coordination:claims/023236f2/ 下 track_id 逐字为 pre-merge-completeness-gate-change-scope 的 active 条目 (A.2 时: s-86f7@1836.yaml, heartbeat 2026-09-17T08:47:15Z), 记为本轨 claim 文件`
- `:559` `own_claim_files: 'TASK-001 读到的本容器同 track 的 active claim 文件 (A.2 时: claims/023236f2/s-86f7@1836.yaml); 重新认领后换成新文件'`
- `:16` `metadata.claim: 'A.2 实读: … claims/023236f2/s-86f7@1836.yaml … status active …'`
- `:538` `coord_ref_precheck` 用法注释的例子同一文件

live 协调 ref 实读 (本地 `6ddf089` = `git ls-remote origin refs/aria/coordination`, 未做任何 fetch):

```
claims/023236f2/s-86f7@1836.yaml  status: yielded   heartbeat_at: 2026-09-17T11:54:49Z  track_id: pre-merge-completeness-gate-change-scope
claims/bfe8285d/s-73b9@1606.yaml  status: active    heartbeat_at: 2026-09-18T16:23:55Z  claimed_at: 2026-09-17T16:06:46Z  track_id: pre-merge-completeness-gate-change-scope
```

`derive_track_id` 实跑: 两者归一化后**同为** `pre-merge-completeness-gate-change-scope` (长度 44 < 64, 无非 ASCII)。本机 `get_container_id()` 实跑 = **`bfe8285d`**。

时间线 (证明 v2.1 落盘时事实已不成立, 不是审计期间才变的):

- 2026-09-17T11:54:49Z 023236f2 的 claim 转 `yielded`
- 2026-09-17T16:06:46Z bfe8285d 以原串重新认领 (`claimed_at`)
- 2026-09-17 17:42:53 +0000 提交 `5d435e9` (v2.1) —— **在重认领之后**, 而 `:16` / `:559` / `:990` 仍写 023236f2 与 status active

`docs/handoff/latest.md` 的 **Latest** 指针逐字印证这是一次有意的交接:「会话收尾 (simonfish/023236f2), 交双子星接手 … 两条 claim 经授权 `yielded` 让出 …, 双子星以原串重新认领 (须授权)」。

源码判据 (`aria` `1cb3872`):

- `claim_schema.py:56` `STATUS_ENUM = frozenset({"active", "yielded", "done", "abandoned", "unknown"})` —— `yielded` 是独立状态, 既非 active 也非 abandoned
- `claim_lifecycle.py:482` `heartbeat_by_track` 文档串逐字 "Refresh THIS container's **active** claims", `:491-493` 匹配是「container / 归一 track / **active**」三重合取
- `phase1_gate.py:1460` 的 `--include-terminal` 帮助文本只点名「终态 claim (**done / abandoned**)」, 不含 yielded

**失败场景 (执行者照字面做 → 得到什么)**:

1. 执行 `git show refs/aria/coordination:claims/023236f2/…` 找 active 条目 → 只有一条 `yielded` ⇒ 取不到。
2. 计划只给了第二条路: 「claim 已被扫成 **abandoned** ⇒ 获授权 (owner_gates 第 14 项) 后…重新认领」(`:991`, owner_gates `:131` 的条件逐字是「本容器 claim 已被扫成 abandoned」)。状态是 `yielded` 不是 `abandoned` ⇒ 该分支的前提字面不成立 ⇒ **无枚举内的合法下一步**。
3. 若执行者改按 tasks.md 判断清单第 11 条的「本容器」理解 (= `bfe8285d`) 去心跳, `heartbeat_by_track` 会刷新 `claims/bfe8285d/s-73b9@1606.yaml`, 该提交触到的文件**不在** `own_claim_files` 钉死的 `claims/023236f2/s-86f7@1836.yaml` 里 ⇒ `coord_ref_precheck` 判 `kind: other` ⇒ exit 1 ⇒ owner_gates 第 15 项触发「本会话不调 `/state-scanner`、不心跳推送、不强制对齐」。也就是说**owner 2026-09-17「已有 active claim 的心跳刷新免逐次授权」这条例外, 在 TASK-001 首跑就结构性地够不着**。
4. 附带: `phase1_gate.py --heartbeat-only` 的退出码**恒为 0** (`_heartbeat_only` 文档串逐字 "the code is always 0 — a heartbeat that refreshed nothing is an observation, never a gate failure"), 只有 `outcome` 能区分 `refreshed` / `error`。计划写了「期望 outcome refreshed」是对的, 但这一条一旦被按退出码读, 失败会静默通过 —— 建议在文本里显式点名「不看退出码」。

**建议修法** (小改, 不动设计):

- `:990` 把读取面从写死路径改为「按本会话 `get_container_id()` 求出的容器目录」, 并把状态分支从二分改为三分: `active` ⇒ 心跳; `yielded` / `abandoned` / 不存在 ⇒ 走 owner_gates 第 14 项 (把该项条件改写为「本容器无 active claim (yielded / abandoned / 缺失)」);
- `:559` `own_claim_files` 改为「TASK-001 当场求出的本容器同 track 的 active claim 文件全集 (A.2 时曾是 `claims/023236f2/s-86f7@1836.yaml`, **已于 2026-09-17 交接后失效**)」;
- `:16` `metadata.claim` 补一句交接事实与现值, 免得下一个执行者再按它复述。

---

#### M2 `4013aad9` · major · issue · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase`

**一句话**: `standards` 子模块在 v2.1 落盘前已从 `8b49562` 前进到 `940cb5b`, 其中 Rule #6 的 SOT `skill-benchmark-exemption.md` 升到 1.1.0 并新增**规范性**的 §4.1 `rule6_note` 最小模板; 计划的 `rule6_note` 一个模板字段都没有, 而 TASK-001 的基线复核清单**结构上不含 standards**, 这处漂移在整个 Phase B 都不会被任何一步发现。

**证据 (我亲自核验)**:

计划侧:

- `:38-40` `scope_repos` 第三项: `repo: standards` / `head_at_a2: 8b49562` / `surface: 不改`
- `:78` `baseline_rebase.standards`: 五个 conventions/openspec 文件「对 proposal 定稿时的 gitlink 21748d4 零 diff」
- `:995` TASK-001 基线复核逐字只枚举三组: `aria_zero_diff` 的每个文件、`aria_shifted` 各条冒号前的文件、`main_repo` 的文件 —— **没有 standards 任何一项**

实测:

```
standards HEAD = 940cb5b   (git submodule status)
git diff --shortstat 21748d4 8b49562 -- conventions/skill-benchmark-exemption.md   -> (空)
git diff --shortstat 8b49562 940cb5b -- conventions/skill-benchmark-exemption.md   -> 1 file changed, 21 insertions(+), 3 deletions(-)
git log -1 --format='%H %ci' 940cb5b -> 940cb5b … 2026-09-17 13:45:34 +0000
```

即: A.2 记录的 `8b49562` 上该文件确实零 diff (计划当时没写错), 但 `940cb5b` 在 **2026-09-17 13:45:34Z** 就已落地 —— 早于 v2.1 提交 (17:42:53Z), 也早于 v2 之外的任何返修。落地内容 (逐字节 diff 实读):

- `Version` 1.0.0 → 1.1.0
- §2 末句改为: 「`description` 或指令流程变动 ⇒ 一律第二行, **照跑场景 1**; `description` 变动另须跑**场景 4b 地板守卫**…」
- 新增 §3 边界注
- 新增 **`## 4.1 rule6_note 最小模板`** (`:59`), 其 YAML 模板要求五个键 `decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`, 并逐字规定「`description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ **不合规**」「`scenario4b` 为 `fail` 或 `void` ⇒ 义务未完成, **不得 ship**」

对计划的 `rule6_note` (`:134`) 逐键 grep, 两个被审文件全为 0 命中:

```
decision_table_row  tasks.md=0 yaml=0
description_changed tasks.md=0 yaml=0
scenario1           tasks.md=0 yaml=0
scenario4b          tasks.md=0 yaml=0
negctrl             tasks.md=0 yaml=0
场景 4b             tasks.md=0 yaml=0
```

(`场景 1` 在 yaml 里有 2 处, 但都是引 `AB_TEST_OPERATIONS.md` 的验收步骤, 不是 rule6_note 的字段。)

**失败场景**: 执行者按 TASK-001 复核基线 → 清单里没有 standards → 不会发现 Rule #6 的 SOT 已换版 → TASK-024 / TASK-031 按 `:134` 的散文 rule6_note 交付 → 该 rule6_note 按现行 SOT §4.1 **缺全部五个机读字段**, 属「不合规」。Rule #6 是不可协商规则, 其 SOT 就是这份文件, 而计划自身没有任何一步会红。

需要说清楚的是: **义务本身是满足得了的** —— 本 spec `description` 字段零改动 (`:134` 明写, TASK-015 `:1267` / TASK-016 `:1285` / TASK-017 `:1304` 以 awk 切 frontmatter + sha256 相等来守), 故 `description_changed: no`、`scenario4b: not_required` 成立。缺的是**格式落地 + 复核通道**, 不是实质动作。

**建议修法**:

1. TASK-001 基线复核清单补第四组: 对 `baseline_rebase.standards` 所列文件跑 `git -C standards diff --shortstat <A.2 记录的 SHA> <B.1 实测 gitlink> -- <文件>`, 并把 `scope_repos` 的 `head_at_a2: 8b49562` 更新为执行时实测 (现为 `940cb5b`);
2. `metadata.rule6_note` 按 SOT §4.1 补一段机读块, 取值 `decision_table_row: 3` / `description_changed: no` / `scenario1: <结果目录>` / `scenario4b: not_required` / `negctrl: n/a`, 现有散文作为其下的说明保留;
3. 顺带把 `AB_TEST_OPERATIONS.md` 新增的 §场景 4b 与 trigger 套件在 rule6_note 里点一句「本 cycle 不触发」, 免得下轮再被当成新发现。

### Minor

#### m1 `638d2a0f` · minor · issue · documentation · scope: `detailed-tasks.yaml TASK-029`

**一句话**: 16 个版本点里 `CLAUDE.md 两处 (:139 / :141)` 的行号已漂到 `:138` / `:142`。

**证据**: `git show a563192:CLAUDE.md | grep -n 1.73.3` → `139` / `141` (**A.2 时完全正确**); 当前 HEAD → `138` / `142`。成因是 `10CG/Aria#211` 轨 2026-09-17 改写了「项目状态」块。另 15 个版本点逐个实读全部命中: `README.md:8` badge / `:242` Plugin Version; `README.zh/ja/ko` 各 `:3` translated-from / `:10` badge / `:244` Plugin Version; `VERSION:24` 仍为 `v1.73.0` (计划已点名「三次漏改」); `system-architecture.md:189`; `version-scheme.md:23`。计数 2+9+2+1+1+1 = 16 ✓。TASK-029 已写「行号以执行时 grep 为准」, 故不改变执行者会做什么。

**建议**: 把 `(:139 / :141)` 也加上「A.2 时」限定, 与同句 README.md 的写法对齐。

---

#### m2 `f0e78a1e` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.revision_log`

**一句话**: 被审artifact 是 v2.1, 但文件头注释、`metadata.updated`、`revision_log` 与 tasks.md 头部 Status 都还自称 v2, 无 v2.1 条目。

**证据**: yaml `:1` `# Generated by task-planner (A.3) — …, v2 (2026-09-17, post_planning R1 rework)`; `:11` `updated: '2026-09-17'`; `revision_log` 末条为 `'v2 minor m1–m20 与顺带三项…'`, 全表无 v2.1; tasks.md `:6` `**Status**: A.2/A.3 v2 (2026-09-17, …) — 待 post_planning R2`。而 `5d435e9` 的提交信息逐字是「A.2/A.3 v2.1 — 证据层返修 (C1 核验发现的两处不可复现), 计划内容未变」。

**为什么只算 minor**: 计划内容确实未变 (我对 `tasks`/`metadata` 两块做了结构化比对思路的等价核验 —— 两个证据块之外的判据代码 `coord_ref_precheck` / `commit_attribution` / `new_checks` / `stage_cells` 我都是直接从仓内 yaml 取码执行的, 行为与嵌入 output 一致), 不改变执行者会做什么; 但 `revision_log` 是这份计划唯一的返修追溯面, 少一条会让「为什么 N6 的 fixture 改成自造 claim」在 Phase B 无处可查。

**建议**: `revision_log` 追加一条 v2.1 (只列 `v2_state_runs` 的 script/output 两块 + 两处不可复现的根因与修法), 头注释与 Status 同步。

---

#### m3 `0b3d81e7` · minor · risk · testing · scope: `detailed-tasks.yaml metadata.v2_state_runs`

**一句话**: v2 三态脚本第 99 行写死 `git fetch /home/dev/Aria`, 换机器直接失败。

**证据**: 我抽出的脚本第 99 行逐字为

```
    run(["git", "-C", str(bare), "fetch", "-q", "/home/dev/Aria", "refs/aria/coordination:refs/aria/coordination"])
```

我确认该调用是**从真仓 fetch 到临时裸仓**, 对真仓只读 (跑完 `/home/dev/Aria` 与 `aria` 的 `git status --porcelain` 均无新增); 结论侧确实零影响 (N6 的六态只依赖 fixture 自造的 claim)。代价只在: 席位机器无该路径时脚本在 N6 段整体抛错, 前面的 N4 / C1 也一并拿不到。

**建议**: 改成可选实参 (给了就 fetch, 不给就跳过并打印一行说明), 或直接删掉这一行 —— 按执笔人自述「空 ref 变体同输出」, 它对证据不承重。

---

#### m4 `f0e0d6b8` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.c25_five_questions`

**一句话**: 第 2 问把 `push_all_remotes.sh` 的成功判据写成「本地 `refs/remotes/<remote>/master` 等于 **HEAD**」, 源码比的是**推送前快照的 `PRE_LOCAL_HEAD`**。

**证据**: `git-remote-helper/scripts/push_all_remotes.sh:103-119` 实读, 判据行逐字:

```
if [ "$PUSH_EXIT" -eq 0 ] && [ -n "$POST_REMOTE_HEAD" ] && [ "$POST_REMOTE_HEAD" = "$PRE_LOCAL_HEAD" ]; then
```

同一处注释逐字说明「no network needed, no race condition」。另核: 该脚本全文 `ls-remote` 出现 **0** 次 —— c25 第 2 问「子模块不做 ls-remote 核验 ⇒ aria 的硬约束 2 由 TASK-028 承担」这半句**成立**, 是本条唯一承重的部分。其余四问逐条核对: `:603` / `:612-623` / `:625-630` / `:638` / `:614` 行号与内容全部吻合; `DEFAULTS.json:6-15` 里 `fail_on_partial_push: true` 与 `read_only_remotes: []` 都在区间内 ✓。

**为什么只算 minor**: 正常路径 (推送前工作树干净、HEAD 即分支尖) 两者取值相同, 不改变 TASK-030 会做什么。但若推送与快照之间本地又前进, 两个谓词会分叉。

**建议**: 改成「等于本次推送前的本地分支尖 (`PRE_LOCAL_HEAD`)」。

---

#### m5 `538a06a4` · minor · risk · testing · scope: `detailed-tasks.yaml TASK-022`

**一句话**: SC-11 的 post_planning 子断言被显式定义为不可判失败, 该格结构上不会红。

**证据**: TASK-022 `:1402` 逐字: `post_planning 为 present (tasks.md 读前必看第 16 条; 实跑为 missing 属新发现: 记台账并上报, 本任务不判失败, 也不改断言)`。tasks.md 读前必看第 16 条同样写「本条无区分力, 区分力在重写 c」。

**为什么只算 minor 而不是恒绿类 major**: 这是**声明过的**无区分力格, 且区分力已被移到重写 c 的 `a563192` 快照格 (那一格有真反事实: 判据退回「只看两个文件」⇒ `not_applicable/no-a2-artifact`), 归属规则本身另有 SC-1 / SC-2 / SC-19 的单测与 TASK-019 / 020 的反事实覆盖。我另实测当前 `.aria/audit-reports/` 里本轨报告 38 份 (post_spec 30 份, post_planning 已有 R1 六份 + R2 在落), 故 TASK-022 跑到时 post_spec `matched_count ≥ 6` 与 post_planning `present` 都会因正确原因成立。

**建议**: 保留现状即可; 若要更干净, 把这一条从「断言」降格成「观察项」措辞, 免得读者误以为它是闸。

## 对执笔人自报薄弱点的表态

**(a) `stage_cells` 39 格「在 P6 之前以终局结束」按求值总序推出、实现前无法验证 — 可接受。** 我把 39 格逐个对着 proposal §1.0 的求值总序过了一遍: TASK-008 的 13 格全落 argparse / config / P1 (`audit_not_enabled`) 或纯常量比对 (SC-21 三格根本不跑脚本); TASK-009 的 8 格全落 P2a/P2 的 exit 2; TASK-010 的 2 格落 P3 的 `config_unreadable` 与 `spec_level_undetermined`; TASK-011 的 16 格全落 P5 格 B–E 或豁免短路。没找到反例。更关键的是, 即便某格推错, `cell_status.py` 的三态实跑 (我复跑得 `bad_cell_renamed` 与 `bad_method_errors_before_cell` 都输出 `["not-run"]` 且 exit 1) 保证它显示为 not-run 而判红, 不会假绿 —— 这条兜底把「推导可能错」的代价从「静默通过」降到「当场红」。

**(b) `coord_ref_precheck` / `commit_attribution` 偏严、方向 fail-closed — 方向可接受, 但当前参数化不可接受 (即 M1)。** 「心跳格式变 / 同容器同轨多 claim / 改 `docs/handoff/latest.md` 都停下请裁」作为**方向**我完全认可: 误停的代价是一次 owner 问答, 误放的代价是污染生产协调 ref 或推走他轨提交, 不对称。`commit_attribution` 把 `latest.md` 一律判 foreign 也是对的 (它是 Rule #9 的共享指针)。但 M1 表明: `own_claim_files` 钉在一个已交接失效的容器文件上, 使这份「偏严」在 TASK-001 首跑就必然触发 —— 那不是严格度问题, 是参数错。修掉 M1 之后 (b) 成立。

**(c) 第 99 行 `git fetch /home/dev/Aria` — 可接受 (已按 m3 记为 minor)。** 我实测确认: 对真仓只读、对结论零影响、本机复跑逐字节一致。它只伤及换机复现, 且修法是删一行或改成可选参数, 不动任何判据。

**(d) `own_claim_files` 描述生产用法、与 fixture 自造 claim 并列可能被读成矛盾 — 不可接受 (问题定性错了)。** 执笔人把它归为**措辞歧义**, 但我核到的是: 这两句根本不矛盾 —— fixture 侧确实已正确地与容器身份解耦 (v2.1 的修复是对的), 而生产侧那句话**本身就是错的** (钉死的容器与 claim 状态在 v2.1 落盘前已失效, 见 M1 的时间线)。按 (d) 的自我诊断去改措辞, 改完仍然会在 TASK-001 首跑停住。必须按 M1 改参数化, 而不是改说明文字。

## 风险 / 疑问 (不计入 finding)

1. **本轨存在跨容器并发面**: `claims/bfe8285d/s-73b9@1606.yaml` 的心跳是 2026-09-18T16:23:55Z (本轮派发前约半分钟), `phase: A.2`。计划 TASK-001 只读单一容器目录, 不做跨容器碰撞判读, 重认领命令用的是 `--mode advisory` (放行姿态)。修 M1 时建议一并把「读到他容器 active claim」纳入 owner 等待点, 否则 Phase B 起跑时的占用判断没有落点。
2. **`metadata.test_runner` 里 state-scanner 那条与环境互斥的结论我复现到了一半**: 不带 `ARIA_COORDINATION_NO_PUSH` 时 `Ran 1605 … OK` 与计划一致; 带该变量会失败 1 条 (`test_refresh_without_no_push_publishes_to_remote`) 这一半我没跑 (跑它需要在本会话设该环境变量, 属会话级副作用, 避开)。TASK-021 / TASK-027 都已写明「会话不带该变量」, 风险可控。
3. **`AB_TEST_OPERATIONS.md` 在 `a563192..HEAD` 间 +36/-2** (新增场景 4a/4b 与 trigger 套件行)。计划引用的四个锚点我逐个实读仍在 (`场景 1` `:201`、`验收 delta.pass_rate > 0` `:220`、`场景 1 运行前置` `:223`、`push_skipped` `:228`), 且该文件在 `baseline_rebase.main_repo` 清单内、会被 TASK-001 复核到 —— 不构成 finding, 但它与 M2 同源, 一并复核更省事。
4. **`ab-suite/version.yaml` 仍是 1.5.0**, `skills_covered: 32` / `total_eval_cases: 84` 我程序化重算完全一致 (加 eval id 3 后应为 32 / 85, 与 TASK-023 声称相同)。读前必看第 4 条预期的并发轨 `10CG/Aria#211` T4 至今未把它升过 1.5.0, 故 TASK-023 的「被占即顺延」暂时不会触发 —— 执行时仍按计划实读 `origin/master` 取值即可。
5. **`spec_complete.py` 的 `classify_symbol_liveness` 会把任何 `*/.aria/config.json` 与 `hooks.json` 里出现的符号名判为 `aria_plugin_integration`** (`:733-744` 实读, 判据为 narrow 白名单)。计划已用 `guard_config_hooks` 兜住, 我在当前树实跑该命令**零输出** (rc=1), 与 `sc12_liveness.blind_spots` 声称一致。

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C / 2M / 5m**

**Vote: REVISE**

## 是否足以开始 Phase B

**不足以 (差两处小修)** —— 证据层本身已经很硬 (两份三态脚本在异容器逐字节复现, 60 余处 `file:line` 引用仅 1 处 post-A.2 漂移, 全部基线数字与测试计数实测吻合), 但 M1 会让 TASK-001 在第一步就落进未枚举的 claim 状态并被自己的 fail-closed 检查挡住, M2 会让 Rule #6 的交付物按现行 SOT 判不合规且计划内无人会发现; 两处都是文本级修改 (改读取面与分支条件、给基线复核补 standards 一组、rule6_note 补五个机读键), 不触及设计, 改完即可进 B.1。
