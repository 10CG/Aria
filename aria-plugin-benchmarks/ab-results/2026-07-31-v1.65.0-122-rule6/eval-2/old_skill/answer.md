# Phase C C.2 合并冲突处理 — 描述性推演 (old_skill 臂)

> 场景前提: 正在把 `feature/oauth2-social-login` 合入 `main`, 在 `backend/config/settings.py` 检测到冲突。
> 按 phase-c-integrator SKILL (v1.2.0 快照) 的指令推演处理流程, 不实跑任何命令。

---

## 1. 入口判定与配置加载

**我应该使用这个 Skill 吗?** — 是。场景属于"需要合并分支 / 开发完成后的集成阶段", 命中使用场景; C.1 (提交) 假定已完成 (分支已就绪待合并), 本次聚焦 C.2。

**config-loader**: 执行前先读 `.aria/config.json`, 关键取值 (缺失用默认):

- `audit.enabled` (默认 false) + `audit.checkpoints.pre_merge` — 决定是否触发 pre_merge 审计
- `phase_c_integrator.pre_merge_gate.enabled` (默认 true) — C.2.4 CI gate
- `phase_c_integrator.submodule_gate.mode` (默认 block) — C.2.4.5 submodule pointer gate
- `phase_c_integrator.pre_merge_gate.no_ci_fallback` (默认 skip_with_warning)
- `phase_c_integrator.multi_remote_push.enabled` (默认 true) — C.2.5

## 2. 冲突在流程中的定位

SKILL §C.2.4 的命名空间澄清指出: branch-manager 内部实现层负责 C.2.1 sync / C.2.2 push / C.2.3 create-PR / C.2.4 wait-approval / C.2.5 merge。**merge 冲突最可能浮现的位置是 branch-manager 的 sync 步骤** (把 `main` 最新提交 rebase/merge 进 feature 分支时), 或服务端合并前的冲突预检。本场景: `feature/oauth2-social-login` 与 `main` 在 `backend/config/settings.py` 各自有改动 (典型情况: OAuth2 分支加了 `SOCIAL_AUTH_*` / OAuth client 配置项, `main` 上其他 PR 同期改了同一配置区块), 产生了文本冲突。

按 SKILL「错误处理」表: **推送失败 / 远程冲突 → 提示拉取最新代码** — 即冲突不是静默吞掉, 也不是自动强行解决, 而是**停下、报告、引导修复**。graceful 的含义:

- 不做任何破坏性操作 (不 force push, 不丢弃任一侧改动, 不自动挑边)
- 保留现场 (冲突标记留在工作区, 或 abort 回到干净状态, 二选一并明确告知用户)
- 输出结构化失败报告, 把"如何修"的具体命令给到用户

## 3. 冲突处理流程 (逐步推演)

### Step 1 — 检测与即时止损

merge/rebase 返回非零 + `git status` 显示 `both modified: backend/config/settings.py`。此时:

- **立即停止流水线推进**: 不继续 C.2.4 gate、不调用 merge API、不进入 C.2.5 多远程推送。冲突未解决前后续步骤全部无意义且危险。
- 快照冲突上下文: 冲突文件清单 (本例仅 1 个)、两侧最近触碰该文件的 commit (`git log main -- backend/config/settings.py` / 同 feature 侧)、冲突 hunk 数。

### Step 2 — 输出冲突报告 (对齐 SKILL 输出格式风格)

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

C.2 合并: feature/oauth2-social-login → main
  状态: 阻塞 (BLOCKED) — 合并冲突

冲突详情
───────────────────────────────────────────────────────────────
  文件: backend/config/settings.py
  类型: both modified (main 与 feature 分支同时修改)
  main 侧最近变更:    <sha-main>  <该 commit 标题>
  feature 侧最近变更: <sha-feat>  feat(auth): OAuth2 social login 配置

处理建议
───────────────────────────────────────────────────────────────
  1. 拉取最新 main 并在 feature 分支本地解冲突:
     git fetch origin
     git checkout feature/oauth2-social-login
     git rebase origin/main        # 或 git merge origin/main, 按项目分支策略
  2. 编辑 backend/config/settings.py 解决冲突:
     - settings.py 是配置文件, 冲突大概率是"两侧各加了配置项" →
       通常正确解法是保留双方新增 (union), 而非二选一
     - 但必须逐 hunk 人工确认: 若冲突落在同一配置键 (如同一
       中间件列表 / INSTALLED_APPS / 同名环境变量默认值), 需要
       语义裁决, 不能机械合并
  3. 解决后: git add backend/config/settings.py && git rebase --continue
  4. 重新运行测试 (validation 必须重做, 见 Step 4)
  5. 重新推送: git push origin feature/oauth2-social-login --force-with-lease
     (rebase 改写历史才需要 force-with-lease; merge 方式则普通 push)
  6. 重新进入 Phase C.2 流程
```

要点: 引导性输出用普通数字编号; 提示 `--force-with-lease` 而非 `--force` (仅 rebase 路径需要, 且要先确认远端无他人新提交)。

### Step 3 — 冲突解决策略判定 (settings.py 特殊性)

`backend/config/settings.py` 是后端配置文件, 推演其冲突性质分两类:

| 冲突形态 | 判定 | 处置 |
|----------|------|------|
| 两侧各自**新增**不同配置块 (feature 加 OAuth2 provider keys, main 加了别的配置) | 低风险, 结构性可并存 | union 合并: 两侧都保留, 注意去重 import 与末尾逗号/格式 |
| 两侧修改**同一配置键** (如同一 AUTHENTICATION_BACKENDS 列表、同一超时值) | 语义冲突, 需要裁决 | 不自动挑边; 呈报两侧意图, 由用户/开发者确认最终值; 涉及安全相关键 (secret key 引用、callback URL 白名单) 时尤其不得静默取舍 |

同时做一个**secret 卫生检查** (Rule #7 意识): OAuth2 分支的 settings.py 常涉及 client_id/client_secret — 解冲突时确认 secret 只以环境变量/secret store 引用出现, 不因手工合并把明文凭据带进最终文件; 呈现冲突 hunk 给用户时如含疑似明文 secret, 用 redact 形式展示。

### Step 4 — 解决后的重新验证 (不可跳过)

冲突解决改动了即将合入的代码, 因此之前 Phase B 的 `test_results` / branch-finisher 的 `validation_report` 对新树**失效**。graceful 处理必须包含:

- 重跑测试套件 (至少后端配置相关 + auth 模块测试), 更新 validation_report
- 若 `audit.enabled=true` 且 `pre_merge != "off"`: pre_merge audit 需基于**解冲突后的新 diff** (branch vs base) 重新执行 — 旧 verdict 不能沿用, 因为审计对象已变
- 这一步与 Rule #10 一致: 已启用的闸门不因"只是解了个冲突"而豁免或降级

### Step 5 — 重新走 C.2 门链 (解冲突后)

按 SKILL 顺序完整重跑, 不因重试而缩水:

1. **pre_hook audit** (如启用): audit-engine pre_merge 检查点, verdict PASS / PASS_WITH_WARNINGS → 继续; FAIL → 再次阻塞并出报告
2. **推送 + PR 更新**: branch-manager 推新分支头; 已有 PR 则更新, 无则创建
3. **C.2.4 pre-merge precondition gate** (enabled=true 默认):
   - backend resolution (`resolve_ci_backend`, Aether-first)
   - 查本 PR CI 状态 + main in-flight — 注意解冲突后新 push 会触发新 CI run, 初查大概率 `pending` → verdict=wait → 走 workflow-runner wait+retry (默认间隔 `[30,60,120,300,300]` 秒, 上限 1800s)
   - CI passing 且 main 无 in-flight → green; failing → fail 阻塞 (如果冲突解错导致测试挂, 会在这里被兜住)
   - stub backend 抛 NotImplementedError → abort 不降级 (Hard Constraint #7); 无可用 backend → 按 `no_ci_fallback` (默认 skip_with_warning)
4. **C.2.4.5 submodule gate** (mode=block 默认): 本场景冲突文件是普通 Python 文件非 gitlink, 预期各 submodule 为 no-change → pass; 若碰巧有 pointer regression 会独立 block, 与本冲突无关但同样不放行
5. **merge 执行**: gate 全 green 后调 branch-manager merge。若 gate 与 merge 间 main 又进了新 commit 导致**再次冲突** — 这是 SKILL 已知的 race window (窗口最小化但不消除), 处理方式回到 Step 1 循环, 不 force
6. **C.2.5 multi-remote push**: 合并成功后快照 `expected_sha`, 枚举 submodule, 对每个 enforced remote 推送 + `verify_parity_post_push` SHA 核验; 任一失败按失败优先级表决策 (默认 `fail_on_partial_push: true` → 阻断 + 输出逐 remote 修复命令)
7. **C.2.6** (仅 `upm.milestone_driven=true` 时): commit message 含 US-XXX 则追加 UPM sub-bullet

### Step 6 — 最终输出

成功路径 (冲突已解、门链全过):

```yaml
success: true
steps_executed: [C.2]
results:
  C.2:
    pr_url: "https://.../pulls/<N>"
    pr_number: <N>
    pre_merge_verdict: "green"
    gate_verdict: "pass"          # submodule gate
    conflict_resolution:
      file: "backend/config/settings.py"
      strategy: "manual union merge + 逐 hunk 语义确认"
      revalidated: true           # 测试重跑通过
context_for_next:
  commit_sha: "<merge 后 master HEAD>"
  pr_url: "https://..."
  ready_for: Phase D
```

用户未及时解冲突 / 放弃本次合并的路径: 返回 `success: false` + 上文冲突报告, PR 保持 open, 工作区回到干净状态 (rebase --abort 或 merge --abort), 不留半合并残局 — 这就是"handle gracefully"的最终形态: **流程阻塞但状态无损、路径可续**。

## 4. 本推演遵循的关键纪律小结

- 冲突 = 阻塞信号, 不 force、不自动挑边、不静默吞错; 报告 + 引导 + 保留现场
- 解冲突后所有已启用闸门 (audit / C.2.4 CI gate / C.2.4.5 submodule gate) 基于新状态完整重跑, 不以"重试成本"为由降级 (Rule #10)
- settings.py 类配置冲突: 结构性新增走 union, 同键语义冲突交人裁决; 顺带做 secret 卫生检查 (Rule #7)
- merge 后仍须完成 C.2.5 多远程推送 + SHA parity 核验才算 C.2 闭环
