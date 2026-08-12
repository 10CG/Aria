---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T16:20:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — knowledge-manager 席位报告

**被审对象**: `openspec/changes/premerge-gate-branch-existence/proposal.md` (Spec A, Level 2), R1-fix 后 (commit `e165df4`)
**审视角度**: Rule #5/#6/#9/#10 合规 · Level 2 判据 · 非目标与 B 侧划界一致 · follow-up 可证伪
**投票**: REVISE · **verdict**: PASS_WITH_WARNINGS (0 Critical + 1 Major + 3 minor)

---

## 0. 先说结论

R1 的两条 Critical (Rule #6 定档错误 / 划界承重句「存在性核验单独就关掉恒绿腿」在执行路径层不成立) **都是真闭合, 不是「写下来」**——逐条回源见 §1。R1-fix 附带的三条自我更正 (SOT 行号引错 / aggregate 归属错 / 未去重) 与两条新发现 (`UnicodeDecodeError` 非 `OSError` 子类 / SC-A11 空真) 我逐条独立复核, **全部属实**。本轮我新发现 1 条 Major + 3 条 minor, 均是本轮独立浮出、非 R1 的 finding 搬运。**Major 落在「C-2 虽已在文档内自洽闭合, 但闭合物本身的可发现性弱」这个二阶问题上, 不是重新打开 C-2。**

---

## 1. R1 两条 Critical 是否真闭合 (逐条回源)

### C-1 (Rule #6 定档): **真闭合**

R1 的问题是: A 判第一行 (substitute) 但提名的 SC-A6/A13/A-zero 对它要替代的 `SKILL.md` 两处 hunk 恒绿, 不满足 baseline-failing。R1-fix 没有"修补"这个恒绿的 substitute, 而是**整体改判第二行** (照跑 AB), 使"这个 substitute 不满足 baseline-failing"这个问题**结构性消失** —— 因为不再有 substitute 需要满足这个要求。

我独立核对了三条依据:
- 实读 `standards/conventions/skill-benchmark-exemption.md` (`Read` 工具, 逐行编号): **substitute 定义在 `:28`, "拿不准照跑" 在 `:31`, SKILL.md 专属附加约束在 `:33`** —— 与proposal.md现文 `:334/:341/:343` 的引用**逐行核对全部命中**。这本身修正了 R1 aggregate 的引用错误 (aggregate `:67`/`:76` 分别误引 `:26`/`:33` 代指两处不同文本, 其中 `:33` 那处连引的文本对象都错了)。
- `rule6_note` (proposal.md:329) 现文 = 「第二行 —— 照跑 AB, 零裁量。本 Spec 不申请任何豁免」, 全文 `grep "豁免\|substitute"` 复核: 所有 "substitute" 字样均出现在 (a) 历史更正语境 (「上一版」) 或 (b) 明确否定语境 (「SC-A-doc 确实 baseline-failing 但本 Spec 不拿它当 substitute」), **无一处残留矛盾**。
- 我独立读了 `aria/skills/phase-c-integrator/SKILL.md:238-280` 确认: `§C.2.4 执行流程` 是**编号步骤本体** (1/2/2.5/3/4/5/6), `2.5` 正是 v1.65.0 为同形改动新增的步骤, 与 A 现在计划新增的 `2.2` 同构 —— A 的"改判第二行"依据 (a) 站得住。

**结论**: C-1 真闭合。

### C-2 (划界承重句 / 残余暴露): **真闭合**

R1 的问题是: DEC §3 与 A §Why 的承重句「存在性核验单独就关掉恒绿腿」只引了 B 侧 §症状, 漏引 §根因, 导致该句在 AI 实际执行的 `SKILL.md` 散文路径上不成立 (`:243` 硬编码 `main`, 本仓 `origin` 无 `main` 分支, `ls-remote` 返 RC=0 零行)。

R1-fix 的处理: 不是让承重句变成"真"(那结构上做不到, A 明确声明不碰 `SKILL.md:243`/`:167` 既有裸命令), 而是 (1) 给承重句加限定「`gate_check()` 这份实现里的」, (2) 新增 `### 根因` 段逐字补引, (3) 新增整节 `### ⚠️ 残余暴露`, 内含逐字声明「A ship 不构成 #137 闭环, 不得据 A ship 关闭 #137」+ 三条实测支撑 + 残余的精确形态描述。

我独立验证:
- `git ls-remote --heads origin main` 本仓与 `aria` 子模块**均**复现零行 + RC=0 (与文中 `:31-33` 声称一致)。
- 全文 `grep "#137"` 只有 4 处 (`:13/:73/:76/:391`), **无一处**与「A ship 不构成 #137 闭环」矛盾 —— 即不存在"一处说已闭环、一处说未闭环"的自相矛盾残留。
- B 侧姊妹 Spec `premerge-gate-mainbranch-failclosed` 的抬头**同步**带了对应更正 (「A 承接的是关掉 `gate_check()` 那份实现里的恒绿腿」), 与 A 现文口径一致, 未出现"A 说已限定、B 还在说 A 拿走了全部"的两侧漂移。

这不是把 R1 指出的缺陷"修没了", 而是把一个**结构上 A 确实做不到的事** (让散文路径也变安全, 那是 B 侧 D1 的工作) 转化为**显式的、可读的、无矛盾的边界声明**, 并把闭环判据正确地挂到了 B 侧 D1。这是这类"结构性残余"缺陷唯一诚实的关闭方式。

**结论**: C-2 真闭合。**但**闭合物本身的可发现性/耐久性有缺口, 见下 Major-1。

---

## 2. R1-fix 的三条自我更正 + 两条新发现: 逐条独立复核

我不复用 R1-fix 执笔方给出的结论, 全部重新独立取证:

| 声称 | 我的独立复核方法 | 结论 |
|---|---|---|
| SOT 行号引错 (substitute 定义在 `:28` 非 `:26`;「拿不准」在 `:31` 非 `:33`) | `Read` 全文, 逐行核对 | ✅ **属实**, 且我自己 R1 报告 (`post_spec-R1-4-...-knowledge-manager.md:72`) 也引了错误的 `:26`/`:33` —— 这个错误在我自己的原始 finding 里就存在, R1-fix 是唯一独立核对了 SOT 实际行号的一方 |
| aggregate 归属错 (「行为兼容面未评估」+「`:6`/`:229`自我推翻」出自 tech-lead 的 `additive_claim` 字段, aggregate 记成 backend-architect) | 读 `journal.jsonl` 五席 `result.additive_claim` 字段原文 | ✅ **属实**——backend-architect 的 `additive_claim`/`findings` 全文均无「行为兼容面」字样; tech-lead 的 `additive_claim` 逐字含「(a) 行为兼容面未评估…(b) `:6`…被`:229`自我推翻」 |
| 未去重 (6C 里 4 条指向同一件事, 去重后约 2C+10M) | 逐份读 5 份 R1 seat 报告的 Critical 项, 按"指向同一底层事实"分组 | ✅ **属实** —— 6 个 Critical 可归两组: (i) Rule #6 substitute 恒绿: tech-lead C-1 + knowledge-manager C-1 + qa-engineer C-2, 共 3 条; (ii) 划界承重句/残余暴露不成立: backend-architect Finding1 + knowledge-manager C-2 + qa-engineer C-1, 共 3 条。两组共 6 条收敛为 2 条独立事实, 与「约 2C」吻合 |
| `UnicodeDecodeError` 不是 `OSError` 子类 | 独立实跑 `python3 -c "print(issubclass(UnicodeDecodeError, OSError)); print(UnicodeDecodeError.__mro__)"` | ✅ **属实**, 输出 `False`, MRO = `UnicodeDecodeError→UnicodeError→ValueError→Exception→BaseException→object`。且我核实 `path_coverage.py:78-102` 确已用 `capture_output=True` + `.decode("utf-8", errors="surrogateescape")` 规避了这个坑 (未用 `text=True`) —— A §5 钉死"照抄 `path_coverage.py` 的私有 runner 形状"这条处方是可执行的, 不是空话 |
| SC-A11 若打桩核验入口会退化为恒真 (5 席全漏) | `git show e165df4` diff 核对 SC-A11 改动前后文本 + 逐份检索 5 份 R1 报告的 SC-A11 相关文字 | ✅ **属实** —— 改动前 SC-A11 只写「负控: 分支存在且有 in-flight → verdict=wait 不变」, 未限定"分支存在"必须来自真实裸仓而非对核验函数本身的 mock; 5 份 R1 报告中仅 code-reviewer `:356` 提到「需真实 fixture 或 mock, 未列」但未点出"若 mock 的是核验入口本身则退化为恒真"这一具体机制, 其余 4 席零提及 |

**这五条核对结果全部支持 R1-fix 执笔方的自陈**——包括其中一条指出了我自己 R1 报告的错误。这提高了我对本轮其余声称的信任度, 但不改变我仍需独立验证 (而非采信) 的纪律。

---

## 3. 本轮新发现 (均为本轮独立浮出, 非 R1 finding 搬运)

### Major-1: 「A ship 不构成 #137 闭环」的约束只落在会被归档的 Spec 文件内, 无外部/机械留痕, 耐久性弱

**locator**: `proposal.md:73-94` (§残余暴露) × `proposal.md:391` (§Impact「外部」行)

**evidence**:
1. `proposal.md:391` 逐字: 「外部 | **无外部动作** —— 不改 #137 body, 不发评论。留痕与否由 owner 决定。⚠️ **不得据 A ship 关闭 #137** (§残余暴露)」。即整份"A 不等于 #137 已解决"的约束, **唯一**的落点是这份 Level 2 proposal.md 自身。
2. Level 2 = proposal only, 无 `tasks.md`; Phase D.2 (`openspec-archive` skill) 会把这份文件移入 `archive/`。移入 archive 后, 它不再出现在 `openspec/changes/` 的活跃列表里。
3. `aria-plugin #137` issue 本身 (我未能直接访问外部 Forgejo 核实当前内容, 只能从本仓引用推断) 在 A ship 时**不会**收到任何指向这份残余暴露声明的评论或标签 —— 按 `:391` 逐字, 这是刻意的("留痕与否由 owner 决定"是显式、合规的 Rule #10 式留白, 不是疏漏)。
4. `CLAUDE.md` "两层 AI 分工" 段落写明 Layer 1 主管「只加载 ~1K token 元知识, **不加载** aria-plugin」(AD7) —— Layer 1 在判断"#137 是否可以关闭"这类问题时, 结构上不太可能主动去读一份埋在 (未来会被归档的) Level 2 proposal.md 里的 §残余暴露 小节。

**why not re-opening C-2**: C-2 的原始缺陷是"承重句在文档内部自相矛盾/失实"——这已被逐字纠正且全文一致 (§1 已验)。本条谈的是一个**不同维度**的风险: 声明本身准确、自洽, 但**分发路径薄弱**, 一旦离开这份文档的阅读语境就失效。这是 R1 三选一处置建议 (backend-architect 「(a)/(b)/(c)」) 里 (b) 的一个未被充分意识到的副作用——选 (b) 时隐含假设"未来做决策的人会读这份文档", 但 A 自己在 §Impact 「外部无动作」处主动放弃了任何强化这个假设的机会。

**how_it_goes_red**: B 侧头部已声明「本侧当前不具备进 Phase B 的条件」—— D1 落地时点未定。若干个月后 owner/Layer 1 依据「A 已 merge / git log 有 `--main-branch` 相关改动」这类间接信号判断 #137 已经解决并将其关闭 (且过程中未主动翻出这份特定的 Level 2 proposal.md), #137 会被误判闭环——这正是 R1 两条 Critical (backend-architect Finding1 / knowledge-manager C-2) 试图防止的确切场景, 而目前唯一的防线是"读者会主动打开这份文档"。

**blocks_phase_b**: false (不阻塞 A.2 起步; 建议 A.2 或 D.2 前补一句机械化的提醒, 例如「D.2 归档 A 时, 若 #137 仍 open, 须在 archive 提交信息或 handoff 里逐字复述这条残余暴露, 不能随 D.2 静默带走」)

**introduced_by_r1fix**: true (`§残余暴露`整节与`§Impact`「外部」行均为 R1-fix 新增内容; R1 之前的版本根本没有这条约束, 无从谈"分发弱")

---

### minor-1: 「八轮 40 席」与 `audit-reports` 实际记录不符 (少算一整轮)

**locator**: `proposal.md:17-18`, `:122`, `:449` (三处均写「八轮 40 席」)

**evidence**: 实跑 `ls .aria/audit-reports/ | grep "mainbranch-failclosed" | sed -E 's/^(post_[a-z]+-R[0-9]+)-.*/\1/' | sort -u`, 结果为 `post_planning-R1..R4` (4 轮) + `post_spec-R1..R5` (5 轮) = **9 轮**; 逐轮 `grep "^${r}-" | grep -v aggregate | wc -l` 确认每轮**5 个席位文件** (tech-lead/backend-architect/qa-engineer/code-reviewer/knowledge-manager) ⇒ **45 席**, 非 40 席。B 侧姊妹 Spec 自己的 Status header 也写「post_spec 跑满 R1–R5, **25 个 agent-run**」(= 5 轮 × 5 席), 与「八轮」矛盾 (若只算 post_spec 就该是 5 轮 25 席, 加 post_planning 4 轮 20 席才是 9 轮 45 席; 无论哪种切法都凑不出「8 轮 40 席」)。

**溯源**: 该数字来自 `DEC-20260812-001-premerge-gate-spec-split.md:114`「SC-M6/…已经过八轮 40 席打磨」, A 直接承袭, 不是 R1-fix 本轮引入的新错误。

**how_it_goes_red**: 该数字目前只用于修辞强调 (「这条底层事实八轮 40 席都没浮出」), 未被用作任何机械判据的输入或计数校验的基准 ⇒ 即使数字修正为「九轮 45 席」, 结论方向不变 (审计覆盖更多、遗漏依然存在, 反而**加强**而非削弱原论点) ⇒ 不影响任何决策, 判 minor。

**introduced_by_r1fix**: false (承自 DEC, DEC 早于 A 的 R1)

---

### minor-2: `docs/handoff/latest.md` 未反映 DEC-20260812-001 拆分, 仍显示拆分前的单一 track

**locator**: `docs/handoff/latest.md:3,12` (mtime 2026-08-11 01:26, 早于 DEC 的 2026-08-12)

**evidence**: `Read` 确认该文件当前 `Latest` 指针与 track 表仍只有一行 `premerge-gate-mainbranch-failclosed | ... | A.2-audit (blocked) | 2026-08-11`, **没有** Spec A (`premerge-gate-branch-existence`) 的 track 条目, 也没有反映 B 侧当前的新 phase (「不具备进 Phase B 条件」)。DEC 创建于 2026-08-12, proposal.md (A) 现已进入 post_spec R2, 但这份跨会话状态文件停留在拆分前一天的快照。

**为什么与 Rule #9 相关**: CLAUDE.md 规则 #9「多终端场景经 claim/reconcile advisory 协调」的设计前提是 `docs/handoff/latest.md` 反映当前真实活跃 track。若停留在拆分前状态, 另一个终端/session 据此判断"只有一个被阻塞的 Spec"而不知道已拆分出独立推进的 A 侧, 存在与 memory `feedback_concurrent_duplicate_audit_fetch_before_start` 同形的重复劳动/漏审计风险。

**why not against proposal.md itself**: 这不是 proposal.md 内容本身的缺陷, 而是围绕它的跨文档 KB 状态同步缺口, 严格说不属于「被审对象=proposal.md」的直接范围, 但落在我本职「Rule #9 合规」审视角度内, 如实上报。是否该由 A.1 落地这一步顺手更新, 还是留给下一次 session-closer/D.1 处理, 建议 owner 或后续会话裁定。

**blocks_phase_b**: false

**introduced_by_r1fix**: false (与 R1-fix 的具体改动无关, 是围绕整个 A/B 拆分决策的既有 KB 同步缺口)

---

### minor-3: 4 处新增/强化的 "follow-up" 承诺均无 issue 编号或验收标准, Level 2 无 `tasks.md` 承载

**locator**: `proposal.md:163` (168h catch-all 不重试权衡) · `:263`/`:390` (共享重试 helper 抽取) · `:379` (fetch_gate.py/worktree_manager.py 同形兄弟, 此条承自 R1 前版本)

**evidence**: `grep -n "follow-up"` 命中 4 处, 逐处读取均**无** issue 链接 / 编号 / 验收判据。用 `git show 0548317:...proposal.md | grep "follow-up"` 核对 R1-fix 前的版本, 仅 `:216`(现 `:379`) 一处已存在, 其余 `:163`/`:263`/`:390` 三处均为 R1-fix 新增或从「条件性入 scope」措辞强化而来 (`:227` 原文「条件性——仅当 spike 判定须抽取共享重试 helper 时入 scope」在 R1-fix 后变为 `:390`「follow-up」+ 机械判据 `git diff --stat`)。对照同文件 `:394-399` 处理"发版清单机械承载缺口"的方式 (如实标注 + 给 owner 两条明确出路), 这 4 处 follow-up 没有获得同等严谨对待。

**how_it_goes_red**: Phase B/D2 执行者若不回读 A 的 proposal.md 原文 (归档后更不易被翻到), 这些技术债 (共享重试 helper 抽取 · 168h 无人值守下 catch-all 不重试的可用性权衡 · `fetch_gate.py`/`worktree_manager.py` 同形兄弟) 不会有任何机制在未来提醒任何人跟进, 与 memory `feedback_fix_the_class_not_the_instance` 点名的"认出了类却没建立跟进机制"同形。

**blocks_phase_b**: false

**introduced_by_r1fix**: true (3/4 处为 R1-fix 新增或实质强化内容)

---

## 4. Level 2 判据复核

R1 M-1 (「无跨仓同步面」被 `:229` 自我推翻) 与 M-4b (「无架构变更」悬在未决 spike 上) 已被 R1-fix 妥善处理: 前者改措辞为「无跨仓**内容**同步面」+ 显式列出发版清单 + 如实标注机械承载缺口 + 把 Level 2/3 的选择权交给 owner (`:394-399`, Rule #10 式留白, 合规); 后者被「钉死: A 不动 `aether.py`」+ 机械判据 (`git diff --stat` 不得出现该文件) 消除了不确定性。两条均**真闭合**, 不是文字游戏——都附带了可执行的验证方式或明确的 owner 决策点。

## 5. 非目标与 B 侧划界一致性

已核对 A 现文 (`:365-379` §非目标) 与 B 侧 proposal.md 抬头 (`:1-24`) 互相引用、措辞对称 —— 均使用「关掉 `gate_check()` 那份实现里的恒绿腿」这个经过限定的措辞, 未见一侧已更正、另一侧仍陈旧的漂移。DEC 本身 (`docs/decisions/DEC-20260812-001-...md`) 也带了对应的带日期更正块 (`:80-105`), 三份文档 (DEC / A / B) 在这条关键限定上口径一致。

## 6. SC 集合自足性

16 条 SC (`grep -c '^\| \*\*SC-A'` 实跑确认 = 16, 与 `:293` 声称的计数法「下表行数」一致, 无 B 侧曾出现过的"数字对不上任何可数集合"问题) 我逐条检查恒真/恒绿/空真风险: 唯一已知的空真 (SC-A11 打桩核验入口) 已在本轮修复且验证 (§2); SC-A-cwd 存在**已被文档自己承认**的诚实限制 (不能区分继承 ambient cwd 与显式传 `cwd=`), 这是恰当的"如实标注局限"而非隐藏缺陷。未发现新的空真/恒真风险。

---

## 7. 我这一轮没有做的事 (边界声明)

- 未继承 B 侧 (post_planning R4) 的任何 finding, 全部 4 条本轮 finding 均在 A 的范围内独立论证;
- 未改任何文件 (本报告除外), 未 `git commit`/`push`, 未调外部 API (未能访问 aria-plugin #137 的实际 Forgejo 页面核实其当前内容, Major-1 的证据链因此止步于"本仓侧可验证的部分");
- 未独立复核 SC-A6/A7/A8/A10/A10b/A10c/A13/A-zero/A-order/A-cli/A-doc/A-sc22/A-baseline 的全部细节 (已由 R1 五席与 R1-fix 交叉验证过, 本轮聚焦我本职角度的新增角度, 未重复劳动)。
