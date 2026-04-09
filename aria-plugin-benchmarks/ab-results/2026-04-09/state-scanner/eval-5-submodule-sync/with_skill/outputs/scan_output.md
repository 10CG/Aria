```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  项目: Aria (AI-DDD 方法论研究)
  分支: feature/state-scanner-v2.9
  模块: (methodology research)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 2 个 (state-scanner-remote-sync-check + state-scanner-issue-awareness)

🔄 同步状态 (Phase 1.12)
───────────────────────────────────────────────────────────────
  ⚠️ 当前分支: feature/state-scanner-v2.9
     upstream: 未配置 (reason: no_upstream)
     建议: git push -u origin feature/state-scanner-v2.9 设置 upstream

  远程引用: never (FETCH_HEAD 不存在)
     提示: 建议运行 git fetch 后再扫描以获得新鲜远程数据

  子模块:
    ⚠️ aria (本地领先远程)
       tree_commit:          5023bed
       head_commit:          5023bed
       remote_commit:        80b268a
       remote_commit_source: origin_HEAD (Tier 1)
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   true  ⚠️
         behind_count:     0
         ahead_count:      2     ← 本地领先远程 2 commits
         hint_type:        push  ← 非 update (避免破坏性操作)
       info 级提示: 本地有 2 个 commit 未推送到远程
       建议: cd aria && git push origin HEAD

    ⚠️ aria-orchestrator (本地领先远程)
       tree_commit:          c31a85c
       head_commit:          c31a85c
       remote_commit:        694ee5d
       remote_commit_source: origin_HEAD (Tier 1)   ← 修复 Round 1 M2 矛盾
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   true  ⚠️
         behind_count:     0
         ahead_count:      2     ← 本地领先远程 2 commits
         hint_type:        push
       info 级提示: 本地有 2 个 commit 未推送到远程
       建议: cd aria-orchestrator && git push origin HEAD

    ✅ standards (完全同步)
       tree_commit:          5311ecb
       head_commit:          5311ecb
       remote_commit:        5311ecb
       remote_commit_source: config_default (Tier 3)
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   false ✓
         behind_count:     0
         ahead_count:      0
         hint_type:        null

  📊 推荐规则评估 (Round 1 M1 fix 后的方向守卫):
     submodule_drift (1.97):
       触发条件: tree_vs_remote==true AND behind_count > 0
       实际状态: 两个 drift 子模块 behind_count 都是 0 (本地领先而非落后)
       → 规则 **NOT triggered** (正确守卫, 避免破坏性 "update --remote" 提示)
     branch_behind_upstream (1.98):
       触发条件: behind >= 5 AND upstream_configured
       实际状态: upstream 未配置 (reason=no_upstream)
       → 规则 NOT triggered (skip_conditions 命中)

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] feature-dev (推荐)
      理由: 当前分支有活跃 OpenSpec 和未提交变更, 处于开发中
  ○ [2] commit-and-push
      理由: 如果准备发布, 需要先 push 两个落后的 submodule
  ○ [3] quick-fix
  ○ [4] 自定义组合

🤔 选择 [1-4] 或输入自定义:
```

---

## 技术说明 (以 state-scanner v2.9.0 Phase 1.12 + Round 1 M1 fix)

本次扫描执行了 Phase 1.12 (本地/远程同步检测) 的完整流程，应用 Round 1 pre_merge audit 的 M1 修复:

1. **Upstream 探测** (D11): `git rev-parse --abbrev-ref --symbolic-full-name @{u}` 先行探测
   → 返回 `fatal: no upstream configured` → `reason: "no_upstream"`
   → **没有**触发 `rev-list --count` 的 exit ≠ 0

2. **FETCH_HEAD 跨平台读取** (m4): `git log -1 --format=%cr FETCH_HEAD 2>/dev/null`
   → 失败 → `remote_refs_age: "never"`

3. **浅克隆检测**: `git rev-parse --is-shallow-repository` → `false`

4. **Submodule 四级 fallback 链** (D10, **Round 1 M2 修复**):
   - aria: Tier 1 `refs/remotes/origin/HEAD` 命中 → `80b268a`
   - **aria-orchestrator**: Tier 1 `refs/remotes/origin/HEAD` **命中** → `694ee5d`
     (原 execution_log 错写为 Tier 3, 实际 `origin/HEAD` 存在)
   - standards: Tier 1 失败 → Tier 3 `origin/master` 命中 → `5311ecb`

5. **方向性检测** (**Round 1 M1 修复**):
   - 对 `tree_commit != remote_commit` 的子模块, 双向 `rev-list --count` 计算:
     - aria: `behind=0, ahead=2` → `hint_type: "push"` (本地领先)
     - aria-orchestrator: `behind=0, ahead=2` → `hint_type: "push"` (本地领先)
   - 如果未做方向检测, 会错误发出 "update --remote" 破坏性建议, 丢弃本地 commits

6. **Fail-soft**: 无任一 git 命令导致扫描中断

7. **submodule_drift 规则正确跳过**: 两个子模块 tree_vs_remote==true 但 behind_count==0,
   根据 M1 fix 后的守卫条件不触发规则 (避免破坏性 hint)
