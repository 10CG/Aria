---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T01:10:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — knowledge-manager 席位报告

被审对象: R2-fix 后的 A.2 产物 (commit `0dd26ce` 时的工作树, `git status --porcelain openspec/changes/premerge-gate-mainbranch-failclosed/` 全程零输出, 只读)。

镜头: Rule #5/#6/#9/#10 合规 / Level 3 三件套 / follow-up 可证伪性 / `config-loader` 的 Rule #6 三件套是否真补齐 / 发版同步面。

已读: R2 aggregate、R1/R2 本席原始报告、R3 已完成的 tech-lead / backend-architect / qa-engineer 三份报告 —— 用于避免重复劳动、并对其中落在我镜头内的条目做**独立回源**(非采信)。

## 投票

**VOTE: REVISE** — 0 Critical, **2 Major**(1 条全新、1 条与 tech-lead M4 交叉确认但补了独立证据与一个新推论), 1 Minor。**verdict = PASS_WITH_WARNINGS**(按本席自身发现的裸枚举: 0C+≥1M)。

不构成本席自己的 FAIL, 但我确认 tech-lead 报告的 1 Critical + blocks_phase_b ×5 仍然成立(见下"R2 闭合"一节的交叉复核), 故**不应仅凭本席结论推进 TG-3/Phase C**。

---

## 一、R2 的 1C + ~13M 逐条回源 —— 仅限落在我镜头内、且我能独立贡献证据的条目

不采信"已修"的声称。方法: 实读现版 + 实跑命令 + 与其他三席 R3 报告的证据做**独立复算**(不转抄结论)。

| R2 条目 | 现状(我镜头内的核验) | 判定 |
|---|---|---|
| **M2**(config-loader Rule #6 归档缺口, 我 R2 原始发现之一, tech-lead R2 独立命中) | 实读 `proposal.md:322-333`、`tasks.md:107`、`detailed-tasks.yaml` TASK-015: 判据表第三行三件套(点名行为/SC-M17/TASK-019(8))**三样全给**, 且 `TASK-015.dependencies` 实读含 `TASK-019`(issue 必须先于归档存在, 非事后补票)。**逐字核对 SOT** `standards/conventions/skill-benchmark-exemption.md`: proposal 引"第三行措辞是「典型: authoring 向导」"与 SOT 原文逐字一致(`… (典型: authoring 向导 —— 给 spec 作者读的处方, 而套件测的是 skill 运行时行为)`); SC-M17 的可证伪性满足 SOT §3.2"回退必转红"(还原 TASK-020 的删除 ⇒ 计数从 0 变回 2)。 | ✅ **真闭合**(非文字游戏) |
| **M10 / 我的 R2 F-1**(`tasks.md:103` "TASK-019 已纳入" 承诺不成立) | 实读 `tasks.md:141` 已裁段落改口为"TASK-019 第 (7) 项", 且 `detailed-tasks.yaml` TASK-019 verification 真有 `(7) standards/openspec/project.md ... 转记 standards 维护者` 一条, 标题同步改"8 项"。`grep -c` 双文件核对(7)(8)两项均在正文与 yaml 两处一致存在。 | ✅ **真闭合** |
| 我的 R2 F-2(`main_branch_resolved` 孤立术语) | `grep -rn "main_branch_resolved" .` 全目录零命中(已从 TASK-019 (3) 删除, 与 `tasks.md` 同步改口)。 | ✅ **真闭合** |
| **M3**(8 个发版同步面文件全无 task、全不在 scope, tech-lead R2 原始命中) | `scope_repos` 两侧核实已补: `aria` 侧 5 文件(`plugin.json`/`marketplace.json`/`VERSION`/`CHANGELOG.md`/`README.md`) + `Aria` 侧 4 文件(`VERSION`/`README.md`/`README.{ja,ko,zh}.md`) 均在 `detailed-tasks.yaml:9-20` 与 `:36-45`, `TASK-017.deliverables` 逐条列出同一批文件。**但**: 实跑 `grep -rniE 'gitlink|子模块指针|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/` = **零命中**, 而 `CLAUDE.md:81` 逐字「发布同步面: aria 子模块 5 文件 + **主仓 gitlink** + 主仓 VERSION + root README badge + i18n README」把「主仓 gitlink」列为与「aria 子模块 5 文件」并列的独立一项 —— **这与 tech-lead R3/M4a 的发现一致, 我独立复算确认成立**(见下 Finding K2)。 | ⚠️ **半闭合**(内容面改善, 但仍缺 canonical 清单的一项, 且下方 K1 表明连"已列入的那 8 项"的**执行时序**也未收口) |

其余不在我镜头范围的 R2 条目(§6.1 插入点的代码承重理由、SC-M14/16 的红窗真实性、xcheck.py 拒绝能力细节)已由 tech-lead / backend-architect / qa-engineer 三份 R3 报告分别核验, 本席不重复劳动, 仅在下方"三、机械检查评估"一节补一个**三份报告都未覆盖的角度**。

---

## 二、本轮新发现

### Finding K1(**Major, 新发现, 未见于其余三席 R3 报告**)—— `TASK-017`(发版同步面/版本 bump)缺一条对 `TASK-021`(终局全量收口)的依赖边, 合法拓扑序下可在**未验证完成**时就把版本号钉成 "已发布"

**locator**: `detailed-tasks.yaml` TASK-017 `dependencies`(现为 `[TASK-006, TASK-020]`)· 对照 TASK-021 `dependencies`(`[008,009,010,011,012,013,014,020]`)

**实跑(全程只读, `git status --porcelain` 核验零改动)**:

```bash
$ python3 - <<'EOF'
import yaml
d = yaml.safe_load(open("detailed-tasks.yaml"))
tasks = {t["id"]: t for t in d["tasks"]}
def ancestors(tid):
    seen=set(); stack=[tid]
    while stack:
        n=stack.pop()
        for dep in tasks[n].get("dependencies", []):
            if dep not in seen: seen.add(dep); stack.append(dep)
    return seen
anc17 = ancestors("TASK-017")
print(sorted(anc17))
print("TASK-021 in it?", "TASK-021" in anc17)
print("TASK-013 in it?", "TASK-013" in anc17)
EOF
['TASK-001','TASK-002','TASK-003','TASK-004','TASK-005','TASK-006','TASK-007',
 'TASK-008','TASK-009','TASK-010','TASK-011','TASK-014','TASK-020']
TASK-021 in it? False
TASK-013 in it? False
```

且用 Kahn 拓扑排序实证一条**合法**执行序(未穷举全部, 仅证明存在性):

```
...TASK-014, TASK-016, TASK-018, TASK-019, TASK-020, TASK-017, TASK-021, TASK-015
```

`TASK-017` 排在 `TASK-021`(与 `TASK-013`)**之前**, 且这是拓扑合法的(`TASK-017` 一旦 `TASK-006`+`TASK-020` 完成即"ready", DAG 不阻止它提前执行)。

**它怎么会红**: `TASK-017` 的动作是把 `aria/.claude-plugin/plugin.json` bump 到 MAJOR(v2.0.0)、写 `CHANGELOG.md` 条目、改 README badge —— 即**向外界声明"这个 v2.0.0 已经完成并可用"**。而 `TASK-021` 是本 Spec 自己在 R2-fix 里新造的"终局全量收口"，其存在理由逐字是"不接受「应该绿」的声称"、"逐条贴实跑输出"。若实施者按上述合法拓扑序执行(先 `TASK-020` 满足了 `TASK-017` 的依赖门槛, 就先做 `TASK-017`), 则:

1. `plugin.json`/`CHANGELOG.md` 已经声明 v2.0.0 shipped 的那一刻, `TASK-013`(SKILL.md 的 `:267` schema 增 `gate_error`、`:270` 示例、`:279` 四类早退注记同步)**尚未发生** —— 即代码/文档层面 v2.0.0 真正应该有的样子还没落地, 但版本号已经先声明了它存在(直接撞 CLAUDE.md 不可协商规则 #3「文档与代码必须同步更新」);
2. `TASK-021`(全部 17 条 SC 逐条复核 + `pytest` 零失败)尚未跑 —— 若随后 `TASK-021` 真的抓到一条红(这正是它被造出来要抓的场景, 例如 R2-fix 自己在 TASK-014/SC-M16 上就留了这一类缺陷, 见 tech-lead C1/M1), 需要回头修复的将是一个**版本号已经声明"完成"之后**才被发现的缺陷 —— 与本 Spec 通篇反复申明的纪律("不接受应该绿的声称"、"红窗必须先看到")在"发版"这个最外部可见的动作上恰好豁开一个口子。

**归因(`introduced_by_r2fix`)**: `TASK-021` 在 R1-fix 版本中**不存在**(`git show 6818773:.../detailed-tasks.yaml | grep -c TASK-021` = 0), R1-fix 版 `TASK-017.dependencies` 只有 `[TASK-006]`。R2-fix **新造了 TASK-021**, 并把它接到 `TASK-015`(`dependencies += TASK-021`, 理由是"AB 跑的 SHA 必须是 ship 的 SHA")——这条推理完全正确, 但**没有推广到 `TASK-017`**, 而 `TASK-017` 是比 `TASK-015` 更需要这条边的任务(`TASK-015` 声明的是"这次 AB 测的是哪份代码", `TASK-017` 声明的是"这份代码已经发布"), **典型的"只修实例(TASK-015)不修类"**(R2 诊断的原话形状, 在 R2-fix 自己新造的补救机制里复发一次)。⇒ **`introduced_by_r2fix: true`**。

**与 tech-lead M5 的区别(避免被误判去重合并)**: tech-lead 的 M5 说的是**已有边的 group 标签方向倒置**(7 处, 例如 `TASK-021(TG-1)` 依赖 `TASK-020(TG-3)`), 是"标签与拓扑不一致"的问题。K1 说的是**该有而没有的边**——`TASK-017` 与 `TASK-021` 之间目前**没有任何边**(正向反向都没有), 后果也不同: M5 的后果是"组序执行会撞见依赖未满足"; K1 的后果是"版本声明可以在验证完成前发生"。两者需分别修(K1 的修法只需一行: `TASK-017.dependencies += TASK-021`)。

**顺带更正 tech-lead 报告一处未经验证的假设**: tech-lead 报告 §一"TASK-021 是否真收口"一节写道"TASK-021 之后仍会执行的只有 TASK-015(ab-results)/TASK-016(CLAUDE.md)/TASK-017(发版文件), 无一触及被 SC 断言的文件 ⇒ TASK-021 的收口是真的"。**这句话本身对"SC 不会被后续任务打红"这个具体主张仍然成立**(TASK-016/017 确实不改被测文件), 但它的措辞"TASK-021 **之后**仍会执行"隐含了一个**未经 DAG 验证的顺序假设**——本席实测只有 `TASK-015` 真正被 `dependencies` 钉在 `TASK-021` 之后, `TASK-016`/`TASK-017` 与 `TASK-021` 之间**没有任何依赖边**, 在合法拓扑序下可以先于甚至与 `TASK-021` 并行执行。tech-lead 的结论在"不会打红 SC"这个窄命题上没错, 但不能被读成"TASK-017 一定排在 TASK-021 之后"——这正是 K1 成立的空间。

**severity**: Major(非 Critical)——它不改变 Rule #8 gate 本身的运行时行为, 是一个**声明真实性/发布纪律**缺口。`blocks_phase_b`: **false**(TASK-017 属 TG-3, 不阻塞 TG-0~TG-2 开工), 但须在 TG-3 执行前(即 Phase C 之前)补上这条依赖边, 否则"版本号已声明但代码未必验证完成"这个风险会一直悬着到实际执行时才可能被发现。

**修法建议**: `detailed-tasks.yaml` TASK-017 `dependencies` 补 `TASK-021`(比照 `TASK-015` 已有的处置)；`TASK-018`(blast-radius/外部通告)与该风险同形但较弱(它是"核验影响面"而非"声明完成", 未列为独立 finding, 仅供执笔参考一并检查)。

---

### Finding K2(**Major, 与 tech-lead R3/M4a 交叉确认, 独立证据 + 追加一层后果**)—— 发版同步面的"8 个已知落点"清单本身**遗漏 `CLAUDE.md:81` canonical 清单里的"主仓 gitlink"**

**locator**: `CLAUDE.md:81` · `proposal.md:366`(Impact 表"发版同步面"行) · `tasks.md:111` · `detailed-tasks.yaml` TASK-017 verification 第 2 条

**实跑(独立于 tech-lead 报告, 事后核对结论一致)**:

```bash
$ grep -n "发布同步面" /home/dev/Aria/CLAUDE.md
81:- 发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README (仅正文实质变更才重译, #140 B 档)。机械兜底: custom checks `m6-version-badge-match` / `i18n-readme-translation-currency`。

$ grep -rniE 'gitlink|子模块指针|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/
(零命中)
```

CLAUDE.md 的 canonical 措辞把「主仓 gitlink」列为与「aria 子模块 5 文件」**并列**的独立同步项，而本 Spec 三件套全篇(`proposal.md`/`tasks.md`/`detailed-tasks.yaml`)对"gitlink"/"子模块指针"/"submodule pointer"零字面提及，`TASK-017.deliverables`(见上引 yaml)只列了 10 个文件路径，没有一项对应"主仓提交里把 `aria` 子模块指针 bump 到 post-merge SHA"这个动作。

**它怎么会红**: 若实施者严格按 `TASK-017` 现有清单执行(哪怕连同 K1 一起修好、且真的排在 `TASK-021` 之后), 落地结果会是: `aria` 子模块内 `plugin.json`/`CHANGELOG.md` 等 5 文件已经是 2.0.0, 但**主仓提交树里 `aria` 这个 gitlink 条目仍指向旧的子模块 SHA**(因为"按整仓引用点差集枚举"这套方法学枚举的是**文本引用**, 而 gitlink 是 git 树对象层面的指针, 不是任何文件里的一段文本, **结构上不会被"整仓 grep 差集"这套方法捕捉到**——这是比"清单漏项"更深一层的问题: 即便清单补全, `TASK-017` 现在的验证方法(文本 grep 差集)也**天然测不到 gitlink 是否已 bump**, 这是它的方法论盲区, 不只是枚举遗漏)。⇒ `git submodule status aria` 会显示落后于主仓声称的版本, `git clone --recursive` 拿到的是旧插件——**与 CLAUDE.md「多远程推送 — 两条硬约束」一节明确记载的 Aria #165 根因同一形状**(该节原文即针对"gitlink 孤立"这个失效模式写的, 本 Spec 恰好是一个会产出该失效模式的候选样本)。

**追加一层后果(tech-lead M4a 未展开的部分)**: gitlink 的 bump **不是靠 grep 就能验证的机械断言**——它需要一条形如 `git -C aria rev-parse HEAD == git ls-tree HEAD aria | awk '{print $3}'`(或等价)的**结构性**核验, 而 `TASK-017` 现有 verification 三条(引用点差集枚举 / custom check 声明不构成兜底 / 8 落点清单)**没有一条是这个形状**。仅仅把"gitlink"这个词加进清单文本(修 tech-lead M4a 那层)**不足以**让 `TASK-021` 或任何机械勾稽点真正核验它是否发生——这本身又是一个"只补文本没补验证手段"的实例。

**归因**: R1-fix 版 `TASK-017.deliverables` 只有一句"版本引用点清单", 未涉及任何具体文件或 gitlink; R2-fix 补齐了 10 个文件路径但**同样没有**补 gitlink ⇒ **introduced_by_r2fix: true**(R2-fix 在"发版同步面"这个具体维度上做了一次实质性扩充, 但扩充时沿用的仍是"文本引用点枚举"这一种方法, 对 gitlink 这类"树对象指针, 非文本引用"的同步项结构性失明, 与 K1 同源 —— 都是"R2-fix 加固了一个具体维度, 但没把加固推广到与它同类却形态不同的另一个维度")。

**severity**: Major。`blocks_phase_b`: false(TG-3, 不阻塞 TG-0~2)，但因它直接对应 CLAUDE.md 明列的已知失效模式(Aria #165 三次复发), 建议 TG-3 执行前必须解决, 不宜留到 Phase C 才发现。

**修法建议**: `TASK-017` 补一条独立 deliverable/verification —— 「主仓提交内 `aria` gitlink 条目(`git ls-tree HEAD aria`)= aria 子模块侧完成 R2-fix 落地后的 post-merge 主分支 SHA, 用 `git submodule status --recursive` 或等价命令核验非 `+`(ahead)/`-`(uninitialized) 前缀」，并显式引用 CLAUDE.md「多远程推送 — 两条硬约束」以复用既有的本地双推 + `ls-remote` 核验流程(phase-c-integrator §C.2.5 已自动化, 本条只需保证 TASK-017 不会绕过它)。

---

### Finding K3(**Minor, 新发现**)—— `TASK-016`(CLAUDE.md Rule #8 同步)是全 Spec 唯一一条仍用纯散文、无可复跑断言的"合规同步面"任务

**locator**: `detailed-tasks.yaml` TASK-016 `verification`

```yaml
verification:
- '规则 #8 那段反映新增的分支存在性核验腿'
- '对照先例 commit 7661e96 (v1.31.0 CI backend 抽象化在同一提交同步过 Rule #8) 核同步粒度'
```

**它怎么会红**: 与同组 `TASK-015`(`grep -c` 精确判据)、`TASK-017`(逐落点清单 + "怎么会红"反例)、`TASK-020`(逐条 grep 双语口径)相比, `TASK-016` 的两条 verification 全是"反映"/"核同步粒度"这类无量化判据的散文——一个只在 `CLAUDE.md` 里加一句语焉不详的话(甚至语义与新增的分支存在性核验腿完全不对应)的实现, 没有任何机械勾稽点会拒绝它。这正是本 Spec 全篇反复用来定级 Major 的同一形状(参见 proposal `:298` 对"无编号即不被任何机械勾稽点找到"的自我批评), 本条落在 `CLAUDE.md` 这个"单一事实来源"文件上, 按理更该有具体断言(例如: grep `CLAUDE.md` 规则 #8 段落须同时含"main 无 in-flight" 与 "分支存在性" 或等价字样, 今日计数与期望计数)。

**为何只定 Minor 而非 Major**: 它不影响任何 SC / Rule #8 gate 的运行时行为, 且 `TASK-016` 的 agent 是 `knowledge-manager`(本席自己在 Phase B 的执行角色), 执行时有充分上下文能做对; 与 K1/K2(涉及外部可见的"已发布"声明、且有具体的、已被文档明确记载过的失效先例 Aria #165)相比, 风险面更窄。

**introduced_by_r2fix**: false(该任务 R1-fix 版即是这个形态, R2-fix 未触碰它 —— `git diff 6818773 878ee44 -- detailed-tasks.yaml | grep -A3 "id: TASK-016"` 无输出，非本轮新引入)。

---

## 三、对那道机械交叉检查(xcheck.py)的评估 —— 补一个三份 R3 报告都未覆盖的角度

tech-lead / backend-architect / qa-engineer 三份报告已经用具体变异实验证明: CHECK1 无向、CHECK2 是跨任务 OR(不分辨"认领"与"免责声明式提及")、CHECK3 是任务级而非锚点级、CHECK4 是纯字面量匹配零语义。这些结论我读后逐条认可(qa-engineer 的变异实验尤其干净), 不重复验证。

**我补的角度**: 上述四项判据的**共同结构性前提**是"被检查的缺陷必须先在文本里被提及"——CHECK1 靠 `TASK-\d{3}` 正则命中移交对象, CHECK2 靠 SC 编号已在表里注册, CHECK3 靠护栏关键词已被写下, CHECK4 靠预先写死的字面量列表。**K1(TASK-017 缺依赖 TASK-021)是这四项判据结构上**必然**逃过的一类缺陷**——不是"覆盖弱", 是**覆盖对象根本不存在**: 我已实测确认 `TASK-021` 这个字符串在 `TASK-017`/`TASK-016`/`TASK-018` 的整个 YAML 块内**零次出现**(见上文 `blob17`/`blob16`/`blob18` 的 grep 结果), 也确认在当前提交状态下重跑 `xcheck.py`(只读, 未改动任何文件)仍报 `RESULT: PASS`。

⇒ 这补上了 backend-architect Finding 1(CHECK2 对"应该有 SC 编号但从未被造出来"的恒绿)与 qa-engineer F1-F3(CHECK2/3/4 对"措辞改写但语义不变"的恒绿)之外的**第三种**恒绿模式: **"两个任务之间存在真实因果依赖, 但因为从未在任何一方的散文里被提及, 连"点名但没连边"这种最基本的抓取入口都不存在"**——CHECK1 能抓"移交给没核过的下游"这个 R2 原始形状, 前提是移交那句话**至少写出了对方的编号**(如 qa-engineer 变异 1.1 的做法); 一旦缺口是"根本没人想到要写这句移交", 四项判据无一能触及。这与backend-architect"CHECK2 结构性恒绿"的论证同构, 但发生在**依赖边**这个维度而非 **SC-owner** 维度, 说明这不是 CHECK2 一项的局部弱点, 而是**xcheck.py 全部四项判据共享的同一个结构性盲区**("先注册/先提及才能被检查"), 呼应 backend-architect 与 qa-engineer 各自独立给出的"这是 R2 那两个形状的回归测试而非通用不变量验证器"这一定性。

**结论(与其余三席一致, 独立到达)**: xcheck.py 不是无用的(CHECK1/CHECK3 对"已知具体写法被删除"这类回归有真实拒绝力, 本席未见反例); 但它不能被读成"四类失效形状已被机械杜绝"——K1 是这句话在本轮的又一个反例, 且是一个"结构上不可能被四项判据的任何一项碰到"的反例, 不是"覆盖弱"层面的反例。

---

## 四、Rule #5/#6/#9/#10 与 Level 3 三件套 — 本轮判定

- **Rule #5**: ✅ 合规。变更放 `/home/dev/Aria/openspec/changes/premerge-gate-mainbranch-failclosed/`(主仓自身 `openspec/changes/`), 未误放 `standards/openspec/changes/`。
- **Rule #6**: ✅ 合规, 且本轮独立复核 `config-loader` 三件套**逐字对照 SOT** 确认真实成立(见上表 M2), 好于我 R1/R2 两轮的核验深度(本轮首次逐字比对 SOT 原文, 而非只核对 Spec 自身内部一致性)。`phase-c-integrator` 两套件仍走判据表第二行零裁量, 无豁免申请。
- **Rule #9**: ✅ 合规。`grep -rn "\.aria/handoff" openspec/changes/premerge-gate-mainbranch-failclosed/` 零命中。且本轮额外验证: 三件套里全部"须写入 handoff 请复议"的 Rule #10 留痕承诺, 经查 `docs/handoff/2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md` 均**确实被记录**(MAJOR 版本裁定 / config-loader 判据行归属判断 / R2 后是否继续 / 是否并行开 Phase B 四项复议, 逐条核对存在)——这是对 memory `feedback_cross_doc_claim_verify_at_target`(文档 A 声称已在 B 做 X 必须去 B 实测)的一次正例验证, 而非又一次落空。
- **Rule #10**: ✅ 合规。全部 6 处"Rule #10 留痕"引用均指向**已被 owner 显式授权 AI 代裁**的判断(2026-08-10 session "完整执行 2,3,4,5"), 而非自行豁免已启用的闸门; 且这些裁定已如实写入 handoff 供复议, 不是自我了结。未见 CLAUDE.md 规则 #10 四类白名单之外的自创豁免理由。
- **Level 3 三件套**: ✅ 机械同步确认(实跑, 非估读): `tasks.md` checkbox 数 = **21**, `detailed-tasks.yaml` task id 数 = **21**(全部唯一), `metadata.total_tasks` = **21**, 三者一致; 依赖图无悬空引用、无环(Python 脚本实跑确认)。**但**: 三件套"结构完整"不等于"执行序安全"——本轮 K1 表明, 即使字段计数与去重全部通过, DAG 里仍可能缺失语义上必要的边(tech-lead M5 的 7 处方向倒置是"有边但方向错", K1 是"该有边但没有")，这是 Level 3 三件套完整性核验需要覆盖、但目前**没有任何机械手段**(含 xcheck.py)覆盖的一个子维度。

---

## 五、量化 —— `introduced_by_r2fix`

**本席: 2 / 3 = 67%(Major K1、K2 为 R2-fix 引入; Minor K3 非本轮引入)。**

⚠️ **口径警示(不与其余口径比较, memory `critique-repeats-error`)**: 本席样本(3 条)全部来自"我自己这一轮新发现的条目", 不是"R2 原始 1C+~13M 的去重回源计数"——按此判据表回答"R2 是否真闭合"时, 我镜头内可回源的 4 条(M2/M10/我的 F-1/F-2)**全部真闭合**(0 未闭合), 这与 K1/K2/K3 是**两个不同的计数总体**(前者是"R2 遗留项是否被修好", 后者是"R2-fix 本身在我镜头内又留了几个新洞")，不得相加或相除得出一个单一比率。

**可与其他三席比较的唯一同口径事实**: 我镜头内可回源的 R2 遗留条目 **100% 真闭合**(4/4), 但**我镜头内又发现 2 条新 Major**——与 tech-lead(80%, 8/10)、backend-architect(独立发现 1 条 Major)、qa-engineer(独立发现 3 条 Major, 全部针对 xcheck.py 本身)合并看, **五席全部在 R2-fix 自称已收口的范围内继续找到新缺陷**, 这本身是这一轮`fix→审计`循环仍未收敛的独立证据, 与判据「本轮低于 50% 才说明机械检查真的起作用了」的意图(用比例下降来说明"缺陷生产率在降")不完全对得上——真正该关注的信号是: **五个独立席位, 每人都在不同维度找到了至少一条新 Major**, 说明"新缺陷发生率"仍然很高, 只是被 xcheck.py 覆盖到的那几类具体缺陷(R2 原始那两个形状的**已知实例**)确实被压下去了。

---

## 六、阻塞项与建议

**本席新增 blocks_phase_b: 0**(K1/K2/K3 均属 TG-3, 不阻塞 TG-0~TG-2 开工)。

**但**: 本席确认 tech-lead R3 报告的 1 Critical(C1, TASK-014 验收量结构上不可满足)+ 4 条 blocks_phase_b Major(M1/M2/M3/M4)在我核验范围内**均未被推翻**——尤其 M4(gitlink 缺失)与本席 K2 是同一处发现, 双席独立命中提高其可信度; 且 K1/K2 进一步表明 TASK-017 的问题比 tech-lead M4 描述的更深(不只是清单漏项, 是执行时序与验证方法两层都还有缺口)。

**建议**: 按 CLAUDE.md 规则 #10, 本席不得也不建议自行豁免 tech-lead 报告的阻断; K1/K2/K3 建议在 TG-3(`TASK-015`~`TASK-020`)进入实施前一并解决, 成本均为"加一条依赖边 / 加一条 deliverable / 加一条量化断言"级别, 不需要新一轮换人执笔。

---

## 七、实跑命令原文(可复跑)

```bash
cd /home/dev/Aria
git status --porcelain openspec/changes/premerge-gate-mainbranch-failclosed/   # 全程零输出

# M2 / config-loader 三件套核验
grep -n "config-loader" -A10 openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md | sed -n '1,40p'
sed -n '1,40p' /home/dev/Aria/standards/conventions/skill-benchmark-exemption.md

# M10 / F-1 / F-2 核验
grep -n "TASK-019 第 (7)" openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md
grep -rn "main_branch_resolved" openspec/changes/premerge-gate-mainbranch-failclosed/

# K1 — 拓扑与依赖闭包（脚本见正文，用 PyYAML 解析 detailed-tasks.yaml 计算 ancestors("TASK-017")）
git show 6818773:openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml | grep -c "TASK-021"   # 0，证实 R2-fix 新增

# K2 — gitlink 缺口
grep -n "发布同步面" CLAUDE.md
grep -rniE 'gitlink|子模块指针|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/  # 零命中

# K3 — TASK-016 R2-fix 未触碰
git diff 6818773 878ee44 -- openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml | grep -A3 "id: TASK-016"  # 空

# 三、xcheck.py 结构性盲区核验
python3 -c "
import yaml
d = yaml.safe_load(open('openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml'))
tasks = {t['id']: t for t in d['tasks']}
for tid in ['TASK-016','TASK-017','TASK-018']:
    blob = yaml.dump(tasks[tid], allow_unicode=True)
    print(tid, 'mentions TASK-021?', 'TASK-021' in blob)
"
python3 /tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed
# → RESULT: PASS（只读复跑，未改动任何文件；git status --porcelain 收尾复核仍为空）

# Rule #9 / handoff 交叉核验
grep -n "MAJOR\|config-loader\|Rule #10\|复议" docs/handoff/2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md
```

对抗/推理性核验(拓扑排序脚本、ancestors 计算)全部落在只读的 Python 一次性脚本, 未改动仓内任何文件; 全程 `git status --porcelain openspec/changes/premerge-gate-mainbranch-failclosed/` 核验为空。
