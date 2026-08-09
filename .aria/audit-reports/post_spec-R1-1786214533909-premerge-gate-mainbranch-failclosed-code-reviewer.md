---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T19:03:29.173Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — code-reviewer 席位审计报告

**被审对象**: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (Level 2, 179 行)
**工作树**: `/home/dev/Aria` @ `98ad1f5` (branch master)
**镜头**: 修复类 change 的自反性缺陷 (fail-OPEN 在自己新写的分支复发 / 修实例不修类 / 假自陈 / 枚举不完整 / 恒红恒绿对偶)
**方法**: 全部 finding 均以实读源码行或实跑命令输出为锚, 不转述 Spec 自述。

---

## 审计结论

Spec 对**缺陷本体的诊断是准确的**, 而且它最容易被质疑的几处 (两个缺省的行号、aether 无法区分「分支不存在」与「无 run」、对 #137 (a) 腿的订正、D2 的 symbolic-ref 前提) 我逐条实测**全部成立** —— 这在 post_spec 里不常见, 应予确认。

但按现文原样实施会踩到本项目实证过的三类高发形状, 其中三条到 Critical:

1. 它引入的 `verdict=error` 是**第四个枚举值**, 而三个下游消费者都是三态封闭集且对未知值无定义分支 —— gate 层做到了 fail-CLOSED, fail-OPEN 从消费侧的枚举遗漏处重新长出来;
2. 它唯一的 SKILL.md 改动**落在 (a) 腿的契约句上** (它自己判定不在范围的那条腿), 而 (b) 腿在 SKILL.md 里那两处写死 `--branch main` 的运行时指令一个字没动 —— Spec §Why 自己点名的「复制粘贴的命令」这条传播路径原封不动;
3. 「既有用例逐字不改」被现有测试直接证伪, 且 Spec 没有给新解析/核验留可打桩的接缝, 会让单测真发 SSH 网络请求。

⇒ **FAIL**。三条 Critical 都是**Spec 文本层面可修**的 (钉枚举 / 补落点 / 撤回一句自陈 + 指定接缝), 不需要推翻设计。D1-D7 的决策方向我全部支持。

---

## Phase 1 — 规范自洽性 (Spec 对现有代码的每句陈述 / 自我声称 / 枚举完整性)

### 1.1 逐句核验属实的部分 (Strengths)

| Spec 陈述 | 我的核验方式 | 结论 |
|---|---|---|
| `pre_merge_gate.py:300` `main_branch: str = "main"` | 实读该行 | 属实 |
| `pre_merge_gate.py:427` `default="main"` | 实读该行 | 属实 |
| `ci_backends/aether.py:117-135` 只在 aether 自身失败时抛, `runs=[]` 合流 | 实读 `:121-135` | 属实 |
| 「后端结构上无法区分『分支不存在』与『分支无 in-flight run』」 | **独立实跑**: `aether ci status --branch zzz-definitely-no-such-branch --in-flight --json` → `{"status":"ok","data":{...,"runs":[]}}` RC=0 | 属实 (我用的是一个绝无可能存在的分支名, 比 Spec 用 `main` 的证据更强) |
| `path_coverage.py:24` 规则 1 = `git diff 失败 → unknown, reason=git-diff-failed` | 实读 `:24` + `:13-14`「unknown 与 covered 在 gate 层行为一致」 | 属实; **对 #137 (a) 腿的订正成立** |
| 「(a) 观测到的 not_applicable 与分支名无关」 | 佐证: `git rev-parse --verify main` → `fatal: Needed a single revision`, `git branch -a --list "*main*"` 空 ⇒ 本仓无任何 `main` ref ⇒ 若分支名参与, 结果只能是 unknown 而非 not_applicable | 属实 |
| D2 承重前提 (symbolic-ref 取得出真值) | 实跑: 主仓 `git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master` RC=0; **aria 子模块同样 RC=0** → `refs/remotes/origin/master` | 属实 (子模块那侧我额外查了, Spec 没提但那是 (b) 腿真正的高频调用场景) |
| 「测试基线 111」 | `grep -c 'def test_'`: test_ci_backends 25 + test_path_coverage 40 + test_pre_merge_gate 46 = **111** | 属实 |
| ship target v1.65.6 PATCH | `aria/.claude-plugin/plugin.json:4` = `"1.65.5"` | 衔接正确 |
| D1「两处必须同批改」 | 类级 sweep (下 §1.2) | **枚举完整** |

### 1.2 「修实例不修类」专项 sweep (镜头 2 的正面结论)

命令:

```
grep -rn -E "= *\"(origin|main|master)\"" aria/skills/*/scripts/ | grep -v tests
grep -rn "add_argument" aria/skills/*/scripts/*.py aria/skills/*/scripts/**/*.py | grep -iE "branch|remote|main|base"
```

结果: `"main"` 这个字面缺省在整个 `aria/skills/` 里**只有 `pre_merge_gate.py:300` 与 `:427` 两处** —— D1 的枚举是完整的, 这条我明确背书。

sweep 顺带产出两条别处的事实 (下文 M1/M2 用得上, 本身不是对本 Spec 的指控):

- `state-scanner/scripts/phase1_gate.py:1207` 与 `release_gate.py:233` 均为 `--remote default="origin"` —— 本项目对 `<remote>` 参数**已有成文惯例**;
- `git-remote-helper/scripts/push_all_remotes.sh:19` / `check_parity.sh:16` 为 `BRANCH="master"` 硬编码 (方向恰好正确, 非 fail-OPEN, 记录备查)。

### 1.3 自我声称核验 (镜头 3)

- 「#137 正文已同批评论订正」—— **成立**。实跑 `forgejo GET /repos/10CG/aria-plugin/issues/137/comments` 得 1 条评论, `created_at=2026-08-08T16:37:00Z`, 标题逐字为「⚠️ 订正正文一处: 「两条腿都失败为绿」不成立 —— 只有 (b) 那条」。(见 m2: 正文 TL;DR 本身仍未改, 但那不违背这句自陈的字面。)
- 「既有用例逐字不改」—— **不成立**, 见 C3。
- 「零运行时指令流程新增 / 指令面是减少一条人工义务」(rule6_note) —— **不成立**, 见 C2: SKILL.md 步骤 3 是运行时指令且必须改。

**Phase 1 判定: FAIL** (C2 = 承重落点定位错 + §Impact 漏项; C3 = 自陈证伪)。以下 Phase 2 照常给出, 因为问题全部集中在**文本可修**层面, 阻断在 R2 修订即可解除。

---

## Phase 2 — 若按现文原样实施的质量与正确性风险

### Critical

#### C1 — `verdict="error"` 是第四个枚举值, 三个下游消费者都只认三态, §Impact 零枚举 ⇒ fail-OPEN 从消费侧遗漏处复发

**Spec 侧锚点**: §What Changes 2 (`abort, verdict=error`) / §What Changes 3 (两处 `verdict=error`) / D2 / D4 / SC-4 / SC-5 / SC-6 —— 全 Spec 至少 7 处以 `error` 为承重期望值。

**代码/文档侧实读锚点**:

| 位置 | 逐字内容 | 含义 |
|---|---|---|
| `pre_merge_gate.py:47-49` | `VERDICT_GREEN = "green"` / `VERDICT_WAIT = "wait"` / `VERDICT_FAIL = "fail"` | 三常量, 无第四个 |
| `pre_merge_gate.py:177` | docstring「Compute three-state verdict」 | 三态是成文契约 |
| `SKILL.md:267` | `"verdict": "green" \| "wait" \| "fail",` | Output schema 封闭集 |
| `SKILL.md:253-255` | 路由决策只有 green / wait / fail 三支 | 无 catch-all |
| `workflow-runner/scripts/gate_state_helper.py:32-34` | `GATE_STATUS_WAITING = "waiting"` / `_GREEN = "green"` / `_FAIL = "fail"` | 又一个三态封闭集 |
| `gate_state_helper.py:147` | `"status": verdict,` | **verdict 原样写入 gate_state, 零校验** |
| `gate_state_helper.py:165` | `"""True iff gate_state.status == waiting"""` | 未知值 → 不 waiting → 轮询退出 |
| `workflow-runner/SKILL.md:335-336` | `3. verdict=fail → 转为 stop (fatal)` / `4. verdict=green → 继续 merge (正常路径) [最低]` | exit conditions 正向枚举 |
| `workflow-runner/SKILL.md:388-390` | `green` → 跳过 C.2 直接 merge; `fail` → 转 stop | 无 else 分支 |

**为什么这是 Critical 而不是 Major**: Spec 在 gate 层把方向选对了 (abort 而非放行), 但它新引入的值在**所有**消费侧都落进「未建模」区。本项目成文判据 memory `feedback_invariant_needs_failclosed_default` 逐字说的就是这个:「正向枚举对新值/catch-all 天然 fail-OPEN」。具体后果: 一个不在封闭集里的字符串被 `gate_state_helper.py:147` 写进 workflow-state 的 `gate_state.status`; `is_waiting()` 返回 False 使轮询退出; 而 workflow-runner 的 exit conditions 里 green (继续 merge) 是**最低优先级的兜底语义**, 未匹配项由 AI 临场解释。**这正是 Spec 自己要治的病在它自己新写的失败分支上复发** (memory `fix-recurs-in-fallback`: 「修复类 change 最易在自己新写的 except/兜底路径重犯要治的病」)。

**修法 (Spec 须二选一并钉死)**:

- **(i) 推荐**: 不新增 verdict 值。用 `verdict=fail` + 新增诊断字段 (如 `error_kind: "main-branch-unresolved" | "main-branch-not-found" | "ls-remote-failed"`) + `raw_message` 点名。对上表 9 个锚点**全部后向兼容**, 且 `fail → BLOCK/stop` 本身就是 fail-CLOSED 的正确方向。
- **(ii)** 坚持第四值, 则**同批**改: `SKILL.md:267` schema + `SKILL.md:253-255` 路由 + `workflow-runner/SKILL.md:335-336` + `:388-390` + `gate_state_helper.py:32-34` 封闭集与写入校验, 并把这 3 个文件写进 §Impact (当前一个都没有)。

⚠️ 附带: `error` 这个字面在本模块**已被占用为另一维度的值** —— `pre_merge_gate.py:193` `if pr_ci_status in ("failing", "error")`。同名不同维会让排查者与后续 Spec 混淆。

#### C2 — §Impact 唯一的 SKILL.md 落点是 (a) 腿的契约句; (b) 腿那两处写死的 `--branch main` 未被枚举

**Spec 侧锚点**: §Why 第 48 行「`SKILL.md:242` 写着『main_branch 显式传真值 (本项目 master), 不依赖 CLI default』…唯一现有约束是一句散文」+ §What Changes 5 + §Impact 表第 3 行 `SKILL.md:242 散文勘正`。

**我实读 SKILL.md 的结果**:

- `SKILL.md:242` 逐字开头是「**2.5. Path coverage 评估** (v1.65.0+, aria-plugin #122; `path_coverage_enabled=true` 默认): `evaluate_path_coverage(main_branch, pr_branch)` …**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根); `main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」。
  ⇒ 引文本身逐字准确, 但它是 **`evaluate_path_coverage` 的执行上下文契约**, 即 Spec 在 D6 / §非目标 里明确判定**不在范围**的 (a) 腿。
- `SKILL.md:243` (紧邻下一行, (b) 腿本体) 逐字是「3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` → parse `data.runs[]`…」。
- `SKILL.md:167` 同一字面再出现一次: 「- aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)」。
- `grep -n -- "main.branch\|main_branch" SKILL.md` 全文只命中 242 一行 ⇒ **(b) 腿在文档里根本没有那句散文约束, 它有的是一条写死 `main` 的命令**。

**后果三条**:

1. 「唯一现有约束是一句散文」这个诊断把 (a) 腿的契约句当成了 (b) 腿的护栏 —— 该句被 §What Changes 5 改写成「不传会自动解析, 解析不出会 abort」后, 反而会让 `evaluate_path_coverage` 的调用契约描述与 `path_coverage.py:19` 的模块 docstring (逐字仍是「main_branch 由调用方显式传真值 (不依赖 "main" 默认)」) 产生新的不一致 —— 而 §非目标 第 1 条写着「不改 path_coverage.py」。
2. 实施完成后, AI 按 `SKILL.md:243` 步骤 3 执行, 命令仍是 `--branch main`。Spec §Why 第 50 行自己点名的三条传播路径之一「复制粘贴的命令」**一字未动**。这是「有记录 ≠ 有路由」的同族 (memory `fix-recurs-in-fallback` 后半)。
3. rule6_note 的「零运行时指令流程新增/变更」因此不成立: `SKILL.md:243` 的步骤 3 就是运行时指令面。Rule #6 处置表需重判 (至少该 hunk 不能归到「描述性」那一行)。

**修法**: §Impact 的 SKILL.md 行改为枚举 `:167` / `:242` / `:243` 三处并各写明改什么; `path_coverage.py:19` 的 docstring 同步问题要么纳入范围要么在 §非目标 显式声明「有意保留人工义务措辞」。

#### C3 — 「既有用例逐字不改」被现有测试证伪; 且没有可打桩接缝, 单测将真发 SSH 网络请求

**Spec 侧锚点**: §Impact 表第 2 行「`tests/test_pre_merge_gate.py` | 扩展 — SC-1..SC-7 (既有用例逐字不改)」。

**实读证据**:

- `tests/test_pre_merge_gate.py:663-670`:

  ```
  def test_sc12_default_true_lock(self) -> None:
      # 默认值锁定 (unset → 评估执行): config 不含 path_coverage_enabled。
      b = self._backend()
      with mock.patch.object(gate, "resolve_ci_backend", return_value=b):
          gate.gate_check(pr_branch="feat/x", config={})
      self.pc_eval.assert_called_once_with(
          main_branch="main", pr_branch="feat/x"
      )
  ```

  这条测试**把 `main_branch="main"` 锁成了契约**。改动后同一调用解析出的是 `master` (我已实测 symbolic-ref 返回 `origin/master`) ⇒ 该断言按定义必红。「逐字不改」在这一条上直接不成立。

- 另有约 20 处 `gate.gate_check(pr_branch="feat/x")` **不传 main_branch** (`:192 :210 :226 :234 :247 :267 :282 :628 :638 :667 :688 :695 :708 :723` 等)。这些用例只 `mock.patch.object(gate, "resolve_ci_backend", ...)` 与 `evaluate_path_coverage` 打桩 (见 `:191` 等)。Spec 新增的 `git symbolic-ref` 与 `git ls-remote <remote> <branch>` **没有任何打桩点**, 会真跑 subprocess —— `git remote -v` 显示 origin = `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` ⇒ 每条用例一次 SSH 往返, 叠加 Spec 自己要求的重试, 单测变成联网/慢/环境依赖, 且离线环境全红。
- 这与 `run_all_tests.sh` 头部注释里写死的原则冲突: 「一个默认红的检查等于没有检查, 会立刻被学会忽略。这正是本 spec 全程在打的假绿/恒红对偶」。

**修法**:

1. §Impact 撤回「逐字不改」, 改为明列必改用例 (至少 `test_sc12_default_true_lock`);
2. Spec 必须**指定模块级接缝**: 把解析与存在性核验做成 `pre_merge_gate` 的模块级符号 (如 `resolve_main_branch` / `verify_branch_exists`), 口径照抄本文件已有先例 —— `pre_merge_gate.py:42-44` 逐字写着「path coverage 评估器。模块级符号, 测试经 `mock.patch.object(gate, "evaluate_path_coverage")` 打桩 (镜像 resolve_ci_backend 先例)」。不指定, 两个实施者会给出不同的可测性设计。

### Major

#### M1 — `<remote>` 全 Spec 未定义, 而 §3 是自称的「承重条款」

- Spec 侧: §What Changes 2 (`refs/remotes/<remote>/HEAD`) / §3 (`git ls-remote --exit-code --heads <remote> <main_branch>`) / SC-4 (message 含 remote 名) / SC-6。
- 代码侧: `pre_merge_gate.py:298-302` `gate_check(pr_branch, main_branch, config)` 无 remote 参数; `:424-433` CLI 只有 `--pr-branch` / `--main-branch` / `--config-file`; `DEFAULT_CONFIG` (`:53-65`) 无 remote 键。
- 本仓是双 remote: `origin` = Forgejo, `github` = GitHub (`git remote -v` 实跑)。选哪个改变答案。
- 我实测了 aether 的 repo 归属推导: 在 `/home/dev/Aria` 跑得 `"repo":"10CG/Aria"`, 在 `/home/dev/Aria/aria` 跑得 `"repo":"10CG/aria-plugin"` ⇒ aether 按 cwd 的 (Forgejo) remote 定位。若存在性核验打到 `github` 而 in-flight 查询走 Forgejo, **核验的不是被查的那个对象**, 恒绿以另一种形式保留。
- 修法: 显式定名参数 + 缺省, 直接沿用本项目惯例 `--remote default="origin"` (`state-scanner/scripts/phase1_gate.py:1207`, `release_gate.py:233`), 并在 Spec 写明「必须与 aether 定位 repo 用的同一个 remote」。

#### M2 — 已有同功能解析器, 其兜底恰是 D2 明令禁止的字面回落 ⇒ 实施者照抄即复发

- 实读 `aria/skills/phase-d-closer/scripts/fetch_gate.py:108-128`:

  ```
  def _resolve_default_branch(run, cwd: Path) -> Optional[str]:
      """Resolve the default branch (symbolic-ref → ref probe → name probe → None)."""
      rc, out, _ = run(["symbolic-ref", "refs/remotes/origin/HEAD"], cwd, _GIT_QUICK_TIMEOUT)
      ...
      for name in _DEFAULT_BRANCH_FALLBACKS:      # :124
  ```

  且 `:55` 逐字 `_DEFAULT_BRANCH_FALLBACKS = ("master", "main")`。
- 另有 `aria/skills/audit-engine/SKILL.md:389`: `base = .aria/config 配置的 base OR git symbolic-ref refs/remotes/origin/HEAD`。
- Spec 一处都没提。D2 的策略 (解析失败 ⇒ abort, ⛔ 不回落字面缺省) 与既有实现**方向相反**。不写明「有意分叉 + 为什么闸门语义不同」, Phase B 最自然的动作就是复用/照抄现成的 `_resolve_default_branch` —— 它的第三级兜底会命中 `"main"`, **精确复活本 Spec 要治的恒绿**。这是 memory `fix-recurs-in-fallback` + `fix-the-class` 的合流点。
- 修法: D2 增补一段「与 `fetch_gate.py:108-128` 的关系」: 明确 gate 语义禁止 name probe 兜底, 并说明是否要把该差异回写成一条共享约定 (否则同一 plugin 内两套「默认分支解析」长期分叉)。

#### M3 — 同文件第二个 `main_branch` 消费者未被覆盖, 解析时序未钉

- 实读 `pre_merge_gate.py:356-360`:

  ```
  pc: dict[str, Any] | None = None
  if cfg.get("path_coverage_enabled", True):
      pc = evaluate_path_coverage(
          main_branch=main_branch, pr_branch=pr_branch
      )
  ```

  这在 `:366` 的 `backend.query_branch_in_flight(main_branch)` **之前**。
- Spec §What Changes 3 只说「查 in-flight **之前**核验」, §Impact 只写「两处缺省 + 解析 + 存在性核验 + 回显」—— 从未提到 `main_branch` 在同一函数里还有第二个消费者。
- 若实施者把解析放在紧贴 `:365` 处, `None` 会流进 `:359` → `path_coverage.py:442` 组出 `"None...feat/x"` → git diff 失败 → decision=`unknown`, reason=`git-diff-failed`。方向安全 (fail-toward-covered), 但 (a) 腿被静默降级, 且 reason 把排查者引向 git 与 main ref —— `path_coverage.py:33-36` 逐字为了 #126 明文禁止的 reason 冒用形状。
- 修法: Spec 钉死「解析完成于 `:356` 之前, 两个消费者共用同一已解析值」, 并在 §Impact 点名该调用点。

#### M4 — `ls-remote` 的重试次数/超时/退避未定, 与既有 subprocess 规范不衔接

- Spec 侧: §3 第三条「`ls-remote` 自身失败 → 重试后仍失败则 verdict=error」+ SC-6 —— 「重试」几次、多久、退避多少全未写。
- 既有规范逐字存在且具体: `SKILL.md:257-259`「`subprocess.run(..., timeout=primitive_call_timeout_seconds)` 强制 (默认 30s); timeout 触发 → max 3 attempts retry (backoff 5s/15s/45s)」; 实现侧 `ci_backends/aether.py:38-39` `RETRY_BACKOFF = (5, 15, 45)`; `path_coverage.py:59` 另有独立的 `_GIT_TIMEOUT = 15`。
- 三套口径已并存, Spec 不指定第四处该随哪一套 ⇒ 两个实施者必然给出不同结果 (memory `spec-underdetermination`)。最坏情形下每次 gate 多付 65s 退避而 `wait_check_intervals` 时序未做对应说明。

#### M5 — `main_branch_resolved` 出现在哪些输出分支未定, 与 #122 已成文的「早退分支键集不变」契约冲突

- Spec 侧: §What Changes 4 + D5「`gate_result` 输出中回显 `main_branch_resolved` + 其来源」。
- 契约侧实读: `pre_merge_gate.py:232-263` `_build_output` 固定六键 + 可选 `path_coverage`; `:243-247` docstring 逐字「各早退分支 (enabled:false / no-backend / precheck 失败 / backend query 失败) 保持既有六键不变」; `SKILL.md:279` 同样逐字重申一遍; 且 `tests/test_pre_merge_gate.py:683-697` `test_sc15_schema_additive_and_early_exit_six_keys` 正在**机械锁**这条契约 (`self.assertNotIn("path_coverage", fail_out)`)。
- Spec 未表态 `main_branch_resolved` 是 additive 可选键还是全分支必在:
  - 若全分支必在 → 上述测试红 (C3「逐字不改」的第二处证伪);
  - 若仅最终路径在 → `enabled:false` / no-backend / precheck 失败三条早退里「到底查了哪个分支」仍不可见, D5 的可观测性目的对这些分支落空。
- 修法: 在 §What Changes 4 明写键的在场规则, 并与 SC-1/SC-2 的断言点对齐。

### Minor

#### m1 — SC-2 点名的 `run_gate(...)` 在本 skill 不存在, 且该名在本仓另有其人

- Spec SC-2 逐字:「直接调 `run_gate(...)` **不传** `main_branch` (走函数签名那条路径)」并自称「本条是唯一覆盖内部调用路径的用例」。
- 实读 `pre_merge_gate.py:298` 函数名是 `gate_check`。全仓 `grep -rn "run_gate"` 的命中全部属于 **state-scanner 的 phase1_gate** (如 `aria-plugin-benchmarks/interactive-session-dedup/RULE6_SUBSTITUTE.md:27` 「first-ever direct run_gate test」) 与 benchmark harness。
- 即名字不只是笔误, 它在本仓指向另一个 skill 的真实函数, 会把实施者引偏。改为 `gate_check(...)`。

#### m2 — #137 正文 TL;DR 仍逐字保留被推翻的那句

- 自陈「#137 正文已同批评论订正」按字面**成立** (订正评论确实存在, 2026-08-08T16:37:00Z)。
- 但实跑 `forgejo GET /repos/10CG/aria-plugin/issues/137` 取回的 body 首段仍逐字是:「Rule #8 pre-merge gate 的两条腿在本项目上**都不触发, 且都失败为绿**」。只读正文的人或做 triage 的 AI 拿到的仍是被推翻的前提。
- 建议正文那句加删除线 + 指向订正评论的指针 (成本极低, 消除一个长期误导源)。

#### m3 — (a)/(b) 两腿对「分支不存在」的处置不对称, D3 未与既有 `not_found` 槽位对话

- 实读 `ci_backends/base.py:29`: `state: Literal["passing", "failing", "pending", "not_found"]`; `SKILL.md:279` 逐字「backend `CIStatus.state` Literal 另含 `not_found` (backend 层值, gate 输出目前不产生, 列此消除文档与 `ci_backends/base.py:29` 的历史漂移)」。
- D3 论证「存在性核验是策略, 放 gate 层」时没提这个**已经存在的 backend 层槽位**。补一句关系说明即可, 否则 `not_found` 继续是「设计了但永不产生」的死枚举。
- 另: PR 分支不存在时 `aether.py:224` `if not runs: return "pending"` → verdict=wait, 方向安全但会永久 wait —— 不属本 Spec 范围, 记录备查。

### Risk (非 issue, 但建议 Spec 表态)

**R1 — symbolic-ref 读的是本地缓存, 不是「获取」到的真值 ⇒ D2 在健康常态下可能恒红**

`refs/remotes/origin/HEAD` 只在 `git clone` 或显式 `git remote set-head` 时写入, **`git fetch` 不更新它**。我实测本工作树两仓都有 (RC=0), 但 aria-runner Layer 2 容器里脚本化/浅 checkout 的仓可能根本没有这个 ref ⇒ D2 会在一切正常的环境里 abort。这正是 memory `feedback_false_green_dual_is_permanent_red` 的对偶面 (恒红同样零信息), 也是 `feedback_freshness_must_be_fetched_not_measured` 说的「测量本地缓存 ≠ 获取真值」。

既然 §3 已经要打一次网络 (`ls-remote`), 建议 D2 改用 `git ls-remote --symref <remote> HEAD` 取**权威**默认分支, 本地 symbolic-ref 只作无网快路径。这既不违反「⛔ 不回落字面缺省」(它取的是真值不是字面量), 又把两次网络合成一次, 顺带解决 M4 的一半。SC-5 的场景描述也应随之从「ref 缺失」扩写为「本地 ref 缺失 **且** 远端 symref 取不到」。

---

## Verdict

**FAIL** (3 Critical + 5 Major + 3 Minor + 1 Risk)

判据: verdict 规则「≥1 Critical = FAIL」。

需要强调的是**失败点的性质**: 三条 Critical 全部是 Spec **文本层可修**的 —— 钉死 verdict 枚举策略 (C1)、补全 SKILL.md 的三个落点并重判 rule6_note (C2)、撤回一句自陈并指定打桩接缝 (C3)。缺陷诊断本体、D1-D7 的决策方向、SC 表的可证伪性设计我全部背书, 不建议推翻重做。R2 修订后应可迅速收敛。

**是否可以继续?** 需要修复 —— 建议在 R2 修订 Spec 后再进 Phase B, 不要带着 C1/C2/C3 开工: 这三条一旦进代码, 修的成本会从「改几行 Spec」变成「改三个 skill 的枚举契约 + 回改 20 条测试」。

---

## 轮次记录

### Round 1 (code-reviewer 席位)

**镜头**: 修复类 change 的自反性 (fail-OPEN 在新写分支复发 / 修实例不修类 / 假自陈 / 枚举不完整 / 恒红恒绿对偶)。

**实读文件** (全部为只读操作, 未修改任何被审文件):

- `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (全文 179 行)
- `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` (全文 445 行)
- `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` (全文 271 行)
- `aria/skills/phase-c-integrator/scripts/ci_backends/base.py` (:1-70)
- `aria/skills/phase-c-integrator/scripts/path_coverage.py` (:1-120)
- `aria/skills/phase-c-integrator/SKILL.md` (:230-260 + 全文 grep: `--branch main` / `main_branch` / `verdict`)
- `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` (:180-249, :655-699 + 全文 grep 调用点)
- `aria/skills/workflow-runner/scripts/gate_state_helper.py` (verdict/status grep)
- `aria/skills/workflow-runner/SKILL.md` (verdict grep)
- `aria/skills/phase-d-closer/scripts/fetch_gate.py` (:49-55, :100-160)
- `aria/skills/run_all_tests.sh` (:1-60)

**实跑命令 (只读)**:

- `git symbolic-ref refs/remotes/origin/HEAD` (主仓 + aria 子模块) → 均 `refs/remotes/origin/master`, RC=0
- `git remote -v` (主仓 + aria) → 双 remote 确认
- `git rev-parse --verify main` → fatal (本仓无 main ref)
- `aether ci status --branch zzz-definitely-no-such-branch --in-flight --json` → `{"status":"ok",...,"runs":[]}` RC=0 (独立复现核心前提)
- `aether ci status --branch master --in-flight --json` (在 `aria/` 内) → `"repo":"10CG/aria-plugin"` (证 repo 随 cwd)
- `aether ci status --help` → flag 面确认无 `--repo`
- `forgejo GET /repos/10CG/aria-plugin/issues/137` + `/comments` → 正文未改 + 订正评论存在
- 类级 grep sweep (字面缺省 / add_argument / symbolic-ref / run_gate / pre_merge_gate 调用方)
- `grep -c 'def test_'` × 3 → 111

**产出**: 3 Critical / 5 Major / 3 Minor / 1 Risk; 另确认 8 项 Spec 陈述属实 (含 D1 枚举完整性由类级 sweep 背书)。

**未收敛项**: 无 (R1 单轮, 无对手席位交叉)。建议 R2 复核 C1 的修法选型 (i vs ii) 与 M2 的分叉声明是否落到文本。
