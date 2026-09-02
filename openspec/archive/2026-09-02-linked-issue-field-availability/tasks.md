# Tasks — `linked-issue-field-availability`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/linked-issue-field-availability-audit-trail.md) (append-only, 不维护与 Spec 一致性)
> **Level**: proposal 自陈 **2**; 本文件按 Level 3 双层体例出 `tasks.md` + `detailed-tasks.yaml` (理由见下「为什么出 tasks.md」)
> **Status**: ✅ **Shipped 2026-09-02** — 25/25 done; PR #190 merged `888b893`; aria v1.68.1 `d1caa66` (+v1.68.0 `fe32441`) / standards `ffed204`; pre_merge 收敛审计 R1–R5 四票 PASS 0C/0M (converged=false, owner 选 [1] override); 历史: ✅ **B.2 实施完成 2026-09-02** (24/25 勾选; 5.3 / 5.4 双推已核验 2026-09-02 owner 授权; 5.6 主仓 PR #190 pre_merge 收敛审计中) — aria **v1.68.1 `d1caa66`** (R1 清账 PATCH; v1.68.0 `fe32441` 亦在两端, 两 tag) / standards **`ffed204`** (Usage Note 英文化; 前一 `fad8b4b`) / 主仓 feature/linked-issue-field-availability; 测试 **53/53** + state-scanner **1462** + run_all_tests **1894** (v1.68.1 后重跑) 全绿; Rule #6 AB 见 `aria-plugin-benchmarks/ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/RESULT.md` (无 WITHOUT_BETTER); B 期技术裁定 B1–B7 见决策单 2026-09-01 追记。历史: ✅ **A.2 + A.3 complete** (2026-08-30 owner 批准进 A.2; post_planning R1 FAIL → R2 PwW → R3 PwW → **R4 CONVERGED 2026-08-31 (五席 5/5 PASS, 0C 0M)**; 收敛后定点 minor 编辑见文末「R4 收敛后定点编辑」) — 全部任务 `pending`, ready for B.1 (待 owner: 版本档 / O-1 / O-3)
> **Scope**: **三个仓** — `aria/` 子模块 (@ `d69091d`, v1.67.2: 两个新建文件 + 一份 SKILL.md 两 hunk + 一个新建测试文件 + 版本 5 文件) · `standards/` 子模块 (@ `334c609`: 一份模板) · 主仓 (@ `c120f9e`: `.aria/state-checks.yaml` 注册 + 白名单数据文件 + 两个 gitlink + 版本引用面 + AB 结果 + Spec 本体)
> **ship target**: aria-plugin **`<vNEXT>`** (R1/C3 三份统一占位, 本文件**不写** v1.68.0 / v1.67.3 字面; proposal §Impact 自判 **MINOR**, ⚠️ 两条 CLAUDE.md 判据都不字面覆盖本例; 档位 = **MINOR** (2026-09-01 技术裁定, 决策单 §H1: `version-management.md §2.2`「功能增强 (向下兼容)」字面覆盖), 三份串行 ship 各占一号 (字段 → 探针 → 母), 不合并一版; 号段落地时按当时 `plugin.json` 计算)
> **ship order (owner 2026-08-30 O-4 (i))**: **本 Spec 先 ship**; 纯函数 `aria/skills/state-scanner/lib/linked_issue_field.py` 是姊妹 Spec `sibling-spec-probe` 的**硬前置** (其 §1 依赖方向第 3 条 / §3 import 块逐字 `from lib.linked_issue_field import extract_linked_issue_field`)。母 Spec `a1-entry-claim-duplicate-work-guard` 与本 Spec **任意顺序** (其 §2 `:125` 模板行两阶段取法: 脚本存在 ⇒ 用 `--emit-arg` stdout, 不存在 ⇒ 手工按 E6)。

> **为什么出 tasks.md** (proposal 头部写「Level 2 … 不出 `tasks.md`」): (1) rule6_note 有**四条**必须各自独立成任务的 Rule #6 处置 (照跑 / 定向 fixture / 套件缺口 issue / substitute), 先例 `linked-issue-normalization` 正是因「owner 亲裁的 Rule #6 处置无独立落地载体」被 R3′ 两席命中而从 Level 2 升 Level 3; (2) 三仓交付 + 两个 gitlink bump 的次序 proposal `:601` 明写「属 A.2」, 需要可被归档门与 handoff 机械消费的 checkbox 载体; (3) proposal `:388` 升格的显式验收项需要一个 TASK。**这是 A.2 的流程判断, 非 owner 裁定 —— 留痕请复议** (Rule #10)。proposal 的 Level 自陈本文件**不改** (A.2 不编辑 proposal.md)。

---

## 范围边界 — 本文件到哪里为止

| 阶段 | 归属 | 理由 |
|------|------|------|
| 组 1–4: 测试 / 实现 / 写入侧文档 / Rule #6 | **本文件** | change 自身交付物 |
| 组 5: 回归 + 版本面 + **两个子模块的本地合并 + 双推 + 逐 remote `ls-remote` 核验 + 主仓 gitlink bump** | **本文件** (5.3 / 5.4 本地执行, CLAUDE.md 多远程硬约束 1+2) | 子模块合并**禁**走 Forgejo 服务端 merge (硬约束 1); `phase-c-integrator` 只承接主仓 PR + pre-merge 闸门 |
| Phase C: 主仓 PR 创建 / **pre-merge gate (Rule #8)** / merge | **`phase-c-integrator`** (5.6 交付) | 通用流程, 本文件不复述其判据 |
| Phase D: cycle 进度 / Spec 归档 / 周期 handoff (Rule #9) | **`phase-d-closer`** | 归档门会消费本文件全部 checkbox 状态, 故每条必须真做完 |
| 采用方侧 check 自动注册 / 回填 6 份 M6/M7 proposal / 改归一算法 / 编辑母 Spec 的 SKILL.md hunk | **不在本文件** | proposal §非目标 + O-1 / O-3 (2026-09-01 已裁: 维持, 决策单 §H4) |

---

## Task Group Overview

| 组 | 主题 | 依据 |
|----|------|------|
| **1** | 测试先行 (RED) — `aria/skills/state-scanner/tests/test_linked_issue_field.py` (新建) 承载 SC-1~6 / SC-7a / SC-8 / SC-9 + 坏实现拒绝矩阵 | proposal §Success Criteria「验证宿主」表 (逐字路径) |
| **2** | 实现 (GREEN) — 纯函数 + 探针两模式 + 仓本地白名单 + check 注册 + `${CLAUDE_PLUGIN_ROOT}` 实测 | §3 E0–E6 · §4 六臂 · D3/D4/D6 · `:388` |
| **3** | 写入侧文档 — SOT 模板 (跨仓) + spec-drafter hunk A / hunk B | §1 · R5/C1 · D8/D9 |
| **4** | Rule #6 逐 hunk 四件 — 照跑 / 定向 fixture / 套件缺口 issue / substitute 留痕 | rule6_note 表 (五格) |
| **5** | 回归 + 版本面 + 两子模块本地合并双推 + gitlink ×2 + 主仓版本引用面 + 交付 Phase C | §Impact 版本号/发版同步面 · CLAUDE.md 硬约束 1/2 · `:601` |

**排序依据**: 组 1 → 组 2 是 RED-first (baseline 无任何实现, 全部 SC 今天必红 —— 每条 SC 的「它怎么会红」列已在 proposal 成文, 本文件逐条引用不复述)。**同文件一律串行 (同文件)** (R1/C1, A2 9b64d749): 组 1 六条同写一个新建测试文件 ⇒ **1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6** 链式落盘 (允许并行设计/评审, 落盘串行); **2.2 → 2.3** (同写探针脚本); **3.2 → 3.3** (同写 `spec-drafter/SKILL.md`, 落点物理不相邻 ≠ 可并发写); **4.1 → 4.2 → 4.3 → 4.4** (同写 `spec-drafter.json` / `ab-results/` 子目录 `RESULT.md`)。组 3 与组 2 可并行 (不同文件), 但 **3.2 / 3.3 必须早于 4.1 / 4.2** (AB 测的是那两个 hunk 的行为影响)。2.1 的 `dependencies` 含 1.6 (其 verification 引 1.6 矩阵作验收依据, R1/A3 c23f47ce)。**2.6 (`${CLAUDE_PLUGIN_ROOT}` 实测) 无依赖 (不同文件), 可最早做**, 其结论只进审计轨, **不**回写任何文档 (`:388` 禁预写)。组 5 gate 在组 1–4 全绿之后, 内部 **5.1 → 5.2 → 5.3 (aria) ‖ 5.4 (standards) → 5.5 → 5.6** (5.3 ‖ 5.4 的 deliverables 是两个不同 gitlink, 不同文件); 子模块合并 + gitlink bump **先于**主仓 PR (否则主仓 PR 里 gitlink 未变, `phase-c-integrator` C.2.4.5 只会输出 `unchanged`, bump 全程无 PR 无闸门 —— 先例 `linked-issue-normalization` R4 教训)。

**三仓交付次序 (`:601` 的 A.2 落版)**: **aria 先** (它是探针 Spec 的硬前置, 且版本号与 AB 结果都挂在它上) → **standards 独立** (模板与代码无耦合, 可与 aria 并行合并; 其 gitlink 与 aria gitlink 在**同一个主仓 commit** 里 bump, 使主仓 PR 一次携带两处指针) → **主仓 PR 最后** (Spec 本体 + `.aria/` 两文件 + 版本引用面 + AB 结果 + 两 gitlink)。⚠️ 两子模块都**没有**「被 bump gitlink」之外的下游, 故都受硬约束 1 (本地 merge)。

---

## 1. 测试先行 (RED) — `aria/skills/state-scanner/tests/test_linked_issue_field.py` (新建)

> 宿主按 proposal「验证宿主」表**逐字采用**; 目录实存 (与 `test_release_by_track.py` / `test_coordination_default_lockin.py` 同级)。sys.path 体例仿 `test_release_by_track.py:23-25` (`_SKILL_ROOT = parents[1]` + `from lib.… import`); CLI 断言仿其 `:531` `_GATE = Path(_SKILL_ROOT) / "scripts" / …` 用 `subprocess`。夹具一律**内联字符串** (aria 子模块内的测试不得依赖主仓语料; 复用真实语料的条目**逐字嵌入**并注明来源路径)。
> **SC-6 / SC-8 (a)(c) 读的是主仓文件** (`standards/…/proposal-minimal.md` / `.aria/state-checks.yaml`) —— proposal 只对 SC-6 声明了「跨仓读取 fail-soft 为 skip」; **SC-8 (a)(c) 同形, 本文件按同一已知限处置** (`skipTest` + 打印原因), 见「发现的 Spec 内部问题」#3。

- [x] 1.1 SC-1 (E0 定位三谓词 + 两拼写集合封闭, 夹具 (a)–(g) + A.2 补 (h) 非 ASCII 折叠负控) + SC-2 (E2 起始位, 逐字复用 `openspec/archive/2026-06-11-audit-drift-guard/proposal.md:5` 原文)
- [x] 1.2 SC-3 (E4/E5/E6 多值 (a)(b)) + SC-4 (哨兵六分支 (a)–(f); E5 吃 E3 原始串)
- [x] 1.3 SC-5 (探针 check 模式六臂 (a)(b)(c)(d)(e1)(e2), CLI 全链路 `subprocess`, 临时项目根夹具; (d) 用「复制 skill 骨架去掉 `lib/collision.py`」构造真实降级)
- [x] 1.4 SC-9 (`--emit-arg` 四夹具 (a)–(d), CLI 全链路; 失败态 stdout 必空)
- [x] 1.5 SC-6 (SOT 模板恰一条 E0 命中 + canonical 拼写 + Usage Note + spec-drafter 引用路径存在; 跨仓 skip) + SC-7a (预览围栏 (i) 四行顺序 + (ii) 哨兵负控; 块边界 = 围栏) + SC-8 (三臂: 注册条目 / 路径在 `aria/skills/` 下 / 实跑首行前缀; 跨仓 skip)
- [x] 1.6 坏实现拒绝矩阵 — 把 proposal 各 SC「它怎么会红」列点名的坏实现写成同文件内的 `_bad_*` 抽取器, 断言每条夹具对**至少一个**坏实现产生与期望不同的结果 (memory `adversarial-fixture`: 验「拒绝能力」, 非当前取值)

## 2. 实现 (GREEN)

- [x] 2.1 `aria/skills/state-scanner/lib/linked_issue_field.py` (**新建**, 纯函数, stdlib-only) — `FieldVerdict` + `extract_linked_issue_field(text: str)` 按 E0–E6 逐字节实现; 附 `is_sentinel()` / `emit_arg()` 导出 (哨兵集合与 E6 四格表的**唯一**代码宿主); `lib/collision.py` **零改动**
- [x] 2.2 `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**) check 模式 — `argv[0]` 项目根 + `--grandfathered <path>`; 六臂 fail-CLOSED 分区 + 陈旧守卫 (a)(b)(c); 导入 = 包父目录 + `from lib.linked_issue_field import …` (D4), **不得** import `scripts/lib`; `audit-engine/` 下**不存在**名为 `lib/` 或 `collectors/` 的顶层目录 (`:278` 逐字; 不断言目录条目总数 — 探针 Spec 新建 `scripts/` + `tests/` 合法, R1/C4)
- [x] 2.3 同脚本 `--emit-arg <proposal.md>` 模式 — E6 四格表的 CLI 宿主 (SC-9); 只有 `OK` 且非哨兵打印第一个 token 元素, 其余空 stdout + exit 0; 探针自身失败 exit 2 且 stdout 空
- [x] 2.4 `.aria/linked-issue-field-grandfathered.txt` (**新建**, 主仓, 仓本地数据) — 6 条 `openspec/changes/aria-2.0-m{6,7}-*` 路径 + 头注 (格式 / 陈旧守卫 / 「回填一份删一条」/ O-1 指针)
- [x] 2.5 `.aria/state-checks.yaml` 注册 `linked-issue-field-availability` — 逐字照 §4 骨架, **只用既有 7 个键**; 追加在文件末尾; 注册后实跑 command 得首行前缀 ∈ {`OK`, `FAIL`, `##SKIP##`}
- [x] 2.6 **A.2 显式验收项 (`:388`)**: 实测 `${CLAUDE_PLUGIN_ROOT}` 是否被导出到 Phase 1.11 的 check 子进程 — 临时注册 `command: echo "${CLAUDE_PLUGIN_ROOT:-UNSET}"` 探针, 在 **Claude Code 会话内**跑一次 `/state-scanner`, 读回显; 结论**只追加进审计轨**, 临时条目撤除 (`git diff .aria/state-checks.yaml` 为空); **不**在任何文档预写采用方可移植写法

## 3. 写入侧文档

- [x] 3.1 `standards/openspec/templates/proposal-minimal.md` (**跨仓 SOT**) — `:5` `> **Created**:` 后增一行 `` > **Linked Issue**: `{<org>/<repo>#<n>}` ``; `## Template Usage Notes` (`:40`) 增「无关联 (已核实) 时逐字写 `` `none` ``, 不留空、不删行」; **不写**中文 alias (写入侧只教 canonical)
- [x] 3.2 `aria/skills/spec-drafter/SKILL.md` **hunk A** — 正文声明 `Linked Issue` 字段**必填** + 写法引 proposal §3 (`<org>/<repo>#<n>` code span 形 / 多值 `, ` / 无关联 `` `none` ``); 落点在围栏外、不在 `:127-162`、不碰 `:10` frontmatter (归母 Spec)、与母 Spec「前置: REQUIRE claim (A.1, MUST)」块不同 hunk
- [x] 3.3 同文件 **hunk B** — `### Level 2 预览` 围栏 (`:127-162`) 头部 `:140` `> **Status**: Draft` 后插两行 `> **Created**: {YYYY-MM-DD}` 与 `` > **Linked Issue**: `{<org>/<repo>#<n>}` `` (placeholder 与 SOT 同串, **不写哨兵**; SC-7a)

## 4. Rule #6 (逐 hunk, 四件各自独立, ⛔ 不申请豁免)

- [x] 4.1 用 `/skill-creator` 对 **3.2 + 3.3 两 hunk** 照跑 `aria-plugin-benchmarks/ab-suite/spec-drafter.json` 全部现有 eval (当前观测 2 条: id 1 / id 2; ship 时按 `len(evals)` 取, 不锁字面), **同批更新 eval id 2 expectations** (字段名 `Linked Issue` / 无关联 `none`, R5/M2); 会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动 (rule6_note ⛔ 段); 结果落 `aria-plugin-benchmarks/ab-results/<date>-v<ship>-linked-issue-field-rule6/` (含 `PREDICTION.md` 先于实测)
- [x] 4.2 **可证伪定向 fixture ×1 (SC-7 双臂)** — `spec-drafter.json` 新增 eval (id = 该文件当时 `max(id)+1`, ship 时读取不硬编码, @ `c120f9e` 为 3; 本 Spec 先 ship 取到 3, 母 Spec 后 ship 顺延 — R1/C5 三份同写) (中文臂: 新建 Level 2 proposal, 评分锚定「头部含过 E0+E2+E5 的 `Linked Issue` 行 / 无关联逐字 `none`」); 英文臂 = 更新后的 eval id 2 (SC-7 原文「后者即 eval id 2 的场景」); 两臂各自对 baseline (v1.67.2) 与新版实跑, 须有区分力 (省略 / markdown 链接形 / 留空 / 译写成别的字段名 的臂可辨); **同批程序化重算 `ab-suite/version.yaml`** (`ls ab-suite/*.json | wc -l` + python 遍历各 json 的 `len(evals)` 求和, 不写字面计数; R1/C5); 串行于 4.1 之后 (同文件)
- [x] 4.3 套件缺口 issue — **A.2 裁量: 归并到 `aria-plugin#117`** (open, 「AB 测试集缺 authoring 维度」类级 issue), 以评论追加本 Spec 为第二个实例 + 4.2 的 新 eval (id = ship 时 max(id)+1, 今日观测 3) 作为该维度的首条已落地 fixture; **不新开** issue (理由见「A.2 裁量」段; owner 可改判新开) **产物**: `aria-plugin-benchmarks/ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/RESULT.md` §「#117 评论」(comment 20573, `forgejo GET …/issues/117/comments` 回读核验) + `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md` §B5
- [x] 4.4 substitute 留痕 — 模板 hunk (SC-6) 与探针/注册 hunk (SC-4/5/8) 走 substitute: 在 `d69091d` 基线 worktree 上跑 1.x 测试文件证明**红** (ImportError / 断言失败逐条记), 在实现后证明**绿**; 记录进 4.1 的 `RESULT.md` 「逐 hunk 处置表」, 与 AB 结果并列, 缺一则该 hunk 回落照跑

## 5. 回归 + 版本面 + 跨仓交付 + 交付 Phase C

- [x] 5.1 全量回归 — `cd aria/skills/state-scanner/tests && python3 run_tests.py` OK 且 0 failures/errors (基线静态 `def test_` 计数 **1425** @ `d69091d`, 新增数 = 1.x 落盘的 test 方法数); `bash aria/skills/run_all_tests.sh` 0 FAIL; `git -C aria diff --stat -- skills/state-scanner/lib/collision.py skills/state-scanner/SKILL.md` **为空**
- [x] 5.2 aria 子模块版本面 bump (按引用点, 先例 `linked-issue-normalization` 5.9): `plugin.json` (SOT) / `marketplace.json` **2 点** (`:3` / `:16`) / `README.md:5` / `VERSION` (append-only 账本: 头部当前版本行 + 追加发布注, 行数不减) / `CHANGELOG.md` 追加条目 (不含 skill 设计术语外泄到 CLAUDE.md)
- [x] 5.3 aria 子模块 **本地** merge feature 分支 → master + `git push origin && git push github` + **逐个** `git ls-remote <remote> master` 与本地 SHA 比对全部一致 + tag `v<ship>` 双推 + 主仓 gitlink bump 到 post-merge master SHA (硬约束 1/2; push 显式给足超时, memory `partial-push`) (2026-09-02 完成: 本地 --no-ff merge fe32441 + tag v1.68.0 + 主仓 gitlink; owner 授权后双推, origin/github `ls-remote master` = fe32441、`refs/tags/v1.68.0` 两端 present, 与本地逐一 MATCH。**pre_merge R1 清账 PATCH v1.68.1 `d1caa66` + tag 同法双推核验, 主仓 gitlink 随之 → d1caa66**)
- [x] 5.4 standards 子模块 **本地** merge → master + 双推 + 逐 remote `ls-remote` 核验 + 主仓 gitlink bump (**跨仓交付面**; aria-standards 实测无 `VERSION` / `CHANGELOG.md` / tag, 只做 commit + 双推 + gitlink; 是否版本化留 owner) (2026-09-02 完成: 本地 --no-ff merge fad8b4b + 主仓 gitlink 同 commit; owner 授权后双推, origin/github `ls-remote master` = fad8b4b MATCH; 不版本化, 决策单 B4。**pre_merge R1 清账 `ffed204` (Usage Note 英文化) 同法双推核验, gitlink → ffed204**)
- [x] 5.5 主仓版本引用面 14 点 (与 086ee32 同口径) — `CLAUDE.md:139/:141` / `VERSION:24` / `README.md:8` badge + `:242` Plugin Version / i18n ×3 各 3 点 (`:3` translated-from / `:10` badge / `:244` Plugin Version; **仅版本串**, 正文无实质变更不重译, #140 B 档); custom checks `m6-version-badge-match` / `m6-claude-md-version` / `i18n-readme-translation-currency` / `main-project-version-consistency` 全 OK
- [x] 5.6 主仓 PR (Spec 本体 + `.aria/` 两文件 + 两 gitlink + 版本引用面 + `ab-results/` + `ab-suite/spec-drafter.json`) → 交付 `phase-c-integrator` C.2.4 pre-merge gate (Rule #8); PR body 列 2.6 实测结论 + 待 owner 项 (O-1 / 版本档 / #117 归并 / standards 版本化) (2026-09-02: feature 分支已推 origin, **PR #190** 已建, C.2.4 green (not_applicable, main in-flight 清) + C.2.4.5 PASS; **merge = owner 动作**, 合并后 phase-d-closer 归档) **→ 已合并 `888b893` (2026-09-02 18:11Z, pre_merge 收敛审计 R1–R5 四票 PASS 0C/0M, owner 选 [1] 接受结论); origin/github master 一致**

---

## SC → TASK 覆盖表 (proposal §Success Criteria 全部 10 条, 无遗漏)

| SC | 类别 | 测试任务 (RED) | 实现 / 交付任务 (GREEN) | 宿主 (逐字) |
|----|------|----------------|--------------------------|-------------|
| SC-1 | 代码 | 1.1 (TASK-001), 1.6 (TASK-006) | 2.1 (TASK-007) | `aria/skills/state-scanner/tests/test_linked_issue_field.py` |
| SC-2 | 代码 | 1.1 (TASK-001), 1.6 | 2.1 (TASK-007) | 同上 |
| SC-3 | 代码 | 1.2 (TASK-002), 1.6 | 2.1 (TASK-007) | 同上 |
| SC-4 | 代码 | 1.2 (TASK-002), 1.6 | 2.1 (TASK-007) | 同上 |
| SC-5 | 代码 (CLI) | 1.3 (TASK-003) | 2.2 (TASK-008), 2.4 (TASK-010) | 同上 (`subprocess`) |
| SC-6 | 代码 (跨仓 skip) | 1.5 (TASK-005) | 3.1 (TASK-013), 5.4 (TASK-023) | 同上 |
| SC-7 | **行为** (定向 fixture) | — (无代码宿主, 不冒充) | 4.2 (TASK-017), 4.1 (TASK-016) | `aria-plugin-benchmarks/ab-suite/spec-drafter.json` 新 eval (id = ship 时 max(id)+1, 今日观测 3) + id 2 |
| SC-7a | 代码 | 1.5 (TASK-005) | 3.3 (TASK-015) | `test_linked_issue_field.py` (读兄弟 skill `spec-drafter/SKILL.md`) |
| SC-8 | 代码 (跨仓 skip) | 1.5 (TASK-005) | 2.5 (TASK-011), 2.2 (TASK-008) | 同上 |
| SC-9 | 代码 (CLI) | 1.4 (TASK-004) | 2.3 (TASK-009), 2.1 (TASK-007 `emit_arg`) | 同上 (`subprocess`) |

**覆盖: 10/10。未覆盖: 无。**

## Impact 表覆盖对账 (proposal §Impact 逐行)

| Impact 行 | 任务 |
|-----------|------|
| `aria/skills/state-scanner/lib/linked_issue_field.py` (新建) | 2.1 |
| `.aria/linked-issue-field-grandfathered.txt` (新建) | 2.4 |
| `standards/openspec/templates/proposal-minimal.md` (SOT) | 3.1 (编辑) + 5.4 (合并/双推/gitlink) |
| `aria/skills/spec-drafter/SKILL.md` hunk A / hunk B | 3.2 / 3.3 |
| `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (含 `--grandfathered` / `--emit-arg`) | 2.2 / 2.3 |
| `.aria/state-checks.yaml` 注册 | 2.5 |
| `aria/skills/state-scanner/lib/collision.py` 零改动 | 2.1 / 5.1 (git diff 为空断言) |
| `openspec/changes/aria-2.0-m{6,7}-*/proposal.md` ×6 不改 | 2.4 (在册; O-1 指针) |
| AB `ab-suite/spec-drafter.json` 照跑 + eval id 2 expectations (`ARIA_COORDINATION_NO_PUSH=1` / `--no-push`) | 4.1 |
| AB 覆盖外档: 定向 fixture ×1 + 套件缺口 issue (`aria-plugin#117`) | 4.2 / 4.3 |
| 版本号 (MINOR 自判) | 5.2 (aria) / 5.5 (主仓) |
| 发版同步面 (CLAUDE.md §版本管理; 硬约束 1/2) | 5.3 / 5.4 / 5.5 / 5.6 |

**每个 `--flag` 的落点**: `--grandfathered` → 2.2 / 2.4 / 2.5 / 1.3; `--emit-arg` → 2.3 / 1.4 (母 Spec `:125` 消费); `--linked-issue` → 2.1 `emit_arg` / 2.3 / 1.2 / 1.4 (本 Spec **不调用**它, 只产生其实参); `--no-push` / `ARIA_COORDINATION_NO_PUSH` → 4.1 / 4.2。(每个落点 TASK 的 verification 含该 flag 字面, 程序化验见「机械核验」— R1/A4 62285020)

## A.2 显式指令对账 (`grep -n 'A\.2' proposal.md` 逐条)

| 行 | 指令 | 落点 |
|----|------|------|
| `:3` / `:616` | 「待 owner 批准进 A.2」 | 已批准 (2026-08-30), 本文件即 A.2 产物 |
| `:8` | 拆分依据叙述 (非指令) | — |
| `:278` | `audit-engine` 内不得新建 `lib/` / `collectors/` 顶层目录; 探针 helper 放 `scripts/` 并用模块名前缀 (原给探针 Spec, 本 Spec 涉跨 skill import 同守) | 2.2 / 5.1 verification (R1/C4 逐字对齐 proposal): `audit-engine/` 下**不存在**顶层 `lib/` 与 `collectors/` (`test ! -d …/lib && test ! -d …/collectors`); **不**断言「只有 `references/` + `SKILL.md`」(那会在探针 Spec 交付 `scripts/` + `tests/` 当天恒红, A1 c23f47ce); 本探针零 helper 模块, 仅 import `lib.linked_issue_field`; 不 import `scripts/lib` |
| `:388` | 升格为 A.2 显式验收项: 实测 `${CLAUDE_PLUGIN_ROOT}` 是否导出到 Phase 1.11 子进程; 实测前不得预写可移植写法 | **2.6 (TASK-012)** 独立任务; 结论只进审计轨; 本文件与 2.5 注册行只用 Aria 仓字面路径 |
| `:490` (D1) | 抽取规则**不** defer 到 A.2 | 2.1 verification: E0–E6 按 proposal 字符级文本实现, **A.2 不重释**; 本文件补的只是 spec 明写「未定义」处的确定性选择 (见「A.2 裁量」) |
| `:506` / `:580` | 套件缺口 issue「归并或新开由 A.2 定」 | **4.3: 归并 `aria-plugin#117`** (理由见下) |
| `:508` | 若 A.2 落地需改 `state-scanner/SKILL.md`, 该 hunk 另行按判据表重判 | 本文件**不改**它 (5.1 断言 git diff 为空); 若 Phase B 发现必须改 → 停, 回 A.2 重判 Rule #6 (不得顺手改) |
| `:521` | 叙述 (验证宿主为何必须声明) | 组 1 宿主逐字采用 |
| `:601` | 三仓交付顺序与 gitlink bump 次序未排, 属 A.2 | 「三仓交付次序」段 + 5.3 / 5.4 / 5.6 |

## A.2 裁量 (非 owner 裁定, 留痕请 post_planning / owner 复议)

1. **套件缺口 issue 归并 `aria-plugin#117` 而非新开**。实核 (`forgejo GET /repos/10CG/aria-plugin/issues/117`, 2026-08-30): **open**, 标题「[benchmark] AB 测试集缺 authoring 维度 — 全套件零 eval 覆盖『作者读处方性向导做判断』类行为」, 正文点名 `spec-drafter.json` (2) 「均为产出/判级/路径类, 无 authoring 形态」。本 Spec 的缺口 (「spec-drafter authoring 时是否写出某字段」) 是**同一类级缺口的第二个实例**, #117 本身就是按「类」开的; 新开 = 同一类两个跟踪点 (memory `fix-the-class`)。归并方式 = 评论追加实例 + 把 4.2 的 新 eval (id = ship 时 max(id)+1, 今日观测 3) 作为该维度首条已落地 fixture 登记, 使 #117 的「建议 1: 补 authoring 维度 eval」有第一个可复用样本。
2. **SC-7 双臂的落法**: 中文臂 = 新增 新 eval (id = ship 时 max(id)+1, 今日观测 3) (定向 fixture ×1); 英文臂 = eval id 2 更新 expectations 后即是 (SC-7 原文「后者即 `spec-drafter.json` eval id 2 的场景」)。不为英文臂再开 下一个 id (ship 时 max(id)+1)。
3. **`FieldVerdict` 在 proposal 钉的 4 字段外追加 additive 字段 `bad_elements: tuple[str, ...]`** (默认空) —— 否则 `BAD_TOKEN`「点名那个元素」要么在探针里重跑一遍 E5 循环 (第二份实现), 要么无处输出。additive, 探针 Spec 的消费 (`verdict` / `token_str` / `token_elements` / `line_no`) 不受影响。
4. **导出 `is_sentinel(token_str)` 与 `emit_arg(fv)`** 两个辅助纯函数: 哨兵集合 (§2) 与 E6 四格表 (K8) 都是「由本 Spec 定义, 全仓引用」的东西, 给它们唯一代码宿主, CLI `--emit-arg` 只是 `print(emit_arg(...))`; 探针 Spec 层 1.5 可直接 import `is_sentinel` 而不重写折叠逻辑。
5. **陈旧守卫 (b) 的判定**: proposal 字面「路径存在但已移出作用域 (已归档)」自相矛盾 (移到 archive 后 changes 下那条路径就不存在了)。落版: 条目在 `openspec/changes/` 下**不存在** ⇒ 若 `openspec/archive/*-<slug>/` 存在 → (b), 否则 → (a); 条目存在且 verdict `OK` → (c); 条目不以 `openspec/changes/` 起首 → (b)。
6. **两类 FAIL 同时出现时的输出顺序** (proposal「新表面」#2 自陈未定义): 先违规条目 (按路径字典序, 每条一行 `path:line VERDICT 细节`), 后陈旧条目 (`FAIL allowlist 陈旧: <path> (a|b|c)`), 首行 `FAIL <n> 项`; 顺序确定性是为「两个实现者得同一输出」(memory `spec-underdetermination`)。
7. **`--emit-arg` 失败态 exit code = 2** (proposal 只说「非 0」); stdout 必空, 原因到 stderr —— 母 Spec 模板「空 ⇒ 省略」在失败态也安全。
8. **`--grandfathered` 相对路径以项目根 (argv[0]) 解析**, 不以 cwd (分发到采用方后 cwd 不由本仓决定, 与 §4 理由 4 同一精神)。
9. **字段名折叠用 `re.IGNORECASE | re.ASCII`** (Python 无 `re.ASCII` 时 `[a-z]`+IGNORECASE 还会匹配 `K` U+212A 等 4 个非 ASCII 字母), 并在 1.1 加负控夹具 (h) `LinKed Issue` ⇒ `NO_FIELD` —— 这是 E0「折叠只作用于 ASCII 字母」的直接推论, 非新规则。
10. **注册条目追加在 `.aria/state-checks.yaml` 末尾** (并发轨 08-29/30 刚在末尾加第 12 条 `forgejo-app-token-liveness`; 末尾追加是最小合并冲突面), 不插进 plugin 侧两条中间。

## 发现的 Spec 内部问题 / 陈旧行号 / 待 owner (A.2 不自行拍板)

> **2026-09-01 分工裁定** (owner: 产品级 owner / 技术级 AI): #5 (O-1) / #6 (版本档) 已裁 (决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md` §H4a / §H1); #7 (aria-standards 版本化) / #8 (#117 归并) 属技术级, 由 AI 在 B 期落点裁定并追记该决策单, 不再等 owner。

1. **陈旧数字 (非矛盾, 照 proposal 自己的纪律「口径是规范, 数字是观测」)**: `.aria/state-checks.yaml` 今日 `grep -c '^  - name:'` = **12** (proposal 记 10 / 11; 第 12 条 `forgejo-app-token-liveness` 08-30 并发轨加入); `CLAUDE_PLUGIN_ROOT` 仍零命中。`changes/` 9 份 / 两拼写严谓词 17 文件, 与 proposal 一致。
2. **路径写法**: proposal 写 `collectors/custom_checks.py:63 / :122-123 / :399`, 真实路径是 `aria/skills/state-scanner/scripts/collectors/custom_checks.py` (`:63` 注释 / `:121-124` docstring / `:399` `config_path`), 本文件按真实路径写。
3. **SC-8 (a)(c) 的跨仓读取与 SC-6 同形但 proposal 未声明已知限** —— 本文件按 SC-6 的 fail-soft 处置 (主仓文件不存在 ⇒ `skipTest`); 请 post_planning 确认或 owner 裁是否回写 proposal (A.2 不改 proposal)。
4. **§4「本探针除 stdlib 外只 import 这一个符号」写的是 `normalize_linked_issue`** (R3/C3 之前的文本); 纯函数落版后探针唯一非 stdlib import 应是 `lib.linked_issue_field.extract_linked_issue_field` (E5 在纯函数内调 `normalize_linked_issue`)。本文件按后者落, `##SKIP##` 文案仍点名「归一 SOT 不可导入」。
5. ~~**待 owner O-1**~~ **✅ O-1 已裁 (2026-09-01 技术裁定, 决策单 §H4a)**: 不回填 + `GRANDFATHERED` 在册 (维持本文件落版); 6 份由 M6/M7 轨自己在下次触碰各 proposal 时回填并各删一条, 探针零改动。判据: fail-CLOSED 白名单已满足产品目标 (新 Spec 必声明), 回填对撞车检测零增益且是跨轨写入。
6. ~~**待 owner 版本档**~~ **✅ 版本档已裁 (2026-09-01, 决策单 §H1)**: **MINOR** (SOT `version-management.md §2.2`「功能增强 (向下兼容)」字面覆盖本 Spec; CLAUDE.md 两句是缩写); 三份串行各占一号 (字段 → 探针 → 母), 不合并一版; 号一律 `<vNEXT>` 占位、落地时按当时 plugin.json 计算 (统一句见 yaml TASK-021 notes); 5.2 可按依赖开工。
7. **待 owner**: aria-standards 是否需要版本化 (实测该子模块无 VERSION / CHANGELOG / tag; `version-management.md:254` 写「独立版本 (standards-v2.1.0)」但仓内无对应工件)。
8. **待 owner**: #117 归并 (裁量 1) 是否改判新开。
9. **预备观测 (不替代 2.6)**: A.2 执笔的 subagent Bash 环境里 `CLAUDE_PLUGIN_ROOT` = **UNSET** (11 个 `CLAUDE*` 变量存在); `state-scanner/SKILL.md:71` 自身也用 `${CLAUDE_PLUGIN_ROOT:-aria}` 回落 —— 即 Aria 仓内实际走的是回落值 `aria`。2.6 仍须在 Phase 1.11 真实子进程路径上实测。
10. **母 Spec 的 spec-drafter hunk 位置未钉** (其 SC-22 只钉了 phase-a-planner 的 `:60` 之前); 3.2 的落点选择因此只能写「不同 hunk」约束 + 落地时 `git merge-tree` 干跑核验, 不能预先断言零冲突。

---

## R1 清账对账 (2026-08-30)

> post_planning R1 (五席 `post_planning-R1-1788102593777-a1-entry-combined-A{1..5}`) 中 scope 含本 Spec 的 finding + 主控跨 Spec 统一项 (C1 / C3 / C4 / C5 / C7 / C9) 的逐条处置。修法 = 定点编辑 (不重写文件); 不改编号; 不改 proposal.md。同 8-hex id `c23f47ce` 在 A1 与 A3 各指一条**不同** finding, 下表以「席」区分。

| finding id | 席 | 严重度 | 处置 | 改动落点 |
|------------|----|--------|------|----------|
| 9b64d749 | A2 | critical | closed — 同文件任务全部串行 (同文件): 组 1 六条链式 001→…→006, 008→009, 014→015, 016→017→018→019; `execution_order` 删除同文件「parallelizable / 并行 / `{…}`」记法 | yaml TASK-002/003/004/005/006/009/015/017/019 `dependencies` + `execution_order` 全段; tasks.md「排序依据」 |
| c23f47ce | A3 | major | closed — TASK-007 `dependencies` 加 TASK-006 (其 verification 引矩阵作验收依据) | yaml TASK-007 `dependencies`; tasks.md「排序依据」 |
| c23f47ce | A1 | major | closed — `audit-engine/` 断言改为 proposal `:278` 逐字「不存在顶层 `lib/` / `collectors/`」, 删「只有 references/ + SKILL.md」字面 (探针 Spec 的 `scripts/` + `tests/` 合法); finding 处方点名的 tasks.md `:57` / `:129` 两行同步 (方案 C4 只列 yaml 两行, 此处按 finding 补齐, 见汇报) | yaml TASK-008 verification (`:278` 条) + TASK-020 verification; tasks.md 2.2 + A.2 对账 `:278` 行 |
| 6698004d | A1 | major | closed (本 Spec 侧) — TASK-017 deliverables 加 `ab-suite/version.yaml`, verification 写「按实际文件程序化重算, 不写字面计数」; metadata `exports_for_siblings.seam_rules` 收录「改 `ab-suite/*.json` 同批重算 version.yaml」; 探针 / 母 Spec 侧由各自执笔席 | yaml TASK-017 deliverables + verification; metadata seam_rules; tasks.md 4.2 |
| 35dad35d | A1 | major | closed (本 Spec 侧) — TASK-017 `dependencies` 加 TASK-016 (同写 `spec-drafter.json`); eval id 分配约定三份同写 (max(id)+1, ship 时读取, 本 Spec 取到 3, 母顺延); TASK-016 标题 / rule6_note / tasks.md 4.1 的「2 evals」改「全部现有 eval (当前观测 2 条)」 | yaml TASK-016 title + verification, TASK-017 `dependencies` + verification, metadata rule6_note + seam_rules; tasks.md 4.1 / 4.2 |
| 96ecdeb4 | A1 | major | closed — placeholder `{<org>/<repo>#<n>}` 两个写入宿主 (TASK-013 模板 / TASK-015 hunk B) 各加 verification「逐字节 = 探针 SC-19 `_RAW_KEY_BLACKLIST` 字面 (grep 探针 proposal SC-19 行取值), 改动须同批改两 Spec」; metadata 建 `exports_for_siblings.seam_rules` 收录 | yaml TASK-013 / TASK-015 verification; metadata seam_rules |
| 3221f943 | A1 | major | closed (本 Spec 侧, 方案 C3) — 版本字面 v1.68.0 / v1.67.3 全部改 `<vNEXT>` 占位; TASK-021 notes 落三份统一句 (串行各占一号 / 合并一版由母承接 / 未裁 `pending` 不 `blocked`); owner 决策项 (是否合并一版) 留痕不拍板 | tasks.md `:7` + 待 owner #6; yaml metadata.ship_target, TASK-021 verification + notes, TASK-024 verification |
| 970d3368 | A1 | minor | closed — TASK-008 SKIP 文案「版本 < v1.68.0」改 `<vNEXT>` + 「落地时以 plugin.json 实际号回填并在 PR 点名」 | yaml TASK-008 verification (导入逐字条) |
| df090b25 | A4 | major | closed — 25/25 `est_hours: int` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" / L "6-8", DUAL_LAYER_SPEC.md:166 + 母 Spec 同形); metadata 加 `estimated_hours: "50-86"`; summary 同步; TASK-020 补 `reason` | yaml 全部 25 task + metadata.estimated_hours / estimation_note + summary.by_complexity; TASK-020 `reason` |
| 62285020 | A4 | minor | closed — 覆盖表 4 对缺 token 补入 verification 正文: (SC-5, TASK-010) (SC-8, TASK-008) (SC-9, TASK-007) (SC-7, TASK-016); flag 映射: `--linked-issue` 字面补入 TASK-002/004/007, `--no-push` 补入 TASK-016/017; 程序化验 28 对 SC + 12 对 flag 全部命中 (见「机械核验」) | yaml TASK-002/004/007/008/010/016/017 verification; tasks.md flag 行补注 |
| af9f0c47 | A5 | minor | closed (三份统一, 方案 C3) — 版本档阻塞语义统一为「未裁 ⇒ 不开工, status 仍 `pending`, 不用 `blocked`」 | yaml TASK-021 notes; tasks.md `:7` |
| 98fdff37 | A5 | major | closed by 主控 (C11, proposal `:616` 已改) — 本席不动 proposal.md | — |
| C1 (统一) | 主控 | — | closed — 同文件串行 + RED 先于 GREEN + 前置断言在上游 (本 Spec 适用项: TASK-007←006, TASK-016→017) ; 程序化验 (a)(b)(c)(d) PASS + 坏实现两变体 (删边 / 同文件标并行) 均 FAIL | 见「机械核验」 |
| C9 (统一) | 主控 | — | closed — 同 df090b25 | 同上 |
| C4 / C5 / C7 (统一) | 主控 | — | closed — 同 A1 c23f47ce / 6698004d+35dad35d / 96ecdeb4 | 同上 |
| Minors「task_group 形态」 | 主控 | — | 不动 (方案: 三份内部各自一致即可; 本文件 `TG-n`) | — |

**方案与文件实况的出入 (本席不自行偏离, 报主控)**: (1) 方案 C7 写「模板 + spec-drafter hunk A, 即 TASK-013/014 一类」, 但 placeholder 串的两个写入宿主按 finding 96ecdeb4 与 yaml 实况是 **TASK-013 (模板) + TASK-015 (hunk B 预览骨架)**; hunk A (TASK-014) 只写不带花括号的写法 `<org>/<repo>#<n>`, 不写占位串 ⇒ 本席落在 013/015。(2) 方案 C4 只点 yaml `:268` / `:526`, finding 处方另点 tasks.md `:57` / `:129` 同一断言 ⇒ 本席一并改, 否则双层自相矛盾。(3) 方案 C1 规则 1 以「deliverables 含同一路径」为判据, `aria-plugin-benchmarks/ab-results/` 是目录路径且被 TASK-016/017/018/019 四条共列 ⇒ 规则把 TASK-019 (substitute 留痕) 也拉进 018 (#117 评论) 之后; 语义上两者同写同一 `RESULT.md`「逐 hunk 处置表」, 串行无害, 但 019 因此要等 #117 评论落地。

## 机械核验 (R1/C1 依赖不变量 + 覆盖表 token, 2026-08-30)

> 脚本 (`check_c1.py`, 在主仓根执行; exit 0 = PASS)。断言: (a) 任意两任务 deliverables 交集非空 ⇒ 后者依赖前者 (直接或传递); (b) 无环 / 无悬空; (c) 测试任务 (TG-1 或 title 含 测试/RED/单测/夹具) 不依赖任何 GREEN (非测试且有 deliverables 的任务); (d) `execution_order` 任何并行标记内无同文件对, 且无未限定的「并行 / parallelizable」字样; 附 parent 1:1 与 checkbox 对齐、覆盖表 (SC, TASK) ⇒ verification 含 SC token、flag 映射行 ⇒ 落点含 flag 字面。**坏实现负控**: 删 TASK-002 边 ⇒ (a) 报 4 对缺边 FAIL; `execution_order` 把 TASK-001/002 标 parallelizable ⇒ (d) 报同文件并行 FAIL (memory `check-runs-at-baseline-first`)。

```python
#!/usr/bin/env python3
"""R1/C1 机械核验 — linked-issue-field-availability/detailed-tasks.yaml 依赖不变量 (a)(b)(c)(d) + parent 1:1 + 覆盖表 token。
用法: cd /home/dev/Aria && python3 check_c1.py   (exit 0 = 全部 PASS)"""
import itertools, re, sys, yaml
D = "openspec/changes/linked-issue-field-availability/"
d = yaml.safe_load(open(D + "detailed-tasks.yaml", encoding="utf-8"))
T = {t["id"]: t for t in d["tasks"]}; order = list(T)
deps = {i: list(t.get("dependencies") or []) for i, t in T.items()}
files = {i: set(t.get("deliverables") or []) for i, t in T.items()}
def anc(i, seen=None):
    seen = set() if seen is None else seen
    for j in deps[i]:
        if j not in seen: seen.add(j); anc(j, seen)
    return seen
A = {i: anc(i) for i in T}
# (a) 同文件对 ⇒ 后者依赖前者 (直接或传递)
pairs = [(a, b, sorted(files[a] & files[b])) for a, b in itertools.combinations(order, 2) if files[a] & files[b]]
missing = [(a, b) for a, b, _ in pairs if a not in A[b]]
# (b) 无环 / 无悬空
def cycle():
    col = {i: 0 for i in T}
    def dfs(u):
        col[u] = 1
        for v in deps[u]:
            if v not in T: return f"dangling {u}->{v}"
            if col[v] == 1: return f"cycle {u}->{v}"
            if col[v] == 0 and (r := dfs(v)): return r
        col[u] = 2
    return next((r for i in T if col[i] == 0 and (r := dfs(i))), None)
cyc = cycle()
# (c) 测试任务 (TG-1 或 title 含 测试/RED/单测/夹具) 不依赖任何 GREEN (非测试且有 deliverables 的实现/文本任务)
kw = re.compile(r"测试|RED|单测|夹具")
tests = [i for i, t in T.items() if t.get("task_group") == "TG-1" or kw.search(t["title"])]
green = {i for i in T if i not in tests and files[i]}
bad_c = [(i, sorted(A[i] & green)) for i in tests if A[i] & green]
# (d) execution_order 任何并行标记 (parallelizable 列表 / {A, B} / A ‖ B) 内无同文件对
eo = d.get("execution_order", {}); groups = []
for v in eo.values():
    if not isinstance(v, dict): continue
    if isinstance(v.get("parallelizable"), list): groups.append(list(v["parallelizable"]))
    for s in v.values():
        if isinstance(s, str):
            groups += [re.findall(r"TASK-\d{3}", g) for g in re.findall(r"\{([^}]*)\}", s)]
            groups += [list(m) for m in re.findall(r"(TASK-\d{3})\s*‖\s*(TASK-\d{3})", s)]
bad_d = [(a, b) for g in groups for a, b in itertools.combinations(g, 2) if files[a] & files[b]]
eo_txt = yaml.safe_dump(eo, allow_unicode=True)
same_file_ids = {x for p in pairs for x in p[:2]}
bad_word = [ln.strip() for ln in eo_txt.splitlines() if re.search(r"并行|parallelizable", ln) and "不同文件" not in ln and "同文件" not in ln and "串行" not in ln]
# parent 1:1 + tasks.md checkbox
md = open(D + "tasks.md", encoding="utf-8").read()
parents = [t["parent"] for t in T.values()]
boxes = re.findall(r"^- \[[ x]\] (\d+\.\d+) ", md, re.M)
p11 = len(parents) == len(set(parents)) == len(boxes) and set(parents) == set(boxes)
# 覆盖表 (SC, TASK) ⇒ TASK 块含该 SC token (含 SC-a~b 区间展开); flag 映射行 ⇒ 落点任务块含 flag 字面
def block(i):
    t = T[i]; return " ".join([t["title"], *(t.get("verification") or []), *(t.get("deliverables") or []), t.get("notes", "") or ""])
def has_sc(i, sc):
    b = block(i); n = re.fullmatch(r"SC-(\d+)([a-z]?)", sc)
    num, suf = int(n.group(1)), n.group(2)
    if suf: return sc in b
    if re.search(rf"\bSC-{num}\b(?![a-z])", b): return True
    for lo, hi in re.findall(r"SC-(\d+)~(\d+)", b):
        if int(lo) <= num <= int(hi): return True
    return bool(re.search(rf"\bSC-\d+(?:/\d+)*/{num}\b", b))
p2id = {t["parent"]: i for i, t in T.items()}
cov = []
sec = md.split("## SC → TASK 覆盖表")[1].split("## Impact 表")[0]
for row in re.findall(r"^\| (SC-\d+[a-z]?) \|[^|]*\|([^|]*)\|([^|]*)\|", sec, re.M):
    sc, red, grn = row
    ids = set(re.findall(r"TASK-\d{3}", red + grn)) | {p2id[p] for p in re.findall(r"\b(\d\.\d)\b", red + grn) if p in p2id}
    cov += [(sc, i, has_sc(i, sc)) for i in sorted(ids)]
cov_bad = [(sc, i) for sc, i, ok in cov if not ok]
flag_line = re.search(r"\*\*每个 `--flag` 的落点\*\*: (.*)", md).group(1)
flags = []
for seg in re.split(r";\s*", flag_line):
    m = re.match(r"`(--[a-z-]+)`(?: / `[A-Z_]+`)? → (.*)", seg.strip())
    if not m: continue
    flag = m.group(1)
    for p in re.findall(r"\b(\d\.\d)\b", m.group(2)):
        i = p2id[p]; flags.append((flag, i, flag in block(i) or (flag == "--no-push" and "ARIA_COORDINATION_NO_PUSH" in block(i))))
flag_bad = [(f, i) for f, i, ok in flags if not ok]
print(f"tasks={len(T)}  同文件对={len(pairs)}  (a)缺边={missing}  (b)环/悬空={cyc}")
for a, b, s in pairs: print(f"   {a} -> {b}  {s}  edge={'ok' if a in A[b] else 'MISSING'}")
print(f"(c)测试任务={tests}  违反={bad_c}")
print(f"(d)并行组={groups}  同文件并行={bad_d}  可疑并行字样={bad_word}")
print(f"parent 1:1 与 tasks.md checkbox 对齐={p11} ({len(parents)} parent / {len(boxes)} checkbox)")
print(f"覆盖表对数={len(cov)}  缺 token={cov_bad}")
print(f"flag 映射={len(flags)} 对  缺字面={flag_bad}")
ok = not missing and not cyc and not bad_c and not bad_d and not bad_word and p11 and not cov_bad and not flag_bad
print("RESULT:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
```

输出 (2026-08-30, 对本文件与 detailed-tasks.yaml 现状):

```
tasks=25  同文件对=23  (a)缺边=[]  (b)环/悬空=None
   TASK-001 -> TASK-002  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-001 -> TASK-003  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-001 -> TASK-004  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-001 -> TASK-005  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-001 -> TASK-006  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-002 -> TASK-003  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-002 -> TASK-004  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-002 -> TASK-005  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-002 -> TASK-006  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-003 -> TASK-004  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-003 -> TASK-005  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-003 -> TASK-006  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-004 -> TASK-005  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-004 -> TASK-006  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-005 -> TASK-006  ['aria/skills/state-scanner/tests/test_linked_issue_field.py']  edge=ok
   TASK-008 -> TASK-009  ['aria/skills/state-scanner/scripts/linked_issue_field_probe.py']  edge=ok
   TASK-014 -> TASK-015  ['aria/skills/spec-drafter/SKILL.md']  edge=ok
   TASK-016 -> TASK-017  ['aria-plugin-benchmarks/ab-results/', 'aria-plugin-benchmarks/ab-suite/spec-drafter.json']  edge=ok
   TASK-016 -> TASK-018  ['aria-plugin-benchmarks/ab-results/']  edge=ok
   TASK-016 -> TASK-019  ['aria-plugin-benchmarks/ab-results/']  edge=ok
   TASK-017 -> TASK-018  ['aria-plugin-benchmarks/ab-results/']  edge=ok
   TASK-017 -> TASK-019  ['aria-plugin-benchmarks/ab-results/']  edge=ok
   TASK-018 -> TASK-019  ['aria-plugin-benchmarks/ab-results/']  edge=ok
(c)测试任务=['TASK-001', 'TASK-002', 'TASK-003', 'TASK-004', 'TASK-005', 'TASK-006']  违反=[]
(d)并行组=[['TASK-022', 'TASK-023']]  同文件并行=[]  可疑并行字样=[]
parent 1:1 与 tasks.md checkbox 对齐=True (25 parent / 25 checkbox)
覆盖表对数=28  缺 token=[]
flag 映射=12 对  缺字面=[]
RESULT: PASS
```
