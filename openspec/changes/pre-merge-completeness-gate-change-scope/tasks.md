# Tasks — `pre-merge-completeness-gate-change-scope`

> **Spec**: [proposal.md](./proposal.md) (v6, Level 3, Approved 2026-09-12)。本文件所引 proposal 行号指主仓 `a563192` 上的该文件 (sha256 `d3c9b4f2…6f34`, 自 `0a2ae53` 起未变); proposal 所引 aria 行号冻结于 `301641b`, 复核见「读前必看」第 5 条
> **决策单**: `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` §1 与 §2 的 10CG/Aria#199 表 13 行 (连同 §5, 即最终执行口径)
> **Level**: 3 — 本文件 (A.2) + `detailed-tasks.yaml` (A.3, 单一 SOT: verification / 依赖 / 工时 / 外向动作明细 / A.2 实跑记录)
> **Status**: A.2/A.3 v2.6 (2026-09-24, 执笔容器 simonfish/bfe8285d, 执笔人不是派单主控, 沿用 v2.4 的执笔实例; v2.6 = post_planning R6 五条 minor 返修: 5.9 的 `track-id` 加逐字取值断言并删去不可达停点、条目序号引用改锚点式、写协调 ref 之前一律先强制对齐 (release 与重新认领同补)、C.2.4.5 的 override 口径按闸的调用时机改写、custom checks 一律看输出首行 (`##SKIP##` 算没跑成), 另按三份机器清单做同族扫描 (判断清单第 46–50 条); v2 至 v2.5 的返修与逐条追溯见 yaml `metadata.revision_log`) — 待主控核验
> **Scope**: aria 子模块 (A.2 实测 `origin/master` = `1cb3872` = v1.73.3) + 主仓 (A.2 实测 origin 与 github 的 master 均为 `a563192`); standards 不改
> **ship target**: aria-plugin `<vNEXT>`, MINOR (决策单 §2 第 4 行); 本文件不写字面版本号
> **执行台账**: 1.1 新建本目录 `verification-ledger.md`, 主控唯一执笔; 下文「台账」均指它

---

## 读前必看 — proposal 正文与执行口径的差异 (proposal 不改, 以本节为准)

| 编号 | 事项 | proposal 正文 | 执行口径 | 依据 |
|---|---|---|---|---|
| 1 | 执行顺序 | `:4` / `:18` 排在 10CG/Aria#195 之后进 A.2 | owner 2026-09-17 选择先做本 spec 的 A.2/A.3 (10CG/Aria#195 的 Phase B 未起)。ship 仍串行: 1.1 的入口前置 = 10CG/Aria#195 已完成 C.2 合并, 或 owner 明示改序 | 决策单 §1 Q3 |
| 2 | 分支起点 | `:10` 在 `f314785` 起分支 | aria 与主仓都从 B.1 实测的 `origin/master` 起; 主仓规划提交届时未推送则回落为含规划提交的本地 master | A.2 实测 |
| 3 | 版本号 | `:16`、`:366`、`:450`、复议条目 4 的 `v1.73.1` / `v1.74.0` | 作废 (v1.73.1–v1.73.3 已发布)。MINOR, 号在 5.3 按 `plugin.json`、两个远端的 tag 与 10CG/Aria#195 实际发布号计。主仓 `VERSION:24` 仍写 `v1.73.0` (三次漏改), 5.7 直接写新号 | 决策单 §2 第 4 行 |
| 4 | `ab-suite/version.yaml` | `:368` 与裁定 4c: 1.5.0 → 1.6.0, bump 前 `ls-remote --tags` | 目标 = 当时现值的下一个 MINOR。`ls-remote --tags` 管不到这个主仓文件, 改为 fetch 后读 `origin/master` 上该文件; 并发轨 10CG/Aria#211 的 T4 也要把它升过 1.5.0 (其 proposal `:135` / `:146`), 被占即顺延 | A.2 实读 |
| 5 | 基线行号 | `:9` / `:16` 冻结 `301641b` | A.2 跑 `301641b..1cb3872`: proposal 引用的代码与规程文件零 diff (清单见 yaml `metadata.baseline_rebase`); 有 diff 的是 `spec_complete.py` (原位 1 行, 被引的 `:924` / `:1642` 不移)、`multi_remote.py` (原位注释, 被引的 `:107-113` 不移)、`check_bare_issue_refs.py` (旧 SHA 上不存在)、`CHANGELOG.md` (`[1.73.0]` 现 `:104`, `[1.70.0]` 现 `:200`, 完整性门条目现 `:3136`)、`VERSION` (两条先例行现 `:7` / `:8`) 与版本号文件。standards 侧按 `21748d4..940cb5b` (proposal 定稿 gitlink → 当前 gitlink) 2026-09-19 实测: 全仓只两个文件变动 —— `content-integrity.md` +56/-2 (新增 §4.4 / §4.5, 须遵守) 与 `conventions/skill-benchmark-exemption.md` +21/-3 (SOT 升 1.1.0, 新增 §4.1 `rule6_note` 五字段模板, 本 spec 已按其重写); 其余六个被引文件 (`openspec/project.md` / `templates/proposal-minimal.md` / `configured-gate-authority.md` / `version-management.md` / `git-commit.md` / `session-handoff.md`) 在该区间零 diff (2026-09-21 复测退出码均为 0) —— **这是对这六个文件、这两个 SHA 的断言, 不是全称句**。被引文件全集 (八份, 含上面两份已变动的; `session-handoff.md` 是 v2.4 按 Rule #9 的间接引用补入, 求法见 yaml `metadata.baseline_rebase.standards_files_basis`) 与各自的依赖点见 yaml `metadata.baseline_rebase.standards_files`; 1.1 对该清单逐个重跑, 对象是 B.1 当时的 gitlink | yaml |
| 6 | 裁定 1 连带 | §1.3 排除四项; SC-18 两分支; SC-15(5) 期望四个 checkpoint | 排除**五项** (加 `post_brainstorm`); SC-18 只留排除分支; **SC-15(5) 期望改为 `['post_implementation', 'post_planning', 'post_spec']`、`len(results) == 3`、三对 `missing`** (fixture 不变); SC-8 / SC-15(3)(7)(9) / SC-20(2)(7) 实算不变; CHANGELOG 迁移文案另加「`post_brainstorm` 不再作为前置依赖」 | 决策单第 1 行 |
| 7 | 裁定 11 连带 | 按「降为 / 不被豁免 / 豁免 / 逃生口 / `no_spec_unverifiable`」全文检索, 与裁定 11 冲突的共 9 处: `:118` (§1.0 短路第 2 类)、`:162` (§1.1 末段)、`:181` (§1.1b 第 4 行)、`:338` (§2 SKILL.md 注释)、`:340` (§2 Step 2 改写句)、`:360` (§4 表 execution-modes 行)、`:378` (§5 第 2 条)、`:386` (§5 第 10 条)、`:473` (SC-17(5)); `:285` 是论证句, 不作执行依据 | `allow_incomplete_checkpoints` 覆盖 `no_spec_unverifiable` (降 `bypassed` exit 0 并短路), `allow_dangling_change_ids` 不覆盖; `no_spec_contradicted` / `change_id_unanchored` 不豁免。Step 2 改写句定为「→ 仍逐对评估三态并全部留痕, 只把 missing / scope_unresolved / spec_level_undetermined / no_spec_unverifiable 降为 verdict=bypassed (exit 0) 并短路终止求值; no_spec_contradicted / change_id_unanchored 不被本键豁免」。降级后取值同 §1.1 末段「S4-bypassed 的字段取值」, 统一 WARN 行取 `scope_unresolved=1`, 另加 `[WARN] bypassed: no_spec_unverifiable`。SC-17(5) 改写全文见 yaml TASK-006 | 决策单第 11 行; 取值由执笔人钉定 |
| 8 | 短路运行的非判定键 | §1.4 未全定义 | 在 P6 之前终止的运行 (error / S4、`spec_level_undetermined`、`no_spec_unverifiable` 被豁免的 bypassed / 格 B–E; missing 被豁免的 bypassed 走完 P6, `results` 照常输出): `results=[]`, 两个计数 0, `unattributed=[]`, `scanned_dir_depth=1`, `scan_status` 取报告目录当时是否存在, `no_prior_checkpoints` 仅格 B/D/E 为 true, `scope_source` / `change_ids` 取已产出值否则 `null` / `[]`; **`checked_checkpoints` 在三类被豁免的早退 (S4、`no_spec_unverifiable`、`spec_level_undetermined`) 下一律用 explicit-only 规则** = 只收原始 config 的 `audit.checkpoints` 里显式写出、值非 `off` 且不属五项排除的键, `sorted()` 输出。**不取「已产出值」**: 那个写法由实现装配该字段的时机决定 (边算边收 vs P4 末尾统一收), 两个字面合规的实现会给不同值 (`['post_spec']` 或 `[]`) 而现有断言都不会红 (post_planning R2 的 PP2-M5)。`spec_level_undetermined` 被豁免时另加 `[WARN] bypassed: spec_level_undetermined`; 该格 (SC-9(4)) 的 fixture 钉 `checkpoints: {post_spec: 'convergence'}` (mode 仍按第 9 条为 `adaptive`, 其余期望值不变) 使两种读法可区分, 并逐字断言 `checked_checkpoints == ['post_spec']` | 执笔人钉定 |
| 9 | fixture 的 mode 例外 | §1.0 `:122` 的 adaptive 例外清单 | 漏列 SC-9(2) 第二跑与 SC-15(8)(9) (adaptive)、SC-15(5)(7) (convergence) ⇒ 正文逐字给出 mode 的格按正文, 其余钉 manual | A.2 实读 |
| 10 | catalog 缺口 issue 的仓 | 决策单第 9 行「开到 `aria-plugin-benchmarks`」 | 该远端仓不存在 (A.2 `forgejo GET` 得 404, 目录属主仓) ⇒ 开在 **10CG/Aria**; 套件覆盖缺口仍开在 10CG/aria-plugin | A.2 实测 |
| 11 | `check_bare_issue_refs.py` 是不是门 | `:451` 请 owner 明确 | 已由 `standards/conventions/content-integrity.md` §4.4 回答: 手动自检工具, 不以整份文件 rc 0 为门槛 ⇒ 5.4 只查本 cycle 新增行 | standards §4.4 |
| 12 | SC-12 state-scanner 命令的环境 | `:468` | 须在**不带** `ARIA_COORDINATION_NO_PUSH` 的会话跑。A.2 副本实测: 带该变量 `Ran 1605` 失败 1 条 (`test_refresh_without_no_push_publishes_to_remote`), 不带 `OK (skipped=1)` (其余见 yaml `metadata.test_runner`) | A.2 实跑 |
| 13 | 归档门 liveness | `:468` 子句已删; F7 注 `:58` 只靠 SC-13 | Level 3 已成立 ⇒ SC-13 守文本面, 归档门守调用面, 见「重写 a」 | 决策单第 12 行 |
| 14 | §1.3(c) 自证段 | `:267` 本 spec 自身即此形态 | 见「重写 b」 | 同上 |
| 15 | SC-6 自证格 | `:462` 对本 spec 自身目录跑 (3) 分支 | 见「重写 c」 | 同上 |
| 16 | SC-11 的 post_planning | `:467` `present` 或 `missing`, 理由是本 spec 有内联 Tasks | 理由改为本目录已有 `tasks.md`; 届时 post_planning 报告已落盘 ⇒ 期望 **`present`**, 实跑为 `missing` 属新发现, 记台账上报, 不改断言; 本条无区分力, 区分力在重写 c | 第 15 条 |
| 17 | `mid_post_spec` 进入 B.2 | 头部 `:14` B.2 未开工故不跑 | 该前提在 B.2 失效且两读法并存 (`phase-b-developer/SKILL.md:214` 读合并视图字面键 = off; §1.3 优先级链 = 启用)。B.2 出现漂移信号 ⇒ 停在该任务、记台账、请 owner 裁, 不自行跳过, 不当场改断言 | Rule #10 |
| 18 | 复议前置门 | `:428` | 已全部裁定 ⇒ 解除 | 决策单 |
| 19 | 同形位置 | §3 / §4 只列 `phase-c-integrator/SKILL.md:132` | 同文件 `:57` 与 `:754`、`audit-engine/SKILL.md:423` 也按字面条件判 pre_merge, 3.2 / 3.3 改为同一短语「pre_merge 按 C.2 pre_hook 步骤 3 的优先级链判为启用」(N8) | A.2 实读 |
| 20 | 发布面 | `:449-450` | 只合并 aria; 主仓动 aria gitlink 与 16 个版本点 | §4 表 |
| 21 | issue 号「写回本 spec」 | SC-14(c)、`:451` | 号记台账、ab-results README 与周期 handoff; 复议结论已在 `0a2ae53` 回写 | 本节原则 |
| 22 | 内联 Tasks 的 checkbox | `:409-451` 共 **17** 个 | 保持不勾; 进度以本文件为准 (归档门只读 `tasks.md`, `spec_complete.py:273`) | A.2 实读 |
| 23 | 未给 checkpoint 配置的格 | 部分 SC (如 SC-22(1)) 正文没给 `checkpoints`, 而断言要求纳入集非空 | 按硬约束钉 manual 后纳入集为空、会落格 C; 1.3 为这类格补 `checkpoints: {post_spec: convergence}`, 期望值不变 | 执笔人补定 |

### 三处 Level 3 重写 (执行口径全文)

**重写 a — SC-12 追加归档门 liveness 子句**。输入 = 5.9 归档预演时的本目录 (tasks.md 已全部勾选) 与主仓根。(L3) 抽取面: 对 tasks.md 第 3.2 行调 `spec_complete.extract_claim_symbols`, `symbols` 含 `completeness_gate`; (L2) 分类面: `spec_complete.classify_symbol_liveness('completeness_gate', <主仓根>, {'aria/skills/audit-engine/scripts/completeness_gate.py'})` 的 `status == 'alive'` 且 `alive_categories` 含 `aria_plugin_integration`; (L1) 门面: `spec_complete.py --gate <本目录>` 的 `verdict != 'block'` 且 `blocking_reasons` 不含 `completeness_gate`。**验收 = L2 与 L3 同真**, L1 只作「归档门不拦」的确认。A.2 在副本上的实跑 (yaml `metadata.a2_state_runs`): 脚本不存在 ⇒ 分类器判 `ambiguous`, L2 假而 L1 真; 调用只写在 SKILL.md 散文里 ⇒ `dead`, L1 与 L2 同假; 散文加上 `ab-suite/audit-engine.json` 里的脚本字面路径 (5.1 的 eval id 3 会写入) ⇒ 按 JSON 判 `alive` (`generic_path_call`), L1 真而 L2 假; 3.2 行丢掉脚本 token ⇒ L3 假。3.2 行写全仓相对路径是承重的: 门按该 token 找定义文件, 找不到时只能靠脚本正文含自身名字 (对照态 D2)。反事实 = 调用行只写散文 ⇒ L2 红 (5.1 之后 L1 不再红)。4.3 先跑 L2 / L3 与副本上的 L1, 5.9 复跑三条。

**重写 b — §1.3「(c) 为什么改成『任何 A.2 产物』」的自证段**, 替换「本 spec 自身即此形态 …… (c) 在它们上仍会正常触发。」: 本 spec 在 A.2 之前 (主仓 `a563192`) 即此形态 —— 目录只有 `proposal.md`, 内联 `## Tasks` 在 `:407`, 头部却声明跑 post_planning, 按原稿判据这份快照会拿到 not_applicable 免检票。Level 3 裁定后本目录已有 `tasks.md` 与 `detailed-tasks.yaml`, 两种判据都判 `present`/`missing`, **当前目录不再能区分两种判据**, 区分力改由 SC-6 在该快照上承担 (重写 c)。改判据的理由不依赖本 spec: Level 2 输出只有 `proposal.md` (`standards/openspec/project.md:117`), 模板自带 `## Tasks` (`templates/proposal-minimal.md:28-32`); `a563192` 实测有 `proposal.md` 的 change 154 个, 无 A.2 文件的 54 个, 其中有内联 `## Tasks` 的 17 个 (含本 spec, A.2 落盘后为 53 / 16), 三样全无的 37 个 —— (c) 在这 37 个上仍正常触发。

**重写 c — SC-6 的自证格**, 替换「自证: 对本 spec 自身目录跑 (3) 分支 …… 一致」: (i) **(3) 分支用 A.2 前快照, 由 4.4 活体执行 (快照 295KB, 不进单测)** —— hermetic 仓 (`git init -b master`, 一次提交) 内 `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` 取 `git show a563192:<同路径>` 的原样字节 (sha256 `d3c9b4f2…6f34`; 快照里该目录只有这一个文件), 不放 `tasks.md` / `detailed-tasks.yaml`, `.aria/audit-reports/` 为空目录, config `{audit: {enabled: true, mode: 'manual', checkpoints: {post_planning: 'convergence'}}}`, 两个路径参数同为该仓根, `--base master --change-id pre-merge-completeness-gate-change-scope` → 该对恰为 `missing`; 反事实: 判据退回「只看两个文件」⇒ 判 `not_applicable/no-a2-artifact`。(ii) **当前目录只作对照**: 跑得 `present` 或 `missing` 且 reason 不是 `no-a2-artifact`; 对错误实现同样成立, 不计作区分力证据。

---

## AI 流程判断清单 (请 owner 复议 — Rule #10 §5)

以下由 A.2/A.3 执笔人自行作出; 5.9 的周期 handoff 照录并追加新增项。

1. proposal 不改, 执行口径与三处重写全文落在本文件 (沿用 10CG/Aria#195 先例)。
2. owner 2026-09-17 选择先做本 spec 的 A.2/A.3、10CG/Aria#195 的 Phase B 未起; 本文件未把它解读为改 ship 顺序, 决策单 Q3 的串行落成 1.1 的等待点。
3. 内联 Tasks 17 项重排为 5 组 31 项 (末表映射), 编号无字母后缀。
4. SC-12 liveness 验收取 L2 + L3, L1 只作确认; 3.2 行写全仓相对路径以便门能定位定义文件。
5. SC-6 自证改用 `a563192` 快照并移到活体运行, 当前目录降为无区分力的对照。
6. SC-11 的 post_planning 期望收紧为 `present`。
7. SC-15(5) 期望值按裁定 1 由本文件重算, 不留给实现者。
8. 裁定 11 派生的字段取值与 WARN 行、短路运行的非判定键 (读前必看第 7、8 条) 由执笔人钉定; fixture 的 mode 例外按正文补全 (第 9 条)。
9. 新增文档机检 N1 / N2 与 stdlib 检查 N3 (只增不改, 三态实跑见 yaml), 并要求 execution-modes.md 的 `Step 1:`–`Step 5:` 五个标记全部保留 (proposal 只要求 4 / 5)。
10. `phase-c-integrator/SKILL.md:57` 与 `:754` 纳入 3.3, `audit-engine/SKILL.md:423` 纳入 3.2 (同形, 多三处触点)。
11. B.0 认领不照 phase-b-developer「本 session 没有 claim 就跑 phase1_gate」的字面: 先按 (本容器, 归一 track_id, `active`) 三元组**运行时解析**本轨 claim (不钉文件名), 解析到就 `--heartbeat-only` 刷新; 解析不到 `active` (`done` / `yielded` / `abandoned`, 或本容器该轨无 claim) 才在获授权后用原串重认领, 未获授权则停在 1.1; 解析到多条 `active` 不假设唯一, 按 `10CG/aria-plugin#202` 的形态全部纳入并上报 (CLI 每次新生成 session id, 照字面会写出第二条 claim)。v2.5 起这一解析连同前置检查、强制对齐与心跳核验在 Phase B–D 每个会话入口重做 (第 41 条)。
12. `mid_post_spec` 在 B.2 的两读法按「停下请裁」处置。
13. 反事实补丁由既非实现者也非测试作者的新实例构造, 语料复现核对由未参与标注的实例做; 反事实在 2.6 SHA 的副本上三步法跑; 基线 RED 不充当反事实。
14. 脚本不存在时, 测试 helper 先断言脚本文件存在, RED 以 AssertionError 呈现。
15. 5.2 的两个套件按描述性推演下发并逐字禁止 fetch / pull、git 写命令与 forgejo 写接口; 前后各取一次本地与远端快照, 两次之间本会话不调 `/state-scanner`、不 fetch; 远端值变化时以「新值对象是否已在本地」判是否本机推出; 不改 remote 配置。
16. catalog 缺口开在 10CG/Aria; `version.yaml` 取号改读 `origin/master` 上的文件。
17. aria 推送与逐 remote 核验由 5.6 承担; 主仓 master 双推交 C.2.5, 事前核五问 (yaml `metadata.c25_five_questions`)。
18. 同步 `origin/master` 用 merge 不 rebase, 主仓 PR 以 merge commit 合并 (覆盖 C.2.1 与 branch-manager 的默认), 使台账引用的 SHA 留在远端 master 上。
19. Phase B 期间 aria 发版属常规情形: 5.3 先把 aria `origin/master` 并入 feature 并重跑回归, 5.5 按 AB 基线与合并基线之间两个 skill 目录的 diff 决定是否重跑 5.2 (v2.5 起另比 feature 一侧 W 之后的改动, 两侧都按退出码判零 diff, 见第 43 条)。其余罕见路径 (并入冲突 / 取号被占 / 合并冲突 / 推送被拒 / 半推) 停下上报, 只给先例指针 aria `ec72175`, owner 确认后执行, 不写自动恢复流程。
20. 全部 checkbox 由主控在 5.9 归档预演前一次勾选。
21. 含集成关键词的行只点名它接线的脚本; 归档门预演的其余 warn (4.4 行 dogfood 无可链接产物) 照记, 不为躲检查器改措辞。
22. AB 判据按套件分: 两个套件都逐 eval 判回归 (复跑两次、三取二); `delta > 0` 只要求 audit-engine 套件; without 臂用 AB 开跑时 aria `origin/master` 的快照 (old_skill 语义)。
23. 1.3 给未写 checkpoint 配置的格补钉 `checkpoints: {post_spec: convergence}` (读前必看第 23 条)。
24. 5.7 与 5.8 把 `plugin-cache-currency` 的 STALE 视为预期 (owner 更新插件缓存前)。
25. 5.9 手写 Phase D, 不调 phase-d-closer。phase-d-closer 的全部子步 (依据 `aria/skills/phase-d-closer/SKILL.md` 与同目录 `references/execution-steps.md`、`references/handoff-mechanics.md`) 在手写路径里逐一落点如下 (v2.4 按 post_planning R4 R4-M2 列全; 此前只写了 D.1 / D.2b / D.4 三项偏离): D.1 进度更新 —— 跳过并留痕, 本仓无运行时 UPM (phase-d-closer 自身的跳过规则同此); D.post post_closure 审计 —— 5.9 执行时按 phase-d-closer 的触发条件 (`audit.enabled == true` 且 `audit.checkpoints.post_closure != off`) 读配置判定, 不成立才按配置跳过 (Rule #10 白名单第一类; 2026-09-21 实读 `post_closure` 为 `off`), 成立则照跑; D.2 归档 —— 归档预演的 `spec_complete.py --gate` 与 openspec-archive 兜住三路 (`verdict=block` 停下上报; `complete=false` 由 openspec-archive Step 1 自身拦下; 放行才归档, Step 7 由 owner 裁); D.2b claim 释放 —— yaml TASK-031 的 release 条 (release 之前单独请等待点 13a, v2.5), 不带 `--sweep-stale` / `--gc` (须另行授权), 推后按 `coord_push_verify` 核 `push_success` (phase-d-closer SKILL.md 的「除 exit code 外还须看 `push_success`」落在这里); D.3 子步 1 触发评估 —— 不做, 本计划无条件写周期 handoff, 比触发条件更严; D.3 子步 2 按模板起稿 —— yaml TASK-031 的周期 handoff 起稿条 (`owner-container` 取 `handoff_autofill.py --owner-container` 的机械值); D.3 子步 2b 写后五字段自校验 (E1) —— 同任务的五字段自校验条, 命令逐字照抄 (含 `head -8` 窗口); D.3 子步 3 `latest.md` 两子步 —— 同任务的子步骤 1 条 (History prepend 恒做、不可跳过) 与子步骤 2 条 (pointer 按三行判定表, 多轨 follower 不改), 改动单独成提交, 该提交产生之后请等待点 13b 并附其 diff (见第 38 条与第 40 条); D.3 子步 4 提示提交 —— 5.9 末条 Phase D 提交经授权双推; D.4 estimator 采集 —— 照跑, 非阻塞 (phase-d-closer 的触发条件 `ai_native_estimator.enabled != false`: 2026-09-21 实读 `.aria/config.json` 无该键, 即成立)。
26. 组 2 的中间任务只验收本段完成后即可观测的子格 (yaml `metadata.stage_cells`), 测试的每个格包在 `subTest` 里; SC 方法级全绿只在 2.5。
27. 协调 ref 的写入与推送 (心跳、获授权的认领与重新认领、release) 与强制对齐之前先跑 yaml `metadata.coord_ref_precheck`, 本地领先的只有本轨心跳才继续; 这是心跳免授权的适用前提, Phase B–D 各会话调用 `/state-scanner` 之前也跑。**退出 0 之后、动手写或推之前**再强制对齐一次并重跑三元组解析 (v2.6, post_planning R6 `2c2e8931`, 见第 48 条): 前置检查退出 0 含「与 origin 分叉」一态, 分叉时不对齐就写, 写得进本地却推不出去。**推送之后**再按 yaml `metadata.coord_push_verify` 核验推成了没有 (`push_success` 为真、`push_skipped` 为假, 再 `ls-remote` 与本地比对) —— 免授权只覆盖「发起这次推送」, 不覆盖「推成了没有」(v2.3)。
28. 待推送的主仓提交按 yaml `metadata.commit_attribution` 判归属: 路径分本轨专属 (本目录、本轨审计报告、本轨 handoff、以及本轨 A.2/A.3 工具目录 `.aria/notes/2026-09-17-199-a2-a3-tooling/` —— 末项 v2.3 补入) / 发布同步面 / 他轨三类, **整条只落发布同步面的提交不再单独算本轨** —— 需同一提交另有本轨专属路径, 或提交信息带本轨 `Spec:` trailer (`git-commit.md` §6.2 既有写法); 共享指针 `docs/handoff/latest.md` 的改动一律请裁。
29. 组 2 / 组 3 / 组 4 串行 (编号序), 组 3 从 2.6 之后开始。
30. 同仓判定在 P1 之后求值; ref 解析与陈旧比对在 P2a 之前无条件执行。
31. 新增机检 N4 (调用串对 canonical)、N7 (CRLF)、N8 (同形改写)、N10 (配置文件不含符号), 与 N1–N3 同为只增不改, 三态见 yaml。
32. (v2.2) 读前必看第 8 条的 explicit-only 收窄扩到 `spec_level_undetermined`, 并给 SC-9(4) 的 fixture 补钉 `checkpoints: {post_spec: 'convergence'}` 使两种读法可区分 —— 补钉 fixture 参数沿用第 23 条的先例 (期望值不变), 新增的是一条逐字断言, 不是改既有期望值。
33. (v2.2) 提交归属收紧: 整条只落发布同步面的提交不再单独构成本轨, 判据是「同一提交另有本轨专属路径」或「提交信息带本轨 `Spec:` trailer」; 代价面在 v2.3 按 31 个 TASK 的交付物全量重跑路径分类后改写: 结构上不含本轨专属路径的交付物有**两组** —— 5.7 的九个版本同步面文件与 5.1 的两个 `ab-suite` 文件, 两组都必须带 trailer, 任一漏写即停在等待点 16 (fail-closed, 多一次请裁); 另三类不靠 trailer —— 本轨工具目录改由专属前缀集兜住 (v2.2 漏列, 真提交 `12c870d` 曾因此被判他轨), 本次 `ab-results` 目录靠 5.8 调用判据时把它作 `extra` 传入兜住 (与台账同提交并不改判 —— `foreign` 短路优先于本轨专属, 实测), 5.9 周期 handoff 靠 frontmatter `track-id` 逐字相符兜住 (v2.6 链接注: 5.9 自身不跑该判据, 那里的 `track-id` 取值另由 `grep -cxF` 逐字断言守, 见第 46 条)。
34. (v2.2) claim 身份一律运行时按 (本容器, 归一 track_id, `active`) 三元组解析并覆盖四态; 多条 `active` 不自行删除或释放, 全部纳入并上报。
35. (v2.4) post_planning R4 R4-M3 按 (b) 裁: skill-creator 工作区会产生, 但按仓内 SOT 不入库 —— 5.8 的提交归属判据不再收它作 `extra`, 5.2 的快照比较不再单列它为例外; 它放在已被忽略的位置 (aria 子模块 `skills/*-workspace/` 或主仓 `aria-plugin-benchmarks/ab-workspace/`; v2.5 改为只放后者, 见第 44 条), 结果依据的逐 eval 产物复制进结果目录 (形状对齐先例 `2a46d08`)。依据: 生效 skill-creator 的 SKILL.md 只用散文规定工作区位置 (「as a sibling to the skill directory」), 两个脚本只收调用方传入的目录; aria 与主仓两处 `.gitignore` 的对应条目及其注释; 2026-04-10 之后触及 `ab-results/` 的 51 个提交零 workspace 路径, 仓内 23 个被追踪的 `state-scanner-workspace/` 文件全部出自 2026-04-09 的 `2892c6f`, 早于三条忽略规则。
36. (v2.4) 1.1 基线复核的 aria 组与主仓组按 standards 组同口径一并改 (两端点先 `cat-file -e`, 零 diff = 退出码 0 且输出为空), 而不是只论证它们不受影响: 两组端点按构造已在本地, 同口径在正常路径上不会误停, 另拦 SHA 抄错一类同形失败 (2026-09-21 实测抄错一位时 stdout 同为空串、退出 128)。
37. (v2.4) standards 被引文件集的求法定为两步: 字面计数 (输入钉在冻结快照 standards `940cb5b` 与主仓 `71c500e`, 排除清单封闭为三族) 加 Rule #N 映射 (按 CLAUDE.md 各条 SOT 指针); 第二步里「内容是否被依赖」仍是判断, 本轮只据此补入 `session-handoff.md`; 以概念名间接引用、不经规则号的依赖不在求法保证范围内。
38. (v2.4) 5.9 的 D.3 补齐起稿 / 五字段自校验 / `latest.md` 两子步, D.post 改为执行时按配置判断; `latest.md` 的改动单独成提交, 该提交产生之后请等待点 13b 并附其 diff —— 这是第 28 条「共享指针 `docs/handoff/latest.md` 的改动一律请裁」在 5.9 的落点 (v2.4 原写在原等待点 13 的授权请求里点明、不另立等待点, 与原第 13 项「同批」的时序冲突, v2.5 拆为 13a / 13b, 见第 40 条); 本仓 `latest.md` 当前没有字面名为 History 的表 (该节曾由 `16b5bf1` 按 SOT 加入、在合并提交 `ecb6296` 中丢失; 13b 的请求里注明来历, 恢复与否由 owner 裁), History prepend 按执行时实读的版式落 (track 表本轨行与说明段), 落点记台账。
39. (v2.4) 5.7 的 deliverables 去掉台账, 与姊妹任务 5.3 同口径 (只列本任务提交的文件); 台账的本任务追加仍随 5.8 第一条提交。post_planning R3 minor `638d2a0f` 的原意由此在 deliverables 一侧也闭合; R4 minor `f0e78a1e` 指出的 v2.3 revision_log 那句不实, 原文不改, 勘正写在 v2.4 条目里。
40. (v2.5) 原等待点 13 拆为 13a / 13b (post_planning R5 R5-M1): v1 起原第 13 项把 `release_gate` 的协调 ref 推送与 Phase D 提交双推捆成「同批」, v2.4 又要求在原第 13 项的请求里点明 `latest.md` 的 diff —— 原第 13 项须在 D.2b 用掉, 那时该 diff 还不存在, 照字面无合法下一步。owner 2026-09-17 的原意是 release 逐项授权 (yaml `hard_constraints` 第 3 条「新写 claim、`release_gate` 的 release / sweep / gc、推 master / tag / gitlink 仍逐项授权」), 「同批」捆绑本身就与它不符, 且从未登记为流程判断; 拆分后 13a 只含 release 的协调 ref 推送 (恢复逐项), 13b 在 `latest.md` 的单独提交产生之后才请、请求附其 diff, 第 28 条「共享指针一律请裁」由此可执行。代价: Phase D 多一次授权往返; 多出一个中间态 —— 13a 已批并已 release、13b 未批时, 协调 ref 上本轨已是 `done` 而归档与周期 handoff 只在本地, 原样记台账。`latest.md` 的 History 节曾由 `16b5bf1` 按 SOT 加入、在合并提交 `ecb6296` 中丢失, 13b 的请求里注明来历, 恢复与否由 owner 裁; `latest.md` 单独成提交的理由改写为「给 owner 一份可单独否决的共享指针 diff」, 不再以 5.9 不跑的 `commit_attribution` 为据。
41. (v2.5) claim 存活从「只在 1.1 核一次」改为「Phase B–D 每个会话入口核一次」(post_planning R5 R5-M2; yaml `hard_constraints` 第 4 条): 三元组解析 → 协调 ref 前置检查 → 把本地协调 ref 强制对齐到 origin 后重跑解析 → `--heartbeat-only` 并按 `coord_push_verify` 核验; 对齐后解析不到 `active` 或心跳返回 `claim_not_found` ⇒ 等待点 14 (挂载从 1.1 扩到任意会话), 前置检查或推后核验不过 ⇒ 等待点 15。强制对齐是本轮新加的一步 (交互检查查出): 心跳不自己 fetch, 本地协调 ref 落后 origin 时心跳叠在旧值上、推送非快进必失败 (resilient_push 的重取用非强制 refspec, 分叉即被拒), 被 sweep 成 `abandoned` 的 claim 在落后的本地值上也仍显示 `active` —— 两者都有 yaml `v2_state_runs` 的 N11 实测; 对齐只在前置检查退出 0 (本地领先的只有本轨心跳) 之后做, 丢的也只是它们。会话间隔超过 `SWEEP_TTL` (24h) 时 claim 可能已被 sweep, 入口核验只能事后发现、由等待点 14 补认领, 防不住这段时间里他容器把本轨看作无人认领。例外: 5.2 的 AB 会话不做入口核验 (推不出心跳, 两次快照之间不得 fetch), 由其前一个普通会话补一次核验过的心跳、其后第一个普通会话先做入口核验; 5.9 的 release 之后本轨已无 `active` claim, 不再做入口核验。5.9 的 release 遇 `claim_not_found` (`release_gate` 记为 benign、退出 0、什么都不推) 不按推送失败落等待点 15, 呈 owner 裁是否先补认领再 release。(v2.6 链接注: 强制对齐当时只写进了会话入口心跳, 已推广到全部写协调 ref 的动作, 见第 48 条。)
42. (v2.5) C.2.4.5 子模块指针闸 (post_planning R5 R5-M3): 本仓未配置 `phase_c_integrator.submodule_gate` ⇒ 缺省 `block`, 已启用; 它的自动触发挂在 branch-manager merge action 上, 主仓 PR 按约束 1 的主仓例外走 Forgejo 合并, 不会触发 ⇒ 5.8 由主控在 C.2.4 green 之后、Forgejo 合并之前在主仓根显式跑 `submodule_gate.sh` (mode 取执行时配置)。放行除退出 0 外还要看到逐子模块结论行 —— 脚本在没有 `.gitmodules` 的目录里会打印「trivially passes」并退出 0; block 与闸没跑成都停在新立的等待点 17, override 只由 owner 决定。闸拿 HEAD 与 `origin/master` 的 gitlink 直接比, 同步合并之后 `origin/master` 若又前进 (他轨 bump 了某子模块) 也会判 block, 是否重新同步后重跑由 owner 裁。(v2.6 链接注: override 的写法与裁后重跑的放行判据见第 49 条。)
43. (v2.5) 5.5 的 AB 复核补 feature 一侧并与 1.1 同口径 (post_planning R5 R5-M4 与 `1453c41f`): 上游一侧 (A..S3) 两端点先 `cat-file -e`、`diff` 看退出码 —— A 是全计划唯一隔会话从台账抄回的 SHA, 抄错时旧判据 (有输出才停) 按空输出放行, 静默跳过 Rule #6 重跑; feature 一侧比 W 之后两个 skill 目录与主仓 `ab-suite/audit-engine.json` 的改动 (5.4 第一次自检在 5.2 之后, 按设计会改本 cycle 的新增行), 非空时逐 hunk 按 Rule #6 判据表分类: 描述性 ⇒ substitute 记入 `rule6_note`, 处方性或拿不准 ⇒ 重跑 5.2。为此 5.2 的结果提交 SHA 记台账。
44. (v2.5) skill-creator 工作区只放主仓 `aria-plugin-benchmarks/ab-workspace/` (post_planning R5 R5-M5, 两个修法里按「新增交互更少」选 (a)): aria 侧 `skills/*-workspace/` 虽被 `aria/.gitignore` 忽略、躲过 porcelain, 却在 3.5 的 `grep -rn … aria/skills/` (SC-13) 与 `no-unresolved-version-placeholder` 的 `grep -rn … aria/` 两个递归检索面上 (`grep -r` 不认 `.gitignore`), 5.3 / 5.5 在 AB 之后重跑它们时会被工作区里的旧版快照误红。选址可由调用方指定: 生效 skill-creator 的 SKILL.md 只以散文给默认「as a sibling to the skill directory」(`:167`), 快照写法 `cp -r <skill-path> <workspace>/skill-snapshot/` 相对于工作区 (`:186`), `aggregate_benchmark.py` 与 `generate_review.py` 都只收调用方传入的目录; 先例 `3d3c820` 把 `ab-workspace/` 加进主仓 `.gitignore`, v1.69.0 那次 AB 的旧版快照即放在 `ab-workspace/…/skill-snapshot`。(b) (AB 后删 aria 侧工作区并在重跑前断言) 要多一个删除动作和至少两处断言, 且本机主仓已有一个早年 AB 留在 aria 侧的被忽略工作区 (`aria/skills/issue-triage-workspace/`, 2026-09-22 实测), 「断言无 `*-workspace` 目录」会误停, 故不选。(a) 只加一处断言: 5.2 两次快照的 `find aria/skills -maxdepth 1 -name '*-workspace'` 之差须为空。
45. (v2.5)「空输出即通过」全计划同族扫描 (owner 2026-09-22 点名): yaml `hard_constraints` 新增第 14 条判据命令的通用口径 (退出码先于输出、管道逐段看、比较两侧都看退出码、运行目录钉死、子模块先确认已检出), 另把退出 0 仍可能没比成的已知形态逐处写进条目 —— 1.1 基线复核的路径须至少在一端存在 (`aria_shifted` 原第 6 条三个文件名连写, 已拆开)、5.9 的 `owner-container` 粘贴前看退出码并加值非空检查、5.5 与 5.7 的 `no-unresolved-version-placeholder` 先确认当前目录、4.3 与 5.5 的 unittest 看 Ran 数、5.4 的检查器与 §4.5 命令看退出码; 各处 porcelain、`ls-remote --tags`、SC-13 计数、frontmatter 比较补退出码或正向断言; `coord_ref_precheck` / `commit_attribution` / `crlf_guard` 三段代码补退出码 (前两者新增退出 2)。dispatch 点名的两处之外, 交互检查另找出一处: 5.5 第 7 步复跑 L2 前原本不跑配置文件守卫, 已补。(v2.6 链接注: 本族还漏了「打印 `##SKIP##` 却仍退出 0」一形, 见第 50 条。)
46. (v2.6) 5.9 周期 handoff 的 `track-id` 取值加逐字断言, 并删去够不着的停点 (post_planning R6 `354faf33`, owner 2026-09-24 定级 minor): `head -8 <handoff> | grep -cxF 'track-id: pre-merge-completeness-gate-change-scope'` 的打印值须为 1。原写的「写错就判他轨、停在等待点 16」在 5.9 够不着 —— 那个判据只在 1.1 与 5.8 调用, 5.9 自己不跑它; 而 E1 的「字段在不在」与 v2.5 加的「值非空」对多写一个字母的 `track-id` 都照样满分 (本轮反事实实测), 只有逐字比对拦得住。按打印值判不按退出码判 (零命中时 `grep -c` 打印 0 并退出 1)。
47. (v2.6) 条目序号引用一律改锚点式 (post_planning R6 `6ad0a84b`): 「TASK-0NN 第 K 条 / 末条 / 上一条 / 下一条」这类写法在多轮返修里会随条目增删整体腐坏 —— 本轮实测出 10 处已经指错 (两处 v2.5 新写的「TASK-024 末条」实际要指的是取第二次快照那条, 两处「TASK-023 末条」实为并入上游那条, 两处「TASK-001 第 1 条」实为 claim 身份条, 三处相对引用指向相邻条, 一处从任务外部用「上一条」), 全部改为引用条目开头的字面锚点。机器清单 (扫描面 = 本文件全文 + 整份 yaml 树, 共 299 处引用, 逐处给判定) 由执笔报告呈主控。
48. (v2.6) 写协调 ref 之前一律先强制对齐 (post_planning R6 `2c2e8931`): yaml `hard_constraints` 第 4 条升为通则 —— 前置检查退出 0 之后、动手写或推之前先 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 并重跑三元组解析; 5.9 的 release 与 1.1 的重新认领本轮补上 (v2.5 只写进了会话入口心跳)。证据 = yaml `v2_state_runs` 新增的 N12: 同一分叉态下照原顺序直接 release 得 `released.success` 为真但 `push_success` 为假、远端不等于本地, 再跑前置检查即退出 1 (下一个会话卡在等待点 15); 先对齐再 release 则两者都为真。例外: 5.2 的 AB 会话带 `ARIA_COORDINATION_NO_PUSH`, 两次快照之间不得 fetch, 期间只写本地的心跳不对齐, 由 AB 之后的对齐整体丢弃。
49. (v2.6) C.2.4.5 的 override 口径按闸的调用时机改写 (post_planning R6 `749f8d15`): 闸读的是运行时 HEAD 的提交信息, 而本计划让它跑在 Forgejo 合并之前 (HEAD = PR head), 所以写进合并提交的 `Submodule-Rollback:` trailer 它看不见 —— owner 若裁 override, 两个修法各有代价: trailer 放进 PR head 那个提交 = 改写并强推已推送的 feature 分支, 与等待点 8 「不 force、不改写历史」冲突, 须 owner 一并裁准, 且分支 SHA 变了之后 C.2.4、本闸与 5.8 的提交范围核验都要重做; 改用 PR 标签 `submodule-rollback-approved` 则不动提交 (API 失败按无标签, 方向 fail-closed)。裁后重跑的放行 = 退出 0 且被 override 的子模块有 `GATE:` 行与其后的 `ALLOW:` 行, 其余子模块照旧 —— v2.5 的放行判据只认 `PASS:` 与 `OK:`, owner 裁了 override 也仍判「缺结论行」而停, 照字面无合法下一步。
50. (v2.6) custom checks 一律看输出首行, 不看退出码 (post_planning R6 `29325b2c`): `plugin-version-arch-docs-match` 读不到 `aria/.claude-plugin/plugin.json` 时打印 `##SKIP##` 并仍退出 0, `custom_checks.py` 把它映射为 skip (既不算通过也不算失败) —— 只看退出码会把没跑成当成过。六条点名 check 的期望首行逐条写进 5.7 的条目 (四条须 `OK`, `no-unresolved-version-placeholder` 通过时无输出, `plugin-cache-currency` 在 owner 更新缓存前首行 `STALE` 属预期)。这是第 45 条那次同族扫描的漏网形态, 本轮把「退出 0 却没跑成」的已知形态清单补齐。

---

## 外向动作与 owner 等待点

明细以 yaml `metadata.owner_gates` 为准; 本计划不预设任何一项已获授权。本容器已有 claim 的心跳刷新 (`--heartbeat-only`) 免逐次授权 (owner 2026-09-17), 前提是推送前协调 ref 前置检查通过并已强制对齐到 origin (v2.6, 见判断清单第 48 条)、且推送后按 yaml `metadata.coord_push_verify` 核验通过 (两者都落在第 15 行), 不在本表; v2.5 起 Phase B–D 每个会话入口都做一次这类心跳 (yaml `hard_constraints` 第 4 条, 判断清单第 41 条); 新写 claim 与 `release_gate` 仍逐项授权。

| 编号 | 任务 | 性质 | 方式 |
|---|---|---|---|
| 1 | 1.1 | owner 裁定: 10CG/Aria#195 已完成 C.2 或明示改序 | 会话内明示 |
| 2 | 1.1 | 推送: 主仓规划提交推两端 (先并入 `origin/master`, 提交清单随请求呈上) | 逐项授权 |
| 3 | 组 1–4 (条件) | owner 裁定: B.2 出现 spec 漂移信号 | AskUserQuestion |
| 4 | 5.2 | owner 启动: 以 `ARIA_COORDINATION_NO_PUSH=1` 启动 AB 会话, 结束后换会话 | 会话级前置, 会话内补不上 |
| 5 | 5.2 | owner 裁定: 任一套件判回归, 或 audit-engine 套件 delta ≤ 0, 或 eval id 3 未转差 | AskUserQuestion |
| 6 | 5.1 / 5.3 / 5.5 | 停下上报: 并入上游冲突 / 取号被占 / 合并冲突 / 终核不符 / 合并树回归不过 / AB 后上游改了两个 skill 目录 / AB 后 feature 一侧含处方性或拿不准的改动 / AB 复核没比成 (cat-file 或 diff 退出非 0) | 先例指针 aria `ec72175`, owner 确认后重走 |
| 7 | 5.6 | 推送: aria master 与 tag 双推 | 逐项授权 |
| 8 | 5.6 / 5.8 / 5.9 | 停下上报: 推送被拒 / 只推成一个 | 不 force, 不 bump gitlink |
| 9 | 5.8 | 推送与发帖: 主仓分支、PR、合并、C.2.5 双推 | 逐项授权 |
| 10 | 5.9 | 发帖: 七张 issue | 逐张授权 |
| 11 | 5.9 | owner 裁定: 归档 Step 7 建不建 tracker | AskUserQuestion |
| 12 | 5.9 | 发帖: 10CG/Aria#199 与 10CG/aria-plugin#161 回帖关闭 | 逐项授权 |
| 13a | 5.9 (D.2b, release 之前) | 推送: `release_gate` 释放本轨 claim 的协调 ref 推送 (只此一项) | 逐项授权 (v2.5 起不与 Phase D 提交同批); 未授权 ⇒ 不 release, 记周期 handoff |
| 13b | 5.9 (`latest.md` 的单独提交产生之后) | 推送: Phase D 提交双推 (归档、周期 handoff、单独成提交的 `latest.md`), 请求附 `latest.md` 提交的 diff | 逐项授权; 未授权 ⇒ 留本地 |
| 14 | 1.1 与任一会话的入口 claim 核验、5.9 的 release (条件: 三元组解析不到本容器同轨的 `active` claim —— `done` / `yielded` / `abandoned` 任一终态, 或本容器该轨无 claim; 或心跳 / release 返回 `claim_not_found`) | 推送: 用原串重新认领 | 逐项授权; 未授权 ⇒ 不认领, 停在当前任务 (5.9 的 release 可由 owner 裁为不补认领) |
| 15 | 1.1 / 5.2 / 5.9 与各会话的入口 claim 核验 (调用 `/state-scanner` 之前) | 停下请授权: 本地协调 ref 领先的提交含本轨心跳以外的写入; 或协调 ref **推后核验不过** (`push_success` 非真 / 不带 `--no-push` 却 `push_skipped` 为真 / `ls-remote` 与本地不一致且本地不是远端祖先) | 心跳不推、不对齐, 不重试不 force, 请 owner 裁 |
| 16 | 1.1 / 5.8 | owner 裁定: 待推送的主仓提交含非本轨提交, 或含只落发布同步面又无本轨 `Spec:` trailer 的提交 (可能是他轨 `chore(release)`, 也可能是本轨 5.7 或 5.1 漏写) | 清单与 kinds 呈 owner, 未裁不推送 |
| 17 | 5.8 | 停下上报: C.2.4.5 子模块指针闸没放行 (block、闸没跑成, 或缺逐子模块结论行) | 不合并; override 只由 owner 决定, trailer 须落在 PR head 那个提交上或改用 PR 标签, 裁后重跑的放行判据见判断清单第 49 条 |

## 范围边界

| 事项 | 归属 |
|---|---|
| 组 1–5 | 本文件 |
| Phase B 入口认领 | 判断清单第 11 条; raw track-id 逐字为 `pre-merge-completeness-gate-change-scope`, 不补容器后缀 |
| C.2.4 pre-merge gate (Rule #8) / C.2.4.5 子模块指针闸 / C.2.5 | `phase-c-integrator`, 由 5.8 调用; C.2.4.5 的自动触发挂在 branch-manager merge action 上, 主仓 PR 走 Forgejo 合并不经过它, 由主控在 Forgejo 合并前显式跑其脚本 (yaml TASK-030) |
| 产出侧四个调用方对齐 / `--no-spec` 加固 / F8 注册面 / 写侧命名强制 / config-loader 程序化入口 / catalog node id 修正 | **不在本文件**, 只在 5.9 开 issue |
| 可配置下界 N; 本仓 `pre_merge` 配置 | 不做 (裁定 3); 保持 `off` (proposal F1) |

---

执行序: 编号序 1.1 → 5.9, 单执行席串行 (yaml `metadata.execution_order`); 唯一例外是 5.4 分两次。

## 1. B.1 入口、基线复核与测试先行

- [ ] 1.1 B.1 入口: owner 等待点 → 按 (本容器, 归一 track_id, `active`) 三元组解析本轨 claim, 过协调 ref 前置检查并强制对齐到 origin 后以 `--heartbeat-only` 刷新、并按 yaml `metadata.coord_push_verify` 核验推成了没有 (解析不到 `active` 且未获重认领授权则停) → fetch 后实测 aria 与主仓 `origin/master`, 定分支起点 (回落时核提交归属) → 按 yaml 触点清单重跑基线 diff (**aria / 主仓 / standards 三组**, standards 组对 B.1 当时 gitlink 重测) → 建台账骨架 — 台账
- [ ] 1.2 语料冻结 `corpus-freeze.md` (本目录): 取样命令与时刻、六族样本、双列标注 (frontmatter 定序与归一化 / 名匹配)、按族分流的机械仲裁与争议表; 标注由非实现者完成, 复现由另一实例核对 — SC-2 / SC-4 前置
- [ ] 1.3 fixture 前提矩阵: SC-1~SC-22 逐格列 mode、Level 行、`audit.enabled`、两个路径参数、作用域来源与 carve-out, 写入读前必看第 6、7、9、23 条的口径; 每个格包在 `subTest(cell=...)` 里并照用阶段子格名; 测试一律 `unittest.TestCase`, 不 import pytest、不建 conftest.py — 台账
- [ ] 1.4 新建 `tests/test_completeness_gate.py` 第一批: SC-1~SC-6 — RED
- [ ] 1.5 第二批: SC-7~SC-10 与 SC-18 (排除分支) — RED
- [ ] 1.6 第三批: SC-15~SC-17 与 SC-19~SC-22 (SC-15(5) 与 SC-17(5) 按读前必看第 6、7 条) — RED
- [ ] 1.7 RED 台账: 全文件对基线逐条实跑, 失败形态为 AssertionError, 阶段子格全部被执行且失败; `run_all_tests.sh --list` 仍列 audit-engine 为 `(unittest)`; 主控提交测试文件与 `corpus-freeze.md` — 台账

## 2. 实现 `scripts/completeness_gate.py` (按 §1.0 求值总序, stdlib only; 2.1–2.4 只验收各自的阶段子格, SC 方法级全绿在 2.5)

- [ ] 2.1 CLI 与 P0 / P1: 必填与可选参数及互斥, config 直读加内联缺省与旧配置兼容映射, 格 A, 两面 toplevel 判同仓, stdout 只出 16 键 JSON、人读行走 stderr, exit code 与短路框架 — 阶段子格 (SC-10 / SC-15(1) / SC-17(7) / SC-21)
- [ ] 2.2 P2a 与 P2: `--no-spec` 锚点面前置核验, S1 锚点逐字比对与 `allow_dangling_change_ids` 继承, S2 锚点面 `--no-renames` diff, S3 / S4, 两个 base 轴的陈旧告警, `git_failed` — 阶段子格 (SC-5(8) / SC-7 / SC-17(4)(5) / SC-22(3))
- [ ] 2.3 P3 与 P4: Level 三条判据, 五档优先级链, 五项排除, 逐对纳入与按需求 Level, `dangling-skip` — 阶段子格 (SC-15(5) / SC-20(3))
- [ ] 2.4 P5 与早退型豁免: 格 B / C / D / E 与归约 R-1 / R-2, S4 / `spec_level_undetermined` / `no_spec_unverifiable` 的豁免 (含裁定 11) 与短路, 读前必看第 8 条的取值 — 阶段子格 (SC-7(e) / SC-9 / SC-15 / SC-17(5))
- [ ] 2.5 P6: 归属规则 1–3, 顶层 `iterdir()` 与目录缺失, 两个排除计数与 `unattributed`, 三态与 (b)(c) 通道, trail 行与前 20 截断, missing 的豁免降级 — SC-1~SC-22 的单测方法全绿
- [ ] 2.6 组 2 收口: 新测试文件与 audit-engine 既有测试全绿后, 主控只提交脚本与测试文件并记 SHA — 台账

## 3. 规程与文档同步 (Rule #3)

- [ ] 3.1 `execution-modes.md`: §入口逻辑 `:10` 改读优先级链并取上界; §Pre-merge 互补说明、Step 1 注、Step 2 改写、Step 3 五项排除与枚举源、Step 4-5 改为调用 `scripts/completeness_gate.py` 的命令行与三态路由并逐字写入消费方 fail-closed 义务 (五个 Step 标记与围栏保留); 三态失败模板 (Fix 四项); `:44` 与 `:82` 豁免文案统一 — SC-13 / N1 / N2
- [ ] 3.2 `audit-engine/SKILL.md`: 输入参数表补五项; 在 fenced bash 块内调用 `aria/skills/audit-engine/scripts/completeness_gate.py` (调用串照抄 yaml 的 canonical, 与 3.1 相同); `:381-384` 与 `:385-388` 两个注释块各补一句; `:423` 同形改写; 相关文档加契约指针 — SC-13 / SC-12 liveness / N4 / N8
- [ ] 3.3 `phase-c-integrator/SKILL.md` (CRLF, 保持行尾): 步骤 3 改为五档优先级链 (convergence / challenge 照常调用门), `:57` 与 `:754` 同形改写, pre_hook 向 `scripts/completeness_gate.py` 传五个参数, 步骤 4.5 三态处置, `:157` 勘正 — SC-13 / N7 / N8
- [ ] 3.4 旧 schema 散文残留清零 (`phase-a-planner:267`、`phase-b-developer:204,277`, 后者为 CRLF; 第四处 `phase-c-integrator:157` 由 3.3 落); `report-storage.md` §向后兼容补四句; `pre-write-validation.md:3` 补 change 维度 — SC-13
- [ ] 3.5 文档机检: SC-13 全部条目与 N1 / N2 / N4 / N7 / N8 在组 3 改动后全真, **四份**被改 SKILL.md (`audit-engine` / `phase-c-integrator` / `phase-b-developer` / `phase-a-planner`) 的 frontmatter 不变; 主控提交组 3 改动 — 台账

## 4. 反事实、回归与活体运行

- [ ] 4.1 反事实第一批 (SC-1~SC-10、SC-18): 既非实现者也非测试作者的新实例在 2.6 SHA 的一次性副本上三步法实跑, 一律 `python3 -B` — 台账
- [ ] 4.2 反事实第二批 (SC-15~SC-17、SC-19~SC-22), 做法同 4.1 — 台账
- [ ] 4.3 回归: SC-12 三条命令零失败且 Ran 数不少于基线 (state-scanner 那条不带 `ARIA_COORDINATION_NO_PUSH`); 配置文件守卫 (钉在主仓根, 退出码为 0 或 1 且无命中行) 通过后, 重写 a 的 L2 / L3 为真、L1 在全勾选副本上为真; catalog 5/8 可执行 fixture 的三条命令 OK — 台账
- [ ] 4.4 活体 dogfood (SC-11) 与 SC-6 自证 (重写 c 的快照格与对照) — 台账与周期 handoff

## 5. Rule #6 AB、发布与收尾 (5.4 第二次在 5.9 内)

- [ ] 5.1 AB 套件编辑: `audit-engine.json` 新增定向 eval id 3 并把文件内 `version` 改为 1.1.0; `version.yaml` 升到当时现值的下一个 MINOR, 两个计数程序化重算; 开 AB 会话前把 aria `origin/master` 并入 feature 并重跑 3.5 与 4.3; 主控提交时必须带本轨 `Spec:` trailer 并回读确认 (两个交付物都在发布同步面, 结构上不含本轨专属路径, 漏写会在 5.8 判 `shared-only` 而停) — rule6_note
- [ ] 5.2 Rule #6 照跑 (两读法并集, 经 `/skill-creator`): 前置 = owner 以 `ARIA_COORDINATION_NO_PUSH=1` 启动会话, aria `origin/master` 已在 feature 里; 写 PREDICTION.md 并取副作用快照; `audit-engine.json` 与 `phase-c-integrator.json` 按描述性推演两臂照跑, 两套件逐 eval 无回归, audit-engine 套件 delta > 0 且 eval id 3 的 without 臂低于 with 臂; 结束后过协调 ref 前置检查才对齐; catalog 三条命令与三条缺口写进 README; 结果落 `aria-plugin-benchmarks/ab-results/` (5.9 勾选时换成本次结果目录全路径) — SC-14
- [ ] 5.3 版本与 CHANGELOG: 上游在 5.1 之后又前进时先并入 feature (merge, 不 rebase) 并重跑 3.5 与 4.3; 再取 MINOR 号改版本 SOT 5 文件 (记取号时 SHA); CHANGELOG 写十三条迁移文案 (§5 第 2、10 条按读前必看第 7 条) — 台账
- [ ] 5.4 引用与编号写法自检, 两次 (5.5 前; 周期 handoff 与回帖落笔前): 本 cycle 新增行的 issue 引用全限定、文内编号不用 `#` 与带圈字符 — 台账
- [ ] 5.5 aria 本地合并: fetch → 断言 feature 分支干净 → master 对齐 `origin/master` 并记 SHA → 取号与 AB 基线复核 (上游与 feature 两侧) → `git merge --no-ff` 并断言本轮双父合并提交 → 取号终核 → 合并树原位回归 → 打 tag; 任一步不成立即停下上报 — 台账
- [ ] 5.6 aria 双推: owner 授权后每个远端一条原子推送 (master 与 tag, 先 origin 后 github), 推后逐 remote `ls-remote` 核 master 与 tag; 被拒或只推成一个即停下上报 — 台账
- [ ] 5.7 主仓同步面: aria gitlink 取 5.6 核验后的 SHA (只前进), 16 个版本点 (含 `VERSION:24`), custom checks 复跑 (判通过看输出首行, `##SKIP##` 算没跑成); 主控在主仓 feature 分支只提交上述九个版本同步面文件 (台账追加随 5.8 一并提交), 提交信息带本轨 `Spec:` trailer 并回读确认 (这九个文件整条落在发布同步面, 漏写会在 5.8 的提交归属核验里判 `shared-only` 而停) — 台账
- [ ] 5.8 主仓 PR: 工作树与提交范围核验 (提交清单随授权请求呈上), merge 不 rebase, PR 过 C.2.4 pre-merge gate 与 C.2.4.5 子模块指针闸 (主控在 Forgejo 合并前显式跑, 没放行即停; override 由 owner 裁, trailer 须在 PR head 提交上) 后以 merge commit 合并; 合并后本地 master 快进并核对合并提交, 断言三个子模块无待推内容后交 C.2.5 双推与 parity, 再复核版本点与 ab-suite 计数 — 台账
- [ ] 5.9 Phase D (手写, 与 phase-d-closer 逐步对应): 开七张 issue 并回填台账; 主控一次勾选全部 checkbox; post_closure 审计按执行时配置处置 (`off` 则跳过); 归档预演并复跑重写 a 的 L1–L3; Step 7 由 owner 裁; release 之前单独请等待点 13a, 过协调 ref 前置检查并强制对齐后 `release_gate` 释放 claim 并按 `metadata.coord_push_verify` 核验推成了没有 (不带 sweep / gc; 遇 `claim_not_found` 呈 owner, 不按推送失败处置); estimator 采集; 10CG/Aria#199 与 10CG/aria-plugin#161 回帖关闭; 周期 handoff 按模板起稿并照录判断清单 (frontmatter 五字段写全, `track-id` 逐字写本 spec id 并用 `grep -cxF` 断言取值为 1), 写后跑五字段自校验 (`head -8` 窗口, 须为 5), 再做 `docs/handoff/latest.md` 两子步 (History prepend 恒做; pointer 按判定表, follower 不改; 单独成提交); `latest.md` 提交产生之后请等待点 13b (请求附其 diff), 获授权后 Phase D 提交双推并逐 remote 核验 — 台账

---

## Success Criteria ↔ 任务映射

| SC | RED | 转绿 | 反事实 / 回归 / 活体 |
|---|---|---|---|
| SC-1 | 1.4 | 2.5 | 4.1 |
| SC-2 | 1.2 + 1.4 | 2.5 | 4.1 |
| SC-3 | 1.4 | 2.5 | 4.1 |
| SC-4 | 1.2 + 1.4 | 2.5 | 4.1 |
| SC-5 | 1.4 | 2.5 (子格 2.2) | 4.1 |
| SC-6 | 1.4 (hermetic 四格) | 2.5 | 4.1; 4.4 (重写 c) |
| SC-7 | 1.5 | 2.5 (子格 2.2 / 2.4) | 4.1 |
| SC-8 | 1.5 | 2.5 | 4.1 |
| SC-9 | 1.5 | 2.5 (子格 2.4) | 4.1 |
| SC-10 | 1.5 | 2.5 (子格 2.1) | 4.1; 5.5 |
| SC-11 | — | — | 4.4 |
| SC-12 | — | — | 4.3; 5.5; 5.9 (重写 a) |
| SC-13 | — | 3.1–3.4 | 3.5; 5.5 |
| SC-14 | — | — | 4.3 (catalog); 5.1; 5.2; 5.9 (缺口 issue) |
| SC-15 | 1.6 | 2.5 (子格 2.1 / 2.3 / 2.4) | 4.2 |
| SC-16 | 1.6 | 2.5 | 4.2 |
| SC-17 | 1.6 | 2.5 (子格 2.1 / 2.2 / 2.4) | 4.2 |
| SC-18 | 1.5 | 2.5 | 4.1 |
| SC-19 | 1.6 | 2.5 | 4.2 |
| SC-20 | 1.6 | 2.5 (子格 2.3) | 4.2 |
| SC-21 | 1.6 | 2.5 (子格 2.1) | 4.2 |
| SC-22 | 1.6 | 2.5 (子格 2.2) | 4.2 |
| N1 / N2 / N4 / N7 / N8 (新增) | — | 3.1–3.4 | 3.5; 5.5 |
| N3 (新增) | — | 2.1 | 2.6; 5.5 |
| N10 (新增) | — | — | 4.3; 5.9 |

## 内联 Tasks (17 项) ↔ 新编号

| 序 | proposal 行 | 内联项 | 新编号 |
|---|---|---|---|
| 1 | `:409` | B.0 语料冻结 (含第 5 条前置门) | 1.2; 前置门见读前必看第 18 条 |
| 2 | `:429` | 测试风格 unittest | 1.3; 1.7 |
| 3 | `:430` | SC fixture 前提回扫 | 1.3; 1.4–1.6 |
| 4 | `:431` | TDD RED | 1.4–1.7 |
| 5 | `:432` | 实现脚本 | 2.1–2.6 |
| 6 | `:433` | §入口逻辑 `:9-10` | 3.1 |
| 7 | `:434` | §Pre-merge | 3.1 |
| 8 | `:435` | audit-engine SKILL.md | 3.2 |
| 9 | `:436` | phase-c-integrator SKILL.md | 3.3 |
| 10 | `:437` | 旧 schema 残留 4 处 | 3.3 + 3.4; 3.5 |
| 11 | `:438` | report-storage + pre-write-validation | 3.4 |
| 12 | `:439-446` | AB 两读法并集 | 4.3; 5.1; 5.2; 5.9 |
| 13 | `:447` | 枚举范围两条边界 | 2.5; 3.4; 3.5 |
| 14 | `:448` | 活体 dogfood | 4.4 |
| 15 | `:449` | ship 前基线重取 | 1.1; 5.5; 5.7 |
| 16 | `:450` | 版本 | 5.3; 5.7 |
| 17 | `:451` | Phase D | 5.4; 5.9 |
