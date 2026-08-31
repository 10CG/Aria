---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-30T16:32:16.979Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 2
minor_count: 1
r1_disposition: {closed: 8, partial: 0, not_addressed: 0}
introduced_by_fix: 3
---

# post_planning R2 — A4 code-reviewer (机械一致性镜头, combined-mode 三份, R1 清账后版本)

> 工作树: 主仓 HEAD c120f9e / aria d69091d, 2026-08-30 UTC。六份被审文件 sha256 见「实测记录 [0]」; 本席未改任何被审文件 (全部脚本跑在 scratchpad, 坏输入跑在 scratchpad 副本; 审后 sha256 复核一致)。

## 摘要

R1 八项检查在三份终版全部重跑 (82 任务), **结构层与 R1 四条 finding 全部闭合**: `yaml.safe_load` 与归档门 `parse_detailed_tasks` 三份 parse_ok (25/18/39, status 集合 = {pending}); parent 与 tasks.md checkbox 三份**序列相等** (非仅集合相等); 必需字段 12 项零缺席, `estimated_hours` 三份统一为 `"a-b"` 串且逐任务求和 = metadata (50-86 / 55-87 / 94-153), `est_hours` 零残留, linked TASK-020 `reason` 已补; 依赖无悬空 / 无自依赖 / 无环; 母 Spec 第 6 组六条边已翻转 (TASK-025~030 deps 只含 {001, 003} 与链前任务; TASK-017~023 各含对应 RED 直接边), 七条 verification[0] 全部改为「落文本后由红转绿 (基线 d69091d 先红)」, TASK-025 notes 改为可执行措辞; 覆盖表 (SC, TASK) 对 28 / 46 / 55 在 **verification 层**全部命中 (R1 是 17 对缺 + SC-3 零命中); TASK-038 deliverables 改为 7 文件 (`aria` gitlink / VERSION / README.md / CLAUDE.md / README.{zh,ja,ko}.md), 全部实存且行号锚点 (`:24` / `:139,:141` / `:8,:242` / `:3,:10,:244`) 实读命中 `1.67.2`, 与 086ee32 的 7 文件集合相等。`1.68.0` / `1.67.3` / `README.zh-CN` / `parallelizable` / `.gitmodules` 残留只剩清账留痕句与「非 .gitmodules」澄清句; `<vNEXT>` 32 处形态一致。fix 引入的新表面: 42 条清账表声称的边在 yaml 逐条实存; 新增 `seam_rules` / `ab_suite_seam_rules` 为 str 列表, eval id `max(id)+1` 约定三份同写; 清账新引的 19 处锚点 (proposal :278/:473/:511/:513/:525/:578/:616/:683/:754/:798, `phase1_gate.py:1154`, `branch-manager:149`, `state-checks.yaml:141/:161`, AB 手册 :142) 全部实读命中。

**Major 2 条, 都是 R1 fix 引入的「证据/自述层」缺陷, 不动计划本体**: (1) sibling tasks.md「机械核验」段贴的脚本**逐字不可复现其贴出的输出** —— 正则里全部 `\d` 被写成 `\\d` (6 行), 原样亲跑 RESULT=FAIL (parent 18 vs 0 / estimated_hours False), 且 (e) 并行-同文件检查在原样脚本下**恒空** (`parallel line []`); 去转义后才 PASS 并能拒绝两个坏输入。(2) sibling yaml `execution_order` 第 1/2 行与 `metadata.phase_b1_preconditions[1]` 没跟上「主控追记」新加的两条边 (TASK-003 ← TASK-002, TASK-004 ← TASK-003): 自述仍写「[并行, 不同文件] TASK-001 · TASK-002 · TASK-003」与「TASK-004 ← 001, 002」, 而追记要治的正是 002/003 并行时 TASK-002「无 audit-engine.json」断言会红。Minor 1 条 (母 Spec): 贴出的脚本 (d) 不展开 `TASK-013/014` 缩写 (51 对 vs 实际 55 对, 4 对未检); 贴出的 [a] 输出「40 对」与当前文件 (37 对, TASK-003 `phase1_gate.py` 后补了「只读」) 不一致, 「出入 #5」一句同陈旧; flag 映射行 `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035) 在 TASK-032~035 块零字面 (R1 已观测、未在处方内, 残留)。

由 R1 fix 引入的占比: 3/3 条 finding 的主体都是清账新增文本 (机械核验段 / 追记边 / 出入段), 子项 5 处中 4 处为 fix 引入、1 处残留。

## R1 finding 逐条闭合表 (本席 R1 8 条, 程序化判)

| R1 id | 严重度 | 判定 | 证据 (实测记录编号) |
|-------|--------|------|---------------------|
| bd55ab9c | critical | **closed** | [2] TASK-025 deps=[001,003], 026~030 = [003, 前一任务]; TASK-017/018 含 025, 019 含 026, 020 含 030, 021 含 028+030, 022 含 027, 023 含 029; 七条 verification[0] 逐字「本任务落文本后, 对应 TASK-02x 由红转绿 (基线 d69091d 上先红…)」; TASK-025 notes「R1 C1 后在依赖图上可执行: 本任务是 TASK-017/018 的上游」; [1] 后向边恰为这 9 条 (含原有 017→022), 无环; 坏输入 (025 回指 017) 被贴出脚本 (b)+(c) 抓到 [5c] |
| df090b25 | major | **closed** | [1] 三份 `estimated_hours` 全为 `"a-b"` 串, `est_hours` 零残留, metadata 与逐任务求和一致 (50-86 / 55-87 / 94-153); linked TASK-020 `reason` = 「全量回归 + 零改动断言 (AGENT_MAPPING …; R1/A4 df090b25 补)」 |
| fead49d5 | major | **closed** | [3] 母 Spec 覆盖表 55 对 (含 `TASK-013/014` 缩写展开、`SC-5 / SC-6 / SC-7` 展开) 在 verification 层 0 缺; SC-3 在 TASK-004 首条 + TASK-011「TASK-004 全绿 (SC-3)」; TASK-018 五个 flag 字面 / TASK-019 三个字面全部在块内 [6]。处方外残留 (031–035 的 `--no-push` 字面) 记入 minor 9db42f0a |
| 518a7d7f | major | **closed** | [2][6] TASK-038 deliverables = aria / VERSION / README.md / CLAUDE.md / README.zh.md / README.ja.md / README.ko.md, 全部 `test -e` 为真; 与 086ee32 `--stat` 7 文件集合相等; i18n 三份 :3/:10/:244 实读含 `1.67.2`; `README.zh-CN` 只剩清账留痕 3 行 + TASK-038 notes「已改」 |
| 62285020 | minor | **closed** | [3] linked 覆盖表 28 对 verification 层 0 缺; flag 映射 12 对贴出脚本亲跑 0 缺 [5a] |
| 4bf32c17 | minor | **closed** | [3] sibling 覆盖表 46 对 verification 层 0 缺 (含 (SC-16, 016) / (SC-18, 006)) |
| 948363d3 | minor | **closed** | [7] TASK-010 verification[1] 改为「三条 import 逐字存在 … 同块允许第四符号 `is_sentinel` … 块外零 `from lib.` / `from collectors.`」(『包含』口径) |
| b0e8b171 | minor | **closed** | [6] `phase1_gate.py:1154` 实读 = `--raw-track-id --phase [--mode advisory|block] [--linked-issue]` 契约行; `branch-manager/SKILL.md:149` 实读 = `--raw-track-id <carry-id>` 命令行; task_group 形态按主控裁「三份内部各自一致」不动 (三份内部各自一致已验) |

## Findings

| id | severity | 来源 | category | scope | type | 描述 + 证据 + 处方 |
|----|----------|------|----------|-------|------|-------------------|
| 4a669876 | major | **fix 引入** | documentation | openspec/changes/sibling-spec-probe/tasks.md | issue | **「机械核验」段贴出的脚本逐字不可复现其贴出的输出; (e) 检查在贴出形态下恒空。** 证据 (实测记录 [5b]): 从 tasks.md `## 机械核验` 段抽出 ```python 块 (92 行) 原样执行 ⇒ `parent 1:1 … -> False (18 vs 0)`, `estimated_hours present on all = False`, `(e) parallel line []: same-file pairs = none`, `RESULT: FAIL parent mismatch […] vs []`, exit 1; 而 tasks.md :262-272 贴的输出是 `True (18 vs 18)` / `True` / `parallel line ['TASK-001', 'TASK-002', 'TASK-003']` / `RESULT: PASS`。根因: 脚本文本里 6 行正则把 `\d` / `\[` / `\.` 写成 `\\d` / `\\[` / `\\.` (:233 `r"TASK-\\d{3}"`, :245 `r"^- \\[[ x]\\] (\\d+\\.\\d+) "`, :250 `r"\\d+-\\d+"`), 在 raw string 里是字面反斜杠, 匹配不到任何任务号 / checkbox / 工时串。后果: (i) 段落声称的「亲跑 PASS」与「拒绝能力 (13 对缺边 / (d) 缺 / (e) 11 对)」在贴出物上不成立 (memory `check-runs-at-baseline-first`: 新机械检查须在基线亲跑三态; `cross-doc-claim-verify-at-target`); (ii) (e) 在贴出形态下对任何 `execution_order` 并行标记都返回空列表 = 恒绿 (坏输入 v2 把同文件 RED 行改回「[并行, RED]」, 原样脚本仍 `parallel line []`, 去转义脚本报 10 对同文件并行 FAIL [5b])。**不变量本身成立** (本席独立脚本 [1] + 去转义脚本 [5b] 均 PASS), 故 major 非 critical。处方: 把三处 `\\` 改回 `\` (或改用 `re.compile("TASK-[0-9]{3}")` 这类无反斜杠写法), 重跑后用真实输出替换 :262-272; 顺手让 (e) 在没有任何并行行时打印「(e) 0 parallel lines」而非静默, 避免下次恒空不可见。 |
| ea33f282 | major | **fix 引入** | implementation | openspec/changes/sibling-spec-probe/detailed-tasks.yaml | issue | **`execution_order` 第 1/2 行与 `metadata.phase_b1_preconditions[1]` 没跟上「主控追记」新加的两条边, 自述与依赖图打架。** 证据 (实测记录 [4]): yaml deps 现为 TASK-003 = [TASK-002], TASK-004 = [TASK-001, TASK-002, TASK-003] (tasks.md :157 主控追记 (1)(2) 两条一行改动, 已实存); 但 `execution_order[0]` 仍逐字 `[并行, 不同文件] TASK-001 (硬前置断言, 阻塞门) · TASK-002 (基线三态, 只读观测) · TASK-003 (AB 套件文件, B.1 前置)`, `execution_order[1]` 仍 `TASK-004 (测试骨架 + SC-21)  ← 001, 002`; `phase_b1_preconditions[1]` 仍「上游边: TASK-015 / 016 (指令面接线) 与 TASK-017 (AB 实跑) 的 dependencies 各含 TASK-003」, 漏掉追记加的 TASK-004 边 (proposal :473「Phase B.1 不得开始」的落点正是这条); tasks.md :275「已知限 … 已上报主控 (未自行加边)」也停在追记前。为什么重要: 追记要治的正是「002 与 003 并行时 TASK-002『无 audit-engine.json』断言会红」, 而执行者 (人或 subagent) 读的是 `execution_order` 而非逐任务 deps —— 现在两处方向相反, 同一 R1 A2 critical (a257ffa4) 的形状在自述层复发 (memory `fix-the-class`: 改了 deps 没改它的三个自述兄弟位置); 贴出脚本 (e) 只查「并行行内同文件对」, 001/002/003 不同文件 ⇒ 结构上抓不到这种「有依赖边却标并行」的矛盾 (memory `invariant-dimension`)。处方: `execution_order[0]` 改为「TASK-001 ‖ (TASK-002 → TASK-003) [002/003 串行: 002 断言 ab-suite 无 audit-engine.json, 003 建它]」, `[1]` 改为「← 001, 002, 003」; `phase_b1_preconditions[1]` 上游边补 TASK-004; tasks.md :275 已知限尾句改「主控已加边, 见追记」; 机械核验加一条 (f)「execution_order 标『并行』的行内任务两两互不在对方 (传递) deps 里」并在坏输入 (把 003 ← 002 边留着、行内仍标并行) 上验红。 |
| 9db42f0a | minor | fix 引入 ×2 / 残留 ×1 | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md | issue | 母 Spec「机械核验」段三处小项: (1) **fix 引入** — 贴出脚本 (d) 用 `re.findall(r"TASK-\d{3}", cells[3])` 抽表中 TASK, 不展开覆盖表 4 行的 `TASK-013/014` / `TASK-017/018` 缩写 (:100 / :108 / :118 / :127), 故报「51 对」; 本席展开后为 **55 对**, 漏检的 4 对 = (SC-2, 014) (SC-12, 018) (SC-22, 018) (SC-29, 014) —— 恰是 R1 fead49d5 点名的对, 当前 verification 已含 token (本席 [3] 55/55 命中), 但贴出脚本对它们的回退不设防。(2) **fix 引入** — 贴出输出 :429「[a] 同文件写入对 40 对 (共写文件 19 个)」与 `phase1_gate.py: TASK-003 -> 014 -> 015 -> 016`, 原样脚本对当前文件亲跑为 **37 对** 与 `TASK-014 -> 015 -> 016` [5c] —— TASK-003 的 `phase1_gate.py` / `release_gate.py` 两行在脚本跑后补了「只读核验」注释, 输出没重贴; 「出入 #5」:264「TASK-003 的 16 条 deliverable 未标只读」同陈旧 (实为 19 行、2 行标只读)。(3) **残留** (R1 fead49d5 [4c] 已观测, 处方只点 018/019) — flag 映射行 :133 `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035): TASK-032/033/034/035 块内两字面均零命中 (031 有 env 名无 `--no-push`; 001 有 `--no-push` 无 env 名) [6]。处方: (1) 缩写展开 `TASK-(\d{3})((?:/\d{3})+)?`; (2) 重跑后重贴输出、改 :264 一句; (3) 映射行改为 (001, 031) 或在 032–035「运行前置」句补 `ARIA_COORDINATION_NO_PUSH=1` 字面 (TASK-031 已有此句, 同形复制)。 |

**已证伪的怀疑 (留痕, 不构成 finding)**: sibling TASK-001 verification「否则本任务 status=blocked」不与 C3「不用 `blocked`」冲突 —— C3 说的是版本档未裁的发布任务, TASK-001 是 owner (i) 硬前置, 且 `blocked` 是 `detailed_tasks.py:28` 列举的合法残留态; linked yaml verification 出现 `SC-19` 而本 Spec 只有 10 条 SC —— 上下文逐字「探针 Spec SC-19 `_RAW_KEY_BLACKLIST`」, 是限定了的跨 Spec 引用; a1 TASK-017 → TASK-022 后向边为 R1 前既有 (R1 [2-dir] 环路径已含), 非本轮引入; sibling TASK-014 被本席 RED 启发式误捕 (title 含「测试」), 实为 G3 GREEN 收口, 依赖 010–013 正确; 三份 `(新建)` 标记文件今日全部不存在, 「未标新建但不存在」的 12 处全是同 Spec 上游任务新建的同一文件 (R1 同口径剔除); a1 `docs/handoff/` 标新建为目录追加型宿主。

## Verdict

**PASS_WITH_WARNINGS** (0 critical / 2 major / 1 minor)。计划本体 (依赖图 / 字段 / 覆盖表 / 发布面) 在机械层已收敛; 两条 major 都在清账新增的证据/自述文本上 (脚本文本转义、追记后未同步的三处自述), 均为定点一行到几行的改动, 不触 proposal、不改编号、不改边。

## Vote

**REVISE (定点, 仅 sibling 两文件 + 母 tasks.md 三小处; 不需 R3 全席)**。理由: (a) R1 四条本席 finding 8/8 closed, 无 partial; (b) 本轮 3 条 finding 全部由 fix 引入的新文本承载 (memory `marginal-return-negative`: 本轮 fix 引入占比 = 3/3, 已到拐点 —— 再开通用轮只会审到更多自述文本), 处方可由执笔席 10 分钟内落地并用本报告 [5b]/[5c] 两个坏输入自证; (c) 建议主控收账方式 = 定向复核 (重跑本席 chk1 + 去转义后的 sibling 脚本 + a1 脚本, 三者 exit 0 且贴出输出与亲跑一致) 而非新一轮五席。

## 实测记录 (脚本 + 逐字输出; 主仓 HEAD c120f9e / aria d69091d; 2026-08-30 16:09–16:24 UTC)

### [0] 被审六份 sha256 (审前; 本席未改)

```
d5b1429e030a2e8e5cffdcdab53ca408aa92e8e3d00ce2e4b63363db64281250  openspec/changes/linked-issue-field-availability/tasks.md
4a3f7e12577e596db386d87cae820a46bd2b2f39e04d2f01d7b0c1e039d15e88  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
9853d600335aa219f3fd6a2d897a946fbb998799c2e27f05d5b4550a3b19d32c  openspec/changes/sibling-spec-probe/tasks.md
09380e19711c052a87d2645d21936e2301a8b0e85764f8c1d7a7a3040fa2c1d1  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
55e4f13738a390acd064eba3d28a5ed297c4cafd0fef95e176b4d2b61fe86824  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
270cb59adc10497628f58fe549a3e999d9d42a2dcd658d9cdeb4edfde504a159  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```

### [1] 检查 1/3/6/7 — 字节卫生 · 两解析器 · status 枚举 · parent 序列 1:1 · 必需字段 · estimated_hours 形态与求和 · deps 悬空/自依赖/环 · 后向边 · RED→GREEN 方向 (启发式) · agent 集合

脚本 `chk1_battery.py`:

```python
#!/usr/bin/env python3
"""R2/A4 检查 1: R1 8 项在三份终版重跑 (parent 1:1 / deps 存在·无环·方向 / status 枚举 / 必需字段 / 两解析器 / total·估时汇总)."""
import re, sys, os, yaml, itertools
sys.path.insert(0, "/home/dev/Aria/aria/skills/state-scanner/scripts")
from lib.detailed_tasks import parse_detailed_tasks
ROOT = "/home/dev/Aria/openspec/changes/"
SPECS = ["linked-issue-field-availability", "sibling-spec-probe", "a1-entry-claim-duplicate-work-guard"]
REQ = ["id","parent","title","status","estimated_hours","dependencies","deliverables","verification","agent","reason","complexity","task_group"]
HRS = re.compile(r"\d+-\d+")
overall = []
for s in SPECS:
    print(f"\n===== {s}")
    raw = open(ROOT+s+"/detailed-tasks.yaml", encoding="utf-8").read()
    md = open(ROOT+s+"/tasks.md", encoding="utf-8").read()
    # 字节卫生
    ctrl=sum(1 for c in raw if ord(c)<32 and c!=chr(10))
    print(f"  CRLF={raw.count(chr(13))} tab={raw.count(chr(9))} ctrl={ctrl}")
    doc = yaml.safe_load(raw)
    tasks = doc["tasks"]; ids=[t["id"] for t in tasks]; T={t["id"]:t for t in tasks}
    print(f"  safe_load OK: tasks={len(tasks)} dup_ids={[i for i in set(ids) if ids.count(i)>1]} total_tasks(meta)={doc['metadata'].get('total_tasks')}")
    r = parse_detailed_tasks(raw)
    print(f"  parse_detailed_tasks: parse_ok={r['parse_ok']} n={len(r['tasks'])} statuses={sorted({t['raw_status'] for t in r['tasks']})} reason={r['reason']!r}")
    # status 枚举
    st = sorted({t["status"] for t in tasks}); print(f"  status 枚举={st}")
    # parent 1:1
    parents=[t["parent"] for t in tasks]
    boxes=re.findall(r"^- \[[ x]\] (\d+\.\d+) ", md, re.M)
    print(f"  parent 1:1: parents=={len(parents)} boxes=={len(boxes)} seq_equal={parents==boxes} set_equal={set(parents)==set(boxes)} orphan_parent={sorted(set(parents)-set(boxes))} orphan_box={sorted(set(boxes)-set(parents))}")
    # 必需字段
    missing = {f:[t["id"] for t in tasks if f not in t] for f in REQ}
    missing = {f:v for f,v in missing.items() if v}
    print(f"  必需字段缺失={missing or 'none'}")
    hrs=[(t["id"],t.get("estimated_hours")) for t in tasks]
    bad_hrs=[(i,h) for i,h in hrs if not (isinstance(h,str) and HRS.fullmatch(h))]
    print(f"  estimated_hours 全为 'a-b' 串: {not bad_hrs} bad={bad_hrs}; est_hours 残留={[t['id'] for t in tasks if 'est_hours' in t]}; meta.estimated_hours={doc['metadata'].get('estimated_hours')!r}")
    lo=sum(int(h.split('-')[0]) for _,h in hrs if isinstance(h,str) and HRS.fullmatch(h)); hi=sum(int(h.split('-')[1]) for _,h in hrs if isinstance(h,str) and HRS.fullmatch(h))
    print(f"  逐任务求和 lo-hi = {lo}-{hi}")
    # deps 存在 / 无环
    deps={t["id"]:list(t.get("dependencies") or []) for t in tasks}
    dang=[(a,b) for a in deps for b in deps[a] if b not in T]
    selfdep=[a for a in deps if a in deps[a]]
    color={i:0 for i in T}; cyc=[]
    def dfs(u,st):
        color[u]=1; st.append(u)
        for v in deps[u]:
            if v not in T: continue
            if color[v]==1: cyc.append(st+[v])
            elif color[v]==0: dfs(v,st)
        st.pop(); color[u]=2
    for i in T:
        if color[i]==0: dfs(i,[])
    print(f"  deps: 悬空={dang} 自依赖={selfdep} 环={cyc}")
    # 方向: 后向边 (依赖编号更大的任务) 列出 (供人工看), RED/GREEN 判定按 group
    back=[(a,b) for a in deps for b in deps[a] if ids.index(b)>ids.index(a)]
    print(f"  后向边 (依赖编号更大者) = {back}")
    def anc(i,seen=None):
        seen=set() if seen is None else seen
        for j in deps[i]:
            if j in T and j not in seen: seen.add(j); anc(j,seen)
        return seen
    A={i:anc(i) for i in T}
    # 通用 RED 判据: title 含 RED/红测/测试 且 deliverables 含 tests/
    red=[i for i in T if any('/tests/' in str(d) for d in (T[i].get('deliverables') or [])) and re.search(r"RED|红|测试|断言|substitute", T[i]["title"])]
    green={i for i in T if i not in red and any(('/tests/' not in str(d)) for d in (T[i].get('deliverables') or [])) and not re.search(r"前置|断言|锚点|观测|核对", T[i]["title"])}
    viol=[(i,sorted(A[i]&green)) for i in red if A[i]&green]
    print(f"  RED 任务={red}\n  RED 传递依赖 GREEN (实现/文本) = {viol or 'none'}")
    # agent_allocation vs agent 字段
    al=doc.get("agent_allocation") or doc["metadata"].get("agent_allocation")
    agents=sorted({t["agent"] for t in tasks})
    print(f"  agents={agents}; agent_allocation keys={sorted(al) if isinstance(al,dict) else al}")
    if isinstance(al,dict):
        for k,v in al.items():
            lst = v.get("tasks") if isinstance(v,dict) else v
            if isinstance(lst,list):
                got=sorted(i for i in T if T[i]["agent"]==k); exp=sorted(lst)
                if got!=exp: print(f"    MISMATCH agent {k}: alloc={exp} actual={got}")
```

输出 (逐字):

```

===== linked-issue-field-availability
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=25 dup_ids=[] total_tasks(meta)=25
  parse_detailed_tasks: parse_ok=True n=25 statuses=['pending'] reason='25 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==25 boxes==25 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='50-86'
  逐任务求和 lo-hi = 50-86
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-005', 'TASK-006']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'new_agents', 'note', 'qa-engineer', 'tech-lead']

===== sibling-spec-probe
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=18 dup_ids=[] total_tasks(meta)=18
  parse_detailed_tasks: parse_ok=True n=18 statuses=['pending'] reason='18 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==18 boxes==18 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='55-87'
  逐任务求和 lo-hi = 55-87
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = []
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-014']
  RED 传递依赖 GREEN (实现/文本) = [('TASK-014', ['TASK-010', 'TASK-011', 'TASK-012', 'TASK-013'])]
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']

===== a1-entry-claim-duplicate-work-guard
  CRLF=0 tab=0 ctrl=0
  safe_load OK: tasks=39 dup_ids=[] total_tasks(meta)=39
  parse_detailed_tasks: parse_ok=True n=39 statuses=['pending'] reason='39 task(s) parsed'
  status 枚举=['pending']
  parent 1:1: parents==39 boxes==39 seq_equal=True set_equal=True orphan_parent=[] orphan_box=[]
  必需字段缺失=none
  estimated_hours 全为 'a-b' 串: True bad=[]; est_hours 残留=[]; meta.estimated_hours='94-153'
  逐任务求和 lo-hi = 94-153
  deps: 悬空=[] 自依赖=[] 环=[]
  后向边 (依赖编号更大者) = [('TASK-017', 'TASK-022'), ('TASK-017', 'TASK-025'), ('TASK-018', 'TASK-025'), ('TASK-019', 'TASK-026'), ('TASK-020', 'TASK-030'), ('TASK-021', 'TASK-028'), ('TASK-021', 'TASK-030'), ('TASK-022', 'TASK-027'), ('TASK-023', 'TASK-029')]
  RED 任务=['TASK-004', 'TASK-005', 'TASK-007', 'TASK-008', 'TASK-009', 'TASK-010', 'TASK-025', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']
  RED 传递依赖 GREEN (实现/文本) = none
  agents=['backend-architect', 'knowledge-manager', 'qa-engineer', 'tech-lead']; agent_allocation keys=None
```

> 注: sibling 「RED 传递依赖 GREEN = TASK-014 → 010~013」为启发式误捕 (TASK-014 title 含「测试」但 task_group=G3, 是 GREEN 收口任务); 三份 agent 集合与 `agent_roster` 列表相等 ([3] 末段)。

### [2] R1 finding 闭合细节 — Group 6 / Group 5 deps 与 verification[0] · TASK-038 deliverables · linked TASK-020 reason · seam_rules 字段类型

脚本 `chk2_closure.py`:

```python
import yaml, re, os, json
ROOT="/home/dev/Aria/openspec/changes/"
A=yaml.safe_load(open(ROOT+"a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml",encoding="utf-8"))
Sb=yaml.safe_load(open(ROOT+"sibling-spec-probe/detailed-tasks.yaml",encoding="utf-8"))
L=yaml.safe_load(open(ROOT+"linked-issue-field-availability/detailed-tasks.yaml",encoding="utf-8"))
TA={t["id"]:t for t in A["tasks"]}; TS={t["id"]:t for t in Sb["tasks"]}; TL={t["id"]:t for t in L["tasks"]}
print("== [bd55ab9c] a1 Group6 deps / Group5 deps + verification[0]")
for i in ["TASK-025","TASK-026","TASK-027","TASK-028","TASK-029","TASK-030"]:
    t=TA[i]; print(f"  {i} g={t['task_group']} deps={t['dependencies']}\n     v0={t['verification'][0][:160]!r}")
print("  --- Group 5")
for i in ["TASK-017","TASK-018","TASK-019","TASK-020","TASK-021","TASK-022","TASK-023"]:
    t=TA[i]; print(f"  {i} g={t['task_group']} deps={t['dependencies']}\n     v0={t['verification'][0][:200]!r}")
print("  TASK-025 notes:", (TA["TASK-025"].get("notes") or "")[:400])
print("  TASK-027 notes:", (TA["TASK-027"].get("notes") or "")[:300])
print("\n== a1 TASK-017 reason/notes (why dep TASK-022?)"); print("  reason:",TA["TASK-017"].get("reason")); print("  notes:",(TA["TASK-017"].get("notes") or "")[:500])
print("\n== sibling TASK-014"); t=TS["TASK-014"]; print(json.dumps({k:t[k] for k in ("title","dependencies","deliverables","reason","task_group")},ensure_ascii=False,indent=1))
print("\n== a1 top-level keys:", list(A.keys()), "metadata keys:", list(A["metadata"].keys()))
print("\n== [518a7d7f] a1 TASK-038 deliverables:"); [print("   ",d) for d in TA["TASK-038"]["deliverables"]]
print("   verification:"); [print("    -",v[:220]) for v in TA["TASK-038"]["verification"]]
print("\n== linked TASK-020 reason:", TL["TASK-020"].get("reason"))
print("\n== seam_rules / ab_suite_seam_rules / exports_for_siblings")
for name,doc in (("linked",L),("sibling",Sb),("a1",A)):
    m=doc["metadata"]
    for k in ("seam_rules","ab_suite_seam_rules","exports_for_siblings","phase_b_preconditions","phase_b1_preconditions","ship_target","estimation_note","a2_discretions"):
        if k in m: print(f"  {name}.metadata.{k}: type={type(m[k]).__name__} len={len(m[k]) if hasattr(m[k],'__len__') else '-'}")
    if "exports_for_siblings" in m and isinstance(m["exports_for_siblings"],dict):
        print("    exports_for_siblings keys:", list(m["exports_for_siblings"].keys()))
        sr=m["exports_for_siblings"].get("seam_rules"); print("    seam_rules type:", type(sr).__name__, "n=", len(sr) if sr else None)
```

输出 (逐字; 带圈数字已按 owner 可读性偏好改为 (n)):

```
== [bd55ab9c] a1 Group6 deps / Group5 deps + verification[0]
  TASK-025 g=6 deps=['TASK-001', 'TASK-003']
     v0='SC-22 (1) `assertRegex(text_outside_fences, r"(?m)^#{2,4}[ \\t]+前置: REQUIRE claim\\b[^\\n]*A\\.1")` — 先按 ``` 切段只在围栏外跑; 切片 = 该标题行至下一个 `^#{1,4}[ \\t]` 行 (围栏内 # 不算边界)'
  TASK-026 g=6 deps=['TASK-003', 'TASK-025']
     v0="SC-34: phase-b-developer/SKILL.md / branch-manager/SKILL.md / phase-d-closer/SKILL.md 各 `count('A.1 认领时派生的那一串') >= 1`, 三条独立断言 (失败信息点名文件); 在 d69091d 上先跑出红并留痕, 转绿"
  TASK-027 g=6 deps=['TASK-003', 'TASK-026']
     v0="DEFAULTS.json `state_scanner.coordination` 恰含 {enabled, mode, unattended} 三键 (集合相等, 不多不少); 值 {True, 'advisory', False}"
  TASK-028 g=6 deps=['TASK-003', 'TASK-027']
     v0="`'update_heartbeat' not in text` 且 `'heartbeat(' in text` (两条独立断言)"
  TASK-029 g=6 deps=['TASK-003', 'TASK-028']
     v0="切片 = 从 `### 3.2 Reader downgrade on unknown version` (:129) 至 `### 3.3` 止; `'unknown_schema_claims' in slice`"
  TASK-030 g=6 deps=['TASK-003', 'TASK-029']
     v0='layer-l-integration.md: 存在标题行匹配 `^#{2,4}[ \\t]+Layer L A.1 heartbeat 集成`; 该节切片 (至下一 `^#{1,4}[ \\t]`) 含 `--heartbeat-only`; 负控 = 标题在、命令行写在别节 ⇒ 红'
  --- Group 5
  TASK-017 g=5 deps=['TASK-002', 'TASK-003', 'TASK-014', 'TASK-016', 'TASK-022', 'TASK-025']
     v0='本任务落文本后, 对应 TASK-025 (SC-22 (1)–(7), phase-a-planner 臂) 由红转绿 (基线 d69091d 上先红, 见该任务); 切片内无字面 `--phase B` ((4))'
  TASK-018 g=5 deps=['TASK-002', 'TASK-014', 'TASK-025']
     v0='本任务落文本后, 对应 TASK-025 (SC-22, spec-drafter 臂) 由红转绿 (基线 d69091d 上先红, 见该任务); 两文件逐一断言不拼接'
  TASK-019 g=5 deps=['TASK-003', 'TASK-026']
     v0='本任务落文本后, 对应 TASK-026 (SC-34) 由红转绿 (基线 d69091d 上先红, 见该任务): 三文件各 ≥1 逐字 `A.1 认领时派生的那一串`'
  TASK-020 g=5 deps=['TASK-016', 'TASK-030']
     v0='本任务落文本后, 对应 TASK-030 (:168 切片含 push_skipped 臂) 由红转绿 (基线 d69091d 上先红, 见该任务); TASK-033 eval-13 两臂可辨'
  TASK-021 g=5 deps=['TASK-016', 'TASK-020', 'TASK-028', 'TASK-030']
     v0='本任务落文本后, 对应 TASK-028 (无 `update_heartbeat` 且含 `heartbeat(`) 与 TASK-030 (含标题 `Layer L A.1 heartbeat 集成` 且切片含 `--heartbeat-only`) 由红转绿 (基线 d69091d 上先红, 见各该任务)'
  TASK-022 g=5 deps=['TASK-003', 'TASK-027']
     v0='本任务落文本后, 对应 TASK-027 (三键与 SKILL.md 登记值逐字一致; 负控红) 由红转绿 (基线 d69091d 上先红: coordination 段今天不存在, 见该任务)'
  TASK-023 g=5 deps=['TASK-014', 'TASK-029']
     v0='本任务落文本后, 对应 TASK-029 (§3.2 切片含字面 `unknown_schema_claims`; 负控写进 §4.2 ⇒ 红) 由红转绿 (基线 d69091d 上先红, 见该任务)'
  TASK-025 notes: 落 D17 (1)(2)(3) (Spec SC-22 头部)。RED-first (R1 C1 后在依赖图上可执行: 本任务是 TASK-017/018 的上游): 断言先于 TASK-017/018 落文本, 在 d69091d 上跑一次全红并留痕 (红痕进 B.2 handoff); TASK-017/018 落文本后 转绿由它们各自的 verification[0] 断言。

  TASK-027 notes: 旧 substitute SC-9 无效 (对象是散文); 本条是「真的可机械断言且现在就是红的」测试 (memory check-runs-at-baseline-first)。

== a1 TASK-017 reason/notes (why dep TASK-022?)
  reason: 主落点; 七字面量 + 完整命令行 + 幂等谓词 + 四档选项集 + 退出义务 + 三条 skip 分支, 且须同时满足 SC-22 (1)–(7) 的机械形态
  notes: 委派动作行 (:763-766 待办 (2)): A.1 项 :63 `A.1 - Spec 管理:` / :64 `skill: spec-drafter` / :65-67 skip_if (Level1 :67) / :68-70 action / :71-73 output。precondition 键放 :63 之后首位。文件内 ```yaml 围栏实为 8 处 (Spec 写 7), (5) 靠 `A.1 - Spec 管理:` 锚点定位。SC-26 的 handoff 宿主未定义 (tasks.md 待 owner 裁 #5), 本任务先写「待复议记录 + awaiting_owner」措辞, 落点按 owner 裁定回填。


== sibling TASK-014
{
 "title": "GREEN + 回归: 全套测试通过 / run_all_tests.sh 自动纳入 / 三个坏实现负控亲跑 / state-scanner 零改动断言",
 "dependencies": [
  "TASK-009",
  "TASK-011",
  "TASK-012",
  "TASK-013"
 ],
 "deliverables": [
  "aria/skills/audit-engine/scripts/sibling_spec_probe.py",
  "aria/skills/audit-engine/tests/test_sibling_spec_probe.py"
 ],
 "reason": "实现收口: 让 2.1–2.5 全绿并证明断言对坏实现有拒绝能力 (memory adversarial-fixture / test-claims-vs-verifies)",
 "task_group": "G3"
}

== a1 top-level keys: ['metadata', 'tasks'] metadata keys: ['feature', 'title', 'level', 'datasource', 'spec', 'scope_repo', 'scope_repo_head', 'scope_repo_version', 'spec_line_baseline', 'secondary_repo', 'decision_source', 'audit_source', 'created', 'updated', 'total_tasks', 'task_groups', 'estimated_hours', 'status', 'new_agents_required', 'agent_roster', 'estimation_note', 'ship_order', 'ship_order_note', 'external_dependencies', 'phase_b_preconditions', 'rule6_note', 'not_tasked']

== [518a7d7f] a1 TASK-038 deliverables:
    aria
    VERSION
    README.md
    CLAUDE.md
    README.zh.md
    README.ja.md
    README.ko.md
   verification:
    - gitlink: `git ls-files -s aria` 的 SHA = aria post-merge master SHA, 且该 SHA 在 `git -C aria ls-remote origin master` 与 `github master` 上均可取到 (orphaned gitlink 守卫, Aria #165); `git submodule status` 无 `+`/`-` 前缀
    - 主仓 14 处版本点全部改为 ship 号 (与上次发布 commit 086ee32 同口径: CLAUDE.md ×2 / VERSION ×1 / README.md ×2 / i18n ×3 各 translated-from + badge + Plugin Version = 9): `grep -rn '1\.67\.2' CLAUDE.md VERSION README.md README.zh.md README.ja
    - i18n B 档 (#140): 正文无实质变更 ⇒ **不重译**, 但 `<!-- translated-from: vX.Y.Z -->` 标记与 badge / Plugin Version 两处版本串**必须同批改** —— check `i18n-readme-translation-currency` 读的是标记 (`.aria/state-checks.yaml:161-173`), 不是「有无正文变更」
    - 机械兜底: 在上述**全部**文件改完后才断言 custom checks `m6-version-badge-match` / `i18n-readme-translation-currency` 绿 (跑 `/state-scanner` Phase 1.11 或 scan.py 读 custom_checks 段); 改完前两条必红是预期 (R1/A1 实跑: 只 bump plugin.json ⇒ STALE ×3 + DRI
    - 不带路径的 `git status` 干净 (memory scoped-add-splits-claim)

== linked TASK-020 reason: 全量回归 + 零改动断言 (AGENT_MAPPING: **/tests/**/*.py → qa-engineer; R1/A4 df090b25 补)

== seam_rules / ab_suite_seam_rules / exports_for_siblings
  linked.metadata.exports_for_siblings: type=dict len=8
  linked.metadata.ship_target: type=str len=145
  linked.metadata.estimation_note: type=str len=271
    exports_for_siblings keys: ['module_path', 'import_form', 'functions', 'dataclass_FieldVerdict', 'constants', 'cli', 'json_keys', 'seam_rules']
    seam_rules type: list n= 2
  sibling.metadata.ab_suite_seam_rules: type=list len=2
  sibling.metadata.exports_for_siblings: type=dict len=9
  sibling.metadata.phase_b1_preconditions: type=list len=2
  sibling.metadata.estimation_note: type=str len=294
  sibling.metadata.a2_discretions: type=list len=9
    exports_for_siblings keys: ['consumer', 'cli', 'stdout_keys', 'verdict_enum', 'status_enum', 'reason_enum', 'own_layer_enum', 'exit_codes', 'consumer_obligation']
    seam_rules type: NoneType n= None
  a1.metadata.phase_b_preconditions: type=list len=6
  a1.metadata.estimation_note: type=str len=195
```

### [3] 检查 4/5/8 — 覆盖表 (SC, TASK) 对 → verification 层 / 整块层 token (含 `SC-a~b` · `SC-a/b/c` · `TASK-013/014` 展开) · 反向 (yaml 有 / 表无) · deliverables 实存性 vs (新建) · agent_roster

脚本 `chk3_cov_deliv.py`:

```python
#!/usr/bin/env python3
"""R2/A4 检查 3: (i) tasks.md SC→TASK 覆盖表 vs yaml token (verification-only 与 block-wide, 含 SC-a~b / SC-a/b/c 与 TASK-013/014 缩写展开)
(ii) deliverables 实存性 vs (新建) 标记 (iii) Impact 表路径 ⊆ deliverables ∪ 零改动行 (iv) agent_roster/agent_allocation vs agent 字段."""
import re, os, yaml, itertools
ROOT="/home/dev/Aria/openspec/changes/"; REPO="/home/dev/Aria/"
SPECS=["linked-issue-field-availability","sibling-spec-probe","a1-entry-claim-duplicate-work-guard"]
def expand_tasks(cell, p2id):
    ids=set()
    for m in re.finditer(r"TASK-(\d{3})((?:/\d{3})+)?", cell):
        ids.add("TASK-"+m.group(1))
        if m.group(2):
            for n in m.group(2).strip("/").split("/"): ids.add("TASK-"+n)
    for p in re.findall(r"(?<![\d.])(\d+\.\d+)(?![\d.])", cell):
        if p in p2id: ids.add(p2id[p])
    return ids
def expand_sc(cell):
    scs=set()
    for lo,hi in re.findall(r"SC-(\d+)~(\d+)", cell): scs|={f"SC-{n}" for n in range(int(lo),int(hi)+1)}
    for m in re.finditer(r"SC-(\d+)((?:/\d+)+)", cell):
        scs.add("SC-"+m.group(1)); scs|={"SC-"+n for n in m.group(2).strip("/").split("/")}
    scs|=set(re.findall(r"SC-\d+[a-z]?", cell))
    return scs
def has_sc(text, sc):
    n=int(re.match(r"SC-(\d+)",sc).group(1)); suf=sc[len(f"SC-{n}"):]
    if suf: return sc in text
    if re.search(rf"SC-{n}(?![\d])", text): return True
    for lo,hi in re.findall(r"SC-(\d+)~(\d+)", text):
        if int(lo)<=n<=int(hi): return True
    return bool(re.search(rf"SC-\d+(?:/\d+)*/{n}(?!\d)", text))
for s in SPECS:
    print(f"\n===== {s}")
    raw=open(ROOT+s+"/detailed-tasks.yaml",encoding="utf-8").read(); doc=yaml.safe_load(raw); T={t["id"]:t for t in doc["tasks"]}
    md=open(ROOT+s+"/tasks.md",encoding="utf-8").read()
    p2id={t["parent"]:i for i,t in T.items()}
    sec=md.split("## SC → TASK 覆盖表")[1].split("\n## ")[0]
    rows=[r for r in sec.splitlines() if r.startswith("| SC-")]
    pairs=[]; 
    for r in rows:
        cells=[c.strip() for c in r.strip().strip("|").split("|")]
        scs=expand_sc(cells[0])
        if "撤销" in r or "迁出" in r: 
            # 只在有 TASK 落点时计
            pass
        ids=set()
        for c in cells[1:]:
            if s=="a1-entry-claim-duplicate-work-guard":
                if cells.index(c)!=3: continue
            else:
                if cells.index(c) not in (2,3): continue
            ids|=expand_tasks(c,p2id)
        for sc in sorted(scs, key=lambda x:(int(re.search(r"\d+",x).group()),x)):
            for i in sorted(ids): pairs.append((sc,i))
    ver_bad=[]; blk_bad=[]
    for sc,i in pairs:
        t=T[i]; ver="\n".join(t.get("verification") or [])
        blk=" ".join([t["title"],ver,*(str(d) for d in (t.get("deliverables") or [])),t.get("notes","") or ""])
        # deliverables 注释在 safe_load 已丢, 用原文块
        m=re.search(rf"  - id: {i}\n(.*?)(?=\n  - id: TASK-|\Z)", raw, re.S); rawblk=m.group(1) if m else ""
        if not has_sc(ver,sc): ver_bad.append((sc,i))
        if not (has_sc(blk,sc) or has_sc(rawblk,sc)): blk_bad.append((sc,i))
    print(f"  覆盖表行={len(rows)} (SC,TASK) 对={len(pairs)}")
    print(f"  verification 无 token: {len(ver_bad)} {ver_bad}")
    print(f"  整块 (title/verification/deliverables 注释/notes) 无 token: {len(blk_bad)} {blk_bad}")
    # 反向: yaml verification 出现的 SC 是否都在表里 (表遗漏)
    tbl_sc={sc for sc,_ in pairs}|{sc for r in rows for sc in expand_sc(r.split("|")[1])}
    yaml_sc=set()
    for t in T.values():
        v="\n".join(t.get("verification") or [])
        yaml_sc|=set(re.findall(r"SC-\d+(?![\d])", v))
        for lo,hi in re.findall(r"SC-(\d+)~(\d+)", v): yaml_sc|={f"SC-{n}" for n in range(int(lo),int(hi)+1)}
    print(f"  yaml verification 出现但表无行: {sorted(yaml_sc-tbl_sc, key=lambda x:int(x[3:]))}")
    # (ii) deliverables 实存性
    deliv=[]; cur=None; ind=False
    for line in raw.splitlines():
        m=re.match(r"^  - id: (TASK-\d{3})",line)
        if m: cur=m.group(1); ind=False; continue
        if cur and re.match(r"^    deliverables:",line): ind=True; continue
        if cur and ind:
            if re.match(r"^    \w",line): ind=False; continue
            m=re.match(r"^      - (\S+)\s*(#.*)?$",line)
            if m: deliv.append((cur,m.group(1),m.group(2) or ""))
    print(f"  deliverables 行={len(deliv)}")
    for tid,p,c in deliv:
        if "<" in p: 
            print(f"    占位路径 {tid} {p}"); continue
        ex=os.path.exists(REPO+p); new=("新建" in c) or ("(新建)" in p)
        if new and ex: print(f"    ⚠ 标新建但已存在: {tid} {p}")
        if not new and not ex: print(f"    ⚠ 未标新建但不存在: {tid} {p} | {c[:80]}")
    # (iv) agent roster
    ag={}
    for i,t in T.items(): ag.setdefault(t["agent"],[]).append(i)
    ros=doc["metadata"].get("agent_roster") or doc.get("agent_allocation") or doc["metadata"].get("agent_allocation")
    print(f"  agent 字段分布={{k:len(v) for k,v in ag.items()}}")
    if isinstance(ros,dict):
        for k,v in ros.items():
            lst=v.get("tasks") if isinstance(v,dict) else v
            if isinstance(lst,list):
                exp=sorted(lst); got=sorted(ag.get(k,[]))
                print(f"    roster {k}: n={len(exp)} match={exp==got}" + ("" if exp==got else f" diff alloc-actual={sorted(set(exp)-set(got))} actual-alloc={sorted(set(got)-set(exp))}"))
            elif isinstance(v,dict): print(f"    roster {k}: keys={list(v.keys())} {str(v)[:120]}")
    else: print("    roster type:", type(ros).__name__, str(ros)[:300])
```

输出 (逐字):

```

===== linked-issue-field-availability
  覆盖表行=10 (SC,TASK) 对=28
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: ['SC-19']
  deliverables 行=36
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['qa-engineer', 'backend-architect', 'knowledge-manager', 'tech-lead']

===== sibling-spec-probe
  覆盖表行=21 (SC,TASK) 对=46
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=41
    ⚠ 未标新建但不存在: TASK-001 aria/skills/state-scanner/lib/linked_issue_field.py | # 由姊妹 Spec 交付; 本 Spec 只核验, 零改动 (今天不存在)
    ⚠ 未标新建但不存在: TASK-005 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 夹具以字符串字面量内嵌 (逐字原文)
    ⚠ 未标新建但不存在: TASK-006 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 三臂对照 + 第四臂合成夹具
    ⚠ 未标新建但不存在: TASK-007 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # runner 体例仿 phase-d-closer/tests/test_fetch_gate.py:22 `_runner(seq)`: run(args
    ⚠ 未标新建但不存在: TASK-008 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # subprocess.run([sys.executable, <script>, ...]) 体例仿 state-scanner/tests/test_c
    ⚠ 未标新建但不存在: TASK-009 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | # 读同 skill 的 SKILL.md 与 references/execution-modes.md (Path(__file__).parents[1]
    ⚠ 未标新建但不存在: TASK-011 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # 纯分类函数 + 键构造 + 求交
    ⚠ 未标新建但不存在: TASK-012 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # remote/default-branch/fetch 段
    ⚠ 未标新建但不存在: TASK-013 aria/skills/audit-engine/scripts/sibling_spec_probe.py | # corpus 段
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/scripts/sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-014 aria/skills/audit-engine/tests/test_sibling_spec_probe.py | 
    ⚠ 未标新建但不存在: TASK-017 aria-plugin-benchmarks/ab-suite/audit-engine.json | # 若三臂语义分档显示断言措辞过宽 ⇒ 拆条不删 (手册 :142-159), 并 version.yaml 再升
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['tech-lead', 'qa-engineer', 'backend-architect', 'knowledge-manager']

===== a1-entry-claim-duplicate-work-guard
  覆盖表行=33 (SC,TASK) 对=55
  verification 无 token: 0 []
  整块 (title/verification/deliverables 注释/notes) 无 token: 0 []
  yaml verification 出现但表无行: []
  deliverables 行=85
    ⚠ 标新建但已存在: TASK-001 docs/handoff/
    ⚠ 未标新建但不存在: TASK-006 aria/skills/state-scanner/tests/test_heartbeat_by_track.py | # 同文件加 TestRenameTwoStep 类 (改名是 claim_lifecycle 语义, 与 heartbeat 同宿主); 串行于 TASK-0
    ⚠ 未标新建但不存在: TASK-008 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加四个测试类; 串行于 TASK-007 之后
    ⚠ 未标新建但不存在: TASK-009 aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py | # 同文件加 TestA1CarryIdRoundTrip; 串行于 TASK-008 之后
    占位路径 TASK-031 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-a-planner/
    占位路径 TASK-032 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/spec-drafter/
    占位路径 TASK-033 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/state-scanner/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-b-developer/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/branch-manager/
    占位路径 TASK-034 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/phase-d-closer/
    占位路径 TASK-035 aria-plugin-benchmarks/ab-results/<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/targeted/
  agent 字段分布={k:len(v) for k,v in ag.items()}
    roster type: list ['backend-architect', 'qa-engineer', 'knowledge-manager', 'tech-lead']
```

### [4] fix 引入的新表面 — 42 条清账表声称的边 vs yaml 实况 · sibling execution_order / phase_b1_preconditions 全文 · 残留字面 grep · vNEXT 出现处

```
== 声称边 (linked 7 / sibling 17 / a1 18 = 42) 逐条 in T[a]["dependencies"]:  yaml 缺失: none
   sibling TASK-002 deps: []   TASK-003 deps: ['TASK-002']   TASK-004 deps: ['TASK-001', 'TASK-002', 'TASK-003']
== sibling execution_order (逐字):
   [并行, 不同文件] TASK-001 (硬前置断言, 阻塞门) · TASK-002 (基线三态, 只读观测) · TASK-003 (AB 套件文件, B.1 前置)
   TASK-004 (测试骨架 + SC-21)  ← 001, 002
   [串行 (同文件 tests/test_sibling_spec_probe.py), RED] TASK-005 ← 001, 004 → TASK-006 ← 001, 005 → TASK-007 ← 001, 006 → TASK-008 ← 001, 007 → TASK-009 ← 001, 008
   TASK-010 (探针骨架)  ← 004, 008
   [串行 (同文件 scripts/sibling_spec_probe.py)] TASK-011 (谓词)  ← 010, 005, 006 → TASK-012 (远端)  ← 011, 010, 007
   TASK-013 (语料 + cap)  ← 012, 007
   TASK-014 (GREEN + 负控)  ← 009, 011, 012, 013
   TASK-015 (execution-modes.md)  ← 003, 009
   TASK-016 (SKILL.md + report-format.md)  ← 003, 009, 015
   TASK-017 (AB 双臂实跑)  ← 003, 014, 015, 016
   TASK-018 (发布同步, 档位与号待 owner; 未裁 ⇒ 不开工)  ← 017
== sibling metadata.phase_b1_preconditions[1] (逐字):
   TASK-003 done: aria-plugin-benchmarks/ab-suite/audit-engine.json 存在, 含 α/β 两 eval (proposal :473 逐字「该任务未 done 则 Phase B.1 不得开始」; 建不成 ⇒ 上呈 owner, 不自判豁免)。上游边: TASK-015 / 016 (指令面接线) 与 TASK-017 (AB 实跑) 的 dependencies 各含 TASK-003 (R1 C1 第 3 条, 主控裁量落第 4/5 组)
== sibling tasks.md :157 主控追记 (逐字节选): 「(1) proposal :473 … TASK-003 追加为 TASK-004 (第 2 组起点) 的依赖 … (2) … 追加 TASK-003 ← TASK-002 边。均为一行 dependencies 改动」
== sibling tasks.md :275 已知限 (逐字节选): 「… 第 1 组「并行」在此语义上有时序依赖, 已上报主控 (未自行加边)。」

== 残留 grep (六份; 逐字命中行):
   1\.68\.0     : sibling tasks.md:121 (统一句「不预写 v1.68.0…」) · linked tasks.md:7/:177/:178 (清账留痕) · a1 tasks.md:195/:248 (留痕)  —— 两份 yaml 零命中
   1\.67\.3     : sibling tasks.md:121 · linked tasks.md:7/:177 (留痕)  —— yaml 零命中
   README\.zh-CN: a1 tasks.md:246/:247/:450 (留痕) · a1 yaml:977 TASK-038 notes「R1 C2: …」(留痕)  —— deliverables 零命中
   est_hours:   : linked tasks.md:179 · sibling tasks.md:151 (留痕)  —— yaml 零命中
   parallelizable: linked tasks.md:171/:192/:230/:234/:242 (留痕 + 脚本正文)  —— yaml 零命中
   \.gitmodules : sibling yaml:557 / a1 yaml:964 / a1 tasks.md:90 (均为「非 .gitmodules」澄清) · a1 tasks.md:246/:450 (留痕)
   blocked      : sibling yaml:124/:131 (TASK-001 硬前置, 合法态) · 其余为「不用 blocked」统一句
== vNEXT 出现处: linked tasks.md 4 / yaml 5; sibling tasks.md 3 / yaml 5; a1 tasks.md 5 / yaml 10 (TASK-031~035 七条 ab-results 占位路径 `<YYYY-MM-DD>-<vNEXT>-a1-entry-rule6/<suite>/`, TASK-037 title/CHANGELOG/grep 断言, TASK-038 无) —— 形态一致, 无 `v1.68.0` 混用
== seam rules: linked exports_for_siblings.seam_rules n=2 {str}; sibling ab_suite_seam_rules n=2 {str}; a1 external_dependencies[0].seam_rules n=3 {str}; `max(id)+1` 约定三份 yaml 各 >=1 处逐字
```

### [5] 执笔席自贴脚本可信度 — 从各 tasks.md `## 机械核验` 段抽 ```python 块原样执行 + 坏输入 (副本在 scratchpad `bad/`, 仅改脚本内 ROOT 路径常量)

抽取: linked 90 行 / sibling 92 行 / a1 126 行; `"\\d" in text` = False / **True** / False。

**[5a] linked 原样 (cwd=/home/dev/Aria)** ⇒ 与 tasks.md :259-289 贴出输出逐字一致, `RESULT: PASS`, exit 0。坏输入 (TASK-017 deps 删 TASK-016):

```
tasks=25  同文件对=23  (a)缺边=[('TASK-016', 'TASK-017'), ('TASK-016', 'TASK-018'), ('TASK-016', 'TASK-019')]  (b)环/悬空=None
   TASK-016 -> TASK-017  ['aria-plugin-benchmarks/ab-results/', 'aria-plugin-benchmarks/ab-suite/spec-drafter.json']  edge=MISSING
   TASK-016 -> TASK-018  ['aria-plugin-benchmarks/ab-results/']  edge=MISSING
   TASK-016 -> TASK-019  ['aria-plugin-benchmarks/ab-results/']  edge=MISSING
(c)测试任务=['TASK-001', 'TASK-002', 'TASK-003', 'TASK-004', 'TASK-005', 'TASK-006']  违反=[]
(d)并行组=[['TASK-022', 'TASK-023']]  同文件并行=[]  可疑并行字样=[]
parent 1:1 与 tasks.md checkbox 对齐=True (25 parent / 25 checkbox)
覆盖表对数=28  缺 token=[]
flag 映射=12 对  缺字面=[]
RESULT: FAIL      (exit=1)
```

**[5b] sibling 原样 (脚本逐字, 对真文件)**:

```
(a) same-file pairs = 34; all with edge = True
(b) cycles = []
(c) RED=['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; RED depending on GREEN = none
(d) TASK-001 direct in deps of ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: OK
(d) TASK-003 direct in deps of ['TASK-015', 'TASK-016', 'TASK-017']: OK
(e) parallel line []: same-file pairs = none
parse_detailed_tasks: parse_ok=True n=18 reason='18 task(s) parsed'; statuses=['pending']
parent 1:1: yaml parents == tasks.md checkboxes -> False (18 vs 0); dup ids=[]; total_tasks meta=18
estimated_hours present on all = False; est_hours leftover = False
RESULT: FAIL parent mismatch ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '3.1', '3.2', '3.3', '3.4', '3.5', '4.1', '4.2', '5.1', '5.2'] vs []
(exit=1; FutureWarning: Possible nested set at position 6 — 来自 r"^- \\[[ x]\\] …")
```

tasks.md :262-272 贴出的却是 `parallel line ['TASK-001', 'TASK-002', 'TASK-003']` / `True (18 vs 18)` / `estimated_hours … True` / `RESULT: PASS` ⇒ 贴出脚本 ≠ 产生贴出输出的脚本 (finding 4a669876)。

sibling 坏输入 v2 (execution_order 第 3 行 `[串行 (同文件 …), RED]` 改回 `[并行, RED]`), **原样脚本** ⇒ `(e) parallel line []: same-file pairs = none` ×2, 其余同上 FAIL (仍因 parent/estimated_hours 而非 (e)) —— (e) 恒空。**去转义副本** (`\\`→`\`, 6 行差异, 其余逐字) 同坏输入 ⇒

```
(e) parallel line ['TASK-001', 'TASK-002', 'TASK-003']: same-file pairs = none
(e) parallel line ['TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: same-file pairs = [('TASK-005', 'TASK-006'), ('TASK-005', 'TASK-007'), ('TASK-005', 'TASK-008'), ('TASK-005', 'TASK-009'), ('TASK-006', 'TASK-007'), ('TASK-006', 'TASK-008'), ('TASK-006', 'TASK-009'), ('TASK-007', 'TASK-008'), ('TASK-007', 'TASK-009'), ('TASK-008', 'TASK-009')]
parent 1:1: yaml parents == tasks.md checkboxes -> True (18 vs 18); dup ids=[]; total_tasks meta=18
estimated_hours present on all = True; est_hours leftover = False
RESULT: FAIL (e) [10 对]      (exit=1)
```

去转义副本对**原样输入** ⇒ 与 tasks.md 贴出输出逐字一致 `RESULT: PASS` (exit 0); 对坏输入 v1 (TASK-005 deps 删 TASK-001) ⇒ `(d) TASK-001 direct in deps of […]: MISSING ['TASK-005']` / `RESULT: FAIL (d) TASK-001 missing in ['TASK-005']` (exit 1)。⇒ 去转义后脚本可信, 贴出物不可信。

**[5c] a1 原样 (脚本逐字, 对真文件)** ⇒ `[b]`–`[e]`、`[+]` 与 tasks.md :429-447 贴出输出逐字一致, `RESULT: PASS` exit 0; 但 `[a]` 行与其清单不同:

```
[a] 同文件写入对 37 对 (共写文件 19 个) — 全部有边: True        <- 贴出为 40 对
      aria/skills/state-scanner/scripts/phase1_gate.py: TASK-014 -> TASK-015 -> TASK-016     <- 贴出为 TASK-003 -> TASK-014 -> TASK-015 -> TASK-016
      (其余 18 行与贴出一致, 略)
```

原因 (yaml TASK-003 deliverables raw): `- aria/skills/state-scanner/scripts/phase1_gate.py   # 只读核验: 7a :537-538 / …` 与 `release_gate.py  # 只读核验: …` —— 「只读」注释在脚本跑后补入, 脚本按规则把 TASK-003 从写入方剔除 (4 写入方 6 对 → 3 写入方 3 对 = 40-3 = 37)。TASK-003 deliverables 19 行 / 含「只读」2 行 (tasks.md :264 写「16 条 … 未标只读」)。坏输入 (TASK-025 deps 加 TASK-017):

```
[a] 同文件写入对 37 对 (共写文件 19 个) — 全部有边: True
[b] 无环: False; 悬空: []
[c] Group 6 = ['TASK-025', …, 'TASK-030']; 无一 (传递) 依赖 Group 5: False; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: False
[c'] 不经传递到达 TASK-001 的任务 (豁免 […]): []; 不到达 TASK-003: []
[d] 覆盖表 (SC, TASK) 对 51; verification 无 token 的对: []
[e] proposal SC 集合 1..34 共 34; 排除 [1, 4, 13, 16, 17, 18, 19, 20, 27, 30, 31]; 现行 23 条无命中: []
RESULT: FAIL
    (b) 环: TASK-017 -> TASK-022 -> TASK-027 -> TASK-026 -> TASK-025 -> TASK-017
    (c) Group 6 任务 TASK-025 (传递) 依赖 Group 5: ['TASK-022', 'TASK-017']   (026~030 同)      (exit=1)
```

⇒ a1 脚本拒绝能力成立; (d) 51 对 vs 本席 [3] 展开缩写后 55 对 (差 = (SC-2, 014) (SC-12, 018) (SC-22, 018) (SC-29, 014), 当前均命中)。

### [6] fix 引入的新锚点实读 (sed -n 逐行) + flag 字面

```
VERSION:24        | aria (插件) | v1.67.2 | https://github.com/10CG/aria-plugin |
CLAUDE.md:139     aria-plugin 方法论轨: v1.52.0–v1.67.2 已 ship — …
CLAUDE.md:141     版本: 插件 aria-plugin v1.67.2 | 主项目 v1.7.5 | …
README.md:8       [![Plugin Version](https://img.shields.io/badge/Plugin-v1.67.2-blue)](…)
README.md:242     Plugin Version:   1.67.2 (aria-plugin, 42 Skills + 11 Agents)
README.{zh,ja,ko}.md:3/:10/:244   <!-- translated-from: v1.67.2 --> / badge v1.67.2 / Plugin Version: 1.67.2   (三份各三行全部命中)
086ee32 --stat    CLAUDE.md README.ja.md README.ko.md README.md README.zh.md VERSION aria  (7 files; 与 TASK-038 deliverables 集合相等)
.aria/state-checks.yaml:141  - name: "i18n-readme-translation-currency"; :161  m = re.search(r"translated-from:\s*v?(\d+\.\d+\.\d+)", text)  (TASK-038「:161-173 读的是标记」成立); :88 m6-version-badge-match
linked proposal:278   > ⇒ **A.2 的一条显式约束**: `audit-engine` 内**不得**新建名为 `lib/` 或 `collectors/` 的顶层目录 …   (C4 逐字来源)
linked proposal:616 / sibling :578 / a1 :798   三份尾句均已改为「R6 已跑 … owner 2026-08-30 已批准进 A.2/A.3」(C11)
sibling proposal:473  > **谁在什么时点检查这个条件 (主控 2026-08-25 补 …)**   (追记 (1) 引用点)
a1 proposal:511 「实数 12 hunk / 9 文件」 · :513 表头 · :525 第 11 行 · :683 「rule6_note 11-hunk 表」 · :754 「重算为 11 hunk / 9 文件」  (tasks.md 出入 #3 所述 12 vs 11 不一致属实, 留 owner)
phase1_gate.py:1154   #   args  : --raw-track-id --phase [--mode advisory|block] [--linked-issue]
branch-manager/SKILL.md:149   `phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory` (命令模板见
task-planner/DUAL_LAYER_SPEC.md:166   | `estimated_hours` | (必填) | string | 工时范围 (如 "2-4") |
AB_TEST_OPERATIONS.md:142   ### Expectations 编写原则   (sibling TASK-017「手册 :142-159 拆条不删」区间起点)

flag 字面 (a1 yaml 任务块 raw, 含 deliverables 注释):
  TASK-018: --raw-track-id=Y  --phase A.1=Y  --mode advisory=Y  --linked-issue=Y  --repo-path=Y
  TASK-019: --status abandoned=Y  --sweep-stale=Y  --gc=Y
  TASK-001: --no-push=Y (title + deliverable 注释 5 行)  ARIA_COORDINATION_NO_PUSH=N
  TASK-031: --no-push=N  ARIA_COORDINATION_NO_PUSH=Y (「运行前置: harness 会话以 ARIA_COORDINATION_NO_PUSH=1 claude … 启动」)
  TASK-032 / 033 / 034 / 035: --no-push=N  ARIA_COORDINATION_NO_PUSH=N
  tasks.md :133 映射行: `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035)
```

### [7] 杂项 (逐字)

```
sibling TASK-010 verification[1]: 「§3 唯一代码块逐字: … 紧接 §3 代码块的三条 import 逐字存在 (…) … 同块允许追加第四符号 is_sentinel … 块外零 from lib. / from collectors.」   (948363d3 处方落地)
sibling tasks.md :121 版本档统一句: 「档位 (MINOR/PATCH) 与号由 owner 裁; 三份串行 ship 各占一号 (字段 → 探针 → 母); 若 owner 裁合并一版, 由最后 ship 的母 Spec 发布任务承接, 前两份的发布任务改为 no-op 并留痕。未裁 ⇒ 5.2 不开工 (status 仍 pending, 不用 blocked); 版本字面一律 <vNEXT> 占位」  — 与 linked yaml:564 / a1 yaml:951 同句
detailed_tasks.py:28  (pending/deferred/blocked/in_progress/unknown/None) counts as residual.   — sibling TASK-001「status=blocked」合法
finding id: sha256("documentation:openspec/changes/sibling-spec-probe/tasks.md:major:issue")[:8] = 4a669876
            sha256("implementation:openspec/changes/sibling-spec-probe/detailed-tasks.yaml:major:issue")[:8] = ea33f282
            sha256("documentation:openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md:minor:issue")[:8] = 9db42f0a
```

### [8] 审后 sha256 复核 (与 [0] 逐行一致)

```
d5b1429e030a2e8e5cffdcdab53ca408aa92e8e3d00ce2e4b63363db64281250  openspec/changes/linked-issue-field-availability/tasks.md
4a3f7e12577e596db386d87cae820a46bd2b2f39e04d2f01d7b0c1e039d15e88  openspec/changes/linked-issue-field-availability/detailed-tasks.yaml
9853d600335aa219f3fd6a2d897a946fbb998799c2e27f05d5b4550a3b19d32c  openspec/changes/sibling-spec-probe/tasks.md
09380e19711c052a87d2645d21936e2301a8b0e85764f8c1d7a7a3040fa2c1d1  openspec/changes/sibling-spec-probe/detailed-tasks.yaml
55e4f13738a390acd064eba3d28a5ed297c4cafd0fef95e176b4d2b61fe86824  openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md
270cb59adc10497628f58fe549a3e999d9d42a2dcd658d9cdeb4edfde504a159  openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml
```
