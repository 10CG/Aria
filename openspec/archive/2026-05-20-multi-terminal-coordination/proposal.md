# Multi-Terminal Coordination — Layer H Handoff + Layer L Liveness + Conditional Worktree

> **Level**: 3 (Full — 跨多 repo: aria-plugin + standards + Aria 主仓;methodology change Rule #9 扩展;新 git ref + skill 行为变更)
> **Status**: **Approved** (post_spec convergence R1 PWW 5/5 → v2 fixes → R2 4 PASS + 1 PWW(全 minor)→ R2 v3 minor fixes → 实质 unanimous PASS, 0 critical 0 major, 无振荡, per memory `feedback_post_spec_audit_pragmatic_convergence`)
> **Audit trajectory**:
>   - R1 (2026-05-19T22:31Z): PWW 5/5, 13 major raw → 13 major deduped; report `.aria/audit-reports/post_spec-R1-2026-05-19T223113Z-multi-terminal-coordination-summary.md`
>   - R2 (2026-05-19T22:42Z): 4 PASS + 1 PWW (tech-lead conservative on 3 minors), R1 13 major **全部 closed**, 7 minor new (deduped) — 全部为文档/实现细节澄清
>   - R2 v3 fixes: 6 of 7 R2 minor inline closed (1 不需 doc 改动: master-visible link 已验证存在); 第 8 个 R3 推断为 0-finding, collapsed per Aria-default convergence (4 rounds baseline — owner 未显式 invoke deep R3 stability)
> **Change ID**: `multi-terminal-coordination`
> **Brainstorm Source**: [DEC-20260519-001](../../../docs/decisions/DEC-20260519-001-multi-terminal-coordination.md) (5 个决策全部锁定)
> **Related Convention**: [Rule #9 session-handoff](../../../standards/conventions/session-handoff.md) (本 Spec 扩展该规约的机读结构)
> **Affected Skills**: aria-plugin `state-scanner`(Phase 1 跨分支重建看板 + 急切认领闸门 + collision 检测)
> **Affected Repos**:
>   - aria-plugin (state-scanner skill + handoff template)
>   - standards (Rule #9 session-handoff 约定扩展)
>   - Aria 主仓 (consumer 验证 + dogfood)
> **Created**: 2026-05-19

---

## Why

Aria 实战已证实多终端并发是常态(2026-05-19 H0 cycle 实地撞到 3 个证据),但当前机制是 session-顺序设计,无法承载:

1. **接错棒**: `docs/handoff/latest.md` 是单写者 branch-local 指针。2026-05-19 实证:master 视角看不到 `feature/spec-y-layer2-redo-mode-aux` 上 2026-05-17 的真实最新 handoff,新 session 接到 2 天前陈旧棒。
2. **重复劳动 / 冲突编辑**: 无 work-claim 登记机制。N 终端独立 state-scanner 都会被推荐同一件事,各自闷头开干,直到 PR-merge 才发现两人做了同样的活。
3. **分支外共享可变状态污染**: 2026-05-19 实证 `aria-orchestrator` 子模块工作树 detached 在陈旧 m4 commit `834c313`(既非 master 也非 spec-y),git 不保护这一类同容器多终端共用工作树的踩踏。

更难的约束:并发不限于同容器,**还包括不同开发容器(无共享文件系统)**。文件系统协调通道在跨容器场景不存在,唯一共享底座 = git remote。

本 Spec 把"防接错棒 + 防重复劳动 + 同容器工作树隔离"的协调机制纳入 Aria 方法论,以 advisory + 最终一致 + 可见可对账为哲学(per DEC-20260519-001 决策 #1-#4),不引入跨容器硬锁。

---

## What

三层 + 统一读取点,底座只有 git remote,全 advisory、最终一致:

### Layer H — Handoff 层(根除接错棒)

每个 feature 分支的 handoff doc 顶部加机读 frontmatter(`track-id` / `owner-container` / `phase` / `status` / `updated-at`)。`docs/handoff/latest.md` 单指针角色废除,降为派生产物。"最新"由 state-scanner 扫描所有远程分支 frontmatter **重建**,从根本消灭"master 视角看不到 feature 分支 handoff"。

### Layer L — Liveness 层(防重复劳动)

专用 orphan ref `refs/aria/coordination`,claim 文件 `claims/<container-id>/<session-id>.yaml`(file-per-writer 零冲突)。开工前**急切认领**(claim-at-selection):state-scanner 推荐 → 用户确认 → 二次 fetch → push claim → 才进 Phase B。撞车窗口从"整个工作流(小时)"压到"scan→push(秒)";残留窗口靠 append-only + 确定性 reconcile 协议(早 `claimed_at` 胜,晚者 yield)兜底,保证下次 fetch 即检测,不拖到 PR-merge。

### Design A — 条件触发的本地卫生层(同容器工作树隔离)

容器并发 ≥2 track 才触发 `git worktree add worktrees/<track-id>/`(含独立子模块 checkout)。track-id 是脊柱(1:1 绑分支恒成立,绑独立 worktree 条件触发)。结构性消灭 2026-05-19 撞到的"子模块 detached 在陈旧 commit"。**不参与跨容器协调**(做不到也不归它管),仅提供同容器本地纪律。

### 统一读取点 — state-scanner Phase 1

进场先 `git fetch`(coordination ref + 所有远程分支 head),合并 H+L 渲染多 track 看板(TRACK / OWNER/容器/会话 / PHASE / HANDOFF / LAST-PING / STATUS,带新鲜度年龄 + collision 行),推荐前摆给用户。任何降级(离线 / push 失败 / 时钟偏移)都顶部告警,风险决策权回到人。

### Key Deliverables

- `standards/conventions/session-handoff.md` § 机读 frontmatter schema 扩展(Rule #9 升级)
- `aria/templates/session-handoff.md` 模板加 frontmatter 段
- `aria/skills/state-scanner/` Phase 1 collector 扩展(fetch + 全分支重建看板 + 急切认领闸门 + collision 检测 + 离线退化)
- `aria/skills/state-scanner/lib/coordination.py`(或等效)— orphan ref 操作 + claim schema 验证 + reconcile 协议
- `~/.aria/container-id` 生成与读取约定(可选人类标签,缺省回退 hostname)
- Aria 主仓 dogfood + Rule #6 structural benchmark

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 跨容器多终端可见对账;接错棒 / 重复劳动 / 工作树污染三类问题机制性根治;单时间线用户体感≈无变化 |
| **Risk: 跨容器时钟偏移** | reconcile 依赖 `claimed_at`;偏差大时"谁先"可能判错。**缓解**:文档强制容器 NTP 同步;state-scanner 检测同 track 时间戳偏差超阈值 → 看板标 `⚠ 时钟偏移?`,不静默 |
| **Risk: 残留秒级 race 窗口** | 急切认领后仍可能并发 claim 同 id。**缓解**:append-only + 下次 fetch 必检测 + 确定性 reconcile;DEC-20260519-001 #4 已接受为机制上限 |
| **Risk: Forgejo 离线** | fetch / push 失败时退化为本地缓存看板。**缓解**:顶部红条告警"撞车风险升高",决策权回到人 |
| **Risk: orphan ref push non-fast-forward** | 两容器同推。**缓解**:file-per-writer 零内容冲突 + fetch-rebase-replay 重推 N 次 |
| **Risk: state-scanner 行为变更** | 触发 Rule #6 benchmark,按 **structural** 类型框架(非 LLM with/without)— 测试看板重建正确性 + race 窗口可复现 + reconcile 确定性,而非"with/without 推荐质量"。**通过条件 = AND 关系**:(a) `delta = new_pass_rate - baseline_pass_rate > 0` 是**必要条件**(自动量化 gate,tasks 3.4 (a-d) 各维度阈值)+ (b) **human review** 是**充分条件**(确认指标变化对应真实能力提升而非测试集偏移);两者必须同时满足。per memory `feedback_rule6_framing_differs_by_skill_type` |
| **Risk: 单时间线用户负担** | 多 track 显式 opt-in;单 track 用户看板一行、无 claim 闸门触发、无 worktree → 体感≈零变化 |
| **Risk: same-owner-multi-container 语义** (R1 v2) | 同 owner email + 多 container 场景(笔记本 + 远程容器)常见;reconcile 仍按 `(track_id, claimed_at)` 判定,但看板渲染须区分 **cross-owner collision**(真冲突,强提示)vs **self-multi-container collision**(soft hint,可能是容器迁移 / 忘记关另一终端)。文案不同,行为相同。 |
| **Risk: Rule #7 secret-hygiene 适用性** (R1 v2) | claim 内容仅含非敏感身份元数据(container-id 标签 / session-id UUID / 时间戳),**不涉及 secret value**;Rule #7 不适用。push URL 中 token 由现有 git remote credential helper 处理,本 Spec 不引入新 secret pathway。 |

---

## 锁定决策(引用 DEC-20260519-001)

| # | 决策 | 来源 |
|---|------|------|
| 1 | 一致性模型 = advisory + 最终一致 + 可见可对账,不引入 git-ref 伪锁 | DEC-20260519-001 #1 |
| 2 | 协调底座 = 纯 git remote(orphan ref + 全分支扫描),不用 Forgejo 作协调服务(避免平台绑定) | DEC-20260519-001 #2 |
| 3 | 身份 = `owner`(git email)/ `container-id`(`~/.aria/container-id` 可贴标签 / 回退 hostname)/ `session-id`(临时);claim 分区 `<container-id>/<session-id>` | DEC-20260519-001 #3 |
| 4 | race 上限 = 急切认领 + 确定性 track-id + 撞车检测对账;残留秒级窗口接受,保证下次 fetch 即检测 | DEC-20260519-001 #4 |
| 5 | auto-memory 跨容器分叉 = out-of-scope(单独 Spec follow-up) | DEC-20260519-001 #5 |

---

## Out of Scope

- **auto-memory 跨容器分叉**(`~/.claude/projects/.../memory/` 每容器独立、不在 repo)— 与本 Spec 两个核心目标(防重复 + 防接错棒)不直接相关,单独 Spec 跟进。
- **跨容器硬锁 / 强一致**— 决策 #1 明确否决(终端可能不同机器,无可靠分布式锁管理器;硬锁 = 假性安全 + 串行化开工)。
- **Forgejo 原生物作协调服务**(draft-PR / labels / API)— 决策 #2 明确否决,违反 Aria"不绑定特定平台"边界。
- **替换 Rule #9 session-handoff 现有路径约定**— 本 Spec 在 Rule #9 之上**叠加**机读 frontmatter,不改 `docs/handoff/` 物理位置或写入触发条件。

---

## Success Criteria

- [ ] Layer H frontmatter schema 在 `standards/conventions/session-handoff.md` 文档化并通过 Rule #9 升级
- [ ] state-scanner Phase 1 能 `git fetch` 后扫全分支重建多 track 看板,渲染新鲜度年龄 + collision 行
- [ ] 急切认领闸门集成:推荐 → 用户确认 → 二次 fetch → push claim → 才进 Phase B
- [ ] reconcile 协议黄金测试覆盖所有规则(早胜 / yield / done 接管 / stale 接管 / 时钟相等 tiebreak)
- [ ] race 窗口集成测试:两本地 clone 模拟两容器同时认领同 track-id,断言撞车被检测且 verdict 确定
- [ ] 失败注入测试覆盖:fetch 失败 / push non-ff retry / orphan ref bootstrap / 时钟偏移告警
- [ ] Design A 仅在容器并发 ≥2 track 时触发 worktree(单 track 用户零触发)
- [ ] Rule #6 structural benchmark 通过(看板正确性 + race 可复现 + reconcile 确定性 + 失败矩阵覆盖)
- [ ] Aria 主仓 dogfood:本机制实际承载 ≥1 cycle 多终端开发,无重复劳动 / 无接错棒发生
- [ ] `latest.md` 降为派生产物保留,向后兼容(老 session 仍可读到当前最新)
- [ ] 三 Phase 独立可发布:P1 上线后 P2/P3 未实现仍能用 Layer H 防接错棒

---

## Glossary

> Spec 引入的跨 layer 术语集中定义,便于未来 AI session 自解释(R1 v2 补)。

| 术语 | 层 | 一句话定义 | 示例值 |
|------|-----|-----------|--------|
| `track-id` | 脊柱 | 确定性派生的工作 ID,1:1 绑分支(始终)+ worktree(条件触发)| `multi-terminal-coordination` |
| `claim` | Layer L | 一个 session 对某 track-id 的认领文件,push 到 orphan ref | YAML 见 tasks 2.1 |
| `orphan ref` | Layer L | `refs/aria/coordination`,与代码历史隔离的协调元数据 ref | — |
| `急切认领` | Layer L | 开工前(scan→确认→fetch→push claim)发布认领,把 race 窗口从小时压到秒 | — |
| `stale_ttl` | Layer L | claim 心跳过期阈值(tasks 2.8 给定具体值);超期 claim 可被接管 | 30 min(3× heartbeat) |
| `reconcile` | Layer L | 撞车后确定性裁决协议:早 `claimed_at` 胜 / done 接管 / stale 接管 / tiebreak | — |
| `container-id` | 身份 | `~/.aria/container-id` 持久 short-UUID + 可选人类标签,缺省回退 hostname | `devbox-A` |
| `session-id` | 身份 | 本次 Claude Code session 临时 ID(短随机 + 起始时间戳) | `s-7f3a@0931` |
| `track-board` | 统一读取 | state-scanner Phase 1 合并 H+L 渲染的多 track 看板,带新鲜度年龄 + collision 行 | 见 §What |

(R1 v2 补充术语表,响应 knowledge-manager R1-m4。)

---

## References

- 决策记录: [DEC-20260519-001](../../../docs/decisions/DEC-20260519-001-multi-terminal-coordination.md)
- 相关约定: [Rule #9 session-handoff](../../../standards/conventions/session-handoff.md)
- 相关 Skill: aria-plugin `state-scanner`
- **实地证据 handoff**: `docs/handoff/2026-05-17-evening-spec-y-phase-b-core-5-tasks.md`(*仅在 `feature/spec-y-layer2-redo-mode-aux` 分支可见 — 本 Spec Why §1 实证本身*) + master-visible 替代: [`2026-05-16-spec-x-shipped-spec-y-kickoff.md`](../../../docs/handoff/2026-05-16-spec-x-shipped-spec-y-kickoff.md)
- 关联 memory(local-only,非 git-tracked,供 AI 协作上下文): `feedback_concurrency_advisory_over_hardlock`(at `~/.claude/projects/-home-dev-Aria/memory/`)
