---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-11T05:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — backend-architect 独立审计

被审对象: R2-fix 后的 `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (commit `0dd26ce`)。
执笔方为 R2 五席之外的换人执笔轮, 本轮首次施用「fix 后强制跑机械条款间交叉检查」处方。

## 投票

**VOTE: REVISE** — 0 Critical + 1 Major (本轮独立发现, 非 R2 遗留)。**verdict = PASS_WITH_WARNINGS**。

不投 PASS 的理由: 我发现的 Major 直接命中本轮的核心问题 ("那道机械检查真的有效吗"), 且是一个
**machine-invisible** 的缺口 (不会被任何现有 SC/xcheck 抓到), 按本 Spec 自己的方法论 ("无编号即不被
任何机械勾稽点找到, 只能靠人工读散文" —— proposal SC-M14 那句原话) 应该在进入 TASK-020 实施前补上。

## 审视范围与方法

我的席位角度 = **实现可行性**: §6.1 插入点是否唯一确定且与 D9/§6/SC-M10 不冲突 / 异常·重试·解码三轴
/ 信号传播通道是否真存在。方法: 对 `pre_merge_gate.py` / `ci_backends/aether.py` / `path_coverage.py`
/ `config-loader/SKILL.md` / `workflow-runner/SKILL.md` / `github_actions.py` 逐行实读 (非采信 Spec 自陈),
并**实跑** `xcheck.py`(未改动)以及一份**受控变异后的副本**(测拒绝能力, 未触碰仓内真实文件)。

---

## R2 的 1C + ~13M 是否真闭合 (逐条回源)

### Critical (TASK-020 信号传播缺口) — ✅ 已闭合, 已独立复核

**R2 原始证据** (`post_planning-R2-1786406287820-...-backend-architect.md` Finding 1, 我本人上一轮所写):
`_normalize_config()` 与 `main()` 对 `gate_check()` 的调用均无 `try/except`, 裸 `raise` 会使 CLI 崩溃、
stdout 无 JSON、`verdict` 从未被构造。

**本轮独立复读** `pre_merge_gate.py:298-445`:
```
$ sed -n '325,339p' pre_merge_gate.py
    user_normalized = _normalize_config(config or {})
    cfg = {**DEFAULT_CONFIG, **user_normalized}
    if not cfg["enabled"]:
        return _build_output(...)
    backend = resolve_ci_backend(cfg)
    if backend is None:
        return _no_ci_output(cfg["no_ci_fallback"])
$ sed -n '434,440p' pre_merge_gate.py
    output = gate_check(
        pr_branch=args.pr_branch, main_branch=args.main_branch, config=config
    )
    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
```
**确认**: 全函数唯一的 `try/except` 是 `:365-376` `:388-399` 两处, 分别只包裹
`backend.query_branch_in_flight` / `backend.query_pr_ci` 两次调用, `_normalize_config()` 调用处
(`:325`) 与 `main()` 对 `gate_check()` 的调用处 (`:435`) **均无任何异常兜底**, 证据成立。

**R2-fix 的处置** (`tasks.md:124-125` + `detailed-tasks.yaml` TASK-020): 明确要求硬失败走
`verdict="fail"` + `raw_message` 的正常六键输出, ⛔ 不得裸 `raise` 穿过, 且验收**必须含一条走
`main()`/CLI 真实路径的用例**(断言 stdout 可解析 JSON + `verdict=="fail"`), 明确否决
"只在 `_normalize_config` 上做 `assertRaises`" 这种维度不匹配的验收。

**结论**: 机制设计正确, `_build_output(verdict=VERDICT_FAIL, ...)` 是仓内已有的正确落点
(`_no_ci_output` 的 `abort` 分支就是同形先例, 已实读确认 `pre_merge_gate.py:266-287`)。**✅ 闭合。**

### Major 抽样回源 (聚焦本席位相关的条目, 非穷举全部 ~13)

| 条目 | 判定 | 证据 |
|---|---|---|
| TASK-008 不传递依赖 TASK-010 (24 处补参未完成前插入新 subprocess ⇒ TypeError) | ✅ 已闭合 | `detailed-tasks.yaml` TASK-008 `dependencies` 实读含 `TASK-010` |
| SC-M10 需两个 fixture 变体 (含 legacy key 交叉输入) | ✅ 已闭合 | proposal §6.1 表 + TASK-008/TASK-020 verification 均含变体 (b) 表述一致 |
| TASK-015 (AB) 未传递依赖 TASK-020 ⇒ AB 跑的 SHA ≠ ship SHA | ✅ 已闭合 | TASK-015 `dependencies` 实读含 `TASK-021`(传递闭包覆盖 020) |
| §6/§6.1 两个插入点会否互相干扰 | ✅ 确认不冲突, 见下方独立分析 | 见"§6.1 插入点唯一性"一节 |
| TASK-014 验收量第三次换成"与 F 相等"而非计数 | ✅ 逻辑自洽, 对位移/spike产出免疫 | 已复核推理链, 未发现反例 |
| SC-M14 (UnicodeDecodeError) 补编号 + `_run_with_retry` 缺口 4 条 | ✅ 闭合且证据可核 | `aether.py:173/180` 实读确认 `text=True` + 只捕 `TimeoutExpired`；`path_coverage.py:78-101` 实读确认 `(TimeoutExpired, FileNotFoundError, OSError)` 元组precedent 真实存在 |
| `resolve_ci_backend`/`no_ci_fallback` 消费点行号 (:337/:339) | ✅ 属实 | 逐行核对一致 |

**§6.1 插入点唯一性 —— 独立分析 (本席位重点)**:

`:328`(enabled 早退) → `:337`(resolve_ci_backend) 之间插入 legacy-key 硬失败,
`:345`(precheck 失败早退) → `:356`(path coverage) 之间插入分支存在性核验 —— 两者是函数体内
**不重叠的两段区间**, 顺序为 enabled 检查 → [legacy-key 检查] → resolve_ci_backend → no-backend
早退 → precheck → [存在性核验] → path coverage → in-flight 查询。用三条穷举组合验证:
`enabled=false+legacy` 走不到任一新检查 (最先返回); `enabled=true+legacy+无backend` 会在
legacy 检查处提前 fail (不会掉进 `_no_ci_output` 用翻译后的默认值悄悄放行); `enabled=true+
legacy+backend正常` 会在 legacy 检查提前 fail (不会走到存在性核验)。**三条 fixture 确实能唯一
判别"检查放错位置"的两种错误实现** (放进 `_normalize_config` / 放到三早退之后), 我未能构造出
第三个能通过全部三条 fixture 但插入点仍错误的实现。**判定该插入点声明为唯一确定, 与 D9/§6/
SC-M10 不冲突。**

---

## Finding 1 (Major, 本轮新发现) — TASK-020 自己的删除面里, 4/5 个文件没有机械 SC, 只有 config-loader 一个有

**定位**: `proposal.md` §Rule #6 / SC-M17 (`:301`) · `tasks.md:116-119`(TASK-020) ·
`detailed-tasks.yaml:739-802`(TASK-020 verification) 对照
`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:68,:70,:71,:79,:82,:85,:89,:116`。

**实读证据 — 逐文件今日的"键名面/承诺措辞面"计数, TASK-020 verification 自己列出的**:
```
pre_merge_gate.py 6/2 · phase-c-integrator/SKILL.md 6/4 · config-loader/SKILL.md 2/2 ·
test_pre_merge_gate.py 17/3 · .aria/config.template.json 2/0
```

**实跑, 我本人复核这两个数字 (承诺措辞面, pre_merge_gate.py)**:
```
$ grep -nE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' \
    aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
68:# Old keys still readable until v2.0; new key wins on conflict (Hard #9).
116:                    f"will be removed in v2.0",
```
= 2 行, 与 TASK-020 verification 自陈完全一致。

**关键缺口**: 通篇 `proposal.md`/`tasks.md`/`detailed-tasks.yaml` 中, **只有 config-loader/SKILL.md**
这一个文件的"承诺措辞面"被提升为一条真正的机械 SC (**SC-M17**, `2 → 0`, 由 TASK-001 建红窗、
TASK-020 转绿、TASK-021 终局复核), 且这条 SC 本身还带着一段明确的方法论旁白:
> `proposal.md:300` "无编号即不被任何机械勾稽点找到, 只能靠人工读散文" (原话讲的是 SC-M14, 但
> 同一句道理适用于本 finding)。

而**同一个 TASK-020、同一份"删除面跨两个仓 5 个文件两个 key"枚举里的另外 4 个文件**
(`pre_merge_gate.py` 自己 · `phase-c-integrator/SKILL.md` · `test_pre_merge_gate.py` ·
`.aria/config.template.json`) —— 只有**散文描述今日计数**, **没有任何 SC 编号要求它们落地后
变成什么值**。我逐条搜索确认:
```
$ grep -n "removed in v2\.0\|still (readable\|仍读\|v2\.0 移除" tasks.md detailed-tasks.yaml proposal.md
```
命中的全部 8 处引用中, 除 SC-M17 本身及其在 TASK-015/TASK-019/TASK-021 里的重复提及外,
**没有一处**是"pre_merge_gate.py 的这两行须归零"的机械断言 —— 全部是描述性散文
("逐文件今日实测…" / "早先清单只列 6 行, 漏了 :349" 这类**枚举完整性**校正, 不是**归零目标**校正)。

**为什么会红 (可证伪, 已构造反例路径)**:

一个完全按 TASK-020 现有文字实现的方案可以是: (a) 在 `:328`~`:337` 之间新增一段独立检查,
直接读**原始** `config` 参数 (未经 `_normalize_config` 翻译) 判断是否含 `primitive_preference`/
`no_aether_fallback`, 命中即 `return _build_output(verdict=FAIL, raw_message=...)`; (b) **完全不碰
`_normalize_config()` 函数体**——它继续在 `:325` 无条件执行, 继续做"翻译 + `warnings.warn(...will
be removed in v2.0...)`"这套软降级逻辑, 只是它的**产出此后被 (a) 新检查判定为非法而整体丢弃**;
(c) 把三个 `test_old_key_*` 单测**改写为**调用 `gate_check(...)` 断言 `verdict=="fail"` (而不再直接
调 `_normalize_config()` 断言翻译成功), 满足"由翻译成功改为断言硬失败"的测试面要求。

在这个实现下:
- SC-M10(a)(b) 两条 fixture 全过 (enabled=false 先于任何新检查返回);
- 三条插入点判别 fixture (i)(ii)(iii) 全过 (新检查在 `resolve_ci_backend` 前拦截);
- CLI 真实路径用例过 (`_build_output` 走正常六键输出);
- 三个改写后的 `test_old_key_*` 过 (它们不再断言 `_normalize_config` 的输出/warning 文本);
- **SC-M17 过**(它只查 `config-loader/SKILL.md`, 跟 `pre_merge_gate.py` 无关);
- TASK-021 的"SC-M1…SC-M17 全部为期望值"过 (17 条编号 SC 里根本不含这个量)。

**但** `pre_merge_gate.py:68` 和 `:116` 的"will be removed in v2.0"文本 100% 原样留在已发布的
v2.0.0 代码里, 且 `_normalize_config()` 每次遇到 legacy key 仍会真的执行一次翻译 + 发一次
`DeprecationWarning`(只是其产出随后被丢弃)—— 这与 TASK-020 的**存在理由本身**
("`will be removed in v2.0` 这句承诺到期, 必须兑现") 直接矛盾, 却**没有任何机械信号会变红**。

**与本轮核心问题的关系**: 这正是 SC-M17 本身想解决的那个类的**同一个类**, 只是 SC-M17 在
config-loader 这一个实例上做对了 (proposal §Rule #6 明确把它包装成"另一个 skill 需要独立
Rule #6 归档"的理由), 但**没有意识到它的姊妹缺口就长在 TASK-020 自己主战场的那两个文件里**
——本 change 全篇反复出现的"只修实例不修类"形状, 这次落在了它自己刚发明的补救机制身上。

**建议**: 参照 SC-M17 的模板, 至少给 `pre_merge_gate.py` 补一条独立 SC (例如 SC-M18):
`grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' pre_merge_gate.py` 由 2 → 0,
owning task = TASK-020, 红窗建在 TASK-001。`phase-c-integrator/SKILL.md`(4 行)、
`.aria/config.template.json`(承诺面 0, 键名面 2→0)两处同理, 至少各需一条可核验的 grep 断言,
或明确注明"这些文件只删键名不删承诺措辞, 因此保留是有意为之"(若真是有意为之, 也应写清楚为什么
`config-loader` 与 `pre_merge_gate.py` 待遇不同)。`test_pre_merge_gate.py` 17/3 中的 3 处
"承诺措辞面"若不在断言重写时一并核实清空, 同样会静默留存。

**严重度评级理由**: Major 而非 Critical —— 它不影响 Rule #8 gate 本身的行为正确性 (fail-closed
机制真的会 fail-closed, 三条插入点判别 fixture 真的能把两种错位置的实现打红), 只是让一个"版本
承诺已到期"的陈述性文本在 v2.0.0 里继续说谎, 且**机械上完全检测不到**——按本 Spec 自己的标准
(SC 表抬头"零裁量" / D8 诊断信息主通道原则 / SC-M17 存在的理由), 这类"文本层面的失信而无红灯"
正是本 Spec 治理哲学要消灭的东西, 值得在进入 TASK-020 实施前补上, 但不阻塞 TG-0~TG-2 的开工。

---

## 那道机械检查 (xcheck.py) 真的有效吗

### 1. 四项判据覆盖得住 R2 的两个形状吗?

**部分覆盖, 且覆盖方式本身脆弱**。

- **CHECK1 (DAG vs 点名对象)**: 我做了一次真实变异测试 (方法见下), 它**确实抓住了**一次
  "移交给没核过的下游"式的依赖边缺失。但它的抓取机制是**正则匹配裸字符串 `TASK-\d{3}`**——
  本文件里"依赖补边"类的说明句常用**紧凑数字枚举**写法 (例如 TASK-020 的"本任务与
  006/007/008/009 同改 pre_merge_gate.py"), 这种写法**不会被正则命中**。这次之所以仍被
  CHECK1 抓到, 是因为 TASK-008/TASK-020 在 SC-M10 交叉输入那句里**恰好**各自额外用了一次
  完整的"TASK-020"/"TASK-008"字面量(为了叙述 SC-M10 的归属关系, 并非为了服务这项机械检查)
  ——这是**巧合覆盖**, 不是 CHECK1 结构性保证的覆盖。若某处只用紧凑数字枚举而没有这层巧合的
  完整字面量, CHECK1 会对同类缺口保持沉默。
- **CHECK2 (SC 是否交付测试文件)**: 完全覆盖不到 Finding 1 这个形状——它的 `SCS` 集合**逐字
  取自 proposal SC 表已有的行**(`re.findall(r"^\|\s*\*\*(SC-M\d+[a-c]?)\*\*\s*\|", ...)`),
  结构上**不可能**发现"一个描述性要求从未被赋予 SC 编号"这件事, 因为它的搜索空间本身就是
  "已经注册过的 SC", 不是"应该存在但还没注册的 SC"。这正是本 finding 能存活的根本原因。

### 2. 有没有恒绿的判据?

**CHECK2 对"缺 SC 编号"这整个类别是结构性恒绿**——不是"当前输入下凑巧不报", 而是它的判据
公式(`SC ∈ proposal 表 → 查 owner`)在**任何**"要求写在散文里但没给编号"的输入下都不可能触发,
因为不存在的 key 不会进入被迭代的集合。这不是"这次没测到", 是**这道检查的设计边界本来就画在
"已注册 SC 集合"内部**, 对集合外的缺口无感。Finding 1 是这条恒绿判据的一个真实、当场可复现的实例
(实跑 `xcheck.py` 于committed 状态返回 `RESULT: PASS`, 而 Finding 1 描述的缺口彼时已经在场)。

### 3. xcheck.py 自己是不是一个"只修实例不修类"的产物?

**是**。三个例子:

- **CHECK4 完全硬编码**——`INSERT` 字典和 `need`/后续两个列表里的每一条 key/pattern 都是
  R2 那一次具体发现的 D9/§6/§6.1 冲突量身定做的字面量 (`"resolve_ci_backend(cfg)\` 之前"`、
  `"两节不得互相援引"` 等)。它验证的是"那次已发现的冲突的修复文字还在不在", **不是**"当前文档里
  是否存在任何插入点被多条条款同时管辖"的通用检测。若 Phase B 实施或未来某轮再给 `gate_check()`
  加第三个新插入点 (哪怕位置与已有两个都冲突), CHECK4 不会报警——它没有对"新插入点"的通用解析,
  只会去查那几条写死的字符串在不在。
- **CHECK1 对紧凑数字枚举失明**(上面已证明), 是"这轮撞到的具体写法被覆盖, 同族的紧凑枚举写法
  没被覆盖"的直接例子。
- **CHECK2 只查『表里已有的 SC』**, 是"覆盖了『SC 存在但 owner 缺失』这个子类, 没覆盖『SC 应该
  存在但压根没被造出来』这个更早的子类"——这正是本 Finding 1 的形状, 也是 R2 处方原文
  ("失效集中在只修实例不修类") 精确预言过、但这道补救检查自己又落入的坑。

### 4. 拒绝能力实测 (改一处再跑)

用**未改动仓内任何真实文件**的方式, 复制三份文档到 scratch 目录后做了两处受控变异:

**变异 A** (验证 CHECK1 的正向抓取能力): 从 `TASK-020.dependencies` 删除 `TASK-009`
(切断"TASK-020 → TASK-009 → TASK-008"这条唯一的传递路径)。
```
$ python3 xcheck.py .   # 变异后
RESULT: FAIL (2)
  - CHECK1: TASK-008 的 verification 点名 TASK-020 但两者无依赖序
  - CHECK1: TASK-020 的 verification 点名 TASK-008 但两者无依赖序
```
**CHECK1 确实抓住了**——证明它不是完全无用的检查, 对"依赖边被删掉、但散文里仍留着完整
`TASK-XXX` 字面量互指"这种情况有真实检测力。

**变异 B** (验证 CHECK2 的边界, 与代码走读一致, 未做独立重跑——因为其恒绿性由代码结构本身
即可证明, 不需要变异实验: `SCS` 变量的赋值语句本身决定了它不可能包含未注册的编号, 这是一个
数学事实而非需要经验验证的行为)。

### 综合评估

xcheck.py **不是**橡皮图章——CHECK1 在有巧合覆盖时能抓真实回归, CHECK3 的位移护栏检查(正则
扫 `:NNN` + 要求同任务出现"内容锚"字样)对本文档目前的用法是有效的。但它是**四个针对性很强、
覆盖面很窄的正则/集合检查**, 不是通用不变量验证器——它的价值应被理解为"R2 那两个具体形状的
回归测试", 而不是"能防住同类新缺陷的通用机制"。Finding 1 是这个边界的一个真实实例: 一个新的
"只修实例不修类"缺口, 就诞生在 xcheck 首次投入使用的**同一轮**, 且不在它的检测范围内。

---

## 阻塞项

1. **Finding 1** —— TASK-020 需为 `pre_merge_gate.py`(自身)/`phase-c-integrator/SKILL.md`/
   `test_pre_merge_gate.py`/`.aria/config.template.json` 四个文件的"承诺措辞面"补机械 SC
   (参照 SC-M17 模板), 或显式论证为何只有 config-loader 需要。建议在 TASK-020 进入实施前解决,
   不阻塞 TG-0~TG-2 开工。

无发现推翻本 Spec 三条承重腿或 §6/§6.1 插入点设计本身; R2 的 1 Critical 确认闭合, 抽样的 Major
条目确认闭合。
