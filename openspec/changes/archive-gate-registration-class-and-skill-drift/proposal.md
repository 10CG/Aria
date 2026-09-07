# openspec-archive 文档/实现漂移收口 — 类级补齐 + 两个机械兜底

> **Level**: 3 (Full — 跨三个 Skill 的指令面变更 + 两个新探针 + 八条开单 + 发版同步面; 四个 task group)
> **Status**: Draft (Phase A.1; post_spec R1→R2 已跑, 本文为 R2 修订版)
> **Change ID**: `archive-gate-registration-class-and-skill-drift`
> **Linked Issue**: `10CG/aria-plugin#186` (类级排查总 tracker)
> **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2` (Layer L claim 2026-09-06T15:32:43Z, session `s-f260@1532`)
> **Parent US**: 无 — 方法论工具链维护 (v1.x 轨)
> **前序**: `a1-entry-claim-duplicate-work-guard` (2026-09-06 归档) 的 carry-forward M2
>
> ### ⚠️ 跨仓 issue 号消歧 (R1 RF-4/AB-7 + R2 R1V-8 — 上一版自宣此纪律却违反 7 次)
> **全文所有 issue 号一律写 `<org>/<repo>#<n>`, 无例外。** 已知真实撞号:
> `10CG/aria-plugin#186` (本 Spec tracker) vs `10CG/Aria#186` (`[Archive Tracker] phase-c-integrator-ci-path-coverage`);
> `10CG/aria-plugin#185` vs `10CG/Aria#185` (SC-6 夹具用的是 **Aria 仓**那个)。
>
> ### 🔀 Part A 已拆出 (2026-09-07 owner 裁定)
> 原 Part A (归档闸门 `python -m` 谓词) 连同 V4 设计、21 个对抗用例、三处接入点、基线三态,
> 全部移入 **`10CG/aria-plugin#188`**。**拆分依据是实测**: 沿生产链 (`extract_claim_symbols`)
> 测得 7 个活跃 spec 抽出 **0 个**符号; 最近 59 个 spec 抽出 18 个, 其中父目录是真 Python 包
> (谓词唯一能锚定的形态) 的 **0 / 18**; 全仓 20 处 `-m <点分路径>` 命中**全在**
> `aria-orchestrator/hermes-extensions/aria-layer1/`, 而无任何 spec 声称过该包里的符号。
> ⇒ 那个修复会带着全绿测试 ship 而生产触达为 0 (memory `completion_signals_vs_runtime_invocation`)。
> 拆分不制造接缝: 本 Spec 余下部分对它**零实现/零引用/零导出依赖** (原先声称的「共用 `spec_complete.py`」
> 已在 R1 被证伪 —— Part B 一行都不碰那个文件)。

---

## Why

2026-09-06 母 Spec 交接记了 `openspec-archive/SKILL.md` 两处与实现漂移 (M2)。Phase A.1 取证证实了漂移、**推翻了它的后果推断**, 并在 R1/R2 两轮审计中把「类」从 5 处推到 **20 处、跨三个 Skill**。

### 取证的三个反转

**反转 1 — `openspec archive` CLI 是个不存在的东西, 而 SKILL.md 把它当核心动作。**
`command -v openspec` 无输出; CLI 工作区 (`openspec/project.md`) 从未初始化; 审计报告
`post_planning-R1-2026-07-19-...:33` 明文承认手工 `git mv`; **144** 份归档中 **134 份 (93%)**
无 Step 2 的任何 frontmatter 写入痕迹。归档条目 rename/add 分类实测 **102 R + 42 A = 144**。

**反转 2 — 交接记的「SHA 逐字匹配静默落空 ⇒ 永远填不进去」不成立。**
漂移本身是真的 (`SKILL.md:317` 写 `Step2`, `spec_complete.py:1251` 写 `Step 7`, difflib 逐字符
diff = 单一 opcode `replace '2' -> ' 7'`)。但全仓**无 `str.replace`** —— 那是给 AI 的自然语言
指令。6 个 `10CG/Aria` 仓的 `[Archive Tracker]` issue 全量翻页核过 (open 2 + closed 4, 无第 3 页):
**3/6 含 SHA**。真缺陷是 Step 7 的 SHA 填充**没有代码宿主** —— 6 次执行 4 种形态,
`10CG/Aria#185` 被替换成一句完全不含 SHA 的话而无人发现 (memory `no-code-host-no-assertion`)。

**反转 3 (R2) — 「类级补齐」本身连漏三次。**
R1 枚举 5 处 → R1 修订扩到 12 处 → R2 审计席再抓 **1 处类内 + 1 处跨 Skill**。逃掉的那处是
`SKILL.md:17`「修复 CLI 归档位置 **bug**」—— 它**逃出了 SC-4 自己的 grep 模式** (`CLI 归档位置 bug`
不匹配 `CLI bug`)。跨 Skill 的那处是 `phase-d-closer/SKILL.md:41`。
⇒ 本版的类级枚举**先跑加宽 grep 再定表**, 且 SC-4 的判据改为「区段外命中 == 0 ∧ 区段内命中集合
逐行钉死」, 不再依赖「我想到了几处」。

---

## What Changes

### Part B — CLI 漂移类级收口 (三个 Skill, 20 行)

**完整类级枚举** (加宽 grep `openspec (archive|validate|CLI)|CLI[^。]{0,12}bug|CLI 完成|安装 openspec|自动修正|修正 CLI|CLI 归档` 实跑所得, 非人工回忆):

| # | 位置 | 改动 |
|---|---|---|
| B1 | `openspec-archive/SKILL.md:317` | `Step2` → `Step 7` (对齐 `spec_complete.py:1251`) |
| B2 | 同 `:318` + Step 7 段落 | 替换文案改为可验证约束 (必须含 7-40 位十六进制 SHA) + 强制调用 C2 |
| B3 | 同 **`:4`** | **frontmatter `description`** —— 删「自动修正 CLI bug」。⚠️ **这条决定整个变更的 Rule #6 档位** |
| B4 | 同 **`:17`** | 历史行「修复 CLI 归档位置 bug」加时限限定 (R2 新增, 逃出 SC-4 grep 的那处) |
| B5 | 同 `:40` + `:41` | 核心功能表两行: 「调用 CLI」→ `git mv`; 「自动修正」→「位置校验」 |
| B6 | 同 `:56` | 「**本 Skill 会自动修正此问题**」→ 对采用者的条件表述 (它是现时承诺, 不是历史陈述) |
| B7 | 同 `:247` + `:248` + `:249` | Step 3 标题/命令/等待 → `git mv openspec/changes/{id} openspec/archive/{YYYY-MM-DD}-{id}` |
| B8 | 同 `:251-257` + `:259-261` | Step 4 降级为位置校验三断言; Step 5 **保留编号, 段落体改为一行 pointer**「(已并入 Step 3)」(R2 ID-3: 落地形态原先未定) |
| B9 | 同 `:87` | 退役 `keep_changes_copy` |
| B10 | 同 `:392` + `:393` + **`:394`** + `:401` | 示例 1 四行 (R2 ID-3: `:394` 「Step 5: ✅ 清理活跃变更目录」必然过时, 原先漏枚举) |
| B11 | 同 `:588` | 错误表 CLI 行 → `git mv` 失败三分支 |
| B12 | 同 `:607` | 流程图行 |
| B13 | 同 `:47-58` 已知 Bug 节 | **保留** + 顶部加时限限定行 |
| B14 | 同 `:622` | 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` |
| **B15** | **`phase-d-closer/SKILL.md:41`** | **跨 Skill (R2 GOV-refuter)**: D.2 行的「(自动修正 CLI bug; …)」删除 |

**保留不改 (SC-4 的两个豁免区段, 按位置定义)**:
- **区段 (i)** = `## ⚠️ 已知 Bug` 标题行 (`:47`) 到其后第一条 `---` (`:58`)。区段内允许命中 `:47` `:49`; **`:56` 必须被 B6 改到不再命中** (它在区段内但是现时承诺)。
- **区段 (ii)** = **`## 变更历史`** (`:627`) 标题行到文件末尾 (机械边界, R2 ID-5/MISS-4: 上一版只写「文末 CHANGELOG 表格区」无锚)。区段内允许命中 `:632`。

**⚠️ 误伤守卫**: `Step2` 全文出现**恰好两次**, `:275` 的 `§Step2 warn_overlay` 是语义正确的交叉引用。**禁全局 `sed`**, 只改 `:317`。
**⚠️ 不重编 Step 编号**: Step 7 的编号被 `spec_complete.py:1251` 的 d_payload 文案引用。

**B1 改哪边的判据**: 代码是 `d_payload.body` 唯一运行时生产者; 改名有成文裁定 —— `openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/proposal.md:174` 逐字「**裁定: 保留改名, 收窄声称。**」并论证 `Step2` 是**事实错误**的引用 (`:172` 是论证段, 已逐字核)。

**B9 退役 `keep_changes_copy` 的三条实证**: 全仓只出现 2 次 (SKILL.md `:87` `:261`), 零代码消费方/零测试/零 eval; `changes/` 与 `archive/` slug **零重叠** ⇒ 历史从未行使; 若行使则同一 spec 同时在两处 ⇒ `collectors/openspec.py:208` 无条件枚举 `changes/` 计成**幽灵活跃变更**, 且 `:241` 让它永挂 `pending_archive`。
⚠️ **声明接口移除**, 须在 handoff 点名请 owner 复议 (memory `narrow-owner-options`)。**版本影响**: 该选项从未实现 (零代码宿主), 移除不构成运行时破坏性变更 ⇒ 仍 MINOR; 若 owner 裁定保留, B9 撤销, 版本级别不变 ⇒ 发版不阻塞于该复议。

### Part C — 机械兜底

**C1. `skill_md_literal_sync_probe.py`** → `aria/skills/state-scanner/scripts/` (随插件分发), 注册进本仓 `.aria/state-checks.yaml`。

**抽取锚点成文** (R1 AB-5/RF-2/RF-6 + R2 R1V-7):
- SKILL.md 侧: `"(> 归档 SHA 回链:[^"]*填入)"` —— **以「填入」结尾**是承重的, 它把 `:317` 的匹配串与 `:318` 的替换串区分开。
- ⚠️ **R2 R1V-7 抓到的自冲突**: 该唯一性依赖 `:318` 现文本以 `HEAD)` 结尾, 而 **B2 在同一份 Spec 里正要重写 `:318`**。⇒ **B2 的新文案硬约束: 不得以「填入」二字结尾**, 并在 B2 落地后**立即重跑 C1 的锚点唯一性** (基线命中数须仍为 1)。
- 生产者侧: `lines\.append\(\s*"(> 归档 SHA 回链:[^"]*)"\s*\)`。
- **两个文件路径钉死** (经 `CLAUDE_PLUGIN_ROOT` 优先、回落 `<repo>/aria`), **禁用 glob** —— 仓内有 AB skill-snapshot 冻结副本, glob 式实现会恒红。

**第三条断言** (R1 AC-1): 纯双边相等挡不住「两侧同步改回 `Step2`」(实测该坏实现 rc=0)。故追加: 命中串**必须含 `Step 7`** —— 该值有 2026-07-22 成文裁定背书, 不是任选常量。
> ⚠️ 诚实登记 (memory `author-to-match-checker`): 这条断言与 B1「把 SKILL.md 改成 Step 7」看起来是同义反复。辩护是「`Step 7` 钉的是**裁定过的真值**而非当前值」。**该辩护未经独立复核, 写进 handoff 请 owner 复议。**

**五态实测** (对齐 `collectors/custom_checks.py` 三态契约):

| 态 | 结果 |
|---|---|
| 基线 (本仓) | **FAIL** rc 1, 打印两侧原文 |
| 目标 (B1 落地后) | **PASS** rc 0 |
| 插件源码不可见 (采用方场景) | **SKIP** rc 0 + `##SKIP##` |
| 文件在但锚点提取数 ≠ 1 | **FAIL** rc 1 (fail-CLOSED) |
| 三个坏实现 (只比前缀 / 只比到步骤名前 / 两侧同改回 `Step2`) | 前两个基线 GREEN 已判无效; 第三个由 `Step 7` 断言拒掉 |

**C2. `archive_tracker_verify.py`** → **新建 `aria/skills/openspec-archive/scripts/`**; 单测 → **新建 `aria/skills/openspec-archive/tests/`**, 夹具 → 其下 `fixtures/`。

⚠️ **必须避开 harness 假绿陷阱** (`10CG/aria-plugin#187`, 本 session 实测并已最小止血): `run_all_tests.sh` 靠 `find skills -type d -name tests` 自动发现套件, 但若目录里只有 pytest 风格裸函数且无 `conftest.py`, 会落 `unittest discover` ⇒ **收集 0 个** ⇒ 打印 `OK (0 tests)` 且退出码 0。⇒ 新建的 tests 目录**必须带 `conftest.py`**, 且落地后须核 `run_all_tests.sh` 里该行的测试数**非 0**。

**夹具契约**: **冻结快照**, 不实时抓 API (issue body 可被编辑)。每份注明来源 `10CG/Aria#<n>` 与抓取时刻。

**五态实测**:

| 夹具 | 结果 |
|---|---|
| `10CG/Aria#201` (含 `4c3c826`) | rc 0 OK |
| `10CG/Aria#185` (行在无 SHA) | rc 1 NO_SHA |
| `10CG/Aria#186` (无回链行) | rc 1 MISSING |
| 合成 `synth-short` (尾部含短十六进制 `abc`) | rc 1 NO_SHA |
| body 取不到 | rc 2 **fail-CLOSED** |

坏实现拒绝: 「只查行存在」在 #185 上 GREEN ⇒ 无效; 「`[0-9a-f]+` 无长度下限」在 **#185 上也红** (该真语料尾部纯中文, 零 ASCII 十六进制) ⇒ **真语料证不了长度下限**, 必须靠合成夹具。

> ⚠️ **R1 AB-3 / R2 R1V-2 未完全解决, 诚实登记**: B2 的「强制调用 C2」仍是写给 AI 读的自然语言指令 —— 与 Spec 自己实证 6/6 失效的是**同一条通道**。C2 给了**断言**一个代码宿主, 没给**调用**一个宿主。真正的常驻宿主需要把校验挂进 `.aria/state-checks.yaml` 或 D.2 闸门, 但两者都要求「本次刚建的 issue 号」这个运行时输入, 现有机制拿不到。**本 Spec 不假装解决了它**; 已开 `10CG/aria-plugin#189` 跟踪 (见 D9)。

### Part D — 开单 (九条, 全部带仓限定 + 回读核验)

| # | 内容 | 仓 |
|---|---|---|
| D1 | AB 固定套件缺 Step 7 / D auto-issue 维度 (`ab-suite/openspec-archive.json` 只选 2/4 eval) — Rule #6 SOT §3 第 3 条强制 | `10CG/aria-plugin` |
| D2 | openspec-archive evals **三个**涉及「正确归档路径」的 eval 全部缺强制 `YYYY-MM-DD-` 前缀 (含**已被选进套件**的 eval 1); `cli-bug-fix` 的 `cli_wrong_path` 与 SOT 矛盾; 断言首句 `openspec/archive` 是次句的**真子串** ⇒ 零判别力 | `10CG/aria-plugin` |
| D3 | `unverified_claims` / `unverified_ack` frontmatter 只写不读 (`spec_complete.py:103` 自承) | `10CG/aria-plugin` |
| D4 | `standards/openspec/AGENTS.md:57` 悬空脚本 `verify-openspec-archive.sh` | `10CG/aria-standards` |
| D5 | `spec-drafter/SKILL.md:192 :507 :510` 三处指示运行未安装的 `openspec validate --strict` (同类兄弟位置; 未纳入因「用什么替代校验」是未解设计题, 且会触发第三个 AB 套件) | `10CG/aria-plugin` |
| D6 | ⏰ **有日期**: `check-m6-e2e-acceptance` 判 dead。**引信行是 `aria-2.0-m6-e2e-resilience/tasks.md:353`** (行内写全仓相对路径 ⇒ dead ⇒ **block**), **不是 `:380`** (裸文件名 ⇒ ambiguous ⇒ 仅 warn) — 两行分类已主控实跑复核。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免 | `10CG/Aria` |
| D7 | **已开** `10CG/aria-plugin#187` — `run_all_tests.sh` 收集 0 个测试却报 OK (本 session 已最小止血: `phase-d-closer` 0 → 11 tests, 全套件 2111 → **2122**) | `10CG/aria-plugin` |
| D8 | **已开** `10CG/aria-plugin#188` — Part A 拆出件 (谓词 V4 设计 + 21 用例 + 零触达测量) | `10CG/aria-plugin` |
| D9 | **待开** — Step 7 的「强制调用」无常驻代码宿主 (见 Part C2 登记) | `10CG/aria-plugin` |

### Part E — 发版同步面

Part B/C 全部落在 `aria` 子模块 ⇒ 必须发版。

- **级别 MINOR** — 依据 `standards/conventions/version-management.md §2.2` 逐字的「**功能增强（向下兼容）**」: C1/C2 是两个随插件分发的新探针。v1.71.1 → **v1.72.0**。
- **同步面实测**: `1.71.1` 共 **23 处 / 13 文件** —— aria 子模块 7 处 (plugin.json 1 / marketplace.json 2 / VERSION 2 / CHANGELOG 1 / README 1) + 主仓 **16 处** (VERSION 1 / CLAUDE.md 2 / README.md 2 / zh 3 / ja 3 / ko 3 / system-architecture 1 / version-scheme 1)。主仓 16 与前 cycle commit `4c3c826` 精确对账。
- **不改**: `.aria/triage-*` / `docs/handoff/*` / 本 proposal 引前序版本处 (历史记录)。
- **Rule #3 文档同步**: `aria/skills/openspec-archive/CHANGELOG.md` 的 `[Unreleased]` 段须加条目 (R2 GOV-2)。**已核**: `docs/architecture/*.md` 对归档手法**零命中**, 无需同步; `aria/README.md` 的 skill 名册中 openspec-archive **在册**。
- **机械兜底须全绿**: `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency` / `m6-claude-md-version` / `plugin-cache-currency`。i18n README **仅正文实质变更才重译** (#140 B 档)。

---

## Rule #6 判定 (逐 hunk, `rule6_note`)

SOT: `standards/conventions/skill-benchmark-exemption.md` v1.0.0 (逐字读过)。

**决定性事实**: **B3 改的 `openspec-archive/SKILL.md:4` 就是 frontmatter `description`**。SOT §2 附加约束逐字: 「仅当变动是事实性同步 … 且 frontmatter `description` **零变动**, 才可能落进第一行; **`description` 或指令流程变动 ⇒ 一律第二行**」。

⇒ **openspec-archive 侧整体第二行, 照跑 AB, 零裁量。**

**phase-d-closer 侧 (B15) 落第一行 substitute**: 它改的是一张**描述另一个 Skill 职责**的表格行, 属 SOT §2 附加约束的「事实性同步 (术语修正)」, 且 phase-d-closer 自己的 `description` 零变动。

**⚠️ 上呈复议项 (Rule #10, 不由 AI 终局) — 上一版曾以「两次先例」为由删除本项, 那是基于未核实的证据链自行豁免, 已订正**:

SOT §1「任一 hunk 处方性且在测量范围内 ⇒ **整个变更**照跑」的语境是同一文件内 hunk 并存, 未明文覆盖「一个 Spec 跨两个 Skill」时作用域是否及于另一 Skill 的套件。

- **有一次同形状 shipped 先例**: aria-plugin **v1.69.1** (2026-09-04) 同时改 spec-drafter 指令面与 `spec_complete.py` 分类器, CHANGELOG 逐字「路径 + hunk A 两处是处方性运行时指令面 ⇒ **照跑 AB** (`ab-suite/spec-drafter.json`)… **分类器改动为描述性 ⇒ substitute**」; `ab-results/` 目录实测该批只有 spec-drafter 一个套件。
- **但 v1.71.1 不是先例** —— 其 CHANGELOG 逐字「纯代码, **零 SKILL.md / description 变更**」, 是**单 Skill** 变更。
- 按 memory `exact-exception-condition`「**N 次非正式援引 ≠ 成文 lane**」, **一次先例不构成 Rule #10 白名单里的「已成文 lane」**。

⇒ 本 Spec 按 v1.69.1 的形状执行 (openspec-archive 照跑, phase-d-closer substitute), 但**上呈 owner 裁**: (a) ratify 成 lane 并写进 SOT §5, 或 (b) 另裁 (含补跑 phase-d-closer AB)。

> ⚠️ **R2 R1V-6 登记**: SC-7 要求的 AB 在现有 2 个 eval 上**可预测为零区分** —— 本 Spec 自己的 D1/D2 正说明该套件测不到 Step 3/4/7。这与 SOT §3 警告的「测量剧场」同形。但 `description` 变动使本变更落第二行是 SOT 的**明文映射**, 不是我的裁量。**处置**: 照跑, 并在 RESULT.md 里**显式记录「本次 AB 对本改动零区分力, 区分力缺口见 D1」**, 不把「跑过了」当成「验过了」。

---

## 验收标准

- **SC-1** (B, **机械判据**): 落地后跑
  `grep -rnE 'openspec (archive|validate|CLI)|CLI[^。]{0,12}bug|CLI 完成|安装 openspec|自动修正|修正 CLI|CLI 归档' aria/skills/openspec-archive/SKILL.md aria/skills/phase-d-closer/SKILL.md`,
  **落在两个豁免区段之外的命中数 == 0**。区段按**位置**定义: (i) `## ⚠️ 已知 Bug` 标题行到其后第一条 `---`; (ii) **`## 变更历史`** (`:627`) 标题行到文件末尾。
  区段内允许命中集合 **逐行钉死 = {`:47`, `:49`, `:632`}**; **`:56` 虽在区段 (i) 内但必须被 B6 改到不再命中** (它是现时承诺)。
  **基线实测** (脚本按上述区段定义实跑, 锚点名已实测非手写 —— 本版初稿写的「## 版本历史」在文件里不存在, 解析器返回 None 会让 `:632` 误落区段外, 已订正为 `## 变更历史`):
  openspec-archive 总命中 **16**, 区段内 **4** (`:47 :49 :56 :632`), **区段外 12** (`:4 :17 :40 :41 :247 :248 :249 :392 :393 :401 :588 :607` —— 与 B3/B4/B5/B7/B10/B11/B12 **一一对应**); phase-d-closer **区段外 1** (`:41`)。**⇒ SC-1 基线区段外合计 = 13**。
  (spec-drafter 的 `:192 :507 :510` 属 D5, **不在本 SC 的 grep 目标文件内**。)
- **SC-2** (B, 误伤守卫): `grep -c 'Step2' openspec-archive/SKILL.md` == **1** 且唯一命中在 `:275`。
- **SC-3** (B8/B10 落地形态): Step 5 段落体为**一行 pointer**且编号保留; 示例 1 的 `:392 :393 :394 :401` 四行全部同步 (R2 ID-3 点名 `:394` 原先漏枚举)。
- **SC-4** (B9): `keep_changes_copy` 在 SKILL.md 中命中数 == 0 或仅出现在「已退役」说明里。
- **SC-5** (C1 五态): 见 Part C1 表, 五态均留实跑输出; 三个坏实现均被拒。**外加 B2 落地后重跑锚点唯一性** (命中数须仍为 1)。
- **SC-6** (C2 五态): 夹具为冻结快照, 每份注明 `10CG/Aria#<n>` 与抓取时刻; 含合成 `synth-short`。
  **外加**: `bash aria/skills/run_all_tests.sh` 里 `openspec-archive` 那行的测试数 **非 0** (防 `10CG/aria-plugin#187` 的假绿)。
- **SC-7** (Rule #6): openspec-archive AB 跑完, 留 `ab-results/2026-09-XX-v1.72.0-archive-skill-drift/RESULT.md`; 两臂 = **v_new vs v_old** (SOT §6: with/without 那列因 CLAUDE.md 污染不可用); **RESULT.md 须显式记录本次 AB 对本改动的区分力评估** (预期为零, 见 R1V-6 登记)。
- **SC-8** (D): D1-D6 + D9 开单并回读核验, issue 号**带仓限定**记入 tasks.md; D7/D8 已开, 记号即可。D6 须在 handoff 单独点名。
- **SC-9** (E): `aria/.claude-plugin/plugin.json` == `1.72.0`; 23 处版本点全同步; 六个版本类 custom check 全绿; `openspec-archive/CHANGELOG.md` `[Unreleased]` 有条目; **两仓** (`10CG/Aria` + `10CG/aria-plugin`) 逐 remote `ls-remote` 核验 (R2 MISS-5: 上一版写「三仓」但本 Spec 不动 standards)。
- **SC-10** (回归): `cd aria/skills/state-scanner/tests && python3 -B run_tests.py` ≥ **1575 / OK** (canonical 口径); 全套件 `bash aria/skills/run_all_tests.sh` ≥ **2122** 且 0 FAIL (基线实测, 已含 `#187` 止血带来的 +11)。
  ⚠️ canonical runner 对 state-scanner 用的是 `run_tests.py` 不是 pytest (pytest 口径为 1603, 两种发现方式收集集不同)。

### 验收项基线实跑 (memory `spec-acceptance-needs-baseline-run`)

| SC | 基线实测 | 期望 | 红? |
|---|---|---|---|
| SC-1 | 区段外命中 **13 行** (openspec-archive 12 + phase-d-closer 1) | 区段外 0 | ✅ |
| SC-2 | `grep -c 'Step2'` = **2** | 1 | ✅ |
| SC-3 | Step 5 是完整段落; `:394` 未在任何枚举里 | 一行 pointer; `:394` 已改 | ✅ |
| SC-4 | `keep_changes_copy` 出现 2 次 (`:87` `:261`) | 0 或仅退役说明 | ✅ |
| SC-5 | rc 1 + 两坏实现基线 GREEN + 提取失败 rc 1 | rc 0 | ✅ |
| SC-6 | 脚本与 tests 目录均不存在 | 五态可分辨 + 测试数非 0 | ✅ |
| SC-7 | AB 未跑 | RESULT.md 存在且含区分力评估 | ✅ (do-it) |
| SC-8 | `10CG/aria-plugin` 仓标题含 `Step 7` / `cli-bug-fix` / `unverified_claims` / `openspec validate` 的 issue 各 **0** 条 | D1-D6+D9 已开 | ✅ |
| SC-9 | plugin.json = `1.71.1` | `1.72.0` | ✅ |
| SC-10 | state-scanner **1575 OK**; 全套件 **2122**, 10 OK / 0 FAIL | ≥ 同值 | 基准值 |

---

## 非目标

- **不安装 `openspec` CLI** (引入外部依赖属产品级决定, 上呈 owner)。
- **不改 `spec_complete.py`** —— 包括 `:1251` 的生产文案 (改名有成文裁定)。本 Spec 对该文件**只读**。
- **不做 Part A** (归档闸门谓词) —— 已拆入 `10CG/aria-plugin#188`, 依据是生产触达实测为 0。
- **不修 D5 (spec-drafter) / D6 (M6 acceptance) / D9 (Step 7 调用宿主)** —— 只开单。
- **不修 `10CG/aria-plugin#187` 本体** (`run_all_tests.sh` 的判据缺陷); 本 session 已做最小止血 (`phase-d-closer/tests/conftest.py`), 判据修复留给该 issue。
- **不动 `aria-orchestrator`** (他轨 `feature/m6-cost-model-telemetry`)。
