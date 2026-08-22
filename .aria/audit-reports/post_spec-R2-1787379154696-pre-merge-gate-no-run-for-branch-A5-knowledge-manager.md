---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T10:30:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 3
minor_count: 2
---

## 摘要

R2 对 v2 (R1-fix) 做知识管理透镜复核: (1) 逐条核对归我席的 R1 簇 (#14/#15/#16/#17/#11) 是否真落地; (2) 条款间交叉一致性; (3) 新鲜眼睛。方法: 全部结论基于 `aria @ 400f0bc` 实读源码 (`pre_merge_gate.py` 逐行核对 SC-7 七落点行号 / `pre-merge-gate-empirical-traps.md` 全文 / `workflow-state-schema.md`/`SKILL.md` 引用区间)、实读 `docs/decisions/` 全目录找修正案先例、`forgejo GET` 实查 Aria#177 全文与 aria-plugin#126/#127/#152 现状、实读 `phase-d-closer`/`openspec-archive` 两份 SKILL.md 找机械路由。

结论: **归我席的 5 个 R1 簇里, 2 个真收敛 (#15/#17-A5-m1), 3 个方向对但落地打了折扣 (#14/#16/#17-A5-m2/#11 部分)** —— 共同形状: v2 都做了"正确方向的最小修补", 但没有对照项目自己的**既有先例**(DEC 修正案格式 / #177 逐点清单 / #127 既存 issue)做到位, 留下的缺口恰好是"下次同形状问题会不会再犯"这条线上的。0 Critical, 不阻断合并安全性; 3 Major 建议在 R3 前吸收。

## R1 处置核对

| 簇# (来源) | 状态 | 证据 |
|---|---|---|
| #14 (A5-M1: DEC-20260731-001 零引用/零修正) | **partial** | Cross-references 已加 `docs/decisions/DEC-20260731-001-...md` (本 spec 限缩其「wait」语义, 以修正案形式衔接); §5 加一行「文末 append-only 修正案」。方向正确 (原文不改 + 前向指针), 但落地方式弱于本项目已有的同类先例, 且未处理"读者若只读到『退役裁定』小节本身, 看不到指针"这个具体路径——见新 Finding [A5-R2-M1] |
| #15 (A5-M2: F3 未列入 traps §6) | **closed** | §5 traps 行明写「收录 F1 / F3 / F4(tasks 只列已领+全量历史⇒单调) / (b) 轴同形盲区 / F6」——F3 已在列, 与 R1 建议的因果链合并写法一致 |
| #16 (A5-M4: 版本同步面「5 文件」口径) | **partial** | aria 子模块侧已改「引用点」口径并点名 `marketplace.json` **`:3`/`:16`** 两处 (本席重新实读该文件, `:3`="1.66.3" `:16`="1.66.3", 属实, 与 #177 原指控一致); 但**主仓侧原样沿用「gitlink/VERSION/README badge/i18n」旧框架**, 未按 #177 原文逐点补齐 (#177 明确点名的两处漏项——「CLAUDE.md 自己」与「README 的 `Plugin Version:` 行 (非仅 badge)」——在 v2 里仍然缺席) ——见新 Finding [A5-R2-M2] |
| #17 / A5-m1 (kind 命名易混) | **closed** | §2.3 「`gate_error.kind` 二维消歧表 (R1 A5-m1, 写进 SKILL.md 枚举处)」已实际写入表格, 覆盖「分支存在×run 存在」两轴四象限 |
| #17 / A5-m2 (issue #152 归档收尾留言) | **partial** | §5 末行已加安排, 但表述本身有时态/归属缺口 (「立案时加」在 owner 裁定于立案后两天才发生的事实下站不住, 且全文未指名由谁在何时执行), 且该安排在 phase-d-closer 实际执行链路上无机械落点——见新 Finding [A5-R2-M3] |
| #11 (A4-M7+A5-M3: memory 断言与 AD-5 前提) | **partial** | §3.4 TASK-0 建立了「先活体验证, 按结果二选一改 memory」的正确骨架, 解决了 R1 指出的核心问题 (AD-5 建在未验前提上); 但两条分支对"修正后 memory 该留什么证据"要求不对称——见新 Finding [A5-R2-m2] (Minor, 结构问题已解, 残留精度问题) |

## 交叉一致性检查 (跨簇接缝)

逐一核对 §5 文档同步表的 14 行是否内部互斥或与 Design Decisions / Out of Scope 矛盾: 未发现新的条款间冲突 (SC-7 七落点行号、`SKILL.md:248-263`、`workflow-state-schema.md:110-131` 三处引用区间逐行核对与实际源码精确对应, 见下方"引用准确性复核"; TASK-0 的"前置"排序与 §2.2 remedies_available 表的 dispatch 分支之间不存在循环依赖——TASK-0 在 Phase B 实现前跑完, §2.2/§3.3 的实现按其结果二选一落地, 顺序已由"前置"二字锁定)。真正的接缝问题不在"两条款互相矛盾", 而在"多处** Phase D 时点的散文承诺**互相独立地都假设了一个并不存在的机械收口点"——即下方 [A5-R2-M3]。

## 引用准确性复核 (v2 新增引用, 逐条实核)

| 引用 | 结果 |
|---|---|
| F4「Aether CLI `internal/ci/status.go:45-47`」 | **准确**。实读 `/home/dev/Aether/aether-cli/internal/ci/status.go:45-47`,三行原文: `// Forgejo v11.0.6: /actions/tasks works, /actions/runs returns empty.` / `// The /actions/tasks endpoint returns {"workflow_runs": [...]} despite the name.` / `endpoint := fmt.Sprintf("/repos/%s/actions/tasks", repo)`。该行只支持 F4 的"查询哪个端点"部分, F4 的"只列已领+全量历史无截断"部分由同行标注的另两个出处 (2026-08-20 handoff + R1 A1 三仓实测) 承载——复合引用, 非误引 |
| SC-7 七落点行号 | **全部精确匹配** `pre_merge_gate.py`@400f0bc: `:418`(`if not cfg["enabled"]:`) `:362`(`if no_ci_fallback == "abort":`) `:376`(skip_with_warning 分支 `return`) `:434`(`if not ok:`) `:455`/`:458`(main 核验两 kind 分支锚点) `:489`/`:512`(两处 `except AetherQueryError as exc:`)。并独立验证"七键 vs 六键": `_build_output` 基础 6 键 (`verdict/pr_ci_status/in_flight_runs/primitive_used/primitive_version_sha/raw_message`) + 仅 main 核验 fail 分支携带 `gate_error` = 7 键, 其余六处确为 6 键——v1→v2 的措辞订正准确 |
| `SKILL.md:248-263` | **准确**。`:248`=步骤 2.2 (main 分支存在性核验), `:252`=步骤 4, `:253-259`=步骤 5, `:260-263`=步骤 6, 区间边界与拟议改动逐一对应 |
| `workflow-state-schema.md:110-131` | **准确**。`:110`=`gate_state` 小节标题, `:116-125`=字段表 (含待改的 `raw_message` 行), `:127`=Defensive access, `:129-131`=Lifecycle 前三条——拟改内容完整落在区间内 |
| R1 聚合报告路径 | **准确**, 文件存在且内容与本次核对一致 |
| rule6_note「NEG-3 `_description` 逐字就是…」 | **不准确, 但影响极小**: 实读 `NEG-3-internal-error-surface.json` 的 `_description` 字段原文是"既有 6 个 fixture (green/wait/wait_then_green/fail/NEG-1/NEG-2) 结构上都碰不到 path_coverage 的 unknown 分支, 更碰不到 D9 surface 的 reason 分档措辞"——是**释义**不是**逐字**引用。用词"逐字" (verbatim) 与实际(paraphrase) 不符, 建议改「同型先例」或直接引原句。未单独开 finding (不影响判断, 仅措辞精度), 但因 R2 明确要求"引用准确性复核"故如实记录 |

## 新 Findings

### [A5-R2-M1] Major — DEC-20260731-001 修正案的落地方式弱于项目自身先例, 未覆盖"读者停在退役裁定小节本身"的路径

**锚点**: proposal.md §5 表 `docs/decisions/DEC-20260731-001-c24-wait-adjudication-retirement.md` 行 ("文末 | append-only 修正案:…原文不改…"); 对照 `docs/decisions/` 目录内已有三个修正案先例。

**问题**: 本项目对"决策存档类文档需要事后修正"这件事已经沉淀了具体、可复制的格式先例, 且该先例明确包含两个 v2 未覆盖的要素:

1. **`standards/conventions/version-management.md:174`**: `> 🔴 **2026-08-16 更正: aria 插件不属于本类** (owner 裁定, 选项 C)。` —— 更正是一个**带日期、带🔴视觉标记、带裁定来源的独立区块**, 不是"在文末追加一段无格式标记的散文"。
2. **`DEC-20260812-001:80`**: `> ## 🔴 更正 (2026-08-12, A 侧 post_spec R1 — 四席独立命中)` —— 同样是日期化的标题级更正区块, 且是**在被更正内容紧邻之后**插入 (不是移到文档最后)。
3. **`DEC-20260704-003-archive-gate-completion-vs-runtime-reality.md`**: 用 `## Amendment 1 (2026-07-04, post_spec R1 触发)` 收纳完整更正内容, 但**同时**在原文每一处被超越的段落旁插入 `📌` 就地指针 (如 `:22`「当前以 §Amendment 1 为准」、`:35`「历史保留, 当前架构以 …§Amendment 1 为准」、`:62`「读到此处务必续读文末 §Amendment 1」——四处, 非一处)。
4. **`DEC-20260702-001:128`** 把这条约定写得更直白: 「上文三处 amend 字面表述保留原样 (历史决策记录不回改), **本节仅作前向指针**」——即"末尾放修正内容"与"原地放指针"是**两件都要做的事**, 不是二选一。

v2 §5 只安排了"文末追加一段无日期无标记的 append-only 修正案"这一半, 缺:

- 日期化 + 视觉标记的独立区块格式 (而非融入表格单元格的一句话散文);
- **就地指针**: `DEC-20260731-001` 的问题断言不在文档末尾, 而在中段 `## 退役裁定 (2026-07-31)` 小节的第二个项目符号——「此后 `verdict=wait` 真正意味着『CI 在跑或该跑没跑完』, 按 workflow-runner wait 正常处理。」这正是被 issue #152 与本 spec 证伪的那句话。若修正只写在文末, 一个从头读到 `## 退役裁定` 就停下 (该小节恰好是全文信息密度最高、最像"结论"的一段) 的读者, 读到的仍是这句未加限定的定案语气断言, 直到读完整篇才会 (也可能不会) 翻到文末的修正——这正是 R1 A5-M1 原始 finding 想防止的场景("误诊会重蹈覆辙"), 而 v2 的落地方式没有堵住这条具体路径。

**按 spec 实施会怎样错**: v1.66.4 ship 后, `DEC-20260731-001` 文末多了一句正确的修正, 但 `## 退役裁定` 小节本身字面未变。未来任何人 (含 AI) 在别处 (例如被 grep `verdict=wait` 命中、或被别的文档交叉引用直接跳转到这一小节) 读到该小节, 依然会看到无限定的"wait 真正意味着 CI 在跑或该跑没跑完", 且没有本地信号提示"这句话已被修正, 请翻到文末"——与 R1 finding 描述的风险完全同构, 只是把"零处理"改成了"处理了一半"。

**建议**: (1) 把 §5 该行的落地格式改为项目自有先例的标题级区块 (`> ## 🔴 更正 (日期, 触发来源)` 或 `## Amendment 1 (日期, 触发)`), 而非融入表格单元格的一句话; (2) 在 `## 退役裁定` 小节被引用的那个项目符号后面加一句 📌 就地指针 (「⚠️ 本条已被 aria-plugin#152 / spec `pre-merge-gate-no-run-for-branch` 限缩, 见文末更正」), 而不仅仅是"文末"。两处都是几行文字量级的改动。

---

### [A5-R2-M2] Major — 版本同步面主仓侧仍未按 Aria#177 逐点对齐: 漏「CLAUDE.md 自己」与「README 的 `Plugin Version:` 行」, 恰是 #177 点名的两个具体坑

**锚点**: proposal.md §5 表最后一段 `aria/CHANGELOG.md + 版本引用点` 行:「…同步面按**引用点**口径 (非文件数, Aria#177): `plugin.json` / `marketplace.json` `:3` 与 `:16` 两处 / `VERSION` / `CHANGELOG` / `README` + **主仓 gitlink / VERSION / README badge / i18n** (仅正文实质变更才重译)」; 对照 `forgejo GET /repos/10CG/Aria/issues/177` 全文实读。

**问题**: Aria#177 是本项目对"版本同步面漏项"这一类问题开的、**尚未 close** 的治理 issue, 标题逐字点名「四错一行」, 第一条错是「按文件数枚举而非引用点数」, 但另外明确列了两条**主仓侧**具体漏项 (原文):

> 「2. **漏 `CLAUDE.md` 自己** —— `CLAUDE.md:139`(版本区间) + `:141`(「版本:」行) 各含版本号。自指盲区 —— 规定同步面的那份文件没把自己列进去, 且无任何 custom check 兜它」
> 「3. **「root README badge」漏 `Plugin Version:` 行** —— `README.md:8` 是 badge, `:242` 是 `Plugin Version:   1.65.5 (aria-plugin, 42 Skills + 11 Agents)` —— 两处都得改, 只写了 badge」

v2 §5 对 aria 子模块侧确实按"引用点"口径重写并点名了 `marketplace.json` 的两个具体字段 (`:3`/`:16`, 本席复核属实, 呼应 #177"aria 子模块侧同样是文件数口径"那段) —— **这部分吸收到位**。但对**主仓侧**, v2 只是原样保留 CLAUDE.md 现有的「gitlink / VERSION / README badge / i18n」四项框架, 一字未改, 而这四项里:

- **没有"CLAUDE.md 自己"** —— 而这份正在写"版本同步面"这句话的文件, 自己的 `:139`/`:141` (在本 session 打开的 CLAUDE.md 里对应「项目状态」段「版本: 插件 aria-plugin v1.66.3 | 主项目 v1.7.3 | …」一行) 同样含 aria-plugin 版本号, 本 spec 一旦 ship v1.66.4, 这一行也需要同步改, 但 §5 没提;
- **"README badge" 仍是旧措辞** —— 未按 #177 明确指出的"还得改 `Plugin Version:` 行 (`:242`)"补全, 只字面写"badge"。

**按 spec 实施会怎样错**: 执行本 spec 的版本 bump 步骤时 (Phase C/D), 若操作者按 §5 字面逐项过一遍, 会漏改 `CLAUDE.md` 自身的版本行与 `README.md:242` 的 `Plugin Version:` 行——这恰好是 #177 描述的"三次复发, 每次只修当次实例"模式里的**第四次**: #177 本身是在另一个 Spec (`linked-issue-normalization`) 里发现并开的治理 issue, 尚未 close, 而本 spec (`pre-merge-gate-no-run-for-branch`) 是 #177 开立后第一个真正要执行版本 bump 的 Spec, 却在采纳了 #177 一半观点 (子模块侧引用点口径) 的同时, 未把另一半 (主仓侧漏项清单) 落到自己的执行步骤里——若不补, 会在 #177 issue 仍 open 的情况下, 用实际行动重新验证一遍它描述的问题。

**建议**: §5 该行主仓侧部分改写为「`CLAUDE.md` 自身版本引用行 (`:139`/`:141`, 本 SHA 对应内容以本 session 实读为准) / `README.md` badge (`:8`) **与 `Plugin Version:` 行 (`:242`)** / gitlink / i18n 三语 README 同样含 badge+`Plugin Version:` 行 (仅正文实质变更才重译)」, 并在 Cross-references 挂 `Aria#177` 明说"本 spec 版本 bump 步骤同时采纳 #177 对主仓侧的逐点清单, 不止子模块侧"。

---

### [A5-R2-M3] Major — 三处"Phase D 待办" (issue #152 收尾留言 / (b) 轴另案 issue / rule6_note 套件缺口 issue) 全部是纯散文承诺, 在 `phase-d-closer`/`openspec-archive` 的实际执行链路上没有任何机械路由点, 且部分 WHO/WHEN 表述本身有缺口

**锚点**: proposal.md §5 最后一行 (issue #152); §1 与 Out of Scope 的 (b) 轴「Phase D 立案 aria-plugin issue」; rule6_note 第一段「套件缺口 issue」; 对照实读 `aria/skills/phase-d-closer/SKILL.md` 全文 + `aria/skills/openspec-archive/SKILL.md` Step 7 全文。

**问题**: 本 spec 是 Level 2 (仅 `proposal.md`, 无 `tasks.md`), 这意味着它没有一份会被 Phase B/C/D 机械读取、逐项打勾的任务清单——三处"以后再做"的安排, 唯一的载体就是 proposal.md 里的散文:

1. **issue #152 评论**:「立案时加 owner 裁定 + spec 链接; Phase D 关闭时留收尾留言」。「立案时」在时态上站不住——issue #152 已于 2026-08-20 立案, owner 裁定发生在 2026-08-22 (本 spec 起草 session), **晚于**立案两天, "立案时加"字面读起来像是在描述一件已经发生的事, 但本席实查 `forgejo GET .../issues/152/comments` 当前**仍是 0 条评论**——这件事并未发生, 措辞的时态错位有实际后果: 一个只扫读表格的执行者容易把"立案时"读成"已完成, 无需我做", 而不是一个还要主动执行的动作项。全文也没有指名由谁 (哪个 Phase/哪个 Skill 调用) 执行这条评论。
2. **(b) 轴另案 issue**:「Phase D 立案 aria-plugin issue『Rule #8 (b) 腿对未被领取 run 不可见』」——WHEN 有 ("Phase D"), 但 WHO 没有 (是 phase-d-closer 自动做? 还是执行者手动做?), 且 Out of Scope 段的复述比 §1 更弱, 只写"另案 issue", 连"Phase D"都被省略, 读者若只看 Out of Scope 一节甚至连时点都看不到。
3. **rule6_note 套件缺口 issue**:「追加到 NEG-3 当时开的缺口 issue, 若无则新开」——WHEN 完全没写 (§1/(b)轴那两条好歹还写了"Phase D", 这条连阶段都没有), WHO 也没有。(此条与 A3-R2-M1 的发现有实质重叠——A3 席已独立查证 NEG-3 当时开的缺口 issue 就是 aria-plugin#127 (open, 标题与内容逐字对应), 本席复核该查证结果准确, 不再重复取证; 本 finding 在此条上不再展开, 仅计入"三处均无 WHO/WHEN"这一类级观察。)

更根本的问题: 本席逐字读了 `phase-d-closer/SKILL.md` 的 D.1→D.2→D.2b→D.3 全部步骤, 以及它委托的 `openspec-archive/SKILL.md` Step 7「D auto-issue」——**该机制真实存在, 但管的是完全不同的一件事**: 它扫描 `detailed-tasks.yaml` 的非-done 项与 C 分级证据闸的 `unverified_claims`, 与 Spec 正文散文里"另案开 issue"/"issue 里留言"这类自由文本承诺**零关联**(`grep -n "另案\|后续 issue\|开.*issue" phase-d-closer/SKILL.md` 零命中)。也就是说, 这三处安排全部符合本项目自己已经反复点名的反模式「有记录无路由」(memory `feedback_fix_recurs_in_its_own_fallback_path` 同形)——写在文档里, 但没有任何执行路径会真的读到并执行它们, 完全依赖 Phase D 的执行者 (人或 AI) 恰好记得回头翻这份已经进入 `openspec/archive/` 的 proposal.md。

**按 spec 实施会怎样错**: Phase D 收尾走完 D.1(进度更新)→D.2(归档, 委托 openspec-archive 处理它自己的 deferred/unverified 机制)→D.2b(claim 释放)→D.3(session handoff) 这条固定流水线后, 三件"额外该做的事"没有任何一步会被自动触发去做; 若执行者当时正专注在 D.2/D.3 的机械检查上 (它们本身分支就多、有 tri-state verdict 等复杂度), 大概率会漏掉这三条纯靠记忆执行的散文承诺, 且不会有任何绿/红信号提示"这件事本该做但没做"。

**建议**: (1) 把 issue #152 的时态改为明确的"待办"语气 (如「本 session 内 (Phase A 阶段) 即应补一条评论……」), 并指名执行者 (如"由起草本 spec 的 session/AI 直接执行, 不依赖 Phase D"); (2) (b) 轴 issue 与 rule6_note issue 统一改写为"Phase D 收尾时, 由执行 D.3 session handoff 的同一个人/session 顺手创建", 并在 §5 表格里像"issue #152"那行一样, 各给一个独立的表格行 (当前只有 (b) 轴那条能在正文里搜到"Phase D"字样, 另两条要靠上下文推断); (3) 若认为这类"spec 内散文承诺 Phase D 执行"的模式本身值得机械化 (例如 phase-d-closer 增加一步「扫描待归档 proposal.md 的 Out of Scope / 文档同步面表格找`issue`/`Phase D`关键词做清单展示」), 该建议本身可考虑另开 issue, 不必阻塞本 spec。

---

### [A5-R2-m1] Minor — traps §6 拟收录的 F1 条目本身可仅凭读代码得到, 与 traps 文件头「没有一条能靠读代码想出来」的自我主张不完全相符

**锚点**: proposal.md §5「新 §六」拟收录清单第一项 F1 (`aether.py:225-226` 那一行 `if not runs: return "pending"`); 对照 `pre-merge-gate-empirical-traps.md` 文件头逐字声明「半页。**每一条都是实测踩出来的, 没有一条能靠读代码想出来。**」。

**问题**: F1 的内容——"backend 把『零 run』与『run 未完』同映射为 `pending`"——是打开 `aether.py:225-226` 单行代码即可直接看到的事实, 不需要任何实测/运营历史/API 探针才能发现, 与既有五条 (ls-remote 三个反直觉行为 / Unicode 解码坑 / 位置坑 / 测试隔离坑 / #137 根本形状) 的性质不同——那五条 (以及本次新收录的 F3/F4/F6) 都需要**实际踩坑或主动做实验**才能获知 (PR 历史查询 / API 全量计数对比 / 端点探测)。若逐字执行 v2 §5 的收录清单, 会在收录判据自称"每一条"都满足某性质的同一份文件里, 塞进一条不满足该性质的条目, 使文件头的自我描述出现字面上的例外。

**按 spec 实施会怎样错**: 影响很小 (traps 文件仍然对未来排查者有用, F1 本身也确实是"这个 bug 的根因在哪一行"这个问题的正确答案), 但会让"每一条都不能靠读代码想出来"这句判据本身变得不完全可信——下次有人想往这份文件加一条边界情况不那么清楚的"事实"时, 无法再用这句判据做筛选依据 (先例已经破了)。

**建议**: 二选一——(a) 把 F1 从"traps 清单"移到已有的第五节「这道 gate 的根本形状」(该节本身就是"为什么会有 #137"这类根因解释, 已经容纳了同样可以纯读代码得出的 `#137` 根因描述, 是更贴切的落点, 且新六节可与其呼应); 或 (b) 保留在第六节但改写措辞, 强调"这一行本身好找, 难的是**在 2026-08-19/20 那次事故里, 从『恒 wait』的症状反推到就是这一行**"这个调查过程本身, 而不是把它写成一个孤立的代码事实。

---

### [A5-R2-m2] Minor — TASK-0 两分支对"修正后的 memory 应留什么证据"要求不对称

**锚点**: proposal.md §3.4「成功 → …修正 memory `reference_forgejo_new_branch_paths_filter_no_run` (『不可用』→『可用, 按文件名寻址』)」 vs 「失败 → …memory 保留并补 HTTP 码证据」。

**问题**: 失败分支明确要求"补 HTTP 码证据"这个可验证的具体产物, 成功分支只说"改断言"三个字, 没有同等要求写入可验证证据 (如实际观测到的 HTTP 码 / 建 run 的 Δt / dispatch 后 run 是否出现)。R1 A5-M3/A4-M7 这一簇的根本问题正是"该 memory 现在的『不可用』断言是无证据的裸断言, 容易被当作事实直接采信"——若成功分支的修正同样写成一句无证据的裸断言"可用", 只是把错误方向的裸断言换成正确方向的裸断言, 结构性风险 (下一个读到这条 memory 的人无法自行判断可信度、也无法在环境变化后知道该不该重新验证) 并未消除, 只是这次凑巧改对了。

**按 spec 实施会怎样错**: 如果 TASK-0 成功但执行者图省事, memory 最终文本可能变成"`workflow_dispatch` API 在 gitea-1.22 系可用, 按文件名寻址"这样一句同样无日期无证据的断言, 未来再有人 (或另一个 aria-plugin 版本的 Forgejo 升级后) 需要重新确认这件事时, 无法判断这条 memory 的"保鲜期", 与本 spec 起草期发现的原问题 (裸断言被直接采信、混淆了 list 端点 404 与 dispatch 端点 400 两件事) 是同一形状的复发风险, 只是暂时方向对了。

**建议**: 成功分支的措辞后面加一句与失败分支对称的要求, 例如:「…(『不可用』→『可用, 按文件名寻址; 证据: <日期> TASK-0 throwaway 分支实测, HTTP <码>, run 出现 Δt=<秒>, 见 spec pre-merge-gate-no-run-for-branch』), 并保留原文里对『GET 列表端点 404』与『POST dispatch 端点非 404』两者区分的说明不动」。

## Verdict

**verdict**: PASS_WITH_WARNINGS (0 Critical / 3 Major / 2 Minor)
**vote**: REVISE

归我席的 5 个 R1 簇中 2 个真正收敛 (#15 traps F3 纳入、#17-A5-m1 kind 消歧表), 其余 3 个 (#14 DEC 修正案、#16 版本同步引用点、#17-A5-m2 issue 收尾) 都是"方向对、落地打折扣"——且三者共同指向同一类风险: **v2 在采纳 R1 建议时, 倾向于做"最小语言学修补"而非对照项目自己已经沉淀的先例 (DEC 修正案格式 / #177 逐点清单 / 已存在的 #127) 做到位**, 这与本项目其他四席在 R2 各自发现的问题 (A2 的"至多一次升级"同形姊妹坑、A3 的 NEG-4 孤儿 fixture) 是同一类"R1-fix 在自己的新条款里重犯同形状缺陷"的模式。3 条 Major 均可在不推翻设计的前提下于 R3 前吸收 (加几行文字/挪一个位置/补一句证据要求), 不建议进入 R3 前把方案打回重来。
