---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-06T17:05:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — handoff-multibranch-subdir-path-fidelity (Round 1)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文逐字落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager), 五份 frontmatter 15 字段齐全, 0 份需补齐。

**合并规则 (本轮实际执行, 与前一份 post_spec 聚合报告同规则, 供 Round 2 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 (例: SC-10 的「基线计数 73 vs 78」与「两条已知失败豁免的正当性」是两条)。
5. 席位在报告正文明标「不构成 finding / 核验通过不计 finding」的判断**不计入** `found_by`, 但在条目内注明, 以免 Round 2 丢失该信号。
6. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (33 条全部唯一, 无碰撞)。

---

## 审计结论

### Critical (2)

- `63d1ce08` [critical] architecture/§5 消费方枚举/latest_md_writer → handoff.py pointer 往返 — **found_by: tech-lead (critical), backend-architect (critical), code-reviewer (major), knowledge-manager (major) (4/5)**
  `filename` 从 basename 改成相对路径后, D.3 的 `latest_md_writer` 会把 `tracks[].filename` 原样写进 `**Latest**: [archive/x.md](./archive/x.md)` (`latest_md_writer.py:143`); 而**姊妹 collector** `handoff.py` 仍是扁平世界 —— `_parse_latest_pointer` 用 `Path(target).name` 剥掉目录段 (`:288`), 候选集来自**非递归**扫描 (`:300-301` / `:318`) ⇒ 必 miss ⇒ 新增 `handoff_pointer_target_missing` soft_error (`:387-404`) + `latest_source` 由 pointer 退回 mtime ⇒ `scan.py:119` 继续 exit 10。§5 消费方枚举表 (proposal.md:116) 把该消费方判为「相对路径天然正确 / 无影响」—— 四席一致指出该判断只对**人类点击的 markdown 链接**成立, 机器读回链未追。
  tech-lead 是唯一做了端到端实跑的席位: 对 `301641b` 抽取副本打上 proposal 的枚举层改法后跑 `collect_handoff_multibranch` → `write_latest_md` → `collect_handoff` 两个变体 —— 变体 A (全部交接在子目录): collector 侧修复有效 (`filename="sub/2026-09-06-subdir-track.md"`, `legacy_count=0`), 但 `collect_handoff` 返回 `exists=False` / `latest_source=None` / **零 soft_error** (两个 collector 在同一快照里互相矛盾且无任何信号); 变体 B (顶层旧件 + 子目录 active): `handoff_pointer_target_missing`, latest 落到更旧的 done 文档, scan 依旧 exit 10。
  触发条件 = 单 active track 的交接文件位于子目录 (月份分目录布局即命中; knowledge-manager 指出 #195 报告方的 `archive/` 只放旧件, 恰好躲过)。四席一致判为**本变更引入的新失败面** (今天 basename 里没有 `/`, 结构上不可达), 且直接落在本 spec 声称要服务的人群上 —— Impact 里「子目录采用方不再恒 exit 10」与 SC-12 在 D.3 写完 latest.md 后即失效; tech-lead 另指它重开了 H5「pointer 是语义权威、mtime 只是兜底」那条既有修复。
  *severity 分歧注*: code-reviewer / knowledge-manager 记 major, tech-lead / backend-architect 记 critical —— 按规则取最高。
  *修法 (三席各提, 汇总席不裁决)*: (1) 输出面保持 `filename` = basename, 另加 additive 字段 (`relpath` / `path`) 供 git 操作与 `scan.py:186` 消费 (= issue / triage 原案, 见 `109b412c`); (2) 同 cycle 一并修 `handoff.py::_parse_latest_pointer` 与 `_scan_md_files` 的扁平假设; (3) 限定 pointer 只在顶层 track 写真指针。任一路径都需补一条「writer 写出 → collector 读回」的往返 SC。

- `24165c1c` [critical] testing/sc-10 两条基线已知失败豁免的正当性 — **found_by: qa-engineer** — **conflicted: true**
  qa-engineer: SC-10 白纸黑字允许 `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` 与 `Test1210ChannelStabilityUnderOffline` 原样为红, 但这两条是**环境伪失败** —— 根因是 `tests/test_normalize_snapshot.py:272` / `:344` 的 `project_root = Path(__file__).resolve().parents[4]`, 在 plugin cache 里那是 `~/.claude/plugins/cache/10CG-aria-plugin/aria` (**非 git 仓**), `scan.py` 返回 20 (EXIT_HARD_PRECONDITION, `scan.py:120`) ⇒ 两条 assert 挂; 同一份文件 (与本地 `0545f86` diff 无输出) 在真实仓 checkout 下是 **32 tests OK**。后果: 被豁免的恰是全套件里唯一「连跑两次 scan.py 再 diff 归一化快照」的端到端稳定性测试, 正对 Impact.Risk 第三行 (`-z` 解析写错 ⇒ 静默失明) 与本 spec 新增快照键的爆点 —— 属 SC 自身开的假绿口子。修法: 在 `301641b` 真仓 checkout 重测基线并删掉该豁免。
  *conflicted*: tech-lead 就同一 scope 明确判「SC-10 的另两项 (`1571 tests` 与两项已知失败) 我在 `301641b` 抽取副本上复现属实, **不属错误**」; backend-architect / code-reviewer / knowledge-manager 三席也各自复跑并记「1571 与两项已知失败核验一致 / 无误」(三席只作事实复现, 未对豁免的正当性表态)。
  *汇总席记 (不代替裁决)*: 双方对**复现结果**无分歧 —— 五席在 plugin cache / 抽取副本上都拿到 `Ran 1571 ... failures=1, errors=1`。分歧在**该失败是被审对象的属性还是测量环境的属性**。tech-lead 自己报告的另一条数据与 qa-engineer 的诊断同向: 「全量 discover 在**仓内工作树** 1505 OK, 在 `301641b` 抽取副本 1571 (含 proposal 点名的两项失败)」—— 真仓绿 / 非 git 副本红, 与 `parents[4]` 诊断一致, 但 tech-lead 未据此改判。这是本轮**可机械闭合**的冲突: Round 2 在一个真 git checkout 上跑一次 `test_normalize_snapshot.py` 即可定案。

### Major (15)

- `60e465ad` [major] testing/sc-10 改前基线测试计数 (73 vs 78) — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  SC-10 (proposal.md:176) 记「改前基线已实测: 73 tests OK」。五席各自实跑同一条 `python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories`, **无一例外得 `Ran 78 tests ... OK`**: tech-lead 三处 (1.71.1 cache / 仓内工作树 / `301641b` 抽取副本) 均 78 且分模块 21+27+25+5; code-reviewer 在 `301641b` 与工作树 `0545f86` 均 78, 并指出 73 恰是漏掉 `test_track_board_advisories` (5 条); knowledge-manager 另做静态 `def test_` 计数同为 78; 四个测试文件在两 SHA 间字节相同 ⇒ 非版本差异。后果: 基线数写错 5 条会让「5 个测试静默消失」也满足该 SC。按 audit-points 横切「数据量 / baseline 断言规模不符 ⇒ 载重 verdict」条款处理, 这是本轮唯一 5/5 全席独立命中的 finding。

- `352d744d` [major] implementation/§why f1 / §5 / sc-6 引用的 scan.py 函数符号 — **found_by: tech-lead, qa-engineer, code-reviewer (3/5)**
  proposal.md:41 / :115 / :172 三处把 `scan.py` 的 AC-5 检查写成 `_check_handoff_ancestry`, 该符号在 `301641b` 的 `scripts/` 与 `tests/` **全树零命中** (三席各自 grep; code-reviewer 另测该文件无 `ancestry` 标识符), 只命中 proposal 自身三处。真实符号是 `_same_branch_head_unreachable_tracks` (`scan.py:126`, 拼串在 `:186`), 由 `_check_snapshot_self_consistency` (`scan.py:216`) 在 `:255` 调用 ⇒ SC-6 的核验句柄 `scan.py::_check_handoff_ancestry` 按字面不可执行。tech-lead 另指实施者还需知道该函数带的前置门槛才能构造用例 (见 `07dc73c8`)。

- `cc8be8f0` [major] architecture/§what.2 (:95) updated_at 断言与 sc-4 冲突 — **found_by: backend-architect (architecture), code-reviewer (implementation)**
  §What.2 (proposal.md:95) 断言路径修正后 `_get_file_commit_date` 使 `updated_at`「不再取到 mv 提交日」—— 两席各自 hermetic 实跑证伪。backend-architect 构造「顶层 2026-05-09 → `git mv` 进 `archive/` 2026-08-15」: `git log -1 --format=%aI` 对**旧 basename 路径**与**新 archive/ 路径**都返回 `2026-08-15T12:00:00+00:00`, 加 `--follow` 亦同; code-reviewer 独立跑同三种写法得同一结果。真正被修的是 (a)「从未在顶层存在过」的文件从空串变成真日期, (b) git show 成功后改走 frontmatter —— 与本文自身 SC-4 (proposal.md:170)「路径正确后仍取 mv 日, 属预期」**正面冲突**。backend-architect 另指 Why §后果 3 的归因同样错位, 照此措辞写 CHANGELOG 会宣称一个未发生的修复。
  *category 平票注*: backend-architect 记 architecture / code-reviewer 记 implementation, 按席位序取 architecture。

- `9756b070` [major] testing/§1 pointer 任意深度排除 / sc-8 前半 / 待 owner 复议 1 — **found_by: qa-engineer (major), backend-architect (minor), code-reviewer (minor)**
  「pointer 排除改为任意深度」在基线上**已经是现状**, §1 把 no-op 标成了行为变更。现码 `handoff_multibranch.py:277` 先取 `basename = Path(path).name`, `:280` 再比 `_POINTER_FILENAME` —— 本来就是任意深度。qa-engineer 在含 `docs/handoff/latest.md` + `docs/handoff/archive/latest.md` 的临时仓上直调基线 `_list_handoff_files`, 返回 `['2026-05-10-top.md', '2026-05-09-session-end.md']`, 两个 `latest.md` 都已被排除。三层后果: (1) §1 表该行描述错误; (2) SC-8 前半条在 `301641b` 上**已绿**, 违反 Task 1.2「对 301641b 全红且红在正确断言上」, 鉴别力只剩后半条 `archive/latest-notes.md`; (3)「待 owner 复议 1」把现状包装成待定默认, 其反对分支实为**引入**新行为而非保留现状, 应重写为「现状即任意深度, 是否收窄到只排顶层」。
  *found_by 补注*: knowledge-manager 在其报告 Verdict 段作同判并给出同一改写建议, 但明标「不构成 finding」, 依合并规则 5 未计入 found_by。code-reviewer 把该点与 SC-4 / SC-12 合并为一条 risk 提出。

- `ed8b0c48` [major] testing/§1 前缀守卫返回契约与 sc-9 判据强度 — **found_by: backend-architect (testing), code-reviewer (implementation)**
  两层缺口。(a) **契约表达不了**: `_list_handoff_files` 现签名 `tuple[list[str], str | None]` 只有**分支级**错误通道 —— 主循环 (`handoff_multibranch.py:619-626`) 收到非 None 即 `soft_error("handoff_multibranch_ls_tree_failed")` 后 `continue` **跳过整支分支**, 把已枚举的文件全部丢弃; §1 要求的「不以 `docs/handoff/` 开头的行计一条 soft_error 并跳过**该行**」必须改签名或注入 reporter, 而 §What / §Tasks 均未点名该契约变更。(b) **断言无区分度**: SC-9 只断言「有 soft_error + 该项不进 `tracks[]` + 不 crash」, 吞掉整分支的天真实现在单条 fixture 上同样满足 ⇒ 假绿, 且 code-reviewer 指出那种实现**比原 bug 更坏**。修法: SC-9 增加「同分支其它文件仍进 `tracks[]`」断言。
  *category 平票注*: backend-architect 记 testing / code-reviewer 记 implementation, 按席位序取 testing。

- `e21120c6` [major] architecture/f2 非 ascii 现状失效形态 (§why :62 / sc-3 反事实机制) — **found_by: backend-architect**
  hermetic 实证: `git ls-tree -r --name-only` 对任何含非 ASCII 的路径**整条加引号**, `Path(path).name` 得 `2026-\346\265\213\350\257\225.md"`, 在 `handoff_multibranch.py:278` 的 `.endswith(".md")` 处即被 `continue` 丢弃 —— 今天的形态是**静默漏扫**, 不产生 `git show` 失败、不进假 legacy、不推高 exit 10; 非 ASCII 落在**目录段**时同样如此 (basename 得 `x.md"`)。故 proposal.md:62「同样落进那条假 legacy 分支 / 同一 bug 类只是触发条件不同」不成立, SC-3 的反事实机制描述 (「git show 失败」) 须改写。
  *交叉核对注 (汇总席记)*: code-reviewer 的 decision `b14f94c8` 与 tech-lead 的 risk `9d8891b4` 都实测并确认了**转义机制**这一半 (引号 + 八进制, `Path().name` 产出带尾引号的串), 与本条一致; 但两席均未继续测 `.endswith(".md")` 那一格, 因而各自的表述仍沿用 proposal 的「假 legacy 行」框架。三席事实不矛盾, 分歧只在有没有追到下一行 —— Round 2 一条断言即可闭合, 故未标 conflicted。

- `74829542` [major] implementation/unreadable_count 恒存在不变量与 fail-soft 早退路径 — **found_by: backend-architect, knowledge-manager**
  proposal.md:107 自述 `unreadable_count`「恒存在, 默认 0」, 但分支枚举失败的 fail-soft **早退 dict** (`handoff_multibranch.py:586-596`, knowledge-manager 记 `:592`) 与其在 schema 文档里的字面 shape (`references/state-snapshot-schema.md:1136` 逐字列 `{exists, tracks, branches_scanned, legacy_count, collision, errors}`) 都会缺这个键 ⇒ 自述的不变量在错误路径上不成立。§6 文档同步只点了 `:1074` 起的字段表, 无任何 task / SC 承接该路径 (SC-12 只覆盖正常路径)。修法: 代码早退与 schema fail-soft 形状两处同改, 并补一条错误路径 SC。

- `9fee145b` [major] documentation/§6 文档同步面/collector 模块 docstring 与 json-diff-normalizer 键集 — **found_by: knowledge-manager (major), code-reviewer (minor)**
  §6 只点 `references/state-snapshot-schema.md`, 漏 collector 自身的机读契约文档: `handoff_multibranch.py:14-31` 的 top-level 键表缺 `unreadable_count`, `:42-43` 仍写 `"filename": str,  # basename of the handoff file` (本 spec 直接推翻它), `:20` 的 `legacy_count` 注释是 code/doc 早已不一致的那半 (代码在 git-show 失败分支同样 `legacy_count += 1`)。code-reviewer 另指 `references/json-diff-normalizer.md:241` 显式枚举了 `branches_scanned / legacy_count / collision / errors / exists` 键集, 同样未列入。SC-11 只 grep `state-snapshot-schema.md`, 这两处不会转红 (与 `7de08ae9` 的判据不定位问题叠加)。

- `e3935228` [major] documentation/schema :1125 tie-break 论据与 risk 承诺的 schema 说明落点 — **found_by: knowledge-manager**
  两半。(a) `references/state-snapshot-schema.md:1125` 现存论据「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one」在相对路径下**直接变假** (`archive/` 的 `a` = 0x61 > 数字) —— 不改就是把一条错误不变量留给下一个动排序的人。(b) proposal.md:140 承诺「缓解: SC-7 用定向用例钉住**并在 schema 文档写明**」, 但 §6 / Task 4.1 / SC-11 四项清单里没有这个落点。

- `6b713e2f` [major] documentation/tasks 5.1/5.2 发版同步面 (主仓版本引用面) — **found_by: knowledge-manager**
  Task 5.1/5.2 只列 aria 侧「版本 SOT 5 文件 + CHANGELOG」与「主仓 spec/gitlink」, 漏 CLAUDE.md「发布同步面」要求的主仓版本引用面: root README badge 与正文版本行 (`README.md:8,242`)、i18n README 的 `translated-from` marker、`docs/architecture/system-architecture.md:189`、`docs/architecture/version-scheme.md:23`。这四处由三条 **enabled** custom check 兜底 (`.aria/state-checks.yaml:88 m6-version-badge-match` / `:141 i18n-readme-translation-currency` / `:372 plugin-version-arch-docs-match`, 判据均为「与 `aria/.claude-plugin/plugin.json` 比对」) ⇒ 归档闸会红; 且本轨与同伴 v1.71.1 先后落地时这些行要连动两次, 不写进 tasks 极易停在 v1.70.0 / v1.71.1。

- `4c05b95a` [major] architecture/ship 顺序与主仓 gitlink 归属 — **found_by: tech-lead** — **conflicted: true**
  tech-lead: proposal 的 ship 计划建立在**陈旧的 origin 视图**上。实测 `origin/master` = `9f25a66`「Merge pull request #202 … from feature/a1-entry-claim-duplicate-work-guard」(2026-09-06T15:27:16Z), `git ls-tree origin/master aria` 已是 `301641b` (其中 `4c3c826` 即「主仓同步 aria-plugin v1.71.1 — gitlink 301641b + 16 处版本点」); 而 proposal 于 15:46:20Z 提交 (本地 `origin/master` ref 早在 15:31:43 已更新) 仍写「尚未开 PR / gitlink 仍指 `0545f86` / 本 spec 的 gitlink bump 排在其 PR 之后」(proposal.md:9,158,197), 并把一个已不存在的选择升级给 owner。本地 master 与 origin 已分叉。后果: 排队前置是幻影; 照本地基线做主仓同步会把 gitlink 从 `301641b` **回退**。
  *conflicted*: knowledge-manager 在其 Sibling probe 段就同一 scope 判「与头部『同伴 PR 尚未开』『gitlink 仍指 0545f86』**一致**」, 依据是 `git ls-tree HEAD -- aria` = `0545f86` + 主仓 open PR = `[]`。
  *汇总席记 (不代替裁决)*: 两席量的不是同一个 ref —— knowledge-manager 读**本地 HEAD**, tech-lead 读 **origin/master**; 而 knowledge-manager 自己测到的「主仓 open PR = `[]`」恰与 tech-lead 的「PR #202 已 merge」相容 (已合并的 PR 不再 open)。这同样是**可机械闭合**的冲突: 一条 `git ls-tree origin/master aria` 即可定案。同族结论已在本仓上一份 post_spec 聚合报告 (`pre-merge-completeness-gate-change-scope`, finding `eaceacdd`) 独立出现过。

- `07dc73c8` [major] testing/sc-6 反事实前提 (tracks_data 来源) 与 scan.py 四道前置 — **found_by: qa-engineer**
  SC-6 只说「对含子目录 track 的**快照**跑」, 而 `_same_branch_head_unreachable_tracks` 的签名正好只吃 dict ⇒ 最省事的实现是手搓 `{"tracks":[{"filename":"archive/x.md",...}]}`, 那样 collector 根本没被调用, 「退回 basename ⇒ 空 SHA ⇒ 红」的反事实为假, SC 恒绿。另有四道前置未点名 (`scan.py:166-183`): `current_branch` 非空 / 非 `detached_head` / `enforced_remotes` 非空 / `t["branch"] == current_branch` —— 任一没配到, 函数在早返回 `[]` 上假绿。修法: SC-6 明确要求 tracks_data 由同一临时仓上的 `collect_handoff_multibranch` 端到端产出, 并列出四道前置。
  *found_by 补注*: tech-lead 在 `352d744d` 条目内附带点出「实施者需要知道那两道前置才能构造用例」, 未单列 finding。

- `7d76ccad` [major] testing/§2 _make_legacy_track_id 相对路径化的 sc 覆盖缺口 — **found_by: qa-engineer**
  §2 (proposal.md:96) 明写改为 `legacy:<branch>:<relpath>` 并给了动机 (两个子目录下同名文件否则产生同一 legacy track_id, 被 dedupe 当成同一 track), 但 SC-1~SC-9 **无一条断言它**: SC-1 是非 legacy 真 track, SC-5 断言不可读文件**不产生** legacy 行, 其余不涉及。改完后唯一还能产 legacy 行的路径是无 frontmatter 分支 (`handoff_multibranch.py:683-700`) —— 恰恰就是这个碰撞场景, 零覆盖。修法: 补一条 SC (两份 `archive/x.md` 与 `x.md` 皆无 frontmatter ⇒ 两条不同 `track_id`, dedupe 不折叠; 反事实: 用 basename ⇒ 同 id ⇒ 折叠成一条 ⇒ 红)。

- `353ad1ca` [major] testing/sc-2 动态载入 301641b 原实现的可行性 (risk) — **found_by: qa-engineer (major), tech-lead (minor), backend-architect (minor)**
  SC-2「测试内以 `git show 301641b:` 取原实现动态载入」未验证可行性, 而它是 top-risk (`-z` 解析写错 ⇒ 静默失明) 的唯一缓解。三层障碍, qa-engineer 实跑两种载入路径确认: (a) 朴素 `exec` 直接 `ImportError: attempted relative import with no known parent package` (collector 在 `:120-127` 用 `from ._common import` / `from .handoff import`); (b) 必须建 `collectors.<name>` 包上下文**并手动设 `__file__`** 才成功 —— 否则 `:141` 的 `_Path(__file__)` 抛 NameError, 而 `:152` 只 `except ImportError` 接不住; (c) 引入 git 历史依赖, 而插件把 `tests/` 分发到**无 `.git`** 的 cache 目录 (基线恰恰是在那里测的), tech-lead 另指组织 CI checkout 约定为 `fetch-depth: 1` (`.forgejo/workflows/issue-triage-tests.yml:33-35`) ⇒ 异地必 error。tech-lead 另核: 本套件 `tests/` 全树零 `importlib` / `exec_module`, 无先例。三席修法一致: 改用已存在的冻结语料 / vendored baseline 比对 (仓内已有 `tests/fixtures/freeze_corpus.py` + `handoff-tracks-frozen-*.json` 形态), 或 `skipUnless(是 git 仓)` 并另留一条不依赖 git 历史的等价断言。backend-architect 另指其反事实已被 SC-1 / SC-3 冗余覆盖, 可降级。

- `50bb5886` [major] documentation/头部基线冻结行 (proposal.md:9) 两 sha 差异概括 — **found_by: tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5)**
  「两 SHA 间只新增了 7 个 a1-entry 相关测试文件, 均不触碰本触点」与实读不符。四席各自跑 `git diff --name-status 0545f86 301641b`: **29 文件变更** (knowledge-manager 拆为 5 added + 24 modified; tech-lead 另计 2462 行新增, 其中新增测试文件 5 个), modified 含 `lib/collision.py` / `lib/identity.py` / `lib/claim_lifecycle.py` / `lib/constants.py` / `phase1_gate.py` / `scripts/lib/spec_complete.py` / `coordination_probe.py` 与 6 份 SKILL.md。knowledge-manager 与 tech-lead 同指要害: `lib/collision.py` 正是 SC-7 所测 dedupe 分组键 (`identity_key` / `split_owner_container`) 的实现所在, 说「只新增测试文件」会让复审者误判基线增量对本触点完全惰性而跳过复核。**载重结论侧无损**: 5 个触点文件 `git diff --stat` 确为空, 「行号在两 SHA 一致」四席独立复核成立 (见 `1883bf5b`)。
  *code-reviewer 同条目内的第二处转述偏差*: proposal.md:28 称 `_get_file_commit_date`「issue 未点名」, 但 issue-195 正文第 21 行已明确点名 (承袭 triage 措辞, 属 memory `feedback_spec_inherits_upstream_dec_errors` 形态)。
  *category 注*: tech-lead 把本条与 `60e465ad` 合并为一条 testing finding 提出, 其余三席记 documentation, 按多数取 documentation。

### Minor (10)

- `265330d9` [minor] documentation/sc-4 判据强度与 why 第三层后果的表述张力 (risk) — **found_by: tech-lead (risk), qa-engineer (issue), code-reviewer**
  SC-4 标题写「`updated_at` 不再取 mv 日期」, 正文却自认无 frontmatter 分支改后仍取 mv 日 (`git log -1` 的真值) ⇒ 该半条**改前改后同值**, 对本变更零鉴别力, 却没有像 SC-7 那样标「现状记录性断言」(qa-engineer); 是唯一没写反事实的行为型 SC (code-reviewer)。tech-lead 补另一侧张力: Why (proposal.md:35) 把 mv 日期失真列为**要修的**第三层后果, SC-4 (proposal.md:170) 又把它定为**预期真值** —— 两者都对 (有 frontmatter 走 frontmatter, 无 frontmatter 只能靠 `git log -1`, `--follow` 也救不了「最近一次触碰该路径」的语义), 但报告方归档进 `archive/` 的正是老格式交接, 他们抱怨的那一半可能仍在, 该残余既未进 Impact/Risk 也未列待 owner 复议。风险: Phase B 读标题去给 `_get_file_commit_date` 加 `--follow`。
  *type 平票注*: tech-lead 记 risk / qa-engineer 记 issue, 按席位序取 risk。code-reviewer 把本点与 `9756b070` / `37de67cd` 合并为一条 risk 提出。

- `5f1ff0ce` [minor] implementation/§1 (:86) 前缀剥离字面量 = 第五处硬编码前缀 — **found_by: qa-engineer**
  §1 用字面量 `path[len("docs/handoff/"):]` 剥前缀, 等于**新造第五处硬编码前缀** —— 正是本 spec 自己认定的根因族 (「四处硬编码前缀」)。应从 `_HANDOFF_TREE_PATH` 派生 (`path[len(_HANDOFF_TREE_PATH) + 1:]` 或 `PurePosixPath.relative_to`)。顺带勘正既有注释错误: `handoff_multibranch.py:177` 写「trailing slash required by git ls-tree --name-only」, 而 `:178` 常量值 `"docs/handoff"` 并无斜杠。

- `9d8891b4` [minor] implementation/f2 修复覆盖边界 (非 utf-8 文件名) (risk) — **found_by: tech-lead (implementation), code-reviewer (testing)**
  `_common.py` 的 `_run` 用 `encoding="utf-8", errors="replace"` (tech-lead 记 `:355-360`, code-reviewer 记 `:406-413`) ⇒ `-z` 方案对可解码 UTF-8 路径可行 (F2 修法成立), 但**真正非 UTF-8 字节**的文件名解码即失真、拼不回 git 对象: 修后它从「假 legacy 行」变成「新的 unreadable 分支 + 继续 exit 10」, 并非修好。同类文件名在 `handoff.py:308-322` 是**显式跳过**的既有先例。两席修法一致: schema 与 CHANGELOG 写明 F2 只覆盖「可解码 UTF-8 的非 ASCII 名」, 并考虑对不可解码名显式跳过而非计入 `unreadable_count`, 以免后续被当成回归。
  *category 平票注*: tech-lead 记 implementation / code-reviewer 记 testing, 按席位序取 implementation。

- `c45d191e` [minor] documentation/rule6_note 对 sc 反事实的概括 (:186) — **found_by: backend-architect**
  rule6_note 称「SC-1~SC-9 逐条对应一个行为改动, 每条附反事实」, 但 SC-2 自述「零行为变化」、SC-7 自述「现状记录性断言」, 两条在 baseline 上本就为绿, 属回归锁而非 baseline-failing。substitute 实体仍由 SC-1/3/4/5/6/8/9 七条撑住, **结论不倒**, 措辞需收紧。

- `2962102f` [minor] documentation/rule6_note skill.md tracks_multibranch 出现处计数 (:184) — **found_by: qa-engineer**
  rule6_note 称 SKILL.md「只在 collector 清单里出现 `tracks_multibranch` 一词」; 实测 **3 处** —— `SKILL.md:117` (collector 清单)、`:149` 与 `:153` (coordination 闸门接线, 属运行时指令面)。判定**结论仍成立** (`lib/collision.py:480-485` 排除 `owner_container == "unknown"`, 而假 legacy 行的 `owner_container` 恒 `unknown` ⇒ 删掉它们不动 `collision.kind`, 闸门面不受影响), 但 Rule #6 / Rule #10 的判定前提写错值得勘正。

- `07e3a5f1` [minor] documentation/代码行号引用精度 (:275 → :277) — **found_by: backend-architect, code-reviewer**
  proposal.md:26 写 `:275 basename = Path(path).name`, 实际在 `:277` (`:275` 是 `if not path:`); code-reviewer 另测 docstring 引用 `:244-250` 实际落在 `:246-247`。两席各自逐条核对同段其余行号 (`:178` / `:240-288` / `:301` / `:321` / `:329-336` / `:428-457` / `:637-658` / `:683-700` / `scan.py:186` / `schema:1074-1136`) **均无误**。

- `507ff38c` [minor] architecture/§5 track_board 行「无影响」表述 (间接经 dedupe 排序键) — **found_by: backend-architect (issue), code-reviewer (risk)**
  §5 该行写「不读 `filename` 字面 ⇒ 无影响」, 但 `track_board.py` 直接 import 并应用 collector 的 `dedupe_latest_per_track_container` (backend-architect 记 `:742-760`, code-reviewer 记 `:183,187-188`), 经四级排序键的第 3 级 (`_dedupe_sort_key`, `handoff_multibranch.py:541` 用 `max`) **间接消费** `filename` ⇒ Impact 第 1 条的 tie-break 风险同样落到看板 collision 输入的代表行选择上; code-reviewer 指出同组两行的 `status` / `phase` 可以不同 ⇒ 渲染同样改变。backend-architect 估实际差异在三重并列下近乎为零, 建议表述收紧为「间接经共享 dedupe 生效, 语义由 SC-7 覆盖」而非删除该行。
  *type 平票注*: backend-architect 记 issue / code-reviewer 记 risk, 按席位序取 issue。
  *与 decision 群的关系 (汇总席记)*: qa-engineer 与 knowledge-manager 各自复核「`track_board.py` 不读 `filename` **字面**」为真 (见 `1883bf5b` / `b14f94c8` 相关记述) —— 与本条不矛盾, 两侧量的是不同谓词 (字面读取 vs 经共享 dedupe 的间接消费)。

- `b550edff` [minor] documentation/references 现场行 #182 引用 (proposal.md:206) — **found_by: knowledge-manager**
  `aria-plugin#182 (handoff status 不收口, 相邻但不同根因)` 属误标 —— Forgejo API 实查 #182 = 「[缺陷][state-scanner] issue_scan 无分页且 limit=20 硬顶 —— open_count 静默截断 40%」(open), 与 handoff 无关。同行 `#155 (dedupe 由来)` 正确 (closed)。误标使「邻近 issue 已排查」这条信号不可信。

- `7de08ae9` [minor] testing/sc-11 文档机检判据 (grep -c basename) (risk) — **found_by: knowledge-manager**
  `grep -c 'basename' collectors/handoff_multibranch.py` 相对基线「减少」是**不定位**的代理判据 (当前 7 处: 模块 docstring `:42`、函数 docstring `:246`、循环体 `:277,278,280,284,288`)。新实现仍需 basename 做 `.md` 过滤与 pointer 排除, 只改 `:246` 一句即可让计数下降 ⇒ 结构上钉不住 `:42` 的漏改 (与 `9fee145b` 直接叠加)。建议换成两条具体断言: 「`callers compose the full git-object path` 消失」+「模块 docstring `filename` 行含『相对』」。

- `37de67cd` [minor] testing/sc-12 基线取自活文件 state-snapshot.json (risk) — **found_by: code-reviewer**
  SC-12 拿**活文件** `.aria/state-snapshot.json` (14:22Z 生成, 1408 tracks) 当基线, Phase B 期间只要 origin 上多一份交接就会假红。更稳的做法是同工作区跑 baseline 与改后各一次。(与 memory `feedback_baseline_corpus_stat_must_run_against_frozen_snapshot` 同型。)

### Decisions (6 — 1 条 major + 5 条 minor; 按前一轮同规则**不计入**上表缺陷 severity 计数)

- `109b412c` [major] architecture/方案 a 形态取舍与来源偏离 (候选表 + additive 契约声明) — **found_by: tech-lead (decision/architecture/major), backend-architect (issue/documentation/major)**
  **本条是 `63d1ce08` (critical) 的两席共同指认的根源, 需 rework, 只是 type 平票落在 decision 上 — 见下方口径注。**
  issue-195 原文 A 案与 triage 修法倾向都写「`filename` / `track_id` 等需要 basename 的字段**另行派生**」/「`filename` 字段另派生 basename」(即相对路径只进 git 操作面); 本 spec 直接改**既有输出字段**的语义 (schema 文档 `:1110` 现写「basename of the handoff file」), 与两个来源的关键分句相反。proposal.md:72 却称「issue 与 triage 均倾向此案」(backend-architect), 候选方案表 proposal.md:70-75 未把「另派生」变体列出供 owner 对比 (tech-lead), 既未声明偏离也未进「待 owner 复议」。tech-lead 另指契约声明自相冲突: 仍宣称「additive-only 演进契约、`snapshot_schema_version` 保持 1.0」(proposal.md:130), 而改既有字段取值语义不是 additive。
  *口径注 (汇总席记)*: `type` 与 `category` 均 1-1 平票 (tech-lead decision/architecture vs backend-architect issue/documentation), 按合并规则 2 取席位序在先的 tech-lead ⇒ 落 decision/architecture。为与前一份 post_spec 聚合报告口径一致 (decisions 不计入缺陷 severity 表), 本条**未计入** Major 15 那一格; 但两席均标 major、两席均称其为 critical 项的直接来源, 故**照常列入 Rework 清单**。若 owner 或 Round 2 认为该口径失真, 请按 `issue|major` 重记 —— 汇总席不自行改规则。

- `0f9dc120` [minor] testing/rule6_note 判据表选行 (第一行 描述性 ⇒ substitute) — **found_by: backend-architect (testing), qa-engineer (architecture), code-reviewer (testing), knowledge-manager (documentation) (4/5)**
  Rule #6 判定**核实通过**, 四席结论一致且互不依赖。判据面: SOT 决策表第一行 (`standards/conventions/skill-benchmark-exemption.md:28`) + `:63-64` 已把「纯代码 collector 层」同形变更裁为 substitute (code-reviewer / knowledge-manager 各自引同一先例); backend-architect 另引 `:24-30,68-74` 的 worked example。事实面: `aria-plugin-benchmarks/ab-suite/state-scanner.json` (15518 B) 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词命中**全 0** —— 四席各自实测 (qa-engineer 用 `str.count`, 并指出连 `handoff` 一词也是 0); 本 spec 不触 SKILL.md 指令面与 `description` ⇒ 不落第三行, 无需开套件缺口 issue, 不需跑 AB。
  *found_by 补注*: tech-lead 在其「核验通过、不计 finding 的判断」清单第 5 项作同判 (明标不计 finding), 依规则 5 未计入。

- `1883bf5b` [minor] architecture/基线冻结 / 平铺仓零变化前提 / 根因复现 — **found_by: backend-architect, qa-engineer, code-reviewer, knowledge-manager (4/5)**
  三层事实底座四席独立复核**全部成立**。(a) 基线冻结: `git -C aria rev-parse origin/master` = `301641b`, 5 个触点文件 `git diff --stat 0545f86 301641b` 为**空** ⇒ 「行号跨两 SHA 一致」成立 (与 `50bb5886` 的旁证失真不冲突: 错的是概括, 不是载重结论)。(b) 平铺仓零行为变化前提: 本仓 `docs/handoff/` 185 项、**0 子目录 / 0 非 ASCII** (qa-engineer 另扫**全部 origin 分支**前 25 条同此结论); 两份冻结语料 (`tests/fixtures/` 与 `.aria/repro/`) 各 996 行, `filename` 含 `/` 0 条、非 ASCII 0 条 ⇒ §7「冻结语料不需重生成」成立。(c) 根因复现: qa-engineer 在临时仓上直调 `collect_handoff_multibranch`, **逐字复现**假 legacy 行 (`track_id=legacy:master:2026-05-09-session-end.md`, `status=legacy`, `updated_at=""`) 与 `handoff_multibranch_git_show_failed`, `scan.py` 对该仓 exit 10 且仅此一条 soft error ⇒ SC-12 后半条「改后 exit 0」可达; 另测活体 `.aria/state-snapshot.json` 的 252 条 legacy 全部来自无-frontmatter 分支 (`errors` 长度 0) ⇒ 变更 4 不动本仓 `legacy_count`。code-reviewer 另核认领记录 `refs/aria/coordination:claims/bfe8285d/s-e4b1@1447.yaml` 与 triage 2/2 hit_rate 属实。
  *found_by 补注*: tech-lead 在其「核验通过」清单第 1、6 项作同判 (明标不计 finding); backend-architect 报告正文另有 2 条同族 decision 未列入其结构化清单。

- `b14f94c8` [minor] implementation/起草期新事实 f1 (scan.py:186 第四硬编码点) 复核 — **found_by: code-reviewer, knowledge-manager**
  F1 **成立**: `scan.py:186` 独立硬编码 `docs/handoff/{filename}` 是第四处前缀点; `:198-200` 对空 SHA `continue` 并在注释里判定为「a real answer」⇒ 路径拼错后**静默跳过**, 无任何告警 (两席各自实读, knowledge-manager 记 `:199-200`)。knowledge-manager 另核 `track_board.py:254,559` 的 HANDOFF 列只吃 `updated_at`, 确不读 `filename` 字面 (其 `:19` docstring 的「或 filename stem」是**既有陈旧注释**, 非本 spec 引入)。code-reviewer 另核 F2 的转义机制成立 (见 `e21120c6` 的交叉核对注)。
  *found_by 补注*: backend-architect 报告正文 Decisions 段有同判条目 (「F1 分析准确」) 但未列入其结构化清单; tech-lead「核验通过」清单第 2 项亦同判 (全 `.py` 树只有四处硬编码前缀, 无第五处)。

- `270a0181` [minor] documentation/rule 10 闸门权限 (审计计划 + a.1.0 行) — **found_by: knowledge-manager**
  `.aria/config.json` 实读: `audit.checkpoints` = post_brainstorm off / post_spec convergence / post_planning convergence / mid_implementation · post_implementation · pre_merge · post_closure off, `teams.post_spec` 5 席 —— 与 proposal.md:12-13 的「审计计划」与「A.1.0 未跑头脑风暴」**逐项一致**, 全部落 Rule #10 白名单第一类 (config 显式 off), 无 AI 自行豁免。

- `6709ffb4` [minor] documentation/头部 linked issue 机械判据 (proposal.md:6) — **found_by: knowledge-manager**
  spec-drafter 写法三条全过: `linked_issue_field_probe --emit-arg` 输出 `10CG/Aria#195`; check 模式 FAIL 的 6 项均为既有 M6/M7 proposal, 本文件不在内; 紧邻的 `> **Issue**: [Aria#195](url)` 链接行 (proposal.md:7) 未干扰 E0 抽取。

---

## Verdict

**FAIL** — Critical 2 / Major 15 / Minor 10 (缺陷类 = issue + risk, 共 27 条; 另有 6 条 decision 不计入, 其中 1 条 major 见 `109b412c` 口径注)。

rationale: 两条 Critical 分别落在**被审对象**与**它自己的验收判据**上, 且互不重叠。

- **`63d1ce08` (方案面)**: 四席一致 —— 把 `filename` 的语义从 basename 改成相对路径, 会让 D.3 的 `latest_md_writer` 写出的 pointer 被姊妹 collector `handoff.py` 读不回来 (剥目录段 + 非递归扫描), 于是**同一类 exit 10 换个错误码复发**, 而 §5 消费方枚举表恰恰把这个消费方判成「天然正确 / 无影响」, 实施者不会去碰它。这不是推理: tech-lead 打上 proposal 的改法后端到端跑了两个变体, 一个静默自相矛盾 (`handoff.exists=False` 且零 soft_error), 一个报 `handoff_pointer_target_missing` 并把 latest 指到更旧的文档。影响正好落在本 spec 声称要服务的人群 (子目录布局采用方) 上, 且 `109b412c` 显示该取舍与 issue / triage 原案的关键分句相反、未披露。
- **`24165c1c` (判据面, conflicted)**: qa-engineer 指 SC-10 豁免的两条「基线已知失败」是 plugin cache 非 git 仓造成的环境伪失败 (`parents[4]` → `scan.py` rc=20), 真仓 checkout 下 32/32 OK —— 被豁免的恰是全套件唯一的端到端快照稳定性测试, 正对本 spec 自列为「比原 bug 更坏」的 `-z` 静默失明风险。tech-lead 就同 scope 判「不属错误」, 故标 conflicted; 但 tech-lead 自己报的「仓内工作树 1505 OK / 抽取副本 1571 含两项失败」与该诊断同向。Round 2 一次真仓 checkout 跑测即可定案。

15 条 Major 集中在三类, 均可在 Phase A 内改 spec 消解, **不需推翻方案骨架**:

1. **事实与计数错误** (5 条): SC-10 基线 73 vs 78 (5/5 全席实测)、`_check_handoff_ancestry` 符号不存在 (3 席)、§What.2 的 mv 日期因果被 hermetic 实跑证伪且与自身 SC-4 冲突 (2 席)、F2 现状失效形态实为静默漏扫而非假 legacy (1 席)、头部基线冻结行 29 文件 vs 7 文件 (4 席)。
2. **判据可证伪性与覆盖缺口** (5 条): SC-8 前半在基线已绿 (pointer 排除本就任意深度)、SC-9 无法区分「吞整分支」的错误实现、SC-6 允许一条不调用 collector 的恒绿实现、`_make_legacy_track_id` 相对路径化零 SC、SC-2 动态载入在分发副本与浅克隆 CI 必 error。
3. **同步面与不变量清单不全** (5 条): `unreadable_count`「恒存在」在 fail-soft 早退路径不成立、§6 漏 collector 模块 docstring 与 json-diff-normalizer 键集、schema `:1125` 的 tie-break 论据在相对路径下变假、Task 5.1/5.2 漏主仓四处版本引用面 (三条 enabled check 会红)、ship 顺序基于陈旧 origin 视图 (conflicted, 照字面执行会把主仓 gitlink 从 `301641b` 回退)。

按 report-storage.md §Verdict 计算, ≥1 Critical ⇒ FAIL。post_spec 的阻塞行为是 `blocking: false` (report-format.md 阻塞行为表), 故本 FAIL **不硬阻断**流程; 但按 Rule #10, 该判定不得由 AI 自行降格 —— 两处 conflicted (`24165c1c` / `4c05b95a`) 与 `109b412c` 的口径均需 owner 或 Round 2 拍板后再进 Phase B。

正面记录 (不因 FAIL 抹掉): 本 spec 的**事实底座与方案方向**在四席独立复核下成立 (`1883bf5b`) —— 基线冻结 5 触点零 diff、平铺仓与两份冻结语料零子目录零非 ASCII、根因假 legacy 行与 exit 10 在临时仓逐字复现; Rule #6 判定四席一致核实通过 (`0f9dc120`); F1 是起草期的**真增量**发现 (`b14f94c8`, 三席复核); Rule #10 与头部机械判据全部合规 (`270a0181` / `6709ffb4`)。五席一致认为缺陷集中在 `filename` 语义取舍的下游影响与 SC 判据强度, 不在调研质量 —— qa-engineer 明记「这份 spec 的分析质量高于均值」。

计算依据:
- Critical issues: 2 (2 issue + 0 risk)
- Major issues: 15 (14 issue + 1 risk)
- Minor issues: 10 (6 issue + 4 risk)
- Decisions (不计入): 6 (1 major + 5 minor)

---

## 轮次记录

### Round 1

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (五席各自独立报同一结论; knowledge-manager 另列扫描面 —— `openspec/changes/` 9 个在制 spec 无第二份指向 Aria#195, 主仓 open PR = `[]`, aria remote 仅同伴 `feature/a1-entry-claim-duplicate-work-guard` 分支)
- Conclusions: 33 (去重前 60) —— Critical 2 / Major 15 / Minor 10 / Decisions 6
- Delta vs 上轮: N/A (Round 1, 上轮 keys = null, 结构上无法判定收敛)
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: FAIL 3 (tech-lead / backend-architect / qa-engineer) + PASS_WITH_WARNINGS 2 (code-reviewer / knowledge-manager); 后两席各自 Critical=0, 仍按横切检查原则载重投 REVISE
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 1 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 60 / 33 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 2 / 15 / 10 |
| 其中 issue / risk | 22 / 5 |
| Decisions (不计入缺陷计数) | 6 (1 major `109b412c` + 5 minor) |
| Conflicted 对 | 2 (`24165c1c` SC-10 豁免正当性 · `4c05b95a` gitlink 归属) —— 两条均可机械闭合 |
| 5/5 全席独立命中的 finding | 1 (`60e465ad`) |
| 4/5 席命中的 finding | 4 (`63d1ce08` · `50bb5886` · `0f9dc120` · `1883bf5b`) |
| finding id 碰撞 | 0 (33 条全部唯一, python3 实算) |
| unanimous_pass | false |
| converged | false (Round 1: 上轮 keys = null, 且 unanimous_pass=false) |
| 收敛轮次 | N/A |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的条目按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `63d1ce08` | critical | tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5) | **待 owner 复议**: 三选一 —— (a) `filename` 保持 basename + 另加 additive `relpath`/`path` 字段供 git 操作与 `scan.py:186` 消费 (= issue/triage 原案, 兼容面最干净); (b) 同 cycle 一并修 `handoff.py::_parse_latest_pointer` 与 `_scan_md_files` 的扁平假设; (c) 限定 pointer 只在顶层 track 写真指针。任一路径都须补「writer 写出 → collector 读回」的往返 SC, 并按结果订正 §5 该行与 Impact 里「不再恒 exit 10」的措辞 |
| 2 | `24165c1c` | critical | qa-engineer (**conflicted** vs tech-lead) | 在 `301641b` 的**真 git 仓 checkout** 重测全量基线, 删掉 SC-10 对两条已知失败的豁免; 若届时确有真失败再逐条 `git log -- <file>` 归因。该冲突可用一次跑测机械闭合 |
| 3 | `60e465ad` | major | 5/5 全席 | SC-10 基线数改记 **78** (21+27+25+5), 并注明基线测于 `301641b` 的真仓 checkout; 或把命令收敛成实际测过的模块集 |
| 4 | `352d744d` | major | tech-lead, qa-engineer, code-reviewer | 全文把 `_check_handoff_ancestry` 更正为 `_same_branch_head_unreachable_tracks` (`scan.py:126`), 同步 SC-6 的核验句柄 |
| 5 | `cc8be8f0` | major | backend-architect, code-reviewer | 重写 §What.2 第二条: 路径修正的真实收益是「从未在顶层存在过的文件由空串变成真日期」+「git show 成功后走 frontmatter」; mv 过的无 frontmatter 文件仍为 mv 日 (与 SC-4 一致); 同步订正 Why §后果 3 的归因, 避免 CHANGELOG 宣称未发生的修复 |
| 6 | `9756b070` | major | qa-engineer, backend-architect, code-reviewer | 订正 §1 该行 (任意深度排除是**现状**非行为变更); SC-8 前半改为记录性断言或删除, 鉴别力交给 `archive/latest-notes.md` 那半; 「待 owner 复议 1」重写为「是否要收窄到只排顶层」再问 owner |
| 7 | `ed8b0c48` | major | backend-architect, code-reviewer | §1 前缀守卫补契约说明 (`_list_handoff_files` 返回值改为携带 per-item 错误, 或调用方接收部分成功); SC-9 增加「同分支其它文件仍进 `tracks[]`」断言, 否则吞整分支的实现照样绿 |
| 8 | `e21120c6` | major | backend-architect | 改写 proposal.md:62 的 F2 现状描述 (今天是 `.endswith(".md")` 处的**静默漏扫**, 不产生假 legacy / 不推高 exit 10) 与 SC-3 的反事实机制 (不能写「git show 失败」) |
| 9 | `74829542` | major | backend-architect, knowledge-manager | 把 fail-soft 早退路径 (`handoff_multibranch.py:586-596`) 与 schema `:1136` 的字面 shape 一并纳入变更面, 使 `unreadable_count`「恒存在」成立; 补一条错误路径 SC (SC-12 只覆盖正常路径) |
| 10 | `9fee145b` | major | knowledge-manager, code-reviewer | §6 文档同步面补入 collector 模块 docstring (`:14-31` 键表加 `unreadable_count`、`:42-43` 的 `filename` 契约、`:20` 的 `legacy_count` 注释) 与 `references/json-diff-normalizer.md:241` 键集; SC-11 相应扩 grep 面 |
| 11 | `e3935228` | major | knowledge-manager | 订正 `state-snapshot-schema.md:1125` 的 tie-break 论据 (相对路径下「字典序更大 = 更晚」不再成立); 把 proposal.md:140 承诺的 schema 说明落成具体 task / SC |
| 12 | `6b713e2f` | major | knowledge-manager | Task 5.1/5.2 补主仓版本引用面: `README.md:8,242` badge 与正文版本行、i18n README `translated-from` marker、`system-architecture.md:189`、`version-scheme.md:23` (对应三条 enabled check `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match`) |
| 13 | `4c05b95a` | major | tech-lead (**conflicted** vs knowledge-manager) | 先用 `git ls-tree origin/master aria` 定案实况, 再据实重写头部基线行、Task 5.2 与「待 owner 复议 5」; 无论结论如何, Phase C 前须核 gitlink 不得从 `301641b` 回退 |
| 14 | `07dc73c8` | major | qa-engineer (+ tech-lead 附带) | SC-6 明确要求 `tracks_data` 由同一临时仓上的 `collect_handoff_multibranch` **端到端产出** (禁手搓 dict), 并列出 `scan.py:166-183` 的四道前置 (current_branch 非空 / 非 detached / enforced_remotes 非空 / branch 相等) |
| 15 | `7d76ccad` | major | qa-engineer | 补一条 SC 覆盖 `_make_legacy_track_id` 相对路径化: 两份无 frontmatter 的 `archive/x.md` 与 `x.md` ⇒ 两条不同 `track_id` 且 dedupe 不折叠 (反事实: 用 basename ⇒ 同 id ⇒ 折叠 ⇒ 红) |
| 16 | `353ad1ca` | major | qa-engineer, tech-lead, backend-architect | SC-2 改用已存在的冻结语料 / vendored baseline 比对 (或 `skipUnless(是 git 仓)` + 一条不依赖 git 历史的等价断言); 现方案在无 `.git` 的插件分发副本与 `fetch-depth: 1` 的 CI 上必 error |
| 17 | `50bb5886` | major | tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5) | 头部基线冻结行改记实况 (29 文件变更 / 5 added + 24 modified, 含 `lib/collision.py` 等生产文件), 保留「5 触点零 diff ⇒ 行号一致」的载重结论; 顺带订正 proposal.md:28「issue 未点名 `_get_file_commit_date`」 |
| 18 | `109b412c` | major (decision) | tech-lead, backend-architect | **待 owner 复议**: 把「`filename` 另派生 basename」变体补入候选方案表并说明取舍; 订正 proposal.md:72「issue 与 triage 均倾向此案」的转述; 重新评估 §7「additive-only / schema_version 保持 1.0」的声明是否与改既有字段语义相容。本条与 `63d1ce08` 同源, 两者应一并裁决 |

Minor (10 条) 不逐条列入本表, 建议随上述 rework 一并顺手订正: `265330d9` (SC-4 加记录性标注 + 反事实, mv 残余入 Impact/待复议) · `5f1ff0ce` (前缀剥离从 `_HANDOFF_TREE_PATH` 派生, 顺带修 `:177` 注释) · `9d8891b4` (schema/CHANGELOG 写明 F2 只覆盖可解码 UTF-8 名) · `c45d191e` (rule6_note 收紧 SC 反事实的概括) · `2962102f` (rule6_note 勘正 SKILL.md 3 处) · `07e3a5f1` (`:275` → `:277`, `:244-250` → `:246-247`) · `507ff38c` (§5 track_board 行改「间接经共享 dedupe 生效」) · `b550edff` (References 行 #182 改正或删除) · `7de08ae9` (SC-11 换成定位到具体字符串的断言) · `37de67cd` (SC-12 基线改同工作区跑两次, 不用活文件)。
