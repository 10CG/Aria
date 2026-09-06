---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T22:01:31.682Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席 (任务分解的架构与排序)

审计对象: `tasks.md` (6 组 41 项) + `detailed-tasks.yaml` (41 TASK) @ commit `60808b2`, 依据 `proposal.md` v7 (Approved)。

机械底账 (脚本实跑, `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/dag.py`):
41 任务 / id 唯一 / 依赖引用全部可解析 / **无环, 拓扑序存在 (topo len = 41)** / 总工时 84.5h / 无 >8h 或 <0.5h 任务 (最大 4h, 最小 0.5h 共 3 项) / agent 分配实计 `backend-architect 15 · qa-engineer 16 · knowledge-manager 10` 与 `metadata.agents` 完全一致 / parent 1:1 覆盖 tasks.md 全部 41 个 checkbox (归档门实读 boxes 总数 = 41, 无游离 checkbox)。
组 1 → 组 2 的 RED→GREEN 边**全部成立**: TASK-012←001 / 013←012,002 / 014←013,004,005 / 015←013,003 / 016←013,007 / 017←014,010,006 / 018←008 / 019←018(→008) / 020←014,009, 每条实现任务都传递依赖到它的 RED 测试。以下问题都在这层之外。

## 审计结论

### C-1 (critical · issue · architecture) — S1 归档路径被组 6 的 4 个未勾 checkbox 结构性挡死; 「归档门按 status: deferred-s2 识别」是不存在的机制

- **scope**: `tasks.md:8` `tasks.md:93` · `detailed-tasks.yaml` TASK-000 verification · 归档门 `aria/skills/state-scanner/scripts/lib/spec_complete.py`
- **summary**: 计划断言 S2 任务在 S1 下「不算未完成, 归档门按 `status: deferred-s2` 识别」。实读 gate: yaml 分支**只在 tasks.md 缺失时**才被读, 且 `deferred-s2` 不在 done-family。S1 收尾必被 BLOCK。
- **evidence**:
  - `spec_complete.py:257-259` `tasks_file = spec_dir / "tasks.md"` → `if not tasks_file.is_file():` 才走 `:264 _yaml_only_tasks_verdict`; tasks.md 存在时 `:274 unchecked = [b for b in boxes if b not in ("x","X")]` → `:278` 直接判 `complete=False`。yaml 的 `status` 字段在该路径上**从未被读取** (`:189-193` docstring 自陈「tasks.md 缺失时用 detailed-tasks.yaml」)。
  - 即便走 yaml 分支也不放行: `detailed_tasks.py:83 _DONE_FAMILY = frozenset({"done","completed"})`, `spec_complete.py:215` 非 done-family 一律计为 non_done。`deferred-s2` ∉ 白名单。
  - `openspec-archive/SKILL.md:153` 「complete=false ∧ verdict∈{pass,warn} ∧ 未配逃生舱 → 默认 BLOCK … 中止归档」; `:267-276` Step 7 另会把未勾项当 deferred 自动开 tracker issue。
  - **实跑复现** (scratchpad `simS1/`, 组 0-5 全部 `[x]`, 组 6 保持未勾, yaml TASK-027..030 置 `deferred-s2`):
    `is_spec_complete(...) = {'complete': False, 'reason': "tasks.md has 4/41 unchecked task(s); normalized Status = 'approved' (≠ done)"}`
  - 附注: `carry_forward.py` 的注释正则要求 `[` 紧邻 token, tasks.md 里的 `` `deferred-s2` `` 不触发, 因此**没有**第二条兜底路径。
- **后果**: S1 (proposal 自陈的可独立 ship 形态, 且 `0.1` 尚无 ack 时的默认形态) 走到 D.2 必然撞 BLOCK, 只剩两条出路: owner 授权 `--archive-design-only` 逃生舱 (会给本 Spec 打上 `archive_type: implementation-deferred`), 或临场改 tasks.md —— 而 Rule #10 禁止 AI 自行豁免 enabled 闸。必须在 A.2 阶段就选定并写死落法 (可选: 组 6 不进 tasks.md checkbox 面, 只留 yaml 条件任务 + proposal 记 deferred; 或 S1 下把 6.x 勾为 `[x]` 并在行内写「S1 不适用」而不使用 `[defer...]` 形注释; 或预先取得 owner 的逃生舱授权并写进 5.x)。

### C-2 (critical · issue · implementation) — TASK-033 的 SC-7「14 条 state-check failed=0」在其排定位置上不可满足, 且全 41 任务无人负责让它变绿

- **scope**: `detailed-tasks.yaml` TASK-033 (parent 4.3, `dependencies: [TASK-035]`) · `tasks.md:82` · `.aria/state-checks.yaml:266-288`
- **summary**: TASK-035 一 bump `plugin.json`, `plugin-cache-currency` 立刻 FAIL(STALE); 转绿需要 push + marketplace update + `/plugin update` + 重启 session, 这四步没有任何任务承载, 而 TASK-039 (PR/merge) 又以 TASK-033 为前置。
- **evidence**:
  - `.aria/state-checks.yaml:266-288`: 比对「Claude Code 实际加载版本 vs 仓内 SOT `aria/.claude-plugin/plugin.json`」, 判据「`< SOT → STALE`」, `enabled: true`; fix 明写「依次跑 `/plugin marketplace update` 再 `/plugin update`, 装完**重启 session**」。
  - `.aria/probes/plugin-cache-currency.py:18-19` 「`min(已装版本) < SOT → FAIL STALE`」, `:139 return _fail(...)`。
  - 当前 `.aria/state-snapshot.json` 14 条 check 全 `pass`, 计数字段为 `failed/passed/skipped/total` ⇒ 一条 STALE 即 `failed=1`, 与 TASK-033 verification `custom_checks failed=0` 直接冲突。
  - DAG 位置: TASK-033 deps 只有 TASK-035 (bump), 早于 TASK-036 (双推) —— 即使不算 session 重启, 此刻 marketplace clone 也拿不到新版本 (memory `feedback_plugin_cache_stale_via_stale_marketplace_clone` 同形)。
- **后果**: SC-7 as sequenced 结构性红, 会在 B/C 交界处逼出「这条 check 是 warning 就跳过吧」的临场降级 —— 正是 Rule #10 点名禁止的形态。需要显式落法: 把 `plugin-cache-currency` 的复绿动作 (push → marketplace update → plugin update → 重启 session → 复跑) 拆成 TASK-036 之后的独立任务, 或在 tasks.md 明写该 check 在本 cycle 的期望态与 owner 授权的判定口径。

### M-1 (major · issue · architecture) — 合并/推送闸的前置集漏掉 6 个交付与留痕任务, 拓扑上允许「未做完就 ship」

- **scope**: `detailed-tasks.yaml` TASK-034 `dependencies: [TASK-032, TASK-026, TASK-023]` · 反向依赖计算
- **summary**: TASK-016 / 022 / 025 / 031 / 037 与整个组 6 都是零反向依赖的叶子, 不在 5.1 merge / 5.3 双推 / 5.6 PR 的任一前置链上。
- **evidence**: 反向依赖实算 (同一脚本) 得零 dependents 的任务: `TASK-016`(2.5 D-0(a) 族键剥离) / `TASK-022`(3.2 §2.3.5 判据表, D2 的核心交付) / `TASK-025`(3.5 模板删鼓励句) / `TASK-031`(4.1 Rule #6 substitute RED→GREEN 留痕) / `TASK-037`(5.4 fixture 公开性确认) / `TASK-028,029,030`。TASK-034 的前置只有 032/026/023。
  - 代码侧 (016) 有间接兜底: TASK-032 全套 pytest 会因 TASK-007 的族键夹具红而暴露。**文档与留痕侧没有任何兜底**: 022 (standards §2.3.5 三行) / 025 (模板) / 031 (Rule #6 留痕) 的 verification 都只在自己身上, 全套 pytest 不覆盖 standards 与 `aria/templates/`。
  - 尤其 TASK-031: Rule #6 要求「Skill 变更发版前须过 benchmark (或 substitute)」, 而版本 bump (035) 与双推 (036) 都不以它为前置 ⇒ 顺序语义被 DAG 反转。
- **建议**: TASK-034 前置补 `TASK-016, TASK-022, TASK-025`; TASK-035 前置补 `TASK-031`; TASK-036 前置补 `TASK-037` (双推 github 是不可逆的公开动作, 公开性确认必须在它之前)。

### M-2 (major · issue · architecture) — S2 形态在 DAG 上是死支: flip / 发布门 / 复现测试 不进回归, 也不进合并推送

- **scope**: `detailed-tasks.yaml` TASK-027..030 · TASK-032 / 034 / 036 / 039 的 dependencies
- **summary**: 判定为 S2 时, `get_container_id()` flip 及其发布门在拓扑上可以晚于 merge/push, 或干脆缺席本次 ship, 而 SC-3 的 S2 臂正是「未通过发布门则 flip 不进合并集」。
- **evidence**: 反向依赖实算: `TASK-028 <- []`, `TASK-029 <- []`, `TASK-030 <- []`; `TASK-027 <- [028,029,030]` (只回流到组 6 内部)。TASK-032 (全套回归) deps `[020,017,019,011]` 不含 027/030; TASK-034/036/039 均不含组 6 任一。
  - 对照 `tasks.md:96` 「6.2 发布门: phase-c-integrator C.2 前 release 清单加『T3b 迁移检查通过』勾选项; 未通过则 flip 提交不进合并集」, 而承载 C.2 的 TASK-039 (5.6) deps `[TASK-036, TASK-033]`, 与 TASK-028 零关联 ⇒ 该发布门无机械承载, 只是一句自述。
- **建议**: 给组 6 加条件边 (S2 时 TASK-032 前置补 027/030, TASK-034 前置补 028), 并在 tasks.md 明写「S1 时这些边随 6.x 一并失活」。

### M-3 (major · issue · architecture) — S2 判定时点自相矛盾: 判形态的 0.1 跑在征求 ack 的 0.2 之前, 首轮 S2 不可达且无重评点

- **scope**: `tasks.md:8` `tasks.md:40-41` · `detailed-tasks.yaml` TASK-000 / TASK-00A (`dependencies: [TASK-000]`) / TASK-027 (`dependencies: [TASK-000, TASK-00A, TASK-018]`)
- **summary**: S2 的定义含「对方在 #174 ack」, 但请求 ack 的 TASK-00A 依赖 TASK-000; 0.1 落笔时 ack 结构上尚不存在 ⇒ 形态只能写 S1, 而计划里没有「ack 到达后重评形态」的任务。
- **evidence**: `tasks.md:8` 「**S2** = a1-entry B.2 已落地**且**对方在 #174 ack」; `tasks.md:40` 「0.1 … 据此在 detailed-tasks.yaml `metadata.ship_shape` 写 S1 或 S2」; `tasks.md:41` 「0.2 … 征求 ack (S2 前置)」。yaml TASK-00A deps `[TASK-000]` 固化了这个顺序。TASK-027 notes 「仅 S2 (a1-entry B.2 已落地 且 #174 ack)」但其依赖里的 TASK-00A 只保证「留言已发」, 不保证「ack 已收」。
  - 该分支并非空谈: `git branch -a` 实读, `remotes/origin/feature/a1-entry-claim-duplicate-work-guard` 与 `remotes/github/...` 双端都已存在 ⇒ TASK-000 很可能读到「a1-entry 已落地」, 于是形态判定唯一悬而未决的就是 ack。
- **建议**: 把 S2 的两个前提拆开 —— 「a1-entry 已落地」由 0.1 判, 「ack 已收」作为 TASK-029 (且仅 029, 因为只有它动对方文本) 的独立前置; 或增设一个「ack 回收后重评 ship_shape」的任务并写明重评截止点。

### M-4 (major · issue · implementation) — 5.1 先打 tag、5.2 才 bump 版本, tag 会落在版本号仍是旧值的 commit 上

- **scope**: `tasks.md:86` · `detailed-tasks.yaml` TASK-034 (deliverables 含「aria 子模块 master (本地) + tag」) → TASK-035 (版本 5 文件 bump)
- **summary**: 顺序与 version-management 的规定相反, 产出的 `vNEXT` tag 指向的树里 `plugin.json` / `VERSION` 还是旧版本, 直接废掉 tag 的唯一用途。
- **evidence**: `standards/conventions/version-management.md:224-228` 「更新顺序: 1. 更新 VERSION 文件 (版本 SOT) 2. 提交 + 双远程推送 (含 tag: `git push <remote> vX.Y.Z`) 3. 逐 remote 独立核验 **tag 对象 SHA**」; 同文件 `:218-221` tag 的存在理由是「『v1.52.0 到底是哪个 commit』这种问题有答案」。计划里 TASK-034 (merge + tag) 是 TASK-035 (bump) 的前置 (`TASK-035 dependencies: [TASK-034]`)。
  - 附带: TASK-036 verification 只写「每 remote ls-remote SHA == 本地」, 未覆盖 `:228` 要求的 tag 对象 SHA 逐 remote 核验。
  - (标注: `version-management.md:104-106` 明确本仓群只有 `aria/` 打 tag, standards 零 tag —— yaml TASK-034 的 deliverables 已正确区分, 这一点无问题; tasks.md:86 的「standards 子模块同法」措辞偏松, 以 yaml 为准即可。)
- **建议**: 把 tag 从 TASK-034 移到 TASK-035 之后 (或直接并入 TASK-036 的推送步), 并把 tag 对象 SHA 的逐 remote 核验写进 TASK-036 verification。

### M-5 (major · issue · testing) — TASK-011 无转绿归属, 且其两条断言中至少一条在基线就是绿的, 与组 1「每条先红」抬头冲突

- **scope**: `tasks.md:55` (1.11) · `detailed-tasks.yaml` TASK-011 (deps `[]`, 反向依赖只有 TASK-032)
- **summary**: rule 1.54 在代码里根本不存在 (纯散文规则), 「规则命中」无可执行载体; fetch_gate 的「advisory 文案含 cross_owner」今天就成立。没有任何实现任务声明「TASK-011 转绿」。
- **evidence**:
  - `grep -rn "concurrent_churn" aria --include=*.py` 零命中; `scripts/`+`lib/` 下唯一 "1.54" 命中是 `spec_complete.py:1619` 的版本串 `v1.54.0`。rule 1.54 只存在于 `RECOMMENDATION_RULES.md` 与 `references/rules/advanced-rules.md:531-582` 的散文表。
  - 既有同类测试的可行形态是结构性存在测试: `tests/test_git_operation_rule.py:1-5` 自陈「Prose AI behavior … is verified by dogfood; this locks the *structural* contract」—— 那种测试的转绿来自 TASK-024 (文档加 `identity_advisories` 一句), 而非组 2 实现; yaml 里 TASK-024 与 TASK-011 之间零依赖边, TASK-024 的 verification 也没点名 TASK-011。
  - `aria/skills/phase-d-closer/scripts/fetch_gate.py:251-255`: `elif collision_kind != "none":` 分支的 message 已内插 `f"({collision_kind})"` ⇒ 传 `kind="cross_owner"` 时文案天然含该串, **改动前就绿**。而 `tasks.md:43` 的组 1 抬头写的是「测试先行 (RED — **每条**对 aria `7dd0135` 先红, 组 2 落地后转绿)」。
- **建议**: TASK-011 拆成两条并各自标注基线色 —— (a) rule 1.54 结构性存在测试, 依赖 TASK-024, 断言必须包含 TASK-024 新增的 `identity_advisories` token 才具备可证伪性; (b) fetch_gate 夹具明确降格为「回归锁 (基线即绿)」, 从组 1 的「每条先红」全称句里排除, 或把组 1 抬头改成非全称。

### m-1 (minor · risk · documentation) — S1 即改写 container-id 文件头注释为「label 仅展示」, 与 S1 下 label 仍是协调身份的事实反向

- **scope**: `tasks.md:65` (2.7) · `detailed-tasks.yaml` TASK-018
- **summary**: S1 不 flip, `get_container_id()` 仍 label 优先; 此时注释若正面断言「label 仅展示」, 会把 #135 陷阱从「邀请踩」变成「否认存在」。
- **evidence**: `tasks.md:65` 「2.7 `lib/identity.py` 新增 `get_container_label()`; `~/.aria/container-id` 文件头注释改写 (label 仅展示)」, 无 S1/S2 分档; 同文件 `tasks.md:8` 明确 S1「不 flip `get_container_id()`」; yaml TASK-018 verification 只锁「accessor 子句转绿」与「`get_container_id()` 语义在 S1 不变 (lock-in 仍绿)」, 对注释措辞零断言。
- **建议**: TASK-018 verification 增一条: S1 形态下注释须写明「label 当前仍参与协调身份, 将在后续版本改为仅展示」(反向 grep 锁「仅展示」不得单独出现), S2 落地后再改成终态措辞。

### m-2 (minor · issue · documentation) — 「ship 后关 #193 / #135 留缺口 1-2」无归属任务

- **scope**: `tasks.md:90` (5.5) · `tasks.md:19` (范围边界表) · `detailed-tasks.yaml` TASK-038
- **summary**: 计划把 issue 关闭推给「D 期执行」, 但 D 期的宿主 phase-d-closer 没有关 linked issue 的步骤, TASK-038 的交付物只到文案。
- **evidence**: `tasks.md:90` 「ship 后关 #193, #135 留缺口 1/2 (D 期执行, 本条只准备文案)」; `tasks.md:19` 把 Phase D 界定为「cycle 进度 / 归档 / 周期 handoff / claim 释放」; `aria/skills/phase-d-closer/SKILL.md` 全文 issue 相关只有委托 openspec-archive Step 7 建 **tracker** issue (`:111-124, :261-262, :281`), 无关闭 linked issue 的动作。yaml TASK-038 deliverables 只有 `.aria/triage-comment.md`, verification 只验文案内容。
- **建议**: 或在 5.5 明确「关闭动作由本 cycle 执行者在 5.6 merge 后手动完成」并写进 TASK-038 的 verification, 或加一条 D 期任务。

## Verdict

FAIL (Critical 2 / Major 5 / Minor 2)。

DAG 本体是健康的 —— 无环、拓扑序存在、组 1→组 2 的 RED→GREEN 边逐条成立、agent 分配与 deliverable 类型一致、工时粒度全部落在 0.5-4h。问题集中在**边界任务**: (a) 两个 Success Criteria 的承载机制经实读/实跑证明不存在或不可满足 (C-1 归档门的 `deferred-s2` 识别、C-2 plugin-cache-currency); (b) 合并推送闸的前置集漏掉 6 个交付/留痕任务, 使「未做完即 ship」在拓扑上合法 (M-1/M-2); (c) S2 分支的判定时点与 tag 顺序两处排序倒置 (M-3/M-4); (d) 一条测试无转绿归属且部分断言基线即绿 (M-5)。C-1 与 C-2 都会在 B/C/D 交界处逼出「这条闸跳过吧」的临场降级, 而这正是 Rule #10 禁止 AI 自行处置的形态 —— 必须在 A.2/A.3 收口, 不能留到执行期。

## Vote

REVISE

## 轮次记录

| 轮次 | 席位 | 结论 | 备注 |
|------|------|------|------|
| R1 | tech-lead | FAIL (2C / 5M / 2m) | post_planning 首轮; 镜头 = 依赖 DAG / S1-S2 双形态 / a1-entry 排序 / Level 3 完整性 / 工时与粒度。全部 finding 附实读 file:line 或脚本实跑输出; 归档门结论经 scratchpad 沙箱复现 (未触碰仓内文件)。本轮无历史轮次可比对, converged=null。 |

**未列为 finding 的核对项 (已实读排除, 备下轮复用)**:
- proposal T12「Lab 内部指针决策单放主仓 `docs/decisions/`」看似无对应任务, 实为已完成 —— `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md:13,16-18` 自陈「Lab 内部指针决策单即本文件」, 交付面已闭合, 不是缺口。
- 冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 实读 `tracks` 长度 = 996, 与 proposal 的「996 行」一致 (文件物理 9967 行是 pretty-print, 非矛盾)。
- 该语料的记录键实测恰为 `branch/filename/legacy/owner_container/phase/status/track_id/updated_at` 八项, 与 TASK-006 的「八字段」清单逐字相同, 且覆盖 `collision.py:86-140 track_to_claim_record` 读取的全部字段 (`owner_container`/`track_id`/`updated_at`/`status`/`phase`) ⇒ fixture 形态无 drift 风险。
- `claim_lifecycle.py:377-381 release_claim_by_track(raw_track_id, status="done", identity=None, ...)` —— TASK-019 把它列为 deliverable 并注「(既有)」属实, 不是隐藏的 scope creep。
- 组 5 的多远程顺序主干正确: TASK-036 verification 明写「gitlink 在子模块核验后才 bump」「每 remote ls-remote SHA == 本地」, 与 CLAUDE.md 硬约束 1+2 一致; TASK-034 明写禁 Forgejo 服务端合并。仅 tag 位置有误 (M-4)。
- TASK-033 依赖 TASK-035 的方向本身合理 (`m6-version-badge-match` / `plugin-version-arch-docs-match` 只能在 bump 后绿), 问题不在这条边而在同批的 `plugin-cache-currency` (C-2)。
