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
timestamp: 2026-09-07T05:31:58.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead]
---

# post_spec R4 单席报告 — tech-lead — handoff-multibranch-subdir-path-fidelity

本席为 R4 新席位, **不继承** R1/R2/R3 结论。全部事实经实读 / 实跑核验; 行号一律对 aria `origin/master` `301641b` (= v1.71.1, 实读副本 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`)。本轮**只审不改**, 未触碰仓库任何文件。

透镜: 架构与范围 / 根因 vs 症状 / 候选方案取舍 / 与其它 collector 及消费方的接缝 / 越界面 / ship 顺序与 gitlink 归属。

## 审计结论

### Decisions

- [minor] documentation/R3 19 条 major 的正文落地复核: 19 条逐条命中正文而非批注 —— `a7536535`→§What.1 契约行 + Task 2.1 二选一实现路径; `92565b30`→§2.5 新增「返回契约 action」行 + 裁定块 + Task 2.5(e) + SC-15(h); `b5a94a9c`→§6.2 两块各归其位 (**实读复核块边界正确**: 顶层返回键表确为 `:16-31`, TrackEntry 块确为 `:35-44`); `4608f5b2`→§6.1 新 bullet + Task 4.1/4.2 + SC-11(j); `db126eff`→§6.3 撤回 + SC-11(d) 改判为 deferred 记录断言; `334e62dc`→头部第 3 段三条勘正。未见「改一处引入另一处矛盾」的系统性回填 —— **唯一例外是 `ebaad4a5` 的行号勘正自身出错**, 已单列 (证据: `handoff_multibranch.py:16-31,35-44`, proposal.md:19,107,206)
- [minor] documentation/SC-11 机检判据的基线可证伪性: 逐条实跑复核, R3 换的新判据成立 —— `grep -c 'callers compose the full git-object path'` = **0** (旧判据确为恒绿), `'Returns only the basename'` = **1** (有鉴别力), `'path relative to'` = **0** (正向断言亦 baseline-failing), `'legacy:<branch>:<filename>'` 合计 **4** (collector 3 + schema 1), `'unreadable_count'` 在 schema = **0** (证据: handoff_multibranch.py:246, references/state-snapshot-schema.md:1104)
- [minor] architecture/ship 顺序与 gitlink 归属: 主仓 `HEAD` = `origin/master` = `e58ac22`; `git ls-tree HEAD aria` = `301641b` = `git -C aria rev-parse origin/master`; `standards` gitlink = `21748d4` = 其 `origin/master`; `git -C aria tag --list 'v1.7*'` 最高 `v1.71.1`。⇒ Task 5.2 的「从 `301641b` 前进, 严禁回退 `0545f86`」与 Task 4.4 的「standards 只许从 `21748d4` 前进」两条写死起点均正确, 两个候选号未被占用 (证据: proposal.md:10,268,266)
- [minor] architecture/越界面与同伴在飞轨: 触点集合不含 `phase1_gate.py` / `claim_lifecycle` / `spec-drafter` / `phase-a-planner` / AB 套件本体 —— `phase1_gate` 全文仅作认领命令出现一次 (proposal.md:8), `ab-suite/state-scanner.json` 四处出现全为证据引用或 Task 5.5(b) 的缺口 issue, 无编辑动作。同仓另一在制 spec `pre-merge-completeness-gate-change-scope` (#199) 的触点为 audit-engine + `ab-suite/audit-engine.json` + `version.yaml`, 与本 spec 五触点**零文件交集**; 两者只在 aria 版本号面串行, 已由待复议 6 的 `ls-remote --tags` 前置覆盖。`docs/handoff/latest.md` track 表在飞仅本容器 M6 轨 (aria-orchestrator, 零交集)。**无越界**
- [minor] architecture/A′ 骨架与代码结构对得上: 四个 git 路径消费方确为全部 (`handoff_multibranch.py:301` `_read_file_content` / `:321` `_get_file_commit_date` / `:329-336` `_make_legacy_track_id` / `scan.py:186`), 无第五处。`"rel_path"` 作为字典键在插件 1.71.1 全树 **0 命中** (56 处 `rel_path` 全是局部变量名, 如 `remote_refresh.py:288`) ⇒ 新键不与既有语义撞名。Task 2.1 推荐默认 (保持 2-tuple + 注入带默认值的 reporter) 与 `test_max_branches_resolver.py:286,300,316,332` 的 `mock.patch.object(..., return_value=([], None))` 形态兼容 (mock 接受任意入参), 该默认支成立
- [minor] architecture/根因判断成立: 契约错配的定性 (枚举层承诺「调用方自行拼路径」却交出信息量不足的 basename) 与实读一致 —— `handoff_multibranch.py:246-247` docstring 自述 + `:277` `Path(path).name` + 三处 `_HANDOFF_TREE_PATH` 拼串 + `scan.py:186` 的第四处**独立字面量** `f"docs/handoff/{filename}"`。B/C 两案 (去 `-r` / 显式 skip) 的否决理由 (以「看不见」换「不报错」) 成立; D (git show 失败不再伪造 legacy) 与 A/A′ 正交亦成立

### Issues

- [major] architecture/§2.5 返回契约行 / Task 2.5(e) / SC-15(h): **`degraded_reason` 的产生路径全文未定义**。`_render_pointer` (`latest_md_writer.py:110-148`) 只返回字符串, `write_latest_md` (`:298-320`) 结构上拿不到「内部是否回退」这个事实; 全文 10 处提 `degraded_reason` 无一处说明如何回传。最省事实现 = 在 `write_latest_md` 内**重算同一守卫谓词**, 于是 `rel == filename` 这条判据在两个函数里各写一遍、靠巧合一致 —— 正是本 spec §3 对 `scan.py:186` 与 `_HANDOFF_TREE_PATH` 明写过的根因族 (「两处独立字面量, 今天靠巧合一致」)。两处一旦漂移, `degraded_reason` 就会与正文互相矛盾, 把 `92565b30` 要修的「人读面诚实、机读面说谎」原样复制一份。SC-15(h) 只断返回值, 对两种实现同样绿 (证据: latest_md_writer.py:110,116,124,143,298-320; proposal.md:126,259,320)
- [major] architecture/§3 / Task 2.2(a) / §5: **`scan.py` 两个上报字段的归属未定**。§3 用整段规定 `:186` 改读 `rel_path` 且「不做缺键兜底」, 却未说同一函数 `:193` (`inconclusive`) 与 `:209` (`offenders`) 上报的 `"filename"` 该装 basename 还是相对路径; 这两个 dict 经 `:269` / `:283` 进快照顶层 `errors[].tracks[]`, 是机读输出 (schema `:1141-1147` 的 `errors[]` 形状还只列三键, 根本没记 `tracks` 子键)。按 Task 2.2(a)「沿用 `:180-182` 既有早退形态、改成读 `rel_path` 后同形早退」的字面写法, 最自然的实现是重指那个局部变量 ⇒ 一个机读字段的取值语义静默改变, 而 A′ 的立意恰是**不动既有 `filename` 语义**。§5 消费方表、§6 同步清单、SC 集三处零登记 (证据: scan.py:180-186,193,209,269,283; references/state-snapshot-schema.md:1141-1147; proposal.md:121,257)
- [major] architecture/Task 2.0 前置门 / §待 owner 复议 7: **Level 裁定无任务承接**。Task 2.0 写「前置门 — 已解除」并逐一枚举「待复议 1 / 3 / 4 / 5 / 6 均取推荐默认推进」, 但 R3 新增的**待复议 7 (Level 2 vs Level 3) 不在枚举内**, 而它恰是全文唯一自述「无推荐默认, 执笔者不自裁」的一条。它的裁定结果决定 Phase B **之前**是否必须先补 A.2 `tasks.md` + A.3 `detailed-tasks.yaml` + post_planning 收敛审计 (目录内现仅 `proposal.md` 一个文件, 实测 `ls`)。Task 5.1 为待复议 6 (版本级别) 明装了「裁定后才动手」的前置门, 同等级的待复议 7 却无任何任务挂钩 ⇒ 按现文可直接进 Phase B, 若 owner 裁 Level 3 则整个 A.2/A.3 要回补 (证据: proposal.md:3,255,266,357; `ls openspec/changes/handoff-multibranch-subdir-path-fidelity/` = 仅 proposal.md)
- [minor] documentation/§What.2 / §6.2 / Task 2.2(b) / Task 4.2: **legacy 公式四处的第三处行号错**。实测 `legacy:<branch>:<filename>` 在 `handoff_multibranch.py` 命中 3 次: `:36` / `:332` / **`:494`**; v5 五处写作 `:495-496` (proposal.md:117,206,257,265,305), 而 `:495-496` 那两行是「so two legacy rows can never share a dedupe key…」, 不含该公式。R3 rework 记录还专门把审计席给的 `:493-496`「勘正」成 `:495-496` —— 勘正动作自身出错 (memory `feedback_author_and_verifier_must_differ_for_corrections` 形态)。SC-11(i) 的 grep 不看行号故仍能兜底, 不构成假绿 (证据: handoff_multibranch.py:493-499)
- [minor] documentation/§6.2 / Task 4.2: **三行同族 docstring 未登记**。`:243`「Uses ``git ls-tree -r --name-only origin/<branch> -- docs/handoff/``」在加 `-z` 后失真 (而 `-z` 正是 F2 的载重机制); `:298`「``git show origin/<branch>:docs/handoff/<filename>``」与 `:315`「``git log -1 --format=%aI origin/<branch> -- docs/handoff/<filename>``」在入参改名 `rel_path` 后同样过时。后两者与**已登记**的 `:332` 是同一理由 (§What.2 原话:「就在 Task 2.2 要改的函数头上, 改代码不改它等于当场留一条自相矛盾的注释」), 本 spec 只对三个姊妹函数中的一个施加了这条标准 (证据: handoff_multibranch.py:241-248,296-299,313-318; proposal.md:206,265)
- [minor] documentation/rule6_note 首条前提句: **「无 references 的文本变动」已被自身任务表证伪**。rule6_note 的「变更性质 (不变的部分)」逐字写「**无** SKILL.md / references 的文本变动」, 而 v5 的 Task 4.2 要改 `references/phase-1-collectors.md:102`、Task 4.4 要改 `state-scanner/references/layer-l-integration.md:103`。Rule #6 结论 (照跑 state-scanner AB) 不因此改变 —— 两文件都在 state-scanner 自己的 AB 射程内 —— 但这条支撑前提为假, 会让 owner 低估处方面半径 (证据: proposal.md:266,336)

### Risks

- [major] architecture/§5 消费方枚举 / §2.5 / Impact: **active track 计数是第五个被本 spec 改动却未登记的量**。§5 与 Impact 登记了 `exists` / `len(tracks)` / `legacy_count` / `collision.kind` / `identity_advisories` 五个量, 唯独漏了 `n_active`。路径修好后子目录件从 legacy 变真 track, 被 `_get_active_tracks` (`latest_md_writer.py:89-94`) 收进 ⇒ `write_latest_md:298-310` 的 **0 / 1 / ≥2 三分派**可从 1 翻到 ≥2 ⇒ 走 `_render_banner` (`:172-223`, 输出**不含** `**Latest**: [` 行) ⇒ `handoff.py:263-266` 的 `_LATEST_POINTER_RE` 不匹配 ⇒ `latest_source` 静默退回 `"mtime"` 且零 soft_error。§2.5 的写侧守卫只活在 `n_active == 1` 这一支, 覆盖不到; SC-15 三个布局最高只到 1 active。可达性非假想: schema `:1118` 逐字记载历史行的 frontmatter「frozen at write time (`status: active`) and never rewritten」, 本仓 `docs/handoff/` 190 份交接里实测 **22 份 `status: active`** —— 归档进子目录的采用方 (即 #195 报告方形态) 正是这个人群。讽刺处: Task 4.4 要改的 `standards/conventions/session-handoff.md:172-173` 恰恰就是按「1 active track / ≥2 active tracks」分档的那张表, 而本 spec 只从 `n_active == 1` 这一格里往外看
- [minor] architecture/§What.1 前缀守卫 / §4 / §7 末条: **`unreadable_count` 的外延未定**。这个新机读契约字段 (CHANGELOG `### Added`、schema 常驻) 的计数范围只被 SC-5 钉住「git show 失败」一例, SC-14 钉早退为 0。前缀守卫 (`handoff_multibranch_unexpected_path_prefix`) 丢弃的行是否计入无定论; 不可解码 UTF-8 名更被 §7 末条与 Impact.Risk 末条给了两个**互斥**选项 (「计入 unreadable_count」vs「显式跳过, 对齐 `handoff.py:319-322` 先例」) 且未择一 ⇒ 新契约的语义会由实施者随手决定, 再由 Task 4.1 写进 schema SOT (证据: proposal.md:107,222,232; handoff.py:319-322)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **4** / Minor **4** (另 6 条 decision 按 R1-R3 同口径不计入 severity)。

rationale: 方案骨架 (A′ = `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git show 失败不再伪造 legacy + 写侧守卫) 经本席独立代码级复核成立, **不主张推翻**; R3 的 19 条 major 全部落进正文而非批注, 无系统性回填矛盾; ship 顺序 / gitlink 起点 / 版本号占用 / 越界面四项独立实测全部正确。无 Critical: 无一条构成方案错误、无一条会打断今天在跑的生产消费方 (`write_latest_md` 零生产调用点这一既有事实仍成立)、无一条造成 SC 恒绿假绿。

4 条 Major 集中在**同一族**——「新契约或被改动的量, 走到边界处就没人接手了」:

1. `degraded_reason` 有取值定义、无产生路径 (最省事实现重造本 spec 的根因模式);
2. `scan.py` 改读 `rel_path` 后, 同函数两个**上报**字段的归属未定 (R3 `b57e3209` 修的是同一函数相邻两行, 这是它没走完的那半);
3. `n_active` 是第五个被改动的量, 却是唯一没进 §5 / Impact / CHANGELOG 的那个, 而它直通 writer 的三分派与 Task 4.4 要改的那张 SOT 表;
4. 待复议 7 (Level) 无任务承接, 而它决定 Phase B 之前要不要先补 A.2/A.3。

四条都可在 Phase A 内改 spec 消解, 零设计骨架改动。4 条 Minor 为文档面精度问题, 其中 `:495-496` 行号错是 R3 rework「勘正」动作自身产生的, 建议由非 R3 执笔者复核。

按 Rule #10, 上述 major 不得由实施者以「代码面小 / Level 低 / session 已长」自行降格或改序; 其中第 4 条与既有的待复议 6 / 7 / 8 同属 **owner 门**, 本席不代裁。`post_spec` 为 `blocking: false`, 本 verdict 不阻断后续流程。

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 — Conclusions 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6), 去重前 60
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**

### Round 2 (承前)

- Agents: 5/5 — Conclusions 31 (Critical 3 / Major 10 / Minor 9 / Decisions 9), 去重前 55; 与 R1 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**; conflicted 1 (`cecc06af`, 已由 rework hermetic 实跑闭合)

### Round 3 (承前)

- Agents: 5/5 — Conclusions 33 (Critical 0 / Major 19 / Minor 7 / Decisions 7), 去重前 51; 与 R2 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **PASS_WITH_WARNINGS**; conflicted 1 (`120e1171`, 已由 R3 rework 双前提实跑闭合)

### Round 4 (本轮 — tech-lead 单席)

- **Agents**: tech-lead (本报告为单席产出; 聚合由汇总席合并五席后计算)
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品
  - 扫描面: `openspec/changes/` 8 个在制 spec 逐一检查, 引用 `Aria#195` 的仅本 spec; 唯一与 aria-plugin 发版面重叠的 `pre-merge-completeness-gate-change-scope` (#199) 触点为 audit-engine + `ab-suite/audit-engine.json` + `version.yaml`, 与本 spec 五触点零文件交集; `docs/handoff/latest.md` track 表在飞仅本容器 M6 轨 (aria-orchestrator)
- **Conclusions**: 10 条 — Critical 0 / Major 4 / Minor 4 / Decisions 6 (decision 不计入 severity)
- **与上轮的关系**: R3 的 19 条 major 逐条复核**均已落进正文**, 本轮无一条重开; 4 条 major 全部为新增 —— 其中 2 条 (`degraded_reason` 产生路径 / `scan.py` 上报字段) 落在 R3 rework 新写段落的下游, 1 条 (`n_active`) 是前三轮均未测到的机械事实, 1 条 (Level 无任务承接) 是 R3 新增待复议 7 与 Task 2.0 之间的接缝
- **Vote**: REVISE (Major 4 > 0)
- **本席实跑 / 实读清单** (可复现): `git rev-parse HEAD` / `ls-tree HEAD aria standards` / `git -C aria rev-parse origin/master` / `git -C standards rev-parse origin/master` / `git -C aria tag --list 'v1.7*'` · `handoff_multibranch.py` 的 `:14-44` / `:170-182` / `:240-290` / `:293-336` / `:390-400` / `:425-460` / `:488-500` / `:515-530` / `:555-600` / `:612-665` · `latest_md_writer.py:25-40,75-170,171-235,255-320` · `scan.py:160-215,240-300,380-400` · `handoff.py:260-330,380-410,435-460` · `state-snapshot-schema.md:1100-1175` · `standards/conventions/session-handoff.md:93-100,168-176` · `test_p1_layer_h.py:228-275` · SC-11 五组 grep 计数 · `docs/handoff/*.md` 的 `status:` 分布 (190 份 / 22 份 active) · `"rel_path"` 全树键名占用扫描
