---
seat: A1-backend-architect
round: R2
checkpoint: post_spec
spec: subprocess-decode-hardening
verdict: PASS
critical_count: 0
major_count: 1
minor_count: 1
timestamp: 2026-08-20T13:05:00Z
---

# R1 findings 复核 (Q1 忠实 / Q2 处置对不对)

## A1-M1 (pre_merge_gate.py docstring 与全局约定矛盾)

**Q1 忠实**: 是。v2 条目 5(b) 逐字采用了 R1 建议的选项 (b) — 保留 `_verify_main_branch_exists`/`_sanitize_for_json` 局部描述 (surrogateescape+净化), 追加指向本 spec 全局约定的 cross-ref, 并明确声明「全局约定适用于新增/迁移调用点、不要求重写既有结构安全实现」。实读 `pre_merge_gate.py:302-349` 确认该函数确实不在 16 处迁移目标内 (无 `text=True`, 用手写 `capture_output=True` + `surrogateescape` 解码), 与 v2 的排除声明一致。SC-7「勘正执笔人≠实现执笔人」也已落。

**Q2 处置对**: 对。「追加而非改写 + 显式声明不适用范围」结构上避免了「docstring 指向约定但代码不遵约定」的自我复现 — 这正是本 spec §Why 诊断的病灶, 条目 5(b) 没有重蹈。未发现新矛盾。

## A1-M2 (扫描谓词是允许清单, 未来目录可静默逃逸)

**Q1 忠实**: 是。v2 条目 4 把谓词从「认 `scripts/`/`lib/`/`hooks/` 三目录」倒转为「`aria/**/*.py` 全量, 显式排除仅 `**/tests/**` 与 `test_*.py`/`conftest.py`」, 与 R1 建议的倒转方向一致。

**Q2 处置对，且比我 R1 的建议更彻底**: 对, 并且我需要修正自己 R1 的建议。R1 [A1-M2] 建议「至少加一条谓词完备性断言 (每个 .py 文件必属于扫描∪已知排除, 断言无第三类)」——但 v2 选择的「全含减显式排除」写法本身就是一个**全函数** (total predicate): 任何 `.py` 路径要么落入 `aria/**/*.py`, 要么被排除项接住, 数学上不存在「谓词覆盖不到」的第三态, 完备性由构造保证, 不需要额外跑一次「无第三类」的断言来兜底。我在 R1 建议的「加完备性断言」在这个更优的修法下是多余的 (allowlist 写法才需要这条断言打补丁; 倒转成 default-exclude 后完备性是构造性质, 不是经验性质)。**这处是我原判断可以再收紧的地方**: 应直接建议「倒转谓词」而非「倒转谓词 + 加断言」。

核验: 全仓 `find aria -name conftest.py` 只命中 `issue-triage/tests/conftest.py` 与 `tdd-enforcer/examples/python/tests/conftest.py`, 两者均落在 `**/tests/**` 内, 不会被误判为生产文件的「排除式误伤」——`test_*.py`/`conftest.py` 这层排除对当前语料是冗余保险, 未发现生产 `test_*.py`/生产 `conftest.py` 存在。

## A1-m1 (coordination_ref.py:255 误归类)

**Q1 忠实**: 是。v2 §Why 四层表把该点位单列 L3「errors= 结构安全 (1)」, 与 census 附注「R1 勘正」逐字对应。

**Q2 处置对**: 对, 无新问题。

## A1-m2 (helper 粒度: 按文件 vs 按调用点)

**Q1 忠实**: 是。v2 条目 3 明确「按文件级去重内联」, 点名 `aether.py :150/:173` 共用一个文件内 helper def。

**Q2 处置对**: 对, 无新问题。

## A1-m3 (SC-8 无 try 点缺 spec 层默认)

**Q1 部分忠实, 但方向不同**: v2 SC-8 确实给出了 spec 层默认 (满足「不留给 A.2 完全开放裁量」的核心诉求), 但选的默认方向与我 R1 建议的**相反**——我建议「默认复用 (TimeoutExpired, FileNotFoundError, OSError) 元组包一层」, v2 选的是「默认保持裸抛 + 行注声明」。

**Q2 我 R1 的建议本身是错的, 这次是对的**: 实读 `validate_schema_doc.py:116-142` (`_run_scan`), 它是独立 dev-time CLI 校验脚本的顶层调用, 不是被上层 gate 兜底的库函数——包一层 except 元组在这里只会静默吞掉 spawn 失败 (`sys.executable` 缺失等), 没有任何重试/降级收益, 反而削弱「dev-time 脚本 loud failure 优先」的合理默认。v2 选的「裸抛+注释」与任务 1.3「L1 层逐处保留既有 except 元组」(此点本就没有 except 可保留) 自洽, 也不违反 Out of scope 「except 元组不缩窄」(没有元组可缩窄)。**判定: 我 R1 [A1-m3] 建议的具体默认值是错的, v2 的默认值更贴合该调用点的实际语义**, 应作为 backend-architect 席自我纠正记录在案。

---

# 新增审计 (架构透镜, v2 新写文本自身)

## [A1-R2-C1] 无

## [A1-R2-M1] SC-9「四层计数复现 7/4/1/4」对 L2 层的机械化程度未言明, 存在过度承诺风险 (Major)

**锚点**: spec §Why AST 普查方法行 (「... + 调用链顶层捕获**人工补查**」) 对照 §Success Criteria SC-9 (「普查脚本... 对冻结基线跑复现四层计数 7/4/1/4」)。

§Why 自己明确把「调用链顶层捕获」标注为**人工补查**, 与前三轴 (`text=True` 实参 / enclosing except 枚举 / `errors=`/`encoding=` kwarg) 的纯 AST 自动检测性质不同——L2 的 4 处判定 (`custom_checks.py:342` 等经 `scan.py:476-479` `except Exception` 兜住、`issue-triage _common.py:39` 经 `triage.py:315-323` 兜住) 依赖跨文件调用图知识 (谁调用了谁、调用点是否被哪层 try 包住), 这不是单文件 `ast.walk` 能推导的, 必须靠人工先定位、脚本再对「记录下来的 wrapper file:line 处 except 类型是否仍然吻合」做结构性回验。

但 SC-9 的措辞读起来像是在断言「普查脚本 (机械) 能够复现 7/4/1/4」, 没有说明 L2 这一层的机械化边界在哪——即脚本对 L2 的「复现」实际上是「对一张人工核验过的调用链事实表做存在性/一致性回验」, 不是「从零推导分类」。这个边界如果不写进 SC-9, 会有两个下游风险: (a) 1.2 执笔人可能真的去写一个尝试自动做跨文件调用图分析的通用求解器, 在只有 4 个已知站点的场景下是过度工程; (b) 复核轮/未来维护者拿 SC-9 字面意思去验收, 发现「脚本」其实内嵌了一张手写映射表, 会误判为「不够机械」而打回, 或反过来误以为新增站点会被自动分类进 L2 而漏检——这正是本 spec 本身在整治的「文档断言与代码实际机制不同步」病灶, 出现在 spec 自己新增的 SC 条目里, 属于自我复现。

**建议修法**: SC-9 补一句机制声明, 例如: 「L2 层判定基于人工核验的调用链事实表 (站点→wrapper file:line→except 类型), 随 census 脚本一并入库; 脚本对该表做结构性回验 (记录的 wrapper 位置及 except 类型仍然成立), 而非通用调用图推导; 新增站点若涉及跨文件顶层捕获, 需人工补录该表, 不由脚本自动发现」。这样「机械」的适用范围就限定在「回验已知事实」而非「发现新事实」, SC-9 本身不再有过度承诺。

## [A1-R2-m1] 排除式扫描谓词未覆盖 `examples/`/`references/`/`templates/` 目录, 完备性目前靠语料巧合而非结构保证 (Minor)

**锚点**: spec §What Changes 条目 4 (「显式排除仅 `**/tests/**` 与 `test_*.py`/`conftest.py`」), 对照 `aria/skills/tdd-enforcer/examples/python/src/`。

实测 `find aria -name "*.py" -not -path "*/tests/*"` 全仓仅两个文件落在 `scripts/`/`lib/`/`hooks/`/`tests/` 之外 —— `tdd-enforcer/examples/python/src/calculator.py` 与 `__init__.py`, 且逐一确认均**不含** `subprocess`/`text=True` (语料当前干净)。但这两个文件属于「skill 自带的教学示例项目源码」, 不是本 spec 语境下的「生产调用点」——若未来该示例项目 (或任何 skill 新增的 `examples/`/`references/` 下的 `.py` 演示脚本) 恰好用 `subprocess.run(text=True)` 做教学示范, 新谓词会把它当「生产」纳入 SC-2/SC-3(a)(b) 的 0 命中断言, 造成假阳性 (需要「迁移」一段根本不是插件运行时代码的示例代码), 而不是 A1-M2 原本担心的假阴性方向。

这不影响 A1-M2 所修复的核心风险 (生产代码静默逃逸——`aria/**/*.py` 全量 + 排除 `tests/` 结构上已堵死), 是同一份谓词在覆盖面变广之后暴露的反方向、更低概率的次生风险, 且当前语料验证为零命中, 不阻塞本 spec 落地。

**建议修法**: 可选; 若 A.2 顺手把 `**/examples/**`、`**/references/**`、`**/templates/**` 一并加入排除清单 (与「已知非生产目录」定性一致) 更干净, 但不强制作为本轮 REVISE 理由——留 tasks 备注即可, 或干脆接受 (当前 0 命中, 且这三类目录 aria 仓内约定俗成不放运行时代码)。

---

# 总体判断

方案本体 (B/B′、16 处迁移目标、四层 7/4/1/4 口径) 经复核在 v2 仍然成立: 四层表逐一映射回 census 的 12 处「接不住」+ 4 处「接得住」, 互斥且完整覆盖 16 处, 未发现遗漏或重叠。排除式谓词的核心修法 (allowlist→default-exclude) 结构上确实堵死了 A1-M2 指出的静默逃逸, 且严格优于我 R1 建议的「加完备性断言」打法 (完备性变成构造性质)。A1-m3 上我 R1 给的默认值建议本身有误, v2 选择的默认 (裸抛+注释) 更贴合 `validate_schema_doc.py` 的实际语义, 记为自我纠正。

新增 Major (SC-9 L2 机械化边界未言明) 是文本精度问题, 不是方案可行性问题——可通过在 SC-9 补一句机制声明解决, 不需要重新设计。按判据 (0 Critical, 1 Major < 2) 落 **PASS**; 建议该 Major 在 A.2/1.2 落地 census 脚本时顺手把 SC-9 措辞收紧, 不必因此单独开一轮 R3。

---

## v3 收敛确认

对照 v3 `proposal.md` 逐条重读:

- **[A1-R2-M1] closed**: SC-9 (proposal.md:80) 已补「机制边界声明 (R2 A1/A3 席)」—— 明文区分 L3/L4 (词法 except 轴, 脚本机械推导) 与 L1/L2 (调用链顶层捕获, 不做通用调用图分析、以 §Why 四层表为人工标注输入、脚本仅做结构性回验、标注表变更须人工重核)。与我 R2 建议的修法方向一致 (「回验已知事实」而非「发现新事实」), 未来复核者/实现者不会再误读「census 脚本能自动推导 L2」。**closed**。

- **[A1-R2-m1] closed**: 条目 4 (proposal.md:55) 已补「`examples/`/`templates` 等文档性目录**有意不排除** (R2 A1-R2-m1): 示例代码同样是被复制的先例面, 命中即红是期望行为 (当前基线零命中, 实测核对)」。这把我原本标记为「结构性缺口 (靠语料巧合)」的状态显式转为「有意设计 (示例代码本就该被扫)」, 消除了歧义——不再是未言明的空白, 而是记录在案的裁决。**closed**。

两项 R2 findings 均已闭合, 无残留 Major/Minor, 未发现 v3 新引入的自相矛盾。**最终 verdict: PASS** (0 Critical / 0 Major / 0 Minor open)。

timestamp: 2026-08-20T14:20:00Z
