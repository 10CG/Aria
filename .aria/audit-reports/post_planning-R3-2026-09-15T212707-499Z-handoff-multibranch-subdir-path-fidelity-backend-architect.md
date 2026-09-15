---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T22:27:10.000Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

## 审计结论

### 实读范围

全文读毕: `tasks.md` (159 行)、`detailed-tasks.yaml` (868 行)、`sc11-predicate-validation.py` (341 行)、`post_planning-R2-...-aggregated.md` (335 行, 含全部 9 个 Major 簇处置与 17 条 Minor)、`proposal.md` SC 表 :415/:417/:418/:419/:422/:429/:432 七行 (python 按行切片读)。未读同轮其他席位 R3 报告, 未读 R2 个人席位报告 (仅按要求读聚合报告)。

对照代码: `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` (755 行, 全文或分段读: 1-120 / 160-300 / 300-440 / 439-500 / 580-720)、`scripts/scan.py` (175-214)、`scripts/writers/latest_md_writer.py` (1-175 / 255-320)、`tests/test_scan_integration.py` (160-200)、`tests/test_handoff_multibranch_collision_dedupe.py` (地址核验)、`tests/test_max_branches_resolver.py` (284-334)。全部核对基线 = aria `1cb3872` (v1.73.3), 与子模块状态一致。

### 实跑命令与关键输出

1. **sc11-predicate-validation.py 实跑** (仓库根, 只读):
   ```
   python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py
   ```
   退出码 0, stderr: `verdict: OK (mismatch cells 0, stderr notes 0; 13 states x 19 predicates)`, stdout 矩阵与 yaml `metadata.sc11_predicate_validation.measured_2026_09_15_at_1cb3872_v3_1` 逐字节一致 (13 态 × 19 谓词全部核对, 非抽样)。追加两项自证: (a) `python3 -B -OO` 重跑, 退出码同为 0 且 stdout 与非 -OO 版逐字节相同 (脚本自称用 `ast.parse` 重读 docstring 而非运行时 `__doc__`, 实测在 `-OO` 剥离 docstring 的条件下仍成立); (b) `grep -n '^\s*assert \|[^.]assert('` 对脚本全文零命中, 确认脚本自称「不依赖 assert」属实; (c) `ls /tmp | grep -c sc11-validate-` 为 0, 确认 `finally: shutil.rmtree` 清理生效, 无残留临时目录。
2. **单元测试基线复跑** (`aria/skills/state-scanner/tests` 下, 只读):
   - `python3 -B -m unittest test_handoff_multibranch_collision_dedupe -v` → `Ran 23 tests ... OK` (与 TASK-014/016 引用值一致)
   - `python3 -B -m unittest test_scan_integration -v` → `Ran 19 tests ... OK` (与 TASK-010 引用值一致)
   - `python3 -B -m unittest test_p1_layer_h -v` → `Ran 24 tests ... OK` (与 TASK-013 引用值一致)
   - `python3 -B -m unittest test_max_branches_resolver -v` → `Ran 39 tests ... OK`; 并读 `:284-334` 确认四处 mock 均为 `mock.patch.object(hmb, "_list_handoff_files", return_value=([], None))` 全量替换式 mock (非签名绑定式), 不受 TASK-009 新增 `reporter` 默认参数影响
3. **`_dedupe_sort_key` 第 5 级键语义实验** (`/tmp/.../scratchpad/r3-backend-architect/test_dedupe_key.py`, 复刻 TASK-014 字面实现): 顶层行 vs 子目录行, 正反序都选顶层 (`(True,'x.md') > (False,'archive/x.md')`); 两个子目录行, 正反序都选字典序大者 (`'archive/x.md' > 'old/x.md'` 为 False ⇒ 选 `old/x.md`, 与 TASK-005 夹具期望「两种顺序都选 old/x.md」一致); 缺 `rel_path` 键时 `rel=filename` 不抛异常。三项均 PASS。
4. **TASK-035 补丁 1 (SC-1) 反事实实验** (`/tmp/.../scratchpad/r3-backend-architect/sc1-patch1-experiment/`, 真实 git 仓 + `simulate_collector.py`): 建仓一份 `docs/handoff/archive/2026-05-09-session-end.md` (合法 frontmatter, 从未在顶层存在), `git update-ref refs/remotes/origin/master <sha>`。TARGET 模拟 (TASK-009+011 正确实现) 产出 `tracks=[{legacy:False, rel_path:'archive/2026-05-09-session-end.md'}]`, `unreadable_count=0`。PATCH 1 模拟 (枚举退回 basename, TASK-011 不变) 产出 **`tracks=[]`, `unreadable_count=1`, error kind=`handoff_multibranch_git_show_failed`** —— 而非 proposal 原句「该行变 legacy」。独立用真 git 命令复核: `git show origin/master:docs/handoff/2026-05-09-session-end.md` → `fatal: path 'docs/handoff/2026-05-09-session-end.md' does not exist in 'origin/master'` (rc=128)。详见 finding 1。
5. **TASK-035 补丁 3 (SC-4 后半) 反事实实验** (`/tmp/.../scratchpad/r3-backend-architect/sc4-patch3-experiment/`): 建仓一份无 frontmatter、从未在顶层存在的 `docs/handoff/archive/2026-06-01-x.md`。`git log -1 --format=%aI origin/master -- docs/handoff/archive/2026-06-01-x.md` 正常返回日期; 改用错误的 basename-only 路径 `docs/handoff/2026-06-01-x.md` → `stdout=[] rc=0` (空但不失败, 与 `_get_file_commit_date` 的 `if rc != 0: return ""` 配合, 实际返回空串); 同时 `git show origin/master:docs/handoff/archive/2026-06-01-x.md` (内容读路径未受补丁 3 影响) 仍正常返回内容。confirms 补丁 3「只此一处」的窄化确实只影响 `updated_at` 字段, 不引发 git show 失败, 精确命中 SC-4 后半的目标断言 (updated_at 非空)。

### R2 处置落地核验 (本席侧重相关项)

| R2 编号 | 处置内容 (摘要) | 落地判定 | 证据 |
|---|---|---|---|
| PP2-M1 | TASK-019/020/023 补依赖边 TASK-033; TASK-033 核验改为四路径 `add` + 提交后 porcelain 为空; TASK-018 从「工作树前后一致」改为「副本生命周期证据」 | 落地 | yaml:537,558,619 `dependencies` 含 `TASK-033`; yaml:427-431 TASK-033 核验第一条为四路径 add + porcelain 为空; yaml:495-501 TASK-018 verification 首行即「副本生命周期证据 (取代...)」 |
| PP2-M3 | TASK-019/020/023(aria 侧)/024/026/030 各补「由主控在 …feature 分支提交, 只 add 本任务 deliverables, 提交 SHA 记台账」; TASK-021 回归前记两仓 porcelain 为空 + HEAD SHA; TASK-029 合并树回归改「干净工作树原位跑」而非 worktree 副本; TASK-031 开 PR 前 porcelain 为空 (有范围) + `git ls-files` | 落地 | yaml:548,571,631,649,705,822 六处提交点原文俱在; yaml:585 TASK-021 首条; yaml:775-777 TASK-029 第 7 步 + notes 显式引用 PP2-M3; yaml:837-838 TASK-031 两条 |
| PP2-M6 | TASK-027 记取号时 SHA; TASK-029 fetch 后前进则重算取号, 合并后核 5 文件 + 两远端无同名 tag 不符则回退重取号; TASK-034 推前再查同名 tag | 落地 | yaml:724 TASK-027; yaml:770-774 TASK-029 第 3/6 步; yaml:793 TASK-034 首条 |
| PP2-M9 | 全部 proposal SC 表反事实改在组 3 按三步法「只回退该组件」实跑, 新编号 TASK-035 (不复用旧号); TASK-007 删「RED 即反事实」标注; TASK-011 删 SC-14 中间态反事实条 | 落地 (但组件内部见 finding 1) | yaml:503-524 TASK-035 独立存在, 编号未复用; yaml:284 TASK-007 verification 第 3 条; yaml:362 TASK-011 notes 显式回指 PP2-M9 |
| m1 | TASK-020 `_dedupe_sort_key` docstring 区间 `:429-452`→`:429-453` | 落地且经代码核实**行号确实止于 453** | yaml:560; 本席直读 `handoff_multibranch.py:428-455`, docstring 恰为 429-453 (454 起为函数体) |
| m16 | TASK-021 冻结语料 diff 检查拆成两条分仓命令 (超级仓对子模块路径恒 0 行的陷阱) | 落地 | yaml:590 两条独立 `git -C aria diff` / `git diff` 命令, 各自基线 SHA 取自 TASK-001 台账 |
| PP2-M7/M8/m9/m11/m14/m15 (验证脚本口径) | 脚本改全矩阵核验 + try/finally 清理; (a2) 定位反引号形状 dict; (j2)/(j3) 锚点处置; (j4) 同义词扩面; (k) 收紧为字面; (l1) 补 Scenarios 段 | 落地, 已实跑复核 (见上「实跑」第 1 项) | 13 态×19 谓词矩阵 rc=0 逐字节match; `shutil.rmtree` 在 `finally` 内 (脚本 :319-320); 13 个坏态 (`bad_*`/`alt_j3_anchor`) 覆盖 m9/m11/m14/m15 各条 |

**本席侧重相关的 R2 处置全部已落地**; PP2-M9 的「统一走三步法」这一上位处置确实落地 (TASK-035 存在且结构正确), 但其内部对六个补丁的「只回退该组件」窄化推演在补丁 1 上不完整, 见 finding 1 (这是 v3 新写内容内部的问题, 不是 R2 处置未落地)。

### 实施者试派生 (只看该 TASK 与其引用文件)

1. **TASK-009** (`_list_handoff_files` 枚举层): 依据 `:177-178`(常量)/`:240-290`(函数)/`:619-626`(主循环调用点), 逐行核对与真实代码字节对齐 (含罕见的「:177 注释与 :178 无斜杠值不一致」这个预先存在的 bug, TASK-009 明确要求顺手修正)。核验条款「签名保持 2-tuple, 新增带默认值的 reporter」与 `test_max_branches_resolver.py` 的 4 处全量替换式 mock 兼容, 已实跑确认 (见上)。**无卡点, 可无歧义执行。**
2. **TASK-011** (git show 失败处理 + unreadable_count 三类外延): 依据 `:637-658`(主循环 git-show-失败分支)/`:586-596`(fail-soft 早退 dict)。逐行核对与真实代码一致。**发现一处未言明的收尾细节** (见 finding 2, Minor): `:644` 的 `fallback_date = _get_file_commit_date(...)` 调用在新实现下变成死代码 (其结果只曾被移除的 `tracks.append(...)` 消费), 核验条款未显式要求删除, 但也不影响任何断言 (`_get_file_commit_date` 对任何失败都 fail-soft 返回空串, 不抛异常)。
3. **TASK-013** (`latest_md_writer.py` 全部契约面): 依据 `:30-35`/`:110-148`/`:124`/`:151-169`/`:259-320`/`:277-290`(Returns)/`:287-290`(Scenarios)/`:303`/`:159`。全部行号逐字核对命中 (含 `write_latest_md` 唯一调用点 `:303` 与 sc11 脚本 `code_changes()` 的 `rep()` 锚点逐字符一致)。`_render_pointer` 内部如何新增 "rel != filename ⇒ 走 unavailable 分支" 未给出精确签名 (是否给 `_render_pointer_unavailable` 加 `reason` 参数), 但受约束的输出契约 (两处 docstring 须逐字含 `target_in_subdir`、返回 `(content, reason)`、`reason` 三态) 已经把实现空间收得足够窄, 判断**不构成阻断级歧义**, 是合理的技术裁量范围。**发现一处次要文案缺口** (见 finding 3, Minor): `:159`「仅在单 active track 场景下写真实指针」句在 `_render_pointer` 内 `:140` 有逐字相同的副本, TASK-013 只点名 `:159` 补子目录限定。
4. **TASK-014** (`_dedupe_sort_key` 第 5 级键): 依据 `:428-455`。字面实现与语义描述 (顶层优先 / 子目录内字典序取大 / 缺键按 filename 处理不抛异常) 经独立 Python 实验三项全部证实为真 (见上「实跑」第 3 项)。核对 `_dedupe_sort_key` 唯一消费点 `:541 max(rows, key=_dedupe_sort_key)`, 无其它调用方或测试直接解包该元组, 返回类型从 4 元组扩到 5 元组不破坏任何既有签名依赖。**无卡点, 可无歧义执行, 且已独立证实正确。**
5. **TASK-029** (子模块本地合并 + tag + 回归, 不推送): 8 步顺序逐条核对。Step 6 回退子程序的前置 (`HEAD^1`/`HEAD^2` 精确核对 + porcelain 为空) 与命令 (`checkout master` 后 `reset --hard <step-2 记录 SHA>`, 不读可能已被后续 fetch 推进的 `origin/master`) 语义正确: `--no-ff` 产生的合并提交 `HEAD^1` 确为合并前 master tip、`HEAD^2` 确为被合并分支 tip, 是标准 git parent 语义, precondition 检查可防止在错误状态上盲目 `reset --hard`。**核实执笔人自报存疑点**「TASK-029 第 2 步的 checkout master 早于第 4 步的干净工作树断言」: 推演两种后果 —— (a) 若 checkout 前工作树已脏且与 master 冲突, `git checkout master` 本身会报错拒绝切换 (安全, 阻断在 checkout 处); (b) 若不冲突, `checkout` 会静默带过脏改动, 但第 4 步的 `status --porcelain` 断言会在真正执行 merge (第 5 步) 之前拦下来。两条路径都在「危险操作 (merge/reset)」之前被拦截, **判定为低风险, 已被下游步骤兜底, 不构成独立 finding**。
6. **TASK-035** (proposal SC 表反事实, 三步法只回退该组件): 六个补丁逐个对照代码推演, 详见「实跑」第 4/5 项。**补丁 1 (SC-1) 存在卡点**, 见 finding 1 (Major)。补丁 2/3/4/5/6 经推演 (补丁 3 另经实验证实) 判定命中目标断言, 无卡点。

### Findings

**Finding 1 — [Major] type=risk · category=testing · scope=TASK-035 补丁 1 (SC-1 部分) · v3 引入: 是**

证据: `detailed-tasks.yaml:516` 补丁 1 描述「枚举层退回 basename: `_list_handoff_files` 产出 basename, 其余不动」, 供 SC-1 (`test_subdir_file_read_as_real_track`) 与 SC-17 共用; `:516` 声称「SC-1 所指断言 = proposal 原句「该行变 legacy + 该 kind 出现 ⇒ 全红」覆盖的该用例全部断言」。本席在真实 git 仓上复刻 TASK-009 (枚举返回 rel_path) + TASK-011 (git show 失败 ⇒ soft_error + `unreadable_count+=1`, **不**追加 legacy 行) 的目标实现, 对 SC-1 的具体夹具 (`docs/handoff/archive/2026-05-09-session-end.md`, 从未在顶层存在, 合法 frontmatter) 应用补丁 1: 实测 `_read_file_content` 重构路径 `docs/handoff/2026-05-09-session-end.md` (丢失 `archive/` 前缀) 后 `git show` 以 rc=128 失败 (`fatal: path ... does not exist`); 由于 TASK-011 的修复未被回退 (补丁 1 只动枚举), 该失败走的是**新**逻辑分支——不追加 legacy 行、`unreadable_count += 1`——最终 `tracks == []`, 而不是 proposal 原句所指「该行变 legacy」。

照计划执行会出的错: TASK-035 本身的方法论要求「逐 SC 记下 unittest 原样输出中的失败断言文本, 并写明它落在 proposal 该 SC 反事实原句所指的哪一条断言上」, 且已有安全阀「首个失败断言不属原句所指...⇒该次运行不算该 SC 的反事实证据: 缩小补丁到只回退该组件后重跑」。但按本仓既有测试惯例 (`test_handoff_multibranch_collision_dedupe.py:284-289` 明确以 `len(data["tracks"])` 作为「schema-additive contract pin」放在断言序列最前), SC-1 的测试大概率会先断言 `len(tracks)==1` 之类的存在性, 在补丁 1 下必定先红在「行整体消失」而非「行退化为 legacy」。这与 TASK-035 自己给补丁 3 / 补丁 5 的处理形成不一致: 该任务的 notes 字段 (`:524`) 已经明确写出「TASK-011 落地后枚举退回 basename 会让该行因 git show 失败直接消失, 首个失败断言落在行存在性上, 不是原句所指的...」这个**完全相同的因果链**, 并据此把补丁 3 / 5 从「回退整个枚举」窄化为「只回退单个字段的取值来源」——但补丁 1 (SC-1 使用的那份) 恰恰就是被那条 notes 点名要避免的「回退整个枚举」形态, 没有被同样窄化。执行者大概率会在 TASK-035 执行阶段重新踩一遍已经被踩过、且被记录过解法的坑, 需要临场把补丁 1 (至少 SC-1 的部分) 重新窄化为类似「只在 TrackEntry 构造点把 `rel_path` 退回 basename, 枚举与 git show 读取路径不动」的形态 (与补丁 5 同构), 才能让首个失败断言落在 proposal 原句所指的 `rel_path`/`legacy` 字段上。SC-17 因为涉及两条不同 owner_container 的行、其目标断言 (`collision.kind`/`len(groups)`/有无 `git_show_failed`) 恰好会随「archive 行整体消失」同向翻转, 本席推演认为大概率不受此问题影响 (未独立起夹具验证, 置信度低于 SC-1 部分)。

建议改法: 补丁 1 拆分为二: SC-17 继续用「枚举退回 basename」(消融式验证 owner_container/collision 三项即可, 该三项确实会因行消失而翻转); SC-1 单独换成按补丁 3/5 同款「只回退该组件」的窄化形态——例如只把 SC-1 用例里 TrackEntry 构造时写入的 `rel_path` 字段值退回 basename, 保持枚举与 `_read_file_content` 使用真实 rel_path (即与补丁 5 同构, 只是换一个 TrackEntry 构造分支)——使首个失败断言精确落在 `rel_path == "archive/2026-05-09-session-end.md"` 或 `legacy == False` 上。

**Finding 2 — [Minor] type=issue · category=documentation · scope=TASK-011 · v3 引入: 否 (v1 起即缺失, 各轮均未点名)**

证据: `handoff_multibranch.py:644` `fallback_date = _get_file_commit_date(project_root, branch, filename)` 位于 `:637-658` 的 git-show-失败分支内; TASK-011 (yaml:345-362) 要求该分支「不追加 legacy 行」, 但未提及是否删除本行。

照计划执行会出的错: 若实现者原样保留 `:644`, `fallback_date` 的计算结果不再被任何代码消费 (原消费者 `tracks.append({...})` 已按 TASK-011 移除), 成为死代码; 因为 `_get_file_commit_date` 对任何失败一律 fail-soft 返回空串 (`if rc != 0: return ""`, 已实验证实不抛异常), 不会导致任何断言变化或崩溃, 纯属多余的一次 `git log` 子进程调用与可读性问题。

建议改法: TASK-011 verification 补一条「同批删除 `:644` 已失去消费者的 `_get_file_commit_date` 调用」, 或在 notes 里显式记「保留亦不影响正确性, 交实现者自行取舍」以避免歧义被误读为遗漏。

**Finding 3 — [Minor] type=issue · category=documentation · scope=TASK-013 · v3 引入: 否 (v1 起即缺失)**

证据: `latest_md_writer.py:140` (`_render_pointer` 渲染的真实指针正文内) 与 `:159` (`_render_pointer_unavailable` 降级正文内) 两处存在逐字相同的句子 `"> 自 v1.22.x 起,本 pointer 仅在**单 active track** 场景下写真实指针;"`。TASK-013 (yaml:381-396) 只点名 `:159`「补子目录限定」, 未提 `:140`。

照计划执行会出的错: 新增子目录降级场景后, 该句在「单 active track 但目标在子目录」的情形下已不再精确 (需要「单 active track **且不在子目录**」才写真实指针) —— 这个不精确同样存在于 `:140` 版本的措辞 (虽然 `:140` 只在真正写出真实指针、即 `rel==filename` 已确认成立时才被渲染, 故不会对读者产生该次渲染内的误导, 但该句作为「本系统的通用规则说明」在两处均出现, 仅改一处会造成同一份文档两处对同一规则的表述不同步)。不影响任何 SC/断言 (无机器可判定的判据挂在这句文字上), 纯属内容一致性问题。

建议改法: TASK-013 verification 增补 `:140` 是否同步改写的判断 (或显式记录「`:140` 因只在 rel==filename 成立时渲染, 保持原句不算错误, 不改」), 避免执行者遗漏后产生的不同步被误判为疏漏。

### 核对无误的部分

- **组 2 行号精度**: TASK-009 (`:177-178`/`:240-290`/`:619-626`)、TASK-010 (`:301`/`:321`/`:329-336`/`:332`/`:665-676`/`:683-698`/`:686`/scan.py `:180`/`:186`/`:193`/`:209`/test_scan_integration.py `:164-166`)、TASK-011 (`:586-596`/`:637-658`)、TASK-012 (`:586-596`)、TASK-013 (`:30-35`/`:110-148`/`:124`/`:151-169`/`:259-320`/`:277-281`/`:287-290`/`:303`/`:159`)、TASK-014 (`:428-455`)、TASK-020 (m1 修正后的 `:429-453`) 逐一对照真实代码, **全部逐字节命中, 零偏差**, 包括若干非平凡细节 (如 `:177` 注释与 `:178` 值的既存不一致、`:140`/`:159` 重复句、scan.py `:186` 单行拼串点)。这一精度水平明显高于典型规划文档, 是本次核验的一个突出优点。
- **TASK-033 提交范围闭合性**: 独立核对 TASK-009~014 六个任务触及的文件并集, 恰为 `handoff_multibranch.py` / `scan.py` / `latest_md_writer.py` / `test_scan_integration.py` 四个路径, 与 TASK-033 声明的「只对组 2 的四个具体路径 add」精确重合, 无遗漏也无多余。
- **sc11-predicate-validation.py**: 13 态 × 19 谓词矩阵实跑 0 差异; `-OO` 下行为不变 (docstring 靠 `ast.parse` 重读, 不依赖运行时 `__doc__`); 全文零裸 `assert`; `finally` 块清理临时目录经验证确实生效; `code_changes()`/`writer_docs()`/`collector_docs()` 的多处 `rep()` 锚点原文逐字符核对与仓内真实代码一致。
- **TASK-014 语义**: `max()` 下 `(True, rel)` 恒胜 `(False, rel)`、子目录间取字典序大者、缺 `rel_path` 键按 filename 处理不抛异常, 三项均经独立 Python 实验证实; 唯一消费点为 `:541` 的 `max(rows, key=_dedupe_sort_key)`, 无其它调用方受 4→5 元组扩展影响。
- **TASK-029 / TASK-034 git 语义**: 8 步内部顺序 (fetch → 对齐记 SHA → 取号复核 → 干净工作树 → 本地合并 → 取号终核+两远端查 tag → 合并树回归(有前提) → 打 tag) 自洽; Step 6 回退子程序的 precondition (`HEAD^1`/`HEAD^2` 精确匹配) 与 `reset --hard <已记录 SHA>` (非读可能漂移的 `origin/master`) 命令语义正确, 符合标准 git merge parent 约定; TASK-034 推送前重新用 `ls-remote` (非本地 ref, 天然规避「未 fetch 即测」陷阱) 复核同名 tag, 复用 TASK-029 同一套回退前置/命令而非另造一套。
- **R2 的 PP2-M1/M3/M6/M9/m1/m16 与验证脚本相关的 6 个簇 (PP2-M7/M8/m9/m11/m14/m15)**: 均已落地, 见上表, 逐条附 file:line 证据。

## Verdict

PASS_WITH_WARNINGS (0 Critical, 1 Major, 2 Minor)

## Vote

REVISE

## 轮次记录

本轮为 post_planning R3 (max_rounds 5 的第 3 轮), 本席为本轮新派席位, 未参与 R1/R2; 聚焦「组 2 行号与代码落点 / TASK-014 第 5 级键语义 / TASK-035 六补丁的反事实鉴别力 / TASK-029 与 TASK-034 的 git 语义」四项。R2 聚合报告点名的、与本席侧重相关的处置 (PP2-M1/M3/M6/M9/m1/m16 及验证脚本 6 簇) 经本席独立核对 (含实跑 sc11 验证脚本、四个既有 unittest 模块、两个真实 git 仓反事实实验) 全部确认落地; 但在核验 PP2-M9 新落地的 TASK-035 内部时, 发现其六个补丁中补丁 1 (SC-1 部分) 未套用该任务自身 notes 字段已经对补丁 3/5 明确写出的「只回退该组件」窄化逻辑, 属 v3 新写内容内部的一致性缺口 (Major), 另有两处次要文档完整性缺口 (Minor, 均为 v1 起存量、各轮未点名)。
