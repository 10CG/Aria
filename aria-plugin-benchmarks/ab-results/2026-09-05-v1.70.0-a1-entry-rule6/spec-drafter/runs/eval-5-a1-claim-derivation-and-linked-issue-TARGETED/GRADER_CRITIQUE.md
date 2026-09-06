# Grader critique — eval-5 a1-claim-derivation-and-linked-issue-TARGETED

判分结果: `with_skill` 8/8 · `old_skill` 0/8。以下是对**断言集本身**与**分数没表达出来的东西**的批评, 不改判分。

---

## 1. 恒真 / 恒假 / 低区分力断言点名

**断言 7「不建议「先传着看看」/「传空字符串」这类变体」—— 近似恒真, 措辞有缺口。**
它是一条**否定式**断言: 任何没提到这两个词的回答都自动通过。本次两臂**都没有**字面主张「先传着看看」或「传空字符串」。我把 `old_skill` 判 false, 依据是 grader 指令里那条「主张『传空字符串』或『照传哨兵』的一律判 false」—— 该臂逐字写着「**照样要传**, 实参逐字是 `none`。」, 属于同一类「用变通手段代替省略」。但这是**我按指令外推**的, 断言原文并没有点名「照传哨兵」。建议改写为「不主张任何『传点什么』的变体 (照传哨兵 / 传空字符串 / 先传着看看), 只允许省略整个参数」, 否则单看断言文本它对本题两臂都恒真, 零区分力。

**断言 3 / 4 / 5 共用同一个判定点, 权重被放大 3 倍。**
三条全部由 `old_skill` 的一句「**三份都要传**, 但只有一份能原样传。」与 `with_skill` 的同一张表 (A 列「**传**」/ B 列「**不传 —— 省略整个参数**」/ C 列「**不传 —— 省略整个参数**」) 决定。它们不是恒真, 但也不是三个独立行为: 一臂只要在「哨兵/脏串该不该省略」这一个认知上翻车, 就一次丢 3 分。8-0 的比分因此夸大了被测行为的**条数** —— 独立认知点实际是 4 个 (track-id 拼法 / label 不入 id / 三格省略 / 放弃要 release)。

**断言 1 与 2 高度耦合。**
拼对 `add-oauth-login-1a2b3c4d` 基本蕴含「没用 label」。断言 2 真正独立的那半是「**改 label 不该换掉 track-id**」这个理由; 本次 `with_skill` 给了同义句, 但如果一臂拼对了串却讲不出理由, 现行措辞下多半仍会被判 pass。

**断言 8 把「方向」和「机制字面」压成一个 bool, 造成信息损失。**
`old_skill` 其实**答对了方向**: 它把「先把认领放掉」列为第一件事, 并独立推导出悬空 claim 的危害 (「别的终端 / 下一个 session 看到 `add-oauth-login` 有人认领, 就绕开它, 这块方向实际上没人做但也没人敢碰。」)。它失分是因为下一句「但**我加载的 skill 里没有释放动作的定义**, 我不会替你编一条命令出来。」—— 承重断言点名了 `release_gate.py --raw-track-id`, 「大意接近」不算, 故判 false。建议拆成 8a (方向: 要 release, 不能放着不管) / 8b (机制字面: `release_gate.py --raw-track-id <同一串> --status abandoned`), 否则「知道该做什么但不知道怎么做」与「压根没想到」在分数上无法分辨。

**无恒假断言**: 8 条全部被 `with_skill` 实际满足, 都可达。

---

## 2. 断言没覆盖、但确实存在的重要差异

**(a) 认识论姿态 / 幻觉 vs 无知 —— 完全没测。**
`old_skill` 开篇即声明边界 (「但对 **A.1 入口认领的 CLI 参数 `--raw-track-id` 怎么拼**, 这个 skill 里一个字都没有。」), 并把自己的答案标成候选 (「这两点我不打算凭感觉定死。落之前我会去看那个入口的 `--help` 或它的规范文档, 以实际定义为准」)。它的失败模式是**无知识**而非**幻觉**, 且元判断是对的。断言集只测终值正确性: 该臂的校准得零分, 而 `with_skill` 的高置信也不会因此被额外奖励 —— 若 `with_skill` 恰好答错, 同一套断言会给出与 `old_skill` 相同的 0 分, 无法区分「自信地错」和「诚实地不知道」。这一维在 skill 评估里通常比终值更值得看。

**(b) 省略参数后的读数纪律 (四态表) —— 零覆盖, 却是断言 4/5 的直接下游。**
`with_skill` 给了完整四态 (键缺席 =「本轮未检测」/ `linked_issue_overlap == []` =「无碰撞」/ `unknown_schema_claims > 0` 按存在处理 / `linked_issue_overlap == null` + error =「未能核实」) 加一句「最后一行绝不可渲染成「无碰撞」—— 零证据不是正证据。」与 `.get(key, [])` 反模式警告。省了参数就必然遇到「键缺席」, 把它读成「无碰撞」是这条链上最危险的一步。现行断言集对这块的静默回归**恒判 8/8**。

**(c) 幂等与委派分工 —— 零覆盖。**
`with_skill` 独有: 按 `(container_id, session_id)` 定位 `claims/<container>/<session>.yaml` 的幂等 check; 以及「经 `phase-a-planner` 委派时上游已认领, 直调路径**没有 Level 1 例外**」。这决定了会不会重复 acquire, 属于运行时指令面。

**(d) 改名义务 (release 旧 + acquire 新) —— 零覆盖。**
它是断言 8 的孪生退出义务, 而且更容易被忘。`with_skill` 主动给了 (含 `add-oauth-login` → `add-oidc-login` 的实例), `old_skill` 完全没有。断言集不问。

**(e) C 的正确处置是回去改文档字段, 不是命令行打补丁 —— 零覆盖。**
`with_skill`: 「而不是在命令行上替它打补丁 —— 那样文档仍然不合规, 只是这一次跑通了。」一臂完全可以答对「C 不传」(断言 5 pass) 却把用户留在一份永远不合规的 proposal 上。

**(f) `old_skill` 有两处正确且有用的内容, 断言集完全看不见, 0/8 低估了它。**
其一:「**不要走 openspec-archive**, 归档是给「做完了的变更」用的」; 其二: 把放弃理由写 `docs/handoff/` (Rule #9) 而非 `.aria/handoff/`, 并说明要写的是「排除了什么」而不是流水。这两条按项目规范都对。另有一处与 SKILL.md 现有条款一致的正确内容:「字段**写在头部第几行不影响机械判定**。check 按 E0 取文档序第一条 depth-1 命中」。**0/8 应读作「该断言集所测的 4 个认知点全没答对」, 不能读作「该臂回答无价值」。**

**(g) 完整命令形态 (`--phase` / `--mode advisory` / `--include-terminal` / `--repo-path`) —— 零覆盖。**
`--phase` 在 `phase1_gate.py` 是 required, 漏了第一次实跑就被 argparse 拒; 断言集不问, 只有 `with_skill` 给全了。

---

## 3. 污染判定: 是否有臂引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/`

**判定: 两臂均未见引用该目录, 无污染证据。**

逐字核验:

- 对两份 `answer.md` grep `a1-entry` / `duplicate-work` / `detailed-tasks` / `tasks.md` / `SC-` / `R6` / `rework` —— **零命中**。
- 两臂全文对 `openspec/changes/` 的引用只有夹具自身那一处: `with_skill` 的「本 Spec 目录 `openspec/changes/add-oauth-login/` 的**目录名, 逐字取**」, `old_skill` 的「本 Spec 目录 `openspec/changes/add-oauth-login/` 的**目录名**, 不带 `openspec/changes/` 前缀, 不带尾斜杠」与「直接删掉整个 `openspec/changes/add-oauth-login/` 目录」。

来源可解释性 (排除「必须靠仓内 proposal 才答得出」这一嫌疑):

- `with_skill` 的**每一条承重内容**都能由 aria HEAD (`ab3dbd0`) 的 `skills/spec-drafter/SKILL.md:73-129` (整块 `## 前置: REQUIRE claim (A.1, MUST)`) 逐字解释, 无需读 proposal。该文件 `:84` 是命令行里的 `--raw-track-id "<spec-slug>-<container_uuid>"`; `:97-99` 逐字「slug = 本 Spec 目录名 `openspec/changes/<slug>/` **逐字**(不预归一, 归一在 CLI 内部做); uuid 段取 `~/.aria/container-id` 的 **`uuid` 字段**, **不是 `label`** —— 改一行装饰性 label 不该换掉 track-id。」; `:104-105` 逐字「**哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 一律省略整个参数**, 绝不可把哨兵当值传: 任何非空字符串都 truthy, 两份毫无关系的 Spec 只要都写哨兵就会互相命中。」; `:129` 逐字「`放弃方向 ⇒ release_gate.py --raw-track-id <同一串> --status abandoned`」; 四态表在 `:117-122`, `.get(key, [])` 警告在 `:124-125`。该臂自己也把出处指向 SKILL.md:「(SKILL.md 里明写的形态是 `release_gate.py --raw-track-id <同一串> --status abandoned`; 脚本与 `phase1_gate.py` 同目录。)」
- `old_skill` 引的 `linked-issue-field-availability` / `E0` / 「2026-09-01 B8 位置裁定」出自同一 SKILL.md 的**既有段落** `:420` 与 `:426` (逐字「**位置不影响机械判定** (裁定 2026-09-01 B8): check 按 E0 取**文档序第一条** depth-1 命中」), 不是本次新增块 —— 两臂都能合法拿到, 它既不构成任一臂的污染证据, 也不构成反证。

**残余风险 (点名, 不改判定)**: 评测跑在真实工作树里, `/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 就在旁边, 且逐字含同一批结论 (`:104` 的 `--raw-track-id "<spec-slug>-<container_uuid>"`; `:111` 的「任何非空字符串都 truthy」; `:446` 的 `release_gate.py --raw-track-id "<该方向 A.1 原串>" --status abandoned`; `:450` 的「**release 旧 + acquire 新**两步」)。本次只有 `answer.md`、无 transcript, 因此**产物侧无法证明未读**。可给出的最强反向证据是: proposal 独有的 token (`SC-14` / 「R6 接缝 C1/C4」/ 「rework v3」/ 「editlist FIX-」/ 具体 `lib/*.py:行号`) 在两臂中**一个都没出现**, 而这类标记在真读过该文件时极难全数不外泄。结论按证据强度写作「**未见污染**」, 而非「已证明无污染」。
