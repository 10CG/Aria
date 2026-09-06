已跑完 `Step 0` 机械扫描 (`scan.py --output .aria/state-snapshot.json`, **exit 0**, `errors[] = []`, snapshot schema 1.0)。

先说结论, 因为它和你的描述对不上:

> **本仓当前没有「origin 已推 / github 落后」的漂移。** 主仓 + `aria` + `standards` 三个仓在 `origin` 和 `github` 上**两端 SHA 完全一致**, `gitlink_integrity` 六对全 `ok`, `has_pending_push = false`。而且**不存在 aria-plugin v1.15.0** —— 插件版本 SOT 现在是 **v1.69.1**。你记的那次发布, 在当前工作树里找不到对应物。
>
> 唯一一处 remote 不对称是 **`aria-orchestrator` 的 `feature/m6-cost-model-telemetry` 分支在 `github` 上没有 tracking ref** —— 这条不属于你说的那次发布 (它是另一条在飞的轨), 详见下面第 8 区块。

下面是完整扫描结果。

---

## 📍 当前状态
───────────────────────────────────────────────────────────────
- 分支: `feature/a1-entry-claim-duplicate-work-guard` (与 `origin/...` 同步, ahead 0 / behind 0)
- 主仓 HEAD: `5d9b568` — `docs(handoff): §3 第 1 条补 AB 会话运行守则`
- 模块: Aria meta-repo (子模块 `aria` / `standards` / `aria-orchestrator`)
- Phase·Cycle: UPM 未配置 ⇒ 无 cycle 字段; 按 OpenSpec 看在 `a1-entry-claim-duplicate-work-guard` 的 **B.2 (31/40)**
- 变更文件: 4 (3 个 dirty 子模块 gitlink + 1 个 untracked 目录)
- 关联 OpenSpec: `a1-entry-claim-duplicate-work-guard` (approved, active)
- 上次 handoff: `2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (**0.8h 前**, via pointer) — 已读, 其 §6 优先级已并入第 10 区块
- 中断状态: `.aria/workflow-state.json` = `completed` (2026-09-02 的 `linked-issue-field-availability` 周期), 忽略, 不提示 Resume
- git 层操作: `none` (无暂停中的 rebase/merge/cherry-pick)

## 📊 变更分析
───────────────────────────────────────────────────────────────
- 变更类型: other ×4 (code 0 / test 0 / docs 0 / config 0)
- 复杂度: **Level 2**
- 架构影响: 否 | 测试覆盖: 否
- Skill 变更: **未检出** (`skill_changes.detected = false`) ⇒ 本次无 Rule #6 AB 触发
- ⚠️ 三个 dirty 子模块指针 (`aria` / `standards` / `aria-orchestrator`) 是**有意保持**的 —— 上次 handoff §0 明写 gitlink bump 归 TASK-038/8.2, **不要 `git add`**

## 📄 需求状态
───────────────────────────────────────────────────────────────
- 配置: 已配置
- PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved, 归一为 pending)
- User Stories: 共 **21** — done 17 / in_progress 2 / approved 1 / pending 1
- 优先项: US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)

## 🏗️ 架构状态
───────────────────────────────────────────────────────────────
- `docs/architecture/system-architecture.md` 存在, status **Active**, 最后更新 **2026-09-02** (3d)
- 需求链路: **完整** (`chain_valid = true`, 双 PRD 上溯 v1 + v2)

## 📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
- 活跃变更: **7** (全部 approved)
- 已归档: **142** | 待归档: **0**
- ⚠️ 设计未实施 (`design_deferred`) **5 个**:
  - `aria-2.0-m6-release-closeout` — approved, 41/41 未勾, staleness **103d**
  - `aria-2.0-m7-agent-lifecycle` — approved, 18/18 未勾, staleness 65d
  - `aria-2.0-m6-cost-model-telemetry` — approved, 25/38 未勾, staleness 58d
  - `aria-2.0-m6-e2e-resilience` — approved, 25/40 未勾, staleness 55d
  - `aria-2.0-m7-fleet-aggregation` — approved, 20/20 未勾, staleness 48d

## 🛡️ 审计状态
───────────────────────────────────────────────────────────────
- 审计系统: **enabled**, mode = `convergence`, max_rounds 5
- 活跃检查点: `post_spec` / `post_planning` (其余 off)
- 上次审计: `pre_merge` **R5 PASS** (2026-09-02T18:10Z, spec `linked-issue-field-availability`) — 但 **`converged = false`** (全集未稳定, max_rounds 耗尽)。这条仍挂着待 owner 的三选一降级裁决, 非阻塞但别当已收敛。

## 🔧 自定义检查
───────────────────────────────────────────────────────────────
**14 / 14 全 OK, 0 FAIL, 0 STALE** —— 逐条:

`issue-cache-freshness` ✅ · `silknode-contract-deferral-expiry` ✅ (superseded_by_split) · `m6-version-badge-match` ✅ (badge=1.69.1) · `m6-claude-md-version` ✅ (2.0.0) · `m6-arch-doc-stale` ✅ (age=3d) · `i18n-readme-translation-currency` ✅ (3 份 @1.69.1) · `claude-md-changelog-free` ✅ (151 行 / 13316 B) · `coordination-gate-invocation` ✅ (近期 7 次真实 run_gate) · `config-template-key-currency` ✅ (10 键 0 deprecated) · `plugin-cache-currency` ✅ (installed 1.69.1 = SOT) · `main-project-version-consistency` ✅ (1.7.5, 9 个引用点全一致) · `forgejo-app-token-liveness` ✅ (2 枚 token 活性正常) · `linked-issue-field-availability` ✅ · `plugin-version-arch-docs-match` ✅

> 注意 `m6-version-badge-match` 与 `plugin-cache-currency` 都报 **1.69.1** —— 这是你问题里 "v1.15.0" 对不上的机械旁证。

## 🔄 同步状态 — **这是你要的那块**
───────────────────────────────────────────────────────────────
- 当前分支: `feature/a1-entry-claim-duplicate-work-guard` (最新, 与 `origin/feature/a1-entry-claim-duplicate-work-guard` 同步)
- 远程引用: **1m 前同步** (`remote_refresh` 本轮 8 条 leg 全部 `fetch_ok = true`, `skipped_count = 0`, 证据窗内 ⇒ 全部 `evidence_grade = fresh`)
- 强制远程集 (`enforced_remotes_resolved`): **`origin`, `github`** (无只读排除)
- 待推送: **无** (`has_pending_push = false`) | 不可达远程: **无** (`has_unreachable_remote = false`)

### 🌐 多远程一致性

| 仓 | 分支 | 本地 HEAD | origin | github | 判定 |
|---|---|---|---|---|---|
| 主仓 `.` | `feature/a1-entry-claim-duplicate-work-guard` | `5d9b568` | `5d9b568` **equal / fresh** | `5d9b568` **equal / fresh** | ✅ 一致 |
| `aria` (aria-plugin) | 同名分支 | `ab3dbd0` | `ab3dbd0` **equal / fresh** | `ab3dbd0` **equal / fresh** | ✅ 一致 |
| `standards` | 同名分支 | `bb5d375` | `bb5d375` **equal / fresh** | `bb5d375` **equal / fresh** | ✅ 一致 |
| `aria-orchestrator` | `feature/m6-cost-model-telemetry` | `92acce5` | `92acce5` **equal / fresh** | ❓ **unknown** (`no_local_tracking_ref`) | ⚠️ 见下 |

**gitlink 完整性** (主仓已发布 gitlink 在各 remote 的子模块侧是否可达): 6 对 (2 remote × 3 子模块) **全部 `ok`**, 零 `orphaned` / 零 `orphan_unverified` ⇒ 从任一 remote `clone --recursive` 都不会断。

`overall_parity = **true**`。

### ⚠️ 唯一一处不对称: `aria-orchestrator` 在 github 上没有该分支的 tracking ref

- 判定细节: `parity = unknown`, `reason = no_local_tracking_ref`, `evidence_grade = fresh`。
- 按推荐规则 1.35 的 dispatch, 这一档归 **benign unknown**, 规则**不触发** drift 告警; 规则 1.36 (`has_unpublished_branch`) 要求 `evidence_grade != fresh`, 也不触发。所以工具层面它不算"落后"。
- 但**诚实地讲**: 本轮对 `(aria-orchestrator, github)` 的 fetch 是**成功且新鲜的** (23:21:48Z), fetch 成功之后本地依然没有 `refs/remotes/github/feature/m6-cost-model-telemetry` —— 最可能的解释就是**这个分支从来没推到 github**。这是**推断, 不是测量**, 因为 snapshot 只给"没有 tracking ref", 不给"远端也没有"。
- 这条不属于你说的那次发布: 它是 M6 遥测轨 (`feature/m6-cost-model-telemetry`) 的分支, 上一份 handoff §7 已标注为"另一轨, 本 session 未动"。

### 🔴 一条要提醒你的裁决层局限

`overall_parity` 报 `true` 的同时, 上表里存在一个 `unknown` 的 (remote, repo) 对。这正是 **Aria#176** 已在册的形状 (AC-5 一致性检测未排除/未点名本仓某 remote 上不存在的分支)。所以: **别把 `overall_parity: true` 读成"每个 remote 的每条分支都齐了"** —— 它的准确含义是"至少有一条新鲜的 equal 正证据, 且没有任何 behind/diverged/阻断性 unknown"。

### 📝 README 版本一致性
- root `README.md`: 存在 (未提取到版本号)
- `aria` 子模块: README **1.69.1** = plugin.json **1.69.1** ✅ 一致

### 📦 插件依赖
- `standards` 子模块: 已注册 ✅ 已初始化 ✅

### 🔗 Forgejo 配置检查
- 检出 Forgejo remote (`forgejo.10cg.pub`), 但 **`CLAUDE.local.md` 的 `forgejo:` 配置块缺失** (`config_status = missing`)
- 建议: 需要时跑 `/forgejo-sync` 引导创建 (非阻塞)

### 🔀 多终端协调 (advisory)
- `refs/aria/coordination` 本轮 fetch 成功 (25s 前, 未降级)
- `tracks_multibranch.collision.kind = **self_multi_container**`, 冲突组 `["dev-claude", "simonfishgit/dev-claude"]` —— 同一容器的两种 git 身份串被当成两个 owner (即 **Aria#193** 的形状), 不是真的两个人在抢。
- 本次**没有调用** `phase1_gate`: 触发条件是"用户确认进入 Phase B"时才调, 你这次是只读状态查询; 本会话也不持 active claim, 故也没跑 `--heartbeat-only`。若你要续做本轨, 顺序必须是**先 fetch 再刷 heartbeat** (见第 10 区块)。

## 🎫 Open Issues
───────────────────────────────────────────────────────────────
- 平台: Forgejo — **open 47** (来源: cache, 4m 前)
- 分仓: `10CG/Aria` **20** · `10CG/aria-plugin` **20** · `10CG/aria-standards` 5 · `10CG/aria-orchestrator` 2
- 🔴 **这个 47 是被截断的**: config `issue_scan.limit = 20`, 而 Aria 与 aria-plugin **恰好各报 20** = 顶到上限, 且 snapshot **零截断标记**。真实总数更高 (上一 session 实测四仓合计 65)。这是上次 handoff §2 的 M2, **至今未开单**。
- 与本次问题直接相关的两条:
  - **Aria#165** — GitHub 镜像漏推第三次复发 (子模块服务端合并 + gitlink bump 无序 → orphaned gitlink)。你描述的正是这个类别的故障, 只是这一轮**没有复现**。
  - **Aria#176** — AC-5 一致性检测未排除本仓不存在的 remote (上面那条裁决层局限)。

---

## 🎯 你要的修复命令

### 1. 针对 origin/github parity: **当前不需要修复命令**

三个仓两端 SHA 全等。**别为了"保险"随手推一次** —— 在已经一致的状态下推送不会有任何变化, 但会让你少做那一步真正有价值的事: 核验。要确认的话跑这个 (只读):

```bash
# 主仓 + 两个已同步子模块 — 逐 remote 独立取 SHA, 与本地比对
BR=feature/a1-entry-claim-duplicate-work-guard
for R in origin github; do
  echo "== main/$R:  $(git ls-remote "$R" "refs/heads/$BR" | cut -c1-7)"
done
echo "   main/local: $(git rev-parse --short HEAD)"

for S in aria standards; do
  for R in origin github; do
    echo "== $S/$R:  $(git -C "$S" ls-remote "$R" "refs/heads/$BR" | cut -c1-7)"
  done
  echo "   $S/local: $(git -C "$S" rev-parse --short HEAD)"
done
```

预期: 6 行远端 SHA 与 3 行本地一一对应相等。

### 2. 针对 `aria-orchestrator` 的 github 缺口 (先确认, 再决定推不推)

```bash
# 【1】确认 github 上到底有没有这条分支 (只读)
git -C aria-orchestrator ls-remote github refs/heads/feature/m6-cost-model-telemetry
#   有输出 → 只是本地缺 tracking ref, 跑 git -C aria-orchestrator fetch github 即可, 不用推
#   无输出 → 确实没推过, 走【2】

# 【2】确认要镜像时才推 (这是另一条在飞的轨, 推之前先确认它归你处置)
git -C aria-orchestrator push github feature/m6-cost-model-telemetry

# 【3】推后逐 remote 核验 — 不要信 push 回执
git -C aria-orchestrator ls-remote origin refs/heads/feature/m6-cost-model-telemetry
git -C aria-orchestrator ls-remote github refs/heads/feature/m6-cost-model-telemetry
git -C aria-orchestrator rev-parse HEAD
```

### 3. 如果你真正想做的是"发一版插件并同步双远程" (v1.70.0)

那不是修 parity, 是走发布流程。硬约束两条 (CLAUDE.md, 根治 Aria#165), 请照抄:

```bash
# 子模块合并一律本地做 —— 禁用 Forgejo Web UI / API 的 "Do: merge"
git -C aria checkout master && git -C aria merge --no-ff feature/a1-entry-claim-duplicate-work-guard
git -C aria push origin master && git -C aria push github master
# 推后逐个 ls-remote 核验, 全部一致才算推成功
git -C aria ls-remote origin master; git -C aria ls-remote github master; git -C aria rev-parse HEAD
# 之后才 bump 主仓 gitlink (顺序反了会造 orphaned gitlink)
```

⛔ 但**现在还不能开始**: 按 Spec 执行序是 `8.1 CHANGELOG + 版本 SOT 5 文件 → 8.4 aria merge/双推/tag → 8.2 主仓 16 版本点 + gitlink bump`, 而 Group 8 整体**待 Rule #6 AB 过关**。见下。

---

## 🎯 推荐工作流

置信度中等 (你的问题是只读查询, 但仓库状态指向一条明确的在制主线)。请选:

**【1】(推荐) 续做 `a1-entry-claim-duplicate-work-guard` — 31/40**
- 先决条件卡在**会话级前置**: `ARIA_COORDINATION_NO_PUSH` 实测 **UNSET**, 会话内 `export` 补不上 (只影响那一个 Bash 子进程, 改不了 subagent 的继承环境)。
- 处置: 由你以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话 → 经 `/skill-creator` 跑 Rule #6 AB 六套件 → 结果落 `ab-results/2026-XX-XX-v1.70.0-a1-entry-rule6/<skill>/`。
- AB 过关后依次解锁: TASK-036 (7.6) 依赖解除 → Group 8 发版 (vNEXT = **1.70.0**)。
- ⚠️ 进本轨前先刷 heartbeat, **顺序是先 fetch 再刷** (反了会被强制 fetch 冲掉本地未推的 commit, 09-05 已实证):
  ```bash
  git fetch origin '+refs/aria/coordination:refs/aria/coordination'
  python3 -B aria/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "a1-entry-claim-duplicate-work-guard" \
    --phase A.1 --heartbeat-only --repo-path /home/dev/Aria
  ```
  本轨 sweep 死线 `2026-09-06T21:40Z`, 时间充裕。

**【2】补齐 `aria-orchestrator` 到 github** — 走上面"修复命令 2"的三步 (先 ls-remote 确认, 再推, 再逐 remote 核验)。属另一轨, 动之前确认归属。

**【3】收掉两条已识别的技术债**
- `issue_scan.open_count` 静默截断 (本轮 snapshot 报 47, 两个仓恰好顶到 `limit=20` 且零标记) —— **仍未开单**, 与 Aria#173/#182「证据越少越宽松」同族。
- aria-plugin#169 `resilient_push` non-FF 恢复路径结构必失败 —— 已开单未修, 影响 `acquire_claim` + `heartbeat` 两条写路径, 修复面在 `lib/failure_handlers.py` + `lib/coordination_ref.py:1339`。

**【4】只看状态, 不启动工作流** — 本回答即全部内容, 到此为止。

也可以自定义组合 (例如 `B.2 + C.1`)。你选哪个?
