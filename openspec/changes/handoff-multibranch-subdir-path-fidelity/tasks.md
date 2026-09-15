# Tasks — `handoff-multibranch-subdir-path-fidelity`

> **Spec**: [proposal.md](./proposal.md) (v7, Approved 2026-09-12) | **决策单**: [`2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`](../../../.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md) (§2 的 10CG/Aria#195 表 8 行 + §5 复核, 21 条即最终口径) · [`2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`](../../../.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md) (A′ + 写侧守卫, 09-12 追认; 其「落地约束」第 1 / 2 / 4 条已作废, 见「读前必看」第 12 条) | **审计**: post_spec R1–R5 (R5 `overridden_by_user: true`) → post_planning R1 (`.aria/audit-reports/post_planning-R1-2026-09-15T151749-638Z-handoff-multibranch-subdir-path-fidelity-aggregated.md`) → post_planning R2 (`.aria/audit-reports/post_planning-R2-2026-09-15T180659-081Z-handoff-multibranch-subdir-path-fidelity-aggregated.md`)
> **Level**: 3 (决策单 §2 第 7 行, 不拆) — 本文件 (A.2) + `detailed-tasks.yaml` (A.3, 单一 SOT: verification / 依赖 / 工时 / rule6_note / A.2 基线复核记录 / SC-11 谓词与多状态验证 / 外向动作与 owner 等待点)
> **Status**: A.2/A.3 v3.1 (2026-09-15, simonfish/023236f2) — post_planning R2 rework (聚合 0C / 9M), 待 R3。v3 由换任的执笔人落笔 (R2 聚合报告称本次返工为「R3 rework」), v3.1 为主控核验后的返修 (2 必改 + 2 建议改); v2 = post_planning R1 rework (聚合 0C / 13M)
> **Scope**: 三个仓 — aria 子模块 (A.2 实测 `1cb3872` = v1.73.3; proposal 行号冻结于 `f314785`) · standards 子模块 (`8b49562`) · 主仓 (A.2 时 origin 与 github 的 master = `36ea288`, 本地 master 另领先规划提交; 分支起点见「读前必看」第 13 条)
> **ship target**: aria-plugin `<vNEXT>`, 档位 **MINOR** (决策单 §2 第 6 行)。本文件不写字面版本号, 号在 5.1 执行时按 `plugin.json` + 远端 tag + 并发轨取号计
> **执行记录**: B 期由 1.3 新建 [`verification-ledger.md`](./verification-ledger.md), 二级标题照 `detailed-tasks.yaml` `metadata.verification_ledger.skeleton` (本文件不另列); **主控唯一执笔**, subagent 只交回证据; 归档后的写入路径见同处 `path_after_archive`; 下文「记入台账」均指该文件

---

## 读前必看 — proposal 正文与执行口径的差异 (proposal 不改, 以本节为准)

proposal 是 09-10 冻结、09-12 裁定前写成的; 下列各项在正文里写的是另一支或已过期的事实。实施者照正文字面执行会做错, 故逐条列出。「proposal 正文」列标 `:行号` 的是原文位置, 标「推论」的是 v1 的转述。

| 编号 | 事项 | proposal 正文 | 执行口径 | 依据 |
|---|---|---|---|---|
| 1 | dedupe 排序键 | 推荐默认「不改排序键」(Task 2.0 `:370` 称待复议 1/3/4/5 取推荐默认); §6 `:308` / `:320` 与 Task 4.1 / 4.2 / SC-11(j) 写「仅默认支下」把 build-order 不变量条件化为「同 `rel_path` 前提下」; Risk 表 `:353` 与 SC-7 `:421` 称本 spec 不为该 tie 加断言 | **改键支**: 新增 2.6 加第 5 级键; **全部键层级描述整类改写** —— collector `:58-61` / `:93-96` / `:355` / `:368-399` / `_dedupe_sort_key` docstring / `:490-492` / `:716-717`, schema `:1124` / `:1128` / `:1134`, dedupe 测试文件 `:885` / `:1162` 两处 docstring (断言不动); 不变量句保持无条件; SC-11 取 (j1)–(j5) | 决策单 §2 第 4 行附问 + §5 终裁 |
| 2 | CHANGELOG 已知边界 | §6.5 与 SC-11(e) 写「四条」 | **五条**: 追加「mv 过的无 frontmatter 件, `updated_at` 仍取 mv 提交日; 不加 `--follow`」; mv 日语义**只由 CHANGELOG 承载, 不进遗留 issue**; `### Changed` 另追加 dedupe 第 5 级键一条 ⇒ 至少六条 | 决策单 §2 第 5 行、第 4 行 |
| 3 | standards 第三态措辞 | §6 `:330`「AI 手改路径 (`handoff-mechanics.md`) 是否同步该态待 owner 裁」; Task 4.4 `:384`「注明处方路径待裁」 | 写成「经 AI 手改路径 (`handoff-mechanics.md`) 写入时尚未同步该态, 跟踪见 10CG/aria-plugin#<5.3 开出的号>」, 并按该文件 `:180` 先例加 `> **Amended**` 标注 | 决策单 §2 第 2 行第 (4) 问 |
| 4 | 遗留缺口 issue 所在仓 | Task 5.3 未定 | `10CG/aria-plugin` | 决策单 §2 第 2 行第 (2) 问 |
| 5 | 前置门 Task 2.0a / 2.0b | 未解除, 阻断 B.1 | 已随 09-12 裁定解除 (Level 3 / MINOR), 并入 2.0 | 决策单 §2 第 6、7 行 |
| 6 | SC-10 可执行命令 | 9 模块一条 `python3 -m unittest …`, 「Ran 169」 | A.2 实跑: 该命令对 `test_collision` **收集 0 条** (28 个 pytest 风格裸函数), 169 = 其余 8 模块之和 ⇒ **追加 pytest 腿** (只增不改); 同型的 phase-d-closer `test_fetch_gate.py` (11 条, 消费 `collision.kind`) 一并进 4.3 回归 | yaml `metadata.test_runner` |
| 7 | SC-12a 改前 / 改后快照 | `:426`「在本仓同一工作区先跑改前 scan.py …, 再跑改后」, 两次扫描间比对分支集 (「改前须在 B.1 时跑」是 v1 推论, 非原文) | **追加** ref→SHA 映射比对 (同分支上的新提交同样改变 collector 输入, 只比分支名会误判); 改前扫描用 B.1 基线 SHA 的一次性 worktree 旧代码, 与改后**背靠背**跑 (只增不改) | memory `partial-freeze` 同型 |
| 8 | 基线行号 | 冻结 `f314785` | A.2 复核 `f314785..1cb3872` (41 触点): **代码落点零 diff, 行号全部有效**; `state-snapshot-schema.md` 的 `:1062` 为原位改写、旧 `:1064` 之后插入 2 行 ⇒ 旧 `:1065` 起全部 +2 (例 `:1104`→`:1106` / `:1114`→`:1116` / `:1126`→`:1128` / `:1136`→`:1138`); `layer-l-integration.md` `:84` 后插 2 行 (`:103`→`:105`); `phase-1-collectors.md` 原位改 1 行, 不移位; schema `## Change history` 表末已有 2026-09-13 新行 (正文「表末行仍是 2026-07-19」过期); `aria/CHANGELOG.md` 的 v1.70.0 先例现位于标题 `:200` / Fixed `:202` / Added `:209` / Changed `:215` (正文 `:109` / `:118-122` / `:124-125` 已二次过期)。1.3 在 B.1 时对当时 HEAD 重跑 | yaml `metadata.baseline_rebase` |
| 9 | 主仓 16 个版本点 | 写作时取值 v1.73.0 | A.2 实测: 15 点 = 1.73.3, **`VERSION:24` 仍为 v1.73.0** (v1.73.1 / v1.73.2 / v1.73.3 三次发版漏改; 该点无机械兜底) ⇒ 5.1 直接写新号, 不按「上一版 +1」核对 | 同上 |
| 10 | 编号 | 含 2.0a / 2.0b / 5.4a | 2.0a / 2.0b 并入 2.0; 5.4a → **5.6** (内容按 standards `content-integrity.md` §4.4 / §4.5 更新); 新增 **1.3 / 2.6 / 2.7 / 3.4 / 3.5** (3.5 为 v3 新增)。字母后缀不被归档门的 checkbox 正则识别为 parent, 故不沿用 | 归档门 `spec_complete.py` `_CHECKBOX_ANY_RE` |
| 11 | 测试编写时点 | 3.1–3.3 列在实现之后 | 用例本体全部在组 1 写好并取 RED (Task 1.2 的例外清单已把 SC-6(c) / SC-7 列为同文件用例, 第二条记录含 SC-6(a)(b)); 3.1–3.3 承接实现后的 GREEN 与反事实。2.5 依赖 2.1 / 2.2 产出 `rel_path` 的数据序不变 | proposal Task 1.2 |
| 12 | 09-07 决策单「落地约束」 | 头部 `:21` 已声明其第 2 / 4 条作废, 决策单本体未改 | 该节第 1 条字段名 `relpath`、第 2 条判据 `relpath != filename`、第 4 条归档-only 夹具**全部不得照做**; 以 proposal §2.5 (`rel = track.get("rel_path") or track.get("filename")`) 与 SC-15 布局 2 为准 | 决策单 2026-09-12 §2 第 2 行第 (5) 问 |
| 13 | 分支起点 | 头部 `:9`「Phase B 在 `f314785` 起分支」 | aria / standards 的 feature 分支从 **B.1 实测的 `origin/master`** 起 (先 fetch 或直接 `ls-remote`, 不读陈旧的远端跟踪 ref); 主仓同样从该实测值起, **前置**: 规划提交 (A.2/A.3 各版与 post_planning 各轮报告) 已经 owner 授权推到 origin 与 github 并逐 remote `ls-remote` 核验; B.1 时仍未推送 ⇒ 主仓 feature 分支改从包含规划提交的本地 master 起, 起点 SHA 与未推送事实记台账, 推送随 5.2 的主仓 PR 发生 (AI 流程判断清单第 13 条); 1.3 记录实测值 | 与第 8 条同源; A.2 实测 origin 与 github 的 master 均为 `36ea288`, 其上本 change 目录只有 `proposal.md` |
| 14 | SC-11 验收判据 | `:425` SC-11 (a)–(l) 的整文件 grep 与计数 | **以 yaml `metadata.sc11_baseline_predicates` 的 19 条定位谓词为准**, 与原文逐项差异: (a) 整文件计数 ≥ 2 → (a1) 字段块内 `unreadable_count` 行 + (a2) `**Fail-soft**: branch-list` 行反引号内的形状 dict 含 `"unreadable_count": 0` (同行散文不算); (b) → TrackEntry 块内 `rel_path` 行; (c) 前两条同原文 (c1)(c2), 模块 docstring 两块各归其位不入谓词, 由 4.2 核验; (f) 整文件 grep → (f1)(f2) 限非表格行; (g) → 限 `## Change history` 之后的表格行; (i) 两文件否定式 → (i1) collector 否定式 + (i2) TrackEntry 的 `track_id` 行含新公式 (schema 的 Change history 行写旧公式属正常); (j) 默认支的条件化 → 改键支 (j1)–(j5), 见第 1 条; (k) 两条删旧句否定式 + 「等义措辞」→ 两处 docstring 逐字含 `target_in_subdir`, 不再要求删旧句, 意译不算; (l) writer 三处合计 ≥ 3 + 两个 references → (l1) 模块 docstring 与 `write_latest_md` 的 Returns 段各含 `degraded_reason`, 且 `Scenarios:` 之后含 `degraded_reason` 或 `target_in_subdir`, (l2) 限 `Return dict` 行, (l3) 限 `单 track` 行含 `子目录` 或 `subdir`; (d)(e)(h) 不入谓词, 分由 5.3 与 5.4 / 5.1 / 4.4 承载 | post_planning R1 PP1-M2; R2 PP2-M8 / m11 / m14 / m15; 多状态验证见 yaml `metadata.sc11_predicate_validation` |

---

## AI 流程判断清单 (请 owner 复议 — Rule #10 §5)

下列判断在 A.2 / A.3、post_planning R1 rework (v2) 与 post_planning R2 rework (v3) 中由 AI 自行作出, 不来自 owner 裁定; 第 1–17 条由主控作出 (v3 由换任执笔人照 R2 聚合报告的处置落笔), 第 12 条中标「执笔人」的部分与第 18 条由 v3 执笔人作出。均已公开列出并经 post_planning 审阅, 但按 `standards/conventions/configured-gate-authority.md` §5 仍须写进 handoff 请复议; 5.4 的周期 handoff 照录本清单并追加 Phase B / C / D 新增项。

1. **不按 phase-a-planner 前置条款重新认领**: A.1 已 Approved 故跳过; 本容器对同一 track 的 claim 仍为 active (09-15 已刷新心跳); CLI 每次调用都新生成 session id, 重认领只会造出重复 claim (原串) 或第三个名字 (`<slug>-<uuid>` 形)。
2. **SC-10 追加 pytest 腿**: 实跑发现 unittest 对 `test_collision` 收集 0 条。
3. **SC-12a 执行方法**: 改前扫描改用基线 worktree 旧代码、与改后背靠背跑, 并追加 ref→SHA 映射比对。
4. **编号**: 2.0a / 2.0b 并入 2.0, 5.4a 改为 5.6, 新增 1.3 / 2.6 / 2.7 / 3.4, v3 另增 3.5。
5. **测试编写时点**: 用例本体提前到组 1, 3.1–3.3 改为实现后的 GREEN 与反事实。
6. **第 5 级排序键方向**: 子目录行之间按 `rel_path` 字典序**取大** (决策单只写「其余字典序」; 取大与前四级方向一致)。
7. **B.0 的 occupied**: 若对象是本容器自己, 定性为已知缺口而非竞争者。
8. **反事实证据来源** (v3 改写): proposal SC 表所列反事实全部在组 3 按三步法实跑 —— SC-1 / 3 / 4 后半 / 5 / 8 后半 / 14 / 17 归 3.5, 其余归 3.1–3.4; 基线 RED 记录只作 RED 证据, 不再充当反事实, SC-14 也不再用 2.3 完成、2.4 未做的中间态。理由: 基线是全部组件同时回退, unittest 停在首个失败断言, 记下哪一条取决于书写顺序, 证明不了反事实所指断言的鉴别力 (post_planning R2 code-reviewer 席在 1cb3872 上跑 SC-5 基线探针, 同时有三个失败源); 工作树中间态不可复现, 已提交 SHA 是唯一可复现的检出源。v2 的做法 (基线 RED 即反事实 + SC-14 中间态) 撤销。
9. **mv 日语义的承载**: 只进 CHANGELOG 已知边界, 不进遗留 issue。
10. **执行台账**: 放在 change 目录 (`verification-ledger.md`), 主控唯一执笔。
11. **归档门假阳性** (v3 改写): 归档门预演实为三条 unverified_claims、三类检查器假阳性 —— 2.2 行 `HEALTHY_TRACKS` unclassified reference form (测试专用常量) / 4.4 行 no extractable symbol (文件名子串) / 4.3 行 dogfood 声称无可链接产物路径; 以执行时的预演结果为准。三类都不改写措辞规避; 归档前预演, 由 owner 决定 Step 7 是否建单, 假阳性经授权另报。
12. **SC-11 验收判据的形态**: proposal 的整文件 grep 改为定位谓词 (19 条), 与原文的逐项差异见「读前必看」第 14 条; 验证脚本内嵌全部状态 x 全部谓词的期望矩阵, 在十三份副本上实跑一致 (yaml `metadata.sc11_predicate_validation`)。v3 的谓词改动: (a2) 定位到 Fail-soft 行反引号内的形状 dict; (j3) 改为 python 单行谓词 —— 以 `# Tie-break` 开头的行须恰一行、位于 `def _dedupe_sort_key(` 行之前, 且两行之间 (含首行) 含 `rel_path`, 任一不成立即 FAIL (v3.1 主控核验返修: v3 的 sed 区段在结束后遇到后续 `# Tie-break` 行会重开到文件尾, 已被构造态 `bad_j3_later_tiebreak` 骗过; 多出一行 `# Tie-break` 属书写规则事先告知的可见假红); (j4) 同义词扩为 four-level 各形态 / 4-level 各形态 / 四级 / 四层, 扫描面加 dedupe 测试文件, 不按行排除历史标记, 扫描面外的已发布 CHANGELOG 旧条目不回改 (执笔人对边界的判定); (k) 只认字面 `target_in_subdir`; (l1) 追加 Scenarios 段检查, 并把原「`write_latest_md` docstring 含 `degraded_reason`」收窄到 Returns 段 (执笔人: 只追加不收窄时, Scenarios 里的 `degraded_reason` 会掩盖 Returns 段漏改, 已用负控实跑证实); (j2) 谓词不改, 由 authoring_rules 保留锚点词 `compound key`; 另加 (j3) 保留 `# Tie-break` 行首前缀的书写约束 (v3.1 补: 且该类行在 collector 中唯一) 与 `bad_test_docstring_stale` / `bad_k_paraphrase` 两个验证态 (执笔人: 否则扫描面扩展与只认字面两处改动没有任何状态能证伪)。
13. **分支起点** (v3 补列): 三处 feature 分支改为从 B.1 实测 `origin/master` 起, 替代 proposal `:9`「Phase B 在 `f314785` 起分支」; 主仓另有回落支 —— B.1 时规划提交若仍未经授权推送, 主仓 feature 分支从包含规划提交的本地 master 起 (起点 SHA 与未推送事实记台账), 推送随 5.2 的主仓 PR 发生。理由: aria 已从 `f314785` 前进到 `1cb3872` (v1.73.3), 从旧点起分支会让 gitlink 回退; 主仓 origin/master (`36ea288`) 上没有本 change 的规划文件。
14. **AB 判据口径** (v3 补列): 「无回归」在本次运行内逐 eval 判 (with vs old 同一 grader, with < old 的 eval 复跑两次, 三样本 ≥2 仍劣即回归), 不与存档分数比; 两臂取「代码 + 文档整体」口径 (with = 4.3 回归前记录的 aria HEAD, old = B.1 基线 worktree)。这替代了 SOT 发版前清单「与上一次结果比对, 无回归」的字面。理由: 最近一次含 state-scanner 的存档 (`2026-09-05-v1.70.0-a1-entry-rule6`) 已自判回归臂分数无效度, 与之比对没有意义。场景 1 验收 `delta.pass_rate > 0` 不在本条替代范围内: 仍如实登记, 未达成即请 owner 裁。
15. **勾选改序** (v3 补列): 5.4 在其子步骤 (release_gate / 回帖 / handoff) 完成前勾选; 5.6 在第一次自检完成后勾选, 第二次的证据记台账。理由: 归档门要求 tasks.md 全部勾选才判 complete, 而这些子步骤发生在归档之后。
16. **post_planning R1 conflicted 项 (组 5 执行序) 的裁决** (v3 补列): 组 5 标题原写「5.3 → 5.5」而 yaml 无 TASK-025 → TASK-026 依赖边, qa-engineer 席按标题字面判不一致, tech-lead / code-reviewer 席按依赖图判两者并行、与标题一致; 主控以「标题改为 5.3 与 5.5 互不依赖、不加依赖边」自行裁决 (两任务无数据依赖)。
17. **post_planning R2 两处 conflicted 的裁决** (v3 新增): (1) 基线 RED 是否等价于 proposal 反事实 —— 采 code-reviewer 席 (不等价; 前者比对的是「基线像不像反事实」, 后者比对的是「RED 记录能不能证明该断言的鉴别力」, 后者才是 substitute 证据要回答的问题, 且有实跑输出), 由第 8 条落地; (2) SC-14 兜底反事实的检出源 —— 采 tech-lead / code-reviewer 席 (已提交 SHA 是唯一可复现的检出源), 不采 knowledge-manager 席「写例外、检出源用当时工作树」, 由第 8 条统一 (该兜底随中间态一并删除)。
18. **反事实补丁的组件取法** (v3 执笔人): 3.5 中 SC-4 后半取「无 frontmatter 分支 `_get_file_commit_date` 的路径参数退回 basename」, SC-8 后半取「该行所走 TrackEntry 构造点的 `rel_path` 退回 basename」, 未照搬 proposal 原句「回退为 basename (-only 枚举)」的字面。理由: 2.3 落地后枚举退回 basename 会让该行因 git show 失败直接消失, 首个失败断言落在「行存在」上, 不是原句所指的 `updated_at` 非空 / `rel_path` 保留目录段; 只回退该组件才让失败落在所指断言上。执行时若首个失败断言仍不属原句所指, 按 yaml TASK-035 的规则处置并追加进本清单。

---

## 外向动作与 owner 等待点

单一来源 = `detailed-tasks.yaml` `metadata.owner_gates` (按执行序逐项列出承载任务、性质、未获授权或裁定时的处置; 本文件不复述)。其中三处须特别留意: B.1 前的主仓规划提交推送 (1.3)、按 AB 预测**预期会触发**的 owner 裁决点 (5.5, 在 5.1 之前)、归档 Step 7 建或不建 (5.4)。

---

## 范围边界 — 本文件到哪里为止

| 阶段 | 归属 | 说明 |
|------|------|------|
| 组 1–5: 基线复核 / 测试先行 / 实现与收口提交 / 实现后钉测 / 文档与回归 / AB / 发布同步 / 收尾 | **本文件** | change 自身交付物 |
| Phase B 入口 `phase1_gate` (advisory) | `phase-b-developer` | 若 B.0 调用: 用同一串 raw track-id `handoff-multibranch-subdir-path-fidelity` (不带容器后缀)。预期: CLI 每次调用都新生成 session id, 对本容器 09-12 的 claim 走不到 self-resume ⇒ 另写一条 claim (该 claim 心跳新鲜时还会报 `occupied`, 对象是本容器自己)。属已知缺口, 不是竞争者, 记入台账 (AI 流程判断清单第 7 条) |
| Phase C: 主仓 PR / pre-merge gate (Rule #8) / merge | `phase-c-integrator` | 由 5.2 交付 |
| Phase D: 归档 / claim 释放 / 周期 handoff (Rule #9) / owner 插件更新 | `phase-d-closer` + owner | 归档门消费本文件全部 checkbox; `plugin-cache-currency` 在 owner 更新插件前预期 STALE |
| `handoff.py` 子目录支持 (原选项 (ii)) / `handoff-mechanics.md:114-124` 手改路径未同步第三态 / `reference-snapshot-aria.json` 重采样 / schema `errors[].tracks[]` 形状 | **不在本文件** | 决策单 §2 第 2 行; 统一登记进 5.3 的 issue |
| `_get_file_commit_date` 的 mv 日语义 | **不在本文件** | 决策单 §2 第 5 行; 只由 CHANGELOG 已知边界承载 |

---

## Task Group Overview

| 组 | 主题 | 依据 |
|----|------|------|
| **1** | B.1 基线复核 + 前置核验 + 测试先行 (RED 台账) | proposal Task 1.1 / 1.2, §触点文件清单 |
| **2** | 实现: 枚举层 / 调用方与 legacy id / 读不到不伪造 / fail-soft 键 / 写侧守卫 / 排序键第 5 级 / 收口提交 | proposal §What 1–4、§2.5; 决策单 §2 第 4 行 |
| **3** | 实现后钉测: F1 消费方 / tie-break / legacy id 的 GREEN 与反事实; 其余实体的反事实实跑; proposal SC 表所列反事实 (SC-1 / 3 / 4 后半 / 5 / 8 后半 / 14 / 17) 的实跑 —— 全部三步法, 基线 RED 不充当反事实 | proposal Task 3.1–3.3, SC 表「反事实」列 |
| **4** | 文档同步 (schema / docstring / standards / references) + 全量回归 + 活体 dogfood + 处方面措辞复核 | proposal §6, Task 4.1–4.5, SC-10 / 11 / 12 |
| **5** | 遗留 issue 与 Rule #6 AB → 版本与 CHANGELOG → 引用写法自检 → 子模块合并、合并树回归与授权推送 → 主仓同步面与 PR → 收尾 | proposal Task 5.1–5.5; 执行序以 yaml 依赖为准 |

## 1. B.1 基线复核与测试先行 (RED — 对 B.1 基线实跑红, 组 2 落地后转绿)

- [ ] 1.1 前置核验: 本仓 `docs/handoff/` 无子目录、无非 ASCII 文件名; 当时全部 `refs/remotes/origin/*` 的 `docs/handoff` 树逐个 `git ls-tree` 核无子目录与转义路径; 两份冻结语料 (`aria/skills/state-scanner/tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json`) 内无子目录路径 (结构性成立, 按 proposal 要求照记) — 台账
- [ ] 1.2 新建 `tests/test_handoff_multibranch_path_fidelity.py` (`unittest.TestCase` 风格), 按 SC 分四批写完全部用例 (含 SC-6 / SC-7 / SC-13 与 2.6 的排序键用例); 对 B.1 基线逐条实跑, 记两条 RED 记录 (五族 SC-1 / 3 / 5 / 13 / 17 + 其余 baseline-failing 实体; RED 记录只作 RED 证据, proposal 所写反事实归 3.5) 与回归锁在基线上为绿的记录 — 台账
- [ ] 1.3 B.1 基线复核: 前置 = 规划提交已经 owner 授权推到主仓 origin 与 github 并逐 remote `ls-remote` 核验 (未推送则主仓 feature 分支从包含规划提交的本地 master 起, 见「读前必看」第 13 条); 先 fetch 再实测 aria / standards / 主仓 `origin/master` 并定三处分支起点; 照 proposal §触点文件清单 41 条对 `f314785` 与 `1cb3872` 各跑 `git diff --stat` 并更新偏移表; 重跑 SC-11 验证脚本 (退出码 0, 矩阵与 yaml 实测块逐字节一致); SC-11 的 19 条定位谓词 (yaml `metadata.sc11_baseline_predicates`) 在基线上全假; 建台账骨架 — 台账

## 2. 实现 (aria `state-scanner`)

- [x] 2.0 前置门全部解除: A′ + 写侧守卫 (决策单 2026-09-07, 09-12 追认) · Level 3 不拆 (原 2.0a) · MINOR (原 2.0b) — 决策单 §2 第 2、6、7 行
- [ ] 2.1 枚举层 `_list_handoff_files` (`:240-290`): `-z` 按 NUL 切分并丢空段 · 相对路径的前缀剥离从 `_HANDOFF_TREE_PATH` 派生 (切片支须先判前缀) · 前缀守卫逐项上报 (保持 2-tuple 签名 + 注入 reporter, 双通道) · `.md` 过滤作用于 `rel` 的 basename · docstring 契约句与 `:177` 常量注释 — SC-3 / 9 转绿, SC-2 保持绿, SC-11 (c1)(c2)
- [ ] 2.2 三个仓内调用方与 legacy track_id 改用 `rel_path`; 两个 TrackEntry 构造点都写 `rel_path` (含无 frontmatter 分支 `:686` 的 `_get_file_commit_date` 调用); `scan.py:186` 只拼串改读 `rel_path` (无兜底, 同形早退), `:193` / `:209` 上报的 `filename` 不变; 同批给 `test_scan_integration.py` 的 `HEALTHY_TRACKS` 补键; `:36` / `:332` / `:494` 格式声明同改 — SC-1 / 4 / 6 / 8 / 13 / 17 转绿, SC-11 (i1)
- [ ] 2.3 git show 失败只报 soft_error, 不进 `tracks[]`; 新增 `unreadable_count` 按三类外延实现; 不可解码名 (`chr(0xFFFD) in rel`, 与 proposal 的判据写法等价) 显式跳过并报 `handoff_multibranch_undecodable_path` — SC-5 / 16 / 18 转绿
- [ ] 2.4 fail-soft 早退 dict 补 `unreadable_count: 0` — SC-14 转绿
- [ ] 2.5 pointer 写侧守卫 (`writers/latest_md_writer.py`): 判据 `rel = track.get("rel_path") or track.get("filename")` 再比 `rel == filename`; `_render_pointer` / `_render_pointer_unavailable` 返回 `(content, reason)`; `write_latest_md` 三支恒带 `degraded_reason`; 降级文案写明子目录原因; 该文件全部契约面 (`:32` 模块 docstring / `write_latest_md` docstring `:277-290` / 两个被改函数 docstring / `:159` 口径句) 本项一并改 — SC-15 转绿, SC-11 (k)(l1)
- [ ] 2.6 dedupe 排序键加第 5 级 `rel_path` (决策单 §2 第 4 行附问): 顶层行 (`rel_path == filename`) 优先, 其余按 `rel_path` 字典序取大; 缺 `rel_path` 键按 `filename` 处理; 算法字面见 yaml TASK-014 — 排序键用例转绿
- [ ] 2.7 组 2 收口提交: 2.1–2.6 完成后由主控在 aria feature 分支只 add 组 2 的四个交付物路径并提交、记 SHA, 提交后不带路径的 `git -C aria status --porcelain` 为空; 组 3 的一次性副本一律从该 SHA 检出; 4.1 / 4.2 / 4.4 依赖本项, 在其后开工 — 台账

## 3. 实现后钉测 (GREEN + 反事实, 三步法: 未打补丁副本绿 → 打补丁后红 → 记副本 SHA 与补丁 diff)

- [ ] 3.1 SC-6 (F1 跨文件消费方): 端到端产出 tracks_data、四道前置齐备下 GREEN; 反事实两条 (枚举退回 basename ⇒ (a)(b) 红 / `:180` 局部变量整体重指 `rel_path` ⇒ (c) 红) — 台账
- [ ] 3.2 SC-7 特性化测试 (docstring 首行标注 hypothetical input) 与 2.6 排序键用例 GREEN; 删去第 5 级的反事实; 既有 dedupe 用例 (含 `TestDedupeTiebreakByBranchWhenUpdatedAtAndFilenameTie`) 断言不变 (其两处 docstring 的键层级措辞由 4.2 改) — 台账
- [ ] 3.3 SC-13 GREEN; 三条反事实 (id 沿用 basename / 日期仍拼顶层路径 / 只给 frontmatter 分支加 `rel_path`) 各自转红; 不写「不折叠」断言 — 台账
- [ ] 3.4 其余实体的反事实实跑 (SC-15 四条 / SC-18 两条 / SC-9 (b)(c) / SC-16 两条 / SC-2 解析写错): 在 2.7 SHA 检出的一次性 worktree 副本上按三步法、`python3 -B` 跑, 不在 feature 分支工作树上改; 副本的创建与移除记台账 — 台账
- [ ] 3.5 proposal SC 表所列反事实的实跑 (SC-1 / SC-3 / SC-4 后半 / SC-5 / SC-8 后半 / SC-14 / SC-17): 在 2.7 SHA 检出的一次性 worktree 副本上按三步法只回退该组件 (补丁清单见 yaml TASK-035), 逐 SC 记失败断言文本并对照 proposal 反事实原句; 基线 RED 记录不充当反事实 — 台账

## 4. 文档同步与回归

- [ ] 4.1 `references/state-snapshot-schema.md` §`tracks_multibranch` 同步 (行号按 A.2 偏移表): `rel_path` 行 / `unreadable_count` 与三类外延 / legacy 公式 / pointer 排除句勘正为任意深度 / 键序说明改为五级 (`:1124` / `:1128` / `:1134`, 改键支) / fail-soft 形状补 `unreadable_count` 与 `identity_advisories` (SC-11 (a2) 查反引号内的形状 dict 本身, 同行散文不算) / 两个新 kind 登记 / git show 失败不再产生 legacy 行 / F2 条件式边界 / committer 改 author date / `## Change history` 新增一行; 本项改动由主控在 aria feature 分支单独提交 — SC-11 (a1)(a2)(b)(f1)(f2)(g)(i2)(j2), (j4) schema 侧
- [ ] 4.2 collector docstring / 注释: proposal Task 4.2 清单 + 键层级描述整类 (`:58-61` / `:93-96` / `:355` / `:368-399` / `_dedupe_sort_key` docstring / `:490-492` / `:716-717`, 改键支), 以及 `tests/test_handoff_multibranch_collision_dedupe.py` 的 `:885` / `:1162` 两处 docstring (只改措辞, 断言不动); `:36` / `:332` / `:494` 已由 2.2 落, 本项只核; `references/phase-1-collectors.md:102` 返回契约补 `degraded_reason`; `latest_md_writer.py` 不在本项 (归 2.5); 本项改动由主控在 aria feature 分支单独提交 — SC-11 (j1)(j3)(j5)(l2), (j4) collector 与 dedupe 测试文件侧
- [ ] 4.3 回归 (在 3.1–3.5 与 4.1 / 4.2 / 4.4 / 4.5 之后): 回归前 aria 与 standards 两个 feature 分支的工作树干净并记 HEAD SHA (该 aria SHA 即 5.5 的 with 臂); `run_tests.py` 全量 + pytest 腿 (`test_collision.py` / phase-d-closer `test_fetch_gate.py`) 零失败; SC-10 点名集按两腿执行; 两份冻结语料 (分仓各自对 B.1 基线 diff) 与 1.2 新建的平铺基线 JSON 均未被重生成; SC-11 全部谓词为真; SC-12a (本仓平铺, 背靠背 + ref→SHA 映射比对) 与 SC-12b (子目录临时仓) 活体 dogfood — 台账
- [ ] 4.4 `standards/conventions/session-handoff.md:97` 与 `:171-173` 补第三态 (限定机械 writer 路径, 措辞按「读前必看」第 3 条), 按 `:180` 先例加 Amended 标注, 版本头是否 bump 记台账 (参见 10CG/aria-standards#20); `references/layer-l-integration.md:105` 同步; 记一行「已复核, 本 spec 不对子目录布局表态」; 措辞中的 issue 号先以占位落笔, 5.3 开单后回填; 两侧改动由主控分别在 standards 与 aria 的 feature 分支提交 — SC-11 (h)(l3)
- [ ] 4.5 处方面措辞复核 (在 2.5 与 2.6 之后): `references/rules/advanced-rules.md:443-444,511-512,544` · `RECOMMENDATION_RULES.md:28,30,31` · `phase-d-closer/SKILL.md:218` 逐处读并记结论; 若对前两者落编辑, rule6_note 落行升判据表第二行; 若对 `phase-d-closer/SKILL.md` 落编辑, AB 追加 phase-d-closer; 落了编辑则由主控在 aria feature 分支提交 — 台账

## 5. Rule #6 AB / 发布 / 收尾 (执行序: 5.3 与 5.5 互不依赖、均先于 5.1 (aria 侧; 5.5 含预期会触发的 owner 裁决点) → 5.6 (第一次) → 5.2 (子模块合并与合并树回归) → 5.2 (授权推送与核验) → 5.1 (主仓同步面) → 5.2 (主仓 PR) → 5.4 (含 5.6 第二次))

- [ ] 5.1 版本与发布同步面 (MINOR, 号执行时计): aria 版本 SOT 5 文件 + `CHANGELOG.md` (`### Fixed` 三条 / `### Added` 三个字段与两个新 kind / `### Changed` 至少六条含五条已知边界; 先例用 `grep -n '^## \[1.70.0\]'` 定位); 取号时记下 aria `origin/master` 的 SHA, 供 5.2 合并前复核; 子模块推送核验之后, 主仓两个 gitlink + 16 个版本点 (含 `VERSION:24`) + custom checks 复跑, 主仓同步面由主控在主仓 feature 分支提交 — SC-11(e)
- [ ] 5.2 Phase C: 子模块合并按固定顺序 —— fetch → 检出 master 并断言本地 master 等于 origin/master (不等先 `merge --ff-only`, 不能快进即停下上报), 记下此刻 SHA → aria origin/master 相对取号时前进则回 5.1 重算取号 → 两个子模块工作树干净 (standards 占位号已回填) → 各自本地 `git merge --no-ff` → 核版本 5 文件等于取号值且 origin 与 github 均无同名 tag (不符则按记下的 SHA 回退本地合并、回 5.1 重新取号; 回退命令与前置见 yaml TASK-029) → 在干净工作树且 HEAD 等于合并 SHA 时对合并树重跑两腿回归与 SC-11 全部谓词 → 通过后打 aria tag; 推 master 之前再核两个远端无同名 tag, owner 授权后双推并逐 remote `ls-remote` 核验 master 与 tag; 主仓 gitlink 从实测值前进、不得回退; 主仓开 PR 前把不带路径的 `git status --porcelain` 原样记台账, 其中不得有任何一行触及本 cycle 交付物路径 (清单见 yaml TASK-031; 其余行逐条写明归属并判定与本 cycle 无关, 不 stash、不删除、不顺带提交他人文件), AB 结果目录与台账已提交, PR 正文与 diff 新增行已自检, 经 `phase-c-integrator` 开 PR 过 pre-merge gate 后合并
- [ ] 5.3 遗留缺口 issue 开在 `10CG/aria-plugin` (外向, owner 授权后发): `handoff.py` 子目录支持 + SC-15 布局 2 复现 + proposal Task 5.3 的 (a)–(f) 分条 + (g) `handoff-mechanics.md:114-124` 手改路径未同步第三态 + `session-handoff.md:97`「自动」一词 + 子目录布局不表态的锚点; 开单后回填 4.4 措辞中的占位号 (standards 追加提交); owner 不授权开单时 4.4 措辞按 yaml TASK-025 的回落形态落笔
- [ ] 5.4 Phase D: 归档前只读预演归档门 (`spec_complete.py --gate`) 并记 verdict 与 unverified_claims (预期三条, 以执行时预演为准); D.2 之前请 owner 裁 Step 7 建或不建 tracker issue (裁不建则只跳过 Step 7, 裁定原文记台账与周期 handoff); 本行在归档前勾选, 其余子步骤证据记归档后台账 (`openspec/archive/<日期>-handoff-multibranch-subdir-path-fidelity/verification-ledger.md`, 纳入 Phase D 提交); `release_gate` 释放 claim; 10CG/Aria#195 回帖关闭; 周期 handoff 含两处记录 (`reference-snapshot-aria.json` 未重采样; standards 已改) 与「AI 流程判断清单」; 提交经授权双推并逐 remote `ls-remote` 核验 — SC-11(d)(h)
- [ ] 5.5 Rule #6 照跑 AB (用 `/skill-creator` 跑 state-scanner): 前置 = owner 以 `ARIA_COORDINATION_NO_PUSH=1` 启动会话并在子进程实测变量生效; 按 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 场景 1 三步执行 (启动 / transcript 核 `push_skipped`, 各臂都没跑到两个 gate CLI 时记「未触达」并以远端前后比对兜底 / 事后强制对齐本地协调 ref); 开跑前在结果目录写 PREDICTION.md; 两臂 = 代码加文档整体 (with 取 4.3 回归前记录的 aria HEAD, old 取 B.1 基线 worktree); 无回归在本次运行内逐 eval 判 (with 劣于 old 的 eval 复跑两次, 三样本中两个以上仍劣即判回归), 判回归或出现 WITHOUT_BETTER 即阻断 5.1 / 5.2 并上报 owner; RESULT.md 如实登记场景 1 验收 `delta.pass_rate > 0` 是否达成, 未达成或回归面无效度则结论写「未被有效测试」, 5.1 之前请 owner 裁 (按预测预期会触发); 结果落 `aria-plugin-benchmarks/ab-results/` (勾选本行时把这个父目录 token 整个替换为本次结果目录全路径, 行内不残留父目录); 开 AB 套件缺口 issue (外向); RESULT.md 与 issue 正文先自检; AB 结束后换不带该变量的会话继续 — rule6_note
- [ ] 5.6 引用与编号写法自检 (原 proposal Task 5.4a, 按 standards `content-integrity.md` §4.4 / §4.5 更新), 分两次: 子模块合并前一次, 周期 handoff 与回帖落笔前一次; 本行在第一次自检完成后勾选, 第二次的证据记归档后台账; 本 cycle 新写或改动的文字 issue 引用全限定、文内编号不用 `#` 与带圈字符; PR 正文与主仓 PR diff 新增行在 5.2 开 PR 前自检, RESULT.md 与套件缺口 issue 正文在 5.5 自检; `check_bare_issue_refs.py` 作手动自检, 不把整份文件 rc 0 当验收门槛 — 台账

---

## Success Criteria ↔ 任务映射

| SC | 编写 (RED) | 转绿 | 钉测 / 反事实 |
|----|------|------|------|
| SC-1 | 1.2 | 2.2 | 3.5 + 4.3 |
| SC-2 | 1.2 (基线 JSON 在实现前生成) | (回归锁) | 3.4 + 4.3 (基线 JSON 未重生成) |
| SC-3 | 1.2 (仓内 `core.quotePath true`) | 2.1 | 3.5 + 4.3 |
| SC-4 | 1.2 | 2.2 (后半) | 3.5 (后半) + 4.3 |
| SC-5 | 1.2 | 2.3 | 3.5 + 4.3 |
| SC-6 | 1.2 | 2.2 | 3.1 |
| SC-7 | 1.2 | (回归锁) | 3.2 |
| SC-8 | 1.2 | 2.2 (后半) | 3.5 (后半) + 4.3 |
| SC-9 | 1.2 | 2.1 | 3.4 |
| SC-10 | — | — | 4.3 (两腿) / 5.2 (合并树) |
| SC-11 | 1.3 (基线全假) | 2.1 (c1)(c2) / 2.2 (i1) / 2.5 (k)(l1) / 4.1 (a1)(a2)(b)(f1)(f2)(g)(i2)(j2) / 4.2 (j1)(j3)(j5)(l2) / 4.1 与 4.2 (j4) / 4.4 (h)(l3) / 5.1 (e) / 5.3 与 5.4 (d)(h) | 4.3 (全部谓词复跑) / 5.2 (合并树复跑) |
| SC-12a / SC-12b | — | — | 4.3 |
| SC-13 | 1.2 | 2.2 | 3.3 |
| SC-14 | 1.2 | 2.4 | 3.5 + 4.3 |
| SC-15 (六个布局) | 1.2 | 2.5 | 3.4 |
| SC-16 | 1.2 | 2.3 (`rel_path` 由 2.2, `unreadable_count` 由 2.3) | 3.4 |
| SC-17 | 1.2 | 2.2 | 3.5 + 4.3 |
| SC-18 | 1.2 | 2.3 | 3.4 |
| 决策单 §2 第 4 行 (排序键第 5 级) | 1.2 | 2.6 | 3.2 |

## rule6_note

单一来源 = `detailed-tasks.yaml` `metadata.rule6_note` (本节不复述, 防两份不同文)。
