---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T15:36:10.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [completeness-lens]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — completeness lens (新鲜眼睛, 单镜头)

> **镜头**: 只审「枚举是否完整」。范围 = `tasks.md` **## 5. 整段** + `detailed-tasks.yaml` 的 `TASK-014` / `TASK-022..028` / `metadata` 各块; 参照 `proposal.md §Impact`。
> **HEAD**: `72923de` (主仓) / `af87cae` (aria)
> **不报**: 组 1–4 本体 · 委派/兜底是否真被执行 (另一席) · 已修的四条 (发版面文件数口径 / breakdown 缺 aria 侧 / sc-baseline 两条失效路径 / proposal 指针 2→3)

---

## 0. 枚举清点 — 组 5 范围内逐处 (共 26 处) 与独立核实结论

| # | 枚举位置 | 声称 | 独立求出 | 结论 |
|---|---|---|---|---|
| 1 | `metadata.version_reference_surface.main_repo_points` | 14 | 14 (`git grep -n "1\.65\.5" -- . ':!openspec' ':!docs/handoff' ':!.aria'`) | ✅ 一致 |
| 2 | 同 `.aria_side_normal_points` | 4 | 4 (`git -C aria grep -n`) | ✅ |
| 3 | 同 `.total_normal_points` | 18 | 18 | ✅ |
| 4 | 同 `.breakdown` 9 个文件 | 9 键 / 14+4 点 | 9 文件, 逐文件点数逐一吻合 | ✅ |
| 5 | `two_classes_of_file.normal_reference.files` | 9 | 9 | ✅ |
| 6 | 同 `.append_only_ledger.files` | 2 | 2 | ✅ 分类对, **阈值错** → **C2** |
| 7 | 同 `.append_only_ledger.invariant` (b) 阈值 | `aria/VERSION ≥2` | 正确 bump 后必为 1 | ❌ **C2 critical** |
| 8 | 同 `.append_only_ledger.invariant` (a)「头部当前版本行」 | 覆盖 aria/VERSION 全部当前版本声明 | aria/VERSION 有**两处**当前版本声明 (`:3` + `:56-58` `## 版本号` 块 = **1.47.0**) | ❌ **M10** |
| 9 | 同 `.enabled_check_blindness` 「7 处」 | 两条 check 失明 7 处 | 主仓 14 点中仅 4 点被覆盖 ⇒ 失明 **10** 点 | ❌ **M6** |
| 10 | 「两条 enabled custom check」 | 2 | enabled check 实为 **8** 条, 与版本相关 3 条; 另有 `readme` collector `version_match` 覆盖 `aria/README.md` | ⚠️ **m3** (custom check 数对, 「唯一维度匹配」不成立) |
| 11 | 两个白名单是否构成 fail-CLOSED 分区 | (隐含穷尽) | 无「整仓 grep 差集必须落在白名单内」步骤 | ❌ **M9** |
| 12 | `TASK-023` 「14 个引用点 (1+2+3+3+3+2)」 | 14 | 14 | ✅ |
| 13 | `TASK-022` 5 文件 / marketplace 2 点 (`:3`/`:16`) | 5 / 2 | 5 / 2 实读确认 | ✅ |
| 14 | 发版同步面是否含 git tag | 未提 | `version-management.md §4.3` 逐字点名 aria 插件为**分发型**要求 VERSION==tag | ⚠️ **m1** |
| 15 | `metadata.scope_boundary` 的 in/out 分区 | 合并/双推/gitlink **不在本文件** | `TASK-028` 明文承载它们 | ❌ **C1 critical** |
| 16 | `tasks.md` 范围边界表 (`:42`) + 交接段 (`:46`) | 同上 | 同上 | ❌ **C1** |
| 17 | DAG 节点集「只画 active 20 条」 | 20 | active **21**, 缺 `TASK-028` | ❌ **M1** |
| 18 | DAG 关键路径 | …→024→026 | 真终点 028 | ❌ **M1** |
| 19 | DAG 「真并行组: {011, 012}」 | 1 对 | **32** 对 (传递闭包实算) | ❌ **M2** |
| 20 | DAG 派生值机械重算命令覆盖面 | (隐含全覆盖) | 只覆盖 complexity/工时/agent 三条, 不覆盖节点数/并行组/关键路径 | ❌ **M1** 同因 |
| 21 | `active 复杂度 S×14·M×6·L×1 / 88h / agent 10·7·4` | — | 实算完全一致 | ✅ |
| 22 | `total_tasks: 28 = 21 active + 7 cancelled` | 28/21/7 | 实算一致; `is_spec_complete` 实跑读出 **21/21 unchecked** | ✅ (R3-fix 的删除线处置有效) |
| 23 | CANCELLED 台账 `superseded_by` ×7 | 7 条 | `TASK-016`/`TASK-017` 两条指向已被 R3-fix 推翻的接收方 | ❌ **M4** |
| 24 | `5.2`–`5.8` 正文引用清扫 | (隐含已扫净) | `tasks.md:180` 仍引 **5.8** (CANCELLED) | ❌ **M8** |
| 25 | `file_domain_serialization` 文件清单 (2 文件) | 2 | 多任务文件恰 2 个; 32 并行对中 **0 对同文件** | ✅ |
| 26 | `known_env_trap.impact_on_this_spec` 影响面 | test_collision.py + 连带 test_coordination_ref_lib.py; 全量 run_tests.py 为准 | pytest collect 实跑: 恰 2 个 ERROR, 就这两个; 宿主 `test_release_by_track.py` 单模块跑 34 tests OK (不受影响) | ✅ 完整 |
| 27 | `TASK-014` 基线 1322 / 9 OK / 1698 | 1322 / 9 OK / 1698 | 实跑 `Ran 1322 tests / OK`; `run_all_tests.sh` → `9 OK / 0 FAIL / 0 SKIP (累计 1698)` | ✅ 逐字吻合 |
| 28 | 「既有 6 条测试逐字不改」 | 6 | 文件实有 **34** 个既有 test 方法; 那 6 个在删掉行号锚后**全文无处点名** | ❌ **M3** |
| 29 | 各任务 `deliverables` 穷尽性 | — | `TASK-013`/`025`/`027` 三条各漏自己 verification 强制要改的文件 | ❌ **M5** |
| 30 | `TASK-025` dangling 清扫面 (proposal.md 3 处) | 1 文件 3 处 | 引用该脚本的交付面文件还有 `tasks.md`、`detailed-tasks.yaml` | ❌ **M7**; 且 `:181` 一行含 2 处 occurrence → **m2** |
| 31 | `TASK-027` Tier-1 要求引用点 (`:397` + `:545`) | 2 | 第三处 `:483`; 且 `tasks.md:158` 写成 `:396` (实为 `:397`) | ⚠️ **m5** |
| 32 | `scope_repos[].head` | 主仓 `2cf2569` | 实际 `72923de` (落后 1) | ⚠️ **m4** |
| 33 | `agent_roster` 3 / `task_groups` 5 / 17 SC / 45 场景 | 3 / 5 / 17 / 45 | 全部实算一致 (45 = 13+5+15+8+1+3, 逐 SC 从 proposal 表独立重推) | ✅ |

---

## 1. Critical

```
- 枚举位置: detailed-tasks.yaml:52-77 (metadata.scope_boundary.delegated + why_group5_is_here)
           + tasks.md:42 (范围边界表行) + tasks.md:46 (组 5↔Phase C 交接段)
  声称覆盖: 本文件的 in/out 分区总体 —— 「哪些事在本文件做、哪些委派出去」
  独立求出: 逐处实读 4 个位置的原文, 与 TASK-028 / 5.15 的原文并列:
    · yaml:54-57  delegated[phase-c-integrator].what = "aria 子模块分支合并 + 双远程推送 +
      逐远端 ls-remote 核验 (C.2.5) + 主仓 gitlink bump + PR 创建 + pre-merge gate"
    · yaml:75     why_group5_is_here = "**合并 / 双推 / gitlink 不在本文件** (见 delegated)"
    · tasks.md:42 「aria 子模块合并 + 双远程推送 | phase-c-integrator C.2.5, **不在本文件**」
    · tasks.md:46 「由它做 aria 子模块合并 + 双推 + 主仓 gitlink bump + PR + pre-merge gate。
      gitlink 必须指向合并后的 master SHA, 这条约束随交接一并移交, 由 C.2.5 的既有机制保证」
    ↕ 对立面:
    · TASK-028 (5.15) 承载: 本地 merge + 双推 + 逐远端 ls-remote + 主仓 gitlink bump
    · TASK-026 (5.13) verification 逐字: "⛔ **未**把 aria 子模块的合并动作 / 双推 /
      ls-remote 核验 / gitlink bump 交出去 —— 那些由 TASK-028 承载"
  差集: R3-fix 把合并/双推/ls-remote/gitlink **收回本文件** (新增 5.15/TASK-028), 但四处
        「范围分区」枚举一处未改, 仍把它们列在 delegated 侧。⇒ TASK-028 的整个主题在
        scope_boundary 这个分区里落在**错误的桶**里, 而 in_this_file 那一侧也没提它
        ("Phase B 实施 (组 1-4) + 版本引用面编辑与双向断言与留证处置")。
        附带: delegated.why 仍逐字复述「该 Skill (SKILL.md:242) 本就建模子模块合并」——
        这正是 TASK-026.notes 自己判定为**误引**、R3 四席独立命中的那句 (`:242` 实为
        Path coverage 评估的执行上下文契约)。撤回写在 TASK-026, 原句留在 metadata。
        同源残留还有 tasks.md:117 (5.3 → "见 5.13", 应为 5.15) 与 tasks.md:118
        (gitlink "归 5.13", 应为 5.15), 以及组 5 标题/Group Overview 行未含「合并」。
  单位是否匹配错误维度: 否 —— 分区枚举的单位应是「工作项」, 但这四处是按 R2-fix 的
        旧委派决定写的**决定快照**, 从未随任务集重求。错误维度 = 任务集变化, 无向的
        「有没有写委派段」检查对它免疫 (memory feedback_invariant_dimension_must_match_error_dimension)。
  severity: critical (会致验收假绿 + 复现事故)
    理由: `scope_boundary` 是给执行者/Phase C 读的权威分区且出现在文件最前部。读它的
    执行者会认为合并+双推+gitlink 已委派 ⇒ 跳过 TASK-028 ⇒ 走 phase-c-integrator 的
    真实合并链 (C.2.4:253 → branch-manager → `Do: merge` 服务端合并) ⇒ 本地 master 从未
    fast-forward ⇒ 主仓 bump gitlink 即 orphaned gitlink, GitHub clone --recursive 断裂
    (2026-07-14 事故)。TASK-028 的存在理由就是防这个, 而分区枚举把它注销了。
```

```
- 枚举位置: detailed-tasks.yaml:136-145 (metadata...append_only_ledger.invariant (b))
           + TASK-024 verification 第 3 条 (:777) + tasks.md 5.11 第 2 类
  声称覆盖: 「aria/VERSION 里旧版本号应有的命中数」总体 —— 断言为「旧值命中数不减
           (aria/VERSION ≥2, aria/CHANGELOG.md ≥1)」
  独立求出: 逐版本实测 aria/VERSION 与 aria/CHANGELOG.md 的命中数
    for v in 1.65.5 1.65.4 1.65.3 1.65.2 1.65.1 1.65.0 1.64.0; do
      grep -c "$v" aria/VERSION; grep -c "$v" aria/CHANGELOG.md; done
      → VERSION:  1.65.5=2  1.65.4=0  1.65.3=0  1.65.2=1  1.65.1=1  1.65.0=0  1.64.0=1
      → CHANGELOG:1.65.5=1  1.65.4=3  1.65.3=2  1.65.2=3  1.65.1=1  1.65.0=2  1.64.0=1
    结构实读: aria/VERSION 的 2 次命中 = `:3 > **版本**: 1.65.5` (当前版本行) +
    `:4 > **发布日期**: 2026-08-02  # patch: v1.65.5 收尾 …` (发布注)。
  差集: 阈值 `≥2` 取的是**当前版本**的命中数, 而它要判的是**旧版本**的命中数。
        `:3` 那一处按 TASK-022 的编辑程序 (「只改头部当前版本行 + 追加本次发布注,
        历史行原样保留」) **必须**被改成 1.66.0 ⇒ 正确 bump 后 1.65.5 只剩 `:4` 降级后的
        1 次 ⇒ `≥2` **必然判红 = 恒红**。实测佐证: 没有任何一个已发布旧版本靠降级机制
        拿到 2 次命中 (1.65.4/1.65.3/1.65.0 甚至是 0 —— 那两轮根本没降级保留发布注;
        1.64.1 的 2 次是别的发布注里顺带提了它, 属偶然)。
        更硬的一点: **(a) 与 (b) 在 TASK-022 的程序下互斥** —— (a) 要求 `:3` == 1.66.0,
        (b) 要求 1.65.5 仍出现 ≥2 次, 二者只能靠「在新发布注里硬提一次旧版本号」这种
        任意动作凑, 不是 022 写的程序。
  单位是否匹配错误维度: 否 —— 单位应是「历史行的命中数」, 实际取的是「历史行 + 当前
        版本行的命中数」。总体求错了一格。
  severity: critical
    理由: 这是 R3-fix 为杀 TASK-020 的恒红而新写的 invariant, 它自己是第二个恒红 ——
    memory feedback_fix_recurs_in_its_own_fallback_path 在本 Spec 的第三次实证; 且
    恒红与假绿同为零信息量 (feedback_false_green_dual_is_permanent_red), 本 Spec 全程
    在打这个对偶。而恒红的实际后果比零信息更坏: 唯一能凑绿的路径是「不降级 / 把旧版本
    号硬塞进新发布注」, 正是 (b) 当初被加进来要阻止的「销毁发布史凑绿」的镜像。
    最小修法: (b) 改为 **绝对下界而非「不减」** —— 断言 `发布日期(旧)` 族里对 1.65.5 的
    命中 ≥1 (即降级动作发生过), 并显式排除 `:3` 当前版本行; 或直接改判「bump 前的
    `发布日期` 行内容逐字出现在 bump 后的 `发布日期(旧)` 族中」。
```

---

## 2. Major

```
- 枚举位置: detailed-tasks.yaml:890-918 (依赖图 DAG 注释块)
  声称覆盖: active 任务节点全集 —— 逐字「只画 active 20 条 (TASK-015..021 已 cancelled)」;
           另含「关键路径」与自证命令
  独立求出: yaml 解析 → active = 21 条 (['TASK-001'..'014','022'..'028']);
           DAG 注释块内出现的任务号 (sed 890,915 | grep -oE '\b0[0-9][0-9]\b' | sort -u)
           = 001-014,022-027 (015/021 仅出现在「已 cancelled」那句里)
  差集: **TASK-028 完全不在 DAG**。声称 20 与实际 21 的差恰是它。连带:
        「关键路径: …→024→026」止于 026, 而 028 依赖 026 ⇒ 真终点是 028;
        `:916-918` 那条「不要靠人工重算, 跑这条命令」只重算 complexity / 工时 / agent
        三条, **不覆盖**节点数、真并行组、关键路径 —— 而两次成文订正史 (「S×12/M×4/67h」
        与「Agent 8/7/6」) 恰好都落在被覆盖的三条里 ⇒「机械核验拦住了」这个教训对未被
        覆盖的三条根本没生效, 现在这三条全是错的。
  单位是否匹配错误维度: 否 —— 机械开关的作用域 ≠ 派生声明的集合
        (memory feedback_mechanization_knob_must_match_granularity)。
  severity: major
```

```
- 枚举位置: detailed-tasks.yaml:907 「真并行组 (不同文件): {011, 012}」
  声称覆盖: active 任务里所有可真并行的组合
  独立求出: 对 21 个 active 任务的 dependencies 求传递闭包, 取无祖先关系的对
           → **32 对**。例: {006,008} {006,009} {006,010} {006,011} {006,012} {006,013}
           {006,025} {006,027} {009,011} {009,012} {009,013} {010,025} {011,025}
           {012,025} {013,025} {014,025} {014,027} {022,025} {022,027} {023,025}
           {023,027} {024,025} {024,027} {025,027} …
  差集: 漏 31 对。特别是 TASK-025 与 TG-3/TG-4/TG-5 前段几乎全可并行 (DAG 图里那条
        `009 ──▶ 025` 支线自己就画出了这个并行, 文字总结却没算进去)。
  单位是否匹配错误维度: 否 —— 单位应为「无祖先关系的任务对」, 实际写的是「作者当时
        想到的那一对」。
  severity: major
    理由: 该行是 A.3 排程与「同文件碰撞是否已检查过」两件事的依据。所幸我实算 32 对里
    **0 对同文件**, 故 `⛔ 无同文件并行边` 这条结论是真的 —— 但它是**碰巧**真, 不是被
    这个枚举证成的。枚举只覆盖 1/32 时, 它对同文件碰撞的证明力等于零。
```

```
- 枚举位置: tasks.md:66 组 1 段首 + TASK-001 verification 第 4 条 + TASK-014 verification 第 4 条
           (三处逐字「既有 6 个 test 方法名与函数体逐字未变 (git diff 核, 非行号区间核)」)
  声称覆盖: 宿主文件 test_release_by_track.py 里的「既有测试」总体 = 6
  独立求出: grep -cE "^\s*def test" aria/skills/state-scanner/tests/test_release_by_track.py
           → **34** 个既有 test 方法, 分布在 8 个 class。
           被删掉的旧行号锚 `:206-247` / `:527-575` 对应的恰是
           TestLinkedIssueOverlaps 的 4 个 (:224/:232/:236/:245) +
           TestPhase1GateLinkedIssueCli 的 2 个 (:533/:563) = 6。
  差集: 那 6 个**从未被点名** —— R1 的 minor fix 把行号锚换成「内容锚」时, 删掉的正是
        全文里唯一能识别这 6 个是哪 6 个的东西, 而没有补上方法名或 class 名。
        剩下 28 个既有 test 方法不在任何枚举里, 其「不得改动」的地位无声明。
  单位是否匹配错误维度: 否 —— 「6」这个数只在「行号区间」这个单位下有定义, 换成
        「方法名」单位后它的指称对象消失, 而数字被原样保留。
  severity: major
    理由: 验收项不可执行 (git diff 核**哪** 6 个?), 且两个实现者会得相反结果 ——
    一个核 34 个 (安全), 一个核「6 个」时因为文件里有 34 个而无从下手或随便挑
    (memory feedback_spec_underdetermination_two_implementer_test)。修法一行:
    写成「TestLinkedIssueOverlaps 4 个 + TestPhase1GateLinkedIssueCli 2 个」。
```

```
- 枚举位置: detailed-tasks.yaml:545 (TASK-016.superseded_by) + :577 (TASK-017.superseded_by)
           + :546-547 / :578-579 两条 cancel_reason
  声称覆盖: 7 条 cancelled 的接收方总体 (「原条的全部要求去哪了」)
  独立求出: 逐条核 7 个 superseded_by 与现行任务的 verification 原文, 并与
           tasks.md:20-28 的 old→new 重映射表并列
           · TASK-015 → TASK-022 ✅ (5 文件 + MINOR + CHANGELOG 措辞三项均在 022)
           · TASK-016 → yaml 写 "phase-c-integrator C.2.5"; tasks.md 表写 "TASK-028
             (合并+gitlink)" ⇒ **两层冲突**, 且 yaml 那一侧是 R3-fix 明文推翻的方案
           · TASK-017 → yaml 写 "TASK-023 (版本面) + **TASK-026 (gitlink)**";
             TASK-026 自己的 verification 逐字说 gitlink **不**由它承载, 是 TASK-028
             ⇒ **yaml 内部自相矛盾**; tasks.md 表写 "TASK-023 + TASK-028" (对)
           · TASK-018/019 → TASK-023 ✅ · TASK-020 → TASK-024 ✅ · TASK-021 → TASK-025 ✅
  差集: 7 条里 2 条指错接收方, 且错的方向一致 —— 都停在 R2-fix 的委派语义上。
        cancel_reason 同源残留 ("gitlink 随合并一并移交 Phase C")。
  单位是否匹配错误维度: 是 (单位=每条 cancelled), 但**清扫未跑完** —— tasks.md 的
        重映射表更新了, yaml 的台账没有。跨层不一致本身就是本 Spec 三轮反复的形状。
  severity: major
    理由: 「编号不可变 + 含义冻结」的全部价值就是台账可信; 台账指错时, 读旧报告的人
    按 yaml 换算会换到一个 R3-fix 已否决的方案上。
```

```
- 枚举位置: TASK-013.deliverables (:474) · TASK-025.deliverables (:797-798) ·
           TASK-027.deliverables (:845-846)
  声称覆盖: 各任务实际会改/会产出的文件总体
  独立求出: 逐条把 verification 里**强制要求的落地动作**与 deliverables 对表
    · TASK-013: verification 末条要求「覆盖外 → 三件套齐备 (点名行为 + **可证伪定向
      fixture** + 套件缺口 issue)」。实测定向 fixture 的家是
      `aria-plugin-benchmarks/ab-suite/` (先例: `ab-suite/phase-c-integrator-pre-merge-
      gate-fixtures/NEG-3-*.json`, `ab-suite/state-scanner.json`)。deliverables 只有
      `ab-results/` ⇒ 走三件套那条分支时的产出面不在枚举里。
    · TASK-025: verification (b) 逐字要求「同批修 **proposal.md** 的 3 处 artifact 指针」
      + 「脚本移出 .aria/repro/」(⇒ 产生一个新的存档位置)。deliverables 只有那个脚本
      ⇒ proposal.md 与存档目的地都不在枚举里。
    · TASK-027: 成文披露一个 Rule #6 门范围决定。CLAUDE.md 规则 #6 要求这类处置
      「须在 **spec/tasks** 留 rule6_note」, 而 proposal.md:165 正有 rule6_note 段。
      deliverables 只有 `.aria/decisions/` ⇒ rule6_note 的更新不在枚举里。
  差集: 3 个任务各漏 1-2 个文件, 三例同形状。
  单位是否匹配错误维度: 否 —— deliverables 按「主产物」枚举, 而错误维度是「verification
        会强制改动的全部文件」。
  severity: major
    理由: deliverables 是 file_domain_serialization 与碰撞检测的输入 (metadata 自己
    这么说), 也是 `spec_complete` 的 `_extract_deliverables_for_parent` 的输入。漏项使
    「谁和谁同文件」的判断建立在不完整的文件集上; 且 memory
    feedback_scoped_git_add_splits_claim_from_landing 的病灶正是「声称面 ≠ 落地面」。
```

```
- 枚举位置: detailed-tasks.yaml:125-128 (enabled_check_blindness) + tasks.md:142 +
           proposal.md:271 — 三处同抄「**7 处**残留旧版本时两条 check 仍全绿」
  声称覆盖: 两条 enabled check 的失明点集
  独立求出: 主仓 14 点 − 被覆盖的点
           · m6-version-badge-match 覆盖 README.md badge = 1 点
           · i18n-readme-translation-currency 覆盖 zh/ja/ko 的 translated-from = 3 点
           ⇒ 覆盖 4 点, 失明 = 14 − 4 = **10 点**:
             README.md `Plugin Version:` 1 + i18n×3 的 (badge + `Plugin Version:`) 6
             + **CLAUDE.md 2** + **主仓 VERSION 1**
           aria 侧另有 `marketplace.json` 2 点零覆盖。
  差集: 「7」只统计了 README 家族的失明点, 漏 CLAUDE.md 2 + VERSION 1 (aria 侧再 2)。
  单位是否匹配错误维度: 单位对 (引用点), **总体框错了** —— 取的是「README 家族的
        失明点」而声明的是「两条 check 的失明面」。
  severity: major
    理由: 这个数字是 TASK-024 存在理由的量化依据, 三份文档同抄。TASK-024 断言的是全
    18 点, 故不产生假绿; 但「漏 7 处」是本 Spec R1 的 Critical-1 本体, 而现在描述该
    Critical 规模的数字自己又少算了 3 —— 同一形状第四次, 且这次落在**解释**层。
```

```
- 枚举位置: TASK-025 verification 第 3 条 (:802) — 「同批修 proposal.md 的 **3 处**
           artifact 指针 (:181 / :183 / :219) 避免 dangling」
  声称覆盖: 脚本移位后会 dangling 的指针总体
  独立求出: git grep -c "sc-baseline-linked-issue-normalization" 全仓
           → 16 个文件。按性质分:
           · **交付面 (必须同批改)**: proposal.md(4 occ / 3 行) ·
             **tasks.md:146** · **detailed-tasks.yaml (:692 cancelled + :798 deliverables)**
           · append-only 史 (正确排除): 11 份 .aria/audit-reports/* ·
             docs/handoff/2026-08-08-*.md · 脚本自身
  差集: 枚举只含 proposal.md; **tasks.md 与 detailed-tasks.yaml 这两个交付面文件的
        引用不在枚举里** —— 而它们恰好不是审计史, 不能用「审计史与交付面分离」豁免。
  单位是否匹配错误维度: 否 —— 单位是「proposal.md 里的处数」, 错误维度是「全仓非
        审计史引用数」。正确的求法是 git grep 而不是读 proposal.md。
  severity: major
```

```
- 枚举位置: tasks.md:180 「唯一可当作证据的是 `sc-baseline-*.py` —— **但见 5.8**: 它在
           实现落地后会恒红, 必须处置。」
  声称覆盖: (指针) 现行处置任务
  独立求出: grep -nE "(^|[^0-9.])5\.[2-8]([^0-9]|$)" tasks.md → 命中 :12 :14 :60 :100
           :116-122 :180。前面各处都是在谈「取消」这件事本身 (合法); **:180 是唯一一处
           把 5.8 当**现行任务**引用**。而 5.8 已 CANCELLED, 对应现行任务是 **5.12**。
  差集: 「把 5.2–5.8 的正文引用换成新编号」这次清扫漏 1 处 (1/1 的漏率 —— 需要改的
        就这一处)。
  单位是否匹配错误维度: 是 (单位=引用处), 清扫未跑完。
  severity: major
    理由: 顺着它走会落到「CANCELLED, 勿复用」段; 且这份文件已两次因编号语义问题写下
    撤回声明 (:12 与 :16), 第三次同类残留在同一文件里。
```

```
- 枚举位置: detailed-tasks.yaml:130-147 (two_classes_of_file 两个 files 白名单) +
           TASK-024 verification 前两条
  声称覆盖: 需要断言的版本引用文件全集 (9 普通 + 2 账本)
  独立求出: 两个白名单对**当前** 1.65.5 的分布是完整的 (核实见清点表 #1-#5)。但断言
           的构造是**两个正向白名单, 没有「其余」分支**: 没有任何一步做
           `git grep -l "1\.65\.5"` 求全集再检查差集是否为空。
  差集: 结构性差集 —— 任何**未来新增**的引用点 (新 i18n README / 新 docs 页 / 新
        skill README / 新 badge) 落在两个白名单之外时, TASK-024 全绿。
  单位是否匹配错误维度: 否 —— 正向枚举对「新值/漏项」天然 fail-OPEN
        (memory feedback_invariant_needs_failclosed_default: 枚举分区必须 fail-CLOSED
        = 显式豁免白名单 + 其余阻断)。
  severity: major
    理由: 本 Spec 的原始缺陷正是「按错误单位枚举 ⇒ 漏 7 处」。R3-fix 修的是**实例清单**
    (把 18 点列全), 没修**机制** —— 下一次新增引用点会原样复发
    (memory feedback_fix_the_class_not_the_instance)。
    最小修法: 在 TASK-024 加一条 —— `git grep -l "1\.65\.5"` (两仓) 的结果集必须是
    {两个白名单} ∪ {显式历史白名单: docs/handoff/, .aria/, openspec/,
    aria-plugin-benchmarks/} 的子集, 否则红。这一条把正向枚举变成分区, 且成本一行。
```

```
- 枚举位置: detailed-tasks.yaml:138-140 append_only_ledger.invariant (a)
           「头部「当前版本」行 == plugin.json」+ TASK-022 verification 第 2 条
  声称覆盖: aria/VERSION 里的「当前版本声明」总体 = 1 处 (头部)
  独立求出: sed -n '50,60p' aria/VERSION →
             `## 版本号` 段的围栏代码块 `:56-58` 内容为 **1.47.0**
           grep -n "1\.47\.0" aria/VERSION → :16(历史注) :32(历史注) **:58(裸声明)**
           对照主仓 VERSION 的同构位置: `:3 版本: 1.7.3` 与 `:9 ## 版本号 → 1.7.3`
           **两处保持一致** ⇒ 该 `## 版本号` 块在本项目的 VERSION 文件里是「当前版本
           声明」而非历史行。
  差集: aria/VERSION 有 2 处当前版本声明, 枚举只取 1 处; `:58` 已陈旧 18 个版本
        (1.47.0 vs plugin.json 1.65.5), 直接违反 CLAUDE.md「派生文件必须与 SOT 一致」。
        yaml 的 `why` 字段**看见过**这一行 (「`:58` 还有裸 1.47.0」) 却把它当历史证据
        用来论证「不要做零命中」, 从未问它自己该不该 bump。
  单位是否匹配错误维度: 否 —— 「头部」这个限定词把单位从「当前版本声明」缩成
        「文件第一处声明」, 恰好把那处漂移排除在断言之外。
  severity: major
    理由: invariant (a) 是这一类文件唯一的判据, 而它会在一个与 SOT 矛盾的文件上判绿
    = 假绿。且这条陈旧行**已经造成过生产缺陷** (aria/VERSION 自己的发布注记载:
    v1.56.1 修 aria-report「grep VERSION 人类可读快照 (恒命中围栏代码块冻结串 1.47.0,
    污染所有生成 issue 的版本字段 + 连带 triage 版本筛失效)」—— 当时的修法是绕开
    VERSION 改读 plugin.json, 陈旧行本体从未修)。
    最小可接受处置: 要么纳入 TASK-022 一并 bump, 要么在枚举里**显式声明**它出范围
    并指向那段历史 —— 不能靠「头部」两个字静默排除。
```

---

## 3. Minor

```
- 枚举位置: TASK-022 / tasks.md 5.9 的 aria 侧发版面 (5 文件 / 4 点)
  声称覆盖: aria 插件的发版同步面
  独立求出: standards/conventions/version-management.md §4.3 逐字:「**分发型组件
           (如 aria 插件 — 市场/下游按 tag 拉取)**: VERSION 文件必须与 Git Tag 保持
           一致 … 3. 打对应的 Git Tag」; §6.2 步骤 3/4 同。
           实测反面证据: `git -C aria tag | wc -l` = 10, 最新 **v1.21.3** (≈45 个版本
           前即停); `aria/.claude-plugin/marketplace.json` 的 source 为
           `{"source":"url","url":".../aria-plugin.git"}` —— **不按 tag 拉**,
           按 §4.3 自己的判据「有下游按本仓 tag 拉取 → 分发型」它已不成立。
  差集: 枚举零处提 tag, 也无「本次不打 tag」的声明。
  单位是否匹配错误维度: —
  severity: minor
    理由: 实质上 tag 已事实退役且有 §4.3 判据支撑, 不构成漏做。但按
    memory feedback_written_exception_exact_condition_match「N 次非正式援引 ≠ 成文
    lane」, 这是第 N 次不声明地偏离一条**逐字点名本组件**的成文要求 —— 与 TASK-027
    对 Tier-1 门范围的处理方式 (披露 + 开 convention issue) 是同一形状, 却没同样处理。
    一行声明即可闭合。
```

```
- 枚举位置: TASK-025 verification (:802) 「proposal.md 的 **3 处** artifact 指针
           (:181 / :183 / :219)」
  声称覆盖: proposal.md 里指向该脚本的处数
  独立求出: grep -c (按行) = 3; grep -o | wc -l (按 occurrence) = **4**
           —— `:181` 一行含两处: markdown label `[\`.aria/repro/…py\`]` 与
           链接目标 `(../../../.aria/repro/…py)`。
  差集: 按行 3, 按 occurrence 4。
  单位是否匹配错误维度: 否 —— 单位是「行」, 而移位后要改的是每一处 occurrence。
        这正是本 Spec 反复强调的「文件数/行数 ≠ 引用点数」下沉一层。
  severity: minor (label 与 href 同行相邻, 实际漏改概率低; 但计数口径与本 Spec 自己
        的原则不一致, 且 R3-fix 刚把这里从「2 处」改成「3 处」)
```

```
- 枚举位置: TASK-019.notes (:643-645, cancelled 但结论被 TASK-023 继承) +
           TASK-024 notes 「本条是唯一维度匹配的判据」
  声称覆盖: 现有机械覆盖面 —— 「无任何 custom check 兜 (claude-md-changelog-free 只查
           滚动 changelog 与行数)」/「两条 enabled check」
  独立求出: 解析 .aria/state-checks.yaml → enabled check 共 **8** 条:
           issue-cache-freshness · silknode-contract-deferral-expiry ·
           m6-version-badge-match · **m6-claude-md-version** · m6-arch-doc-stale ·
           i18n-readme-translation-currency · claude-md-changelog-free ·
           coordination-gate-invocation
           其中 `m6-claude-md-version` 就是「Verify CLAUDE.md top-level version field」
           —— 一条查 CLAUDE.md 版本字段的 check (查的是顶层 2.0.0 而非插件版本, 故
           结论仍成立, 但「无任何 custom check」是在未枚举 check 集的情况下断言的)。
           另: state-scanner `collectors/readme.py:60` 产出
           `.readme.submodules.aria.version_match` = (aria/README.md 版本 ==
           plugin.json 版本), 实测 snapshot 里为 true —— 这是**第三个维度匹配的机制**,
           覆盖 18 点里的 `aria/README.md`。
  差集: 相关机制 3 个 (+1 collector 信号), 枚举 2 个; 「唯一维度匹配」不成立。
  单位是否匹配错误维度: —
  severity: minor (方向是**多**了覆盖而非少了, 不致假绿; 但「唯一」这类全称句在本
        Spec 已被证伪过一次 (proposal SC-3 的「唯一」), 同形状)
```

```
- 枚举位置: detailed-tasks.yaml:25-33 metadata.scope_repos[].head
  声称覆盖: 两仓的基线 SHA
  独立求出: 主仓声称 `2cf2569`, 实际 HEAD `72923de` (git rev-list --count 2cf2569..HEAD
           = 1); aria 声称 `af87cae`, 实际 `af87cae` ✅
  差集: 主仓落后 1 提交。该字段的注释自陈「R3-fix 时更新 (R2-fix 版停在 a52ab81,
        落后 2 提交)」⇒ 同一字段第二次漂移。
  单位是否匹配错误维度: 否 —— 一个必须手工跟每个 commit 的字段结构上保证漂移
        (memory feedback_freshness_must_be_fetched_not_measured 的同族: 新鲜度不能靠
        手写维持)。
  severity: minor (建议改成「A.2 定稿时基线 <SHA> (仅供追溯, 不保证 == HEAD)」或删)
```

```
- 枚举位置: TASK-027.notes 「AB_TEST_OPERATIONS.md:397 … 发版前清单 :545」+
           tasks.md:158 「`AB_TEST_OPERATIONS.md:396` 逐字为…」
  声称覆盖: 「Tier 1 全量必测」这一要求在手册里的出处
  独立求出: grep -n "Tier 1" aria-plugin-benchmarks/AB_TEST_OPERATIONS.md
           → :243 (执行顺序) · **:397** (「Tier 1: 核心 Skills (10 个, 每次发版必测)」)
           · **:483** (「每次发版前跑 Tier 1 全量 AB 测试 (场景 3)」) · **:545** (清单)
           Tier 1 表逐行实读 = **10 个** skill, state-scanner 在内 ✅ (数字正确)
  差集: 出处 3 处 (:397/:483/:545), 枚举 2 处; 且 tasks.md 写 `:396`, 实为 `:397`
        —— 两层引用不一致, 人读层错。
  单位是否匹配错误维度: —
  severity: minor
```

---

## 4. 核实为**完整/正确**的枚举 (供收敛判断)

这些我用独立方法求过总体, 与文中数字吻合, **不需要动**:

1. `main_repo_points: 14` / `aria_side_normal_points: 4` / `total_normal_points: 18` / `breakdown` 9 键逐文件点数 — `git grep` 两仓独立求出, 逐点吻合; 且主仓无「已陈旧到不含 1.65.5」的插件版本引用点 (对 `1\.(5[0-9]|6[0-9])\.[0-9]+` 全仓扫过, 剩余命中全在 handoff/decisions/user-stories/ab-results 等历史面)。
2. **主项目版本 (1.7.3) 正确地不在枚举内** — 实测近 6 次 `chore(release)` 的 VERSION diff 只改子模块表行, 从不 bump 主项目版本 ⇒ 排除有先例支撑 (它自己另有 9 个引用点)。
3. `TASK-023` 的 14 点分解 (1+2+3+3+3+2) 与 deliverables 6 文件 — 完整。
4. `marketplace.json` 2 个 version 字段 (`:3`/`:16`) — 实读确认。
5. `total_tasks: 28 = 21 active + 7 cancelled`; `parent` 与 checkbox 21↔21 双射; `complexity S×14·M×6·L×1 / 88h`; `agent 10·7·4` — 全部实算一致。
6. **CANCELLED 的加粗删除线处置有效** — 实跑 `spec_complete.is_spec_complete()` 读出 `21/21 unchecked`, 证实 R3-fix 消除了「完工后恒 7/27」的归档门永久失效。这是本轮唯一一处「机械工具实跑复验通过」的声明。
7. `file_domain_serialization` 2 个文件清单 — 多任务文件恰 2 个, 且 32 个并行对里 **0 对同文件**, 故 `⛔ 无同文件并行边` 成立。
8. `known_env_trap` 影响面 — pytest collect 实跑恰 2 个 ERROR (test_collision.py + test_coordination_ref_lib.py), 与描述逐字一致; 宿主 `test_release_by_track.py` 单模块跑 34 tests OK, 不受陷阱影响 ⇒ 组 1 的落盘宿主选得对。
9. `TASK-014` 三个基线数 — 实跑 `Ran 1322 tests / OK` + `9 OK / 0 FAIL / 0 SKIP (累计 1698)`, 逐字吻合。
10. 17 条 SC / 45 场景 — 从 proposal `## Success Criteria` 表独立重推 (13+5+15+8+1+3=45), 且组 1 的 6 个任务对 17 条 SC 是双射无遗漏; proposal 里另出现的 SC-7/SC-8a/8b/8c 已随 Q6 整体移出 §移出范围, 正确地不在组 1 内。
11. Tier 1 = **10 个** skill (逐行实读), state-scanner 在内 — 数字对。

---

## 5. 「还缺什么」 — completeness critic 的收束回答

**(a) 哪个总体没被求过**

1. **「本文件负责什么」这个总体, 在 R3-fix 加了 TASK-028 之后没有被重求一遍。** 四处范围分区 (yaml `scope_boundary` ×2 + tasks.md 范围边界表 + 交接段) 全部停在 R2-fix 的委派语义上 → **C1**。这是本轮唯一一条能重演历史事故的漏项。
2. **「旧版本号在 append-only 账本里应有的命中数」这个总体没被求过** —— 求的是当前版本的命中数 (2), 拿它当旧版本的下界 → **C2 恒红**。正确的求法是拿一个**已经降级过的**版本 (1.65.2/1.65.1 = 1) 做样本, 而不是拿当前版本。
3. **「引用该 sc-baseline 脚本的全部非审计史文件」没被求过** (只读了 proposal.md) → **M7**。一条 `git grep` 就能求出。
4. **「两条 enabled check 的失明点集」没被完整求过** —— 只减了 README 家族 → **M6 (10 而非 7)**。
5. **「aria/VERSION 里有几处当前版本声明」没被求过** —— `## 版本号` 块的 1.47.0 被当成历史 → **M10**。
6. **「enabled check 全集」没被枚举过**就断言「无任何 custom check 兜」→ **m3** (实为 8 条, 含一条查 CLAUDE.md 版本字段的)。
7. **「宿主文件里既有 test 方法的全集」没被求过** —— 34 个, 而「6」的指称对象随行号锚一起被删掉了 → **M3**。

**(b) 哪个声明没被独立验证过**

- `superseded_by` 两条 (**M4**) 与 DAG 三条派生值 (**M1/M2**) —— 它们的共同点是: 那条自证命令 (`:918`) 只覆盖 complexity/工时/agent，**恰好把出错的三条都留在覆盖外**。而该处的订正史自陈「警告没拦住, 拦住的是机械核验」—— 这个教训对未被机械核验覆盖的声明**一次都没生效**。这是 memory `feedback_mechanization_knob_must_match_granularity` 的干净复现: 开关作用域 < 情形集。
- `tasks.md:180` 引用 5.8 (**M8**) —— 编号清扫的完成度没被机械核验 (一条 `grep -nE "5\.[2-8]"` 即可)。

**(c) 哪个会变的东西没进枚举**

- **未来新增的版本引用点**: 两个白名单是正向枚举, 无「其余阻断」分支, 对新文件 fail-OPEN → **M9**。这是本 Spec 修实例而未修类的地方 (`feedback_fix_the_class_not_the_instance`)。
- **`scope_repos[].head`**: 每个 commit 都会变, 手写维持结构上必漂 → **m4** (已第二次)。
- **任务集**: R3-fix 增删任务时, DAG/scope_boundary/superseded_by 三处派生枚举无一自动跟随 → C1/M1/M4 三条同根。
- **`aria/VERSION` 的降级形态**: 实测 1.65.4/1.65.3 的发布注**根本没被降级保留** (命中 0) ⇒「历史行原样保留」这个前提在近两轮发布里就不成立。TASK-022 的编辑程序与实际历史行为的偏差没被求过, 而 TASK-024 的 (b) 建立在这个前提上。

---

## Verdict

**2 critical + 10 major + 5 minor ⇒ vote: REVISE / verdict: FAIL**

收敛判断建议 (供编排层): 本轮 2 条 critical **都是 R3-fix 自身引入的** (C1 = R3-fix 加 TASK-028 未扫分区枚举; C2 = R3-fix 新写的 invariant (b))。这与 R2→R3 的形状一致 (「两条 Critical 都是 R2-fix 造的」, 见 HEAD commit message)。按 memory `feedback_audit_marginal_return_goes_negative` 的判据 (**本轮 fix 引入的占比 > 1/2 即拐点**), 若 R4-fix 后再开 R5, 应预期同样的再生产率。建议 R4-fix **只做机械收口**, 不做叙述性补丁:
1. C1: 删/改四处范围分区文字, 使之与 5.13/5.15 的切法一致 (含删掉 `SKILL.md:242` 误引)。
2. C2: (b) 改为「`发布日期(旧)` 族里对旧版本的命中 ≥1」并显式排除头部当前版本行。
3. M1/M2: 把 DAG 的节点集/并行组/关键路径三条**并入那条自证命令**, 或直接删掉这三行文字 (它们无消费者, 而错的成本已实证两次)。
4. M9: TASK-024 加一行整仓 grep 差集断言 —— 这一条同时把 M6 变成不必算的数。
5. M3: 把「6 个」换成两个 class 名。
6. M4/M8: 两处编号指错, 逐字改。
7. M5/M7/M10/m1/m2/m4: 各一行。

⚠️ 上述 4 与 9 是**唯一两条把「类」而非「实例」修掉的**建议; 其余是实例级。若只能改一处, 改 M9。
