---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T14:31:09.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — knowledge-manager 席位报告

**被审对象**: `openspec/changes/premerge-gate-branch-existence/proposal.md` (Spec A, Level 2)
**审视角度**: Rule #5/#6/#9/#10 合规 · Level 2 判据 · 非目标与 B 侧划界一致 · follow-up 可证伪
**基线**: 主仓 HEAD, `aria` 子模块 `af87caeeed88af6af76f29a8002badbe1228d927` (Spec 声称的行锚基线)
**投票**: REVISE · **verdict**: FAIL (2 Critical + 2 Major + 1 minor)

---

## 0. 先说结论

拆分决策本身 (DEC-20260812-001) 有充分数据支撑, A 的每条行锚 / 逐字引用 / 三次受控实验结论我逐条回源均命中, 执笔质量明显高于 B 侧此前四轮。**但有两条 Critical 落在「组合是新的」这个接缝上** —— 一条是 A 自己的 Rule #6 定档站不住脚 (我的本职角度), 一条是 A/DEC 共同的划界承重理据 ("存在性核验单独就关掉恒绿腿") 在真实执行路径上不成立。二者都不是从 B 侧搬运来的 finding, 而是拆分后新组合暴露出的问题。

发现另一份同轮报告 `post_spec-R1-0-premerge-gate-branch-existence-tech-lead.md` 已独立命中了这两点 (其 C-1 / M-1) —— 我是在读取该文件前已通过自己的独立验证得出这两点结论, 下文按我自己的证据链重新给出, 并补充两条它未覆盖的角度 (Level 2 判据的自相矛盾细节、CLI 接线覆盖缺口的独立复核)。这属于多席收敛而非重复劳动。

---

## 1. 我实际跑过的命令 (证据链)

```bash
# 六键 schema 与调用面
grep -n "def _build_output" -A 30 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
grep -c "gate_check(" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py         # 24
grep -n "gate_check(" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py | grep -c "main_branch="   # 0
grep -rn "gate_check(" aria/ --include='*.py' | grep -v /tests/    # :298 (def) + :435 (main() 内唯一生产调用)
grep -n "main(argv" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py           # 零命中 ⇒ CLI 入口零覆盖

# Rule #6 SOT 逐字核对
grep -n '' standards/conventions/skill-benchmark-exemption.md | sed -n '20,40p'

# SKILL.md 实际执行流程 (AI 照做的那份)
grep -n '' aria/skills/phase-c-integrator/SKILL.md | sed -n '160,175p;238,250p;260,280p'

# 本仓活体验证 — "main" 恒绿腿今天在哪
git ls-remote --heads origin main        # RC=0, 零行
cd aria && git ls-remote --heads origin main   # RC=0, 零行 (子模块同样复现)

# SC 号段冲突核查
grep -n 'SC[-_ ]\?[0-9]\|sc22' aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py aria/skills/phase-c-integrator/tests/test_path_coverage.py
# 结果: SC-1..SC-28 裸数字段, 无 "SC-A*" 命中 ⇒ 与 A 的 SC-A* 前缀零冲突

# Level 2 判据交叉核对
grep -n '发布同步面' CLAUDE.md    # :81 "aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README"
grep -n '发版同步面' openspec/changes/premerge-gate-branch-existence/proposal.md   # :39 (非目标外)· :229 (§Impact)
```

行锚逐个实读 (全部命中, 与 A 文一致): `pre_merge_gate.py` `:328/:338/:344/:345/:356/:357/:358/:366`; `SKILL.md` `:255/:259/:260/:267/:279`; `SKILL.md:243` (执行流程步骤 3, 逐字硬编码分支名 `main`); Rule #6 SOT `:26/:33`。

---

## 2. Findings

### C-1 [Critical] Rule #6 substitute 不满足 SOT 的 "baseline-failing" 定义 — 三条被点名的 SC 对 `SKILL.md` 那两处改动零敏感度

**locator**: `proposal.md:191-201` (§Rule #6) × `standards/conventions/skill-benchmark-exemption.md:26` (第一行处置逐字 "SC 级 **baseline-failing** 单元/集成测试, 必须在场") × `proposal.md:171-187` (SC-A6/A13/A-zero 定义)

**evidence**:

1. SOT `:26` 第一行 (描述性) 的处置逐字是 "deterministic substitute: 以结构化测试 (SC 级 **baseline-failing** 单元/集成测试, 必须在场) 替代 AB"。"baseline-failing" 的可操作含义 (与 SOT §3 第 2 条 "把改动回退, 该 fixture 必须转红" 一致) 是: 该测试对**被替代的那处具体改动**必须具备回归检测力。
2. A `:196-197` 逐字点名 "本 Spec 的 SC-A6 / A13 / A-zero 即是" 那个 substitute, 而它要替代的是 `:194` 列出的两处 `SKILL.md` 改动 (`:267` schema 增 `gate_error` 键 / `:279` 四类早退注记同步)。
3. 我逐条读了 SC-A6 / SC-A13 / SC-A-zero 的断言列 (`proposal.md:173-175`): 三条全部只断言 `gate_check()` 的**返回 dict** (`verdict` / `kind` / `raw_message` 内容), **没有任何一条读取或 grep `SKILL.md` 文件**。
4. **可证伪推演**: 若单独回退 `SKILL.md` 的 `:267`/`:279` 两处 hunk (保留 `.py` 全部改动), SC-A6/A13/A-zero 断言的对象 (`gate_check()` 返回值) 不受影响 ⇒ 三条**依然全绿**。

⇒ substitute 机制要求的是 "回退被替代的改动, fixture 必须转红" —— 这里回退了被替代的改动, fixture **不转红**。三条 SC 是对 `.py` 改动的 baseline-failing 测试, 不是对 `SKILL.md` 那两处 hunk 的。

**旁证 (先例反向)**: A `:125` 自引 "`gate_error` 是 additive 可选结构化副本 (沿用 v1.65.0 `path_coverage` 先例)"。`aria/CHANGELOG.md` v1.65.0 段实读记载该同形改动 (往 `gate_check` 中插新步 + 加 additive 输出键 + 同步 schema/早退注记) **走的是 Rule #6 第二行 (照跑 AB)**, 且落地在 `SKILL.md:242` 留下了一条新执行流程步骤 (`2.5. Path coverage 评估`)。A 自引的先例本身就没有走它现在主张的这一行。

**how_it_goes_red**: 在 Phase B 落地分支上单独回退 `SKILL.md` 的 `:267`/`:279` 两处 hunk, 保留全部 `.py`/测试改动, 跑 `pytest -k "sc_a6 or sc_a13 or sc_a_zero"` —— 预期全绿即证实本 finding; 若要让它转红, 三条 SC 至少要有一条改为断言 "SKILL.md Output schema 块所列键集合 == `_build_output` 实产键集 ∪ {gate_error}" 这类 doc-code 一致性测试。

**blocks_phase_b**: **true** — `rule6_note` 直接决定 A.2 是否要给 `SKILL.md` 那两处改动排 Rule #6 AB 任务。

---

### C-2 [Critical] "存在性核验单独就关掉恒绿腿" 在 `gate_check()` 层成立, 在 AI 实际执行的 C.2.4 流程层不成立

**locator**: `proposal.md:27-35` (§本 Spec 的范围判定, DEC §3 同句) × `proposal.md:222-229` (§Impact, SKILL.md 改动逐字只列 "仅描述性: `:267` schema / `:279` 注记") × `aria/skills/phase-c-integrator/SKILL.md:167-168` 与 `:243-244` (§C.2.4 执行流程 步骤 3/4, 与"步骤执行"节重复的同款裸命令)

**evidence**:

1. `SKILL.md:243` 逐字: `` 3. **Query main in-flight**: `aether ci status --branch main --in-flight --json` → parse `data.runs[]` `` —— 分支名 `main` 是硬编码字面量, 且这是 **"执行流程" 编号步骤**本体 (`:238` "**执行流程**:" 标题下第 3 步), 不是注释或折叠块内容。`:167-168` ("步骤执行" 节) 是同款命令的重复出现。
2. 我实读了 A 的 §Impact 改动清单 (`:222-229`): 对 `SKILL.md` 唯一列出的改动是 "**仅描述性**: `:267` schema 增 `gate_error` · `:279` 四类早退注记同步"。`:243`/`:167` 不在这份清单内 ⇒ A 落地后这两行原封不动。
3. **本仓活体验证** (我独立跑了这条命令, 非引用): `git ls-remote --heads origin main` 在主仓与 `aria` 子模块**均返回 RC=0 + 零行输出**。这正是 §症状描述的场景 —— 若 AI 依 `:243` 字面执行 `aether ci status --branch main --in-flight --json`, 拿到的是 `runs:[]`, RC=0, 与 "无 in-flight" 完全同形。
4. A 新增的分支存在性核验完全长在 `gate_check()`/`pre_merge_gate.py` 内部, 而 `:243` 这条 AI 实际会读、会执行的散文命令**不经过** `gate_check()`。`workflow-runner/SKILL.md` 对 gate 的表述是 "re-invoke: phase-c-integrator C.2.4" —— 交回的是 `SKILL.md` 散文流程本身, 不是指名调用 `pre_merge_gate.py`。

⇒ A 修复的是 `gate_check()` 这个函数自身的行为 (单测可见、可证伪), 但 §症状描述的、也是 #137 报的那个"恒绿腿"其**执行形态**是 `:243`/`:167` 的裸命令, A 完全不碰它。DEC §3 的推理引用了 B 的 §症状 (后端不可区分性), 但没有引用 B 紧邻的 §根因 ("同一算法两份实现, AI 走没被加固的那份")——这个限定条件没有随 §症状 一起传给 A。

**how_it_goes_red**: A ship 后, 建两条对照 fixture —— "按 SKILL.md 散文路径执行 C.2.4 步骤 3" (即字面跑 `aether ci status --branch main --in-flight --json`) 得 `runs:[]` RC=0, 无从得知 fail; "按 `gate_check()` 路径执行" 得 `verdict=fail`+`kind=main-branch-not-found`。两者行为不一致本身就是可证伪形态; 更直接的红: 在本仓上, 按 `:243` 字面执行一次, 观察不到任何 "main-branch-not-found" 信号。

**为什么这条 Critical 落在 A 的范围而非 B**: 被审的是 A/DEC §3 **自己的**承重判断句 "存在性核验单独就足以关掉恒绿腿" —— 这是 A 用来论证自己可以独立以 MINOR 交付、不需要等 B 的核心依据, 不是把 B 的 finding 挪过来。若这句不成立, A "只做这一件事" 的自足性论证本身就有缺口, 需要 A 自己补一条残余暴露声明, 不能指望 B 去补。

**blocks_phase_b**: **true** — 改变 A 的 "完成即关闭 #137" 这个隐含收尾判据; B 侧抬头逐字 "本侧当前不具备进 Phase B 的条件" ⇒ D1 何时落地无期限, 若 A ship 后被当作 #137 已闭环, 是 paper fix (memory `feedback_paper_fix_antipattern` / `feedback_completion_signals_vs_runtime_invocation` 同形)。

---

### M-1 [Major] Level 2 判据自相矛盾 — "无跨仓同步面" 被本文件自己的 §Impact 推翻, "无架构变更" 悬在未决 spike 上

**locator**: `proposal.md:6` (Level 2 依据逐字 "无架构变更, 无跨仓同步面, 无破坏性契约变更") × `proposal.md:10` (代码落点 `aria/` 子模块) × `proposal.md:229` (§Impact "发版同步面: MINOR, 走常规发版流程") × `proposal.md:227` (`ci_backends/aether.py` "条件性" 入 scope) × `CLAUDE.md:81` (发布同步面定义)

**evidence**:

1. `CLAUDE.md:81` 逐字定义 "发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README"。A 的代码落点是 `aria/` 子模块 (`:10`), Spec 落主仓 —— 按此定义, 任何要真正发版的 aria 子模块改动**结构上就是跨仓同步动作** (子模块内 bump 版本文件 + 主仓 bump gitlink/VERSION/badge)。
2. A `:6` 却写 "无跨仓同步面", `:229` 又自己承认 "发版同步面: MINOR, **走常规发版流程**" —— 同一份文档里一处说没有, 一处说走流程, 且因 Level 定为 2 (proposal only, 无 `tasks.md`), 这份 "常规发版流程" 清单 (5 文件 + gitlink + VERSION + badge + i18n) 没有任何机械承载物。姊妹 Spec B 的 R4 三条 Critical 之一 (`TASK-017` 漏 gitlink) 正是这类清单在 `tasks.md` 里都会漏项; A 把清单压缩成一句话, 机械可验性比 B 更低。
3. `:227` 逐字 "`ci_backends/aether.py` | **条件性** —— 仅当 spike 判定须抽取共享重试 helper 时入 scope"。我实读 `aether.py`: `_run_with_retry` 定义于 `:164`, 唯一调用者是同文件 `:199` 的 `AetherBackend._query`; `grep -c '_run_with_retry' tests/test_ci_backends.py` = 0 (全 `tests/` 同样 0)。若 Phase B spike 判定需要抽取, 这是一次跨 backend 抽象层、零既有测试保护的结构改动, 与 `:6` "无架构变更" 直接冲突 —— 而 Level 已经定死为 2, 没有 `tasks.md` 去承载这个分支风险。

**how_it_goes_red**: (a) A ship 后只改 `aria` 子模块而不同步 bump 主仓 gitlink/VERSION/README badge ⇒ `git submodule status` 与 root README badge 立即不一致, 且 custom check `m6-version-badge-match` 对 "gitlink 落后" 方向的检测能力已在 post_planning R3 被实证失明 —— 即 "不会发红" 本身就是本条的证据; (b) Phase B spike 若判 "抽取共享 helper", `git diff --stat` 会出现 `ci_backends/aether.py`, 与 `:6` 的 Level 2 判据直接冲突, 届时 A 已在 Phase B 中途, 需要回炉重定 Level。

**blocks_phase_b**: **true** — 需在 A.2 前二选一钉死: 要么在 §Impact 补全机械化的发版同步面清单 (哪怕只是一句 "本 change 走 CLAUDE.md §版本管理 标准 5 文件 + gitlink + VERSION + badge 流程, 无额外项"), 要么把 "无跨仓同步面" 这句从 Level 2 依据里删掉 (它不是真的); 并把 `aether.py` 的入 scope 状态在 A.2 前钉死为 "不动" (可复用 `path_coverage.py:78-96` 的私有 runner 形状), 避免 Level 判据悬在未决 spike 上。

---

### M-2 [Major] SC 集合覆盖缺口 — `--remote` 的 CLI 接线零 SC 覆盖, 12/12 可在漏接线情况下全绿

**locator**: `proposal.md:49-51` (§1 "/ CLI `--remote`") × `proposal.md:171-187` (12 条 SC) × `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:424-440` (`main()` 定义)

**evidence**:

1. 我独立核实了 `pre_merge_gate.py` 的生产调用面: `grep -rn "gate_check(" aria/ --include='*.py' | grep -v /tests/` 只命中两处 —— `:298` (定义) 与 `:435` (`main()` 函数体内的**唯一真实生产调用**: `output = gate_check(pr_branch=args.pr_branch, main_branch=args.main_branch, config=config)`)。`--remote` flag 若要生效, 必须在这里补一个 `remote=args.remote`。
2. `grep -n "main(argv" aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` **零命中** —— CLI 入口 `main()` 今天完全没有测试覆盖。
3. 我逐条过了 12 条 SC-A* 的断言主体: 全部经由 Python 层直接调 `gate.gate_check(...)`, 没有一条经过 `main(argv)`。

⇒ 一个只在 argparse 里加 `parser.add_argument("--remote", default="origin")` 却漏掉 `:435` 处 `remote=args.remote` 的实现, `--remote` 会静默变成 no-op (永远查 `origin`), 而 12 条 SC 依然全绿, 因为它们都不走 CLI 路径。

**次生小项** (同 finding 内, 不单独计分): §版本 `:234` "既有 24 处 `gate_check(` 调用零改动" 的口径遗漏了 `:435` 这第 25 处真实调用点 (不影响 MINOR 结论 —— 加带默认值的关键字参数对 25 处都零破坏 —— 但它恰好是 `--remote` 唯一需要真正落地改一行的位置, 被排除在读者视野外)。

**how_it_goes_red**: 补一条 `main(["--pr-branch", "x", "--remote", "<指向不存在 remote 的路径>"])` ⇒ 期望 `verdict=fail` + `kind=="main-branch-verify-failed"` 的 SC; 漏接线的实现在这条新 SC 下会转 fail (因为它仍查 `origin`, 若 `origin` 上 main 分支存在则得 green, 与期望的 fail 不符)。

**blocks_phase_b**: **true** — SC 集合自足性缺口, 直接影响 A.2 任务验收粒度。

---

### m-1 [minor] `verify-failed` 路径的 `raw_message` 内容无任何 SC 断言 — 可全绿但生产诊断为空

**locator**: `proposal.md:117-124` (§4, 逐字要求 raw_message "含分支名与 remote 名" 且 "明确区别于无 in-flight run") × SC 表 `SC-A7`/`SC-A8`/`SC-A14` (`proposal.md:176-177,182`)

**evidence**: §4 对 `raw_message` 提出的是**内容**要求, 但 `SC-A7`/`SC-A8`/`SC-A14` (即全部 "verify-failed" 分支的 SC) 逐条只断言 `kind` 字段, 不断言 `raw_message` 内容。而 `kind` 住在 `gate_error` 里, A `:137` 自陈实测 "`gate_error` 全仓零消费者" —— 生产上唯一能被 `SKILL.md:255` ("fail → BLOCK + 输出 verdict + **raw_message**") 输出的诊断就是 `raw_message`。只有 `SC-A6` 断言了 `raw_message` 内容, 且只覆盖 "not-found" 一条分支。

**how_it_goes_red**: 实现在 verify-failed 三个分支统一写 `raw_message=""`, `SC-A7/A8/A14` 依然全绿 (它们不检查该字段), 而无人值守场景下唯一可见的诊断通道是空串。补 `assert main_branch in raw_message and remote in raw_message` 于这三条 SC 即可让该实现转红。

**blocks_phase_b**: false

---

## 3. 明确不成立的怀疑 (我查过并排除, 避免下一轮重复劳动)

| 我怀疑的 | 实测 | 结论 |
|---|---|---|
| `SC-A*` 前缀与既有 `SC-N` / B 侧 `SC-M*` 号段冲突 | `grep` 全部三个测试文件, 既有裸数字段 `SC-1..SC-28`, B 侧 `SC-M*` 只存在于 B 的 proposal/tasks 文档、尚未落进任何测试文件 | ✅ 无冲突, A `:168-170` 的预防成立 |
| 六键 schema 会被新增 `gate_error` 破坏 | `_build_output` 实读: 固定六键 + `path_coverage` 条件加键 (v1.65.0 先例); 新增 `gate_error` 与之同构, 都是"仅当该路径被执行才在场"的 additive 键 | ✅ 纯 additive, 与既有 `path_coverage` 先例的**机制**一致 (虽然 §Rule #6 引用它作为**豁免**先例时不成立, 见 C-1) |
| 既有 24 处调用会因新增 `remote` 参数 TypeError | 24 处全部关键字调用 (`gate_check(pr_branch=..., ...)`), 且 `main()` 的唯一生产调用也是关键字调用; 只要 `remote` 带默认值且不改变已有形参顺序/名称, 不会破坏任何一处 | ✅ "零改动" 对调用点本身成立 (虽然口径少数了第 25 处, 见 M-2) |
| B 侧 detailed-tasks.yaml/tasks.md 里 TASK-003/004/005/007/008/009 尚未标 cancelled, 与 A 内容重复 | 确认属实 (`tasks.md` 内这些任务仍是活跃 `[ ]` 状态), 但 DEC §5 第 3 条已明确把这列为 "Phase A.1 待执行" 的已知待办, 非本轮意外发现, 且是 B 侧文档卫生问题而非 A 的缺陷 | 不计分 (已声明的 pending item, 非 A 的范围) |

---

## 4. 划界结论 (席位本职, 回答任务书给出的判据问题)

**「存在性核验单独就关掉了恒绿腿」这个声称成立吗?** —— **在 `gate_check()` 函数层成立, 在 AI 实际执行的 C.2.4 散文流程层不成立** (C-2)。这不是拆分决策错误 —— A 仍是必要且正确的第一个可独立交付的增量, 也是唯一能以 MINOR 交付的那一步 —— 但 A 的"完成"定义必须显式声明这条残余暴露 (`SKILL.md:243`/`:167` 散文路径在 B 落地前原样恒绿), 否则 ship + 据此关闭 #137 就是教科书式的 paper fix。

**Rule #6 定档对吗?** —— **不对** (C-1)。A 判第一行合理 (`:267`/`:279` 两处从性质上确实是 schema/字段勘正, 不涉 `description` 或指令流程), 但它挑选的 "substitute" 证据 (SC-A6/A13/A-zero) 对被替代的那两处改动没有回归检测力, 不满足 SOT `:26` "baseline-failing" 的定义性要求。这是可以在不改判档结论 (仍走第一行) 的前提下修复的 —— 只需新建一条真正读 `SKILL.md` 内容的 doc-code 一致性测试。

**非目标与 B 侧划界是否自洽?** —— 划界的**方向**是对的 (D1/D5/折叠块/24 处补参/v2.0 弃用面/发版同步面/Rule#6 AB 留 B 侧, §5 逐字), 但 §Impact 对 SKILL.md 改动范围的**刻画**与 M-1/C-2 揭示的现实有出入: A 需要在 A.2 阶段把 "本 Spec 不改 SKILL.md 执行流程" 这句话的后果 (C-2 的残余暴露) 写清楚, 而不是让读者以为 A 落地就闭环了症状。

---

## 5. 我这一轮没有做的事 (边界声明)

- 未继承 post_planning R4 的 3 条 Critical (全属 B 侧); 上文任一 finding 均不引用它们, 也未对 B 侧 `proposal.md`/`tasks.md`/`detailed-tasks.yaml` 提出任何 finding;
- 未改任何文件 (本报告除外), 未 `git commit`/`push`, 未调外部 API;
- `git ls-remote` 验证命令为只读查询, 未对本仓或子模块产生任何写操作;
- 未独立复核 12 条 SC 溯源表 (`proposal.md:245-262`) 的全部来源标注, 仅复核了与我 5 条 finding 直接相关的部分。
