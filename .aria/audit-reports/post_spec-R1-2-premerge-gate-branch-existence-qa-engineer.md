---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T14:18:48.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — qa-engineer 席位报告

**被审对象**: `openspec/changes/premerge-gate-branch-existence/proposal.md`(Spec A, Level 2)
**审视角度**: SC 可证伪性 —— 12 条的红窗是否真实存在 / 有无恒红恒绿空真 / 打桩边界自洽 / 三条负控早退是否真能拒绝坏实现
**投票**: REVISE · **verdict**: FAIL(2 Critical + 1 Major)

---

## 0. 先说结论

我独立跑了一遍受控裸仓实验、独立读了 `pre_merge_gate.py` 全文与 `SKILL.md:90-330`、独立 grep 了
`aria-orchestrator/` 与全仓 workflow 文件,**在看任何同轮报告之前**先形成了判断,随后才读到
`post_spec-R1-0`(tech-lead)与 `post_spec-R1-1`(backend-architect)——两份报告独立命中了同一个
结构性问题(生产执行路径不可达)。我在下面按自己的证据链复核了一遍,结论收敛一致,一并计入
本报告(标注为已交叉验证);此外我发现了一条二者都未提及、**属于我本席专职范围**的独立缺陷
(SC-A7 打桩边界自相矛盾)。

**判断本身**:

- **12 条 SC 各自的红窗均真实存在**(SC-A6/A13/A-zero 我用独立构造的裸仓复现,SC-A7/A8/A14 的
  mock 场景逻辑自洽,负控 SC-A10/A10b/A10c/A11 的因果断言设计正确、确能拒绝对应坏实现)——
  **但作为一个集合,它们测量的对象和 #137 症状真实发生的场所不同源**,这是结构性问题,不是
  某条 SC 写错了(C-1)。
- Rule #6 substitute(SC-A6/A13/A-zero)对它声称要替代的两处 `SKILL.md` hunk **恒绿**(C-2,
  与 tech-lead C-1(a) 收敛)。
- SC-A7 的打桩边界说明**自相矛盾**,且是对姊妹 Spec B 已经修复过的同型缺陷的**回归**(M-1,
  独立发现)。

---

## 1. 证据链(全部本轮实读/实跑)

```bash
# 基线
$ cd /home/dev/Aria/aria/skills/phase-c-integrator && python3 -m pytest tests/ -q
111 passed in 1.15s

# 五个插入点行锚(pre_merge_gate.py 全文 Read 逐行核对)
:328 if not cfg["enabled"]:            :338 if backend is None:
:344 ok, precheck_err = backend.precheck()   :345 if not ok:
:356 pc: dict[str, Any] | None = None  :357 if cfg.get("path_coverage_enabled", True):
:358 pc = evaluate_path_coverage(      :366 in_flight = backend.query_branch_in_flight(main_branch)
# 全部逐字命中,顺序正确

# 生产执行路径可达性(独立验证)
$ grep -n "" aria/skills/phase-c-integrator/SKILL.md | sed -n '166,168p;238,244p'
167: - aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)
243: 3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` → parse `data.runs[]` ...
$ grep -rn "pre_merge_gate\.py\|pre_merge_gate(" --include='*.md' --include='*.py' --include='*.sh' \
    --include='*.yaml' --include='*.yml' --include='*.json' . | grep -v '\.pytest_cache\|__pycache__\|/tests/'
# 全部命中落在: 测试文件 / aria-plugin-benchmarks 归档 / CHANGELOG / 审计报告 / 本文件自身的说明句
# 零命中: 任何"AI 执行指令"或"CI/hook 自动触发"路径
$ ls /home/dev/Aria/aria-orchestrator && grep -rln "pre_merge_gate" /home/dev/Aria/aria-orchestrator
# aria-orchestrator 存在,零命中
$ git ls-remote --heads origin main   # 本仓真实主分支是 master
# 零行输出,RC=0  ← §Why 症状的活体,今日仍在

# SC-A7 打桩边界(我独立搭建的裸仓实验)
$ git ls-remote --heads remote.git master              # rc=0,命中
$ git ls-remote --heads remote.git wibble               # rc=0,零行
$ git ls-remote --exit-code --heads remote.git wibble    # rc=2
$ git ls-remote --heads /tmp/does-not-exist-repo-xyz master
fatal: '/tmp/does-not-exist-repo-xyz' does not appear to be a git repository
rc=128
$ git ls-remote --heads remote.git 'mast*' / 'm[a]ster' / 'maste?'   # 三者全命中 refs/heads/master,rc=0
```

---

## 2. Findings

### C-1 [Critical] 12 条 SC 无一验证"AI 是否会走到这条新增校验"——测量对象与症状真实发生场所不同源

**locator**: `proposal.md:27-35`(§本 Spec 的范围判定)+ `:171-187`(SC 表全部 12 行)+ `:205-216`
(§非目标排除 D1)× `aria/skills/phase-c-integrator/SKILL.md:167`/`:243`

**evidence**:

1. Spec A `:29-30` 逐字断言的机制是「传 `--main-branch main` 而 `main` 在远端不存在时, 核验判
   `fail`」——这句话描述的是 `gate_check()` / CLI `main()` 内部行为。
2. `SKILL.md §C.2.4「执行流程」`(AI 实际被指令执行的规范面)`:167`/`:243` 逐字仍是裸命令
   `aether ci status --branch main --in-flight --json`,与 `pre_merge_gate.py` 无任何调用关系
   ——我独立 grep 全仓确认零处带参调用示范(见 §1 证据链)。
3. SC 表 12 条(SC-A6/A7/A8/A10/A10b/A10c/A11/A13/A14/A-zero/A-sc22/A-baseline)**全部**经
   `gate_check(...)` 或 `main(argv)` 直接调用——没有一条断言"沿 `SKILL.md` 指令执行 C.2.4 时
   会触达 `_verify_branch_exists()`"。
4. Spec A `:37-39`(⛔不在范围)把「SKILL.md 两处散文收敛为 helper 调用(D1)」整块划给 B 侧,
   但没有承认这个划分的直接后果:**在 B 落地前,本 Spec 交付的代码对 AI 实际执行路径的作用
   是零**——这正是我作为 QA 席位最该抓的一类缺陷: 一个测试集合完全自洽、红窗真实、内部无懈可击,
   却测的是错误的维度(memory `feedback_invariant_dimension_must_match_error_dimension`:
   机械不变量的维度须匹配错误的维度)。

**how_it_goes_red**(可证伪,今天就能复现,不需要等 Phase B):
Phase B 按 Spec A 逐字实现 `_verify_branch_exists()`(不改 `SKILL.md` 执行流程,这是 A 自己的
非目标)并合并上线。之后任意一次真实 C.2.4:AI 沿 `SKILL.md:243` 指令跑
`aether ci status --branch <main> --in-flight --json`——这条命令**不经过** `pre_merge_gate.py`,
新增核验不会被执行,输出仍是 `runs:[]` RC=0,verdict 仍判 green。#137 原始症状原样复现,而
`test_pre_merge_gate.py` 里 12 条新 SC 全绿——**测试集合报告"已修复",生产行为报告"未修复"**,
两者不矛盾,因为它们衡量的根本不是同一件事。

**与同轮其他席位的收敛**: 与 `post_spec-R1-0`(tech-lead)M-1、`post_spec-R1-1`(backend-architect)
Finding 1 结论一致;backend-architect 判 Critical,tech-lead 判 Major。我独立形成的判断也是
**Critical**——理由: 这不是"遗漏了一个边角覆盖",是**整个 SC 集合的测量对象系统性地够不到症状
发生地**,且 DEC-20260812-001 §3 与 proposal 的 §Why 都把「关掉恒绿腿」当作已完成的价值主张来
写,若据此 close #137 就是 memory `feedback_paper_fix_antipattern` 的教科书实例。

**blocks_phase_b**: true

---

### C-2 [Critical] Rule #6 substitute(SC-A6/A13/A-zero)对它声称要替代的两处 `SKILL.md` hunk 恒绿——空真的 substitute

**locator**: `proposal.md:191-201`(§Rule #6)+ `:171-175`(SC-A6/A13/A-zero 定义)×
`aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:232-263`(`_build_output`)

**evidence**:

Spec A `:196-197` 逐字提名「SC-A6 / A13 / A-zero」作为 SOT 判据表第一行(描述性)的
substitute——即它们必须是「回退 `SKILL.md` 那两处改动(`:267` 加 `gate_error` 键 / `:279` 早退
注记同步)后, fixture 会转红」的 baseline-failing 测试。我独立读了 `_build_output`(`:232-263`):
`gate_error` 是否写入 `SKILL.md` 的 Output schema 示例, 与 SC-A6/A13/A-zero 断言的
`gate_check()` 返回 dict 里是否含 `gate_error` 键**完全无关**——三条 SC 断言的都是 Python 层
`gate_check()` 的**返回值**,不读 `SKILL.md` 文件本身一个字节。

**how_it_goes_red**(我独立复核了 tech-lead 给出的机械复现,逻辑成立): 在 Phase B 落地分支上
只回退 `SKILL.md` 的那两处 hunk(`git checkout -- SKILL.md`),保留全部 `.py` 与测试改动,
`pytest -k "sc_a6 or sc_a13 or sc_a_zero"` 三条**仍然全绿**——因为它们的断言对象是
`gate_check()` 的 dict 返回值,与 `SKILL.md` 文件内容之间没有任何机械耦合。substitute 的定义性
要求(SOT `:26` 逐字「baseline-failing」)在此处不成立⇒这三条 SC**不是**那两处 `SKILL.md` hunk
的 substitute,只是与它们同批出现、彼此无关的另一组测试。

**为什么我作为 qa-engineer 判它 Critical 而不是"Rule #6 分类学术问题"**: 这直接落在我的审视
角度第二条「有无恒红恒绿空真」——一条被**明确指定**用来担保 Rule #6 豁免合法性的 SC,对它要
担保的具体改动是空真的,这正是 memory `feedback_false_green_dual_is_permanent_red` 描述的
"假绿"形状: 该信号在健康常态下应该跟随 `SKILL.md` 改动而红/绿,但它对 `SKILL.md` 改动本身
完全不敏感,永远只反映 `.py` 层的状态。

**与同轮收敛**: 与 tech-lead C-1(a) 独立收敛(证据链与复现方法一致)。

**blocks_phase_b**: true

---

### M-1 [Major] SC-A7「打桩边界(钉死)」段自相矛盾,且回归了姊妹 Spec B 已修复的同型缺陷(独立发现,peer 未覆盖)

**locator**: `proposal.md:186-187`(§Success Criteria「打桩边界(钉死)」)×
`proposal.md:176`(SC-A7 定义行)对照 `premerge-gate-mainbranch-failclosed/proposal.md:358-361`
(B 侧同一段落, R3-fix 已修正)

**evidence**:

Spec A `:176` SC-A7 行本身逐字写:「`ls-remote` 返 **128**(指向不存在的 remote 名, **或 mock**)」
——允许两种手段。但 `:186-187`「打桩边界(钉死)」段落逐字写:「SC-A7 / SC-A8 **必须 mock**
(真实 `ls-remote` 无法产出确定性 128 或 timeout)」——把 SC-A7 收窄成**只能 mock**,与它自己
定义行的「或 mock」直接矛盾。

**我独立实测(不依赖任何既往报告)证明该"必须 mock"的理据是错的**:

```bash
$ git ls-remote --heads /tmp/does-not-exist-repo-xyz master
fatal: '/tmp/does-not-exist-repo-xyz' does not appear to be a git repository
fatal: Could not read from remote repository.
rc=128
```

真实(非 mock)`ls-remote` 指向不存在的 remote 名/路径,**确定性**返回 128——这与「打桩边界」段
声称的「真实 `ls-remote` 无法产出确定性 128」直接矛盾,且是可重复实验(git 对不可达 remote 的
128 退出码是稳定契约,不依赖网络时序)。

**这不是本 Spec 首次出现这个错误——它是对姊妹 Spec B 同一段落已修复错误的回归**:
`premerge-gate-mainbranch-failclosed/proposal.md:358-361`(B 侧, post_planning R3 修订版)
逐字记载: 「上一版此段有两处自相矛盾,本版一并更正: … 逐字写『SC-M7 必须 mock(真实 `ls-remote`
无法产出确定性 128)』,而 SC-M7 自身的定义允许『指向不存在的 remote 名』这一非 mock 手段,
且受控实验证明它确实确定性返 128」——B 侧把这条错误**改成**了「SC-M7 两种手段皆可: …
经受控实验实测确定性返 128(非 mock 亦可复现),或直接 mock」。Spec A 承接 B 侧材料时(A 自称
「承自八轮审计的输入,逐条注明来源」),这一条**已修复的更正被静默丢失**,A 的文本又变回了
B 侧 R3 之前那个已经被推翻的错误版本。

**how_it_goes_red**: 命令级,见上方独立实测;字面对照 B 侧 R3-fix 段落即得出「A 回退了一个已修复
的缺陷」的结论,二者任一都足以证伪 A `:186-187` 的现文。

**为什么落在我本席而非重复peer**: 我核对了 `post_spec-R1-0`(tech-lead)与 `post_spec-R1-1`
(backend-architect)全文,均未提及「打桩边界」段落或 SC-A7 的这处矛盾——这是我审视角度
「打桩边界自洽」项下的独立产出。

**影响面为何只判 Major 而非 Critical**: 无论 Phase B 实施者选择 mock 还是真实裸仓,SC-A7
本身的验收断言(`fail` + `kind=="main-branch-verify-failed"` + 未重试)都能正确落地——这条
矛盾不会导致某个坏实现被放行,只会在"选哪种测试手段"上误导实施者、或在评审时因为两处表述
互斥而产生返工争议。它是文档自洽性缺陷,不是验收有效性缺陷。

**blocks_phase_b**: false

---

## 3. 三条负控早退——独立验证,未发现缺陷(供交叉参考)

按本席审视角度第四项「三条负控早退是否真能拒绝坏实现」逐条构造反例:

| SC | 我构造的坏实现 | 是否被拒绝 | 判断依据 |
|---|---|---|---|
| SC-A10(`enabled=false`) | 把 `_verify_branch_exists()` 插在 `_normalize_config` 之后、`enabled` 检查**之前** | ✅ 会被拒绝 | 断言含 `assert ls-remote 未被调用`(因果断言),该坏实现会先跑 ls-remote 才检查 enabled,断言必红 |
| SC-A10b(no-backend `:338`) | 把核验插在 `resolve_ci_backend` **之前** | ✅ 会被拒绝 | 同上,因果断言而非仅六键快照 |
| SC-A10c(precheck 失败 `:345`) | 把核验插在 `backend.precheck()` **之前** | ✅ 会被拒绝 | 同上 |
| SC-A11(存在 + in-flight → wait) | 用一个"总是判 fail"的伪核验(cheat) | ✅ 会被拒绝 | SC-A11 要求 `verdict=wait` 不变,cheat 实现会把它变成 `fail`,直接红;`SC-A-baseline`(111 全绿)亦会连带发红,双重覆盖 |

**结论**: 三条负控早退的设计**是自洽且有判别力的**——因果断言(`assert ls-remote 未被调用`)
而非仅比对"六键快照"是关键,Spec A `:179` 自己写明"兄弟早退不同步则该类只修了一个实例"并对
三个早退**都**补了这条因果断言,做到了 memory `fix-the-class` 要求的同形位置全覆盖。这一项我
未发现缺陷,不构成 finding。

---

## 4. 溯源表(`proposal.md:245-262`)抽查

抽查 6/12 行,独立回源实测,全部命中(与 tech-lead 11/11、backend-architect 的独立复核结果一致,
未发现新的溯源错误):

| 事实 | 我的复核方式 | 结果 |
|---|---|---|
| 五个插入点行锚 | Read `pre_merge_gate.py` 全文 328/338/344/345/356/357/358/366 | ✅ 全部命中 |
| `SKILL.md:255`「fail → BLOCK + raw_message」 | Read `SKILL.md:255` | ✅ 逐字命中 |
| `ls-remote` 零命中亦返 rc=0 | 独立裸仓实验(§1) | ✅ 复现 |
| `--exit-code` 无命中返 rc=2 | 独立裸仓实验(§1) | ✅ 复现 |
| `_run_with_retry`(aether.py:164-187)硬绑 binary / 只捕 TimeoutExpired / 无 cwd / text=True | Read `aether.py:164-187` | ✅ 全部属实 |
| `test_ci_backends.py` 25 tests 零命中 `_run_with_retry` | `grep -c '_run_with_retry' tests/test_ci_backends.py` = 0;`grep -c 'def test_'` = 25 | ✅ 属实 |

`SC-A*` 前缀与既有测试号段(sc9/10/11/12/13/15/21/22)无冲突——独立 grep 确认(`grep -n
"def test_sc" tests/test_pre_merge_gate.py`),无 `SC-A` 命名。

---

## 5. 未做的事(边界声明)

- 未继承 B 侧 R4 的 3 条 Critical(全属 B 侧);
- 未改任何文件(报告除外),未 commit/push,未调外部 API;
- 受控裸仓实验全部建在 scratchpad,与本仓无交互;
- 未对 B 侧 proposal 提任何 finding;
- 阅读同轮 `post_spec-R1-0` / `post_spec-R1-1` 仅用于交叉核对措辞与避免纯重复呈现,C-1/C-2
  的证据链与判断均为本席独立收集/独立复现,非转述。
