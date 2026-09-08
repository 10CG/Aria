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
verdict: FAIL
timestamp: 2026-09-07T05:55:43.375Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [qa-engineer]
---

# post_spec R2 单席审计报告 — qa-engineer (pre-merge-completeness-gate-change-scope)

席位透镜: 可证伪性 (每条 SC 做反事实) · hermetic case 可构造性 · 既有测试与冻结语料影响 · 负向测试缺口 · 既有失败项处置。
本轮为**只审不改**; 全部数字均由本席独立复算 (冻结快照 `3f4b379` + 插件缓存 `1.71.1` 副本 = `301641b`), 未采信 proposal 自述。

---

## 审计结论

### Decisions

- [minor] testing/R1 五条 Critical 落地复核: 规则 2 末段形态 (`proposal.md:112`)、两个计数拆分 (`:121-124`)、(b) 换 Phase A-only 判据 (`:148`)、(c) 含内联 `## Tasks` (`:148,153`)、SC-2 形态族重写 (`:245`) **全部落在正文而非批注**, 无一条以「已知悉」方式敷衍 (证据: proposal.md:112,121-124,148,153,245)
- [minor] documentation/语料事实底盘独立复算全中: 冻结快照 780 顶层条目 = 778 `.md` + 2 目录; cp-prefixed 末段形态 **62**、`unattributed` **170**、真 2-field legacy **6**、原合并定义 **238**、`|C|` **152**、前缀碰撞 **1** 对 / 后缀 **0** / 中缀 **0**; 无 A.2 文件 change **52** 其中内联 Tasks **15** ⇒ (c) 仍触发 **37** —— 与 proposal 数字逐个相符 (证据: proposal.md:50,51,121-124,153 对 `git ls-tree 3f4b379 -- .aria/audit-reports/` 全枚举)
- [minor] testing/SC-12 既有测试基线实跑全绿 @ `301641b` (本地 gitlink 已对齐): audit-engine **104** OK / phase-c-integrator **148** OK / state-scanner **1575** OK, 三者 exit 0 ⇒ **无既有失败项需 carve-out**, SC-12 的「三者 0 failure」起点成立 (证据: proposal.md:256; 本席实跑三条命令)
- [minor] implementation/规则 3 对称有界包含谓词手工代入验证成立: 前缀 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`)、后缀 (`gate-scope` ⊂ `pre-merge-gate-scope`)、中缀 (`gate`) 三型均正确排除, 且不误伤真归属 (`post_spec-R1-gate-scope-tech-lead.md` 对 `gate-scope` 仍命中) ⇒ SC-3 三型 case 与其反事实设计成立 (证据: proposal.md:114,246)
- [minor] documentation/§1.2b 边界事实三条全中: 冻结快照内子目录确为 `pr19-submodule-scan/` 与 `wf-r1fix/`; `*-audit-trail.md` 恰 **5** 份; `sibling-spec-probe` 按逐字规则 2 在全语料命中 **0** 份 (证据: proposal.md:134,135,262)
- [minor] testing/Rule #6 并集执行成立且不构成豁免: SOT 附加约束 (`skill-benchmark-exemption.md:33`) 要求「指令流程变动 ⇒ 一律第二行」, 而并集已含第二行的「照跑」; `ab-suite/phase-c-integrator.json` (3 evals) 与 `phase-c-integrator-pre-merge-gate.json` 实存并已入照跑面 ⇒ 档位裁决 (待 owner 复议 #5) 不改变 Phase B 动作集 (证据: proposal.md:12,264-270)
- [minor] documentation/SOT 行号与 §5 消费方面复核: `phase-c-integrator/SKILL.md:136` = `context: PR diff`、`:137` = 「5. 处理 verdict」、`:157` 旧 schema、`:252` 执行上下文契约、`:265` surface 义务; `execution-modes.md:44/:82` 两种豁免字面; `spec_complete.py:924` liveness; 全仓 `{timestamp}` 残留恰 **4** 处 —— R1 勘正方向正确, code-reviewer 的 `9a245f24`「无一漂移」不成立 (证据: proposal.md:42,97,54,194)

### Issues

- [critical] implementation/§1.4 空集短路 / pre_merge-only 采用方: 空集短路把「`audit.enabled=true` 且 `pre_merge != off` 但其余 checkpoint 全 off」也判 `error` exit 2 —— Step 3 明写排除 pre_merge 自身, 该配置的 `checked_checkpoints` 结构上恒空; 叠加消费方 fail-closed 义务 (exit≠0 ⇒ 按 fail 拒绝执行 pre_merge 审计) ⇒ 这类采用方**永久无法再跑 pre_merge 审计**, 而改前该配置是正常 PASS。§1.1 的豁免面按字面只覆盖 S4 与 missing, `allow_incomplete_checkpoints` 不救; ERROR 文案「audit 未启用或全 off」对该采用方是假陈述; 引用的先例 `audit-engine/SKILL.md:410` 恰恰相反 —— 空集是 `pass-through (不降级)` 走标准审计, 不是中止。旧配置映射按 `agent_team_audit_points` 逐项生效 (`config-loader/SKILL.md:323-329`), 故 `points: ["pre_merge"]` 的历史采用方直接命中。SC-15 的三个 fixture (`{}` / 无 audit 块 / 文件缺失) 全是「audit 根本没开」, 对该格零覆盖 (证据: proposal.md:163 / :95 / :209 / :258; execution-modes.md:49; audit-engine/SKILL.md:410)
- [major] testing/SC-19(a) 与 SC-10 stdout 键集冲突: SC-19(a) 断言 stdout 含 `scanned_dir_depth: 1` (§1.2b 亦写「在 stdout 契约里输出」), 但 §1.4 的顶层键集「**逐字**」清单 13 键不含 `scanned_dir_depth`, 而 SC-10 断言「顶层键集逐字 = 1.4 列表」⇒ 实现加了键 SC-10 红、不加 SC-19 红, **两条 SC 结构上不可能同时绿**。成因是 2026-09-07 追加 §1.2b 时未回改 §1.4 与 SC-10 (证据: proposal.md:134,164,253,262)
- [major] testing/SC-19(b) 反事实不成立: 所写反事实「把规则 1 的 `startswith(f"{checkpoint}-")` 去掉 ⇒ (b) 判 present ⇒ 红」实测为假 —— fixture 文件 `<change_id>-audit-trail.md` 的 change_id 位于**串首**, 左侧无连字符, 规则 2 的两个分支 (`-{id}-` 子串 / stem 以 `-{id}` 结尾) **都不命中**, 去掉规则 1 该断言仍绿。本仓真实同族样本 `sibling-spec-probe-audit-trail.md` 对 id `sibling-spec-probe` 实测规则 2 零命中, 可直接反证。⇒ SC-19(b) 号称锁的「规则 1 前缀约束」这条不变量**无守卫**; 其仍有效的部分只有「三桶都不收」(需换一个真能翻转的变异体, 如把 `unattributed` 定义里的 checkpoint 前缀条件去掉) (证据: proposal.md:262,135; 本仓 `.aria/audit-reports/sibling-spec-probe-audit-trail.md`)
- [major] architecture/§1.3(b) not_applicable 判据纳入 `openspec/archive/**`: 「全部变更文件路径都在 `openspec/changes/**` ∪ `openspec/archive/**` 之下 ⇒ **B.2 实现工序整个未发生**」对 **D.2 归档-only PR 为假** —— 本仓 `62de051` 即纯 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/{proposal.md,tasks.md,detailed-tasks.yaml}` 三文件提交, 而该 change 是 Level 3 已 ship, 实现工序确已发生。§3 规定 pre_hook 显式传 `change_id`, 故这类 PR 走 S1 且锚点在 `archive/*-{id}/` 命中, (b) 会正常触发并发 `phase-a-only-no-implementation` 免检票。三态 first-match 下 `present` 优先 ⇒ (b) **唯一被触发的时刻正是「post_implementation 报告确实缺失」= 门该拦的那一次**, 与 R1 Critical `8c7972ce` 的失效形状同型 (只是入口更窄), 也与 knowledge-manager 在 待 owner 复议 #7 的论证同向。SC-5 的五条反事实 (`src/a.py` / `.md` / `docs/` / 空 diff / 跨仓) 无一覆盖归档-only 形态 (证据: proposal.md:148,248,283; `git show --name-only 62de051`)
- [major] implementation/§1.4「config 一律经 config-loader」不可机械执行: config-loader 实读只有 `SKILL.md` + `DEFAULTS.json` + `config-example.md`, **零 `.py`**; 全 aria skill 树 `grep -rln agent_team_audit --include=*.py` **零命中** ⇒ stdlib-only 的 `completeness_gate.py` 无从「经 config-loader 读取」, 只能内联复制两样东西: (1) `DEFAULTS.json` 的 audit 缺省集 (8 个 checkpoint 全 `off` + `enabled:false`), (2) `config-loader/SKILL.md:311-331` 的旧配置兼容映射散文。proposal 既未规定 `DEFAULTS.json` 的路径解析 (调用行只传 `--repo-path/--diff-repo-path/--base/--change-id/--no-spec`), 也未留「脚本缺省 == DEFAULTS.json」的相等性 SC —— 这正是 R1 `013d0274` 那条 finding 的**更大形态**, 而 rework 以「`scope_skip_paths` 零消费」为由宣告其「自然消解」。同仓既有先例反向: `state-scanner/scripts/collectors/multi_remote.py:107-113` 明写 `_load_config` never reads DEFAULTS.json at runtime, DEFAULTS.json 是 adopter-facing 文档、Python 常量才是运行时缺省 (证据: proposal.md:82,159,227,258; config-loader 目录实读; multi_remote.py:107-113)
- [minor] implementation/`[WARN] unattributed reports` 文案双字面且与作用域矛盾: §1.2 计数表写 `[WARN] unattributed reports: …`, §1.4 audit trail 写 `[WARN] unattributed reports ({cp}): …`; 同段又定义 `unattributed_count`/`unattributed` 是**全局单值** (统计面 = 纳入集并集) ⇒ 多 checkpoint 下 `{cp}` 取哪个、是否逐 checkpoint 重复输出全未定义。与 R1 已处置的 `92aaa082` (豁免文案第三种拼法) 同型, 且 SC-13 未给这行加逐字 grep (证据: proposal.md:124,165,169,261)
- [minor] documentation/SC-11 的 `unattributed` 引用数与自定契约口径不符: SC-11 括注「本仓真实语料实测 **170** 份」是**全 checkpoint** 口径; 按 §1.4 定义只统计**纳入校验的 checkpoint** 前缀之并集, 而本仓 `.aria/config.json` 实读 `checked = [post_planning, post_spec]`, 冻结快照上实测为 **160**。断言本体是 `> 0` 不会红, 但同一份 spec 内两个口径混用会让 Phase B 误以为期望值可写死 (证据: proposal.md:165,254; `.aria/config.json` audit 块)
- [minor] documentation/`ab-suite/version.yaml` 现值已非 1.4.0: 头部 Rule #6 行与 §4 表两处写「现值实测 **1.4.0**」「1.4.0 → **1.5.0**」, 实读该文件 `version: "1.5.0"` —— 同伴轨 `a1-entry-claim-duplicate-work-guard` 已完成 bump。§4 同格已写「撞号则顺延为 1.6.0」的并发预案, 后果被兜住, 但两处「实测」值已失真, 按表面值执行会覆写同伴 changelog 条目 (证据: proposal.md:12,198; ab-suite/version.yaml:1)
- [minor] testing/SC-16 与 SC-5 的作用域来源未声明: SC-16 的 fixture 只给 `diff 含 src/a.py` + 期望 `verdict=pass`, SC-5 case (4) 给「diff 为空」+ 期望 `missing`, case (5) 给跨仓 —— 三者 diff 都不触 `openspec/changes/**` 且未写 `--change-id`, 按 §1.1 的 S2→S4 应先得 `change_scope_unresolved` exit 2, 与期望直接冲突 (与 R1 已修的 SC-1 锚点缺失**同型**, 属同一形态族的漏清扫)。另 SC-5 标题写「**四条**反事实」而正文列 (1)~(5) **五条** (证据: proposal.md:93,248,259)
- [minor] documentation/两处 SOT 行号偏移 + 一处 SC 追溯缺口: References 把 `skill-benchmark-exemption.md` 的「附加约束」记为 `:35` (实为 `:33`; `:35` 是「## 3. 第三行不是逃生舱」标题); §1.3(c) 称「`standards/openspec/project.md:118` 规定 Level 2 输出 = proposal.md」而 `:118` 是 **Level 3** 行 (Level 2 在 `:117`), 论证方向不受影响但引用错格。另 Tasks 的 TDD RED 项只列 `SC-1~SC-10 + SC-15~SC-17`, **SC-18 无任何任务承接** (SC-19 由「枚举范围两条边界落地」项承接) (证据: proposal.md:153,226,288; skill-benchmark-exemption.md:33,35; project.md:117,118)

### Risks

- [minor] testing/B.0 `corpus-freeze.md` 人工标注的独立性: SC-2 的期望值取自 B.0 的「**独立人工标注**真实归属」, 但 Phase B 是无人值守, 标注者与谓词实现者是同一执行体, 共享同一套「文件名里哪段是 change_id」的心智模型 ⇒ R1 Critical `3170df8a` 钉死的自指恒绿会以更软的形态回归 (标注跟着规则走, 而不是规则跟着事实走)。可执行的降险: 标注列改由**与文件名无关的机械源**交叉 —— 报告 frontmatter 的 `context:` / `spec_id:` 字段 (本仓 78 份有), 或写盘时刻仓内活跃 change 目录的 git 历史 —— 名匹配只作为第二列, 两列不一致的条目单独列出供人裁 (证据: proposal.md:224,245; 候选方案 D 行 `:64`)

---

## Verdict

**FAIL** — Critical **1** / Major **4** / Minor **6** (缺陷类 = issue + risk: 10 issue + 1 risk; 另有 7 条 decision 不计入)。

rationale: R1 的五条 Critical 本席逐条复核**确已在正文落地**, 事实底盘与既有测试基线独立复算全中 (见 Decisions 七条), 方案骨架无需推翻。本轮缺陷集中在**R1 修复动作自身引入的新面**, 三类:

1. **修「假绿」时新造了一处假红且无逃生口** (Critical): 为堵「零证据判绿」加的空集短路, 把 Step 3 结构上必然为空的 `pre_merge`-only 合法配置也判成 exit 2, 而 fail-closed 义务把它变成永久阻断; 它引用的 `SKILL.md:410` 先例恰恰规定空集要 pass-through。这条**破坏消费方**且零 SC 覆盖, 按 severity 判据落 critical。
2. **2026-09-07 追加的 §1.2b 没有回改上游契约** (Major 2 条): SC-19(a) 要求的 `scanned_dir_depth` 与 §1.4 的「逐字」键集 + SC-10 互斥, 两条 SC 不可能同时绿; SC-19(b) 的反事实经代入实测为假 (id 在串首无左侧连字符, 去掉规则 1 断言仍绿), 它号称锁的不变量实际无守卫。这两条正是本席透镜要抓的「反事实没跑过」。
3. **两处 R1 修复的残余口子** (Major 2 条): (b) 判据把 `openspec/archive/**` 一并纳入, 使 D.2 归档-only PR (本仓 `62de051` 即此形态) 拿到「实现工序整个未发生」的免检票, 与 R1 Critical `8c7972ce` 同型只是入口更窄; 「config 经 config-loader」在 config-loader 零 `.py` 的实况下不可机械执行, 把 `013d0274` 消掉的第二副本以更大规模重新引入且仍无相等性 SC。

Minor 6 条 (含 1 risk) 属随稿修订面: 两处 WARN 文案与作用域自相矛盾、两处计数口径/实测值失真、SC-16 与 SC-5 复现了 SC-1 已修过的「作用域未声明」形态族、两处行号偏移与 SC-18 无任务承接、B.0 标注独立性。

按 `verdict-format.md:6-8`, ≥1 Critical ⇒ **FAIL**; post_spec `blocking: false` 故不硬阻断流程, 但按 Rule #10 该判定不得由 AI 自行降格 —— Critical 1 与 Major 4 的处置须进 Phase B rework, 其中 (b) 是否保留 `archive/**` 这一格与 待 owner 复议 #7 同面, 建议合并裁决。

计算依据:
- Critical issues: 1
- Major issues: 4
- Minor: 6 (5 issue + 1 risk)
- Decisions (不计入): 7

---

## 轮次记录

### Round 2

- Agents: qa-engineer (本报告为五席之一的单席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 18 (Critical 1 / Major 4 / Minor 6 / Decisions 7)
- Delta vs 上轮: R1 的 C5/M9/m10 中, 5 条 Critical 与 9 条 Major 本席复核**均已在正文落地**且未见敷衍; 本轮 5 条 critical/major 全部是 **R1 修复动作新引入或残留**的面 (空集短路 / §1.2b 追加 / (b) 判据范围 / config-loader 可执行性), 无一条是 R1 结论的重复提出
- Vote 票型: REVISE (本席 Critical 1 ⇒ 单席 verdict FAIL)
- 实跑证据: `git ls-tree 3f4b379 -- .aria/audit-reports/` 全枚举 (780 条目 / 778 `.md` / 2 子目录) · 152 个 change id 的三型碰撞全枚举 · 三条既有测试腿 (104 / 148 / 1575, 全 OK) · `config-loader/` 目录与全树 `--include=*.py` grep · `git show --name-only 62de051`
