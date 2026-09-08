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
timestamp: 2026-09-07T05:49:57.474Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [knowledge-manager]
---

# post_spec R2 单席报告 — knowledge-manager (pre-merge-completeness-gate-change-scope)

席位透镜: 知识与文档一致性 —— 头部字段机械判据 / Rule #3 同步面完整性 / 与 standards·CLAUDE.md 规则 (Rule #6 判据表选行、Rule #10) 的冲突 / 术语与归档口径 / 引用的 issue·先例是否真实存在。本轮**只审不改**, 未触碰仓库任何文件 (工作区冻结)。

R1 处置复核方式: 对聚合报告的 5 critical + 9 major 逐条到 proposal 正文定位, 确认是「改判据本体」而非「加批注」; 再对 R1 rework 引入的新文本独立取证 (不继承上轮结论)。语料类统计一律对 `git ls-tree` 冻结树跑 (R1 rework 落盘 commit `813e82c`), 不对会随本轮审计增长的活目录跑。

---

## 审计结论

### Decisions

- [minor] documentation/R1 C5/M9 落地复核: R1 全部 5 critical + 9 major 均落在正文判据本体上 —— 末段匹配放宽 (:112)、两个排除计数拆分 (:119-126)、(b) 换 Phase A-only (:148)、(c) 纳入内联 `## Tasks` (:148,:153)、SC-2 形态族穷举 + 人工标注期望 (:245)、`--repo-path`/`--diff-repo-path` 分离 (:79-81)、config-loader + 空集短路 (:159,:163)、`mid_implementation` 排除 (:141)、对称有界包含 (:114)。无一条以批注形式敷衍 (证据: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md:79-163,245)
- [minor] documentation/语料事实底盘复算: 独立全枚举复现一致 —— 末段形态 **62** / `unattributed` **170** / 真 2-field legacy **6** (`post_spec-2026-04-12T0400Z.md` 等) / 合计 **238** / `C` = **152** / 前缀碰撞 **1** 对后缀 **0** 中缀 **0** / **25** 个 (checkpoint, change_id) 组合的自有报告全为末段形态; 归档语料 52 − 15 = **37** 亦一致。F1 (`.aria/config.json` audit 块 `pre_merge=off` / `post_planning=convergence` / `post_brainstorm=off`)、F5–F8 行号逐条实读命中 (证据: git ls-tree 813e82c -- .aria/audit-reports/ + /home/dev/Aria/.aria/config.json)
- [minor] documentation/头部字段合规 + 引用真实性: `> **Linked Issue**: \`10CG/Aria#199, 10CG/aria-plugin#161\`` 过 E0 三谓词 (行首 `> ` 单层、单个 code span、`, ` 分隔), 紧随的 `> **Issue**:` 行因字段名不在封闭集内不干扰 E0 定位; aria-plugin#161 `state=open` 且标题与头部引述逐字相符, aria-plugin#127 `state=open`; 三条归档先例目录实存, `2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:282-284` 逐字即「rule6_note 判据表第三行 + 三义务 + 缺口挂 #127」 (证据: spec-drafter/SKILL.md:414-424 · archive/2026-09-02-linked-issue-field-availability/proposal.md:164-201 · forgejo GET /repos/10CG/aria-plugin/issues/161,127)
- [minor] architecture/Rule #10 与 Rule #6 档位标签: 三态判据全部是机械结构事实 (无 AI 价值判断), (b)(c) 两条 not_applicable 均朝**收窄**改并明写「放宽须 owner 明示」, 头部审计计划与 `.aria/config.json` 七个 checkpoint 逐项一致 ⇒ 无 Rule #10 冲突。`rule6_note` 标签在全 skill 树无任何机械消费方 (`grep -rn rule6_note skills/` 零命中), 而「两读法并集」是第二行与第三行动作集的**超集**, 故档位分歧不构成 finding, 留复议 #5 (证据: configured-gate-authority.md:35-40 · skill-benchmark-exemption.md:26-33 · proposal.md:12,264-270)

### Issues

- [major] implementation/§1.2b + §1.4 stdout 契约 vs SC-10/SC-19: v3 新增的 `scanned_dir_depth` 要求与「顶层键集**逐字**为 …」清单互斥 —— 该清单 (`schema_version` … `elapsed_ms`) 不含 `scanned_dir_depth`, 而 SC-10 断言「顶层键集逐字 = 1.4 列表」、SC-19 断言「stdout 含 `scanned_dir_depth: 1`」。任何实现都必红一条。SC-10 括注只补了 R1 新增的 `unattributed_count`/`unattributed`, 说明这次漏更是 rework 下游 AC 漂移 (证据: proposal.md:134, 164, 253, 262)
- [major] documentation/§1.2b「schema 文档写明」+ §4 同步表 (Rule #3): 两条枚举边界都要求「schema 文档写明 / 须显式写明」, 但**未点名任何文件**; §4 的 `report-storage.md` 行只写归属匹配三句、不含「子目录不计入」与「无 checkpoint 前缀三桶都不收」; SC-13 的文档机检七条无一覆盖; Tasks 把该义务指向 SC-19, 而 SC-19 只断言运行时行为。⇒ 该文档义务既无落点文件、也无可证伪核验, 可静默不做 (证据: proposal.md:134-135, 192, 234, 258, 262)
- [major] testing/§4 ab-suite/version.yaml 行 + 头部 Rule #6 行: 事实错误且目标号已被占。实测 `aria-plugin-benchmarks/ab-suite/version.yaml` 首行 `version: "1.5.0"` (changelog 顶条 1.5.0 / 2026-09-05, 由同伴轨落), proposal 在 :12 与 :198 两处称「现值实测 **1.4.0**」并计划「1.4.0 → **1.5.0**」= 撞已存在版本; 该文件在 `3f4b379` (起草) 时确为 1.4.0, 但在 `813e82c` (R1 rework 落盘) 时已是 1.5.0 —— rework 的「实测」复核未复现。同时 §4 称同伴轨 `a1-entry-claim-duplicate-work-guard` 为「在飞」, 实为已归档 (`openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard`, Status `Complete (2026-09-06 归档; 40/40)`), 其 version.yaml 串行编排早已完成 ⇒ 并发预案的前提与目标号双双失效, 正确目标应为 **1.6.0** (证据: aria-plugin-benchmarks/ab-suite/version.yaml:1-9 · proposal.md:12,198 · openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:49)
- [minor] documentation/头部「gitlink 现况 (R1 实测勘正)」: 该块三句均已不成立 —— `git submodule status aria` = ` 301641b1c893… aria (v1.71.1)` (无 `+`, 即 checkout 与索引一致), `git -C aria rev-parse HEAD master origin/master` 三者全为 `301641b`, 主仓 gitlink 在 `813e82c` 与 `HEAD` 上均为 `301641b` (v1.71.1 主仓同步 commit `4c3c826` 是 R1 rework 的祖先)。故「本地 checkout 仍停在 `0545f86`」「本地 master 与 origin/master 已分叉」「否则会把 gitlink 回退到 v1.70.0」是幻影前置, 与它自己删掉的那条排队幻影同型 (证据: proposal.md:10 · git submodule status · git ls-tree 813e82c aria)
- [minor] documentation/§Why F3 计数分解: 实测 `openspec/changes` **8** 目录 (proposal 写 9)、`openspec/archive` **144** 目录 + `README.md` = **145** 条目 (proposal 写「143 目录, 第 144 个条目是 README.md」)。总数 `C` = 152 与「前缀碰撞 1 对」经全枚举复算成立, 错的只是分解式; 但这正是 R1 `ffd3834a` 勘正后新写的一句, 属勘正自身逃逸 (证据: proposal.md:50 · ls openspec/changes | wc -l = 8 · ls -d openspec/archive/*/ | wc -l = 144)
- [minor] documentation/References 规范行指针: `skill-benchmark-exemption.md` 的附加约束「`description` 或指令流程变动 ⇒ 一律第二行」在 **:33**, 而 proposal 标 `:35` (:35 是「## 3. 第三行不是逃生舱」小节标题); 判据表实为 **:26-31** 而非 `:25-33`。`project.md` 的 Level 2 行在 **:117**, `:118` 是 Level 3 行 —— 而 §1.3(c) 的核心论证正以 `project.md:118` 为锚。两处均只是指针偏移, 被引述的规范内容本身逐字成立 (证据: proposal.md:288, 153 · standards/conventions/skill-benchmark-exemption.md:26-35 · standards/openspec/project.md:114-118)
- [minor] documentation/头部「代码落点」vs §4 同步表: R1 rework 采纳「旧 schema 散文残留形态族穷举」后, §4 与 Tasks 都补入 `phase-a-planner/SKILL.md:267` 与 `phase-b-developer/SKILL.md:204,277` (全仓实测恰 4 处, 与 proposal 所列逐字一致), 但头部代码落点行仍只列 `phase-c-integrator/SKILL.md`。A.3 派单 / B.1 划范围若按头部读会漏三处 (证据: proposal.md:11 vs :196 · grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/ = 4 命中)
- [minor] testing/头部 Rule #6 行 vs rule6_note 的 substitute 集合: 头部写「脚本 + schema + 勘正 = 描述性 ⇒ substitute = **SC-1~SC-13** 结构化测试」, rule6_note 写「substitute = **SC-1~SC-10 + SC-13 + SC-15~SC-17**」。两处枚举互不相等 —— 前者把 SC-11 (活体 dogfood) / SC-12 (既有测试) / SC-14 (AB 本体) 卷进 substitute, 又漏掉 R1 新增的 SC-15~SC-17。Rule #6 的合规证据面自身不自洽 (证据: proposal.md:12 vs :270)
- [minor] testing/`unattributed` = 170 与 §1.4 计数作用域: 170 是对全 8 个 checkpoint 前缀取并集的口径 (本席在冻结树 813e82c 复算一致), 但 §1.4 明确把两个计数的统计面限定为「以**任一纳入校验的** checkpoint 名开头的文件的并集」。Step 3 恒排除 `pre_merge`/`post_closure`/`mid_post_spec`/`mid_implementation`, 故本仓 config (post_spec + post_planning) 下实跑输出为 **160** (legacy 仍 6)。SC-11 的绑定断言是 `> 0` 故不会假红/假绿, 但其引数「实测 170 份」与本 spec 自己的契约不同口径, Phase B 对不上数会误判实现 (证据: proposal.md:124,164,254 · 复算脚本对 813e82c: 全 8 cp = 170, {post_spec,post_planning} = 160)

### Risks

- 无新增 risk 条目。R1 记录的 R-a/R-b/R-c/R-d/R-e 五条在本轮复核中仍成立且缓解已落文; 其中 R-a 的量级 (170 / 6) 请按上条 minor 统一口径后重述。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **3** / Minor **6** (另 4 条 decision 不计入)。

rationale: R1 的两类致命缺陷 (归属谓词漏末段形态 ⇒ 假红阻断; 两条 not_applicable 通道以「产物文件在不在」代理「工序做没做」⇒ 假绿) 都已在正文判据本体上闭合, 且本席独立全枚举复现了它们赖以成立的全部语料数字, 没有一条是引述而未验的。因此本轮不再有 critical。

留下的 3 条 major 全部是**同一类**问题 —— rework 与 v3 追补之后, 文档面的下游没跟上:
1. `scanned_dir_depth` 加进了 §1.2b 与 SC-19, 却没加进 §1.4 的「逐字」键集, 于是 SC-10 与 SC-19 互斥, Phase B 必红一条;
2. §1.2b 两条边界要求「schema 文档写明」但没点名文件、没进 §4、没进 SC-13, 是一条无落点也无核验的文档义务 (Rule #3 同步面缺口);
3. `ab-suite/version.yaml` 的现值与同伴轨状态都被写成 R1 rework 时的旧快照 (实为 1.5.0 / 已归档), 目标号 1.5.0 撞已存在版本。

6 条 minor 集中在头部: gitlink 现况块、F3 分解式、两处规范指针、代码落点漏三处、Rule #6 substitute 集合、`unattributed` 口径 —— 其中四条是 R1 勘正动作**自身**引入或未随现实更新的, 与 memory `feedback_author_and_verifier_must_differ_for_corrections` 的形态一致, 建议 Phase B 的勘正批由非本轮执笔者复核一次。

按 verdict-format.md 计算: 0 Critical + ≥1 Major ⇒ PASS_WITH_WARNINGS; post_spec `blocking: false`, 本判定不硬阻断流程, 但 3 条 major 中的第 1 条会在 Phase B 直接卡住 (两条 SC 无法同时绿), 应在进 A.2 前修掉。

计算依据:
- Critical issues: 0
- Major issues: 3 (3 issue + 0 risk)
- Minor issues: 6 (6 issue + 0 risk)
- Decisions (不计入): 4

---

## 轮次记录

### Round 2

- Agents: knowledge-manager (本席单份报告; 本轮五席由编排侧聚合)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 13 (Critical 0 / Major 3 / Minor 6 / Decisions 4)
- Delta vs 上轮: R1 的 5 critical + 9 major 经逐条定位确认全部在正文落地, 本轮零继承; 新增缺陷全部锚在 R1 rework 与 v3 追补写下的新文本上 (§1.2b / §4 / 头部四行)
- Vote: **REVISE** (Major = 3 > 0)
