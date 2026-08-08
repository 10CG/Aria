---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T09:45:30.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席

**审计对象**: `openspec/changes/linked-issue-normalization/tasks.md` + `detailed-tasks.yaml` (17 → 21 任务) @ HEAD `3fc6f3f`
**R1 基线**: 5/5 REVISE / FAIL, 3 Critical + 12 Major。本席 R1 = 2C + 5M + 2m (F1–F9)
**镜头** (与 R1 同): 交付顺序 / 外部门 / 多远程与子模块协调 / 范围纪律双向 / Phase C-D 缺口 / agent 分配可执行性
**不重审**: 归一规则本体 · basename 截断轴 D4 · phase1_gate.py CLI · include_terminal

**verdict: FAIL** (2 Critical + 6 Major + 1 Minor 新增; 5 条 carryover 未闭合)
**vote: REVISE**

---

## Part 1 — R1 九条闭合判定

| # | R1 severity | 判定 | 一句话 |
|---|---|---|---|
| F1 | Critical | **partially_closed** | TASK-016 独立成任务 + 三判据入 verification ✓; 但 aria 子模块**分支创建/PR 环节仍无任务** (实测 aria 处 detached HEAD 无分支), 且 TASK-017 的 gitlink 判据仍是散文无机械断言 |
| F2 | Major | **partially_closed** | `scope_repos` + `path_convention` 已加, 抽查 4 组 deliverables 路径与行号全部实测吻合 ✓; 但主仓 surface 枚举仍漏 `aria-plugin-benchmarks/` (= F7 后半) |
| F3 | Major | **partially_closed** | `scope_boundary` + tasks.md 范围边界表已加 ✓; 但 (a) 该块**自相矛盾** (见 N1), (b) 归档门依赖写错机制名, 「TASK-016 的 status 何时落 done-family」仍未定义 |
| F4 | Major | **partially_closed** | TASK-021 二选一已加且验收可判 ✓; 但 F4 点名的**第二条失效路径** (归档后 `FATAL: 找不到 proposal.md`) 未覆盖, 且 (b) 分支会让 proposal 两处引用悬空 |
| F5 | Major | **closed** | #133 comment 17976 实读确认: collision×13, `:210/:307/:155` 三处全在, 更正为「6 处具名 + 1 处内联, 3 种成员集」, 与 yaml 表述逐字一致 |
| F6 | Major | **closed** | TASK-010 改归 backend-architect ✓ + `009→010` 串行边 ✓ + DAG 注释「三个不同文件」错述已删, 真并行组改为 `{011,012}·{018,019}` ✓ |
| F7 | Minor | **partially_closed** | gitlink 已进 TASK-017 deliverables ✓; AB 结果的仓归属仍未收口 (同 F2) |
| F8 | Minor | **closed** | tasks.md 标题改「协调项已关闭, 但已知限悬空风险仍在 (两件事, 不要混读)」+ (1)/(2) 分列 + X3 消歧 ✓ |
| F9 | Critical | **partially_closed** | 两路都写了 fail-CLOSED 措辞, 但**两路的出口都坏** (见下方逐条论证 + N9) |

### F1 — 三条硬判据够不够可执行? 漏了什么?

**够用的部分**: verification 第 3 条 (`逐个 git ls-remote <remote> master 取 SHA 与本地比对, origin 与 github 全部一致`) 是**结构上足够**的 — 服务端合并会使本地 master 从未 fast-forward, 此时 `ls-remote origin` ≠ 本地 ⇒ 被抓。所以第 3 条一条就承住了 CLAUDE.md 约束 1 与约束 2 两个失效面。第 1、2 条 (`未使用服务端 merge` / `双推已执行`) 是**过程声称**, 事后无状态可查, 只能自证 — 建议明写「第 3 条是唯一承重判据, 1/2 条不可单独判绿」, 否则会出现「1、2 打勾, 3 没跑」的部分通过。

**漏掉的第一件事 — aria 子模块的分支创建/PR 环节完全无任务归属**:

```
$ git -C aria rev-parse --short HEAD   → af87cae
$ git -C aria branch --show-current    → (空 = detached HEAD)
```

TASK-016 要「本地 `git merge` 到 aria 子模块 master」, 但**没有任何任务生产那个被合并的分支**。21 个任务实读: 零 branch / checkout / PR 创建动作。而新加的范围边界表把 **Phase B (含 B.1 分支创建) 明确划归本文件**, 只把 Phase C/D 委派出去 ⇒ 分支创建既不在文件里, 也没被委派。这与 R1 的 F1 是**同一形状**: 一个 verification 谓词消费一个没有任务生产的产物 (R1 是「合并后 master SHA」, R2 是「被合并的分支」)。

**漏掉的第二件事 — TASK-017 的 gitlink 判据仍不可机械核验**:

逐字 `"gitlink 指向 aria 子模块 **TASK-016 合并后的 master SHA**, 不是 feature 分支 SHA"` — 这是散文断言, 没有对应命令。风险是具体的而非理论的: **aria 当前就是 detached HEAD**, 而 `git add aria` 记录的是 `git -C aria rev-parse HEAD` 而不是 `master`; 若 TASK-016 合并后没有把子模块工作树切到 master, TASK-017 会把 gitlink 钉到 detached/feature SHA, 而 verification 照样可以声称「已指向合并后 SHA」。

维度匹配的断言应是 `git ls-tree HEAD aria` 的 SHA == `git ls-remote github master` 的 SHA — 即**在写 gitlink 的那一刻重新核 GitHub 侧存在性**。TASK-016 的核验发生在 T 时刻, TASK-017 的写入发生在 T+1, 两者之间没有不变量。而 memory `feedback_mirror_sync_needs_mechanical_backstop` 的处方逐字是「靠纪律的同步对服务端合并路径无效, 须**机械兜底 / bump 前 orphan 守卫**」—— 本次 fix 交付的是纪律散文, 不是兜底。全份计划里唯一的机械断言 (TASK-020) 明确只管版本字符串, 不管 gitlink。

补充一条实测不利事实: `phase-c-integrator` 的 C.2.4.5 submodule pointer gate 只 `git -C <submodule> fetch **origin**` (SKILL.md:190) ⇒ **GitHub 侧的 orphan 从来不在任何 enabled 闸门覆盖内**, TASK-016 的 `ls-remote github` 是唯一的 GitHub 守卫, 而它在 gitlink 写入之前就结束了。

### F9 — 「两路钉成 fail-CLOSED」够不够? 「结构性看不见」该不该在 A.3 就有结论?

**不够。而且把它推给运行时本身就是问题** —— 三条实证理由:

**(1) 两条 fail-CLOSED 出口构成回路, 回路的两个出口分别是恒红与假绿。**

- A 路 (能测): 判据「with_skill 优于 without_skill」。在对该 hunk 零覆盖的套件上, **健康常态的结果就是 EQUAL** (`AB_TEST_OPERATIONS.md:363` 逐字 `EQUAL | delta < 5% 或全部 TIE`)。EQUAL 不满足「优于」⇒ **恒红**。
- B 路 (覆盖外): 三件套, 而其兜底逐字是「**缺一则照跑**」= 回到 A 路。
- ⇒ 实施者的可达终局只有两个: 恒红, 或者用「跑了」把 A 路判绿 (即 R1/F9 点名的假绿)。**没有一个出口是「这个闸门对该 hunk 作出了判别」**。

形状 = memory `feedback_fix_recurs_in_its_own_fallback_path` (修复类 change 最易在自己新写的兜底路径重犯要治的病) + `feedback_false_green_dual_is_permanent_red` (假绿的反面是恒红, 同样零信息)。本 Spec 全程在打这个对偶 —— TASK-021 的存在就是为了拆掉一个恒红 —— 却在 TASK-013 里装了一个。

**(2) B 路没有 deliverables, 所以它落不了地, 所以它必然坍缩回 A 路。**

TASK-013 的 deliverables 只有一行 `aria-plugin-benchmarks/ab-results/`。三件套要求的三件东西 —— 点名行为 / 可证伪定向 fixture / 套件缺口 issue —— 在 verification 散文里出现, 在 deliverables 里**零对应项**: 没有 `ab-suite/state-scanner.json` (含 version+changelog bump)、没有 fixture 路径、没有 issue 号字段。R1/F9 已实测过本项目 Rule #6 AB 的既有形态 (`2026-07-20-v1.62.0-phase4-rule6` / `2026-07-31-v1.65.0-122-rule6`) 都是「定向 eval + 双臂 skill snapshot/candidate + benchmark.json + grading-summary.md」, 本轮 fix 没有采信那两个先例的形态。

**(3) R1/F9 的核心断言未被反驳, 只是被改写成了不预判。**

覆盖度是**现在可判定的事实** (R1 已逐 eval 列名实测两条输入面共 19 个 eval 零覆盖), 不是运行时条件。fix 说「本任务不预判结论」是一个合法的姿态, 但它同时**没有加任何任务去让这个判定可审计** —— 既没有「先判定覆盖度并留证」的前置任务, 也没有把判定结论写成一个可复核的产物。结果是: 一个 owner 亲裁 (Q5)、Rule #10 保护、tasks.md 标题写着「⛔ 不申请豁免、不走 substitute」的闸门, 它的判别力由实施者在运行时裁量, 而两个出口都是坏的。

**结论**: F9 partially_closed。最小修法不是再改措辞, 而是 (i) 在 TASK-013 之前加一个「覆盖度判定 + 留证」任务, 让「能测 / 覆盖外」成为一个有产物的结论而不是运行时口头分支; (ii) 给 B 路配齐 deliverables, 使它成为可落地的第二条真路; (iii) 把 A 路的判据从「优于」改成对该 hunk 有意义的判据 (否则零覆盖套件恒红)。

### F2/F7 — deliverables 路径抽查

`path_convention` 逐字「本文件所有 deliverables 路径**从主仓根起算**, aria 子模块内的文件一律带 `aria/` 前缀」。逐组实测:

| 任务 | deliverable | 实测 |
|---|---|---|
| TASK-017 | `VERSION` | ✅ 主仓那一份; `:24` = `| aria (插件) | v1.65.5 | …` 逐字命中 |
| TASK-017 | `README.md` | ✅ 主仓; `:8` badge + `:242` `Plugin Version:   1.65.5` 两处实测 |
| TASK-018 | `README.zh.md` | ✅ 主仓; `:3` translated-from + `:10` badge + `:244` Plugin Version 三处逐字命中 |
| TASK-019 | `CLAUDE.md` | ✅ `:139` 版本区间行 + `:141`「版本:」行 两处逐字命中 |
| TASK-015 | `aria/VERSION` 等 5 文件 | ✅ 全部带 `aria/` 前缀, 指向子模块内那一份 |
| TG-1..TG-3 | 全部 | ✅ 一律 `aria/skills/state-scanner/...` 全限定 |

⇒ 「同一 YAML 两套根」的歧义**已消除**, 且全部行号今日实测有效。F2 的主体闭合。

**残留**: `scope_repos[Aria 主仓].surface` 逐字 = `gitlink · VERSION · README.md · README.{zh,ja,ko}.md · CLAUDE.md · Spec 本体 · .aria/repro/` —— **不含 `aria-plugin-benchmarks/`**, 而 TASK-013 的 deliverable 正落在那里 (实测该路径是主仓内普通 tree, 非子模块)。这就是 R1/F7 的后半, 未闭合。它和 Critical-1 是同一病: **枚举式声明与真实落点集合脱节**。

小注: TASK-016 的 deliverable 写 `aria/` (子模块 master ref), TASK-017 写 `aria` (gitlink) —— 两者仅差一个尾斜杠, 语义完全不同。注释里说清了, 但作为机读字段过于脆弱。

### F3 — 归档门依赖写清了吗?

**没写清, 而且机制名是错的。** `scope_boundary.delegated[1].why` 逐字「归档门会消费本文件全部 **21 个 checkbox 状态**」。实测归档门消费的是 **detailed-tasks.yaml 的 `status:` 字段**, 不是 tasks.md 的 checkbox:

```
aria/skills/state-scanner/scripts/lib/detailed_tasks.py:83
_DONE_FAMILY = frozenset({"done", "completed"})   # done-family whitelist (fail-CLOSED)
```

而 21 个任务当前全是 `status: pending`, `pending ∉ {done, completed}`。R1/F3 明确要求的那一条 —— 「TASK-016 的 `status` 何时落 done-family 的规则」—— 依然不存在。本项目对这个耦合已有 canonical 写法, 就在同仓的姊妹 Spec 里 (`openspec/changes/phase-c-integrator-ci-path-coverage/detailed-tasks.yaml:105-114`, 实读), 它逐字写出了 done-family 白名单、fail-CLOSED、`lib/detailed_tasks.py:83` 的 file:line、以及「不得留在 blocked, 否则 spec 卡住无法归档或有人改 status 绕过门」。本 Spec 没有采信这个先例 (memory `feedback_spec_precedent_verify_execution_history`: 引先例须核实际语义 —— 这里是反过来, 有可用先例而未引)。

### F4 — 二选一的验收怎么判?

**(a) 分支**「加 post-implementation 模式: 断言那 8 条 SC 已转绿」—— 可执行 (跑脚本即可判), 但**不解决 F4 点名的第二条失效路径**。实读脚本:

```
:208  _PROPOSAL = <repo>/openspec/changes/linked-issue-normalization/proposal.md
:215  sys.exit("FATAL: 找不到 proposal.md (%s) —— 漂移守卫无法核对, 拒绝以硬编码…")
:239  SPEC_TABLE, EVIDENCE_FACE = _parse_spec_table(_PROPOSAL)
```

EVIDENCE_FACE 是从 proposal.md **现场解析**出来的, 所以 Phase D.2 把 Spec 移到 `openspec/archive/` 之后, post-implementation 模式的脚本连表都解析不到 ⇒ 换一种恒红。TASK-021 的三条 verification 都不覆盖这一路。R1/F4 的 evidence 里把它逐字列为「第二条独立失效路径」, 本轮吸收只处理了第一条。

**(b) 分支**「脚本移出 `.aria/repro/`」—— 会让 proposal 的两处引用悬空。实读 `proposal.md:181` 是相对链接 `[…](../../../.aria/repro/sc-baseline-linked-issue-normalization.py)`, `:183` 是复现命令 `python3 .aria/repro/sc-baseline-... aria/skills/state-scanner`。TASK-021 没有任何一条 verification 要求同批改这两行。R1/F4 的 fix_direction 里有这一句 (「把 proposal.md:183 的复现命令改成『仅在 pre-fix 树上有效』」), 吸收时丢了。

⇒ 二选一本身**可判**, 但两条分支各留一个未覆盖的洞, 且「无论哪条, substitute 论证的可复核性必须仍然成立」这条兜底句在 (a)+归档 组合下与事实冲突。

### F5 — #133 实读核验

```
comment id 17976 · 2026-08-08T09:36:49Z · 1950 chars
'collision' ×13 · 'unknown' ×6 · '210' ×3 · '155' ×2 · '307' ×3 · '内联' ×3
表格三行: collision.py:210 (tuple, 含 unknown) / :307 (tuple) / :155 (列表推导内联 tuple, 无常量绑定)
三种成员集分列, 并逐字「更正本 issue 标题里的『4 处定义 2 种成员集』…是 6 处具名定义 + 1 处内联, 3 种成员集」
```

与 yaml TASK-008 notes 的新表述 (`6 处具名 + 1 处内联, 3 种成员集`) **逐字一致**。R1/F5 的「范围纪律论证建立在不存在的覆盖上」已消除 —— 覆盖现在真实存在。**closed**。

两点留痕 (不构成本 Spec 的发现, 属 #133 自身):
- issue 的 **title 与 body 未 PATCH** (`updated_at` == 评论时间; body 的 `collision` 计数仍为 0, 标题仍写「4 处定义 2 种成员集」)。评论宣布了标题更正但没执行。按标题/正文扫描的人仍看不到 collision 覆盖。
- 评论新开了一个 `lib/gc.py:213 (同族, 待核)` 悬项, 无人承接。

### F6 — DAG 注释同步核验

全部同步且派生值重算一致:

```
:634  001,002,003,004,005 → 007 → 008 → 009 → 010          ✅ 与 dependencies 字段逐条一致
:645  真并行组 (不同文件): {011, 012} · {018, 019}          ✅ 010 已移出并行组
:646  ⛔ 无同文件并行边                                      ✅
:650  S ×14 · M ×6 · L ×1 · 88h                             ✅ 逐条重算一致 (14×3+6×6+1×10=88)
:651  qa ×9 · backend ×7 · knowledge ×5 = 21                 ✅ 逐条重算一致
```

另核 `co_dependency_note` / `file_domain_serialization` / DAG 三处对 TG-1 串行链与 006 例外的表述**互相一致**; 17 条 SC 在 TG-1 六任务里恰好覆盖一次无重无漏; 场景数 13+5+15+8+1+3 = 45 == `test_counting_contract.scenario_count`。**closed**。

---

## Part 2 — R1-fix 自身引入的新问题

### N1 — `new`

```
- type: issue
  severity: critical
  category: architecture
  scope: detailed-tasks.yaml metadata.scope_boundary + TASK-016 + tasks.md 范围边界表
  summary: scope_boundary 块**自相矛盾** (同一块内既把 merge 委派给 phase-c-integrator 又承认合并在组 5), 且 TASK-016 把 aria 子模块合并搬到本文件执行, 从而把两个 **enabled 默认开** 的闸门 (Rule #8 C.2.4 pre-merge gate / C.2.4.5 submodule pointer gate) 切到了没有任何任务执行的一侧 —— 结构性自我豁免, 违 Rule #10。
  evidence: |
    同一个 metadata 块内, 相隔 5 行, 两句极性相反:
      scope_boundary.delegated[0].what 逐字: "Phase C — PR 创建 / pre-merge gate (Rule #8, C.2.4: 本 PR
        CI passing + main 无 in-flight run) / **merge**"  (who: phase-c-integrator; 该块标题即 `delegated`)
      scope_boundary.why_group5_is_here 逐字: "组 5 的 aria 子模块 bump+**合并** (5.2/5.3) 必须先于主仓
        gitlink bump (5.4)"  ⇒ 合并在组 5 = in_this_file
    tasks.md 范围边界表第 3 行同样把「merge」列为「**`phase-c-integrator`**, 不在本文件」, 而 tasks.md:82
    的 5.3 就是「aria 子模块分支合并 + 双远程推送」。⇒ merge 同时被声明为委派出去和在本文件执行。

    这不是措辞问题, 因为被绕过的东西是实存且默认开的。实读 aria/skills/phase-c-integrator/SKILL.md:
      :46  phase_c_integrator.pre_merge_gate.enabled          默认 **true**   (Rule #8 的 SOT)
      :47  phase_c_integrator.submodule_gate.mode             默认 **"block"** (v1.49.0+)
      :242 C.2.4 执行上下文契约逐字: "在执行 C.2 合并的目标仓根内调用 (**子模块合并 → 子模块根**)"
           ⇒ 该 Skill **本来就建模了子模块合并**, 不是只管主仓
      :183-199 C.2.4.5 Submodule Pointer Regression Gate: git -C <submodule> merge-base --is-ancestor
           MASTER_PTR FEATURE_PTR; verdict block = pointer regression/divergence
      :202-211 C.2.5 Multi-Remote Push Enforcement —— 正是 TASK-016 手工重写的那件事
    而 CLAUDE.md 逐字: "多远程推送由 phase-c-integrator §C.2.5 **自动化** (post-push SHA 验证); **手工路径**
    守下方两条硬约束。" ⇒ 两条硬约束是**手工路径的降级守卫**, 不是对自动化路径的替代。

    后果: 21 个任务里没有任何一条为 aria 子模块的 PR 跑 C.2.4 (CI passing + main 无 in-flight run)。
    Rule #8 是不可协商规则, Rule #10 的封闭豁免白名单四类逐条不成立 —— config 没 off (默认 true/block)、
    无 adaptive_rules 映射、无已成文 lane、结构性前提成立 (aria 侧确有 PR 与 CI)。
    形状 = memory feedback_fixes_contradict_each_other_across_clusters: 多簇 fix 逐条吸收后每条单独看都对
    (F1 要求「合并要有 owner」✓; F3 要求「Phase C 要么补要么声明委派」✓), 但 F1 的落点违反了 F3 落点的
    隐含前提, 接缝正好落在两个角度之间。
  fix_direction: |
    二选一, 不可两头都要:
    (i) 把 aria 合并+双推交回 phase-c-integrator (白拿 C.2.4 + C.2.4.5 + C.2.5 自动化), TASK-016 退化为
        「合并后三条硬判据的独立核验」, 范围边界表保持现状;
    (ii) 保留 TASK-016 作为执行者, 则必须把 C.2.4 的两个谓词 (本 PR CI passing / main 无 in-flight run,
        经 CI backend 抽象层) 与 C.2.4.5 的 ancestry 检查一并写进它的 verification, 并**改掉**边界表里
        「merge → 委派」那一行。
    无论哪条, 都不得让 Rule #8 对两个仓中的一个保持静默。
```

### N2 — `new`

```
- type: issue
  severity: critical
  category: testing
  scope: detailed-tasks.yaml TASK-020 verification (零命中 grep) + aria/VERSION 实际格式
  summary: 本轮 fix 自称「唯一维度匹配的判据 / Critical-1 的根因修法」的那条机械断言, 按 aria/VERSION 的真实格式是**恒红** —— Spec 一边拆掉一个恒红 (TASK-021) 一边装了一个。
  evidence: |
    TASK-020 verification 逐字: grep -rn "1\.65\.5" <10 个文件> → **零命中**
      (`aria/CHANGELOG.md` 显式排除: 它是版本史, 保留旧版本号正确)
    ⇒ 排除名单只有 CHANGELOG 一项, `aria/VERSION` 在**被断言零命中**的名单里。

    实读 aria/VERSION —— 它不是裸版本文件, 是一本 append-only 发布纪要账本:
      :3  > **版本**: 1.65.5
      :4  > **发布日期**: 2026-08-02  # patch: v1.65.5 收尾 — secret-guard.test.sh …
      :5  > **发布日期(旧)**: 2026-08-02  # patch: v1.65.2 修 #124 …
      :6  > **发布日期(旧)**: 2026-08-01  # patch: v1.65.1 …
      :7+ 继续堆叠 v1.64.1 / v1.64.0 / v1.63.0 / v1.61.0 / v1.60.0 / v1.59.1 逐版本纪要
      grep -c "1\.65\.5" aria/VERSION = **2**
    该文件对每次发版的处置就是: 新增一行 `发布日期`, 把上一行降级成 `发布日期(旧)` 并**原样保留其版本号**。
    ⇒ bump 到 1.66.0 后, :3 变 1.66.0, 而 :4 降级为 `发布日期(旧)` 并**继续含字面 v1.65.5**
    ⇒ `grep "1\.65\.5" … aria/VERSION` 恒 ≥1 命中 ⇒ TASK-020 **按构造判红**, 100% 确定, 非概率。

    两个都坏的出路: 实施者要么删发布史去凑绿, 要么把这条断言当「已知噪声」忽略 —— 后者正是
    TASK-021 存在的理由 (memory feedback_false_green_dual_is_permanent_red: 恒红与假绿同为零信息)。
    本 Spec 全程在打这个对偶, 不能自己再造一个, 更不能造在「Critical-1 的根因修法」这条上。
  fix_direction: |
    (1) 把 `aria/VERSION` 与 `aria/CHANGELOG.md` 同等对待 —— 或整体排除, 或把 pattern 收窄到 live 字段
        (只查 `> **版本**:` 行与 `> **发布日期**:` 行, 不查 `发布日期(旧)`);
    (2) 顺带核一遍其余 9 个文件是否也含发布史型残留 (今日实测: 主仓 VERSION / README×4 / CLAUDE.md /
        aria plugin.json / marketplace.json / aria README.md 均为 live 引用, 无历史行 ⇒ 只有 aria/VERSION
        这一个特例);
    (3) 与 N3 同批修 —— 改成正向计数断言可同时消掉这个恒红 (计数只看 live 字段)。
```

### N3 — `new`

```
- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-020 verification + metadata.version_reference_surface.plus + TASK-015 verification
  summary: 零命中 grep 是**缺席**断言, 只对了一半维度 (它不断言新版本出现在 14 个点); 且 aria 侧仍按「5 文件」计, 正是主仓侧刚被判为 Critical 的那个维度错误 —— 诊断只被单边采纳。
  evidence: |
    metadata.version_reference_surface 自陈的论点逐字: 「三份文档都按**文件数**枚举同步面, 而错误的
    维度是**版本引用点数**」, 并给出主仓 14 点的逐文件 breakdown (今日实测逐一吻合:
    README.md 2 / zh 3 / ja 3 / ko 3 / CLAUDE.md 2 / VERSION 1 = 14 ✓)。

    但落地的断言是 `grep "1\.65\.5" → 零命中` —— 一个**缺席**谓词:
      · 把某个版本行整行删掉 → 零命中 → 判绿;
      · 把 1.66.0 写错成 1.6.60 / 166.0 → 零命中 → 判绿;
      · 从来不断言「1.66.0 在这 14 个点各出现应有次数」。
    错误的维度是**引用点计数**, 匹配它的断言就该是计数: 逐文件 `grep -c "1\.66\.0"` == breakdown 里的
    2/3/3/3/2/1。这个目标计数**今天就是已知的** (上面实测已证 breakdown 精确), 所以可直接写死。

    同一块的 `plus` 字段逐字: 「主仓 gitlink (非文本引用) + aria 子模块 **5 文件**」—— 文件维度, 即它
    自己刚判为病根的那个口径。实测 aria 侧的引用点数并不等于文件数:
      aria/.claude-plugin/plugin.json      1 处
      aria/.claude-plugin/marketplace.json **2** 处  (:3 与 :16 两个 "version" 字段)
      aria/VERSION                          **2** 处
      aria/README.md                        1 处
      ⇒ 4 个文件 6 个引用点 (CHANGELOG 另计, 排除)
    而 TASK-015 的 verification 是文件级的 (「plugin.json 为 SOT, 其余 4 文件与其一致」) ⇒
    marketplace.json 或 aria/VERSION 漏掉第二处时该任务判绿。
    ⇒ fix 把主仓侧升级到引用点维度, aria 侧留在文件维度; 同一份 metadata 内两套口径。
  fix_direction: |
    (1) TASK-020 改正向计数断言 (逐文件 grep -c 新版本 == 声明的点数), 缺席 grep 作为补充而非主判据;
    (2) version_reference_surface.plus 展开成 aria 侧的引用点 breakdown (4 文件 6 点), 并把
        TASK-015 的 verification 从「5 文件一致」改成点数匹配;
    (3) 与 N2 同批 —— 正向计数只看 live 字段, 天然绕开 aria/VERSION 的发布史行。
```

### N4 — `new`

```
- type: issue
  severity: major
  category: architecture
  scope: detailed-tasks.yaml TASK-020 dependencies + DAG :641-642
  summary: 唯一的机械断言被排在它要保护的那个**不可回退步骤之后** —— TASK-020 的 aria 侧断言只可能在 aria master 已合并、已双推、gitlink 已钉死之后才发红, 而计划里没有任何回退/重推的边。
  evidence: |
    依赖链实读: TASK-020 dependencies [TASK-018, TASK-019] → 017 → **016 (aria 合并 + 双推)** → 015。
    DAG :641 逐字: `{…} ──▶ 014 ──▶ 015 ──▶ 016 ──▶ 017 ──┬──▶ 018 ┐ └──▶ 019 ┴──▶ 020`
    而 TASK-020 的 grep 名单里有 4 个 **aria 子模块内**的文件
    (aria/.claude-plugin/plugin.json · marketplace.json · aria/VERSION · aria/README.md, 由 TASK-015 交付)。

    ⇒ 若这 4 个文件有残留 (按 N3, marketplace.json 与 aria/VERSION 各有第 2 处最可能被漏),
      发现时点是: aria master 已 merge (016)、已推到 origin+github 两个共享 remote (016)、
      主仓 gitlink 已钉到那个 SHA (017)。
    修它需要: 新 commit 到 aria → 第二次本地 merge → 第二次双推 → gitlink re-bump → 再核 ls-remote。
    这四步在 21 个任务里**都不存在**, DAG 也没有任何回边; TASK-020 是终端节点。
    ⇒ 计划把它唯一的机械护栏放在了它唯一的不可逆步骤的下游。这与 TG-1→TG-2 的 RED-first 排序原则
      (先立断言后改实现) 在同一份文件里方向相反。
  fix_direction: |
    拆成两条断言, 按仓面分别定位:
      · aria 侧引用点断言 —— 作为 TASK-015 的出口判据 / 或独立任务插在 **015 与 016 之间**
        (即在合并与双推之前, 此时改错还是本地成本);
      · 主仓侧引用点断言 —— 保留在 019 之后 (那一侧的 PR 走 Phase C, 尚未合并, 可回退)。
```

### N5 — `new`

```
- type: issue
  severity: major
  category: documentation
  scope: CLAUDE.md:81 (发布同步面 SOT) vs TASK-017/018/019/020 + 缺失的 issue
  summary: 修的是实例, 类留在原地 —— Critical-1 的根因就在 CLAUDE.md 自己那行「发布同步面」枚举里, 而它同时犯了本 Spec 已诊断出的全部三个错; 本 Spec 只在自己的 tasks.md 里装了一次性 grep, 既不修那行, 也不加持久 check, **也没开 issue**。
  evidence: |
    CLAUDE.md:81 逐字: 「发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge
    + i18n README (**仅正文实质变更**才重译, #140 B 档)。机械兜底: custom checks `m6-version-badge-match`
    / `i18n-readme-translation-currency`。」
    三个错, 与本 Spec 本轮的三条发现一一对应:
      (a) 「aria 子模块 5 文件」= 文件维度 (= N3 判的病);
      (b) **CLAUDE.md 自己的两处引用不在清单里** —— 这正是首版 tasks.md 完全没有 CLAUDE.md 落点的原因
          (R1/code-reviewer 的 Major): 实施者按 SOT 枚举办事, SOT 漏了它;
      (c) 「root README badge」漏掉 README.md 的 `Plugin Version:` 行, 而它把那两条 custom check 断言为
          「机械兜底」—— 本 Spec 的 metadata.version_reference_surface.enabled_check_blindness 已实证
          那两条对 **7 处**结构性失明。
    本轮 fix 的处置: TASK-017/018/019 逐点补, TASK-020 一次性 grep。全部落在**本 Spec 的 tasks.md 内**,
    Phase D.2 归档后随 Spec 一起离场 ⇒ 下一次发版按 CLAUDE.md:81 办事的人会原样重犯。
    而 TASK-020 的 notes 自己写着「三份文档首版都写『5 文件 + gitlink』这一文件数口径…**同一形状第三次**」
    并宣布「本版不再靠逐条补丁, 改用机械断言收口」—— 断言只收本 Spec 这一口。
    形状 = memory feedback_fix_the_class_not_the_instance (修实例必问「这形状还有几个兄弟位置」)。
    对照本 Spec 自己的范围纪律模板: #133 (跨仓常量分歧) 与 #134 (sys.path) 都走了「披露 + 开 issue +
    显式不并入」。这一条既没并入也没开号, 是三者中唯一的静默。
  fix_direction: |
    范围纪律上不强求本 Spec 修 CLAUDE.md:81 或新建 custom check (那可能确属越界), 但**静默不是选项**。
    最小处置二选一:
    (i) TASK-019 顺带把 :81 那行改成引用点口径并补上 CLAUDE.md 与 Plugin Version 行 (一行改动, 且该
        任务本就在编辑该文件); 或
    (ii) 开 issue 记「发布同步面 SOT 枚举 + 两条 custom check 的 7 点失明」, 号写进 TASK-020 notes,
         与 #133/#134 同形态。
```

### N6 — `new`

```
- type: issue
  severity: major
  category: documentation
  scope: tasks.md:10 (编号不可变约束自陈) + TASK-016/TASK-017 的 ID 语义漂移
  summary: 「本次只追加 5.5–5.8, 不改动任何既有编号」这句自陈**当场不成立** —— 5.3 与 5.4 的语义都被换掉, TASK-016/TASK-017 两个 ID 被改指到完全不同的工作, 使五份已 commit 的 R1 报告与审计轨里对这两个号的引用全部静默错位。
  evidence: |
    tasks.md:10 逐字: 「**本次 R1-fix 只在组 5 末尾追加 5.5–5.8, 不改动任何既有编号**
    (1.1–1.6 / 2.1–2.3 / 3.1–3.3 / 4.1 / **5.1–5.4** 语义与编号均保持)」。

    对 a52ab81 (A.2/A.3 首版) 实测:
      tasks.md 5.3  旧: 「**主仓同步面 3 项** — gitlink + VERSION 的子模块版本表行 + root README.md 的 Plugin badge」
                    新: 「**aria 子模块分支合并 + 双远程推送**」
      tasks.md 5.4  旧: 「`README.{zh,ja,ko}.md` 的 `translated-from` 标记 ×3」
                    新: 「**主仓** gitlink + VERSION 子模块版本表行 + README.md 两处版本引用」
      yaml TASK-016 旧 title: 「主仓同步面 3 项 — gitlink + VERSION 子模块版本表行 + root README badge」(parent 5.3)
                    新 title: 「aria 子模块分支合并 + 双远程推送 + 逐远端 ls-remote 核验」(parent 5.3)
      yaml TASK-017 旧 title: 「i18n README translated-from 标记 ×3 (#140 B 档: 只更标记不重译)」(parent 5.4)
                    新 title: 「主仓 gitlink + VERSION 子模块版本表行 + README.md 两处版本引用」(parent 5.4)
    ⇒ 5.3/5.4 与 TASK-016/017 都被**原地改指**, 新工作插在中间而非追加在末尾。

    两个实际代价:
    (a) 文件在专门承诺引用稳定性的那一段里陈述了一个关于自己的假事实;
    (b) 所有外部对 TASK-016/TASK-017 的引用现在解析到别的工作 —— 包括五份已 commit 的 R1 报告
        (本席 R1 的 F1/F7 讨论的「TASK-016」是 gitlink 任务, 而 R1-fix 后 TASK-016 是合并任务, 且新
        TASK-016 的 notes 还把本席 F1 的原文搬过去挂在新语义下) 与 audit-trail。
        R2 之后若再有轮次, 「F7 说 TASK-016 漏 gitlink」这句话对着新文件是假的。
    形状 = memory feedback_cross_doc_claim_verify_at_target (跨文档断言须在目标处成立) +
    feedback_audit_trajectory_placeholder_footgun (committed 审计轨与可变交付面同居的 footgun)。
  fix_direction: |
    (1) 把新的合并任务改成 5.9 / TASK-022 并恢复 5.3/5.4 与 TASK-016/017 的原语义 (最干净, 真正兑现
        「只追加」); 或
    (2) 删掉「不改动任何既有编号」这句自陈, 换成显式重映射表: 「R1 报告中的 TASK-016 = 本版 TASK-017;
        R1 的 TASK-017 = 本版 TASK-018」。
    ⛔ 不可保留现状 —— 现状是一句可被一条 git show 推翻的自我描述。
```

### N7 — `new` (根在 R1/F6 附带项)

```
- type: issue
  severity: major
  category: process
  scope: detailed-tasks.yaml TASK-016 agent 分配 + agent_roster
  summary: TASK-016 授权一个 AI agent 无 owner 触点地向两个共享 master 双推 —— 外向且难撤销的写操作, 本项目已成文要求显式确认; 21 个任务里没有任何 `agent: owner`。
  evidence: |
    TASK-016 `agent: backend-architect`; verification 逐字「`git push origin && git push github` 双推已执行」。
    metadata.agent_roster = [qa-engineer, backend-architect, knowledge-manager] —— 无 owner 席。
    memory feedback_sync_instruction_not_push_authorization 逐字: 推共享 master 是外向 + 难撤销,
    须显式确认, 「低风险 doc」不能自我授权跳过。这里推的不是 doc, 是一次 plugin MINOR 发版的
    master 合并, 且要推到 GitHub 公开镜像。
    本项目已有 canonical 拆法: memory feedback_t15_owner_blocking_pattern (AI-runnable 段 + owner-action
    段, AI 段 commit 后 task 留 in_progress), 且同仓姊妹 Spec 就在用
    (phase-c-integrator-ci-path-coverage/detailed-tasks.yaml:100+ 有 `agent: owner` + `gate_condition`
    + 「不得由执行 TASK-001 的 AI 顺带代为标记」)。
    另: aria-orchestrator AD10 把 v2.0 唯一的人类参与点定为 **merge 签字**; 本计划把 merge 交给 AI 且无签字点。
    R1/F6 的附带项 (「TASK-016 承载两条多远程硬约束, 而 roster 里没有 agent 的职责面覆盖子模块/多远程操作」)
    未被处置; TASK-016 是本轮新增任务, 故记 new。
  fix_direction: |
    TASK-016 拆两段: AI-runnable (本地 merge + bump 就绪, 停在推之前, status 留 in_progress) +
    owner-action (双推 + 逐远端 ls-remote 核验, `agent: owner`)。若与 N1(i) 一起把合并交回
    phase-c-integrator, 则由该 Skill 的 C.2.4/C.2.5 承接, 本条自然消解。
```

### N8 — `new`

```
- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-019 verification[0]
  summary: 验收条目把**旧值**写成了断言内容 —— 声称「两处均已更新」而引号里引的是 bump 前的字符串, 字面满足它的方式就是什么都不改。
  evidence: |
    逐字: `- "两处均已更新: 版本区间 (v1.52.0–v1.65.5 已 ship) + 「版本:」行的 插件 aria-plugin v1.65.5"`
    实测 CLAUDE.md:139 = 「aria-plugin 方法论轨: v1.52.0–v1.65.5 已 ship …」, :141 = 「版本: 插件
    aria-plugin v1.65.5 | …」⇒ 引号内两串**正是今天的现状**。
    对照写法正确的同批任务: TASK-017「README.md **两处**版本引用都已更新 (badge + 'Plugin Version:' 行)」、
    TASK-018「三份各 **3 处**版本引用全部更新 (共 9 处)」—— 都只点位置不嵌旧值。
    严重度限于 minor: 主仓侧由 TASK-020 兜 (且主仓侧的排序是对的, 见 N4)。
  fix_direction: 改成「:139 版本区间行的上界 与 :141「版本:」行的插件版本 均已为 v1.66.0」, 不嵌旧串。
```

### N9 — `new`

```
- type: issue
  severity: major
  category: testing
  scope: detailed-tasks.yaml TASK-013 verification (结果判据三条) + deliverables 注释
  summary: 新补的「结果判据」误引 AB_TEST_OPERATIONS.md —— 那条判据不在它声称的「发版前清单」里; 而真被引进来的三条**全属场景 3 全量回归** (28 Skills / ~$14 / 6-8h), 与一个括注 hunk 的 M/6h 任务规格量级不符, 且 summary.yaml 是全量运行产物, 两次先例单 skill run 都没有它。
  evidence: |
    TASK-013 verification 逐字: 「结果判据 (**AB_TEST_OPERATIONS.md 发版前清单**): with_skill 优于 without_skill」。
    实读 AB_TEST_OPERATIONS.md:544-548 —— **发版前**清单恰好四条, 无此项:
      - [ ] Tier 1 Skills **全量** AB 测试已执行
      - [ ] summary.yaml 已生成并审查
      - [ ] 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复)
      - [ ] 与上一次结果比对, 无回归
    「with_skill 表现优于 without_skill」在 :538-542 的**「新增 Skill 后」**清单里 —— 另一张表。
    ⇒ 字段级误引 (memory feedback_written_exception_exact_condition_match: 援引成文判据须逐字核对确切
      触发条件, 非精神/类推)。

    被真正引进来的三条又都锚在场景 3:
      :237-256 「场景 3: 发版前全量回归 … 逐 Skill 执行 … 预估: **28 Skills × ~$0.50/Skill ≈ $14,
                ~6-8 hours**」, 其 step 4 = 「汇总到 ab-results/YYYY-MM-DD/**summary.yaml**」, step 5 =
                「更新 latest symlink」
      :314     「summary.yaml (每次**全量**运行的总览)」
    而 TASK-013 是 complexity M / est_hours 6, 标题「对 SKILL.md:176 的 hunk 照跑 AB」, deliverables 注释
    逐字「本轮结果子目录含 **summary.yaml**」。
    实测两次先例单 skill Rule #6 run 的产物, **均无 summary.yaml**:
      2026-07-20-v1.62.0-phase4-rule6/ → anchors.json assertions.json benchmark.json eval-06 eval-10
        eval-11 grade.py grading-summary.md skill-snapshot-v1.61.0
      2026-07-31-v1.65.0-122-rule6/    → benchmark.json eval-1 eval-2 eval-3 grading-summary.md
        skill-candidate-v1.65.0-SKILL.md skill-snapshot-v1.64.1-SKILL.md
    ⇒ 两种解读都坏: 要么 TASK-013 被静默扩成 28-skill / 6-8h 全量回归 (complexity M / 总 88h /
      关键路径均未反映), 要么该判据按字面不可满足。
    第三条「与上一次结果比对无回归」还与 B 路冲突: :194 要求跨 run 比较须标注 eval_suite_version,
    「修改 eval case 前」清单 :555 逐字「理解: 修改后旧数据**不可直接比较**」⇒ B 路一旦新增定向 eval,
    这条判据自动失效。三条被打包引进来的判据里有一条与另一条互斥。
  fix_direction: |
    (1) 删掉误引, 改为对本 hunk 有意义的判据 (单 skill 双臂: skill-snapshot vs skill-candidate 在**能看见
        该 hunk 的 eval** 上的 delta), 并按两次先例形态列全 deliverables;
    (2) 若确实要求全量回归, 必须显式写出来并同步 complexity / est_hours / DAG (不可留成一句附带判据);
    (3) 与 F9 的三条同批修 —— 单独修任一条都不足。
```

---

## Part 3 — 已核验、**未**构成发现 (留痕, 防下一轮重复投入)

| 核验项 | 结论 |
|---|---|
| 交付顺序: TASK-016 插入 015→017 之间是否制造新顺序错误 | ✅ **顺序本身正确** —— 子模块 bump → 子模块合并 → 主仓 gitlink 指向 post-merge SHA, 与 memory `feedback_submodule_pointer_post_merge_bump` 一致; `scope_boundary.why_group5_is_here` 的论证成立。真正的顺序错误在 TASK-020 (见 N4), 不在 016 的位置 |
| 派生值: S×14 / M×6 / L×1 / 88h | ✅ 逐条重算一致 |
| 派生值: agent 分摊 9/7/5 = 21 | ✅ 逐条重算一致 (R1-fix 修正了上一版的 8/7/6 错算) |
| 关键路径 001→…→020 | ✅ 按 est_hours 重算 67h, 经 010 / 013 / 018 / 019 四条并列路径均为 67h (并列最长, 非错) |
| DAG 注释 ↔ dependencies 字段逐条一致 | ✅ 全 21 条比对通过 (R1 minor 已闭) |
| 17 条 SC 在 TG-1 六任务的覆盖 | ✅ 恰好各一次, 无重无漏 (1/1b/2/3/4 · 5/5b/5c · 6/6b/10 · 11/13/15/14 · 9 · 12) |
| 场景数加总 13+5+15+8+1+3 = 45 == `test_counting_contract.scenario_count` | ✅ 一致; TASK-008 的「12 条」(SC-1..15 列举) 亦逐条点算一致 |
| `co_dependency_note` / `file_domain_serialization` / DAG 三处对 TG-1 串行链与 006 例外的表述 | ✅ 三处互相一致, 无矛盾 |
| **TASK-021 人读层 (5.8) vs 机读层 (dependencies)** | ✅ **一致** —— yaml `dependencies: [TASK-009]`; tasks.md:39 逐字「**5.8 例外: 可在 2.3 之后任意时点执行**…排在末位仅为阅读顺序 —— 依赖字段以 `detailed-tasks.yaml` 为准」; 2.3 == TASK-009 ✓。此前那类「建议不是边」的病本轮未复发 |
| 范围纪律 (拉入方向): TASK-019 改 CLAUDE.md 是否越界 | ✅ **不算越界** —— CLAUDE.md 实测确有两处 plugin 版本引用 (:139/:141), 不改则 ship 后违 Rule #3, 且无任何 custom check 兜 (`claude-md-changelog-free` 只查滚动 changelog 与行数)。真问题是 SOT 枚举本身漏了它 (N5), 不是这个任务多余 |
| 范围纪律: TASK-020 跨仓 grep 是否越界 | ✅ 不越界 —— 只读断言, 无写操作, 且覆盖的正是本 change 自己的交付面 |
| 范围纪律: TASK-021 改 `.aria/repro/` 是否越界 | ✅ 不越界 —— 该脚本是本 Spec 自己产的留证 artifact (proposal:181 声明), 处置自己的产物属本 change 交付面 |
| 范围纪律 (拉入方向) 总评 | ✅ 未发现借修 Critical 夹带无关工作; #133 / #134 / 三件机械工具 / R3' 24 条残留 五处「披露不并入」姿态全部保持。唯一的范围缺口是**该开而未开的 issue** (N5), 属漏做而非多做 |
| `known_env_trap` (#134) 是否仍准确 | ✅ `in_scope: false` 保持; 表述未变 |
| gitlink ↔ 子模块 HEAD | ✅ `git ls-tree HEAD aria` = `af87caee…` == `git -C aria rev-parse HEAD`; 但**子模块处 detached HEAD 无分支** (见 F1) |
| TASK-020 grep 名单外是否有该 bump 而漏的文件 | ✅ 全仓 `grep -rln "1\.65\.5"` = 31 个文件, 减去名单内 11 个 (10 个断言项 + 已排除的 `aria/CHANGELOG.md`) 余 **20** 个, 逐条核**全部属历史/审计/自指**: audit-reports ×10 (含本轮 R2 三席) / docs/handoff ×3 / `.aria/triage-*` ×2 / `.aria/repro/sc-baseline-*.py` (自产留证, 头注写「v1.65.5 工作树」) / 本 Spec 自己的 tasks.md + detailed-tasks.yaml (grep 命令字面) / 另一 Spec 的 proposal / `standards/conventions/secret-hygiene.md:401` (实读为**版本史表格行**「1.1.2 | 2026-08-02 | …同批 co-land aria-plugin v1.65.5」, 保留旧号正确, 且 standards 不在 plugin 发布同步面内) ⇒ 名单在**该更新**这一侧无遗漏; 问题在**不该断言零命中**那一侧 (N2) |

---

## Part 4 — 收敛评估

**本轮 Critical/Major 计数与归因**:

| | Critical | Major | 计 |
|---|---|---|---|
| `carryover` (R1 未闭合) | F1, F9 | F2/F7, F3, F4 | 5 |
| `new` (R1-fix 引入) | N1, N2 | N3, N4, N5, N6, N7, N9 | 8 |
| 合计 | 4 | 9 | **13** |

**fix 引入占比 = 8/13 ≈ 62% > 1/2 ⇒ 已到边际产出转负的拐点** (memory `feedback_audit_marginal_return_goes_negative` 的判据本体)。R1 = 3C+12M = 15 条, R2 = 4C+9M = 13 条, major 数基本持平 (12 → 9, 未显著下降), 同时 62% 是本轮 fix 自造 —— 两个信号一致指向「加轮无用」(memory `feedback_stop_adding_rounds_when_major_count_flattens`: 判据是 major 是否还在降, **换新鲜眼睛 > 加轮**)。

**缺陷已从任务层迁移到 metadata 层**。R1 的问题多是任务缺失/分配错; R2 的新问题集中在新增的 6 个 metadata 块与它们之间的接缝:

- N1 = `scope_boundary` 块**内部**自相矛盾, 且与 TG-5 的任务体相矛盾 —— 这正是 memory `feedback_fixes_contradict_each_other_across_clusters` 的形状: F1 的落点 (合并要有 owner) 与 F3 的落点 (Phase C 委派声明) 各自都对, 但前者违反后者的隐含前提, 接缝落在两个审计角度之间, 多 agent 并行审计天然不覆盖它。
- N2/N3/N4 都长在同一个新任务 (TASK-020) 上: 一个恒红 + 半个维度 + 排在不可逆点之后。这个任务是本轮 fix 对 Critical-1 的**根因修法**, 三处独立缺陷说明它是赶出来的。
- N6 说明 fix 连自己「只追加不改号」的自我描述都没核。

**R3 前的最小修订集** (按承重排序, 建议一次过并做条款间交叉一致性检查):

1. **N1** (Critical) — 合并归属二选一并改正边界表; 让 Rule #8 对 aria 侧不再静默。这条决定 N7 是否自动消解。
2. **N2 + N3 + N4** (Critical + 2 Major) — TASK-020 一并重写: 排除/收窄 `aria/VERSION` · 改正向计数断言 · 按仓面拆成两条并把 aria 侧前移到 016 之前。
3. **F9 + N9** (Critical + Major) — TASK-013 一并重写: 加覆盖度判定前置任务 · B 路配齐 deliverables · 删误引并改用单 skill 双臂判据。⛔ 单修任一条不足 (R1 已警示过一次)。
4. **F1** (Critical carryover) — 补 aria 子模块分支创建任务; TASK-017 的 gitlink 判据改成 `git ls-tree HEAD aria` == `git ls-remote github master` 的机械断言。
5. **N6** (Major) — 恢复 5.3/5.4 原语义并把新任务改 5.9, 或删除自陈 + 加重映射表。
6. **F3 + F4** (2 Major carryover) — 归档门依赖改写成 yaml `status` / done-family `{done, completed}` fail-CLOSED 并定义 TASK-016 何时落; TASK-021 补归档后 FATAL 路径与 (b) 分支的 proposal 引用同步。
7. **N5** (Major) — 开 issue 或顺带修 CLAUDE.md:81 (不可静默)。
8. **F2/F7 残留 + N8** (Major + Minor) — `scope_repos` 主仓 surface 补 `aria-plugin-benchmarks/`; TASK-019 验收条目不嵌旧值。

**对 R3 编排的建议**: 不要原班五席重跑。本轮 13 条里 8 条是 fix 自造, 且 N1 这一类「条款间接缝」按定义落在单席视角之外 —— 建议 R3 只上 2 席**新鲜眼睛**, 且把 R3 的镜头显式限定为 **(a) 条款间交叉一致性** (每条 fix 是否违反另一条 fix 的隐含前提) 与 **(b) 每条新机械断言在健康常态下应该是什么值** (恒红/假绿双向筛查), 而不是再做一遍全面复审。⛔ 同时建议**停止继续往 metadata 加块** —— 矛盾密度已经在那一层。

**vote: REVISE**
