---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-06T16:45:46.235Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [code-reviewer]
---

# post_spec 审计报告 — code-reviewer 席 (Round 1)

审计对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, Aria#195)。
席位透镜: 逐条打开 proposal 引用的 文件:行号 验真伪 / 改动是否破坏同文件与跨文件调用路径 / 文档同步面是否列全。
核验基准: 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b`)。本轮所有断言均实读或实跑, hermetic 复现仓建在 scratchpad, 未改动仓库任何文件。

## 审计结论

### Decisions

- [minor] testing/Rule #6 判定复核: 判为「描述性 ⇒ deterministic substitute」与 SOT 决策表第一行一致; `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词实测零命中, 「AB 测不到」结论成立 (证据: `standards/conventions/skill-benchmark-exemption.md:28`, 先例 `:63-64`; grep -c 四词 = 0)
- [minor] architecture/基线与事实底座复核: 5 个触点文件在 `0545f86..301641b` 实测零 diff (行号基准成立); 全量基线复跑得 `Ran 1571 tests / FAILED (failures=1, errors=1)`, 两项红即 proposal 点名的 `Test1210ChannelStabilityUnderOffline` setUpClass ERROR 与 `TestStabilityIntegration.test_two_consecutive_runs_diff_zero`; 认领记录真实存在 (证据: `refs/aria/coordination:claims/bfe8285d/s-e4b1@1447.yaml` — track_id / linked_issue / claimed_at 与 proposal:8 相符; `.aria/triage-report-195.json` hit_rate 2/2, case-2 `updated_at=2026-08-15T12:00:00+00:00`)
- [minor] implementation/起草期新事实 F1 与 F2 复核成立: F1 = `scan.py:186` 独立硬编码 `docs/handoff/{filename}`, `:198-200` 对空 SHA `continue` 并在注释里判定为「a real answer」⇒ 路径拼错后静默跳过, 无告警; F2 = hermetic 实跑确认无 `-z` 时非 ASCII 路径输出为 `"docs/handoff/2026-\346\265\213..."`, `Path(line).name` 产出带尾引号的转义串 (证据: `scan.py:184-200`; scratchpad hermetic 仓 `git ls-tree` 输出对照)
- [minor] architecture/向后兼容前提成立: 本仓 `docs/handoff/` 实测无子目录、无非 ASCII 文件名 ⇒ 平铺仓零行为变化的前提为真; `unreadable_count` 走 additive、`snapshot_schema_version` 保持 `"1.0"` 与既有先例一致 (证据: `find docs/handoff -type d` 空; `references/phase-1-collectors.md:70` handoff_worktrees 同型 additive 先例)

### Issues

- [major] implementation/proposal §Why F1 · §5 · SC-6 函数名: proposal:41 / :115 / :172 三处把 `scan.py` 的 AC-5 检查写成 `_check_handoff_ancestry`, 真实函数为 `_same_branch_head_unreachable_tracks`, 该文件无 `ancestry` 标识符; SC-6 的核验句柄 `scan.py::_check_handoff_ancestry` 按字面不可执行 (证据: `scan.py:126`; `grep -n "ancestry" scan.py` 零命中)
- [major] implementation/§What.2 与 SC-4 互斥: §What.2 (proposal:95) 断言路径修正后 `_get_file_commit_date` 使 `updated_at`「不再取到 mv 提交日」; hermetic 实测旧 basename 路径、新 `archive/` 路径、`--follow` 三种写法全部返回 mv 日 `2026-08-15T12:00:00+00:00`。真正消除失真的是 git show 成功后改走 frontmatter, 与 SC-4 (proposal:170)「路径正确后仍如此, 属预期」直接冲突 (证据: `handoff_multibranch.py:310-326`; scratchpad hermetic 仓三次 `git log -1 --format=%aI`)
- [major] testing/SC-10 改前基线计数错: proposal:176 记「73 tests OK」, 实跑同一条命令在 `301641b` 与工作树 `0545f86` 均为 `Ran 78 tests ... OK`; 分模块为 21+27+25+5, 73 恰是漏掉 `test_track_board_advisories`。4 个测试文件在两 SHA 间字节相同, 故非版本差异 (证据: 逐模块实跑; `git diff --stat 0545f86 301641b -- <4 测试文件>` 为空)
- [major] architecture/latest.md pointer 写读往返未闭合: 修复后子目录 active track 会让 writer 写出 `**Latest**: [archive/x.md](./archive/x.md)`; 兄弟 collector 解析时 `Path(target).name` 剥掉目录段, 而候选集来自**非递归**目录扫描 ⇒ 命中 `handoff_pointer_target_missing` 软错 + 退回 mtime。§5 判「相对路径天然正确」只对人类点击的 markdown 链接成立, 机器消费链未覆盖, 也无 SC。这使 Impact 里「子目录采用方不再恒 exit 10」被高估 (证据: `writers/latest_md_writer.py:143` + `:72-94` 取 `status=="active"`; `collectors/handoff.py:288`、`:300-301`、`:387-404`)
- [major] implementation/前缀守卫与 SC-9 判据强度: `_list_handoff_files` 的返回契约是 `(list[str], str | None)`, 调用方一见 `ls_err` 非 None 就整分支 `continue`、把已枚举的文件全部丢弃。§1 要求「不以 `docs/handoff/` 开头的行计一条 soft_error 并跳过」在现契约下无法表达; SC-9 只断言该异常项不进 `tracks[]`, 没断言同分支其它文件仍在 ⇒ 吞掉整分支的天真实现照样绿, 且比原 bug 更坏 (证据: `handoff_multibranch.py:240`、`:619-626`)
- [minor] documentation/行号引用精度: proposal:26 写 `:275 basename = Path(path).name`, 实际在 `:277` (`:275` 是 `if not path:`); docstring 引用 `:244-250` 实际落在 `:246-247`。其余 `:178` / `:301` / `:321` / `:329-336` / `:428-457` / `:637-658` / `scan.py:186` / `schema:1074-1136` 逐条核对无误 (证据: `handoff_multibranch.py:272-290`)
- [minor] documentation/上游事实转述两处偏差: proposal:28 称 `_get_file_commit_date`「issue 未点名」, 但 issue 正文第 21 行已明确点名 (承袭 triage 措辞, 属 memory `feedback_spec_inherits_upstream_dec_errors` 形态); proposal:9 称两 SHA 间「只新增了 7 个 a1-entry 相关测试文件」, 实为 29 文件变更, 含 `lib/collision.py`、`lib/constants.py`、`lib/identity.py`、`phase1_gate.py`、6 份 SKILL.md。载重结论 (触点零 diff) 不受影响, 但该表述会误导 Phase B 的基线取样 (证据: issue-195 原文:21; `git -C aria diff --stat 0545f86 301641b`)
- [minor] documentation/§6 文档同步面漏两处: collector 自身的返回 schema docstring 未列入 —— `handoff_multibranch.py:14-31` 的 top-level 键表缺 `unreadable_count`, `:43` 仍写 `"filename": str, # basename of the handoff file`; 另 `references/json-diff-normalizer.md:241` 显式枚举了 `branches_scanned / legacy_count / collision / errors / exists` 键集。SC-11 只 grep `state-snapshot-schema.md`, 这两处不会转红 (证据: 上述两文件行号)
- [minor] testing/SC-4 · SC-8 · SC-12 判据强度: SC-4 前半 (legacy 行 = mv 日) 与 SC-8 前半 (`archive/latest.md` 不入 tracks) 在 `301641b` 上本就为真 —— 现码 `:277-280` 用 basename 比较, 任意深度的 `latest.md` 今天已被排除, 故「任意深度排除」在改前/改后同值; SC-4 亦是唯一没有写反事实的行为型 SC。SC-12 用活文件 `.aria/state-snapshot.json` (14:22Z 生成, 1408 tracks) 当基线, Phase B 期间只要 origin 上多一份交接就会假红, 更稳的做法是同工作区跑 baseline 与改后各一次 (证据: `handoff_multibranch.py:277-287`; `.aria/state-snapshot.json` mtime + tracks 计数)
- [minor] architecture/§5 track_board 行结论不成立: `track_board.py:183` 与 `:187-188` 直接 import `dedupe_latest_per_track_container`, 经四级排序键 (`_dedupe_sort_key` 第 3 级) 间接消费 `filename`。「无影响」只对「不读 filename 字面」成立; `archive/` 前缀翻转 tie-break 会换掉该组代表行, 而同组两行的 `status` / `phase` 可以不同 ⇒ 看板渲染同样改变。Impact.Risk 已记该风险本体, 缺的是渲染侧的覆盖与措辞更正 (证据: `renderers/track_board.py:183,187-188`; `references/state-snapshot-schema.md:1132` renderer parity)

### Risks

- [minor] testing/`-z` 解析与非 UTF-8 文件名: `_run` 用 `encoding="utf-8", errors="replace"` (`collectors/_common.py:406-413`), 故 `-z` 方案对 UTF-8 路径可正确解码 (F2 修法可行); 但文件名若不是合法 UTF-8, 字节会被替换成 U+FFFD 而无法回拼, 仍会落进 git show 失败分支。SC-3 只覆盖中文名, 建议在 spec 里显式声明「非 UTF-8 文件名不在本次修复域内」以免后续被当成回归 (证据: `_common.py:406-413`; `handoff.py:308-322` 已有同族「跳过非 UTF-8 文件名」处理)
- [minor] implementation/legacy track_id 变长: 改为 `legacy:<branch>:<relpath>` 后无解析型消费方受影响 (全仓 grep 仅生成处与文档), 但看板 TRACK 列宽固定, 长 id 会被截断, 属显示面小噪声 (证据: `grep -rn '"legacy:' --include=*.py skills/` 仅 `handoff_multibranch.py:36,336`; `track_board.py:205` 列宽常量)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 5 / Minor 7 (含 4 条 decision 记录, 按 minor 归档)。

rationale: 方案主干 (A + D) 与根因判断经代码与 hermetic 实跑双向核实成立, F1 / F2 两条起草期新事实属真扩面, Rule #6 判定与 SOT 决策表一致, 基线冻结前提为真。但存在 5 条 major: 引用的 scan.py 函数名不存在 (连带 SC-6 句柄失效)、`_get_file_commit_date` 与 mv 日期的因果陈述被实测证伪且与 SC-4 自相矛盾、SC-10 基线计数 73 与实测 78 不符 (触发 audit-points「数据可用性」载重条款)、latest.md pointer 写读往返在子目录仓会引入新的软错却被判为「天然正确」、前缀守卫要求超出现有返回契约且 SC-9 无法证伪「吞整分支」的实现。均为文本/判据层可改, 不动方案骨架, 故非 FAIL。

建议 Phase A 收口动作 (只列, 不代改):

1. 全文把 `_check_handoff_ancestry` 更正为 `_same_branch_head_unreachable_tracks`, 并把 SC-6 的核验句柄同步。
2. 重写 §What.2 第二条: 路径修正让 `_get_file_commit_date` 在「从未在顶层存在过」的文件上从空串变成真日期; mv 过的无 frontmatter 文件仍为 mv 日 (与 SC-4 一致), 并给 SC-4 补一条反事实。
3. SC-10 基线改记 78, 或把命令收敛成实际测过的三模块; 同时注明基线测于 `301641b`。
4. 新增一条 SC (或 Task) 覆盖 latest.md pointer 往返: 子目录 active track 写出 pointer 后, `collect_handoff` 不得新增 `handoff_pointer_target_missing`; 若判定该场景不修, 在 Impact 里显式降级「不再恒 exit 10」的措辞并列入待 owner 复议。
5. §1 前缀守卫补契约说明 (返回值改为携带 per-item 错误, 或由调用方接收部分成功), SC-9 增加「同分支其它文件仍进 tracks[]」断言。
6. §5 更正 track_board 行 (间接消费 dedupe 排序键), §6 文档同步面补 collector 模块 docstring 与 json-diff-normalizer.md, SC-11 相应扩 grep 面。
7. 修 proposal:26 行号 (`:275` → `:277`)、proposal:28「issue 未点名」、proposal:9「只新增 7 个测试文件」三处转述。

## 轮次记录

### Round 1

- Agents: code-reviewer (五席之一, 本报告仅本席结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 12 条 (Decisions 4 / Issues 10 / Risks 2 —— 其中 4 条 decision 与 2 条 risk 均按 minor 记账, 合计 Critical 0 / Major 5 / Minor 7)
- Vote: REVISE
