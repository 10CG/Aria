# GRADER_CRITIQUE — eval-3 readme-sync-detection (rep2)

prompt: `检查项目状态，特别注意文档版本是否一致`
断言 3 条, 两臂得分: 3/3 vs 2/3 (唯一差异落在断言 2「CHANGELOG 作为日期同步参照源」)。

---

## 0. 定向问题 —— `📝 README 同步状态` 区块

`references/output-formats.md:63` 规定的规范区块名是 **`📝 README 同步状态`**, 位置在 `🔧 自定义检查` 与 `📦 插件依赖状态` 之间, 内含 6 个维度: 主项目版本号 / **主项目日期** / 子模块版本号 / Skill 数量 / Skill 列表 / Plugin badge。

**两臂都没有输出这个区块名。** 逐臂:

| | with_skill | old_skill |
|---|---|---|
| 有无字面 `📝 README 同步状态` | ❌ 无 | ❌ 无 |
| 实际标题 | `### 📝 README 版本一致性（本次重点）` (第 106 行) | `## 📝 文档版本一致性 (专项 — 你重点关注的部分)` (第 113 行) |
| 层级 | `###` 三级, **嵌在 `## 🔄 同步状态` 之内** | `##` 二级, 独立顶层区块 |
| 位置 | 🔧 自定义检查 → 🔄 同步状态 → **(README 子节)** → 📦 插件依赖 | 🔧 自定义检查 → **(README 专项)** → 🔄 同步状态 → 🌐 多远程 → 📦 插件依赖 |
| 与规范位置的距离 | 差一层级 + 被降为 同步状态 的附属 | **位置与规范顺序一致** (紧接 自定义检查 之后), 只是改了名 |
| 6 个规定维度覆盖 | 版本号 ✅ / badge ✅ / 日期 ⚠️「本轮未检测」明写 / Skill 数量 ❌ / Skill 列表 ❌ | 版本号 ✅ / badge ✅ / 日期 ❌ 完全缺席 / Skill 数量 ❌ / Skill 列表 ❌ |
| 引 readme collector 字段 | `readme.submodules.aria` (readme_version=plugin_version=1.69.1, version_match:true) + `readme.root` (`version=null`) | `readme.version_match=true` + `readme.root.version` 采集为 `null` |

两臂**都**明确点出「root README 的 `version=null` 是零证据、不能当正证据」这一点 (with: 「⚠️ **无证据（不是「一致」）**」; old: 「readme collector 在 root 这一层是零信息的, 不要把它的沉默当正证据」) —— 这个正确判断两臂等价, 断言完全没覆盖。

**规范本身的问题**: snapshot 的 `readme` 段只有 `{root:{exists,version}, submodules:{aria:{plugin_version,readme_version,version_match}}}` 两类字段 (两臂 snapshot 逐字节同构), 而 output-formats.md 规定的 6 个维度里 **日期 / Skill 数量 / Skill 列表 三个根本没有 collector 宿主**。也就是说规范区块**结构上不可能被完整产出**, 只能靠 AI 从 custom_checks 侧拼。两臂都自然地改用了「版本一致性」这个能被数据支撑的标题 —— 这更像规范与数据面脱节, 而不是两臂各自跑偏。

---

## 1. 恒真 / 恒假断言

**断言 3「Should output readme_status section」≈ 恒真, 且措辞与任何真实标识符都对不上。**
- prompt 直接说「特别注意文档版本是否一致」, 任何及格回答都必然给一个 README/版本一致性专节 ⇒ 区分力接近 0。本轮两臂各自都给了, 且都不是规范名。
- `readme_status` 这个串在 schema 里不存在 (真实字段名是 `readme`), 在 output-formats.md 里也不存在 (真实区块名是 `📝 README 同步状态`)。按 GRADER_INSTRUCTIONS「特定字符串形态要真的出现」的严档读, **两臂都该判 false**; 按「有没有 README 状态专节」的行为档读, **两臂都 true**。两种读法下都是 0 区分力, 只是把恒真翻成恒假。**建议改写**为可证伪且钉字面的版本, 例如「输出中必须出现字面 `📝 README 同步状态` 作为区块标题」—— 那样本轮两臂会齐刷刷 fail, 反而是有信息的 (它会暴露上面那个「规范区块不可完整产出」的真问题)。

**断言 1「README.md version against VERSION or plugin.json」≈ 恒真。** 数据面上 `readme.submodules.aria.version_match` 与 6 条版本类 custom check 全在 snapshot 里摆着, 而 prompt 又点名要查版本一致性; 任何会读 snapshot 的臂都会命中。本轮两臂都以表格形式给全。它测的是「有没有读 snapshot」而非「技能差异」。

**断言 2 是三条里唯一真有区分力的**, 但它区分的东西存疑 —— 见下节。

**没有恒假断言。**

---

## 2. 断言未覆盖的重要臂间差异

按重要性排序:

1. **「日期维度没有代码宿主」这一诊断, 只有 with 臂做出。** with 臂不但答了 CHANGELOG 是参照源, 还指出 `collectors/readme.py` 只产 `version` 不产 date、schema `readme` 段也无 date ⇒ 「`readme_date_mismatch` 这条规则现在恒不触发」, 并给了两条处置 (补 collector 字段 / 降级成 custom check) + 建议开 issue。old 臂全文 **0 次**出现「日期」二字, 等于把「没测」隐式呈现成「没问题」。断言 2 只问「有没有提 CHANGELOG」, 测不到这层「假绿识别」的差距 —— 而这恰恰是本 eval 名义上最该测的能力。
2. **old 臂独有: PRD v2 Status 归一漂移。** old 臂发现 `prd-aria-v2.md` 的 Status 行原文是 `Approved (Draft → Approved 2026-04-11…)` 但归一化成 **pending** (substring shadow), 引 `references/status-field-guide.md §lifecycle-head` 给了修复写法, 并把它归入「同族一致性问题」。这是一条 with 臂完全没有的**真实增量发现**, 断言零覆盖。若只看断言分, old 臂 2/3 看起来更差, 但它多交付了一个可执行的文档缺陷。
3. **old 臂独有: aria-orchestrator github `no_local_tracking_ref` 的规则级解读** —— 明写「evidence_grade=fresh 因此**不触发** `has_unpublished_branch` 规则 (该规则要求 evidence_grade != fresh)」, 并给出 push 命令。with 臂只写「(feature/m6-cost-model-telemetry, 另一轨)」一笔带过。
4. **old 臂独有: 14 条 custom check 逐条列名**; with 臂只给「14/14 ✅ 全绿」聚合数。对「版本一致性」这个主题, 逐条列名的可核验性明显更高。
5. **with 臂独有: 「Skill 变更 detected=false ≠ 没有 Skill 变更」的主仓 diff 视角澄清** (真实 SKILL.md 改动在 aria 子模块 feature 分支, 主仓只看到 gitlink)。old 臂只写「未检出 SKILL.md 变更 → 本次不触发 Rule #6 AB 区块」, 没有点破这个盲区。
6. **with 臂独有: 明确指出「这些一致都是相对旧世界 1.69.1 成立」并把发版同步面整批列出**; old 臂也讲了这点 (限定条件 2), 且额外挂了 Aria#177「发布同步面那行是漏同步面的类级根因」。两臂在这个维度接近, old 略详。
7. **共有但断言未覆盖的高价值项 (两臂等价, 不产生区分)**: `issue_scan.open_count=47` 顶到 `limit=20` 的静默截断 (两臂都判「至少 47」)、三个 dirty 子模块是有意保留、`.aria/workflow-state.json` 非活跃中断、`collision.kind=self_multi_container` 即 Aria#193 身份漂移、本轮未调 `run_gate` / 未写 claim。
8. **推荐工作流的排序分歧**: with 臂把「仅状态检查, 到此为止」排 [1] (理由: 问的是状态), old 臂把「续做 a1-entry cycle」排 [1] (理由: handoff §6 第 1 优先级)。两者都合理但取向相反, 断言不覆盖。old 臂额外给了 AB run 的**可证伪验收方式** (transcript 里 `"push_skipped": true, "push_skipped_reason": "env_var"`, 见 false 则该 run 作废), with 臂只说要重启会话。

**方法论层面的关键警告**: 本批 (a1-entry) 对 state-scanner 的改动经核为 `SKILL.md` / `lib/{claim_lifecycle,collision,constants,identity}.py` / `scripts/{coordination_probe,phase1_gate}.py` / `references/layer-l-integration.md` / 五份测试 —— **`references/output-formats.md`、`references/rules/basic-rules.md`、`collectors/readme.py` 全部未被触碰**。也就是说本 eval 涉及的 README/日期/版本相关技能内容两臂**完全相同**, 断言 2 的臂间差异**不可能由本批改动导致**, 只能是采样噪声 (这也正是本轮复跑要诊断的东西)。建议: eval-3 在本批里应视为**噪声探针**而非区分力证据; 若要保留, 应把它标注为 control eval。

---

## 3. 仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 语料污染核查

**结论: 两臂都没有引用该目录下的文档。** 逐项核过:

- 两臂 answer.md 中 `grep -n "openspec/changes\|proposal\.md\|tasks\.md\|detailed-tasks"` **零命中**。
- 对 Spec 的提及仅止于 snapshot `openspec` 段能给的信息 (变更 id / approved / 活跃 / 归档数 / design_deferred 的 staleness 与勾选比)。
- 看似「像读了 tasks.md」的细节, 逐条溯源均在 **handoff** `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` 内, 而读 handoff 是技能明写步骤:
  - with 臂「TASK-036 (7.6) 的 `dependencies: [TASK-035]` 明写依赖 7.5 跑完」← handoff:54 「yaml `dependencies: [TASK-035]`, tasks.md 行尾也写着「按 Spec 它依赖 7.5 跑完」」(**注意: 是 handoff 在转述 tasks.md, 不是臂在读 tasks.md**)。
  - 两臂的「执行序 8.1 → 8.4 → 8.2」「`<vNEXT>` = 1.70.0」← handoff:55 / :176。
  - 两臂的「不是 Rule #6 豁免 / 本批改了 allowed-tools」← handoff:94。
  - old 臂「修复面 lib/failure_handlers.py + lib/coordination_ref.py:1339」← handoff:112 / :178。
  - old 臂「claim sweep 死线 2026-09-06T21:40Z」「先 fetch 再刷」← handoff §0 第 2 条 / :195 + aria-plugin#169。
  - with 臂引的 `rules/basic-rules.md §1.3` `readme_date_mismatch`、old 臂引的 `references/status-field-guide.md` **都是技能自身的 reference 文件** (已在 skill-snapshot 中实见), 非 Spec 语料。
- **残留污染通道 (非本 eval 独有, 但要记账)**: handoff 本身逐字包含了 tasks.md 的 `dependencies` 字段、Group 8 执行序、Rule #6 照跑判词。这些是 in-flight Spec 的内容经 handoff **二次落地**到两臂共同输入里的。它对本 eval 的三条断言无影响 (都不涉及这些), 但对同批其他 eval (尤其涉及 Rule #6 / 认领 / 发版顺序的) 构成 `ab-baseline-leaks-via-co-landing-docs-and-repo-corpus` 那条已知形状的通道: **两臂读同一份 handoff ⇒ 基线臂免费获得目标行为的知识**。建议在本批的结论里对「AB 输入含 in-flight handoff」做一次统一声明。
