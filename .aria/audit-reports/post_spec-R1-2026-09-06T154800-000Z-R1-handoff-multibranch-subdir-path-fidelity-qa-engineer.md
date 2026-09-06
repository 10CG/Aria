---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T16:35:41.760Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [qa-engineer]
---

# post_spec 审计 — qa-engineer 席位 (Round 1)

审计对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, Aria#195)。
席位透镜: SC 可证伪性 (逐条反事实) / hermetic case 可构造性 / 既有测试与冻结语料受影响面 / 负向测试缺口 / 已知既有失败项处置。

本轮**只审不改**, 工作区在返回时 `git status --porcelain` 为空 (主仓 + aria 子模块均 clean); 全部实验落在 scratchpad 与 tempdir。

---

## 审计结论

### Decisions

- [minor] architecture/proposal.md rule6_note: **Rule #6 判定核实通过** —— 实读计数 `aria-plugin-benchmarks/ab-suite/state-scanner.json` (15518 B) 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词命中数**均为 0** (连 `handoff` 一词也是 0), 且本 spec 不触 SKILL.md 指令面 ⇒ 判据表第一行 (描述性) + SC 级 baseline-failing substitute 成立, 不需跑 AB。(证据: 本席位对该 json 的 `str.count` 实测)
- [minor] architecture/proposal.md §Why + §7 + 方案 A/D: **根因与向后兼容前提核实通过** —— 我在临时仓 (`docs/handoff/archive/2026-05-09-session-end.md` 带合法 frontmatter + 顶层文件 + 两个 `latest.md`) 上直调 `collect_handoff_multibranch`, 逐字复现了假 legacy 行 (`track_id=legacy:master:2026-05-09-session-end.md`, `status=legacy`, `updated_at=""`) 与 `handoff_multibranch_git_show_failed`; `scan.py` 对该仓 exit 10 且**仅此一条** soft error (offline 与非 offline 均如此) ⇒ SC-12 后半条「改后 exit 0」可达。平铺零变化前提亦实证: 工作树与**全部 origin 分支**(committerdate 前 25 条) 下 `docs/handoff/` 0 子目录 / 0 非 ASCII; 两份冻结语料各 996 行, `filename` 含 `/` 0 条、非 ASCII 0 条、`legacy` 0 条; 活体 `.aria/state-snapshot.json` 的 1408 行中 252 条 legacy 全部来自无-frontmatter 分支 (`tracks_multibranch.errors` 长度为 0) ⇒ 变更 4 不动本仓 `legacy_count`。(证据: `.aria/state-snapshot.json`, `aria/skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json`)

### Issues

- [critical] testing/proposal.md SC-10: **SC-10 允许的两条「基线已知失败」是环境伪失败, 等于预授权唯一端到端快照稳定性测试变红。** 我从 plugin cache 目录跑全量 discover, 精确复现了 proposal 写的 `Ran 1571 tests ... FAILED (failures=1, errors=1, skipped=13)` 与两条同名失败; 但根因是 `tests/test_normalize_snapshot.py:272` 与 `:344` 的 `project_root = Path(__file__).resolve().parents[4]` —— 在 cache 里那是 `~/.claude/plugins/cache/10CG-aria-plugin/aria` (**非 git 仓**), `scan.py` 返回 20 (EXIT_HARD_PRECONDITION, scan.py:120) ⇒ 两条 assert 挂。同一份 `test_normalize_snapshot.py` (与本地 0545f86 `diff` 无输出) 在真实仓 checkout 下跑是 **32 tests OK**。也就是说基线是在 plugin cache 里测的, 不是在声明的 301641b 仓 checkout 里。后果: SC-10 白纸黑字允许 `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` 与 `Test1210ChannelStabilityUnderOffline` 原样为红 —— 而它们恰是全套件里唯一「连跑两次 scan.py 再 diff 归一化快照」的端到端稳定性测试, 正对 Impact.Risk 第三行 (`-z` 解析写错 ⇒ 静默失明) 与本 spec 新增快照键的爆点。修法: 在 301641b 的真仓 checkout 重测基线, 删掉这条豁免; 若届时确有真失败再逐条 `git log -- <file>` 归因。(证据: `aria/skills/state-scanner/tests/test_normalize_snapshot.py:272,344`; `scan.py:120`)
- [major] implementation/proposal.md §Why F1 (:41) / §5 (:115) / SC-6 (:172): **`scan.py::_check_handoff_ancestry` 这个符号不存在。** 对 v1.71.1 全 skill 树 grep `_check_handoff_ancestry` 零命中, 只命中 proposal 自身三处。真正拼 `docs/handoff/{filename}` 的是 `_same_branch_head_unreachable_tracks` (scan.py:126, 拼串在 :186), 由 `_check_snapshot_self_consistency` (scan.py:216) 在 :255 调用。SC-6 因此指向一个不存在的测试目标, 三处引用需一并勘正。(证据: `scan.py:126,186,216,255`)
- [major] testing/proposal.md SC-6: **SC-6 的反事实只在 tracks_data 由真 collector 产出时成立, 而 SC 文本没写这一条。** SC-6 只说「对含子目录 track 的**快照**跑」; `_same_branch_head_unreachable_tracks` 的签名正好只吃 dict, 最省事的实现是手搓 `{"tracks":[{"filename":"archive/x.md",...}]}` —— 那样 collector 根本没被调用, 「退回 basename ⇒ 空 SHA ⇒ 红」的反事实为假, SC 恒绿。另有四道前置未点名: `current_branch` 非空、非 `detached_head`、`enforced_remotes` 非空、`t["branch"] == current_branch` (scan.py:166-183); 任一没配到, 函数在早返回 `[]` 上假绿。SC-6 需明确要求「tracks_data 必须由同一临时仓上的 `collect_handoff_multibranch` 端到端产出」并列出四道前置。(证据: `scan.py:166-183`)
- [major] testing/proposal.md §1 pointer 行 (:88) + SC-8 + 待 owner 复议 1: **「pointer 排除改为任意深度」在基线上已经是现状, §1 把 no-op 标成了行为变更。** 现码 `handoff_multibranch.py:277` 先取 `basename = Path(path).name`, `:280` 再比 `_POINTER_FILENAME` —— 本来就是任意深度。我在含 `docs/handoff/latest.md` + `docs/handoff/archive/latest.md` 的临时仓上直调基线 `_list_handoff_files`, 返回 `['2026-05-10-top.md', '2026-05-09-session-end.md']`, 两个 `latest.md` 都已被排除。后果三层: (1) §1 表该行描述错误; (2) SC-8 前半条 (两个 latest.md 均不出现在 `tracks[]`) 在 301641b 上**已绿**, 违反 Task 1.2「对 301641b 全红且红在正确断言上」—— 其鉴别力只剩后半条 `archive/latest-notes.md`; (3)「待 owner 复议 1」把现状包装成待定默认, 其「反对分支」实为**引入**新行为而非保留现状, 需重写为「现状即任意深度, 是否要改成只排顶层」。(证据: `handoff_multibranch.py:277,280`)
- [major] testing/proposal.md SC-10 基线数字: **「73 tests OK」不成立, 实测 78。** SC-10 原命令 (`python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories`) 我在 301641b 缓存副本与本地 0545f86 checkout 上各跑一次, **两次都是 `Ran 78 tests ... OK`**。数字错 5 条; 与上面 1571 只在 plugin cache 复现一并佐证基线不是在声明位置测的。(证据: 两次实跑输出)
- [major] testing/proposal.md §2 (:96) 与 SC 集合: **`_make_legacy_track_id` 改用相对路径这一声明的行为改动零 SC 覆盖。** §2 明写改为 `legacy:<branch>:<relpath>` 并给了动机 (两个子目录下同名文件否则产生同一 legacy track_id, 被 `dedupe` 当成同一 track), 但 SC-1~SC-9 无一条断言: SC-1 是非 legacy 真 track; SC-5 断言不可读文件**不产生** legacy 行; 其余不涉及。改完后唯一还能产 legacy 行的路径是无 frontmatter 分支 (`handoff_multibranch.py:683-700`) —— 恰恰就是这个碰撞场景。需补一条 SC: 两份 `archive/x.md` 与 `x.md` 皆无 frontmatter ⇒ 两条不同 `track_id`, `dedupe_latest_per_track_container` 不折叠 (反事实: 用 basename ⇒ 同 id ⇒ 折叠成一条 ⇒ 红)。(证据: `handoff_multibranch.py:329-336,683-700`)
- [minor] documentation/proposal.md SC-4: **SC-4 标题与正文自相矛盾, 且前半条是未标注的记录性断言。** 标题写「`updated_at` 不再取 mv 日期」, 正文却正确地自认: 无 frontmatter 的那半条改后仍是 `2026-08-15` (`git log -1` 的真值)。该半条改前改后同值 ⇒ 对本变更零鉴别力, 却没有像 SC-7 那样标「现状记录性断言」。风险是 Phase B 读标题去给 `_get_file_commit_date` 加 `--follow`。建议照 SC-7 加标注, 并把标题收窄为「有 frontmatter 的子目录交接不再退化到 mv 日」。(证据: `handoff_multibranch.py:310-326`)
- [minor] implementation/proposal.md §1 (:86): **前缀剥离用字面量 `path[len("docs/handoff/"):]`, 等于新造第五处硬编码前缀** —— 正是本 spec 认定的根因族 (「四处硬编码前缀」)。应从 `_HANDOFF_TREE_PATH` 派生 (`path[len(_HANDOFF_TREE_PATH) + 1:]` 或 `PurePosixPath.relative_to`)。顺带勘正既有注释错误: `handoff_multibranch.py:177` 写「trailing slash required by git ls-tree --name-only」, 而 `:178` 常量值 `"docs/handoff"` 并无斜杠。(证据: `handoff_multibranch.py:177-178`)
- [minor] documentation/proposal.md rule6_note (:184): **SKILL.md 前提陈述不准。** rule6_note 称 SKILL.md「只在 collector 清单里出现 `tracks_multibranch` 一词」; 实测 3 处 —— `SKILL.md:117` (collector 清单)、`:149` 与 `:153` (coordination 闸门接线, 属运行时指令面)。判定**结论仍成立**: 我核实 `lib/collision.py:480-485` 确实排除 `owner_container == "unknown"` (schema 文档 :1128 同述), 而假 legacy 行的 `owner_container` 恒 `unknown` ⇒ 删掉它们不动 `collision.kind`, 闸门面不受影响。但 Rule #6 / Rule #10 的判定前提写错值得勘正。(证据: `SKILL.md:117,149,153`; `lib/collision.py:480-485`)

### Risks

- [major] testing/proposal.md SC-2 + Impact.Risk 第三行: **SC-2 的「动态载入改前实现」既非平凡也非 hermetic, 而它是 `-z` 静默失明的唯一缓解。** 我实跑了两种载入路径: 朴素 `exec(git show 301641b:… 的源码)` 直接 `ImportError: attempted relative import with no known parent package` (collector 在 `:120-127` 用 `from ._common import …` / `from .handoff import …`); 必须建 `collectors.<name>` 的包上下文**并手动设 `__file__`** 才成功 —— 否则 `:141` 的 `_Path(__file__)` 抛 NameError, 而 `:152` 只 `except ImportError` 接不住。此外 SC-2 引入 git 历史依赖: plugin 分发副本 `~/.claude/plugins/cache/10CG-aria-plugin` **不是 git 仓** (`fatal: not a git repository`), 而基线恰恰是在那里测的 ⇒ SC-2 会在同一位置直接 error, 再添一条「已知失败」。建议改为对冻结期望 fixture 断言 (仓内已有 `tests/fixtures/freeze_corpus.py` + `handoff-tracks-frozen-*.json` 形态), 或 `skipUnless(是 git 仓)` 并另留一条不依赖 git 历史的「枚举结果非空且等于预置清单」断言, 保住反事实。(证据: `handoff_multibranch.py:120-127,141,152`)

---

## 补充: 已机械核实**通过**的断言 (不构成 finding, 供后续席位免于重复)

| proposal 断言 | 核验手段 | 结论 |
|---|---|---|
| 5 个触点文件在 0545f86↔301641b 零 diff | `git -C aria diff --stat 0545f86 301641b -- <5 files>` | 真 (空输出) |
| F2: `ls-tree` 默认引号+八进制转义, `-z` 给原样 NUL 分隔 | 临时仓 `git ls-tree -r --name-only [-z]` + `od -c`, git 2.39.5 | 真 (末尾有 trailing NUL, 与 §1「空段丢弃」一致) |
| triage case-2「`updated_at = 2026-08-15T12:00:00+00:00`」 | 读 `.aria/triage-comment-195.md:47` | 逐字一致 |
| `renderers/track_board.py` 不读 `filename` 字面 | 读 `_render_row` (track_board.py:548-572), 仅用 `_handoff_date(updated_at)` | 真 (该文件 `:19` 的模块 docstring「or filename stem」是既存陈旧注释, 非本 spec 引入) |
| `lib/collision.py` 少几条假 legacy 行不改分类 | `collision.py:480-485` + schema 文档 `:1128` | 真 |
| `unreadable_count` 为 additive 新键不破既有断言 | grep 全 tests: 无任何对 `tracks_multibranch` 精确 key set 的断言; `validate_schema_doc.py` 自述只做**顶层 key** 粒度 | 真 (SC-11 的 grep 是唯一文档面守卫, 合理) |
| hermetic 临时仓 (含 `refs/remotes/origin/*`) 可构造 | `tests/test_handoff_multibranch_collision_dedupe.py:208-241` `_build_repo` (`git init` + `update-ref refs/remotes/origin/<branch>`) 可直接复用 | 真; SC-4 另需给 `_GIT_ENV` (`:174-183`) 补 `GIT_AUTHOR_DATE`, 现无日期控制 |
| SC-9 的 monkeypatch 点存在 | `_run` 由 `:122` 导入到模块命名空间, 可 patch `handoff_multibranch._run` | 真 (需按 cmd 选择性伪造, 否则连 for-each-ref 一起打掉) |
| 全部被引用的规范/先例/triage 文件存在 | 逐个 `test -e` | 6/6 存在, 两个 archive 先例目录亦在 |
| 框架约定 (Aria #95) | 本仓非 Next.js/Astro 等 framework 项目 | N/A |

---

## Verdict

**FAIL** — Critical 1 / Major 6 / Minor 3 (issues + risks 计); 另有 2 条 decision 记录 (severity minor, 非缺陷, 不计入)。

rationale: 方案本体 (A + D)、根因诊断、Rule #6 判定、平铺仓向后兼容前提, 我都逐条机械复现且**成立** —— 这份 spec 的分析质量高于均值, F1/F2 两条起草期补充确实扩大了正确的修复面。判 FAIL 的唯一原因是 SC-10: 它把两条「在 plugin cache 里跑才会红」的环境伪失败写成基线已知失败并予以豁免, 而那两条恰是全套件里唯一端到端验证 `scan.py` 快照稳定性的测试, 正对本 spec 自己列为「比原 bug 更坏」的 `-z` 静默失明风险 —— 这是 SC 自身开的假绿口子, 属 critical。六条 major 分三类: 事实错误 (不存在的 `_check_handoff_ancestry`、73 vs 78、pointer 排除的 no-op 误标)、可证伪性 (SC-6 允许一条不调用 collector 的恒绿实现、SC-8 前半条基线已绿)、覆盖缺口 (legacy track_id 相对路径化零 SC) 与构造性风险 (SC-2)。均可在 Phase A 内改 spec 消解, 不需推翻方案。post_spec `blocking: false`, 故本判定不阻断进入 post_planning, 但按横切原则「数据/事实核实结果对 verdict 载重」记 FAIL 而非仅观察。

待 owner 复议 (本席位不裁决): (1) 「待 owner 复议 1」需按 M-3 重写后再问 —— 现状已是任意深度排除, 问题应改为「是否要收窄到只排顶层」; (2) SC-2 是保留 git-history 动态载入还是改冻结 fixture, 涉及测试哲学取舍。

---

## 轮次记录

### Round 1

- Agents: qa-engineer (五席之一, 本报告仅本席位)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 (Decisions 2 / Issues 9 / Risks 1)
- Vote: REVISE
