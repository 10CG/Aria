---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-19T11:44:51.948Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — code-reviewer 席 (证据与命令可执行性视角)

## 已实读文件

被审对象 (主仓 `5fd7e08`, yaml 落在 `12c870d`):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (227 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1675 行; metadata 全部键 + 31 个 TASK)

对照读:

- `proposal.md` 按视角取节: `:4` `:9` `:10` `:16` `:18` `:77-80` `:103` `:118` `:122` `:153` `:162` `:172` `:181` `:187` `:210` `:221` `:267` `:271` `:285` `:325` `:338` `:340` `:343` `:356` `:360` `:366` `:368` `:370` `:378` `:386` `:393` `:407` `:409-451` `:428` `:447-451` `:453-461` `:462` `:465` `:466` `:467` `:468` `:469` `:480` `:488`
- `.aria/audit-reports/post_planning-R2-…-aggregated.md` 全文; 我自己的 R2 席位报告全文
- `CLAUDE.md` 多远程两条硬约束 + 规则 3 / 6 / 8 / 10; `.aria/config.json` (audit 块 + phase_c_integrator 块); `.aria/state-checks.yaml:29-46`
- standards `940cb5b`: `conventions/skill-benchmark-exemption.md` (§2 决策表全文 + §4.1 模板全文 + Version 行 `:3`)、`conventions/git-commit.md:188-215` (§6.2)、`conventions/content-integrity.md` §4.5
- aria `1cb3872` 实读 (逐行清单见下方引用精度表)
- `docs/handoff/latest.md` 全头部与最新两份 handoff 的 frontmatter; `aria-plugin-benchmarks/{AB_TEST_OPERATIONS.md, ab-suite/*.json, ab-suite/version.yaml}`

实跑 (全部在 `scratchpad/audit-R3/code-reviewer/` 下; 真仓只做 `log` / `show` / `diff` / `ls-tree` / `ls-remote` / `grep` 等读操作, 零 git 写操作, 零文件改动):

- `metadata.a2_state_runs.script` 全文按其 `command` 复跑 **两次** (副本 A = 主仓 `5fd7e08`; 副本 C = 主仓 `a563192`, 即该证据 `what` 字段自述的前提)
- `metadata.v2_state_runs.script` 全文按其 `command` 在副本 B 复跑
- `metadata.commit_attribution.code` 直接从 yaml 取码, 跑 7 个自造场景 + 3 组真实提交
- `metadata.coord_ref_precheck.code` / `stage_cells.code` / `new_checks.code` / `crlf_guard.code` / `sc12_liveness.code` 全部从 yaml 取码落盘 (经 v2 脚本执行)
- `derive_track_id` / `get_container_id` / `check_bare_issue_refs.py` / `estimator.py` / TASK-024 的 env 判据 / `sc13_baseline` 七项计数 / CRLF `ls-files --eol` / standards 六文件 shortstat

### 复跑三态证据 (视角第 1 条, 先行给出)

| 证据块 | 结果 |
|---|---|
| `metadata.v2_state_runs` (N4 / C1 / N6 / N7 / N8 / **N9 含 v2.2 新增 3 态** / N10) | **逐字节一致** (`cmp` 通过, 3977 bytes) |
| `metadata.a2_state_runs` 在主仓 `a563192` (证据自述前提) | **逐字节一致** (`cmp` 通过) |
| `metadata.a2_state_runs` 在主仓 `5fd7e08` (当前 master) | **不一致** (2630 vs 2396 bytes; 7 条 liveness 状态行全部不同) — 见 m1 |

两点结论: (1) v2.2 声称「`a2_state_runs` 逐字节不变」属实, 且我在异于执笔容器的会话里复现了**两份**证据; (2) `v2_state_runs` 的 N9 新增三态 (`shared-only` / `own-release-sync` / trailer 不能洗白 foreign) 我逐字节复现, 判据代码改动与嵌入输出自洽。

### 引用精度抽查 (33 处, aria 对 `1cb3872` 实读 / proposal 与主仓对当前文件实读)

| 引用 | 实读 | 一致 |
|---|---|---|
| `phase-c-integrator/SKILL.md:42` 配置表缺省行 | `\| audit.checkpoints.pre_merge \| "off" \| …` | 是 |
| 同 `:57` 触发条件摘要 | `…且 audit.checkpoints.pre_merge != "off" 时，C.2 合并前触发…` | 是 |
| 同 `:131` 步骤 2 (计划写「不动」) | `2. 检查 audit.enabled — false 则跳过` | 是 |
| 同 `:132` 步骤 3 | `3. 检查 audit.checkpoints.pre_merge — "off" 则跳过` | 是 |
| 同 `:157` 旧 schema 残留 | `audit_report: ".aria/audit-reports/pre_merge-{timestamp}.md"` | 是 |
| 同 `:603` / `:613` / `:614` / `:623` / `:625` / `:630` / `:638` (c25 五问) | 触发时机 / expected_sha / submodule status --recursive / 阻断 / 决策表 / fail_on_partial_push 行 / detached HEAD | 是 (7/7) |
| 同 `:754` hotfix 降级条件 | `…仅 audit.enabled=true 且 audit.checkpoints.pre_merge != "off" 时…` | 是 |
| `audit-engine/SKILL.md:381-384` / `:385-388` 两注释块 | allow_dangling_change_ids / allow_incomplete_checkpoints 各自块 | 是 |
| 同 `:423` 同形改写点 | `…仅 audit.enabled=true 且 pre_merge checkpoint != off 时降级到 convergence…` | 是 |
| 同 `:427` / `:433` 相关文档 | `## 相关文档` / agent-team-audit 行 | 是 |
| `execution-modes.md:9` / `:10` / `:15` | 入口两行 + 优先级链句 | 是 |
| 同 `:25-30` 互补说明 / `:34` 开围栏 / `:66` 闭围栏 | 均命中 | 是 |
| 同 `:37` `:41` `:43` `:46` `:54` `:63` 五个 Step 标记 | Step 1-5 分别落该处, 全在同一围栏内 | 是 |
| 同 `:44` / `:82` 两处 bypassed 文案 | `by config` 与 `missing={checkpoint_names` 两种拼法 | 是 |
| `report-storage.md:8` / `:37` / `:43`; `report-format.md:5`; `pre-write-validation.md:3` | 5-field schema / 向后兼容两句 / 旧 schema 说明 / 关联行 | 是 (5/5) |
| `spec_complete.py:273` 归档门读 checkbox | `boxes = _CHECKBOX_RE.findall(tasks_text)` | 是 |
| 同 `:733-744` hooks/config 分类器 | `_is_hooks_or_config_path` 全函数 | 是 |
| 同 `:924` / `:1636` / `:1642` | `if name == "SKILL.md":` / 原位注释 / 两文件皆缺早退 | 是 |
| `multi_remote.py:107-113` (计划称「不移」) | freshness join defaults 注释块 | 是 |
| `phase-a-planner/SKILL.md:267`; `phase-b-developer/SKILL.md:204` `:214` `:277` | 三处 `{timestamp}` 形态 + mid_post_spec 字面键行 | 是 (4/4) |
| `state-scanner/SKILL.md:182` 入口心跳 | 触发条件句 | 是 |
| `test_pre_merge_gate.py:266` catalog 真方法名 | `test_case_e_malformed_aether_main_leg_routes_fail` | 是 |
| `config-loader/DEFAULTS.json:130` | `"level_1": "off"` | 是 |
| `push_all_remotes.sh:103-119` 成功判据 | 判据行在 `:119` (`POST_REMOTE_HEAD = PRE_LOCAL_HEAD`) | 是 (区间含之) |
| `release_gate.py:253` choices | `["done", "yielded", "abandoned"]` | 是 |
| `claim_schema.py:56` STATUS_ENUM | 五值 frozenset | 是 |
| `run_all_tests.sh:41-46` pytest 判据 | `is_pytest_suite()` 全函数落该区间 | 是 |
| `.aria/state-checks.yaml:29-46` | `no-unresolved-version-placeholder` 全条目 | 是 |
| proposal `:77-80` canonical call | 与 `metadata.canonical_call` 逐行相同 (v2 脚本亦断言 True) | 是 |
| proposal `:407` `## Tasks` + `:409-451` 内联 17 个 checkbox | 实测 17 个, 落在 409-451 | 是 |
| `AB_TEST_OPERATIONS.md` 规则 1 / 场景 1 / delta 验收 / push_skipped | `:173` 未声明视为 descriptive; `:201` / `:220` / `:228` | 是 |
| `git-commit.md §6.2` (M3 的 trailer 依据) | `:193` `### 6.2 Spec 关联`, 示例 value 是 `standards/openspec/changes/{feature}/spec.md` | **部分** (trailer 键一致; value 形态不同, 但本仓 `10CG/Aria#211` 有 5 次同形先例, 不构成错引) |
| 主仓 16 个版本点 | README.md `:8`/`:242`; zh/ja/ko 各 `:3`/`:10`/`:244`; VERSION `:24`; system-architecture `:189`; version-scheme `:23` 全中; **CLAUDE.md 实为 `:138`/`:142`, 计划写 `:139`/`:141`** | 15/16 (见风险 1) |

另: `sc13_baseline` 七项计数复测全中 (2 / 4 / 0 / 3 / 3 / 1 / 0); 两个 CRLF 文件 `i/crlf w/crlf` 属实; standards 六文件 shortstat 复测与 v2.2 新写的断言逐字相符。

## Findings

### Critical

无。

### Major

#### M1 `9122f4a9` · major · issue · implementation · scope: `detailed-tasks.yaml metadata.commit_attribution`

**一句话**: v2.2 收紧后的路径三分集与本轨**自己的**交付物足迹不匹配 —— 有两个在正常路径上必然发生的形态会把本轨自己的提交判成非本轨并停在 owner_gates 第 16 项; 这与判断清单第 33 条与 `cannot_catch` 里「收紧的代价只有 TASK-029 漏写 trailer」的自述直接矛盾。

**证据 (我从 yaml 取码实跑)**:

(i) **TASK-023 的交付物整条落在 `SHARED` 集里, 而 TASK-023 没有 trailer 要求**。`commit_attribution.code` 的 `SHARED` 逐字含 `aria-plugin-benchmarks/ab-suite/audit-engine.json` 与 `aria-plugin-benchmarks/ab-suite/version.yaml` (yaml `:591-593`); TASK-023 的 `deliverables` 恰为这两个文件 (yaml `:1477-1478`), 末条只写「主控在主仓 feature 分支提交」(yaml `:1487`), 全任务无 `Spec:` trailer 字样。实跑:

```
CASE 1 (audit-engine.json + version.yaml, 无 trailer)
{"verdict": "stop", "commits": 1, "kinds": ["shared-only"]}
CASE 2 (同两文件 + TASK-029 的 trailer)
{"verdict": "ok", "commits": 1, "kinds": ["own-release-sync"]}
CASE 7 (同两文件 + verification-ledger.md 同提交)
{"verdict": "ok", "commits": 1, "kinds": ["own"]}
```

(ii) **本轨的生成器不在 exclusive 集里**。`.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 是本计划的产出工具 (禁手改 yaml, 一律经它), 它既不在 `SHARED` 也不匹配任何 exclusive 前缀 ⇒ 判 `foreign`。对**真实提交**实跑:

```
$ python3 -B attrib.py 12c870d^ 12c870d     # 本轨自己的 v2.2 规划提交
{"verdict": "stop", "commits": 1, "kinds": ["foreign"]}
逐文件: foreign  .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py
        exclusive openspec/changes/<SID>/detailed-tasks.yaml
        exclusive openspec/changes/<SID>/tasks.md
```

**失败场景**:

- 形态 (ii) 现在就可达: 执笔实例提出、owner 尚未裁定的三条都要改 `gen_yaml.py`。owner 一旦裁定并落 v2.3 返修提交, 该提交未推送时 TASK-001 的「回落前对 `origin/master..<起点>` 跑 commit_attribution」立刻得 `stop`, B.1 入口多一道非预期的 owner 裁定才能往下走。
- 形态 (i) 在正常路径上**必然**发生: TASK-023 按字面提交两个交付物 → TASK-030 的提交范围核验对 `origin/master..<feature>` 跑 attribution → 该提交判 `shared-only` → exit 1 → 停在 owner_gates 第 16 项, 未裁不推送、不开 PR。也就是说这条核验在一切都做对的情况下**恒红**。

**为什么是 major 不是 minor**: 它改变执行者会遇到什么 —— 一次结构性的、计划自己预言不会发生的停顿; 并且判断清单第 33 条是要交 owner 复议的 (Rule #10 §5), 现在给 owner 的代价陈述是错的。定 major 不定 critical 的理由: 方向仍是 fail-closed (误停不误放), 不会推走他轨内容。

**建议修法 (任选其一, 均已实测有效)**: (a) 给 TASK-023 补与 TASK-029 相同的 trailer 要求 (CASE 2 转 `own-release-sync`); 或 (b) 让 TASK-023 把台账一并提交 (CASE 7 转 `own`)。另把 `.aria/notes/2026-09-17-199-a2-a3-tooling/` 加进 `exclusive()` 的前缀集或作为 `extra` 参数传入, 并把判断清单第 33 条与 `cannot_catch` 的代价陈述改写为「本轨凡是整条只落 shared 集或只落工具目录的提交都须带 trailer」。

---

#### M2 `e06fea62` · major · issue · testing · scope: `detailed-tasks.yaml TASK-018`

**一句话**: v2.2 新写的 `rule6_note` 把 `scenario4b: not_required` 完全架在 `description_changed: no` 上, 而该字段自称的机械依据只覆盖**四份被编辑的 SKILL.md 中的三份** —— `phase-a-planner/SKILL.md` 是 TASK-017 的交付物、带 `description` frontmatter, 却不在任何 frontmatter 比对清单里。

**证据 (实读)**:

- `metadata.rule6_note.fields_basis` (yaml `:140`) 逐字: 「`description_changed` 为 no 的判据 = TASK-015 / 016 / 017 改前改后比**三份** SKILL.md 的 frontmatter, 逐字相同 (TASK-018 复核)」
- TASK-018 verification (yaml `:1381`) 逐字: 「audit-engine / phase-c-integrator / phase-b-developer **三份** SKILL.md 的 frontmatter 与 aria 起点逐字相同」
- TASK-017 的 `deliverables` (yaml `:1356-1359`) 含 `aria/skills/phase-a-planner/SKILL.md`; 其 CRLF 条款 (yaml `:1365`) 只说「phase-a-planner/SKILL.md 是 LF」, 没有任何 frontmatter 不变的断言
- 实读 `aria/skills/phase-a-planner/SKILL.md:1-8`: frontmatter 内确有 `description: |` 多行块
- SOT `conventions/skill-benchmark-exemption.md` §2 末段逐字: 「`description` 变动另须跑场景 4b 地板守卫」; §4.1 逐字: 「`description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规」

**失败场景**: TASK-017 编辑 `phase-a-planner/SKILL.md:267` 时若连带触到 frontmatter 的 `description` (多行块, 编辑器整块替换或行尾处理都可能碰到), 计划里没有任何一步会红 —— TASK-018 不比它, TASK-031 的齐备性断言只查五个字段在不在、有没有尖括号残留, 不查取值真假。结果是带着「`description_changed: no` / `scenario4b: not_required`」ship, 而按 SOT 这已是未完成的 Rule #6 义务 (Rule #6 不可协商)。

**为什么是 major**: 漏的是一个必做核验项, 且方向 fail-open (错了没人红)。我承认现实概率不高 (改的是 `:267` 的一行散文), 但整条 Rule #6 合规链条就靠这一个字段, 而它的依据自称机械、实际有洞。

**建议修法**: TASK-018 的 frontmatter 比对清单从三份扩到**四份** (加 `phase-a-planner/SKILL.md`, 它是 LF, 不需去 CR), 并把 `fields_basis` 里的「三份」同步改为「四份」。一行改动。

### Minor

#### m1 `a5996c58` · minor · risk · testing · scope: `detailed-tasks.yaml metadata.a2_state_runs`

**一句话**: `a2_state_runs` 的六个 liveness 状态是 premise-bound 到主仓 `a563192` 的; 在 Phase B 实际执行的树 (当前 master `5fd7e08`) 上, 七条状态行**全部**不再复现, 根因是本轨自己提交进主仓的 `gen_yaml.py` 让符号恒为 `alive`。

**证据 (两次复跑, 同一脚本同一参数, 只换副本的主仓 SHA)**:

```
副本 C (主仓 a563192, aria 1cb3872)  -> cmp 通过, 逐字节一致
副本 A (主仓 5fd7e08, aria 1cb3872)  -> 差异如下 (节选)
  A  嵌入: status=ambiguous categories=[]      实跑: status=alive categories=['code_reference', 'generic_path_call']
  D  嵌入: status=dead  L1=False verdict=block 实跑: status=alive L1=True  verdict=warn
  D2 嵌入: status=dead  L1=False verdict=block 实跑: status=alive L1=True  verdict=warn
  E  嵌入: categories=['generic_path_call']    实跑: 多出 code_reference
  C/B/F 同样多出 code_reference / generic_path_call
```

归因 (实测): `git grep -l -F completeness_gate` 在 `a563192` 上除 proposal 与 audit-reports (分类器按 `spec_complete.py:930` 视为散文, 不计 alive) 外无命中; 在 `5fd7e08` 上多出 `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` —— 一个 `.py` 文件同时命中 `_code_reference_match` 与字面脚本路径匹配, 于是 `code_reference` + `generic_path_call` 两项恒在。

**为什么只算 minor**: 验收面是 L2 与 L3 (tasks.md 重写 a 明写 L1 只作确认), 而我实测 L2 在当前树上**仍然区分** (只有把调用写进 SKILL.md 的 fenced bash 块才出 `aria_plugin_integration`), L3 也仍区分 (F 态 L3=False)。TASK-021 / TASK-031 要求的是目标态三条全真, 那在当前树上照样成立, 执行者不会做错也不会卡住。

**但要改的地方有三处**: (1) tasks.md 重写 a 的叙述「脚本不存在 ⇒ 分类器判 `ambiguous`」「调用只写在 SKILL.md 散文里 ⇒ `dead`, L1 与 L2 同假」「对照态 D2」在执行期的树上已为假; (2) `sc12_liveness.blind_spots` 现在低估了 —— L1 在当前树上**零区分力** (一切状态都 warn/不 block), 不只是它列的两态; (3) `guard_config_hooks` 只拦 `config.json` / `hooks.json`, 拦不到 `.py`, 建议在 TASK-021 复跑前把守卫扩成「仓内除 skills 树与散文面外还有谁命名该符号」。

---

#### m2 `af5e1e47` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata.owner_gates`

**一句话**: owner_gates 第 14 项为 `--include-terminal` 给的理由对 `yielded` 不成立 —— 源码里 `yielded` 根本不算终态, 不带该 flag 也看得见。

**证据**: yaml `:131` 逐字「`--include-terminal` 对三态同样必要 —— 不带它, takeover 判据看不见终态 claim」。实读 `aria/skills/state-scanner/lib/collision.py:416` 与 `:420`:

```
_TERMINAL = ("done", "abandoned", "unknown")
if not include_terminal and c.status in _TERMINAL:   # yielded 不在集合里, 永不跳过
```

`phase1_gate.py:1463` 的 help 文本同样只点名 `done / abandoned`。本轨现存的正是一条 `yielded` (`claims/023236f2/s-86f7@1836.yaml`, 我实读协调 ref 确认), 即计划最可能走到的那一态。

**为什么只算 minor**: 结论 (三态下一步都要重新认领) 我复核成立 —— `heartbeat_by_track` 的匹配是 container / 归一 track_id / **active** 三重合取 (`claim_lifecycle.py:482` 与 `:505-560` 实读), 对 `yielded` 一律不刷新; 带上 `--include-terminal` 对 yielded 只是无害冗余。执行者按字面做不会错。

**建议**: 把理由句改为「done / abandoned 需要它才看得见; yielded 不属 `collision._TERMINAL`, 带上属无害冗余」。

---

#### m3 `a2d80059` · minor · risk · documentation · scope: `detailed-tasks.yaml metadata.commit_attribution`

**一句话**: `cannot_catch` 里「`docs/handoff/latest.md` 这类共享指针**一律**判 foreign」不是机制保证, 而是对该文件当前形态的依赖。

**证据**: `exclusive()` 对 `docs/handoff/*.md` 的判据是读该提交里的文件头 2000 字节找 `^track-id: <SID>$`。实跑:

```
CASE 4 latest.md 无 frontmatter (= 当前真文件形态)  -> {"verdict":"stop","kinds":["foreign"]}
CASE 5 latest.md 带 track-id: <本轨 SID> 的 frontmatter -> {"verdict":"ok","kinds":["own"]}
```

我实读 `/home/dev/Aria/docs/handoff/latest.md`: 首行是 `# Latest Session Handoff`, 无 frontmatter、无 `track-id:` 行 ⇒ **今天成立**。

**为什么只算 minor**: 当前形态下结论正确, 且 latest.md 按既有约定是纯指针文件, 不带 frontmatter。**建议**把 `cannot_catch` 的「一律」改成「在 latest.md 不带本轨 `track-id` frontmatter 的前提下判 foreign」, 或把 `docs/handoff/latest.md` 直接写死进 `SHARED`, 让它与文件内容无关地恒需请裁。

---

#### m4 `638d2a0f` · minor · issue · documentation · scope: `detailed-tasks.yaml TASK-029`

**一句话**: TASK-029 的 `deliverables` 含 `verification-ledger.md` (exclusive 路径), 与同一任务 verification 里「本任务的交付物**整条**落在 `commit_attribution` 的 shared 集里」互相矛盾。

**证据**: yaml `:1604-1614` 的 deliverables 末项是 `openspec/changes/pre-merge-completeness-gate-change-scope/verification-ledger.md`; yaml `:1622` 逐字「本任务的交付物整条落在 metadata.commit_attribution 的 shared 集里, 不带 trailer 会…判 shared-only 而停」。实跑 CASE 7 证明: 只要台账同提交, 该提交判 `own`, trailer 不再承重。

**为什么只算 minor**: 两种执行路径 (带台账 / 不带台账) 都不会得出错误结论, trailer 写上总是安全的。**注意去重**: 本条的四元组与 R2 我那条 `638d2a0f` (TASK-029 的 CLAUDE.md 行号) 撞车但内容是两件事, 按 R2 聚合对同类情形的处理, 请并列保留不要丢弃。

## R2 对账

| 编号 | 判定 | 证据 |
|---|---|---|
| **PP2-M1** (architecture / TASK-001 claim 身份钉死 + 对 `yielded` 失明) | **closed** | TASK-001 第 2 条改为按 (本容器, 归一 track_id, active) 三元组运行时解析, 0 / 1 / 2+ 三种条数各有明确处置 (yaml `:1048`); owner_gates 第 14 项的触发条件从只认 `abandoned` 扩成三终态加「本容器该轨无 claim」并写明三者下一步相同 (yaml `:131`); `metadata.claim` / `container` 降级为「记录时事实」(yaml `:15-16`)。我独立复跑: 计划给的容器 id 命令原样可执行, 返回 `bfe8285d`; `git ls-tree -r --name-only refs/aria/coordination` 候选枚举可用; 本轨现存三条 claim = 1 active (`claims/bfe8285d/s-73b9@1606.yaml`) + 1 yielded + 1 abandoned, 其中 abandoned 那条的 `track_id` 是带容器后缀的 `…-bfe8285d`, 我实跑 `derive_track_id` 确认它归一化后**仍带后缀**、不等于原串 ⇒ 计划的「逐字等于」过滤与 `heartbeat_by_track` 的归一匹配在这批真数据上给出同一个集合, 不会出现 own 集与实际心跳面不一致。残留只有 m2 (理由句) 与风险 3 (读本地 ref 未先快进)。 |
| **PP2-M2** (implementation / TASK-001 `own_claim_files` 钉在失效文件上) | **closed** | `own_claim_files` 改为「TASK-001 运行时解析出的 claim 文件, 可能不止一条, 不是写死的路径」并补了 fixture 反向指针 (yaml `:566`)。我按 R2 的失败链逐环复验: 解析面用的是活的协调 ref (本地 `f121e5d5` 与 `git ls-remote origin` 完全相同, 无分叉), 解析结果就是那条 active claim; `coord_ref_precheck` 的 own 集因此不会在首跑判 `other`。N6 六态我逐字节复现, fixture 仍是自造 claim 并从 `phase1_gate` 返回的 `own_claim` 回填, 不依赖执笔容器身份。 |
| **PP2-M3** (implementation / `commit_attribution` 放行「整条全落 FIXED 集」) | **partially** | **原洞已堵**: 我对真实的他轨发版提交 `1b9734a` (`chore(release): aria-plugin v1.73.3 主仓同步面 — gitlink fcbc8ac→1cb3872`, 8 个文件含 `aria` gitlink 行) 实跑得 `{"verdict":"stop","kinds":["shared-only"]}`; trailer 也确实洗不白 foreign 路径 (N9 末态复现)。**但开了新洞**: 三分路径集与本轨自己的足迹不匹配, 两个可达形态把本轨提交判成非本轨 (M1 的 CASE 1 与真提交 `12c870d`)。故判 partially —— 收紧方向对、他轨面守住了, 本轨面漏了。 |
| **PP2-M4** (documentation / `baseline_rebase` 失效断言 + `rule6_note` 不含 SOT 五字段) | **closed** | 两半都闭合。(1) standards 断言重写并限定 (yaml `:78`), 我对 `21748d4..940cb5b` 逐文件复测: 四个被引文件 shortstat 输出**全为空**, `content-integrity.md` +56/-2、`skill-benchmark-exemption.md` +21/-3, 且 `git diff --name-only` 全仓**恰好只有这两个文件** —— 新写的每个数字都对得上。(2) `rule6_note` 现含 SOT §4.1 的全部五个字段 (yaml `:134-140`), 取值 `decision_table_row: 3` / `description_changed: no` / `scenario1: <待回填>` / `scenario4b: not_required` / `negctrl: n/a`; 我逐字读 §4.1 的合规判据, 「不合规」只在 `description_changed: yes` 时触发, 本组合合规。**残留 (不单列 finding)**: TASK-001 的基线复核枚举仍只有 `aria_zero_diff` / `aria_shifted` / `main_repo` 三组 (yaml `:1055`), standards 的重测要求只写在 `baseline_rebase.standards` 的散文与 tasks.md 读前必看第 5 条里 —— 有指令、没进可执行清单, 建议顺手补成第四组。另 M2 是 `rule6_note` 这一半新开的洞, 不是 PP2-M4 没闭合。 |
| **PP2-M5** (testing / `checked_checkpoints` explicit-only 只覆盖两类早退) | **closed** | 读前必看第 8 条把 explicit-only 扩到 `spec_level_undetermined` 并写明「不取已产出值」及其理由 (tasks.md `:24`); TASK-011 有规则 + 可证伪落点 (yaml `:1249-1250`), TASK-005 有逐字断言 (yaml `:1132`), TASK-003 进矩阵 (yaml `:1093`)。我另核了两件计划没说的事: (a) 给 SC-9(4) 钉 `checkpoints: {post_spec: convergence}` **不会消掉触发** —— mode 仍是 adaptive, post_planning / post_implementation 两个未排除且未显式配置的键仍落级 2a, 仍需求 Level, 仍得 `spec_level_undetermined`; (b) 期望值 `['post_spec']` 与 proposal SC-9(2) 第一跑的同名断言 (`:465` 实读「只收级 1 explicit 且值非 off 的键」) 口径一致, 不是新造判据。反事实 (P4 末尾统一装配 ⇒ `[]`) 成立。 |

## 对执笔人自报薄弱点的表态

- **(a) trailer 把归属从路径事实降级为提交者声明 — 可接受。** 方向是 fail-closed, 且我实测 trailer 洗不白 foreign 路径 (foreign 优先于 trailer 判定), 加上 owner_gates 第 2 / 9 项仍要把 `git log` 清单呈给 owner, 伪造需要意图且过不了人这一关。但请注意它没有解决反方向的问题 (本轨自己被判非本轨), 那是 M1。
- **(b) M4 的修复是「记录更新 + 范围限定」不是机制, standards 还会再变旧 — 可接受但要打折。** 断言本身现在限定到「四个文件 + 两个 SHA」且明写「不得沿用本行数值」, 加上 tasks.md 读前必看第 5 条也写了 B.1 重跑, 两处指令足以让执行者做对; 但机制化只差一行 —— 把 standards 补进 TASK-001 的基线复核枚举 (见 PP2-M4 残留)。不加机械守卫我认为可以接受: 这类断言真正的守卫是「执行时实测」, 而不是再造一个会同样变旧的计数器。
- **(c) SC-9(4) 的触发前提是读出来的不是跑出来的 — 可接受。** 被测脚本要到 Phase B 才存在, 这是 TDD RED 的结构性必然, 不是本计划的选择。我按 proposal §1.0 求值总序 + §1.3 优先级链把该格推了一遍 (见 PP2-M5 的 (a)), 触发前提在钉了 fixture 之后仍成立; 且期望值来自 proposal 原文而非实现者现算, 万一推错会在 TASK-005 的 RED 阶段以 AssertionError 显形, 不会假绿。
- **(d) N9 新 fixture 用普通文件冒充 shared 路径, 没复现 gitlink 形态 — 可接受 (已被真数据补上)。** 我用真实的 `1b9734a` (真 gitlink bump) 跑了同一份判据代码, 得 `shared-only`, 与 fixture 结论一致 ⇒ `git diff-tree --name-only` 对 gitlink 输出的就是 `aria` 这一行, `SHARED` 命中。fixture 的缺口在证据层, 不在结论层。
- **(e) 只改了五条 Major 指到的地方, 跨节交叉引用是读着核的 — 部分不可接受。** 我机械核了 33 处引用, 精度很好 (仅 1 处 post-A.2 漂移); 但 M1(i) 恰恰是「新判据 (SHARED 集) 与既有 TASK 交付物清单」的跨节一致性没被机械核对而漏掉的 —— 这正是自报里担心的那一类, 而且它确实发生了。建议把「新增/修改任何路径集后, 对 31 个 TASK 的 deliverables 全量重跑一次分类」做成返修后的固定动作。
- **(f) 一次自造的路径失误 (拼错 scratch 路径) — 可接受, 无实质影响。** 与被审对象无关。

## 对执笔实例六条待裁项的表态 (不作为新发现)

1. `rule6_note.scenario1` 在 A.3 只能是占位, 回填与齐备性断言放 TASK-031 — **可接受**。SOT §4.1 的模板本身允许 `<结果目录>` 形态, 回填点明确, TASK-031 的「无占位尖括号残留」断言是可执行的。
2. `scenario4b: not_required` / `negctrl: n/a` 依赖「description 零改动」、无机械触发器 — **不可接受**, 见 M2: 不是没有触发器的问题, 是现有触发器漏了四份之一。补齐第四份后这条即可接受。
3. M3 的 `Spec:` trailer 是声明不是证明, 替代方案是砍掉 trailer 分支 — **维持 trailer 分支**。砍掉会让 TASK-029 与 TASK-023 这两个纯同步面提交**无路可走** (只能靠 owner 每次裁定), 代价更大; 真正该补的是把本轨工具目录纳入 exclusive (M1)。
4. M3 新增停点 (本轨 5.7 漏写 trailer 停在等待点 16) — **可接受**, 但计划把它写成了唯一停点, 而实测至少还有两个 (M1)。
5. 多条 active claim 选「全部纳入 + 上报」不挑不删 — **可接受且正确**。与 `heartbeat_by_track` 的 all-matching 语义 (`claim_lifecycle.py:491-503` 实读) 一致, 若只取一条, own 集会小于实际心跳面, `coord_ref_precheck` 反而会判 `other` 停下。
6. TASK-030 只改 standards 半句、不碰未裁的 minor — **可接受**。边界切得干净, 未裁 minor 不动符合 Rule #10。

## 风险 / 疑问 (不计入 finding)

1. **R2 未处理的 8 条 minor 里至少一条经复测仍成立**: `CLAUDE.md` 两个版本点实测在 `:138` / `:142`, 计划仍写 `:139` / `:141` (yaml `:1620`)。v2.2 明示这 8 条等 owner 裁, 我不重复报, 只确认它没自愈; TASK-029 已有「行号以执行时 grep 为准」兜底, 执行面无害。
2. **TASK-001 从**本地** `refs/aria/coordination` 解析 claim, 而 `coord_ref_precheck` 只 fetch 到 `FETCH_HEAD`、且只看本地领先**: 本地 ref 若落后 origin, 检查会照常给 `ok`, 解析却读的是旧快照 (已知形态 `10CG/aria-plugin#197`)。我实测当前 local 与 origin 同为 `f121e5d5`, 不可复现, 故不计 finding。建议在解析前加一句「先把本地协调 ref 快进到 origin 再解析」。
3. **`aria` 子模块当前没有 `origin/master` 远程跟踪 ref** (`git -C aria rev-parse origin/master` 报 `Needed a single revision`), 本地在 `master` 分支上。TASK-001 与 TASK-027 第 1 步都先 `fetch origin`, 会把它建出来, 故不构成 finding; 但 TASK-027 第 3 步的断言在没 fetch 成功时会以「解析失败」而非「不相等」的形态失败, 值得在台账里预期到。
4. **c25 第 3 问的前提我复核属实且更精确**: 本仓 `.aria/config.json` 无 `multi_remote` 段 (确认), `phase_c_integrator` 段**存在**但其中**无** `multi_remote_push` 子键 (确认) ⇒ 仍取 `DEFAULTS.json` 缺省, 结论不变。
5. **AB 前置数字全部对得上**: `ab-suite/audit-engine.json` 现为 `version 1.0.0` / `evals [1,2]` (TASK-023 要改成 1.1.0 / 加 id 3), `phase-c-integrator.json` 为 `1.1.0` / `evals [1,2,3]`, `phase-c-integrator-pre-merge-gate.json` **无 `evals` 键** (裁定 9 的前提成立), `version.yaml` 为 `1.5.0` / `32` / `84`, `ls ab-suite/*.json | wc -l` = 32。
6. **归档门预演 (视角第 5 条)**: 我在 `a563192` 副本的 C 态复现 `gate verdict=warn exit=0`, warn 的唯一来源是 `unverified_claims` 那条「活体 dogfood (SC-11) 与 SC-… → dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在」, 与 TASK-031 的预期逐字一致; `d_payload` 非 null, 而 `openspec-archive/SKILL.md:287` 的 Step 7 触发条件逐字是 `gate_result.d_payload != null` 且 `:294` 明写「无论交互模式是否提供 `--ack-unverified`, 本 Step 判定只看 d_payload」⇒ **warn 下 Step 7 确会产生外向动作 (建 tracker issue)**, 计划已登记为 owner_gates 第 11 项并写明「裁不建则只跳过 Step 7」, 登记到位。
7. **命令可执行性抽查全部通过**: `check_bare_issue_refs.py --repo-root=. <file>` 对本目录两个文件均 rc=0 (零命中); `estimator.py --project-root . capture --help` 可用; TASK-024 的 env 判据子进程返回 1 (env 未设, 符合预期); `spec_complete.py --gate <dir>` 可独立调用 (a2 脚本内已实跑)。TASK-027 第 6 步用了 `comm` 加进程替换, 计划已写明「在 bash 下」。

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C / 2M / 4m**

**Vote: REVISE**

## 是否足以开始 Phase B

**不足以 (差两处定点修改)** —— 证据层这一轮很硬 (两份嵌入证据在异容器会话里复跑, `v2_state_runs` 逐字节一致、`a2_state_runs` 在其自述前提 `a563192` 上逐字节一致, 33 处引用仅 1 处已知漂移, R2 五条 Major 有四条实测闭合); 但 M1 会让 TASK-030 的提交范围核验在**一切都做对**的情况下恒红并多出一道 owner 裁定 (我已用计划自己的判据代码在真提交与构造提交上双向实测), M2 让 Rule #6 唯一的合规字段留着一个 fail-open 的洞。两处都是文本级修改 (给 TASK-023 补 trailer 要求或并台账 + 把工具目录纳入 exclusive; TASK-018 的 frontmatter 清单从三份改四份), 不触及任务结构与设计取舍, 改完即可进 B.1 的 owner 门。
