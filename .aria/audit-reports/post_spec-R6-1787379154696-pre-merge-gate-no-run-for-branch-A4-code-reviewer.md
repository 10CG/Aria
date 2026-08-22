---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T09:55:13.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 0
minor_count: 3
---

# post_spec R6 (max_rounds=6 末轮) — A4 code-reviewer 席 (spec↔代码逐行 / 引用稳定性 / 实施者分叉)

审计对象: v6 (R5-fix) `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md`。基线 aria @ `400f0bc` (`git rev-parse` 实核, 工作树干净)。实读/实跑: `pre_merge_gate.py:40-575` 全文 (`DEFAULT_CONFIG :57-69` / `compute_verdict :174-233` / `_build_output :236-275` / `_verify_main_branch_exists :302-352` / `gate_check :387-527` 含全部早退行号 / `main :544-570` `--config-file` 缺省) · `gate_state_helper.py` 全文 (`write_gate_state :115-155` is_first 语义 / `_next_check_at :104-112` / 无 `reset_*` 函数) · `path_coverage.py:1-60` (cwd 契约 `:17`, `_repo_root :105`) · `test_pre_merge_gate.py:44-90` (mixin 默认 stub `_PC_COVERED_STUB` = `workflow-trigger-matched`, 无 `dispatchable_workflows` 键; `:85-89` 旧名打桩) / `:363` · `aether.py:218,225-226` · `workflow-runner/SKILL.md:245-392` (`:249-264/:313/:326/:332-336/:338-358/:345/:389` 逐行) · `workflow-state-schema.md:36-38/:110-112/:123-125/:308-310` · `phase-c-integrator/SKILL.md:241/:248/:250/:252-260/:276-290` · 主仓 `.gitignore:19-21` · 主仓 `.aria/config.json` pre_merge_gate 块 · aria-plugin 仓根**无** `.aria/` 目录 (`ls`) · pytest: phase-c-integrator 119 / gate_state_helper 22 (SC-12 基数属实)。

## 摘要

R5 归我席的 4 条 minor **全部 closed**, 吸收文本与我给的修法逐字等价 (m1 计数 / m2 reset 签名 / m3 占位符字面 + `.format` 理由 / m4 R-e)。v6 13 处 diff 在本席核查面 (§2.1 / §2.3 / §3.1 / §3.2 / SC-5 / SC-13 / R-e 的引用 / 编号 / 行号 / 占位) 无漂移; 全部 SC-7 行号、§2.1 区间、test `:85-89` / `:363`、schema / SKILL 行号对 `400f0bc` 逐一实核一致。发现 **3 条 v6 新引入的 minor** (1 条 SC 文本与 2.3 封闭表互斥 / 1 条旗标缺省未钉 / 1 条 Impact 漏列新函数), 每条一行修法; 两实施者分叉点末次扫描: 仅前两条构成分叉, 都不满足 Major 四门槛 (不造成错误 verdict/kind、不 fail-open、不破坏既有契约; 分叉可见面 = message 里是否多出分支名 / 旗标是否可省)。**vote PASS**。

## R5 处置核对

| 簇# | 状态 | 证据 (实读 v6) |
|---|---|---|
| #3 / A4-R5-m1 (2.3「既有七个」) | **closed** | `:134`「既有六个早退 return 点 (八变体) 键集逐字不变 (SC-7); main 核验那支本就是七键」— 与 §2.1 `:72` / SC-7 `:260` / Impact `:247` 口径统一; SC-7 八处行号 (`:418/:428/:363/:376/:434/:454/:455/:458/:489/:512/:498`) 本轮对源码逐一复核全准 |
| #3 / A4-R5-m2 (reset 签名句) | **closed** | `:152`「`--retry-count` 置 `retry_count=0` **并置 `started_at=now`**, 与 §3.2 exit 2 continue 语义一致 — 具名 helper `reset_retry_count(state)`」+ §3.2 `:173` + SC-11(d) 三处同语义 ✓ (但新具名函数未进 Impact 清单 → 新 m3) |
| #3 / A4-R5-m3 (`{o}/{r}` + `.format` 理由) | **closed** | `:126` 模板字面改 `/repos/<owner>/<repo>/…/dispatches -d '{"ref":"<pr_branch>"}'`; 理由改「占位统一尖括号; 渲染禁用 `str.format` — JSON 体的花括号本就在串内」= 我给的修法; 3.3 (a) `:183`「AI 只填 `<owner>/<repo>`」一致 ✓ |
| #3 / A4-R5-m4 (R-e vs 3d) | **closed** | R-e `:290`「CLI 退出码 2 ⇒ AI surface + 直接 abort (3d 终止分支), 禁回退手写 JSON」= 3d `:168` ✓ |

小计: closed 4 / partial 0 / not_addressed 0。

### 非本席簇的交叉复核 (只记事实)

- 簇 #2 (A2-R5-M1 + A1-m3; 我 R5「还能挑」同题): SC-5 加 (c)(d) ✓ 意图已落, 但 (c) 文本与 2.3 封闭表互斥 → 新 m1 (见下)。
- 簇 #1 (A1-R5-M1): SC-13 改「gate 在 aria-plugin 根执行 + `--state-file` 主仓绝对路径」。实核: aria-plugin 仓根无 `.aria/`, gate `--config-file` 缺省 `.aria/config.json` (`:553-556`) 相对 cwd ⇒ SC-13 下 gate 走 `DEFAULT_CONFIG` (threshold 3); 与 `wait_check_intervals=[5,5,5]` (workflow-runner 读主仓 config 经 `--intervals` 传) 配合, t≈0/5/10 三次观测 ⇒ prompt, 时间轴自洽 ✓。telemetry 派生路径 = `dirname(主仓 state-file)/gate-state-telemetry.jsonl` = 主仓 `.aria/…` = frontmatter partition ✓。
- 簇 #3 / A2-R4-m1/m2 (`record` 文件缺失 + verdict≠wait → exit 2; `reset_retry_count` 具名): `:152` 两条都在 ✓; 与 helper `write_gate_state:131-135` is_first 语义 (retry 0 / started_at=now) 一致, §3.2 步骤 2「is_first ⇒ retry_count=0, obs=1 若带 kind」与之相符 ✓。

## v6 13 处 diff 一致性 (主控点名面)

| 点 | 结论 |
|---|---|
| §2.1 `:72`「第七个早退 return 点 (现六点八变体之外新增一点)」↔ 2.3 `:134` ↔ SC-7 ↔ Impact | **一致** (v5 残留已清) |
| §2.1 伪码 `:77-93` 与源码 `:485-527` 插入位置 / `_build_output` None 不入键 (`:271-274`) / `st` 三值 (`:307`「ok / not-found / verify-failed」) | 一致; `if st != "ok"` 只剩 verify-failed 一支 ✓ |
| 2.3 `:126` 占位三个 (`<owner>/<repo>` / `<basename(file)>` / `<pr_branch>`) ↔ 2.1 末段只回填 `<pr_branch>` ↔ 3.3 (a)「AI 只填 `<owner>/<repo>`」 | 一致 |
| 2.3 `:126` 第三成因「`branches` 过滤」↔ SC-2 trigger-matched 断言 (含 `#152` + matched 名) | 不冲突 (additive 文案) |
| §3.1 `:150` CLI 签名 `--state-file .aria/workflow-state.json` (相对) ↔ §3.2 `:161`「所有调用显式传绝对路径」 | 语义一致, 但**旗标是否有缺省未钉** → m2 |
| §3.1 `:152` `reset` ↔ §3.2 `:173` ↔ SC-11(d) | 一致 |
| §3.1 `:152` `record` 文件缺失 × verdict 分支 ↔ `:151` 骨架条件 ↔ 3d exit 2 → abort | 一致 |
| §3.2 3c' `--state-file <主仓 .aria/workflow-state.json 绝对路径>` ↔ 步骤 2 `<主仓根绝对路径>/.aria/workflow-state.json` | 同义两写法, 可接受 |
| SC-5 (c) ↔ 2.3 封闭表 (`pc=None` 档 / `empty-diff` 档「不带分支名」R3 #6) ↔ mixin 默认 stub (无 `dispatchable_workflows`) ↔ 3.5 删除清单 | **互斥** → m1 |
| SC-5 (d)「核验失败: boom」↔ 2.1 `:87` `f" (PR 分支存在性核验失败: {detail})"` ↔ SC-10 verify-failed 支 | 一致 (子串含) |
| SC-13 ↔ §3.1 `:154` 分区派生 ↔ frontmatter partition ↔ SC-16(c) | 一致 (见簇 #1 交叉复核) |
| R-e ↔ 3d | 一致 |
| Status 行 / `rounds: 5` / owner_rulings | 与 R5 聚合一致 |

## 新 Findings

### 必须改 (全部 Minor, 各一行修法; 建议与 A.2 转 tasks 同一 pass 落)

#### [A4-R6-m1] Minor — SC-5 (c)「**两变体** message 均**含** `feat/x`」与 2.3 封闭表互斥 (v6 新引入)

- 2.3 里**只有** trigger-matched 档的 dispatch 处方行携带 `<pr_branch>` 占位 (`:126`), 且仅当 `DISPATCH_VIABLE and dispatchable_workflows`; `pc=None` 档 (`:130`「远端零 run; 路径覆盖评估已关闭」) 与 `empty-diff` 档 (`:128` 明写「不带分支名, R3 #6」) 都没有分支名槽位; 2.1 末段只做 `.replace("<pr_branch>", …)`, 不另加分支名。
- SC-5 (b) disabled 变体 ⇒ message 恒为「评估已关闭」档 ⇒ **结构上不可能含 `feat/x`**; (a) enabled 变体用 mixin 默认 stub (`_PC_COVERED_STUB`, 无 `dispatchable_workflows`) 也不会渲染 dispatch 行 ⇒ 同样不含。若 TASK-0a 判 `dispatch_viable=false` (3.5 整组删除), **任何**档都不再含 `<pr_branch>`, SC-5 (c) 的「含 `feat/x`」对两变体皆不可满足, 而 3.5 删除清单未列它。
- 分叉形状: 实施者 A 为过 SC 给**所有**档前缀加分支名 (偏离封闭表「要点」与 R3 #6 说明, 但无 SC 禁止); 实施者 B 发现不可满足而收窄测试。两者差异 = message 是否多一段分支名, 不动 verdict / kind / 副本通道 ⇒ 不到 Major (不造成错误行为 / 不 fail-open / 不破坏既有 kind·键集契约; 字面读法是红不是假绿)。
- 修法: SC-5 (c) 改为「**(c1)** 两变体: message **不含**字面 `<pr_branch>` 且 `raw_message == gate_error.message`; **(c2)** (仅 `dispatch_viable=true`) enabled 变体 pc stub 带 `dispatchable_workflows=[".forgejo/workflows/x.yml"]` + `DISPATCH_VIABLE` monkeypatch True → message 含 `feat/x` (回填成功) 且不含 `<pr_branch>`」; 3.5 删除清单追加「SC-5 (c2)」。

#### [A4-R6-m2] Minor — CLI `--state-file` 是否必填未钉; 与 R4 A1-M3 (`--source` 必填, 「忘带旗标 = 红不是假绿」) 同形 (fix-the-class 兄弟位)

- `:161` 自陈危害「helper 默认相对 cwd, 子模块 cwd 下会静默另起 state + 分区」, 然后以「所有 CLI 调用显式传」的纪律兜底; `:150` 签名模板又写着相对路径样例。实施者 A 给 `--state-file` 缺省 `.aria/workflow-state.json` (沿 helper `load_state` 默认), 实施者 B 设必填; 无 SC 区分 (SC-11(d) 必带 `--state-file`)。
- 不到 Major: SKILL 规范面已强制显式传, 只有未来 SKILL 编辑漏旗标时才触发静默分叉; 且后果是 telemetry 落子模块 `.aria/` → 探针 `missing → warn` (不 block 但可见, R-f)。
- 修法: `:150` 改「`--state-file <abs>` **必填, 无缺省** (缺失 exit 2; 理由同 `--source`: 相对 cwd 缺省在子模块 cwd 下静默另起 state)」; SC-11(d) 「缺 `--source` exit 2」旁加「缺 `--state-file` exit 2」。

#### [A4-R6-m3] Minor — Impact `:245` 新函数清单漏 `reset_retry_count`

- v6 `:152` 新增具名 helper `reset_retry_count(state)` (基线 helper 无此函数, 实核), Impact 只列 `reset_no_run_observations`。一 token 补齐。

### 还能挑 (不要求改, 备 A.2 裁量)

- **gate 读 config 的 cwd 契约 vs 新 key 生效面** (既有形状, 非本 spec 引入): gate `--config-file` 缺省 `.aria/config.json` 相对 cwd (`:553-556`), 子模块合并时 cwd = 子模块根 (`path_coverage.py:17` D11), aria-plugin 仓根无 `.aria/` ⇒ 主仓 `config.json` 的 `no_run_prompt_after_observations` 对子模块合并**不生效**, 恒走 `DEFAULT_CONFIG=3`。`path_coverage_enabled` / `enabled` 早已同形; 后果有界 (AD-4: 早/晚一次 prompt)。SC-13 可加一句「gate 在子模块根走 DEFAULT_CONFIG (threshold 3)」免活体时困惑; 根治 (workflow-runner 传 `--config-file <主仓>`) 属 #122 契约另案。
- SC-2「2.3 表 6 档对应的 6 个 reason」措辞 (R5 已记, 未改; reason 集无歧义)。
- Status 行「本版落 2M + 10 minor」为叙述计数, 不核。

## Verdict

**PASS** (0 Critical / 0 Major / 3 Minor) — **vote: PASS**

归我席 R5 4 条 minor 全部逐字吸收; v6 13 处 diff 的引用 / 编号 / 行号 / 占位在本席核查面零漂移 (SC-7 十一处行号、§2.1 五个区间、test `:85-89`/`:363`、helper/schema/SKILL 行号全部对 `400f0bc` 实核)。三条新 minor 都是 v6 定点修改的**邻接未同步** (SC-5 (c) 断言面宽于封闭表 / 旗标缺省未钉 / Impact 漏一函数), 修法各一行, 无一满足 Major 四门槛; 两实施者分叉末次扫描只剩 m1/m2 两处, 可见面均不触 verdict / kind / fail-closed。v6 可批准进 A.2, 三条 minor 随 A.2 转 tasks 同 pass 落。
