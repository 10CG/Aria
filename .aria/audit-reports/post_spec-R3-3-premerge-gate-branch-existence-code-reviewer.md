---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T17:55:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — code-reviewer — Spec A `premerge-gate-branch-existence`

**VOTE**: REVISE · **VERDICT**: PASS_WITH_WARNINGS (0C + 5M + 6m) · 阻塞 B: 3 条 · 本轮 R2-fix 引入 **9/11 = 82%**

审视角度 (本席): 逐字核对 — 末尾溯源表回源抽查 / `SC-A*` 号段冲突 / 全部 file:line 属实 / 条款间自相矛盾。

---

## 0. 先说结论

- **R2 的 13M 有 12 条真闭合、1 条闭成了一个新的错数** (见 F-1)。没有 paper-fix: 每条闭合都带上了可复跑的机械判据, 我逐条复跑, 除 F-1 外全部命中。
- **R2-fix 新写的内容质量明显高于前几轮**: SC-A-doc 的两条解析规则、SC-A-step 的对抗性验证、§5 出口净化的三段实测, 我**逐条独立复跑全部复现**(命令与输出见 §2)。
- **但引入率没降**: 我的 11 条里 9 条落在 R2-fix 新写的文字上。形状**变了** —— 不再是「承重结论错」, 而是「新写的**精确化**声称本身不够精确」(把「至少 4 处」写成「恰是 4 处」· 把「全部兄弟位置」写成只清点 SC 表 · 新 SC 的红窗在真实 harness 下不红)。

---

## 1. R2 的 13M 逐条回源 — 区分「写下来」与「闭合」

| # | R2 finding (席位) | 处置落点 | 我的判定 |
|---|---|---|---|
| BA-1 | `main()` 出口 `UnicodeEncodeError` 新口 | §5 「R2 追加的第三件: 出口净化」+ `SC-A14` 腿 2 | **真闭合** — 三条实测我全部复跑复现 (见 §2.4)。⚠️ 但腿 2 的红窗在指定 harness 下不成立 → **F-2** |
| BA-2 | `SC-A-doc`「实际解析」欠定 | SC 表下方两条解析规则 (`:456-468`) | **真闭合** — `json.loads` 报错串逐字命中、朴素正则 16 键、锚定正则恰 7 键且键名逐字一致 (§2.3) |
| TL-1 | hunk ① 零机械锚 (Rule #6 定档唯一承重依据) | 新增 `SC-A-step` | **真闭合** — 今日区块编号序列实跑 = `1. 2. 2.5. 3. 4. 5. 6.`,区间 (2, 2.5) 内零编号 ⇒ 今日必红成立。⚠️ 起点锚非唯一 → **F-6** |
| TL-2 | 撞 B 侧 `SC-M3a` | §残余暴露 🔴 框 + 兄弟位置表 + `SC-A-step` (c) | **真闭合** — B `:345` 逐字期望 2、今日 0 复跑一致; `grep -n -- '--main-branch' SKILL.md` 零行复跑一致。取 (i) 拒绝 (ii) 的论证成立 (见 §3) |
| TL-3 / CR-4 | backend ambient ⇒ 两条 SC 恒红 | 「可达前提」块 (适用集 10 / 例外 3 / 不适用 3 / 元断言 2 = 18) | **闭合 5/6** — 分区与 SC 表 18 行一一对上; 但**例外集把 `SC-A10c` 放错边** → **F-3** |
| TL-4 | `SC-A-doc` 代码侧操作数未定义 | §4 R2 钉死「必须经 `_build_output()` 产出」 | **真闭合** — `_build_output` 实读 `:232-263`, `path_coverage` 就是该形状 |
| TL-5 | Level 2 三项义务零承载 | 文首 🚧 BLOCKER (O-1/O-2/O-3) | **闭合 (路由到 owner)** — O-1「`m6-version-badge-match` 对 gitlink 失明」实读 `.aria/state-checks.yaml:88-99` 属实; O-2「无闸门读 proposal 散文」实跑 `grep -niE 'rule.?6|benchmark|gitlink' .aria/state-checks.yaml` 零命中属实。⚠️ 但出路 (i) 给 O-1 的兜底是失效委派 → **F-4** |
| QA-1 | 无 SC 验核验独立于 `path_coverage_enabled` | `SC-A-order` 腿 2 | **真闭合** — `:357` 逐字 `if cfg.get("path_coverage_enabled", True):` 实读命中, 误植位置真实存在 |
| CR-1 | 「24 处全部触达」自相矛盾 | §6 R2 更正框「20/24」 | **闭成了新的错数** → **F-1** (实测 19/24; R2 原文写的是「**至少** 4 处」, R2-fix 把它精确成「恰是 4 处」) |
| CR-2 | §6 名单漏 `SC-A11` | 改为「名单唯一 SOT = 打桩边界表」 | **真闭合** — §6 已不复制名单, 打桩边界表含 `SC-A11` 且带反例注 |
| CR-3 | §4 委派 `SC-A-doc` 失效 | 改由 `SC-A-note` 钉 | **真闭合** — `SKILL.md` json 块 `:265-277` 与归纳句 `:279` 实读确认互不覆盖; `SC-A-doc` 已逐字声明「不管 `:279`」 |
| KM-1 | #137 禁令耐久性弱 | 上提 O-3 (owner 裁定) | **闭合 (如实路由)** — 判「缺陷成立但 A 内不可修」正确 (见 §3) |

10 条 minor: 8 条闭合 (含 `workflow-runner/SKILL.md:335` 行锚更正 — 我实读 `:335` = `3. **verdict=fail** → 转为 stop (fatal)`、`:337` 为空行, 更正正确); `docs/handoff/latest.md` 未反映拆分属仓内他处、不在本 Spec 交付面; follow-up 无 issue 号一条与 O-1/O-2/O-3 同一裁定覆盖。

---

## 2. 溯源表与 file:line 逐字回源 (全部实跑, 命令原文附)

### 2.1 末尾溯源表 21 行 — 全部回源, 21/21 命中

| 溯源行 | 我的复核命令 / 实读 | 结果 |
|---|---|---|
| 插入点 5 逻辑锚位 / 8 行号 | `sed -n '{328,338,339,344,345,356,357,358,366}p' pre_merge_gate.py` | **8/8 逐字命中** |
| `SKILL.md:255` = `fail` surface 通道 | 实读 | ✅ 逐字 |
| `SKILL.md:279` = 四类早退 | 实读 | ✅ 括号内恰 4 项 |
| `SKILL.md:259`/`:260` 重试 + 退出码映射 (含 `127 → no_ci_fallback`) | 实读 | ✅ 逐字 |
| 锚定 pattern 仍 fail-OPEN | 受控裸仓: `git ls-remote --heads origin 'refs/heads/mast*' / 'refs/heads/m[a]ster' / 'refs/heads/maste?'` | **三条全部命中 + rc=0** ✅ |
| `ls-remote` 零命中亦返 rc=0 | `git ls-remote --heads origin develop; echo rc=$?` | **零行 + rc=0** ✅ |
| `--exit-code` 无命中返 rc=2 | `git ls-remote --exit-code --heads origin develop` | **rc=2** ✅ |
| `test_sc22` patch 全局 + `:723` 未传 `main_branch` | 实读 `:710/:718/:723` | ✅ |
| `gate_error` 全仓零消费者 | `grep -rn 'gate_error' aria/ \| wc -l` | **0** ✅ |
| `_run_with_retry` 硬绑/只捕 `TimeoutExpired`/无 `cwd`/`text=True` | 实读 `aether.py:164-187` | ✅ 四条全对 |
| `test_ci_backends.py` 零命中 `_run_with_retry` | `grep -c '_run_with_retry' tests/*.py` | **0/0/0** ✅ |
| 测试基线 111 passed | `python3 -m pytest -q tests/` | **111 passed** ✅ |
| `SKILL.md:243` 硬编码且是编号步骤本体 | 实读 | ✅ 逐字 |
| 本仓 `ls-remote --heads origin main` | 实跑 | **零行 + rc=0** ✅ |
| `workflow-runner` 全文零命中 `pre_merge_gate.py` | `grep -rn 'pre_merge_gate\.py' aria/skills/workflow-runner/ \| wc -l` | **0** ✅; 不带后缀得 3 处 (`:342` `:373` `gate_state_helper.py:37`), 逐个实读**确为配置键读取, 非 helper 调用** ✅ |
| v1.65.0 同形先例 | `aria/CHANGELOG.md` 实读 | 「SKILL.md §C.2.4 八处同步 (新步骤 2.5 …)」+「Rule #6 照跑 AB (3 eval × with/old/without 三臂)」**逐字命中** ✅ |
| `issubclass(UnicodeDecodeError, OSError)` | 实跑 | **False** ✅ |
| `ls-remote` 指向不存在路径 ⇒ 确定性 128 | `git ls-remote --heads /tmp/does-not-exist-repo-xyz master` | **rc=128** ✅ |
| 24/24 既有调用不传 `main_branch` | `grep -c 'gate\.gate_check(' …` = 24 · `grep -c 'gate\.gate_check(.*main_branch' …` = 0 · 六处多行 (`:311/:321/:394/:524/:654/:675`) 逐个实读 | ✅ |
| `_ProbeCacheResetMixin:59-80` | 实读, docstring 逐字命中 | ✅ |
| 真实调用点 25 | `grep -rn 'gate_check(' aria/skills --include=*.py` | 25 成立 (⚠️ 该 grep 的原始输出另有 5 行文档串, 见 **F-11**) |

### 2.2 `SC-A*` 号段冲突 — 无冲突, 结论成立

```
grep -rhoE 'SC-[A-Za-z0-9]+' aria/skills/phase-c-integrator/tests/  → SC-1 SC-11 SC-14 SC-18 SC-19 SC-2 SC-22 SC-23 SC-27 SC-4 SC-9
grep -rn 'SC-A' aria/                                              → 零命中
grep -c '^| \*\*SC-A' proposal.md                                  → 18   (= 抬头「18 条」计数法自洽)
```
B 侧号段实测 `SC-M1 … SC-M18` (含 M3a/b/c), 与 `SC-A*` 无交集 ✅。SC 表 18 行与「可达前提」的 10+3+3+2 分区**恰好配平** ✅。

### 2.3 `SC-A-doc` 三条解析声称 — 逐条复跑, 全部逐字复现

```
json.loads(块)  → JSONDecodeError: Expecting ',' delimiter: line 2 column 22 (char 23)   [与 Spec 逐字一致]
朴素 "key": 正则 → 16 键
^  "([A-Za-z_]+)": (MULTILINE) → 7 键: verdict / pr_ci_status / in_flight_runs /
                                 primitive_used / primitive_version_sha / raw_message / path_coverage
```
与 `_build_output` 今日实产 7 键相等 ✅。**这是本轮质量最高的一处修复。**

### 2.4 §5 出口净化的三条实测 — 复跑复现

```python
s = b"fatal: bad \xff\xfe stuff".decode("utf-8","surrogateescape")   # 'fatal: bad \udcff\udcfe stuff'
json.dumps({"raw_message": s}, ensure_ascii=False)                    # 成功
sys.stdout.errors                                                     # 'strict'
TextIOWrapper(..., errors="strict").write(payload)                    # UnicodeEncodeError: surrogates not allowed
s.encode("utf-8","replace").decode("utf-8")                           # 'fatal: bad ?? stuff' → 写出成功
```
✅ 四条全部复现。**但见 F-2** —— 这套事实在**测试 harness 里**并不成立。

---

## 3. 四条「不同意」与两条 owner 裁量项 — 分类复核

| 项 | 执笔方处置 | 我的判定 |
|---|---|---|
| **SC-M3a 二选一** | 取 (i)「A 新步骤不得含 `--main-branch`」, 拒 (ii)「改 B 的期望值为 3」 | **正确, 且理由站得住**。(i) 本就是 aggregate 给的两条之一, 不是拒绝处方。援引的先例实读属实: `SKILL.md:242` 步骤 2.5 逐字 `evaluate_path_coverage(main_branch, pr_branch)` 是**函数调用形态非 CLI 示范**, `:241` 步骤 2 亦然 ⇒「A 写 CLI 示范 = 替 B 交付」成立。拒 (ii) 的理由 (期望值会变成随 ship 顺序漂移的量) 与 memory `feedback_freshness_must_be_fetched_not_measured` 同形, 成立 |
| **#137 耐久性** | 判「缺陷成立但 A 内不可修」⇒ 路由 O-3 | **分类正确**。A 是 Level 2 ⇒ 无 tasks.md 载体; 仓外写动作按 DEC §6 逐字「外向动作待授权」⇒ 只能上报。⚠️ 但同一文件对**另外三条仓外写动作**给了相反口径 → **F-10** |
| **版本 MINOR vs MAJOR** | 判 MINOR + 留痕请复议 | **正确** (规则 #10 留痕形态标准) |
| **Level 2 vs 3** | 两条出路交 owner | **正确**, 但出路 (i) 的 O-1 兜底是失效委派 → **F-4** |

---

## 4. Findings

### Major

**F-1 (M, 引入=是, 阻塞=否) —「触达新核验的 20/24」实测为 19/24, 漏的正是第三类早退**

- **位置**: `proposal.md:379-385` (§6 R2 更正框) · `:597` (§Impact 测试行) · `:660-661` (§行为兼容面) × `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:272-288`
- **逐字**: §6 「**结构上够不到核验的恰是 4 处** (我逐行实读复核): `:301` · `:311` · `:321` · `:524`」⇒「20 处触达 + 4 处不触达」。
- **实测** (机械, 非阅读): 用 `sys.settrace` 在整套 46 条测试上记录每次 `gate_check` 动态调用是否执行到插入点 (`pre_merge_gate.py:356`, 即 §3 钉的「三早退之后 / path coverage 之前」):
  ```
  tests run: 46 · dynamic gate_check calls: 24 · reached insertion point: 19
  NOT reached: [282, 301, 311, 321, 524]
  ```
  `:282` = `test_case_f_outdated_binary_fails_fast`, 其 `:276` 逐字 `mock_backend.precheck.return_value = (False, …)` ⇒ 在 `:345` 早退, **结构上够不到核验**。
- **三项并列** (memory `critique-repeats-error`): **总体** = `tests/test_pre_merge_gate.py` 内 `gate.gate_check(` 调用点 (与被审文件同为 24); **范围** = 基线 `af87cae`; **计数法** = 逐调用点判是否执行到 `:356` (Spec 自己的计数法是「逐行实读判是否早退」, 同一判据)。
- **它怎么会红**: Phase B 按「20 处触达」设计 mixin 覆盖面与红窗预期 ⇒ 实测 19; 更实在的是**分类矛盾** —— Spec 有**三条**负控 `SC-A10`/`A10b`/`A10c` 对应**三道**早退, 而「必须继续够不到」的名单只含 `enabled=false` 与 `backend is None` **两类**, 第三类 (precheck 失败) 在仓里现成有一个实例却未被点名。这正是 R2 该条 finding 自己批评的「同类只覆盖一个实例」。
- **注**: R2 code-reviewer 原文写的是「实测**至少** 4 处」; R2-fix 把它精确成「**恰是** 4 处」并加了「我逐行实读复核」的背书 —— 精确化的方向对, 但把一个正确的下界改成了错误的等式。

**F-2 (M, 引入=是, 阻塞=是) — `SC-A14` 腿 2 在它被指定的形态下, 对它声称要拒绝的实现恒绿**

- **位置**: `proposal.md:446` (SC-A14 腿 2) × `:489` (打桩边界表「必须 mock」档逐字「**腿 2** 走 `main(argv=…)`, 注入的是**同一批** mock, 只是断言点移到进程出口」) × `:349-359` (§5 出口净化)
- **逐字期望**: 腿 2 = 「**进程退出码 == 0** 且 stdout 是可 `json.loads` 的单行 JSON」; 逐字红窗 = 「`surrogateescape` 解码后不做出口净化就塞进 `raw_message` 的实现必红 —— `:438` 的 `sys.stdout.write` 抛 `UnicodeEncodeError`」。
- **实测**: 同一段写入代码在三种 harness 下的 `sys.stdout`:
  ```
  pytest 默认捕获 : stdout=EncodedFile   errors=replace → 写入成功, 无异常   ← 假绿
  pytest -s       : stdout=TextIOWrapper errors=strict  → UnicodeEncodeError
  python -m unittest: stdout=TextIOWrapper errors=strict → UnicodeEncodeError
  ```
  仓内**无 `pytest.ini` / `pyproject.toml` / `setup.cfg` / `tox.ini`** (逐个 `ls` 确认) ⇒ 默认捕获生效; 而本 Spec 的基线与 B 侧 TASK-021 都逐字用 `python3 -m pytest -q`。
- **它怎么会红 / 不会红**: 一个**跳过出口净化**的实现, 在 `python3 -m pytest -q` 下腿 2 全绿 (pytest 用 `errors="replace"` 替 stdout, `UnicodeEncodeError` 永不触发); 而「进程退出码」这个操作数在 in-process `main(argv=…)` 里根本不存在。⇒ R2-fix 新加的**唯一**出口净化机械锚, 在它自己指定的落地形态下零信息量 (memory `feedback_false_green_dual_is_permanent_red` 的另一面 + `test-claims-vs-verifies`)。
- **可行修法** (不属本席交付, 仅证明可修): 腿 2 改为**真子进程** (`subprocess.run([sys.executable, "pre_merge_gate.py", …])`, 断言真实 exit code) —— 但那与「注入同一批 mock」不兼容, 需改用 fixture 仓/环境变量注入; 或保留 in-process 但**强制** `redirect_stdout(TextIOWrapper(BytesIO(), encoding="utf-8", errors="strict"))` 并把断言从「退出码」改为「不抛异常」。Spec 必须钉死其一, 否则该腿欠定且默认恒绿。

**F-3 (M, 引入=是, 阻塞=是) —「可达前提」的例外集把 `SC-A10c` 放错边, 使该负控在干净 runner 上假绿**

- **位置**: `proposal.md:413-433` (可达前提块), 逐字「**例外 (3 条负控本就要打这两道早退)**: `SC-A10` (`enabled=false`) · `SC-A10b` (backend **必须**为 `None`) · `SC-A10c` (precheck **必须**返 `(False, …)`)」× SC 表 `:444` × `pre_merge_gate.py:337-345` × `ci_backends/aether.py:62-69`
- **矛盾**: 该块的规则是「凡断言核验确实发生的 SC 必须显式提供 mock backend, ⛔ 不得依赖 ambient 的 `aether`/`gh` binary」, 例外集 = 不适用该规则者。但 `SC-A10c` 的成立条件逐字是「precheck **必须**返 `(False, …)`」—— 这**只有 mock backend 能做到** (实读 `ci_backends/base.py:79-85`: 默认 `precheck()` 恒返 `(True, "")`; `AetherBackend.probe()` = `shutil.which("aether")`)。它被免除了它最需要的那条要求。
- **它怎么会红 (实为不会红)**: 在无 `aether`/`gh` 的干净 CI runner 上, 不打桩 backend 的 `SC-A10c` ⇒ `resolve_ci_backend` 返 `None` ⇒ 在 `:339` `_no_ci_output` 返 green ⇒「六键不变 + 无 `gate_error` + ls-remote 未被调用」**三条断言全部成立** ⇒ 绿, 但走的是 `SC-A10b` 的分支, precheck 早退**从未被执行** ⇒ 一个把核验错插在 `:345` **之前**的实现在此照样全绿。在本机 (实跑 `which aether` = `/usr/local/bin/aether`) 则相反: 真 shell out 到 binary, 判决随其版本漂移。
- **同形**: 这正是该块自己声明要根治的病 (「本条是『同一 ambient 只防了一个』的**类级修复**」), 类级修复漏掉了自己例外集里的成员 (memory `fix-the-class`)。

**F-4 (M, 引入=否, 阻塞=是) — BLOCKER 出路 (i) 给 O-1 的兜底是失效委派: C.2.5 与双推 `ls-remote` 核验都对「gitlink 未 bump」结构上失明**

- **位置**: `proposal.md:46` 逐字「O-1 由 phase-c-integrator §C.2.5 既有自动化 + 双推 `ls-remote` 核验兜 gitlink 那条腿」× `aria/skills/phase-c-integrator/SKILL.md:582-593` (C.2.5 执行流程) × `CLAUDE.md` 多远程硬约束 2
- **去 X 核它真做不做这件事** (memory `delegate-verify`): C.2.5 逐字流程 = ① `expected_sha = git rev-parse HEAD` (**本地 master HEAD 快照**) → ② 枚举子模块 → ③④ per-remote 推子模块+主仓 → ④d `verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])`。**全流程无一步比较「主仓 gitlink」与「子模块 post-merge master SHA」**; `expected_sha` 取的就是本地当前 HEAD ⇒ **gitlink 未 bump 时, C.2.5 把这个未 bump 的 commit 一致地推到所有 remote 并 verify parity 成功 ⇒ green**。双推 `ls-remote` 核验 (CLAUDE.md 约束 2) 比的同样是 remote SHA ↔ 本地 SHA, 同一盲区。
- **它怎么会红**: 不会。这与同一张表 O-1 行**自己**判定 `m6-version-badge-match`「对『主仓 gitlink 未 bump』这个方向结构上失明」是**同一个盲区**, 而出路 (i) 把它当成了兜底。⇒ owner 若据此选 (i), 会在「O-1 已被机械兜住」的错误前提下定档; 而 B 侧 R4 的 Critical `TASK-017` 漏 gitlink 正是这个形状的已实现版本 (A 自己引用了它)。
- **引入判定**: 该句实为 R1-fix 内容 (`git diff e165df4 017eb54` 显示它从 §Impact 脚注 `:422` **逐字上移**到 BLOCKER), R2-fix 只搬了位置 ⇒ `introduced_by_r2fix = false`。**但上移把它从脚注提升为呈交 owner 的两条出路之一, 危害被放大。**

**F-5 (M, 引入=是, 阻塞=否) —「这个形状的**全部**兄弟位置」只清点了 B 的 SC 表, 漏掉 B 的 `tasks.md` / `detailed-tasks.yaml` 里同类的预写量**

- **位置**: `proposal.md:141` (小节标题逐字「这个形状的**全部**兄弟位置」) 与 `:144` (总体逐字「B 侧全部断言到『A 会碰的文件』的 SC」) 之间的口径落差 × `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md:85,122` × `detailed-tasks.yaml:478,488`
- **实读漏掉的兄弟** (与被清点的 SC-M15 是**同一类**: 一侧 ship 使另一侧预写的量失真, 差别只是方向由「B ship 打爆 A」变成「A ship 打爆 B」):
  - `tasks.md:85` TASK-010 逐字「既有 **24 处** `gate_check(` 调用补 `main_branch="master"`」;
  - `detailed-tasks.yaml:488` 逐字「实测 24 处 `gate_check(` 调用点、**显式传 main_branch 的 0 处** — 补完后应为 24/24」;
  - `tasks.md:122` TASK-021 验收逐字「贴出 collected 数与变更前基线 **111** 的差值」。
- **它怎么会红**: A 的 `SC-A6/A7/A8/A10/A10b/A10c/A11/A13/A14/A-order/A-cli/A-cwd/A-zero` 各需 ≥1 条新用例, 且其中多条**必须显式传 `main_branch`** (SC-A6/A13/A-zero/A-cwd/A-cli 逐字如此)。A ship 当天:
  `grep -c 'gate\.gate_check(' tests/test_pre_merge_gate.py` **> 24** 且「显式传 `main_branch` 的 0 处」**为假** ⇒ B 的 TASK-010 验收对**任何**正确实现都不成立; `111` 亦不再是基线。
- **可接受的最小修法**: 把总体从「SC」扩到「B 侧任何以 A 会碰的文件为操作数的**预写量**」并补 3 行, 或在标题上把「全部兄弟位置」收窄为「全部**SC**兄弟位置」并显式声明 task 级量未清点。**两者都行, 但现状是声称强于实做。**

### Minor

**F-6 (m, 引入=是) — `SC-A-step` 的区块起点锚在 `SKILL.md` 有两处**
`proposal.md:451` 逐字「取 `SKILL.md` §C.2.4 `**执行流程**:` (`:238`) 与 `**Subprocess 调用规范**:` (`:257`) 之间的区块」。实跑: `**执行流程**:` 命中 **`[238, 582]`** (`:582` 属 `### C.2.5 Multi-Remote Push Enforcement`, 标题在 `:570`); 终点锚唯一。取**末次**匹配的实现得到起点 582 > 终点 257 ⇒ 空区块 ⇒ 三腿与被测实现无关地全红。与同批为 `SC-A-doc` 把解析规则钉到字符级的标准不一致 (memory `spec-underdetermination` 只修了一半)。修法一行: 「取**首个**匹配 / `:238` 那处」。

**F-7 (m, 引入=是) — `SC-A-note` 的「段」边界无机械定义**
`proposal.md:452` 逐字「取 §C.2.4『枚举归层注记』段 (含逐字 `各早退分支` 的那段, 今日 `:279`)」。`:279` 是**单行段落** (`:280` 空行)。若合规实现把第五类早退写成**紧邻的新段落** (完全满足 §4 的要求), 则按「含 `各早退分支` 的那段」取到的区块**不含**新文本 ⇒ (b)(c) 两腿对合规实现红。同一份文件在 `SC-A-doc` 上刚刚论证过「不写死解析规则,『实际解析』四个字就是欠定」。

**F-8 (m, 引入=是) — 抬头「实跑 `ls .aria/audit-reports/ | grep mainbranch-failclosed` 得 9 轮 × 5 席 = 45」: 该命令实际输出 55 行**
三项并列: **总体** = `.aria/audit-reports/` 内文件名含 `mainbranch-failclosed` 者; **范围** = 今日 `/home/dev/Aria`; **计数法** = 该行逐字给出的命令 + `wc -l` ⇒ **55** = 45 席报告 + 9 aggregate + 1 `…-audit-trail.md`。**45 这个数 (席报告数) 是对的**, 错的是「该命令得 45」这个可复跑性声称 —— 与 R2 抓的「Rule #6 (c) 的命令是 no-op」完全同形。危害低 (Spec 自陈该数只作修辞), 但它出现在一个专门用来**更正上一版数错**的括号里。

**F-9 (m, 引入=是) — 兄弟位置表把 `SC-M18` 的操作数缩写成「`SKILL.md` 的计数」, 实为四个文件**
`proposal.md:156` 逐字「`still (readable|works)|removed in v2\.0|仍读|v2\.0 移除` 在 `SKILL.md` 的计数」; 而 B `:364` 逐字跑在**四个文件**上: `.../scripts/pre_merge_gate.py` (今日 2) · `.../phase-c-integrator/SKILL.md` (4) · `.../tests/test_pre_merge_gate.py` (3) · `.aria/config.template.json` (0) —— **其中三个正是 A 要改的文件**。判定方向「不会打爆」我复核**仍成立** (A 不添此类措辞), 但该行给出的操作数比真实拒绝域窄, 后续读者据它判「只要不动 `SKILL.md` 就安全」会得到错误的安全感 (例如给 `--remote` 写一句带 `removed in v2.0` 形状的兼容注释)。

**F-10 (m, 引入=是) — 仓外写动作的授权口径自相矛盾**
`proposal.md:615` §Impact「外部」行逐字「**无外部动作** —— 不改 #137 body, 不发评论」+ O-3 把「在 #137 留一条评论」上提 owner 裁定; 而 `:572-583` Follow-up 归属表把 **F-1/F-2/F-3 三条开 issue** 逐字派给「**A 侧, A 的 D.2**」, 并写「**实际大概率由 A 开**; A 开出后把号写进 A 的 D.2 handoff」。开 3 个新 issue 与发 1 条评论同为同一 tracker 上的仓外写动作, 却一个自派、一个上呈; DEC-20260812-001 §6 逐字「本 session 记录的 5 个仓外缺陷仍未开 issue (**外向动作待授权**)」。**它怎么会红**: A 的 D.2 执行时, 同一份文件既写着「无外部动作」又要求 A 开三个 issue, 执行者必须临场裁量 —— 而临场裁量正是 O-3 被上提的理由。

**F-11 (m, 引入=否) — §版本 的 grep 溯源列举不全**
`proposal.md:637-638` 逐字「`grep -rn 'gate_check(' aria/ --include=*.py` **另得** `pre_merge_gate.py:298` (def, 非调用) 与 `:435`」。实跑该 grep 在测试文件之外另得 **7** 行: 除这两处外还有 `ci_backends/base.py:11`、`:106`、`ci_backends/github_actions.py:8`、`:40`、`:48` (均为 docstring/字符串, 非调用)。**结论「真实调用点 = 25」不受影响**、口径三项写得规范; 仅列举不全, 复跑者会多得 5 行。属 R1-fix 内容。

---

## 5. 优点 (须记录, 否则下一轮会把它们改掉)

1. **`SC-A-doc` 的两条解析规则**是本 session 迄今最扎实的一处机械化: 它同时钉住了「不能这样解析」(json.loads / 朴素正则) 与「必须这样解析」(`^  "([A-Za-z_]+)":`), 且两个反例都附了实测值 (JSONDecodeError 逐字串 / 16 键)。我独立复跑**三个数全部逐字复现**。
2. **`SC-A-step` 的对抗性验证** (1 好实现 + 5 个坏实现, 逐条命中预期腿) 是 memory `adversarial-fixture` 的正确执行形态 —— 它证明的是**拒绝能力**而非当前取值。今日基线 `1. 2. 2.5. 3. 4. 5. 6.` 我实跑复现。
3. **「可达前提」改为一次性全表分区**而不是逐条补注, 分区数 (10+3+3+2) 与 SC 表 18 行**恰好配平**, 这是把 `fix-the-class` 做成结构而非补丁的正确形态 (尽管 `SC-A10c` 放错了边)。
4. **`SC-A-order` 两腿合一条**而不是新开编号, 并写明理由「拆开等于把『同类只覆盖一个实例』复制进 SC 编号」—— 方法论自洽。
5. **拒绝 (ii) 而不是照做 aggregate 的字面**, 且给出了结构性理由 (期望值会成为随 ship 顺序漂移的量)。审计处方不该被当成必须照抄的指令, 这次拒绝是对的。

---

## 6. 判定

**VERDICT: PASS_WITH_WARNINGS** (0 Critical + 5 Major + 6 minor) · **VOTE: REVISE**

- Critical 连续第二轮归零, R1 的 2C 与 R2 的 13M **无一复发** (我逐条回源确认);
- 但 5 条 Major 中 **3 条 (F-2/F-3/F-6) 打在 R2-fix 新增的机械锚本身的可红性上** —— 新锚写下来了, 其中两条在指定的落地形态下不会红;
- **引入率 9/11 = 82%**, 高于本轮 <50% 的目标。诚实的读法: 形状变了 (不再是承重结论错, 而是新写的精确化声称本身不够精确), 但**「每轮 fix 引入约等量同形状缺陷」这个稳态本轮没有被打破** (memory `stop-adding-rounds` / `marginal-return-negative`)。
