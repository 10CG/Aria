# aria-plugin v1.77.0 发版准备草案 (TASK-013, 不执行 bump)

> **性质**: 草案 — 本文只定义目标值与执行序列, 不改任何版本文件。
> **Spec**: `openspec/changes/issue-groomer-p1-mvp` (10CG/Aria#238) TASK-013 (parent 3.2)
> **核对基线**: 2026-10-19, aria 分支 `feature/issue-groomer-p1-mvp` (HEAD `63b7772`), aria master = origin/master = `500e6c2` (v1.76.0)
> **⛔ 发版总闸**: Rule #6 SC-6② — **#239 未解冻 ⇒ ship 恒阻塞 (裁定⑥, fail-closed, 无逐案放行)**。Forgejo 实查 2026-10-19: #239 state=open。本文全部内容在解冻前均为「就绪待发」, 不可执行。

---

## 1. 版本号核对

| 项 | 结果 |
|---|---|
| SOT 当前值 (`aria/.claude-plugin/plugin.json` L4) | `"version": "1.76.0"` (已核实) |
| 目标值 | **1.77.0** |
| 档位依据 | 新增 Skill = MINOR+ (CLAUDE.md 版本管理节; `standards/conventions/version-management.md`) |
| tag 占用核对 (2026-10-19) | `git ls-remote --tags` origin 与 github: `v1.77*` **零命中**, 两端最新 tag 均 `v1.76.0` ⇒ 号可用 |
| 并发轨 vNEXT 核对 | `docs/handoff/latest.md` track 表无其他 aria-plugin 发版轨在飞; secret-net 轨 (023236f2) 表面 B.2 active 但其内容 v1.75.0 已于 2026-10-15 ship (CHANGELOG 在案) — 表行陈旧, 无撞号风险 |
| feature 分支 commits | **实测 12 个** (`git log origin/master..feature/issue-groomer-p1-mvp`), 任务描述的 14 与实测不符 (见 §7-4) |

---

## 2. 五文件同步清单 (aria 子模块内)

机械基线 (feature 分支实测, 2026-10-19): `skills/` 44 目录 = **36 user-facing + 7 internal** (SKILL.md 总数 43) + 1 无 SKILL.md 目录 (`issue-triage-workspace`, 非 skill)。master 上为 35+7=42。

### 2.1 `aria/.claude-plugin/plugin.json` (版本 SOT)

| 字段 | 现状值 | 目标值 |
|---|---|---|
| `version` (L4) | `1.76.0` | `1.77.0` |
| `description` (L3) | `…42个 Skills (35 user-facing + 7 internal) + 11个 Agents + Hooks系统…` | `…**43个 Skills (36 user-facing + 7 internal)** + 11个 Agents + Hooks系统…` (计数经机械核对, 其余字节不动) |

### 2.2 `aria/.claude-plugin/marketplace.json` (⚠ 实际路径在 `.claude-plugin/` 下, 非 aria 仓根)

**两处** `version` 字段都要改 (memory: 同文件双缩进 version 陷阱):

| 位置 | 现状值 | 目标值 |
|---|---|---|
| L3 (顶层 `version`) | `1.76.0` | `1.77.0` |
| L16 (plugins 数组条目 `version`) | `1.76.0` | `1.77.0` |

### 2.3 `aria/VERSION`

- L3 `> **版本**: 1.76.0` → `1.77.0`
- L4 新条目 (现 v1.76.0 行整体降级为 `**发布日期(旧)**` 格式, 追加在其下):

```
> **发布日期**: 2026-MM-DD  # minor: v1.77.0 issue-groomer-p1-mvp — 新增 issue-groomer skill: 卫星仓 open issue 组合面批量梳理 (10CG/Aria#238; 五层: forgejo 双端点 fetch (comments 计数对账 fail-closed) / Tier A 机械粗分 / 三面指纹+增量复用 / Tier B 语义评估 SKILL 适配层 / groom.py CLI 11 flag; 产出 groom-report.json schema v1.1 + .aria/groom-assessments.json; issue-groomer 套件 525 测 + 57 subtest 全绿; Skills 42→43 (35→36 user-facing))
```

### 2.4 `aria/CHANGELOG.md` — 新条目 `[1.77.0]` (全文草稿见 §6, 插入位置: 文件头 NOTE 注释块之后、`## [1.76.0]` 之前)

### 2.5 `aria/README.md`

| 位置 | 现状 | 目标 |
|---|---|---|
| L7 tagline | `35 user-facing Skills + 7 internal` | `36 user-facing Skills + 7 internal` |
| L44 名册标题 | `### Skills (35 user-facing + 7 internal = 42 total)` | `### Skills (36 user-facing + 7 internal = 43 total)` |
| L47 internal 注 | 7 个列表 — **不变** (internal 集合无变化) | 不变 |

名册行新增 **3 行** (1 预期 + 2 既有缺漏补齐, 机械核对证据见 §7-1):

```markdown
**Requirements** 节末追加:
- issue-triage — Systematic issue verification (version / code path / in-flight branch / repro) before proposing fixes  ← 既有缺漏补齐
- issue-groomer — Satellite-repo open-issue batch grooming: full-pagination fetch → Tier A mechanical triage → incremental 3-plane fingerprint + diff → Tier B semantic assessment → MD report  ← 本次新增 (v1.77.0)

**Ten-Step Cycle Core** 节 (或 Git Workflow 节后适当分组, 与 i18n 表格行归属对齐) 追加:
- session-closer — Session-level closeout ritual (handoff for unfinished threads; orthogonal to Phase D cycle closure)  ← 既有缺漏补齐 (v1.50.0 引入后从未入册)
```

> 行文措辞以既有名册单行风格 (skill 名 — 一句英文描述) 终稿时对齐; 分组落点由执行席定, 但 3 行必须齐。

---

## 3. 主仓同步面 (gitlink bump PR 内完成)

| # | 文件 | 现状 | 目标 | 备注 |
|---|---|---|---|---|
| 1 | root `README.md` L8 badge | `Plugin-v1.76.0` | `Plugin-v1.77.0` | 机械 check `m6-version-badge-match` 覆盖 |
| 2 | root `README.md` L242 | `Plugin Version:   1.76.0 (aria-plugin, 42 Skills + 11 Agents)` | `1.77.0 (aria-plugin, 43 Skills + 11 Agents)` | |
| 3 | 主仓 `VERSION` 子模块表 | `aria (插件) \| v1.76.0` | `v1.77.0` | 主项目版本 `1.7.5` **不动** (惯例: v1.74.1–v1.76.0 三次 plugin 发版均未 bump 主项目版本) |
| 4 | 主仓 `VERSION` L4 头部 | `最后更新: 2026-08-16` (**陈旧**, git log 实改 2026-10-17 `2436a1b`) | 刷新为实际发版日 | §7-2 不一致的顺带修复 |
| 5 | `docs/architecture/system-architecture.md` §2.8 表 (L189) | `aria-plugin \| v1.76.0` | `v1.77.0` | check `plugin-version-arch-docs-match` 覆盖 |
| 6 | `docs/architecture/system-architecture.md` L206 | `skills/ (42 Skills)` | `skills/ (43 Skills)` | 同文档树状图行, 易漏 |
| 7 | `docs/architecture/version-scheme.md` L23 表 | `aria-plugin … v1.76.0` | `v1.77.0` | L72「v1.28.x 系列」为历史叙述, 不动 |
| 8 | 主仓 `CLAUDE.md` 项目状态段 | `版本: aria-plugin v1.76.0` + `v1.52.0–v1.76.0 已 ship` | 两处 → `v1.77.0` | 预算内覆写, 不追加 |
| 9 | i18n `README.zh.md` / `README.ja.md` / `README.ko.md` | 各 3 处: L3 `translated-from: v1.76.0` / L10 badge / L244 版本行 (42 Skills) | 全部 → `v1.77.0` + 43 Skills | **B 档判定: 重译** — 依据见下 |

**i18n B 档判定**: README.md 正文本次有实质变更 (名册 +3 行、计数 42→43), 非「只版本号」⇒ 按 #140 B 档须重译受影响正文段 (名册/表格行 + 计数行, zh L135/L144/L224 同源对齐), 并同步 3 处版本面 (badge / 版本行 / translated-from marker)。⚠ memory 教训: version checks 只读英文 badge, **i18n 正文 badge 与版本行是静默 drift 面**, 必须人工核对本表第 9 行逐文件落地。

---

## 4. gitlink bump 序列 (多仓 ship checklist — 硬约束两条 + Rule #8)

> 执行前提: §5 状态栏四行全绿或按裁定⑥落恒阻塞记录 (#239 解冻)。

- [ ] **0. 前置核对**: bump 前 `git ls-remote --tags` 双 remote 再核 v1.77.0 未被占 + 读并发轨 handoff `<vNEXT>` (2026-10-19 已核通过, 执行日重跑)
- [ ] **1. aria 五文件 bump** (§2 全部) 在 feature 分支完成并 commit (`chore(release): aria-plugin v1.77.0 …`, Conventional Commits)
- [ ] **2. aria 本地 merge 到 master**: 本地 `git checkout master && git merge feature/issue-groomer-p1-mvp` — **禁止 Forgejo 服务端合并** (约束 1: 子模块合并一律本地做, 服务端 merge commit 产生 orphaned gitlink, 2026-07-14 事故)
- [ ] **3. aria 本地打 tag** `v1.77.0`
- [ ] **4. aria 双推**: `git -C aria push origin master && git -C aria push origin v1.77.0` → github 同套 (双远程逐 remote 分开推)
- [ ] **5. 逐 remote ls-remote 核验** (约束 2: 不信 push 回执): `git ls-remote origin master` / `git ls-remote github master` / 两 remote 的 `v1.77.0` tag SHA 与本地逐一比对, **全部一致才算推成功**; ls-remote 失败重试再下结论
- [ ] **6. 主仓 gitlink bump + 同步面**: `git add aria` (gitlink → merge 后 SHA) + §3 全部 9 项 + `standards` gitlink 若有独立变更一并; commit `chore(release-sync): 主仓发布同步面 → aria-plugin v1.77.0`
- [ ] **7. 主仓 PR** → 可走 Forgejo merge (**主仓例外允许**, 无被 bump gitlink 的下游)
- [ ] **8. Rule #8 pre-merge gate** (phase-c-integrator C.2.4): (a) 本 PR CI passing; (b) main 无 in-flight CI run; 经 CI backend 抽象层, stub 抛 NotImplementedError 时 abort
- [ ] **9. C.2.5 post-push 验证**: 四仓 (Aria / aria / standards / aria-orchestrator) × 双 remote 全部 `ls-remote` SHA 比对全绿
- [ ] **10. Phase D 收尾**: Spec 归档 (openspec-archive 五条落点断言) + #238 关单 (POST comment + 单独 PATCH state) + `docs/handoff/` 周期收尾; #239 恒随解冻状态 (未解冻不关), #240 随 Tier B fixture 完成关

---

## 5. Rule #6 发版前置状态栏 (SC-6 四 facet)

| facet | 状态 | 证据 / 说明 |
|---|---|---|
| **场景 1 AB** (SC-6①) | **pending** | eval 语料已建: `aria/skills/issue-groomer/evals/evals.json` (per ab-suite source 约定); ab-suite 主套件文件 (`ab-suite/issue-groomer.json`) **尚未提取**, 双臂未跑; 结果目录 `ab-results/2026-MM-DD-issue-groomer-rule6/` 不存在 (ab-results 最新仍 2026-10-15) |
| **场景 4b 地板守卫** (SC-6②) | **blocked (owner 门)** | #239 state=**open** (Forgejo 实查 2026-10-19) ⇒ 裁定⑥: 恒阻塞 fail-closed, 无逐案放行; 唯一出路 = #213 owner 审阅解冻。解冻 ⇒ 4b 照跑且 pass; 未解冻 ⇒ TASK-012 落恒阻塞记录, **ship 整体不放行** |
| **substitute 证据** (SC-6④ 第一行成文证据) | **done** | issue-groomer 套件 **525 测 + 57 subtest 全绿** (aria `63b7772`, B.3 对抗 review 处置轮, 净 +66 测); rule6_note 五字段 × 四变更面的成文本身属 TASK-012 → pending |
| **判据表第三行 Tier B fixture** (SC-6③) | **done** | `ab-suite/issue-groomer/tier-b-fixtures/` 7 用例 (3 正 / 3 反 / 1 边界) 三行为 (B1 疑似已修 / B2 优先级 vs 在制轨 / B3 决策面), 已 commit 主仓 `f3555f9` (2026-10-19); ⚠ detailed-tasks.yaml TASK-011 `status: pending` 字段滞后 (§7-5), Phase D 一并刷 |

---

## 6. CHANGELOG `[1.77.0]` 条目全文草稿

> 日期占位 `2026-MM-DD`, ship 日回填。风格对齐 `[1.76.0]` / `[1.75.0]`。

```markdown
## [1.77.0] - 2026-MM-DD — issue-groomer-p1-mvp: 新增 issue-groomer skill (`10CG/Aria#238`; MINOR: 新增 Skill = MINOR+, 版本管理约定)

### Added — 新 user-facing skill `issue-groomer` (卫星仓 open issue 组合面批量梳理; Skills 42 → 43, user-facing 35 → 36)

五层结构 (spec `issue-groomer-p1-mvp`, DEC-20261018-001 裁定-1~13):

- **fetch 层** (`scripts/lib/fetch.py`): Forgejo 双端点 — issue-list 真分页 (空页终止 = 严格更安全, 短页非终态钉死); comments 端点实测忽略 `limit`/`page` 恒全量返回 (三组实验 + 主 loop 独立复验, Runtime Amendment #1 修正 spec §1 分页前提), 改为**计数对账 fail-closed** (声明数 ≠ 返回数即报错); `rc=0` 空 stdout ⇒ FetchError 非空页 (B.3 A-2); 每仓隔离 + 限速; 三态 `[]` / `None` 结构可区分。
- **Tier A 规则引擎** (`scripts/lib/tier_a.py`): title 前缀 / label / staleness / 活跃度机械粗分; 项目级 `.aria/labels.yaml` 存在时默认层**被整体覆盖非合并** (裁定①, fail-closed 不静默回落); 逐信号 confidence 枚举, unknown 不猜, conflict 互斥裁决; 时钟 seam 含左不含右档位; SC-9 七项具名自检; 受限 stdlib yaml parser; `taxonomy_hash` 单点 SOT。
- **groom-report schema v1.1** (`scripts/groom_report.schema.json`, JSON Schema draft 2020-12): 标签契约封闭键集 + 禁 remove + idempotent const (裁定-8); provenance 双层 (harness 顶层 / model_id 在 assessment); additive-only; v1.0 → v1.1 演进只加 `drift_truncated` / `drift_total` 可选字段。
- **增量状态与复用引擎** (`scripts/lib/incremental.py`): 三面指纹 (issue 面: labels 顺序不敏感 / comments 三态 error 面权威 / 显式排除五键封闭; 上下文面: changes 全树内容级 hash + archive 结构性排除 + handoff=latest.md 指针行非 mtime; provenance 拼接串); Tier A 复用门 (issue_key + 判据输入快照); Tier B provenance 门 (`context_key` 四分量 canonical, Amendment #4) + 7+2 封闭枚举 stale reason + orphaned; **结构性保证**: 引擎无 assessment 写面, 重写 state 后 assessments 字节不变为结构不可达而非纪律 (裁定④); 原子写 temp + fsync + rename; assessments 落点 `.aria/groom-assessments.json` (AI 产物非 cache)。
- **diff 段引擎** (`scripts/lib/diff_engine.py`): 键级面 + 富化基元 seam 切分; drift 候选池 = reclassify ∪ new ∪ assessed 点名 (复用非重评不进); `top_n` 字典序截断语义钉死 (0/None/负/bool 拒); baseline 短路 + 参数校验前置。
- **十一态分类矩阵** (`scripts/lib/classify.py`): 22+1 态 (分量级变体 ③×4 / ⑨×2 / ⑩×5; 关闭重开走 new 不复活; 排除字段负向镜像; 并发 LWW + assessments 字节不变); 19/19 mutation 精确命中。
- **CLI `groom.py`** (11 flag, 与 SKILL.md 零漂移机械核验): 编排五层零复刻; repos 回落链 (config 显式 → issue_scan repos 键 → scan_submodules → `.gitmodules` 推导); assessment 白名单投影 (类型不符面省略不造语义); schema 自校验单点 SOT; 退出码 0/1/2。
- **Tier B 语义评估 SKILL 适配层** (`skills/issue-groomer/SKILL.md`): 三类语义判断流程 (疑似已修可关单 / 优先级 vs 在制轨道 / owner 决策面抽取); **拿不准 = null 不猜**; 落盘前必读 `state.last_run.context_key` 置顶警示; 键结构按 `ASSESSMENTS_SCHEMA_DOC` 机读锚点引用勿手抄; MD 渲染四段骨架。

产出: `groom-report.json` (schema v1.1) 与 `.aria/groom-assessments.json`。no-op 实测: duplicate label add 彻底 no-op (连 `updated_at` 不动, fresh add 会 bump ⇒ 差集保留 = 写放大最小化)。

测试: issue-groomer 套件 **525 测 + 57 subtest 全绿** (B.3 对抗 review 处置轮后, 双席 19 条 1C/3H/4M/11L 全落, 净 +66 测; 15/15 + 19/19 + 22+1 mutation 反假绿验证)。B.3 关键处置: 仓 error ⇒ exit 1 不写 state (重跑幂等); `scan_submodules` 三态; `resolve_git_roots` strict (上下文门不再 fail-OPEN); `mini_validate` 迁生产层 `lib/schema_validate.py`。

### Changed

- `plugin.json` description 计数 42 → 43 Skills (35 → 36 user-facing); `marketplace.json` 双 version 字段、`VERSION`、README 名册同步。README 名册顺带补齐两个既有缺行: `issue-triage` 与 `session-closer` (v1.50.0 引入后从未入英文册, 机械核对 36 user vs 名册 33 user 行)。

Rule #6: 新 Skill = 触发面全开。SC-6① 场景 1 AB (evals.json 已建, 结果 `aria-plugin-benchmarks/ab-results/<date>-issue-groomer-rule6/`); SC-6② 场景 4b 地板守卫 **恒阻塞记录** (#239 open, 裁定⑥ fail-closed; 锚 #213 owner 审阅); SC-6④ 第一行 substitute 成文证据 = 本套件 525 结构化测试; 判据表第三行落地 = `aria-plugin-benchmarks/ab-suite/issue-groomer/tier-b-fixtures/` 7 用例定向 fixture (10CG/Aria#240 勘正后范围)。rule6_note 五字段见各任务 `rule6_note` (SOT §4.1)。
```

---

## 7. 核对中发现的版本不一致 (报告项)

1. **aria/README.md 英文名册缺 2 个既有 user skill 行** — `issue-triage` 与 `session-closer`。机械核对 (python 全目录扫描 × README 逐名匹配): feature 分支 36 user skill, 名册仅 33 user 行; zh README 表格行含 issue-triage 而英文无 (中英漂移)。二者均早于本 cycle 引入, 属既有缺漏, 已纳入 §2.5 发版补齐 (3 行 = 1 新增 + 2 补漏)。
2. **主仓 VERSION 头部「最后更新: 2026-08-16」陈旧** — git log 实证该文件 2026-10-17 被 `2436a1b` (v1.76.0 同步) 修改, 头部日期字段未随刷。已在 §3-4 纳入顺带修复。
3. **marketplace.json 实际路径为 `aria/.claude-plugin/marketplace.json`** — 任务描述写 `aria/marketplace.json`, 仓根无此文件; 且含**两处** version 字段 (L3 顶层 + L16 插件条目), 漏改任一即派生文件不一致。
4. **feature 分支 commit 数: 任务描述 14 vs 实测 12** — `git log origin/master..feature/issue-groomer-p1-mvp` = 12 (TASK-001~009/017 + TASK-010 + TASK-007 修正 + B.3)。CHANGELOG 提炼按实测 12 个。
5. **detailed-tasks.yaml TASK-011 `status: pending` 与产物已落盘不符** — tier-b-fixtures 已 commit 主仓 `f3555f9` (2026-10-19)。§5 状态栏按实际产物判 done; yaml 字段滞后留 Phase D 刷 (同型先例: memory `feedback_dec_ship_target_staleness_verify`)。
6. (附注, 超本任务范围) **docs/handoff/latest.md track 表 secret-net 行陈旧** — 表面 B.2 active (10-09), 其交付内容 v1.75.0 已于 2026-10-15 ship (CHANGELOG 在案)。不构成撞号风险, 建议该轨下个 handoff 收敛。
