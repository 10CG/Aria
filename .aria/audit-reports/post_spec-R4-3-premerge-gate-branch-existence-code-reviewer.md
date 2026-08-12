---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — Spec A `premerge-gate-branch-existence` · seat: code-reviewer

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** (0C + 4M + 7m = 11) · `blocks_phase_b`: 2 条
本轮 findings 由 R3-fix 引入: **10/11 = 91%**

审视角度 (本席): 逐字核对 —— 末尾溯源表抽查回源 / `SC-A*` 号段无冲突 / 所有 file:line 属实 / 条款间自相矛盾。
**所有数字均本轮实跑, 命令原文随条附上。**

---

## 0. 先说结论形状

R3 的 14M **12 条真闭合、2 条只闭合了一半**; 10 条 minor **全闭合**。
本轮 4 条 major 里 **3 条落在 R3-fix 自己新写的结构上** (§非目标未同步 / 可达前提配方冲突 / R3-新定档块的两条行锚),
**1 条落在 R3 新增的 §交付义务** (O-1 的证据命令恒空)。
两条 `blocks_phase_b` **都是一句话可改的**: 删/换 `:844` 一个从句 · 给 `:641` 的配方加一个例外括号。

---

## 1. R3 的 14M 逐条回源 —— 「写下来 vs 闭合」

| # | R3 finding (席位) | 处置位置 | 我的复核 (实跑/实读) | 判定 |
|---|---|---|---|---|
| 1 | SC-M18 只清点四分之一 (BA) | 表 1 SC-M18 行 `:265` | 实跑四分量 `grep -cE 'still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除'` ⇒ `pre_merge_gate.py`=**2** · `SKILL.md`=**4** · `test_pre_merge_gate.py`=**3** · `.aria/config.template.json`=**0**, 与 Spec 写的 `2/4/3/0` **逐个相等** | ✅ 闭合 |
| 2 | BLOCKER 承载前提被证伪 (TL, blocks) | 全块重写 `:48-119` | 实读 `task-planner/SKILL.md:59-67` (路径 B / `:67` 「始终从 proposal.md 读取 `## Success Criteria` 章节」逐字命中) + 实跑归档 4 例, **4/4 都是 Level 2**, TASK- 计数 **31/21/19/28** 与 Spec 全等 | ✅ 闭合 (证伪比 R3 席位更强) |
| 3 | 出路 (i) 委派 §C.2.5 失明 (TL+CR, blocks) | `:92-104` 改为事实声明 | 实读 `SKILL.md:583-593` 六步 (`expected_sha = git rev-parse HEAD` → `verify_parity_post_push`) 与 `:194` 逐字「forward bump 或 **no-change** 或 first-time」⇒ 「未 bump = no-change = PASS」成立 | ✅ 闭合 (但见 M-4) |
| 4 | `SC-A-step` (c-含) 是 landmine (TL, blocks) | `:195-212` + SC 行 `:703` + §Impact `:896` | 三处口径已换成「本步作用域边界 + `#137`」 | ⚠️ **半闭合 → M-1** (§非目标 `:844` 仍命令写旧标注) |
| 5 | 三禁不含 `--pr-branch` (TL, blocks) | `:286-297` 升为类级 + `:703` (c-禁1) + `:901` | 三处措辞一致 (「不得含**任何**以 `--` 起头的 CLI flag 字面量」) | ✅ 闭合 |
| 6 | `SC-A14` 腿 2 恒绿 (TL+CR, blocks) | `:541-568` + SC 行 `:698` | 新判据在 `gate_check()` 返回值上跑 `s.encode("utf-8","strict")`, 不读 `sys.stdout` ⇒ 与 harness 捕获模式结构上无关; 换的是测量点不是不变量 | ✅ 闭合 |
| 7 | 「六键」枚举第四处落点 (TL) | `SC-A-note` (d) `:704` | 实读 `pre_merge_gate.py:241-246` docstring 确为第二份拷贝 (4 项枚举 + 「保持既有六键不变」); 且「各早退」/「分支」被源码换行拆开 ⇒ **抹空白规则确有必要** | ✅ 闭合 (残余 m-6) |
| 8 | 清点漏 B 侧 7 条行为型 SC (QA) | 表 1 `:266-270` | 实跑 `grep -c '^| \*\*SC-M' B/proposal.md` = **20**; 表 1 列出的号集 = B 的号集 (M1,M2,M3a/b/c,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13,M14,M15,M16,M17,M18) **一一对齐, 零遗漏** | ✅ 闭合 |
| 9 | BLOCKER 路由缺口 (KM, blocks) | `### 交付义务` 移入 `## Success Criteria` `:754-783` | 实跑 `grep -c '^### Key Deliverables' A` = **0** ⇒ `## Success Criteria` 确是路径 B 必读的唯一落点 (`DUAL_LAYER_SPEC.md:90-93` 实读确认三项穷举) | ✅ 闭合 |
| 10 | 「20/24」实为 19/24 (CR) | `:588-607` 动态实测 | **我独立复跑** `sys.settrace` 探针 (记录每次 `gate_check` 是否执行到 `pre_merge_gate.py:356`): `tests run: 46 · dynamic gate_check calls: 24 · reached: 19 · NOT reached: [282, 301, 311, 321, 524]` —— 与 Spec **逐字节相同** | ✅ 闭合 (本轮最强的一条) |
| 11 | `SC-A14` 腿 2 (CR, 同 6) | 同上 | — | ✅ 闭合 |
| 12 | `SC-A10c` 放错例外集 (CR, blocks) | 移入适用集 `:641` + 理由 `:651-662` | 理由段对 (要让 precheck 失败**必须** mock backend, `base.py:79-85` 逐字「Default: always (True, "")」实读确认) | ⚠️ **半闭合 → M-2** (适用集的成员定义与 mock 配方与它冲突) |
| 13 | 出路 (i) 失效委派 (CR, 同 3) | 同上 | — | ✅ 闭合 |
| 14 | 漏 B 的任务级预写量 (CR) | 表 1 末段 `:275-279` | 实读 `B/tasks.md:85` (TASK-010「既有 24 处」) · `B/detailed-tasks.yaml:488` (「显式传 main_branch 的 0 处」) · `B/tasks.md:122` (TASK-021「基线 **111** 的差值」) —— **三条引文逐字属实、行锚全中** | ✅ 闭合 |

**10 条 minor 全部闭合** (抽查: 起点锚「首个」—— 实跑 `grep -n '^\*\*执行流程\*\*:' SKILL.md` = `238` `582` ✓ / `SC-A-note` 区块边界 `:278`–`:280` —— 实读 json 围栏止于 `:277`、`**配置参数**:` 在 `:281` ✓ / 45 席 —— 实跑 `ls .aria/audit-reports/ | grep mainbranch-failclosed | grep -vE 'aggregate|audit-trail' | wc -l` = **45** ✓ / §版本 7 行列举 —— 实跑 `grep -rn 'gate_check(' aria/ --include=*.py` 去掉测试文件后**恰 7 行**且逐个对上 ✓ / 授权口径 —— `D-a` / §Impact 外部行 / Follow-up 表三处已统一 ✓)。

---

## 2. 本轮 findings

### M-1 (major, blocks_phase_b) §非目标 `:844` 仍命令写 R3 判定为 landmine 的那条标注 —— 与三处新口径直接冲突

- **实读** `proposal.md:844` 逐字: 「由此产生的「新步骤用 `<MAIN_BRANCH>` 而步骤 3 硬编码 `main`」这条不一致, 按 §残余暴露在**该步骤处逐字标注**;」
- 而 §残余暴露 `:205-212` 已把标注对象换成「**本步骤自身的作用域边界**」, `SC-A-step` (c-含) `:703` 的机械腿**只剩 `#137` 一个 token**, §Impact `:896` 也已改成「标注本步自身的作用域边界」。**三处改了, 第四处没改** —— 正是本 Spec 自己反复援引的 `fix-the-class`。
- **怎么会红**: Phase B 若照 `:844` 执行, 在新步骤正文写下「步骤 3 仍硬编码 `main`」——`SC-A-step` 三禁不禁 `步骤 3`、(c-含) 只查 `#137` ⇒ **18/18 全绿**; 而 B 的 D1 落地后 `SKILL.md:243` 那条命令即被收敛 (B `SC-M1` 期望 `grep -c 'aether ci status' SKILL.md` = 0, 我实跑今日 = 4) ⇒ 随 plugin 分发给第三方一句**同页面即可证伪的假话** (违反规则 #3) —— 这正是 R3 判 `blocks_phase_b` 的那条缺陷本体。反向也坏: 若实现照 §残余暴露 只写作用域边界, 则 `:844` 这条指令**无对应产物**, 两条指令无法同时满足。
- **修法**: `:844` 改为「按 §残余暴露 在该步骤处标注**本步作用域边界**并指向 `#137`; ⛔ 不得标注步骤 3 的当下状态」。

### M-2 (major, blocks_phase_b) 「可达前提」把 `SC-A10c` 收进适用集, 但适用集的**成员定义**与**mock 配方**都与 `SC-A10c` 相反

- **实读** `:635-642`: 「**凡断言「核验确实发生了」的 SC**, 其 fixture 必须显式提供一个可解析的 CI backend (mock backend: `probe()`→`True` · **`precheck()`→`(True, "")`** · …)」, 适用集 (11 条) 末位 = 🔴 `SC-A10c` (R3 移入)。
- **实读** SC 行 `:696`: 「**SC-A10c** | 负控: **precheck 失败** (`:345`) 早退 | 同上 (六键不变、无 `gate_error`, 且 `assert ls-remote 未被调用`)」。
- 两条**同时为真不可能**: 成员定义说它「断言核验确实发生了」(它恰恰断言核验**没**发生), 配方说 `precheck()`→`(True,"")` (它要求 `(False, …)`)。上一版把它放例外集时**带着括号注**「(precheck **必须**返 `(False, …)`)」(实读 R3-fix 前版本 `:422`), R3 移入时**把这半句丢了** —— `assertion-swap-severs-link` 的又一实例。
- **怎么会红**: 实现者按适用集配方给 `SC-A10c` 配 `precheck()`→`(True,"")` ⇒ gate 不在 `pre_merge_gate.py:345` 早退 ⇒ 核验执行 ⇒ `assert ls-remote 未被调用` 失败 ⇒ **完全正确的实现下 `SC-A10c` 恒红**; 按 SC 行实现则违反适用集条文 ⇒ **两个独立实现者得相反结果** (`spec-underdetermination`)。
- **修法**: 适用集里给 `SC-A10c` 加括号例外「(⚠️ 唯一例外: 本条须 `precheck()`→`(False, …)`; 打桩 backend 这一点相同, 配方只差这一项)」——一句话。

### M-3 (major) R3 新写的「定档依据」块两条 SOT 行锚**都不落在被引文本上**, 且两处实际内容都是 **Level 1**

- `:10` 逐字「照 SOT `spec-drafter/LEVEL_GUIDE.md:26` 的 **Q2 三腿**走一遍」。**实读** `LEVEL_GUIDE.md:26` = 「`│      ├─ YES ──────▶ LEVEL 1 (Skip)     │`」; **Q2 在 `:29`** (`│      └─ NO ──▶ Q2: 是否架构变更/跨模块/Breaking?`)。
- `:15` 逐字「(`standards/openspec/project.md:116` 逐字「2 | Minimal | Medium features (1-3 days) | proposal.md」)」。**实读** `project.md:116` = 「`| 1 | Skip | Simple fixes, typos | No spec needed |`」; **被引的 Level 2 行是 `:117`**。
- 两条都是 **R3-fix 新增** (实跑 `grep -n 'project.md:116\|LEVEL_GUIDE.md:26'` 于 `ff847fb^` 版本 ⇒ 零命中)。
- **为什么这条不只是排版**: 该块的立论本体是 memory `exact-exception-condition` 的「**字段级匹配, 不是精神匹配**」, 而它自己两条锚都只做到了精神匹配; 更糟的是复核者按锚回源看到的**恰好都是 Level 1 的行**, 对 `D-c` (owner 要裁的 Level 2 vs 3) 是**反向误导**。这也是本 Spec 家族第四次同形复发 (55/45 · `:337`→`:335` · SC-M18 操作数 · 本条)。
- **怎么会红**: 任何按行锚复跑 `sed -n '26p' LEVEL_GUIDE.md` / `sed -n '116p' project.md` 的复核者拿不到被引文本 ⇒ 定档依据不可复核。**结论 (Level 2) 我复核成立** —— 改的是锚, 不是结论。

### M-4 (major) §交付义务 O-1 的 gitlink 证据命令 `git diff --submodule=short` **在提交后恒空**, 对它唯一要防的方向没有区分力

- **实读** `:772` 逐字: 「逐项贴出 `git show --stat` / `git diff` 证据; **gitlink 一项须贴 `git diff --submodule=short` 显示指针前后 SHA**」。
- **实跑**: 本仓 `aria` gitlink 在 `fb5ed36` 被 bump 过、工作树干净 ⇒ `git diff --submodule=short -- aria | wc -l` = **0**。而「从未 bump」的仓上同一命令同样是 **0 行**。⇒ **健康态与病态输出相同**。
- 与本 Spec 自己的判据一致性: `:104` 逐字「O-1 今日没有任何机械兜底, 本 Spec 不假装它有」——正因如此, **人工判据是这条义务的最后一道**, 而它选的量恰好不区分。
- **怎么会红 / 怎么会假绿**: D.2 执行者贴出 0 行输出 ⇒ 与漏 `git add aria` 的证据**逐字节相同** ⇒ 打勾通过 ⇒ 落到 B 侧 R4 `TASK-017` 那个 Critical 的形状 (orphaned gitlink)。
- **修法**: 换成 **`git show --submodule=short <release-commit> -- aria`** 或 `git diff --submodule=short <BASE_SHA>..<HEAD> -- aria` (我实跑前者对 `fb5ed36` 有非空输出且含指针 SHA)。这与同一格里另一半用的 `git show --stat` 基准一致 —— **同一格内两个命令用了两种基准**, 只有 `git show` 那个在提交后有效。

### m-1 (minor) 方向 2 归纳 `:314-317` 的配平算错, 且 `SC-A-step` 被计了两次

- 逐字: 「18 条中 **B 落地会打爆的是 3 类** … 另有 **1 条** (`SC-A-step (a)(b)`) … **其余 14 条**实测不受影响」。
- 按本 Spec 自己钉的计数法 (`:251` 「总体 = A 本 Spec SC 表的全部表行 (`grep -c '^| \*\*SC-A'` ⇒ 18)」, 我实跑 = **18** ✓): 受影响的 **SC 行** = `SC-A10` · `SC-A10b` · `SC-A10c` · `SC-A-step` · `SC-A-baseline` = **5** ⇒ 不受影响 = **13** (`SC-A6/A13/A-zero/A7/A8/A11/A14/A-order/A-cwd` 9 条 + `SC-A-cli` + `SC-A-doc` + `SC-A-note` + `SC-A-sc22`)。
- 「3 类 + 1 条 + 14」这个分割把**类**与**行**混着数, 且 `SC-A-step` 同时进「3 类」(c-含) 与「另有 1 条」((a)(b))。
- **怎么会红**: 任何复跑 `18 - 5` 的人得 13 ≠ 14。**表本体的覆盖我核过是完整的** (10 行覆盖 18 条 SC, 无重无漏) —— 错的只是归纳句。

### m-2 (minor) BLOCKER 自查留痕的「实跑得 4」今日实跑得 **5**, 且与本 commit message 自陈的数不一致

- 逐字 `:73`: 「初稿写的是不带 `^` 的 `grep -c '### Key Deliverables'`, 而本段正文自己就含这个串 ⇒ **实跑得 4**」。
- **实跑今日**: `grep -c '### Key Deliverables' openspec/changes/premerge-gate-branch-existence/proposal.md` = **5** (`grep -c '^### Key Deliverables'` = **0** ✓ 那半是对的)。
- `ff847fb` 的 commit message 自己写的是「实测: 行首锚定 0, **非行首 5**」⇒ **文档与它自己的提交说明不一致**。
- 这正是它在同一段落里批评的形状 (「照它复跑的人会得另一个数」), 是 55/45 那条的第二次复发。非承重 (只作留痕), 故 minor。

### m-3 (minor) `:196` / `:304` 的 B 侧行锚 `:156` 不含被引文本 (实为 `:158`)

- 逐字 `:304`: 「**归属已成文在 B 侧**: B `:156` 逐字「折叠块须**补上 §3 新增的分支存在性核验步**」」; `:196` 另逐字「我本轮**实读** B `:156`/`:161` … 复核成立」。
- **实读** `B/proposal.md:156` = 「`<details><summary>helper 内部算法 (供理解与排障, ⛔ 不要手工执行)</summary>` … `</details>`。」; 被引的那句在 **`:158`** (我实跑 `grep -n '折叠块须'` ⇒ 唯一命中 `158`)。`:161` 的引用**成立** (该行确含「正落在本节要整体折叠的 1-5 步之内」)。
- **内容属实、结论不变**, 但「我实读了」这句被自己的锚证伪; 而 `SC-A-step (a)(b)` 的「不为它编造断言」这个处置**正是靠这条归属撑住的**。R3-fix 新引入 (前版无 `:156` 引用)。

### m-4 (minor, 非本轮引入) `:746` 引「B 侧 `:358-361`」, 实为 B 的 SC-M12/M13/M14/M15 表行

- 逐字 `:746`: 「且 B 侧 `:358-361` 早在 post_planning R3 就把同一句更正过, A 承接时把更正丢了」。
- **实读** `B/proposal.md:358-361` = `SC-M12` / `SC-M13` / `SC-M14` / `SC-M15` 四行 SC 表; 被引的那条更正 (打桩边界「上一版此段有两处自相矛盾」) 在 **`:366-369`**。
- 承自 R2-fix 版本 (实跑 `grep -n '358-361'` 于 `ff847fb^` ⇒ 命中), **不是本轮引入**; 但今日仍不落地, 属 `reporter-miscite` 未清。

### m-5 (minor) `:927` 逐字「两处都不复述清单本体 —— 清单本体的唯一 SOT 是本行」被同版本自身证伪, 且三份拷贝已经不一致

- **实读三处**: §Impact `:917` (带 「i18n README (**仅正文实质变更才重译**, #140 B 档)」) · §交付义务 O-1 `:772` (复述 5 文件全名 + gitlink + VERSION + badge + i18n, **无 #140 限定**) · 文首 BLOCKER O-1 `:88` (复述简版)。
- 讽刺点: 本 Spec 在 `:621` 刚写下「**两处名单同步不了就不该有两处名单** ⇒ 名单唯一 SOT = 打桩边界表, 本节只引用不复制」, 同一版本里又造了三份发版清单。
- **怎么会红/错**: A.2 路径 B 真正读到的是 `:772` 那份 (这正是 R3 移入的理由) ⇒ 出的 TASK 会写「翻译 i18n README」而丢掉 `#140 B 档` 的「仅正文实质变更才重译」限定 ⇒ 无谓重译四语 README。危害小, 故 minor。

### m-6 (minor) `SC-A-note` (d) 的 token 里 `…` 未定义为通配还是字面 —— 与同一条 SC 刚钉死的解析规则不对称

- 逐字 `:704`: 「先 `re.sub(r'\s+', '', 区块)` 抹掉全部空白再匹配, token 相应写作 `各早退分支(…)保持…六键不变` / `gate_error` / `main-branch` / `无path_coverage`」。
- **实读两个操作数**: `SKILL.md:279` = 「…保持**六键不变**」; `pre_merge_gate.py:245-246` docstring = 「…保持\n**既有**六键不变」⇒ 抹空白后两串**不同** (`保持六键不变` vs `保持既有六键不变`)。
- **怎么会红**: 把 `…` 当**字面** (U+2026) 实现 ⇒ 两个操作数都零命中 ⇒ (a)(d) **与被测实现无关地恒红**; 当**通配**实现 ⇒ 正常。同一条 SC 为「抹空白」写了三行理由钉死规则, 却给 `…` 留了同类的欠定 (`spec-underdetermination`)。

### m-7 (minor) `SC-A-step (a)(b)` 的诚实标注**缺一条时序限定** —— 兄弟位置 (`SC-A-baseline`) 已有的处置没推广过来

- `:304` 的处置「A 此侧无法断言, 且不为它编造断言」**我判定是对的** (见 §3 对执笔方预判 ① 的回答), 但它只回答了「A 现在能不能断言」, 没回答「**A 先 ship 后, 已落地的 (a)(b) 断言在 B 落地当天怎么办**」。
- 对照: 同一张表里 `SC-A-baseline` 遇到同形问题时给了可执行处置 (`:310` 逐字「111 = 基线 `af87cae` 且 B 未 ship 时的量; 若 B 先 ship, 须以 B ship 后的实测数重定基线」)。
- **怎么会红**: A 先 ship ⇒ (a)(b) 作为持久测试留在套件里 ⇒ B 的 D1 把步骤 1-5 折进 `<details>` (B `:154`/`:161`), 若折叠后不保留行首 `N.` 编号, 提取序列为空 ⇒ (a)(b) 对**完全正确的 B 实现**红, 且无人有权删它。补一句时序限定 (与 `SC-A-baseline` 同款) 即可。

---

## 3. 对执笔方三处自我预判的复核 (owner 要的那个区分)

**① 表 2 中它明确拒绝断言的 `SC-A-step (a)(b)` 行 —— 判定: 不是「修错了」, 是「本就只能诚实标注」, 但标注不完整。**
理由 (实证): (a)(b) 的操作数是 `SKILL.md` 中 `**执行流程**:` (`:238`) 与 `**Subprocess 调用规范**:` (`:257`) 之间的**行首步骤编号序列** (我实跑该区间 = `1. 2. 2.5. 3. 4. 5. 6.`); B 的 D1 会把这段整体折进 `<details>` (B `:154` 标题 + `:161` 逐字「正落在本节要整体折叠的 1-5 步之内」), 而**折叠后的行首形态取决于 B 尚未写出的文本**。任何在 A 侧写死「折叠后也应如何」都是钉合成 fixture (`gate_tracks_reality_synthetic_fixture`)。⇒ 拒绝断言是**正确**处置, R4 不该在这上面判它错。
**但**它漏了可机械化的那一半 —— 见 m-7: 同文件的 `SC-A-baseline` 对同形问题给了时序限定, 这条没给。**这是「不完整」, 不是「修错」。**

**② §交付义务的「完成判据」是人工判据 (贴 `git show --stat`) —— 判定: 人工这件事本身不是缺陷; 但 O-1 那条人工判据没有区分力 (M-4)。**
「六项全无机械闸门」我逐条复核成立: O-1 (C.2.4.5 判 `no-change` = PASS `:194` + C.2.5 核的是 `expected_sha` 到达性 `:583-593` + `m6-version-badge-match` 只比 badge↔`plugin.json`) · O-2/O-3/F-1..F-3 (无闸门读 proposal 散文 / 仓外写动作)。**在造不出真量时诚实写「没有」是正确的**, 不该判它错。
**要打的是另一件事**: 既然只剩人工判据, 那条判据必须能区分健康态与病态, 而 `git diff --submodule=short` 在提交后**两态同为空** (实跑 0 行)。⇒ **打的是「这条人工判据选错了量」, 不是「你怎么没机械化」。**

**③ `SC-A-note` (d) 的 token 与语言绑定 —— 判定: 语言那一半确已收口, 但 token 里留了新的欠定 (m-6)。**
`:495-501` 明文「须沿用该段落既有的中文措辞 / 把该段改写为英文不在本 Spec 授权范围内」+ 实读 `:243-246` 确认该段今日本就是中文 ⇒ 语言绑定风险已收口 ✅。残余在 `…` 的语义未定义 (见 m-6), 与语言无关。

---

## 4. 对四条「不同意」与双向清点表的复核

**「第三条路」(换的是标注什么, 不是是否标注) —— 我判定: 成立。**
新标注句「本步只核验 `main_branch` 在 `<remote>` 上存在, **不保证后续步骤查询的是同一个分支**」陈述的是**本步契约**, 不是别处缺陷的当下状态 ⇒ B 的 D1 收敛两份实现后该句**仍为真** (本步确实不承担跨步骤一致性)。`#137` 退化为溯源指针有本文件内先例, 我实读确认: `SKILL.md:242` 逐字含 `(v1.65.0+, aria-plugin #122; …)`、`:253` 含 `#126` —— issue 关闭后引用仍合法。
**但这条路只在提出它的那一节落地**: §非目标 `:844` 仍写着旧标注 (M-1)。⇒ 论证成立, **贯彻没做完**。
另: (c-含) 机械腿只剩 `#137` 一个 token, 「措辞是否真的陈述了作用域边界」无机械锚 —— 文档已如实声明, **我同意不为它编造第二个量** (编出来的量会在 B 落地后变成新的 landmine)。

**表 1 (20 行) 有没有数漏 —— 没有。** 实跑 `grep -c '^| \*\*SC-M' B/proposal.md` = **20**, 且表 1 列出的号集与 B 的号集**逐个对齐** (`SC-M3` 确是 `SC-M3a/b/c` 的前缀伪命中, B `:473` 自己也写着「按编号计 18 条 / 按 SC 表行计 20 行」)。三条任务级预写量的引文与行锚**逐条实读命中**。
**表 2 (18 条) 有没有数漏 —— 集合完整, 只有归纳句配平错 (m-1)。** 10 个表行覆盖 18 条 SC, 无重无漏。
**我特意追了一类候选遗漏并否掉了它**: B 的 `tasks.md:85` (`test_sc12_default_true_lock` `:663`) 与 `detailed-tasks.yaml:344/:500` 里有指向 `test_pre_merge_gate.py` 的**行锚**, A 扩 `_ProbeCacheResetMixin` (`:59-80`) 会把它们全部打漂 —— 但 B 已有**全局行锚约定** (`tasks.md:14` + yaml 逐字「以基线 SHA 为准 … 按函数名内容锚重定位, 不得按行号核」) ⇒ **不构成漏项, 不报**。

---

## 5. 抽查回源: 末尾溯源表 (`:986-1008`) 22 行中我实跑/实读 21 行

全部命中, 逐条列出命令与结果:

| 溯源表行 | 我的验证 | 结果 |
|---|---|---|
| 插入点 5 锚位 / 8 行号 | `sed -n '324,370p' pre_merge_gate.py` | `:328` `:338` `:344` `:345` `:356` `:357` `:358` `:366` **8/8 命中** ✅ |
| `SKILL.md:255` = `fail` 走 `raw_message` | 实读 | 逐字命中 ✅ |
| `SKILL.md:279` = 四类早退保持六键 | 实读 | 括号内**恰 4 项**, 不含 `main-branch` ✅ |
| `:259`/`:260` 重试 + 退出码 (含 `127 → no_ci_fallback`) | 实读 | 逐字命中 ✅ |
| 锚定 pattern 仍 fail-OPEN | **受控裸仓复跑**: `git ls-remote --heads <bare> 'refs/heads/mast*'` / `'refs/heads/m[a]ster'` / `'refs/heads/maste?'` | **三条全部命中 `refs/heads/master`, RC=0** ✅ |
| `ls-remote` 零命中亦返 rc=0 | 同裸仓 `... develop` | **零行 + RC=0** ✅ |
| `--exit-code` 无命中返 rc=2 | 同裸仓 `--exit-code ... develop` | **RC=2** ✅ |
| `test_sc22` patch 全局 + `:723` 未传 `main_branch` | 实读 `:710`/`:718`/`:723` | 全中 ✅ |
| `gate_error` 全仓零消费者 | `grep -rn 'gate_error' aria/ \| wc -l` | **0** ✅ |
| `_run_with_retry` 硬绑 binary/只捕 Timeout/无 cwd/`text=True` | 实读 `aether.py:164-187` | 四项全中 ✅ |
| `test_ci_backends.py` 零命中 `_run_with_retry` | `grep -c` | **0** (全 `tests/` 亦 0) ✅ |
| 测试基线 111 | `python3 -m pytest -q tests/` | **111 passed** (46+25+40) ✅ |
| `SKILL.md:243` 硬编码 `--branch main` 且是编号步骤本体 | 实读 | 逐字命中 (步骤 `3.`) ✅ |
| 本仓 `ls-remote --heads origin main` | 实跑 | **零行 + RC=0** ✅ |
| `workflow-runner` 零命中 `pre_merge_gate.py` | `grep -rc` | **0**; 不带 `.py` 另得 3 处 (`SKILL.md:342` `:373` `gate_state_helper.py:37`) —— 与 `:183-187` 的 R2 更正**逐字相符** ✅ |
| v1.65.0 先例: 照跑 AB + 补步骤 2.5 | `CHANGELOG.md:181` (在 `## [1.65.0]` 段内, `:150` 起) 逐字「Rule #6 照跑 AB (3 eval × with/old/without 三臂」 + `SKILL.md:242` | 双中 ✅ |
| `issubclass(UnicodeDecodeError, OSError)` | 实跑 | **False** ✅ |
| `ls-remote` 指向不存在路径 ⇒ 128 | 实跑 `/tmp/does-not-exist-repo-xyz` | **RC=128** ✅ |
| 24/24 既有调用不传 `main_branch` | `grep -c 'gate\.gate_check(' ` = **24** / `grep -c 'gate\.gate_check(.*main_branch'` = **0** + 六处多行调用实读 | ✅ |
| `_ProbeCacheResetMixin:59-80` | 实读 | 起止**逐行对齐** ✅ |
| 真实调用点 25 | 实跑 (7 行去掉 5 处 docstring 提及与 1 处 def) | **24 + `:435` = 25** ✅ |

**唯一未独立复跑**: 「锚定 pattern 仍 fail-OPEN」的**前两次历史实验**本身 (我用第三次同款受控裸仓复现了结论)。

---

## 6. `SC-A*` 号段冲突复核 (本席专项)

- `grep -rn 'SC-A[0-9-]' aria/` ⇒ **零命中** ⇒ 与既有测试无冲突 ✅
- 既有测试的 SC token 实跑 = `SC-1 SC-11 SC-14 SC-18 SC-19 SC-2 SC-22 SC-23 SC-27 SC-4 SC-9` (纯数字段) ⇒ 与 `SC-A*` 正交 ✅
- 与 B 的 `SC-M*` 正交 ✅
- 表内自身: 18 行**无重号**; 可达前提配平 `11 + 2 + 3 + 2 = 18` 与打桩边界表 `6 + 1 + 2 + 4 + 3 + 2 = 18` **两套分区各自完整且互不矛盾** ✅ (唯一冲突是 M-2 的配方, 不是号段)

---

## 7. 评估

**是否可以继续?** 需要**两处一句话的修复** (M-1 `:844` · M-2 `:641`), 其余 2 major + 7 minor 可随 Phase B 首批 commit 带走或交 owner 裁量。
**理由**: Critical **连续三轮归零**, 且本轮**最承重的两个量 (19/24 动态实测 · 20 行 SC 清点) 我独立复跑逐字节相同** —— 这是三轮以来第一次「承重数据经得起对抗复跑」。残余 major 全部是**局部未同步**而非结构错误; 引入率 (10/11) 仍高, 但**引入的东西变轻了** (本轮 major 无一是「恒红/假绿的机械判据」, R3 有 3 条)。
