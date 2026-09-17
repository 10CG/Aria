---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T01:14:53.197Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R5 — tech-lead (流程与跨任务结构)

对象: 主仓 master `0e60b08` 的 `tasks.md` (27 checkbox) · `detailed-tasks.yaml` (35 TASK) · `sc11-predicate-validation.py` (24 态 x 19 谓词)。本席为 R5 新派, 前四轮未参与。

counts: **0 Critical / 5 Major / 6 Minor**

---

## 审计结论

### 0. 本席实跑的基线核对 (先于一切判断)

| 项 | 命令 | 结果 |
|---|---|---|
| 验证脚本 | `TMPDIR=<scratch> python3 -B openspec/changes/.../sc11-predicate-validation.py` | `rc=0`; stderr `verdict: OK (mismatch cells 0, stderr notes 0; 24 states x 19 predicates)` |
| 矩阵与 yaml 实测块 | python 逐字节比对 stdout 与 `metadata.sc11_predicate_validation.measured_2026_09_16_at_1cb3872_v5` | `True` (完全一致) |
| 结构不变量 | 解析 yaml: `len(TASK)=35` / `distinct parent=27` / `sum(est_hours)=107.0` / `len(checkbox)=27` / `checkbox 集 == parent 集` / 依赖图无环、无未知依赖 | 全部成立, 与 `metadata.total_tasks=35` `est_hours_total=107` 一致 |
| 组 5 执行序 | 依赖边 TASK-025/026 → 027 → 028 → 029 → 034 → 030 → 031 → 032 | 与 `tasks.md:134` 标题行的顺序逐段一致 |

即: 本轮的 5 个 Major **没有一个**来自「脚本自身坏了」或「数字对不上」, 全部来自跨任务/跨 Skill 的语义接缝。

### 1. R4 处置落地核验 (本席侧重相关的逐条)

| R4 条目 | 处置要求 | 落地? | 证据 |
|---|---|---|---|
| PP4-M1 取号恢复死锁 | 第 4 / 6 步基准改「台账最近一次记录」+ 恢复后追加新记录 + 清单第 22 条 | 是 | yaml:806 「相对台账中最近一次记录的取号时 SHA (首次 = TASK-027 的记录)」+「按 TASK-027 的记录格式在台账追加新的取号时 SHA 与取号值」; yaml:808 「== 台账最近一次记录的取号值」; tasks.md:60 第 22 条 (a) |
| PP4-M2 两仓合并结局不一致 / 本地 master 领先静默放行 | 第 5 步两仓视为整体 + 第 3 步 ff-only 后复核相等 | 是 | yaml:807「任一仓退出码非 0 ⇒ 对两个仓都走下一条的回退条」; yaml:805「ff-only 之后再断言一次两者相等 …… 实测这一支 merge --ff-only 返回 Already up to date. 且退出码 0」 |
| PP4-M3 第 7 步 `--emit-json` 必然 rc=3 | 删该句, 一致性归 TASK-001 | 是 | yaml:810 第 7 步只剩「run_tests.py 全量 + pytest 两腿 + `metadata.sc11_baseline_predicates` 全部谓词」, 无脚本调用; TASK-001 (yaml:195) 保留唯一机械核验点; tasks.md 清单第 27 条 |
| PP4-M4 主仓两端一致恒假 | 交 C.2.5 + 核三项配置事实 + owner_gates 第 11 项补性质 | 部分 | yaml:882 已写委派与三项配置事实, owner_gates (yaml:159) 已补; **但触发前置未建立, 见 M1; 「两个子模块」的事实陈述与 C.2.5 实际枚举面不符, 见 M2** |
| PP4-M5 半推后仍可 bump gitlink | 三处各一句 | 是 | owner_gates yaml:158「两个远端未都核验一致前不进 TASK-030 (不得 bump gitlink)」; TASK-030 yaml:857 前置条; TASK-031 yaml:879 / TASK-032 yaml:909 各补「被拒或只推成一个远端 ⇒ 不 force …… 停下上报」 |
| PP4-M6 (j1)(j2)(j3) 换量 | 平衡括号 + 三个新坏态 + authoring_rules + 合法写法守卫 | 是 | yaml:94-96 三条谓词均为 `g=lambda s: next(... accumulate ...)` 平衡括号实现; 新态 `bad_j1_same_para` / `bad_j3_same_block` / `bad_j2_same_line` / `alt_tuple_wrapped` 实跑各自只 FAIL 对应谓词 (本席实跑矩阵 25-28 行) |
| PP4-M7 (l1) 标题行余部 | `partition(chr(10))[2]` + Scenarios 结构化 + 新坏态 | 是 | yaml:100 `blk=lambda s,h: s.partition(h)[2].partition(chr(10))[2].split(chr(10)*2)[0]` + `len(a)>=4 and any('target_in_subdir' ...)`; `bad_l1_title_paren` 实跑仅 (l1) FAIL |
| m1 owner_gates 补四处止损 | 顶部注明 + 补列 + 第 2 步重执行断言 | 是 | owner_gates yaml:147 注释 + 第 9 项 (yaml:156); yaml:804「本地提交后重新执行本步断言」 |
| m3 tasks.md「须特别留意」纳入两处 fail-closed | — | 是 | tasks.md:74 已写「五处」并点名 TASK-029 / TASK-034 |
| m4 `touchpoints-aria.txt` 与 AB worktree 落 scratchpad | — | 是 | yaml:192 / yaml:726 |
| m5 TASK-026 扩面拆任务的 parent 与 metadata | — | 是 | yaml:738 末句 |
| m6 台账骨架补停下标题 | — | 是 | `verification_ledger.skeleton` (yaml:29) 末尾「停下与上报」, 共 12 个二级标题 |
| m7 第 2 步正向条件可执行式 + 负控写非 0 | — | 形式是, **实质否** | yaml:804 已写 `grep -qE '10CG/aria-plugin#[0-9]+'`, 但该条件在基线上已为真, 见 M4 |
| m8 TASK-029 工时提到 3.5-4h | — | 是 | `est_hours: 4` (yaml:793), 总计 107 与 metadata 一致 |
| m9 第 6 步 CHANGELOG 计数括注改写 | — | 括注改了, **量没改**, 见 M3 |
| m10 读前必看第 14 条同步 | — | 部分: (l1) 已同步, (c2) 未同步, 见 m1 |
| m11 (j4) 左边界 `(^|[^0-9A-Za-z])` | — | 是 | yaml:97 与脚本 `PRED["j4"]` 一致; `alt_j4_numeric` 实跑全 PASS |
| m12 TASK-009 字面量约束收窄 | — | 是 | yaml:347 「源码的路径拼接与前缀剥离逻辑里不新增 …… docstring / 注释里引用该路径说明契约不受此限」 |
| m13 (c2) 收紧 + 已知边界入 handoff | — | 是 | (c2) 改 AST 限域 (yaml:88) + `bad_c2_module_only`; TASK-032 (yaml:907) 列 10 条无隔离态谓词, 与本席按矩阵重算的集合完全一致 |
| m14 补丁 4 具体化 | — | 是 | yaml:525 给出三行具体代码; 本席读 `latest_md_writer.py:299-306` 核对红绿模式成立 (见「核对无误」第 7 条) |
| m15 两臂同码后补跑 | — | 是 | yaml:727 |
| m16 台账行括注统一 | — | 是 | TASK-018 / 023 / 024 括注与同组兄弟一致 |
| 跨簇 4 EXPECTED 收窄 | — | 是 | 脚本 `EXPECTED_FAILS` + `expand_expected()` + rc=4 的定义自检 (`check_doc_lists_states` / 未知标签 / 重复标签 / 状态集顺序) |
| 跨簇 5 判断入清单 | — | 是 | tasks.md 清单第 27-30 条 + 第 22 条 (a)(b) |

---

## Major

### M1 — TASK-031 把主仓推送交给 C.2.5, 但计划从未建立 C.2.5 的触发前置; 计划另一处还明写此时前置不成立

`[Major] type=issue · category=architecture · scope=detailed-tasks.yaml TASK-031 (与 TASK-032 接缝) · v5 引入: 是`

**证据**

C.2.5 的触发条件逐字写在被委派的 Skill 里:

```
$ sed -n '206,211p' aria/skills/phase-c-integrator/SKILL.md
C.2.5 - Multi-Remote Push Enforcement:
  触发条件:
    - Phase C.2 合并成功 (master 已 fast-forward)
    - 配置 phase_c_integrator.multi_remote_push.enabled: true (默认)
```

`SKILL.md:613` 的执行流程第 1 步是 `快照 expected_sha = git rev-parse HEAD (合并后本地 master HEAD)`。

而 `push_all_remotes.sh` 的成功判据是 SHA 比较, 且比较基准取的是**当前 HEAD**, 不是被推的分支:

```
$ sed -n '49p;107p;119p' aria/skills/git-remote-helper/scripts/push_all_remotes.sh
PRE_LOCAL_HEAD=$(git -C "$REPO" rev-parse HEAD)
  PUSH_OUTPUT=$(git -C "$REPO" push "$REMOTE" "$BRANCH" 2>&1) || PUSH_EXIT=$?
  if [ "$PUSH_EXIT" -eq 0 ] && [ -n "$POST_REMOTE_HEAD" ] && [ "$POST_REMOTE_HEAD" = "$PRE_LOCAL_HEAD" ]; then
```

计划里没有任何一步把本地 master 快进到含 PR 合并提交的 `origin/master`。相反, 下游任务明写此刻本地 master 是落后的:

```
yaml:900 (TASK-032 第一条)
'开头先把本地 master 对齐到含 TASK-031 合并提交的 origin/master (TASK-031 走 Forgejo 服务端合并, 本地 master 此时落后): git fetch origin → git checkout master → git merge --ff-only origin/master …'
```

本仓已有 C.2.5 因该前置不成立而不运行的先例 (AB 存档, 非本席推测):

```
$ grep -n 'multi_remote_push' aria-plugin-benchmarks/ab-results/2026-08-16-v1.66.0-137-rule6/eval-2-c2-conflict/with_skill/outputs/answer.md
221:  "multi_remote_push": { "status": "not_run", "reason": "§C.2.5 触发条件为合并成功 (master 已 fast-forward)" },
```

**照计划执行会出的错**: 三支结局, 没有一支能满足 TASK-031 写的断言 (`C.2.5 的 per-remote 矩阵对 origin 与 github 两个 remote 均推送成功且 verify_parity_post_push 的 match 为 true`):

1. 执行者按触发条件字面判定前置不成立 ⇒ C.2.5 `not_run` ⇒ 断言无从判定, 主仓 master 从未推到 github, 而计划里主仓第一次 github 推送要等到 TASK-032 的 Phase D 提交 —— PP4-M4 要治的病原样复发, 只是从「恒假」变成「被跳过」。
2. 执行者仍调用, 而 HEAD 停在 feature 分支 ⇒ `PRE_LOCAL_HEAD` = feature tip, 推的是陈旧的 `master` ⇒ `POST_REMOTE_HEAD != PRE_LOCAL_HEAD` ⇒ 两个 remote 全 `success=false` ⇒ `fail_on_partial_push` 阻断 ⇒ 停在本步。
3. 执行者仍调用, 而 HEAD 在陈旧的本地 master 上 ⇒ origin 非快进被拒 (success=false), github 「Everything up-to-date」且 `POST_REMOTE_HEAD == PRE_LOCAL_HEAD` ⇒ **success=true** ⇒ 得到一个「github 成功、origin 失败」的矩阵, 与现实完全相反 (真实情况是 origin 有合并提交、github 没有), 这正是 memory `assert-this-action` 说的「上游遗留同形状物让根本没发生的动作假绿」。

**建议改法** (一行前置 + 一行断言, 不新增流程层):

- TASK-031 在 C.2.5 那一条之前插入前置: `git fetch origin → git checkout master → git merge --ff-only origin/master → 断言 git rev-parse HEAD == PR 合并提交 SHA (不能快进即停下上报)`, 并把 TASK-032 第一条改写为「若 TASK-031 已对齐则本步为幂等复核 (Already up to date. 可接受), 仍须跑 `git merge-base --is-ancestor <TASK-031 的合并提交> HEAD`」。
- 或者放弃委派、退回 PP4-M4 之前的手工路径但补上失败口径。**不建议**, 因为 C.2.5 的 per-remote 矩阵与 parity 重试本身是好东西, 缺的只是那一行前置。

---

### M2 — C.2.5 的子模块循环枚举三个子模块 (含 `aria-orchestrator`), 计划写「两个子模块」; 该仓有 github remote, 落在 owner_gates 之外

`[Major] type=risk · category=architecture · scope=detailed-tasks.yaml TASK-031 · v5 引入: 是`

**证据**

C.2.5 第 2 步与第 4 步 a 的枚举面:

```
$ sed -n '614p;617p;618p' aria/skills/phase-c-integrator/SKILL.md
2. 枚举子模块: `git submodule status --recursive`
   - a. 遍历子模块, 调用 `git-remote-helper.push_all_remotes(SUBMODULE.path, SUBMODULE.branch, [REMOTE])`
   - b. 子模块推 REMOTE 任一失败 → 按失败优先级决策 (见下), 阻断则跳过本 REMOTE 的主仓库推送
```

实测枚举结果与 `aria-orchestrator` 的 remote 配置:

```
$ git submodule status --recursive
 1cb387218935433312fde4067c276754b77686a8 aria (v1.73.1-10-g1cb3872)
 237045ac2cfed9849c201e18434e9f6cb9036ab5 aria-orchestrator (heads/master)
 8b4956242d74b24400aa8e62bca020f0233eb0f2 standards (heads/master)

$ git -C aria-orchestrator remote -v
github  git@github.com:10CG/aria-orchestrator.git (fetch)
github  git@github.com:10CG/aria-orchestrator.git (push)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/aria-orchestrator.git (fetch)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/aria-orchestrator.git (push)
```

计划的事实陈述:

```
yaml:882 (TASK-031)
'C.2.5 第 4 步 a 会先遍历子模块推同一 remote: 此时两个子模块的 master 已由 TASK-034 推完, 该步应为幂等无新对象, 若它报出子模块有待推内容即与 TASK-034 的核验矛盾, 停下查明'
```

**照计划执行会出的错**: `aria-orchestrator` 从来不在本 cycle 的 scope (`metadata.scope_repos` 只有三项: aria / standards / 主仓), 也不在 TASK-034 的推送范围, 但它在 C.2.5 的推送循环里。执行时点 (M6 自主跑在制, CLAUDE.md 项目状态列了 `feature/m6-dispatch-input-delivery` 等在制分支) 有两种结局:

1. 若其本地 master 领先某个远端 ⇒ C.2.5 把**他轨未推送的提交**推到 origin 与 github。这是一次外向推送, 不在 `metadata.owner_gates` 的 16 项里, 违反本计划自己的硬约束 `metadata.hard_constraints`「外向动作 …… 执行前逐项请 owner 授权」, 也正是 memory `sync≠push-auth` 的形状 (「保持同步」不等于推共享 master 的授权)。`aria-orchestrator` 按 CLAUDE.md 是不对外发布的内部实现, 推到 github 后不可撤销。
2. 若其推送失败 (网络 / 分叉) ⇒ 按失败优先级阻断该 REMOTE 的主仓推送, 而计划给执行者的诊断词是「与 TASK-034 的核验矛盾, 停下查明」—— 一个必然误导的根因指向 (memory `reporter-miscite` 同形: 症状字段的真实产者不是计划认定的那个)。

今天的取值不触发 (`git -C aria-orchestrator rev-list --left-right --count origin/master...HEAD` = `0 0`, 且 `refs/remotes/github/master` 与 `refs/remotes/origin/master` 同为 `237045a`), 所以这不是「必然」而是「条件成立即不可逆」, 故定 Major 而非 Critical。

**建议改法**: TASK-031 的 C.2.5 条改两处 —— (a) 把「两个子模块」改为「三个子模块 (aria / standards / aria-orchestrator)」并写明本 cycle 只对前两个负责; (b) 执行前加一条前置断言: `对 aria-orchestrator 逐 remote git ls-remote 与本地 master 比对, 不一致即停下请 owner 裁 (本 cycle 不推他轨仓)`, 或在调用 C.2.5 前把 `enforced_remotes` / 子模块范围显式限定并把该限定记台账。

---

### M3 — TASK-029 第 6 步的 CHANGELOG 节计数断言检不出它自称要防的那个失败

`[Major] type=issue · category=testing · scope=detailed-tasks.yaml TASK-029 第 3 / 6 步 · v5 引入: 部分 (公式沿自 v4, v5 按 R4 m9 只改写了括注理由)`

**证据**

```
yaml:805 (第 3 步末) '…… 记下两个子模块此刻的 origin/master SHA 与 aria CHANGELOG 的 grep -c ''^## \['' 计数'
yaml:808 (第 6 步)   '…… 且合并树 aria CHANGELOG 的 grep -c ''^## \['' 不少于第 3 步所记计数 (防第 4 步 fail-closed 后经 owner 确认的手工解冲突丢掉对方发版小节 ……)'
```

三态实跑 (临时目录, 已删):

```
master                   count=3
merged_good              count=4      # 本方小节加入, 对方小节保留
merged_dropped_peer      count=3      # 本方小节加入, 对方小节被解冲突丢掉  ← 要防的正是这个
merged_dropped_both      count=2

--- 判据: merged_count >= master_count ---
merged_good              PASS (4 >= 3)
merged_dropped_peer      PASS (3 >= 3)   ← 目标失败形态被判 PASS
merged_dropped_both      FAIL (2 >= 3)
```

**照计划执行会出的错**: 第 4 步 fail-closed 后由 owner 确认的手工解冲突若丢掉对方发版小节 (同时加入本方小节), 计数恰好持平, 第 6 步放行, 打 tag、推送、bump gitlink 全部照常 —— 丢掉的那一节随发版永久进入 `aria/CHANGELOG.md`。这是 memory `feedback_rationale_formula_contradiction_is_signal` 的教科书形态: 理据句点名的场景, 公式检不到; 也是 `redfix-change-quantity` 说的「在同一个量上挪阈值」(计数只能捕捉净减少, 捕捉不到等量替换)。

**建议改法** (换量, 一行): 把「不少于」改成集合包含 —— `第 3 步另记下 master 上全部 '^## \[' 标题行的原文集合; 第 6 步断言合并树的标题行集合是其超集, 且恰多出本方的一行 (差集大小 == 1 且该行为本次取号的号)`。命令形态: `comm -23 <(git show <第3步SHA>:CHANGELOG.md | grep '^## \[' | sort) <(grep '^## \[' CHANGELOG.md | sort)` 输出必须为空。

---

### M4 — TASK-029 第 2 步「standards 占位已清」的正向条件在基线上已为真, 对其目标恒真

`[Major] type=issue · category=testing · scope=detailed-tasks.yaml TASK-029 第 2 步 · v5 引入: 是 (R4 m7 处置落地)`

**证据**

```
yaml:804 '…… 对 git -C standards show <standards feature 分支>:conventions/session-handoff.md 的同一份输出三条都要成立:
          grep -c ''#<'' 为 0 · grep -qE ''10CG/aria-plugin#[0-9]+'' 成立 …… · 含第三态从句'
```

基线 (standards `8b49562`, 即本 cycle 一行未改的状态) 实测:

```
$ grep -c '#<' standards/conventions/session-handoff.md
0
$ grep -nE '10CG/aria-plugin#[0-9]+' standards/conventions/session-handoff.md
6:> **Forgejo Issue**: [10CG/Aria#92](…) / [10CG/aria-plugin#94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94) (双子星防重复, §2.3.8)
```

第 2 个条件由文件头 `:6` 一条**与本 cycle 无关的既有引用**独立满足, 与 TASK-023 写没写占位、TASK-025 回填没回填毫无关系。

**照计划执行会出的错**: 该条件的用途是「确认占位 `#<…>` 已被真号替换」, 但它无法区分「替换成真号」与「把占位连同跟踪指针一起删掉」。回填提交若误删整句 (只保留第三态从句), 三条全过, 合并放行, standards 上留下一个**没有跟踪去处**的已知缺口 —— 而 `10CG/aria-plugin` 的遗留 issue 是决策单 §2 第 2 行第 (2)(4) 问的落点。这是 memory `assert-this-action`:「验动作发生了须钉本次新产生的对象, 不能钉状态存在」。

顺带记一笔: 这一条是执笔人忠实照抄 R4 聚合报告 m7 给出的表达式 (`grep -qE '10CG/aria-plugin#[0-9]+'`) 的结果 —— 缺陷在处置而非落地, 与 R4 主控自查里 PP4-M3 的自省同形 (只看判据逻辑, 没看它要判的输入长什么样, memory `verify_predicate_inputs_exist`)。

**建议改法**: 把正向条件钉到本次改动产生的那句话上, 而不是整份文件。例如 `sed -n '/经机械 latest_md_writer 写入时/,+3p'` 取第三态从句所在段, 在该段内 `grep -qE '10CG/aria-plugin#[0-9]+'` (回落形态则在该段内 grep 「已知缺口, 尚未开跟踪 issue」); 并同批把「自然负控」改成对同一段落的 `#<` 计数。

---

### M5 — TASK-029 第 5 步没有「本轮确实产生了合并提交」的正向断言, 第 7 步的前提因此自指

`[Major] type=issue · category=implementation · scope=detailed-tasks.yaml TASK-029 第 5 / 7 / 8 步 · v5 引入: 部分 (v5 只堵住了「本地 master 领先」这一个成因)`

**证据**

```
yaml:807 (第 5 步) '…… git -C aria merge --no-ff <aria feature 分支>, standards 同形 …… 两仓的合并 SHA 记台账。
   任一仓退出码非 0 ⇒ …… 理由: 一仓合成功另一仓冲突时, 成功那仓的合并提交留在 master 上无人处理,
   重走时 --no-ff 会返回 Already up to date. 而不产生本轮的合并提交'
yaml:810 (第 7 步) '仅当 git -C aria status --porcelain 为空且 git -C aria rev-parse HEAD 等于合并 SHA 时 ……'
```

第 5 步的理据句自己点名了「`Already up to date.` 退出码 0 而不产生合并提交」这一形态, 但 v5 只在第 3 步补了针对**本地 master 领先**这一个成因的复核; 另一个成因 —— `origin/master` 本身已包含 feature 分支 (子模块被服务端合并过; CLAUDE.md 多远程硬约束 1 记录该事故 2026-07-14 真实发生过, `#165` 三次复发) —— 第 3 步的「master == origin/master」断言照过, 第 5 步 `--no-ff` 返回 `Already up to date.` 退出码 0, 回退条不触发。

而第 7 步的前提是「HEAD 等于**合并 SHA**」, 合并 SHA 的定义就是第 5 步之后记下的 HEAD ⇒ 在本任务内部这条前提近乎恒真, 起不到守卫作用。

**照计划执行会出的错**: 第 5 步不产生任何提交 ⇒ 台账记下一个假的「合并 SHA」(其实是第 3 步的 master SHA) ⇒ 第 6 / 7 步在该树上全绿 ⇒ 第 8 步把 `v<vNEXT>` tag 打在一个**不是本轮产生**的提交上 ⇒ TASK-034 推送 tag。内容碰巧是对的 (feature 已是祖先), 但发布记录、台账与审计报告引用的合并 SHA 全部指向一个本轮没做过的动作, 事后按 SHA 复核会得出错误结论。

**建议改法** (一句): 第 5 步在「两仓的合并 SHA 记台账」之后补 —— `逐仓断言 git rev-parse HEAD != 第 3 步记下的该仓 SHA 且 git rev-parse HEAD^2 == 该仓 feature 分支 HEAD (本轮确实产生了双父合并提交); 不成立即按回退条处置后停下上报`。这与回退条已有的前置判据同形, 只是把它从失败路径搬到正路径上做一次。

---

## Minor

| 编号 | 内容 | 证据 | 建议 |
|---|---|---|---|
| m1 | 读前必看第 14 条对 (c) 仍写「前两条同原文 (c1)(c2)」, 未随 v5 把 (c2) 从整文件 grep 收紧到 `_list_handoff_files` 自己的 docstring 同步 (与 R4 m10 完全同类, m10 只修了 (l1)) | `tasks.md:31`「(c) 前两条同原文 (c1)(c2) ……」; v5 diff 显示该行改了 (l1) 段但 (c) 段未动; `git diff edd256d 0e60b08 -- …/detailed-tasks.yaml` 第 59/60 行显示 (c2) 由 `grep -q 'path relative to' <file>` 改为 AST 限域 | 第 14 条 (c) 改为「(c1) 同原文; (c2) 收紧为 `_list_handoff_files` 自己的 docstring 含 `path relative to`, 只写进模块 docstring 不算」 |
| m2 | AI 流程判断清单第 22 条 (b) 写「四处止损停摆」, 括注实列六处 | `tasks.md:60`「…… 只需知情的四处止损停摆 (TASK-029 第 2 / 3 / 7 / 8 步 · TASK-034 同名 tag · TASK-032 开头 ff-only)」; owner_gates 第 9 项 (yaml:156) 同为六处 | 「四处」改「六处」 |
| m3 | TASK-031 要核的三项 C.2.5 配置事实, 漏了失败优先级表里**优先级最高**的 `read_only_remotes` | `SKILL.md:628`「remote ∈ `read_only_remotes` \| warning 降级, 继续 (最高优先级)」; 本仓 `.aria/config.json` 无 `multi_remote_push` 块, 默认 `[]`, 故当前不触发 | 三项配置事实加第四项「`read_only_remotes` 为空 (非空则「半推阻断」这句不成立)」 |
| m4 | 未要求记录 C.2.5 是否走 `git-remote-helper` 降级路径 | `SKILL.md:640`「不可用时用内联降级 (不重试, 简化实现)」; 本仓 `aria/skills/git-remote-helper/SKILL.md` 在位且 `ARIA_PLUGIN_ROOT` 未设 ⇒ 不降级。降级下 `verify_post_push.py` 的 4 次 backoff (0/2/4/8s) 消失, Forgejo 复制延迟下 match=false 概率上升 | 配置事实再加一项「helper 在位 (`test -f` 输出记台账), 未走内联降级」 |
| m5 | TASK-029 第 1 步 fetch 失败无对应停下条目 | owner_gates 第 9 项只列第 2 / 3 / 7 / 8 步 | 第 9 项括注补「第 1 步 fetch 失败同此」 |
| m6 | TASK-031「合并后核台账所记各主仓提交 SHA 均为 `origin/master` 的祖先」未写明先 fetch | yaml:880; `origin/master` 是远端跟踪 ref, 不 fetch 即陈旧 (memory `freshness-must-be-fetched`) | 该句补「先 `git fetch origin`, 或直接对 `git ls-remote origin master` 取到的 SHA 判祖先」 |

---

## 实施者试派生 (照文本落地, 看会不会卡住)

1. **TASK-029 第 1 至 8 步**: 第 1-4 步可无歧义执行 (fetch / porcelain / checkout+ff+复核相等 / 取号复核基准已明确为「台账最近一次记录」)。卡点在第 5 步: 文本只说「退出码非 0 ⇒ 回退」, 没说退出码 0 但无新提交怎么办 (M5); 第 6 步的 CHANGELOG 条我按字面执行会在目标失败上判 PASS (M3)。其余可落地。
2. **TASK-030**: 前置「TASK-034 对两个远端均已 ls-remote 核验一致」可直接判; 16 个版本点逐处 `grep -n` 可执行; `VERSION:24` 的特例已写死。无卡点。
3. **TASK-031**: 前三条 (有范围核验 / 已跟踪核验 / 写法自检) 可落地, 交付物路径清单完整 (与 TASK-030 的 10 个 deliverables 逐一对齐, 本席核对一致)。卡点在 C.2.5 那一条: 我按字面走到「执行前先核对三项配置事实」没问题, 但走到「断言 per-remote 矩阵两个 remote 均 match=true」时必须临场决定「要不要先把本地 master 快进」——计划没说, 而下游 TASK-032 说此刻它是落后的 (M1)。另外「两个子模块」与实际枚举面不符, 我会按字面只查两个 (M2)。
4. **TASK-032**: 27 行勾选规则、5.5 的父目录 token 替换、归档门预演三条 unverified_claims、Step 7 授权分支、归档后台账路径, 全部可落地。`release_gate` 与 Phase D 双推的授权并批已在 owner_gates。无卡点。
5. **TASK-001** (额外一个, 因为它是全链基线): 前置 / 回落支 / 三处 `origin/master` 实测 / 41 触点 diff / 脚本 rc 口径 / 19 条谓词基线全假 —— 逐条可执行, 且本席实跑证实脚本在当前基线上 rc=0、19 条在基线态全 FAIL (矩阵 base 行)。无卡点。

---

## 核对无误的部分

1. **SC-11 谓词族**: 24 态 x 19 谓词实跑零 mismatch、零 stderr; yaml 实测块与脚本 stdout 逐字节一致。R4 两席各自构造的三个绕过态 (`bad_j1_same_para` / `bad_j3_same_block` / `bad_j2_same_line`) 与标题行括注态 (`bad_l1_title_paren`) 现在各自只 FAIL 对应谓词; 合法写法守卫 `alt_tuple_wrapped` / `alt_j4_numeric` / `alt_j3_anchor` 全 PASS, 无假红。**换量成功**, 本席未能构造出新的绕过 (平衡括号是结构量, 不是位置量)。
2. **EXPECTED_FAILS 收窄**: 断言强度未降 —— `expand_expected()` 把未列谓词一律展成 PASS, 逐格比对; 另有 rc=4 的四类定义自检 (状态集与顺序 / 未知标签 / 重复标签 / docstring 漏列)。加一态确实只需一行。
3. **结构不变量**: 35 TASK / 27 parent / 27 checkbox / 依赖图无环、无未知依赖 / `est_hours` 合计 107 == `metadata.est_hours_total`。
4. **依赖图与执行序**: 组 5 的拓扑序与 `tasks.md:134` 标题行逐段一致 (5.3 与 5.5 并行 → 5.1 aria 侧 → 5.6 → 5.2 合并 → 5.2 推送 → 5.1 主仓 → 5.2 PR → 5.4)。TASK-026 的 with 臂 SHA 取自 TASK-021 回归前快照, 而 TASK-021 依赖 TASK-024, 故 TASK-024 若落编辑也已进 with 臂 —— 无时序倒挂。
5. **C.2.5 的三项配置事实属实**: `.aria/config.json` 的 `phase_c_integrator` 只含 `pre_merge_gate` 块, 无 `multi_remote_push` 覆盖 ⇒ `enabled` 默认 true; 顶层无 `multi_remote` 键 ⇒ `enforced_remotes` 空 ⇒ 自动发现, 主仓实测 remote 恰为 `origin` 与 `github`; `SKILL.md:630` 失败优先级表确为 `fail_on_partial_push: true` 默认阻断。委派对象**确实做**计划声称的三件事 (per-remote 矩阵 `SKILL.md:616-621` / `verify_parity_post_push` 走纯读 `git ls-remote refs/heads/<branch>` 带 4 次 backoff / 半推阻断并输出修复命令) —— 缺的只有触发前置 (M1) 与枚举面 (M2)。
6. **AB 判据**: `delta.pass_rate` 的符号方向经本席实读 `aggregate_benchmark.py` 证实 —— `configs = [k for k in run_summary if k != "delta"]` 的顺序来自 `sorted(config_dir)`, `delta = configs[0] − configs[1]` (`:208-214`); 故 `new_skill`/`old_skill` 得 new−old, `with_skill`/`old_skill` 得 old−with。计划写死的口径与「with 臂须排在前」的告警都正确。逐 eval 回归判据 (复跑两次、三样本 ≥2 仍劣) 与止损 (阻断 TASK-027 / TASK-029) 自洽; 两臂「代码 + 文档整体」口径与 memory `ab-input-baseline` / `ab-baseline-leaks-via-repo-corpus` 都对上了。
7. **TASK-018 补丁 4 的红绿模式成立**: 实读 `latest_md_writer.py` 的 `n_active == 1` 支为 `content = _render_pointer(active_tracks[0], now)`, 布局 6 (缺 `filename` 键) 走同一支; 补丁按 `rel = t.get("rel_path") or t.get("filename")` 判, 布局 6 的 track 带 `rel_path` ⇒ `rel != None` ⇒ 不覆写 ⇒ `missing_filename` 保住, 与计划声称的「顶层与缺 rel_path 键两个布局翻红而 (d)(e) 不动」一致。
8. **TASK-032 的已知边界清单准确**: 无单点隔离态的 10 条 `(a1)(b)(c1)(f1)(f2)(i1)(i2)(j5)(l2)(l3)` 与本席按 v5 矩阵重算的集合完全一致; (c2) 已正确移出该清单 (新增 `bad_c2_module_only`), (g) 由 `bad_changelog_only` 反向隔离的说法也对。
9. **owner_gates 16 项**与各任务文本双向对应, 无悬空条目; tasks.md「五处须特别留意」与 v4/v5 新增的两处 fail-closed 一致。
10. **组 1-4 的 24 个任务**: 本席按流程与跨任务结构的镜头复核 (提交点归属 / 并发面 / 依赖边 / 台账去处), 未发现 Major。TASK-033 的收口提交点、TASK-018 的副本生命周期证据、TASK-021 的回归前干净树断言, 三者构成的「组 3 与组 4 并发但互不污染」的结构是成立的。

---

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical / 5 Major / 6 Minor。

5 个 Major 全部落在组 5 发布段的两个任务 (TASK-029 / TASK-031) 上, 与 R4 的分布事实一致 (缺陷集中在发布段)。其中 M1 / M2 是 v5 为修 PP4-M4 而新引入的跨 Skill 接缝, M3 / M4 是「判据对目标恒真」, M5 是「缺 this-action 断言」。五条的修法合计约 6 句话, 无一需要重构。组 1-4 本轮继续零 Major。

## Vote

**REVISE**

投 REVISE 是对文本的判断: 组 5 的五处若不改, 执行者会在 TASK-031 卡住并临场裁决 (M1 / M2), 并在 TASK-029 拿到两个判不出问题的绿灯 (M3 / M4) 和一个可能打错位置的 tag (M5)。

但这与我的边际判断**不冲突**: 我不建议再加审计轮。这五条都是「主控读完本报告直接落笔 + 一次机械复核」就能收掉的, 不需要五席再跑一遍。

---

## 边际判断

### 1. 这份计划现在是否足以开始 Phase B?

**是, 可以现在开 Phase B, 组 5 的五处修正作为 Phase C 的准入条件。**

依据:

- 本轮 5 个 Major 的 scope 全部是 TASK-029 与 TASK-031, 即 5.2 (子模块合并 / 主仓 PR)。Phase B 走的是组 1 至组 4 (TASK-001 至 TASK-024、TASK-033、TASK-035), 共 26 个任务、约 79h, **本轮与 R4 连续两轮零 Major**, 且 R4 有两席 (backend-architect 真仓实验 + knowledge-manager 字节级核对) 投 PASS。
- 本席对组 1-4 做了流程镜头的独立复核 (提交点归属 / 并发面 / 依赖边 / 台账去处), 也未发现 Major; 试派生了 TASK-001 / TASK-030 / TASK-032 与 TASK-029 / TASK-031, 只有后两个有卡点。
- 组 1 的入口 (TASK-001) 我实跑验证过: 脚本在当前基线 rc=0, 19 条谓词 base 行全 FAIL, yaml 实测块可复现 —— 实施者第一天就能拿到确定的绿/红信号。
- 风险隔离干净: 组 5 的缺陷不会污染组 1-4 的产出 (它们只影响合并与推送动作本身), 所以「B 期照跑、C 期前补五句」在工程上是安全的排法, 也避免继续用审计轮阻塞 79h 的实现工作。

### 2. 若继续加轮, 下一轮会找到什么类型的问题? 值不值两轮成本?

**类型可以预测: 仍是 (a) 跨 Skill / 跨任务边界的隐含前置未建立, (b) 正向断言可被上游遗留的同形状物满足。不值两轮。**

- 本轮 5 个 Major 里, M1 / M2 完全由 v5 引入 (为修 PP4-M4 而生), M4 由 v5 落地 R4 的处置文本而生 ⇒ **本轮 fix 引入的 Major 占比 3/5**, 已越过 memory `marginal-return-negative` 给的拐点判据 (> 1/2)。R4 是 3/7, R3 是 7/9 —— 这个比例没有单调下降, 说明每修一轮就在新表面上长一轮的规律仍在。
- 而且缺陷面正在从「计划内部」迁到「计划与既有 Skill 的接缝」。接缝类缺陷靠加审计轮找的效率最低 (R4 五席里只有 tech-lead 一席去读了 C.2.5 的 SKILL.md, 而且只读了配置项没读触发条件), 靠一次定向核对 (去被委派的 Skill 源码里逐条核「触发条件 / 枚举面 / 失败口径」) 的效率最高。
- 两轮成本 ≈ 10 份席位报告 + 两次 rework + 主控核验, 大致等于本 Spec 组 1 的全部工时; 而剩余缺陷的期望收益是「再抓 2-4 个同类接缝问题」, 这些问题在 Phase C 执行时会以「停下上报」的形式暴露 (计划的 fail-closed 设计本来就是为此), 代价远低于两轮审计。

### 3. 有没有比「继续加轮」更能降低剩余风险的做法?

有三条, 按性价比排:

1. **把发布段整体降级为「按 `phase-c-integrator` 执行 + 本 Spec 三条特有约束」, 不再在计划里复述八步。** 本 Spec 真正特有的只有三条: 子模块一律本地 `--no-ff` 合并 (CLAUDE.md 硬约束 1) · 推后逐 remote `ls-remote` 核验 (硬约束 2) · gitlink 只从双端均已核验的 SHA 前进。其余 (fetch / 干净树 / ff / 取号 / tag / 回归) 都是 `phase-c-integrator` 与 `branch-manager` 本就该做的事, 复述一遍就多一套会自己长缺陷的文本 —— R3 至 R5 的 21 个 Major 里, 落在这段复述上的占了大半。降级后 M1 / M2 / M5 这三类「与被委派 Skill 的接缝」会从计划文本里消失, 变成执行期的一次配置核对。
2. **把「新写的机械断言必须先在基线上跑负控」提升为本 Spec 的一条通用规则, 挪到执行期 (TASK-001) 统一做一次**, 替代逐条审计。本轮的 M3 / M4 都是「新断言在基线上就已经是绿的 / 检不出目标失败」, 与 memory `spec-acceptance-needs-baseline-run` 完全同形 —— 这类缺陷用「逐条读」找很贵 (R4 五席全漏了 M4, 因为它要求去 standards 文件里实跑一次), 用「所有新断言一律先跑基线三态」找很便宜。具体落法: TASK-001 的 verification 加一条「本计划新写的每一条 shell / python 断言 (TASK-029 第 2 / 3 / 6 步、TASK-030 前置、TASK-031 的 C.2.5 断言) 各在 B.1 基线上跑一次, 逐条记下取值; 任何在基线上就已为真的断言先修再进组 2」。
3. **对被委派的 Skill 做一次定向的「三问核对」并写进台账**, 而不是靠审计席碰巧去读。三问 = 触发条件在我这一步成立吗 / 它遍历的对象集合与我以为的一样吗 / 它失败时会发红还是静默。本轮 M1 与 M2 正是这三问的第一、二问的答案。这条可以直接写成 TASK-031 的一条 verification, 成本是执行期十分钟。

最后一句给 owner 的三选一: 按本席判断, **「接受当前结论 + 主控落五句修正 + 开 Phase B」** 优于「加两轮」, 也优于「降级为单轮」—— 单轮再跑一次还是会在同一片 200 行文本上找同一类问题, 而这五条的修法已经逐条写在上面, 不需要再发现一次。

---

## 轮次记录

| 轮 | Major | Vote | 分布 |
|---|---|---|---|
| R1 | 13 | — | 全域 |
| R2 | 9 | — | 全域 |
| R3 | 9 | — | 全域 |
| R4 | 7 | REVISE 3 / PASS 2 | 组 5 发布段 5 · SC-11 谓词族 2 · 组 1-4 零 |
| **R5 (本席)** | **5** | **REVISE** | **组 5 发布段 5 (TASK-029 三条 / TASK-031 两条) · SC-11 谓词族 零 · 组 1-4 零** |

- **趋势**: 13 → 9 → 9 → 7 → 5, 仍在降, 但降幅趋缓; 本轮 fix 引入占比 3/5 (R4 为 3/7), 未继续下降。
- **谓词族本轮清零**: PP4-M6 / M7 的换量与结构化被本席实跑证实有效, 且未引入假红。SC-11 这条线可以认为收敛。
- **剩余缺陷全部同源**: 5 条里 4 条是「与被委派对象 / 与上游既有事实的接缝」(M1 M2 M4 M5), 1 条是「量选错」(M3)。这是一个可以一次性处置的类, 不是一个需要多轮收敛的面。
- **本席临时目录**: `/tmp/claude-1000/-home-dev-Aria/3d294e0c-5181-450f-9b0e-140b2710f7a7/scratchpad/r5-tech-lead/`, 审计结束时已清空; 仓内除本报告外零写入。
