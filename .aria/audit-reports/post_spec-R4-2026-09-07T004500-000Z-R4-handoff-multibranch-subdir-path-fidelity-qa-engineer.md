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
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T05:55:26.052Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [qa-engineer]
---

# post_spec R4 单席报告 — qa-engineer (handoff-multibranch-subdir-path-fidelity)

席位透镜: 每条 SC 的反事实 (机制没实现会不会红) / hermetic case 能不能真造出来 / 既有测试与冻结语料是否受影响 / 缺哪些负向测试 / 已知失败项处置是否正确。本轮**只审不改**, 未编辑任何仓库文件。行号基准 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `origin/master` `301641b`), 并在真 checkout `/home/dev/Aria/aria` (实测 HEAD `301641b1c893477f387a1f85d1e90d105ebf0db9`) 上交叉复跑。

## 审计结论

### Decisions

- [minor] documentation/R3 19 条 major 的落地复核: 逐条复核 R3 的 19 条 major, 全部落在**正文**而非批注 —— `a7536535`→§What.1 契约行 + Task 2.1 · `92565b30`→§2.5 表 + 裁定块 + Task 2.5(e) + SC-15(h) · `ebaad4a5`→§What.2/§6.1/§6.2/Task 2.2(b)/SC-11(i) · `b5a94a9c`→§6.2 两块分派 + SC-11(c) · `120e1171`→SC-15 三布局定性 + rule6_note 重算 · `2af687f5`/`3dd75e12`→§6.6 + Task 4.4 · `b57e3209`→§3 缺键口径段 · `4608f5b2`→Impact + SC-11(j) · `f658ae7e`/`019ff413`/`56845091`→§待复议 6/7/8 · `17f270f5`→SC-17 · `1ad9b4ed`→SC-4/SC-13 夹具 · `90e3b4b8`→SC-11(c) · `7d909571`→SC-15 细则 · `db126eff`→§6.3 撤回 · `e854a801`→§6.5 三段 · `334e62dc`→头部 R3 轨迹第 3 段。7 条 minor 亦逐条落地。(证据: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md:107,144,197,208,214,254,257,264,266,304,305,312,318,357)
- [minor] testing/SC-10 点名集与消费方覆盖面: 真 checkout `301641b` 实跑 —— 原五模块 `Ran 102 tests … OK`, 新补四模块 (`test_max_branches_resolver` / `test_scan_integration` / `test_collision` / `test_collision_frozen_corpus`) `Ran 65 tests … OK`, 合计 167 全绿。另全 aria 树中引用 `tracks_multibranch` / `collect_handoff_multibranch` / `write_latest_md` / `_list_handoff_files` 的**测试**模块恰为 7 个 (test_collision / test_handoff_multibranch_collision_dedupe / test_max_branches_resolver / test_p1_layer_h / test_scan_integration / test_track_board_advisories / fixtures/freeze_corpus), 9 模块点名集全覆盖; 跨 skill 唯一生产消费方 `phase-d-closer/scripts/fetch_gate.py:187` 以入参吃 `collision_kind`, 其 `tests/test_fetch_gate.py` 传字面值 ⇒ 无回归面。(证据: aria/skills/state-scanner/tests/ 全量实跑 + aria/skills/phase-d-closer/scripts/fetch_gate.py:187)
- [minor] documentation/数据可用性核实 (audit-points 横切原则): 机械核实本文的历史/环境数据断言 —— 本仓 `docs/handoff/` 190 份顶层 `.md`、零子目录、零非 ASCII; `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 各 996 行、filename 零斜杠零非 ASCII; `aria-plugin-benchmarks/ab-suite/state-scanner.json` = 17551 B, `tracks_multibranch` 命中 1 (`:214`, prompt 逐字把 `collision.kind` 的值写死在题面), `handoff_multibranch`/`legacy`/`basename` 三词 0; schema 引用行 `:1104`/`:1108`/`:1110`/`:1114`/`:1125`/`:1126`/`:1136` 与 `_render_pointer` 系列 `:110,143,151,159,162,164` 及 `:298-304` 逐处命中。三类断言全部成立。(证据: aria-plugin-benchmarks/ab-suite/state-scanner.json:214 · aria/skills/state-scanner/references/state-snapshot-schema.md:1104-1136)

### Issues

- [major] testing/SC-3 · §Why F2 · Task 1.2 建红测: F2 的「引号 + 八进制转义 ⇒ 静默漏扫」不是 `git ls-tree --name-only` 的无条件属性, 而是 `core.quotePath` 的默认值。本席在隔离配置的临时仓实测: 默认下输出 `"docs/handoff/2026-\346\265\213\350\257\225-\344\272\244\346\216\245.md"`, 加 `-c core.quotePath=false` 则输出原样 `docs/handoff/2026-测试-交接.md`。而生产侧 `_noninteractive_git_env` 只注入 `LC_ALL` / `GIT_TERMINAL_PROMPT` / `GIT_SSH_COMMAND`, **继承采用方 git 配置** ⇒ (a) 把 `core.quotePath=false` 的采用方 (中文/日文环境常见, 本仓工作语言即中文) 今天**根本不触发** F2; (b) SC-3 的 baseline-red 资格随宿主配置漂移 —— 在这类机器上 SC-3 在 `301641b` 上就是绿的, Task 1.2 的「五族全红」不可满足, 实施者最可能的反应是削断言。姊妹夹具 `_GIT_ENV` 已 pin `GIT_CONFIG_GLOBAL=/dev/null` / `GIT_CONFIG_SYSTEM=/dev/null`, 但本文两处 (SC-4 / SC-13) 把它描述成「只 pin 姓名 / 邮箱」, 正好掩盖了这条载重隔离。修法: SC-3 明写「新夹具必须复用 `_GIT_ENV` 式配置隔离」, 并把 §Why F2 与 CHANGELOG `### Fixed` 的 F2 条改成条件式表述 (`-z` 使行为**不再依赖** `core.quotePath` —— 这才是修复的准确措辞)。(证据: aria/skills/state-scanner/scripts/collectors/_common.py:336 · tests/test_handoff_multibranch_collision_dedupe.py:174-183 · proposal.md:60-75,297,298,308)
- [major] testing/SC-13 · SC-16 · Task 2.2(a) · §6.5: `rel_path` 与 `unreadable_count` 被 §6.5 CHANGELOG `### Added` 声明为**恒存在** (`unreadable_count` 另注「默认 0」), 但 SC 集只在部分产出路径上钉住: SC-16 只覆盖平铺仓且未规定夹具含无 frontmatter 文件, SC-13 的两条 legacy 行只断言 `track_id` 与 `updated_at`, SC-14 只覆盖 fail-soft 早退, 成功路径上 `unreadable_count == 0` 无任何断言。而 Task 2.2(a) 同时强制 `scan.py:186` 改读 `rel_path` 且**不做兜底**、沿用 `:180-182` 的 `if not …: continue` 早退 ⇒ 只要 legacy 追加点 (`handoff_multibranch.py:683-700`) 漏填 `rel_path`, 该行在 AC-5 ancestry 检查上被**静默跳过**, 无任何告警 —— 与 §Why F1 认定的失效形态同型, 且全部 SC 结构上看不见。修法: SC-16 的夹具明写含一条无 frontmatter 文件并断言其 `rel_path` 存在; SC-13 追加 `rel_path` 断言; 任一正常路径 SC 追加 `"unreadable_count" in data and data["unreadable_count"] == 0`。(证据: proposal.md:214,257,308,311 · aria/skills/state-scanner/scripts/scan.py:180-186 · scripts/collectors/handoff_multibranch.py:683-700)
- [major] testing/§7 平铺仓条 · Task 4.3 禁重生成理由: 「用改后代码重生成冻结语料 ⇒ `test_collision_frozen_corpus.py:51` / `:112` 立刻转红」经实读为假。仓内**受认可的**重采样路径是 `tests/fixtures/freeze_corpus.py` (其 docstring `:17-21` 逐字写「Re-running the script on a newer dump is how a future spec refreshes the corpus」), 而 `trim()` (`:32-37`) 用 `{k: r.get(k, …) for k in FIELDS}` 把每行投影成**恰好那八个键**, `main()` (`:48-53`) 回写 `"fields": list(FIELDS)` ⇒ 新增 `rel_path` 根本进不了产物, `:51`/`:112` 重生成后**仍然绿**。真正会红的是 `:111` 的 `assertEqual(len(self.rows), 996)` 以及依赖该 996 行内容的归因断言。后果: 禁令本身正确、理由却站不住, 实施者一核实就会认定禁令无据而放手重生成, 从而打红 `:111` 一族 —— 这正是 memory `feedback_never_write_unverified_impossibility_claims` 的形态。修法: 把 §7/Task 4.3 的证据换成 `:111` 行数钉死 + `freeze_corpus.trim` 的八字段投影事实 (后者恰恰说明「新增字段不构成重采样理由」)。(证据: aria/skills/state-scanner/tests/fixtures/freeze_corpus.py:17-21,29,32-37,48-53 · tests/test_collision_frozen_corpus.py:51,111,112 · proposal.md:224,266)
- [major] architecture/§2.5 `action` 契约三选一裁定块: 本文就地裁定保留 `action` 三值枚举、改为新增 `degraded_reason`, 其唯一机械证据是「改枚举会打红 `tests/test_p1_layer_h.py:264` 的 `assertEqual(result["action"], "pointer")`」—— 该断言为假。`:264` 的夹具是 `_active_track("my-spec", "2026-05-20-my-spec.md")` (`:230-240`, 八字段、**无** `rel_path`、filename 是顶层名), 按 §2.5 强制的缺键兜底 `rel = rel_path or filename` 判定为平铺 ⇒ 走真指针支 ⇒ `action` 仍是 `"pointer"`, 新增第四个枚举值根本触不到它; 全模块 8 处 `_active_track(` 调用与全文件均无子目录 / `rel_path` 夹具 (grep 实证)。另一半理由 (打破 `phase-1-collectors.md:102` 的公开契约) 对「加 `degraded_reason`」同样成立 —— 本文自己已把 `:102` 排进 Task 4.2 的同步面。⇒ 「保留说谎的 `action`」这一支目前缺可核实的机械支撑, 而本文自述其反面 (§2.5「把无声失败原样复制到写侧」) 恰恰指向改枚举。请重写裁定依据 (可保留结论, 但须换成真依据: 例如老消费方只 switch `action` 时的向后兼容代价), 或把该取舍并入 §待 owner 复议。(证据: proposal.md:144 · aria/skills/state-scanner/tests/test_p1_layer_h.py:230-240,246-270,289-336 · references/phase-1-collectors.md:102)
- [minor] documentation/Task 1.2 (proposal.md:254): 同一条 bullet 内自相矛盾 —— 前半写「…**五族**, **这五族**对 `301641b` 全红」, 后半警示块仍写「**⚠️「全红」只限定到上列四族**」(仅在括注里补了「v4 原写四族也已随 SC-17 更新为五族」)。这是 R3 rework 落地 `17f270f5` 时的半改。照后半读会把 SC-17 排除出红测门, 而 SC-17 恰是唯一覆盖闸门输入 (`collision.kind`) 的 baseline-failing 实体。(证据: proposal.md:254)
- [minor] testing/SC-10 (proposal.md:304): SC-10 断言格开头的可执行命令仍只列原五模块并钉死 `Ran 102 tests … OK`, 同格结论却是「点名集共 9 模块…须由 Phase B 重取总数」。验收判据的可执行半与其点名集不一致, 照命令跑只验 9 分之 5。本席实测供参考: 原五模块 102 OK, 新四模块 65 OK, 合 167。建议把命令行直接列全 9 模块并把「总数由 Phase B 抄录」的口径留在括注里。(证据: proposal.md:304 · 真 checkout 301641b 实跑)
- [minor] testing/§What.1 「空段丢弃」(proposal.md:105,107) · SC-9: `git ls-tree -r --name-only -z` 的输出以 NUL **结尾**, 本席实测 `stdout.split("\0")` 必产生一个尾随空段 (`['…2026-测试-交接.md', '…a.md', '…archive/b.md', '']`)。§What.1 把「空段丢弃」写成要求, 但 SC 集无一条覆盖它: SC-9 只断言坏前缀行产生指定 kind 且同分支其它文件照常入 `tracks[]`, SC-2/SC-16 走八字段投影, SC-12a 的 `tracks_multibranch` 逐字段 diff 也看不到 —— 推荐实现 (i) 把 per-item 错误交给 `r.soft_error`, 只进 `CollectorResult.errors`, 不进 `data["errors"]`。若实现把空段送进新前缀守卫, 每个分支多一条 `handoff_multibranch_unexpected_path_prefix`, 恰是本 spec 立意要消除的告警噪声。目前唯一 (偶然、手工) 的网是 SC-12a 的「exit code 与改前相同」。建议 SC-9 加第三条断言: 平铺临时仓上 `handoff_multibranch_unexpected_path_prefix` 计数为 0。(证据: proposal.md:105,107,303,306 · 本席 hermetic 实测 `ls-tree -z` 尾随 NUL)
- [minor] documentation/§What.2 · §6.2 的 dedupe 论据句行号: `legacy:<branch>:<filename>` 在 `dedupe_latest_per_track_container` docstring 里的实际行号是 `handoff_multibranch.py:494` (grep 实证; 整句跨 `:493-499`), 本文 §What.2 与 §6.2 / Task 4.2 多处写 `:495-496`。R3 rework 记录自称把席位给的 `:493-496` 「勘正」为 `:495-496`, 方向反了。SC-11(i) 用 grep 判定, 故不致漏改, 但实施者按行号定位会扑空。另附: SC-11(i) 写的 `grep -c '…' fileA fileB` **合计为 0** —— `grep -c` 多文件时按文件分行输出, 需改成 `! grep -q` 或显式求和。(证据: aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:493-499 · proposal.md:117,197,265,305)

### Risks

- [minor] testing/SC-10 基线取样时点 · §待复议 8: SC-10 写死「基线口径 = 真仓 checkout **零失败**, 出现任何失败都要逐条归因, 不得预先豁免」, 同格又给出第三类归因路径 (日历失效, 2026-09-09 起 2 条自动转红)。两者的相容性取决于**基线在哪天取**: 早于 09-09 取则基线零失败、后续两条红可按日历归因; 晚于 09-09 取则基线自身就带 2 条红, 「零失败」判据不可满足。本席复核该日历机制成立 (夹具 `test_handoff_multibranch_collision_dedupe.py:380-382` 三行日期 2026-08-02/08-10/08-15, 调用处 `:386` 未 pin `now`, `lib/collision.py:222-241` 按 `lib/constants.py:88` 的 30 天窗丢行; 08-10 行在 2026-09-09 出窗)。建议 SC-10 明写「基线须在 2026-09-09 之前取, 否则先按 §待复议 8 的裁定处置再取基线」。(证据: aria/skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py:380-386 · lib/collision.py:222-241 · lib/constants.py:88 · proposal.md:304,358)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **4** / Minor **4** (另 1 条 minor risk + 3 条 decision, 不计入缺陷计数)。

rationale: 方案主干 (A′ + 相对路径贯穿四个调用方 + 写侧守卫 + 读不到不再伪造 legacy) 在代码层复核成立, 全部 hermetic case 均可构造 (`_build_repo` 的 `update-ref refs/remotes/origin/<branch>` 技法不需要真远端; `_list_origin_branches` / `_read_file_content` / `_run` 均可 monkeypatch; `collect_handoff_multibranch(root, now=…)` 入参实存于 `handoff_multibranch.py:559-560`), SC 集绝大多数条目的反事实经代码路径复核为真, R3 的 19 条 major 全部正文落地, 无一条被批注化。无 critical: 没有发现会破坏既有消费方或让整条机制假绿的缺陷 —— 9 个点名模块在 `301641b` 上实跑 167 全绿, `track_to_claim_record` 用 `.get()` 读字段故 additive `rel_path` 不会打红既有管线。

4 条 major 全部落在**可证伪性与事实基础**上, 不阻断方向但会在 Phase B 造成假绿或误导: (1) SC-3 的 baseline-red 资格随宿主 `core.quotePath` 漂移 —— 它是 rule6_note 十一条 substitute 实体之一, 失去鉴别力即等于 Rule #6 的替代面缺一角; (2) 两个自称「恒存在」的机读契约字段在 legacy / 正常路径上无 SC 钉住, 且与 `scan.py:186` 的「不兜底」口径叠加成静默跳过; (3)(4) 两条载重论证 (禁重生成语料的理由、`action` 枚举不动的理由) 经实读/实跑为假 —— 均是 R3 rework 落地过程中新引入的事实错误, 属「勘正引入新错」形态, 需在下一轮 rework 一并闭合。4 条 minor 为半改留下的内部矛盾与行号漂移, 零风险可顺手订正。

## 轮次记录

### Round 4: qa-engineer

- Agents: [qa-engineer] (五席之一; 本报告仅代表本席, 聚合由 audit-engine 完成)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 (Decisions 3 / Issues 8 / Risks 1) — Critical 0 · Major 4 · Minor 8
- Vote: **REVISE**

## 本轮机械核验清单 (全部实读 / 实跑, 可复现)

1. 9 模块基线实跑 (真 checkout `/home/dev/Aria/aria`, HEAD 实测 `301641b1c893477f387a1f85d1e90d105ebf0db9`): 原五模块 `Ran 102 tests … OK`; `test_max_branches_resolver test_scan_integration test_collision test_collision_frozen_corpus` `Ran 65 tests … OK`。
2. `core.quotePath` 对照实验 (隔离 `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` 的临时仓, git 2.39.5): 默认输出带引号 + 八进制转义, `-c core.quotePath=false` 输出原样 UTF-8; 并实读 `_common.py:317-346` 确认生产 env 不隔离 git 配置。
3. `ls-tree -z` 尾随 NUL 实测: `split("\0")` 产生 4 段, 末段为空串。
4. `freeze_corpus.py` 全文实读: `FIELDS` 八元组 (`:29`) + `trim()` 投影 (`:32-37`) + `main()` 回写 `fields` (`:48-53`) + docstring 承认重采样是既有刷新路径 (`:17-21`)。
5. `test_p1_layer_h.py` 全量 `action` 断言与 `_active_track` 夹具实读: `:230-240` 八字段无 `rel_path`, `:264` / `:310` / `:336` 三处 action 断言, 全文件零子目录 / `rel_path` track 夹具。
6. `legacy:<branch>:<filename>` 四处命中实证: `handoff_multibranch.py:36,332,494` + `state-snapshot-schema.md:1104`。
7. SC-11(c) 三条 grep 判据基线复核: `'callers compose the full git-object path'` = 0 (跨行, 确为恒绿) · `'Returns only the basename'` = 1 · `'path relative to'` = 0。
8. 数据可用性: 本仓 `docs/handoff/` 190 顶层 `.md` / 零子目录 / 零非 ASCII; 两份冻结语料各 996 行、filename 零斜杠零非 ASCII; origin 分支数 11; `ab-suite/state-scanner.json` 17551 B 且 `tracks_multibranch` 唯一命中在 `:214`。
9. Layer H 日历机制复核: 夹具日期 `:380-382` + 未 pin `now` `:386` + 30 天窗 (`lib/constants.py:88`, `lib/collision.py:222-241`) ⇒ 2026-08-10 行在 2026-09-09 出窗。
10. 消费方全树扫描: 引用 `tracks_multibranch` 的非 state-scanner 生产代码仅 `phase-d-closer/scripts/fetch_gate.py:187`; 引用四个变更符号的测试模块恰 7 个, 均在 SC-10 的 9 模块点名集内; `references/json-diff-normalizer.md` 的 `reference-snapshot-aria.json` 无任何测试消费 ⇒ §6.3 的 defer 无测试面风险。
11. issue / triage 原文交叉核对: issue 正文确已点名 `_get_file_commit_date` (「这些假 track 的 `updated_at` 走 `_get_file_commit_date` fallback」), A 案原文确为「`filename` / `track_id` 等需要 basename 的字段另行派生」, triage `repro` 两 case `match: true` —— 本文对三者的转述均准确。
