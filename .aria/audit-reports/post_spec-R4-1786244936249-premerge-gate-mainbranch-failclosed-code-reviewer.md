---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T03:23:45.974Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — code-reviewer 审计报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (263 行, R3-fix 范围重定版)
镜头: D1 路径收敛真实性 / 新写三段 (§4 §5 §6) 自身缺陷 / 假自陈回源 / 恒红恒绿对偶 / D1-D9 交叉一致性 / 修实例不修类
所有 finding 均已实读锚点或实跑验证; 推翻性陈述均附实跑输出。

---

## 审计结论

### 先说做对的部分 (回源全过)

以下带数字/行号的断言我**逐个回源, 全部属实**, 不再重复列举为问题:

| Spec 断言 | 实测 | 结论 |
|---|---|---|
| `SKILL.md:167` `:243` 各含 `--branch main` (SC-1 今日 2) | `grep -c -- '--branch main'` = **2**, 行号命中 167/243 | ✅ |
| `SKILL.md:270` 含 `"branch": "main"` (SC-2 今日 1) | `grep -c '"branch": "main"'` = **1** @ 270 | ✅ |
| 「同行含 `python3` 与 `--main-branch` 的行数为 0」 | `grep -cE 'python3.*--main-branch\|--main-branch.*python3'` = **0** | ✅ |
| `pre_merge_gate.py` 出现 4 次 (`:262` `:308` `:310` `:316`) | 实测 4 次, 行号逐一命中 | ✅ |
| `:262` 是 §C.2.4 段内 (218-303) 唯一提及 | 308/310/316 均在 §C.2.4.X (306+) | ✅ |
| SC-4 三 pattern 今日 1/1/1, SC-5 今日 1 | 实跑 `1 / 1 / 1 / 1` | ✅ |
| `gate_check` 内六项全在 | 337 `resolve_ci_backend` / 344 `precheck` / 358 `evaluate_path_coverage` / 366 `query_branch_in_flight` / 389 `query_pr_ci` / 401 `compute_verdict` | ✅ |
| `aether.py:117-135` `query_branch_in_flight` 只在 aether 自身失败时抛 | 实读 117-135, 仅 `not ok` / 非 list 两处 raise | ✅ |
| `gate_check:378-386` not_applicable 通路存在 | 实读, 逐行吻合 | ✅ |
| `pre_merge_gate.py:47-49` / `SKILL.md:267` / `:252-255` / `gate_state_helper.py:32-34` / `:147` 四处封闭枚举 + 原样写入 | 逐处实读, **行号全部精确** | ✅ |
| `ci_backends/base.py:29` `not_found` + `SKILL.md:279` 逐字「gate 输出目前不产生」 | 实读吻合 | ✅ |
| 24 处 `gate_check(` 调用点, 显式传 `main_branch` 的 0 处 | `grep -c` = 24; 全库唯一 `main_branch=` 出现在 `:669`, 是 `assert_called_once_with` 的**断言**不是调用 | ✅ (§Impact 写「断言由 main 改 master」也对) |
| 111 tests = 46 + 25 + 40 | `def test_` 实测 46 / 25 / 40 | ✅ |
| `test_sc12` @ `:663`, `test_sc22` @ `:710` | 实读, 行号精确 | ✅ |
| Rule #6 SOT 逐字「`description` 或指令流程变动 ⇒ 一律第二行」 | `skill-benchmark-exemption.md:33` 逐字吻合 | ✅ |
| `fetch_gate.py` 第三级兜底逐字 `("master","main")` | `fetch_gate.py:55` 吻合 | ✅ |
| **D4 锚定 pattern 的 R2 实证** | 受控裸仓复跑: 只有 `refs/heads/wip/master` 时 `--heads origin master` → **RC=0**(命中 wip/master), `--heads origin refs/heads/master` → **RC=2** | ✅ **完全成立** |

D4 是本版最扎实的一条: 我在 `/tmp` 独立重建裸仓复跑, 尾段 glob 的 fail-OPEN 与锚定后的 RC=2 都复现了。§6 的四处封闭枚举点位也是我见过最精确的一组引用 (5/5 行号无漂移)。

### 但承重项 D1 没有立住

本版把承重项换成 D1, 而 D1 的**三个必要条件同时不成立**: 路径没收敛干净 (C1) · 唯一入口在本项目主要合并场景启动不了 (C4) · 它的承重断言 SC-3 对自己给的逐字命令实测为 0 (C2)。再叠加 §测试卫生 对 `test_sc22` 的事实陈述被实验推翻 (C3), 按本 Spec 原样实施会产出一个「AI 仍能照抄裸命令 + 唯一入口跑不起来 + 承重断言恒红 + 卫生守卫意外变红」的组合。

---

## Findings

### Critical

#### C-1 D1 只收敛了两份实现里的**一份半**, `SKILL.md:167-168` 的裸命令块原样留存, 且无任何 SC 能发现它

- **锚点**: `aria/skills/phase-c-integrator/SKILL.md:161-169` (实读) vs proposal §1 (`:60-76`) / §Impact (`:222`) / SC-1 (`:174`)
- **事实**: 本 skill 对 C.2.4 的命令面其实有**三处**, 不是 Spec 说的两处:

  | # | 位置 | 形态 | §1 是否处置 |
  |---|---|---|---|
  | (i) | `SKILL.md:161-181`, 在 `## 执行流程` → `### 步骤执行` 的 yaml 内, 小标题逐字 **`primitive 调用:`** | `- aether ci status --branch main --in-flight --json`(`:167`) + `- aether ci status --branch <PR_BRANCH> --json`(`:168`) | ❌ **仅换字面量** |
  | (ii) | `SKILL.md:238-255` `**执行流程**:` 步骤 1-5 | 逐条裸命令 | ✅ 移入折叠块去命令 |
  | (iii) | `pre_merge_gate.py` | helper | — |

  §Impact 对 `:167` 的处置逐字只有「`:167` `:243` `:270` **字面量**」——即把 `main` 换成 `<MAIN_BRANCH>`。而 R3 自己的结论 (proposal `:37`) 是: **「把 `:243` 的 `main` 换成占位符也没用 —— 占位符被逐字执行返回同样的空集」**。同一条推理原样适用于 `:167`, Spec 却对 (i) 只用了被自己否决的那个药方。
- **且无机械兜底**: SC-1 只数 `--branch main`, 占位符替换即满足 → **SC 全绿而 (i) 完好无损**。§1 写的「去掉**全部**可执行命令字面量」这个性质, 全表**没有任何一条 SC 断言它**; 折叠块内 `:244` 步骤 4 的 `aether ci status --branch <PR_BRANCH> --json` 同理不被任何 SC 覆盖 (SC-1 pattern 不匹配)。
- **为什么重要**: (i) 位于 skill 的**主执行流程 yaml**, 排在详细段之前, 标题就叫「primitive 调用」——它比 (ii) 更像「该执行什么」的权威列表。D1 的整个价值主张是「收敛成一条路径」; 留着 (i) 就等于把 R3 的根因原样搬到上一屏。
- **修法**: (a) `:166-169` 的 `primitive 调用:` 整块改为 `helper 调用: python3 <...>/pre_merge_gate.py --pr-branch ... --main-branch ... --remote origin` (与 §1 同一条命令); (b) 新增零裁量 SC: `grep -c 'aether ci status' SKILL.md` 期望 **0** (今日实测 3 @ `:167` `:168` `:243`) —— 这才是 §1 那句「去掉全部可执行命令字面量」的可证伪形态。

#### C-2 SC-3 (自称承重断言) 对 §1 给的**逐字**命令块实测 = 0 ⇒ 正确实施后恒红

- **锚点**: proposal `:67-72` (§1「新增的唯一执行入口 (**逐字**)」) vs `:176` (SC-3)
- **实跑**(把 proposal 69-72 行原样抽出成文件后跑 SC-3 自己的 pattern):

```
$ sed -n '69,72p' proposal.md > sc3_probe.md
$ grep -cE 'python3.*--main-branch|--main-branch.*python3' sc3_probe.md
0
$ grep -c 'python3' sc3_probe.md ; grep -c -- '--main-branch' sc3_probe.md
1
1
```

  原因是 §1 的命令用 `\` 续行, `python3` 在第 1 行、`--main-branch` 在第 2 行, 而 SC-3 是**同行**匹配。
- **为什么重要**: SC-3 是 Spec 自己标注的「**承重断言, 对应 D1**」, 且 SC 表开篇逐字写「本表**不留裁量空间**」。现在的状态是: 一个**完全正确**地实施了 D1 的 Phase B 会拿到 SC-3 红。实施者只有两条路 —— 改命令排版 (无害) 或**放宽 SC-3** (有害: 一旦退回 `grep -c 'pre_merge_gate.py' ≥ 2` 之类, 就正好落回 SC-3 自己在 `:176` 警告的「恒绿零信息量」)。R3 烧掉三个版本的教训就是「断言没断言它声称的东西」, 这里是同一形状。
- **修法**: 二选一并写死 —— (a) §1 命令改为**单行**(去掉 `\` 续行); 或 (b) SC-3 改成对**代码块**求值的形态, 例: `awk '/^```bash/,/^```/' SKILL.md | grep -c -- '--main-branch'` ≥ 1 且 `... | grep -c 'pre_merge_gate.py'` ≥ 1 同块。不要只删同行约束。

#### C-3 §测试卫生 对 `test_sc22` 的事实陈述**为假**; 处方是 no-op, 真实后果方向相反 (恒红而非恒绿), 并与 SC-6 互斥

- **锚点**: proposal `:188` vs `tests/test_pre_merge_gate.py:710-724` (实读) + `scripts/path_coverage.py:47` (实读)
- **Spec 原文** (`:188`): 「`test_sc22...` 当前 patch 的是 **`pc_module.subprocess`** (path_coverage 模块的), **看不见** gate 层新增的 subprocess。本 change 须把该守卫**扩到 patch `pre_merge_gate` 模块自己的 `subprocess`**, 否则它对新代码恒绿。」
- **推翻**: `path_coverage.py:47` 是 `import subprocess`(模块对象, 非 `from subprocess import run`), 因此 `mock.patch.object(pc_module.subprocess, "run", _forbidden)` 改的是**全局唯一的 `subprocess` 模块对象**上的 `run` 属性, 对**所有**模块生效。受控实验:

```
a_mod.py: import subprocess; def call_a(): subprocess.run(["true"])
b_mod.py: import subprocess; def call_b(): subprocess.run(["true"])
with mock.patch.object(a_mod.subprocess, "run", forbidden): b_mod.call_b()
→ b_mod BLOCKED -> BLOCKED   (即: 守卫是全局的)
```

- **三个连锁后果**:
  1. 处方「扩到 patch `pre_merge_gate` 模块自己的 `subprocess`」= **对同一个对象再 patch 一次** = no-op, 花掉的工时买不到任何覆盖。
  2. 真实后果**方向相反**: gate 层一落 `subprocess.run(["git","ls-remote",...])`, `test_sc22:723` 那句 `gate.gate_check(pr_branch="feat/x")` 就会撞上 `_forbidden` → `AssertionError("real git subprocess spawned in unit suite")` → **`test_sc22` 直接变红**。Spec 预算里没有这项工作, 更没说它会红。实施者在毫无预期地看到一条名叫「卫生守卫」的测试变红时, 最省事的解法就是**删弱它** —— 那正是这条守卫存在的理由被消灭。
  3. 与 SC-6 结构互斥: `:186` 要求 SC-6/7/8「**不得**用 mixin 打桩 —— 它们要验的正是**真实 `ls-remote` 行为**」, 而 `test_sc22` 的名字与断言逐字是「**no real git subprocess in suite**」。Spec 的 §待R4审 item 4 正好问了这个冲突, 而 §Success Criteria 用一个错误机制回答了它。
- **修法**: (a) 删掉 `:188` 那句错误陈述; (b) 明确 `test_sc22` 的 with-块内必须把新的分支核验 stub 掉 (例: `mock.patch.object(gate, "_verify_branch_exists", return_value=(True, None))`), 并在 Spec 里把它计入工作量; (c) 给 `test_sc22` 的「suite-wide 无真 git」不变量与 SC-6 的「真 `ls-remote`」划一条显式边界 (例: SC-6 走独立 TestCase 且不继承该 mixin, 并把守卫名/docstring 改成「gate_check 单元路径内无真 git」以免名实不符)。

#### C-4 「唯一执行入口」在子模块根**启动不了**, 而子模块合并是本项目被 CLAUDE.md 硬约束钉死的主场景

- **锚点**: proposal `:70-71` (§1 逐字命令) vs `SKILL.md:242` (执行上下文契约) + CLAUDE.md「多远程推送 — 约束 1」
- **实跑**:

```
$ echo "ARIA_PLUGIN_ROOT=[${ARIA_PLUGIN_ROOT:-<UNSET>}]"
ARIA_PLUGIN_ROOT=[<UNSET>]

$ python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" --help ; echo RC=$?
usage: pre_merge_gate.py [-h] --pr-branch PR_BRANCH [--main-branch MAIN_BRANCH] ...
RC=0

$ cd /home/dev/Aria/aria-orchestrator && python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" --help ; echo RC=$?
python3: can't open file '/home/dev/Aria/aria-orchestrator/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py': [Errno 2] No such file or directory
RC=2
```

  `ARIA_PLUGIN_ROOT` **全仓从未被赋值** (`grep -rn 'ARIA_PLUGIN_ROOT='` 零命中; 仅 6 处 `${ARIA_PLUGIN_ROOT:-aria}` 消费点), 所以恒走 `aria` 相对回落。`CLAUDE_PLUGIN_ROOT` 在本环境同样未设 (换成它结果一样)。
- **为什么重要**: `SKILL.md:242` 逐字规定 C.2.4 的执行上下文是「在执行 C.2 合并的**目标仓根**内调用 (子模块合并 → **子模块根**)」; CLAUDE.md「约束 1」又逐字规定「子模块 (aria / standards / aria-orchestrator) 的分支合并**必须本地** `git merge`」。三个子模块 + 主仓 = 本项目 4 类合并里 **3 类**的 cwd 是子模块根, 在那里唯一入口**跑不起来**。而 D1 恰恰把 `:238-255` 的散文步骤降级为「⛔ 不要手工执行」的折叠块 —— 唯一被授权的动作失败, 且 SKILL.md 里没有任何 helper-not-found 的降级契约。AI 面对「唯一入口报 `No such file`」只有两种反应: 硬停 (对 3/4 的合并恒红) 或**自行改写路径/重新拼裸命令** —— 而 C-1 留着的 `:167` 正好在等它。D1 的收敛主张在本项目最常见的场景下不成立。
- **注**: `:262` 今日已用同一路径表达式, 但它是「**Helper 实现**: 路径」式的**指引**; D1 把它升格为**唯一可执行命令**, 承重性质是本版新引入的。
- **修法**: §1 必须给出路径解析契约, 三选一并写死: (a) 用 `CLAUDE_PLUGIN_ROOT` 并在 Spec 里承认 `:737` 先例用的就是它 (见 M-2); (b) 命令前置一步「解析 plugin root: `PLUGIN_ROOT=$(git rev-parse --show-superproject-working-tree || git rev-parse --show-toplevel)/aria`」; (c) 明确要求用绝对路径。另须补一条 SC: 从**子模块根** cwd 执行 §1 逐字命令, 断言能启动 (今日 RC=2 ⇒ 必红)。

### Major

#### M-1 §6 的 `gate_error` 示例逐字含 `"branch": "main"`, 与 SC-2 期望 0 直接对撞

- **锚点**: proposal `:141` vs `:175` (SC-2) vs `:222` (§Impact 「`:267` schema 增 `gate_error`」)
- **实跑**: `grep -n '"branch": "main"' proposal.md` → `141:  "branch": "main",`; SC-2 的 pattern 逐字就是 `'"branch": "main"'`, 期望 SKILL.md 内 **0**。
- §Impact 明确要求把 `gate_error` schema 搬进 `SKILL.md:267` 的 Output schema 块。照搬 → SC-2 红; 改写 → 违反 §6 逐字。两条零裁量条款互斥。
- **修法**: §6 示例改 `"branch": "<MAIN_BRANCH>"`(与 D3 占位符统一同步), 并把 `message` 示例里的 `'main'` 一并占位符化。

#### M-2 §1 引 `SKILL.md:737` 作「**强制** helper 调用范式」先例, 与该处实读不符 (它是 advisory, 且用另一个环境变量)

- **锚点**: proposal `:74` vs `SKILL.md:734-742` (实读)
- **实读 `:737` 上下文**: `:734` 「…**判断**"本 cycle 收尾后是否该暂停换会话"」→ `:737` 命令 → `:740` 逐字「`used_percentage` … `>85%` → **建议** merge 完成后即暂停…**advisory, 不自动中断**」。这是一条 advisory 诊断调用, **不是**「唯一执行入口 / 强制」范式。
- 且 `:737` 用的是 **`${CLAUDE_PLUGIN_ROOT:-aria}`**, 而 §1 写 `${ARIA_PLUGIN_ROOT:-aria}` —— 声称「本条**沿用**」却换了变量前缀。全仓 `CLAUDE_PLUGIN_ROOT` 100 处 / `ARIA_PLUGIN_ROOT` 6 处 (且全是消费点, 无赋值点)。
- **为什么重要**: D1 是本版唯一承重项, 它援引的唯一先例既不承载「强制」语义也不同形。「有先例」这句话正是让实施者跳过路径解析思考的东西 —— C-4 就是这么漏出来的。(同 memory `delegate-verify` / `spec-precedent-verify-execution-history` 的形状。)
- **修法**: 要么删掉先例主张 (D1 靠自身理据即可成立), 要么改写为「`:737` 提供的是 helper 调用**书写形态**的先例 (不含强制语义), 环境变量沿用其 `CLAUDE_PLUGIN_ROOT`」。

#### M-3 §4 未定义核验的**仓上下文**, 与 C-4 叠加后极可能「在父仓核验子模块的分支」→ 恒绿 fail-OPEN

- **锚点**: proposal `:96-100` (核验命令) / `:115` (已知残留限制) vs `SKILL.md:242` (执行上下文契约)
- **事实**: §4 给的命令是 `git ls-remote --exit-code --heads <remote> "refs/heads/<main_branch>"` —— **无 `-C`, 无 repo-root 参数**, 完全依赖进程 cwd。§4 的「已知残留限制」只声明了 git 平面 vs API 平面不同源, **没有**声明「核验查的是哪个仓」这件事完全未受控。
- **叠加效应**: C-4 使唯一入口在子模块根跑不起来 ⇒ 实施者/AI 最自然的绕法是**回到主仓根执行**。此时合并的是 `aria` 子模块, 而 `ls-remote` 查的是 **Aria 主仓的 origin** —— 两个仓都有 `master`, 于是 RC=0, 核验「通过」, 而它压根没看目标仓。这正是本 Spec 要治的病 (「查询与核验用的不是同一个东西」) 换了个平面复发, 且方向是 **fail-OPEN**。
- **修法**: §4 命令加显式仓根 (`git -C "<REPO_ROOT>" ls-remote …`), `gate_check` 增 `repo_root` 参数或明写「核验必须与 `evaluate_path_coverage` 共用同一 cwd 契约, 且 Phase B 须加一条断言证明二者同源」; 「已知残留限制」段补一句仓上下文声明。

#### M-4 §4「其他非零」的判据援引了一个**不含实际取值**的区间 (`exit 1-126`), 且被援引条款自带 `127 → no_ci_fallback` 这条 fail-OPEN 分支

- **锚点**: proposal `:109` / D5 `:160` vs `SKILL.md:259-260` (实读)
- **`SKILL.md:260` 逐字**: 「exit-code 映射 (**per-backend, Aether 示例**): `0` = success / `1-126` = aether 错误 → `fail` / **`127` = binary not found → `no_ci_fallback`** / `-SIGTERM` = subprocess timeout → retry …」
- **实测最常见的失败取值不在区间内**:

```
$ git ls-remote --exit-code --heads nosuchremote "refs/heads/master" >/dev/null 2>&1 ; echo RC=$?
RC=128
```

  远端不可达 / remote 名不存在 / 认证过期 (CF Access 掉线) 全部落 **128**, 而援引的规范只覆盖 1-126。D5 自己逐字写着「**不得越界援引**」, 这里正是越界援引。
- **更硬的一点**: `:260` 里的 `127 → no_ci_fallback` 若被一并「复用」, 默认 `skip_with_warning` ⇒ **verdict 变 green**。承重的 fail-CLOSED 核验在自己的兜底路径上重新长出 fail-OPEN (同 memory `fix-recurs-in-fallback`)。
- **另有未枚举分支**: `subprocess.run(["git",...])` 在 git 不可执行时抛的是 `FileNotFoundError` 而非 RC=127; §4 的四行表 (0 / 2 / timeout / 其他非零) 对**异常**路径零覆盖。
- **修法**: §4 自带完整封闭映射, 不援引 `:260`: `RC==0 → 存在` / `RC==2 → not-found(fail)` / `其余任何非零 (含 127/128/≥128) → verify-failed(fail), 不重试, **显式禁止**路由到 `no_ci_fallback`` / `OSError·FileNotFoundError → verify-failed(fail)` / `TimeoutExpired → 按 :259 重试 3 次后 fail`。timeout 值须点名沿用 `primitive_call_timeout_seconds`(`SKILL.md:258` 逐字「强制」), 否则会写出无 timeout 的 `subprocess.run` 把 gate 挂死。

#### M-5 `gate_error` 是一个**没有消费者**的诊断字段: 文档化的 fail surface 通道是 `raw_message`, 而 §6 明确把信息只放进 `gate_error`

- **锚点**: proposal `:131-148` (§6) / `:227` (follow-up (3)) vs `SKILL.md:255` (实读) + `gate_state_helper.py:145-152` (实读)
- **事实链**: `SKILL.md:255` 逐字「`fail` → BLOCK + 输出 verdict + **`raw_message`**」; `gate_state_helper.py` 写入 `gate_state` 的键是固定七项 (`name/status/started_at/retry_count/next_check_at/in_flight_runs/**raw_message**`), **无 `gate_error` 位置** —— Spec 的 follow-up (3) 自己承认了这一点, 却仍把 `message` 只放进 `gate_error`, 理由是「`message` 是 SC-6 的断言对象」。
- **后果**: 单测能看见 `gate_error.message` (SC-6 绿), 运行时它在 workflow-runner 持久化那一层被丢掉, 操作者拿到的是 `verdict=fail` + 一个 Spec 未规定内容的 `raw_message`。这就是「有记录 ≠ 有路由; 无人消费的诊断字段 = 静默」(memory `fix-recurs-in-fallback`)。对照 v1.65.0 的 `path_coverage.decision == unknown` —— 那条是配了 `SKILL.md:253` 的**显式 surface 义务**才不静默的。
- **修法**: §6 规定 `gate_error` 在场时 `raw_message` **必须**同时被置为同一句人读文案 (加一条 SC 断言 `message in raw_message`), 并给 `gate_error` 补一条与 `:253` 同形的 AI surface 义务; follow-up (3) 保留但不作为借口。

#### M-6 SC-10 这条负控没有强制失败注入 ⇒ 它自己可以恒绿, 测不出 D7 的顺序错误

- **锚点**: proposal `:183` (SC-10) / `:162` (D7) / `:117-129` (§5)
- **事实**: SC-10 的场景只写「`enabled=false` 早退」, 期望「保持六键、无 `gate_error`、不因核验失败变 fail」, 「怎么会红」写「把核验放到早退之前的实现必红」。但这句只在 fixture **让核验真的失败**时才成立。一个把核验错误地前置、同时 SC-10 用的是「分支存在」的桩的实现, 会返回 green + 六键 → **SC-10 绿**, D7 完全没被守住。
- 判据「该信号在健康常态下应是什么值」: SC-10 现在的形态在**健康与不健康两种实现下都是绿**, 零信息量。
- **修法**: SC-10 必须钉死 fixture: 「`enabled=false` **且**核验会失败 (`ls-remote` 桩 RC=2 / 受控裸仓只有 `wip/master`)」→ 期望仍 green + 六键 + 无 `gate_error` + **`ls-remote` 未被调用** (`assert_not_called`, 这条才是 D7 的因果机制)。同样处理建议施加于 no-backend / precheck 两个早退 (§5 列了三个, SC 只覆盖一个)。

### Minor

#### m-1 §5 的两处行号漂移

`:124` 写「`:356 evaluate_path_coverage(main_branch=...)`」, 实读 `:356` 是 `pc: dict[str, Any] | None = None`, 调用在 `:358`; `:122` 写「`:344` precheck 失败 → 早退」, 实读 `:344` 是 `ok, precheck_err = backend.precheck()`, 早退在 `:345-352`。在一份把「零裁量 / 逐字」当卖点的 Spec 里, 插入点图应逐字对齐 (memory `spec-frontmatter-reflects-reality`)。

#### m-2 §6「三个早退」与 `SKILL.md:279` 逐字的**四类**早退不一致

`SKILL.md:279` 逐字: 「各早退分支 (no-backend / precheck 失败 / **backend query 失败** / enabled:false) 保持六键不变」= 4 类。proposal `:148` 只说「三个早退分支保持既有六键不变」。§Impact 要求同步改写 `:279`, 按 §6 的三类改写会把 `backend query 失败` 从契约里掉出去 (`test_sc15` `:691-697` 正在守它)。

#### m-3 `:186` 与 SC-7/SC-8 自相矛盾

`:186` 写「SC-6/SC-7/SC-8 …**这三条不得**用 mixin 打桩 —— 它们要验的正是真实 `ls-remote` 行为」, 但 SC-7 (`:180`) 自带括注「(mock)」、SC-8 (`:181`) 自带「(mock; 须 mock `time.sleep`)」。真实 `ls-remote` 无法稳定产出「非 0 非 2」或确定性 timeout。应改为「仅 SC-6 用受控裸仓真调用; SC-7/SC-8 打桩」。

#### m-4 §待R4审 item 3 描述的 SC-3 形态是**上一版残留**, 与 SC-3 正文互相打脸

`:262` 写「SC-3 那条断言的形态 (`grep -c 'pre_merge_gate.py'` ≥2 + 同行含 `python3` 与 `--main-branch`)」, 而 SC-3 正文 `:176` 逐字「⚠️ **不得附加**「`grep -c 'pre_merge_gate.py'` ≥2」之类的从句」。审阅指引里挂着被正文明令禁止的形态, 会把 R4/Phase B 引向错误对象。

#### m-5 Rule #6「过两套件」对 D1 结构上零信息, `:202` 的「覆盖不足」表述偏轻

实测 `ab-suite/phase-c-integrator.json`: `aether` / `C.2.4` / `in-flight` / `pre_merge` 四个 token 出现次数**均为 0** (不是「不足」, 是零)。`ab-suite/phase-c-integrator-pre-merge-gate.json` **没有 `evals` 键**, 它是 fixture→unit-test 映射清单 (`fixtures` / `primary_pass_gate_metric`), 跑 AB 与它是两种东西。D8 判第二行「照跑 AB, 零裁量」在 SOT 上是对的 (`skill-benchmark-exemption.md:33` 逐字支持), 不必降档 —— 但 Spec 应诚实写成「两套件对 D1 改动面结构上零覆盖, 本次 AB 结果不构成 D1 的证据; 证据由 SC-1/SC-3(修正后)/SC-6 承担」, 而不是「覆盖不足」。

#### m-6 「修实例不修类」的类枚举不全

`:214` 只点名 `fetch_gate.py`; follow-up (2) 提的 `sync.py` 我核到了实处 (`aria/skills/state-scanner/scripts/collectors/sync.py:48-49` 同形 `refs/remotes/origin/master` + `/main` 回落列表, 引用成立)。但**同形第三处未被枚举**: `aria/skills/state-scanner/lib/worktree_manager.py:170` `base_branch: str = "master"` —— 与 `pre_merge_gate.py:300` 完全同形的硬编码主分支缺省。好消息是 `collectors/multi_remote.py:800` 走的是 `main_branch is None → 短路` 的正确形态, 可作为 follow-up 的参照实现。

---

## Verdict

**FAIL** (4 Critical + 6 Major + 6 Minor)

**什么阻塞进入 Phase B** (最后一轮, 明确点名):

| 必须修掉才能进 B | 理由 |
|---|---|
| **C-1** | 承重项 D1 只做了一半; 留下的 `:167-168` 恰是 R3 根因的同一形状, 且无 SC 能发现 |
| **C-2** | D1 的承重断言对 D1 的逐字产物恒红; 不修则 Phase B 必须在「零裁量」表上行使裁量 |
| **C-3** | Spec 对现有代码的事实陈述被实验推翻, 处方是 no-op 且真实后果反向; 照做会诱导删弱卫生守卫 |
| **C-4** | 唯一入口在 3/4 的合并场景启动不了, D1 的收敛主张在本项目不成立 |
| **M-1** | 两条零裁量条款直接对撞 (§6 示例 vs SC-2), 实施者必然卡住 |
| **M-3 / M-4 / M-5** | 三条都在新写的 §4/§6 里重新引入 fail-OPEN 或静默 (核验错仓 / 127→no_ci_fallback / 诊断无路由) —— 与本 Spec 的存在理由直接冲突 |

**不阻塞** (可在 Phase B 内顺手修或转 follow-up): M-2、M-6、m-1..m-6。

**给 owner 的一句话**: 范围重定的**方向**是对的 —— R3 找到的根因 (AI 走散文那份) 成立, D4 的锚定 pattern 我独立复现验证也成立, §6 的封闭枚举点位是全文最精确的一段。问题在于 D1 这个新承重项是**这一版才写的、且没被任何机械信号守住**: 它的收敛主张有个未处理的第三处 (C-1), 它的唯一入口在本项目跑不起来 (C-4), 它的承重断言对自己恒红 (C-2)。这三条都是「新表面第一次被审」的典型产出, 不是 Spec 质量在退步。建议**不进 Phase B**, 做一轮定向修订 (预计改动集中在 §1 / SC-3 / SC-10 / §测试卫生 / §4 五处), 因为已到 max_rounds, 修订后是否再审由 owner 裁定。

---

## 轮次记录

| 轮次 | 席位 | 对象 | 本轮性质 |
|---|---|---|---|
| R1 | 5 席 | v1 (helper 缺省加固) | 范围内审计 |
| R2 | 5 席 | v2 | 范围内审计; 产出 `ls-remote` 尾段 glob 受控实证 (本轮已独立复现, 成立) |
| R3 | 5 席 | v3 | **推翻前三版范围** —— AI 走 SKILL.md 散文那份实现, helper 加固对真实路径无效 |
| **R4** | code-reviewer (本报告) | **v4 范围重定版, 承重项换为 D1** | **D1 面首次被审**。D1 三项必要条件均不成立 (C-1 残留裸命令 / C-2 承重断言恒红 / C-4 唯一入口不可达) + §测试卫生 事实陈述被实验推翻 (C-3)。verdict FAIL |

**本轮方法**: 全部 finding 均基于实读锚点或实跑; 其中 4 项由受控实验独立验证 —— (1) `/tmp` 裸仓复现 `ls-remote` 尾段 glob (D4 成立); (2) 抽出 proposal 69-72 行原样跑 SC-3 pattern (C-2); (3) 双模块 `patch.object` 全局性实验 (C-3); (4) 主仓根 vs 子模块根实跑唯一入口 (C-4)。**未修改本仓任何文件, 未 commit/push。**
