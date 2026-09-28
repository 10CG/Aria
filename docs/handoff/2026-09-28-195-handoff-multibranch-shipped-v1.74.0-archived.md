---
track-id: handoff-multibranch-subdir-path-fidelity
owner-container: simonfish/bfe8285d
phase: D.3
status: done
updated-at: 2026-09-28T10:51:13Z
---

# Aria — 周期 Handoff (2026-09-27 ~ 28) — `10CG/Aria#195` handoff-multibranch-subdir-path-fidelity 全周期收尾: Rule #6 AB → aria-plugin v1.74.0 → PR `10CG/Aria#222` → 归档

> **性质**: 周期收尾 (phase-d-closer D.3, cycle 单元; Rule #9)。上一份会话层 handoff: [2026-09-27-session-close-195-task025-legacy-issue-204.md](./2026-09-27-session-close-195-task025-legacy-issue-204.md)。**权威实测台账**: `openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity/verification-ledger.md` (本文只放结论与指针, 证据以台账为准)。

---

## §0 入口 (新 session 优先读)

1. **本轨已终结**: 十步循环走完。aria-plugin **v1.74.0** 已发布 (aria `5215cf2` + tag `v1.74.0` / standards `2bc1c4c`, 两个 remote 逐个核验一致), 主仓 PR `10CG/Aria#222` 以 merge commit `03f97ac` 合并, Spec 已归档到 `openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity/`, 本轨 claim 已释放为 `done` (协调 ref `4d40f84`)。`10CG/Aria#195` 的关闭回帖在本文所在提交推送之后执行 —— 结果见文末追记 (写作时自指排除)。
2. **工作区**: 主仓在 `master`; 两个子模块都检出 `master` (aria `5215cf2` / standards `2bc1c4c`), 与主仓 gitlink 一致, 不再有 `M aria` / `M standards` 的中间态。三个仓的 `feature/handoff-multibranch-subdir-path-fidelity` 分支本地与远端都还在, 是否删除由 owner 定。
3. **下一条轨**: `10CG/Aria#199` (`pre-merge-completeness-gate-change-scope`, claim `claims/bfe8285d/s-73b9@1606.yaml` active, 心跳 `2026-09-28T07:52:48Z` ⇒ **最晚 2026-09-29T07:52Z 前刷**)。它的 B.1 入口门第 1 项「`10CG/Aria#195` 完成 C.2」**现已满足** (`03f97ac`); 但按 owner 2026-09-27 决策单第 3 项, 进 B.1 前先做 **v2.7 返修** (六条 minor + 各轮未处置 minor 与基线平移合成; 另须改计划里对 `no-unresolved-version-placeholder` 的 10 处旧行为描述)。
4. **待 owner 的事**: 见 §4 高 / 中优先级。

---

## §1 已完成 (UTC)

| 时间 | 任务 | 结果 | 提交 / 外发 |
|---|---|---|---|
| 09-27 16:52 – 17:33 | TASK-026 Rule #6 AB (以 `ARIA_COORDINATION_NO_PUSH=1` 启动的专用会话) | 13 个 eval 两臂同为 50/78, delta.pass_rate = +0.0000, 与跑前 PREDICTION 相符; eval 5 复跑两次 1/3 不判回归; 协调 ref 全程 `e911132`; 结论「未被有效测试」→ owner 裁放行 | 主仓 `be91134`; 套件缺口 `10CG/aria-plugin#205` |
| 09-27 18:11 – 18:14 | 普通会话入口 | 变量实测未设; 两条 claim 心跳经前置检查刷新 | 协调 ref `4ae229e` |
| 09-27 18:15 起 | TASK-027 版本号 + CHANGELOG + standards 1.4.0 | 取号 `1.74.0` (两个 remote 无 `v1.74.*`, `10CG/Aria#199` 无预留号); CHANGELOG `[1.74.0]` 逐条对真代码核; 提交面经 owner 当场裁定扩为六个文件 (含 `README.zh.md`) | aria `1ad31fa` · standards `56306d1` · 主仓 `4c754a2` |
| 09-27 | TASK-028 写法自检第一次 | 三仓新增行裸引用首跑 2 / 0 / 5, 订正后归零 | aria `820ea57` · 主仓 `016a43a` |
| 09-27 18:33 → 09-28 01:55 | TASK-029 本地合并 + tag + 合并树回归 | 首次执行停在第 2 步 (判据与 TASK-023 规定矛盾) → owner 裁按实质判通过 → 跨 UTC 日订正发布日期 → 从第 1 步重走: 双父合并断言、取号终核、`Ran 1627 OK` + 28 + 11 + 谓词 19/19 → 打 tag | aria `651ff6e` / merge `5215cf2` / tag `v1.74.0` (`f951d1e`) · standards merge `2bc1c4c` · 主仓 `877ed17` |
| 09-28 02:00 | TASK-034 子模块原子双推 (owner 授权) + 主仓 feature 备份双推 (同批授权) | 两个 remote 的 master / tag 对象 / tag 指向全部 MATCH; feature `877ed17` 两端 MATCH | 主仓 `ab200c6` |
| 09-28 02:05 | TASK-030 主仓同步面 | gitlink 前进; 16 个版本点 → 1.74.0 (含补上 `VERSION:24`); custom checks 15 pass + `plugin-cache-currency` 预期 STALE | 主仓 `a99dd8d` · `9b4a291` |
| 09-28 02:10 – 07:48 | TASK-031 主仓 PR (owner 授权五项) | 同步 master (merge 不 rebase) → PR → C.2.4 green (not_applicable, 已按 SKILL 原样呈报警告行) + C.2.4.5 PASS → merge commit → 本地快进 → C.2.5 两个 remote parity match → gitlink_integrity 六组 ok | 主仓 `0d24604` / `6fdff9f`; PR `10CG/Aria#222` → `03f97ac` |
| 09-28 07:48 起 | TASK-032 Phase D | 27 行勾选; 归档门预演 verdict=warn (三条已知检查器假阳性); owner 裁 Step 7 不建 tracker; openspec-archive Step 1-6 (五条位置断言全绿); `release_gate` 释放本轨 claim; 第 2 类假阳性另开单 | 主仓 `06e2e95` · `c8238c3`; 协调 ref `4d40f84`; `10CG/aria-plugin#206` |

---

## §2 AI 流程判断清单 (Rule #10 §5, 请 owner 复议)

### 2.1 `tasks.md`「AI 流程判断清单」全文照录 (第 1 ~ 36 条)

下列判断在 A.2 / A.3 与 post_planning R1–R3 的历次 rework 中由 AI 自行作出, 不来自 owner 裁定: 第 1–17 条出自主控 (v2 / v3 的处置与 R1–R2 聚合裁决), 第 18 条与第 12 条中标「执笔人」的部分出自 v3 执笔人, 第 19–21 条是 v3 / v3.1 落地时未列而 R3 点出的旧判断, 第 22–26 条是 v4 (post_planning R3 rework) 新作的判断, 第 27–32 条是 v5 / v6 (post_planning R4 与 R5 rework) 新作的判断。post_planning 的收口方式是 **owner 裁定** (五轮未收敛, owner 裁「接受当前结论 + 定点修后收口」), 不是 AI 自判已收敛。均已公开列出并经 post_planning 审阅, 但按 `standards/conventions/configured-gate-authority.md` §5 仍须写进 handoff 请复议; 5.4 的周期 handoff 照录本清单并追加 Phase B / C / D 新增项。

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
12. **SC-11 验收判据的形态**: proposal 的整文件 grep 改为定位谓词 (19 条), 与原文的逐项差异见「读前必看」第 14 条; 验证脚本内嵌每态的期望 FAIL 集 (由脚本展开成全矩阵后逐格比对), 在二十六份副本上实跑一致 (yaml `metadata.sc11_predicate_validation`)。v3 的谓词改动: (a2) 定位到 Fail-soft 行反引号内的形状 dict; (j3) 改为 python 单行谓词 —— 以 `# Tie-break` 开头的行须恰一行、位于 `def _dedupe_sort_key(` 行之前, 且两行之间 (含首行) 含 `rel_path`, 任一不成立即 FAIL (v3.1 主控核验返修: v3 的 sed 区段在结束后遇到后续 `# Tie-break` 行会重开到文件尾, 已被构造态 `bad_j3_later_tiebreak` 骗过; 多出一行 `# Tie-break` 属书写规则事先告知的可见假红); (j4) 同义词扩为 four-level 各形态 / 4-level 各形态 / 四级 / 四层, 扫描面加 dedupe 测试文件, 不按行排除历史标记, 扫描面外的已发布 CHANGELOG 旧条目不回改 (执笔人对边界的判定); (k) 只认字面 `target_in_subdir`; (l1) 追加 Scenarios 段检查, 并把原「`write_latest_md` docstring 含 `degraded_reason`」收窄到 Returns 段 (执笔人: 只追加不收窄时, Scenarios 里的 `degraded_reason` 会掩盖 Returns 段漏改, 已用负控实跑证实); (j2) 谓词不改, 由 authoring_rules 保留锚点词 `compound key`; 另加 (j3) 保留 `# Tie-break` 行首前缀的书写约束 (v3.1 补: 且该类行在 collector 中唯一) 与 `bad_test_docstring_stale` / `bad_k_paraphrase` 两个验证态 (执笔人: 否则扫描面扩展与只认字面两处改动没有任何状态能证伪)。 v4 另改: (j1)(j3)(j2) 由「块内出现 rel_path」改为钉现状键元组 ((parse_ok 之后须含 rel_path), 因为「首行写五级、另起一段讲 rel_path、元组仍四元」能骗过旧写法 (R3 code-reviewer 席构造 `bad_tuples_stale_para` 实证); (l1) 的模块 docstring 与 Returns 两处都只取「标题到第一个空行」的块 (顶部场景列表与 Never raises 段会遮蔽); (j4) 正则加左边界, 讲目录深度的 `14-level` 不再假红。四条替换谓词取 R3 code-reviewer 席已三态实跑的写法。 v5 再改 (见第 29 条): (j1)(j3)(j2) 换量为「只看 `(parse_ok` 起的那一对平衡括号之内」, (l1) 丢掉标题行余部并把 Scenarios 判据改成结局行计数, (c2) 收紧到 `_list_handoff_files` 自己的 docstring。 v6 再改 (见第 29 条 v6 段): (j1)(j3)(j2) 由「串落在某窗口内」换成结构量 —— 平衡括号组内深度 1 的元素恰 5 个且第 5 元逐字为 `(rel_path == filename, rel_path)`。
13. **分支起点** (v3 补列): 三处 feature 分支改为从 B.1 实测 `origin/master` 起, 替代 proposal `:9`「Phase B 在 `f314785` 起分支」; 主仓另有回落支 —— B.1 时规划提交若仍未经授权推送, 主仓 feature 分支从包含规划提交的本地 master 起 (起点 SHA 与未推送事实记台账), 推送随 5.2 的主仓 PR 发生。理由: aria 已从 `f314785` 前进到 `1cb3872` (v1.73.3), 从旧点起分支会让 gitlink 回退; 主仓 origin/master (`36ea288`) 上没有本 change 的规划文件。
14. **AB 判据口径** (v3 补列): 「无回归」在本次运行内逐 eval 判 (with vs old 同一 grader, with < old 的 eval 复跑两次, 三样本 ≥2 仍劣即回归), 不与存档分数比; 两臂取「代码 + 文档整体」口径 (with = 4.3 回归前记录的 aria HEAD, old = B.1 基线 worktree)。这替代了 SOT 发版前清单「与上一次结果比对, 无回归」的字面。理由: 最近一次含 state-scanner 的存档 (`2026-09-05-v1.70.0-a1-entry-rule6`) 已自判回归臂分数无效度, 与之比对没有意义。场景 1 验收 `delta.pass_rate > 0` 不在本条替代范围内: 仍如实登记, 未达成即请 owner 裁。
15. **勾选时点与改序** (v3 补列, v4 改写): 27 行 checkbox 全部在 5.4 的归档预演之前由主控一次勾选, 随 Phase D 提交; 其中 5.4 在其子步骤 (release_gate / 回帖 / handoff) 完成前勾选, 5.6 在第一次自检 (5.6 第一次) 完成后即满足条件但同样到 5.4 才勾, 5.5 勾选时按 yaml TASK-032 替换父目录 token。理由: 归档门要求 tasks.md 全部勾选才判 complete, 而这些子步骤发生在归档之后; tasks.md 只有 Phase D 一个提交点, 提前勾会让 5.2 开 PR 前的有范围核验恒假 (R3 tech-lead 席临时仓三态实证)。
16. **post_planning R1 conflicted 项 (组 5 执行序) 的裁决** (v3 补列): 组 5 标题原写「5.3 → 5.5」而 yaml 无 TASK-025 → TASK-026 依赖边, qa-engineer 席按标题字面判不一致, tech-lead / code-reviewer 席按依赖图判两者并行、与标题一致; 主控以「标题改为 5.3 与 5.5 互不依赖、不加依赖边」自行裁决 (两任务无数据依赖)。
17. **post_planning R2 两处 conflicted 的裁决** (v3 新增): (1) 基线 RED 是否等价于 proposal 反事实 —— 采 code-reviewer 席 (不等价; 前者比对的是「基线像不像反事实」, 后者比对的是「RED 记录能不能证明该断言的鉴别力」, 后者才是 substitute 证据要回答的问题, 且有实跑输出), 由第 8 条落地; (2) SC-14 兜底反事实的检出源 —— 采 tech-lead / code-reviewer 席 (已提交 SHA 是唯一可复现的检出源), 不采 knowledge-manager 席「写例外、检出源用当时工作树」, 由第 8 条统一 (该兜底随中间态一并删除)。
18. **反事实补丁的组件取法** (v3 执笔人): 3.5 中 SC-4 后半取「无 frontmatter 分支 `_get_file_commit_date` 的路径参数退回 basename」, SC-8 后半取「该行所走 TrackEntry 构造点的 `rel_path` 退回 basename」, 未照搬 proposal 原句「回退为 basename (-only 枚举)」的字面。理由: 2.3 落地后枚举退回 basename 会让该行因 git show 失败直接消失, 首个失败断言落在「行存在」上, 不是原句所指的 `updated_at` 非空 / `rel_path` 保留目录段; 只回退该组件才让失败落在所指断言上。执行时若首个失败断言仍不属原句所指, 按 yaml TASK-035 的规则处置并追加进本清单。v4 补: 补丁 1 (SC-1 / SC-17 共用的枚举层退回 basename) **不**窄化 —— 但 2.3 落地后 git show 失败不再追加 legacy 行, 所以 proposal 原句的「该行变 legacy」现表现为「该行不在 tracks[] + 该 kind 出现 + unreadable_count == 1」(R3 backend-architect 席真仓实测), 「所指断言」以 yaml TASK-035 各补丁条写明的现表现形态为准。
19. **TASK-031 提交面核验放宽** (v3.1 主控核验返修, R3 补列): R2 处置写的是「主仓 `git status --porcelain` 为空」, 实测健康常态下主仓就有他轨与其它审计的未跟踪文件, 该判据不可满足; 改为「不得有任何一行触及本 cycle 交付物路径 (清单见 yaml TASK-031), 其余行逐条记归属」。保留了「本 cycle 自身的产物必须已提交」这一核心意图, 放弃的是「全局清空」。
20. **TASK-018 不变式替代** (v3): 「feature 分支工作树 git status 前后一致」换成副本生命周期证据 (补丁 diff 以副本路径为根、副本创建与移除记台账、任务结束时 worktree list 不含本任务副本), 补丁泄漏改由 4.3 全量回归兜底。理由: 2.7 之后组 3 与组 4 并发, 组 4 会合法地改 aria 工作树, 原不变式在并发下不可满足。
21. **合并树回归原位跑** (v3, 未采纳审计席方案): R2 的 tech-lead 席建议在合并 SHA 的 `git worktree add` 副本上跑, 主控未采纳 —— `run_tests.py` 会在所在仓跑 `scan.py`, 放到主仓布局之外的 aria 副本里, 依赖主仓布局的用例可能假红; 改以「工作树干净且 HEAD 等于合并 SHA」的前提达到同一目的。另: v3.1 主控核验返修的另两项 (TASK-029 / TASK-034 回退命令写死、验证脚本不依赖 assert) 只是让既有要求更稳固, 不放宽任何验收义务。
22. **罕见并发路径一律 fail-closed** (v4, 按 R3 的 R4 处置原则 1): 取号被占 / 合并冲突 / 取号终核不符 / 推送被拒 / 只推成一个远端 —— 一律停在本步、原样记台账、上报 owner, 计划里只给先例指针 (aria `ec72175`) 而不展开自动恢复流程。理由: 前三轮每修一次就新增一层流程, 下一轮的缺陷就长在新流程上; 这些路径都罕见且后果外向, 停下比自动恢复安全。 v5 补两条口径: (a) 经 owner 确认的恢复动作做完后, 5.2 的三支一律从 TASK-029 第 1 步重走 (恢复动作落在 feature 分支上, 而第 5 / 6 步已把两个子模块的本地 master 复位、owner 等待期间远端还可能再前进), 唯一例外是第 2 步工作树不干净这一本地可修复分支; (b) 不需要 owner 动作、只需知情的止损停摆 (v6 实为七处: TASK-029 第 1 / 2 / 3 / 7 / 8 步 · TASK-034 同名 tag · TASK-032 开头 ff-only) 合并为 `owner_gates` 的一项, 不逐条单列 —— owner 面对的等待点数目不变。
23. **删去 WITHOUT_BETTER** (v4, 按 R3 PP3-M5): 该标签是 `AB_TEST_OPERATIONS.md` 对 with vs without 的判定, 与本次 with vs old 的两臂不同源, 官方聚合脚本也不产出它; 其对应物是 5.5 已写死的逐 eval 回归判据。同批把 `delta.pass_rate` 的取法写死为 mean(with) − mean(old), 因为官方 `aggregate_benchmark.py` 对 `with_skill` / `old_skill` 目录给出的是 old − with (符号相反, R3 tech-lead 席实跑)。
24. **post_planning R3 两处 conflicted 的裁决** (v4): (1) TASK-035 补丁 1 —— backend-architect 席建议比照补丁 5 窄化为「构造点 rel_path 退回 basename」, 不采; SC-1 是 issue 主症状, 它要抓的回归就是枚举层退回 basename, 换成构造点回退测的就成了 SC-8 的面, 只把原句在 2.3 落地后的表现形态写明 (见第 18 条与 yaml TASK-035)。(2) TASK-029 步序 —— 采 tech-lead 席判 Major (占位检查在 master 工作树上恒真, 有四态实跑证据), 不采 code-reviewer / qa-engineer 的 Minor 与 backend-architect 的「下游兜底」。
25. **两类协调 ref 推送的口径统一** (v4, 按 R3 m1): B.0 `phase1_gate` 认领推送与 5.4 `release_gate` 释放 claim 的推送都是外向推送, 统一为「需授权, 与同批的主推送一起请 (前者并入 1.3 的规划提交推送, 后者并入 Phase D 双推), 不另设独立等待点」。理由: 两者是同一机制, 分别单列会让 owner 面对两个语义相同的等待点; 并批后 `metadata.owner_gates` 仍能逐项查到。
26. **覆盖两个 Skill 的默认合并策略** (v4, 按 R3 m5): 5.2 写死「同步 `origin/master` 用 merge 不 rebase、主仓 PR 以 merge commit 合并不 squash」, 覆盖 `phase-c-integrator` C.2.1 的 sync rebase 默认与 `branch-manager` 的 squash 默认。理由: 回落支让规划提交随 feature 分支进 PR, rebase 或 squash 会让审计报告与台账引用的主仓 SHA 不在远端 master 上, 事后无法按 SHA 复核 (本仓 PR 先例均为 merge commit)。
27. **删去 TASK-029 第 7 步的谓词一致性核验** (v5, 按 R4 PP4-M3): 该核验要求在合并树上跑 `sc11-predicate-validation.py --emit-json` 再与 yaml 谓词块比对, 但脚本的全部模拟改动锚定 1cb3872 原文, 实现落地后锚点必然消失 ⇒ 退出码 3、拿不到 JSON (R4 tech-lead 席只施加一处真实编辑即实测触发); 且脚本与 yaml 自 TASK-001 起无人改动, 比对结果在健康常态下恒等于 TASK-001 的结果 (恒绿)。两份谓词原文的一致性由 TASK-001 一次性核验承担。该核验是主控在 R3 采纳 m11 时未核执行时点的处方, 本轮撤回。
28. **主仓 master 的多远程推送交给 `phase-c-integrator` C.2.5** (v5, 按 R4 PP4-M4): 原 5.2 断言「合并后主仓 master 在 origin 与 github 的 ls-remote SHA 一致」在计划动作集下恒假 —— PR 走 Forgejo 服务端合并只发生在 origin, 而计划里主仓第一次 github 推送要到 Phase D。改为由已有 Skill 承担并核对其配置事实 (C.2.5 默认 enabled · enforced remote 自动发现为 origin 与 github · `fail_on_partial_push` 默认阻断), 计划只保留断言与失败口径, 不自写手工推送步骤。子模块的分支合并与 tag 推送 C.2.5 不管, 仍由 5.2 的 TASK-029 / TASK-034 承担。 **v6 补** (按 R5 PP5-M2 / M3): 委派方必须自己把被委托方的触发前置建起来 —— PR 合并后先 `git fetch origin` → `git checkout master` → `git merge --ff-only origin/master` 并断言 HEAD 等于该 PR 的合并提交 (C.2.5 的触发条件写死「合并成功且 master 已 fast-forward」, 其第 1 步取的 expected_sha 就是合并后本地 master HEAD; 陈旧 master 下它必然 match=false 误红); 并核对被委托方的作用对象 —— C.2.5 按 `git submodule status --recursive` 枚举, 本仓实为三个子模块 (aria / standards / **aria-orchestrator**, 后者是他轨的 v2.0 运行时仓, 同样带 origin 与 github), 故调用前先断言 aria-orchestrator 无待推内容, 不成立即停下, 本 cycle 不顺带把他轨未推送的提交推到两个远端。理由: 委派时只核「它做什么」不够, 还要核「它何时触发」与「它作用在哪些对象上」(memory `delegate-verify` 的三问)。
29. **SC-11 谓词第三次换量** (v5, 按 R4 PP4-M6 / M7 / m13): (j1)(j3)(j2) 由「块 / 行内 `(parse_ok` 之后含 rel_path」换成「只看 `(parse_ok` 起的那一对平衡括号之内」—— 前者的「其后」是整块剩余文本, 元组留四元、紧跟其后补一句 rel_path 就能全绿 (R4 code-reviewer 与 qa-engineer 两席各自构造实证, 与 memory `redfix-change-quantity` 同形: 两轮都在同一个量上挪边界); (l1) 丢掉标题行余部, Scenarios 改判「含 → 的结局行至少四条且其中一条含 target_in_subdir」而不是「段内出现某子串」; (c2) 收紧到 `_list_handoff_files` 自己的 docstring。执笔人另加一个合法写法守卫态 (元组跨两行不得假红)。 **v6 (按 R5 PP5-M1) 第四次换量并换了量纲**: 平衡括号仍是「串落在某窗口内」, R5 的 code-reviewer 席 (元组内嵌括注 `filename (basename, never rel_path)`) 与 qa-engineer 席 (第 5 元写成 `note: rel_path NOT used`) 各自独立绕过; 现改为数结构 —— 取 `(parse_ok` 起的平衡括号组, 深度 1 的逗号分隔元素须恰 5 个, 且第 5 元归一化空白后逐字含 `(rel_path == filename, rel_path)`; 两种攻击各加一个坏态 (`bad_tuples_inner_paren` / `bad_tuples_denial_clause`) 钉住。执笔人在两席给的写法上做了合并: code-reviewer 席的元素计数式单独用时抓不住 qa-engineer 席的否认子句 (实跑 3 格假绿), 故把 qa-engineer 席建议的规范字面比对并入同一判据。
30. **验证脚本的期望表达收窄** (v5, 按 R4 跨簇一致性第 4 条): 内嵌期望由 18 态 x 19 谓词的定值矩阵改为「每态只声明期望 FAIL 的谓词集」(`EXPECTED_FAILS`), 由脚本展开成全矩阵后逐格比对; 断言强度不变 (base 全 FAIL / target 全 PASS / 每个坏态只对应谓词 FAIL 一条不减), stdout 仍打印完整矩阵, yaml 实测块照旧由脚本输出重生成。理由: 加一个状态的成本从手推 19 格降到写一行, 而每轮重算全矩阵本身就是 R2–R4 反复出错的面。
31. **两个子模块的合并视为一个整体** (v5, 按 R4 PP4-M2): 5.2 的 TASK-029 第 5 步里, aria 与 standards 任一仓合并失败 ⇒ 对**两个**仓都执行回退条 (已产生合并提交的 `reset --hard` 回第 3 步 SHA, 停在冲突中的 `merge --abort`, 都没有的不执行命令), 两仓 HEAD 一并回到第 3 步记下的 SHA 后停下上报; 同批在第 3 步的 `merge --ff-only` 之后补一次「master == origin/master」复核。理由: 一仓合成功另一仓冲突时, 成功那仓的合并提交会留在 master 上无人处理, 重走时 `--no-ff` 返回 `Already up to date.` 而不产生本轮的合并提交 (临时仓实测); 「本地 master 领先」这一支下 `merge --ff-only` 返回 0 却不改变 master, 不复核就静默放行。
32. **半推或被拒一律停下, 且不得 bump gitlink** (v5, 按 R4 PP4-M5): 5.2 的全部外向推送 (子模块 TASK-034 / 主仓 TASK-031 与 5.4 的 Phase D 双推) 统一口径 —— 被拒或只推成一个远端 ⇒ 不 force、不改写历史、不重打 tag, 原样记台账并停下上报; 5.1 的主仓 gitlink bump (TASK-030) 新增前置「TASK-034 对 origin 与 github 双方均已 ls-remote 核验一致」, 任一方未一致不得 bump。理由: 半推后 bump 出的 gitlink 在 github 侧指向不存在的对象, GitHub 的 `clone --recursive` 即断 (CLAUDE.md 多远程硬约束 1 · memory `mirror_sync_needs_mechanical_backstop`), 这是不可逆损坏。
33. **standards `session-handoff.md` 升 1.4.0 并入 TASK-027** (Phase B 执行期计划外改动, **owner 2026-09-27 裁定**, 决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` 第 1 项): 头部 Version 行一次补齐 1.3.0 之后的三次增量 (`d217ed0` / `21748d4` / 本 cycle `11b0a14` + `d86fc91`), 按 `10CG/aria-standards#20` 建议的格式逐条列出, 提交到 standards feature 分支 (先于 TASK-029 合并); 合并后回帖关闭 `10CG/aria-standards#20` (届时另请授权)。更正组 4 TASK-023 台账「Version 头保持 1.3.0」的理由。
34. **TASK-027 提交面由五个文件扩为六个** (Phase B 执行期计划外改动, **owner 2026-09-27 当场裁定**): verification 末条写「`git -C aria show --stat HEAD` 恰含这五个文件」, 执行时实读发现 `aria/README.zh.md` 第 5 行同样带版本号与发布日期, 且 v1.73.1 / v1.73.2 / v1.73.3 三次发版提交都同改了它 (实际发版面是六个文件)。按五个文件提交会让中文 README 停在旧号, 现有 custom check 不读这一行、不会报出。owner 裁「带上, 六个文件一次提交」⇒ 该条 verification 的字面不成立, 台账如实记录。
35. **顺手订正 `aria/VERSION` 的「## 版本号」代码块** (AI 判断, 请复议): 该代码块在 v1.73.3 发版时漏改, 停在 `1.73.2`; 它与头部版本行同在 TASK-027 的交付文件内, 改号时一并订正为 `1.74.0`, 未扩大文件面。同文件「## 说明」节的 Minor 计数列表长期未维护 (止于 Minor 38), 属历史记述, 未动。
36. **TASK-029 第 2 步 standards 占位核验的判据与 TASK-023 规定不一致** (**owner 2026-09-28 裁「按实质判通过, 重走后继续」**): 判据要求「经机械 latest_md_writer 写入时」两处窗口都含 `10CG/aria-plugin#<n>`, 但 TASK-023 的 verification 只要求 `:171-173` 那节写跟踪指针、`:97` 只补限定从句, 故 `:97` 窗口按字面恒不成立; 另定位串写成不带反引号, 与文件实际写法 (带反引号) 不符, 字面命中 0 处。实质: 两窗口 `#<` 均为 0, 指针所在窗口在回填后含 `10CG/aria-plugin#204`、回填前 `11b0a14` 不含 (自然负控有效)。计划文件未改; 若日后复用该判据, 应只取指针所在窗口、定位串按文件实际写法。

### 2.2 Phase B / C / D 执行期新增 (不在上面清单里; 每项: 做了什么 + 理由 + 请 owner 复议)

37. **AB 臂与评分员的隔离做法** (TASK-026): 臂的产出先写 scratchpad 的中性目录, 两臂以随机 X / Y 匿名; 每个 eval 由同一个评分员一次评两臂, 全部评完再按映射复制进结果目录。理由: 计划只要求「同一 grader」, 这样做还能减少臂读到评测材料、评分员知道哪臂是新版的机会。**请 owner 复议**。
38. **把「不跑两个 gate CLI、不写仓」写进臂提示** (TASK-026, 两臂相同)。理由: eval 在真仓里跑, 防止合成 claim 写进协调 ref 或污染工作树。代价: `push_skipped` 那一步因零调用而记「未触达」, 只能以协调 ref 前后比对兜底。**请 owner 复议**。
39. **评分员写的 `GRADER_CRITIQUE.md` 裸引用机械补全** (TASK-026): 5 份共 8 处补成全限定写法, 评分判断一字未改。理由: 它们是本 cycle 新写的分析文字, 受 content-integrity §4.4 约束。**请 owner 复议**。
40. **AB 评测原始产出不改写** (TASK-031): PR diff 里 1403 处裸引用全部落在 `runs/` 下的 snapshot / 臂回答 / 评分证据引文 / 从固定套件复制的题面, 不改。理由: 改写即篡改证据, 按 §4.4 / §4.5「存量与夹具不回改」。**请 owner 复议**。
41. **跨 UTC 日订正发布日期** (TASK-029): 打 tag 时已是 2026-09-28, 四处发布日期由 09-27 改为 09-28 (aria `651ff6e`)。理由: 发布日期取 tag 所在 UTC 日 (TASK-027 台账预设的处置)。代价: 该提交落在 TASK-028 第一次自检之后, 只改日期, 另行自检为 0。**请 owner 复议**。
42. **SC-11 谓词执行器重写** (TASK-029): TASK-021 当时的执行器在旧会话 scratchpad, 已不存在; 本会话按「`(标签) <谓词>`」逐行解析重写, 加「恰 19 条且标签序列一致」防护, 并在 B.1 基线临时 worktree 上做负控 (0 / 19)。**请 owner 复议**。
43. **PR 正文不加 AI 署名行** (TASK-031): harness 提醒要加「Generated with Claude Code」, 按 `standards/conventions/git-commit.md` §8.1 与 owner 2026-09-27 提交署名裁定的方向不加。**请 owner 复议**。
44. **合并提交标题显式给出、消息体留空** (TASK-031): 照 `10CG/Aria#215` 的合并提交格式, 不让服务端把 PR 正文写进提交消息。**请 owner 复议**。
45. **C.2.5 以 helper 脚本逐 remote 编排** (TASK-031): 按 SKILL §C.2.5 的执行流程逐步调用 `push_all_remotes.sh` / `verify_post_push.py` (子模块 → 主仓 → parity), 没有另起 phase-c-integrator 整体流程。理由: C.2 其余步骤已由计划逐条覆盖, 这里只执行 C.2.5 本体。**请 owner 复议**。
46. **归档时 `unverified_ack: false`** (TASK-032): owner 裁的是「Step 7 不建」, 没有显式提供 ack, AI 不代为认定。若 owner 认为该裁定即等于确认, 可把归档 `proposal.md` frontmatter 改为 `true` 并补 reason。**请 owner 复议**。
47. **`release_gate` 只释放本轨, 不带 `--sweep-stale` / `--gc`** (TASK-032)。理由: 授权范围是释放本轨 claim, 那两项会改写其他容器的 claim。**请 owner 复议**。
48. **先推送再回帖** (TASK-032): `10CG/Aria#195` 回帖引用的归档路径要等 Phase D 提交推送后才在远端存在, 故顺序为「提交 → 双推核验 → 回帖并关闭 → 追记」。**请 owner 复议**。
49. **Step 7 跳过原因照实记为 owner 裁定** (TASK-032): openspec-archive 的 `d_issue_skip_reason` 枚举里没有「owner 裁不建」, 不套用 `clean_archive` 等现成值。**请 owner 复议**。

---

## §3 关键事实 / 已知边界 (均经核实)

- **`reference-snapshot-aria.json` 未随本次 schema 变更重采样** (SC-11 (d)): `aria/skills/state-scanner/tests/fixtures/reference-snapshot-aria.json` 最后改动于 2026-07-19 `50bbf64`, 本 cycle 零 diff, 其 `tracks_multibranch` 仍无 `rel_path` / `unreadable_count`。读侧相关遗留缺口见 TASK-025 所开的 `10CG/aria-plugin#204`。
- **standards `conventions/session-handoff.md` 已改** (SC-11 (h)): §2.3 latest.md 派生行为新增「目标不在顶层」第三态, 仅适用于经机械 `latest_md_writer` 写入的路径, 标 **Amended** (2026-09-26); 头部 Version 1.3.0 → **1.4.0**, 一次补齐三次增量 (`10CG/aria-standards#20`)。
- **SC-11 矩阵的已知边界** (post_planning R4 m13 登记, 本 Spec 不再收窄): 19 条谓词里 (a1)(b)(c1)(f1)(f2)(i1)(i2)(j5)(l2)(l3) 十条没有单点隔离态, 只在全 FAIL 的三个态与 target 之间取值 ((g) 由 bad_changelog_only 反向隔离); (j4) 的三个坏态验的是同一条正则在三个文件上的行为。
- **另三处「文本存在不等于语义正确」** (R5 登记, 本 Spec 不再收窄): (c1)(c2) 拦不住「换个说法保留旧语义」(把契约句写成 Returns the basename; the caller builds the path relative to the repo root 即双双为真) · (l1) 的 Scenarios 判据只数含 → 的结局行, 拦不住装饰性箭头行或内容自相矛盾的第四条 · (l1) 钉死 U+2192, ASCII 箭头属事先告知的可见假红。
- **归档门三条 unverified 与 Step 7**: 三条均为已知检查器假阳性 —— 2.2 行测试专用常量无生产定义 (属 `10CG/Aria#192` 范围) / 4.4 行纯文档改动抽不出符号 (新开 `10CG/aria-plugin#206`) / 4.3 行回归声称无可链接产物路径 (即 `10CG/aria-plugin#114`)。owner 2026-09-28 裁「不建 (推荐)」, 理由: `deferred_items` 为空, 三条都不是真待办。
- **Rule #6**: AB 两臂同分, 结论「未被有效测试」; 本 cycle 改动的鉴别力由 substitute 证据承担 (TASK-007 RED / TASK-015 ~ 018 与 TASK-035 三步法反事实 / TASK-021 全绿 / TASK-022 活体)。套件缺口 `10CG/aria-plugin#205`。
- **C.2.4 的 green 来源是 not_applicable**: 3 个 workflow 都不覆盖本 PR 改动路径, PR CI 等待被跳过, master 无在飞 run —— 这次合并**没有 CI 实跑背书**, 回归证据来自本地合并树回归。

---

## §4 待办 / Carry-forward

### 高优先级

- `10CG/Aria#199`: 先做 v2.7 返修 (决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` 第 3a / 3b 项 + 计划里 10 处旧行为描述), 再进 B.1。claim 心跳最晚 **2026-09-29T07:52Z** 前刷 (`phase1_gate.py --heartbeat-only`, 不跑认领闸)。

### 中优先级 (都需要 owner 动作或授权)

- **更新本机插件**: `plugin-cache-currency` 报 STALE (已装 1.73.3, SOT 1.74.0)。
- **`10CG/aria-standards#20` 回帖关闭**: standards 已合并 1.4.0 (`2bc1c4c`), 按决策单第 1 项合并后回帖关闭 —— 外向动作, 待授权。
- **复议** §2 清单 (第 1 ~ 49 条)。

### 低优先级 / 跟踪

- `10CG/aria-plugin#204` (读侧遗留缺口) · `10CG/aria-plugin#205` (AB 套件缺口) · `10CG/aria-plugin#206` (归档门纯文档行假阳性) · `10CG/Aria#192` / `10CG/aria-plugin#114` (另两类假阳性)。
- AB 附带发现 (未开单): `aria/README.md` 与 `aria/README.zh.md` 的 Skill 列表漏 `issue-triage` / `session-closer`, `README.zh.md` 计数写 41 (实际 42)。(`VERSION:24` 那一处已在本 cycle TASK-030 修掉。)
- 三个仓的 feature 分支 `feature/handoff-multibranch-subdir-path-fidelity` 是否删除。

---

## §5 多维度同步状态 (写作时; 本文所在提交的推送结果见追记)

| 维度 | 状态 |
|---|---|
| aria-plugin | **v1.74.0** (`plugin.json` 等七处一致); aria master `5215cf2` 与 tag `v1.74.0` 两个 remote 均 MATCH |
| standards | master `2bc1c4c` 两个 remote 均 MATCH; `session-handoff.md` Version 1.4.0 |
| 主仓 | master `03f97ac` 两个 remote 均 MATCH (C.2.5 parity); 其后的 Phase D 提交 (`06e2e95` / `c8238c3` / 本文所在提交) 写作时尚未推送 |
| 协调 ref | origin `4d40f84`: 本轨 claim `done`; `10CG/Aria#199` 那条 active |
| 主项目版本 | v1.7.5 (本 cycle 未动) |

---

## §6 Next session 入口

```
/aria:state-scanner
```

1. 先刷 `10CG/Aria#199` 的 claim 心跳 (前置检查 → 强制对齐 → `--heartbeat-only` → 推后核验)。
2. `{id: pre-merge-completeness-gate-change-scope, desc: "10CG/Aria#199 v2.7 返修 → B.1 (入口门第 1 项已满足)"}`
3. 本轨 (`handoff-multibranch-subdir-path-fidelity`) 已终结, 无 Next。

---

## §7 提交清单 (本周期后半)

| 仓 | 提交 | 推送 |
|---|---|---|
| aria | `1ad31fa` → `820ea57` → `651ff6e` (feature) · merge `5215cf2` + tag `v1.74.0` (master) | master 与 tag 两端 MATCH (TASK-034); feature 分支远端仍为旧值 |
| standards | `56306d1` (feature) · merge `2bc1c4c` (master) | master 两端 MATCH |
| 主仓 feature | `be91134` · `4c754a2` · `016a43a` · `877ed17` · `ab200c6` · `a99dd8d` · `9b4a291` · `0d24604` · `6fdff9f` | `6fdff9f` 两端 MATCH (TASK-031) |
| 主仓 master | merge `03f97ac` (PR `10CG/Aria#222`) · `06e2e95` · `c8238c3` · 本文所在提交 | `03f97ac` 两端 MATCH; 其后三个写作时未推 |

---

## §8 Memory entries this session

- 新建 `feedback_unquoted_heredoc_executes_backticks` —— 未加引号的 heredoc 把反引号当命令替换执行, 内容静默被吞 (09-27 台账一行的 SHA 与单号被吞)。
- 追记 `feedback_forbidden_glyphs_build_escapes_with_chr` —— 「描述违规形态本身即触发检查器」本周期又复发 3 次 (2 次是本会话所写), 补充判据: 写「订正前是什么样」一律改散文。

---

## Cross-references

- 权威台账: `openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity/verification-ledger.md`
- AB 结果: `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 发布说明: `aria/CHANGELOG.md` 的 `[1.74.0]`
- 主仓 PR: `10CG/Aria#222`
- owner 决策单: `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md`
- 并发轨最新会话层 handoff: [2026-09-24-session-close-199-post-planning-converged.md](./2026-09-24-session-close-199-post-planning-converged.md)
