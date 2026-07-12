---
track-id: state-scanner-stale-refs-false-parity
linked-issue: 10CG/aria-plugin#110
owner-container: aria-runner-bot/023236f2
phase: A.1-postspec-R6
status: active
updated-at: 2026-07-12
---

# Session Handoff — GitHub 镜像修复 + post_spec R5/R6 + F10′ 被证伪 → F10″ 换原语

> owner /goal: `/state-scanner` → 发现真缺陷 → 修镜像 → 跑 R5 → 改 v6 → 跑 R6。
> **本 session 的核心产出不是「Spec 又前进了一版」, 而是「找到了正确的原语」。**

## §0 入口 (新 session 优先读)

- **下一步 = 按 F10″ 重写 §13 + 2.15/2.16, 出 v7, 跑 R7。** F10″ 的设计 + **实测证据**已写进 `proposal.md §F10″`。
- 🔴 **不要按 F10′ 的伪码实施** —— 它已被 R6 三方独立证伪并标 `SUPERSEDED`。
- **前置**: 本 session 有 **3 条 owner 待裁** (见 §6) + **1 条归因待复验** (custom_checks 是否真是漂移通道)。

## §1 已完成

### 1.1 🔴 修复 GitHub 镜像断裂 (真事故, 非演练)

`/state-scanner` 报 `overall_parity: true`。**我不信任它**(本 Spec 的标的就是它撒谎), 直接 `ls-remote` 问远端:

| 仓库 | gitlink | origin | github | |
|------|---------|--------|--------|---|
| standards | `79b7cd6` | ✅ | `9df1722` | **落后 2** |
| aria-orchestrator | `8b947fa` | ✅ | `daf7c79` | **落后 2** |

**主仓 master 已在 GitHub 上, 但它引用的两个 gitlink 在 GitHub 上根本不存在** ⇒ `git clone --recursive` from GitHub **断裂**。
成因: 双子星的 PR#162 只推 Forgejo 漏推 GitHub (违反 CLAUDE.md 多远程推送; 2026-04-10 同类事故重演)。
**已修复并独立核验** (不看 push 回执): 4 仓 × 2 远程全 parity, gitlink 恢复可达。

### 1.2 post_spec R5 (5-agent) — **5/5 FAIL**, 5 Critical / 9 Major / 6 Minor

**决定性发现 (C-A)**: **公式对了, 但它要裁决的数据不存在。**
`multi_remote.py:169` 在 `branch is None` (detached HEAD = **子模块的规范常态**) 时**在读任何 remote ref 之前就 return** ⇒ 无论 F3′ fetch 多新鲜, **比较从未发生** ⇒ v5 判 benign 不阻断 ⇒ **本 Spec 要杀的 bug 原样存活**。
**今日活体复现**: 就是 §1.1 那个事故。

其余 4 Critical: `has_unreachable_remote` 正向枚举 fail-OPEN (**第六次复发**) / deadline 三态缺失 + 大仓恒红 / Spec C 的 AC-3 把恒红从 cache 搬到 live / **baseline「0 failed」是假前提** (实测 1006 tests **1 红**, ≥4 条漂移通道)。

### 1.3 三份 Spec → v6 + DEC → v7

- **谓词定义域横扫表** (把「类修」从纪律变机制) —— **当场抓出 `has_unpublished_branch` 被引用 4 次、代码零命中、从未定义** (前 5 轮 25 个 agent-round 无人发现)
- `has_unreachable_remote` **三态化** (`fetch_ok == false`, **零枚举 ⇒ 无补集可漏** —— 比补集白名单更彻底)
- `可信(r)` 补 `null` 兜底 (第七次复发)
- `enforced_set` 的 `[]` 语义 (不修则**所有默认采用者恒 false**)
- Spec B: 词表裁定 **(b) 保留旧词表** + tasks 同步 3→9 处 + AC-3/AC-4 可满足化 (**它被指定"应先落地", 却按自己的 0-failed 闸门无法 ship**)
- Spec C: AC-3 单边化 + §3 根因撤回 + AC-5 豁免

### 1.4 🔴 v6 起草时 owner 自查抓到**第八次复发**

采纳 backend-architect 建议把 `deadline_skipped` 归 benign ① ⇒ 推演发现**制造假绿**:
大仓 origin 快腿提供 ∃ 证据 + github 被 deadline 砍判 benign ⇒ `overall_parity: true`, **而 github 可能真领先 100 commit**。
⇒ **本 Spec 要杀的 bug 经由新机制复活。** 改用 code-reviewer 的方案 (裁决权交回 `可信(r)` + 防饥饿排队)。
**R6 的 backend-architect 独立复核: 「同意推翻, 找不到反驳」。**

### 1.5 post_spec R6 (3-agent) — **3/3 FAIL** ⇒ **F10′ 被证伪**

```
事故态: standards 本地 79b7cd6 | github/master 9df1722 (镜像落后 2)
$ git rev-list --left-right --count 79b7cd6...9df1722
2	0                              # left=ahead=2, right=behind=0
multi_remote.py:205:  ahead, behind = int(parts[0]), int(parts[1])
⇒ parity = "ahead"                ← 不是 "behind"!
```
**「镜像落后」在 git 眼里是「本地领先」。** 而 `ahead` 的非阻断性被**三处独立证据锁死**:
AC-8/DEC-D7 + golden fixture (`main github->ahead ⇒ overall_parity: true`) + AB rubric (`:143` "Should exclude parity: ahead")
⇒ **F10′ 上线后事故场景仍是 `true`。AC-16 与 AC-8 字面互斥。**

另外 2 Critical: fallback 链 `{HEAD,master,main}` 是**又一个正向枚举** (实测**三个子模块的 `refs/remotes/github/HEAD` 全部不存在**, 全靠"分支恰好叫 master"侥幸) / 伪码**丢了 shallow 守卫**。

### 1.6 ✅ owner 裁定: **换原语 → F10″ (orphaned-gitlink 可达性)**, 实测已验

```
gitlink_orphaned(R) := ∃ 子模块 S:
      C = 主仓在 R 上【已发布】的 commit (refs/remotes/R/<default>)   # 只看已发布的, 不看本地 HEAD
    ∧ G = C 引用的 S 的 gitlink
    ∧ G 在 S 的 remote R 上【不可达】
      # 判定: git -C S branch -r --contains G --list "R/*"  为空 (零分支名假设)
    ∧ ¬shallow(S)
```
**实测三场景全过**: 事故态**正确报警** / 开发期**零误报** / **零分支名假设**。
**一次性免疫 R6 全部 3 Critical + M-4**, 且**与 AC-8 零冲突 ⇒ D7 不必重开**。

### 1.7 产出物

| 文件 | 内容 |
|------|------|
| `.aria/audit-reports/post_spec-R5-...-aggregated.md` | R5 (5C/9M/6m) |
| `.aria/audit-reports/post_spec-R6-...-aggregated.md` | R6 (3C/7M) + **F10″ 设计 + 实测** |
| `openspec/changes/state-scanner-stale-refs-false-parity/` | v6.1 (F10′ 标 SUPERSEDED + F10″ 写入) |
| `.../state-scanner-snapshot-stderr-secret-leak/` | Spec B v2 |
| `.../state-scanner-issue-cache-freshness-assertion/` | Spec C v2 |
| `docs/decisions/DEC-20260712-001-*.md` | v7 (D7-D14; D10 SUPERSEDED by D14) |
| commit `840e154` | 已推 origin + github, **独立核验** |

## §2 未完成 / Carry-forward

- **carry-f10-double-prime**: 按 **F10″ 重写 tasks §13 + AC-16/AC-17 (2.15/2.16)** → v7 → **R7**。设计 + 实测已在 `proposal.md §F10″`, **可直接照抄**。
- **carry-r6-majors**: R6 的 7 个 Major 待折入 v7 (详见 R6 报告):
  - **M-1 大仓恒红未闭环** (⚠️ 需 owner 裁定): 防饥饿队列只解决 **scan 内**饥饿; **跨 scan** 的新鲜度衰减仍恒红 —— 60 腿 + 15s deadline ⇒ 每次只刷 ~24 腿, 剩下的要"仍在 300s 窗内"**必须 300s 内连跑 3 次 scan**, 而真实 scan 间隔是**小时级**。**Spec 自己的前提「稳态下 window ≫ scan 间隔」对它要保护的那类采用者不成立。**
  - M-2 防饥饿排队对**永久失败**的 leg 无退避 (吊销的 deploy key ⇒ 恒在队首 ⇒ 挤占同 host 预算)
  - M-3 三态 `fetch_ok` → 旧 `coordination_fetch.success` (bool) 的 **shim 映射未定义** (折错 ⇒ `track_board` 跳"⚠离线"假警报)
  - M-4 「**有意 pin 住旧 commit 的子模块**」(跨项目常态) 在 F10′ 下恒红 —— **F10″ 天然免疫** (只要可达就不报警, 与"新不新"无关)
  - M-5 谓词横扫闸**不可机械实现** (表在主仓, Spec target 是 aria-plugin 子模块 ⇒ 插件 unit test 读不到父仓文件)
  - M-6 `DROP_KEYS` 对**数组元素无粒度** (`errors[]` / `source` 全局丢弃会误伤承重字段)
  - M-7 F6′「一次网络往返」与 #141 two-fetch 字面冲突 (**合并会复活 #141**)
- 🔴 **carry-ce-reattribution**: **R5-C-E 的归因待复验**。code-reviewer R6 用**冷缓存**复现出 `custom_checks` **确实是**漂移通道, 与 R5 的结论("4 条通道无一是 custom_checks")矛盾。owner 复验时**被并发 session 的推送污染** (漂移键跑成了 `behind` 0→2), 未能隔离。
  ⇒ **v7 前必须在「无并发写入 + 冷缓存」的干净条件下重跑。** 若 custom_checks 确是通道 ⇒ **Spec C 应撤回它的"撤回"** (它的 `generated_at` 修法本来就能杀死这条)。
  ⇒ 该测试的漂移通道**至少 5 条** ⇒ 它本质是「跑真 scan 打真网络」的不可靠测试, **根治可能是 offline 旁路 (tasks 9.7) 而非逐条 DROP_KEYS**。
- (承前) M6 owner 4 门 / M7 D3 门 / carry-136-rotation / 168h 跑。

## §3 关键风险 / 已知陷阱

### 3.1 🔴 同一不变量, **九次复发**

| # | 形态 | 发现于 |
|---|------|--------|
| 1-5 | (见 R3-R4 报告) | R1-R4 |
| 6 | `has_unreachable_remote` 「按 network 类」= **正向枚举** ⇒ 真实故障 5 种 3 种落 catch-all ⇒ fail-OPEN | R5 |
| 7 | `可信(r)` 未定义 `fetched_at = null` | R5 |
| 8 | `deadline_skipped` 归 benign ⇒ **假绿** | **v6 起草时 owner 自查** |
| 9 | **F10′ 用错原语** (算出 `ahead` 而非 `behind`) | R6 |

**7 次已杀死。** 但**根因每次换宿主**: 谓词 → 兜底默认 → **原语选择**。

### 3.2 🔴 审计的注意力会被「公式」独占

5 轮 × 5-agent 反复打磨裁决公式, **R5 才有人问「这个公式要裁决的数据, 真的会被生成吗?」**
**R6 抓到同一盲区在新一层重演**: 补上的数据生成层**用错了原语**。
⇒ **每加一层, 必须重问: 「这一层产出的值, 真的能表达我们要判的那个不变量吗?」**
⇒ memory `feedback_verify_predicate_inputs_exist`

### 3.3 🔴 理据 ↔ 公式矛盾时, 别默认公式是对的

v6 修 R5-m-1 时, owner 让**理据**去迁就**公式** (`ahead ⇒ true`)。
**R6 证明改错了方向** —— 被删的那句理据 (「有未推送 commit 确实不是已同步的」) **对 mirror remote 才是对的**。
**该项目已两次因「领先」形态出事** (2026-04-10 市场滞后 + 今天的 gitlink 断裂)。
⇒ memory `feedback_rationale_formula_contradiction_is_signal`

### 3.4 本仓 dogfood 是 reference, **不是 authority**

F10′ 的分支名枚举缺陷, 在本仓 dogfood 上**必然 PASS** —— 因为三个子模块的默认分支**恰好都叫 `master`**。**AC-17 结构上测不出这个洞。**
⇒ **凡是「靠命名/惯例成立」的机制, fixture 必须对抗性违反那个惯例。**

### 3.5 跨 agent 一致 ≠ 正确 (两个新形态)

- **「只测了一半定义域就报 PASS」**: qa 判 Spec C 的 AC-3 PASS —— 它只 emulate 了 **cache-HIT**, 从没测 **cache-MISS/live** (那一格恒假)。**不是错, 是漏测, 而报告里看不出来。**
- **「五个 agent 一起算错」**: R4 全体用 `ceil(60/4)×7s≈105s` (把 per-host cap 当全局单池); R5 用真实拓扑推翻 —— 只有 **2 个物理 host**, 正解 **35s**。**量级差 3 倍。**

## §4 owner 决策记录

| 决策 | 内容 |
|------|------|
| **修镜像优先** | 先修 GitHub 镜像断裂再跑 R5 (对外可见的完整性破损 + 顺手成为主 Spec 的第二个活体证据) |
| **C-A 处置** | **扩本 Spec 加 F10′** (而非拆 Spec D) —— **后被 R6 证伪** |
| 🔴 **D14 换原语** | **F10′ → F10″ (orphaned-gitlink 可达性)**, 取代 D10。理由: `parity` 天生无法区分「我有未推的 commit」(开发常态) 与「**已发布的** gitlink 不可达」(完整性破损)。**F10″ 与 AC-8 正交 ⇒ D7 不必重开。** |
| **D7 盲区留痕** | D7 的理据「领先时假红无害」**对 mirror remote 是错的** —— 但 D14 换原语后**不必重开 D7** |

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | `840e154` (Spec v6 + DEC v7 + R5/R6 报告) → origin + github ✅ **独立核验** |
| aria / standards | 未变更 (本 session 无插件代码改动 —— **全部是 Phase A.1 文档**) |
| aria-orchestrator | ` M` = **有意的 WIP feature 分支 checkout**, 非待办 |
| GitHub 镜像 | ✅ **已修复** (standards `→79b7cd6` / aria-orchestrator `→8b947fa`), gitlink 恢复可达 |
| 协调 ref | `state-scanner-stale-refs-false-parity` claim **仍 active** (A.1 未完成, 不释放) |
| 双子星 | 本 session 期间推了 2 commit (`3487ad4`): **补齐 DEC-20260712-002 + 闭合编号撞车** ⇒ R5-m-6 **已被他们关掉** |

## §6 Next session 入口 + 优先级

1. 🔴 **按 F10″ 重写 tasks §13 + AC-16/AC-17** → v7。**设计与实测证据已在 `proposal.md §F10″`, 可直接照抄。**
2. **3 条 owner 待裁**:
   - **M-1 大仓恒红**: `freshness_window` 随 leg 数自适应? 还是放弃 deadline 硬上界? 还是承认「大仓必然有 leg 过期」并接受?
   - **OQ-F** (`verify_mode: ls_remote` 退役) 转正式 D 编号 —— 目前只是"倾向", Phase B 会分叉
   - **M-5**: 谓词横扫表**放哪** (主仓 proposal 里插件测不到 ⇒ 要么搬进 aria-plugin, 要么改成 review checklist)
3. 🔴 **carry-ce-reattribution 复验** (干净条件: 无并发写入 + 冷缓存)
4. **R7** (窄范围: F10″ + R6 的 7 个 Major)
5. **落地顺序不变**: Spec C (独立) → Spec B (Rule #7, 须先于主 Spec) → 主 Spec

## §7 提交清单

- `840e154` (Spec v6.1 ×3 + DEC v7 + R5/R6 报告) → **origin + github, 已独立核验**
- 本 handoff → 待 commit

## §8 Memory entries

**新建**:
1. `feedback_verify_predicate_inputs_exist` — 审计判定机制必分两层: 逻辑对吗 + **它要判的输入真会被生成/能表达那不变量吗**。注意力被公式独占 (公式是唯一能逐字推演的东西, 数据生成层往往连编号都没有)。
2. `feedback_rationale_formula_contradiction_is_signal` — **理据↔公式矛盾时别默认公式对**; 理据常在保护公式漏掉的场景。

**补强既有**:
- `feedback_cross_agent_verdict_independent_verify` — 两个新形态: 「只测半个定义域就报 PASS」+「五个 agent 一起算错 (105s vs 35s)」
- `feedback_per_spec_assumption_recheck` — **本仓 dogfood 会系统性掩盖「靠惯例成立」的缺陷** (三个子模块默认分支恰好都叫 master)
- `feedback_invariant_needs_failclosed_default` — **谓词定义域横扫表** (把类修变机制) + **三态优于补集白名单** (让枚举消失 ⇒ 无补集可漏)

## Cross-references

- Spec: `openspec/changes/state-scanner-stale-refs-false-parity/` (**v6.1, F10′ SUPERSEDED, F10″ 待实施**)
- DEC: `docs/decisions/DEC-20260712-001-*.md` (**v7, D14**)
- 审计: `.aria/audit-reports/post_spec-{R1-R2,R3-R4,R5,R6}-*.md`
- Issue: aria-plugin [#110](https://forgejo.10cg.pub/10CG/aria-plugin/issues/110)
- 下游: `openspec/changes/aria-2.0-m7-fleet-aggregation` (Approved, 消费 `overall_parity`)
- 前序 handoff: `2026-07-12-state-scanner-false-parity-spec-r4.md`
