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
timestamp: 2026-09-10T17:24:24.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [backend-architect]
---

# post_spec 单席审计报告 — backend-architect (Round 3)

被审对象: `/home/dev/Aria/openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (v3, R2 rework 后)。本席位透镜: 数据契约与实现可行性 (字段语义的向后兼容与消费方枚举 / 错误路径穷举 / 伪代码与真代码结构对齐)。本轮只审不改, 未触碰任何仓库文件。

**核验方式**: proposal 的自述一律不采信。行号基准 = aria `301641b` (v1.71.1) 的实读副本; 另实跑 `git -C aria diff --stat 301641b f314785 -- <触点>` 确认基线在当前 gitlink 上仍有效。语料数字 (62 / 6 / 170 / 160 / 碰撞三型) 与 Level 行可解析率均由本席独立 python 全枚举重算, 未沿用任何席位的数字。

## 审计结论

### Decisions

- [minor] implementation/§Why F2-F4 语料数字: 独立全枚举复算 —— 末段族 **62**、真 2-field legacy **6**、unattributed 全 8 checkpoint 口径 **170** / `{post_spec,post_planning}` 口径 **160**、前缀碰撞 1 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`)、后缀 0、中缀 0、archive 无重名 id, 与正文逐字一致 (证据: proposal.md:51-53,126; 本席实跑)
- [minor] architecture/基线冻结有效性: `git -C aria diff --stat 301641b f314785 -- <全部触点文件>` 输出为空, 全量 21 files 895+/63-, 与 :16 陈述一致 ⇒ 本文行号在当前 gitlink (f314785 = v1.73.0) 上继续有效 (证据: proposal.md:16; 本席实跑)
- [minor] architecture/§5 消费方枚举完整性: 全插件树对 `allow_incomplete_checkpoints` / `missing_checkpoint` / `Completeness Gate` **零代码消费方** (命中全在 CHANGELOG 与另一个同名「archive-completeness-gate」语境); 文件名 schema 消费方确为 `collectors/audit.py` 与 `aria-dashboard/references/parse-rules.md` 两处; `aria-orchestrator/.../extension.py:615,661` 对 `.aria/audit-reports/` 的命中是 `cron-tick-skip-*.log` 注释, 不落 `.md` 扫描面 (证据: proposal.md:238-239; 本席 grep)
- [minor] implementation/§1.2 规则 2+3 碰撞正确性: 逐例代入前缀 / 后缀 (`gate-scope` ⊂ `pre-merge-gate-scope`) / 中缀三型, 含末段族与 role 后缀族 —— 他人报告被排除、本 change 真报告不被误排除; 规则 3 写成「f 按规则 2 命中 c'」而非纯中缀比对, 恰好覆盖末段分支 (证据: proposal.md:114,116; 本席代入验算)
- [minor] testing/R2 缺陷落地核验: R2 的 C2 / M9 全部在正文落地 (非批注) —— 空集三格 + `no_prior_checkpoints`、Step 3 优先级链 + `enabled_by`、config 直读 + SC-21 相等性、`--base` 远程跟踪 ref + §3 补 `- base:`、S1 继承 `allow_dangling_change_ids`、SC-19(b) 换成真能翻转的变异体并补 (c) 格、stdout 键集 13→15 闭合 SC-10×SC-19 互斥 (证据: proposal.md:92,156,185,188,197,290,299)

### Issues

- [major] implementation/§1.4 stdout 契约 × SC-5/SC-15 的 audit trail 通道: 全文未定义 trail 的输出通道。:197 规定「stdout 恰一个 JSON」且顶层键集**逐字 15 项**、`results` 元组字段也是封闭集, 无任何消息字段; 而 SC-5 断言「stdout 含 `[INFO]` 与 `not_applicable`」、SC-15(3) 断言「stdout/trail 含 `[INFO]`」⇒ 与 SC-10「四种 verdict 下 stdout 均可 `json.loads` 且键集逐字 15 项」结构上不可能同绿 (与 R2 已修的 `13c973b9` 同型)。更坏的一支: 若实现为满足 SC-5 把 `[INFO]` 打进 stdout, :199 的消费方 fail-closed 条款 (「stdout 非 JSON ⇒ 按 fail 处置」) 会把**每次 not_applicable 运行判成 fail**。本 spec 自称镜像的先例把人读行放 stderr、stdout 只出 JSON (证据: proposal.md:197,199,285,295; sibling_spec_probe.py:148-151,684)
- [major] architecture/§1.4 格 B 人群论证 vs SC-20(2): §1.4:188 论证格 B 时把官方 `config-example.md:402-417` **场景 B** 列为「落进空纳入集」的采用方 (§5:242 与 待 owner 复议 #8:325 同口径), 但按本 spec 自己新定的 Step 3 优先级链, 场景 B (adaptive 且无 `checkpoints` 块) 对 Level 2/3 的 change 解析出**非空**纳入集 —— SC-20(2):300 正是这么断言的 (`checked_checkpoints` 非空且全部 `enabled_by == 'adaptive:level_3'`)。只有 `adaptive_rules.level_1="off"` 的 Level 1 才落格 B。同一份文档里两句互斥, 且错的那句正是请 owner 拍板 #8 时的人群依据 (证据: proposal.md:188,242,300,325; config-example.md:402-417; DEFAULTS.json audit.adaptive_rules)
- [major] implementation/§1.4 格 A-C 与 §1.1 S1-S4 的求值顺序 + SC-15 fixture: 两段判据谁先执行未定义。SC-15 的三格 fixture 只给 config, 未给 `--change-id` 也未给 diff ⇒ 按 :93/:95 会**先**落 S2→S4 `change_scope_unresolved` exit 2, 与期望的 `audit_not_enabled` / `pre_merge_not_enabled` / `pass` 直接冲突, 期望值随实现顺序红绿翻转。同一形态族 R2 只清扫了 SC-5(4)(5) 与 SC-16, SC-15 / SC-19 / SC-20 / SC-22 未补作用域声明。附带一格: 格 B/C 的 `resolved(pre_merge)` 在 adaptive 且 `pre_merge` 无显式值时需要 change 的 Level, 而 Level 依赖作用域解析 —— 循环依赖亦未定义 (证据: proposal.md:93,95,188,193,295)
- [major] implementation/§1.3 Level N 取法对真实语料: :156 写「读 `openspec/changes/{id}/proposal.md` **头部** Level 行」, 但「头部」未定义范围, 且对真实语料不成立 —— 本仓 153 个 change 目录中, **9 份 proposal 全文无可解析 Level 行** (如 `2026-06-10-handoff-frontmatter-enforcement`), 另 **6 份 Level 行落在第 15 行之后** (如 `2026-09-06-a1-entry-claim-duplicate-work-guard`, `2026-08-22-phase-c-integrator-ci-path-coverage`)。按只读头部的实现, 这 6 份会误落 `spec_level_undetermined` exit 2 (消费方 fail-closed ⇒ 硬阻合并); SC-20(3) 只测「全文无 Level 行」一格, 对「有但不在头部」零覆盖 (证据: proposal.md:156,300; 本席对 openspec/{changes,archive} 全枚举实跑)
- [major] architecture/§1.1 S1 `allow_dangling_change_ids` × §1.3 Level 取法: R2 两条 accepted 修法互撞。S1:92 让锚点缺失在该键为 true 时降为 `[WARN]` 并「按该 id 零报告继续评估」, 但同一轮新增的 Step 3 优先级链在 adaptive 档要读**该 id 的** `proposal.md` 取 Level —— 无锚点即无 proposal.md, 必然「解析不到」⇒ 仍 `spec_level_undetermined` exit 2。⇒ 迁移期逃生舱恰好对 adaptive 采用方 (官方场景 B/C, 也就是 `ca4cd11f` 修法要保护的那批) 失效, 只是换了个 `error_kind`; SC-7(c):287 的 fixture 走显式 checkpoints, 测不到这一格 (证据: proposal.md:92,156,287)
- [major] testing/SC-13 调用串机械护栏计数: SC-13:293 规定「调用串机械护栏 = 计数恰 2 (`grep -c 'completeness_gate.py'` 在 SKILL.md fenced bash 块与 execution-modes.md 各 1)」, 而 §2:210 计划在 SKILL.md `## 执行流程` 散文里写 `completeness_gate.py`、§4:224 计划在 `## 相关文档` 加 `completeness_gate.py` 契约指针 ⇒ 该 grep 至少 4 命中, 护栏与「命中行在 bash 块内」两条同时必红; 实施者只能删掉计划中的文档指针或改弱断言。先例的 SC-17 计的是带前缀的整条调用串, 不是裸文件名 —— 实测 `sibling_spec_probe.py` 在 execution-modes.md 3 处 / SKILL.md 1 处, 用裸名 grep 本就得不到 2 (证据: proposal.md:210,224,293; execution-modes.md:90,121,159; audit-engine/SKILL.md:124)
- [minor] implementation/§1.4 list 字段顺序契约: 只给 `checked_checkpoints` 钉了 `sorted()` 字典序 (且明写「使断言可逐字比对」), `matched` 与 `unattributed` 的顺序未定义, 而扫描面用的是 `iterdir()` (顺序随文件系统); SC-4:284 对 `unattributed` 断言字面 list 相等, 元素多于一个时会 flaky (证据: proposal.md:197,284)
- [minor] documentation/头部 :10 与 Tasks :273 对 :16 复核的分叉: 头部仍写 `git ls-tree HEAD aria` = `301641b` 与「Phase B 在 `301641b` 起分支」, Tasks 基线重取项同写 gitlink = `301641b`; 但 :16 的 2026-09-10 复核已认定 aria 到 `f314785` (v1.73.0)、版本目标顺延 v1.73.1, 实测主仓 gitlink 也确是 `f314785` ⇒ 照头部起分支等于从落后 21 个提交的点开分支再 bump v1.73.1, CHANGELOG / VERSION / plugin.json 会带着陈旧内容进合并 (证据: proposal.md:10,16,273; `git ls-tree HEAD aria` = f314785)
- [minor] implementation/§1.1 `--change-id` 与 `--no-spec` 并存语义: 两参数同时给出时契约未定义 —— S1 first-match 会静默吞掉 `--no-spec`, S3 的 `no_spec_contradicted` 矛盾检测随之失效 (调用方误声明 Level 1 时不再有任何机械反证); 无 SC 覆盖 (证据: proposal.md:88-95)

### Risks

- [minor] implementation/§1.3(b) 的 gitlink 子句可判定性: :83/:165 要求「diff 中出现 gitlink/submodule 条目时 (b) 不触发」, 但 §1.1:93 指定的取法是 `git diff --name-only --no-renames`, 该输出把 gitlink 变更显示为普通路径 (要判定需 `--raw` 的 160000 mode), 脚本无从识别。当前无行为后果 —— gitlink 路径必然不在 `openspec/changes/{id}/**` ∪ `.aria/audit-reports/**` 之下, 同格的路径集判据已先行否决; 但它是一条写进契约、无法机械核验、也无 SC 的条款 (证据: proposal.md:83,93,165)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 6 / Minor 4 (另 5 条 decision 不计入)。

rationale: 无 critical。R2 的两条 critical 与九条 major 逐条在正文落地且方向正确 (空集改判 pass、枚举源过优先级链、config 直读 + 相等性断言、`--base` 绑定、S1 豁免继承、SC-19(b) 反事实换新), 语料数字与消费方枚举经本席独立机械复算全部成立, 归属规则对三型碰撞可证明正确 —— 方案本体没有错误, 不构成 FAIL。但六条 major 都落在**同一类根因**: 一次 rework 改了 A 段却没有回灌到 B 段的下游断言 (trail 通道 × 15 键封闭契约; 格 B 人群论证 × SC-20; 空集判据 × 作用域解析顺序; S1 豁免 × Level 取法; SC-13 护栏 × §2/§4 落点), 以及一条新引入的机械判据 (Level 行) 未对真实语料值域验证。这些在 Phase B 无人值守下会以「SC 必红 / 期望值随实现翻转 / 合法采用方硬阻」的形态爆掉, 应在进入 Phase B 前闭合。本席位投 REVISE。

## 轮次记录

### Round 3

- Agents: backend-architect (本席位单报告; 五席结论合并由汇总席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 15 条 (decision 5 / issue 9 / risk 1); severity 计数 Critical 0 / Major 6 / Minor 4
- Vote: REVISE
