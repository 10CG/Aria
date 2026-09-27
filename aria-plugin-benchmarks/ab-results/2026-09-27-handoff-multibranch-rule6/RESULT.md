# RESULT — Rule #6 AB `state-scanner` · `10CG/Aria#195` handoff-multibranch-subdir-path-fidelity (TASK-026)

> 跑前预测: 同目录 `PREDICTION.md` (写于 2026-09-27T16:56:51Z, 先于任何臂派出, 全程未改; sha256 `3aab0a78…c765d` 记在本轨台账)。
> 逐 eval 分数: `SCORES.md` (由 `tools/score.py` 从两臂 `grading.json` 直接汇总)。
> 逐 eval 的评分批判: 各 `state-scanner/runs/eval-*/GRADER_CRITIQUE.md`。
> 派臂与评分的原始说明、盲标映射、transcript 审计: `dispatch/`。

## 1. 结论

### 1.1 数字

| 项 | 值 |
|---|---|
| 主样本 | 13 eval / 78 条断言 |
| with 臂 | 50/78 · mean(pass_rate) = 0.7141 |
| old 臂 | 50/78 · mean(pass_rate) = 0.7141 |
| **delta.pass_rate** | **+0.0000** (= mean(with) − mean(old), 脚本直算) |
| 预测 (PREDICTION.md) | delta ≈ 0, 两臂逐 eval 相等 |

对账: 13 条里 11 条两臂逐条同分, 与预测一致。偏离预测的两条互相抵消:

- eval 5: with 3/6 < old 4/6 —— 按判据复跑两次 (rep2 3/6 = 3/6, rep3 3/6 = 3/6), 三个样本里 with < old 只有 1 个 ⇒ **不判回归**。评分员查明差距来自 old 臂那次恰好碰上 origin fetch 失败, 断言 6 (「git 出错不阻断扫描」) 才有了证据; 复跑中网络正常, 差距消失。
- eval 6: with 2/6 > old 1/6 —— 差在断言 4 (detached HEAD): with 臂多写了一段情形说明。评分员核对两臂 `collectors/sync.py` / `collectors/git.py` 逐字相同, 判为回答详略差异, 非版本差异。

绝对分与预测点估计 (取自 09-05 先例) 有漂移 (预测 56/78, 实得 50/78), 两臂同向, 在预测时已说明「仓库状态已变, 绝对分可能漂移, 但两臂同向漂移」。

### 1.2 「无回归」判据 (本次运行内逐 eval, 同一评分员)

- 每个 eval 由**同一个**评分员一次评两臂, 两臂匿名为 X / Y (随机分配, 映射见 `dispatch/arm_map.json`), 评分员不知道哪个是新版。
- 主样本 with < old 的 eval: 仅 eval 5 ⇒ 复跑两次 ⇒ 1/3 ⇒ **不判回归**。
- ⇒ **未触发止损**, TASK-027 / TASK-029 不因回归阻断。
- 需复跑的 eval 只有 1 条 (< 3) ⇒ 不触发「扩面即拆任务」。

### 1.3 回归面: **未被有效测试**, 不是「已验证无回归」

与先例 `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/RESULT.md` §1.2 同一判断, 且本次更彻底:

1. **两臂的 AI 可见输入几乎相同。** `SKILL.md` 两臂逐字节相同; 在本仓跑两臂 `scan.py`, snapshot 的唯一结构差异是 with 臂多了 `tracks_multibranch.unreadable_count` 与每条 track 的 `rel_path` 键, 其余 2040 条 track 完全相同。本 spec 修的是 handoff 放在子目录时的路径, 而本仓与全部 origin 分支的 `docs/handoff/` 都是平铺 —— 被修的代码路径在真仓里**没有输入**。
2. **套件结构上测不到本次改动。** `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `legacy` / `basename` 零命中; `tracks_multibranch` 只在 eval 13 题面出现一次, 且把 `collision.kind` 的取值写死在题里 (见 §5 套件缺口)。
3. **既有断言大面积恒真 / 恒假。** 13 份评分批判逐条点名: eval 5 断言 4 (新旧两版 scan.py 都自动 fetch, 恒假) / eval 6 断言 1、5 (要求回答写出实现细节, 恒假) / eval 8 断言 5、7、8、eval 9 断言 3、7、eval 10 的 5 条、eval 11 的 5 条 (前提场景在真仓里不存在, 恒假或空真) / eval 1、2、4、12、13 (复述题面或模板即可通过, 恒真)。

⇒ 50/78 对 50/78 这组数字**只能**读作「在这个套件能看到的面上, 两臂没有可测差别」, **不能**读作「已验证本 cycle 改动无回归」, 更不能读作「本 cycle 改动有增益」。

### 1.4 区分力分写 (落地前已证 / ship 态边际)

- **落地前已证** (substitute 证据, 本 AB 不削减): TASK-007 RED 记录 / TASK-015~018 与 TASK-035 三步法反事实 / TASK-021 全量回归全绿 (`Ran 1627 OK`) / TASK-022 活体 dogfood (SC-12a / SC-12b)。本 spec 的鉴别力全部来自这些。
- **ship 态边际**: 本 AB 测得 0。原因如 §1.3 第 1、2 条 —— 不是改动无效, 是这个套件和这份仓库语料都够不到改动面。
- 另注: 基线臂与 with 臂都能读到仓内本 change 目录、台账与 handoff (多个臂在回答里引用了 09-27 handoff 与 AB 结果目录的存在), 两臂同等暴露, 不构成单侧污染。

## 2. 与 SOT 验收判据的关系 (如实登记)

- `AB_TEST_OPERATIONS.md` 场景 1 的验收是 **`delta.pass_rate > 0`**。本次 delta = **+0.0000** ⇒ **未达成**。
- 回归面按 §1.3 判为**无效度**。
- ⇒ 按 TASK-026 verification, 结论写「**未被有效测试**」, **不单独构成通过**。
- ⇒ 触发 TASK-026 的 owner 裁决点 (PREDICTION 已预期会触发), 经 AskUserQuestion 呈 owner (附 PREDICTION 对照与套件缺口单)。
- **owner 裁定 (2026-09-27)**: 「放行进 TASK-027」—— 认定 Rule #6 义务已照跑履行, 本 cycle 改动的鉴别力由 §1.4 所列 substitute 证据承担, 套件测不到的面由 `10CG/aria-plugin#205` 跟踪。裁定原文记本轨台账。

## 3. 两臂口径与执行路径核验

- 口径写死为「**代码 + 文档整体**」, 区分力不归因到文档。
- with 臂: aria `b181678619023910bb4eed7266afc765ce937322` (= TASK-021 回归前 HEAD), 开跑前断言 `git -C aria rev-parse HEAD` 等于该 SHA 且 `status --porcelain` 为空 (0 行), 直接用 `/home/dev/Aria/aria/skills/state-scanner`。
- old 臂: B.1 基线 `1cb387218935433312fde4067c276754b77686a8` 的一次性 worktree, 建在会话 scratchpad (16:54:09Z 建, 17:32:57Z `worktree remove`)。
- 本环境 `CLAUDE_PLUGIN_ROOT` 未设 ⇒ 两臂提示都写明各自 `SKILL.md` 与 `scan.py` 的绝对路径。
- transcript 审计 (`dispatch/transcript_audit.txt`, 30 个 run): 26 个 run 跑了 scan.py, **全部**跑的是本臂的那一份 (r03y 的命令写成 `$S/scripts/scan.py`, 其 `S=` 设为 old 臂 skill 目录, 展开后即 old 臂路径); eval 12、13 的 4 个 run 按题面「只回答不跑命令」未跑 scan.py (r13x 的 scan.py 命中是写进 answer.md 的命令文本)。**没有一个 run 两臂跑到同一份代码** ⇒ 零作废。
- 为减少臂读到评测材料的机会, 臂的产出先写 scratchpad 的中性目录 (`runs/rNNx|y`), 全部评完后再按映射复制进本目录; 臂与评分员都只看到 X / Y。

## 4. 隔离验收 (AB_TEST_OPERATIONS.md 场景 1 三步)

| 步 | 结果 |
|---|---|
| 第 1 步 · 会话带 `ARIA_COORDINATION_NO_PUSH=1` 启动 | ✅ 环境变量 = `1`; 子进程 `no_push_requested_by_env()` → `True`。开跑前协调 ref: 本地 = origin = `e91113242a3d087b718ab08608f55a92041c2658` |
| 第 2 步 · transcript 中 phase1_gate / release_gate 输出含 `push_skipped: true` | **未触达** —— 30 个 run **零执行** phase1_gate / release_gate (regex 命中的 12 处全部是写进 answer.md 的 heredoc 命令文本, 逐条核过), 也无任何 `push_skipped` 输出。该步空真, **不算核验通过**, 由第 1 / 第 3 步的前后比对兜底 |
| 第 3 步 · `git fetch origin +refs/aria/coordination:refs/aria/coordination` | ✅ 17:32:24Z 执行。执行前 本地 = origin = `e911132…`; 执行后 本地 = origin = `e911132…`。AB 期间远端 ref **未变化** (运行中另抽查两次, 本地与 origin 均为 `e911132`), 无需逐 commit 核作者 |

仓库收尾: 主仓只有两个有意 dirty 的子模块指针 (`M aria` / `M standards`, 归 TASK-030 / 031) + 本结果目录; aria 工作树干净, HEAD 仍为 `b181678`。scan.py 自带的 fetch 刷新了远程跟踪 ref 与 gitignore 下的 `.aria/cache/`, 属 skill 固有行为, 两臂相同。

## 5. 套件缺口 → `10CG/aria-plugin#205` (owner 2026-09-27 授权后开出, GET 核验 open 且标题正文逐字一致)

- `ab-suite/state-scanner.json` (version 1.7.0, 13 eval) 对 `handoff_multibranch` / `legacy` / `basename` **零命中**; `tracks_multibranch` **仅 :214 一处** (eval 13 题面), 且题面把 `collision.kind` 的值写死为「空」—— 答题不依赖 collector 实际产出。
- ⇒ 该套件**结构上测不到** collector 输出的变化; 本 spec (以及今后任何只动 `handoff_multibranch.py` / `latest_md_writer.py` 的改动) 的 Rule #6 AB 都会得到 delta ≈ 0 的无效度结果。
- 查重 (Forgejo `10CG/aria-plugin`, `state=all`, 标识符类检索词 `handoff_multibranch` / `tracks_multibranch` / `ab-suite` / `state-scanner.json` / `basename` / `legacy`): 相关的 `10CG/aria-plugin#157` (Layer L / `--linked-issue` 零覆盖) 与 `10CG/aria-plugin#177` (eval 1/3/5/7 断言不可区分) 都不涉及 collector 输出或子目录路径; `10CG/aria-plugin#204` 是本 spec 的读侧遗留缺口, 不是套件缺口。⇒ 无重复。
- 各 eval 评分员另列的断言缺陷 (eval 11 断言 2 要求 `behind` 与断言 4 自相矛盾 / eval 5 断言 5 写四级回落而代码是三级 / eval 6 断言 5 的 `.git/shallow` 回落在现行代码里找不到 等) 记在各 `GRADER_CRITIQUE.md`, 不并入本 issue (与 `10CG/aria-plugin#177` 同族, 由其承接或另议)。

## 6. 附带发现 (仓库真实问题, 与本次 AB 判定无关; 未开单)

1. 主仓 `VERSION` 「子模块版本」表 aria 行仍写 `v1.73.0`, 实际 1.73.3; 该行最后改动于 `6a7ab16` (v1.73.0 发版), v1.73.1 ~ v1.73.3 三次发版都没同步, 现有 16 条 custom check 无一覆盖该表 (两个臂独立发现, 主控 `sed -n 24p VERSION` 复核属实)。
2. `aria/README.md` 与 `aria/README.zh.md` 的 Skill 列表漏 `issue-triage` 与 `session-closer`, `aria/README.zh.md` 计数写 41 (实际 42); 现有检查只核版本号不核列表 (eval 8 两臂各发现一部分, 评分员复核)。
3. 在 feature 分支工作树上, `docs/handoff/latest.md` 仍指 09-24 那份 (master 上已指 09-27) —— 这是本轨 feature 分支落后 master 12 个提交的自然结果, 不是 collector 缺陷; 多个臂自行去 `origin/master` 读了最新 handoff。

## 7. 下一步

1. ~~owner 裁定 (§2 触发)~~ → 已裁「放行进 TASK-027」(见 §2)。
2. ~~开 §5 的套件缺口 issue~~ → 已开 `10CG/aria-plugin#205`。
3. 本会话 (`ARIA_COORDINATION_NO_PUSH=1`) 到此退出; TASK-027 起在不带该变量的新会话执行, 且新会话须先在 2026-09-28T12:35Z 之前刷两条 claim 心跳。
