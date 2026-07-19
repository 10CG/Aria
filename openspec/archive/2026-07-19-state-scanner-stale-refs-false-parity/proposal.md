---
unverified_claims:
  - claim: "**裁决接线**: `gitlink_orphaned(R) == true` ⇒ 进 F4′ **blocking** ∀ 子句; `multi_remote_drift` 建议文案「主仓在 R 上引用的子模块 commit 在 R 上不存在 — 从 R clone --recursive 会断裂。修法: git -C S push R <branch>」 (✅ Phase 4 收口, v1.62.0)"
    reason: "symbol 'multi_remote_drift' unclassified reference form"
    symbols: ["multi_remote_drift"]
  - claim: "🆕 **AC-11 (防 R3-C5 恒红)**: **detached-HEAD 子模块** + 全部 remote 刷新成功 + 主仓 equal → `overall_parity` **仍 true**。**本仓可直接 dogfood** (`aria` 子模块正是 detached)"
    reason: "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
    symbols: []
  - claim: "**跨进程同仓并发** (两个终端同时 scan) 写明为**已知可接受降级**: 依赖 git 自身 ref lock; 争用 ⇒ `fetch_ok=false` ⇒ 降级 unknown (**假红方向, 可接受**)。🆕 **v8 (RM-6a) 声明扩到 cache 层**: tmp+rename 防损坏不防 lost-update — 迟写者覆盖早写者的 per-leg 更新 ⇒ 偏红/重复 fetch (可接受, 方向正确); 计数器回退的 fail-OPEN 缝由 3.16 钳位封死。否则 dogfood 时会被当 bug 追"
    reason: "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
    symbols: []
  - claim: "**dogfood (本仓)**: `aria` 子模块 detached-HEAD + 全 remote 真 equal ⇒ `overall_parity` **仍 true** (AC-17); **`standards` / `aria-orchestrator` 的 github 镜像若落后 ⇒ 必须报出来** (AC-16); `sync_status` 与 `tracks_multibranch` 不再自相矛盾 (✅ Phase 4 收口, v1.62.0)"
    reason: "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
    symbols: []
unverified_ack: true
unverified_ack_reason: "post_planning R1 补审 (报告 .aria/audit-reports/post_planning-R1-2026-07-19-state-scanner-stale-refs-false-parity-phase4-aggregated.md) 抓出本 spec 归档时走手工 git mv 而非 openspec-archive skill, #95 两条机械通道 (warn_overlay frontmatter / D auto-issue tracker) 均未点亮 (R1 M-B)。本 frontmatter 为补写。逐条 ack: (1) multi_remote_drift 符号未分类属归档门 _ARTIFACT_PATH_TOKEN_RE / 符号分类器的已知局限 (非本 change 引入), 该符号在 basic-rules.md dispatch 表与 RECOMMENDATION_RULES.md 均有活引用, 非死代码; (2)(3)(4) 三条 dogfood 声称同属分类器只认 ab-results|ab-suite 路径的结构性局限 —— 真实 dogfood 执行记录见 dogfood-evidence.md (与本文件同目录, 按姊妹 spec 2026-07-19-state-scanner-openspec-collector-false-green 先例补写)。**AC-16 正向腿 (镜像真落后必须报出) 在本仓实测恒 vacuous** (live snapshot 全 ok/no_matching_remote), 该腿未获正面验证, 见 dogfood-evidence.md §限制。"
---
# Proposal: state-scanner 陈旧 ref 假同步修复 — 「新鲜度靠获取, 不靠测量」

> **Status**: **✅ Approved v10 (owner sign-off 2026-07-15)** — R9 PASS-with-fixes 2/2 (0 Critical — R1-R8 八轮全 FAIL 后首个非 FAIL), fixes 已全部折入本版 (2026-07-14; D20 三档全分割经受住全部证伪, 唯一实质补丁=负墙钟龄钳位; 12M/13m 全为镜像/残留文本级, 已修并机械复核 [代 R10, 两审计一致建议]; 聚合 `.aria/audit-reports/post_spec-R9-2026-07-14-*-aggregated.md`)。**owner 终审通过 D15′-D20 五条代裁 (D15′ 双角色谓词 / D16 SOT 搬入 aria-plugin+lock / D18 豁免代际上界 / D19 漂移通道#5 划归 Spec C / D20 evidence_grade 三档全分割 E 优先)**。**下一步: Phase A.2/A.3** (落地顺序: Spec C → Spec B → 主 Spec; Spec B 待其独立 post_spec R6 收敛后签)。
> ⚠️ **F10′ 已被 R6 证伪, 勿按其伪码实施** —— 见下方 §F10′ 的 🔴 SUPERSEDED 批注 + [R6 报告](../../../.aria/audit-reports/post_spec-R6-2026-07-12T2300Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **Level**: 3 (Full — 十步循环统一入口的裁决逻辑 + collector 编排 + 网络行为 + 影响所有采用者的配置 + snapshot schema)
> **Created**: 2026-07-12 | **v6 修订**: 2026-07-12 (R5 的 5 Critical + 9 Major; **新增 F10′** per owner 裁定)
> **Decision**: [DEC-20260712-001](../../../docs/decisions/DEC-20260712-001-state-scanner-stale-refs-false-parity.md)
> **Audit trail**: [R1+R2](../../../.aria/audit-reports/post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R3+R4](../../../.aria/audit-reports/post_spec-R3-R4-2026-07-12T2000Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R5](../../../.aria/audit-reports/post_spec-R5-2026-07-12T2230Z-state-scanner-stale-refs-false-parity-aggregated.md) → [**R6**](../../../.aria/audit-reports/post_spec-R6-2026-07-12T2300Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **Track**: `state-scanner-stale-refs-false-parity`
> **Target**: aria-plugin (子模块 `aria/`)

> ### 🔀 范围已拆分 (owner 2026-07-12, 5/5 agent 一致建议)

> **归档状态 (2026-07-19, Phase D.2 + post_planning R1 补审后修订)**: 四段式核心 v1.60.0 + Phase 4 收口 v1.62.0 ship。
> tasks **104/119 done, 活跃未勾 7** (另 8 条在 SUPERSEDED 区, 一律不勾)。
> ⚠️ 此数字在同一 session 内漂过三次 (每次勾选/回退后手写数字即作废: 102→103→104)。**下次归档请在最后一步用 `grep -c` 机械取数再写入**, 不要手抄。归档门 `gate_result` verdict=**warn** / **0 block**。
>
> ⚠️ **本段经 post_planning R1 补审修订** (审计报告: `.aria/audit-reports/post_planning-R1-2026-07-19-state-scanner-stale-refs-false-parity-phase4-aggregated.md`)。
> 该审计是**补跑** —— 原 cycle AI 自行豁免了 post_planning, owner 按不可协商规则 #10 裁定不认可。R1 抓到 1 Critical + 9 类 Major,
> 下列披露清单中标 🆕 的三项是 R1 抓出的**原披露遗漏**。
>
> **🔴 AC-5 声称降级 (R1 C-1)**: 原状态段与 CHANGELOG 把 AC-5 记为「已实现」。**准确表述是: AC-5 只实现到 advisory/检测级, 未实现到裁决级。**
> AC-5 原文要求「track 不可达 ⇒ `overall_parity == false` **或** `reason` 非空」; 实际实现 (`scan.py:_check_snapshot_self_consistency`)
> 是在「`overall_parity` 已为 true 且 `reason` 为空」时才启动检测, 检出后**不翻转 `overall_parity`、不写 `reason`**, 只 append
> `snapshot_self_contradiction` 到 `errors[]`。且该 kind 当时不在 `state-snapshot-schema.md`、不在任何 dispatch、`output-formats.md` 不渲染 `errors` ⇒
> **在使用者侧与「未实现」不可区分**。task 2.12 保持勾选 (代码确实落地且经对抗 review 加固), 但**不得据此声称 AC-5 裁决维度已满足**。
>
> **明示未做 (owner 已裁定可 defer; 🆕 = R1 抓出的原遗漏)**:
> - **3.16 k_eff `observed_rotation` 持久化 — DEFERRED** (fail-CLOSED)。k_eff=k_min 冷启动, **AC-15 防饥饿仅对 rotation ≤ k_min=3 的采用者完全成立**。**不得记 AC-15 已完全满足。**
>   - 🆕 补充 (R1 m-3): AC-15 有**两个**失效源, 原披露只覆盖 3.16 一个。另一个是 3.5d —— AC-15(c) 防饥饿的全称量词写的是「每条**非退避** leg」, 该 carve-out 的前提机制 3.5d 不存在。
> - **3.5d 永久失败 leg 退避** (per-leg `consecutive_failures` + 2^n 跳过): 未实现。🆕 (R1 M-G) 原披露只写「未实现」无影响面论证 —— 它落在 spec 自述的恒红根因面上 (proposal AC-15(c): 「这才是 C-C 的真正根因: 不是分桶, 是饥饿」)。一条永久失败的 remote 每次 scan 照常占 deadline 预算, 既挤压其它 leg 又让自己永久 ¬E∧¬X ⇒ blocking。**影响面数字待补** (本仓 6-8 腿下是否实际可达)。
> - 🆕 **5.5 `_aggregate_flags` docstring 三段式** — 原披露**完全缺席** (R1 M-D)。背后事实: `_aggregate_flags` **零生产调用点** (仅定义 + 测试导入), 符合 v1.53.0 归档门 block 档字面定义而门给 0 block。**待裁定: 删除 (连同测试) 或写明保留理由。**
> - 🆕 **7.2 SOT 清扫 — 已回退勾选** (R1 M-A): 本 cycle 清的是 `verify_mode`/ls_remote (属 task 1.10), 不是本条要求的 F2′ `warn_after_hours` 清扫。详见 tasks.md 该条批注 (含一处待 owner 裁的理由互斥)。
> - **3.10 / 13.7**: 人工审计产出 (collector 依赖核对表 / gitlink contains 性能实测附表) 未产出。
> - **11.1 `/skill-creator` AB benchmark**: 未跑。🆕 (R1 M-E) 原理由「未动 SKILL.md 指令面」**被本 cycle 自己的 diff 否证** —— `basic-rules.md` 改 77 行新增 dispatch 第七路 + `degrade_when`, 那就是「什么状态给什么建议」的规则表; 且 task 11.2 修了 AB rubric (承认判分标准失准) 却不跑用它的 AB。**该豁免理由不成立, 应改走 deterministic skill 的 Rule #6 substitute 路径显式命名替代证据, 或补跑。**
> - **13.x SUPERSEDED 区** (F10′ 原方案, R6 证伪): 保留仅供溯源, 一律不勾。
>
> **归档流程偏离 (R1 M-B, 最该补救)**: 本 spec 走的是手工 `git mv` 而非 `openspec-archive` skill ⇒ #95 的两条机械通道均未点亮 —— warn_overlay frontmatter (Step 2) 与 D auto-issue tracker (Step 7, 门控 `d_payload != null`)。对照组: 同日归档的姊妹 spec `../2026-07-19-state-scanner-openspec-collector-false-green/proposal.md` 首行即 frontmatter。**已补: 见本文件 frontmatter + tracker issue [Aria #168](https://forgejo.10cg.pub/10CG/Aria/issues/168)。** (⚠️ 本句原先也是提前宣称 —— frontmatter 补了但 tracker 当时未建, 跑 R2 前自查抓出并补实。)
>
> **follow-up**: Aria #165 (镜像漏推) — 本 cycle 产出 A/B/C 评估报告 (issue 评论), 核心结论: F10″ **不可**直接复用为 bump 守卫。


---

## Why

`state-scanner` 是十步循环的**统一入口** (Rule #2)。它的 `sync_status` **会撒谎** —— 本地 remote-tracking ref 陈旧时报 `parity: equal` / `overall_parity: true`, 而工作树实际落后远程。后果: **AI 基于落后工作树开工 → 重复劳动**。它本该是这类事故的防线, 现在反而是**假绿的来源**。

**本 session 活体受害** + **R1 独立复现** (未修改代码 `fc7c372`, 真 fixture 跑真 collector):
```
fixture: refs/remotes/{origin,github}/master=367e66e, 真实远程=12f730a (前进 4 commit), FETCH_HEAD age=14h
overall_parity   : True        ← 假绿
local_refs_stale : <absent>    ← 14h < 24h, 没置位
  origin  parity=equal  behind=0
  github  parity=equal  behind=0
```

**HEAD 上此刻的活体现状**:
```
overall_parity: True
main:                   [(github, equal),   (origin, equal)]
 sub aria:              [(github, unknown), (origin, unknown)]
 sub aria-orchestrator: [(github, unknown), (origin, equal)]     ← 其 github 镜像实际落后 32 commit
```

> **同一份 snapshot 自相矛盾**: `sync_status` 说「已同步」, 而 `tracks_multibranch` (基于 Phase 1.16 的**新鲜** fetch) 看到了并发 session 在 2026-07-12 ship 的 handoff。**这个内部矛盾就是 collector 编排缺陷的指纹。**

---

## 核心洞察 — 一个不变量, 三种违反; 以及它的对偶

`_aggregate_flags()` docstring 记载 **QA-C1**: *"all-unknown inputs short-circuited to True with no data"* —— **「零证据」不得当「正证据」**。

| # | 违反形态 | 状态 |
|---|----------|------|
| 1 | **零证据** 当正证据 | QA-C1 已修 |
| 2 | **陈旧证据** 当新鲜证据 | 本 Spec |
| 3 | **从未获取过的证据** 当正证据 (`age is None` → 判「不陈旧」) | 本 Spec (R1 发现) |

**对偶不变量** (R2/R3 教训, 本 Spec 自己犯过三次):
> **假绿的反面是恒红, 两者同样零信息量。** 判据 = **该信号在健康常态下应该是什么值?**

**方法论教训** (R3-C5): 修复不能**点修**, 必须**类修**。QA-C1 只修了 no-data 没修 old-data; v3 只豁免了 `ahead` 没问「还有哪些健康常态值落在允许集之外」。⇒ **必须把 `parity` 的取值 × `reason` 的枚举摊开, 逐格问一遍。** 见下 §裁决表。

---

## 🔬 谓词定义域横扫 (v6 新增 — 把「类修」从纪律变成机制)

> **R5 元教训**: R4 把「类修不能点修」的教训**只点修在 `blocking_unknown` 上**, 没有横向扫一遍「本 Spec 里**还有哪些谓词**是正向枚举 / 定义域不完整」⇒ **第六次复发在 `has_unreachable_remote`**, **第七次在 `可信` 的 null**。
>
> **本表是防第八次的机制**: 本 Spec 引入或修改的**每一个**谓词都必须在此登记, 并回答两个问题 —— **(1) 定义域完整吗? (2) 补集的默认是什么?**

| 谓词 | v6 定义 | 定义域完整? | 补集默认 | v5 的病 |
|------|---------|------------|----------|---------|
| `证据资格(r)` | 🔍 **v8 (D15′)**: `fetched_at ≠ null ∧ (now − fetched_at) ≤ evidence_window (1h)` — ∃ 正证据侧, 世界时间新鲜 | ✅ (null ⇒ false) | `false` (fail-CLOSED) | ❌ v7 单谓词 可信 兼任两角色 ⇒ R7 三 Critical (陈旧 equal 替全仓作证 / split-brain / hard_cap 放宽 2000×) |
| `豁免资格(r)` | 🔍 **v8 (D15′+D18)**: `fetched_at ≠ null ∧ generation_age ≤ k_eff ∧ wall ≤ hard_cap (7d) ∧ consecutive_unverified < k_eff` — equal 降级侧; k_eff 收敛耦合见 F3′ (v9: 分母 per-host + 冷启动 k_min) | ✅ (null/generation 缺失/负代龄钳位 ⇒ false; 见 tasks 3.16) | `false` (fail-CLOSED) | ❌ v7 k=3 与 rotation 脱钩 (实测拓扑 rotation=4, 零边距); 无 D18 时限升级 |
| 🆕 `evidence_grade(r)` | **v9 (D20/8C-2)**: 三值 `{fresh [E], stale_unverified [¬E∧X], expired [¬E∧¬X]}` — **独立 per-remote 字段, 不进 parity.reason** (补集陷阱防, 与 gitlink_integrity 同构); 守卫全分割 (两两互斥 ∪ 全覆盖 — 5.1d 新维度机械断言) | ✅ (三格恰覆盖 E×X 全域) | expired ⇒ not_refreshed blocking (fail-CLOSED) | ❌ v8 三档守卫在 E∧¬X 重叠 (R8 两 agent 独立命中, 第 11 次复发) |
| `benign_unknown(r)` | 显式白名单, 两层 (① fetch-无关 / ② fetch-依赖 ∧ **证据资格** [v8]) | ✅ | — (它是白名单本身) | ⚠️ `remote_branch_missing` 分桶错 (见 F4′) |
| `blocking_unknown(r)` | `parity=="unknown" ∧ ¬benign_unknown(r)` | ✅ **补集定义** | **阻断** (fail-CLOSED) | ✅ v5 已正确 |
| `has_unreachable_remote(r)` | `fetch_ok(r) == false` (**试了→失败**, 与 `error_kind` 无关) | ✅ (v6: 三态使枚举白名单多余) | **置位** (fail-CLOSED, **零枚举**) | ❌ v5 = 「按 **network 类**」= **正向枚举** ⇒ fail-OPEN |
| `fetch_ok(r)` | **三态** `{true, false, not_attempted}` | ✅ (v6 补第三态) | — | ❌ v5 二值 ⇒ deadline 砍掉的 leg 无归属 |
| **deadline-砍掉的 leg** | **不是 reason 值**, 是 `fetch_ok = not_attempted` ⇒ 裁决权交回三档全分割 (v10 D20, SOT=F4′) | ✅ | E ⇒ 作证; ¬E∧X ⇒ stale_unverified (可见); ¬E∧¬X ⇒ blocking | 🔴 **v6 起草时一度归 benign ① ⇒ 假绿 (第八次复发), owner 自查推翻** |
| `enforced_set` | `enforced_remotes` 非空则取之; **`[]` ⇒ 自动发现全部 remote** | ✅ (v6 补空值) | 自动发现 | ❌ v5 未定义 `[]` ⇒ 实现者直读 ⇒ AC-12 非空护栏 ⇒ **默认采用者恒 false** |
| `has_unpublished_branch(r)` | `parity=="unknown" ∧ reason=="no_local_tracking_ref" ∧ **证据资格(r)** [v8]` (**per-remote**) | ✅ (v6 首次定义; v8 换谓词) | `false` | ❌ v5 **被引用 4 次, 从未定义** (proposal L197/L250 + tasks 5.4/9.2) |
| `has_pending_push(r)` | `parity(r)=="ahead"` (沿用 `multi_remote.py:400`) | ✅ | `false` | ✅ 无变更 |
| `overall_parity` | 见 F4′ 三子句 | ✅ | `false` | ✅ v5 已正确 |
| `error_kind(r)` | 复用 Spec B 分类器 (**词表按 Spec B 的 OQ-B1 裁定 = (b) 旧词表**) | ⚠️ 依赖 Spec B | `unknown` (catch-all) | ❌ v5 三套词表未裁定 |
| `parity(r)` | 沿用代码 5 值 `{equal, ahead, behind, diverged, unknown}` | ✅ | `unknown` | ✅ 无变更 —— F10″ 后 **完全不碰它** (F10′ 想改它, 已证伪) |
| 🆕 `gitlink_orphaned(R)` | **v8 (F10″/D14 + R7 修)**: `∃ S: C=refs/remotes/R/<branch> ∧ G=ls-tree(C,path) [mode==160000] ∧ G 在 S 的 R/* 全不 contains ∧ ¬shallow(S) ∧ 豁免资格(主仓,R) ∧ 豁免资格(S,R) ∧ gen(S,R) ≥ gen(主仓,R)`; **前提: Fetch 1 带 --prune** (无 prune 时本地化石 ref 使 contains 假绿 — R7 狩猎 C-1) | ✅ — **八分支各有归宿** (v8 补 3): C 缺失⇒no_published_ref; **path 非 gitlink (ls-tree mode≠160000)⇒非 gitlink skip 可见** (rev-parse 对 tree rc=0, 不能按 rc 探); S 未 init⇒uninitialized; shallow⇒unknown 可见; ¬豁免(S,R) 或 gen 序不满足⇒**orphan_unverified (D18: 连续 ≥k_eff 代升级 blocking)**; **contains rc=129 no-such-commit ∧ 豁免(S,R)⇒orphaned 候选 (G 无处存在 = 更重破损, 不得落 soft-error)**; 其它 rc≠0⇒soft-error 可见; **S 无 remote R⇒no_matching_remote 可见** (与真 orphan 原语层同像, 靠此分支区分) | **true ⇒ blocking**; 无法判定 ⇒ 可见 + D18 时限升级 (fail 向可见, 逾期向红) | ❌ v7 五分支漏 3 格 + 无 prune 前提 + 无主仓腿/gen 序条件 (R7 RC-1/RC-5/RM-1/RM-2/RM-3) |

> **闸门**: tasks 5.1d 加机械检查 —— **本表的谓词集合必须与 Spec 正文中出现的谓词集合逐字相等**。新增谓词而不登记 ⇒ 检查失败。

---

## 现状 (code-grounded, R1-R3 五方实测)

1. **陈旧度算了但不参与裁决**: `_aggregate_flags` (`multi_remote.py:371-418`) 只读 `parity`; `local_refs_stale` (L494-507) 是纯咨询 boolean。
2. **连「陈旧」都没判出来**: `warn_after_hours` 默认 24; 事故 ref 陈旧 14h < 24h。
3. **collector 顺序倒置**: Phase 1.12 (sync, `scan.py:106`) 跑在 Phase 1.16 (`coordination_fetch`, **真 fetch**, `scan.py:119`) **之前** —— **消费者早于生产者**。
4. 🔴 **新鲜度信号无 per-remote 分辨率**: `_fetch_head_age_hours` (L130-142) 读 `<gitdir>/FETCH_HEAD` **mtime** —— **每仓一个文件**, 任何 remote 的 fetch 都整体覆写。R1 阈值扫描: 前移 fetch 后, **阈值降到 3.6 秒都救不回 github**。
5. 🔴 **子模块零覆盖**: `_scan_repo` 恒返回 `stale=False` (死返回值); `_fetch_head_age_hours` 在 FETCH_HEAD 缺失时返回 `None`, 而 L497 `if age is not None and age > warn` ⇒ **`None` 判为「不陈旧」**。实测三个子模块 `.git/modules/*/FETCH_HEAD` **全不存在** ⇒ **「从未 fetch」被当成「最新鲜」**。
6. 🔴 **本地不存在可用的 per-remote 新鲜度信号** (R1 逐一实测排除):

   | 候选 | 结论 |
   |------|------|
   | `FETCH_HEAD` mtime | repo 全局单值, 任一 fetch 都重置 |
   | `.git/refs/remotes/<r>/<b>` 文件 mtime | **只在 ref 值变化时更新** → 「刚 fetch 但没变」与「3 天没 fetch」不可区分 |
   | 同上, packed 之后 | `git pack-refs` (gc 自动跑) 后 loose 文件**直接消失** |

   ⇒ **新鲜度不能「测量」, 只能「获取」。**
7. 🔴 **`enforced_remotes` 是死配置 + 假文档** (#95 靶心):
   ```
   DEFAULTS.json → state_scanner.multi_remote.enforced_remotes = null   ← _load_config 读的 block
   DEFAULTS.json → 顶层 multi_remote = {enforced_remotes: [], read_only_remotes: []}
   grep enforced_remotes / read_only_remotes 在 .py 中命中: 0 / 0
   sync-detection.md:515 却记载它「已实现」
   ```
   **且顶层 block 已是跨 skill 公共契约** (R3-M2): `phase-c-integrator/SKILL.md:574` 明写「skill 级 `enforced_remotes == null` 时**继承顶层** `multi_remote.enforced_remotes`」, `system-architecture.md:928` 的 worked example 亦用顶层键。
8. 🔴 **`sync.py` 是第三个平行 ref 读取点**: `_collect_current_branch` (`sync.py:86-197`) 独立对 `@{u}` 算 ahead/behind, **无 `fetch_ok` 概念**, 而 `scan.py:127` 把它与 `multi_remote` 合并进**同一个** `sync_status` 对象 ⇒ origin fetch 失败时**同一 snapshot 自相矛盾**。

---

## 承重性能实测 (spike-first)

> **采集条件**: 2026-07-12 ~18:40 UTC / dev 容器 (LXC) / 10CG Lab 内网 / origin = `forgejo.10cg.pub` 走 **Cloudflare Access** (~7s/腿, SSH 握手主导) / github = `github.com` (~3.5s/腿) / 8 个 (repo, remote) 对 = {主仓, aria, standards, aria-orchestrator} × {origin, github} / warm / SSH **未**复用 (无 ControlMaster)。

```
串行全量 fetch (8 对) = 42.7s     并行全量 fetch (8 对) = 7.6s  ← 等于最慢单腿
当前 scan 已在付的    ≈  7.0s     当前 scan 全程        = 16.9s
⇒ 边际 ≈ +0.6s (+4%)              (tech-lead 独立复现: 7.81s, 8/8 rc=0)

单次 ls-remote ≈ 单次 fetch (均被 SSH 握手主导) ⇒ fetch 严格更优 (同价且真刷新 ref) ⇒ ls_remote 方案删除
```

> ⚠️ **单点数据, 不是通用承诺。** aria-plugin 跨项目分发; 采用者的 remote 数 / 子模块数 / 网络可能远差。**不得把 +4% 写进 CHANGELOG 当承诺。**

**同仓并发 fetch 竞态 —— 实证不存在** (R2 backend-architect, 10 轮): `10/10 rc=0`, FETCH_HEAD 两条记录都在, 零锁错误 (git 隐式串行化)。⇒ **v3 的「同 repo 内串行」约束删除** (不必要的保守, 且它与承重数字的采集条件不一致)。

---

## What Changes

### 🔴 F10″ — orphaned-gitlink 可达性检查 (**v7 定稿方向**; owner 裁定 2026-07-12; **实测已验**)

> **F10′ (下方, 已 SUPERSEDED) 被 R6 三方独立证伪**: 它要修的那个事故, 在 git 眼里是 **`ahead`** 而不是 `behind`。
> ```
> 事故态: standards 本地 = 79b7cd6 | github/master = 9df1722 (镜像落后 2)
> $ git rev-list --left-right --count 79b7cd6...9df1722
> 2	0                                    # left=ahead=2, right=behind=0
> multi_remote.py:205:  ahead, behind = int(parts[0]), int(parts[1])
> ⇒ parity = "ahead"                     ← 不是 "behind"!
> ```
> 而 **`ahead` 的非阻断性被三处独立证据锁死** (AC-8/DEC-D7 + golden fixture `main github->ahead ⇒ overall_parity: true` + AB rubric `:143` "Should exclude parity: ahead")
> ⇒ **F10′ 上线后, 事故场景的 `overall_parity` 仍是 `true`。AC-16 与 AC-8 字面互斥。**

#### 根因: `parity` 天生无法表达要修的那个不变量

| 语义 | 是什么 | 正确处置 |
|------|--------|----------|
| 「我本地有没推的 commit」 | **开发常态** | `has_pending_push` (**AC-8/D7 正确, 不必重开**) |
| 「**已发布的** gitlink 在 remote 上不可达」 | 🔴 **完整性破损** | **必须阻断** |

**今天真正断掉的不变量是「跨仓可达性」, 不是 parity**:
```
主仓 master 已推到 github (dfb3118 ✓)
  └─ 它引用的 gitlink standards@79b7cd6
       └─ 在 standards 的 github 上不可达 ✗
⇒ 任何人 clone --recursive from GitHub = 断裂        ← 这就是今日事故 + CLAUDE.md 2026-04-10 事故
```

#### F10″ 定义

```
gitlink_orphaned(R) := ∃ 子模块 S:
      C = 主仓在 R 上【已发布】的 commit (refs/remotes/R/<default>)   # 只看已发布的, 不看本地 HEAD
    ∧ G = C 引用的 S 的 gitlink
    ∧ G 在 S 的 remote R 上【不可达】
      # 判定: git -C S branch -r --contains G --list "R/*"  为空
      # ⇒ 枚举 R/* 下【实际存在】的 ref, 零分支名假设
    ∧ ¬shallow(S)                                                  # shallow ⇒ 无法判定可达性 ⇒ 诚实 unknown
```

`gitlink_orphaned(R)` 为真 ⇒ **blocking** (进 `overall_parity` 的 ∀ 子句), 且 `multi_remote_drift` 给出成因专属建议:
「**主仓在 `R` 上引用的子模块 commit 在 `R` 上不存在 —— 从 `R` clone --recursive 会断裂。修法: `git -C S push R <branch>`**」

#### F10″ 实测验证 (owner, 2026-07-12, 真仓真命令)

| 场景 | 期望 | 实测 | |
|------|------|------|---|
| **正例**: 今天的事故态 | 报警 | `merge-base --is-ancestor 79b7cd6 9df1722` → **不可达 ⇒ ORPHANED** | ✅ |
| **反例**: 开发期本地 commit (本地 HEAD 领先 github) | **不报警** | F10″ 只看**已发布**的 `github/master=dfb3118`; 其 gitlink **可达** | ✅ **零误报** |
| **分支名假设** | 不得有 | `branch -r --contains <G> --list "github/*"` → 命中 `github/master` | ✅ **零假设** |

#### F10″ 一次性免疫 R6 的全部 3 个 Critical + M-4

| R6 finding | F10″ 为何免疫 |
|---|---|
| **C-1** (ahead/behind 语义冲突) | **完全不碰 `parity`** ⇒ 与 AC-8 / golden fixture / AB rubric **零冲突** ⇒ **D7 不必重开** |
| **C-2** (`{HEAD,master,main}` 枚举 ⇒ 健康仓恒红; 实测三个子模块的 `refs/remotes/github/HEAD` **全部不存在**) | 检查**具体 SHA 的可达性** ⇒ **不猜分支名** |
| **C-3** (shallow 守卫丢失) | 可达性检查的 shallow 守卫语义清晰 (无法判定 ⇒ 诚实 unknown) |
| **M-4** (**有意 pin 住旧 commit 的子模块**在 F10′ 下算出 `behind` ⇒ 恒红) | **天然免疫** —— pin 住的 gitlink 只要在 remote 上**可达**就不报警, **与"新不新"无关** |

> ✅ **v7 已完成 (2026-07-14)**: tasks §13 已按 F10″ 重写; AC-16/AC-17 已重述; 谓词横扫表已登记 `gitlink_orphaned`。
>
> 🔴 **v8 前提与边界 (R7 折入)**:
> - **喂数视图前提 (RC-1)**: contains 读本地 remote-tracking refs, 而 `git fetch` (无 `--prune`) **只增不删** — 远端删支/force-push 后本地化石 ref 仍 contains G ⇒ 假绿。⇒ **Fetch 1 必须带 `--prune`** (见 F3′/tasks 3.1); `refs/aria/coordination` 走独立 Fetch 2 (#141), 不在 Fetch 1 refspec 内, **prune 不影响它** (tasks 3.15 写死断言)。
> - **绑定方式声明 (RM-3)**: F10″ 用 **remote 名字配对** (主仓的 R ↔ S 的同名 R) 作代理判据。本仓 .gitmodules 是绝对 forgejo URL ⇒ 「从 R clone --recursive 断裂」的字面机制只在**相对 URL / 同名镜像自洽**场景成立; 对绝对 URL 仓, F10″ 保护的是**镜像集合自洽**不变量 (发布的引用图在每个 remote 上自包含)。S 无同名 R ⇒ `no_matching_remote` 可见分支 (不阻断)。
> - **snapshot 载体 (RM-10)**: 判定结果落独立字段 `multi_remote.gitlink_integrity[]` per-(R,S): `{remote, submodule, status ∈ {ok, orphaned, orphan_unverified, no_published_ref, not_a_gitlink, uninitialized, shallow_unverifiable, no_matching_remote, soft_error}, consecutive_unverified}` — **不进 parity.reason** (进 reason 会被 blocking_unknown 补集全判 blocking, 与「skip/不判」矛盾); 裁决接线与逐格归属见 tasks 13.4。
> - **「可达」的有意收窄 (RM-11)**: 可达 := **branch-可达** (`R/*` remote-tracking 分支; Fetch 1 `--no-tags`)。tag-only-reachable 的 pin (分支已删仅 tag 可达) **会报警** — 有意: 判据统一且 tag 空间不在喂数视图内; 逃生口 = `read_only_remotes` 排除该 remote 或显式接受告警。AC-17 加 tag-only fixture 钉死此行为。

---

### ~~🆕 F10′ — detached-HEAD 仓库的 commit-based parity~~ 🔴 **SUPERSEDED (R6 证伪, 2026-07-12) —— 勿实施**

> **保留全文仅供审计溯源。** 它的**诊断**是对的 (detached-HEAD 子模块的非-origin drift 结构性不可见), 但**药方**用错了原语 —— 见上方 F10″。

> **R5 的决定性发现**: R1-R4 反复打磨 F4′ 的**裁决公式**, 但从未问过 —— **「这个公式要裁决的 `parity` 值, 真的会被生成出来吗?」**
> 答案是: **对 detached-HEAD 子模块 (子模块的规范常态), 不会。** 一个完美的裁决公式, 裁决的是一个**从不存在的输入**。

**根因** (`multi_remote.py:148-183` `_remote_parity_local_refs`, **生产默认路径** `verify_mode=local_refs`):

```python
if branch is None:
    base["reason"] = "detached_head"
    return base                              # ← 在触碰任何 remote-tracking ref 之前就返回
...
ref = f"refs/remotes/{remote}/{branch}"      # ← 只有走到这里才会真的看这个 remote 的数据
```

子模块经 `git submodule update --init --recursive` (**CLAUDE.md 让每个新采用者跑的第一条命令**) 后**恒为 detached HEAD** (`branch=None`) ⇒ **对每一个 remote 都在同一行早退**。

⇒ 🔴 **无论 F3′ 把 github 的 ref fetch 得多新鲜, 这个函数从未看过它一眼。网络成本已经付了, 但比较从未发生。**
⇒ 两个 remote 条目都是 `unknown/detached_head` ⇒ F4′ 判**恒 benign 不阻断** ⇒ **`overall_parity` 仍 `true`**。

**今日活体证据** (production, 非 fixture —— **本 Spec 的 R5 审计当天, 本仓自己复现**):

```
scan.py snapshot (2026-07-12T21:58Z):
  overall_parity: true                                       ← 报「已同步」
  standards:         github parity=unknown reason=detached_head
  aria-orchestrator: github parity=unknown reason=no_local_tracking_ref

ls-remote 地面真相 (同一时刻):
  standards          gitlink=79b7cd6  origin=79b7cd6 ✅  github=9df1722 ❌ 落后 2 commit
  aria-orchestrator  gitlink=8b947fa  origin=8b947fa ✅  github=daf7c79 ❌ 落后 2 commit
  ⇒ 主仓 master (已在 GitHub 上) 引用的两个 gitlink 在 GitHub 上根本不存在
  ⇒ `git clone --recursive` from GitHub = 断裂
```

**state-scanner 对一次真实的、对外可见的仓库完整性破损, 报告「已同步」。** 这正是本 Spec §Why 引用的活体证据 (`aria-orchestrator github 落后 32 commit`) 与 **CLAUDE.md 记载的 2026-04-10 真实事故** (aria v1.11.1 发版后未推 GitHub, 市场版本滞后) 的**同一模式** —— **本项目已经发生过两次, 不是假想**。

**交叉证据: snapshot 里没有任何字段能捕获它。** `sync.py:36-41`:
```python
_ORIGIN_HEAD_REFS = ["refs/remotes/origin/HEAD", "refs/remotes/origin/master", "refs/remotes/origin/main"]
```
⇒ `sync.py` 的 commit-based 子模块 drift 算法 (**不依赖分支名, 算法本身是对的**) **硬编码只对 origin 跑**, 从不看 github。

**变更 (不是发明新机制 —— 是把已验证可工作的算法搬过来)**:

`_remote_parity_local_refs` 在 `branch is None` 时**不再早退**, 改走 **commit-based 比较** (复用 `sync.py:200-330` 已验证的算法):

```
if branch is None:                                   # detached HEAD (子模块常态)
    remote_ref = 首个存在者 of refs/remotes/{remote}/{HEAD,master,main}   # 与 sync.py 同一 fallback 链, 但按 remote 参数化
    if remote_ref 不存在:  reason = "no_remote_head_ref";  parity = "unknown"    # → blocking (fail-CLOSED)
    else:
        behind/ahead = git rev-list --left-right --count local_head...remote_ref
        parity = equal | behind | ahead | diverged     # ← 真正的 parity, 不再是 unknown
```

- **`detached_head` 不再是「恒 benign 的黑洞」** —— 它现在只在 **remote 侧没有任何 HEAD/master/main ref** 时才产生 `unknown` (新 reason `no_remote_head_ref`, 归 **blocking** 桶, fail-CLOSED)。
- **`shallow_clone` 仍恒 benign** (shallow 仓的 `rev-list` 计数本就不可信 —— 这是 fetch 也改变不了的结构性限制)。
- **对主仓无影响** (主仓有分支名, 走原路径)。

**Impact**: `overall_parity` 在**本仓当前状态**下会从 `true` 变 **`false`** (因为 github 镜像若落后, 现在真的会被报出来)。⚠️ **这是有意的行为变更, 也正是本 Spec 存在的理由。** 但它同时意味着 **AC-11 的措辞必须改** —— 见 Verification。

> ⚠️ **对偶检查** (防第 6 次过冲成恒红): 「detached-HEAD 子模块 + 全部 remote 真的 equal」在健康常态下必须是 **`overall_parity: true`**。F10′ 让子模块**能**产出 `equal` 正证据 (今天它连 `equal` 都产不出来), 所以这个方向是**从恒 unknown 走向可判定**, 不是走向恒红。**AC-16/AC-17 对偶验收此点。**

---

### F3′ — 新鲜度靠获取 (`remote_refresh`)

`coordination_fetch` 泛化为**并行 fetch 所有 enforced remote** (主仓 + 全部子模块), **改名 `remote_refresh`**, 落点 **Phase 0.5** (`collect_git_state` 之前)。

- **`fetch_ok` 锚定 Fetch 1** (#141 归档 Spec 的 two-fetch 语义): Fetch 1 = `+refs/heads/*` (**载重**), Fetch 2 = `refs/aria/coordination`。**benign-missing 的 coordination ref 不得置 `fetch_ok=false`** —— github/子模块远端**几乎必然没有**该 ref, 否则**每个非-origin remote 恒 false ⇒ 恒红**。
- **并发**: 全并行, **per-host 上限** (默认 ≤4/host; sshd `MaxStartups` 默认 `10:30:100`, 超限会**随机丢连** ⇒ 不可复现的间歇性假警报)。丢连**重试 + 退避** (与真 auth/network 失败区分)。
  🔴 **「per-host」= 按解析后的 hostname 去重** (跨仓库、跨 remote 名聚合), **不是按 remote 名字个数** (v6 修正, R5-C-C):
  ```
  实测本仓真实拓扑 (4 仓 × 2 remote):
    origin → forgejo.10cg.pub   (全部 4 仓同一 host)
    github → github.com         (全部 4 仓同一 host)
  ⇒ 只有 2 个物理 host, 不是 8 条独立通道
  ```
  ⚠️ **R4 的 `ceil(60/4)×7s≈105s` 算式是错的** —— 它把 cap-4 当全局单池。按 per-host 正确计算 (20 子模块场景):
  ```
  forgejo: ceil(20/4)=5 轮 × 7.0s = 35.0s
  github:  ceil(20/4)=5 轮 × 3.5s = 17.5s   (与 forgejo 并发, 非串行叠加)
  ⇒ wall-clock ≈ max(35.0, 17.5) = 35s      (不是 105s)
  ```
  **结论方向不变** (35s ≫ 默认 15s), 但**量级差 3 倍**。⇒ 若实现者按「remote 名字个数」限流, 真会跑出 105s 那一档。**必须写死 hostname 去重语义。**
  > 📌 **元教训**: R4 的**五个 agent 一起用了错误的算式**, R5 用真实拓扑推翻。memory `feedback_cross_agent_verdict_independent_verify` 再度实证 —— **跨 agent 一致 ≠ 正确**。

- **全局 deadline** (R3-M11 + **v6 三态修正**, R5-C-C): `refresh_deadline_seconds` (默认 **15s**)。**网络成本必须有硬上界**。
  🔴 **到点未完成的 leg ⇒ `fetch_ok = "not_attempted"` (三态之一) ⇒ 不推进 `fetched_at` / 不置 `has_unreachable_remote` (我们没试, 不是对方不可达) / 🔴 但也 __不__ 直接标 `not_refreshed`。**
  **它的裁决完全交给双角色谓词** (v8 D15′, F1′ 的新鲜度轴统一处理):
  ```
  leg 被 deadline 砍掉 ⇒ fetched_at 保持上一次的值 (不推进); v10 D20 三档全分割:
     E  (证据资格, 墙钟 ≤1h)  ⇒ 其 equal 照常提供 ∃ 正证据            ✅ 不恒红
     ¬E ∧ X (豁免资格)        ⇒ stale_unverified (可见/不作证/不阻断)  ✅ 诚实中间态
     ¬E ∧ ¬X                  ⇒ equal 降级 not_refreshed ⇒ blocking    ✅ 诚实

  > ⚠️ **不得把 `deadline_skipped` 归入 benign 桶** (v6 起草时一度采纳此方案, **owner 自查推翻**):
  > benign ① 的判据是「**fetch 不能改变它**」(`detached_head`: fetch 一万次也变不成 equal); 而 `deadline_skipped` 是「**我们没去问**」—— fetch **完全能**改变它 ⇒ 按本 Spec 自己的分类法, 它属于「**我们不知道真相, 而这是可以知道的**」。
  > **归 benign 的后果 (可推)**:
  > ```
  > 大仓 60 腿, deadline 15s:
  >   origin (快, 队列靠前) 刷新成功 ⇒ 证据资格 ∧ equal ⇒ 满足 ∃ 子句
  >   github 被 deadline 砍 ⇒ 若判 benign ⇒ 不阻断
  >   ⇒ overall_parity = TRUE
  >   但 github 可能真的领先 100 个 commit —— 我们根本没去看
  > ```
  > ⇒ 🔴 **假绿。本 Spec 要杀的那个 bug, 经由新引入的 deadline 复活 —— 这将是同一不变量的第八次复发。**
  > **「零证据不得当正证据」在这里的形态: 「没去问」不等于「不适用」。**

  **为什么不能像 v5 那样标 `not_refreshed`** (v5 的致命错):
  ```
  not_refreshed ∈ blocking 桶
    ⇒ ∀ r: ¬blocking_unknown(r)  对该 leg 失败
    ⇒ overall_parity = false   (即便其余 59 条腿全部 证据资格 ∧ equal)
  而「某条 leg 被 deadline 砍掉」对大仓采用者是**每次扫描的常态**, 不是偶发故障
    ⇒ overall_parity 对该采用者**恒 false, 且没有任何一次 scan 能翻身**
    ⇒ 🔴 性能护栏亲手制造了正确性回归 —— 本 Spec 第 5 次「修假绿过冲成恒红」
  ```
  **v6 的判据 (v8 按 D15′ 精化)**: deadline 只影响「**这次刷没刷**」, **不影响「我们对它的了解是否仍然新鲜」** —— 后者由 **双角色谓词**承担: `证据资格` (墙钟 1h, ∃ 侧) + `豁免资格` (代际 k_eff + 墙钟 7d, 降级侧)。
  ⇒ **`overall_parity` 的正确性不依赖 deadline 数值大小** (稳态下三档谓词兜住 [v10]), 但**也绝不因为「我们没去看」就放行** (过期即阻断)。默认值大小只影响**多快能覆盖全部 leg** —— 由防饥饿排队保证最终覆盖。

  🔴 **防饥饿 — fetch 优先级 = 最久未刷新者优先** (`fetched_at` 升序; `null` 最优先):
  若 fetch 顺序固定, deadline 会**每次砍掉同一批靠后的 leg** ⇒ 那些 leg 的 `fetched_at` **永远推不进** ⇒ 新鲜度谓词恒 false ⇒ **恒 blocking ⇒ overall_parity 恒 false 且永不翻身** (**这才是 C-C 的真正根因 —— 不是分桶, 是饥饿**)。
  ⇒ **按 `fetched_at` 升序排队** ⇒ 每条 leg 在 rotation = ⌈max_host_legs/每scan覆盖数⌉ 代内必轮到。🔴 **v9 收敛条件 (R8 8M-11 补墙钟项; 取代 v8 单不等式)**: 不恒红 ⇐ **rotation ≤ k_eff ∧ rotation × scan间隔 ≤ hard_cap** (双条件 — 代际臂与墙钟臂各自可独立击穿豁免; v8 只写了前者, 60 腿单 host + 日更 scan 时 8d > 7d 恒红于墙钟臂)。`k_eff = min(K_CAP=8, max(k_min=3, observed_rotation))`; 🔴 **observed_rotation 分母 = per-host** (8C-3): `= max over hosts ⌈该host腿数 / max(1, 该host上轮实际覆盖数)⌉` — 逐 host 记录, 全局单标量在异速双 host (本仓 7s vs 3.5s) 下会算出偏小 rotation ⇒ 恒红; **冷启动/rotation 记录缺失 ⇒ k_eff = k_min (偏红, fail-CLOSED)** (8C-3 附)。**rotation > K_CAP ⇒ 显式接受滚动红** + advisory; 墙钟臂击穿 (低频 scan) ⇒ 同样滚动红 + advisory (边界外行为均有定义)。🆕 v10 两声明 (R9-m1/m4): (1) k_eff 为**全局单值** (取最慢 host rotation) — 快 host 腿获等宽豁免是有意取舍: stale_unverified 结构性不作证 ⇒ 宽 X 只延迟红非假绿; (2) 「不恒红」是稳态命题 — in-flight/覆盖波动可致单 scan 瞬红后自愈, 瞬态可接受。冷启动/长闲置时诚实报 false (**正确**)。

  **覆盖率缺口另立 advisory-only 信号** (**不进裁决层**): `remote_refresh.skipped_count` + `skipped_remotes[]`。输出区块提示「本次有 N 条 remote 未刷新 (预算 15s 用尽) —— 调大 `refresh_deadline_seconds` 或收窄 `enforced_remotes`」。
  > ⚠️ **被砍的 leg 不自动豁免也不自动阻断** —— 裁决权交回三档全分割 (v10 D20): E ⇒ **照常作证** (被砍 ≠ 失去证据资格); ¬E∧X ⇒ `stale_unverified` 可见不作证不阻断; ¬E∧¬X ⇒ blocking (诚实)。**AC-15 验此点 (含防饥饿)。**
- **非交互契约**: `_common._run` (L344-366) 有 `capture_output=True` 但**无 `stdin=DEVNULL`**, env **只有 `LC_ALL`**。fetch 路径必须 `stdin=DEVNULL` + `GIT_TERMINAL_PROMPT=0` + `GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=N"`; auth 失败**只提示一次**。
- snapshot 记 per-remote `{fetched_at, fetch_ok, error_kind}`。**`error_kind` 是枚举** (复用姊妹 Spec 的分类器), **永不含 stderr 原文**。
- **`fetched_at` 只在 Fetch 1 真成功刷新时推进** —— stale-serve/degraded 路径 (`coordination_fetch.py:379-390` 现返回 `cached:True` + **任意陈旧**的 `last_fetch_at`) **不得**推进它。
- **TTL 命中时逐 remote replay** per-remote map (现 cache schema 只有 3 个标量键, 无 per-remote 结构 — R3-M10)。

### F1′ — 两个正交轴 (v4 关键修正, R3-M9)

> **v3 把「可达性」与「新鲜度」挤在一条路径上。** 后果: github token 刚过期, 但 200s 前上次 fetch 成功过 ⇒ `200s < 300s window` ⇒ 判「可信」⇒ 不降级 ⇒ **不记 reason** ⇒ `has_unreachable_remote=false` ⇒ 不可达告警**不响**。凭据坏了 5 分钟, snapshot 一声不吭。

**两轴各自成信号, 不互相 gate**:

| 轴 | v6 定义 | 作用 |
|----|---------|------|
| **可达性** | `has_unreachable_remote(r) := fetch_ok(r) == false` (**三态**: `true`/`false`/`not_attempted`; 后者 ≠ `false`) | 「**试了 → 失败**」⇒ **永远**置位 + 记 `error_kind`。**与窗口无关, 也与 `error_kind` 的取值无关** (零枚举 ⇒ 无补集可漏)。 |
| **新鲜度** | 🔍 **v8 (D15′) 拆双角色谓词**: `证据资格(r) := fetched_at(r) ≠ null ∧ (now − fetched_at(r)) ≤ evidence_window (默认 1h, 键 sync_freshness.evidence_window_seconds)` — 供 **∃ 正证据子句**; `豁免资格(r) := fetched_at(r) ≠ null ∧ generation_age(r) ≤ k_eff ∧ (now − fetched_at(r)) ≤ hard_cap (默认 7d, 键 sync_freshness.hard_cap_days)` — 供 **equal 降级判定**。equal 按三档全分割处置 (v10 D20): E ⇒ 作证; ¬E∧X ⇒ `stale_unverified` (不供 ∃ / 不阻断 / **必须可见**); ¬E∧¬X ⇒ `not_refreshed` (blocking); 连续 unverified ≥ k_eff 代 ⇒ 升级 blocking (D18)。**豁免 conjunct 细节 SOT=F4′ v9** (R9-m4)。旧单谓词 `可信(r)` (300s wall-clock) **退役** — 单谓词承担两角色是 R7 三 Critical 的共同根 | 新鲜度轴按角色分裂 gate: ∃ 用证据资格, 降级用豁免资格。 |

🔴 **v6 修正 1 — `has_unreachable_remote` 必须 fail-CLOSED, 不得写成「按 network 类」的正向枚举** (R5-C-B, **同一不变量的第六次复发**):

v5 写的是「`fetch_ok == false` ⇒ **按 network 类**置 `has_unreachable_remote`」。**「按 network 类」= 正向枚举 ⇒ 未列举值 fail-OPEN。**

**owner 用生产分类器 (`coordination_fetch.py:235` `_classify_error`) 跑真实 stderr 实测**:

| 真实失败模式 | `error_kind` | 落 network 类? |
|---|---|---|
| HTTPS 连不上 (`Failed to connect to ... port 443`) | `other` | 🔴 **否 → fail-OPEN** |
| HTTPS TLS 握手失败 (`gnutls_handshake() failed`) | `other` | 🔴 **否 → fail-OPEN** |
| **SSH 公钥被拒** (`Permission denied (publickey)`) | `other` | 🔴 **否 → fail-OPEN** |
| SSH 连接超时 | `network` | ✅ 是 |
| DNS 解析失败 | `network` | ✅ 是 |

**5 种真实故障, 3 种落 catch-all。** (backend-architect 独立复现第 4 种: `The TLS connection was non-properly terminated` —— `network_signals` 有 `"ssl"` 但**没有 `"tls"`**。)

**加重情节**: **auth 被拒也落 `other`** —— 而 **AC-13 正是要测「auth 失败 ⇒ `has_unreachable_remote` 必须 true」**。按 v5 的「按 network 类」措辞, **AC-13 自己测不出来**。

**后果链** (全部在 v5 文本内可推):
1. github 真连不上 ⇒ `fetch_ok=false`, `error_kind=other`
2. `other ∉ network 类` ⇒ **`has_unreachable_remote` 不置位** (fail-OPEN)
3. 上次成功 fetch 在 200s 前 ⇒ `可信=true` ⇒ **不降级** ⇒ `parity` 保持 `equal` ⇒ **还给 ∃-子句提供正证据**
4. ⇒ snapshot 报「已同步 + 无不可达 remote」, 而那个 remote **硬 down**

**这逐字就是 R3-M9 的失败模式** (「凭据坏了 5 分钟, snapshot 一声不吭」) —— **F1′ 两轴拆分就是为杀它而生的, 结果在自己的轴上留了同一个洞。**

**v6 修法** (**三态使枚举彻底消失** —— 这比补集定义更彻底):
```
has_unreachable_remote(r) := fetch_ok(r) == false          # 「试了 → 失败」= 不可达, 与 error_kind 无关
                                                           # fetch_ok 三态: true / false / not_attempted
                                                           # not_attempted (deadline 砍掉) ≠ false ⇒ 不置位
```
⇒ **零枚举 ⇒ 无补集可漏。** 任何 catch-all / 未来新增的 `error_kind` 都会置位 (**最彻底的 fail-CLOSED**: 它根本不看 `error_kind`)。
⇒ 「我们自己没试」由**第三态** `not_attempted` 承载, 而**不是**靠在枚举里开一个豁免口子 —— **豁免口子正是 fail-OPEN 的温床**。**AC-14 验此点。**

🔴 **v6 修正 2 — `可信(r)` 必须显式兜住 `fetched_at = null`** (R5-M-1, **第七次复发**):

v5 写的是 `可信(r) := now - fetched_at <= freshness_window`, **全文未定义 `fetched_at` 为 null 时取值** (从未成功 fetch 过)。

这与本 Spec **自己**在 §核心洞察 列的**违反形态 #3** (「**从未获取过的证据** 当正证据 (`age is None` → 判「不陈旧」)」) **完全同形** —— 也正是 `multi_remote.py:497` 今天的 bug (`if age is not None and age > warn` ⇒ **`None` 判「不陈旧」**)。

> AC-6 兜住了**行为** (子模块从未 fetch ⇒ 不得提供 equal 正证据), **但谓词定义没兜**。
> 按本 Spec 自己的元教训: **「把一个不变量写进文档」≠「把它写进兜底默认值」。**

~~**v6 定义**: `可信(r) := fetched_at(r) ≠ null ∧ (now − fetched_at(r)) ≤ freshness_window`~~
🔴 **v8 SUPERSEDED (D15′)**: 单谓词 `可信` 已退役, 新鲜度轴 = `证据资格` (∃ 侧, 1h) + `豁免资格` (降级侧, k_eff+7d) — **SOT = F4′ v8 公式块**。下表读法 (v10 D20): 降级仅发生于 **¬E∧¬X** (E 优先 — E∧¬X 照常作证, SOT=F4′ v9); 「照常提供证据」的资格 = 证据资格:

**降级只作用于正证据**:

| 原 parity | ¬E∧¬X 时 (v10) | 理由 |
|-----------|---------|------|
| `equal` | → `unknown` + `reason: not_refreshed` | 陈旧数据算出的「相等」不可信 |
| `behind` / `diverged` | **原样保留** | 陈旧 ref 报的落后是**下界** —— 真实只会更落后 |
| `ahead` | **原样保留** | 同理; 且降级会**杀死 `has_pending_push`** (`multi_remote.py:270-277` QA-I1 注释明写警告过) |

`reason` 优先级: **后置降级只在 parity 本会是 `equal` 时改写** —— 不覆盖 `detached_head` / `shallow_clone` / `no_local_tracking_ref`。

### F4′ — `overall_parity` 裁决表 (v4 核心修正; R3 两个 Critical 的合并解)

> **v3 的 `∀ r: 可信 ∧ parity ∈ {equal, ahead}` 两端都错**:
> - **太严** (R3-C5): `detached_head` ⇒ `parity: unknown` ⇒ `∉ {equal, ahead}` ⇒ 阻断。而 **detached HEAD 是每个子模块的规范常态** (`git submodule update --init --recursive` 会把**全部**子模块置于 detached HEAD) ⇒ **`overall_parity` 在 Aria 自己的仓库上恒 false**, 每个新采用者**第一天就恒红**。`no_local_tracking_ref` (未推送的 feature 分支 = **整个 Phase B**) 同理。
> - **太松** (R3-N1): **Python `all([]) == True`** ⇒ 空参与集 ⇒ **vacuous true** ⇒ **复活 QA-C1 假绿**。而这正是本 Spec 自己点名批评的 `check_parity.sh:383` `jq 'all(...)'` bug —— **v3 会把它从 shell 抄进 Python**。

**`unknown` 必须二分** (这是「类修」, 不是给某个值开豁免):

**代码里 `reason` 的完整枚举 = 10 个** (grep `multi_remote.py` 全部赋值点, **逐格填**, 不留空格):

| 类别 | `reason` (代码行) | fetch 能改变吗? | 语义 | 阻断? |
|------|-------------------|----------------|------|-------|
| **blocking unknown** | `not_refreshed` (新增) / `network_timeout` (L260,266) / `auth_failed` (L262) / `not_found` (L264) / `rev_list_failed` (L198) / `rev_list_parse_failed` (L202,207) / **`parse_error` (L281)** / 🆕 **`no_remote_head_ref`** (F10′ 新增) | **能** (或: 是真错误) | 「我们**不知道**真相, 而这是可以知道的」 | **是** |
| **benign ①** (fetch-**无关**, 恒 benign, **不看新鲜度谓词**) | `detached_head` (L169,188,250,293)¹ / `shallow_clone` (L173,289) / 🆕 **`remote_branch_missing`** (L276, **v6 从 ② 移入**) | **不能** (fetch 一万次也变不成 equal) | 「这个问题**不适用**」 | **否** (但也不提供正证据) |

> 🔴 **`deadline_skipped` 不在任何 benign 桶里** (v6 起草时一度写入 ①, **owner 自查推翻** —— 见 F3′)。它**不是一个 `reason` 值**, 而是 `fetch_ok` 的**第三态** (`not_attempted`); 其 parity 裁决**完全由双角色谓词承担** (v9: E/X 三档全分割, 见 F4′)。
> **判据**: benign = 「fetch **不能**改变它」; 而「我们没去问」**fetch 完全能改变** ⇒ 它属于「**我们不知道真相, 而这是可以知道的**」⇒ 若 `fetched_at` 过期则**照常 blocking**。
> **归 benign 会制造假绿** (大仓: origin 快腿提供 ∃ 证据 + github 被砍判 benign ⇒ `overall_parity: true`, 而 github 可能真领先 100 commit) —— **本 Spec 要杀的 bug 经由新机制复活 = 第八次复发。**
| **benign ②** (fetch-**依赖**, 须 `∧ 证据资格(r)` [v8]) | `no_local_tracking_ref` (L181) | **能** —— 「没这个 ref」可能只是「我们没 fetch 过」 | 「分支未发布」(经 `has_unpublished_branch`) | **否** (仅当 `证据资格`) |

> ¹ **F10′ 之后 `detached_head` 在默认路径 (`local_refs`) 上不再产生 `unknown`** —— 它改走 commit-based 比较, 产出真 parity。此处保留它在 ① 桶, 是为 `ls_remote` 路径 (L250/L293) 与 shallow 交叉场景兜底。

🔴 **v6 修正 — `remote_branch_missing` 从 ② 移入 ①** (R5-M-2, backend-architect 代码实测):

```python
# :253  _remote_parity_ls_remote —— remote_branch_missing 的产地
rc, out, err = _run(["git","ls-remote","--heads",remote,branch], ...)   # ← 实时网络往返
...
if not first:                                                            # rc==0 但输出为空
    base["reason"] = "remote_branch_missing"                             # :276

# :181  _remote_parity_local_refs —— no_local_tracking_ref 的产地
rc, out, _ = _run(["git","rev-parse", ref], ...)   # ← 读本地缓存的 tracking ref
if rc != 0:
    base["reason"] = "no_local_tracking_ref"        # :181
```

**两种结构不同的失败**:
- `no_local_tracking_ref` = 「读一个**可能陈旧**的本地缓存, 失败了 —— 不知道是『真没发布』还是『我们没 fetch 过』」⇒ **需要 `证据资格(r)` 去区分** (v8) ⇒ ② 桶 ✅
- `remote_branch_missing` = 「这一秒钟**真打了一发网络请求**, 对方**权威地**回答『没有』」⇒ **新鲜度内建在自己的调用里**, 与 Phase 0.5 `remote_refresh` 是否碰巧成功**毫无关系** ⇒ ① 桶

**v5 把它塞进依赖 `可信(r)` 的 ② 桶的后果**: `可信(r)` 挂在**另一个独立 collector** (`remote_refresh`, Phase 0.5) 的 `fetched_at` 上, 而 `_remote_parity_ls_remote` 是 Phase 1.12 内**自己发起**的独立调用 —— **拿不到那个 `fetched_at`** ⇒ `可信` 恒 false ⇒ `remote_branch_missing` **永远落 blocking** ⇒ 「一个刚被权威确认的『分支从未发布』的健康状态」被判成阻断 ⇒ **又一次自造恒红**。

> ⚠️ **`parse_error` 是本 Spec 起草时第四次「漏格」的实例** —— v4 初稿的两个桶里都没有它 (owner 自查 grep 时发现)。这再次印证 R3-C5 的方法论: **不能凭印象列举, 必须 grep 出全集逐格填。** 任何新增 `reason` 枚举**必须**同时归入某个桶 (加一条机械检查: 断言 `blocking ∪ benign == 代码中所有 reason 赋值`)。
>
> 附带发现: `state-snapshot-schema.md:499` 的 enum 列表**漏了 `rev_list_failed` / `rev_list_parse_failed`** (schema doc 与代码已 drift)。

**v8 公式** (D15′ 双谓词落位; v5 的 ∀/∃ 结构**不变**; v6 的 benign 分桶保留):
```
证据资格(r) := fetched_at(r) ≠ null                                # 🆕 v8 D15′: ∃ 侧 — 世界时间新鲜
              ∧ 0 ≤ (now − fetched_at(r)) ≤ evidence_window        #    默认 1h (创始事故 14h ≫ 1h)
                                                                   # 🆕 v10 (R9-M3): 负墙钟龄 (时钟回拨/NTP 跳变)
                                                                   #   ⇒ 视同 null ⇒ ¬E 且 ¬X (fail-CLOSED, 与负代龄
                                                                   #   钳位同构 — 回拨可使 14h 前真 fetch 呈现假 E)

豁免资格(r) := fetched_at(r) ≠ null                                # 🆕 v8 D15′: 降级侧 — 注意力节律新鲜
              ∧ generation_age(r) ≤ k_eff                          #    k_eff 见 F3′ 收敛不等式
              ∧ (now − fetched_at(r)) ≤ hard_cap (默认 7d)
              ∧ consecutive_unverified(r) < k_eff                  # 🆕 D18: 连续 unverified ≥ k_eff 代 ⇒ 豁免失效

# equal 的三档处置 (D15′ 核心; v9 D20 改全分割 — 守卫两两互斥, 并集全覆盖, 无 E∧¬X 重叠格):
#   E  (证据资格)         ⇒ equal 供 ∃ 正证据 (evidence_grade = "fresh")
#   ¬E ∧ X (豁免资格)     ⇒ stale_unverified — 不供 ∃ / 不阻断 / 必须渲染 (evidence_grade = "stale_unverified")
#   ¬E ∧ ¬X               ⇒ equal 降级 not_refreshed ⇒ blocking (诚实)
# 🔴 载体钉死 (v9, 8C-2): 三档落 per-remote 独立字段 evidence_grade ∈ {fresh, stale_unverified,
#   expired} — parity 保持 equal 不改写为 unknown, stale_unverified **不进 parity.reason**
#   (进 reason 会被 blocking_unknown 补集自动判 blocking, 三档塌两档 — 与 gitlink_integrity
#   不进 reason 的 13.4 决策同构)。expired 档的 not_refreshed 降级仍走 F1′ 既有路径。
# D18 求值先序 (v9 D20 附带): 本 scan 该 leg fetch 成功 ⇒ consecutive_unverified 先清零,
#   再评 X — 恢复腿不落旧计数器阴影。

benign_unknown(r) := parity(r) == "unknown" ∧ (
        reason(r) ∈ {detached_head, shallow_clone,                # ① fetch-无关 ⇒ 恒 benign, 不看新鲜度
                     remote_branch_missing}                       #    (ls-remote 实时权威回答)
     ∨ (reason(r) == "no_local_tracking_ref" ∧ 证据资格(r))       # ② fetch-依赖 ⇒ 断言「没发布」需世界时间新鲜
   )
   # 🔴 deadline_skipped 不在此 —— 「没去问」≠「不适用」; 它由双谓词裁决 (见 F3′)

blocking_unknown(r) := parity(r) == "unknown" ∧ ¬benign_unknown(r)   # 🔴 fail-CLOSED 兜底 (v5 已正确, 保留)

has_unreachable_remote(r) := fetch_ok(r) == false                    # 三态使枚举白名单多余 (v6, 保留)

has_unpublished_branch(r) := parity(r) == "unknown"
                             ∧ reason(r) == "no_local_tracking_ref"
                             ∧ 证据资格(r)                            # 断言「真的没发布」需世界时间新鲜

overall_parity = true  iff
      enforced_set ≠ ∅                                              # 非空 (防 vacuous true; 见 F5′ 的 [] 语义)
   ∧  (∃ r ∈ enforced: 证据资格(r) ∧ parity(r) == "equal")          # 🆕 v8: ∃ 侧用证据资格 (陈旧 equal 不再替全仓作证)
   ∧  (∀ R ∈ enforced: ¬gitlink_blocking(R))                        # 🆕 v9 (8M-4): gitlink 层接线 — gitlink_blocking(R) :=
                                                                    #   ∃(R,S): gitlink_integrity.status == orphaned
                                                                    #   ∨ (orphan_unverified ∧ consecutive ≥ k_eff) (D18); 定义见 tasks 13.4
   ∧  (∀ r ∈ enforced: parity(r) ∉ {behind, diverged}
                        ∧ ¬blocking_unknown(r))                     # ⚠️ ∀ 里不再有独立的新鲜度谓词项 (v8 同理适用双谓词)
```

> **v6 的 4 处 diff (相对 v5)**, 每一处都是**同一个病的不同宿主** —— 「定义域不完整 / 正向枚举 ⇒ 补集 fail-OPEN」:
> 1. `可信` 补 `fetched_at ≠ null` (第七次复发)
> 2. `has_unreachable_remote` 从正向枚举改补集定义 (**第六次复发**)
> 3. `remote_branch_missing` 从 ② 移 ① (分桶错 ⇒ 恒红)
> 4. deadline 砍掉的 leg ⇒ `fetch_ok = not_attempted` (三态), **裁决权交回双角色谓词 (v8)** + 按 `fetched_at` 升序排队防饥饿
>    (v5 无条件标 `not_refreshed` ⇒ 大仓恒红; 而「归 benign」⇒ **假绿** —— **两端都是错的**, 见 F3′)
>
> **∀/∃ 三子句结构本身在 R5 五方核验下无一人提出异议** —— 轴是对的, 不需第六次换轴。

> **为什么新鲜度谓词必须从 ∀ 子句里删掉** (qa-engineer R4 实证, 原谓词 可信(r), v8 后同理适用双谓词): 它在那里**冗余且有害** ——
> - 对本来 `equal` 的 r: 不可信时 **F1′ 的降级已经**把它变成 `unknown` + `not_refreshed` (∈ blocking) ⇒ `¬blocking_unknown(r)` **已经**挡住了, 不需要再挡一次;
> - 对 `behind`/`diverged` 的 r: 降级明确**不覆盖**它们 (下界证据依然为真); **`ahead` 的保留理据 (v8 按 hunter m-2 改写)**: 下界逻辑**不可迁移**到 ahead — 陈旧 ahead 可掩蔽真 diverged (sister 已推进远端), ahead 保留的真理由是 **has_pending_push 保活** (QA-I1: 压掉它会杀死未推送提醒); 掩蔽窗口 = **已知接受项** (¬豁免时该 leg 另有 has_unreachable/stale 可见信号兜底, overall 不因它为 true — ∃ 侧要求证据资格), 显式声明防未来审计员按「陈旧证据」判复发;
> - 对 `benign_unknown` 的 r: 它们的可信度**与是否阻断无关** —— 但字面公式仍要求 `可信`, 于是**只要该 remote 恰好这次 fetch 失败** (网络抖动 / per-host 丢连 / deadline 砍), `overall_parity` 就被拖成 false。**这又是恒红。**
>
> 「可信」的过滤作用**已经被 F1′ 的降级步骤下沉进 `parity`/`reason` 里了**。在 ∀ 里重复它, 只会误伤那些「降级规则明确不该碰」的 remote。

> 🔴 **`blocking_unknown` 必须写成 `¬benign_unknown` 的兜底 (fail-CLOSED), 不能写成正向枚举** (R4 **四方独立收敛**: tech-lead C6 / code-reviewer X-2 / knowledge-manager R4-C1 / backend-architect):
> v4 初稿把它写成 `reason ∈ {6 个显式值}` ⇒ **任何未列举的值 fail-OPEN (不阻断)**。实测可达的漏网之鱼:
> - **`reason = None` + `parity = unknown`**: `multi_remote.py:308/312/317` **三条 best-effort 返回路径**
> - **`parse_error`** (`:281`)
> - **姊妹 Spec B 的分类器兜底值 `unknown` / `git_error` / `permission_denied` / `timeout`** —— backend-architect 用**真实 `git fetch` 连接失败**复现: 其 stderr (`Failed to connect to ... Couldn't connect to server`) **一个已知分类 pattern 都没中** ⇒ 落进 catch-all ⇒ 按正向枚举**不阻断**。
>
> **这是同一个不变量的第五次复发** (QA-C1 只修 no-data / v3 只豁免 ahead / v4 漏 parse_error / v4 漏 reason=None / v4 枚举方向 fail-open)。
> **元教训: 「把一个不变量写进文档」≠「把它写进兜底默认值」。没有为「集合的补集」定义行为, 就是给了它一个隐式的、通常是错的默认。**
- `ahead` **不阻断**, 继续经 `has_pending_push` **单独承载** —— 这是对 `multi_remote.py:400-402` 既有决策的**保留** (三处独立证据一致: 代码注释 / golden fixture `main github->ahead` 且 `overall_parity: True` / **AB rubric `ab-suite/state-scanner.json:143`**)。
- **「分支从未推到任何 remote」不压在 `overall_parity` 上** —— 它有自己的 flag **`has_unpublished_branch`** (**v6 首次给出谓词定义**, 见上方公式; v5 引用它 4 次却从未定义它何时置位 / 是 per-remote 还是 repo 级 —— **这是 v6 谓词横扫抓出的、前五轮无人发现的缺口**), 由 `multi_remote_drift` 单独处理。**把三种语义挤进一个 bool 正是它今天撒谎的原因。**
- read-only remote **不参与** `overall_parity`。

### F5′ — enforced remote 集合

- **消费既有键**, 不发明新键: `enforced_remotes` / `read_only_remotes`。
- 🔴 **`enforced_remotes: []` 的语义必须写死 = 「自动发现全部 remote」** (v6 新增, R5-m-2):
  跨 skill 契约 (`phase-c-integrator/SKILL.md:574`, **已发布**) 原文: 「skill 级为 null 时继承顶层 `multi_remote.enforced_remotes`, **空则自动发现所有 remote**」。而 `DEFAULTS.json:9` 顶层**就是 `[]`**。
  ⇒ 若 Phase B 实现者**直读 `[]` 当空集** ⇒ `enforced_set = ∅` ⇒ 撞上 AC-12 的**非空护栏** ⇒ 🔴 **所有默认采用者 `overall_parity` 恒 false**。
  ⇒ **`enforced_set` 的计算必须是**: `enforced_remotes` 非空则取之 **∩ 该仓实际存在的 remote 集合** (🆕 v8 RM-3: 显式配置对「没有该 remote 的仓」不制造幽灵 leg — 差集记 `no_matching_remote` 可见, 不产生恒 fetch 失败腿); **为 `[]` 或 null ⇒ 自动发现该仓全部 remote** (再减去 `read_only_remotes`)。**AC-12 的非空护栏针对的是「自动发现后仍为空」(零 remote 的仓库 / 全部 read-only), 不是「配置写了 `[]`」。**
- 🔴 **命名空间必须对齐已发布的跨 skill 契约** (R3-M2): `phase-c-integrator/SKILL.md:574` 已把**顶层 `multi_remote.*`** 当公共契约 (skill 级为 null 时继承顶层)。state-scanner **不得另立门户** —— 否则「state-scanner 认定该强制的 remote 集合」≠「phase-c-integrator 认定该强制推送的 remote 集合」= **本 Spec 的病在跨 skill 层复现**。
- **read-only 排除必须同时作用于** `overall_parity` **和** `has_unreachable_remote` **和** `multi_remote_drift` 触发 (R3, backend-architect) —— 只挂 `overall_parity` 会让「我不关心它」的 remote 抖一下网络仍全局告警。
- **删除 `fetch_all: false` 旋钮** (R3, backend-architect): `enforced_remotes: ["origin"]` 已能达到同样效果。**不要为收窄 fetch 范围发明第 4 个键** —— 本 Spec 存在的理由之一正是「死配置键 + 假文档」, 别用一次修复换一次同类 drift。
- **修假文档** `sync-detection.md:515`。
- **Impact**: 已按该文档设过 `enforced_remotes` 的采用者, 其配置**今天是惰性的**; 本 Spec 让它承重 ⇒ **直接改变其网络行为**。CHANGELOG 必须显著标注。

### F2′ — 退役 FETCH_HEAD-mtime **实现** (保留新鲜度**概念**)

mtime 路径整体退役 (repo 全局单值, 当 fallback 都不合格); 新鲜度由 `fetched_at` + **双角色谓词** (证据资格 evidence_window / 豁免资格 k_eff+hard_cap, v8 D15′) 承载 — 旧键 `freshness_window` 一并入清扫清单。**无条件清扫** ≥8 处 SOT (⚠️ v2 曾把条件写反成「若保留才清扫」—— **退役意味着它变死配置键, 清扫更必须**)。

> ⚠️ 这推翻了 owner v1 的「24→1」决策 (其前提被 R1 证伪: age 是 repo 级, age≈0 对**所有** remote 都不触发)。R2/R3 五位一致确认推翻成立。

### F6′ — collector 改名 + 可关闭性契约

`coordination_fetch` → **`remote_refresh`** (Phase 0.5)。SKILL.md **写死契约**: 「关闭它 ⇒ 所有 parity 变 unknown」—— 防后人以为它归 `coordination.*` 配置管 (本仓 `.aria/config.json` 里正有 `coordination.enabled: true`), 关掉 coordination 静默摧毁 parity 真值。

🔴 **v6 硬约束 — 旧实现 retire, 不并行运行** (R5-M-6, backend-architect):

OQ-B 说「保留原 `coordination_fetch` 块 origin-only 原样, 另开 `remote_refresh` 新块」—— 这句话只锁死了 **snapshot key 的 shape**, **没锁死背后的实现**。两种读法:

| 读法 | 后果 |
|------|------|
| **(a) 退役旧实现 + shim** ✅ | `remote_refresh` 统一 N-remote 并行 fetch; origin 那条腿的结果经 **backward-compat shim** 重新打包成旧 `coordination_fetch` 的 10 个标量字段。**每个 (repo,remote) 每次 scan 只有一次真实网络往返。** |
| **(b) 旧代码原样继续跑 + 新代码并行** 🔴 | origin 每次 scan 被 fetch **两次**; 且**两套独立 TTL 缓存** (旧: `.aria/cache/coordination-fetch.json` 30s; 新: per-remote TTL) 对同一 origin 的 `fetched_at`/成功与否**可能给出不同答案** ⇒ **在 `coordination_fetch` 块与 `remote_refresh` 块之间, 重新生产本 Spec 想消灭的「同一 snapshot 自相矛盾」**; 且违背 F3′「网络成本必须有硬上界」的初衷 |

> prose 更容易被读成「别碰旧代码, 只加新代码」(读法 b), 而 OQ-B 给的理由 —— 「就地改基数会破坏两个下游契约」—— **只论证了不能改 shape, 没论证不能改实现**。tasks 3.2 列的「≥11 引用点需处理」**隐含的是读法 (a)** (否则 `track_board.py` / `normalize_snapshot.py` 根本不用动), 但正文从未明说。

**⇒ 写死 (v7 按 R6-M-7 精化)**: 「`coordination_fetch` 的 snapshot key 通过 backward-compat shim 从 `remote_refresh` 统一 fetch 结果的 origin 条目**派生**; 每个 (repo,remote) 每次 scan **branch-refs 层只有一次**真实网络往返; **旧的独立两段式实现 retire, 不并行运行**。⚠️ **#141 two-fetch 语义保留**: origin 的 `refs/aria/coordination` orphan-ref fetch (Fetch 2) 是**独立于 branch-refs (Fetch 1) 的第二次往返, 不合并** —— 合并会复活 #141 修掉的缺陷; 『一次往返』的量词只作用于 branch-refs 层 (3.3 的 fetch_ok 锚定 Fetch 1 与此一致)。」

**改名波及 ≥11 个引用点** (R3-N3): `normalize_snapshot.py` / `renderers/track_board.py` / `lib/coordination_ref.py` / `collectors/__init__.py` / `scan.py` / `tests/test_coordination_fetch.py` / `tests/test_p1_layer_h.py` / `SKILL.md` / `state-snapshot-schema.md` / `phase-1-collectors.md` / `docs/rule9-5layer-matrix.md`。

### F9′ — `sync.py` 平行计算点 (OQ-E)

`_collect_current_branch` 与 `submodules[].drift` 独立算 ahead/behind, 无 `fetch_ok` 概念 ⇒ 与 `multi_remote` **在同一 snapshot 自相矛盾**。

**两条路径必须在 Phase A 二选一** (R3, backend-architect: **这条路径的错误方向选择历史上就是数据丢失事故的成因**, `sync.py:312-328` 的 US-008 directional guard):
- **(a) 让它消费 per-remote 新鲜度** (不可信 ⇒ 标注/降级) ← 🆕 **v6 倾向** (R5-M-7)
- (b) 显式声明「本地视角、不保证新鲜」并在输出区块区分

> 🆕 **v6 补倾向 (a)** —— R5 指出: **OQ-E 是全文唯一一个连「倾向」都没给的 OQ** (OQ-A/B/C/D 都有), 而它**恰恰坐在 US-008 数据丢失护栏正上方**, 风险等级与「零倾向」不成比例, 且三轮过去原样未填。
>
> **理由**: (a) 让 `_collect_current_branch` / `submodules[].drift` 消费 F1′/F3′ **已经产出的同一份** per-remote 新鲜度信号 (`fetched_at` / 双角色谓词 [v8]), 而不是维持第二套独立的本地计算。
> - 与本 Spec 的核心哲学 (**「新鲜度靠获取, 不靠测量」**) 一致;
> - 让 **AC-10「不得自相矛盾」自动成立** —— 两个区块**共享同一个新鲜度来源**, 而不是靠人工交叉核对两套独立计算 (**「不得自相矛盾」是结果, 不是机制; 共享单一来源才是机制**)。

🔴 **v6 新增 — 第三个平行计算点: `verify_mode: "ls_remote"`** (R5-M-5, tech-lead):

三个 Spec 全文 grep `verify_mode` / `ls_remote` ⇒ **唯一命中是「ls_remote 方案删除」, 指的是被否掉的新方案, 不是既有的 `verify_mode` 配置键。**

但 `multi_remote.py:228-330` 的 `_remote_parity_ls_remote` **今天就存在**:
- 自己发**独立网络调用** (`git ls-remote`), 自己算 `reachable` + `reason` (`:258-266`)
- **10 个 reason 里有 6 个只在这条路径可达** (`network_timeout`/`auth_failed`/`not_found`/`remote_branch_missing`/`parse_error` + 三条 `reason=None` best-effort `:308/312/317`)
- **F3′ 落地后它会变成第三个独立的可达性计算点** (`remote_refresh.fetch_ok` / `ls_remote.reachable` / `sync.py` **各算各的**) + **双倍网络** (Phase 0.5 全量 fetch + 每 remote 再 ls-remote)

**这与 F9′ 识别出的结构缺陷同族。必须裁定** (🆕 **OQ-F**):
- **(a) 退役 `verify_mode: ls_remote`** (F3′ 的全量 fetch 已让它冗余) ← **倾向**
- (b) 保留但改由 `remote_refresh` 供数 (不再自发网络调用)
- (c) 保留且接受双算 —— **必须说明谁赢** (否则又是「同一 snapshot 自相矛盾」)

⚠️ **`submodules[].drift` 的 `hint` / `hint_type` 从陈旧变新鲜 ⇒ 直接改变 `git submodule update --remote` 建议的触发** —— **US-008 数据丢失护栏在此路径**。

---

## 下游消费者 (grep 实证)

| 消费者 | 性质 |
|--------|------|
| `multi_remote_drift` (`RECOMMENDATION_RULES.md:12` + `references/rules/basic-rules.md:69-82`) | **非阻塞** advisory, 75% 置信, **无去重/冷却** (grep 零命中) |
| `session-closer/handoff_autofill.py:52,54` | L52 **显式排除 `unknown`** ⇒ 会静默吞掉降级 = **新假绿通道** |
| **`aria-2.0-m7-fleet-aggregation` (Approved, 活的)** | 把 `overall_parity == false` 用作 **fleet 健康信号** ⇒ v2 的「唯一消费者」结论**在 skill 树内为真、全仓为假** |
| `phase-c-integrator` | **不消费** `overall_parity` (0 命中); 但**消费顶层 `multi_remote.enforced_remotes` 契约** (见 F5′) |
| golden fixture / **AB rubric `ab-suite/state-scanner.json:143`** | 都腌入了旧语义, 须同步 |

**`multi_remote_drift` 的建议必须按成因分派** (≥6 种, 非 3 种):

| 成因 | 建议 |
|------|------|
| `behind` / `diverged` | `git pull` / `submodule update --remote` |
| `ahead` | `git push` |
| `detached_head` / `shallow_clone` | **不该触发** (benign) |
| `no_local_tracking_ref` | 「分支未发布」—— 走 `has_unpublished_branch`, 不是 parity |
| `not_refreshed` / network / auth | **查网络/凭据 —— 不是 git 操作** |

> 「一律改 fetch/pull 导向」是**把 v1 的对称错误换方向再犯**。`sync.py:312-328` US-008 directional guard: 方向搞反会 `update --remote` **覆盖未推送的本地 commit**。

---

## Impact

| 维度 | 影响 |
|------|------|
| **网络行为** ⚠️ | fetch 1 个 → **所有 enforced remote** (并行, per-host 限流, **全局 deadline 15s**)。本机 +0.6s, **非通用承诺**。 |
| **配置从惰性变承重** ⚠️ | 已设 `enforced_remotes` 的采用者, 配置今天无效, 本 Spec 让它生效 ⇒ **直接改变网络行为**。 |
| **裁决语义** | 见 F4′ 裁决表。**benign unknown 不再阻断** (修 v3 的恒红); **空集/无正证据 ⇒ false** (修 v3 的 vacuous true)。 |
| **`git` block** | ahead/behind 由陈旧变新鲜 ⇒ 影响 `branch_behind_upstream` 规则 (阈值 `behind >= 5`) + golden fixture。 |
| **`sync_status.submodules[].drift`** | `hint`/`hint_type` 从陈旧变新鲜 ⇒ **US-008 数据丢失护栏在此路径**。 |
| **snapshot schema** | `multi_remote.remotes[]` 加 `{fetched_at, fetch_ok, error_kind}` = additive。**`coordination_fetch` 块是扁平单-remote 标量 (10 字段) ⇒ F3′ 使其基数改变 = 非 additive** ⇒ **OQ-B**。 |
| **回归** | 机械性破裂: `test_local_refs_stale_flag` / `test_scan_with_two_remotes_local_refs` / `test_full_main_repo_flow_with_config_overrides`。 |
| **离线** | 全 fetch 失败 ⇒ 全不可信 ⇒ `overall_parity: false`。**OQ-C** (debounce)。 |

---

## Verification — 可证伪锚点

> **调用命令**: `python3 aria/skills/state-scanner/tests/run_tests.py` (**不是 pytest** — 44 collection errors)。
>
> 🔴 **baseline 不是「0 failed」** (v6 修正, R5-C-E; **owner 连跑两次实测**):
> ```
> 未修改代码 (aria HEAD 0964496):
>   Run A: Ran 1006 tests ... FAILED (failures=1)
>   Run B: Ran 1006 tests ... FAILED (failures=1)
>   失败测试: test_two_consecutive_runs_diff_zero   ← baseline 就是红的
> ```
> **该测试跑的是真 scan 打真网络**, 两跑之间的网络/TTL/缓存状态本来就会变。跨 4 次观测 (code-reviewer 2 + owner 2) 暴露 **4 条互不相同的漂移通道**:
>
> | # | 漂移键 | 根因 | 谁认领 |
> |---|--------|------|--------|
> | 1 | `remote_refs_age` | `sync.py:396/405` 读 FETCH_HEAD mtime; **scan 自己的 Phase 1.16 会改写 FETCH_HEAD** | 本 Spec (tasks 8.4) |
> | 2 | `issue_status.repos[].source` | `issue_scan.py:822` cache 命中返 `"cache"` / live 返 `"live"` (900s TTL 在两跑间翻转) | 🆕 **本 Spec (tasks 12.10)** |
> | 3 | `coordination_fetch.degraded` / `degradation_reason` | 真实网络抖动 ⇒ 一跑降级一跑不降级 | 🆕 **本 Spec (tasks 12.10)** |
> | 4 | `errors[]` 数组 | 同上 soft error 时有时无 | 🆕 **本 Spec (tasks 12.10)** |
>
> **4 条都不在 `normalize_snapshot.py` 的 `TIMESTAMP_KEYS`/`DROP_KEYS` 名单里。**
> 📌 **仓内已有逐字先例**: `DROP_KEYS` 的 `cached`/`age_seconds`/`refs_fetched` 注释 (v1.30.2) **明写**「TTL-based, varies between consecutive runs… Stability test requires drop」—— **同一 class 已解过一次**。
>
> 🔬 **v7 CE 归因复验修正 (2026-07-14)**: 上表是 R5 时点的 4 条; CE 干净条件复验后**通道实数 6 条** — 补 (5) `custom_checks[issue-cache-freshness]` (**确是**通道, 条件=缓存缺失/mtime>30min; R5「无一是 custom_checks」只在新鲜热缓存条件下成立) + (6) 天数型 output 跨日界 (结构性潜伏)。⇒ Spec C 的归因**条件性正确**, 其修法可杀通道 #5 (仅此一条); 全清单与根治排序 (offline 旁路为主) 见 **tasks 12.10 (SOT)**, 本段不再复制。
> ⚠️ **Spec B 受害最重**: 它被指定「**应先落地**」, 却既不碰 `remote_refs_age` 也不碰 `source` 也不碰网络抖动 ⇒ **它的 AC-3 (0 failed) 在自己的 PR 上结构性恒红 ⇒ Spec B 按自己的闸门无法 ship。**
>
> **v6 判据** (三份 Spec 统一):
> **`0 failed`** ∧ **无既有绿测试转红** ∧ **新增测试数 = N** ∧ **baseline 既有的 1 红 (`test_two_consecutive_runs_diff_zero`) 由 <本 Spec / Spec B / Spec C> 中的哪一份消除, 必须显式声明**。
> ⇒ **本 Spec 认领全部漂移通道 (v7 修正: 6 条, SOT=tasks 12.10)** (tasks 8.4 + 12.10)。**Spec B / Spec C 的判据改为「0 failed **除** `test_two_consecutive_runs_diff_zero` (由母 Spec 消除, 见其 tasks 12.10)」** —— 否则它们无法独立 ship。

- **AC-1**: remote **¬E∧¬X** (v10 三档词汇) + 真实落后 → `parity != "equal"` 且 **`reason == "not_refreshed"`** (显式断言走过 F1′ 路径, 防死代码 ship)。
- **AC-2**: origin 刷新成功且 equal + github fetch 失败且真落后 → github `unknown` + **network 类 `reason`** + `overall_parity: false`。
  > **fixture 必须钉死**: github **无 `evidence_window` (1h) 内的成功 `fetched_at`** [v8] (否则不触发降级 ⇒ green/red by accident)。**用 mock `_run` 注入精确 stderr, 不打真实不可达域名** —— 实测 TLS 握手失败的 stderr 是 `gnutls_handshake() failed`, **不落在任何已知分类 pattern 里** ⇒ 真实网络构造会环境相关地误判。
- **AC-3 (性能预算)**: mock `_run` 断言 **每个 (repo, remote) 恰好被 fetch 一次** (集合/计数不变量, **不是 strict order** —— 真并行下调用序是线程调度决定的, 断言序会成为新 flaky 点)。wall-clock 仅作 **spike 记录, 不作 CI 硬 gate**。
- **AC-4 (无回归)**: 见上方判据。
- **AC-5 (snapshot 自洽)**: `tracks_multibranch` 中**与 HEAD 同分支** (`branch` == HEAD upstream) 的 track commit 对 HEAD 不可达时 ⇒ `overall_parity == false` 或该 remote `reason` 非空。(**不能用「任意 HEAD 不可达的 commit」** —— 任何有其它活跃分支的仓库本来就有 ⇒ 健康仓假红 + 误触设计闸。)
- **AC-6 (子模块覆盖)**: 子模块 remote 从未 fetch ⇒ **不得**提供 `equal` 正证据。
- **AC-7 (降级只作用于正证据)**: ¬E∧¬X且 `behind` **不得**降级为 `unknown`; ¬E∧¬X且 `ahead` **不得**让 `has_pending_push` 变 false。
- **AC-8 (`ahead` 不阻断, 但也不是正证据)** — **owner 裁定 2026-07-12 (DEC)**:
  🔴 **v6 措辞修正** (R5-m-1: **公式是对的, 但 v5 的一行理据不是公式的正确描述**):
  > v5 写的理据是「`overall_parity` 语义 = 本地与远端一致; 有未推送 commit 的仓库**确实不是已同步的** ⇒ 报 false 是诚实的」。
  > **但 v5 的断言又要求 `origin=equal + github=ahead` ⇒ `overall_parity: true`** —— 那个仓库**对 github 有未推送 commit**, 按上面的理据它应当 false。
  > ⇒ **理据与断言字面打架。** Phase B 实现者完全可能据此写出「任一 remote ahead ⇒ false」, **那会打掉 golden fixture 并让 AC-8 自己红**。

  **v6 的正确表述** (逐字对应 F4′ 公式, 不再用「已同步」这种会偷换概念的词):
  > **`overall_parity == true` 当且仅当: ≥1 个 enforced remote 提供了「**新鲜的 equal 证据**」(∃ 子句), 且**没有任何** enforced remote 处于 `behind` / `diverged` / `blocking_unknown` (∀ 子句)。**
  >
  > `ahead` 既**不阻断** (∀ 子句不排斥它) 也**不是正证据** (∃ 子句只认 `equal`) —— 它由 `has_pending_push` **单独承载**。
  > ⇒ 「一个仓库可以同时是 `overall_parity: true` 和 `has_pending_push: true`」**不是矛盾**, 而是「有 remote 证实我们不落后, 且我们还有东西没推」。

  **与现有代码 (`has_equal_evidence` 要求 `equal`) / golden fixture / AB rubric 三者一致 ⇒ blast radius 最小。**
  > ⚠️ **v4 的 AC-8 措辞把「健康」与「已同步」偷换了概念** (R4 tech-lead C7 / code-reviewer X-5 双方都指出它与 AC-12 **字面互斥**)。一个有未推送 commit 的仓库**是健康的, 但不是已同步的**。
  > **本 Spec 修的是「落后时假绿」** (危险: 会在旧代码上开工、重复别人的劳动 —— 本 session 即受害者), **不是「领先时假红」** (领先不会导致重复劳动)。两者不可混为一谈。
  >
  > **断言**: `origin=equal + github=ahead` 的仓库 (golden fixture 场景) ⇒ `overall_parity: true` ∧ `has_pending_push: true`。**前提: ≥1 个 remote 为 `证据资格 ∧ equal` [v9]。**
  > 单 remote 且 `ahead` ⇒ `overall_parity: false` (无正证据) + `has_pending_push: true` + 建议 `push` —— 见 **AC-12**, 二者现已**自洽, 不再互斥**。
  >
  > tech-lead 的反方论据 (「单 repo+单 remote+未推送 = 中位数采用者, 按『健康常态该是什么值』判据答案应是 true」) 记录在案 —— 若未来 Phase B dogfood 实测告警疲劳成立, 可重开此裁定。
- **AC-9 (TTL 不复发旧病)**: 30s 内连跑两次 scan ⇒ 第二次 TTL 命中 ⇒ **不降级** + 两次 snapshot diff == 0; **fetch 失败 + stale cache ⇒ `fetched_at` 不得推进**。
- **AC-10 (F9′ 平行计算点)**: origin fetch 失败时, `sync_status.current_branch` 与 `sync_status.multi_remote[origin]` **不得自相矛盾**。**断言字段由 OQ-E 的裁定决定** (不能停留在「不得自相矛盾」的 prose 谓词)。
- 🆕 **AC-11 (benign unknown 不阻断 —— 防 R3-C5 恒红回归)** — **v6 措辞更新 (F10′ 改变了它的机制)**:
  **detached-HEAD 子模块** + 全部 remote 刷新成功 + **子模块与其全部 remote 真的 equal** + 主仓 equal ⇒ `overall_parity` **仍为 true**。
  > ⚠️ **F10′ 之前**, 此 AC 通过是因为「`detached_head` ⇒ unknown ⇒ **恒 benign 不阻断**」(**子模块根本没参与判定**)。
  > **F10′ 之后**, 它通过是因为「子模块**真的**算出了 `equal`, 提供了正证据」。
  > **同一个 `true`, 完全不同的语义** —— 前者是「没看」, 后者是「看了, 确实一致」。**AC-16 验证「看了, 确实不一致」的那一格。**
- 🆕 **AC-11b (benign ① 类 remote 自身 fetch 失败仍不阻断)**: benign ① 类 (`detached_head` / `shallow_clone` / `remote_branch_missing`) 的 remote **自身 fetch 失败** ⇒ `overall_parity` **仍不受它阻断** (只要其它 remote 提供 `证据资格 ∧ equal` [v8])。
  > ⚠️ **deadline 砍掉的 leg 不在此列** —— 它**不是 benign**, 其裁决由三档全分割承担 (v10 D20: E ⇒ 作证 / ¬E∧X ⇒ stale_unverified / ¬E∧¬X ⇒ 阻断)。**见 AC-15(a′)(b)。** *(v5 只存在于 tasks 5.2b, v6 补进官方 AC 枚举 — R5-m-5)*
- 🆕 **AC-12 (无 vacuous true —— 防 R3-N1 假绿回归)**: 参与集为空 (零 remote / 全部 read-only) ⇒ `overall_parity` **必须 false**; 无任何 `证据资格 ∧ equal` 的 remote (如单 remote 且 `ahead`) ⇒ **必须 false** [v8]。
  > ⚠️ **前提**: `enforced_set` 已按 F5′ 的 `[]` 语义**自动发现全部 remote** 之后仍为空。**配置写 `[]` 不等于参与集为空** (否则默认采用者恒 false — R5-m-2)。
- 🆕 **AC-13 (可达性与新鲜度两轴独立 —— 防 R3-M9)**: remote 本次 fetch 失败 (auth) 但 `fetched_at` 仍在窗口内 ⇒ `parity` **不降级** (仍 equal), **但** `error_kind` **必须记录** 且 `has_unreachable_remote` **必须 true**。

### 🆕 v6 新增 AC (R5 的 5 个 Critical 各配一条可证伪锚点)

- 🆕 **AC-14 (`has_unreachable_remote` fail-CLOSED —— 防 R5-C-B 第六次复发)**:
  分类器返回 **catch-all 值** (`other` / `unknown` / `git_error`) 时, `has_unreachable_remote` **必须 true**。
  > **fixture 必须注入真实 stderr, 不得用合成字符串** —— 用 owner 实测的三条: `Failed to connect to <host> port 443` / `gnutls_handshake() failed` / `Permission denied (publickey)`。**这三条今天全部落 `other`。**
  > **对偶**: `fetch_ok == "not_attempted"` (deadline 砍掉) ⇒ `has_unreachable_remote` **必须 false** (**我们没试 ≠ 对方不可达**)。
  > ⚠️ **注意这不是枚举豁免** —— 是三态里的一个**独立状态**。`has_unreachable_remote` 根本不读 `error_kind`。

- 🆕 **AC-15 (deadline 三态 + 防饥饿 —— 防 R5-C-C 恒红 **和** v6 起草期差点引入的假绿)**:
  **(a) 稳态不恒红 (v9 D20 措辞)**: 60-leg fixture (**预算参数取 §承重实测: 8 腿/scan + host 拆分 30/30 钉死 [rotation=4]; scan 间隔亦钉死 [30min, 满足 rotation×间隔 ≤ hard_cap] — 两参数均不得反推**), 多数 leg 被 deadline 砍, **证据资格成立 (E)** ⇒ 作证 ⇒ `overall_parity` **不得** false。
  **(a″) 🆕 v9 稀疏节律 fixture (8M-10, k_eff 真执行)**: scan 间隔 > evidence_window (如 2h) 多轮跑 — 被砍腿走 ¬E∧X 档 (stale_unverified) ⇒ 豁免/k_eff/D18 计数路径**真被执行** (防 k_eff 未实现的代码在 (a) 上假绿); 轮转完成后腿恢复 E ⇒ 计数清零 (先序)。
  **(a‴) 🆕 v9 边界 fixture (8M-12, 批准参数)**: **72 腿单 host** 变体 ⇒ rotation=⌈72/8⌉=9 > K_CAP=8 ⇒ 期望滚动红 + advisory 指引 (行为有定义; 不得用压低覆盖数的方式构造)。
  **(a⁗) 🆕 v10 D20 核心格 fixture (R9-M4)**: **E∧¬X 腿** (fetched_at=50min [E] + generation_age > k_eff [¬X], cache 预置) ⇒ 断言 `evidence_grade == "fresh"` ∧ 作证 ∧ overall 不因它 false — 锁死 E 优先; 「¬X 一律 blocking」的 v8 式实现必 RED。
  **(b) 🔴 过期即诚实 (防假绿; v9 D20 全分割措辞)**: leg **¬E ∧ ¬X** (无证据资格 **且** 无豁免资格) ⇒ 其 `equal` **必须**降级 `not_refreshed` ⇒ **blocking** ⇒ `overall_parity` **必须 false**。🆕 **¬X 三分支各配单变量 fixture (8M-14)**: 代际>k_eff (须叠加 ¬E: 墙钟 >1h) / 墙钟>hard_cap (cache 预置 fetched_at=8d 前 + 代际 ≤k_eff — 无需时钟 seam) / null — 各自单独成立即 blocking, 防漏实现某臂的代码半绿。
  **(a′) stale_unverified 三断言配对 (v9 按 m-9 拆; v10 标号与 tasks 2.18(a′) 对齐)**: leg ¬E∧X ⇒ (i) **不作证**: 全腿 ¬E∧X ⇒ ∃ 空 ⇒ overall false; (ii) **不阻断**: 另加一条 E∧equal 腿 ⇒ overall **true** (配对 fixture, 缺它则 (i)(ii) 不可区分); (iii) **必须渲染** (evidence_grade 字段 + 输出区块 aging 列表, 落点 10.4)。
  > ⚠️ **即使其它 remote (如 origin) 提供了 `证据资格 ∧ equal` 正证据, (b) 仍必须 false** —— 「origin 说我们没落后」**不能**替 github 作证。**这一格就是 v6 起草时差点写成假绿的那一格。**
  **(c) 防饥饿 (v8 RM-7 carve-out)**: 连续 N 次 scan ⇒ **每条非退避 leg 都至少被刷新过一次** (fetch 优先级 = `fetched_at` 升序, `null` 最优先); 退避腿 (3.5d) 按 2^n 节律重试并在 `skipped_remotes[]` 标 `backoff`, 不计入本全称量词。
  > **若 fetch 顺序固定** ⇒ deadline 每次砍同一批靠后的 leg ⇒ 它们的 `fetched_at` 永远推不进 ⇒ **恒 blocking 且永不翻身** —— **这才是 C-C 的真正根因: 不是分桶, 是饥饿。**
  **(d) advisory**: `remote_refresh.skipped_count > 0` **必须**出现在输出区块 (**不进裁决层**)。

- 🆕 **AC-16 (F10″ 正向 —— 本 Spec 的存在理由; 防 R5-C-A; v7 按 D14 重述)** 🔴 **这是最重要的一条**:
  **主仓在 R 上已发布的 commit 引用的子模块 gitlink, 在该子模块的 R 上不可达** ⇒ `gitlink_orphaned(R) == true` ⇒ **blocking** ⇒ `overall_parity` **必须 false**, 且 `multi_remote_drift` 给出成因专属修复建议 (`git -C S push R <branch>`)。
  > **fixture = 2026-07-12 的活体事故态**: 主仓 github/master=`dfb3118` 引用 `standards@79b7cd6`, 而 standards 的 github 只到 `9df1722` (G 不可达) ⇒ `clone --recursive` from GitHub 断裂。
  > **自我否证**: 此测试在**未修改代码**上**必须 RED** (事故当天 scanner 报 `overall_parity: true`)。**意外 GREEN ⇒ 诊断有误, 回 Phase A。**
  > 🆕 **v8 补两个 fixture (R7)**: **(prune, RC-1)** 远端删支/force-push 后本地留化石 remote-tracking ref 仍 contains G — **无 --prune 时必须 RED** (化石 ref 制造假绿), 加 prune 后正确报警; **(rc=129, RC-5)** G 对象在 S 本地 odb 不存在 (`branch -r --contains` rc=129 "no such commit") ∧ S 的 R leg 豁免资格成立 ⇒ **必须判 orphaned** (未修改代码/按 fail-soft 直觉实现 ⇒ RED — 「gitlink 无处存在」不得比「只缺镜像」更绿)。
  > ⚠️ **完全不经 parity 表达** (F10′ 教训): 该场景手工 `rev-list` 算出的是 `ahead` (反事实 — 生产代码对 detached 子模块 leg 恒 unknown/detached_head, 不会真产出 ahead); fixture 断言 **parity 相关字段与未修改代码基线逐字相等**, 共验 AC-8 需另加主仓 ahead leg (见 tasks 2.15) —— AC-16 与 AC-8 在 F10″ 下正交, 不再互斥。

- 🆕 **AC-17 (F10″ 对偶 —— 防过冲成恒红; v7 按 D14 重述, 含反惯例 fixture)**:
  **(a) 健康常态必绿**: detached-HEAD 子模块 + 已发布 gitlink 在全部 enforced remote 上**可达** ⇒ `gitlink_orphaned == false` (∀R) ⇒ 不因 F10″ 阻断 — **CI fixture = 合成 bare-remote** (v10 同 tasks 2.16(a); 本仓 dogfood 环境依赖, 归 12.5 人工)。
  **(b) 开发期零误报**: 本地 HEAD 领先 (未发布的新 gitlink) ⇒ F10″ **只看已发布的 C**, 不报警。
  **(c1) 🔴 反惯例·正向 (R6-C-2 教训 + §3.4「本仓 dogfood 不是 authority」)**: 子模块默认分支**故意叫** `trunk` (非 master/main), `refs/remotes/R/HEAD` **不存在**, gitlink **orphaned** ⇒ **必须报警** — 锁死零分支名假设的故障侧。
  **(c2) 🔴 反惯例·对偶**: 同 trunk 环境, gitlink **可达** ⇒ **必须不报警** — 健康侧。(v8 按 qa m-2 拆成两个 checkbox, 防 #95 归档门只见一格)
  **(d) pin 住旧 commit 的子模块** (跨项目常态, R6-M-4): gitlink 陈旧但在 R 上 branch-**可达** ⇒ 不报警 (与「新不新」无关)。
  **(e) 🆕 v8 tag-only pin (RM-11)**: gitlink 仅 tag 可达 (分支已删) ⇒ **报警** — 钉死「可达 := branch-可达」的有意收窄 (逃生口见 F10″ v8 边界注)。
  **(f) 🆕 v8 跨腿代差 (RM-2)**: 主仓 R leg 本代刚 fetch (C 含新 gitlink), S 的 R leg 上代 fetch (豁免内但 gen(S,R) < gen(主仓,R)) ⇒ **不判 orphaned** (记 orphan_unverified) — S 的 refs 早于 G 被推上去的时刻, contains 空是时序假象非破损。
  > **判据**: 「该信号在健康常态下应该是什么值?」—— `submodule update --init` 后一切已发布且可达的仓库, 答案是**不阻断**。

**自我否证闸**: 红测试在未修改代码上意外 GREEN ⇒ 诊断有误, 回 Phase A。修复后红测试**仍无法转绿** ⇒ **设计缺陷, 回 Phase A** (v1 的 AC-2 正是这种情况)。

> 🔬 **v6 新增机械闸 (对偶验收)** —— R5 元教训 #3:
> **本 Spec 系列的每一次修复都在对偶方向过冲一次** (v2 `ahead` / v3 `detached_head` / Spec C cache-hit / **Spec C live-miss** / **deadline**)。根因同一: **只验算了要修的那一侧, 没问「修完之后, 另一侧在健康常态下是什么值?」**
> ⇒ **每条 AC 必须同时给出两个 fixture: 「健康常态必 PASS」+「真故障必 FAIL」。** (Spec C 的 AC-2「防恒绿真空」已是这个形状, 只是**没有对称地应用到 AC-3** —— 于是 AC-3 制造了新恒红。)
> ⇒ AC-14 / AC-15 / AC-16+AC-17 **均已成对给出**。

---

## Open Questions (Phase A 内锁死)

- **OQ-A** — `read_only_remotes` 默认值。**倾向 `[]` (不自动推断)**: git 没有可靠的「只读」内建信号 (push URL 缺省等于 fetch URL); **误标 read-only 会吞掉真实的落后信号**, 比要求显式配置更危险 (R3: qa + backend-architect + code-reviewer 三方一致)。**必须与 AC-12 的非空护栏捆绑裁定。**
- **OQ-B** — `coordination_fetch` snapshot 块 shape。**倾向: 保留原块 (origin-only) 原样, 另开 `remote_refresh` 新块**承载 per-remote 数组 —— 原块是 **#141 归档契约** + **m7-fleet-aggregation 防御式消费清单**双重锁定, 就地改基数会同时破坏两个下游契约; 新开键 = **纯 additive** ⇒ 不 bump schema version (R3: tech-lead + backend-architect + qa 三方一致)。
- **OQ-C** — 离线 debounce。**倾向: 不造新的有状态冷却机制**。用 F1′ 的两轴拆分: 离线 ⇒ `has_unreachable_remote=true` ⇒ 让 `multi_remote_drift` **在该 flag 为 true 时不触发**, 换成一条「离线, 同步状态不可知」的降级横幅 (复用 `coordination_fetch` 现有的 `degraded` 红条先例)。**debounce 只作用于建议层, 不作用于裁决层** (让 `overall_parity` 变回 true 会重新引入假绿)。
- **OQ-D (v8 按 D15′ 重述)** — 旧单键 `freshness_window` (300s) **退役** (F2′ 清扫清单 + 配置迁移注), 由双键取代: `sync_freshness.evidence_window_seconds` (默认 3600; 须 > TTL 30s 且 > scan 全程 17.6s) + `sync_freshness.hard_cap_days` (默认 7) + `sync_freshness.k_min` (默认 3; K_CAP=8 为常量)。**schema doc 写明新的有界承诺**: 「∃ 正证据的陈旧容忍 ≤1h (与创始事故 14h 量级相称); ¬blocking 豁免 ≤ min(k_eff 代, 7d) **且全程以 stale_unverified 可见** — 豁免不等于作证。与本 Spec 修复的**无界**陈旧 bug 是两个量级, 不要被未来审计员误认成同一缺陷复发」。
- 🆕 **OQ-E** — F9′ 二选一 ((a) 消费新鲜度 / (b) 声明本地视角)。**必须与 OQ-A~D 同等对待** —— 这条路径直接落在 **US-008 数据丢失护栏**上, 错误的方向选择历史上就是事故成因, **不得留给 Phase B 实现者临场挑最省事的分支**。AC-10 的断言字段跟着此裁定定死。
  🆕 **v6 补倾向: (a)** —— 消费 F1′/F3′ 已产出的同一份新鲜度信号。理由见 F9′ (与「新鲜度靠获取」一致 + 让 AC-10 **自动成立**而非靠人工核对)。*(R5-M-7: 它是全文唯一零倾向的 OQ, 三轮未填, 与其风险等级不成比例)*
- 🆕 **OQ-F** — `verify_mode: "ls_remote"` 路径的归宿 (R5-M-5)。**倾向 (a) 退役** —— F3′ 的全量 fetch 已让它冗余; 保留它 = **第三个独立的可达性计算点 + 双倍网络**。若保留, 必须裁定「谁赢」。
  > ⚠️ **注意其副作用**: `multi_remote.py` 的 **10 个 `reason` 里有 6 个只在 `ls_remote` 路径可达**。退役它 ⇒ F4′ 裁决表的一半格子在生产上不可达 (**无害** —— fail-CLOSED 兜底仍覆盖; 但 schema doc 的 enum 需标注)。
  > 🔴 **且它揭示 m-4**: 默认 `verify_mode=local_refs` 下 `reachable` **恒 True** (`:163/:182` 硬编码), L410 的 `has_unreachable` 触发集 (`network_timeout`/`auth_failed`/`not_found`) **只产自 ls_remote 路径** ⇒ **`has_unreachable_remote` 今天在生产默认模式下结构性恒 False**。⇒ tasks 4.1 必须**替换**该触发器为 `fetch_ok` 驱动, **而非叠加**。

---

## 关联

- **拆出的姊妹 Spec**: [snapshot-stderr-secret-leak](../2026-07-16-state-scanner-snapshot-stderr-secret-leak/proposal.md) (Rule #7, **应先落地**) / [issue-cache-freshness-assertion](../2026-07-16-state-scanner-issue-cache-freshness-assertion/proposal.md) (正交)
- **承重先例 (必读)**: `openspec/archive/2026-06-12-state-scanner-coordination-fetch-resilience` (**#141** — two-fetch 语义, `fetch_ok` 锚定依据) / `openspec/archive/2026-04-25-state-scanner-mechanical` (**AD-SSME-6** — `state-snapshot-schema.md` 才是 schema SOT; `multi_remote.py:4` 声称 git-remote-helper 是 canonical 的 docstring 是**被取代的 stale 声明**, **不得**据此把 SOT 迁回代码)
- **下游 Spec**: `aria-2.0-m7-fleet-aggregation` (Approved — 消费 `overall_parity`)
- **aria-plugin #109**: 同一失败模式的**协调层**维度; 本 Spec 是**扫描层**维度。R1 核实真 disjoint。**互补**: 即使认领点前移, 若 `sync_status` 撒谎说「已同步」, AI 照样在落后树上开工。
- **memory**: `feedback_concurrent_duplicate_audit_fetch_before_start` (本缺陷是其**工具层成因**) / `feedback_test_mock_pattern_hides_prod_bug` / `feedback_completion_signals_vs_runtime_invocation` / `feedback_probe_first_scope_reframe` / `feedback_spike_first_for_data_hypotheses` / `project_submodule_drift_direction` (US-008) / `feedback_cross_agent_verdict_independent_verify` (R3 两位 agent 对 `fetched_at` 是否在 normalize 白名单给出**相反的代码事实**, owner grep 裁决)
- **CLAUDE.md** 多远程推送段 (2026-04-10 市场滞后事故 —— 即本缺陷盲区所在)
