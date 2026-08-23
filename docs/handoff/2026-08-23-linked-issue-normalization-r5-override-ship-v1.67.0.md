---
track-id: linked-issue-normalization
owner-container: simonfish/bfe8285d
phase: D-done
status: done
updated-at: 2026-08-23T10:40:00Z
---

# Cycle Handoff (2026-08-23) — linked-issue-normalization: R5 不收敛 → owner override → Phase B/C/D 全程, ship aria-plugin v1.67.0 (track 终结)

> **一句话**: `/state-scanner` [1] → owner 裁 R5 加轮 → R5 两席新鲜眼睛 FAIL (2C+7M, **0 条新发现**, 4 条由我的「机械收口」引入) → owner 裁修九条后 override 进 B → TDD (19 个 SC 测试基线 RED/GREEN 分布与 Spec 表一致) → 实现 `normalize_linked_issue` + 谓词切换 → Rule #6 AB 真跑 (12 eval × 2 臂 + iteration-2; 定向 eval-12 新版 5/5 vs 基线 3/5; AB 抓到括注缺空白细则, 改了交付物) → 合入并发轨 v1.66.5 → 三项 owner 裁量 (v1.67.0 MINOR / TASK-025 (b) / TASK-027 披露) → TASK-024 三态断言 (执行中抓出 spec 两处判据缺陷并回填) → aria `ca52d1c` 双推 + tag → PR #189 审计 (code-reviewer: 0 Critical / 1 Important / 3 Minor, 可 merge) → Forgejo merge `c453504` → 归档 + claim 释放。**track 终结。**
>
> ⭐ **这段最该留下的**: 第五轮审计证明了「修审计发现」本身是缺陷发生器 —— 连最小编辑 (改版本号、补 deliverables、刷 head) 都各造 1 条 C/M。真正压住缺陷的是**执行**: TASK-024 在基线上亲跑三态, 当场抓出「`git show HEAD:aria/...` 对 gitlink 必崩」和「排除集缺行级类」两条 R1–R5 十七席没抓到的东西。**判据写进 spec 前在基线亲跑一遍, 比加审计轮便宜一个数量级。**

## §0 入口 (新 session 优先读)

- **本轨终结**: spec 已归档 `openspec/archive/2026-08-23-linked-issue-normalization/`; claim `linked-issue-normalization` 已 release (push_success=true); **无本轨后续**。
- **版本**: aria-plugin **v1.67.0** @ aria `ca52d1c` (origin == github == tag); 主仓 master `c453504` (origin == github); 主仓 gitlink → `ca52d1c`。本机插件缓存已刷到 1.67.0 (owner 本 session 跑了 `/plugin marketplace update` + `/plugin`)。
- **并发轨 (023236f2)**: 09:14Z 认领 `a1-entry-claim-duplicate-work-guard` (rework) + `issue-batch-149-151-155-134-state-scanner`; 均未推分支。他们下次 fetch 会看到 aria master 已到 v1.67.0 (collision.py / claim_schema.py / test_release_by_track.py 有改动; 其 #134 改 test_collision.py, 不重叠)。
- **待排期 (Level 1, 见 §2)**: code-reviewer Important — `test_release_by_track.py` 两个新 class 写在 `unittest.main()` 之后。

## §1 已完成 (按时间顺序)

1. 状态扫描 → 识别本容器 bfe8285d, #152 由 023236f2 在做; 选 `linked-issue-normalization`。实况比 handoff 写的靠后: A.3 已做, post_planning R1-R4 全 FAIL 停 14 天。
2. owner 裁 **R5 加轮** → 我先做机械收口 (`09eb919`: v1.66.0→v1.67.0 / #137 已修 C3 解除 / R4 M3·M5·M7·5.8 / head 刷新) → R5 两席 (executability / claim-landing) **FAIL 2C+7M**, 4 条由收口引入 (旧值字面没跟新值改 ⇒ 差集断言恒真 / 补 deliverables 造同文件并行边 / 刷 head 不刷行号锚 / 状态头三改二)。聚合报告 `post_planning-R5-1787435452341-*`。
3. owner 裁 **修九条后 override 进 B** (`826b356`, Rule #10 留痕审计轨 §9/§10) → B.1 claim passed + 两仓分支。
4. **B.2**: 16+3 个 SC 测试 (基线 RED: 1/1b/3/4/5b/11/13/15; GREEN 护栏: 2/5/5c/6/6b/9/10/14) → `normalize_linked_issue` + `_linked_issue_matches` (`8f5f5bd`) → 文档同步 (`0fe2e0d`) → run_all 7 OK / 0 FAIL。
5. **Rule #6 AB** (TASK-013): state-scanner 全套件 11 条 + 新建定向 eval-12, 24 臂; 既有零回归; eval-12 新版 4/5 vs 基线 2/5; 承重断言 1 两臂皆 hedge ⇒ 括注补「大小写/首尾空白/`./_`」细则 (`880060d`) ⇒ iteration-2 5/5 vs 3/5。结果 `ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`; eval-12 入 ab-suite v1.6.0; 套件缺口 **aria-plugin#157**。
6. 并发轨 ship **v1.66.5** 被多臂旁证 → 两仓 merge origin/master (aria `394cffd`, 主仓 ff `1205ec3`), 基线改 1.66.5, 测试 1641 OK。
7. owner 三裁: **v1.67.0 MINOR** / **TASK-025 (b)** (脚本退役 + 冻结报告 `.aria/repro/archive/sc-baseline-*-REPORT.md`, 基线 16/16) / **TASK-027 单 Skill 披露** (决策 `.aria/decisions/2026-08-23-rule6-ab-scope-single-skill-disclosure.md`, convention **aria-standards#17**)。
8. **TG-5**: aria 5 文件 bump (`3ff8cb2`) → 主仓 14 点 (`01dab46`) → TASK-024 三态 (基线 14 红 / 目标 0 / 漏 1 点红; 新值 18; 账本 +1 行) —— 执行抓出 spec 两缺陷并回填 (子模块旧值取法 / 排除类 (2) 补 4 目录 + 行级类 (5)), 脚本 `.aria/repro/vdiff.sh`。
9. **C**: owner 授权 (核实双子星无冲突后) → aria master 本地 `--no-ff` 合并 `ca52d1c` + 双推 + tag v1.67.0 逐远端核验 → gitlink `4591d32` → PR #189 → pre-merge gate green (path not_applicable, main clear) → owner 指出主仓 merge 在我授权内 → **PR 审计** (aria:code-reviewer 两阶段: 规范合规 PASS, 53/53 tests, 22 版本点对齐; 0 Critical / 1 Important / 3 Minor, 可 merge) → Forgejo merge `c453504` → 本地 ff + github 镜像推 + ls-remote 一致。
10. **D**: 归档门 verdict=pass (21/21, 无 d_payload) → 归档 (CLI 位置 bug 修正) → claim release + sweep/gc → 本 handoff。

## §2 未完成 / Carry-forward 清单 (AI 内省, load-bearing)

- ✅ **Level 1 hotfix 已修 (2026-08-23 当日, 未发版)**: `aria/skills/state-scanner/tests/test_release_by_track.py` 两个新 class 已移到 `if __name__ == "__main__"` 守卫之前 (aria master `e1be8f3`, 双端已推)。两条调用路径实测均 `Ran 53 OK`; `run_all_tests.sh` 7 OK / 0 FAIL (1693 tests)。**未 bump 版本、未 bump 主仓 gitlink** —— 随下一次 aria PATCH 的发版同步面自动带出。
  > ⚠️ **给下一个发版者**: aria `master` (`e1be8f3`) 比主仓 gitlink (`58a49e7` = v1.67.1) 领先 1 个纯测试布局 commit。下次 bump gitlink 时会连带发出, CHANGELOG 请顺手提一句 (本条 commit message 已自述)。
  > 📌 时序: 本 hotfix 原计划「并入下一 PATCH」, 但并发轨 023236f2 在本 session 尾声先 ship 了 **v1.67.1** (state-scanner 四缺陷批 #134/#149/#151/#155, gitlink `ca52d1c→58a49e7`), 其改动面未碰本文件 ⇒ 错过那班车, 故当日直接落 master 等下一班。
- 🟡 code-reviewer Minor: CHANGELOG 1.67.0 条目「Aria#177 相关」措辞易误读 (应为「版本面校验类级根因见 #177」); `vdiff.sh` 硬编码仓路径; `.git` 后缀仓名译码为 `repo-git` (规则 3 推论, 非 bug)。随上条一起。
- 🟡 **aria-plugin#157 / aria-standards#17** 新立案待 owner 排期 (套件 Layer L 段零覆盖 / AB lane convention)。
- 🟡 **aria-plugin#137 在 Forgejo 仍 open** 但 v1.66.0 已修 (分支存在性 fail-CLOSED); #136 仍 open (phase-c-integrator 无 gate-only 形态, 本轨按硬约束 1 手工本地合并绕过)。建议关 #137。
- 🟡 上 session carry 未动: #182 (handoff status 收口) / #184 (brainstorm 被绕过) / #179 周期 handoff §2 三项 owner 复议 / Aether#283 两项凭据未核。`a1-entry-claim` rework 已被 023236f2 接走。
- ⏸️ M6/M7 六门控 spec 不变。

### owner 复议闭环 (2026-08-23, #179 周期 handoff §2 三项 + #137)

- ✅ **aria-plugin#137 关闭**: v1.66.0 (`8683551` release / `61b4d76` 散文) 已修 —— `_verify_main_branch_exists()` 对不存在分支 fail-CLOSED, 原「main 无 in-flight 恒真」解除 (缺省值仍 `main`, 但不再静默绿)。评论留证后 close。
- ✅ **Amendment-1/2 范围修正 + 行为变化知悉**: owner 确认, **维持 v1.66.4 现状不返工** (白名单两族 + 适用集枚举 14 行 + `/`-根名不套白名单; `cat x.profile` 从拦变放属设计本意)。
- ✅ **review 三条残余弱点挂 aria-plugin#138 评论** (不新开): `| tee /dev/stderr | jq keys` 旁路 · jq 错误信息回显输入值 · `node -p` 未覆盖。三条均未修, 记已知限, 随 #138 排期。
- ⚠️ **SC-8 空载复测 (owner 裁「复测一次再结」) — PASS, 但请知悉判据方差**:

  2026-08-23 22:35 UTC 单跑 (不并发), 起跑 `loadavg=2.97`, 测量期 `4.78`, bash 5.2.15, N=10 calls/round × 20 rounds, 进程内 EPOCHREALTIME 只计判定段:

  | tier | old_min | new_min | 增幅(min) |
  |---|---|---|---|
  | (a) 单条 benign | 381855µs | 96731µs | **-74.7%** |
  | (b) 2 段全 benign | 340311µs | 149420µs | **-56.1%** |
  | (c) 2 段全命中 | 374809µs | 103994µs | **-72.3%** |
  | (d) 3 段全命中 | 364443µs | 129977µs | **-64.3%** |
  | **(e) 最坏档 (末位 pattern + 每段 filter)** | 374291µs | 551060µs | **+47.2%** |

  全量 599/599 PASS (FAIL 0)。**tier (e) 过闸 (≤50%) 但仅余 2.8pp。**

  **⚠️ 待 owner 知悉的真问题不是这一次的值, 是判据本身的方差**: tier (e) 六次实测 = `+58%` (load≈12, FAIL) / `+6.8%` (PASS) / `+83%` (load 15-22, FAIL) / `+0.8%` (PASS) / `+9.2%` (PASS) / **`+47.2%` (本次, 最低负载, PASS)** —— 跨度 0.8%–83%, 且**本次是六次里负载最低的一跑, 增幅却排第三高**。换句话说「高负载导致超标」这个解释被本次数据削弱: min-of-20-rounds 去噪后仍有约 ±40pp 抖动, 闸门通过与否在这台 4 核共享机上接近抛硬币。按 Rule #10 不自判「噪声」也不改阈值/口径/档位, 原样呈报。**若 owner 认为该判据需要加固, 可选方向**: 提高 rounds (20→100) 或 N / 改用 taskset 绑核 / 把 (e) 档从闸门降为 advisory 观测项 —— 三者都属改 enabled 闸门配置, 须 owner 裁。
  - 附带发现 (minor, 未修): 脚本 `:1863` 的自述行仍写 `median-of-rounds`, 而 2026-08-16 判据已改 min (`increase(min)` 才是主判据, median 只作审计参考) —— 文案陈旧, 建议随下次 secret-guard 改动顺手改。

**机械补漏**: 本轨 21/21 done, 归档门无 d_payload; consistency flags 全 `active_change_not_in_upm` (恒亮)。

## §3 关键风险 / 已知陷阱

- **scan.py 在 feature 分支恒 exit 10** (#176 形状, AC-5 对 github 无 feature 分支): 24 个 AB 臂全报这一条, 两臂同受影响不构成 delta, 但每次都要人工判「parity=true 未验证」。
- **`git show HEAD:aria/...` 对 gitlink 取不到文件** ⇒ 任何「取子模块旧值」判据必须 `git -C aria show "$(git rev-parse HEAD:aria)":<path>`。
- **版本差集按路径类排除不够**: 上一版 ship 留下的「`vX.Y.Z+` 功能引入标注」(SKILL.md / pre_merge_gate.py / config.template / fixture 共 19 处) 只能按行内形态排除, 否则恒红。
- **harness 后台 `git status` 造 index.lock** 本 session 撞 1 次, 在 `git stash` 中途 —— stash 创建成功但 reset 失败, 留下与工作树重复的 stash; 处置 = diff 比对后 drop, 不要 pop。
- **aggregate_benchmark.py**: run 目录必须 `run-N/` 子层; grading.json 须含 `summary` 块 (grader 按 grader.md 只写 expectations, 要自己补); Summary 的 Delta 符号按 Old−With 打印。
- **自写 AB 定向 fixture 时**: 承重断言要求「明确答 X」, 而 skill 文本若没钉住边界条件 (这次是空白), 好模型会诚实 hedge 而被判败 —— 这是断言在替规范找漏洞, 不是断言写错。

## §4 实战教训 (memory 沉淀来源)

```
[已写 memory 本 session]
- (无新增文件; 下列候选待写)
[候选 memory]
- feedback_check_runs_at_baseline_before_spec (对方容器已写 feedback_new_mechanical_check_must_run_at_baseline_first): 本 session 第二次独立实证 —— R1-R5 十七席漏的两条判据缺陷, 执行时 5 分钟抓出。若该文件已存在, 追记本例。
- feedback_mechanical_cleanup_is_also_a_defect_generator: 「机械收口」四条 C/M 的形状: 改新值漏旧值 / 补 deliverables 不复算并行边 / 刷 head 不刷行号锚 / N 处改 N-1。每次改「同一事实的多个落点」必须 grep 全量落点 + 程序化复算派生值 (已有 feedback_scoped_git_add_splits_claim_from_landing 覆盖一半, 可追记)。
- feedback_ab_targeted_fixture_hedge_means_spec_gap: 定向 AB 承重断言两臂皆 hedge ⇒ 不是模型差, 是 skill 文本缺边界条件; 修文本重跑, 而非放宽断言。
- feedback_gitlink_old_value_via_submodule_show: 取子模块文件旧值须经 gitlink SHA 在子模块里 show (上方 §3 第 2 条), 一行命令级陷阱。
```

## §5 多维度同步状态

| 维 | 状态 |
|---|---|
| UPM | 无 (Aria 不配置) |
| OpenSpec | 活跃 7 (门控 6 + a1-entry, 后者已被 023236f2 认领); 本轨已归档; pending_archive 0 |
| User Story | 21 (done 17), 本轨无 US 变动 |
| 版本 | aria-plugin 1.67.0 (SOT = 22 引用点 + 账本 + gitlink 全对齐, TASK-024 断言 PASS); 主项目 1.7.3 (CLAUDE.md 仍写 1.7.3 vs root VERSION 头 1.7.5 — AB 臂旁证的 pre-existing 漂移, 未动) |

## §6 Next session 入口 + 优先级建议

`/aria:state-scanner`。本轨终结, **本 session 的 carry 已全部落地或转交**:

- ~~(1) Level 1 hotfix~~ ✅ 已修 (aria master `e1be8f3`, 未发版, 见 §2 首条)
- ~~(2) 关 aria-plugin#137~~ ✅ 已关 (2026-08-23, 留 v1.66.0 修复证据)
- ~~(3) #179 三项复议~~ ✅ 已结 (见 §2 owner 复议闭环)
- **余待 owner 定方向**: (a) **SC-8 判据方差** — 六次跨度 0.8%–83%, 空载这次 +47.2% 距闸仅 2.8pp, 三个加固方向见 §2 末条; (b) 主项目版本 `1.7.3` vs root `VERSION` 头 `1.7.5` 漂移 (Level 1 doc); (c) #182 (handoff status 收口) / #184 (brainstorm 被绕过) 未动。
- **并发轨 (023236f2)**: 本 session 尾声 ship **v1.67.1** (state-scanner 四缺陷批 #134/#149/#151/#155) + a1-entry rework 走到 post_spec R2 未收敛 → owner 裁 (iii) 撤/方向 b 缩 scope。起任何 state-scanner 改动前先 fetch 三面 + 读其 [2026-08-23 会话收尾](./2026-08-23-session-close-v1.67.1-batch-and-a1-entry-r2-direction-b.md)。并发轨 023236f2 在做 a1-entry + state-scanner issue batch, 起任何 state-scanner 改动前先 fetch 三面 + 读其 handoff。

## §7 提交清单 (commit hash + multi-remote parity)

```
[main master]   c453504 (PR #189 merge) | origin == github (ls-remote 逐个核验)
  路径: 09eb919 (R5 前收口) → 914a4c7 (R5 报告) → 826b356 (R5-fix + override) → a6cdeef (B 组1-4 + AB)
        → 71a3149 (5.12/5.14) → 01dab46 (主仓版本面) → 4591d32 (gitlink) → 3c1910b (TASK-026) → c453504
[aria master]   ca52d1c (merge --no-ff feature) = tag v1.67.0 | origin == github
  路径: 9e6a17c (v1.66.4) → 8f5f5bd (feat) → 0fe2e0d (docs) → 394cffd (merge v1.66.5) → 880060d (括注 v2) → 3ff8cb2 (release) → ca52d1c
[standards]     334c609 (未动) | [aria-orchestrator] 237045a (未动)
[coord ref]     claims/bfe8285d/s-e9f8@0541 → done (release_gate, push_success=true)
[config]        .aria/config.json audit.max_rounds 4→5 (owner 裁定, 随 09eb919 入库)
本 handoff + 归档 commit: 见 git log (master, 双推)
```

## §8 Memory entries this session

- 新增: 0 (候选 4 条见 §4, 留给 session-closer 或下 session 裁量)

## Cross-references

- Spec (已归档): `openspec/archive/2026-08-23-linked-issue-normalization/` · 审计轨 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` §9/§10 · R5 报告 `post_planning-R5-1787435452341-*`
- AB: `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/{PREDICTION,RESULT}.md`
- 决策: `.aria/decisions/2026-08-23-rule6-ab-scope-single-skill-disclosure.md`
- Issues: aria-plugin#157 · aria-standards#17 · Aria#177 · aria-plugin#136/#137 · PR #189
- 并发轨: [2026-08-23 #152 Phase B→D](./2026-08-23-issue152-phase-b-through-d-ship-v1.66.5.md) · 前序本容器 [2026-08-22 session close](./2026-08-22-session-close-179-full-cycle-and-147-supersession.md)
