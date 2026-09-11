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
timestamp: 2026-09-10T17:23:10.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead]
---

# post_spec R5 单席报告 — tech-lead (handoff-multibranch-subdir-path-fidelity)

本席为新席位, 不继承前四轮结论。透镜: 架构与范围 / 根因 vs 症状 / 候选方案取舍 / 与其它 collector 与消费方的接缝 / 是否越界到同伴容器在飞面 / ship 顺序与 gitlink 归属。全部结论基于实读与实跑, 本轮**未编辑任何仓库文件** (收尾复核 `git status --porcelain` = 0 行, 三个仓均干净)。

## 审计结论

### Decisions

- [minor] documentation/R4 的 1 critical + 10 major 落地复核: 11/11 逐条落进**正文而非批注** —— `5c28d58f`→Task 2.2(c) 补 `HEALTHY_TRACKS` 键 + §3 删掉已被证伪的「照绿」句; `5513534d`→§3 上报字段语义归属块 + §5 行; `ead9ac24`→§2.5 指定 `_render_pointer` 返回 `tuple[str, str | None]` + SC-15 (i)(j) + 第 4 条反事实; `5105b00e`→裁定依据换成兼容性论证; `7ae33f13`→SC-13(c) + SC-16 夹具组成; `177d72e6`→SC-3 `_GIT_ENV` 配置隔离 + F2 条件式措辞; `31bc3c6a`→依据换 `:111` 996 行; `b3e5ea8d`→Task 2.0a; `ab615189`→rule6_note 落行条件化; `5b252465`→Task 2.5(g)+SC-11(k); `23b414c9`→§5+Impact.Risk+Task 5.3(d)。14 条 minor 抽验 6 条亦落地 (证据: `proposal.md:285` `:313` `:332` `:333`; 残留的两处 `:495-496` 均为「勘正自身出错」的叙述性引用, SC-11(i) 判据本身已改为 `:494`)
- [minor] architecture/§5 消费方枚举完整性: `grep -rl 'tracks_multibranch'` 在 301641b 全插件树命中 24 文件, state-scanner 之外仅 phase-d-closer 三处 (`SKILL.md:218` / `references/handoff-mechanics.md` / `scripts/fetch_gate.py`), 均已入 §5 表; v1.73.0 新增的 `state-scanner/scripts/check_bare_issue_refs.py` / `skill_md_literal_sync_probe.py` / `phase-d-closer/tests/conftest.py` 对本 spec 触面 grep 零命中 ⇒ 新版本未引入未登记消费方 (证据: 实跑 grep + `git diff --name-status 301641b f314785`)
- [minor] documentation/Task 5.1 的 16 个版本点行号在主仓 HEAD `fe703c5` 上逐处实测仍命中: `README.md:8` / `:242`, `VERSION:24`, `CLAUDE.md:139` / `:141`, `README.zh.md:3` / `:10` / `:244`, `docs/architecture/system-architecture.md:189`, `docs/architecture/version-scheme.md:23` (取值均为 v1.73.0) ⇒ 该表只需改号, 不需重定位
- [minor] architecture/待复议 7 若裁 Level 3 的拆分建议 (供 owner 一并裁): 按「今日症状面 vs 未来接线面」拆两个 sub-spec —— (1) 枚举层 `-z` + 相对路径 + 四调用方 + 假 legacy 移除 + schema 同步 (直接闭合 #195 报告方的三层症状); (2) pointer 写侧守卫 + `degraded_reason` + standards 第三态 + writer 契约面。理由: (2) 的全部价值发生在 `write_latest_md` 未来被 D.3 接线之后, 而它今天**零生产调用点** (`references/phase-1-collectors.md:95` 逐字「deliberately D.3-scoped … 不引入 production call-site」; 本席在 f314785 上复跑 `grep -rn write_latest_md` 排除 tests 后仍只剩 `__init__.py` 再导出与两份文档), 却占本文近半篇幅、5 个文档同步面与整个 SC-15 三布局

### Issues

- [major] architecture/proposal.md:16 基线复核块 · :9 基线冻结 · Task 5.2 (:313): **基线冻结 301641b 的「继续有效」结论被复核自身的证据面推翻**。`:16` 只对「本 spec 全部触点文件」跑 diff 就断言「本文**全部行号**在 `f314785` 上继续有效」; 本席实测 `git -C aria diff --name-status 301641b f314785` = 21 文件, 其中 `skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py` **正是本文多处引用行号的文件**且属 SC-10 点名 9 模块 —— `_GIT_ENV` 由 `:174-183` 漂到 `:176-185`, `GIT_CONFIG_GLOBAL/SYSTEM` 由 `:181-182` 漂到 `:183-184`, 日历夹具由 `:380-382` 漂到 `:382-384`, 调用点由 `:386` 漂到 `:388` (且已加 `now=_FIXED_NOW`)。同一复核块承认「主仓 gitlink 已随之前进」, 却未同步 `:9`「Phase B 在 `301641b` 起分支」与 Task 5.2「gitlink bump **从 `301641b` 前进** …… 严禁回退到 `0545f86`」—— 实测主仓 `git ls-tree HEAD aria` = **`f314785`** (bump 提交 `c02b0ef`), 今天真正要防的回退面是 `f314785` 而不是 `0545f86`。⇒ 硬约束句所指的 SHA 与现实脱节, 与它当初要根治的「陈旧 origin 视图」是同一形态 (证据: `proposal.md:16` / `:9` / `:313`; `git -C /home/dev/Aria/aria diff --name-status 301641b f314785`; `git -C /home/dev/Aria ls-tree HEAD aria`)
- [major] architecture/待 owner 复议 8 (proposal.md:381) · SC-10 基线口径 (:332) · Task 1.2: **一个被列为 Phase B 硬门的 owner 复议项已被同伴轨解决, 正文仍以现在时陈述**。aria `f314785` 的提交标题逐字「fix(state-scanner/test): collision_dedupe 16 个 collector 调用点钉 `now=` — 半冻结时钟致按日历腐烂 (aria-plugin#194)」, 该 issue 原文标题即「collision_dedupe 测试只冻结了 renderer 的时钟没冻结 collector — 21 条测试用绝对日期, 今日 2 红并按日历恶化至 7 红」。本席两处实跑: 在 `f314785` 真 checkout 上 `python3 -m unittest test_handoff_multibranch_collision_dedupe` = **`Ran 23 tests … OK`**; 在冻结基线 `301641b` 副本上同一命令 = **`Ran 21 tests … FAILED (failures=2)`** (`AssertionError: 'none' != 'cross_owner'`)。而 SC-10 明写「基线取样时点必须早于 2026-09-09 …… **若已过该日, 先按 §待复议 8 的裁定处置再取基线**, 不得就地把『零失败』改口径」—— 今天是 2026-09-10, 照文推进即被一个上游已闭合的问题卡死; 连带 SC-10 的 `Ran 102 tests` 基线数字与「第三类归因路径 (日历失效)」整段作废 (证据: `proposal.md:381` / `:332`; `git log --oneline 301641b..f314785`; forgejo `10CG/aria-plugin#194` 标题; 两次 unittest 实跑)
- [major] architecture/待 owner 复议 6 (proposal.md:378) · Task 2.0b · Task 5.1: **版本级别门的候选号与实况不符, 且 09-10 复核只顺延了一半**。待复议 6 逐字写「`git -C aria tag --list 'v1.7*'` 最高为 `v1.71.1`, 两个候选号 (`v1.71.2` / `v1.72.0`) 当前均未被占用」并把**推荐默认改为 MINOR / v1.72.0**; 实测 aria 已 ship **v1.73.0** (`git ls-remote --tags origin` 有 `refs/tags/v1.73.0^{} = 6726df1`, `plugin.json:4` = `"1.73.0"`)。`:16` 的复核只把 **PATCH** 候选顺延到 v1.73.1, 未动 MINOR 候选 ⇒ owner 若照签「MINOR / v1.72.0」, 版本 SOT 会从 1.73.0 **回退**, 并连坐 Task 5.1 的 16 个版本点与 tag。另: 同伴轨的取号理由 (aria `CHANGELOG.md` v1.73.0 Notes 与 `docs/handoff/2026-09-08-archive-gate-drift-shipped-v1-73-0.md:77` 逐字「避开并发轨 `10CG/Aria#195` / `10CG/Aria#199` 正在争的 `v1.71.2` / `v1.72.0`」) 表明**两条并发轨都在等这两个号**, 顺延后需要与 #199 重新协调, 而本条目对 #199 零字提及 (证据: `proposal.md:378` / `:16`; `git ls-remote --tags`; `aria/.claude-plugin/plugin.json:4`; `aria/CHANGELOG.md:13,36`)

### Risks

- [minor] testing/Phase B 起点与新夹具模板 (SC-3 / SC-4 / SC-13 引用的 `_GIT_ENV`): 若维持 `301641b` 起点, 新测试会照**旧模板**写夹具, 而 origin/master 的同一文件已改 99 行 (新增 `_FIXED_NOW`(`:173`) 与 16 处 `now=` 口径) ⇒ 合并期出现同文件内两种时钟口径; 且 aria-plugin#194 原文记该红态「按日历恶化至 7 红」, 冻结越久, 基线越脏、Task 1.2 的红态记录越难与「本 spec 打的红」区分。缓解方向与上面第一条 major 同一处置: 把基线重取到当前 `origin/master`, 并对本文引用该文件的四处行号重新实测

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **3** / Minor **1** (+ 4 decisions, 不计入 severity)。

rationale: 本轮**未发现任何新的设计缺陷**。R4 的 1 critical + 10 major 经逐条复核全部落进正文 (非批注), 且抽验未见「勘正引入新错」; A′ + 写侧守卫的方案本身仍成立 —— 根因 (枚举层交出的 basename 在信息论上不足以回拼) 修在枚举层而非症状点, 四个调用方与五个受影响量 (`exists` / `len(tracks)` / `legacy_count` / `collision.kind` / `n_active`) 均已登记, 消费方枚举经全树复核完整, 也未越界到 phase1_gate / claim_lifecycle / spec-drafter / AB 套件 (仅开缺口 issue, 不改套件)。

三条 major **全部属同一族: 世界在动, 而基线冻在 3 天前** —— 同伴轨在 09-07…09-09 之间 ship 了 v1.73.0 并追加了 `f314785`, 于是 (1) 「全部行号继续有效」为假, (2) 一个 owner 硬门已被上游解决, (3) 版本候选号回退。三者都不需要重新设计, 只需一次**基线重冻 + 三处顺延**。按当前收敛态势, 若不重冻基线, 后续每多一天都会再生一批同族 major, 收敛不可能发生; 重冻之后本 spec 的技术实体已具备进 Phase B 的条件 (剩余阻塞只有待复议 6 / 7 两个真 owner 门)。

## 轮次记录

### Round 5: Agents

- tech-lead (本席, 单席报告)

Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品

Conclusions 数: 8 (Issues 3 / Risks 1 / Decisions 4)

Vote: **REVISE**

### 本轮机械核验清单 (可复算)

1. `git -C /home/dev/Aria ls-tree HEAD aria standards` = `f314785` / `21748d4` (standards 与本文 Task 4.4 的冻结起点一致)
2. `git -C aria diff --name-status 301641b f314785` = 21 文件 / 895 增 63 删; 逐个比对本文引用面 ⇒ 命中 `tests/test_handoff_multibranch_collision_dedupe.py` (行号漂 +2) 与 `phase-d-closer/SKILL.md` (`:218` 未漂, 经 grep 双 SHA 核对)
3. `python3 -m unittest test_handoff_multibranch_collision_dedupe`: f314785 = `Ran 23 … OK`; 301641b 副本 = `Ran 21 … FAILED (failures=2)`
4. `git ls-remote --tags origin` = v1.70.0 / v1.71.0 / v1.71.1 / v1.73.0; `plugin.json:4` = 1.73.0
5. 301641b 逐处实读复核本文载重行号: `handoff_multibranch.py:177-178,240,243,246-247,277-280,298,301,313,315,321,329-336` · `scan.py:180-182,186,193,209,255,388` · `latest_md_writer.py:89-95,110-116,143,151-169,294-310` · `references/phase-1-collectors.md:95,102,104` · `standards/conventions/session-handoff.md:97,171-173` · `spec-drafter/LEVEL_GUIDE.md:155-163` (跨模块四条判据「满足任一」属实) —— **全部命中, 无一处失真**
6. 数据可用性 (Aria #54 横切): `.aria/decisions/2026-09-07-…-pointer-guard.md` 存在 (6794 B); 两份冻结语料 `tests/fixtures/` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 均存在; `freeze_corpus.py:29` 八字段投影与 `test_collision_frozen_corpus.py:51,111,112` (996 行) 逐字属实 ⇒ R4 `31bc3c6a` 换上的依据成立
7. 本仓平铺前提 (Task 1.1 / SC-12a): `docs/handoff/` 零子目录、零非 ASCII 名、193 份顶层 `.md`、23 份 frontmatter `status: active` (本文记 190 / 22, 属自然增长, 已带测量日期标注)
8. 全树 `grep -rl tracks_multibranch` (301641b) = 24 文件, 与 §5 表逐一对齐
