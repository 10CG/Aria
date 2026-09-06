# GRADER_CRITIQUE — eval-2-test-verification (phase-b-developer)

评分结果: `with_skill` 3/3, `old_skill` 1/3。**这个 2 分差不能读成技能质量差**, 理由见 Q0/Q1。

---

## Q0. 断言碰得到本轮改动面吗? —— 一条都碰不到

本轮两版 `phase-b-developer/SKILL.md` 的差异全部落在 **B.0 认领块**:

1. carry-id 占位串 `<本 cycle carry-id/Spec id>` → `<A.1 认领时派生的那一串>`, 并新增处方行「carry-id 取值 = A.1 认领时派生的那一串 (逐字, 不重新拼) …… 两端不同串会各认领一条, 收尾时 release 只命中一条」;
2. 两段 push 注释勘正: bootstrap 走 `push=False` **不推**, 真正推送点是 `phase1_gate.py` Step 9 `resilient_push`(:880) 与 7a self-resume(:597); `--no-push` / `ARIA_COORDINATION_NO_PUSH` **只抑制推送, 不是 skip 条件**。

三条断言分别测「跑没跑测试套件」「报没报计数与 pass/fail」「有没有把 Phase C 入口卡在测试上」—— **全部落在 B.2 / Phase C 闸门, 与 B.0 认领块零交集**。所以本 eval 对本次改动的**测量覆盖率 = 0**; 观察到的 3:1 分差来自一个与改动正交的行为选择 (见 Q1), 不构成改动有效性的证据。

反讽的是, **两臂输出里恰好有一处清晰的、正落在改动面上的差异, 但没有任何断言去读它** (详见 Q2 第 1 条)。

---

## Q1. 恒真 / 恒假 / 零信息量的断言

**1. 断言 3「Should gate Phase C entry on all tests passing」—— 本 fixture 下实质恒真。**

本 eval 的 prompt 前提是假的: 仓内根本不存在 OAuth2 的 TASK-006 (两臂独立实测均确认)。既然「所有测试通过」这个正分支在本 fixture 下**不可达**, 任何合规回答唯一能产出的裁决就是「不进 Phase C」, 于是断言 3 必 pass。实测: `old_skill` **一条测试都没跑**照样拿到 pass (「三项阻塞项任一不过，不进 Phase C。」+「ready_for: ✗ 尚不可进入 Phase C」)。

也就是说这条断言**分辨不出「因为测试红所以卡」和「因为测试压根没跑所以卡」**, 而这正是它字面上想区分的东西。零信息量。

**2. 断言 1 与断言 2 不是两条独立测量, 是同一件事记两分。**

断言 2 (报计数与 pass/fail) 对任何跑完测试的臂都是断言 1 的必然推论 —— 没有哪个臂会跑完 pytest 却不贴计数。反向也成立: 没跑就一定报不出计数。三条断言实际只有 **~1 个独立比特** (跑了没有), 而且那一比特被记了两次, 把单一行为差放大成 2 分差距。

**3. 更严重的效度问题: 断言 1 在本 fixture 下奖励「顶替验证」、惩罚「诚实拒绝」。**

prompt 要的是 TASK-006 (OAuth2) 的验证。两臂都实测到它不存在:

- `old_skill` 停下不跑: 「我不会拿「跑了别的测试套件、全绿」去顶 TASK-006 的验证 —— 那是假绿，会把「未验证」当成「已验证」传给 Phase C。」→ 断言 1、2 双 fail。
- `with_skill` 换了个对象跑: 「按**当前分支**上那条真实的、状态为 `done` 的 TASK-006 执行验证」→ 断言 1、2 双 pass。

按 Aria 自己的方法论 (禁假绿 / 「没测」≠「测了达标」), `old_skill` 的处置是**可辩护的**, 甚至更保守。当前断言集把它判成了失败项。**结论: 这 2 分差是 fixture 缺陷的产物, 不应计入版本比较。** 建议要么给这个 eval 配一个真实存在的被测任务, 要么把断言 1 改成「要么跑套件并给出计数, 要么明确指出任务不存在并拒绝以别的套件顶替」这种双分支形式。

---

## Q2. 断言完全没覆盖的重要差异

**1. (正落在改动面上) carry-id 的取值方式 —— 两臂相反。**

- `with_skill`: 「补跑命令 (**carry-id 逐字取 A.1 认领时那一串, 不重新拼**)」, 命令里 `--raw-track-id "a1-entry-claim-duplicate-work-guard-<container_uuid>"` (沿用 Spec id 派生)。
- `old_skill`: `--raw-track-id "TASK-006-oauth2-integration"` —— **当场新拼了一串**, 既非 A.1 carry-id 也非 Spec id。这恰好就是新版处方要防的失败形态 (「两端不同串会各认领一条, 收尾时 release 只命中一条」)。

这是本轮改动**唯一在输出里可观测到的直接效果**, 而断言集完全没读它。

**2. (正落在改动面上) push 点的归属精度 —— 两臂相反。**

- `with_skill` 点名到步骤: 「它的 **Step 9** 会向 `origin` 推 `refs/aria/coordination` —— 外向且难撤销的动作, 需要你显式点头, 我不自我授权。」并进一步正确应用第二条勘正: 「当前 shell 里 `ARIA_COORDINATION_NO_PUSH` 是**设着的** …… 这时候跑只会写本地 claim 而不同步远端, 等于制造一条别人看不见的认领, 比不跑更坏。」—— 既没把它当 skip 条件, 也没把「写 claim」等同于「已同步远端」。
- `old_skill` 把推送笼统挂在 claim 写入上: 「成本只是一次 claim 写入（会向 origin 推 `refs/aria/coordination`，只有协调元数据，不碰代码分支）」—— 不点步骤, 且暗含「写 claim 即已推」的旧理解。

同样零断言覆盖。(公平起见: `old_skill` 的 `skip_if` 分析本身没错, 只列了 `coordination.enabled` 与非 git repo 两条, 没有误把 env 变量当 skip 条件。)

**3. 唯一 1 红的根因分析 + 双向负控 (仅 with_skill)。**
`with_skill` 把 `1 failed, 1557 passed` 定位到执行环境污染 (`ARIA_COORDINATION_NO_PUSH` 使 `push_skipped=True`), 并跑了**两组**负控: 单文件去变量 7 passed; 15 个涉 push 文件去变量 393 passed, 且显式说明第二组的必要性 —— 「该变量若还造成了**反向的假绿** …… 单看 (a) 看不出来」。这是本次两臂间质量差距最大的一处, 断言集只问「有没有报 pass/fail」, 读不到根因质量与假绿控制。

**4. 覆盖率三态与 `not_measured` ≠ pass。**
两臂都做对了 (`with_skill`: 「现状记为 `coverage: not_measured`, **不是 pass**」; `old_skill`: `coverage: null`, 且 `framework_build_passed: not_configured   # 三态：skip ≠ pass`), 但这是本 skill 的核心反假绿行为, 断言集一条都没有 —— 属于**共有强项被漏测**, 换成一个会把 skip 写成 pass 的坏版本, 本 eval 照样满分。

**5. 只有 `old_skill` 提出的三点。**
(i) 覆盖率门槛 80 (B.2 参数) vs 85 (branch-finisher / 评审) 的既有不一致, 并请 owner 定夺;
(ii) 集成测试特有的假绿模式 —— 「集成测试最常见的假绿是「外部 IdP 不可达 → 测试被 skip → 套件绿」」+「对每条 OAuth2 测试问一句「它怎么会红？」」;
(iii) 流程边界勘正 —— 「**PR merge 前的 pre-merge gate（本 PR CI passing + main 无 in-flight run）是 phase-c-integrator C.2.4 的事**，不在 Phase B 内」。
三条都是真实增量, 断言集不读。

**6. 只有 `with_skill` 提出的三点。**
(i) Phase C 的真实阻塞面 —— 任务 31/40、Rule #6 AB benchmark 未跑 (`benchmarks.require_before_merge=true`)、aria 子模块工作树脏;
(ii) 运行坑 —— 「**从仓根跑会 12 个 collection error**(`ModuleNotFoundError: No module named '_helpers'`) …… 必须先进 tests 目录」;
(iii) 负控安全性自证 —— 确认用例跑在 `tempfile.mkdtemp()` 临时 repo + 临时 bare remote, 去掉变量不会向生产 origin 推东西。均无断言覆盖。

**7. 共有强项: 步骤号勘正。** 两臂都指出用户说的「B.3」实为 **B.2 (test-verifier)**, B.3 是 arch-update。这是本 eval 里两臂最一致的正确行为, 也没有断言。

---

## Q3. 仓内语料污染 —— `with_skill` 明确污染, `old_skill` 未污染

**`with_skill` 直接引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档, 且其得分依赖于此。**逐字证据:

- `answer.md:46` —— 「| \`openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:281\` | SC-15 回归守卫 (baseline 即绿): 改名两步无孤儿 + 无关第三方 claim 负控 | \`done\` |」(带行号引用该 change 的 `detailed-tasks.yaml`)
- `answer.md:51` —— 「它就在你现在这个分支 \`feature/a1-entry-claim-duplicate-work-guard\` 的 Spec 里, 交付物是 \`aria/skills/state-scanner/tests/test_heartbeat_by_track.py\`」(把该 Spec 的交付物当成被测对象)
- `answer.md:199` —— 「\`proposal.md\` 有 Status / Spec Level (2) / Linked Issue (\`10CG/Aria#174\`) / Why / What Changes / Success Criteria / Impact; \`tasks.md\` 编号连续无缺口; \`detailed-tasks.yaml\` 结构有效, TASK-006 \`status: done\`」
- `answer.md:200` / `:257` —— 「进度以 \`tasks.md\` 为准: **31/40**」/「**任务未做完 — 31/40**。\`tasks.md\` 还有 9 条未勾。」
- `answer.md:104` —— 「SC-5 / SC-6 / SC-7 / SC-15 全绿」(引该 change 的 SC 编号)
- `answer.md:67` —— `--linked-issue "10CG/Aria#174"` (该 change 的 Linked Issue 原串)
- 另外 `answer.md:47` 还引了第二个 in-repo Spec: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/detailed-tasks.yaml:116`

污染的**因果影响明确**: `with_skill` 的断言 1、2 之所以 pass, 正是因为它从这个仓内 change 里挑出了一个真实的、`status: done` 的 TASK-006 当替身来跑。换到干净仓 (没有这份 in-repo Spec 语料), 这一臂没有可跑的对象, 大概率也会退回到 `old_skill` 那种「停下问路径」的形态 —— 即 **3:1 的分差在干净语料下很可能塌成 1:1**。

**`old_skill` 未引用该目录。**全文的仓内引用只到 `.aria/config.json` 实读值、当前分支名、以及测试目录清单 (「\`tests/{acceptance,auto-trigger,integration}\`、\`aria/tests\`、\`aria/hooks/tests\`、\`aria-orchestrator/tests\`、\`aria-orchestrator/scripts/tests\`」), grep `openspec|a1-entry|detailed-tasks|proposal\.md|tasks\.md|10CG/Aria#|31/40|SC-1[0-9]` 在其 `answer.md` 里**零命中**。

---

## 建议 (给套件维护者)

1. 本 eval 的 3:1 **不要计入本轮 v1.70.0 的区分力结论** —— 覆盖率为 0 (Q0) + fixture 前提为假导致奖惩倒挂 (Q1.3) + 高分臂依赖仓内 Spec 语料 (Q3), 三重失效。
2. 若要让本 eval 真能测 B.0 改动, 需加断言 (可证伪): 「carry-id 必须声明为逐字沿用 A.1 派生串 / Spec id, 不得当场新拼一个 track id」「若提及推送, 必须点到 `phase1_gate` Step 9 / 7a, 不得把 bootstrap 或 claim 写入等同于已推远端」「不得把 `--no-push` / `ARIA_COORDINATION_NO_PUSH` 当作 B.0 的 skip 条件」。前两条在本轮两臂上已实测有区分力 (Q2.1 / Q2.2)。
3. 断言 3 需拆成可分辨两态, 或换到一个「测试真能全绿」的 fixture 上, 否则永远只观测得到 block 分支。
4. 补一条覆盖 `skip ≠ pass` / `not_measured ≠ pass` 的断言 —— 这是该 skill 的承重行为, 现在完全裸奔。
