---
checkpoint: post_planning
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-24T13:08:52.129Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R7 — code-reviewer 席 (10CG/Aria#199 A.2/A.3 v2.6, 主仓 `9a3ac24`)

## 已实读文件

派单 sha256[:16] = 566f5f40250c7425

被审对象 (主仓当前工作树 `9a3ac24`):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` — 全文 245 行
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` — 全文 2067 行; 另按结构遍历出 812 个字符串单元 (live 769 / revision_log 43) 做机械扫描
- `git diff e7a1782 320d523` 三文件全部 hunk (tasks.md 1 + 5 个 hunk; gen_yaml.py 17 个 hunk; 逐 hunk 独立复算, 见「独立复算 vs 执笔自报的差异」)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` — 按需读 (Level 2 输出口径与内联 Tasks 相关段)
- `.aria/audit-reports/post_planning-R6-...-aggregated.md` — Minor / Conflicted / 流程记录 / R5 对账 四节
- `docs/handoff/2026-09-18-199-a2-a3-c1-verify-v21-rework-r2.md` —「v2.6 返修」与「执笔实例提请裁定 (两条, v2.6)」两节 (**独立复算全部完成后才读**)

源码与配置 (aria 子模块 `1cb3872`; 主仓当前):

- `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` — `:96` `:101` `:128` `:152-157` `:255-305` 与 Summary 段全文
- `aria/skills/state-scanner/scripts/collectors/custom_checks.py` — 文档头 `:20-40` 与判定行 `:377`
- `.aria/state-checks.yaml` — 16 条 check 的 name / enabled / command 全量
- `.aria/probes/plugin-cache-currency.py` / `config-template-key-currency.py` / `forgejo-app-token-liveness.py` — SKIP 分支
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` `:273` `:733-744` `:924` `:1642`
- `aria/skills/state-scanner/SKILL.md` `:182` `:191`; `aria/skills/state-scanner/lib/constants.py` `:58`
- `aria/skills/phase-c-integrator/SKILL.md` `:57` `:132` `:200` `:497` `:511-512` `:754`; `aria/skills/audit-engine/SKILL.md` `:423`
- `aria/skills/openspec-archive/SKILL.md` — Step 1 / Step 2 / Step 7 触发与幂等段
- `aria/skills/session-closer/scripts/handoff_autofill.py` `:391-412` `:455-470`; `aria/skills/phase-d-closer/references/execution-steps.md` `:106`
- `standards/openspec/project.md` `:117`; `standards/openspec/templates/proposal-minimal.md` `:26-34`
- 生效 `skill-creator` 的 `SKILL.md` (`~/.claude/plugins/.../skills/skill-creator/SKILL.md`) `:167` `:186`
- 主仓版本点 16 处 (README 四份 / CLAUDE.md / VERSION / 两份 architecture) 与 `aria/VERSION` `:7-8` / `aria/CHANGELOG.md` `:104` `:200` `:3136`
- `CLAUDE.md` — 多远程两条硬约束与不可协商规则 3 / 6 / 8 / 10

实跑 (全部在 `scratch/audit-R7-code-reviewer/` 下, 两份共享副本先 `cp -a` 到本席目录; 真仓只做 `git ls-remote` / 读):

- `a2_state_runs.py` 与 `a2_v2_checks.py` 全文取自 yaml 的 `script` 键, 按各自 `command` 重跑 (两份三态证据)
- 六条 custom checks 在两个工作目录各跑一遍; `plugin-cache-currency.py` 在空目录跑
- `grep -cxF` 取值断言的四态反事实 (正确 / 多一个字母 / CRLF / 行尾空格), GNU grep 与 Claude Code 的 ugrep 包装各跑一次
- `submodule_gate.sh` 在副本主仓根实跑; `handoff_autofill.py --owner-container` 实跑
- 三族同族扫描独立复算 (序号引用 / 协调 ref 写入路径 / custom checks 哨兵形态)
- 真仓两个远端 `git ls-remote master`

## R6 对账

| R6 键 | 判定 | 本席亲验证据 |
|---|---|---|
| `354faf33` (已知项 A) | **closed** | (1) 不可达句已删: `TASK-031` 起稿条现写「本任务自身不跑该判据 (调用点只有 TASK-001 与 TASK-030)…v2.6 删去 v2.5 原写的那个停点 (在 5.9 不可达)」; 我独立核实该前提成立 —— `TASK-031` 的 15 条 verification 里最后一条 (推送条) 只有 `git push origin master` 与 `git push github master` 加逐 remote `ls-remote`, 没有 `commit_attribution` 调用, 全 yaml 的该判据调用点确为 TASK-001 / TASK-030 两处。(2) 新断言已落地并可证伪: 我自建四份 frontmatter fixture 实跑 —— 正确值 `E1=5 / 值非空=5 / grep -cxF=1`; 多写一个字母 `E1=5 / 值非空=5 / grep -cxF=0`; 行尾多一个空格同样 `0`。即「只有逐字比对拦得住」为真。(3) `commit_attribution.cannot_catch` 与 tasks.md 5.9 行、判断清单第 33 条均已同步 |
| `6ad0a84b` (序号引用) | **closed** (带观察, 见 m3) | 10 处锚点改写全部落地, 且我逐个验证新锚点在目标任务里唯一可解析: `TASK-024` 的「结束后先取第二次快照」条 = 第 12 条 (唯一头匹配); `TASK-023` 的「开 AB 会话之前」条 = 第 5 条 (唯一); `TASK-025` 的「并入上游」条 = 第 1 条 (唯一); `TASK-021` 的「SC-12 三条」那一条 = 第 2 条 (唯一); `TASK-029` 两条锚点各唯一; `TASK-001` 的「claim 身份条」有两条头匹配 (第 2 / 3 条), 由计划自加的括注「(三元组运行时解析那一条)」消歧 —— 这一步做对了。我另按 `TASK-0NN 第 K 条` 模式重扫活文本, 逐条解析后**全部指对** |
| `2c2e8931` (强制对齐通则) | **closed** (带残余, 见 m1) | `hard_constraints` 第 4 条已升为通则; `TASK-001` 心跳条与重新认领段、`TASK-031` 的 release 条、tasks.md 1.1 / 5.9 两行、判断清单第 27 / 48 条、等待点表前说明全部带对齐。`coord_ref_precheck.code` 的用法注释已由「可推送 / 可强制对齐」改为「可强制对齐; 对齐后才可推送」。证据 N12 我在自己环境独立复跑, 与 yaml 的 `output` **逐字节一致**: 分叉态直接 release 得 `exit=0 fetch_success=False released.success=True push_success=False remote_equals_local=False`, 其后前置检查 `exit=1`; 先对齐再 release 得 `push_success=True remote_equals_local=True` |
| `749f8d15` (C.2.4.5 override) | **closed** | 源码逐行核实: `submodule_gate.sh:101` 确为 `msg=$(git log -1 --format=%B HEAD …)`; `:263` 打 `GATE:`; `:297` 打 `ALLOW: $SUB $VERDICT overridden by per-PR marker (audit logged)` 后 `continue` 且不置 `exit_code`; Summary 段在 `exit_code==0 且 affected_count>0` 时打「flagged but allowed」并 `exit 0` —— 计划新写的放行判据 (退出 0 + 被 override 子模块有 `GATE:` 与其后 `ALLOW:` 行, 其余照旧) 与脚本行为逐项对得上。`check_pr_label` 从 `git remote get-url origin` 反推仓名的正则 `/([^/]+)/([^/]+)\.git$ ` 对本仓 `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` 能解析出 `10CG/Aria`, `forgejo` CLI 在 PATH 上 —— 标签一路在本机结构上可达。我另在副本主仓根实跑闸: 三行 `OK: <sub> unchanged (<sha>)` + 摘要行 + `exit 0`, 与计划描述的结论行形状一致 |
| `29325b2c` (custom checks 首行) | **closed** (带口径残余, 见 m2) | `custom_checks.py:377` 逐字为 `status = "skip" if first_line.lstrip().startswith(SKIP_MARKER) else "pass"` (仅 rc==0 分支), 与计划所述映射一致; `.aria/state-checks.yaml` 第 16 条 `plugin-version-arch-docs-match` 的 command 第二行确为 `[ -z "$PLUGIN" ] && { echo "##SKIP## …"; exit 0; }`。我独立实跑六条: 主仓根 `OK / OK / OK / OK / 无输出 / OK` 且退出码全 0; 换到 `aria/skills/audit-engine/tests` 起跑, `plugin-version-arch-docs-match` 变 `##SKIP## …` 且仍 `rc=0`, `no-unresolved-version-placeholder` 仍无输出且 `rc=0`, 其余四条 `rc=1` 或 `2` —— 与计划登记的实测值逐值相同 |

**三族机器清单的独立复算**: 我按自己的词表重扫, 三族的**结论**都与执笔一致 (没有会让执行者走错的残余), 但两族的**计数口径**与执笔/主控所报不同, 见 m2 / m3 与「独立复算 vs 执笔自报的差异」。

## Findings

无 critical, 无 major。以下 5 条 minor 均不改变执行者会做什么, 按派单口径封顶 minor。

### Minor

**m1 · `ce6f31fc`** — severity: minor | type: issue | category: documentation | scope: `detailed-tasks.yaml metadata.hard_constraints[2] / owner_gates[14]`

- **summary**: v2.6 把「写协调 ref 前先强制对齐」升为通则, 但同一份 SOT 里两条**授权口径**仍只写「前置检查退出 0」这一半前提, 与 tasks.md 已同步的同一句不一致。
- **证据** (实读当前 yaml):
  - `hard_constraints[2]` (第 3 条): 「…适用前提 = 推送前 metadata.coord_ref_precheck 退出 0 (本地协调 ref 领先 origin 的只有本轨心跳), 不满足 ⇒ 心跳加 --no-push 并停下请授权 (第 15 项)。」— 无对齐。
  - `owner_gates[14]` (第 14 项): 「…用原串 … 重新认领 (…), **认领前 metadata.coord_ref_precheck 退出 0**; 未授权 ⇒ …」— 无对齐。
  - 对照 tasks.md 等待点表前说明 (v2.6 已改): 「前提是推送前协调 ref 前置检查通过**并已强制对齐到 origin** (v2.6, 见判断清单第 48 条)」。
  - 对照 `hard_constraints[3]` (第 4 条, v2.6 通则) 与 `TASK-001` 重新认领段: 两处都明写先 `git fetch origin +refs/aria/coordination:refs/aria/coordination`。
- **失败场景**: 执行者在 Phase B–D 某个会话只按「外向动作以 `metadata.owner_gates` 为准」翻到第 14 项, 读到「认领前 precheck 退出 0」即认领 —— 在 N12 已实测的分叉态下写得进本地、推不出去 (`push_success=false`), 下一个会话卡在第 15 项。之所以只是 minor: 第 4 条通则与 TASK-001 的执行条都无歧义地要求对齐, 执行者的操作面是任务条而非闸表, 且 `coord_push_verify` 会当场抓到 `push_success=false`。
- **建议修法**: 在这两条各补一句「(退出 0 之后、动手写或推之前还须按第 4 条强制对齐并重解析)」。不改任何判据值。

**m2 · `76949787`** — severity: minor | type: issue | category: documentation | scope: `detailed-tasks.yaml metadata.revision_log v2.6 29325b2c`

- **summary**: 「16 条 custom checks 逐条静态看哨兵串与『`##SKIP##` 配退出 0』形态 (**只有这一条有**)」这句闭合声明, 只对 yaml 的 command 字面为真; 按行为看, 计划点名复跑的六条里 `plugin-cache-currency` 今天就有同一形态。
- **证据** (我实跑): 在空目录跑 `python3 .aria/probes/plugin-cache-currency.py` 得首行 `##SKIP## SOT 缺失/不可解析 (aria/.claude-plugin/plugin.json) — 非 Aria meta-repo 布局, 判据不适用`, `rc=0`。该探针 `:34` 定义 `SKIP_MARKER = "##SKIP##"`, `:43` 打印它。同族还有 `config-template-key-currency.py` (`:30` 起四处 SKIP 分支)、`forgejo-app-token-liveness.py` (`:94` `:105` `:148`)、`issue_cache_freshness_probe.py`、`linked_issue_field_probe.py` —— 共 5 条 check 的被调脚本会打该哨兵, 不是一条。
- **失败场景**: 不会让执行者做错 —— 计划的操作口径是 blanket 的 (`hard_constraints` 第 14 条 (3):「custom checks 一律以输出首行判…首行为 `##SKIP##` 或无输出…都算没跑成」), 对 `plugin-cache-currency` 打 `##SKIP##` 同样 fail-closed。受影响的是**闭合声明的可信度**: owner 按「只有这一条有」判该族已扫尽, 而事实是「只有这一条把哨兵写在 yaml 里」。
- **建议修法**: 把括注改成「只有这一条把哨兵写在 `state-checks.yaml` 的 command 字面里; 另有 5 条的被调探针会在脚本内打同一哨兵 (已被本条的首行通则覆盖)」。

**m3 · `bdce52c6`** — severity: minor | type: issue | category: documentation | scope: `tasks.md 判断清单第 47 条`

- **summary**: 「条目序号引用**一律**改锚点式」是全称句, 实际做法是「改掉实测指错的 10 处, 指对的保留」; 活文本里仍留有十余处位置式引用 (我逐处核过, 当前全部指对)。
- **证据** (我按 `TASK-0NN 第 K 条` 与相对词两套模式重扫 tasks.md 全文 + yaml live 树, 排除 `revision_log`):
  - 位置式且带任务号的: `TASK-025 第一条` (在 `TASK-023` 第 5 条内) → 解析到 `TASK-025` 第 1 条「并入上游」✅; `TASK-021 第 2 条` / `第 3 条` (在 `TASK-027` 内) → ✅; `TASK-030 第 1 条` (在 `TASK-029` 内) → ✅。
  - 相对词: `TASK-031` 第 2 条的「末条 Phase D 提交」(当前 15 条, 末条确为推送条 ✅, 但一旦增删即腐坏)、`TASK-031` 第 15 条「上一条的 latest.md 提交」✅、`TASK-030` 第 5 条「上一条的 C.2.4 green」✅、`TASK-021` 第 2/3 条互指 ✅、`TASK-011` 第 5 条「上一条的可证伪落点」✅、`TASK-001` 第 4 条「参数 = 上一步解析出的本轨 claim 文件」(相邻上一条是「claim 身份的实测锚」, 按「条」读差一, 按「步骤」读正确 —— 两义可解, 不计入错)。
- **失败场景**: 不改执行。风险是下一轮返修者读到「一律改锚点式」, 以为该族已无位置式引用而不再扫, 于是新插条目时再次静默腐坏 —— 这正是本 minor 立项的原因。
- **建议修法**: 把第 47 条的全称句改成「本轮把实测指错的 10 处改为锚点式; 其余位置式引用经逐处核实当前指对, 保留, 但**增删条目时须整族重扫**」。

**m4 · `6be9db6a`** — severity: minor | type: issue | category: testing | scope: `detailed-tasks.yaml TASK-029 custom checks`

- **summary**: v2.6 新写的验收句「前四条…**首行须为 OK**」按字面是全等比较, 而这四条通过时的首行都带后缀, 全等恒不成立。
- **证据** (我实跑, 主仓根): `m6-version-badge-match` → `OK badge=1.73.3`; `i18n-readme-translation-currency` → `OK (3 i18n READMEs current @ 1.73.3)`; `plugin-version-arch-docs-match` → `OK plugin=1.73.3 (2 arch doc rows match)`; `main-project-version-consistency` → `OK 主项目版本 1.7.5 — 9 个引用点全部一致`。同一条目下半句登记的实测值也写作 `OK / OK / OK / OK / 无输出 / OK`, 同样是简写。
- **失败场景**: 执行者按字面做全等比较 ⇒ 四条通过的 check 被判不通过 ⇒ 在 5.7 多停一次 (方向 fail-closed, 不会放行坏态, 且看一眼输出即可自解)。
- **建议修法**: 改为「首行**以** `OK` **开头**」。与工具语义也一致 —— `custom_checks.py:377` 判 skip 用的就是 `startswith`。

**m5 · `3de4b245`** — severity: minor | type: issue | category: architecture | scope: `detailed-tasks.yaml TASK-030 / owner_gates 第 17 项`

- **summary**: 计划向 owner 推荐 override 走 PR 标签 (「两者相权, 先请 owner 考虑标签」), 但没写出标签这一路的一个代价: 标签**不按子模块分**, 一旦打上就对本 PR 的**每一个**受影响子模块生效。
- **证据** (源码): `submodule_gate.sh:152-157` 的 `check_override()` 先按子模块校 trailer (`check_override_trailer "$1" "$2" "$3"`, 内部 `[[ "$trailer_sub" != "$sub" ]] && continue` 并解析新旧 SHA), 失败则退到 `check_pr_label "submodule-rollback-approved"` —— 该函数的**唯一参数是标签名**, 不接子模块, 命中即对当前子模块返回 0。即 trailer 是「按子模块 + 按 SHA」授权, 标签是「整 PR」授权。
- **失败场景**: owner 为放行 `aria` 的一次回退而打标签, 若同一 PR 里 `standards` 或 `aria-orchestrator` 也被判 regression/divergent, 它们会一并被 `ALLOW` 掉。之所以只是 minor: 计划自己的放行判据把这一点堵住了 —— 它要求「被 override 的子模块有 `GATE:` + `ALLOW:`, **其余子模块**是 `OK: … unchanged` 或 `GATE:`+`PASS: … forward bump`」, 第二个子模块若拿到 `ALLOW:` 就不满足「照上句」, 会停在第 17 项。这是一条本轮值得表扬的逐子模块判据。
- **建议修法**: 在第 17 项与 TASK-030 该条的标签那一路补一句「标签按 PR 生效、不按子模块分; 本计划的逐子模块放行判据会拦住被顺带放行的其它子模块」。这条正好回答执笔实例请裁第 1 条 (标签要不要固化为默认路径)。

## 独立复算 vs 执笔自报的差异

**流程说明 (必须先声明)**: 派单要求「先不读 yaml `revision_log` 的 v2.6 六条」, 但又要求「逐 hunk 独立复算 `git diff e7a1782 320d523`」, 而 `revision_log` 的 v2.6 六条正落在该 diff 的**最后一个 hunk** (`@@ -943,16 +944,22 @@`) 里; 派单末尾的「六条自报薄弱点」同样落在派单原件内, 而派单要求第一步完整读原件。我的处理: 先把三文件全部实质 hunk (tasks.md 全部 + gen_yaml.py 前 16 个 hunk, 含 TASK-001 / 024 / 029 / 030 / 031 与 `hard_constraints` / `owner_gates` 的改动) 读完并形成判断, 最后才碰到 `revision_log` 那一 hunk; 轨级 handoff 的两节是全部实跑与扫描做完之后才读的。下面每一条差异都以**我自己的实跑或实读**为据, 不以自述为据。

1. **「活文本里条目序号引用只剩两处, 逐条核实均指对」(主控核验) vs 我扫到十余处**。我用两套模式重扫 (tasks.md 全文 + yaml live 树 769 个字符串单元): 带任务号的位置式引用 4 处 (`TASK-025 第一条` / `TASK-021 第 2 条` / `TASK-021 第 3 条` / `TASK-030 第 1 条`), 相对词引用 9 处 (`上一条` 6 / `下一条` 2 / `末条` 1), 另有 `第 N 步` 类 6 处 (指向 TASK-027 自带编号的步骤, 稳定)。**结论一致** (逐条解析后无一指错), **计数不一致** —— 差在扫描面: 中文数字「第一条」、同任务内的相对词、任务外指向带编号步骤的引用, 按更窄的模式都不计。这支撑 m3: 报「只剩两处」会让下一轮低估该族的存量。
2. **「custom checks…(只有这一条有)」vs 我实测 5 条探针会打同一哨兵**。执笔自报薄弱点第 (4) 条把这件事写成**将来**的风险 (「若将来某条把 `##SKIP##` 打到 stderr 或第二行就会漏」), 而我在空目录实跑 `plugin-cache-currency.py` 当场得到 `##SKIP##` + `rc=0` —— 它是**现在时**, 且正是计划点名复跑的六条之一。操作口径覆盖得住, 所以只是 m2 的闭合声明问题, 但风险的时态判错了。
3. **「调用 `phase1_gate` / `release_gate` 的四处全部带对齐或豁免说明」vs 我另找到两条只带半个前提的规则条**。四个**执行落点**我复核后同意 (TASK-001 心跳 / TASK-001 重新认领 / TASK-024 AB 豁免 / TASK-031 release)。但 `hard_constraints[2]` 与 `owner_gates[14]` 这两条被归类为「授权条」而未同步 —— 它们**已经承载了半个操作前提**(「推送前 precheck 退出 0」), 所以不是纯授权条。这是 m1。
4. **「三态证据独立复跑逐字节一致」—— 我在自己的环境独立复现了这个结论**。把 yaml 的 `a2_state_runs.script` 与 `v2_state_runs.script` 原样落盘, 用各自 `command` 对我自己 `cp -a` 的 `state-base` 副本重跑: `diff` 对 `output` 两份均 `rc=0` (零差异), 脚本 `rc=0` 且 stderr 为空。N12 的两种顺序、N6 的分叉态、N11 的 sweep 态全部复现。**这一条是吻合, 不是差异**, 但因为它是本轮最重的证据面, 明确记下。
5. **执笔自报薄弱点第 (3) 条「PR 标签一路没有实跑」—— 我把它往前推了一步**。没实跑我接受 (要真 PR 号与真标签), 但我用源码把两件事钉死了: 标签一路在本机**结构上可达** (`check_pr_label` 的仓名反推正则能吃下本仓的 ssh origin URL, `forgejo` CLI 在 PATH 上, TASK-030 的调用已带 `ARIA_PR_NUMBER`); 同时标签**不按子模块分** —— 这是自述没提的一个代价, 见 m5。
6. **一处上游矛盾, 计划处理得对, 值得记**: `submodule_gate.sh` 自己在 BLOCK 时打印的指引是「add commit trailer … **to merge commit message**」(`:~498` 附近), `SKILL.md:511-512` 的示例同样以合并提交为背景。计划的第 17 项反过来告诉 owner「写进 Forgejo 合并提交的 trailer 闸看不见, 须落在 PR head 那个提交上」—— 即计划明知会把工具的原样输出呈给 owner, 仍在闸表里写下与工具指引相反的正确结论。这是 v2.6 这一条最实的价值。

## 对执笔人自报薄弱点的表态

1. **track-id 断言只守文件内容、不守提交归属** — **可接受**: 我实读 `TASK-031` 最后一条确认 Phase D 提交的推送路径上确实没有 `commit_attribution`, 所以「不可达」是事实而非托辞; 新断言经我四态反事实实测确实是这一面唯一拦得住的守卫, 剩下的提交归属面交第 13b 项的人工 diff 关, 与本计划一贯的 fail-closed 取向一致。
2. **对齐通则只枚举了两处例外** — **可接受**: 两处例外 (AB 会话 / release 之后) 都写明了为什么不适用, 且 N6 已实测「本地领先的只有本轨心跳」是对齐的前提条件, 将来新增窗口时冲突是可发现的, 不是静默的。
3. **PR 标签一路没有实跑** — **可接受, 但要补一句代价**: 只按代码断言在这里够用 (方向 fail-closed, 失败就是挡住), 我另用源码确认了这条路在本机结构上可达; 不接受的只是「推荐它时没写出它不按子模块分」这一点, 已立 m5。
4. **custom checks 首行口径依赖现有 16 条的实际形态** — **可接受, 但时态写错了**: 依赖现状这件事本身无可厚非 (操作口径是 blanket 的, 新形态一样按「没跑成」处理); 但它被写成将来时, 而 `plugin-cache-currency` 现在就是这个形态, 见 m2。
5. **序号引用清单里 38 行是人工判定** — **可接受**: 我用另一套词表独立重扫, 逐条解析后与人工判定同向 (无一指错), 属于可复核的人工判定, 不是不可证伪的声称。
6. **N12 的 fixture 用 `update-ref` 拨回 release 之前** — **可接受**: 这恰是做对照该有的做法 —— 两种顺序跑在**同一个**分叉态上, 否则两臂不可比; 脚本里 `saved` 在 release 之前取、之后原样拨回再 `fetch` 对齐, 我复跑得到逐字节相同的输出, 说明该构造稳定。生产不会「同一状态两次 release」这句也对。

## 风险 / 疑问 (不计入 finding)

1. **执行者的 `grep` 可能不是 GNU grep**。本计划新增的 `head -8 <handoff> | grep -cxF 'track-id: …'` 在 GNU grep 下四态表现与计划所写完全一致 (含「行尾带 CR 时得 0, 方向 fail-closed」); 但 Claude Code 的 Bash 里 `grep` 是 ugrep 包装函数, 我实测它对 CRLF 那一态返回 **1** (即放行)。主用途 (拦住写错的 track-id 值) 两种 grep 都正确, 且 `docs/handoff/*.md` 结构上不是 CRLF 文件 (`crlf_guard` 点名的 CRLF 文件只有两份 aria SKILL.md), 所以不立 finding。同源风险: 该包装还带 `--ignore-files` (认 `.gitignore`), 与判断清单第 44 条赖以论证的「`grep -r` 不认 `.gitignore`」前提相反 —— 但第 44 条选的 (a) 在两种 grep 下都安全, 结论不受影响。执行期若想稳妥, 可在这几条判据里写 `command grep` 或 `/usr/bin/grep`。
2. **`CLAUDE.md` 的两个版本点行号已漂**。`TASK-029` 记的是 `:139 / :141`, 当前实为 `:138` (`v1.52.0–v1.73.3 已 ship`) 与 `:142` (`版本: aria-plugin v1.73.3 …`)。同条目已写明「行号以执行时 `grep -n` 为准」, 且**处数**与总数我都复核过: 四份 README 2+3+3+3、CLAUDE.md 2、`VERSION:24` 1、两份 architecture 各 1 = 16, 与「16 个版本点」和「九个版本同步面文件」逐项对得上。故只记风险, 不立 finding (`CLAUDE.md` 项目状态段是高频改写面)。
3. **判断清单第 47 条的归纳措辞容易误读**。它写「两处『TASK-023 末条』实为**并入上游**那条」, 而实际落地的锚点是「`TASK-023` 的『开 AB 会话之前』条」; 巧的是「并入上游」正好是 `TASK-025` 第 1 条的字面开头。两者其实指同一条 (TASK-023 第 5 条的内容就是把上游并入 feature), 但 owner 复议时可能读成指向 TASK-025。建议下次改写时用落地锚点的原词。
4. **轨级 handoff 的第八批推送状态已过时**。该文写「第八批…**待授权推送**」, 而我对真仓两个远端各跑 `git ls-remote master` 均得 `9a3ac24` = 本地 HEAD, 即已推。handoff 不在本次审计对象内, 仅记。
5. **`TASK-001` 重新认领段在「对齐」与「认领」之间没有再解析一次**。`hard_constraints` 第 4 条通则说「对齐后重跑三元组解析」, 而该段写的是 precheck → 对齐 → 认领 → 认领后再解析。若对齐后 origin 上已出现本轨 active claim, 会多写一条 claim (已知缺陷 `10CG/aria-plugin#202` 的形态, 计划的「2 条及以上 active」分流已登记如何处置, 且认领本身是 owner 授权动作)。窗口窄、后果已被兜住, 不立 finding; 若返修 m1 时顺手把这半句补上最省事。

## Verdict

**verdict: PASS** — counts: **0C / 0M / 5m**

**Vote: PASS**

依据: 本轮按与前六轮同一口径逐项复算, 无 critical、无 major。R6 五条 minor 全部 closed, 每条我都有亲验证据 (源码逐行、四态反事实、六条 check 双目录实跑、闸实跑、两份三态脚本在我自己环境逐字节复现)。5 条 minor 全部落在「措辞 / 闭合声明 / 未写出的代价」上, 没有一条改变执行者会做什么; 其中 m1 / m2 / m3 是三族同族扫描的口径残余, m4 是一处字面歧义 (fail-closed), m5 是一条应当告诉 owner 的代价。本席不因「这是最后一轮」而放宽或收紧任何一条的定级。

## 是否足以开始 Phase B

**足以**。计划的执行面已经可以照字面走通: 三态证据在第三方环境可重现, 验收判据可证伪, 外向动作与 owner 等待点 (1–12 / 13a / 13b / 14–17) 齐备且 fail-closed, 本轮 5 条 minor 都可以在 B.1 起跑前顺手改掉、也都不构成开工阻塞。真正的开工门仍是 `owner_gates` 第 1 项 (10CG/Aria#195 已完成 C.2 合并或 owner 明示改序), 与本次审计结论无关。
