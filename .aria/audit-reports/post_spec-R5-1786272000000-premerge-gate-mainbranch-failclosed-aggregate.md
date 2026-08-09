---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T08:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R5 汇总 — premerge-gate-mainbranch-failclosed

## 投票

| 席位 | VOTE | VERDICT | 原始 C+M+m | 本版引入 | 阻塞 B |
|---|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 2+6+5 = 13 | 11/13 | 2 |
| code-reviewer | REVISE | FAIL | 1+7+6 = 14 | 12/14 | 5 |
| qa-engineer | REVISE | FAIL | 1+3+2 = 6 | 3/6 | 2 |
| backend-architect | REVISE | FAIL | 1+3+0 = 4 | 0/4 | 1 |
| knowledge-manager | REVISE | FAIL | 1+3+0 = 4 | 3/4 | 0 |

**5/5 REVISE** · verdict **FAIL** · `converged: false` · 零 spawn 失败。原始 41 条 → 去重 **3C + 11M + 7m = 21**。

## 五轮全景

| 轮 | C | M | m | 合计 | 投票 | 本轮 fix 引入 (Major) |
|---|---|---|---|---|---|---|
| R1 | 5 | 10 | 6 | 21 | 5/5 REVISE | — |
| R2 | 3 | 15 | 8 | 26 | 5/5 REVISE | **100%** |
| R3 | 3 | 10 | 9 | 22 | 4 REVISE / 1 PASS | **9/10** |
| R4 | 4 | 14 | 9 | 27 | 5/5 REVISE | **11/14** |
| R5 | 3 | 11 | 7 | 21 | 5/5 REVISE | **~8/11** |

**五轮 25 个 agent-run, 去重约 117 条。总量五轮持平 (21→26→22→27→21), 每轮 Major 有 73-100% 由上一步 fix 新造。**

## 三条 Critical (去重)

| ID | 席位 | 内容 | 阻塞 B |
|---|---|---|---|
| **TC-A** | **4 席独立收敛** | §1 两分支路径解析对 `standards` / `aria-orchestrator` 子模块根与 **plugin 市场安装态**结构性不可达 ⇒ `exit 2` 恒 abort ⇒ **Rule #8 由恒绿变恒红**。编排层复核: 第三副本确实存在于 `~/.claude/plugins/marketplaces/.../pre_merge_gate.py` 且与仓内 **identical**; 且 D2 排除 env var 的依据是**单次运行时量测**, 而 `CLAUDE_PLUGIN_ROOT` 仓内 **66 处**在用 (`ARIA_PLUGIN_ROOT` 仅 5 处) —— **测错总体** | **是** |
| **TC-B** | 2 席独立 Forgejo 实读 | §Why 断言「#137 正文关于 (a) 腿的陈述成立」并据此不打删除线 + 发 supersede 评论; 而该 issue 唯一评论 (id 18015, 编排层前一 session 所写) 逐字是「**我在正文里对 (a) 那条腿的判断是错的**」。且 (a)/(b) 标签与 `CLAUDE.md:113` canonical 编号相反。⇒ 落地会在公开 issue 发一条推翻作者本人自撤回的评论 | 否 (但阻塞外向动作) |
| **TC-C** | 2 席 | **SC-3 与 D1 直接矛盾**: D1 逐字要求「两处散文都收敛为强制 helper 调用」, SC-3 期望该块计数 **== 1**。两处都放 ⇒ 恒红; 只放一处 ⇒ D1 未落地。两个实现者得相反结果且都能自称合规 | **是** |

## 主要 Major (去重后 11 条, 摘 5)

- **锚定只关掉一半** — `refs/heads/<name>` 未关闭 name 内含 glob 元字符时的误匹配。编排层受控实验: 远端只有 `refs/heads/master` 时, `refs/heads/mast*` / `m[a]ster` / `maste?` / `*` **全返 RC=0**。⇒ **R2 那条承重 Critical 改了三个版本仍未真正关闭**; 正确修法是对返回 ref 名精确比对, 不依赖 pattern 匹配 (2 席 + 编排层复现);
- **退出码表自称「完整分区」却无 catch-all** — 漏 `FileNotFoundError` (git 二进制缺失, 抛异常无退出码) / `OSError` / 129; 同包 `path_coverage.py:93` 已有三合一先例未复用 (3 席);
- **§非目标「由 SC-10 机械钉住」不成立** — SC-10 只走 `enabled=false` 早退, no-backend / precheck 失败 / stub NIE 三条零覆盖 (3 席, `delegate-verify` 形状);
- **在治「两份实现」的 Spec 里造第二份同算法实现** — `aether.py:38` 已有 `RETRY_BACKOFF=(5,15,45)` / `_run_with_retry`, Spec 要求 gate 层重新实现同样的 3 attempts (2 席);
- **§版本「两条条款指向不同」是逻辑错误** — `MINOR+` 是**下界非枚举**, MAJOR 满足它; 与 Spec 自认 D5 为破坏性变更组合后交集唯一为 MAJOR。「地板 = MINOR」给下游留了看似合规的违规口 (2 席 + 归档先例佐证)。

## 本轮最有信息量的一条元观察 (knowledge-manager)

该席位确认自己 R4 的 4 条 Major 有 **3 条被正确采纳** (版本 PATCH 排除框架 / Level 3 升级 / CLAUDE.md 行补入 / Rule #6 措辞更正), **而吸收这些修法的同一批新写文字里又新造出 2 个更细粒度的问题** —— 与 `feedback_fix_recurs_in_its_own_fallback_path` 同形, 但发生在**元层面**: 不是某条修法复发, 是「修法这个动作」本身稳定产出新缺陷。

另: 该席位指出本 Spec 是姊妹 Spec 同日开出的 **Aria #177**「下次会原样重犯」预言的**即时复现样本** (§Impact 缺发版同步面整行)。

## 编排层本轮新增错误 (承前 12 条)

| # | 错误 | 性质 |
|---|---|---|
| 13 | 「`ARIA_PLUGIN_ROOT` 全仓未赋值」— **测错总体** (grep 的是仓内何处 set, 而它由插件运行时在仓外设; 仓内真正约定是 `CLAUDE_PLUGIN_ROOT`, 66 处) | 问错问题 |
| 14 | 两分支路径解析把假绿换成**对所有第三方采用方恒红** —— 而本 Spec 逐字引用过「假绿的反面是恒红」这条判据 | 同一文件内既立判据又违反它 (第 4 次) |
| 15 | **SC-3 期望值未随 D1 扩面更新** (D1 从一处扩到两处, SC-3 仍写 ==1) —— 且这条 SC 正是上一版为「零裁量」专门重做的 | 同上 (第 5 次) |
| 16 | §Why 断言 #137 (a) 腿陈述成立, 与**自己上一 session 发布的订正评论**正面冲突 | 把两个不同的「(a) 主张」混为一件事 |

**关键教训**: 本版通过了编排层的 **23 项机械自检**, 而 TC-A / #13 / #14 全部**在自检覆盖之外** —— 自检验的是「我写下的断言的值对不对」, 验不了「我该不该问这个问题」。**机械自检抓错值, 抓不了错问题。**

## 五轮下来从未被动摇的部分

| 结论 | 确认方式 |
|---|---|
| 病是真的 (三分支名返回完全同形 `runs:[]` RC=0) | R5/code-reviewer 用真 aether 第三次独立复现 |
| 根因是「散文流程 + helper 两份实现, AI 走散文那份」 | R3 发现, R4/tech-lead 独立复核成立, 五轮无人推翻 |
| 存在性核验方向正确 (须精确比对而非 pattern) | R2 / R4 / R5 三次受控实验 |
| Rule #6 第二行「照跑 AB」 | SOT 直接管辖条款, 3 席逐字核过 |
| Level 3 | `project.md` 判据表 |

**反复失败的只有一件事: 把这些结论写成可执行契约。**

## 处置

`max_rounds` = 6 (owner R4 后加 2), 已用 **5**, 余 **1**。`converged: false`。处置须 owner 裁定。
