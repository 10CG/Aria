---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T01:38:44.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [knowledge-manager]
---

# post_spec R2 单席审计报告 — knowledge-manager (handoff-multibranch-subdir-path-fidelity, Aria #195)

本席为 Round 2 新席位, 不继承 R1 结论。全部事实断言均在本轮实读 / 实跑核验; 行号以 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria 子模块 `origin/master` `301641b`) 为准, 主仓行号以工作树当前内容为准。本轮**只审不改**, 未编辑任何仓库文件。

---

## 审计结论

### Decisions

- [minor] documentation/Rule #6 判据表选行: 核实通过 — 变更为纯代码 + schema 描述性文档, 无 `description` 与 SKILL.md 指令面变动 (SKILL.md 三处 `tracks_multibranch` 均不改), 与 SOT 已裁样例「纯代码 collector 层 ⇒ substitute」同形 (证据: standards/conventions/skill-benchmark-exemption.md:28,63-64; skills/state-scanner/SKILL.md:117,149,153)
- [minor] documentation/Rule #10 闸门权限: 合规 — `.aria/config.json` 实读 `audit.checkpoints` = post_brainstorm off / post_spec convergence / post_planning convergence / mid_implementation · post_implementation · pre_merge · post_closure off, `teams.post_spec` 5 席, 与头部「审计计划」「A.1.0 未跑」逐项一致, 全部落白名单第一类 (证据: /home/dev/Aria/.aria/config.json)
- [minor] documentation/头部 Linked Issue 机械判据: 三条全过 — 值为 inline code span `` `10CG/Aria#195` ``, 行首无空白、`>` 后恰一空格、字段名两侧各两星号、ASCII 冒号, 字段序与 SOT 模板一致; 紧邻的 `> **Issue**: [Aria#195](url)` 链接行字段名不在 E0 封闭集合内, 不干扰抽取 (证据: proposal.md:6-7; skills/spec-drafter/SKILL.md:414-421; standards/openspec/templates/proposal-minimal.md:6,55-58)
- [minor] documentation/R1 rework 落地复核: 2 critical + 15 major + 10 minor 全部落进**正文**而非批注 (逐条对位见下节), 未见新矛盾。本席独立实跑复现四项载重数据: `Ran 78 tests … OK` (真仓 checkout)、`0545f86..301641b` = 29 文件 (5 added + 24 modified)、5 个触点文件 `diff --stat` 为空、`git ls-tree origin/master aria` = `301641b`。头部「主仓实况」记 `ecb6296` 今已前进到 `8da3518` (本 spec 自己的两次 commit 所致), 该行已自标日期为观测快照, 载重结论 (gitlink 起点 `301641b`, 严禁回退 `0545f86`) 仍成立, 不构成 finding (证据: 本席实跑; scratchpad/handoff-multibranch-subdir-path-fidelity-rework-R1.md)

### Issues

- [major] documentation/rule6_note 套件覆盖实测 · 头部 Rule #6 判定行: 两处均称 AB 套件对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词「零命中」。实测 `tracks_multibranch` **命中 1 次** —— `evals[12].prompt` 的协调闸门用例问「本次扫描的 `tracks_multibranch.collision.kind` 是空的, 这会改变 (A) 的答案吗」; 该用例由 2026-09-05 的 commit `5697477` 引入, 在 `813e82c` (R1 审计所见树) 上同样为 1, 且全机只此一份副本 (17551 B)。**结论不倒** (判据表第一行 substitute 不依赖套件覆盖度), 但支撑证据须改写为「唯一命中落在闸门面 `SKILL.md:149/153`, 而本 spec 三处均不改, 且假 legacy 行的 `owner_container` 恒 `unknown` 已被 `classify()` 排除」——现在这条恰是 rule6_note 第一条自己的论据, 两条应合并陈述, 不能继续写「零命中」(证据: aria-plugin-benchmarks/ab-suite/state-scanner.json:214; proposal.md:12,244)
- [major] documentation/§6 文档同步 (Rule #3) 漏 standards SOT: Rule #9 的 SOT 把 latest.md 派生行为写成**穷尽两态** —— 「单 track 场景 (1 active track): `latest.md` 写当前 track 指针」/「多 track 场景 (≥2 active): 仅 deprecation banner」。§2.5 的写侧守卫引入**第三态**: 单 active track 但其文件在子目录 ⇒ 不写真指针, 走 `_render_pointer_unavailable` 并写明原因。落地后 SOT 那句无条件表述对子目录采用方即为假, 而 §6 的五条同步清单与 Tasks 4.1/4.2 全部只覆盖 aria 插件内文档, 无一条指向 `standards/`。该文件在共享子模块内, 影响所有采用方; 若判定本轮不改 standards, 也须在 spec 内显式写成 deferred 并说明理由 (Rule #5 允许规范自身变更落 standards 仓, 但会带出 standards 版本与 gitlink 同步面, 属实施面成本, 应在 Tasks 里可见) (证据: standards/conventions/session-handoff.md:171-173; proposal.md:123-133,157-169,201)
- [major] documentation/Task 5.1 发布同步面清单与「三条 check 兜底」断言: 本仓 aria-plugin 版本引用点实测共 **16 处** (CLAUDE.md:139,141 · README.md:8,242 · README.zh/ja/ko.md:3,10,244 各 3 处 · VERSION:24 · system-architecture.md:189 · version-scheme.md:23), 与上一次发版 commit `4c3c826` 自述的「16 处版本点」逐一对上。Task 5.1 只列其中 **7 处**, 漏掉: (1) 主仓 `VERSION:24` 子模块版本表行 —— CLAUDE.md 的「发布同步面」逐字列出「主仓 VERSION」; (2) CLAUDE.md:139 与 :141; (3) 三份 i18n README 的 badge (`:10`) 与正文版本行 (`:244`) 共 6 处 —— Task 5.1 对 i18n 只提 `translated-from` marker。更要紧的是兜底断言不成立: `m6-version-badge-match` 的命令是 `grep -m1 … README.md`, 只看首个 badge; `i18n-readme-translation-currency` 只正则 `translated-from`, 不读 i18n 正文 (与 memory `feedback_version_checks_blind_to_i18n_readme_body` 完全同型); `plugin-version-arch-docs-match` 只比两处架构行; 另一条 `main-project-version-consistency` 的 POINTS 清单全是**主项目 1.7.5** 那条线, 不含插件版本行。⇒ 含 `README.md:242` 在内的 **10 处**零机械兜底, 「漏改必在归档闸转红」这句会给实施者假安全感 (证据: .aria/state-checks.yaml:88-102,141-182,289-316,372-399; .aria/probes/main-project-version-consistency.py:39-49; CLAUDE.md:81)
- [minor] documentation/§6 第 1 条与 Task 4.1 的 schema 文档面两处遗漏: (a) `state-snapshot-schema.md` 有 `## Change history` 表, 既有口径是**每次 schema 变更加一行** (H5 pointer / #134 / #141 / Task 10.1 逐条在列), 本 spec 新增 `unreadable_count` 与 `relpath` 却未把该行列入同步项; (b) 本 spec 要改的 `:1136` fail-soft 形状本身已与代码漂移 —— 代码早退 dict 的 `collision` 是 `{"kind","groups","identity_advisories"}`, 文档只写 `{"kind","groups"}`; 既然要动这一行, 顺带勘正比留一条半真的形状说明便宜 (证据: state-snapshot-schema.md:1136,1156-1168; collectors/handoff_multibranch.py:588-595)
- [minor] testing/SC-9 与新 soft_error kind 的命名: 本 collector 现有四个 kind 全为 `handoff_multibranch_*` (`branch_list_failed` / `branch_cap` / `ls_tree_failed` / `git_show_failed`), 是机读契约的一部分 (schema `:1136` 与 `errors[]` 段按 kind 记述)。§What.1 的前缀守卫要新增一条 per-item 错误, 但全文未给它命名, SC-9 也只断言「计一条 soft_error」—— 实现若直接复用 `handoff_multibranch_ls_tree_failed`, SC-9 仍绿而消费方无法区分「整支分支 ls-tree 失败」与「单行前缀异常」。建议在 §What.1 定名 (例 `handoff_multibranch_unexpected_path_prefix`), SC-9 断言 kind 字面, 并把它加进 §6 的 schema 同步项 (证据: collectors/handoff_multibranch.py:587,607,623,643; proposal.md:103,231)
- [minor] documentation/新机读字段 `relpath` 的命名与既有口径: 本 schema 的多词键一律下划线分词 —— `legacy_count` / `owner_container` / `branches_scanned` / `updated_at` / `identity_advisories` / `latest_filename`, 连本 spec 自己新增的 `unreadable_count` 也是。`relpath` 是唯一的连写例外, 且 `grep -rn '\brelpath\b'` 在插件 1.71.1 全树零命中 (无先例可援)。字段一旦 ship 即为永久机读契约名 (schema 文档 + collector docstring + `scan.py` + writer 四处消费), 现在改成 `rel_path` 成本为零 (证据: state-snapshot-schema.md:1080-1111; proposal.md:82,106)
- [minor] documentation/SC 表内 A 分支未就地 neutralize: 前置门已裁定 A′ (Task 2.0 勾选, 决策单在案), 但 SC-1 / SC-8 仍并列「A: `filename == "archive/…"` / A′: `filename == basename` 且 `relpath == …`」两套断言, 唯一的消歧句在候选表下方的裁定注里 (「实施以 A′ 为准」)。审计要点里 amendment 的 neutralize 要求正是针对这一失效模式 —— 读者停在原文断言处不会回头看上游说明。建议对 SC 表内 A 分支就地划除或加「见裁定注」标记 (证据: proposal.md:91,200,223,230)

### Risks

- [major] architecture/§2.5 与 SC-15 的守卫判据在 `relpath` 缺失时未定义: §2.5 与 Task 2.5 把判据钉死为 `relpath != filename` 并禁止字符串嗅探, SC-15 的第二条反事实还专门锁住这个形式 —— 但没有一处定义 `relpath` **不存在**时怎么办。这不是理论边界: `session-closer/SKILL.md:90` 明确允许「跑 scan.py 取 snapshot **或读既有 `.aria/state-snapshot.json`**」, 而升级前写下的快照里每一行 track 都没有 `relpath`。按字面实现 (`track.get("relpath") != track.get("filename")`) 会对**平铺仓 (含 Aria 自身)** 的每一条 active track 判定为「在子目录」, 于是真指针被吞掉、写出一条理由为假的降级横幅, `handoff.py` 随即由 pointer 退回 mtime —— 正好重开 H5「pointer 是语义权威」那条既有修复, 与 R1 critical `63d1ce08` 同族, 只是触发条件从「子目录布局」换成「快照跨版本」。SC-15 的两个布局都在同一次运行里现造 `relpath` 与 `filename`, 结构上覆盖不到缺失分支。建议: §2.5 明写「`relpath` 缺失时按 `relpath = filename` 处理 (老快照即平铺世界)」, 并给 SC-15 补第三条断言 (无 `relpath` 键的 track ⇒ 仍写真指针) (证据: skills/session-closer/SKILL.md:90; writers/latest_md_writer.py:110-124,151-169; proposal.md:123-133,237)

---

## R1 落地复核 (逐条对位, 只记结论)

- Critical 2/2 落地: `63d1ce08` → §2.5 守卫 + SC-15 + Impact 新 Risk 行 + 决策单 `.aria/decisions/2026-09-07-…-pointer-guard.md` (文件存在, 内容与 proposal 自洽); `24165c1c` → SC-10 删除两条豁免并改记「真仓 checkout 零失败」。本席在 `/home/dev/Aria/aria/skills/state-scanner/tests` (HEAD = `301641b`) 实跑该命令得 `Ran 78 tests … OK`, 与 SC-10 记载一致。
- Major 15/15 落地, 抽验四条: `352d744d` 符号更正 (`_same_branch_head_unreachable_tracks` 在 `scan.py:126` 定义 / `:186` 拼串 / `:255` 调用, 与文一致); `07dc73c8` 四道前置 (`scan.py:166-173` 三道 + `:178` 分支相等) 与文一致; `74829542` fail-soft 早退 dict 六键 (`:588-595`) 与文一致; `50bb5886` 头部 29 文件与 5 触点零 diff 本席复算一致。
- Minor 10/10 落地, 抽验三条: `:277` / `:246-247` 行号更正属实; References 已删 `#182`; SC-11 已换成定位断言 (旧 `grep -c basename` 基线 7 处分布 `:42,246,277,278,280,284,288` 本席复算一致)。
- 唯一 partial (`109b412c` 的 `snapshot_schema_version` 处置) 在 A′ 裁定后事实上已收敛 (A′ 为纯 additive ⇒ 保持 `"1.0"`), 但 §7 与待复议 2 仍保留条件式行文, 属上面 minor「A 分支未 neutralize」的同一处。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 4 (另有 4 条 decision, 不计入缺陷计数)。

rationale: 方案骨架、事实底座与 R1 rework 的落地质量本席复核成立 —— 四项载重数据 (78 tests / 29 文件 / 5 触点零 diff / gitlink `301641b`) 全部实跑复现, Rule #6 选行、Rule #10 闸门、头部机械判据三项合规。**无 Critical**: 未发现方案错误、消费方破坏或恒绿 SC。四条 Major 分两类: 一类是**外沿知识面不全** —— Rule #3 清单漏了 Rule #9 的 standards SOT (M2)、发版同步面漏了 16 点里的 9 点且兜底断言被高估 (M3); 另一类是**证据与契约的精度** —— AB 套件「零命中」按横切「数据可用性」条款实测规模不符 (M1, 结论不倒但证据须重写)、pointer 守卫判据对 `relpath` 缺失态未定义 (M4, 有具体触发路径且现有 SC 测不到)。四条都可在 Phase A 内改 spec 消解, 不触及方案骨架, 故投 REVISE 而非 FAIL。

计算依据:
- Critical: 0
- Major: 4 (3 issue + 1 risk)
- Minor: 4 (4 issue + 0 risk)
- Decisions (不计入): 4

---

## 轮次记录

### Round 1 (承前, 非本席产出)

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager)
- Conclusions: 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6)
- Vote 票型: REVISE 5 / PASS 0 ⇒ verdict FAIL
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 2 (本席)

- Agents: knowledge-manager (本报告只记本席结论; 其余席位不在本文件口径内)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
  - 扫描面: `openspec/changes/` 8 个在制 spec 中, 引用 `Aria#195` 的仅本 spec; 触及 `handoff_multibranch` / `latest_md_writer` 的 proposal 亦仅本 spec
- Conclusions: 12 (Critical 0 / Major 4 / Minor 4 / Decisions 4)
- Vote: REVISE (Major 4 > 0)
