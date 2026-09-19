---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-19T11:45:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — backend-architect

被审对象: v2.2 (主仓 `5fd7e08`, yaml 落在 `12c870d`), R2 五条 Major 的返修稿。视角: 组 2 (`scripts/completeness_gate.py` 实现, tasks.md 2.1–2.6) 对 proposal 的忠实度。

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`(全文 227 行)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`(全文 1675 行, 分块读毕: 1-400 / 400-800 / 800-1200 / 1199-1419 / 1420-1675)。
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `:100-371`(逐段, 含 `§1` 参数定义 / `§1.0` 求值总序 / `§1.1` S1-S4 / `§1.1b` 判定表 / `§1.2` 归属规则 / `§1.2b` 枚举边界 / `§1.3` 三态 / `§1.4` 路由与 16 键契约 / `§2` `§3` `§4` 接线段首部); `grep` 定位并精读 SC-15 全文、SC-21 全文、SC-9 全文(`:465-478` 区间); `grep git_failed` 核对 `--repo-path`/`--diff-repo-path`/`--base`/`--anchor-base` 相关条款(`:89-100`, `:158`, `:385`, `:402`, `:457`, `:478`)。
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`: 标题全扫 + `:76-95`(#199 的 13 条裁定表)精读。
- `.aria/audit-reports/post_planning-R2-2026-09-18T162427-983Z-pre-merge-completeness-gate-change-scope-aggregated.md`(全文 133 行)。
- `aria/skills/config-loader/DEFAULTS.json`(全文, 用 `python3 json.load` 核 `audit` 子块)。
- `aria/skills/config-loader/SKILL.md`: `:270-335`(旧配置兼容层全节)。
- `aria/skills/audit-engine/SKILL.md`: `:47`/`:75`/`:344`/`:362`/`:375-392`/`:418-426`(定位精读)。
- `aria/skills/phase-c-integrator/SKILL.md`: `:50-60`/`:125-136`/`:750-758`。
- `aria/skills/audit-engine/scripts/sibling_spec_probe.py`: `grep` 定位 `:147-151`/`:681-684`(stderr/stdout 分离先例)。
- 实跑核验(均只读, 未做任何 git 写操作): `find aria/skills/config-loader -name '*.py'` (0 个); `completeness_gate.py` / `test_completeness_gate.py` 均不存在; `git -C aria rev-parse HEAD` = `1cb3872`; `git ls-tree -r --name-only refs/aria/coordination` 核对 claim 文件; `git show refs/aria/coordination:claims/023236f2/s-86f7@1836.yaml` 与 `claims/bfe8285d/s-73b9@1606.yaml` 两份原文; `git show -s`/`git diff-tree --no-commit-id --name-only -r` 对 `1b9734a`/`5fe15b0`/`c9fe08f`/`9de3074`/`5d435e9`/`1b6f9ad`/`12c870d`/`5fd7e08` 等提交逐一核实; `git -C standards diff --stat / --shortstat 21748d4 940cb5b` 全仓与逐文件核验; `git ls-files .aria/notes/` 核 `.aria/notes/` 是否为仓库通用惯例。

## Findings

| id | severity | type | category | scope | summary |
|---|---|---|---|---|---|
| `9122f4a9` | major | issue | implementation | `detailed-tasks.yaml metadata.commit_attribution` | `foreign` 优先级吞掉 `exclusive`, 导致混合提交被判得比 `shared-only` 更差 |
| `32076746` | major | issue | implementation | `detailed-tasks.yaml TASK-001` | "基线复核" 未覆盖 `metadata.baseline_rebase.standards`, 与该字段自身的重测义务矛盾 |

### M1 — `9122f4a9`

**一句话**: `commit_attribution` 的单亲提交分类里, "存在任一无法识别的路径 ⇒ 整条判 `foreign`" 的优先级高于 "存在 `exclusive` 路径 ⇒ 判 `own`", 而 `.aria/notes/<topic>/` 这一仓库通用、本轨自己也在用的路径族不在任何识别规则里; 真实提交 `12c870d`(本轨 v2.2 返修提交本身)如果落在未来某次 commit_attribution 的检查范围内, 会被整条判成 `foreign`, 而不是更贴切的 `own` 或至少 `shared-only`。

**证据**:
- `detailed-tasks.yaml:591` `SHARED = {"aria", "VERSION", "README.md", ...}` 不含 `.aria/notes`。
- `detailed-tasks.yaml:597-610` `exclusive(c, p)` 只识别四类路径: `openspec/changes/{SID}/**`、`openspec/archive/*-{SID}/**`、`.aria/audit-reports/**`(且文件名含 SID)、`docs/handoff/*.md`(且 frontmatter `track-id` 等于 SID)。`.aria/notes/**` 不落在任何一类。
- `detailed-tasks.yaml:611-614` `klass(c, p)`: `exclusive(c,p)` 为真 ⇒ `"exclusive"`; 否则 `p in SHARED` ⇒ `"shared"`; 否则 `"foreign"`。
- `detailed-tasks.yaml:622-631` 主循环: `ks = [klass(c, p) for p in <该提交改动的全部路径>]`; `if not ks or "foreign" in ks: kinds.append("foreign")`(第 624 行) — **此判断先于** `elif "exclusive" in ks: kinds.append("own")`(第 625 行)。即: 只要提交里有一个文件的 `klass` 是 `"foreign"`, 整条提交就是 `"foreign"`, 不论其余文件里有没有 `"exclusive"`。
- 实测真提交 `12c870d`(`docs(openspec): 10CG/Aria#199 A.2/A.3 v2.2 — post_planning R2 五条 Major 返修`)改动三个文件: `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py`(生成本 yaml 用的生成器脚本)、`openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`、`openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`。按上述规则逐一分类: 后两者 `exclusive=True`(`openspec/changes/{SID}/` 前缀), `gen_yaml.py` 既不在 `SHARED` 也不满足 `exclusive` 任何一条 ⇒ `klass="foreign"`。三者合入 `ks` 后 `"foreign" in ks` 为真 ⇒ 整条提交判 `"foreign"` — 与真正的第三方提交(如 `9de3074`)同一桶, 而不是 `own` 或 `shared-only`。
- `git ls-files .aria/notes/` 实测: 该目录被 19 个以上不同专题的历史文件占用(如 `2026-05-27-aria-fleet-three-layer-architecture.md`、`2026-08-09-secret-guard-128-owner-decision-queue.md`), 是这个仓库长期、跨轨、被 git 正常追踪的规划笔记惯例, 不是本轨临时误用; 本轨自己新开的子目录 `2026-09-17-199-a2-a3-tooling/` 已含 `README.md`/`gen_yaml.py`/`audit-seat-prompt-template.md`/`r1-seat-prompts/*.md` 多个文件, 后续任何一轮返修(含本轮若判 REVISE 后的 v2.3)如果沿用同一生成器工作流, 再次产出"改 `.aria/notes/.../gen_yaml.py` + 改 `detailed-tasks.yaml`"这种同形提交的概率很高。

**失败场景**: TASK-001(B.1 入口, 对 `origin/master..<起点>` 跑 `commit_attribution`)或 TASK-030(对 `origin/master..<主仓 feature 分支>` 跑)若检查范围内包含一个 `12c870d` 形态的提交(yaml 重新生成时顺带提交了 `.aria/notes/` 下的生成器/模板文件), `commit_attribution` 会把它归为 `"foreign"`, 落入 `owner_gates` 第 16 项"含 foreign / foreign-merge(非本轨提交)"的停机文案(`detailed-tasks.yaml:133`), 把本轨自己确凿无疑的规划产物错误呈报为"非本轨提交"。这不是取不到值或崩溃, 但会把一个应呈报为"良性"的提交, 放进措辞上等同"外来提交"的桶里, 直接误导 owner 在 `owner_gates` 第 2/9/16 项要做的裁定; 且由于 `.aria/notes/` 是本轨已经在用、未来大概率复用的路径, 该误判不是一次性偶发, 而是这套返修工作流下的系统性复发点。

**建议修法**: 在 `exclusive(c, p)` 里补一条 `.aria/notes/**` 的判据(如目录名含 SID 字面或含所引 issue 号), 或在 TASK-001/TASK-030 调用 `commit_attribution` 时把本轨已知的 `.aria/notes/2026-09-17-199-a2-a3-tooling/` 作为 `extra` 参数传入 — `extra` 机制已经存在(`detailed-tasks.yaml:590` 的 `sys.argv[3:]`, TASK-030 已用它传 ab-results 目录), 只是 TASK-001 的调用点(`detailed-tasks.yaml:1053`)没有使用。

### M2 — `32076746`

**一句话**: `metadata.baseline_rebase.standards` 这条断言自己写明"TASK-001 必须对 B.1 当时的 gitlink 重测, 不得沿用本行数值", 但 TASK-001 的"基线复核"验证条目字面上只重测 `aria_zero_diff`/`aria_shifted`/`main_repo` 三个清单, 完全没有提到 `standards`, 计划内部自相矛盾; 而 `standards` 在两天内(`2026-09-17`→`2026-09-19`)已经真实变动过一次, 复发概率不低。

**证据**:
- `detailed-tasks.yaml:78`(`metadata.baseline_rebase.standards` 全文)逐字: "standards 是并发轨随时会动的共享子模块, **TASK-001 必须对 B.1 当时的 gitlink 重测, 不得沿用本行数值**"。
- `detailed-tasks.yaml:1055`(TASK-001 verification 的"基线复核"bullet)逐字: "基线复核: 对 `metadata.baseline_rebase.aria_zero_diff` 的每个文件与 `aria_shifted` 各条冒号前的文件跑 `git -C aria diff --shortstat 301641b <aria 起点> -- <文件>`, 对 `main_repo` 的文件跑 `git diff --shortstat a563192 <主仓起点> -- <文件>`; ……" — 通篇只提 `aria_zero_diff`/`aria_shifted`/`main_repo` 三个清单键名, 未出现 `standards` 字样, TASK-001 的其余 9 条 verification bullet(claim 身份、协调 ref、心跳、分支起点等)里也没有第二处提到 `standards` 的重测。
- 实测 `git -C standards diff --stat 21748d4 940cb5b`: 仅 `conventions/content-integrity.md`(58 行)与 `conventions/skill-benchmark-exemption.md`(24 行)两个文件变动; 逐文件 `--shortstat` 核对四个"零 diff"文件(`openspec/project.md`/`openspec/templates/proposal-minimal.md`/`conventions/configured-gate-authority.md`/`conventions/version-management.md`)输出均为空; `content-integrity.md` 精确为 `+56/-2`, `skill-benchmark-exemption.md` 精确为 `+21/-3` — 与 yaml 断言逐字节吻合(证明 v2.2 落盘这一刻断言是对的), **同时也证明** standards 在 `2026-09-17`(`8b49562`)到 `2026-09-19`(`940cb5b`)两天内已经真实前进过一次(PP2-M4 本身就是这次前进暴露出来的)。
- tasks.md 引用了具体的 standards 行号来支撑论证: `tasks.md:45`(重写 b)引用 `standards/openspec/project.md:117` 作为"Level 2 输出只有 `proposal.md`"的依据。该行号当前(`940cb5b`)有效(已确认此文件在 `21748d4..940cb5b` 零 diff), 但如果 standards 在 B.1 实际执行前又推进(入口本身还卡在 `owner_gates` 第 1 项 / `10CG/Aria#195` 的门, 时间跨度不可控), 该引用可能静默失真, 而计划里没有任何任务会去重新核对它。

**失败场景**: B.1 真正执行时(可能距 v2.2 落盘已有相当天数, 因为入口前置门尚待 `10CG/Aria#195` 完成或 owner 明示改序), `standards` 很可能已经再次推进(参考口径: 两天内已推进一次)。执行者逐字照做 TASK-001 的"基线复核"清单, 不会去碰 standards 的任何文件, 于是带着一份可能已经过期的 `metadata.baseline_rebase.standards` 断言(含 `:117` 这类具体行号引用)直接进入 Phase B, 且计划里没有下一个任务会补做这个检查 —— 直到某处因行号偏移引发的问题在无关场景里暴露, 才会被事后发现, 而不是在 B.1 当场拦下。这正是执笔人自报薄弱点 (b) 描述的"没有为这类冻结断言加机械守卫", 但不是一个尚待验证的风险描述, 而是可以直接在 TASK-001 verification 清单里指出的具体遗漏。

**建议修法**: 在 TASK-001 的"基线复核"bullet 里, 对 standards 补一条与 aria/main_repo 对称的重测步骤 —— 对四个"零 diff"文件与 `content-integrity.md`/`skill-benchmark-exemption.md` 跑 `git -C standards diff --shortstat 21748d4 <B.1 当时 gitlink> -- <文件>`, 与 v2.2 记录比对, 新出现 diff 的文件同样记偏移表。

## R2 对账

| 编号 | 判定 | 证据 |
|---|---|---|
| PP2-M1 | **closed** | `detailed-tasks.yaml:1048`(TASK-001 verification 第 2 条)已改为按 `(本容器, 归一 track_id, active)` 三元组运行时解析, 按 `status` 分流覆盖 0 条 active(含 `done`/`yielded`/`abandoned`/无claim 四种)与 2 条及以上 active 两端; `owner_gates` 第 14 项(`detailed-tasks.yaml:131`)的触发条件已从"只认 `abandoned`"扩为"解析到 `done`/`yielded`/`abandoned` 任一终态, 或本容器该轨无任何 claim"。**实测复核**: `git show refs/aria/coordination:claims/023236f2/s-86f7@1836.yaml` 得 `status: yielded`, `git show refs/aria/coordination:claims/bfe8285d/s-73b9@1606.yaml` 得 `status: active`, 两份原文与 `metadata.claim`(`detailed-tasks.yaml:16`)自述逐字吻合 —— "钉死写法失效是实测而非推断"这句自检站得住。|
| PP2-M2 | **closed** | `metadata.coord_ref_precheck.own_claim_files`(`detailed-tasks.yaml:566`)已改写为"TASK-001 在运行时按三元组解析出的 claim 文件……不是写死的路径", 并新增"反向指针"说明 fixture(`N6`)自造 claim 与生产运行时解析的等价关系, 采纳了 R2 (d) 条里可读性建议部分; TASK-001 verification 第 4 条(`detailed-tasks.yaml:1050`)显式要求把"上一步解析出的本轨 claim 文件(可多条)"作为 `coord_ref_precheck` 的参数。原来"`own_claim_files` 钉在已失效文件上 ⇒ `coord_ref_precheck` 首跑必判 `other` 而停"的问题随 PP2-M1 的修法同时消除(两者共享同一处代码改动)。|
| PP2-M3 | **closed(原报告的缺陷); 但本轮在同一机制里发现一个新的、未被自报的缺口, 见上方 finding `9122f4a9`** | `commit_attribution` 已改为 `exclusive`/`shared`/`foreign` 三分类, 单亲提交判 `own` 需要"无 foreign 文件 且(有 exclusive 文件 或 带本轨 `Spec:` trailer)"(`detailed-tasks.yaml:580-634`)。**实测复核**(未跑脚本, 手工按代码逐行核对四个真实提交): `1b9734a`/`5fe15b0`/`c9fe08f`(改动集合均 ⊆ `SHARED`, 无 `Spec:` trailer)按新逻辑归 `shared-only`, 与 revision_log 自述"由 `ok/[own]` 翻为 `stop/[shared-only]`"一致; `9de3074`(改动路径均不在 `SHARED` 也不满足任何 `exclusive` 条件, 且是另一个 spec `rule6-description-change-trigger-eval-lane` 的产物)仍归 `foreign`, 与自述一致。R2 原始复现的三个"整条提交全落 FIXED 集判 own"的具体样本已验证不再复现。但同一套三分类逻辑在处理"部分 exclusive + 部分未登记路径"的混合提交时(`12c870d` 即是实例)会把整条提交误判成比 `shared-only` 更差的 `foreign`, 这是 R2 未覆盖、本轮新发现的缺口, 已计入 finding `9122f4a9`, 不重复计入本行判定。|
| PP2-M4 | **closed** | (1) 断言本体: `metadata.baseline_rebase.standards`(`detailed-tasks.yaml:78`)已从"零 diff 全称句"改写为限定在 `21748d4..940cb5b` 之间、限定在四个文件的断言, 并逐字标注"v1/v2/v2.1 写的『standards 被引文件零 diff』在 940cb5b 落地后即已为假(post_planning R2 的 PP2-M4)"。**实测复核**: `git -C standards diff --stat 21748d4 940cb5b` 与逐文件 `--shortstat` 结果与 yaml 断言(含 `+56/-2`/`+21/-3` 精确行数)逐字节吻合。(2) `rule6_note`: 已按 `standards/conventions/skill-benchmark-exemption.md` 1.1.0 §4.1 的五字段模板重写(`detailed-tasks.yaml:134-141`), **实读 SOT 原文**(`standards/conventions/skill-benchmark-exemption.md:59-68`)确认模板要求恰为 `decision_table_row`/`description_changed`/`scenario1`/`scenario4b`/`negctrl` 五个字段, v2.2 五者俱全且取值符合 SOT 的合规判据(`description_changed: 'no'` 时 `scenario4b: not_required` 与 `negctrl: n/a` 均合规); 另加的 `fields_basis`/`note` 是模板之外的补充说明, 不违反"最小模板"要求。**但**: PP2-M4 判定时提到的自报薄弱点(b)"没有为这类冻结断言加机械守卫", 在本轮验证中被证实是一个可以指名道姓的具体遗漏(TASK-001 的基线复核未覆盖 standards), 已计入 finding `32076746`, 不重复计入本行判定。|
| PP2-M5 | **closed, 且有真实区分力** | 读前必看第 8 条(`tasks.md:24`)已将 explicit-only 收窄从"仅 S4 与 `no_spec_unverifiable`"扩到 `spec_level_undetermined`; TASK-011 verification(`detailed-tasks.yaml:1249-1250`)给出完整定义与 SC-9(4) 的可证伪落点, fixture 钉 `checkpoints: {post_spec: 'convergence'}`, 断言 `checked_checkpoints == ['post_spec']`。**独立复算区分力**(未跑代码, 逐条推理该 fixture 下两种实现路径的输出): 该 fixture 下非排除 checkpoint 有 `post_spec`(显式)、`post_planning`、`post_implementation`(均需读锚点 Level, 而 Level 不可解析); "P4 末尾统一装配"实现在早退前从未完整跑完 P4, 该字段应为空 ⇒ `[]`, 与断言 `['post_spec']` 冲突 ⇒ 红, 与 yaml 自述的反事实一致; "边算边收"类实现里, 若按字典序枚举(`post_implementation < post_planning < post_spec`)则 `post_implementation` 会先触发 `spec_level_undetermined` 而 `post_spec` 尚未被处理, 同样只能给出 `[]` 或不完整的中间态, 而非 `['post_spec']` —— 即无论"何时装配"还是"何种非显式优先枚举顺序", 都无法侥幸撞出与 explicit-only 规则相同的结果, 只有真正按"过滤原始 `config.checkpoints` 字面值"实现才能稳定给出 `['post_spec']`。区分力成立, 不是走过场断言。|

## 对执笔人自报薄弱点的表态

- **(a) trailer 判据把"归属"从路径事实降级为提交者声明**: **可接受**。理由: `owner_gates` 第 2/9/16 项在推送前都要求把 `git log` 清单连同 `kinds` 呈给 owner, 人工复核这一关没有被绕过; 伪造需要故意在提交信息里写出本轨字面的 `Spec:` trailer, 属于需要主观刻意配合才能触发的低概率场景, 且后果只是"少问 owner 一次"而不是"绕开 owner 直接推送"。
- **(b) M4 的修复是"记录更新 + 范围限定"不是机制, 没有为这类冻结断言加机械守卫**: **不可接受**。这不是一个仍待验证的风险描述——本轮已经在 TASK-001 的"基线复核" verification 里找到具体、可指名的遗漏(只重测 `aria_zero_diff`/`aria_shifted`/`main_repo`, 通篇未提 `standards`), 与 `metadata.baseline_rebase.standards` 自己写的"TASK-001 必须对 B.1 当时的 gitlink 重测"直接矛盾, 已计入 finding `32076746`, 需要在返修里实际补上这条重测步骤, 不能只停留在自报层面。
- **(c) SC-9(4) 的触发前提是读出来的不是跑出来的(被测脚本要到 Phase B 才存在)**: **可接受**。这是 Phase A/A.2(TDD RED 之前的计划阶段)固有的验证形态——被测脚本尚未实现, 反事实只能靠对 §1.0 求值顺序的字面推演完成; yaml 自己也如实标注了这一点("`checked_checkpoints == ['post_spec']` 逐字相等……反事实: 在 P4 末尾才统一装配该字段的实现在此格给 `[]`"), 而这条推演我在 R2 对账里独立复算过、逻辑站得住(见上表), 不是草率的"拿不准也算过关"。

## 风险 / 疑问

1. §1.0 的 P0-P6 总序表没有给"同仓判定"(`--repo-path` 与 `--diff-repo-path` 的 git toplevel 比对)和"`--base`/`--anchor-base` 陈旧比对"显式编号步骤; proposal 把它们放在参数定义段(`:95-100`), 不在 P0-P6 表内。TASK-008(`detailed-tasks.yaml:1191`)把"同仓判定"排在 P1 之后, TASK-009(`detailed-tasks.yaml:1211`)把"ref 解析与陈旧比对"排在"同仓判定之后、P2a 之前"。这是任务规划层面对未明说顺序的合理外推, 但我没能构造出一个会让最终 `verdict`/`error_kind` 因这个顺序而判决不同的具体 fixture(两条路径都以 `git_failed` exit 2 收场, 目前没有 SC 断言要求区分"同一次调用里两种错误同时成立时报哪个 `error_kind`"), 故不计入 finding, 留作执笔人/审计后续轮可以澄清的点。
2. finding `9122f4a9` 描述的 `.aria/notes/` 缺口, 如果 Phase B 期间(例如本轮若判 REVISE 后的下一次返修)生成器工作流继续复用同一目录, 会重复触发; TASK-030 已经用 `extra` 参数处理了 ab-results 目录的同类问题, 但 TASK-001 目前没有对称处理。这是 M1 的直接推演, 未单独计入第二条 finding。

## Verdict

**0C / 2M / 0m**

**Vote: REVISE**

## 是否足以开始 Phase B

**不足以**。两条 major 均可在返修中低成本修复(补一处 fixture/`extra` 参数、补一条 verification bullet), 不涉及任务结构重排或 proposal 设计取舍; 但 `commit_attribution` 与"基线复核"都是 TASK-001(B.1 入口)第一时间会跑到的机制, 在它们被修好之前进入 Phase B, 会让执行者在最开始几步就可能撞上这两个已知会触发的缺口。且入口本身仍卡在 `owner_gates` 第 1 项(`10CG/Aria#195` 未完成 C.2 合并)——审计收敛与"可以开工"是两件事, 这一点 R2 已经提醒过, 本轮依然成立。
