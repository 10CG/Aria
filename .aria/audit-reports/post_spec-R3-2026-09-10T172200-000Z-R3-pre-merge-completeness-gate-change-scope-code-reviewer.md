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
timestamp: 2026-09-10T17:47:50.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [code-reviewer]
---

# post_spec R3 单席审计报告 — code-reviewer (pre-merge-completeness-gate-change-scope, v3)

席位透镜: 代码级核对。逐条打开 proposal 引用的 文件:行号 验证真伪 (行号漂移 / 函数名错 / 分支描述与真代码不符)；改动是否破坏同文件、同目录其它调用路径；文档同步面是否列全。本轮为新席位, 不继承 R1/R2 结论, 但逐条复核了 R2 的 2 critical + 9 major 是否真在正文落地。

核验基线: aria 子模块实读副本 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= `301641b`); 语料统计对冻结快照 `3f4b379`; 当前 aria gitlink 实测 `f314785` (v1.73.0), 主仓 HEAD `fe703c5`。

---

## 审计结论

### Decisions

- [minor] documentation/语料事实底盘独立复算: 对 `3f4b379` 独立写脚本全枚举, proposal 的载重数字逐个精确命中 —— `|C|`=152 (9 changes + 143 archive dirs + README)、末段族 **62**、`unattributed` **170** (全 8 checkpoint 口径) 与 **160** (本仓 `checked={post_spec,post_planning}` 口径)、真 2-field legacy **6**、原稿合并口径 **238**、post_spec **499** / post_planning **209** / post_implementation **3**、「全部自有报告皆末段形态」的组合 **25**、缺 `-R\d+-` 计数 24/2/1/1、含 `spec_id:`/`change_id:` 的报告 **78** (证据: proposal.md:38,51-53,115,198 对 `git ls-tree 3f4b379 .aria/audit-reports/`)
- [minor] documentation/SOT 引用行号逐条实读: `execution-modes.md:15,23-82,44,46-52,54-61,63-65,82,152,185` · `audit-engine/SKILL.md:49-54,63,75-81,381-391,403-419,410-411,123-125` · `report-storage.md:8,18,34-39` · `pre-write-validation.md:14,16-18,20-26,28-30` · `phase-c-integrator/SKILL.md:131,132,133-136,137,157,252,253,260,265,299` · `collectors/audit.py:52,62-69,245` · `spec_complete.py:924-930` · `DEFAULTS.json:118-123` (audit 键集确无两个 `allow_*`) · `config-example.md:280,381-400,402-417,419-440` · `project.md:117,118` · `configured-gate-authority.md:35,38,40` · `skill-benchmark-exemption.md:26-31,33,35` —— 全部命中所述内容 (证据: 逐文件 awk 取行比对)
- [minor] architecture/基线冻结与发版面复核: `git -C aria diff --stat 301641b f314785 -- <六个代码/规程触点>` 输出为空 (期间 21 文件 / 895 增 / 63 删), 与头部 (:16) 自述一致; §4 (:229) 列的 16 个主仓版本字符串点在当前 HEAD 逐行命中 (`README.md:8,242` + `README.{zh,ja,ko}.md:3,10,244` + `VERSION:24` + `CLAUDE.md:139,141` + `system-architecture.md:189` + `version-scheme.md:23`) (证据: proposal.md:16,229)
- [minor] implementation/R2 缺陷落地形态: 2 critical + 8 major 均落在判据本体而非批注 —— 空纳入集三格 (:188-196)、Step 3 优先级链 (:143-156)、stdout 15 键实数 15 (:197)、config 直读 + 内联 (:176-180)、照跑面收敛 (:308)、`--base` 绑定 (:85)、(b) 两处收窄 (:165)、SC-19 换真能翻转的反事实 (:299)、S1 继承 `allow_dangling_change_ids` (:92)、§1.2b 落点点名 + SC-13 两条 grep (:225,:293) (证据: proposal.md 上述各行)
- [minor] testing/机制谓词实跑验证: tmp 仓复现 `git mv` 归档移动 —— 默认 rename 检测只输出目的侧路径, `--no-renames` 才两侧齐 ⇒ SC-7(a) 反事实成立; 规则 2 + 规则 3 代入 778 份真语料, 多归属文件 0, 前缀/后缀/中缀三型排除正确且不误伤末段形态; `ab-suite/phase-c-integrator-pre-merge-gate.json` 实读确为 `type=workflow_skill_subextension` / 无 `evals` / 8 条 fixtures 绑单测 (证据: proposal.md:93,116,308)

### Issues

- [major] testing/SC-13 调用串计数 vs §2/§4 的 SKILL.md 写入规定: SC-13 断言 `grep -c 'completeness_gate.py'` 在 SKILL.md 与 execution-modes.md「各 1」; 而 §2 规定执行流程正文改写为「经 `completeness_gate.py` 机械执行」, §4 又要求相关文档加同名契约指针 ⇒ SKILL.md 必 ≥3 次, 该护栏结构上必红。先例 `sibling_spec_probe.py` 的「恰 2」是靠两行**长前缀串**限定 (裸文件名在 execution-modes.md 实测 3 次), 不能照搬到裸文件名计数 (证据: proposal.md:293 vs :210,:224; execution-modes.md:152; grep 实测 SKILL.md=1 / execution-modes.md=3)
- [major] architecture/§1.3 Step 3 三级链只覆盖 mode=adaptive: 级 2 判据逐字为「`audit.mode == "adaptive"` ⇒ 取 adaptive_rules」, 其余全落级 3 默认 `off`。而 `audit.mode` 是四值枚举, SOT 对 `convergence`/`challenge` 写的是「**所有检查点强制使用**该模式」—— 本仓 `.aria/config.json` 实测 `mode="convergence"`。未显式列出的 checkpoint 在该读法下应被纳入却被判 off ⇒ 与被修 bug 同型的残余假绿面; SC-20 三格只测 adaptive 场景 B/C, 该口径零断言 (证据: proposal.md:148-154,:300; config-example.md:271-280; audit-engine/SKILL.md:369)
- [major] implementation/§1.3 Level 解析硬阻未入 §5 行为变更: 新增「Level 解析不到 ⇒ `spec_level_undetermined` exit 2」, 经 §1.4 消费方 fail-closed + `on_fail: 阻塞合并`, 且 §1.1 的豁免枚举 (只降 S4/missing) 不覆盖它。实跑本仓 153 份 proposal, **15 份 (9.8%)** 头 15 行无可解析 Level 行 ⇒ adaptive 采用方对这些 change 恒硬阻。§5 自称穷举「五条」行为变更, 本条与「adaptive_rules 启用的 checkpoint 新被纳入 ⇒ missing 变多」两条均缺席; 另 `--no-spec` + adaptive 下 N=1 ⇒ `level_1="off"` ⇒ 空纳入集落格 B, 与 S3 承诺的 `not_applicable/level1-no-spec` 输出形状不同, 无 SC 消歧 (证据: proposal.md:156,:94,:97,:239-245; DEFAULTS.json adaptive_rules.level_1="off")
- [major] architecture/§1.3(b) 判据的语料证据与路径集不符: (b) 与复议 #7 以「实测 `2c8eaa6` 1/1」论证「本仓 Phase A 分支惯例把审计报告与 triage 一并落 `.aria/audit-reports/`」; 实读 `2c8eaa6` 两文件为 `.aria/decisions/2026-09-07-handoff-multibranch-...md` + `openspec/changes/.../proposal.md`, **零** audit-reports。triage 实际落 `.aria/` 根 (本文 References 自引 `.aria/triage-comment-199.md`)。⇒ 新路径集不含其自述的两类 Phase A 产物 (DEC 记录 / triage), 三例证据中一例反证该格仍不可达 (方向 fail-closed, 是假红) (证据: proposal.md:165,:323,:333; `git show --name-only 2c8eaa6`)
- [major] testing/新测试文件与既有 tests 目录 runner 分类冲突: 全部 SC 核验列用 pytest node-id 写法 (`::test_issue_case1_...` 等裸函数名), 而 SC-12 只跑 `python3 -m unittest discover`。同目录既有 `test_sibling_spec_probe.py` 有两条守卫锁「audit-engine/tests 恒 unittest 套件」(`:303-316` 禁顶层 import pytest, `:319-336` 断言 `run_all_tests.sh --list` 分类为 unittest)。裸 pytest 函数且不 import pytest ⇒ unittest 收集 0 个 = 整套新测试假绿; 加 conftest.py 或 import pytest ⇒ 既有两条守卫转红且无 pytest 时全套 SKIP。先例 spec 明写过该约束, 本文 Tasks/SC 零提及测试风格 (证据: proposal.md:281-302,:292; test_sibling_spec_probe.py:303-336; run_all_tests.sh:41-45,48; archive/2026-09-04-sibling-spec-probe/proposal.md:544)
- [major] documentation/版本目标三处未随头部订正: 头部 2026-09-10 基线复核已把 PATCH 候选改为 **v1.73.1** (实测 `plugin.json`=1.73.0, tag `v1.73.0` 在, 16 个版本点全读 1.73.0), 但 §4 同步表、Tasks 版本项、待 owner 复议 #4 三处仍写 **v1.71.2** 且原句无 strike/指针 neutralize。§4 自称是 Phase B 照单, 照执行会把 aria 5 文件 + 主仓 16 点回退到 1.71.2 (机械 check 只比派生面与 plugin.json 一致, 拦不住倒退), CHANGELOG 与 tag 序也乱 (证据: proposal.md:16 vs :229,:274,:317; aria/CHANGELOG.md `[1.73.0]` 段「版本号取号避开并发轨 #195/#199 正在争的 v1.71.2/v1.72.0」)
- [minor] documentation/头部基线复核的全称句过宽: (:16) 称「本文全部行号在 `f314785` 上继续有效」; 实测 `CHANGELOG.md` 顶部 +25 行, §5 引的 `CHANGELOG.md:3020` 在 `f314785` 已漂到 `:3045`, 与同文 (:9)「CHANGELOG 行号只对 `301641b` 成立」的 carve-out 自相矛盾 —— 与 R1 已勘正过的「全部触点文件 diff 为空」同型 (证据: proposal.md:9,:16,:235; `git show f314785:CHANGELOG.md | sed -n '3045p'`)
- [minor] documentation/两处引用行号不落在所述内容上: §4 与复议 #4 引 #195 `proposal.md:352` 为「推荐改走 MINOR v1.72.0」, 实读该行是「布局 3 — 老快照缺 `rel_path` 键」, 版本级别论证在 `:382-386`; §1.3(c) 与 References 引 `templates/proposal-minimal.md:27-31` 为「模板自带 `## Tasks` 小节」, 实读该小节为 `:28-32` (`:27` 是 Impact 表末行) (证据: proposal.md:231,:317,:170,:331)
- [minor] documentation/§3 接线 base 行的同源标注与被引行相反: §3 写 base = 远程跟踪 ref「本项目 `origin/master`, **不是裸 `master`**; 与 `:253`/#137 同源」; 实读 `phase-c-integrator/SKILL.md:252-253` 逐字规定的正是裸 `master`(「取本项目主干真实名字 —— 本项目是 `master`」/「`main_branch` 显式传真值 (本项目 `master`)」)。同源的只是「无缺省、显式传真值」那一半, 远程跟踪 ref 的真出处是 `audit-engine/SKILL.md:404-405` (证据: proposal.md:216; phase-c-integrator/SKILL.md:252-253)
- [minor] implementation/gitlink 条款在收窄后的路径集下不可达: (:83)(:165) 规定「diff 中出现 gitlink/submodule 条目时 (b) 不触发」; 但 (b) 的路径集已收窄为 `openspec/changes/{id}/**` ∪ `.aria/audit-reports/**`, gitlink 条目 (如顶层 `aria`) 必然落集外, (b) 已因路径判据不成立 ⇒ 该子句无可触发面; 且 S2 规定的 `git diff --name-only` 结构上不输出 mode 信息, 无从识别 gitlink。无 SC 覆盖 ⇒ 写了也无法证伪 (证据: proposal.md:83,:93,:165)
- [minor] implementation/纳入集迭代口径两读: (:156) 定义纳入为 per (checkpoint, change_id) 逐对求值并用 `enabled_by` 记「这对为什么没被查」, (:160) 却写「对每个纳入的 checkpoint × 作用域内每个 change_id」= 用并集叉乘。混合 Level 的多 change PR 下两读法结果不同 (叉乘会对 off 的那一对判 missing 假红); SC-7 只测同 Level 多 change, SC-20 只测单 change (证据: proposal.md:156,:160,:287,:300)

### Risks

- 无新增风险条目。Impact 现有 R-a…R-g 七条经复核与本轮 issue 无重叠; 其中 R-f (「(b) 判据 species 未变」) 与上表 §1.3(b) 条目同面, 本轮补的是它的**证据错误**而非重开 species 争论。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 6 / Minor 5 (另 5 条 decision 不计入)。

rationale: v3 的事实底盘经本席独立全枚举复算**逐个精确命中**, 三十余处 SOT 行号逐条实读全中, R2 的两条 critical 与八条 major 均落在判据本体; 方案 B 的机械化方向、规则 2/3 谓词、`--no-renames` 与三态路由经代入与实跑验证成立。**无一条 critical**: 本轮没有发现会破坏消费方、或使 SC 恒绿从而放行零证据的缺陷。

六条 major 分三类: (a) **v3 自造的内部矛盾** —— SC-13 的调用串计数与 §2/§4 规定的三处写入互斥 (Phase B 必红一条, 同 R2 `13c973b9` 形态); 版本目标 v1.71.2 与头部 v1.73.1 三处分叉且 §4 是 Phase B 照单。(b) **R2 修法只做了一半** —— Step 3 优先级链只机械化了四值 `audit.mode` 中的 `adaptive` 一支, 而本仓自己跑的正是 `convergence`; Level 解析新引入的 exit 2 硬阻在本仓语料上 9.8% 命中却未进 §5 的「五条」行为变更枚举。(c) **证据与落点错配** —— (b) 判据的三例语料证据中 `2c8eaa6` 实为 `.aria/decisions/` 而非 audit-reports, 且其自述要覆盖的 triage 类产物根本不在新路径集内; 新测试文件的宿主目录有两条既有守卫锁 unittest 分类, 本文用 pytest node-id 写 SC 却零提及, 两个分支一个假绿一个连坐红。

五条 minor 集中在引用精度 (两处行号不落在所述内容、`:253` 同源标注与被引行相反、头部全称句过宽) 与两处不可执行/两读条款, 随稿修订即可。

按 `report-storage.md §Verdict` 计算: 0 Critical + ≥1 Major ⇒ **PASS_WITH_WARNINGS**; post_spec `blocking: false`, 本判定不硬阻流程。但按横切检查原则 (数据可用性 / 事实错误对 verdict 载重) 与 Rule #10, 六条 major 须进 Phase B rework —— 其中「mode=convergence/challenge 的枚举语义」与「(b) 是否需要把 `.aria/decisions/**`、`.aria/triage-*` 纳入路径集」两项涉及放宽/收窄豁免面, 属既有复议 #7/#8 同面, **待 owner 复议**, 本席不代裁。

计算依据:
- Critical issues: 0
- Major issues: 6 (6 issue + 0 risk)
- Minor issues: 5 (5 issue + 0 risk)
- Decisions (不计入): 5

Vote: **REVISE** (major > 0)。

---

## 轮次记录

### Round 3

- Agents: code-reviewer (本报告为五席之一的单席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 16 —— Critical 0 / Major 6 / Minor 5 / Decisions 5
- 复核口径: R2 的 C2/M9 逐条到正文定位 (见 Decisions 第四条), 无一条以「已知悉」方式敷衍; 本轮 11 条缺陷全部锚在 R2 rework 新写的文本 (Step 3 优先级链 / 空集三格 / (b) 收窄 / SC-13 新增 grep / 2026-09-10 头部基线复核) 与「新增测试文件对既有目录的影响」这一未被前两轮触及的面上, 无一条是 R1/R2 结论的重复提出
- Vote: REVISE
