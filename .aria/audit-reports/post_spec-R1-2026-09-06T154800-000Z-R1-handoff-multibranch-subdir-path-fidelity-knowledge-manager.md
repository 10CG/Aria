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
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T16:58:03.071Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [knowledge-manager]
---

# post_spec 审计报告 — knowledge-manager (Round 1)

被审对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, Aria#195)

席位透镜: 知识与文档一致性 (头部机械判据 / Rule #3 同步面 / Rule #6 判据表选行 / Rule #10 / 术语与归档口径 / 引用真实性)。本轮只审不改, 未触碰任何仓库文件。

核验方式: proposal 自述一律不采信, 逐条对 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `origin/master` 301641b, 已用 `git rev-parse v1.71.1^{commit}` 与触点 `git diff` 双向确认) 实读; 数字类断言实跑复算; issue 引用走 Forgejo API 实查。

---

## 审计结论

### Decisions

- [minor] documentation/Rule #6 判据表选行: 选「第一行 描述性 ⇒ substitute」经核成立 —— SOT 已把同形状变更裁定过, 且 AB 套件对本 collector 结构上零覆盖, 不落第三行 (无需开套件缺口 issue) (证据: `standards/conventions/skill-benchmark-exemption.md:28,63-64,66` · `aria-plugin-benchmarks/ab-suite/state-scanner.json` 实测 handoff_multibranch/tracks_multibranch/legacy/basename 命中 0/0/0/0)
- [minor] documentation/Rule #10 闸门权限: 「审计计划」与「A.1.0 未跑头脑风暴」与 config 逐项一致, 全部落「config 显式 off」白名单第一类 (证据: `.aria/config.json` audit.checkpoints = post_brainstorm off · post_spec convergence · post_planning convergence · mid_implementation/post_implementation/pre_merge/post_closure off; teams.post_spec 5 席 · `proposal.md:12-13`)
- [minor] documentation/头部 Linked Issue 机械判据: 写法三条全过, 紧邻的 markdown 链接行未干扰抽取 (证据: `linked_issue_field_probe.py --emit-arg` 输出 `10CG/Aria#195`; check 模式 FAIL 6 项全是既有 M6/M7 proposal, 本文件不在内 · `proposal.md:6-7`)
- [minor] documentation/§7 向后兼容前提: 「本仓平铺 + 冻结语料无子目录」实测成立 (证据: `find docs/handoff -type d` 空、185 项零非 ASCII; 两份 `handoff-tracks-frozen-2026-09-05.json` 各 996 行、含 `/` 的 filename 为 0 · `proposal.md:128`)
- [minor] implementation/§5 消费方枚举主体正确: F1 与 track_board 判定属实 (证据: `scan.py:186` 第四硬编码点 + `:199-200` 静默 `continue`; `track_board.py:254,559` HANDOFF 列只吃 `updated_at`, 不读 `filename` 字面 —— 其 `:19` docstring 的「或 filename stem」是既有陈旧注释, 非本 spec 引入)

### Issues

- [major] architecture/§5 消费方枚举 (latest_md_writer) + 姊妹 collector handoff.py: §5 判 latest_md_writer「天然正确/无影响」只看了写侧。读侧 `handoff.py` 仍是扁平世界 —— `_parse_latest_pointer` 显式剥掉目录段 (注释「pointer targets are siblings in the same dir」), `_scan_md_files` 非递归。一旦 `filename` 变成相对路径, D.3 写出的 `**Latest**: [archive/x.md](./archive/x.md)` 会被读成 `x.md` → 扁平目录里找不到 → 新增 `handoff_pointer_target_missing` soft_error + 退回 mtime, scan 再次 exit 10, 正是本 spec 要消灭的症状换形复发。触发条件 = 单 active track 的交接文件位于子目录 (月份分目录布局即命中; #195 报告方的 `archive/` 只放旧件, 恰好躲过)。今天不可达 (basename 里没有 `/`), 属**本变更引入**的新失败面 (证据: `writers/latest_md_writer.py:110-124,143` · `collectors/handoff.py:286-288,301,318,387-404` · `references/layer-l-integration.md:107`「latest_md_writer 不在 scan.py 内自动触发, 它是 D.3 工具」· `proposal.md:116`)
- [major] documentation/Tasks 5.1/5.2 + §6 (发版同步面): 计划只覆盖 aria 侧「版本 SOT 5 文件 + CHANGELOG」与「主仓 spec/gitlink」, 主仓版本引用面一处未列 —— root README badge 与正文版本行、i18n README 的 `translated-from` marker、`system-architecture.md` §2.8 版本表行、`version-scheme.md` 版本表行。这四处由三条 **enabled** custom check 兜底 (判据都是「与 `aria/.claude-plugin/plugin.json` 比对」), 归档闸会红; 且本轨 v1.71.2 与同伴 v1.71.1 先后落地时这些行要连动两次, 不写进 tasks 极易停在 v1.70.0/v1.71.1 (证据: `proposal.md:10,124,157-158` · `README.md:8,242` · `docs/architecture/system-architecture.md:189` · `docs/architecture/version-scheme.md:23` · `.aria/state-checks.yaml:88 m6-version-badge-match / :141 i18n-readme-translation-currency / :372 plugin-version-arch-docs-match` · CLAUDE.md 版本管理段「发布同步面」)
- [major] documentation/§6 文档同步 · Task 4.1 · Impact.Risk (Rule #3 清单漏三处):
  1. **collector 自身的机读契约文档未列**: 模块 docstring `:42` 写 `"filename": str,  # basename of the handoff file`, `:20` 写 `"legacy_count": int,  # Tracks that fell back to legacy (no frontmatter)` —— 前者本 spec 直接推翻, 后者是 code/doc 早已不一致的那半 (代码在 git-show 失败分支同样 `legacy_count += 1`)。§6 只点 `references/state-snapshot-schema.md`, 这两行会留成新的漂移源。
  2. **`unreadable_count`「恒存在」缺落点**: schema `:1136` 逐字列了 fail-soft 返回形状 `{exists, tracks, branches_scanned, legacy_count, collision, errors}`, 对应代码早退在 `:592`; 新键要「恒存在」必须同时改这两处, tasks 与 SC 都没有 (SC-12 只覆盖正常路径)。
  3. **Risk 承诺的 schema 说明无对应任务/SC**: `proposal.md:140` 写「缓解: SC-7 用定向用例钉住**并在 schema 文档写明**」, 但 §6/Task 4.1/SC-11 四项清单里没有它; 更关键的是 schema `:1125` 现存论据「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one」在相对路径下直接变假 (`archive/` 的 `a`=0x61 > 数字), 不改就是把一条错误不变量留给下一个动排序的人 (证据: `collectors/handoff_multibranch.py:20,42,592` · `references/state-snapshot-schema.md:1110,1114,1125,1136` · `proposal.md:124,140,155`)
- [major] documentation/头部「基线冻结」行: 「两 SHA 间只新增了 7 个 a1-entry 相关测试文件, 均不触碰本触点」与实读不符 —— `git diff --name-status 0545f86 301641b` = **5 added + 24 modified** (共 29 文件), modified 含 `skills/state-scanner/lib/collision.py`、`lib/identity.py`、`lib/claim_lifecycle.py`、`scripts/phase1_gate.py`、`state-scanner/SKILL.md` 与 2 个既有测试文件。`lib/collision.py` 正是 SC-7 所测 dedupe 分组键 (`identity_key` / `split_owner_container`) 的实现所在, 说「只新增测试文件」会让复审者误判基线增量对本触点完全惰性。**结论侧无损**: 触点 5 文件 `git diff --stat` 确为空, 「行号在两 SHA 一致」独立成立 (证据: `proposal.md:9`; `git -C aria diff --name-status 0545f86 301641b` 实跑)
- [minor] testing/SC-10 基线数字: 「改前基线已实测: 73 tests OK」不复现 —— 在 1.71.1 副本实跑 `python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories` = **Ran 78 tests, OK**; 两 SHA 上这 4 个文件未被修改, 静态 `def test_` 计数同为 78。基线数写错会让「5 个测试静默消失」也满足该 SC。同段「1571 tests / 2 项已知非本 spec 失败」实跑核验一致 (Ran 1571, failures=1 errors=1, 恰为 `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` 与 `Test1210ChannelStabilityUnderOffline`) (证据: `proposal.md:176`; 两次实跑)
- [minor] documentation/References 现场行: `aria-plugin#182 (handoff status 不收口, 相邻但不同根因)` 属误标 —— API 实查 #182 = 「[缺陷][state-scanner] issue_scan 无分页且 limit=20 硬顶 —— open_count 静默截断 40%」(open), 与 handoff 无关。同行 `#155 (dedupe 由来)` 正确 (closed,「tracks_multibranch collision 把已终结线的历史 handoff 当活跃 track」)。误标使「邻近 issue 已排查」这条信号不可信 (证据: `proposal.md:206`; `forgejo GET /repos/10CG/aria-plugin/issues/182`, `/155`)

### Risks

- [minor] testing/SC-11 文档机检: `grep -c 'basename' collectors/handoff_multibranch.py` 相对基线「减少」是不定位的代理判据 (当前 7 处: 模块 docstring `:42`、函数 docstring `:246`、循环体 `:277,278,280,284,288`)。新实现仍需 basename 做 `.md` 过滤与 pointer 排除, 只改 `:246` 一句即可让计数下降 ⇒ 结构上钉不住 `:42` 的漏改。建议换成两条具体断言:「`callers compose the full git-object path` 消失」+「模块 docstring `filename` 行含『相对』」(证据: `proposal.md:177` · `collectors/handoff_multibranch.py:42,246,277-288`)

---

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 2 (另 5 条 Decision + 1 条 Risk 均 minor, 不参与判定)。

rationale: 方案主体 (A 案 + D 附加) 与根因诊断经实读复核成立 —— 症状表、四处硬编码前缀、F1 跨文件消费方、`-z` 转义、dedupe tie-break 风险、平铺仓零行为变化前提均逐条属实; Rule #5/#6/#10 与头部机械判据全部合规; 引用的 memory (5/5)、归档先例 (2/2)、规范文件 (3/3)、issue #195/#155 均真实存在。故**无 Critical, 方案不需推翻**。

但四条 Major 都落在「知识资产一致性」这条主轴上, 且都会在 Phase B/C/D 变成返工或闸门红: 一条是新引入的跨 collector 断链 (子目录指针写得出、读不回), 两条是同步面清单不全 (发版版本引用面 / 代码内契约与 schema fail-soft 形状), 一条是被标为「已核验」却不复现的基线陈述。post_spec 非阻塞, 建议在进入 post_planning 前补齐 §5 读侧评估、§6/Task 4.1 三处目标、Task 5.1/5.2 主仓版本面, 并订正 `proposal.md:9` / `:176` / `:206` 三处数字与引用。

补充给 owner 复议 (不构成 finding): proposal「待 owner 复议 1」把「pointer 任意深度排除」当成新口径, 但现行代码 `:277,280` 取 basename 后比对, `archive/latest.md` 今天**已经**被排除 —— 推荐默认「是」= 保持现状, 采纳反对意见才是行为变更, 复议描述宜按此改写。

---

## 轮次记录

### Round 1

- Agents: knowledge-manager (post_spec 5 席之一, 本报告仅本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
  - 扫描面: `openspec/changes/` 9 个在制 spec (a1-entry-claim-duplicate-work-guard / pre-merge-completeness-gate-change-scope / M6 四件 / M7 两件 / 本 spec) 无第二份指向 Aria#195; 主仓 open PR = `[]`; aria remote 仅同伴 `feature/a1-entry-claim-duplicate-work-guard` 分支 —— 与头部「同伴 PR 尚未开」「gitlink 仍指 0545f86」一致 (`git ls-tree HEAD -- aria` = 0545f86; `git ls-remote` 确认 v1.71.1 → 301641b)
- Conclusions: 12 条 (Decisions 5 / Issues 6 / Risks 1)
- Vote: REVISE (存在 Major, 未达零 rework 干净轮)
