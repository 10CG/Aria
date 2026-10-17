本条是按 owner 2026-09-30 决策单第 6 项做的 issue 卫生清扫核验 (疑似已修未关的 issue 先 triage 核验, 再评论 / 关闭); 结论基于 aria-plugin v1.74.1 (aria-plugin 仓 master `268da8f`, 10CG/Aria 主仓 master `0748dbc`, origin / github 两端一致) 在隔离副本里的实测, 不是对 issue 历史文字的转述。

## Triage Report

**Verdict**: `partial-repro` | **Severity**: `minor` | **Recommended Action**: `backlog`

> 一句话结论: 建议保持 open。本 issue 的一个子集 (同一 issue、不同 track-id) 已由 v1.67.0 到 v1.71.0 修复; 但 issue 自己举的原场景 (无共享 issue token、只共享一份 deferral 档) 在 v1.74.1 的闸门输出上仍原样复现 (`passed` / `surface=null` / 无 `linked_issue_overlap` 键)。编排层现会明示「本轮未检测」(A.1) 或「未能核实 (原因: own_token_absent)」(审计轮), 但撞车本身仍不可见。10 项具体诉求里 1 项已修 (第 9 项)、2 项部分满足 (第 1、7 项)、7 项未实现或未答复。

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.63.0` |
| Current | `1.74.1` |
| Gap | behind |

报告方当时安装的是 v1.63.0 (issue 创建日 2026-08-05 上游已是 v1.65.5); 此后 minor 号从 1.63 前进到 1.74 (没有 1.72 这一版), 其中 v1.67.0 到 v1.71.0 五个版本与本 issue 直接相关。所以这是一份部分过期的报告, 不能把正文当作现状。

### Code Path

- 路径约定: 下文 `aria/...` 开头的路径是 10CG/Aria 主仓里 aria-plugin 子模块的路径 (在 10CG/aria-plugin 仓内去掉 `aria/` 前缀即是仓内相对路径); `openspec/`、`docs/`、`.aria/` 开头的是 10CG/Aria 主仓路径。
- issue 引用的 10CG/ShenQuant 仓文件不在本仓, 经 forge 读取: `openspec/changes/archive/2026-08-04-add-replay-derived-ladder/tasks.md` 在该仓 main 分支存在, 其 TASK-006 下 2026-08-02 的 deferral 段明写三项「绑定 synth 真接线的那个 change」同 PR 闭环, 并要求接线 change 的 proposal 引用该档, 与 issue 转述一致; `docs/handoff/2026-08-05-CROSS-CONTAINER-synth-collision-alignment.md` 在该仓现有的 4 个远端分支上都读不到, 无法核对。复现改用等价夹具, 不影响结论。
- 评论 21906 / 21989 里的 `lib/identity.py` 是 `aria/skills/state-scanner/lib/identity.py` (triage collector 按主仓根目录解析, 报 file not found 是路径解析假象)。现状: `get_container_uuid()` 在 :248, `get_container_id()` 仍是 `return label if label else uuid` (:223)。评论引用的 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` 在 10CG/Aria 主仓存在。
- 评论 21906 里的 a1-entry 分支 `ab3dbd0` 已是过去式: 它是 aria-plugin 仓 master 的祖先, a1-entry 已作为 v1.71.0 合入。

### Git History

collector 因 cited path 没解析到, `likely_fix_candidates` 为空。人工核对出的相关提交, 均已确认是对应仓 origin/master 与 github/master 的祖先 (两端 master 头已用 `git ls-remote` 逐个核对: aria-plugin 仓 `268da8f`, 10CG/Aria 主仓 `0748dbc`):

| 仓 / 提交 | 版本 | 内容 |
|-----------|------|------|
| aria-plugin `ca52d1c` | v1.67.0 | `linked_issue` 跨格式归一比较 |
| aria-plugin `fe32441` | v1.68.0 | proposal 「Linked Issue」字段可得性 (E0-E6 抽取 + 探针 + spec-drafter 字段义务) |
| aria-plugin `2eca24b` | v1.69.0 | audit-engine 每轮入口的竞品 spec 探针 |
| aria-plugin `0545f86` | v1.70.0 | owner-container 两段式 + `identity_key` 判定 + 族键 + 同机多身份 advisory (10CG/Aria#193) |
| aria-plugin `985e629` | v1.71.0 | A.1 入口重复劳动闸门 (本 issue 是其立项 issue, 见 aria-plugin 仓 `CHANGELOG.md` 的 v1.71.0 条) |
| 10CG/Aria 主仓 `3dd7f1d` | - | a1-entry-claim-duplicate-work-guard 归档 (40/40) |
| 10CG/Aria 主仓 `909d771` | - | subprocess-decode-hardening 归档为 design-only (SUPERSEDED-BY-SHIP) |

补记: a1-entry 是以本 issue 立项的, 但本 issue 下此前没有 ship 通告, 这条评论一并补上。

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (10CG/Aria 与 10CG/aria-plugin 两仓 open PR 均为 0) |
| Local branches | `remotes/origin/feature/owner-container-identity-key-and-collision-parser` (已并入 master 的旧特性分支, 非在途) |
| Worktrees | 仅主 worktree |

两个仓的远端分支里没有专门承接下面「未修」项的分支; 已扫描两仓全部 open issue, 也没有其他 issue 承载这些残余诉求。与本 issue 有关的两条 open tracker: 10CG/Aria#198 是 owner-container-identity-key 的 S2 后续项承载体 (0 评论), 与评论 21906 的 SC-3 改写 ack 有关, 见逐项核对第 10 项; 10CG/Aria#201 是 a1-entry 的归档残留待办 tracker, 内容是该 Spec 自身未验证的验收项, 不含本 issue 的残余诉求。

### Reproduction

**Mode**: `auto` | **Hit rate**: `5/10` (命中 = issue 所述症状在 v1.74.1 上复现)

复现在隔离副本里做, 夹具不连任何生产远端 (phase1_gate 夹具无 remote 且一律 `--no-push`, 探针夹具只连本地 bare 仓), 没有碰任何生产 coordination ref。

| Case | 输入 | 观察 | 症状复现 |
|------|------|------|----------|
| case-1 | 两 track 名不同 (`add-synth-today-bar-wiring` 与 `wire-synth-quote-bars`), 无共享 issue token, 按 A.1 模板省略 `--linked-issue`, 跑 `phase1_gate.py --phase A.1 --mode advisory --include-terminal --no-push` | `outcome=passed`, `surface=null`, 输出里没有 `linked_issue_overlap` 键 | 是 |
| case-2 | 同上, 但双方登记同一个合成 token `10CG/Example#7` (夹具专用, 与任何真实 issue 无关; 结果与 token 取值无关) 并传 `--linked-issue` | `linked_issue_overlap` 命中对方 claim | 否 |
| case-3 | 直接把 deferral 档路径当 `--linked-issue` 键传给闸门 (对方 claim 与本方实参都用同一路径) | 命中对方 claim (不可解析值回落原串精确比较) | 否 |
| case-4 | proposal 的 Linked Issue 写 deferral 档路径, 跑 `linked_issue_field_probe.py --emit-arg` | 输出为空 (判 `BAD_TOKEN`), A.1 模板随之省略整个 `--linked-issue`, 落回 case-1 | 是 |
| case-5 | 两份 proposal 的 Linked Issue 都是哨兵 `none`, 正文引用同一份 deferral 档, 跑 `sibling_spec_probe.py` | `verdict=not_established`, `reason=own_token_absent`, `hits=[]` | 是 |
| case-6 | 同 case-5 夹具, 两边改成同一 canonical token | `verdict=sibling_found`, 命中远端分支上的竞品 (夹具有效, case-5 的空结果不是假象) | 否 |
| case-7 | 批次型 track (复刻评论 19366 方向 B 的形态, token 取自该评论的真实场景): A 的 proposal 字段写 `10CG/Aria#181, 10CG/aria-plugin#147`, B 只写 `10CG/aria-plugin#147` | A 的 `--emit-arg` 只输出首个元素 `10CG/Aria#181`, B 的 `linked_issue_overlap` 为 `[]`, 漏检 | 是 |
| case-8 | Layer H: 同 owner、两个 uuid 容器、不同 track 名 | `classify` 给 `kind=none` | 是 |
| case-9 | Layer H: a1-entry 风格 `<slug>-<uuid8>` track-id、同 slug 双容器 | `kind=self_multi_container` (v1.70.0 族键) | 否 |
| case-10 | handoff 里同一 uuid 出现 `aria-runner-bot/023236f2` 与 `simonfish/023236f2` | `kind=none` + 1 条同机多身份 advisory | 否 |

case-1 与 case-2 在定稿前又用合成 token 重跑了一遍, 结果不变。另在隔离副本里跑了相关现成测试, 全部通过: `test_a1_entry_gate_cli` 20, `test_coordination_default_lockin` 26, `test_heartbeat_by_track` 12, `test_linked_issue_field` 59 (2 skipped), `test_collision` 28, `test_collision_frozen_corpus` 7, `test_track_board_advisories` 5, `test_identity_label` 6, `test_identity_container_uuid` 5, audit-engine 的 `test_sibling_spec_probe` 100 (1 skipped)。

**Deviation note**: 报告方当时安装的是 v1.63.0, 正文称当前没有任何编排层传 `--linked-issue`。此后 v1.67.0 到 v1.71.0 已经 ship 了归一、字段可得性、竞品 spec 探针和 A.1 入口认领, 同一 issue 不同 track-id 的形态已可检出 (case-2)。但 issue 的原场景在 v1.74.1 的闸门输出上仍原样复现 (case-1 / case-5: `passed` / `surface=null` / 无 overlap 键, 探针 `not_established`); 编排层现会明示「本轮未检测」(A.1) 或「未能核实 (原因: own_token_absent)」(审计轮), 但撞车本身仍不可见。评论提出的若干诉求也没有实现。因此既不是「已修」, 也不是「原样复现」。

### 逐项核对 (正文 4 项建议 + 3 条评论的诉求, 共 10 项)

| 序号 | 诉求 | 来源 | 状态 | 依据 |
|------|------|------|------|------|
| 1 | Phase A 入口由编排层传 `--linked-issue` | 正文建议 1 | 部分满足 (仅 A.1 入口, Level 2/3 Spec) | v1.71.0 `985e629`; `aria/skills/phase-a-planner/SKILL.md:60-88`、`aria/skills/spec-drafter/SKILL.md:73-105` 的「前置: REQUIRE claim (A.1, MUST)」块; case-2。限定: 仅当 proposal 的 Linked Issue 是合法 `<org>/<repo>#<n>` token 时才传; Phase B 入口 (`aria/skills/phase-b-developer/SKILL.md:93` 的 B.0、`aria/skills/state-scanner/SKILL.md:178`) 的 `--linked-issue` 仍为可选且无取参规则; A.1 对 Level 1 零调用 (phase-a-planner 的 skip 三条之第 2 条) |
| 2 | proposal 声明「强制输入档路径」时, 把路径作为 `--linked-issue` 传入 | 正文建议 1 (字面) | 未修 | case-4: 路径判 `BAD_TOKEN`, 参数被省略; 闸门原语本身能承载路径键 (case-3), 缺的是撰写 + 编排侧。另 (核验补充实跑, 不计入上面 10 个 case): audit-engine 竞品探针对不可解析值回落原串比较 (`aria/skills/audit-engine/scripts/sibling_spec_probe.py` 的 `classify_proposal`), 两份 proposal 若在 Linked Issue 字段写同一路径, 会在审计轮入口得到 `sibling_found`; 但该写法按字段规则判 `BAD_TOKEN` (不合规), 且只在审计轮生效、不在 A.1 生效, 不算已实现 |
| 3 | deferral 档稳定机读 id, 后继 change 在 frontmatter 引用作 overlap 键 | 正文建议 2 | 未修 | `deferral-id` / `ARDL-` 在 aria、standards 子模块、10CG/Aria 主仓的 `openspec/`、`docs/`、`.aria/` 全部 0 命中; 未见任何 Spec 或决策单评估过这一项 |
| 4 | 分支名 token 级相似度 advisory 兜底 | 正文建议 3 | 未修 | aria 非测试 `.py` 中没有任何相似度实现 (jaccard / levenshtein / difflib 等 0 命中); `sibling_spec_probe.py` 枚举远端分支只为读 proposal、按 issue token 求交, 不看分支名。sibling-spec-probe 的 Spec 已把「标题 / slug / 语义相似度的模糊匹配」列为非目标 (`openspec/archive/2026-09-04-sibling-spec-probe/proposal.md:531`, 同文件 :203 写明「不猜标题、不猜 slug、不做模糊匹配」), 审计轮探针因此不做这一层; 更早的 2026-07-11 coordination-claim-lifecycle-and-overlap Spec 也把模糊匹配与 `file_globs` 文件重叠列为选项 (`openspec/archive/2026-07-11-coordination-claim-lifecycle-and-overlap/proposal.md:16`、:43), 部件 B 最终只做了 B1 (`linked_issue`), aria 里没有 `file_globs` 实现。若要在 phase1_gate 侧做分支名相似度, 属另一条机制, 需要新 Spec |
| 5 | 文档: 把「同源不同名」列为已知盲区, 提示 Phase B 入口额外 fetch + 扫视活跃分支 | 正文建议 4 | 未修 | `aria/skills/state-scanner/SKILL.md:143-178` 与 `aria/skills/state-scanner/references/layer-l-integration.md` 没有该成文 (盲区 / 同源 / 不同名 均 0 命中); phase-b-developer 的 B.0 与 branch-manager 也没有「Phase B 入口 fetch 后扫视远端活跃分支」的步骤 (branch-manager 里的 `git fetch` 只出现在 C.2 同步与回滚段)。缺口只成文在归档 Spec 里 (`openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:509`, §6 首行), 采用方读不到。近似机制: 审计轮入口的竞品探针 (v1.69.0) 会拉取并扫描远端全部分支, 但触发点是审计轮而非 Phase B 入口, 且按 issue token 求交 |
| 6 | `self_multi_container` 不应等同良性, 该分类下仍做内容重叠检查 | 评论 18965 第 4 点 | 未修 | `aria/skills/state-scanner/references/layer-l-integration.md:27` 仍写「soft hint (不阻塞)」; `aria/skills/state-scanner/lib/collision.py:186-217` 的 `classify_claims` 只按 (identity_key, 可归属 owner 数) 分类, 没有内容 / 文件集重叠维度; case-8。部分改善: v1.70.0 族键让同 slug 的 `<slug>-<uuid8>` 双容器能被 Layer H 分组 (case-9), 仅限同 slug |
| 7 | 手写 owner-container 与派生值不一致时 fail-loud 或至少 warn | 评论 18965 第 5 点 | 部分满足 (信息级) | v1.70.0 `0545f86` (10CG/Aria#193 已关): `identity_key` 对 uuid 容器只认 uuid, 判定不再依赖手写 owner 段 (`aria/skills/state-scanner/lib/collision.py:96-113`); 同机多身份信息级 advisory (`collision.py:263-303`、`aria/skills/state-scanner/scripts/renderers/track_board.py:826`; case-10)。限定: advisory 只在同一 uuid 的两种 owner 串同时出现在 handoff 语料里时触发, 写 handoff 时不与 `handoff_autofill` 的派生值比对 (`aria/skills/session-closer/scripts/handoff_autofill.py:391-410` 的 `owner_container()` 是 best-effort, 失败返回 None 后仍保留手填); 语料里只有手填值一行时不告警 |
| 8 | 批次型 track 一个 claim 挂多个 issue | 评论 19366 | 未修 | `aria/skills/state-scanner/lib/linked_issue_field.py:94-105` 的 `emit_arg` 只取首个 token 元素; claim 的 `linked_issue` 与 `linked_issue_overlaps` (`aria/skills/state-scanner/lib/collision.py:365` 起) 的入参都是单个字符串; a1-entry proposal 非目标明写不新增任何 claim 字段 (10CG/Aria 主仓 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:683`); case-7。另 (核验补充实跑): audit-engine 竞品探针按字段全部 token 求交, 两份 proposal 都写多 token 时能检出 (正反两个方向均得 `sibling_found`); 缺口在于 claim 侧只登记首个元素, 且评论 19366 方向 B 的原形态 (一侧是 Level 1 直修, 没有 proposal、不经 A.1; Phase B 入口的 `--linked-issue` 仅可选) 在 v1.74.1 下, claim 层与审计探针层都没有可比的输入 |
| 9 | `subprocess-decode-hardening` 残留处置 | 评论 19366 | 已修 | 10CG/Aria 主仓 `909d771` (2026-08-21) 归档为 design-only (`archive_type: implementation-deferred`, `archived_reason: SUPERSEDED-BY-SHIP`); 目录已在 `openspec/archive/2026-08-21-subprocess-decode-hardening/`, `openspec/changes/` 下已无该目录 |
| 10 | 征求 a1-entry 对 SC-3 改写 (S2 条件) 的 ack | 评论 21906 | 未答复 | live GET (2026-09-30): 本 issue 仍 open, 共 4 条评论, 最后一条 21989 (2026-09-06) 之后无回复。S2 从未激活: v1.70.0 (`0545f86`, 2026-09-06T08:27:19Z) 先于 v1.71.0 (`985e629`, 2026-09-06T09:36:58Z) 进 master。S2 后续项 (含 SC-3 改写) 由 10CG/Aria#198 承载 (open, 0 评论), 其正文仍写本 issue 的 ack 征求中。a1-entry 已归档, SC-3 原文冻结在 `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:617` |

另有两条纯信息项无需处理: 评论 19366 的成本不对称说明 (a1-entry 以「认领必须早于投入」作为立项依据), 评论 21906 / 21989 的 D-0(a) 通告与 S1 ship 结果 (已核实 a1-entry 侧零契约改动: `get_container_id()` 仍 label 优先)。

### 建议

1. 保持 open。未修的是第 2、3、4、5、6、8、10 项。其中 2 和 3 (共享输入档键 + 稳定 id) 是覆盖原场景的直接路径, 4 (分支名相似度) 与 6 (内容 / 文件集重叠) 是不依赖撰写纪律的兜底路径, 5 是文档, 8 是判据增强 (多 issue claim)。
2. 流程性缓解 (单方无法自救): 写 deferral 时就为它开 issue 并在 deferral 段写明, 后继 change 的 Linked Issue 都引用该 issue, 才能落进已 ship 的 A.1 检测。
3. 第 10 项: 如果将来关闭本 issue, 需要先把 ack 请求迁到 10CG/Aria#198, 否则它的前置引用会指向已关闭的讨论串。
4. 如 owner 倾向关闭本 issue, 建议先把未修项拆成窄 scope 的新 issue 再关, 避免诉求随关闭丢失。是否拆分、是否关闭, 已提请 owner 决定。

### Verdict Rationale

a1-entry 系列 (v1.67.0 到 v1.71.0, 本 issue 是其立项 issue) 解决了「同一 issue、不同 track-id」这个子集, 所以标题所述症状不再原样成立; 但 issue 自己举的原场景 (无共享 issue token、只共享 deferral 档) 在 v1.74.1 的闸门输出上仍是 `passed` / `surface=null`, 且逐项核对表第 2、3、4、5 项 (正文建议 1 的字面做法与建议 2、3、4) 及第 6、8 项均未实现或未成文, 其中第 2、8 项只在审计轮探针层有部分缓解, claim / A.1 层没有。原场景的缺口只成文于归档 Spec (a1-entry proposal 的 §6 首行、sibling-spec-probe proposal 的 §10 B3 / B4), sibling-spec-probe 还在非目标里明确排除了「标题 / slug / 语义相似度的模糊匹配」。

严重度取 `minor`、处置取 `backlog` 是 triage 的技术判断, 可商榷, 已提请 owner 复议; 两边证据如下。取低的依据: 缺口已成文为已知缺口, 不造成数据损坏、不阻断主流程; 10CG/Aria 仓 2026-09-02 起归档的 7 份 proposal 里 5 份带合法 canonical token (另 2 份是拆分出的子 Spec, 无独立 issue 号), 该形态在本仓的出现频率已经下降 (样本小, 仅本仓); 另有上面的流程性缓解。取高的依据: a1-entry proposal 自称这是「最大的单项缺口」(窗口无界, 覆盖机制为「无」), sibling-spec-probe proposal 称其为「量级最大的一类」; issue-triage 的 severity 量表把「功能错误」归 major; 撞掉的是一整条 L2 spec 加收敛审计 (评论 19366 的成本不对称)。若 owner 认为原场景必须覆盖, 可在第 2 + 3 项 (直接路径)、第 4 或第 6 项 (兜底路径) 中选一条升为 next-cycle; 第 5 项 (文档) 与第 8 项 (多 issue claim) 不依赖这一选择, 可另行排期。

---

*Generated by `/issue-triage` v1.74.1 — Ref: 10CG/Aria#174*
