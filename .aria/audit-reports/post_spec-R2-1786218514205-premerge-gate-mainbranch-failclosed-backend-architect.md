---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T20:18:58.339Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — backend-architect 审计报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md`(387 行, R1-fix 结构性重写版)。
镜头: 实现可行性与接口契约 —— §3 两级解析 / §5 exit-code 判据表 / §6 重试规范复用 / §7-§8 additive 键与消费点。

**方法论**: 未采信 Spec 正文对命令行为的陈述, 对 §3/§5 的全部 git 命令在本仓 (`/home/dev/Aria`, 真实 origin+github 双 remote) 与 `/tmp` 受控临时仓 (裸仓, 可操纵 HEAD) 中实跑; 对 §6/§7/§8 的消费点声明逐一去源码核对函数签名与调用点行号。

---

## 审计结论

本轮新写内容 (§3-§8 全部为 R1-fix 重写产物) 里, **两级分支解析机制自身的权威路径存在未覆盖的成功态-但-不可解析输出**(实测复现, 非推测), 且 §5/§6 的重试语义与 §8 的字段在场范围表都存在与其自引用源相矛盾的欠定。这些都命中被授权指出的"fix 轮最易在新写内容里复发同形状缺陷"模式 —— 具体说: R1 已经在治"某条件判定表没覆盖所有情形"(C1/M2/M5/M6 等), 但 R1-fix 新写的判定表本身又在更细粒度上重犯同一形状(表格穷举声称完备, 实测/源码核对后不完备)。

判定 **FAIL**(≥1 Critical)。

---

## Verdict

**FAIL** — 1 Critical + 4 Major + 2 Minor。

---

## 轮次记录

- R1: 5 席 5/5 REVISE, FAIL (5C+10M+6m)。owner 裁定结构性重写 §What Changes/§决策记录/§Success Criteria/§Impact 四节。
- R2 (本轮, backend-architect 单席): 聚焦重写后内容自身的实现可行性与接口契约, 4 个指定镜头全部深挖 + 实跑验证。发现 1 Critical (§3 权威路径解析盲区) + 4 Major (§4 失败信令欠定 / §5-§6 重试语义自相矛盾 / §5 exit-code 表对 glob pattern 语义的隐藏假设 / §8 在场范围表非穷举)。

---

## 已验证成立的部分(positive controls, 简述)

以下 Spec 陈述经实跑/源码核对确认准确, 不构成 finding, 仅记录方法论上"我确实查过"(避免只报坏消息造成幸存者偏差):

- §Why "两者返回完全同形" / AetherBackend 无法区分「分支不存在」vs「无 in-flight」: 源码核对 `aether.py:121-135` 确认 `main_runs_raw = data.get("runs") or []` 对两种情形产出同一 `InFlightStatus(runs=[])`。
- §Why "main 分支名错时 (a) 腿更保守不是变绿": 实跑 `git diff --name-only --no-renames main...HEAD` → RC=128; `master...HEAD` → RC=0。与陈述逐字一致。
- §2 "origin/HEAD 是 symbolic ref, github/HEAD 不是": 实跑 `git symbolic-ref refs/remotes/origin/HEAD`(RC=0, `refs/remotes/origin/master`)与 `git symbolic-ref refs/remotes/github/HEAD`(RC=128, `fatal: ref ... is not a symbolic ref`)双双确认。
- §5 exit-code 基本语义: `git ls-remote --exit-code --heads origin master` → RC=0; `origin main` → RC=2; `origin totally-bogus-branch-xyz123` → RC=2。核心 0/2 二分准确。
- §8 "`gate_state_helper.write_gate_state()` 与 `workflow-state-schema.md` 均无 `main_branch_resolved` 字段位置": 源码核对 `write_gate_state()` 具名参数(`name/verdict/in_flight_runs/primitive_used/raw_message/intervals`)与 `workflow-state-schema.md:38-54` 的 `gate_state` schema 均确认无此字段。Spec 自陈准确。
- Impact 表 "SKILL.md:243 与 :167 的 `--branch main` 字面量": grep 全文件确认仅此两处, 无遗漏第三处同形字面量; `pre_merge_gate.py` 的三处(`:21/:300/:427`)与 §1 表逐一对应。
- Impact "既有测试 24 处 `gate_check(` 调用, 显式传 `main_branch` 0 处; `test_sc12` 断言 `main_branch="main"`": grep 确认 24/0/1(且该 1 处是 `test_sc12` 对 `evaluate_path_coverage` 的断言, 非 `gate_check` 调用)。
- Impact "`test_sc22` patch 的是 `path_coverage` 模块的 `subprocess`, 非 `pre_merge_gate` 自己的": 源码确认 `pre_merge_gate.py` 当前**没有** `import subprocess`(本 Spec 是该模块第一次引入 subprocess 调用), `test_sc22` 精确 patch `pc_module.subprocess.run`。Spec 自陈准确, 且已在 Impact 段给出 Phase B 处置(扩 `_ProbeCacheResetMixin` 覆盖 `_resolve_main_branch`/`_verify_branch_exists`)——检查该处置对所有会触发 `gate_check` 的测试类均适用(`GateCheckTests`/`FallbackTests`/`TestGHAStubAbortNotSkip`/`TestAliasKeyPath`/`TestBothKeysPresentNewWins`/`TestBackendRegistry`/`TestNormalizeConfigSequencing`/`TestProbeCacheIsolation`/`PathCoverageGateTests` 均继承 `_ProbeCacheResetMixin`), 处置方案本身可行。

---

## Findings

### [CRITICAL] §3 权威路径 `ls-remote --symref` 存在 "RC=0 但无 `ref:` 行" 的两种实测边界态, Spec 未覆盖

**scope**: proposal.md §3(117-127 行), 特别是步骤 2("权威路径...解析 `ref: refs/heads/<name>\tHEAD`")与步骤 3("两者均失败 ⇒ abort")。

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:119-127`

Spec 把 `_resolve_main_branch` 的判定框成二元: 步骤 2 命令要么"给出可解析的 `ref:` 行"要么"失败"(与步骤 3 的"两者均失败"呼应, 隐含"失败"= 非零退出码)。但 `git ls-remote --symref` 的真实输出空间是三态, 其中两态是 **RC=0 但没有 `ref:` 行**, 用受控裸仓实测复现(在 `/tmp` 建裸仓操纵 HEAD 文件, 非推测):

```
# 场景 A: 远端 HEAD 是 detached(直接写 SHA 到裸仓 HEAD 文件, 而非 symbolic ref)
$ echo 50a2c92f77816f576db2fb1710bf45c49ed32b17 > remote.git/HEAD
$ git ls-remote --symref origin HEAD
50a2c92f77816f576db2fb1710bf45c49ed32b17	HEAD
RC=0                                          ← 无 "ref:" 前缀行, 只有一行 SHA+HEAD

# 场景 B: 远端是全新裸仓, 从未 push 过(unborn HEAD)
$ git init --bare empty-remote.git
$ cat empty-remote.git/HEAD
ref: refs/heads/master
$ git ls-remote --symref empty-remote.git HEAD
(完全空输出)
RC=0                                          ← 空 stdout, 连一行都没有
```

两种情形 RC 都是 **0**(git 认为查询本身成功), 但都不含 Spec 步骤 2 要解析的 `ref: refs/heads/<name>\tHEAD` 格式。Spec 步骤 3 的"两者均失败 ⇒ abort"只在"非零退出码"意义上是完备的判定, 对这两种"成功态但不可解析"的输出**没有规定行为**。

按 Spec 文字直接实现的典型代码(`out.splitlines()[0]` 取首行, 或 `line.split("ref: refs/heads/")[1]` 提取分支名)在场景 A 会因子串不存在而 `IndexError`, 在场景 B 会因空列表取索引而 `IndexError` —— 这是**未捕获的 Python 异常**, 不是 Spec 承诺的 `verdict=fail` + `gate_error.kind="main-branch-unresolved"` 结构化输出。这直接违反本 Spec 自己的硬约束"⛔ 不得回落任何字面缺省"的精神延伸——不是回落到错误值, 而是根本不产出 `pre_merge_gate.py` 自身文档承诺的"Output: single JSON line on stdout... Exit code: 0 = success (any verdict)"契约(`pre_merge_gate.py:23-24`), 把原本"恒绿但至少是良构 JSON"的旧缺陷换成了"硬崩溃, 调用方(workflow-runner)拿不到任何可解析输出"的新缺陷, 且发生在这个 Spec 专门新增来堵漏洞的"权威路径" fallback 上(R1 m6 新增, 为了防止只用本地 `symbolic-ref` 在无该 ref 的容器里恒红)。

场景 A(detached remote HEAD)并非纯理论: 本仓的 `github` remote 就已经缺少本地 `refs/remotes/github/HEAD` symbolic ref(已在"已验证成立"部分证实), 促使 Spec 设计了权威路径兜底; 但没有进一步验证权威路径自身在**远端** HEAD 本身处于非常规状态时(迁移、手工重建、镜像同步中断等)的行为。场景 B(unborn remote)在 CI/沙箱环境新建的镜像 remote 或测试 fixture 中是常见状态。

**两个独立实现者会得到不同结果**: 一个可能让代码在此崩溃(违反契约); 另一个可能防御性地写 `if len(lines) < 2 or "ref:" not in lines[0]: treat as failure`(需要额外发明这条校验, Spec 未言明); 第三个可能误把裸 SHA 当分支名向下传递(`main_branch = "50a2c92f..."`), 依赖后续 `_verify_branch_exists` 侥幸兜底成"not-found"(诊断信息却指向错误方向: 报"分支 `50a2c92f...` 不存在", 而非"HEAD 解析失败")。

**introduced_by_r1fix**: true — 权威路径本身是 R1 新增（m6 恒红对偶修复), 这个边界态是新增内容自身的缺陷, 非对 R1 前版本的复核。

---

### [MAJOR] §4 `_resolve_main_branch` 的失败信令机制自相矛盾("抛/返回"未择一), 且与相邻 `_verify_branch_exists` 的隐含约定不一致

**anchor**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:142-143`

```python
main_branch, resolved_from = _resolve_main_branch(main_branch, remote)   # 失败 → 抛/返回 error 输出
_verify_branch_exists(remote, main_branch)                               # §5
```

第 142 行注释"失败 → **抛/返回** error 输出"用"/"并列了两种结构上互斥的错误传播机制(raise exception vs. return 一个错误值), 未择一。而同一行的赋值语法 `main_branch, resolved_from = _resolve_main_branch(...)` 隐含"该调用总是成功返回一个 2-tuple"(否则 tuple-unpack 本身就会在失败路径上抛 `TypeError`/`ValueError`, 与"返回 error 输出"的读法冲突) —— 这意味着"返回"分支在字面代码里根本没有合法的落点, 唯一自洽的读法是"失败必须靠 raise", 但注释仍然明文保留了"返回"选项, 造成协议层面的自相矛盾。

第 143 行 `_verify_branch_exists(remote, main_branch)` 更进一步: 调用结果**完全没有被赋值捕获**, 说明它传播失败的唯一可能方式是 raise —— 但如果这是既定约定, 为什么 142 行还要用"抛/返回"这种模棱两可的措辞, 而不是像 143 行一样明确用"仅抛"?两个相邻、同类职责(都是"main branch 解析/校验失败即阻断")的函数在同一份代码块里被赋予了不一致(至少是表述不一致)的失败传播约定。

这正命中本 Spec 自陈的判据"两个独立实现者读本节应得同一结果"——按当前文字, 实现者 A 会为 `_resolve_main_branch` 定义一个自定义异常(如 `MainBranchResolutionError`)并在 `gate_check` 里 `try/except` 捕获后构造 `gate_error` 输出; 实现者 B 会让 `_resolve_main_branch` 返回 `(None, "unresolved")` 之类的哨兵值, 在 `gate_check` 里 `if main_branch is None: return _build_output(...)`。这两种实现在函数签名、单元测试的 mock 方式(`side_effect=Exception` vs `return_value=(None, ...)`, 直接影响 Impact 段要求扩展的 `_ProbeCacheResetMixin` 打桩形态)、以及 `_resolve_main_branch`/`_verify_branch_exists` 能否被同一套 mock 机制统一打桩上都会产生分叉。

**introduced_by_r1fix**: true — §4 插入点代码块是 R1-fix 新写(R1 M5 的处置产物)。

---

### [MAJOR] §5/§6 重试触发条件自相矛盾: §5 判据表说"其他非零 / timeout"都按 §6 重试, 但 §6 引用的既有规范(及其源码先例)只在 timeout 触发时重试

**anchor**: proposal.md §5 判据表第 3 行(约 165 行)vs §6(173-183 行)+ `ci_backends/aether.py:164-187`

§5 判据表原文(第 3 行):
> 其他非零 / timeout → 查询失败 → **按 §6 重试**; 重试耗尽 ⇒ `verdict=fail` + `gate_error.kind="main-branch-verify-failed"`。⛔ 不得当成「存在」也不得当成「不存在」

§6 引用"`SKILL.md:257-259` 已成文 subprocess 调用规范": "timeout 触发 → max 3 attempts retry"——**只提 timeout 触发重试**, 未提"其他非零退出码"触发重试。实读该规范的唯一现存实现先例 `ci_backends/aether.py::AetherBackend._run_with_retry`(164-187 行), 逻辑是:

```python
for attempt in range(MAX_RETRY_ATTEMPTS):
    try:
        result = subprocess.run(..., timeout=self.timeout)
        return result.returncode, result.stdout or "", result.stderr or ""   # 只要进程跑完就立即返回, 不管 returncode
    except subprocess.TimeoutExpired as exc:
        ...retry...
```

`subprocess.run` 一旦在 `timeout` 内跑完(无论 exit code 是 0、128 还是其他), 函数**立即 return**, 循环体里唯一能触发下一次 `for` 迭代(=重试)的路径是 `except subprocess.TimeoutExpired`。也就是说: 一个"瞬间返回非零"(如 DNS 失败、认证失败、remote 不存在——这些 git 通常几百毫秒内就以非零 RC 报错, 根本不会撞到 `timeout`)在这份"既有规范"的实际语义下 **不会重试**, 会被当作单次失败直接向上冒泡。

§5 却把"其他非零"和"timeout"并列送进同一个"按 §6 重试"桶。二者只有一个能在"既有规范"下成立。这是**同一版本(R1-fix)新写的两节之间的直接矛盾**, 恰好落在本 Spec 明确要求 R2 复核的"是否真落在适用面内"这个问题上——答案是: 部分落在(timeout 触发 3 次重试确实可复用), 部分不落在(非 timeout 的即时非零退出码没有对应的重试先例, `§5` 却声称它有)。

两个独立实现者的分叉点: 一个严格照抄 `_run_with_retry` 的判别式(`except TimeoutExpired` 才重试), 网络瞬时故障(非 timeout 类)会立即变成 `main-branch-verify-failed`, 不给重试机会, 与 §5 文字承诺不符; 另一个严格照抄 §5 的文字("其他非零...按 §6 重试"), 会为"非零退出码"也套上 3 次重试循环, 这是在 SKILL.md:257-259 之外**新发明的重试触发条件**, 与 D-G"不新造参数"的决策初衷(仓内已有三套口径, 不要再造第四套)相悖(触发条件本身也是"口径"的一部分, 不只是"参数")。

**附带的次级 gap(同一节, 一并报告以免二次开单)**: `SKILL.md:257-259` 的"复用"实际上是被 `primitive_call_timeout_seconds` 这个**配置值**参数化的(`_instantiate()` 把它喂给 `AetherBackend(timeout=...)`)。但 §4 给出的函数签名 `_resolve_main_branch(main_branch, remote)` / `_verify_branch_exists(remote, main_branch)` 都**没有 `cfg`/`timeout` 形参**——如果两个新 subprocess 真要"沿用"这个可配置的 timeout, 需要一条从 `gate_check` 内的 `cfg` 到这两个函数的传参路径, 但 Spec 未展示。两个实现者会分叉: 硬编码 30(丢失可配置性, 事实上"违反"了复用声明) vs. 悄悄给函数签名多加一个未在 §4 提及的参数。

**introduced_by_r1fix**: true — §5/§6 均为 R1-fix 全新写作内容(R1 M1/M6 的处置产物)。

---

### [MAJOR] §5 exit-code 判据表隐含"字面精确匹配"假设, 但 `git ls-remote --heads` 的 pattern 实为 glob 语义 —— 存在能让「不存在的分支被判为存在」的输入

**anchor**: proposal.md §5(153-167 行), 尤其"exit 0 → 存在 → 继续原流程"这一行

Spec 把 `git ls-remote --exit-code --heads <remote> <main_branch>` 的 RC=0 无条件等同于"`<main_branch>` 这个分支存在"。实测这不成立——`<main_branch>` 位置是**glob pattern**, 不是字面 ref 名精确匹配:

```
$ git ls-remote --exit-code --heads origin '*'
80c961d5...  refs/heads/aria/DEMO-001
...(本仓全部 heads)...
71bdd60f...  refs/heads/master
RC=0                                    ← "*" 匹配了仓内每一个分支, RC=0

$ git ls-remote --exit-code --heads origin 'mast??'
71bdd60f...  refs/heads/master
RC=0                                    ← "?" 通配符命中 master

# 对照: 非 glob 字符的子串/前缀不会误匹配(排除了"更普遍的假阳性"担忧, 精确定位到 glob 元字符)
$ git ls-remote --exit-code --heads origin 'aster'   # master 的子串
RC=2
$ git ls-remote --exit-code --heads origin 'mast'    # master 的前缀
RC=2
```

即: 若 `main_branch` 的值里含有 `*`/`?`/`[...]` 等 glob 元字符, `_verify_branch_exists` 会把"没有任何分支字面等于这个字符串"的情形误判为"存在"(RC=0), 这正是 Spec 自己在判据表旁点名要防的方向——"⛔ 不得当成「存在」"——却在这一类输入上恰好失手。

**触达路径**: git 的 `check-ref-format` 规则本身禁止合法分支名包含 `*`/`?`/`[`, 所以 §3 的两级**解析**路径(从 `symbolic-ref`/`ls-remote --symref` 输出中提取的名字)不可能产出含 glob 字符的值, 这条路不受影响。但 SC-3/SC-4 覆盖的**显式传参路径**(`--main-branch <值>`)不受此约束——`argparse` 只是把命令行字符串原样传入, 一个操作者在无引号 shell 里敲 `--main-branch *`(且当前目录下没有匹配文件, bash 默认不启用 nullglob 时会把未展开的字面 `*` 原样传给程序)、或某个上游脚本拼接失误传入空/通配符值, 都会让本该走"main-branch-not-found"判定的输入被判定为"存在"而继续往下走, 违背本 Spec 存在的初衷(这正是 SC-4 想守住但没能覆盖到的输入类)。

**introduced_by_r1fix**: true — §5 整节含 exit-code 判据表是 R1 新增(M6 处置产物), SC-4 也是 R1-fix 新写。

---

### [MAJOR] §8 `main_branch_resolved` 在场范围表非穷举, 且与其自引用的 SKILL.md:279 契约自相矛盾 —— 遗漏"backend query 失败"这个既有第四分支

**anchor**: proposal.md §8(212-226 行) vs `pre_merge_gate.py:369-376` + `:392-399`

§8 开篇原文自己先引用了既有契约:

> `SKILL.md:279` 成文契约: 「各早退分支(**no-backend / precheck 失败 / backend query 失败 / enabled:false**)保持六键不变」

——这里明确点名了**四个**早退分支, 其中 "backend query 失败" 是第四个。但紧接着的分类表只覆盖了三组:

| 输出分支 | `main_branch_resolved` 在场? |
|---|---|
| `enabled=false` / no-backend / precheck 失败 | 否 |
| §3 解析失败 / §5 核验失败(新 error 路径) | 是 |
| 走到 `compute_verdict` 的最终路径(green/wait/fail) | 是 |

"backend query 失败"在表里**完全没有出现**——既不在第一行(它没被列进"enabled=false / no-backend / precheck 失败"的枚举), 也不在第二行(它不是 §3/§5 的新 error 路径), 也不在第三行(它不经过 `compute_verdict`)。这是 Spec 在同一节内, 先自己引用了一个四分支契约, 再自己写了一张三分支表——表本身对自己引用的契约都不是穷举的。

源码核实"backend query 失败"具体指哪里、以及它相对本 Spec 新插入的解析点在时序上处于什么位置: `pre_merge_gate.py:365-376`(main in-flight 查询)与 `:388-399`(PR CI 查询)各有一个 `except AetherQueryError` 分支, 直接调 `_build_output(verdict=VERDICT_FAIL, ...)`(不经过 `compute_verdict`, 也不传 `path_coverage=`, 与 #122 先例"该分支不带 `path_coverage`键"一致)。关键是: 按本 Spec §4 的解析点插入位置(三个早退**之后**、`evaluate_path_coverage` **之前**), 这两个 `AetherQueryError` 分支执行时, `main_branch` **已经成功解析完毕**(否则更早的 §3/§5 步骤就会先行 abort)——即"该往哪填"的信息在那一刻是齐备的、真实的, 不存在"写入即撒谎"的顾虑(这正是 §8 给第一行"否"定的理由, 但那个理由对这两个分支不成立, 因为它们发生在解析点**之后**)。

两种同样站得住脚但互斥的推断都能从 Spec 现有文字导出: (a) 类比 `path_coverage` 键在这两个分支里被排除的既有先例, 推出 `main_branch_resolved` 也该排除; (b) 按 §8 自己反复强调的 D-E"可观测性目标"("这正是最需要可见的路径"), 推出恰恰应该在场——因为如果 main 分支已解析成功之后 CI 查询才失败, 运维人员想知道"至少 main 分支解析对了", 省得排查方向被引导去查分支名。Spec 没有明确二选一, 两个独立实现者会在这一点分道扬镳, 且 `_build_output()` 的签名要不要新增 `main_branch_resolved` 形参、这两个既有调用点(:370-376/:393-399)要不要改动, 直接取决于这个悬而未决的选择。

**introduced_by_r1fix**: true — §8 整节是 R1-fix 新写(R1 M2 处置产物), 且是本轮被 Spec 自己点名重点复核的对象之一("R2 请优先验...(a) §4 的解析点是否真的同时满足三个早退与 path_coverage 两侧约束")——本 finding 正是该自陈风险点在 §8 侧的具体化。

---

### [MINOR] gate verdict 词表({green,wait,fail})与 gate_state status 词表({waiting,green,fail})不是同一个词表 —— "wait" ≠ "waiting"

**anchor**: `pre_merge_gate.py:47-49`(`VERDICT_GREEN/WAIT/FAIL`)vs `gate_state_helper.py:32-34`(`GATE_STATUS_WAITING/GREEN/FAIL`)+ `workflow-state-schema.md:40`(`"status": "string (waiting | green | fail)"`)

按任务书要求专门核对这一点: 两张词表**不是同一张**——`pre_merge_gate.py` 的 `VERDICT_WAIT = "wait"`, 而 `gate_state_helper.py` 的 `GATE_STATUS_WAITING = "waiting"`, `workflow-state-schema.md:40` 也钉死 `waiting`。`gate_state_helper.tests/test_gate_state_helper.py` 里全部 `write_gate_state(..., verdict=...)` 调用都传字面 `"waiting"`(而非 `"wait"`), 印证了调用方(workflow-runner, 按其自身 docstring"markdown-driven, LLM caller handles state")被期望在把 pre_merge_gate 的 `wait` verdict 交给 `write_gate_state()` 之前, 先做一次 `"wait"→"waiting"` 的文本翻译, 但我在 `workflow-runner/SKILL.md` 里没找到这处翻译被显式写出的位置(`:313/:324/:389` 只是分别提到"phase-c-integrator 返回 verdict=wait"和"gate_state.status==waiting", 中间的映射关系是隐含的)。

**这不会破坏本 Spec 的 SC-8**: SC-8 断言只针对新 `gate_error` 路径, 而该路径的 verdict 恒为 `"fail"`——`"fail"` 在两张词表里字面相同, 不受"wait"≠"waiting"影响, SC-8 能如实通过。

**为什么仍报告(非阻塞, 定为 minor)**: 任务书明确要求核对这一点, 说明它是关注对象; 且这是一个**既有的、本 Spec 未触碰但也未提及**的潜在缺口——若日后有人以为"本 Spec 已经把 gate verdict 与 gate_state status 的一致性钉死了"(容易望文生义, 因为 §7/§8 通篇在讲两套词表的收口), 可能误以为 wait 路径也已被覆盖。建议在 §Impact 的"already known 不同步面"清单里追加一句澄清, 明确"wait/waiting 翻译层不在本 Spec 范围内, 且本 Spec 不改变其现状", 避免 Phase B/日后读者的范围误解。不阻塞本轮收敛。

**introduced_by_r1fix**: false — 该差异是既有代码库里早已存在的状态, 本 Spec 未修改、未引入, 只是被任务书点名要求核实。

---

### [MINOR] §4 代码片段的行号锚点有一处偏移: `:344` 实际指向 `backend.precheck()` 调用行, 而非其后的 `if not ok:`/`return` 判断-输出行

**anchor**: proposal.md §4(约 139 行)"`ok, err = backend.precheck(); if not ok: return _build_output(FAIL, ...) # :344`" vs `pre_merge_gate.py:344-352`

实读: `pre_merge_gate.py:344` 是 `ok, precheck_err = backend.precheck()`(赋值行本身), 而该分支真正的判断与提前返回落在 `:345`(`if not ok:`)到 `:352`(`)`收尾)。同一代码块里另外两处锚点(`:328` 对应 `if not cfg["enabled"]:`、`:338` 对应 `if backend is None:`)都精确落在"判断行"上, 与其注释描述("← 解析之前"标注在判断-返回逻辑上)完全对齐; 唯独 `:344` 这一处比照同侪模式应指向 `:345` 或 `:346`, 实际指向的是判断之前的取值行。

鉴于本 Spec 通篇强调的核心卖点正是"编号 1..8, 每条钉到符号/行/字面量级"、"两个独立实现者读本节应得同一结果"这种行级精确性, 一处一行的锚点偏移本身不影响任何实现决策(读者仍能在附近一两行内定位到正确代码), 定为 minor、仅作记录, 不建议为此单独返工, 可在下次顺手改动该表格时一并订正。

**introduced_by_r1fix**: true — 该代码片段整体是 §4(R1-fix 新写, R1 M5 处置产物)的一部分。

---

## 给 Phase B 的建议(非 finding, 仅顺带记录, 供收敛后参考)

- Critical 项的最小修法: `_resolve_main_branch` 的权威路径解析必须显式判空/判缺 `ref:` 前缀(而不是盲目索引), 三态(可解析 / RC=0但不可解析 / RC非0)都要有对应分支, 且都要走同一个"构造 `gate_error` 输出"的出口, 不能让任何一态穿透到未捕获异常。
- Major #2(raise/return 二义)与 Major #3(重试触发条件矛盾)建议合并处理: 在 §4 明确 `_resolve_main_branch`/`_verify_branch_exists` 统一用同一种失败传播方式(建议 raise, 与 `_verify_branch_exists` 已隐含的约定一致), 并在 §6 明确重试循环只包裹"timeout 一种触发条件", 其余非零退出码直接终态化, 同时改写 §5 判据表第 3 行, 把"其他非零"从"按 §6 重试"里摘出来单独给一句话(例如"其他非零 → 立即 `main-branch-verify-failed`, 不重试")。
- Major #4(glob 语义)最小修法: 在把 `main_branch` 传给 `git ls-remote --heads` 前, 加一个字面校验(如用 `git check-ref-format --branch <name>` 或等价的白名单正则), 拒绝含 `*`/`?`/`[` 的输入, 直接判 `main-branch-not-found`(或新增 `main-branch-invalid-name` kind), 而不是把这类值送进 glob 语义的命令。
- Major #5(§8 表非穷举)最小修法: 在表格里显式加一行"backend query 失败(既有 `AetherQueryError` 分支, `:369-376`/`:392-399`)", 二选一写清楚(在场/不在场), 并说明与 `path_coverage` 既有先例是"保持一致"还是"有意分叉"。
