---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:42:34.651Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [qa-engineer]
---

# post_spec R5 单席报告 — qa-engineer (handoff-multibranch-subdir-path-fidelity, Aria #195)

席位透镜: 可证伪性 (每条 SC 的反事实) · hermetic case 可构造性 · 既有测试与冻结语料受影响面 · 缺失的负向测试 · 已知既有失败项的处置。本轮**只审不改**, 未编辑任何仓库文件。全部结论建立在实读 SOT 副本 + 本轮实跑之上 (实跑清单见文末附录)。

## 审计结论

### Decisions

- [minor] testing/R4 critical+major 落地复核: 抽验 5 条均落在正文而非批注 — `5c28d58f`→§3 重写 + Task 2.2(c)(d); `ead9ac24`→SC-15 布局 1 (i) / 布局 3 (j) + 反事实扩到四条; `7ae33f13`→SC-13(c) + SC-16 夹具组成; `5b252465`→SC-11(k); `23b414c9`→§5 新增 `n_active` 行 + Impact.Risk + Task 5.3(d)。未见「加批注了事」形态 (证据: proposal.md:125,288,333,337 与 §5 表)
- [minor] testing/SC-11 新判据的基线鉴别力全部成立: 逐条实跑 `301641b` 副本 — `unreadable_count`(schema)=0 · `Returns only the basename`=1 · `path relative to`=0 · `degraded_reason`(writer / phase-1-collectors)=0/0 · `when the filename cannot be`=1 · `Fallback when single active track has no filename`=1 · `legacy:<branch>:<filename>` collector 3 处 + schema 1 处 ⇒ (a)(c)(i)(k)(l) 都 baseline-failing, R4 rework 自查抓到的跨行陷阱确已闭合 (证据: proposal.md:333)
- [minor] testing/新增键不打红既有键集断言: `test_collision.py:445` 的 `set(coll.keys()) == {kind, groups, identity_advisories}` 与 `:131` / `:277` 的同类断言都只作用于 collision dict 与 advisory dict, **不**作用于 TrackEntry 行; `test_p1_layer_h.py` 三处 `result["action"]` 断言 (`:264` / `:310` / `:336`) 亦无整字典 `assertEqual(result, {...})` ⇒ 新增 `rel_path` / `degraded_reason` 结构上打不红既有断言, proposal 该处自述属实 (证据: test_collision.py:445, test_p1_layer_h.py:264)
- [minor] testing/hermetic 可构造性总体成立: `_build_repo` 模板 (`update-ref refs/remotes/origin/<branch>`) 覆盖 SC-1 / SC-4 / SC-8 / SC-13 / SC-16 / SC-17 的仓构造; `_list_handoff_files` / `_read_file_content` / `_list_origin_branches` / `_run` 都是模块级名字 (collector `:120` `from ._common import`), monkeypatch 点确实存在; SC-6 需要的四道前置 (`scan.py:166-183`) 逐条可在夹具里配齐; `scan` 模块本身可直接 import (`test_scan_integration.py` 已有先例)

### Issues

- [major] testing/SC-3 · Task 1.2 · 新夹具的 `core.quotePath` 隔离: SC-3 把「baseline-red 资格随宿主配置漂移」的修法写成「夹具必须照 `test_handoff_multibranch_collision_dedupe.py:181-182` 的 `_GIT_ENV` 写法把 `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` 设 `/dev/null`」。**该处方够不到被测代码**: 模板里的 `_GIT_ENV` 只作为 `env=` 传给夹具自己的 `subprocess.run` (`_git()` 助手), 而被测的 `_list_handoff_files` 走 `_common._run` → `_noninteractive_git_env`, 后者是 `{**os.environ, "LC_ALL": "C", ...}`。本轮隔离实跑三档: (A) 宿主无 quotePath 覆盖 ⇒ 中文件被丢弃 (SC-3 红); (B) 宿主 global 设 `core.quotePath=false`, 测试照模板只把 `_GIT_ENV` 喂自己的 `_git()` ⇒ **中文件照常被枚举, SC-3 在 `301641b` 上就是绿的**; (C) 另行 patch `os.environ` 的 `GIT_CONFIG_GLOBAL/SYSTEM` ⇒ 恢复为红。⇒ R4 `177d72e6` 想关的门只关了一半, Task 1.2 的「五族全红」在 `quotePath=false` 的宿主 (中文/日文环境, 本仓工作语言即中文) 上仍不可满足, 而 F2 在整个 SC 集里只有 SC-3 一条覆盖。修法二选一并写进 SC-3: 用 `mock.patch.dict(os.environ, {...})` 覆盖测试进程环境, 或在临时仓里显式 `git config core.quotePath true` 走**仓内 local 配置** (后者不依赖任何环境变量传递) (证据: _common.py:341, test_handoff_multibranch_collision_dedupe.py:174-183, proposal.md:325)
- [major] testing/§3 上报字段 `filename` 的语义归属无可证伪判据: §3 与 §5 用整段把「只有 `scan.py:186` 的拼串改读 `rel_path`; `:193` / `:209` 上报的 `"filename"` 仍取 basename、**逐字节不变**」钉成硬口径, 并据此宣布「不构成语义变更 ⇒ §5 / §6 / CHANGELOG / SC 集不需要为它登记」。但**全 SC 表 (proposal.md:319-356) 对 `inconclusive` / `offenders` / `errors[].tracks[]` 零覆盖** (grep 实证), 唯一被援引作保的 `test_scan_integration.py:272` 结构上分辨不出两种实现: Task 2.2(c) 要求补的键值是 `"rel_path": "2026-07-19-x.md"` = 与 `filename` **同值**, 且 `_mock_run` (`:172-176`) 对任何 `git log -1` 返回同一 SHA、**完全不看路径参数**。本轮实跑: 在 `301641b` 副本上按**被明令禁止**的写法实改 (把 `:180` 的局部变量整体重指 `rel_path`) + 按 Task 2.2(c) 补夹具键 ⇒ `Ran 19 tests … OK` **全绿**。⇒ 一个进快照顶层 `errors[].tracks[]` 的机读字段, 其「不许变」是全文最强口径之一, 却既无 SC 也无既有断言能证伪。修法: SC-6 的子目录夹具上追加一条断言 (令该 track 走 `inconclusive` 或 `offenders` 支, 断 `["filename"] == basename` 且不含 `/`), 或新开一条 SC (证据: proposal.md:125, scan.py:180,186,193,209, test_scan_integration.py:164-166,172-176,272)
- [major] testing/SC-10 · Task 4.3 · 待复议 8 的「已知失败项」处置已被上游追平: 本轮把 SC-10 点名的 9 模块在两个 SHA 上各跑一遍 —— **冻结基线 `301641b` 今日 2 条真红** (`TestCrossOwnerRealCollisionSurvivesDedupe::test_both_latest_active_different_owners_still_reports_cross_owner` `'none' != 'cross_owner'` · `TestBoardAndCollectorAgreeOnCollisionCount::test_real_collision_produces_matching_board_collision_line_count` `0 != 1`, 即 待复议 8 预言的 Layer H 日历腐烂; 第三条 hook 可执行位失败是我只导出 `skills/state-scanner/` 的产物, 真 checkout 里该文件 `-rwxr-xr-x`, 不计), 而**当前 aria master `f314785` (= v1.73.0) 上同一命令 0 条真红** —— 同伴容器已用 `fix(state-scanner/test): collision_dedupe 16 个 collector 调用点钉 now=`(aria-plugin#194) 修掉。⇒ 三处连锁: (1) SC-10 的「基线须在 2026-09-09 之前取」今日已不可满足; (2) 它给的逃生口「先按 §待复议 8 的裁定处置再取基线」指向一个**已被上游关闭**的门, 而 待复议 8 的两个选项 (本 spec 内修 / 不修) 都不是现实已发生的第三条路 (上游已修, 应重取基线); (3) 按「不修」的推荐默认走, Task 4.3 的「既有测试全绿」与 SC-10 的「真仓 checkout 零失败」在 `301641b` 上恒不可满足。修法: 把基线冻结与 Phase B 分支点重取到 ≥ `f314785`, 并把 待复议 8 从 owner 门降为「已由上游 aria-plugin#194 关闭」的记述 (证据: proposal.md:332,388)
- [major] implementation/Task 5.2 的 gitlink bump 起点已过期且护栏漏掉这一代: Task 5.2 逐字写「主仓 spec + gitlink bump **从 `301641b` 前进** (实测起点, 见头部主仓实况行; 严禁回退到 `0545f86`)」。实测主仓 `git ls-tree HEAD aria` = **`f314785`** (HEAD `fe703c5`, 经 merge `c115fd4`) ⇒ 「实测起点」这个限定词今天为假, 而唯一成文的回退禁令只点名 `0545f86`, **`f314785 → 301641b` 这一代没有任何护栏**。头部 2026-09-10 复核块虽提到「主仓 gitlink 已随之前进」, 却没有把 Task 5.2 与「Phase B 在 `301641b` 起分支」同步改口。这正是 CLAUDE.md「多远程推送两条硬约束」与 Aria #165 三次复发的同族形态, 且它落在 Phase C 的可执行指令行上 (证据: proposal.md:313, git ls-tree HEAD aria)
- [minor] documentation/头部 2026-09-10 基线复核块的行号结论过宽: 该块由「5 个触点文件在 `301641b..f314785` 零 diff」推出「**本文全部行号**在 `f314785` 上继续有效, 基线冻结不需重取」。实测该区间 21 文件 895 增 63 删, 其中 `skills/state-scanner/tests/test_handoff_multibranch_collision_dedupe.py` 变了 99 行, `_GIT_ENV` 由 `:174-183` 移到 `:176-185` —— 而该文件正是 SC-3 / SC-4 / SC-13 逐处引用的夹具模板 (`:174-183` / `:176-179` / `:181-182`) 与 待复议 8 的对象 (`:380-382` / `:386`)。触点零 diff 只支撑「触点行号有效」, 不支撑全文。(另: `phase-d-closer/SKILL.md:218` 经复核内容与行号均未变, 该引用仍成立) (证据: proposal.md:16)
- [minor] documentation/待复议 6 的候选版本号已被上游越过: 本条逐字写「两个候选号 (`v1.71.2` / `v1.72.0`) 当前均未被占用」并把 **MINOR / v1.72.0** 定为推荐默认。实测 `git tag --list 'v1.7*'` = v1.70.0 / v1.71.0 / v1.71.1 / **v1.73.0**, `plugin.json` = `1.73.0` ⇒ 两个候选号虽都没被打 tag, 但**都落在当前版本之下**, 谁都不能用 (MINOR 支应为 v1.74.0)。头部只把 PATCH 候选顺延到 v1.73.1, 本条未同步; 另头部「已被 v1.72.x / v1.73.0 越过」里的 v1.72.x 在 tag 与 CHANGELOG 里都不存在。本条是 owner 面前的硬前置门, 数字错会直接误导裁定 (证据: proposal.md:382)
- [minor] testing/SC-2 未规定夹具组成与日期 pin: SC-2 的判据是「hermetic 临时仓 × 冻结 JSON × 八字段投影逐字段相等」, 但没写夹具放哪些文件。若夹具含**无 frontmatter** 的件 (SC-16 恰恰要求这一类以避免真空满足), 其 `updated_at` 取 `git log -1 --format=%aI` = 建仓时刻 ⇒ 冻结 JSON 与第二次运行必然不等, 变成不可复现的红; 而本文多处自陈「恒红的下场是实施者顺手削断言」。SC-4 / SC-13 已为同一机制立了「逐 commit 显式 `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`」的口径, SC-2 未沿用。修法: 明写夹具组成 (纯 frontmatter 件, 或含 legacy 件但 pin 日期) (证据: proposal.md:324, handoff_multibranch.py:686,693)
- [minor] testing/`degraded_reason` 的 `"missing_filename"` 取值零覆盖: §2.5 把新键定义为三值 (`None` / `"missing_filename"` / `"target_in_subdir"`), SC-15 只钉住 `None` (布局 1 (i) / 布局 3 (j)) 与 `"target_in_subdir"` (布局 2 (h)); 既有 `"缺 filename ⇒ 降级"` 分支**今天本就零测试** (`test_p1_layer_h.py` 全文无 unavailable / 缺 filename 用例, grep 零命中) ⇒ 实施者把该支的 reason 写成任意串 (甚至复用 `"target_in_subdir"`) 全绿通过, 而它同样是本 spec 要往公开契约里加的机读取值。修法: SC-15 加一个「active track 缺 `filename` 键」的最小布局, 断 `degraded_reason == "missing_filename"` (成本 = 一个手搓 snapshot dict) (证据: proposal.md:147, test_p1_layer_h.py:230-240)
- [minor] documentation/`_render_pointer` 调用点行号差一行: §2.5 与 Task 2.5(e2) 两处写「其**唯一**调用点是 `:302`」「由 `write_latest_md` 的 `n_active == 1` 分支 (`:302`) 解包」。实读 `latest_md_writer.py:302` 是 `elif n_active == 1:`, 真正的调用在 **`:303`** (`content = _render_pointer(active_tracks[0], now)`, grep 实证)。该行号载重于「返回形状改 tuple 后在哪解包」这条处方 (证据: proposal.md:147,288, latest_md_writer.py:303)

### Risks

- [minor] testing/SC-9 的 monkeypatch 面比字面大: SC-9 说「monkeypatch `_run` 构造一批枚举返回, 其中一条不以 `docs/handoff/` 开头」。但 `_run` 是本 collector 全部四个 git 调用 (`for-each-ref` / `ls-tree` / `git show` / `git log`) 的唯一出口 (`handoff_multibranch.py:120` 一次导入, 四处复用) ⇒ 一旦 patch, 断言 (b)「同分支的其它文件仍照常进 `tracks[]`」就要求假件同时给出可解析的 `git show` 内容与分支列表, 即必须写成按命令分派的 fake (`test_scan_integration._mock_run` 是现成范式)。SC 未点明这一点, 而本文对同类实现选择 (Task 2.1 的 (i)/(ii)、Task 2.2 的缺键口径) 一律坚持「选型后果不能对实施者不可见」(证据: handoff_multibranch.py:120,619,637,644)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 4 / Minor 6 (含 1 条 risk); 另 4 条 decision 为核实通过项, 按既有规则不计入缺陷计数。

rationale: 方案本体 (A′ + 写侧守卫 + 四调用方相对路径化 + git-show 失败不再伪造 legacy) 经本轮逐处实读代码复核**成立且可实施**, R4 的 1 critical + 10 major 抽验 5 条全部落在正文而非批注, SC-11 的机检判据逐条实跑确认有鉴别力 —— 故无 critical。但四条 major 都指向「判据/事实与现场不一致」这同一族: 两条是**验收判据够不到它要防的东西** (SC-3 的配置隔离处方够不到被测子进程; §3 的 basename 语义硬口径全 SC 集零覆盖, 且被禁止的实现实跑全绿), 两条是**上游 v1.73.0 落地后本文未同步** (SC-10 的基线今日在冻结点上 2 条真红而在上游 0 条, 待复议 8 已成空门; Task 5.2 的 gitlink 起点与实测差一代且护栏未覆盖)。前两条不修则本 spec 的 substitute SC 体系在两个点上是纸面的; 后两条不修则 Phase B 起不了正确的基线、Phase C 有回退子模块指针的口子。

## 轮次记录

### Round 1 (承前)
- Agents: 5 席 (tech-lead / backend-architect / code-reviewer / knowledge-manager / qa-engineer)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 2 / Major 15 / Minor 10 (+6 decisions)
- Vote: REVISE 5 / PASS 0 (verdict FAIL)

### Round 2 (承前)
- Agents: 5 席
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 3 / Major 10 / Minor 9 (+9 decisions); 与 R1 交集 0
- Vote: REVISE 5 / PASS 0 (verdict FAIL)

### Round 3 (承前)
- Agents: 5 席
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 0 / Major 19 / Minor 7 (+7 decisions); 与 R2 交集 0
- Vote: REVISE 5 / PASS 0 (verdict PASS_WITH_WARNINGS)

### Round 4 (承前)
- Agents: 5 席
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: Critical 1 / Major 10 / Minor 14 (+9 decisions); 与 R3 四元组交集 1 (仅 decision `a0cb3407`)
- Vote: REVISE 5 / PASS 0 (verdict FAIL; 唯一 critical 为定级差 `5c28d58f`)

### Round 5
- Agents: qa-engineer (本报告为单席产出, 五席之一)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 13 条 (Critical 0 / Major 4 / Minor 6 / Decisions 4 — decisions 不计入缺陷计数)
- Vote: REVISE

## 附录 A — 本轮实跑清单 (全部可复现, 只读, 未改仓库文件)

1. **9 模块基线双跑** (导出树, 非 worktree): `git -C aria archive 301641b|f314785 skills/state-scanner | tar -x -C <tmp>`, 各跑
   `python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories test_p1_layer_h test_max_branches_resolver test_scan_integration test_collision test_collision_frozen_corpus`
   - `301641b`: `Ran 167 tests … FAILED (failures=3)` — 2 条 Layer H 日历真红 + 1 条 hook 可执行位 (导出面产物)
   - `f314785`: `Ran 169 tests … FAILED (failures=1)` — 仅 hook 可执行位
   - 单模块对照: `301641b` 的 `test_handoff_multibranch_collision_dedupe` = `Ran 21 … FAILED (failures=2)`; `f314785` = `Ran 23 … OK`
   - hook 归因: `ls -l aria/hooks/handoff-location-guard.sh` = `-rwxr-xr-x` ⇒ 真 checkout 上不红
2. **SC-3 配置隔离三档探针** (`scratchpad/r5/sc3_probe.py`, 基线树 = `301641b` 导出): 临时仓放 `docs/handoff/2026-测试-交接.md` + `2026-01-01-a.md`, 直接调 `_list_handoff_files`
   - A (宿主无 quotePath 覆盖) → `['2026-01-01-a.md']` (中文件被丢弃, SC-3 红)
   - B (宿主 global `core.quotePath=false`, 测试只把 `_GIT_ENV` 喂自己的 `_git()`) → `['2026-01-01-a.md', '2026-测试-交接.md']` (**SC-3 绿**)
   - C (同时 patch `os.environ` 的 `GIT_CONFIG_GLOBAL/SYSTEM`) → `['2026-01-01-a.md']` (SC-3 红)
3. **§3 被禁实现的盲区证明**: 在 `301641b` 副本上把 `scan.py:180` 的 `filename = t.get("filename")` 整体重指为 `t.get("rel_path")` (§3 明令禁止的写法) + 按 Task 2.2(c) 给 `HEALTHY_TRACKS` 补 `"rel_path": "2026-07-19-x.md"` ⇒ `python3 -m unittest test_scan_integration` = `Ran 19 tests … OK`
4. **版本面**: `git -C aria tag --list 'v1.7*'` = v1.70.0 / v1.71.0 / v1.71.1 / v1.73.0; `git ls-remote --tags origin` 同; `f314785:.claude-plugin/plugin.json` = `1.73.0`; `f314785:CHANGELOG.md` 无 `## [1.72`
5. **主仓 gitlink**: `git ls-tree HEAD aria` = `f314785…`, `git ls-tree HEAD standards` = `21748d4…` (后者与 Task 4.4 头部冻结一致)
6. **SC-11 判据基线计数** (在 1.71.1 插件缓存副本上): schema `unreadable_count`=0 · collector `Returns only the basename`=1 / `path relative to`=0 / `legacy:<branch>:<filename>`=3 · schema 同串=1 · writer `degraded_reason`=0 / `when the filename cannot be`=1 / `Fallback when single active track has no filename`=1 · `phase-1-collectors.md` `degraded_reason`=0 · `layer-l-integration.md` `子目录|subdir`=0
7. **行号逐处实读复核** (抽样, 全部与 proposal 相符): `handoff_multibranch.py` `:36` / `:243` / `:246-247` / `:277` / `:278` / `:280` / `:288` / `:298` / `:301` / `:315` / `:321` / `:329-336` / `:332` / `:494` / `:521-524` / `:586-596` / `:619` / `:637-658` / `:645,665,687` · `scan.py` `:180` / `:186` / `:193` / `:209` · `latest_md_writer.py` `:72` / `:110-148` / `:111-114` / `:143` / `:151-169` / `:152` / `:159` / `:164` / `:172-224` / `:259` / `:295-320` · `handoff.py` `:263` / `:288` / `:300` / `:318` / `:321` / `:389` / `:399` · `state-snapshot-schema.md` `:1104` / `:1110` / `:1114` / `:1118` / `:1125-1128` (文件共 1168 行) · `freeze_corpus.py:29,32-35,50` · `test_collision_frozen_corpus.py:51,111,112` · `test_max_branches_resolver.py:286,300,316,332` · `test_scan_integration.py:164-166,172-176,272` · `test_p1_layer_h.py:230-240,264,270`。**唯一对不上的一处**: `_render_pointer` 调用点实为 `:303` 而非 proposal 写的 `:302`
8. **冻结语料**: `handoff-tracks-frozen-2026-09-05.json` 996 行 / 八字段 / `filename` 无斜杠 ⇒ Task 1.1 的前置断言与 §7 的「平铺仓零行为变化」前提成立

## 附录 B — 给 rework 席的最小修法建议 (不代裁 owner 门)

1. SC-3: 把「照 `_GIT_ENV` 写法」改成可执行的两选一 —— `mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})` 包住被测调用, 或临时仓内 `git config core.quotePath true` (仓内 local 配置不依赖环境变量传递)。
2. §3: 给 SC-6 的子目录夹具补一条上报字段断言 (令该 track 落进 `inconclusive` 或 `offenders`, 断 `["filename"]` 为 basename 且不含 `/`), 使「逐字节不变」这条硬口径第一次有反事实。
3. SC-10 / 待复议 8: 基线冻结与 Phase B 分支点重取到 ≥ `f314785` (aria-plugin#194 已修日历腐烂); 待复议 8 由 owner 门改为「上游已关闭」的记述, 并同步 SC-3/SC-4/SC-13 引用的 `_GIT_ENV` 行号 (`:174-183` → `:176-185`)。
4. Task 5.2 + 头部: gitlink 起点改写为实测的 `f314785`, 回退禁令扩到「不得低于当前主仓 gitlink」; 待复议 6 的 MINOR 候选随之更新 (v1.72.0 → v1.74.0), PATCH 候选 v1.73.1 保持。
5. SC-2 明写夹具组成与日期 pin; SC-15 补一个「缺 `filename` 键」的最小布局钉 `degraded_reason == "missing_filename"`; §2.5 / Task 2.5(e2) 的 `:302` 改 `:303`; SC-9 补一句「假件须按命令分派」。
