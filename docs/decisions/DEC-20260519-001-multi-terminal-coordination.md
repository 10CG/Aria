# 决策: DEC-20260519-001 - 多终端并发开发协调机制

> **日期**: 2026-05-19 | **模式**: technical (brainstorm v2.0)

## 背景

Aria 的 handoff / state 模型是 **session-顺序**(单一时间线、接力棒传递),但实际工作流是 **session-并发**(多终端、多 feature 分支并行),且并发不限于同一开发容器,还包括**不同容器(无共享文件系统)**。

本次 session 实地撞到三个证据:

1. `docs/handoff/latest.md` 是单写者全局指针、branch-local —— master 视角看不到 `feature/spec-y-layer2-redo-mode-aux` 分支上 2026-05-17 的真实最新 handoff(接错棒)。
2. 无 work-claim / 所有权登记 —— 终端间可能重复劳动或冲突编辑。
3. 分支外共享可变状态无人管 —— `aria-orchestrator` 子模块工作树 detached 在陈旧 m4 commit `834c313`(既非 master `b197f26` 也非 spec-y `a5f0ef6`);auto-memory 目录、`.aria/` 状态跨容器各自独立。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 拓扑 | 多终端含跨容器,**无共享文件系统** | 唯一跨容器共享底座 = git remote (Forgejo);文件系统协调通道不存在 |
| 一致性 | 选 (c):最终一致 + advisory + 可见可对账,不做跨容器硬锁 | 机制目标 = 让分叉可见 + 有对账协议,而非阻止;接受秒级残留窗口 |
| 核心目标 | 防重复劳动 + 防 handoff 接错棒(两者并重,要自洽整体) | auto-memory 跨容器分叉判定 **out-of-scope**(单独 follow-up) |
| 平台 | 弱化 Forgejo 绑定(Aria"不绑定特定平台"边界) | 协调走纯 git ref,不用 Forgejo 原生物作协调服务 |
| 方法论 | 单时间线为默认,多 track 显式 opt-in;小步 + 向后兼容 | 单终端用户体感≈无变化 |

## 考虑的方案

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| 设计1 | 专用 orphan ref `refs/aria/coordination` + 每容器每会话一文件 | 高(无冲突/不污染历史) | **采纳(Liveness 层)** |
| 设计2 | 复用 per-branch handoff + 机读 frontmatter,index 由扫描所有远程分支重建 | 高(零新概念/根治单指针 siloing) | **采纳(Handoff 层,为主)** |
| 设计3 | Forgejo draft-PR 即 claim | 中(近实时但重绑 Forgejo) | 否决(违反平台边界约束) |
| Design A | git worktree per track | 条件触发 | **收缩采纳(同容器工作树隔离)** |

## 最终选择

**方案**: 设计2(为主)+ 设计1(薄 Liveness 层)+ Design A(条件触发的同容器本地卫生层)

三层 + 统一读取点,底座只有 git remote,全 advisory、最终一致:

- **Layer H(Handoff,设计2)**:每 feature 分支 handoff doc 顶部加机读 frontmatter(`track-id`/`owner-container`/`phase`/`status`/`updated-at`);`latest.md` 单指针角色废除,降为派生产物;"最新"由扫描所有远程分支 frontmatter 重建 → 根除接错棒。
- **Layer L(Liveness,设计1)**:orphan ref `refs/aria/coordination`,`claims/<container-id>/<session-id>.yaml`,file-per-writer 零冲突;**急切认领**(claim-at-selection,开工前 push)。
- **统一读取点**:state-scanner Phase 1 `fetch` 后合并 H+L 渲染多 track 看板(带新鲜度年龄 + collision 行),推荐前摆给用户。
- **track-id 是脊柱**:1:1 绑分支恒成立;绑独立 worktree 仅在容器并发 ≥2 track 时触发(Design A 收缩为同容器工作树隔离,不参与跨容器协调)。

### 5 个锁定决策

1. 一致性模型 = (c) 最终一致 + advisory + 可见可对账,不引入 git-ref 伪锁。
2. 协调底座 = 纯 git remote(orphan ref + 全分支扫描),不用 Forgejo 作协调服务。
3. 身份 = `owner`(git email)/ `container-id`(`~/.aria/container-id` 可贴标签,回退 hostname)/ `session-id`(临时);claim 按 `<container-id>/<session-id>` 最细分区。
4. race 上限 = 急切认领 + 确定性 track-id + 撞车检测对账;残留秒级窗口接受,保证下次 fetch 即检测。
5. auto-memory 跨容器分叉 = out-of-scope(单独 follow-up Spec)。

## 理由

1. 设计2 复用 Rule #9 已有 handoff 机制,零新概念即根治"单可变指针 shadow 掉真实最新"。
2. 设计1 file-per-writer 分区使 claim push 永不产生写冲突,只产生可检测的语义冲突,由确定性 reconcile 协议消解(早 `claimed_at` 胜,晚者 yield;done/stale 可接管)。
3. 急切认领把撞车窗口从"整个工作流(小时)"压到"scan→确认→push(秒)",且确定性 track-id 保证重复**可被检测**而非两船夜里相错。
4. Design A 是 H+L 解决不了的"同容器单一工作树污染"(本次 `834c313` bug)的唯一解;跨容器由 H+L 全解,故 Design A 正确收缩为条件触发本地卫生层。
5. 三 Phase 渐进(P1 纯读 / P2 Liveness / P3 worktree)每步独立安全、向后兼容,单时间线为默认。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 跨容器时钟偏移影响 reconcile "谁先" | 文档强制容器 NTP 同步;state-scanner 检测同 track 时间戳偏差超阈值 → 看板标 `⚠ 时钟偏移?`,不静默 |
| fetch 失败 / Forgejo 不可达 | 用缓存看板渲染 + 顶部红条告警"离线,撞车风险升高";风险决策回到人 |
| 残留秒级窗口仍并发认领同 track | append-only + 时间戳,下次任一方 fetch 即检测 collision,reconcile 早者胜 |
| orphan ref push non-fast-forward(两容器同推) | fetch + 重放本会话文件 + 重推,最多 N 次;内容无冲突仅延迟 |
| 废弃分支污染看板 | `status: done/abandoned` 或 stale_ttl 超时 → 折叠到"已归档/疑废弃"分区 |
| 给单终端用户增负担 | 多 track 显式 opt-in;单时间线为默认,体感≈无变化 |
| state-scanner skill 行为变更 | 触发 Rule #6 benchmark,按 `structural` 类型框架(非 LLM with/without) |

## 后续

- **OpenSpec 定级**: Level 3(proposal + tasks),跨 3 repo:aria-plugin(state-scanner skill)+ standards(session-handoff 约定 / Rule #9)+ Aria 主仓。
- **落地**: Phase 1(纯读零行为变更,直接修接错棒,独立可发布)→ Phase 2(Layer L advisory)→ Phase 3(Design A 条件触发)。
- **引用**: 供 `/aria:spec-drafter` 起 proposal 引用本决策 ID。
- **out-of-scope follow-up**: auto-memory 跨容器分叉单独 Spec。
- **Spec(R1 v2 反向回引)**: `openspec/changes/multi-terminal-coordination/`(Draft,2026-05-19;post_spec R1 PASS_WITH_WARNINGS → v2 fixes → R2 verify)
