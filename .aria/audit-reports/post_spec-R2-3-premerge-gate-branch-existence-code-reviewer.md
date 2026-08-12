---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T16:40:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — Spec A `premerge-gate-branch-existence` — 席位 code-reviewer

**视角**: 逐字核对 — 溯源表逐行回源 / `SC-A*` 号段无冲突 / 所有 file:line 属实 / 条款间自相矛盾。

**VOTE**: REVISE · **VERDICT**: PASS_WITH_WARNINGS (0C + 4M + 4m)

---

## 0. 我实跑/实读了什么 (命令原文)

```bash
# 基线 = aria 子模块 HEAD
git -C /home/dev/Aria/aria log --oneline -1        # af87cae (工作树 clean)

# file:line 逐行实读
sed -n '68p;116p;251p;298p;328p;338p;344p;345p;356p;357p;358p;366p;427p;435p' scripts/pre_merge_gate.py
sed -n '78p;81p;82p;83p;84p;91p;93p;105p' scripts/path_coverage.py
sed -n '167p;168p;242p;243p;244p;253p;255p;259p;260p;265p;275p;277p;279p' SKILL.md
sed -n '335p;336p;337p' ../workflow-runner/SKILL.md
sed -n '59,80p;301p;311p;321p;394p;524p;654p;675p;710p;718p;723p' tests/test_pre_merge_gate.py

# 计数
grep -c 'gate\.gate_check(' tests/test_pre_merge_gate.py                 # 24
grep -c 'gate\.gate_check(.*main_branch' tests/test_pre_merge_gate.py    # 0
grep -rn 'gate_check(' aria/ --include=*.py                              # 24 调用 + :298 def + :435 调用
grep -rn 'gate_error' aria/                                              # rc=1 (零命中)
grep -c '_run_with_retry' tests/test_ci_backends.py                      # 0
grep -rn "main(argv" tests/                                              # rc=1 (零命中)
grep -rhoiE 'sc[-_]?a?[0-9]+[a-z]?' tests/*.py | sort -u   # SC-1..SC-28 + sc20a/b, 无 SC-A*
python3 -m pytest tests/ -q                                              # 111 passed
python3 -m pytest tests/test_pre_merge_gate.py --collect-only -q | grep -c '::'   # 46 (25 / 40 同法)

# 受控裸仓复跑 (R1/主 loop 五条实证全部复现)
git ls-remote --heads $W/R1.git master              # refs/heads/wip/master, rc=0   (裸名尾段 glob)
git ls-remote --heads $W/R2.git 'refs/heads/mast*'  # 命中 refs/heads/master, rc=0  (锚定关不掉 glob)
git ls-remote --heads $W/R2.git 'refs/heads/m[a]ster' / 'refs/heads/maste?'  # 均命中, rc=0
git ls-remote --heads $W/R2.git develop            # 零行, rc=0
git ls-remote --exit-code --heads $W/R2.git develop # rc=2
git ls-remote --heads /tmp/does-not-exist-repo-xyz master  # rc=128
git ls-remote --heads origin main                  # 零行, rc=0 (本仓)

python3 -c "print(issubclass(UnicodeDecodeError, OSError))"   # False
python3 -c "import json; json.loads(<SKILL.md:265-277 块>)"    # INVALID JSON
python3 -c "from ci_backends.aether import AetherBackend; print(AetherBackend.probe(), AetherBackend().precheck())"
                                                    # True (True, '')  —— 本机 aether 在 /usr/local/bin/aether
```

---

## 1. R1 两条 Critical 的闭合判定 (逐条回源, 区分「写下来」与「闭合」)

### C-1 划界承重句 — **判定: 闭合**

R1 的 C-1 本身是一条**声称缺陷** (A 的完成定义写错了), 因此它的闭合形态**只能**是「更正后的声称 +
更正传播到所有承载该声称的文件」。我按后者核验, 三处**全部**落地:

| 落点 | 实读结果 |
|---|---|
| A `proposal.md:35-39` | 新增 `### 根因` 段, 逐字补引「同一算法有两份实现, 而 AI 走的是没被加固的那份」 |
| A `proposal.md:43,46-48` | 承重句加限定「`gate_check()` 这份实现里的」+ 明写「DEC §3 与本节上一版都只引了 §症状, 漏引了紧邻的 §根因」 |
| A `proposal.md:73-94` | 新增 §残余暴露整节, 逐字「A ship 不构成 aria-plugin #137 的闭环, 不得据 A ship 关闭 #137」 |
| B `proposal.md:13-21` | 「即关掉 #137 那条恒绿腿所需的**全部内容**」逐字作废 + 更正块 |
| `DEC-20260812-001.md:80-105` | owner 原文保留, 追加带日期的更正块 (不改写裁定) |

**它是不是 paper fix?** 我按 memory `feedback_paper_fix_antipattern` 的判据 (code+test+doc 三位一体) 检查:
本条缺陷**没有 code 面** —— 缺的不是一段实现, 是一句错的声称。A 还额外做了两件超出「写下来」的事:
(a) 给出**可现场复现的残余精确形态** (`:86-89`: 核验步用 `<MAIN_BRANCH>` 而步骤 3 硬编码 `main` ⇒
`main≠master` 的仓上按散文逐字执行 verdict 仍 green) —— 这句是可证伪的, 不是修辞;
(b) 明确**拒绝**为它编造 SC (`:91-94`), 理由是「断言缺陷仍在」的哨兵在 B 落地后必须被删 = landmine,
援引 memory `feedback_false_green_dual_is_permanent_red`。**拒绝编造一条恒红的量, 比编一条更接近闭合。**
⇒ 我判 **真闭合**, 不是「写下来」。

### C-2 Rule #6 改判第二行 — **判定: 闭合, 且改判本身正确**

我不采信 R1 aggregate 的行号 (它引 `:26`/`:33` 两处都错), 独立实读 SOT
`standards/conventions/skill-benchmark-exemption.md`:

- `:28` = 决策表第一行, 处置逐字「**deterministic substitute**: 以结构化测试 (SC 级 baseline-failing
  单元/集成测试, 必须在场) 替代 AB」 — A `:345` 的引用**正确**;
- `:31` = 决策表第四行「拿不准算不算处方性 / 算不算在范围内 | — | **照跑** (宁跑勿豁)」 — A `:343` 的引用**正确**;
- `:33` = SKILL.md 附加约束「仅当变动是**事实性同步** (溯源注释 / 行号勘正 / 术语修正) 且 frontmatter
  `description` 零变动, 才可能落进第一行 … `description` 或**指令流程变动 ⇒ 一律第二行**」 — A `:334`/`:341`
  的两处引用**逐字属实**。

**改判对不对 (独立判定)**: A `§Impact` ① 要求给 `SKILL.md §C.2.4` **执行流程新增编号步骤** ⇒ 落在
`:33` 的「指令流程变动」⇒ **一律第二行**。同形先例我实读复核: `SKILL.md:242` 确为 v1.65.0 新增的
「2.5. **Path coverage 评估**」编号步骤; `aria/CHANGELOG.md:174` 逐字「新步骤 2.5」、`:181` 逐字
「Rule #6 **照跑 AB** (3 eval × with/old/without 三臂」。⇒ 改判**成立**, 且 (a) 一条即足以定档,
(b)(c)(d) 是加固不是承重。三处互斥 (`:196`/`:201`/`:39` 旧行号) 确已消除。

---

## 2. 溯源表逐行回源 — **21/21 属实, 无一需要下调**

表已从 12 行扩到 **21 行** (`:453-473`, `grep -c '^| '` 实测)。我逐行回源:

| # | 事实 | 我的复核 |
|---|---|---|
| 1 | 插入点 5 逻辑锚位 / 8 行号 | ✅ `:328/:338/:344/:345/:356/:357/:358/:366` 八行逐行实读全中 |
| 2 | `SKILL.md:255` = `fail` surface 通道是 `raw_message` | ✅ 逐字 |
| 3 | `SKILL.md:279` = 四类早退保持六键 | ✅ 逐字 (enabled:false / no-backend / precheck / backend query) |
| 4 | `SKILL.md:259`/`:260` 重试与退出码 (含 `127 → no_ci_fallback`) | ✅ 逐字 |
| 5 | 锚定 pattern 仍 fail-OPEN | ✅ 受控裸仓复现三 pattern 全命中 rc=0 |
| 6 | `ls-remote` 零命中亦 rc=0 | ✅ 复现 |
| 7 | `--exit-code` 无命中返 rc=2 | ✅ 复现 |
| 8 | `test_sc22` patch 全局生效 + `:723` 未传 `main_branch` | ✅ `:718` `mock.patch.object(pc_module.subprocess,"run",…)` — `import subprocess` 模块对象共享, 确全局 |
| 9 | `gate_error` 零消费者 / workflow-runner 仅四条臂 | ✅ `grep -rn 'gate_error' aria/` rc=1; exit conditions 实读为 4 条 |
| 10 | `_run_with_retry` 硬绑 binary / 只捕 TimeoutExpired / 无 cwd / `text=True` | ✅ `:164-187` 逐行实读, docstring 自陈「other exceptions bubble up」 |
| 11 | `test_ci_backends.py` 25 tests 零命中 `_run_with_retry` | ✅ `grep -c` = 0 (全 `tests/` 亦 0) |
| 12 | 测试基线 111 passed | ✅ 实跑 `111 passed`; 46/25/40 分文件亦对 |
| 13 | `SKILL.md:243` 硬编码且是执行流程编号步骤本体 | ✅ 逐字 |
| 14 | 本仓 `ls-remote --heads origin main` 零行 + RC=0 | ✅ 复跑 |
| 15 | `workflow-runner` 全文零命中 `pre_merge_gate.py` | ✅ (但「唯一表述」一句不准, 见 m-4) |
| 16 | v1.65.0 同形先例: 照跑 AB + 补步骤 2.5 | ✅ CHANGELOG `:174`/`:181` + `SKILL.md:242` |
| 17 | `issubclass(UnicodeDecodeError, OSError)` = False | ✅ 我独立实跑 = False, MRO 与 A 写的一致 |
| 18 | 坏路径 remote ⇒ 确定性 rc=128 | ✅ 复现 |
| 19 | 24/24 既有调用不传 `main_branch` | ✅ 六处多行调用逐个实读; `:669` 的 `main_branch="main"` 是 `pc_eval.assert_called_once_with` 的断言参数, **不是** `gate_check` 调用 —— A 没数错 |
| 20 | `_ProbeCacheResetMixin:59-80` | ✅ `:59` class / `:80` `super().tearDown()`; docstring 逐字与 A 引的一致 |
| 21 | 真实调用点 25 (24 + `main():435`) | ✅ `:298` 是 def, `:435` 是调用; `base.py`/`github_actions.py` 的命中全在 docstring/注释, 非可执行调用 |

**`SC-A*` 号段无冲突**: 实跑 `grep -rhoiE 'sc[-_]?a?[0-9]+[a-z]?' tests/*.py` = `SC-1..SC-28` + `sc20a/sc20b`,
`grep -rniE 'sc[-_]a' tests/ scripts/ SKILL.md` **零命中** ⇒ **无冲突, 属实**。SC 表行数实测 **16**,
与 `:293` 的「16 条 = 上一版 12 + R1 新增 4」一致; 打桩边界表 6 档合计 **16/16 逐条覆盖**, 无遗漏无重复。

**执笔方对主 loop 的三条纠正 — 我的复核**:
1. `UnicodeDecodeError` 非 `OSError` 子类: **属实**, 我独立实跑 = False。处置 (§2 表显式点名 + §5 钉「不规定怎么补」+ SC-A14 参数化探针含「任取一个不在实现 `except` 元组里的异常类」) **够** —— 它把断言从「枚举」换成了「探针」, 正是 memory `redfix-change-quantity` 要求的「换量而不是调阈值」。
2. SC-A11 空真: **属实**, 但**修法只落了一半** ⇒ 见 M-2。
3. R1 aggregate 归属/去重错: **属实** —— aggregate `:67` 引 SOT `:26`、`:76` 引 `:33` 说「第四行」, 两处行号都错 (正确为 `:28` / `:31`); 6C 实为两簇各 3 条 (划界句: backend-architect / qa C-1 / km C-2; Rule #6: tech-lead / qa C-2 / km C-1), 非「4 条指向同一件事」。⇒ 本轮我全程以 journal 原始 findings 与 SOT 原文为准。

---

## 3. Findings

### Major

#### M-1 · §6「落地后这 24 处全部触达新核验」与 §3 的核验点定位 + SC-A10/A10b 直接矛盾; 实测至少 4 处结构上不触达
- **locator**: `proposal.md:274` (§6) × `:167`/`:185` (§3) × `:302-303` (SC-A10/A10b) × `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:301,311,321,524`
- **证据**: §3 逐字把核验点钉在「三个早退**之后**」。而实读:
  `:301` `gate.gate_check(pr_branch="feat/x", config={"enabled": False})` ⇒ 在 `pre_merge_gate.py:328` 返回;
  `:311` / `:321` 外层 `mock.patch.object(gate, "resolve_ci_backend", return_value=None)` ⇒ 在 `:338-339` 返回;
  `:524` (alias 测试) 同款 `return_value=None` ⇒ 亦在 `:339` 返回。**这 4 处全部在核验点之前退出。**
- **怎么会红**: 与实现无关 —— 任何遵守 §3 的实现下, `enabled=false` 与 no-backend 两条早退都**结构上**够不到核验;
  这正是 SC-A10 / SC-A10b 存在的理由 (「assert ls-remote 未被调用」)。「24/24 全部触达」与「这两类必须不触达」
  不可能同时为真。若 Phase B 照 §6 这个量设计 mixin 覆盖面与红窗预期, 会在这 4 处得到与 Spec 相反的实测。
- **introduced_by_r1fix**: **是** (整段 §6:271-275 为 R1-fix 新写)

#### M-2 · §6 的「绕过 mixin」名单漏了 SC-A11 —— 与打桩边界表逐字冲突, 照 §6 实现会重新造出执笔方本轮刚修掉的那个空真
- **locator**: `proposal.md:283` vs `:305` / `:318`
- **证据**: `:283` 逐字「同时保证 **SC-A6 / SC-A13 / SC-A-zero / SC-A-cwd / SC-A-cli** 能绕过该 mixin 用真实 git
  受控裸仓」—— **SC-A11 不在名单内**。而 `:318` 打桩边界表把 SC-A11 放进「⛔ 不得打桩」档, 并逐字警告
  「若把核验入口打桩, 本条就不再验『核验放行了一个真实存在的分支』, **退化为恒真**」; `:305` 亦逐字
  「本条**不得打桩核验入口** —— 打了就退化为恒真」。
- **怎么会红**: Phase B 若按 §6 的名单建接缝 (那是 §6 明文规定的「分层, 不是 spike 的自由度」), SC-A11 仍留在
  mixin 下 ⇒ 核验入口被打桩 ⇒ 一个**恒判 `not-found`** 的坏实现在 SC-A11 上照样绿 (核验根本没跑) ⇒ 恒真。
  这与 memory `fix-the-class` 同形: 认出了类 (SC-A11 的空真), 只修了它在一处的实例 (打桩边界表), 没同步到
  它在另一处的实例 (§6 名单)。
- **introduced_by_r1fix**: **是** (v0 的 §6 只写「保证 SC-A6/SC-A13 能用真实 git 受控裸仓」, SC-A11 的
  ⛔ 档位与恒真警告都是 R1-fix 新增 —— 新增了警告却没同步扩名单)

#### M-3 · §4「第五类早退注记的一致性由 SC-A-doc 机械钉住」是失效的委派 —— SC-A-doc 对该注记双向失明
- **locator**: `proposal.md:239-241` (§4) × `:310` (SC-A-doc) × `:389` (§Impact ③) × `SKILL.md:265-277` vs `:279`
- **证据**: SC-A-doc 的断言逐字是「从 `SKILL.md` §C.2.4 **Output schema json 块**实际解析出的**键名集合**
  == `_build_output` 的实产键**全集**」。而 §4 要它钉的那件事住在 **`:279` 的散文归纳句**里
  (实读 `:279`: 「…各早退分支 (no-backend / precheck 失败 / backend query 失败 / enabled:false) 保持六键不变」),
  该句**不在 json 块内** (json 块是 `:265-277`), 且它断言的是**某一条路径的键集**而非全集。
- **怎么会红**: 两个方向都碰不到 ——
  (a) 一个只改了 json 块、把 `:279` 原样留作**四类**的实现: SC-A-doc **全绿** (它一个字节都不读 `:279`);
  (b) 一个在核验失败路径上**也**塞了 `path_coverage` 的实现 (直接违反 §4 逐字「**无** `path_coverage`」):
  键的**并集不变** ⇒ SC-A-doc **仍全绿**。
  ⇒ §Impact ③ 是 A 必交付的三处 `SKILL.md` hunk 之一, 却**实际零机械锚**, 而 Spec 声称它有。
  形状同 memory `delegate-verify` (写「由 X 保证」前必去 X 核「它真做这件事吗」)。
- **introduced_by_r1fix**: **是** (§4:239-241 与 SC-A-doc 均为 R1-fix 新增)

#### M-4 · 「⛔ 不得打桩」这一档的 6 条 SC 都要先过 backend 解析 + precheck 两道早退才够得着核验, 该可达前提 Spec 全文未声明; 无 CI backend 的环境下与实现无关地恒红
- **locator**: `proposal.md:318` (打桩边界 ⛔ 档) × `:167`/`:185` (§3 核验点) × `:297` (SC-A6 逐字「用真实 `ls-remote`, 不打桩」) × `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:338-339,344-352`
- **证据**: 实读 `gate_check`: `:338` `backend is None` ⇒ `:339` `return _no_ci_output(...)`;
  `:344-345` precheck 失败 ⇒ `:346` return。**两道都在 §3 钉的核验点之前**。本机实测
  `AetherBackend.probe()=True` / `precheck()=(True,'')` (aether 在 `/usr/local/bin/aether`) ⇒ 今天恰好过得去;
  但这是**环境事实, 不是 Spec 保证**。
- **怎么会红**: 在任何没有可用 CI backend 的执行环境 (典型: 干净 CI runner, 无 `aether` 无 `gh`),
  `resolve_ci_backend` 返 `None` ⇒ `_no_ci_output` 走默认 `skip_with_warning` ⇒ `verdict=green` ⇒
  **承重的 SC-A6 期望 `fail`+`not-found` 必红, 且与被测实现无关** = 恒红 = 零信息
  (memory `feedback_false_green_dual_is_permanent_red`)。同表 SC-A11 的行内又自带「+ **mock backend** 提供
  in-flight runs」⇒ 「⛔ 不得打桩」这个档位标签与它自己的成员要求当场冲突。
- **处方**: 档位标签改写为「⛔ 不得打桩**核验入口 / `ls-remote`**」, 并在 §6 或该表补一句可达前提
  (「这 6 条须先使 backend 解析成功且 precheck 通过 —— 既有 24 处调用一律 `mock.patch.object(gate, "resolve_ci_backend", …)`, 沿用即可」)。
- **introduced_by_r1fix**: **否** —— ⛔ 档在 v0 已对 SC-A6/A13/A-zero 成立, R1 五席无人命中; R1-fix 只是把成员从 3 扩到 6。

### Minor

#### m-1 · `workflow-runner/SKILL.md:337` 行锚错 —— 该行是空行, 被逐字引用的 exit condition 3 在 `:335`
- **locator**: `proposal.md:160` × `aria/skills/workflow-runner/SKILL.md:335,337`
- **证据**: `sed -n '335p;336p;337p'` ⇒ `:335` = `3. **verdict=fail** → 转为 stop (fatal)`; `:336` = `4. **verdict=green** …`;
  `:337` = **空行**。A `:160` 逐字写「`workflow-runner/SKILL.md:337` 逐字 exit condition 3」。
- **怎么会红**: 任何按 `:337` 去回源的复核者读到空行 ⇒ 无法验证该承重权衡的依据。内容本身属实, 只有锚错。
  (该错误由 R1 tech-lead 的 minor finding 原样继承, 属 memory `reporter-miscite` 形状。)
- **introduced_by_r1fix**: **是** (v0 无 `:337` 引用)

#### m-2 · Rule #6 (c) 给的证伪实验命令在落地分支上是 no-op
- **locator**: `proposal.md:348`
- **证据**: 逐字「在落地分支上单独 `git checkout HEAD -- .../SKILL.md` 回退 `SKILL.md` 侧**全部** hunk」——
  落地分支上该 hunk 已在 HEAD 里, `git checkout HEAD -- <file>` 恢复的正是**已改**的版本 ⇒ 不构成回退。
  要复现 baseline-failing 须 `git checkout <base-sha> -- <file>`。
- **怎么会红**: 有人照此命令复跑, 会得到「三条仍全绿」但**原因是文件根本没被回退**, 从而误以为验证了 (c);
  真结论 (三条确实恒绿) 需要正确的基线 checkout 才成立。定档结论不受影响 —— (a) 一条已足以定第二行。
- **introduced_by_r1fix**: **是**

#### m-3 · SC-A-doc 的「实际解析 json 块」不可按字面实施: 该块不是合法 JSON, 且含两层嵌套键
- **locator**: `proposal.md:310` × `aria/skills/phase-c-integrator/SKILL.md:265-277`
- **证据**: 实跑 `json.loads` 该块 ⇒ `Expecting ',' delimiter: line 2 column 22` (因 `"verdict": "green" | "wait" | "fail"`
  是 schema 伪 JSON)。块内另含 `in_flight_runs` 的 `run_id/branch/started_at/elapsed_seconds` 与 `path_coverage` 的
  `decision/workflows_scanned/matched_workflows/changed_files_count/reason` 共 9 个**嵌套**键。
- **怎么会红**: 用 `json.loads` 的实现 ⇒ 抛异常, 与被测实现无关地红; 用朴素 `"key":` 正则的实现 ⇒ 取到 16 键,
  与 code 侧 8 键永不相等 ⇒ 恒红。SC 的「今日实测 doc 侧 7 键」只有在**仅取顶层键**的解析下才成立, 而 Spec
  既禁止硬编码 doc 侧、又未规定这条解析约束 ⇒ 欠定 (memory `spec-underdetermination`)。补一句「仅顶层键」即可闭合。
- **introduced_by_r1fix**: **是** (SC-A-doc 为 R1-fix 新增)

#### m-4 · §残余暴露表第三行的「唯一表述是 `:329`/`:351`」不准确
- **locator**: `proposal.md:84` × `aria/skills/workflow-runner/SKILL.md:342,373` × `workflow-runner/scripts/gate_state_helper.py:37`
- **证据**: `grep -rn "pre_merge_gate" workflow-runner/` 得 3 处: `SKILL.md:342`「读 .aria/config.json 加载
  `phase_c_integrator.pre_merge_gate.*` 配置」· `SKILL.md:373` (`poll_chunk_seconds`) · `gate_state_helper.py:37`。
  A 的 grep 目标带 `.py` 后缀, 那一串确为**零命中**, 但「唯一表述」这四个字被上述 `:342` 证伪。
- **怎么会红**: 承重结论 (编排层不直调 helper 脚本, 把执行交回散文流程) **不受影响** —— 那 3 处都只读配置键,
  无一是 helper 调用。仅是措辞过强。
- **introduced_by_r1fix**: **是** (§残余暴露整节为 R1-fix 新增)

---

## 4. 我**没有**报的 (逐条说明为什么不报)

- **B 侧 R4 的 3 条 Critical** (TASK-017 gitlink 求值时点 / `config.template.json` 键名面 / `CLAUDE.md:113` 同步):
  逐条核过是否污染 A —— gitlink 那条 **A 已自曝**并升 owner 裁量 (`:394-400`, 且明写「⛔ 不得以 Level 低自行降级」,
  合规则 #10); `config.template.json` 那条**结构性不成立** (`--remote` 是带默认值的 CLI 参数, 实读
  `.aria/config.template.json:73-88` 的 `pre_merge_gate` 块无对应键, A 不新增 config 键); `CLAUDE.md:113` 逐字
  只描述 gate 的**两条 verdict 腿** (PR CI passing / main 无 in-flight), A 加的是 verdict 之前的 fail-closed
  前置核验, 不改那两条腿的表述 ⇒ 不构成 Rule #3 失同步。**三条都不落在 A 的范围内。**
- **`gate_check` 未被生产路径调用** (R1 backend-architect / qa 的 C): 已由 §残余暴露闭合, 见 §1。
- **SC-A10/A10b/A10c 写「assert ls-remote 未被调用」而观测点其实是 mixin 的桩**: 打桩边界表该档的括注
  「(断言"未被调用", 需可观测的打桩点)」已消歧, 不重复计一条。
- **§3 代码块 `:358` 那行把三行调用压成一行**: 该块是节选展示, 行号本身 8/8 实读命中, 不构成缺陷。

---

## 5. 评估

**是否可以继续?** 需要修复 (4 条 Major), 但**不阻断本 Spec 的方向**。

R1 的 2C + ~10M 我逐条回源, **实质全部闭合**, 且闭合方式经得起对抗检查 (跨三文件传播 / 拒绝编造恒红哨兵 /
改判有 SOT 逐字与同形先例双支撑 / SC 从 12 扩到 16 且打桩边界 16/16 逐条覆盖 / 21 行溯源表 21/21 属实)。
新缺陷集中在 R1-fix **新写的那几段**上 —— 4 条 Major 里 3 条由 R1-fix 引入 (75%), 高于 50% 的拆分收益门槛;
但严重度已从 2C 降到 0C, 且这 3 条都是**同一形状**: 「在一处认出了类, 只把修法落到了那一处」
(M-2 = SC-A11 的空真只修了打桩表没修 §6 名单; M-3 = 声称有锚而锚不在那; M-1 = 新写的量与既有 SC 的前提对撞)。
⇒ 下一轮 fix 建议**先做一次条款间交叉一致性扫描** (memory `fixes-contradict`), 而不是继续加新条款。
