---
track-id: state-scanner-stale-refs-false-parity
linked-issue: 10CG/aria-plugin#110
owner-container: aria-runner-bot/023236f2
phase: D-phase0-shipped
status: done
updated-at: 2026-07-17
---

# Session Handoff — 主 spec stale-refs-false-parity Phase 0 (prereq) 独立 ship v1.59.0 + 镜像修复 + #165

> 本对话 2026-07-14 → 07-17, 从 `/state-scanner` 开局多次。核心产出: **主 spec 第一个 sub-cycle (Phase 0 prereq) 独立 ship v1.59.0** (十步循环 B→C→D 完整)。附带: 修 aria-orchestrator GitHub 镜像断裂 + 开 Aria #165 (镜像漏推预防侧) + 追平双子星遗漏的 3 版 badge drift。

## §0 入口 (新 session 优先读)

- **下一步 = 主 spec Phase 1 (core, 不可拆, 最高风险)**。见 §6 四段式 roadmap (详版在双子星 `2026-07-16-specC-ship-falseparity-signoff.md §6`)。**F3′ remote_refresh 新 collector 是全 spec 最高风险单元** (多 remote 并行 fetch + `--prune` + per-host 限流 + deadline + 防饥饿 + 退避)。**需专门 session**, 非顺手。
- **当前态**: 主 spec Phase 0 已 ship v1.59.0 (aria `a537e7d` / 主仓 gitlink `e54a891`)。四仓双远程 parity ✓ (ls-remote 独立核验)。claim 已 **yielded** (下个 Phase 1 session 重新 acquire)。
- **⚠️ 2 条环境/机制观察** (见 §3): clock_skew 容器时钟 20663s + badge drift 靠人同步 (#140 实证)。

## §1 已完成

### 1.1 ⭐ 主 spec Phase 0 (prereq) 独立 ship v1.59.0 (B→C→D)

用户从 `/state-scanner` 推荐选 "先 ship Phase 0"。Phase 0 单 commit `e2a2b22` (基 aria master `cae92e8`/v1.58.0), 零行为变更基础:
- **F5′ `resolve_enforced_remotes`** 纯函数 (`collectors/multi_remote.py`) — **INERT 确认** (grep 全 scripts/ 零调用点, 未接线主链直到 Phase 1 F4′) → 据此判定 **免 benchmark** (Rule #6: 无行为变更可 AB)
- **sync_freshness.* config 键** (`config-loader/DEFAULTS.json`)
- **D16 predicate-domain-table.md 表骨架**
- **8 测试** (`test_mainspec_phase0.py`); 全量 **1072 绿** (含 multi_remote 不回归)
- 版本 bump v1.59.0: plugin.json (SOT) + marketplace.json ×2 + VERSION + CHANGELOG + README → commit `a537e7d` → 推 aria origin+github (FF, ls-remote 独立核验)

### 1.2 🔴 修 aria-orchestrator GitHub 镜像断裂 (本对话早期)

`/state-scanner` 报 `overall_parity: true`, 独立 ls-remote 抓出 aria-orchestrator github master 落后 2 (gitlink `86bb684` orphaned, `clone --recursive` from GitHub 断裂)。成因: PR#33 服务端合并只推 Forgejo。已推 github + F10″ 独立核验修复。

### 1.3 开 Aria #165 (镜像漏推预防侧) + cross-link aria-plugin #110

第三次镜像漏推复发 → 尽调根因: **gitlink bump 与子模块镜像推送无强制顺序** (分钟级时间线实证) + 四仓 Forgejo `push_mirrors=0` 零兜底。方案 A (push mirror) / B (bump 前 F10″ orphan 守卫) / C 并用, 待 owner 评估。双向 cross-link #110 (检测侧)。落 memory `feedback_mirror_sync_needs_mechanical_backstop`。

### 1.4 追平 badge drift (双子星 v1.57/v1.58 遗漏 3 版)

侦察发现 root README badge / 主项目 VERSION / i18n translated-from **全停在 1.56.1** (双子星 ship v1.57/v1.58 只更 CLAUDE.md, 漏主仓 badge 同步 3 版, #140 实证)。本 ship 一步追平 → v1.59.0 (badge×2 + VERSION + CLAUDE.md + i18n×3; README 正文自 v1.56.1 无实质变更 → i18n 免重译 #140 B 档)。

### 1.5 处理并发 rebase (c1da6e4)

主仓 push 撞并发: 另一 session 推 `c1da6e4` (badge 1.56.1→1.58.0, 修同一 drift)。rebase 我的 commit 到其上, README×4 冲突取我的 1.59.0 (supersede 1.58.0), 干净解决 → `e54a891`。

## §2 未完成 / Carry-forward

- 🔴 **主 spec Phase 1 (core)** — 最高风险, 专门 session。分支 `feature/state-scanner-stale-refs-false-parity` @ aria (Phase 0 已合入 master `a537e7d`; Phase 1 从新 master 起分支或复用该分支)。四段式 roadmap 见双子星 07-16 handoff §6。
- **Aria #165 方案评估** (owner 决策): A/B/C。⚠️ **方案 B (bump 前 orphan 守卫) 复用主 spec Phase 2 Track A 的 F10″ gitlink_orphaned 谓词** — 同一谓词两个消费点, **建议并入主 spec Phase 2 而非单开一条线** (避免重复实现)。
- (承前, owner 门) M6 4 门 (input-delivery + Blocker 4 Luxeno) / 168h 跑 / #136 webhook 轮换 / #151 credentials。
- claim 已 **yielded** — 下个 Phase 1 session 经 phase1_gate 重新 acquire。

## §3 关键风险 / 已知陷阱

- 🔴 **clock_skew 20663s (≈5.7h)**: phase1_gate acquire 时报容器时钟偏移 > 30s 阈值。本次无 competing claim (`competing_winner: null`) → 对 reconcile 无实际影响, 但 **aria-runner 容器 023236f2 时钟疑未同步**, 影响未来任何时间戳类 reconcile 判定。建议查容器 NTP。
- 🔴 **badge drift 靠人同步 (#140 实证再现)**: 双子星连 ship 3 版 (v1.57/v1.58 + 中途 1.58.0 补) 都漏 root README badge / VERSION / i18n。custom check `m6-version-badge-match` 依赖**下次 scan** 才暴露 (非 ship 时闸)。本 session 已追平, 但机制上仍靠人 → 与 #165 (版本/gitlink 同步机械化) 同源。
- 🔴 **主仓高频撞并发**: 本 session 撞一次 (c1da6e4)。每次主仓 push 前必 fetch + 视情况 rebase; scan.py 的 `behind` 数不可信 (#110, 本对话 5 次活体撒谎)。
- **本仓 dogfood 是 reference 非 authority**: F5′ INERT 在本仓测得过, 但 Phase 1 F3′ 的真实网络/拓扑风险 (2 host / 60 腿) 本仓测不全 (承双子星 R5-R9 教训)。

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | `e54a891` 双远程 parity ✓ (ls-remote 独立核验) |
| aria-plugin master | `a537e7d` **v1.59.0** 双远程 parity ✓ (marketplace 已发布) |
| 主 spec stale-refs | v10 Approved; **Phase 0 shipped v1.59.0**; Phase 1-3 待 |
| standards / aria-orchestrator | `79b7cd6` / `86bb684` gitlink 两远程可达 (F10″ ✓) |
| aria-orchestrator 工作树 | ` M` = WIP feature checkout (`feature/m6-cost-model-telemetry`), 非待办 |
| 协调 ref | 主 spec claim **yielded** (含清旧 2026-07-12 A.1 悬挂 claim) |
| 测试 | state-scanner 1072 real-green |

## §6 Next session 入口 + 优先级

1. ⭐ **主 spec Phase 1 (core)** — 专门 session, 最高风险 F3′。四段式:
   - Phase 1 (不可拆): F1′ 两轴双谓词 + F2′ 退役 mtime + **F3′ remote_refresh collector** (最高风险) + F4′ overall_parity 四子句重写 + F6′ shim + **9.7 offline 三面冻结 (必须同 PR)**
   - Phase 2 A/B (并行): Track A F10″ gitlink_orphaned 八分支; Track B F9′ sync.py 消费 (⚠️ 绝不碰 US-008 方向性判据 sync.py:312-328)
   - Phase 3: 12.10 六漂移通道核实 + golden fixture 重采 + 下游 + 发布
2. **#165 方案评估** (建议并入 Phase 2 Track A, 复用 F10″)
3. owner 门 (M6 4 门 / 168h / #136 / #151)

## §8 Memory entries this session

- **已落** (本对话早期): `feedback_mirror_sync_needs_mechanical_backstop` (镜像同步靠纪律对服务端合并路径无效; #165 根因)。
- **[候选, 评估后不单落]**:
  - clock_skew 容器时钟 — 单例环境观察, handoff §3 记录足够, 非 generalizable。
  - badge drift 追平 — 已被 `feedback_mirror_sync_needs_mechanical_backstop` (版本同步靠人易漏) + #140 覆盖。
- **[未写下经验]**: 无。

## Cross-references

- 主 spec: `openspec/changes/state-scanner-stale-refs-false-parity/` (v10 Approved, Phase 0 shipped)
- 前序 handoff: `docs/handoff/2026-07-16-specC-ship-falseparity-signoff.md` (三 spec sign-off + C/B ship + Phase 0 roadmap)
- Issue: Aria #165 (镜像漏推预防侧) / aria-plugin #110 (检测侧)
- ship commits: aria `a537e7d` (v1.59.0) / 主仓 `e54a891` (gitlink bump + badge)
