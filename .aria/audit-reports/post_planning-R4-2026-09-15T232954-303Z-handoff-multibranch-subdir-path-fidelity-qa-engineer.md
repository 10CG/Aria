---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T00:05:48.457Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 — qa-engineer 席位报告 (10CG/Aria#195, v4 `edd256d`)

## 审计结论

### 实读范围

- `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` (v4, 全文)
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml` (v4, 全文 896 行, 分两次读完)
- `openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py` (v4, 全文 406 行)
- `.aria/audit-reports/post_planning-R3-2026-09-15T212707-499Z-handoff-multibranch-subdir-path-fidelity-aggregated.md` (全文)
- `git diff 2b9cb3e edd256d -- openspec/changes/handoff-multibranch-subdir-path-fidelity/` (650 行, 分三次读完)
- `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` 的 `_dedupe_sort_key` 实读 (确认 docstring/注释真实结构)
- `aria/skills/state-scanner/scripts/writers/latest_md_writer.py` 的 `write_latest_md` 实读 (确认 docstring 真实结构)
- `aria/skills/state-scanner/references/state-snapshot-schema.md` 中 `compound key` 行实读
- `/home/dev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/aggregate_benchmark.py` 与 `SKILL.md` / `references/schemas.md` / `eval-viewer/viewer.html` (独立核验 AB delta 符号 bug 与 `new_skill`/`old_skill` 命名是否官方支持, 不采信 R3 转述)
- 未读: proposal.md 设计取舍本身 (按指示不审); R3 五份席位单席报告 (未要求, 只读聚合报告); 其他席位本轮 R4 报告 (约束禁止)

### 实跑命令与关键输出

1. `TMPDIR=<scratchpad>/tmphome python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py`
   → `EXIT:0`; stdout 18 态 x 19 谓词矩阵与 yaml `metadata.sc11_predicate_validation` 实测块逐字节一致; stderr `verdict: OK (mismatch cells 0, stderr notes 0; 18 states x 19 predicates)`。
2. `python3 -B ... --emit-json`, 取 `predicates` 字段, 与 yaml `metadata.sc11_baseline_predicates` 中 `(label)` 开头的 19 行逐字节比对 → **完全一致**(唯一差异是我自己抽取脚本多打的一个空行, 非内容差异)。这证实 m11 处置 (`--emit-json` 加 `predicates` 字段供机械核验两份谓词原文) 已经在当前状态下可满足。
3. 自建对抗脚本 (不复用官方 STATES, 直接调用脚本内 `rep()` / `build_target()` / `PRED`, 对真实源文件精确取字节锚点) 构造 5 个新坏态, 证实 (j1)(j2)(j3)(l1) 仍可被骗过 —— 见下方 finding 1/2, 命令与输出见该 finding 内联。
4. 读取 `skill-creator` 插件的 `aggregate_benchmark.py:86,101,183,207-209` 与 `SKILL.md:180-186`、`references/schemas.md:297`、`eval-viewer/viewer.html:716,719`, 独立复核 R3 tech-lead 关于聚合脚本 delta 符号的结论与 v4 的修复写法 —— 见「核对无误的部分」第 4 条。

### R3 处置落地核验

我按 R3 聚合报告的 9 个 Major 簇 + 与本席相关的若干 Minor, 逐条对照 `git diff 2b9cb3e edd256d` 核实是否落地。全部结论均基于实读 diff 的具体增删行, 未采信 R3 报告自身的措辞。

| 簇 | R3 处置摘要 | 落地 | 证据 (v4 文件:定位) |
|---|---|---|---|
| PP3-M1 (勾选无提交点) | 27 行 checkbox 合并到 TASK-032 归档预演前一次勾选 | 是 | tasks.md 清单第 15 条改写; yaml TASK-028 verification 末句改「勾选动作在 TASK-032」; TASK-032 新增「tasks.md 勾选 (一次性...)」整段 |
| PP3-M2 (TASK-029 占位检查对 master 工作树恒真) | 干净断言前移到 checkout 之前; 占位检查改查 feature 分支提交内容 | 是 | yaml TASK-029 第 2 步改为「前置断言 (两个子模块仍在各自 feature 分支上做, 早于任何 checkout)」+ `git -C standards show <feature 分支>:...  \| grep -c '#<'`; 旧「第 4 步」grep 工作树的写法已删除 |
| PP3-M3 (取号被占后合并冲突无分支) | 第 4/5/6 步 fail-closed 停下上报, 第 5 步显式 `merge --abort` | 是 | yaml TASK-029 第 4 步「停下上报, 不自行改号重走」; 第 5 步「退出码非 0 (冲突) ⇒ `git merge --abort`, 断言 HEAD 等于第 3 步记下的 SHA...不在 master 上解冲突」; 第 6 步追加 CHANGELOG 计数不减断言 |
| PP3-M4 (`--follow-tags` 半推留孤儿 tag) | 每远端一条 `--atomic`, 禁 `--follow-tags`, 被拒不 force | 是 | yaml TASK-034「推送写法写死...`git push --atomic`...禁用 `--follow-tags`」+「任一远端被拒...原样记台账并上报」 |
| PP3-M5 (delta 符号相反, WITHOUT_BETTER 无来源) | delta 写死 mean(with)−mean(old); 删 WITHOUT_BETTER | 是 (并独立复核, 见下) | yaml TASK-026 / rule6_note / owner_gates / tasks.md 5.5 四处一致删除 WITHOUT_BETTER 并写死取法 |
| PP3-M6 (清单漏列 v3/v3.1 判断) | 补第 19-21 条(旧判断)+ 22-26 条(R4 新判断) | 是 | tasks.md 清单第 19-26 条, 内容与 R3 处置表逐条对应(部分通过改写已有第 15/18 条而非新增序号落地, 但内容完整, 未见遗漏) |
| PP3-M7 ((j1)(j2)(j3) 只判「出现 rel_path」) | 换成钉「现状键元组」的 j1x/j2x/j3x, 新增 `bad_tuples_stale_para` / `bad_j2_tuple_stale_para` 两态 | **官方给出的构造态是** (即 R3 code-reviewer 自建的那两个坏态确实按预期变红), **但存在同类未覆盖的坏态**, 见 finding 1 | yaml/脚本内 `j1`/`j2`/`j3` 谓词与 `bad_tuples_stale_para` 等态; 本席自建对抗态见 finding 1 |
| PP3-M8 (补丁 1 表现形态未写明) | 保留「不窄化」, 在 TASK-035 与清单 18 条补现表现形态说明 | 是 | yaml TASK-035 补丁 1 两条 bullet; tasks.md 清单第 18 条「v4 补」段; 清单第 24 条 conflicted 裁决三处相互一致 (见「核对无误」第 3 条) |
| PP3-M9 (deliverables 未列台账) | TASK-019/020/027/030 补台账 deliverable; TASK-016/017 补标题注释 | 是 (并对全部 35 个 TASK 做了程序化核验, 见「核对无误」第 1 条) | 见下方核对无误第 1 条 |

相关 Minor 逐条核对 (均确认落地, 未逐条列证据以免报告过长): m1 (owner_gates 未获授权处置补全 + 两类协调 ref 推送口径统一)、m3 (TASK-035 补丁 3 措辞 + 读前必看 11 条 3.1-3.5)、m4 (TASK-032 服务端合并后本地对齐)、m5 (TASK-031 merge 不 rebase/不 squash)、m6 (TASK-027 提交点 `--stat` 断言)、m7 (l1x 两处只取「标题到第一个空行」, 新增 `bad_l1_module_scenarios`/`bad_l1_neverraises`)、m8 (authoring_rules 补 a2 三个新锚点)、m9 (j4 正则加左边界, 新增 `alt_j4_numeric`)、m10 (docstring 状态自检改行首匹配; 缺文件 rc 从 1 改 2)、m11 (`--emit-json` 加 `predicates` 字段, 已实测确认可用)、m12 (TASK-003 补 SC-8 后半取行方式)、m13 (TASK-001 补检出断言)、m14 (unittest 命令补 cwd; check_bare_issue_refs 补 `--repo-root`)、m15 (TASK-011 补删除失去消费者的调用)、m16 (writer `:140`/`:159` 两处同步)、m17 (读前必看 14 条 (h) 归属与 SC 映射表行) —— 全部在 diff 中找到对应增删, 未发现遗漏或走样。

**结论: R3 的 9 Major + 17 Minor + 2 conflicted 裁决, 在 v4 中逐条可核实落地, 无遗漏、无走样、无新的跨簇矛盾。** 但 PP3-M7 针对的缺陷类别("文本邻近性检查 ≠ 结构正确性检查")本身只是被**缩窄**而非**消除**, 本席自建的对抗构造证明同类坏态仍能骗过谓词 —— 详见下方 finding。

### 实施者试派生

只看任务本身与其引用文件, 不看审计报告叙事, 判断能否无歧义执行。

| TASK | 判断 | 说明 / 卡点 |
|---|---|---|
| TASK-014 (排序键第 5 级) | **可无歧义执行** | 实现字面、返回类型注解、语义 (`max()` 下 `(True,…)` 胜 `(False,…)`) 全部逐字给出; 用 Python 元组比较规则验证过语义自洽 (`True==1 > False==0`); 缺 `rel_path` 键的兜底行为也写明。无卡点 |
| TASK-018 (SC-15/18/9/16/2 反事实四条+) | **基本可执行, 1 个 Minor 卡点** | 前 3 条补丁 (去守卫 / 判据换 `"/" in filename` / 缺键兜底写反) 是字面代码变更, 可直接执行; 第 4 条「在 `write_latest_md` 内重算谓词并写反」只给出行为意图 (要让布局 1(i)/布局 3(j) 红、布局 2(d) 仍绿), 没有给出具体代码形状, 需要实现者先写一版再跑三步法核对红绿模式是否吻合, 有一轮试错空间。不阻断执行(有可判定的终态), 但不是「读完就能落笔」 |
| TASK-026 (Rule #6 AB) | **可执行, 但有一条已被计划自己承认的执行期不确定性** | `/skill-creator` 的 with/old 两臂如何强制指向不同的 `scan.py` 绝对路径, 计划已预见 `CLAUDE_PLUGIN_ROOT` 解析陷阱并给出应对(两臂提示写绝对路径 + transcript 核对实际路径 + 「跑到同一份代码⇒作废」兜底), 这是合理的风险化解而非缺口。delta 符号与 `new_skill`/`old_skill` 命名做法经本席独立到 skill-creator 源码核实无误(见核对无误第 4 条), 比 R3 更进一步确认了这不只是「转述可信」而是「真的对」。其余 owner 门 (5 处) 均有明确的未授权处置 |
| TASK-029 (子模块合并 8 步) | **可无歧义执行** | 8 步顺序、每步前置、每步失败分支、回退前置 (`HEAD^1`/`HEAD^2` 存在性判断, 覆盖「合并冲突时根本没有合并提交」这个边界) 全部写明; 与 R3 tech-lead/code-reviewer 的真实临时仓四态实验结论一致。未发现卡点 |
| TASK-035 (proposal SC 表反事实 7 条) | **可无歧义执行** | 六个补丁逐条给出改哪个组件、供哪个 SC、所指断言是什么; 补丁 1 的「现表现形态」说明消解了 R3 PP3-M8 指出的字面矛盾, 且与 tasks.md 清单第 18/24 条三处互相一致 (见核对无误第 3 条)。补丁 3/5 明确「不得复用其他任务的副本」, 避免并行任务互相踩踏。未发现卡点 |

### Findings

**[Major] type=issue · category=testing · scope=`sc11-predicate-validation.py` 谓词 (j1)(j2)(j3) 与 `detailed-tasks.yaml` `metadata.sc11_baseline_predicates`/`authoring_rules` (j1)(j2)(j3) · v4 引入: 部分**

R3 PP3-M7 的处置把 (j1)(j2)(j3) 从「整个 docstring/整份文件出现 `rel_path` 子串即算」收窄为「必须在 `(parse_ok` 所在的**首段/同一行/同一块**内出现 `rel_path`」, 并用 `bad_tuples_stale_para`(另起一段) 证明了旧写法的漏洞已堵住。但这个收窄只堵死了「另起一段/另起一行」这一种绕过方式, 没有堵死「**就在同一段/同一行内、紧跟在元组字面后面追加一句提及 rel_path, 但元组字面本身仍是旧元素数**」这种同类绕过 —— 这恰好是 authoring_rules 明文要求的反面(「现状键元组写全五元」要求的是元组字面本身, 谓词判的却是「该段/该行内某处出现子串 rel_path」)。

证据(本席不借用 R3 已构造的坏态, 自建三个新坏态, 用脚本内真实 `rep()`/`build_target()`/`PRED` 在真实源文件字节上验证):

```
$ python3 -B /tmp/.../adversarial_test2.py
A_j1_trailing_sameparagraph: PASS   # 应为 FAIL
B_j2_trailing_sameline:      PASS   # 应为 FAIL
C_j3_trailing_sameline:      PASS   # 应为 FAIL
```

- **(j1)**: 在 `_dedupe_sort_key` docstring 首段句号后原地追加 `"The 5th\n    level compares \`\`rel_path\`\` when the first four tie."`, 元组字面保持 `` ``(parse_ok, updated_at, filename, branch)`` `` (仍四元) 不动。(j1) 谓词取 `docstring.split("\n\n")[0]` 后 `find('(parse_ok')` 再判 `'rel_path' in p[i:]` —— 追加句仍在同一段(未插入空行), 位置又在 `(parse_ok` 之后, 于是 PASS。
- **(j2)**: 在 schema「the **four-level** compound key `` `(parse_ok, parsed updated_at, filename, branch)` `` wins:」这一行, 只把 `four-level`→`five-level`, 并在同一行末尾追加 `` (5th level: `rel_path`) ``, 反引号内元组字面不变。(j2) 谓词按行过滤含 `compound key` 且含 `(parse_ok` 的行, 再判该行 `(parse_ok` 之后是否含 `rel_path` —— 同一行内的追加文字满足此判据, PASS。
- **(j3)**: 在 collector 注释块 `# \`\`(parse_ok, parsed_updated_at, filename, branch)\`\`.` 这一行末尾原地追加 `, plus rel_path 5th.`, 元组字面不变。(j3) 谓词提取 `# Tie-break` 到第一个纯 `#` 行之间的文本块, 判块内 `(parse_ok` 之后是否含 `rel_path` —— 同样满足, PASS。

**照计划执行会出的错**: 一个实现者如果只在紧邻元组字面之后补一句「第 5 级见 rel_path」而没有真的把反引号内的元组改成五元(即字面仍是旧的 4 元描述), TASK-019/TASK-020 会误判为「已完成」, TASK-021「SC-11 全部谓词为真」与 TASK-029 第 7 步「合并树回归」两道后续闸门都不会拦下它, 最终这份**元组字面本身仍描述旧键**的文档会随 Phase C 一起合入 master 打 tag —— 与 Rule #3(文档与代码必须同步更新)的意图相反, 而这恰恰是 SC-11 这套机制本应捕捉的那类缺陷。

**建议改法**: 不再用「子串在某文本区间内出现」判定, 改判**元组字面本身的逗号分隔元素数**——例如从 `(parse_ok` 到匹配的右括号(或到反引号/句末)之间用正则或简单括号计数取出字面串, 断言其内**恰好**含 5 个逗号分隔的成分且最后一个成分含 `rel_path`。这是结构检查而非邻近检查, 能一次性堵死这整个缺陷类(同段/同行/跨段的所有变体), 而不必每轮再枚举一个新的绕过位置。

---

**[Major] type=issue · category=testing · scope=`sc11-predicate-validation.py` 谓词 (l1) 的 `Scenarios:` 判据部分 与 `detailed-tasks.yaml` `metadata.sc11_baseline_predicates` (l1) · v4 引入: 否 (v3 已有, v4 未修)**

(l1) 谓词由三个条件组成: 模块 docstring「Return dict schema:」块含 `degraded_reason`、`write_latest_md` docstring「Returns:」块含 `degraded_reason`、`Scenarios:` 之后含 `degraded_reason` 或 `target_in_subdir`。v4 把前两个条件都收窄到 `blk(s,h) = s.partition(h)[2].split("\n\n")[0]`(标题到第一个空行的块), 但**第三个条件(`Scenarios:` 部分)没有做同样的收窄** —— 它是 `d.partition('Scenarios:')[2]` 的**整个剩余 docstring**, 没有 block 上限。

证据:

```
$ python3 -B /tmp/.../adversarial_test3.py
D_l1_trailing_decoy_after_scenarios: PASS   # 应为 FAIL
```

构造: 跳过官方 `l1s` 编辑(即真的**不**在 Scenarios 列表里插入第四种结局「active count == 1, file in a subdirectory → ...」这一行), 只在 Scenarios 列表**之后、docstring 结尾之前**追加一句无关旁白 `"See the module docstring for background on target_in_subdir handling."`。由于 `scen` 变量扫描整个剩余 docstring 而非仅 Scenarios 块本身, 这句旁白就让第三个条件为真, (l1) 整体判 PASS —— 尽管 Scenarios 列表本身压根没有第四种结局这一行, 这正是 `bad_scenarios_missing` 这个官方坏态原本想抓的那类缺陷的一个未覆盖变体。

**照计划执行会出的错**: 与上一条同源 —— `write_latest_md` docstring 的 Scenarios 列表如果漏掉第四种结局, 只要在文档别处顺带提一句 `target_in_subdir`(很自然的写法, 比如在改动说明或交叉引用里), (l1) 就不会拦下来, TASK-013/TASK-021/TASK-029 三道闸门都会误判通过。

**建议改法**: 把 `scen` 也用类似 `blk()` 的方式限定范围(例如限定到 Scenarios 块本身、即到下一个顶格标题或 docstring 结尾中较近者, 而不是任意剩余文本), 或者直接要求 Scenarios 块内**新增一行**且该行含 `target_in_subdir`(比「块内某处含子串」更贴近「新增了第四种结局」这个意图)。

---

**[Minor] type=issue · category=documentation · scope=TASK-018 补丁 4 的措辞**

「在 `write_latest_md` 内重算谓词并写反」是行为意图描述, 不是可直接落笔的代码变更(不同于本文件其余反事实补丁基本都给出具体改哪一行/改成什么)。执行者需要先写一版实现, 用三步法验证是否落在「布局 1(i) 与布局 3(j) 红而布局 2(d) 仍绿」这个目标红绿模式上, 有一次试错空间。不阻断执行(终态可判定、可收敛), 建议在 notes 里补一句最小实现提示(例如「在 `n_active == 1` 分支内部另行计算 `rel == filename` 并对 `_render_pointer` 返回的 `reason` 做布尔取反」), 减少来回。

---

**[Minor] type=issue · category=testing · scope=TASK-026 「两臂跑到同一份代码 ⇒ 该 run 作废」**

该 verification 条目只写了判定条件与「作废」的结论, 没写「作废后如何补」(重新起一次该 eval? 还是整批 AB 重跑?)。鉴于同一条目已经花了大量篇幅写清楚「逐 eval 判回归」的复跑规则(该 eval 复跑两次), 此处可以同样补一句「补跑该 eval 一次, 并入止损判据前的样本」, 消除执行时的临场判断空间。

### 核对无误的部分

1. **PP3-M9 全量核验(不止抽查)**: 用脚本解析 `detailed-tasks.yaml` 全部 35 个 TASK, 程序化断言「verification 提到记台账 ⇒ deliverables 含 `verification-ledger.md`」, 结果 0 处例外。这比逐条抽查更强 —— 确认 PP3-M9 是**全量**落地而不只是 R3 点名的那 4 个 TASK。
2. **验证脚本自检**: `sc11-predicate-validation.py` 无参数实跑退出码 0, 18 态 x 19 谓词与 yaml 实测块逐字节一致; `--emit-json` 的 `predicates` 字段与 yaml `metadata.sc11_baseline_predicates` 的 19 行 `(label)` 内容逐字节一致(m11 处置已可用, 非只是「计划要做」)。
3. **TASK-035 补丁 1 口径三处一致**: tasks.md 清单第 18 条(v4 补段)、清单第 24 条(conflicted 裁决)、yaml TASK-035 补丁 1 两条 bullet, 三处对「该行变 legacy」现表现为「该行不在 tracks[] + kind 出现 + unreadable_count==1」的说法逐字一致, 未发现三处描述互相矛盾。
4. **AB delta 符号 bug 独立复核(不采信 R3 转述)**: 直接读 skill-creator 插件真实源码 `aggregate_benchmark.py:101,183,207-209`(`configs = list(results.keys())`, 插入顺序来自 `sorted(eval_dir.iterdir())` 的目录名字母序), 确认 `with_skill`/`old_skill` 命名下 `'o' < 'w'` 会导致 `configs[0]` 是 `old_skill`、`delta = old − with`(符号相反); 改用 `new_skill`/`old_skill`(`'n' < 'o'`)确实能让 `configs[0]` 变成 with 臂。另外在 `eval-viewer/viewer.html:716,719` 发现 `new_skill`/`old_skill` 是查看器**官方已支持**的命名(与 `with_skill`/`without_skill` 并列识别, 且 `old_skill` 被正确当作 baseline), 说明 v4 选的绕过命名法不是本 Spec 自造的 hack, 是插件自身已支持的路径, 风险比单纯「读代码猜测可行」更低。
5. **TASK-014(排序键第 5 级)实现字面自洽**: `(rel == filename, rel)` 配合 `max()` 的语义(`True>False`)已用 Python 布尔比较规则验证, 与「顶层行优先」的自然语言描述一致。
6. **TASK-029 8 步回退前置**: 第 6 步回退命令前置显式检查 `HEAD^1`/`HEAD^2`, 并明确「第 5 步冲突中止时根本没有合并提交, 此时不执行回退直接停下上报」—— 覆盖了 R2 阶段曾经缺失的这个边界情形。
7. **SC 映射表 (tasks.md) 与 detailed-tasks.yaml 抽样一致性**: 抽查 SC-6 / SC-11 两行, parent 编号(2.2/2.5/4.1/4.2/4.4/5.1/5.3/5.4 等)与对应 TASK 的 `parent` 字段、verification 内容逐一对应, 未发现漂移。
8. **j4 正则左边界与 `alt_j4_numeric` 守卫态**: 实跑矩阵确认「14-level」(讲目录深度)不触发 (j4) 误判, 且未影响其余 18 个谓词。

## Verdict

PASS_WITH_WARNINGS — 0 Critical, 2 Major(均为本席新构造发现、非 R1-R3 已列), 2 Minor。R3 的全部处置(9 Major + 17 Minor + 2 conflicted)经逐条核验确认落地, 无遗漏、无走样、无新引入的跨簇矛盾。本轮的 2 个 Major 属于同一缺陷类的「未被此前几轮枚举到的兄弟情形」(memory `fix-the-class`): R1→R3 把 (j1)(j2)(j3)(l1) 从「整份文件/整个 docstring 出现子串」逐步收窄到「限定文本区间内出现子串」, 但「限定区间内**紧邻元组字面之后追加一句提及**」与「Scenarios 部分未做区间上限」这两个具体形状此前四轮都没人构造过。

## Vote

REVISE — 存在 Major 级别、已用真实源文件实证复现的判据被骗过证据, 建议执笔人在 R5(如继续)按「建议改法」把 (j1)(j2)(j3) 改成结构性(元组元素计数)检查、把 (l1) 的 Scenarios 部分同样加 block 上限, 而不是再枚举一个新坏态贴上去。

## 边际判断

本 Spec 的验收体系(19 条定位谓词 + 18 态矩阵 + 三步法反事实 + AB)相对它保护的改动(aria 4 个代码文件 + 少量文档面, 规模上是一次中等大小的字段新增/语义收紧), 在**广度**上已经过度, 在**深度**的一小部分上仍然不足 —— 这两件事同时成立并不矛盾:

**已经过度、可以收掉而不明显损失鉴别力的部分**:
1. **三步法反事实被均匀套用到约 20 条 SC 上**, 不分难度。像 SC-14(早退 dict 补一个 `unreadable_count: 0`)这种单字段存在性检查, 一条直接索引断言 + 代码审查的鉴别力并不明显弱于「建 worktree → 打补丁 → 记 SHA → 删 worktree」的完整仪式; 完整仪式该留给真正容易被「看似对但差一点」的坏实现蒙混的地方(排序键比较逻辑、legacy id 拼接、TASK-035 反复讨论的「首个失败断言是否命中所指断言」这类)。本轮的两个 finding 恰好证明: 把有限的审计精力花在给**已经很难被攻破的**三步法反事实再加仪式感, 边际产出远低于花在给**明显还能被攻破的**文本邻近谓词上。
2. **SC-11 谓词系统本身连续 4 轮加固**(R1 引入 → R2/R3/本轮各发现新绕过), 且每轮修复都是「针对上一轮具体构造的坏态打补丁」而非「改变检查的结构类型」。这是一个会持续产生新一轮 Major 的模式(19 个谓词里, 光 (j1)(j2)(j3)(l1) 4 个就已经改了 3 版), 除非把检查方式从「子串邻近」换成「结构解析」(如本报告建议), 否则下一轮大概率还能再构造出第 3 种绕过位置。**这不是"该不该继续测"的问题, 是"用什么类型的检查"的问题** —— 继续加状态/加谓词是在同一个天花板下反复加固, 换成结构检查是换天花板。
3. **Rule #6 AB 在本 Spec 里预先自证无效**(rule6_note 明写「已预判套件结构上测不到 collector 输出变化, 预期 delta ≈ 0」), 却仍要求完整走完协调 ref 安全三步、PREDICTION/RESULT 两份文档、逐 eval 回归判定、owner 裁决点等全套仪式。这是 Rule #6 这条不可协商规则本身的成本, 不是本 Spec 的裁量空间(按 Rule #10 不该自我豁免), 但作为观察值得指出: 如果多个 Spec 都遇到「套件结构性测不到」却仍要求全套仪式, 这可能是 Rule #6 判据表本身(而非某个 Spec 的执行)该由 owner 复议是否需要一条「预判无效度时的简化仪式」分支, 而不是每个 Spec 各自在 rule6_note 里重复写一遍「预期无效」再照样全套跑一遍。
4. **post_planning 本身的 4 轮审计**: R3 报告自己的数学已经触发 `stop-adding-rounds`(Major 数 13→9→9 持平)与 `marginal-return-negative`(每轮新增 Major 中 >1/2 由上一轮改写引入)两条记忆判据。本席这一轮的 2 个 finding 客观上**延续**了这个模式(又是新一轮改写引入的新表面, 尽管是通过更彻底的独立对抗构造而非阅读发现) —— 但这恰恰是这两条记忆判据想说的: 审计"广度"(轮数)的边际回报已经很低, 而这一轮真正有产出的是"深度"(自建副本实跑、不信任前序结论)而非"再来一轮通读"。

**仍然不足、不能收的部分**:
1. **三步法反事实对"首个失败断言是否命中所指"这类真正脆弱的地方**(TASK-035 反复处理的问题)是必要的 —— 没有实跑就无法知道断言顺序会不会让反事实证明了错误的东西, 这在 R2 已经被基线 RED 证据的失败具体证明过(post_planning R2 PP2-M9)。
2. **验证脚本的自检机制本身**(EXPECTED 与 STATES 一致性检查、docstring 状态自检、锚点漂移检测)不能省 —— 这是防止验证脚本自己烂掉的最后一道线, 且本身很轻量。
3. **本轮发现的两个 finding 指向的具体检查逻辑**必须修 —— 不是因为"验收体系太大"就可以放过已证实的漏洞, 广度过度和深度不足可以同时是真的。

一句话: 该收的是"审计轮数"与"对简单 SC 也用重型仪式", 不该收(且实际还欠一点)的是"对判据本身的结构性攻击面的检查深度"。
