---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T18:13:41.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [knowledge-manager]
---

# post_spec 审计报告 (Round 3) — pre-merge-completeness-gate-change-scope · knowledge-manager 席

审计对象为 v3 (R2 rework 后)。本席不继承前两轮结论, 全部事实自行实读/实跑复核; 本轮只审不改, 未触碰仓库任何文件。

## 审计结论

### Decisions

- [minor] documentation/头部 Linked Issue 字段: `> **Linked Issue**: \`10CG/Aria#199, 10CG/aria-plugin#161\`` 过 spec-drafter 写法三条 (单 code span + `, ` 分隔 + 行首无空白 + 非 markdown 链接形); 紧邻的 `> **Issue**:` 行字段名不在 E0 谓词 1 的两拼写集合内, 不遮蔽第一条命中 (证据: proposal.md:6-7 · spec-drafter/SKILL.md:414-426 · openspec/archive/2026-09-02-linked-issue-field-availability/proposal.md:164-201)
- [minor] documentation/冻结快照语料数字: 对 `3f4b379` 独立复算, 全部逐字命中 —— changes 9 + archive 144 条目、`|C|`=152、前缀碰撞 1 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`) 后缀 0 中缀 0、audit-reports 780 条目 (778 `.md` + 子目录 `pr19-submodule-scan` / `wf-r1fix`)、`*-audit-trail.md` 族恰 5 份且成员名逐字同集、末段族 62、真 legacy 6、unattributed 170 (全 8 checkpoint 口径) (证据: proposal.md:38,51-53,115,133-134 对 `git ls-tree 3f4b379` 复算)
- [minor] documentation/R2 缺陷落地: C2 与 M9 全部落进正文而非批注 —— 空集三格 (:190-196) + SC-15、枚举优先级链 (:143-156) + SC-20 + `results.enabled_by`、stdout 15 键 (:197) 与 SC-10 逐字一致 (原 13 键与 SC-19 的结构性互斥已消)、config 直读 + SC-21、照跑面收敛 + 复议 #9、`--base` 绑定 + §3 接线 + SC-22、(b) 通道两处收窄 + SC-5(6)(7)、SC-19 反事实换新并补 (c)、S1 继承 `allow_dangling_change_ids`、report-storage 落点 + SC-13 两条逐字 grep (证据: proposal.md:92,143-156,190-197,285,295,300-303 对 rework-R2 清单逐条比对)
- [minor] documentation/SOT 行号与基线有效性: 抽查的引用全部实读命中 (execution-modes `:15/:32/:37-38/:44/:46-52/:54-61/:63-65/:82/:185`; audit-engine SKILL `:49-54/:60/:63/:123-125/:381-388/:391/:398-400/:404-406/:410-411`; phase-c-integrator `:131/:132/:133-137/:157/:252/:265/:299`; config-loader `:8-10/:37/:305-331` 与 config-example `:280/:381-400/:402-417/:419-440`; project.md `:117/:118`; skill-benchmark-exemption `:26-31/:33/:35`; configured-gate-authority `:35/:38-40`)。`301641b..f314785` 21 文件变更中触点与被引文件 diff 全空, 故 :16 的基线断言成立; 主仓 16 个版本字符串点的位置逐条仍命中 (证据: proposal.md:9,16,229 对插件缓存 v1.71.1 副本与 `git diff --stat 301641b f314785`)
- [minor] architecture/Rule #6 与 Rule #10 处置: 判据表附加约束 (`skill-benchmark-exemption.md:33`「指令流程变动一律第二行」) 下, 本 spec 取两读法并集 (照跑 `audit-engine.json` 2 evals + `phase-c-integrator.json` 3 evals + 定向 fixture + 缺口 issue), 严于任一单读法; `phase-c-integrator-pre-merge-gate.json` 实读确无 `evals` 键 (`type=workflow_skill_subextension`, 8 `fixtures[]`, `issue=10CG/Aria#60`), 认定权挂复议 #9 未自行删闸 (证据: proposal.md:12,270,304-308,326 对 ab-suite 三文件 `json.load` 实读)
- [minor] documentation/Level 2 定级口径: 同类 audit-engine 脚本型 spec 归档实测均为 Level 2 (`2026-09-04-sibling-spec-probe` / `2026-08-23-pre-merge-gate-no-run-for-branch` / `2026-07-31-phase-c-gate-path-coverage-not-applicable`), 内联 `## Tasks` 无 `tasks.md` 的形态亦有先例 ⇒ 本 spec 的 Level 2 与内联 Tasks 形态与归档口径一致, 不构成缺陷 (证据: proposal.md:3 对三份归档 proposal 头部 Level 行与目录清单实读)

### Issues

- [major] documentation/头部基线复核 vs §4 · Tasks · 复议 #4 的版本目标: :16 已宣告「PATCH 候选改为 v1.73.1」, 但三处可执行位置 (:229 §4 同步表、:274 Tasks 版本项、:317 复议 #4) 仍写 v1.71.2, 且失效断言处无 inline 标记。实读 `aria/.claude-plugin/plugin.json` = `1.73.0` 且 tag `v1.73.0` 实存 ⇒ 照 Tasks:274 执行会 bump 到被越过的号; 复议 #4 交给 owner 的「v1.71.2 vs #195 的 v1.72.0」两号皆已作废, owner 拿到的是失效决策项 (证据: proposal.md:16 vs :229/:274/:317 · aria/.claude-plugin/plugin.json:4 · `git -C aria tag --list 'v1.7*'`)
- [major] implementation/§1.3 Level N 取法与 SC-20(3): :156 只给正则 `Level\s*\**\s*[:：].*?([123])`, 未定扫描窗口、未定「取文档序第一条」、未定字段形态集。对本仓 153 份 proposal 实测: Level 行位置 L3–L58, 其中 2 份在 L40 之后 (`2026-08-16-premerge-gate-mainbranch-failclosed` L44 / `2026-09-06-a1-entry-claim-duplicate-work-guard` L58), 9 份全文无该行, 字段形态 3 种 (`> **Level**:` / `- **Level**:` / `## Level:`), 另有 6 份的首个正则命中落在非字段行。取 head-window 的实现会把那 2 份真实 change 判 `spec_level_undetermined` exit 2 硬阻, 而 SC-20(3) 只测「无 Level 行」⇒ 该错法在测试下全绿。同仓同类字段 (Linked Issue) 已有反向裁定: 「位置不影响机械判定, 不限行号; 只扫头部 N 行的加固已被真实语料实测否决」(证据: proposal.md:156,300 · spec-drafter/SKILL.md:426 · 153 份 proposal 全枚举实测)
- [major] testing/§1.4 空纳入集三格与 §1.1 S1-S4 的求值顺序 (SC-15): 两节均未声明先后, Tasks:264 的实现清单把「作用域 S1-S4」列在「空纳入集三格」之前。SC-15 的格 A / 格 C / 格 B 三条 fixture 都不给 `--change-id`、不建锚点、不给 diff ⇒ 在「作用域先」这一合法实现下会先落 S4 `change_scope_unresolved` exit 2, 与断言的 `error_kind=audit_not_enabled` / `verdict=pass` exit 0 直接冲突, 尤其把 R2 Critical 专门保护的官方场景 A/B 采用方那一格 (格 B) 变成不可满足。R2 已对 SC-16 与 SC-5(4)(5) 修过同类缺陷 (minor `5f8e4dfb`), 新写的 SC-15 复发 (证据: proposal.md:92-97,190-196,264,295)
- [minor] documentation/§4 version.yaml 行与复议 #4 对并发轨 #195 的行号锚: 两处引 `#195 proposal.md:352` 佐证「现推荐改走 MINOR v1.72.0 但仍待 owner 拍板」。实读该文件 :352 是「(f) 的处置 (R2 `88a49037` 改写)」, 与版本无关; 版本级别项已随 #195 的 R4 rework (`cf6f56a`) 移到 :382。结论仍真, 锚点已漂 (证据: proposal.md:231,317 · openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md:352,382)
- [minor] documentation/SC-13 的「SC-17 计数恰 2」先例锚: SC-13 把该先例锚到 `execution-modes.md:152`, 而该行是竞品探针节的 blockquote (「本节是探针 stdout 契约 + exit code + 消费措辞的权威可执行版」), 不含计数断言。真实出处是 `openspec/archive/2026-09-04-sibling-spec-probe/proposal.md:513` (另 :387 / :397 写明「恰 2 次是有意的保守」) (证据: proposal.md:293 · execution-modes.md:150-152 · 该归档 proposal:387,397,513)

### Risks

- [minor] documentation/裸 issue 引用纪律 (v1.73.0 随插件 ship 的新 check): `aria/skills/state-scanner/scripts/check_bare_issue_refs.py` 对本 proposal 实跑报 **55** 条裸 `#N` (同伴 #195 的 proposal 报 18 条)。该 check 目前**未被**任何 `SKILL.md` / `.aria/state-checks.yaml` / `standards/` 引用 ⇒ 不是已启用闸门, 本席**不判违规**; 但同伴轨已把「对 proposal.md 与 tasks.md 跑该脚本 rc==0」当成自检并写进 tasks (证据: `python3 check_bare_issue_refs.py --repo-root=/home/dev/Aria <proposal>` 实跑 · openspec/archive/2026-09-08-archive-gate-registration-class-and-skill-drift/tasks.md:145 · 全仓 grep 零 SOT 引用)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 3 / Minor 3 (另 6 条 decision 不计入缺陷计数)。

理由: 本轮无方案级错误。R2 的两条 Critical 与九条 Major 已逐条落进正文并经复算成立, 语料数字、SOT 行号、Rule #6 与 Rule #10 处置、Level 定级口径均实读通过, 关键的「15 键 vs SC-19 结构性互斥」「空集硬阻」两条已消解。三条 Major 均属知识一致性与可证伪性缺口, 不改变方案形态: (1) 版本目标在头部已顺延而三处可执行位置未同步, Phase C/D 与 owner 复议会读到作废的号; (2) Level 取法的判据未钉到可实现程度, 与同仓同类字段的既有裁定冲突, 且现有 SC 覆盖不到那条错法; (3) 两节求值顺序未定义, 使 R2 新写的 SC-15 在一种合法实现下不可满足。三条各自的修法都限于本文改写与 SC 补断言, 不触及 §1 契约与三态设计。

## 轮次记录

### Round 3

- Agents: knowledge-manager (五席之一; 本文件为单席报告)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 条 (Decisions 6 / Issues 5 / Risks 1); 其中计入缺陷计数的 8 条 = Major 3 + Minor 3, 另 6 条为正面核验记录 (与 Round 1/2 同一记法, decision 不计入 severity 计数)
- Vote: REVISE
