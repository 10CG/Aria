# Phase C · C.2 合并冲突处置报告

> 模拟场景 — **未触碰任何真实仓库**, 下文所有命令均为交回执行者的清单, 我没有执行。
> 依据: `phase-c-integrator` SKILL.md §C.2 / §C.2.4 / §C.2.4.5 / §C.2.5 / §错误处理 +
> `references/pre-merge-gate-empirical-traps.md`。

---

## 0. 结论 (先给判决)

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

  ✅ C.1 完成 → 提交已落地 (feature/oauth2-social-login)
  ⛔ C.2 阻塞 → merge conflict: backend/config/settings.py
     blocking_reason: merge_conflict (非 gate verdict, 非 wait_recoverable)
     working tree: 已 abort, 干净; 未产生任何 merge commit
  ⏭  C.2.4.5 / C.2.5 / C.2.6 / Phase D: 未触达 (合并未发生, 不得执行)

  下一步归属: 回 Phase B, 由**分支作者在 feature 分支上**解冲突, 再重入 Phase C
```

`success: false`。**不**声称 C.2 完成, **不**继续 Phase D。

---

## 1. 立刻不做的四件事 (graceful 的一半是克制)

| ⛔ 不做 | 为什么 |
|--------|--------|
| `git checkout --ours/--theirs backend/config/settings.py`, `git merge -X ours/theirs` | settings.py 的冲突是**语义**冲突不是文本冲突。整边取舍会静默丢掉另一边的 key/列表项 —— OAuth2 分支典型改动 (`AUTHENTICATION_BACKENDS` / `INSTALLED_APPS` / `SOCIAL_AUTH_*`) 与主干同期改动往往落在同一 hunk, 取舍即丢配置, 且**不会红** (进程能起来, 只是某个 backend 没注册) |
| AI 自行猜测合并结果并提交 | 该文件的正确合并结果需要产品/作者的意图 (启用哪些 provider、backend 顺序、env 变量命名), 不是 diff 能推出来的 |
| 为"绕过去"而调配置: `pre_merge_gate.enabled=false` / `submodule_gate.mode=off` / 直接推 target 分支 | Rule #10: enabled 的闸门不得由 AI 自行豁免。冲突不构成豁免理由 |
| 在 target 分支 (main/master) 上就地解冲突后 push | 产出的树**从未被 CI 验过** —— PR 那份 green 描述的是冲突前的树。而且这是对共享主干的外向、难撤销的写, 需显式授权 |

---

## 2. 现场固定 (第一步)

冲突可能出现在两个位置, 处置一致但命令不同:

```bash
# 判断当前处于哪种未完成状态 (输出只看状态, 不打印文件内容)
git status --porcelain=v2 --branch | head -5
ls .git/MERGE_HEAD .git/rebase-merge .git/rebase-apply 2>/dev/null

# 分别对应:
git merge  --abort     # C.2 merge 态冲突
git rebase --abort     # branch-manager C.2.1 sync rebase 态冲突
```

**先 abort 再分析**: 保持工作树处于已知干净状态, 让后续所有核验 (fetch / ls-tree / diff) 结论可信。
冲突信息不会因 abort 丢失 —— 它可被确定性重现 (见 §4)。

**Secret 卫生 (Rule #7)**: `backend/config/settings.py` 是**最可能含 secret 形状值**的文件
(`SECRET_KEY` / `SOCIAL_AUTH_*_SECRET` / DB URL)。所以:

- ⛔ 不把该文件的 `git diff` / 冲突 hunk 正文贴进对话或报告
- ✅ 只用 metadata 描述冲突: 冲突块数、行号区间、**key 名**、两侧各改了哪些 setting 名

```bash
# 只数不看: 冲突块计数 (不泄露值)
grep -c '^<<<<<<<' backend/config/settings.py
# 只取 key 名: 冒号/等号左侧标识符
grep -nE '^[A-Z_]+ *=' backend/config/settings.py | cut -d= -f1
```

---

## 3. 冲突是真的吗 — 先排除"陈旧本地 ref"

冲突的一个常见假象是本地 target ref 陈旧 (fetch 只更新 remote-tracking, 本地 `main`/`master` 会静默腐烂):

```bash
git fetch origin                      # 强制, 失败即 abort (同 §C.2.4.5 Step 1 的 fail-loud 语义)
git rev-parse HEAD                    # 本地 target
git rev-parse origin/<TARGET>         # 远端 target
# 二者不等 ⇒ 先对齐再重测冲突; 冲突可能只是拿旧基线合出来的
```

对齐后用**只读试合**确认冲突仍在, 且拿到精确冲突面 (不改工作树):

```bash
git merge-tree --write-tree --name-only origin/<TARGET> feature/oauth2-social-login
# 或: git merge --no-commit --no-ff <TARGET> ; 记录冲突 ; git merge --abort
```

---

## 4. 冲突性质判定 (要写进交接的实质内容)

`backend/config/settings.py` = **配置面冲突**, 在 OAuth2 social login 这个 change 上属于高危形状:

| 冲突形状 | 典型表现 | 危险点 |
|---------|---------|-------|
| 列表追加撞列表追加 | 两侧都往 `INSTALLED_APPS` / `AUTHENTICATION_BACKENDS` / `MIDDLEWARE` 尾部加项 | git 只能标冲突, **正确解几乎总是"两边都要"**, 但**顺序承重** (auth backend 顺序决定认证优先级, middleware 顺序决定请求链) |
| 新增 env 读取撞重构 | 本分支加 `SOCIAL_AUTH_<PROVIDER>_KEY/SECRET`, 主干把 env 读取方式换了 (`os.environ` → settings helper) | 机械合并后**能 import、能启动**, 但 secret 读不到 ⇒ 运行时 401, 测试可能全绿 |
| 同名 setting 两侧不同值 | `LOGIN_REDIRECT_URL` / `SESSION_COOKIE_*` / `ALLOWED_HOSTS` | 只能由人裁, 二选一有产品语义 |

⇒ 处置结论: **需要作者/owner 裁定**, 不是可自动化的 hunk 合并。报告里给出 key 名清单即可, 不给"我建议这样合"的成品代码。

---

## 5. 冲突在三态里的位置: 既不是 green/wait 也不是 gate 的 fail

`§C.2.4` 的三态 (green / wait / fail) 描述的是 **CI 前置条件**。合并冲突是另一类阻塞, 必须单独标注:

- ⛔ **不是 `wait`**: `wait` 的语义是"再等一会儿条件会自己变好", 由 workflow-runner 走 wait+retry
  (`wait_check_intervals` 退避)。冲突**不会因等待而消失** —— 没有人改 feature 分支, 重试到
  `wait_timeout_seconds` 耗尽也只是白等 30 分钟。这与 traps §四"重试只对 timeout, 确定性失败重试是白等"同形状。
- ⛔ **不是 gate 的 `verdict=fail`**: 那个 fail 的因是 `pr_ci_status in [failing, error]` 或 primitive 出错。
  把冲突塞进同一个字段会让消费方以为 CI 红了, 排查方向被带偏 (同 §C.2.4 对
  `internal-error` 必须与 `git-diff-failed` / `workflow-parse-failed` 区分的理由)。
- ✅ 正确表达: 独立的 `blocking_reason: "merge_conflict"`, terminal block, phase-c-integrator return failure,
  路由目标是**人**(分支作者), 不是重试循环。

---

## 6. 解决路径 (交回执行者)

解冲突**在 feature 分支上做**, 不在合并态做:

```bash
git switch feature/oauth2-social-login
git fetch origin
git merge origin/<TARGET>          # 或 rebase, 按本仓分支策略; 二选一保持一致
#   → 在此解 backend/config/settings.py:
#     - 列表类: 默认"两边都保留", 顺序由作者裁定并在 commit message 说明理由
#     - 同名不同值: 逐条裁, 每条写下选择依据
#     - env/secret: 只改读取方式与 key 名, ⛔ 不把值写进文件 (Rule #7)
git add backend/config/settings.py
git commit                          # Conventional Commits; 正文注明冲突裁定 (Rule #4)
git push origin feature/oauth2-social-login
```

冲突解在 feature 侧的三个理由:
1. 解出来的树会**被 PR 的 CI 重新验证** (推 feature 分支触发), 合并态解则不会;
2. target 分支始终保持可合并、无中间态;
3. 裁定过程留在 PR 里可审, 而不是藏在一个 merge commit 里。

**追加一条**: settings 的语义冲突单靠现有测试通常抓不到 (启动即绿)。建议随解冲突补一条**能红的**断言 ——
例如断言 `AUTHENTICATION_BACKENDS` 同时含 OAuth2 backend 与原有 backend 且顺序符合裁定, 而不是只断言"能 import"。

---

## 7. 重入 Phase C 时必须重跑的闸门 (不是接着往下走)

冲突解决 = 产生了**新的树和新的 changed-file 集合**, 冲突前算出的所有 gate 结论一律作废:

| 步骤 | 为什么必须重跑 |
|------|--------------|
| §C.2.4 pre-merge gate | 新 push ⇒ PR CI 重跑 ⇒ `pr_ci_status` 先变 `pending` (即 `verdict=wait`, 这次**是**合法的 wait), 跑完才可能 green。拿冲突前那次 green 直接 merge = 用旧结论放行新树 |
| §C.2.4 步骤 2.5 path coverage | changed files 变了 (至少多了 settings.py) ⇒ 覆盖判定必须重算; 不可复用旧 `decision` |
| §C.2.4 步骤 2.2 主干存在性核验 | 见 §8, 每次 gate 执行都要做, 不是一次性 |
| §C.2.4.5 submodule gate | 解冲突过程中 `git merge origin/<TARGET>` 可能顺带带入/回退 gitlink; 必须重新做 ancestry 检查 (regression vs divergence) |
| §C.2.5 multi-remote push | 只在**合并成功后**执行。本次未合并 ⇒ 本次不执行 |

---

## 8. 前置核验: 目标分支叫 `main` 还是 `master` (aria-plugin #137)

任务描述里写的是 "merge into **main**"。这是必须**核验而非照抄**的一项:

- SKILL.md §C.2.4 步骤 3 与 §C.2.4 触发条件都注明: `<MAIN_BRANCH>` 取**本项目主干的真实名字**;
  **本项目 (Aria) 是 `master`, 不是 `main`**。照抄字面 `main` 正是 #137。
- 根本形状 (traps §五): backend **结构上无法区分**"分支不存在"与"分支没有正在跑的构建" —— 两者都返
  `InFlightStatus(runs=[])` ⇒ 都判 green。所以主干名写错时, Rule #8 的 (b) 腿 (main 无 in-flight) **恒真**,
  等于这道闸门不存在。冲突场景下这一点更要紧: 人会以为"gate 都过了, 只剩冲突", 实际 gate 那一腿从没真跑过。
- 核验判据 (traps §一, 三条都是实测坑):
  - 判据落在**解析出的 ref 名列表**上做**精确字符串比对** (`"refs/heads/" + branch` 是否在列表里);
  - ⛔ 不看退出码 —— `git ls-remote` **零命中也返 `rc=0`**, 用它判存在性 = 永远判存在;
  - ⛔ 不用 glob/pattern —— 参数被当 glob, `mast*` / `m[a]ster` / `maste?` 都会命中 `master`。
- 两种失败必须分开, 不可混:
  `main-branch-not-found` (核验做成了, 结论是不存在) vs `main-branch-verify-failed` (核验本身没做成, 如远端不可达)。
- 位置 (traps §三): 该核验在三道早退之后、path coverage 评估**之前**;
  ⛔ 不得放进 `if cfg.get("path_coverage_enabled", True):` 块内 —— 那样关掉覆盖评估的调用方会连这道核验一起失去。

⇒ 本场景的处置: 在报告里把 target 标为 **未核验**, 并要求执行者先确认真实主干名。
若目标仓确为 Aria 本仓, 则 `main` 不存在 ⇒ 这不只是"冲突", 还是一个 `gate_error.kind=main-branch-not-found`
的 `verdict=fail`, 两个问题都要修。

```bash
# 核验示意: 取 ref 名列表做精确比对, 退出码只用来判"这次核验做成了没有"
git ls-remote --heads origin | awk '{print $2}' | grep -Fxq "refs/heads/<TARGET>" \
  && echo "TARGET_EXISTS" || echo "TARGET_ABSENT_OR_VERIFY_FAILED"
```

---

## 9. 结构化输出

```json
{
  "phase": "C",
  "step": "C.2",
  "success": false,
  "blocking_reason": "merge_conflict",
  "terminal": true,
  "wait_recoverable": false,
  "steps_executed": ["C.1"],
  "steps_blocked": ["C.2"],
  "steps_not_reached": ["C.2.4.5", "C.2.5", "C.2.6", "Phase D"],
  "merge_attempt": {
    "source_branch": "feature/oauth2-social-login",
    "target_branch_as_given": "main",
    "target_branch_verified": false,
    "target_branch_verify_note": "未做 refs/heads 精确比对; Aria 本仓主干为 master (#137)",
    "conflicted_paths": ["backend/config/settings.py"],
    "conflict_class": "config-surface / semantic",
    "auto_resolution_attempted": false,
    "merge_commit_created": false,
    "working_tree_state": "clean (merge --abort executed)"
  },
  "pre_merge_gate": {
    "status": "stale",
    "reason": "冲突解决会产生新树与新 changed-file 集合; 冲突前的 verdict 一律作废, 必须重算"
  },
  "submodule_gate": { "status": "not_run", "reason": "§C.2.4.5 触发条件要求 C.2.4 green 且即将 merge" },
  "multi_remote_push": { "status": "not_run", "reason": "§C.2.5 触发条件为合并成功 (master 已 fast-forward)" },
  "secret_hygiene": {
    "file_contents_echoed": false,
    "note": "settings.py 属高 secret 密度面; 仅以 key 名/行号/冲突块计数描述 (Rule #7)"
  },
  "owner_action_required": [
    "确认目标主干真实分支名 (main vs master)",
    "在 feature/oauth2-social-login 上裁定 settings.py 冲突 (列表顺序 / 同名不同值 / env 读取方式)",
    "push 后重入 Phase C, 重跑 C.2.4 (含 2.2 主干存在性 + 2.5 path coverage) 与 C.2.4.5"
  ]
}
```

---

## 10. 一句话交接

C.2 因 `backend/config/settings.py` 语义冲突**终止**(非等待、非 CI 失败): 现场已 abort 回干净态、未做任何自动取舍、
未产生 merge commit; 冲突应由作者在 feature 分支上裁定并 push, 重入 Phase C 时冲突前的 gate 结论全部作废须重跑;
另外目标分支写作 `main` 尚未核验 —— 本仓主干是 `master`, 主干名错会让 Rule #8 的 in-flight 那条腿恒真 (#137)。
