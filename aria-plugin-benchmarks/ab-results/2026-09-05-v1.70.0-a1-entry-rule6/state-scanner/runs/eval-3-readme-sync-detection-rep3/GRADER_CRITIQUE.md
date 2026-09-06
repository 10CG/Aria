# GRADER_CRITIQUE — eval 3 `readme-sync-detection` (rep3)

评分结果: `with_skill` 3/3 · `old_skill` 2/3 (唯一分歧在断言 2)。

两臂的 `state-snapshot.json` 除时间戳/`scan_generation` 外**逐字节相同** (diff 仅 6 处
`age_seconds` / `last_fetch_at` / `generated_at` / `age_hours` / `fetched_at` / `generation_fetched`),
所以机械输入不构成差异来源。

---

## 1. 恒真 / 恒假的断言

### 断言 1「Should check README.md version against VERSION file or plugin.json」— 实质恒真

snapshot 的 `readme` 字段本身就直接给出了这个比对结果:

```json
"readme": {"root": {"exists": true, "version": null},
           "submodules": {"aria": {"plugin_version": "1.69.1",
                                    "readme_version": "1.69.1", "version_match": true}}}
```

外加 `custom_checks` 里现成的 `m6-version-badge-match` (badge vs plugin.json) 与
`main-project-version-consistency` (VERSION 的 9 个引用点)。也就是说, **任何把 snapshot
如实转述出来的回答都会 pass**, 而 prompt 又明写「特别注意文档版本是否一致」。零区分力。
若要让它有信息量, 应改成可证伪的更硬形态, 例如「必须报出 `readme.root.version = null`
并说明这个 null **不等于**版本漂移」—— 那样才区分「读懂 collector 解析形态」与「照抄 ✅」。

### 断言 3「Should output readme_status section」— 恒真, 且锚点不存在

两臂都开了 `### 📝 README / 文档版本一致性` 区块, 都判 pass。但这条断言的措辞是坏的:

- `readme_status` 这个串**在任何地方都不存在**: snapshot 的字段叫 `readme` (不是 `readme_status`),
  `output-formats.md` 里的区块叫 `📝 README 同步状态` (不是 `readme_status`)。断言指向了一个
  既非 schema 字段、也非输出区块名的幻影 token。
- 按 GRADER_INSTRUCTIONS「特定字符串形态…缩写、截断、同义替换都不算」的严格读法, **两臂都该 fail**
  (谁都没写 `readme_status`, 也没写规范的 `📝 README 同步状态`); 按宽松读法两臂都 pass。
  两种读法下都是零区分力, 只是把 0/2 换成 2/2。

建议改写成可机检的字面: 「输出必须含 `📝 README 同步状态` 区块标题」, 并同时把
output-formats.md 规定的行项 (主项目版本号 / 主项目日期 / 子模块版本号 / Skill 数量 /
Skill 列表 / Plugin badge) 写成逐条子断言 —— 见下面第 4 节, 这才是当前真正被两臂同时漏掉的东西。

### 断言 2「Should mention CHANGELOG date as reference source for date sync」— 唯一有区分力, 但它测的**不是本次 skill 变更**

这条 rep3 里 with 过 / old 不过。但必须点破一个方法论问题:

**两臂的 `references/output-formats.md` 逐字节相同** (实测 `diff ab-workspace/.../skill-snapshot/skills/state-scanner/references/output-formats.md aria/skills/state-scanner/references/output-formats.md` → 无输出)。
`期望: 2026-03-18 (来源: CHANGELOG.md)` 这行在 output-formats.md:261, **两臂都能读到**。
且当次会话的 handoff (`docs/handoff/2026-09-05-2200-…md`) 通篇不含 README/日期/CHANGELOG-as-date-source
的任何内容 (grep `README` / `最后更新` / `日期一致` 全部零命中), 所以也不是 handoff 喂的。

⇒ 这条断言度量的是「模型这一次有没有下钻到 references/output-formats.md 的
『README 日期不一致时』小节」, 是**注意力/采样差异**, 不是本轮 SKILL.md diff (Layer L A.1 heartbeat +
`push_skipped` / `linked_issue_overlap` 三态渲染) 造成的能力差异。作为**采样稳定性诊断**的 rep3, 这条
恰恰是最容易在 rep 之间翻面的一条 —— 它的 pass/fail 不应被计入「新版技能更好」的证据。

另有一个反向激励值得记下: snapshot schema 1.0 的 `readme` **根本没有 date 维度**, 14 条自定义检查里
也没有任何一条比对 README 日期 vs CHANGELOG 日期。也就是说「日期一致性」在当前系统里**结构上不可判定**。
一个严格只报可判定事实的回答会闭口不谈日期 —— 而它会因此 fail 断言 2。这条断言在奖励
「谈论一个系统还测不了的机制」。with 臂的处理方式 (报为**未核实** + 点名期望源应是 CHANGELOG.md +
建议加一条 state-check) 是正确解, 但断言本身没有把「不得把零证据说成一致」这个负向要求写进去 ——
一个只说「日期应以 CHANGELOG 为准, 已核对一致」的**编造式**回答同样会 pass。建议加负向断言:
「不得在无 date 字段的情况下断言 README 日期一致」。

---

## 2. 断言完全没覆盖的重要差异

按重要性排序:

1. **Layer L A.1 heartbeat 的显式声明 (with 有 / old 无)** —— with 臂单列一段:
   「**心跳: 本次未执行, 显式声明而非静默跳过。**」并给出未执行的成文依据 (AB 会话 `ARIA_COORDINATION_NO_PUSH=1`
   期间强制 fetch 会冲掉真 claim) 与死线余量 (~22h)。old 臂只在转述 handoff 时提到 heartbeat 时间戳,
   **没有把「本次入口应不应该刷心跳」当成自己的义务来交代**。这恰好是本轮 SKILL.md 新增段落
   (`### Layer L A.1 heartbeat 集成`, 含「静默等于『心跳从没跑过』, 二者必须可分辨」) 想要的行为 ——
   **本 eval 的三条断言一条都没测到它**, 而它才是真正的技能差异。

2. **零证据处置的方向相反** —— with 臂: 「⇒ 现在说『日期一致』是没有证据的; 我按『零证据不算正证据』
   如实报为**未核实**」「现在的绿是"没测", 不是"测过了"」。old 臂: 「**结论: 当前 8 个机械版本核对点全绿,
   未发现任何版本漂移**」「文档版本**是一致的**」—— 一个覆盖面完整性的断言, 但它从未检查过日期维度。
   这是 AB 里最值得量的一条差异 (覆盖 vs 结论的口径), 断言集完全没碰。

3. **old 臂在 `readme.root.version = null` 的根因上更硬** —— 这是 old 臂**赢过** with 臂的地方,
   同样没被覆盖: old 给出 collector 只认的三种形态 (`**版本**: x.y.z` / `## Version: …` /
   `> **Version**: …`)、根 README 的两处真实载体 (`README.md:8` badge + `README.md:241-242` 的
   `Project Version: 1.7.5` / `Plugin Version: 1.69.1`), 并推出「所以 `readme_outdated` 规则
   (priority 1.3) **未触发**, 是对的」。with 臂只说「没有可解析的 `**版本**:` / `## Version:` 行」,
   未给行号、未追到 badge 之外的第二处载体、也未讨论 rule 1.3。断言集只问「有没有比对版本」,
   量不到这层深度差。

4. **with 臂独有: PRD status substring shadow** —— 指出 `prd-aria-v2.md` 的
   `Approved (Draft → Approved 2026-04-11, …)` 因括号内含 `Draft` token 被归一成 `pending`,
   判为**读数失真而非阻断** (未满足 `prd_draft_blocking` 的 ≥5 Story 条件), 并给出修法
   (叙述移到 em-dash 之后)。old 臂只把原始串与归一结果并列, 不下判断。这与 prompt
   「文档一致性」同族, 但断言没覆盖。

5. **推荐工作流的可执行性差异** —— with 臂给了 4 项, 其中 [2] 直接把本 eval 暴露的缺口
   (加一条以 CHANGELOG 日期为期望源的 state-check) 变成动作, 并说明「不碰 aria 子模块, 不污染 [1] 的 AB 基线」;
   还给了验收 env 是否真进会话的可证伪判据 (`"push_skipped": true, "push_skipped_reason": "env_var"`,
   见到 false 该 run 作废) —— 后者正是本轮 SKILL.md 新增的 `push_skipped` 键。old 臂的 [1]-[4]
   没有这类闭环。断言没覆盖。

6. **两臂共同的漏项 (说明断言集偏松)** —— `output-formats.md:63-76` 规定的
   `📝 README 同步状态` 区块含 6 行: 主项目版本号 / **主项目日期** / 子模块版本号 /
   **Skill 数量** / **Skill 列表** / Plugin badge。两臂都**只做了版本 + badge 两类**,
   `Skill 数量` 与 `Skill 列表` 一个字没提。附带一个真实缺陷: snapshot schema 1.0 的 `readme`
   字段**根本没有** skill count / skill list / date 三个维度, 规范要求的 6 行里有 3 行
   **无数据宿主** —— 属 output-formats.md 与 collector schema 的规范漂移, 建议单独开单
   (与 memory `no-code-host-no-assertion` 同形)。

---

## 3. 有没有臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 的文档?

**没有。两臂都没有出现该目录下任何文件的路径引用** (grep `openspec/changes` / `tasks.md` /
`detailed-tasks` / `proposal.md` 于两份 answer.md → 全部零命中)。

看起来像「读了 Spec」的几处, 逐条追下来**都能在 handoff 里找到逐字出处**, 属 state-scanner
本来就该消费的 `docs/handoff/` 输入:

| 疑似点 | 出现在哪臂 | 真实出处 (逐字) |
|--------|-----------|----------------|
| `TASK-038 / 8.2` gitlink bump | 两臂 | handoff:18 「gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后」 |
| `7.6 (TASK-036)` + `dependencies: [TASK-035]` | old | handoff:54 「yaml `dependencies: [TASK-035]`, tasks.md 行尾也写着…现在开 = 改序 (Rule #10)」 |
| 执行序 `8.1 → 8.4 → 8.2` / `vNEXT = 1.70.0` / 主仓 16 版本点 | 两臂 | handoff:55 逐字 |
| 六个套件名单 + `PREDICTION.md` + 清理 fetch | 两臂 | handoff:53 逐字 |
| 「本批改了 `allowed-tools` = 能力面扩权, 照跑档」 | with | handoff:94 逐字 (`allowed-tools` 在 snapshot 里零命中, 只在 handoff) |
| 「31/40」「剩余 9 条」 | 两臂 | handoff:38 / handoff:86 |
| 「符合 Diff 9 期望值」 | old | 不是 Spec —— 是 `.aria/state-checks.yaml:112` 的 `fix` 文案, 已随 `custom_checks` 进 snapshot (实测 `'Diff 9' in snapshot == True`) |
| `期望: <date> (来源: CHANGELOG.md)` | with | `references/output-formats.md:261` —— **技能自带参考文件**, 两臂版本逐字节相同 |

**但这不等于本 run 没有仓内语料影响。** 污染通道换成了 `docs/handoff/` 而非 change 目录:
两臂都大段复述了 handoff 的 H1/H2/H3 与 Rule #6 论断 (「AB 仍未跑且不是豁免」「7.6 改序 = 违 Rule #10」),
这些是**本轨在制交付物的结论**, 不是技能能力。好消息是**两臂对称吃到同一份 handoff**,
所以它不制造臂间偏差; 坏消息是它把两臂的分数一起抬高, 压缩了区分度 —— 与 memory
`ab-baseline-leaks-via-co-landing-docs-and-repo-corpus` 记录的形状一致, 结论应拆成
「落地前已证 / ship 态边际未证」。

---

## 4. 给 eval 维护者的三条具体修改

1. 断言 3 改为字面可机检: 「输出含 `📝 README 同步状态` 标题」+ 拆出
   `Skill 数量` / `Skill 列表` / `主项目日期` 三条子断言 (当前两臂全漏, 且会顺带暴露
   schema 无宿主的真缺陷)。
2. 断言 2 补一条负向: 「在 snapshot 无 date 字段时, **不得**断言 README 日期一致 (须报未核实或点明零覆盖)」——
   否则编造式回答与诚实回答同分。
3. 本 eval 想量的若是**本轮 SKILL.md 变更**, 应新增一条针对 heartbeat 的断言 (例如
   「持 active claim 时须显式交代本次 heartbeat 执行与否, 静默跳过判 fail」)。
   现有三条断言与 SKILL.md diff **没有任何交集**, 全部落在两臂共享的 output-formats.md /
   snapshot 上, 因此 rep 间翻面风险高、对技能版本的归因力弱。
