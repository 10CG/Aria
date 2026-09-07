# openspec-archive 文档/实现漂移收口 — 类级补齐 + 两个机械兜底

> **Level**: 3 (Full — `openspec-archive/SKILL.md` 指令面变更 + `phase-d-closer/SKILL.md` 与两份 README 的**描述性**事实同步 + 三个新脚本 + 九条开单 + 发版同步面; 四个 task group)
> ⚠️ 措辞承重: 只有 openspec-archive 那侧是**指令面**变更; phase-d-closer 与 README 是**描述性**事实同步 —— 这与 Rule #6 判定表把它们判进第一行是同一件事, 两处不得说法不一 (R4 `fixes-contradict` 抓到)。
> **Status**: Draft (Phase A.1; post_spec R1→R2→R3 已跑, 本文为 R3 修订版)
> **Change ID**: `archive-gate-registration-class-and-skill-drift`
> **Linked Issue**: `10CG/aria-plugin#186` (类级排查总 tracker)
> **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2`
> **前序**: `a1-entry-claim-duplicate-work-guard` (2026-09-06 归档) 的 carry-forward M2
>
> ### ⚠️ 跨仓 issue 号纪律 (R1 RF-4 → R2 R1V-8 → R3 GOV-2, **连三轮被抓**)
> **全文所有 issue 号一律写 `<org>/<repo>#<n>`。** 已知真实撞号: `10CG/aria-plugin#186` vs `10CG/Aria#186`; `10CG/aria-plugin#185` vs `10CG/Aria#185`。
> **机械自检 (落地前必跑, 不再靠人工通读 —— 那正是连三轮复发的根因)**:
> 用 `aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal.md>` (Part C3), **exit 0 = 无裸引用**。
> 它必须排除三类**不是** issue 引用的 `#<n>`: (a) `Rule #N` / `规则 #N` 规则编号; (b) 反引号 code span 内逐字引用的目标文件原文 (如 B15 的目标行含 `#95`); (c) 已带 `<org>/<repo>` 限定的。
> **三态实测**: 本版 **0** (rc 0) / R3 修订前版 **3** (rc 1 — 恰是 R3 审计席点名的 `:130` 两处 + `:156` 一处, 正控成立) / **坏实现** (不排除上述三类的裸 `grep -cE '(^|[^/A-Za-z0-9-])#[0-9]+'`) 在本版报 **9**、在 R3 修订前版报 **10** ⇒ **判无效**。
> ⚠️ **R4 抓到的自伤**: 上一版把**那个坏实现的命令**写进了本处 (并声称负控是 3), 而 3 是正确实现的输出 —— 手抄命令而非引用实跑的那个 (memory `pasted-evidence-is-derived`)。本处现改为**只引脚本路径, 不复述命令**。
>
> ### 🔀 Part A 已拆出 (2026-09-07 owner 裁定) → `10CG/aria-plugin#188`
> 原 Part A (归档闸门 `python -m` 谓词) 连同 V4 设计、三处接入点、21 个对抗用例、基线三态全部随迁。
> **拆分依据是实测**: 沿生产链 (`extract_claim_symbols`) 测得 7 个活跃 spec 抽出 **0 个**符号; 最近 59 个 spec 抽出 18 个, 父目录是真 Python 包 (谓词唯一能锚定的形态) 的 **0 / 18**; 全仓 20 处 `-m <点分路径>` 命中**全在** `aria-orchestrator/hermes-extensions/aria-layer1/`, 而无任何 spec 声称过该包里的符号。
> ⇒ 那个修复会带着全绿测试 ship 而生产触达为 0 (memory `completion_signals_vs_runtime_invocation`)。
> 拆分不制造接缝: 本 Spec 余下部分对它**零实现/零引用/零导出依赖**。

---

## Why

母 Spec 交接记了 `openspec-archive/SKILL.md` 两处与实现漂移 (M2)。Phase A.1 取证证实漂移、**推翻其后果推断**, 并在三轮审计中把「类」从 5 处推到 **20 行、跨两个 SKILL.md + 两份 README**。

### 三个反转

**反转 1 — `openspec archive` CLI 是个不存在的东西, 而 SKILL.md 把它当核心动作。**
`command -v openspec` 无输出; CLI 工作区 (`openspec/project.md`) 从未初始化; 审计报告 `post_planning-R1-2026-07-19-...:33` 明文承认手工 `git mv`; **144** 份归档中 **134 份 (93%)** 无 Step 2 的任何 frontmatter 写入痕迹; 归档条目 rename/add 实测 **102 R + 42 A = 144**。

**反转 2 — 交接记的「SHA 逐字匹配静默落空 ⇒ 永远填不进去」不成立。**
漂移是真的 (`SKILL.md:317` 写 `Step2`, `spec_complete.py:1251` 写 `Step 7`, difflib 逐字符 diff = 单一 opcode `replace '2' -> ' 7'`)。但全仓**无 `str.replace`** —— 那是给 AI 的自然语言指令。`10CG/Aria` 仓 6 个 `[Archive Tracker]` issue 全量翻页核过: **3/6 含 SHA**。真缺陷是 Step 7 的 SHA 填充**没有代码宿主** —— 6 次执行 4 种形态, `10CG/Aria#185` 被替换成一句完全不含 SHA 的话而无人发现。

**反转 3 — 「类级补齐」连漏四次。**
R1 枚举 5 处 → R1 修订 12 处 → R2 抓到 `SKILL.md:17` (**逃出了判据自己的 grep 模式**: `CLI 归档位置 bug` 不匹配 `CLI bug`) 与 `phase-d-closer/SKILL.md:41` → **R3 又抓到 `aria/README.md:85` 与 `aria/README.zh.md:85`** —— 它们此刻就逐字带着 B3 要删的那句现时声称 (`(auto-fixes CLI bugs)` /「（自动修正 CLI bug）」), 而且是**采用者最显眼的入口**。
⇒ 本版的类级枚举**先跑加宽 grep 再定表**, 判据从「文件目录」改成「**含同一句现时声称的每一处**」, 且 SC-1 的 grep 目标扩到四个文件。

---

## What Changes

### Part B — CLI 漂移类级收口 (两个 SKILL.md + 两份 README, 20 行)

> **通用 post-condition (R3 RFV-3)**: B3-B17 里每一条「改写」类改动, 改后该行**必须不再命中 SC-1 的 pattern**。凡本表只给方向未给字面文案的, 落地时须先用该 pattern 自测再落盘。

| # | 位置 | 改动 |
|---|---|---|
| B1 | `openspec-archive/SKILL.md:317` | `Step2` → `Step 7` (对齐 `spec_complete.py:1251`) |
| B2 | 同 `:318` + Step 7 段落 | 替换文案改为可验证约束 (必须含 7-40 位十六进制 SHA) + 写明调用 C2。**硬约束: 新文案不得以「填入」二字结尾** (否则会破坏 C1 的锚点唯一性, 见 Part C1) |
| B3 | 同 **`:4`** | **frontmatter `description`** —— 删「自动修正 CLI bug」。⚠️ **这条决定 openspec-archive 侧的 Rule #6 档位** |
| B4 | 同 **`:17`** | 历史行改写。**候选文案 (已实测对 SC-1 pattern 零命中)**: `> **历史**: 2026-02-08 - 初始版本，修复归档目录落点错误 (彼时经由外部工具链, 现已改为 git mv)` |
| B5 | 同 `:40` + `:41` | 核心功能表**两行的两个单元格全部重写** (不是只换标签): `:40` 执行归档 → `git mv …`; `:41` 自动修正 → 位置校验 |
| B6 | 同 `:56` | 「**本 Skill 会自动修正此问题**」→ 对采用者的条件表述 (它是现时承诺, 不是历史陈述) |
| B7 | 同 `:247` `:248` `:249` **三行各自给目标** (R3 IMPL-3): `:247` 标题 → `Step 3 - 执行归档 (git mv):`; `:248` 命令 → `git mv openspec/changes/{change_name} openspec/archive/{YYYY-MM-DD}-{change_name}`; `:249` → `等待: git mv 返回` | ⚠️ 占位符用 `{change_name}` —— 全文件既有惯例, `{id}` 从未出现过 |
| B8 | 同 `:251-257` + `:259-261` | **Step 4 目标字面** (三行断言, 替换原「检测并修正归档位置」整块):<br>`Step 4 - 归档后位置校验:`<br>`  断言 1: openspec/archive/{YYYY-MM-DD}-{change_name}/ 存在`<br>`  断言 2: openspec/changes/{change_name}/ 已不存在 (git mv 的必然结果)`<br>`  断言 3: openspec/changes/archive/ 不存在 (若存在 ⇒ 历史上有人走过 CLI 路径, 搬到 openspec/archive/ 后 rmdir)`<br>**Step 5 目标字面** (保留编号, 整块压成标题行本身, 其下无正文):<br>`Step 5 - (已并入 Step 3: git mv 使源目录必然消失)` |
| B9 | 同 `:87` | 退役 `keep_changes_copy`, 移入新增小节 `## 已退役配置项` (给 SC-4 第二分支一个可 grep 的锚点) |
| B10 | 同 `:392` `:393` **`:394`** `:401` | 示例 1 四行 |
| B11 | 同 `:588` | 错误表 CLI 行 → `git mv` 失败三分支 |
| B12 | 同 `:607` | 流程图行 |
| B13 | 同 `:47-58` 已知 Bug 节 | **保留**; 时限限定行插在**标题行 `:47` 之后、`**问题**:` 行之前**, 作为小节正文第一行 |
| B14 | 同 `:622` | 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` |
| B15 | **`phase-d-closer/SKILL.md:41`** | 删括号内声称。**目标行完整字面**: `| D.2 | openspec-archive | Spec 归档 (**#95 完成度 + C 分级证据闸 tri-state verdict, verdict=block 时本步 BLOCK**) | spec_archived |` |
| **B16** | **`aria/README.md:85`** | **R3 新增**: `- openspec-archive — Archive completed OpenSpec changes to openspec/archive/ with post-move location checks` (已实测零命中) |
| **B17** | **`aria/README.zh.md:85`** | **R3 新增**: `- openspec-archive — 归档已完成的 OpenSpec 变更到 openspec/archive/ 并做落点校验` (已实测零命中) |

**保留不改 (SC-1 的两个豁免区段, 按位置定义)**:
- **区段 (i)** = `## ⚠️ 已知 Bug` 标题行到其后第一条 `---` (基线 `:47`-`:58`)
- **区段 (ii)** = `## 变更历史` 标题行到文件末尾 (基线 `:627`-EOF)
- `:56` 虽在区段 (i) 内但**必须被 B6 改到不再命中** (现时承诺, 非历史陈述)

**⚠️ 误伤守卫**: `Step2` 全文出现恰好两次, `:275` 的 `§Step2 warn_overlay` 是语义正确的交叉引用。**禁全局 `sed`**。
**⚠️ 不重编 Step 编号**: Step 7 的编号被 `spec_complete.py:1251` 的 d_payload 文案引用。

**B1 改哪边的判据**: 代码是 `d_payload.body` 唯一运行时生产者; 改名有成文裁定 —— `openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/proposal.md:174` 逐字「**裁定: 保留改名, 收窄声称。**」并论证 `Step2` 是**事实错误**的引用。

**B9 退役 `keep_changes_copy` 的三条实证**: 全仓只出现 2 次 (SKILL.md `:87` `:261`), 零代码消费方/零测试/零 eval; `changes/` 与 `archive/` slug **零重叠** ⇒ 历史从未行使; 若行使则同一 spec 同时在两处 ⇒ `collectors/openspec.py:208` 计成**幽灵活跃变更**且 `:241` 让它永挂 `pending_archive`。
⚠️ **声明接口移除**, handoff 点名请 owner 复议。**版本影响**: 该选项从未实现 (零代码宿主) ⇒ 移除不构成运行时破坏性变更 ⇒ 仍 MINOR; owner 若裁定保留则 B9 撤销, 版本级别不变 ⇒ **发版不阻塞于该复议**。

### Part C — 机械兜底

**C1. `skill_md_literal_sync_probe.py`** → `aria/skills/state-scanner/scripts/` (随插件分发), 注册进本仓 `.aria/state-checks.yaml`。

**抽取锚点成文**:
- SKILL.md 侧 `"(> 归档 SHA 回链:[^"]*填入)"` —— **以「填入」结尾**是承重的 (把 `:317` 匹配串与 `:318` 替换串分开)。⚠️ 该唯一性依赖 `:318` 不以「填入」结尾 ⇒ **B2 已加对应硬约束**, 且 B2 落地后须**立即重跑锚点唯一性** (命中数须仍为 1)。
- 生产者侧 `lines\.append\(\s*"(> 归档 SHA 回链:[^"]*)"\s*\)`。
- **两个文件路径钉死** (`CLAUDE_PLUGIN_ROOT` 优先、回落 `<repo>/aria`), **禁用 glob** (仓内有 AB skill-snapshot 冻结副本, glob 会恒红)。

**第三条断言**: 双边相等挡不住「两侧同步改回 `Step2`」。故追加 `REQUIRED_STEP = "Step 7"` 判断 —— 该值有 2026-07-22 成文裁定背书, 不是任选常量。
> ⚠️ **R3 ACC 抓到并已修**: 该断言此前**只写在 proposal 里, 探针脚本中并不存在**, 五态表第五行是假的。现已写入脚本并重跑, 见下表。

**五态实测 (探针含第三条断言后重跑)**:

| 态 | 结果 |
|---|---|
| 基线 (本仓, 两侧不等) | **FAIL** rc 1, 打印两侧原文 |
| 目标 (B1 落地后) | **PASS** rc 0 |
| 插件源码不可见 (采用方场景) | **SKIP** rc 0 + `##SKIP##` |
| 锚点提取数 ≠ 1 | **FAIL** rc 1 (fail-CLOSED) |
| **坏实现「两侧同改回 `Step2`」** | **FAIL** rc 1 —— 修前实测 rc 0 (假绿), 修后打印「两侧一致但值错了 (缺 'Step 7')」 |

另两个坏实现 (只比前缀 / 只比到步骤名前) 在基线上 GREEN ⇒ 已判无效。

**C2. `archive_tracker_verify.py`** → **新建 `aria/skills/openspec-archive/scripts/`**; 单测 → **新建 `aria/skills/openspec-archive/tests/`** (含 `conftest.py`), 夹具 → 其下 `fixtures/`。

⚠️ **必须带 `conftest.py`** —— `run_all_tests.sh` 靠 `find skills -type d -name tests` 自动发现, 但目录里只有 pytest 风格裸函数且无 `conftest.py` 时会落 `unittest discover` ⇒ 收集 0 个 ⇒ 打印 `OK (0 tests)` 且退出码 0 (`10CG/aria-plugin#187`; 本 session 已用同一手法修好 `phase-d-closer`, 实测 0 → 11 tests)。

**夹具契约**: **冻结快照**, 不实时抓 API。每份注明来源 `10CG/Aria#<n>` 与抓取时刻。

**五态实测**: `10CG/Aria#201` rc 0 OK / `10CG/Aria#185` rc 1 NO_SHA / `10CG/Aria#186` rc 1 MISSING / 合成 `synth-short` rc 1 NO_SHA / body 取不到 rc 2 fail-CLOSED。
坏实现拒绝: 「只查行存在」在 `10CG/Aria#185` 上 GREEN ⇒ 无效; 「`[0-9a-f]+` 无长度下限」在该真语料上**也红** (尾部纯中文零 ASCII 十六进制) ⇒ **真语料证不了长度下限**, 必须靠合成夹具。

> ⚠️ **诚实登记 — 未解决的另一半**: B2 的「调用 C2」仍是写给 AI 读的自然语言指令, 与 Spec 自己实证 6/6 失效的是**同一条通道**。C2 给了**断言**代码宿主, 没给**调用**宿主。两条现有机制都试过且实测不成立 (定期扫全部 tracker ⇒ 恒红 3/6; 只扫 open ⇒ 恒绿 2/2; 按 marker 过滤无效 ⇒ 6/6 都带 marker)。**本 Spec 不假装解决它**, 已开 `10CG/aria-plugin#189` (D9)。

**C3. `check_bare_issue_refs.py`** → `aria/skills/state-scanner/scripts/` (随插件分发)。
守「Spec 文档里的 issue 引用必须带 `<org>/<repo>` 限定」这条纪律 —— 该纪律在本 Spec 上**连三轮复发** (R1 RF-4 → R2 R1V-8 → R3 GOV-2), 靠人工通读修不住。
排除三类非 issue 引用: `Rule #N` / `规则 #N`; 反引号 code span 内; 已带仓限定的。
**三态实测**: 本版 proposal **0** (rc 0) / R3 修订前版 **3** (rc 1, 正控) / 坏实现 (裸 grep 不排除三类) 在两版分别报 **9** 与 **10** ⇒ 判无效。

### Part D — 开单 (九条, 全部带仓限定 + 回读核验)

| # | 内容 | 仓 | 状态 |
|---|---|---|---|
| D1 | AB 固定套件缺 Step 7 / D auto-issue 维度 (`ab-suite/openspec-archive.json` 只选 2/4 eval) — Rule #6 SOT §3 第 3 条强制 | `10CG/aria-plugin` | 待开 |
| D2 | openspec-archive evals **三个**涉「正确归档路径」的 eval 全缺 `YYYY-MM-DD-` 前缀 (含**已选进套件**的 eval 1); `cli-bug-fix` 的 `cli_wrong_path` 与 SOT 矛盾; 断言首句是次句的**真子串** ⇒ 零判别力 | `10CG/aria-plugin` | 待开 |
| D3 | `unverified_claims` / `unverified_ack` frontmatter 只写不读 (`spec_complete.py:103` 自承) | `10CG/aria-plugin` | 待开 |
| D4 | `standards/openspec/AGENTS.md:57` 悬空脚本 `verify-openspec-archive.sh` | `10CG/aria-standards` | 待开 |
| D5 | `spec-drafter/SKILL.md:192 :507 :510` 三处指示运行未安装的 `openspec validate --strict` | `10CG/aria-plugin` | 待开 |
| D6 | ⏰ **有日期**: `check-m6-e2e-acceptance` 判 dead。**引信行是 `aria-2.0-m6-e2e-resilience/tasks.md:353`** (全仓相对路径 ⇒ dead ⇒ **block**), **不是 `:380`** (裸文件名 ⇒ ambiguous ⇒ 仅 warn)。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免 | `10CG/Aria` | 待开 |
| D7 | `run_all_tests.sh` 收集 0 个测试却报 OK (本 session 已最小止血: `phase-d-closer` 0 → 11 tests, 全套件 2111 → **2122**) | `10CG/aria-plugin#187` | ✅ 已开 |
| D8 | Part A 拆出件 (谓词 V4 + 21 用例 + 零触达测量) | `10CG/aria-plugin#188` | ✅ 已开 |
| D9 | Step 7 的 SHA 回链填充无**调用**宿主 | `10CG/aria-plugin#189` | ✅ 已开 |

### Part E — 发版同步面

- **级别 MINOR** — `standards/conventions/version-management.md §2.2` 逐字「**功能增强（向下兼容）**」: C1/C2 是两个随插件分发的新探针。v1.71.1 → **v1.72.0**。
- **版本串同步面实测**: `1.71.1` 共 **23 处 / 13 文件** —— aria 子模块 7 处 (plugin.json 1 / marketplace.json 2 / VERSION 2 / CHANGELOG 1 / README 1) + 主仓 **16 处** (VERSION 1 / CLAUDE.md 2 / README.md 2 / zh 3 / ja 3 / ko 3 / system-architecture 1 / version-scheme 1)。主仓 16 与前 cycle commit `4c3c826` 精确对账。
- **⚠️ 主仓 gitlink (R3 RFV-7 补入 —— 六个版本类 custom check 无一覆盖它, 且仓内此刻就漂移)**: 主仓记录 `301641b`, aria 子模块 HEAD 已是 `3a28339` (D7 止血 commit)。C.2 合并后须 bump 到 aria master 的 post-merge SHA。
- **i18n README 重译判据**: `README.zh.md` / `README.ja.md` / `README.ko.md` **仅正文实质变更才重译** (`10CG/Aria#140` B 档; CLAUDE.md §版本管理)。本 Spec 只改版本串 ⇒ **不触发重译**。
  ⚠️ 但 **B17 改的是 `aria/README.zh.md` 的正文** (skill 名册那行), 属实质变更 —— 故 B16/B17 两份须**同批改到语义一致**, 不适用「只改版本号不重译」那条。
- **机械兜底须全绿**: `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency` / `m6-claude-md-version` / `plugin-cache-currency`。
  ⚠️ **覆盖面诚实登记 (R4 GOV 逐个读源码所得)**: 这六个 check 合计只覆盖 **23 处版本点里的约 6 处**; 至少 17 处 (**含全部 7 处 aria 子模块点位**) 不受任何机械检测覆盖。⇒ SC-9 的「23 处全同步」**不能只靠这六个 check 判绿**, 必须逐文件 `grep -c` 实测并把 13 行计数贴进 tasks.md (与 gitlink 那条同等对待, 不留不对称缺口)。
- **不改**: `.aria/triage-*` / `docs/handoff/*` / 本 proposal 引前序版本处 (历史记录; 六个 custom check 按显式文件+窄正则比对, 对这些文件免疫)。
- **Rule #3 文档同步**: `aria/skills/openspec-archive/CHANGELOG.md` 的 `[Unreleased]` 段须加条目。**已核**: `docs/architecture/*.md` 对归档手法**零命中**; `aria/README.md` / `README.zh.md` 的 openspec-archive 行**在册且带同一句现时声称** ⇒ 已纳入 B16/B17 (R3 RFV-2 订正 —— 上一版的「已核: 名册在册」答的是另一个问题)。

---

## Rule #6 判定 (逐 hunk, `rule6_note`)

SOT: `standards/conventions/skill-benchmark-exemption.md` v1.0.0。**本版按 §2 的逐 hunk 决策表对三侧各自独立判定, 不依赖对 §1「整个变更」跨 Skill 作用域的任何解读** (R3 GOV-1 订正 —— 上一版把结论建立在一个自己论证为「不成立」的先例上, 构成 Rule #10 自行豁免)。

| 侧 | hunk | 档位 | SOT 依据 (逐 hunk, 非跨 Skill 推演) |
|---|---|---|---|
| **openspec-archive** | B1-B14 | **第二行 · 照跑 AB, 零裁量** | B3 改的 `:4` 就是 frontmatter `description`。§2 附加约束逐字: 「**`description` 或指令流程变动 ⇒ 一律第二行**」 |
| **phase-d-closer** | B15 | 第一行 **substitute** | §2 第一行 + 附加约束: 改的是**描述另一 Skill 职责**的表格行 = 事实性同步 (术语修正), 且 phase-d-closer 自己的 `description` **零变动**。substitute 物 = SC-1 的机械判据 |
| **state-scanner** | C1 落点 | 第一行 **substitute** | **R3 RFV-6 补入**: 纯新增探针脚本, 不被 state-scanner 自身流程调用, 其 `SKILL.md` 与 `description` **零变动**。判据同 v1.69.1 对 `spec_complete.py` 的处置。substitute 物 = SC-5 的五态实跑 (baseline-failing 结构化测试) |
| README ×2 | B16/B17 | 不适用 | 非 Skill 内容 (插件门面文档), 不在 Rule #6 判据表覆盖范围 |

**⇒ 只跑 openspec-archive 一个套件。** 三侧的档位各自来自 §2 的**明文映射**, 无一依赖跨 Skill 推演。

**上呈复议项 (⛔ 阻塞 C.2 合并, 见 SC-11 —— R4 GOV 抓到「advisory 不阻塞」本身是一种新形态的自行豁免, 不在 `configured-gate-authority.md` 白名单四类内)**: SOT §1「任一 hunk 处方性且在测量范围内 ⇒ **整个变更**照跑」在「一个 Spec 跨多个 Skill」时作用域仍无明文。**本 Spec 的判定不依赖对它的解读**; 但若 owner 认为 §1 应压过 §2 的逐 hunk 表, 则须补跑 phase-d-closer 与 state-scanner 两个套件。**已有一次同形状 shipped 先例**: aria-plugin **v1.69.1** (2026-09-04) 同改 spec-drafter 指令面与 `spec_complete.py` 分类器, CHANGELOG 逐字「路径 + hunk A 两处是处方性运行时指令面 ⇒ **照跑 AB**… **分类器改动为描述性 ⇒ substitute**」, `ab-results/` 实测该批只跑 spec-drafter 一个套件。**但按 memory `exact-exception-condition`「N 次非正式援引 ≠ 成文 lane」, 一次先例不构成 Rule #10 白名单里的 lane** —— 故写进 handoff 请 owner 裁 (a) ratify 成 lane 写进 SOT §5, 或 (b) 另裁。
> ⚠️ 上一版**曾以「两次先例」为由删除本项**, 逐字核 CHANGELOG 后发现 v1.71.1 是「纯代码, 零 SKILL.md / description 变更」= 单 Skill, 不是那个形状。那是基于未核实证据链的自行豁免, 已订正。

> ⚠️ **R2 R1V-6 登记**: SC-7 要求的 AB 在现有 2 个 eval 上**可预测为零区分** —— 本 Spec 的 D1/D2 正说明该套件测不到 Step 3/4/7。这与 SOT §3 警告的「测量剧场」同形。但 `description` 变动使本变更落第二行是 SOT 的**明文映射**, 不是裁量。**处置**: 照跑, 并在 RESULT.md 显式记录「本次 AB 对本改动零区分力, 区分力缺口见 D1」, 不把「跑过了」当成「验过了」。

---

## 验收标准

- **SC-1** (B, **机械判据**): 落地后跑
  `grep -nE 'openspec (archive|validate|CLI)|CLI[^。]{0,12}bug|CLI 完成|安装 openspec|自动修正|修正 CLI|CLI 归档|auto-fix' <四个目标文件>`
  (目标 = `openspec-archive/SKILL.md` + `phase-d-closer/SKILL.md` + `aria/README.md` + `aria/README.zh.md`),
  **落在两个豁免区段之外的命中数 == 0**。
  区段按**标题文本动态定位**, **不硬编码绝对行号** (R3 IMPL-5/RFV-4: Part B 自身会移动行号): (i) `## ⚠️ 已知 Bug` 标题行到其后第一条 `---`; (ii) `## 变更历史` 标题行到 EOF。
  **区段内允许命中集合按内容钉死** (非行号): (a) `## ⚠️ 已知 Bug: OpenSpec CLI 归档位置错误` 标题行; (b) `**问题**: \`openspec archive\` CLI 命令有 bug，输出到错误位置：`; (c) CHANGELOG 表里 `1.0.0 … 初始版本，实现 CLI bug 自动修正` 那行; (d) B13 新插的时限限定行 (若其命中)。**其余一律不允许。**
  **基线实测 (四文件)**: openspec-archive 区段内 4 / 区段外 12; phase-d-closer 区段外 1; `aria/README.md` 区段外 1; `aria/README.zh.md` 区段外 1。**⇒ SC-1 基线区段外合计 = 15**。
- **SC-1b** (语义复核, R3 SCF-2): SC-1 是固定词表 grep, **可被同义换词绕过** (实测 `自动修正→自动纠正` 零命中)。故**另设一条非机械判据**: 复核者对着 §Why 反转 1 逐条重读 B3/B5/B6/B15/B16/B17 的改后原文, 断言它们**不再承诺自动处理 CLI 问题**。此条不可自动化, 须在 tasks.md 里作为独立勾选项。
- **SC-2** (误伤守卫): `grep -c 'Step2' openspec-archive/SKILL.md` == **1** 且唯一命中在 `§Step2 warn_overlay` 交叉引用处。
- **SC-3** (B8/B10 落地形态, **机械判据**, R3 SCF-4 + R4-2/`fixes-contradict` 订正):
  (a) `Step 5 -` 标题行到 `Step 6 -` 标题行之间**非空正文恰 0 行** —— B8 把内容压进标题行本身 (`Step 5 - (已并入 Step 3: git mv 使源目录必然消失)`), 故其下无正文。**上一版写「恰 1 行」与 B8 的字面目标互斥** (R4 抓到)。
  (b) `Step 4 -` 到 `Step 5 -` 之间正文**恰 3 行**, 逐行等于 B8 给出的三条断言字面。
  (c) 示例 1 四行**逐行等于**下列目标文本 (基线位置 `:392` `:393` `:394` `:401`):
  - `  Step 3: ✅ git mv → openspec/archive/2026-02-08-cloudflare-access-auto-handling/`
  - `  Step 4: ✅ 位置校验通过 (目标存在 / 源已消失 / 无 changes/archive/)`
  - `  Step 5: ⏭️ (已并入 Step 3)`
  - `  📦 归档路径: openspec/archive/2026-02-08-cloudflare-access-auto-handling` (替换原 `  🐛 CLI bug 已自动修正`)
- **SC-4** (B9, **机械判据**, R3 SCF-5): `keep_changes_copy` 在 SKILL.md 中的命中**全部落在新增小节 `## 已退役配置项` 内** (与 SC-1 同样按标题文本定位), 区段外命中 == 0。
- **SC-5** (C1 五态): 见 Part C1 表, 五态均留实跑输出; 三个坏实现均被拒。**外加 B2 落地后重跑锚点唯一性** (SKILL.md 侧命中数须仍为 1)。
- **SC-6** (C2 五态): 夹具为冻结快照, 每份注明 `10CG/Aria#<n>` 与抓取时刻; 含合成 `synth-short`。**外加**: `bash aria/skills/run_all_tests.sh` 里 `openspec-archive` 那行的测试数 **非 0**。
- **SC-7** (Rule #6): openspec-archive AB 跑完, 留 `ab-results/2026-09-XX-v1.72.0-archive-skill-drift/RESULT.md`; 两臂 = **v_new vs v_old**; **RESULT.md 须显式记录本次 AB 对本改动的区分力评估** (预期零, 见 R1V-6 登记)。
- **SC-8** (D): D1-D6 开单并回读核验; D7/D8/D9 已开, 号记入 tasks.md。**全部 issue 号带仓限定**, 并跑头部的机械自检 (裸 `#<n>` 命中数 == 0)。D6 须在 handoff 单独点名。
- **SC-9** (E): `aria/.claude-plugin/plugin.json` == `1.72.0`; 23 处版本串全同步; 六个版本类 custom check 全绿; `openspec-archive/CHANGELOG.md` `[Unreleased]` 有条目; **主仓 gitlink 机械断言**: `git ls-tree HEAD aria | awk '{print $3}'` == **`git -C aria rev-parse HEAD`** (子模块实际 checkout 的 commit)。⚠️ **不得比 `origin/master`** —— 上一版那样写在基线上恒绿 (两者天然相等 `301641b`), 与基线表登记的「红」互斥 (R4 抓到)。改后基线实测 `301641b` vs `3a28339` ⇒ **红** ✅; **两仓** (`10CG/Aria` + `10CG/aria-plugin`) 逐 remote `ls-remote` 独立核验 (硬约束 2)。
- **SC-10** (回归): `cd aria/skills/state-scanner/tests && python3 -B run_tests.py` ≥ **1575 / OK** (canonical 口径; pytest 口径为 1603, 两种发现方式收集集不同); 全套件 `bash aria/skills/run_all_tests.sh` ≥ **2122** 且 0 FAIL。
- **SC-11** (Rule #10 闸门, **阻塞 C.2 合并**, R4 GOV 补入): owner 已就「SOT §1『整个变更』在一个 Spec 跨多个 Skill 时的作用域」明确答复:
  (a) ratify v1.69.1 的形状为成文 lane 并写进 SOT §5 ⇒ 本 Spec 只跑 openspec-archive 一个套件即可合并; 或
  (b) 另裁 ⇒ 按其裁定补跑 phase-d-closer / state-scanner 套件后方可合并。
  **在取得答复前不得进入 C.2。** 判据可机械核: handoff 里该问题的 owner 答复段非空, 且若为 (b) 则对应 `ab-results/` 目录存在。
  > ⚠️ 上一版把此项写成「advisory, 不阻塞发版」—— R4 GOV 指出那是**一种新形态的自行豁免**: 它不在 `configured-gate-authority.md` 白名单四类 (config 显式 off / adaptive_rules 映射 / 已成文 lane 降级 / 结构性前提不成立) 内, 也没套用 SOT §2 末行「拿不准 ⇒ 照跑」的默认。已改为阻塞。

### 验收项基线实跑 (memory `spec-acceptance-needs-baseline-run`)

| SC | 基线实测 | 期望 | 红? |
|---|---|---|---|
| SC-1 | 区段外 **15 行** (openspec-archive 12 + phase-d-closer 1 + README ×2 各 1) | 0 | ✅ |
| SC-1b | 六处改后文案尚不存在 | 均不再承诺自动处理 | ✅ |
| SC-2 | `grep -c 'Step2'` = **2** | 1 | ✅ |
| SC-3 | Step 5 是完整段落 (标题 + 2 行正文); Step 4 是 6 行「检测并修正」块; 示例四行均为 CLI 措辞 | Step 5 正文 0 行 / Step 4 正文 3 行 / 示例四行逐行等于目标文本 | ✅ |
| SC-4 | `keep_changes_copy` 2 次 (`:87` `:261`), `## 已退役配置项` 小节不存在 | 全落该小节内 | ✅ |
| SC-5 | 基线 rc 1; **「两侧同改回 Step2」修前 rc 0 (假绿) → 加第三条断言后 rc 1** | rc 0 | ✅ |
| SC-6 | 脚本与 tests 目录均不存在 | 五态可分辨 + 测试数非 0 | ✅ |
| SC-7 | AB 未跑 | RESULT.md 存在且含区分力评估 | ✅ (do-it) |
| SC-8 | `check_bare_issue_refs.py` 在 R3 修订前版 **3** (rc 1) / 本版 **0** (rc 0); D1-D6 未开 | rc 0 / 六条已开 | ✅ (D 部分) |
| SC-9 | plugin.json `1.71.1`; **gitlink 实测 `git ls-tree HEAD aria`=`301641b` vs `git -C aria rev-parse HEAD`=`3a28339` ⇒ 不等** | `1.72.0` / 两者相等 | ✅ |
| SC-10 | state-scanner **1575 OK**; 全套件 **2122**, 10 OK / 0 FAIL | ≥ 同值 | 基准值 |
| SC-11 | owner 未答复 | 已答复 (a) 或 (b) | ✅ |

---

## 非目标

- **不安装 `openspec` CLI** (产品级决定, 上呈 owner)。
- **不改 `spec_complete.py`** —— 包括 `:1251` 的生产文案。本 Spec 对该文件**只读**。
- **不做 Part A** (归档闸门谓词) —— 已拆入 `10CG/aria-plugin#188`, 依据是生产触达实测为 0。
- **不修 D1-D6 / D9 的本体** —— 只开单。
- **不修 `10CG/aria-plugin#187` 的判据本体**; 本 session 已做最小止血 (`phase-d-closer/tests/conftest.py`)。
- **不动 `aria-orchestrator`** (他轨 `feature/m6-cost-model-telemetry`)。
