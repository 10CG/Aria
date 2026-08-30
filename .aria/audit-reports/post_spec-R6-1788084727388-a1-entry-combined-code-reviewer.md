---
checkpoint: post_spec
round: 6
role: code-reviewer
verdict: REVISE
scope_ok: true
counts: 3C/11M/13m
---

# post_spec R6 — a1-entry 三份 Spec (rework v4, 2026-08-30) — code-reviewer 席

> **本席镜头 (一句话)**: 跨 Spec 接缝 + R5 九条修复是否真的进了 A.2 消费的三张表 (SC 表 / Impact 表 / 决策记录) + 条款间交叉一致性; 不重审设计优劣。
>
> **基线**: 主仓工作树 (三份 proposal.md 均 `M`, 2026-08-30 10:11 落盘) · aria 子模块工作树停在 `fix/phase1-gate-no-push` @ `007d355`, 代码行号一律按 `git -C aria show d50f9c3:<path> | sed -n 'Np'` 实读 · 主仓语料口径 `cc1bdef`。**本席未修改任何被审文件, 未 `git add/commit/push`。**
> **方法**: 凡本报告写「逐字」处均为 `sed -n` / `git show | sed -n` 实读后抄录, grep 只用于定位。**原文中的带圈数字 (SC-22 / D17 的分项编号) 在本报告一律改写为 [1] [2] … 形式**, 不是原文拼写。
> **三条机械不变量 (决策单第 3 项要求 R6 前跑绿)**: 本席用脚本复跑 —— (1) 正文每个 `SC-NN` 在本文件 SC 表内有行: 母 33/33 (`SC-7a` 是引字段 Spec, 非本地 id) · 字段 10/10 (`SC-13`/`SC-19` 是引母/探针的跨文件 id) · 探针 20/20 (`旧 SC-19a/c` 是母旧编号); (2) 正文每个 `--flag` 在 Impact 段出现: 三份全绿 (剩余命中 `--flag` / `--is-ancestor` / `--include=` / `--get` / `--no-tags` / `--symref` 均为 git/grep 参数或占位, 非本 Spec 的 CLI 面); (3) 枚举拼写唯一: `"bad_token_union"` 4 处一种拼写, `"none_sentinel"` 8 处一种拼写, `"wu_empty"` 只出现在「原 …」括注。**三条全绿, 与执笔侧自述一致。** 因此本报告不再花篇幅在机械项上。

---

## (b) Findings (按严重度)

### Critical

#### 接缝 C1 — `--linked-issue` 实参的省略门: 字段 Spec 定义了四态 (三态省略), 母 Spec 只豁免哨兵且 SC-12 反向规定「不得跳过」; 字段 Spec 又声称母 §2 已有「从 `--emit-arg` stdout 取实参」一句, 母 Spec 全文零命中

- **字段 Spec** `:218` 逐字: 「**一句话判据**: **只有 `OK` 且非哨兵的那一格产生 `--linked-issue` 实参**, 其余三格一律省略。」 `:219` 逐字: 「母 Spec 的 A.1 模板在本 Spec ship 后**从该 stdout 取实参, 空 ⇒ 省略 `--linked-issue`**; ship 前 AI 按 E6 手工取。」 `:602` 逐字: 「母 Spec 的 A.1 模板在本 Spec ship 后改从它取实参 (母 Spec §2 一句), ship 前 AI 手工取; 该切换点未写成 SC (行为面), 请 R6 看是否需要。」 `:572` Impact 逐字: 「**它的 stdout 就是母 Spec A.1 模板 `--linked-issue` 的实参来源** (空 ⇒ 母 Spec 省略该参数)」。
- **母 Spec** 实测: `grep -c "linked_issue_field_probe\|emit-arg\|E6\|BAD_TOKEN\|NO_TOKEN\|手工取\|从该 stdout" proposal.md` = **0**。母 Spec 对该实参的全部规定只有三处, 且只豁免哨兵: `:111` 逐字「token 为「无关联」哨兵时 (canonical `none`, alias `无` …): 整个 `--linked-issue` 参数必须省略」; `:527` rule6_note (a) 逐字「A.1 起草前必调 `phase1_gate.py` 且传 `--linked-issue` (token 为哨兵 `none`/`无` 时**省略**该实参)」; §6 首行 `:458` 只列「哨兵 … 或字段缺席」。而 **SC-12** `:578` 逐字: 「| **SC-12** (行为) | spec 有「关联 Issue」但未传 `--linked-issue` | AI 不得跳过该参数 |」。
- **为什么是 Critical (两个相反规定 + 引用悬空 + 实现无归属)**: (1) 一份字段为 markdown 链接形 (`NO_TOKEN`, 存量 14/14 全是这种) 或未填号的模板 placeholder (`BAD_TOKEN`) 的 proposal, 字段 E6 规定**省略**, 母 SC-12 规定**不得跳过** —— 同一事件两个相反规定, 而 K8 已实跑证明 placeholder 照传会让两份无关 Spec 互相命中 (「什么都不做就中」)。母 Spec 若先 ship (两侧都成文「任意顺序」), 只读母 Spec 的实现者按 `:527`/`:578` 落地即复现 K8。这是 R5 comment-analyzer **字段 C-2** 原样未回灌 (母侧同步是它处方的「两侧同批」一半)。(2) 字段 `:602` 括注「(母 Spec §2 一句)」指向不存在的文本 (memory `cross_doc_claim_verify_at_target`)。(3) 「字段 ship 后把 A.1 模板改为从 `--emit-arg` 取实参」这条编辑没有归属: 字段 Spec Impact 不列 `phase-a-planner/SKILL.md` (它不碰母的 hunk), 母 Spec Impact / SC-22 六字面量也不含 `--emit-arg` ⇒ memory `split-makes-seams` 的「实现无归属」形状。
- **建议处置 (两侧同批, 只建议)**: 母 `:111` 段标题改为「token 不产生合法 canonical 值时 (哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD`, 分档判据引字段 Spec E6 四态表) 整参省略」; 母 SC-12 场景改为「spec 字段判 `OK` 且非哨兵但未传 `--linked-issue`」; 母 §6 首行缺口描述同步扩; 母 §2 或 Impact `phase-a-planner` 行补一句「字段 Spec ship 后实参改由 `linked_issue_field_probe.py --emit-arg <proposal>` stdout 提供 (空 ⇒ 省略), 该模板改动归母 Spec 后续 PATCH 或由字段 Spec 承担 —— 二选一写死」; 字段 `:602` 括注按母侧实际改写。

#### 接缝 C2 — 探针 Spec「可先于姊妹 ship, 全走层 2」与「E0–E6 一条都不复制」+「import `lib.linked_issue_field` 逐字钉死」三者不可同时成立: 姊妹未 ship 时层 0 定位与层 2 的字段行都没有实现宿主

- **探针 Spec** `:133` 逐字: 「**⛔ 本 Spec 不得内含第二份抽取实现 (E0–E6 一条都不复制)。**」 `:137` 逐字: 「本 Spec **可先于姊妹 ship** —— 此时层 1 恒 `NO_TOKEN`、**全部走层 2** (= 今天的状态, 见下方「姊妹 Spec 未 ship 时的行为」); 姊妹 ship 后本 Spec **必须**改为 import 该纯函数以接通层 1, **该改动是本 Spec 的 follow-up 而非前置**。」 `:156` 逐字「**⇒ 本 Spec 采用该模式, 逐字钉死**」+ `:162` 逐字 `from lib.linked_issue_field import extract_linked_issue_field`。 `:169` 逐字: 「四态里只有 `NO_FIELD` / `NO_TOKEN` 会出现 (canonical 层恒无输出) ⇒ 全部依赖层 2。」 `:182` 层 2 逐字: 「姊妹判定 ∈ {`NO_TOKEN`, `BAD_TOKEN`} 时 (**且仅当**), 从该 proposal 的**「关联 Issue」字段行本身**提取全部形如 `/<org>/<repo>/issues/<n>` 的片段」。 `:70` 逐字: 「姊妹 Spec `linked-issue-field-availability` 是本 Spec 的能力上限提升项, 不是阻塞前置。」 **字段 Spec** `:247` 逐字对称: 「探针 Spec 的「非阻塞」措辞同批订正 (它可先 ship 并全走层 2, 该函数 ship 后再接层 1)。」
- **为什么是 Critical**: 「全走层 2」仍要 (a) 用 E0 三谓词定位**字段行** (`:182` 明写「从字段行本身提取」), (b) 判出 `NO_FIELD` / `NO_TOKEN` 四态之二 (`:169`)。这两件事的唯一宿主是姊妹的 `lib/linked_issue_field.py::extract_linked_issue_field` (字段 Impact `:568`, 新建); 姊妹未 ship 时该模块不存在, `:162` 的钉死 import 抛 `ImportError` ⇒ 探针每轮 exit 非 0 ⇒ 消费面恒「未能核实」; 若为了「先 ship」自写层 0 定位, 又违反 `:133`。探针 Impact `:524` 把 SC-1~15/17/18 全挂在 `tests/test_sibling_spec_probe.py` —— SC-7/8/9/10/11/18/19 的期望值全是姊妹四态的函数, 姊妹未 ship 时**整套测试不可运行**。⇒ 这正是 R3/C3 判定的「E0–E6 实现无归属」在「ship 顺序」这一维上原样存活: 两侧措辞一致 (都说可先 ship), 但联合起来不可实现 (memory `split-makes-seams`: 拆后必做只看接缝的核验)。
- **建议处置 (属 owner 决定, 因为它改变 2026-08-23 拆分时「均非阻塞前置」的成文前提)**: 二选一写死 —— (i) 把姊妹的 `lib/linked_issue_field.py` 声明为探针的**硬前置** (探针 §1 依赖方向第 3 条 + 字段 `:247` + 母 §4 指针段同批改「探针 ship 依赖字段 Spec 的纯函数模块」, 三处); 或 (ii) 保留「可先 ship」但把「姊妹未 ship 时」的行为改成 `verdict="not_established"` + `reason="extractor_unavailable"` (import 失败 fail-soft, 探针不定位任何字段行), 并把 SC-1~15 的宿主注明「须在姊妹模块存在时运行, 否则 skip」。两案都不改 E0–E6 的归属, 只改依赖声明。

#### 母 C1 — Level 1 路径下「前置 claim 零调用」只写在 Impact 行的括注里, SC-9 与 §2.5 都没有这一臂; rule6_note (a) 仍写「A.1 起草前必调」

- **母 Spec** Impact `:658` 逐字: 「**Level 1 (`skip_if: complexity: Level1`, 实读 `:66`) 时前置 claim 零调用** (R5/M4: 否则每个 typo 修复写一条永不 release 的僵尸 claim + 一次外向 push; SC-9 补该臂)」。
- **SC-9** `:575` 逐字全行: 「| **SC-9** (**行为**, 定向 fixture — **⚠️ 类别按 R2/M-16 订正, 旧标「代码」有误**) | `coordination.enabled == false` | A.1 **零调用**, 不写 claim, 不推远端 | …」—— **无 Level 1 臂**。§2.5 (`:365-369`) grep `Level` = **0**。rule6_note (a) `:527` 逐字「(a) A.1 起草前必调 `phase1_gate.py` 且传 `--linked-issue` …」无 Level 1 例外。
- **为什么是 Critical**: 这正是 R5 判「不可进 A.2」的形状 —— 修复只写进 Impact 行的括注 (「SC-9 补该臂」是对 SC 表的**声称**, SC 表没动), A.2 从 SC 表派生 fixture 会漏掉这一臂; 且 rule6 (a)「必调」与 Impact「零调用」对 Level 1 这一事件是两个相反规定。R5 skill-reviewer **母 M4** 的三个落点 (§2.5 skip 条件 / SC-9 臂 / Impact) 只落了一个。
- **建议处置**: §2.5 首条 bullet 补「判定 Level 1 (`phase-a-planner/SKILL.md:67` `complexity: Level1` 命中) ⇒ 前置 claim 零调用」; SC-9 场景列改为「(A) `coordination.enabled == false`; (B) Level 1 skip 命中」两臂, 期望/怎么会红各补一句; rule6 (a) 加「(Level 1 与 `enabled == false` 时零调用)」。

### Major

#### 母 M1 — 把 `branch-manager/SKILL.md:146` 的 `Part A1` 改成 `Part B1` 是一处**事实错误的编辑**: `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的**部件名** (= REQUIRE claim + enabled 默认翻转), 不是「Phase A.1」; `Part B1` 在同一命名空间里指 `linked_issue` 字段

- **母 Spec** `:125` 逐字: 「该标题的 `Part A1` 本 Spec 同批改为 `Part B1`, 见 Impact 表 `branch-manager` 行」; rule6 #8 `:516` 逐字: 「`branch-manager/SKILL.md:146` 块: 占位串同步 + 标题 `Part A1` → `Part B1` (R5/M2: 该块命令是 `--phase B`, 标题却写 A1, AI grep 到会照抄成 A.1 入口)」; Impact `:664` 逐字: 「标题 `(Part A1, MUST — …)` 改为 `(Part B1, MUST — …)`」。
- **实读**: `openspec/archive/2026-07-11-coordination-claim-lifecycle-and-overlap/proposal.md:35` 逐字「**A1 (插件内)**: `enabled` 默认 false→true + phase-b-developer/branch-manager 进 Phase B 前 REQUIRE 一条本 (container,session) 的 active claim, 无则强制先 claim。」; `:50` 逐字「部件 A1 翻 enabled 默认可能对未配置项目引入 claim 写入 …; 部件 B1 加字段是 additive」。aria `d50f9c3`: `phase-b-developer/SKILL.md:86` 逐字 `B.0 - REQUIRE claim (coordination-claim-lifecycle-and-overlap Part A1, MUST):`; `config-loader/SKILL.md:136` 逐字 `default: true                   # Part A1 (defect a): false→true — …`; `state-scanner/SKILL.md:149` 逐字「coordination-claim-lifecycle-and-overlap Part A1 把默认 false→true」; `tests/test_coordination_default_lockin.py:1` 逐字 `"""Part A1 lock-in (coordination-claim-lifecycle-and-overlap).`; 反之 `lib/collision.py:172` 逐字 `# Part B1 — linked_issue semantic-overlap advisory`, `phase1_gate.py:1228` 逐字 `# Part B1 (additive key): "same issue, two names" advisory.`。**母 Spec 自己在 `:132` 也按这个含义用 `Part B1`**: 「「是不是同一个 issue」由 claim 的 `linked_issue` 字段承载 (Part B1 已 ship, …)」。
- **为什么是 Major**: R5/M2 把部件名 `Part A1` 误读成「Phase A.1」, v4 把这个误读落成了对已 ship SKILL.md 的一处改名, 改完后 branch-manager 的 REQUIRE-claim 块会被标成「linked_issue 部件」—— 与仓内其余 5 处 `Part A1` / `Part B1` 用法全部冲突, 且母 Spec 自身 `:132` 与 `:664` 对同一记号取两个含义。可单侧修: SC-22 [1] 要求标题含 `A.1`、[4] 禁 `--phase B` 已足以把两个块分开, 改名没有必要。
- **建议处置**: 删去 `:125` 括注、rule6 #8 的「标题 `Part A1` → `Part B1`」、Impact `:664` 的改名半句 (只留占位串同步); rule6 #8 的性质说明改为「占位串取值口径 hunk」。

#### 母 M2 — SC-22 没有落 D17 要件 [2]「至少一条可直接执行的完整命令行」: 六个字面量散落在散文里的实现也绿; 探针的 SC-20 反而落了

- **D17** `:500` 逐字: 「[2] 块内须含**至少一条可直接执行的完整命令行** (脚本路径 + 必需参数), 不得只有概念名 / 名词短语」。**SC-22 [2]** `:605` 逐字: 「[2] 切片内含**六个字面量**: `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` / `--raw-track-id "<spec-slug>-<container_uuid>"` / `未能核实`」—— 无「以 `python3` 起首的一行」断言。对照探针 **SC-20** `:501` 逐字: 「**且**含一条以 `python3` 起首、含 `sibling_spec_probe.py` 与 `--own-spec-dir` 的完整命令行 (D17 [2])」。Impact `:658` 写「含 D17 [2] 的完整命令行 = §2 的模板」, 但那是 Impact 的要求, 不是 SC 的断言。
- **为什么是 Major**: 坏实现「本步骤调用 `phase1_gate.py`, 传 `--linked-issue`、`--include-terminal`、`--phase A.1` 与 `--raw-track-id "<spec-slug>-<container_uuid>"`; 失败时渲染「未能核实」」六字面量全中而无一条可执行命令 —— 正是 R5 对探针 C1 点名、母 Spec 用 D17 想类级消掉的那个形状, 母 Spec 自己的 SC 没照做 (memory `cite≠apply`)。另 §2 模板的 `--mode advisory` / `--repo-path` 也不在六字面量内。
- **建议处置**: SC-22 加 [7]: 切片内含一条以 `python3` 起首、含 `phase1_gate.py` 与 `--phase A.1` 的完整命令行 (与 SC-20 同形)。

#### 母 M3 — SC-22 [5] 与「[2]–[6] 只在该切片内求值」互斥, 且新标题块在 `phase-a-planner/SKILL.md` 里的放置位置未钉 ⇒ 两个实现者会得相反结果

- `:605` 逐字: 「「步骤块」= 从匹配 [1] 的标题行起, 至下一个 `^#{1,4}[ \t]` 行 (或文件尾) 止的切片; [2]–[6] **只在该切片内求值**。」 同行 [5] 逐字: 「**仅 `phase-a-planner`**: 其 ```yaml 围栏内 `A.1 - Spec 管理:` 项下含逐字 `precondition: 见「前置: REQUIRE claim」小节 (MUST, 在本表之前执行)`」。
- **实读** `phase-a-planner/SKILL.md` (`d50f9c3`): `A.1 - Spec 管理:` 在 `:63`, 位于 `### 步骤执行` (`:60`) 之下的 ```yaml 围栏 (`:62` 起) 内。新标题「在本表之前执行」若放在 `### 步骤执行` 之前, 切片止于 `:60` ⇒ YAML 围栏在切片外, [5]「只在切片内求值」恒红; 若放在 `### 步骤执行` 与 ```yaml 之间, 切片吞下整个 YAML 表直到 `### 输出` (`:101`) ⇒ [5] 可求值, 但「前置块」在结构上包含了它要「先于」的表。母 Spec 「未做/存疑 #2」自陈「SC-22 [5] 的 `precondition:` 落点由 A.2 钉」—— 但 [5] 的可求值性取决于这个未钉的落点 (memory `spec-underdetermination`)。
- **建议处置**: 把 [5] 改写为「在**整个文件**的 ```yaml 围栏内求值, 不受块边界限制」(一句), 或钉死新标题放在 `### 步骤执行` 之前并把 [5] 从「切片内」条款里显式摘出。

#### 母 M4 — SC-23 与 SC-14(a) 标「现状 … 必红」为假: 作为 CLI 全链路夹具, 今天用同一串 X 先 acquire 后 release 就是绿的; 它们与 SC-2 / SC-15 同属「baseline 即绿的回归守卫」, 应同样如实标注

- **SC-23** `:606` 逐字 (怎么会红): 「现状 A.1 原串 ≠ carry-id ⇒ `release_claim_by_track` 按 `(container, 归一 track_id)` (`lib/claim_lifecycle.py:377`/`:425`) 匹配不到 ⇒ claim 悬挂到 sweep ⇒ 必红。」 **SC-14(a)** `:585`: 「该臂的红点在「传 A.1 原串能否匹配到」(与 SC-23 同根: 不统一 carry-id 则匹配不到, 必红)」。
- **实读**: `release_claim_by_track` (`claim_lifecycle.py:377`) 匹配 `:425-427` = `if rec.container == resolved.container_id` / `and rec.track_id == norm` / `and rec.status == "active"`; `phase1_gate.py:1191` `--phase` 无 `choices=` ⇒ `--phase A.1` 可用。一条代码测试「`phase1_gate.py --raw-track-id X --phase A.1` → `release_gate.py --raw-track-id X --status abandoned`」在 `d50f9c3` 上**今天即通过** (`tests/test_release_by_track.py` 就是这条路径)。「原串 ≠ carry-id」是**三处 SKILL.md 模板**的文本/行为缺陷, 代码夹具里由测试作者同时手写 X 两次, 感知不到。⇒ 与 R5 主控对 SC-2 的裁法同形: 真正的「怎么会红」只能是「改坏 `derive_track_id` / 匹配键」的回归守卫; 「AI 三处是否逐字复用」属文本层 (无 SC) + rule6 照跑档。
- **为什么是 Major**: 母 Spec 刚为 SC-2/SC-15 精确区分了「baseline 红/绿」并要求 A.2 用坏实现验红 (memory `check-runs-at-baseline-first`); SC-23 用同一套措辞标了相反的 baseline, A.2 会去找一条不存在的红。
- **建议处置**: SC-23 / SC-14(a) 的「怎么会红」改为「baseline 即绿的回归守卫: 坏实现 = `derive_track_id` 去容器段 (SC-2 同时红) 或 `release_claim_by_track` 匹配键改坏」; 「三处模板逐字复用」的文本层若要守, 加一条对 `phase-b-developer:92` / `branch-manager:148` / `phase-d-closer:52` 占位串字面的断言 (见 minor 母 m4)。

#### 母 M5 — §瓶颈 `:83` 的「可当场复核」现状句复核即错, 且 6i 落版后方向反了 (R5 comment-analyzer 母 M-4 未回灌)

- `:83` 逐字: 「**落盘后的现状 (可当场复核)**: 旧 §1 连同那行示例已迁出, 本文件按 FIX-19 补了**真的**字段 (第 12 行) ⇒ `changes/` 下的 1 条命中现在是**真阳**。」 `:78` 的口径命令逐字 `grep -rl '\*\*关联 Issue\*\*' openspec --include=proposal.md | wc -l   # 15  (14 在 archive/, 1 在 changes/)`。
- **实测 (当前工作树)**: 本文件的字段在 **`:13`** 且拼写已改 `> **Linked Issue**:` (`cat -A` 逐字节 `> **Linked Issue**: \`none\` …`), `:78` 那条按 `关联 Issue` 的 grep 对母 Spec **不再命中**; `grep -rnE '^> \*\*关联 Issue\*\*:' openspec/changes/` 的唯一命中是字段 Spec `:95` (围栏内的 markdown 链接形示例) ⇒ 「`changes/` 下的 1 条命中」现在是**假阳**, 不是真阳。
- **建议处置**: `:83` 改为「三份在制 Spec 头部均为 canonical `Linked Issue` + 哨兵 `none` (`:13` / 字段 `:6` / 探针 `:6`), 旧口径 `关联 Issue` grep 在 `changes/` 已只剩围栏内示例; 数字是当日观测, 复核以命令为准」。

#### 母 M6 — `:235` 标「逐字」的引文出处仍标错文件 (R5 factcheck A-M1 未回灌; R5 聚合报告「主控自证 #1」已承认)

- `:235` 逐字: 「实读 `skills/state-scanner/scripts/coordination_probe.py:4-25`: … 而该分区「written only by the CLI production path (`_main` → `_gated` with `_source="production"`)」(逐字)。」
- **实读**: `git -C aria grep -n "written only by the CLI production path" d50f9c3 -- .` 唯一命中 `skills/state-scanner/scripts/phase1_gate.py:1048`; `coordination_probe.py:18-21` 是同义另一句 (逐字 `The production partition file is written only when ``_source=="production"``,` …)。结论不变, 但这一段正是全文援引「逐字」纪律最重的一段。
- **建议处置**: 出处改 `phase1_gate.py:1048` (run_gate docstring), 探针侧改引 `coordination_probe.py:18-21` 的实际句子。

#### 母 M7 — K6 的「加 swept 标记」follow-up 仍无落点 (R5 comment-analyzer 母 M-2 未回灌)

- `:282` (§2.3 `abandoned` 行) 逐字: 「**给 `ClaimRecord` 加 swept 标记以真正分辨二者, 记 follow-up, 不在本 Spec**」。Impact follow-up 表 `:683-688` 六行 = owner-container 口径 / SWEEP_TTL 措辞 / unknown 路径 / B.0 YAML 形态 / unattended 三腿 / 跨容器 release —— **无 swept 行**。
- **建议处置**: follow-up 表补第 7 行 (改 schema 须与 `coordination-ref-schema.md` §3 演进契约同批评估)。

#### 母 M8 — `unattended` 的取值路径「容器镜像 / Nomad env」二选一混写, 而 env 三腿被明写「不在本 Spec」⇒ 该分支在生产的进入条件未定义 (R5 code-simplifier M4, 未处置亦未上呈)

- `:268` 逐字: 「`state_scanner.coordination.unattended == true` (**新 config key**, type boolean, **default false**; 在 `config-loader` 登记并在 `DEFAULTS.json` 注册, 由 aria-runner 容器镜像 / Nomad task env 显式置 true)」; `:273` 逐字: 「**Layer 1→2 的 env 传递三腿契约** … **不在本 Spec** —— 缺 import 会静默 fallback 到 `false` (即「照问不误」), 转 A.2/follow-up。」
- **为什么是 Major**: 「容器镜像置 true」= 写 `.aria/config.json` 路径 (本 Spec 内可闭环, 廉价); 「Nomad task env」= 三腿契约 (明写不在本 Spec)。两者并列且未选 ⇒ 实现者按后者读时 SC-26 只在夹具里为真, 生产分支永不进入; 与 AD10 的冲突就没有真的解掉。R5 聚合报告未把该席 8 条 Major 呈给 owner (只呈了选项 A/B), 本条在 v4 无处置也无拒绝留痕。
- **建议处置**: 把取值路径逐字钉死为「aria-runner 镜像内 `.aria/config.json` 的 `state_scanner.coordination.unattended: true`」(env 三腿保持 follow-up), 或整条转 follow-up 并在 §2.3 写明「本 Spec 只登记 key, 生产接线由 follow-up 承担」。

#### 探针 M1 — §3 的两处仍只写 `无`: 「`OK` 两分的写死判据」(`:116`) 与对姊妹 E6 的引述 (`:186`), 与同节映射表 `:112` 的 `{none, 无}` 是同一份文档两个规定

- `:116` 逐字: 「- **`OK` 的两分靠什么区分要写死**: 靠**姊妹 E3 的 token 串本身**逐字节比 `无` (单个 U+65E0, 无空白、无其他字符 —— 姊妹 E5 原文), **不靠**归一结果、**不靠**集合是否为空。」 `:186` 逐字: 「后者由姊妹 E6 单独规定 (「第一个 token 元素逐字节; token 串为 `无` 时整参省略」)」。对照 `:112` 逐字: 「| `OK` | token 串为**哨兵** (姊妹 §2 集合 `{none, 无}`: `none` 按 ASCII 大小写折叠 / `无` 逐字节) | **层 1.5** | …」。字段 E5 (`:197`) 逐字「**是哨兵** (逐字节等于 `无` [单个 U+65E0], **或** ASCII 大小写折叠后等于 `none` …)」; 字段 E6 现为四态表 (`:211-218`), 「token 串为 `无` 时整参省略」已不是它的原文。
- **为什么是 Major**: `:116` 是被标为「写死」的分派判据; 照它实现, `none` 落层 1 → `normalize_linked_issue("none")` 返 `None` → 原串键 `("r","none")` → 两份 `none` 互相命中 —— SC-9 的 (`none`,`none`) 组会抓到, 所以不是 Critical, 但同节两个判据相反是 R5 判「不可进 A.2」的原病。`:186` 是对姊妹 E6 的**失实引述** (两次修订后仍是 2026-08-25 的旧文)。
- **建议处置**: `:116` 改「逐字节等于 `无`, 或 ASCII 大小写折叠后等于 `none` (姊妹 §2 集合)」; `:186` 括注改引 E6 四态表 (「只有 `OK` 且非哨兵产生实参, 其余三格省略」)。

#### 字段 M1 — 头部「代码落点」仍缺 Impact 首行的 `lib/linked_issue_field.py` 与仓本地 `.aria/linked-issue-field-grandfathered.txt` (R5 comment-analyzer 字段 M-1 只回灌了 §非目标那一半)

- `:7` 逐字: 「**代码落点** (**三个仓**): `standards/` 子模块 `openspec/templates/proposal-minimal.md` (跨项目 SOT) + `aria/` 子模块 `skills/spec-drafter/SKILL.md` 与 `skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**) + 主仓 `.aria/state-checks.yaml` (注册)」。Impact `:568` 首行 = `aria/skills/state-scanner/lib/linked_issue_field.py` (**新建**, R3/C3, 探针 Spec 的承重依赖); `:569` = `.aria/linked-issue-field-grandfathered.txt` (**新建**)。§非目标 `:554` 已订正为「新建两个文件」, 头部未同步。
- **建议处置**: `:7` 补两个新建文件。

#### 字段 M2 — SC-5 的臂数在同一文档三个值 (五 / 五 / 四+e1e2), §4 判据表无「白名单文件缺失」行 (R5 comment-analyzer 字段 M-2 未回灌)

- `:418` 逐字 「**探针的判据分割 (fail-CLOSED, 五臂)**:」 (表体 5 行, 无「`--grandfathered` 文件缺失」行); `:523` 逐字 「| SC-5 (探针判据分区五臂) |」; `:540` 逐字 「**探针判据分区四臂**。(a) … (d) … **(e)** … **(e1)** … **(e2)** …」。
- **建议处置**: `:540` 改「六臂」并把 (e1)(e2) 提为独立臂; `:418` 表补第 6 行「`--grandfathered` 缺省或文件不存在 ⇒ 白名单空集, 照常判定」; `:523` 同步。

### minor

1. **母 m1 — D17 要件 [1] 的边界定义只覆盖「标题起至下一标题」**: 字段 SC-7a (`:543`) 引 D17 [1] 但块边界 = ``` 围栏 (「块边界 = 该 ``` 围栏, D17 [1]」), 与 `:500` 逐字「从锚点标题行起至下一个 `^#{1,4}[ \t]` 行止」不是同一规则; 且围栏内的 `#` 行 (如 `spec-drafter/SKILL.md:137/:142/:145/:148/:152/:156` 预览骨架里的 `# User Authentication` 等) 会被字面规则当作切片终点。建议 D17 [1] 补一句「围栏内的 `#` 行不作为边界; 被测块本身是围栏时边界即该围栏」。(母 Spec 新表面 #4 已自问此题, 本席确认它是真问题。)
2. **母 m2 — 行号新错 (v4 引入)**: `:658` 与 `:755` 写 `skip_if: complexity: Level1` 在 `:66`; 实读 `phase-a-planner/SKILL.md:66` 逐字 `    - has_openspec: true          # 已有活跃 Spec`, `:67` 逐字 `    - complexity: Level1          # 简单任务` (R5 skill-reviewer 原写 `:67` 是对的)。
3. **母 m3 — SC-11 (`:577`) 仍写「四档选项集不同」**, 同行又写 `abandoned`「按 `active` 同档请裁」⇒ 照字面建 fixture 会去分辨一个已合并的档 (R5 comment-analyzer 母 m-1 未回灌)。建议「四档渲染不同, `abandoned` 与 `active` 共用选项集」。
4. **母 m4 — §非目标 `:627` 「**唯一的边界争点已成文**: §2.1b 的 carry-id 统一 …」不再唯一**: `branch-manager:146` 标题改名 (若保留) 与 `phase-b-developer:96-97` 注释勘正也是 Phase B 文档面的触碰; 且三处 carry-id 占位串 (`phase-b-developer:92` / `branch-manager:148` / `phase-d-closer:52`) 只有 rule6 照跑档覆盖, 无文本层断言 (对比 A.1 两处有 SC-22)。建议一句「另有两处描述性勘正」+ 视需要加一条占位串字面断言。
5. **母 m5 — rule6_note 11-hunk 表漏一个描述性 hunk**: Impact `:662` 把 `state-scanner/SKILL.md:168` 输出键集补 `push_skipped` / `push_skipped_reason` 与 heartbeat 小节记为「同 hunk」, 但表 #5 只描述了 heartbeat 小节; 按母 Spec 自己「逐 hunk 判」的纪律该键集勘正是描述性档 (第一行), 缺 substitute 声明 (可与 #11 同法: 结构化断言「`:168` 一带含字面 `push_skipped`」)。
6. **母 m6 — R5 factcheck 的一批引用 minor 未回灌 (全部不改结论)**: D4 `:487` 仍写「§2.2 `:188`」(现 `:188` 为空行, 口径统一段在 `:205`); `:356` 引归档件 `:260` 实为 `:259` (`:257` 逐字正确); `:360` 「`_run_gate_impl` … 至下一个顶层定义 `run_gate` `:1032` 前」实为 `:950 def _telemetry_path(`; `:232` 「`basicConfig` 只在 `scan.py`」在全 aria 为假 (`issue-triage/scripts/triage.py:290` 亦有), 限 state-scanner 内为真; `:713` FIX-04 「全文 grep `A1_SWEEP_TTL` = 0」自指命中 1; `:207` docstring 引文删去 `ship/close` 未标省略; `:57` `skip_if:` 实在 `:95`; `:667` §3.2 五条实为 `:133-140`; 字段 Spec 全文 `FIX-07` = **0** 命中 (母 `:716` 称「随 §1 迁出」, 承接方零锚点)。
7. **字段 m1 — §Why `:58` 的 grep 输出仍写 `proposal.md:88:   > > **关联 Issue**: …`**: 该行在任何已提交 SHA 上都不是 `:88` (真身 `cc1bdef:75`, 且自三份产物落盘起母 Spec 全文 depth-2 命中 = 0); SC-1 (c) `:536` 已改引 `cc1bdef:75`, D2 `:488` 指定「§Why 的 grep 输出」为稳定锚点, 而那段输出自身是错的 (R5 factcheck L-M1 只修了 SC-1 一半)。
8. **字段 m2 — 跨文档行号/拼写残留**: `:84` / `:461` 写母 Spec 字段在 `:12`, 实为 `:13` (母 `:83` / `:728` 自写「第 12 行」同误); `:469` 同一格既写「`:6` token 串 `none`, 2026-08-30 改」又括注「本席实读其 `:6` 为 `> **关联 Issue**: \`无\` — …」(探针 `:6` 现为 `> **Linked Issue**: \`none\``)。
9. **字段 m3 — 轮次脚手架与命名残留**: `:249` / `:369` 逐字「请 R4 优先审」; `:416` 引 `custom_checks.py:122-123` 实为 `:123-124` (`:122` 空行); `:326` 「共 **10** 条 check」与 `:416` 「实测 = **11**」并存 (后者已作口径说明, 但前者未标「当日观测」); `GRANDFATHERED` 仍作机制名用于 `:398` description / `:424-425` 表 / D6, 而 R3/C2 已把它改成仓本地文件 (R5 comment-analyzer 字段 m-2)。
10. **探针 m1 — 残留**: `:138` 逐字「请 R4 优先审」; `:555` 段尾仍以「**这是本轮最实的跨 Spec 风险。**」结尾 (段首已写「该风险已闭环」); 新 `SC-19` 与 `:69` / `:476` / `:486-487` 的「旧 SC-19」同名 (v4 未按 R5 建议改号, 靠「旧」字前缀区分, 编号说明 `:476` 未补「本文 `旧 SC-NN` 一律指母 Spec 编号」一句)。
11. **探针 m2 — SC-17「全文恰 2 次」与 Impact 新节的相容性未定义**: `:498` 逐字「对 `references/execution-modes.md` 全文计数字面串 `每轮入口: 竞品 spec 探针` | 出现**恰 2 次**」; Impact `:526` 逐字「**另新增一节** `## 竞品 spec 探针 (per-round 入口)` 承载 §7 十二字段 stdout 契约 + exit code 三分 + §9 三档消费措辞的**权威可执行版**」。若权威版复述 §8 那两行 (含前缀), 正确实现得 3 ⇒ 红。建议 SC-17 计数范围限定为两个模式块的围栏内, 或在 Impact 明写新节不得出现该前缀字面。
12. **探针 m3 — `read_only` 的来源未定义**: `:214` 复用 `resolve_enforced_remotes(configured, actual_remotes, read_only)`, `:221` / SC-4 `:485` 都以「全部落 `read_only`」作场景, 但全文没写 `read_only` 从哪个 config 键取 (`multi_remote.py:255-259` 签名默认 `()`)。建议钉一句 (取 `.aria/config.json` 的哪个键, 或恒为空元组)。
13. **流程 m1 — R5 code-simplifier 的 C3 与 M1/M2/M3/M5/M6/M7/M8 八条既未进 R5 聚合的「主控处置建议」, 也未在 v4 或决策单留任何采纳/拒绝痕迹** (只有 C1 → 1A、C2 → `dataclasses.replace` 纪律被接住)。其中 M4 已在上方升为 母 M8; 其余是简化建议而非缺陷, 本席不替它们定级, 但按 memory `narrow-owner-options` 应至少在 handoff 或决策单里留一行「未采纳, 理由」供 owner 复议 (Rule #10)。

---

## (c) R5 逐项回灌核验表

| R5 项 | 现状 | 证据 (行号) |
|---|---|---|
| R5-1 · SC-30/31 入表 | **随 1A 消失 + 撤销说明入表** (行保留标 ⛔, 编号不复用) | 母 `:613-614` 两行 ⛔ + 理由格 |
| R5-1 · SC-32/33 入表 | **入表** (代码类, 场景/期望/怎么会红齐全) | 母 `:615-616`; Impact tests 行 `:657` 列 SC-32/33 |
| R5-1 · Impact `fail-CLOSED` 误名 (`claim_schema.py` 行) | **随 1A 消失 + 撤销说明** | 母 `:648` 「**零改动** (rework v4 / 1A: 不新增 `spec_slug` / `track_form`; 旧行原文见审计轨 §6)」; 全文 `fail-CLOSED` 剩 4 处均指 §2.2 新鲜度谓词 (命名正确) |
| R5-1 · `:642` `compose` 残留 | **消失** | `grep -n compose` 只命中 `:4` 决策单文件名; SC-2 `:563` 负控臂改「两串**相同** (模拟容器段被丢弃)」 |
| R5-1 · `gc.py` + `heartbeat :244-256` 进 Impact | **K1 随 1A 消失 + 撤销说明**; heartbeat 行保留 `:244-256` 引用与 `dataclasses.replace` 纪律 | 母 `:451` 「K1 (heartbeat 逐字段重建的透传面) … 全部无对象」; `:453` / `:651` |
| R5-2 · K2 残余矛盾 (`:453` vs `:497`/`:722`) + day-one 悬崖 | **随 1A 消失 + 撤销说明** | 母 `:614` SC-31 ⛔ 「legacy claim 与新 claim 形态一致 … 无「day-one 悬崖」」; `:451`; 全文 `track_form` / `零影响` / `force-legacy` 只剩撤销句 |
| R5-3 · AB 推生产 ref | **入表 (rule6 ⛔ 段 + Impact AB 行) + 独立修复实存** | 母 `:521` / `:675`; 字段 `:507` / `:576`; aria `007d355` 基于 `d50f9c3`, 本地分支存在、`ls-remote origin` 无该分支 (与决策单「未推」一致); `tests/test_coordination_no_push.py` 在树; `AB_TEST_OPERATIONS.md:222-228` 新段在工作树 (未提交) |
| R5-4 · rule6_note 11 hunk / 9 文件 | **入表** (11 行, 逐 hunk 落档) | 母 `:507-519`; 9 文件数复核成立。缺一个描述性 hunk 见 minor 母 m5 |
| R5-5 · 字段 spec-drafter 预览骨架 | **入表** (Impact hunk B + SC-7a 代码类 + 验证宿主表) | 字段 `:571` / `:543` / `:526` |
| R5-6 · 探针 9 字名词短语 | **入表** (§8 两行可执行串 + SC-20 + Impact SKILL.md/execution-modes 行) | 探针 `:380-381` / `:501` / `:525-526` |
| 席位分歧 · SC-15 回滚代码类 | **入表** | 母 `:586` (代码; baseline 即绿回归守卫 + 负控第三方 claim) |
| 席位分歧 · SC-2 改写声称对象 | **入表** | 母 `:563` (钉 `linked_issue_overlaps` 经 CLI 行为; 负控「两串相同」) |
| skill-reviewer 母 C1 (rule6 6 处) / C2 (AB push) | 入表 (同 R5-4 / R5-3) | 同上 |
| skill-reviewer 母 M1 (SC-22 [3] 幂等谓词删逃逸口) | **入表** | 母 `:605` [3] 逐字串 + `claims/` |
| skill-reviewer 母 M2 (标题含 `A.1` + 禁 `--phase B` + Part A1 改名) | **入表, 但改名那一半是错的** | 母 `:605` [1][4] 正确; `:125`/`:516`/`:664` 改名 → **母 M1** |
| skill-reviewer 母 M3 (`precondition:` 指针) | **入表** ([5]), 但与切片规则互斥 | 母 `:605` → **母 M3** |
| skill-reviewer 母 M4 (Level 1 零调用 + SC-9 臂) | **只在 Impact 括注, SC-9 / §2.5 / rule6 (a) 未动** | 母 `:658` vs `:575` / `:365-369` / `:527` → **母 C1** |
| skill-reviewer 母 M5 (块边界) | **入表** | 母 `:605` 块边界句 |
| skill-reviewer 母 M6 (heartbeat 设计落 reference) | **入表** | 母 `:662` / `:668` [4] |
| skill-reviewer 母 m1 / m2 | 入表 | 母 `:605` 锚点措辞 / 两文件路径绑定 |
| skill-reviewer 字段 C1 / M1 / M2 / m1 | 入表 (hunk B + SC-7a / `:134` 关系实证 / 6i / `:571` hunk 归属) | 字段各行 |
| skill-reviewer 探针 C1 / M2 / M3 / m1 | 入表 (§8 两行 + SC-20 / `:531` import 指针 / SKILL.md 概述+权威版 / `:384`) | 探针各行 |
| feature-dev K2 / K1 item 4-5 / release 过滤算法欠定 | **随 1A 消失** | 母 `:451` / `:614` |
| comment-analyzer 母 C-1..C-5 | C-1/C-2 入表 (SC-2/SC-15 重分类 + compose 消失); C-3/C-4 随 1A 消失; C-5 入表 (SC-30..33) | 同 R5-1 |
| comment-analyzer 母 M-1 (脚手架) | 母 Spec 已清 (`grep "请 R4\|给 R3"` = 0), Status 行到 R6 | 母 `:3` |
| comment-analyzer 母 M-2 (swept follow-up) | **仍只在批注** | → **母 M7** |
| comment-analyzer 母 M-3 (K7 → Impact) | **入表** | 母 `:656` 「[3] 两级都取不到 ⇒ 编排层仍调用 … 追加 `_source="heartbeat"` / `outcome="skipped_no_track"`」 |
| comment-analyzer 母 M-4 (`:82` 复核即错) | **未回灌, 且 6i 后方向反了** | → **母 M5** |
| comment-analyzer 母 m-1 / m-2 | m-1 未回灌 (→ 母 m3); m-2 随 1A 消失 | 母 `:577` |
| comment-analyzer 字段 C-1 (SC-9 入表 + 宿主) | **入表** | 字段 `:545` / `:527` |
| comment-analyzer 字段 C-2 (母侧 `--linked-issue` 门未同步) | **未回灌** | → **接缝 C1** |
| comment-analyzer 字段 M-1 / M-2 / M-3 / m-1 / m-2 | M-1 半 (§非目标改, 头部未改) → 字段 M1; M-2 未回灌 → 字段 M2; M-3 Status 改、`请 R4` 残 2 处; m-1/m-2 未回灌 | 字段 `:7` / `:418,:523,:540` / `:249,:369` / `:416` |
| comment-analyzer 探针 M-1 (`bad_token` 拼写) | **入表** (全文一种拼写) | 探针 `:111` / `:328` |
| comment-analyzer 探针 M-2 (SC-19 同名) | **部分**: SC-19 入表, 未改号, 靠「旧」前缀 | 探针 `:500` / `:476` → 探针 m1 |
| comment-analyzer 探针 M-3 / m-1 | Status 改; `:138` / `:555` 残 | → 探针 m1 |
| factcheck A-M1 (`:238` 出处) | **未回灌** | → **母 M6** |
| factcheck A-M2 (compose) | **消失** | 同上 |
| factcheck L-M1 (`:88` 悬空) | **半**: SC-1 (c) 改 `cc1bdef:75`; §Why `:58` 未改 | → 字段 m1 |
| factcheck 19 minor | 大部分未回灌 (不改结论) | → 母 m6 / 字段 m2-m3 / 探针 m1 |
| code-simplifier C1 (单一形态) / C2 (`dataclasses.replace`) | **入表** (1A: §2.1 / §5 / D3 / D18 / SC 表; §5.3 保留纪律 + Impact `:651`) | 母 `:132` / `:453` / `:501` / `:651` |
| code-simplifier C3 (对账层同居) / M1 / M2 / M3 / M5 / M6 / M7 / M8 / m2-m5 | **未处置、未上呈、无留痕** | → 流程 m1 |
| code-simplifier M4 (`unattended` 取值路径) | **未处置** | → **母 M8** |

---

## (d) 接缝核验表

| 接缝 | 定义侧 | 引用侧 | 判定 |
|---|---|---|---|
| 哨兵集合 `{none, 无}` | 字段 §2 `:154` (canonical `none` 大小写折叠 / alias `无` 逐字节 / 集合封闭) + E5 `:197` | 母 `:111` / `:123` / §6 `:458` / rule6 (a) `:527` 一致; 探针映射表 `:112` / 层 1.5 `:173` / P5 `:430` / SC-9~11 一致 | **一致**, 除探针 `:116` / `:186` 两处只写 `无` → **探针 M1** |
| 字段名两拼写 `Linked Issue` / `关联 Issue` | 字段 E0 谓词 1 `:164` (封闭两拼写, canonical 英文, 写入侧只教 canonical) | 探针层 0 `:89` 「逐字节以 `> **Linked Issue**:` **或** `> **关联 Issue**:` 开头 (姊妹 E0 的两拼写集合 …; 集合封闭, 本 Spec 不另加)」; 母 §6 `:458` 「「Linked Issue / 关联 Issue」token」; 三份头部 `cat -A` 逐字节 `> **Linked Issue**: \`none\`` | **一致**; 谁定义谁引用清楚 (字段 `:14` 逐字「哨兵集合 (§2) 与字段名拼写集合 (E0 谓词 1) 的定义在本 Spec, 母 Spec 与探针 Spec 引用本 Spec」) |
| `"none_sentinel"` 枚举 | 探针 §7 `:328` (6 值枚举) | 探针映射表 `:112` / SC-9~11; 字段术语表 `:312` 引同名 | **一致**; `"wu_empty"` 只在「原 …」括注 |
| `"bad_token_union"` | 探针 `:328` | 探针 `:111` / SC-19 `:500` | **一致** (R5 探针 M-1 已修) |
| `--emit-arg` | 字段 K8 `:219` / Impact `:572` / SC-9 `:545` / 宿主表 `:527` | 母 Spec **零引用**; 字段 `:602` 称「母 Spec §2 一句」 | **引用悬空 + 归属缺失** → **接缝 C1** |
| `--linked-issue` 省略门 | 字段 E6 四态 `:211-218` | 母 `:111` / `:527` 只豁免哨兵; 母 SC-12 `:578` 反向 | **两个相反规定** → **接缝 C1** |
| D17 三要件 | 母 D17 `:500` | 字段 SC-7a `:543` 引 [1] (围栏边界, [2][3] 不适用); 探针 SC-20 `:501` 全落 [1][2][3]; 母 SC-22 `:605` 落 [1][3], **未落 [2]** | 探针合规; 字段合规 (边界规则措辞见 母 m1); 母自身 → **母 M2 / M3** |
| `ARIA_COORDINATION_NO_PUSH` 前提 | aria `007d355` (`lib/failure_handlers.py:91` `COORDINATION_NO_PUSH_ENV = "ARIA_COORDINATION_NO_PUSH"`; `phase1_gate.py:1311` reason `cli_flag` / `env_var`; `release_gate.py:11-13` 同套) | 母 rule6 `:521` / Impact `:675` / `:662` (`push_skipped` 键集); 字段 rule6 `:507` / Impact `:576`; 决策单第 4 项; 运维手册 `:222-228` (射程 4 套件今天 + 母 ship 后加 2 = 母表 #1/#2/#5/#7/#8/#9 六套) | **五面一致**; 分支存在且基于 `d50f9c3`、未推 (与「已落, 未推」一致); 母「未做 #6」的担忧成立 (修复未 ship 前照跑档前提为假, 已成文) |
| `resolve_enforced_remotes` import 路径 | 探针 §3 `:157-163` (skill root → `from lib.…`) | 探针 Impact `:531` 补充 (2) (`state-scanner/scripts` → `from collectors.multi_remote import`), 先例 `handoff_autofill.py:48-51` 逐字对上; §4 `:214` 引 `multi_remote.py:255-286` 实读成立 | **一致**; 两条 `sys.path` 并存未实测已由新表面 #10 自陈; `read_only` 来源未定 → 探针 m3 |
| `<spec-slug>-<container_uuid>` 占位串 | 母 §2.1 `:132` / D18 `:501` | 母 §2 模板 `:104`; §2.1a 文本层 `:164`; SC-22 [2] `:605` 字面 `--raw-track-id "<spec-slug>-<container_uuid>"`; 三处 Phase B/D 占位串按 §2.1b `:189` 改「A.1 认领时派生的那一串; 未走 A.1 的 session 沿用 Spec id」(Impact `:663-665`) | **一致** (两种措辞是设计: A.1 两处写字面, B/D 三处写取值口径); 三处 B/D 占位串无文本层 SC → 母 m4 |
| 探针 SC-19 常量黑名单 ↔ 字段 §2 集合 / 模板 placeholder | 字段 `:116` `` `{<org>/<repo>#<n>}` `` + §2 集合 | 探针 `:111` / `:500` 「黑名单逐字内容与姊妹 §3 的模板默认值 + §2 哨兵集合**同源**」; 字段 SC-9 `:545` 反向点名「探针 SC-19」 | **双向接住** (人肉同步义务已双侧成文) |
| 探针 ship 顺序 ↔ 字段纯函数 | 字段 `:247` 「它可先 ship 并全走层 2」 | 探针 `:70` / `:137` / `:169` 同义; 但 `:133` / `:162` / `:182` 使之不可实现 | **联合不可实现** → **接缝 C2** |

---

## (e) 本席核验为真、无 finding (下轮免重复)

1. **代码行号 (aria `d50f9c3`, 全部 `git show | sed -n` 实读)**: `phase1_gate.py` `:56` / `:210` (docstring 含 `"fetch_degraded"`) / `:283-294` / `:335` / `:791-802` (Step 9 注释块 + `push_res = resilient_push(`) / `:1032` / `:1173` / `:1191` (`required=True`, 无 `choices=`) / `:1230` `if args.linked_issue:` / `:1233-1235` / `:1236-1238` (`except` → `out["linked_issue_overlap"] = []`); `collision.py` `:46` / `:178` / `:230-234` (三参数) / `:265-266` / `:268` (`_TERMINAL = ("done", "abandoned", "unknown")`) / `:272-275` / `:278-279` / 函数体止于 `:292`; `claim_lifecycle.py` `:99` / `:178` / `:228` / `:244-256` (逐字段重建恰 11 个字段) / `:274` / `:377` / `:396-399` / `:425-427` / `:430`; `claim_schema.py` `:69` frozen / `:130` / `:165`; `identity.py` `:191` / `:222` / `:242` `return _hostname()` / `:244` `return uuid`; `constants.py` `:32` / `:36` / `:40-44` / `:50-51`; `track_id.py` `:61` / `:70-76`; `gc.py` `:324` / `:338-344` (`stale_ttl_seconds: int = SWEEP_TTL`); `release_gate.py` `:141` / `:225` / `:236-237`; `coordination_ref.py` `:119` / `:596` / `:800` (`bootstrap(repo_path=repo, push=False)`) / `:1367` (非强制 refspec); `reconcile.py` `:154-163`。
2. **SKILL.md / references**: `branch-manager:146-152` (标题逐字, 块内 `--phase B`); `phase-b-developer:86` / `:88` / `:91-93` / `:96-97` 注释跨两行 / `:98` skip 项 (母 rule6 #7 的行号勘正成立); `phase-d-closer:42` / `:51-52` / `:55` / `:56`; `spec-drafter:9-10` / `:125-162` 预览围栏 / `:139-140` 两行头部 / `:429` 链接 / 全部 `^#` 标题无 `A.0`; `phase-a-planner:9` / `:60-73`; `state-scanner/SKILL.md:119` / `:149` / `:168` 键集 / `:176` / `:178`; `layer-l-integration.md:15` / `:45` (`update_heartbeat()` 全 aria 只自命中); `coordination-ref-schema.md:129` + 5 条 `:133-140`; `coordination_probe.py:76-85` / `:140-141`; `config-loader/SKILL.md:134` / `:140`; `DEFAULTS.json` 无 `coordination`、`:124-128` `adaptive_rules`; `multi_remote.py:255-286`; `handoff_autofill.py:48-51` / `:403-407`; `audit-engine/SKILL.md:83` / `:85` / `:236-237`; `execution-modes.md:84` / `:113` / 144 行 / 插入锚点 `:89-90` `:118-119`; audit-engine 8 文件无 `scripts/` `tests/`; `fetch_gate.py:21` / `:23` / `:50-55` / `:108-128` / `:111-112`。
3. **主仓/环境**: SOT 模板 `proposal-minimal.md:3-5` 三行、`:20` `## Impact`、`:40` `## Template Usage Notes`, 两种字段拼写均 0 命中 (SC-6 / SC-7a baseline 必红成立); `.aria/state-checks.yaml` 11 条; `ab-suite/` 31 个 `.json`, 六个照跑套件实存, `audit-engine.json` 不存在; 三份在制 Spec 头部字段行 `cat -A` 逐字节合规 (过 E0 谓词 1-3 / E2 / E5), `changes/` 下两拼写行首命中 = 3 真 + 2 围栏内示例 (字段 `:95` / `:116`), 围栏排除谓词把后两条挡掉 (dogfood 自述成立)。
4. **跨 Spec 一致 (无 finding)**: 母 `:97` / 字段 `:14` / 探针 `:16` 对「语义母体 / 定义方」的分工三面一致; 母 §6「探针 ship 前无覆盖」↔ 探针 `:67` 对称; 母 SC-22 [4] 禁 `--phase B` 不会误红 (SC-22 绑定 `phase-a-planner` 与 `spec-drafter` 两文件, `phase-b-developer:92` 与 `branch-manager:148` 的 `--phase B` 都不在被断言文件内); 字段 §非目标「不改既有代码 / 新建两文件」与 Impact 已自洽; 探针「不改 state-scanner」与经 `sys.path` import 不矛盾; 母 §2.1b「不改写存量 ref」与 §6 末行、1A 后形态并存的已知限一致; 母 SC-2 ↔ SC-23 设计相容 (母「未做 #3」已自陈, 但 SC-23 baseline 标注见 母 M4)。
5. **1A 残留扫描**: 全文 `派生形` / `回落形` / `track_form` / `spec_slug` / `--spec-slug` / `force-legacy` / `零影响` 命中全部落在撤销说明、⛔ 行与审计轨指针; `K1`–`K4` 仅剩「随 1A 消失」句。审计轨 §6 (`:142-495`) 确含被移出的旧 §2.1 / SC-1·4 两层表 / K3 块 / 旧 §5 整节, 头部四条声明齐全。

---

## (f) 收敛判断

- **finding 落在 2026-08-30 新写文本上的占比**: Critical 3 条中 1.5 条 (母 C1 的 Impact 括注是新文; 接缝 C1 的母侧缺口是 R5 遗留, 字段 `:602` 的悬空引用是新文; 接缝 C2 是 2026-08-25 文本, 本轮未动); Major 11 条中 4 条 (母 M1 改名 / M2 / M3 是 SC-22 重写引入; 探针 M1 是 6i 扫描漏改), 其余 7 条全是 **R5 已点名而 v4 未回灌** 的项 (母 M5/M6/M7/M8, 字段 M1/M2, 以及 M4 这条 R5 未见、但与 R5 对 SC-2 的裁法同形的旧文)。⇒ 新文本引入的缺陷占比约 5.5/14 ≈ 39%, **低于** memory `marginal-return-negative` 的 1/2 拐点; v4 的九条修复本身是干净的 (本席逐条实读未见「修一处造一处」), 问题在于 **R5 三席 (comment-analyzer / factcheck / code-simplifier) 的 Major 有一半没进清账清单**。
- **是否同意「现状可进 A.2」**: **不同意, 但距离很近。** 三条 Critical 都是文本层动作: 接缝 C1 是两侧同批各改三处 (无设计变更); 母 C1 是把一个括注誊进 §2.5 / SC-9 / rule6 (a); 接缝 C2 需要 owner 在「字段纯函数是探针硬前置」与「探针先 ship 即降级为恒 not_established」之间点一下 (它改变的是 2026-08-23 拆分时成文的「均非阻塞前置」, 不是机制)。11 条 Major 里 10 条可单侧机械修, 只有 母 M1 (撤回 `Part A1` 改名) 需要执笔侧确认 R5/M2 的误读。
- **不建议再加通用审计轮** (与 R5 五席一致): 清账后只需一次「只看接缝 + 三张表」的定向核验; 三条 grep 不变量已绿, 建议再加第四条机械不变量「Impact 行里凡写『SC-NN 补/钉 X 臂』, SC-NN 行须含 X 的字面」—— 母 C1 正是它会抓到的形状。

---

## (g) counts

**3C / 11M / 13m** —— Critical: 接缝 C1 / 接缝 C2 / 母 C1; Major: 母 M1–M8 (8) + 探针 M1 + 字段 M1–M2 (2); minor: 母 m1–m6 (6) + 字段 m1–m3 (3) + 探针 m1–m3 (3) + 流程 m1 (1)。

**本席未修改任何被审文件; 唯一写入 = 本报告。** 全部行号可在主仓当前工作树 / aria `d50f9c3` 上按报告头的复核命令重跑。
