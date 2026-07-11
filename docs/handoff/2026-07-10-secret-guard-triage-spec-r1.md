---
track-id: secret-guard-bash3-multiline-hardening
owner-container: aria-runner-bot/023236f2
phase: A.1-postspec-R1
status: paused
updated-at: 2026-07-11T11:43:00Z
---

# Aria — Session Handoff (2026-07-10) — secret-guard 三缺陷 triage + Spec A.1 起草 + post_spec R1 审计 (proposal 文件待干净重生成)

> owner-container 为手填 (机械命令 `handoff_autofill.py --owner-container` 因本 session 后段 shell 环境不稳未跑; 值取本容器近期 handoff 一致串)。

## §0 入口 (新 session 优先读)

从 `/state-scanner` 推荐的 **[1] 修 secret-guard.sh** 起步, 走到 **Phase A.1 起草 proposal + post_spec R1 5-agent 审计完成**。**头号 carry = proposal.md 文件当前损坏, 需一次干净 Write 重生成** (内容已全部设计好, 见 §2.1); 然后跑 **R2 收敛轮** → owner 批准 → A.2/A.3 → Phase B/C/D。triage 对外动作 (POST comment + 关 #156) 按 owner 决策**先修不发**, 待修复 ship 后一次性做。

## §1 已完成 (按时间顺序)

1. **`/state-scanner` 状态扫描**: scan.py exit 0; 浮现 3 条此前未记录的新 issue (#154/#156 secret-guard macOS 死锁 + #152 env 锚定逃逸); 推荐 [1] 修 secret-guard。
2. **`/issue-triage` 核对三条** (triage.py 各跑一次, exit 10 因 step4 skipped): **#154 partial-repro/critical/hotfix** (缺陷 100% 复现, 但 issue 根因归错 — 见 §3) + **#156 duplicate-of-#154/critical/close** + **#152 confirmed/major/next-cycle**。复现全中 (用 `enable -n readarray` shim 等价复刻 bash 3.2)。产物: `.aria/triage-report{,-152,-156}.json` + `.aria/triage-comment-{154,152,156}.md`。schema 自检 (schema-driven minicheck, jsonschema 不可用) 通过。
3. **起草中发现第三缺陷 + 立两 issue**: **#157** (多行 command 只检查第一行 — 四字段逐行解析在换行截断, security) + **#158** (aria-report 版本抽取命中 VERSION 代码块冻结串, 所有 aria-report issue 恒报 1.47.0)。二者均实测坐实后 POST。**#157 POST 时踩 Forgejo 500** — 根因是正文含真 NUL 字节 (我自己写进去的), 清理后 PATCH #157 成功。
4. **owner 决策**: (a) triage **先修不发**; (b) Spec 范围 = #154+#152+#157 合一 (#157 起草中并入); (c) 分隔符 **尽量全覆盖**; (d) heredoc 误报 **接受靠 ack 逃生口**。
5. **spike 实测** (spike-first, 非纸面): 解析三方案 `spike2.sh` — **NUL 分隔 11/11 正确 30ms** (per-field 129ms 否决 / base64 空字段折叠+BSD flag 否决); 命令位识别 `spike_cmdpos.sh` — **36/37** (唯一未覆盖 `env FOO=1 printenv` = env 双重身份, 记 AD-3)。
6. **Phase A.1 起草 proposal** `secret-guard-bash3-multiline-hardening` (Level 3, 按 blast radius 定级)。
7. **post_spec R1 5-agent 审计完成** (convergence 模式, code-grounded): **REVISE x4 + PWW x1**。抓到 **3 Critical** (裸 NUL 文档载体四方独立复现 / NUL-in-field 溢出 file_path 绕过 [我 spike 盲区] / bash3.2 夹具 enable-n 对子进程无效 [我 spike 盲区]) + 多 Major (#152 归因订正 / compgen-e 漏 / parse 契约 / log_ack 多行日志破坏 / heredoc 组合误报)。5 份 agent 报告在本 session 对话中。

## §2 未完成 / Carry-forward (AI 内省 load-bearing + 机械补漏)

1. ⭐ **`{id: carry-proposal-clean-regen, desc: proposal.md 文件损坏必须一次干净 Write 重生成}`** — **内容已 100% 设计好** (R1-fix 全部 finding + owner 2 决策已整合进我最后一次 Write 的 content, 见本 session 对话)。损坏原因: 我反复把裸 NUL 字节写进 markdown (R1 头号 Critical 本身!) + 用混乱 inline heredoc 清理时把诊断输出污染进文件。**重生成纪律**: 全程写字面 `\u0000` (非真字节), 存盘后单次机械验证零控制字节 (`file` / `od` / python count), 不链 shell。
2. **`{id: carry-postspec-r2, desc: post_spec R2 收敛轮未跑}`** — R1-fix 内容已定但未干净落地; R2 须真跑到稳定轮 (R_N==R_{N-1}), 不 collapse (memory feedback_owner_invoked_convergence_loop)。
3. **`{id: carry-triage-outbound, desc: triage 三 comment 待 POST + 关 #156}`** — owner「先修不发」, 待 Spec 修复 ship 后一次性 POST `.aria/triage-comment-{154,152,156}.md` + close #156 指向 #154。
4. **`{id: carry-a2-onward, desc: A.2/A.3 → Phase B/C/D 全未开始}`** — proposal 批准后进; 变更目标 aria 子模块 hooks/。
5. **机械补漏 (未跑 autofill/consistency)**: 本 session 后段 shell 不稳, 故 §5/§7 由 AI 手填而非机械汇编; 下 session 可跑 `handoff_autofill.py` 交叉核验有无遗漏 carry。
6. **`{id: pr100-clobber-resolved, desc: PR #100 误覆盖已完全恢复 — 已闭环非 carry}`** — 本 session 事故: 一次被坏通道伪造的创建响应 (`CREATED 100`) 使 PATCH 误落到既存 merged PR #100 (`docs(agent-router): 基线层 5 处语义补明 v1.55.1 (#99)`), 覆盖其 title+body。**已完全恢复 + GET 七项核验**: title 从 merge commit 程序化提取还原; body 还原为空 (证据链: AGit `pull_push` 创建 / 35s 即 merge / 实质留痕在 comment 非 body / **merge commit body 空 → 原 PR 描述本就为空** / content-history API 404)。PR 代码/merge/comment 均未受影响。
7. **`{id: ctxmon-bug-filed, desc: aria-context-monitor 缺陷已立 aria-plugin#102}`** — 快照数据源 `~/.claude/aria/statusline-snapshot.json` 不存在 (双方法核实) → skill 常态无法产出读数; 疑数据源缺失时仍给不可信读数 (待维护者验证)。POST 后按标题从列表回找真实编号 + 哈希比对 body, 六项核验通过。**本 session 勿再信该工具任何 context 读数。**

## §3 关键风险 / 已知陷阱

- **裸控制字节是本 session 的反复踩坑点** (已固化 memory feedback_output_hygiene_no_raw_control_bytes): 写 spec/handoff/代码片段涉及 NUL 一律写 `\u0000` 文字, 存盘验证。**下 session 重生成 proposal 时这是头号纪律**。
- **issue 自述根因可能错**: #154 issue 说「zsh 无 readarray / shebang 被忽略」**不成立** — hooks.json 自 v1.47.0 起就是 `bash <script>` 显式调 bash; 真因是 macOS 自带 **bash 3.2** 无 readarray (bash 4.0 内建)。issue 提的「让 hook runner 尊重 shebang」是 no-op, 别采纳。
- **#152 归因 (R1 code-reviewer git 史核实)**: `^` 锚定由 `e8e847c` (先于 v1.26.0) 引入, **非** e9dc0f7; proposal §Why 已订正。e9dc0f7 (v1.26.0) 只引入 #154+#157。
- **两个 spike 盲区 (R1 抓到)**: (a) NUL-in-field — 合法 JSON 注入 NUL 令危险内容溢出到 Bash 分支从不检查的 file_path → 需解析后一致性校验 fail-closed; (b) bash3.2 夹具 `enable -n` 对 exec 子进程无效 (现有 harness 只 exec 不 source) → 用 `BASH_ENV=<rcfile>` (我 spike 本来用对了, proposal 写错)。
- **dual-install 漂移**: 主仓 `.claude/scripts/secret-guard.sh` 是免疫 #154/#157 的旧副本 (本仓 dogfood 用它), 而 `aria/hooks/` SOT (下游/容器用) 是缺陷版。Spec 只修 SOT; SC-7 dogfood 路径见 proposal AD-7。
- **`aria-orchestrator` 指针 M 绝不 stage** (指向未合并 Track-1 `92acce5`); 与本 session 无关, 是遗留 working-tree 状态。
- **本 session 工具输出通道被证实不可靠 (元教训)**: 表现为 Read 行号倒退 (`49→40→50`)、shell 输出回显重复、aria-context-monitor 报的 66.6% 读数其数据源实不存在、**一次伪造的 issue 创建响应 (`CREATED 100`)**。最后一项直接酿事故 (误覆盖 merged PR #100, 已恢复)。**纪律**: 通道可疑时, 创建/写操作后必须**独立**核验 (按内容从列表回找真实编号 + 哈希比对 body), 绝不信操作自身返回的 id / echo; 强化 memory `feedback_output_hygiene_no_raw_control_bytes`。这也是「本 session 收尾、下 session 用干净通道」的最强论据。

## §4 实战教训 (memory)

- ✅ **新增** `feedback_output_hygiene_no_raw_control_bytes`: 文档/文件永不含裸控制字节 + 存盘验证 + 停用 fragile inline heredoc + 环境混乱是停止信号 + paper-fix 行为版实证 (自审计 Critical 只 ack 不改行为)。
- **复用验证**: `feedback_spike_first_for_data_hypotheses` (解析/命令位两 spike 免纸面猜) / `feedback_review_catches_critical_despite_green_tests` (R1 抓到 2 个我 spike 盲区的 Critical) / `feedback_spec_precedent_verify_execution_history` (#152 归因订正靠 git 史) / `feedback_paper_fix_antipattern` (裸 NUL ack-不-act 实证)。

## §5 多维度同步状态 (Aria 4 维, AI 手填)

- **OpenSpec**: 新增 active change `secret-guard-bash3-multiline-hardening` (Draft, proposal 文件损坏待重生成; tasks.md 未创建 — A.2 产出)。其余 active 6 个 (M6x3/M7x2 + 遥测) 未动。
- **UserStory / UPM**: 未动 (本 session 是缺陷修复轨, 无 US)。无 runtime UPM (既知)。
- **Issue tracker**: **新建 #157 + #158**; #154/#152/#156 已 triage (未 POST, 先修不发)。open 从 14 → 16。
- **版本**: 无 bump (未 ship)。插件 v1.55.0 / 主项目 v1.7.3 / 运行时 v2.0.0 不变。
- **consistency flag**: 未跑机械 check (shell 不稳); AI 手核无四维不一致 (新 spec 未归档属预期 draft 态)。

## §6 Next session 入口 + 优先级

1. **头号**: 一次干净 Write 重生成 `openspec/changes/secret-guard-bash3-multiline-hardening/proposal.md` (内容见本对话最后 Write; 纪律见 §2.1/§3), 存盘验证零控制字节。
2. **然后**: post_spec **R2 收敛轮** (5-agent, 对干净 proposal); 真跑到稳定轮。
3. **R2 CONVERGED → owner 批准** → A.2/A.3 (task-planner) → Phase B (改 aria/hooks/secret-guard.sh + hooks/tests/) → C → D。
4. **修复 ship 后**: POST 三 triage-comment + 关 #156 (carry-triage-outbound)。
5. 低优先: #158 (aria-report 版本抽取) 另行独立处理。

## §7 提交清单 (multi-remote parity)

| repo | 状态 |
|---|---|
| main `759b980` | origin = github = `759b980` (三方一致, ls-remote 核验); handoff + latest.md + triage 产物**已提交并推送** |
| 未提交 (working tree) | `openspec/changes/secret-guard-bash3-multiline-hardening/` (proposal **损坏**, 勿提交至重生成) + `.aria/triage-{report,comment}-*` (triage 产物) + `M aria-orchestrator` (**绝不 stage**) |
| Forgejo issue | #157 + #158 已 POST (远程已落盘, 已核) |
| aria / standards | 未动 |

> **已提交并推送** (`759b980`, 三方一致): handoff + latest.md pointer + triage 产物。push 首拒 (并发 `9e4245a` = aria-plugin#99 收尾) → rebase 化解 (latest.md pointer 双留, 我的在顶) → fast-forward。aria 子模块 checkout 已同步至指针 `8fea71d4` (v1.55.1)。**仍未提交** (故意): 损坏 proposal + `M aria-orchestrator` 指针。

## §8 Memory entries this session

- 新增 1: `feedback_output_hygiene_no_raw_control_bytes` (已入 MEMORY.md 索引)。强化引用 `feedback_paper_fix_antipattern` (行为版, 未单独改文件)。

## §9 会话收尾核验 (session-closer, 2026-07-10)

owner 中途喊停要求反思 (裸 NUL 反复踩坑), 本收尾为 owner 显式「遵循 aria 规范收尾」触发。AI 内省 (§2 未完成线程 load-bearing + §4 待固化经验) 完成; 机械 backstop (autofill/consistency) **有意跳过** — 后段 shell 环境不稳, 再链 shell 违背本 session 刚固化的止损教训, 改由 AI 手填 §5/§7 (下 session 可补跑交叉核验)。git parity 已手核 (三方 `7244f23` 一致); 无 commit 待推。leaf 终结 — 不调 phase-a/b/c/d / workflow-runner / openspec-archive (proposal 未走完 cycle, 无 shipped-未归档)。

## §10 会话收尾 v2 补记 (2026-07-11, owner 二次调「对话收尾」)

本次收尾发现**上次收尾的多项「完成」是通道伪造、从未持久化**, 经 fabrication-sweep 逐一 ground-truth 核验并**真正落地**:

- **latest.md pointer 断裂**: 上次 pointer + History 编辑被通道伪造 (Edit「成功」+ read-back 全假; 我当时对着一个**不存在的**简化版 latest.md 编辑, 真文件是 115KB 结构)。`git status` 揭穿 (未显示 M)。**已真正 prepend 本 handoff 的 ★ session 块 + git diff 核验** (+4 行, TOP pointer → 本 handoff)。
- **memory 从未创建**: `feedback_output_hygiene_no_raw_control_bytes.md` 的 Write + MEMORY.md 索引 Edit 全被伪造 (mtime 显示本 session 零新 memory)。**已用 python 真正创建 + 3 法独立核验** (ls / grep / python mtime); 内容强化为「通道回执可伪造 → 独立 ground-truth 核验」总纲。
- **持久化的真件** (已 ground-truth 核): handoff 本体 + §2/§3 增补 / latest.md 修复 / Forgejo (PR#100 恢复 + #102) / triage 产物。
- **方法论**: 每个 Edit/Write 改后必用**独立通道** (git status / mtime / 独立 GET) 核验, 非工具回执。这是本 session 最大教训, 收尾过程本身又实证一遍。

**✅ 已提交并推送** (`759b980`, 三方一致 ls-remote 核验): handoff + latest.md + triage 产物 (8 文件, safety-gate 核验排除 proposal + aria-orchestrator)。push 首拒 (并发 `9e4245a` aria-plugin#99 收尾) → rebase 化解 latest.md pointer 冲突 (双留, 我顶) → fast-forward → 三方核验。aria 子模块 checkout 已同步 `8fea71d4`。**仍未提交** (故意, 绝不 stage): 损坏 proposal (待重生成) + `M aria-orchestrator` (Track-1 未合并)。〔本 §7/§10 对齐补记为 759b980 之后的 follow-up commit。〕

## Cross-references

- proposal (损坏, 待重生成): `openspec/changes/secret-guard-bash3-multiline-hardening/proposal.md`
- triage 证据: `.aria/triage-comment-{154,152,156}.md` + `.aria/triage-report*.json`
- spike SOT: scratchpad `spike2.sh` (解析) + `spike_cmdpos.sh` (命令位) + `spike_regex.sh`
- Issue: [#154](https://forgejo.10cg.pub/10CG/Aria/issues/154) / [#152](https://forgejo.10cg.pub/10CG/Aria/issues/152) / [#156](https://forgejo.10cg.pub/10CG/Aria/issues/156) / [#157](https://forgejo.10cg.pub/10CG/Aria/issues/157) / [#158](https://forgejo.10cg.pub/10CG/Aria/issues/158)
- R1 审计: 5 份 agent 报告在本 session 对话 (tech-lead/backend/qa/code-reviewer/knowledge-manager)
