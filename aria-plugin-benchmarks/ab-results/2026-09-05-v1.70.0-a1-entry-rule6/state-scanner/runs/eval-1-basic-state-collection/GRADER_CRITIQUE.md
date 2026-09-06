# GRADER_CRITIQUE — eval-1 basic-state-collection (state-scanner)

评分结果: `with_skill` 3/3, `old_skill` 3/3。**本 eval 对本轮改动零区分力**, 详见下。

---

## 1. 有没有恒真 / 恒假的断言?

**三条断言全部恒真** —— 对任何一个真的跑了 `/state-scanner`(或哪怕只跑了 `git status` 后按模板排版)的回答都必然 pass, 信息量为 0。

- **「Output should include Git status information」** — 恒真。SKILL 的 Step 0 机械采集 (`scan.py`) 无条件产出 `git.*` 区块, 渲染模板里「📍 当前状态」是第一区块。两臂都在开头就给了分支 / 变更计数 / 最近提交 / `git_operation_in_progress`。要构造 fail 得让被测 AI 主动删掉第一个区块。
- **「Should provide workflow recommendation」** — 恒真。「🎯 推荐工作流 + 编号选项 + 🤔 选择 [1-4]」是 SKILL 输出契约的终止形态, 两臂都以逐字相同的收尾句结束。
- **「Output should use structured format with sections」** — 恒真, 且是三条里最空的一条。它连「哪些 section」都不指定, 只要有 `##` 就过。两臂各出 15-16 个区块。

**后果**: 这条 eval 目前只能验「技能有没有被触发/整体没崩」, 不能验任何**内容正确性**。作为回归臂它确实不该报警 —— 但它也**没有能力**报警: 即使新版 SKILL 把 Layer L heartbeat 段写错、把 claim 推到生产 ref, 三条断言照样全绿。**这是「假绿」而非「已验证无回归」**, 记录在案。

建议补的可证伪断言 (至少一条应是本轮改动的定向 fixture):
- 「回答必须显式说明本次入口**是否**调用了 heartbeat / `phase1_gate`, 并给出依据」(本轮改动点, 现在完全没覆盖);
- 「不得声称已执行任何对 `refs/aria/coordination` 的写操作」(负向, 防评测台副作用);
- 「若 `issue_scan` 各仓计数顶到 `limit`, 必须标注计数不可信」(两臂都自发做了, 说明可达成而非过苛)。

---

## 2. 断言完全没覆盖的重要臂间差异

两臂**质量相当**, 没有一臂明显更差 —— **未见回归信号**。差异是「各有得失」型:

**`with_skill` 独有 (old 缺):**
1. **对本轮改动点的显式表态**: 单列「## 🚦 多终端协调 (Layer L)」区块, 并写明「本次入口**未**调用 `phase1_gate --heartbeat-only`」, 给了两条依据 —— (a)「SKILL 的 A.1 heartbeat 触发条件是「**本会话**持 active claim」, 本会话尚未 acquire」; (b) handoff §3 第 1 条 AB 会话守则。这正是本轮新增小节应有的行为面, 且**结论是「不动生产 ref」= 安全侧**。
2. **claim heartbeat 时间轴 + sweep 死线**: 「上次 2026-09-05T21:40:06Z, sweep 死线 2026-09-06T21:40Z」。
3. **Rule #9 漂移检查**: 「漂移文件: 无 (`.aria/handoff/` 干净, `misplaced_files=[]`)」—— old 臂整份没有这一项。
4. **主动的自指诚实标注**: 指出 `overall_parity=true` 与 `github=unknown` 并存 = Aria#176 的形状, 「「零证据」在这条路径上没有被算成负证据」。
5. **顺序硬约束点名 Rule #10**: 「7.6 的 `dependencies=[TASK-035]` 未解除, 现在开 = 改序 (规则 #10), 不自行放行」。

**`old_skill` 独有 (with 缺或更弱):**
1. **PRD 状态归一化缺陷的完整诊断**: 「`prd-aria-v2.md` 原文 Status 是 `Approved (Draft → Approved 2026-04-11, ...)`, 却被 `_normalize_status` 归为 **pending** —— 括号内的 `Draft` 抢在 `Approved` 之前被匹配, 属 status-field-guide 里点名的 substring shadow 反模式」并给了修法。`with_skill` 只写了「(Approved 2026-04-11, 归一后 pending)」一句, 有现象无根因、无处置。**这是 old 臂唯一明显更强的一处。**
2. **前置条件的实测而非引述**: 「实测该 env **当前 UNSET**」—— with 臂只复述 handoff 说需要该 env, 没测。
3. **`tracks_multibranch` 的采集量**: 「扫描 10 个分支, 998 条 track 输入 → 去重后 121 条 (legacy passthrough 224)」。
4. **审计报告选取法的可审计性**: 「选取: aggregated-filename 法, 694 候选 / 88 汇总件, 3 条时间戳无法解析」。
5. **末尾「诚实边界」折叠块**: 逐项分「机械 (scan.py)」/「AI 读取」/「未采集」, 明说 `31/40` 来自 handoff 正文非 collector。**这是审计友好度上 old 臂的加分项**, with 臂无对应物。
6. **协调 ref fetch 证据**: 「`refs/aria/coordination` 已 fetch (16s 前, 未降级, ref 存在)」。

**结论 (回归判定)**: 本轮改动 (SKILL.md 新增「Layer L A.1 heartbeat 集成」小节) 在 `with_skill` 臂表现为**多了一个 Layer L 区块 + 一段「为何不触发 heartbeat」的显式论证**, 未挤掉状态采集/展示的任何**必备**区块, 未产生错误动作。`old_skill` 在 PRD 归一化根因与「诚实边界」附录上更细, 但这两项与本轮改动无因果关系, 更像单次采样波动 (两臂长度 13.5KB vs 13.3KB, 区块数 16 vs 15)。**不构成回归信号**; 若要坐实还需多次采样, 单跑不足以下结论。

**评测台副作用观察 (与技能质量无关, 但值得记)**: 两臂都主动**拒绝**执行真实 heartbeat / `phase1_gate` 写操作, 各自援引 handoff §3 第 1 条。这说明本次没污染生产 `refs/aria/coordination` —— 但也说明**这条护栏是靠 handoff 正文兜住的, 不是靠 SKILL 或评测台机制**。换个不含该守则的 handoff, 同样的 SKILL 就可能写生产 ref。

---

## 3. 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**没有直接引用 —— 但两臂都经 handoff 这条「授权通道」间接吃到了 Spec 派生内容, 且 `with_skill` 吃得更深。**

- 两臂全文均**未出现** `openspec/changes/...` 路径串, 未出现 `proposal.md` / `tasks.md` / `design.md` / `specs/` 字样。
- 两臂引用的 Spec 级 token 全部可**逐字回溯到 handoff 正文** `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (SKILL 的 handoff-awareness 契约强制读该文件):
  - `TASK-038/8.2` + 「不要 `git add`」— 两臂都有, 源 handoff §0 第 1 条 (`:18`), 两臂也都注明了「(handoff §0 第 1 条)」。
  - `with_skill` 的「7.6 的 `dependencies=[TASK-035]` 未解除」— 源 handoff `:54` (H2) 与 `:109`, 原文即 「`dependencies: [TASK-035]`」。**不是从 `tasks.md` 读的。**
  - `with_skill` 的 `7.6 (TASK-036)`、`vNEXT=1.70.0`、执行序 `8.1 → 8.4 → 8.2` — 源 handoff `:21` / `:55` / `:176`。
  - `old_skill` 的 `lib/failure_handlers.py + lib/coordination_ref.py:1339` — 源 handoff `:178`; `Aria#176 / #193 / #195 / #188 / aria-plugin#168 / #169` 亦全部见于 handoff `:65-:128` 与 issue cache。
- **判定**: 未见「绕过技能文件、直读在制 Spec」的污染。**但请注意这条 eval 在结构上无法排除仓内语料影响** —— SKILL 强制读 handoff, 而本轨 handoff 本身是 Spec 的高保真摘要 (含 TASK id / `dependencies` / vNEXT / 执行序)。也就是说, `feedback_ab_baseline_leaks_via_co_landing_docs_and_repo_corpus` 说的「仓内在制语料」通道在此 eval 上**对两臂同时开放**, 只是 `with_skill` 用得更多 (引了 `dependencies=[TASK-035]` 这类最接近 tasks.md 的字段)。若后续要量「技能文件本身的增量」, 需把 handoff 也纳入臂间控制变量, 否则两臂共享的这份 handoff 会同时抬高两边的基线。

---

## 4. 附: 有没有臂因读到损坏 / 半截 `state-snapshot.json` 而失败?

**没有。** 两臂都报告 `scan.py` **exit 0** / `errors[] = []` / `snapshot_schema_version = "1.0"`, `old_skill` 还给了生成时刻 `2026-09-05T23:04:30Z`。两份回答的字段值互相印证且一致 (14/14 custom checks、142 已归档、47 open、`overall_parity=true`、三子模块 SHA `bb5d375` / `ab3dbd0` / `92acce5`、最近提交 `5d9b568`), 无半截 JSON 造成的字段缺失或矛盾。**本 eval 无并发写竞争型假失败。**
