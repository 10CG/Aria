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
verdict: FAIL
timestamp: 2026-09-10T17:49:33.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [qa-engineer]
---

# post_spec R3 审计报告 — pre-merge-completeness-gate-change-scope (席位 qa-engineer)

> 席位透镜: SC 可证伪性 (逐条反事实) · hermetic fixture 可构造性 · 既有测试与冻结语料受影响面 · 缺失的负向测试 · 既有失败项处置。
> 本轮只审不改, 未编辑仓库任何文件; 所有断言均对 `301641b`/`f314785` 的实读副本与本仓语料实跑核验, 探针脚本落 scratchpad。

## 审计结论

### Decisions

- [minor] testing/SC-12 既有测试基线: 三套件实跑全绿 — `aria/skills/audit-engine/tests` 104 tests OK, `phase-c-integrator/tests` 148 OK, `state-scanner/tests` 1593 OK (0 failure) ⇒ **无既有失败项需处置**, SC-12 的三命令口径可原样沿用 (证据: 实跑 `python3 -m unittest discover`, proposal.md:292)
- [minor] testing/反事实实证: hermetic 实测 `git diff --name-only` 对 `git mv` 默认只输出目的侧路径、加 `--no-renames` 输出两侧 ⇒ SC-7(a) 反事实真翻转; SC-19(b) 的 R2 新反事实 (去掉 `unattributed` 的 `startswith` 条件 ⇒ 0→1) 与 SC-19(c) 亦真翻转, R2 `16935cfe` 的修法成立 (证据: proposal.md:287,299 + scratchpad `r3_hermetic.sh`)
- [minor] architecture/机械复核: 碰撞枚举在 `3f4b379`/`813e82c`/HEAD 三快照均为前缀 1 对 / 后缀 0 / 中缀 0 (F3 成立); 「三样 A.2 产物全无」的 change 实测 **37** 个 (§1.3(c) 成立); `git diff --stat 301641b f314785` 对全部触点文件为空 ⇒ 行号在当前 gitlink 上仍有效 (证据: proposal.md:53,163,16)
- [minor] testing/SC-2 选样面: 「同时具 F-a 与 F-b 族」硬约束**可满足但极薄** —— 全语料仅 4 个 id 符合 (`state-scanner-mechanical` 6/8 · `state-scanner-inter-cycle-surfacing` 2/3 · `secret-guard-per-segment-evaluation` 2/37 · `linked-issue-normalization` 1/29), 其中只有 1 个两族各 ≥3 (证据: proposal.md:282 + scratchpad `r3_corpus.py`)
- [minor] documentation/R2 落地复核: R2 的 C2/M9 逐条在正文落地 (非批注) —— `fdb30703`→§1.4 三格 (:188-196)、`ca4cd11f`→§1.3 优先级链 (:143-155)、`13c973b9`→15 键 (实数逐字 15 项)、`84d49ad0`→§1.4 直读+SC-21、`4f360230`→SC-14(a)+复议 #9、`31f29cf3`→version.yaml 1.5.0 (现值实测仍为 1.5.0, 未再撞号)、`eb21d182`→§1/§3/SC-22、`b9e07647`→(b) 两处收窄+复议 #7、`5a57d0e0`→S1 继承+SC-7(c)、`2bf48619`→§4 四句+SC-13 两条 grep。**但三条修法之间未互相对账**, 见下方 Issues 的 C-1 / M-1 / M-3

### Issues

- [critical] architecture/§1.3 Step 3 枚举链 + §1.4 格 B: 枚举链只处理 `mode=="adaptive"` (proposal.md:152-154), 而同一份 SOT 把 `convergence`/`challenge` 定义为「**所有检查点强制使用该模式**」。采用方写 `{"audit":{"enabled":true,"mode":"convergence"}}` 而不写 `checkpoints` 块 ⇒ 八键全落第 3 级 `off` ⇒ 纳入集空 ⇒ 新增的格 B 判 `verdict=pass` + `[INFO] … 依 audit.checkpoints/adaptive_rules 的配置放行 (Rule #10 白名单第一类)` —— owner 明明把所有 checkpoint 打开了, 门却盖章说「配置显式关闭, 非零证据判绿」。这与被修 bug 同型 (零相关证据判绿), 且 SC-15(3) 的格 B fixture 用 `mode:'manual'`、SC-20 只覆盖 adaptive ⇒ **没有任何 SC 会红**。本仓 `.aria/config.json` 自身即 `mode="convergence"`, 证明该 mode 值在真实使用 (证据: proposal.md:152-154,188,193 · config-loader/config-example.md:276-278 · /home/dev/Aria/.aria/config.json)
- [major] testing/SC fixture 前提 (SC-1/3/4/5/6/7/8/9/16/17/19/22): R2 引入枚举链后, 脚本内联缺省 `mode="adaptive"` + `adaptive_rules.level_2="convergence"` 使「config 里没写的 checkpoint」由 off 变为**启用** (`config-example.md:442` 逐字:「其余检查点按 adaptive_rules 推导」)。后果两条: (1) SC-8 期望 `checked_checkpoints == ['post_planning','post_spec']` 与其「本 fixture 不含 `post_brainstorm` 键 ⇒ 两个分支都不改 SC-8」的注**同时失效** —— 缺该键现在等于「按 level_2 启用」; (2) 其余 fixture 未钉 `audit.mode` 或 proposal 头部 Level 行者, 会在 Level 解析处落 `spec_level_undetermined` exit 2, 与各自期望的 exit 0/1 冲突。只有 SC-20 自己钉了 Level (证据: proposal.md:288,153,183,300 · DEFAULTS.json `audit.adaptive_rules` · config-example.md:442)
- [major] documentation/SC-13 调用串计数 vs §2/§4: SC-13 要求 `grep -c 'completeness_gate.py'` **计数恰 2**, 但 §2 让 `audit-engine/SKILL.md` 的 `## 执行流程` 散文写「经 `completeness_gate.py` 机械执行」, §4 又要 `:427-433` 相关文档「加 `completeness_gate.py` 契约指针」—— 两处都落在 SKILL.md 的 fenced bash 块之外 ⇒ 实现 §2/§4 即令 SC-13 必红。所引先例并不支持裸文件名计数: 实测 `sibling_spec_probe.py` 在 `execution-modes.md` **3** 处 / `SKILL.md` **1** 处, `:152` 锁的是更长的字面串 (「每轮入口: 竞品 spec 探针 —— python3 …」), 且该先例的相关文档条目**刻意不写脚本名** (证据: proposal.md:293,210,224 · execution-modes.md:152 · 实测 grep -c)
- [major] architecture/§1.4 格 B 论证 + 待 owner 复议 #8: §1.4 把官方场景 B (`config-example.md:402-417`) 列为「落到空纳入集这一格的采用方」, 但按本文自己的枚举链与 SC-20(2), 场景 B (adaptive 无 checkpoints 块) 在 Level 2/3 下纳入集**非空** (由 `adaptive_rules` 推导), 只有 Level 1 才空 —— 而 Level 1 走 `--no-spec`/S3, 本就无可校验对象。⇒ 复议 #8 与 §5 行为变更第 3 条据以论证的「合法采用方人群」被高估, owner 在被高估的证据面上拍板 (证据: proposal.md:188,242,300,317)
- [major] implementation/§1 `--base` 绑定 + Impact R-b + SC-22(1) 论证: 「裸本地分支名陈旧 ⇒ `merge-base` 偏移 ⇒ diff **偏小** ⇒ S3 交叉核验假通过 ⇒ 假绿」方向错。hermetic 实测 (本地 `master` 停在 c1、`origin/master` 前进到 c3、feature 从 c3 开出): 陈旧 base ⇒ merge-base 更旧 ⇒ diff 是**超集** (`base.txt` + 他人 `openspec/changes/other/proposal.md` + `src.py` 3 文件, 对远程跟踪 ref 只有 1 文件)。真实后果是**反向**的: S2 把他人 change 目录卷进作用域 ⇒ 那些 id 零自有报告 ⇒ `missing` 假红阻断合并, `--no-spec` 下则误报 `no_spec_contradicted` exit 2。SC-22(1) 的断言本身 (打不打 WARN) 仍可证伪, 但守的是一个不存在的失效方向, 真实方向零覆盖 (证据: proposal.md:85,253,302 · scratchpad `r3_base.sh` 实跑)
- [major] testing/§1.1 S3 交叉核验的空集真空成立: S3 的机械交叉核验只问「diff 不触 `openspec/changes/**`」, 空 diff 上**真空成立** (实测: `--base` 指向已含 HEAD 的 ref ⇒ 0 行) ⇒ 全部纳入 checkpoint 记 `not_applicable/level1-no-spec` + `verdict=pass` = 零证据全免检。同一文档的 `missing` 行已按 `audit-engine/SKILL.md:410`「防 vacuous-true 空集误触」显式不放行, S3 却没有对称短路; SC-5 case(4) 的空 diff 只覆盖 `--change-id` 路径, `--no-spec` + 空 diff 无任何 SC (证据: proposal.md:94,166,285,287 · audit-engine/SKILL.md:410 · scratchpad `r3_base.sh`)
- [major] testing/Tasks B.0 双列标注与 SC-2 期望值来源: B.0 要求对**全量**语料双列交叉、两列不一致者「单列成表**供人裁**, 不得由实现者自行取舍」, 同一段却声明「Phase B 是无人值守」—— 无仲裁者, 也没写不一致时是阻断还是降级。实测量级使这不是边角: 825 份报告中 570 份有 `context:`/`spec_id:` (文中只写「78 份有」, 低估了独立源), 255 份两者皆无; 60 份随机抽样两列不一致 **14 份 (23%)**、无独立源 6 份 (10%); SC-2 硬约束下唯一两族各 ≥3 的样本 id `state-scanner-mechanical` 的 15 份报告**全部无 frontmatter**, 其 git 历史列给出的是写盘时刻的目录名 `state-scanner-mechanical-enforcement` (归档后改名为 `2026-04-25-state-scanner-mechanical`) ⇒ 15/15 两列不一致。R2 用来堵「自指恒绿」的这条修法, 在真实语料上落不了地 (证据: proposal.md:262,282 · scratchpad `r3_cross.py` / `r3_ids.py` 实跑)
- [major] documentation/§4 · Tasks · 复议 #4 的版本目标: 头部 2026-09-10 复核行已把 PATCH 候选顺延为 **v1.73.1**, 但正文三处仍逐字 **v1.71.2** (§4 CHANGELOG 行 / Tasks 版本项 / 复议 #4), 而 `aria/.claude-plugin/plugin.json` 实测已是 **1.73.0** ⇒ 照正文执行是版本回退, 且 `plugin-version-arch-docs-match` 等机械兜底会转红。复议 #4 的整段并发面论证 (「#195 同抢 v1.71.2, 其推荐改走 v1.72.0 但未拍板 ⇒ v1.71.2 未出局」) 亦已作废: v1.72.x 与 v1.73.0 都已发布 (证据: proposal.md:16 vs 229,274,317 · aria/.claude-plugin/plugin.json)
- [minor] testing/SC-3 · SC-4 · SC-9 fixture 作用域输入: R2 只给 SC-16 与 SC-5(4)(5) 补了 `--change-id` 与锚点, 同族的 SC-3/SC-4/SC-9 仍未声明作用域来源 —— 按 §1.1 它们会先落 S4 `change_scope_unresolved` exit 2, 与各自的计数 / 排除 / 豁免断言冲突 (证据: proposal.md:283,284,289,97)
- [minor] testing/§1.2 `unattributed` 截断到 20 无 SC: §1.2 把「按字典序前 20 个 + 其余 K 份」论证为 R-a 显影缓解的量级需要 (本仓 170 份), 但没有任何 SC 断言该截断与那句逐字文案 (SC-11 只断言 `count > 0`) ⇒ 实现一次倒 170 行、或干脆不列名单, 都不会红 (证据: proposal.md:126,204,291)

### Risks

- [minor] architecture/§1.4 格 C 与 SC-11 活体口径: 格 C 的「`audit.enabled=true` 但 `resolved(pre_merge)=="off"` ⇒ error exit 2 (调用方步骤 3 本该早退)」写成前置条件语气, 但按小节标题只作用于**纳入集为空**时。本仓实测 `pre_merge="off"` 且纳入集非空 (`post_spec`/`post_planning` = convergence), SC-11 的活体 dogfood 必须依赖「只在空集时判 error」这一读法才跑得通 —— 两种读法只由一个手动 dogfood 步骤区分, 实现者取无条件读法则 SC-11 当场红 (证据: proposal.md:194,291 · /home/dev/Aria/.aria/config.json)

## Verdict

**FAIL** — Critical 1 / Major 7 / Minor 3 (缺陷类 = issue + risk; 另 5 条 decision 不计入)。

判据: 按 `verdict-format.md` 的规则, ≥1 Critical ⇒ FAIL; post_spec 的阻塞行为是 `blocking: false`, 故本 FAIL **不硬阻断**流程, 但按 Rule #10 不得由 AI 自行降格。

一句话归因: **v3 的三条 R2 修法各自成立, 彼此没有对账**。枚举链 (`ca4cd11f` 修法) 只覆盖 4 个 mode 值里的 1 个, 剩下两个把空纳入集送进新加的格 B (`fdb30703` 修法) 变成盖章放行 = C-1; 同一条枚举链改变了「config 没写的 key」的语义, 却没有回扫既有 SC 的 fixture 前提 = M-1; 新加的落点句 (`2bf48619` 修法) 与 SC-13 的计数护栏互斥 = M-2; 格 B 的人群论证与枚举链修法互相矛盾 = M-3。另有两条与 `--base`/S3 相关的判据方向性错误 (M-4/M-5, 均已实跑反证), 一条 R2 修法在真实语料上不可执行 (M-6), 以及 09-10 头部复核只改了头部、没有下沉到 §4/Tasks/复议 #4 的版本目标 (M-7)。

建议 rework 顺序 (可全部由 Phase A 内完成, 不需 owner 拍板者优先): M-7 → M-2 → M-1 → M-3 → C-1 (枚举链补 `convergence`/`challenge` 两个 mode 值, 并给格 B 加「非 manual/adaptive 模式下空集必须判 error」的分支) → M-5 (S3 空 diff 显式短路 + SC) → M-4 (改写论证方向 + 补作用域膨胀的负向 SC) → M-6 (把 B.0 收窄为「只标注 SC-2/SC-4 采样到的族」并定义不一致条目在无人值守下的阻断规则) → 三条 minor。C-1 若 owner 认为应保留现语义, 则属 Rule #10 的语义选择, 须与复议 #8 合并请裁。

## 轮次记录

### Round 1: post_spec (2026-09-06, 引自聚合报告)
- Agents: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5 席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 5 / Major 9 / Minor 10 (另 7 条 decision 不计入)
- Vote: REVISE 5 / PASS 0

### Round 2: post_spec (2026-09-07, 引自聚合报告)
- Agents: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5 席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 2 / Major 9 / Minor 16 (另 12 条 decision 不计入; conflicted 0)
- Vote: REVISE 5 / PASS 0

### Round 3: post_spec (2026-09-10, 本报告)
- Agents: qa-engineer (本席位)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 15 (Critical 1 / Major 7 / Minor 3 / Decisions 5)
- Vote: REVISE
