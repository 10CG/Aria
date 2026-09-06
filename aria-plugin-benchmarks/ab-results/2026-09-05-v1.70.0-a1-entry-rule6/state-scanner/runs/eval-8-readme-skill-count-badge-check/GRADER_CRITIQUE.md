# GRADER_CRITIQUE — eval 8 `readme-skill-count-badge-check`

评分结果: `with_skill` 5/8, `old_skill` 5/8 (逐条完全同形: 1/2/3/4/6 pass, 5/7/8 fail)。
两臂输入可比: 两份 `state-snapshot.json` 逐叶比对只差 12 个时间戳字段 (`generated_at` 23:20:09Z vs 23:20:13Z 等), 无语义差异。

---

## 1. 恒真 / 恒假断言

### 恒假 (本仓状态下任何诚实回答都拿不到) —— 3 条, 占断言总数 3/8

**A7「Should report badge mismatch as warning severity」— 结构性恒假。**
本仓 `README.md:8` = `[![Plugin Version](https://img.shields.io/badge/Plugin-v1.69.1-blue)]`,
`aria/.claude-plugin/plugin.json` = `"version": "1.69.1"` —— **badge 根本没有 mismatch**, 两臂都只能报「一致」。
断言要求的是 mismatch 分支的严重度渲染, 而该分支在本仓语料里不可能被触发。
零信息量, 且是「假绿的反面 = 恒红」那一类。
**修法二选一**: (a) 改写成条件式「一致时须声明一致; 不一致时须标 warning」; (b) 造一个 badge 落后的 fixture 仓再测这条。

**A8「Should gracefully handle missing aria submodule (skip, not error)」— 结构性恒假。**
`aria` 子模块存在且已初始化 (snapshot `readme.submodules.aria.exists=true`), prompt 也没有任何理由让回答去讨论「子模块缺失」的降级路径。
两臂全文都没提, 而且**提了才反常**。同样零信息量, 属于「审的对象整个未产生」。

**A5「Should output skill_list_missing items at info severity level (not warning)」— 恒假, 而且与被测技能自己的 SOT 矛盾, 这条最该改。**
三重问题:
1. **没有代码宿主**: `skill_list_missing` 这个字段在管道里根本不存在 —— snapshot 里 `'skill_list_missing' in json` = False, `'skill_count'` = False; `aria/skills/state-scanner/scripts/collectors/readme.py` 的 `r.data` 只产出 `root.version` / `submodules.aria.{exists,readme_version,plugin_version,version_match}` 五个字段。断言在评一个采集端从未生产过的字段的严重度。
2. **与技能自己的输出模板相反**: `references/output-formats.md:75` 明写漂移态渲染为 `⚠️ Skill 列表: 缺失 3 项 (project-analyzer, agent-gap-analyzer, agent-creator)` —— **warning**; ℹ️ 只用在 `:69` 的 `ℹ️ Skill 列表: 完整` 与 `:77` 的 `ℹ️ Skill 列表: 无法解析`。也就是说**严格照 SOT 渲染的臂会被这条断言判 false**, 断言与被测物打架。
3. 两臂实际都用 ❌ 级呈现 (`with_skill`: 「❌ **不完整, 漏 2 个 (这是本次唯一的真问题)**」, 全文零个 ℹ️; `old_skill`: 「❌ 不完整，漏 2 条」), 无一落在 info 级 ⇒ 判定同为 false, 不区分。
**修法**: 先裁定 SOT 到底是 info 还是 warning (`output-formats.md:75` 与断言必须有一方改), 再让断言引 SOT 的字面渲染串; 在此之前这条只是噪声。

### 近似恒真 (区分力≈0, 但不算无效) —— A1 / A3 / A6, 部分 A2

A1 (aria/README 版本 vs plugin.json)、A6 (root badge vs plugin.json) 的答案**直接躺在 snapshot 与 custom check 输出里** (`readme.submodules.aria.version_match=true`, `m6-version-badge-match: OK badge=1.69.1`), 任何跑完 Step 0 并转述结果的臂都会 pass。A3 (数量比对) 与 A2 (排除 `user-invocable: false` 计数) 需要额外 grep, 略难一点, 但两臂也都做了。

**结论: 8 条断言里, 3 条不可达 + 4 条近乎白送, 真正有区分力的只有 A4 (列表完整性), 而两臂都拿到了 ⇒ 本 eval 当前的净区分力 = 0。** 这对回归臂而言是「无回归」的证据, 但它同时意味着这套断言即便真出现质量回退也未必抓得到 —— 下面第 2 节列的差异全在断言之外。

### 另一处设计陈旧

prompt 的前提 (「刚发布 v1.14.0, 新增 3 个 Skill」) 与 `output-formats.md` 的示例块 (`子模块版本号: 一致 (v1.14.0)` / `Skill 数量: 一致 (33)`) 同源, 说明这条 eval 是照 v1.14.0 时代的仓库状态写的; 现仓为 1.69.1 / 42 skills, 差 55 个 minor。两臂各花了开头一整段做前提勘正 (这是本 prompt 实际最强诱发的行为), 而**断言集里没有任何一条评「是否勘正错误前提」**。建议补一条 (且它天然可证伪: 回答里必须出现实测版本 1.69.1 且明说与 v1.14.0 不符)。

---

## 2. 断言完全没覆盖的臂间重要差异

### 2.1 事实正确性差异 (对 `aria/skills/session-closeout/` 的定性相反) —— 实测判 `with_skill` 对

两臂都注意到 `aria/skills/` 有 43 个目录但只有 42 个含 `SKILL.md`, 但解释相反:

- `with_skill`: 「`session-closeout/` 只有一个空的 `scripts/` 子目录、**没有 SKILL.md 且未被 git 跟踪** —— 是本地残留物, 不是 skill」「建议直接删掉本地这个空目录」
- `old_skill`: 「`session-closeout/` 只含 `scripts/`、**没有 SKILL.md**（是 `session-closer` 的脚本宿主，不是一个 Skill）」

实测: `ls -R aria/skills/session-closeout/` = 只有一个**空**的 `scripts/`; `git ls-files skills/session-closeout/` (aria 子模块内) 返回空 ⇒ 未跟踪; 且 `aria/skills/session-closer/SKILL.md:22` 写着 `supersedes session-closeout-internalization`。
⇒ `with_skill` 的定性正确, `old_skill`「是 session-closer 的脚本宿主」**是错的** (那个目录是空的, session-closer 不从它取任何脚本), 并因此给出了相反的处置暗示 (留着 vs 删掉)。断言零覆盖。

### 2.2 `old_skill` 输出了一条假阳性附加发现 —— 断言零覆盖

`old_skill`: 「但 `aria/hooks/host-docker-logout-guard.sh` 存在却**未在 hooks.json 注册**。不是 README 错，是有个脚本没接线」。
实测 **false**: `aria/hooks/hooks.json:37` = `"command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/host-docker-logout-guard.sh"`。
同段的计数也不准: 它写「注册了 6 条 entry / 5 个不同脚本」, 实际 hooks.json 有 7 处 `.sh` 引用、6 个不同脚本 (session-start-check / handoff-location-guard / secret-guard / secret-scan / submodule-gate-telemetry / host-docker-logout-guard)。
这是「多报一个不存在的缺陷」, 对 state-scanner 这种诊断型 skill 是真实的质量差异 —— 而 8 条断言里没有任何一条惩罚假阳性。

### 2.3 `old_skill` 有一条 `with_skill` 缺失的真实警示 (方向相反的加分项)

`old_skill`: 「⚠️ 计数不可信下限: config `issue_scan.limit = 20`，Aria 与 aria-plugin 恰好各报 20 = 顶到上限且无截断标记 ... 真实 open 数 > 47」。
`with_skill` 则把 47 当事实报 (「**47 条 open**」) 且无截断提示。这是「顶到 limit 的计数不能当总量」的正确识别, 同样零覆盖。

### 2.4 对「机械覆盖缺口」的处理深度不同 (两臂都有, 侧重不同)

- `old_skill` 的独有点: **来源披露** ——「上面 [1][2] 两项是我在 snapshot 之外**补测**的」, 并点出模板与采集端的矛盾 (`output-formats.md` 承诺 `Skill 数量`/`Skill 列表` 两行, 采集端从未生产)。这正好是 §1 里 A5 那条断言指向的洞。
- `with_skill` 的独有点: 给出**可落地的 fail-closed 判据三条** (实际⊄声称 → FAIL / 声称⊄实际 → FAIL / 三个数字不符 → FAIL, 并写明「三个判据缺一不可: 只比总数会被本次这种『总数对、列表少』骗过去」), 且要求**新检查先在基线亲跑三态** (「打补丁前应 FAIL ... 补完后应 PASS ... 人为删一行 bullet 应重新 FAIL —— 否则就是写了一条恒绿的假绿检查」)。

断言集对「是否发现并正确刻画这个 collector 缺口」没有任何一条 —— 而这恰是两臂都自发投入最多篇幅的地方。

### 2.5 修复路由建议实质不同

- `with_skill`: 单开 Level 1 doc-only 修复 (给出逐字补丁行与分类归属), 并提醒落点在 `aria` 子模块须本地 merge + 双推 + 逐 remote `ls-remote` 核验。
- `old_skill`: **不建议 drive-by**, 主张并入在制发版 Group 8 的 8.1 (理由: 8.1 本来就要改 `aria/README.md`, 且 8.1 卡在 Rule #6 AB 未跑)。

两者都成立但取向相反 (即时修 vs 并入在制序列), 对使用者的实际影响远大于任何一条现有断言。建议补一条评「是否与在制 cycle 的作业面冲突做了显式处理」。

### 2.6 溯源颗粒度

`with_skill` 给出两个漏列项的**引入时间与 commit** (`issue-triage` d2d7cb6 / 2026-05-13, `session-closer` 7801bd4 / 2026-06-25, 「漏了约 3.7 / 2.4 个月」) —— 实测两个 SHA 与日期**全部准确** (`git log --diff-filter=A`)。`old_skill` 只列名称与描述。断言未覆盖。

### 2.7 共有的同款小错 (不构成区分, 记录备查)

两臂都把 root `README.md` 的 `Plugin Version: 1.69.1 (aria-plugin, 42 Skills + 11 Agents)` 引成 `:242` (实际 **241**); `old_skill` 另把 `Project Version: 1.7.5` 引成 `:241` (实际 **240**)。同方向 +1 偏移。

---

## 3. 真实缺陷发现 (parent 点名要求)

**两臂都发现了 `aria/README.md` 的 skill 列表缺项, 且都点名正确 —— 这是本 eval 唯一的真区分性产出, 并且是真缺陷。**

独立机械复核 (我自己跑的, 不依赖任一臂):

```
bullets in aria/README.md 「### Skills」–「### Agents」 之间: 40
aria/skills/*/SKILL.md 目录数:                              42
missing from README: ['issue-triage', 'session-closer']
ghost in README:     []
```

即 README **标题数字 42 / 35 / 7 全部正确**, 内部 7 个 (`user-invocable: false`) 具名清单也逐个吻合 (agent-router / agent-team-audit / arch-common / audit-engine / config-loader / git-remote-helper / aria-token-telemetry), **但正文 bullet 只有 40 条** —— 33 user-facing + 7 internal。
两臂对这个「数量对、列表少」的形状都做了正确刻画:
- `with_skill`: 「计数行是手写的、与 bullet 数**不自洽** —— 数量核对**恰恰通不过**这个漏洞, 只有逐条比对目录才抓得到」
- `old_skill`: 「只核计数不核清单，这个漂移查不出来；反过来，如果当初是照清单去数的，计数早就该是 33 而不是 35」

漏列已存活 3.7 / 2.4 个月 (commit 日期已复核)。建议按两臂共同的提议开单: 给 `collectors/readme.py` 或 `.aria/state-checks.yaml` 补 roster 比对, 判据取 `with_skill` 给的三条 fail-closed 形式, 并按其要求先在基线跑三态。

---

## 4. 仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 语料污染

**结论: 两臂都没有引用该目录下的任何文档内容; 但两臂都读了同一 cycle 的在制 handoff, 那是同源语料的另一条腿。**

- 直接引用该 change 目录下 `proposal.md` / `tasks.md` 内容的: **无**。两臂出现 `a1-entry-claim-duplicate-work-guard` 都只是 snapshot 字段的转述 (`OpenSpec 关联: a1-entry-claim-duplicate-work-guard (approved)` / 活跃变更 7 个的枚举), 属合法扫描输出。
- `old_skill` 唯一一处点到 spec 文件名是**建议动作**而非引用内容: 「执行: 在 tasks.md / 8.1 清单里追加「aria/README skill 列表补 2 条」一行」—— 没有引 tasks.md 的任何字面。
- **两臂都从 `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` 取了在制内容**, 且都能在该文件里逐字对上:
  - `old_skill`: 「Group 8 发版三条的执行序是 **8.1 → 8.4 → 8.2**」← handoff `:55` 「**执行序 8.1 → 8.4 → 8.2**」; 「上次 handoff §3 第 1 条明确写着: AB 评测会话期间不要做真实 heartbeat / acquire」; 「本轨 sweep 死线 `2026-09-06T21:40Z`」← handoff `:195` heartbeat `21:40:06Z`。
  - `with_skill`: 「最新 handoff §0 明确写了这 3 个 dirty 子模块**是有意的**, gitlink bump 归 TASK-038/8.2」← handoff `:18` 逐字 「gitlink bump 归 TASK-038/8.2」; 「Rule #6 AB 仍未跑且不属豁免」「31/40」。
- 影响判断: 该 handoff 是**本 AB 跑本身所属 cycle** 的在制记录 (含 `<vNEXT> = 1.70.0`、Rule #6 AB 未跑等), 属 `ab_baseline_leaks_via_repo_corpus` 里「仓内在制文档」那条通道。对本 eval 的**被评面** (README skill 数/列表/badge) 无影响 —— handoff 里没有 skill roster 信息, 两臂的 A1–A6 结论都是自己实测的; 但它**确实塑造了两臂的「推荐工作流」段**, 尤其 `old_skill` 的「并入 8.1」建议几乎完全由 handoff 驱动。两臂访问权对等, 故不构成臂间偏置, 但如果后续要评「工作流推荐质量」, 这条通道必须先隔离 (评测仓内不放本 cycle 的 handoff)。
