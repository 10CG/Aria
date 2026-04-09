```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  项目: Aria (AI-DDD 方法论研究)
  分支: feature/state-scanner-v2.9
  模块: (methodology research)
  变更: 4 文件 unstaged + 4 untracked (openspec/ + audit-reports/)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: OpenSpec + 审计报告 (docs/spec)
  复杂度: Level 2
  架构影响: 有 (system-architecture.md 1.7→1.8)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置 (docs/requirements/)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 2 个 (state-scanner-remote-sync-check + state-scanner-issue-awareness)
  已归档: 多个

🔄 同步状态
───────────────────────────────────────────────────────────────
  ⚠️ 当前分支: feature/state-scanner-v2.9
     upstream: 未配置 (reason: no_upstream)
     建议: 首次 push 用 git push -u origin feature/state-scanner-v2.9 设置 upstream

  远程引用: never (FETCH_HEAD 不存在, 未做过 git fetch)
     提示: 建议运行 git fetch 后再扫描以获得新鲜远程数据

  子模块:
    ⚠️ aria  (3/3 状态异常)
       tree_commit:   5023bed (主仓库记录)
       head_commit:   5023bed (工作目录 HEAD, 已对齐)
       remote_commit: 80b268a (origin/HEAD)
       remote_commit_source: origin_HEAD (Tier 1 成功)
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   true  ⚠️ (主仓库记录落后远程 1 个 commit)
       修复建议: git submodule update --remote aria

    ⚠️ aria-orchestrator
       tree_commit:   c31a85c
       head_commit:   c31a85c
       remote_commit: 694ee5d (origin/master, Tier 3 config_default fallback 生效)
       remote_commit_source: config_default
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   true  ⚠️ (本地领先远程, 主仓库记录包含未推送的 commits)
       说明: 本地超前远程是罕见情况，通常意味着子模块有未推送的 commits
       修复建议: cd aria-orchestrator && git push origin master

    ✅ standards (同步)
       tree_commit:   5311ecb
       head_commit:   5311ecb
       remote_commit: 5311ecb (origin/master, Tier 3 fallback)
       remote_commit_source: config_default
       drift:
         workdir_vs_tree:  false ✓
         tree_vs_remote:   false ✓

  🛑 推荐规则触发: submodule_drift
     发现 2 个 submodule 存在 tree_vs_remote 偏差 (aria, aria-orchestrator)
     这不阻断其他推荐, 但建议优先处理以免在陈旧代码上做分析

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] sync-and-continue (推荐)
      理由: 发现 submodule drift, 建议先 git submodule update --remote aria
            然后再继续当前的 OpenSpec 工作
  ○ [2] feature-dev (继续开发)
      理由: 当前分支有未提交的 OpenSpec 变更
  ○ [3] quick-fix
  ○ [4] 自定义组合

🤔 选择 [1-4] 或输入自定义:
```

---

## 技术说明 (以 state-scanner v2.9.0 Phase 1.12 实现)

本次扫描执行了 Phase 1.12 (本地/远程同步检测) 的完整流程：

1. **Upstream 探测** (D11): `git rev-parse --abbrev-ref --symbolic-full-name @{u}` 先行探测
   → 返回 `fatal: no upstream configured`
   → 安全降级为 `ahead: null, behind: null, reason: "no_upstream"`
   → **没有**触发 `rev-list --count` 的 exit ≠ 0 (修复 M3 验证通过)

2. **FETCH_HEAD 跨平台读取** (m4 修复): `git log -1 --format=%cr FETCH_HEAD 2>/dev/null`
   → 命令失败 (FETCH_HEAD 不存在) → 降级为 `remote_refs_age: "never"`
   → **没有**使用 `stat -c %Y` (不跨平台)

3. **浅克隆检测**: `git rev-parse --is-shallow-repository` → `false`
   → git 版本 ≥ 2.15，无需 fallback 到 `.git/shallow`

4. **Submodule 四级 fallback 链** (D10):
   - aria: Tier 1 `refs/remotes/origin/HEAD` 命中 → `80b268a`
   - aria-orchestrator: Tier 1 失败 (无 origin/HEAD) → Tier 3 `origin/master` 命中 → `694ee5d`
   - standards: Tier 1 失败 → Tier 3 `origin/master` 命中 → `5311ecb`
   - **未触发 ls-remote (Tier 2)**，符合 `check_remote: false` 默认配置 (不主动发网络请求)

5. **Fail-soft 验证**: 所有场景中没有任一 git 命令导致整个扫描中断 (D4 + D9 定义的 fail-soft)

6. **submodule_drift 推荐规则触发**: 2/3 submodule 有 `tree_vs_remote: true`，降级提示 (非阻断)
