---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-12T03:10:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R4 — qa-engineer 席位报告

## 0. 派发口径更正 (与 R4-0/R4-1 一致, 独立复核)

任务书写「R3 — 被审对象 = R2-fix 后的 A.2 产物 (commit `0dd26ce`)」。实跑核验:

```
$ git rev-parse HEAD
e9709435e71d88bc4524ace7073298cfc602e793
$ git merge-base --is-ancestor 0dd26ce HEAD && echo YES
YES
$ git log --oneline 0dd26ce..HEAD -- openspec/changes/premerge-gate-mainbranch-failclosed/
e970943 docs(spec): R3-fix — 不再做第四次同形换量, 改为「停止预写量 + 诚实上报」; xcheck 补齐维度
$ ls .aria/audit-reports/ | grep 'post_planning-R4-'
post_planning-R4-0-premerge-gate-mainbranch-failclosed-tech-lead.md
post_planning-R4-1-premerge-gate-mainbranch-failclosed-backend-architect.md
```

`.aria/audit-reports/` 内已有一轮完整真实 R3 (5 席 + aggregate, `post_planning-R3-1786494000000-...-aggregate.md`, 判 FAIL)。交付契约要求的文件名是 `R4-2`, `rounds: 4` —— 我审的是 **R3-fix 后的产物** (`e970943`, HEAD, 工作树干净), 是 R4 的 qa-engineer 席位。与 R4-0 (tech-lead) 采取同一口径: schema 字段 `introduced_by_r2fix` 读作「由本轮被审的那次 fix (= R3-fix) 引入」。这本身是本 session 又一次「共享 Spec 每次实质动作前必 fetch」的实证 (memory `feedback_concurrent_duplicate_audit_fetch_before_start`)，供编排层核对派发是否重复。

---

## 1. 投票

| 项 | 值 |
|---|---|
| VOTE | **REVISE** |
| VERDICT | **FAIL** (1 Critical, 与 R4-0/tech-lead 的 F-1 独立收敛) |
| findings | 1C (corroborated) + 1M (新) + 1m (新) = 3 |
| blocks_phase_b | 1 (F-1, 与 tech-lead 收敛) |

`converged: null` (单席无权判收敛)。

---

## 2. R2 的 1C + ~13M 是否真闭合 —— 本席位角度的独立抽查

R4-0 (tech-lead) 已对全部 13 条逐条回源, 我不重复整表, 但**没有采信「已修」的声称**, 而是用**与 tech-lead 不同的方法**独立抽查了三条与 QA/可证伪性直接相关的项:

```
$ grep -n "含任一 legacy key 的 config" openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
321:| **SC-M10** | 负控: `enabled=false` 早退。**两个 fixture 变体, 缺一不可**: (a) 干净 config; (b) **含任一 legacy key 的 config** (交叉输入) | ...
  → ✅ SC-M10 交叉输入变体确实逐字在场

$ grep -cE '^#### +TASK-014 验收判据' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
0
  → ✅ TASK-014 第三版量确已作废, 今日文本不再含该小标题 (第四次没有重犯「换量不换手段」)

# TASK-021 收口闭包 — 独立用程序重算 (非手工枚举, 方法与 tech-lead 不同):
$ python3 -c "
import yaml
d = yaml.safe_load(open('openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml'))
tasks = {t['id']: t for t in d['tasks']}
def anc(tid, seen=None):
    seen = seen if seen is not None else set()
    for dep in tasks[tid].get('dependencies') or []:
        if dep not in seen:
            seen.add(dep); anc(dep, seen)
    return seen
closure = anc('TASK-021') | {'TASK-021'}
TESTISH = ('test_', 'tests/')
offenders = [tid for tid,t in tasks.items()
             if any(any(k in str(x) for k in TESTISH) for x in (t.get('deliverables') or []))
             and tid not in closure]
print('闭包大小:', len(closure), '交付测试文件但漏在闭包外:', offenders or '(空)')
"
闭包大小: 16 交付测试文件但漏在闭包外: (空)
  → ✅ 与 tech-lead 结论一致 (不同方法收敛): TASK-021 依赖闭包确实覆盖全部交付测试文件的任务
```

**结论: 三条抽查全部闭合, 与 tech-lead 的整表结论一致, 方法独立。** 我把 `r2_closure` 判为**闭合**, 但这不代表 R3-fix 本身零缺陷 —— 见下。

---

## 3. 逐条 finding

### F-QA-1 🔴 Critical (= 与 tech-lead R4-0/F-1 独立收敛, 非重复劳动 —— 本席位独立读取后确认成立)

**locator**: `detailed-tasks.yaml` TASK-017 verification 第 4 条 · `tasks.md:141` · `proposal.md:394`

**实读** (`detailed-tasks.yaml` TASK-017 verification 第 4 条, 逐字节选):
> 🔴 **第 9 项落点 = 主仓 gitlink (非文件, 2026-08-12 新增)**: … ⇒ **判据换到树对象层**: 主仓根跑 `git rev-parse HEAD:aria` (实跑 rc=0, 断言其值 == aria 子模块**本 change 落地 commit**的 SHA)。

**实跑**:
```
$ git rev-parse HEAD:aria
af87caeeed88af6af76f29a8002badbe1228d927
$ git -C aria rev-parse HEAD
af87caeeed88af6af76f29a8002badbe1228d927
```
两者今日相等 (因为今天还没开始实施), 但这不能证明判据可求值 —— 「aria 子模块**本 change 落地 commit**」这个量本身在 Phase B 语境下无定义: 子模块的落地 commit 只在 Phase C.2 本地 merge 之后才存在 (CLAUDE.md「多远程推送 — 两条硬约束」约束 1 逐字规定子模块合并必须本地做)。该条款既没有像同一提交里 TASK-015 那样做「Phase B 可求值半边 / Phase C 明确移交半边」的拆分 (`metadata.evaluation_time_convention` 派生规则 (2) 本身就在同一份 yaml 里逐字要求这个拆分), 也没有把自己标注为 Phase C 专属核验。

**为什么算 Critical (QA 角度补一条独立理由)**: 从可证伪性角度看, 这条判据不满足「一个实现下必红、另一个实现下必绿」的最基本 fixture 结构 —— 因为它压根没有告诉实施者**在什么时间点**跑这条 `git rev-parse` 命令。若在 Phase B 完成点跑, 右侧的量不存在 (子模块分支还没被本地 merge), 判据本身就是 ill-defined; 若拖到 Phase C 才跑, 则需要实施者自己脑补「这条其实是 Phase C 的」, 而条款文本没有这个信号。**一个「怎么会红」的判据答不出「什么时候跑」, 本身就不是一条可交付给 TDD RED-before-GREEN 流程的验收标准。**

**怎么会红**: 让实施者在 TASK-017 声明完成的那一刻执行该命令 —— 他要么说不出「本 change 落地 commit」指哪个 SHA (未合并), 要么把主仓 gitlink 现在就 bump 到 aria feature 分支尚未合并的 tip 上 (为了让判据"过") ⇒ 后者正是 Aria #165 同族的 orphaned gitlink。

**blocks_phase_b**: 是。**introduced_by_r2fix (= 本轮 R3-fix)**: 是 (该判据是 2026-08-12 新增的第 9 项, R3-fix 产物)。

---

### F-QA-2 🟠 Major (新, 我独立发现且已构造反例验证) — `xcheck.py` CHECK6 的「理由已成文」判据不做邻近绑定, 可被与该倒置完全无关的文本免费蒙混; 构造两个全新的、真实的、无理由的 DAG 组序倒置, CHECK6 全部判「已成文」, 脚本整体仍报 PASS

**locator**: `scratchpad/xcheck.py` CHECK6 (`:585-606`, `RATIONALE` 判据)

**背景**: CHECK6 是本轮 (R3-fix) 新增的两项检查之一, 用来堵 R3 点名的「task_group ↔ DAG 方向一致性」同族缺席。它的判据逐字:
```python
RATIONALE = ("理由", "因为", "必须先于", "先于", "正交", "天然", "有理由", "不能是事后补票")
...
ok = (dep in doc_a and any(r in doc_a for r in RATIONALE)) or (
    tid in doc_b and any(r in doc_b for r in RATIONALE)
)
```
`doc_a` 是**整个任务**的 `verification + notes + title` 拼成的大 blob (`blob()` 函数), 不是像 CHECK1 那样先按句子切开再判「理由词与 ID 是否同句」(CHECK1 的 `frags()` + `near = " ".join(f for f in frags(b) if n in f)` 邻近绑定, 见 `xcheck.py:165`)。**CHECK6 没有复用这个刚刚才在 CHECK1 里被证明必要的邻近约束。**

**实跑** (在隔离副本上做的构造; 命令与输出全部原文):

```
# 第一步: 在不做任何修改的情况下, 独立确认 TASK-011 的 blob 天然同时含
#         「TASK-002」(它是 TASK-011 的真实依赖) 与某个 RATIONALE 关键词
#         (与 TASK-002 完全无关 —— 是在讲 SC-M3b 的拒绝域):
$ python3 -c "
import yaml
d = yaml.safe_load(open('detailed-tasks.yaml'))
tasks = {t['id']: t for t in d['tasks']}
t11 = tasks['TASK-011']
blob = '\n'.join(str(x) for f in ('verification','notes','title')
                  for x in ((t11.get(f) if isinstance(t11.get(f), list) else [t11.get(f)]) if t11.get(f) else []))
print('TASK-011 group:', t11['task_group'], 'deps:', t11.get('dependencies'))
print('contains TASK-002:', 'TASK-002' in blob)
RATIONALE = ('理由','因为','必须先于','先于','正交','天然','有理由','不能是事后补票')
print('hits:', [r for r in RATIONALE if r in blob])
"
TASK-011 group: TG-2 deps: ['TASK-002', 'TASK-003']
contains TASK-002: True
hits: ['因为']

# 「因为」出现在哪句? —— 与 TASK-002 无关, 讲的是 SC-M3b pattern 收紧:
#   「...2026-08-11 pattern 扩了拒绝域(加 ["']?), 因为上一版的声称『写死字面值必红』
#     强于它的实际拒绝域...」

# 第二步: 只改一处 —— 把 TASK-002 的 task_group 从 TG-0 改到 TG-3
#         (人为制造两个全新的、无任何理由文本支撑的组序倒置: TASK-011/TASK-014 都依赖它)
$ python3 -c "
import re
raw = open('detailed-tasks.yaml', encoding='utf-8').read()
lines = raw.split(chr(10)); out=[]; in_002=False
for ln in lines:
    if ln.strip()=='id: TASK-002': in_002=True
    elif re.match(r'^-\s*id:\s*TASK-\d{3}', ln.strip()) and in_002: in_002=False
    if in_002 and re.match(r'^\s*task_group:\s*TG-0\s*$', ln):
        ln = ln.replace('TG-0','TG-3')
    out.append(ln)
open('detailed-tasks.yaml','w',encoding='utf-8').write(chr(10).join(out))
"

# 第三步: 跑 xcheck CHECK6
$ python3 xcheck.py <mutated-copy> --repo-root /home/dev/Aria
  ...
  CHECK 6 — task_group ↔ DAG 方向一致性 (R3 点名的同族缺席项)
  ==============================================================================
  规则: task_group 编号 < 某依赖的 task_group 编号 ⇒ 红, 除非两侧任一写有指名对方的理由。
    TASK-011 (TG-2) dep TASK-002 (TG-3)  ✓ 已成文
    TASK-014 (TG-2) dep TASK-002 (TG-3)  ✓ 已成文
    TASK-015 (TG-3) dep TASK-019 (TG-4)  ✓ 已成文
  ==============================================================================
  RESULT: PASS — 六项交叉检查全部通过
```

（`TASK-014` 同样天然命中 —— 独立核验: `contains TASK-002: True`, `hits: ['理由']`，也是在讲别的事。）

**缺陷**: 我人为把一个基础 spike 任务 (TASK-002, 五种 cwd 全可达的锚点探测) 的 `task_group` 挪到晚于依赖它的 TASK-011/TASK-014, 这是一个**真实的、荒谬的、任何 reviewer 都会一眼看出没有理由**的组序倒置 (基础 spike 排到用它结论的任务之后), CHECK6 却把两条都判「✓ 已成文」, 脚本总输出仍是 `RESULT: PASS`。原因就是判据只问「这个任务的大段文本里, 某处出现过 dep 的 ID 字符串, 且某处 (不管在哪) 出现过一个理由词」——两者可以毫无关系。**这正是 CHECK1 在同一份文件里已经修过的那类 bug** (`xcheck.py:154` 注释「⚠️ 不收『半边归 TASK-xxx』这类措辞…歧义句式一律不断言」+ `near = …` 的邻近绑定), 而 CHECK6 是**同一轮同一个作者新写的**, 却没有复用这个刚被证明必要的约束 —— 「只修实例不修类」在**关闭该类的同一轮、同一份脚本文件内、相邻两个函数之间**复发 (与 tech-lead F-1 指出的「同一轮同一执笔者在相邻两条任务上复发」是同构的现象, 只是发生在审计工具自己身上而不是 Spec 正文里)。

**与 CHECK6 唯一一条真实数据 (`TASK-015 dep TASK-019`) 的对照**: 那一条的「理由」文本是**逐字针对这个具体依赖**写的 (`tasks.md:69`「TASK-015(TG-3) 依赖 TASK-019(TG-4) — 有理由且已成文: Rule #6 判据表第三行三件套要求…」), 是真实、on-topic 的论证。但 CHECK6 的判据逻辑**分辨不出**这条真论证和我构造的两条假蒙混 —— 它们在机制层面走的是同一条 `ok = True` 路径。当前取值恰好为 PASS 不能作为它「有效」的证据 (与 memory `adversarial-fixture` 一致的形状)。

**怎么会红**: 上面的实跑即是 —— 任何未来对 `task_group` 字段的误改, 只要该任务的 verification/notes/title 里凑巧含被依赖任务的 ID 字符串 (在这类长文档里极常见, 几乎每个任务都会在别处提到别的任务) 与八个通用理由词之一 (其中「因为」「先于」「理由」都是全文极高频词), CHECK6 就会静默放行, 不会有任何机械信号变红。

**blocks_phase_b**: 否 (它是审计机制自身的缺陷, 不直接阻断 Phase B 的交付物; 但它直接削弱本轮核心处方「机械交叉检查」的可信度, 与 tech-lead F-4/F-5/F-6 同族, 是该族目前唯一命中 **CHECK6** 的实例)。
**introduced_by_r2fix (= 本轮 R3-fix)**: 是 (CHECK6 是 R3-fix 新增的两项检查之一)。

---

### F-QA-3 🟡 minor (新角度, 与 tech-lead §3.1(2) 部分重叠, 但补了「命中的正是我本席位要审的 SC-M14」这一点) — `CHECK5` 对 SC-M6..SC-M14 共 9 行 (含本轮 QA 焦点 **SC-M14** 自身) 因「今日实测」栏是破折号而整体跳过, SC-M14 的红窗声明从未被机械复核过

**locator**: `xcheck.py` CHECK5 (`:548-550` 的 `if not claimed: … skip`)

**实跑**:
```
$ python3 xcheck.py openspec/changes/premerge-gate-mainbranch-failclosed --repo-root . 2>&1 | grep -A1 "SC-M14"
  SC-M14   今日实测非数字 (—) — 跳过
```

**缺陷**: 这不是一个"错误"意义上的 bug (SC-M14 测的是尚不存在的「共享重试 helper」, 今天确实没有数字可算, 这是 TDD RED-before-GREEN 的正常状态), 但它意味着**本轮任务书要我重点审的对象** (SC-M14..M17 的红窗真实性) 里, SC-M14 这一条今天**结构上不可能被 CHECK5 机械复核**, 只能靠人工读散文 (与 SC-M14 自己那句「无编号即不被任何机械勾稽点找到, 只能靠人工读散文」互为镜像 —— 这次不是没编号, 是编号了但机械勾稽点覆盖不到)。我用与 tech-lead 独立的路径 (aether.py 源码实读, 见下) 验证了它的散文推理站得住:

```
$ sed -n '160,190p' aria/skills/phase-c-integrator/scripts/ci_backends/aether.py | grep -n "text=True\|except\|TimeoutExpired"
# (确认 _run_with_retry 用 text=True, 只 except TimeoutExpired, 未处理 UnicodeDecodeError)
```
⇒ SC-M14「照搬 aether.py 的 text=True 而不换 decode 策略必红」这个论据**有真实代码支撑**, 不是凭空编造的假设情形。**红窗本身可信**, 但可信度目前完全靠人工读代码, 机械交叉检查在这条线上是**结构性盲区**而非「暂时没测到」。

**怎么会红**: 若日后有人把 SC-M14 表格行的 `verdict`/`kind` 期望值悄悄改错 (比如把 `main-branch-verify-failed` 打错成别的 kind 名), CHECK5 不会发现, 因为它对非数字声称值整体不处理。

**introduced_by_r2fix (= 本轮 R3-fix)**: 部分是 —— CHECK5 本身是 R3-fix 新增, 但「今日实测=—」这个空白早于本轮 (SC-M14 是 R2-fix 加的)；本轮新增的是"号称覆盖但结构性覆盖不到"这个落差。

---

## 4. 那道机械交叉检查真的有效吗 (任务书四问, QA 角度作答)

**(1) 四项 (现六项) 判据覆盖得住 R2 那两个形状吗?**
不完全。CHECK1/CHECK2 已被 tech-lead (F-4/F-5) 证明有 fail-open 缺口; 我这轮补的 **F-QA-2 证明 CHECK6 (本轮新增, 专门用来堵"同族缺席"的那两项检查之一) 同样对"移交/理由不成立却被判定合规"这个形状 fail-open** —— 而这正是 R2 两个形状之一 ("移交给没核过的下游") 在新场景 (task_group 排序理由) 下的翻版。

**(2) 有没有恒绿的判据?**
CHECK5 对 SC-M6..M14 共 9/20 行结构性 skip (F-QA-3), 相对这 9 行是**恒不检**而非恒绿, 但效果等价 —— 它们的「今日实测」栏永远不会被 CHECK5 判红, 无论声称值改成什么 (只要仍不是纯数字)。**CHECK6 在"理由文本与被依赖 ID 同任务但不同句"的输入子空间上是事实上的恒绿** (F-QA-2 实证: 任何长文档几乎必然满足这个条件)。

**(3) 它自己是不是"只修实例不修类"的产物?**
是, F-QA-2 是第三手证据 (第一手: 原始 CHECK1-4 的 5 处失效; 第二手: tech-lead 本轮的 F-4/F-5/F-6)。而且这次落在最讽刺的位置 —— **CHECK1 在同一份文件里已经把"邻近绑定"这个类级修复做对了 (`near = ...`), CHECK6 是同一轮同一次改写里新写的姊妹检查, 却没有复用这个刚证明必要的约束**。这比"忘了推广到别的检查项"更进一步: 修法**就在隔壁函数里**, 依然没有被复用。

**(4) 拒绝能力 vs 当前取值**
F-QA-2 就是这一问的答案: 当前取值 (`PASS`) 对 CHECK6 唯一一行 (`TASK-015 dep TASK-019`) 而言是真的 (有真实理由文本), 但我改一处 (`TASK-002` 的 `task_group`) 就在**零新增文本**的情况下让它对两个全新的、无理由的倒置也判"已成文"。**它当前 PASS 的唯一原因是"运气好, 目前没人乱改 task_group", 不是它有拒绝乱改的能力。**

---

## 5. 我认为不该再报的 (与 tech-lead §7 一致, 补一条我自己验过的)

- **TASK-021 收口** —— 我用独立方法 (程序化祖先闭包 + deliverables 扫描, 非手工枚举) 复算, 结论与 tech-lead 一致: 闭包大小 16, 零遗漏。**不要再动它。**
- **SC-M15/SC-M16/SC-M17/SC-M18 的「今日实测」数字本身** —— 我逐条 `grep` 复跑, 全部与表内声称值逐位一致 (`0`/`0`/`2`/`2,4,3,0`), 且 `<details>` 块数确实是 0 (SC-M15/SC-M3c 的「空真」自陈属实, 不是掩饰)。**这几行不要再报"数字不符"这类 finding, 除非用了新方法。**

---

## 6. 阻塞 Phase B 的条目

| # | 条目 | 理由 |
|---|---|---|
| F-QA-1 (= tech-lead F-1) | TASK-017 gitlink 判据未标注求值时点, Phase B 求值即 ill-defined 或制造 orphan | Critical; 两独立席位收敛 |

按 CLAUDE.md 规则 #10, 上述阻断不得由 AI 自行豁免。

---

## 7. 席位结论

**VOTE: REVISE · VERDICT: FAIL (1C 收敛 + 1M 新 + 1m 新)**

R2 的三条抽查 (SC-M10 变体 b / TASK-014 作废 / TASK-021 闭包) 用与 tech-lead 不同的方法独立复核, 全部闭合。但本轮核心处方 (机械交叉检查) 在我的角度下又添了一个新缺口: **CHECK6, 本轮为堵"同族缺席"而新增的两项检查之一, 自己就是又一个"只修实例不修类"的实例** —— 且修法 (邻近绑定) 就写在同一文件的隔壁函数里, 未被复用。SC-M14 (本轮点名要我重点审的新增 SC 之一) 的红窗论据本身可信 (有真实源码支撑), 但结构上不在任何机械检查的复核范围内, 只能靠人工。

`converged: null` (单席无权判收敛)。
