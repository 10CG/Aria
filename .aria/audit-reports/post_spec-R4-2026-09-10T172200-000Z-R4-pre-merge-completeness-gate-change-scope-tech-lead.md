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
timestamp: 2026-09-10T19:49:47.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead]
---

# post_spec Round 4 单席报告 — tech-lead (架构与范围透镜)

本席为 Round 4 新席位, 不继承 R1-R3 结论。全部断言均对真文件实读 / 实跑核验; 行号除 proposal 自身外, 一律以插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b`) 为准, 并对当前 gitlink `f314785` 复核过触点 diff 为空。

## 审计结论

### Decisions

- [minor] documentation/R3 的 3 Critical + 12 Major 落地复核: 抽验 12 处锚点全部落在判据本体而非批注 —— §1.0 求值总序 P0-P6、§1.3 四值优先级链 (2b/2c/2d + 级 3 `config_unreadable`)、§1.1 S3 三条核验 + `no_spec_unverifiable`、§1.4 stderr 通道、15 键与 9 项 `error_kind`、SC-13 分块计数、v1.73.1 三处对齐、unittest 测试风格、B.0 无人值守机械仲裁 (证据: proposal.md:89-103,111,169-176,237-238,270,308-315,328,347,371)
- [minor] architecture/ship 前提与同伴在飞面实测: `git ls-tree HEAD aria` = `f314785` (= v1.73.0 + 1 个 state-scanner 测试修复提交); `git -C aria diff --stat 301641b f314785 --` 对六个代码/规程触点文件输出为空; 旧 schema `{timestamp}` 残留实测恰 4 处且行号逐字命中; `ab-suite/version.yaml` 仍 `1.5.0` (目标 1.6.0 未被占); 并发轨 #195 的「待 owner 复议 6」今日确在 `:510`, 代码触点与本 spec 零交叠 (证据: aria/skills/phase-b-developer/SKILL.md:204,277 · phase-c-integrator/SKILL.md:157 · phase-a-planner/SKILL.md:267 · aria-plugin-benchmarks/ab-suite/version.yaml:1 · openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md:510)

### Issues

- [major] architecture/§1.4 格 B/格 C 分格 × adaptive 档 Level 1 (含 `--no-spec`): 代入实算 —— adaptive 档 Level 1 时 `resolved(pre_merge) = adaptive_rules.level_1 = "off"` ⇒ 纳入集空 ⇒ 格 B 的 `resolved(pre_merge) != "off"` 前置**不成立** ⇒ 落格 C `pre_merge_not_enabled` exit 2 + 消费方 fail-closed = 硬阻, 而 `allow_incomplete_checkpoints` / `allow_dangling_change_ids` 都不救; 但 `:226` 与 `:283` 把该人群列为格 B「仍 pass」, `:111` 又承诺 `--no-spec` 把全部 checkpoint 判 `not_applicable` (证据: proposal.md:111,226,233-234,283; config-loader/DEFAULTS.json `audit.adaptive_rules.level_1 = "off"`)
  - `:226` 的括注「Level 1 通常走 `--no-spec`/S3, 那条路在 **P2** 就把全部 checkpoint 判 `not_applicable`, 不到本格」与 §1.0 自己钉的总序冲突: 三态在 **P6**, 空集分格在 **P5**, S3 在 P2 只产出 `scope_source`。
  - 结果随采用方 config 翻转: 只要有任一 checkpoint 是 explicit 非 off (官方场景 C), 纳入集非空 ⇒ S3 的 `not_applicable` + pass 成立; 全 adaptive 推导 (场景 B) ⇒ 同一输入变 exit 2 硬阻。同一条 `--no-spec` 路径两种终局, 无 SC 覆盖 (SC-7 未钉 mode, 与 §1.0 末段「每份 fixture 必须显式钉 `audit.mode`」相撞)。
  - 与 R2 Critical `fdb30703`「合法采用方无逃生口硬阻」同结构, 一轮之后换个入口复现; 且 `待 owner 复议 #8` 的人群依据第三次偏移 (R2 场景 A/B → R3 移出场景 B → 本轮发现新补的第 3 类实际落格 C)。

- [major] architecture/§3 调用方接缝 — phase-c-integrator 步骤 3 的 pre_merge 解析语义未对齐: 门侧 Step 3 已被两轮 Critical 钉成优先级链 (`checkpoints` 显式 > `adaptive_rules` > off), 调用方守卫却仍是**对 config-loader 合并视图的字面键判断** —— `phase-c-integrator/SKILL.md:132` 逐字「检查 `audit.checkpoints.pre_merge` — "off" 则跳过」, 而 `config-loader/SKILL.md:28` 第 5 步「与 DEFAULTS.json 合并」会把未写的 `pre_merge` 填成 `"off"` (证据: proposal.md:220,257,287; phase-c-integrator/SKILL.md:131-132; config-loader/SKILL.md:24-28; DEFAULTS.json audit.checkpoints 八键全 "off")
  - 字面读法 (SOT 现状): 官方场景 B (`:402-417`) 与场景 C (`:419-440`) 的采用方 `pre_merge` 都是 DEFAULTS 填的 `"off"` ⇒ 步骤 3 早退 ⇒ **门根本不被调用** ⇒ §5 第 7 条声称的行为变更 (「`adaptive_rules` 推导的 checkpoint 首次进入校验面 ⇒ 这批采用方会新看到 missing」) 在生产路径不可达; SC-20(1)(2) 与 SC-15(5) 全是直调 fixture, 测不到这一层。
  - 链读法 (若实现者按 `config-example.md:276,280` 把调用方也改成优先级链): 上一条的 adaptive Level 1 硬阻立刻变生产可达。
  - 两个读法各击穿本 spec 的一条声称, 而 §1.4 `:220` 恰恰把「调用方守卫」当作格 A/格 C「生产不可达」的论证前提。§3 只在步骤 4/4.5 加参数与三态处置, Tasks 无任何一项对齐步骤 2/3 —— 修法留在门内, 接线口没动。

- [major] testing/SC-12 的归档门 liveness 断言恒绿 (F7 落点): 本 spec 目录只有 `proposal.md` (无 `tasks.md` / `detailed-tasks.yaml`), 本席实跑 `python3 …/lib/spec_complete.py --gate <本 spec 目录>` 得 `{"verdict":"pass","blocking_reasons":[],"unverified_claims":[],"d_payload":null}` —— 代码在 `spec_complete.py:1642` 是「两文件皆缺 (proposal-only) → designed 零评估早退」, 符号分类器根本不运行 ⇒ SC-12 的「归档门判 `completeness_gate.py` alive、无 dead-code block」**不可能红** (证据: proposal.md:56,346; spec_complete.py:924-930,1642)
  - F7 的规则本体正确 (`spec_complete.py:924-930` 确实只认 SKILL.md 里的真 bash 调用), 但它写的后果句「否则 D.2 判 dead-code」对**本 cycle**不成立; 真正守住「调用行落 fenced bash 块」的只有 SC-13 的分块 grep。
  - 处置建议二选一: (a) 把 SC-12 该子句改成可证伪形态 (对一个**带 tasks.md** 的合成 spec 目录跑 `--gate`, 断言含 `completeness_gate.py` 的 `[x]` 集成声称被判 alive; 反事实 = 调用行只写散文 ⇒ block); (b) 删该子句并把 F7 的落点明确改挂 SC-13。

- [minor] implementation/§1.4 格 B 新增的 `enabled_by` 前置条件: 「该**空集**的每一项 `enabled_by` 都是 `explicit` / `manual-default` / `adaptive:level_{N}` 之一」在空集上是全称真空恒真 (空集无项), 该守卫按字面实现零效力; 若按意图读成「每个判 `off` 的 checkpoint」, 则条件为假时空集三格**无覆盖分支** = 未定义行为, 与「按成因分三格」的穷举声称冲突 (证据: proposal.md:233; SC-15 :349 无该格; memory `feedback_universal_predicate_vacuous_truth_on_empty_set` / `feedback_predicate_tiers_need_total_partition_proof`)

- [minor] documentation/§1 调用块 (`:74-78`) 漏 `--anchor-base`: R3 为修 Critical `34507656` 新增的 `--anchor-base` 没有回灌到调用模板, 而 §3 (`:257`) 要求调用方传 `anchor_base`、Tasks (`:318`) 要求 argparse 实现它。该模板正是 Phase B 逐字写进 `audit-engine/SKILL.md` fenced bash 块与 `execution-modes.md` Step 4、并被 SC-13 计数的那一份 ⇒ 照抄即缺参数名 (证据: proposal.md:74-78,84,257,318)

- [minor] testing/SC-1 的输出通道残留: §1.4 (`:238`) 已钉「全部 `[OK]`/`[INFO]`/`[WARN]`/ERROR 走 stderr, stdout 恒且仅恒一个 JSON」并要求「全部 SC 里 stdout 含文案的断言一律改到 stderr」, SC-5 与 SC-15(3) 已改, SC-1 (`:335`) 仍写「stderr/stdout 文案含 `post_implementation@x`」—— 该串在 15 键 JSON 里不存在 (`checkpoint` 与 `change_id` 是两个字段), stdout 分支恒假 (证据: proposal.md:237-238,335)

### Risks

- [minor] architecture/Spec Level 2 声明 vs 实际范围: 本 spec 交付面 = 新增可执行脚本 + 重写闸门 Step 3-5 + 新增两个输入参数 + 15 键 stdout 契约 + 22 条 SC + 八条采用方行为变更 (含两条对现有配置的行为反转) + 10 个 owner 复议项, 版本级别推荐 MINOR; 对照 `standards/openspec/project.md:114-118` (Level 2 = Medium features 1-3 天 / Level 3 = Architecture changes, 输出含 `tasks.md`), 更贴 Level 3。附带效应正是上面 SC-12 那条: proposal-only 使归档门的 liveness 轴结构性不运行。**不建议 AI 自行改判**, 建议并入 `待 owner 复议` 一并裁 (证据: proposal.md 全文 396 行 / :306-329 Tasks / :331-356 SC / :280-288 §5 / :366-388 复议; standards/openspec/project.md:114-118)
- [minor] documentation/SKILL.md 与 execution-modes.md 两份「同字面」调用串无相等性断言: §1 要求两处同字面, SC-13 只做**分块计数**不做**两侧比对**; 本仓已有一条 enabled 机械闸 (`.aria/state-checks.yaml` `skill-md-sha-backlink-literal-sync`) 就是为同类「跨文件手工同步字面串」漂移而立, 其 description 自述 2026-09-06 实测已漂移 ⇒ 该风险在本仓有实证前科。低成本缓解: SC-13 加一条两侧切片逐字相等的断言 (证据: proposal.md:72,251,347; .aria/state-checks.yaml:46-62)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 3 / Minor 4 (另 2 条 decision 不计入缺陷计数)。

理由: R3 的 3 Critical + 12 Major 抽验全部落在判据本体, 事实底盘 (语料数字、SOT 行号、版本面、同伴在飞面) 本轮独立复核未发现新错, 方案对两层根因仍各有落点 —— 无一条构成「方案错误 / 破坏消费方 / SC 恒绿导致假绿」的 Critical。但三条 Major 都指向同一模式的延续: **修法只在门内闭合, 门外的接线口 (调用方步骤 3) 与门自身的分格穷举 (格 B/C × adaptive Level 1) 没有对账**, 以及**一条自称验证 F7 的 SC 在本 spec 形态下结构上不可能红**。这三条各自都有确定的落点与可证伪修法, 建议 REVISE 后进 Round 5。

## 轮次记录

### Round 4: Agents / Sibling probe 行 / Conclusions 数 / Vote

- Agents: tech-lead (本席; 五席之一, 本报告只载本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 9 条 (Decisions 2 / Issues 6 / Risks 1) — 缺陷计数 Critical 0 · Major 3 · Minor 4
- Vote: REVISE

**本席核验清单 (可复现)**:

```
python3 <cache>/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/pre-merge-completeness-gate-change-scope
    → {"complete": false, "verdict": "pass", "unverified_claims": [], "d_payload": null}   # 零符号分类
git ls-tree HEAD aria                                   → f314785 ;  git submodule status aria → v1.73.0-1-gf314785
git -C aria diff --stat 301641b f314785 -- <六触点文件>  → 空
grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/ → 恰 4 处 (204/277/157/267)
python3 -c "json.load(ab-suite/*.json)"                 → audit-engine 1.0.0/2 evals · phase-c-integrator 3 evals · pre-merge-gate type=workflow_skill_subextension/0 evals/8 fixtures
ab-suite/version.yaml:1                                 → "1.5.0"
DEFAULTS.json audit                                     → mode=adaptive · adaptive_rules{level_1:off, level_2:convergence, level_3:challenge} · checkpoints 八键全 off
config-loader/SKILL.md:28                               → "5. 与 DEFAULTS.json 合并 (用户值覆盖默认值)"
phase-c-integrator/SKILL.md:131,132                     → 步骤 2 检查 audit.enabled / 步骤 3 检查 audit.checkpoints.pre_merge == "off"
config-example.md:276,280,442 · :381-400 场景 A          → 逐字命中 proposal 所述
audit-engine/tests/test_sibling_spec_probe.py:303,319   → TestNoPytestImport / TestRunAllTestsDiscovery 两条守卫今仍在
sibling_spec_probe.py:147-151,684                       → log() 走 stderr / stdout 只 json.dumps
spec_complete.py:924-930,1642                           → SKILL.md bash 块才 alive / proposal-only 零评估早退
纯代入验算 (adaptive + Level 1 + --no-spec)              → 纳入集 [] · resolved(pre_merge)=('off','adaptive:level_1') · 落格 C exit 2
```
