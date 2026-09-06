# GRADER_CRITIQUE — eval 3 readme-sync-detection (**重评, 覆写前一版**)

> 本文覆写 23:25 那一版。前一版评的是**已被覆盖的答卷** —— 两臂的 `answer.md` mtime
> (with 23:33:46 / old 23:29:09) 都晚于当时的 grading (23:24), 故两臂全部从头重评、同批同尺。
> `old_skill/grading.STALE.json` 未读、未参考、不参与计分。
>
> 复评实测的**当前**答卷体量: with 259 行 / old 236 行 (REPEAT_NOTE 里的 "318 vs 258" 是旧答卷的数, 已失效)。

| 断言 | with_skill | old_skill |
|------|-----------|-----------|
| A1 README.md version vs VERSION / plugin.json | ✅ | ✅ |
| A2 CHANGELOG 日期作为 date sync 的参照源 | ✅ (边界判定, 见下) | ❌ |
| A3 输出 readme_status 区块 | ✅ (语义判定) | ✅ (语义判定) |
| **合计** | **3/3** | **2/3** |

---

## 特别问题 — with 臂有没有输出 `📝 README 同步状态` 区块?

**没有。实测 `grep -c "README 同步状态"` = 0。**

而且**old 臂 (当前这份答卷) 同样是 0**。REPEAT_NOTE 里记的 "with 0 次 / old 1 次" 是对**上一对**
答卷 (old 被重复派发前那份) 的测量, 对当前这一对**不再成立**。也就是说: 就这一对答卷而言,
「丢失规定区块」不是 with 臂独有的行为, 两臂都丢, 该差异**不构成回归证据**。

### with 臂把 README 三项放在哪里了

放在自造标题的区块 `📝 文档版本一致性 (你特别关注的部分)` (answer.md:109-153) 里 —— emoji 沿用 📝,
位置也在 output-formats.md 规定的槽位 (自定义检查之后、插件依赖状态之前), 只有标题被换掉。三项落点:

| output-formats.md 规定项 | with 臂落点 | old 臂落点 |
|---|---|---|
| 子模块版本号 (plugin.json vs aria/README) | :113 `✅ aria 子模块: plugin.json 1.69.1 == aria/README 1.69.1 (version_match=true)` | :123-124 `✅ SOT aria/.claude-plugin/plugin.json 1.69.1` / `✅ aria/README.md 版本行 1.69.1` |
| Plugin badge | :114 `✅ 主仓 README badge: Plugin-v1.69.1, 与 plugin.json 一致` | :125 `✅ 根 README.md Plugin badge 1.69.1` |
| 主项目版本号 | :116 `✅ 主项目 1.7.5: 9 个引用点全部一致` | :130-131 `【2】主项目 Aria = 1.7.5` |
| 主项目**日期** (来源 CHANGELOG) | **无该项**; 仅在实读复核里带出 `README.md (… Released 2026-09-04)` / `CHANGELOG.md 首个条目 [1.69.1] - 2026-09-04` (:118-119) | **完全没有** |
| **Skill 数量** | **两臂都没有** | **两臂都没有** |
| **Skill 列表** | **两臂都没有** | **两臂都没有** |

结论: 丢的不只是标题。规定区块的 6 项里, **两臂都只覆盖 3 项** (子模块版本号 / Plugin badge /
主项目版本号), 都丢了 Skill 数量与 Skill 列表两项; 主项目日期只有 with 臂以副产品形式带到。
两臂各自补了规定区块**没有**的东西 (with: `readme.root.version=null` 的零证据论证 + standards
版本矛盾 + tag 现实; old: i18n / 架构文档 / plugin-cache 六处齐平表 + CLAUDE.md 2.0.0 轴 + POINTS
清单覆盖面盲区)。

---

## Q1 — 有没有恒真 / 恒假的断言?

**A3「Should output readme_status section」两个方向都失效, 是本 eval 最该改的一条。**

- 按**语义**读 (「有没有一个专门报告 README 同步状态的区块」) ⇒ 两臂都 pass = 恒真。本 prompt 原文
  就是「特别注意文档版本是否一致」, 任何不跑题的回答都会有这么一段, 该断言等于在测「有没有回答问题」。
- 按**字面**读 (「必须出现 output-formats.md 规定的 `📝 README 同步状态`」) ⇒ 两臂都 fail = 恒假。
- 两种读法 delta 都是 0。**它恰恰是 REPEAT_NOTE 想用来判定「区块遗漏是否回归」的那条断言, 而它测不到区块遗漏** ——
  区块在不在, 它的取值都不变。要能测, 断言必须钉死字符串形态, 例如
  「输出中出现标题行 `📝 README 同步状态` (逐字)」并另立一条「该区块含 Skill 数量与 Skill 列表两项」。
  我按语义读判两臂 pass, 并在两份 `grading.json` 的 evidence 里逐字写明了「标题不是规定的那个」,
  下游不会被这个 pass 误导。

**A1 在本仓当前状态下接近恒真。** 版本一致性的判定材料 (`readme.submodules.aria.version_match=true`、
`m6-version-badge-match: OK badge=1.69.1`) 就在两臂都拿到的同一份 `state-snapshot.json` 里, 照抄即可 pass;
它测的是「有没有转述 snapshot 字段」, 不是「会不会做 README↔SOT 核对」。

**A2 是本 eval 唯一真正分开了两臂的断言 (1 pass / 1 fail), 但它的区分力是脆的**: 当前仓里
README 的 `Released 2026-09-04` 与 CHANGELOG 首条目日期**相同**, 没有漂移可报, 所以断言实际奖励的是
「有没有额外去手读那 5 个发布同步面文件」这种**篇幅/勤勉度**, 而不是技能文件里的日期同步逻辑。
造一个日期真漂移的 fixture 才能让它测到该测的东西。

**A2 的判定边界 (我把标尺写在这里以便复核)**: with 臂**从未**把 CHANGELOG 称作日期的「来源 / 权威」
(output-formats.md 里的形态是 `期望: 2026-03-18 (来源: CHANGELOG.md)`), 那一整段自述的核对维度是
版本号 (「也全部 1.69.1」), 两个日期是括注。我采用的标尺是「README 日期与 CHANGELOG 日期**成对给出并核为相同**
即算 date sync」—— 若只出现 CHANGELOG 日期而不与 README 日期配对, 按此标尺仍判 fail。换成更严的
「必须显式指认 CHANGELOG 为参照源」标尺, with 臂应判 **false**, 此时该 eval 变成 with 2/3 vs old 2/3, delta = 0。
这一条是本次两臂分差的**全部**来源, 复核者若不同意此标尺, 结论会翻。

---

## Q2 — 断言完全没覆盖的重要差异

**【1】最重要的一条: 两臂对「文档版本是否一致」给出了相反的结论, 而没有任何断言在测这个。**

- old 臂: 「**当下三条版本轴全部一致, 零漂移**」(:1)、「文档版本当下一致, 无漂移」(:234)。
- with 臂: 「**但有一处真的不一致**」—— root `VERSION` 的子模块表写 standards **v2.2.3**,
  `standards/openspec/project.md` 头部写 **2.2.2** (:123-133)。

我独立核过, with 臂是对的: `VERSION:25` = `| standards | v2.2.3 | …`,
`standards/openspec/project.md:3` = `> **Version**: 2.2.2`。两值在两臂的 `state-snapshot.json` 里
**都取不到** (`2.2.3` 命中 0 次), 只能靠实读文件才发现 —— 即 old 臂对用户 prompt 的正面回答是错的。
本 eval 三条断言全部只看「有没有做某类核对」, 没有一条看「结论对不对」, 于是这个最强区分点
(一臂答对、一臂答错) 计分为 0 差值。**建议补一条结论级断言** (例: 「不得在 standards 版本二写并存
时声称零漂移」), 这类负向断言正好是标尺里明确支持的形态。

**【2】with 臂独有的第三个维度: 文档自洽 ≠ git 现实。** :143-147 指出 root VERSION 的
`## 对应 Tag` 写 `v1.7.5` 而实际最新 tag 是 `v1.5.0` (共 7 个)。我核过属实 (`git tag | wc -l` = 7,
最新 v1.5.0)。**但要打折**: `VERSION:36` 本身就写着「⚠️ 实际 git tag 最新为 `v1.5.0`」, 所以这是**读到**
而非**推出** —— with 臂自己也如实说了「VERSION 文件自己已经写明这点」, 没有冒功。

**【3】两臂都命中、也都没被计分的一个共同好行为**: 都识别出 `readme.root.version = null` 是
「**没有输入**」而不是「通过」, 并都指出根 README 的守卫实际落在两条 custom check 上
(with :135-141「零证据不等于正证据」; old :137-144「这两条一旦被禁用或改名 … 将没有任何信号」)。
这是本 eval 语义上最贴题的判断, 三条断言一条都没测。

**【4】old 臂独有、未被计分的产出**: (a) PRD Status 归一化缺陷 —— `Approved (Draft → Approved …)`
首段同含 draft/approved 两 token, 被机械归为 pending, 并给出 status-field-guide 的修法 (:41-47);
(b) 把 CLAUDE.md 2.0.0 作为第三条版本轴纳入版本区块 (with 臂只在自定义检查里带过);
(c) 列出**未触发**的降级规则 (readme_outdated 1.3 / multi_remote_drift 1.35 / submodule_drift 1.97)
作为「一致」结论的机械依据 (:226-227) —— 把「没报警」显式当证据陈述, 是值得测的行为。

**【5】with 臂独有、未被计分的产出**: (a) Rule #6 补注 ——
`changes.skill_changes.detected=false` **不等于**本 cycle 无 Skill 变更 (改动已提交在 aria feature
分支 ab3dbd0, 机械层看不到) (:28-32); (b) 未跑 A.1 heartbeat 的取舍论证 (:195-200);
(c) 明确列出「不推荐现在做」的两件事及理由 (Rule #10 改序) (:240-246)。

**【6】两臂的 issue 计数截断判断强度不同**: old 说「上面的 47 应读作『≥47』」, with 说
「这个 47 不可信为总数 … 上次 handoff 实测四仓合计 65」。都对, 但 with 给了对照值。无断言覆盖。

---

## Q3 — 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**只有 with 臂点名了该目录下的文件, 但证据不足以判定它真去读了那份文件; old 臂一处都没点名。**

- with 臂 :241-242: 「TASK-036 (7.6 套件缺口 issue): **detailed-tasks.yaml 写着 dependencies: [TASK-035]**,
  7.5 未跑完就开 = 改序, 属 Rule #10 不得自行豁免的范畴。」—— 这是两臂里**唯一**一处按文件名引用
  change 目录产物的地方。
- **反证 (为什么不能据此判定污染)**: 两臂都自述读了 `docs/handoff/2026-09-05-2200-a1-entry-…md` 全文
  (with :17「已读, §6 入口指引已纳入」; old :191「✅ 已读取全文」), 而该 handoff `:54` **逐字**写着
  「yaml `dependencies: [TASK-035]`」, `:109` 再写一次。with 臂那句话的**全部信息**都在 handoff 里够用。
- 我对两臂答卷里所有能想到的 change-dir 特征串做了穿透核验 —— `TASK-035` / `TASK-036` / `TASK-038` /
  `1.70.0` / `16 版本点` / `Group 7`·`Group 8` / `8.1→8.4→8.2` / `7.6` / `六个套件` / `PREDICTION` /
  `push_skipped` / sweep 死线 `21:40` / `#173`「证据越少越宽松」—— **全部在 handoff 里命中**;
  同时 `TASK-035` / `TASK-036` 在两臂的 `state-snapshot.json` 里**命中 0 次** (说明来源确实不是 snapshot)。
  也就是说, 本 eval 里 change-dir 内容对两臂**经 handoff 这一条通道等量可达**, 没有任何一臂拿到了
  另一臂拿不到的语料。
- **另一条真实存在的仓内语料通道 (与 change dir 无关, 但影响解读)**: with 臂的 [A][C] 用到了
  `VERSION` / `standards/openspec/project.md` / `git tag` 的实读值 (`2.2.3` / `v1.5.0` 在 snapshot 中
  命中 0 次), 属 `ab-baseline-leaks-via-repo-corpus` 说的仓内语料面, 但这是**回答用户问题所需的实读**,
  不是从在制 Spec 抄行为。
- **对结论的影响**: 两臂 Group 7/8 的推荐细节 (发版序、vNEXT=1.70.0、依赖阻塞) **不能算作技能文件行为的证据** ——
  它们的来源是 handoff, 两臂共享。本 eval 剩下真正由答卷自身产生的差异, 就是 Q2【1】那条结论对错,
  而它恰好不在断言里。**没有 transcript, 「点名文件」≠「读了文件」, 故本条只能报「with 臂点名、
  不能判定实读」, 不宜升级为污染判定。**
