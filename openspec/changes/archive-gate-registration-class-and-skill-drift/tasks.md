# Tasks — openspec-archive 文档/实现漂移收口

> **Change ID**: `archive-gate-registration-class-and-skill-drift` | **Level**: 3
> **Linked Issue**: `10CG/aria-plugin#186` | **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2`
> **post_spec**: R1→R5 已跑满 (`max_rounds=5`)。R5 = PASS_WITH_WARNINGS, **converged=false** (未达全票 PASS) ⇒ **该事实须原样写进 handoff 请 owner 复议**, 不得自行当作已收敛。
> **rule6_note**: openspec-archive 侧**照跑 AB** (B3 改 frontmatter `description` ⇒ SOT §2 附加约束「description 变动 ⇒ 一律第二行」); phase-d-closer 与 state-scanner 两侧走 **substitute** (SOT §2 第一行, 事实性同步 / 纯新增脚本且 `description` 零变动)。跨 Skill 作用域歧义 ⇒ **SC-11 阻塞 C.2**, 见下 E-0。

---

## Phase A.3 — Agent 分配

| Task Group | 主责 | 理由 |
|---|---|---|
| TG-B SKILL.md / README 收口 | `aria:knowledge-manager` | 文档与实现一致性、指令面措辞 |
| TG-C 三个脚本 + 测试 | `aria:qa-engineer` | 三态/五态可证伪性是其专长 |
| TG-D 开单 | 主控 | 对外动作不外派 |
| TG-E AB + 发版 + 集成 | 主控 | git / 发版 / 闸门不外派 (memory `workflow-file-domain`: subagent 不 commit) |

**并行性**: TG-B (两个 SKILL.md + 两份 README) 与 TG-C (三个新脚本 + 新 tests 目录) 文件域 **disjoint**, 可并行。
TG-C 的 C1 三态目标态依赖 TG-B 的 B1 落地 ⇒ C1 的目标态验证排在 B1 之后。

---

## TG-B — CLI 漂移类级收口 (20 行, 两个 SKILL.md + 两份 README)

> **通用 post-condition**: 每条改写后, 该行**必须不再命中 SC-1 pattern**。落盘前逐条自测。
> ⛔ **禁全局 `sed`** (`:275` 的 `§Step2 warn_overlay` 是正确交叉引用) · ⛔ **不重编 Step 编号** (Step 7 被 `spec_complete.py:1251` 引用)

### 有完整字面目标的 (照抄即可验收)

- [ ] **B-1** `openspec-archive/SKILL.md:317` `Step2` → `Step 7`
- [ ] **B-4** `:17` → `> **历史**: 2026-02-08 - 初始版本，修复归档目录落点错误 (彼时经由外部工具链, 现已改为 git mv)` (已实测零命中)
- [ ] **B-7** `:247` → `Step 3 - 执行归档 (git mv):` / `:248` → `  命令: git mv openspec/changes/{change_name} openspec/archive/{YYYY-MM-DD}-{change_name}` / `:249` → `  等待: git mv 返回`
- [ ] **B-8a** `:251-257` 整块 → Step 4 三行断言 (字面见 proposal B8)
- [ ] **B-8b** `:259-261` 整块 → `Step 5 - (已并入 Step 3: git mv 使源目录必然消失)`, **其下无正文**
- [ ] **B-10** 示例 1 四行 → 字面见 proposal SC-3(c)
- [ ] **B-15** `phase-d-closer/SKILL.md:41` → 字面见 proposal B15
- [ ] **B-16** `aria/README.md:85` → `- openspec-archive — Archive completed OpenSpec changes to openspec/archive/ with post-move location checks`
- [ ] **B-17** `aria/README.zh.md:85` → `- openspec-archive — 归档已完成的 OpenSpec 变更到 openspec/archive/ 并做落点校验`

### 只给方向的 (靠 post-condition 兜底, 落盘前逐条自测 pattern)

- [ ] **B-2** `:318` 替换文案 → 可验证约束 (必须含 7-40 位十六进制 SHA) + 写明调用 C2。**硬约束: 不得以「填入」二字结尾** (否则破坏 C1 锚点唯一性)
- [ ] **B-3** `:4` frontmatter `description` 删「自动修正 CLI bug」
- [ ] **B-5** `:40` + `:41` 核心功能表**两行的两个单元格全部重写**
- [ ] **B-6** `:56`「本 Skill 会自动修正此问题」→ 对采用者的条件表述
- [ ] **B-9** `:87` 退役 `keep_changes_copy`, 移入**新增小节 `## 已退役配置项`**
- [ ] **B-11** `:588` 错误表 CLI 行 → `git mv` 失败三分支
- [ ] **B-12** `:607` 流程图行
- [ ] **B-13** `:47-58` 已知 Bug 节保留 + 时限限定行插在**标题行之后、`**问题**:` 行之前**
- [ ] **B-14** `:622` 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/`

### TG-B 验收

- [ ] **B-V1** SC-1 机械判据: 四文件区段外命中 == **0** (基线 15)
- [ ] **B-V2** SC-1b **语义复核** (非机械, 独立勾选): 对着 §Why 反转 1 重读 B-3/B-5/B-6/B-15/B-16/B-17 改后原文, 断言**不再承诺自动处理 CLI 问题**
- [ ] **B-V3** SC-2: `grep -c 'Step2' openspec-archive/SKILL.md` == **1** 且唯一命中在 `:275`
- [ ] **B-V4** SC-3: Step 5 正文 **0 行** / Step 4 正文 **3 行** / 示例四行逐行等于目标文本
- [ ] **B-V5** SC-4: `keep_changes_copy` 命中全落 `## 已退役配置项` 内
- [ ] **B-V6** Rule #3: `aria/skills/openspec-archive/CHANGELOG.md` `[Unreleased]` 加条目

---

## TG-C — 三个脚本 + 测试

- [ ] **C-1** `skill_md_literal_sync_probe.py` → `aria/skills/state-scanner/scripts/` (含 `REQUIRED_STEP = "Step 7"` 第三条断言)
- [ ] **C-2** 注册 C-1 进 `.aria/state-checks.yaml` (`severity: warning`, 参照 `issue-cache-freshness` 体例)
- [ ] **C-3** **五态实跑留证**: 基线 FAIL rc1 (打印两侧原文) / 目标 PASS rc0 / 插件源码不可见 SKIP rc0+`##SKIP##` / 锚点提取数≠1 FAIL rc1 / **坏实现「两侧同改回 Step2」FAIL rc1**
- [ ] **C-4** **B-1 落地后重跑 C-1 锚点唯一性** (SKILL.md 侧命中数须仍为 1) —— B-2 改 `:318` 会威胁它
- [ ] **C-5** `archive_tracker_verify.py` → **新建** `aria/skills/openspec-archive/scripts/`
- [ ] **C-6** 单测 → **新建** `aria/skills/openspec-archive/tests/`, **必须带 `conftest.py`** (否则 `run_all_tests.sh` 走 `unittest discover` 收集 0 个并报 `OK (0 tests)` 假绿, 见 `10CG/aria-plugin#187`; 可照抄 `phase-d-closer/tests/conftest.py` 的做法)
- [ ] **C-7** 夹具 → `tests/fixtures/`, **冻结快照**不实时抓 API; 每份注明来源 `10CG/Aria#<n>` 与抓取时刻; **含合成 `synth-short`** (真语料证不了长度下限)
- [ ] **C-8** C2 五态实跑: `10CG/Aria#201` rc0 / `#185` rc1 NO_SHA / `#186` rc1 MISSING / `synth-short` rc1 / body 取不到 rc2
- [ ] **C-9** `check_bare_issue_refs.py` → `aria/skills/state-scanner/scripts/` (SC-12)
- [ ] **C-10** C-9 三态留证 (目标态 rc0 / 正控 `d81873b^` rc1 / 坏实现裸 grep 任一版报非零 ⇒ 判无效)。**具体命中数只贴脚本产出, 不写进 proposal 正文**
- [ ] **C-V1** `bash aria/skills/run_all_tests.sh` 里 `openspec-archive` 那行测试数 **非 0**
- [ ] **C-V2** 全套件 ≥ **2122** 且 0 FAIL; state-scanner `run_tests.py` ≥ **1575 / OK**

---

## TG-D — 开单 (六条待开 + 三条已开)

- [ ] **D-1** AB 套件缺 Step 7 / D auto-issue 维度 → `10CG/aria-plugin` (Rule #6 SOT §3 第 3 条强制)
- [ ] **D-2** openspec-archive evals 三处缺 `YYYY-MM-DD-` 前缀 + `cli_wrong_path` 与 SOT 矛盾 + 断言首句零判别力 → `10CG/aria-plugin`
- [ ] **D-3** `unverified_claims`/`unverified_ack` frontmatter 只写不读 → `10CG/aria-plugin`
- [ ] **D-4** `standards/openspec/AGENTS.md:57` 悬空脚本 → `10CG/aria-standards`
- [ ] **D-5** `spec-drafter/SKILL.md:192 :507 :510` 指示运行未安装的 `openspec validate` → `10CG/aria-plugin`
- [ ] **D-6** ⏰ `check-m6-e2e-acceptance` 判 dead, 引信行 `aria-2.0-m6-e2e-resilience/tasks.md:353` → `10CG/Aria`。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免
- [x] **D-7** `10CG/aria-plugin#187` (harness 假绿; 已最小止血)
- [x] **D-8** `10CG/aria-plugin#188` (Part A 拆出件)
- [x] **D-9** `10CG/aria-plugin#189` (Step 7 无调用宿主)
- [ ] **D-V1** 六条新单全部**回读核验** (title + 正文首行), issue 号**带仓限定**记回本文件
- [ ] **D-V2** 跑 `check_bare_issue_refs.py` 对 proposal.md 与本文件, rc == 0

---

## TG-E — Rule #6 AB + 发版 + 集成

- [ ] **E-0** ⛔ **SC-11 阻塞项**: 把「SOT §1『整个变更』跨多 Skill 时的作用域」写进 handoff 请 owner 裁 (a) ratify v1.69.1 形状为成文 lane / (b) 另裁。**取得答复前不得进入 C.2**
- [ ] **E-1** AB 前置**已核**: `ab-suite/openspec-archive.json` 两个选中 eval 用合成路径 `/workspace/my-project`, 不触真仓、不走 Step 7 ⇒ **不需要 `ARIA_COORDINATION_NO_PUSH=1` 会话级前置**
- [ ] **E-2** 跑 openspec-archive AB (`/skill-creator`; runner 在 `claude-plugins-official/skill-creator/unknown/skills/skill-creator/`)。两臂 = **v_new vs v_old** (SOT §6: with/without 那列因 CLAUDE.md 污染不可用)
- [ ] **E-3** 结果存 `ab-results/2026-09-XX-v1.72.0-archive-skill-drift/RESULT.md`; **须显式记录本次 AB 对本改动的区分力评估** (预期零, 见 proposal R1V-6 登记); `WITHOUT_BETTER` 逐条解释或回退
- [ ] **E-4** 版本 bump `aria/.claude-plugin/plugin.json` → **1.72.0** (SOT = 该文件, 其余派生)
- [ ] **E-5** 23 处版本串同步 (aria 子模块 7 + 主仓 16), **逐文件 `grep -c` 实测并把 13 行计数贴进本文件** —— 六个 custom check 只覆盖约 6/23, 不能只靠它们判绿
- [ ] **E-6** 六个版本类 custom check 全绿
- [ ] **E-7** C.1 提交 (Conventional Commits) → aria 子模块**本地 merge** 到 master + 双推 (⛔ 禁 Forgejo 服务端合并, 硬约束 1)
- [ ] **E-8** 主仓 gitlink bump; **SC-9 两条断言**: (a) `git ls-tree HEAD aria` == `git -C aria rev-parse HEAD`; (b) 子模块 HEAD == `origin/master`
- [ ] **E-9** 主仓 PR → **Rule #8 pre-merge gate** (phase-c-integrator C.2.4) → 合并 (主仓例外可走 Forgejo merge)
- [ ] **E-10** **逐 remote `ls-remote` 独立核验**两仓 (`10CG/Aria` + `10CG/aria-plugin`), 不信 push 回执 (硬约束 2); gitlink orphan 守卫
- [ ] **E-11** D.1 进度 → D.2 归档 → D.2b release claim → D.3 handoff
- [ ] **E-V1** handoff 须点名的四项: (1) SC-11 的 owner 裁定; (2) B-9 退役 `keep_changes_copy` 是**声明接口移除**请复议; (3) **post_spec `converged=false`, max_rounds 耗尽**这一事实; (4) D-6 是别的 track 的定时风险

---

## 已知风险

1. **自证循环**: D.2 归档要走的正是本 Spec 改的那条路径的邻近面。独立证据: 改前必红测试 (C-3/C-8/C-10 三态) + SC-1 基线 15 → 0 的对跑。
2. **AB 零区分力**: 已在 proposal 登记, RESULT.md 须显式写明, 不把「跑过了」当「验过了」。
3. **`aria-orchestrator` 指针全程 dirty** (他轨 `feature/m6-cost-model-telemetry`) —— 本 Spec 全程不动它, C.1 提交时须核 `git status` 确认未卷入。
