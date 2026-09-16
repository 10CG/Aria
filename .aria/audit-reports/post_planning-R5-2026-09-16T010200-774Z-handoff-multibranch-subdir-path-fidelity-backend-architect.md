---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T01:50:44.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R5 — backend-architect (10CG/Aria#195, v5 `0e60b08`)

本席为 R5 (`max_rounds: 5` 最后一轮) 新派席位，前四轮未参与。侧重：组 2/3 代码级正确性、TASK-035 六补丁代码级推演、TASK-029/030/031/034 的 git 语义与被委派方 (`phase-c-integrator` C.2.5) 真实行为。方法：逐行核对 aria `1cb3872` 实际源码、独立实跑 `sc11-predicate-validation.py`、在 `/tmp/.../scratchpad/r5-backend-architect/gitexp/` 建临时仓做 git 行为实验、直接读 `phase-c-integrator/SKILL.md` 与本仓 `.aria/config.json` / `git remote -v`。

## 一、R4 处置落地核验

| R4 簇 | 落地位置 | 证据 (file:line / 实测) |
|---|---|---|
| PP4-M1 (TASK-029 取号恢复死锁) | TASK-029 第4/6步基准改「台账最近一次记录」; AI流程判断清单#22(a) | `detailed-tasks.yaml:806,808`（diff 确认新句）|
| PP4-M2 (两仓合并结局不一致无处置; 本地领先静默放行) | TASK-029 第3步补二次相等断言; 第5步「两个子模块视为一个整体」 | `detailed-tasks.yaml:805,807`; **本席实测**：本地领先时 `git merge --ff-only origin/master` 返回 `Already up to date.` exit=0 且不改变本地 (见下「git 实验 1」) — 证实 v5 新增断言是必要的 |
| PP4-M3 (第7步 `--emit-json` 核验必然 rc=3 且恒绿) | 已整条删除；AI流程判断清单#27 | `detailed-tasks.yaml:810`（diff 确认第7步不再含该核验）|
| PP4-M4 (TASK-031「双远程 ls-remote 一致」恒假) | 改为委派 `phase-c-integrator` C.2.5；AI流程判断清单#28 | `detailed-tasks.yaml:882`；**本席实测**：`aria/skills/phase-c-integrator/SKILL.md:612-643` 逐条核对通过（见下「C.2.5 核验」）|
| PP4-M5 (半推仍可 bump gitlink；主仓推送无失败分支) | `owner_gates` 两条 TASK-034 项补「不进 TASK-030」；TASK-030 补前置断言；TASK-031/032 推送条补失败分支 | `detailed-tasks.yaml:127-129(owner_gates),291(TASK-030前置),300,317`（diff 确认新增文字）|
| PP4-M6 ((j1)(j2)(j3) 可被「同段/同行续写」骗过) | 三谓词换量为「只看 `(parse_ok` 起的平衡括号之内」 | `detailed-tasks.yaml:94-96` 谓词代码；**本席实测**：脚本实跑 24 态 x 19 谓词，`bad_j1_same_para`/`bad_j3_same_block`/`bad_j2_same_line` 均精确只令对应谓词 FAIL，与 yaml 记录逐字节一致（见下「脚本实跑」）|
| PP4-M7 ((l1) 块截取含标题行余部; Scenarios 可被标题括注满足) | 块截取丢标题行余部；Scenarios 改判结局行计数 | `detailed-tasks.yaml:99-100` 谓词代码；同上脚本实跑确认 `bad_l1_title_paren` 精确只令 (l1) FAIL |
| m1–m16 (16条 Minor) | 逐条检查 diff，均已落地（m1 owner_gates 顶部加注 + TASK-029 第2步补重执行句；m7 第2步判据改可执行式；m9 CHANGELOG 计数括注改写；m10 「读前必看」#14 与 v5 谓词同步；m11 `(j4)` 左边界改 `[^0-9A-Za-z]`；m13 部分接受，仅收紧 (c2)……) | `diff edd256d 0e60b08 -- tasks.md detailed-tasks.yaml` 全文比对，未见遗漏 |

**结论**：R4 的 7 Major + 16 Minor 全部在 v5 找到对应改动，且本席对其中技术含量最高的 5 条 (M2/M4/M6/M7 + 部分 M5) 做了独立实测（非仅读 diff），全部与聚合报告的处置描述一致，无「声称已改但实测不符」的情况。

## 二、实施者试派生（组 2/3 代码级 + git 语义，共 7 项）

### 1. TASK-009/010/011/012/014 —— 行号与落点核对

逐一读取 aria `1cb3872` 实际源码，核对四份计划引用的行号：

- `handoff_multibranch.py:240-290` = `_list_handoff_files` 整个函数体，`:246-247` 确认是跨行的 "Returns only the basename...so callers / compose the full git-object path as needed." — 与 SC-11(c) 描述的「跨行」逐字符相符。
- `:329-336` = `_make_legacy_track_id`；`:36`/`:332`/`:494` 三处 `legacy:<branch>:<filename>` 字面量经 `grep -n` 核实确为这三行（非估读）。
- `:428-455` = `_dedupe_sort_key`，docstring 第 429-430 行确实含字面 `(parse_ok` 子串 —— 这是 (j1) 谓词的锚点，位置精确。
- `:586-596` = 分支枚举失败的 fail-soft 早退 dict，结构与 TASK-012 描述的 `{"exists"/"tracks"/"branches_scanned"/"legacy_count"/"collision"/"errors"}` 完全一致。
- `:619-626` = 主循环调用 `_list_handoff_files` 并处理 `ls_err` 之处，是 TASK-009 「reporter 传入」的正确落点。
- `:636-658` = git show 失败处理块，`:644` 精确是 `fallback_date = _get_file_commit_date(...)`（TASK-011 要求删除的那一行），`:665-676`/`:683-698` 为两个 TrackEntry 构造点，`:686` 精确是第二个 `_get_file_commit_date` 调用点，`:753` 精确是 `"errors": error_messages,`。

结论：proposal 所称「A.2 复核 `f314785..1cb3872`：代码落点零 diff，行号全部有效」在本席重复核验下**成立**，未发现任何行号漂移。

### 2. TASK-013 —— `latest_md_writer.py` 契约面 + 试派生

通读 `writers/latest_md_writer.py` 全文（320 行），核对 TASK-013 引用的全部行号（模块 docstring `:30-35`、`_render_pointer:110-148`（内部调用 `:124`）、`_render_pointer_unavailable:151-169`、`write_latest_md:259-320`（docstring `:277-290`、唯一调用点 `:303`））**全部精确匹配**。「仅在单 active track 场景下写真实指针」一句在 `:140` 与 `:159` 确认逐字重复（`_render_pointer` 与 `_render_pointer_unavailable` 各一处）。`test_p1_layer_h.py` 现有 24 个 `def test_` 方法（`grep -c` 核实），且其对 `write_latest_md` 的断言均用 `result["action"]` 等键级访问（如 `:264 self.assertEqual(result["action"], "pointer")`），非整字典相等 —— 新增 `degraded_reason` 键不会打破这 24 个既有用例，「保持 Ran 24 … OK」的声称可信。

### 3. TASK-018 补丁 4 —— 逐行推演三行最小实现

补丁 4：在 `elif n_active == 1:` 分支解包 `_render_pointer` 之后插入
```python
t = active_tracks[0]
rel = t.get("rel_path") or t.get("filename")
if rel == t.get("filename"): degraded_reason = "target_in_subdir"
```
逐布局推演：
- **布局 1（顶层，`rel_path == filename`）**：`rel == t.get("filename")` 为真 ⇒ `degraded_reason` 被强制覆写为 `"target_in_subdir"`，而正确值应为 `None` ⇒ (i) 断言 `is None` **失败 → 红**。
- **布局 3（缺 `rel_path` 键）**：`rel = None or filename = filename`，同样 `rel == filename` 为真 ⇒ 同样被错误覆写 ⇒ (j) **红**。
- **布局 2（子目录，`rel_path != filename`）**：`rel == t.get("filename")` 为假 ⇒ `if` 不触发 ⇒ `degraded_reason` 保持 `_render_pointer` 解包时的原值（子目录场景下 `_render_pointer` 自身逻辑不变，仍正确产出 `"target_in_subdir"`）⇒ (d)（正文内容，与本补丁完全无关）与 (h)（`degraded_reason == "target_in_subdir"`）**均不受影响，保持绿**。

三条推演与计划所写「布局 1 (i) 与布局 3 (j) 红而布局 2 (d) 仍绿」**完全吻合**，且能解释为何 (e) 也不受影响（(e) 是 `collect_handoff` 的 kind 集合，与 `degraded_reason` 计算无关）。**此补丁的最小实现是正确的**，R4 m14（"是意图描述，不是可直接落笔的变更"）在 v5 已被恰当地具体化。

### 4. TASK-018 的范围缺口 —— SC-15 布局 4/5/6 反事实未被任何任务指派（新发现，Major，见下）

在做上一条推演时核对 TASK-018 「SC-15」verification bullet 全文，只列 (1)-(4) 四条反事实，覆盖布局 1/2/3；随后核对 `rule6_note` 的 baseline-failing 实体清单、`proposal.md` SC-15 细则、以及全 yaml 文件 `grep -n "KeyError\|n_active == 0\|n_active >= 2"`，确认**没有任何任务**为布局 4、5、6 指派三步法反事实。详见「四、Finding M1」。

### 5. TASK-029 —— 8 步流程的 git 语义，实仓实验

在 `scratchpad/r5-backend-architect/gitexp/` 建三组临时仓验证：

- **实验 1（本地领先 origin 时 `merge --ff-only`）**：`before: local≠origin`（local 领先一个 commit）→ `git merge --ff-only origin/master` 输出 `Already up to date.`，exit=0，**local 未变、仍不等于 origin/master**。这精确重现了 PP4-M2 指出的「不复核就会静默放行」陷阱，证实 v5 新增的「ff-only 之后再断言一次两者相等」是必要且正确的修复。
- **实验 2（`--no-ff` 合并的父提交顺序）**：`HEAD^1` = 合并前 master SHA，`HEAD^2` = feature 分支 HEAD —— 与「回退条」前置判据「`HEAD^1` 等于第 3 步记下的 SHA 且 `HEAD^2` 等于 feature 分支 HEAD」的假设完全一致。
- **实验 3（冲突场景）**：制造真实文件冲突后 `git merge --no-ff` 失败（exit=1），此时 `HEAD` **未移动**（仍是合并前 SHA）、`git status --porcelain` 显示 `UU f.txt`（**非空**）、`git rev-parse -q --verify MERGE_HEAD` 成功（exit=0）。这证实「回退条」的两分支判据互斥且穷尽：合并成功走 `reset --hard` 分支（前置全部满足），合并冲突走 `merge --abort` 分支（`porcelain` 非空使前置不成立，转而查到 `MERGE_HEAD` 存在）。
- **实验 4（无 `MERGE_HEAD` 时 `merge --abort`）**：确认会 `fatal: There is no merge to abort (MERGE_HEAD missing).`，exit=128 —— 证实计划里「先判 `MERGE_HEAD` 是否存在，否则什么都不执行」这一步是必要的防御，不是多余的谨慎。

四组实验与计划文本逐句对应，**无一处失实**。

### 6. TASK-034 —— `--atomic` vs 裸多 ref / `--follow-tags`，实仓实验

同样在临时仓构造「本地落后于远端」的场景（并发推送使 master 处于 non-fast-forward），用真实的带注释 tag 测试三种推送写法：
- `git push origin master v9.9.9`（裸两 ref）：master 被拒，但 **tag 被单独接受并发布**（远端出现孤儿 tag）。
- `git push origin master --follow-tags`（带注释 tag）：master 被拒，**tag 同样被单独发布**（远端出现孤儿 tag）。
- `git push --atomic origin master refs/tags/v9.9.9`：整个事务失败（`error: atomic push failed for ref refs/heads/master`），**没有新对象被推送**，之前已发布的孤儿 tag 也未被这次调用重复处理。

三组结果与计划文本「实测 `git push <remote> master v<vNEXT>` 与 `--follow-tags` 在 master 被拒时 tag 照样发布，留下指向未合并提交的孤儿 tag；`--atomic` 下两者同拒」**逐字符吻合**。这是计划里「禁用 `--follow-tags`」这条硬约束的技术依据，本席确认该依据成立。

### 7. TASK-031 —— 委派 `phase-c-integrator` C.2.5 是否真做计划声称的事

直接读 `aria/skills/phase-c-integrator/SKILL.md:600-643`（C.2.5 全节）逐条核对 TASK-031 的转述：

| TASK-031 声称 | SKILL.md 原文（行号） | 核对结果 |
|---|---|---|
| enabled 默认 true | `:604` `multi_remote_push.enabled: true`（默认）| 一致 |
| enforced_remotes 为空⇒自动发现 | `:615` 「skill 级 `enforced_remotes == null` 时继承顶层…空则自动发现所有 remote」| 一致 |
| 第4步a先遍历子模块推同一 remote | `:617` 「a. 遍历子模块, 调用 `git-remote-helper.push_all_remotes(...)`」| 一致，且顺序（子模块先、主仓后）也一致（`:619`）|
| verify_parity_post_push match 判定 | `:620` | 一致 |
| fail_on_partial_push 默认阻断 | `:625-630` 失败优先级表 | 一致 |

另外直接读本仓 `.aria/config.json`：`phase_c_integrator` 键下没有 `multi_remote_push`，顶层也没有 `multi_remote` —— 与 TASK-031「`.aria/config.json` 未覆盖…enabled 默认 true / enforced_remotes 为空」的台账断言完全一致；`git remote -v` 确认本仓恰好是 `origin` + `github` 两个 remote，与「本仓实测 origin 与 github」一致。**被委派方确实会做计划声称的事**，不是空引用。

（唯一需要留意但不构成 finding 的一点：C.2.5 第 4 步 a 遍历子模块时用的是子模块工作树当前 checkout 的分支状态，若彼时子模块处于 detached HEAD，SKILL.md `:638` 已声明「警告但不阻断」，不会与 TASK-034 的核验产生虚假矛盾；TASK-031 自己也写了「若它报出子模块有待推内容即与 TASK-034 的核验矛盾, 停下查明」作为兜底，是稳妥的。）

## 三、Finding

**[Major] type=issue · category=test-completeness/verification-gap · scope=detailed-tasks.yaml TASK-018 (3.4) + rule6_note + proposal.md SC-15 细则布局4/5/6 · v5 引入: 否**

**证据**：
1. `detailed-tasks.yaml` `rule6_note`（约行164）把「SC-15 布局 2 (d) 后半与 (h)、布局 1 (i)、布局 3 (j)、**布局 4、布局 5、布局 6**」并列为 baseline-failing 实体，与其前后句「每条实体均附反事实」（措辞源自 `proposal.md` substitute 覆盖节）同一语域。
2. `proposal.md` SC-15 细则明确给布局 4/5 与布局 6 各自写了专属反事实：布局4/5「实现只在 `n_active == 1` 支往返回 dict 里塞 `degraded_reason` ⇒ 布局 4 / 布局 5 双 `KeyError` ⇒ 红」；布局6「实施者给该支复用 `"target_in_subdir"` 或留空 ⇒ 红」。
3. `detailed-tasks.yaml` TASK-018（parent `3.4`，标题「其余实体反事实实跑」）的 `SC-15` verification bullet 只列 (1)-(4) 四条，逐条核对全部只覆盖布局 1/2/3（(1)(2) 覆盖布局2的(d)(e)，(3) 覆盖布局3的(g)(j)，(4) 覆盖布局1的(i)与布局3的(j)）。
4. 对整份 `detailed-tasks.yaml` 做 `grep -n "KeyError\|n_active == 0\|n_active >= 2"`，唯一涉及布局4/5/6的行是 TASK-006（组1，写 GREEN 测试）里定义断言的那一条（第295行），以及一条泛化的失败形态说明（第238行）；**没有任何任务的 verification 字段指派对布局4/5/6 执行三步法（GREEN→打补丁→RED→记 SHA+diff）**。
5. 反例（同 Spec 内的正例对照）：结构上与布局4/5「恒存在」契约完全同型的 SC-14（`unreadable_count` 必须恒存在于早退 dict）**有**专属三步法反事实——TASK-035 补丁6「fail-soft 早退 dict 删去 `unreadable_count` 键」，逐 SC 记 GREEN/RED/diff。同一份计划对结构相同的两类契约（`unreadable_count` 恒存在 vs. `degraded_reason` 恒存在）采用了不一致的验证深度。
6. 检索 R1-R4 四份 post_planning 聚合报告（`grep -n "布局 4\|布局 5\|布局 6\|missing_filename"`），**零命中**——此缺口此前四轮均未被指出。

**照计划执行会出的错**：如果 TASK-013 的实现者恰好落入 proposal 自己描述的那类坏实现（`degraded_reason` 只在 `n_active == 1` 分支赋值、其余分支忘记无条件初始化；或 `_render_pointer_unavailable` 对 `missing_filename` 误写成复用 `"target_in_subdir"`），执行本计划的人不会被要求做一次「打补丁验红」的动作去确认 TASK-006 写的直接索引断言真能抓住这类坏实现——这类证据缺口不会被记入 `verification-ledger.md`，Phase D 归档/`spec_complete.py --gate` 预演也不会把它列为已知缺口（`TASK-032` 的「已知边界」条目只覆盖 SC-11 谓词矩阵，不含 SC-15）。若实际实现恰好是正确的，此缺口不影响交付；若实现恰好踩中这个坑，测试很可能仍会转红（直接索引对 KeyError 本就敏感），但计划里没有留下"确认过"的证据，与本 Spec 反复强调的「adversarial-fixture：验拒绝能力非当前取值」纪律不一致。

**建议改法**：在 TASK-018 的 SC-15 verification bullet 追加两条（或仿 TASK-035 拆成命名补丁），与已有补丁 4 同等具体度：
- 补丁 5（布局4/5）：把 `degraded_reason = None` 的初始化从「三分派之前」改到只在 `elif n_active == 1:` 分支内部赋值（即 `n_active == 0` 与 `n_active >= 2` 两支不再带该键）⇒ 布局4/5 两处 `result["degraded_reason"]` 直接索引 ⇒ 双 `KeyError` ⇒ 红。
- 补丁 6（布局6）：把 `_render_pointer_unavailable` 返回的 reason 由 `"missing_filename"` 改写为复用 `"target_in_subdir"` ⇒ 布局6 对应断言红。

两条均按 `metadata.hard_constraints` 的三步法记录 GREEN/RED/副本SHA+diff，写入 `verification-ledger.md` 的「GREEN 与反事实」节；工时相应从 TASK-018 现有 4.5h 略增（建议 +1h）。

## 四、核对无误的部分

- 组 2（TASK-009/010/011/012/013/014）全部引用行号在 aria `1cb3872` 上逐一核实，零漂移；TASK-011「删除 `:644`」、TASK-010「`:36`/`:332`/`:494`」等细粒度断言全部精确。
- TASK-018 补丁 4 的三行最小实现，经逐布局推演，红绿模式与计划宣称完全一致（布局1(i)/布局3(j)红，布局2(d)/(e)不受影响）。
- `sc11-predicate-validation.py` 实际执行：`exit=0`，`verdict: OK (mismatch cells 0, stderr notes 0; 24 states x 19 predicates)`，stdout 矩阵与 `--emit-json` 输出的 `states`/`expected`/`predicates`/`matrix` 四个字段与 yaml 对应文本**逐字节比对相等**（含 19 条谓词的独立比对）——R4 M6/M7 的换量修复不仅"看起来对"，是真的在跑且与文档零漂移。
- TASK-029 的 8 步流程（含「回退条」两分支）逐分支用真实 git 仓库验证，四组实验全部与文本描述吻合，未发现语义错误。
- TASK-034 的 `--atomic` / 禁 `--follow-tags` 硬约束，其技术依据经真实推送冲突场景验证成立。
- TASK-031 对 `phase-c-integrator` C.2.5 的转述（触发条件、执行顺序、失败优先级）逐条核对 `SKILL.md:600-643` 原文，全部一致；本仓 `.aria/config.json` 与 `git remote -v` 的实测事实也与计划断言一致。
- `.aria/state-checks.yaml` 中 `m6-version-badge-match:124` / `i18n-readme-translation-currency:177` / `plugin-version-arch-docs-match:408` 三处行号核实准确。
- `test_p1_layer_h.py` 恰好 24 个测试方法，其对 `write_latest_md` 的断言用键级访问而非整字典比较，新增 `degraded_reason` 键不会造成回归，「保持 Ran 24 … OK」可信。
- R4 的 7 Major + 16 Minor 全部在 v5 的 diff 中找到对应改动，未发现「聚合报告说改了但代码没改」的情况。

## Verdict

PASS_WITH_WARNINGS（0 Critical / 1 Major / 0 Minor）

## Vote

REVISE

## 边际判断

1. **组 1–4 是否足以无歧义落地 / 接受当前结论进 Phase B 还有什么风险**：除上述 1 条 Major 外，组 1–4 的代码级设计（含最容易出错的 SC-15 writer 契约、`_dedupe_sort_key` 五级键、git show 失败路径）本席逐行核实均与 aria 实际源码精确对应，无歧义。剩余风险窄且已定位：TASK-018 缺 2 条反事实（布局4/5/6），修法是往 TASK-018 追加两个命名补丁，不涉及架构改动，可在 owner 授权后由主控直接补丁并入 v5，无需整轮返工。除此之外未发现会让实现者需要临场裁决的空白。
2. **若继续加轮，预计能找到什么、值不值两轮成本**：预计再加轮会继续在「深埋在 proposal 细则与 rule6_note 交叉引用中的完整性缺口」这一类上找到 0-2 条同量级的窄缺口（本次这条需要同时核对三份文件——yaml 的 TASK-018、yaml 的 rule6_note、proposal.md 的 SC-15 细则——才能发现，此前四轮均未触及这一交叉路径），但不太可能再发现结构性/架构级问题：组 2/3 代码落点、组 5 的 git 语义与委派机制经本轮大量真实实验验证，均无失实。按 R4 五席「已越过拐点」的共识与本轮的发现量级（1 条窄 Major，修法为局部追加），不值得再投入两轮；更划算的路径是本轮的这条 Major 由 owner 直接授权最小补丁后收尾，而非再开一轮五席审计。
3. **是否有约束写得过细、限制了合理实现**：未发现。git 步骤序列（TASK-029 八步）与 SC-11 谓词的字符级书写规则（`authoring_rules`）表面上很硬，但本席验证过其中最「苛刻」的几条（ff-only 后二次断言、`--atomic` 强制、平衡括号谓词）全部对应过真实复发的坑（本席用真实 git 仓库复现了其中三条），不是凭空加码；`authoring_rules` 的密度确实要求实现者仔细读一遍而非凭直觉写，是文档可用性成本，不是正确性风险。

## 轮次记录

R1 (0C/13M) → v2 → R2 (0C/9M) → v3 → 主控核验返修 → v3.1 → R3 (0C/9M) → v4 → R4 (0C/7M, REVISE 3 / PASS 2) → v5 (本报告对象) → **R5 backend-architect: 0C/1M/0m, PASS_WITH_WARNINGS, vote REVISE**。本席新发现 1 条此前四轮未触及的 Major（TASK-018 SC-15 布局4/5/6 反事实缺口），其余 R4 处置与本席实测范围内的全部技术性声称（git 语义、C.2.5 委派、行号、脚本实跑）均验证通过。
