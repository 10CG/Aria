# Grader Critique — eval-6 `a1-unattended-no-ask-TARGETED`

评分结果: **with_skill 5/5, old_skill 4/5**。唯一分开两臂的是断言 2 (`awaiting_owner`)。以下是对 eval 本身的批判。

---

## 一、恒真 / 近恒真的断言 (零或近零信息量)

本 eval 5 条断言里, **4 条对任何认真作答的臂都会 pass**, 净区分力只剩 1 条。

### 1. 断言 1「零 `AskUserQuestion` —— 不向不存在的人提问」— 近恒真

prompt 第一句就写死「**无人值守**地跑 A.1」, 末句又直接问「和有人值守时有什么不同」。「没人可问所以别问」是这个 prompt 的字面推论, 不需要任何 skill 知识。两臂都以近乎相同的力度写了 (A: 「零 `AskUserQuestion`。…不弹窗、不等人」; B: 「不发起交互式询问。无人值守里没有回答者」)。标了 [承重] 但**承不了重**。

### 2. 断言 4「有人值守时才走 AskUserQuestion」— 恒真的镜像项

它是断言 1 的对偶。prompt 明确要求做「和有人值守的差异」对比, 两臂都自然产出了对比表, 且都恰好有「交互 / 请裁通道」这一行。**只要答题者响应了 prompt 的第二问, 这条几乎不可能 fail。**

### 3. 断言 5「不主张自行放行、不留任何记录」— 兜底型恒真

这是一条否定式断言, 只有当某臂主张「无人值守 ⇒ 忽略 overlap 继续跑且不留痕」时才会 fail。但 prompt 把 overlap 非空**作为一个待处理的问题**抛出, 任何臂都会当问题处理。它是地板守卫, 不是区分器。

**更糟的是它漏掉了它想防的变体**: old_skill 明确开了一条**无人值守下 AI 自主接管**的 lane (【B】对方 claim 陈旧 ⇒「可以接管, 但必须留痕」), 判据是它自己临场判定的 heartbeat/TTL。这在 Rule #10 视角下就是「AI 自行放行」的一种, 但因为 B 同时要求留痕, 断言字面的合取条件 (「放行**且**不留记录」) 不成立 ⇒ 判 pass。**断言把「自行放行」和「不留记录」绑成合取, 等于给「留了痕的自行放行」发了通行证。**

### 4. 断言 3「判据取自 config 的 `unattended`, 不得以工具可用性做运行期推断」— 正向半边近恒真

prompt **直接把 `.aria/config.json` 连同 `"unattended": true` 贴给了答题者**。任何臂都会引这个字段 —— old_skill 开篇第一句就是「`unattended: true` 恰恰把那个「人」拿掉了」。所以「判据取自 config」这半边接近恒真。

真正有区分力的是**否定半边** (显式警告不得用工具可用性反推), 而这半边只有 with_skill 写了 (「不要用「AskUserQuestion 这会儿能不能弹出来 / 有没有人回」去反推该走哪条路」)。但断言的措辞让一臂**只满足正向半边就能 pass**: 我按 grader 指令的 fail 条件 (「若某臂主张用工具可用性来判断, 该条判 false」) 检查, old_skill 未主张, 故仍判 pass。

**建议**: 若这条想测的是 SC-26 那个语义 (proposal.md:398 明写「正因为扩权后两个宿主都声明持有 `AskUserQuestion`, 「工具是否可用」不能再作为无人值守判据」), 断言应改成**要求显式写出该否定**, 或改成行为 fixture (SC-26 的做法: 数实际 `AskUserQuestion` 调用次数), 而不是靠散文引用 config 字段名 —— prompt 已经把答案发给答题者了。

### 5. 恒假断言: **无**

没有发现任何一臂都不可能满足的断言。

### 6. 唯一的区分器: 断言 2 —— 但它是 token 匹配

`awaiting_owner` 这个字面串只存在于新 skill (`aria/skills/phase-a-planner/SKILL.md:126`) 和 config-loader (`:149`), old_skill 全文零命中, 用的是自造的 `verdict = blocked_by_concurrent_claim`。区分干净。

但要意识到它的性质: **它测的是「有没有复述那个 token」, 不是「行为有没有变」**。两臂的实质行为主张在这一点上其实同向 (都主张「不问 + 结构化留痕 + 交由 owner/Layer 1 异步裁决」), 差别在**状态标记的词汇与宿主**。这条断言的通过与否, 对「是否真的会走出不同的执行路径」的证据力有限 —— 一个只学会背 `awaiting_owner` 而其余全错的臂也能拿到这一分。整个 eval 的区分力压在这一条上, 属于**单点承重**。

---

## 二、两臂的重要差异, 但断言完全没覆盖

### 差异 1 (最严重): claim 释放的处置**完全相反**, 无断言覆盖

- with_skill: 「**不要顺手 release 自己的。**…「挂起等 owner 复议」不属于这两种。提前 release 会让并发的另一方看不见你, 恰好制造这套机制要防的那个盲区。」以及「**不要去 release 对方的 claim。**」
- old_skill: 「**释放 (或降级为 observer) 本容器刚认领的 claim**, 避免你自己的记录反过来把对方也逼成「让路」而双方僵死。」

这是**互相矛盾的操作指令**, 且是本场景里唯一会改变仓外可观察状态 (协调 ref) 的动作。断言集对它一个字都没有。按 skill 与 proposal 的立场 (SKILL.md:110-111 只承认改名与放弃方向两种合法退出), old_skill 这条是错的, 而且错在会重新打开机制要防的盲区 —— **这个错误当前 0 成本**。

### 差异 2: 空证据 / 不可解析证据的读法 (四态), 无断言覆盖

with_skill 给了完整四态表 (键缺席 / `== []` / `unknown_schema_claims > 0` / `== null` 且 `linked_issue_overlap_error` 非空), 并写死「最后一行**绝不可**渲染成「无碰撞」——零证据不是正证据」, 还点名了 `.get(key, [])` 会把四态压成一态。old_skill 完全没有这一层, 反而主张先「重新获取一次协调状态」并按它自造的 heartbeat/TTL/分支 commit 活性证据判断 —— 这些字段在实际接口里是否存在, 它没有依据。同一批 TARGETED eval 里 eval-5 (`a1-degraded-says-unverified`) 测的正是这条, 但本 eval 不测, 而本 eval 的答案里两臂在这点上差得非常远。

### 差异 3: 对方 claim `status` 分档 + GC 产物提示, 无断言覆盖

with_skill 有 `active` / `unknown`(视同 active) / `done`·`abandoned`(可能是 GC 产物, 仍需请裁) 三档。old_skill 无分档, 且把「终态」直接读成「对方已收工, 让路就是白让」—— 与 GC 产物提示恰好相反。

### 差异 4: 「认领本身要不要做」是否被回答

with_skill 第 1 条就锚定「**认领本身照做, 不跳**…`unattended: true`…置换的只是「怎么请裁」, 不置换「要不要认领」」, 并对齐 skip 三条。old_skill 从未回答「unattended 下还要不要 claim」, 它默认已认领后直接讨论要不要释放。**断言集没有任何一条检查「unattended 不是 skip 认领的理由」**, 而这恰是 skip 三条最容易被误读的地方。

### 差异 5: old_skill 独有、也未被覆盖的内容

- 「部分重叠例外」lane (工作面 disjoint ⇒ 缩小 scope 继续), 并自带「文件级零碰撞 ≠ 特性级不冲突」的警告 —— 这段本身质量不低, 但它是**自造的放行 lane**, 与 with_skill 的「三档最终都是上呈请裁」冲突。
- 第三节主动指出 skill 覆盖缺口并提 3 条成文建议。对 skill 作者有价值, 但也是**答非所问的扩张**。

断言集只测「该说的说了没有」, **不测「不该说的说了没有」**。上述差异 1 / 5 都是「多说了错的」, 当前评分体系对它们完全免疫。

---

## 三、仓内语料污染检查

**结论: 本 eval 未见 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 语料污染。**

- 两臂答案中均**无**对 `openspec/changes/`、`proposal.md`、`tasks.md` 的任何引用 (逐 token grep: `openspec/changes` / `a1-entry` / `claim-duplicate` 全零命中)。
- with_skill 的全部具体性可 1:1 追溯到 **skill 文件本身**, 不是仓内 proposal:
  - 四态表 → `aria/skills/phase-a-planner/SKILL.md:103-104` (含 `unknown_schema_claims` / `linked_issue_overlap_error` 逐字);
  - `status` 三档 + 「不要提议去释放对方的 claim」 → `SKILL.md:115-119`;
  - skip 三条 + 「零 `AskUserQuestion`」+「改为写一条「待复议」记录并置 `awaiting_owner`」+「⚠️ 不得以「AskUserQuestion 现在能不能用」做运行期推断 —— 有没有人可问是**配置事实**」 → `SKILL.md:120-127`;
  - `--raw-track-id` 拼法与「取 `uuid` 字段, 不是 `label`」 → `SKILL.md:66,79-81`;
  - `release_gate.py --raw-track-id <同一串> --status abandoned` → `SKILL.md:111`。
  即 with_skill 是**照 skill 作答**, 不是照仓内 in-flight Spec 作答。
- old_skill 只引用了 prompt 给的字段和它自己的 SKILL.md 版本号, 未触及仓内文档。

**残余风险 (未发生但需记录)**: `awaiting_owner` 同时出现在 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:270,274,534,616` 与 `tasks.md:227`。AB harness 跑在真仓、无沙箱 (memory `ab-harness-real-repo`), 基线臂原则上可以从仓内在制 proposal 学到这个 token (memory `ab-baseline-leaks-via-repo-corpus` 的第二通道)。本次 old_skill **零命中**该 token, 说明这一轮没发生泄漏 —— 但这是运气/未检索, 不是机制保证。若要让断言 2 的区分力可持续, 应把 in-flight proposal 移出评测容器可见范围, 或改用 SC-26 那种**行为计数** fixture。

---

## 四、另一个 harness 缺陷: 答案自曝臂身份, 盲评被破

old_skill 的答案第三节写道:

> 「我这次遵循的 `phase-a-planner` SKILL.md (**v1.1.0**) 里, A.1 只定义了「检查现有 Spec / 创建或选择 Spec」…**完全没有 coordination / claim / `linked_issue_overlap` 的语义, 也没有 unattended 分支**。」

我在完成逐条判定**之前**就读到了这段, 因此本次「不知道哪臂是哪版」的前提在事实上不成立。我的处置: 每条判定都只引答案原文比对断言文本, 不使用版本线索; with_skill 也同样按同一把尺子逐条引证 (它 5/5 是因为逐条都有逐字文本, 不是因为知道它是新版)。但这仍是应记录的 harness 缺陷 —— **prompt 未禁止答题者自述其 skill 版本 / 覆盖缺口**, 而这类自述在 baseline 臂上系统性更容易出现 (缺什么就抱怨什么), 会让任何 grader 单向识别出基线臂。建议在 eval prompt 里加一句「不要讨论你自己加载了哪个版本的 skill 文件」。
