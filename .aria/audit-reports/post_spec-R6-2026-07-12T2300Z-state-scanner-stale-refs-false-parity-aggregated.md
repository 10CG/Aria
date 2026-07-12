---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
verdict: FAIL
timestamp: 2026-07-12T23:00:00.000Z
context: state-scanner-stale-refs-false-parity
agents: [qa-engineer, code-reviewer, backend-architect]
---

# post_spec 收敛审计 — state-scanner-stale-refs-false-parity (R6)

> **接续**: [R1+R2](./post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R3+R4](./post_spec-R3-R4-2026-07-12T2000Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R5](./post_spec-R5-2026-07-12T2230Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **R6 scope** (窄): 对抗性证伪 **v6 自己** —— 尤其 owner 裁定新增的 **F10′**。
> **参与**: 3/3 (qa-engineer / code-reviewer / backend-architect) | **Verdict: FAIL** (3/3 FAIL)

---

## 🔴 R6 的结论: **F10′ 方向搞反了。旗舰修复在它要修的场景上算出了相反的值。**

**三个 agent 独立收敛于同一条 Critical。owner 已实测复核。**

### C-1 — 「镜像落后」在 git 眼里是 `ahead`, 不是 `behind`

```
事故态 (今日活体): standards 本地 = 79b7cd6 | github/master = 9df1722 (镜像落后 2)

$ git rev-list --left-right --count 79b7cd6...9df1722
2	0
  left  = local 有而 github 没有 = 2
  right = github 有而 local 没有 = 0

代码映射 (multi_remote.py:205):  ahead, behind = int(parts[0]), int(parts[1])
⇒ ahead=2, behind=0  ⇒  parity = "ahead"        ← 不是 "behind"!
```

**F10′ 的 AC-16 断言 `parity == "behind"` 是事实错误。**

**更致命的第二跳**: 即便接受 `ahead`, **三处独立证据把 `ahead` 的非阻断性锁死**:

| # | 证据 | 原文 |
|---|------|------|
| 1 | **AC-8 / DEC D7** (owner 裁定 2026-07-12) | 「`ahead` 既不阻断也不是正证据」 |
| 2 | **golden fixture** `tests/fixtures/reference-snapshot-aria.json` | `main github->ahead` + `overall_parity: true` |
| 3 | **AB rubric** `ab-suite/state-scanner.json:143-144` | `"Should exclude parity: ahead from overall_parity computation"` + `"Should NOT trigger drift warning when only has_pending_push is true"` |

⇒ F4′ 的 ∀ 子句**不排斥 ahead**; ∃ 子句由主仓/origin 的 `equal` 满足
⇒ **`overall_parity` = `true`** ⇒ 🔴 **C-A 根本没修好。AC-16 与 AC-8 字面互斥。**

> **AB rubric `:142` 甚至逐字描述了这个场景并把修法钉成 `push`**: `"per-claim fix hint: 'git -C <path> push github master' for the lagging remote"` —— **它自己就承认这是 `ahead` 语义。**

### C-1 揭示的更深问题: **D7/AC-8 裁定本身有盲区**

D7 的理据 (owner 采纳 code-reviewer R4 药方):
> 「本 Spec 修的是「**落后时假绿**」(危险: 会在旧代码上开工重复劳动), **不是「领先时假红」** (领先不会导致重复劳动)。」

🔴 **这句话对 mirror remote 是错的。**

**领先 github 恰恰就是危害本身** —— 它意味着 GitHub 镜像陈旧、`clone --recursive` 断裂、插件市场版本滞后。

- **今天的事故**: 主仓 master 已推 github, 但其 gitlink 在 github 上不存在 ⇒ **"领先"形态**
- **CLAUDE.md 记载的 2026-04-10 事故** (aria v1.11.1 发版后未推 github ⇒ 市场停在 v1.11.0) ⇒ **"领先"形态**

> ⚠️ **owner 在 v6 修 R5-m-1 时, 还把那句自相矛盾的理据朝错误方向对齐了** —— 让**理据**去迁就**公式** (`ahead ⇒ true`), 而 v5 原本的理据 (「有未推送 commit 确实不是已同步的, 报 false 是诚实的」) **对 mirror 才是对的**。
> **元教训: 当理据与公式矛盾时, 不要默认公式是对的 —— 先问「这个矛盾在保护什么」。**

### C-2 (backend-architect + qa; owner 实测确认) — F10′ 的 fallback 链是**又一个正向枚举**

```
F10′ 伪码: remote_ref = 首个存在者 of refs/remotes/{remote}/{HEAD, master, main}
           不存在 ⇒ reason = "no_remote_head_ref" ⇒ blocking
```

**owner 实测本仓**:
```
aria               origin/HEAD=refs/remotes/origin/master   github/HEAD=MISSING
standards          origin/HEAD=refs/remotes/origin/master   github/HEAD=MISSING
aria-orchestrator  origin/HEAD=refs/remotes/origin/master   github/HEAD=MISSING
```

**`refs/remotes/origin/HEAD` 是 `git clone` 的免费保证; 而 `github` 是 `git remote add` 手工加的 —— 没人会跑 `git remote set-head github -a`。**

⇒ **本仓三个子模块全靠「默认分支恰好叫 `master`」侥幸命中。这是巧合, 不是设计保证。**
⇒ 采用者默认分支叫 `develop`/`trunk` (GitHub 新仓默认 `main`, 但团队约定各异) ⇒ 三候选全 miss ⇒ `no_remote_head_ref` ⇒ **blocking ⇒ 一个字节都没落后的健康 mirror 被判 `overall_parity: false`**。

> **AC-17 dogfood 测不出这个洞** —— 本仓所有默认分支恰好都叫 `master` ⇒ dogfood 会 PASS, **掩盖缺陷**。
> ⇒ memory `feedback_per_spec_assumption_recheck` 的又一次实证: **本仓 dogfood 是 reference, 不是 authority。**

### C-3 (qa + code-reviewer) — F10′ 伪码**丢了 shallow 守卫**

代码顺序 (`multi_remote.py:168` vs `:172`): **`branch is None` 检查在 `shallow` 之前**。
F10′ 把 `branch is None` 的早退**换成** commit-based 路径 ⇒ **`shallow` 再也不会被检查到**。

⇒ shallow 仓 (`--depth 1` submodule checkout = **标准快速 CI 模式**) 的**截断历史算出的 rev-list 计数被当权威 parity**:
```
# shallow(depth=1) + detached HEAD, upstream 改写过历史
$ git rev-list --left-right --count $LOCAL...refs/remotes/x/master
1  5     # 报 "diverged" —— 本地 shallow graft 对自己 root 之外的历史零可见性
```
与 Spec 自己的 footnote 1 / tasks 13.5 (「`shallow_clone` 恒 benign」) **自相矛盾**。

---

## ✅ owner 裁定 (2026-07-12): **换原语 —— F10′ → F10″ (orphaned-gitlink 可达性)**

**根因诊断**: `parity` (ahead/behind/equal/diverged) **天生无法区分两件事**:

| 语义 | 是什么 | 正确处置 |
|------|--------|----------|
| 「我本地有没推的 commit」 | 开发常态 | `has_pending_push` (AC-8/D7 正确) |
| 「**已发布的** gitlink 在 remote 上不可达」 | **完整性破损** | 🔴 必须阻断 |

**今天真正断掉的不变量是「跨仓可达性」, 不是 parity**:
```
主仓 master 已推到 github (dfb3118 ✓)
  └─ 它引用的 gitlink standards@79b7cd6
       └─ 在 standards 的 github 上不可达 ✗
⇒ 任何人 clone --recursive from GitHub = 断裂
```

### F10″ 定义

```
gitlink_orphaned(R) := ∃ 子模块 S:
      主仓在 R 上【已发布】的 commit C = refs/remotes/R/<default>     # 只看已发布的, 不看本地 HEAD
    ∧ G = C 引用的 S 的 gitlink
    ∧ G 在 S 的 remote R 上【不可达】
      # 判定: git -C S branch -r --contains G --list "R/*" 为空
      # ⇒ 枚举 R/* 下【实际存在】的 ref, 零分支名假设
```

### F10″ 实测验证 (owner, 2026-07-12, 真仓真命令)

| 场景 | 期望 | 实测 | 判定 |
|------|------|------|------|
| **正例**: 今天的事故态 (github/master=dfb3118 已发布, 其 gitlink 79b7cd6 在事故时的 github ref 集 {9df1722} 上不可达) | 报警 | `merge-base --is-ancestor 79b7cd6 9df1722` → **不可达 ⇒ ORPHANED** | ✅ **正确报警** |
| **反例**: 开发期本地 commit (本地 HEAD 领先 github) | **不报警** | F10″ 只看**已发布**的 `github/master=dfb3118`; 其 gitlink 79b7cd6 现在**可达** | ✅ **零误报** |
| **分支名假设** | 不得有 | `git -C standards branch -r --contains <G> --list "github/*"` → 命中 `github/master` | ✅ **零假设** (枚举实际存在的 ref) |

### F10″ 一次性免疫 R6 的全部 3 个 Critical

| R6 Critical | F10″ 为何免疫 |
|---|---|
| **C-1** (ahead/behind 语义冲突) | **完全不碰 `parity`** ⇒ 与 AC-8 / golden fixture / AB rubric **零冲突** ⇒ **D7 不必重开** |
| **C-2** (分支名枚举 ⇒ 恒红) | 检查的是**具体 SHA 的可达性** ⇒ **不需要猜分支名** |
| **C-3** (shallow 守卫) | 可达性检查只需一个 shallow 守卫, 且语义清晰 (shallow ⇒ 无法判定可达性 ⇒ 诚实 `unknown`) |

**且 F10″ 只在主仓真的推过去之后才可能触发** ⇒ **开发期零误报** (这正是 D7 担心的告警疲劳)。

---

## MAJOR (R6, 待 v7 折入)

| # | 内容 | 提出者 |
|---|------|--------|
| **M-1** | 🔴 **C-C 未闭环: 防饥饿队列救不了「跨 scan」的新鲜度衰减** —— 60 腿 + 15s deadline ⇒ 每次 scan 只刷得动 ~24 腿; 未刷的 ~36 腿要「仍在 300s 窗内」**必须在 300s 内连跑 ~3 次 scan**, 而真实 scan 间隔是**小时级** ⇒ 那 36 腿的 `fetched_at` 恒在数小时前 ⇒ ¬可信 ⇒ blocking ⇒ **大仓恒红且永不翻身**。**Spec 自己写的前提「稳态下 `freshness_window` ≫ scan 间隔」恰恰对它要保护的那类采用者不成立。** 附带: AC-15(c)「连续 N 次 scan 每条 leg 至少刷新一次」与 tasks 3.8 的 **30s TTL replay** 冲突 (连跑会 TTL 命中 ⇒ 零 fetch ⇒ 该 AC 按字面必红) | code-reviewer |
| **M-2** | **防饥饿排队对「永久失败」的 leg 无退避**: SSH deploy key 被吊销的 leg ⇒ `fetched_at` **永不推进** (tasks 3.7: 只在真成功时推进) ⇒ **每次 scan 恒在队首** ⇒ 每次吃一次 ConnectTimeout + 占 host cap 的 1/4 槽位 ⇒ **长期挤占同 host 健康 leg 的预算**。需独立的 `last_attempted_at` + 失败退避窗口 | backend-architect |
| **M-3** | **三态 `fetch_ok` → 遗留 `coordination_fetch.success` (bool) 的 shim 映射规则未定义**。`not_attempted` 折成 `false` ⇒ 谎报失败 (触发 `track_board.py:513` 的「⚠ 离线」红条 = **假警报**, 正是本 Spec 家族第一轮就在打的病); 折成 `true` ⇒ 谎报成功。**8 个既有测试断言 `success`** | backend-architect + code-reviewer |
| **M-4** | **F10′ 把「有意 pin 住的子模块」变成恒红**: 采用者把子模块 pin 在旧 commit (**跨项目常态**) ⇒ F10′ 算出 `behind` ⇒ ∀ 子句阻断 ⇒ 恒 false (今天是 `unknown/detached_head` ⇒ benign)。**AC-17 只覆盖「真 equal」那格, 从没问「pinned 子模块在健康常态下该是什么值」** ⇒ **F10″ 同样必须回答这个问题** | code-reviewer |
| **M-5** | **5.1d 谓词横扫闸不可机械实现**: (a) 「谓词集合」无抽取规则; (b) 表在**主仓 `proposal.md`**, 而 Spec Target 是 **aria-plugin 子模块** ⇒ **插件的 unit test 读不到父仓文件** ⇒ 结构上无法落地; (c) 表内 `error_kind` catch-all 写 `unknown`, 而 Spec B 裁定 (b) 的词表 catch-all 是 **`other`** (AC-14/tasks 2.17 的 fixture 值域同错); (d) tasks 13.4 要求把 `no_remote_head_ref` (一个 **reason 值**, 非谓词) 登记进谓词表 ⇒ 破坏表自身契约 | code-reviewer |
| **M-6** | **12.10 通道 4 (`errors[]`) 无机制**: `normalize_snapshot._transform:148-157` 的 `DROP_KEYS` 是**按 key 名全局丢弃**, 对**数组元素无粒度**; 把 `errors` 放进去会连 `tracks_multibranch.errors` 一起丢掉**承重字段**。同理 `"source"` 全局丢弃会连 `issue_status.source` (聚合字段) 一起丢 | code-reviewer |
| **M-7** | **F6′「一次真实网络往返」与 #141 two-fetch 语义字面冲突**: `coordination_fetch` 现在是**两个独立 `git fetch` subprocess** (各一次握手), 且**不能合并** —— 合并正是 #141 要修的 bug (rc=128 传染)。措辞须澄清: 「一次网络往返」= 「**一次 `remote_refresh` 执行**」(内部仍 Fetch1+Fetch2), **不是**「一次 TCP 连接」 | backend-architect |

## ⚠️ 悬而未决 — C-E 的归因 (需 v7 前独立复验)

**code-reviewer R6-C-3 声称**: `custom_checks` **确实是**漂移通道 (它用**冷缓存**复现: run1 `failed:1` → run2 `failed:0`), 因此 R5-C-E 的归因 (「4 条通道没有一条是 custom_checks」) **是错的**, 且 **Spec C v2 撤回了唯一正确的解药** (`generated_at` 同-snapshot 断言本可根除该通道)。

**owner 复验尝试**: 把 `.aria/cache/issues.json` mtime 设为 40 分钟前后跑测试 ⇒ 失败, **但漂移键是 `behind` (0→2)** —— 因为**并发 session 恰好在两跑之间推了 2 个 commit** ⇒ **该次复验被真实上游变动污染, 未能隔离 custom_checks**。

⇒ 🔴 **v7 前必须在「无并发写入 + 冷缓存」的干净条件下重跑一次**, 裁定:
- 若 custom_checks **确是**通道 ⇒ **Spec C 应撤回它的「撤回」** (它的修法本来就能杀死这条), 母 Spec 只认领它真能修的那几条。
- 该测试的漂移通道**至少有 5 条** (R5 的 4 条 + 可能的 custom_checks + 真实上游变动) ⇒ **它本质是一个「跑真 scan 打真网络」的不可靠测试**, 根治方案可能是 **offline 旁路** (tasks 9.7) 而非逐条 DROP_KEYS。

---

## 收敛状态

**R5 → R6: 未收敛。** 但**性质变了**:

| 轮 | 剩余缺陷的量级 |
|----|---------------|
| R1 | 药方机制上自我拆台 (换轴) |
| R2 | 新轴上的边界条件 |
| R3 | 公式两端都错 |
| R4 | 分类表的空格 + 一条 ∃-子句 |
| R5 | **公式对了, 但它的上游数据不存在** |
| **R6** | **上游数据的修法用错了原语** —— `parity` 无法表达要修的那个不变量 |

**v6 的正面成果 (R6 三方确认真闭环)**:
- ✅ `可信` 的 null 兜底 (第七次复发) — 闭环
- ✅ `has_unreachable_remote` 三态化 (第六次复发) — 闭环, **零枚举 ⇒ 无补集可漏**
- ✅ `enforced_set` 的 `[]` 语义 — 闭环
- ✅ Spec B 的词表裁定 (b) + tasks 同步 9 处 — **四处一致**, 且 `test_coordination_fetch.py` **零处断言 `error_kind` 值** ⇒ AC-4 可满足
- ✅ Spec C 的 AC-3 单边化 — 闭环 (live Δ<0 PASS / cache-hit PASS / 真陈旧 FAIL / **非恒绿**)
- ✅ tasks 重号 — **104 个编号零重复** (机械核过)
- ✅ **owner 在 v6 起草时自查抓到的第八次复发** (`deadline_skipped` 归 benign ⇒ 假绿) — **backend-architect 独立复核: 「同意推翻, 找不到反驳」**

**⇒ 8 次复发中的 7 次已被杀死。第 9 次 (F10′ 的原语错误) 由 R6 抓出, owner 已裁定换原语 (F10″, 实测已验)。**

---

## R6 的元教训

> **1. 「审计盯着裁决公式」的盲区, 在新一层机制上原样重演。**
> R5 抓到「公式的上游数据不存在」; v6 补了数据生成层 (F10′); **R6 抓到「数据生成层用错了原语」**。
> ⇒ **每加一层, 都要问同一个问题: 「这一层产出的值, 真的能表达我们要判的那个不变量吗?」**

> **2. 当「理据」与「公式」矛盾时, 不要默认公式是对的。**
> v6 修 R5-m-1 时, owner 让**理据**去迁就**公式** (`ahead ⇒ true`)。而 v5 原本的理据 (「有未推送 commit 确实不是已同步的」) **对 mirror remote 才是对的**。
> ⇒ **矛盾是信号, 不是噪音。先问「这个矛盾在保护什么」。**

> **3. 本仓 dogfood 是 reference, 不是 authority** (memory `feedback_per_spec_assumption_recheck` 再度实证)。
> F10′ 的 C-2 (分支名枚举) 在本仓 dogfood 上**必然 PASS** —— 因为本仓三个子模块的默认分支**恰好都叫 `master`**。**AC-17 结构上测不出这个洞。**
> ⇒ **凡是「靠命名/惯例成立」的机制, fixture 必须对抗性地违反那个惯例。**

---

## 下一步 (v7 入口)

1. 🔴 **F10′ → F10″ 重写** (owner 已裁定 + 实测已验; 设计见上)
   - 必须回答 **M-4**: 「**有意 pin 住旧 commit 的子模块**」在 F10″ 下是什么值? (提示: F10″ 天然免疫 —— pin 住的 gitlink 只要在 remote 上**可达**就不报警, 与"新不新"无关 ⇒ **这正是 F10″ 优于 F10′ 的又一处**)
2. **M-1 大仓恒红** (需 owner 裁定: freshness_window 随 leg 数自适应? 还是放弃 deadline 硬上界?)
3. M-2 / M-3 / M-5 / M-6 / M-7 折入
4. 🔴 **C-E 归因复验** (干净条件: 无并发写入 + 冷缓存)
5. R7 (窄范围)
