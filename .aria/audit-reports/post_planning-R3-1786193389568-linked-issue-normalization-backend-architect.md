---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T12:49:49.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — backend-architect — 组 5 (TG-5) 专项

审对象: `openspec/changes/linked-issue-normalization/` 组 5 / TG-5, HEAD = `2cf2569`。范围严格限定
`tasks.md` 「## 5.」整段 + `detailed-tasks.yaml` TASK-014 / TASK-015..021 (cancelled) / TASK-022..027 /
`metadata` 相关块。未审组 1–4。

镜头: 「委派/移交给外部单元时是否核实了那个外部单元真的做那件事」+「路径与机制真实性」。

## 已知三条 (不重复报, 已核实其结论在本次独立实读中站得住)

我对以下三条做了独立交叉验证 (非仅采信另两席措辞), 结论: 三条均成立, 且都是 **R2-fix (2cf2569) 本轮新引入**的缺陷 (不是 R1-fix 之前就有的):

1. **[critical]** 委派 `phase-c-integrator` 做子模块合并, 但真实合并链 (`C.2.4:253 → branch-manager merge action → curl -X POST .../pulls/{pr}/merge -d '{"Do":"merge"}'`) 是 CLAUDE.md 硬约束 1 明文禁止的服务端合并。TASK-016 被删且是全 Spec 唯一写这两条硬约束的地方。这是本轮 (TASK-016 cancelled → 委派 phase-c-integrator) 才引入的缺陷 (R1-fix 的 TASK-016 是手工步骤, 不依赖 phase-c-integrator 是否会做对)。
2. **[critical]** 主仓 gitlink bump 零归属: TASK-017 cancelled + TASK-023 明文排除 + TASK-026 声称「C.2.5 既有机制保证」, phase-c-integrator 全文无 gitlink bump 步骤。同属本轮新引入 (旧 TASK-017 直接持有 gitlink 交付物)。
3. **[major]** CANCELLED 用 `- [ ]` 使 `is_spec_complete` (`aria/skills/state-scanner/scripts/lib/spec_complete.py`) 归档门恒红。我独立读了该模块的判定逻辑, 确认: `tasks.md` **存在**时, 完成度判据是分支一 `(tasks.md 存在 AND 全 [x] AND 无 carry-forward 注释)`, **不会**回落到读 `detailed-tasks.yaml` 的 `status` 字段 (那只在 `tasks.md` **缺失**时才生效)。本 Spec `tasks.md` 显式存在且组 5 段的 7 条 CANCELLED 全部写成 `- [ ] ~~5.x ...~~`, 故无论 `detailed-tasks.yaml` 里 `status: cancelled` 写得多准确, 归档门看的是 `tasks.md` 的 checkbox, 完工后仍恒 7/27 unchecked。**元数据里把这归因描述为「归档门消费本文件 (detailed-tasks.yaml) 全部 27 个 checkbox」并不精确** —— 实际消费的是 `tasks.md` 的 checkbox (两文件此处内容平行, 结论不变, 但归因对象错了一层, 附带一提, 不单独计分)。

## 新发现

- type: gap
  severity: major
  category: assertion-completeness (双向断言的「先枚举」半只做了一半)
  scope: TASK-024 (5.11) + `metadata.version_reference_surface`
  summary: >
    TASK-024 verification 逐字写「预期点数**先枚举后断言**...见 `metadata.version_reference_surface.breakdown`」。
    但 `breakdown` dict (`detailed-tasks.yaml:103-109`) 只有 6 个 key (`README.md`/`README.zh.md`/`README.ja.md`/
    `README.ko.md`/`CLAUDE.md`/`VERSION`), 全部是**主仓**文件, 求和 = 14 = `main_repo_points`。
    而 `normal_reference.files` (:119-120) 明列 9 个文件 (上述 6 个 + `aria/.claude-plugin/plugin.json` +
    `aria/.claude-plugin/marketplace.json` + `aria/README.md`), 后 3 个 aria 侧文件**不在** `breakdown` 里 ——
    TASK-024 的判据文字指向一个结构性不覆盖它们的对象。实读三份 aria 侧文件的「预期点数」在全文件的落点:
    - `plugin.json`: 有, 但只在 TASK-022 deliverables 行内注释 `# 版本 SOT (1 点)` (:701), 不在 breakdown。
    - `marketplace.json`: 有, 同样只在 TASK-022 行内注释 `# **2 点**...` (:702) 与 `aria_side_points` 散文
      (:130), 不在 breakdown。且 `aria_side_points` 文字本身有计数瑕疵: 写「**4 个**普通引用点文件」,
      但 `normal_reference.files` 里 aria 侧只有 **3 个文件** (4 个点是 1+2+1 三文件之和, 「文件」与
      「点」两个单位在这句话里被混用, 与本 Spec 全程强调的「场景数≠Ran 数」「文件数≠引用点数」两次
      教训同一种混淆形状)。
    - `aria/README.md`: **全文件零处**写明其预期点数。我实测该文件只有 1 处版本号 (`:5`, `> **Version**:
      1.65.5 | **Released**: 2026-08-02`), 期望值显然是 1, 但这是我从源文件反推出来的, Spec 本身在 9 个
      `normal_reference` 文件里唯独没有为它写下任何「= N 点」的断言依据。
    净效果: TASK-024 标榜要修的正是 R2/tech-lead N3 (「只断言旧值缺席 = 缺席断言, 维度只对一半」),
    而它自己引用的枚举表对 9 个应枚举对象中的 3 个 (aria 侧) 结构性缺席 —— 其中 1 个 (`aria/README.md`)
    连散落的行内注释也没有。这是同一形状缺陷在自己修复对象内部的局部复发 (但不是本轮的核心/唯一判据,
    marketplace.json/plugin.json 的计数实际上是对的, 只是位置不对; 故定 major 非 critical)。
  evidence: >
    `detailed-tasks.yaml:99-130` (breakdown 只 6 key, `aria_side_points` 措辞), `:701-703`
    (TASK-022 deliverables 行内注释), `aria/README.md:5` (实测唯一版本行), `aria/.claude-plugin/marketplace.json:3,16`
    (实测 2 个 version 字段, 数值正确), `aria/.claude-plugin/plugin.json:4` (实测 1 个 version 字段, 数值正确)。
  origin: new

- type: undercount
  severity: minor
  category: 自我指涉的枚举纪律缺口
  scope: TASK-025 (5.12)
  summary: >
    TASK-025 verification 写「同批修 `proposal.md:181/:219` 两处 artifact 指针」。实读 `proposal.md`,
    该脚本路径出现 **3 处**: `:181` (留证 artifact 的 markdown 链接) / `:183` (紧邻的 repro 命令行,
    同一 blockquote 代码块内) / `:219` (框定合规段落引用)。`:183` 未被计入。风险实际很低 (`:183` 与
    `:181` 同段落相邻两行, 修 `:181` 时顺手带到的概率很高), 但本 Spec 通篇的立论正是「枚举不全会让
    验收在不该绿的地方绿」(TASK-020→024 那整条修复线), 这里在处置自己的 substitute 留证脚本时又欠数了一处,
    是同一形状在收尾任务里的小范围复发。
  evidence: "`grep -n sc-baseline openspec/changes/linked-issue-normalization/proposal.md` → 181/183/219 三处命中, TASK-025 只写 181/219。"
  origin: new

## 未采信为发现的核实项 (逐条属实, 记录以证明镜头扫过而非漏检)

- `TASK-022` 声称 `marketplace.json` 有 2 个 version 字段 (`:3`/`:16`) — 实读 `aria/.claude-plugin/marketplace.json` 精确命中，属实。
- `TASK-022` 声称 `aria/VERSION` 是 append-only 账本、167 行、`:58` 有裸 `1.47.0` — 实读 `wc -l`=167、`sed -n 58p` 命中「```」代码块里的 `1.47.0`，属实（这是一段自 v1.41.0→v1.47.0 之后就再没被同步的独立「版本号」字段，本身已死 18 个版本，Spec 元数据已如实记录其存在，未虚报）。
- `TASK-023` 声称主仓 14 个引用点 (README.md 2 / zh 3 / ja 3 / ko 3 / CLAUDE.md 2 / VERSION 1) — 逐文件 `grep -n "1\.65\.5"` 精确复现，属实，且主仓 `VERSION:24` 恰是子模块表行。
- `TASK-024` 引用的两条 enabled check 失明面描述 (`m6-version-badge-match` 只比 badge、`i18n-readme-translation-currency` 只比 `translated-from`) — 实读 `.aria/state-checks.yaml:88-102` 与 `:141-156` 两条 check 的 `command:` 脚本，逐字确认只查各自声称的窄面，未覆盖 `README.md`「Plugin Version:」行与 i18n 的 badge/Plugin-Version 行，属实。
- `TASK-025` 引用 `:275-277` (baseline-failing 断言, `sys.exit(1)`) 与 `:205-215` (proposal.md 现场解析 + FATAL fail-CLOSED) — 逐行核对 `.aria/repro/sc-baseline-linked-issue-normalization.py`，`measured_face != EVIDENCE_FACE` 在 `:275`、对应 `sys.exit(1)` 在 `:277`，`_PROPOSAL` 路径构造在 `:205-209`、`_parse_spec_table` 的 `FATAL: 找不到 proposal.md` 在 `:214-215`；且验证了归档后的失效机制真实存在——`openspec-archive` 的归档目标是 `openspec/archive/<date>-<name>/`（非 `openspec/changes/archive/`），脚本硬编码路径指向 `openspec/changes/linked-issue-normalization/proposal.md`，归档后该路径确实会变为不存在，触发 FATAL，属实。
- `TASK-027` 引用 `AB_TEST_OPERATIONS.md:396`「Tier 1: 核心 Skills (10 个, 每次发版必测)」与 `:545`「Tier 1 Skills 全量 AB 测试已执行」——逐行核对，行号与文字逐字命中；且确认 `state-scanner` 确实在 Tier 1 十个之列，属实。
- 全部 deliverables 路径 (`aria/.claude-plugin/{plugin,marketplace}.json`、`aria/{VERSION,CHANGELOG.md,README.md}`、主仓 `{VERSION,README.md,README.{zh,ja,ko}.md,CLAUDE.md}`、`.aria/repro/sc-baseline-linked-issue-normalization.py`、`.aria/decisions/`) 逐条 `[ -e ]` 检查，**全部存在**；`aria/VERSION` 与主仓 `VERSION` 确认为不同文件、不同内容（前者是 167 行插件发布账本，后者是 39 行含子模块表的项目版本快照）。
- CANCELLED 七条 (`TASK-015..021`) 的 `superseded_by` 逐条核对：`TASK-015→022`、`TASK-017(部分)→023`、`TASK-018→023`、`TASK-019→023`、`TASK-020→024`、`TASK-021→025` 的技术性要求（文件枚举、custom check 名字、MINOR 措辞约束等）在新任务里均有承接（`custom check` 的显式调用被 grep 式双向断言取代，非遗漏，是判据升级）；`TASK-016→phase-c-integrator` 的承接失败已计入「已知三条」的第 1 条，不再单独计分。
- 依赖图自检命令 (`detailed-tasks.yaml:866`) 实跑复现: `20 active | {'M': 5, 'S': 14, 'L': 1} | 82 h | {'qa-engineer': 10, 'backend-architect': 6, 'knowledge-manager': 4}`，与文件所写逐字一致（此前两次订正的同一处这次没有第三次复发）。`total_tasks: 27`、`cancelled: 7` 亦用 `grep -c` 复核一致。
- `metadata.test_counting_contract.baseline` 声称的 `state-scanner 1322 tests OK` 与跨 skill `9 OK / 0 FAIL / 累计 1698` — 实跑 `run_tests.py` 与 `run_all_tests.sh`，两个数字逐字复现，属实（当前为 pre-implementation 基线态，与声称的口径一致）。

## 委派/移交逐条核实结果表

| 委派表述 | 出处 | 目标 X | 核实结论 |
|---|---|---|---|
| aria 子模块合并 + 双推 + gitlink bump | TASK-026 / metadata.scope_boundary.delegated | phase-c-integrator C.2.5 | **不成立** (已知 critical #1/#2, 目标做被禁止的服务端合并; gitlink bump 无步骤承接) |
| Phase D 归档消费本文件 27 checkbox | metadata.scope_boundary.delegated | phase-d-closer / is_spec_complete | **归因对象有误但结论不变** (实际消费 tasks.md 而非 detailed-tasks.yaml, 两者此处平行不改变「恒红」结论; 已知 major #3 涵盖) |
| enabled check m6-version-badge-match / i18n-readme-translation-currency 的失明面 | TASK-024 / metadata.enabled_check_blindness | `.aria/state-checks.yaml` 两条 check 脚本 | **成立**, 逐行核对命令体确认只测窄面 |
| TASK-024「先枚举后断言」引用 breakdown | TASK-024 / metadata.version_reference_surface.breakdown | 同 YAML 内的 breakdown dict | **不成立** (新发现 major, 见上) |
| sc-baseline 脚本行号与归档后失效机制 | TASK-025 | `.aria/repro/sc-baseline-linked-issue-normalization.py` + `openspec-archive` 归档路径约定 | **成立**, 行号精确命中且归档路径迁移机制确认真实 |
| AB Tier 1 门槛引用 | TASK-027 | `AB_TEST_OPERATIONS.md` | **成立**, 行号与文字精确命中 |

## 本轮 fix 引入占比

R3 本轮 (2 critical + 2 major + 1 minor，另一席 code-reviewer/tech-lead 的具体计数以其自身报告为准，此处只算我覆盖到的 6 条: 2 critical carryover-in-name-but-new-in-substance + 1 major carryover + 我的 1 major + 1 minor 新增) —— **6/6 (100%) 均座落在 R2-fix (`2cf2569`) 本轮新增/新写的内容里**: TASK-022..027 全部是本轮新增任务, CANCELLED 标记写法是本轮新决定, `phase-c-integrator` 委派是本轮新决定, `metadata.version_reference_surface` 的 breakdown/aria_side_points 结构也是本轮新写。

这个 100% 需要一个诚实的限定: 组 5 本轮是**整组重derive** (旧 7 条全 cancel, 新 6 条从零写), 不是在旧内容上打补丁, 所以「fix 引入」这个指标在满是新内容的场景下几乎必然趋近 100% —— 不能直接与 R1→R2 的「83%/62%」在同一把尺子上比较严重度。但即便打了这个折扣, 实质结论仍然成立且值得点名: **owner 裁定的「停止逐条补丁、按规律整组重做」策略, 目的是跳出边际产出转负的循环, 但从我审的组 5 子集看, 它没有跳出去 —— 委派未核实目标行为 (critical×2) 与断言枚举不完整 (major×1, 与它标榜修复的缺陷同形状) 在全新写的内容里原样复发了。** 重做换掉了文件的每一行字, 没换掉产生缺陷的认知习惯 (委派前不读目标源码 / 强调「先枚举」却枚举不全)。

## 输出

- verdict (frontmatter): FAIL
- vote: **REVISE** (2 个已知 critical 仍开放, 即便非本席新报, 客观仍在场; 加 1 major 新发现)
- 已知三条: 核实成立, 均系本轮新引入 (非 R1-fix 遗留)
- 新发现: 1 major (TASK-024 「先枚举后断言」对 aria 侧 3/9 文件结构性缺席, 其中 `aria/README.md` 全文件零处枚举) + 1 minor (TASK-025 artifact 指针 2/3 undercounted, `proposal.md:183` 遗漏)
- fix 引入占比: 6/6 (100%), 但需限定为「整组重derive 场景下的退化到近乎必然」, 核心信号是 owner 的重做策略未阻止同形状缺陷在全新内容中复发
- 报告路径: `/home/dev/Aria/.aria/audit-reports/post_planning-R3-1786193389568-linked-issue-normalization-backend-architect.md`
