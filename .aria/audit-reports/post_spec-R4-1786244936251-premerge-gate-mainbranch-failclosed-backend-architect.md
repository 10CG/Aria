---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T03:47:52.911Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — backend-architect — premerge-gate-mainbranch-failclosed

## 审计结论

本轮审的是范围重定后的新承重项 D1 (`SKILL.md §C.2.4` 散文改强制 helper 调用) + 因 D1 而重新变得"可达"的 D4 (存在性核验) / D6 (`gate_error`)。四条镜头全部**实跑**验证 (`/tmp` 受控裸仓实验 + 本仓真实 cwd/grep 复现), 不满足"仅读文档"。

结论: **D1 自身的落地文本存在两处独立的、可复现的缺陷** (§1 命令的 cwd 契约冲突 + SC-3 断言对自身示例恒红), **D4 的兜底分支有一处实测缺口** (真实失败退出码 128 落在援引区间外)。三条均为 **Critical**, 且都直接命中 Spec 自称的"承重项"本体, 不是外围问题。另有一条 **Major** (`gate_error` 无消费者) 关系到 SC-6 的信息是否真能传达给人类。

**这不是"标准仍不完美但可接受"的量级** —— 第一条 (cwd 矛盾) 和第三条 (SC-3 自证恒红) 都精确命中 Spec 自己反复强调的"D1 是唯一承重项, 其余是配套"这句话本身: 如果 D1 的落地文本自相矛盾, 配套的 D4/D6 无论多正确都建在同一个不稳的地基上。

## Verdict

**FAIL** (3 Critical + 1 Major)。判据: verdict = FAIL 当且仅当 ≥1 Critical; 本轮 3 条 Critical 全部来自实测复现, 非推测。

## 轮次记录

- R1-R3 (历史): 聚焦 helper (`pre_merge_gate.py`) 侧加固 (D2 参数必填 / D3 占位符 / D4 存在性核验雏形)。R3 结论: 三版范围都错了 —— AI 实际执行 C.2.4 走的是 SKILL.md 散文步骤 3 的裸命令, 不经过 helper, 加固全部落空。
- R4 (本轮, 我的第 4 次坐席): 范围重定到 D1 (SKILL.md 结构重整, 强制 helper 调用)。本轮新验: (a) D1 新命令块本身的 cwd/路径解析契约 [新发现, Critical]; (b) D1 新命令块与 SC-3 grep 断言的逐行匹配语义冲突 [新发现, Critical]; (c) D4 存在性核验的 exit-code 表对真实 `git ls-remote` 失败码的覆盖缺口 [延续 R1/R2 已提及但未收敛的线索, 本轮用真实裸仓实验钉死, Critical]; (d) D6 `gate_error` 的消费链路 [与 R2 tech-lead M6 相关但角度不同 (本轮聚焦"人类能否看到 message", 非 verdict 词表), Major]。

---

## 镜头 1 — §1 唯一执行入口的路径解析

**Spec 原文** (proposal.md:67-76):
```bash
python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
  --pr-branch "<PR_BRANCH>" --main-branch "<MAIN_BRANCH>" --remote origin
```
**先例**: `SKILL.md:737` 已有同形的强制 helper 调用范式 (`token_telemetry.py`), 本条沿用。

### 实测 1a — `ARIA_PLUGIN_ROOT` 由谁设置

```
$ grep -rn "ARIA_PLUGIN_ROOT\s*=" --include='*.py' --include='*.md' --include='*.sh' --include='*.json' /home/dev/Aria | grep -v '/\.git/\|ab-results\|ab-suite'
(零命中 — 全仓从未被赋值, 只有 6 处 `${ARIA_PLUGIN_ROOT:-aria}` 消费点)
$ env | grep ARIA_PLUGIN_ROOT
(空)
$ cat .claude/settings.json | python3 -c "...print(d.get('env','NO env KEY'))"
"NO env KEY"
```
**结论**: `ARIA_PLUGIN_ROOT` 无人设置, 100% 恒走 `:-aria` 相对路径回落 —— 这不是罕见分支, 是**唯一会发生的分支**。

### 实测 1b — 相对路径回落在 `:242` 契约要求的 cwd 下能否解析

`SKILL.md:242` (同一进程内、同一次 gate_check 调用链上, 紧邻步骤 3 之前的步骤 2.5) 逐字: **"执行上下文契约: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)"**。本 Spec 自己的"代码落点"就是 `aria/` 子模块 —— 也就是说本 Spec 自己的 PR 落地时, C.2.4 执行的正是"子模块合并", `:242` 契约要求 cwd = `aria/` 子模块根。

```
$ cd /home/dev/Aria && test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" && echo OK
OK   # 从 meta-repo 根可解析

$ cd /home/dev/Aria/aria && python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" --pr-branch foo --main-branch master --remote origin
python3: can't open file '/home/dev/Aria/aria/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py': [Errno 2] No such file or directory
$ echo $?
2
```
**从子模块根 (即 `:242` 契约钦定的 cwd) 执行 §1 给出的逐字命令, 硬失败** —— 回落路径拼出 `aria/aria/skills/...`, 该目录不存在 (`aria` 子模块内没有嵌套的 `aria/` 目录)。

`evaluate_path_coverage()` (`path_coverage.py:105-111` `_repo_root()`) 用 `git rev-parse --show-toplevel`, `cwd=None` (继承调用进程 cwd) —— 证实 `:242` 契约管的就是**整个 `pre_merge_gate.py` 进程的 cwd**, 不是某个内部函数单独的参数, 与 §1 新命令的路径解析共享同一个 cwd, 二者要求互斥。

### 实测 1c — helper 不可达时 Spec 有无降级契约

搜遍 proposal.md §1 全段与折叠块描述: **没有**。D1 明确要求把原 5 步"移入折叠块 ... ⛔ 不要手工执行" —— 即上面这条路径解析一旦失败 (exit=2, 如实测), AI **没有任何 Spec 认可的下一步**: 唯一被明令禁止的退路 (手工执行裸命令) 恰恰就是 R3 认定的病根, 不能重新打开。

### 附带: "先例" 引用不精确

`SKILL.md:737` 实际写的是 `${CLAUDE_PLUGIN_ROOT:-aria}` (Claude Code 官方注入变量), 不是 `${ARIA_PLUGIN_ROOT:-aria}`。本会话内 `env | grep CLAUDE_PLUGIN` 同样为空 (Bash 工具子进程不继承该变量), 所以两者在"Bash 工具执行 C.2.4"场景下**结果相同** (都回落 `aria`) —— 不改变上面的结论, 但"本条沿用 :737 同形先例"这句表述本身不准确 (变量名不同, 且 :737 是单行命令, 无 cwd 契约冲突可比对), 不能作为"这个模式已验证可行"的证据。

**severity: critical / blocks_phase_b: true** —— 这是 D1 (唯一承重项) 自身文本的路径解析在其自称覆盖的场景 (子模块合并) 下实测失败, 且无降级契约。

---

## 镜头 2+3 — §4 存在性核验命令的 exit code 语义

**Spec 原文** (proposal.md:98-111):
```bash
git ls-remote --exit-code --heads <remote> "refs/heads/<main_branch>"
```
| 情形 | 判据 | 输出 |
|---|---|---|
| exit 0 | 存在 | 继续 |
| exit 2 | 不存在 | fail + `main-branch-not-found` |
| timeout | 按 `:259`: 3 attempts | fail + `main-branch-verify-failed` |
| 其他非零 | 按 `:260`: exit 1-126 → fail, 不重试 | fail + `main-branch-verify-failed` |

### 实测 2a — 核心 0/2 语义 (D4 主张的锚定修复)

受控裸仓 (`git init --bare` + 只推 `wip/master`, R2 手法复现):
```
$ git ls-remote --exit-code --heads origin "refs/heads/master"     ; echo RC=$?
RC=2
$ git ls-remote --exit-code --heads origin "refs/heads/wip/master" ; echo RC=$?
<sha>  refs/heads/wip/master
RC=0
$ git ls-remote --exit-code --heads origin master   # 裸分支名, 未锚定
<sha>  refs/heads/wip/master
RC=0   # ← 尾段 glob 命中, 复现 R2 的原始发现: 裸分支名会把 wip/master 误判成"存在"
```
D4 的核心主张 (必须锚定 `refs/heads/<name>`) **实测成立**, 表格 exit-0/exit-2 两行准确。

### 实测 2b — "其他非零" 的真实分布 (关键缺口)

```
$ git ls-remote --exit-code --heads doesnotexist_remote "refs/heads/master"
fatal: 'doesnotexist_remote' does not appear to be a git repository
fatal: Could not read from remote repository...
RC=128

$ git remote add badremote /tmp/.../nonexistent-path-xyz.git
$ git ls-remote --exit-code --heads badremote "refs/heads/master"
fatal: '...' does not appear to be a git repository ...
RC=128

$ git remote add unreachable_net http://127.0.0.1:1/repo.git
$ timeout 8 git ls-remote --exit-code --heads unreachable_net "refs/heads/master"
fatal: unable to access 'http://127.0.0.1:1/repo.git/': Failed to connect ...
RC=128
```
**三种独立构造的真实失败场景 (remote 名未配置 / remote URL 是坏路径 / 网络不可达) 全部返回 128, 无一落在 Spec 表格援引的 "1-126" 区间内。** `git` 对 `fatal:` 级错误统一走 `die()` → `exit(128)`, 这是 git 自身的退出码惯例, 和 `:260` 那张表 (为 **aether 二进制** 的 subprocess 退出码设计, "127=binary not found→no_ci_fallback" 是 shell "command not found" 惯例) 本来就是两套不同命令、两套不同惯例的退出码空间, 照搬不成立。

⚠️ 这不是"127 分支会被错误触发"那么轻 (128≠127, 那条分支确实不会误发); 而是"1-126 → fail"这条**catch-all 桶本身覆盖不到 128**, 而 128 恰是三种真实失败构造**全部命中**的码 —— 也正是本审计任务书点名要核的"remote 不可达"场景。

### 影响: 两个独立实现者会分叉, 且分叉方向有一支重新打开 fail-OPEN

- 实现者 A: 严格照抄"exit 1-126 → fail" → `elif 1 <= code <= 126: fail`, 128 落不进任何分支。若无兜底 `else`, 函数隐式返回 `None`/继续往下走而不设 `verdict=fail` —— 这正是本 Spec 存在的理由 (Rule #8 那条腿不能悄悄变绿)。
- 实现者 B: 读"其他非零"这四个字的字面意思 → `else: fail` 全覆盖 —— 恰好正确, 但与"1-126"这个具体数字承诺不符。

**SC-7 是 mock 测试** (`ls-remote 返回非 0 非 2 (mock)`), mock 的返回码是任意选的, 测不出真实 128 是否被正确路由 —— `feedback_test_mock_pattern_hides_prod_bug` 这类风险在此复现: 测试能过, 生产可能不过。

### 历史延续性

本线索并非本轮首次出现: R1/R2 backend-architect 报告已讨论"其他非零 vs timeout 的重试语义分叉"(含一次对 `git diff` 128 的旁证), 但聚焦点是重试触发条件而非"1-126 数值区间是否覆盖真实 git fatal 码"。本轮用三组独立受控实验把这个更具体的缺口钉死, 且**当前 263 行文本仍未解决**。故标记 `introduced_by_r3fix: false` (缺口本身不是本轮新引入), 但仍判 `blocks_phase_b: true` —— 因为它命中的是 D4 (本 Spec 另一条承重项:"一道对两条路径都有效的拦截"), 且是该拦截在最常见真实失败模式下的行为空白, 遗留到 Phase B 有复现本 Spec 要根治的 fail-open 病的风险。

**severity: critical / blocks_phase_b: true**

---

## 镜头 (追加发现) — SC-3 对 §1 自身示例恒红

审计任务书"待 R4 重点审"第 3 点点名要查 SC-3 的形态; 实测发现比"会不会被无关改动误触发"更严重的问题: **SC-3 连 Spec 自己给出的正确示例都测不出来。**

SC-3 (proposal.md:176): `grep -cE 'python3.*--main-branch|--main-branch.*python3' SKILL.md` 期望 **≥1**, 且明文标注"**承重断言, 对应 D1**"。

§1 给出的逐字命令块 (proposal.md:69-72) 用 `\` 续行, `python3` 在第一行、`--main-branch` 在第二行:
```
$ cat > sc3_test.md << 'EOF'
python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
  --pr-branch "<PR_BRANCH>" --main-branch "<MAIN_BRANCH>" --remote origin
EOF
$ grep -cE 'python3.*--main-branch|--main-branch.*python3' sc3_test.md
0
```
`grep` 默认逐行匹配, 不跨行 (SC-3 命令没加 `-z`/`-P(?s)`)。**若 Phase B 实现者最忠实地照抄 §1 给出的两行块 (这是"逐字"二字最自然的读法), SC-3 读到的计数是 0, 判定为红** —— 即便 D1 已经正确落地。

对照组 (命令写成一行, 不用 `\` 续行):
```
$ grep -cE 'python3.*--main-branch|--main-branch.*python3' sc3_test_oneline.md
1
```
只有偏离 §1 自己给出的两行格式、强行拼成一行, SC-3 才会绿。

**这意味着 D1 (本轮唯一承重项) 的验收断言与它自己的示例代码互相矛盾** —— 不是"两个实现者会分叉", 而是"唯一一种最忠实的实现方式就会导致自己的验收标准判红"。Success Criteria 引言本身写着"本表不留裁量空间", 并且刚刚批评过前一版 SC 犯过同类错误 ("被 R3 三席证明两种自然实现都失效") —— SC-3 现在复刻了同一个问题形状。

**severity: critical / blocks_phase_b: true / introduced_by_r3fix: true** (SC-3 与 §1 命令块都是本轮新写内容)。

---

## 镜头 4 — `gate_error` 的消费者

**Spec 原文** (proposal.md §6): `message` 是 SC-6 的断言对象, "故必须是 schema 的一部分而非只存在于 `raw_message`"。

### 实测 4a — `SKILL.md:252-255` 路由决策原文

```
252: green → 调用 branch-manager merge action ... (a)/(b) surface 义务只提 not_applicable / path_coverage.unknown
254: wait → 输出 wait_recoverable 错误 ...
255: fail → BLOCK + 输出 verdict + raw_message, phase-c-integrator return failure
```
`:255` 逐字只提 `verdict` 和 `raw_message`, **不提 `gate_error`**。proposal.md 的 Impact 表 (§Impact, SKILL.md 行) 列出本 Spec 会碰的行是 `:167` `:243` `:270` `:267` `:279` + 占位符统一 —— **不含 `:252-255`**。也就是说这条路由散文在本 Spec 落地后原样保留, 依旧只承诺输出 `raw_message`。

### 实测 4b — 代码层是否有 `gate_error` 消费者

```
$ grep -n "def write_gate_state" -A15 gate_state_helper.py
```
`write_gate_state(state, *, name, verdict, in_flight_runs=None, primitive_used=..., raw_message="", intervals=...)` —— **签名里没有 `gate_error` 形参**, 持久化进 `state["gate_state"]` 的六个字段里也没有它的位置。该文件自己的 docstring 明说: "The actual workflow-runner skill is markdown-driven (LLM caller handles state); this helper exists so the behavior is testable" —— 真正的运行时"消费者"是**读 stdout JSON 的 AI 本身**, 不是任何 Python 调用链。

```
$ grep -rn "gate_error" --include='*.py' /home/dev/Aria | grep -v test_
(零命中 — 全仓没有任何非测试代码引用这个键)
```

### 影响链条

D6 的 additive 设计本意是"`message` 不只存在于 `raw_message`" —— 若 Phase B 据此把 `raw_message` 留空、message 只塞进 `gate_error.message`, 而 `:255` 路由散文没同步更新, AI 执行 C.2.4 遇到 `verdict=fail` 时按 `:255` 字面只会 surface 空的 `raw_message`, **`gate_error.message` (含"这不是「无 in-flight run」"这句本 Spec 存在的全部理由) 可能从未被念出来**。SC-6 作为纯字典级单测能通过 (它只断言 `gate_check()` 的返回值), 测不出这条"人类到底看不看得见"的链路缺口。

与 R2 tech-lead 的 M6 ("`write_gate_state(verdict=)` 消费的根本不是 gate 的 verdict 词表") 相关但角度不同: M6 讲的是 verdict 词表本身, 本条讲的是 `message` 内容能否传达到人类可见的报告面。`introduced_by_r3fix: false` (D6/`gate_error` 概念在 R2/R3 已存在, 非本轮新写), 但当前 263 行文本仍未闭合此链路。

**severity: major / blocks_phase_b: false** —— 不需要重新设计架构, 但需要在 Phase B 任务列表里补一条 (同步 `:252-255` 措辞 + 决定 `raw_message` 是否同步写入), 建议在 Spec 的 Impact 表里显式加这一行, 而不是留给 Phase B 临场发挥。

---

## 一条正向确认 (完整性)

D4 的**核心**修复主张 (锚定 `refs/heads/<name>` 防止裸分支名尾段 glob 误判) 经受控实验独立复现成立: 未锚定 `master` 命中 `wip/master` (RC=0, 假阳性); 锚定后不存在返 RC=2、存在返 RC=0, 与表格一致。这部分设计是稳的, 问题出在"存在性判定之外"的失败分支覆盖 (镜头 2+3) 与"承载它的调用入口"(镜头 1) 上, 不是"锚定"这个核心 idea 本身。

---

## 待 R4 重点审 —— 逐项回应

1. **D1 是否真的收敛了路径**: 全仓 grep `aether ci status --branch main` 只命中 `SKILL.md` 本体, `references/` 目录不存在, 无其他 skill 引用同形裸命令 —— **这一点是干净的**。但见镜头 1: 即便路径收敛到唯一入口, 那个入口自己在 Spec 划定的执行场景 (子模块合并) 下会解析失败。"收敛成一条路径"和"那条路径能走通"是两个问题, 前者过, 后者没过。
2. **折叠块排障能力**: 未展开验证 (不在本镜头范围内, 交由 QA/knowledge-manager 镜头判断更合适)。
3. **SC-3 形态**: 见上方追加发现 —— 不是"会被误触发/漏检", 而是"对自己的正确示例也误判", 更严重。
4. **SC-6/7/8 受控裸仓 fixture 与 test_sc22 冲突**: 未直接测试 test_sc22 交互 (需要读当前 `pre_merge_gate.py` 是否已 `import subprocess`, 已确认现状**没有** `import subprocess` —— 与 R2 报告的既有结论一致, 本 Spec 是该模块首次引入; 这部分留给 QA 镜头覆盖更完整, 本报告不重复断言)。
