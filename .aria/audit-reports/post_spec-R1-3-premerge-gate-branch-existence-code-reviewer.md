---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T14:25:40.679Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — code-reviewer (席位角度: 逐字核对 / 溯源表回源 / SC 号段 / file:line 属实 / 条款间自相矛盾)

被审对象: `/home/dev/Aria/openspec/changes/premerge-gate-branch-existence/proposal.md` (Spec A, Level 2)
基线: `aria` 子模块 detached at `af87cae` (clean, 与 Spec 声明的基线一致)

**判定: PASS_WITH_WARNINGS** (0 Critical / 6 Major / 3 minor)

---

## 0. 先说结论: 溯源表 12 行**全部回源为真**, 划界站得住

我把末尾溯源表 12 行**逐行实跑/实读**核了一遍, **12/12 属实**, 无一条需要下调。
连三条最难核的 (`ls-remote` 零命中 rc=0 / `--exit-code` 返 rc=2 / 锚定 pattern 仍命中)
我都在**自建受控裸仓**上独立复现成功。这在 R1 是罕见的。

因此本报告的 6 条 Major **不是**「这些事实错了」, 而是**拆分后组合出的新缺口** ——
正是本轮被要求审的那件事。

### 溯源表逐行回源 (命令原文附)

```bash
grep -n 'if not cfg\["enabled"\]\|if backend is None\|ok, precheck_err = backend.precheck()\|if not ok:\|pc: dict\[str, Any\] | None = None\|path_coverage_enabled\|pc = evaluate_path_coverage\|in_flight = backend.query_branch_in_flight' \
  aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
# → 328 / 338 / 344 / 345 / 356 / 357 / 358 / 366   全部逐字命中 ✅

grep -n 'fail` → BLOCK\|Subprocess 调用规范\|max 3 attempts retry\|exit-code 映射\|"raw_message"\|枚举归层注记' \
  aria/skills/phase-c-integrator/SKILL.md
# → 255 / 257 / 259 / 260 / 274 / 279  全部逐字命中 ✅  (:260 确含 `127` = binary not found → no_ci_fallback)

grep -rn 'gate_error' /home/dev/Aria/aria/ | wc -l          # → 0   ✅ 零消费者
awk 'NR>=332 && NR<=336' aria/skills/workflow-runner/SKILL.md # → 四条 Exit conditions, 无异常臂 ✅
grep -n 'def write_gate_state' -A8 aria/skills/workflow-runner/scripts/gate_state_helper.py
# → :115, 形参 state/name/verdict/in_flight_runs/primitive_used/raw_message/intervals — 确无 gate_error ✅

grep -n 'except (subprocess.TimeoutExpired, FileNotFoundError, OSError)' aria/skills/phase-c-integrator/scripts/path_coverage.py  # → 93 ✅
grep -n 'RETRY_BACKOFF\|def _run_with_retry\|self.binary\|text=True\|bubble up' aria/skills/phase-c-integrator/scripts/ci_backends/aether.py
# → :38 RETRY_BACKOFF=(5,15,45) ✅ / :164-187 _run_with_retry, :168 "other exceptions bubble up" ✅
#   :174 [self.binary]+args ✅ / :176 text=True ✅ / 无 cwd 形参 ✅
grep -c '_run_with_retry' aria/skills/phase-c-integrator/tests/test_ci_backends.py   # → 0 ✅ (「25 tests 全绿」判据恒绿, 属实)

grep -n 'def test_sc22_no_real_git_subprocess_in_suite\|mock.patch.object(pc_module.subprocess' tests/test_pre_merge_gate.py
# → :710 / :718 ✅;  :723 = `out = gate.gate_check(pr_branch="feat/x")` 确未传 main_branch ✅

cd aria/skills/phase-c-integrator && python3 -m pytest tests/ -q   # → 111 passed ✅
#   分文件: test_pre_merge_gate.py 46 / test_ci_backends.py 25 / test_path_coverage.py 40 = 111 ✅
```

### 三条 `ls-remote` 实验 — 我在独立受控裸仓上复跑, 全部复现

```bash
# 裸仓 A 只含 refs/heads/wip/master; 裸仓 B 只含 refs/heads/master
git ls-remote --heads A.git master                 # → 命中 refs/heads/wip/master, RC=0   (尾段 glob, fail-OPEN 属实)
git ls-remote --heads A.git "refs/heads/master"    # → 零行, RC=0
git ls-remote --heads B.git "refs/heads/mast*"     # → 命中 refs/heads/master, RC=0
git ls-remote --heads B.git "refs/heads/m[a]ster"  # → 命中, RC=0
git ls-remote --heads B.git "refs/heads/maste?"    # → 命中, RC=0        ⇒ 「锚定也关不掉 glob」属实
git ls-remote --heads B.git develop                # → 零行, RC=0        ⇒ 「零命中亦返 rc=0」属实
git ls-remote --exit-code --heads B.git wibble     # → RC=2              ⇒ 「--exit-code 返 2」属实
git -C /home/dev/Aria ls-remote --heads no-such-remote-xyz master  # → RC=128  ⇒ 「错 remote 走 128」属实
```

⚠️ 一处口径需明确 (不构成 finding, 但值得写进 Spec): §2 表格第 2 行「锚定也关不掉 glob」
在**两个不同场景**上的结论并不相同 —— 对 `wip/master` 场景, 锚定**确实**关掉了假命中 (零行);
关不掉的是「**main_branch 自身含通配符**」这一支。Spec 现文把两者并列在同一行, 读者易误读为
「锚定对 wip/master 也无效」。SC-A13 的定义是对的, 是散文的表述略糊。

### SC-A* 号段冲突 — 实跑核, 无冲突

```bash
grep -rho 'SC-[A-Za-z0-9]*' aria/skills/phase-c-integrator/ | sort -u
# → SC-1 SC-11 SC-14 SC-18 SC-19 SC-2 SC-21 SC-22 SC-23 SC-27 SC-4 SC-9   (纯数字段, 无字母前缀)
grep -rn 'SC-A' /home/dev/Aria/aria/ | wc -l        # → 0
grep -rn 'SC-A[0-9-]' /home/dev/Aria/openspec/ | grep -v premerge-gate-branch-existence   # → 空
grep -o 'SC-M[0-9]*' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md | sort -u
# → SC-M1..SC-M18   与 SC-A* 不相交
```
⇒ **前缀声称成立**。但见 Major-5: A **自己的正文** `:78` 却引用了 `SC-M6`, 自破该声称。

---

## 1. 划界对不对 —— 「存在性核验单独就关掉恒绿腿」成立吗

**成立, 但成立范围比 Spec 写的窄一档。**

回源验证 (`aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:117-135` 实读):
`query_branch_in_flight()` (`:117`) 只有两个 raise 点 (`:123` 查询失败 / `:126` runs 非 list),
**都是 aether 自身失败**; 分支不存在时 aether 返 `status:ok` + `runs:[]` ⇒ `InFlightStatus(runs=[])`
⇒ `compute_verdict` 判 green。B 侧 §症状的逐字表述属实。
存在性核验插在 `:345` 之后 `:356` 之前, 对同一输入 (`main_branch="main"`, 远端只有 `master`)
产出 `verdict=fail` ⇒ **确实直接消除了那个不可区分性**。这一步不需要「参数必填」参与。
⇒ **A 自足, 划界正确**; 把 D5/破坏面/弃用面/发版面留 B 的理由 (MAJOR 传染) 也经得起核。

**A 少带了什么? 我逐条比对 B 侧现文, 只发现两处该带未带 (Major-1 / Major-4), 一处正确未带**:
- ✅ 正确未带: B 的 `SC-M10 变体 (b)`「含 legacy key 的 config」—— 它守的是 `TASK-020`
  (v2.0 弃用删除面) 这个 **B 侧独有**的交叉输入, A 无 TASK-020 ⇒ 不带是对的。这一刀切得干净。
- ❌ 该带未带: `SC-M14` 的**断言**(见 Major-1) 与 `aether.py` 入 scope 后的**行为等价判据**(见 Major-4)。

**A 多带了什么?** 没有。`aether.py` 是「条件性」入 scope, 但那是 A 自己的重试轴必需, 不算 scope creep。

---

## 2. 「纯 additive ⇒ MINOR」逐条复核

| A 的实证 | 我的复核 | 结论 |
|---|---|---|
| `gate_check(..., remote: str = "origin")` 带默认值 ⇒ **既有 24 处调用零改动** | `grep -o 'gate\.gate_check(' tests/test_pre_merge_gate.py \| wc -l` = **24** ✅; 但**可执行调用点共 25 个** —— 第 25 个是 `pre_merge_gate.py:435` 的 `output = gate_check(...)`, 且它**必须改** (§1 要求 CLI 新增 `--remote`, main() 得把它传下去) | 数对得上「测试内调用」这个总体, 但**措辞与 §1 自相矛盾** → Major-3 |
| 核验步插在既有早退之后 ⇒ 既有分支语义零改动 | `:328/:338/:345` 三条早退在插入点之前, 实读确认; SC-A10/10b/10c 各带 `assert ls-remote 未被调用` 因果断言 | ✅ 成立 |
| `gate_error` 是 additive 可选键 ⇒ 六键 schema 零改动 | `_build_output` (`:230-261`) 已有 `path_coverage` 同款 additive 先例 (`:258-259` 条件加键); `SKILL.md:279` 逐字「各早退分支…保持六键不变」 | ✅ 成立 |
| 外部消费者 | `grep -rn 'gate_check\|pre_merge_gate'` 排除 `aria/` 后, 仅 `aria-plugin-benchmarks/*/README.md` 的历史归档文本, **无生产消费者**; `aria-orchestrator/` 零命中 | ✅ 无破坏面 |
| 不触发 `:68/:116` 弃用到期 | `:68` = 「Old keys still readable until v2.0」/ `:116` = 「will be removed in v2.0」实读命中; MINOR ⇒ v1.65.5→v1.66.0, 不到 2.0 | ✅ 成立 |

⇒ **MINOR 定档正确**。唯一瑕疵是「24 处零改动」的措辞 (Major-3)。
另: 头部「无跨仓同步面」与 §Impact「发版同步面 走常规发版流程」不一致 (minor-2)。

---

## 3. SC 集合自足吗 —— 恒红 / 恒绿 / 空真扫描

12 条 SC 逐条问「它在什么实现下会红」:

| SC | 会红吗 | 核 |
|---|---|---|
| SC-A6 | ✅ 今日必红 (今日无核验 ⇒ green ≠ fail); 健康实现绿 | 承重腿成立 |
| SC-A13 | ✅ 「锚定」实现红 (实测三 pattern 全 RC=0 命中), 「精确比对」实现绿 | 成立 |
| SC-A-zero | ✅ **双向**: 读 rc 的实现把 rc=0 当成功 → 红; 用 `--exit-code` 的实现得 rc=2 → verify-failed ≠ not-found → 红 | 本条是 `--exit-code` 禁令的**唯一**机械锚 |
| SC-A7 / A8 | ✅ 128 不重试 / timeout 重试 3 次, 两向可证伪 | 成立 |
| SC-A10/10b/10c | ✅ 后半条因果断言 (`assert ls-remote 未被调用`) 使「插错位置」的实现红 | 成立, 且比 B 侧把 `:338/:345` 挂在 task 上更强 |
| SC-A11 | ✅ 恒判 not-found 的实现红 (正向路径守卫) | 成立 |
| SC-A14 | ⚠️ **它自己是正向枚举** —— 只喂三个已枚举输入, 却宣称「正向枚举的实现…会漏」 | **近空真** → Major-1 |
| SC-A-sc22 | ✅ 要求对抗桩, 可证伪 | 成立 |
| SC-A-baseline | ✅ 111 实跑确认 | 成立 |

**无恒红、无恒绿。空真一条 (SC-A14)。**
**覆盖缺口三处**: CLI `--remote` 面 (Major-3) / 查询作用域 (Major-2) / `aether.py` 条件 scope (Major-4)。

---

## Major (6)

### Major-1 · `SC-A14` 是正向枚举, §2 的 catch-all「任何未枚举情形」实为零机械断言; A 自己点名的 `UnicodeDecodeError` 会裸穿 gate

**locator**: `proposal.md:88` (§2 catch-all 行) · `proposal.md:182` (SC-A14) · `proposal.md:148-149` (§5 两轴)

**证据 (实跑)**:
```python
issubclass(UnicodeDecodeError, OSError)   # → False
UnicodeDecodeError.__mro__ → UnicodeError → ValueError → Exception    # 不在 (TimeoutExpired, FileNotFoundError, OSError) 内
```
- §2 catch-all 行逐字承诺: 「其余一切 … **任何未枚举情形** ⇒ `fail` + `kind="main-branch-verify-failed"`」;
- §5 逐字指定异常轴先例 = `path_coverage.py:93` 的 `(TimeoutExpired, FileNotFoundError, OSError)` **三合一元组**;
- §5 同时逐字指定重试轴先例 = `aether.py:38`, 并自陈 `aether.py:176` 是 `text=True` 严格解码,
  「对 git 输出会抛 `UnicodeDecodeError`, 见 `path_coverage.py:81-84` 的 #124 教训」;
- 而 **SC-A14 只喂三个输入**: `FileNotFoundError` / `OSError` / 输出不可解析。`UnicodeDecodeError` 不在其中。
- B 侧为这一支**专门开过编号** (`premerge-gate-mainbranch-failclosed/proposal.md:352` = `SC-M14`,
  post_planning R2 加的, 理由逐字「本条是给 §5 catch-all 里唯一无编号的那一支补编号 ——
  无编号的行为要求不会被任何机械勾稽点找到」)。**A 把 `SC-M14` 这个号复用给了另一条断言**, 原断言**未随行**。

**它在什么实现下会红 (falsifier)**: 实现者**完全照 §5 两轴照做** ——
`except (TimeoutExpired, FileNotFoundError, OSError)` + `subprocess.run(..., text=True)`。
git 返回含非法 UTF-8 的 ref 名时 `UnicodeDecodeError` 既不是 `TimeoutExpired` 也不是 `OSError`
⇒ **裸抛穿过 `gate_check()`**; 而 A `:138` 自己实读确认 workflow-runner 的 verdict 路由
(`workflow-runner/SKILL.md:333-336`) **只有四条臂、无异常臂** ⇒ 路由未定义。
此时**全部 12 条 SC 仍绿** (SC-A14 喂的三个输入都被那个元组接住了)。
⇒ 这正是 memory `fix-recurs-in-fallback`:「修复类 change 最易在自己新写的兜底路径重犯要治的病」。

**处方**: 要么把 SC-A14 的输入改成**不可枚举的探针** (至少补 `UnicodeDecodeError` 一支 + 一条
「任取一个不在实现 except 元组里的异常类」的参数化), 要么承接 B 的 SC-M14 断言另开一条 `SC-A15`。
⚠️ 别只加一个 `UnicodeDecodeError` 用例就算完 —— 那又是「修实例不修类」(memory `fix-the-class`)。

**blocks_phase_b: true** —— 不补, Phase B 的 TDD 写出来的就是那个会裸抛的实现。

---

### Major-2 · 存在性查询**在哪个仓执行**未规定, 且零 SC 覆盖; 方向是 fail-OPEN

**locator**: `proposal.md:51` (§1 `--remote` 定义) · `proposal.md:115` (§3 的 ⛔) · SC 表整体

**证据 (实跑, 无网络)**:
```bash
git -C /home/dev/Aria/aria remote -v   # origin → ssh://forgejo…/10CG/aria-plugin.git
git -C /home/dev/Aria      remote -v   # origin → ssh://forgejo…/10CG/Aria.git
git -C /home/dev/Aria/aria for-each-ref 'refs/remotes/*/master'  # → refs/remotes/origin/master 存在
git -C /home/dev/Aria      for-each-ref 'refs/remotes/*/master'  # → refs/remotes/origin/master 存在
```
`origin` 这个**名字**在主仓与 `aria` 子模块解析到**两个不同的 repo**, 而两边都有 `master`。
§3 `:115` 逐字只给了**否定式**「⛔ 不得为解析路径而 `cd` —— 那会使 `ls-remote` 查错仓
(主仓与 `aria` 子模块都有 `master`, 会 RC=0 假通过)」—— **它准确识别了危害, 却没给正面规定**:
新增的 git 子进程用哪个 `cwd`? A 全文未答。对照 `path_coverage.py` 是有答案的
(`_repo_root()` = `git rev-parse --show-toplevel`, 再把 `cwd` 显式传给 `_run_git`, 见 `:76/:88/:101`),
A 的 §5「按轴分派两个既有先例」**只分派了异常轴与重试轴, 漏了 cwd 轴** —— 而 `_run_with_retry`
恰恰**无 `cwd` 形参** (A `:149` 自己写了这一条, 却没把它转成一条要求)。

**它在什么实现下会红 (falsifier)**: 实现用环境 cwd (最省事写法)。
SC-A6/A13/A-zero 把**受控裸仓的路径**当 `remote` 传 (这是它们唯一可行的构造方式 ——
`git ls-remote <绝对路径>` 绕过 repo config, 我上面的实验就是这么跑的) ⇒ **cwd 对这三条完全无影响**;
SC-A7 用「不存在的 remote 名」得 128, 同样不区分仓; SC-A10* 断言的是「未被调用」。
⇒ **12 条 SC 全绿, 而生产上查的可能是另一个仓的 `origin`**。
危害面窄于我最初的估计 (`main` 在两仓都不存在, 故 #137 原始场景仍会正确判 fail),
但对「默认分支是 `main` 的仓在 cwd 落到默认分支是 `main` 的另一个仓时」是**实打实的 fail-OPEN**,
而这正是本 Spec 唯一要关的那条腿。

**处方**: §1 或 §3 补一条正面规定 (至少: 「git 子进程的 `cwd` 必须显式传入, 取值 = 被合并仓的仓根,
求法沿用 `path_coverage.py:_repo_root()`」), 并补一条 SC: 「在仓 X 内、`remote='origin'`、
仓 X 的 origin 无 `<b>` 而 cwd 所在仓 Y 的 origin 有 `<b>` ⇒ 须 `fail`」。

**blocks_phase_b: true**

---

### Major-3 · CLI `--remote` 面零 SC 覆盖; 且「既有 24 处调用零改动」与 §1 自相矛盾

**locator**: `proposal.md:51` · `proposal.md:234` (§版本) · `pre_merge_gate.py:428-437` (实读)

**证据 (实跑)**:
```bash
grep -o 'gate\.gate_check(' aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py | wc -l   # → 24
grep -rn 'gate_check(' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py                   # → :298 (def) + :435 (call)
```
可执行调用点是 **25** 个 = 测试 24 + `pre_merge_gate.py:435` 的 `output = gate_check(pr_branch=..., main_branch=..., config=...)`。
而 §1 要求「CLI `--remote`」⇒ `main()` 必须 `parser.add_argument("--remote", default="origin")`
并把它传进 `gate_check` ⇒ **第 25 个调用点必改**。§版本 `:234` 逐字「**既有 24 处 `gate_check(` 调用零改动**」
在「测试内调用」这个总体上数字是对的 (我复跑确认 24), 但措辞省略了口径, 与 §1 直接冲突。
(按 memory `critique-repeats-error`: 总体 = 「`aria/` 内可执行 `gate_check(` 调用点」, 范围 = `af87cae`,
计数法 = `grep -o` 出现次数; 三项写明后是 25, 与「测试内 24」**不是**同一个量, 二者都对。)

**它在什么实现下会红**: 实现者只加 `gate_check(remote=...)` 形参与核验逻辑, **忘了 argparse 的 `--remote`**。
12 条 SC 全部作用在 `gate_check()` 层 (SC-A6 写「传 `--main-branch master`」是 flag 记法, 但既有 46 条
测试无一走 `main()`; 实读 `test_pre_merge_gate.py` 24 处全是 `gate.gate_check(...)`) ⇒ **全绿, 而 §1 承诺的 CLI 面缺席**。

**处方**: (a) `:234` 改成带口径的表述 (「既有 24 处**测试内**调用零改动; `main()` 一处随 CLI 新增而改」);
(b) 补一条 SC 走 `main(argv=[...])` 真实 CLI 路径断言 `--remote` 生效 (B 侧 `:358` 提过「CLI 真实路径用例」, A 没接)。

**blocks_phase_b: false** (评审可见, 但缺 SC 就没有红窗)

---

### Major-4 · `aether.py` 条件入 scope, 却**只否定了一个判据、没给任何可用判据**; 该文件的回归零覆盖

**locator**: `proposal.md:151-153` (§5 末段) · `proposal.md:227` (§Impact 条件性行)

**证据 (实跑)**:
```bash
grep -c '_run_with_retry' aria/skills/phase-c-integrator/tests/test_ci_backends.py   # → 0
python3 -m pytest tests/test_ci_backends.py -q                                       # → 25 passed
```
A `:152-153` 逐字: 「**行为等价的判据不得用「`test_ci_backends.py` 25 tests 全绿」** —— 实测 …= **0**,
那 25 条**系统性绕过它** ⇒ 该判据恒绿」。**这个否定是对的, 我复跑确认。**
但 A **到此为止** —— 没有给出替代判据, 也没有任何 SC 覆盖 `aether.py`。
`SC-A8` 测的是**新核验步**的重试 (3 attempts + mock `time.sleep`), 不是 `AetherBackend._query` 那条路径。

**它在什么实现下会红**: spike 判定「抽取共享重试 helper」, 改写 `aether.py:164-187`,
过程中把 `RETRY_BACKOFF` 语义弄坏 (例: 只重试 1 次 / 吞掉 `last_exc`)。
- `test_ci_backends.py` 25 条: 绿 (它们从不触碰 `_run_with_retry`, grep=0 已证);
- SC-A8: 绿 (它断言的是 gate 层核验的重试);
- SC-A-baseline: 绿 (111 全过)。
⇒ **aether 的重试真回归了, 12 条 SC 一条都不红**。这与 memory `redfix-change-quantity` 同形:
指出了旧量恒绿, 却没换上新量。

**处方**: 要么把 `aether.py` 从条件 scope 里**拿掉** (spike 若判定需要共享 helper, 则整体退回 B 侧或另开 change),
要么补一条 SC 钉住等价 (例: 「新增针对 `_run_with_retry` 的直测 ≥N 条, 覆盖 3 attempts + backoff 序列 +
`last_exc` 透出; 把改动回退该组必红」)。

**blocks_phase_b: false**

---

### Major-5 · `:78` 引用 `SC-M6` —— 既是悬空引用 (A 的号段是 `SC-A*`), 又与 B 侧 `:199` 的逐字结论相反

**locator**: `proposal.md:78` vs `proposal.md:168-169` (号段声明) vs `premerge-gate-mainbranch-failclosed/proposal.md:199`

**证据 (逐字)**:
- A `:168-169` 逐字: 「SC 编号用 **`SC-A*`** 前缀 —— 与 B 侧的 `SC-M*` … **全部不冲突**
  (B 侧曾因编号冲突被 post_planning 判 Critical, **此处预防**)」;
- 而 A `:78` 逐字: 「一个合法缺失的分支会被误分类成「查询失败」而非「分支不存在」
  (**SC-M6 会抓到它**, 但应在 Spec 层直接排除)」—— A 内部**没有 SC-M6**;
- B 侧 `:199` 逐字则说反话: 「该禁令由 TASK-003 / TASK-008 的零命中用例钉住 …
  **现有 SC-M6 / SC-M13 两个场景都有命中, 结构上碰不到这条分支, 故不能靠它们代管**」。

**它在什么实现下会红 (falsifier, 我构造并逐步核过)**: 实现 = 精确字符串比对 (合规),
但取列表用 `git ls-remote --exit-code --heads <r> <b>`, 非零 rc 一律 → `verify-failed`:
- SC-A6 (远端只有 `wip/master`, 查 `master`): 实测 rc=0 + 一行输出 → 精确比对不等 → `not-found` ⇒ **绿**;
- SC-A13 (`mast*`): 实测 rc=0 + 命中 → 精确比对不等 → `not-found` ⇒ **绿**;
- SC-A-zero (`develop`): 实测 **rc=2** → catch-all → `verify-failed` ≠ `not-found` ⇒ **红**。
⇒ 抓住它的是 **SC-A-zero**, `SC-A6` 结构上碰不到 (它的 ref 列表非空)。A `:78` 的归因**实质错误**。
后果: Phase B 若据 `:78` 认为 `SC-A6` 已代管, 可能删掉 SC-A-zero —— 那才是 `--exit-code` 禁令的唯一机械锚。

**处方**: `:78` 改为「(**SC-A-zero** 会抓到它, 但应在 Spec 层直接排除)」。

**blocks_phase_b: false**

---

### Major-6 · Rule #6 定档落「第一行」缺 SOT `:33` 的必要条件; 且与同段「本 Spec 不申请任何豁免」自相矛盾

**locator**: `proposal.md:193-201` (§Rule #6) vs `standards/conventions/skill-benchmark-exemption.md:33` (逐字实读)

**证据 (逐字)**: SOT `:33` 原文 ——
> 「**SKILL.md 有变动时的附加约束** (承前): **仅当**变动是**事实性同步** (溯源注释 / 行号勘正 / 术语修正)
> 且 frontmatter `description` 零变动, **才可能**落进第一行; 须在 spec 里**逐行点名**该变动并声明非指令语义变更。
> `description` 或指令流程变动 ⇒ 一律第二行。」

这是一条**「仅当…才可能」的必要条件**, 且其括号枚举 = {溯源注释, 行号勘正, 术语修正} **三项**。
A 的 SKILL.md 变动是「`:267` schema **增** `gate_error`」—— 我实读 `SKILL.md:264-277` 确认那是
Output schema 的 json 块 (`:267` 是 `"verdict"` 行, `gate_error` 实际会落在 `:275/:276` 附近, 行号本身也偏);
**给 schema 新增一个本 change 才产生的键, 不是上述三项中的任何一项** —— 它不是把陈旧文档同步到既有事实,
而是**为新行为写新文档**。A 的 `:195-196` 只援引了**判据表第一行**的标签「(描述性 / schema / 字段)」,
**跳过了 `:33` 这条专门管辖 SKILL.md 的收窄条款**, 而 A 自己在 `:199` 又把 `:33` 列为「附加约束」——
即它**知道 `:33` 在场, 却没对其必要条件作答**。这正是 memory `exact-exception-condition`
「援引成文豁免前逐字核对**确切触发条件**字段级匹配 (非精神/类推)」。

**自相矛盾**: 同段 `:201` 逐字「**拿不准照跑** —— 本 Spec **不申请任何豁免**」,
而 `:196` 正在申请 —— 落「第一行 ⇒ substitute」就是**免跑 AB**, SOT 文件名逐字即
`skill-benchmark-exemption.md`, CLAUDE.md Rule #6 亦把该表称为「豁免判据」。两句不能同时为真。

**它在什么实现下会红**: 若 A.2 按 `:199` 逐行点名时诚实作答 `:33` 的必要条件, 结论只能是
「不属三项 ⇒ 拿不准 ⇒ 照跑 (宁跑勿豁, 表第四行)」—— 即**当前 `rule6_note` 的结论会被自己的复核推翻**。
反之若不复核, 就是 Rule #10 禁止的「AI 自行豁免已启用闸门」。

**处方**: 二选一并写死 —— (a) 直接定第二行照跑 AB (A 是 MINOR, AB 成本可控);
(b) 保留第一行, 但在本文件里就**补上 `:33` 的三项匹配论证**, 并把 `:201` 的「不申请任何豁免」改成
「申请第一行 substitute, 依据如下」。**Rule #10 要求这个判断写进 handoff 请复议。**

**blocks_phase_b: false** (但**必须**在 A.2 前落定, 否则 Phase C 发版会撞 Rule #6 闸门)

---

## minor (3)

1. **`:98` / `:249` 「五个行锚」但列了 8 个行号** —— `:328`/`:338`/`:344`/`:345`/`:356`/`:357`/`:358`/`:366` = 8 个。
   按逻辑锚位分组 (enabled / no-backend / precheck / path-coverage / in-flight) 确是 5 组, 但**计数法未写明**,
   而这恰是 B 侧四轮反复被抓的形状 (B `:37` 逐字「与本 Spec 内任何可数集合都对不上」)。
   改法: 写成「**5 个逻辑锚位 / 8 个行号**」。DEC `:90` 同样表述, 一并更正。
2. **头部 `:6` 「无跨仓同步面」与 §Impact `:229` 「发版同步面: MINOR, 走常规发版流程」不一致** ——
   CLAUDE.md 版本管理段逐字把发版同步面定义为「aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION +
   root README badge + i18n README」, 那**就是**跨仓面。A 想说的应是「无**弃用删除**那种跨仓内容面」。
   建议改为「无跨仓**内容**同步面 (发版例行 gitlink/badge 由既有机械 check 兜底)」。
3. **`:186-187` 「打桩边界 (钉死)」只覆盖 5/12 条 SC** —— SC-A14 的 `FileNotFoundError`
   (git 二进制缺失) 结构上**只能** mock, 却未列; SC-A10/10b/10c 的「assert ls-remote 未被调用」
   需要打桩接缝, 亦未列; SC-A11「分支存在」需真实 fixture 或 mock, 未列。
   B 侧 `:358-361` 正是在这一段栽过两次自相矛盾 (自称唯一权威入口却漏了 SC-M14)。
   A 没有自称「唯一入口」故未构成矛盾, 但「钉死」二字与覆盖率不符。

---

## 优点 (具体点名)

1. **溯源表 12/12 回源为真** —— 我逐条实跑/实读, 无一条需要下调。三条 `ls-remote` 实验我在独立
   受控裸仓上复现成功 (rc=0 零命中 / `--exit-code` rc=2 / 锚定 pattern 仍命中), 这三条是本 Spec 承重判据的地基。
2. **`SC-A-zero` 是本轮最有价值的新增** —— 它双向可证伪 (读 rc 的实现红 / 用 `--exit-code` 的实现也红),
   且是 `⛔ 不得使用 --exit-code` 这条禁令的**唯一**机械锚。B 侧 `:199` 只把它挂在 TASK 上, A 提升为 SC 是升级。
3. **`SC-A10b` / `SC-A10c` 把 B 侧 `:400` 挂在 TASK-008 上的两条早退提升为独立 SC, 并各带因果断言** ——
   「六键不变」是**健康与不健康实现都成立**的弱断言, 加 `assert ls-remote 未被调用` 才把它变成真信号。
   这是 memory `false-green-dual-is-permanent-red` 的正确应用。
4. **正确识别并剔除 B 的 `SC-M10 变体 (b)`** —— 它守的是 TASK-020 (B 侧独有) 的交叉输入。
   A 不带它是**划界正确**, 不是遗漏。这一刀的干净程度是 A/B 拆分成立的最好证据。
5. **`:137-139` 主动声明 `gate_error` 全仓零消费者、workflow-runner 无异常臂, 并明说「本 Spec 不依赖它发红」** ——
   这是对 memory `feedback_completion_signals_vs_runtime_invocation` 的正面应用: 承认「有记录 ≠ 有路由」。
6. **`:136` 示例用占位符 `<MAIN_BRANCH>` 而非 `"main"`, 理由是「写 `"main"` 会与 B 侧的 SC 对撞」** ——
   拆分期的交叉污染意识, 很细。

---

## 评估

**是否可以继续?** 可以, 但 **Major-1 / Major-2 必须在 Phase B 之前补进 SC 表** (二者都是「全绿而缺陷在场」),
Major-6 必须在 A.2 前落定 Rule #6 档位并写进 handoff 请复议 (Rule #10)。

**理由**: A 的事实基座 (溯源表 12 行 + 三条 `ls-remote` 实验 + 111 baseline + 行锚) 我逐条复核**全部为真**,
划界判断「存在性核验单独就关掉恒绿腿」经 `aether.py:117-135` 实读**成立**, MINOR 定档经 25 个调用点
与外部消费者扫描**成立**。6 条 Major **无一是继承自 B 的旧账**, 全部是**拆分后组合出的新缺口** ——
其中 3 条 (Major-1/2/4) 是同一个形状: **A 把「否定」写得很准 (⛔ 不得 cd / 不得用 25 tests 全绿 / 不得正向枚举),
却没把对应的「肯定」落成 SC**。这是 A 的系统性缺口, 建议一次性按类修, 别逐条补 (memory `fix-the-class`)。
