---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:20:00.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — handoff-multibranch-subdir-path-fidelity (Round 5)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文**逐字**落盘于同目录 `…-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager); 五份 frontmatter 15 字段齐全 (机械核验: 逐文件 awk 抽 frontmatter 后计 `^[a-z_]+:` = 15/15/15/15/15), **0 份需补齐**。缺席 0, `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (本轮实际执行; 第 1-8 条与 R1 / R2 / R3 / R4 聚合报告同规则, 第 9 条为本轮新增, 供后续复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取各席**报告值**的最高者。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (不是同一缺陷的不同 severity, 而是结论相反) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。本轮 `conflicted` = **0** —— 逐条比对未发现「一席说成立、另一席说不成立」的对立结论。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 / 同一 Task。本轮实例四处: (a) `c9728601`(§3 basename 硬口径无 SC 可证伪) 与 `d3227a59`(同一上报面的语义后果未登记进 Task 5.3 / schema) 都锚在 `scan.py:193/:209`, 但主张与修法不同 (前者补断言, 后者补登记), 保留两条; (b) `079dcc71`(`degraded_reason` 在 banner / skipped 两支的键存在性未定义) 与 `2a7110db`(三值枚举里 `missing_filename` 无 SC) 都锚在 §2.5 / SC-15, 前者是契约面、后者是判据面, 保留两条; (c) `1efc6e5d`(新 kind 只进 soft_error 单通道) 与 `c39306e1`(SC-9 的 monkeypatch 面须按命令分派) 都锚在 SC-9, 一为上报通道、一为夹具构造, 保留两条; (d) `220a2393`(Task 5.1 表**机械兜底列**引的 `.aria/state-checks.yaml` 三处行号漂移) 与 decision `8e906135`(同表**16 个版本点**行号今日仍逐处命中) 锚在同一张表的两列, 对象不同 ⇒ **非矛盾**, 保留两条并互相注明。
5. 席位**报告正文有、结构化清单未列**的条目**不计入** `found_by`, 但在相应条目内注明, 以免信号丢失。本轮共 3 处: backend-architect 报告正文的 11 条 decision 与「本轮机械核验清单」17 项、knowledge-manager 报告正文的 6 条 decision 与 3 条 risk (终轮预算 / 同源性 / 触点集定义缺失) 中未进其结构化清单的 2 条、qa-engineer 报告正文的「附录 A 实跑清单」8 项 —— 已分别归并入 `57fbaada` / `9c794f72` / `b28a77a6` / `31042495` 与 Verdict 节内注明。
6. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, 用 python3 实算 (29 条全部唯一, **0 碰撞**)。scope 归一为小写写法后入哈希与 keys。
7. 本轮去重前 **46** 条 (tech-lead 8 / backend-architect 4 / qa-engineer 13 / code-reviewer 14 / knowledge-manager 7), 去重后 **29** 条。
8. severity 计数**不含** decision 类 (与 R1 / R2 / R3 / R4 同口径)。
9. **(本轮新增) 复合条目拆分**: 一个 bullet 内点名两个语义不同的缺陷时, 按其点名的每个缺陷分别计入相应条目的 `found_by`, 并在条目内注明来源 bullet。本轮实例 2 条: tech-lead 首条 (`:16` 行号断言 + Task 5.2 gitlink 起点) 分别进 `dbdd80e9` 与 `a5bd18e1`; code-reviewer 第 5 条 (Phase B/C 起点 + 待复议 6 版本号) 分别进 `a5bd18e1` 与 `f8eef4d2`。故 46 条原始条目 = 48 项缺陷/结论主张。

---

## 审计结论

### Critical (0)

本轮**无 critical** —— 五席自报 critical 均为 0; R4 唯一的 critical `5c28d58f` 经三席 (tech-lead / backend-architect 报告正文 / code-reviewer 独立复跑) 复核确认已在正文闭合 (见 decision `57fbaada` / `1e2c89f4`)。

### Major (9)

- `dbdd80e9` [major] documentation/`proposal.md:16` 头部 2026-09-10 基线复核块 (「全部行号继续有效」断言) — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5)**, `conflicted: false`
  该块由「本 spec 触点文件在 `301641b..f314785` 零 diff」推出「本文**全部行号**在 `f314785` 上继续有效, 基线冻结不需重取」。四席各自实测 `git -C aria diff 301641b f314785` = **21 文件 / 895 增 / 63 删**, 其中至少三个被本文逐行引用: (1) `skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py` +99 行 (code-reviewer 记 +82/-17) —— 它正是 SC-3 / SC-4 / SC-13 逐处引用的 `_GIT_ENV` 夹具模板与 SC-10 点名 9 模块之一: `_GIT_ENV` `:174-183`→`:176-185` (knowledge-manager 记 `:176-184`), `GIT_CONFIG_GLOBAL/SYSTEM` `:181-182`→`:183-184`, 名/邮箱 `:176-179`→`:179-182`, 日历夹具 `:380-382`→`:382-384`, 调用点 `:386`→`:388`; (2) `aria/CHANGELOG.md` +25 行, v1.70.0 先例 `:84`→`:109`、Added 先例 `:93-97`→`:118-122`、Amended 先例 `:99-100`→`:124-125` —— 而这三处正是 §6.5 与 SC-11(e) 的成文口径依据 (code-reviewer / knowledge-manager); (3) `skills/phase-d-closer/SKILL.md` 两处改写 (其 `:218` 经三席复核**未移位**, 该引用仍成立)。knowledge-manager 另指: 该块自己抄对了总量 (21 / 895 / 63), 说明 diff 确实跑过, 漏检出在**按文件过滤时用的「触点集」**。⇒ 「触点零 diff」只支撑「触点行号有效」, 不支撑全文; 而这句话是给复审者与实施者的**免检许可**。
  *severity / category 分歧注*: qa-engineer 报 minor, 另三席报 major ⇒ 按规则 1 取最高 major; tech-lead 标 architecture, 另三席标 documentation ⇒ 取多数 documentation。
  *规则 9 注*: tech-lead 的来源 bullet 同时点名 Task 5.2 的 gitlink 起点, 该半进 `a5bd18e1`。

- `a5bd18e1` [major] architecture/Phase B/C 起点与 gitlink bump 基线 (`proposal.md:9` / `:10` / Task 5.2 `:313`) — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5)**, `conflicted: false`
  四席各自实测主仓 `git ls-tree HEAD aria` = **`f314785`** (= v1.73.0; qa-engineer 另记主仓 HEAD `fe703c5`、经 merge `c115fd4`; tech-lead 记 bump 提交 `c02b0ef`), 而 `:9` 仍写「Phase B 在 `301641b` 起分支」、`:10` 仍写「gitlink bump 起点是 `301641b`, 任何情况下不得回退到 `0545f86`」、Task 5.2 `:313` 仍写「gitlink bump **从 `301641b` 前进** (实测起点)」。⇒ (a) 「实测起点」这个限定词今日为假; (b) 照字面执行即把主仓 gitlink **回退一代 (v1.73.0 → v1.71.1)**, 而唯一成文的回退禁令只点名 `0545f86`, `f314785 → 301641b` 这一代**无任何护栏**; (c) `:16` 虽自陈「主仓 gitlink 已随之前进」, 却未在这三处加任何 inline neutralize 标记。三席同指其归属: CLAUDE.md §多远程推送两条硬约束与 Aria #165 三次复发的同族形态 (knowledge-manager 另接 memory `feedback_sequenced_multirepo_gitlink_bump`), 且它落在 **Phase C 的可执行指令行**上。
  *category / type 分歧注*: tech-lead 与 knowledge-manager 标 architecture、qa-engineer 与 code-reviewer 标 implementation ⇒ 2:2 平票, 按规则 2 取席位序在先者 = architecture; knowledge-manager 标 type=risk, 另三席 issue ⇒ 取多数 issue。
  *规则 9 注*: tech-lead 与 code-reviewer 的来源 bullet 均为复合条目 (另半分别进 `dbdd80e9` 与 `f8eef4d2`)。

- `f8eef4d2` [major] documentation/待 owner 复议 6 的版本候选号 (`proposal.md:378-386` / Task 2.0b / Task 5.1) — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5)**, `conflicted: false`
  待复议 6 逐字写「`git -C aria tag --list 'v1.7*'` 最高为 `v1.71.1`, 两个候选号 (`v1.71.2` / `v1.72.0`) 当前均未被占用」并把**推荐默认**定为 MINOR / `v1.72.0`。四席实测 tag 集 = `v1.70.0 / v1.71.0 / v1.71.1 / **v1.73.0**` (tech-lead 另经 `git ls-remote --tags origin` 取到 `refs/tags/v1.73.0^{} = 6726df1`), `aria/.claude-plugin/plugin.json:4` = `"1.73.0"` ⇒ 两个候选号**都低于当前版本**, SemVer 单调下均不可用 (qa-engineer: MINOR 支应为 v1.74.0)。`:16` 的复核**只把 PATCH 候选顺延到 v1.73.1, 未动 MINOR 候选** ⇒ owner 只读 §待 owner 复议 清单即会对死号签字, 而本条自述「级别定错则 Task 5.1 的 16 个版本点、tag、CHANGELOG 标题全部连坐」。两处附加事实: knowledge-manager 与 qa-engineer 各自核实 `:16` 里「已被 v1.72.x 越过」的 **v1.72.x 在 tag 与 CHANGELOG 中从未存在**; tech-lead 读到同伴轨的取号理由 (aria `CHANGELOG.md` v1.73.0 Notes 与 `docs/handoff/2026-09-08-archive-gate-drift-shipped-v1-73-0.md:77` 逐字「避开并发轨 `10CG/Aria#195` / `10CG/Aria#199` 正在争的 `v1.71.2` / `v1.72.0`」) ⇒ **两条并发轨都在等这两个号**, 顺延后须与 #199 重新协调, 而本条目对 #199 零字提及。
  *severity / category 分歧注*: qa-engineer 报 minor, 另三席 major ⇒ 取最高 major; tech-lead architecture / code-reviewer implementation / qa-engineer 与 knowledge-manager documentation ⇒ 取多数 documentation。
  *规则 9 注*: code-reviewer 的来源 bullet 为复合条目 (另半进 `a5bd18e1`)。

- `f355e725` [major] testing/SC-10 第三类归因路径 + 待 owner 复议 8 (`proposal.md:332` / `:388`) — **found_by: tech-lead, qa-engineer, code-reviewer, knowledge-manager (4/5)**, `conflicted: false`
  SC-10 的「日历失效」归因路径与整个待复议 8 (「是否顺手补 `now=`」) 建立在「2026-09-09 起该模块自动转红 2 条」之上, 该前提**已被同伴轨修掉**: aria `f314785` 提交自述「fix(state-scanner/test): collision_dedupe 16 个 collector 调用点钉 `now=` — 半冻结时钟致按日历腐烂 (aria-plugin#194)」, `test_handoff_multibranch_collision_dedupe.py:173` 定义 `_FIXED_NOW = 2026-08-23T12:00Z` 并在 `:276,327,363,388,436,483,547,642,683,729,783` 逐处传入 (knowledge-manager 逐行列出)。四席今日 (2026-09-10) 各自实跑取到同一组数字: `f314785` 上该模块 **`Ran 23 tests … OK`**; 冻结基线 `301641b` 上 **`Ran 21 … FAILED (failures=2)`** (`'none' != 'cross_owner'` 与 `0 != 1`, 即待复议 8 预言的两条)。qa-engineer 另把 9 模块点名集在两 SHA 上整跑: `301641b` = `Ran 167 … FAILED (failures=3)` (2 条日历真红 + 1 条导出面 hook 可执行位, 真 checkout 上不红), `f314785` = `Ran 169 … FAILED (failures=1)` (仅 hook 可执行位); knowledge-manager 另记五模块点名集今日 `Ran 104 … OK` ⇒ SC-10 钉死的 `Ran 102 tests … OK` 亦过时。⇒ 三处连锁: (1) 一个被列为 Phase B 硬前置的 owner 门**失去对象**; (2) SC-10 的硬句「基线取样时点必须早于 2026-09-09 …… 若已过该日, 先按 §待复议 8 的裁定处置再取基线」今日字面成立 ⇒ **Phase B 被一个已修好的缺陷锁死**; (3) 按待复议 8 的「不修」推荐默认走, Task 4.3 的「既有测试全绿」与 SC-10 的「真仓 checkout 零失败」在 `301641b` 上恒不可满足。
  *category 分歧注*: tech-lead architecture, 另三席 testing ⇒ 取多数 testing。

- `6f60cbc8` [major] testing/SC-3 · Task 1.2 新夹具的 `core.quotePath` 隔离 — **found_by: qa-engineer (1/5)**, `conflicted: false`
  R4 `177d72e6` 的修法 (「新夹具必须照 `test_handoff_multibranch_collision_dedupe.py:181-182` 的 `_GIT_ENV` 写法把 `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` 设 `/dev/null`」) 已落进 SC-3, 但**该处方够不到被测代码**: 模板里的 `_GIT_ENV` 只作为 `env=` 传给夹具自己的 `subprocess.run` (`_git()` 助手), 而被测的 `_list_handoff_files` 走 `_common._run` → `_noninteractive_git_env` = `{**os.environ, "LC_ALL": "C", …}` (`_common.py:341`)。qa-engineer 三档隔离实跑: (A) 宿主无 quotePath 覆盖 ⇒ 中文件被丢弃 (SC-3 红); (B) 宿主 global 设 `core.quotePath=false` 且测试照模板只喂自己的 `_git()` ⇒ 中文件照常被枚举, **SC-3 在 `301641b` 上就是绿的**; (C) 另行 patch `os.environ` 的 `GIT_CONFIG_GLOBAL/SYSTEM` ⇒ 恢复为红。⇒ R4 想关的门只关了一半, Task 1.2 的「五族全红」在 `quotePath=false` 的宿主 (中文 / 日文环境, 本仓工作语言即中文) 上仍不可满足, 而 F2 在整个 SC 集里只有 SC-3 一条覆盖 (rule6_note 的 substitute 面缺一角)。
  *修法 (qa-engineer, 二选一写进 SC-3)*: `mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})` 包住被测调用; 或临时仓内 `git config core.quotePath true` 走**仓内 local 配置** (不依赖任何环境变量传递)。

- `c9728601` [major] testing/§3 上报字段 `filename` 的 basename 硬口径 · 全 SC 集覆盖 — **found_by: qa-engineer (1/5)**, `conflicted: false`
  §3 与 §5 用整段把「只有 `scan.py:186` 的拼串改读 `rel_path`; `:193` / `:209` 上报的 `"filename"` 仍取 basename、**逐字节不变**」钉成硬口径, 并据此宣布不需登记进 §5 / §6 / CHANGELOG / SC 集。但**全 SC 表 (`proposal.md:319-356`) 对 `inconclusive` / `offenders` / `errors[].tracks[]` 零覆盖** (grep 实证), 唯一被援引作保的 `test_scan_integration.py:272` 结构上分辨不出两种实现 —— Task 2.2(c) 要补的键值 `"rel_path": "2026-07-19-x.md"` 与 `filename` **同值**, 且 `_mock_run` (`:172-176`) 对任何 `git log -1` 返回同一 SHA、**完全不看路径参数**。qa-engineer 实跑证明盲区: 在 `301641b` 副本上按**被明令禁止**的写法把 `:180` 局部变量整体重指 `rel_path` + 按 Task 2.2(c) 补夹具键 ⇒ `Ran 19 tests … OK` 全绿。⇒ 一个进快照顶层 `errors[].tracks[]` 的机读字段, 其「不许变」是全文最强口径之一, 却既无 SC 也无既有断言能证伪。
  *修法 (qa-engineer)*: SC-6 的子目录夹具上追加一条断言 (令该 track 走 `inconclusive` 或 `offenders` 支, 断 `["filename"] == basename` 且不含 `/`), 或新开一条 SC。
  *与 `d3227a59` 的关系 (规则 4 保留两条)*: 本条是「判据缺失 ⇒ 不可证伪」, `d3227a59` 是「该口径的语义后果未登记」, 修法互不覆盖。

- `079dcc71` [major] architecture/§2.5 `degraded_reason` 返回契约在三分支的存在性 (`proposal.md:147` / `:154` / `:239`) — **found_by: code-reviewer (1/5)**, `conflicted: false`
  该键的存在性只在 `n_active == 1` 支被断言 (SC-15 布局 1 (i) / 布局 2 (h) / 布局 3 (j) 全落在 pointer 支), `banner` 与 `skipped` 两支未定义; 措辞亦不自洽 —— `:154` 写「optional 返回键 (缺省 None)」, `:239` 却给另两个新字段写「恒存在」。⇒ **只在 pointer 支加键的实现能通过全部 SC**, 而 Task 2.5(e) 要改的公开契约 `references/phase-1-collectors.md:102` 将声明一个在 2/3 分支不存在的键 = 本 spec 立意要修的「契约陈述 ≠ 实现」。对照组: `unreadable_count` 配了 SC-14 (错误路径) + SC-16 (成功路径) 两面 (证据: `latest_md_writer.py:298-320`)。
  *相关正向核验 (规则 5 内注)*: backend-architect 报告正文 decision 独立复核 collector 侧的「恒存在」不变量**覆盖完全** (`collect_handoff_multibranch` 恰两个 `return r`: `:596` fail-soft 早退与 `:755` 正常返回) —— 与本条不矛盾, 两者分别是 collector 侧与 writer 侧。

- `b0f70827` [major] architecture/§4 `unreadable_count` 三类外延定义第 3 类 (§7 末条 / Impact.Risk 末条 / Task 2.3) — **found_by: backend-architect (1/5)**, `conflicted: false`
  R4 `dd55dac3` 刚收敛的择一 (「不可解码 UTF-8 名 ⇒ 显式跳过, 不计入 `unreadable_count`」) **在本 collector 上不可实现, 且实际结果与之相反**。所援引的先例 `handoff.py:317-322` (`entry.name.encode("utf-8")` / `except UnicodeError: continue`) 有效, 是因为那里的名来自 `os.scandir` 的 **surrogateescape** 字符串; 而本 collector 的名来自 `_run`, 解码为 `encoding="utf-8", errors="replace"` (`_common.py:411-412`) ⇒ 坏字节变 **U+FFFD**, `"�".encode("utf-8")` **不抛**, 守卫恒不触发。backend-architect hermetic 全链实跑 (临时仓建名含 `0xff` 的 `docs/handoff/2026-\xff-bad.md`): `ls-tree -r --name-only -z` 经同款解码得 `'docs/handoff/2026-�-bad.md'` → `.encode("utf-8")` OK (跳过不发生) → 过 `.md` 过滤 → `git show HEAD:<该路径>` **rc=128** ⇒ 落进 §4 第 1 类 ⇒ **被计入 `unreadable_count`**, 与定义相反; 对照同脚本内 `os.scandir` 得 `'2026-\udcff-bad.md'` 并抛 `UnicodeEncodeError` (先例在 `handoff.py` 侧确实有效) ⇒ 两条数据通路的字符串生成机制不同, **先例不可移植**。后果正是 §4 自己警示的那条:「计进 `unreadable_count` 会让一个恒不可修复的量永久非零」; 且 **SC 集无一条覆盖第 3 类** (SC-5 只造 git show 失败, SC-3 只造可解码中文名) ⇒ 该错误不会被任何验收判据抓到。
  *修法 (backend-architect, 二选一须在正文择定, 不得保留现文)*: (i) 改判据为「`rel` 含 U+FFFD (或 `rel.encode("utf-8","surrogateescape")` 回写后与 tree 原字节不等) 即跳过」并补一条 SC; (ii) 承认本 collector 结构上分辨不出, 把第 3 类改写为「不可解码名与 git show 失败合流、计入 `unreadable_count`」并同步 §7 / Impact.Risk / CHANGELOG 的边界措辞。

- `669e7f86` [major] documentation/§6.5 CHANGELOG 计划 + Impact (F1 / AC-5 第六个被改动的量) — **found_by: code-reviewer (1/5)**, `conflicted: false`
  §6.5 (`:238`) 把 `### Fixed` 钉死为三条 (子目录 / 非 ASCII / 假 legacy) 且 SC-11(e) 按三条机检, `### Changed` 四条也不含 AC-5 面; 而 `:264` 的 §Impact 自称「修掉一个跨文件静默失效点 (F1): AC-5 ancestry 检查……变成真检查」。修好路径后子目录 track 会**首次**走到 `git merge-base --is-ancestor` 并可产生顶层 `errors[]` 的 `snapshot_self_contradiction` / `snapshot_consistency_inconclusive` (`scan.py:186-213,260-284`) —— 这是**第六个**被本 spec 改动的量 (spec 自己登记了 `exists` / `len(tracks)` / `legacy_count` / `collision.kind` / `n_active` 五个), 版本 SOT 与 Risk 表零登记 (Rule #3 同步缺口)。

### Minor (13)

- `d3227a59` [minor] implementation/`scan.py:193` / `:209` 上报面 `filename` 的语义后果 (§3 / §5 / Task 5.3) — **found_by: code-reviewer (1/5)**
  把上报 `filename` 钉成 basename 后, 子目录 track 的 `offenders` / `inconclusive` 报告不再唯一标识**实际被检查的文件** (命令行用 `rel_path`) —— 正是 §Why 后果 3「同名不同目录不可区分」被搬到错误报告面, 未登记进 Task 5.3。建议至少与 Task 5.3(e) 的 `errors[].tracks[]` schema 缺口一并登记 (证据: `proposal.md:133,196,314`; `scan.py:192-196,207-212`)。

- `2a7110db` [minor] testing/`degraded_reason` 的 `missing_filename` 取值 (§2.5 / SC-15) — **found_by: qa-engineer (1/5)**
  §2.5 定义三值枚举 (`None` / `missing_filename` / `target_in_subdir`), SC-15 只钉 `None` (布局 1 (i) / 布局 3 (j)) 与 `target_in_subdir` (布局 2 (h)); 而「缺 `filename` ⇒ 降级」这一支**今天本就零测试** (`test_p1_layer_h.py` 全文无 unavailable / 缺 filename 用例, grep 零命中) ⇒ 实施者把该支的 reason 写成任意串 (甚至复用 `target_in_subdir`) 仍全绿。修法: SC-15 加一个「active track 缺 `filename` 键」的最小布局 (成本 = 一个手搓 snapshot dict), 断 `degraded_reason == "missing_filename"`。

- `dfcc7e6c` [minor] documentation/§2.5 与 Task 2.5(e2) 的 `_render_pointer` 调用点行号 `:302` — **found_by: backend-architect, qa-engineer, code-reviewer (3/5)**
  三席各自实读 `latest_md_writer.py:302` = `elif n_active == 1:`, 真实调用在 **`:303`** (`content = _render_pointer(active_tracks[0], now)`), 而 `proposal.md:147` / `:288` 两处写「其**唯一**调用点是 `:302`」。该行号载重于「返回形状改 `tuple[str, str | None]` 后在哪解包」这条处方, 会把实施者指到判断行。backend-architect 指其与 R4 五席全席条目 `7b7aed03` (`:495-496` 实为 `:494`) **同型**; code-reviewer 另指 `_render_pointer_unavailable` 还有内部调用点 `:124`, 改返回形状时须同批处理。
  *category 分歧注*: backend-architect / qa-engineer documentation, code-reviewer implementation ⇒ 取多数 documentation。

- `1efc6e5d` [minor] architecture/§What.1 前缀守卫新 kind 的上报通道 (Task 2.1 (i) / SC-9) — **found_by: backend-architect (1/5)**
  新 kind `handoff_multibranch_unexpected_path_prefix` 按处方只注入 `r.soft_error` ⇒ 只进 `CollectorResult.errors`, **不进** `data["errors"]` (快照 `tracks_multibranch.errors[]`, schema `:1101`), 将成为本 collector 唯一单通道的 kind —— 既有四个 kind 全部双通道成对 (`:587`+`:594` / `:607`+`:608` / `:622`+`:623` / `:641`+`:643`); 而 SC-9 只断 soft_error, SC-14 对 `branch_list_failed` 恰好两通道各断一次 ⇒ 同一份 SC 集对新旧 kind 判据不对称。修法: Task 2.1 明写 reporter 是否同时回填 `error_messages` (推荐传一个同时写两处的闭包) + SC-9 补一条 `data["errors"]` 断言; 或显式写明该 kind 有意单通道并在 schema 登记例外。

- `870f2e0f` [minor·risk] documentation/Task 4.4 · `standards/conventions/session-handoff.md` 对子目录布局无表态 — **found_by: backend-architect (1/5)**
  本 spec 使 `docs/handoff/**` 成为 multibranch collector 的一等输入域 (方案 B/C 被显式否决), 但共享 SOT 自始至终只描述扁平布局 —— `:15` MUST canonical · `:88`/`:94` 路径模板 · `:336`「输出路径硬编码 …… 不接受 dir 参数」· `:301`「`exists: bool # docs/handoff/*.md has files?`」(单星 glob); Task 4.4 在同一文件内只改 `:97` 与 `:171-173` 两处 latest.md 派生行为。后果: Task 5.3 的遗留 issue (姊妹 collector `handoff.py` 是否也该递归) **缺规范锚点**。这些句子今天未被证伪 (归档件仍在 `docs/handoff/` 之下) 故列 risk; 但本 cycle 已付出 standards 子模块链路成本, 顺带表态 (或明写「本 spec 不表态, 交 Task 5.3」) 的边际成本接近零。
  *type 注*: backend-architect 报 risk, 汇总席保留原 type。

- `220a2393` [minor] documentation/`.aria/state-checks.yaml` 闸门行号漂移 (`proposal.md:297` Task 5.1 机械兜底列 / `:396` References) — **found_by: code-reviewer, knowledge-manager (2/5)**
  两席各自实测三条 check 的 `name:` 行现为 `:124` / `:177` / `:408` (文写 `:88` / `:141` / `:372`), 且旧行号今日各属别的 check —— `:88` = `silknode-contract-deferral-expiry`、`:141` = `m6-claude-md-version`、`:372` = `forgejo-app-token-liveness` (code-reviewer 归因 d2d93da 2026-09-07 与 ed5357f 2026-09-08 两次提交, 并核实起草时的 `fdfb183` 上确为 88/141/372)。主仓文件**不在 aria 基线冻结的覆盖面内**, 与 `dbdd80e9` 那句「全部行号继续有效」叠加会让读者误以为不必复核。影响有限 (三条 check 都给了名字, 可 grep 定位)。
  *与 decision `8e906135` 的关系 (规则 4(d))*: 本条是 Task 5.1 表的**机械兜底列**, `8e906135` 是同表的**16 个版本点**, 对象不同, 非矛盾。

- `5930ef8a` [minor] testing/§2.5 对 R4 `5105b00e` 的反证依据「`rel_path` 零命中」(`proposal.md:156`) — **found_by: code-reviewer (1/5)**
  「全模块 …… 全文件 `rel_path` 零命中 (grep 实证)」为假 —— `tests/test_p1_layer_h.py:115-116` 有两处同名循环变量。结论 (八字段 `_active_track` 夹具无该键) 仍成立, 但**机械依据本身写错**, 与本 spec 反复要求的「依据须实跑取到」自相矛盾 (R4 rework 的新写段落下游)。

- `be85ff65` [minor·risk] documentation/裸 issue 引用纪律 (`check_bare_issue_refs.py` 未注册) — **found_by: code-reviewer (1/5)**
  `f314785` 新落 `skills/state-scanner/scripts/check_bare_issue_refs.py` (fail-CLOSED, 封闭豁免集), 主仓 `.aria/bare-issue-ref-allowlist.txt` 今日新建但该 check **尚未**注册进 `.aria/state-checks.yaml`; 对本 proposal 实跑报 **18 处**裸 `#<n>` (`:1,:7,:10,:207,:223,:311,:315,:381,:396,:399`)。若本 cycle 内该闸门注册, proposal 与其 handoff 会在 Phase C/D 转红; 预防成本 = 把裸引用写成 `10CG/Aria#195` 形态。
  *type 注*: code-reviewer 报 risk, 保留原 type。

- `c3590954` [minor] testing/SC-2 夹具组成与日期 pin — **found_by: qa-engineer (1/5)**
  SC-2 的判据是「hermetic 临时仓 × 冻结 JSON × 八字段投影逐字段相等」, 却未规定夹具放哪些文件。若夹具含**无 frontmatter** 的件 (SC-16 恰要求这一类以避免真空满足), 其 `updated_at` 取 `git log -1 --format=%aI` = 建仓时刻 ⇒ 冻结 JSON 与第二次运行必然不等 = 不可复现的红; 而本文多处自陈「恒红的下场是实施者顺手削断言」。SC-4 / SC-13 已为同一机制立了「逐 commit 显式 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`」的口径, SC-2 未沿用 (证据: `proposal.md:324`; `handoff_multibranch.py:686,693`)。

- `c39306e1` [minor·risk] testing/SC-9 的 monkeypatch 面 (`_run` 是四个 git 调用的唯一出口) — **found_by: qa-engineer (1/5)**
  SC-9 说「monkeypatch `_run` 构造一批枚举返回, 其中一条不以 `docs/handoff/` 开头」, 但 `_run` 是本 collector 全部四个 git 调用 (`for-each-ref` / `ls-tree` / `git show` / `git log`) 的唯一出口 (`handoff_multibranch.py:120` 一次导入, 四处复用) ⇒ 要满足断言 (b)「同分支其它文件仍照常进 `tracks[]`」就必须写成**按命令分派**的假件 (`test_scan_integration._mock_run` 是现成范式), SC 未点明 —— 而本文对同类实现选择 (Task 2.1 (i)/(ii)、Task 2.2 缺键口径) 一律坚持「选型后果不能对实施者不可见」。
  *type 注*: qa-engineer 报 risk, 保留原 type。

- `7f46b1d1` [minor] documentation/Task 5.4 + SC-11(d)(h) 的 D.3 handoff 任务承接 — **found_by: knowledge-manager (1/5)**
  Task 5.4 (`:315`) 只列「归档 + `release_gate` claim 释放 + #195 关闭回帖」, 而 SC-11(d) 要求「本文 §6.3 与**本 cycle handoff** 各有一处『`reference-snapshot-aria.json` 未重采样』的显式 deferred 记录」、SC-11(h) 与 Task 4.4 末条同要求 handoff 内的 deferred 记录 ⇒ **验收判据的对象没有任何任务产出** (Rule #9 的 D.3 handoff 无承接)。本文自己在 R3 `73c20653`(c) 处立过口径「只在 §5 写了动作却无任务承接 ⇒ 无人执行也无从验收」并为此新建 Task 4.5, 此处未执行同一标准。

- `f1b664f0` [minor] testing/Task 1.2 两份清单 vs SC-15 布局 2 的 (d) 后半 — **found_by: knowledge-manager (1/5)**
  SC-15 布局 2 的 (d) 后半 (降级文案含具体原因) 在 rule6_note 被列为 baseline-failing 实体, 却既不在 Task 1.2 的「必须全红五族」、也不在其回归锁例外清单 (只列布局 2 的 (e) 半条)、也不在第二条记录清单 (只列 SC-15 的 (h)(i)(j)) ⇒ **红态验收无归属**。这正是 Task 1.2 自述「R3 引入例外清单的初衷正是消除这类灰区」要消除的形态, R4 的补救 (`ce719781`) 又漏了这一格 (证据: `proposal.md:280,366`)。

- `eb1f8584` [minor·risk] testing/Phase B 起点 vs 新夹具模板分叉 (SC-3 / SC-4 / SC-13 引用的 `_GIT_ENV`) — **found_by: tech-lead (1/5)**
  若维持 `301641b` 起点, 新测试会照**旧模板**写夹具, 而 origin/master 的同一文件已改 99 行 (新增 `_FIXED_NOW` `:173` 与 16 处 `now=` 口径) ⇒ 合并期出现同文件内两种时钟口径; 且 aria-plugin#194 原文记该红态「按日历恶化至 7 红」, 冻结越久基线越脏、Task 1.2 的红态记录越难与「本 spec 打的红」区分。缓解方向与 `dbdd80e9` / `f355e725` 同一处置 (基线重取到当前 `origin/master` 并重测四处引用行号)。
  *type 注*: tech-lead 报 risk, 保留原 type。

### Decisions (7 — 全部 minor; 按 R1-R4 同规则**不计入**上表缺陷 severity 计数)

- `57fbaada` [decision] documentation/R4 的 1 critical + 10 major 正文落地复核 — **found_by: tech-lead, qa-engineer, code-reviewer (3/5; backend-architect 与 knowledge-manager 在报告正文给出同一结论, 按规则 5 不计入 found_by ⇒ 实为 5/5 同结论)**
  五席各自把 R4 的 11 个缺陷 id 映回正文, 结论一致: **11/11 全部落在正文而非批注**, 未见「加批注了事」形态。落点 (合并各席): `5c28d58f`→§3 重写 + Task 2.2(c)(d) + Task 4.3 + SC-10 · `5513534d`→§3 上报字段语义归属块 + §5 表 · `ead9ac24`→§2.5 指定 `tuple[str, str | None]` + Task 2.5(e2) + SC-15 (i)(j) + 第 4 条反事实 · `5105b00e`→§2.5 裁定依据重写 (改为兼容性论证) · `7ae33f13`→SC-13(c) + SC-16 夹具组成 · `177d72e6`→§Why F2 条件式 + SC-3 配置隔离 · `31bc3c6a`→依据换 `:111` 的 996 行 + §7 / Task 4.3 · `b3e5ea8d`→Task 2.0a · `ab615189`→头部 Rule #6 行 + rule6_note 首条条件化 · `5b252465`→§6.2 + Task 2.5(g) + SC-11(k) · `23b414c9`→§5 `n_active` 行 + Impact.Risk + Task 5.3(d)。knowledge-manager 另给 id 命中计数 (各 3-9 次); tech-lead 抽验 14 条 minor 中的 6 条亦落地, 并注明残留的两处 `:495-496` 均为「勘正自身出错」的叙述性引用, SC-11(i) 判据本身已改为 `:494`。
  *category 分歧注*: tech-lead / code-reviewer documentation, qa-engineer testing ⇒ 取多数 documentation。
  *注意*: 本条只断言「R4 处置已落进正文」, **不**断言处置内容正确 —— 本轮 `6f60cbc8` / `b0f70827` / `5930ef8a` 三条正是对 R4 落地内容本身的证伪。

- `9c794f72` [decision] architecture/§5 消费方枚举完整性 (跨 skill 全树) — **found_by: tech-lead, code-reviewer (2/5; backend-architect 报告正文给出同结论的第三份独立 grep, 规则 5 不计入)**
  三份独立全树 grep 一致: `tracks[].filename` 的非测试消费点**恰 4 处** (`scan.py:180` · `handoff_multibranch.py:455` · `latest_md_writer.py:116` · `:213`); `tracks_multibranch` 跨 skill 仅 phase-d-closer 三文件 (`SKILL.md:218` · `handoff-mechanics.md:116,120,121` · `fetch_gate.py:187`, 均已入 §5 表); `_list_handoff_files` 的仓内外部消费仅 `test_max_branches_resolver.py:286,300,316,332` 四处 mock。tech-lead 另核 v1.73.0 新增的 `check_bare_issue_refs.py` / `skill_md_literal_sync_probe.py` / `phase-d-closer/tests/conftest.py` 对本 spec 触面 grep **零命中** ⇒ 新版本未引入未登记消费方。backend-architect 另核硬编码前缀点数恰 4 处 (collector 内 3 处经 `_HANDOFF_TREE_PATH` 派生 + `scan.py:186` 独立字面量) 与 §Why F1 一致。**§5 表无遗漏**。

- `b28a77a6` [decision] testing/SC-11 grep 判据的基线鉴别力 — **found_by: qa-engineer, code-reviewer (2/5; backend-architect 报告正文对 SC-11(l) 三条另给一份实测, 规则 5 不计入)**
  两席逐条实跑 `301641b` 基线, 取到同一组计数: schema `unreadable_count`=0 · `Returns only the basename`=1 · `path relative to`=0 · writer `degraded_reason`=0 · `when the filename cannot be`=1 · `Fallback when single active track has no filename`=1 · `legacy track missing filename`=1 · `legacy:<branch>:<filename>` collector 3 + schema 1 ⇒ (a)(c)(i)(k)(l) 均 baseline-failing, **无一恒绿**。backend-architect 另测 SC-11(l) 的第三条 (`layer-l-integration.md` 上 `子目录\|subdir` 基线 = 0) 亦有鉴别力。

- `31042495` [decision] testing/新增键对既有键集断言的影响 — **found_by: qa-engineer (1/5; backend-architect 报告正文给出同结论的更宽扫描, 规则 5 不计入)**
  `test_collision.py:445` 的 `set(coll.keys())` 与 `:131` / `:277` 的同类断言只作用于 collision dict 与 advisory dict, **不**作用于 TrackEntry 行; `test_p1_layer_h.py` 三处 `result["action"]` 断言无整字典 `assertEqual(result, {...})` ⇒ 新增 `rel_path` / `degraded_reason` 结构上打不红既有键集断言。backend-architect 另把 `.keys()` 断言全树枚举 (`test_collision.py:131,277,445` · `test_handoff.py:141` · `test_handoff_worktrees.py:446,451` · `test_p1_layer_h.py:734`), 均不覆盖 `tracks_multibranch` 行。

- `1e2c89f4` [decision] testing/R4 critical `5c28d58f` 独立复现 — **found_by: code-reviewer (1/5)**
  在当前 checkout 副本上三步复跑: 基线 `Ran 19 tests … OK` → 仅打「`rel_path` 无兜底早退」补丁即 `FAILED (failures=3)` 且 `:270` 报 `0 != 1` → 给 `HEALTHY_TRACKS` 补 `"rel_path"` 后复绿 `Ran 19 tests … OK` ⇒ 与 Task 2.2(a)(c)(d) 的落地写法**完全一致**, R4 那条 critical 的修法有效。

- `8e906135` [decision] documentation/Task 5.1 的 16 个版本点行号 — **found_by: tech-lead (1/5)**
  在主仓 HEAD `fe703c5` 上逐处实测仍命中: `README.md:8` / `:242`, `VERSION:24`, `CLAUDE.md:139` / `:141`, `README.zh.md:3` / `:10` / `:244`, `docs/architecture/system-architecture.md:189`, `docs/architecture/version-scheme.md:23` (取值均为 v1.73.0) ⇒ 该表**只需改号, 不需重定位** (与 `f8eef4d2` 的版本号顺延同批做)。
  *与 `220a2393` 的关系*: 见规则 4(d) —— 同表两列, 对象不同。

- `218efeff` [decision] architecture/待复议 7 若裁 Level 3 的拆分建议 — **found_by: tech-lead (1/5)**
  供 owner 一并裁: 按「今日症状面 vs 未来接线面」拆两个 sub-spec —— (1) 枚举层 `-z` + 相对路径 + 四调用方 + 假 legacy 移除 + schema 同步 (直接闭合 #195 报告方的三层症状); (2) pointer 写侧守卫 + `degraded_reason` + standards 第三态 + writer 契约面。理由: (2) 的全部价值发生在 `write_latest_md` 未来被 D.3 接线之后, 而它今天**零生产调用点** (`references/phase-1-collectors.md:95` 逐字「deliberately D.3-scoped … 不引入 production call-site」; tech-lead 在 `f314785` 上复跑 `grep -rn write_latest_md` 排除 tests 后仍只剩 `__init__.py` 再导出与两份文档), 却占本文近半篇幅、5 个文档同步面与整个 SC-15 三布局。**审计席不代裁 Level (Rule #10)**。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **9** / Minor **13** (另 7 条 decision 不计入)。

按 `references/report-storage.md §Verdict 计算` 的 SOT 规则: `0 Critical + >=1 Major ⇒ PASS_WITH_WARNINGS`。`drift_terminated: false`, 无 override。五席**自报 verdict 全为 PASS_WITH_WARNINGS** (自报计数: tech-lead 0/3/1 · backend-architect 0/1/3 · qa-engineer 0/4/6 · code-reviewer 0/5/5 · knowledge-manager 0/4/3), 与聚合结果同档 —— 与 R4「四席 PASS_WITH_WARNINGS 对一席 FAIL」的分裂相比, 本轮**无定级分歧、无 conflicted**。

**方案骨架第五轮仍无人主张推翻**: A′ (= `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git show 失败不再伪造 legacy + 写侧守卫) 被五席从五个透镜再次独立复核成立; 消费方枚举经三份独立全树 grep 证明完备 (`9c794f72`); R4 的 1 critical + 10 major 经 5/5 全席复核**全部落进正文而非批注** (`57fbaada`), 且 code-reviewer 独立复跑确认那条 critical 的修法有效 (`1e2c89f4`)。

9 条 Major 集中在**两族**:

1. **「世界在动, 基线冻在 3 天前」(5 条, 全部 4/5 高共识)** — `dbdd80e9`(「全部行号继续有效」为假) · `a5bd18e1`(Phase B/C 起点与 gitlink 回退口子) · `f8eef4d2`(版本候选号 `v1.71.2` / `v1.72.0` 已低于已发布的 v1.73.0) · `f355e725`(日历门被上游 aria-plugin#194 关闭, 而 SC-10 的「基线须早于 2026-09-09」今日反过来锁死 Phase B) · 连带 minor `220a2393`(主仓 `.aria/state-checks.yaml` 行号漂移)。四条同一根因: 2026-09-10 的基线复核是一次**事后 amendment**, 只在自身段落里陈述新事实, 未按 neutralize 要求传播到依赖旧事实的六处载重断言 (knowledge-manager 报告正文另立此为「同源性」风险, 并指出本文从未枚举「触点文件集」⇒ 每次复核的过滤面都由执笔者临场重建, 本轮漏检即由此产生)。**处置是一次基线重冻 + 全文 neutralize 扫描, 不是逐条打补丁, 零设计骨架改动**。
2. **R4 落地内容自身的缺口与证伪 (4 条, 均单席深挖)** — `6f60cbc8`(R4 `177d72e6` 的 SC-3 配置隔离处方够不到被测子进程, 三档实跑证明 SC-3 在 `quotePath=false` 宿主上基线就是绿的) · `b0f70827`(R4 `dd55dac3` 择定的「不可解码名显式跳过」在本 collector 的 `errors="replace"` 通路上恒不触发, hermetic 全链实跑取到相反结果, 且无 SC 覆盖) · `c9728601`(§3 最强口径之一「上报 `filename` 逐字节不变」全 SC 集零覆盖, 被禁写法实跑全绿) · `079dcc71`(`degraded_reason` 只在 `n_active == 1` 支有断言, banner / skipped 两支未定义) + `669e7f86`(F1 修复带出的第六个被改动的量未进 CHANGELOG / Risk 表)。这一族与 minor `5930ef8a`(反证依据「`rel_path` 零命中」为假) 同属 memory `feedback_author_and_verifier_must_differ_for_corrections` 记的形态: **勘正动作由原作者执笔时错误系统性逃逸**, 建议 rework 由非 R4 执笔者执笔。

**收敛判定 (汇总席实算, 最终由编排脚本裁决)**: 本轮 keys (29 条) 与上轮 R4 keys (34 条) 逐条归一后**交集 0** ⇒ `conclusions_stable = false`; `unanimous_pass = false` (Vote REVISE 5 / PASS 0) ⇒ **`converged = false`**。五轮的四元组交集依次为 R1∩R2 = 0 · R2∩R3 = 0 · R3∩R4 = 1 · R4∩R5 = 0 —— 按 memory `feedback_convergence_needs_zero_rework_round`「收敛只发生在干净轮 + 零 rework 的下一轮」, 本轮既非干净轮 (9 major), 结论集又整体翻新, 结构上不可能收敛。**须交 owner 的判断 (Rule #10, 汇总席不代裁)**: `.aria/config.json` 的 `audit.max_rounds = 5` ⇒ 本轮即终轮 (knowledge-manager 报告正文的「终轮预算」风险), 是否按 MAX_ROUNDS_EXHAUSTED 降级、以及待复议 6 / 7 / 8 三个 owner 门如何裁, 均须 owner 闭合。

**跨轮观察 (记录, 非本轮 conflicted)**: R4 的 decision `59f15b38`「Task 5.2 的『从 `301641b` 前进』与两个候选号未被占用均正确」在本轮被 `a5bd18e1` / `f8eef4d2` 整条推翻 —— 不是审计席前后矛盾, 而是**同伴轨在 R4 与 R5 之间 ship 了 v1.73.0**。这条本身即 `dbdd80e9` 一族的最好例证: 冻结基线的「已核实」结论有保质期。

`post_spec` 为 `blocking: false` (见 `report-format.md §阻塞行为` —— 非阻塞检查点), 本 verdict **不阻断**后续流程; 但按 Rule #10, 上述 major 不得由实施者以「代码面小 / Level 低 / session 已长 / 反正是终轮」自行降格、跳过或改序。

---

## 轮次记录

### Round 1 (承前)

- Agents: 5/5 (缺席 0) — Conclusions 去重后 33 (Critical 2 / Major 15 / Minor 10 / Decisions 6), 去重前 60
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**
- 来源: `.aria/audit-reports/post_spec-R1-2026-09-06T154800-000Z-R1-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 2 (承前)

- Agents: 5/5 — Conclusions 去重后 31 (Critical 3 / Major 10 / Minor 9 / Decisions 9), 去重前 55; 与 R1 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **FAIL**; conflicted 1 (`cecc06af`, 已闭合)

### Round 3 (承前)

- Agents: 5/5 — Conclusions 去重后 33 (Critical 0 / Major 19 / Minor 7 / Decisions 7), 去重前 51; 与 R2 交集 0
- Vote: REVISE 5 / PASS 0 — verdict **PASS_WITH_WARNINGS**; conflicted 1 (`120e1171`, 已闭合)

### Round 4 (承前)

- Agents: 5/5 — Conclusions 去重后 34 (Critical 1 / Major 10 / Minor 14 / Decisions 9), 去重前 57; 与 R3 交集 1 (decision `a0cb3407`)
- Vote: REVISE 5 / PASS 0 — verdict **FAIL** (唯一支点 = `5c28d58f` 的 critical vs major 定级差); conflicted 0
- 来源: `.aria/audit-reports/post_spec-R4-2026-09-07T004500-000Z-R4-handoff-multibranch-subdir-path-fidelity-aggregated.md`

### Round 5

- **Agents**: 5/5 (缺席 0; `round_incomplete: false`, `skipped_agents: []`) — tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (五席逐席自述一致; tech-lead 另核 v1.73.0 新增三个脚本对本 spec 触面零命中, 并读到同伴轨 `docs/handoff/2026-09-08-archive-gate-drift-shipped-v1-73-0.md:77` 逐字记载「避开并发轨 `10CG/Aria#195` / `10CG/Aria#199` 正在争的 `v1.71.2` / `v1.72.0`」⇒ 与 #199 的耦合面**只在版本号取号**, 无文件交集)
- **审计对象冻结**: 五席均自述「只审不改」; tech-lead 收尾 `git status --porcelain` = 0 行 (三仓干净), backend-architect / qa-engineer 的核验产物落 scratchpad 临时仓 ⇒ 符合 memory `feedback_audit_object_frozen_until_round_aggregated`
- **Conclusions**: 去重前 **46** (tech-lead 8 / backend-architect 4 / qa-engineer 13 / code-reviewer 14 / knowledge-manager 7; 其中 2 条为复合条目, 按缺陷计 48 项) → 去重后 **29** (Critical 0 / Major 9 / Minor 13 / Decisions 7)
- **Delta vs 上轮 (R4, 34 条)**: `+29 / -34` —— 四元组交集 **0** (python3 集合比较实算)。R4 的 1 critical + 10 major 全部闭合 (`57fbaada`, 5/5 复核), 本轮 22 条缺陷类**全部为新增**: 其中 5 条源于 R4 之后同伴轨 ship v1.73.0 (`dbdd80e9` / `a5bd18e1` / `f8eef4d2` / `f355e725` / `220a2393`), 4 条是 R4 rework 落地内容自身经实跑证伪或留缺口 (`6f60cbc8` / `b0f70827` / `5930ef8a` / `079dcc71`), 其余 13 条是前四轮未测到的机械事实与判据缺口
- **Vote 票型**: REVISE **5** / PASS **0** ⇒ `unanimous_pass = false`
- **自报 verdict 票型**: PASS_WITH_WARNINGS **5** / FAIL **0** (五席一致, R4 的定级分裂已消失)
- **conflicted**: **0** 条 (逐条比对未发现结论相反的对立意见; 唯一需说明的 `220a2393` vs `8e906135` 经核为同表两列、对象不同, 非矛盾)
- **收敛判定 (汇总席实算)**: `conclusions_stable = (R5 keys == R4 keys)` = **false** (29 vs 34, 交集 0); `unanimous_pass` = **false** ⇒ **`converged = false`**
- **振荡检测**: `keys_R5 == keys_R3`? **false** —— R3 为 Critical 0 / Major 19 / Minor 7 / Decisions 7 (33 条, 据 R4 聚合报告 §轮次记录), R5 为 0 / 9 / 13 / 7 (29 条), 条目数与 severity 分布均不相等 ⇒ `oscillation = false`
- **Duration**: N/A (编排脚本未向汇总席传递计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 5 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| 需补齐 frontmatter 的席位报告 | 0 / 5 (机械核验 15/15/15/15/15 字段) |
| 去重前/后 conclusions | 46 / 29 |
| Critical / Major / Minor | 0 / 9 / 13 |
| Decisions (不计入 severity) | 7 |
| conflicted 条目 | 0 |
| finding id 碰撞 | 0 / 29 (python3 sha256 实算) |
| 与上轮四元组交集 | 0 (R5 29 条 vs R4 34 条) |
| 收敛轮次 | N/A (未收敛; 本轮为 `max_rounds = 5` 终轮) |

### 席位票型与自报计数

| 席位 | Vote | 自报 verdict | 自报 C / M / m | 结构化条目数 |
|------|------|--------------|----------------|--------------|
| tech-lead | REVISE | PASS_WITH_WARNINGS | 0 / 3 / 1 | 8 (含 4 decision) |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0 / 1 / 3 | 4 (报告正文另有 11 条 decision + 17 项机械核验未入清单) |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 6 | 13 (含 3 decision; 附录另有 8 项实跑清单) |
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0 / 5 / 5 | 14 (含 4 decision) |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0 / 4 / 3 | 7 (报告正文另有 6 条 decision + 2 条 risk 未入清单) |

---

## Rework 清单

Critical **0** 条 + Major **9** 条, 逐条列出 (id / 提出席位 / 建议动作)。动作取自各席报告原文, 汇总席**不裁决**、不新增修法。

| # | id | 席位 | 建议动作 |
|---|----|------|----------|
| 1 | `dbdd80e9` | tech-lead · qa-engineer · code-reviewer · knowledge-manager | 删除或改写 `:16` 的「本文**全部行号**在 `f314785` 上继续有效」——改成「触点集零 diff」这一实际被验证的范围, 或改成双轨口径「行号锚定 `301641b`, 实施基于 `f314785`」; 同批重测本文引用 `test_handoff_multibranch_collision_dedupe.py` 的四处行号 (`_GIT_ENV` `:174-183`→`:176-185` · `GIT_CONFIG_*` `:181-182`→`:183-184` · 日历夹具 `:380-382`→`:382-384` · 调用点 `:386`→`:388`) 与 `aria/CHANGELOG.md` 的三处先例行 (`:84`→`:109` · `:93-97`→`:118-122` · `:99-100`→`:124-125`); knowledge-manager 另建议**在 §References 之外单列一份可直接喂给 `git diff` 的触点文件清单**, 终止「过滤面临场重建」。 |
| 2 | `a5bd18e1` | tech-lead · qa-engineer · code-reviewer · knowledge-manager | 把 `:9` / `:10` / Task 5.2 `:313` 三处的起点从 `301641b` 改写为实测的 `f314785`, 回退禁令由点名 `0545f86` 扩为「**不得低于当前主仓 gitlink**」; `:16` 的 amendment 须在这三处加 inline neutralize 标记, 而不是只在自身段落陈述。 |
| 3 | `f8eef4d2` | tech-lead · qa-engineer · code-reviewer · knowledge-manager | 待复议 6 的实测句与推荐默认同步到实况: tag 集 = v1.70.0 / v1.71.0 / v1.71.1 / **v1.73.0**, `plugin.json` = 1.73.0 ⇒ PATCH 候选 v1.73.1 (`:16` 已顺延)、**MINOR 候选由 v1.72.0 改为 v1.74.0**; 删掉 `:16` 里查无实据的「v1.72.x」; 补一句与并发轨 `10CG/Aria#199` 的取号协调 (两轨都在等原来的两个号)。**须 owner 裁级别** (Rule #10)。 |
| 4 | `f355e725` | tech-lead · qa-engineer · code-reviewer · knowledge-manager | 把基线冻结与 Phase B 分支点重取到 ≥ `f314785`; 待复议 8 由 owner 门改写为「已由上游 `10CG/aria-plugin#194` 关闭」的记述; SC-10 删掉「第三类归因路径 (日历失效)」整段与「基线须早于 2026-09-09」硬句, 并按重取后的基线更新点名集总数 (旧钉死的 `Ran 102` / `Ran 167` 均过时; 今日 9 模块在 `f314785` 上仅剩 1 条导出面 hook 可执行位失败, 真 checkout 不红)。 |
| 5 | `6f60cbc8` | qa-engineer | SC-3 的配置隔离处方改成够得到被测子进程的两选一: `mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})` 包住被测调用, 或临时仓内 `git config core.quotePath true` (仓内 local 配置, 不依赖环境变量传递); 同批订正「照 `_GIT_ENV` 写法」这一措辞在 SC-4 / SC-13 的连带引用。 |
| 6 | `c9728601` | qa-engineer | 给 SC-6 的子目录夹具追加一条上报字段断言 (令该 track 落进 `inconclusive` 或 `offenders`, 断 `["filename"]` 为 basename 且不含 `/`), 或新开一条 SC —— 使 §3「逐字节不变」这条硬口径第一次具备反事实。 |
| 7 | `079dcc71` | code-reviewer | §2.5 明确 `degraded_reason` 在 `banner` / `skipped` 两支的键存在性 (恒存在并置 `None`, 还是仅 pointer 支存在), 并消除 `:154`「optional 返回键」与 `:239`「恒存在」的措辞冲突; 按择定结果给 SC-15 补对应布局的断言, 使 Task 2.5(e) 要改的 `references/phase-1-collectors.md:102` 契约陈述与实现一致 (对照 `unreadable_count` 的 SC-14 + SC-16 两面覆盖)。 |
| 8 | `b0f70827` | backend-architect | §4 第 3 类外延二选一改写并同步 §7 末条 / Impact.Risk 末条 / Task 2.3 / CHANGELOG 边界措辞: (i) 判据改为「`rel` 含 U+FFFD (或 `rel.encode("utf-8","surrogateescape")` 回写后与 tree 原字节不等) 即跳过」并补一条 SC; 或 (ii) 承认本 collector 分辨不出, 改为「不可解码名与 git show 失败合流、计入 `unreadable_count`」。**不得保留现文** (它对一个新机读契约字段给了实现不出来的规定, 且无 SC 覆盖)。 |
| 9 | `669e7f86` | code-reviewer | 把 F1 修复带出的第六个量 (子目录 track 首次走到 `git merge-base --is-ancestor` ⇒ 可产生 `snapshot_self_contradiction` / `snapshot_consistency_inconclusive`) 登记进 §6.5 CHANGELOG (`### Fixed` 或 `### Changed`) 与 §5 / Impact.Risk 表, 并同步 SC-11(e) 的三条机检口径。 |

> **Minor 与 Decisions 不进 Rework 清单** (13 条 minor 见上文 `### Minor (13)` 各条内附修法; 7 条 decision 为核实通过项, 无动作)。
>
> **跨条提醒 (汇总席不裁决, 仅记)**: 第 1-4 条是同一次基线漂移的四个下游, 建议**一次 neutralize 扫描 + 一次基线重冻**整批闭合, 不要逐条打补丁 (memory `feedback_handoff_closure_neutralize_nextstep` / `feedback_status_doc_claims_need_diff_verification_and_variant_sweep`); 第 5 / 6 / 8 条与 minor `5930ef8a` 同属「R4 勘正动作自身引入新错或未闭合」形态, 按 memory `feedback_author_and_verifier_must_differ_for_corrections` 建议**由非 R4 执笔者执笔**。
>
> **仍须 owner 闭合的门 (Rule #10, 审计席不代裁)**: 待复议 6 (版本级别 / 候选号, 见第 3 条) · 待复议 7 (Level 2 vs 3, decision `218efeff` 另给拆分建议) · 待复议 8 (是否降为「上游已关闭」记述, 见第 4 条) · 以及 `max_rounds = 5` 终轮后的降级处置。
