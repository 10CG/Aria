---
checkpoint: post_spec
round: 3
role: qa-engineer
verdict: REVISE
scope_ok: true
counts: 0C/5M/5m
---

# post_spec R3 — a1-entry-rework-v3-combined — qa-engineer

**逐 Spec verdict (分开给)**:

| Spec | 轮次 | verdict | counts |
|---|---|---|---|
| `a1-entry-claim-duplicate-work-guard` (母) | R3 | **REVISE** | 0C/4M/1m |
| `linked-issue-field-availability` (子) | R1 | **REVISE** | 0C/1M/2m |
| `sibling-spec-probe` (子) | R1 | **PASS_WITH_WARNINGS** | 0C/0M/2m |
| **combined** | — | **REVISE** | 0C/5M/5m |

## 审计对象与实读环境

主仓 HEAD `027a50f`；`git -C aria rev-parse HEAD` = `58a49e7`（gitlink，已知落后 `d50f9c3` 2 commits），全部行号核验一律用 `git -C aria show d50f9c3:<path> | sed -n 'N,Mp'`，未直接读工作树 aria/。

本席逐 SC 问「它怎么会红」，并对每条采用四字段 (宿主/baseline/怎么会红/恒绿恒红判定)。核验方式 = 亲自读源码 + 亲自跑命令 + 对既有测试文件做交叉比对（非转述 Spec 自述）。以下是本轮**亲手实跑**、构成本报告结论支柱的关键证据（命令均可复现）：

```
$ git -C aria show d50f9c3:skills/state-scanner/lib/collision.py | sed -n '229,291p'
# 确认 linked_issue_overlaps() 全函数体、_TERMINAL、own_track_id 自排除逻辑逐字与 Spec 引用一致

$ git -C aria show d50f9c3:skills/state-scanner/tests/test_release_by_track.py | sed -n '/test_linked_issue_written_and_overlap_surfaced/,/def test_no_linked/p'
# 该既有测试传 --raw-track-id "carry-secretguard-followup" 与 track 名 "secret-guard-hardening"
# —— 两个手写字符串，不含容器段，与 §2.1 派生规则无关 —— 见 finding F2

$ git -C aria show d50f9c3:skills/state-scanner/tests/test_release_by_track.py | sed -n '/test_sweep_stale_cross_container_fresh_untouched/,/def test_sweep_default/p'
# 该既有测试直调 sweep_stale_active(repo, now=now)，全程未调用任何 heartbeat —— 见 finding F3

$ git -C aria grep -n "heartbeat_by_track\|heartbeat-only" d50f9c3 -- 'skills/state-scanner/**'
# 零命中 —— heartbeat-by-track 机制在基线上确实完全不存在（非现有代码复用）

$ git -C aria show d50f9c3:skills/config-loader/DEFAULTS.json | python3 -c "import json,sys; print(sorted(json.load(sys.stdin)['state_scanner'].keys()))"
# ['audit_log_path','auto_execute_enabled','auto_execute_rules','confidence_threshold','issue_scan','multi_remote','sync_check','sync_freshness'] —— 无 coordination

$ grep -n "^#\+ " <(git -C aria show d50f9c3:skills/phase-a-planner/SKILL.md) <(git -C aria show d50f9c3:skills/spec-drafter/SKILL.md)
# 两文件全部标题内均无任何 A.0/A.1 认领步骤标题 —— SC-1/4/22 baseline 红成立

$ git -C aria grep -n "A\.0[^.]" d50f9c3 -- 'skills/*/SKILL.md'
# phase-a-planner:30/:369、spec-drafter 同族、progress-updater:29,254、task-planner:31
# 全部把 "A.0" 用作既有的 "state-scanner" 步骤标签 —— 见 finding F1

$ (在仓内直接跑) git remote -v / git symbolic-ref refs/remotes/{origin,github}/HEAD / git config --get remote.probe.url / git for-each-ref refs/remotes/
# origin 有 symbolic-ref(→master)，github 无(exit 128)；remote.probe.url 不存在(exit 1)但 refs/remotes/probe/master 仍在
# —— sibling-spec-probe SC-12/13/14 的"本仓当场可复现"断言逐条属实

$ find openspec -name proposal.md | wc -l  → 149（与 field-availability §Why 一致）
$ grep -rn '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l  → 39（field-availability 自称 37，见 F4）
$ grep -c '^  - name:' .aria/state-checks.yaml  → 11（field-availability 自称 10，见 F4）
$ python3 -c "import json;print(len(json.load(open('aria-plugin-benchmarks/ab-suite/spec-drafter.json'))['evals']))"  → 2（与两处引用一致）
```

## 上一轮 (R2) major 遗留判定 —— 逐条判

| R2 finding | 本轮判定 | 证据 |
|---|---|---|
| **M-16a**（SC-8/SC-10 捆绑 CLI 字段与消费层措辞） | ✅ **确认已拆** | SC-8 现仅剩「该条出现在 `linked_issue_overlap[]` 里」单一断言（措辞面移到 SC-11）；SC-10 现仅剩 `GateResult.error == "fetch_degraded"` 单一断言（消费面措辞移到 SC-25）。逐条核对 SC-11/SC-25 内容，移出项确有承接，非空头声明 |
| **M-16b**（SC-9 标「代码」实为散文） | ✅ **确认已订正** | SC-9 类别列现为「行为 (定向 fixture)」，理由「无代码宿主」成立（heartbeat/A.1 调用是否发生只活在 AI 读 SKILL.md 的行为里，无任何 wrapper 脚本可断言）。SC-14 同批按 M-16 拆 (a)代码 [`release_gate.py --raw-track-id`, 已核 `:236-237` 三选一必需参数] / (b)行为 两层，划分合理 |
| **SC-13/16/17/18/19 是否真被子 Spec 承接** | ✅ **逐条确认承接，非空占位** | field-availability SC-1~SC-5 头部显式声明承接旧 SC-13 的五要素（定位/token/多值/`无`/判据分区），逐条内容比对一致；sibling-spec-probe SC-1↔旧16、SC-2↔旧17、SC-3+4↔旧18（且订正了旧18 与 D11「非0 仅探针自身失败」的自相矛盾——旧 SC-18 字面写「无远端⇒exit非0」，姊妹 Spec §7 明确勘正为「无远端=`skipped`+exit 0」）、SC-5+6↔旧19(a)(c)。旧 SC-19(b)「不得把自己的 claim 计入 overlap」**两侧独立判定不迁入探针**（探针语境用 claim/track_id 词汇错配），改由母 Spec 新 SC-29 承接——两侧各自给出理由且结论一致，是真收敛信号，非互抄。**唯一瑕疵**: 母 Spec 迁出占位行 SC-18 保留的旧文字仍写「exit 非 0」，未随姊妹的订正回填，见 finding F5（Minor，非阻塞——权威内容在姊妹 Spec，占位行本身已明确标注「已迁出」不再承担独立语义） |
| **SC-29 回归守卫是否恒真装饰** | ⚠️ **不是纯装饰，但当前 fixture 未命中本 Spec 实际引入的新风险面** | 详见 finding F4（本轮判断的重点项，见下） |

## 本轮新 findings

| id | severity | Spec | 定位 | 标题 | 证据 (实跑命令+输出) | 处方 (字符级) |
|---|---|---|---|---|---|---|
| **F1** | **Major** | 母 | §2 触发时机段 + SC-22；落点 `phase-a-planner/SKILL.md`、`spec-drafter/SKILL.md` | 新锚点 `A.0 - REQUIRE claim` 与两文件**已有的** `A.0 = state-scanner 步骤` 命名占用冲突 | `git -C aria grep -n "A\.0[^.]" d50f9c3 -- 'skills/*/SKILL.md'`：`phase-a-planner/SKILL.md:30` 「查询项目状态 → 使用 `state-scanner` (A.0)」、`:369` 流程图「state-scanner (A.0) ──▶ 状态感知」；`spec-drafter/SKILL.md` 同族用法；`progress-updater/SKILL.md:29,254`、`task-planner/SKILL.md:31` 同一约定；另有 `A.1.0 - 头脑风暴检查` 已占用相邻数字空间。SC-22 的正则 `^#{2,4}[ \t]+A\.0 - REQUIRE claim\b` 机械上仍会通过（不同标题文本），但落地后同一份 `phase-a-planner/SKILL.md` 内会**同时存在两个语义不同的「A.0」**——一个指「本 skill 运行前的上游步骤 (state-scanner)」，一个指「本 skill 内部的认领子步骤」，人类/AI 读者极易混淆；三轮审计 + 两轮 rework 均未查过这条 | 换一个不落在既有 `A.x`/`A.x.y` 数字序号命名空间的锚点字面（例如复用正文已在用的「Part A1」措辞，或采用非数字前缀如 `PRE-A.1`），SC-22 的正则同步改 |
| **F2** | **Major** | 母 | SC-2（§2.1「四个被推翻版本的红窗」表）；落点 `skills/state-scanner/tests/` | SC-2 标「代码 (CLI 全链路)」单层，但**测不出它声称要防的 R1-fix 回归** | 亲读既有测试 `test_release_by_track.py:527` `class TestPhase1GateLinkedIssueCli` 下 `:533` `test_linked_issue_written_and_overlap_surfaced`：该测试传 `--raw-track-id "carry-secretguard-followup"` 与另一容器 track 名 `"secret-guard-hardening"`——**两个手写字符串，不含 `container_uuid` 段，与 §2.1 派生公式无关**，测试今天就绿。§2.1a 自陈「拼接由 AI 在 A.1 模板里做，没有代码宿主」——真正的回归点（AI 派生时丢掉容器段）活在 authoring 层，CLI 测试只能验证「传入两个不同字符串时 overlap 能各含对方」，这件事**与容器段是否存在无关**，且今天不改一行代码即真。若实现者让 AI 派生时丢掉容器段（两容器同 issue 派生出同一 track_id），只要 SC-2 的测试作者像现有先例一样手写两个不同占位字符串来模拟"两个容器"，测试依然会通过——**本 SC 无法分辨"真派生出的两个不同 track-id"与"测试随手挑的两个不同字符串"**。这与本节开场白「SC-1~SC-4 一律分两层 (文本层+行为层)」自相矛盾——SC-2 表格行没有这个二层拆分 | 比照 SC-1/SC-4 补文本层断言：验证两处 SKILL.md 的 `--raw-track-id` 占位串字面含 `<container_uuid>` 段；CLI 层测试须改为**同 basename+number、不同 container_uuid** 的正向对照（若容器段被丢弃，两者会派生出同一串，被 `:278-279` 自排除，overlap 恒空——这才是真正会被 R1-fix 回归打破的断言） |
| **F3** | **Major** | 母 | SC-7（同上表）；落点 `skills/state-scanner/lib/gc.py` 单测宿主（既有） | SC-7 未覆盖本 Spec 新增的 heartbeat-by-track 机制，与既有测试重复 | 亲读既有测试 `test_release_by_track.py:377` `class TestSweepStaleActive` 下 `:380` `test_sweep_stale_cross_container_fresh_untouched`：构造一条 2 天陈旧 claim + 一条新鲜 claim，直调 `sweep_stale_active(repo, now=now)`，**全程未调用任何 heartbeat 函数**，断言陈旧的被 sweep、新鲜的不被——这与 SC-7 场景描述（「超 SWEEP_TTL 未刷新⇒仍被 sweep」）**逐字重复**。且 `git -C aria grep -n "heartbeat_by_track\|heartbeat-only" d50f9c3 -- 'skills/state-scanner/**'` 零命中，确认新机制今天确实不存在；Impact 表也未列 `gc.py` 有任何改动。SC-7 自称要防「heartbeat 变成永不过期」，但没有一个分支**先调用**新 heartbeat 机制再验证 sweep 仍生效——它测的是一个跟本 Spec 无关、已被验证过的既有行为 | SC-7 改为：调用新 by-track heartbeat 刷新一条 claim 后，claim 仍在 `SWEEP_TTL` 之后被 sweep（验证 heartbeat 没有意外产生"永不过期"标记）；现有 `test_sweep_stale_cross_container_fresh_untouched` 保留作为既有回归覆盖，不重复计入 SC-7 |
| **F4** | **Major** | 母 | SC-29（「保护窗可生产验证性」表）| SC-29 是真回归守卫，但当前 fixture（own claim status=active）未命中本 Spec 实际新开的风险面 | 亲读 `collision.py:265-291`：`_TERMINAL = ("done","abandoned","unknown")` 在 `:272-273` 早退（`if c.status in _TERMINAL: continue`），随后才到 `:278-279` 的 `if c.track_id == own_track_id: continue` 自排除。`active` 从未落在 `_TERMINAL` 集合内 ⇒ **对 SC-29 指定的 active-fixture，本 Spec 的 diff（`include_terminal` 新增 + `_TERMINAL` 早退改为可绕过）根本不触碰这条代码路径的可达性**——self-exclusion 检查在改动前后走的是完全相同的代码。Spec 自己给的负控例子「删掉 :278-279 两行」是与本 Spec 实际 diff 无关的人为构造，不是本 Spec 改动会自然引导出的错误。**本 Spec 真正新开的风险面**是：`include_terminal=True` 首次让 `_TERMINAL`（含 own claim 处于 `done`/`abandoned`）状态的 claim 流到 self-exclusion 检查——若实现者为该分支写一条并行/复制的早退逻辑（bool 旁路的常见写法）而漏抄 self-exclusion 这一行，own-claim-terminal 场景会把自己算进 overlap，而 SC-29 现在的 fixture 测不到这个场景 | A.2 给 SC-29 补第二臂：own claim status ∈ {done, abandoned} + `include_terminal=True` ⇒ 该 claim 仍不得出现在 overlap 中。原 active-fixture 保留（仍能抓住"整个 continue 块被误删"类粗粒度回归），两臂并存 |
| **F5** | Minor | 母 | SC-18 迁出占位行 | 占位行文字未同步姊妹 Spec 的订正 | 母 Spec 现文 `⛔ 已迁至 sibling-spec-probe (探针 fetch 失败 ⇒ degraded + exit 非 0)`；但 sibling-spec-probe §7 明确「勘正母 Spec 旧 SC-18」——按 D11，fetch 失败 = degraded **+ exit 0**（非「exit 非0」），已拆入其 SC-3/SC-4。单独读母 Spec 占位行会得到与最终裁决相反的 exit code 语义 | 占位行文字加一句「(exit code 语义已被姊妹 Spec §7 订正为 exit 0，非本行原字面)」，或直接删去残留的旧措辞只留迁出指针 |
| **F6** | **Major** | field-availability | Impact 表整体；影响 SC-1~SC-6/SC-8（8 条 SC 里 6 条标「代码」类） | 全部「代码」类 SC 没有声明的测试宿主 | `grep -n "宿主\|tests/\|test_.*\.py"` 全文命中的 9 处「宿主」全部指探针**脚本自己**该落哪个目录（D3 的形态 ii/iii 之争），无一处提及 SC-1~6/SC-8 的**测试文件**该落哪。对照：母 Spec Impact 表显式一行 `skills/state-scanner/tests/ (既有宿主)`；sibling-spec-probe Impact 表显式一行 `skills/audit-engine/tests/test_sibling_spec_probe.py (新增)`。field-availability 是三份里唯一缺这一行的。`state-scanner/tests/` 目录已存在且已确认被 `run_all_tests.sh` 的 `find … -type d -name tests` 自动发现——不缺可行方案，缺的是**声明**。**本 Spec 的立项理由正是「C-A: 抽取规则 defer ⇒ check 无实现宿主」——若自己的测试也没宿主，是同一个病换了一层复发** | Impact 表补一行，如 `aria/skills/state-scanner/tests/test_linked_issue_field_probe.py`（新建，自动纳入既有发现机制），并把 SC-1~SC-8 逐条挂上去 |
| **F7** | Minor | field-availability（叙事影响延伸至 sibling-spec-probe SC-18） | §Why「当日观测值」表 + SC-1(c) | 语料自修改导致部分引用数字/行号已过期（数字漂移不影响机械逻辑） | 逐字复跑 field-availability §Why 给出的**全部**命令：`find openspec -name proposal.md`=149 ✓、松·文件=17 ✓、严·文件=17 ✓、严·行=19 ✓ 全部匹配；但**松·行**：自称 37，实测 **39**；松→严差额按文件：自称「母3/本11/探针4」，实测「母2/本11/探针7」（三项并列：总体相同=同一 commit 027a50f、范围相同=命令逐字照抄、计数法相同=同一 grep flags——三项皆同而结果不同，是**真矛盾**非不可比，根因是三份 Spec 并发编辑，sibling-spec-probe 后续增补的对照表内容比 field-availability 捕获快照时更多）。**更关键**：SC-1(c) 引用「该形状在真实语料上有实例: 母 Spec `:88`」，但当前 `sed -n '88p'` 该行是 `## What Changes`（章节标题）；`grep -rn '> >.*关联 Issue'` 全库 149 篇零命中——**当前语料里已不存在任何真实的嵌套引用实例**，该「真实语料实例」现在是悬空指针。这同一根因也影响 sibling-spec-probe SC-18 的「谓词1必要性」叙事（它引用同一处母 Spec 行）——**两处的合成夹具本身不受影响**（不依赖真实文件当前状态），仅叙事性论据过期 | SC-1(c) 与 sibling-spec-probe §3 层0 处的「真实语料实例见母 Spec :88」应删除或改为「历史观测，当前语料已无实例（合成夹具仍有效）」 |
| **F8** | Minor | field-availability | §4「既有 check 的宿主形态」表头 | check 总数从「10」变为「11」 | `grep -c '^  - name:' .aria/state-checks.yaml` 现返回 **11**；新增 `main-project-version-consistency`（`:289`，「owner 2026-08-25 核实立案」，与本 Spec 同期落地），形态属 (iii) `.aria/probes/`。不影响 D3 实质结论（plugin 侧仍是 2 个既有先例，本 Spec 仍应选形态 ii），但「6+2+2=10」枚举需改「6+2+3=11」 | 落地前重跑 `grep -c` 并更新枚举 |
| **F9** | Minor | sibling-spec-probe | SC-5（field-availability，四臂 fail-closed 表）| (a)「新违规」与(c)「白名单陈旧」两臂都 `exit 1`，靠文案区分，但文案模板未钉死 | Spec 判据分割表只给了语义描述（「点名该 path」/「文案含"allowlist 陈旧"」），未给具体字符串模板；若两臂措辞前缀雷同，机械断言可能难以稳定区分（未到 Major——"陈旧"文案按设计要求点名 path，天然与"新违规"不同结构） | A.2 落地时钉死两臂的文案模板（如固定前缀 `FAIL allowlist 陈旧:` vs `FAIL:`），SC-5 断言改为逐字匹配前缀而非仅测 exit code |
| **F10** | Minor | sibling-spec-probe | SC-13 | `fetch_gate.py:55/:124-127` 的 `_DEFAULT_BRANCH_FALLBACKS` 具体内容本轮未逐字核对 | 已确认该函数存在且 P6 决策「不复用」的方向性理由（origin 硬编码 + 名字猜测）与其余代码不矛盾，但未独立逐字读取 `:55`/`:124-127` 原文核实猜测列表的确切内容 | 不阻断；A.2 实施前建议补一次逐字核对 |

## 逐 SC 四字段表（三份合计 55 条：母 29 + field-availability 8 + sibling-spec-probe 18）

字段: 宿主 / baseline 红绿 / 它怎么会红 / 恒绿恒红判定。除 F1~F10 已展开分析的行外，其余「怎么会红」列给最小复现描述；「NORMAL」= 未发现恒真恒假风险。

### 母 Spec `a1-entry-claim-duplicate-work-guard`（宿主默认 `skills/state-scanner/tests/`；行为类=定向 AB fixture，无代码宿主）

| SC | 宿主 | baseline | 它怎么会红 | 判定 |
|---|---|---|---|---|
| SC-1 | 文本层 `test_coordination_default_lockin.py`（扩）+ 行为层 fixture | 红（两处 SKILL.md 均无 A.0/A.1 标题，已核 `grep -n "^#\+ "`） | 占位串写 `<slug>-…`（含 slug）的坏实现必红 | NORMAL |
| SC-2 | 代码 CLI 全链路（无文本层） | 红（A.1 机制不存在） | 见 **F2** | **⚠️ 恒绿风险 (F2)** |
| SC-3 | `identity.py` 新 accessor 单测（待建） | 红（accessor 不存在；`get_container_id():222` label-or-uuid 已核） | 设 label 后直调 `get_container_id()` 的实现必红 | NORMAL |
| SC-4 | 同 SC-1 | 红 | 裸 `<number>`（漏 `str(int())`）必红；措辞面对语义等价但字面不同的写法略脆（轻微，非阻塞） | NORMAL |
| SC-5 | 代码（新 by-track heartbeat 变体单测，待建） | 红（`heartbeat()` 现仅 `(container,session)` 键，已核 `:228`；`heartbeat_by_track` 零命中） | 假 by-track 实现仍按 session 匹配 | NORMAL |
| SC-6 | 同 SC-5 | 红 | 只刷新一条（`break`式实现）必红 | NORMAL |
| SC-7 | 既有 `TestSweepStaleActive` 可扩 | 绿（既有场景已覆盖；新机制未调用） | 见 **F3** | **⚠️ 恒绿风险 (F3)** |
| SC-8 | 代码 CLI 全链路 | 红（`--include-terminal` flag 不存在，argparse 会先 `SystemExit`） | 已核 `_TERMINAL` 不含 `yielded`（3 项 done/abandoned/unknown），场景列同步删除属实 | NORMAL |
| SC-9 | 无代码宿主，行为 fixture | N/A | 无条件调用臂可辨 | NORMAL（类别订正确认成立） |
| SC-10 | 代码 CLI 全链路 | 红（已核 `:1236-1238` 现状 `except→[]`，`error` 字段全文无 `fetch_degraded` 赋值） | 未赋值实现必红 | NORMAL |
| SC-11 | 行为 fixture | N/A | 四档措辞可辨；「对 done 也给释放选项」臂可辨 | NORMAL |
| SC-12 | 行为 fixture | N/A | 跳过传参臂在真实 CLI 输出的键存在性上可辨（已核 `:1230` 整块门控） | NORMAL |
| SC-13 | 迁出占位 | — | 已确认真承接（field-availability SC-1~5） | 诚实 |
| SC-14 | (a) `release_gate.py` CLI (b) 行为 fixture | (a) 红（已核 `:425/:427` container+status=="active" 匹配条件；红点=carry-id 未统一而非 flag 缺失，Spec 已自陈） | 已述 | NORMAL |
| SC-15 | 代码（release+acquire 两步，待建） | 红 | 「有无关联 issue」谓词在第三类夹具（有 issue 但落回落形）上必红；判断逻辑若落进 AI authoring 层而非代码，会有与 SC-2 同形的轻度恒绿风险——未像 SC-1/4 显式分两层，建议 A.2 留意 | NORMAL（轻微关注） |
| SC-16~19 | 迁出占位 | — | 已确认真承接（sibling SC-1/2/3+4/5+6），旧19(b)→新 SC-29，两侧独立判定一致 | 诚实（SC-18 占位文字见 **F5**） |
| SC-20 | — | ⛔撤销，已核 `constants.py:36` 仍 `STALE_TTL=1800` | N/A | NORMAL |
| SC-21 | 行为 fixture | N/A（`heartbeat()` 生产调用点=0 已核 `:43-44`） | 两臂（挂载/未挂载）可辨 | NORMAL，与 SC-28 互补 |
| SC-22 | `test_coordination_default_lockin.py`（扩） | 红（两处均无 `A.0` 标题） | 裸 `assertIn` 对「塞进 YAML 列表」免疫，本正则不免疫 | 机制 NORMAL；**目标锚点命名见 F1** |
| SC-23 | 代码 | 红（已核 `:425` 匹配机制；carry-id 未统一） | 已述 | NORMAL |
| SC-24 | 代码 | 红（`unknown_schema_claims` 键不存在） | **本席已用 Python 亲测复现整条因果链**：`parse_claim(schema_version="99", linked_issue=...)` → `linked_issue=None` → `linked_issue_overlaps(...)` → `[]`，证据最强的一条 | NORMAL |
| SC-25 | (代码) `phase1_gate.py` CLI + (行为) fixture | 红（已核 `:1236-1238` 现状） | 已述 | NORMAL |
| SC-26 | 行为 fixture | N/A（`unattended` key 确认不存在于 `DEFAULTS.json`） | 「用工具是否可用做判据」臂在扩权后恒走问的那一臂，可辨 | NORMAL |
| SC-27 | 代码 | 红（release 语义现无差别按 track 释放，未分档） | 两臂（放弃一个方向 vs 放弃整个 issue）对连坐可辨 | NORMAL |
| SC-28 | 行为 fixture | N/A | 「无视 opt-out」臂可辨 | NORMAL |
| SC-29 | 代码 | **绿**（已核 `:278-279` 当前生效） | 见 **F4** | **⚠️ 非装饰但 fixture 不足 (F4)** |

### `linked-issue-field-availability`（宿主：**见 F6，全 Spec 未声明**；下表按「若循惯例落 `state-scanner/tests/`」记）

| SC | 宿主 | baseline | 它怎么会红 | 判定 |
|---|---|---|---|---|
| SC-1 | ⚠️见 F6 | 红（探针脚本不存在，`ls` 零命中） | 四夹具设计合理；(c)(d) 合成夹具本身不受语料变化影响，但引用的「真实实例」已悬空，见 **F7** | NORMAL 机制上 |
| SC-2 | ⚠️见 F6 | 红 | **本席逐条实读全部 6 个真实归档路径**（如 `2026-06-10-handoff-frontmatter-enforcement/proposal.md:4` 等），内容与 Spec 描述逐字吻合（先 markdown 链接、后随 triage code span） | NORMAL，证据最强 |
| SC-3 | ⚠️见 F6 | 红 | **本席实跑** `normalize_linked_issue('10CG/aria-plugin#1')→('aria-plugin',1)`；`'[b](url)'→None`；`'无'→None`，与断言吻合 | NORMAL |
| SC-4 | ⚠️见 F6 | 红 | (a) 本文件自身 dogfood 字段已核；(b) `archive/2026-08-23-linked-issue-normalization/proposal.md:6` 经 `cat -A` 核实确系裸「无」无反引号 | NORMAL |
| SC-5 | ⚠️见 F6（GRANDFATHERED 机制不存在） | 红 | 四臂设计具体可测；**GRANDFATHERED 6 条路径本席逐个 `test -f` 全部确认存在**且 `grep -c 关联 Issue`=0（NO_FIELD 属实）；(a)/(c) 两臂文案区分度见 **F9** | NORMAL |
| SC-6 | ⚠️见 F6（测模板本身，非 probe） | 红（`grep -c "关联 Issue" standards/openspec/templates/proposal-minimal.md`=0，已核） | 模板加字段但写裸文本/漏 Usage Note 均可判红 | NORMAL |
| SC-7 | 明确无代码宿主，AB 定向 fixture | N/A | `spec-drafter.json` 实测 `evals`=2，与 Spec 逐字一致 | NORMAL |
| SC-8 | ⚠️见 F6 + `.aria/state-checks.yaml` 注册（均未落） | 红（`grep linked-issue-field-availability .aria/state-checks.yaml` 零命中；两个同类既有探针字节数精确匹配 7716/11115） | (b) 臂"放回 `.aria/probes/`"红设计合理，直接钉住 D3 改判 | NORMAL；总量见 **F8** |

### `sibling-spec-probe`（宿主 `aria/skills/audit-engine/tests/test_sibling_spec_probe.py`，待建；`git -C aria ls-tree d50f9c3 skills/audit-engine/` 已确认目录内目前只有 `SKILL.md`+`references/`，`scripts/`/`tests/` 均待建）

| SC | 宿主 | baseline | 它怎么会红 | 判定 |
|---|---|---|---|---|
| SC-1 (旧16) | 待建 | 红 | 6 个真实 archive 路径核对全部存在，成对指向同一 issue 号 (#95/#122/#137) | NORMAL |
| SC-2 (旧17) | 待建 | 红 | 无命中映射非 0 exit 的实现必红 | NORMAL |
| SC-3 (旧18a) | 待建 | 红 | 三个坏实现（verdict 算错/exit 映射错/hits 整体丢弃）均可信、可分辨 | NORMAL |
| SC-4 (旧18b) | 待建 | 红 | 「无远端⇒exit 非0」的旧写法在本条上必红（本席已核 D11 与本条口径一致） | NORMAL |
| SC-5 (旧19a) | 待建 | 红 | 自命中排除逻辑缺失时"本 Spec 合并后自报一条命中"必红 | NORMAL |
| SC-6 (旧19c) | 待建 | 红 | 三臂（静默截断/排序错/截断后报无竞品）均可信 | NORMAL |
| SC-7 ⭐ | 待建 | 红 | **本席核对两份真实文件**（`:6`/`:22`）内容与描述完全吻合 | NORMAL |
| SC-8 ⭐ | 待建 | 红 | 同一对真实文件确有多个 code span (`confirmed`/`major`/`next-cycle`)，"取任意位置第一个"确会抽错 | NORMAL |
| SC-9 ⭐ | 待建 | 红 | **本席实测** `normalize_linked_issue('无')` 返回 `None`，因果链成立 | NORMAL |
| SC-10 ⭐ | 待建 | 红 | 同上验证支撑；回落触发条件写成"canonical集合为空"的坏实现会让"无"那份走URL回落，可辨 | NORMAL |
| SC-11 | 待建 | 红 | 折叠 `wu_empty`/`no_field` 为同一枚举值的实现会被抓——两个空集合表面行为相同，是最容易被偷懒实现蒙混的一条，设计得当 | NORMAL |
| SC-12 ⭐ | 待建 | 红 | **本席直接实测复现**：`git symbolic-ref refs/remotes/github/HEAD` → exit 128，逐字匹配 | NORMAL |
| SC-13 ⭐ | 待建 | 红 | 照抄 `_DEFAULT_BRANCH_FALLBACKS` 名字猜测的实现必红；具体猜测列表内容未逐字核对，见 **F10** | NORMAL（轻微未核） |
| SC-14 ⭐ | 待建 | 红 | **本席直接实测复现**：`git for-each-ref` 显示 `probe` 在 remote-tracking 里但 `git remote -v` 没有，`git config --get remote.probe.url` exit 1 | NORMAL |
| SC-15 | 待建 | 红 | 把 `log()` 写进 stdout 破坏 JSON 契约的实现必红 | NORMAL |
| SC-16 | 明确无代码宿主，AB fixture | N/A | 三者任一折叠成"无竞品"的实现必红 | NORMAL |
| SC-17 ⭐ | 待建 | 红（**本席实测**：`每轮入口: 竞品 spec 探针` 当前计数=0；`## Convergence 模式`/`## Challenge 模式` 标题存在） | 只 patch 一处的实现命中1次必红；docstring 已预先声明"未来第三模式块会误判"的已知限，是好实践 | NORMAL |
| SC-18 ⭐ | 待建 | 红（探针不存在） | 三臂坏实现（宽松定位含假阳性/加固过头漏真簇）均可信 | NORMAL 机制上；**叙事性依据的语料现状已过期，见 F7** |

## 经本轮实读确认成立的部分 (下轮免重复)

- 母 Spec 全部行号引用（`collision.py`/`claim_schema.py`/`claim_lifecycle.py`/`identity.py`/`track_id.py`/`constants.py`/`gc.py`/`phase1_gate.py`/`release_gate.py`/`coordination_ref.py` 及各 SKILL.md）逐条核对 **精确匹配**，未发现任何虚构行号。
- field-availability 的 E0-E6 抽取规则、6 条真实语料反例、`normalize_linked_issue` 行为、GRANDFATHERED 6 路径存在性 —— **全部逐条核实成立**。
- sibling-spec-probe 的「本仓当场可复现」类断言（`github` 无 symbolic-ref、`probe` 陈旧 remote-tracking ref、`normalize_linked_issue('无')→None`、两份真实归档字段行内容）—— **全部亲手复现成立**。
- SC-13/16/17/18/19 的迁出承接关系诚实，旧 SC-19(b) 的归属判断（不迁入探针，改由 SC-29 承接）两侧独立推理一致。
- SC-8/SC-10 的 M-16 拆绑、SC-9/SC-14 的散文/代码类别订正 —— **均已落实**，非空头自述。
- Rule #6 三份 Spec 判据表落格均可复核（`phase-a-planner.json`=2 evals、`spec-drafter.json`=2、`state-scanner.json`=12、`audit-engine.json` 确认不存在），母 Spec 与 sibling-spec-probe 对 rule6_note 的处置诚实。

## scope_ok

`true`。三份 Spec 各自变更面与其自述范围一致，未发现越界改动；本席未修改任何被审文件（`git status` / `stat` mtime 已核实三份 proposal.md 未被触碰）。

## 一句话结论

三份 Spec 的事实基线质量在本席核对的 ~55 条 SC + ~60 条 `文件:行号` 引用中**全部精确匹配**（含多条亲手复现的因果链），R2 的 M-16 系列与 SC 迁移承接关系均属实——但本轮用「与既有测试交叉比对」的新方法在母 Spec 挖出两条此前三轮审计都未发现的**恒绿风险**（SC-2/SC-7 测不出它们声称要防的回归），加上 SC-29 回归守卫的 fixture 未命中本 Spec 真正新开的风险面、以及 `A.0` 锚点与既有约定的命名冲突，母 Spec 判 **REVISE**；field-availability 因其全部「代码」类 SC 缺一个声明的测试宿主（直接命中该 Spec 自己要治的「无实现宿主」病根）判 **REVISE**；sibling-spec-probe 未发现同等量级问题，判 **PASS_WITH_WARNINGS**。语料数字的当日观测漂移（F7/F8）不影响任何设计结论。
