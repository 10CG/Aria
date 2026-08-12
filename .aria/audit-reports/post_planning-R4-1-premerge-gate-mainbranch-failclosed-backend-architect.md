---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T01:28:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3(→R4-1) — backend-architect 独立审计

被审对象: R2-fix 后的 `proposal.md` + `tasks.md` + `detailed-tasks.yaml`（commit `0dd26ce`）。
本报告文件名按派发指令写作 `R4-1`；正文内容是对 `0dd26ce` 的**独立**审计（见下方"⚠️ 首要发现"，本轮的
派发本身已经陈旧，但我仍按指令完整、独立地做了这件事，而不是省略）。

---

## ⚠️ 首要发现（操作层面，非 Spec 缺陷本身）：本轮派发已经陈旧

在动手审计前先做了 `git log` / `ls .aria/audit-reports/` 核验，结果如下（命令与输出附在文末"核验命令
存档"）：

- 当前仓 HEAD 是 `e970943`，比被审对象 `0dd26ce` **领先 5 个提交**，其中包含：
  - `47f94ae docs(audit): post_planning R3 (FAIL) — 三种结构性干预无一收敛, 机械交叉检查被证伪`
  - `ab4da15 docs(spec): A.1 premerge-gate-mainbranch-failclosed (Level 2) — Rule #8 那条腿恒绿的修法`
  - `b1c0fd9 docs(audit): #128 补落盘 R5.5 (v7 复核 2 席) + R6 (5 席) 审计报告`
  - `4ab295d docs(spec): #128 v9 — R6 findings 落地 + 机械闸全绿 (tech-lead 执笔, 第四次换人)`
  - `e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度`
- `.aria/audit-reports/` 里已经存在**完整的一轮真实 R3**（5 席全交 + aggregate）：
  `post_planning-R3-0/1/2/3/4-...` + `post_planning-R3-1786494000000-...-aggregate.md`，
  其中 `post_planning-R3-1-premerge-gate-mainbranch-failclosed-backend-architect.md`
  **正是我这个席位、审这同一个 commit** 的一次已完成运行（`timestamp: 2026-08-11T05:00:00.000Z`）。
- 该真实 R3 的 aggregate 判定 **FAIL**（4 REVISE / 1 PASS，去重 2C+~13M，10 条 `blocks_phase_b`），
  并且**明确回答了本轮的核心问题**：「那道机械交叉检查被证伪 —— 维度错配」（tech-lead 对副本做 5 个
  对抗构造，4 个被放行）。随后 `xcheck.py` 已被**重写**（当前 scratchpad 里的版本头部自陈
  "2026-08-12 R3-fix 重写... 该版本被证伪"），且更早的 `.aria/config.template.json`/Spec 本身也已经
  历过 R3-fix → v9(#128 R6 落地) 的后续迭代。

**结论**：这轮任务是对一个已经跑过、已有 aggregate 结论、且下游已经修复过的历史快照的**重复审计**。
我判断按硬性纪律"独立完成 R3 审计"这条指令仍应逐字执行（不得因为"反正已经有结论"就跳过实读源码），
但把这件事写在最前面，供编排层核对派发是否重复（memory
`feedback_concurrent_duplicate_audit_fetch_before_start`）。下文是我在**未读**上述已存在的
`post_planning-R3-1-...-backend-architect.md` 之前独立做出的分析；读取该文件仅用于收尾阶段的交叉验证
（见"与既有 R3 backend-architect 报告的交叉核对"一节），未回改我自己的结论。

---

## 投票

**VOTE: REVISE** — 0 Critical + 2 Major（均为本轮独立发现，且均可回源到 R2-fix 引入的新文本）。
**verdict = PASS_WITH_WARNINGS**。

---

## 审视范围与方法

席位角度：**实现可行性** — §6.1 插入点是否唯一确定且与 D9/§6/SC-M10 不冲突 / 异常·重试·解码三轴 /
信号传播通道是否真存在。方法：对 `pre_merge_gate.py`（当前仓内，尚未被本 change 改动，是 Phase B 的
起点真值）/ `ci_backends/aether.py` / `path_coverage.py` / `workflow-runner/SKILL.md` 逐行实读；把
`0dd26ce` 的三份文档单独 `git show` 到 scratch 目录后核对（**不使用当前工作树的 proposal.md** ——
工作树已经是 R3-fix 之后的版本，与被审对象不是同一份文本，见下方证据）。

---

## R2 的 1C + ~13M 是否真闭合（本席位角度逐条回源）

### R2 Critical（信号传播缺口）—— 位置声明正确，但承重理由本身有事实错误（见 Finding 1）

R2 原始 Critical：TASK-020 的 fail-CLOSED 既无插入点规定，又可能与 D9/§6/SC-M10 在同一输入上冲突。
`0dd26ce` 版 §6.1 给出了明确的插入点（`:328` enabled 早退之后、`:337 resolve_ci_backend` 之前）与三条
判别用例，**位置声明本身**经我独立核验是自洽的（见下方 Finding 1 之前的"位置唯一性"分析）。但支撑这个
位置的**承重理由**里有一句可独立证伪的事实性错误，会让"位置对、依据错"的文本产生"表面已闭合、实际
留了一个数据源空洞"的效果 —— 详见 Finding 1。故我把 R2 Critical 判定为**部分闭合**：位置维度已闭合，
但闭合方式所依赖的理由本身不成立，需要单独修（已被 `0dd26ce` 之后的真实 R3-fix 修掉，见下方证据）。

**§6.1 插入点位置唯一性 —— 独立复核**（`pre_merge_gate.py` 当前源码实读）：

```
$ grep -n "def gate_check\|_normalize_config(\|resolve_ci_backend(\|_no_ci_output(\|cfg\[.enabled.\]\|precheck(\|evaluate_path_coverage(" \
    aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
94:def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
124:def resolve_ci_backend(config: dict[str, Any]) -> CIBackend | None:
266:def _no_ci_output(no_ci_fallback: str) -> dict[str, Any]:
298:def gate_check(
325:    user_normalized = _normalize_config(config or {})
328:    if not cfg["enabled"]:
337:    backend = resolve_ci_backend(cfg)
339:        return _no_ci_output(cfg["no_ci_fallback"])
344:    ok, precheck_err = backend.precheck()
358:    pc = evaluate_path_coverage(
```

行号与 §6.1/§6 引用的 `:325/:328/:337/:339/:344/:358` **逐一核对一致**（这些行号在 Phase B 落地前尚未
位移，是当前基线真值）。§6（存在性核验）钉在 `:345`（precheck 失败早退）之后、`:358`（path coverage）
之前；§6.1（legacy-key 硬失败）钉在 `:328` 之后、`:337` 之前 —— **两段区间在执行顺序上不重叠**
（enabled → [legacy-key 检查] → resolve_ci_backend → no-backend 早退 → precheck → [存在性核验] →
path coverage），§6 末尾"两节不得互相援引"的声明在**位置**这个维度上站得住。

### 三个测试用例本身的判别力 —— 有效，但仅当"读哪个变量"被正确实现时

我逐条走查了 §6.1 的三条穷举用例 (i)/(ii)/(iii) 对"正确实现"与"读错变量的实现"的判别力：

- (i) `enabled=false` + legacy key → 在 `:328` 就已提前返回，两种实现都会通过（这条本来就不测插入点，
  它测的是"不该被误伤"）；
- (ii) `enabled=true` + `no_aether_fallback` + 无可用 backend → **若实现读的是 `cfg`**（而非原始
  `config`），因为 `cfg` 里已经没有 legacy key 名（见 Finding 1 的源码证据），这条新检查永远不触发，
  执行会落到 `:339 _no_ci_output(cfg["no_ci_fallback"])`。由于 `_normalize_config` 已经把
  `no_aether_fallback: "abort"` 正确翻译成 `cfg["no_ci_fallback"] = "abort"`，`_no_ci_output("abort")`
  **本来就会**返回 `verdict=fail`（见 `pre_merge_gate.py:273-284`）—— 但它的 `raw_message` 是
  `_no_ci_output` 自己的文案（"no CI backend available and no_ci_fallback=abort: install..."），**不会
  点名旧键**。§6.1 用例 (ii) 的期望是 "`fail` + `raw_message` **点名旧键**"，所以只要验收断言同时核对
  `raw_message` 的内容（而不是只核对 `verdict == "fail"`），这条用例**确实能**把"读 cfg"的错误实现
  打红；
- (iii) `enabled=true` + legacy key + backend 正常 → "读 cfg" 的错误实现会完全跳过新检查、正常往下走
  查 in-flight/PR CI，最终返回 `wait`/`green`，**不是** `fail`，会被这条用例直接打红。

⇒ **三条用例的"验收断言"本身足以防住"读错变量"这个错误**，只要 (ii) 的 `raw_message` 内容断言被
如实实现（这点 §6.1 正文与 TASK-020 verification 都写明了"点名旧键"）。这也是我把 Finding 1 定级为
Major 而非新的 Critical 的主要理由：**具体的验收命令能兜底，但支撑这些验收命令的叙述性理由本身
是错的**，误导性文本仍然是一个真实的实现风险（见 Finding 1）。

---

## Finding 1（Major）—— §6.1 的承重理由"两个别名键的首个消费者分别在 `:337` 与 `:339`"与代码不符

**定位**：`proposal.md`（`0dd26ce` 版）§6.1 第二段 "**在 `resolve_ci_backend` 之前**" 一句；
`detailed-tasks.yaml`（`0dd26ce` 版）TASK-020 verification 逐字复述同一句（"两个别名键的首个消费者
分别在 `:337` 与 `:339`"）。

**实读证据**（`pre_merge_gate.py:94-121`，`_normalize_config` 全函数）：

```python
def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    out = dict(config)  # shallow copy
    for old, new in _OLD_TO_NEW.items():
        if old in out:
            if new in out:
                ...
                del out[old]                              # :111
            else:
                ...
                out[new] = _translate_value(old, out.pop(old))   # :120 —— pop 把旧键名从 out 里摘掉
    return out
```

`gate_check()` 里紧接着 `:325 user_normalized = _normalize_config(config or {})` /
`:326 cfg = {**DEFAULT_CONFIG, **user_normalized}` —— **`_normalize_config` 在返回前已经把旧键名
`del`/`pop` 掉**，它的返回值（进而合成的 `cfg`）**结构上不可能再含有旧键名**。`:337
resolve_ci_backend(cfg)` 与 `:339 _no_ci_output(cfg["no_ci_fallback"])` 读的都是这个已经翻译过的
`cfg`，它们消费的是**翻译后的新键值**，**从未接触过旧键名本身**。旧键名字面量在整个函数体内**唯一**
被检查（`if old in out`）的地方是 `:103`，也就是 `_normalize_config` 内部，对应 `gate_check` 里的
`:325` 这一行。

**⇒ "两个别名键的首个消费者分别在 `:337` 与 `:339`" 是一个可独立证伪的事实性错误** —— 真正"消费"
（检测）旧键名字面量的地方是 `:325`（`_normalize_config` 调用处/其内部），不是 `:337`/`:339`。

**为什么这不只是措辞问题**：§6.1 把插入点钉在 `:328` 之后、`:337` 之前，这个**位置**声明本身是对的
（见上节）；但它给出的**理由**——"两个别名键的首个消费者在 :337/:339"——如果被字面理解，会暗示"检查
应该在 `resolve_ci_backend`/`_no_ci_output` 消费之前拦截**它们即将读到的那份数据**"，而那份数据
（`cfg`）里根本没有旧键名。一个只依据这句理由、不逐行核对 `_normalize_config` 实现细节的实现者，
容易写出"在 `:328`~`:337` 之间检查 `cfg` 是否含旧键名"这种**结构上恒假**的判断（`cfg` 永远不含
旧键名），从而让 TASK-020 要治的 fail-OPEN **原样复发**——具体分析见上节"三个测试用例本身的判别力"：
好在 (ii)/(iii) 两条用例的**验收断言**（尤其是 (ii) 对 `raw_message` 内容的要求）足以在测试阶段把这种
错误实现打红，所以我把它定级为 Major（风险真实存在、但有下游安全网）而非新的 Critical。

**这条错误在 `0dd26ce` 之后被真实修正过**：当前工作树（`HEAD`, 即真实 R3-fix 之后）的
`proposal.md` §6.1 已经把这句改成：

> "⚠️ 上一版此处的承重理由是错的，本版更正（post_planning R3/tech-lead，编排层复跑坐实）...
> 旧键名本身的首个消费者是 `:325` 的 `_normalize_config`... 🔴 判定的输入必须是未归一化的原始
> `config` 入参，不是 `cfg`"

这与我独立读源码得出的结论**逐字一致**（我在读到这段修正文本之前已经完成上面的源码核对与结论）。
这也印证了：**这个缺陷在 `0dd26ce`（本轮被审对象）时点确实存在**，且已经被后续一轮（真实存在的
post_planning R3，非本次派发）的 tech-lead 席位发现并修复。

---

## Finding 2（Major）—— TASK-020 自己的主战场（`pre_merge_gate.py` 等 4/5 文件）没有机械 SC 钉住"归零"，只有 `config-loader` 一个文件有

**定位**：`proposal.md`（`0dd26ce`）§Rule #6 / SC-M17（唯一一条）；`detailed-tasks.yaml` TASK-020
verification（`0dd26ce` 版，对应当前仓 `:739-804` 区间的前身）。

**实测**（在 `0dd26ce` 快照上跑，命令与结果见下）：

```
$ grep -n "removed in v2\.0\|still (readable\|仍读\|v2\.0 移除" tasks.md detailed-tasks.yaml proposal.md
```

命中的全部行里，**没有一处**是"`pre_merge_gate.py` 的 `:68`/`:116`（或 `SKILL.md` 的 7 行、
`.aria/config.template.json` 的 2 行）必须在落地后归零"这种带期望值的机械断言 —— 全部是叙述今日计数
或枚举完整性的散文。全篇唯一被提升为机械 SC 的只有 `SC-M17`（`config-loader/SKILL.md` 的 2 处
"still readable/removed in v2.0" 措辞，`2 → 0`）。TASK-020 自己 verification 里逐字列出的
"逐文件今日实测（键名面/承诺措辞面命中）"表——

```
pre_merge_gate.py 6/2 · phase-c-integrator/SKILL.md 6/4 · config-loader/SKILL.md 2/2 ·
tests/test_pre_merge_gate.py 17/3 · .aria/config.template.json 2/0
```

——除 `config-loader/SKILL.md` 那一栏外，其余四栏的"承诺措辞面"（2、4、3、0）**没有任何一个** SC
编号要求它们归零。

**怎么会红（可证伪，已构造反例路径）**：一个实现可以（a）在 `:328`~`:337` 之间正确插入 legacy-key
硬失败检查（读原始 `config`，Finding 1 的坑已避开）；（b）**完全不触碰 `_normalize_config()` 函数体**
——它继续无条件执行、继续做"翻译 + `warnings.warn(...will be removed in v2.0...)`"这套软降级逻辑，
只是产出随后被 (a) 判定为非法整体丢弃；（c）把三个 `test_old_key_*` 改写为断言 `gate_check(...)`
返回 `verdict=="fail"`。在这个实现下：SC-M10 两条 fixture、三条插入点判别用例、CLI 真实路径用例、
改写后的 `test_old_key_*`、**SC-M17**（它只查 `config-loader/SKILL.md`，与 `pre_merge_gate.py` 无关）
**全部通过**，TASK-021 的"SC-M1..SC-M17 全部为期望值"也通过（17 条编号 SC 里根本不含这个量）。但
`pre_merge_gate.py:68`/`:116` 的 "will be removed in v2.0" 文本会 100% 原样留在已发布的 v2.0.0 代码
里，`_normalize_config()` 每次遇到 legacy key 仍会真的执行一次翻译 + 发一次 `DeprecationWarning`
——这与 TASK-020 存在的理由本身（"到期承诺必须兑现"）直接矛盾，却**没有任何机械信号会变红**。

**与本轮核心问题的关系**：这正是 Spec 自己反复诊断的"只修实例不修类"在它自己发明的补救机制
（SC-M17）身上的复发 —— `config-loader` 这一个实例被正确钉住了，但同一份 TASK-020、同一个"5 文件
删除面"枚举里的姊妹实例（尤其是 `pre_merge_gate.py` 自身）没有被同等对待。也正是 SC-M14 那句方法论
原话（"无编号即不被任何机械勾稽点找到，只能靠人工读散文"）预言的失效模式。

**建议**：仿 SC-M17 的模板，至少给 `pre_merge_gate.py` 补一条独立 SC（如 SC-M18）：
`grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' pre_merge_gate.py` 由 2 → 0；
`phase-c-integrator/SKILL.md`（4 行承诺面）、`.aria/config.template.json`（键名面 2→0）同理，或明确
写清楚"为什么这些文件的待遇与 `config-loader` 不同"。

---

## 那道机械交叉检查（xcheck.py）真的有效吗

### 1. 四项判据（现已扩到六项）覆盖得住 R2 的两个形状吗？

**覆盖不住，我的两条 Finding 都在覆盖范围之外，且是两种不同的逃逸方式**：

- **Finding 1 的逃逸方式**：这是"移交给没核过的下游"这个形状的一个更隐蔽的变体 —— 它不是"任务 A 把
  活移交给任务 B，而 B 不知道"，而是"**Spec 正文对源码结构做了一个断言（:337/:339 是首个消费者），
  但这个断言从未与真实源码核对过**"。我实读了 `xcheck.py`（scratchpad 里 R3-fix 重写后的版本）
  全部六项检查，没有一项会读取或核对 `pre_merge_gate.py` 之类的**实现源码**——CHECK5 是唯一会
  `subprocess.run(["grep", ...])` 读仓内真实文件的检查，但它只核对 SC 表"今日实测"列的**数字**是否
  可回源，不核对 proposal 正文里"某行是某某函数的首个消费者"这类**关于代码结构的散文断言**是否属实。
  这是一个结构性盲区：**xcheck 只做"三份 Spec 文档互相对照"，从不做"Spec 断言 vs 真实实现源码"的
  对照**。
- **Finding 2 的逃逸方式**：与真实 R3 backend-architect 报告（见下方交叉核对）已经指出的 CHECK2
  盲区完全一致 —— CHECK2 的 `SCS` 集合逐字取自 proposal SC 表**已经存在**的行
  (`re.findall(r"^\|\s*\*\*(SC-M\d+[a-c]?)\*\*\s*\|", ...)`)，结构上不可能发现"一条要求写在散文里，
  但从未被赋予 SC 编号"这件事，因为不存在的 key 根本不会进入被迭代的集合。

**我自己额外跑的验证**（用 R3-fix 重写后的 `xcheck.py` 回跑 `0dd26ce` 快照，验证它是否会意外碰到我
的两条 Finding）：

```
$ python3 xcheck.py <0dd26ce 快照目录> --repo-root /home/dev/Aria
...
RESULT: FAIL (22)
```

22 条失败里全部是 CHECK3(c)（行号锚未被护栏覆盖）、CHECK5（SC-M16 声称 1 实跑 0）、CHECK6（3 处
task_group 与 DAG 方向未成文）——**没有一条**涉及 Finding 1（`:337`/`:339` 断言与源码不符）或
Finding 2（`pre_merge_gate.py` 缺 SC）。这是直接证据：即便是"证伪后重写"的六项版本，也覆盖不住我
本轮独立发现的两个缺口。**⚠️ 方法论说明**：这个回跑用的是当前（R3-fix 之后）的 `xcheck.py` 去测
`0dd26ce` 时点的文档快照，是一次跨版本组合，不等价于"R2-fix 当时跑的原始四项版本会不会抓到" ——
但它足以回答本轮真正该问的问题：**"经过一次真实的证伪-重写循环之后，六项版本仍然覆盖不住这两个新
形状"**，这本身就是"只修实例不修类"在 xcheck 自己身上的第二次复发证据。

### 2. 有没有恒绿的判据？

**有，且是结构性的，不是"这次没测到"**：

- **CHECK2 对"要求写在散文里但从未被赋予 SC 编号"这整个类别是结构性恒绿**——判据公式
  `SC ∈ proposal 表 → 查 owner` 在任何"不存在的 SC 编号"输入下都不可能触发，因为不存在的 key
  不会进入被迭代的集合。Finding 2 是这条恒绿判据的一个真实、当场可复现的实例：`0dd26ce` 快照上
  跑 `xcheck.py` 不会对 Finding 2 报警，即便这个缺口彼时已经在场（这是我自己实测得到的，不是转引）。
- **xcheck.py 自身的头部注释承认**（scratchpad 版本文件第 6-19 行，逐字）：R2-fix 当时跑的**原始**
  四项版本里，CHECK1 是"无向"判据（把依赖边反向仍 PASS）、CHECK4 前半段"纯 print 零断言"——这两项
  在"当前取值恰好为 PASS"之外的绝大多数输入下**根本不可能变红**，是被真实 R3/tech-lead 的 5 个
  对抗构造实测出 4 个被放行后才承认、才重写的。**我自己没有能力拿到那个原始版本去复现这一点**（
  scratchpad 只留了重写后的版本），但这段自陈本身是这份 Spec 系列文档里少见的、经过对抗测试验证过的
  一手证据，我认为可以直接引用而不必自己重复实验。

### 3. xcheck.py 自己是不是一个"只修实例不修类"的产物？

**是，且我这一轮又给它加了一个新的同族缺口样本**：

真实 R3（`.aria/audit-reports/post_planning-R3-1786494000000-...-aggregate.md`）已经点名三个"同族
缺席"项：`task_group ↔ DAG 方向一致性`、`deliverables ⊆ scope_repos.paths`、`SC 表"今日实测"列
是否回源`——随后 R3-fix 把前两项之一（`task_group` 方向）与"SC 表回源"分别做成了新的 CHECK6/CHECK5。
但我本轮独立发现的 Finding 1（**Spec 断言 vs 真实源码语义**）和 Finding 2（**要求存在但从未被赋 SC
编号**的这个具体新实例，尽管其"类"——CHECK2 盲区——R3 已经点名过，`pre_merge_gate.py` 这个具体
"孙子实例"仍然没人把它填进任何 SC 表）——两者都还没有被纳入任何一项检查。**每一轮"抓到什么就补哪
项检查"的修法都只扩大了已知失效实例的覆盖面，从未把"Spec 正文断言是否与实现源码相符"这一整类检查
补进来**——这本身就是本 Spec 反复诊断的那个形状，在负责"诊断这个形状"的工具自己身上第三次复发
（第一次是原始 xcheck 的 CHECK1-4，第二次是真实 R3 点名的三个同族缺席，第三次是本轮）。

### 4. 拒绝能力实测（改一处再跑）

我做了一次针对 **CHECK5**（"SC 表今日实测列回源"）的受控变异，验证它是否真的会核对数字而不是照抄：

```
$ # 在 scratch 副本的 proposal.md 里把 SC-M17 的"今日实测"列从 2 改成 5（保持其余不变）
$ python3 xcheck.py <变异后目录> --repo-root /home/dev/Aria 2>&1 | grep SC-M17
  SC-M17   声称 [5]          实跑 [2]          ✗ **不符**
```

**CHECK5 确实有拒绝能力**——它不是橡皮图章，对"声称值被人为改错"这种情形会真实报红。这与真实 R3
backend-architect 报告里对 CHECK1 做的正向变异测试（删依赖边后 CHECK1 真实报红）结论一致：xcheck
**不是完全无效**，它对自己判据公式覆盖到的输入有真实的拒绝能力；问题在于判据公式的**覆盖边界**
本身画得太窄，一次次被同一份 Spec 的下一版新写法绕过。

---

## 与既有 `post_planning-R3-1-...-backend-architect.md` 的交叉核对

完成上述独立分析后，我读了这份已存在的同席位报告用于交叉验证（未改动我上面的结论）：

- **收敛点**：该报告同样判定 §6.1 插入点"位置"唯一确定、与 D9/§6/SC-M10 不冲突；同样独立发现了
  Finding 2（其报告标为"Finding 1"，逐字实读证据与我基本一致，含同样的三步反例构造）；投票同为
  `REVISE / PASS_WITH_WARNINGS / 0C+1M`。
- **分歧点（值得记录）**：该报告在"Major 抽样回源"表格里把"`resolve_ci_backend`/`no_ci_fallback`
  消费点行号 (`:337`/`:339`)"标注为"✅ 属实"，理由是"逐行核对一致"——**这个核对本身没有错**（`:337`
  确实是 `resolve_ci_backend` 调用行，`:339` 确实是 `_no_ci_output` 调用行），但它验证的是"行号→
  函数调用"这个较弱的命题，没有验证 §6.1 正文更具体的主张"这两行是**旧键名**的首个消费者"——后者才是
  我 Finding 1 定位的错误点。真实 R3 的 tech-lead 席位抓到了这个更具体的错误（已被 R3-fix 采纳修正，
  见 Finding 1 证据段）。我认为这是"引用在一个维度上核对通过，掩盖了另一个维度上的错误"的一个实例
  （呼应 memory `critique-repeats-error`：核对别人的断言时，必须核对断言**实际主张的那个量**，而不是
  与它字面相邻、看起来相关但更弱的另一个量）——即便是同一个席位、同一个人跨轮独立核验，也会在这一点
  上打盹，说明这类"叙述对代码的具体结构性主张"最好有机械/半机械的复核习惯（例如：任何"X 是 Y 的
  首个消费者"这类断言，复核时应该单独去读 Y 的定义本身，而不是只确认 Y 所在的行号存在）。

---

## 阻塞项

我本席位本轮的两条 Major 均不构成对 Phase B **开工**的阻塞（不影响 TG-0~TG-2 的 TDD 前置与核心实现），
但都应在 TASK-020 落地前补上（Finding 1 已经在真实 R3-fix 中被修正；Finding 2 截至 `0dd26ce` 与我核对
的当前工作树均未见对应的 SC-M18，建议由 owner/后续执笔方确认是否已补或仍待补，因为 CLAUDE.md 里的
`当前阶段` 摘要未提及此 Spec 的最新状态，本报告不代裁）。

`blocks_phase_b`: 均为 **false**（本席位角度）。

---

## 核验命令存档（全部实跑，附输出）

```
$ git rev-parse HEAD
e9709435e71d88bc4524ace7073298cfc602e793

$ git merge-base --is-ancestor 0dd26ce HEAD && echo YES
YES

$ git log --oneline 0dd26ce..HEAD
e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度
4ab295d docs(spec): #128 v9 — R6 findings 落地 + 机械闸全绿 (tech-lead 执笔, 第四次换人)
b1c0fd9 docs(audit): #128 补落盘 R5.5 (v7 复核 2 席) + R6 (5 席) 审计报告 — 修 R6 CR6-M2
7582238 docs(handoff): §10.5 编排层第 7 条错误 — 我用 Rule #10 之外的理由停了一个 enabled 闸门
47f94ae docs(audit): post_planning R3 (FAIL) — 三种结构性干预无一收敛, 机械交叉检查被证伪

$ grep -n "def gate_check\|_normalize_config(\|resolve_ci_backend(\|_no_ci_output(\|precheck(\|evaluate_path_coverage(\|query_branch_in_flight(" \
    aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
94:def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
124:def resolve_ci_backend(config: dict[str, Any]) -> CIBackend | None:
266:def _no_ci_output(no_ci_fallback: str) -> dict[str, Any]:
298:def gate_check(
325:    user_normalized = _normalize_config(config or {})
328:    if not cfg["enabled"]:
337:    backend = resolve_ci_backend(cfg)
339:        return _no_ci_output(cfg["no_ci_fallback"])
344:    ok, precheck_err = backend.precheck()
358:    pc = evaluate_path_coverage(
366:    in_flight = backend.query_branch_in_flight(main_branch)

$ grep -n "def main\|__main__\|sys.exit(main\|try:\|except" aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
(见正文 —— 确认 main() 与 gate_check() 调用处均无 try/except 包裹，仅 :365-376/:388-399
两处局部 try/except 包裹 backend.query_* 调用)

$ grep -rn "gate_error" aria/
(零命中)

$ sed -n '350,357p' aria/skills/workflow-runner/SKILL.md
     - verdict=green → 调 branch-manager merge,清理 gate_state
     - verdict=fail → workflow-state.session.status=failed,保留 gate_state 给 audit trail
     - timeout → user prompt;continue → reset retry_count + 继续;abort → stop
     - Ctrl-C → workflow-state.session.status=suspended,保留 gate_state 给 resume

$ sed -n '160,190p' aria/skills/phase-c-integrator/scripts/ci_backends/aether.py
(确认 _run_with_retry 用 text=True、只 except TimeoutExpired、docstring "other exceptions
bubble up"、RETRY_BACKOFF=(5,15,45)、超时哨兵 return -1)

$ sed -n '75,100p' aria/skills/phase-c-integrator/scripts/path_coverage.py
(确认 _run_git 捕获 (TimeoutExpired, FileNotFoundError, OSError) 三元组、bytes+surrogateescape 解码)

$ grep -n "removed in v2\.0\|still (readable\|仍读\|v2\.0 移除" tasks.md detailed-tasks.yaml proposal.md
(0dd26ce 快照; 全部命中均为散文, 无一是 pre_merge_gate.py/SKILL.md/.aria/config.template.json 的
机械归零断言; 唯一机械断言 SC-M17 只管 config-loader/SKILL.md)

$ python3 xcheck.py <0dd26ce 快照目录> --repo-root /home/dev/Aria
RESULT: FAIL (22)  # 全部为 CHECK3(c)/CHECK5(SC-M16)/CHECK6, 均与 Finding 1/2 无关

$ # 受控变异: SC-M17 今日实测列 2→5
$ python3 xcheck.py <变异后目录> --repo-root /home/dev/Aria 2>&1 | grep SC-M17
  SC-M17   声称 [5]          实跑 [2]          ✗ **不符**
```
