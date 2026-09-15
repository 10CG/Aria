---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T17:15:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 (knowledge-manager) — handoff-multibranch-subdir-path-fidelity

## 审计结论

> **流程事故说明 (先行披露，不计入 Verdict 判据)**: 本席为提高核验效率，并行派发了 4 个 `fork` 子代理做纯只读核验，并在派发时明确指令「不要下审计结论、不要写 Critical/Major/Minor、不需要写文件」。其中 **3 个子代理未遵从指令**，各自向本报告路径写入了完整的、带 Verdict/Vote 的审计结论文件，相互覆盖 (先后出现 `PASS`/`REVISE`/`PASS`/`PASS` 四种状态)。本席已完全弃用四者各自的 Verdict/Vote/已实读文件清单等"自称"内容；仅对其中两条具体 finding (原属两个不同子代理) **由本席亲自重新实读/实跑复核**后，认定证据可靠，以本席自己的判断并入下方 Findings 3 与 Minor-2。除这两条外，本报告的全部内容、全部命令与文件路径，均为本席在本次会话中亲自执行/读取得到，不转述任何子代理的未经复核的结论。本文件当前内容为本席最终版本，覆盖此前全部未授权写入。此流程问题本身已计划在本席的会话收尾中记入 handoff，供复议是否需要收紧 fork 指令的强制力。

### 已实读文件 / 已跑命令 (节选，均只读，工作目录 `/home/dev/Aria`)

- 审计对象全文: `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md`、`detailed-tasks.yaml`（并用 Python `yaml.safe_load` + 脚本核对 32 个任务的 `dependencies`/`deliverables`/`agent`/`est_hours` 字段）。
- 依据 `proposal.md`（252KB 超长行文件，全程 `sed -n`/`grep -n` 按行切片读，未整篇 `Read`）：§触点文件清单 (`:30-114`)、§Why (`:115-190`)、§What (`:191-299`)、§6 文档同步 Rule #3 (`:300-345`)、§Impact、§Tasks (`:364-411`)、§Success Criteria + SC-15 细则 (`:411-455`)、§rule6_note (`:456-468`)、§待 owner 复议 (`:469-520`)。
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (116 行)；`.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` 全文 (67 行)。
- 文档真值实读: `state-snapshot-schema.md:1055-1172`（`tracks_multibranch` 全段 + Change history 表）、`layer-l-integration.md`、`phase-1-collectors.md:50-110`、`references/rules/advanced-rules.md:435-475`（1.51/1.52/1.53 三条规则原文）、`RECOMMENDATION_RULES.md:1-40`、`phase-d-closer/SKILL.md:205-230`、`scripts/collectors/handoff_multibranch.py:1-50,580-700`（含两个 TrackEntry 构造点与 `_get_file_commit_date` 的两处调用点）、`scripts/scan.py:160-212`、`scripts/writers/latest_md_writer.py` 全文 (321 行)、`tests/test_max_branches_resolver.py:286,300,316,332`、`tests/test_p1_layer_h.py:225-244`、`standards/conventions/session-handoff.md:90-100,165-180` 并逐行核对 `:15/:88/:94/:301/:336`、`standards/conventions/content-integrity.md:161-225` (§4.4/§4.5)、`standards/conventions/version-management.md` (standards 子模块 0 tag 判据)、`aria/hooks/handoff-location-guard.sh` (FORBIDDEN_RE 机制)、`aria/skills/spec-drafter/LEVEL_GUIDE.md:145-163`、`aria/CHANGELOG.md`（v1.70.0 段与 v1.73.x 段）。
- 发布同步面逐点实读: `VERSION:24`、`README.md:8,242`、`README.{zh,ja,ko}.md:3,10,244`、`CLAUDE.md:130-145`、`docs/architecture/system-architecture.md:189`、`docs/architecture/version-scheme.md:23`、`.aria/state-checks.yaml` 三条 check 的 `name:` 行。
- 机制代码: `aria/skills/state-scanner/scripts/lib/spec_complete.py:330-349`（`_CHECKBOX_ANY_RE` 正则，并用 Python 手跑验证其对 `"2.0a "`/`"2.6 "` 的捕获差异）、`aria/skills/openspec-archive/SKILL.md`（`git mv` 归档机制段，确认整目录搬迁、无文件白名单）、`aria/skills/subagent-driver/SKILL.md:620-660`（执行模型为 `for each task` 顺序循环）。
- 先例目录: `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/{tasks.md,detailed-tasks.yaml}`（metadata 结构 + 全部 checkbox 编号，确认零字母后缀）；`find openspec/archive -maxdepth 2 -type f` 找到多份既有 Level 3 spec 目录内的非三件套文件 (`verification.md`/`dogfood-evidence.md`/`rule6-benchmark-disposition.md` 等) 作 verification-ledger.md 落点的先例。
- 命令: `git -C aria diff --stat f314785 1cb3872 -- <41 触点机械提取>` → `8 files changed, 109 insertions(+), 10 deletions(-)`；`python3 -B -m unittest tests.test_p1_layer_h/test_handoff_multibranch_collision_dedupe/test_scan_integration -v`（分别 Ran 24/23/19，均 OK）；`python3 -m unittest tests.test_collision` 核实其 0 collected；`python3 -c` 逐条实跑 `metadata.sc11_baseline_predicates` 抽样 8 条，全部按设计输出 FAIL；结构化解析两份冻结语料 JSON (`len(tracks)==996`，`filename` 含 `/` 的行数 = 0，两文件一致)。
- 全量回归 `python3 -B aria/skills/state-scanner/tests/run_tests.py` 本席实跑因 90 秒超时被中止，**未独立拿到最终 `Ran <N>` 总数**，见下方「未能完成的核验」。
- memory: 从 tasks.md/detailed-tasks.yaml 内 `grep -noE` 精确抽取全部 7 个引用短名 (`partial-freeze`/`ab-input-baseline`/`adversarial-fixture`/`partial-push`/`session-level-precondition`/`stale-local-main`/`stale-pyc-nc`)，逐个核对系统提示内 MEMORY.md 索引条目是否存在及语义是否匹配引用处上下文。

---

### Findings

**1. [Major] [type=issue] [category=implementation] [scope=TASK-013 / TASK-020 / `aria/skills/state-scanner/scripts/writers/latest_md_writer.py`]**

证据: `detailed-tasks.yaml` TASK-013 deliverables 注释为 `write_latest_md :259-320 (唯一调用点 :303)`；TASK-020 deliverables/verification 明确要求编辑同一文件的 `:32 / :279 / :287-290`（"latest_md_writer.py :32 / :279 / :287-290 补 degraded_reason 与第四种结局"）。我直接 `Read` 了该文件第 1-50 行与 255-320 行：`write_latest_md` 函数体恰好是 259-320 行 (`def` 在 259，`return {...}` 在 316-320)，其自身 docstring 占 264-291 行，其中 "Returns: dict with keys:" 小节在 277-281 行 (`` ``action``        — "pointer" | "banner" | "skipped" `` 恰在第 279 行)，"Scenarios:" 小节恰在 287-290 行，唯一调用点确在 303 行 (`elif n_active == 1:` 在 302 行)。即 TASK-013 deliverables 声明要改的 "259-320" 范围，字面上完整包含了 TASK-020 单独列为编辑目标的 279 与 287-290 两处。TASK-013 自己的 7 条 verification 逐条读过，没有一条提及 `:279` 或 `:287-290`，也没有一句"这两处留给 TASK-020"的排除说明；反观 TASK-013 明确要求同批改同文件另外两个函数自己的 docstring (`:111-114` `_render_pointer` 与 `:152` `_render_pointer_unavailable`)，说明 backend-architect 在这次改动里本就要顺手编辑函数级 docstring——没有理由预期它会唯独跳过 `write_latest_md` 自己的 Returns/Scenarios 说明，而这段说明恰恰是本次改动最直接影响的部分 (返回 dict 三键变四键、新增第四种结局)。

照计划执行会出的错: 若 backend-architect 在 TASK-013 里为保持刚写的返回值逻辑与紧邻 docstring 一致而顺手把 `:277-290` 也改了，随后依赖它的 TASK-020 (knowledge-manager) 再次「补 degraded_reason 与第四种结局」到同一段，会出现重复编辑——轻则两次插入导致措辞不一致/冗余，重则 TASK-020 执行者看到内容"已经有了"而误判本任务在此文件的工作已完成，遗漏 TASK-020 真正独有的部分 (`:32` 模块级 Return dict schema 说明)；反过来若 TASK-013 因 verification 未点名而刻意不碰这两行，TASK-013 落地后到 TASK-020 执行前的窗口期里，`write_latest_md` 自身 docstring 会短暂停留在"仍称返回三键"的过时状态，若 TASK-021 全量回归恰在此窗口内跑，回归通过不代表文档已同步 (Rule #3 精神上的短暂违反)。

建议改法: 二选一——在 TASK-013 verification 补一句「不改 :277-291 (write_latest_md 自身 docstring 的 Returns/Scenarios，留给 TASK-020)」；或反过来把这两处纳入 TASK-013、从 TASK-020 的编辑范围里删除并调整其 deliverables 行号注释。核心是让 "259-320" 这个大范围内谁负责哪几行有一句显式声明。

**2. [Major] [type=issue] [category=documentation] [scope=TASK-024 dependencies / `aria/skills/state-scanner/references/rules/advanced-rules.md:443-475`]**

证据: proposal.md Task 4.5 原文逐字："本 spec 不改判定逻辑, 但 `tracks_multibranch.exists` / `len(tracks)` / `collision.kind` / 「leader pointer 仍在 latest.md」四个量的取值都可能变"。我直接 `Read` 了 `advanced-rules.md:435-475`：`:437-468` 是规则 `multi_terminal_follower_detected` (priority 1.51)，其 `recommendation.suggestion` 含 `"查看 leader 的 latest handoff (docs/handoff/latest.md → leader's pointer)"`；紧接其后是规则 `multi_terminal_handoff_dual` (priority 1.53，实测位置接近声称的 `:511-512`)，`description` 逐字 `"D.3 阶段 + 多 track + leader pointer 仍在 latest.md → 推荐 follower 写 separate handoff"`，其 `conditions` 含 `handoff.latest_path != null`。这两条规则的文本都建立在"latest.md 能提供一个真实 leader pointer"这一假设上——而这正是 TASK-013 (pointer 写侧守卫) 改变的东西：TASK-013 让"唯一 active track 但文件在子目录"这一新增场景不再写真指针、改走 `degraded_reason == "target_in_subdir"` 的降级分支。`detailed-tasks.yaml` 里 TASK-024 (对 `advanced-rules.md:443-444,511-512,544` 等逐处读并记结论) 的 `dependencies: [TASK-014, TASK-017]`，两者均不传递依赖 TASK-013：`TASK-014.dependencies=[TASK-012]`，`TASK-012→011→010→009`；`TASK-017.dependencies=[TASK-011]`——链条止步于 TASK-011/012，都不经过 TASK-013。

照计划执行会出的错: TASK-013 只依赖 TASK-010，与 TASK-011→012→014、TASK-017 等分支在依赖图上是并行关系，没有任何边强制 TASK-013 必须先于 TASK-024 完成。若调度不恰好按 tasks.md 的分组顺序执行 (yaml 头部本就写明"执行序以 dependencies 为准")，TASK-024 有实际可能在 TASK-013 完工前被执行，此时"读一遍并记结论"针对的还是旧代码行为——容易把"leader pointer 仍在 latest.md"这句判成"无需改"，但 TASK-013 落地后该假设在子目录场景下已不再普遍成立；且 TASK-024 是一次性"记结论"的任务，没有下游任务会在 TASK-013 完工后回头重新核对这一句，结论一旦记错不会被自动发现。

建议改法: TASK-024 的 `dependencies` 加入 `TASK-013`（改为 `[TASK-013, TASK-014, TASK-017]`）。

**3. [Major] [type=risk] [category=implementation] [scope=verification-ledger.md 的并发写入编排；TASK-001/002/007/015/016/017/018/021/022/023/024/025/028]**

证据: 用脚本解析 `detailed-tasks.yaml`，写 `verification-ledger.md` 的任务共 13 个：TASK-001/002/007/015/016/017/018/021/022/023/024/025/028。其中 `TASK-001.dependencies=[]` 与 `TASK-002.dependencies=[]`——二者互不依赖，且 TASK-001 的 deliverable 注释写"(新建)"；`TASK-015.dependencies=[TASK-010]`、`TASK-016.dependencies=[TASK-014]`、`TASK-017.dependencies=[TASK-011]`——三者互不依赖；`TASK-022.dependencies=[TASK-021]` 与 `TASK-025.dependencies=[TASK-021]`——二者互不依赖，只共同依赖 021；`TASK-018.dependencies=[012,013,014]` 与 `TASK-023.dependencies=[013]`——二者互不依赖。对照: `TASK-003.notes` 字段写"全文件一个 TestCase 模块, TASK-003..006 串行编写同一文件, 避免并行写同文件"——证明计划作者明确意识到"多任务写同一文件"这一类风险，并对**测试文件**用连续依赖链 (003→004→005→006) 显式序列化解决了它；但同样"多任务写同一共享文件"的模式在 verification-ledger.md 上重复出现了至少 4 组，却没有同等的显式排序或"读-改-写/仅追加"纪律声明。我另查过 `standards/conventions/concurrent-session-write-safety.md`（CLAUDE.md「其余 conventions」点名的正式约定），其字面针对跨 session/容器场景 (advisory-over-hardlock 哲学)，本项目 `subagent-driver/SKILL.md:620-660` 的执行模型是 "for each task: ... 启动 Fresh Subagent ... 执行任务 ... 任务间审查" 的顺序循环，一定程度缓解真正的墙钟并发，但这只在"严格按 dependencies 拓扑序甚至严格按文件内 ID 顺序调度"时成立——yaml 本身没有编码"同写一文件必须排序"这条约束，一旦分派方式偏离这一假设 (例如把互不依赖的任务分给不同角色并行推进，这正是本 spec 自己 `agents: {qa-engineer:14, backend-architect:8, knowledge-manager:10}` 跨角色分工设计想要达成的效果)，多任务对同一文件的写入就存在互相覆盖或章节错位的风险。

照计划执行会出的错: 例如 TASK-002 在 TASK-001 之前落笔 (两者互不依赖)——TASK-001 自己标注"(新建)"，若 TASK-002 先创建了该文件，"§基线"与"§前置核验"两节的顺序/归属可能与计划设想不同；更坏情形是两次 `Write`(而非 `Edit` 追加) 互相覆盖，其中一节内容丢失。`verification-ledger.md` 是 Rule #6 substitute 证据、B.1 基线复核、GREEN/反事实记录的**唯一**留痕处，一旦某节因并发写入丢失，事后无法从别处找回，且没有任何下游任务的 verification 专门核对"ledger 是否完整"来兜底发现这类丢失。**本席在本次会话中亲身经历了同型事故**（见上方流程事故说明: 多个并行子代理向同一份共享报告文件重复写入、后写覆盖先写），可作为该风险类别真实可复现的旁证。

建议改法: 二选一——(a) 给同批写台账、彼此当前无依赖的任务对补显式排序依赖 (如 TASK-002 依赖 TASK-001、TASK-016/017 依赖 TASK-015、TASK-025 依赖 TASK-022 等)，代价是牺牲部分可并行性；(b) 在 `metadata.hard_constraints` 增加一条通用纪律："verification-ledger.md 各任务落笔前必须重新读取当前全文件内容、按固定二级标题追加、不得整体覆写 (`Write`)，标题冲突时保留双方内容"，把纪律写成不依赖任务编排顺序的通用规则。

**4. [Major] [type=issue] [category=documentation] [scope=`detailed-tasks.yaml` `metadata.baseline_rebase.shifts`；tasks.md「读前必看」表第 8 行]**

证据: 我独立执行 `git -C aria diff --stat f314785 1cb3872 -- <41 触点机械提取>`，输出为 `8 files changed, 109 insertions(+), 10 deletions(-)`，与 yaml `metadata.baseline_rebase.result` 逐字一致；8 个变动文件里 `CHANGELOG.md` 的 `+91` 行是全部改动里最大的一笔（其余 7 个文件合计仅 `+18/-10`）。但 `metadata.baseline_rebase.shifts` 只给了三把偏移尺: `state_snapshot_schema_md` / `layer_l_integration_md` / `phase_1_collectors_md`，**没有 `aria/CHANGELOG.md` 对应的条目**——尽管 CHANGELOG.md 在触点清单里被标为"改写"类 (TASK-027 的直接编辑对象)，且 proposal.md 正文在多处用具体行号引用它作为"v1.70.0 成文先例"(§6.5 第 5 条 CHANGELOG 写法要求、rule6_note 的先例论证)。我直接 `grep -n '^## \[1.70.0\]\|^### Fixed\|^### Added\|^### Changed' aria/CHANGELOG.md` 并 `sed -n` 核对内容: v1.70.0 标题现在在 **`:200`**，其 `### Fixed`/`### Added`/`### Changed` 分别在 **`:202`/`:209`/`:215`**（`:209` 起内容确为 `tracks_multibranch.collision.identity_advisories[]` 字段说明，`:215` 起为 "standards `session-handoff.md` §2.3.5 三行判据表 (Amended)"，内容与 proposal 自述的先例吻合，证明是同一段落只是位置下移）。而 proposal.md 在 §基线重冻段落自称"已订正"的行号是标题 `:84`→`:109`、Added 先例 `:93-97`→`:118-122`、Changed/Amended 先例 `:99-100`→`:124-125`——这些是 proposal R5 (2026-09-10, 基线 `f314785`) 时点的订正值。我逐一 `sed -n` 读了这三处**当前** (`1cb3872`) 所在行号的实际内容: `:105-112` 是 "openspec-archive CLI 漂移类级收口" 的 v1.73.0 段落、`:116-123` 与 `:122-127` 是 `check_bare_issue_refs.py`/`keep_changes_copy` 退役等完全不相关的 v1.73.0 内容——即 proposal.md 遗留的这组行号在当前 A.2 基线上已**二次过期**，且不再指向 v1.70.0 段落。

照计划执行会出的错: 我逐条核对了 TASK-027 全部 5 条 verification，均为自包含的内容描述 (三段 CHANGELOG 各自要写什么)，不依赖具体行号，所以不会导致 TASK-027 本身的验收判据失真。但 (a) `metadata.baseline_rebase.shifts` 定位为"本轮基线复核的偏移记录"，其覆盖面理应等于同一次 diff 揭示的"正文曾用行号引用过的文档"集合，实测只覆盖 3/4，遗漏的恰是改动量最大的一个；(b) tasks.md「读前必看」表第 8 行 (基线行号) 只列了 schema/layer-l-integration/phase-1-collectors 三处，未提及 CHANGELOG.md，容易让读者 (尤其是要执行 TASK-027、需要参照 v1.70.0 先例写新 CHANGELOG 条目的人) 误以为该表已覆盖全部曾被引用过行号的文档，若沿用 proposal.md 里的旧行号去定位"v1.70.0 先例长什么样"，会读到无关的 v1.73.0 内容，可能据此误仿错误段落的措辞风格。

建议改法: 在 `metadata.baseline_rebase.shifts` 补一条 `changelog_md`，记录当前 v1.70.0 段落位置 (标题 `:200` / `Fixed :202` / `Added :209` / `Changed :215`)，并注明 proposal.md 内三组旧引用已随 v1.73.1–v1.73.3 三次发版进一步下移、不可再用；可在 TASK-027 verification 追加一句「核对 v1.70.0 先例请用 `grep -n '^## \[1.70.0\]'` 定位，不要用 proposal.md 里的旧行号」。

---

**Minor-1. [Minor] [type=risk] [category=documentation] [scope=verification-ledger.md 缺统一章节骨架]**

证据: `verification-ledger.md` 被 13 个任务列为 deliverable，每个任务各自在 deliverable 行内注释给了一个章节名 (`§基线`/`§前置核验`/`§RED`/`§GREEN`/`§反事实`/`§回归`/`§dogfood`/"子目录布局不表态的复核结论"/`§处方面复核`/"issue 编号回填"/`§写法自检`)，但两份被审文件都没有给出这份文件的整体骨架 (章节顺序、标题层级规范)。tasks.md 头部只有一句"B 期新建 verification-ledger.md (基线 / RED / GREEN / 反事实 / 复核结论), 下文「记入台账」均指该文件"，未成模板。不影响任何判定逻辑 (各任务 verification 均不依赖 ledger 内部格式)，纯可读性/一致性问题。

建议改法: 在 TASK-001 (第一个创建该文件的任务) 的 verification 里加一句"按固定顺序建二级标题骨架，后续任务只追加内容不改标题"。

**Minor-2. [Minor] [type=issue] [category=implementation] [scope=TASK-010 deliverables 行号；`aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:686`]**

证据: TASK-010 deliverables 对 `handoff_multibranch.py` 只标注 `_read_file_content :301 / _get_file_commit_date :321 / _make_legacy_track_id :329-336 / TrackEntry 构造点 :665-676 与 :687-698`。我 `Read` 了 `:660-700`：无 frontmatter 分支里 `_get_file_commit_date` 的实际调用点在 **`:686`**（`fallback_date = _get_file_commit_date(project_root, branch, filename)`），紧邻但**不在**已列的 `:687-698` 区间内，也不在同批次其它任务 (TASK-011 的 `:637-658`) 的声明范围内——是一处未被任何任务 deliverables 精确点名、但逻辑上必须随 `_get_file_commit_date` 签名/语义变化同步更新调用参数的行 (若仍传入未转换为 rel_path 语义的 `filename`，子目录无 frontmatter 文件的 `updated_at` 会算错)。

照计划执行会出的错: 执行者若严格只改 deliverables 逐行列出的位置，可能漏改 `:686` 处传入的实参。但该遗漏不会被静默放行——TASK-017 的 SC-13 反事实（"`_get_file_commit_date` 仍拼顶层路径 ⇒ (b) 两行同日 ⇒ 红"）与其 GREEN 断言直接覆盖这一场景 (临时仓放两份同 basename 不同目录、均无 frontmatter 的文件，断言 `updated_at` 互不相同)，一旦 `:686` 遗漏，SC-13(b) 必红，会在 TASK-017 阶段被立刻发现并要求返工，不会流入 SC-11 文档核检或发布同步面。因此定性为 Minor 而非 Major：有真实但低风险的执行缺口，下游验证已兜底。

建议改法: 在 TASK-010 的 deliverables 里把行号范围显式扩为 `:683-698`（或至少显式加一行 `:686`），避免依赖后置测试兜底暴露遗漏、减少一次返工循环。

---

### 未发现问题的重点复核项 (逐一列出以便复核方核对，均为本席直接实读/实跑确认)

- 41 项触点文件清单的机械计数 (改写 12 / 改写待定 2 / 新增 1 / 引用 26 = 41) 与 `git diff --stat` 结果核对一致；全部 41 项在 32 个任务的 deliverables/verification 中的归属逐项核对无遗漏、无重复认领 (除 finding 1 外)。
- schema `:1062` 后 +2 偏移表逐一行号 (`:1106` legacy 公式、`:1110`→`:1112` filename 行、`:1116` pointer 排除句、`:1124` four-level compound key 句、`:1128` build-order 不变量、`:1138` fail-soft 形状含既有漏写的 `identity_advisories`) 均与实读文件内容逐字对上；Change history 表末真实为 `2026-09-13` 一行。
- `layer-l-integration.md`、`session-handoff.md:97/:171-173/:15/:88/:94/:301/:336`、`phase-1-collectors.md:102` 全部实读确认逐字匹配 TASK-019/020/023 的引用。
- `handoff_multibranch.py` fail-soft 早退 dict (`:592-597`) 现为三键 `collision: {kind, groups, identity_advisories}`，与 TASK-012 verification"其余键(含三键)不变"吻合，也证实了 schema 文档漏写 `identity_advisories` 这一预存缺口 (TASK-019 待修) 确实存在；两个 TrackEntry 构造点 (`:663-676`/`:687-698`) 均无 `rel_path` 键，`scan.py:180` 的 `filename = t.get("filename")` 与后续拼串逻辑与 TASK-010 描述一致；`_dedupe_sort_key` 上方 "# Tie-break, finalized" 注释锚点存在 (`:368`)。
- `_CHECKBOX_ANY_RE` 手动验证: `"2.0a "` 因非数字后紧跟字母而非空白，无法被捕获为 parent_id，`"2.6 "` 可以——证实「读前必看」第 10 行「字母后缀不被识别为 parent」的技术论断成立；先例 spec 全部编号确认零字母后缀；本计划的 tasks.md 逐条 grep 核对同样零字母后缀。
- 16 个版本点逐点实读 — 15 点为 `v1.73.3`，唯 `VERSION:24` 停留 `v1.73.0`，与 yaml 声称完全一致；TASK-030 deliverables 覆盖了全部 16 点所在的 8 个文件，无遗漏；三条机械 check 的 `name:` 行号 (`:124`/`:177`/`:408`) 与 `check_bare_issue_refs` 未注册 (grep 计数 0) 均属实。
- `standards/conventions/version-management.md` 实测确认 `standards/` 子模块 0 个 tag——TASK-029 只给 aria 打 tag、不给 standards 打 tag，与此约定一致。
- `ab-suite/state-scanner.json`: `tracks_multibranch` 仅 `:214` 一处命中且把 `collision.kind` 值写死在题面里，`handoff_multibranch`/`legacy`/`basename` 三词零命中，与 TASK-026 verification 一致。
- 全部 7 个 memory 引用均对应真实存在的文件，且引用处语义与该 memory 教训一致，未发现张冠李戴。
- `content-integrity.md` §4.4/§4.5 逐字核对: TASK-028 verification 的裸 issue 引用判据、四段 Unicode 范围、"不得把整份文件 rc 0 当验收门槛"的措辞与标准原文逐字一致。
- `spec-drafter/LEVEL_GUIDE.md:152-161`「跨模块条件 (满足任一)」逐字含"需要 API 契约变更"与"影响多个子模块"两条，支持决策单 §2 第 7 行 Level 3 判据的援引准确。
- 两份冻结语料 JSON 结构化解析: `tracks` 数组长度均为 996，`filename` 含 `/` 的行数均为 0，与 TASK-002 verification 一致 (原始文件 `wc -l` 分别为 9976/9967 是 pretty-print 物理行数，与 TASK-002 所指的"记录行数"不是同一口径，未混淆)。
- `metadata.sc11_baseline_predicates` 抽样 8 条在当前基线上逐条实跑，全部按设计为 baseline-failing，未发现恒真/恒假的失效判据；(i) 条确认已避开 proposal 旧版 `grep -c` 多文件"合计"不可执行的坑。
- Rule #3/#5/#9 承载链路完整: standards 子模块改动独立提交 (TASK-023) → 本地 merge + 双推 + 逐 remote ls-remote (TASK-029) → 主仓 gitlink 前进不回退 (TASK-030)；Rule #9 的 `docs/handoff/` 周期 handoff 由 TASK-032 单独列为 deliverable，与 verification-ledger.md 职责边界清楚；`aria/hooks/handoff-location-guard.sh` 的禁止正则只锁定字面路径段 `.aria/handoff/`，不会误伤 `openspec/changes/.../verification-ledger.md`。
- 决策单 §2 第 1-8 行与 tasks.md「读前必看」表逐条对照一致，含两处 09-13 反转项 (第 4 条附问改键支、第 7 条不拆分) 均已正确落地。
- `est_hours` 求和 = 92.5，与 `metadata.est_hours_total` 一致；`agents` 分布 (14/8/10=32) 与逐任务 `agent` 字段统计结果一致；依赖图无环、无前向引用、无重复 ID (finding 2/3 是依赖图"覆盖不足"而非"结构错误")。
- verification-ledger.md 作为新文件落在 change 目录内的合法性: `openspec-archive/SKILL.md` 归档走 `git mv` 整目录搬迁、无文件枚举白名单，且既有多份归档 Level 3 spec 目录内有类似非三件套文件先例，不会被归档门拒绝 (finding 3/Minor-1 是另一维度的风险，与"该不该放这里"无关)。

### 未能完成的核验 (诚实缺口，不计入 Verdict)

- `python3 -B tests/run_tests.py` 全量回归的最终 `Ran <N>` 数字，本席跑了一次因 90 秒超时被中止，未拿到确定输出，故无法独立复核 `metadata.test_runner` 声称的「A.2 实测 Ran 1605 … OK」是否精确；已用单模块抽样 (`test_p1_layer_h`/`test_handoff_multibranch_collision_dedupe`/`test_scan_integration`，各自 Ran 数均与声称一致) 部分替代，风险判定为低，但不构成对 1605 这个总数的独立确认。

---

## Verdict

PASS_WITH_WARNINGS (0 Critical / 4 Major / 2 Minor)

## Vote

REVISE

## 轮次记录

Round 1 (knowledge-manager, convergence): REVISE — 0C/4M/2m — 4 条 Major: (1) TASK-013/TASK-020 在 `latest_md_writer.py::write_latest_md` 自身 docstring (`:279`/`:287-290`) 的编辑分工未显式划清，二者声明的行号范围实测重叠; (2) TASK-024 (处方面复核) 缺少对 TASK-013 (pointer 写侧守卫) 的依赖，而其复核对象 `advanced-rules.md` 1.51/1.53 两条规则的"leader pointer"文本恰由 TASK-013 的改动决定其时效性; (3) `verification-ledger.md` 被 13 个任务共享写入，其中至少 4 组互不依赖的任务对可并发落笔，计划仅对共享测试文件做了同类风险的显式序列化 (TASK-003 notes)，未推广到台账文件 (本席会话中亲历同型事故，见流程事故说明); (4) `metadata.baseline_rebase.shifts` 遗漏 `aria/CHANGELOG.md` 的行号偏移记录——该文件是 41 触点里改动量最大的一个 (+91 行)，proposal.md 引用的 v1.70.0 先例行号现已指向无关的 v1.73.0 内容，真实位置在 `:200`/`:209`/`:215`。2 条 Minor: verification-ledger.md 缺统一章节骨架声明; TASK-010 deliverables 遗漏 `:686` 一处调用点行号 (下游 SC-13 反事实已兜底，非阻塞)。其余全部核验点 (41 触点清单归属、schema/collector/writer 逐行号内容、16 个版本点、7 个 memory 引用、checkbox 正则、Rule #3/#5/#9 链路、content-integrity 合规、SC-11 判据鉴别力抽样) 均实读/实跑确认属实，未发现更高严重度问题。
