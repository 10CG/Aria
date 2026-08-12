---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T00:02:55.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — qa-engineer 单席报告

被审对象: commit `0dd26ce` 后的 A.2 产物 (`proposal.md` / `tasks.md` / `detailed-tasks.yaml`)。

**投票**: PASS (verdict PASS_WITH_WARNINGS — 0 Critical, 3 Major, 1 Minor, 全部是「加固建议」而非「阻塞 Phase B 的活缺陷」)。

## 方法论声明 (硬性纪律遵从)

本轮全部数字与行号引用均**实读源文件**得出 (`Read` 工具, 逐行核对); 全部「拒绝能力」结论均**实跑**得出 (在 `/tmp/claude-1000/-home-dev-Aria/a87f33ea-9a9d-49e2-a762-18d0fd38bfc4/scratchpad/qa-mut/` 隔离副本内变异, 命令原文见下)。**只读, 未改动真实仓文件** — 已用 `git status --porcelain openspec/changes/premerge-gate-mainbranch-failclosed/` 核验为空。

---

## 一、xcheck.py 拒绝能力实测 (R3 核心问题的正面回答)

方法: 复制三件套到隔离目录, 对 `xcheck.py` 声称守护的四类失效逐一构造**最小变异** (mutation), 实跑并记录结果。基线先确认原样 PASS:

```
$ python3 xcheck.py .   # 隔离副本, 未改动
RESULT: PASS — 四项交叉检查全部通过
```

### 1.1 CHECK1 (DAG 依赖边 vs 移交对象) — **拒绝能力属实**

变异: 在 `TASK-016`(CLAUDE.md 规则 #8 同步) 的 `verification` 里新增一句臆造引用 `TASK-017`(它俩无任何依赖序)。

```
$ python3 xcheck.py .
  TASK-016  -> TASK-017   ✗ (无序)
RESULT: FAIL (1)
  - CHECK1: TASK-016 的 verification 点名 TASK-017 但两者无依赖序
```

**结论**: CHECK1 在**逐条引用 (per-mention) 粒度**上确实能拒绝一个新捏造的、拓扑上不成立的移交。这是四项里唯一被我验出「真有拒绝力」且粒度对的一项 —— 它精确对应 R2 诊断的原始缺陷形状 (`TASK-010` 点名 `TASK-008` 但 `TASK-008` 当时不依赖它)。

### 1.2 CHECK2 (每条 SC 的 owning task 是否交付测试文件) — **恒绿式漏洞, 已复现**

判据逐字是「该 SC 的**任一** owner 有测试类 deliverable 即算过 (`any(r.endswith("✓")...)`)」—— 这是**跨任务 OR**, 不是「真正评断该 SC 的那个任务有测试」。

变异: 只删掉 `TASK-008`(gate 层真实评断 SC-M14 的任务) verification 里的 `SC-M14` 那个词, 保留 `TASK-004` 里已有的、**明文自我声明「不是我评断」**的提及 (`detailed-tasks.yaml:214-215` 逐字:「SC-M14 本身在 **TASK-008** 求值, 本任务只交付使它**可能**为绿的那半」):

```diff
- SC-M6 / SC-M13 / SC-M7 / SC-M8 / SC-M14 全绿 (...)
+ SC-M6 / SC-M13 / SC-M7 / SC-M8 全绿 (...)
```

```
$ python3 xcheck.py .
  SC-M14   owners=TASK-004✓  ✓
RESULT: PASS — 四项交叉检查全部通过
```

**结论**: 一个「真正评断 SC-M14 的任务丢失了对它的认领」这种**恰好命中 R2 诊断的『移交给没核过的下游』同款形状**的回归, CHECK2 检测不到 —— 只要还留着一个**明文自称不负责**、但恰好有其他测试文件 deliverable 的旁支提及, 该 SC 就永远绿。这是**恒绿判据**: 判据本体「任一提及者有测试文件」与它想验证的性质「真正的评断者有测试文件」不是同一件事, 且没有机制区分「认领」与「免责声明式提及」。

### 1.3 CHECK3 (断言的量是否随实施位移) — **粒度是任务级, 非锚点级, 恒绿式漏洞**

判据逐字是「该 task 的 `verification` blob 里**只要出现过一次**护栏关键词, 该 task 的**全部**行号锚就都算有护栏」(`guarded = any(...)`, 作用域是整个 `blob(t, "verification")`, 不是逐条 bullet)。

变异: 给 `TASK-006` 新增一条**全新臆造、真实文件里并不存在**的行号锚 `:999`, 且这条新 bullet **不带任何护栏字样**; `TASK-006` 原有的其他 bullet 里已含护栏关键词 (`行号锚 (:21/:300/:427) 以基线 SHA 为准...`)。

```
$ python3 xcheck.py .
  TASK-006  行号锚 :21,:300,:427,:999          ✓ 有位移护栏
RESULT: PASS — 四项交叉检查全部通过
```

**结论**: 一条**毫无护栏的新锚点** (且指向一个不存在的行) 混进已有护栏语句的任务后, 依然全绿 —— CHECK3 验证的是「这个任务提过一次护栏咒语」而不是「这条具体锚点有没有被护栏覆盖」。考虑到本 Spec 六轮以来锚点是持续追加的量 (逐任务新增 bullet 是常态编辑动作), 这正是最容易在**未来编辑**中静默复发的形状。

### 1.4 CHECK4 (插入点是否被多条条款同时管辖) — **纯字面量匹配, 零语义, 恒绿式漏洞已复现且最严重**

判据本体是一份**逐字复制自 R2-fix 自己写下的六句话**的 `need` 白名单 (`"两节不得互相援引"` 等), 命中即算「该不变量在场」。

变异 A (验证它至少不是「永远命中」): 把 proposal 里的 `"两节不得互相援引"` 改写成同义但字不同的 `"两节各自独立描述"`:

```
$ python3 xcheck.py .
RESULT: FAIL (...)
  - CHECK4: proposal 缺 §6 声明两节不得互相援引
```

确认它会因**改写措辞**而红 (说明它不是死代码)。但这只证明它对「字面量消失」敏感, 不证明它对「语义被违反」敏感。

变异 B (关键实验 —— **恢复变异 A**, 保留全部六句必需字面量原封不动, 只在 §6 尾部**追加**一句制造真实矛盾):

```
(测试注入) 若 §6.1 的插入点判定与本节冲突, 以 §6.1 的三早退位置为准, 存在性核验也一并挪到该点之后。
```

这句话**逐字违反**了 CHECK4 想守的那条不变量本身 (§6 与 §6.1 的插入点被同一句话互相援引并合并, 制造出 R2 判 Critical 时的原型矛盾 —— 「同一个插入点被两条条款要求相反结果」), 但六个必需字面量 (`"两节不得互相援引"` 等) 一个字没动:

```
$ python3 xcheck.py .
RESULT: PASS — 四项交叉检查全部通过   # (剔除 1.3 的 TASK-016 变异后单独复跑, 同样 PASS)
```

**结论**: CHECK4 是一份**纯字符串存在性检查**, 对它自称守护的不变量 (两个插入点互不冲突) 没有任何语义解析。**只要免责声明句还在, 文档尾部随便加一句实质推翻它的话, CHECK4 岿然不动。** 这是四项里恒绿性最强、也最讽刺的一项 —— 它是 R2-fix 为了「防止条款自相矛盾」而造的机制, 但它自己的构造方式 (逆向摘抄本轮刚写下的几句话当判据) 正是 R2 诊断的病灶「只修实例不修类」在工具层面的复现: 它精确防住了 R2 抓到的**那一句矛盾的具体措辞**, 对**同一形状、换一种写法**的矛盾零抵抗。

### 1.5 小结 — 回答 R3 给出的四个具体问题

1. **四项判据覆盖得住 R2 那两个形状吗?** 部分覆盖。CHECK1 对「移交给没核过的下游」的**拓扑序**半部分覆盖良好 (1.1 已证); CHECK2/CHECK3/CHECK4 表面上对应「只修实例不修类」与「移交」两个形状, 但实测判据本体的**粒度**(跨任务 OR / 任务级而非锚点级 / 纯字面量) 系统性地弱于它们名义上要守护的性质。
2. **有没有恒绿的判据?** 有, 且不是理论推测 —— 1.2/1.3/1.4 三项均**已用具体、最小、可复现的变异实证**: 保持 xcheck.py 报 `PASS`, 同时让它名义上要防的那类缺陷真实发生。
3. **它自己是不是一个「只修实例不修类」的产物?** 是, 证据最直接的是 CHECK4: 它的 `need` 列表逐字取自本轮 fix 写下的具体句子, 本质是「校验这几句话还在」而非「校验这类矛盾不存在」——防住的是这一个实例, 没有推广成一类检测。
4. **拒绝能力验证** 见 1.1–1.4 全部命令与输出, 每项均给出「好实现绿 / 变异后本该红却仍绿(或该绿却红以验证敏感度)」的对照。

**重要限定**: 上述四点全部是对**审计工具 xcheck.py 本身**(存于 `/tmp/.../scratchpad/xcheck.py`, 非仓内 tracked 文件, 非任何 TASK 的 deliverable) 的评估, 不是对 `proposal.md`/`tasks.md`/`detailed-tasks.yaml` 三件套内容本身的评估 —— 下节二 单独回源三件套内容。这也意味着: **xcheck.py 报 PASS 只能当「必要不充分」证据**(与本 Spec 自己反复用的表述同构, 例如 §D-4 对「25 tests 全绿」的降级处理), 编排层/其余席位不应把它的 `RESULT: PASS` 直接读成「四项失效形状已被机械杜绝」。

---

## 二、SC-M14..M17 红窗真实性 / 打桩边界 / 空真核验 (回源三件套本身)

### SC-M14 (UnicodeDecodeError catch-all, mock)

- Owner: `TASK-004`(交付「可能为绿的那半」) + `TASK-008`(实际求值)。在**未变异的真实仓**内, `TASK-008` 的 verification 逐字含 `SC-M6 / SC-M13 / SC-M7 / SC-M8 / SC-M14 全绿` —— 认领关系今日成立, 上节 1.2 的漏洞是对**未来编辑**的预警, 不是今日活缺陷。
- 红窗设计: mock subprocess 抛 `UnicodeDecodeError`, 断言 `fail` + `kind=="main-branch-verify-failed"` + 未重试 + 异常不逸出。这是可证伪的具体行为断言 (可写出「抓到 UnicodeDecodeError 但仍裸抛」「误当 TimeoutExpired 重试」两类会让它变红的坏实现), 不是空真也不是恒红。
- **打桩边界缺口 (Minor, 内容级, 非工具级)**: proposal.md 有一段专门的「**打桩边界 (前一版自相矛盾, 本版钉死)**」段落 (`grep -n '打桩边界' proposal.md` 命中该段), 逐字列了 SC-M6/SC-M13 (真实 `ls-remote`)、SC-M8 (必须 mock)、SC-M7 (两种皆可, 禁网络依赖) —— **唯独没提 SC-M14**, 尽管 SC-M14 自己的表格行已明写 `(mock)`。
  ```
  $ grep -n '打桩边界' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
  303:**打桩边界 (前一版自相矛盾, 本版钉死)**: **SC-M6 与 SC-M13 用真实 `ls-remote`...
  ```
  该段本身声明「本版钉死」即自称是打桩边界的权威汇总, 但 SC-M14 是本版 (R2-fix) 新增的 SC 且明确要求 mock, 却未被汇总进这段。**怎么会红**: Phase B 实施者若只读这段汇总 (它读起来就是「打桩边界」的唯一入口) 而非逐行核对每条 SC 的括注, 可能漏掉 SC-M14 的 mock 要求, 尝试用真实环境构造非法 UTF-8 ref 名 (需要特制 git 仓库/ref, 不确定性/脆弱性高, 且不同 git 版本行为不保证一致) —— 这正是 proposal 自己在别处反复强调要避免的「依赖网络可达性/环境不确定性的手段」的同类风险。**这是与本 Spec 六轮以来反复出现的「打桩边界」矛盾同一形状的复发 (只是这次不是自相矛盾, 而是遗漏), 且是本轮 (R2-fix) 新增 SC-M14 带来的新缺口** (`introduced_by_r2fix: true`)。

### SC-M15 / SC-M16 (折叠块内零命令字面量 / 折叠块外 MAIN_BRANCH 取值说明)

- 两者 owner 均只有 `TASK-011`(单一, 不受 1.2 揭示的跨任务 OR 漏洞影响)。
- 空真自陈核验: 实测 `grep -c '<details>' aria/skills/phase-c-integrator/SKILL.md` = **0**, 与 proposal 自己写的「今日 `<details>` 块数 = 0」一致, 「空真」标注属实、诚实, 不是掩盖。
- 二者「今日实测 = 期望值」这个巧合被正确标注为无信息量, 不构成正面证据, 本身没有问题。
- SC-M15 的判据描述**不是逐字可复跑的命令**(不同于 SC-M1/M2/M4/M5/M17), 而是散文式算法描述 (`pattern = 行内 code 或 fenced code 中以 aether / git / python3 / bash 起头的串`), 对「行内 code」的判定 (单反引号 span 提取) 留有实现空间。这是**轻微欠定** (不同实施者可能写出略有出入的提取正则), 但目标行为清晰 (捕获 `:240` 这类可执行字面量), 予以 **观察性备注而非独立 finding** —— 因为它不满足「答不出会在什么实现下红」的可证伪反证门槛 (任何合理正则实现在给定的对抗 fixture 上都会红)。

### SC-M17 (config-loader v2.0 到期措辞归零)

```
$ grep -nE "still (readable|works)|removed in v2\.0|仍读|v2\.0 移除" aria/skills/config-loader/SKILL.md
249:  # v1.31.0+ replaces legacy `primitive_preference` (alias still works, emits DeprecationWarning, removed in v2.0)
257:  # v1.31.0+ replaces legacy `no_aether_fallback` (alias still works, emits DeprecationWarning, removed in v2.0)
$ grep -cE "still (readable|works)|removed in v2\.0|仍读|v2\.0 移除" aria/skills/config-loader/SKILL.md
2
```
与 proposal「今日实测 2」逐字一致, 红窗真实(非空真 —— 今日代码确实含该措辞, 转 0 是有意义的正面断言)。红窗建于 `TASK-001`, 转绿由 `TASK-020`, owner 关系清楚, 未见问题。

### R2-fix 是否引入了 M14-M17 相关的 owner/依赖新缺陷?

抽查了 `TASK-008.dependencies` 含 `TASK-010`(修复 R2 指出的「重跑全量」拓扑缺口)、`TASK-015.dependencies` 含 `TASK-021`(修复 AB 跑的 SHA ≠ ship 的 SHA)—— 均在真实仓内逐行核对存在, 属于对 R2 Major 的**真实闭合**而非文字游戏。

---

## 三、R2 的 1 Critical 闭合情况 (回源, 非采信声称)

R2 唯一 Critical: TASK-020 fail-CLOSED 插入点「既无插入点规定, 又与 D9/§6/SC-M10 同一输入要求相反结果」。

回源 `detailed-tasks.yaml:753-778` (TASK-020 verification):
- 插入点明确钉在 `:328 enabled 早退之后` 与 `:337 resolve_ci_backend(cfg) 之前`, 且逐句给出「不得放 `_normalize_config`」「不得放三早退之后」两侧各自的理由, 与 `proposal.md §6.1` 的三条用例 (i)(ii)(iii) 逐字一致；
- `TASK-008` 的 `SC-M10` 负控已含「(b) 含任一 legacy key 的 config」交叉输入变体 (`detailed-tasks.yaml:331-334`), 与 §6.1 的用例 (i) 对应；
- 信号通道要求「不得裸 `raise`, 须走 `verdict=fail` + `raw_message`, 且验收须含一条 CLI 真实路径用例」逐句具体、可执行 (`detailed-tasks.yaml:771-778`)。

**判定: 该 Critical 在本轮提交的文本层面真实、实质性地闭合**(不止是关键词命中, 三条用例的方向、位置、因果链彼此自洽, 且与 `SC-M10`/`§6`/`§6.1` 交叉引用可核实一致)。此判定与 xcheck.py `CHECK4` 的字面量匹配无关 —— 是我独立通读内容后的结论, 与工具结果**方向一致但方法独立**。

**范围限定**: 我的席位角度未逐条覆盖全部 ~13 个去重 Major (DAG 拓扑穷尽性 / 架构级插入点冲突等更属 tech-lead / backend-architect / code-reviewer 席位), 上文只报告了与我角度 (可证伪性/红窗/打桩边界/机械检查恒绿性) 重叠、且我独立回源过的子集。

---

## 四、Findings 汇总

| # | 严重度 | 摘要 | `introduced_by_r2fix` |
|---|---|---|---|
| F1 | Major | `xcheck.py` CHECK4 是纯字面量匹配, 对它声称守护的「插入点不被多条条款同时管辖」零语义验证 —— 实测: 保留全部 6 条必需字面量, 追加一句制造真实条款矛盾, 仍报 PASS | true |
| F2 | Major | `xcheck.py` CHECK2 的「owning task 是否交付测试文件」判据是跨任务 OR, 不区分「认领」与「免责声明式提及」—— 实测: 删除真实评断者 `TASK-008` 对 `SC-M14` 的认领, 只留 `TASK-004` 的明文免责提及, 仍报该 SC 有效 owner | true |
| F3 | Major | `xcheck.py` CHECK3 是任务级而非锚点级判据 —— 实测: 给已有护栏的任务新增一条**无护栏**的臆造行号锚, 仍判「有位移护栏」 | true |
| F4 | Minor | proposal.md 的「打桩边界 (本版钉死)」汇总段遗漏本轮新增的 SC-M14, 其 mock 要求只见于该 SC 自己的表格行, 未汇总进权威段落, 有被 Phase B 实施者漏读的风险 | true |

**统计**: 本席共 4 条 finding, `introduced_by_r2fix=true` 占 **4/4 = 100%**。

⚠️ **口径警示 (供编排层汇总时勿误用)**: F1-F3 针对的是 `xcheck.py` 这个**审计辅助脚本**本身 (存于 scratchpad, 非仓内文件, 非任何 TASK 的 deliverable), 与 post_spec/post_planning 历次统计的「fix 引入新缺陷占比」(针对 `proposal.md`/`tasks.md`/`detailed-tasks.yaml` 三件套内容) **不是同一总体** —— xcheck.py 是本轮全新产物, 没有「上一版」可比, 把它计入「R2-fix 引入率」分母/分子前必须先说明这一层总体差异, 否则会把「工具类新脚本天然 100% 新代码」误读成「Spec 内容缺陷率」。真正落在三件套内容上的 finding 只有 **F4 一条** (1/1 = 100%, 但样本量为 1, 不构成统计意义上的比率)。

---

## 五、阻塞项

**本席无 blocks_phase_b 项**。F1-F4 均为加固/留痕建议:
- F1-F3 建议: 在 handoff 中如实记录 xcheck.py 是「必要不充分」信号 (与 D-4 对「25 tests 全绿」的处理同构), 不应被编排层或后续轮次当作「四类失效已被机械杜绝」的证据; 若要真正堵上, CHECK2 需要「唯一/主 owner」标记而非跨任务 OR、CHECK3 需要逐 bullet 而非逐 task 判定护栏、CHECK4 需要从字面量匹配升级为对同一插入点的多条款做交叉约束求值 (而非关键词命中) —— 但这已超出本轮 Phase B 就绪判定的必要范围, 留 follow-up 即可。
- F4 建议: `TASK-004` 或 `TASK-008` 完成时, 把「打桩边界」汇总段同批追加 SC-M14 一行, 成本极低 (一行文字)。

## 六、总体判断

三件套本身 (proposal.md/tasks.md/detailed-tasks.yaml) 在我核验的角度 (SC-M14..M17 红窗真实性、打桩边界、R2 Critical 闭合) 上**站得住**, 未发现活缺陷会阻塞 Phase B。真正值得编排层重视的是 F1-F3: **R2-fix 引以为傲的「机械交叉检查」机制, 在我实测的三个维度 (owner 认领粒度 / 锚点粒度 / 条款语义) 上都存在可复现的恒绿路径**, 且这恰恰是 R2 诊断出的「只修实例不修类」在工具层面的同形复发。这不构成本轮 FAIL 的理由 (它是对未来编辑的预防性风险, 不是当前文本缺陷), 但如果编排层打算把 `xcheck.py` 的 `PASS` 当作「后续轮次可以减少人工复核强度」的依据, 本报告的结论是: **不能** —— 它目前只能证明「没有踩到已知的那几个具体坑」, 证明不了「同类坑已被杜绝」。
