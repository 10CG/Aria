---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:55:39.959Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [knowledge-manager]
---

# post_spec R5 — knowledge-manager 单席报告

被审对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, Aria#195)
席位透镜: 知识与文档一致性 (头部机械判据 / Rule #3 同步清单 / 与 conventions + CLAUDE.md 规则的冲突 / 术语与归档口径 / 引用真实性)
本轮只审不改, 未编辑任何仓库文件。

## 审计结论

### Decisions

- [decision] documentation/R4 缺陷落地核验: R4 的 1 critical + 10 major 全部落进正文而非批注 —— 11 个 finding id 在正文各命中 3-9 次, 落点实读确认为 §3 上报字段语义段 / §2.5 传播路径与裁定依据重写 / SC-13(c) / SC-16 夹具组成 / SC-15 (i)(j) + 第 4 条反事实 / Task 2.0a 前置门 / Task 2.2(c)(d) / rule6_note 前提句 (证据: `proposal.md:120-133,140-149,336,338,342-346,282,289,366-370`; 聚合报告 `.aria/audit-reports/post_spec-R4-2026-09-07T004500-000Z-R4-…-aggregated.md:38-99`)
- [decision] documentation/头部 `Linked Issue` 行机械合规: 实跑 `python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt` 返回 `OK (8 份在范围内, 6 条在册)`, 本 proposal 不在白名单 ⇒ 写法三条 (code span / 非链接形 / `>` 后一空格) 全过 (证据: `proposal.md:6`; `.aria/state-checks.yaml:382-405`)
- [decision] architecture/审计计划与 Rule #10 白名单适用成立: `proposal.md:13-14` 声称的 `post_brainstorm=off` / post_spec + post_planning convergence / 其余四检查点 off, 与 `.aria/config.json` 的 `audit.checkpoints` 逐字一致 ⇒ 属白名单第一类 (config 显式 off), 非 AI 自行豁免 (证据: `.aria/config.json` audit 段)
- [decision] documentation/Rule #6 判据表选行经 SOT 逐行核对成立: `skill-benchmark-exemption.md:20` 确为「`references/rules/*` 的 dispatch 表、判定规则 …… 与 SKILL.md 正文同性质」, `:22` 逐 hunk 原则, `:29` 第二行「照跑 AB, 零裁量」, `:31` 第四行「拿不准 ⇒ 照跑」—— 头部 `proposal.md:12` 的条件式落行 (4.5 落编辑 ⇒ 第二行, 否则第四行) 写法正确, 处置「照跑 + 开套件缺口 issue + 保留全部 substitute SC」符合 Rule #10
- [decision] documentation/外部引用抽样全部真实且逐字相符: issue 原文 `issue-195.md:21` (点名 `_get_file_commit_date`) / `:41` (A 案「`filename` / `track_id` 等需要 basename 的字段另行派生」) · `.aria/triage-comment-195.md:25` (「issue 未点名」) / `:53` (「`filename` 字段另派生 basename」) · 决策单 `:56-61` §落地约束四条, 第 2 条在 `:59`、第 4 条在 `:61` · `LEVEL_GUIDE.md:156-162` 跨模块四条判据 (满足任一) · 归档先例 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/proposal.md:3` 逐字命中且同目录确有三文件 · `state-snapshot-schema.md:46-48,1070,1156-1168` (末行 2026-07-19, 全文 1168 行) · `docs/handoff/latest.md:103-107` · `.aria/probes/main-project-version-consistency.py:39-49` POINTS 确不含插件版本行
- [decision] architecture/standards 侧基线未漂: Task 4.4 写死的 `21748d4` 仍等于 `git -C standards rev-parse origin/master` 与主仓 `git ls-tree HEAD standards` ⇒ 该条写死起点在今日仍成立 (与 aria 侧形成对照)

### Issues

- [major] documentation/`proposal.md:16` 基线复核块: 「触点零 diff、行号在 f314785 上继续有效」为假。实测 `git -C aria diff --stat 301641b f314785` 的 21 个变更文件里, 至少三个被本文逐行引用 —— `CHANGELOG.md` +25 行 (`:84` 的 1.70.0 先例 / `:93-97` Added 先例 / `:99-100` Amended 先例 已分别移到 `:109` / `:118-122` / `:124-125`, 而这三处正是 §6.5 与 SC-11(e) 的成文口径依据)、`skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py` +99 行 (SC-3 / SC-4 / SC-13 引用的 `_GIT_ENV` 由 `:174-183` 移到 `:176-184`, `GIT_CONFIG_GLOBAL/SYSTEM` 由 `:181-182` 移到 `:183-184`, 夹具日期由 `:380-382` 移到 `:382-384`)、`skills/phase-d-closer/SKILL.md` 两处改写 (`:218` 本身未移位, 属该文件唯一幸存的引用)。该块自己抄对了总量 (21 文件 / 895 增 / 63 删), 说明 diff 跑过, 但按文件过滤时用的「触点集」漏了这三个 (证据: `proposal.md:16`; `aria/CHANGELOG.md:109`; `aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:173,183-184`)
- [major] testing/`proposal.md:332` SC-10 第三类归因路径 + `:388` 待复议 8: 日历失效条款已成死条目, 且今天反过来卡住 Phase B。上游 f314785 已给该模块**每一个**调用点 pin `now=_FIXED_NOW` (`test_handoff_multibranch_collision_dedupe.py:173` 定义 `_FIXED_NOW = 2026-08-23T12:00Z`, `:276,327,363,388,436,483,547,642,683,729,783` 逐处传入), 而 301641b 上 `:386` 是裸 `collect_handoff_multibranch(root)`。本席今日 (2026-09-10, 已过 09-09) 实跑该模块 `Ran 23 tests … OK`, 五模块点名集 `Ran 104 tests … OK` —— SC-10 钉的「基线 `Ran 102 tests … OK`」与「2026-09-09 起自动转红 2 条」双双过时。后果两层: (a) 待复议 8 请 owner 裁的对象已不存在, 白占一个前置门; (b) SC-10 的硬句「基线须在 2026-09-09 之前取; 若已过该日, 先按 §待复议 8 的裁定处置再取基线」在今日字面成立 ⇒ Phase B 被一个已修好的缺陷锁死 (证据: `proposal.md:332,388`; `aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:173,388`)
- [major] documentation/`proposal.md:382-386` 待复议 6 (Task 2.0b 前置门): 候选版本号已作废但未同步。`:386` 逐字写「`git -C aria tag --list 'v1.7*'` 最高为 `v1.71.1`, 两个候选号 (`v1.71.2` / `v1.72.0`) 当前均未被占用」, 而实测 tag 集为 `v1.70.0 / v1.71.0 / v1.71.1 / v1.73.0`, `aria/.claude-plugin/plugin.json:4` = `"1.73.0"` ⇒ 两个候选号都**低于**当前版本, SemVer 单调下均不可用 (v1.72.x 更是从未存在过, `:16` 说「已被 v1.72.x 越过」也不准确)。`:16` 只把 PATCH 支顺延到 v1.73.1, 留下 `:382` 的推荐默认「MINOR / v1.72.0」与 `:386` 的实测句原样 —— owner 只读 §待 owner 复议 清单即会对死号签字, 而本条自述「级别一旦定错, Task 5.1 的 16 个版本点、tag、CHANGELOG 标题全部连坐」(证据: `proposal.md:16,382,386`; `aria/.claude-plugin/plugin.json:4`)
- [major] architecture/`proposal.md:10` Phase C 硬约束 + `:313` Task 5.2 + `:9` 基线冻结: gitlink 起点已被主仓越过, 三处未 neutralize。`:10` 逐字「本 spec 的 gitlink bump 起点是 `301641b`, 任何情况下不得把主仓 gitlink 回退到 `0545f86`」, `:313` 逐字「主仓 spec + gitlink bump **从 `301641b` 前进**」, 而实测 `git ls-tree HEAD aria` = `f314785` (v1.73.0) ⇒ 照字面执行即把主仓 gitlink 从 v1.73.0 回退两个版本。`:16` 虽提到「主仓 gitlink 已随之前进 (本地已 merge 到 `c115fd4` 并双推 MATCH)」(该 SHA 经核实存在且是 HEAD 祖先), 但没有在 `:10` / `:313` 处加任何 inline 标记, 而 `:9` 仍写「Phase B 在 `301641b` 起分支」是第二个未消歧起点。这正是 CLAUDE.md §多远程推送两条硬约束与 memory `feedback_sequenced_multirepo_gitlink_bump` 要根治的那一族 (证据: `proposal.md:9,10,16,313`; `git ls-tree HEAD aria` → `f314785`)
- [minor] documentation/`proposal.md:297` Task 5.1 机械兜底列 + References 闸门行: `.aria/state-checks.yaml` 三处行号已漂移 —— `m6-version-badge-match` 实为 `:124` (文写 `:88`)、`i18n-readme-translation-currency` 实为 `:177` (文写 `:141`)、`plugin-version-arch-docs-match` 实为 `:408` (文写 `:372`)。主仓文件不在 aria 基线冻结的覆盖面内, `git log --since=2026-09-05 -- .aria/state-checks.yaml` 有两次提交。影响有限 (三条 check 都给了名字, 可 grep 定位), 但与 `:16` 那句「全部行号继续有效」叠加会让读者误以为不必复核 (证据: `.aria/state-checks.yaml:124,177,408`)
- [minor] documentation/`proposal.md:315` Task 5.4 + `:333` SC-11(d)(h): Rule #9 的 D.3 handoff 无任务承接。Task 5.4 只列「归档 + `release_gate` claim 释放 + #195 关闭回帖」, 而 SC-11(d) 要求「本文 §6.3 与**本 cycle handoff** 各有一处『`reference-snapshot-aria.json` 未重采样』的显式 deferred 记录」、SC-11(h) 与 Task 4.4 末条同要求 handoff 内的 deferred 记录 ⇒ 验收判据的对象没有任何任务产出。本文自己在 R3 `73c20653`(c) 处立过口径「只在 §5 写了动作却无任务承接 ⇒ 无人执行也无从验收」并为此新建 Task 4.5, 此处未执行同一标准 (证据: `proposal.md:315,333,295`)
- [minor] testing/`proposal.md:280` Task 1.2 两份清单: SC-15 布局 2 的 (d) 后半 (降级文案含具体原因) 在 rule6_note 被列为 baseline-failing 实体, 却既不在 Task 1.2 的「必须全红五族」, 也不在其回归锁例外清单 (该清单只列「布局 2 的 (e) 半条」), 也不在第二条记录清单 (只列「SC-15 的 (h)(i)(j)」) ⇒ 它的红态验收无归属。这正是 Task 1.2 自述「R3 引入例外清单的初衷正是消除这类灰区」要消除的形态, R4 的补救 (`ce719781`) 又漏了这一格 (证据: `proposal.md:280,366`)

### Risks

- [risk] documentation/终轮预算: `.aria/config.json` 的 `audit.max_rounds = 5`, 本轮即终轮。本席 4 条 major 全部为 R4 之后新增内容 (2026-09-10 基线复核块) 的下游, 不涉及 R1-R4 任何已闭合结论的重开; 若按机制判 MAX_ROUNDS_EXHAUSTED, 建议把这 4 条与 5c28d58f 定级差一并交 owner, 而非当作未收敛的证据
- [risk] documentation/同源性: 4 条 major 与 2 条 minor 同一根因 —— `:16` 的基线复核是一次**事后 amendment**, 却只在自身段落里陈述新事实, 没有按 `agent-team-audit/references/audit-points.md:126-130` 的 neutralize 要求在失效断言处 (`:9` / `:10` / `:313` / `:332` / `:382,386` / `:388` / `:297`) 加 inline 标记。建议 rework 时按一次 neutralize 扫描处理 (含重取 aria 基线 SHA 或明写「行号锚定 301641b, 实施基于 f314785」的双轨口径), 而不是逐条打补丁 —— 逐条补丁正是 memory `feedback_handoff_closure_neutralize_nextstep` 与 `feedback_status_doc_claims_need_diff_verification_and_variant_sweep` 记的复发形态
- [risk] architecture/触点集定义缺失: 本文从未在任何一处**枚举**「本 spec 的触点文件集」, 而 `:9` 与 `:16` 两次拿它当机械判据的输入 (`git diff --stat -- <本 spec 全部触点文件>`)。集合不成文 ⇒ 每次复核的过滤面都由执笔者临场重建, 本轮的漏检即由此产生。建议在 §References 之外单列一份可直接喂给 `git diff` 的路径清单

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 3。

rationale: 本 proposal 在 301641b 这个冻结基线上的事实密度与自洽度很高 —— 本席抽查的全部外部引用 (issue 原文两行 / triage 两行 / 决策单四条落地约束 / LEVEL_GUIDE 四条跨模块判据 / 归档先例逐字 / schema 三处先例 / probe POINTS / latest.md) 无一处失实, R4 的 1 critical + 10 major 也确认全部落进正文而非批注, Rule #6 判据表选行与 Rule #10 白名单适用均经 SOT 逐行核对成立, 头部 `Linked Issue` 行经机械探针实跑合规。扣分全部落在 R4 之后新增的那一个段落上: 2026-09-10 的基线复核把「同伴容器已把 aria 推到 v1.73.0」这条新事实写进文档, 却只顺延了自己那一句, 没有传播到依赖旧事实的六处载重断言 —— 其中三条 (gitlink 起点 / 版本候选号 / 09-09 基线时点) 是 Phase B/C 的硬前置门, 一条 (行号继续有效) 是给复审者与实施者的免检许可。这些不是风格问题: 按 audit-points「数据可用性」横切原则的 verdict 后果条款, 引用的历史/环境数据经机械核实与断言不符即须 REVISE, 即使 post_spec 非阻塞。无 critical: 未发现方案错误、消费方破坏, 也未发现新的恒绿 SC (SC 集本身在冻结基线上仍可证伪)。

## 轮次记录

### Round 5: Agents

- knowledge-manager (本席, 五席之一)
- Sibling probe 行: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 13 (Decisions 6 / Issues 7 / Risks 3 中 Issues 与 Risks 分列, 计入缺陷的为 Issues 7 条)
- Vote: REVISE (Major 4 > 0)
