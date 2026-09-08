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
verdict: FAIL
timestamp: 2026-09-06T16:05:02.709Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [backend-architect]
---

# post_spec R1 — backend-architect (数据契约与实现可行性)

审计对象: `openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (Level 2, Aria#195)。
席位透镜: 字段语义变更的向后兼容与消费方枚举完整性 (自行 grep 核实, 不采信 proposal 的表) · 错误路径穷举 · 伪代码与真代码结构对齐。
全部行号以插件缓存副本 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `origin/master` 301641b) 为准; 本轮只审不改, 工作区 `git status --porcelain` 为空。

## 审计结论

### Decisions

- [minor] testing/Rule #6 判定: 判据表第一行 (描述性/纯代码) + SOT §5 worked example「collector 代码层 → substitute」支持本判定; `aria-plugin-benchmarks/ab-suite/state-scanner.json` 实测对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` 四词 `grep -c` 全 0, 「套件结构上测不到」属实; SKILL.md 与 `description` 确未触碰 (证据: standards/conventions/skill-benchmark-exemption.md:24-30,68-74; ab-suite/state-scanner.json)
- [minor] architecture/基线冻结: `git -C aria rev-parse origin/master` = 301641b; `git diff --stat 0545f86 301641b -- <5 触点文件>` 为空 ⇒ 行号跨两 SHA 一致成立 (证据: 本轮实跑)
- [minor] architecture/平铺仓零变化前提: 本仓 `docs/handoff/` 185 个 md、0 子目录、0 非 ASCII; 冻结语料 996 行 `filename` 无 `/` 无非 ASCII; `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 与 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` 均实际存在 (证据: 本轮 find / json 实读)
- [minor] architecture/F1 分析准确: `scan.py:186` 拼 `docs/handoff/{filename}`, rc=0 且空 SHA 时 `continue` 静默跳过, 无任何告警 —— proposal 对「静默失效」的刻画与真代码一致 (证据: scan.py:184-200)
- [minor] architecture/legacy 行不影响 collision: `lib/collision.py:281` 跳过 legacy、`:480-485` 过滤 `owner_container == unknown`, §5 该行结论成立; SC-7 期望方向也对 —— `handoff_multibranch.py:541` 用 `max(rows, key=_dedupe_sort_key)`, filename 字典序大者胜 (证据: collision.py:281,480-485; handoff_multibranch.py:428-455,541)

### Issues

- [critical] architecture/state-scanner filename 往返: `filename` 改相对路径后, `latest_md_writer._render_pointer` 写出 `**Latest**: [archive/x.md](./archive/x.md)`; 但**另一个 collector** `handoff.py::_parse_latest_pointer` 用 `Path(target).name` 剥掉目录段, 再到 `_scan_md_files` 的**非递归**顶层集合里查, 必然 miss ⇒ `handoff_pointer_target_missing` soft_error ⇒ `EXIT_SCAN_PARTIAL = 10` 且 `latest_source` 由 pointer 退回 mtime。§5 表把该消费方判为「天然正确 / 无影响」, 未追往返 (证据: writers/latest_md_writer.py:116,143,259-303; collectors/handoff.py:263-288,297,387-404; scan.py:119,337; proposal.md:116)
- [major] architecture/§2 updated_at 断言: `proposal.md:95`「`updated_at` 不再取到 mv 提交日」为假, 且与自身 SC-4 (`proposal.md:170`) 正面冲突。hermetic 实证 (顶层 2026-05-09 → `git mv` 进 `archive/` 2026-08-15): `git log -1 --format=%aI` 对旧路径 `docs/handoff/x.md` 与新路径 `docs/handoff/archive/x.md` **都**返回 `2026-08-15T12:00:00+00:00`, 加 `--follow` 亦同。真正被修的是「从未在顶层存在过」(改前空串 → 改后真日期) 与「有 frontmatter 时 `updated_at` 走 frontmatter」两类; Why §后果 3 把 mv 日期归因于路径 bug 同样错位, 若照此措辞写 CHANGELOG 会宣称一个未发生的修复 (证据: proposal.md:35,95,170 + 本轮 hermetic 实跑)
- [major] architecture/F2 非 ASCII 形态: 实证 `git ls-tree -r --name-only` 对任何含非 ASCII 的路径**整条加引号**, `Path(path).name` 得 `2026-\346\265\213\350\257\225.md"`, 在 `handoff_multibranch.py:278` 的 `.endswith(".md")` 处即被 `continue` 丢弃 —— 今天的形态是**静默漏扫**, 不产生 `git show` 失败、不进假 legacy、不推高 exit 10。非 ASCII 落在**目录段**时同样如此 (basename 得 `x.md"`)。故 `proposal.md:62`「同样落进那条假 legacy 分支 / 同一 bug 类只是触发条件不同」不成立, SC-3 的反事实机制描述 (「git show 失败」) 也须改写 (证据: proposal.md:62,169; handoff_multibranch.py:277-278 + 本轮 hermetic 实跑)
- [major] testing/SC-9 前缀守卫: `_list_handoff_files` 现签名 `tuple[list[str], str | None]` 只有分支级错误通道 —— 主循环收到非 None 即 `soft_error("handoff_multibranch_ls_tree_failed")` 后 `continue` **跳过整支分支**。要落地「计一条 soft_error 并跳过该行」必须改签名或注入 reporter, §What / §Tasks 均未点名该契约变更; 更糟的是 SC-9 只断言「有 soft_error + 不进 `tracks[]` + 不 crash」, 天真实现 (整支跳过) 在单条 fixture 上同样满足 ⇒ 断言无法区分正确与错误实现 (证据: handoff_multibranch.py:240,265-288,619-626; proposal.md:86,175)
- [major] implementation/unreadable_count 错误路径: `proposal.md:107` 自述该字段「恒存在, 默认 0」, 但分支枚举失败的 fail-soft 早退 dict 与其在 schema 文档里的字面 shape 都会缺这个键, 且无任何 task / SC 承接该路径 (§6 只点了 `:1074` 起的字段表) (证据: handoff_multibranch.py:586-596; references/state-snapshot-schema.md:1136; proposal.md:107,124,152)
- [major] testing/SC-10 基线数字: 实跑 `python3 -m unittest test_handoff_multibranch_collision_dedupe test_handoff test_handoff_worktrees test_track_board_advisories` = **Ran 78 tests, OK**, 而非 `proposal.md:176` 写的 73。按 audit-points 横切原则「数据量 / baseline 断言 → 计数查询; 规模不符 ⇒ 载重 verdict」处理。另一半数字无误: 全量 discover 静态计数 1575, 减去 `Test1210ChannelStabilityUnderOffline` 因 setUpClass ERROR 未跑的 4 个方法 = 1571, 与 proposal 一致; `TestStabilityIntegration.test_two_consecutive_runs_diff_zero` 亦确实存在 (证据: proposal.md:176 + 本轮实跑; tests/test_normalize_snapshot.py:229,260)
- [major] documentation/A 案来源误引: `proposal.md:72` 称「issue 与 triage 均倾向此案」, 但 issue 原文 A 案明写「`filename` / `track_id` 等需要 basename 的字段**另行派生**」, triage 修法倾向亦写「`filename` 字段另派生 basename」。本 spec 直接把输出字段 `filename` 的语义改成相对路径, 与两个来源 A 案的关键分句相反 —— 既未声明偏离, 也未进「待 owner 复议」。该偏离正是上面 critical 项的直接来源 (证据: proposal.md:72,89,128; issue-195.md 建议修法 A; .aria/triage-comment-195.md 修法倾向段)
- [minor] documentation/行号漂移: `proposal.md:26` 称 `:275` 是 `basename = Path(path).name`, 实际在 `:277`。同段其余行号 (178 / 240-288 / 301 / 321 / 329-336 / 428-457 / 637-658 / 683-700) 逐条核对无误 (证据: handoff_multibranch.py:277)
- [minor] documentation/基线段概括不实: `proposal.md:9` 称两 SHA 间「只新增了 7 个 a1-entry 相关测试文件」, 实测 `git diff --name-status 0545f86 301641b` = 29 files, 含 `lib/collision.py` / `phase1_gate.py` / `lib/spec_complete.py` / `coordination_probe.py` 等生产文件修改。载重结论 (5 个触点文件零 diff) 已独立核实为真, 故只是概括失真 (证据: 本轮 `git diff --name-status` 实跑)
- [minor] documentation/rule6_note 概括过宽: `proposal.md:186` 称「SC-1~SC-9 逐条对应一个行为改动, 每条附反事实」, 但 SC-2 自述「零行为变化」、SC-7 自述「现状记录性断言」, 两条在 baseline 上本就为绿, 属回归锁而非 baseline-failing。substitute 实体仍由 SC-1/3/4/5/6/8/9 七条撑住, 结论不倒, 措辞需收紧 (证据: proposal.md:168,173,186)
- [minor] documentation/pointer 排除口径: `handoff_multibranch.py:277-280` 今天就按 basename 比较 `latest.md`, `archive/latest.md` 现状即被排除。`proposal.md:88` 与待复议第 1 条把「任意深度」呈现为新的保守选择, 未点明反向选项 (只排顶层) 才是行为变更, 可能误导 owner 裁决方向 (证据: handoff_multibranch.py:277-287; proposal.md:88,193)
- [minor] architecture/§5 track_board 行: 该行写「不读 `filename` 字面 ⇒ 无影响」, 但 `track_board.py` import 并应用 collector 的 `dedupe_latest_per_track_container` (filename 字典序 tie-break), 故 Impact 第 1 条 tie-break 风险同样落到看板 collision 输入的代表行选择上。实际差异在三重并列下近乎为零 (被选行的 track_id / owner_container / updated_at 全同), 但「无影响」的表述应收紧为「间接经共享 dedupe 生效, 语义由 SC-7 覆盖」(证据: renderers/track_board.py:742-760; handoff_multibranch.py:541; proposal.md:119,140)

### Risks

- [minor] testing/SC-2 可行性: 动态载入 301641b 原实现的方案未验证 —— 被载模块使用 `from ._common import ...` 相对导入, 需 package 上下文; 且依赖运行环境能 `git show` 到该 SHA (浅克隆 CI 会失败)。其反事实 (`-z` 解析写错 ⇒ 枚举空集) 已被 SC-1 / SC-3 冗余覆盖, 建议降级为「冻结期望列表比对」以免最高风险项的唯一守卫本身脆弱 (证据: handoff_multibranch.py:113-120; proposal.md:142,168)

## 建议修法 (供 Phase A 修订, 非本轮裁决)

针对 critical 项, 三条低成本路径任选其一并补一条 round-trip SC:

1. 输出面保持 `filename` = basename (与 issue / triage 原案一致), 另加 additive 字段 `path` (相对 `docs/handoff/`) 供 `_read_file_content` / `_get_file_commit_date` / legacy `track_id` / `scan.py:186` 使用 —— 兼容面最干净, `latest_md_writer` 与 `handoff.py` 往返不变。
2. 保留本 spec 的 `filename` 语义, 但 `_render_pointer` 的链接**文本**用 basename、href 用相对路径, 并同步教 `handoff.py::_parse_latest_pointer` 不再剥目录段 + `_scan_md_files` 支持子目录 (改动面最大)。
3. 保留本 spec 语义, 但显式限定 pointer 只在顶层 track 上写真指针, 子目录 active track 走 banner 路径 (需写进 schema 文档并加 SC)。

## Verdict

**FAIL** — Critical 1 / Major 6 / Minor 6 (含 1 条 risk)。

rationale: 方案主干 (相对路径贯穿四个调用方 + git show 失败不再伪造 legacy) 方向正确, F1 的发现是真增量, Rule #6 判定与基线冻结均经机械核实成立。但 (a) `filename` 输出语义变更打断了 `latest_md_writer` → `handoff.py` 的 pointer 往返, 在本 spec 的目标人群 (子目录布局采用方) 上会以另一条路径重新产出 exit 10, 而 §5「消费方枚举」表把该消费方判为无影响; (b) 该偏离源自对 issue / triage A 案「`filename` 另行派生 basename」分句的误引; (c) 三条事实性断言 (mv 日期修复、F2 失效形态、SC-10 基线 73) 经 hermetic 实跑与实测证伪, 其中两条与本文自身 SC 冲突。post_spec 为 advisory, 不阻断流程, 但按 audit-points 数据可用性条款该 verdict 载重。

## 轮次记录

### Round 1

- Agents: backend-architect (五席之一, 本报告仅本席)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 14 (Decisions 5 / Issues 12 / Risks 1 — findings 数组按去重后 14 条提交, Decisions 只保留 2 条载重项)
- Vote: REVISE
