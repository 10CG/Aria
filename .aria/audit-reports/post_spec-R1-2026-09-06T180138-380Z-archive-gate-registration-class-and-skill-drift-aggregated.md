---
checkpoint: post_spec
round: 1
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 1C/8M/16m (五席原始合计 30 条; 反驳席推翻 6 条, 存活 24 条 + 反驳席另报约 15 条)
clusters: 1C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-06T18:01:38.381Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 1
---

# post_spec R1 — archive-gate-registration-class-and-skill-drift (aggregated)

## drift_metrics (anchor 快照, Step 0 固化)

- **checkpoint**: post_spec
- **primary_goal**: 把 D.2 归档闸门的调用面缺口从「修实例」推到「修类」, 并把 openspec-archive SKILL.md 与实现的漂移收口
- **in_scope**: Part A (spec_complete.py 分类器) / Part B (openspec-archive SKILL.md) / Part C (机械兜底) / Part D (开单)
- **out_of_scope_hints**: 安装 openspec CLI / 改 spec_complete.py:1251 生产文案 / GAP-3 pyproject / 注释语法分派 / D7 的 M6 轨修复 / aria-orchestrator 指针
- **source_sha**: 07bf4c1
- **anchor_source**: proposal.md §Why (fallback 链第 1 档)

## Round 1

- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品 (`verdict=no_sibling_found`, own_key = `aria-plugin#186` canonical; github 152 / origin 156 份 spec, hits=[])
- **编排**: 动态工作流 10 agent —— 5 席镜头并行 + 每席一个独立反驳席 (pipeline, 无 barrier)
- **原始合计**: 30 条 (TL 8 / BA 5 / QA 4 / CR 11 / KM 2); 反驳席推翻 **6** 条, 存活 **24** 条 (8 Major + 16 Minor); 反驳席在 `missed` 字段另报约 **15** 条 (其中 5 条 Major)

### 逐席 verdict

| 席 | verdict | 原始条数 |
|---|---|---|
| aria:tech-lead (架构与边界) | PASS_WITH_WARNINGS | 8 |
| aria:backend-architect (谓词设计正确性) | **FAIL** | 5 |
| aria:qa-engineer (验收可证伪性) | PASS_WITH_WARNINGS | 4 |
| aria:code-reviewer (引用与事实核验) | PASS_WITH_WARNINGS | 11 |
| aria:knowledge-manager (规范一致性与 Rule #6) | PASS_WITH_WARNINGS | 2 |

### ⚠️ 反驳机制本轮出过一次假推翻 (记录在案)

BA 席报的 **Critical (PRED-1)** —— 「带点形态无代码语境锚定 ⇒ 散文里的 `-m pkg.symbol` 变 alive」——
**被其反驳席推翻** (理由: 落在 fail-toward-warn 安全方向、零真实语料)。

**主控独立复核后判定该推翻是错的**: 自建 6 夹具实跑, **5 个变假 alive** (`//` / `--` / `<!-- -->`
三种注释 + Python 字符串字面量 + JSON 散文), 只有 `#` 注释被挡住。方向是**假 alive** (闸门放行虚假
完成声称), 不是安全方向。TL 席的 AB-2 (存活 Major) 独立报了同一根因。

⇒ 本报告 verdict 取 **FAIL** (1 Critical, 主控实测确认), 不取「推翻后 0C/8M ⇒ PASS_WITH_WARNINGS」。
⇒ 方法论教训: 反驳席的「refuted=true」不是终局, 主控须对**被推翻的最高档 finding** 独立复验
(同 memory `feedback_cross_agent_verdict_independent_verify` 形状)。

## 存活 finding (24 条)

### Major (8)

| id | 席 | 标题 |
|---|---|---|
| AB-2 | TL | A1 安全网只防 `#` 注释 —— `//` 与 `--` 注释里的 `-m pkg.sym` 由 unclassified 翻成 alive |
| AB-3 | TL | C2 只是断言函数的宿主, 不是机制的宿主; B2 的「强制调用」落在 6/6 已证失效的 AI 自然语言通道 |
| AB-6 | TL | B3 编辑集漏 frontmatter `description` (:4) 与同表相邻行 :41 等 ≥7 行, SC-4 因此无法裁决 |
| AC-1 | QA | C1 是纯双边相等断言, 挡不住「两侧同步改回错误值」这第三种坏实现 |
| AC-2 | QA | SC-2 四条负控未覆盖 A1 自己列出的两个正则锚点保证 |
| AC-3 | QA | SC-6/C2 夹具钉在活体 Forgejo issue 上, 未声明快照 vs 实时, 未消歧仓库 |
| RF-1 | CR | B3 的 CLI 位置枚举漏至少 9 行; SC-4 基线「4 行」低估 |
| RF-4 | CR | 跨仓 issue 号未限定仓名; `aria-plugin#192` 实测 404; `#186` 在同一文档里有两义 |

### Minor (16)

AB-1 (合并判据「同改一文件」不成立) / AB-4 (D2 缺陷同样存在于**被选中**的 eval) / AB-5 (C1 抽取锚欠定到会改变基线 rc) /
AB-7 (跨仓 `#186` 撞号) / AB-8 (Part C 两制品落点未声明) / PRED-5 (A3 极性变更后两分支对「仅剩注释提及」处理不对称) /
AC-4 (SC-4 第二分句无机械判据, 代理检查会因 B4 保留段假红) / RF-2 (C1「基线 rc=1」与自身 fail-closed 规则互斥) /
RF-3 (Rule #6 B3 档位承重引用指向非套件源集) / RF-5 (行号簇轻微漂移;「4 个调用点」实测为 5) /
RF-6 (C1 未钉死两个文件路径, glob 式实现会恒红) / RF-7 (SC-2「包段锚定零复现力」过度一般化) /
RF-8 (A1 分隔符描述自相矛盾; `-Xm` 排除例是空谈) / RF-9 (SC-8 基线行把 D4 归错仓, 四关键词只覆盖 7 条中的 4 条) /
RF-10 (Rule #6 上呈项未挂钩已在案的 aria-standards#17) / RF-11 (D2 只点名 cli-bug-fix, 同一失真在已选进套件的 eval 1 上也成立)

## 反驳席另报 (missed, 约 15 条; 其中 5 条 Major —— 本轮反驳席产出重于找茬席)

| 来源 | 严重度 | 内容 |
|---|---|---|
| TL-refuter M-1 | **Major** | **全 Spec 零版本 bump / 零发布同步面** —— Part A/B/C1 全在 aria 子模块, 196 行 proposal 一字未提; 而 SC-7 要求的 `ab-results/<date>-<version>-<slug>/` 预设了一个从未规划的版本号 |
| BA-refuter 【1】 | **Major** | B3 漏同类 6 处 (`:4` `:41` `:249` `:393` `:401` `:607`), 其中 `:41` 是已枚举 `:40` 的**同表相邻行**; 类规模至少 10 行而非 4 行 —— `fix-the-class` 复发在本 Spec 自己身上 |
| QA-refuter RB-1 | **Major** | B2 的「可证伪定向 fixture」**结构上不可能满足** —— C2 单测输入是 issue body 夹具, 回退 SKILL.md:318 不改脚本不改夹具 ⇒ 三条夹具 rc 恒等, SOT §3 条件 2「回退须转红」无法演示 ⇒ 应回落第二行 |
| QA-refuter RB-2 | **Major** | §156 自认 SOT 未覆盖, 却把「豁免」当待复议期间的默认, 与 SOT fail-closed 方向相反 |
| CR-refuter M-1 | **Major** | **D7 点错行** —— `tasks.md:380` 实测 `ambiguous`(warn); 真引信是 `:353` (行内写全仓相对路径 ⇒ `dead` ⇒ block)。主控已实跑复核确认 |
| KM-refuter MISS-1 | **Major** | Rule #6 跨 Skill 作用域**已有两次 shipped 先例** (v1.69.1 `CHANGELOG:110-112` / v1.71.1 `:39,:45-46`), 上呈 owner 属重复提问 |

## 处置 (主控 R1 修订, 已落 `07bf4c1`)

proposal 194 → 275 行。逐条对应见 commit message。关键三项:
1. **Critical 修复**: A1 谓词加「包段 == 符号定义文件父目录名」结构锚。实测 5 类假 alive 全拒、真信号 3/3 全留, 且原记录在案的残余向量 `git commit -m fix.sym` 一并拒掉; 21 用例 0 不符。
2. **Rule #6 整体重判**: B3 改的 `:4` 就是 frontmatter `description` ⇒ SOT §2 附加约束「description 变动 ⇒ 一律第二行」⇒ openspec-archive 侧照跑 AB, 原「B1/B4/B5 第一行 + B2 第三行」两判定作废; 跨 Skill 上呈项按先例删除。
3. **新增 Part E 发版同步面** (23 处 / 13 文件, 主仓 16 处与前 cycle commit `4c3c826` 精确对账)。

**下一轮 (R2)**: 按 memory `rewrite≠cleanup` (结构重写后 86% finding 落在当轮新文本), 镜头改为
实现者试派生 / R1 修复验证 / 定稿谓词拒绝能力 / 新文本引用核验 / 治理面 + Part E 规范核对。
