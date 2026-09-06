# 归档路径两处「分类与现实脱节」收口 — 闸门调用面类级补齐 + openspec-archive 文档/实现对齐

> **Level**: 3 (Full — 跨两个 Skill 的代码 + 指令面变更, 含 Rule #6 AB、机械兜底与发版同步面; 五个 task group)
> **Status**: Draft (Phase A.1; post_spec R1 已跑, 本文为 R1 修订版)
> **Change ID**: `archive-gate-registration-class-and-skill-drift`
> **Linked Issue**: `10CG/aria-plugin#186` — 本 Spec 的立项 issue (类级排查; 兑现母 Spec 交接 §2 H2「承诺开 issue 未开」那条)
>   ⚠️ **跨仓号消歧 (R1 RF-4/AB-7)**: 全文所有 issue 号一律带仓限定。`10CG/aria-plugin#186` 是本 Spec 立项 issue; `10CG/Aria#186` 是另一件事 (`[Archive Tracker] phase-c-integrator-ci-path-coverage`), 两者内容无关。SC-6 夹具用的是 **Aria 仓**的 tracker issue。
> **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2` (Layer L claim 2026-09-06T15:32:43Z, session `s-f260@1532`, push_success=true)
> **Parent US**: 无直接父 US — 方法论工具链维护 (v1.x 轨)
> **前序**: `a1-entry-claim-duplicate-work-guard` (2026-09-06 归档) 的 carry-forward H2 + M2
> **Predecessor 实例修复**: aria-plugin v1.71.1 `301641b` (`_is_aria_check_registry_path` 白名单 — 修的是**实例**)

---

## Why

2026-09-06, D.2 归档闸门拦停了一个本该归档的 cycle: `coordination_probe.py` 由 `.aria/state-checks.yaml` 注册且每次扫描真实执行, 却被 `_classify_file_occurrence()` 归到 `prose` ⇒「有 Python 定义 ∧ 零 alive 引用」⇒ 误判高置信 dead code ⇒ `verdict=block`。

v1.71.1 新增 `_is_aria_check_registry_path()` 修掉了那个实例, **但只修了实例, 没修类** (memory `fix-the-class`)。同批交接把这条记成 H2 并明写「我承诺开 issue 未做」; 同批还记了 `openspec-archive/SKILL.md` 两处漂移 (M2)。

### 为什么合成一份 Spec (R1 AB-1 订正 — 原判据「两侧同改一文件」是假的)

**订正**: 原文写「Part A 与 Part B 共用 `spec_complete.py`」。核实后**不成立** —— Part B 的 B1-B9 全部只改 `openspec-archive/SKILL.md`, 一行都不碰 `spec_complete.py` (§非目标亦明令不许动)。「生产者住在那个文件」≠「本 Spec 会改那个文件」。这句是一条**引用了却没去核**的论据, 恰是本 Spec 在治的病, 已删。

**实际判据 (三条, 逐条可证伪)**:
1. **同一子系统 + 同一触发事件**: 两个缺陷都是 2026-09-06 那次 D.2 归档被 block 时暴露的, 同属十步循环 D.2 归档路径。
2. **Part C1 读 Part A 改的那个文件**: C1 探针的锚点抽的是 `spec_complete.py::_build_d_payload`, 而 Part A 改同一文件的 `_classify_file_occurrence`。分属两份 Spec 时, C1 的锚点会在 A 落地后失配而无人负责。诚实说明强度: A 不改 `_build_d_payload` 本身, 该耦合是「同文件不同函数」级。
3. **同一发版同步面**: Part A/B/C1 全部落在 `aria` 子模块内, 一次发版即可 (见 Part E)。拆两份 = 两轮 post_spec + 两轮 post_planning + 两次 23 处版本点同步。memory `no-ruling-shortens` 实证过「拆 Spec 降复杂度是净负」。

> R1 TL 席指出「合并**制造**了跨 Skill 的 Rule #6 上呈项」。该上呈项已按 R1 MISS-1 删除 (先例已存在, 见 §Rule #6), 故这一反对意见的前提已消失。

### Phase A.1 + R1 取证的四个反转

**反转 1 — 缺口不在「路径」轴, 在「证据」轴。** v1.71.1 修的是路径白名单。真正漏掉的是 `python -m <pkg>.<module>`: `_literal_script_path_match` 只认 `symbol.py` / `symbol.sh` / definition path 整串。**再加多少路径白名单都盖不住它** —— 实测刚被加进白名单的 `.aria/state-checks.yaml`, 遇到 `-m` 形态仍只到 `unclassified`。

**反转 2 — 同一个包里假死与假活并存 (主控实跑复核)。**

| 符号 | 接线 | 当前 `classify_symbol_liveness` |
|---|---|---|
| `tick_runner` | `deploy/aria-layer1-cron.nomad.hcl:50-51` Nomad periodic `python -m aria_layer1.tick_runner` | **dead** (会 block) |
| `comment_poll_runner` | 同构 (`...-comment-poll.nomad.hcl:88`) | **dead** |
| `cost_snapshot_runner` | 同构 (`...-cost-sentinel.nomad.hcl:65`) | **dead** |
| `reconcile_runner` | **完全同构** (`...-reconcile.nomad.hcl:80`) | **alive** |

`reconcile_runner` 的 alive 全部来自 `aria_layer1/schema.sql:248` 与 `migrations/006_schema_v4.2_add_spec_id.sql:17` 两条 **SQL `--` 注释** —— `_strip_comments_and_docstrings` 只剥 `#`。**它是靠一条注释的运气活着的。**

**反转 3 — 交接记的 M2 后果推断被推翻。** 漂移本身成立 (`SKILL.md:317` 写 `Step2`, `spec_complete.py:1251` 写 `Step 7`, 差一字符加一空格, 字节级已核); 但「逐字匹配静默落空 ⇒ SHA 永远填不进去」不成立: 全仓无 `str.replace`, 那是给 AI 的自然语言指令; 6 个 `[Archive Tracker]` issue 全量翻页核过 (`10CG/Aria` 仓, open 2 + closed 4, 无第 3 页), **3/6 含 SHA**。真缺陷是 Step 7 的 SHA 填充**没有代码宿主** —— 6 次执行 4 种形态, `10CG/Aria#185` 被替换成一句完全不含 SHA 的话而无人发现 (memory `no-code-host-no-assertion`)。

**反转 4 (R1 新增, 最重) — 初版 A1 谓词会造出一整类新的假 alive。** R1 BA 席报 Critical, 主控自建 6 夹具复核, **5 个变假 alive**:

| 夹具 | 初版 A1 后 |
|---|---|
| `//` 注释 (HCL/TS) 里的 `-m pkg.sym` | **alive** |
| `--` 注释 (SQL) 里的 | **alive** |
| `<!-- -->` 注释 (HTML) 里的 | **alive** |
| Python 字符串字面量里的 | **alive** |
| JSON 里的散文 (AB eval prompt 就是这形状) | **alive** |
| `#` 注释里的 | prose (唯一被挡住的) |

根因: **真信号住在字符串字面量里** (HCL/JSON 数组的 `"-m", "pkg.mod"`), **噪声也住在那里**; 且 `_strip_comments_and_docstrings` 只剥 `#`。剥字符串会杀掉真信号, 剥注释治不了字符串。**我在自查时写过「注释里的靠 stripped 挡住」—— 那只对 `#` 成立, 我从一种注释风格推广到了全部, 是 `fix-the-class` 复发在自己身上。** 方向是**假 alive** (闸门放行虚假完成声称), 比误拦隐蔽。修法见 A1。

---

## What Changes

### Part A — 归档闸门调用面 (`aria/skills/state-scanner/scripts/lib/spec_complete.py`)

**A1. 新增证据谓词 `_module_path_invocation_match`**

字符级设计 (R1 后定稿, 三处相对初版有变):

- **带点形态** `-m <pkg>(.<pkg>)*.<symbol>` —— **额外要求「紧邻 symbol 的那一段 == symbol 定义文件的父目录名」** (R1 Critical 修复的核心)。散文里随手写的 `pkg.sym` / `foo.sym` 包段不是真包名, 一律不命中。
- **裸形态** `-m <symbol>` —— 仅当 `<symbol>.*` 是本 Spec 声明的 deliverable (`definition_paths` 的 stem)。
- **分隔符字符集 `[\s,\]\['\"-]*`** (`*` 非 `+`) —— 相对初版**新增连字符 `-`**, 为覆盖 YAML bullet 列表 (`- "-m"` 换行 `- "pkg.mod"`), 那是 docker-compose `command:` 段两种常见写法之一, 也正是 A2 白名单的目标文件类型 (R1 PRED-3)。字符集封闭 ⇒ 任何字母 / `;` / `=` 中断匹配, 故 `-m --verbose pkg.sym` 不命中 (已实测)。
- 前置 `(?<![\w-])` 排除 `--m` / `x-m` / `-Xm`; 尾锚 `(?![\w.])` 排除 `pkg.sym_v2`。
- 新类别名 `module_path_call` (英文 canonical)。**三个接入点统一用该类别名**, 不复用 `generic_path_call` —— 可诊断性优先 (R1 未决项已裁)。

**已实测的拒绝能力** (`python3 -B`, 21 用例 0 不符):

| 类 | 用例 | 结果 |
|---|---|---|
| 真信号 | HCL 跨字面量 / shell 单行 / 紧挨 `-mpkg.sym` / 多级包末段真包 / 行首 `-m` / JSON 紧凑数组 / YAML bullet / 大写真包 / 符号含正则元字符 | 全 True |
| 包锚拒绝 | 散文假包名 / 多级包末段非真包 / `git commit -m fix.sym` | 全 False |
| 边界拒绝 | 包段锚定 (取包名) / 尾锚 `_v2` / `--m` / `x-m` / `-Xm` / 数字开头包段 / `=` 分隔符 / 裸 `-m` 未声明 | 全 False |
| 语境拒绝 (R1 新增) | `//` · `--` · `<!-- -->` 三种注释 + Python 字符串字面量 + JSON 散文, 包名为假 | 全 False (初版 5/5 全是 True) |

**残余暴露面 (诚实登记)**: 注释或字符串里写出**真实**模块路径 (`// 曾用 python -m aria_layer1.tick_runner`) 仍会命中。这与 `_literal_script_path_match` 的既有暴露面同级 (非 `#` 注释里写 `tick_runner.py` 今天也命中), **不是新开的类**; 根治属 D6 (注释语法按扩展名分派)。

**接入三处, 全部 OR 追加, 不删既有分支**:

| 位置 | 文本 | 为什么 |
|---|---|---|
| `:947` yaml CI/registry/runtime 支 | **stripped** | — |
| `:969` `.json` 支 | **raw** | 沿用 #192 的「`#` 不是 JSON 注释」结论 |
| `:985-986` 通用支 | **stripped** | 承重: `aria-layer1-cron.nomad.hcl:3` 注释里就写着 `` `python -m aria_layer1.tick_runner` ``; 用 raw 会让「注释里提过」变 alive |

**A2. runtime-yaml 封闭白名单 `_is_runtime_yaml_path`** (本仓 0 实例; 加它是因 aria-plugin 是对外分发件)

basename **精确相等** (不 `.lower()`), 集合封闭优先于优雅。R1 PRED-4 补入同生态遗漏项:

`.pre-commit-config.{yaml,yml}` / `docker-compose.{yaml,yml}` / `docker-compose.override.{yaml,yml}` / `compose.{yaml,yml}` / `.gitlab-ci.{yml,yaml}` / `Taskfile.{yml,yaml}` / `taskfile.{yml,yaml}` / `azure-pipelines.{yml,yaml}` / `.travis.yml` / `buildspec.{yml,yaml}` / `cloudbuild.{yaml,yml}` / `.drone.yml`; 另加 `endswith("/.circleci/config.{yml,yaml}")`。

命中后走**与 CI 支同一套证据** (`_literal_script_path_match or _module_path_invocation_match`), **不用** `_config_has_registration` (它接受裸 `symbol in text`)。

**A3. 极性钉子测试**: A2 落地后, 白名单内文件在**不匹配**证据时由 `prose` (`:952`) 变 `unclassified` (`:949`) —— 方向 dead→warn, 与 CI 支一致, 但是真语义变更, 须立钉子测试。**R1 PRED-5 补充**: 白名单分支的 fallback 缺通用分支那一步「剥完注释后是否仍出现」的判断, 故纯注释提及会记成 unclassified 而非 prose; 方向仍安全, 须在钉子测试里一并固定。

**A4. 明确不动的两处 (刻意从严, 非缺口)**: `.md` 通用支 (`:929`) / `_is_test_path` (`:747`)。

### Part B — `openspec-archive/SKILL.md` 与实现对齐

> **R1 RF-1 / BA-refuter 订正: 位置从 5 处扩到 11 处。** 原枚举漏了同类 6 行, 其中 `:41` 是已枚举的 `:40` 的**同表相邻行** —— 改 `:40` 不改 `:41` 会让同一张表自相矛盾。这正是 `fix-the-class` 复发在本 Spec 自己身上。

| # | 位置 | 改动 |
|---|---|---|
| B1 | `:317` | `Step2` → `Step 7` (对齐 `spec_complete.py:1251`) |
| B2 | `:318` | 替换文案改为**可验证约束**: 该行必须含 7-40 位十六进制 SHA; 并在 Step 7 段落写明强制调用 C2 校验脚本 |
| B3 | **`:4`** | **frontmatter `description`** —— 「自动修正 CLI bug」删除/改述。⚠️ **这条决定了整个变更的 Rule #6 档位**, 见下 |
| B4 | `:40` + **`:41`** | 核心功能表两行: 「调用 CLI」→ `git mv`; 「自动修正」→「位置校验」 |
| B5 | `:248` + **`:249`** | Step 3 → `git mv openspec/changes/{id} openspec/archive/{YYYY-MM-DD}-{id}` (命名 SOT `standards/openspec/project.md:24`); 删「等待: CLI 完成」 |
| B6 | `:251-257` + `:259-261` | Step 4 降级为归档后位置校验三断言; Step 5 标「已并入 Step 3」。**Step 编号一律不重编** —— Step 7 的编号被 `spec_complete.py:1251` 的 d_payload 文案引用 |
| B7 | `:87` | 退役 `keep_changes_copy` (证据见下) |
| B8 | `:392` + **`:393`** + **`:401`** | 示例 1 三行同步 |
| B9 | `:588` | 错误表 CLI 行 → `git mv` 失败三分支 |
| B10 | **`:607`** | 流程图「Step 3-6 执行归档 / 修正 CLI bug / 验证结果」同步 |
| B11 | `:47-56` | 已知 Bug 节**保留** + 时限限定 + 「本 Skill 会自动修正」改为对采用者的条件表述 |
| B12 | `:622` | 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` |

**⚠️ 误伤守卫**: `Step2` 全文出现**恰好两次**, `:275` 的 `§Step2 warn_overlay` 是语义正确的交叉引用。**禁全局 `sed`**, 只改 `:317`。

**改哪边的判据**: (1) 代码是 `d_payload.body` 唯一运行时生产者; (2) 改名有**成文裁定** —— `openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/proposal.md:174` 逐字写「**裁定: 保留改名, 收窄声称。**」并论证 `Step2` 对该动作是**事实错误**的引用 (已逐字核, `:172` 是论证段, `:174` 是裁定句); (3) 反向改代码会退回错误语义。

**B7 退役 `keep_changes_copy` 的三条实证**: 全仓只出现 2 次 (均在 SKILL.md `:87` `:261`), 零代码消费方 / 零测试 / 零 eval; `changes/` 与 `archive/` 的 slug **零重叠** ⇒ 历史从未行使; 若行使, 同一 spec 会同时在两处 ⇒ `collectors/openspec.py:208` 无条件枚举 `changes/` 计成**幽灵活跃变更**, 且 `:241` 会让它永挂 `pending_archive`。
⚠️ 这是**声明接口的移除**, 须在 handoff 点名请 owner 复议 (memory `narrow-owner-options`)。

### Part C — 机械兜底

**C1. `skill_md_literal_sync_probe.py`** → 落点 `aria/skills/state-scanner/scripts/` (随插件分发 —— 它守的是插件内部不变量, 每个采用方都继承该风险), 注册进本仓 `.aria/state-checks.yaml` 作 dogfood。

**抽取锚点成文** (R1 AB-5/RF-2/RF-6 —— 原版锚点欠定到会改变基线 rc):
- SKILL.md 侧: `"(> 归档 SHA 回链:[^"]*填入)"` —— **以「填入」结尾**是承重的, 它把 `:317` 的匹配串与 `:318` 的替换串 (以 `HEAD)` 结尾) 区分开, 故基线命中数 = 1 而非 2。
- 生产者侧: `lines\.append\(\s*"(> 归档 SHA 回链:[^"]*)"\s*\)`。
- **两个文件路径钉死**, 经 `CLAUDE_PLUGIN_ROOT` 优先、回落 `<repo>/aria` 解析 —— **禁用 glob** (仓内有 AB skill-snapshot 冻结副本, glob 式实现会恒红, R1 RF-6)。

**第三条断言 (R1 AC-1)**: 纯双边相等挡不住「两侧同步改回 `Step2`」这第三种坏实现 (实测 rc=0 GREEN)。故追加: 命中串**必须含 `Step 7`** —— 该值有 2026-07-22 成文裁定背书, 不是任选常量。

**五态实测** (production 版, 对齐 `collectors/custom_checks.py` 三态契约):

| 态 | 结果 |
|---|---|
| 基线 (本仓) | **FAIL** rc 1, 打印两侧原文 |
| 目标 (B1 落地后) | **PASS** rc 0 |
| 插件源码不可见 (采用方场景) | **SKIP** rc 0 + `##SKIP##` 哨兵 |
| 文件在但锚点提取数 ≠ 1 | **FAIL** rc 1 (fail-CLOSED, 不降级 SKIP) |
| 坏实现: 只比前缀 / 只比到步骤名前 / **两侧同改回 `Step2`** | 基线均 GREEN ⇒ 前两个已判无效; **第三个由新增的 `Step 7` 断言拒掉** |

**C2. `archive_tracker_verify.py`** → 落点 `aria/skills/openspec-archive/scripts/` (**新建该目录**; 语义正确 —— 它是 openspec-archive Step 7 的宿主, 且随插件分发)。输入 `--repo <org>/<repo> --issue <n>` 或 `--body-file <夹具>`。

**夹具契约 (R1 AC-3)**: 单测用**冻结快照**, 不实时抓 API —— issue body 可被编辑, 钉活体会让测试随时被悄悄破坏。快照落 `aria/skills/openspec-archive/tests/fixtures/`, 每份注明来源 `10CG/Aria#<n>` 与抓取时刻。

**五态实测**:

| 夹具 | 结果 |
|---|---|
| `10CG/Aria#201` (真, 含 `4c3c826`) | rc 0 OK |
| `10CG/Aria#185` (真, 行在无 SHA) | rc 1 NO_SHA |
| `10CG/Aria#186` (真, 无回链行) | rc 1 MISSING |
| 合成 `synth-short` (尾部含短十六进制 `abc`) | rc 1 NO_SHA |
| body 取不到 | rc 2 **fail-CLOSED** |

坏实现拒绝: 「只查行存在」在 #185 上 GREEN ⇒ 无效; 「`[0-9a-f]+` 无长度下限」在 **#185 上也是红的** (该真语料尾部是纯中文, 零 ASCII 十六进制字符) ⇒ **真语料夹具证不了长度下限**, 必须靠合成夹具 `synth-short` 才能拒掉它。

**自反性**: C1 注册进 `.aria/state-checks.yaml` 后, Part A 的分类器会因 `_is_aria_check_registry_path` 判它 alive —— A 与 C 互为活体验证。

### Part D — 开单 (八条; 全部带仓限定 + 回读核验)

| # | 内容 | 仓 |
|---|---|---|
| D1 | AB 固定套件缺 Step 7 / D auto-issue 维度 (`ab-suite/openspec-archive.json` 只选 2/4 eval) — Rule #6 SOT §3 第 3 条强制 | `10CG/aria-plugin` |
| D2 | openspec-archive evals **三个**涉及「正确归档路径」的 eval 全部缺强制 `YYYY-MM-DD-` 前缀 (含**已被选进套件**的 eval 1 `correct-archive-path`, R1 AB-4/RF-11); `cli-bug-fix` 的 `cli_wrong_path` 与 SOT 矛盾; 断言首句 `openspec/archive` 是次句 `standards/openspec/archive` 的**真子串** ⇒ 首句零判别力 | `10CG/aria-plugin` |
| D3 | `unverified_claims` / `unverified_ack` frontmatter 只写不读 (`spec_complete.py:103` 自承) | `10CG/aria-plugin` |
| D4 | `standards/openspec/AGENTS.md:57` 悬空脚本 `verify-openspec-archive.sh` | `10CG/aria-standards` |
| D5 | GAP-3 `pyproject.toml` entry_points 不被识别 (1 真实例 `aria_layer1:register`; 该文件单独判 prose 已实测) | `10CG/aria-plugin` |
| D6 | 注释语法只剥 `#` ⇒ `--` / `//` / `<!-- -->` 里的提及被当代码体 (实例 `reconcile_runner`) | `10CG/aria-plugin` |
| D7 | ⏰ **有日期**: `check-m6-e2e-acceptance` 判 dead。**引信行是 `aria-2.0-m6-e2e-resilience/tasks.md:353`** (行内写全仓相对路径 ⇒ dead ⇒ **block**), **不是 `:380`** (行内只有裸文件名 ⇒ ambiguous ⇒ 仅 warn) —— R1 CR-refuter 抓到本 Spec 引错行, 两行分类已主控实跑复核。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免 | `10CG/Aria` |
| D8 | **(R1 后新增, Part B 的类级兄弟位置)** `spec-drafter/SKILL.md:192 :507 :510` 三处同样指示运行未安装的 `openspec validate --strict`。**不纳入本 Spec**: 判据与 GAP-3 一致 (「删掉之后用什么替代校验」是未解设计题); 且它会触发**第三个** AB 套件 | `10CG/aria-plugin` |

> **本 Spec 只修了这个类的一半**, 明写在此以免它在 Spec 面上不可见 (memory `fix-the-class`)。

### Part E — 发版同步面 (R1 M-1 补入; 原版整份 Spec 零提及)

Part A/B/C1/C2 全部落在 `aria` 子模块 ⇒ **必须发版**。SC-7 要求的 `ab-results/<date>-<version>-<slug>/` 也预设了一个原本从未规划的版本号。

- **版本级别**: **MINOR** (Part A 新增证据类别 `module_path_call` + 新谓词, 属 CLAUDE.md「新增 Skill / Skill 架构重构 = MINOR+」的后半; B3 改 `description`)。v1.71.1 → **v1.72.0**。
- **同步面实测枚举**: `1.71.1` 共 **23 处出现 / 13 文件** —— aria 子模块 7 处 (plugin.json 1 / marketplace.json 2 / VERSION 2 / CHANGELOG 1 / README 1) + 主仓 **16 处** (VERSION 1 / CLAUDE.md 2 / README.md 2 / zh 3 / ja 3 / ko 3 / system-architecture 1 / version-scheme 1)。主仓 16 与前一 cycle commit `4c3c826` 记的「16 处版本点」精确对账。
- **不改**: `.aria/triage-*` / `docs/handoff/*` / 本 proposal 引前序版本处 —— 历史记录, 改了反而失真。
- **机械兜底须全绿**: `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency` / `m6-claude-md-version` / `plugin-cache-currency`。i18n README **仅正文实质变更才重译** (#140 B 档), 只改版本号不算。

---

## Rule #6 判定 (逐 hunk, `rule6_note`)

SOT: `standards/conventions/skill-benchmark-exemption.md` v1.0.0 (逐字读过)。

**判定的决定性事实 (R1 后)**: **B3 改的 `:4` 就是 frontmatter `description` 字段** (原文含「自动修正 CLI bug」)。SOT §2 附加约束逐字写: 「仅当变动是事实性同步 … 且 frontmatter `description` **零变动**, 才可能落进第一行; **`description` 或指令流程变动 ⇒ 一律第二行**」。

⇒ **openspec-archive 侧整体落第二行, 照跑 AB, 零裁量。** 原版对 B1/B4/B5 的「第一行 substitute」与对 B2 的「第三行」两个判定**全部作废**:
- B2 的第三行本来也不成立 (R1 RB-1): SOT §3 条件 2 要求「回退改动, 该 fixture 必须转红」, 而 C2 单测的输入是 issue body 夹具, 回退 `SKILL.md:318` 不改脚本不改夹具 ⇒ 三条夹具 rc 恒等, **「回退须转红」结构上无法演示** ⇒ 按 SOT §3「缺一即回落到照跑」。这是 memory `no-code-host-no-assertion` 复发在我自己新写的兜底路径上 (memory `fix-recurs-in-fallback`)。
- 成本≈0: B3 本来就要跑同一个套件。

**state-scanner 侧 (Part A) 走 substitute** —— 依据是**四条先例**, 不是类推:

| 先例 | 内容 | 处置 |
|---|---|---|
| `state-scanner-stale-refs-false-parity` v1.59.0 | 纯函数 (INERT 零调用点) | substitute (SOT §5) |
| 同 spec v1.60.0 | **F1′-F10″ collector 代码层** | substitute (SOT §5) |
| **aria-plugin v1.69.1** (2026-09-04) | 同一文件同一函数 `_classify_file_occurrence` 补 `.json` 分支; **同批另有 spec-drafter 指令面变更照跑了 spec-drafter 套件, state-scanner 套件未跑** | substitute (CHANGELOG `:110-112`) |
| **aria-plugin v1.71.1** (2026-09-06, 本 Spec 前序) | `_is_aria_check_registry_path`, 纯代码零 description 变更 | substitute (CHANGELOG `:39` `:45-46`, 并自己点名 v1.69.1 先例链) |

> **R1 MISS-1 订正**: 原版把「一个 Spec 跨两个 Skill 时作用域是否及于另一个 Skill 的套件」当作「SOT 未覆盖」上呈 owner 复议。**该问题已有两次 shipped 答案** (v1.69.1 / v1.71.1 都是这个形状), 上呈项**已删** —— 拿一个已答过两次的问题去问 owner, 是 memory `narrow-owner-options` 的反面浪费。

**结论**: **openspec-archive 套件照跑 AB** (`/skill-creator`); **state-scanner 走 substitute** (= SC-1/SC-2/SC-3 的 baseline-failing 测试)。

---

## 验收标准

- **SC-1** (A1 正例): `tick_runner` / `comment_poll_runner` / `cost_snapshot_runner` 的 `classify_symbol_liveness().status` 由 `dead` 变 `alive` 且 `alive_categories` 含 `module_path_call`; **外加** `reconcile_runner` 的 `alive_categories` 新增 `module_path_call` (它 status 不变, 只查 status 会让「假活变真活」这条真实改善不可观测 —— memory `invariant-dimension`)。
- **SC-2** (A1 负控, 六类, 缺一不可):
  (a) `detailed-tasks.yaml` 含字面路径 → 仍非 alive;
  (b) 裸 `-m symbol` 且 symbol 非声明 deliverable → 仍非 alive;
  (c) 散文 `-m flag; see pkg.symbol` → 仍非 alive;
  (d) **五种语境**里的假包名 `-m pkg.symbol` 全部非 alive: `//` 注释 / `--` 注释 / `<!-- -->` 注释 / Python 字符串字面量 / JSON 散文 (初版这五个**全是** alive);
  (e) **正则锚点各自的负控** (R1 AC-2): 前置 `--m` `x-m` `-Xm` / 尾锚 `pkg.sym_v2` / `=` 分隔符 / 数字开头包段 —— 每条一个夹具, **在谓词层测**;
  (f) **`replay_cli`** (真语料负控): 有 `-m` 形态但只在自己定义文件里 → 修复前后均 `dead`。
  「包段锚定」须在**谓词层**测: 分类器层零复现力 (`_code_reference_match` 的 `\bsym\.` `:645` 会先命中) —— **该结论只对通用支成立, CI-yaml 支有区分力** (R1 RF-7 订正)。
- **SC-3** (A2 + A3 极性钉子): `docker-compose.yml` 只提裸名时由 `prose` 变 `unclassified` (两值都写进断言); 且白名单内文件「仅注释提及」时的归宿一并固定 (R1 PRED-5)。
- **SC-4** (B, **机械判据**, R1 AC-4/RF-1): 落地后跑
  `grep -nE 'openspec archive|openspec CLI|CLI bug|CLI 完成|安装 openspec|自动修正' SKILL.md`,
  **落在两个豁免区段之外的命中数 == 0**。豁免区段按**位置**定义 (不按措辞, 否则改几个反引号就能骗过检查 — memory `author-to-match-checker`):
  (i) `## ⚠️ 已知 Bug` 标题行到其后第一条 `---` 之间 (B11 保留的历史说明节);
  (ii) 文末 CHANGELOG 表格区。
  **基线实测 13 行命中**: `:4 :40 :41 :49 :56 :248 :249 :392 :393 :401 :588 :607 :632`; 其中区段内 3 行 (`:49` `:56` 在 (i), `:632` 在 (ii)), **区段外 10 行** (`:4 :40 :41 :248 :249 :392 :393 :401 :588 :607`) —— 这 10 行恰是 B3-B10 的编辑对象, 一一对应。
  另: `grep -c 'Step2'` == **1** 且唯一命中在 `:275`。
- **SC-5** (C1 五态): 见 Part C1 表, 五态均留实跑输出; 三个坏实现 (只比前缀 / 只比到步骤名前 / **两侧同改回 `Step2`**) 均被拒。
- **SC-6** (C2 五态): 夹具为**冻结快照**, 每份注明 `10CG/Aria#<n>` 与抓取时刻; 含合成 `synth-short` (否则长度下限的必要性证不了)。
- **SC-7** (Rule #6): openspec-archive AB 跑完, 留 `ab-results/2026-09-XX-v1.72.0-archive-gate-class/RESULT.md`; `WITHOUT_BETTER` 逐条解释或回退。两臂 = **v_new vs v_old** (SOT §6: with/without 那列因 CLAUDE.md 污染不可用)。
- **SC-8** (D): D1-D8 八条全部开单并回读核验, issue 号**带仓限定**记入 tasks.md。D7 须在 handoff 单独点名。
- **SC-9** (E 发版): `aria/.claude-plugin/plugin.json` = `1.72.0`; 23 处版本点全部同步; 六个版本类 custom check 全绿; 三仓逐 remote `ls-remote` 核验。
- **SC-10** (回归): `cd aria/skills/state-scanner/tests && python3 -B -m pytest -q` ≥ **1603 passed** 且 0 fail (基线实测 1603/0)。⚠️ 必须从 `tests/` 目录内跑 —— 在 skill 根跑会因两个同名 `lib` 包产生 12 个 collection error (memory `ss-two-lib-pkgs`)。

### 验收项基线实跑 (memory `spec-acceptance-needs-baseline-run`)

| SC | 基线实测 | 期望 | 红? |
|---|---|---|---|
| SC-1 | 三符号 `dead`; `reconcile_runner` alive 但来源是两条 SQL 注释 | 三个 alive + 第四个来源新增 | ✅ |
| SC-2(d) | 五种语境**初版全部 alive** (V1 实测 5/5 假 alive) | 全部非 alive (定稿 V3 实测 0/5) | ✅ |
| SC-3 | `docker-compose.yml` 裸名 → `prose` | `unclassified` | ✅ |
| SC-4 | `grep -c 'Step2'` = **2**; CLI 类命中 **13 行**, 区段外 **10 行** (`:4 :40 :41 :248 :249 :392 :393 :401 :588 :607`) | 1 / 区段外 0 | ✅ |
| SC-5 | rc 1 + 三坏实现基线 GREEN + 提取失败 rc 1 | rc 0 | ✅ |
| SC-6 | 脚本尚不存在; #201 有 SHA / #185 有行无 SHA / #186 无行 | 三态可分辨 | ✅ |
| SC-7 | AB 未跑 | RESULT.md 存在 | ✅ (do-it) |
| SC-8 | `10CG/aria-plugin` 仓标题含 `Step 7` / `cli-bug-fix` / `unverified_claims` / `openspec validate` 的 issue 各 **0** 条 | 8 条 | ✅ |
| SC-9 | plugin.json = `1.71.1` | `1.72.0` | ✅ |
| SC-10 | **1603 passed / 0 fail** | ≥1603 / 0 | 基准值 |

---

## 非目标

- **不安装 `openspec` CLI** (引入外部依赖属产品级决定, 上呈 owner 而非 AI 自裁)。
- **不改 `spec_complete.py:1251` 的生产文案** (改名有成文裁定, 反向改退回错误语义)。
- **不修 D5 / D6 / D8** —— 判据统一: 设计到字符级的纳入 (A2), 未到的开单。D5 的 TOML section 追踪欠定; D6 是「按扩展名分派注释语法」的独立设计题; D8 的「用什么替代 `openspec validate`」未解且会触发第三个 AB 套件。
- **不修 D7** (属 M6 轨, owner/基建门), 只点名 + 开单。
- **不改 `.md` 通用支与 `_is_test_path`** (Part A4)。
- **不动 `aria-orchestrator` 指针** (他轨 `feature/m6-cost-model-telemetry`)。
