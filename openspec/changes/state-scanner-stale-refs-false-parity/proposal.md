# Proposal: state-scanner 陈旧 ref 假同步修复 — 「新鲜度靠获取, 不靠测量」

> **Status**: **Draft v4** (v1 → R1 FAIL [机制自拆台] → v2 → R2 FAIL [边界条件] → v3 → R3 FAIL [∀ 公式两端都错] → **v4 + 拆 Spec**) → 待 post_spec **R4**
> **Level**: 3 (Full — 十步循环统一入口的裁决逻辑 + collector 编排 + 网络行为 + 影响所有采用者的配置 + snapshot schema)
> **Created**: 2026-07-12 | **v4 修订**: 2026-07-12 (R3 的 2 Critical + 拆分)
> **Decision**: [DEC-20260712-001](../../../docs/decisions/DEC-20260712-001-state-scanner-stale-refs-false-parity.md)
> **Audit trail**: [`.aria/audit-reports/post_spec-R1-R2-...-aggregated.md`](../../../.aria/audit-reports/post_spec-R1-R2-2026-07-12T1850Z-state-scanner-stale-refs-false-parity-aggregated.md)
> **Track**: `state-scanner-stale-refs-false-parity`
> **Target**: aria-plugin (子模块 `aria/`)

> ### 🔀 范围已拆分 (owner 2026-07-12, 5/5 agent 一致建议)
> | Spec | 内容 | 与本 Spec 的关系 |
> |------|------|------------------|
> | **[state-scanner-snapshot-stderr-secret-leak](../state-scanner-snapshot-stderr-secret-leak/proposal.md)** (L2) | Rule #7: 裸 git stderr → 分类枚举 | **应先落地** —— 本 Spec 的 F3′ 把该暴露面放大 N×M 倍。本 Spec **复用**它提炼出的分类器。 |
> | **[state-scanner-issue-cache-freshness-assertion](../state-scanner-issue-cache-freshness-assertion/proposal.md)** (L2) | `issue-cache-freshness` 重定义 + `generated_at` 字段 | **零代码路径重叠**。原「四者同根 = collector 顺序」的叙事**是错的** (R1 已论证): F3′ 是「消费者早于生产者」的真顺序 bug; 它是「外部反向证据被放进被审计进程内部」的设计混淆。 |
> | **本 Spec** (L3) | F1′/F2′/F3′/F4′/F5′/F6′/F9′ —— **不可再拆的核心机制** | fetch 无降级 = 白烧网络; 降级无 fetch = 恒红; F9′ 不同步落地 = 上线当天就制造新的自相矛盾。 |

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

### F3′ — 新鲜度靠获取 (`remote_refresh`)

`coordination_fetch` 泛化为**并行 fetch 所有 enforced remote** (主仓 + 全部子模块), **改名 `remote_refresh`**, 落点 **Phase 0.5** (`collect_git_state` 之前)。

- **`fetch_ok` 锚定 Fetch 1** (#141 归档 Spec 的 two-fetch 语义): Fetch 1 = `+refs/heads/*` (**载重**), Fetch 2 = `refs/aria/coordination`。**benign-missing 的 coordination ref 不得置 `fetch_ok=false`** —— github/子模块远端**几乎必然没有**该 ref, 否则**每个非-origin remote 恒 false ⇒ 恒红**。
- **并发**: 全并行, **per-host 上限** (默认 ≤4/host; sshd `MaxStartups` 默认 `10:30:100`, 超限会**随机丢连** ⇒ 不可复现的间歇性假警报)。丢连**重试 + 退避** (与真 auth/network 失败区分)。
- **全局 deadline** (R3-M11): `refresh_deadline_seconds` (默认 **15s** ≈ 当前 scan 全程)。**网络成本必须有硬上界** —— `ceil(N/cap) × slowest` 中 N 无界 (采用者 20 子模块 × 3 remote = 60 腿 ⇒ 105s/scan)。到点未完成的 leg ⇒ 标 `not_refreshed` (走既有降级路径, **零新机制**), 不阻塞 scan。
- **非交互契约**: `_common._run` (L344-366) 有 `capture_output=True` 但**无 `stdin=DEVNULL`**, env **只有 `LC_ALL`**。fetch 路径必须 `stdin=DEVNULL` + `GIT_TERMINAL_PROMPT=0` + `GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=N"`; auth 失败**只提示一次**。
- snapshot 记 per-remote `{fetched_at, fetch_ok, error_kind}`。**`error_kind` 是枚举** (复用姊妹 Spec 的分类器), **永不含 stderr 原文**。
- **`fetched_at` 只在 Fetch 1 真成功刷新时推进** —— stale-serve/degraded 路径 (`coordination_fetch.py:379-390` 现返回 `cached:True` + **任意陈旧**的 `last_fetch_at`) **不得**推进它。
- **TTL 命中时逐 remote replay** per-remote map (现 cache schema 只有 3 个标量键, 无 per-remote 结构 — R3-M10)。

### F1′ — 两个正交轴 (v4 关键修正, R3-M9)

> **v3 把「可达性」与「新鲜度」挤在一条路径上。** 后果: github token 刚过期, 但 200s 前上次 fetch 成功过 ⇒ `200s < 300s window` ⇒ 判「可信」⇒ 不降级 ⇒ **不记 reason** ⇒ `has_unreachable_remote=false` ⇒ 不可达告警**不响**。凭据坏了 5 分钟, snapshot 一声不吭。

**两轴各自成信号, 不互相 gate**:

| 轴 | 定义 | 作用 |
|----|------|------|
| **可达性** | `fetch_ok`(本次尝试) | `fetch_ok == false` ⇒ **永远**记 `error_kind` + 按 network 类置 `has_unreachable_remote`。**与窗口无关。** |
| **新鲜度** | `可信(r) := now - fetched_at <= freshness_window` (默认 300s > TTL 30s) | **只** gate parity 降级。 |

**降级只作用于正证据**:

| 原 parity | 不可信时 | 理由 |
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
| **blocking unknown** | `not_refreshed` (新增) / `network_timeout` (L260,266) / `auth_failed` (L262) / `not_found` (L264) / `rev_list_failed` (L198) / `rev_list_parse_failed` (L202,207) / **`parse_error` (L281)** | **能** (或: 是真错误) | 「我们**不知道**真相, 而这是可以知道的」 | **是** |
| **benign unknown** | `detached_head` (L169,188,250,293) / `shallow_clone` (L173,289) / `no_local_tracking_ref` (L181) / `remote_branch_missing` (L276) | **不能** (fetch 一万次也变不成 equal) | 「这个问题**不适用**」 | **否** (但也不提供正证据) |

> ⚠️ **`parse_error` 是本 Spec 起草时第四次「漏格」的实例** —— v4 初稿的两个桶里都没有它 (owner 自查 grep 时发现)。这再次印证 R3-C5 的方法论: **不能凭印象列举, 必须 grep 出全集逐格填。** 任何新增 `reason` 枚举**必须**同时归入某个桶 (加一条机械检查: 断言 `blocking ∪ benign == 代码中所有 reason 赋值`)。
>
> 附带发现: `state-snapshot-schema.md:499` 的 enum 列表**漏了 `rev_list_failed` / `rev_list_parse_failed`** (schema doc 与代码已 drift)。

**v5 公式** (R4 五方发现的合成解):
```
# benign 不是同质的 —— 必须按「fetch 能否改变它」再分一层 (代码实测):
benign_unknown(r) := parity(r) == "unknown" ∧ (
        reason(r) ∈ {detached_head, shallow_clone}                          # ① fetch-无关 (multi_remote.py:169/173
                                                                            #    在读任何 ref 之前就返回) ⇒ 恒 benign
     ∨ (reason(r) ∈ {no_local_tracking_ref, remote_branch_missing}          # ② fetch-依赖 (:181 是"读 ref 失败"才返回)
          ∧ 可信(r))                                                        #    ⇒ 只有本次刷新成功才算 benign;
   )                                                                        #    否则「没这个 ref」可能只是「我们没 fetch 过」

blocking_unknown(r) := parity(r) == "unknown" ∧ ¬benign_unknown(r)          # 🔴 fail-CLOSED 兜底 (见下)

overall_parity = true  iff
      enforced_set ≠ ∅                                              # 非空 (防 vacuous true)
   ∧  (∃ r ∈ enforced: 可信(r) ∧ parity(r) == "equal")              # QA-C1 正证据要求 (可信只需在此出现)
   ∧  (∀ r ∈ enforced: parity(r) ∉ {behind, diverged}
                        ∧ ¬blocking_unknown(r))                     # ⚠️ ∀ 里不再有独立的 可信(r) 项
```

> **为什么 `可信(r)` 必须从 ∀ 子句里删掉** (qa-engineer R4 实证): 它在那里**冗余且有害** ——
> - 对本来 `equal` 的 r: 不可信时 **F1′ 的降级已经**把它变成 `unknown` + `not_refreshed` (∈ blocking) ⇒ `¬blocking_unknown(r)` **已经**挡住了, 不需要再挡一次;
> - 对 `behind`/`diverged`/`ahead` 的 r: 降级明确**不覆盖**它们 (下界证据依然为真) ⇒ 新鲜度对它们**没有正确的语义**;
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
- **「分支从未推到任何 remote」不压在 `overall_parity` 上** —— 它该有自己的 flag (`has_unpublished_branch`), 由 `multi_remote_drift` 单独处理。**把三种语义挤进一个 bool 正是它今天撒谎的原因。**
- read-only remote **不参与** `overall_parity`。

### F5′ — enforced remote 集合

- **消费既有键**, 不发明新键: `enforced_remotes` / `read_only_remotes`。
- 🔴 **命名空间必须对齐已发布的跨 skill 契约** (R3-M2): `phase-c-integrator/SKILL.md:574` 已把**顶层 `multi_remote.*`** 当公共契约 (skill 级为 null 时继承顶层)。state-scanner **不得另立门户** —— 否则「state-scanner 认定该强制的 remote 集合」≠「phase-c-integrator 认定该强制推送的 remote 集合」= **本 Spec 的病在跨 skill 层复现**。
- **read-only 排除必须同时作用于** `overall_parity` **和** `has_unreachable_remote` **和** `multi_remote_drift` 触发 (R3, backend-architect) —— 只挂 `overall_parity` 会让「我不关心它」的 remote 抖一下网络仍全局告警。
- **删除 `fetch_all: false` 旋钮** (R3, backend-architect): `enforced_remotes: ["origin"]` 已能达到同样效果。**不要为收窄 fetch 范围发明第 4 个键** —— 本 Spec 存在的理由之一正是「死配置键 + 假文档」, 别用一次修复换一次同类 drift。
- **修假文档** `sync-detection.md:515`。
- **Impact**: 已按该文档设过 `enforced_remotes` 的采用者, 其配置**今天是惰性的**; 本 Spec 让它承重 ⇒ **直接改变其网络行为**。CHANGELOG 必须显著标注。

### F2′ — 退役 FETCH_HEAD-mtime **实现** (保留新鲜度**概念**)

mtime 路径整体退役 (repo 全局单值, 当 fallback 都不合格); 新鲜度由 `fetched_at` + `freshness_window` 承载。**无条件清扫** ≥8 处 SOT (⚠️ v2 曾把条件写反成「若保留才清扫」—— **退役意味着它变死配置键, 清扫更必须**)。

> ⚠️ 这推翻了 owner v1 的「24→1」决策 (其前提被 R1 证伪: age 是 repo 级, age≈0 对**所有** remote 都不触发)。R2/R3 五位一致确认推翻成立。

### F6′ — collector 改名 + 可关闭性契约

`coordination_fetch` → **`remote_refresh`** (Phase 0.5)。SKILL.md **写死契约**: 「关闭它 ⇒ 所有 parity 变 unknown」—— 防后人以为它归 `coordination.*` 配置管 (本仓 `.aria/config.json` 里正有 `coordination.enabled: true`), 关掉 coordination 静默摧毁 parity 真值。

**改名波及 ≥11 个引用点** (R3-N3): `normalize_snapshot.py` / `renderers/track_board.py` / `lib/coordination_ref.py` / `collectors/__init__.py` / `scan.py` / `tests/test_coordination_fetch.py` / `tests/test_p1_layer_h.py` / `SKILL.md` / `state-snapshot-schema.md` / `phase-1-collectors.md` / `docs/rule9-5layer-matrix.md`。

### F9′ — `sync.py` 平行计算点 (OQ-E)

`_collect_current_branch` 与 `submodules[].drift` 独立算 ahead/behind, 无 `fetch_ok` 概念 ⇒ 与 `multi_remote` **在同一 snapshot 自相矛盾**。

**两条路径必须在 Phase A 二选一** (R3, backend-architect: **这条路径的错误方向选择历史上就是数据丢失事故的成因**, `sync.py:312-328` 的 US-008 directional guard):
- (a) 让它**消费** per-remote 新鲜度 (不可信 ⇒ 标注/降级)
- (b) 显式声明「本地视角、不保证新鲜」并在输出区块区分

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
> **判据**: **0 failed** ∧ **无既有绿测试转红** ∧ **新增测试数 = N** (不用绝对总数)。

- **AC-1**: remote 不可信 + 真实落后 → `parity != "equal"` 且 **`reason == "not_refreshed"`** (显式断言走过 F1′ 路径, 防死代码 ship)。
- **AC-2**: origin 刷新成功且 equal + github fetch 失败且真落后 → github `unknown` + **network 类 `reason`** + `overall_parity: false`。
  > **fixture 必须钉死**: github **无 `freshness_window` 内的成功 `fetched_at`** (否则不触发降级 ⇒ green/red by accident)。**用 mock `_run` 注入精确 stderr, 不打真实不可达域名** —— 实测 TLS 握手失败的 stderr 是 `gnutls_handshake() failed`, **不落在任何已知分类 pattern 里** ⇒ 真实网络构造会环境相关地误判。
- **AC-3 (性能预算)**: mock `_run` 断言 **每个 (repo, remote) 恰好被 fetch 一次** (集合/计数不变量, **不是 strict order** —— 真并行下调用序是线程调度决定的, 断言序会成为新 flaky 点)。wall-clock 仅作 **spike 记录, 不作 CI 硬 gate**。
- **AC-4 (无回归)**: 见上方判据。
- **AC-5 (snapshot 自洽)**: `tracks_multibranch` 中**与 HEAD 同分支** (`branch` == HEAD upstream) 的 track commit 对 HEAD 不可达时 ⇒ `overall_parity == false` 或该 remote `reason` 非空。(**不能用「任意 HEAD 不可达的 commit」** —— 任何有其它活跃分支的仓库本来就有 ⇒ 健康仓假红 + 误触设计闸。)
- **AC-6 (子模块覆盖)**: 子模块 remote 从未 fetch ⇒ **不得**提供 `equal` 正证据。
- **AC-7 (降级只作用于正证据)**: 不可信且 `behind` **不得**降级为 `unknown`; 不可信且 `ahead` **不得**让 `has_pending_push` 变 false。
- **AC-8 (`ahead` 不阻断, 但也不是正证据)** — **owner 裁定 2026-07-12 (DEC)**:
  `overall_parity` 的语义 = 「**本地与远端一致**」。有未推送 commit 的仓库**确实不是已同步的** ⇒ 报 `false` 是**诚实**的, 且下游给的 `push` 建议**是对的**。**与现有代码 (`has_equal_evidence` 要求 `equal`) / golden fixture / AB rubric 三者一致 ⇒ blast radius 最小。**
  > ⚠️ **v4 的 AC-8 措辞把「健康」与「已同步」偷换了概念** (R4 tech-lead C7 / code-reviewer X-5 双方都指出它与 AC-12 **字面互斥**)。一个有未推送 commit 的仓库**是健康的, 但不是已同步的**。
  > **本 Spec 修的是「落后时假绿」** (危险: 会在旧代码上开工、重复别人的劳动 —— 本 session 即受害者), **不是「领先时假红」** (领先不会导致重复劳动)。两者不可混为一谈。
  >
  > **断言**: `origin=equal + github=ahead` 的仓库 (golden fixture 场景) ⇒ `overall_parity: true` ∧ `has_pending_push: true`。**前提: ≥1 个 remote 为 `可信 ∧ equal`。**
  > 单 remote 且 `ahead` ⇒ `overall_parity: false` (无正证据) + `has_pending_push: true` + 建议 `push` —— 见 **AC-12**, 二者现已**自洽, 不再互斥**。
  >
  > tech-lead 的反方论据 (「单 repo+单 remote+未推送 = 中位数采用者, 按『健康常态该是什么值』判据答案应是 true」) 记录在案 —— 若未来 Phase B dogfood 实测告警疲劳成立, 可重开此裁定。
- **AC-9 (TTL 不复发旧病)**: 30s 内连跑两次 scan ⇒ 第二次 TTL 命中 ⇒ **不降级** + 两次 snapshot diff == 0; **fetch 失败 + stale cache ⇒ `fetched_at` 不得推进**。
- **AC-10 (F9′ 平行计算点)**: origin fetch 失败时, `sync_status.current_branch` 与 `sync_status.multi_remote[origin]` **不得自相矛盾**。**断言字段由 OQ-E 的裁定决定** (不能停留在「不得自相矛盾」的 prose 谓词)。
- 🆕 **AC-11 (benign unknown 不阻断 —— 防 R3-C5 恒红回归)**: **detached-HEAD 子模块** + 全部 remote 刷新成功 + 主仓 equal ⇒ `overall_parity` **仍为 true**。**本仓可直接 dogfood** (`aria` 子模块正是 detached HEAD)。
- 🆕 **AC-12 (无 vacuous true —— 防 R3-N1 假绿回归)**: 参与集为空 (零 remote / 全部 read-only) ⇒ `overall_parity` **必须 false**; 无任何 `可信 ∧ equal` 的 remote (如单 remote 且 `ahead`) ⇒ **必须 false**。
- 🆕 **AC-13 (可达性与新鲜度两轴独立 —— 防 R3-M9)**: remote 本次 fetch 失败 (auth) 但 `fetched_at` 仍在窗口内 ⇒ `parity` **不降级** (仍 equal), **但** `error_kind` **必须记录** 且 `has_unreachable_remote` **必须 true**。

**自我否证闸**: 红测试在未修改代码上意外 GREEN ⇒ 诊断有误, 回 Phase A。修复后红测试**仍无法转绿** ⇒ **设计缺陷, 回 Phase A** (v1 的 AC-2 正是这种情况)。

---

## Open Questions (Phase A 内锁死)

- **OQ-A** — `read_only_remotes` 默认值。**倾向 `[]` (不自动推断)**: git 没有可靠的「只读」内建信号 (push URL 缺省等于 fetch URL); **误标 read-only 会吞掉真实的落后信号**, 比要求显式配置更危险 (R3: qa + backend-architect + code-reviewer 三方一致)。**必须与 AC-12 的非空护栏捆绑裁定。**
- **OQ-B** — `coordination_fetch` snapshot 块 shape。**倾向: 保留原块 (origin-only) 原样, 另开 `remote_refresh` 新块**承载 per-remote 数组 —— 原块是 **#141 归档契约** + **m7-fleet-aggregation 防御式消费清单**双重锁定, 就地改基数会同时破坏两个下游契约; 新开键 = **纯 additive** ⇒ 不 bump schema version (R3: tech-lead + backend-architect + qa 三方一致)。
- **OQ-C** — 离线 debounce。**倾向: 不造新的有状态冷却机制**。用 F1′ 的两轴拆分: 离线 ⇒ `has_unreachable_remote=true` ⇒ 让 `multi_remote_drift` **在该 flag 为 true 时不触发**, 换成一条「离线, 同步状态不可知」的降级横幅 (复用 `coordination_fetch` 现有的 `degraded` 红条先例)。**debounce 只作用于建议层, 不作用于裁决层** (让 `overall_parity` 变回 true 会重新引入假绿)。
- **OQ-D** — `freshness_window` 默认 **300s**。须 > TTL(30s) 且 > scan 全程(17.6s)。**必须在 schema doc 写明**: 「这是有意接受的**有界**陈旧容忍 (≤5min), 与本 Spec 修复的**无界**陈旧 bug 是两个量级 —— **不要被未来审计员误认成同一缺陷复发**」。
- 🆕 **OQ-E** — F9′ 二选一 ((a) 消费新鲜度 / (b) 声明本地视角)。**必须与 OQ-A~D 同等对待** —— 这条路径直接落在 **US-008 数据丢失护栏**上, 错误的方向选择历史上就是事故成因, **不得留给 Phase B 实现者临场挑最省事的分支**。AC-10 的断言字段跟着此裁定定死。

---

## 关联

- **拆出的姊妹 Spec**: [snapshot-stderr-secret-leak](../state-scanner-snapshot-stderr-secret-leak/proposal.md) (Rule #7, **应先落地**) / [issue-cache-freshness-assertion](../state-scanner-issue-cache-freshness-assertion/proposal.md) (正交)
- **承重先例 (必读)**: `openspec/archive/2026-06-12-state-scanner-coordination-fetch-resilience` (**#141** — two-fetch 语义, `fetch_ok` 锚定依据) / `openspec/archive/2026-04-25-state-scanner-mechanical` (**AD-SSME-6** — `state-snapshot-schema.md` 才是 schema SOT; `multi_remote.py:4` 声称 git-remote-helper 是 canonical 的 docstring 是**被取代的 stale 声明**, **不得**据此把 SOT 迁回代码)
- **下游 Spec**: `aria-2.0-m7-fleet-aggregation` (Approved — 消费 `overall_parity`)
- **aria-plugin #109**: 同一失败模式的**协调层**维度; 本 Spec 是**扫描层**维度。R1 核实真 disjoint。**互补**: 即使认领点前移, 若 `sync_status` 撒谎说「已同步」, AI 照样在落后树上开工。
- **memory**: `feedback_concurrent_duplicate_audit_fetch_before_start` (本缺陷是其**工具层成因**) / `feedback_test_mock_pattern_hides_prod_bug` / `feedback_completion_signals_vs_runtime_invocation` / `feedback_probe_first_scope_reframe` / `feedback_spike_first_for_data_hypotheses` / `project_submodule_drift_direction` (US-008) / `feedback_cross_agent_verdict_independent_verify` (R3 两位 agent 对 `fetched_at` 是否在 normalize 白名单给出**相反的代码事实**, owner grep 裁决)
- **CLAUDE.md** 多远程推送段 (2026-04-10 市场滞后事故 —— 即本缺陷盲区所在)
