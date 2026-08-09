---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T18:48:20.576Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — premerge-gate-mainbranch-failclosed (席位: tech-lead)

## 审计结论

Spec 抓的病是**真的**: `pre_merge_gate.py:300` / `:427` 两处 `"main"` 缺省确实存在, `aether.py:117-135`
确实无法区分「分支不存在」与「分支无 in-flight run」(`:124` `main_runs_raw = data.get("runs") or []`
是唯一合流点)。§2 / §3 的 fail-CLOSED 方向、D2「不回落字面缺省」、D4「ls-remote 失败不猜」在架构上
都是对的, 这几条我不反对。

但**范围边界切错了**, 而且切错的方式恰是本项目反复复发的三个形状里的两个 (委派/引用未核实到目标、枚举
不完整), 外加一处假自陈。核心事实: `main_branch` 不是 (b) 腿独占参数 —— 它在 `pre_merge_gate.py:359`
同时喂给 `evaluate_path_coverage()`, 也就是 (a) 腿那侧。Spec 的 D6 /「非目标」/ D7 三处「只治 (b) /
不动 path_coverage / 无行为面扩大」因此同时不成立。

另一处承重错位: Spec 全篇把 `SKILL.md:242` 当作 (b) 腿的「唯一现有约束」并提议改写它 —— 实读该行,
它是 **步骤 2.5 Path coverage 评估**的「执行上下文契约」; 而 (b) 腿自己的指令行是 `SKILL.md:243`,
那行**硬编码 `aether ci status --branch main --in-flight --json`**, 完全不在 Spec 的 Impact 枚举里。
按 Spec 原样执行 Phase B, 会改到 path_coverage 的契约句 (Spec 自称不碰的东西), 而把真正带 `main`
字面的 (b) 腿指令行留在文档里。

判定 **FAIL** (2 Critical + 6 Major)。这些都是 Spec 层面可修的, 不需要推翻方案本体 —— 修好范围、
补齐枚举、把 `<remote>` 和插入位置钉死、重判 Rule #6, 方案就可以走 Phase B。

---

## Findings

### C-1 (Critical / architecture) — `main_branch` 是两条腿共享输入, D6 与「非目标」与代码矛盾

**锚点**: `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:358-360`

```python
    if cfg.get("path_coverage_enabled", True):
        pc = evaluate_path_coverage(
            main_branch=main_branch, pr_branch=pr_branch
        )
```

同一个 `main_branch` 随后才在 `:366` 进 `backend.query_branch_in_flight(main_branch)`。
下游 `path_coverage.py:442` 用它拼 `f"{main_branch}...{pr_branch}"` 做三点 diff。

⇒ Spec 的三处声称同时被证伪:

- §非目标第 1 条「**不改** `path_coverage.py`」—— 文件是没改, 但它的**运行时输入**被改了, 这是行为面的
  改动不是文件面的。
- D6「**只治 (b) 腿**, 不动 `path_coverage`」—— 结构上做不到, 除非显式给两条腿分别传参 (Spec 未提)。
- D7「PATCH —— **无行为面扩大**」—— 见下面的实测。

**实测方向 (在 `aria/` 子模块内, 即 SKILL.md:242 契约规定的执行仓根)**:

```
$ git diff --name-only --no-renames -z main...HEAD
fatal: ambiguous argument 'main...HEAD': unknown revision or path not in the working tree.
RC=128
```

⇒ **今天**在本项目, path_coverage 恒走 `path_coverage.py:446-447` 规则 1 → `unknown` /
`git-diff-failed` → fail-toward-covered (保守)。**修好之后**首次拿到真 `master`, 规则 4/6/7/8 才
第一次真的参与判决, 其中规则 8 (`path_coverage.py:506-507`, `not_applicable` /
`no-triggering-paths`) 会走到 `pre_merge_gate.py:378-386` 直接 **跳过 (a) PR CI 查询**, 再由
`:208-214` 判 `VERDICT_GREEN`。

也就是说: 这个「把恒绿的腿修好」的 change, 在同一次落地里**首次打开了另一条腿的 green 通路**。
方向与 Spec 自述相反 —— Spec 在 §订正 (line 56) 自己论证过「(a) 在分支名错时更保守」, 却没把这个前提
推到结论: 前提成立正说明**修复会解除那份保守**。

Success Criteria 7 条**零覆盖**这条转变: SC-1/2 只断言解析出 `master`, SC-3/SC-7 是负控,
SC-4/5/6 是存在性核验轴。没有任何一条断言 path_coverage 从 `unknown` 转入真实评估后的判决。

**要求**: (a) 把「本 change 使 #122 路径覆盖机制在本项目首次真正生效」写进 Impact/风险并撤回
D6/D7/非目标的相反表述; (b) 补 SC —— 至少一条断言解析生效后 `path_coverage.decision` 不再是
`git-diff-failed`, 一条覆盖 `not_applicable → green` 这条首次可达路径 (含 SKILL.md:253 要求的
surface 义务是否被触发)。

---

### C-2 (Critical / documentation) — 承重引用错位: `:242` 是 path_coverage 的契约, (b) 腿的 `main` 字面在 `:243` 且未被枚举

**锚点**: `aria/skills/phase-c-integrator/SKILL.md:242` 与 `:243` (二者均实读; `:242` 是 524 字符长行)

`:242` 逐字尾部 = `**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根);
main_branch 显式传真值 (本项目 master), 不依赖 CLI default` —— 该句挂在 **`2.5. Path coverage 评估
(v1.65.0+, aria-plugin #122)`** 之下, 约束的是 `evaluate_path_coverage(main_branch, pr_branch)`。

(b) 腿自己的那行是 `:243`:

```
3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` → parse `data.runs[]` — **无条件执行, 不因 not_applicable 免除** ...
```

**`--branch main` 是字面写死的**, 且它是处方性运行时指令行 (告诉执行者这一步跑什么命令)。

⇒ Spec §Why line 46-50「唯一现有约束是一句散文」+ §5「`SKILL.md:242` 的散文同步」+ Impact 表第 3 行
「`SKILL.md:242` 散文勘正」这条链**整条建立在错认的行上**:

- 真正需要改的 `:243` 不在 Impact 任何一行里 → 落地后 (b) 腿文档继续写着 `--branch main`, 与新机制
  直接矛盾 (Rule #3 文档与代码同步)。
- 按 §5 原样执行会去改写 path_coverage 的执行上下文契约 —— 即 Spec 在「非目标」里声明不碰的那个机制的
  规范句。
- 同一句契约在 `path_coverage.py:19` 还有一份 (`- main_branch 由调用方显式传真值 (不依赖 "main" 默认)。`),
  也不在枚举内 → 改一处留一处的经典 fix-the-instance。
- `pre_merge_gate.py:21` 模块 docstring 的 `[--main-branch main]` 是同文件第三处字面, Impact 只写了
  「两处缺省」。

这正是本项目成文的 `reporter-miscite` 形状: 症状描述全对, 根因 file:line 引错; 引用被继承进 Spec 后,
后续 15 个 agent 都读同一条错引用。

**要求**: Impact 表按引用点重新枚举 —— 至少 `SKILL.md:243` (承重) / `SKILL.md:242` /
`SKILL.md:264-279` (见 M-3) / `path_coverage.py:19` / `pre_merge_gate.py:21`, 并订正 §Why 的
「唯一现有约束」表述。

---

### M-1 (Major / architecture) — `<remote>` 全篇是未绑定占位符; 且存在性核验与被守护的查询不同源

**锚点**: proposal.md §2 (`git symbolic-ref refs/remotes/<remote>/HEAD`) / §3
(`git ls-remote --exit-code --heads <remote> <main_branch>`) / D2 / D4

`<remote>` 从哪来, Spec 从头到尾没有定义: 没有 `--remote` 参数 (`pre_merge_gate.py:424-433` 只有
`--pr-branch` / `--main-branch` / `--config-file`), 没有 config 键 (`DEFAULT_CONFIG:53-65` 无),
没有决策记录, 没有 SC。这是承重承载面上的欠定 —— 两个独立实现者会写出不同东西 (memory
`spec-underdetermination`)。

**为什么在本项目它不是学术问题** (实测):

```
$ git remote -v            # /home/dev/Aria/aria
github  git@github.com:10CG/aria-plugin.git
origin  ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git
$ git symbolic-ref refs/remotes/origin/HEAD   → refs/remotes/origin/master   RC=0
$ git symbolic-ref refs/remotes/github/HEAD   → fatal: ... is not a symbolic ref   RC=128
```

选 `origin` → 解析成功走正常路; 选 `github` → 按 D2 直接 `verdict=error`。**同一个仓, 两种结果, Spec
不裁决。** 本项目是 CLAUDE.md 明确的双远程仓, 这个分叉必然被踩到。

**第二层, 更硬**: `ls-remote` 走的是 **git wire 平面**, 而被守护的查询 `aether ci status --branch X`
走的是 **Aether/Forgejo API 平面**, 二者的「仓」由不同配置决定。存在性核验绿 ≠ aether 那侧认识这个分支。
换句话说, §3 这条承重条款守的不是它要守的那个不变量的**同一个源**。这与 memory
`delegate-verify`(写「由 X 保证」前须核 X 真做吗/方式合约吗) 同形: Spec §100 论证了「为什么放 gate 层」,
但没论证「gate 层这个探针问的是不是 backend 那个问题」。

**要求**: 钉死 `<remote>` 来源 (建议: 显式参数 + config 键, 缺省 `origin`, 并把「解析用哪个 remote」
本身写进 `main_branch_resolved` 的来源字段); 并补一条决策明确承认存在性核验与 CI 查询是两个平面 ——
要么改用 backend 侧探针 (代价: 违反 D3), 要么在 Spec 里显式接受这个残余盲区并写明。

---

### M-2 (Major / testing) — 「既有用例逐字不改」是假自陈: 24/24 既有 `gate_check()` 调用依赖旧缺省

**锚点**: `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:663-670` (+ 全文件统计)

机械统计: 该文件 `gate_check(...)` 调用 **24 处, 其中传 `main_branch` 的 0 处**。全部依赖
`pre_merge_gate.py:300` 的 `= "main"`。

最硬的一条:

```python
    def test_sc12_default_true_lock(self) -> None:
        # 默认值锁定 (unset → 评估执行): config 不含 path_coverage_enabled。
        b = self._backend()
        with mock.patch.object(gate, "resolve_ci_backend", return_value=b):
            gate.gate_check(pr_branch="feat/x", config={})
        self.pc_eval.assert_called_once_with(
            main_branch="main", pr_branch="feat/x"
        )
```

它**逐字断言了要被删掉的那个缺省值**。⇒ Impact 表第 2 行「(既有用例逐字不改)」不成立。

更实质的后果: 缺省改 `None` 后, 这 24 条单测会走进新的解析路径, 也就是在单元测试里真起
`git symbolic-ref` / `git ls-remote` 子进程 —— 后者是**网络调用**。要么它们全部需要新的 mock (那就是
「既有用例要改」), 要么单测套件从此依赖网络与 CWD 的 git 状态。Spec 对此零处置。

**要求**: 撤回「逐字不改」的表述; 在 §What Changes 里明确解析层的可打桩点 (镜像既有
`mock.patch.object(gate, "resolve_ci_backend")` / `evaluate_path_coverage` 的模块级符号先例,
见 `pre_merge_gate.py:42-44` 注释), 并明确 24 条既有用例的迁移方式。

---

### M-3 (Major / documentation) — 新增 `main_branch_resolved` 撞已成文的「六键不变」契约, 且在场分支未规定

**锚点**: `aria/skills/phase-c-integrator/SKILL.md:279` + `tests/test_pre_merge_gate.py:598-604`

SKILL.md `:279` 是成文契约:

> `path_coverage` 为 additive 可选键 — 仅评估已执行且流程走到最终 verdict 路径时在场; 各早退分支
> (no-backend / precheck 失败 / backend query 失败 / enabled:false) 保持**六键**不变。

`_OLD_KEYS` (`tests/test_pre_merge_gate.py:598-604`) 把这六键固化, 由
`test_sc11_covered_existing_fields_identical_to_disabled` 与
`test_sc15_schema_additive_and_early_exit_six_keys` 两条测试守着。

Spec §4 / D5 要往 `gate_result` 加 `main_branch_resolved` + 来源, 但:

1. Impact 表只列 `SKILL.md:242`, **没有** `SKILL.md §Output schema (:264-279)` —— 加键必须同步改
   schema 段与那句「六键不变」, 否则文档与代码即刻漂移 (Rule #3)。
2. Spec 未规定新键在**哪些分支**在场。`_build_output` 有 5 条早退路径
   (`pre_merge_gate.py:329` enabled=false / `:339` no-backend / `:346` precheck 失败 /
   `:370` 与 `:393` query 失败)。而 D5 的目的正是「使假绿在 surface 可见」—— 恰恰是早退分支上的绿
   (`:287-295` skip_with_warning 的 `VERDICT_GREEN`) 最需要它。不规定 = 实现者两种写法都合规,
   且大概率写成「只在最终路径在场」, 于是 D5 的目的在最该生效的分支上落空。

**要求**: Impact 补 `SKILL.md:264-279`; §4 明确新键的在场契约 (建议: 无条件在场, 并同步改写 `:279`
那句为「六键 + `main_branch_resolved`」)。

---

### M-4 (Major / architecture) — §3 abort 的插入位置未定, 可能与「非目标」第 5 条正面冲突

**锚点**: `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:328 / :337-339 / :344-352 / :357-360`
+ proposal.md §非目标 第 5 条

`gate_check` 现有早退次序是硬的:

- `:328` `if not cfg["enabled"]:` → 直接 green skip
- `:337-339` `resolve_ci_backend` 返回 None → `_no_ci_output(cfg["no_ci_fallback"])`
- `:344-352` `backend.precheck()` 失败 → fail
- `:357-360` path_coverage 评估 (**这里已经要用 `main_branch`**)
- `:366` (b) 查询

Spec §2/§3 只说「未显式传参时解析」「查 in-flight **之前**核验存在性」, 没说相对上面四个点的位置。这不是
风格问题:

- 若解析/核验放在 `:328` **之前** → owner 显式 `enabled: false` 关掉的闸门会因为 remote HEAD 解析不出
  而 `error`; 无可用 backend 的 `skip_with_warning` 降级也会变 `error`。这**直接违反** Spec 自己的
  §非目标第 5 条「不动 `no_ci_fallback` / stub backend 的既有降级语义」, 也越过了 Rule #8 SOT 的降级
  契约。
- 若放在 `:357` **之后** → path_coverage 会先拿到 `None` 作 `main_branch`, `path_coverage.py:442` 拼出
  `"None...feat/x"` → git diff 失败 → 恒 `unknown`。等于把 C-1 那条腿钉死在 fail-toward-covered,
  修了一半。
- 唯一自洽的位置是 `:344` 之后 `:357` 之前 —— 但那是**读代码推出来的**, 不是 Spec 写的。

**要求**: §2/§3 明确写「解析在 precheck 成功之后、path_coverage 评估之前; 存在性核验在 (b) 查询之前」,
并明确 `enabled=false` 与 `no_ci_fallback` 两条既有早退**不受新 abort 影响** (否则 §非目标第 5 条要撤)。

---

### M-5 (Major / architecture) — 仓内已有同款默认分支解析器且策略相反, Spec 未复用也未论证分歧

**锚点**: `aria/skills/phase-d-closer/scripts/fetch_gate.py:108-128`

```python
def _resolve_default_branch(run, cwd: Path) -> Optional[str]:
    """Resolve the default branch (symbolic-ref → ref probe → name probe → None).

    Mirrors state-scanner sync.py::_resolve_default_branch (replicated to keep
    phase-d-closer self-contained — no cross-skill runtime import).
    """
    rc, out, _ = run(["symbolic-ref", "refs/remotes/origin/HEAD"], cwd, _GIT_QUICK_TIMEOUT)
```

同一 plugin 内**已有两份**该逻辑 (phase-d-closer + state-scanner sync.py), 都硬编码 `origin`, 且失败
时的策略是**继续降级探测 → None → soft skip** (`tests/test_fetch_gate.py:129` 注释:
`symbolic-ref fails + all ref probes fail → cannot resolve → soft skip`), 即 **fail-OPEN**。

本 Spec 要写第三份, 策略 **fail-CLOSED (abort)**。方向上我认同 gate 语境下 fail-CLOSED 是对的 —— 但
Spec 对这两件事都沉默:

1. 既有实现的存在 (复用/不复用及理由 —— 注意既有注释明说「no cross-skill runtime import」是刻意的,
   这是可以直接引用的论据, Spec 却没引);
2. 同一 plugin 内两条相反策略并存的解释 (读者/后续实现者会以为其中一条是 bug)。

更要紧的是 memory `fix-the-class` 的判据「这形状还有几个兄弟位置」: 本 Spec 治的正是「默认分支解析
fail-OPEN」这一类, 而它自己点名的类里另有两个成员未被处置或显式排除。

**要求**: §决策记录加一条 D8 —— 说明为何不复用 `_resolve_default_branch`、为何 gate 语境策略相反、
以及 phase-d-closer/state-scanner 那两处是否在本 change 范围外 (若排除, 给判据)。

---

### M-6 (Major / implementation) — Rule #6 判据适用错: 存在专属 AB 套件, 且指令面确有处方性改动

**锚点**: proposal.md §110-117 (rule6_note) vs
`aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` + `SKILL.md:243` / `:253`

rule6_note 把两个 hunk 都判到 CLAUDE.md 判据表**第一行「描述性」→ substitute**, 理由是「纯 Python,
零 AI 指令面」「零运行时指令流程新增」。两条支撑都不成立:

1. **存在专属 AB 套件, Spec 从未核对**。实存:
   `ab-suite/phase-c-integrator-pre-merge-gate.json`, `skill_name: phase-c-integrator-pre-merge-gate`,
   `version: 1.1.0`, `type: workflow_skill_subextension`, `parent_skill: phase-c-integrator`,
   `fixtures: 7 条`, 外加 `phase-c-integrator-pre-merge-gate-fixtures/` 目录。判据表第三行的
   「套件覆盖外」结论必须先去看这个文件才能下 —— Spec 通篇没提它。这正是 memory `delegate-verify`
   的形状: 结论落在「套件测不到」上, 却没去套件那里核。
2. **指令面不是「零新增」, 是被改动**。`SKILL.md:243` 是处方性运行时指令行 (见 C-2), 必须改;
   `SKILL.md:253` 规定了两条「AI **必须** surface」义务, 其中 (a) 分支 (`green` 来源为
   `not_applicable`) 与 (b) 分支 (`decision == unknown`) 的**触发频率被本 change 直接反转** (C-1:
   本项目今天恒走 unknown 分支, 之后才可能走 not_applicable 分支)。这是运行时指令面的实质变化。

按 CLAUDE.md Rule #6 判据表, 这落在第二行「处方性 · 运行时指令面 / 能测 → 照跑 AB, 零裁量」; 即便认为
存疑, 也落在第四行「拿不准 → 照跑 (宁跑勿豁)」。把它归到第一行去换 substitute 通道, 形状上就是 Rule #10
禁止的自我豁免 (memory `no-self-exempt-gates`) —— 哪怕 Spec 写了「不申请豁免」, substitute 与照跑是
两条不同成本的通道, 选错通道等于降级。

**要求**: 重判 rule6_note —— 先读 `phase-c-integrator-pre-merge-gate.json` 与 `phase-c-integrator.json`
两个套件的实际覆盖面, 再定通道; `SKILL.md:243`/`:253` 那两个 hunk 按处方性单独判。若最终仍走 substitute,
须逐字给出「这两个套件为何测不到本变更行为」的字段级论证, 而不是「纯 Python」这种文件性质论证。

---

### 次要 (Minor)

- **m-1 (documentation)** — `pre_merge_gate.py:21` 模块 docstring 仍写 `[--main-branch main]`,
  是同文件第三处 `main` 字面; Impact 只说「两处缺省」。
- **m-2 (documentation)** — `path_coverage.py:19` 携带与 `SKILL.md:242` 同义的契约句
  (`main_branch 由调用方显式传真值 (不依赖 "main" 默认)。`), 落地后同样陈旧, 不在 Impact。
- **m-3 (testing)** — SC-6「`ls-remote` 自身失败 → 重试后仍失败 ⇒ error」没有规定**重试次数与退避**。
  同文件既有 `RETRY_BACKOFF = (5, 15, 45)` / `MAX_RETRY_ATTEMPTS` (`ci_backends/aether.py:38-39`)
  可直接复用; 不钉死则「重试几次」由实现者裁量, 且单测无法写确定断言。

### 核过但**没有**问题的点 (免得下一轮重复劳动)

- `pre_merge_gate.py:300` / `:427` 两处缺省, 逐字与 Spec 引用一致 ✅
- `ci_backends/aether.py:117-135` 的合流点分析正确; `:124` `data.get("runs") or []` 确是唯一收敛处,
  「后端结构上无法区分」的判断成立 ✅
- `path_coverage.py` 规则 1 (`:446-447`) 确为 `unknown` / fail-toward-covered, §订正 line 52-58
  对 #137 原文的更正**是对的** ✅
- 测试基线 111 = `test_ci_backends.py` 25 + `test_path_coverage.py` 40 + `test_pre_merge_gate.py` 46,
  实测吻合 ✅ (`run_all_tests.sh` 实际在 `aria/skills/run_all_tests.sh`, 非 skill 目录内 —— 不影响结论)
- D3「backend 是薄适配器 ×N」属实: `BACKENDS = [AetherBackend, GitHubActionsBackend]`
  (`ci_backends/__init__.py:17`), GHA 是 NIE stub (`github_actions.py:37/45`); 「放 gate 层一处即对
  所有 backend 生效」的分层论证**成立** ✅ (残余问题见 M-1 第二层, 是探针平面问题不是分层问题)
- §非目标对 aria-plugin #136 (子模块服务端合并) 的切分干净, 与 CLAUDE.md 硬约束 1 无耦合冲突 ✅

---

## Verdict

**FAIL** — 2 Critical + 6 Major + 3 Minor。

判据: FAIL = ≥1 Critical。两条 Critical 都不是「方案有风险」而是「Spec 写错了」——
C-1 的范围声明与 `pre_merge_gate.py:359` 直接矛盾, C-2 的承重引用指向了另一个机制的规范句。二者都会
让 Phase B 按字面执行时改错对象。

方案本体 (fail-CLOSED 解析 + 存在性核验 + 回显) 我**支持**, 不需要重做; 需要的是范围订正 + 枚举补齐 +
三处欠定钉死 (`<remote>` / 插入位置 / 重试参数) + Rule #6 重判。修完这些, 我预期 R2 可收敛。

---

## 轮次记录

### Round 1 (2026-08-08, tech-lead)

**镜头**: 架构与流程 —— D1-D7 自洽性 / §3 承重条款的分层论证 / §非目标 边界 / 与 #136·Rule #8 SOT·
CLAUDE.md 硬约束的耦合 / ship 路径与 Rule #6 判据适用。

**实读落点** (全部亲读, 无一条据 Spec 自述转述):

| 文件 | 读的范围 | 用于 |
|---|---|---|
| `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` | 1-179 全文 | 被审对象 |
| `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | 1-445 全文 | C-1 / M-2 / M-3 / M-4 / m-1 |
| `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` | 1-270 全文 | 核 §Why 合流点 (通过) |
| `aria/skills/phase-c-integrator/scripts/path_coverage.py` | 1-60, 400-507 | C-1 / m-2 / 核 §订正 (通过) |
| `aria/skills/phase-c-integrator/SKILL.md` | 225-266 + `:242` 分句 + `:279` | C-2 / M-3 / M-6 |
| `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` | 598-700 + 全文机械统计 | M-2 / M-3 |
| `aria/skills/phase-d-closer/scripts/fetch_gate.py` | 100-160 | M-5 |
| `aria/skills/phase-c-integrator/scripts/ci_backends/__init__.py` / `github_actions.py` | BACKENDS + stub 签名 | 核 D3 (通过) |
| `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` | 顶层字段 | M-6 |

**实跑的只读命令** (零写入, 零 commit, 零 push):

- `git remote -v` (主仓 + `aria/`) → 双远程确认 → M-1
- `git symbolic-ref refs/remotes/{origin,github}/HEAD` → origin=master RC=0 / github RC=128 → M-1
- `git diff --name-only --no-renames -z main...HEAD` (在 `aria/`) → RC=128 → C-1 的方向实证
- `grep -rn "main_branch\|--main-branch"` 全 `aria/` → 枚举面 → C-2 / m-1 / m-2
- python3 静态统计 `gate_check(...)` 调用 24 处 / 含 `main_branch` 0 处 → M-2
- `grep -c 'def test_'` × 3 文件 = 25+40+46 = 111 → 核基线 (通过)

**三个复发失败形状的专项核查结果**:

| 形状 | 结果 | 落点 |
|---|---|---|
| 1. 委派而不核实目标 | **命中 ×2** | M-1 (§3 核验的平面 ≠ 被守护查询的平面, 未核 backend 侧) / M-6 (判「套件测不到」却没读那个存在的套件) |
| 2. 枚举不完整 | **命中 ×2** | C-2 (漏 `SKILL.md:243` 这个唯一带 `main` 字面的指令行 + `path_coverage.py:19` + `pre_merge_gate.py:21`) / M-3 (漏 `SKILL.md:264-279` schema 段 + 新键在场分支未枚举) |
| 3. 假自陈 | **命中 ×2** | M-2 (「既有用例逐字不改」vs 24/24 依赖旧缺省 + `test_sc12` 逐字断言 `main_branch="main"`) / C-1 (D7「无行为面扩大」vs 首次打开 not_applicable→green 通路) |

**收敛判断**: 本轮不收敛 (`converged: null`, 由编排层四元组比较决定)。R2 前置条件 = C-1/C-2 订正 +
M-1/M-4 的欠定钉死。M-6 若走「照跑 AB」路线, 其结论不阻塞 Spec 收敛但阻塞 ship。
