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
timestamp: 2026-09-17T08:48:36.574Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R8 — code-reviewer 席 (改完之后的复核轮)

被审对象: proposal **v9** @ 主仓 `a563192`; 同批 RESULT.md 升 **v8**。v9 相对 v8 只动四处 (SC-9 两个实质锚点 / SC-12 加「含新增 skill」/ T2b 与 T4 的「搬」改「复制」/ `fault_matrix.py` 非空输出目录报错退出), 本轮只审这四处修得对不对、有没有带出新问题, 不重开 R1–R7 已闭合的题目。

只审不改: 唯一写入仓库的是本报告; 重跑、探针、变异模拟全在 session scratchpad (`r8-code-reviewer/`), 审后 `git status --porcelain` 为空。独立性: 同目录未打开本 spec 的别席 R8 报告。下文数字全部来自实跑, 命令与输出见「实跑记录」。

## R7 对账

范围: 本席 R7 报告 Findings 的 1 条 (critical 0 / major 0 / minor 1)。

| 序号 | R7 条目 | v9 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [minor] `fault_matrix.py` 第 110–111 行对 `--out` 已有目录无条件 `shutil.rmtree`, `--out .` 会删空当前目录 | 第 110–116 行改为: 目录存在且非空 ⇒ 打印「输出目录已存在且非空, 请换一个 `--out`」并 `return 2`; 不存在 ⇒ `mkdir(parents=True)`; `shutil.rmtree` 已从该分支消失 | **closed** | 三个指定探针 + 两次全量重跑全部实测通过 (下表); RESULT v8 已记录这次加固, 归档产物同步重跑 |

合计: **closed 1 / partially 0 / open 0**。

### 指定的三件实测 (全部自己跑)

| 探针 | 期望 | 实测 | 结论 |
|---|---|---|---|
| `--out` 指向非空目录 | 报错退出、退出码 2、目录内容不变 | rc **2**; stderr 正是该提示; stdout 空; 目录内容 md5 指纹 before = after (`cfff947b…`), 含子目录里的文件 | 符合 |
| `--out` 指向不存在的目录 | 正常新建并跑完 | rc **0**, 目录被新建, 末行「用例 24, 与预期不符 0」 | 符合 |
| 缺省不传 `--out` | 用临时目录 | rc **0**, `tempfile.mkdtemp` 新建 `trigger-eval-fault-matrix-ysgmu_4_` (78 个条目), 末行「与预期不符 0」 | 符合 |

补测两个边界: (1) 在一个有文件的工作目录里 `--out .` (R7 minor 的原始危险形态) ⇒ rc 2, `important.txt` 原样还在, 危险已根除; (2) `--out` 指向已存在的**空**目录 ⇒ 正常跑完 rc 0 (加固没有误伤合法用法)。

### 自己重跑矩阵与反事实

- **故障矩阵** (加固后脚本, 不调用 API): **24 个用例、与预期不符 0、退出码 0**; 逐行结论与归档 `fault-matrix/matrix-summary.json` 一致 —— 我的重跑产物与归档版**逐字节相同**。
- **反事实** (临时副本里删掉 `classify_calls.py` 对报错结果帧的判定两行): **24 个用例、与预期不符 5、退出码 1**; 5 个用例名 = `F1_result_error`、`S1_overbroad_fault_in_shouldnot_half`、`S2_correct_fault_on_one_should_query`、`S8_two_run_fault_should`、`S10_negctrl_two_run_fault_x6`, 与 SC-13 与 RESULT 所写**逐一相同**; 我的反事实产物与归档 `fault-matrix-counterfactual/matrix-summary.json` 也逐字节相同。
- **RESULT v8 那句「归档在 `fault-matrix/` 与 `fault-matrix-counterfactual/` 的就是加固后重跑的产物」属实**: 两个目录的 mtime 均为 09-17 08:30; `fault-matrix/` 下 22 个 `*.classify.json` 确有改动, 逐字段比对后差异**只有** `duration_s` 与 `file` (垫片按时间戳命名的日志文件名) 两个字段, `summary` 与 `queries` 全部 22 个文件逐一相同、`verdict` 全部一致 ⇒ 是真重跑而非改数; `matrix-summary.json` 两份未进 diff 是因为它对重跑确定性 (我独立重跑得到逐字节相同的文件), 不是没跑。
- **加固没有污染预登记**: `prereg.lock` / `prereg-amendment.lock` 记录的 sha1 与两份预登记正文实算值仍逐位吻合 (`8e3d63797bcc…` / `2639940452cb…`)。

## Findings

- [major] testing/proposal.md §SC-9 (`classify_calls.py` 锚) (issue): v9 把 v8 的「含 `classify_calls.py` 的行 ≥ 1」换成「含 `classify_calls.py` 的**那一行**同时含「两种可能」」, 丢掉了存在性断言。整条「逐调用健康检查」bullet 被漏写时, 该子句在空集上真空成立, SC-9 六项全绿 (已实测)。修法: 写成「含 `classify_calls.py` 的行 ≥ 1, 且该行同时含「两种可能」」。

## 观察 (不进收敛比较键, 不影响 vote)

1. **SC-9 的作废锚这一半修得很扎实**: 我用三种攻击各做一次变异, 全部转红 —— (1) 把括号里的实质判定悄悄改回「即存在任一次不健康的调用」(R7 qa 席的原攻击) ⇒ 缺「足以改变判定」转红; (2) 从作废行整项删掉「任一臂逐调用健康检查不通过 (…)」⇒ 缺两串转红; (3) 只删括号内的实质判定、保留标签词 (最隐蔽的一种) ⇒ 同样转红。且作废行本身有「同时含「作废」与「不得 ship」的行 ≥ 1」兜底存在性, 不存在 Findings 那条的真空问题 —— 两个锚只有一半有兜底, 是这次的不对称之处。
2. **SC-12 修对了**: SOT 新句六串齐全 (原文绿), 删掉「(含新增 skill)」即转红 (实测)。但 R7 major 3 的**另一半**仍在: 手册侧对应句「新增 skill 的首个 description 同样要过本场景」依旧没有任何 SC 兜底。owner 2026-09-17 的裁定原文只点名「SC-12 加「含新增 skill」」, 这半条未被点名 ⇒ 它算不算该 major 的 partially, 留给聚合席判, 本席不自行改判。
3. **T2b / T4 改「复制」后前提全部对得上**: D3 前置表第三列 14 条机读实证路径全部 `test -e` 为真 (含第 3 行的 `v6-per-call-health-opus5/claude-shim.sh`); SC-4 的 diff 目标 `trigger-eval-openspec-archive.json` 仍在基线目录根; T2b 目的地 `aria-plugin-benchmarks/tools/trigger-eval/` 尚不存在 (任务未执行, 符合预期)。
4. **SC-13 在新位置可执行 (演练过, 不是推演)**: 把四个文件复制进镜像的 `aria-plugin-benchmarks/tools/trigger-eval/`, `cmp` 四份全部逐字节相同, 不传 `--suite` 直接跑 ⇒ rc 0、末行「与预期不符 0」。`find_suite()` 沿父目录找到 `aria-plugin-benchmarks` 后解析到基线套件, 正是 T4 现在明写要保留的那份 —— 「复制而非搬」这一改同时救了 SC-4 的 diff、SC-2 第 3 行与 `find_suite()` 三处, 改得对。
5. **`--out` 指向一个已存在的普通文件时会抛未捕获异常**: `any(out.iterdir())` 抛 `NotADirectoryError`, 打印 traceback 且退出码 **1**。方向是安全的 (不删任何东西), 但 1 在本脚本里的语义是「有用例不符」, 而这属于「环境不全」应为 2。一行 `out.is_dir()` 判断即可, 不阻塞。
6. **`v6a/fault_matrix.py` 仍带无条件 `shutil.rmtree` (第 92 行)**: 它是修订预登记之前那一批的冻结产物, 不被 T2b 复制、不被 SC-13 比对、手册也不引用, 动它反而破坏 v6a 归档的溯源 ⇒ 建议不动, 但 RESULT v8 的加固说明里点一句「v6a 那份按冻结保留旧行为」会更少歧义。
7. **RESULT 版本引用已全部同步**: proposal 里 `grep -n RESULT` 共 12 处, 带版本号的 6 处 (头部基线数据 / Why / D2 两处 / D3 第 4 行 / Impact / T8) 全部为 v8, 「RESULT v7」「RESULT.md v7」在 proposal 里 0 处。全仓扫一遍, 仍写 RESULT v7 的只有 R7 五席报告 (审计存档, 不应改) 与两份 handoff。
8. **`docs/handoff/latest.md` 的本轨行已陈旧**: a563192 改了 latest.md 但漏了这一行, 它仍写「v8 `15ab323` + RESULT v7; R7 已跑完 …, 待 owner 三选一降级裁定」, 而 owner 已裁定、v9 已落地。这是 Rule #9 的活导航面, 下一个 session 或并发容器读它会拿到过期版本。非阻塞, 建议随本轮结果一并回填。
9. **SC-9 那句「v7 自检实测」指的是 proposal v7, 不是 RESULT v7** (v8 起就有的旧文字)。同一份文档里 v8/v9 既当 proposal 版本号又当 RESULT 版本号, 这一处紧挨着 RESULT 的版本引用, 建议写成「proposal v7 自检实测」消歧。
10. **SC-13 的反事实日期「(2026-09-15 已实跑)」可以顺手更新**: 本轮用加固后的脚本重跑过一次, 结论与 5 个用例名不变; 写成「2026-09-15 首跑, 2026-09-17 加固后复跑结论不变」更贴合 RESULT v8。

## Verdict

**PASS_WITH_WARNINGS** —— critical **0** / major **1** / minor **0** (Findings 口径); 观察 10 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal / RESULT.md / `PREREGISTRATION.md` / `PREREGISTRATION-AMENDMENT.md` 各跑一次: 均「裸 issue 引用: 0」, rc 0 / 0 / 0 / 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊与科普特 U+0370–03FF / 希腊扩展 U+1F00–1FFF) 与 NUL: 上述 4 个文档 + 四个工具文件, 共 8 个文件全部 0 / 0。
  - 本 Spec 自己的 rule6_note: `n/a` / `no` / `n/a` / `n/a` / `n/a`, 五项逐一在 D4 值域内; `description_changed: no` 不触发 D4 的合规条款; v9 未动 aria 子模块 gitlink ⇒ 「aria-plugin 零改动, 本 Spec 自身不触发 Rule #6」仍成立。
  - D1 三条旧句: `CLAUDE.md` / SOT / 手册各 `grep -F` 恰 1 次; 核心句在三个现状文件中各 0 次 (新句尚未落地, 符合 Phase A 状态)。
  - 范围: `15ab323..a563192` 在本 spec 面上只动 proposal、RESULT.md、`fault_matrix.py` 与 22 份重跑归档; 四处改动与 owner 裁定逐条对得上, 无范围外变更。
- **Phase 2 (质量): PASS_WITH_WARNINGS** —— 加固代码本身经五个探针 + 两次全量重跑验证正确且未误伤; 唯一的 major 是 SC-9 修复时丢了一个存在性断言 (见 Findings)。

## Vote

**REVISE** —— 有 1 条 major。它是一句话的事 (把「那一行」改回带 `≥ 1` 的写法), 不需要重跑任何实验、不动任何实验产物; 但因为它与 R7 三条 major 属同一类 (SC 锚不住转录漏写), 且恰恰是这次修复动作自己带出来的, 按 R7 的同一把尺子必须记 major。若聚合席认为「含 X 的**那一行**」在本仓的判读惯例上自带存在性语义 (即空集判红), 则本条降为 minor, 本席无异议。

## 映射表

### v9 四处改动 → 我的验证 → 结论

| # | 改动 | 落点 | 我怎么验的 | 结论 |
|---|---|---|---|---|
| 1 | SC-9 补两个实质锚点 | proposal L151 | 以 D2 判据正文 + D3 前置表为手册代理, 跑原文 + 4 个变异 | 作废锚 **修对** (三种攻击全转红); classify 锚 **有真空缺口** (见 Findings) |
| 2 | SC-12 加「含新增 skill」 | proposal L153 | 取 D1 表第 2 行 SOT 新句, 六串齐全性 + 漏写变异 | **修对** (原文绿, 漏写红); 手册侧那半条仍无 SC (观察 2) |
| 3 | T2b / T4 「搬」改「复制 (原件保留)」 | proposal L133 / L135 | SC-2 的 14 条路径 `test -e`; SC-4 diff 目标存在性; 镜像目录 T2b 演练 + SC-13 全流程 | **修对**, 同时救了 SC-4 / SC-2 第 3 行 / `find_suite()` |
| 4 | `fault_matrix.py` 非空输出目录报错退出 | 基线目录该文件 L110–116 | 五个探针 + 矩阵 24/0 + 反事实 5/rc 1 + 归档一致性 | **修对**, R7 minor closed; 余一个文件形参边界 (观察 5) |

### v9 新增文字里的全称句与事实断言

| 句子 (位置) | 依据 | 结论 |
|---|---|---|
| 「前置表第 3 行的机读实证与 SC-13 的逐字节比对**都要求**它还在」(T2b) | 第 3 行 `v6-per-call-health-opus5/claude-shim.sh` 受 SC-2 `test -e`; SC-13 `cmp` 需基线那份 | 成立 |
| 「SC-4 的 diff **要求**它还在」(T4) | SC-4 diff 目标 = 基线目录 `trigger-eval-openspec-archive.json`, 实测存在 | 成立 |
| 「只删作废条件里的逐调用检查一项, 或把括号里的实质判定悄悄改回…, 本条**都**转红」(SC-9) | 两种变异实测各缺一到两串 ⇒ 红; 另补测「只删括号内实质判定」也红 | 成立 |
| 「三处都是给自主模式划的边界, 转录时漏掉任一处本条**转红**」(SC-12) | 删「(含新增 skill)」实测转红; 另两处是 `grep -cF` = 1 的确定性判据 | 成立 |
| 「24 个用例仍全部符合、反事实仍 5 例转为不符」(RESULT v8) | 本席独立重跑: 24/0 rc 0; 反事实 5/rc 1, 5 个用例名逐一相同 | 成立 |
| 「归档在 `fault-matrix/` 与 `fault-matrix-counterfactual/` 的就是加固后重跑的产物」(RESULT v8) | 两处归档与我的重跑逐字节相同; 22 份 classify 报告差异仅 `duration_s` / `file`, verdict 全同; mtime 09-17 08:30 | 成立 |
| 「`--out` 传错 (例如指到当前目录) 会毁掉整个目录」(代码注释, 陈述旧危险) | 旧版第 110–111 行确为无条件 `rmtree`; 新版 `--out .` 实测 rc 2 且文件留存 | 成立 |
| 「R7 … 0C / 3M / 1m, max_rounds 耗尽未收敛, owner 2026-09-17 裁定增加轮次 (7 → 8) 并先改四条」(Status) | 与 R7 聚合报告及其末尾 owner 裁定逐条对应 | 成立 |

## 实跑记录

1. `--out` 非空目录探针: rc **2**, stderr =「输出目录已存在且非空, 请换一个 `--out`: …」, stdout 0 行; 目录内容指纹 before = after = `cfff947b45fdd7e02503558557e8d33b`(含 `keep.txt` 与 `sub/deep.txt`)。
2. `--out .` 探针 (工作目录内有 `important.txt`): rc **2**, 文件原样留存, 内容未变。
3. `--out` 不存在目录探针: 目录被新建, 24 用例 / 不符 0 / rc **0**。
4. `--out` 已存在空目录探针: 24 用例 / 不符 0 / rc **0** (未误伤)。
5. 缺省不传 `--out` 探针 (`TMPDIR` 指到 scratchpad): rc **0**, 新建 `trigger-eval-fault-matrix-ysgmu_4_`, 78 个条目, 末行「与预期不符 0」。
6. `--out` 指向普通文件探针: `NotADirectoryError` 未捕获, rc **1** (观察 5)。
7. 故障矩阵重跑: `python3 fault_matrix.py --out <scratchpad>/fm` ⇒ 24 用例 / 不符 0 / rc 0; `cmp` 我的 `matrix-summary.json` 与归档版 ⇒ **逐字节相同**。
8. 反事实重跑 (副本删掉 `if errored: reasons.append("result 帧报错")` 两行, 显式 `--suite` 指基线套件): 24 用例 / **不符 5** / rc **1**; 名单 = F1_result_error、S1_overbroad_fault_in_shouldnot_half、S2_correct_fault_on_one_should_query、S8_two_run_fault_should、S10_negctrl_two_run_fault_x6; `cmp` 与归档反事实 `matrix-summary.json` ⇒ 逐字节相同。
9. 归档产物语义比对: `15ab323` vs `a563192` 的 22 份 `*.classify.json`, 逐字段 diff ⇒ 差异字段并集只有 `{duration_s, file}`; `summary` 与 `queries` 全部相同; `verdict` 全部一致。
10. SC-9 变异模拟 (手册代理 = D2 判据正文 + D3 前置表; 代理内含 `classify_calls.py` 的行恰 1 行): 原文两种读法皆绿; 删整条健康检查 bullet ⇒ 严格读法红、真空读法**绿**; 作废括号改回旧语义 ⇒ 两种读法皆红; 作废行删整项 ⇒ 缺「逐调用健康检查不通过」「足以改变判定」⇒ 红; 只删括号内实质判定 ⇒ 缺「足以改变判定」⇒ 红。
11. 删整条 bullet 后其它 SC 的兜底情况: SC-10 参数钉死行仍在 (绿), SC-2 前置表仍六行 (绿), 且前置表第 5 行仍写着「同批负控与逐调用健康检查 (判据见本小节上文)」而判据已不在 ⇒ 无 SC 接得住。
12. SC-12 模拟: SOT 新句六串齐全 ⇒ 绿; 删「(含新增 skill)」⇒ 红 (缺该串)。
13. T2b 演练 + SC-13: 四文件复制进镜像 `aria-plugin-benchmarks/tools/trigger-eval/`, `cmp` 四份全部逐字节相同; 不传 `--suite` 在新位置跑 ⇒ rc 0 / 「与预期不符 0」; `find_suite()` 对新位置解析到基线套件且该文件存在。
14. SC-2 机读实证: D3 第三列 14 条路径全部存在、缺失 0; 第 4 行为唯一 `[配置推导]` 行。
15. Phase 1: `check_bare_issue_refs.py` 四文件 rc 0 / 0 / 0 / 0 (均「裸 issue 引用: 0」); 禁用字形与 NUL 八文件全 0 / 0; D1 三条旧句各 1 次、核心句在三个现状文件各 0 次; rule6_note 五字段取值全在 D4 值域内。
16. 版本引用: proposal `grep -n RESULT` 12 处, 带版本号的 6 处全为 v8, 「RESULT v7」0 处; 全仓仍写 RESULT v7 的只剩 R7 审计存档与两份 handoff (其中 `docs/handoff/latest.md` 本轨行陈旧, 观察 8)。
17. 预登记完整性: `prereg.lock` = `PREREGISTRATION.md sha1=8e3d63797bcc 锁定于 2026-09-15T13:09:14Z`, 实算 `8e3d63797bcc4963…`; `prereg-amendment.lock` = `sha1=2639940452cb 锁定于 2026-09-15T13:51:34Z`, 实算 `2639940452cb6335…` ⇒ 两份均未被本次加固触碰。
18. 环境与卫生: HEAD = `a563192` (2026-09-17); 审计全程 `git status --porcelain` 为空, 仓库文件零改动; 所有重跑与变异副本均在 session scratchpad。
