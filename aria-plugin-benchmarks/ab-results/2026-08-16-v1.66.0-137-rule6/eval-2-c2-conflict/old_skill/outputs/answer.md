# Phase C — C.2 合并冲突处置报告

> Skill: phase-c-integrator v1.3.0 (snapshot) | 步骤: C.2 (branch-manager merge action)
> 场景: 模拟执行 (simulated) — 未对任何真实仓库执行写操作

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  C.1 commit-msg-generator  → Git 提交            (已完成 / 无新变更)
  C.2 branch-manager        → 合并 PR             ⛔ 阻塞

🚀 执行中...
───────────────────────────────────────────────────────────────
  ✅ C.2.4   pre-merge precondition gate → 见下方「门状态」
  ⛔ C.2 merge → CONFLICT: backend/config/settings.py
```

---

## 1. 事实确认 (先理解现状, 不先动手)

| 项 | 值 |
|----|----|
| 源分支 | `feature/oauth2-social-login` |
| 目标分支 | `main` |
| 冲突文件 | `backend/config/settings.py` (1 个) |
| 冲突发生位置 | C.2 `branch-manager merge action` — **不是** C.2.4 pre-merge gate 的判定项 |
| 当前 verdict | **BLOCKED** — 合并未发生, 工作树/远程均无变化 |

**归层澄清 (重要, 避免误报门失效)**: 本 SKILL §C.2.4 pre-merge precondition gate 的三态 (`green` / `wait` / `fail`) 只覆盖两个轴 —— 本 PR CI 状态 + main 是否有 in-flight CI run;§C.2.4.5 只覆盖 submodule pointer ancestry。**文本冲突不在任何一个 gate 的判据里**, 因此:

- gate 判 `green` 与本次冲突并不矛盾, 不要把冲突当成 gate 漏判去"修 gate";
- 反过来也不能因为 gate 是 `green` 就对 merge 失败做重试/加 `-X ours` 之类的强行推进。

冲突是 branch-manager merge action 阶段的**终止性失败**, 按本 SKILL §错误处理表「远程冲突 → 提示拉取最新代码」处置, 即回到分支侧同步 + 人工消解, 而非在合并侧绕过。

---

## 2. 立即动作: 停 + 复位 (不留半合并状态)

合并冲突时 git 会留下 `MERGING` 中间态。**在消解方案确定前, 先把仓库恢复到干净可解释的状态**, 否则后续任何 gate/审计读到的都是半态:

```bash
# 只读诊断 (先看, 不改)
git status --porcelain            # 确认仅 backend/config/settings.py 处于 UU
git diff --name-only --diff-filter=U
git log --oneline main..feature/oauth2-social-login   # 本分支引入了什么
git log --oneline feature/oauth2-social-login..main   # main 上我落后了什么

# 复位 (在 main 侧不留痕迹)
git merge --abort
```

**明确不做的事** (这几条都是把冲突"消失"而不是"解决"):

- ❌ `git merge -X ours` / `-X theirs` — 对 settings.py 这种**配置聚合文件**必然静默丢配置;
- ❌ `git checkout --ours/--theirs backend/config/settings.py` 整文件取一侧;
- ❌ `git push --force` 到 `main`;
- ❌ 在 Forgejo Web UI 点 "resolve conflicts" 在线编辑 —— 消解结果不经本地测试、也不经 C.2.4 重跑。

---

## 3. 消解策略: 回到分支侧, 而不是在 main 侧硬合

正确方向是**让 feature 分支先吸收 main**, 消解在 feature 分支上完成并经过验证, 再让 main 做一次干净的合并 (对应 branch-manager 的 C.2.1 sync rebase 语义):

```bash
git fetch origin
git switch feature/oauth2-social-login
git rebase origin/main        # 或 git merge origin/main, 按项目分支策略
# → 在 backend/config/settings.py 上消解
```

### 3.1 `backend/config/settings.py` 的消解原则

这个文件几乎必然是**双方各自新增/修改配置键**造成的冲突, 属于「两侧都要保留」的语义合并, 不是二选一:

1. **逐 hunk 判定**, 不整文件取侧。对每个冲突块先答: 这是 (a) 双方新增不同键 → **两侧都留**; (b) 双方改同一个键的值 → **必须判定哪个是意图**, 拿不准就问 owner; (c) 一侧删除一侧修改 → 默认按删除方的 Spec 意图, 但必须确认 OAuth2 侧是否依赖它。
2. OAuth2 分支典型新增: `AUTHENTICATION_BACKENDS` 追加项、`INSTALLED_APPS` 追加 social 相关 app、`OAUTH2_PROVIDERS` / `SOCIAL_AUTH_*` 配置块、回调 URL、scope 列表。**列表/字典类配置的冲突几乎全是 (a) 类, 应做并集而非取侧** —— 取侧会让 main 上他人已 ship 的 backend/app 静默消失。
3. **敏感值不进代码**: client_id / client_secret 一律走环境变量 (`os.environ` / `.env`), 消解过程中不得把任何 secret 字面量写进 settings.py, 也不得把 secret 值打印到终端 (Rule #7)。若冲突块里出现了疑似明文凭据, 停下来先报 owner。
4. 消解后**通读整个 hunk 的上下文**, 而不只看冲突标记之间那几行 —— settings.py 常有"后面的赋值覆盖前面"的顺序语义, 并集写对了但顺序放错同样是错的。
5. 清干净 `<<<<<<<` / `=======` / `>>>>>>>` 标记 (`grep -n '^<<<<<<<\|^=======\|^>>>>>>>' backend/config/settings.py` 应为空)。

### 3.2 消解后必须重新验证 (不能沿用冲突前的绿)

冲突消解产生的是**一份谁都没测过的新代码**, Phase B 的 `test_results.passed=true` 对它不成立:

```bash
python -c "import backend.config.settings"     # 最起码: 文件能 import
<项目测试命令>                                   # 全量或至少 auth/config 相关套件
```

- 配置文件的错误特征是**运行时才炸**, 单测常绕开它 → 建议额外做一次真实启动 (dev server / app factory) 冒烟。
- 两侧配置的**交互**是并集合并的真正风险面 (例如 main 新增的中间件与 OAuth2 回调路由顺序), 只跑各自分支的老用例测不到。

---

## 4. 重新进入 C.2 的完整路径 (不能从冲突点"接着合")

消解 + 验证通过后, **重新走一遍 C.2, 而不是直接调 merge**:

```yaml
1. C.1 (commit-msg-generator):
   - 消解 commit 单独成 commit, message 说明"合并 main 并消解 settings.py 冲突"
   - 遵循 Conventional Commits (Rule #4)
   - 增强标记: 🤖 Executed-By / 📋 Context / 🔗 Module

2. 推送 feature 分支 → PR 自动更新 (PR 号不变)

3. C.2.4 pre-merge precondition gate — **必须重跑, 不复用冲突前结果**:
   - 新 commit ⇒ 需要新的 PR CI run; 旧 run 的 passing 已对不上当前 HEAD
   - `aether ci status --branch feature/oauth2-social-login --json` → pr_ci_status
   - `aether ci status --branch main --in-flight --json` → main in-flight
   - verdict: pending → wait+retry; failing → BLOCK; passing + main 无 in-flight → green
   - 注意: 冲突消解期间 main 又前进了, main 侧很可能正有 in-flight run ⇒ 大概率先落 `wait`

4. C.2.4.5 submodule pointer regression gate:
   - 本次 rebase/merge 把 main 的 submodule gitlink 拉了进来, 存在 pointer 被带回旧 SHA 的风险
   - 必须确认每个 submodule 是 forward bump / no-change, 不是 REGRESSION 或 DIVERGENT

5. gate 全绿 → branch-manager merge action

6. C.2.5 multi-remote push enforcement:
   - master 合并后逐 remote 推送 + post-push SHA 核验
```

**闸门不因"只是消解冲突"而豁免** (Rule #10): 冲突消解是一次真实的代码变更, C.2.4 / C.2.4.5 都必须按配置照跑, 不得以"改动小 / 只是合并"为由跳过或降级。

---

## 5. 结构化输出

```yaml
success: false
blocked_at: "C.2 (branch-manager merge action)"
steps_executed: [C.1, C.2.4]
steps_blocked: [C.2-merge]
steps_not_reached: [C.2.4.5, C.2.5, C.2.6]

failure:
  type: merge_conflict
  scope: text_conflict            # 非 gate verdict, 非 CI failure
  conflicted_files:
    - path: "backend/config/settings.py"
      resolution_class: "semantic_union"   # 配置聚合文件, 需并集而非取侧
  repo_state_after_handling: "clean (merge --abort executed)"
  merge_performed: false
  remote_mutated: false

gate_status:
  pre_merge_gate: "green (合并前), 消解后必须重跑 — 结果已失效"
  submodule_gate: "not_reached"

next_action:
  owner: "human + AI 协作 (settings.py 语义需人工确认)"
  path:
    - "feature 分支 rebase/merge origin/main"
    - "逐 hunk 消解 settings.py (并集优先, 值冲突需 owner 判定)"
    - "重跑测试 + 启动冒烟"
    - "C.1 提交 → 推送 → C.2.4 重跑 → C.2.4.5 → merge → C.2.5"

context_for_next:
  branch_name: "feature/oauth2-social-login"
  base_branch: "main"
  requires_human_decision: true
  decision_points:
    - "settings.py 中双方修改同一配置键时以哪侧为准"
    - "OAuth2 provider secret 的注入方式确认 (必须环境变量, 不入库)"
```

---

## 6. 给用户的话 (需确认的点)

冲突已被安全拦下, `main` 未被改动, 本地也已复位到干净状态。要继续需要你定两件事:

1. **分支策略**: 用 `rebase origin/main` (线性史, 推荐) 还是 `merge origin/main` (保留合并史)?
2. **settings.py 值冲突的裁决**: 我会先做逐 hunk 并集消解并把 (b) 类"双方改同一个键"的位置逐条列给你, 由你定值 —— 这类判定我不代你做。

确认后我按 §4 的顺序重新走完 C.2, 包括重跑 C.2.4 / C.2.4.5 两道闸门。
