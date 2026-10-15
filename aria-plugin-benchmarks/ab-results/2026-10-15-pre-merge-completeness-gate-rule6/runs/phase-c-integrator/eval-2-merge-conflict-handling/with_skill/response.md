# Phase C C.2 merge 冲突处理推演 — `feature/oauth2-social-login` → 主干, 冲突于 `backend/config/settings.py`

> **产出形态**: 描述性推演 (benchmark 约束)。本文所有命令均为「按 skill 规定应当执行什么」的推演, **未实际执行任何 git 读写 / fetch / forgejo 调用**。
> **依据**: `aria/skills/phase-c-integrator/SKILL.md` (C.2 编排 + §C.2.4 / §C.2.4.5 / §C.2.5) → 实现层 `aria/skills/branch-manager/SKILL.md` (C.2.1-C.2.5) → SOT `standards/core/ten-step-cycle/phase-c-integration.md` (Step 8 + Common Issues → Merge Conflicts) + `references/pre-merge-gate-empirical-traps.md`。

---

## 0. 场景先决校正 (动手前必须做的三个核实)

冲突处理本身之前, 按 skill 的教训先校正三个事实面, 否则后续每一步都在错的地基上:

1. **主干名: Task 写 `main`, 但不得照抄字面。** phase-c-integrator SKILL.md §C.2.4 明文 (aria-plugin #137 事故): `<MAIN_BRANCH>` 必须取本项目主干**真实名字** —— 本仓 (Aria) trunk 是 **`master`**, 不是 `main`; helper `pre_merge_gate.py` 的 CLI 缺省恰是 `--main-branch main` (脚本 `main()` 里 `default="main"`), 查一个不存在的分支会返回「没有在跑的」⇒ CI 门恒放行。因此本场景落到本仓时: merge 目标与后续 gate 查询一律用 `master` / `origin/master`。若这是**消费方项目** (见下条), 则先用 `git symbolic-ref refs/remotes/origin/HEAD` 或解析 `git ls-remote` ref 列表做**精确字符串比对**核实 trunk 真名 (⛔ 不看退出码 — 零命中也返 rc=0; ⛔ 不用 glob — `mast*` 会命中 `master`), 不假设为 `main`。
2. **路径核实: `backend/config/settings.py` 在 Aria 仓不存在** (本仓无 `backend/` 目录, 已只读核实)。⇒ 场景属于使用 Aria 方法论的消费方项目 (如 SilkNode 类 backend 服务)。推演按 skill 的通用 C.2 流程执行, 所有仓特定参数 (trunk 名 / remote 集 / CI backend) 按消费方项目实际配置取值。
3. **分支名合规性**: `feature/oauth2-social-login` 不符合 branch-manager 命名规范 `{type}/{module}/{task-id}-{desc}` (缺 module / task-id 段)。不阻断合并, 但属于流程偏差, 记入 handoff / workflow report 一笔, 供 cycle 复盘。

**定位结论**: merge conflict 在 Aria 流程里**不是异常路径**, 是 SOT (`phase-c-integration.md` §Common Issues → Merge Conflicts) 与 branch-manager 错误处理表 («Rebase 冲突 | develop 有新变更 | 手动解决冲突后 `git rebase --continue`») 明文列出的**常见分支**, 有既定处置程序。"Handle gracefully" = 走这条既定程序, 不发明新动作。

---

## 1. 冲突在 C.2 流程中的位置

C.2 编排 (orchestrator-tier, phase-c-integrator) 委托 branch-manager (implementation-tier) 执行, 门在后:

```
branch-manager C.2.1  sync: git fetch origin <trunk> + git rebase origin/<trunk>   ← ★ 冲突的正常暴露点
branch-manager C.2.2  push 分支 (rebase 后需 --force-with-lease)
branch-manager C.2.3  创建 PR (Forgejo API, 前置 PRE_CHECK Cloudflare Access 检查)
phase-c-integrator §C.2   pre_hook: audit-engine pre_merge 检查点 (若 audit.enabled 且优先级链判启用)
phase-c-integrator §C.2.4 pre-merge precondition gate (CI 三态: green/wait/fail)
phase-c-integrator §C.2.4.5 submodule pointer regression gate (默认 block)
branch-manager C.2.4-C.2.5  等待审批 + merge
phase-c-integrator §C.2.5 multi-remote push + 逐 remote SHA 核验
```

冲突出现的两种姿势, 处置面不同, **先判别再动手**:

| 姿势 | 触发点 | ours/theirs 语义 |
|------|--------|------------------|
| **A. rebase 冲突** (常态) | C.2.1 `git rebase origin/<trunk>` | `ours` = 主干侧被 replay 的基底, `theirs` = 本 feature commit — **与 merge 相反** |
| **B. 本地 merge 冲突** | merge action (auto_merge 前 / 子模块本地合并, 见 §3 多远程约束) | `ours` = 主干 (HEAD), `theirs` = `MERGE_HEAD` = feature |

判别方法 (推演): `git status` 看是 `rebase in progress` 还是 `You have unmerged paths`; 这决定 continue 用 `git rebase --continue` 还是 `git merge --continue`, 也决定读冲突块时哪一侧是哪个意图 — **搞反语义是 settings.py 冲突最常见的二次事故来源**。

---

## 2. Graceful handling — 处置程序 (推演, 逐条)

### 2.1 稳住状态: 只读侦察, 不破坏现场

- **禁止动作先行**: 不 `git push --force`(裸 force)、不 `git reset --hard`、不 `git checkout --<file>` 丢侧、不 `-X ours` / `-X theirs` 盲策略对付 settings.py (配置聚合文件, 机械选边 = 静默丢一侧配置键, 属语义级破坏)。
- 侦察 (只读):
  - `git status --porcelain` + `git diff --name-only --diff-filter=U` → 确认冲突文件清单。本场景 = `backend/config/settings.py` 单文件; 若实际清单更长, 以实测为准逐文件处理。
  - `git log --oneline --merge -- backend/config/settings.py` → 看两侧各自改了什么 (谁动了 OAuth 配置块, 谁动了别的 settings)。
  - `git diff` (带冲突标记) → 读 `<<<<<<< / ======= / >>>>>>>` 三段, 分别对应两侧意图。

### 2.2 语义解决: 双侧意图并集, 不是选边

`settings.py` 是配置聚合点, OAuth2 social login feature 侧的典型意图 = 新增 `oauth2_providers` / `client_id` 类配置块与开关; 主干侧意图 = 期间合入的其他配置变更 (别的 feature 动了相邻行)。解决原则:

- **双侧语义都保留** (union of intent): feature 侧新增的 OAuth 配置键完整落位, 主干侧同期变更完整落位; 只有同键同属性真互斥时才做语义裁决, 且裁决理由要能写进 handoff。
- **Secret 卫生 (Rule #7)**: OAuth2 场景的 settings 冲突高概率夹带 client secret / token 类字面量。处置时 stdout/stderr 不得流入 chat 可见通道 (Bash 强制 `>/dev/null 2>&1`); 侦察与验证用 metadata (键名 / status code / 长度), **不回显 secret value 字面**; 例外须 `# secret-leak-ok-explicit` + 理由 + owner sign-off — 本场景不构成例外。
- 解决后自查: `python -c "import backend.config.settings"` (或项目等价的导入冒烟) 确认文件语法完整、两侧键齐全 — 冲突标记残留会在导入时立刻炸, 这是最便宜的机械验证。

### 2.3 收敛提交

- `git add backend/config/settings.py`
- 姿势 A: `git rebase --continue`; 姿势 B: `git merge --continue` (或 `git commit` 收尾 merge commit)。
- 过程中产生的提交信息遵循 Conventional Commits (Rule #4): 如 `chore(config): merge oauth2 settings with upstream changes` 性质的描述; merge commit 不引入无关变更。

### 2.4 解决冲突 = 代码变更 ⇒ B.2 验证义务重开

这是最容易被「赶合并」跳过的一步: 冲突解决产生了主干上从未存在过的新代码形态, **必须重跑受影响验证**再进入后续步骤:

- settings 加载 / 导入冒烟 (上条) + 本模块相关单测 (auth / oauth2 相关测试面);
- 消费方项目按其 B.2 验证面执行; 结果进 workflow report。

### 2.5 失败回退 (安全出口)

解决过程中状态不可收拾 (误 add、语义裁决推翻、冲突面扩大) → `git rebase --abort` (姿势 A) / `git merge --abort` (姿势 B), 回到尝试前状态, **分支与主干均无损**。abort 不是失败, 是 skill 错误处理表里的正常恢复操作 («如果 rebase 出错, 中止»)。

### 2.6 推送与 PR

- 姿势 A (rebase 过) → C.2.2: `git push --force-with-lease origin feature/oauth2-social-login` (branch-manager 明文允许 rebase 后 force-with-lease; ⛔ 裸 force)。
- 姿势 B → merge 完成后常规 push。
- 重新 push 会触发 PR 的 CI 重跑 — 这正是 §C.2.4 门要等的东西, 不要在 CI 重跑完成前抢跑 merge。

---

## 3. 冲突不豁免任何门 — 后续门序列照常 (Rule #8 / Rule #10)

冲突折腾过不构成任何 enabled 闸门的豁免理由 (Rule #10 封闭白名单四类无一命中: config 未显式 off、无 adaptive 映射、无成文 lane 降级、「结构性前提不成立」指审的对象整个未产生 — 而 CI 门 / 审计的对象都产生了)。冲突解决 + 重推后, merge 前完整序列照走:

1. **audit-engine pre_merge 检查点** (若 `audit.enabled=true` 且按 C.2 pre_hook 步骤 3 优先级链判启用): 审计对象是 PR diff (branch vs base) — **冲突解决本身就是 diff 的一部分**, 属被审对象而非豁免理由。`repo_path` / `diff_repo_path` 两者都必传 (同仓合并显式传同值); `base` 传远程跟踪 ref (`origin/master` 形态, 非裸本地分支名 — 裸名在 detached HEAD / 本地 trunk 陈旧时 merge-base 静默偏移)。completeness gate 三态处置: `fail` → 阻塞 + ERROR; `error` (exit 2) → 按 fail 阻塞 (fail-closed); `not_applicable` → workflow report 带 `[INFO]` 行; `unattributed_count > 0` → 带 `[WARN]` 行。
2. **§C.2.4 pre-merge precondition gate** (默认 enabled): `pr_ci_status=passing` + trunk 无 in-flight → green; 注意 MAIN_BRANCH 用真名 (§0 第 1 条)。若重推后观测到 `pr_ci_status=not_found` (远端零 run) → `verdict=wait` + `gate_error.kind=no-run-for-branch`, 按处方 (a) dispatch / (b) 推碰 CI 触发路径的实质 commit / (c) 继续等或放弃 — **AI 不自动执行, 交人**; message 原文必须 surface, 不得缩写成「CI pending」。path coverage: settings.py 属源代码路径, 预期 `covered` (走正常 PR CI wait), 不会触发 `not_applicable` 短路。
3. **§C.2.4.5 submodule pointer gate** (默认 block): 若该 backend 仓是某主仓的子模块, 或本 PR 动了 gitlink — 照跑。冲突解决若曾把子模块指针弄回旧值, 正是这道门要拦的 REGRESSION。
4. **多远程硬约束 (CLAUDE.md, owner 裁决 2026-07-20)**:
   - **约束 1**: 子模块的分支合并一律**本地** `git merge` + 双推, 禁 Forgejo 服务端 merge (服务端 merge commit 会造成 orphaned gitlink / recursive clone 断裂)。本场景的本地冲突处理与该约束同向 — 冲突只能在本地解决, 顺带满足了「本地做合并」。主仓自身 PR 可走 Forgejo merge。
   - **约束 2**: 推后对每个 remote 独立 `git ls-remote <remote> <trunk>` 取 SHA 与本地比对, **全部一致才算推成功**; 不信 push 回执。此即 §C.2.5 multi-remote push enforcement (snapshot `expected_sha` → per-remote 矩阵 → `verify_parity_post_push`)。
5. merge 成功后: branch 清理 (远程 + 本地) + 切回 trunk 更新; worktree 模式下按 v1.1.0 集成询问是否清理 worktree。

---

## 4. 输出与记录义务

- **workflow report** 必含: 冲突文件清单 (`backend/config/settings.py`)、判别出的冲突姿势 (rebase/merge)、双侧意图摘要、解决语义 (并集/裁决 + 理由)、重跑的验证及其结果、主干名核实结论 (若消费方 trunk ≠ `main`, 点名)。
- **handoff (Rule #9)**: 若 session 在冲突解决后、门通过前中断, 未交接成果写 `docs/handoff/` (⛔ 不写 `.aria/handoff/`); 机读 frontmatter 5 字段。长会话撞 context 的风险点恰在 gate wait 期 — merge 完成后按 aria-context-monitor 契约 advise `/session-closer`。
- **不可自我裁定的项**: 若冲突裁决涉及破坏性配置语义 (如移除主干侧某配置键), 该判断写进 handoff 请复议, 不现场拍板。

---

## 5. 处置清单 (一屏版)

```
[ ] 0. 核实 trunk 真名 (本仓 master; 消费方项目 ls-remote 精确比对) — 不照抄 "main"
[ ] 1. 只读侦察: status / diff-filter=U / log --merge; 判别 rebase vs merge 姿势
[ ] 2. 语义解决 settings.py: 双侧意图并集; Rule #7 secret 不回显; 导入冒烟
[ ] 3. git add → rebase --continue / merge --continue (Conventional Commits)
[ ] 4. 重跑受影响验证 (B.2 义务重开)
[ ] 5. push (rebase 后 --force-with-lease; ⛔ 裸 force)
[ ] 6. 门序列照常: audit pre_merge (如启用) → C.2.4 CI 门 → C.2.4.5 submodule 门
[ ] 7. merge (子模块: 本地 merge + 双推, 禁服务端 merge) → C.2.5 逐 remote ls-remote 核验
[ ] 8. 分支/worktree 清理 + workflow report + handoff
回退出口 (任一步不可收拾): git rebase --abort / git merge --abort — 无损回到尝试前
```

**红线回顾**: 不裸 force push / 不 `-X ours|theirs` 盲合并 / 不在冲突未解决时创建 PR 或调 merge API / 不以「冲突已拖时间」豁免任何 enabled 门 (Rule #10) / secret value 不进 chat 通道 (Rule #7) / 主干名不照抄字面 (#137)。
