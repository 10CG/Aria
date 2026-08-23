---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-23T11:04:31.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 (重写 v2 + C1/C2 落版) — tech-lead

> **席位**: tech-lead · **处置**: **REVISE** (frontmatter `verdict` 按 `verdict-format.md` 机械映射填 `FAIL` —— ≥1 Critical; post_spec `blocking: false`, 仅记录不阻断)
> **counts**: critical=**1** · major=**10** · minor=**6** · OUT_OF_SCOPE=0 · `scope_ok`: **true**
> **timestamp**: 1787481000000 (2026-08-23T11:04:31Z)

## 审计对象与工作树

| 项 | 值 |
|---|---|
| 被审文件 | `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (475 行, **未提交**; 工作树相对主仓 `1205ec3` 为 `+123/-42`) |
| 主仓 HEAD | `1205ec3` |
| aria 子模块工作树 | `cb6bd5d` (分支 `fix/issue-batch-149-151-155-134`, #149/#151/#155/#134 同批并行在改 — **非异常**, 已知并发轨) |
| aria `origin/master` | `ca52d1c` (v1.67.0, 2026-08-23T09:14:07Z, 已含前置 Spec `linked-issue-normalization` 合并) |
| 上一版比较基线 | `git show 86540f2:.../proposal.md` (C1/C2 裁定回填版) · `c6aa29a` (重写 v2) |
| 对照报告 | `post_spec-R1-1785710000000-a1-entry-claim-rewrite-{aggregated,tech-lead}.md` |
| 取证方式 | **全部 finding 经实读**; §1 与 §2.2 两条另附**可复现实跑** (脚本口径见正文); 无一条基于记忆或推断 |

**⚠️ 本席 R1 自身的两处行号误差 (先自证, 免误伤本版)**: R1/M5 记 `phase1_gate.py:1229` `if args.linked_issue:`、R1/M6 记 `:1235-1237` `except → []`。**实读 `cb6bd5d`: 门控在 `:1230`, `except` 块在 `:1236-1238`, 调用在 `:1233`。** 本版 Spec 采用的 `:1233` **正确**, 其「原 R3 记 `:1232`, 实为下一行」的订正也**正确** (`:1232` 确为 `claims = read_claims(repo).claims`)。**⇒ R1/m3 与 Spec 的 `_run_gate_impl` 行号订正 (`:335`–`:1032`) 亦经复核属实。** 本报告下文一律用实读值。

---

## 判定

**REVISE。** 本轮 rework 的**执行质量明显高于上一轮**: 两处 owner 裁定原文经 `git show 86540f2` 逐字比对**确认已恢复** (无偏差), C4/C5/C6 三条事实订正实读全部属实, `lib/collision.py` 与 `phase1_gate.py --heartbeat-only` 两条 Impact 缺口已补, SC-20/SC-21 是**真正的 runtime-invocation 断言** (SC-20 在 `STALE_TTL=1800` 现状下必红, 经算术复核成立)。**且新增的「⚠️ 实读订正 · 请 owner 复议」段是本 Spec 三轮以来第一次把「AI 发现 owner 裁定理据被证伪」正确地上呈而非自行改判** —— 这条行为本身值得记为正面信号 (memory `no-self-exempt-gates` / `narrow-owner-options` 的正确姿态)。

**但**:

| 形状 | 实例 |
|---|---|
| **A. R1 的 major 有 5 条一字未动** | M2 (§4 匹配谓词) / M4 (`standards/` 模板) / M5 (§6 缺口表 + `:1230` 门控) / M6 (fail-soft `[]`) / m1 / m2 —— 本轮 8 findings 全部来自「上一轮独立核验」, **R1 五席原报告的 major 清单没有被重新过一遍** |
| **B. 本轮新写的 4 段各自引入了新缺陷** | rule6_note 两档 (M9/M10) · (iii) 落版 (M1) · (ii) 落版 (M2) · §2.4 订正与 SC-8 脱节 (M3) |
| **C. 最重的一条是「诊断对了但处方没落」** | §1 的 ⚠️ 块把 R1/C3 诊断得**完全正确**, 却把承重规则 defer 到 A.2, 而它自己给的候选正则**实测只救 4/13** |

**按 memory `marginal-return-negative` 的判据自测**: 本轮 10 条 major 中 **5 条 (M1/M2/M3/M9/M10) 是本轮 fix 自己引入的** = 50%, 恰在「边际产出转负」的拐点上。**⇒ 本席建议: R3 不要再由同一执笔者加轮修补, 换执笔者或按 memory `fix-writer-bottleneck` 处置。** 但这是给 owner 的观察, **AI 不预判裁决。**

---

## R1 finding 逐条 closed / open

### 聚合报告的 5 个 critical 簇 (去重后)

| R1 簇 | 状态 | 实读复核 |
|---|---|---|
| **C1** 两落点 `allowed-tools` 不支持本机制 | ✅ **closed** | owner 裁 (a) 扩权; Impact `:421`/`:423` 两行逐字标明变更前后。实读 `phase-a-planner/SKILL.md:9` = `Read, Write, Glob, Grep, Task, Skill` ✅ / `spec-drafter/SKILL.md:10` = `Read, Write, Glob, Grep, AskUserQuestion` ✅ / `:9` `user-invocable: true` ✅ —— 引用全部属实。**残留 → R2-TL-m1** (无任何机械断言守护该扩权) |
| **C2** heartbeat 只换匹配键, 无人调 | ✅ **closed (设计面)** | owner 裁 (ii)+(iii); 具体入口钉为 `phase1_gate.py --heartbeat-only`; Impact 补两行; **SC-20/SC-21 是真断言** (SC-20: 现状 `STALE_TTL=1800` 时 23h ⇒ `age>STALE_TTL` 为真 ⇒ 判 stale ⇒ 必红 ✅)。**但 (ii)/(iii) 各自引入新缺陷 → R2-TL-M1 / M2** |
| **C3** §1 字段格式对真实语料 0/13 | ❌ **still open (核心未解)** | 诊断已吸收且实跑数据落版 ✅; 但承重的「抽取规则」defer A.2 + 候选实测不足 + §1.2 原文未调和 + §1.4 仍只豁免 128 篇无字段者 + 本 Spec 头部仍无该字段 → **R2-TL-C1** / **m2** |
| **C4** `_TERMINAL` 事实断言与代码相反 | ⚠️ **正文 closed, SC 未同步** | §2.4 `:180-182` 订正实读全对: `collision.py:210`(`origin/master:268`) `_TERMINAL = ("done","abandoned","unknown")` ✅ 不含 `yielded` ✅ 含 `unknown` ✅, 且给了 `unknown` 的零证据极性处置 (质量高)。**但 SC-8 原文未改 → R2-TL-M3** |
| **C5** D6「无任何函数支持释放别人 claim」为假 | ✅ **closed** | `:172` 订正为「只有无差别 sweep, 没有定向 release」—— 实读 `release_gate.py:225` help「跨 container」✅ + `gc.py:352-362` docstring「Cross-container by design」✅, 结论与理由均成立 |
| **C6** `include_terminal` 传递链漏第 0 段 | ✅ **closed** | §2.4 item 0 补 `linked_issue_overlaps` 增 keyword-only 形参 ✅; 实读现签名 `(claims, own_track_id, own_linked_issue)` 三参数 (`cb6bd5d:177-181` / `origin/master:230-234`) ✅; `lib/collision.py` 已入 Impact `:415` ✅ |

### 本席 R1 的 6 major / 4 minor

| R1 # | 标题 | 状态 | 依据 |
|---|---|---|---|
| **M1** | `yielded`/`_TERMINAL` 事实 + SC-8 + 丢失 R2/M3 | ⚠️ **partially open** | 事实面已订正; **SC-8 `:366` 逐字未动** (场景仍含 `yielded`, 「怎么会红」仍写 `_TERMINAL` skip 必红) ⇒ 与 `:181` 自相矛盾; R2/M3 (yielded 在 §2.3 status 分档的归属) 仍缺 → **R2-TL-M3** |
| **M2** | §4 探针「同 issue」匹配谓词未定义 | ❌ **still open (一字未动)** | 全文 grep 「谓词」3 命中, 无一在 §4; §4 仍只写「扫远端同 issue 的竞品 spec」(`:240`) → **R2-TL-M4** |
| **M3** | 两 Spec 间归一能力职责真空 | ✅ **closed by reality** | 前置 Spec 已 ship: `origin/master:collision.py:178` `def normalize_linked_issue(value) -> Optional[tuple[str,int]]` **是公开函数** ✅ ⇒ 真空消失。**残留**: Spec 仍只写「前置 Spec 的归一」, 未点名该 callable → 并入 **R2-TL-M5** |
| **M4** | 「进模板」丢了 `standards/` 一半 | ❌ **still open (一字未动)** | Impact 表 grep `standards/` 仅命中 `conventions/skill-benchmark-exemption.md` (引规范, 非变更面); 实读 `standards/openspec/templates/proposal-minimal.md:1-20` 字段仍只有 Level/Status/Created → **R2-TL-M6** |
| **M5** | `:1230` 门控整块 + §6 缺口表未列 | ❌ **still open + 自相矛盾加重** | §6 表 (`:270-276`) 4 行仍无「本轨无关联 issue」; 而 §2 的 NEW-01 段 `:103` **自己写着「该已知限须写进 §6 缺口表」**; 门控行全文零提及 → **R2-TL-M7** |
| **M6** | `:1236-1238` fail-soft `[]` 不在 `error` 覆盖面 | ❌ **still open (一字未动)** | §2.5 `:199` 仍只写「fetch 降级须进 `error` 契约」; SC-10 `:368` 未增子例; 实读 `except Exception → out["linked_issue_overlap"] = []` 在 `out` 层, 结构上不受 `GateResult.error` 覆盖 → **R2-TL-M8** |
| m1 | 三口径 (uuid / label-first / owner-container) | ❌ still open | §3 `:236` 仍写两个标识; 实读 `claim_lifecycle.py:150` `container=resolved.container_id` ← `identity.py:222` label-first → **R2-TL-m3** |
| m2 | §4 exit code 契约 vs SC-18 | ❌ still open | `:257`「非 0 **仅**用于探针自身失败」 vs SC-18 `:381`「无远端 ⇒ exit 非 0」→ **R2-TL-m4** |
| m3 | `_run_gate_impl` 行号 | ✅ **closed** | 订正为 `:335`–`:1032`, 实读 `def _run_gate_impl` @ `:335`, 下一顶层 `def run_gate` @ `:1032` ✅; 区间内 grep `linked_issue_overlaps` 命中 **0** ✅ |
| m4 | `layer-l-integration.md:45` `update_heartbeat()` 不存在 | ❌ **still open, 且因 C2 落版而加重** | 实读 `:45` 逐字仍是「`heartbeat` \| `phase-b-developer` mid-cycle \| 每 10min \| `lib/claim_lifecycle.py::update_heartbeat()`」; 全仓 grep `update_heartbeat` **仅此一处文本** → **R2-TL-m5** |

### R1 其余席位中经本席实读确认**仍开**的两条 (不重复计数, 供聚合去重)

- **CR/M8** `coordination` 键未在 `DEFAULTS.json` 注册 —— 实读 `grep -n coordination skills/config-loader/DEFAULTS.json` **零命中**; 默认值只活在散文 (`state-scanner/SKILL.md:149`「缺省即 true」/ `layer-l-integration.md:12`)。本轮 rule6_note 新把 SC-9 当 substitute, 使该缺口开始**承重** → 并入 **R2-TL-M10**。
- **QA/M9** SC-9/SC-14 标「代码」但实测对象是 SKILL.md 散文 —— SC-14 与既有 `tests/test_release_by_track.py:138 test_release_abandoned_roundtrips` 重复 (实读确认该测试存在) → SC-9 部分并入 **R2-TL-M10**; SC-14 部分本席不重复报 (QA 席原判仍成立)。

---

## 本轮新 findings

### 🔴 Critical

#### R2-TL-C1 — §1 的承重「抽取规则」被 defer 到 A.2, 而 Spec 自给的候选正则**实测只救 4/13**; §1.2「单一形态」原文未随之调和 ⇒ R1/C3 的「custom check 恒红 = 零信息」未解

- **category**: spec-completeness / mechanical-check-viability
- **scope**: `proposal.md:71` (§1.2) · `:72-78` (§1.3 + ⚠️ 块) · `:79` (§1.4) · SC-13 `:376` · Impact `:429`
- **证据 (可复现实跑, 语料 = 主仓 `openspec/{changes,archive}/*/proposal.md`, 归一函数 = `origin/master:collision.py:178` 逐字加载)**:

  ```
  语料 147 篇 · 有「关联 Issue」字段 14 篇 (其中 1 篇为显式 `无`)

  直接喂归一            : OK=0   EXPLICIT_NONE=1  UNPARSEABLE=13     ← R1/C3 结论复现 ✅
  Spec 候选正则 :78     : parseable=4/13   仍红=9      ← [\w.-]+/[\w.-]+\s*#\d+
  ```

  9 条落空的**真实写法**都缺 `org/` 段或被 markdown 包裹, 逐字样本:

  | 实例 | 为何 Spec 候选救不了 |
  |---|---|
  | `Forgejo [#134](https://.../issues/134) (triage ...)` | `#` 前无 `repo`, 更无 `org/repo` |
  | `aria-plugin [#95](https://.../issues/95) (归档 spec ...)` | repo 与 `#` 被 `[` 隔开, 无 `org/` |
  | `Forgejo [aria-plugin#17](https://.../issues/17)` | `aria-plugin#17` 无 `/` ⇒ 不匹配 `org/repo` |
  | `[aria-plugin #137](https://.../issues/137)` | 同上 (2 篇) |
  | `[#154](...) (readarray/bash3, ...)` | 无 repo 段 |

- **问题 (四条并列, 缺一不可)**:
  1. **§1.2 原文未改**: `:71` 仍逐字「格式固定: `<org>/<repo>#<n>` **单一形态**」, 而 `:72` 的 check 判据已改成「从字段值中**抽出的** canonical token」—— 「字段值 == 单一 token」与「字段值**内含**一个 token」是两条互斥规则, 同一节内并存无调和;
  2. **承重规则出 Spec**: `:78` 逐字「**本 Spec 现有措辞不足以实现**」+「抽取规则须在 **A.2** 定死」。A.2 是**任务规划**不是需求定义 —— 一条决定 check 判红判绿的规范性规则移出 Spec, 触 Rule #1 (需求变更须有 OpenSpec) 的精神, 且**未进「请 owner 复议」段** (属 AI 单方流程判断, CLAUDE.md Rule #10 要求写进 handoff 请复议);
  3. **候选本身没在基线跑过** (memory `check-runs-at-baseline-first`: 新机械检查须先在基线亲跑三态): 4/13 意味着 check 上线后对 **9/13 有字段者 + 133 篇无字段者**判红 ⇒ R1/C3 的「恒红 = 零信息」(memory `false-green-dual-is-permanent-red`) 原样存在, 只是从「13/13 红」降到「9/13 红」;
  4. **§1.4 仍只豁免 128 篇无字段者** (`:79` 一字未动), 对**恰恰会被判红的那 13 篇**零表态; check 的**作用域** (全量 / 仅 `changes/` / 仅新增) 仍全文未定义。
- **危害**: §1 被本 Spec 自己定为「整个机制的入口条件, 排在认领机制之前」(⭐ 段 `:56-62`)。入口条件的**唯一机械回声**在落地当天即对多数语料判红 ⇒ 要么被关掉, 要么被降噪成背景, 两种结局都回到「无机械回声的义务会退化」—— 即 §1 自己 `:81` 论证要防的那件事。
- **建议修法 (与危害同向 = 让 check 判的东西真的可判; 附实测)**:
  1. **把抽取规则写回 Spec 并钉到字符级** (memory `spec-underdetermination`: 承重算法钉到字符级)。本席实测两个更优候选, 同一语料同一归一函数:

     | 规则 | parseable/13 | 仍红 |
     |---|---|---|
     | Spec 候选 `[\w.-]+/[\w.-]+\s*#\d+` | 4 | 9 |
     | 放宽 A: `(?:[\w.-]+/)?[\w.-]+\s*#\d+` (org 可选) | **8** | 5 |
     | 放宽 B: **先剥 markdown 链接语法** (`](...)` 与 `[`/`]`) 再套 A | **12** | **1** |

     ⇒ 推荐 B。它与前置 Spec 的归一语义天然自洽 —— 实读 `normalize_linked_issue` docstring 逐字:「`org` (anything before the basename) is **NOT** part of the key」, 即**归一本来就不要求 org**, 而 §1.2 强制 org 是 Spec 单方加严;
  2. **§1.2 二选一并写死**: 或改为「字段值**必须以**规范 token 开头, 其后允许任意 markdown 与注解」(与 12/13 现存写法只差前缀), 或改为「字段值**内含**至少一个可抽取 token」(与 B 规则配套) —— **不要让「单一形态」与「抽出 token」并存**;
  3. **§1.4 补两件事**: check 作用域 + 存量 13 篇的处置 (grandfather 白名单 / 一次性修 / 只对 `changes/` 生效);
  4. 若 owner 仍要 defer 抽取规则, **须把该 defer 本身上呈**「请 owner 复议」段, 并在 §6 记为「§1 机械回声在 A.2 定规则前不可上线」。

---

### 🟠 Major

#### R2-TL-M1 — (iii) 落版遗漏 `STALE_TTL` 的**第三个消费者** `track_board.py::_freshness_status` (行为面, 非注释), 且 `STALE_TTL ≥ SWEEP_TTL` 抹掉 `constants.py:40-42` 明写的两级顺序保障; 「请 owner 复议」段对 (iii) 的影响描述与实读不符、选项集少一档

- **category**: impact-analysis / design-invariant
- **scope**: `proposal.md:154-157` ((iii) 落版) · `:161` (请复议) · SC-20 `:390` · Impact `:416`
- **证据 (逐字实读 `cb6bd5d`)**:
  - **Spec 已正确列出的**: `constants.py:36` `STALE_TTL: int = 1800` ✅ · `:32` 不变量注释 ✅ · `:51` `SWEEP_TTL: int = 86400` ✅ · `:40`/`:43-44`/`:50` 三处过期注释 ✅ · `gc.py:341` 默认值 `SWEEP_TTL` ✅ · `release_gate.py:141` 未传覆盖 ✅ —— **「改 `STALE_TTL` 对 `--sweep-stale` 零影响」这条事实订正完全成立**;
  - **Spec 遗漏的第三个消费者 (行为面)**: `skills/state-scanner/scripts/renderers/track_board.py` 的 `_freshness_status()` — **`origin/master:232`/`:234`** (本地工作树 `cb6bd5d`+未提交为 `:277`/`:279`; 并发轨 #149/#151/#155/#134 的 diff 实测**零处**触及 `STALE_TTL`, 位移来自其它已合并提交 ⇒ 该断言在两个 SHA 上均成立)
    ```python
    if age_s < HEARTBEAT_INTERVAL: return "🟢 active"
    if age_s < STALE_TTL:          return "🟡 stale? 待确认"
    return "🔴 abandoned? 可接管"
    ```
    同文件 `:25-26` docstring (两 SHA 一致) **硬编码**「`STALE_TTL = 1800 s (30 min) → 🟡`」。⇒ `STALE_TTL` 30min→24h 后, track board 的 🟡 带从 [10min, 30min) 拉成 **[10min, 24h)**, 而 🔴「可接管」只在 ≥24h 出现 —— 但 24h 正是 `--sweep-stale` 的阈值, 届时 claim 已被改写为 `abandoned` 并折叠进 Abandoned 分区 (`_classify_track` status 优先于 freshness)。**🔴 档在 freshness 路径上实际上只剩调度运气才够得到。** `track_board.py` **不在 Impact 表**;
  - **另两处同样遗漏但属注释**: `gc.py:354-358` docstring 与 `phase1_gate.py:523-526` 注释都逐字写着「no production heartbeat loop exists ... which is exactly why sweep uses the long SWEEP_TTL (24h) instead of STALE_TTL (30min)」;
  - **设计不变量**: `constants.py:40-42` 逐字「Deliberately **much longer than STALE_TTL**: STALE_TTL only marks a claim "takeover-eligible" (advisory, **reversible**), but the sweep **REWRITES** status=abandoned **durably** and the victim **has no recovery path**」。⇒ 两级阈值的**先后次序**是这段代码的承重设计。SC-20 `:390` 断言 `STALE_TTL >= 86400` **允许 `STALE_TTL > SWEEP_TTL`**, 那将使「可逆 advisory 先于不可逆 sweep」的次序**反转**。
- **问题**: owner 裁定的落版义务原文是「(iii) 的 TTL 变更**量化 sweep 语义代价**」。Spec 回答「**sweep 语义代价 = 0**」—— 对 `--sweep-stale` 这一条腿属实, 但 `STALE_TTL` 的语义代价不只这一条腿, 另两条 (reconcile 的 takeover-eligible 次序保障、track_board 的人读呈现) 未被量化, 落版义务只履行了 1/3。
- **对「请 owner 复议」段的评价 (本条属**上呈内容自身事实不全**, 故计入 finding)**: `:161` 把 (iii) 描述为「效果落在 advisory/takeover-eligible 面, 是把两个原本量级悬殊的软硬信号对齐的一个**自洽**改动」。**「自洽」与实读不符** —— `constants.py:40-42` 恰恰论证这两个信号**必须**量级悬殊。且选项集只给两档 (仍采 (iii) / 只采 (ii)), **漏掉第三档**: `SWEEP_TTL=24h` 的原始理据 (`constants.py:43-44` + `gc.py:355-357` + `phase1_gate.py:523-526` 三处逐字) **正是「无生产 heartbeat loop」**, 而 (ii) 落地后该前提消失 ⇒ 正确方向可能是**下调 `SWEEP_TTL` / 维持 `STALE_TTL`**, 而非上调 `STALE_TTL`。这正是 memory `narrow-owner-options` 的「没想到合并同根问题这个更优解」形状。
- **建议修法**:
  1. Impact 补 `skills/state-scanner/scripts/renderers/track_board.py` (`:25-26` docstring + `_freshness_status` 的 `STALE_TTL` 阈值语义), 并在 §2.2 量化 board 呈现的变化;
  2. SC-20 的断言改为**带次序的**: `HEARTBEAT_INTERVAL < STALE_TTL < SWEEP_TTL` (三段严格递增), 而非单边 `STALE_TTL >= 86400` —— 前者能拒绝「反转」这个坏实现, 后者不能 (memory `adversarial-fixture`: 验断言要验拒绝能力);
  3. 「请 owner 复议」段补第三档选项 (重估 `SWEEP_TTL`) 与 `constants.py:40-42` 的原文引用, 并撤回「自洽」措辞。

#### R2-TL-M2 — (ii) 把 heartbeat 挂成「**无条件**每次 `/state-scanner` 必跑」, 使一个只读型状态命令每次调用都写 claim + 推远端; §2.5 恰好为 A.1 写过同款 opt-out / 外向副作用论证, 却未下移到这个新入口

- **category**: side-effect-scope / opt-out-symmetry
- **scope**: `proposal.md:147-151` ((ii) 落版) · `:150` (「无条件」逐字) · §2.5 `:198` · SC-9 `:367` · Impact `:418`/`:424`
- **证据**:
  - `:150` 逐字:「与 B-entry 的关键差异: B-entry 是**条件触发** ...; heartbeat 是**无条件** —— 只要本会话在 coordination ref 里持有 active claim, **每次 `/state-scanner` 被调用都刷新**」;
  - `:148` 逐字: `--heartbeat-only` **「复用其既有 identity/fetch/push 管道」** ⇒ 含 `resilient_push` (实读 `phase1_gate.py:70`/`:108` import, `:212` 错误面) ⇒ **每次 `/state-scanner` 多一次远端写**;
  - §2.5 `:198` 逐字为 A.1 写过完全同款的顾虑:「否则 opt-out 项目在 A.1 仍被强制写 claim + 推远端 (**对未配 coordination ref 的第三方是外向副作用**)」;
  - **默认值**: `coordination` 键实测**不在** `DEFAULTS.json`; 散文默认为 `true` (`state-scanner/SKILL.md:149`「缺省即 true」/ `layer-l-integration.md:12`「默认 `true`, opt-out」) ⇒ 下游第三方项目**默认落入本行为**;
  - SC-9 `:367` 只覆盖「A.1 零调用」, **不覆盖 `/state-scanner` 入口的 heartbeat**。
- **问题**: 这是 memory `fix-the-class` 的教科书形状 —— §2.5 已经为「入口 A」写好了防护条款, 而**同一轮 rework 新造的「入口 B」**没有沿用它, 且新入口的调用频次**远高于** A.1 (每次状态扫描 vs 每次起草)。「无条件」这个词在 Spec 里是**规范性**的, 实现者会照字面写成不读 config。另: §4 对 fetch 代价做了 ~13.8s 的实测披露并明令「不得称其轻量」, 而 (ii) 给 `/state-scanner` 增加的写+推代价**零量化**, 两处标准不对称。
- **建议修法**:
  1. `:150` 的「无条件」限定为「**在 `coordination.enabled == true` 前提下**无条件」, 并在 §2.5 显式列为第二个 skip 落点;
  2. SC-9 增子例:「`coordination.enabled == false` ⇒ `/state-scanner` 入口**不触发** `--heartbeat-only`, 不写 claim, 不推远端」(现状必红, 因当前根本无该挂载);
  3. 量化 (ii) 给 `/state-scanner` 增加的写+推代价 (口径可直接复用 S2 的 fetch 实测方法), 或明写「fail-soft 且不计入 scan 预算」的依据。

#### R2-TL-M3 — §2.4 的 `_TERMINAL` 事实订正**未同步到 SC-8**: 正文说 `yielded` baseline 即绿, SC-8 仍把它写进「`_TERMINAL` skip 的现状**必红**」场景

- **category**: internal-contradiction / sc-baseline-failing
- **scope**: `proposal.md:181` ‖ SC-8 `:366`
- **证据**: `:181` 逐字「**不含 `yielded`** ⇒ `yielded` **今天就已可见**, 不需要本机制去救; 原文把它列进来是**错的事实断言**, SC-8 的该子例 **baseline 即绿**」;
  SC-8 `:366` 逐字未动: 场景「同 issue 他轨 claim 为 `done`/`abandoned`/**`yielded`**」· 怎么会红「`_TERMINAL` skip 的现状**必红**」。
  实读复核: `origin/master:collision.py:268` `_TERMINAL = ("done", "abandoned", "unknown")` —— `yielded` 不在其中 ✅; `reconcile.py` 注释亦记「yielded is NOT terminal」。
- **问题**: Spec 自己在同一份文件里对同一个子例给出**相反**的 baseline 判定。按 CLAUDE.md Rule #6「substitute 须 SC 级 **baseline-failing**」, SC-8 的 yielded 子例是**恒绿**的 —— 它验证不了任何东西 (memory `test-claims-vs-verifies`: 每条测试必答「它怎么会红?」)。且 R1/M1(b) 点名的 **R2/M3 (yielded 在 §2.3 status 分档中的归属)** 仍缺: §2.3 `:169` 只要求告警含 `status` 字段, 未定义 `yielded` 该渲染成「活跃竞品」还是「已暂停」。
- **建议修法**: SC-8 拆两条 —— (i) `done`/`abandoned`/`unknown` 三态经 CLI 可见且 `unknown` 按「未能核实」措辞 (baseline 必红); (ii) `yielded` 渲染为「已暂停」而非「活跃」(baseline 必红, 因现状无分档); 同时 §2.3 补 status 分档表。

#### R2-TL-M4 — §4 探针的「同 issue」匹配谓词**全文仍未定义** (R1/M2 一字未动)

- **category**: predicate-undefined
- **scope**: `proposal.md:238-258` (§4 全章) · SC-16 `:379` / SC-17 `:380` / SC-19 `:382` · §6 `:275`
- **证据**: `:240` 仍只写「`audit-engine` 每轮入口扫远端同 issue 的竞品 spec」; 其后 6 个 bullet 分别定义扫描范围 / 时机 / fetch 代价 / 规模上限 / 消费面 / 盲区, **无一句**定义「同 issue」的输入从哪取、怎么比。全文 grep「谓词」3 处命中, 均不在 §4。
- **问题**: 与 R1 原判完全相同, 且**现在更容易修了** —— 前置 Spec 已 ship 公开的 `normalize_linked_issue()` (`origin/master:collision.py:178`), 谓词可以直接复用它 + R2-TL-C1 的抽取规则。而 §6 `:275` 已把探针记为「部分覆盖 legacy 轨」—— 在谓词未定义的前提下声称覆盖 (memory `verify-predicate-inputs-exist`)。
- **建议修法**: §4 增「匹配谓词」小节, 钉死: 输入 = proposal 头部「关联 Issue」字段经 §1 抽取规则得 canonical token; 比较 = `normalize_linked_issue()` 的 key 相等; 并以本 Spec 的 motivating case 两份真实 proposal (`2026-07-31-phase-c-gate-path-coverage-not-applicable/` 与 `2026-08-22-phase-c-integrator-ci-path-coverage/`, **实读两者字段值都是 `[10CG/aria-plugin #122](...)`**) 作 fixture —— 它们在 R2-TL-C1 的放宽 B 规则下都能抽到 `10CG/aria-plugin #122` ⇒ 谓词可命中, 是现成的可证伪语料。

#### R2-TL-M5 — §1.3 custom check 的 Impact 只有 `.aria/state-checks.yaml` 一行: **既无实现宿主, 也无 SC-13 的验证宿主**, 且未点名已 ship 的 `normalize_linked_issue()` 为调用对象

- **category**: impact-coverage / test-host-gap
- **scope**: Impact `:429` · Impact `:419` (SC 分配) · SC-13 `:376` · §1.3 `:72`
- **证据**:
  - 实读 `.aria/state-checks.yaml`: 现有 check 的 `command:` 或指向脚本 (`aria/skills/state-scanner/scripts/issue_cache_freshness_probe.py` / `coordination_probe.py` / `.aria/probes/*.py`) 或为内联 shell+`python3 -c`。§1.3 的 check 要做「抽取 token → 调归一 → 分级」**必然需要一个实现宿主**, Impact 表零覆盖;
  - Impact `:419` 的 SC 分配逐字「`skills/state-scanner/tests/` (既有宿主) \| SC-1~10, 14, 15, **20**」; audit-engine tests 行 (`:426`) 无 SC 清单; 行为类 fixture 覆盖 SC-11/12/21。**SC-13 在整张表中没有任何宿主**;
  - §1.3 `:72` 只写「可被**前置 Spec 的归一**解析」, 未点名 `collision.py::normalize_linked_issue` —— 而该函数**已在 `origin/master:178` 公开可用** (实读确认, 非私有下划线名)。
- **问题**: R1/M3 的「归一 API 职责真空」已被现实关掉, 但 Spec 没有接收这个事实 ⇒ 实现者仍可能在 check 脚本里**复写**一份归一 (双实现漂移, 正是前置 Spec 的 S5 刚揭示的病换个位置复发)。而 SC-13 无宿主 = R1/C4 判过的同一形状 (SC 挂在不存在的宿主上) 的静默版本 —— 这次不是挂错宿主, 是**没挂**。
- **建议修法**: Impact 补 check 实现宿主一行 (建议 `aria/skills/state-scanner/scripts/linked_issue_field_probe.py`, 与 `coordination_probe.py` 同族, 使其随 plugin 分发 —— 这也顺带部分解 R2-TL-M6); §1.3 逐字点名 `from lib.collision import normalize_linked_issue`; SC-13 在 Impact 的 SC 分配表里给出宿主。

#### R2-TL-M6 — R1/M4 的 `standards/openspec/templates/proposal-minimal.md` 一半仍未回补 (Impact 表零 `standards/` 变更行)

- **category**: cross-repo-coverage / rule-3
- **scope**: `proposal.md:70` (§1.1) · Impact `:422` (spec-drafter) / `:429` (state-checks.yaml)
- **证据**: Impact 表 grep `standards/` 零命中 (全文两处 `standards/` 都在 rule6_note 引 `conventions/skill-benchmark-exemption.md`, 属**引规范**非变更面); 实读 `standards/openspec/templates/proposal-minimal.md:1-20` —— 字段仍只有 `Level` / `Status` / `Created`, **无「关联 Issue」**; 该文件是 Level-2 proposal 的模板 SOT (`standards/openspec/templates/README.md` 明列复制路径)。
- **问题**: 与 R1/M4 逐字相同 —— (a) 走 standards 模板复制路径的项目照样产出无字段 proposal; (b) §1 `:81` 自证「无机械回声的义务会退化」, 而那个机械回声 (`.aria/state-checks.yaml`) 是**项目级 opt-in、不随 plugin 分发**, 该论证在 Aria 仓之外全线失效; (c) proposal 文档格式属 standards 域, 漏改触 Rule #3。
- **建议修法**: Impact 补 `standards/openspec/templates/proposal-minimal.md` (必要时含 `standards/openspec/project.md` 字段说明); **或**显式成文「本 Spec 的机械回声只覆盖 Aria 仓, 其余项目仅有模板 (承认会退化)」并记入 §6 —— **不要用一般性的「机械校验」措辞掩盖覆盖边界**。

#### R2-TL-M7 — §2 的 NEW-01 段**自陈**「该已知限须写进 §6 缺口表」, 而 §6 表无该行; 连带 R1/M5 的 `:1230` 门控仍全文未提

- **category**: internal-contradiction / gap-table-completeness
- **scope**: `proposal.md:103` ‖ §6 `:270-276`
- **证据**: `:103` 逐字「此时 track-id 走 §2.1 的回落形 ...; 主机制对该轨**不产生输入** —— **该已知限须写进 §6 缺口表**」; §6 表实读 4 行 (双方未 claim 未 push / 跳过 A.1 直调 spec-drafter / `coordination.enabled=false` / legacy 轨), **无「本轨无关联 issue」行**。
  实读 `phase1_gate.py:1230` `if args.linked_issue:` 门控 `:1231-1238` 整块 ⇒ 不传该参数时输出 dict **根本没有** `linked_issue_overlap` 键 (不是空列表, 是键缺失), `--include-terminal` 亦静默无效。Spec 全文对 `:1230` 零提及。
- **问题**: 按 §1 自己的统计, 「无关联 issue / 写 `无`」是**多数路径** (13-14/147 有字段) ⇒ 这是量级最大的缺口, 而 §6 独缺它。且键缺失最易被消费面渲染成「无碰撞」—— 正是 §2.5 自己禁止的「零证据当正证据」。**Spec 明写要做而未做**, 属可机械核对的自相矛盾。
- **建议修法**: §6 增一行「本轨无关联 issue (含显式 `无`) \| 无界 \| 无 (§4 探针需另给输入才部分覆盖)」; §2.3/§2.5 明确该分支措辞为「本轨无关联 issue, 未做同 issue 核实」而非「无碰撞」; §2.4 传递链补一句「`--include-terminal` 在无 `--linked-issue` 时静默无效 (`:1230` 门控)」。

#### R2-TL-M8 — §2.5 的降级契约仍只覆盖 fetch 一条腿, `phase1_gate.py:1236-1238` 的 `except → out["linked_issue_overlap"] = []` 未纳入 (R1/M6 一字未动)

- **category**: fail-soft-contract
- **scope**: `proposal.md:199` (§2.5 第二条) · SC-10 `:368`
- **证据 (逐字实读 `cb6bd5d`)**:
  ```
  1236        except Exception as exc:  # fail-soft: overlap advisory must not break the gate
  1237            logger.warning("phase1_gate: linked_issue overlap check skipped (%s)", exc)
  1238            out["linked_issue_overlap"] = []
  ```
  该赋值发生在 `out = _gate_result_to_dict(result)` (`:1226`) **之后**, 是 `out` 上的独立键 ⇒ 把 `GateResult.error` 置 `"fetch_degraded"` (`:210` docstring 确已预留该 token, 实读 grep 全文该字面量**仅此一处**且从无 `error=` 赋值 ✅) **在结构上无法覆盖这条路径**。§2.5 `:199` 与 SC-10 `:368` 均未动。
- **问题**: 与 §2.5 自己写的「零证据不得当正证据」直接互斥 —— overlap 计算异常时消费面拿到 `[]`, 与「真没人在做」逐字节相同, 只留一条 `logger.warning`。memory `fix-recurs-in-fallback`: 要治的病在既有 except 兜底路径上原样存在, 而修复条款只覆盖了 fetch 一条腿; 且「有记录」≠「有路由」—— 无人消费的 `logger.warning` = 静默。
- **建议修法**: §2.5 把降级契约从「fetch 降级」扩为「**任何**使 overlap 无法核实的降级」, 并指明需要一个 **`out` 层**可见标记 (新增 `linked_issue_overlap_error`, 或该键置 `null` 而非 `[]` —— 后者须评估既有 Phase B 消费方); SC-10 增子例「`read_claims` 抛异常 ⇒ 消费面渲染『未能核实』」(现状 `[]` 必红)。

#### R2-TL-M9 — rule6_note 的「覆盖外」档把 `audit-engine` 与另两个 skill 并列, 但点名行为 (a)(b)(c) **无一条是 audit-engine 的新行为**, 且 `ab-suite/audit-engine.json` **不存在** ⇒ 按判据表「缺一照跑」该档不成立

- **category**: rule-6-compliance / gate-authority
- **scope**: `proposal.md:329-332` (rule6_note 覆盖外档) · Impact `:431`
- **证据**:
  - `:329` 逐字:「**`phase-a-planner` / `spec-drafter` / `audit-engine` 三处 SKILL.md** ... 落判据表**第三行「套件覆盖外」**, **三条缺一不可**」;
  - `:330` 的点名行为逐字: 「(a) A.1 起草前必调 phase1_gate 且传 `--linked-issue`; (b) overlap 非空时经 `AskUserQuestion` 请裁而非自行放行; (c) fetch 降级时按「未能核实」而非「无碰撞」」—— **三条全是 A.1 / phase1_gate 侧行为**, audit-engine 的新处方性行为 (§4「per-round 入口探针; Convergence `:84-111` 与 Challenge `:113-144` **两段都要改**」) **零点名**;
  - `:331` 逐字「上述三条各一个 eval」⇒ 定向 fixture 也只有 3 个, 对应 (a)(b)(c), audit-engine 无 fixture;
  - 实读 `ls aria-plugin-benchmarks/ab-suite/`: **无 `audit-engine.json`** (37 项中不含);
  - 对照实读: `phase-a-planner.json` (2 evals) ✅ / `spec-drafter.json` (2 evals) ✅ / `state-scanner.json` (11 evals, v1.5.0, 11 个 eval 名实读**均与 heartbeat 无关**) ✅ —— **Spec 对这三者的断言全部属实**, 问题只出在 audit-engine。
- **问题**: CLAUDE.md Rule #6 判据表第三行的三要件是「点名行为 + 建可证伪定向 fixture + 套件缺口开 issue (**缺一照跑**)」。audit-engine 缺前两件 ⇒ 按规则本体回落「照跑」, 而无套件可跑 ⇒ 实际结果是**该 skill 的处方性变更既不跑 AB 也无 fixture**。这落在 Rule #10 的管辖内 (已启用闸门不得由 AI 自行降级), 且 `standards/conventions/skill-benchmark-exemption.md` 的封闭白名单四类无一适用。
- **建议修法**: 二选一并写死 —— (i) 为 audit-engine 点名行为 (建议:「每轮审计入口必跑 `sibling_spec_probe.py`, Convergence 与 Challenge 两段对称」) + 建对应定向 fixture + 开套件缺口 issue (与 `aria-plugin#117`/`#127` 同族); 或 (ii) 显式上呈 owner 请裁该 skill 的 benchmark 处置。**不要**让它停在现在这个「列在覆盖外档但三要件都没有」的状态。

#### R2-TL-M10 — rule6_note 新增的「描述性」档以 **SC-9** 作 substitute, 但 SC-9 断言的是 SKILL.md **散文行为** (§2.5 自陈)、被标 (代码) 并挂 `state-scanner/tests/` —— 违反本 Spec 自己的「验证面分层」; 且其判定输入 `coordination` 键**实测未在 `DEFAULTS.json` 注册**

- **category**: rule-6-substitute-validity / verify-predicate-inputs
- **scope**: `proposal.md:333` (config-loader 描述性档) · SC-9 `:367` · 验证面分层表 `:343-348` · Impact `:419`/`:428`
- **证据**:
  - `:333` 逐字:「⇒ 纯**描述性**内容, 落判据表**第一行「描述性」**; substitute = **SC-9** (状态类结构化测试 ...), 不需 AB」;
  - SC-9 `:367` 逐字: 「**SC-9 (代码)** \| `coordination.enabled == false` \| A.1 **零调用**, 不写 claim, 不推远端 \| 无条件调用必红」, Impact `:419` 把它挂在 `skills/state-scanner/tests/`;
  - **但 §2.5 `:198` 自己写着**:「`phase1_gate` **本身不读 config**, **skip 判断在调用方 SKILL.md 层**」⇒ 「A.1 零调用」是一条**AI 是否遵守 SKILL.md 指令**的断言, 不是可在 `state-scanner/tests/` 里机械断言的代码状态;
  - **本 Spec 自己的验证面分层表** `:343-348` 逐字: 行为类「**只能由 eval 覆盖, 不冒充结构化测试**」;
  - **判定输入不存在**: 实读 `grep -n coordination skills/config-loader/DEFAULTS.json` **零命中**; 默认值只活在散文 (`state-scanner/SKILL.md:149`「缺省即 true」/ `layer-l-integration.md:12`)。Impact 表有 `config-loader/SKILL.md` 一行, **无 `DEFAULTS.json`**。
- **问题**: CLAUDE.md Rule #6 判据表第一行的 substitute 要求是「**SC 级 baseline-failing 结构化测试**」。SC-9 既非结构化 (行为断言) 又缺 canonical 判定输入 (键未注册 ⇒ 缺键默认在本仓已有两个相反先例, R1/CR-M8 原判) ⇒ substitute **不成立**, 该档应回落「照跑」或另建定向 fixture。这是 memory `verify-predicate-inputs-exist` 的形状: 注意力放在「归档到哪一档」上, 没问「它要判的输入真的存在吗」。
- **建议修法**: (i) SC-9 拆两条 —— 结构化那半「`config_loader` 读到 `coordination.enabled == false` 时返回 false 且有 canonical 默认」(挂 `state-scanner/tests/`, 需先在 `DEFAULTS.json` 注册该键, **补进 Impact**), 行为那半「A.1 零调用/不写/不推」改标 (行为) 并建定向 fixture; (ii) rule6_note 的 config-loader 档 substitute 改指向 (i) 的结构化那半, 或改判「照跑」。

---

### 🟡 Minor

| # | scope | 内容 |
|---|---|---|
| **R2-TL-m1** | Impact `:421`/`:423` · SC 全表 | C1 落版把两处 `allowed-tools` 写进 Impact, 但**无任何 SC / 机械断言**守护它。R1/C1 建议 4 (「断言两个落点 frontmatter 含所需全部工具」, 现状必红) 未采纳, 也未说明为何不采。这是唯一能机械挡住本类回归的验证面 —— 而本类回归 (机制挂在无权限宿主上) 是 R1 五席里 4 席独立命中的那条 |
| **R2-TL-m2** | `proposal.md:3-8` | **本 Spec 头部六个字段仍无「关联 Issue」** (dogfood 缺口, R1/KM+CR 已点名一次)。对比: 前置 Spec `linked-issue-normalization` 本轮已把该字段补成规范的 `无` (实读确认) —— 姊妹 Spec 做到了, 本 Spec 没做。§1.3 的 check 上线后它会是自己的第一个 warning |
| **R2-TL-m3** | `proposal.md:236` | §3「口径待定」仍写两个标识 (`owner-container` vs claim container 段), 实读为**三**个: track_id 的 uuid 段 (§2.1 明定不看 label) / `claim.container` = `claim_lifecycle.py:150` `container=resolved.container_id` ← `identity.py:222` **label 优先** / handoff `owner-container`。今天两容器 label 全空故后两者巧合相同; 一旦有人按 `identity.py` 模板设 label (正是 §2.1 整个论证的前提), 三者分叉 |
| **R2-TL-m4** | `proposal.md:257` ‖ SC-18 `:381` | §4 exit code 契约内部仍不齐: `:257`「非 0 **仅**用于探针自身失败」 vs SC-18「探针 fetch 失败 / **无远端** ⇒ exit 非 0」。无 `enforced_remotes` 是合法环境状态而非探针故障; 且 §4 明写「不阻断」, 非 0 的消费者未定义 |
| **R2-TL-m5** | Impact `:427` · `layer-l-integration.md:45` | Impact 只点名该活文档的「闸门仅在 Phase B 触发」一处。同文件 `:45` 逐字仍是「`heartbeat` \| `phase-b-developer` mid-cycle \| **每 10min** \| `lib/claim_lifecycle.py::**update_heartbeat()**`」—— 实读全仓 grep `update_heartbeat` **仅此一处文本, 函数不存在**。C2 落版后该行的**调用方 / 节律 / 函数名三项全与新设计相反**, 而 Impact 的修改理由把编辑范围钉在了另一处 (memory `cross-doc-claim-verify-at-target`) |
| **R2-TL-m6** | `proposal.md:58` (⭐段) · `:79` (§1.4) · D1 `:314` · 非目标 `:405` | 语料统计已陈旧: Spec 记「141 篇 / 13 篇 / 9% / 存量 **128** 篇无字段」, **本轮实测 147 / 14 / 9.5% / 133**。**结论方向不受影响** (9% 仍成立), 但 §1.4 与非目标把「128 篇」当作 grandfather 集的**具体规模**引用 ⇒ 该集合的边界描述已与现实不符 (memory `past-summary≠measurement`)。建议改为「**存量所有无字段者**」的集合式表述, 免去随语料增长而复发 |

---

## 经本轮实读确认**正确**的部分 (R3 免重复)

1. **✅ owner 裁定原文逐字恢复属实** —— 与 `git show 86540f2:.../proposal.md:150` (C2) 与 `:214` (C1) **逐字节比对一致**, 无删改。上一轮的 major-3 (转述偏差) **确已修复**;
2. **✅ `--sweep-stale` 与 `STALE_TTL` 无关的事实订正完全成立** —— `gc.py:341` `stale_ttl_seconds: int = SWEEP_TTL` ✅ · `release_gate.py:141` `sweep_stale_active(repo, now=ts)` 未传覆盖 ✅ · `release_gate.py:225` help 用词确实不准 ✅ · `reconcile.py:154-163` `_is_stale` 用 `STALE_TTL` ✅ —— **这是本轮质量最高的一条自查**;
3. **✅ 前置 Spec 合并状态断言全对** —— `git merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立 ✅; 合并提交 `ca52d1c` (v1.67.0) `2026-08-23T09:14:07Z` ✅; `linked_issue_overlaps` **三参数签名未变** ✅; 新增 `normalize_linked_issue()`(`:178`) / `_linked_issue_matches()`(`:219`) 两 helper ✅; 行号下移 `_TERMINAL` `:210→:268` ✅ / `:207-208→:265-266` ✅ / `:219-220→:278-279` ✅ / `linked_issue_overlaps` `:230-234` ✅ —— **「事实断言逐条实读清单」#3/#4/#5/#6/#16 全部复核通过**;
4. **✅ 事实清单其余条目复核通过** —— #1/#2 (两处 frontmatter 逐字 + `user-invocable`) ✅ · #7 (`:1232` 是 `read_claims`, 调用在 `:1233`) ✅ · #8 (`heartbeat` @ `:178`) ✅ · #9 (`release_claim_by_track` @ `:377`) ✅ · #10 (`:425`) ✅ · #11 (`get_container_id` @ `:191`, label-first `:222`, hostname `:242`) ✅ · #12 (`fetch_degraded` 仅 docstring, 从无赋值) ✅ · #13 (`constants.py:36`/`:51`/`:32`/`:28`) ✅ · #14 (三处 `STALE_TTL`/`SWEEP_TTL` 混用描述) ✅ · #15 (`SKILL.md:149` + `layer-l-integration.md:15`) ✅ · #17 (`_run_gate_impl` `:335`–`:1032`, 区间内 grep 命中 0) ✅ —— **17/17 逐条复跑, 无一条虚报**;
5. **✅ Impact 表的两条新补行属实且必要** —— `lib/collision.py` (C6 落地必需) ✅ · `phase1_gate.py --heartbeat-only` (C2 (ii) 的具体入口) ✅; `constants.py` 行列的三处过期注释 `:40`/`:43-44`/`:50` **逐字实读全部命中** ✅;
6. **✅ SC-20 是真 baseline-failing 断言** —— 现状 `STALE_TTL=1800`, 23h=82800 > 1800 ⇒ `_is_stale` 返回 True ⇒ 必红 ✅ (缺陷在断言**形状**不在极性, 见 M1);
7. **✅ AB 套件事实断言全对** —— `phase-a-planner.json` / `spec-drafter.json` 均实存且**各 2 eval case** ✅; `state-scanner.json` 实存 (11 evals, v1.5.0) 且 11 个 eval 名无一涉及 heartbeat ⇒「当前 eval case 未覆盖此新分支」✅; 引用的 `880060d` 提交实存且正是 state-scanner AB 迭代 ✅。**⇒ §3 的「请 owner 复议 (b)」中「两套件实存 ⇒ 应照跑」的核实结论与 owner 原话字面一致, 本席确认无需另行复议**;
8. **✅ §4 引用的 audit-engine 事实全对** —— `audit-engine/` 实读只有 `references/` + `SKILL.md`, **零 `scripts/` 零 `tests/`** ✅; `SKILL.md:85` 逐字「Round 1 启动前**一次性**」✅; `execution-modes.md` Convergence @ `:84` / Challenge @ `:113` / 全文 144 行 ⇒ `:84-111` 与 `:113-144` 两段边界成立 ✅; `DEFAULTS.json:124-128` `adaptive_rules.level_3 = "challenge"` ✅;
9. **✅ 闸门状态段 (Rule #10) 论证成文正确** —— 实读 `.aria/config.json`: `audit.checkpoints.post_spec = "convergence"` ✅ · `state_scanner.coordination.enabled = true` ✅; 四类封闭白名单逐条判否, 无自我豁免, 「AI 不预判 R2 裁决」措辞正确;
10. **✅「请 owner 复议」两段的姿态正确** —— 发现 owner 裁定理据被实读证伪时**上呈而非自行改判**, 并把上一轮的越权改写显式撤销; 这是本 Spec 三轮以来第一次做对这件事。(其中 §2.2 那段的**内容**有事实不全 → M1; §3 那段的内容**经核实无误**, 不构成 finding。)

---

## scope_ok

**true。** 全部 finding 均落在被审对象 (`proposal.md` 本身及其对既有代码/文档的事实断言) 内; 无一条要求改本 Spec 非目标范围内的代码; 无 OUT_OF_SCOPE 项。审计对象包含本轮新写的 C1/C2 落版段、「请 owner 复议」两段、事实断言逐条实读清单、Impact 表、rule6_note —— 均已覆盖。

## 一句话结论

**REVISE** —— 本轮把 owner 裁定逐字恢复、17 条事实断言逐条复核无一虚报、C4/C5/C6 三条订正全部属实, **执行忠实度是三轮最高的一次**; 但 R1 的 5 条 major 一字未动 (§4 谓词 / `standards/` 模板 / §6 缺口表 / fail-soft `[]` / 两条 minor), 新写的四段又各自引入新缺陷 (占本轮 major 的 50%, 已到 memory `marginal-return-negative` 的拐点), 而最重的一条是 §1 把 R1/C3 **诊断得完全正确却把承重规则 defer 出 Spec**, 且自给候选实测只救 4/13 —— **建议 R3 换执笔者而非同一人再加一轮。AI 不预判裁决。**
