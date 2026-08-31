---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-30T17:22:41.318Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 3
minor_count: 6
r1_disposition: {closed: 11, partial: 1, not_addressed: 0}
introduced_by_fix: 6
---

## 摘要

R1 本席 12 条 (2C/6M/4m) **逐条到终版文件亲验**: 11 条 closed, 1 条 partial (`95f02272`), 0 条 not_addressed。两条 critical 的机械证据已消失 —— 探针 TASK-018 与母 TASK-038 的 deliverables 现各含 `README.md` badge + i18n ×3 + `plugin.json`, 「全部改完后才断言两条 check 绿」的措辞三份齐备, 我 R1 用来证明「必红」的那个模拟前提 (deliverables 不含 check 要读的文件) 不再成立。版本字面量 `1.68.0` 两文件零命中, `README.zh-CN.md` / `.gitmodules 承载 gitlink` 两处错误路径已删。

依赖图我**没有采信任何一份对账表**, 用自己的脚本重跑了三份: 25/18/39 任务全部合法解析、无重复编号、无悬空依赖、无环; 同 deliverable 多写入方的对全部有向可达 (母 Spec 两处例外是 TASK-001↔TASK-003, 二者 deliverable 注释均为「只读核验」, 非写入方); RED 无一依赖其 GREEN; 母 Spec 除 TASK-001/002/003/039 外全部传递到达 TASK-001 与 TASK-003; 探针全部到达 TASK-001 与 TASK-003。**镜头 3 点名的两个疑点均判无问题**: 探针 TASK-004 ← TASK-003 (AB 套件) 不是不合理前置 —— proposal `:473` 逐字「该任务未 done 则 **Phase B.1 不得开始**」, 把它编码成 B.2 首任务的边是忠实派生; 各链的「B.1 起点」确在最前。语义倒置零发现。

问题**全部落在本轮 fix 自己新写的那 ~300 行上**, 且形状高度一致: **改了边, 没改描述那些边的散文与证据**。9 条 finding 里 6 条 (3 条 major 里的 2 条) 由本轮 fix 引入 —— 按 memory `marginal-return-negative` 的判据 (本轮 fix 引入占比 > 1/2 即到拐点), **不建议再加第三轮五席**; 三条 major 各有一行可跑命令, 定点修 + 主控自验即可。

三条 major:

1. **母 Spec 的发布链缺 aria 子模块「本地 merge + 双推 + 逐 remote ls-remote」的任务宿主** (残留, R1 我自己漏了)。程序化实测: 母 Spec 39 个任务里, verification 含该纪律的**只有 TASK-024, 且它管的是 `standards`**; 字段 Spec 有专任务 TASK-022 (aria) + TASK-023 (standards), 探针 Spec 落在 TASK-018 verification —— 三份里**只有母 Spec 的 aria 这条腿没有宿主**, 而它 verification 又断言「gitlink SHA 在两个 remote 上均可取到」= 断言了一个没人执行的动作的后置条件。
2. **探针 `execution_order` 与 `dependencies` 正面矛盾两处**, 且矛盾点恰是主控追记新加的两条边 (fix-introduced)。
3. **探针 tasks.md「机械核验」段贴的脚本逐字重跑 `RESULT: FAIL`**, 且其中不变量 (e) 因转义被降级为恒真 (fix-introduced)。

---

## R1 finding 逐条闭合表

| id | R1 severity | 处置 | 实证命令 + 结果 |
|---|---|---|---|
| `a257ffa4` | critical | **closed** | `python3 -c "yaml…"` 读探针 TASK-018 deliverables ⇒ 12 项, 含 `VERSION` / `README.md` / `README.zh.md` / `README.ja.md` / `README.ko.md` / `CLAUDE.md` / `aria` (gitlink); verification[2] 逐字「正文无实质变更 ⇒ **不重译**, 但三份 `<!-- translated-from: v<vNEXT> -->` 标记与各自两处版本串**必须同批改** —— check 读的是标记」; verification[3]「在完成上述**全部**文件后才断言 … 绿」。R1 的必红前提 (deliverables 不含 check 读的文件) 已不成立 |
| `73809784` | critical | **closed** | `grep -rn 'README.zh-CN' */tasks.md */detailed-tasks.yaml` ⇒ 仅对账段留痕, 无 deliverable 命中; 母 TASK-038 deliverables = `aria` / `VERSION` / `README.md` / `CLAUDE.md` / `README.{zh,ja,ko}.md`; `:964` 注释逐字写明 gitlink 是 index/tree 条目「**不是** .gitmodules」; verification[1] 的 grep 负控含 `CLAUDE.md`, 口径「14 处 (与 086ee32 同)」—— `git log -1 --format=%s 086ee32` 逐字 14 点, `git show --stat 086ee32` = 7 文件 15 行 ✅ |
| `3221f943` | major | **closed** | `grep -rn '1\.68\.0\|1\.67\.3' */detailed-tasks.yaml` ⇒ **零命中** (仅 tasks.md 对账/待 owner 段的留痕句); 母 TASK-031~035 五处目录字面量 = `ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/…`; 三份 `ship_target` / notes 落同一句 (档位与号 owner 裁 / 串行各占一号 / 合并一版由母承接 / 未裁不开工 `pending`) |
| `c23f47ce` | major | **closed** | 字段 yaml `:272` 与 `:536` 均改为 `test ! -d aria/skills/audit-engine/lib && test ! -d aria/skills/audit-engine/collectors`, 并逐字写「**不断言**目录条目总数 — 探针 Spec 的 `scripts/` + `tests/` 合法」; 与探针 TASK-004 的渲染同形 ✅ |
| `6698004d` | major | **closed** | 三份全部落: 探针 TASK-003 / TASK-017 · 字段 TASK-017 · 母 TASK-033 / TASK-035 的 deliverables 各含 `ab-suite/version.yaml`, verification 写程序化重算命令; 「29→30 / 58→60」与「== 32」字面已删。实测基线 `ls ab-suite/*.json \| wc -l` = **31**, `sum(len(evals))` = **73**, version.yaml 仍 29/58 ⇒ 首个 ship 的 Spec 会把它拉回真值 |
| `35dad35d` | major | **closed** | 字段 TASK-017 `dependencies` 现含 TASK-016 (同文件串行, 我自己的可达性脚本复核 OK); 母 TASK-035 verification 有 max(id)+1 条 + 「不修改**任何**既有 eval」; 母 TASK-032 标题 =「当时套件全部 eval; d69091d 时 2, 字段 Spec ship 后为 3」; 母 `seam_rules[2]` 覆盖 `spec-drafter.json` 三处写入 |
| `05b5c605` | major | **closed** (衍生新 minor `a7311d2e`) | 母 TASK-018 verification[3] 现为显式两分支 ((i) 已 ship ⇒ 断言不相邻 + `git merge-tree` 干跑; (ii) 未 ship ⇒ **不断言**, PR 记「由字段 TASK-014 对称分支在其 ship 时验」); `seam_rules[1]` 从断言式改为义务式 (「**落地时须核验的义务**, 不是既成事实」) ✅。分支**判据的输入**另见 `a7311d2e` |
| `96ecdeb4` | major | **closed** | 字段 TASK-013 verification[5] 与 TASK-015 verification[5] 各有逐字「占位串 `{<org>/<repo>#<n>}` 逐字节 = 探针 SC-19 `_RAW_KEY_BLACKLIST` … 须**同批改两 Spec**」; `metadata.exports_for_siblings.seam_rules[0]` 收录。跨文核对: `grep -n 'SC-19' openspec/changes/sibling-spec-probe/proposal.md` ⇒ `:505` 该行确含逐字 `` `{<org>/<repo>#<n>}` `` (`:111` 亦含) ✅ |
| `1246445b` | minor | **closed** | 探针 TASK-010 verification[1] 现为『包含』口径:「三条 import 逐字存在 … 同块允许追加第四符号 `is_sentinel` … **断言用『包含』非『恰等』**: 全文件 `sys.path.insert` 仅此一处 (grep -c == 1), 块外零 `from lib.`」; `a2_discretions (i)` 追记三席复核结论 |
| `970d3368` | minor | **closed** | 字段 yaml `:266` SKIP 文案 = 「… 缺失 / 版本 < `<vNEXT>`」+ 「落地时以 plugin.json 实际号回填并在 PR 点名, 不预写字面版本」 |
| `95f02272` | minor | **partial** → 见 `95f02272` (同 id, 残留半) | deliverables **已补** `CLAUDE.md` ✅; 但标题与 verification[0] 仍是「**12** 个引用点」, verification[3] 只点「项目状态「版本:」行」(= `:141`), **`:139` 未点名**, 且负控 `grep -rn '1\.67\.2' VERSION README.md README.*.md` **不含 CLAUDE.md**; tasks.md `5.5` 整行无 `CLAUDE.md` |
| `af9f0c47` | minor | **closed** | 探针 `interface_expected.token_elements` 现为「= 全部元素 (含不可解析者); 坏元素的**点名**由字段 additive `bad_elements` 承担, 本探针不消费」+ 括注 R1 出处 ✅ |

---

## Findings

> ⚠️ 4-tuple id 碰撞: `3221f943` 与 `95f02272` 与我 R1 的两条同 id (同 category/scope/severity/type)。`95f02272` 是**同一条**的残留半 (故意同 id); `3221f943` 是**不同内容** (R1 该条已 closed), 聚合请按内容分簇。

| id | severity | category | scope | type | 描述 + 证据 + 处方 | 来源 |
|---|---|---|---|---|---|---|
| `3221f943` | major | architecture | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | issue | **母 Spec 的发布链没有任何任务执行 aria 子模块的「本地 merge → master + 双推 + 逐 remote `ls-remote` 核验」, 而 TASK-038 断言了这个动作的后置条件。** 证据 (程序化, 见实测记录 3): 扫三份 yaml 的 verification 找该纪律 ⇒ **母 Spec 唯一命中是 TASK-024, 且它管的是 `standards`** (`:672` 逐字「standards 子模块: 本地 `git merge` + `git push origin && git push github` + 逐个 `ls-remote` 一致」); 字段 Spec 命中 TASK-022 (aria, 6 条 verification 含 fetch 断言 / `--no-ff` / 双推显式超时 / 逐 remote 比对 / gitlink / **owner 推送授权**) 与 TASK-023 (standards); 探针 Spec 命中 TASK-018 (verification[4] 同款)。母 Spec 的发布链是 TASK-037 (aria 五文件 bump) → TASK-038 (主仓面), **中间那一步没有宿主**; 而 TASK-038 verification[0] 逐字要求「该 SHA 在 `git -C aria ls-remote origin master` 与 `github master` 上均可取到」—— 断言一个无人执行的动作的结果。硬约束 1/2 只出现在 TASK-038 的 `notes` 散文里 (memory `no-code-host-no-assertion`: 只在散文里的义务没有宿主; 而这正是 #165 三次复发的那条腿)。**同类三份只错一份** (memory `fix-the-class`) —— 且母 Spec 自己对 `standards` 那条腿写对了, 说明是漏项不是裁量。**处方**: 母 Spec 在 TASK-037 与 TASK-038 之间补一个 tech-lead 任务 (照抄字段 TASK-022 的六条 verification, 含 owner 推送授权那条 memory `sync≠push-auth`), TASK-038 `dependencies` 改指它; 或明写「本 Spec 的 aria 合并由 phase-c-integrator §C.2.5 承接」并给出该 Skill 真做这件事的行号 (memory `delegate-verify`, 未核不得写) | 残留 (R1 本席漏报) |
| `ea33f282` | major | implementation | `openspec/changes/sibling-spec-probe/detailed-tasks.yaml` | issue | **探针 `execution_order` 与 `dependencies` 正面矛盾两处, 矛盾点恰是本轮追记新加的两条边。** 证据 (实跑 `yaml.safe_load` 取两个键对照): (1) `execution_order[0]` 逐字「**[并行, 不同文件]** TASK-001 · TASK-002 · TASK-003」, 而 `TASK-003.dependencies == ['TASK-002']` —— 主控追记 (2) 逐字「TASK-002 断言『无 `audit-engine.json`』与 TASK-003 建该文件存在隐性时序, 追加 TASK-003 ← TASK-002 边」。**并行叙述仍在授权它要防的那个并行**: 按 `execution_order` 先跑 TASK-003, TASK-002 的基线断言「`ab-suite/` 无 `audit-engine.json`」当场为假。(2) `execution_order[1]` 逐字「TASK-004 (测试骨架 + SC-21) ← **001, 002**」, 而 `TASK-004.dependencies == ['TASK-001','TASK-002','TASK-003']` —— 追记 (1) 加的 TASK-003 边 (proposal `:473` B.1 前置) 在执行顺序叙述里**看不见**。metadata `ordering_note` 虽写「执行顺序以 dependencies 拓扑为准」, 但同一文件里两处叙述与拓扑相反, 且 B.2 执行者读的是叙述。**该 Spec 自己的机械检查 (e) 结构上抓不到它** —— (e) 只判「并行行内两任务是否同文件」, 而这里的错误是**顺序维度**, 不是文件维度 (memory `invariant-dimension`: 无向检查对方向性错误天然免疫)。**处方**: `execution_order[0]` 改为「TASK-001 ‖ TASK-002 → TASK-003 (← 002, 见追记)」; `execution_order[1]` 补 `003`; (e) 增判「并行行内任意两任务之间不得存在 (传递) 依赖边」 | **fix 引入** |
| `4802c929` | major | testing | `openspec/changes/sibling-spec-probe/tasks.md` | issue | **「机械核验」段贴的脚本逐字重跑 `RESULT: FAIL` (exit 1), 与其下方声称的逐字输出 `RESULT: PASS` 不符; 且其中一条不变量被转义降级为恒真。** 证据 (实跑: 从 tasks.md 提取第一个 ```python 块原样落盘执行, 见实测记录 2): 实际输出 `RESULT: FAIL parent mismatch [...18 项...] vs []`, exit 1; 声称输出「parent 1:1 … -> True (18 vs 18)」「estimated_hours present on all = True」「(e) parallel line ['TASK-001','TASK-002','TASK-003']」。根因 = 三处正则被双重转义: `:234` `re.findall(r"TASK-\\d{3}", line)` / `:245` `re.findall(r"^- \\[[ x]\\] (\\d+\\.\\d+) ", …)` / `:250` `re.compile(r"\\d+-\\d+")` (对照: 母 Spec 同段 `:310` / `:393` / `:411` 全是单反斜杠 `\d`, 我实跑其脚本可正常执行)。后果分级: `:245` ⇒ `md_ids == []` ⇒ 报 FAIL (**噪声型**, 但把整段的 PASS 结论作废); `:234` ⇒ (e) 的任务名列表恒为 `[]` ⇒ 「same-file pairs = none」**恒真, 零信息** (memory `false_green_dual_is_permanent_red`); `:250` ⇒ `hrs_ok` 恒 False 但不入 `fails` (**假红且不阻断**)。我用正确正则复核: parents == md_ids 为 True (18 vs 18) —— 即**结论对, 证据坏**。**处方**: 三处 `\\` 改 `\\`→`\`(单), 重跑并把真实输出替换进 tasks.md; (e) 按 `ea33f282` 扩维度后一并重跑 | **fix 引入** |
| `f1cc9ee9` | minor | testing | `openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md` | issue | **母 Spec「机械核验」贴的逐字输出与当前文件不同步: 声称 `[a] 同文件写入对 40 对`, 实跑 **37 对**。** 证据 (实跑同一脚本, 见实测记录 2): 唯一差异行 —— 声称 `phase1_gate.py: TASK-003 -> TASK-014 -> TASK-015 -> TASK-016` (4 写入方 = 6 对), 实跑 `TASK-014 -> TASK-015 -> TASK-016` (3 写入方 = 3 对), 差 3 对。原因: 脚本按 deliverable 行尾注释含「只读」排除写入方, 而 yaml `:192` TASK-003 的 `phase1_gate.py` 现带 `# 只读核验:` —— 与该段自己的对账句「TASK-003 的 16 条 deliverable **未标只读**, 被计为上游写入方」矛盾 ⇒ 输出是在这次注释编辑**之前**跑的。两次都 PASS, 结论不变, 但「逐字输出」不可复现 = 证据失效 (memory `past-summary≠measurement`)。**处方**: 重跑并替换该段输出, 同时把对账句改成与实际排除规则一致 | **fix 引入** |
| `95f02272` | minor | documentation | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | issue | **发布同步面三份口径仍未逐字对齐 (母 14 / 探针 12+CLAUDE.md 另述 / 字段 12), 且字段 Spec 漏了 `CLAUDE.md:139` 并把它排除在唯一的负控之外。** 证据: 母 tasks.md `:90` + yaml TASK-038 verification[1] = 「**14 处**… CLAUDE.md ×2 / VERSION ×1 / README.md ×2 / i18n ×3 各 3」, 负控 `grep -rn '1\.67\.2' **CLAUDE.md** VERSION README.md README.{zh,ja,ko}.md`; 探针 TASK-018 verification[1] = 「主仓 **12** 个版本引用点 (VERSION:24 / README.md:8,:242 / i18n ×3 各 :3,:10,:244) … **CLAUDE.md :139/:141 同步**」(计数 12 但两点点名, 负控不含 CLAUDE.md); 字段 TASK-024 标题「VERSION:24 + README.md 2 点 + i18n ×3 各 3 点」+ verification[0]「**12** 个引用点」+ 负控 `grep … VERSION README.md README.*.md` (**排除 CLAUDE.md**) + verification[3] 只点「项目状态「版本:」行」= `:141` ⇒ **`:139` 无人点名、无人 grep**。实测 `grep -n '1\.67\.2' CLAUDE.md` ⇒ `:139` (`v1.52.0–v1.67.2 已 ship`) 与 `:141` 两行; 发布先例 `086ee32` commit message 逐字含 `CLAUDE.md:139/:141`, `--stat` 显示 `CLAUDE.md \| 4 ++--` = 2 行。**无机械兜底**: `.aria/state-checks.yaml:104-113` 的 `m6-claude-md-version` 只判 `(?<=\*\*版本\*\*: )` 是否 `2.0.0` (方法论版本), `main-project-version-consistency` 只管 `主项目 v…` ⇒ 字段 Spec 先 ship 时 `:139` 静默陈旧。另: 字段 tasks.md `5.5` 整行不含 `CLAUDE.md` (yaml 与 tasks.md 不同步); 探针对账表自述「deliverables (**13 项**)」而实测 12 项。**处方**: 字段 TASK-024 标题/verification 口径 12 → **14**, 点名 `:139` 与 `:141` 两处, 负控 grep 加 `CLAUDE.md`, tasks.md `5.5` 同步; 探针计数句 12 → 14 (它已点名两处, 只是数没算进去) | 残留 (`95f02272` partial) |
| `a7311d2e` | minor | implementation | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | risk | **TASK-018 新加的两分支 verification 把分支判据的输入挂在 TASK-002 上, 而 TASK-002 不产生这个输入。** 证据: TASK-018 verification[3] 逐字「(i) **TASK-002 记录**字段 Spec 的 spec-drafter hunk A (字段必填声明) / hunk B (:127-162 Level 2 预览围栏) **已 ship** ⇒ …」; 实读 TASK-002 的五条 verification: 只断言 `linked_issue_field_probe.py` 存在 + `--emit-arg` 输出 + `lib.linked_issue_field` 可 import + `sibling_spec_probe.py` 存在 + 记录 live 分支 —— **零处涉及 `spec-drafter/SKILL.md` 的 hunk A/B**。「脚本存在」≠「SKILL.md 两 hunk 已落」(字段 Spec 里它们是 TASK-008/009 与 TASK-014/015 两组不同任务)。memory `verify_predicate_inputs_exist` 的形状: 逻辑对了, 它要判的输入没人生成。**处方**: TASK-018 (i) 的判据改为自查 (`grep -n '前置: REQUIRE claim' aria/skills/spec-drafter/SKILL.md` + 字段 hunk 的锚点串), 或 TASK-002 verification 补一条「记录 `spec-drafter/SKILL.md` 是否已含字段 Spec 的 hunk A/B (grep 锚点串)」 | **fix 引入** |
| `7904cede` | minor | testing | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | issue | **TASK-018 把幂等谓词的坏臂委派给 TASK-035, 而 TASK-035 的 SC 映射里没有这个臂。** 证据: TASK-018 verification[4] 逐字「正常委派路径 … 幂等谓词使只写一条 claim: **由 TASK-035 fixture (a) 的「一次 A.1 两条 claim」坏臂验**」; 实读 TASK-035 verification[2] 的逐条映射 = 「(a) ⇒ SC-9 (A)(B) + SC-12 两臂 + SC-14(b); (b) ⇒ SC-11 …; (c) ⇒ SC-25 ②; (e) ⇒ SC-26」—— **无一条是幂等/两条 claim**; proposal `:534` 的点名行为 (a) 亦只含「必调 phase1_gate / 两阶段 `--linked-issue` / 拼串 / release 义务」。真正的宿主在 proposal `:612` SC-22 ③ 逐字「**缺 ③ 的实现 (一次 A.1 写两条 claim + 两次外向推送) 也必红**」= TASK-025 (TASK-018 已依赖它)。⇒ 委派指向了不做这件事的任务 (memory `delegate-verify`)。**处方**: TASK-018 verification[4] 的宿主改为 TASK-025 (SC-22 ③), 或在 TASK-035 (a) 的 expectations 里真加那个坏臂并同步其 SC 映射行 | 残留 (R1 未报) |
| `d5dd27b8` | minor | testing | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | risk | **本轮新写的 eval id 规则与同任务里旧有的 id 字面量并存 —— C3 治了版本号字面量, 没治同一形状的 eval id 字面量。** 证据: 字段 TASK-017 标题逐字「spec-drafter.json **新增 eval id 3** (中文臂)」+ verification[0]「eval id 3 prompt (中文)」+ verification[1]「双臂 = **eval id 3** (中文) + eval id 2」; 而同任务 verification[2] (本轮新加) 逐字「新 eval id = 该文件当前 **max(id)+1**, **ship 时读取, 不硬编码**」。三份 Spec 又都成文允许「owner 裁合并一版 ⇒ 由母 Spec 承接」这一分支, 该分支下 AB 任务的先后无任何边约束 ⇒ 母 TASK-035 若先落两 eval, `max(id)+1` = 5 而非 3。实测当前 `spec-drafter.json` `evals` = id 1/2, `selected_count: 2` (字面 3 在**默认**顺序下才成立)。**处方**: 与 `<vNEXT>` 同款处理 —— 标题与 verification[0]/[1] 的 `3` 改 `<eval-id>` 占位并注「= 落地时 max(id)+1, 默认顺序下为 3」 | **fix 引入** (矛盾由新规则句产生; 字面量原有) |
| `90bbf397` | minor | architecture | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | issue | **三份 seam_rules 对同一条 `version.yaml` 义务的适用范围互相不一致。** 证据: 字段 `exports_for_siblings.seam_rules[1]` 逐字「任何改 `ab-suite/*.json` 的任务同批 … 重算 `version.yaml` (**本 Spec: TASK-017**)」—— 括注把范围收到 TASK-017 一个; 而母 `external_dependencies[0].seam_rules[2]` 逐字把 `spec-drafter.json` 的写入方列为「**字段 TASK-016/017** · 本 Spec TASK-035」, 即按母 Spec 的规则 TASK-016 也在义务内。实测字段 TASK-016 deliverables = `ab-suite/spec-drafter.json` + `ab-results/`, **无 `version.yaml`** ⇒ 按母 Spec 的措辞它违规, 按字段 Spec 的措辞它豁免。实质影响小 (TASK-016 只改 eval 2 的 expectations, 计数不变, 且 TASK-017 紧随其后重算), 但这是**同一条跨 Spec 规则在两侧被写成两个范围**, 正是拆 Spec 自造的接缝 (memory `split-makes-seams`)。**处方**: 三份统一为「凡 deliverables 含 `ab-suite/*.json` 的任务同批重算 `version.yaml`; 纯 expectations 修改可重算得同值但仍须跑一次」, 并把字段 TASK-016 加进 deliverables 或在括注里显式豁免并说明理由 | **fix 引入** |

---

## 实测记录

全部命令在 `/home/dev/Aria` 主仓根亲跑 (工作树 HEAD `c120f9e`, `aria` @ `d69091d`, `standards` @ `334c609`; 三份 tasks.md / detailed-tasks.yaml 均 untracked, 无法 `git diff` 出 R1-fix 增量 —— 故「fix 引入」的判定依据是对账表自述的落点 + R1 报告里的逐字引文)。

**1. 三份 yaml 独立机械体检 (不采信对账表, 自写脚本)**

```
=== linked-issue-field-availability tasks=25 meta_total=25 dup=[] dangling=[] cycles=[]
=== sibling-spec-probe               tasks=18 meta_total=18 dup=[] dangling=[] cycles=[]
=== a1-entry-claim-duplicate-work-guard tasks=39 meta_total=39 dup=[] dangling=[] cycles=[]

同 deliverable 多写入方 ⇒ 有向可达 (自写脚本, 不做「只读」排除):
  字段  5 组 (test 文件 6 任务链 / probe.py / SKILL.md / spec-drafter.json / ab-results) 全部 OK
  探针  7 组 (test 文件 7 任务 / script 5 任务 / audit-engine.json / version.yaml / 三份 audit-engine 文档) 全部 OK
  母    21 组, 仅 2 组报 NO-EDGE: phase1_gate.py 与 release_gate.py 的 (TASK-001, TASK-003)
        ⇒ 实读 yaml :127-129 与 :192-193, 两任务对这两个文件的 deliverable 注释均为「# 只读核验:」⇒ 非写入方, 判无问题
  另 docs/handoff/ 4 任务无边 ⇒ 追加型宿主 (目录), 判无问题

前置门可达性 (自写):
  母: 除 TASK-001/002/003/039 外, 全部传递到达 TASK-001 与 TASK-003 (TASK-039 = follow-up 开单, 只需 TASK-003)
  探针: 全部 15 个下游任务传递到达 TASK-001 与 TASK-003
  RED 不依赖 GREEN: 母 Group 6 (025-030) 祖先集 ⊆ {001,003} ∪ Group6 ✅; 探针 G2 (004-009) 祖先集不含 G3/G4 ✅;
                    字段 TG-1 (001-006) 无实现任务祖先 ✅
```

**2. 复跑三份自贴的「机械核验」脚本 (从 tasks.md 提取第一个 ```python 块原样落盘执行)**

| Spec | 声称 | 实跑 | 判定 |
|---|---|---|---|
| 母 | `[a] … 40 对`, `RESULT: PASS`, exit 0 | `[a] … 37 对`, `RESULT: PASS`, exit 0; 唯一差异 = `phase1_gate.py` 写入方少了 `TASK-003` | 结论一致, **计数不可复现** ⇒ `f1cc9ee9` |
| 探针 | 「(e) parallel line ['TASK-001','TASK-002','TASK-003']」/「parent 1:1 → True (18 vs 18)」/「estimated_hours present on all = True」/ `RESULT: PASS` | `(e) parallel line []`, `parent 1:1 … False (18 vs 0)`, `estimated_hours present on all = False`, **`RESULT: FAIL`, exit 1** | 三处 `\\d` 双转义 ⇒ `4802c929`; 用正确正则复核 parents == md_ids **True (18 vs 18)** |
| 字段 | 28 对 SC + 12 对 flag 全命中, `RESULT: PASS` | 逐字复现: 同文件对 23 全有边 / 覆盖表 28 对缺 token `[]` / flag 12 对缺字面 `[]` / parent 1:1 True / `RESULT: PASS`, exit 0 | ✅ 完全复现 |

**3. 发布链宿主扫描 (支撑 `3221f943`)**

```python
# 扫三份 yaml 的 verification, 找含「双推 / push github / push origin」的任务
母:   [('TASK-024', 'standards/conventions/session-handoff.md §2.3.8 …')]      ← 只有 standards
字段: [('TASK-022', 'aria 子模块本地 merge → master + 双推 + 逐 remote ls-remote 核验 + tag'),
       ('TASK-023', 'standards 子模块本地 merge → master + 双推 + ls-remote 核验 + 主仓 gitlink bump')]
探针: [('TASK-018', '发布同步面 (aria 子模块): … + 主仓 gitlink + 双推逐 remote 核验')]
```

母 Spec 发布链实读: TASK-037 (aria 五文件 bump, deps = 24 个上游) → TASK-038 (主仓面, deps = [TASK-037]); 二者之间无任务。

**4. 发布同步面口径 (支撑 `95f02272`)**

```
git log -1 --format=%s 086ee32
  ⇒ chore(release): aria-plugin v1.67.2 发布同步面 — gitlink 58a49e7→d69091d + 14 版本字符串点
    (CLAUDE.md:139/:141, VERSION:24, README.md:8/:242, i18n ×3 各 badge/Plugin Version/translated-from)
git show --stat --format="" 086ee32
  ⇒ CLAUDE.md 4 ++-- / README.ja.md 6 / README.ko.md 6 / README.zh.md 6 / README.md 4 / VERSION 2 / aria 2   (7 文件)
grep -n '1\.67\.2' CLAUDE.md ⇒ :139 (v1.52.0–v1.67.2 已 ship) · :141 (插件 aria-plugin v1.67.2)
.aria/state-checks.yaml :104-113 m6-claude-md-version  ⇒ 只判 `**版本**: 2.0.0`, 与插件版本无关
.aria/state-checks.yaml :88-102  m6-version-badge-match ⇒ 读 README.md badge vs plugin.json
三份口径: 母「14 处」(负控 grep 含 CLAUDE.md) / 探针「12 个 + CLAUDE.md :139/:141 同步」/ 字段「12 个」(负控不含 CLAUDE.md, 只点「版本:」行)
```

**5. AB 套件基线 (三份的重算口径都指向它)**

```
ls aria-plugin-benchmarks/ab-suite/*.json | wc -l      ⇒ 31
sum(len(evals))                                        ⇒ 73
version.yaml                                           ⇒ 1.1.0 / skills_covered 29 / total_eval_cases 58   (仍漂 2 / 15, 由首个 ship 的 Spec 拉回)
spec-drafter.json                                      ⇒ evals id [1, 2], selected_count 2
state-scanner.json                                     ⇒ evals id [1..12]  (母 TASK-033 的「d69091d 时为 13」成立)
```

**6. 镜头 3 (跨 Spec 传递链) 的两个疑点 — 均判无问题, 存证**

- **探针 TASK-004 ← TASK-003 (AB 套件先于任何测试)**: 不是不合理前置。`sibling-spec-probe/proposal.md:473` 逐字「该任务未 done 则 **Phase B.1 不得开始**」+「A.2 任务清单的一条显式验收项」⇒ 把它编码成 B.2 首任务 (TASK-004) 的边是忠实派生, 其余 14 个任务经 TASK-004 传递到达。另: TASK-003 的验收只钉「文件建成 + 结构 + expectations 字面」, 把 proposal 同句要求的「两 eval 在坏实现上必红」推到 TASK-017 —— 该拆分已在 `a2_discretions (h)` + TASK-003 notes + tasks.md 待 owner #2 三处显式留痕上呈, 不是自判豁免 ⇒ 不报 finding。
- **母第 6 组 (RED) ← TASK-001/003**: 六条边实测在位且第 6 组祖先集不含第 5 组; 第 5 组七条各含对应第 6 组直接边 (017←025 / 018←025 / 019←026 / 020←030 / 021←028+030 / 022←027 / 023←029), 各 `verification[0]` 逐条与其 RED 任务对得上 (逐条实读, 无错指)。翻转后新性质: 任何回指都会成环 ⇒ 倒置从「静默可执行」变成结构性报错, 是净改进。

**7. 过度串行 (镜头 2 的 minor 项) — 逐条看过, 不报**

探针 TASK-016 ← TASK-015 (SKILL.md+report-format.md ← execution-modes.md, 不同文件) / 母 TASK-021 ← TASK-020 / 母 TASK-017 ← TASK-022 / 字段 TASK-018 ← TASK-017: 四处都是不同文件被串起来, 但四处都有内容依赖 (后者引用前者落的契约节 / config key / 同一 RESULT.md), 且都由同一 agent 域承担 ⇒ 属合理保守, 不构成 finding。字段 `{TASK-022 ‖ TASK-023}` 并行两个子模块合并, deliverables 是两个不同 gitlink, 但 TASK-022 notes 明写两者「落**同一个主仓 commit**」—— 文件级不碰撞、提交级需协调, 已由 notes 点明, 判可接受。

**8. 三份 seam_rules 逐条对照 (三种命名下)**

| 条款 | 字段 `exports_for_siblings.seam_rules` | 探针 `ab_suite_seam_rules` | 母 `external_dependencies[0].seam_rules` |
|---|---|---|---|
| placeholder 同批改 | [0] 有 (取值命令 + 两侧宿主点名) | `seams_pinned_by_this_spec[1]` 有 (同源, 同批改) | — (非其接缝) |
| version.yaml 程序化重算 | [1] 有, **范围括注「本 Spec: TASK-017」** | [0] 有, 无范围括注 | [2] 有, 无范围括注 | 
| eval id = max+1 | [1] 有 (先 ship 取 3, 母顺延) | [1] 有 (逐字同款) | [2] 有 (逐字同款) |
| hunk 不相邻 = 义务非事实 | TASK-014 verification 两分支 | — | [1] 义务式 + TASK-018 两分支 |

⇒ 三处 id 约定与重算义务实质一致, **唯一不一致是重算义务的适用范围** (`90bbf397`)。

---

## Verdict

**PASS_WITH_WARNINGS** — 0 critical / 3 major / 6 minor。

R1 的两条 critical 与六条 major 已实证闭合 (11 closed / 1 partial / 0 not_addressed), 依赖图的三条统一规则 (同文件串行 / RED 先于 GREEN / 前置在上游) 我用独立脚本复核**全部成立**, 语义倒置与不合理前置零发现。

但本轮 9 条 finding 里 **6 条 (67%)、3 条 major 里 2 条 (67%) 由本轮 fix 引入**, 形状高度一致: **边改对了, 描述边的散文 (`execution_order`)、证明边的脚本 (机械核验段)、引用边的委派句 (TASK-018 两处) 没跟上**。按 memory `marginal-return-negative` 的判据 (fix 引入占比 > 1/2 即到拐点) 与 `stop-adding-rounds` (换新鲜眼睛 > 加轮), **我不建议开第三轮五席**: 三条 major 每条都配了一行可复跑的判定命令, 定点修 + 主控复跑三段脚本 (母/探针/字段) 即可自验; 若主控要再上一轮, 建议只上**一席新鲜眼睛**审「fix 引入」那 6 条所在的三个新表面, 不重复本轮已核的依赖图与语义接缝。

给 owner 的决策项仍挂着 (R1 提出、本轮未变): **三份是否合并为一次 MINOR 发版**。合并后 `d5dd27b8` (eval id 字面) 与 `3221f943` (三条 aria 合并/双推腿) 的表面各减三分之二。

## Vote

**PASS**
