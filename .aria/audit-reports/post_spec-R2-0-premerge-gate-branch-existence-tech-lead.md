---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T15:25:39.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — tech-lead — Spec A `premerge-gate-branch-existence`

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** (0C + 5M + 3m) · 4 条 `blocks_phase_b`

席位视角: 划界是否自足 / Level 2 与 MINOR 定档 / 与 B 侧的边界有无重叠或缺口。

---

## 0. 我实跑过的命令 (所有数字的出处)

```bash
git rev-parse HEAD                                  # e165df4 (R1-fix)
git -C aria rev-parse HEAD                          # af87cae (proposal 声明的基线, 一致)
python3 -m pytest tests/ -q                         # 111 passed  ← §测试基线属实
python3 -c "print(issubclass(UnicodeDecodeError, OSError))"   # False ← §5/SC-A14 属实
git -C /home/dev/Aria ls-remote --heads origin main            # 零行 + RC=0  ← 属实
git ls-remote --heads /tmp/does-not-exist-repo-xyz master      # RC=128       ← 属实
grep -rn 'gate_check(' aria/ --include=*.py                    # 24 测试调用 + :298 def + :435 调用 = 25 ← 属实
grep -c 'gate\.gate_check(.*main_branch' tests/test_pre_merge_gate.py   # 0
grep -n 'main_branch' tests/test_pre_merge_gate.py             # 唯一 1 行 (:669, 是 mock 断言不是入参) ← 24/24 属实
grep -rn "main(argv" tests/ | wc -l                            # 0   ← CLI 入口零覆盖属实
grep -rn 'gate_error' aria/ | wc -l                            # 0   ← 零消费者属实
grep -c '_run_with_retry' tests/test_ci_backends.py            # 0   ← 恒绿判据属实
grep -c -- '--main-branch "<MAIN_BRANCH>"' aria/skills/phase-c-integrator/SKILL.md   # 0
grep -n -- '--main-branch' aria/skills/phase-c-integrator/SKILL.md                   # 零行
ls -1 aria-plugin-benchmarks/ab-suite/ | grep -i phase-c        # 两个套件均在
which aether                                                    # /usr/local/bin/aether (本机有, 容器未必)
```

行锚逐个实读复核: `pre_merge_gate.py` `:328`/`:338`/`:344`/`:345`/`:356`/`:357`/`:358`/`:366` **8/8 命中**;
`:68`/`:116` (v2.0 弃用承诺) / `:251` (从 `ci_backends.aether` import 常量先例) / `:427`/`:435` 命中;
`SKILL.md` `:167`/`:168`/`:242`(步骤 2.5 + 执行上下文契约逐字)/`:243`/`:244`/`:253`/`:255`/`:259`/`:260`/`:265-277`/`:279` 命中;
`path_coverage.py` `:78`(`_run_git(args, cwd)`)/`:81-84`(#124 surrogateescape)/`:91`(`cwd=cwd`)/`:93`(三合一 except)/`:105`(`_repo_root` = `rev-parse --show-toplevel`, `cwd=None`)/`:430` 命中;
`tests/test_pre_merge_gate.py` `:59-80`(`_ProbeCacheResetMixin`, docstring 逐字属实)/`:710`(`test_sc22`) 命中。

**A 承自八轮的事实层面, 我这一轮再次回源, 无一条需要下调。**

---

## 1. R1 的 2C + ~10M 闭合情况 (逐条回源, 区分「写下来」与「闭合」)

我直接读了 R1 五席的原始 findings (journal, 26 条 = 6C+14M+6m, 与 aggregate 的分席计数逐格相符;
`blocks_phase_b` 逐条统计 = 1+5+2+2+4 = **14**, 与 aggregate 一致)。

### C-1 划界承重句 — **实质闭合, 但闭合的方式是「重定完成定义」而非「补上缺口」, 这是正确的取舍**

R1 的三条同源 Critical (backend-architect C / qa-engineer C1 / knowledge-manager C2) 说的是同一件事:
存在性核验修的是 `gate_check()` 那份实现, 而 AI 走的是 `SKILL.md` 散文那份。
R1-fix 的处置: §Why 补 §根因 逐字引用 · 承重句加「`gate_check()` 这份实现里的」限定 ·
新增 §残余暴露 整节 (逐字「A ship 不构成 #137 闭环」+ 残余的精确形态) · 连带更正 B 抬头与 DEC §3。
我去 B 侧与 DEC 实测了这两处连带更正 —— **都真的落了** (B `proposal.md:15-21` 逐字「该句不成立, 已作废」;
DEC `:80-105` 追加带日期的更正块且 owner 原文保留)。memory `feedback_cross_doc_claim_verify_at_target`
要求的「去 B 实测」我做了, 不是自证。

**这不是 paper fix**: R1 给的处方本身就是「补声明」(扩范围纳入 D1 = 拉 MAJOR = 拆分归零),
而 A 拒绝为残余编造哨兵 SC 的理由 (「它在 B 落地后必须被删, 是 landmine」) 与
memory `feedback_false_green_dual_is_permanent_red` 的判据一致, 我认可。

**但闭合是有洞的**: 「不得据 A ship 关闭 #137」这条禁令的**唯一载体是一份 D.2 会被归档的 proposal 散文**,
而 A 同一行又逐字写「无外部动作 …… 留痕与否由 owner 决定」—— 禁令被断言了, 它唯一的执行通道被设成可选。
详见 Finding 5 (与 Level 2 无 `tasks.md` 承载是同一个缺口的两条腿)。

### C-2 Rule #6 改判第二行 — **改判本身正确, 我独立核了 SOT, 且 R1 aggregate 的两处行号引错在 R1-fix 里被纠正了**

我实读 `standards/conventions/skill-benchmark-exemption.md`:
- `:28` = 第一行 (描述性) 的处置, 逐字「**deterministic substitute**: 以结构化测试 (SC 级 baseline-failing 单元/集成测试, 必须在场) 替代 AB」;
- `:31` = 「拿不准算不算处方性 / 算不算在范围内 → **照跑** (宁跑勿豁)」;
- `:33` = SKILL.md 附加约束, 逐字「仅当变动是**事实性同步** (溯源注释 / 行号勘正 / 术语修正) 且 frontmatter `description` 零变动, 才可能落进第一行 …… `description` 或**指令流程变动 ⇒ 一律第二行**」。

**R1 aggregate 引的是 `:26` (表头行) 与 `:33` 第四行 (`:33` 不是「拿不准」那格) —— 两处都错。
A 的 R1-fix 版逐字引的是 `:28` / `:31` / `:33`, 三处全对。** 改判的三条依据 (a)(b)(c) 我逐条核:
(a) A 往 §C.2.4 执行流程加编号步骤 = 指令流程变动 ⇒ `:33` 直接管辖 ⇒ 第二行, 成立;
(b) A 的两处描述性 hunk 不属 `:33` 那三项穷举, 落 `:31` 照跑, 成立;
(c) SC-A6/A13/A-zero 无一读 `SKILL.md` ⇒ 不满足 `:28` 的 baseline-failing, 成立。
三处互斥 (`:196`/`:201`/`:39`) 已消除 —— §Why ⛔ 清单现逐字是「**B 侧自己的** Rule #6 AB」。
旁证: B 侧 `proposal.md:379` 对自己的 D1 用的是**同一条 SOT 条款**得出同一档位, 两侧一致。

⇒ **C-2 真闭合。** 唯一残留是 A 没继承 B 已成文的「同一套件对 C.2.4 覆盖薄」限定 (Finding 7, Minor)。

### ~10 条去重 Major — 逐条

| R1 Major (去重后) | 处置 | 闭合? |
|---|---|---|
| §3「唯一合法插入点」零 SC | 新增 **SC-A-order** (`assert evaluate_path_coverage 未被调用`) | ✅ **代码侧**闭合; **doc 侧同款顺序约束仍零锚** → Finding 1 |
| CLI `--remote` 接线零 SC | 新增 **SC-A-cli** | ⚠️ 建了, 但该 SC 自身够不到核验步 → Finding 3 |
| 「24 处零改动」漏计第 25 处 | §版本 三项并列 (总体/范围/计数法) + 点名 `:435` | ✅ 我实跑复核 = 25, 属实 |
| Level 2「无跨仓同步面」自我推翻 | 改为「无跨仓**内容**同步面」+ 发版同步面照常适用 | ⚠️ 措辞闭合, **承载缺口未闭合** → Finding 5 |
| `aether.py` 条件性入 scope | §5 **钉死不动** + 机械判据 `git diff --stat` | ✅ 闭合 (且给出了「零测试保护 ⇒ 等价判据恒绿」的理由, 硬) |
| cwd 轴只有否定式 | §3 新增正面规定 + **SC-A-cwd** | ✅ 正面规定本身**经得起核** (`_repo_root():105` / `_run_git():78/:91` / 步骤 2.5 契约逐字, 我全部实读命中); SC 侧 → Finding 3 |
| SC-A14 正向枚举 (空真) | 改参数化探针 + 显式点名 `UnicodeDecodeError` | ✅ 承重那条已钉住 (见 §2) |
| `:78` 引用 `SC-M6` 悬空 + 归因错 | 改 **SC-A-zero** + 逐字更正 | ✅ |
| SC-A7「必须 mock」理据被实测证伪 | 改「两种手段皆可」+ 逐字承认 B 侧 R3 已更正过而 A 承接时丢了 | ✅ 我复跑 rc=128 确认 |
| 打桩边界只覆盖 5/12 | 现覆盖 **16/16** | ✅ 我逐条点过 |
| `raw_message` 无 SC 兜底 (m) | SC-A6/A7/A8/A14 全部加「含分支名与 remote 名」 | ✅ |
| catch-all 不重试的权衡未评估 (m) | §2 补显式权衡段 (引 `workflow-runner:337` 逐字) | ✅ |
| 五个行锚 vs 8 个行号 (m) | 补计数法 | ✅ |
| 行为兼容面未评估 | 新增 §行为兼容面 (翻转的确切条件 + 实测在场 + 迁移说明 + Rule #10 留痕请复议) | ✅ 这一条做得比 R1 要求的更完整 |

**结论**: R1 的 2C 都不是纸面修复; ~10M 中 11 条闭合、3 条部分闭合。
**旧 finding 无一复发** —— 与 B 侧四轮的同一观察一致 (执笔不是瓶颈)。

---

## 2. 复核执笔方的两条「新发现」与它对主 loop 的三条纠正

**(1) `UnicodeDecodeError` 不是 `OSError` 子类 — 属实。**
实跑 `python3 -c "print(issubclass(UnicodeDecodeError, OSError)); print([c.__name__ for c in UnicodeDecodeError.__mro__])"`
⇒ `False` / `['UnicodeDecodeError','UnicodeError','ValueError','Exception','BaseException','object']`。
§5 指定的三合一元组 `(TimeoutExpired, FileNotFoundError, OSError)` 结构上接不住它, `text=True` 下裸抛穿过 `gate_check()` 成立。
**处置够不够**: 够。SC-A14 已把 `UnicodeDecodeError` **显式列进参数化探针**(不是靠再枚举一次), 承重的那条钉死了。
第五个探针「任取一个不在实现 `except` 元组里的异常类」写得含糊 (运行时不能 introspect except 子句, 需 AST 解析实现源码),
落地时最省事的写法是硬编码一个类 ⇒ 退化为「再多枚举一项」。但它是加分项不是承重项, 我不为它开 finding。

**(2) SC-A11 打桩即退化为恒真 — 属实, 修法正确。**
若把核验入口打桩成「存在」, 则「核验放行了一个真实存在的分支」这句被桩保证, 断言只剩验 backend 路径;
「恒判 not-found」的实现会被桩掩住 ⇒ 对它声称验的东西恒真。改用**真实受控裸仓 + mock backend** 正确。
⚠️ **注意这条修法本身正是 Finding 3 的反证**: R1-fix 在 SC-A11 上想到了「必须安排 backend」,
在同批新写的 SC-A-cli / SC-A-cwd 上没想到 —— 同一类只推广了一半。

**(3) 对主 loop 汇总的两条指控 —— 一条属实、一条只能算部分属实。**
- **归属错误: 属实。** aggregate 的「两条 A 声称里没想到的破坏面 (**backend-architect**)」两条都不是 backend-architect 报的
  —— 该席原始 findings 只有 1C (划界) + 1M (Rule #6 SOT `:33`)。行为兼容面那条出自 **tech-lead 的 `additive_claim` 字段**,
  跨仓同步面那条出自 **tech-lead `additive_claim` + code-reviewer 的 minor**。
- **未去重: 部分属实。** aggregate 的数字全部对得上原始 journal (6C/14M/6m/26, 14 blocking, 分席五格全对),
  且它自己标了「**原始**」并在正文把 6C 归成了两个承重簇 —— 不能说没去重。
  但主 loop 在 commit message / 交接里写的「6C 里 **4 条**指向同一件事」与原始数据对不上: 实际是 **3 + 3**
  (划界簇 = backend-architect C · qa C1 · km C2; Rule #6 簇 = tech-lead C · qa C2 · km C1) ⇒ 去重后 **2C** 这个结论对, 但配比说错了。
- ⇒ **主 loop 的汇总在数上可信、在归属上不可信。** 本轮我按要求直接读了 journal 原始 findings, 未依赖 aggregate 的叙述。

---

## 3. Findings

### M-1 · 「新增 §C.2.4 编号步骤」是 Rule #6 第二行定档的唯一承重依据, 却零机械锚且内容欠定 (blocks_phase_b)

**Locator**: `openspec/changes/premerge-gate-branch-existence/proposal.md` §Impact `SKILL.md` 行 ① × §Rule #6 (a) × SC 表 (SC-A-doc)

§Rule #6 (a) 逐字: 「A 往 `gate_check()` 中间插新步 …… **本 Spec 因此明确要求**新增对应编号步骤 (见 §Impact 的 `SKILL.md` 行) ⇒ **指令流程变动**成立」——
即整个第二行定档挂在这一处 hunk 上。§Impact ① 对它的规定逐字是「位于步骤 **2** 与 **2.5** 之间, 号建议 `2.2`;
**号本身非承重, 承重的是它落在 2 与 2.5 之间**」+「**在该步骤处逐字标注**它与步骤 3 硬编码 `main` 的不一致并指向 B 侧 D1」。

16 条 SC 中唯一读 `SKILL.md` 的是 **SC-A-doc**, 而它逐字只解析「§C.2.4 **Output schema json 块**」(实读 = `:265-277`),
即 §Impact 的 hunk **②**。hunk **①** (编号步骤) 与 **③** (`:279` 归纳句四类→五类) **零断言**。

**它在什么实现下会红**: 都不会红 ——
(a) 落全部 `.py` + 全部测试 + 只改 ② ⇒ **16/16 全绿**, 而 Rule #6 (a) 的定档依据当场不存在, 且 A 自己逐字警告的
「文档流程与 helper 流程当场分叉 (违反规则 #3)」实际发生;
(b) 加了步骤但落在 **2.5 之后** ⇒ 16/16 全绿, 而 §Impact 逐字点名的「承重的是它落在 2 与 2.5 之间」被违反;
(c) 加了步骤但**不标注**与步骤 3 的不一致 / 不指向 B 侧 D1 ⇒ 16/16 全绿, 而 §残余暴露 的唯一留痕落点消失。

**「机械化不可能」的辩解在这里不成立**: §残余暴露 拒绝为**散文执行行为**建 SC 是对的 (没有 harness 能执行散文),
但「新步骤在不在 / 排第几 / 含不含那句标注」是**纯文本断言**, SC-A-doc 已经证明这份文件可被解析断言。

**这是 `fix-the-class` 的第三次同形复发**: R1 抓的正是「§3 自称唯一合法插入点却零 SC」, R1-fix 用 SC-A-order 补了**代码侧**顺序约束,
**doc 侧的同款顺序约束 (落在 2 与 2.5 之间) 没补**。A 自己在 SC-A10b 就写着「兄弟早退不同步则该类只修了一个实例」。

---

### M-2 · A 新增的 SKILL.md 步骤会撞 B 侧承重 SC-M3a 的精确计数; A 已对同类另一实例做过检查, 独漏这个 (blocks_phase_b)

**Locator**: `premerge-gate-branch-existence/proposal.md` §残余暴露 + §Impact ① × `premerge-gate-mainbranch-failclosed/proposal.md:345` (SC-M3a)

B 侧 `:345` 逐字实读:

```
| **SC-M3a** | `grep -c -- '--main-branch "<MAIN_BRANCH>"' .../SKILL.md` | **2** | **0** | 必红 —— **D1 承重红窗**。断言的是**占位符形态**, 两处散文各一条 |
```

期望值是 **精确的 2**, 注解逐字「**两处散文各一条**」。我实跑核对今日基线:
`grep -c -- '--main-branch "<MAIN_BRANCH>"' aria/skills/phase-c-integrator/SKILL.md` = **0**;
`grep -n -- '--main-branch' aria/skills/phase-c-integrator/SKILL.md` = **零行** (整份文件今天没有任何 `--main-branch`)。

A 侧 §残余暴露 逐字: 「本 Spec 给执行流程新增的核验步用 **`<MAIN_BRANCH>` 占位符**」;
而 A 的 §根因 逐字指认的病症是「**SKILL.md 从无带参 helper 调用示范**」—— 该指认直接把
「写一行带 `--main-branch "<MAIN_BRANCH>"` 的 helper 调用示范」推成新步骤最自然的落地形态。

**它在什么实现下会红**: A 按该形态落地 ⇒ `SKILL.md` 出现**第 3 处**该字面 ⇒ B 的 D1 把两处散文收敛后
`grep -c` 得 **3 ≠ 2** ⇒ **B 一条已打磨八轮的承重红窗 SC 在完全正确的 B 实现下必红**。
A 全文无一句要求 B 重设该期望值; B 抬头的保留清单也没有这条。

**A 已经认出了这个形状的另一个实例并处置了** —— §4 逐字「示例的 `branch` 用**占位符**而非真值 ——
写 `"main"` 会与 B 侧的 SC 对撞」。同一类只检查了一个实例, 而漏掉的这个恰好落在两个 Spec 的接缝上
(memory `fixes-contradict`: 多 agent 并行审计不覆盖它, 接缝落在角度之间)。

**修法二选一**: (i) A 明文规定新步骤**不得**含 `--main-branch "<MAIN_BRANCH>"` 字面 (改用别的表达),
或 (ii) A 明文声明「本步骤使 B 侧 SC-M3a 的期望值由 2 变 3」并把该更正写进 B。二者都是一句话的事, 但必须选一个。

---

### M-3 · SC-A-cli / SC-A-cwd 走的路径在 no-backend 早退之前就返回了, 对正确实现恒红且随环境漂移 (blocks_phase_b)

**Locator**: SC 表 `SC-A-cli` / `SC-A-cwd` × §3 (核验点在三早退之后) × `scripts/pre_merge_gate.py:337-339`

§3 逐字规定核验点在三个早退**之后**, 其中第二个是 `:338 if backend is None: → 早退`。我实读并实跑验证:

```python
# pre_merge_gate.py:337-339
backend = resolve_ci_backend(cfg)
if backend is None:
    return _no_ci_output(cfg["no_ci_fallback"])       # DEFAULT no_ci_fallback = "skip_with_warning" ⇒ verdict=green
```

实跑 (`mock.patch.object(gate,'resolve_ci_backend',return_value=None)`) ⇒ `gate_check(pr_branch='feat/x')['verdict']` = **`green`**。
backend 能否解析出来完全取决于**宿主环境**: `AetherBackend.probe()` (`ci_backends/aether.py:62-69`) = `shutil.which("aether")`;
GHA stub `probe()` (`github_actions.py:23-34`) = `shutil.which("gh")` + `gh auth status`。本机 `which aether` = `/usr/local/bin/aether`, **标准 pytest 容器没有**。

SC-A-cli 逐字「走 **`main(argv=[...])`** 真实 CLI 入口」, 对 backend **零安排**;
SC-A-cwd 逐字「同一实现、同一参数 …… 各跑一次」, 期望「W₁ ⇒ `fail`+`not-found`」, 亦零安排。

**它在什么实现下会红**: 在**没有 aether/gh 的机器上**, 接线正确的实现与漏接线的实现**都**在 `:339` 早退返 `green`
⇒ SC-A-cli 断言的 `verdict=fail` 落空 ⇒ **对正确实现恒红**, 判别力为零, 并连带打破 SC-A-baseline 的「111 + 新增 ≥ 全绿」;
在本机则会真的 shell out 到 `aether` binary (`precheck()` 跑 `_verify_in_flight_flag()`) ⇒ 结果随 binary 版本漂移。
两个方向都不是「实现错了」而是「SC 建错了」。

**同轮已有正解, 只推广了一半**: 打桩边界表给 SC-A11 的注逐字是「须用**分支确实存在**的受控裸仓 + **mock backend** 提供 in-flight runs」
—— 那正是这两条缺的那句。A 也确实警惕过 ambient 依赖 (SC-A-cli 逐字「fixture 必须自带受控 `origin`, **不得依赖 ambient origin**」),
但只防了 `origin` 这一个 ambient, 没防 backend 这个 ambient。

---

### M-4 · SC-A-doc 的代码侧操作数未定义, 两种落地方式各损失它声称能力的一半

**Locator**: SC 表 `SC-A-doc` × §4 (`gate_error` 的产出形态) × `scripts/pre_merge_gate.py:232-263` (`_build_output`)

SC-A-doc 逐字: 「从 `SKILL.md` §C.2.4 Output schema json 块**实际解析**出的键名集合 (⛔ 不得硬编码 doc 侧)
== **`_build_output` 的实产键全集** (六固定键 ∪ `path_coverage` ∪ `gate_error`)」,
「怎么会红」列逐字宣称「只落 `.py` 而漏 `SKILL.md` schema 键 (**或反之**) 的实现必红」。

我实读 `_build_output` (`:232-263`): 它固定产六键, 只对 `path_coverage` 做条件加键, **形参里没有 `gate_error`**。
而 §4 只说 `gate_error` 是「additive 可选结构化副本」, **从未规定它必须经 `_build_output` 产出**。

**它在什么实现下会红 / 失效**:
- (i) 实现把 `gate_error` 在 `gate_check()` 内直接 `out["gate_error"] = {...}` 附加 (**完全合规**),
  测试按 SC 字面把代码侧取为 `_build_output` 的产键 ⇒ 代码侧 7 键 vs doc 侧 8 键 ⇒ **对合规实现必红**;
- (ii) 为规避 (i) 而把代码侧硬编码成那 8 个字面 (SC 只禁了硬编码 **doc 侧**) ⇒
  「`SKILL.md` 有 `gate_error` 而 `.py` 从不产出」这个方向**全绿** ⇒ 它自称的「或反之」不成立, doc 漂移只防住一半。

二者必居其一。修法: 明文规定代码侧操作数取自**核验失败路径的真实输出** (跑一次判 `not-found` 的调用, 取返回 dict 的键集),
或明文规定 `gate_error` 必须经 `_build_output` 产出。

---

### M-5 · Level 2 定档与 A 自己承认的义务集不匹配: **三项**义务零承载, 而「须 owner 裁量」这句本身没有消费者 (blocks_phase_b)

**Locator**: proposal 抬头 `Spec Level: 2` × §Impact 发版同步面行及其下方风险声明 × §Rule #6 × §Impact 外部行

R1 抓的是两条**定档依据**自相矛盾 —— 那一半 R1-fix 闭合了 (改「无跨仓**内容**同步面」+ `aether.py` 钉死)。
留下的是**承载**这一半, 而 A 只对其中一项作了声明:

| 义务 | 逐字出处 | 有 checkbox 承载吗 | A 是否承认缺口 |
|---|---|---|---|
| 发版同步面 (子模块 5 文件 + **主仓 gitlink** + VERSION + badge + i18n) | §Impact 发版同步面行 | ❌ | ✅ 承认 |
| **Rule #6 照跑 AB** | §Rule #6 逐字「照跑 AB, 零裁量」+「具体 eval 选取属 A.2/Phase B」 | ❌ | ❌ 未提 |
| **「不得据 A ship 关闭 #137」** | §Impact 外部行 + §残余暴露 | ❌ | ❌ 未提 |

**它在什么实现下会红**: 都不会红。A.2/task-planner 读 frontmatter `Level: 2` ⇒ 按 CLAUDE.md 判据表**不出 `tasks.md`**
⇒ 三项义务的唯一载体是一份 D.2 就会被归档的 proposal 散文; 而 A 自己逐字承认 custom check `m6-version-badge-match`
「对『主仓 gitlink 未 bump』这个方向**结构上失明**」⇒ 漏做任一项时**没有任何信号会转红**。
B 侧 R4 三条 Critical 之一 (`TASK-017` 漏 gitlink) 就是这个形状的已实现版本。

**更硬的一层**: A 逐字写「两条出路 (**须 owner 裁量, A 不自行决定**)」, 但**没有任何闸门会读这句话**,
而 A 已经带着 `Level: 2` 往下走了 —— 这正是 memory `fix-recurs-in-fallback` 记的「**有记录 ≠ 有路由**: 无人消费的诊断字段 = 静默」。
`#137 不得关闭` 那条尤其典型: 禁令被断言在 §Impact, 而同一行又逐字写「**无外部动作** …… 留痕与否由 owner 决定」
—— 唯一能把禁令送到「关闭动作真正发生的地方」(issue 本身) 的通道被设成可选。

⚠️ 我**不**指控 A 违反规则 #10 —— A 把判断留痕并请复议, 程序是对的。
本 finding 说的是: 留痕这个动作**没有接收端**, 而 A 已按未决的那一侧继续执行。
最小修法: 把「(i)/(ii) 待裁」升为 proposal 顶部的显式 **BLOCKER** 字段 (A.2 入口须读), 或直接取 (ii) 出 `tasks.md` 承载三项。

---

### m-1 · A 与 B 各自声明要为**同一组**同形兄弟位置开 follow-up, 归属未定

**Locator**: A `proposal.md` §非目标 末条 × B `proposal.md:410` / `:430` follow-up 清单 (2)

两侧逐字几乎同句: A「**不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 ·
`state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"` …… **开 follow-up**」;
B `:410` 同句, `:430` follow-up 清单 (2) 逐字「`fetch_gate.py` / `worktree_manager.py:170` 同形回落」。
**它在什么实现下会红**: 不会红 —— 两侧各自 ship 时都可以合理认为对方已开, 或各开一个重复 issue。
一句归属声明即可 (memory `delegate-verify`)。

---

### m-2 · A 的 Rule #6 AB 未继承 B 已成文的「同一套件对 C.2.4 覆盖薄」限定

**Locator**: A §Rule #6 末段 × B `proposal.md:383`

B 逐字: 「ship 前须过 `ab-suite/phase-c-integrator.json` 与 `ab-suite/phase-c-integrator-pre-merge-gate.json` ……
**已知**: 两套件对 C.2.4 覆盖薄 (承 aria-plugin #127), 本 Spec **不以此降档**, 且诚实声明 D1 的行为证据主要由 SC 承担,
**AB 是合规义务而非本 change 的主要证据来源**」。我实测两套件均在 (`ls ab-suite/ | grep phase-c` 命中两者)。
A 只写「AB 形态照 v1.65.0 先例 …… 具体 eval 选取属 A.2/Phase B」, **不点名套件, 不带任何有效性限定**。
**它在什么实现下会红**: 不会红 —— 反而是「三臂无差异」被读成「AB 通过 = 行为已验证」的风险
(SOT `:73-74` 的已知局限 + memory `feedback_false_green_dual_is_permanent_red` 正是这一形状)。
A 是本轮**新**承接这项义务的 (改判前它不欠 AB), 所以这条限定没有被继承。

---

### m-3 · A 要求把「指向 B 侧 D1」写进**随 plugin 分发**的 SKILL.md, 而 B 的 change_id 按 DEC §6 尚未定

**Locator**: A §Impact ① × `DEC-20260812-001` §6 × `ls openspec/changes/`

A §Impact ① 逐字要求在新步骤处「**指向 B 侧 D1**」。DEC §6 逐字未决项:「B 是改名还是新建 + 归档旧的, **待定**」。
实跑 `ls -1 openspec/changes/` ⇒ 只有 `premerge-gate-mainbranch-failclosed`, DEC §2 建议的 `premerge-gate-prose-helper-convergence` **不存在**。
**它在什么实现下会红**: 不会红, 但两条路都通向悬空引用 —— 写 DEC 建议名 ⇒ **今日即悬空**; 写现名 ⇒ B 按 DEC §6 改名后悬空。
额外一层: `SKILL.md` 是随 plugin 分发给第三方采用者的文件, 把他们指向 Aria 内部 openspec change id 对其**恒悬空**
(同 memory `memory-store-local` 记的「CLAUDE.md/standards 引内部名对第三方恒悬空」形状)。
修法: 标注只写**行为事实**(「步骤 3 仍硬编码 `main`, 与本步骤的 `<MAIN_BRANCH>` 不一致」)+ 指向 **issue #137** (稳定外部锚), 不引 change_id。

---

## 4. 划界自足性 / 定档 / 边界 — 席位结论

**划界 (split_soundness)**: **拆分方向仍然成立, 且 R1-fix 后 A 的完成定义是诚实的。**
A 的价值主张现在被正确地限定在 `gate_check()` 层, 残余暴露有逐字声明与可现场复现的精确形态,
连带更正在 B 与 DEC 两处**实测已落**。A 在代码面确实纯 additive (25 个调用点零破坏, 我实跑复核),
在行为面的运行时翻转也已单独成节并留痕请复议 —— 这比 R1 时完整得多。
**但「自足」现在卡在两处新接缝上**: (a) A 为定档 Rule #6 而新揽的那处 `SKILL.md` 指令流程变动**没有任何验收**(M-1);
(b) 它落地后会破坏 B 侧一条承重 SC 的精确计数, 而两侧文档都没写这件事 (M-2)。
这两条都不推翻拆分, 但它们说明: **A 的边界不是「代码在哪停」, 而是「A 往共享的 `SKILL.md` 里写了什么」——
这条边界 R1-fix 刚刚往外推了一格, 却没有同步推验收面与 B 侧对齐面。**

**Level 2 定档**: 判据表三条 (无架构变更 / 无跨仓内容同步面 / 无破坏性契约变更) 逐条成立, 措辞已修好。
**问题不在判据, 在承载** —— 见 M-5。我不认为该自动升 Level 3; 我认为 (i)/(ii) 这个选择必须有一个真实的接收端。

**MINOR 定档**: 技术上正确 —— 带默认值 kwarg 对 25 个调用点零破坏 (实跑复核), additive 可选键与 `path_coverage` 同构,
`:68`/`:116` 的 v2.0 弃用承诺不被触发 (MINOR ⇒ v1.65.5 → v1.66.0)。
A 主动把「一个此前恒 green 的闸门开始 fail 是否够 MAJOR」留给 owner 复议, 处置正确, 我不加码。

**与 B 侧边界**: 静态归属 (D1/D5/折叠块/24 处补参/v2.0 弃用面/`config.template.json`/B 侧发版面与 AB 留 B) 逐条与 DEC §2 一致, **无 scope creep, 无遗漏**。
B 抬头的作废声明已落。发现的重叠/缺口共三处: **M-2 (承重, SC-M3a 计数)** · m-1 (follow-up 归属) · m-2 (AB 套件限定未继承)。
B 侧 R4 的 3 条 Critical 我逐条核过, 确属 B (gitlink 求值时点 / `config.template.json` 键名面 / `CLAUDE.md:113`),
**未搬运任何一条到 A**; M-5 引用 `TASK-017` 只作**同形先例**, 论证落在 A 自己的 Level 2 承载面上。

## 5. 本轮 fix 引入率 (如实报, 不修饰)

我这 8 条里 **6 条 (M-1 / M-2 / M-3 / M-4 / m-2 / m-3) 由 R1-fix 引入** = **75%**,
其中 4 条正落在执笔方自己点名要求对抗检查的面上 (4 条新 SC 中的 3 条 + Rule #6 改判带来的新义务)。
M-5 与 m-1 是 R1 未闭合的旧缺口的延伸, 不计入。

**这个数高于任务给的 50% 门槛, 也高于 B 侧 R4 的 71%** —— 但**三项并列后它与 B 侧的数不可直接比**:
总体不同 (单席 8 条 vs 五席去重后 ~13), 范围不同 (post_spec R2 vs post_planning R4), 计数法不同
(我按单条 finding 计, B 侧那组按去重后 Major 计)。可比的只有一个定性观察: **每件新手段都造出新表面**
(memory `marginal-return-negative`) —— 4 条新 SC 造出 3 条新 finding, 1 处新正面规定 (cwd) **没有**造出 finding
(它是本轮唯一经得起对抗核验的新增面)。
是否据此收敛/停轮由汇总席判定, 单席无权。
