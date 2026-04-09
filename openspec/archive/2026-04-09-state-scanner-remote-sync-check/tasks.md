# Tasks: state-scanner 本地/远程同步检测

> **Parent Spec**: [proposal.md](./proposal.md)
> **Level**: 2 (Minimal) — tasks.md 非强制，此处补充用于协调与 `issue-awareness` 共享 v2.9.0 发布
> **Estimated Total**: 4-6 小时
> **Coordination**: 与 `state-scanner-issue-awareness` 同版本 v2.9.0 并行开发

## Task Breakdown

### T1: Upstream 探测与 ahead/behind 计算 [0.5h]

- [ ] 在 `references/sync-detection.md` 定义 upstream 探测逻辑 (proposal D11)
- [ ] `git rev-parse --abbrev-ref --symbolic-full-name @{u}` 探测 upstream
- [ ] upstream 缺失 → `{ahead: null, behind: null, reason: "no_upstream"}`
- [ ] upstream 存在 → `git rev-list --count upstream..HEAD` 和 `HEAD..upstream`
- [ ] detached HEAD 场景: `current_branch.name: null, reason: "detached_head"`

### T2: 浅克隆检测与 fallback [0.5h]

- [ ] 探测 git 版本: `git --version | awk '{print $3}'`
- [ ] git ≥ 2.15: `git rev-parse --is-shallow-repository`
- [ ] git < 2.15: `[ -f "$(git rev-parse --git-dir)/shallow" ] && echo true`
- [ ] 浅克隆 → `{shallow: true, behind: null, reason: "shallow_clone"}`

### T3: Submodule 四级 fallback 链 [1h]

实现 `remote_commit` 的四级降级 (proposal D10):

- [ ] Tier 1: `git -C <sub> rev-parse refs/remotes/origin/HEAD` → `origin_HEAD`
- [ ] Tier 2: `timeout 5 git -C <sub> ls-remote origin HEAD` → `ls-remote`
- [ ] Tier 3: 读 `git config --get init.defaultBranch` + `refs/remotes/origin/<branch>` → `config_default` (注意: 本地配置可能与远端默认分支不一致，属 fail-soft 可接受)
- [ ] Tier 4: 全失败 → `remote_commit: null, remote_commit_source: "unavailable"`
- [ ] 实现 `workdir_vs_tree` 和 `tree_vs_remote` 偏差计算
- [ ] 子模块未初始化时跳过该条目 (不报错)

### T4: FETCH_HEAD 时间戳跨平台读取 [0.25h]

- [ ] 使用 `git log -1 --format=%cr FETCH_HEAD 2>/dev/null` (跨平台友好)
- [ ] FETCH_HEAD 缺失 → `remote_refs_age: "never"`
- [ ] `remote_refs_age > warn_after_hours` (默认 24h) → 附加 warning 标注

### T5: SKILL.md 阶段 1.12 + references/sync-detection.md [1h]

- [ ] 在 `aria/skills/state-scanner/SKILL.md` 追加阶段 1.12 摘要 (~25 行)
- [ ] 明确标注："详细逻辑见 references/sync-detection.md"
- [ ] 配置表格新增 `state_scanner.sync_check.*` 三字段
- [ ] **新建** `aria/skills/state-scanner/references/sync-detection.md`:
  - 完整检测流程
  - Upstream 探测代码示例
  - 四级 fallback 链示例
  - 跨平台命令兼容表
  - 所有边界场景处理

### T6: RECOMMENDATION_RULES.md 新增规则 [0.25h]

- [ ] 新增 `submodule_drift` 规则: 任一 submodule `tree_vs_remote: true` → 降级推荐 + 附加 `git submodule update --remote` 提示
- [ ] 新增 `branch_behind_upstream` 规则: `behind >= 5` → 降级推荐 + 附加 `git pull` 提示
- [ ] 两规则均**不阻断**推荐 (fail-soft)

### T7: config-loader 默认值 [0.25h]

- [ ] 扩展 `aria/skills/config-loader/SKILL.md` 默认值表格:
  - `state_scanner.sync_check.enabled` = `true` (本地 git，默认开)
  - `state_scanner.sync_check.check_submodules` = `true`
  - `state_scanner.sync_check.warn_after_hours` = `24`
- [ ] 同步扩展 `.aria/config.template.json` 新增 `state_scanner.sync_check` block

### T8: 架构文档更新 [0.25h]

- [ ] 更新 `docs/architecture/system-architecture.md`，PATCH 级:
  - 标注 Phase 1.12 作为 state-scanner 扩展点
  - 记录子阶段数量 12/15 (D8 上限追踪)
- [ ] 无版本号字段变更，仅内容更新

### T9: output-formats.md 新增同步状态区块 [0.25h]

- [ ] 在 `aria/skills/state-scanner/references/output-formats.md` 新增 "🔄 同步状态" 输出示例
- [ ] 覆盖 4 种场景: 正常 / 落后 / 浅克隆 / detached HEAD

### T10: AB Benchmark [0.75h]  **(必须先于 T11 执行)**

- [ ] Mock fixture: 模拟 submodule drift 场景 (tree vs remote commit 偏差)
- [ ] Mock fixture: 模拟 upstream 落后场景 (behind 3)
- [ ] Mock fixture: 模拟浅克隆降级
- [ ] 运行 `/skill-creator benchmark` with/without AB 对比
- [ ] 验证 delta (sync-check 为纯本地 git 命令，若 delta EQUAL 仍属正常，对照 project_ab_baseline.md 3 EQUAL 先例)
- [ ] 结果归档到 `aria-plugin-benchmarks/ab-results/`
- [ ] **若 delta 为负: 暂停后续，回到 T1-T5 调整**

### T11: 版本号同步 [0.25h]  **(与 issue-awareness 协调, 避免 merge conflict)**

- [ ] 确认 `issue-awareness` 是否已先合并 (若是，仅追加 CHANGELOG 条目)
- [ ] 若先于 `issue-awareness` 合并:
  - `aria/.claude-plugin/plugin.json` → 2.9.0
  - `aria/.claude-plugin/marketplace.json` → 2.9.0
  - `aria/VERSION` → 2.9.0
  - `aria/CHANGELOG.md` → 新增 [2.9.0] 条目 (含 sync-check feature bullet)
  - `aria/README.md` → 版本号 + Skills 描述
- [ ] 若 `issue-awareness` 已合并:
  - 仅在 `aria/CHANGELOG.md` 的 [2.9.0] 条目追加 sync-check feature bullet
  - 其他文件已是 2.9.0，无需修改

### T12: 集成验证 [0.25h]

- [ ] 在 Aria 本仓库运行 state-scanner
- [ ] 确认输出包含 "🔄 同步状态" 区块
- [ ] 确认 aria / standards / aria-orchestrator 三个子模块均被检测
- [ ] 确认 `remote_commit_source` 字段正确填充 (origin_HEAD / ls-remote / config_default / unavailable)
- [ ] 手动测试: 浅克隆、detached HEAD、无 upstream 场景

## Dependencies

```
T1 (upstream) ──┐
T2 (shallow) ───┼──> T5 (SKILL.md + references)
T3 (submodule) ─┤
T4 (FETCH_HEAD) ┘

T5 ──┬──> T6 (rules)
     ├──> T7 (config)
     ├──> T8 (architecture)
     └──> T9 (output-formats)

T6, T7, T8, T9 ──> T10 (AB Benchmark)   ← 先 benchmark
T10 (delta 非负) ──> T11 (版本号同步)    ← 后 bump 版本
T11 ────────────> T12 (集成验证)
```

## Agent Assignment (Phase A.3)

| Task | Primary Agent | 辅助 Agent | 理由 |
|------|---------------|-----------|------|
| T1 Upstream 探测 | `aria:backend-architect` | - | git 命令设计 |
| T2 浅克隆 fallback | `aria:backend-architect` | - | 跨版本兼容 |
| T3 Submodule 四级 fallback | `aria:backend-architect` | `aria:qa-engineer` (边界) | 核心逻辑 + 边界测试 |
| T4 FETCH_HEAD 时间戳 | `aria:backend-architect` | - | 跨平台命令 |
| T5 SKILL.md + references | `aria:knowledge-manager` | `aria:backend-architect` | 文档组织 + 技术准确性 |
| T6 RECOMMENDATION_RULES | `aria:backend-architect` | - | 规则设计 |
| T7 config-loader 默认值 | `aria:backend-architect` | - | Schema 扩展 |
| T8 architecture 文档更新 | `aria:knowledge-manager` | - | 文档同步 |
| T9 output-formats 区块 | `aria:knowledge-manager` | - | 输出格式 |
| T10 AB Benchmark | `aria:qa-engineer` | - | 质量验证 |
| T11 版本号同步 | **主 agent** (协调) | - | 需跨 Spec 协调 |
| T12 集成验证 | `aria:qa-engineer` | `aria:code-reviewer` | 最终验证 |

**Code Review 门禁**: 所有任务完成后由 `aria:code-reviewer` 做 final review (C.2 前)

## Merge Gate (不可协商)

- ✅ T10 AB Benchmark 已执行 (delta 非负，允许 EQUAL 因纯本地 git 无 LLM 路径分歧)
- ✅ T11 版本号与 `issue-awareness` 协调一致 (避免 merge conflict)
- ✅ T12 集成验证 12/15 阶段数追踪 (对齐 D8)
- ✅ 本 Spec 影响 **12 个文件** (其中 5 个版本号文件共享 `issue-awareness`)
- ✅ Code review 通过 (`aria:code-reviewer`)

## 与 issue-awareness 的协调检查清单

- [ ] 两 Spec 的 T10 (benchmark) 独立执行，互不依赖
- [ ] 哪个 Spec 的 PR 先合并 → 由该 PR 完成 `2.8.0 → 2.9.0` 全量升级
- [ ] 后合并的 PR 仅在 CHANGELOG 追加自身 feature bullet
- [ ] 两 Spec 均通过 AB Benchmark 后，方可进入 C.2 merge 阶段
