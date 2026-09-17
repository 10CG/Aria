---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T00:31:13.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

# post_spec Round 7 — knowledge-manager 席

被审 SHA `15ab323` (v8, 仓库 HEAD)。drift_guard 仍未配置 (`.aria/config.json` 实读核验: 无 `drift_guard` 键) ⇒ `drift_check_skipped: true`, 沿用 R4–R6 判定。本轮为 max_rounds=7 的最后一轮, 按 owner 2026-09-15 裁定: 若本轮无 major, 由 owner 选「接受当前结论」。

## R6 对账

| # | R6 finding (本席) | 状态 v8 | 依据 |
|---|---|---|---|
| 1 | documentation/proposal.md §D5 item 7 仍写「开 issue」, 与「三张新 issue」口径 (头部/Key Deliverables/T6/SC-6 四处) 矛盾 | **closed** | v8 的 D5 列表现只有 1–6 项, 原 item 7 (「编排器不消费 runner 结果枚举」) 已整条删除; 其内容 (`CLAUDE_NO_OP` 等枚举与 Claude 最终消息编排器不读) 已合并进 D5.6 (现第 6 项) 「已知缺口」列表的第 (2) 条, 与其余 7 条已知缺口 (放弃后终态 / runner 补提交矛盾 / `unattended` 传递未定义 / 缺 skill-creator / GLM 未验证 / 新套件审阅 / layer-boundary-contract 文档过时) 并列。头部第 7 行、Key Deliverables (第 116 行)、T6 (第 137 行)、SC-6 (第 148 行) 四处「三张新 issue (D5.2, D5.3, D5.6)」现与列表项数 (1–6, 无第 7 项) 完全一致, 不存在「该开第四张 issue 还是不该」的双重口径。 |
| 2 | documentation/proposal.md §D6+文档头部: 头部「RESULT 再修订须同步重核」清单缺 §D6; D6 待转录句里版本号+SHA 补写指令缺「不转录」标记, 逐字转录会自相矛盾 | **closed** | (a) 头部「基线数据」行 (第 9 行) 已从「同步重核本文 §Why 与 §D2 §D3」的枚举式清单改为「同步重核本文**每一处**引用 RESULT 的位置, 以 `grep -n RESULT` 逐处列出, 不只看某几节」—— 这是机制性改法 (机械枚举取代人工枚举), 结构上覆盖 §D6、§Impact、T8 等全部引用点, 不再依赖「有没有把某一节的名字写进清单」。(b) D6 待转录的引号文本 (第 103 行) 已删去硬编码的「v6」版本号与「写入时附当时的版本号与提交 SHA」这句指令, 该指令改落到 T5 (第 136 行): 「转录第三条时在基线路径后补写当时 RESULT.md 的版本号与主仓提交 SHA (**这是给执行者的指令, 本身不转录**)」, 与 D4 的「(不转录)」标记用法一致。两点均已修复, 现状: D6 引号内文本自身不含版本号, 不会产生「写死 v6 又说写入时用当时版本」的矛盾。 |

**closed 2 / partially 0 / open 0**。

## Findings

- [major] testing/proposal.md §T2b+SC-2+SC-13 (issue): T2b 用「原样搬到」把 `claude-shim.sh`/`classify_calls.py`/`fake-claude`/`fault_matrix.py` 迁到 `tools/trigger-eval/`;「搬」若按字面执行 (删除源文件), 会同时打断 D3 前置表第 3 行的证据路径 `v6-per-call-health-opus5/claude-shim.sh` (SC-2 用 `test -e` 核验) 与 SC-13 自身的 `cmp` 比对 (两者都要求该文件仍在 `ab-results/.../v6-per-call-health-opus5/` 原处)。已实测: 该路径目前存在 (`test -e` 为真); T4 对套件文件用同一「搬入」措辞且 SC-4 有同构依赖 (`diff` 需要旧路径仍存在), 但两处均未注明「复制、不删除原件」。
- [major] documentation/proposal.md §D1(SOT §2 新句)+SC-12 (issue): SOT §2 新句含「不做 description 改动 (**含新增 skill**)」, 是 OQ-9「新增 skill 算不算 description 变动」的落点; 但 SC-12 只核对该行含 5 个短语 (`unattended == true` / 不做 description 改动 / 放弃整个任务 / 撤销本任务已做的全部改动 / 写明), **不含「新增 skill」**。手册侧 D2「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」同样没有对应 SC。转录 (T1/T2) 若漏掉这两处「含新增 skill」表述, 自主运行时的禁令与手册的建套件义务都会在事实上收窄到「只覆盖已有 skill 改 description」, 而没有任何 SC 能拦到这个回退 —— 与同一句里其余边界短语「转录时漏掉任一处本条转红」的机械核验标准 (SC-12 自身注明的设计目的) 不一致。

## 观察

- **T2b「手册 §场景 4b 引用两个工具的新路径」核对无误**: 初读像是「4 个工具只提 2 个」的遗漏, 实读 D2/D3 后确认准确 —— D3 行 3 引用 `claude-shim.sh` 新路径, D2「逐调用健康检查」引用 `classify_calls.py` 新路径, `fault_matrix.py` 与 `fake-claude` 是开发期自测工具, 手册正文 (面向「跑场景 4b」的使用者) 本不需要引用它们的路径。用词准确, 不构成缺陷, 不必因 Findings 1 的措辞问题连带修改这一句。
- **SC-13 可复现性已独立验证**: 按任务指引在自己的临时目录用绝对路径重跑 `fault_matrix.py --out <绝对路径>`, 24 个用例全部符合、退出码 0、末行「与预期不符 0」, 与基线目录 `fault-matrix/matrix-summary.json` 结论一致。首次尝试传了相对路径 `--out`, 因脚本对子进程用 `cwd=root` 导致相对路径的套件 json 找不到 (`FileNotFoundError`), 这是调用方式问题, 不是脚本缺陷; SC-13 本身没有要求相对路径, 不受影响。
- **待转录三条 (逐调用健康检查/作废/fail 的后果) 自足性**: 模拟「只看手册, 不看本 proposal 或 RESULT.md」的执行者视角通读, 三条术语前后一致 (「逐调用健康检查」「不健康」「void/pass/fail/valid」四词贯穿), 内部引用 (「见前置表第 3 条」「见下」) 都指向同一手册小节内的表或邻近条款, 不含 `OQ-\d`/`D\d`/`T\d`/`SC-\d` 字面。唯一密度较高的一句是「不健康的调用按『触发』『没触发』两种可能都算: … 在两种极端下都不变 … 会变, 结论为 void」: 它没有解释「为什么只取两个极端而不是逐次调用穷举组合」(答案是 trigger_rate 阈值判定对触发次数单调, 已读 `classify_calls.py` 源码确认 `lo`/`hi` 区间法), 单靠这句话重建算法有一次性理解门槛。但该判定不需要执行者重新实现——T2b 把 `classify_calls.py` 逐字节搬进工具目录, 手册这句话只是给人看的说明, 实际判定由脚本给出, 因此密度问题不构成执行风险, 不列入 Findings。
- **RESULT.md v7 §v6: v6a/v6b/`v6a/` 归档目录关系可读**: 开篇「v6a 的全部产物归档在 `v6-per-call-health-opus5/v6a/`, 目录根下是 v6b 的工具与结果」单独读稍松 (`PREREGISTRATION.md` 与 `prereg.lock` 实际留在根目录, 不在 `v6a/` 下, 因为它们是修订说明的共同前提, 不属「产物」); 但文末「原始产物」清单逐条列出「预登记...与修订预登记 (...); v6b 的四个工具文件 (...); `v6a/` (原预登记那一批的工具与全部结果)」, 与实际目录结构 (已用 `ls` 核对) 完全一致, 足以让未参与本 session 的读者重建正确的目录关系。锁定记录核验: `PREREGISTRATION.md` sha1 前 12 位 `8e3d63797bcc`、锁定时间 `2026-09-15T13:09:14Z` 与 `prereg.lock` 完全一致; `PREREGISTRATION-AMENDMENT.md` sha1 `2639940452cb`、锁定时间 `2026-09-15T13:51:34Z` 同样一致。不列入 Findings。
- **交互模式/自主模式/自主运行时 三词形 (R4→R5→R6 延续观察, 本轮未升级)**: v8 在 D1 正文 (第 30 行) 把「自主模式下 description 变动的完整处理」改成了「自主运行时 description 变动的完整处理」, 较 v7 少一处旧词形, 是净改善而非恶化。残留: D4 的 OQ-7 不转录条款 (第 92 行)、D5.6 issue 标题 (第 104 行)、OQ-7 正文 (第 165 行) 仍用「交互模式/自主模式」。但这三处均不在 SC-11 界定的转录目标 (CLAUDE.md/SOT §2 核心句行/SOT §3 边界注/SOT §4.1/SOT §6 第三条/手册 §4a §4b) 之内, 且 D5.6 issue 标题的「自主模式」在 v2.0 Layer 2 语境下自解释, 不会引发外部读者误读。维持 R4–R6 结论: 非阻断, 不必为此专门返工。
- **D5.6 内容扩充后的自足性**: 新的「已知缺口」8 条 (对比 v7 的 6 条) 全部标注「均按 aria-orchestrator 代码核实」, 且新增了「旁注现状 (2026-09-15 按代码核): 这类失败本来就不自动重试, 目标设计里真正缺的是告警与原因传递」——这句是对 R6 major #3/#4 (container_crash 默认自动重试的失实断言) 的直接更正, 且更正后的措辞与 R6 聚合报告「主控复核」段核实的代码行为 (`reconciler.py` 可重试集合不含 `container_crash`; 失败分析默认关闭) 一致, 未见新的事实性错误。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 2 major / 0 minor。本席 R6 的 2 条 major 全部 closed (D5 item 7 已删并入 D5.6; D6+头部重核清单的两处残留均已修复且方式结构性, 不止是补一个名字)。本轮新发现 2 条 major, 均出在 v8 本轮新增的内容上: 1 条是 T2b 搬迁工具文件的动词歧义, 若按字面 (删除源文件) 执行会同时打断 SC-2 第 3 行与 SC-13 自身的比对机制 (已用 `test -e` 实测当前证据路径存在, 确认这是真实的破坏面而非假设); 1 条是 OQ-9 新增的「(含新增 skill)」表述缺少对应机械核验, 与同一句其余边界短语「漏掉任一处即转红」的既定标准不一致。两条均满足「不改会让某条 SC 不可执行 / 让规则执行者做错事」的 major 门槛, 且均可用局部文字修补解决 (T2b 加「(复制, 不删除原件)」类澄清; SC-12 补一个短语)。

## Vote

REVISE

## 术语与关系对照表

| 术语/概念 | proposal.md v8 | RESULT.md v7 (基线) | SOT/CLAUDE.md/手册 (拟改文本现状) | 一致性 |
|---|---|---|---|---|
| D5 item 7 / 「三张 vs 四张」issue 计数 | item 7 已删除, 内容并入 D5.6 (现第 6 项) 已知缺口第 (2) 条; 头部/Key Deliverables/T6/SC-6 四处「三张」现与列表项数一致 | 不涉及 | 不涉及 (D5.6 issue 正文已吸收) | 一致, R6 finding 1 closed |
| RESULT.md 版本引用 + 重核机制 | 头部改为「每一处引用 RESULT 的位置, 以 `grep -n RESULT` 逐处列出」(机制性, 非枚举); D6 引号文本已删版本号, 版本号+SHA 补写指令移到 T5 并标「不转录」 | 文件头自述「本文件版本: 7」 | SOT §6 (待 T5 写入) | 一致, R6 finding 2 closed |
| 同批参照臂 → 逐调用健康检查 | D2「同批参照臂」整段替换为「逐调用健康检查」; D3 行 5 同步改写引用新证据路径 | 新增 §v6 (v6a 原预登记暴露规则太严 → v6b 修订预登记全部重跑), 结论段说明替换理由 | 待 T2 转录 (手册尚无 §场景 4b, 现状仍是 R6 之前的「参照臂」空缺) | proposal 与 RESULT 互相引用一致, 是 R6 major #2 的重新设计, 本轮独立验证 (自跑 `fault_matrix.py`) 结论成立 |
| T2b/T4 的「搬」语义 (复制 vs 移动) | T2b「原样搬到」(4 个工具文件); T4「搬入」(套件 json) 两处均无「保留原件」的显式说明 | 不涉及 (工具/套件文件不是 RESULT.md 内容, 但 RESULT.md 本身反复强调 `ab-results/` 是历史存档) | 不涉及 | **有歧义, 见 Findings 1**; T4/SC-4 是先例 (同构问题已存在数轮未被点名), T2b 是本轮新增的第二例, 建议一次性澄清两处 |
| OQ-9「含新增 skill」 | D1 SOT 句 + D2 手册句均已写入「含新增 skill」/「新增 skill 的首个 description 同样要过本场景」; OQ-9 正文给出裸推荐「算」 | 不涉及 | 待转录; SC-12 未覆盖该短语, 手册句也无对应 SC | **覆盖缺口, 见 Findings 2** |
| 交互模式/自主模式/自主运行时 | D1 正文本轮改用「自主运行时」(较 v7 少一处旧词形); D4/D5.6 标题/OQ-7 仍用旧词形 (第 92/104/165 行) | 不涉及 | 转录目标句 (第 40/41 行) 全部统一「自主运行时」 | 转录目标内部一致; 说明性文字词形未完全统一但较 v7 略有改善, 非阻断 (R4→R5→R6→R7 连续观察) |
| PREREGISTRATION.md / PREREGISTRATION-AMENDMENT.md 锁定记录 | proposal rule6_note 段引用两份锁定文件及其修订理由 | RESULT.md §v6a/§v6b 小节头部引用 sha1 前 12 位与锁定时间 | 不涉及 | 一致, 已用 `sha1sum` 与 `prereg*.lock` 内容逐字核对, 数字与时间戳均吻合 |
