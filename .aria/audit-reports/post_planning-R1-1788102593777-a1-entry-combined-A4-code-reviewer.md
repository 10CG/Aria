---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-30T15:26:46.401Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 1
major_count: 3
minor_count: 4
---

# post_planning R1 — A4 code-reviewer (机械一致性镜头, combined-mode 三份)

## 摘要

三份 A.2/A.3 产物 (82 任务) 全部程序化跑了 8 项检查 (脚本与逐字输出见「实测记录」)。**结构层全部通过**: `yaml.safe_load` 与归档门解析器 `detailed_tasks.py::parse_detailed_tasks` 都接受三份 (parse_ok=True, 25/18/39 条, raw_status 全为 `pending`, 落在 `_DONE_FAMILY` 之外 = 归档门会正确判残留); 无重复 id / 无 tab / 无控制字节 / 无 CRLF; parent 与 tasks.md `- [ ] N.M` 三份均一一对应 (25=25 / 18=18 / 39=39, 无孤儿, 顺序一致, 标题语义逐条抽查一致); dependencies 无悬空、无环; `metadata.total_tasks` == len(tasks) 三份成立; a1 `metadata.estimated_hours "94-153"` 与逐任务区间求和 (94/153) 一致, 两份子 Spec 的 summary/complexity_summary 与实际 count/hours/清单全部相符; agent_allocation 清单与 `agent:` 字段集合相等; 214 处行号锚点实读 210 处命中 (2 处 1 行漂移, 2 处为本席取样口径差)。

**Critical 1 条**: 母 Spec Group 6 (TASK-025~030, SC-22/SC-34 红测 + 四条 rule6 substitute) 的 `dependencies` 全部指向它们要断言的文本任务 (TASK-017~023), 与同文件 Group 2→3/4 (实现依赖红测) 及姊妹 Spec (SKILL.md hunk 任务依赖 TASK-005 红测) 方向相反; 且 TASK-017~023 各自 `verification[0]` 都是「TASK-02x 绿」——被引用的测试反过来依赖本任务, verification 层成环; TASK-025 notes 自述「在 TASK-017/018 落文本前于 d69091d 跑一次全红」在此依赖图下不可执行, 而 a1 又没有姊妹 TASK-019 那样的「基线 worktree 红 / 实现后绿」留痕任务 ⇒ Rule #6 substitute 所需的 baseline-failing 证据无采集载体, 红窗结构性关闭。

**Major 3 条**: (1) 两份子 Spec 43/43 任务用 `est_hours: int` 而非 DUAL_LAYER_SPEC 必需字段 `estimated_hours: string`, 母 Spec 用 SOT 形态, combined-mode 三份不一致; linked-issue TASK-020 另缺 A.3 字段 `reason`; (2) 母 Spec tasks.md「SC → TASK 覆盖表」有 17 对 (SC, TASK) 声称在对应 TASK.verification 里找不到该 SC (11 对在整个 TASK 块任何字段都不出现), SC-3 在 39 条任务的 verification 中零命中; (3) 母 Spec TASK-038 deliverable `README.zh-CN.md` 不存在 (实为 `README.zh.md`), 且发布同步面漏 `README.ja.md` / `README.ko.md`。

**Minor 4 条**: 两份子 Spec 覆盖表少量 token 缺失 (实质在) / sibling TASK-010「恰三条 import」与 TASK-011「优先 import is_sentinel」接缝 / task_group 形态三份各异 + 两处 1 行锚点漂移。

## Findings

| id | severity | category | scope | type | 描述 + 证据 + 处方 |
|----|----------|----------|-------|------|-------------------|
| bd55ab9c | critical | testing | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | **Group 6 红测/substitute 的依赖方向反了, 红窗结构性关闭。** 证据 (实测记录 [2-dir]): TASK-025 deps=[017,018] / 026=[019] / 027=[022] / 028=[021] / 029=[023] / 030=[020,021] —— 六条测试任务全部依赖它们要断言的文本任务; 同时 TASK-017 `verification[0]`=「TASK-025 … 全绿」, 018→025, 019→026, 020→030, 021→028+030, 022→027, 023→029, 每一对的被引测试都反过来 depends on 该文本任务 (verification 成环: 文本任务的完成判据要求一个不能在它完成前开始的测试为绿)。TASK-025 notes 逐字「RED-first: 断言在 TASK-017/018 落文本前于 d69091d 跑一次全红并留痕」、TASK-027 notes「现在就是红的测试 (memory check-runs-at-baseline-first)」在此依赖图下不可执行。对照: 同文件 Group 2→3/4 是 TASK-011 deps=[004]、TASK-014 deps=[008,013] (实现依赖红测, 方向正确); 姊妹 linked-issue TASK-014/015 (SKILL.md hunk) deps=[TASK-005] (文本依赖结构红测)。后果: rule6_note 描述性档 substitute (TASK-027~030) 依赖「SC 级 baseline-failing 结构化测试」, 而 a1 没有姊妹 TASK-019 那样的「基线 worktree 红 → 实现后绿」留痕任务, 「baseline 必红」只剩散文声称 (memory `fix-writer-bottleneck` / `completion-signals-vs-runtime-invocation` 同形)。处方 (二选一, 不改 proposal): (a) 翻转边: TASK-017 deps 加 TASK-025, 018 加 025, 019 加 026, 022 加 027, 021 加 028+030, 023 加 029, 020 加 030; TASK-025~030 deps 改为 [TASK-003] (与 Group 2 同款); TASK-025~030 verification 首条改写为「在 d69091d 上跑 ⇒ 红 (留痕)」; 或 (b) 保持现序但新增一条 substitute 留痕任务 (仿姊妹 TASK-019: `git -C aria worktree add … d69091d` 跑六条断言全红 + 实现后全绿, 输出进 RESULT.md「逐 hunk 处置表」), 并把 TASK-025 notes 的「落文本前」改成「在基线 worktree 上」。两案都需同步 tasks.md「顺序」行 (5 → 6 改为 6 与 5 并行/先行) 与 Notes 的「同文件串行 6.1→6.6」。 |
| df090b25 | major | implementation | openspec/changes/{linked-issue-field-availability,sibling-spec-probe}/detailed-tasks.yaml | issue | **必需字段 `estimated_hours` 缺席 43/43 (两份子 Spec), 用 `est_hours: int` 代替; 母 Spec 用 SOT 形态 ⇒ combined-mode 三份不一致。** 证据 (实测记录 [7]): DUAL_LAYER_SPEC.md:166 `estimated_hours | ✅ | string | 工时范围 (如 "2-4")`; linked-issue 25/25、sibling 18/18 缺 `estimated_hours` (字段名实为 `est_hours`, 类型 int); a1 39/39 为 `estimated_hours: "1-2"` 串; 两份子 Spec 的 `metadata` 也无 `estimated_hours` (只有 `summary.total_est_hours` / `complexity_summary.total_hours`)。语料现状 (实测记录 precedent): 先例 `aria-2.0-m6-dispatch-input-delivery` 与归档 `linked-issue-normalization` 用 `est_hours`, 其余归档 4 份用 `estimated_hours` —— 先例与 SOT 冲突时以 SOT 为准; `grep` aria/skills 下无任何代码消费两字段之一 ⇒ 不影响归档门, 故非 critical。**附带同类缺失**: linked-issue TASK-020 无 `reason` 字段 (DUAL_LAYER_SPEC:170 A.3 阶段字段; 其余 24 条与 sibling 18 条、a1 39 条均有)。处方: 两份子 Spec 全局 `est_hours: N` → `estimated_hours: "N"` (或按 S/M/L 区间串 "1-2"/"3-5"/"6-8" 与母 Spec 对齐), `metadata` 补 `estimated_hours: "<lo>-<hi>"`; TASK-020 补 `reason: "全量回归 + 零改动断言 (qa-engineer: **/tests/**)"` 之类一句。 |
| fead49d5 | major | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md | issue | **「SC → TASK 覆盖表」与 yaml 实际不一致 (17 对), SC-3 在全部 39 条 verification 零命中。** 证据 (实测记录 [4a]/[4b], 已做 `SC-1~4` / `SC-5/6/7` 范围展开, 且把 deliverables 的 `#` 注释也算进去): SC-3 只出现在 TASK-004 的 title, 表声称的 TASK-004 · TASK-011 两条 verification 都没有 `SC-3` (TASK-011 只写「TASK-004 全绿」); 17 对声称在 TASK.verification 找不到, 其中 11 对在整个 TASK 块 (title/deliverables 注释/notes 含) 都不出现: (SC-2, 014) (SC-3, 011) (SC-8, 014) (SC-9, 017) (SC-11, 017) (SC-12, 017) (SC-12, 018) (SC-21, 020) (SC-23, 019) (SC-26, 022) (SC-29, 014); 另 6 对只在 title/notes: (SC-3, 004) (SC-15, 006) (SC-22, 025) (SC-26, 017) (SC-28, 033) (SC-34, 026)。同一行的「flag / config / JSON 键 → TASK」映射 12 项也靠「同 TASK-031 / 同 TASK-017」间接 ([4c]: `--no-push`→031/035, `ARIA_COORDINATION_NO_PUSH`→001/035, `--raw-track-id`/`--phase A.1`/`--mode advisory`/`--linked-issue`/`--repo-path`→018, `--status abandoned`/`--sweep-stale`/`--gc`→019 字面均不在该 TASK 块)。为什么重要: 覆盖表是 post_planning 与 phase-d 归档时「SC 是否都有落点」的唯一机读对账面; 实现任务的 verification 只写「TASK-00x 全绿」而不点名 SC, 则任一 SC 被从红测任务里删掉时表仍然「全覆盖」(memory `invariant-dimension`: 无向的存在性对账抓不到)。处方: 按表逐对在 TASK.verification 补 `SC-N` token (实现任务写成「TASK-007 全绿 (SC-2 / SC-8 / SC-29)」即可); 或把表的「实现后回归」列改为只引测试任务、实现任务不入表; TASK-018/019 补齐它们真正落的 flag 字面。 |
| 518a7d7f | major | implementation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | **TASK-038 deliverable `README.zh-CN.md` 不存在; 发布同步面漏两份 i18n README。** 证据 (实测记录 [8a] + `ls README*.md`): 主仓根只有 `README.md README.zh.md README.ja.md README.ko.md`; TASK-038 deliverables 列 `README.zh-CN.md` (注释「i18n: … badge/版本串必改」) ⇒ 路径不存在; CLAUDE.md §版本管理「发布同步面 = … root README badge + i18n README」+ 最近一次 v1.67.2 发版 commit 086ee32 改的是 `i18n ×3 各 badge/Plugin Version/translated-from`; 姊妹 linked-issue TASK-024 正确列出三份 (`README.zh.md` / `README.ja.md` / `README.ko.md` 各 :3/:10/:244, 本席 sed 实读均含 `1.67.2`)。为什么重要: 机械兜底 `i18n-readme-translation-currency` 会在漏改的两份上红, TASK-038 verification 又要求该 check 绿 ⇒ 按本 yaml 执行必然自相矛盾。处方: 改为三行 `README.zh.md` / `README.ja.md` / `README.ko.md` (各 :3 translated-from / :10 badge / :244 Plugin Version, 与姊妹 TASK-024 同口径)。 |
| 62285020 | minor | documentation | openspec/changes/linked-issue-field-availability/tasks.md | issue | 覆盖表 4 对 token 缺 (实质内容在, 故 minor): (SC-5, TASK-010) (SC-8, TASK-008) (SC-9, TASK-007) 在整个 TASK 块无该 SC 字面 (TASK-007 有「E6 = emit_arg 四格表」、TASK-008 有首行前缀契约、TASK-010 有「OK (9 份…6 条在册)」实跑); (SC-7, TASK-016) 只在 notes。flag 映射行: `--linked-issue`→2.1/1.2/1.4 (TASK-007/002/004 块无该字面, 只有 emit_arg)、`--no-push`→4.1/4.2 (TASK-016/017 只有 `ARIA_COORDINATION_NO_PUSH`, 017 连 env 名也无, 只写「同 TASK-016」)。处方: 补 token 或把映射行改成引测试任务。 |
| 4bf32c17 | minor | documentation | openspec/changes/sibling-spec-probe/tasks.md | issue | 覆盖表 2 对 token 缺: (SC-16, TASK-016) —— TASK-016 verification 逐字含 SC-16 的期望「(β) verdict == not_established / exit≠0 / 非 JSON … ⇒ 渲染「未能核实」而非「无竞品」」但无 `SC-16` 字面; (SC-18, TASK-006) —— 只在 title。处方: 两处补 token。 |
| 948363d3 | minor | implementation | openspec/changes/sibling-spec-probe/detailed-tasks.yaml | risk | **TASK-010 与 TASK-011 / a2_discretions (i) 在「唯一 import 块」符号数上打架。** TASK-010 verification 逐字「紧接三条 import (…) … 三符号不复制」+「全文件 `sys.path.insert` 仅此一处 (grep -c == 1)」; TASK-011 verification「优先 `is_sentinel(token_str)` (姊妹导出…)」+ metadata.a2_discretions (i)「在 §3 唯一 import 块内追加 `is_sentinel` 一并 import」并明确请 post_planning 复核。本席复核: 「位置唯一」的约束 (proposal §3 / SC-21) 不受第四个符号影响, 判不违反 —— 但 TASK-010 的字面判据「三条」会把正确实现判错。处方: TASK-010 改为「三条必需 import + 可选第四条 `is_sentinel`, 同块; 块外零 `from lib.` / `from collectors.`」, 并让 TASK-004 结构断言按「块外零 import」而非「恰三条」写。 |
| b0e8b171 | minor | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | 格式/锚点小项: (1) `task_group` 三份形态各异 (a1 整数 `1..8` / linked `TG-1..5` / sibling `G1..5`; 先例 m6 用 `TG-n`), combined-mode 下同族三份宜统一; (2) 行号 1 行漂移两处: TASK-014 注释「:1155-1158 CLI 契约注释同步」—— `[--linked-issue]` 契约行实在 `phase1_gate.py:1154`; TASK-019 注释 branch-manager「:148 命令」—— `--raw-track-id <carry-id>` 命令行实在 `:149` (:148 是前一句), tasks.md「行号复核」表未记这两处。其余 210 处锚点命中。处方: 统一 task_group 前缀; 两处行号改正。 |

**不构成 finding 的核对 (已证伪的怀疑, 留痕)**: Impact 表路径未入 deliverables 者全部是「零改动 / ⛔ 迁出 / 引用」行 (collision.py 零改动、`aria-2.0-m{6,7}-*` 不改、`skills/state-scanner/**` 不改、audit-engine 面迁出、`track_id.py` 自述 SOT 等), 对应「零改动」在 verification 以 `git diff --stat` 为空断言承接; proposal 里出现而 yaml 全无的 flag 只有 `--spec-slug` (1A 撤销, 正确缺席)、`--is-ancestor` / `--stat` / `--get` / `--symref` / `--no-tags` (git 子命令) 与 `--flag` (泛指)。三份 `(新建)` 标记文件今日全部不存在 (`linked_issue_field.py` / `linked_issue_field_probe.py` / `sibling_spec_probe.py` / `audit-engine.json` / `.aria/linked-issue-field-grandfathered.txt` / 四个新测试文件); 现存 deliverables 除 `README.zh-CN.md` 外全部 `test -e` 为真。TASK-001 声称的 `ls-remote origin master` == `github master` == `d69091d` 本席实跑成立; `test_coordination_no_push.py` `def test_` = 16、state-scanner tests 基线 1425、`.aria/state-checks.yaml` 12 条、ab-suite 31 个 json 且无 `audit-engine.json`、version.yaml 1.1.0/29/58、state-scanner.json 12 evals v1.6.0、phase-a-planner ```yaml 围栏 8 处、spec-drafter SKILL.md 438 行、audit-engine SKILL.md 421 行 / execution-modes.md 144 行 / `每轮入口` 0 命中、`update_heartbeat` 全 aria 仅 layer-l-integration.md:45、DEFAULTS.json `state_scanner` 无 `coordination`、cc1bdef 语料 147 / HEAD 149 (9+140) —— 全部与三份 yaml 的自述一致。

## Verdict

**FAIL** (1 critical / 3 major / 4 minor)。

## Vote

**REVISE**。Critical 一条修法明确 (翻转 Group 6 六条边 + 改 7 条 verification 首句, 或补一条 worktree 留痕任务), 三条 major 均为字段/路径/对账表层面, 不涉 proposal.md, 预计一轮可清。

## 实测记录 (脚本 + 逐字输出; 工作树: 主仓 HEAD de5b80c / aria d69091d / standards 334c609, 2026-08-30 UTC)

### 检查 1 / 3 / 6 / 7 — parent↔tasks.md · status/total/估时汇总 · 两解析器 · 必需字段

**脚本** `check_1_3_6_7.py`:

```python
#!/usr/bin/env python3
"""Checks 1 (parent<->tasks.md), 3 (status/total/estimate), 6 (parsers), 7 (required fields)."""
import re, sys, yaml, json
sys.path.insert(0, "/home/dev/Aria/aria/skills/state-scanner/scripts")
from lib.detailed_tasks import parse_detailed_tasks

ROOT = "/home/dev/Aria/openspec/changes"
SPECS = ["linked-issue-field-availability", "sibling-spec-probe", "a1-entry-claim-duplicate-work-guard"]
REQ = ["id","parent","title","status","complexity","estimated_hours","dependencies","deliverables","agent","reason","verification"]
STATUS_ENUM = {"pending","in_progress","completed","blocked"}

for s in SPECS:
    print(f"\n================ {s} ================")
    ypath = f"{ROOT}/{s}/detailed-tasks.yaml"; mpath = f"{ROOT}/{s}/tasks.md"
    raw = open(ypath, encoding="utf-8").read()
    # --- check 6: bytes hygiene
    ctrl = [(i+1, repr(l)) for i,l in enumerate(raw.splitlines()) if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", l)]
    tabs = [i+1 for i,l in enumerate(raw.splitlines()) if "\t" in l]
    print(f"[6] control bytes: {len(ctrl)} {ctrl[:3]}; tab-indented lines: {len(tabs)} {tabs[:5]}; CRLF: {raw.count(chr(13))}")
    d = yaml.safe_load(raw)
    tasks = d["tasks"]
    print(f"[6] yaml.safe_load OK; top keys={list(d.keys())}; len(tasks)={len(tasks)}")
    pr = parse_detailed_tasks(raw)
    print(f"[6] parse_detailed_tasks: parse_ok={pr['parse_ok']} reason={pr['reason']!r} n={len(pr['tasks'])}")
    statuses = sorted({t['raw_status'] for t in pr['tasks']})
    print(f"[6] parser raw_status set = {statuses}; ids match yaml? {[t['id'] for t in pr['tasks']] == [t['id'] for t in tasks]}")
    ids = [t["id"] for t in tasks]
    dups = {i for i in ids if ids.count(i) > 1}
    idfmt = all(re.fullmatch(r'TASK-\d{3}', i) for i in ids); seq = ids == [f'TASK-{n:03d}' for n in range(1,len(ids)+1)]
    print(f"[6] duplicate ids: {dups or 'none'}; id format ok: {idfmt}; sequential: {seq}")
    # --- check 7: required fields
    missing = {}
    for t in tasks:
        m = [k for k in REQ if k not in t]
        if m: missing[t["id"]] = m
    est_fields = sorted({k for t in tasks for k in t if k in ("estimated_hours","est_hours")})
    print(f"[7] required-field misses (DUAL_LAYER_SPEC 表): {len(missing)} tasks; sample: {dict(list(missing.items())[:3])}")
    print(f"[7] estimate field names in use: {est_fields}; types: {sorted({type(t.get('estimated_hours', t.get('est_hours'))).__name__ for t in tasks})}")
    # --- check 3
    st = sorted({t["status"] for t in tasks})
    print(f"[3] status set = {st}; all pending: {st==['pending']}; in enum: {set(st) <= STATUS_ENUM}")
    print(f"[3] metadata.total_tasks={d['metadata'].get('total_tasks')} == len(tasks)={len(tasks)} -> {d['metadata'].get('total_tasks')==len(tasks)}")
    cx = {}
    for t in tasks: cx.setdefault(t["complexity"], []).append(t["id"])
    print(f"[3] complexity counts: { {k: len(v) for k,v in cx.items()} }")
    # estimate sums
    def hrs(t):
        v = t.get("estimated_hours", t.get("est_hours"))
        if isinstance(v, (int,float)): return (v, v)
        m = re.fullmatch(r"(\d+)-(\d+)", str(v)); return (int(m.group(1)), int(m.group(2))) if m else (None,None)
    lo = sum(hrs(t)[0] for t in tasks if hrs(t)[0] is not None); hi = sum(hrs(t)[1] for t in tasks if hrs(t)[1] is not None)
    print(f"[3] sum of per-task hours: lo={lo} hi={hi}; metadata.estimated_hours={d['metadata'].get('estimated_hours')!r}; summary={d.get('summary',{}).get('total_est_hours') or d.get('complexity_summary',{}).get('total_hours')!r}")
    if "summary" in d:
        for k,v in d["summary"]["by_complexity"].items():
            print(f"    summary.by_complexity[{k}] count={v['count']} est={v['est_hours']} | actual count={len(cx.get(k,[]))} est={sum(hrs(t)[0] for t in tasks if t['complexity']==k)}")
    if "complexity_summary" in d:
        for k,v in d["complexity_summary"].items():
            if not isinstance(v, dict): print(f"    complexity_summary[{k}] = {v}"); continue
            act = [t['id'] for t in tasks if t['complexity']==k]
            print(f"    complexity_summary[{k}] count={v['count']} hours={v['hours']} listed={v['tasks']} | actual count={len(act)} hours={sum(hrs(t)[0] for t in tasks if t['complexity']==k)} match_list={sorted(v['tasks'])==sorted(act)}")
    # task_group consistency
    tg = sorted({str(t.get("task_group")) for t in tasks}); print(f"[3] task_group values: {tg}; metadata.task_groups={d['metadata'].get('task_groups')}")
    # agent allocation
    if "agent_allocation" in d:
        for ag, v in d["agent_allocation"].items():
            if not isinstance(v, dict) or "tasks" not in v: continue
            act = [t["id"] for t in tasks if t["agent"] == ag]
            print(f"    agent_allocation[{ag}] count={v['count']} listed={len(v['tasks'])} actual={len(act)} same_set={sorted(v['tasks'])==sorted(act)}")
    # --- check 1: parent <-> tasks.md
    md = open(mpath, encoding="utf-8").read()
    md_items = re.findall(r"^- \[ \] (\d+\.\d+) (.*)$", md, re.M)
    md_nums = [n for n,_ in md_items]
    md_titles = dict(md_items)
    parents = [t["parent"] for t in tasks]
    PRE = re.compile(r"\d+\.\d+")
    badfmt = [(t["id"], t["parent"]) for t in tasks if not (isinstance(t["parent"], str) and PRE.fullmatch(t["parent"]))]
    print(f"[1] tasks.md checklist items: {len(md_nums)} (dup: {[n for n in md_nums if md_nums.count(n)>1]}); yaml parents: {len(parents)} distinct={len(set(parents))}")
    print(f"[1] parent format bad: {badfmt or 'none'}")
    print(f"[1] parents not in tasks.md: {sorted(set(parents)-set(md_nums)) or 'none'}")
    print(f"[1] tasks.md nums without TASK: {sorted(set(md_nums)-set(parents)) or 'none'}")
    multi = {p: [t['id'] for t in tasks if t['parent']==p] for p in set(parents) if parents.count(p)>1}
    print(f"[1] parents shared by >1 TASK: {multi or 'none'}")
    # order check: TASK ids ascending vs parent order in md
    order_ok = [md_nums.index(p) for p in parents] == sorted(md_nums.index(p) for p in parents)
    print(f"[1] TASK order follows tasks.md order: {order_ok}")
    print(f"[1] title pairs (parent -> md title[:60] | yaml title[:60]):")
    for t in tasks:
        print(f"    {t['parent']:>4} md: {md_titles.get(t['parent'],'?')[:70]}")
        print(f"         yaml: {t['title'][:70]}")

```

**输出**:

```text

================ linked-issue-field-availability ================
[6] control bytes: 0 []; tab-indented lines: 0 []; CRLF: 0
[6] yaml.safe_load OK; top keys=['metadata', 'tasks', 'agent_allocation', 'execution_order', 'summary', 'out_of_scope']; len(tasks)=25
[6] parse_detailed_tasks: parse_ok=True reason='25 task(s) parsed' n=25
[6] parser raw_status set = ['pending']; ids match yaml? True
[6] duplicate ids: none; id format ok: True; sequential: True
[7] required-field misses (DUAL_LAYER_SPEC 表): 25 tasks; sample: {'TASK-001': ['estimated_hours'], 'TASK-002': ['estimated_hours'], 'TASK-003': ['estimated_hours']}
[7] estimate field names in use: ['est_hours']; types: ['int']
[3] status set = ['pending']; all pending: True; in enum: True
[3] metadata.total_tasks=25 == len(tasks)=25 -> True
[3] complexity counts: {'M': 10, 'S': 14, 'L': 1}
[3] sum of per-task hours: lo=112 hi=112; metadata.estimated_hours=None; summary='~112h coarse (token 轴为 canonical, 见 metadata.estimation_note)'
    summary.by_complexity[S] count=14 est=42 | actual count=14 est=42
    summary.by_complexity[M] count=10 est=60 | actual count=10 est=60
    summary.by_complexity[L] count=1 est=10 | actual count=1 est=10
    summary.by_complexity[XL] count=0 est=0 | actual count=0 est=0
[3] task_group values: ['TG-1', 'TG-2', 'TG-3', 'TG-4', 'TG-5']; metadata.task_groups=5
    agent_allocation[qa-engineer] count=11 listed=11 actual=11 same_set=True
    agent_allocation[backend-architect] count=5 listed=5 actual=5 same_set=True
    agent_allocation[knowledge-manager] count=6 listed=6 actual=6 same_set=True
    agent_allocation[tech-lead] count=3 listed=3 actual=3 same_set=True
[1] tasks.md checklist items: 25 (dup: []); yaml parents: 25 distinct=25
[1] parent format bad: none
[1] parents not in tasks.md: none
[1] tasks.md nums without TASK: none
[1] parents shared by >1 TASK: none
[1] TASK order follows tasks.md order: True
[1] title pairs (parent -> md title[:60] | yaml title[:60]):
     1.1 md: SC-1 (E0 定位三谓词 + 两拼写集合封闭, 夹具 (a)–(g) + A.2 补 (h) 非 ASCII 折叠负控) + SC-2 
         yaml: SC-1 E0 定位夹具 (a)–(h) + SC-2 E2 起始位 (逐字复用真实语料)
     1.2 md: SC-3 (E4/E5/E6 多值 (a)(b)) + SC-4 (哨兵六分支 (a)–(f); E5 吃 E3 原始串)
         yaml: SC-3 多值 E4/E5/E6 + SC-4 哨兵六分支 (E5 吃 E3 原始串)
     1.3 md: SC-5 (探针 check 模式六臂 (a)(b)(c)(d)(e1)(e2), CLI 全链路 `subprocess`, 临时项目根夹
         yaml: SC-5 探针 check 模式六臂 — CLI 全链路 subprocess + 真实降级夹具
     1.4 md: SC-9 (`--emit-arg` 四夹具 (a)–(d), CLI 全链路; 失败态 stdout 必空)
         yaml: SC-9 --emit-arg 四夹具 CLI 全链路 (失败态 stdout 必空)
     1.5 md: SC-6 (SOT 模板恰一条 E0 命中 + canonical 拼写 + Usage Note + spec-drafter 引用路径存
         yaml: SC-6 模板 SOT + SC-7a 预览围栏 + SC-8 注册/分发面/实跑 (结构断言, 跨仓 fail-soft)
     1.6 md: 坏实现拒绝矩阵 — 把 proposal 各 SC「它怎么会红」列点名的坏实现写成同文件内的 `_bad_*` 抽取器, 断言每条夹具对**
         yaml: 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器
     2.1 md: `aria/skills/state-scanner/lib/linked_issue_field.py` (**新建**, 纯函数, st
         yaml: lib/linked_issue_field.py — E0–E6 纯函数 + FieldVerdict + is_sentinel/emi
     2.2 md: `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建*
         yaml: scripts/linked_issue_field_probe.py — check 模式: 六臂 fail-CLOSED + --gra
     2.3 md: 同脚本 `--emit-arg <proposal.md>` 模式 — E6 四格表的 CLI 宿主 (SC-9); 只有 `OK` 且非哨
         yaml: 同脚本 --emit-arg <proposal.md> 模式 — E6 四格表 CLI 宿主 (SC-9)
     2.4 md: `.aria/linked-issue-field-grandfathered.txt` (**新建**, 主仓, 仓本地数据) — 6 条
         yaml: .aria/linked-issue-field-grandfathered.txt — 仓本地白名单 6 条 + 头注
     2.5 md: `.aria/state-checks.yaml` 注册 `linked-issue-field-availability` — 逐字照 §
         yaml: .aria/state-checks.yaml 注册 linked-issue-field-availability (只用既有 7 键, 
     2.6 md: **A.2 显式验收项 (`:388`)**: 实测 `${CLAUDE_PLUGIN_ROOT}` 是否被导出到 Phase 1.11 的
         yaml: A.2 显式验收项 (:388): 实测 ${CLAUDE_PLUGIN_ROOT} 是否导出到 Phase 1.11 check 子进程
     3.1 md: `standards/openspec/templates/proposal-minimal.md` (**跨仓 SOT**) — `:5`
         yaml: standards/openspec/templates/proposal-minimal.md — 头部增 Linked Issue 行 
     3.2 md: `aria/skills/spec-drafter/SKILL.md` **hunk A** — 正文声明 `Linked Issue` 字
         yaml: spec-drafter/SKILL.md hunk A — 正文声明 Linked Issue 必填 + 写法引 §3
     3.3 md: 同文件 **hunk B** — `### Level 2 预览` 围栏 (`:127-162`) 头部 `:140` `> **Statu
         yaml: spec-drafter/SKILL.md hunk B — Level 2 预览围栏头部补 Created + Linked Issue 
     4.1 md: 用 `/skill-creator` 对 **3.2 + 3.3 两 hunk** 照跑 `aria-plugin-benchmarks/a
         yaml: 用 /skill-creator 对 hunk A + hunk B 照跑 ab-suite/spec-drafter.json 2 eva
     4.2 md: **可证伪定向 fixture ×1 (SC-7 双臂)** — `spec-drafter.json` 新增 eval id 3 (中文臂
         yaml: 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.json 新增 eval id 3 (中文臂); 英文臂
     4.3 md: 套件缺口 issue — **A.2 裁量: 归并到 `aria-plugin#117`** (open, 「AB 测试集缺 authori
         yaml: 套件缺口 issue — 归并 aria-plugin#117 (评论追加本 Spec 为第二实例 + eval id 3 登记)
     4.4 md: substitute 留痕 — 模板 hunk (SC-6) 与探针/注册 hunk (SC-4/5/8) 走 substitute: 在 
         yaml: substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk 处置表
     5.1 md: 全量回归 — `cd aria/skills/state-scanner/tests && python3 run_tests.py` OK
         yaml: 全量回归 — run_tests.py OK + run_all_tests.sh 0 FAIL + 零改动断言
     5.2 md: aria 子模块版本面 bump (按引用点, 先例 `linked-issue-normalization` 5.9): `plugin.
         yaml: aria 子模块版本面 bump — 按引用点 (plugin.json SOT / marketplace ×2 / README / V
     5.3 md: aria 子模块 **本地** merge feature 分支 → master + `git push origin && git pu
         yaml: aria 子模块本地 merge → master + 双推 + 逐 remote ls-remote 核验 + tag + 主仓 gitl
     5.4 md: standards 子模块 **本地** merge → master + 双推 + 逐 remote `ls-remote` 核验 + 主
         yaml: standards 子模块本地 merge → master + 双推 + ls-remote 核验 + 主仓 gitlink bump (
     5.5 md: 主仓版本引用面 — `VERSION:24` / `README.md:8` badge + `:242` Plugin Version /
         yaml: 主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n ×3 各 3 点 (仅版本串)
     5.6 md: 主仓 PR (Spec 本体 + `.aria/` 两文件 + 两 gitlink + 版本引用面 + `ab-results/` + `a
         yaml: 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge gate (Rule #8)

================ sibling-spec-probe ================
[6] control bytes: 0 []; tab-indented lines: 0 []; CRLF: 0
[6] yaml.safe_load OK; top keys=['metadata', 'tasks', 'execution_order', 'agent_allocation', 'complexity_summary']; len(tasks)=18
[6] parse_detailed_tasks: parse_ok=True reason='18 task(s) parsed' n=18
[6] parser raw_status set = ['pending']; ids match yaml? True
[6] duplicate ids: none; id format ok: True; sequential: True
[7] required-field misses (DUAL_LAYER_SPEC 表): 18 tasks; sample: {'TASK-001': ['estimated_hours'], 'TASK-002': ['estimated_hours'], 'TASK-003': ['estimated_hours']}
[7] estimate field names in use: ['est_hours']; types: ['int']
[3] status set = ['pending']; all pending: True; in enum: True
[3] metadata.total_tasks=18 == len(tasks)=18 -> True
[3] complexity counts: {'S': 4, 'M': 11, 'L': 3}
[3] sum of per-task hours: lo=108 hi=108; metadata.estimated_hours=None; summary=108
    complexity_summary[S] count=4 hours=12 listed=['TASK-001', 'TASK-002', 'TASK-009', 'TASK-018'] | actual count=4 hours=12 match_list=True
    complexity_summary[M] count=11 hours=66 listed=['TASK-003', 'TASK-004', 'TASK-006', 'TASK-008', 'TASK-010', 'TASK-011', 'TASK-013', 'TASK-014', 'TASK-015', 'TASK-016', 'TASK-017'] | actual count=11 hours=66 match_list=True
    complexity_summary[L] count=3 hours=30 listed=['TASK-005', 'TASK-007', 'TASK-012'] | actual count=3 hours=30 match_list=True
    complexity_summary[XL] count=0 hours=0 listed=[] | actual count=0 hours=0 match_list=True
    complexity_summary[total_hours] = 108
[3] task_group values: ['G1', 'G2', 'G3', 'G4', 'G5']; metadata.task_groups=5
    agent_allocation[tech-lead] count=1 listed=1 actual=1 same_set=True
    agent_allocation[qa-engineer] count=9 listed=9 actual=9 same_set=True
    agent_allocation[backend-architect] count=5 listed=5 actual=5 same_set=True
    agent_allocation[knowledge-manager] count=3 listed=3 actual=3 same_set=True
[1] tasks.md checklist items: 18 (dup: []); yaml parents: 18 distinct=18
[1] parent format bad: none
[1] parents not in tasks.md: none
[1] tasks.md nums without TASK: none
[1] parents shared by >1 TASK: none
[1] TASK order follows tasks.md order: True
[1] title pairs (parent -> md title[:60] | yaml title[:60]):
     1.1 md: 前置断言: `aria/skills/state-scanner/lib/linked_issue_field.py` 已存在且导出 `ex
         yaml: 前置断言: 姊妹纯函数 lib/linked_issue_field.py 已存在且导出所需接口 (缺席 ⇒ 阻塞, 不建替身)
     1.2 md: 基线三态记录: audit-engine 现状 (零 `scripts/` / 零 `tests/` / 零 `lib/` / 零 `col
         yaml: 基线三态记录: audit-engine 现状 + 锚点复核 + SC-17/20/21 基线必红亲跑
     1.3 md: 建 `aria-plugin-benchmarks/ab-suite/audit-engine.json` (**经 `/skill-cre
         yaml: 建 ab-suite/audit-engine.json (经 /skill-creator; α/β 两 eval, 其一即 SC-16)
     2.1 md: 新建 `aria/skills/audit-engine/tests/test_sibling_spec_probe.py` 骨架: 模块级
         yaml: 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控) + 结构断言 (无 lib/collectors
     2.2 md: 谓词层测试 (纯函数, 不打网络): **SC-7** (`#122` 两行原文经层 2 得 `["k","aria-plugin",122
         yaml: 谓词层测试 (纯函数): SC-7 / SC-8 / SC-9 / SC-10 / SC-11 / SC-19 + 键构造 + BAD_TO
     2.3 md: 层 0 假阳性拒绝 **SC-18** 四臂 (a 行首 / b 宽松 / c 行首+仅头部 / d 合成围栏夹具) 在主仓 `cc1bde
         yaml: SC-18 层 0 假阳性拒绝四臂 (cc1bdef 147 篇 + 合成围栏夹具) + SC-1 archive 命中
     2.4 md: 远端解析 / fetch / cap 测试 (注入式 git runner, 仿 `phase-d-closer/tests/test_fe
         yaml: 远端解析 / fetch / cap 测试 (注入式 git runner): SC-12/13/14 + SC-3/4/5/6 + §5 
     2.5 md: CLI 全链路契约测试 (`subprocess.run([sys.executable, script, ...])`, 仿 `state
         yaml: CLI 全链路契约测试 (subprocess): SC-15 三终局 stdout 恰一 JSON + SC-2 + exit 三分 + 
     2.6 md: 指令面结构断言 (RED): **SC-17** (execution-modes.md `## Convergence 模式` / `##
         yaml: 指令面结构断言 (RED): SC-17 分块计数 + 负控 / SC-20 (i) SKILL.md 小节切片 + (ii) execut
     3.1 md: 骨架 + I/O 边界: CLI `--own-spec-dir <name>` (必需) / `--repo-path <root>` (
         yaml: 探针骨架 + I/O 边界: CLI / 唯一 import 块 / own proposal / 可注入 runner / §7 输出契约
     3.2 md: 谓词层: 姊妹四态 → 层分派表 (`NO_FIELD`→层 3 / `NO_TOKEN`→层 2 / `BAD_TOKEN`→层 1 ∪ 
         yaml: 谓词层: 四态 → 层分派 / 哨兵层 1.5 / 层 2 URL 回落 / 键构造 / SC-19 常量黑名单 / 集合求交 / 自命中排
     3.3 md: remote 与默认分支 (§4, fail-closed): `actual_remotes` 取 `git -C <repo> remo
         yaml: remote 集合 + 默认分支 fail-closed (ls-remote --symref) + fetch 私有 ref + 30s
     3.4 md: 语料枚举 + 规模上限 (§2 / §6): 在私有 ref 上 `git ls-tree -r --name-only` 过滤 `^ope
         yaml: 语料枚举 (ls-tree on 私有 ref, changes 先 archive 后, 字节序) + MAX_PROPOSALS_SCA
     3.5 md: GREEN + 回归: 2.1–2.5 全绿 (2.6 留红待 4.x); `bash aria/skills/run_all_tests.
         yaml: GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 / 三个坏实现负控亲跑 / state-scanner
     4.1 md: `aria/skills/audit-engine/references/execution-modes.md`: Convergence 
         yaml: execution-modes.md: Convergence / Challenge 两块各插逐字相同两行插入串 + 新增 `## 竞品 
     4.2 md: `aria/skills/audit-engine/SKILL.md`: 在 `## 执行流程` 内 `### Step 0: Anchor
         yaml: SKILL.md 「per-round 入口探针」小节 (概述 + 指针 + 四字面 + 命令行 + 与 Step 0 消歧 + α/β 点
     5.1 md: `/skill-creator benchmark audit-engine` 双臂实跑 (with_skill = 4.x 后的 SKIL
         yaml: /skill-creator benchmark audit-engine 双臂实跑 (with = 4.x 后 / without = 基
     5.2 md: 发布同步面 (aria 子模块): `aria/CHANGELOG.md` 条目 + `.claude-plugin/plugin.json
         yaml: 发布同步面 (aria 子模块): CHANGELOG + plugin.json (SOT) + 派生文件一致 + 主仓 gitlink 

================ a1-entry-claim-duplicate-work-guard ================
[6] control bytes: 0 []; tab-indented lines: 0 []; CRLF: 0
[6] yaml.safe_load OK; top keys=['metadata', 'tasks']; len(tasks)=39
[6] parse_detailed_tasks: parse_ok=True reason='39 task(s) parsed' n=39
[6] parser raw_status set = ['pending']; ids match yaml? True
[6] duplicate ids: none; id format ok: True; sequential: True
[7] required-field misses (DUAL_LAYER_SPEC 表): 0 tasks; sample: {}
[7] estimate field names in use: ['estimated_hours']; types: ['str']
[3] status set = ['pending']; all pending: True; in enum: True
[3] metadata.total_tasks=39 == len(tasks)=39 -> True
[3] complexity counts: {'S': 19, 'M': 15, 'L': 5}
[3] sum of per-task hours: lo=94 hi=153; metadata.estimated_hours='94-153'; summary=None
[3] task_group values: ['1', '2', '3', '4', '5', '6', '7', '8']; metadata.task_groups=8
[1] tasks.md checklist items: 39 (dup: []); yaml parents: 39 distinct=39
[1] parent format bad: none
[1] parents not in tasks.md: none
[1] tasks.md nums without TASK: none
[1] parents shared by >1 TASK: none
[1] TASK order follows tasks.md order: True
[1] title pairs (parent -> md title[:60] | yaml title[:60]):
     1.1 md: 断言 aria-plugin `--no-push` 修复已在 `origin/master` 且主仓 gitlink 指向它 (v1.67
         yaml: 断言 --no-push 修复已在 aria origin/master + github/master, 主仓 gitlink 一致
     1.2 md: 记录两份子 Spec 导出物存在性 (`linked_issue_field_probe.py --emit-arg` + `lib/lin
         yaml: 记录两份子 Spec 导出物存在性与 §2 两阶段模板 live 分支 (advisory, 不阻塞 — proposal :96/:423
     1.3 md: B.1 起点重跑行号锚点核对 (7a/7c/7d 分支 + Step 9 推送点 + `_main()` 门控/except + `rele
         yaml: B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/except + release_gate 三选一
     2.1 md: SC-3: `get_container_uuid()` 单测 — 设了 `label` 的 container-id 夹具仍取 `uuid
         yaml: SC-3 红测: get_container_uuid() 在设了 label 的 container-id 夹具上仍取 uuid 字段
     2.2 md: SC-5 / SC-6 / SC-7: `heartbeat_by_track` 单测 — 跨 subprocess 第二次不同 sessi
         yaml: SC-5 / SC-6 / SC-7 红测: heartbeat_by_track 跨 session 刷新 / 一对多全刷 / sweep
     2.3 md: SC-15 (baseline 即绿回归守卫): 改名两步 `release_claim_by_track(旧)` + `acquire_c
         yaml: SC-15 回归守卫 (baseline 即绿): 改名两步无孤儿 + 无关第三方 claim 负控
     2.4 md: SC-2 / SC-8 / SC-29 (CLI 全链路 subprocess): 同 issue 不同 track-id 双方互含 (SC
         yaml: SC-2 / SC-8 / SC-29 红测 (CLI 全链路 subprocess): 互含 / 终态可见 / 自排除两组
     2.5 md: SC-24 / SC-33 / SC-25 代码臂 / SC-10 (CLI 全链路): `unknown_schema_claims` 计
         yaml: SC-24 / SC-33 / SC-25 代码臂 / SC-10 红测 (CLI 全链路): unknown 计数 / except 双 
     2.6 md: SC-23 / SC-14(a) (CLI 全链路, baseline 即绿回归守卫): A.1 原串 X acquire → `relea
         yaml: SC-23 / SC-14(a) 回归守卫 (CLI 全链路, baseline 即绿) + SC-2 ↔ SC-23 相容性断言
     2.7 md: SC-32 + SC-28 第二臂 + argparse 负控 (CLI 全链路): 无 carry-id 跑 `--heartbeat-o
         yaml: SC-32 + SC-28 第二臂 + argparse 模式校验负控 红测 (CLI 全链路)
     3.1 md: `lib/identity.py` 新增 `get_container_uuid(home_dir=None) -> str` (直取 `u
         yaml: lib/identity.py: 新增 get_container_uuid(home_dir=None) -> str (直取 uuid,
     3.2 md: `lib/claim_lifecycle.py` 新增 `heartbeat_by_track(raw_track_id, identity
         yaml: lib/claim_lifecycle.py: 新增 heartbeat_by_track (dataclasses.replace; 既有
     3.3 md: `lib/collision.py::linked_issue_overlaps` 增 keyword-only `include_term
         yaml: lib/collision.py::linked_issue_overlaps 增 keyword-only include_termina
     4.1 md: 第一处变更 ①②③④⑥: `--include-terminal` flag / `_main()` 调用处加关键字参数 / 门控放宽为 `
         yaml: phase1_gate.py 第一处变更 ①②③④⑥: --include-terminal / 门控放宽 / unknown_schema
     4.2 md: 第一处变更 ⑤: `GateResult.error` 真正携带 `"fetch_degraded"` (Step 4 `health_ch
         yaml: phase1_gate.py 第一处变更 ⑤: GateResult.error 真正携带 "fetch_degraded"
     4.3 md: 第二处变更 ⑦ + `--heartbeat-only` 模式: `--raw-track-id` `required=False` + `
         yaml: phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式 + 遥测 heartbeat 分区 + coord
     5.1 md: `phase-a-planner/SKILL.md`: frontmatter `:9` `allowed-tools` 加 `Bash, 
         yaml: phase-a-planner/SKILL.md: allowed-tools 扩权 + 独立标题级「前置: REQUIRE claim (
     5.2 md: `spec-drafter/SKILL.md`: frontmatter `:10` `allowed-tools` 加 `Bash` + 
         yaml: spec-drafter/SKILL.md: allowed-tools 加 Bash + 第二落点「前置: REQUIRE claim (
     5.3 md: carry-id 三处占位措辞 (§2.1b, 逐字 `A.1 认领时派生的那一串`): `phase-b-developer/SKILL.
         yaml: carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-developer :96-97 push 机制勘正 + sk
     5.4 md: `state-scanner/SKILL.md`: Layer L 段 (`:143-178`) 新增「Layer L A.1 heartb
         yaml: state-scanner/SKILL.md:「Layer L A.1 heartbeat 集成」四句小节 + :168 键集补 push_
     5.5 md: `state-scanner/references/layer-l-integration.md` 四处: `:15` Design A 句
         yaml: references/layer-l-integration.md 四处: :15 Design A / :45 update_heartb
     5.6 md: `config-loader/SKILL.md` 登记 `coordination` A.1 skip 语义 + 新 key `state_
         yaml: config-loader/SKILL.md 登记 A.1 skip 语义 + unattended key; DEFAULTS.json 
     5.7 md: `state-scanner/docs/coordination-ref-schema.md` §3.2 (`:129`) 追加第 6 条:
         yaml: docs/coordination-ref-schema.md §3.2 追加第 6 条: unknown_schema_claims 语义
     5.8 md: `standards/conventions/session-handoff.md` §2.3.8 (`:217`; **非** §2.3)
         yaml: standards/conventions/session-handoff.md §2.3.8: {id, desc} 之 id = 本 c
     6.1 md: SC-22 ①–⑦: 两文件各自断言 (标题正则 + 围栏外 / 切片边界 `^#{1,4}[ \t]` / 七字面量 / 幂等谓词逐字 +
         yaml: SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUST)」块机械断言 (切片 / 七字面量 / 幂等 
     6.2 md: SC-34: `phase-b-developer` / `branch-manager` / `phase-d-closer` 三文件各 
         yaml: SC-34: 三处 SKILL.md 各含逐字 `A.1 认领时派生的那一串`
     6.3 md: substitute (rule6 #6): `DEFAULTS.json` `state_scanner.coordination.{en
         yaml: substitute (rule6 #6): DEFAULTS.json coordination 三键 ↔ config-loader/S
     6.4 md: substitute (rule6 #10a): `layer-l-integration.md` 不含字面 `update_heartbe
         yaml: substitute (rule6 #10a): layer-l-integration.md 不含 `update_heartbeat` 
     6.5 md: substitute (rule6 #11): `coordination-ref-schema.md` §3.2 切片 (`### 3.2
         yaml: substitute (rule6 #11): coordination-ref-schema.md §3.2 切片含 `unknown_s
     6.6 md: 补充 substitute (rule6 #10b + #12): `layer-l-integration.md` 含标题字面 `Laye
         yaml: 补充 substitute (rule6 #10b + #12): layer-l 新节标题 + 切片含 `--heartbeat-only
     7.1 md: 照跑 `ab-suite/phase-a-planner.json` (2 evals, 零裁量; 前置 `ARIA_COORDINATIO
         yaml: 照跑 ab-suite/phase-a-planner.json (2 evals, 能力面 hunk, 零裁量)
     7.2 md: 照跑 `ab-suite/spec-drafter.json` (2 evals, 同上)
         yaml: 照跑 ab-suite/spec-drafter.json (2 evals, 能力面 hunk, 零裁量)
     7.3 md: `ab-suite/state-scanner.json` 新增 eval-13 钉点名行为 (d) (`enabled == true` 
         yaml: ab-suite/state-scanner.json 新增 eval-13 (点名行为 (d), SC-21 / SC-28 第一臂) 后
     7.4 md: 照跑 `ab-suite/phase-b-developer.json` / `branch-manager.json` / `phase-
         yaml: 照跑 ab-suite/phase-b-developer.json / branch-manager.json / phase-d-clo
     7.5 md: 覆盖外档定向 fixture: `phase-a-planner.json` 增 (a) 拼串 + `--linked-issue` 省略/
         yaml: 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b)(c)(e) 四 eval, spec-draft
     7.6 md: 套件缺口 issue: **新开** aria-plugin issue「phase-a-planner / spec-drafter 套件
         yaml: 套件缺口 issue: 新开 aria-plugin issue (A.1 入口认领编排行为零 eval 覆盖), 交叉引用 #117 / 
     8.1 md: `aria/CHANGELOG.md` 条目 + 版本 SOT 5 文件同步 (`.claude-plugin/plugin.json` /
         yaml: aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算, A.2 自判 MINOR v1.68.0)
     8.2 md: 主仓发版同步面: gitlink bump 到 post-merge master SHA + 主仓 `VERSION` + root RE
         yaml: 主仓发版同步面: gitlink bump + 主仓 VERSION + root README badge + i18n README 判
     8.3 md: follow-up 开单 (不在本 Spec, 各带去处): Impact follow-up 表 #1–#7 (`owner-contai
         yaml: follow-up 开单: Impact follow-up #1–#7 + §2.2 audit-engine 轮间 heartbeat 

```

### 检查 2 / 7 — dependencies 存在性 · 无环 · 边列表 (角色提示) · 完整缺字段表

**脚本** `check_2.py`:

```python
#!/usr/bin/env python3
"""Check 2: dependencies exist / acyclic / direction; plus full required-field miss list; plus precedent est field."""
import re, sys, yaml
ROOT = "/home/dev/Aria/openspec/changes"
SPECS = ["linked-issue-field-availability", "sibling-spec-probe", "a1-entry-claim-duplicate-work-guard"]
REQ = ["id","parent","title","status","complexity","estimated_hours","dependencies","deliverables","agent","reason","verification"]
for s in SPECS:
    print(f"\n================ {s} ================")
    d = yaml.safe_load(open(f"{ROOT}/{s}/detailed-tasks.yaml", encoding="utf-8"))
    tasks = d["tasks"]; byid = {t["id"]: t for t in tasks}
    miss = {t["id"]: [k for k in REQ if k not in t] for t in tasks}
    miss = {k: v for k, v in miss.items() if v}
    print(f"[7] full required-field miss map: {miss}")
    print(f"[7] optional 'notes' present in {sum('notes' in t for t in tasks)}/{len(tasks)}")
    # deps
    bad = [(t["id"], dep) for t in tasks for dep in t["dependencies"] if dep not in byid]
    print(f"[2] dangling deps: {bad or 'none'}")
    selfdep = [t["id"] for t in tasks if t["id"] in t["dependencies"]]
    print(f"[2] self-deps: {selfdep or 'none'}")
    # cycle detection (Kahn)
    indeg = {t["id"]: len(t["dependencies"]) for t in tasks}
    succ = {t["id"]: [] for t in tasks}
    for t in tasks:
        for dep in t["dependencies"]:
            if dep in succ: succ[dep].append(t["id"])
    q = [i for i, n in indeg.items() if n == 0]; order = []
    while q:
        n = q.pop(0); order.append(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0: q.append(m)
    print(f"[2] acyclic: {len(order) == len(tasks)} (topo-sorted {len(order)}/{len(tasks)}); roots={[i for i,t in byid.items() if not t['dependencies']]}")
    # forward-only? (dep id < task id numerically)
    backward = [(t["id"], dep) for t in tasks for dep in t["dependencies"] if int(dep[5:]) > int(t["id"][5:])]
    print(f"[2] deps pointing to a LATER id (not necessarily wrong, review): {backward or 'none'}")
    # edges listing with role hints
    def role(t):
        ti = t["title"]; dl = " ".join(t["deliverables"] or [])
        if "/tests/" in dl or "红测" in ti or "RED" in ti or "测试" in ti or "断言" in ti: r = "TEST"
        elif "ab-" in dl or "AB" in ti or "照跑" in ti or "fixture" in ti: r = "AB"
        elif dl.endswith(".md") or "SKILL.md" in dl or ".md" in dl or "CHANGELOG" in dl: r = "DOC"
        elif ".py" in dl or ".json" in dl or ".yaml" in dl or ".txt" in dl: r = "IMPL"
        else: r = "OTHER"
        return r
    print("[2] edges (task <- dep) with role hints:")
    for t in tasks:
        for dep in t["dependencies"]:
            print(f"    {t['id']}[{role(t)}:{t['agent']}] <- {dep}[{role(byid[dep])}:{byid[dep]['agent']}]  | {t['title'][:45]} <- {byid[dep]['title'][:45]}")

```

**输出**:

```text

================ linked-issue-field-availability ================
[7] full required-field miss map: {'TASK-001': ['estimated_hours'], 'TASK-002': ['estimated_hours'], 'TASK-003': ['estimated_hours'], 'TASK-004': ['estimated_hours'], 'TASK-005': ['estimated_hours'], 'TASK-006': ['estimated_hours'], 'TASK-007': ['estimated_hours'], 'TASK-008': ['estimated_hours'], 'TASK-009': ['estimated_hours'], 'TASK-010': ['estimated_hours'], 'TASK-011': ['estimated_hours'], 'TASK-012': ['estimated_hours'], 'TASK-013': ['estimated_hours'], 'TASK-014': ['estimated_hours'], 'TASK-015': ['estimated_hours'], 'TASK-016': ['estimated_hours'], 'TASK-017': ['estimated_hours'], 'TASK-018': ['estimated_hours'], 'TASK-019': ['estimated_hours'], 'TASK-020': ['estimated_hours', 'reason'], 'TASK-021': ['estimated_hours'], 'TASK-022': ['estimated_hours'], 'TASK-023': ['estimated_hours'], 'TASK-024': ['estimated_hours'], 'TASK-025': ['estimated_hours']}
[7] optional 'notes' present in 9/25
[2] dangling deps: none
[2] self-deps: none
[2] acyclic: True (topo-sorted 25/25); roots=['TASK-001', 'TASK-002', 'TASK-003', 'TASK-004', 'TASK-005', 'TASK-012']
[2] deps pointing to a LATER id (not necessarily wrong, review): none
[2] edges (task <- dep) with role hints:
    TASK-006[TEST:qa-engineer] <- TASK-001[TEST:qa-engineer]  | 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器 <- SC-1 E0 定位夹具 (a)–(h) + SC-2 E2 起始位 (逐字复用真实语料)
    TASK-006[TEST:qa-engineer] <- TASK-002[TEST:qa-engineer]  | 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器 <- SC-3 多值 E4/E5/E6 + SC-4 哨兵六分支 (E5 吃 E3 原始串)
    TASK-006[TEST:qa-engineer] <- TASK-003[TEST:qa-engineer]  | 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器 <- SC-5 探针 check 模式六臂 — CLI 全链路 subprocess + 真实降
    TASK-006[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器 <- SC-9 --emit-arg 四夹具 CLI 全链路 (失败态 stdout 必空)
    TASK-007[IMPL:backend-architect] <- TASK-001[TEST:qa-engineer]  | lib/linked_issue_field.py — E0–E6 纯函数 + Field <- SC-1 E0 定位夹具 (a)–(h) + SC-2 E2 起始位 (逐字复用真实语料)
    TASK-007[IMPL:backend-architect] <- TASK-002[TEST:qa-engineer]  | lib/linked_issue_field.py — E0–E6 纯函数 + Field <- SC-3 多值 E4/E5/E6 + SC-4 哨兵六分支 (E5 吃 E3 原始串)
    TASK-008[IMPL:backend-architect] <- TASK-007[IMPL:backend-architect]  | scripts/linked_issue_field_probe.py — check 模 <- lib/linked_issue_field.py — E0–E6 纯函数 + Field
    TASK-008[IMPL:backend-architect] <- TASK-003[TEST:qa-engineer]  | scripts/linked_issue_field_probe.py — check 模 <- SC-5 探针 check 模式六臂 — CLI 全链路 subprocess + 真实降
    TASK-009[IMPL:backend-architect] <- TASK-007[IMPL:backend-architect]  | 同脚本 --emit-arg <proposal.md> 模式 — E6 四格表 CLI  <- lib/linked_issue_field.py — E0–E6 纯函数 + Field
    TASK-009[IMPL:backend-architect] <- TASK-004[TEST:qa-engineer]  | 同脚本 --emit-arg <proposal.md> 模式 — E6 四格表 CLI  <- SC-9 --emit-arg 四夹具 CLI 全链路 (失败态 stdout 必空)
    TASK-010[IMPL:backend-architect] <- TASK-008[IMPL:backend-architect]  | .aria/linked-issue-field-grandfathered.txt —  <- scripts/linked_issue_field_probe.py — check 模
    TASK-011[IMPL:backend-architect] <- TASK-008[IMPL:backend-architect]  | .aria/state-checks.yaml 注册 linked-issue-field <- scripts/linked_issue_field_probe.py — check 模
    TASK-011[IMPL:backend-architect] <- TASK-010[IMPL:backend-architect]  | .aria/state-checks.yaml 注册 linked-issue-field <- .aria/linked-issue-field-grandfathered.txt — 
    TASK-013[DOC:knowledge-manager] <- TASK-005[TEST:qa-engineer]  | standards/openspec/templates/proposal-minimal <- SC-6 模板 SOT + SC-7a 预览围栏 + SC-8 注册/分发面/实跑 (结构
    TASK-014[DOC:knowledge-manager] <- TASK-005[TEST:qa-engineer]  | spec-drafter/SKILL.md hunk A — 正文声明 Linked Is <- SC-6 模板 SOT + SC-7a 预览围栏 + SC-8 注册/分发面/实跑 (结构
    TASK-015[DOC:knowledge-manager] <- TASK-005[TEST:qa-engineer]  | spec-drafter/SKILL.md hunk B — Level 2 预览围栏头部 <- SC-6 模板 SOT + SC-7a 预览围栏 + SC-8 注册/分发面/实跑 (结构
    TASK-016[AB:qa-engineer] <- TASK-014[DOC:knowledge-manager]  | 用 /skill-creator 对 hunk A + hunk B 照跑 ab-suit <- spec-drafter/SKILL.md hunk A — 正文声明 Linked Is
    TASK-016[AB:qa-engineer] <- TASK-015[DOC:knowledge-manager]  | 用 /skill-creator 对 hunk A + hunk B 照跑 ab-suit <- spec-drafter/SKILL.md hunk B — Level 2 预览围栏头部
    TASK-017[AB:qa-engineer] <- TASK-014[DOC:knowledge-manager]  | 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.jso <- spec-drafter/SKILL.md hunk A — 正文声明 Linked Is
    TASK-017[AB:qa-engineer] <- TASK-015[DOC:knowledge-manager]  | 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.jso <- spec-drafter/SKILL.md hunk B — Level 2 预览围栏头部
    TASK-018[AB:knowledge-manager] <- TASK-017[AB:qa-engineer]  | 套件缺口 issue — 归并 aria-plugin#117 (评论追加本 Spec 为 <- 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.jso
    TASK-019[AB:qa-engineer] <- TASK-006[TEST:qa-engineer]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器
    TASK-019[AB:qa-engineer] <- TASK-007[IMPL:backend-architect]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- lib/linked_issue_field.py — E0–E6 纯函数 + Field
    TASK-019[AB:qa-engineer] <- TASK-008[IMPL:backend-architect]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- scripts/linked_issue_field_probe.py — check 模
    TASK-019[AB:qa-engineer] <- TASK-009[IMPL:backend-architect]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- 同脚本 --emit-arg <proposal.md> 模式 — E6 四格表 CLI 
    TASK-019[AB:qa-engineer] <- TASK-011[IMPL:backend-architect]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- .aria/state-checks.yaml 注册 linked-issue-field
    TASK-019[AB:qa-engineer] <- TASK-013[DOC:knowledge-manager]  | substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk  <- standards/openspec/templates/proposal-minimal
    TASK-020[TEST:qa-engineer] <- TASK-006[TEST:qa-engineer]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- 坏实现拒绝矩阵 — 「它怎么会红」列机械化为同文件内 _bad_* 抽取器
    TASK-020[TEST:qa-engineer] <- TASK-007[IMPL:backend-architect]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- lib/linked_issue_field.py — E0–E6 纯函数 + Field
    TASK-020[TEST:qa-engineer] <- TASK-008[IMPL:backend-architect]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- scripts/linked_issue_field_probe.py — check 模
    TASK-020[TEST:qa-engineer] <- TASK-009[IMPL:backend-architect]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- 同脚本 --emit-arg <proposal.md> 模式 — E6 四格表 CLI 
    TASK-020[TEST:qa-engineer] <- TASK-010[IMPL:backend-architect]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- .aria/linked-issue-field-grandfathered.txt — 
    TASK-020[TEST:qa-engineer] <- TASK-011[IMPL:backend-architect]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- .aria/state-checks.yaml 注册 linked-issue-field
    TASK-020[TEST:qa-engineer] <- TASK-013[DOC:knowledge-manager]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- standards/openspec/templates/proposal-minimal
    TASK-020[TEST:qa-engineer] <- TASK-014[DOC:knowledge-manager]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- spec-drafter/SKILL.md hunk A — 正文声明 Linked Is
    TASK-020[TEST:qa-engineer] <- TASK-015[DOC:knowledge-manager]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- spec-drafter/SKILL.md hunk B — Level 2 预览围栏头部
    TASK-020[TEST:qa-engineer] <- TASK-016[AB:qa-engineer]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- 用 /skill-creator 对 hunk A + hunk B 照跑 ab-suit
    TASK-020[TEST:qa-engineer] <- TASK-017[AB:qa-engineer]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- 可证伪定向 fixture ×1 (SC-7 双臂) — spec-drafter.jso
    TASK-020[TEST:qa-engineer] <- TASK-019[AB:qa-engineer]  | 全量回归 — run_tests.py OK + run_all_tests.sh 0 F <- substitute 留痕 — 基线 worktree 红 / 实现后绿, 逐 hunk 
    TASK-021[DOC:knowledge-manager] <- TASK-020[TEST:qa-engineer]  | aria 子模块版本面 bump — 按引用点 (plugin.json SOT / ma <- 全量回归 — run_tests.py OK + run_all_tests.sh 0 F
    TASK-022[OTHER:tech-lead] <- TASK-021[DOC:knowledge-manager]  | aria 子模块本地 merge → master + 双推 + 逐 remote ls- <- aria 子模块版本面 bump — 按引用点 (plugin.json SOT / ma
    TASK-023[OTHER:tech-lead] <- TASK-013[DOC:knowledge-manager]  | standards 子模块本地 merge → master + 双推 + ls-remo <- standards/openspec/templates/proposal-minimal
    TASK-023[OTHER:tech-lead] <- TASK-020[TEST:qa-engineer]  | standards 子模块本地 merge → master + 双推 + ls-remo <- 全量回归 — run_tests.py OK + run_all_tests.sh 0 F
    TASK-024[DOC:knowledge-manager] <- TASK-022[OTHER:tech-lead]  | 主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n × <- aria 子模块本地 merge → master + 双推 + 逐 remote ls-
    TASK-025[OTHER:tech-lead] <- TASK-012[DOC:qa-engineer]  | 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge <- A.2 显式验收项 (:388): 实测 ${CLAUDE_PLUGIN_ROOT} 是否
    TASK-025[OTHER:tech-lead] <- TASK-018[AB:knowledge-manager]  | 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge <- 套件缺口 issue — 归并 aria-plugin#117 (评论追加本 Spec 为
    TASK-025[OTHER:tech-lead] <- TASK-022[OTHER:tech-lead]  | 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge <- aria 子模块本地 merge → master + 双推 + 逐 remote ls-
    TASK-025[OTHER:tech-lead] <- TASK-023[OTHER:tech-lead]  | 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge <- standards 子模块本地 merge → master + 双推 + ls-remo
    TASK-025[OTHER:tech-lead] <- TASK-024[DOC:knowledge-manager]  | 主仓 PR — 交付 phase-c-integrator C.2.4 pre-merge <- 主仓版本引用面 — VERSION:24 + README.md 2 点 + i18n ×

================ sibling-spec-probe ================
[7] full required-field miss map: {'TASK-001': ['estimated_hours'], 'TASK-002': ['estimated_hours'], 'TASK-003': ['estimated_hours'], 'TASK-004': ['estimated_hours'], 'TASK-005': ['estimated_hours'], 'TASK-006': ['estimated_hours'], 'TASK-007': ['estimated_hours'], 'TASK-008': ['estimated_hours'], 'TASK-009': ['estimated_hours'], 'TASK-010': ['estimated_hours'], 'TASK-011': ['estimated_hours'], 'TASK-012': ['estimated_hours'], 'TASK-013': ['estimated_hours'], 'TASK-014': ['estimated_hours'], 'TASK-015': ['estimated_hours'], 'TASK-016': ['estimated_hours'], 'TASK-017': ['estimated_hours'], 'TASK-018': ['estimated_hours']}
[7] optional 'notes' present in 18/18
[2] dangling deps: none
[2] self-deps: none
[2] acyclic: True (topo-sorted 18/18); roots=['TASK-001', 'TASK-002', 'TASK-003']
[2] deps pointing to a LATER id (not necessarily wrong, review): none
[2] edges (task <- dep) with role hints:
    TASK-004[TEST:qa-engineer] <- TASK-001[TEST:tech-lead]  | 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控) <- 前置断言: 姊妹纯函数 lib/linked_issue_field.py 已存在且导出所
    TASK-004[TEST:qa-engineer] <- TASK-002[AB:qa-engineer]  | 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控) <- 基线三态记录: audit-engine 现状 + 锚点复核 + SC-17/20/21 
    TASK-005[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | 谓词层测试 (纯函数): SC-7 / SC-8 / SC-9 / SC-10 / SC- <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-006[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | SC-18 层 0 假阳性拒绝四臂 (cc1bdef 147 篇 + 合成围栏夹具) +  <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-007[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | 远端解析 / fetch / cap 测试 (注入式 git runner): SC-12 <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-008[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | CLI 全链路契约测试 (subprocess): SC-15 三终局 stdout 恰一 <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-009[TEST:qa-engineer] <- TASK-004[TEST:qa-engineer]  | 指令面结构断言 (RED): SC-17 分块计数 + 负控 / SC-20 (i) SK <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-010[IMPL:backend-architect] <- TASK-004[TEST:qa-engineer]  | 探针骨架 + I/O 边界: CLI / 唯一 import 块 / own propos <- 测试骨架 + 前置 skip 守卫 + SC-21 import 顺序断言 (含反序负控)
    TASK-010[IMPL:backend-architect] <- TASK-008[TEST:qa-engineer]  | 探针骨架 + I/O 边界: CLI / 唯一 import 块 / own propos <- CLI 全链路契约测试 (subprocess): SC-15 三终局 stdout 恰一
    TASK-011[IMPL:backend-architect] <- TASK-010[IMPL:backend-architect]  | 谓词层: 四态 → 层分派 / 哨兵层 1.5 / 层 2 URL 回落 / 键构造 /  <- 探针骨架 + I/O 边界: CLI / 唯一 import 块 / own propos
    TASK-011[IMPL:backend-architect] <- TASK-005[TEST:qa-engineer]  | 谓词层: 四态 → 层分派 / 哨兵层 1.5 / 层 2 URL 回落 / 键构造 /  <- 谓词层测试 (纯函数): SC-7 / SC-8 / SC-9 / SC-10 / SC-
    TASK-011[IMPL:backend-architect] <- TASK-006[TEST:qa-engineer]  | 谓词层: 四态 → 层分派 / 哨兵层 1.5 / 层 2 URL 回落 / 键构造 /  <- SC-18 层 0 假阳性拒绝四臂 (cc1bdef 147 篇 + 合成围栏夹具) + 
    TASK-012[IMPL:backend-architect] <- TASK-010[IMPL:backend-architect]  | remote 集合 + 默认分支 fail-closed (ls-remote --sym <- 探针骨架 + I/O 边界: CLI / 唯一 import 块 / own propos
    TASK-012[IMPL:backend-architect] <- TASK-007[TEST:qa-engineer]  | remote 集合 + 默认分支 fail-closed (ls-remote --sym <- 远端解析 / fetch / cap 测试 (注入式 git runner): SC-12
    TASK-013[IMPL:backend-architect] <- TASK-012[IMPL:backend-architect]  | 语料枚举 (ls-tree on 私有 ref, changes 先 archive 后, <- remote 集合 + 默认分支 fail-closed (ls-remote --sym
    TASK-013[IMPL:backend-architect] <- TASK-007[TEST:qa-engineer]  | 语料枚举 (ls-tree on 私有 ref, changes 先 archive 后, <- 远端解析 / fetch / cap 测试 (注入式 git runner): SC-12
    TASK-014[TEST:backend-architect] <- TASK-011[IMPL:backend-architect]  | GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 /  <- 谓词层: 四态 → 层分派 / 哨兵层 1.5 / 层 2 URL 回落 / 键构造 / 
    TASK-014[TEST:backend-architect] <- TASK-012[IMPL:backend-architect]  | GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 /  <- remote 集合 + 默认分支 fail-closed (ls-remote --sym
    TASK-014[TEST:backend-architect] <- TASK-013[IMPL:backend-architect]  | GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 /  <- 语料枚举 (ls-tree on 私有 ref, changes 先 archive 后,
    TASK-015[DOC:knowledge-manager] <- TASK-009[TEST:qa-engineer]  | execution-modes.md: Convergence / Challenge 两 <- 指令面结构断言 (RED): SC-17 分块计数 + 负控 / SC-20 (i) SK
    TASK-016[DOC:knowledge-manager] <- TASK-009[TEST:qa-engineer]  | SKILL.md 「per-round 入口探针」小节 (概述 + 指针 + 四字面 +  <- 指令面结构断言 (RED): SC-17 分块计数 + 负控 / SC-20 (i) SK
    TASK-016[DOC:knowledge-manager] <- TASK-015[DOC:knowledge-manager]  | SKILL.md 「per-round 入口探针」小节 (概述 + 指针 + 四字面 +  <- execution-modes.md: Convergence / Challenge 两
    TASK-017[AB:qa-engineer] <- TASK-003[AB:qa-engineer]  | /skill-creator benchmark audit-engine 双臂实跑 (w <- 建 ab-suite/audit-engine.json (经 /skill-creato
    TASK-017[AB:qa-engineer] <- TASK-014[TEST:backend-architect]  | /skill-creator benchmark audit-engine 双臂实跑 (w <- GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 / 
    TASK-017[AB:qa-engineer] <- TASK-015[DOC:knowledge-manager]  | /skill-creator benchmark audit-engine 双臂实跑 (w <- execution-modes.md: Convergence / Challenge 两
    TASK-017[AB:qa-engineer] <- TASK-016[DOC:knowledge-manager]  | /skill-creator benchmark audit-engine 双臂实跑 (w <- SKILL.md 「per-round 入口探针」小节 (概述 + 指针 + 四字面 + 
    TASK-018[DOC:knowledge-manager] <- TASK-017[AB:qa-engineer]  | 发布同步面 (aria 子模块): CHANGELOG + plugin.json (SO <- /skill-creator benchmark audit-engine 双臂实跑 (w

================ a1-entry-claim-duplicate-work-guard ================
[7] full required-field miss map: {}
[7] optional 'notes' present in 39/39
[2] dangling deps: none
[2] self-deps: none
[2] acyclic: True (topo-sorted 39/39); roots=['TASK-001', 'TASK-002', 'TASK-003']
[2] deps pointing to a LATER id (not necessarily wrong, review): [('TASK-017', 'TASK-022')]
[2] edges (task <- dep) with role hints:
    TASK-004[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-3 红测: get_container_uuid() 在设了 label 的 con <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-005[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-5 / SC-6 / SC-7 红测: heartbeat_by_track 跨 s <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-006[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-15 回归守卫 (baseline 即绿): 改名两步无孤儿 + 无关第三方 cla <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-007[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-2 / SC-8 / SC-29 红测 (CLI 全链路 subprocess):  <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-008[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-24 / SC-33 / SC-25 代码臂 / SC-10 红测 (CLI 全链路 <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-009[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-23 / SC-14(a) 回归守卫 (CLI 全链路, baseline 即绿)  <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-010[TEST:qa-engineer] <- TASK-003[DOC:tech-lead]  | SC-32 + SC-28 第二臂 + argparse 模式校验负控 红测 (CLI 全 <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-011[IMPL:backend-architect] <- TASK-004[TEST:qa-engineer]  | lib/identity.py: 新增 get_container_uuid(home_d <- SC-3 红测: get_container_uuid() 在设了 label 的 con
    TASK-012[IMPL:backend-architect] <- TASK-005[TEST:qa-engineer]  | lib/claim_lifecycle.py: 新增 heartbeat_by_track <- SC-5 / SC-6 / SC-7 红测: heartbeat_by_track 跨 s
    TASK-012[IMPL:backend-architect] <- TASK-006[TEST:qa-engineer]  | lib/claim_lifecycle.py: 新增 heartbeat_by_track <- SC-15 回归守卫 (baseline 即绿): 改名两步无孤儿 + 无关第三方 cla
    TASK-013[IMPL:backend-architect] <- TASK-007[TEST:qa-engineer]  | lib/collision.py::linked_issue_overlaps 增 key <- SC-2 / SC-8 / SC-29 红测 (CLI 全链路 subprocess): 
    TASK-014[IMPL:backend-architect] <- TASK-008[TEST:qa-engineer]  | phase1_gate.py 第一处变更 ①②③④⑥: --include-termina <- SC-24 / SC-33 / SC-25 代码臂 / SC-10 红测 (CLI 全链路
    TASK-014[IMPL:backend-architect] <- TASK-013[IMPL:backend-architect]  | phase1_gate.py 第一处变更 ①②③④⑥: --include-termina <- lib/collision.py::linked_issue_overlaps 增 key
    TASK-015[IMPL:backend-architect] <- TASK-008[TEST:qa-engineer]  | phase1_gate.py 第一处变更 ⑤: GateResult.error 真正携带 <- SC-24 / SC-33 / SC-25 代码臂 / SC-10 红测 (CLI 全链路
    TASK-015[IMPL:backend-architect] <- TASK-014[IMPL:backend-architect]  | phase1_gate.py 第一处变更 ⑤: GateResult.error 真正携带 <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-016[IMPL:backend-architect] <- TASK-010[TEST:qa-engineer]  | phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式  <- SC-32 + SC-28 第二臂 + argparse 模式校验负控 红测 (CLI 全
    TASK-016[IMPL:backend-architect] <- TASK-012[IMPL:backend-architect]  | phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式  <- lib/claim_lifecycle.py: 新增 heartbeat_by_track
    TASK-016[IMPL:backend-architect] <- TASK-014[IMPL:backend-architect]  | phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式  <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-017[DOC:knowledge-manager] <- TASK-002[IMPL:tech-lead]  | phase-a-planner/SKILL.md: allowed-tools 扩权 +  <- 记录两份子 Spec 导出物存在性与 §2 两阶段模板 live 分支 (advisory
    TASK-017[DOC:knowledge-manager] <- TASK-014[IMPL:backend-architect]  | phase-a-planner/SKILL.md: allowed-tools 扩权 +  <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-017[DOC:knowledge-manager] <- TASK-016[IMPL:backend-architect]  | phase-a-planner/SKILL.md: allowed-tools 扩权 +  <- phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式 
    TASK-017[DOC:knowledge-manager] <- TASK-022[DOC:knowledge-manager]  | phase-a-planner/SKILL.md: allowed-tools 扩权 +  <- config-loader/SKILL.md 登记 A.1 skip 语义 + unatt
    TASK-018[DOC:knowledge-manager] <- TASK-002[IMPL:tech-lead]  | spec-drafter/SKILL.md: allowed-tools 加 Bash + <- 记录两份子 Spec 导出物存在性与 §2 两阶段模板 live 分支 (advisory
    TASK-018[DOC:knowledge-manager] <- TASK-014[IMPL:backend-architect]  | spec-drafter/SKILL.md: allowed-tools 加 Bash + <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-019[DOC:knowledge-manager] <- TASK-003[DOC:tech-lead]  | carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-develo <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-020[DOC:knowledge-manager] <- TASK-016[IMPL:backend-architect]  | state-scanner/SKILL.md:「Layer L A.1 heartbeat <- phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式 
    TASK-021[DOC:knowledge-manager] <- TASK-016[IMPL:backend-architect]  | references/layer-l-integration.md 四处: :15 Des <- phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式 
    TASK-021[DOC:knowledge-manager] <- TASK-020[DOC:knowledge-manager]  | references/layer-l-integration.md 四处: :15 Des <- state-scanner/SKILL.md:「Layer L A.1 heartbeat
    TASK-022[DOC:knowledge-manager] <- TASK-003[DOC:tech-lead]  | config-loader/SKILL.md 登记 A.1 skip 语义 + unatt <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/
    TASK-023[DOC:knowledge-manager] <- TASK-014[IMPL:backend-architect]  | docs/coordination-ref-schema.md §3.2 追加第 6 条: <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-024[DOC:knowledge-manager] <- TASK-019[DOC:knowledge-manager]  | standards/conventions/session-handoff.md §2.3 <- carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-develo
    TASK-025[TEST:qa-engineer] <- TASK-017[DOC:knowledge-manager]  | SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUS <- phase-a-planner/SKILL.md: allowed-tools 扩权 + 
    TASK-025[TEST:qa-engineer] <- TASK-018[DOC:knowledge-manager]  | SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUS <- spec-drafter/SKILL.md: allowed-tools 加 Bash +
    TASK-026[TEST:qa-engineer] <- TASK-019[DOC:knowledge-manager]  | SC-34: 三处 SKILL.md 各含逐字 `A.1 认领时派生的那一串` <- carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-develo
    TASK-027[TEST:qa-engineer] <- TASK-022[DOC:knowledge-manager]  | substitute (rule6 #6): DEFAULTS.json coordina <- config-loader/SKILL.md 登记 A.1 skip 语义 + unatt
    TASK-028[TEST:qa-engineer] <- TASK-021[DOC:knowledge-manager]  | substitute (rule6 #10a): layer-l-integration. <- references/layer-l-integration.md 四处: :15 Des
    TASK-029[TEST:qa-engineer] <- TASK-023[DOC:knowledge-manager]  | substitute (rule6 #11): coordination-ref-sche <- docs/coordination-ref-schema.md §3.2 追加第 6 条:
    TASK-030[TEST:qa-engineer] <- TASK-020[DOC:knowledge-manager]  | 补充 substitute (rule6 #10b + #12): layer-l 新节标 <- state-scanner/SKILL.md:「Layer L A.1 heartbeat
    TASK-030[TEST:qa-engineer] <- TASK-021[DOC:knowledge-manager]  | 补充 substitute (rule6 #10b + #12): layer-l 新节标 <- references/layer-l-integration.md 四处: :15 Des
    TASK-031[AB:qa-engineer] <- TASK-001[TEST:tech-lead]  | 照跑 ab-suite/phase-a-planner.json (2 evals, 能力 <- 断言 --no-push 修复已在 aria origin/master + github
    TASK-031[AB:qa-engineer] <- TASK-017[DOC:knowledge-manager]  | 照跑 ab-suite/phase-a-planner.json (2 evals, 能力 <- phase-a-planner/SKILL.md: allowed-tools 扩权 + 
    TASK-031[AB:qa-engineer] <- TASK-025[TEST:qa-engineer]  | 照跑 ab-suite/phase-a-planner.json (2 evals, 能力 <- SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUS
    TASK-032[AB:qa-engineer] <- TASK-001[TEST:tech-lead]  | 照跑 ab-suite/spec-drafter.json (2 evals, 能力面 h <- 断言 --no-push 修复已在 aria origin/master + github
    TASK-032[AB:qa-engineer] <- TASK-018[DOC:knowledge-manager]  | 照跑 ab-suite/spec-drafter.json (2 evals, 能力面 h <- spec-drafter/SKILL.md: allowed-tools 加 Bash +
    TASK-032[AB:qa-engineer] <- TASK-025[TEST:qa-engineer]  | 照跑 ab-suite/spec-drafter.json (2 evals, 能力面 h <- SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUS
    TASK-033[AB:qa-engineer] <- TASK-001[TEST:tech-lead]  | ab-suite/state-scanner.json 新增 eval-13 (点名行为  <- 断言 --no-push 修复已在 aria origin/master + github
    TASK-033[AB:qa-engineer] <- TASK-020[DOC:knowledge-manager]  | ab-suite/state-scanner.json 新增 eval-13 (点名行为  <- state-scanner/SKILL.md:「Layer L A.1 heartbeat
    TASK-033[AB:qa-engineer] <- TASK-021[DOC:knowledge-manager]  | ab-suite/state-scanner.json 新增 eval-13 (点名行为  <- references/layer-l-integration.md 四处: :15 Des
    TASK-033[AB:qa-engineer] <- TASK-030[TEST:qa-engineer]  | ab-suite/state-scanner.json 新增 eval-13 (点名行为  <- 补充 substitute (rule6 #10b + #12): layer-l 新节标
    TASK-034[AB:qa-engineer] <- TASK-001[TEST:tech-lead]  | 照跑 ab-suite/phase-b-developer.json / branch-m <- 断言 --no-push 修复已在 aria origin/master + github
    TASK-034[AB:qa-engineer] <- TASK-019[DOC:knowledge-manager]  | 照跑 ab-suite/phase-b-developer.json / branch-m <- carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-develo
    TASK-034[AB:qa-engineer] <- TASK-026[TEST:qa-engineer]  | 照跑 ab-suite/phase-b-developer.json / branch-m <- SC-34: 三处 SKILL.md 各含逐字 `A.1 认领时派生的那一串`
    TASK-035[AB:qa-engineer] <- TASK-001[TEST:tech-lead]  | 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b) <- 断言 --no-push 修复已在 aria origin/master + github
    TASK-035[AB:qa-engineer] <- TASK-017[DOC:knowledge-manager]  | 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b) <- phase-a-planner/SKILL.md: allowed-tools 扩权 + 
    TASK-035[AB:qa-engineer] <- TASK-018[DOC:knowledge-manager]  | 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b) <- spec-drafter/SKILL.md: allowed-tools 加 Bash +
    TASK-035[AB:qa-engineer] <- TASK-022[DOC:knowledge-manager]  | 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b) <- config-loader/SKILL.md 登记 A.1 skip 语义 + unatt
    TASK-036[OTHER:tech-lead] <- TASK-035[AB:qa-engineer]  | 套件缺口 issue: 新开 aria-plugin issue (A.1 入口认领编排行 <- 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b)
    TASK-037[DOC:knowledge-manager] <- TASK-011[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- lib/identity.py: 新增 get_container_uuid(home_d
    TASK-037[DOC:knowledge-manager] <- TASK-012[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- lib/claim_lifecycle.py: 新增 heartbeat_by_track
    TASK-037[DOC:knowledge-manager] <- TASK-013[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- lib/collision.py::linked_issue_overlaps 增 key
    TASK-037[DOC:knowledge-manager] <- TASK-014[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- phase1_gate.py 第一处变更 ①②③④⑥: --include-termina
    TASK-037[DOC:knowledge-manager] <- TASK-015[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- phase1_gate.py 第一处变更 ⑤: GateResult.error 真正携带
    TASK-037[DOC:knowledge-manager] <- TASK-016[IMPL:backend-architect]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- phase1_gate.py 第二处变更 ⑦ + --heartbeat-only 模式 
    TASK-037[DOC:knowledge-manager] <- TASK-017[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- phase-a-planner/SKILL.md: allowed-tools 扩权 + 
    TASK-037[DOC:knowledge-manager] <- TASK-018[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- spec-drafter/SKILL.md: allowed-tools 加 Bash +
    TASK-037[DOC:knowledge-manager] <- TASK-019[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- carry-id 三处占位措辞 (§2.1b 选项 A) + phase-b-develo
    TASK-037[DOC:knowledge-manager] <- TASK-020[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- state-scanner/SKILL.md:「Layer L A.1 heartbeat
    TASK-037[DOC:knowledge-manager] <- TASK-021[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- references/layer-l-integration.md 四处: :15 Des
    TASK-037[DOC:knowledge-manager] <- TASK-022[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- config-loader/SKILL.md 登记 A.1 skip 语义 + unatt
    TASK-037[DOC:knowledge-manager] <- TASK-023[DOC:knowledge-manager]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- docs/coordination-ref-schema.md §3.2 追加第 6 条:
    TASK-037[DOC:knowledge-manager] <- TASK-025[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUS
    TASK-037[DOC:knowledge-manager] <- TASK-026[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- SC-34: 三处 SKILL.md 各含逐字 `A.1 认领时派生的那一串`
    TASK-037[DOC:knowledge-manager] <- TASK-027[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- substitute (rule6 #6): DEFAULTS.json coordina
    TASK-037[DOC:knowledge-manager] <- TASK-028[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- substitute (rule6 #10a): layer-l-integration.
    TASK-037[DOC:knowledge-manager] <- TASK-029[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- substitute (rule6 #11): coordination-ref-sche
    TASK-037[DOC:knowledge-manager] <- TASK-030[TEST:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- 补充 substitute (rule6 #10b + #12): layer-l 新节标
    TASK-037[DOC:knowledge-manager] <- TASK-031[AB:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- 照跑 ab-suite/phase-a-planner.json (2 evals, 能力
    TASK-037[DOC:knowledge-manager] <- TASK-032[AB:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- 照跑 ab-suite/spec-drafter.json (2 evals, 能力面 h
    TASK-037[DOC:knowledge-manager] <- TASK-033[AB:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- ab-suite/state-scanner.json 新增 eval-13 (点名行为 
    TASK-037[DOC:knowledge-manager] <- TASK-034[AB:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- 照跑 ab-suite/phase-b-developer.json / branch-m
    TASK-037[DOC:knowledge-manager] <- TASK-035[AB:qa-engineer]  | aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算 <- 覆盖外档定向 fixture: phase-a-planner.json 增 (a)(b)
    TASK-038[DOC:tech-lead] <- TASK-037[DOC:knowledge-manager]  | 主仓发版同步面: gitlink bump + 主仓 VERSION + root REA <- aria/CHANGELOG.md 条目 + 版本 SOT 5 文件同步 (号段落地时计算
    TASK-039[OTHER:tech-lead] <- TASK-003[DOC:tech-lead]  | follow-up 开单: Impact follow-up #1–#7 + §2.2 a <- B.1 起点重跑行号锚点核对 (7a/7c/7d + Step 9 + _main 门控/

```

### 检查 2 (方向) — Group 6 依赖方向与 verification 成环 (Critical 证据) + finding id 计算

**脚本** `check_crit_ids.py`:

```python
import yaml, re, hashlib
d = yaml.safe_load(open("/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml", encoding="utf-8"))
byid = {t["id"]: t for t in d["tasks"]}
print("[2-dir] Group 6 test tasks -> their dependencies (all point at the text tasks they test):")
for tid in ["TASK-025","TASK-026","TASK-027","TASK-028","TASK-029","TASK-030"]:
    t = byid[tid]; print(f"   {tid} deps={t['dependencies']}  title={t['title'][:60]}")
print("[2-dir] Text tasks whose FIRST verification item requires a Group-6 test to be green (the test depends on this very task):")
for tid in ["TASK-017","TASK-018","TASK-019","TASK-020","TASK-021","TASK-022","TASK-023"]:
    v0 = byid[tid]["verification"][0]; refs = re.findall(r"TASK-0(?:2[5-9]|30)", v0)
    cyc = [r for r in refs if tid in byid[r]["dependencies"]]
    print(f"   {tid} verification[0]={v0[:70]!r} refs={refs} cycle_with={cyc}")
print("[2-dir] TASK-025 notes:", repr(byid["TASK-025"]["notes"].strip()[:120]))
print("[2-dir] TASK-027 notes:", repr(byid["TASK-027"]["notes"].strip()[:120]))
print("[2-dir] contrast Group 2/3 (impl depends on RED test): TASK-011 deps", byid["TASK-011"]["dependencies"], "| TASK-014 deps", byid["TASK-014"]["dependencies"])
d2 = yaml.safe_load(open("/home/dev/Aria/openspec/changes/linked-issue-field-availability/detailed-tasks.yaml", encoding="utf-8"))
b2 = {t["id"]: t for t in d2["tasks"]}; print("[2-dir] contrast sister linked-issue: TASK-014/015 deps ->", b2["TASK-014"]["dependencies"], b2["TASK-015"]["dependencies"], "(TASK-005 = RED structural test)")
def fid(cat, scope, sev, typ): return hashlib.sha256(f"{cat}:{scope}:{sev}:{typ}".encode()).hexdigest()[:8]
for f in [("testing","openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml","critical","issue"),
 ("implementation","openspec/changes/{linked-issue-field-availability,sibling-spec-probe}/detailed-tasks.yaml","major","issue"),
 ("documentation","openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md","major","issue"),
 ("implementation","openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml","major","issue"),
 ("documentation","openspec/changes/linked-issue-field-availability/tasks.md","minor","issue"),
 ("documentation","openspec/changes/sibling-spec-probe/tasks.md","minor","issue"),
 ("implementation","openspec/changes/sibling-spec-probe/detailed-tasks.yaml","minor","risk"),
 ("documentation","openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml","minor","issue")]: print(fid(*f), f)

```

**输出**:

```text
[2-dir] Group 6 test tasks -> their dependencies (all point at the text tasks they test):
   TASK-025 deps=['TASK-017', 'TASK-018']  title=SC-22 ①–⑦: 两文件各自的「前置: REQUIRE claim (A.1, MUST)」块机械断言 (切片 / 
   TASK-026 deps=['TASK-019']  title=SC-34: 三处 SKILL.md 各含逐字 `A.1 认领时派生的那一串`
   TASK-027 deps=['TASK-022']  title=substitute (rule6 #6): DEFAULTS.json coordination 三键 ↔ confi
   TASK-028 deps=['TASK-021']  title=substitute (rule6 #10a): layer-l-integration.md 不含 `update_h
   TASK-029 deps=['TASK-023']  title=substitute (rule6 #11): coordination-ref-schema.md §3.2 切片含 
   TASK-030 deps=['TASK-020', 'TASK-021']  title=补充 substitute (rule6 #10b + #12): layer-l 新节标题 + 切片含 `--hear
[2-dir] Text tasks whose FIRST verification item requires a Group-6 test to be green (the test depends on this very task):
   TASK-017 verification[0]='TASK-025 (SC-22 ①–⑦, phase-a-planner 臂) 全绿; 切片内无字面 `--phase B` (④)' refs=['TASK-025'] cycle_with=['TASK-025']
   TASK-018 verification[0]='TASK-025 (SC-22, spec-drafter 臂) 全绿; 两文件逐一断言不拼接' refs=['TASK-025'] cycle_with=['TASK-025']
   TASK-019 verification[0]='TASK-026 (SC-34) 绿: 三文件各 ≥1 逐字 `A.1 认领时派生的那一串`' refs=['TASK-026'] cycle_with=['TASK-026']
   TASK-020 verification[0]='TASK-030 绿 (:168 切片含 push_skipped); TASK-033 eval-13 两臂可辨' refs=['TASK-030'] cycle_with=['TASK-030']
   TASK-021 verification[0]='TASK-028 绿 (无 `update_heartbeat` 且含 `heartbeat(`); TASK-030 绿 (含标题 `La' refs=['TASK-028', 'TASK-030'] cycle_with=['TASK-028', 'TASK-030']
   TASK-022 verification[0]='TASK-027 绿 (三键与 SKILL.md 登记值逐字一致; 负控红)' refs=['TASK-027'] cycle_with=['TASK-027']
   TASK-023 verification[0]='TASK-029 绿 (§3.2 切片含字面 `unknown_schema_claims`; 负控写进 §4.2 ⇒ 红)' refs=['TASK-029'] cycle_with=['TASK-029']
[2-dir] TASK-025 notes: '落 D17 ①②③ (Spec SC-22 头部)。RED-first: 断言在 TASK-017/018 落文本前于 d69091d 跑一次全红并留痕。'
[2-dir] TASK-027 notes: '旧 substitute SC-9 无效 (对象是散文); 本条是「真的可机械断言且现在就是红的」测试 (memory check-runs-at-baseline-first)。'
[2-dir] contrast Group 2/3 (impl depends on RED test): TASK-011 deps ['TASK-004'] | TASK-014 deps ['TASK-008', 'TASK-013']
[2-dir] contrast sister linked-issue: TASK-014/015 (SKILL.md hunks) deps -> ['TASK-005'] ['TASK-005'] (TASK-005 = RED structural test)

bd55ab9c ('testing', 'openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml', 'critical', 'issue')
df090b25 ('implementation', 'openspec/changes/{linked-issue-field-availability,sibling-spec-probe}/detailed-tasks.yaml', 'major', 'issue')
fead49d5 ('documentation', 'openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md', 'major', 'issue')
518a7d7f ('implementation', 'openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml', 'major', 'issue')
62285020 ('documentation', 'openspec/changes/linked-issue-field-availability/tasks.md', 'minor', 'issue')
4bf32c17 ('documentation', 'openspec/changes/sibling-spec-probe/tasks.md', 'minor', 'issue')
948363d3 ('implementation', 'openspec/changes/sibling-spec-probe/detailed-tasks.yaml', 'minor', 'risk')
b0e8b171 ('documentation', 'openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml', 'minor', 'issue')

```

### 检查 4 / 5 (第一版, 仅 verification 字段, 未展开范围记法)

**脚本** `check_4_5.py`:

```python
#!/usr/bin/env python3
"""Check 4 (SC coverage: proposal SC set vs yaml verification; tasks.md coverage table vs yaml) and 5 (Impact paths / flags)."""
import re, yaml, os
ROOT = "/home/dev/Aria/openspec/changes"
CUR = {
 "linked-issue-field-availability": ["SC-1","SC-2","SC-3","SC-4","SC-5","SC-6","SC-7","SC-7a","SC-8","SC-9"],
 "sibling-spec-probe": [f"SC-{i}" for i in range(1,22)],
 "a1-entry-claim-duplicate-work-guard": [f"SC-{i}" for i in (2,3,5,6,7,8,9,10,11,12,14,15,21,22,23,24,25,26,28,29,32,33,34)],
}
EXCL = {"a1-entry-claim-duplicate-work-guard": "撤销 1,4,20,27,30,31 / 迁出 13,16,17,18,19(a)(c) / 19(b)→SC-29 (proposal SC 表逐行)",
        "linked-issue-field-availability": "SC-13/SC-19 出现在 proposal 只是引用母 Spec 旧编号 (编号说明段), 非本 Spec SC",
        "sibling-spec-probe": "无"}
def tok(sc):  # exact token regex
    return re.compile(re.escape(sc) + r"(?![0-9a-z])")
for s, cur in CUR.items():
    print(f"\n================ {s} ================")
    d = yaml.safe_load(open(f"{ROOT}/{s}/detailed-tasks.yaml", encoding="utf-8")); tasks = d["tasks"]; byid = {t["id"]: t for t in tasks}
    prop = open(f"{ROOT}/{s}/proposal.md", encoding="utf-8").read()
    md = open(f"{ROOT}/{s}/tasks.md", encoding="utf-8").read()
    # SC set in proposal Success Criteria section
    sc_sec = prop.split("## Success Criteria",1)[1].split("\n## ",1)[0]
    found = sorted({m for m in re.findall(r"\*\*SC-\d+[a-z]?\*\*", sc_sec)}, key=lambda x:(int(re.search(r"\d+",x).group()), x))
    found = [f.strip("*") for f in found]
    print(f"[4] proposal SC 表 bold tokens: {found}")
    print(f"[4] excluded (撤销/迁出): {EXCL[s]}")
    print(f"[4] current set used ({len(cur)}): {cur}")
    def ver(t): return "\n".join(t.get("verification") or [])
    def anyf(t): return ver(t) + "\n" + t["title"] + "\n" + "\n".join(t.get("deliverables") or []) + "\n" + str(t.get("notes",""))
    uncovered_ver = [sc for sc in cur if not any(tok(sc).search(ver(t)) for t in tasks)]
    uncovered_any = [sc for sc in cur if not any(tok(sc).search(anyf(t)) for t in tasks)]
    print(f"[4] SC with ZERO task.verification mention: {uncovered_ver or 'none'}")
    print(f"[4] SC with ZERO mention anywhere in yaml tasks: {uncovered_any or 'none'}")
    for sc in cur:
        hits = [t["id"] for t in tasks if tok(sc).search(ver(t))]
        print(f"      {sc:<6} verification hits: {hits}")
    # tasks.md coverage table
    sec = md.split("## SC → TASK 覆盖表",1)[1].split("\n## ",1)[0]
    rows = [l for l in sec.splitlines() if l.startswith("| SC-") or l.startswith("| **SC-")]
    print(f"[4] tasks.md coverage table rows: {len(rows)}")
    bad = []
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        scs = re.findall(r"SC-\d+[a-z]?", cells[0])
        # task ids: TASK-NNN plus '/NNN' continuations plus 'N.M (TASK-NNN)' forms; plus bare 'N.M' parents
        tail = " | ".join(cells[1:])
        ids = set(re.findall(r"TASK-(\d{3})", tail))
        ids |= set(re.findall(r"TASK-\d{3}/(\d{3})", tail))
        ids |= set(re.findall(r"TASK-\d{3}/\d{3}/(\d{3})", tail))
        # bare parents like '1.6' (linked-issue style) → map
        for p in re.findall(r"(?<![\d.])(\d+\.\d+)(?![\d.])", tail):
            for t in tasks:
                if t["parent"] == p: ids.add(t["id"][5:])
        if "撤销" in tail or "迁出" in tail or "由 SC-29 承担" in tail: 
            print(f"      row {cells[0][:14]:<14} -> excluded ({'撤销' if '撤销' in tail else '迁出/承担'})"); continue
        for sc in scs:
            for n in sorted(ids):
                tid = f"TASK-{n}"
                if tid not in byid: bad.append((sc, tid, "NO SUCH TASK")); continue
                ok = bool(tok(sc).search(ver(byid[tid])))
                okany = bool(tok(sc).search(anyf(byid[tid])))
                flag = "OK" if ok else ("title/notes-only" if okany else "MISSING")
                if flag != "OK": bad.append((sc, tid, flag))
        print(f"      row {cells[0][:14]:<14} scs={scs} tasks={sorted(ids)}")
    print(f"[4] coverage-table claims NOT backed by TASK.verification: {bad or 'none'}")
    # ---- check 5: Impact paths
    imp = prop.split("\n## Impact",1)[1].split("\n## ",1)[0]
    cands = set(re.findall(r"`([^`\n]+)`", imp))
    paths = sorted({c for c in cands if re.fullmatch(r"[\w.@{},*-]+(?:/[\w.@{},*-]+)+|[\w-]+\.(?:py|md|json|yaml|txt|sh)", c)})
    delivs = "\n".join(x for t in tasks for x in (t.get("deliverables") or []))
    def norm(p):
        p = p.split(":")[0]
        if p.startswith("skills/"): p = "aria/" + p
        return p
    miss = []
    for p in paths:
        n = norm(p)
        key = n.rstrip("/").split("/")[-1] if "*" in n or "{" in n else n
        if key not in delivs and n not in delivs: miss.append(p)
    print(f"[5] Impact backtick path tokens ({len(paths)}): {paths}")
    print(f"[5] Impact paths NOT found in any deliverables: {miss or 'none'}")
    # flags
    flags = sorted(set(re.findall(r"(?<![\w-])--[a-z][a-z-]+", prop)))
    allyaml = open(f"{ROOT}/{s}/detailed-tasks.yaml", encoding="utf-8").read()
    tasktext = "\n".join(anyf(t) for t in tasks)
    fmiss_tasks = [f for f in flags if f not in tasktext]
    fmiss_file = [f for f in flags if f not in allyaml]
    print(f"[5] proposal flags ({len(flags)}): {flags}")
    print(f"[5] flags absent from task deliverables/verification/title/notes: {fmiss_tasks or 'none'}; absent from whole yaml: {fmiss_file or 'none'}")

```

**输出**:

```text

================ linked-issue-field-availability ================
[4] proposal SC 表 bold tokens: ['SC-1', 'SC-2', 'SC-3', 'SC-4', 'SC-5', 'SC-6', 'SC-7', 'SC-7a', 'SC-8', 'SC-9']
[4] excluded (撤销/迁出): SC-13/SC-19 出现在 proposal 只是引用母 Spec 旧编号 (编号说明段), 非本 Spec SC
[4] current set used (10): ['SC-1', 'SC-2', 'SC-3', 'SC-4', 'SC-5', 'SC-6', 'SC-7', 'SC-7a', 'SC-8', 'SC-9']
[4] SC with ZERO task.verification mention: none
[4] SC with ZERO mention anywhere in yaml tasks: none
      SC-1   verification hits: ['TASK-001', 'TASK-006', 'TASK-007', 'TASK-019']
      SC-2   verification hits: ['TASK-001', 'TASK-007']
      SC-3   verification hits: ['TASK-002', 'TASK-007']
      SC-4   verification hits: ['TASK-002', 'TASK-007', 'TASK-016', 'TASK-019']
      SC-5   verification hits: ['TASK-003', 'TASK-008']
      SC-6   verification hits: ['TASK-005', 'TASK-013', 'TASK-016', 'TASK-019', 'TASK-021', 'TASK-023']
      SC-7   verification hits: ['TASK-017', 'TASK-018']
      SC-7a  verification hits: ['TASK-005', 'TASK-015']
      SC-8   verification hits: ['TASK-005', 'TASK-011', 'TASK-019', 'TASK-021']
      SC-9   verification hits: ['TASK-004', 'TASK-006', 'TASK-009']
[4] tasks.md coverage table rows: 10
      row SC-1           scs=['SC-1'] tasks=['001', '006', '007']
      row SC-2           scs=['SC-2'] tasks=['001', '006', '007']
      row SC-3           scs=['SC-3'] tasks=['002', '006', '007']
      row SC-4           scs=['SC-4'] tasks=['002', '006', '007']
      row SC-5           scs=['SC-5'] tasks=['003', '008', '010']
      row SC-6           scs=['SC-6'] tasks=['005', '013', '023']
      row SC-7           scs=['SC-7'] tasks=['016', '017']
      row SC-7a          scs=['SC-7a'] tasks=['005', '015']
      row SC-8           scs=['SC-8'] tasks=['005', '008', '011']
      row SC-9           scs=['SC-9'] tasks=['004', '007', '009']
[4] coverage-table claims NOT backed by TASK.verification: [('SC-2', 'TASK-006', 'MISSING'), ('SC-3', 'TASK-006', 'MISSING'), ('SC-4', 'TASK-006', 'MISSING'), ('SC-5', 'TASK-010', 'MISSING'), ('SC-7', 'TASK-016', 'title/notes-only'), ('SC-8', 'TASK-008', 'MISSING'), ('SC-9', 'TASK-007', 'MISSING')]
[5] Impact backtick path tokens (11): ['.aria/linked-issue-field-grandfathered.txt', '.aria/state-checks.yaml', 'aria-plugin-benchmarks/ab-suite/spec-drafter.json', 'aria/skills/spec-drafter/SKILL.md', 'aria/skills/state-scanner/lib/collision.py', 'aria/skills/state-scanner/lib/linked_issue_field.py', 'aria/skills/state-scanner/scripts/linked_issue_field_probe.py', 'openspec/changes/aria-2.0-m{6,7}-*/proposal.md', 'spec-drafter/SKILL.md', 'standards/conventions/version-management.md', 'standards/openspec/templates/proposal-minimal.md']
[5] Impact paths NOT found in any deliverables: ['aria/skills/state-scanner/lib/collision.py', 'openspec/changes/aria-2.0-m{6,7}-*/proposal.md', 'standards/conventions/version-management.md']
[5] proposal flags (5): ['--emit-arg', '--grandfathered', '--include', '--linked-issue', '--stat']
[5] flags absent from task deliverables/verification/title/notes: ['--include']; absent from whole yaml: ['--include']

================ sibling-spec-probe ================
[4] proposal SC 表 bold tokens: ['SC-1', 'SC-2', 'SC-3', 'SC-4', 'SC-5', 'SC-6', 'SC-7', 'SC-8', 'SC-9', 'SC-10', 'SC-11', 'SC-12', 'SC-13', 'SC-14', 'SC-15', 'SC-16', 'SC-17', 'SC-18', 'SC-19', 'SC-20', 'SC-21']
[4] excluded (撤销/迁出): 无
[4] current set used (21): ['SC-1', 'SC-2', 'SC-3', 'SC-4', 'SC-5', 'SC-6', 'SC-7', 'SC-8', 'SC-9', 'SC-10', 'SC-11', 'SC-12', 'SC-13', 'SC-14', 'SC-15', 'SC-16', 'SC-17', 'SC-18', 'SC-19', 'SC-20', 'SC-21']
[4] SC with ZERO task.verification mention: none
[4] SC with ZERO mention anywhere in yaml tasks: none
      SC-1   verification hits: ['TASK-006', 'TASK-011', 'TASK-013', 'TASK-014', 'TASK-016']
      SC-2   verification hits: ['TASK-008', 'TASK-010']
      SC-3   verification hits: ['TASK-007', 'TASK-012']
      SC-4   verification hits: ['TASK-007', 'TASK-012']
      SC-5   verification hits: ['TASK-007', 'TASK-011']
      SC-6   verification hits: ['TASK-007', 'TASK-013']
      SC-7   verification hits: ['TASK-005', 'TASK-011', 'TASK-014']
      SC-8   verification hits: ['TASK-005', 'TASK-011']
      SC-9   verification hits: ['TASK-005', 'TASK-011']
      SC-10  verification hits: ['TASK-005', 'TASK-011', 'TASK-014']
      SC-11  verification hits: ['TASK-005', 'TASK-011']
      SC-12  verification hits: ['TASK-007', 'TASK-012']
      SC-13  verification hits: ['TASK-007', 'TASK-012']
      SC-14  verification hits: ['TASK-007', 'TASK-012']
      SC-15  verification hits: ['TASK-008', 'TASK-010']
      SC-16  verification hits: ['TASK-003', 'TASK-017']
      SC-17  verification hits: ['TASK-002', 'TASK-009', 'TASK-014', 'TASK-015']
      SC-18  verification hits: ['TASK-011', 'TASK-014']
      SC-19  verification hits: ['TASK-005', 'TASK-011']
      SC-20  verification hits: ['TASK-002', 'TASK-009', 'TASK-014', 'TASK-015', 'TASK-016']
      SC-21  verification hits: ['TASK-004', 'TASK-010', 'TASK-014']
[4] tasks.md coverage table rows: 21
      row SC-1           scs=['SC-1'] tasks=['006', '011', '013', '016']
      row SC-2           scs=['SC-2'] tasks=['008', '010']
      row SC-3           scs=['SC-3'] tasks=['007', '012']
      row SC-4           scs=['SC-4'] tasks=['007', '012']
      row SC-5           scs=['SC-5'] tasks=['007', '011']
      row SC-6           scs=['SC-6'] tasks=['007', '013']
      row SC-7           scs=['SC-7'] tasks=['005', '011']
      row SC-8           scs=['SC-8'] tasks=['005', '011']
      row SC-9           scs=['SC-9'] tasks=['005', '011']
      row SC-10          scs=['SC-10'] tasks=['005', '011']
      row SC-11          scs=['SC-11'] tasks=['005', '011']
      row SC-12          scs=['SC-12'] tasks=['007', '012']
      row SC-13          scs=['SC-13'] tasks=['007', '012']
      row SC-14          scs=['SC-14'] tasks=['007', '012']
      row SC-15          scs=['SC-15'] tasks=['008', '010']
      row SC-16          scs=['SC-16'] tasks=['003', '016', '017']
      row SC-17          scs=['SC-17'] tasks=['009', '015']
      row SC-18          scs=['SC-18'] tasks=['006', '011']
      row SC-19          scs=['SC-19'] tasks=['005', '011']
      row SC-20          scs=['SC-20'] tasks=['009', '015', '016']
      row SC-21          scs=['SC-21'] tasks=['004', '010']
[4] coverage-table claims NOT backed by TASK.verification: [('SC-16', 'TASK-016', 'MISSING'), ('SC-18', 'TASK-006', 'title/notes-only')]
[5] Impact backtick path tokens (13): ['.../state-scanner/scripts', 'AB_TEST_OPERATIONS.md', 'aria-plugin-benchmarks/ab-suite/audit-engine.json', 'scripts/lib', 'sibling_spec_probe.py', 'skills/audit-engine/SKILL.md', 'skills/audit-engine/references/execution-modes.md', 'skills/audit-engine/references/report-format.md', 'skills/audit-engine/scripts/sibling_spec_probe.py', 'skills/audit-engine/tests/test_sibling_spec_probe.py', 'skills/run_all_tests.sh', 'skills/state-scanner/**', 'sync.py']
[5] Impact paths NOT found in any deliverables: ['.../state-scanner/scripts', 'AB_TEST_OPERATIONS.md', 'scripts/lib', 'skills/run_all_tests.sh', 'skills/state-scanner/**', 'sync.py']
[5] proposal flags (6): ['--get', '--linked-issue', '--no-tags', '--own-spec-dir', '--repo-path', '--symref']
[5] flags absent from task deliverables/verification/title/notes: ['--get', '--linked-issue']; absent from whole yaml: ['--get']

================ a1-entry-claim-duplicate-work-guard ================
[4] proposal SC 表 bold tokens: ['SC-1', 'SC-2', 'SC-3', 'SC-4', 'SC-5', 'SC-6', 'SC-7', 'SC-8', 'SC-9', 'SC-10', 'SC-11', 'SC-12', 'SC-13', 'SC-14', 'SC-15', 'SC-16', 'SC-17', 'SC-18', 'SC-19', 'SC-20', 'SC-21', 'SC-22', 'SC-23', 'SC-24', 'SC-25', 'SC-26', 'SC-27', 'SC-28', 'SC-29', 'SC-30', 'SC-31', 'SC-32', 'SC-33', 'SC-34']
[4] excluded (撤销/迁出): 撤销 1,4,20,27,30,31 / 迁出 13,16,17,18,19(a)(c) / 19(b)→SC-29 (proposal SC 表逐行)
[4] current set used (23): ['SC-2', 'SC-3', 'SC-5', 'SC-6', 'SC-7', 'SC-8', 'SC-9', 'SC-10', 'SC-11', 'SC-12', 'SC-14', 'SC-15', 'SC-21', 'SC-22', 'SC-23', 'SC-24', 'SC-25', 'SC-26', 'SC-28', 'SC-29', 'SC-32', 'SC-33', 'SC-34']
[4] SC with ZERO task.verification mention: ['SC-3']
[4] SC with ZERO mention anywhere in yaml tasks: none
      SC-2   verification hits: ['TASK-007', 'TASK-009', 'TASK-013']
      SC-3   verification hits: []
      SC-5   verification hits: ['TASK-005', 'TASK-012']
      SC-6   verification hits: ['TASK-005']
      SC-7   verification hits: ['TASK-005']
      SC-8   verification hits: ['TASK-007', 'TASK-009', 'TASK-013']
      SC-9   verification hits: ['TASK-002', 'TASK-035']
      SC-10  verification hits: ['TASK-008', 'TASK-015']
      SC-11  verification hits: ['TASK-035']
      SC-12  verification hits: ['TASK-035']
      SC-14  verification hits: ['TASK-009', 'TASK-035']
      SC-15  verification hits: ['TASK-012']
      SC-21  verification hits: ['TASK-033']
      SC-22  verification hits: ['TASK-003', 'TASK-017', 'TASK-018']
      SC-23  verification hits: ['TASK-009']
      SC-24  verification hits: ['TASK-008', 'TASK-014']
      SC-25  verification hits: ['TASK-008', 'TASK-014', 'TASK-035']
      SC-26  verification hits: ['TASK-035']
      SC-28  verification hits: ['TASK-010', 'TASK-016']
      SC-29  verification hits: ['TASK-007', 'TASK-013']
      SC-32  verification hits: ['TASK-010', 'TASK-016']
      SC-33  verification hits: ['TASK-008', 'TASK-014']
      SC-34  verification hits: ['TASK-019']
[4] tasks.md coverage table rows: 33
      row SC-1           -> excluded (撤销)
      row SC-2           scs=['SC-2'] tasks=['007', '009', '013', '014']
      row SC-3           scs=['SC-3'] tasks=['004', '011']
      row SC-4           -> excluded (撤销)
      row SC-5 / SC-6 /  scs=['SC-5', 'SC-6', 'SC-7'] tasks=['005', '012']
      row SC-8           scs=['SC-8'] tasks=['007', '013', '014']
      row SC-9 (A)(B)    scs=['SC-9'] tasks=['017', '035']
      row SC-10          scs=['SC-10'] tasks=['008', '015']
      row SC-11          scs=['SC-11'] tasks=['017', '035']
      row SC-12          scs=['SC-12'] tasks=['017', '018', '035']
      row SC-13          -> excluded (迁出/承担)
      row SC-14 (a)      scs=['SC-14'] tasks=['009']
      row SC-14 (b)      scs=['SC-14'] tasks=['035']
      row SC-15          scs=['SC-15'] tasks=['006', '012']
      row SC-16 / SC-17  -> excluded (迁出/承担)
      row SC-19 (a)(c)   -> excluded (迁出/承担)
      row SC-19 (b)      -> excluded (迁出/承担)
      row SC-20          -> excluded (撤销)
      row SC-21          scs=['SC-21'] tasks=['020', '033']
      row SC-22 ①–⑦      scs=['SC-22'] tasks=['017', '018', '025']
      row SC-23          scs=['SC-23'] tasks=['009', '019']
      row SC-24          scs=['SC-24'] tasks=['008', '014']
      row SC-25 ① 代码臂    scs=['SC-25'] tasks=['008', '014']
      row SC-25 ② 行为臂    scs=['SC-25'] tasks=['035']
      row SC-26          scs=['SC-26'] tasks=['017', '022', '035']
      row SC-27          -> excluded (撤销)
      row SC-28 第一臂      scs=['SC-28'] tasks=['033']
      row SC-28 第二臂      scs=['SC-28'] tasks=['010', '016']
      row SC-29          scs=['SC-29'] tasks=['007', '013', '014']
      row SC-30 / SC-31  -> excluded (撤销)
      row SC-32          scs=['SC-32'] tasks=['010', '016']
      row SC-33          scs=['SC-33'] tasks=['008', '014']
      row SC-34          scs=['SC-34'] tasks=['019', '026']
[4] coverage-table claims NOT backed by TASK.verification: [('SC-2', 'TASK-014', 'MISSING'), ('SC-3', 'TASK-004', 'title/notes-only'), ('SC-3', 'TASK-011', 'MISSING'), ('SC-6', 'TASK-012', 'MISSING'), ('SC-7', 'TASK-012', 'MISSING'), ('SC-8', 'TASK-014', 'MISSING'), ('SC-9', 'TASK-017', 'MISSING'), ('SC-11', 'TASK-017', 'MISSING'), ('SC-12', 'TASK-017', 'MISSING'), ('SC-12', 'TASK-018', 'MISSING'), ('SC-15', 'TASK-006', 'title/notes-only'), ('SC-21', 'TASK-020', 'MISSING'), ('SC-22', 'TASK-025', 'title/notes-only'), ('SC-23', 'TASK-019', 'MISSING'), ('SC-26', 'TASK-017', 'title/notes-only'), ('SC-26', 'TASK-022', 'MISSING'), ('SC-28', 'TASK-033', 'title/notes-only'), ('SC-29', 'TASK-014', 'MISSING'), ('SC-34', 'TASK-026', 'title/notes-only')]
[5] Impact backtick path tokens (42): ['.aria/state-checks.yaml', 'DEFAULTS.json', 'ab-suite/audit-engine.json', 'aria-plugin-benchmarks/ab-suite/state-scanner.json', 'branch-manager.json', 'config-loader/SKILL.md', 'coordination-ref-schema.md', 'layer-l-integration.md', 'phase-a-planner.json', 'phase-b-developer.json', 'phase-d-closer.json', 'phase1_gate.py', 'references/execution-modes.md', 'references/layer-l-integration.md', 'scripts/heartbeat_gate.py', 'simonfish/bfe8285d', 'skills/audit-engine/SKILL.md', 'skills/audit-engine/scripts/sibling_spec_probe.py', 'skills/branch-manager/SKILL.md', 'skills/config-loader/DEFAULTS.json', 'skills/config-loader/SKILL.md', 'skills/phase-a-planner/SKILL.md', 'skills/phase-b-developer/SKILL.md', 'skills/phase-d-closer/SKILL.md', 'skills/spec-drafter/SKILL.md', 'skills/state-scanner/SKILL.md', 'skills/state-scanner/docs/coordination-ref-schema.md', 'skills/state-scanner/lib/claim_lifecycle.py', 'skills/state-scanner/lib/claim_schema.py', 'skills/state-scanner/lib/collision.py', 'skills/state-scanner/lib/constants.py', 'skills/state-scanner/lib/identity.py', 'skills/state-scanner/references/layer-l-integration.md', 'skills/state-scanner/scripts/coordination_probe.py', 'skills/state-scanner/scripts/phase1_gate.py', 'skills/state-scanner/scripts/release_gate.py', 'spec-drafter.json', 'standards/conventions/session-handoff.md', 'standards/openspec/templates/proposal-minimal.md', 'state-scanner.json', 'test_coordination_default_lockin.py', 'track_id.py']
[5] Impact paths NOT found in any deliverables: ['.aria/state-checks.yaml', 'ab-suite/audit-engine.json', 'branch-manager.json', 'phase-b-developer.json', 'phase-d-closer.json', 'references/execution-modes.md', 'scripts/heartbeat_gate.py', 'simonfish/bfe8285d', 'skills/audit-engine/SKILL.md', 'standards/openspec/templates/proposal-minimal.md', 'track_id.py']
[5] proposal flags (17): ['--emit-arg', '--flag', '--gc', '--heartbeat-only', '--include', '--include-terminal', '--is-ancestor', '--linked-issue', '--mode', '--no-push', '--phase', '--raw-track-id', '--repo-path', '--spec-slug', '--stat', '--status', '--sweep-stale']
[5] flags absent from task deliverables/verification/title/notes: ['--flag', '--is-ancestor', '--spec-slug']; absent from whole yaml: ['--flag', '--is-ancestor', '--spec-slug']

```

### 检查 4 (第二版, 范围记法展开 `SC-1~4` / `SC-5/6/7`) + flag 映射行

**脚本** `check_4b.py`:

```python
#!/usr/bin/env python3
"""Check 4 refined: expand SC range/slash notation ('SC-1~4', 'SC-5/6/7', 'SC-1~4/SC-9') before matching; re-evaluate
(a) each current SC has >=1 task whose verification names it, (b) tasks.md coverage-table (SC, TASK) claims vs TASK.verification,
(c) tasks.md flag->TASK map lines."""
import re, yaml
ROOT = "/home/dev/Aria/openspec/changes"
CUR = {
 "linked-issue-field-availability": ["SC-1","SC-2","SC-3","SC-4","SC-5","SC-6","SC-7","SC-7a","SC-8","SC-9"],
 "sibling-spec-probe": [f"SC-{i}" for i in range(1,22)],
 "a1-entry-claim-duplicate-work-guard": [f"SC-{i}" for i in (2,3,5,6,7,8,9,10,11,12,14,15,21,22,23,24,25,26,28,29,32,33,34)],
}
def expand(text):
    out = set()
    for m in re.finditer(r"SC-(\d+)([a-z]?)((?:[~/](?:SC-)?\d+[a-z]?)*)", text):
        base = int(m.group(1)); out.add(f"SC-{base}{m.group(2)}")
        tail = m.group(3)
        prev = base
        for sep, num, suf in re.findall(r"([~/])(?:SC-)?(\d+)([a-z]?)", tail):
            n = int(num)
            if sep == "~":
                for k in range(prev, n+1): out.add(f"SC-{k}")
            else: out.add(f"SC-{n}{suf}")
            prev = n
    return out
def ver(t): return "\n".join(t.get("verification") or [])
def anyf(t): return ver(t)+"\n"+t["title"]+"\n"+"\n".join(t.get("deliverables") or [])+"\n"+str(t.get("notes",""))
for s, cur in CUR.items():
    print(f"\n================ {s} ================")
    d = yaml.safe_load(open(f"{ROOT}/{s}/detailed-tasks.yaml", encoding="utf-8")); tasks = d["tasks"]; byid = {t["id"]: t for t in tasks}
    md = open(f"{ROOT}/{s}/tasks.md", encoding="utf-8").read()
    vsets = {t["id"]: expand(ver(t)) for t in tasks}; asets = {t["id"]: expand(anyf(t)) for t in tasks}
    unc_v = [sc for sc in cur if not any(sc in vsets[i] for i in vsets)]
    unc_a = [sc for sc in cur if not any(sc in asets[i] for i in asets)]
    print(f"[4a] SC with zero task.verification mention (range-aware): {unc_v or 'none'}; zero anywhere: {unc_a or 'none'}")
    for sc in unc_v:
        print(f"      {sc}: title/deliverables/notes hits -> {[i for i in asets if sc in asets[i]]}")
    sec = md.split("## SC → TASK 覆盖表",1)[1].split("\n## ",1)[0]
    rows = [l for l in sec.splitlines() if l.startswith("| SC-") or l.startswith("| **SC-")]
    bad = []
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        tail = " | ".join(cells[1:])
        if "撤销" in tail or "迁出" in tail or "由 SC-29 承担" in tail: continue
        scs = sorted(expand(cells[0]))
        ids = set(re.findall(r"TASK-(\d{3})", tail)) | set(re.findall(r"TASK-\d{3}/(\d{3})", tail))
        for p in re.findall(r"(?<![\d.])(\d+\.\d+)(?![\d.])", tail):
            for t in tasks:
                if t["parent"] == p: ids.add(t["id"][5:])
        for sc in scs:
            for n in sorted(ids):
                tid = f"TASK-{n}"
                if sc in vsets[tid]: continue
                bad.append((sc, tid, "title/deliv/notes-only" if sc in asets[tid] else "ABSENT"))
    print(f"[4b] coverage-table (SC,TASK) pairs NOT named in TASK.verification: {len(bad)}")
    for b in bad: print("      ", b)
    # flag map line
    fm = [l for l in md.splitlines() if l.startswith("**flag") or l.startswith("**每个 `--flag`")]
    if fm:
        line = fm[0]
        print(f"[4c] tasks.md flag→TASK map line found ({len(line)} chars)")
        # parse segments 'X (ids)' or 'X → a/b/c'
        if s.startswith("a1"):
            for seg in re.findall(r"((?:`[^`]+`[ /]*)+)\((\d{3}(?:[,–-]\s*\d{3})*)\)", line):
                flags = re.findall(r"`([^`]+)`", seg[0]); nums = re.findall(r"\d{3}", seg[1])
                # expand ranges like 031–035
                if "–" in seg[1] and len(nums)==2: nums = [f"{k:03d}" for k in range(int(nums[0]), int(nums[1])+1)]
                for fl in flags:
                    for n in nums:
                        tid=f"TASK-{n}"; hit = fl in anyf(byid[tid]) or fl.replace('"','') in anyf(byid[tid])
                        if not hit: print(f"      flag map claim NOT backed: {fl!r} -> {tid}")
        else:
            for seg in line.split(";"):
                flags = re.findall(r"`([^`]+)`", seg.split("→")[0]) if "→" in seg else []
                parents = re.findall(r"(\d+\.\d+)", seg.split("→")[1]) if "→" in seg else []
                for fl in flags:
                    for p in parents:
                        tids = [t["id"] for t in tasks if t["parent"]==p]
                        for tid in tids:
                            if fl not in anyf(byid[tid]): print(f"      flag map claim NOT backed: {fl!r} -> {p} ({tid})")
        print("      (end of flag-map check)")

```

**输出**:

```text

================ linked-issue-field-availability ================
[4a] SC with zero task.verification mention (range-aware): none; zero anywhere: none
[4b] coverage-table (SC,TASK) pairs NOT named in TASK.verification: 4
       ('SC-5', 'TASK-010', 'ABSENT')
       ('SC-7', 'TASK-016', 'title/deliv/notes-only')
       ('SC-8', 'TASK-008', 'ABSENT')
       ('SC-9', 'TASK-007', 'ABSENT')
[4c] tasks.md flag→TASK map line found (242 chars)
      flag map claim NOT backed: '--flag' -> 2.2 (TASK-008)
      flag map claim NOT backed: '--flag' -> 2.4 (TASK-010)
      flag map claim NOT backed: '--flag' -> 2.5 (TASK-011)
      flag map claim NOT backed: '--flag' -> 1.3 (TASK-003)
      flag map claim NOT backed: '--linked-issue' -> 2.1 (TASK-007)
      flag map claim NOT backed: '--linked-issue' -> 1.2 (TASK-002)
      flag map claim NOT backed: '--linked-issue' -> 1.4 (TASK-004)
      flag map claim NOT backed: '--no-push' -> 4.1 (TASK-016)
      flag map claim NOT backed: '--no-push' -> 4.2 (TASK-017)
      flag map claim NOT backed: 'ARIA_COORDINATION_NO_PUSH' -> 4.2 (TASK-017)
      (end of flag-map check)

================ sibling-spec-probe ================
[4a] SC with zero task.verification mention (range-aware): none; zero anywhere: none
[4b] coverage-table (SC,TASK) pairs NOT named in TASK.verification: 2
       ('SC-16', 'TASK-016', 'ABSENT')
       ('SC-18', 'TASK-006', 'title/deliv/notes-only')

================ a1-entry-claim-duplicate-work-guard ================
[4a] SC with zero task.verification mention (range-aware): ['SC-3']; zero anywhere: none
      SC-3: title/deliverables/notes hits -> ['TASK-004']
[4b] coverage-table (SC,TASK) pairs NOT named in TASK.verification: 17
       ('SC-2', 'TASK-014', 'ABSENT')
       ('SC-3', 'TASK-004', 'title/deliv/notes-only')
       ('SC-3', 'TASK-011', 'ABSENT')
       ('SC-8', 'TASK-014', 'ABSENT')
       ('SC-9', 'TASK-017', 'ABSENT')
       ('SC-11', 'TASK-017', 'ABSENT')
       ('SC-12', 'TASK-017', 'ABSENT')
       ('SC-12', 'TASK-018', 'ABSENT')
       ('SC-15', 'TASK-006', 'title/deliv/notes-only')
       ('SC-21', 'TASK-020', 'ABSENT')
       ('SC-22', 'TASK-025', 'title/deliv/notes-only')
       ('SC-23', 'TASK-019', 'ABSENT')
       ('SC-26', 'TASK-017', 'title/deliv/notes-only')
       ('SC-26', 'TASK-022', 'ABSENT')
       ('SC-28', 'TASK-033', 'title/deliv/notes-only')
       ('SC-29', 'TASK-014', 'ABSENT')
       ('SC-34', 'TASK-026', 'title/deliv/notes-only')
[4c] tasks.md flag→TASK map line found (649 chars)
      flag map claim NOT backed: '--no-push' -> TASK-031
      flag map claim NOT backed: '--no-push' -> TASK-035
      flag map claim NOT backed: 'ARIA_COORDINATION_NO_PUSH' -> TASK-001
      flag map claim NOT backed: 'ARIA_COORDINATION_NO_PUSH' -> TASK-035
      flag map claim NOT backed: '--raw-track-id' -> TASK-018
      flag map claim NOT backed: '--phase A.1' -> TASK-017
      flag map claim NOT backed: '--phase A.1' -> TASK-018
      flag map claim NOT backed: '--mode advisory' -> TASK-017
      flag map claim NOT backed: '--mode advisory' -> TASK-018
      flag map claim NOT backed: '--linked-issue' -> TASK-017
      flag map claim NOT backed: '--linked-issue' -> TASK-018
      flag map claim NOT backed: '--repo-path' -> TASK-017
      flag map claim NOT backed: '--repo-path' -> TASK-018
      flag map claim NOT backed: '--status abandoned' -> TASK-019
      flag map claim NOT backed: '--sweep-stale' -> TASK-019
      flag map claim NOT backed: '--gc' -> TASK-019
      flag map claim NOT backed: 'state_scanner.coordination.{enabled, mode, unattended}' -> TASK-022
      flag map claim NOT backed: 'state_scanner.coordination.{enabled, mode, unattended}' -> TASK-027
      flag map claim NOT backed: 'linked_issue_overlap_error' -> TASK-014
      flag map claim NOT backed: 'linked_issue_overlap: null' -> TASK-014
      flag map claim NOT backed: 'linked_issue_overlap: null' -> TASK-008
      flag map claim NOT backed: 'push_skipped_reason' -> TASK-020
      flag map claim NOT backed: 'error: "fetch_degraded"' -> TASK-015
      (end of flag-map check)

```

### 检查 4 / 5 (第三版, 用归档门解析器切块, 把 deliverables `#` 注释算进去 — 报告采用此版数字)

**脚本** `check_4c.py`:

```python
#!/usr/bin/env python3
"""Check 4/5 on RAW task blocks (includes deliverables '# comments', which yaml.safe_load drops)."""
import re, yaml, sys
sys.path.insert(0, "/home/dev/Aria/aria/skills/state-scanner/scripts")
from lib.detailed_tasks import _split_task_blocks, _tasks_block_bounds
ROOT = "/home/dev/Aria/openspec/changes"
CUR = {
 "linked-issue-field-availability": ["SC-1","SC-2","SC-3","SC-4","SC-5","SC-6","SC-7","SC-7a","SC-8","SC-9"],
 "sibling-spec-probe": [f"SC-{i}" for i in range(1,22)],
 "a1-entry-claim-duplicate-work-guard": [f"SC-{i}" for i in (2,3,5,6,7,8,9,10,11,12,14,15,21,22,23,24,25,26,28,29,32,33,34)],
}
def expand(text):
    out = set()
    for m in re.finditer(r"SC-(\d+)([a-z]?)((?:[~/](?:SC-)?\d+[a-z]?)*)", text):
        base = int(m.group(1)); out.add(f"SC-{base}{m.group(2)}"); prev = base
        for sep, num, suf in re.findall(r"([~/])(?:SC-)?(\d+)([a-z]?)", m.group(3)):
            n = int(num)
            if sep == "~":
                for k in range(prev, n+1): out.add(f"SC-{k}")
            else: out.add(f"SC-{n}{suf}")
            prev = n
    return out
def section(block, key):
    m = re.search(rf"^    {key}:(.*?)(?=^    [a-z_]+:|\Z)", block, re.S | re.M)
    return m.group(1) if m else ""
for s, cur in CUR.items():
    print(f"\n================ {s} ================")
    raw = open(f"{ROOT}/{s}/detailed-tasks.yaml", encoding="utf-8").read()
    lines = raw.splitlines(); a, b = _tasks_block_bounds(lines)
    blocks = dict(_split_task_blocks("\n".join(lines[a:b])))
    d = yaml.safe_load(raw); tasks = d["tasks"]
    md = open(f"{ROOT}/{s}/tasks.md", encoding="utf-8").read()
    vsets = {i: expand(section(bl, "verification")) for i, bl in blocks.items()}
    dvsets = {i: expand(section(bl, "verification") + section(bl, "deliverables")) for i, bl in blocks.items()}
    allsets = {i: expand(bl) for i, bl in blocks.items()}
    unc_v = [sc for sc in cur if not any(sc in v for v in vsets.values())]
    unc_dv = [sc for sc in cur if not any(sc in v for v in dvsets.values())]
    print(f"[4a] SC absent from every TASK.verification: {unc_v or 'none'} | absent from verification+deliverables(with comments): {unc_dv or 'none'}")
    sec = md.split("## SC → TASK 覆盖表",1)[1].split("\n## ",1)[0]
    rows = [l for l in sec.splitlines() if l.startswith("| SC-") or l.startswith("| **SC-")]
    bad_v, bad_dv, bad_all = [], [], []
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]; tail = " | ".join(cells[1:])
        if "撤销" in tail or "迁出" in tail or "由 SC-29 承担" in tail: continue
        scs = sorted(expand(cells[0]))
        ids = set(re.findall(r"TASK-(\d{3})", tail)) | set(re.findall(r"TASK-\d{3}/(\d{3})", tail))
        for p in re.findall(r"(?<![\d.])(\d+\.\d+)(?![\d.])", tail):
            for t in tasks:
                if t["parent"] == p: ids.add(t["id"][5:])
        for sc in scs:
            for n in sorted(ids):
                tid = f"TASK-{n}"
                if sc not in vsets[tid]: bad_v.append((sc, tid))
                if sc not in dvsets[tid]: bad_dv.append((sc, tid))
                if sc not in allsets[tid]: bad_all.append((sc, tid))
    print(f"[4b] coverage-table pairs not in TASK.verification: {len(bad_v)} -> {bad_v}")
    print(f"[4b] ... not in verification+deliverables(+comments): {len(bad_dv)} -> {bad_dv}")
    print(f"[4b] ... not anywhere in the TASK block (title/notes incl.): {len(bad_all)} -> {bad_all or 'none'}")
    # flag map on raw blocks
    fm = [l for l in md.splitlines() if l.startswith("**flag") or l.startswith("**每个 `--flag`")]
    if fm:
        line = fm[0]; nb = []
        if s.startswith("a1"):
            for seg in re.findall(r"((?:`[^`]+`[ /]*)+)\((\d{3}(?:[,–-]\s*\d{3})*)\)", line):
                flags = re.findall(r"`([^`]+)`", seg[0]); nums = re.findall(r"\d{3}", seg[1])
                if "–" in seg[1] and len(nums)==2: nums = [f"{k:03d}" for k in range(int(nums[0]), int(nums[1])+1)]
                for fl in flags:
                    key = fl.replace('"','').split(".{")[0] if ".{" in fl else fl.replace('"','')
                    key = key.replace("error: ", "").replace(": null", "")
                    for n in nums:
                        if key not in blocks[f"TASK-{n}"]: nb.append((fl, f"TASK-{n}"))
        else:
            for seg in line.split(";"):
                if "→" not in seg: continue
                flags = [f for f in re.findall(r"`([^`]+)`", seg.split("→")[0]) if f != "--flag"]
                parents = re.findall(r"(\d+\.\d+)", seg.split("→")[1])
                for fl in flags:
                    for p in parents:
                        for t in tasks:
                            if t["parent"]==p and fl not in blocks[t["id"]]: nb.append((fl, f"{p}/{t['id']}"))
        print(f"[4c] flag→TASK map claims not backed by raw TASK block text: {nb or 'none'}")

```

**输出**:

```text

================ linked-issue-field-availability ================
[4a] SC absent from every TASK.verification: none | absent from verification+deliverables(with comments): none
[4b] coverage-table pairs not in TASK.verification: 4 -> [('SC-5', 'TASK-010'), ('SC-7', 'TASK-016'), ('SC-8', 'TASK-008'), ('SC-9', 'TASK-007')]
[4b] ... not in verification+deliverables(+comments): 4 -> [('SC-5', 'TASK-010'), ('SC-7', 'TASK-016'), ('SC-8', 'TASK-008'), ('SC-9', 'TASK-007')]
[4b] ... not anywhere in the TASK block (title/notes incl.): 3 -> [('SC-5', 'TASK-010'), ('SC-8', 'TASK-008'), ('SC-9', 'TASK-007')]
[4c] flag→TASK map claims not backed by raw TASK block text: [('--linked-issue', '2.1/TASK-007'), ('--linked-issue', '1.2/TASK-002'), ('--linked-issue', '1.4/TASK-004'), ('--no-push', '4.1/TASK-016'), ('--no-push', '4.2/TASK-017'), ('ARIA_COORDINATION_NO_PUSH', '4.2/TASK-017')]

================ sibling-spec-probe ================
[4a] SC absent from every TASK.verification: none | absent from verification+deliverables(with comments): none
[4b] coverage-table pairs not in TASK.verification: 2 -> [('SC-16', 'TASK-016'), ('SC-18', 'TASK-006')]
[4b] ... not in verification+deliverables(+comments): 2 -> [('SC-16', 'TASK-016'), ('SC-18', 'TASK-006')]
[4b] ... not anywhere in the TASK block (title/notes incl.): 1 -> [('SC-16', 'TASK-016')]

================ a1-entry-claim-duplicate-work-guard ================
[4a] SC absent from every TASK.verification: ['SC-3'] | absent from verification+deliverables(with comments): ['SC-3']
[4b] coverage-table pairs not in TASK.verification: 17 -> [('SC-2', 'TASK-014'), ('SC-3', 'TASK-004'), ('SC-3', 'TASK-011'), ('SC-8', 'TASK-014'), ('SC-9', 'TASK-017'), ('SC-11', 'TASK-017'), ('SC-12', 'TASK-017'), ('SC-12', 'TASK-018'), ('SC-15', 'TASK-006'), ('SC-21', 'TASK-020'), ('SC-22', 'TASK-025'), ('SC-23', 'TASK-019'), ('SC-26', 'TASK-017'), ('SC-26', 'TASK-022'), ('SC-28', 'TASK-033'), ('SC-29', 'TASK-014'), ('SC-34', 'TASK-026')]
[4b] ... not in verification+deliverables(+comments): 17 -> [('SC-2', 'TASK-014'), ('SC-3', 'TASK-004'), ('SC-3', 'TASK-011'), ('SC-8', 'TASK-014'), ('SC-9', 'TASK-017'), ('SC-11', 'TASK-017'), ('SC-12', 'TASK-017'), ('SC-12', 'TASK-018'), ('SC-15', 'TASK-006'), ('SC-21', 'TASK-020'), ('SC-22', 'TASK-025'), ('SC-23', 'TASK-019'), ('SC-26', 'TASK-017'), ('SC-26', 'TASK-022'), ('SC-28', 'TASK-033'), ('SC-29', 'TASK-014'), ('SC-34', 'TASK-026')]
[4b] ... not anywhere in the TASK block (title/notes incl.): 11 -> [('SC-2', 'TASK-014'), ('SC-3', 'TASK-011'), ('SC-8', 'TASK-014'), ('SC-9', 'TASK-017'), ('SC-11', 'TASK-017'), ('SC-12', 'TASK-017'), ('SC-12', 'TASK-018'), ('SC-21', 'TASK-020'), ('SC-23', 'TASK-019'), ('SC-26', 'TASK-022'), ('SC-29', 'TASK-014')]
[4c] flag→TASK map claims not backed by raw TASK block text: [('--no-push', 'TASK-031'), ('--no-push', 'TASK-035'), ('ARIA_COORDINATION_NO_PUSH', 'TASK-001'), ('ARIA_COORDINATION_NO_PUSH', 'TASK-035'), ('--raw-track-id', 'TASK-018'), ('--phase A.1', 'TASK-018'), ('--mode advisory', 'TASK-018'), ('--linked-issue', 'TASK-018'), ('--repo-path', 'TASK-018'), ('--status abandoned', 'TASK-019'), ('--sweep-stale', 'TASK-019'), ('--gc', 'TASK-019')]

```

### 检查 8a — deliverables 路径实存性 vs `(新建)` 标记 (启发式; `同文件`/`不新建文件`/`新增 test_x` 的命中为误报, 已人工剔除, 真阳性 = TASK-038 README.zh-CN.md)

**脚本** `check_8.py`:

```python
#!/usr/bin/env python3
"""Check 8a: deliverables path existence vs (新建) marker."""
import re, os
ROOT = "/home/dev/Aria"
SPECS = ["linked-issue-field-availability", "sibling-spec-probe", "a1-entry-claim-duplicate-work-guard"]
for s in SPECS:
    print(f"\n================ {s} ================")
    lines = open(f"{ROOT}/openspec/changes/{s}/detailed-tasks.yaml", encoding="utf-8").read().splitlines()
    cur = None; in_del = False; rows = []
    for ln in lines:
        m = re.match(r"^  - id: (TASK-\d+)", ln)
        if m: cur = m.group(1); in_del = False; continue
        if re.match(r"^    deliverables:\s*(\[\])?\s*$", ln): in_del = "[]" not in ln; continue
        if re.match(r"^    [a-z_]+:", ln): in_del = False; continue
        if in_del:
            m2 = re.match(r"^      - (\S+)\s*(#.*)?$", ln)
            if m2: rows.append((cur, m2.group(1), (m2.group(2) or "")))
    mism = []
    for tid, p, c in rows:
        if "<" in p: kind = "template"; ex = None
        else:
            ex = os.path.exists(os.path.join(ROOT, p))
            newmark = bool(re.search(r"新建|新增|由姊妹 Spec 交付|字段 Spec 新建|探针 Spec 新建", c)) and "同文件" not in c and "扩它" not in c
            kind = "NEW" if newmark else "EXISTING"
        ok = None if ex is None else ((not ex) if kind == "NEW" else ex)
        if ok is False: mism.append((tid, p, kind, ex, c[:70]))
    print(f"[8a] deliverable rows: {len(rows)}; mismatches (NEW-but-exists / EXISTING-but-missing): {len(mism)}")
    for x in mism: print("     ", x)
    # also list NEW ones for the record
    news = [(tid, p) for tid, p, c in rows if re.search(r"新建", c) and "<" not in p]
    print(f"[8a] rows marked 新建: {len(news)} -> all absent today: {all(not os.path.exists(os.path.join(ROOT,p)) for _,p in news)}")

```

**输出**:

```text

================ linked-issue-field-availability ================
[8a] deliverable rows: 34; mismatches (NEW-but-exists / EXISTING-but-missing): 3
      ('TASK-002', 'aria/skills/state-scanner/tests/test_linked_issue_field.py', 'EXISTING', False, '# (新建, 与 TASK-001 同文件)')
      ('TASK-009', 'aria/skills/state-scanner/scripts/linked_issue_field_probe.py', 'EXISTING', False, '# (新建, 与 TASK-008 同文件) argparse 子模式')
      ('TASK-017', 'aria-plugin-benchmarks/ab-suite/spec-drafter.json', 'NEW', True, '# 新增 eval id 3 (name 建议 linked-issue-field-authoring-TARGETED, 承 state')
[8a] rows marked 新建: 10 -> all absent today: True

================ sibling-spec-probe ================
[8a] deliverable rows: 34; mismatches (NEW-but-exists / EXISTING-but-missing): 11
      ('TASK-005', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '# 夹具以字符串字面量内嵌 (逐字原文)')
      ('TASK-006', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '# 三臂对照 + 第四臂合成夹具')
      ('TASK-007', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '# runner 体例仿 phase-d-closer/tests/test_fetch_gate.py:22 `_runner(seq)`')
      ('TASK-008', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '# subprocess.run([sys.executable, <script>, ...]) 体例仿 state-scanner/te')
      ('TASK-009', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '# 读同 skill 的 SKILL.md 与 references/execution-modes.md (Path(__file__).')
      ('TASK-011', 'aria/skills/audit-engine/scripts/sibling_spec_probe.py', 'EXISTING', False, '# 纯分类函数 + 键构造 + 求交')
      ('TASK-012', 'aria/skills/audit-engine/scripts/sibling_spec_probe.py', 'EXISTING', False, '# remote/default-branch/fetch 段')
      ('TASK-013', 'aria/skills/audit-engine/scripts/sibling_spec_probe.py', 'EXISTING', False, '# corpus 段')
      ('TASK-014', 'aria/skills/audit-engine/scripts/sibling_spec_probe.py', 'EXISTING', False, '')
      ('TASK-014', 'aria/skills/audit-engine/tests/test_sibling_spec_probe.py', 'EXISTING', False, '')
      ('TASK-017', 'aria-plugin-benchmarks/ab-suite/audit-engine.json', 'EXISTING', False, '# 若三臂语义分档显示断言措辞过宽 ⇒ 拆条不删 (手册 :142-159), 并 version.yaml 再升')
[8a] rows marked 新建: 4 -> all absent today: True

================ a1-entry-claim-duplicate-work-guard ================
[8a] deliverable rows: 80; mismatches (NEW-but-exists / EXISTING-but-missing): 13
      ('TASK-001', 'docs/handoff/', 'NEW', True, '# 核验结果写入 B.1 起点 handoff (不新建文件, 追加到当日 handoff)')
      ('TASK-006', 'aria/skills/state-scanner/tests/test_heartbeat_by_track.py', 'EXISTING', False, '# 同文件加 TestRenameTwoStep 类 (改名是 claim_lifecycle 语义, 与 heartbeat 同宿主)')
      ('TASK-008', 'aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py', 'EXISTING', False, '# 同文件加四个测试类')
      ('TASK-009', 'aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py', 'EXISTING', False, '# 同文件加 TestA1CarryIdRoundTrip')
      ('TASK-020', 'aria/skills/state-scanner/SKILL.md', 'NEW', True, '# Layer L 段 :143-178: 在 :176 之后、:178 指针之前新增 `### Layer L A.1 heartbeat')
      ('TASK-021', 'aria/skills/state-scanner/references/layer-l-integration.md', 'NEW', True, '# ① :15「闸门仅在用户确认要进入 Phase B 时调用」补 A.1 触发点; ② :45 表行 `lib/claim_lifecyc')
      ('TASK-022', 'aria/skills/config-loader/DEFAULTS.json', 'NEW', True, '# `state_scanner` 段 (:24 起) 新增 `"coordination": {"enabled": true, "mod')
      ('TASK-026', 'aria/skills/state-scanner/tests/test_coordination_default_lockin.py', 'NEW', True, '# 新增 test_a1_carry_id_wording_three_files')
      ('TASK-027', 'aria/skills/state-scanner/tests/test_coordination_default_lockin.py', 'NEW', True, '# 新增 test_defaults_json_coordination_three_keys_match_skill_md (读 ../c')
      ('TASK-028', 'aria/skills/state-scanner/tests/test_coordination_default_lockin.py', 'NEW', True, '# 新增 test_layer_l_reference_no_dangling_update_heartbeat')
      ('TASK-029', 'aria/skills/state-scanner/tests/test_coordination_default_lockin.py', 'NEW', True, '# 新增 test_schema_doc_section_3_2_documents_unknown_schema_claims')
      ('TASK-030', 'aria/skills/state-scanner/tests/test_coordination_default_lockin.py', 'NEW', True, '# 新增 test_layer_l_reference_has_a1_heartbeat_section / test_state_scan')
      ('TASK-038', 'README.zh-CN.md', 'EXISTING', False, '# i18n: 仅正文实质变更才重译 (#140 B 档); badge/版本串必改')
[8a] rows marked 新建: 8 -> all absent today: False

```

### 检查 8b — 214 处行号锚点 sed 实读 (8 条 FAIL 逐条复核: 1155-1158→实为 :1154 (1 行漂移) · 1308-1311 为本席取样串过严 (实为 env 处理行, 命中) · branch-manager :148→实为 :149 (1 行漂移) · session-handoff :223 为 §2.3.8.1 标题 (命中) · report-format :66-71 区间含 :67 标题 (命中) · test_release_by_track :23-25 为 sys.path 三行 (命中) · linked-issue-normalization :259 逐字「追加 keyword-only 形参不构成回归」(命中) · 最后一条为本席把「姊妹 proposal :118」误指向 sibling, 实读 linked-issue proposal :118 = 围栏内 `> **Linked Issue**: `{<org>/<repo>#<n>}`` (命中))

**脚本** `check_8b.py`:

```python
#!/usr/bin/env python3
"""Check 8b: line anchors cited in deliverables comments / metadata vs live tree (aria @ d69091d, standards @ 334c609, main @ HEAD)."""
import subprocess
ROOT="/home/dev/Aria"
A="aria/skills/"
# (spec, file, "N" or "N-M", expected substring)
CASES = [
 # ---- a1
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "61", "logger"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "219", "fetch_degraded"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "299", "_takeover_eligible"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "351", "def _run_gate_impl"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "362", "no_push"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "497", "health_check_fetch"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "537-538", "_self_resume"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "554", "no_push"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "573", "push"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "693-697", "_takeover_eligible"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "761-762", "No prompt needed"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "848", "no_push"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "856", "resilient_push("),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1010", "def _telemetry_path"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1049", "_gated"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1094", "def run_gate"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1155-1158", "linked_issue"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1255", "def _main"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1269", "required=True"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1273", "required=True"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1281-1288", "--linked-issue"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1292", "--no-push"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1308-1311", "ARIA_COORDINATION_NO_PUSH"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1332", "if args.linked_issue:"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1334", "read_claims"),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1335-1337", "linked_issue_overlaps("),
 ("a1", A+"state-scanner/scripts/phase1_gate.py", "1338-1340", "[]"),
 ("a1", A+"state-scanner/scripts/release_gate.py", "92", "no_push"),
 ("a1", A+"state-scanner/scripts/release_gate.py", "150", "sweep_stale_active("),
 ("a1", A+"state-scanner/scripts/release_gate.py", "240", "choices"),
 ("a1", A+"state-scanner/scripts/release_gate.py", "246", "STALE_TTL"),
 ("a1", A+"state-scanner/scripts/release_gate.py", "255-264", "--no-push"),
 ("a1", A+"state-scanner/scripts/release_gate.py", "267-268", "parser.error"),
 ("a1", A+"state-scanner/lib/failure_handlers.py", "95", "no_push_requested_by_env"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "99", "def acquire_claim"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "178", "def heartbeat"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "228", "rec.session"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "244", "ClaimRecord("),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "274", "def release_claim"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "377", "def release_claim_by_track"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "396-399", "NORMAL"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "425-427", "container"),
 ("a1", A+"state-scanner/lib/claim_lifecycle.py", "430", "claim_not_found"),
 ("a1", A+"state-scanner/lib/identity.py", "105", "def _parse_container_file"),
 ("a1", A+"state-scanner/lib/identity.py", "126", "def _write_container_file"),
 ("a1", A+"state-scanner/lib/identity.py", "191", "def get_container_id"),
 ("a1", A+"state-scanner/lib/identity.py", "222", "return label if label else uuid"),
 ("a1", A+"state-scanner/lib/identity.py", "242", "_hostname()"),
 ("a1", A+"state-scanner/lib/identity.py", "244", "return uuid"),
 ("a1", A+"state-scanner/lib/collision.py", "46", "from .claim_schema import"),
 ("a1", A+"state-scanner/lib/collision.py", "178", "def normalize_linked_issue"),
 ("a1", A+"state-scanner/lib/collision.py", "230", "def linked_issue_overlaps"),
 ("a1", A+"state-scanner/lib/collision.py", "265-266", "return"),
 ("a1", A+"state-scanner/lib/collision.py", "268", "_TERMINAL"),
 ("a1", A+"state-scanner/lib/collision.py", "272-273", "_TERMINAL"),
 ("a1", A+"state-scanner/lib/collision.py", "274-275", "linked_issue"),
 ("a1", A+"state-scanner/lib/collision.py", "278-279", "track_id"),
 ("a1", A+"state-scanner/lib/constants.py", "32", "STALE_TTL"),
 ("a1", A+"state-scanner/lib/constants.py", "36", "STALE_TTL: int = 1800"),
 ("a1", A+"state-scanner/lib/constants.py", "43-44", "NO production heartbeat loop"),
 ("a1", A+"state-scanner/lib/constants.py", "50", "Revisit when a heartbeat loop ships"),
 ("a1", A+"state-scanner/lib/constants.py", "51", "SWEEP_TTL"),
 ("a1", A+"state-scanner/lib/claim_schema.py", "130", "linked_issue"),
 ("a1", A+"state-scanner/lib/coordination_ref.py", "800", "push=False"),
 ("a1", A+"state-scanner/lib/coordination_ref.py", "119", "ReadClaimsResult"),
 ("a1", A+"state-scanner/lib/track_id.py", "61", "def derive_track_id"),
 ("a1", A+"phase-a-planner/SKILL.md", "9", "allowed-tools: Read, Write, Glob, Grep, Task, Skill"),
 ("a1", A+"phase-a-planner/SKILL.md", "60", "### 步骤执行"),
 ("a1", A+"phase-a-planner/SKILL.md", "62", "```yaml"),
 ("a1", A+"phase-a-planner/SKILL.md", "63", "A.1 - Spec 管理:"),
 ("a1", A+"phase-a-planner/SKILL.md", "64", "skill: spec-drafter"),
 ("a1", A+"phase-a-planner/SKILL.md", "67", "Level1"),
 ("a1", A+"phase-a-planner/SKILL.md", "68-70", "action"),
 ("a1", A+"spec-drafter/SKILL.md", "9", "user-invocable: true"),
 ("a1", A+"spec-drafter/SKILL.md", "10", "allowed-tools: Read, Write, Glob, Grep, AskUserQuestion"),
 ("a1", A+"spec-drafter/SKILL.md", "73", "## 执行流程"),
 ("a1", A+"state-scanner/SKILL.md", "143", "Layer L"),
 ("a1", A+"state-scanner/SKILL.md", "149", "触发"),
 ("a1", A+"state-scanner/SKILL.md", "166", "### JSON 消费 + surface 渲染"),
 ("a1", A+"state-scanner/SKILL.md", "168", "push_success"),
 ("a1", A+"state-scanner/SKILL.md", "176", "linked_issue_overlap"),
 ("a1", A+"state-scanner/SKILL.md", "178", "layer-l-integration"),
 ("a1", A+"state-scanner/references/layer-l-integration.md", "15", "Design A"),
 ("a1", A+"state-scanner/references/layer-l-integration.md", "45", "update_heartbeat()"),
 ("a1", A+"state-scanner/docs/coordination-ref-schema.md", "129", "### 3.2"),
 ("a1", A+"state-scanner/docs/coordination-ref-schema.md", "133-141", "unknown"),
 ("a1", A+"phase-b-developer/SKILL.md", "86", "B.0"),
 ("a1", A+"phase-b-developer/SKILL.md", "87", "precondition"),
 ("a1", A+"phase-b-developer/SKILL.md", "92", "--raw-track-id"),
 ("a1", A+"phase-b-developer/SKILL.md", "96-97", "auto_bootstrap"),
 ("a1", A+"phase-b-developer/SKILL.md", "98", "enabled"),
 ("a1", A+"branch-manager/SKILL.md", "146", "Part A1"),
 ("a1", A+"branch-manager/SKILL.md", "148", "--raw-track-id <carry-id>"),
 ("a1", A+"phase-d-closer/SKILL.md", "42", "D.2b"),
 ("a1", A+"phase-d-closer/SKILL.md", "51-52", "--raw-track-id"),
 ("a1", A+"phase-d-closer/SKILL.md", "55", "carry-id"),
 ("a1", A+"phase-d-closer/SKILL.md", "56", "STALE_TTL"),
 ("a1", A+"config-loader/SKILL.md", "134", "enabled"),
 ("a1", A+"config-loader/SKILL.md", "140", "mode"),
 ("a1", A+"config-loader/DEFAULTS.json", "24", "state_scanner"),
 ("a1", "standards/conventions/session-handoff.md", "101", "2.3"),
 ("a1", "standards/conventions/session-handoff.md", "217", "2.3.8"),
 ("a1", "standards/conventions/session-handoff.md", "223", "id"),
 ("a1", "standards/conventions/session-handoff.md", "238", "2.3.8.3"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "23", "_SKILL_ROOT"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "206", "class TestLinkedIssueOverlaps"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "377", "class TestSweepStaleActive"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "380", "def test_sweep_stale_cross_container_fresh_untouched"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "527", "class TestPhase1GateLinkedIssueCli"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "531", "_GATE"),
 ("a1", A+"state-scanner/tests/test_release_by_track.py", "586", "class TestLinkedIssueNormalizationSC"),
 ("a1", A+"state-scanner/tests/test_phase1_gate_telemetry.py", "94", "class TestTelemetryPartitionAntiSpoof"),
 ("a1", A+"state-scanner/tests/test_phase1_gate_telemetry.py", "164", "class TestCoordinationProbe"),
 ("a1", A+"state-scanner/tests/test_coordination_default_lockin.py", "21", "def test_config_loader_sot_default_true"),
 ("a1", A+"state-scanner/tests/test_coordination_default_lockin.py", "36", "def test_no_stale_default_false_wording"),
 ("a1", A+"state-scanner/tests/test_coordination_default_lockin.py", "53", "def test_phase_b_require_claim_present"),
 ("a1", A+"state-scanner/tests/test_coordination_default_lockin.py", "55-56", "assertIn"),
 ("a1", A+"state-scanner/tests/test_mainspec_phase0.py", "19", "DEFAULTS"),
 ("a1", A+"state-scanner/scripts/coordination_probe.py", "17-24", "Partition guarantee"),
 ("a1", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "222-228", "ARIA_COORDINATION_NO_PUSH"),
 ("a1", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "224", "phase-d-closer"),
 ("a1", "README.md", "8", "1.67.2"),
 ("a1", "README.md", "242", "1.67.2"),
 ("a1", "VERSION", "24", "1.67.2"),
 # ---- sibling
 ("sib", A+"audit-engine/SKILL.md", "83", "### Step 0: Anchor 固化"),
 ("sib", A+"audit-engine/SKILL.md", "85", "Round 1 启动前一次性"),
 ("sib", A+"audit-engine/SKILL.md", "119", "---"),
 ("sib", A+"audit-engine/SKILL.md", "121", "## 数据 Schema"),
 ("sib", A+"audit-engine/SKILL.md", "237", "权威可执行版见 references/"),
 ("sib", A+"audit-engine/SKILL.md", "412", "## 相关文档"),
 ("sib", A+"audit-engine/SKILL.md", "421", "最后更新"),
 ("sib", A+"audit-engine/references/execution-modes.md", "84", "## Convergence 模式"),
 ("sib", A+"audit-engine/references/execution-modes.md", "89", "Round N:"),
 ("sib", A+"audit-engine/references/execution-modes.md", "90", "1. 调用 agent-team-audit 单轮引擎"),
 ("sib", A+"audit-engine/references/execution-modes.md", "113", "## Challenge 模式"),
 ("sib", A+"audit-engine/references/execution-modes.md", "118", "Round N (一个完整周期):"),
 ("sib", A+"audit-engine/references/execution-modes.md", "119", "Step 1: 讨论组 spawn"),
 ("sib", A+"audit-engine/references/report-format.md", "50", "## 轮次记录"),
 ("sib", A+"audit-engine/references/report-format.md", "66", "### Round N (Final)"),
 ("sib", A+"config-loader/DEFAULTS.json", "124-128", "challenge"),
 ("sib", A+"phase-d-closer/tests/test_fetch_gate.py", "22", "_runner"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "21", "_resolve_default_branch"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "50-54", "_ORIGIN_HEAD_REFS"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "55", "_DEFAULT_BRANCH_FALLBACKS"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "86", "def _classify_error"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "108", "def _resolve_default_branch"),
 ("sib", A+"phase-d-closer/scripts/fetch_gate.py", "111-112", "sync.py"),
 ("sib", A+"session-closer/scripts/handoff_autofill.py", "48-51", "collectors"),
 ("sib", A+"session-closer/scripts/handoff_autofill.py", "403-407", "lib.identity"),
 ("sib", A+"state-scanner/scripts/coordination_probe.py", "80-85", "lib"),
 ("sib", A+"state-scanner/scripts/collectors/handoff_multibranch.py", "589-598", "cap"),
 ("sib", A+"state-scanner/scripts/collectors/multi_remote.py", "255", "def resolve_enforced_remotes"),
 ("sib", A+"state-scanner/scripts/collectors/multi_remote.py", "1376", "read_only_remotes"),
 ("sib", A+"state-scanner/tests/test_coordination_no_push.py", "132", "subprocess"),
 ("sib", A+"run_all_tests.sh", "44-45", "pytest"),
 ("sib", A+"run_all_tests.sh", "48", "-name tests"),
 ("sib", A+"run_all_tests.sh", "50", "test_*.py"),
 ("sib", A+"run_all_tests.sh", "62-66", "SKIP"),
 ("sib", A+"run_all_tests.sh", "71", "unittest"),
 ("sib", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "76", "28"),
 ("sib", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "142-159", "拆"),
 ("sib", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "161-174", "descriptive"),
 ("sib", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "176-197", "MINOR"),
 ("sib", "aria-plugin-benchmarks/AB_TEST_OPERATIONS.md", "519", "28"),
 # ---- linked
 ("lnk", A+"state-scanner/tests/test_release_by_track.py", "23-25", "from lib"),
 ("lnk", "standards/openspec/templates/proposal-minimal.md", "3-5", "Created"),
 ("lnk", "standards/openspec/templates/proposal-minimal.md", "40", "## Template Usage Notes"),
 ("lnk", A+"spec-drafter/SKILL.md", "75", "```yaml"),
 ("lnk", A+"spec-drafter/SKILL.md", "107-110", "A.1.4"),
 ("lnk", A+"spec-drafter/SKILL.md", "125", "### Level 2 预览"),
 ("lnk", A+"spec-drafter/SKILL.md", "127", "```"),
 ("lnk", A+"spec-drafter/SKILL.md", "139", "> **Level**"),
 ("lnk", A+"spec-drafter/SKILL.md", "140", "> **Status**: Draft"),
 ("lnk", A+"spec-drafter/SKILL.md", "162", "```"),
 ("lnk", A+"spec-drafter/SKILL.md", "166", "```"),
 ("lnk", A+"spec-drafter/SKILL.md", "179", "```"),
 ("lnk", A+"spec-drafter/SKILL.md", "336", "## tasks.md 格式要求"),
 ("lnk", A+"spec-drafter/SKILL.md", "424", "## 相关文档"),
 ("lnk", A+"spec-drafter/SKILL.md", "429", "proposal-minimal.md"),
 ("lnk", A+"state-scanner/scripts/collectors/custom_checks.py", "63", "#"),
 ("lnk", A+"state-scanner/scripts/collectors/custom_checks.py", "121-124", "YAML"),
 ("lnk", A+"state-scanner/scripts/collectors/custom_checks.py", "342", "subprocess"),
 ("lnk", A+"state-scanner/scripts/collectors/custom_checks.py", "399", "config_path"),
 ("lnk", A+"state-scanner/scripts/issue_cache_freshness_probe.py", "148-149", "argv"),
 ("lnk", A+"state-scanner/scripts/coordination_probe.py", "140-141", "argv"),
 ("lnk", A+"state-scanner/SKILL.md", "71", "CLAUDE_PLUGIN_ROOT:-aria"),
 ("lnk", ".aria/state-checks.yaml", "12", "- name:"),
 ("lnk", ".aria/state-checks.yaml", "319", "- name:"),
 ("lnk", "aria/.claude-plugin/plugin.json", "4", "1.67.2"),
 ("lnk", "aria/.claude-plugin/marketplace.json", "3", "1.67.2"),
 ("lnk", "aria/.claude-plugin/marketplace.json", "16", "1.67.2"),
 ("lnk", "aria/README.md", "5", "1.67.2"),
 ("lnk", "aria/VERSION", "3-4", "1.67.2"),
 ("lnk", "README.zh.md", "3", "translated"),
 ("lnk", "README.zh.md", "10", "1.67.2"),
 ("lnk", "README.zh.md", "244", "1.67.2"),
 ("lnk", "README.ja.md", "244", "1.67.2"),
 ("lnk", "README.ko.md", "244", "1.67.2"),
 ("lnk", "openspec/archive/2026-06-11-audit-drift-guard/proposal.md", "5", "关联 Issue"),
 ("lnk", "openspec/archive/2026-08-23-linked-issue-normalization/proposal.md", "6", "> **关联 Issue**: 无"),
 ("lnk", "openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md", "61", "关联 Issue"),
 ("lnk", "openspec/archive/2026-08-23-linked-issue-normalization/proposal.md", "257", "include_terminal"),
 ("lnk", "openspec/archive/2026-08-23-linked-issue-normalization/proposal.md", "259", "include_terminal"),
 ("lnk", "openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md", "13", "10CG/Aria#174"),
 ("lnk", "openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md", "96", "阻塞"),
 ("lnk", "openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md", "423", "阻塞"),
 ("lnk", "openspec/changes/linked-issue-field-availability/proposal.md", "388", "CLAUDE_PLUGIN_ROOT"),
 ("lnk", "openspec/changes/linked-issue-field-availability/proposal.md", "278", "lib/"),
 ("lnk", "openspec/changes/linked-issue-field-availability/proposal.md", "490", "A.2"),
 ("lnk", "openspec/changes/linked-issue-field-availability/proposal.md", "601", "A.2"),
 ("lnk", "openspec/changes/sibling-spec-probe/proposal.md", "171", "lib/"),
 ("lnk", "openspec/changes/sibling-spec-probe/proposal.md", "473", "B.1"),
 ("lnk", "openspec/changes/sibling-spec-probe/proposal.md", "443-452", "0.15"),
 ("lnk", "openspec/changes/sibling-spec-probe/proposal.md", "118", "关联 Issue"),
]
ok = bad = 0; fails = []
for spec, f, rng, exp in CASES:
    a, _, b = rng.partition("-"); b = b or a
    r = subprocess.run(["sed", "-n", f"{a},{b}p", f"{ROOT}/{f}"], capture_output=True, text=True)
    txt = r.stdout
    hit = exp in txt
    ok += hit; bad += (not hit)
    if not hit:
        fails.append((spec, f, rng, exp, txt.strip()[:160].replace("\n", " ⏎ ")))
print(f"[8b] anchors checked: {len(CASES)}; PASS={ok} FAIL={bad}")
for x in fails: print("   FAIL", x)

```

**输出**:

```text
[8b] anchors checked: 214; PASS=206 FAIL=8
   FAIL ('a1', 'aria/skills/state-scanner/scripts/phase1_gate.py', '1155-1158', 'linked_issue', '#           [--repo-path] [--remote] [--no-push] ⏎ #   env   : ARIA_COORDINATION_NO_PUSH=1|true|yes ⇔ --no-push (harness safety: ⏎ #           the AB benchmark runs')
   FAIL ('a1', 'aria/skills/state-scanner/scripts/phase1_gate.py', '1308-1311', 'ARIA_COORDINATION_NO_PUSH', 'env_no_push = no_push_requested_by_env() ⏎     no_push = bool(args.no_push or env_no_push) ⏎     push_skipped_reason = ( ⏎         "cli_flag" if args.no_push else ("e')
   FAIL ('a1', 'aria/skills/branch-manager/SKILL.md', '148', '--raw-track-id <carry-id>', '`action: create` (= 进 Phase B.1) 前, 本 session 必须已有 active claim; 无则先跑')
   FAIL ('a1', 'standards/conventions/session-handoff.md', '223', 'id', '#### 2.3.8.1 Schema')
   FAIL ('sib', 'aria/skills/audit-engine/references/report-format.md', '66', '### Round N (Final)', '')
   FAIL ('lnk', 'aria/skills/state-scanner/tests/test_release_by_track.py', '23-25', 'from lib', '_SKILL_ROOT = str(Path(__file__).resolve().parents[1]) ⏎ if _SKILL_ROOT not in sys.path: ⏎     sys.path.insert(0, _SKILL_ROOT)')
   FAIL ('lnk', 'openspec/archive/2026-08-23-linked-issue-normalization/proposal.md', '259', 'include_terminal', '> ⇒ **D6 与 §接口面 的「签名与 schema 不变」自此限定于本 Spec 的变更面**: 本 Spec 不改签名; 母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**。')
   FAIL ('lnk', 'openspec/changes/sibling-spec-probe/proposal.md', '118', '关联 Issue', '**`BAD_TOKEN` 的归档选择与理由 (主控要求明确选一档并写出来)**')

```

### 杂项实核 (shell, 逐字)

```text
$ ls README*.md
README.ja.md
README.ko.md
README.md
README.zh.md
$ git submodule status
 d69091dfdeb0c6cd83b03da2492812d33cec3712 aria (v1.67.2)
+92acce5cef03eb5cde2f2bb73974f800473d52a9 aria-orchestrator (heads/feature/m6-cost-model-telemetry)
 334c609ef55d4c5970ea1ea7e91d64193478e726 standards (remotes/github/master)
$ grep -rh "^\s*def test_" aria/skills/state-scanner/tests/*.py | wc -l
1425
$ grep -c "^  - name:" .aria/state-checks.yaml
12
$ ls aria-plugin-benchmarks/ab-suite/*.json | wc -l; test -f …/audit-engine.json
31
absent
$ grep -n "version\|skills_covered\|total_eval_cases" ab-suite/version.yaml | head -5
1:version: "1.1.0"
4:skills_covered: 29
5:total_eval_cases: 58
8:  - version: "1.1.0"
11:  - version: "1.0.0"
$ python3 json loads: state-scanner.json / phase-a-planner.json / spec-drafter.json
state-scanner 1.6.0 12
phase-a-planner 1.0.0 2
spec-drafter 1.0.0 [1, 2]
$ ls aria/skills/audit-engine/
references
SKILL.md
$ ls (新建 files)
ls: cannot access 'aria/skills/state-scanner/lib/linked_issue_field.py': No such file or directory
ls: cannot access 'aria/skills/state-scanner/scripts/linked_issue_field_probe.py': No such file or directory
ls: cannot access 'aria/skills/audit-engine/scripts/sibling_spec_probe.py': No such file or directory
ls: cannot access '.aria/linked-issue-field-grandfathered.txt': No such file or directory
$ phase1_gate.py linked-issue lines
87:    from ..lib.collision import linked_issue_overlaps
126:    from lib.collision import linked_issue_overlaps  # type: ignore[import]
1154:#   args  : --raw-track-id --phase [--mode advisory|block] [--linked-issue]
1282:        "--linked-issue",
1335:            out["linked_issue_overlap"] = linked_issue_overlaps(
1340:            out["linked_issue_overlap"] = []
$ sed -n 146,150p branch-manager/SKILL.md
### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)

`action: create` (= 进 Phase B.1) 前, 本 session 必须已有 active claim; 无则先跑
`phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory` (命令模板见
phase-b-developer SKILL.md §B.0)。直接调 branch-manager 绕过 phase-b-developer 的
$ sed -n 118p linked-issue proposal
> **Linked Issue**: `{<org>/<repo>#<n>}`
$ counts
phase-a-planner yaml fences: 8
spec-drafter SKILL lines: 438
audit-engine SKILL lines: 421
execution-modes lines: 144
每轮入口 count: 0
update_heartbeat: skills/state-scanner/references/layer-l-integration.md:45:| `heartbeat` | `phase-b-develop
coordination in state_scanner: False
$ sed -n 134p;140p config-loader/SKILL.md
state_scanner.coordination.enabled:
state_scanner.coordination.mode:
test_coordination_no_push def test_: 16
$ git -C aria ls-remote origin master / github master
d69091dfdeb0c6cd83b03da2492812d33cec3712	refs/heads/master
d69091dfdeb0c6cd83b03da2492812d33cec3712	refs/heads/master
corpus: changes=9 archive=140 cc1bdef=147
$ est field usage across corpus
openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml est_hours=0 estimated_hours=39
openspec/changes/aria-2.0-m6-dispatch-input-delivery/detailed-tasks.yaml est_hours=30 estimated_hours=0
openspec/changes/linked-issue-field-availability/detailed-tasks.yaml est_hours=25 estimated_hours=0
openspec/changes/sibling-spec-probe/detailed-tasks.yaml est_hours=18 estimated_hours=0
openspec/archive/2026-08-18-secret-guard-per-segment-evaluation/detailed-tasks.yaml est_hours=0 estimated_hours=29
openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml est_hours=0 estimated_hours=27
openspec/archive/2026-08-22-secret-guard-manifest-precision/detailed-tasks.yaml est_hours=0 estimated_hours=17
openspec/archive/2026-08-23-linked-issue-normalization/detailed-tasks.yaml est_hours=28 estimated_hours=0
openspec/archive/2026-08-23-pre-merge-gate-no-run-for-branch/detailed-tasks.yaml est_hours=0 estimated_hours=20
$ grep consumers of est(imated)_hours in aria/skills (code)
(none)

```
