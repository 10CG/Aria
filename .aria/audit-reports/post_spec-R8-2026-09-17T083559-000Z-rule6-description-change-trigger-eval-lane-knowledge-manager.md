---
checkpoint: post_spec
mode: convergence
rounds: 8
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T09:17:18.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

# post_spec Round 8 — knowledge-manager 席 (复核轮)

被审 SHA `a563192` (v9, 仓库 HEAD)。drift_guard 仍未配置 (`.aria/config.json` 实读核验: 无 `drift_guard` 键) ⇒ `drift_check_skipped: true`, 沿用 R4–R7 判定。本轮是 owner 2026-09-17 裁定 max_rounds 7→8 后的复核轮, 只审 v9 相对 v8 的四处改动 (SC-9 两锚点 / SC-12 短语 / T2b+T4 措辞 / `fault_matrix.py` 硬化+RESULT v8), 不重开 R1–R7 已闭合的题目。

## R7 对账

| # | R7 finding (本席) | 状态 v9 | 依据 |
|---|---|---|---|
| 1 | testing/proposal.md §T2b+SC-2+SC-13 (issue): T2b「原样搬到」按字面 (删源文件) 会打断 D3 前置表第 3 行与 SC-13 的逐字节比对; T4「搬入」与 SC-4 同构 | **closed** | T2b 已改「原样复制到...(基线目录的原件保留不动——前置表第 3 行的机读实证与 SC-13 的逐字节比对都要求它还在)」; T4 已改「复制入 (逐字节同基线, 基线目录原件保留——SC-4 的 diff 要求它还在)」。对全文 `grep -n 搬` 零命中, 确认此前仅有的 2 处「搬」字全部替换、无第三处遗漏。两处新文都消除了「删除原件」的字面读法, 与 SC-2 第 3 行 / SC-4 / SC-13 的隐含前提 (原件仍在基线目录) 完全自洽。 |
| 2 | documentation/proposal.md §D1(SOT §2 新句)+SC-12 (issue): SC-12 五短语不含「含新增 skill」; 手册侧 D2「新增 skill 的首个 description 同样要过本场景」同样没有对应 SC | **partially** | SC-12 已把「含新增 skill」加入六短语清单, 且核对 D1 的 SOT 新句 (第 41 行) 确实含该短语、`grep -cF` 可命中——**此半 closed**。但手册侧 D2「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」(第 58 行) 仍无任何 SC 引用; T2 的转录清单 (第 132 行) 只列「参数钉死 / 不设比较判据 / 负控 ≤5/10 / 连续 2 轮升级 / 逐调用健康检查」等, 未点名这句; 逐一核对 SC-8 (标题存在性) / SC-9 (负控门槛与 fail/作废后果) / SC-10 (参数钉死行) 均不覆盖它——**此半仍 open**, 详见 Findings。 |

**closed 1 / partially 1 / open 0**。

## Findings

- [major] documentation/proposal.md §D1(SOT §2 新句)+D2(套件)+SC-12 (issue): SC-12 已加「含新增 skill」锚定 SOT 核心句 (R7 finding 此半 closed); 但手册侧 D2「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」一句仍无任何 SC 覆盖, T2 转录清单未点名它, 转录时漏写不会被任何 SC 拦住, OQ-9「新增 skill 算 description 变动」的裁定对交互模式作者的落地路径事实上仍无机械保障, 与 SC-12 自身「三处漏掉任一处即转红」的既定标准不一致 (此处是第四处却不在清单里)。

## 观察

- **本轮四处改动逐一独立复核, 三处半确认修对**: (1) T2b/T4 的「搬」→「复制 (原件保留)」: 全文 `grep 搬` 零命中, 措辞与 SC-2/SC-4/SC-13 的隐含前提自洽 (见 R7 对账第 1 条)。(2) SC-9 两个新锚点: 直接读 D2 正文确认「作废在以下任一情形发生」那一行同时含「逐调用健康检查不通过」「足以改变判定」「≥ 6/10」「不得 ship」四词; 含 `classify_calls.py` 的那一行 (第 51 行, 单行长段) 同时含「两种可能」。按构造法可知: 若把「足以改变判定」删回旧语义「存在任一次不健康的调用」, 或把「两种可能」删掉, 对应锚点检查会转红——这正是 SC-9 设计目的, 判为修对 (该 major 由 qa-engineer 在 R7 提出, 本席独立复核通过)。(3) RESULT.md 版本引用同步: 对 v9 全文 `grep -n RESULT` 逐一核对 12 处, 其中 6 处带版本号的全部同步为「v8」(第 9/16/50/53/69/124/139 行, 含重复), 另 6 处不带版本号或有意留活 (第 51 行「RESULT.md『v6: 逐调用健康检查』一节」引用的是 RESULT.md 内部实验批次标签、非文档版本号, 已核对该标题在 RESULT.md 第 61 行原样存在; 第 57/71/108 行不引用版本号; 第 136 行 T5 的「当时 RESULT.md 的版本号」是特意保留的动态占位, 承接 R6 fix 的设计) 均保持原状。这是「RESULT 再修订须同步重核每一处引用」规则创建以来第一次被真正触发, 核验结果: 执行到位、无遗漏。(4) `fault_matrix.py` 硬化: 代码第 109-114 行已把无条件 `shutil.rmtree` 改成「已存在且非空→报错退出 2, 不存在→建, 已存在且空→复用」三分支。本席在 scratchpad 用绝对路径独立复现: 对已有 78 个文件的非空目录重跑→exit 2、文件原样保留 (未被清空); 对预建空目录重跑→exit 0、24 用例全符合; 对不存在目录→exit 0、24 用例全符合; 反事实 (复制整套工具到 scratchpad, 删掉 `classify_calls.py` 里对报错结果帧的判定后重跑)→5 例不符 (F1_result_error / S1_overbroad_fault_in_shouldnot_half / S2_correct_fault_on_one_should_query / S8_two_run_fault_should / S10_negctrl_two_run_fault_x6)、exit 1, 与 RESULT v8 文中列出的 5 个用例名逐一相同。四处改动里前三处 (含另外两席各自负责发现的 major) 结论都是修对, 不入 Findings。
- **RESULT v8 changelog 的「归档...就是重跑产物」措辞比实际略宽, 但结论未受影响**: 用 `git diff 76959c8 a563192` 精确核对, `v6-per-call-health-opus5/fault-matrix/` 下 22 个有真实子进程调用的用例文件确认被本轮硬化后的脚本重新生成 (内嵌调用日志文件名按纳秒级时间戳解码为 2026-09-17T08:29:52Z, 与 a563192 提交时间 08:35:19Z 前后一致; 另 2 个用例 F8_shim_not_on_path/M1_unmapped_query 结构性无随机内容, 两次跑理应字节相同, 非漏跑); 但 `fault-matrix-counterfactual/` 整个目录在这次提交里零改动 (`git diff` 空), 其内容仍是 2026-09-15 (post_spec R6 时期, commit `76959c8`) 的产物, 并非本轮「用加固后的脚本」重新跑出来的。RESULT v8 changelog 原句「归档在 `fault-matrix/` 与 `fault-matrix-counterfactual/` 的就是加固后重跑的产物」对后半目录严格来说不成立。不过硬化改动本身只触及「`--out` 目录已存在且非空」的处理分支, 不触及 `classify_calls.py` 的判定逻辑, 本席用硬化后脚本的独立副本单独重跑反事实 (见上一条), 复现出与旧产物完全相同的 5 例不符/exit 1——即两版脚本对该反事实的结论确实一致, 只是 changelog 里「两个目录都被重跑」这句话本身不精确。不建议改判 major: SC-13 自身没有引用这句 changelog、也没有要求反事实产物的时间戳, 不影响任何 SC 可执行性, 不阻塞 Phase B; 建议 Phase B 转录 T5 时若要引用 RESULT v8 版本行, 顺手把这句改成「fault-matrix/ 用加固后的脚本重新生成; fault-matrix-counterfactual/ 的产物未变 (硬化不影响判定逻辑, 结论已用硬化后脚本独立复核一致)」, 更精确且不留后续审计再挖一次的成本。
- **`fault_matrix.py` 自身的用法文档字符串未随硬化更新**: 文件头 (第 11 行)「退出码: 0 = 全部用例符合预期; 1 = 有不符; 2 = 环境不全 (找不到套件或 run_eval.py)」只列了 exit 2 的一种成因, 硬化后「`--out` 目录已存在且非空」也返回 exit 2 (第 113-114 行), 但文档字符串没提第二种成因。不影响 SC-13 (只要求 exit 0/1 两种结果), 纯粹是工具自身可读性问题, 不阻塞 Phase B, 留给 Phase B 顺手一并改。
- **文档结构自检 (点 3): OQ-9 / T2b / SC-13 / Key Deliverables 互相引用无新增矛盾**: v9 的 diff 没有触及 OQ-9 本文 (仍是 v8 定稿的「算」+ 代价陈述), Key Deliverables 第 116 行仍只是指向 T2b 的锚点、不重复「搬/复制」措辞, 不会因 T2b 改词产生自相矛盾; SC-13 本身在 v8→v9 没有变化 (它已经假设基线原件保留, 这正是 T2b/T4 改词后才对齐的前提), 三处互相印证一致。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 minor。本席 R7 的 2 条 major 中 1 条 closed (T2b/T4「搬」歧义)、1 条 partially (SC-12: SOT 侧已锚「含新增 skill」, 手册侧 D2 对应句仍无 SC 覆盖)。本轮未发现新的 critical/major; 两项新观察 (RESULT v8 changelog 对 counterfactual 目录的措辞偏宽 / `fault_matrix.py` 文档字符串未同步退出码语义) 经独立复核确认不影响任何 SC 可执行性、不阻塞 Phase B, 计入观察而非 Findings。

## Vote

REVISE

## 术语与关系对照表

| 术语/概念 | proposal.md v9 | RESULT.md v8 (基线) | SOT/CLAUDE.md/手册 (拟改文本现状) | 一致性 |
|---|---|---|---|---|
| T2b/T4「搬」→「复制 (原件保留)」 | 两处均已改「复制」并显式写明基线目录原件保留不动 | 不涉及 | 不涉及 (尚未转录, T2/T3/T5 待执行) | 一致, R7 finding 1 closed |
| SC-12「含新增 skill」+ 手册 D2 覆盖 | SOT 核心句锚点 (D1 第 41 行) 已加短语并被 SC-12 锚定; 手册 D2 句 (第 58 行) 仍在但转录纪律与全部 SC 均未点名它 | 不涉及 | 待转录; SOT 侧有 SC 兜底, 手册侧无 | SOT 侧一致, 手册侧缺口, R7 finding 2 partially, 见 Findings |
| SC-9 两新锚点 (足以改变判定 / 两种可能) | D2 正文 (第 51/55 行) 已含两短语, 与 SC-9 新增判据逐字对应; 独立复核: 现文全绿, 反事实改回旧语义会转红 | 不涉及 | 待转录 (手册 §场景 4b) | 一致 (qa-engineer 的 R7 major 已闭, 本席独立复核通过) |
| RESULT.md 版本引用同步 (v7→v8) | 12 处 RESULT 提及逐一核对: 6 处带版本号全部同步为「v8」, 6 处不带版本号或有意留活 (§v6 段落名 / 结论 1 / T5 的「当时版本号」占位) 保持原状, 无遗漏无误改 | 本文件版本 8, 「引用方请写 v8 @ SHA」 | 不涉及 | 一致, 「同步重核每一处引用」规则首次触发且执行到位 |
| `fault_matrix.py` 硬化 (rmtree→分支判断) | Key Deliverables/T2b 引用同一工具文件, 未描述硬化细节 (细节在 RESULT/代码里) | v8 changelog: 「输出目录已存在且非空时报错退出...用加固后的脚本重跑矩阵与反事实, 结论不变」 | 不涉及 | 主矩阵 (`fault-matrix/`) 已用 git diff + 时间戳独立验证确系重跑产物; `fault-matrix-counterfactual/` 目录零改动仍是 R6 时期产物, changelog「两目录都是重跑产物」措辞偏宽, 结论本身用硬化后脚本独立复核一致, 不影响 SC, 见观察 |
| `fault_matrix.py` exit code 2 语义 | 不涉及 | 不涉及 | 不涉及 (工具自身文档字符串, 非规范转录目标) | 硬化后 exit 2 有两种成因, 文档字符串只写了一种, 轻微漂移, 不影响 SC-13, 见观察 |
