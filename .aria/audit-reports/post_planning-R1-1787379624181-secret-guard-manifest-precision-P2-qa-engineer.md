---
seat: P2-qa-engineer
round: R1
checkpoint: post_planning
spec: secret-guard-manifest-precision
verdict: APPROVE
ready_for_a3: true
counts: {critical: 0, major: 0, minor: 0}
counts_r1: {critical: 0, major: 3, minor: 1}
timestamp: 2026-08-22T01:00:00Z
---

# post_planning R1 — P2 qa-engineer — secret-guard-manifest-precision

审计对象: `detailed-tasks.yaml` 对 `proposal.md` (SC-1..SC-7, What.1b/What.3) 的测试策略忠实性。
基线核实: `git -C aria log -1` = `400f0bc`（与 proposal 冻结基线一致，Impact/行号引用可直接核对，未见漂移）。

## 实测表 (对当前树 = 400f0bc 直接探针; 命令文本 jq -n 构造 stdin，不执行)

| # | 场景 | 探针 | 期望(基线) | 实测 exit | 结论 |
|---|------|------|-----------|-----------|------|
| 1 | SC-1 真实泄露形态 | `jq -c '{model, env:(.env//{})}' ~/.claude/settings.json` (Bash) | 0 (baseline-failing) | 0 | 一致 |
| 2 | SC-1 变体 cat | `cat ~/.claude/settings.json` (Bash) | 0 | 0 | 一致 |
| 3 | SC-2 嵌套探针 | `Read{file_path: ~/.claude/settings.json}` | 0 | 0 | 一致 |
| 4 | SC-5 守卫 1 | `cat ~/.bashrc` (Bash) | 2 | 2 | 一致 |
| 5 | SC-5 守卫 4 (争用形态) | `cat .bashrc` 单空格裸相对名 (Bash) | 2 | 2 | 一致 |
| 6 | SC-5 守卫 5 | `cat "$HOME/.bashrc"` (Bash) | 2 | 2 | 一致 |
| 7 | SC-5 守卫 6 (多行) | heredoc 中段 `cat ~/.bashrc` (Bash) | 2 | 2 | 一致 |
| 8 | lens-4 判据 | `Edit{file_path=test.sh, new_string 含 "cat ~/.bashrc"}` | — | 0 (不拦) | 见 P2-3 |
| 9 | lens-4 判据 | `Write{file_path=test.sh, content 含 "cat ~/.bashrc"}` | — | 0 (不拦) | 见 P2-3 |

8/8 行为断言（含 #1-7）与 TASK-001/TASK-008 的「基线 RED/GREEN」声称逐条一致，未发现基线声称造假。附带证据：审计过程中本席自己构造探针脚本时，第一次尝试把 `echo "... cat ~/.bashrc ..."` 直接内联在外层 Bash 工具调用里，被当前活体 hook **真实拦截**（活体二次复现，见 P2-4）。

## Findings

**[P2-1] Major — TASK-003 的「基线 RED」窗口无留痕机制，红绿证据链在 TASK-002/003 之间可能永不落地**

proposal SC-3 与 TASK-003 都要求「对 TASK-002 后的树跑 RED」——这是一个**中间态基线**（非 400f0bc 冻结树）。detailed-tasks.yaml 里，凡是对 400f0bc 冻结树的红绿声称都显式要求留痕（TASK-001 `"对 400f0bc 跑: 4/4 FAIL ... — 留痕 RED"`；TASK-011 `"基线数对 git archive 400f0bc 冻结树实测 (非活树)"`），但 TASK-003 的 verification 只写「对 TASK-002 后的树跑: ... RED」，**没有**要求（a）TASK-002 必须先落为可引用的独立提交、或（b）RED 跑测输出被捕获进可审计产物。若 B.2 执行者把 TASK-002+003+004 在同一编辑会话里一次性做完再跑一次测试，"RED 曾经发生过" 就成了一句无法事后验证的自述——不同于 400f0bc 有 SHA 可 `git show` 复核，中间态一旦被后续 TASK-004 的 diff 覆盖就不可复现。

本仓同一测试文件里已有可复用先例（#128 段多处 `"canonical = af87cae, the direct pre-#128 parent commit"`），即：对中间态基线的红绿声称必须绑定一个可引用的提交。

**可执行口径建议**：
1. TASK-002 的 deliverables 追加一行：完成后独立提交（哪怕后续会被 squash），产出可引用 SHA；
2. TASK-003 的 verification 追加：把 RED 跑测的完整输出（pass/fail 计数 + 失败 case 名）连同 TASK-002 的提交 SHA 一并写入一份留痕产物（可复用 TASK-007 已经在用的 `.aria/notes/` 路径模式），而非仅在 verification 文字里断言。

**[P2-2] Major — TASK-007 的 `carries_sc: [SC-4]` 属挂名，其 verification 未判定 SC-4 的实际判据**

TASK-007（"路径清单型 pattern 行枚举"）的 deliverable 是一份内部分类笔记 (`.aria/notes/...pattern-rows.md`)，verification 只检查「清单是否含 :709/.env/id_rsa/claude-config 行，命令注入型是否排除」——这判定的是**枚举完整性**这个内部工件，不是 SC-4 本身的判据（"此前被误拦的敏感名字面量位置形态，现在放行"）。SC-4 的真实红绿判定完全由 TASK-009（RED）和 TASK-010（GREEN 翻转 + 反事实）承担；TASK-007 即使被跳过或枚举有遗漏，只要 TASK-009/010 独立写对 fixture，SC-4 依然会被判"过"——`carries_sc` 字段因此对 SC-4 的可信度没有额外贡献，是纯挂名。

不是空判据（TASK-007 确实是 SC-4 达成的必要前置工作），但 `carries_sc` 语义应该只标记"承担判定"的任务，否则 `sc_coverage_crosscheck` 表面上 SC-4 有 3 个任务背书，实际judging power 只来自其中 2 个。

**建议**：从 TASK-007 的 `carries_sc` 移除 SC-4（标注为纯前置/scaffolding 任务，不进 `sc_coverage_crosscheck`），或者反过来把它变成真判据——例如追加一条 verification："TASK-009 六条 fixture 覆盖的 pattern 行 ⊆ 本清单路径清单型行号集合"（枚举完整性→fixture 覆盖度的可判定交叉核验）。

**[P2-3] Major — TASK-001 notes「测试文本含敏感名字面量会被现行 hook 误拦」表述不成立，误导执笔者到错误的规避通道**

探针验证（实测表 #8/#9）：hook 的 `Read|Edit` 分支只查 `file_path`（:546-548 起，`[[ -z "$file_path" ]] && exit 0` 之后只对 `lower_path` 做正则），**从不检查** `tool_input.new_string`/`old_string`/`content`；`Write` 工具甚至根本不在 `case "$tool" in Read|Edit|Bash` 的分发范围内。实测：`Edit{file_path=secret-guard.test.sh, new_string="... cat ~/.bashrc ..."}` 与 `Write{... content="... cat ~/.bashrc ..."}` 均 exit=0（不拦）。

也就是说，**用 Edit/Write 工具本身把含敏感名字面量的 fixture 文本写进测试文件，不会被 hook 拦**——TASK-001 notes 里"测试文本含敏感名字面量会被现行 hook 误拦"这个归因是错的。真实会触发拦截的通道是：**执笔 agent 若改用 Bash 工具（heredoc / `cat >>` / `sed -i` 等）去拼接/追加同样的文本**，Bash 分支的 risky_patterns 是对整条命令字符串做无位置区分的正则匹配（这也正是 What.3 要收敛的那类误报），此时字面量出现在 echo/heredoc 的"散文位置"仍会命中——本席在构造探针脚本时就活体二次复现了这一点（外层 Bash 工具调用里一句 `echo "...cat ~/.bashrc..."` 被真实拦截，须改用文件+变量拼接规避）。

这个误归因有实操风险：若执笔者信了 notes 字面意思，可能会在**持久化的测试 fixture 字符串本身**里插入 `# guard:ack:` 或做字符串拼接混淆（TASK-001 notes 建议的两种规避手段），这对 Edit/Write 路径是多余且会污染 fixture 可读性/grep 能力；而对 Bash 路径又只说对了一半（`# guard:ack:` 只对触发拦截的那条**外层 Bash 命令**有意义，不该写进被追加的文件内容里）。

**建议改写**（对应本审计 lens 4 给出的方向）：
> "AI 用 Bash 工具（heredoc/`cat >>`/`sed`等）拼接含敏感名字面量的 fixture 文本时，外层 Bash 命令会被现行 hook 误拦（散文位置误报，What.3(a) 已知限）——与 Edit/Write 工具直接写入内容无关（hook 的 Read|Edit 分支只查 file_path，Write 甚至不在分发范围内，均不查内容）。若确需用 Bash 拼接，在**该外层 Bash 命令**上加 `# guard:ack:`；优先直接用 Edit/Write 写入，从结构上绕开该问题。"

**[P2-4] Minor — SC-1 变体覆盖表述精度**

proposal SC-1 只说 "grep TOKEN ~/.claude/settings.local.json" / "python3 -c ... ~/.claude.json" 各 ≥1 条同断言，TASK-001 verification 逐字复述了这 4 条形态，一致，无实质问题；仅记录：TASK-002 的 deliverables 文字未显式复述"reader 组 = 既有 12 reader + jq"这一 proposal What.1 的具体动作（隐含在"TASK-001 四条 fixture 翻 GREEN"的验收里可达成，但对照 What.1 文本，建议 deliverables 显式点名 `jq` 加入 reader 组，避免执笔者漏看只加了 claude-config 敏感名组而漏加 jq reader）。不影响判定方向，Minor。

## 其余透镜结论（无 finding）

- **lens 1**（fixture 任务基线声称 vs proposal 声称）：TASK-001/003/005/008/009 的基线方向（RED/GREEN）逐条与 proposal SC-1/SC-2/SC-3/SC-4/SC-5 一致；抽测 7 条（超过 ≥3 门槛）全部吻合，未发现方向写反或数量不符。
- **lens 3**（TASK-008 六条守卫形态是否现行全 2）：实测 4/6（含单空格裸名 + heredoc 多行两个高风险形态）全部 exit=2，无恒绿失效迹象；未实测的 2 条（`grep X ~/.zshrc` / `sed -n 1p /etc/profile`）与已测 4 条共用同一条 :709-710 pattern 行、字符类完全同构，判定为同风险面，未额外抽测。
- **lens 5**（除 P2-2 外）：SC-1/2/3/5/6/7 对应任务的 verification 均含可判定的红绿/计数断言，未见其余挂名。

## 判定依据

3 Major (P2-1/P2-2/P2-3) → 触发 "任一 Critical 或 ≥2 Major → REVISE" 判据。**verdict: REVISE, ready_for_a3: false**。

## v2 终判

对 `detailed-tasks.yaml` v2 (metadata.planned_by 已标注 "v2 = post_planning R1 findings 修订") 逐条复核本席 R1 四项 finding 的落地：

| finding | v2 diff 位置 | 判定 | 说明 |
|---|---|---|---|
| P2-1 (Major, TASK-003 RED 留痕) | TASK-002.deliverables 新增 "独立 commit 落地 (P2-1: 作为 TASK-003 RED 留痕的可引用中间态 SHA)"; TASK-003.verification 改写为 "对 TASK-002 独立 commit 的树跑 (留痕引用该 SHA, 同 #128 af87cae 引用式)" | **closed** | 与 R1 建议的两点（独立提交 + 引用式留痕）逐字对应；`execution_order` 也同步把 TASK-003 从与 TASK-002 同一 parallel_group 拆出为独立 order 3 分组，结构上避免"未提交先并行改"的竞态 |
| P2-2 (Major, TASK-007 挂名 SC-4) | TASK-007.carries_sc 由 `[SC-4]` 改为 `[]`（注 "v2: 前置/枚举任务, 非 SC-4 判定承载 (P2-2/P1-m3); 判定在 TASK-009/010"）；新增 verification "交叉核对: TASK-009 的 .env 面 fixture 所触及的行 ∈ 本清单"；`sc_coverage_crosscheck.SC-4` 由 `[TASK-007, TASK-009, TASK-010]` 改为 `[TASK-009, TASK-010]` | **closed** | 同时采纳了 R1 给出的两个可选修法（摘除挂名 + 补交叉判据），非二选一，力度超出建议下限 |
| P2-3 (Major, TASK-001 note 误归因) | TASK-001.notes 整段重写: 明确"误拦点不在测试文件 (hook Read/Edit 面只看 file_path, Write 不经 hook, 不检查内容 — P2 实测) 而在 AI 用来写 fixture 的外层 Bash 命令"; 规避手段改为"外层命令附 # guard:ack: 或用 Edit 工具写入; 持久化的 fixture 字符串本身不需要 ack" | **closed** | 与本席实测证据 (Edit/Write exit=0 不查内容) 及建议改写文本一致，消除了"在持久化 fixture 里误加 ack/字符串混淆"的误用风险 |
| P2-4 (Minor, TASK-002 缺失 jq reader 显式点名) | TASK-002.deliverables 首行改为 "risky_patterns 新增 claude-config 行 (**reader 组 = 既有 12 + jq**; 敏感名组 3 条目, 抽成 bash 变量供 TASK-004 复用)" | **closed** | jq 已显式点名；附带把敏感名组抽成变量供 TASK-004 复用，对 TASK-004 notes 里原本单独提的"防两处漂移"建议也顺带落地 |

**v2 diff 本身复核（无新增问题）**：TASK-003 的 RED/GREEN 明细改写为 "直读无管道 1（TASK-002 后已 GREEN）+ 管道 jq{env} 1 + keys/wc/>/dev/null 3 + 行级排除 2 + 混合源 1 + .env 对照 1 = 9" —— 与 proposal SC-3 的 9 条表逐项核对一致，计数无漂移；TASK-002/003/004/010 的 dependencies 与 parallel_groups 联动改写后仍满足 INV-1（TASK-008 早于 TASK-010）与 INV-3（`sc_coverage_crosscheck` 每个 SC 至少一个真判据任务）；未发现 v2 引入的新 Critical/Major/Minor。

**未闭合项**：无。本席 R1 提出的 3 Major + 1 Minor 全部 closed。

**最终 verdict：APPROVE，ready_for_a3: true**（counts 归零；R1 计数保留在 `counts_r1` 供审计轨追溯）。
