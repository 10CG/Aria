---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T09:45:30.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer 席 (R1 同席位)

**审计对象**: `openspec/changes/linked-issue-normalization/tasks.md` + `detailed-tasks.yaml` @ `3fc6f3f` (R1-fix, 17 → 21 任务)
**基线**: 我的 R1 报告 (1 Critical + 6 Major + 5 Minor) · 五席合计 3 Critical + 12 Major
**镜头**: (1) R1 十二条逐条实读核闭合 (2) **R1-fix 自身引入的新缺陷** (本轮重点)

---

## 第一部分: R1 逐条闭合判定 (12/12 实读核验)

| R1 # | 判定 | 实读证据 |
|---|---|---|
| **C1** 发版同步面漏 7 处 + 两 check 失明 | **partially_closed** | TASK-018 (i18n 各 3 处) / TASK-019 (CLAUDE.md 两处) / TASK-020 (零命中断言) 均已加, 主仓口径改为「引用点」且数字实测正确 (见下)。**残余: `proposal.md:271` §Impact 那一行仍是原来的文件数口径** —— 逐字仍为「aria 子模块 5 文件 + 主仓 gitlink + 主仓 `VERSION` 表行 + `README.md` 的 Plugin badge + i18n 的 `translated-from` 标记」, 仍缺 README.md:242 / i18n ×3 的 badge 与 :244 / CLAUDE.md 两处 (共 9 处), 并且**假绿论证也原样存活**: 该行仍写「后两项由 enabled custom check 守着 … **任何** bump 都会让三份 i18n README 判 STALE」。21 个任务里**无一条**修 proposal.md。fix 自己的 TASK-020 notes 写「三份文档 (proposal §Impact / tasks.md / 本文件) 首版都写文件数口径 …**同一形状第三次**」—— 结果只修了后两份 (`feedback_fix_the_class_not_the_instance`)。⇒ 列为 CO-1 |
| **M1** CLAUDE.md 无任务归属 | **closed** | TASK-019 (parent 5.6), deliverable `CLAUDE.md`, 落点注 `:139 版本区间行 + :141「版本:」行` —— 实跑 grep 命中行号逐字吻合 |
| **M2** 「9 处落点」vs 11 | **closed** (主仓半幅; 子模块半幅见 N-2) | 新口径 `main_repo_points: 14`。**我独立实跑**: 主仓 14 行命中 (ja 3 / md 2 / CLAUDE 2 / zh 3 / VERSION 1 / ko 3), 与 `breakdown` 六项逐格相同。全仓 grep 已无「9 处」残留 |
| **M3** `Ran ≥1367` 单位错 | **closed** (两条各自可证伪) | 拆成 ①`run_tests.py → OK, 0 failures/errors` (机械, 可证伪) + ②`17 条 SC 场景逐条清单核对` (可证伪但**无留痕要求**, 见残余 minor)。六条 `场景数 ≥N` 加总实算 13+5+15+8+1+3 = **45** = `test_counting_contract.scenario_count` ✅; 17 条 SC 在六组恰各一次 ✅ |
| **M4** TASK-007 引 SC-12 成环 | **closed** (四条新验收各自可证伪, 无重复覆盖) | verification 已无 SC-12, notes 明写「本任务 verification 不含 SC-12」。四条: ①`from lib import collision` 取到 —— **我实跑 (cwd=state-scanner) 成功, 解析到 `lib/collision.py` 而非 `scripts/lib`**, 可证伪 ✅ ②三步复合 (残余 minor, 见 N-6 前的注) ③None 与规则 4 三条一一对应 ✅ ④返回类型 ✅ (与 TASK-006 verification[1] 的重叠是**有意分层**: 007 = 读代码, 006 = 测试杀, 不构成「已被别的任务覆盖」) |
| **M5** SC-11 无 per-task 转绿断言 | **closed** | TASK-008 verification[0] 逐字 12 条含 SC-11, 我数 = 12 ✅ |
| **M6** TASK-013 无结果判据 | **partially_closed** | 四条**三条**逐字存在: `AB_TEST_OPERATIONS.md:546` "summary.yaml 已生成并审查" / `:547` "无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)" / `:548` "与上一次结果比对，无回归" —— 全在 `### 发版前` (:544) 之下 ✅。**但** "with_skill 表现优于 without_skill" 逐字在 `:542`「### **新增 Skill 后**」清单里, 不属发版前清单; 且**发版前清单第一项 `:545` "Tier 1 Skills 全量 AB 测试已执行" 被整条丢掉** ⇒ 列为 N-5 |
| m1 `:155 _TERMINAL` 措辞不准 | **closed** | 现写「`:210` tuple 含 unknown / `:307` tuple / `:155` 列表推导内联 tuple (无常量绑定, 值同 :307)」—— 三处实读逐字吻合 (`:155` = `[c for c in claims if c.status not in ("done","abandoned")]`) |
| m2 既有 6 条用行号锚 | **closed** | 改为「6 个 test 方法名与函数体逐字未变 (git diff 核, 非行号区间核)」, TASK-001 与 TASK-014 两处同步 |
| m3 TASK-009 ∥ TASK-010 同文件跨 owner | **closed** | TASK-010 改归 `backend-architect` + `dependencies: [TASK-009]`; `file_domain_serialization` 声明 007→008→009→010 全链串行, 与 21 条 deps 实测一致 |
| m4 DAG 图 ≠ dependencies | **closed** | 图现在只从 012 引出 013; 我把 21 条 deps 与 ASCII 图逐条对过, 无差 |
| m5 gitlink 不在 deliverables | **closed** | TASK-017 deliverables 首项 `aria  # gitlink (子模块指针)` |

**闭合率: 10 closed / 2 partially_closed / 0 not_closed。**

### 关于 C1 那条 grep 的三个专项核验 (按 R2 任务点名要求)

1. **它现在确实会红 (非空洞)**: 逐字复跑 TASK-020 的 grep → **20 行命中** (主仓 14 + aria 子模块 6), exit 0 ⇒ fix 之前/bump 之前该断言必红 ✅
2. **文件清单对主仓无遗漏**: 全仓 sweep (`grep -rn "1\.65\.5" .` 排除 .git) 后, 主仓侧除清单内 6 个文件外只剩三类**正确不动**的命中 —— `.aria/triage-comment.md` / `.aria/triage-report.json` (工具产物快照) · `.aria/repro/sc-baseline-*.py:32` (溯源注「aria 子模块 af87cae (v1.65.5)」) · `.aria/audit-reports/*` (审计史)。⇒ 清单**无第四类真实引用点遗漏** ✅
3. **排除项判断**: 排除 `aria/CHANGELOG.md` **正确** (`:13` = `## [1.65.5] - 2026-08-02`, 版本史)。**但漏排除一处同性质文件 — `aria/VERSION`** ⇒ N-1 (本轮最重的新缺陷)

---

## 第二部分: 结构化发现

```yaml
- type: issue
  severity: major
  category: documentation
  origin: carryover          # C1 的 SOT 半幅未闭
  scope: openspec/changes/linked-issue-normalization/proposal.md:271 · detailed-tasks.yaml TASK-020 notes
  summary: >
    C1 的根因 (同步面按「文件数」而非「版本引用点数」枚举) 只在 tasks.md 与 detailed-tasks.yaml
    两份修掉, proposal.md §Impact 那一行原样保留旧口径与旧假绿论证, 且 21 个任务里无一条修它。
    fix 自己把这一形状点名为「同一形状第三次」, 却只修了三份中的两份。
  evidence: >
    实读 proposal.md:271 逐字仍为「aria 子模块 **5 文件** + 主仓 **gitlink** + 主仓 `VERSION` 的
    子模块版本表行 + **`README.md` 的 Plugin badge** + **`README.{zh,ja,ko}.md` 的 `translated-from`
    标记**」—— 缺 README.md:242 / i18n ×3 的 badge (:10) 与 "Plugin Version:" 行 (:244) / CLAUDE.md
    :139,:141, 共 9 处。同一行仍写「后两项由 enabled custom check 守着 … 后者逐字比对标记 vs
    plugin.json, **任何** bump 都会让三份 i18n README 判 STALE」—— 我 R1 已实证该 check 只
    re.search("translated-from"), 正文一概不看, 这正是 C1 的假绿论证本体。
    grep 全 21 任务的 deliverables: 无 proposal.md。⇒ ship 后 Spec SOT 仍带错口径进归档,
    下一次 bump 继续继承 (第四次)。修法: 给组 5 加一条「proposal §Impact 同批订正为引用点口径 +
    删除『两条 check 守着』的措辞」, 或把 §Impact 那行改成指向 metadata.version_reference_surface。

- type: issue
  severity: major
  category: testing
  origin: new                # fix 引入
  scope: detailed-tasks.yaml TASK-020 verification[0] · tasks.md 5.7 · aria/VERSION
  summary: >
    TASK-020 的零命中断言把 `aria/VERSION` 纳入 grep 清单, 而该文件与被显式排除的
    aria/CHANGELOG.md 同性质 —— 它自身就是版本史 (49 行历史 release note, 逐行含旧版本号)。
    ⇒ 该判据不可判: 按文件内主流形态 (保留旧注为「发布日期(旧)」) 执行则**恒红**;
    按最近一次 bump 的做法 (覆写该行) 执行则**销毁 v1.65.5 的发布注**。
  evidence: >
    实读 aria/VERSION: `:3` = 当前版本 `> **版本**: 1.65.5`; `:4` = v1.65.5 的 release note;
    `:5`-`:52` = 48 行 `> **发布日期(旧)**: …  # patch/minor: v1.65.2 / v1.65.1 / v1.64.1 …`
    ⇒ 文件性质与 CHANGELOG 相同。两种前例并存: `git show af87cae -- VERSION` 显示上一次 bump
    **覆写**了前一条 (`-… v1.65.4 …` / `+… v1.65.5 …`), 而 :5 起的 v1.65.2 及更早**全部保留**。
    ⇒ 口径未定 ⇒ 实施者按「保留」写就撞恒红门, 而恒红正是 TASK-021 立意要杀的对偶
    (memory feedback_false_green_dual_is_permanent_red —— 本 Spec 全程在打这个对偶, 不能自己造一个);
    更坏的次生风险是诱发对 owner-configured 机械断言的临场降级 (Rule #10)。
    修法二选一: (a) 把 aria/VERSION 移入排除项并说明理由 (与 CHANGELOG 同理);
    (b) 窄化为行级断言 `sed -n '3p' aria/VERSION | grep -c "1\.65\.5"` == 0。

- type: issue
  severity: major
  category: documentation
  origin: new                # 「只把口径换在主仓」是 fix 的选择 (TASK-015 措辞本身是首版原文)
  scope: detailed-tasks.yaml metadata.version_reference_surface · TG-5 banner:441 · TASK-015 verification[0]
  summary: >
    「维度匹配」只落了主仓半幅。aria 子模块侧仍是文件数口径 (`plus: aria 子模块 5 文件`,
    TASK-015 判据「plugin.json 为 SOT, **其余 4 文件**与其一致」), 而该侧实测引用点 ≥6;
    且 TG-5 标题一句里混两种单位 ——「14 个主仓版本引用点 + gitlink + aria **5 文件**」。
  evidence: >
    实测子模块侧: `aria/.claude-plugin/marketplace.json` 有**两个** version 字段 (`:3` 顶层 /
    `:16` plugins[0]); `aria/VERSION` 有两个版本位 (`:3` 与 `:58` 的「## 版本号」代码块 ——
    后者今天实读是 **1.47.0**, 落后 18 个 minor); plugin.json `:4`; aria/README.md `:5`。
    ⇒ (a) TASK-015 的「其余 4 文件与其一致」**今天对 aria/VERSION 就是假的**, 该判据要么迫使
    实施者顺手修范围外漂移 (:58 / :64 说明块), 要么被松读放过 —— 两种都不是可判的验收;
    (b) TASK-020 的 grep 恰好能兜住 marketplace.json:16 (若 N-1 修掉), 但兜不住 :58 的 1.47.0
    (它不含 "1.65.5")。修法: 把子模块侧也写成引用点 breakdown (plugin.json 1 / marketplace 2 /
    VERSION 1(:3) / README 1), 并把 :58 的既存漂移显式记为「不在本 Spec 范围」以免判据自相矛盾。

- type: issue
  severity: major
  category: testing
  origin: new
  scope: detailed-tasks.yaml TASK-021 verification[0..3] · tasks.md 5.8
  summary: >
    TASK-021 把 (a)/(b) 二选一直接放进 verification 数组 ⇒ 无法判。本文件其余 20 个任务的
    verification 数组语义一律是**合取** (逐条都得成立), 而 (a)(b) 互斥 ⇒ 字面读法恒不可满足;
    若读成析取, 则「选了哪条」没有判定程序, 且两支本身都不是机械判据 (无可跑命令、无可查产物路径)。
  evidence: >
    verification 逐字: [0]「…**不再恒红** — 二选一并在脚本顶部成文选了哪条:」[1]「(a) 加
    post-implementation 模式…」[2]「(b) 显式退役…」[3]「无论哪条, substitute 论证的可复核性
    必须仍然成立」。与同批新增的 TASK-020 处置**不对称** —— 后者给了一条可复跑 grep, 前者
    只给了散文。⇒ 「不再恒红」既无命令也无期望 exit code, 审的人只能采信声称
    (memory feedback_falsifiable_evidence_for_binary_acceptance)。
    修法: 加 `chosen_branch: a|b` 字段 + 每支各自的机械判据 ——
    (a) `python3 .aria/repro/sc-baseline-linked-issue-normalization.py aria/skills/state-scanner` → exit 0;
    (b) 断言 `.aria/repro/` 下已无该文件 **且** `<存档路径>` 存在且内含 aria 子模块 SHA。

- type: issue
  severity: major
  category: architecture
  origin: new
  scope: detailed-tasks.yaml TASK-021 (两支各自的未覆盖后果) · proposal.md:181,219 · .aria/repro/sc-baseline-*.py:205-215
  summary: >
    TASK-021 的两支各留一个未被任何验收覆盖的后果, 且其中一个在它自己的 notes 里已被点名:
    (a) 支 —— 脚本硬编码 proposal 路径且 fail-CLOSED, Phase D 归档后恒 FATAL, 「8 条 SC 转绿」
    这条验收对它零覆盖 ⇒ 选 (a) 只是把恒红从 exit 1 换成 FATAL;
    (b) 支 —— 脚本移出 .aria/repro/ 会让 proposal.md 两处路径引用成 dangling, 而无任务改 proposal.md。
  evidence: >
    实读脚本 `:205-211` `_PROPOSAL = os.path.join(_HERE, "..", "..", "openspec", "changes",
    "linked-issue-normalization", "proposal.md")`, `:215` `sys.exit("FATAL: 找不到 proposal.md
    (%s) —— 漂移守卫无法核对, 拒绝以硬编码常量冒充比对基准。")`, `:234` 第二个 FATAL (表格式变更)。
    phase-d-closer 归档会把 Spec 移到 openspec/archive/ ⇒ 路径失配 ⇒ 恒 FATAL, **而归档就在同一周期内**。
    TASK-021 notes 自己写了「Spec 归档后再叠加『FATAL 找不到 proposal.md』」, verification 却只写
    「断言那 8 条 SC 已转绿」。
    (b) 支: 实读 proposal.md:181「**留证 artifact**: [`.aria/repro/sc-baseline-linked-issue-normalization.py`]
    (../../../.aria/repro/sc-baseline-linked-issue-normalization.py)」+ `:219` 再次以该路径作 substitute
    实证的 artifact 指针 (owner 2026-08-02 裁定 db2e983 承重)。grep 21 任务 deliverables: 无 proposal.md
    ⇒ 选 (b) 就在 owner 裁定所依赖的证据指针上制造 dangling ref
    (memory feedback_cross_doc_claim_verify_at_target)。

- type: issue
  severity: major
  category: testing
  origin: new
  scope: detailed-tasks.yaml TASK-013 verification[1..3] · tasks.md 4.1 · aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:397-400,483,542-548
  summary: >
    引「AB_TEST_OPERATIONS.md 发版前清单」时 3 抄 · 1 换 · 1 漏: 换进来的一条来自另一个清单,
    漏掉的那条恰是唯一会扩大范围的一条 —— 而本 Spec 改的 state-scanner 实测就在
    「Tier 1 核心 Skills (每次发版必测)」P0 名单里。收缩 enabled 门却未披露 (Rule #10)。
  evidence: >
    实读 `:544 ### 发版前` 下四项 = `:545` "Tier 1 Skills 全量 AB 测试已执行" / `:546`
    "summary.yaml 已生成并审查" / `:547` "无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)" /
    `:548` "与上一次结果比对，无回归"。计划引的第一条 "with_skill 表现优于 without_skill"
    实际在 `:542`, 属 `### 新增 Skill 后`。计划**未引** `:545`。
    而 `:397` 逐字「### Tier 1: 核心 Skills (10 个, **每次发版必测**)」表内 `state-scanner | 8 | with:100% | P0`;
    `:483` 再写「每次发版前跑 Tier 1 全量 AB 测试 (场景 3)」。
    ⇒ 计划把发版前门缩到「单 hunk 的 AB」, 既未在 notes 声明该收缩, 也未请复议
    (memory feedback_written_exception_exact_condition_match: 援引成文清单须逐字核对确切条件;
    memory no-self-exempt-gates: 收缩 enabled 门不是 AI 的临场判断)。
    修法: 要么加判据/任务覆盖 Tier 1 全量, 要么在 TASK-013 notes 显式写「本轮只跑 state-scanner
    单项, 发版前清单第 1 项按 <理由> 降级, 请 owner 复议」并写进 handoff。

- type: issue
  severity: minor
  category: testing
  origin: new
  scope: detailed-tasks.yaml TASK-020 verification (单向性)
  summary: >
    TASK-020 只有负向断言 (旧版本号零命中), 无配对正向断言 (新版本号在每个点各出现应有次数)
    ⇒ 对「写成错的新值」这一维度免疫; 而两条 enabled check 只覆盖 README.md badge 与
    translated-from, 其余 7 处 (CLAUDE.md :139/:141 · README.md:242 · i18n ×3 的 :244 · VERSION:24)
    在被写成 1.66.1 / 1.6.60 时零命中 + 两 check 全绿。
  evidence: >
    同一份 metadata 引的 memory feedback_invariant_dimension_must_match_error_dimension 的判据是
    「不变量维度须等于错误维度」—— 「残留旧值」与「写错新值」是两个方向, 零命中只覆盖前者。
    修法: 追加正向断言 `grep -c "1\.66\.0"` 逐文件 == breakdown 预期数
    (README.md 2 / zh·ja·ko 各 3 / CLAUDE.md 2 / VERSION 1 / 子模块 4 文件各自数)。

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml TASK-010 task_group:348 vs TG-2 banner:264-266 vs TG-3 banner:368-370
  summary: >
    TG-3 分组三处口径不一: TASK-010 的 `task_group: TG-3` 与 parent 3.1 一致, 但它物理落在
    TG-2 banner 之内, 而 TG-3 banner 又写「3.1 见 TASK-010, 归 TG-2 文件域」。
  evidence: >
    `:264-266` banner 逐字「TG-2 — 实现 (GREEN). 单文件 aria/skills/state-scanner/lib/collision.py,
    全链串行」, 其后依次是 007/008/009/**010**; `:348` `task_group: TG-3`; `:368-370` banner
    「TG-3 — 文档同步 (3.1 见 TASK-010, 归 TG-2 文件域)」。
    ⇒ 任何按 task_group 聚合的消费者会读到 TG-2 = 3 条 / TG-3 = 3 条, 而 DAG 与
    file_domain_serialization 都把 010 当 TG-2 链尾。已部分披露故 minor;
    修法: task_group 改 TG-2 并在 tasks.md 3.1 处注明「编号留在组 3 (编号不可变约束), 文件域属组 2」。

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml metadata.scope_repos[Aria].surface:26 vs TASK-013 deliverables
  summary: >
    主仓 surface 声明漏 `aria-plugin-benchmarks/ab-results/` —— 它是 TASK-013 的唯一 deliverable,
    且实测确为主仓普通 tree。范围声明与 deliverables 并集不闭合。
  evidence: >
    `:26` surface 逐字「gitlink · VERSION · README.md · README.{zh,ja,ko}.md · CLAUDE.md ·
    Spec 本体 · .aria/repro/」。实测 `.gitmodules` 只含 standards/aria/aria-orchestrator,
    `git ls-files -s aria-plugin-benchmarks` 命中普通 blob ⇒ TASK-013 notes 的「主仓普通 tree
    (实测, 非子模块)」为真, 但 scope_repos 没跟上。`ab-results/` 目录存在 (2026-03-13 起 N 个子目录)。

- type: issue
  severity: minor
  category: documentation
  origin: new
  scope: detailed-tasks.yaml TASK-016 deliverables `aria/` vs TASK-017 deliverables `aria`
  summary: >
    两个 deliverable 仅差一个尾斜杠来区分「子模块工作树/master ref」与「gitlink」, 而
    path_convention 只规定了「子模块内文件带 aria/ 前缀」, 未定义这两个裸形态的语义。
  evidence: >
    TASK-016 `- aria/          # 子模块 master ref (合并提交)`; TASK-017 `- aria                # gitlink`。
    机读消费者 (归档门 / handoff_autofill 的 deliverables 扫描) 无从区分; 建议写成
    `aria (submodule master ref)` 与 `aria (gitlink @ main repo index)` 或加显式 kind 字段。

- type: issue
  severity: minor
  category: documentation
  origin: pre-existing        # 非 fix 引入, R1 未报; 不计入 fix 引入占比
  scope: detailed-tasks.yaml metadata.scope_repos[Aria].head:25
  summary: >
    主仓 head 锚仍是 `a52ab81`, 已被 R1-fix 自身的 `3fc6f3f` 取代 ⇒「路径与行号已对该 HEAD
    实测」的锚指向上一个提交。
  evidence: >
    `git log --oneline -1` = 3fc6f3f。我实测本轮引用的全部主仓行号 (CLAUDE.md:139/141 ·
    README.md:8/242 · README.{zh,ja,ko}.md:3/10/244 · VERSION:24) 在 3fc6f3f 下仍逐条命中,
    故只是锚陈旧, 不是引用错误。aria 子模块 head `af87cae` 经 `git submodule status` 实测正确。
```

---

## 第三部分: 确认做对的 (fix 的正面面, 逐条实证)

1. **派生数字这次全对** —— 而且警告被换成了可复跑命令 (`feedback_invariant_needs_failclosed_default` 的正解)。我直接跑了 footer 里那条命令: `21 tasks | {'M': 6, 'S': 14, 'L': 1} | 88h anchor | 88h sum | {'qa-engineer': 9, 'backend-architect': 7, 'knowledge-manager': 5}` —— 与 footer 三行逐格一致, 且**两法互证** (锚公式 14×3+6×6+1×10 = 88 = 逐条 est_hours 相加 88)。parent 21 个互不重复且恰为 tasks.md 的 21 个 checkbox。
2. **零命中断言是非空洞的**: 逐字复跑得 20 行命中 ⇒ 它今天必红, 不是恒真装饰。
3. **主仓引用点清单经全仓 sweep 无遗漏**, 且 `aria/CHANGELOG.md` 的排除理由正确 (`:13` 是版本史行)。
4. **`#133` 的覆盖这次是真的**: Forgejo API 实查 comment `17976` (2026-08-08T09:36:49Z, 早于 fix commit 09:45), 内含 3×成员集表格, 逐字写「加上 `collision.py` 后是 **6 处具名定义 + 1 处内联, 3 种成员集**」—— 与 TASK-008 notes 的引述逐字吻合。R1 抓的「范围纪律论证建立在不存在的覆盖上」这次是用真 artifact 关掉的, 不是用措辞关掉的。
5. **collision.py 引用精度回到 100%**: `:155` 内联 tuple / `:210` 含 unknown / `:307` 两元 tuple / `:217` 裸 `!=` / `:228` 回显 —— 五处实读全中, R1 唯一的措辞误差已修。
6. **TASK-009 依赖从 007 改到 008 的理由站得住**: SC-6/6b/10 是 baseline-GREEN 护栏, 在 008 之前对新写 guard 判绿是假阳性 —— 这条是 R1 五席里最容易被当成「多余的边」而漏掉的, fix 收对了。
7. **同文件并行边已全部消除**: 001→005 串成链, 006 经 007 间接排在 005 之后, 007→010 串成链; 我按 21 条 deps 做了拓扑就绪集检查, 无同文件任务对可同时就绪。
8. **`.aria/repro/` 进了主仓 surface**, TASK-021 让「恒红」这个对偶第一次有了任务归属 —— 方向完全正确, 只是判据形态没跟上 (N-3/N-4)。

---

## Verdict

**verdict: FAIL** (0 Critical + **6 Major** + 5 Minor)
**vote: REVISE**

FAIL 而非 PASS_WITH_WARNINGS 的理由 (与 R1 口径一致 —— R1 把 Major 全部列为「Phase B 开工前必修」): 六条 Major 里有**三条使承重验收字面不可判**(N-1 恒红/销毁史二难 · N-3 二选一放进合取数组 · N-2「其余 4 文件与其一致」今天即假), 一条是**未披露的 enabled 门收缩**(N-5, Rule #10 明令不得由 AI 临场决定), 一条会在 owner 裁定所依赖的证据指针上制造 dangling ref (N-4)。

### 阻塞项

| # | 项 | 落点 | 类别 |
|---|---|---|---|
| N-1 | 零命中断言含 `aria/VERSION` (版本史文件) ⇒ 恒红 或 销毁发布注 | TASK-020 / tasks.md 5.7 | new |
| N-3 | TASK-021 (a)/(b) 二选一放进合取型 verification, 且两支都无机械判据 | TASK-021 / tasks.md 5.8 | new |
| N-4 | (a) 支归档后恒 FATAL; (b) 支使 proposal.md:181/:219 成 dangling, 无任务修 | TASK-021 · proposal.md | new |
| N-5 | 发版前清单 3 抄 1 换 1 漏; state-scanner 是 Tier 1「每次发版必测」 | TASK-013 / tasks.md 4.1 | new |
| N-2 | 维度匹配只落主仓半幅; TASK-015「其余 4 文件与其一致」今天即假 | metadata / TASK-015 | new |
| CO-1 | proposal.md §Impact 仍是旧口径 + 旧假绿论证, 无任务修 (同形状第三次只修两份) | proposal.md:271 | carryover |

### fix 引入占比 (拐点判据)

| 口径 | 计算 | 结果 |
|---|---|---|
| Major 中 fix 引入占比 | 5 (N-1..N-5) / 6 (含 CO-1) | **83%** |
| 全部 finding 中 fix 引入占比 | 9 / 11 (另 1 carryover + 1 pre-existing) | **82%** |
| Major 数跨轮 | R1 = 6 → R2 = 6 | **持平** |

⇒ 两条成文判据同时点亮: `feedback_audit_marginal_return_goes_negative` (本轮 fix 引入的 major 占比 > 1/2 = 已过拐点) 与 `feedback_stop_adding_rounds_when_major_count_flattens` (major 持平 = 每轮 fix 吸收约等量同形状缺陷 = 不收敛)。这与母 Spec 的 R3′ 实测 (26 major 中 22 条 fix 引入) 是同一曲线。

### 给 R3 的处置建议 (不建议同席位再加一轮)

1. **别再逐条打补丁**。本轮 5 条 new major 里有 4 条的形状相同 —— **fix 用散文补了判据, 但没给判据配可跑的东西** (N-1 的 grep 覆盖过宽 · N-3 无命令 · N-4 未覆盖第二失效模式 · N-7 单向)。建议一次性收成**一个 bump 后置脚本** (`.aria/repro/version-surface-assert.py`): 输入 = plugin.json 版本, 输出 = 逐文件逐点的旧值零命中 + 新值计数匹配, 内建 CHANGELOG/VERSION-history 的行级白名单。这一条同时吃掉 N-1 / N-2(b) / N-7, 并且是唯一能防「第四次」的形态。
2. **N-3/N-4/N-5 是 owner 裁量项, 不该由 AI 在下一轮自选**: (i) sc-baseline 走 (a) 还是 (b); (ii) 发版前 Tier 1 全量 AB 这一门本轮跑还是显式降级。两者都属「收缩/选择 enabled 门与 owner 裁定的落地形态」⇒ 按 Rule #10 写进 handoff 请裁, 不要在 R3 里自行择一。
3. **CO-1 (proposal.md) 只需一条任务**, 但必须真加 —— 它是本 Spec 唯一会被归档进 SOT 的口径面。
4. 若仍要再审, **换新鲜眼睛**优于加轮 (R5 新席一轮抓 5/6 major 的先例)。

---

## 轮次记录

| 轮 | 席位 | 结论 | Critical | Major | Minor | fix 引入 major 占比 |
|---|---|---|---|---|---|---|
| R1 | code-reviewer | REVISE | 1 | 6 | 5 | — |
| R2 | code-reviewer | REVISE | 0 | 6 | 5 | **5/6 = 83%** |

**本轮方法**: R1 十二条逐条回到原文实读判闭合 (不采信 fix 的自述「已吸收」); 实跑 6 组命令取 ground truth —— TASK-020 的 grep 逐字复跑 (20 命中) · 全仓 `1.65.5` sweep (定位漏排除与遗漏) · `git show af87cae -- VERSION` (取 bump 惯例的 ground truth) · footer 那条 python 重算命令 (21/S14M6L1/88h/9-7-5 + parent 唯一性) · `from lib import collision` 真导入 (核 TASK-007 verification[0] 可满足) · Forgejo API 实查 issue #133 comments (核「已补评论」不是纸面声称); 另实读 AB_TEST_OPERATIONS.md 四段清单与 Tier 表、sc-baseline 脚本 :196-240 与 :268-285、collision.py 五处、marketplace.json 全文、aria/VERSION :1-67、proposal.md :262-271 与 :181/:219。
