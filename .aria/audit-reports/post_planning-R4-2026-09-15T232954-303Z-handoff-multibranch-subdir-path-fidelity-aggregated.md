---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T00:40:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/8M/20m
counts_dedup: 0C/7M/16m
sibling_probe: no_sibling_found
---

# post_planning R4 聚合 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195, A.2/A.3 v4 `edd256d`)

> **对象**: tasks.md (27 checkbox) + detailed-tasks.yaml (35 TASK) + sc11-predicate-validation.py (18 态 x 19 谓词), 主仓 master `edd256d` (本地, 未推送)。
> **Sibling probe (本轮入口)**: 已完整扫描, 未发现同 issue 竞品 (`status=ok`, origin 161 / github 155, 无 cap)。
> **drift-checker**: convergence 未 opt-in ⇒ 跳过。
> **审计前后状态**: 三仓 HEAD 与 `refs/aria/coordination` 未变; 报告数 869 → 874, 恰为本轮 5 份; 各席临时目录已清。
> **派发**: 默认并发 2, 滑动窗口 (tech-lead + code-reviewer → qa-engineer → backend-architect → knowledge-manager)。

## 判定

| 席 | verdict | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/5M/8m | REVISE | 取号恢复路径死锁; 两仓合并结局不一致无处置; 第 7 步新核验必然 rc=3 且零信息; TASK-031「两远端一致」恒假; 主仓推送无失败分支、半推后仍可 bump gitlink |
| code-reviewer | PASS_WITH_WARNINGS | 0C/1M/8m | REVISE | (j1)(j2)(j3) 只堵住「另起一段」, 没堵住「同段 / 同行在元组后补一句」, 三处元组仍可留四元而 19 条全 PASS |
| qa-engineer | PASS_WITH_WARNINGS | 0C/2M/2m | REVISE | 自建对抗构造独立复现同一族缺陷; (l1) 的 Scenarios 判据同形 |
| backend-architect | PASS (frontmatter 写 PASS_WITH_WARNINGS, 与 0M 不符, 以 counts 为准) | 0C/0M/1m | PASS | 组 2 行号零漂移; TASK-035 六补丁与 TASK-029 / 034 的 git 编排经真实仓实验证实与文字相符 |
| knowledge-manager | PASS (同上) | 0C/0M/1m | PASS | R3 的 9 簇逐条落地; 仅台账行括注三处未统一 |

**合并判定: PASS_WITH_WARNINGS (0 Critical / 7 Major 簇) · Vote REVISE 3 / PASS 2 · 未收敛 (R4)。**

## 收敛计算

- **结论集**: R4 的 7 簇与 R3 的 9 簇无一 (category, scope) 相同 ⇒ `conclusions_stable = false`; 非全票 PASS ⇒ `converged = false`。
- **振荡**: R4 ≠ R2 ⇒ 无振荡。
- **Major 趋势**: 13 → 9 → 9 → **7**, 本轮首次出现两张 PASS 票 (R1 之后第一次)。
- **v4 引入占比**: 完全引入 3 簇 (M1 / M2 / M3), 部分 3 簇 (M4 / M5 / M6), 此前已有 1 簇 (M7) ⇒ 3/7 完全引入, 低于前两轮 (5/9、7/9)。
- **分布**: 7 簇中 5 簇 (M1–M5) 落在组 5 发布段约 200 行文本内; 2 簇 (M6 / M7) 落在 SC-11 谓词族。**组 1–4 的 24 个任务 (约 70h) 本轮零 Major** —— backend-architect 席对组 2 行号与 TASK-035 六补丁做了真实仓实验, knowledge-manager 席对交叉引用做了字节级核对, 两席均投 PASS。

## 五席的边际判断 (本轮新增章节, 供 owner 判断是否继续加轮)

| 席 | 结论 | 依据要点 |
|---|---|---|
| tech-lead | **已越过拐点** | 5 个 Major 全在同一片 200 行发布段且 4 个是最近两轮新加机制自己长出来的; 修法合计约 6 句「删或改一句」; 建议不再加轮, 并考虑把发布段降级为「按 phase-c-integrator 执行 + 本 Spec 特有约束」 |
| code-reviewer | **已越过** | 342 个格子里真正承载信息的只有「7 条谓词 x 各自 1-3 个坏态」, 每加一态要手推 19 格; 建议 EXPECTED 改为「每态只声明期望 FAIL 的谓词集」, 加态成本从 19 格降到 1 行 |
| qa-engineer | **部分越过** | 三步法对约 20 条 SC 不分难度均匀套用、SC-11 连续 4 轮打补丁式加固已属过度广度; 但对判据自身抗攻击的结构性检查深度仍不足 —— 该收的是轮数与对简单 SC 的重仪式, 不该收的是判据逻辑的攻击面 |
| backend-architect | **组 1–4 已足够** | 实现任务可无歧义落地, 未发现过度限制合理实现之处; TASK-029 第 4 步「指针而非流程」的裁量空间是 R4 原则的合理产物, 不建议展开 |
| knowledge-manager | **体量失衡, 但大头不可剪** | 规划三文件与被改模块代码量相当, 审计报告已是规划文档的 5 倍; 失衡大头是防骗验收机制 (问题复杂度本身, 不可剪) 与逐轮累积的追溯性论证 (可移入归档台账) |

**主控读法**: 五席一致认为轮数该收; 分歧只在「哪些该收」。共识部分 —— 组 1–4 已可执行、发布段与谓词族是剩余缺陷的全部所在、两者的修法都以「删 / 换结构」为主。

## Major 簇 (去重后 7) 与处置 (R5 rework)

### PP4-M1 — TASK-029 取号恢复路径死锁

- **席位**: TL M1 · **v4 引入**: 是
- **证据**: 第 4 / 6 步的基准写死为「TASK-027 记录的取号时 SHA / 取号值」, 而第 4 步唯一的恢复动作 (按 `ec72175` 重算号) 恰好改变这两者, 恢复后从第 1 步重走必然在同一处再停; 第 6 步也必因「取重算号 ≠ TASK-027 取号值」判不符。根因是 v3.1 → v4 的组合: R3 要求删掉「回 TASK-027 重跑取号」的路由, v4 删了路由却把基准硬化成冻结值 (memory `fixes-contradict`)。
- **处置 (接受, 不新增分支)**: 第 4 / 6 步的基准改为「台账中**最近一次**记录的取号时 SHA / 取号值」; 第 4 步恢复指针末尾补「重算号后按 TASK-027 的记录格式在台账追加新的取号时 SHA 与取号值, 重走时以该新记录为准」; 「三支一律从第 1 步重走」补进 AI 流程判断清单第 22 条。

### PP4-M2 — 两个子模块合并结局不一致时无处置; 本地 master 领先时静默放行

- **席位**: TL M2 · **v4 引入**: 是
- **证据**: 第 5 步「aria 与 standards 各自」合并, 冲突分支只写单仓 `merge --abort`; aria 合成功而 standards 冲突时 aria 的合并提交留在 master 上无人处理。实测 `git merge --ff-only origin/master` 在本地 master 领先时返回 `Already up to date.` exit=0 (第 3 步之后未复核相等); 再走第 5 步 `--no-ff` 得 `Already up to date.` 不产生合并提交 ⇒ 第 6/7/8 步全落在没有本轮合并提交的树上。standards 侧有并发轨 (`10CG/aria-standards#20` 跟踪同一文件), 这一支不是假想。
- **处置 (接受, 删分支而非加分支)**: 第 5 步改为「两个子模块视为一个整体: 任一仓退出码非 0 ⇒ 对两个仓都执行第 6 步回退条 (前置成立的执行回退, 不成立的执行 `merge --abort`), 两仓 HEAD 都回到第 3 步记下的 SHA 后停下上报」; 第 3 步在 `merge --ff-only` 之后补「再次断言 `rev-parse master` 等于 `rev-parse origin/master`, 不等即停下上报 (本地领先说明有未推送的遗留合并)」; 第 1 条 bullet 的论证句同步。

### PP4-M3 — 第 7 步的 `--emit-json` 核验在其执行时点必然 rc=3, 且健康常态下恒 PASS

- **席位**: TL M3 · **v4 引入**: 是 (源自主控在 R3 采纳的 m11 处置)
- **证据**: 该脚本全部模拟改动锚定 1cb3872 原文, `rep()` 的 count=1 锚点在实现落地后必然消失 ⇒ 抛 `AnchorDrift`, rc=3, 不打印 JSON (TL 实跑: 只施加一处真实 target 编辑即触发)。另一半: 脚本与 yaml 同在主仓 change 目录, 自 TASK-001 起无人改动 ⇒ 比对结果恒等于 TASK-001 的结果。
- **处置 (接受, 删)**: 删去 TASK-029 第 7 步的这一句; 两份谓词原文的一致性由 TASK-001 一次性核验承担。**主控自查**: R3 m11 要求「TASK-001 与 TASK-029 第 7 步各加」是主控未核验执行时点的处方, 本轮按 R4 原则 3 撤回。

### PP4-M4 — TASK-031「主仓 master 在 origin 与 github 的 ls-remote SHA 一致」在计划动作集下恒假

- **席位**: TL M4 · **v4 引入**: 部分 (断言沿自 v1, v4 把合并方式钉成服务端 merge 后成为确定矛盾)
- **证据**: 计划里没有任何一步把主仓 master 推 github; PR 以 Forgejo 服务端 merge commit 合并 (只发生在 origin), 主仓到 github 的唯一通道是本地推送, 而计划里主仓第一次 github 推送要到 TASK-032 的 Phase D。
- **处置 (接受, 采结构性改法 —— 交给已有 Skill 而非在计划里重写)**:
  1. **主控已核实 `phase-c-integrator` C.2.5 的覆盖面** (SKILL.md「C.2.5 Multi-Remote Push Enforcement」): PR 合并成功后触发, per-remote 矩阵门控 (先子模块后主仓), 推后 `verify_parity_post_push`, `fail_on_partial_push` 默认 true ⇒ 阻断并输出修复命令; `.aria/config.json` 未覆盖该键 ⇒ 默认 enabled, `enforced_remotes` 为空 ⇒ 自动发现 origin 与 github。**未覆盖**: 子模块分支的本地合并、tag 推送 —— 这两项仍由本计划承担。
  2. TASK-031 写明: PR 合并后由 phase-c-integrator C.2.5 把主仓 master 推到全部 enforced remote 并做 post-push parity 验证; 执行时先核对「C.2.5 enabled 且 enforced remote 含 origin 与 github」这一配置事实, 输出记台账; 断言改为「C.2.5 对两个 remote 均 match=true」。
  3. `metadata.owner_gates` 第 11 项性质补「含合并后经 C.2.5 的多远程推送」。

### PP4-M5 — 外向推送的失败分支只覆盖子模块侧; 半推后仍可 bump gitlink

- **席位**: TL M5 · **v4 引入**: 部分
- **证据**: owner_gates 其余 5 条外向条目都带「不进下游任务」, 唯独 TASK-034 两条没有; TASK-030 只写「gitlink 取 TASK-034 推送核验后的 master SHA」—— 「origin 成功、github 被拒」时这句照样可执行, 后果正是 CLAUDE.md 硬约束 1 与 memory `mirror_sync_needs_mechanical_backstop` 要防的孤立 gitlink。TASK-031 / TASK-032 的主仓推送也没有被拒 / 半推分支。
- **处置 (接受, 三处各一句)**:
  1. owner_gates 的两条 TASK-034 条目各补「不进 TASK-030」。
  2. TASK-030 第一条核验补前置「TASK-034 对 origin 与 github **双方**均已 ls-remote 核验一致; 任一方未一致不得 bump gitlink」。
  3. TASK-031 与 TASK-032 的推送条各补「被拒或只推成一个远端 ⇒ 不 force、不改写历史, 原样记台账并停下上报 (同 TASK-034)」, owner_gates 第 11 / 15 项同步。主仓侧的多远程推送本身走 C.2.5 (见 PP4-M4), 本条只补人工路径的口径。

### PP4-M6 — (j1)(j2)(j3) 仍可被「同段 / 同注释块 / 同一行在元组后补一句」骗过

- **席位**: CR M1 · QA M1 (两席**各自独立**构造坏态, 结论一致) · **v4 引入**: 部分 (第三轮在同一族谓词上打补丁)
- **证据**: v4 的实现是「取块 → 找 `(parse_ok` → 要求其后出现 `rel_path`」, 而「其后」是该块 / 该行的全部剩余文本。CR 的 ADV-1/2/3 与 QA 的 A/B/C 三态实跑: 三处元组保持四元、只在其后补一句说明, 19 条全 PASS。与 memory `redfix-change-quantity` 同形 —— 两轮都在同一个量 (「块内是否出现 rel_path」) 上挪边界, 没有换量。
- **处置 (接受, 换量)**:
  1. 采 code-reviewer 席已在 10 个状态上实跑、零回归的写法: 只看 `(parse_ok` 起的那一对**平衡括号之内**是否含 `rel_path` (核心片段见其报告 M1); (j3) 保留「`# Tie-break` 恰一行且在 `def _dedupe_sort_key(` 之前」的 fail-closed 前置, (j2) 保留「非表格行且同时含 `compound key` 与 `(parse_ok`」的取行与 `all()`。
  2. 新增三个坏态 `bad_j1_same_para` / `bad_j3_same_block` / `bad_j2_same_line` (期望分别仅对应谓词 FAIL)。
  3. authoring_rules 在「元组写全五元并留在首段」后补「第 5 元写在元组括号之内, 写在元组之后的说明句不算」。
  4. 对「元组跨两行书写」这一合法写法不得假红 (CR 已实测)。

### PP4-M7 — (l1) 的块截取包含标题行余部; Scenarios 条件可被标题行括注满足

- **席位**: QA M2 · CR m1 · **v4 引入**: 否 (v3 已有, v4 未修)
- **证据**: `blk = s.partition(h)[2].split(chr(10)*2)[0]` 从标题串之后开始截 ⇒ `Return dict schema: (另含 degraded_reason)` 这类标题行括注落在块内; 三种写法 (ADV-4/5/6) 下 (l1) 仍为真, 而字典字面量 / 键清单 / 第四种结局都没真改。
- **处置 (接受, 字符级小改 + 结构化)**:
  1. 块截取改为丢掉标题行余部 (`s.partition(h)[2].partition(chr(10))[2]`)。
  2. Scenarios 段的判据改为结构性: 要求该段的结局行数比基线多一行且新增行含 `target_in_subdir` (或等价的、可机械判定的结构量), 而不是「段内出现某子串」。
  3. 相应新增坏态 (标题行括注型), 期望仅 (l1) FAIL。

## Minor (去重后 16) 与处置

| 编号 | 内容 | 席位 | 处置 |
|---|---|---|---|
| m1 | owner_gates 只枚举第 4/5/6 步为 fail-closed 上报点, 第 2/3/7/8 步与 TASK-034 同名 tag 支、TASK-032 ff-only 支同样会停摆却未列 | TL m1 · CR m4 · BA m1 | 接受: owner_gates 顶部注明「仅列需 owner 动作的点, 纯止损停摆见各任务」, 并补这四处; TASK-029 第 2 步补「本地提交后重新执行第 2 步断言, 通过后进入第 3 步」 |
| m2 | owner_gates 第 1 项含 B.0 认领推送, TASK-001 verification 无对应条目; 未授权时无抑制手段 | TL m2 | 接受: TASK-001 补一条, 写明未获授权时以 `ARIA_COORDINATION_NO_PUSH=1` 或 `--no-push` 跑 B.0 |
| m3 | tasks.md「其中三处须特别留意」未纳入 v4 新增的两处 fail-closed 停下点 | TL m3 | 接受 |
| m4 | `touchpoints-aria.txt` 与 AB 两臂 worktree 的落盘位置未定, 会与 TASK-031 的有范围核验冲突 | TL m4 | 接受: 明写落 scratchpad |
| m5 | TASK-026 扩面拆任务未说新任务 parent / `total_tasks` / `est_hours_total` 如何更新, 也未说是否记入清单 | TL m5 | 接受: parent 沿用 5.5 不新增 checkbox; metadata 同批更新; 拆分记入清单 |
| m6 | 台账骨架 11 个固定标题里没有 fail-closed 停下记录的去处, 而「不改标题」是硬约束 | TL m6 | 接受: 骨架补一个标题 (如「停下与恢复」) 或指定归入「外向动作与授权」, 二选一写死 |
| m7 | TASK-029 第 2 步「`grep -c '#<'` 为 0」与「正向含 `10CG/aria-plugin#<n>`」字面互斥; 负控写死「输出 1」可能与实际占位处数不符 | TL m7 · CR m2 | 接受: 正向条件写成可执行式 (如 `grep -qE '10CG/aria-plugin#[0-9]+'` 或回落形态字面); 负控写「非 0 (占位处数)」 |
| m8 | TASK-029 估 2h 却含第 7 步全量回归 (TASK-021 同工作量估 3.5h) 与八步记账 | TL m8 | 接受: 提到 3.5–4h, metadata 工时同批更新 |
| m9 | 第 6 步 CHANGELOG 节计数断言在本任务内恒绿 (第 5 步已排除在 master 上解冲突), 其真实可红路径在重走时 | CR m3 | 接受: 括注改写为「防第 4 步 fail-closed 后 owner 确认的手工解冲突丢掉对方小节; 本任务内第 5 步已排除解冲突, 故只在重走时可红」 |
| m10 | 读前必看第 14 条对 (l1) 的描述停在 v3 口径 | CR m5 | 接受: 与 v4 / v5 谓词同步 |
| m11 | (j4) 左边界 `[^0-9a-z]` 在 `-i` 下把大写一并折叠 | CR m6 | 接受: 改 `(^|[^0-9A-Za-z])` |
| m12 | TASK-009「源码中不新增 `docs/handoff/` 字面量」与验证脚本 target 自相矛盾且无检查 | CR m7 | 接受: 约束收窄为「不新增**用于路径拼接**的字面量; docstring 说明文字不受限」 |
| m13 | 19 条谓词里 10 条无隔离态, (c2) 明显偏松 | CR m8 | **部分接受**: 按边际判断不逐条加态; 只对 (c2) 收紧或加一个隔离态, 其余作为已知边界写入 handoff |
| m14 | TASK-018 补丁 4「在 write_latest_md 内重算谓词并写反」是意图描述, 不是可直接落笔的变更 | QA m1 | 接受: 给出具体改哪一行、改成什么 |
| m15 | TASK-026「两臂跑到同一份代码 ⇒ 该 run 作废」没写作废后如何补 | QA m2 | 接受: 写明重跑该 eval (与逐 eval 复跑规则一致) |
| m16 | 台账行括注在 TASK-018 / 023 / 024 三处与同组兄弟条目不统一 | KM m1 | 接受: 三行统一 |

## 跨簇一致性 (主控核对; 执笔人同批落)

1. **PP4-M1 / M2 / M3 与 m1 / m6 / m7 / m8 / m9 都改 TASK-029**: 改完逐条列出八步, 核对每步前置在上一步结束时成立、每个「停下」都能在 owner_gates 或任务文本里找到去向与重走口径、回退条前置在其每个调用位置成立。
2. **PP4-M4 / M5 与 m1 改 TASK-030 / 031 / 032 / 034 与 owner_gates**: 主仓侧推送走 C.2.5, 子模块侧仍由 TASK-034 手工执行 —— 两条路径的失败口径要一致 (不 force、停下上报), 并且 gitlink bump 的前置只认「双远端均已核验一致」。
3. **PP4-M6 / M7 与 m10 / m11 / m13 改谓词与验证态**: yaml 谓词块、脚本 `PRED`、EXPECTED、states / expected / 实测块、authoring_rules、归属注释、各 TASK「为真」声明、读前必看第 14 条一次改齐; 由 `--emit-json` 重生成, 不手改; 每条改动的谓词先在 1cb3872 基线原文上实跑为 FAIL。
4. **按 code-reviewer 边际判断收窄矩阵表达**: EXPECTED 由定值矩阵改为「每态只声明期望 FAIL 的谓词集」, 由脚本展开为全矩阵后比对 (断言强度不变, 加一态的成本从 19 格降到 1 行); stdout 仍打印完整矩阵, yaml 实测块照旧由脚本输出重生成。
5. **凡属「跳过 / 降级 / 改序 / 替代」的本轮判断** (删第 7 步核验、主仓推送交给 C.2.5、谓词换量、矩阵表达收窄) 全部补进 AI 流程判断清单。

## 主控自查

- **PP4-M3 是主控 R3 处置的错**: R3 m11 要求在 TASK-029 第 7 步也加谓词一致性核验, 没有核验该检查在那个时点能否执行 —— 与 memory `verify_predicate_inputs_exist` 同形 (只看判据逻辑, 没看它要判的输入在那个时点是否存在)。本轮撤回。
- **PP4-M6 连续三轮未根治**: R2 (PP2-M7 前身) → R3 (PP3-M7) → R4, 每轮都在「块内是否出现 rel_path」这个量上挪边界。主控在 R3 采纳 code-reviewer 的收窄写法时没有问「换个写法还能不能绕」。本轮换量。

## 收敛判断与 R5 安排

R4 不收敛 (7 Major, Vote REVISE 3 / PASS 2)。R5 是 `max_rounds: 5` 的最后一轮:

- **执笔**: 由 v3 / v4 执笔人 (同一实例) 按本报告修订三份文件; 只改三份文件, 不提交, 不派子代理。处置以**删 / 换结构 / 交给已有 Skill** 为主, 不新增流程层。
- **主控**: 核验 (机械核验 / 自建坏态 / git 步序模拟 / 清单完整性 / 逐任务删改) 后提交, 再以新派五席进 R5。
- **R5 之后**: 仍未收敛则按降级策略请 owner 三选一, 并把五席的边际判断与本轮的分布事实 (缺陷集中在发布段与谓词族, 组 1–4 已零 Major) 一并呈上。

## 席位报告

同目录 `post_planning-R4-2026-09-15T232954-303Z-handoff-multibranch-subdir-path-fidelity-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
