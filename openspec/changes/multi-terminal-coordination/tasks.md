# Tasks: Multi-Terminal Coordination

> **Spec**: changes/multi-terminal-coordination/proposal.md
> **Level**: Full (Level 3)
> **Status**: Approved (per post_spec R1+R2 convergence audit, 2026-05-19)
> **Created**: 2026-05-19
> **Estimated**: 44-58h (R1 v2 后含新增 1.9 task)

---

## 1. Layer H — Handoff frontmatter + 全分支重建看板 (P1 纯读零行为变更)

- [x] 1.1 在 `standards/conventions/session-handoff.md` 添加机读 frontmatter schema 段 (Rule #9 升级:字段定义 / 语义 / 示例 / 与现有 prose 段共存规则)
- [x] 1.2 升级 `aria/templates/session-handoff.md` 模板加 frontmatter 头
- [x] 1.3 state-scanner Phase 1 collector 扩展 `git fetch`(限定 refspec `refs/heads/*` + coordination ref,`--no-tags`,避免全量 tag 拖慢慢网络;**R1 v2**:本地 fetch 时间戳缓存,距上次 < 30s 跳过 → 看板标"缓存于 Xs 前")
- [x] 1.4 实现"扫所有 `origin/**` 的 `docs/handoff/` + 解析 frontmatter → 重建 track 列表"(**R1 v2**:解析失败时 — 无 frontmatter / schema 不全 — 标记为 `legacy` track 并按 mtime fallback,不阻塞看板;与 H5 v1.21.1 `feedback_handoff_mtime_vs_pointer_divergence` 协同)
- [x] 1.5 多 track 看板渲染(TRACK / OWNER/容器/会话 / PHASE / HANDOFF / LAST-PING / STATUS + 新鲜度颜色 + 折叠 done/abandoned 分区;**R1 v2**:LAST-PING 列源自 `Layer L claim.heartbeat_at`,PHASE 列源自 `Layer H frontmatter.phase`,缺则标 `—`)
- [x] 1.6 `docs/handoff/latest.md` 角色降级为派生产物(**R1 v2**:多 track 场景下 latest.md 不写真实指针,仅含 deprecation banner 指引读看板;单 track 场景仍写当前 track 指针以兼容老 session;L2 collector 读取语义权威**仍以 frontmatter 为准**,latest.md 仅 prose fallback)
- [x] 1.7 离线退化:fetch 失败时用缓存看板 + 顶部红条告警"看板可能陈旧"
- [x] 1.8 P1 单元 + 集成测试(**R1 v2** 具体 case:(a) 无 frontmatter 旧格式 handoff → graceful skip 不报错 / 标 legacy;(b) latest.md 多 track 时为 deprecation banner、单 track 时为指针;(c) 老 session `cat latest.md` 仍得可读 markdown;(d) 离线注入 → 顶部红条;(e) N=20+ 远程分支性能基线)
- [x] 1.9 **(R1 v2)** Rule #9 5 层 enforcement 兼容性同步:(a) **L1 hook** `handoff-location-guard.sh` 仅检查路径不检查内容 → 无需改动,文档化此判定;(b) **L2 collector** `scan.py` / `collectors/handoff.py` 增加 frontmatter-aware 解析能力(向后兼容无 frontmatter 旧 doc);(c) **L4 规约** 1.1 已覆盖;(d) **L5 D.3 template** 1.2 已覆盖 — 输出明确"5 层全覆盖" matrix 文档

## 2. Layer L — Orphan ref + 急切认领 + reconcile (P2 advisory liveness)

- [x] 2.1 设计并文档化 `refs/aria/coordination` orphan ref 结构 + claim 文件 schema(`claims/<container-id>/<session-id>.yaml`);**R1 v2** 字段:`schema_version: "1"`(必需,reader 见未知 version 降级 `status: unknown`)+ `track_id` / `owner` / `container` / `session` / `phase` / `status` / `claimed_at` / `heartbeat_at` + 可选 `superseded_from`
- [x] 2.2 实现身份生成 + 持久化(`~/.aria/container-id` 可选人类标签 + UUID 生成 + 回退 hostname;session-id 临时)
- [x] 2.3 实现 orphan ref bootstrap(幂等初始化)+ claim 读写 + push/fetch 操作
- [x] 2.4 实现确定性 track-id 派生(**R1 v2 规范化规则**:小写化 → `/` `.` `_` 替换为 `-` → 最大长度 64 字符 → 超长或含非 ASCII 时 fallback `sha256(原 id)[:16]`;跨容器实现必须共用此函数,单元测试枚举边界 case)
- [x] 2.5 急切认领闸门集成 state-scanner:推荐 → 用户确认 → 二次 fetch → 撞车检查 → push claim → 才放行 Phase B(**R1 v2 关键语义**:二次 fetch 通过**不是互斥锁获取**;push 后若他人同时 push,下次 fetch 触发 reconcile 确定性裁决;实现必须确保 push 前已写入 `claimed_at`,reconcile 是最终仲裁者,**闸门是窗口压缩器、非排他**)
- [x] 2.6 reconcile 协议实现(早 `claimed_at` 胜 / done 接管 / stale_ttl 接管 / 时钟相等字典序 `<container>/<session>` tiebreak)
- [x] 2.7 看板渲染加 COLLISION 行 + 时钟偏移检测告警;**R1 v2** 区分 **cross-owner collision**(强提示)vs **self-multi-container collision**(soft hint,可能容器迁移);时钟偏移超阈值时 reconcile **降级为 CONFLICT 标记 + 人工决策**,不静默用偏移时间戳判定
- [x] 2.8 claim 生命周期:acquire / heartbeat / release;**R1 v2 具体常量**(全部为命名常量,跨容器实现必须共用):heartbeat 周期 = **10 min**,`stale_ttl` = **30 min**(= 3× heartbeat),**`clock_skew_warn_threshold` = 30s**(R2 v3,同 track 两 claim 时间戳偏差 > 30s 触发 2.7 时钟偏移告警 + reconcile 降级 CONFLICT),orphan ref push 每 heartbeat 周期触发一次;每日 ~20+ push 在 git 单 ref 写压力可接受范围(无 pack GC 触发);**R1 v2 GC**:status=done claim 保留 7 天后移入 `archive/<year-month>/`(保留 sha256 摘要 tombstone),orphan ref 不参与 git GC 需手动维护
- [x] 2.9 失败处理(**R1 v2 失败矩阵完整覆盖**):
  - (a) push non-ff(两容器同推)→ fetch-replay-repush N 次
  - (b) push 401/403(认证失败)→ **不重试**,直接告警 + 人工决策
  - (c) push 失败其它原因 → 让用户决定继续/中止
  - (d) orphan ref 不存在(首次)→ 自动 `git commit --orphan` bootstrap,幂等
  - (e) **(R1 v2)** 磁盘满 / 本地写失败 → 告警 + 跳过 claim,**非崩溃**
  - (f) **(R1 v2)** partial fetch(网络中断,ref 更新不完整)→ **R2 v3 检测方式**:比对 fetch 前后本地 `refs/aria/coordination` 的 sha 是否**单调推进**(允许相等 = 远端未变;若回退或 fetch 报错 = partial fetch),失败按 (a) 重试;单元测试覆盖"fetch 中途 SIGKILL → 本地 ref 未污染"路径
  - (g) **(R1 v2)** 跨容器时钟偏移超阈值 → reconcile 降级 CONFLICT + 人工决策(per 2.7)
- [x] 2.10 P2 单元 + 集成测试(**R1 v2 强化**):
  - (1) **reconcile 黄金表必须覆盖**:全 4 规则 + 边界 `stale_ttl ± 1s`(三档:TTL-1s / TTL / TTL+1s)+ `heartbeat` 缺失视同 stale + `status` 4×4 组合矩阵(`active+active` / `done+active` / `done+done` / `abandoned+active` 等)
  - (2) **race 窗口可复现性**:时间戳通过 `ClockProvider` 抽象注入(或 monkeypatch `datetime.now`),CI 强制注入相同时间戳触发 tiebreak 路径;并发由两线程/进程 **barrier** 同步(**R2 v3**:必须为零 sleep 同步原语,如 `threading.Barrier` / `multiprocessing.Barrier` / 等效 IPC,**禁止用 sleep 近似**),不依赖真实 sleep;CI 报告记录"两 claim 时间戳差 < ε" 作为测试有效性断言
  - (3) **failure 注入矩阵**对应 2.9 每条
  - (4) **(R1 v2 known limitation)** 跨主机真实时钟偏移 E2E 不在本 Spec 范围 — 已在 proposal §测试策略接受;2.10 通过时间戳注入模拟,不要求真实多主机环境,后续 audit 勿重提此 limitation

## 3. Design A 条件触发 + Rule #6 benchmark + Dogfood (P3 完整闭环)

- [ ] 3.1 同容器并发 active claim 计数检测(本容器 ≥2 active 触发 worktree 模式)
- [ ] 3.2 worktree 自动创建逻辑:`worktrees/<track-id>/` + 子模块独立 checkout + 钩入 B.1 分支创建流程
- [ ] 3.3 worktree 生命周期:track release(`status: done`)后归档/清理策略 + 误用保护
- [ ] 3.4 Rule #6 structural benchmark 设计(**R1 v2 量化指标**,非 LLM with/without,需 human review 替代 with/without delta 判定):
  - (a) **看板正确性**:fixture 集 N=20 个,state-scanner 输出行数 / 字段值匹配期望,通过率 ≥ 95%
  - (b) **race 可复现**:10 次并发注入,碰撞检测触发率 = **100%**
  - (c) **reconcile 确定性**:黄金表 K 条(2.10 (1) 全覆盖),verdict 与期望一致率 = **100%**
  - (d) **失败矩阵覆盖**:M 个注入场景(2.10 (3) 全覆盖),降级行为符合规范率 ≥ 90%
  - baseline = 同测试集在旧 state-scanner(P1 上线前)通过率;`delta = new - baseline > 0` 即为通过
- [ ] 3.5 执行 `/skill-creator benchmark` 并存入 `aria-plugin-benchmarks/ab-results/`,通过率达 3.4 标准
- [ ] 3.6 Aria 主仓 dogfood:承载 ≥1 多终端 cycle,**R1 v2 可观测指标**(可证伪):
  - (a) **重复认领**:coordination ref 内同一 track-id 的 `status=active` claim 数 ≤ 1(超出即重复,记录到 dogfood 日志)
  - (b) **接错棒**:state-scanner 看板实际使用的 handoff `updated-at` 与该分支 git log 最新 handoff commit 时间差 **< 60s**
  - (c) dogfood 报告必须**包含上述实测数值**,不接受"未观测到问题"作为 PASS 依据
- [ ] 3.7 文档同步(**R1 v2 5 层 enforcement matrix 全覆盖**):
  - (a) `aria/skills/state-scanner/SKILL.md` 更新(L3)
  - (b) `CLAUDE.md` Rule #9 引用本 Spec(L4 顶层链接)
  - (c) `standards/conventions/session-handoff.md` schema 段(L4 已在 1.1)
  - (d) `aria/templates/session-handoff.md` frontmatter 头(L5 已在 1.2)
  - (e) L2 collector `scan.py` / `collectors/handoff.py` docstring + error message 更新(已在 1.9 covered)
  - (f) L1 hook `handoff-location-guard.sh` 文档化"不需改动,仅检查路径不检查内容"(已在 1.9 covered)
- [ ] 3.8 版本发布:aria-plugin minor bump + 跨 3 repo C.2 + **Rule #8 pre-merge gate (C.2.4)** 通过 + Phase D 归档(plugin.json / marketplace.json / VERSION / CHANGELOG / README + 子模块指针 + 多远程推送)

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. Layer H — Handoff frontmatter + 全分支重建看板 | 9 | 13-17h |
| 2. Layer L — Orphan ref + 急切认领 + reconcile | 10 | 20-26h |
| 3. Design A + Rule #6 benchmark + Dogfood | 8 | 11-15h |
| **Total** | **27** | **44-58h** |

> **R1 v2 note**:tasks.md 每行是粗粒度功能交付单元,符合 OpenSpec 模板"功能层面、不写实现细节"约束;CLAUDE.md "4-8h 可完成" 原则的颗粒度由 A.2 task-planner 在 `detailed-tasks.yaml` Layer 2 中通过 TASK-NNN 原子项保证(本层不直接对齐 4-8h)。响应 R1 knowledge-manager P2 粒度 finding。

---

## Dependencies

```
Phase 1 ──> Phase 2 ──> Phase 3
   │           │           │
   │           │           └── 依赖 1.x + 2.x 全部实现
   │           └── 依赖 1.3 (fetch) + 1.4 (重建) + 1.5 (看板)
   └── 独立可发布(纯读零行为变更,直接修接错棒)
```

每 Phase 独立安全、向后兼容:
- **P1 上线后**:即使 P2/P3 未实现,Layer H 已能根治"接错棒"
- **P2 上线后**:Layer L claim 闸门激活,残留秒级 race 窗口由 reconcile 兜底
- **P3 上线后**:同容器多 track 时 worktree 自动隔离;Rule #6 benchmark 锁定行为基线

---

## Notes

1. **Numbering Immutability**: 一旦编号(1.1, 1.2, ...)确立,不得更改。新增任务用新编号(1.9+),删除标 ~~cancelled~~ 不删行。
2. **粗粒度**: 每条任务是功能层面交付物,不写实现细节 / Agent 分配 / 文件路径(由 A.2 task-planner 在 detailed-tasks.yaml 落具体)。
3. **跨 repo 任务归属**:
   - Phase 1.1 → `standards` repo (session-handoff 约定)
   - Phase 1.2 / 1.3-1.9 / 2.x / 3.1-3.5 / 3.7 → `aria-plugin` repo (模板 + state-scanner skill)
   - Phase 3.6 → Aria 主仓 (dogfood consumer)
   - Phase 3.8 → 全 3 repo(版本发布 + 多远程推送)
4. **out-of-scope 提醒**:auto-memory 跨容器分叉单独 Spec;跨容器硬锁 / Forgejo 协调服务已被 DEC-20260519-001 #1/#2 否决,不应在 detailed-tasks.yaml 阶段重新引入。
5. **(R1 v2)** **跨 repo merge 顺序硬约束**(响应 R1 tech-lead M-01,per `feedback_sequenced_multirepo_gitlink_bump`):
   - **Step A**:`standards` PR(Phase 1.1)先 merge,bump standards 子模块指针
   - **Step B**:`aria-plugin` PR(Phase 1.2-1.9 + 2.x + 3.1-3.5 + 3.7)在 standards 子模块指针更新后再 merge,引用已定稿的 schema
   - **Step C**:Aria 主仓 PR(子模块指针 bump + Phase 3.6 dogfood)最后 merge;**Phase 3.8 发布是跨 3 repo fan-out 动作**(同步触发 standards + aria-plugin + Aria 主仓 的 plugin.json/marketplace.json/VERSION/CHANGELOG/README 同步 + 多远程推送,非单 repo PR),由 phase-c-integrator C.2.5 编排
   - 若 Phase 1 内部 standards PR 仍 in-review 时已开始 aria-plugin 实施,allowed pattern:aria-plugin 实施引用 "pending standards ratification" 标注的草案 schema,standards merge 后 aria-plugin 回填正式版本号;违反此约束 = 自我引入 Phase 1 内部跨 repo 死锁。

---

## Audit Plan (per Aria audit-engine)

- **post_spec (Phase A.1)**:本 Spec 写入后触发 R1 multi-agent audit(预期 5-agent fan-out;关注 race 协议正确性 / 失败矩阵完整性 / Rule #6 benchmark 类型选择)
- **mid_implementation**:Phase 2.6 reconcile 实现 + 2.10 race 集成测试通过后,触发 mid_implementation audit
- **post_implementation**:Phase 3.5 benchmark 通过后,触发 post_implementation audit
- **pre_merge**:跨 3 repo PR 合并前,触发 pre_merge gate(per Rule #8 + Rule #6 benchmark 数据)
