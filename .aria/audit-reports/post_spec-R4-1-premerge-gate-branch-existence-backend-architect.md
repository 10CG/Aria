---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-12T18:20:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — Spec A `premerge-gate-branch-existence` — backend-architect

seat: backend-architect · vote: PASS · 0 Critical + 0 Major + 0 minor

视角: 实现可行性 (插入点 / 退出码分区是否穷尽 / 异常·重试·解码三轴 / 「纯 additive」的代码级复核)。
方法: 对 R3-fix (commit `ff847fb`, `git diff 017eb54 ff847fb` = 267→更大改动) 逐处独立复跑, 不采信自述。

## 0. 我本轮实跑的命令 (全部原文)

```bash
git log --oneline -5 -- openspec/changes/premerge-gate-branch-existence/proposal.md
# ff847fb R3-fix / 017eb54 R2-fix / e165df4 R1-fix / 0548317 建 Spec A

# 45 vs 55 计数法更正 —— 独立复跑新命令
ls .aria/audit-reports/ | grep mainbranch-failclosed | wc -l                              # 55
ls .aria/audit-reports/ | grep mainbranch-failclosed | grep -vE 'aggregate|audit-trail' | wc -l   # 45

# UnicodeDecodeError MRO
python3 -c "print(issubclass(UnicodeDecodeError, OSError))"                               # False

# ls-remote 三态 (催化 §2 退出码表)
git ls-remote --heads origin nonexistent-branch-xyz; echo rc=$?                            # 零行 rc=0
git ls-remote --exit-code --heads origin nonexistent-branch-xyz; echo rc=$?                # rc=2
git ls-remote --heads /tmp/does-not-exist-repo-xyz master 2>/dev/null; echo rc=$?           # rc=128

# NUL byte 边缘情形 —— 我本轮自己新探的一个假设 (见 §3)
python3 -c "
import subprocess
try:
    subprocess.run(['git','ls-remote','--heads','origin\x00evil','master'], capture_output=True, timeout=5)
except Exception as e:
    print(type(e).__name__, e, '| isinstance of (TimeoutExpired,FileNotFoundError,OSError):',
          isinstance(e, (subprocess.TimeoutExpired, FileNotFoundError, OSError)))
"
# → ValueError embedded null byte | isinstance ... False

find aria -maxdepth 4 \( -name pytest.ini -o -name pyproject.toml -o -name setup.cfg -o -name tox.ini \)   # 零命中

# 插入点 8 行号 —— 逐行独立重新 grep -n (非沿用 R1-R3 的转述)
grep -n 'if not cfg\["enabled"\]\|if backend is None\|ok, precheck_err = backend.precheck()\|if not ok:\|pc: dict\|if cfg.get("path_coverage_enabled"\|pc = evaluate_path_coverage\|in_flight = backend.query_branch_in_flight' \
  aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
# → 328 / 338 / 344 / 345 / 356 / 357 / 358 / 366 (8/8 与 Spec 逐字一致)
sed -n '346,357p' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py   # 确认 :345 早退结束到 :356 pc 声明间是干净空隙, 插入点无冲突

# _build_output 当前 docstring (SC-A-note (d) 腿的判据对象)
sed -n '232,247p' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py

# gate_check 当前签名 / main() 当前接线状态 (SC-A-cli 存在理由)
grep -n "^def gate_check" aria/skills/phase-c-integrator/scripts/pre_merge_gate.py     # :298, main_branch: str = "main"
sed -n '423,441p' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py            # main() 无 --remote, gate_check 调用无 remote=

# 异常/重试三轴先例复核
sed -n '160,190p' aria/skills/phase-c-integrator/scripts/ci_backends/aether.py        # _run_with_retry: 硬绑 binary/只捕TimeoutExpired/无cwd/text=True 属实
sed -n '70,102p' aria/skills/phase-c-integrator/scripts/path_coverage.py              # _run_git: cwd 形参 + bytes+surrogateescape + 三合一 except, 与 §5 引用逐字一致
sed -n '75,90p' aria/skills/phase-c-integrator/scripts/ci_backends/base.py            # precheck() 默认 (True,"")

# 两仓 origin 解析 (SC-A-cwd 前提)
git remote -v | grep origin ; git -C aria remote -v | grep origin
git ls-remote --heads origin master | wc -l ; git -C aria ls-remote --heads origin master | wc -l ; git ls-remote --heads origin main | wc -l
# → Aria.git / aria-plugin.git, 各 1/1/0, 与 SC-A-cwd 前提一致

# 双向清点表穷尽性 —— 独立重新枚举双方 SC 全集并核对表内覆盖
grep -oE '^\| \*\*SC-M[A-Za-z0-9]*' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md | sort -u   # 20 个 ID
grep -c '^| \*\*SC-A' openspec/changes/premerge-gate-branch-existence/proposal.md                                # 18
awk 'NR==254,NR==298' openspec/changes/premerge-gate-branch-existence/proposal.md | grep -n '^| '                # 表1: 14 物理行, 覆盖 20 个 SC-M ID (逐一清点无遗漏) + 3 条任务级预写量
awk 'NR==299,NR==313' openspec/changes/premerge-gate-branch-existence/proposal.md | grep -n '^| '                # 表2: 10 物理行, 覆盖全部 18 个 SC-A ID (逐一清点无遗漏)

# B 侧 TASK-003..009 状态 (D.2 handoff 交接项的事实依据)
grep -n "^- id: TASK-00[3-9]" -A4 openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml | grep -E "id:|status:"
# → 7 条全部 status: pending, 与 Spec 逐字一致

# SC-A-step 锚点 (F-6 的更正)
grep -n '^\*\*执行流程\*\*:\|^\*\*Subprocess 调用规范\*\*:\|^### C.2.5' aria/skills/phase-c-integrator/SKILL.md
# → 238 / 257 / 582 (:582 属另一节标题, "首个匹配"取 238 正确; 若误取"末次匹配"得 582>257 恒红)

# SC-A-note 区块边界 (F-7 的更正)
grep -n '^```$\|^枚举归层注记\|^\*\*配置参数\*\*:' aria/skills/phase-c-integrator/SKILL.md | sed -n '3,6p'
# → json fence close :277, 枚举归层注记 :279, 配置参数 :281 — 与 Spec 声称的 :278-280 边界一致
```

## 1. R3 的 14M+10m 是否真闭合 —— 我职责角度内逐条独立复核 (区分「写下来」与「闭合」)

我把 24 条 (14M+10m) 里落在**我的席位角度** (插入点 / 退出码分区 / 异常重试解码 / additive 代码级) 内、以及**我有能力独立实测**的条目全部重新验证 (不采信 commit message 或其他席位转述), 逐条结论如下:

| R3 finding (来源席位) | R3-fix 的处置 | 我的独立复核 | 闭合? |
|---|---|---|---|
| tech-lead M-1 / knowledge-manager Major (BLOCKER 承载前提假, "### Key Deliverables" 不存在) | 六项义务移入 `## Success Criteria` §交付义务小节 | 独立实读 `task-planner/SKILL.md:59-67` 与 `DUAL_LAYER_SPEC.md:90-93`, 确认路径 B 三项穷举含 `## Success Criteria`; `grep -c '^## Success Criteria'` 本轮实跑命中; §交付义务小节确在该章节内 (非文首/非 Impact) | ✅ **真闭合** |
| tech-lead M-2 / code-reviewer F-4 (出路(i) 委派 §C.2.5 兜 gitlink 失效) | 改为事实声明「O-1 无机械兜底」+ D-b 显式请 owner 裁 | 独立重读 §C.2.5 六步与 §C.2.4.5 逐字, 确认现文已删除失效委派句, 代之以「本 Spec 不假装它有」+两个可裁选项 | ✅ **真闭合**, 且这是诚实降级而非 paper-fix |
| tech-lead M-3 (SC-A-step (c-含) landmine) | (c-含) 只留 `#137` 一个 token, 标注对象改为「本步作用域边界」 | 独立读表2 `SC-A-step (c-含)` 行, 确认新判据不再要求「步骤3仍硬编码main」这个会被B修好的瞬时事实, B 落地前后陈述均为真 | ✅ **真闭合**, 且是真正的第三条路 (非二选一的变体, 见 §3) |
| tech-lead M-4 (SC-M3c 与 SC-M15 用的前提互斥, `--pr-branch` 未禁) | (c-禁) 由点名三字面量升级为类级 (禁一切 `--` 起头 flag) | `grep -c -- '--pr-branch' SKILL.md` 本轮独立复跑=0 (今日不违反); 类级禁令覆盖 `--pr-branch` 我逐字核对 SC-A-step 定义确认 | ✅ **真闭合** |
| tech-lead M-5 / code-reviewer F-2 (`SC-A14` 腿2 红机制建立在 `sys.stdout.errors=='strict'` 上, pytest 默认捕获下为 `'replace'`, 假绿) | 腿2 判据换成在 `gate_check()` 返回的 dict 上直接 `s.encode("utf-8","strict")`, 不再走进程出口/stdout | 这是纯字符串操作, 与 `sys.stdout` 捕获模式**结构上无关**——我独立确认 `str.encode()` 不读 `sys.stdout.errors`; 与打桩边界表「同一批 mock, 断言点在返回值上」自洽 (不再要求 `main(argv=…)` 与进程退出码, 消除了此前「子进程注不进 in-process mock」的欠定) | ✅ **真闭合**, 是本轮质量最高的一处 |
| tech-lead M-6 (`_build_output` docstring 第四处落点未上锚) | §4/§Impact 明文「同批更新 docstring」+ `SC-A-note` 新增 (d) 腿, 判据抹空白后匹配 | 独立读 `pre_merge_gate.py:241-246` 当前 docstring, 确认逐字含「各早退\n分支 (…) 保持\n既有六键不变」跨行——若不抹空白锚点确实零命中, Spec 已明文钉死抹空白规则, 我认可这条规则是必要的 (非过度设计) | ✅ **真闭合** |
| tech-lead m-2 / code-reviewer F-9 / **我自己 R3 的 Major** (`SC-M18` 兄弟位置表操作数缩窄成 `SKILL.md` 单文件) | 表1 `SC-M18` 行改为四分量 `2/4/3/0` 全列 | 独立重跑四个 `grep -cE` 命令, 得 `pre_merge_gate.py`=2 / `SKILL.md`=4 / `test_pre_merge_gate.py`=3 / `config.template.json`=0, 与 Spec 逐一对上, 且与 B `:364` 的「今日实测」列一致 | ✅ **真闭合** (我自己 R3 报的这条本轮被验证确实修对, 不是"写下来") |
| code-reviewer F-1 (「20/24 触达」实测 19/24, 精确化过头) | 改用 `sys.settrace` 动态测量, 得 19/24 + 三类早退与三条负控一一对齐 | 独立重读 §6 现文与四类早退的三条负控映射, `:282`/`:301`/`:311`/`:321`/`:524` 五处逐一核对结构位置未变 | ✅ **真闭合** |
| code-reviewer F-3 (`SC-A10c` 例外集分类错, 干净 runner 上假绿) | `SC-A10c` 移入适用集 (11条), 要求 mock backend | 独立读 `ci_backends/base.py:79-85` 确认 `precheck()` 默认 `(True,"")`, 唯一让它返 `(False,…)` 的路径是打桩; 适用/例外/不适用/元断言 = 11+2+3+2=18 配平, 我逐条点过 | ✅ **真闭合** |
| code-reviewer F-5 (「全部兄弟位置」未含 B 的任务级预写量) | 新增「方向1附加总体」表, 3 行覆盖 `tasks.md:85`/`detailed-tasks.yaml:488`/`tasks.md:122` | 独立读三处引文, 逐字与 B 现文比对一致, 处置(交 D.2 handoff)与 A 侧「不改 B」的既定纪律一致 | ✅ **真闭合** |
| code-reviewer F-6 (`SC-A-step` 起点锚有两处, 取末次匹配则恒红) | 明文「首个匹配」 | 独立 `grep -n '^\*\*执行流程\*\*:'` 得 `238` 与 `582`, 确认 `:582` 属 §C.2.5 标题非 §C.2.4; 若实现取末次匹配得区间 (582,257) 为负——Spec 现文已钉「首个」 | ✅ **真闭合** |
| code-reviewer F-7 / qa-engineer QA-3-2 (`SC-A-note`「段」边界 / `SC-A-step` (c) 正文边界均欠定) | `SC-A-note`: json 围栏结束到「配置参数」之间; `SC-A-step` (c): 明文「含缩进续行」 | 独立 grep 确认新锚 (json fence `:277` → `枚举归层注记 :279` → `配置参数 :281`) 是稳定标题/围栏锚, 不因段落如何分段而漂移; (c) 的抽取边界现覆盖「跨行拆分逃逸」这个 qa-engineer 点名的向量 | ✅ **均真闭合** |
| code-reviewer F-8 (45 vs 55 命令口径错) | 命令改为过滤 `aggregate\|audit-trail` | 独立复跑两条命令: 无过滤=55, 过滤后=45, 与 Spec 新命令逐字一致 | ✅ **真闭合** |
| code-reviewer F-10 (仓外写动作口径矛盾) | 四件仓外写动作统一归 D-a 一次裁定 | 独立读 §Impact「外部」行与 D-a, 确认「无外部动作」与「三个 issue 派给 A 侧」的矛盾已消除——现文两处口径一致 | ✅ **真闭合** |
| code-reviewer F-11 (§版本 grep 列举不全) | 补全 7 行列举 | 独立复跑 `grep -rn 'gate_check(' aria/ --include=*.py` 在测试文件外得 7 行, 与新列举一一对上 | ✅ **真闭合** |
| qa-engineer QA-3-1 (兄弟位置表漏 `SC-M6/7/8/10/11/13/14`, 对应 B 的 TASK-003..009 仍 pending) | 表1 新增 M6·M7·M8·M11·M13·M14 合并行 (标注任务层碰撞) + M10 单独行 | 独立重跑 `grep -oE 'SC-M[0-9]+[a-z]?' B/proposal.md \| sort -u` 得 20 个 ID, 逐一核对表1 全部覆盖 (含 M6/7/8/10/11/13/14); 独立复跑 B 的 TASK-003..009 状态确认 7 条全 pending | ✅ **真闭合**, 且是本轮双向清点表能建成的关键前提 |
| knowledge-manager minor (兄弟位置表漏 `SC-M9`) | 表1 补 `SC-M9` 行, 交叉引用表2 | 独立读 B `:355` 逐字, 确认 A→B 方向不打爆 (A 不改 `main_branch` 缺省), 且表2 `SC-A10/A10b/A10c` 行正确处理了反方向 (B 的 D5 必填要求 A 新用例显式传 `main_branch`) | ✅ **真闭合** |

**本轮我职责范围内可独立核实的条目 (约 16/24, 覆盖 14M 中的 13 条 + 10m 中的 4 条): 100% 真闭合, 无一条只是"写下来"。** 其余 8 条 (主要是 Level 2 判据 SOT 溯源 m-1、划界/流程类判断) 落在 tech-lead/knowledge-manager 的专长角度而非我的实现可行性视角, 我未独立复核, 交其余席位判定。

## 2. 引入率 (我职责角度)

本轮我在插入点/退出码/异常重试解码/additive 代码级这个专长范围内, **未发现由 R3-fix 新引入的缺陷**。

具体排查过的、最可能新开洞的三处 (SC-A14 腿2 的新判据 / 表1+表2 双向清点表的完整性 / SC-A-step 三处新约束的自洽性), 逐条独立验证结果均为**闭合且未见新缺陷**——细节见 §1 与 §3。

我本轮额外主动探测了一个此前 20 个席位-轮次都未提及的角度 (§3 的 `ValueError`/NUL byte 假设), 结论是**不构成新发现**——Spec 自己的 `SC-A14` 腿1 末项 (「任取一个不在实现 except 元组里的异常类」) 已经是一个**设计上刻意通用**的探针, 不是枚举清单, 它已经结构性覆盖了这类"三合一 except 元组接不住的类别", 无论具体是哪个异常类。这不是"侥幸没被打中", 是机制本身按其自陈设计目标 ("§2 的 catch-all 必须真的 catch-all") 生效的例子。

⇒ **我这一席本轮: 0 条新 finding。**

## 3. 复核执笔方自己预判的三处

**① `SC-A-step (c-含)` — 从我的角度看, 这是"修对了", 不是"修错了"。**
表2 该行的判据从「断言那句关于步骤3的具体不一致仍在」换成「只要求含 `#137` 这一个稳定外部锚」。这不是回避标注, 而是把标注对象从**一个会被 B 修好的瞬时事实**换成**本步自身作用域边界这个不随 B 漂移的陈述**——我独立核对了 §5/§残余暴露 逐字, 「本步只核验 main_branch 在 remote 上存在, 不保证后续步骤查询的是同一个分支」这句话在 B 落地前后**都为真** (它讲的是这一步契约本身, 不是别处的瞬时状态), `#137` 退化成溯源指针、issue 关闭后引用仍合法。从实现可行性角度, 这是一个可以被 Phase B 直接照抄写入 `SKILL.md` 的稳定句子, 不构成"必然被后续变更打破"的负债。

**② §交付义务的「完成判据」列是人工判据 (贴 `git show --stat`), 有机械闸门吗=没有 — 这是诚实标注, 不是可修复的疏漏。**
从代码可行性角度看, 要让 O-1 (发版同步面) 有机械闸门, 需要一个新的、专门比对「主仓 gitlink SHA」与「子模块 post-merge master SHA」的 custom check——这**不存在**于本 Spec 的交付面内 (D-b 已正确地把它作为 owner 待裁的第三个选项列出, 而非在 A 内部假装解决)。我认可这个判断: 在不新开一个 change 的前提下, A 结构上没有第三条路可以既保持 Level 2 单文件交付, 又凭空生出一个新机械闸门。这与前一轮我判定「O-1 的失效委派」是同一枚硬币的两面: 委派会制造假安全感, 而诚实声明"无兜底"不会。

**③ `SC-A-note` (d) 腿的 token 与语言绑定 — 已收口, 我认可。**
「把该段改写为英文不在本 Spec 授权范围内」这条约束本身是自洽的: 它防止 Phase B 在无关改动 (比如顺手把中文改英文) 时误伤一个内容完全正确的实现。若真要改语言, Spec 已给出退出阀门 (「须与 SKILL.md:279 同批同措辞改并同步改 (d) 的 token」), 不构成死锁。

## 4. 双向清点表 (表1/表2) 的穷尽性复核 — 我本轮独立重新枚举, 未发现遗漏

- **表1 (A→B)**: B 侧 `proposal.md` 独立 `grep -oE 'SC-M[0-9]+[a-z]?' | sort -u` 得 **20** 个唯一 ID (M1/M2/M3a/M3b/M3c/M4-M18 逐一)。我把这 20 个 ID 逐一在表1 中定位 (含被合并进「M4/M5」与「M6·M7·M8·M11·M13·M14」两个合并行的情形), **20/20 全部有归宿**, 无遗漏。加上「方向1附加总体」的 3 条任务级预写量 (`tasks.md:85` / `detailed-tasks.yaml:488` / `tasks.md:122`), 覆盖面比 R3 时 (10/20) 有实质扩大。
- **表2 (B→A)**: A 侧 `proposal.md` `grep -c '^| \*\*SC-A'` = **18**。我把表2 的 10 个物理行展开 (`SC-A-step` 被拆成 (a)(b)/(c-禁)/(c-含) 三个子行, `SC-A10/A10b/A10c` 与 `SC-A6·A13·A-zero·A7·A8·A11·A14·A-order·A-cwd` 各自合并一行), 得 **18** 个唯一 SC-A ID, 与 SC 表行数**恰好一一对应**, 无遗漏、无重复。这是 R3 时完全空白 (0/18) 的方向, 本轮从零建成且经我独立核验完整。

**我未发现表1/表2 还有遗漏的兄弟位置。**

## 5. 「纯 additive」代码级复核 (第三次独立核对, 结论不变)

- 8 个插入点行号 (`:328/:338/:344/:345/:356/:357/:358/:366`) 本轮独立 `grep -n` 重新定位, 8/8 与今日代码逐字一致, 插入缝隙 (`:345` 早退结束 → `:356` `pc` 声明前) 干净, 无变量作用域冲突;
- `gate_check(main_branch: str = "main", ...)` 今日签名确认未变, `remote` 形参确未接线 (`main()` 无 `--remote`, 调用处无 `remote=`)——**`SC-A-cli` 存在的理由本轮仍成立**;
- `_run_with_retry` 三缺陷 (硬绑 binary / 只捕 `TimeoutExpired` / 无 `cwd` / `text=True`) 本轮独立重读仍属实, 支撑「不复用函数体、只复用枚举与常量」的架构判断不变;
- `path_coverage.py:_run_git` (cwd 形参 + bytes+surrogateescape + 三合一 except) 本轮独立重读, 与 §5 引用逐字一致, 是可靠的复制模板;
- `_build_output` 今日仍是 6 固定键 + 条件 `path_coverage`, 无 `gate_error` 形参——`SC-A-doc`/`SC-A-note` 的"今日基线必红"前提本轮仍然成立;
- 两仓 `origin` 解析到不同 repo (Aria.git / aria-plugin.git) 且均有 `master` 无 `main`——`SC-A-cwd` 的对抗性前提本轮独立复现仍成立。

未发现新的恒红 / 恒绿 / 空真, 未发现插入点顺序/退出码分区/异常轴的新缺口。

## 6. 判定

**0 Critical + 0 Major + 0 minor ⇒ verdict = PASS。**

理由: 本轮我职责范围内可独立验证的 R3 findings (约占 14M+10m 的三分之二) **全部真闭合**, 每条我都重新执行了命令或重读了源码, 而非采信 R3-fix 自述; 双向清点表 (表1/表2) 经我独立重新枚举, 20/20 与 18/18 均完整无遗漏; 三处执笔方自己预判的争议点, 我的独立判断均为"诚实标注/合理设计", 不是"修错了"; 我主动探测的一个此前无人覆盖的假设 (`ValueError`/NUL byte) 复核后确认已被 `SC-A14` 腿1 的通用探针机制结构性覆盖, 不构成新发现。

`vote: PASS` (不同于我 R3 的 REVISE)——因为 R3 时我报的那条 Major (SC-M18 兄弟位置表操作数缩窄) 本轮经我独立复核**确实真闭合**, 且本轮未发现新缺陷, 我职责角度内没有理由再投 REVISE。是否据此判定 Spec A 整体收敛/停轮由汇总席跨席交叉判定, 单席无权 (`converged: null`)。
