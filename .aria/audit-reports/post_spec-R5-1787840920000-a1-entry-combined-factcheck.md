---
checkpoint: post_spec
round: 5
role: factcheck
verdict: REVISE
scope_ok: true
counts:
  combined: { critical: 0, major: 3, minor: 19 }
  a1-entry-claim-duplicate-work-guard: { verdict: REVISE, scope_ok: true, critical: 0, major: 2, minor: 11 }
  linked-issue-field-availability: { verdict: REVISE, scope_ok: true, critical: 0, major: 1, minor: 5 }
  sibling-spec-probe: { verdict: PASS, scope_ok: true, critical: 0, major: 0, minor: 3 }
---

# post_spec R5 — 独立事实核验腿 (三份 Spec 联审)

> **镜头**: 只判「文档里的外部事实断言是真是假」。**不做**设计评价、不判方案优劣、不评收敛质量。
> **基线**: 主仓 `b0c16ff` (工作树干净) · aria 子模块 `d50f9c3` · 语料对照 SHA `cc1bdef`。
> **被审对象**: `openspec/changes/{a1-entry-claim-duplicate-work-guard,linked-issue-field-availability,sibling-spec-probe}/proposal.md` + 三份 `.aria/audit-reports/*-audit-trail.md`。
> **未修改任何被审文件。**

## 0. 方法与自纠

按 owner 交办的两条方法纪律执行:

1. **凡标「逐字」「原文」「docstring 逐字」的引文, 一律用不带过滤的连续输出复读** (`git show <sha>:<path> | awk 'NR>=A && NR<=B {printf "%d|%s\n", NR, $0}'`), 不用 `grep` 取证。
2. **比对的是「断言说的内容」与「那行实际写的内容」**, 不是「那行存不存在」。

**本席自身的一次误判留痕 (方法实证)**: 核 a1 审计轨 §5 时, 我先用 `grep -oE '^\| *[0-9]+ '` 数表行, 得 17 行, 据此几乎写下一条 Critical「母 Spec 宣称 34 行、实际 17 行, 6 个交叉引用 (#22/#26/#28/#29/#30/#33) 全悬空」。**该结论是假的** —— 表内 #18–#34 用 `| **25** (新) |` 粗体格式, 被我的正则过滤掉了。改用 `sed -E 's/^\| *\*{0,2}([0-9]+)\*{0,2}.*/\1/'` 重数得 **34 行齐全**, 6 个引用**全部 resolve**, 内容与我独立实读的结果一致。
⇒ **这正是本席存在理由第 2 条 (`grep` 只能定位不能取证) 在核验者自己身上的复现。** 记于此, 供 owner 判本席其余结论的可信度基线。

**核验规模**: 三份 Spec + 三份审计轨的 `文件:行号` / 数字 / 逐字引文断言, 逐条实读 **约 130 条**;其中标「逐字」的引文 **31 条**逐条连续复读;实跑复现 **7 处** (两条 argparse / `无`-`无` overlap / unknown sentinel / placeholder overlap / E0 规则原型全语料 / 层 0 三臂对照)。

---

## 1. 我实读证伪了哪些断言 (findings)

### 1.1 a1-entry-claim-duplicate-work-guard — **2 Major / 11 Minor**

---

#### 🔴 A-M1 (Major) — `:238` 标「逐字」的引文出自另一个文件

**断言原文** (`proposal.md:238`):
> 实读 `skills/state-scanner/scripts/coordination_probe.py:4-25`: 它是**反死代码探针**, 只数 `.aria/coordination-telemetry.jsonl` 里 `_source=="production"` 的**近期** `run_gate` 记录, 而该分区「written only by the CLI production path (`_main` → `_gated` with `_source="production"`)」(**逐字**)。

**实跑**:
```
$ git -C aria show d50f9c3:skills/state-scanner/scripts/coordination_probe.py > /tmp/.../coordination_probe.py
$ grep -n "written only by the CLI production path" /tmp/.../coordination_probe.py
(无输出, rc=1)
$ grep -n "written only" /tmp/.../coordination_probe.py
18:  The production partition file is written only when ``_source=="production"``,
$ git -C aria grep -n "written only by the CLI production path" d50f9c3 -- .
d50f9c3:skills/state-scanner/scripts/phase1_gate.py:1048:    written only by the CLI production path (:func:`_main` → :func:`_gated`
```

**判定: 不一致。** 该「逐字」串在 `coordination_probe.py` **全文不存在**;真身在 **`phase1_gate.py:1048`** (`run_gate` 的 docstring)。`coordination_probe.py:4-25` 表达的是**同义的另一句** (`:18-21`: "The production partition file is written only when ``_source=="production"``, and after the audit tightening that value is reachable ONLY from the private ``phase1_gate._gated`` (invoked with ``_source="production"`` by exactly one call site, the CLI ``_main``)")。

**影响**: 实质结论 (探针只认 production 分区 ⇒ `--heartbeat-only` 复用同一产线会把 enabled check 变恒绿) **独立复核为真**, 由 `coordination_probe.py:18-21` 支持。缺陷只在**逐字引文的出处标错文件**。但这条正是文档自己反复援引「该行存在 ≠ 该断言属实」纪律的段落, 且 R3/TL-M2 声称「主控实读证实」。
**grep 定位**: `written only by the CLI production path`

---

#### 🔴 A-M2 (Major) — SC-2 的 R4/C-1 订正只修了一半, 承重负控臂仍指向文档明说不存在的 `compose`

**断言原文** (`proposal.md:642`, SC-2「怎么会红」格):
> **R4/C-1 订正 —— 主控担责**: 上一版写「必须由 §2.1a 的 compose 函数派生」, 而 §2.1a `:164` 逐字写着「**本 Spec 不新增拼接函数**」, **全文 grep `compose` 仅命中 SC-2 自身** ⇒ **SC-2 引用了一个本 Spec 明说不存在的函数** …… **订正后**: 夹具手写字面串是**允许且必要的** …… 且断言**两层**: (i) 双方 overlap 各含对方; (ii) **把 compose 的 container 段置空重跑同一夹具 ⇒ 双方 overlap 必须变空** (负控)。**缺 (ii) 的实现视为未满足本条**

**实跑**:
```
$ awk 'NR==164 {print}' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
**本 Spec 不新增拼接函数** —— 新增代码落点只有 `lib/identity.py` 的直取 `uuid` accessor …
$ grep -n "compose" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
171:> (R3 主控还一度把 SC-2 的夹具约束写成「必须由 §2.1a 的 compose 函数派生」, 而本节明说不存在该函数 ——
642:| **SC-2** | …… (ii) **把 compose 的 container 段置空重跑同一夹具 ⇒ 双方 overlap 必须变空** (负控)……
```

**判定: 两处不一致。**
1. **订正残留**: 同一格里, 前半刚判定「SC-2 引用了一个本 Spec 明说不存在的函数」并改成「手写字面串」, **后半 (ii) 仍写「把 `compose` 的 container 段置空」** —— 实现者写这条**承重负控臂** (缺它视为未满足本条) 时, 字面上仍找不到可 import 的 `compose` 对象。⇒ 被点名的同一形状 (「把 SC 挂在不存在的宿主上」) 在它自己的修复里残留了一半。这与 memory `feedback_fix_recurs_in_its_own_fallback_path` / `fix-the-class` 同形。
2. **计数断言为假**: 「全文 grep `compose` 仅命中 SC-2 自身」在 `b0c16ff` 上是 **2 命中** (`:171` K3 块 + `:642`)。`:171` 与 `:642` 同属 2026-08-27 R4 清账批次。

**建议的最小订正**: (ii) 改为「把**夹具里手写的那两个 track-id 串的 container 段**置空重跑同一夹具 ⇒ 双方 overlap 必须变空」。
**grep 定位**: `把 compose 的 container 段置空`

---

| # | 严重度 | 位置 | 断言原文 (摘) | 实跑命令 | 实际输出 | 判定 |
|---|---|---|---|---|---|---|
| **A-m1** | Minor | `:575` (D4) | 「§2.2 **`:188`** 与 D16 已统一而本行残留未同步」 | `awk 'NR==188' …/proposal.md` | `**处置 = 统一到一个串, 三处逐字节复用** (owner 的 U-3 选项 A)` — 这是 **§2.1b**;§2.2「**以「增并存变体」为准**」在 **`:208`** | ❌ 不一致 (内部行号) |
| **A-m2** | Minor | `:359` | 「`:260` 逐字「母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**」」 | `grep -n "不视为对本 Spec 的违反" openspec/archive/2026-08-23-linked-issue-normalization/proposal.md` | `259:  > ⇒ **D6 与 §接口面 …**: 本 Spec 不改签名; 母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**。` | ❌ 行号差 1 (`:259` 非 `:260`);**引文本身逐字正确**;`:257` 逐字正确 |
| **A-m3** | Minor | `:363` | 「`_run_gate_impl` (`:335` 定义, **至下一个顶层定义 `run_gate` `:1032` 前**)」 | `grep -n "^def " phase1_gate.py` | `335:def _run_gate_impl(` → 下一个顶层 def 是 **`950:def _telemetry_path(`**, 非 `1032:def run_gate(` | ❌ 区间断言为假 (虚增 ~82 行)。结论「grep 命中 0」独立复核**为真** (`awk 'NR>=335&&NR<=949' \| grep linked_issue_overlaps` 无输出;全 aria 生产调用点只有 `:1233`)。**该行本身是「R1 rework 核验 minor-4 订正」** |
| **A-m4** | Minor | `:235` (K7) | 「`basicConfig` **只在** `scan.py`」 | `git -C aria grep -n "basicConfig" d50f9c3 -- .` | `skills/issue-triage/scripts/triage.py:290` **与** `skills/state-scanner/scripts/scan.py:470` | ⚠️ 总体未写明: 限定在 `skills/state-scanner/` 内**为真** (只有 scan.py:470);全 aria 为假。判**不可比**而非推翻 —— 结论 (phase1_gate subprocess 的 `logger.*` 全丢) 不受影响 |
| **A-m5** | Minor | `:789` (FIX-04) | 「全文 grep `A1_SWEEP_TTL` = **0 命中**」 | `grep -c "A1_SWEEP_TTL" …/proposal.md` | `1` | ❌ 自指式 grep: 唯一命中就是 FIX-04 那行断言自己。substance (设计里无该分档) 为真 |
| **A-m6** | Minor | `:210` | 「docstring **逐字**记载 ……「`release_claim` locates by `(container, session)`, but **a later invocation** runs with a **FRESH session_id**……」」 | `awk 'NR>=387&&NR<=393' claim_lifecycle.py` | `:388` = `locates by ``(container, session)``, but a later **ship/close** invocation` | ❌ 删去 `ship/close` 未加省略号标记。其余逐字正确 |
| **A-m7** | Minor | `:56` | 「B.0 块起于 `:86` … **至 `:96` (`skip_if:` 注释段起始一带)**」 | `git -C aria show d50f9c3:skills/phase-b-developer/SKILL.md \| awk 'NR>=94&&NR<=98'` | `95: skip_if:` / `96: # 可判定谓词 (review I5 …` | ⚠️ `skip_if:` 在 `:95`;`:96` 是其下注释。「一带」已作对冲。`:86` / `:91-93` / 标题无 `B.0` **全部逐字正确** |
| **A-m8** | Minor | `:743` | 「§3.2 (`:129` 起, 现枚举 reader 侧 unknown 行为 **5 条**于 `:133-139`)」 | `git -C aria show d50f9c3:skills/state-scanner/docs/coordination-ref-schema.md \| awk 'NR>=129&&NR<=142'` | `:129` = `### 3.2 Reader downgrade on unknown version` ✅;5 条为 `:133-140` (第 5 条跨到 `:140`) | ⚠️ 区间末端差 1 行 |
| **A-m9** | Minor | `:245` | 「实读 `:1043` **逐字** —— `success: bool  # Reflects FETCH 1 (branch heads, load-bearing)`」 | `git -C aria show d50f9c3:…/state-snapshot-schema.md \| awk 'NR==1043'` | `success: bool                   # Reflects FETCH 1 (branch heads, load-bearing);` | ⚠️ 逐字引文省略行尾 `;` 并压缩对齐空白。`:1056` / `:1061-1064` 逐字正确 |
| **A-m10** | Minor | `:92` | 「原 §1 的四条…与 R1 editlist **FIX-06/07/08**…整体由 [`linked-issue-field-availability`] 承担」;`:792` 「FIX-07 …**⛔ 随 §1 迁出**」 | `grep -c -- "FIX-07" openspec/changes/linked-issue-field-availability/proposal.md` | **0** (对照: `FIX-06` = 3, `FIX-08` = 2) | ❌ **跨文档承接不实**: 子 Spec 全文零处提及 FIX-07。substance 已承接 (check 作用域 → D5;回填 6 篇 → D6 + O-1), 但缺 traceability 锚点。⚠️ FIX-07 标 **⭐ 承重**, 且母 Spec §未做/存疑 #6 正是要求 R3 跨 Spec 联审这一点 |
| **A-m11** | Minor | 审计轨 `:131` / `:136` | (格式) | `awk 'NR>=125' .aria/audit-reports/a1-entry-claim-audit-trail.md` | §5 表在 `:131` / `:136` 有空行 ⇒ markdown 上把 **#31–#34 断成无表头碎片表** | ⚠️ 渲染缺陷, 内容齐全 (34 行全在) |

---

### 1.2 linked-issue-field-availability — **1 Major / 5 Minor**

---

#### 🔴 L-M1 (Major) — §Why 的「逐字 grep 输出」在任何已提交 SHA 上都不成立, 且被同文件 D2 自我推翻而未同步两处

**断言原文** (`proposal.md:55-59`):
> **18 行全部落在三份「讨论该字段」的 Spec 里** …… 其中母 Spec 的那条最典型 —— 行首三个空格 + `> > ` (blockquote 深度 2), 是它旧 §1 里被引用的示例:
> ```
> openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:88:   > > **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; ...)
> ```

以及 `:524` (SC-1「怎么会红」格): 「**(c) 的形状在真实语料上有实例: 母 Spec `:88`**」。

**实跑** (逐 commit 追踪, 不带过滤):
```
$ for sha in 027a50f 13dd8fe 978195a b0c16ff cc1bdef; do echo "=== $sha ==="; \
    git show $sha:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md | grep -nE '\*\*关联 Issue\*\*'; done
=== 027a50f ===   12: > **关联 Issue**: `无` …   81: ⇒ 在**在制**语料 …   677: | FIX-19 …
=== 13dd8fe ===   12 / 81 / 678
=== 978195a ===   12 / 81 / 678
=== b0c16ff ===   12 / 81 / 804
=== cc1bdef ===   75:   > > **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; ...)

$ awk 'NR==88' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md
## What Changes
$ grep -nE '^\s*> > \*\*关联 Issue\*\*' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md ; echo rc=$?
rc=1
```

**判定: 不一致 (三重)。**
1. 母 Spec 的那条 depth-2 示例行**真身是 `cc1bdef:75`**, 不是任何文件的 `:88`;
2. 自 **`027a50f`** (三份产物落盘那一 commit, 即本 Spec 声明的「三份拆分产物全部落盘后」状态) 起, 母 Spec 全文 depth-2 `> > **关联 Issue**` 命中 = **0** —— 该示例随 §1 迁出而消失;
3. 当前 `:88` = `## What Changes`。

**内部矛盾**: 同一文件的 **D2 (`:481`)** 已把这条订正为「该引用现已悬空 …… 真身是**迁出前**的 `cc1bdef:75` …… **稳定锚点改用**「本文件 §Why 的 grep 输出 + `cc1bdef:75`」」。但 **§Why `:58` 本身**与 **SC-1 `:524`** 都未同步 —— 而 D2 恰恰把 §Why 的 grep 输出指定为新的稳定锚点, 那段输出本身却是错的。
**影响**: SC-1 的 (c) 臂声称「在真实语料上有实例」并给出锚点, 该锚点不存在 ⇒ A.2 写夹具时按此去取原文会取到 `## What Changes`。
**grep 定位**: `proposal.md:88:   > > **关联 Issue**`

---

| # | 严重度 | 位置 | 断言原文 (摘) | 实跑命令 | 实际输出 | 判定 |
|---|---|---|---|---|---|---|
| **L-m1** | Minor | `:50-52` | 松→严差额按文件归属 = `3` 母 Spec / `11` 本文件 / `4` 探针 Spec | `grep -rnE '\*\*关联 Issue\*\*' --include=proposal.md openspec/ \| grep -vE ':[0-9]+:> \*\*关联 Issue\*\*' \| cut -d: -f1 \| sort \| uniq -c` (当前) 及同法在 `027a50f` | 027a50f: **2 / 11 / 7**;当前工作树: **2 / 12 / 8** | ❌ 母 Spec 那格 (`3`) 在**任何** commit 上都不成立 (它只有 `:81` `:677/:804` 两条非严格命中);探针 Spec 那格 (`4`) 亦不成立。仅 `11` 在 027a50f 复现 |
| **L-m2** | Minor | `:61`, `:64-67` | 「多出的 2 行都在本文件内 (**`:65` / `:86`**), 是写在围栏代码块里的示例」+ 逐字 grep 输出块 | `grep -nE '^> \*\*关联 Issue\*\*:' …/linked-issue-field-availability/proposal.md` (当前与 027a50f 两次) | 两次均为 **`:6` / `:95` / `:116`** | ❌ 行号偏 30 行 (自指漂移: 写下 §Why 那 30 行本身把它们推下去了)。**结论为真** —— `:95` 与 `:116` 均在围栏内, 严谓词确实过计 2 行, 19→17 的算术复现 |
| **L-m3** | Minor | `:306` | 「(其 **`:103`** 实测「canonical 合规 = 0 行」与本 Spec 的 14/14 一致)」 | `awk 'NR==103' …/sibling-spec-probe/proposal.md` | `**层 1 分派 — 姊妹四态 × 本 Spec 的层归属 …**` — 该实测在 sib **`:169`** | ❌ 跨文档行号错。**事实为真** (实跑: 14 条严谓词字段行, 冒号后首非空白是反引号的 = 0) |
| **L-m4** | Minor | `:583` | 「本文件 **`:123`** 自己就有一个 4 反引号 code span 内含 3 反引号」 | `grep -n '\`\`\`\`' …/linked-issue-field-availability/proposal.md` (当前与 027a50f) | 两次均只命中 **`:159`**;`:123` 是普通 3 反引号围栏开头 | ❌ 行号错。**substance 为真** (`:159` 的 4 反引号 span 确实不在行首, 不触发状态机) |
| **L-m5** | Minor | `:319` / `:342` / `:379` | 「共 **10** 条 check — `grep -c '^  - name:' .aria/state-checks.yaml` = 10」;「(iii) 项目侧探针 `.aria/probes/*.py` (**2** 条 …… 也是**最近两条新增**)」;「现有 **10** 条 check 无一使用 `${CLAUDE_PLUGIN_ROOT}`」 | `git show cc1bdef:.aria/state-checks.yaml \| grep -c '^  - name:'` → `10`;`grep -c '^  - name:' .aria/state-checks.yaml` → `11` | 声明基线 `cc1bdef` = **10** ✅;工作树 `b0c16ff` = **11**, 形态 (iii) = **3** 条 (`config-template-key-currency` / `plugin-cache-currency` / `main-project-version-consistency`) | ⚠️ 判**不可比**非矛盾 (总体不同: `2ae012f` 引入第 11 条)。但**同文件 `:408` 已订正为 11 而 `:319`/`:342`/`:379` 三处未同步**, 且 `:342` 的「6+2+2=10」逐条归类与 `:342` 的「最近两条新增」在当前已失效 |

---

### 1.3 sibling-spec-probe — **0 Major / 3 Minor**

**这份 Spec 的事实面是三份里最干净的**: 我逐条实跑了它引用的全部 git/远端/文件事实与三臂语料对照, **无一条被证伪**。

| # | 严重度 | 位置 | 断言原文 (摘) | 实跑命令 | 实际输出 | 判定 |
|---|---|---|---|---|---|---|
| **S-m1** | Minor | `:433` | 「本仓全部 **11** 条远端跟踪 ref 合计 **151ms**」 | `git for-each-ref --format='%(refname)' refs/remotes \| wc -l` | **12** (含 `refs/remotes/origin/HEAD`) | ⚠️ 口径未写明。排除符号引用 `origin/HEAD` 后恰 **11** ⇒ 判**不可比**非矛盾。耗时 151ms 为单次采样, 不可复核 |
| **S-m2** | Minor | `:62` | 「无 pytest 依赖时走 `python3 -m unittest discover -s . -p "test_*.py"` (`:71`)」 | `git -C aria show d50f9c3:skills/run_all_tests.sh \| awk 'NR>=61&&NR<=72'` | `:68` 先判 `elif [ -f "$tests_dir/run_tests.py" ]`, `:71` 是最后 `else` 回落 | ⚠️ 中间还有一个 `run_tests.py` 分支未提。`:48` / `:50` / `:71` **三个行号逐字正确** |
| **S-m3** | Minor | `:266-270`, `:277-280` | `ls-remote --symref github` 4.5s / `origin` 6.0s / `git remote show github` 4.3s;`git ls-tree` 5ms / `git grep` 12ms (15 行) | — | 单次采样, 结构上不可复核 | ⚠️ 文档已在 (b)(c) 标「各一次采样」。「15 行」与我在 `cc1bdef` 实测的松谓词 15 行**一致** ✅ |

---

## 2. 逐条断言核验表 — 复核为 ✅ 一致的高价值断言

> 只列**承重**或**本轮新增 (commit `100759d` K1–K9 批次)** 的条目。全部经不带过滤的连续输出复读或实跑复现。

### 2.1 本轮新增 (K1–K9) — owner 点名优先核实的那一批

| K | 断言 | 实跑命令 | 实际输出 | 判定 |
|---|---|---|---|---|
| **K1** | `heartbeat()` 在 `claim_lifecycle.py:244-256` **逐字段重建** `ClaimRecord` (显式列 **11 个**字段, 含 `linked_issue=existing.linked_issue`), **不是** `dataclasses.replace` | `git -C aria show d50f9c3:skills/state-scanner/lib/claim_lifecycle.py \| awk 'NR>=222&&NR<=260 {printf "%d\|%s\n",NR,$0}'` | `:244 updated = ClaimRecord(` … `:245 schema_version` `:246 track_id` `:247 owner` `:248 container` `:249 session` `:250 phase` `:251 status` `:252 claimed_at` `:253 heartbeat_at` `:254 superseded_from` `:255 linked_issue=existing.linked_issue` `:256 )` | ✅ **逐字段清点 = 11, 区间 `:244-256` 精确, 无 `replace`** |
| **K1 先例** | `git grep -c "linked_issue=" d50f9c3 -- skills/state-scanner/` ⇒ `claim_lifecycle.py:4` · `claim_schema.py:1` · `gc.py:1` · `phase1_gate.py:5` · `tests/test_release_by_track.py:6` = **17 处 / 5 个文件** | 同左, 逐字 | `4 / 1 / 1 / 5 / 6`, sum = **17**, files = **5** | ✅ **五个文件名与五个计数逐一命中** |
| **K2** | `release_claim_by_track` 只匹配 `active` (`:427`);legacy claim 无 `track_form` ⇒ 释放 `[s1,s2,s3]` vs `[s2]` 两个相反答案 | `awk 'NR>=422&&NR<=430'` | `:425 if rec.container == …` `:426 and rec.track_id == norm` `:427 and rec.status == "active"` `:430 return … error="claim_not_found"` | ✅ 全部逐字 |
| **K3** | §2.1a `:164` 逐字写着「**本 Spec 不新增拼接函数**」 | `awk 'NR==164' …/proposal.md` | `**本 Spec 不新增拼接函数** —— 新增代码落点只有 \`lib/identity.py\` 的直取 \`uuid\` accessor …` | ✅ 逐字 (但见 A-M2: SC-2 (ii) 未同步) |
| **K5** | `unknown_schema_claims` 与 `linked_issue_overlap` 共用 `phase1_gate.py:1231-1238` 同一 `try:`, `except` 只赋 `linked_issue_overlap` | `awk 'NR>=1225&&NR<=1247'` | `:1230 if args.linked_issue:` / `:1231 try:` / `:1233-1235 out["linked_issue_overlap"] = linked_issue_overlaps(...)` / `:1236 except Exception as exc:` / `:1237 logger.warning(...)` / `:1238 out["linked_issue_overlap"] = []` | ✅ **区间与每一行逐字精确** |
| **K6** | `lib/gc.py:324` 逐字「Number of stale active claims **rewritten to** `status='abandoned'`」;`ClaimRecord` **无 swept 标记** | `awk 'NR>=318&&NR<=350' gc.py` ; `grep -n "swept" claim_schema.py` | `:324    Number of stale active claims rewritten to ``status='abandoned'``` ;后者无输出 | ✅ **逐字 + 零命中** |
| **K7** | `def log(` 全 aria **零命中**;`phase1_gate.py:56` 只有 `logger = logging.getLogger(__name__)` 而无 handler | `git -C aria grep -n "def log(" d50f9c3 -- .` ; `awk 'NR>=50&&NR<=60' phase1_gate.py` | 前者无输出;`:56 logger = logging.getLogger(__name__)` | ✅ (`basicConfig` 的范围限定见 A-m4) |
| **K8** | SOT 模板默认值 `` `{<org>/<repo>#<n>}` `` 判 `BAD_TOKEN`, 而 E6 只对 `无` 设门 ⇒ 两份 placeholder **互相命中** | `python3` 直调 `d50f9c3` 的 `normalize_linked_issue` + `linked_issue_overlaps` | `normalize(placeholder) = None`;`overlap: [{'track_id': 'b-uuid2', …, 'linked_issue': '{<org>/<repo>#<n>}', …}]` | ✅ **实跑复现, 与文档断言完全一致** |
| **K9** | 「本仓该文件今天就不存在」(`.aria/linked-issue-field-grandfathered.txt`), 而作用域 9 份里有 6 份 `NO_FIELD` ⇒ 必然 exit 1 | `ls -la .aria/linked-issue-field-grandfathered.txt` ; E0–E6 原型全跑 | `No such file or directory`;9 份 = 3 OK + 6 NO_FIELD | ✅ **两半都成立** |
| **K (跨 skill import 先例)** | `session-closer/scripts/handoff_autofill.py:403-407` 逐字五行 + 同文件 `:48-51` 第二处 | `git -C aria show d50f9c3:skills/session-closer/scripts/handoff_autofill.py \| awk 'NR>=400&&NR<=410'` 与 `NR>=45&&NR<=55` | `:403 # state-scanner/lib 是兄弟 skill 的包; 加其 skill root 使 \`from lib.identity\` 解析。` `:404 _ss_root = str(Path(__file__).resolve().parents[2] / "state-scanner")` `:405 if _ss_root not in sys.path:` `:406     sys.path.insert(0, _ss_root)` `:407 from lib.identity import get_identity`;`:48-51` = `_ss_scripts = …/"state-scanner"/"scripts"` + `from collectors.multi_remote import BENIGN_UNCONDITIONAL_REASONS` | ✅ **逐字节完全一致 (含中文注释), 两处都在。R4/S-1「本仓无先例」前提确被推翻** |
| **K (反例)** | `fetch_gate.py:111-112` 逐字「Mirrors state-scanner sync.py::_resolve_default_branch (replicated to keep phase-d-closer self-contained — **no cross-skill runtime import**)」 | `awk 'NR>=106&&NR<=130' fetch_gate.py` | `:111    Mirrors state-scanner sync.py::_resolve_default_branch (replicated to keep` / `:112    phase-d-closer self-contained — no cross-skill runtime import).` | ✅ **逐字, 跨两行且区间精确** |
| **K (`fetch_gate.py:21`)** | R4 行号订正:「原引 `:23`, 实读 `:23` 是另一句「state-scanner git.py — but the original locks `@{upstream}`」;`sync.py::_resolve_default_branch` 那句在 **`:21`**」 | `awk 'NR>=18&&NR<=25' fetch_gate.py` | `:21    state-scanner sync.py::_resolve_default_branch (module-private, other skill).` / `:23    state-scanner git.py — but the original locks ``@{upstream}``; 切口1 needs` | ✅ **两句、两个行号全部逐字命中。该 R4 订正是对的** |

### 2.2 逐字引文专项 (最高优先级) — 31 条连续复读结果

| 引文 | 声明位置 | 实读位置 | 判定 |
|---|---|---|---|
| 「If several active claims match (**same container re-claimed a track across sessions — the NORMAL case, since every session mints a fresh session_id and B.0 REQUIRE-claim runs per session**), **ALL matching active claims are released**」 | a1 `:482-485` 称 `claim_lifecycle.py:396-399` | `awk 'NR>=395&&NR<=400'` → `:396 the caller passes the raw carry-id. If several active claims match (same` / `:397 container re-claimed a track across sessions — the NORMAL case, since` / `:398 every session mints a fresh session_id and B.0 REQUIRE-claim runs per` / `:399 session), **ALL matching active claims are released** (review I1: releasing` | ✅ **逐字完全一致, 区间 `:396-399` 精确**。⇒ **R4/code-explorer 对上一轮 grep-拼接错误的订正本身是对的** |
| `NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)` | a1 多处称 `constants.py:43-44` | `:43 and in reality NO production heartbeat loop exists (heartbeat() has zero` / `:44 production call sites; phase1_gate self-resume does not refresh either),` | ✅ 逐字 (仅去掉行首连接词 `and in reality`) |
| `Deliberately much longer than STALE_TTL: STALE_TTL only marks a claim` / `"takeover-eligible" (advisory, reversible on next read), but the sweep` / `REWRITES status=abandoned durably and the victim has no recovery path —` | a1 `:252` 称 `constants.py:40-42` | 三行**逐字节一致** | ✅ |
| `# No prompt needed: stale / terminal tracks are safe to acquire.` (7d 注释) | a1 `:145` | `phase1_gate.py:718` 逐字 | ✅ |
| `verdict.winner is not None and not _takeover_eligible(verdict)` (7c 条件) | a1 `:145` | `phase1_gate.py:650-653` = `elif (` / `verdict.winner is not None` / `and not _takeover_eligible(verdict)` / `):` | ✅ |
| `"stale_takeover_eligible" in reason or reason in {"no_active_candidates","empty_claims"}` | a1 `:145` 称 `:283-294` | `:283 def _takeover_eligible(` … `:291-294 return ("stale_takeover_eligible" in reason or reason in {"no_active_candidates", "empty_claims"})` | ✅ 区间精确 |
| `if c.track_id == own_track_id:` / `continue  # same-name collision — reconcile's job, not ours` | a1 `:150` 称 `collision.py:278-279` | 逐字命中 | ✅ |
| `if not own_linked_issue:` / `return []` | a1 `:112` 称 `collision.py:265-266` | 逐字命中 | ✅ |
| `_TERMINAL = ("done", "abandoned", "unknown")` | a1 `:303` 称 `collision.py:268` | 逐字命中;**不含 `yielded`** ✅;**含 `unknown`** ✅ | ✅ |
| `def linked_issue_overlaps(claims, own_track_id, own_linked_issue)` 三参数 | a1 `:357` 称 `:230-234` | `:230 def linked_issue_overlaps(` / `:231 claims:` / `:232 own_track_id:` / `:233 own_linked_issue:` / `:234 ) -> "list[dict]":` | ✅ |
| `linked_issue: Optional[str] = None` | a1 `:327` 称 `claim_schema.py:130` | 逐字命中 | ✅ |
| `if not args.raw_track_id and not args.sweep_stale and not args.gc:` / `parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")` | a1 `:463-467` 称 `release_gate.py:236-237` | 逐字命中;**实跑** `python3 release_gate.py --status abandoned` → `release_gate: error: 至少需要 --raw-track-id / --sweep-stale / --gc 之一` | ✅ **代码 + 运行回执双证** |
| `--phase` 是 `required=True` | a1 `:236` 称 `phase1_gate.py:1191` | `:1190-1192 parser.add_argument("--phase", required=True, help=…)`;**实跑** `python3 phase1_gate.py --raw-track-id x` → `phase1_gate: error: the following arguments are required: --phase` | ✅ **逐字与回执完全一致** |
| CLI help「同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)」 | a1 `:49` | `phase1_gate.py:1204` 逐字 | ✅ |
| 「active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)」 | a1 `:290`, `:705` 称 `release_gate.py:225` | `:225 help="顺带扫描: active 且 heartbeat 超 STALE_TTL → abandoned (跨 container)"` | ✅ |
| 「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, **不在 scan.py 内自动执行**」 | a1 `:227`, `:744` 称 `layer-l-integration.md:15` | 逐字命中 | ✅ |
| `\| `heartbeat` \| `phase-b-developer` mid-cycle \| 每 10min (caller 负责调度) \| `lib/claim_lifecycle.py::update_heartbeat()` \|` | a1 `:744` 称 `layer-l-integration.md:45` | **逐字节一致**;`git grep update_heartbeat d50f9c3` 全 aria **只命中这一行自身**;真名 `heartbeat()` 在 `claim_lifecycle.py:178` | ✅ **悬空函数名成立** |
| 「接线点 = AI 编排层, 不是 `scan.py`」+ 触发条件 `enabled == true` **且** `collision.kind` 非空 | a1 `:227-228` 称 `state-scanner/SKILL.md:149` | 逐字命中 | ✅ |
| `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)` | a1 `:124`, `:684` 称 `branch-manager/SKILL.md:146` | 逐字命中;正文至 `:152` ✅ | ✅ |
| `carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串` | a1 `:190` 称 `phase-d-closer/SKILL.md:55` | 逐字命中 | ✅ |
| `[--linked-issue "<repo>#<n>"] --repo-path "<repo root>"` | a1 `:702`, `:820` 称 `phase-b-developer/SKILL.md:93` | 逐字命中 ⇒ **Phase B 可选传 `--linked-issue`, R3/BA-M3 订正成立** | ✅ |
| `check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)` = 布尔谓词, 不携带 track_id | a1 `:233` 称 `:88` | 逐字命中;track_id 在同文件 `:92` 另取 | ✅ **R3/TL-M6 撤销该先例是对的** |
| `allowed-tools: Read, Write, Glob, Grep, Task, Skill` / `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` | a1 `:393-394` 称 `phase-a-planner:9` / `spec-drafter:10` | 逐字命中;`spec-drafter:9 user-invocable: true` ✅ | ✅ |
| `- 查询项目状态 → 使用 \`state-scanner\` (A.0)` | a1 `:684` 称 `spec-drafter/SKILL.md:30` | 逐字命中;`:369` 流程图同名 ✅;`A.0.5` = brainstorm ✅ | ✅ |
| `_ORIGIN_HEAD_REFS` 三候选全 `refs/remotes/origin/*` + `_DEFAULT_BRANCH_FALLBACKS = ("master", "main")` | sib `:239` 称 `fetch_gate.py:50-54` / `:55` | 逐字命中;`:124-127` 名字猜测循环 ✅;`:108-128` 区间 ✅ | ✅ |
| 「Raw stderr is intentionally never returned — remote URLs in stderr may embed credentials」+ 枚举 `network \| auth_403 \| non_ff \| git_missing \| other` | sib `:358` 称 `fetch_gate.py:86-101` | `:89-90` 逐字, `:90` 枚举逐字 | ✅ |
| 「Callers must fall back to raw-string equality on `None` — never treat `None` as "no match"」 | sib `:178` 称 `normalize_linked_issue` docstring | `collision.py:192-193` 逐字 | ✅ |
| 「the top-level name `lib` resolves to state-scanner/lib (Layer L — a DIFFERENT package, claim_schema.py etc.), not scripts/lib」+「Deliberately NOT `import lib.runtime_probe`」 | lif `:442` 称 `coordination_probe.py:80-85` | `:80-85` 逐字 | ✅ |
| 「Minimal YAML parser — strictly scoped to state-checks.yaml shape.」/「This is a narrow parser — it intentionally rejects YAML features outside the documented schema.」 | lif `:408` 称 `custom_checks.py:63` / `:122-123` | 逐字命中 | ✅ |
| `argv = argv if argv is not None else sys.argv[1:]` / `repo = Path(argv[0]) if argv else Path.cwd()` | lif `:375` 称 `issue_cache_freshness_probe.py:148-149` / `coordination_probe.py:140-141` | 两处均逐字命中 | ✅ |
| `### Step 0: Anchor 固化 (Drift Guard #17, v1.44.0)` + 「入口逻辑完成后、**Round 1 启动前一次性**执行」 | sib `:364` 称 `audit-engine/SKILL.md:83` / `:85` | 逐字命中 | ✅ |
| `10CG/aria-plugin#150` 标题「[benchmark] Rule #6 判据表第三行的兜底「缺一照跑」对 14/43 个 skill 结构上不可执行 — 它们根本没有 AB 套件」 | sib `:454` | `forgejo GET /repos/10CG/aria-plugin/issues/150` → **逐字一致** (state=open) | ✅ |

### 2.3 数字与计数 — 逐条重跑

| 断言 | 位置 | 实跑 | 结果 | 判定 |
|---|---|---|---|---|
| `cc1bdef` 语料 **147** 篇 (`changes/` 7 + `archive/` 140) | a1 `:76-78`, sib `:41/:75`, 审计轨 #30 | `git ls-tree -r --name-only cc1bdef -- openspec \| grep -c '/proposal\.md$'` 等 | `147 / 7 / 140` | ✅ |
| `cc1bdef` 松谓词 **15** 文件 (14 archive + 1 changes) | a1 `:77` | `git grep -l '\*\*关联 Issue\*\*' cc1bdef -- 'openspec/**/proposal.md' \| wc -l` | `15`;archive 14, changes 1 (= a1-entry) | ✅ |
| 当前语料 149 / 17 / 17 / 19 / 9 / 140 | lif `:34-40`, `:76-84` | 六条命令逐字重跑 | `149 / 17 / 17 / 19 / 9 / 140` | ✅ **五条精确命中**;松谓词**行** 实测 **41** vs 文档 **37** ⇒ 语料自修改漂移 (文档 `:31` 已声明「口径才是规范, 数字是当日观测」) ⇒ 判**不可比** |
| 严谓词 14 条存量字段 **14/14** 直喂归一 = `None` | lif `:92` | 实跑 `normalize_linked_issue(rest.strip())` 逐条 | `strict field lines: 14  normalize=None: 14` | ✅ |
| 「取第一个 code span」在 **6** 条真实字段上抽出 triage verdict | lif `:177-185` | 实跑逐条 | `handoff-frontmatter-enforcement:4 → \`partial-repro\`` · `audit-drift-guard:5 → \`confirmed\`` · `cross-worktree-handoff-discovery:4 → \`confirmed\`` · `openspec-collector-false-green:14 → \`confirmed\`` · `gate-yaml-datasource:6 → \`confirmed\`` · `phase-c-gate-path-coverage:6 → \`confirmed\``, 全部 normalize=None | ✅ **6 条 file:line 与抽出值逐条完全一致** |
| §5 作用域 9 份逐份判定 (3 OK + 6 NO_FIELD) | lif `:450-464` | E0–E6 原型对 `openspec/changes/*/proposal.md` 全跑 | `a1-entry OK(无) :12` · `lif OK(无) :6` · `sib OK(无) :6` · 6 份 `aria-2.0-m{6,7}-*` 全 `NO_FIELD` | ✅ **九行逐行、含行号完全一致** |
| 全语料 verdict 分布 `NO_FIELD 132 / NO_TOKEN 14 / OK 3 = 149`;archive `126/14/0 = 140` | lif `:82-83` | 由上两项交叉推算 + 实测 | 全部自洽并与实测一致 | ✅ |
| **§3 层 0 三臂对照** (sib 的承重实证) | sib `:95-97` | E0 原型在 `cc1bdef` 147 篇上三臂各跑一遍 (+ 围栏臂) | 宽松 `no_field 132 / url_fallback 14 / no_token_no_url 1`, 3 簇且 `#122` 簇**含 a1-entry** (假阳性);行首 `133 / 13 / 1`, 3 簇假阳性消失;行首+仅头部 `136 / 10 / 1`, **只剩 1 簇** (`#137`), `#122` 与 `#95` 被误杀;**E0 三谓词 (加围栏) 与行首臂判定差异 = 0** | ✅ **九个数字 + 簇成员逐一命中, 零偏差。lif `:160` 的「加与不加围栏判定差异 = 0」亦成立 (147 与 149 两个总体均为 0)** |
| 三个同 key 簇 (#95 / #122 / #137) 6 份全在 `archive/`, `changes/` 为 0 | sib `:44-47`, `:76` | 同上 | 六个目录名逐一命中 | ✅ |
| B3「147 篇中 133 篇 `no_field` (90.5%), 只对 **13** 篇可见」 | sib `:401` | 同上 | `133/147 = 90.48%`;url_fallback = 13 | ✅ |
| coordination ref **2 个**容器 vs handoff `owner-container` **9 种** | a1 `:376` | `git ls-tree -r --name-only refs/aria/coordination \| grep '^claims/' \| cut -d/ -f2 \| sort -u` ; `grep -rhoE '^owner[-_]container:.*' docs/handoff/*.md \| sort -u` | `023236f2` / `bfe8285d` = **2**;9 个 distinct 值 (`aria-runner-bot/023236f2`, `dev-claude`, `dev-claude2`, `simonfish/023236f2`, `simonfish/bfe8285d`, `simonfish/dev-claude`, `simonfish/dev-claude2`, `simonfish/f9c6e8cd`, `simonfishgit/dev-claude`) = **9** | ✅ **两个数字精确** |
| 竞品轨于 `07-27T11:53:12Z` 确实认领过 | a1 `:58` | 同上 ls-tree | `archive/2026-08/bfe8285d/s-6cd0@1153-2026-07-27T11-53-12Z.yaml` | ✅ 逐秒一致 |
| AB: `ab-suite/` **31** 个 `.json` + **4** fixture 目录 + `version.yaml`;`audit-engine.json` 不存在 | sib `:443`, a1 `:421/:752` | `ls ab-suite/*.json \| wc -l` ; `find -maxdepth 1 -type d \| wc -l` | `31`;4 子目录 (`glm-smoke` / `m1-mvp` / `multi-terminal-coordination` / `phase-c-integrator-pre-merge-gate-fixtures`);`audit-engine.json` 缺 | ✅ (**R4/S-3 把 30 订正为 31 是对的**) |
| `phase-a-planner.json` / `spec-drafter.json` `evals` 各 **2**;`state-scanner.json` **12** | a1 `:412/:595/:596/:599/:751/:753`, lif `:494` | `json.load(...)['evals']` 逐个 | `2 / 2 / 12` | ✅;spec-drafter 两条 eval id 为 `level-judgment` / `bilingual-support`, 与 lif 写的「判断规范等级」「双语输入处理」语义一致 |
| `DEFAULTS.json` 的 `state_scanner` 段**根本没有 `coordination`** (rule6_note substitute baseline 必红) | a1 `:615/:746`, 审计轨 #26 | `git show d50f9c3:skills/config-loader/DEFAULTS.json` → 解析 `state_scanner` 键集 | `['confidence_threshold','auto_execute_enabled','auto_execute_rules','audit_log_path','sync_check','issue_scan','multi_remote','sync_freshness']` —— **无 `coordination`**;而 `config-loader/SKILL.md:134` / `:140` 已登记 `enabled` / `mode` | ✅ **baseline 必红成立** |
| `DEFAULTS.json:124-128` `adaptive_rules.level_3 = "challenge"` | sib `:375/:514` | `awk 'NR>=120&&NR<=130'` | `:124 "adaptive_rules": {` `:125 "level_1": "off"` `:126 "level_2": "convergence"` `:127 "level_3": "challenge"` `:128 }` | ✅ |
| `ca52d1c` diff 只触及 9 个文件、**一个** test 文件、不含 `gc.py`/`constants.py` | a1 `:259` (含 R1 minor-2 订正) | `git -C aria diff --stat ca52d1c^1 ca52d1c` | `marketplace.json / plugin.json / CHANGELOG.md / README.md / VERSION / SKILL.md / claim_schema.py / collision.py / test_release_by_track.py` = 9 files | ✅ **「一个 test 文件」的订正是对的** |
| `ca52d1c` 合入时刻 `2026-08-23T09:14:07Z`, 是 `d50f9c3` 祖先 | a1 `:15/:259` | `git -C aria show -s --format='%cI'` ; `merge-base --is-ancestor` | `2026-08-23T09:14:07+00:00`;is-ancestor 成立 | ✅ |
| `d50f9c3` 与 `58a49e7` 对 `collision.py` diff 为空 | lif `:560` | `git -C aria diff --stat d50f9c3 58a49e7 -- …/collision.py` | 空 | ✅ |
| 两 plugin 侧探针 `7716` / `11115` bytes | lif `:364/:482` | `ls -la` | `issue_cache_freshness_probe.py 7716` · `coordination_probe.py 11115` | ✅ **精确到字节** |
| `grep -n CLAUDE_PLUGIN_ROOT .aria/state-checks.yaml` **零命中** | lif `:379` | 同左 | rc=1, 无输出 | ✅ |
| standards 模板 `grep -c "关联 Issue"` = **0**;头部 blockquote 三行;`## Template Usage Notes` 存在 | lif `:106-119/:488/:496/:529` | 逐条 | `0`;`:3 > **Level**:` `:4 > **Status**:` `:5 > **Created**:`;`:40 ## Template Usage Notes`;全文英文 | ✅ |
| `aria/skills/spec-drafter/` 只有 **3** 个文件、无 `scripts/`;`grep -rn "关联 Issue"` = 0 | lif `:121-125/:370` | `git ls-tree -r --name-only d50f9c3 -- skills/spec-drafter/` | `SKILL.md` / `LEVEL_GUIDE.md` / `LEVEL3_TEMPLATE.md`;grep 0 | ✅ |
| `audit-engine/` **8** 个文件, 既无 `scripts/` 也无 `tests/` | sib `:60` | `git ls-tree -r --name-only d50f9c3 -- skills/audit-engine/` | 8 个 (SKILL.md + 7 个 references/) | ✅ |
| `execution-modes.md` `## Convergence 模式` `:84` / `## Challenge 模式` `:113`;两块**均无** `/state-scanner` 调用 | sib `:370-371/:514`, a1 `:206` | `grep -n "^## "` ; `grep -n "state-scanner"` | `:84` / `:113`;后者 rc=1 零命中;插入锚点 `:89 Round N:` `:90 1. 调用 agent-team-audit 单轮引擎` `:118 Round N (一个完整周期):` `:119 Step 1: 讨论组 spawn` 全部逐字 | ✅ |
| `report-format.md` `## 轮次记录` / `### Round N` 模板 `:50-71` | sib `:379/:515` | `awk 'NR>=48&&NR<=72'` | `:50 ## 轮次记录` … `:71 - Duration: {seconds}s` | ✅ |
| `run_all_tests.sh:48/:50/:71` | sib `:62/:512` | `awk 'NR>=44&&NR<=75'` | 三行逐字命中 | ✅ (中间分支见 S-m2) |
| `sync.py` **8** 个顶层 def、无 `_resolve_default_branch`、只有 `_ORIGIN_HEAD_REFS:46` | sib `:503/:522` | `grep -c "^def "` ; `grep -n "_resolve_default_branch\|_ORIGIN_HEAD_REFS"` | `8`;无该函数;`:46 _ORIGIN_HEAD_REFS = [` | ✅ |
| `remote_refresh.py:691` 写缓存, 在 `:568` 内;唯一生产调用点 `scan.py:312` | sib `:291/:418` | `awk` + `git -C aria grep -n "collect_remote_refresh" d50f9c3 -- .` | `:568 def collect_remote_refresh(` `:691 _write_cache_atomic(...)`;非 import/非 test 的调用点只有 `scan.py:312` | ✅ |
| `handoff_multibranch.py:589-598` cap 披露形态 | sib `:312` | `awk 'NR>=585&&NR<=600'` | `:589 if len(branches) > max_branches:` … `:595 r.soft_error("handoff_multibranch_branch_cap", capped_msg)` `:597 log.warning(...)` `:598 branches = branches[:max_branches]` | ✅ |
| `multi_remote.py:255-286` `resolve_enforced_remotes` 三参数纯函数 (32 行) + `configured` 为 None 走 auto-discover | sib `:214/:216/:519` | `awk 'NR>=250&&NR<=290'` | `:255 def resolve_enforced_remotes(` … `:286 return [r for r in actual if r not in ro], []`;286−255+1 = **32** | ✅ |
| `.aria/config.json` → `state_scanner.multi_remote.enforced_remotes` = **`null`** | sib `:216` | `python3 -c json.load` | `null` | ✅ |
| `git remote` 2 个 vs `refs/remotes/` **3** 个名 (多出 `probe`), `git config --get remote.probe.url` 空且 exit 1 | sib `:219/:485` | 逐条 | `github` `origin`;`github` `origin` `probe`;rc=1 无输出 | ✅ **当场复现** |
| `git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master` (exit 0);`github` → `fatal: … is not a symbolic ref` (exit **128**) | sib `:244-245/:483` | 逐条 | 完全一致 | ✅ **含 exit code** |
| `git version 2.39.5`;`man git-fetch` 无 `followRemoteHEAD` | sib `:248` | `git --version` ; `man git-fetch \| grep -c followRemoteHEAD` | `2.39.5`;`0` | ✅ |
| `refs/aria/*` 现存 **3** 条 | sib `:302/:423` | `git for-each-ref 'refs/aria/*'` | `coord-check` / `coordination` / `coordination-remote` | ✅ |
| `AB_TEST_OPERATIONS.md` 写「Skill eval suites \| 28 个 \| ✅ 全量覆盖」而实测 31 ⇒ 三方不一致 | sib `:523/:541` | `grep -n` | `:76 \| Skill eval suites \| 28 个 \| ✅ 全量覆盖 \|`;`§场景 2: 新增 Skill 首次基线` 在 `:222` | ✅ |
| aria-plugin `#117` / `#127` / `#135` / `#157`, Aria `#180` 的存在与主题 | a1 `:608`, sib `:6/:454` | `forgejo GET` 逐个 | `#117 [benchmark] AB 测试集缺 authoring 维度…`;`#127 …缺 D9 surface…`;`#135 [state-scanner/coordination] 认领机制三处缺口…`;`#157 …ab-suite 对 SKILL.md Layer L / --linked-issue 段零覆盖…`;Aria `#180 coordination claim 的 collision surface 在 30 分钟后静默失效 — heartbeat() 零生产调用点` | ✅ 五条全部 open 且主题一致 |
| spike S1 事故窗 **48–72h**;spike S2 双远端 fetch ×5 = `12.5/13.4/14.1/15.9/13.0` 均值 **~13.8s**, 3 轮净增 **~41s** | a1 `:146/:202/:247`, sib `:260-261` | `grep -n` 两份 spike | S1 `:40` 「第 4 次 ~48h / 第 5 次 ~72h」;S2 `:39` 五个数与均值逐字;S2 `:48` 「本 Spec 自己经历的 3 轮则是 ~41s」 | ✅ **五个采样值逐个命中** |
| **spike S3 `:72` 的 `identity.py:244` 是行号误记** (母 Spec §未做/存疑 #1 自陈「本轮未实读复核」) | a1 `:137/:803/:846` | `sed -n '68,76p' .aria/spikes/2026-08-02-S3-track-id-derivation.md` | `:72` = 「(实测 `identity.py:222` 是 `return label if label else uuid`, `:244` 是 hostname 兜底。)」;而实读 `identity.py:242 return _hostname()` / `:244 return uuid` | ✅ **本席已代为核实: FIX-18 的勘误主张成立, 该存疑项可关闭** |
| a1 审计轨 §5 **34 行**齐全, `#22/#26/#28/#29/#30/#33` 全部 resolve | a1 `:17/:560/:562` + 10 处交叉引用 | `sed -E 's/^\| *\*{0,2}([0-9]+)\*{0,2}.*/\1/'` 重数 | `1..34`, count = **34**;六个被引行内容与我独立实读结果一致 | ✅ (**我先前用带过滤的 grep 得 17 行、几乎误报 Critical, 见 §0**) |
| 两份子 Spec 审计轨行号完备性 | lif `:573-574`, sib `:532-534` | 同法重数 + 交叉引用比对 | sib trail 28 行, 正文引 1–28 ⇒ 全 resolve;lif trail 26 行, 正文引 #14/#16 ⇒ resolve | ✅ 无悬空 |
| 实跑复现:`无`/`无` 互相误报 | a1 `:112-117` | 直调 `d50f9c3` 的 `linked_issue_overlaps` | `[{'track_id': 'spec-b-uuid2', …, 'linked_issue': '无', …}]` | ✅ **与文档展示的输出字面一致** |
| 实跑复现:unknown sentinel 通道恒空 | a1 `:330` | 直调 `parse_claim` + `linked_issue_overlaps` | `status='unknown'`, `linked_issue=None`, `track_id=''`, `container=''`, `claimed_at=''`;overlap → `[]` | ✅ **五个字段 + 返回值逐一命中** |

### 2.4 跨文档承接核验 (owner 交办第 4 项)

| 母 Spec 声称迁往 | 承接方实测 | 判定 |
|---|---|---|
| §1 → `linked-issue-field-availability`: C-A / M-10 / M-2 / **FIX-06/07/08** / SC-13 / `.aria/state-checks.yaml` / `proposal-minimal.md` | `grep -c`: `C-A` 8 · `M-10` 6 · `M-2` 10 · `FIX-06` 3 · **`FIX-07` 0** · `FIX-08` 2 · `SC-13` 1 · `state-checks.yaml` 16 · `proposal-minimal.md` 11 | ⚠️ **FIX-07 零锚点** (见 A-m10);其余 8 项全部接住 |
| §4 → `sibling-spec-probe`: M-1 / M-5 / M-6(audit-engine 档) / M-17(§4 stdout) / FIX-10 / SC-16/17/18/19(a)(c) | `M-1` 12 · `M-5` 10 · `M-6` 1 · `M-17` 7 · `FIX-10` 5 · `SC-16` 5 · `SC-17` 6 · `SC-18` 9 · `SC-19` 5 · `audit-engine` 26 | ✅ **十项全部接住**, 且 M-1/M-5/M-17 各有专节 (§3/§4/§7) |
| lif ↔ sib 的 `BAD_TOKEN` 接缝:lif `:312` 称「探针 Spec 已在其 §3 补了**逐格映射表**, 对 `BAD_TOKEN` 采**层 1 与层 2 并集**」 | sib `:107-113` 确有四态逐格映射表;`:111` 对 `BAD_TOKEN` 明写「**层 1 与层 2 都跑, 取并集**」;`:120` 明写「**采纳姊妹席的建议 …… 因此姊妹侧四态定义无需任何改动**」 | ✅ **双向对上, 接缝闭合** |
| lif `:216-217` 要求「探针 Spec 须同批加一条: **原串键不得由 `BAD_TOKEN` 的常量串产生**」(交叉点名) | sib `:111` 已落:「**落版**: 原串键**排除一个成文的常量黑名单** …… **新增 SC-19**」 | ✅ **交叉点名已被对侧接住** |
| lif `:293` 与 sib `:186` 互为镜像的「URL 回落绝不产生 `--linked-issue` 实参」 | 两侧逐字均在, 且都写了「任一被改必须同批改另一侧」 | ✅ |
| a1 `:359` 称姊妹 Spec 已自行写入关闭条款 | `archive/2026-08-23-linked-issue-normalization/proposal.md:257` 逐字命中;`:259` (非 `:260`, 见 A-m2) 逐字命中 | ✅ substance 接住 |
| a1 §6 缺口表「legacy 轨 / 竞品已归档 → 由 `sibling-spec-probe` 承担, **它 ship 前该缺口无覆盖**」 | sib `:67` 逐字对称声明:「该行在本 Spec 未 ship 时**退化为「无覆盖」**」 | ✅ 双向一致 |
| a1 §Why 与 sib §Why 对第 5 次事故形态的表述 | a1 `:39` 「起草者在 07-31 做修订前自己没有 fetch」;sib `:37` 同义复述并明确它属场景 (b) | ✅ 一致 |

---

## 3. 收敛判断

### 3.1 本轮事实核验腿的产出结构

| 维度 | 数值 |
|---|---|
| 实读断言总数 | 约 **130** 条 |
| 逐字引文专项复读 | **31** 条 |
| 实跑复现 | **7** 处 |
| Critical | **0** |
| Major | **3** (a1 ×2 / lif ×1 / sib ×0) |
| Minor | **19** |
| **被证伪且改变某条设计结论的断言** | **0** |

### 3.2 三条判据

**(a) 「本轮 fix 引入的 major 占比」(memory `marginal-return-negative` 的拐点判据)**

3 条 Major 中:
- **A-M1** (`coordination_probe.py` 逐字出处错标) —— 位于 2026-08-27 的 K1–K9 清账批次, **本轮 fix 引入**;
- **A-M2** (SC-2 的 `compose` 残留) —— 是 **R4/C-1 订正自身只修了一半**, **本轮 fix 引入**;
- **L-M1** (`:88` 悬空锚点) —— **先存缺陷**, 且 D2 已订正一处、漏了两处 (§Why grep 块 + SC-1)。

⇒ **2/3 = 66% 的 Major 由本轮 fix 引入**, 超过 `marginal-return-negative` 给出的 1/2 拐点。**同镜头再开一轮的边际产出预期为负。**

**(b) 缺陷的性质**

**全部 22 条 finding 都是「引用/计数/锚点」类, 无一条是「事实弄反」类。** 逐条核对后:
- 每一条被证伪断言所支撑的**结论**, 我都独立复核为**真** (A-M1 有 `coordination_probe.py:18-21` 兜底;A-m3 的 grep-0 我在 `:335-949` 上亲跑确认;L-M1 的假阳性形态在 `cc1bdef:75` 上真实存在;L-m1/m2/m4 的推理链全部成立);
- 三份 Spec 引用的**全部承重代码事实**(31 条逐字引文中的 30 条、K1–K9 全部 9 条、层 0 三臂 9 个数字、6 条 first-code-span、9 份作用域判定)**零偏差**。

⇒ 这是一份**事实基础扎实、引用维护滞后**的交付面, 不是一份**建立在错误事实上**的交付面。

**(c) 语料自修改造成的漂移已被文档自己预告**

L-m1 / L-m2 / L-m5 / A-m5 四条本质同源: **文档在描述一个包含它自己的语料, 写下描述的动作本身改变了被描述对象**。lif `:31` 已逐字预告这一点并规定「口径 (命令) 才是规范, 数字是当日观测」。⇒ 这四条**不构成对方法的质疑**, 只构成「按已成文的口径重跑一次并回填」的机械作业。

### 3.3 结论与建议

**本席判定: `verdict: REVISE`, 但明确建议 owner 不再为事实核验镜头加第 6 轮。**

1. **不加轮的理由**: 2/3 的 Major 是上一轮 fix 自造 (拐点判据触发);且 3 Major + 19 Minor **全部可机械订正** —— 每一条我都给了精确的 `文件:行号` 与实际取值, 不需要设计判断。再跑一轮同镜头, 预期只会抓到「订正本身又引入的新引用错」。

2. **建议的处置形态 (memory `stop-adding-rounds`: 换新鲜眼睛 > 加轮)**:
   - **一次性机械订正 editlist** (22 条, 每条带 grep 锚点与替换值), **由非本轮执笔席落**;
   - 落完后**只做一次「只看接缝的机械回归」**: 对三份 Spec + 三份审计轨全量重跑 `文件:行号` 解析器 (母 Spec `:561` 自陈的 `verify_line_refs.py` 正是为此而生), 判「每个引用是否解析到一个存在的行, 且该行是否含断言点名的字面串」—— 这是本轮 22 条 finding 里 **19 条**能被机械抓住的形态;
   - 剩下 3 条 (A-M1 出处错标 / A-M2 订正残留 / A-m10 跨文档 traceability) 机械查不到, 须人工点名清账。

3. **必须优先落的两条 (会影响 A.2 可实施性)**:
   - **A-M2**: SC-2 的 (ii) 负控臂仍点名不存在的 `compose` —— A.2 写夹具时会卡住, 且该臂被声明为「缺它视为未满足本条」;
   - **L-M1**: SC-1 的 (c) 臂给出的「真实语料实例」锚点 (`母 Spec :88`) 不存在 —— A.2 取原文会取到 `## What Changes`。

4. **可关闭的既有存疑项**: 母 Spec §未做/存疑 **#1** (「spike S3 `:72` 本轮未实读复核」) —— **本席已实读, FIX-18 的勘误主张成立**, 该项可标为已核。

5. **给 owner 的一条方法观察 (非 finding)**: 本轮三份 Spec 里, **`sibling-spec-probe` 的事实面零 Major**, 而它是唯一一份「所有实读结论都配了可当场重跑的命令 + 三臂对照 (含两个像样的坏实现)」的文件。它的 `:95-97` 三臂表是本次核验中**唯一一处九个数字与簇成员全部零偏差重现**的断言组。这条正相关值得在 R6 之后的执笔规范里点名。

---

**本席未修改任何被审文件。** 全部命令可在 `b0c16ff` / aria `d50f9c3` 上原样重跑。
