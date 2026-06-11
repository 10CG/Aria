# 决策: DEC-20260611-002 - 跨 worktree handoff 发现与 EnterWorktree 引导

> **日期**: 2026-06-11 | **模式**: technical | **来源**: brainstorm (3 问收敛, 每问 3 方案)
> **触发**: Forgejo [10CG/Aria#139](https://forgejo.10cg.pub/10CG/Aria/issues/139) — triage `confirmed` 4/4 ([comment-12467](https://forgejo.10cg.pub/10CG/Aria/issues/139#issuecomment-12467))
> **审计**: post_brainstorm checkpoint = off (config), 跳过; post_spec convergence 审计在 Phase A.1 后执行

## 背景

单人多 worktree 并行场景: Phase D 把 session handoff 写在 feature worktree (分支 Y, 未合 main), 新会话默认在主 worktree 启动, `scan.py` 仅按 cwd 采集 → 完全读不到 worktree Y 的最新 handoff, 新会话被引导进错误状态 (2026-06-04 SilkNode cut2-batch1 实地事故)。

Triage 增量情报 (v1.44.0 核验):
- 全 state-scanner collectors 零 `git worktree list` 调用; `handoff.py` 仅扫 cwd
- frontmatter §2.3.1 无 worktree 字段; #137 (v1.43.0) 仅 enforce 既有 5 字段
- layer-l TASK-024/025 仅 `cross_owner` collision 触发且语义是**创建**新 worktree, single-owner **进入已存在** worktree 是覆盖盲区
- **Step 1.17 `handoff_multibranch` 仅扫 `refs/remotes/origin/*`** — worktree 分支未 push 时多 track 看板同样失明 (sandbox e2e 实证: `tracks_multibranch.exists=False`, branches_scanned=0)

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 哲学 | advisory-over-hardlock (DEC-20260519-001) | 引导不得自动切换 |
| 兼容 | snapshot schema 1.0 additive-only | 不改 `handoff.*` 既有字段语义 |
| 机制 | E1 自校验 `head -8` 窗口 (5 字段 + 2 分隔线 = 7 行) | frontmatter 加字段会破窗口, 牵连 #137 enforcement |
| 语义 | H5 fix: latest.md pointer 是语义权威, mtime 仅 fallback | 跨树仲裁不得退回裸 mtime |
| 既有设计 | TASK-024/025 cross_owner 创建语义 | 本设计正交, 不得混入 claim/heartbeat |

## 考虑的方案

### Q1: worktree 信息载体

| 方案 | 描述 | 状态 |
|------|------|------|
| A | 纯机械发现 (`git worktree list` 枚举, 零 frontmatter schema 变更) | ✅ **选定** |
| B | 字段 + 机械发现双轨 (issue 原案: frontmatter +worktree/branch 字段) | ❌ E1 head-8 破窗 + §2.3.1 bump + E2 同步, 改动面翻倍; 字段写后即可 stale |
| C | 仅字段不机械发现 | ❌ 字段写在 scan.py 读不到的文件里, 自相矛盾 |

**关键论证**: 事故根因是"发现不了"不是"声明不够"; path/branch 由 git 在扫描时刻给出, 是机械真值永不 stale; 机械发现独立覆盖 triage 全部 4 个复现 case。字段层若未来有跨机看板需求可 additive 后补。

### Q2: 跨 worktree "最新" 仲裁

| 方案 | 描述 | 状态 |
|------|------|------|
| A | 每树先按既有两级语义 (pointer→mtime) 解出各自 resolved latest, 跨树用 frontmatter `updated-at` 比较, 缺则降级 mtime; 输出含全量列表 | ✅ **选定** |
| B | 全局裸 mtime (issue 原文) | ❌ 绕过 pointer 语义权威, 与 H5 fix 实证结论冲突; mtime 受 checkout 时间污染 |
| C | 不仲裁只罗列 | ❌ 无"最新"则无法给出明确 EnterWorktree 推荐; A 的输出已包含 C 的全量列表 |

### Q3: EnterWorktree 引导边界

| 方案 | 描述 | 状态 |
|------|------|------|
| A | advisory 推荐 + 用户确认: 警示 + 编号选项 `[1] EnterWorktree / [2] 留在当前树 / [3] 先看该 handoff`; 非 Claude Code 环境降级打印 cd 指引 | ✅ **选定** |
| B | 高置信自动切换 | ❌ 机器无法区分"忘了切"与"故意不切" (hotfix / 新 track), 自动切换 = 反向制造本 issue 要防的事故 |
| C | 仅警示不提供动作 | ❌ 正是 issue 抱怨的现状体验 |

## 最终设计 (两段展示均 owner 确认)

### 架构与数据流

新 collector **`handoff_worktrees.py`** (Phase 1.15b, 紧随 1.15)。不改 `handoff.py` 任何行为, `handoff.*` 继续表示当前 worktree (backward compat)。

```
git worktree list --porcelain (path + branch + HEAD)
  │ 排除当前树; 单 worktree → 整段 no-op (零行为变化)
  ▼
对每个其他 worktree: 复用 handoff.py resolved-latest 逻辑 (pointer→mtime, H5)
                     + parse_handoff_frontmatter 既有 helper
  ▼
跨树仲裁 (含当前树): 比较键 = frontmatter updated-at → 缺则 mtime 降级
  ▼
snapshot additive 顶层字段 handoff_worktrees:
  { enumerated: bool, worktree_count: int,
    others: [ {path, branch, latest_doc, updated_at, status, track_id, source} ],
    global_latest_elsewhere: null | {path, branch, doc, status, age_hours} }
```

`global_latest_elsewhere != null && status == active` → 阶段 2 触发 advisory 推荐 (Q3-A)。

**默认开启**, `state_scanner.worktree_scan.enabled=true` 可关 (无多 worktree 时零成本 no-op, 与 1.16/1.17 default-on 一致; 不同于 issue_scan 的网络开销才 opt-in)。

### 降级与边界

软错误全走 `errors[]` + exit 10:

| 失败点 | soft_error | 行为 |
|--------|-----------|------|
| `git worktree list` 失败 | `worktree_enumeration_failed` | enumerated=false, 阶段 2 不触发引导 |
| 某树不可达 (prunable/网络盘) | `worktree_unreachable` (记 path) | 跳过该树继续 |
| 某树 docs/handoff/ 扫描失败 | 复用 `handoff_canonical_scan_failed` 语义 (带树前缀) | 该树视为无 handoff |

边界裁定 (实施期不得扩 scope):
1. **只读发现零写入** — 不碰任何 worktree 文件, 不做 claim/heartbeat (Layer L phase1_gate 职责, 不混)
2. 不扫 bare/prunable; detached 树照扫 (branch 记 `(detached)`)
3. worktree 数上限复用 `resolve_max_branches_scanned` 模式 (env > config > default **8**), 超限 soft warn
4. TASK-024/025 不动, 文档加一行互引 (创建 vs 进入, 正交)

### 测试策略 (Rule #6 substitute: deterministic collector)

- unit: tmpdir **独立** fixture (#135 教训: 不用 repo.parent) 建 main+2 worktree — 覆盖: 无 worktree no-op / 他树更新 / 当前树更新 / 缺 frontmatter mtime 降级 / pointer-vs-mtime 树内裁决 / enumeration 失败降级
- dogfood: Aria 真树 no-op 验证; triage case-4 sandbox 脚本升级为回归测试

### 交付物边界

collector + scan.py 注册 + SKILL.md 阶段 2 推荐规则 + output-formats.md 区块 + state-snapshot-schema.md 字段定义 + RECOMMENDATION_RULES.md 新规则 (priority 与 handoff awareness 同档)。**不含 standards 变更** (Q1=A 红利)。

## 理由

1. 机械真值优于声明: git 在扫描时刻给出的 path/branch 永不 stale, 字段则写后即旧
2. 零 schema 变更使 #137 E1/E2、standards §2.3.1 全部免动, 改动面减半
3. 逐层复用已验证语义 (H5 pointer 权威 / §2.3.3 updated-at 机读 SOT / soft-error 惯例), 不引入第三套"最新"定义
4. advisory 边界把"忘了切 vs 故意不切"这一只有人能做的判断留给人, 执行成本降到一次选择

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 他树 handoff 属已 abandon 的 track, 误引导 | 仲裁后仅 `status == active` 触发推荐; done/abandoned 仅在列表中展示 |
| worktree 在网络盘/慢盘, 枚举拖慢 scan | 上限 8 + 单树扫描仅 docs/handoff/ 一层 iterdir; 失败走 soft error 不阻塞 |
| 用户在主树故意开新活被反复打扰 | 推荐为编号选项非阻塞 gate; 选 [2] 留下即继续正常推荐流 |
| EnterWorktree 非全环境可用 | 检测不到 harness 工具时降级打印 cd 指引 (advisory 本质不变) |

## Ship target (snapshot, A.1 须重验版本)

- aria-plugin v1.45.0 (MINOR: collector 新增 + 推荐规则) — 当前 v1.44.0 @ `5871e17`
- OpenSpec: Level 2 (`proposal.md`), slug 建议 `cross-worktree-handoff-discovery`
- 关联: #139 (close on ship) / #137 (互补, 零交集) / aria-plugin#75 + Aria#141 (独立, 不卷入本 cycle)
