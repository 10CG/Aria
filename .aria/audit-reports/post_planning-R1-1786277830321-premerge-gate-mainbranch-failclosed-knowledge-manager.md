---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-09T13:09:35.372Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 审计报告 — knowledge-manager 席位

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md` + `detailed-tasks.yaml` (19 条任务)。
参照物: `proposal.md` (post_spec R1-R5 25 agent-run, `converged: false`, owner override 放行, 不重审)。

镜头: 规范合规 / 一致性 / 外部事实 (schema 对照 · ship_target 四处一致性 · MAJOR 连锁后果 · Rule #6 工具口径 · Rule #5/#9/Level 3 交付物 · TASK-019 可证伪性)。全程只读, 未改任何文件。

---

## 审计结论

六项指定核验逐条实读+实跑结论如下:

1. **schema 合规**: `scope_repos[]` 缺姊妹 Spec `linked-issue-normalization/detailed-tasks.yaml:27-33` 已建立的 `head` 锚定基线字段; `tasks.md` 与 `detailed-tasks.yaml` 对 TASK-001 交付物路径给出了不同的选择集。均实读确认, 定级 minor (下述 M-1/M-2 说明理由)。
2. **ship_target 四处一致性**: 四处**未**完全一致——`detailed-tasks.yaml:19` 与 `tasks.md:5` 把 MAJOR 写成无条件事实, 但 `proposal.md:12` (抬头) 与决策表 D11 (`:186`) 仍停留在 R5 之前「地板=MINOR, 待裁」的措辞, 与 `proposal.md:257-266`(§版本) 自身的更正矛盾; `tasks.md:69`(未决#3) 把 MAJOR 又挂成待 owner 确认。定级 Major (下述 M-3)。
3. **MAJOR 连锁后果**: `pre_merge_gate.py:68`/`:116` + `SKILL.md:49`/`:349` 确认存在「until v2.0 / removed in v2.0」的弃用到期承诺 (`no_aether_fallback` / `primitive_preference` 两个 legacy alias, 由本 Spec 引作先例的 commit `7661e96` / v1.31.0 引入); 19 条任务、§非目标、TASK-019 的 5 项 follow-up 均未提及。与上一条同因同果, 合并计入 M-3。
4. **TASK-015 (Rule #6) 工具口径**: verification 未点名 `/skill-creator`(CLAUDE.md:101 逐字要求), 也未内联 `AB_TEST_OPERATIONS.md:544-548`「发版前」checklist 的结果判据(WITHOUT_BETTER / 回归比对 / summary.yaml 审查)。定级 Major (下述 M-1)。
5. **Rule #5/#9/Level 3 三件套**: Rule #5(项目变更落主仓 `openspec/changes/`, 非 `standards/openspec/changes/`)与 Rule #9(无 `.aria/handoff/` 误用)均**合规**, 三件套(proposal.md + tasks.md + detailed-tasks.yaml)**齐备**。但 `tasks.md:67` 未决#1「detailed-tasks.yaml 是否补」在该文件已存在且是被审对象本身的前提下已**陈旧**。定级 Minor (下述 M-2)。
6. **TASK-019 可证伪性**: 5 条 verification 全部是「issue 该写什么内容」, 无一条断言「issue 确实被创建」, deliverables 写「Forgejo issue ×N」但 N 未定、无 URL/编号占位。按现状写法可在零 issue 创建情况下自称完成。定级 Minor (下述 M-4)。

本轮同批的 tech-lead / code-reviewer 席位在审自身镜头时也各自独立触及第 2/3/4/5/6 项中的部分对象(未决#1 / TASK-015 工具 / TASK-019 可证伪性 / ship_target 四处), 属独立复现, 未参考其报告成文(本报告先完成六项核验与实读实跑, 后仅抽查其 frontmatter/小节标题做校准, 未采信其结论)。

零 Critical。定级 **PASS_WITH_WARNINGS**。

---

## Major

### M-1 — TASK-015 (Rule #6 零裁量) 的验收缺工具口径与结果判据

**锚点**: `detailed-tasks.yaml` TASK-015 (`:291-308`) · `CLAUDE.md:101` · `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:544-548` · 对照 `linked-issue-normalization/detailed-tasks.yaml:513-520`(TASK-013)

CLAUDE.md 规则 #6 逐字:「**Skill 基准测试必须用 `/skill-creator`**(自研 runner 已废弃)」(`:101`)。`AB_TEST_OPERATIONS.md` 的「发版前」checklist(`:544-548`)逐字四条:

```
544:### 发版前
545:- [ ] Tier 1 Skills 全量 AB 测试已执行
546:- [ ] summary.yaml 已生成并审查
547:- [ ] 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)
548:- [ ] 与上一次结果比对，无回归
```

TASK-015 实际 verification 只有两条:
```
- "ab-suite/phase-c-integrator.json 与 phase-c-integrator-pre-merge-gate.json 两套件均跑完, 结果存档"
- "不得以「套件对 C.2.4 覆盖薄」为由降档 — 第二行是零裁量的"
```

既未点名 `/skill-creator` 这个工具(照字面「跑完+存档」用已废弃的自研 runner 也能满足), 也无任何结果判据 —— 若跑出 `WITHOUT_BETTER` verdict 或相对上次有回归, 按现状写法仍可勾掉。对照姊妹 Spec 同类任务 TASK-013(`linked-issue-normalization/detailed-tasks.yaml:513-520`)逐条写了「AB 经 /skill-creator 执行」「无 WITHOUT_BETTER verdict」「与上一次结果比对无回归」「summary.yaml 已生成并审查」四条, 本 Spec 缺同等力度。

⚠️ 此缺口部分继承自 `proposal.md:216-224`(§Rule #6)本身——该节同样只写「照跑 AB, 零裁量」「结果存 `ab-results/`」, 从未点名工具或结果阈值, 故不完全是 tasks 层新引入, 但 tasks 层本应补足而未补足(A.2/A.3 的职责正是把 proposal 的「什么算对」转成可执行、可证伪的 verification)。

**blocks_phase_b**: false — TG-0/1/2 与此无关; 但 TG-3 关闭前必须补上, 否则 Rule #6 这条「零裁量」规则在本 Spec 里名存实亡。

### M-2 — ship_target 四处未完全收敛 + MAJOR⇒v2.0.0 触发的弃用到期承诺无任务承接

**锚点**: `detailed-tasks.yaml:19` · `tasks.md:5` · `tasks.md:69`(未决#3) · `proposal.md:12`(抬头) · `proposal.md:186`(D11) · `proposal.md:257-266`(§版本) · `pre_merge_gate.py:68`,`:116` · `SKILL.md:49`,`:349` · `aria/.claude-plugin/plugin.json`(实测 `"version": "1.65.5"`) · commit `7661e96`

四处逐字比对(均已实读):

| 位置 | 逐字/要义 |
|---|---|
| `detailed-tasks.yaml:19` | `ship_target: "MAJOR — 破坏性签名变更 (CLI 参数由可选变必填); 号段落地时按 plugin.json 计算, 不预写字面量"` — 无条件断言 |
| `tasks.md:5` | `**ship target**: **MAJOR** (见 proposal §版本; 破坏性签名变更)` — 无条件断言 |
| `proposal.md:12`(抬头) | `**ship target**: **地板 = MINOR** … MINOR vs MAJOR 待 owner 裁 — 见 §版本` — R5 之前的旧措辞, **未随 §版本 更新** |
| `proposal.md:186`(D11) | `Level 3; 版本**地板 MINOR**` — 同一份旧措辞的第二处残留 |
| `proposal.md:257-266`(§版本) | `**结论: MAJOR。** 上一版写「地板 = MINOR, MINOR vs MAJOR 待裁」是**逻辑错误**` — proposal 自己指出抬头那句错, 但抬头与 D11 均未回改 |
| `tasks.md:69`(未决#3) | `**版本 MAJOR 的确认**(proposal §版本) — 或写下「不构成对外破坏性变更」的论证` — 把 MAJOR 又挂成待裁 |

四处中三处(yaml/tasks.md 头/proposal §版本)同向(MAJOR), 但 proposal 自身两处(抬头+D11)未跟 §版本 同步, 且 tasks.md 自己的头部(无条件)与未决段(待确认)互相矛盾——若 detailed-tasks.yaml 是 Aria 2.0 Layer 2「AI execution basis / single source of truth」(`standards/openspec/specs/detailed-tasks-yaml-format.md:15` 逐字), 无条件的 `ship_target: "MAJOR"` 有诱导自主执行路径跳过 owner 确认步骤的风险, 而 proposal §版本 自己写明「若 owner 认为不构成破坏性变更, 须显式写下该论证并据此改档」——这是一步尚未发生的 owner 动作, 不是既成事实。

**连锁后果**(实测): `aria/.claude-plugin/plugin.json` 当前 `"version": "1.65.5"`。SemVer MAJOR bump ⇒ **2.0.0**。而本 Spec 唯二改动的文件之一 `pre_merge_gate.py` 里逐字写着:

```
68:# Old keys still readable until v2.0; new key wins on conflict (Hard #9).
116:                    f"will be removed in v2.0",
```

对应 `SKILL.md:49`(`no_aether_fallback` … alias 仍读, 发 deprecation warning, **v2.0 移除**)与 `:349`(config schema 示例注释同措辞)。该 alias 机制由本 Spec 自己引作 TASK-016 先例的 commit `7661e96`(v1.31.0, 2026-05-28)引入, 已用 `git show --stat` 核实其 commit message 逐字含「legacy no_aether_fallback / primitive_preference → no_ci_fallback / ci_backends」。⇒ 若 ship_target 最终确认为 MAJOR, 本 Spec 落地的**同一个版本**就是这两个 alias「removed in v2.0」承诺到期的版本, 但 TASK-001..019、§非目标、TASK-019 的 5 项 follow-up 清单里**无一字提及**它。TASK-017/TASK-018 的发版同步面口径找的是 `pre_merge_gate|gate_check|pre-merge gate` 引用点, 结构上捞不到「版本号本身触发的移除承诺」这一维度。

**修**: (a) 统一四处——建议以 §版本 的 MAJOR 结论为准, 同步改掉 proposal 抬头与 D11 的旧措辞, `tasks.md` 未决#3 改写为「MAJOR 已是 §版本 结论, 待 owner 对该结论签字或书面反驳」而非平铺「待裁」; (b) 为 v2.0 弃用到期承诺加一条任务(或至少加进 TASK-019 的 follow-up 清单成第 6 项), 显式选择「随本次一并移除 legacy alias」或「明确展期并改写承诺文案」——两者选一, 不能沉默略过。

**blocks_phase_b**: false — TG-0/1/2 的 grep 断言与 spike 均不依赖版本号确定; 但进入 TG-3(尤其 TASK-016 CLAUDE.md 同步)与 TG-4(TASK-019)前必须解决, 否则本条会在 Phase C 才被发现, 届时回退成本更高。

---

## Minor

### M-3 — `scope_repos[]` 缺锚定基线字段 + TASK-001 交付物路径两层不一致

**锚点**: `detailed-tasks.yaml:6-19`(`scope_repos` 块) · 对照 `linked-issue-normalization/detailed-tasks.yaml:25-36`(`scope_repos` 含 `head`/`path_prefix`/`surface`) · `tasks.md:17` vs `detailed-tasks.yaml:38`(TASK-001 deliverables)

(a) **缺 `head`**: 本 Spec `scope_repos` 只有 `repo`/`role`/`paths` 三键:
```yaml
scope_repos:
    - repo: aria
      role: submodule
      paths: [SKILL.md, pre_merge_gate.py, test_pre_merge_gate.py 三个路径]
    - repo: Aria
      role: main
      paths: [CLAUDE.md, openspec/changes/.../]
```
姊妹 Spec 同一位置(`:25-36`)每个 repo 条目都带 `head: "<SHA>"` 锚定该 repo 在 A.2 落笔时的基线提交, 理由是该 Spec 本身在其 `version_reference_surface` 注记里写明这类锚点是为了防止版本引用点在 A.2→C 之间漂移。本 Spec 的 SC 表与 19 条任务的 verification 同样大量依赖精确行号(`:99` `:167/168` `:218` `:243/244` `:270` `:279` `:300` `:427` `:663` `:710` 等), 本轮审计逐条用 `grep -n`/`sed -n` 复核**全部仍准确**(未发现现存漂移), 但 `scope_repos` 没有可供未来复核的锚点——下次审计或 B.2 执行时若这些行号已变, 无法机械判断是「实现按 spike 结论改动了」还是「基线本身漂移导致引用失效」。因目前未发现实际漂移(功能性风险未兑现, 且没有已知的第二个并发 Spec 正在改 `phase-c-integrator/` 下的文件), 定级 minor, 不升 major。

(b) **TASK-001 两层给出不同的路径选择集**: `tasks.md:17` 逐字「建 `test_premerge_gate_mainbranch.py`(**或并入既有文件**)」——明确提供两个选项; 而 `detailed-tasks.yaml` TASK-001 的 `deliverables`(`:38`)与 `scope_repos.paths`(`:12`)都**只**列出既有文件 `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py`, 未把新文件名纳入 scope。若执行者选「新建文件」这个 tasks.md 明确给出的选项, 产出会落在 `scope_repos` 声明范围之外。经查 `aria/skills/run_all_tests.sh:38`(`ls "$tests_dir"/test_*.py`)按 glob 自动发现测试文件, 与文件名无关, 故此分歧**不会**造成新文件被测试运行器漏掉(功能性后果被验证为不成立), 纯属两层文档的范围声明不一致, 定级 minor。

**修**: 二选一写死(建议直接定「并入既有文件」, 与本 Spec 其余 18 条任务全部编辑既有 3 个文件的模式一致), 并给 `scope_repos` 补 `head` 字段。

### M-4 — `tasks.md` 未决#1 已被自身产物解答

**锚点**: `tasks.md:67`(未决#1) · `detailed-tasks.yaml`(文件整体存在, 19 条任务, 含完整 A.3 `agent`/`verification` 字段, 即证伪) · `standards/openspec/project.md:21` vs `:118`(实读确认两处表述不一致)

`tasks.md` 未决#1 原文:「**`detailed-tasks.yaml` 是否补** —— `standards/openspec/project.md` 两处表述不一致(`:21` 双层 / `:118` 单层), 而**两个先例 Spec 实际都有**。」——但 `detailed-tasks.yaml` **已经存在**且正是本次 post_planning 审的对象本身, 「是否补」这个问句在读者拿到这份文件的同一时刻就已经被证伪。实读 `standards/openspec/project.md` 确认两处矛盾确实存在:
```
:21 一带 「任务表达 | Level 3: proposal.md + tasks.md + detailed-tasks.yaml (双层) | ...」
:118 一带「| 3 | Full | Architecture changes | proposal.md + tasks.md |」(不含 detailed-tasks.yaml)
```
但这是 `standards` 子模块自身的遗留不一致, 不是「本 Spec 要不要补」的问题——本 Spec 已经用行动(产出该文件)回答了这个问题。未决#1 的措辞把「上游文档矛盾待修」和「本文件是否需要该产物」混成一句, 前者依然待决(应转给 `standards/openspec/project.md` 的维护者), 后者已经不待决。

**修**: 把未决#1 改写为「`standards/openspec/project.md:21` 与 `:118` 表述不一致, 建议开 issue 交 standards 维护者; 本 Spec 的 `detailed-tasks.yaml` 已按两个先例 Spec 的惯例产出, 不再是本文件的待决项」, 或直接删除并把 project.md 矛盾上报。

### M-5 — TASK-019 的 verification 只证「issue 该写什么」, 不证「issue 确实存在」

**锚点**: `detailed-tasks.yaml` TASK-019(`:359-378`)

```yaml
deliverables:
  - "Forgejo issue ×N"
verification:
  - "(1) main_branch 自动解析设计面 …"
  - "(2) phase-d-closer/fetch_gate.py 字面 …"
  - "(3) workflow-runner gate_state 无 gate_error …"
  - "(4)「显式传错分支名」此前零测试覆盖"
  - "(5) C.2.4.5 的 SKILL.md:189-191 裸 git 命令 …"
```

deliverables 写「Forgejo issue ×N」, N 未定; 5 条 verification 逐条都是「issue 正文该覆盖哪些内容点」, 没有一条断言「issue 这个 artifact 本身被创建」这件事——例如「N≥1, 每个 issue 的 URL/编号记录在此, 可经 `forgejo GET /repos/.../issues/{n}` 检索到」这类可证伪断言完全缺席。按现状写法, 该任务执行者可以只在 audit-trail 或 commit message 里把这 5 点内容写全, 而从未调用 Forgejo API 创建任何 issue, 也不会被任何一条 verification 挡住——即「它怎么会红」这个问题, 当前 5 条无一能回答。

**修**: 补一条形如「N(具体数字, 建议 1 或 5)个 Forgejo issue 已创建, 每条 URL 记录在 TASK-019 执行记录里, 且可经 `forgejo GET /repos/10CG/aria-plugin/issues/{N}` 检索到非 404」的存在性断言, 内容五条降级为「该断言里的正文摘要须覆盖以下 5 点」的从属条件。

---

## Verdict

**PASS_WITH_WARNINGS**(0 Critical / 3 Major-bucket 项目实为 2 Major + 3 Minor, 见上)

- Critical 0 / Major 2 (M-1, M-2) / Minor 3 (M-3, M-4, M-5)
- 无 Critical: 六项指定核验均未发现「任务清单会产出错误代码」级别的缺陷; 两个 Major 都是「Level 3 应该钉住但没钉住」的范围/验收完整性缺口, 不阻塞 TG-0~TG-2 的 TDD 前置与实现工作。
- 两个 Major 必须在进入 TG-3(合规与同步面)之前补上, 否则 Rule #6 零裁量条款与 MAJOR/v2.0 弃用承诺会在 Phase C 才暴露, 回退成本更高。
- 三个 Minor 属文档 hygiene, 建议随手清理(尤其 M-4, 一句话即可修), 不阻塞任何 Phase B 工作。

**建议**: PASS_WITH_WARNINGS 下可以推进 Phase B; 但请把 M-1/M-2 的修法(统一 ship_target 表述 + 补 v2.0 弃用承诺处置 + TASK-015 补工具与结果判据)记入 TG-3 任务本身的 acceptance, 而非仅口头承诺。

---

## 轮次记录

| 轮 | 席位 | Critical | Major | Minor | verdict | 备注 |
|---|---|---|---|---|---|---|
| R1 | knowledge-manager | 0 | 2 | 3 | PASS_WITH_WARNINGS | 六项指定核验(schema/ship_target 四处/MAJOR 连锁/Rule#6 工具/Rule#5+9+Level3/TASK-019 可证伪)逐条实读+实跑; 未参考同批其他席位报告成文, 仅事后抽查 frontmatter 做校准 |
