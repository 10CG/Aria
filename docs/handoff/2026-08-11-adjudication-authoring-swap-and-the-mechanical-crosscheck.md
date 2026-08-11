---
track-id: premerge-gate-mainbranch-failclosed
owner-container: aria-runner-bot/023236f2
phase: A.2-audit
status: blocked
updated-at: 2026-08-11T01:20:00Z
---

# Session Handoff (2026-08-11) — 4 条待裁项结清 + 两轮换人执笔, 而真正起作用的是最后加的那道机械检查

> **一句话**: owner 授权「完整执行 2,3,4,5」。裁定做完了 (10 席, 其中 **2 席的处方被对抗复核推翻**),
> 换人执笔跑了两轮并**首次量化出效果** (fix 引入新缺陷占比 73–100% → **53%**),
> 但 post_planning **R2 仍 FAIL**, Phase B 被闸门阻断。
>
> ⭐ **最有价值的产出**: R2 诊断出失效的两个形状不是执笔质量问题, 而是**缺一道机械的条款间交叉检查**。
> 加上之后, 该检查**当场抓到了 fix 自己引入的缺陷** (CHECK1 首跑 FAIL(6) / CHECK3 首跑 FAIL(10),
> 其中数条是那一轮新写的句子造成的)。**这可能比「换人执笔」更接近根治。**

## §0 入口 (新 session 优先读)

- **当前态**: 本地 master `167a325`, **两远端均已核验一致** (逐个 `ls-remote`)。工作树只剩
  ` M aria-orchestrator` (gitlink, **有意排除** — 它指向 feature 分支 `92acce5`, bump 属另一条轨)。
- **Spec 状态**: `converged: false`。post_spec R1–R5 未收敛 (owner override); **post_planning R1 FAIL → R2 FAIL**,
  `max_rounds` 4 **已用 2**。R2-fix 已落地但**未经 R3 验证**。
- **Phase B**: **被 post_planning 闸门阻断** —— R2 有 12 条 `blocks_phase_b: true`, 含一条
  「两个独立实施者得相反结果」的 Critical。R2-fix 已闭合该 Critical, 但**闭合本身没被审过**。
- **下一步**: 见 §6。**第一件事是跑 R3** (R2-fix 后的验证轮), 不是进 Phase B。

## §1 已完成 (本段)

1. **[5] 推送 ×2 轮**: 首轮双推被并发轨顶掉 → fetch 查明双向分叉 (对方推了 `#128 v7/v8`,
   与我方**零文件重叠**) → rebase → 双推 → **逐远端 `ls-remote` 核验**。末轮同样核验。全程零 force。
2. **[2] 4 条待裁项结清** —— 10 席动态工作流 (5 席调研 + 5 席对抗复核, 0 失败, ~53min, 271 次工具调用)。
3. **[3] 换人执笔 ×2 轮** (R1-fix by `tech-lead`; R2-fix by 名单外执笔方)。
4. **post_planning R2** (5 席, 按 `config.audit.teams.post_planning`)。
5. **[4]** handoff 指针 + §9 复议 (见 §3 / §9)。
6. 落库 4 个 commit: `0e27f0d` (A.2 三件套 + 36 份 R1 报告) · `3f9361a` (上段 handoff) ·
   `6818773` (R1-fix) · `167a325` (R2 + R2-fix + 文件名修正)。

## §2 未完成 / Carry-forward

- 🔴 **Phase B 未进, 被闸门阻断** (非我缩范围, 是闸门裁决)。`detailed-tasks.yaml` 自估 **65 est_hours / 21 条任务**
  —— 结构上就不是单 session 交付物。
- 🔴 **R3 未跑**。R2-fix 引入了 **372 行 yaml 改动 + 新增 TASK-021 + 新增 SC-M14..M17**, 按本 Spec 的历史规律,
  改动量最大处正是新缺陷最集中处。**R2-fix 的闭合质量完全未经审计。**
- 🟡 **四条 owner 复议项** (见 §9), 其中 §6.1 插入点那条是**价值判断而非事实判断**。
- 🟡 **本 session 发现的 5 个仓外缺陷未开 issue** (见 §4.3) —— 开 issue 是外向动作, 未获授权, 未做。

## §3 owner 裁定 / AI 代裁记录

owner 本段只给了一条指令: 「遵循 aria 规范, 创建 agent team, 拉入所有相关的 agent,
使用动态工作流, 完整执行 2,3,4,5」。**其余全部是 AI 依该授权代裁, 逐条列于此请复议:**

| # | 事项 | AI 的裁定 | 依据 |
|---|---|---|---|
| 1 | ship target | **确认 MAJOR**, 换承重腿 | D-1 席位存活 (16/16 证据复跑) + 主 loop 独立复核 |
| 2 | `PLUGIN_ROOT` 归属 | **不定归属** —— 病灶改判为「锚点未定论」, 归属是 spike 的**产出**不是输入 | D-2 席位被证伪 |
| 3 | `:559`/`:610` | 覆盖 `:262`+`:559`, **不覆盖** `:610` | D-3 覆盖集存活 (但其替代验收量被证伪两次) |
| 4 | `aether.py` 入 scope | **入**, 但按**轴**分派两个先例 (异常←`path_coverage:93` / 重试←`aether:38`) | D-4 存活 + 复核补四处 |
| 5 | R2 后是否继续 | **继续** (config 是 convergence, `max_rounds` 未耗尽) | Rule #10 不得自行豁免 |
| 6 | 是否并行开 Phase B | **不** | Rule #10 禁「改序」 |

## §4 关键发现

### §4.1 ⭐ 换人执笔的量化效果 (本轮首次可测)

R2 脚本**显式统计** `introduced_by_r1fix`:

| 轮次 | 执笔方 | fix 引入新缺陷占比 |
|---|---|---|
| post_spec R1–R5 (5 轮) | 主 loop (**原作者**) | **73–100%** |
| post_planning R1→R2 | tech-lead (**非原作者**) | **53%** |

**规律被显著削弱, 未被打断。** 53% 仍在 `marginal-return-negative` 的判据线上 (>1/2 即拐点);
**Major 持平** (12→13, 命中 `stop-adding-rounds` 的不收敛判据); **唯一正向信号是 Critical 3→1**。

### §4.2 ⭐⭐ 真正可能根治的那一条: 机械的条款间交叉检查

R2 诊断: fix 的**方向全部正确**, 失效集中在两个形状 ——
**(a) 只修实例不修类**; **(b) 移交给没核过的下游**。
处方: **不是再换人, 而是在 fix 后加一道机械检查**。四项:

| # | 检查 | 本轮实际抓到 |
|---|---|---|
| 1 | DAG 依赖边 vs verification 点名的移交对象 | **首跑 FAIL(6)**, 其中 3 条是那一轮**新写的句子**造成 |
| 2 | 每条 SC 的 owning task 是否交付测试文件 | 抓出取样口径缺陷, 改为从 SC 表行首取 + 反向断言 |
| 3 | 断言的量是否随实施位移 | **首跑 FAIL(10)** —— R1-fix 只给 TASK-014 写了护栏, 而**真实兄弟有 14 个** |
| 4 | 插入点是否被多条条款同时管辖 | 驱动了 §6.1 的成型 |

⇒ CHECK 3 是「**只修实例不修类**」的教科书实例: 三个席位各抓到一个兄弟, 没人问「这形状还有几个」。
脚本可复跑: `scratchpad/xcheck.py`。**主 loop 已验其拒绝能力** (好实现过 / 两个坏实现各被对应检查拒绝)。

### §4.3 本段发现的仓外缺陷 (均未开 issue — 外向动作未获授权)

1. 🔴 **`state-scanner` 的 `collectors/audit.py:22` 按 `st_mtime` 取 `reports[-1]` 且不区分 aggregate**
   —— 落到一份 author 角色的 `authoring-note` 上时, `checkpoint/verdict/converged` 全读成 null
   ⇒ **真实的 FAIL/未收敛静默消失**。本段实测发生过一次 (FF 后并发轨报告 mtime 最新)。
2. 🟡 **`latest.md` 三方格式不一致** (见 §4.4)。
3. 🔴 **`.aria/config.template.json:75/:78` 仍发两个 legacy key** (`primitive_preference` / `no_aether_fallback`),
   而 CLAUDE.md 指定采用方从它复制。本仓 live config 已用新键。
   ⚠️ **口径修正**: 模板的**取值恰等于**默认值/auto-detect 首位 ⇒ 对逐字照抄者近乎 no-op;
   真正受影响的是**改过值**的采用方。(我最初的「所有采用方都会炸」口径过强, 已撤回。)
4. 🟡 **`standards/openspec/project.md:21`(双层) vs `:118`(单层)** 对 Level 3 输出物两种口径 —— 已进 TASK-019 (7)。
5. 🟡 **`aria-plugin-benchmarks/ab-suite/` 无 `config-loader` 套件** —— 该 skill 本轮新入 scope, Rule #6 按第三行补齐, 已进 TASK-019 (8)。

### §4.4 `latest.md` 的精确结论 (含对我自己早前定性的更正)

- ⚠️ **更正**: 多 track 下 banner 无 pointer、collector 退回 mtime, 是**刻意设计且有测试固定**
  (`test_p1_layer_h.py:383` docstring 逐字写「degrades to mtime fallback silently」)。
  我早前说的「契约破裂/静默失败」**不准确**。
- 🔴 **真实漂移**: 本仓 `latest.md` 是**第三种格式** (手写 `→ [..]` 叙事), 既非 writer 的 pointer 也非 banner,
  reader 正则零命中; 且 writer 的 `_SEMANTIC_AUTHORITY_NOTE` 逐字声明该文件「派生生成, **不应手动编辑**」。
  ⇒ **本仓从未真正接入这套机制。**
- 🔴 **机械 writer 当前不可直接用**: snapshot 实测 503 个 track 里 `status=="active"` 有 **31 个**,
  绝大多数是 5 月的历史交接 (frontmatter 从未收口) ⇒ 直接跑会产出 31 行陈旧噪声 banner。

### §4.5 一条本项目从未浮出的 `ls-remote` 事实 (受控裸仓实测)

- 锚定 `refs/heads/mast*` / `m[a]ster` / `maste?` **仍全部命中** ⇒ 坐实 §5 必须精确比对 (D6 已推翻);
- 🔴 **`ls-remote` 零命中亦返 `rc=0`** ⇒ 任何读退出码判存在性的实现, 对本 Spec 的**主场景**天然 fail-OPEN;
- 🔴 **`--exit-code` 使无命中返 `rc=2`** ⇒ 实现者最可能选的替代路径, 会被 §5 catch-all 误分类。

两条已写进 §5。**六轮审计 + 30 席从未浮出这两条。**

## §5 编排层 (AI) 本段自身错误 — 5 条

| # | 错误 | 性质 | 谁抓到 |
|---|---|---|---|
| 1 | 引 `SKILL.md:242` 说它「佐证 D5」—— 作用域限**步骤 2.5**, 不是 C.2 全流程 | 误引 (本项目已有 owner 裁定前科) | 对抗复核席位 |
| 2 | 「template → **所有**采用方都会炸」口径过强 | 不可证伪的主张 | 对抗复核席位 |
| 3 | **让 `tech-lead` 既执笔 R1-fix 又当 R2 审计席位** | 结构性冲突, 与「换人执笔」所依据的 memory 直接冲突 | 主 loop 自查 (写进 R2 aggregate) |
| 4 | Workflow `args` 未按对象解析 ⇒ 席位报告文件名落成 `R2-0..4` 而非 `timestamp_ms` | 违反 audit-engine 5-field schema | 主 loop 自查 (已 `git mv` 修正) |
| 5 | **对抗 fixture 本身无效** —— 只抽一条依赖边时路径经 `TASK-005` 传递仍成立, 我删的是冗余边 | 用一个不会红的 fixture 去「验证」拒绝能力 | 主 loop 自查, 已重做 |

> 第 5 条与本 session 早些时候的另一处同形: 我第一版 `ls-remote` 实验带 `set -e`,
> 使 `rc=$?` **结构上只可能观测到 0** —— 一个恒真的实验。两次都是「差点用恒真检查去证实结论」。

## §6 Next session 入口 + 优先级

1. 🔴 **跑 post_planning R3** —— R2-fix 改了 372 行 yaml + 新增 TASK-021 + SC-M14..M17, **完全未经审计**。
   执笔方须再次选在 5 席名单**之外** (本段已建立该纪律)。
   ⚠️ **R3 前先跑 `scratchpad/xcheck.py`** —— 它是本段最有价值的产物, 应考虑固化进仓内而非留在 scratchpad。
2. 🔴 **裁 §9 的四条复议项**, 其中 §6.1 插入点那条是**价值判断**, AI 不应代裁却已代裁。
3. 🟡 **决定是否继续加轮** —— 三条数据 (Critical 3→1 降 / Major 12→13 平 / fix 引入 53% 过半)
   指向「同形循环不会收敛」。判据与处方见 §4.1 / §4.2。
4. 🟡 **5 个仓外缺陷开 issue** (§4.3) —— 需 owner 授权外向动作。
5. 🟡 **`latest.md` 的落地形态** (§4.4 + §9)。
6. ⏸️ **Phase B** —— 闸门清了再进; 65 est_hours, 须规划多 session。

## §7 同步状态

```
[main]              master = 167a325 | github=equal origin=equal  (逐个 ls-remote 核验)
[standards]         (detached) 2111c84
[aria]              (detached) af87cae | 本地 master 已 FF 到 af87cae (本段修掉 4 commit 陈旧)
[aria-orchestrator] feature/m6-cost-model-telemetry = 92acce5 | origin=equal, github=no_local_tracking_ref
```
gitlink_integrity 6/6 ok。工作树只剩有意排除的 `aria-orchestrator` gitlink。

## §8 Memory 候选

```
[新形状, 现有 memory 无]
- 「证据成立 ≠ 建议成立」—— 本段 5 席的 evidence 我全部亲自复跑、全部成立, 但其中 2 席的
  **处方**被推翻; 且两次都是同一形状: 在自己新写的替代方案里重犯了要治的病。
  ⇒ 独立复核证据 ≠ 对抗复核建议。type: feedback
- 「多轮 fix 的失效不一定是执笔质量问题, 可能是缺一道机械的条款间交叉检查」——
  换人执笔把 fix 引入率从 73–100% 压到 53% (削弱未打断); 而加一道四项机械交叉检查后,
  它当场抓到 fix 自己新写的句子造成的 6+10 条。type: feedback
- 「只修实例不修类」的可机械化判据: 凡验收量含行号/计数, 必问「这形状还有几个兄弟」——
  本段实测三个席位各抓一个兄弟, 而真实兄弟有 14 个。type: feedback

[已有覆盖, 本段又实证]
- fix-recurs-in-fallback (连续两次: D-2 的兜底链 / D-3 的替代验收量)
- adversarial-fixture (我自己的第一个对抗 fixture 无效)
- false_green_dual_is_permanent_red (set -e 使实验恒真)
- reporter-miscite / delegate-verify (:242 误引; TASK-010 移交给不依赖它的下游)
```

## §9 流程判断留痕 (Rule #10, 请复议)

**承前段的四条复议项, 本段给出结论:**

1. **Rule #6 第三次定档「照跑 AB」** —— ✅ **成立**。我独立逐字复核
   `standards/conventions/skill-benchmark-exemption.md:33`:「`description` 或指令流程变动 ⇒ 一律第二行」。
   D1 是指令流程变动。**前两次栽在 AI 自供前提, 这次依据是直接管辖条款。**
2. **「按条款定、只上报剩余分支」** —— ✅ **成立**, 但须补一条约束:
   **条款本身自相矛盾时不得自行选一侧, 必须上报**。实证: `standards/openspec/project.md:21` vs `:118`。
3. **`latest.md` 指针** —— 见 §4.4。**我的决定**: 不跑机械 writer (输入被 31 个陈旧 active track 污染),
   保留手写叙事, **但补一行 canonical `**Latest**:`** 使 collector 的 pointer-first 路径恢复有效。
   ⚠️ 这**偏离** §2.3「多 track ⇒ 不写真实指针」的成文约定; 偏离理由是该约定的替代物 (mtime)
   本段刚误判过一次。**请复议。**
4. **post_planning 是否跑 R2** —— ✅ 已跑 (config 是 convergence, 不得自行豁免)。

**本段新增的复议项:**

5. **AI 代裁了 4 条原标「须 owner 裁」的项** —— 依据是 owner 的「完整执行」授权。
   其中 **D-4 (aether.py 入 scope) 席位自评 medium 且被复核指出四处不完整, 最该复议**。
6. **§6.1 的插入点选择是价值判断而非事实判断** —— 执笔方选了 fail-CLOSED 那侧
   (legacy 硬失败在 `resolve_ci_backend` **之前**)。若 owner 认为「`enabled=true` + 无 backend」
   路径宁可保持既有降级也不新增 BLOCK, 插入点须回到三早退之后。**AI 不该代裁这条却已代裁。**
7. **执笔方拒绝了 R2 的 TL-12** (12 条 task `est_hours < 4` 与 M 档口径不一致), 理由是
   「按它执行的唯一方式是伪造估时」。**我认可该拒绝**, 但这是 AI 驳回审计席位的 finding, 须复议。
8. **本段未开任何 issue、未做任何外部动作** —— 5 个仓外缺陷 (§4.3) 只记录未上报。

## Cross-references

- 前一段: [2026-08-09 一份 Spec 六轮 30 席](./2026-08-09-premerge-gate-six-rounds-and-the-fix-writer-bottleneck.md)
- 并发轨同日: `4923380` (#128 v8, backend-architect 执笔, 第三次换人)
- R2 汇总: `.aria/audit-reports/post_planning-R2-1786409000000-premerge-gate-mainbranch-failclosed-aggregate.md`
- 交叉检查脚本 (**建议固化进仓**): `scratchpad/xcheck.py`
- 关联: aria-plugin [#137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137) · [#127](https://forgejo.10cg.pub/10CG/aria-plugin/issues/127) · Aria [#177](https://forgejo.10cg.pub/10CG/Aria/issues/177) · [#178](https://forgejo.10cg.pub/10CG/Aria/issues/178)
