# Phase C C.2 merge 冲突处置 — `feature/oauth2-social-login` → `main`, 冲突文件 `backend/config/settings.py`

> 产出形态: 描述性推演。以下全部命令为推演示例, 本次未实际执行任何 git / forgejo 操作。

## 1. 定性: 这是什么性质的失败

- **流程位置**: Phase C / C.2 (orchestrator tier) 的 merge action。按 SKILL.md 的 skill 边界表, 走到 merge 说明已依次经过 branch-manager C.2.1-C.2.3 (sync rebase + push branch + create PR)、phase-c-integrator §C.2.4 pre-merge precondition gate、(如适用) §C.2.4.5 submodule gate, 现在卡在 branch-manager 侧的 merge 执行面。
- **命名消歧**: "C.2.4" 有两个独立 namespace — 本 skill 的 C.2.4 = pre-merge precondition gate (orchestrator tier); branch-manager 内部 C.2.4 = wait-approval (implementation tier)。同名不同 tier, 语义独立。本次冲突与这两个 C.2.4 都不是一回事: 它是**文本级 merge 冲突**, gate 查的是 CI 状态, 不担保文本可合性。
- **根因类别**: 确定性、可恢复的集成失败。典型成因: PR 创建 / branch-manager C.2.1 sync 之后 `main` 又前进了, 且这次前进没在 gate 窗口内被 (b) 轴 (main in-flight) 拦住 — §C.2.4 明言 gate 检查与 merge call 之间的 race「窗口最小化, 不消除」。这不是 gate 失败, 更不是需要降级或绕闸的异常。
- **"gracefully" 的操作定义** (按本 skill 错误处理章的 stop → report → 修复 → 重试 风格): 停止 merge → 报告冲突事实 → **回到 feature 分支**收敛冲突 → 重新全链过闸 → 重试 merge。不静默降级、不绕闸、不在主干上就地撮合。

## 2. 处置流程 (step-by-step)

### Step 0 — 冻结与诊断, 先报告再动手

本地 merge 停在 CONFLICT 态时, 先诊断, 不急着 `--abort` 也不急着改文件:

```bash
git status --porcelain                       # 确认 both-modified 只有 backend/config/settings.py
git log --merge --oneline -- backend/config/settings.py   # 两侧各自的提交意图
```

读 conflict hunk, 区分两类:
- **相邻行碰撞** (两侧改了同文件不同区域, git 上下文重叠) → 机械可合;
- **同一配置项两侧都改** (同一 key 不同值/不同结构) → 语义取舍, 见 §3 升级条件。

若是 Forgejo PR 侧 merge 被拒 (PR 页标记 conflict): 服务端本来就不会合出坏结果, 直接进 Step 1。

⚠️ **secret 卫生 (Rule #7)**: oauth2 配置常含 client secret / 凭据类条目。冲突诊断与后续报告只引用 key 名、结构、status code 等 metadata, 不把 value 字面打进 chat 或报告。

向用户/上层的冲突时刻报告 (graceful 的沟通面) 应包含: 冲突文件与 hunk 数、两侧意图各是什么 (来自 `git log --merge`)、判定为机械合并还是语义取舍、处置计划 (回分支 → 解冲突 → 重过闸 → 重 merge)、预计影响 (PR 新增 commit + CI 重跑)。

### Step 1 — 不在 main 上解决冲突

**禁止**把 conflict resolution commit 直接落在 `main`: 那会绕过 PR + CI + §C.2.4 gate 整条链 (违背 Rule #8), 且评审者看不到解冲突的推理过程。本地处于 CONFLICT 态时先恢复干净:

```bash
git merge --abort    # main 回到 merge 前状态, 不留半成品
```

### Step 2 — 回 feature 分支 sync main (重入 branch-manager C.2.1)

```bash
git checkout feature/oauth2-social-login
git fetch origin          # 先取最新 base
git merge origin/main     # 或按 branch-manager C.2.1 的 sync rebase 纪律执行
```

- 分支已推远端且已开 PR: 默认 **merge main into feature** (保留评审历史与 PR 连续性); rebase 会重写已推历史, 仅在分支无人引用且流程允许时考虑。
- 冲突在此重现, **在 feature 分支上解决** — 这是解冲突的唯一正确落点。

### Step 3 — 语义解冲突 (settings.py 专项)

- 目标态 = **两侧意图的并集**: oauth2 social login 新增的 provider 配置与 `main` 侧新增/调整的配置同时在场。
- **禁止** `git merge -X ours` / `-X theirs` 一把梭: 对配置文件这是静默丢语义的典型来源 — 一侧的配置项整段消失, 编译照过、测试都可能不红。
- 逐 hunk 处理, 保持文件既有的分组与排序约定; 两侧对**同一 key** 给出不兼容值时 → 不是机械合并, 转 §3。
- **Rule #3 (文档与代码同步)**: 若解冲突后 settings 的有效配置面变化 (新 provider 开关、默认值变动) 且存在对应文档/schema 说明, 同步更新。

### Step 4 — 在 feature 分支上验证合并结果

跑 Phase B 同一验证面: 单测 + 集成测试, 至少覆盖 settings 加载与 oauth2 相关用例; 有 config schema 校验的一并跑。验证对象是**合并结果**而非仅 feature 侧 — 对齐 branch-finisher 的 validation_report 纪律 (passed 才进入集成)。

### Step 5 — Conventional Commits 提交 (Rule #4)

```text
chore(integration): resolve settings.py conflict merging main into feature/oauth2-social-login

- union of oauth2 social provider config (feature side) and main-side settings additions
- Conflict-File: backend/config/settings.py
```

(具体格式按 `standards/conventions/git-commit.md`; 提交不加 AI 署名 trailer, 按 owner 2026-09-27 裁定。)

### Step 6 — push feature 分支 (仅 origin)

按 branch-manager C.2.2 纪律, feature 分支只推 origin。多 remote 的 trunk 推送是 §C.2.5 (merge 之后) 的事, 不在 feature 分支上提前做。正常情况无需 force; 若此前确有 rebase 重写历史需 force, 用 `--force-with-lease` 且先完成前置核验 (双远程半推=镜像分叉的教训)。

### Step 7 — 全链重过闸 (Rule #8 + Rule #10, 零裁量)

feature 分支上的 resolution commit 推上去后, PR head 变了 ⇒ **此前的 §C.2.4 green 作废**, 从头重跑:

1. `pre_merge_gate.py --pr-branch feature/oauth2-social-login --main-branch <真实主干名>`。
   ⚠️ **主干名取该项目主干的真实名字**: 判据 = 解析出的 ref 名列表做精确字符串比对, 不看退出码 (零命中也返 rc=0)、不用 glob (`mast*` 会假命中) — references/pre-merge-gate-empirical-traps.md §一/§五 (#137: 本 workspace 的 Aria 主仓主干是 `master`; 场景字面写的 `main` 要先核实再填)。
2. verdict 三态路由: `green` → 继续; `wait` → workflow-runner wait+retry (intervals `[30,60,120,300,300]`, timeout 1800s; `gate_error.kind=no-run-for-branch` 时必须 surface message 原文, 不写「CI pending 等待中」); `fail` → BLOCK, 回查 PR CI / backend。
3. path coverage 随 gate 自动重评 (settings.py 属代码路径, 预期 `covered`, 不影响流程)。
4. §C.2.4.5 submodule pointer gate (如仓内有 submodule; 默认 mode=block) 照跑。

**Rule #10**: 不得以「只是解个冲突 / 变更小 / 就是同一个功能」为由跳过、降级或改序任何 enabled 闸门 — 豁免白名单 (config 显式 off / adaptive_rules / 成文 lane 降级 / 结构性前提不成立) 四类封闭, 「存在但简单」不算。AI 若认为某闸不适用, 写进报告请 owner 复议, 不自行豁免。

### Step 8 — merge 与后续链

- gate green + 审批 (branch-manager C.2.4 wait-approval) → 执行 merge, 此刻应无冲突。
- merge 成功 (trunk 已 fast-forward) → **§C.2.5 multi-remote push enforcement**: 快照 `expected_sha = git rev-parse HEAD` → 子模块逐 remote 推送 → 主仓推送 → 对每个 remote 独立 `git ls-remote` 比对 SHA (不信 push 回执, 全部一致才算成功)。
- §C.2.6 UPM milestone append 仅在 `upm.milestone_driven=true` 且 C.2.5 完成后触发。
- 之后才进 Phase D。

### Step 9 — 记录与收尾

- 冲突事实、两侧意图、解法、重过闸结果写进本 cycle 报告; session 收尾按 Rule #9 写 `docs/handoff/` (禁 `.aria/handoff/`)。
- 会话已长时, merge 等待期用 aria-context-monitor 判断「本 cycle 收尾后是否暂停换会话」(#104, advisory)。

## 3. 升级条件: 什么时候这不再是机械合并

- 两侧对**同一配置 key** 给出不兼容值, 或解法需要产品级取舍 (如 auth 流程行为变化): 这是**需求层决策**, 不是 AI 单方面拍的机械合并 — 停下, 向 owner 呈报两侧意图与各自代价, 由 owner 裁定。
- 若裁定结果改变既有行为 → 走 OpenSpec (Rule #1: 需求变更须 Level 2/3; Level 取不到按上界跑)。
- 转述待裁项时: 原文没有推荐默认的不得自标默认, 推荐项必须带代价。

## 4. 禁止事项 (anti-pattern 清单)

1. ❌ 在 `main` 上就地解冲突并提交 — 绕过 PR + CI + §C.2.4 gate 整条链 (Rule #8)。
2. ❌ `git merge -X ours` / `-X theirs` 盲合 `settings.py` — 静默丢一侧语义。
3. ❌ 以「变更小」为由跳过解冲突后的重过闸 (Rule #10)。
4. ❌ force-push `main`; 对 feature 分支的无核验 force push。
5. ❌ 把冲突态跨 session 晾着不留 handoff (Rule #9)。
6. ❌ 把 oauth2 凭据 value 字面打进 chat / 报告 (Rule #7)。
7. ❌ 若 `backend/config/settings.py` 属某子模块内文件: 该子模块的合并必须本地 `git merge` + 双推, 禁用 Forgejo 服务端 merge (CLAUDE.md 多远程硬约束 1)。

## 5. 对执行状态与输出面的影响

- 本 cycle 的 `success` 维持 false, `steps_executed` 中 C.2 未完成; §C.2.5 / §C.2.6 的触发条件 ("Phase C.2 合并成功 (master 已 fast-forward)") 不满足 ⇒ **整条下游暂停, 不部分执行**。
- skill 错误处理表中最接近的行是「推送失败 | 远程冲突 | 提示拉取最新代码」— 同一精神在本场景的 gate 版表述: 冲突 = 回分支拉最新收敛后重试, 而非绕过或强推。

## 6. 依据索引 (grounding)

- `SKILL.md`: C.2 步骤表与 branch-manager 边界表; §C.2.4 三态 verdict / race condition 注记 (窗口最小化不消除); §C.2.4.5 submodule gate; §C.2.5 multi-remote push; §C.2.6; 命名 namespace 澄清段; 错误处理表; Context 占用感知 (#104)。
- `references/pre-merge-gate-empirical-traps.md`: §一 (ls-remote 零命中返 rc=0 / 参数被当 glob ⇒ ref 名列表精确比对); §五 (主干名 #137, 本项目主干是 `master`)。
- `scripts/pre_merge_gate.py` (只读): `gate_check()` 为 merge 前置的 CI 状态判定, 不含也不应含文本 mergeability 检查 — 印证冲突属 merge 执行面。
- 项目规则 (CLAUDE.md): Rule #1 / #3 / #4 / #7 / #8 / #9 / #10; 多远程推送两条硬约束; 提交不加 AI 署名 (owner 2026-09-27 裁定)。
