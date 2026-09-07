# Tasks — openspec-archive 文档/实现漂移收口

> **Change ID**: `archive-gate-registration-class-and-skill-drift` | **Level**: 3
> **Linked Issue**: `10CG/aria-plugin#186` | **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2`
> **post_spec**: R1→R5 跑满 (`max_rounds=5`)。R5 = PASS_WITH_WARNINGS, **converged=false** ⇒ 该事实须原样写进 handoff 请 owner 复议, 不得自行当作已收敛。
> **post_planning**: R1 已跑 (4 席 + 4 反驳席), 本文为 R1 修订版。
> **rule6_note**: openspec-archive 侧**照跑 AB**; phase-d-closer 与 state-scanner 两侧 **substitute**。跨 Skill 作用域歧义 ⇒ **SC-11 阻塞 C.2**, 见 E-0。

---

## Phase A.3 — Agent 分配与顺序

| Task Group | 主责 | 理由 |
|---|---|---|
| TG-B SKILL.md / README 收口 | `aria:knowledge-manager` | 文档与实现一致性、指令面措辞 |
| TG-C 三个脚本 + 测试 | `aria:qa-engineer` | 三态/五态可证伪性是其专长 |
| TG-D 开单 | 主控 | 对外动作不外派 |
| TG-E AB + 发版 + 集成 | 主控 | git / 发版 / 闸门不外派 (memory `workflow-file-domain`: **subagent 一律不 commit, 主控统一提交**) |

### 并行性与顺序依赖 (post_planning R1 订正)

**TG-B 与 TG-C 的文件域不是完全 disjoint** —— C-3 的**基线态**要**读** TG-B 正在改的 `openspec-archive/SKILL.md`。约束:

- **C-3 基线态必须在 B-1/B-2 落盘之前跑**, 否则基线已被改掉, 「基线 FAIL」不可复现。
- C-3 的**其余四态**用 `CLAUDE_PLUGIN_ROOT` 指向 scratchpad 夹具跑, **不写仓内任何文件** (Phase A.1 的五态就是这么跑的; 夹具见 C-3 说明)。
- **C-4 必须排在 B-2 之后** (不是 B-1 —— 见 C-4 说明)。
- 其余 TG-B / TG-C 任务文件域 disjoint, 可并行。

---

## TG-B — CLI 漂移类级收口 (**18 条**, 两个 SKILL.md + 两份 README)

> ⚠️ **post_planning R2 Critical (F-1) 订正**: R1 修订 (`240ea4c`) **静默删除了 B-14**, 同时把标题计数从「20 行」改成「17 条」⇒ 删完自洽, **数数核不出来**。而 proposal `:67` 仍在册、`:159` 的 Rule #6 范围写的是「B1-B14」, 且 SC-1 的 pattern 对 `:622` **命中 0** ⇒ **零验收能发现**。已补回并加专属验收 B-V8。

> **通用 post-condition**: 每条改写后该行**不再命中 SC-1 pattern**。
> ⚠️ **B-2 例外**: `:317`/`:318` 本来就不命中该 pattern, 故 post-condition 对 B-2 是**空检查**, 它另有专属验收 (见 B-V7)。
> ⛔ **禁全局 `sed`** (`:275` 的 `§Step2 warn_overlay` 是正确交叉引用) · ⛔ **不重编 Step 编号** (Step 7 被 `spec_complete.py:1251` 引用)

### 有完整字面目标 (照抄即验收)

- [ ] **B-1** `openspec-archive/SKILL.md:317` `Step2` → `Step 7`
- [ ] **B-4** `:17` → `> **历史**: 2026-02-08 - 初始版本，修复归档目录落点错误 (彼时经由外部工具链, 现已改为 git mv)`
- [ ] **B-7** `:247` → `Step 3 - 执行归档 (git mv):` / `:248` → `  命令: git mv openspec/changes/{change_name} openspec/archive/{YYYY-MM-DD}-{change_name}` / `:249` → `  等待: git mv 返回`
- [ ] **B-8a** `:251-257` 整块 → Step 4 三行断言 (字面见 proposal B8)
- [ ] **B-8b** `:259-261` 整块 → `Step 5 - (已并入 Step 3: git mv 使源目录必然消失)`, **其下无正文**
- [ ] **B-10** 示例 1 四行 → 字面见 proposal SC-3(c)
- [ ] **B-15** `phase-d-closer/SKILL.md:41` → 字面见 proposal B15
- [ ] **B-16** `aria/README.md:85` → `- openspec-archive — Archive completed OpenSpec changes to openspec/archive/ with post-move location checks`
- [ ] **B-14** `openspec-archive/SKILL.md:622` 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` (**R2 补回**)
- [ ] **B-17** `aria/README.zh.md:85` → `- openspec-archive — 归档已完成的 OpenSpec 变更到 openspec/archive/ 并做落点校验`

### 只给方向 (落盘前逐条自测 pattern)

- [ ] **B-2** `:318` 替换文案 → 可验证约束 (必须含 7-40 位十六进制 SHA) + 写明调用 C2。**硬约束: 不得以「填入」二字结尾**
- [ ] **B-3** `:4` frontmatter `description` 删「自动修正 CLI bug」
- [ ] **B-5** `:40` + `:41` 核心功能表**两行的两个单元格全部重写** (`:40` 执行归档 → `git mv …`; `:41` 自动修正 → 位置校验)
- [ ] **B-6** `:56`「本 Skill 会自动修正此问题」→ 对采用者的条件表述
- [ ] **B-9** `:87` 退役 `keep_changes_copy`, 移入**新增小节 `## 已退役配置项`** (放在 `## 错误处理` 之前; 格式: 标题 + 一行说明 + 一行退役理由)
- [ ] **B-11** `:588` 错误表 CLI 行 → `git mv` 失败三分支 (目标已存在 → BLOCKED-already-archived / 源未跟踪 → 先 `git add` / 其余按 stderr 原文)
- [ ] **B-12** `:607` 流程图行 (「Step 3-6 执行归档 / 修正 CLI bug / 验证结果」→ 去掉「修正 CLI bug」)
- [ ] **B-13** `:47-58` 已知 Bug 节保留 + 时限限定行插在**标题行之后、`**问题**:` 行之前**; 该行须含「本仓从未安装该 CLI」与「归档走 git mv」两个事实

### TG-B 验收

- [ ] **B-V1a** SC-1 前半: 四文件**区段外命中 == 0** (基线 15)
- [ ] **B-V1b** SC-1 后半 (**post_planning R1 补**): **区段内命中集合按内容钉死** —— 恰为 (a) `## ⚠️ 已知 Bug` 标题行 / (b) `**问题**: …CLI 命令有 bug…` 行 / (c) CHANGELOG 表 `1.0.0 … 初始版本，实现 CLI bug 自动修正` 行 / (d) B-13 新插的时限限定行 (若命中)。**其余一律不允许** —— 缺这半会让 B-6 的守卫消失
- [ ] **B-V2** SC-1b **语义复核** (非机械, 独立勾选): 对着 §Why 反转 1 重读 B-3/B-5/B-6/B-15/B-16/B-17 改后原文, 断言不再承诺自动处理 CLI 问题。**须把六条改后原文逐条抄进本文件 + 一句理由**, 不接受「已复核」四字带过
- [ ] **B-V3** SC-2: `grep -n 'Step2' openspec-archive/SKILL.md` 命中 **1** 处, 且该行**内容**为 `# "全部 unverified_claims" (无论 §Step2 warn_overlay 是否写了 --ack-unverified) 而来;` (**按内容不按行号** —— 前面几个 B 任务会移动行号)
- [ ] **B-V4** SC-3: Step 5 正文 **0 行** / Step 4 正文 **3 行** / 示例四行逐行等于目标文本
- [ ] **B-V5** SC-4: `keep_changes_copy` 命中全落 `## 已退役配置项` 内
- [ ] **B-V6** Rule #3: `aria/skills/openspec-archive/CHANGELOG.md` `[Unreleased]` 加条目, **且该条目须点名本次改的 Step 3/4/5 与退役的 `keep_changes_copy`** (防恒绿)
- [ ] **B-V8** (**R2 补**, B-14 专属 —— SC-1 的 pattern 对 `:622` 结构上命中 0, 抓不到它): `grep -n 'aria-archive-gate-runtime-reality' aria/skills/openspec-archive/SKILL.md` 的命中行须含 `openspec/archive/2026-07-05-` 前缀; 且 `openspec/changes/aria-archive-gate-runtime-reality` 不存在。**基线该断言为红** (现文本指向 `openspec/changes/...`, 而该目录已不存在)
- [ ] **B-V7** B-2 专属验收 (**post_planning R1 补**, 因通用 post-condition 对它是空检查): `:318` 改后 (a) 不以「填入」二字结尾; (b) 含「7-40 位十六进制」字样; (c) 含对 C2 脚本的调用行

---

## TG-C — 三个脚本 + 测试

- [ ] **C-1** `skill_md_literal_sync_probe.py` → `aria/skills/state-scanner/scripts/`。**须含三条判断**: (a) 两侧锚点各提取 1 处否则 rc 2 fail-CLOSED; (b) 两侧逐字相等; (c) **命中串必须含 `Step 7`** (挡「两侧同改回 Step2」)
- [ ] **C-2** 注册 C-1 进 `.aria/state-checks.yaml` (`severity: warning`, 参照 `issue-cache-freshness` 体例)
- [ ] **C-3** **五态实跑留证**。⚠️ **基线态必须在 B-1/B-2 之前跑**; 其余四态用 `CLAUDE_PLUGIN_ROOT` 指向 scratchpad 夹具, **不写仓内任何文件**:
  - 基线 (当前仓, 两侧不等) → FAIL rc1 且打印两侧原文
  - 目标 (夹具: SKILL.md 已改 `Step 7`) → PASS rc0
  - 插件源码不可见 (`CLAUDE_PLUGIN_ROOT=/nonexistent`) → SKIP rc0 + `##SKIP##`
  - 锚点提取数≠1 (夹具: 两个空文件) → FAIL rc1
  - **坏实现「两侧同改回 Step2」** (夹具: SKILL.md 原样 + spec_complete.py 副本改成 `Step2`) → FAIL rc1
- [ ] **C-4** ⚠️ **B-2 落地后**立即重跑 C-1 锚点唯一性 (SKILL.md 侧命中数须仍为 1)。**不是 B-1** —— B-1 只改 `:317` 内的 `Step2`, 不动 `:318`, 锚点数恒为 1 ⇒ 在 B-1 后跑是恒绿; 唯一能把锚点数推到 2 的是 B-2 对 `:318` 的改写
- [ ] **C-5** `archive_tracker_verify.py` → **新建** `aria/skills/openspec-archive/scripts/`
- [ ] **C-6** 单测 → **新建** `aria/skills/openspec-archive/tests/`, **必须带 `conftest.py`**。⚠️ **不是照抄 `phase-d-closer/tests/conftest.py` 的内容** (那份 docstring 逐句是 phase-d-closer 专属事实), 而是照抄它的**做法**: 写成**纯 docstring 零代码**的文件, 内容说明 (a) 它为什么存在 (触发 `is_pytest_suite()` 第一条判据); (b) 删掉它会退回 `OK (0 tests)` 的回归判据。**sys.path 由测试文件自己做** (照 `test_fetch_gate.py:17` 的 `sys.path.insert(0, parent.parent / "scripts")`)
- [ ] **C-7** 夹具 → `tests/fixtures/`, **冻结快照**。抓取命令: `forgejo GET /repos/10CG/Aria/issues/<n> | jq -r '.body' > fixtures/issue-<n>.md`, 对 `201` / `185` / `186` 各一份; 每份**首行加注释**记来源 `10CG/Aria#<n>` 与抓取 UTC 时刻。另建合成夹具 `synth-short.md` (回链行尾部含短十六进制 `abc`) —— 真语料证不了长度下限
- [ ] **C-8** C2 五态实跑: `#201` rc0 / `#185` rc1 NO_SHA / `#186` rc1 MISSING / `synth-short` rc1 / body 取不到 rc2
- [ ] **C-9** `check_bare_issue_refs.py` → `aria/skills/state-scanner/scripts/` (SC-12)
- [ ] **C-10** C-9 三态留证 (目标态 rc0 / 正控 `d81873b^` rc1 / 坏实现裸 grep 任一版报非零 ⇒ 判无效)。**具体命中数只贴脚本产出, 不写进 proposal 正文**
- [ ] **C-V1** `bash aria/skills/run_all_tests.sh` 里 `openspec-archive` 那行测试数 **非 0** (基线该行不存在 ⇒ 真红→绿)
- [ ] **C-V2** 全套件 ≥ **2122** 且 0 FAIL; state-scanner `run_tests.py` ≥ **1575 / OK**
- [ ] **C-V4** (**R2 补**, 对应已知风险 5): C-3 五态跑完后核 `git status --porcelain` 与 `git -C aria status --porcelain`, 确认 `spec_complete.py` **未被修改** (它是本 Spec 明文非目标)。若曾误改须 `git checkout` 还原并复核
- [ ] **C-V3** (**post_planning R1 补**) C-2 注册生效核验: 跑一次 `/state-scanner`, 确认 snapshot 的 `custom_checks.results` 里**出现** `skill-md-sha-backlink-literal-sync` 这一项且 status 非 `error` —— 否则「注册了但没被扫到」与 Part A 的零触达故事同构

---

## TG-D — 开单 (六条待开 + 三条已开)

- [ ] **D-1** AB 套件缺 Step 7 / D auto-issue 维度 → `10CG/aria-plugin`
- [ ] **D-2** openspec-archive evals 三处缺 `YYYY-MM-DD-` 前缀 + `cli_wrong_path` 与 SOT 矛盾 + 断言首句零判别力 → `10CG/aria-plugin`
- [ ] **D-3** `unverified_claims`/`unverified_ack` frontmatter 只写不读 → `10CG/aria-plugin`
- [ ] **D-4** `standards/openspec/AGENTS.md:57` 悬空脚本 → `10CG/aria-standards`
- [ ] **D-5** `spec-drafter/SKILL.md:192 :507 :510` 指示运行未安装的 `openspec validate` → `10CG/aria-plugin`
- [ ] **D-6** ⏰ `check-m6-e2e-acceptance` 判 dead, 引信行 `aria-2.0-m6-e2e-resilience/tasks.md:353` → `10CG/Aria`。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免
- [x] **D-7** `10CG/aria-plugin#187` · [x] **D-8** `10CG/aria-plugin#188` · [x] **D-9** `10CG/aria-plugin#189`
- [ ] **D-V1** 六条新单全部**回读核验** (title + 正文首行), issue 号**带仓限定**记回本文件
- [ ] **D-V2** 跑 `check_bare_issue_refs.py` 对 proposal.md 与本文件, rc == 0

---

## TG-E — Rule #6 AB + 发版 + 集成

- [ ] **E-0** ⛔ **SC-11 阻塞项**: 把「SOT §1『整个变更』跨多 Skill 时的作用域」写进 handoff 请 owner 裁 (a) ratify v1.69.1 形状为成文 lane / (b) 另裁。**取得答复前不得进入 C.2 —— 即不得执行 E-7a 起的任何步骤 (含 E-7a 的 fetch/断言前置)**。
  ⚠️ **卡住时怎么办** (**边界已并入上方主句; 本段只留 rationale** —— post_planning R3 Critical R3-C1: R2 只在此加脚注纠正范围却没回头改主句, 致同一任务两个边界, 而主句权重更高): E-0 不阻塞 TG-B/TG-C/TG-D 与 **E-1..E-6**; 它挡 **E-7a 起的全部步骤**。若 owner 长时间不答复, **停在 E-6c 之后**, 把已完成部分写进 handoff, **不合并也不推任何 remote**。
  ⚠️ **停在那里时 `plugin-cache-currency` 必然是红的** (E-6b) —— 这是**已知且已登记**的状态, **不得**为了「让它绿」而自行豁免或跳过 (那正是 R4 GOV 逐字点名过的自行豁免形状); handoff 须如实写明该 check 红及其原因。
  > **为什么范围要收到 E-6**: R1 版写「不阻塞 E-2..E-8」是错的 —— **E-7b 就是「子模块本地 merge + 双推」**, 它会在 owner 裁定前把 v1.72.0 (含 SC-11 正要问的 B-15 phase-d-closer 与 C-1/C-9 state-scanner 改动) **不可逆地发布到两个公共 remote**。proposal SC-11 明写「取得答复前不得进入 C.2」, 而**子模块合并推送就是 C.2 的一部分**, 不只是主仓 PR 合并。
  > R1 那条修复本身造了一个新的自行豁免 (memory `fix-recurs-in-fallback`: 修复类改动最易在自己新写的兜底路径重犯要治的病)。
- [ ] **E-0b** (**post_planning R1 补**) SC-11 若得 (b) 裁定: 补跑 `phase-d-closer` 与 `state-scanner` 两个 AB 套件, 结果同样存 `ab-results/`
- [ ] **E-1** AB 前置**已核**: `ab-suite/openspec-archive.json` 两个选中 eval 用合成路径 `/workspace/my-project`, 不触真仓、不走 Step 7 ⇒ **不需要 `ARIA_COORDINATION_NO_PUSH=1` 会话级前置**
- [ ] **E-2** 跑 openspec-archive AB (`/skill-creator`)。两臂 = **v_new vs v_old**。**隔离条款 (post_planning R1 补)**: 各臂输出写各自 `outputs/`, 不写仓内固定路径 (`10CG/aria-plugin#180`); AB 跑在真仓无沙箱 (memory `ab-harness-real-repo`)
- [ ] **E-3** 结果存 `ab-results/2026-09-XX-v1.72.0-archive-skill-drift/RESULT.md`; **须显式记录本次 AB 对本改动的区分力评估** (预期零); `WITHOUT_BETTER` 逐条解释或回退
- [ ] **E-4** 版本 bump `aria/.claude-plugin/plugin.json` → **1.72.0** (SOT = 该文件)
- [ ] **E-5** 版本串同步。⚠️ **append-only 豁免有两处, 不是一处** (post_planning R1 抓到第一处, **R3-M2 抓到我只修了实例没修类**):
  - `aria/CHANGELOG.md:13` `## [1.71.1] - 2026-09-06` —— 段标题, **不改**; 动作是在其**上方新增** `## [1.72.0]`
  - **`aria/VERSION:4`** `> **发布日期**: 2026-09-06  # patch: v1.71.1 …` —— **当期发布说明**, 其下已排着一串 `发布日期(旧)`; 发版时是**新增**一条并把这条降格成 `(旧)`, **不是改写它**。(同文件 `:3` 的 `> **版本**: 1.71.1` **要改**)
  ⇒ **要改的是 21 处 / 12 文件** (23 − CHANGELOG:13 − VERSION:4), 外加 CHANGELOG 与 VERSION 各**新增**一条。
  逐文件 `grep -c` 实测并把 **13 行**计数**全部**贴进本文件 (含上述两处标注「append-only, 不改」) —— proposal `:147` 要求「不留不对称缺口」
- [ ] **E-6a** **五个仓内 check 全绿**: `m6-version-badge-match` / `m6-claude-md-version` / `i18n-readme-translation-currency` / `main-project-version-consistency` / `plugin-version-arch-docs-match`。它们的输入全在仓内, E-5 落地后必然可绿
- [ ] **E-6b** ⚠️ **`plugin-cache-currency` 在 E-4 之后期望 STALE, 不是绿** (post_planning R3 R3-M1): 它比的是**运行时** `~/.claude/plugins/installed_plugins.json` 与 SOT `plugin.json`。E-4 一 bump 到 1.72.0 它立刻转红, 且**在 TG-E 的任何位置都转不绿** —— 转绿要 owner 终端跑 `/plugin marketplace update` + `/plugin update` + 重启 session (memory `session-level-precondition`: 会话内补不上)。
  **验收 = 贴出它的实跑输出**, 确认红的原因是「installed 落后 SOT」而非别的; **不得把它算进「全绿」**。
  ⚠️ 该例外**尚未成文**: 上一周期 (`docs/handoff/2026-09-06-session-close-v1.70.0-...`) 已把「SC-7 十三条全绿 + plugin-cache-currency 例外」上呈 owner, **写就时尚未裁定** ⇒ 按 memory `exact-exception-condition`「N 次非正式援引 ≠ 成文 lane」, **现在不能援引它当豁免**, 只能如实登记并在 handoff 再次点名
- [ ] **E-6c** ⚠️ 六个 check 合计只覆盖 23 处版本点里的约 6 处, **不能只靠它们判绿** (E-5 的逐文件实测是主判据)
- [ ] **E-7a** (**post_planning R1 补, memory `stale-local-main`**) 子模块 merge **前置**: `git -C aria fetch origin --prune && git -C aria fetch github --prune`; 断言 `local master == origin/master` (不等则先 FF)。**同一断言对主仓也要做** —— 本文件写就时主仓本地 master 实测**落后 origin/master 8 个 commit** (并发轨在飞)
- [ ] **E-7b** aria 子模块**本地** `git merge` feature → master + 双推 (⛔ 禁 Forgejo 服务端合并, 硬约束 1) + 逐 remote `ls-remote` 核验
- [ ] **E-8** 主仓 gitlink bump; **SC-9 两条断言**: (a) `git ls-tree HEAD aria` == `git -C aria rev-parse HEAD`; (b) 子模块 HEAD == `origin/master`
- [ ] **E-9** 主仓 PR → **Rule #8 pre-merge gate** → 合并 (主仓例外可走 Forgejo merge)。⚠️ **服务端合并后 GitHub 镜像不会自动拿到** (`10CG/Aria#165` 形状) ⇒ 必须本地 FF master + `git push github master`
- [ ] **E-10** **逐 remote `ls-remote` 独立核验**两仓, 不信 push 回执 (硬约束 2); gitlink orphan 守卫 (三个子模块 SHA 在两端均可达)
- [ ] **E-11** D.1 进度 → D.2 归档 → D.2b release claim → D.3 handoff
- [ ] **E-V1** handoff 须点名四项, **逐项在 handoff 里给可 grep 的锚点**: (1) `SC-11 owner 裁定`; (2) `keep_changes_copy 声明接口移除`; (3) `post_spec converged=false`; (4) `D-6 定时风险`。**验收 = 对 handoff 文件 grep 这四个字符串, 缺一即红** (防纯自证)

---

## 已知风险

1. **自证循环**: D.2 归档要走的正是本 Spec 改的那条路径的邻近面。独立证据: 改前必红测试 (C-3/C-8/C-10 三态) + SC-1 基线 15 → 0 的对跑。
2. **AB 零区分力**: 已在 proposal 登记, RESULT.md 须显式写明, 不把「跑过了」当「验过了」。
3. **`aria-orchestrator` 指针全程 dirty** (他轨 `feature/m6-cost-model-telemetry`) —— 本 Spec 全程不动它, C.1 提交时须核 `git status` 确认未卷入。
4. (**post_planning R1 补**) **并发轨在飞**: 主仓本地 master 写就时落后 origin/master **8 个 commit**, aria 子模块 `3a28339` **未推任何 remote**。每次实质 git 动作前必 fetch (memory `concurrent-duplicate-audit-fetch-before-start`)。
5. (**post_planning R1 补**) **负控夹具必须还原**: C-3 的坏实现态改的是 scratchpad 夹具而非仓内文件; 若执笔者图省事直接改仓内 `spec_complete.py`, **必须在跑完后 `git checkout` 还原并核 `git status`** —— 该文件是本 Spec 的明文非目标。
6. (**post_planning R1 补**) **服务端合并的 GitHub 补推**: 主仓走 Forgejo merge 后 GitHub 镜像落后一个 commit (本 session 在 PR `10CG/Aria#202` 上实测过一次), E-9 已含补推步骤。
