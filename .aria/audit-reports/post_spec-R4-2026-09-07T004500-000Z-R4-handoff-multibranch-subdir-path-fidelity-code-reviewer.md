---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T06:03:59.976Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [code-reviewer]
---

## 审计结论

本席透镜 = 代码级核对。做法: 把 proposal 引用的每一处 `文件:行号` 打开逐条比对 (不采信自述), 对载重断言另做实跑复现, 并对「改动是否会破坏同文件其它调用路径 / 文档同步面是否列全」做独立 grep 与补丁模拟。前提先验: 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` 下 5 个被引文件与 `git show 301641b:` **md5 完全相同**, 故行号口径成立。

R3 的 19 条 major 我逐条映回正文, **全部落在正文而非批注**, 未发现「改一处开一处」的新矛盾。以下 findings 均为本轮新发现。

### Decisions

- [minor] testing/R3 落地核验: 19 个 major ID 逐条映回正文 (a7536535→`proposal.md:107,256,304`; 92565b30→`:137,139-144,260,318`; b57e3209→`:125,257,304`; ebaad4a5→`:117,196,204,257`; 4608f5b2→`:197,208,240`; db126eff→`:11,210,265,305`; 334e62dc→`:19`; 其余同形), 无批注代餐 (证据: `.aria/audit-reports/post_spec-R3-…-aggregated.md:44-128` 对照 proposal 正文)
- [minor] testing/机械事实独立复验: 5 模块 `Ran 102 tests … OK`、9 模块点名集 `Ran 167 tests … OK` (真 checkout `/home/dev/Aria/aria` HEAD=301641b); 日历探针把 `lib.collision.datetime` 换 2026-09-09T12:00Z 后**恰 2 条**转红且与 `proposal.md:304` 所列名字逐字相同; AB 套件 17551 B、`tracks_multibranch` 命中 1 处 (`ab-suite/state-scanner.json:214` 且题面写死 `collision.kind`)、另三词 0; Task 5.1 的 16 个版本点逐处实读全为 v1.71.1; `git ls-tree HEAD aria/standards` = `301641b` / `21748d4`, 与头部冻结一致

### Issues

- [critical] implementation/§3 + Task 2.2(a) + SC-10: 按 §3 处方 (`proposal.md:125`「改成读 `rel_path` 后同形早退即可, **不得**照抄 §2.5 的兜底」) 在缓存副本上实改 `scan.py:180-186,193,204` 后跑 `test_scan_integration`, **19 tests → 3 FAIL**: `TestSnapshotSelfConsistencyAC5::test_contradiction_is_reported` / `::test_detection_uses_enforced_set_not_hardcoded_origin` / `::test_unevaluable_track_is_recorded_not_swallowed`。根因: 夹具 `HEALTHY_TRACKS` (`tests/test_scan_integration.py:164-166`) 只有 `track_id`/`filename`/`branch`, 无 `rel_path` ⇒ `if not rel_path: continue` 把每一行都跳过 ⇒ `errs == []`。⇒ proposal 自述「写 `.get()` 则**照绿**但测不出拼进命令行的是哪个字段」(`proposal.md:125`) **为假**, 而 SC-10 (`:304`) 把该模块以「回归面 (只保证不被打红)」身份点名、Task 4.3 (`:266`) 要求「既有测试全绿」—— 三条要求**互斥**。它与 R2 判 critical 的 `6f8fa9f7`「既有夹具立刻翻红」同型 (证据: `proposal.md:125,266,304` + 实跑输出 `AssertionError: 0 != 1` @ `test_scan_integration.py:270`; 基线对照 `Ran 167 tests … OK`)
- [major] testing/SC-16 + SC-13 + Task 2.2 — legacy 行的 `rel_path` 回填无 SC 覆盖: 改后仍有**两个** track append 站点 (`handoff_multibranch.py:663-674` frontmatter 分支 / `:686-697` 无-frontmatter legacy 分支, §4 只删 git-show 失败那个)。SC-1/SC-8/SC-17 走 frontmatter 分支; SC-13 只断 `track_id` 与 `updated_at`; SC-16 (`proposal.md:311`) 虽写「`tracks[]` **每一行**」却**未规定夹具须含无-frontmatter 行** —— 而本文在 SC-15 处刚立过「夹具组成是判据的一部分, 不得按字面取最小夹具」(`:310`)。⇒ 只在 frontmatter 分支填 `rel_path` 的实现可全绿; 叠加 §3 的无兜底早退, 子目录 legacy track 在 `scan.py:180-182` 被静默跳过 = §Impact 声称修掉的 F1 (`proposal.md:239`) 原样复现, 且无任何信号 (证据: `handoff_multibranch.py:686-697`, `scan.py:180-186`, `proposal.md:308,311`)
- [minor] documentation/§5 消费方枚举漏一处: 全插件树 `grep -rl tracks_multibranch skills/` 在 state-scanner 之外只命中 phase-d-closer 三文件, §5 登记了 `handoff-mechanics.md` 与 `fetch_gate.py:175-188`, 漏 **`phase-d-closer/SKILL.md:218`**「子步骤 2 Pointer 更新 (conditional by `snapshot.tracks_multibranch` multi-track detection)」。它与已登记的 `advanced-rules.md` / `RECOMMENDATION_RULES.md` 同类 (不改文本、输入值变), 按本文自身口径应入表 (证据: `skills/phase-d-closer/SKILL.md:218`)
- [minor] documentation/行号漂移 — dedupe docstring 的 legacy 公式在 **`handoff_multibranch.py:494`** (`:495` = "so two legacy rows can never share a dedupe key…", `:496` = "real track, and every legacy row's owner_container…"), 而 `proposal.md:117` / `:206` / `:257` 三处均写 `:495-496`。SC-11(i) 用 `grep -c` 计数, 不产生假绿, 属导航性错误 (证据: `sed -n '492,499p'` 逐行)
- [minor] documentation/行号漂移 — D.3 pointer 决策表: 实读 `phase-d-closer/references/handoff-mechanics.md` 为 `:116` 判定逻辑句 / `:118-119` 表头 / **`:120-122` 三行判据**。`proposal.md:184,267,348` 写「`:116-121` 的 3 行决策表」(截掉第 3 行), `:218` 更把 Single-track 行写成 `:116` (实为 `:120`)。`:114-124` 的引用正确 (证据: `grep -n 'Single-track\|Multi-track'` = 120/121/122)
- [minor] documentation/§6.1 — 「`## Change history` 既有口径是每次 schema 变更加一行」被同家族上一周期证伪: `f2e4231` (v1.70.0 文档同步) 给 `state-snapshot-schema.md` 加了 14 行 (含 `:1091` `identity_advisories`) 却**未触碰** Change history, 表末行仍是 `2026-07-19` (文件共 1168 行)。SC-11(g) 的要求本身合理, 但论据句须改写为「表**应**每次登记, 上周期漏登记」(证据: `git -C aria show f2e4231 -- …schema.md` 无 Change history hunk; `schema.md:1156-1168`)

### Risks

- [minor] implementation/AC-5 记录的 `filename` 语义: `scan.py:180` 的变量同时喂 `:186` 的命令行与 `:193` `inconclusive[].filename` / `:204` `offenders[].filename`。按处方改读 `rel_path` 后, 子目录 track 在 `errors[].tracks[].filename` 里由 basename 变相对路径 —— 该输出语义变化未登记进 §5 / §6 / CHANGELOG (对照: `legacy_count` 语义收窄、`identity_advisories` 加法面都登记了)。`test_scan_integration.py:272` 正钉该值, 若 fixture 补 `rel_path` 时取相对路径写法, 该断言也需同批更新

### 复核记录 (未构成 finding 的正向核验, 供后续轮免重跑)

- 全部代码引用逐处命中: `handoff_multibranch.py` `:16-31`/`:35-44`/`:20`/`:36`/`:40`/`:42`/`:177-178`/`:240-288`/`:246-247` (确为跨行)/`:277`/`:278`/`:280`/`:301`/`:313`/`:316`/`:321-322`/`:329-336`/`:396`/`:428-455`/`:493-499`/`:521-524`/`:559-560`/`:586-596` (`:593` 三键)/`:587,607,623,643`/`:619` 二元解包/`:637-658`/`:683-700`/`:748`/`:753`; `handoff.py:263-266,288,300,318-323,389,397-404,438-451,455`; `latest_md_writer.py:32,89-94,110,116,140,143,151,159,164,205-217,259,279,287-290,298-304`; `scan.py:119-120,166,172,180-182,186,199-200,255,388`; `_common.py:312-313,411-412`; `lib/collision.py:226-241,480-486`; `lib/constants.py:88`; `track_board.py:183,188,254,559`; `schema.md:46-48,1070,1074,1104,1108,1110,1114,1125,1126,1128,1136,1156-1168`; 测试侧 `test_p1_layer_h.py:230-240,264,270`、`test_max_branches_resolver.py:286,300,316,332` (确为 2-tuple mock)、`test_scan_integration.py:164-166,172-176`、`test_collision.py:439,445,460`、`test_collision_frozen_corpus.py:51,112`、`freeze_corpus.py:29`、`test_handoff_multibranch_collision_dedupe.py:174-183,380-382,386`
- SC-11(c) 的换判据成立: 基线 `grep -c 'callers compose the full git-object path'` = **0** (跨行, 旧判据恒绿), `'Returns only the basename'` = **1**, `'path relative to'` = **0** —— 新判据一正一反皆 baseline-failing
- `write_latest_md` 零生产调用点复核成立: 命中集 = 函数自身 + `writers/__init__.py:9,12,14` 再导出 + `test_p1_layer_h.py` **5 处调用** (`:261,286,307,335,362`) + `layer-l-integration.md:101`; `_render_pointer` 只在 `latest_md_writer.py:303` 被调, 改其返回形态不破外部消费方
- `collect_handoff_multibranch` 只有两条 `r.data` 返回路径 (`:588-596` fail-soft / `:747-755` 正常) ⇒ Task 2.3 + 2.4 对「`unreadable_count` 恒存在」是**完备**覆盖, 无第三条漏网早退
- `validate_schema_doc.py` 是 **TOP-LEVEL KEY 粒度**且自述 "nested field completeness is NOT checked" (`:18-22`) ⇒ 新增 `unreadable_count` / `rel_path` 不会被它机械拦下, SC-11 的 grep 集确是唯一闸门 (本文未提该验证器, 但结论上无影响)
- `json-diff-normalizer.md` 撤回判断成立: `:196` 是 `### tests/fixtures/reference-snapshot-aria.json` 节, `:204` 起为 2026-07-18 resample 的过去时记述, `:241` = 截断后仍可查的周边字段枚举; 全篇 `tracks_multibranch` 仅 `:207` / `:235` 两次, 无规范性键集
- 主仓事实: `docs/handoff/` 190 份顶层 `.md` / **0 个子目录** / **无非 ASCII 名**; 两份冻结语料均在; `standards` 与 `aria` gitlink 与头部冻结一致

## Verdict

**FAIL** — Critical 1 / Major 1 / Minor 5 (+ 2 decisions, 不计入)。

理由: 本轮唯一的 critical 不是措辞问题, 而是**处方与验收判据互斥**——按 §3 白纸黑字实施, 本文自己点名要求「不被打红」的模块当场红 3 条, 而本文对该模块的性质判断 (「写 `.get()` 则照绿」) 经补丁模拟证伪。这一条不闭合, Phase B 只有三条路: 改夹具 (未登记、未授权)、加 §3 明令禁止的 `or filename` 兜底、或削断言 —— 第三条正是本文多处引用的失效模式。major 那条同源: `rel_path` 在 legacy 分支的回填缺一条有夹具约束的 SC, 漏填即把本 spec 声称修掉的 F1 静默失效原样搬回来。两条的修法都很小 (Task 2.2 明写夹具补键 + SC-16 规定夹具须含无-frontmatter 行), 属定点 rework 而非重做。

## 轮次记录

### Round 4: Agents

- 席位: code-reviewer (五席之一, 本报告为单席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 9 (Decisions 2 / Issues 6 / Risks 1)
- Vote: REVISE
