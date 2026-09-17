---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T01:37:15.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R5 — qa-engineer 席报告 (handoff-multibranch-subdir-path-fidelity, 10CG/Aria#195)

对象: 主仓 master `0e60b08` (本地未推送) 的 `openspec/changes/handoff-multibranch-subdir-path-fidelity/{tasks.md, detailed-tasks.yaml, sc11-predicate-validation.py}` v5。本席为 R5 新派席位, 侧重「验证判据与证据链」。全部命令均在只读前提下于仓内或 `/tmp/claude-1000/.../scratchpad/r5-qa-engineer/` 临时目录实跑, 未修改仓内任何文件、未 git 写操作、未派子代理。

## 审计结论

组 1–4 (24 个任务) 在 R4 已零 Major, 本轮对其中 TASK-014 (排序键算法)、TASK-018 补丁 4 (m14 落地)、TASK-035 六补丁做了独立复核, 未发现新缺陷, 维持零 Major。R4 的 7 个 Major 簇与 16 个 Minor 在 v5 均已落地 (逐项 file:line 证据见下表), 且我独立重跑了 `sc11-predicate-validation.py`(真实 aria 1cb3872 checkout), 24 态 × 19 谓词与 yaml 实测块逐字节一致 (`verdict: OK, mismatch cells 0`), 证实 PP4-M6/M7 的字面修法已生效、跨簇一致性条目 3 成立。

但本席按任务要求「自建对抗构造」, 对 v5 新写的 (j1)(j2)(j3) 平衡括号判据做了独立的、非沿用前几轮坏态的攻击, 发现这三个判据仍可被一个**在括号之内、但语义上明确否认 rel_path 属实**的逗号子句绕过, 且已用真实 Python 解释器对真实 `aria/skills/state-scanner` 文件树验证 (非凭阅读定性)。这是 R2→R3→R4→R5 同一处「换量不换质」缺陷的第 4 次复现, 判为 Major。另有一个同类但风险更低的 (l1) 旁证发现, 判为 Minor。

## R4 处置落地核验

| R4 编号 | 处置摘要 | 落地证据 (v5, file:line) | 状态 |
|---|---|---|---|
| PP4-M1 | TASK-029 第4/6步基准改「台账最近一次记录」+ 重算号后追记 + 清单#22补「三支重走」 | yaml:806(第4步)/:808(第6步) 均用「台账最近一次记录」措辞; tasks.md:60 清单#22(a) | 落地 |
| PP4-M2 | 第3步 ff-only 后复核相等; 第5步两仓视为整体, 任一失败都回退两仓 | yaml:805(第3步二次断言)/:807(第5步"两个子模块视为一个整体") | 落地 (第3步逻辑本席已用真实 git 沙盒复现验证, 见下) |
| PP4-M3 | 删第7步 `--emit-json` 核验, 一致性核验并入 TASK-001 | yaml:810(第7步已不含该核验)/:195-196(TASK-001"两份谓词原文的唯一机械核验点"); tasks.md:65 清单#27 | 落地 |
| PP4-M4 | TASK-031 主仓多远程推送交 C.2.5, 写明三项配置事实 + 断言口径 | yaml:882(TASK-031)/:159(owner_gates 第11项) | 落地 (本席独立核验 SKILL.md + 真实 config + 真实 remote, 见下) |
| PP4-M5 | owner_gates TASK-034 两条补"不进TASK-030"; TASK-030补双remote前置; TASK-031/032补失败分支 | yaml:157-158/:857/:879/:909 | 落地 |
| PP4-M6 | (j1)(j2)(j3) 换量为"只看balanced parens之内" | yaml:94-96, 133; py:312-314; 新坏态 py:291-293/343-345 | **落地, 但本席发现同类新缺口 (见 M-QA1)** |
| PP4-M7 | (l1) 丢标题行余部 + Scenarios 结构化判据 (≥4条结局行含target_in_subdir) | yaml:100; py:318; 新坏态 bad_l1_title_paren py:294/346 | 落地 (见关联 Minor m-QA1) |
| m1–m16 | (逐条见下) | m1:yaml:146-147 · m2:yaml:191 · m3:tasks.md:74 · m4:yaml:192,726 · m5:yaml:738 · m6:yaml:29 · m7:yaml:804 · m8:yaml:793 · m9:yaml:808 · m10:tasks.md:32(读前必看#14) · m11:yaml:97/py:315 (`(^|[^0-9A-Za-z])`) · m12:yaml:347 · m13:yaml:907(已知边界登记)+TASK-009收紧 · m14:yaml:525(补丁4具体三行) · m15:yaml:727 · m16:yaml:512-524/643-665/666-682(注释统一) | 全部落地 |

跨簇一致性条目 3 (「谓词块/脚本 PRED/EXPECTED/矩阵/authoring_rules 一次改齐, 由 --emit-json 重生成」): 本席独立重跑脚本, `verdict: OK (mismatch cells 0, stderr notes 0; 24 states x 19 predicates)`, 与 yaml `metadata.sc11_predicate_validation.measured_2026_09_16_at_1cb3872_v5` 逐字节一致。confirmed。

## 实施者试派生 (≥4 TASK)

1. **TASK-029 第3步 (ff-only 后复核相等)** — 真实 git 沙盒复现 R4 tech-lead 指出的原始漏洞场景 (本地 master 领先于 origin/master 时 `merge --ff-only` 返回 `Already up to date.` 且 exit=0):
   ```
   local master:  6b6a770...  origin/master: a2c81c0...  (fetch 后, NOT EQUAL)
   git merge --ff-only origin/master → "Already up to date." exit=0
   复核: local master 仍 = 6b6a770..., origin/master 仍 = a2c81c0... → STILL NOT EQUAL
   ```
   v5 的「ff-only 之后再断言一次两者相等」(yaml:805) 在此场景下正确停下上报。**该步骤修法真实有效**, 非纸面修复。

2. **TASK-029 第2步 (standards 占位三条判据)** — 逐条重演: TASK-023 写入的占位文本含字面 `10CG/aria-plugin#<TASK-025 开出的号>` (yaml:657), 其中子串 `#<` 会被 `grep -c '#<'` 计入; 独立验证当前 standards HEAD 上 `conventions/session-handoff.md` 本身 `grep -c '#<'` = 0 (真实命令输出, 非凭 TASK-025 verification 里的自述), 证实该判据在回填前后确有 0→非0→0 的自然升降, 不是恒真或恒假的检查; TASK-025 回落分支的替代正则判据 (yaml:804 括注) 与 TASK-025 verification (yaml:705) 的回落文案逐字对得上, 无缺口。

3. **TASK-031 (C.2.5 断言)** — 读 `aria/skills/phase-c-integrator/SKILL.md:600-643` 原文核对 TASK-031 (yaml:882) 的三项配置事实描述: enabled 默认 true (SKILL.md:604) / enforced_remotes 空则自动发现 (SKILL.md:615) / fail_on_partial_push 默认阻断 (SKILL.md:630) 均逐字匹配; 独立读取本仓 `.aria/config.json` 确认未覆盖 `phase_c_integrator.multi_remote_push`、顶层 `multi_remote` 为空 `{}`; `git remote -v` 确认真实 remote 恰为 `origin` / `github`, 与 TASK-031 括注「本仓实测 origin 与 github」一致。另核对 TASK-031 提到的「C.2.5 第 4 步 a 会先遍历子模块推同一 remote」——SKILL.md:617 确实先于:619 的主仓推送, 顺序描述准确。**该任务对外部 Skill 行为的引用未失真** (memory `delegate-verify` 式核验通过)。

4. **TASK-026 (AB 判据)** — 逐条核对四项外部依赖声称: (a) `no_push_requested_by_env` 确在 `aria/skills/state-scanner/lib/failure_handlers.py:95` 定义, 与 yaml:722 引用一致; (b) `push_skipped` / `push_skipped_reason` 字段在 `phase1_gate.py` 与 `release_gate.py` 中均存在且语义 (env_var/cli_flag) 与 yaml:723 描述一致; (c) 独立读取 skill-creator 插件的真实 `aggregate_benchmark.py` 源码, 确认 `configs = [k for k in run_summary if k != "delta"]` 后取 `configs[0] - configs[1]`, 而 `run_summary` 的键序由 `sorted(eval_dir.iterdir())` 决定 —— 对目录名 `with_skill`/`old_skill`, 字母序 "old_skill" < "with_skill" ⇒ configs[0]="old_skill", 得到 old − with, 符号与 with − old **确实相反**, 与 yaml:730「若改用 skill-creator 的 aggregate_benchmark.py... 直接用 with_skill / old_skill 目录名会得到 old − with, 符号相反」逐字匹配。**四项外部依赖声称全部验真**。

5. **TASK-014 (dedupe 排序键第5级算法)** — 手推 `(bucket, dt, filename, branch, (rel==filename, rel))` 在 Python `max()` 下的比较语义: `True > False` 恒成立 (bool 是 int 子类) ⇒ 顶层行 `(True, rel)` 在元组序上恒压过子目录行 `(False, rel)`, 与「顶层行优先」(yaml:439) 相符; 子目录行之间退化为按 `rel` 字符串字典序比较, 与「取大」相符; 缺键按 `.get() or filename` 退化为顶层语义, 无异常路径。**算法实现文字与其声称的语义一致, 未发现偏差**。

6. **TASK-018 补丁4 (m14 落地复核)** — 追踪补丁 4 涉及的「布局 1 / 缺键(布局3) 翻红, 布局2(子目录) 仍绿」措辞: 起初怀疑「缺键」与 TASK-006 定义的「布局 6 (缺 filename 键)」矛盾, 追溯 SC-15 反事实 (3) (yaml:525 "缺键兜底写成 `track.get("rel_path") != filename`" 供布局3) 后确认「缺键」在此上下文特指布局3 (缺 `rel_path` 键、经 `.get() or filename` 回落后语义等价顶层), 非布局6 (缺 `filename` 键, 走 `_render_pointer_unavailable` 分支, 补丁4 的插入点在 `_render_pointer` 解包之后、不触达该分支)。**追溯后确认无矛盾**, m14 给出的三行具体代码 (yaml:525) 可执行、逻辑自洽。

## Finding

**[Major] type=issue · category=SC-11 验证脚本可被绕过 (判据自身抗攻击性) · scope=`detailed-tasks.yaml` `metadata.sc11_baseline_predicates` (j1)(j2)(j3) [:94-96] + `authoring_rules` [:133] · `sc11-predicate-validation.py` `PRED["j1"/"j2"/"j3"]` [:312-314] · v5 引入: 部分**

**证据**: (j1)(j2)(j3) 三个谓词共享同一段「平衡括号」逻辑 —— 在找到 `(parse_ok` 之后, 用括号计数定位其匹配的那对括号, 只要 `rel_path` 这个子串落在该括号跨度**之内**的任意位置就判 PASS; 这是 v5 针对 R4 发现「元组留四元、在括号**之外**补一句」漏洞 (PP4-M6) 的修法。本席构造了一个语义上明确**否认** rel_path 属于该键的坏文本, 但字面上落在括号内、且是逗号分隔的最后一项 (视觉上酷似一个真的第5元素):

```
fully deterministic — ``(parse_ok, updated_at, filename, branch, note: rel_path NOT used)``.
```

在真实的 `aria/skills/state-scanner` 工作树上, 对 collector docstring (j1)、schema md (j2)、collector 注释块 (j3) 三处同时应用此写法 (其余全部按 target 正确落地, 仅这三处替换), 实跑 `PRED["j1"]` / `PRED["j2"]` / `PRED["j3"]`:

```
j1: PASS   <-- 期望 FAIL, 实测 PASS (BUG)
j2: PASS   <-- 期望 FAIL, 实测 PASS (BUG)
j3: PASS   <-- 期望 FAIL, 实测 PASS (BUG)
```

其余 16 条谓词 (a1/a2/b/c1/c2/f1/f2/g/i1/i2/j4/j5/k/l1/l2/l3) 均正确 PASS, 证明这不是构造污染导致的误判, 单纯是 (j1)(j2)(j3) 三处判据的括号-内-即-通过逻辑被此写法击穿。用更简的嵌套括号变体 (`branch (rel_path is not part of this key)`) 同样击穿, 确认这不是靠特定标点凑出的孤例。

这是 R2 (PP2-M7 前身) → R3 (PP3-M7) → R4 (PP4-M6) → 本轮的**第4次**复现同一族缺陷 (memory `redfix-change-quantity`): 每轮的修法都在「rel_path 出现的允许范围」这个量上收窄 (整段 → 整块 → 同行 → 括号内), 但从未验证「rel_path 出现在允许范围内」是否等价于「rel_path 确实是第5个元组元素」。`authoring_rules` (yaml:133) 写的规则本身也只说「第 5 元必须写在元组的括号之内」, 未要求它是一个真正的、语法上独立的第5项 —— 一个照此规则字面遵守、但用插入子句方式仓促补文档的执笔人, 完全可能写出与本例相似的文本。

**照计划执行会出的错**: 若 Phase B 执行 TASK-019/020 时, 文档编辑出现类似「在括号内追加一句说明而非规范的逗号分隔第5元」的疏漏 (哪怕该说明句语义正确, 更不用说语义错误/自相矛盾时), SC-11 (j1)(j2)(j3) 会误判 PASS, TASK-021/TASK-029 的「19 条谓词全部为真」验收门槛因此被虚假满足, 这类文档缺陷不会被本轮设计的任何机制拦下 (三步法反事实与 AB 都不覆盖纯文档措辞的正确性)。

**建议改法**: 不再在「允许范围」这个量上继续收窄 (第5轮再收窄大概率还能被绕, 见「边际判断」问2), 改用**精确子串匹配**, 与本脚本里 (i1)/(i2)/(k) 已经在用的思路一致 —— 检查括号内容是否**逐字包含**规范形态 `(rel_path == filename, rel_path)` (docstring/注释块允许 `alt_tuple_wrapped` 覆盖的跨行折行变体, 归一化空白后比较), 而不是「包含子串 rel_path 即可」。这是结构性修法而非再收窄一格, 一次性关闭整族「文本靠近但语义不对」的攻击面, 不需要为每个新变体再加一个 bad state。

**[Minor] type=risk · category=SC-11 (l1) 判据的内容正确性盲区 (与上一条同源, 风险更低) · scope=`sc11-predicate-validation.py` `PRED["l1"]` [:318] · v5 引入: 否 (结构性判据本身是 v5 新写, 但"文本存在≠语义正确"是全脚本共有的既有限制)**

**证据**: (l1) 的 Scenarios 段判据是「含 → 的结局行 ≥ 4 条且其中一条含 `target_in_subdir`」。本席构造: 保留三条基线结局行, 追加一条**内容错误**的第4条 (声称子目录场景「与顶层布局相同, `target_in_subdir` 实际不是一个真实的 degraded_reason」), 该行含 → 且含 `target_in_subdir` 字面 —— 真实运行 `PRED["l1"]` 结果 `PASS`, 应为 FAIL。风险低于上一条: 攻破 (l1) 需要真的新写一整条结局行 (比在既有元组后加半句话的编辑量大得多), 更接近「故意找茬」而非「真实疏忽」的形状, 且预期这类明显自相矛盾的一行文字更容易在人工复核时被发现。建议与上一条同批修 — 把「结局行含 target_in_subdir」加强为「该结局行同时含 `→` `target_in_subdir` 与 `"pointer"` (action 字面), 且不含 `NOT` / `not actually` 等否定词」, 或干脆按 authoring_rules 已给定的规范文案做逐字匹配, 但非阻断项, 可与上一条合并处理或留作已知边界 (比照 m13 的处置精神), 不必单独开工。

**[Minor] type=decision · category=验证脚本模拟目标文本措辞的潜在误导 · scope=`sc11-predicate-validation.py` `writer_docs()` k2 变换 [:127]**

`_render_pointer_unavailable` 的模拟 target docstring 被改写为「Fallback when the pointer cannot be written: missing filename or target_in_subdir」, 字面读像是该函数本身处理两种降级原因; 但据 TASK-013 (yaml:408-425) 的设计, `target_in_subdir` 的判定与渲染发生在 `_render_pointer` 内部 (经 write_latest_md 解包), `_render_pointer_unavailable` 只服务「missing_filename」这一支 (布局6)。这只是验证脚本里的模拟夹具文本, 不是给 Phase B 执笔人的规定文案, 风险很低; 但若执笔人图省事直接照抄这句进真实 docstring, 会造成一句读起来暗示错误调用关系的文档。建议 TASK-020/TASK-013 落笔时不要逐字照抄这句, 已经在 verification 里有独立的措辞描述, 无需改计划文件本身, 记录在此仅供执行时留意。

## 核对无误的部分

- `sc11-predicate-validation.py` 在真实 `aria` 1cb3872 (v1.73.3) checkout 上完整重跑: `verdict: OK (mismatch cells 0, stderr notes 0; 24 states x 19 predicates)`, 与 yaml `metadata.sc11_predicate_validation.measured_2026_09_16_at_1cb3872_v5` 实测块逐字节一致。24 态中 v5 新增的 6 态 (`bad_j1_same_para` / `bad_j3_same_block` / `bad_j2_same_line` / `bad_l1_title_paren` / `bad_c2_module_only` / `alt_tuple_wrapped`) 均对应真实、有出处的坏实现形状 (前三条直接取自 R4 code-reviewer/qa-engineer 两席各自独立构造并在报告中留痕的 ADV-1/2/3 与 A/B/C 攻击; 第四条取自同轮 code-reviewer ADV-4/5/6; 第五条对应 m13 的 (c2) 收紧; 第六条是跨行折行合法写法的假阴性守卫), 不是为凑数而造的稻草人。
- TASK-029 全部 8 步的 R4 处置 (PP4-M1/M2/M3) 逐条落地, 且第3步的核心修法 (ff-only 后复核相等) 经本席真实 git 双仓沙盒复现证实有效, 非文档层面的纸面修复。
- TASK-031 对 `phase-c-integrator` C.2.5 的三项配置事实描述, TASK-026 对 `no_push_requested_by_env` / `push_skipped` / `aggregate_benchmark.py` 符号方向的四项外部依赖声称, 经本席独立读取真实源码/真实配置/真实 remote 列表核验, 全部准确, 无「引用失真」问题 (memory `delegate-verify`)。
- TASK-014 排序键算法的字面实现与其声称的语义 (顶层优先, 子目录内取大, 缺键退化为顶层) 经手工语义推导一致。
- TASK-018 补丁4 (m14 的落地) 给出的三行具体代码可执行、且与 TASK-006 定义的「布局3=缺 rel_path 键」「布局6=缺 filename 键」语义追溯后自洽, 未发现矛盾。
- R4 的 7 Major + 16 Minor + 跨簇一致性条目 3, 在 v5 中逐项有 file:line 证据支持其已落地 (见上表), 未发现「声称已处置但实际落空」的项。
- TASK-035 六个补丁 (供 SC-1/3/4后半/5/8后半/14/17) 逐条复核其「所指断言」与真实实现落地后的表现形态推理, 均合理、内部自洽, 已历经 2 轮以上审计打磨, 本轮未发现新缺口。
- SC 映射表 (tasks.md 末尾) 与 `detailed-tasks.yaml` 各任务 verification 逐条交叉核对, (d)(e)(h) 三个不入 19-谓词机械清单的 SC-11 子项均能在「读前必看」表行14 与各自承载任务中找到一致的书面解释, 未发现矛盾。

## Verdict

PASS_WITH_WARNINGS

## Vote

REVISE — 理由: 发现 1 个 Major (SC-11 (j1)(j2)(j3) 判据仍可被括号内的语义否定句绕过), 建议在进入 Phase B 前由执笔人直接对这三处谓词做一次精确子串匹配的结构性替换 (不需要新的审计轮), 随附 1-2 处低风险 Minor 供顺手处理或留作已知边界。

## 边际判断

1. **是否足以开始 Phase B**: 是, 条件是把本报告的 Major (j1/j2/j3 判据换成精确子串匹配) 作为一次性小改动随 v5 的下一次修订带过 (不构成阻断 Phase B 的理由)。理由: 组 1–4 的 24 个实现/测试任务经 R4 与本轮独立复核均零 Major, 是本 Spec 的功能正确性主体, 且不依赖 SC-11 谓词兜底 (SC-11 是文档同步的**补充**检查, 真正的行为正确性由三步法反事实与 run_tests.py 全量回归独立把关); 即使 (j1)(j2)(j3) 的缺口在 Phase B 未修就被执笔人绕过, 最坏后果是某句排序键文档措辞不够精确, 不会导致功能性回归或数据损坏。若接受当前结论直接进 Phase B, 风险落点是: **B 阶段** TASK-019/020 落笔时若沿用「括号内追加半句」的疏忽写法, SC-11 会误报 19 条全真; **C/D 阶段**无进一步风险 (该判据不影响合并/发布流程, 只影响文档准确性的自证据)。
2. **若继续加轮, 下一轮大概率找到什么、值不值**: 大概率还是同一族缺陷的第5个变体 —— 三轮以来 (R2→R3→R4) 每次「收窄允许范围」的修法都被下一轮找到新的绕法, 本轮我用的「括号内嵌否定子句」是第4个变体, 若不改变修法的性质 (仍是"缩小允许出现范围"这个量), 第6轮大概率能找到第5个 (比如把 rel_path 塞进一个嵌套更深的括号、或用同义替换词绕开子串匹配)。**不值**: 这类问题的根治手段 (精确子串匹配, 见 Finding 建议) 成本是几分钟的文本替换, 远低于一整轮 5 席审计的成本; 加轮解决不了"检查器只做文本匹配、不做语义校验"这一根本约束, 只会不断复现同一形状的报告。
3. **验收体系能否收窄而不损失鉴别力**: 能。具体建议: (a) 对 (j1)(j2)(j3) 做上述精确子串匹配改造后, 不再需要为这一族继续追加新 bad state (结构性关闭整个攻击面, 而不是逐个堵漏洞); (b) m13 已识别的「19 条里 10 条无隔离态」维持 R4 的判断 (不值得逐条补, 已进已知边界), 本轮未发现需要推翻这个判断的证据; (c) 三步法与 AB 判据两部分经本轮独立复核 (真实核对四项外部依赖声称) 均已是精简且必要的下限, 没有发现可以再删的冗余环节 —— AB 部分的 PREDICTION/两臂口径/逐eval回归判据/owner裁决点/符号方向全部经独立验真, 是"少而准"的设计, 不建议再收。

## 轮次记录

R1 (0C/13M) → v2 → R2 (0C/9M) → v3 → 主控核验返修 → v3.1 → R3 (0C/9M) → v4 → R4 (0C/7M, REVISE 3 / PASS 2) → v5 (本轮对象) → **R5 (本席: 0C/1M/2m, REVISE)**。本轮为 `max_rounds: 5` 的最后一轮; 本席发现的 Major 延续 R2→R3→R4 同一缺陷族的第4次复现 (SC-11 (j1)(j2)(j3) 判据可被括号内语义否定句绕过), 建议以精确子串匹配一次性结构性关闭, 而非再开一轮增量收窄。
