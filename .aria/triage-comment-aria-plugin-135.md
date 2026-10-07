本评论按 owner 2026-09-30 决策单 (10CG/Aria 主仓 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`) 第 6 项「issue 卫生清扫」做核验, 目的是确认 `10CG/aria-plugin#135` 是否已修或与他单重复。结论: 部分已修 (缺口 3 的分组键读取侧, v1.70.0), 整单未修, 也不是重复, 建议保持 open; 未修子项见文末。

## Triage Report

**Verdict**: `partial-repro` | **Severity**: `major` | **Recommended Action**: `next-cycle`

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.63.0` |
| Current | `1.74.1` (aria-plugin master `268da8f`, origin 与 github 两端 `git ls-remote` 一致) |
| Gap | behind |

报告版本落后当前 11 个 minor。其间与本单相关的发版至少四次: v1.69.0 (audit-engine 竞品 spec 探针, 其 Spec `sibling-spec-probe` 自述与本单相关但不关闭本单) / v1.70.0 (缺口 3 读取侧, CHANGELOG 里唯一点名本单的一版) / v1.71.0 (A.1 入口认领, 未点名本单) / v1.73.2 (提交 `75dc994`, `10CG/aria-plugin#197`: 扫描时本地 `refs/aria/coordination` 快进到 origin, 此前只写 FETCH_HEAD、本地 ref 不动)。另注: 按编号 135 做 `git log --grep` 还会命中 `49722ef` / `23390e8`, 它们属于 `10CG/Aria#135` (interrupt collector 识别 git rebase), 与本单无关。

### Code Path

路径约定: 除注明仓名外, 下文路径均为 10CG/aria-plugin 仓内相对路径。

triage.py 的 step3 把 5 个引用路径全判为 `file not found`, 原因是 issue 写的是裸文件名或外仓路径 (collector 的 miss, 不代表引用失真): `scan.py` / `phase1_gate.py` / `release_gate.py` 实际在 `skills/state-scanner/scripts/`, `session-handoff.md` 在 10CG/aria-standards 仓的 `conventions/`, `docs/operations/multi-container-coordination.md` 属 10CG/nexus 仓 (本次未核)。人工核对: issue 描述与 v1.74.1 代码相符 —— snapshot 顶层键集 (`skills/state-scanner/scripts/scan.py:405-428`) 仍无 claims 字段, `get_container_id()` 仍是 `label if label else uuid` (`skills/state-scanner/lib/identity.py:223`)。

### Git History

step4 因 step3 未解析出路径而 skipped (`likely_fix_candidates: []` 是空转), 改为按主题在 aria-plugin 仓人工核查。下列提交均在 origin/master 与 github/master (两端 master 均为 `268da8f`, 已用 `git ls-remote` 核对):

| 提交 | 内容 |
|------|------|
| `5fbb974` / merge `0545f86` (v1.70.0) | 缺口 3: owner-container 两段式解析 + `identity_key` + `identity_advisories[]` + `get_container_label()` + `label_migration` 告警; 同批修复独立的解析缺陷 `10CG/aria-plugin#170` (已关闭) |
| `4b75921` / `0ae207f` (v1.71.0) | `get_container_uuid()` (恒取 uuid) / `heartbeat_by_track()` |
| `985e629` (v1.71.0) | A.1 入口认领 (phase-a-planner / spec-drafter); 只对 Spec 驱动 (Level 2/3) 的工作前移了触点, 缺口 1 未触及 |
| `75dc994` (v1.73.2) | 扫描时本地 `refs/aria/coordination` 快进到 origin (`10CG/aria-plugin#197`) —— 缺口 1「fetch 已经做了」的前提至此才真正成立; 解析与展示仍未做 |

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (`10CG/aria-plugin` / `10CG/Aria` / `10CG/aria-standards` / `10CG/aria-orchestrator` 四仓的 open PR 均为 0) |
| Local branches | none 相关 (未合并的远端分支: aria-plugin 仓 secret-guard 与 exfil 语料两条, 10CG/Aria 仓 `aria/DEMO-001` / `aria/DEMO-002` 两条, aria-standards 仓 secret-guard 一条, 均与本单无关) |
| Worktrees | 仅主 checkout; 10CG/Aria 仓的 `openspec/changes/` 下无协调相关在制 Spec |

已把四仓全部 open issue (`10CG/aria-plugin` 76 + `10CG/Aria` 46 + `10CG/aria-standards` 6 + `10CG/aria-orchestrator` 2) 按标题与正文在本地过滤: 除本单外没有 issue 专门承接缺口 1 (快照解析 claim) 或缺口 2 (ops leaf 任务认领)。`10CG/Aria#198` 只承接 label 陷阱 (S2 flip, 即 `get_container_id()` 改 uuid 优先)。相关但不构成重复的有:

1. `10CG/aria-plugin#109`: 其建议 1 (把认领 / 查重触点前移到从 `/state-scanner` 选定工作项的那一刻) 与缺口 2 的第一方案 (触点前移到阶段 3 确认任一执行项, 下称 2a; 手动认领指引为替代方案 2b) 同向, 2a 范围更宽, 不限 issue; 修 2a 时应一并回应该单; 但它不含快照解析与 ops leaf 场景, 不构成整单重复。
2. `10CG/aria-standards#19`: owner-container 与 claim container 段口径 (规范侧), 其正文把本单列为「代码侧」对应, 本单状态变化时应同步通知该单。
3. `10CG/aria-orchestrator#31`: 自主 bot 派活时强制认领 (插件管不到); 与缺口 2 同属「部分工作不经认领闸门」一族, 是其 Layer 2 一侧。
4. `10CG/aria-plugin#166`: 跨容器定向 release, 与评论 18823 的孤儿 claim 恢复相关 (见文末未修子项第 5 条)。
5. `10CG/aria-plugin#165`: B.0 的 YAML 键呈现强度, 其正文自述不含本单的三个缺口。

### Reproduction

**Mode**: `auto` | **Hit rate**: `7/8`

在 `/tmp` 实验目录 (v1.74.1 插件副本 + 本地 bare origin + 独立 HOME) 复跑, 并经另一轮独立复跑核对, 真仓零写入:

- case-1 (缺口 1, 快照不解析 claim) 复现: 容器 A 用 `phase1_gate.py` 写 active claim 并推到 origin; 容器 B 跑 `scan.py`, exit 0、`coordination_ref_present: true`, 但快照 23 个顶层键里没有 claims 字段, 整份 JSON 里找不到 A 的 track id 与 uuid, `tracks_multibranch.collision.kind: none`。代码侧同样: `skills/state-scanner/scripts/` 下的 `scan.py` / `collectors/` / `renderers/` / `writers/` 对 `read_claims` 零调用 (调用方只有 `phase1_gate.py`、`release_gate.py` 与 `skills/state-scanner/lib/` 内部)。核验补充: B 扫描后其本地 `refs/aria/coordination` 已含 A 的 claim 文件 (v1.73.2 的效果), 数据已在本地, 快照仍零提及。
- case-2 (缺口 1, 只有 gate 能读到) 复现: 容器 B 对同名 track 调 gate 得 `surface.kind: occupied` (提示容器 A 已认领)。claim 只有在 B 主动以同名 track-id 调 gate 时才可见; `skills/state-scanner/references/` 与 `skills/state-scanner/RECOMMENDATION_RULES.md` 对 occupied 零命中, 渲染约定只存在于 `skills/state-scanner/SKILL.md:171` 对 gate JSON 的消费段。另: `skills/state-scanner/SKILL.md:149` 规定阶段 2 进入 Phase B 时只在 `tracks_multibranch.collision.kind` 非空才调 gate, 该字段来自 handoff frontmatter 而非 claim; case-1 状态下 kind 为 none, 按契约 state-scanner 这条路径根本不调 gate, 只剩 `skills/phase-b-developer/SKILL.md` 的 B.0 兜底 (也只覆盖进 Phase B 的工作)。
- case-3 (缺口 2, ops leaf 无认领路径) 复现: acquire 触点现为 A.1 (`skills/phase-a-planner/SKILL.md:65`, `skills/spec-drafter/SKILL.md:83`, v1.71.0 新增) 与 Phase B (`skills/phase-b-developer/SKILL.md:91`, `skills/state-scanner/SKILL.md:157`, `skills/branch-manager/SKILL.md:149`)。A.1 有成文 skip: `skills/phase-a-planner/SKILL.md:127` (Level 1 命中则零调用) 与 `skills/spec-drafter/SKILL.md:29` (typo / 格式修复属 Level 1, 直接跳过 A.1); 无 Spec 的 leaf 任务本就不经 A.1。`skills/workflow-runner/SKILL.md` 对 coordination / claim 零命中; 在 10CG/aria-plugin 仓、10CG/Aria 的 `docs/`、10CG/aria-standards 的 `conventions/` 中均无 ops leaf 手动认领指引。CLI 本身接受任意 track 与 phase (`--phase ops` 得 `outcome: passed`), 缺的是编排层接线与文档。
- case-4 (缺口 3, 不同机器同主机名) issue 举的例子不复现: `lib.collision.classify()` 对 `simonfish/dev-claude2` 与 `creationhikari/dev-claude2` 判 `cross_owner` (`identity_key` 对主机名型容器保留 owner 段, `skills/state-scanner/lib/collision.py:96-113`); 同 uuid 容器 git owner 漂移 (即已关闭的 `10CG/Aria#193` 所述形态) 判 `none`, `identity_drift_advisories()` 给出 1 条信息级 advisory; 两台真实 uuid 机判 `cross_owner`。collision 相关 4 个 unittest 模块 (`test_collision_frozen_corpus` 7 / `test_handoff_multibranch_collision_dedupe` 23 / `test_track_board_advisories` 5 / `test_p1_layer_h` 24, 均在 `skills/state-scanner/tests/`) 共 59 用例全绿; `test_collision.py` 为 pytest 风格 (unittest 下 Ran 0), 用 pytest 跑 28 passed。补充 (核验发现, 不计入命中率): 「不再误并」只对 owner 不同的同名异机成立 —— `identity_key` 只对 uuid 容器丢掉 owner 段, 主机名型 (及自定义 label 型) 容器保留 owner 段, 所以同 owner 且同主机名 (或同 label) 的两台机器仍合成同一个 `identity_key`, `classify()` 判 `none`, 真实碰撞被漏报; 这一半归缺口 3 残余「主机名 / label 不进键」。
- case-5 (缺口 3, 一机两名) 仍复现, 严重度降低: `simonfish/dev-claude2` (主机名) 与 `simonfish/bfe8285d` (uuid) 仍是两个 `identity_key`, 判 soft hint 级 `self_multi_container`, 不再是硬碰撞, 但无法把主机名串与 uuid 串合并 (10CG/Aria 仓 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/proposal.md` 的非目标: 不推断、不引入映射表)。历史行经 `LAYER_H_ACTIVE_WINDOW_DAYS=30` 窗口退场, 但 label 优先 (见 case-6) 会持续产生新的别名对。
- case-6 (评论 18823, label 陷阱 release) 复现: uuid 身份认领后, 按 `container-id` 文件头的旧邀请语加 `label: dev-claude2`, 同机 `release_gate.py` 得 `claim_not_found` (benign, exit 0), claim 留在 `claims/<uuid>/` 成孤儿。输出带 `label_migration` 告警, 但它只数 `claims/<label>/` 下的 active (此处为 0), 看不见被孤立的那条。对照: 清空 label 后同一 release 成功 (`success: true`, status done)。`skills/state-scanner/tests/test_identity_label.py` 的 `TestS1LockIn` 把「label 优先」钉为 S1 预期, 是被刻意保留的。
- case-7 (评论 18823, label 陷阱 heartbeat) 复现: 同状态下 `--heartbeat-only` 得 `outcome: error` / `claim_not_found`; release 与 heartbeat 都只按单键 `rec.container == resolved.container_id` 匹配 (`skills/state-scanner/lib/claim_lifecycle.py:426`, `:541`)。评论 18823 的时间线只实测了 release, 其建议 2 已点名 release / heartbeat 双键匹配; 本次实测证实 heartbeat 路径同样中招, 且该路径不输出 `label_migration`。
- case-8 (缺口 3, `derive_container_id` 与单一来源) 仍缺: aria-plugin 与 aria-standards 两仓零命中 `derive_container_id`; `skills/state-scanner/lib/__init__.py` 未导出 `get_container_uuid` / `get_container_label` (`get_container_uuid()` 目前没有非测试的调用方); handoff 的 owner-container 经 `skills/session-closer/scripts/handoff_autofill.py:391-411` 走 `get_identity()` -> `get_container_id()` (label 优先) 生成; A.1 的 track-id 仍由 prose 要求手工拼接 (`skills/phase-a-planner/SKILL.md:79-81`)。

**deviation_note**: 本单写于 v1.63.0, 与 v1.74.1 现状相比:

1. 缺口 3 读取侧 (collision 分组键) 已由 v1.70.0 修复: owner 不同的同名异机不再误并; 同 owner 同主机名 (或同 owner 同一自定义 label) 的两台机器仍合成同一个 `identity_key`, `classify()` 判 `none`, 这一半归缺口 3 残余「主机名 / label 不进键」; 「一机两名」降为 soft hint 级仍成立。
2. 缺口 2 的「闸门仅 Phase B」前提已变为 A.1 + Phase B 两个触点, 但 Level 1 被成文 skip、无 Spec 的 leaf 任务本就不经 A.1, 本单点名的 ops leaf 场景仍无认领路径。
3. 缺口 1 的解析与展示零进展; 但原描述「fetch 已经做了」在 v1.63.0 并不完全成立 (只写 FETCH_HEAD), v1.73.2 起扫描会快进本地 ref —— 实验中 B 扫描后本地 `refs/aria/coordination` 已含 A 的 claim 文件, 快照仍零提及。
4. 评论 18823 的 label 陷阱在 S1 只加了告警与 inventory、刻意未改匹配语义, 仍复现。
5. `derive_container_id` / 单一来源建议未做。

### Verdict Rationale

缺口 3 的分组键读取侧与评论 21988 自述的 S1 各项确已在 v1.70.0 落地并在两端 master (自述属实), 但「不再误并」只对 owner 不同的同名异机成立。缺口 1 的解析与展示、缺口 2 的 ops leaf 部分没有任何改动, 评论 21988 里「缺口 1 / 缺口 2 均留」至今成立: 归档 Spec owner-container-identity-key-and-collision-parser 的非目标把二者指给 a1-entry 处置, 而 a1-entry 的 proposal.md 不含本单编号、只对 Spec 驱动的工作前移触点, 缺口 1 没有被任何一份 Spec 认领。label 陷阱被 S1 刻意保留, 由 `10CG/Aria#198` 承载, 该单仍 open、0 评论, 且 `10CG/Aria#174` 上的 SC-3 改写 ack 自 2026-09-06 起无回复。因此不是 `fixed-in-X` (关键项未修), 也不是重复 (没有另一单完整覆盖), 取 `partial-repro`。

### 未修子项 (建议本单保持 open)

reporter 把缺口 1 (1a + 1b) 整体列为最关键, 并指出「fetch 已经做了, 只差解析和展示」, 不动 claim 存储与仲裁语义。

1. 缺口 1a: snapshot 顶层 `coordination_claims[]` —— 未做。
2. 缺口 1b: 推荐区对「他人 active 且与候选工作重叠」的 claim 渲染 advisory 告警行 —— 未做。
3. 缺口 2a / 2b: 认领触点覆盖 ops leaf 任务 (阶段 3 确认任一执行项), 或给出手动认领指引 —— 均未做; A.1 触点因 Level 1 skip 不覆盖, 无 Spec 的 leaf 任务本就不经 A.1。
4. 缺口 3 残余: 身份取值收敛到 uuid、`derive_container_id`、主机名不进键 —— 未做; 其中收敛到 uuid 取决于 S2 (`10CG/Aria#198`), `derive_container_id` helper 不在 `10CG/Aria#198` 的任务清单内, 尚无承接; 规范侧口径见 `10CG/aria-standards#19`; 另外同 owner 同主机名 / 同 label 的两机仍合成一个 `identity_key` (见 case-4 补充)。
5. 评论 18823 的三条建议: 建议 1 (`get_container_id()` 恒返回 uuid) 与建议 2 (release / heartbeat 双键匹配) 未做; 建议 3 各只做了一半 —— 3a (文件头警告): 新生成的 `container-id` 文件头已有警告注释, 但 `_write_container_file` 只在文件缺失或损坏时调用, 存量文件头不会被迁移 (实验: 旧头文件调 `get_container_id()` 后内容不变); 3b (label 生效时提示): `get_container_id()` 本身无任何提示, 只在 gate 层 (`phase1_gate.py` / `release_gate.py`) 有 `label_migration` 与 stderr 告警, 且该告警只数 `claims/<label>/` 下的 active, 事后加 label 时恒为 0, `--heartbeat-only` 路径没有该键。孤儿 claim 的恢复: `release_gate.py` 没有指定 container 的参数, 评论 18823 当时只能绕开 CLI; 现在清空 label 后重跑 release 即可恢复 (实验对照), 若要不清空 label 就释放, 需要跨身份定向 release, 与 `10CG/aria-plugin#166` 相关。

已核实为真的已落地项 (与评论 21988 对照): 缺口 3 读取侧、`identity_key`、`identity_advisories[]`、`get_container_label()`、`label_migration`, 以及 10CG/aria-standards 仓 `conventions/session-handoff.md` 的 §2.3.1 / §2.3.5 / §2.3.9 (aria-plugin `5fbb974` + `0545f86`, aria-standards `d217ed0`, `10CG/Aria#197` 合并 `990318e`; 均已在 origin 与 github 两端 master)。但有一处规范与实现相反: §2.3.1 (10CG/aria-standards 仓 `conventions/session-handoff.md:116`) 已写「label 不参与身份」, 而 v1.74.1 的 `get_container_id()` 仍 label 优先 (`skills/state-scanner/lib/identity.py:223`), `handoff_autofill` 据此写 owner-container, 模板 `templates/session-handoff.md:43` 也写「label 当前仍参与协调身份」—— S2 flip 前规范与实现不一致, 属缺口 3 残余。

关于 S2 的补充 (推断, 供排期参考): `10CG/Aria#198` 的激活条件之一是原 Spec 的 merge 任务 (TASK-034) 尚未执行, 该 Spec 已于 2026-09-06 merge 并归档, 所以 S2 只能作为后续独立 change 推进; 「a1-entry 进 master」这一前提已满足 (v1.71.0), 剩余是 `10CG/Aria#174` 上 SC-3 改写的 ack (征求留言 issuecomment-21906, 此后无回复), 以及两处需同步翻转的测试 (`skills/state-scanner/tests/test_identity_label.py` 的 S1 lock-in、`skills/state-scanner/tests/test_identity_container_uuid.py` 里断言 `get_container_id()` 返回 label 的夹具区分力用例)。

建议: 保持 open。缺口 1 与缺口 2 目前没有其他 issue 承接; 如 owner 希望收敛看板, 可把二者拆成独立 issue 后再关闭本单, 开新 issue 一事已提请 owner 决定, 本评论不代为操作; 在此之前不宜关闭。本次核验未对真仓做任何写操作 (复现在 /tmp 实验副本, 读代码与跑测试均为只读), 也未关闭或修改本单。
