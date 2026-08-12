---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T17:10:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — Spec A `premerge-gate-branch-existence` — backend-architect

seat: backend-architect · vote: PASS (with warnings) · 0 Critical + 1 Major

视角: 实现可行性 (插入点 / 退出码分区是否穷尽 / 异常·重试·解码三轴 / 「纯 additive」的代码级复核)。

## 0. 方法

对 R2-fix (commit `017eb54`) 的每条新增段落逐条独立复核, 命令全部本轮重跑 (不采信 R2/commit message 的转述)。
四件事逐一回答: (1) R2 的 13M 是否真闭合; (2) R1-fix→R2-fix 的引入率; (3) 「兄弟位置清点」表的穷尽性;
(4) 执笔方的四条「不同意」与两条 owner 裁量项分类是否正确。

## 1. R2 的 13M+10m 闭合复核 (在我职责角度内的部分)

我重点核对了 R2 报告里落在我职责范围 (插入点/退出码/异常重试解码/additive代码级) 内的条目, 逐条独立复跑:

| R2 finding | 我的独立复核 | 闭合? |
|---|---|---|
| 我自己 R2 Major-1 (`UnicodeEncodeError` 在 `main()` 出口边界未被覆盖) | 本轮独立复现原始崩溃场景 + 独立验证补救 `s.encode("utf-8","replace").decode("utf-8")` 确实消除孤立代理码位、`sys.stdout.write` 不再抛异常 (见 §2 命令) | ✅ 真闭合, 且补救机制本身可用 |
| 我自己 R2 Major-2 (`SC-A-doc` 解析规则未定义) | 本轮独立按 R2 新增的「行首恰两个空格」正则重新提取 `SKILL.md:265-277`, 得到与 `_build_output` 完全一致的 7 键集合 (见 §2) | ✅ 真闭合, 正则本身正确 |
| tech-lead M-3 (`SC-A-cli`/`SC-A-cwd` 对 backend ambient 零安排, 无 aether/gh 的环境下恒红) | 独立读 `ci_backends/aether.py:62-69` 确认 `probe()=shutil.which("aether")`; R2-fix 新增的「可达前提」块把 `SC-A-cli`/`SC-A-cwd` 纳入「适用集 (10条)」, 要求 mock backend | ✅ 闭合, 分类正确 |
| tech-lead M-4 (`gate_error` 代码侧操作数未定义) | 独立读 `pre_merge_gate.py:232-263` 确认 `_build_output` 今日固定产 6 键 + 条件 `path_coverage`, 无 `gate_error` 形参; R2-fix 钉死「必须经 `_build_output` 产出」, 消除了「事后附加 vs 硬编码 doc 侧」的两难 | ✅ 闭合 |
| code-reviewer M-1 (§6「24 处全部触达」与 `SC-A10`/`A10b` 矛盾) | 独立重读 `test_pre_merge_gate.py:299-325` 与 `:521-530` 附近四处调用, 确认 `enabled=false` 与 `resolve_ci_backend→None` 两类共 4 处结构上确实在核验点之前返回; R2-fix 更正为「20/24 触达 + 4/24 不触达」 | ✅ 闭合, 数字属实 |
| code-reviewer M-4 / qa-engineer QA-M1 (backend ambient 恒红 / `path_coverage_enabled` 门控轴空真) | R2-fix 分别用「可达前提」块与 `SC-A-order` 腿 2 处理, 两者机制独立、不冲突 | ✅ 闭合 |
| 重试/常量复用先例 (`RETRY_BACKOFF`/`MAX_RETRY_ATTEMPTS`/`AETHER_CLI_MIN_SHA` 引用) | 独立读 `ci_backends/aether.py:33-39`、`pre_merge_gate.py:251-252` 确认常量与导入先例逐字命中 | ✅ (R1 起已闭合, 本轮未变, 复核仍成立) |
| `_run_with_retry` 三条缺陷 (硬绑 binary / 只捕 TimeoutExpired / 无 cwd / `text=True`) | 独立读 `ci_backends/aether.py:164-186` 逐行确认全部属实, docstring 自陈「other exceptions bubble up」 | ✅ (支撑「不复用函数体, 只复用枚举/常量」的架构判断, 本轮未变) |

**结论**: 我职责范围内的 R2 findings **全部真闭合**, 不是「写下来」——每条我都独立重跑了命令或重读了源码, 而不是采信 R2-fix 的自述。

## 2. 本轮我重跑的命令 (全部原文)

```bash
git -C aria rev-parse HEAD                                  # af87cae, 工作树 clean

# SC-A-doc 两条解析规则 —— 独立重算
python3 -c "
import re
with open('aria/skills/phase-c-integrator/SKILL.md','rb') as f:
    lines = f.read().split(b'\n')
block = b'\n'.join(lines[264:277]).decode('utf-8')
keys = re.findall(r'^  \"([A-Za-z_]+)\":', block, re.MULTILINE)
print(keys, len(keys))
"
# → ['verdict','pr_ci_status','in_flight_runs','primitive_used','primitive_version_sha','raw_message','path_coverage'] 7

# _build_output 实产键 —— 独立读源码
sed -n '225,263p' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
# → 6 固定键 + 条件 path_coverage, 无 gate_error 形参 (与 SC-A-doc 断言的 code 侧操作数一致)

# SC-A14 腿 2 (出口净化) —— 独立复现崩溃 + 独立验证补救
python3 -c "
import json, sys
raw = b\"fatal: couldn't find remote ref \xff\xfeweird-branch\"
s = raw.decode('utf-8', errors='surrogateescape')
sanitized = s.encode('utf-8','replace').decode('utf-8')
print('lone surrogate before:', any(0xDC80<=ord(c)<=0xDCFF for c in s))
print('lone surrogate after :', any(0xDC80<=ord(c)<=0xDCFF for c in sanitized))
out = {'raw_message': sanitized, 'verdict': 'fail'}
sys.stdout.write(json.dumps(out, ensure_ascii=False) + '\n')
"
# → before True / after False / 正常写出, 无 UnicodeEncodeError

# 20/24 vs 4/24 —— 独立重读四处调用
sed -n '298,325p;515,530p' aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py
# → 确认 4 处 (enabled=False 一处 / resolve_ci_backend→None 三处) 结构上在核验点之前返回

# aether.py 常量与 _run_with_retry 缺陷 —— 独立重读
grep -n "RETRY_BACKOFF\|MAX_RETRY_ATTEMPTS\|AETHER_CLI_MIN_SHA" aria/skills/phase-c-integrator/scripts/ci_backends/aether.py
sed -n '160,190p' aria/skills/phase-c-integrator/scripts/ci_backends/aether.py

# main() CLI 现状 —— 确认 --remote 确未接线 (支撑 SC-A-cli 存在理由)
sed -n '423,441p' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py

# 两个仓 origin 解析到不同 repo, 均有 master 无 main —— 独立复现
git -C /home/dev/Aria remote -v; git -C /home/dev/Aria/aria remote -v
git -C /home/dev/Aria ls-remote --heads origin main   # 零行 + rc=0
git -C /home/dev/Aria ls-remote --heads origin master | wc -l   # 1
git -C /home/dev/Aria/aria ls-remote --heads origin master | wc -l   # 1

# 兄弟位置清点表穷尽性 —— 独立重跑 SC-M18 的四个目标文件 (本节的关键发现, 见 §4)
grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py            # 2
grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' aria/skills/phase-c-integrator/SKILL.md                              # 4
grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py           # 3
grep -n "SC-M18" openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
grep -n "SC-M18" openspec/changes/premerge-gate-branch-existence/proposal.md
```

## 3. R1-fix → R2-fix 引入率 (我职责角度内)

上一轮 (R2) 我报告 2 条 Major, 均由 R1-fix 引入, 本轮**全部真闭合** (§1)。
本轮我新增 1 条 Major (§4), 由 R2-fix **新写的「兄弟位置清点表」自身**引入
(该表是 R2-fix 全新创建的内容, 不存在于 R1-fix 版本)。

⇒ **我这一席这一轮: 1 条新发现 / 1 条 finding = 100%**, 但**总量从 2 降到 1** ——
样本太小 (单席 1-2 条) 不能据此判断整体收敛率, 且这条新发现的**性质**与前两轮出现的
「新写的段落自己开新洞」同形 (与 memory `marginal-return-negative` 一致: 每件新安全网都造出自己的新表面),
但**严重度**明显更轻: 前两轮我的 finding 都是「机制本身会崩溃/欠定」(UnicodeEncodeError 使进程非 0 退出;
解析规则欠定使两个实现者得到相反结果), 这条是「一张审计辅助表的自我描述不准确」——**不影响 A 的任何 SC 本身的可证伪性**
(见 §5), 只影响「兄弟位置清点已穷尽」这句**元声明**的可信度。是否据此判断收敛趋势, 交汇总席判定。

## 4. 复核「兄弟位置清点」表的穷尽性 —— 发现一个数漏的兄弟 (Major, 新发现)

### 结论先行

R2-fix 新增的兄弟位置清点表 (proposal.md「§残余暴露」下方) 声称「归纳: 10 条 B 侧 SC 里 4 条 A 落在其拒绝域内
(M1 · M2 · M3a · M15), 另 6 条实测无对撞」。**这个「10 条」的清点本身不完整** —— 它把 **`SC-M18`** 处理成了
「只检查 `SKILL.md` 一个文件的计数」, 但 B 侧 `SC-M18` 的**真实定义**是对**四个文件独立各跑一次**同一 pattern
(`.../scripts/pre_merge_gate.py` · `.../phase-c-integrator/SKILL.md` · `.../tests/test_pre_merge_gate.py` ·
`.aria/config.template.json`), 其中**前两个 A 直接编辑**——`pre_merge_gate.py` 是 A 新增 `--remote`/
`_verify_branch_exists()`/核验点插入的**同一个文件**, `test_pre_merge_gate.py` 是 A 新增 `SC-A*` 用例、
扩 `_ProbeCacheResetMixin` 的**同一个文件**。清点表从未单独检查这两个目标。

### 证据 (本轮独立实跑, 见 §2 命令原文)

实读 B 侧 `proposal.md:364` 逐字:

```
| SC-M18 | 同一条承诺措辞 pattern 跑在删除面其余四个文件上:
  grep -cE '...' <f>, <f> ∈ {.../scripts/pre_merge_gate.py, .../phase-c-integrator/SKILL.md,
  .../tests/test_pre_merge_gate.py, .aria/config.template.json}
  | 0 / 0 / 0 / 0 | 2 / 4 / 3 / 0 | 必红 (前三个) |
```

A 侧兄弟位置清点表对 `SC-M18` 的行:

```
| 🔴 SC-M18 | ... 在 SKILL.md 的计数 | 0 | 不会 —— A 明确不碰 v2.0 弃用面 | 无需约束 |
```

**这一行只覆盖了 `SC-M18` 四个目标里的一个**。我独立重跑今日实测 (§2 命令), 与 B 侧「今日实测」列逐数字对上:
`pre_merge_gate.py` = **2** (`:68` 注释「Old keys still readable until v2.0」/ `:116` 字面
`f"will be removed in v2.0"`), `SKILL.md` = **4**, `test_pre_merge_gate.py` = **3** (`:293` 注释 + `:419`/`:431`
断言字符串)。**前两个文件 A 都直接编辑。**

### 这不是「A 会打爆 SC-M18」——但清点表的「无需约束」结论没有覆盖它该覆盖的范围

不是说 A 的新增内容会**新增**这个 pattern (A 的新步骤/注记文本不含 `still readable`/`removed in v2.0`/`仍读`/
`v2.0 移除` 字面, 我逐段核对过 A 要求写入 `SKILL.md` 的新增文本, 未命中), 所以**功能层面**这条 SC 不会因 A 而
"从今日的 2/4/3"往上涨。真正的问题是**方法论层面**: 这张表的存在理由 (逐字) 是「不清点就只修一个实例…本轮穷举
B 侧全部断言到『A 会碰的文件』的 SC」, 但它对 `SC-M18` 的清点**只做了四分之一** —— 漏掉的两个恰好是 A 与 B
**都要编辑的同一份 Python 文件** (`pre_merge_gate.py` / `test_pre_merge_gate.py`), 这正是「兄弟位置清点」这个
方法本该最先抓住的那类风险 (对比 `SC-M15` 那条: 它之所以被这轮新抓到, 正是因为清点者意识到「B 的 D1 会折叠
A 新写的那个步骤」——同一种"A、B 迟早会同时触碰同一段文本"的推理, 这里没有被推广到 A、B 会**同时触碰同一份
`.py` 文件**这个更直接的场景)。

**如何会红 (对清点表本身, 不是对 SC-M18)**: 若有人（Phase B 实施者 / D.2 收尾者）依据这张表的「无需约束」结论,
认为「A 与 B 在 `pre_merge_gate.py` / `test_pre_merge_gate.py` 上没有交叉需要协调」, 会漏掉两个真实的下游成本:
(a) A 落地后 `pre_merge_gate.py`/`test_pre_merge_gate.py` 的行数与结构会显著变化 (新增 `--remote` 参数、
`_verify_branch_exists()`、`SC-A*` 测试类), B 侧 `TASK-020` 若之后要去删 `:68`/`:116` 这两行 legacy-alias
deprecation 文案、以及 `test_pre_merge_gate.py:419`/`:431` 对应断言, **行号锚点会因 A 先落地而漂移**,
需要 B 实施者重新定位, 而不是像今天这样可以直接用行号; (b) 这是 A 与 B **在同一份仓内文件上顺序编辑**
的又一个具体实例, 而 A 目前唯一处理"同文件接缝"的机制是 `SKILL.md` 那三条机械锚 (`SC-A-step`/`SC-A-doc`/
`SC-A-note`)——`.py` 文件侧的同类接缝 (A 加代码, B 之后删代码, 都在同一个函数/模块里) 没有被这张表纳入视野。

### 修法建议 (供 A.2/Phase B 参考, 不代替 owner 裁量)

在兄弟位置清点表补一行 (或在 `SC-M18` 行加脚注): 「`SC-M18` 对 `pre_merge_gate.py`/`test_pre_merge_gate.py`
的两个分量属**同文件接缝**而非**文本对撞**——A 不写入该 pattern (不新增计数), 但 B 的 `TASK-020` 落地时须
**以内容定位、不以 A 落地前的行号定位**去删除 `:68`/`:116` 与对应测试断言」。一句话即可闭合, 不改变 A 的任何
交付面, 属**如实标注**而非新增义务。

**severity**: Major (不阻塞 Phase B — A 的功能实现与 18 条 SC-A* 均不受影响; 只是这张新增审计辅助表本身的
「穷尽」自称不准确, 且它点名的正是本轮任务书要求对抗的那个面)。

**introduced_by_r2fix**: **是** (兄弟位置清点表整节为 R2-fix 全新创建, R1-fix 版本没有这张表)。

## 5. SC-A* 集合本身的自足性复核 (18 条, 我职责角度)

本轮独立抽查了与我职责最相关的几条机械锚, 均**行为正确、非空真/恒红/恒绿**:

- `SC-A-doc` 的两条解析规则: 独立重算正则, 恰得 7 键, 与 `_build_output` 今日实产键一致 (§2) —— **正则本身正确, 不是巧合**;
- `SC-A14` 腿 2 (出口净化): 独立复现 `UnicodeEncodeError` 崩溃场景, 独立验证补救方案确实消除孤立代理码位且不破坏正常
  (合法 UTF-8) 分支名的往返 (§2) —— **补救机制真实可用, 不是纸面权宜**;
- `_build_output` 现状 (6 固定键 + 条件 `path_coverage`, 无 `gate_error` 形参) 与 R2-fix「必须经 `_build_output`
  产出」的钉死要求**互相自洽** —— 这条钉死消除了 `SC-A-doc` 「代码侧操作数」原本的两难 (事后附加 vs 硬编码),
  Phase B 若照此实现, `SC-A-doc` 才是一个良定义的相等断言;
- 「可达前提」块声明的适用集 (10)/例外集 (3)/不适用集 (3) 与 18 条 SC 逐一核对**无遗漏无重复**
  (10+3+3=16, 另 2 条 `SC-A-sc22`/`SC-A-baseline` 为元断言, 16+2=18, 与文首「计数法」声明一致)。

**未发现 A 自己的 18 条 SC-A* 里有恒红/恒绿/空真** (§4 的发现是「兄弟位置清点表」这个**非 SC** 的辅助文档, 不是
`SC-A*` 机械判据本身的缺陷)。

## 6. 对「四件不同意」与两条 owner 裁量项的复核 (我职责角度可判定的部分)

- 「不同意 SC-M3a 二选一, 取 (i) 而非 (ii)」: 我认可其论证 (改 B 的 SC 期望值会使该值随 A/B ship 顺序漂移,
  结构上更差) —— 这是一个纯粹的"哪个耦合方向更差"判断, 不在我的插入点/退出码专长内, 但论证内部自洽, 我不反对。
- 「不同意带参 CLI 示范是新步骤最自然形态」: 我核实了步骤 2/2.5 确实都是函数调用形态 (`resolve_ci_backend(cfg)` /
  `evaluate_path_coverage(main_branch, pr_branch)`, 独立 `sed` 确认, 见 §2 输出), 这个类比成立, 不同意有据。
- 「不同意 doc 侧 7 键是人工数的」: 已在 §2/§5 独立验证 —— 正则确实能算出 7, 不是人工拍脑袋。
- 「同意 #137 耐久性是缺陷但不同意在 A 内可修」: 这一条落在划界/流程职责而非实现可行性, 不在我本职角度内评判,
  但从代码可行性角度看没有反例——A 确实没有任何机制能把一份 proposal.md 里的声明"耐久地"绑定到外部 issue 状态,
  路由到 BLOCKER 供 owner 裁量是唯一诚实的选择, 我不反对。

## 7. 严重度与投票

0 Critical + 1 Major + 0 minor ⇒ **PASS_WITH_WARNINGS**。这条 Major 不构成 `blocks_phase_b`
(不影响 A 的 18 条 SC-A* 可证伪性、不影响任何代码级实现细节、修法是一句脚注), 我职责范围内 R2 的全部
findings 真闭合, 未发现新的插入点/退出码分区/异常重试解码/additive 破坏面缺陷。
