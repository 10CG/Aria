---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T13:05:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 0
minor_count: 2
---

## 摘要

R5 (稳定性确认轮, owner 裁 [2] 加 2 轮) 复核 v5 (R4-fix)。实读 aria @ `400f0bc` (基线冻结 SHA, 未变): `pre_merge_gate.py` (`compute_verdict:174-233` 全文重跑一遍红窗验证、`gate_check:409-527` 全文、`_verify_main_branch_exists:301-345`)、`gate_state_helper.py` (`write_gate_state:115-152`、`_utcnow_iso`、docstring 确认 F7 仍成立)、`.gitignore:19-21`、`.aria/config.template.json:73`、`config-loader/SKILL.md:283-287`、`phase-c-integrator/SKILL.md:44-56`+`:288-302`、`skills/state-scanner/scripts/lib/runtime_probe.py`(`validate_descriptor` 全文 + `probe():303-383`)、`skills/state-scanner/scripts/lib/spec_complete.py`(`_find_project_root:754-782`、`_fold_runtime_probe_declaration:1410-1460`)、`skills/openspec-archive/SKILL.md:220-238`、`docs/decisions/DEC-20260731-001-*.md`、主仓与 aria 子模块两份 `.forgejo/workflows/issue-triage-tests.yml`。

## R4 处置核对 (五簇, 全部归属可跨席交叉验证; 逐条实读, 非信任聚合表文字)

| 簇# | 来源 | v5 处置 | 状态 | 证据 |
|---|---|---|---|---|
| 1 | A1-R4-M2 (telemetry 分区根) | 分区路径由 CLI 从 `--state-file` 派生; workflow-runner 恒传主仓路径 | **closed** | 实读 `runtime_probe.py::validate_descriptor` 的 partition 校验 + `spec_complete.py::_find_project_root` 逐字确认: 本 spec `proposal.md` 路径含 `openspec` 段, `_find_project_root` 会返回**主仓根** (`/home/dev/Aria`), 与 frontmatter `partition: .aria/gate-state-telemetry.jsonl` 拼接后落主仓, 不落 aria 子模块。SC-13 的「主仓根执行」进一步验证为**可行**而非仅口头声明: 主仓与 aria 子模块**各自独立**都有 `issue-triage-tests.yml` (`.forgejo/workflows/issue-triage-tests.yml` paths=`aria/skills/issue-triage/**` vs `aria/.forgejo/workflows/issue-triage-tests.yml` paths=`skills/issue-triage/**`) —— SC-13 的复现可以整个发生在主仓 (gate cwd = 主仓、state 文件 = 主仓、ls-remote origin = 主仓), 不需要跨子模块 cwd 切换, 排除了我原先怀疑的「gate cwd 在子模块但 state 文件在主仓」撞车场景 |
| 2 | A1-R4-M3 (`--source` 无缺省) | CLI `record` 的 `--source` 必填, 缺失 exit 2 | **closed** | §3.1 与 SC-11(d) 双处逐字「缺 `--source` exit 2」, 无缺省值描述, 无自相矛盾 |
| 3 | A1-R4-M1 (SC-16 落盘矛盾) | 拆三条 (a 前置可达 / b 红窗 warn / c pass 后机读) | **closed** | 实读 `openspec-archive/SKILL.md:234` 「pass/skipped 两态本身也**不落盘**」逐字属实; 实读 `runtime_probe.py::probe()` 分区文件 missing → `outcome="warn"` (`:366-372`), 印证 SC-16(b) 红窗声明成立 (SC-13 跑之前分区文件确实不存在); `_fold_runtime_probe_declaration` warn → 写入 `unverified_claims[]` (`{claim,reason,symbols}`), 印证「(b) 含本 partition 条目」 |
| 4 | A2-R4-M1 (dispatch 覆盖缺口) | SC-2 加 dispatch 子项 (含 basename 守卫 + 两个负控) | **closed** | SC-2 表最后一句逐字核对: 正控 (`DISPATCH_VIABLE=True`+非空列表 → 含 basename 不含全路径) 与两条负控 (`monkeypatch False` 或列表空 → 不含 `dispatches`) 三态齐全, 与 §2.3 表 `and dispatchable_workflows` 短路语义、§3.5 basename 提取规则逐字吻合, 无遗漏分支 |
| 5 | A4-R4-M1 (passthrough 缺失) | §3.2 两行 CLI 调用补 `--in-flight-runs`/`--raw-message` | **closed** | §3.2 步骤 3c' 与步骤 2 (「同 3c' 全旗标」) 均含两旗标; SC-11(d) 末段「透传到落盘 `gate_state.in_flight_runs`/`raw_message`」断言到位, 与 schema `:123`「wait 态携处方文案」形成闭环 |

**我本席 R4 的 4 条 Minor 逐条重验** (非信任 R4 聚合表「全部吸收」措辞, 逐字比对 v5 正文):

| 我的编号 | 内容 | v5 状态 | 依据 |
|---|---|---|---|
| A3-R4-m1 | TASK-0a 未覆盖 5xx/网络异常 | **closed** | §3.5 现文「4xx/5xx/网络异常 ⇒ false 标 HTTP 码或异常名; R3 #5, R4 A3」逐字采纳我的建议措辞 |
| A3-R4-m2 | `DISPATCH_VIABLE=false` 时 §2.3/§3.3 引用 scope 未回答要不要跟着删 | **closed (实质, 非逐字)** | §3.5 末段现文明确列出「若 false: §4 整段 + SC-8 + SC-9 的 dispatchable 部分 + `DISPATCH_VIABLE` 常量本身 + **2.3 表的 dispatch 渲染句** + SC-2 的 dispatch 子项 + **3.3 (a) 行**, 整组从本 spec 删除」——把我担心的「§2.3/§3.3 两处引用要不要跟着删」显式钉死为「要删」, 用的是删除清单而非我建议的「无需改」措辞, 但两种写法都消除了原有歧义, 问题已解决 |
| A3-R4-m3 | SC-15「真跑一次」未点名 rule6_note 两条行为 (phase-c-integrator surface / workflow-runner should_prompt) 分属两个 skill, 是否各跑一次 | **not_addressed** | 逐字 grep 全文「各跑一次」「两个 skill」「至少各」均无命中; SC-15 与 §6 Phase D 待办第 3 条仍是原文, 未回答「一次是否需覆盖两个 skill」。**R4 聚合报告 (`-aggregated.md` 第 34 行) 的措辞「A3 ×4 …全部吸收 (A3「禁人工模拟 CLI 序列」不采)」在字面上暗示仅 m4 未采、m1-m3 均已采纳, 但本条 (m3) 实际未落地** —— 这是本轮新发现的**聚合表↔正文不一致**, 详见新 Findings m-B |
| A3-R4-m4 | SC-13 未排除人工模拟 CLI 序列 | **not_addressed (owner 知情, 低优先级)** | 与聚合表口径一致 (「A3「禁人工模拟 CLI 序列」不采, 低优先级」), 属已披露的取舍, 非新问题 |

## 核心正确性主张复验 (v5 新增/改写 SC, 逐条按「怎么会红」)

- `compute_verdict([], "not_found", cfg=None, path_coverage=pc)`: 重新在 `:174-233` 逐行走查, `not_found` 既不匹配 `("failing","error")`、不匹配 `"pending"`、不匹配 `"not_applicable"`, `main_in_flight_runs=[]` 为假 → 落 `else: verdict = VERDICT_GREEN` (`:222-224` fallthrough)。SC-2 红窗声明（基线 green, 应 wait）**成立不变**。
- SC-2「6 个 reason + None」计数复核: 6 = `workflow-trigger-matched`/`workflow-files-changed`/`empty-diff`/`git-diff-failed`/`workflow-parse-failed`/`internal-error` 六个真实 reason 字符串 (§2.3 表把后三者合并成一行展示, 不代表只有 1 个 reason); `+ None` = 第 7 个参数化用例 (`path_coverage=None` 整体, 对应 `path_coverage_enabled=false` 分支); `not_applicable` 的两个 reason 显式声明由 SC-6 覆盖、不进 SC-2 参数化列表。三层计数彼此不矛盾, 非新引入的歧义。
- SC-11(d) 全链路 (状态文件不存在起步 → 两次 record → 独立重读 → threshold/should_prompt → reset --observations → reset --retry-count → 缺失文件 exit 2 → 缺 --source exit 2 → passthrough → telemetry ts) 对照 `write_gate_state:115-152` 实际实现的 `is_first` 判定 (`not existing or existing.get("name") != name`) 与「整块重建无 `**existing` 展开」的事实——**验证了 spec 的警示是真实陷阱**: 若实现漏抄 `no_run_observations` 一行进新字典字面量, 该键会被静默吃掉, SC-11(a)/(d) 的独立重读断言会抓到, 不是无的放矢的检查点。
- SC-13「主仓根」经与两份 workflow 文件 (`.forgejo/workflows/issue-triage-tests.yml` 主仓版 vs 子模块版) 交叉核实, 复现路径落在主仓侧确实自洽可行, 不存在「gate 用子模块 cwd 而 state 文件用主仓路径」的隐性撞车 (原本我方向上担心的一种解读, 现证伪: 不需要那样)。
- SC-16 三条与 `openspec-archive/SKILL.md:234`、`runtime_probe.py::probe()` 的 `missing → warn`、`_fold_runtime_probe_declaration` 的 warn→unverified_claims 双写机制逐一对应, 无「测的东西根本不存在」的空判定 (呼应 memory `verify_predicate_inputs_exist`)。

未发现 v4→v5 diff 在这四个重点区域引入新的假绿、fail-open 或契约破坏。

## 新 Findings

### [A3-R5-m1] Minor — SC-15/rule6_note 未强制「两个 skill 各至少一次」证据覆盖 (延续自我 R4-m3, 未被 v5 采纳)

同上表; 不满足 Major 门槛 (不产生错误 merge 行为、不 fail-open、不破坏契约, 只影响 Rule #6 判据表第三行的证据完整度), 建议 Phase B/D 落地时按我 R4 原建议补一句, 不建议为此再开一轮。

### [A3-R5-m2] Minor — R4 聚合报告disposition措辞「全部吸收」与 v5 正文存在一处不完全对应 (审计流程自身的准确性问题)

**问题**: `post_spec-R4-…-aggregated.md` 第 34 行写「A3 ×4 …全部吸收 (A3「禁人工模拟 CLI 序列」不采, 低优先级)」, 字面读法是「4 条里仅 1 条 (人工模拟 CLI 序列, 即 m4) 未采, 其余 3 条均已采纳」。但逐字核对 v5 正文, m3 (SC-15 两 skill 证据覆盖度) 同样未见对应文字改动 —— 实际是「4 条里 2 条未采」, 聚合表的归纳比实情更乐观一档。

**为何是 Minor 非 Major**: 这不影响 v5 本身的正确性或 verdict (m3 本就该降级为 Minor, 不阻塞), 纯粹是审计报告链自身的可追溯性问题——若未来有人只读聚合表不逐字核对正文, 会误以为 m3 已被处理。

**建议**: 无需为此改 v5 或重开一轮; 建议以后聚合表在「全部吸收」类归纳前, 对每条来源 minor 逐一标注 adopted/not_adopted (而非用一句话+一个例外概括), 降低「聚合表≠正文」的漂移概率 (同 memory `feedback_own_past_summary_is_not_a_measurement` 的形状: 摘要性归纳需要被源头验证, 而不是被信任传递)。

## 稳定性核验结论

- v4→v5 的 5 个 Major 簇处置 (对照聚合表 + 我本席 4 条 Minor) 经**独立实读代码/文档源**逐条复核, 全部 5 Major 簇 **closed**, 证据真实存在于 baseline `400f0bc` 或 v5 正文, 非纸面自证。
- 我本席 4 条 Minor: 1 条 (5xx) 逐字采纳, 1 条 (DISPATCH_VIABLE scope) 实质采纳 (措辞不同但消歧目标达成), 2 条 (两 skill 证据覆盖 / 人工模拟排除) 未采纳但均已知情 (其中 1 条聚合表归纳略有失真, 已作为新 Finding 记录)。两条未采纳项严重度仍为 Minor, 不改变 verdict。
- 未发现 v5 新引入的假绿、不可证伪断言、或与既有 Major 门槛 (错误行为/fail-open/契约破坏/两实施者必然分叉且无 SC 区分) 相符的新问题。

## Verdict

PASS (0 Critical, 0 Major, 2 Minor) — v5 相对 v4 的全部 5 个 Major 簇处置经实读验证真实 closed, 核心正确性主张 (SC-2/SC-4/SC-7 红窗声明、SC-13 主仓根可行性、SC-16 三段式判据) 在 baseline 代码上逐条重新走查仍然成立, 无新引入的假绿或矛盾。残余 2 条 Minor (证据覆盖度 + 一处聚合报告归纳偏乐观) 均不满足末轮 Major 门槛, 不阻塞。v5 可批准进 A.2。

vote: PASS
