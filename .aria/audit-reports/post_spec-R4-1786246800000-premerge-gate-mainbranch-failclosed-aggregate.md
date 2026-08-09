---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T00:20:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R4 汇总 — premerge-gate-mainbranch-failclosed (max_rounds 耗尽)

## 投票

| 席位 | VOTE | VERDICT | 原始 C+M+m | 重定引入 | 阻塞 Phase B |
|---|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 3+6+4 = 13 | 13/13 | 4 |
| code-reviewer | REVISE | FAIL | 4+6+6 = 16 | 14/16 | 8 |
| qa-engineer | REVISE | FAIL | 4+2+3 = 9 | 6/9 | 4 |
| backend-architect | REVISE | FAIL | 3+1+1 = 5 | 3/5 | 3 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0+4+2 = 6 | 4/6 | 1 |

**5/5 REVISE** · verdict **FAIL** · **`max_rounds=4` 耗尽, `converged: false`** · 零 spawn 失败 ⇒ `incomplete: false`。

## 四轮全景

| 轮 | Critical | Major | Minor | 合计 | 投票 | 本轮 fix 引入 (Major) |
|---|---|---|---|---|---|---|
| R1 | 5 | 10 | 6 | 21 | 5/5 REVISE | — |
| R2 | 3 | 15 | 8 | 26 | 5/5 REVISE | **100%** |
| R3 | 3 | 10 | 9 | 22 | 4 REVISE / 1 PASS | **9/10** |
| R4 | 4 | 14 | 9 | 27 | 5/5 REVISE | **11/14** |

**四轮 20 个 agent-run, 去重 96 条。总量不降, 且每一轮的 Major 有 79-100% 由上一步的 fix 新造。**

⇒ 结论不是「这份 Spec 还差几条」。**审计席位稳定地找到真问题; 编排层 (AI) 在每一轮 fix 里稳定地制造等量新问题。** 瓶颈在 fix 环节, 不在审计环节。

## 诊断已稳定, 处方反复失败

**被独立确认成立的部分** (跨轮跨席):

| 结论 | 确认方式 |
|---|---|
| R3 根因: SKILL.md 散文流程与 helper 是两份实现, AI 走散文那份 | tech-lead R4 独立复核成立 |
| D4: 裸分支名 `ls-remote` 尾段 glob 误判 (`wip/master` → RC=0), 锚定 `refs/heads/<name>` 后 RC=2 | backend-architect R4 受控实验复现 + 编排层 R2 受控仓复现 |
| D8: Rule #6 第二行「照跑 AB」 | SOT `:33` 逐字过度决定; tech-lead / knowledge-manager 分别逐字核过 |

**R4 的 4 条 Critical 无一条挑战 D1-D9 的决策**, 全部挑战「把决策写成可执行契约」时的具体措辞。

## R4 去重结论集

### Critical (4)

| ID | cat | scope | 席 | 重定引入 | 阻塞B | 复现 | summary |
|---|---|---|---|---|---|---|---|
| QC1 | architecture | §1 唯一执行入口的路径解析 | 4 | 是 | **是** | ✅ | `${ARIA_PLUGIN_ROOT}` 全仓从未赋值 (实测唯一 grep 命中是席位报告自己), 恒走相对回落 `aria/`; 实测子模块根 cwd 下 RC=2 —— 而 SKILL.md:242 契约 + CLAUDE.md 硬约束 1 决定 3/4 合并场景 cwd 就是子模块根。且无 helper-not-found 降级契约, 同时抽走了折叠块命令字面量 ⇒ 新的 Rule #8 静默降级向量 |
| QC2 | testing | SC-3 (自称 D1 承重断言) | 4 | 是 | **是** | ✅ | 双重恒红: (a) `-E` 下 `\|` 是字面竖线, 实测 0 (正确 alternation 得 1); (b) 即便修好, Spec 自己的逐字命令是反斜杠续行两行, `python3` 与 `--main-branch` 永不同行 ⇒ **最忠实的实现反而验收失败** |
| QC3 | documentation | D1 覆盖面 — SKILL.md 有两份 C.2.4 散文 | 3 | 是 | **是** | ✅ | 全文 4 行可照抄 `aether ci status`: `:167`/`:168` 属 `### 步骤执行` (小节起 :99), `:243`/`:244` 属 `### C.2.4` (小节起 :218)。**D1 只重整后者**, §Impact 把 :167 当普通字面量、:168 未提 ⇒ 改完 SKILL.md 会同时说「primitive 调用 aether」与「执行方式(唯一) helper」 |
| QC4 | testing | D4 新增 subprocess 的测试隔离 | 2 | 是 | **是** | ✅ | D4 让正常路径每次都调 gate 层 subprocess, 会击穿既有「零真实 git 子进程」基线 (test_sc22 由 PASS 转 AssertionError); 而 Spec 给的处方 (扩大 patch 范围) 经实验证实是 **no-op** —— `import subprocess` 使模块对象全局共享, `patch.object` 本就跨模块生效。**编排层先前的相反陈述已被推翻** |

### Major (14)

| ID | cat | scope | 席 | 重定引入 | 阻塞B | 复现 | summary |
|---|---|---|---|---|---|---|---|
| QM1 | architecture | §6 gate_error 无消费者 | 2 | 否 | 否 | ✅ | SKILL.md:255 逐字规定 fail 的 surface 通道是 `raw_message`; `write_gate_state()` 签名无 gate_error 位置。信息只放 gate_error ⇒ 单测绿、运行时静默丢失 |
| QM2 | implementation | §4 退出码援引越界 | 3 | 是 | **是** | ✅ | 实测 ls-remote 三种真实失败 (remote 名不存在/坏 URL/网络不可达) 均返 **RC=128**, 落在所援引 SKILL.md:260 的 1-126 **之外**; 而 D5 自己写着「不得越界援引」。且 :260 自带 `127→no_ci_fallback` 分支, 照搬即 verdict 变 green |
| QM3 | implementation | §4 核验命令无 -C/repo-root, 依赖 cwd | 1 | 是 | **是** | — | 叠加 QC1 后最自然的绕法是回主仓根执行 ⇒ 合并 aria 子模块却查 Aria 主仓 origin; 两仓都有 master ⇒ RC=0 假通过。**fail-OPEN**, 且「已知残留限制」未声明仓上下文 |
| QM4 | documentation | §6 示例与 SC-2 对撞 | 1 | 是 | **是** | — | §6 的 gate_error 示例逐字含 `"branch": "main"`, 而 SC-2 要求 SKILL.md 内该串计数为 0, §Impact 又要求把该 schema 搬进 SKILL.md:267 ⇒ 两条零裁量条款直接对撞, 照搬必红 |
| QM5 | documentation | §1「沿用 :737 先例」失实 | 2 | 是 | 否 | ✅ | :737 实读是 **advisory** 调用 (:740 逐字「advisory, 不自动中断」), 非强制范式; 且它用 `CLAUDE_PLUGIN_ROOT` 而 §1 写 `ARIA_PLUGIN_ROOT` 却声称「沿用」。该失实先例直接导出 QC1 |
| QM6 | architecture | SKILL.md:252-255 步骤 6 的归属 | 1 | 是 | **是** | — | §C.2.4 实为 6 步; 步骤 6 是**纯 AI 义务** (路由 + v1.65.0/#126 两条强制 surface 警告, helper 只写 JSON 不产文案), 且是 DEC-20260731-001 逐字记载的 owner 交换条件。Spec 无归属声明/Impact/SC, 有被折进「⛔不要手工执行」块而降级的实际概率 |
| QM7 | documentation | 折叠块未补 §5 新增步骤 | 1 | 是 | 否 | — | §5 新增存在性核验步, 但 §1/§Impact 只说「步骤 1-5 移入折叠块」, 无一句要求折叠块补该步 ⇒ 折叠块自称描述 helper 内部算法却漏掉本 change 唯一会 BLOCK 合并的那一步 (Rule #3 自造失同步) |
| QM8 | testing | 三处「由 X 保证/机械钉住」去 X 实测不成立 | 1 | 是 | 否 | — | SC-10 只钉 `enabled=false` (no-backend 与 stub-NIE 零覆盖); `_OLD_KEYS` 是 assertIn 超集容忍且不覆盖被点名的两条早退; 「沿用 :737 先例」在承重的 env var 那一位没沿用。**同一 class 三例** |
| QM9 | testing | SC-10 负控无失败注入 | 1 | 是 | 否 | — | 若 fixture 让核验成功, 前置核验的错误实现同样返 green+六键 ⇒ SC-10 在健康与不健康实现下都绿, 零信息量, 守不住 D7。缺「assert ls-remote 未被调用」这条因果断言 |
| QM10 | documentation | §版本 悬置的选项集错 | 2 | 是 | 否 | — | 悬置本身正当 (Rule #10), 但 CLAUDE.md 逐字「Skill 架构重构 = MINOR+」**直接管辖 D1** (自称「结构重整」), PATCH 分支应先排除; version-management §2.1 的 MAJOR 触发全是方法论结构级, 不含 CLI 参数必填。应由 Spec 定到地板 MINOR, 只把 MINOR vs MAJOR 交 owner |
| QM11 | documentation | Spec Level 2 未在范围重定后重新核验 | 1 | 否 | **是** | — | D1「结构重整」对照 OpenSpec Level 3 的「Architecture changes」判据, 且**改动面更小的姊妹 Spec 已升 Level 3**; 本 Spec 范围重定后未重核 Level |
| QM12 | documentation | §Impact 无 CLAUDE.md 行 | 2 | 否 | 否 | — | 本 Spec 给 Rule #8 **新增第三条阻断腿**并改写其指名的 SOT 段, 但 §Impact 无 CLAUDE.md 行; v1.31.0 CI backend 抽象化曾在同一提交同步 Rule #8 (commit 7661e96), 构成直接先例。另 §风险 grep 口径实测搜不到 CLAUDE.md (它写「pre-merge gate」不写 `gate_check`) —— 口径维度对不上错误维度 |
| QM13 | testing | SC-7/SC-8 的 (mock) 括注与打桩禁令矛盾 | 2 | 是 | 否 | — | :186 说 SC-6/7/8 三条都不得打桩要验真实 ls-remote, 但 SC-7 括注「(mock)」、SC-8 括注「(mock; 须 mock time.sleep)」。真实 ls-remote 无法产出非0非2 或确定性 timeout |
| QM14 | documentation | #137 新 comment 未声明 supersede | 1 | 是 | 否 | — | #137 已有 comment 描述被本版放弃的方案 (symbolic-ref 自动解析 + main_branch_resolved + 7 SC); 新 comment 若不提 supersede 会与旧评论并存造成矛盾描述 |

### Minor (9)

| ID | cat | scope | 席 | 重定引入 | 阻塞B | 复现 | summary |
|---|---|---|---|---|---|---|---|
| Qm1 | documentation | §5 插入点两处行号漂移 | 1 | 是 | 否 | — | :356 实为 pc=None (调用在 :358); :344 实为 precheck 调用 (早退在 :345-352) |
| Qm2 | documentation | §6 在场范围写「三个早退」 | 1 | 是 | 否 | — | SKILL.md:279 逐字是四类 (含 backend query 失败); 按三类改写会把该契约掉出去, 而 test_sc15 正在守它 |
| Qm3 | documentation | §待R4重点审 item 3 与 SC-3 正文互斥 | 2 | 是 | 否 | — | 前者描述含「grep -c 'pre_merge_gate.py' ≥2」从句, 后者逐字明令不得附加。同一交付面两处对同一断言互斥描述 (上一版残留) |
| Qm4 | documentation | §Rule #6 对 SOT §3 的转述更紧 | 2 | 是 | 否 | — | Spec 写「专指 authoring」, 原文 :30 是「典型: authoring 向导」—— authoring 是例不是定义, 会被后来者当规则复用。**定档结论 D8 本身正确** |
| Qm5 | documentation | SC-2 归零 :270 对 fail-close 零贡献 | 1 | 是 | 否 | — | :270 是 in_flight_runs **输出示例** (取自 SilkNode PR-321 真实事故 run 3161), 与输入占位符不同层; 归零只损示例真实性 |
| Qm6 | implementation | §6 gate_error 在场范围欠定 | 1 | 是 | 否 | — | 「核验失败路径与最终 verdict 路径可能在场」—— 按 §4/§5 核验失败即 return, 走不到 compute_verdict。笔误还是要求 plumb 进 _build_output 签名, 两实施者会给不同 schema |
| Qm7 | documentation | audit-trail 切分缺对称声明 | 1 | 是 | 否 | — | 切分实质合规, 但「不一致时以谁为准」只写在 audit-trail.md, 未如先例对称写回 proposal.md 头部 |
| Qm8 | implementation | 修实例不修类枚举不全 | 1 | 否 | 否 | — | 漏 `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"` —— 与 pre_merge_gate.py:300 完全同形; `multi_remote.py:800` 的 None 短路可作参照实现 |
| Qm9 | implementation | gate_error.message 示例语种 | 1 | 是 | 否 | — | 示例为中文, 而 pre_merge_gate.py 既有全部 raw_message 均为英文; Spec 未说明实现是否要产中文 |

## 阻塞 Phase B 的 9 条及其性质

| ID | 性质 | 会不会在 Phase B 首次实施时自动暴露 |
|---|---|---|
| QC1 路径解析 | 机械 | ✅ 首次运行即 RC=2 |
| QC2 SC-3 恒红 | 机械 | ✅ 该测试永远不绿 |
| QC3 D1 覆盖不全 | 机械 | ✅ grep 即见残留 2 行 |
| QC4 测试隔离 | 机械 | ✅ 首次跑测试即 test_sc22 转红 |
| QM2 退出码越界 | 机械 | ✅ 首个错误分支即命中 |
| QM3 cwd 依赖 (fail-OPEN) | 机械 | ⚠️ 仅在子模块上下文测试时暴露 |
| QM4 §6 示例与 SC-2 对撞 | 机械 | ✅ SC-2 转红 |
| QM6 步骤 6 归属 | **文档决策** | ❌ 不会自动暴露 (涉 DEC-20260731-001 owner 交换条件) |
| QM11 Level 2 vs Level 3 | **治理决策** | ❌ 不会自动暴露, 须 owner 裁 |

⇒ 9 条里 **7 条是 TDD 分钟级自曝**的机械项, 2 条是需要人裁的决策项。

## 编排层四轮累计错误 (增补 R4)

承 R3 汇总的 1-7 条, R4 新增:

| # | 错误 | 性质 |
|---|---|---|
| 8 | 引 `:737` 作强制 helper 调用先例, **抄了形状没抄环境变量名**, 且 `:737` 实为 advisory 调用 | 引先例不核承重位 (同 memory `delegate-verify`) |
| 9 | SC-3 新写的「零裁量 grep」是**恒红** (转义 + 自己的命令跨两行) | 在修该缺陷的编辑里造出反向缺陷 (第 5 次) |
| 10 | §Why 论证「换字面量不够」, §Impact 却按字面量处置 `:167`; 且从未数过 SKILL.md 里有几份散文 (实为 2 份 4 行, D1 覆盖 2 行) | 同一文件内既立判据又违反它 |
| 11 | D5 写「不得越界援引」, 而 §4 自己援引 `:260` 的 1-126 覆盖 RC=128 | 同上, 第 2 次 |
| 12 | 断言 `test_sc22` patch 只对 path_coverage 生效 —— **受控实验推翻** (`import subprocess` 使模块对象全局共享), 且曾向 owner 陈述过 | 对 Python 语义的错误断言 + 已外传 |

## 处置

`max_rounds=4` 耗尽且未收敛 ⇒ 进入 SKILL 定义的**降级策略**, 三路径须由 owner 选择 (AI 不得自行选定)。
