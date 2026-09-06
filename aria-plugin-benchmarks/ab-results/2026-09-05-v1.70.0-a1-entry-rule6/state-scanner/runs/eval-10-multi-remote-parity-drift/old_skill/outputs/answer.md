已跑完 Step 0 机械扫描 (`scan.py`, **exit 0 / `errors: []`**, snapshot schema 1.0)。先给结论, 再给完整状态。

---

## 先回答你的问题: 这次扫描**没有**证实「github 漏推」

本轮 8 条 fetch 腿全部成功 (`remote_refresh.skipped_count = 0`), 远程引用 **1 分钟前**刷新, 证据等级全是 `fresh`, 所以下面的 parity 结论是本轮验证过的, 不是陈旧缓存。

| 仓 | 当前分支 | local | origin (Forgejo) | github (GitHub) | 判定 |
|----|----------|-------|------------------|-----------------|------|
| 主仓 `.` | `feature/a1-entry-claim-duplicate-work-guard` | `5d9b568` | `5d9b568` | `5d9b568` | 两端 equal |
| `aria` (= aria-plugin) | 同名分支 | `ab3dbd0` | `ab3dbd0` | `ab3dbd0` | 两端 equal |
| `standards` | 同名分支 | `bb5d375` | `bb5d375` | `bb5d375` | 两端 equal |
| `aria-orchestrator` | `feature/m6-cost-model-telemetry` | `92acce5` | `92acce5` | — | origin equal; **github = unknown** |

- **落后 (behind) 的 remote: 0 个。** `overall_parity = true`, `has_pending_push = false`, `has_unreachable_remote = false`。
- **gitlink 完整性 6/6 全 `ok`** (2 remote × 3 子模块) —— 主仓已发布 commit 引用的子模块 gitlink 在两个远程上都可达, 从 github `clone --recursive` 不会断。
- 唯一非 equal 的一格: `aria-orchestrator` 在 **github** 上 `parity = unknown`, `reason = no_local_tracking_ref`, `evidence_grade = fresh`。含义是「本地根本没有 `github/feature/m6-cost-model-telemetry` 这个 tracking ref」, 大概率是这条分支**从没往 github 推过**, 不是「推过但落后」。按判据这属于 benign unknown, 不阻断 `overall_parity`, 我也不会据此给你方向性的 pull/push 建议。

### 三点需要你核对的偏差

1. **版本号对不上。** 当前 aria-plugin 版本是 **1.69.1** (`plugin.json` / README badge / 架构文档三处一致, 相关 custom check 全 OK), 仓里没有任何 `1.15.0` 的痕迹, 下一个待发版本按上次交接是 `1.70.0`。你说的 "v1.15.0" 可能是记混了。
2. **子模块指针更新这一步还停在工作区, 还没提交, 更没推。** `git status` 显示 `aria` / `standards` / `aria-orchestrator` 三个子模块 dirty —— 工作区 checkout 的 commit 与主仓记录的 gitlink 不一致 (例: `aria` workdir `ab3dbd0` vs 主仓记录的 gitlink `7dd0135`)。也就是说 "gitlink bump" 尚未发生, 自然谈不上「推了 origin 漏了 github」。上一份 handoff §0 明写这三个 dirty 是**有意**的 (gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后), 所以不要 `git add`。
3. **本次 parity 只覆盖各仓「当前 checked-out 分支」, 不覆盖 master。** 如果你说的发布动作发生在 master 上, 这次扫描看不到它 —— 需要切到 master 再扫, 或直接用下面的只读命令核。同理, **tag 空间完全不在检测范围内** (`multi_remote` 是 RM-11 有意的 branch-reachability only), 「发版」通常还包含 tag, 那部分本扫描不作证。

另外提醒一个信任边界: `overall_parity = true` **不等于**「每个仓的当前分支在两个远程上都存在且都被验证过」—— 像上面 aria-orchestrator 那种 benign unknown 是不会把它翻成 false 的 (schema worked example: `origin=equal, github=unknown` → `true`)。

---

## 修复 / 核验命令

### 第一步 (推荐先做): 只读核验, 不信 push 回执, 逐 remote 独立取 SHA

```bash
# 主仓
git rev-parse HEAD
git ls-remote origin refs/heads/feature/a1-entry-claim-duplicate-work-guard
git ls-remote github refs/heads/feature/a1-entry-claim-duplicate-work-guard

# 三个子模块 (逐个)
for m in aria standards aria-orchestrator; do
  echo "== $m"; git -C "$m" rev-parse HEAD
  git -C "$m" ls-remote origin HEAD
  git -C "$m" ls-remote github HEAD
done

# 如果你关心的是 master 而不是当前 feature 分支
git ls-remote origin refs/heads/master; git ls-remote github refs/heads/master
git -C aria ls-remote origin refs/heads/master; git -C aria ls-remote github refs/heads/master

# tag (本扫描不覆盖, 发版要单独核)
git -C aria ls-remote --tags origin | grep -E 'v1\.(69|70)'
git -C aria ls-remote --tags github | grep -E 'v1\.(69|70)'
```

### 第二步: 只在上面核出真差异时才补推

```bash
git push github <branch>                     # 主仓补推
git -C aria push github <branch>             # 子模块补推 (aria-plugin)
git -C aria push github v1.70.0              # 只在 tag 确实漏推时
```

### 针对那格 unknown (可选, 需你先确认意图)

```bash
# 确认真要把这条 track 的分支镜像到 github 再做; 它属于另一条在飞的 track
git -C aria-orchestrator push -u github feature/m6-cost-model-telemetry
```

### 推完必做 (两条硬约束, 见 CLAUDE.md §多远程推送)

- **逐个 `ls-remote` 核验, 不信 push 回执** —— push 退出码和回执两个方向都会骗人 (假阴性诱发误 force, 半推造成镜像分叉)。全部 remote 的 SHA 与本地一致才算推成功。
- **子模块合并一律本地 `git merge` + 双推, 禁用 Forgejo 服务端 merge** —— 服务端合并的 merge commit 只在 Forgejo 生成, 本地 master 从未 fast-forward, 主仓随后 bump gitlink 就会产生 orphaned gitlink, GitHub `clone --recursive` 断裂。这正是 Aria#165「GitHub 镜像漏推第三次复发」的形状, 目前仍 open。

---

## 完整状态

### 📍 当前状态
- 分支: `feature/a1-entry-claim-duplicate-work-guard` (与 `origin/...` 同步, ahead 0 / behind 0)
- 模块 / Phase·Cycle: UPM 未配置 (`upm.configured = false`) —— 无 cycle/phase 数据
- 变更: 4 项 (未暂存 3 个 dirty 子模块指针 + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/`); 暂存区空
- 关联 OpenSpec: `a1-entry-claim-duplicate-work-guard` (approved)
- 上次 handoff: `2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (1.0h ago, via pointer)
- git 层无暂停操作 (`operation = none`), 无冲突

### 📊 变更分析
- 类型: other ×4 (code/test/docs/config 均为 0) | 复杂度 **Level 2** | 架构影响: 无 | 测试覆盖: 无
- Skill 变更: 未检出 (`skill_changes.detected = false`) —— 本次不触发 Rule #6 AB 判据

### 📄 需求状态
- 需求体系: 已配置 | PRD 2 份: `prd-aria-v1.md` (active) / `prd-aria-v2.md` (raw "Approved" → 归一 pending)
- User Stories 21 条: done 17 / in_progress 2 (US-026, US-007) / approved 1 (US-028) / pending 1 (US-003)

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在, status **Active**, 最后更新 2026-09-02 (3 天前)
- 需求链路完整 (`chain_valid = true`, 上挂 prd-aria-v1 + prd-aria-v2)

### 📋 OpenSpec 状态
- 活跃变更 7 个 (全部 approved): `a1-entry-claim-duplicate-work-guard` / `aria-2.0-m6-cost-model-telemetry` / `aria-2.0-m6-dispatch-input-delivery` / `aria-2.0-m6-e2e-resilience` / `aria-2.0-m6-release-closeout` / `aria-2.0-m7-agent-lifecycle` / `aria-2.0-m7-fleet-aggregation`
- 已归档 142 | 待归档 0
- ⚠️ 设计未实施 5 个: `m6-release-closeout` (approved, 103d, 41/41 未勾) · `m7-agent-lifecycle` (65d, 18/18) · `m6-cost-model-telemetry` (58d, 25/38) · `m6-e2e-resilience` (55d, 25/40) · `m7-fleet-aggregation` (48d, 20/20)

### 🛡️ 审计状态
- 审计系统: enabled
- 上次审计: `pre_merge` R5, verdict **PASS**, 2026-09-02T18:10:11Z (报告 `.aria/audit-reports/pre_merge-R5-...-linked-issue-field-availability-aggregated.md`; `converged` 标记为 false, 属该轮聚合口径)

### 🔧 自定义检查
14 项全部 ✅ PASS (0 FAIL / 0 SKIP)。与本次问题相关的三条:
- ✅ `m6-version-badge-match`: badge = 1.69.1
- ✅ `plugin-version-arch-docs-match`: plugin = 1.69.1, 2 处架构文档版本行一致
- ✅ `plugin-cache-currency`: installed 1.69.1 (scope=user) = SOT 1.69.1
其余: `issue-cache-freshness` / `i18n-readme-translation-currency` (3 语种 @1.69.1) / `claude-md-changelog-free` / `coordination-gate-invocation` (近期 7 次生产调用) / `config-template-key-currency` / `main-project-version-consistency` (1.7.5, 9 个引用点一致) / `forgejo-app-token-liveness` / `linked-issue-field-availability` / `m6-claude-md-version` / `m6-arch-doc-stale` / `silknode-contract-deferral-expiry` 全 OK。

### 🔄 同步状态
```
  当前分支: feature/a1-entry-claim-duplicate-work-guard (最新, 与 origin/... 同步)
  远程引用: 1m 前同步 (8/8 fetch 腿成功, 0 跳过)
  子模块:
    ✅ standards: 同步 (tree = remote = cc864ee, 工作区 checkout 为 bb5d375 — 有意 dirty)
    ✅ aria: 同步 (tree = remote = 7dd0135, 工作区 checkout 为 ab3dbd0 — 有意 dirty)
    ✅ aria-orchestrator: 同步 (tree = remote = 237045a, 工作区 checkout 为 92acce5 — 有意 dirty)
```

```
🌐 多远程一致性
  ✅ 主仓库: 所有远程一致 (origin, github) — 5d9b568
  ✅ aria 子模块: 所有远程一致 (origin, github) — ab3dbd0
  ✅ standards 子模块: 所有远程一致 (origin, github) — bb5d375
  ❓ aria-orchestrator 子模块: github 未见本地 tracking ref (no_local_tracking_ref, 证据 fresh)
     判定: 大概率该分支从未推往 github; 非「落后」, 不阻断 overall_parity
     如确需镜像: git -C aria-orchestrator push -u github feature/m6-cost-model-telemetry
  ✅ gitlink 完整性: 6/6 全 ok (github×3 + origin×3), 无 orphaned / orphan_unverified
```

- 📝 README 版本一致性: aria README 1.69.1 = plugin.json 1.69.1 ✅
- 📦 standards 子模块: 已注册且已初始化 ✅
- 🔗 Forgejo 配置: 检测到 Forgejo remote (`forgejo.10cg.pub`), 但项目未配置 —— 需要时可跑 `/forgejo-sync` 引导创建
- 协调 ref: `refs/aria/coordination` fetch 成功 (15s 前, 未降级)

### 🎫 Open Issues
open 47: `10CG/Aria` 20 · `10CG/aria-plugin` 20 · `10CG/aria-standards` 5 · `10CG/aria-orchestrator` 2。与你这次问题直接相关的:
- **Aria#165** — GitHub 镜像漏推第三次复发 (子模块服务端合并 + gitlink bump 无序 → orphaned gitlink)。你担心的正是这个类
- **Aria#176** — state-scanner AC-5 未排除本仓不存在的 remote (与「分支在某 remote 上不存在」这一格的判定精度有关)
- Aria#195 / aria-plugin#169 (`resilient_push` non-FF 恢复路径结构必失败) 等本轨 in-flight 项

> ⚠️ 计数保留意见: `issue_scan` 每仓 limit = 20, 而 Aria 与 aria-plugin **恰好各报 20** = 顶到上限且无截断标记, 实际总数可能高于 47 (上一份 handoff 已把这条记为未开单缺陷)。

---

## 🎯 推荐工作流

**【1】(推荐) 多远程核验 → 按结果决定是否补推** — 先跑上面「第一步」的只读 `ls-remote` 组合 (含 master 与 tag 两条你这次真正关心的线), 拿到真实差异再决定要不要 push。理由: 本轮机械证据显示零 behind, 在没有实测差异之前补推是盲操作; 而 `ls-remote` 是零副作用的。跳过: 全部写操作。

**【2】回到本轨 Phase B (母 Spec 31/40)** — 上次交接的高优先级是 H1 (Group 7 跑评测, 阻塞于会话级前置 `ARIA_COORDINATION_NO_PUSH`, 会话内补不上) → H3 发版三条 (8.1 CHANGELOG + 版本 SOT 5 文件 → 8.4 aria 本地 merge + 双推 + tag → 8.2 主仓 16 版本点 + gitlink bump)。**你说的「子模块更新 + 发布」其实就是 8.4/8.2, 它们还没执行**。注意 H3 待 AB 过关。

**【3】只看状态 / 换个面再扫** — 若你要确认的是 master 那条线, 切到 master 后重跑 `/state-scanner` (parity 只看当前分支)。

**【4】自定义组合** — 直接告诉我步骤, 例如 "只核验 aria 子模块两端 + tag"。

回复编号即可。两点执行提醒: 进 Phase B 前会触发 coordination advisory (`tracks_multibranch.collision.kind = self_multi_container`, 分组 `dev-claude` / `simonfishgit/dev-claude`); 任何子模块推送按既有硬约束需要你逐条授权, 我不会自作主张推。
