---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T21:40:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead]
---

# post_spec R5 单席报告 — tech-lead (pre-merge-completeness-gate-change-scope)

席位透镜: 架构与范围 / 根因 vs 症状 / 候选取舍 / 消费方接缝 / 越界面 / ship 顺序与 gitlink。本席为新席位, 不继承上轮结论; 下列每条事实均本轮实读或实跑, proposal 自述一律不采信。

## 审计结论

### Decisions

- [minor] architecture/ship 顺序 · gitlink · 版本面: 实测 `git ls-tree HEAD aria` = `f314785`(v1.73.0-1), `git submodule status aria` 无 `+` 前缀, 最高 tag `v1.73.0` (`v1.71.2`/`v1.72.0` 未被占但已过号), `aria/VERSION` 与 `plugin.json` 均 `1.73.0`, `ab-suite/version.yaml` `1.5.0`, `audit-engine.json` version `1.0.0`/2 evals, `phase-c-integrator-pre-merge-gate.json` `type=workflow_skill_subextension`/无 `evals`/8 fixtures —— proposal `:16` 与 §4 的对应陈述**逐项命中**; 「gitlink 只许前进」的硬约束书写正确 (证据: proposal.md:16,326; `git ls-tree` / `git -C aria tag --list` 实跑)
- [minor] architecture/消费方接缝零破坏: 全插件树 `--include=*.py --include=*.json --include=*.yaml` 对 `allow_incomplete_checkpoints|missing_checkpoint` **零命中** (仅三份 `.md`: CHANGELOG / execution-modes / audit-engine SKILL); `collectors/audit.py:62-69` 逐字 `_CHECKPOINT_PREFIX = re.compile(r"^[^-]+-")` + 合成首连字符, 与 F2 的先例引述一致; `.aria/state-checks.yaml` 16 条 check 对 audit-engine / audit-reports 零命中 ⇒ §5「只读文件名, 不改 writer schema」成立 (证据: collectors/audit.py:62-69; proposal.md:331-334)
- [minor] architecture/越界面: `openspec/changes/` 下 8 个在飞目录; 同伴轨 `handoff-multibranch-subdir-path-fidelity` 仍在飞 (538 行, 「待 owner 复议 6」今日实读落 `:510`, 与 proposal §4 引述一致), 落点为 state-scanner collectors/scan/latest_md_writer 与 phase-d-closer, 与本 spec 触点零交叠; 共享面仅版本号与 `ab-suite/version.yaml`。本 spec 对 `phase-a-planner` / `phase-b-developer` 只做 1 行 `{timestamp}` 勘正, 未触 phase1_gate / claim_lifecycle / spec-drafter / AB 套件本体 (证据: handoff-multibranch-subdir-path-fidelity/proposal.md:510; proposal.md:326-329)
- [minor] architecture/根因覆盖与候选取舍: 两层根因各有对应修法 (匹配面 → §1.2 双侧/末段界定 + 对称有界包含排除; 输入面 → §3 pre_hook 五参数 + §2 输入表)。否决理由经实读成立: A 无法写 hermetic 红转绿; D 的 frontmatter 形态不统一 (837 份中 255 份无任一独立字段); C 需新 config 键而 F8 缺口实测存在 (`DEFAULTS.json` audit 键集无两个 `allow_*`) (证据: proposal.md:63-66; config-loader/DEFAULTS.json)
- [minor] documentation/R4 十四条 Major 的落地抽验: 抽验七条**全部落在判据本体而非批注** —— `955907f2` (格 B 第四合取项整条删除 + `:276` 新增分割证)、`f637d129` (`:274` 新增格 D)、`a657bf0a` (§1.0 新增 P2a)、`a00c52bb` (S2 改锚点面 + S4 文案)、`8acafe0a` (`:83-88` 占位来源表 + §2 五项)、`4cbe35ce` (SC-12 已删 liveness 子句、F7 后果句改挂 SC-13; 本席实跑 `spec_complete.py --gate` 得 `verdict=pass` 且零符号分类, 佐证删除正确)、`29c39e2c` (Tasks AB 拆三条命令 + 两条无 node id 缺口)。`7127ab68` / `aebd2f9f` 按 Rule #10 转 待 owner 复议 #11/#12, 未自行放宽放行面 (证据: proposal.md:56,274,276,83-88,415,324)

### Issues

- [major] architecture/§3 调用方接缝 · §4 同步表: 门与 C.2 之间有**两道**启用守卫, 本 spec 只处理调用方 `phase-c-integrator/SKILL.md:132`; audit-engine 自身入口 `execution-modes.md:9-10`「`audit.enabled == false` → 静默返回」/「checkpoint 未启用 → 静默返回」在 proposal 内**零提及** (grep「入口逻辑」「静默返回」各 0 命中), 不在 §4 同步表 (`:326` 只列 `:23-82` 含 `:15`, 而 `:15` 是「同句」引证不是改动目标)、无 Tasks、无 SC。⇒ (1) §5 第 7 条 (`:344`) 声称的行为变更生产可达性**仍未建立** —— 即便按 R4 的 `bb0e565f` 改了调用方步骤 3, 场景 B/C 的采用方仍会被 `:10` 的字面读法拦在门外; (2) §1.4 `:271`/`:273` 的「生产不可达 (调用方早退)」论证只点了一道守卫; (3) R4 为 `f637d129` 新增的**格 D** (`:274`) 是否可达取决于 `:10` 的两种合法读法 (字面合并视图键 vs 优先级链 + Level) —— 按后者读, audit-engine 已拿到 `change_id` 可自行解析 Level 并静默返回, 格 D 成死码; 按前者读格 D 可达。两读法无任何 SC 区分, SC-13 新增的两条调用方接缝 grep 只覆盖 `phase-c-integrator/SKILL.md` (证据: execution-modes.md:9-10,15; proposal.md:271,273,309,326,344,416)
- [major] architecture/§1 `--diff-repo-path` 缺省 = fail-open: R4 的 `a00c52bb` 把 S2/S3 都改取锚点面后, `:91` 自述该参数只剩 §1.3 (b) 一个消费点, 而 (b) 在跨仓被禁 ⇒ 它实际只当「跨仓标记」。缺省 = `--repo-path` 是 **fail-open**: 子模块 PR 漏传时 (b) 拿主仓 diff 判 Phase A-only —— 按顺序化 ship (子模块先 merge、gitlink 后 bump), 此刻主仓分支常只有 `openspec/changes/{id}/**` + `.aria/audit-reports/**` ⇒ **`post_implementation` 假绿**, 与被修 bug 同型, 且正落在本文自称的「pre_merge 主力场景」(`:82`)。`:91` 自认该危害 (「否则 (b) 会误取主仓 diff 判 Phase A-only = 假绿」) 却不设任何机械阻力; SC-17 (1)-(6) 与 SC-5(5) **全是「显式传」格**, 无一格覆盖漏传。与 `--base` 因 #137 教训被定为必填 (`:86`) 相比, 同类参数处置不对称。建议: pre_merge 下把 `diff_repo_path` 提为必填 (同仓显式等于 `repo_path`), 把静默假绿变成 argparse exit 2 (证据: proposal.md:82,86,91,408,420)
- [minor] architecture/§1.4 四格分割证: `:276` 的互斥与全覆盖证把 `resolved(pre_merge)` / `enabled_by(pre_merge)` 当**标量**三轴, 而 §1.3 `:190` 明写解析是 per (checkpoint, change_id)、混合 Level 多 change 下同一 checkpoint 可一纳入一 off。可构造: `mode=adaptive` + 四个非排除项显式 `off` + change A(Level 1)/B(Level 2) ⇒ 纳入集空且 `resolved(pre_merge)` 同时为 `off`(A) 与 `convergence`(B) ⇒ 落格 B 还是格 D **未定义** (两者均 pass, 差异仅 `[INFO]` 文案与 `no_prior_checkpoints` 语义留痕)。影响低但正是 memory `feedback_predicate_tiers_need_total_partition_proof` 要求补的那一维 (证据: proposal.md:190,276)
- [minor] documentation/基线冻结的行号有效范围: 头部 `:9`/`:16` 把行号有效性限定为「代码/规程六文件」+ `CHANGELOG.md`/`VERSION`/`plugin.json`/`README*.md`/`spec_complete.py` 的 carve-out, 而 §4 与 Tasks **以行号点名的编辑目标** `phase-a-planner/SKILL.md:267` 与 `phase-b-developer/SKILL.md:204,277` 两文件**不在任一集内**。本席实跑 `git -C aria diff --stat 301641b f314785 -- <八文件>` 输出为空、三行在两 SHA 上逐字同文 ⇒ 事实无误, 但声明面有缺口 (同伴轨 #195 R5 major `dbdd80e9` 是同型失效: 冻结面只覆盖代码落点而引用面更宽) (证据: proposal.md:9,16,326-329; `git -C aria show f314785:skills/phase-a-planner/SKILL.md | sed -n 267p` 实跑)
- [minor] testing/SC-11 活体 dogfood 的调用形态: `:414` 的唯一活体命令写 `--base master` (裸本地分支名), 与 §1 `:86` 自定的生产契约「必须传远程跟踪 ref」及 R-h (`:357`) 的假红论证直接冲突, 且不断言 R4 新增的 `[WARN] {base|anchor-base} ref 陈旧` 路径。本席实测本仓 `master == origin/master` (`0483c69`)、`aria` 亦对齐 (`f314785`) ⇒ 当下不触 WARN, 属潜伏不一致; 但该输出要「抄进 handoff」, 会成为错误的调用范例 (证据: proposal.md:86,357,414; `git rev-parse master origin/master` 实跑)

### Risks

- 本席未新增独立 risk 条目。上表 major 第 2 条在 Impact 中最贴近的既有条目是 R-e (`:361`), 但 R-e 只写「跨仓时禁用 (b) 通道 + SC-17」, 未覆盖「跨仓但参数漏传」这一格; 建议随 major 2 一并回灌 R-e。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **3** (另 5 条 decision 不计入)。

rationale: 按 `verdict-format.md §判定规则`, 0 Critical + ≥1 Major ⇒ PASS_WITH_WARNINGS; post_spec `blocking: false`, 本判定不阻断流程。本席**投 REVISE**: 两条 major 都不是措辞问题 —— 第一条使本 spec 中心声称 (「修复在生产路径可达」) 仍未建立, 且 R4 刚新增的格 D 的可达性随之未定义; 第二条在自称的主力场景里留了一个 fail-open 缺省, 其后果与被修 bug 同型且无任何 SC 覆盖。二者都可用一句契约 + 一条 SC 闭合, 成本低于风险。

本轮相对 R4 的观察 (供收敛判定参考): R4 的 14 条 Major 经抽验**全部落在判据本体**, 无一条以批注形式敷衍; 本席本轮的两条 Major **不是** R4 任一条的原样复发, 但仍属同一模式 —— 「R4 修法自身的下游未闭合」: `bb0e565f` 只对齐了一道守卫、`a00c52bb` 收窄参数用途后没有把缺省语义一并收紧。按 memory `feedback_convergence_needs_zero_rework_round`, 收敛需要一个「干净轮 + 零 rework 的下一轮」, 本轮尚未达到。

## 轮次记录

### Round 5

- Agents: tech-lead (本席; 五席之一, 本报告只覆盖本席透镜)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 10 (Critical 0 / Major 2 / Minor 3 / Decisions 5)
- Vote: REVISE

#### 本席的机械核验清单 (全部本轮实跑)

1. `git ls-tree HEAD aria` = `f314785…`; `git submodule status aria` = ` f314785… (v1.73.0-1-gf314785)` 无 `+`; `git rev-parse master origin/master` 主仓与 aria 均单值。
2. `git -C aria tag --list | tail`: 最高 `v1.73.0`; `v1.71.2` / `v1.72.0` 不存在。
3. `aria/VERSION` 与 `aria/.claude-plugin/plugin.json` 均 `1.73.0`; `ab-suite/version.yaml` `version: "1.5.0"`, `last_modified: 2026-09-05`。
4. `audit-engine.json`: `version 1.0.0`, `len(evals)=2`; `phase-c-integrator-pre-merge-gate.json`: `type=workflow_skill_subextension`, 无 `evals` 键, `len(fixtures)=8`。
5. `.aria/config.json` audit 块: `enabled=true`, `mode="convergence"`, `checkpoints` **7 键** (`post_spec`/`post_planning`=convergence, 其余 off, **无 `mid_post_spec`**), 无 `adaptive_rules`, 无两个 `allow_*` —— 与 proposal `:14`/F1 一致。
6. `execution-modes.md`: `:5` `## 入口逻辑`, `:9` `audit.enabled == false → 静默返回`, `:10` `checkpoint 未启用 → 静默返回`, `:15` 优先级链, `:32` 触发条件, `:54-61` Step 4 通配, `:63-65` Step 5。
7. `phase-c-integrator/SKILL.md`: `:131` 步骤 2 (`audit.enabled`), `:132` 步骤 3 (`audit.checkpoints.pre_merge — "off" 则跳过`), `:133-136` 步骤 4, `:137` 步骤 5, `:157` `pre_merge-{timestamp}.md` —— proposal 的四处行号引用全中。
8. 消费方 grep: 全插件树 `.py/.json/.yaml` 对 `allow_incomplete_checkpoints|missing_checkpoint` 零命中; `.md` 仅三份。
9. `collectors/audit.py`: `_AGGREGATE_SUFFIXES = ("-aggregated.md", "-aggregate.md")`, `_CHECKPOINT_PREFIX = re.compile(r"^[^-]+-")` (`:62`), `_strip_checkpoint_prefix` (`:65-69`)。
10. `.aria/state-checks.yaml`: 16 条 check, 对 `audit-engine|audit-reports|completeness` 零命中。
11. `git -C aria diff --stat 301641b f314785 --` 对八个触点文件 (六文件 + phase-a-planner + phase-b-developer) 输出为空; `phase-a-planner:267` / `phase-b-developer:204,277` 三行在两 SHA 逐字同文。
12. proposal 内 grep: 「入口逻辑」0 命中、「静默返回」0 命中、`execution-modes.md:15` 3 处 (均为引证)。
13. 同伴轨 `handoff-multibranch-subdir-path-fidelity/proposal.md` 538 行, 「待 owner 复议 6」在 `:510`, 版本候选 PATCH `v1.73.1` / MINOR `v1.74.0` (推荐 MINOR) —— 与本文 §4 引述一致。

#### 给 Phase B / 下一轮的最小闭合动作 (本席建议, 非裁决)

1. §4 同步表与 Tasks 补 `execution-modes.md` **入口逻辑** (`:9-10`) 这一触点, 并把「checkpoint 未启用」的解析语义与门侧/调用方钉成同一条优先级链 (三处一致); 否则 §1.4 `:271`/`:273` 的「生产不可达」论证与 §5 第 7 条须同批改写, 格 D 的存废也要随之定。
2. `--diff-repo-path` 在 pre_merge 下提为必填 (同仓显式等于 `--repo-path`), 并补一条 SC: 跨仓形态漏传 ⇒ argparse exit 2 (反事实 = 缺省 fail-open ⇒ (b) 误判 not_applicable ⇒ 红)。
3. `:276` 的分割证补一句多 change 口径 (建议: 空纳入集时 `resolved(pre_merge)` 取「作用域内任一 change 非 off 即视为非 off」并写死, 或明确该场景恒判格 B)。
4. `:16` 的行号有效范围把 `phase-a-planner/SKILL.md` 与 `phase-b-developer/SKILL.md` 补进已核验集 (本席已代跑, 结论为空 diff)。
5. SC-11 的 `--base` 改 `origin/master`, 并顺带断言不出 `[WARN] base ref 陈旧`; 或保留 `master` 但断言 WARN 出现 —— 二选一, 使活体证据与 §1 契约同向。
