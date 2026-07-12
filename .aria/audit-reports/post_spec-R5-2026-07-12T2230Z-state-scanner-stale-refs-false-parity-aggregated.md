---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
verdict: FAIL
timestamp: 2026-07-12T22:30:00.000Z
context: state-scanner-stale-refs-false-parity
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 收敛审计 — state-scanner-stale-refs-false-parity (R5)

> **接续**: [R1+R2](./post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md) → [R3+R4](./post_spec-R3-R4-2026-07-12T2000Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **Anchor** (不变): 修复 sync parity 假绿, 使「陈旧证据 ≠ 新鲜证据」不变量成立。
> **R5 scope** (按 R4 tech-lead 建议收窄): 只审 **F4′ 最终公式 + R4 的 5 个修正点**, 不跑全量。
> **Forgejo**: aria-plugin **#110**

**参与**: 5/5 | **Verdict: FAIL** (5 FAIL / 0 PASS; **未收敛**)

| agent | verdict | 核心发现 |
|-------|---------|---------|
| qa-engineer | **FAIL** | **C-A** 原始缺陷在 v5 下原样存活 (真 fixture 复现) |
| tech-lead | **FAIL** | C-B `has_unreachable_remote` fail-OPEN (第六次复发) + C-C deadline + C-D Spec C |
| code-reviewer | **FAIL** | C-D Spec C 反向过冲 + **C-E baseline「0 failed」是假前提** |
| backend-architect | **FAIL** | C-C deadline 毒化 `overall_parity` 本体 + `remote_branch_missing` 分桶错 |
| knowledge-manager | **FAIL** | Spec B 三处互斥无裁定任务 + 4 项文档漂移 |

> **五位一致 (与 R4 相同)**: **轴、两轴拆分、benign/blocking 二分都对, 不需第六次换轴。**
> 但 R5 推翻了 R4 的「R5 应当 PASS」预期 —— 因为 R1-R4 **从未验证过 F4′ 的上游数据是否存在**。

---

## 🔴 C-A (qa-engineer; owner 独立复核确认; **今日活体复现**) — 本 Spec 要杀的 bug 在 v5 公式下**原样存活**

**这是 R5 唯一的新轴向发现, 也是最重的一条。**

### 根因 (代码实测)

`multi_remote.py:148-183` `_remote_parity_local_refs` (**生产默认路径**, `verify_mode=local_refs`):

```python
if branch is None:
    base["reason"] = "detached_head"
    return base                              # ← 在触碰任何 remote-tracking ref 之前就返回
...
ref = f"refs/remotes/{remote}/{branch}"      # ← 只有走到这里才会真的看这个 remote 的数据
```

子模块经 `git submodule update --init --recursive` (**CLAUDE.md 让每个新采用者跑的第一条命令**) 后**恒为 detached HEAD** (`branch=None`) ⇒ **对每一个 remote 都在同一行早退**。

⇒ **无论 F3′ 把 github 的 ref fetch 得多新鲜, 这个函数从未看过它一眼。网络成本已经付了, 但比较从未发生。**

### v5 公式在这条数据上的行为

两个 remote 条目都是 `parity=unknown, reason=detached_head` ⇒ v5 判 **① 类 fetch-无关 ⇒ 恒 benign ⇒ 不阻断** ⇒
`∃ r: 可信 ∧ equal` 由**主仓**满足 ⇒ **`overall_parity = true`**。

**F4′ 只对「已经被赋值的 parity/reason」做分类。它无法 catch 一个从未被赋成 `behind` 的落后。**

### 今日活体证据 (production, 非 fixture) — 本 session 开局的真实 scan

```
scan.py snapshot (2026-07-12T21:58Z):
  overall_parity: true                                          ← 报「已同步」
  standards:          github parity=unknown reason=detached_head
                      origin parity=unknown reason=detached_head
  aria-orchestrator:  github parity=unknown reason=no_local_tracking_ref

ls-remote 地面真相 (同一时刻):
  standards          gitlink=79b7cd6  origin=79b7cd6 ✅  github=9df1722 ❌ (落后 2 commit)
  aria-orchestrator  gitlink=8b947fa  origin=8b947fa ✅  github=daf7c79 ❌ (落后 2 commit)
  ⇒ 主仓 master (已在 GitHub 上) 引用的两个 gitlink 在 GitHub 上根本不存在
  ⇒ `git clone --recursive` from GitHub = 断裂
```

**state-scanner 对一次真实的、对外可见的仓库完整性破损, 报告「已同步」。** 而 v5 公式**不会改变这个结论**。

### 与 Spec 自己的 Why section 的关系

proposal.md L33-39 引用的活体证据正是 `aria-orchestrator github 镜像落后 32 commit`。**四轮审计从未验证过 F4′ 是否堵得上它。** 答案是: 堵不上。

CLAUDE.md 记载的 **2026-04-10 真实事故** (aria v1.11.1 发版后未推 GitHub, 市场版本滞后) 是同一模式 —— **本项目已经发生过, 不是假想**。

### 交叉证据: snapshot 里**没有任何字段**能捕获它

`sync.py:36-41` `_ORIGIN_HEAD_REFS` **硬编码只查 origin**:
```python
_ORIGIN_HEAD_REFS = ["refs/remotes/origin/HEAD", "refs/remotes/origin/master", "refs/remotes/origin/main"]
```
⇒ `sync.py` 的 commit-based 子模块 drift 算法 (不依赖分支名, **算法本身是对的**) **只对 origin 跑**, 从不看 github。

⇒ **整个 snapshot 没有任何字段能捕获「detached-HEAD 子模块的非-origin 远端真实落后」。**

### 修法 (owner 裁定)

| 选项 | 内容 |
|------|------|
| **(a) 扩本 Spec (F10′)** | `_scan_repo` 对 detached-HEAD 仓库改用 **commit-based 比较** (`local_head` SHA vs `refs/remotes/{remote}/*`), 而非 `branch is None` 就早退。**不是发明新机制** —— 把 `sync.py:200-330` 已验证工作的算法复用到 `multi_remote.py`。 |
| **(b) 拆 Spec D + 显式 CAVEAT** | 本 Spec 就地 ship F1′-F4′/F9′ (公式本身确已收敛), 但**必须**在 proposal.md 写死「已知缺口: detached-HEAD 子模块对非-origin 远端的真实 drift 不可见」并开跟进 issue。**不得在只字未提的情况下宣称「假同步已修复」。** |

> ⚠️ **不得直接 PASS 合入。** 合入后下一次「忘记推 GitHub」事故发生时, state-scanner 依然会说「已同步」—— 这正是本 Spec 立项要杀的东西。

---

## 🔴 C-B (tech-lead; owner 实测确认; backend-architect 独立补强) — `has_unreachable_remote` 仍是正向枚举 ⇒ fail-OPEN (**同一不变量第六次复发**)

`proposal.md:130` / `tasks.md:59` (4.1) 逐字:
> `fetch_ok == false` ⇒ **永远**记 `error_kind` + **按 network 类**置 `has_unreachable_remote`

「**按 network 类**」= 正向枚举。owner 用**生产分类器** (`coordination_fetch.py:235` `_classify_error`) 跑真实 stderr:

| 真实失败模式 | `error_kind` | 落 network 类? |
|---|---|---|
| HTTPS 连不上 (`Failed to connect to ... port 443`) | `other` | 🔴 **否 → fail-OPEN** |
| HTTPS TLS 握手失败 (`gnutls_handshake() failed`) | `other` | 🔴 **否 → fail-OPEN** |
| **SSH 公钥被拒** (`Permission denied (publickey)`) | `other` | 🔴 **否 → fail-OPEN** |
| SSH 连接超时 | `network` | ✅ 是 |
| DNS 解析失败 | `network` | ✅ 是 |

**5 种真实故障, 3 种落 catch-all ⇒ `has_unreachable_remote` 不置位。**

backend-architect 独立复现**第 4 种**未覆盖模式: `gnutls_handshake() failed: The TLS connection was non-properly terminated` (`network_signals` 里有 `"ssl"` 但**没有 `"tls"`**)。

**加重情节**: **`auth` 被拒也落 `other`** —— 而 **AC-13 正是要测「auth 失败 ⇒ `has_unreachable_remote` 必须 true」**。按 Spec 自己的「按 network 类」措辞, **AC-13 测不出来**。

**后果链** (全部在 v5 文本内可推):
1. github 真的连不上 ⇒ `fetch_ok=false`, `error_kind=other`
2. `other ∉ network 类` ⇒ **`has_unreachable_remote` 不置位** (fail-OPEN)
3. 上次成功 fetch 在 200s 前 ⇒ `可信=true` ⇒ F1′ **不降级** ⇒ `parity` 保持 `equal` ⇒ **还给 ∃-子句提供正证据**
4. ⇒ snapshot 报「已同步 + 无不可达 remote」, 而那个 remote **硬 down**

**这逐字就是 R3-M9 的失败模式** (「凭据坏了 5 分钟, snapshot 一声不吭」) —— **F1′ 两轴拆分就是为杀它而生的, 结果在自己的轴上留了同一个 fail-OPEN 洞。**

**修法** (Spec 自己的 idiom, 一行):
```
has_unreachable_remote(r) := fetch_ok(r) == false ∧ error_kind(r) ∉ 显式 benign 白名单   # fail-CLOSED
```
+ 补 **AC-14**: 分类器返回 catch-all (`other`/`unknown`/`git_error`) 时 `has_unreachable_remote` **必须 true** (pin 测试注入真实 stderr, 非合成 fixture)。

> 与 OQ-C 联动: OQ-C 用 `has_unreachable_remote` 去 gate `multi_remote_drift` 的降级横幅。fail-OPEN 意味着**最常见的真实网络故障下那条横幅永远不显示**。

---

## 🔴 C-C (tech-lead + code-reviewer + backend-architect **三方独立收敛**) — deadline 缺第三态 + 默认 15s 致大仓恒红

**(a) 语义冲突未裁** (R4 提出, v5 **原文未动**):
- `proposal.md:116` / tasks 3.5: 到点未完成的 leg ⇒ 标 `not_refreshed`
- `proposal.md:130` / tasks 4.1: `fetch_ok == false` ⇒ **永远**置 `has_unreachable_remote`

**被我们自己的 deadline 砍掉的 leg, `fetch_ok` 是什么? Spec 全文没答。** 三态 (成功 / 试了失败 / **没试**) 缺一个。

**(b) 默认 15s ⇒ 大仓 `overall_parity` 恒 false** (性能护栏变成正确性回归):

`not_refreshed` ∈ **blocking** 桶 ⇒ `∀ r: ¬blocking_unknown(r)` ⇒ **只要 60 条腿里有 1 条被砍, 整份 snapshot 假红**, 且没有任何一次 scan 能翻身 (无轮转 / deadline 不随 N 伸缩)。

> **backend-architect 纠正了 R4 自己的算式**: R4 的 `ceil(60/4)×7s≈105s` 把 cap-4 当**全局单池**, 但 tasks 1.9 写的是 **per-host**。实测本仓真实拓扑: 4 仓 × 2 remote **只有 2 个物理 host** (forgejo / github)。正确算式:
> ```
> forgejo: ceil(20/4)=5 轮 × 7.0s = 35.0s
> github:  ceil(20/4)=5 轮 × 3.5s = 17.5s   (与 forgejo 并发)
> ⇒ wall-clock ≈ max(35, 17.5) = 35s     (不是 105s)
> ```
> **结论方向不变** (35s ≫ 15s), 但**量级差 3 倍** —— 这本身说明「per-host」的语义 (**按解析后的 hostname 去重**, 而非按 remote 名字数) **必须在 Spec 里写死**, 否则 Phase B 实现者按「remote 名字个数」限流, 真会跑出 105s 那一档。
>
> ⚠️ **又一次「两个 agent 同时错」** —— R4 的算式被 R5 用真实拓扑推翻。memory `feedback_cross_agent_verdict_independent_verify` 再度实证。

**这是本 Spec 第 4/5 次「修假绿过冲成恒红」**, 载体是 F3′ **自己新引入**的 deadline 机制。**R1-R4 从未把 F3′ 的输出代入 F4′ 的 ∀ 子句端到端走一遍。**

**修法** (backend-architect, 最自洽):
1. 给 deadline-cut 的 leg 一个**独立的、无条件 benign** 的 reason (如 `deadline_skipped`), 归 ① 类 —— 它反映的是**我们自己的预算**, 不是该 remote 的真实状态, 语义上与 `detached_head` 同类。覆盖率缺口另立 **advisory-only** 信号 (`remote_refresh.skipped_count`), **不进裁决层**。
   ⇒ `overall_parity` 的正确性**不再依赖 deadline 数值大小**; 默认值选多少只是性能取舍, 不再是正确性回归的开关。
2. F3′/tasks 1.9 写死: 「per-host」= **按解析后的 hostname 去重** (跨仓库、跨 remote 名聚合), 用本仓真实拓扑 (2 host) 做 worked example。

---

## 🔴 C-D (tech-lead + code-reviewer **独立收敛**; owner 实测裁决) — Spec C 的 AC-3 把恒红从 cache 路径**搬到了 live 路径**

v5 的 AC-3: `fetched_at 非空 ∧ 0 ≤ (generated_at − fetched_at) ≤ 2 × cache_ttl_seconds`

**代码实测**:
- `generated_at` = `build_snapshot` **入口** (Spec C task 2.1; `scan.py:91`)
- `issue_scan` 是 **Phase 1.13**, 跑在入口**之后**
- `issue_scan.py:650` / `:711` **live 路径**: `"fetched_at": _now_iso()` ⇒ **fetch 当刻**, 必然**晚于** `generated_at`

| 路径 | Δ = generated_at − fetched_at | AC-3 |
|------|-------------------------------|------|
| **cache MISS (live fetch)** | **−8s (负)** | 🔴 **FAIL — 恒红** |
| cache HIT (600s 前) | +600s | PASS |
| cache HIT (TTL 边缘 900s) | +900s | PASS |
| 真陈旧 (1.13 被跳过, 3600s) | +3600s | FAIL ✅ (正确) |

**cache-miss = 每个 session 首次 scan + 任何间隔 >900s 的 scan + 每次 CI = 常态路径。**
**本 session 自己的 scan 就是 live** (`source=live`, `fetched_at=21:57:58`)。

R4-X-1 说「cache-hit 恒红」; v5 加了 `0 ≤` 下界把它按住, **代价是让 cache-miss 恒红**。
⇒ **在一个专门修「恒红」的 Spec 里, 第二次制造恒红 —— 换了个路径。**

**修法**: 下界毫无必要 (`fetched_at` 比 `generated_at` **晚**是好事, 说明 1.13 在本次 scan 里**真跑了**)。单边即可:
```
issue_status.fetched_at 非空  ∧  (generated_at − fetched_at) ≤ 2 × cache_ttl_seconds
```
+ pin: **live 与 cached 两条路径都必须 PASS** (对偶验收, 与 Spec C 自己的 AC-2「防恒绿真空」同构)。

### 跨 agent 矛盾 (owner 独立裁决)

**qa-engineer 判 AC-3 PASS, tech-lead + code-reviewer 判 FAIL。**

**owner 实测裁决: tech-lead + code-reviewer 对。** qa 的 scenario 7 只 emulate 了 **cache-HIT** 路径 (用 `_lookup_cached_repo`), **从未测 cache-MISS/live 路径**。这不是反证, 是**漏测**。
⇒ memory `feedback_cross_agent_verdict_independent_verify` 的新形态: **不是「两个 agent 同时错」, 而是「一个 agent 只测了一半的定义域就报 PASS」。**

---

## 🔴 C-E (code-reviewer; owner 实测确认 + **发现更多通道**) — 三份 Spec 的 baseline 前提「0 failed」被实测证伪

**owner 独立实测** (未修改代码, aria HEAD `0964496`, 连跑两次):

```
Run A: Ran 1006 tests ... FAILED (failures=1)   test_two_consecutive_runs_diff_zero
Run B: Ran 1006 tests ... FAILED (failures=1)   同一测试, 不同漂移键
```

**跨 4 次观测 (code-reviewer 2 + owner 2), 暴露 4 条互不相同的漂移通道**:

| # | 漂移键 | 根因 | 观测者 |
|---|--------|------|--------|
| 1 | `remote_refs_age` | `sync.py:396/405` 读 FETCH_HEAD mtime; scan 自己的 Phase 1.16 会**改写 FETCH_HEAD** ⇒ run2 看到 "1m" | code-reviewer |
| 2 | `issue_status.repos[].source` | `issue_scan.py:822` cache 命中返 `"cache"`, live 返 `"live"` (900s TTL) ⇒ run1 miss / run2 hit | code-reviewer |
| 3 | `coordination_fetch.degraded` / `degradation_reason` | 真实网络抖动 ⇒ 一跑降级一跑不降级 | **owner** |
| 4 | `errors[]` 数组 | 同上 soft error 时有时无 | **owner** |

**根因同一**: 这个「稳定性测试」**跑的是真 scan 打真网络**, 两跑之间的网络/TTL/缓存状态本来就会变。**4 条都不在 `normalize_snapshot.py` 的 `TIMESTAMP_KEYS`/`DROP_KEYS` 名单里。**

### 后果

**(a) Spec C 的 §3 根因归错了。** Spec C 说 flaky 源于 `custom_checks` 的 `failed:1→0`。**实测的 4 条漂移键没有一条是 custom_checks。** ⇒ Spec C 的修法 (`generated_at` + 重定义 check) **一条都消不掉** ⇒ **AC-4「两种前置条件下都必须绿」不可达**, 且它的两个前置条件 (cache 陈旧/新鲜) **钉错了轴**。

> 与 R4 给 Spec B 的「AC-1 靶点错位」是**同一 species**: 一个可以「碰巧通过」而真 flaky 依旧的 AC。

**(b) 「0 failed」在三份 Spec 里都是假前提**: 母 Spec (proposal L275 + tasks 12.2) / Spec B (AC-3) / Spec C (AC-5)。
**Spec B 受害最重** —— 它被指定「**应先落地**」, 却既不碰 `remote_refs_age` 也不碰 `source` 也不碰网络抖动 ⇒ **它的 AC-3 在自己的 PR 上结构性恒红 ⇒ Spec B 按自己的闸门无法 ship。**

**(c) 即使三份全 ship 该测试仍红**: 母 Spec tasks 8.4 顺带干掉 `remote_refs_age`, 但 **`issue_status.repos[].source` + `degraded` + `errors[]` 无人认领**。

**修法**:
1. 把 `source` (以及 `degraded`/`degradation_reason` 的 run-to-run 变体) 加入 `normalize_snapshot.DROP_KEYS` —— **仓内已有逐字先例**: `DROP_KEYS` 的 `cached`/`age_seconds`/`refs_fetched` 注释 (v1.30.2) **明写**「TTL-based, varies between consecutive runs… Stability test requires drop」。**同一 class 已解过一次, Spec C 又原样引入。**
2. 三份 Spec 的判据改成「**0 failed, 且已声明 baseline 既有 1 红 (`test_two_consecutive_runs_diff_zero`) 由 <哪份 Spec> 消除**」。当前措辞让 Phase B 无法区分「我弄红的」和「本来就红」。
3. Spec C 的 §3 + AC-4 按实测重写。

---

## MAJOR

| # | 内容 | 提出者 |
|---|------|--------|
| M-1 | **`可信(r)` 在 `fetched_at is null` 时未定义** —— 与 Spec 自己 L53 列的违反形态 #3 (「从未获取过的证据当正证据」) **完全同形**, 也正是 `multi_remote.py:497` 今天的 bug。AC-6 兜住了**行为**, **谓词定义没兜**。必须写死 `可信(r) := fetched_at ≠ null ∧ (now − fetched_at) ≤ window` | tech-lead |
| M-2 | **`remote_branch_missing` (:276) 分到 ② 桶 (fetch-依赖) 是分类错误** —— 它是 `git ls-remote` **实时网络往返**的权威回答 (「这一秒对方说没有」), 新鲜度**内建在自己的调用里**; 而 `no_local_tracking_ref` (:181) 是读**可能陈旧的本地缓存**失败。把前者塞进依赖 `可信(r)` 的 ② 桶 ⇒ 若 ls_remote 路径拿不到 `remote_refresh` 的 `fetched_at` (大概率, 它是 Phase 1.12 内的独立调用) ⇒ **`可信` 恒 false ⇒ 恒 blocking ⇒ 又一次自造恒红** | backend-architect |
| M-3 | **Spec B: Tasks 没跟上 §正文** —— §2 已列全集 (≥8/9 处), 但 **tasks 2.1 仍只写 3 处** (`git.py:184/356` + `sync.py:150`); **tasks 1.2 仍写「凭据 sentinel 红测试」**, 而那正是 R4 判定「在未修改代码上就会 PASS ⇒ 违反自我否证闸」的旧 fixture。**Phase B 执行的是 tasks, 不是 §Why。** R4 的矛盾没消除, 只是**从 §Why 搬进了 Tasks** | code-reviewer + tech-lead |
| M-4 | **Spec B: AC-4「逐字节不变」的词表矛盾只被记录、未被裁定, 且无任务承载裁定** —— §1 (L43 新枚举) / AC-4 (L106 逐字节不变) / task 1.1 (L112 逐字节不变) **三处互斥表述原样留在待 sign-off 的文档里**; Spec B 的 tasks 1.1→4.2 **零裁决项**。母 Spec 的 `error_kind` **硬依赖**此裁定 (proposal L118「复用姊妹 Spec 的分类器」), 且 C-B 的 fail-CLOSED 白名单要按最终词表写 ⇒ **Phase B 无法开工** | knowledge-manager + tech-lead + code-reviewer (**三方独立收敛**) |
| M-5 | **F9′ 只堵了 `sync.py` 一个平行计算点, 漏了 `verify_mode: "ls_remote"` 这第二个** —— `_remote_parity_ls_remote` (`:228-330`) 自己发独立网络调用、自己算 `reachable`; F3′ 落地后它会变成**第三个独立的可达性计算点** + **双倍网络**。Spec 必须裁定: 退役 / 改由 `remote_refresh` 供数 / 接受双算 (并说明谁赢) | tech-lead |
| M-6 | **F6′ 改名 与 OQ-B「原样保留+新开块」之间, 「旧 collector 退役还是并行重复跑」没写清** —— 若 Phase B 读成 (b) 并行, origin 每次 scan 被 fetch **两次** + **两套独立 TTL 缓存**可能对同一 origin 给出**不同答案** ⇒ **在 `coordination_fetch` 块与 `remote_refresh` 块之间重新生产本 Spec 想消灭的「同一 snapshot 自相矛盾」** | backend-architect |
| M-7 | **OQ-E 三轮过去仍是全文唯一「零倾向」的 OQ**, 而它直接坐在 **US-008 数据丢失护栏** (`sync.py:312-328`) 之上。建议**倾向 (a)** (消费 F1′/F3′ 已产出的同一份新鲜度信号) —— 与本 Spec 核心哲学一致, 且让 AC-10「不得自相矛盾」**自动成立** (共享同一来源, 而非人工交叉核对两套独立计算) | backend-architect |
| M-8 | **母 Spec 文本 vs 现实漂移**: `proposal.md:3` + `tasks.md:4` 仍写 `Draft v4 … 待 post_spec R4` (正文 L162 已是 **v5 公式**, L285 已含 **R4 owner 裁定**); `proposal.md:7` Audit trail **只链 R1-R2**, 缺 R3-R4 聚合报告 (**v5 公式的来源**) ⇒ 从 Spec 出发**无法发现** fail-CLOSED 的论证过程 | knowledge-manager + tech-lead + code-reviewer |
| M-9 | **DEC-20260712-001 停在 v2** (止于折入 R1), 而 proposal.md 的 **Decision 字段直接指向它** ⇒ **读者顺链接得到的是被推翻的 v1/v2 设计**。且 L182 仍留有未清理的编辑期警示 (「#109 首次活体验证」措辞需交叉核对再落笔) | knowledge-manager |

## MINOR

- **m-1** AC-8 的**理据**与它自己的**断言**不自洽 (理据说「有未推送 commit 确实不是已同步」, 断言却要 `origin=equal + github=ahead` ⇒ true)。**公式与 AC-12 已自洽** (owner 裁定被正确落进公式), 只是那句一行理据不是公式的正确描述 ⇒ Phase B 实现者可能写出「任一 remote ahead ⇒ false」打掉 golden fixture。改一句话即可: **「≥1 个 enforced remote 提供新鲜的 equal 证据, 且没有任何 remote 落后/分叉/blocking-unknown」** — tech-lead
- **m-2** `enforced_set` 的**空值语义**没写进 Spec。跨 skill 契约 (`phase-c-integrator/SKILL.md:574`) 是「空则自动发现所有 remote」, 而 `DEFAULTS.json:9` 顶层就是 `[]` ⇒ 实现者若直读 `[]` ⇒ `enforced_set = ∅` ⇒ AC-12 的非空护栏 ⇒ **所有默认采用者恒 false** — tech-lead
- **m-3** `tasks.md:38` 与 `:39` **都是 `2.13`** (而 tasks 头部自书「编号不可变」, 且 #95 归档门按 checkbox 计数); `tasks.md:26` (2.1) 的「豁免 2.9 设计闸」交叉引用在 renumber 后失效 — tech-lead
- **m-4** `has_unreachable_remote` **今天在生产里结构性恒 False**: 默认 `verify_mode=local_refs` 下 `reachable` 恒 True (`:163/:182` 硬编码), L410 的 reason 触发集 (`network_timeout`/`auth_failed`/`not_found`) **只产自 ls_remote 路径** ⇒ tasks 4.1 必须**替换**该触发器为 `fetch_ok` 驱动, 而非叠加 — code-reviewer
- **m-5** AC-11b 只存在于 tasks.md (5.2b), proposal.md 的官方 Verification 枚举**没有它** — knowledge-manager
- **m-6** 🔴 **`DEC-20260712-001` 编号撞车** (跨 Spec, 不阻塞本 Spec): 主仓 commit `f399e71`/`5b8c3dc` 引用 `DEC-20260712-001 = task-level auth 禁令撤销 (Aether #234)`, 而**全仓 grep 只命中一个文件** —— 本 Spec 的 state-scanner 决策。**那条 auth 决策无任何文件承载 = dangling ref** ⇒ 按 git log 查 DEC 的人会查错。建议双子星侧改用 `-002` 或补文件 — knowledge-manager

---

## R4 的 5 个修正点 — 结算

| # | 修正点 | 状态 |
|---|--------|------|
| 1 | **R4-C1 fail-CLOSED + benign 两层** | ✅ **闭环** (tech-lead / code-reviewer / backend-architect **三方独立逐格核对**: `multi_remote.py` reason 全集 = 10 具名值 + `None`, v5 两桶**零漏格**; `parse_error` 已入桶; `:308/312/317` 的 `reason=None` 由兜底覆盖; tasks 5.1c pin 测试把「逐格填」机制化) |
| 2 | **R4-C7 AC-8 ⊥ AC-12** | ✅ **闭环** (owner 裁定被无矛盾地落进公式与两条 AC; 仅剩理据措辞问题 m-1, 非机制问题) |
| 3 | **`∀ 可信` 缺口** | ✅ **闭环** (已从 ∀ 删除) —— 但**暴露出 M-1**: `可信` 谓词**自身**的 null 兜底缺失 |
| 4 | **Spec B 三处自相矛盾** | 🟡 **半闭环** —— **散文全改对, Tasks 与 AC-4 没跟** (M-3 / M-4) |
| 5 | **Spec C AC-3 恒红** | ❌ **反向过冲** —— 恒红从 cache 路径**搬到** live 路径 (C-D) |

**R4 遗留的 Major (R5 独立核实)**:
- deadline × 可达性轴冲突 → ❌ **未闭环** (C-C a)
- deadline 默认值致大仓恒红 → ❌ **未闭环** (C-C b)
- Spec 文本 vs 现实漂移 → ❌ **未闭环** (M-8)

---

## 收敛状态

**R4 → R5: 未收敛。** 但**收敛仍是单调的**, 且**轴仍然正确** (5/5 一致: 不需第六次换轴)。

| 轮 | 剩余缺陷的量级 |
|----|---------------|
| R1 | 药方**机制上自我拆台** (换轴) |
| R2 | 新轴上的**边界条件** |
| R3 | **公式两端都错** |
| R4 | 分类表的空格 + 一条 ∃-子句 + 两处文本不同步 |
| **R5** | **公式对了, 但它的上游数据不存在** (C-A) + **同一 fail-open 病在另外两个谓词上复发** (C-B / M-1) + **新引入的机制自造恒红** (C-C) + **baseline 前提是假的** (C-E) |

### R5 的元教训 (最重要的一条)

> **R1-R4 反复打磨 F4′ 的裁决公式, 但从未问过: 「这个公式要裁决的 `parity` 值, 真的会被生成出来吗?」**
>
> 答案是: **对 detached-HEAD 子模块 (子模块的规范常态), 不会。** 一个完美的裁决公式, 裁决的是一个**从不存在的输入**。
>
> **审计的注意力被公式吸住了 —— 因为公式是文档里唯一能逐字推演的东西。而数据生成层在 Spec 里根本没有对应的 F 编号。**

> **第二条**: R4 的元教训「**必须类修不能点修**」**只被点修在 `blocking_unknown` 上**。没有横向扫一遍「本 Spec 里**还有哪些谓词**是正向枚举 / 定义域不完整」⇒ **第六次复发在 `has_unreachable_remote`** (C-B), **第七次在 `可信` 的 null** (M-1)。
> ⇒ **建议 R6 前先做一次机械横扫**: 把本 Spec 每一个谓词 (`可信` / `benign_unknown` / `blocking_unknown` / `has_unreachable_remote` / `has_pending_push` / `has_unpublished_branch`) 摊成一张表, 逐个问「**定义域是否完整? 补集的默认是什么?**」—— 把「类修」从**纪律**变成**机制**。

> **第三条 (对偶过冲)**: 本 Spec 系列的**每一次**修复都在对偶方向过冲一次 (v2 `ahead` / v3 `detached_head` / Spec C cache-hit / **Spec C live-miss** / **deadline**)。C-D 与 C-C 是**同一种失误**: 只验算了要修的那一侧, 没问「**修完之后, 另一侧在健康常态下是什么值?**」
> ⇒ **机械闸**: 每条 AC 必须同时给出「**健康常态必 PASS**」与「**真故障必 FAIL**」两个 fixture (Spec C 的 AC-2「防恒绿真空」已是这个形状, 只是**没有对称地应用到 AC-3**)。

---

## 下一步 (owner 裁定)

**C-A 是范围问题, 必须由 owner 裁定** (扩本 Spec 加 F10′ / 拆 Spec D + 显式 CAVEAT)。其余 C-B/C-C/C-D/C-E + 9 个 Major 都是**局部的公式/文本补丁**, 不改变已收敛的轴。

**R6 建议 scope** (比 R5 更窄):
1. **C-A 的裁定落地** (F10′ 或 CAVEAT + Spec D)
2. `has_unreachable_remote` 的 fail-CLOSED 映射 + `可信` 的 null 兜底 (C-B / M-1) —— **附机械横扫谓词表**
3. deadline 三态 (`deadline_skipped` 归 ① 类) + per-host 语义写死 (C-C)
4. Spec C: AC-3 单边化 + §3/AC-4 按实测重写根因 (C-D / C-E a)
5. 三份 Spec 的「0 failed」baseline 前提 + 4 条漂移通道认领 (C-E)
6. Spec B: Tasks 2.1/1.2 同步 + 词表裁定落任务 (M-3 / M-4)
7. 文档漂移: Status 头 / Audit trail / DEC → v5 (M-8 / M-9)
