---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-16T00:14:00.479Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 — backend-architect 席位报告

本席为 R4 新派席位, 未参与 R1–R3。审计对象: 主仓 master `edd256d` (本地, 未推送) 下的 `tasks.md` / `detailed-tasks.yaml` / `sc11-predicate-validation.py`。侧重: 组 2 (TASK-009..014 / TASK-033) 行号与代码落点、TASK-035 六个补丁、git 语义 (TASK-029 / TASK-034 / TASK-032)。

## 审计结论

### 实读范围

- 三份审计对象全文 (`tasks.md` 168 行、`detailed-tasks.yaml` 全文、`sc11-predicate-validation.py` 全文)。
- `post_planning-R3-2026-09-15T212707-499Z-...-aggregated.md` 全文 (未读同轮 R4 其余席位报告, 未读 R3 五份分席报告)。
- `git diff 2b9cb3e edd256d -- openspec/changes/handoff-multibranch-subdir-path-fidelity/` 三份文件全量 diff (tasks.md 34 行、yaml 144 行、sc11 脚本 93 行)。
- aria `1cb3872` 实际代码: `handoff_multibranch.py` 全文相关区段 (:170-182 / :240-340 / :428-456 / :580-702)、`latest_md_writer.py` 全文相关区段 (:1-50 / :95-170 / :255-320)、`scan.py` 与 `test_scan_integration.py` 未逐行读 (未落在本席侧重面, 行号已由 R3 backend-architect / knowledge-manager 两席字节级核对且本轮 diff 未触及其行号)。
- proposal.md SC 表 `:415` `:417` `:418` `:419` `:422` `:429` `:432` (python 按行切片读取, 避免长行截断)。
- `references/session-handoff.md` (standards `8b49562`) 基线内容, 用于核验 TASK-029 新增占位检查的自然负控假设。

### 实跑命令与关键输出

1. `git show --stat ec72175` (aria) — 核验 TASK-029/034 引用的「先例指针」实际内容。
2. 临时仓实验 (`/tmp/.../scratchpad/r4-backend-architect/git-exp1`, 已清理): 构造一个只存在于 `docs/handoff/archive/` 下、从未在顶层出现过的 handoff 文件, 直接对 `origin/master:docs/handoff/<basename>` 取 `git show`:
   ```
   fatal: path 'docs/handoff/2026-05-09-session-end.md' does not exist in 'origin/master'
   exit code (should be non-zero): 128
   ```
   对照组 `git show origin/master:docs/handoff/archive/2026-05-09-session-end.md` 成功读出正文, exit 0。用于独立核验 TASK-035 补丁 1 的「现表现形态」改写 (见下)。
3. 临时仓实验 (`/tmp/.../scratchpad/r4-backend-architect/push-exp`, 已清理): 构造一个远端 master 已分叉的裸仓, 分别实跑
   - `git push origin master v9.9.9` (多 ref 非原子) → master 被拒, **tag 仍发布** (`ls-remote` 证实);
   - `git push origin master --follow-tags`(annotated tag, 与 aria 实际发布 tag 同型 —— `git for-each-ref --format='%(refname) %(objecttype)' refs/tags` 核实 aria 现有 tag 均为 `tag` 类型即 annotated) → master 被拒, **tag 仍发布**;
   - `git push --atomic origin master refs/tags/v9.9.9` → 两者**同拒**, `ls-remote` 确认远端无变化。
   三态结果与 TASK-034 verification 第 2 条文字逐字一致。
4. `python3 -B openspec/changes/handoff-multibranch-subdir-path-fidelity/sc11-predicate-validation.py aria/skills/state-scanner --emit-json`(`TMPDIR` 指向 scratchpad 子目录) — 退出码 0, stderr `verdict: OK (mismatch cells 0, stderr notes 0; 18 states x 19 predicates)`。
5. 用第 4 步的 `--emit-json` 输出, 写 python 脚本逐字节比对 `predicates` 字段与 yaml `metadata.sc11_baseline_predicates` 的 19 条 `(label)` 行 → `RESULT: BYTE-IDENTICAL, full match`。用于核验 R3 m11 处置 (谓词双源一致性核验) 是否真落地且可执行。
6. 负控: `python3 -B sc11-predicate-validation.py /nonexistent-dir-xyz` 与 `... .`(主仓根, 缺 `FILES` 清单文件) 均返回退出码 2 并打印 usage + 缺文件清单, 核验 R3 m10 处置。
7. `grep -c '#<' standards/conventions/session-handoff.md`(基线 `8b49562`) → 0。用于核验 TASK-029 新 Step 2 占位检查的「自然负控」假设 (TASK-023 落笔后应为 1, TASK-025 回填后应为 0) 在基线上确实不会误报。

### R3 处置落地核验 (本席侧重相关项)

| R3 编号 | 内容 | 落地判据 | 核验结果 |
|---|---|---|---|
| PP3-M8 (本席 F1) | TASK-035 补丁 1 在 TASK-011 后使 SC-1 行消失而非「变 legacy」 | `TASK-035` 补丁 1 条款是否写明现表现形态且不窄化 | **落地**。yaml :532-533「补丁不窄化…SC-1 原句…现表现为『该行不在 tracks[] + 该 kind 出现 + unreadable_count == 1』」——与本席本轮独立实跑 (见上「实跑」第 2 条) 结论一致 |
| m15 (本席 F2) | TASK-011 应同批删 `:644` 的 `_get_file_commit_date` 死调用 | 代码 :644 确为该调用且 yaml 有对应条款 | **落地**。真实代码 :644 = `fallback_date = _get_file_commit_date(project_root, branch, filename)`(git-show-失败分支内), yaml TASK-011 verification 第 4 条逐字要求删除 |
| m16 (本席 F3) | `:140`/`:159` 重复句只点名一处 | 代码两处确为逐字重复且 yaml 两处同改 | **落地**。真实代码 `grep -n` 命中两行 (:140, :159, 逐字相同), yaml TASK-013 verification 第 4 条「两处同批补子目录限定」 |
| PP3-M2 (TL M2, 本席上轮误判「非 finding」) | TASK-029 占位检查在 master 工作树上对未回填态恒真 | 检查是否移到 checkout 之前 且改为读 feature 分支提交内容 | **落地且加固**。新 Step 2「早于任何 checkout」+ 用 `git -C standards show <feature 分支>:...\| grep -c` 直接读提交内容 (不依赖当前 checkout 在哪个分支), 比单纯挪到 checkout 前更彻底; 基线 `grep -c '#<' session-handoff.md` = 0 (见「实跑」第 7 条), 证实自然红态假设成立 |
| PP3-M3 (取号被占必冲突) | 需 fail-closed + 先例指针, 不展开自动恢复 | owner_gates / Step 4 文本 | **落地**。Step 4 停下上报 + 指针 `aria ec72175`; 核实 `ec72175` 实际内容 (见「实跑」第 1 条) 同时覆盖版本重算与真实合并冲突解决两类场景, 指针选取准确 |
| PP3-M4 (TASK-034 孤儿 tag) | 推送写法须写死为 `--atomic`, 禁 `--follow-tags`/多 ref | verification 第 2 条 | **落地且经本席独立实验证实** (见「实跑」第 3 条三态结果) |
| PP3-M5 (AB delta 符号反) | 删 WITHOUT_BETTER, delta 公式写死 | TASK-026 / owner_gates / rule6_note / tasks.md 5.5 | **落地**。四处 `WITHOUT_BETTER` 引用均改为逐 eval 回归判据, delta 公式写为 `mean(with) − mean(old)` 并注明官方脚本符号相反的规避写法 |
| PP3-M7 (j1/j2/j3 不钉元组) | 三条谓词改判「现状键元组」, 新增负控态 | 脚本 + yaml 全同步且三态验证矩阵含新态 | **落地且经本席实跑全量验证** (见「实跑」第 4/5 条): 19 谓词 × 18 态含 4 个新 `bad_*` 态与 1 个新 `alt_*` 态, 实测矩阵 0 差异 |
| m1 (owner_gates 完整性) | 两类协调 ref 推送口径统一, 8 项补处置句 | owner_gates 列表逐条含「未获授权 ⇒」 | **落地**(抽查 TASK-026/034/031/032 各条均已补) |
| m3 (TASK-035 补丁3 副本复用冲突) | 改为「diff 可相同但各自独立副本」 | TASK-035 补丁 3 条款 | **落地**, 措辞与 TASK-017 侧对称一致 (TASK-017 无需反向声明, 因 TASK-035 在其后) |
| m4 (TASK-032 缺 ff-only 对齐) | 补开头对齐步骤 | TASK-032 verification 第 1 条 | **落地**, 断言改用 `git merge-base --is-ancestor` 比 R3 处置文字描述的更严格 |
| m5 (主仓合并策略未写死) | merge 不 rebase, merge commit 不 squash | TASK-031 verification | **落地**, 并含「合并后核台账所记 SHA 均为 origin/master 祖先」的可执行核验 |
| m6 (TASK-027 提交点缺细节) | 补分支/add范围/SHA 核验 | TASK-027 verification 末条 | **落地** |
| m11 (谓词双源一致性无核验) | `--emit-json` 加 `predicates` 字段 + TASK-001/029 加比对步骤 | 脚本 + TASK-001 + TASK-029 第 7 步 | **落地且经本席实跑证实可执行** (见「实跑」第 4/5 条, byte-identical) |
| m13 (TASK-001 缺基线检出断言) | 补 HEAD/porcelain 断言 | TASK-001 verification | **落地** |
| m14 (unittest cwd / --repo-root 缺失) | 统一写 `cd .../tests && python3 -B -m unittest`, `check_bare_issue_refs.py` 补 `--repo-root` | 全文搜索 | **落地**(TASK-001/007/010/033 等 unittest 命令与 TASK-028 均已改) |

未在本表列出的 R3 簇 (PP3-M1/M6/M9 及全部 Minor 中与组 2/TASK-035/git 语义无关者) 不在本席核验范围, 留给对应侧重席位。

### 实施者试派生

只看该任务自身文字与其引用文件, 判断能否无歧义执行:

1. **TASK-011**(`git show 失败只报 soft_error…`): 无歧义。四条 verification 逐条可执行 (kind 字面量 / 不追加行 / `chr(0xFFFD)` 判据字面量 / 删 `:644` 调用), 且 `:637-658` 恰是需要整体重写的那个 if 块, 删除 `:644` 调用其实是该重写的自然结果, 单独列出只是提醒, 不构成两处独立编辑点的歧义。
2. **TASK-013**(pointer 写侧守卫): 契约面 (返回值集合 / 三态恒带键 / 两处 docstring 逐字 `target_in_subdir`) 无歧义, 均可由 SC-11 (k)(l1) 机械核验。唯一留给实现者裁量的是 `_render_pointer_unavailable` 内部如何按「missing_filename / target_in_subdir」两种原因分派渲染文案 (现签名 `(track_id, now)` 不带 reason 参数, 需要实现者自己加参数或等价机制) —— 但这是函数内部实现细节, 不被任何 SC 或 SC-11 谓词钉死具体机制, 不影响能否执行, 只是正常的「留白」。
3. **TASK-014**(排序键第 5 级): 无歧义, 返回语句字面已给出, 与真实代码 `:454-455` 对照后只需追加一个元素, 「前四级不动」在真实代码里就是字面意义上的不动。
4. **TASK-029**(子模块合并 8 步): 8 步各自的前置/动作/失败分支/记录项均写明, 步与步之间的前置传递关系本席逐条核对无缺口 (见下「跨簇一致性」复核)。唯一实施者需要自行补一步的地方: Step 2 「不成立 ⇒ 停下…提交…」之后没有显式写「重新核验 porcelain 为空再进入 Step 3」——一个谨慎实现者会自然这样做, 但文字本身没有闭合这个循环 (计入 finding, 见下)。
5. **TASK-034**(推送): 无歧义, 命令字面 (`git push --atomic <remote> master refs/tags/v<vNEXT>`) 经本席实验证实行为符合描述, 三种失败态 (被拒/半推/tag 碰撞) 处置路径均可在 `owner_gates` 或指向 TASK-029 第 6 步回退中找到, 唯一未独立成条的是「TASK-034 pre-push tag 碰撞」场景, 但该场景显式复用 TASK-029 第 6 步回退程序, 不构成缺口。
6. **TASK-035 六补丁**: 补丁 1/4/6 无歧义(字面清楚, 本席对补丁 1 做了独立实跑)。补丁 2/3/5 无歧义, 且补丁 3 与 TASK-017、补丁 5 与 SC-8 的关系均有交叉引用, 未发现悬空引用。

跨簇一致性复核 (针对 R3 聚合报告「跨簇一致性」条目 2, 逐条复核): TASK-029 步 1→8 每步前置在上一步结束时成立 (含 Step 4/5/6 的三条 fail-closed 分支均能在 `metadata.owner_gates` 找到对应条目); 回退条 (`HEAD^1`/`HEAD^2`/porcelain 干净) 的前置只在「Step 5 成功产生合并提交」时才被调用, Step 5 本身冲突 (无合并提交) 时明确走 `merge --abort` 而非回退条, 与 R3 的要求完全一致。全文搜索 `TASK-029` 交叉引用 (`tasks.md` 5.2 行、TASK-034 首条、metadata.owner_gates) 均已同步为新的步序编号 (第 3/4/6 步), 未发现遗留旧编号引用。

### Findings

1. `[Minor] type=risk · category=implementation · scope=TASK-029(detailed-tasks.yaml) · v4 引入: 部分`

   **证据**: yaml TASK-029 verification 第 2 条 (Step 2):「不成立 ⇒ 停下, 查明归属后在对应 feature 分支提交 (只 add 被改文件) 或上报, 不 stash、不带着改动切分支」。
   - 与 `metadata.owner_gates` 对照: `owner_gates` 中仅有「TASK-029 · 停下上报 (罕见并发路径一律 fail-closed) · 取号被占 (第 4 步) / 合并冲突 (第 5 步) / 取号终核不符 (第 6 步) …」一条, 未覆盖 Step 2 的「工作树不干净」停下分支。
   - Step 2 文字本身也没有闭合「本地提交后回到 Step 2 重新断言 porcelain 为空, 再进入 Step 3」这一句, 只隐含在「或上报」的对立分支里。

   **照计划执行会出的错**: 不会导致错误结果 (本席判断: 这是「先查明归属再本地提交」的自愈路径, 属只读、可逆、不外向的本地操作, 不属于 R4 处置原则 1 列举的五类「罕见并发路径」范畴, 因此未强制要求 owner 授权在方法论上是站得住的; TASK-033 也有相同形态的「不为空即先查明来源」且同样未入 owner_gates, 两处一致)。真正的风险是可读性层面的: 一个从 `owner_gates` 反查「TASK-029 有哪些停止点」的读者会漏掉这一条, 且实施者读到「停下」两字后, 若严格按字面「停下」执行, 可能误以为必须像 Step 4/5/6 一样上报等待, 而不会自然推断出「本地提交后继续」这条路径。

   **建议改法**: 二选一 —— (a) 在 Step 2 句尾补一句「本地提交后重新执行 Step 2 断言, 通过后进入 Step 3」, 消除「停下」与「继续」之间的字面落差; 或 (b) 在 `metadata.owner_gates` 补一条「TASK-029 · 不属于 owner 授权范畴 (本地可逆) · Step 2 工作树不干净且归属不明 ⇒ 上报」, 与其余条目对称, 方便反查。两者选一即可, 不要求都做。

### 核对无误的部分

- 组 2 (TASK-009..014) 全部 deliverables 行号锚点, 逐一对照 aria `1cb3872` 真实代码核对: `:177-178`(`_HANDOFF_TREE_PATH`)、`:240-290`(`_list_handoff_files`)、`:301`/`:321`/`:329-336`(`_read_file_content`/`_get_file_commit_date`/`_make_legacy_track_id`)、`:586-596`(fail-soft 早退 dict)、`:619-702`(主循环两个 TrackEntry 构造点与两处 `_get_file_commit_date` 调用)、`:428-456`(`_dedupe_sort_key`)、latest_md_writer.py `:30`/`:110`/`:124`/`:151`/`:259-320`/`:277-290`/`:303` —— **全部精确匹配**, 无一处行号漂移或指代错误。
- TASK-033 的「组 2 四路径」add 清单 (`handoff_multibranch.py` / `scan.py` / `latest_md_writer.py` / `test_scan_integration.py`) 与 TASK-009..014 deliverables 的并集完全一致, 无遗漏无多余。
- TASK-035 补丁 1 的「现表现形态」改写, 本席独立在真实临时仓复现 (未参考 R3 backend-architect 席的既有结论), 得到同一结论: git show 对纯 basename 路径必然失败 (rc=128, `fatal: path … does not exist`), 与「tracks==[] / unreadable_count==1 / kind=handoff_multibranch_git_show_failed」表述一致; 且 R3 conflicted 项裁决 (不采纳「窄化到构造点」的建议) 理由成立 —— 窄化后测的其实是 SC-8 的面 (rel_path 字段保留), 不是 SC-1 的面 (子目录件被读成真 track/枚举层身份混淆), 两者是不同的回归。
- TASK-034 推送写法的三条经验性断言 (多 ref 非原子发布孤儿 tag / `--follow-tags` 同样发布孤儿 tag / `--atomic` 两者同拒) 经本席独立实验全部证实, 且额外验证了 annotated tag (与 aria 实际发布方式一致) 下 `--follow-tags` 确实会把 tag 单独推送出去 (本席最初用 lightweight tag 测试得到不同结果, 换回 annotated tag 后与文档描述一致 —— 这提醒了 lightweight/annotated 的区别是这条经验判断成立的隐含前提, 但 aria 实际发布确实用 annotated tag, 该前提是满足的, 不构成 finding)。
- TASK-029 步序渲染 (Step 1–8) 内部前置/后置链、三条 fail-closed 分支与回退条的调用前置, 逐条复核无缺口; 全文 `TASK-029` 交叉引用的步骤编号 (tasks.md 5.2、TASK-034 首条) 均已同步新编号。
- SC-11 谓词的「(j1)(j2)(j3) 现状键元组」与「(l1) 分块取『标题到第一个空行』」两组本轮改写, 经脚本对 aria `1cb3872` 真实代码实跑 (18 态 × 19 谓词), 与 yaml 内嵌的 EXPECTED/实测矩阵逐格一致, 0 差异; yaml 谓词原文与脚本 `--emit-json` 的 `predicates` 字段逐字节比对一致。
- R3 m10 (脚本自检子串匹配改行首匹配 / 缺文件时退出码 2) 的两个负控态均实跑确认: 不存在目录与缺 `FILES` 清单的目录都返回退出码 2 并打印预期的 usage + 缺文件列表。
- TASK-023/TASK-025 关于 `10CG/aria-plugin#<n>` 占位符回填的时序与 TASK-029 新 Step 2 占位检查的关系, 交叉核对一致 (TASK-025 依赖 TASK-021, 在 TASK-029 之前的执行链上; 基线 `grep -c '#<' session-handoff.md` = 0, 证实检查不会有意外的基线假阳性)。

## Verdict

PASS_WITH_WARNINGS

## Vote

PASS

## 边际判断

就实现任务本身 (组 1–4, 本席深入核对了组 2 全部与组 3 的 TASK-035) 而言, 这份计划已经足够一个实施者无歧义落地 —— 达到了少见的细致程度: 关键函数给出字面返回语句 (TASK-014)、契约变更给出精确的取值集合 (TASK-013)、每处代码改动都标注真实行号且本席逐条对照 `1cb3872` 源码验证零漂移。组 2 与 TASK-035 未发现会致实施者做错或需要临场裁决的缺口。TASK-029/032/034 的 git 编排虽然复杂 (8 步 + 三类 fail-closed 分支), 但前置条件链完整、回退条件与调用点一一对应, 经本席用真实 git 仓库实验复核 (push 孤儿 tag 三态、basename 回退必然 git show 失败) 全部与文字描述相符。

反过来, 没有发现「写得过细以致束缚合理实现」的情形: 看起来最「字面」的几处 (TASK-014 的返回元组形状、TASK-013 的 docstring 逐字要求) 背后都有明确理由 —— SC-11 的机械可验证性要求文档措辞钉死到字面, 这是本 Spec 本身的设计目标(避免 paraphrase 类假绿, 历史上已有 `bad_tuples_stale_para` 一类构造证明「不钉字面会被骗过」), 不是无谓的过度规定。唯一一处「字面但不是强制」的例子是 TASK-014 的具体元组返回值写法 —— 由于没有 SC-11 谓词检查代码本身的元组形状 (只检查 docstring 措辞), 一个把第 5 级拆成两个独立元素而非嵌套 `(bool, str)` 的等价实现同样能通过全部测试; 但这是无害的写作风格差异, 不构成执行障碍, 也不值得单独修订。真正留有裁量空间、且是刻意为之的一处是 TASK-029 Step 4 的恢复流程「指针而非流程」—— 这是 R4 处置原则 1 的直接产物 (避免为罕见路径展开新的自动化流程, 该流程本身就会长出下一轮的缺陷), 本席认为这个克制是合理的, 不建议展开。

## 轮次记录

R1 (聚合 0C/13M) → v2 → R2 (0C/9M, 换执笔人) → v3 → 主控核验返修 → v3.1 → R3 (0C/9M, 持平; backend-architect 席上轮判 TASK-029 步序「下游兜底、非 finding」被聚合裁决为误判, PP3-M8 补丁 1 窄化建议未被采纳但问题本体成立) → v4 (本轮对象, 按 R3 三条处置原则改写)。本席 (R4 新派, 未见前序执笔过程) 独立复核组 2 全部行号锚点、TASK-035 全部六补丁、TASK-029/032/034 git 语义, 并对三处关键经验性断言 (补丁 1 现表现形态 / push 孤儿 tag / SC-11 谓词双源一致性) 做了真实仓库或真实脚本实跑复现, 结论与 R3 处置一致, 新发现仅 1 条 Minor (TASK-029 Step 2 的 owner_gates 覆盖与「继续」路径未闭合, 均不影响可执行性)。就本席侧重面而言, Major 数为 0, 是本 Spec post_planning 审计过程中该侧重面首次清零; 建议 owner 在综合五席后, 若其余侧重面同样收敛, 可考虑本轮是否已达 `stop-adding-rounds` 判据。
