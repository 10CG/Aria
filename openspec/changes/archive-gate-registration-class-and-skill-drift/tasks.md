# Tasks — openspec-archive 文档/实现漂移收口

> **Change ID**: `archive-gate-registration-class-and-skill-drift` | **Level**: 3
> **Linked Issue**: `10CG/aria-plugin#186` | **Track ID**: `archive-gate-registration-class-and-skill-drift-023236f2`
> **post_spec**: R1→R5 跑满 (`max_rounds=5`)。R5 = PASS_WITH_WARNINGS, **converged=false** ⇒ 该事实须原样写进 handoff 请 owner 复议, 不得自行当作已收敛。
> **post_planning**: R1→R5 已跑 (`max_rounds=5` 用满), 本文为 **R5 修订版**。各轮权威记录见 `.aria/audit-reports/post_planning-R*-*-aggregated.md` 的 frontmatter。**R5 verdict = FAIL (3 席 FAIL), `converged=false`** —— 见 E-V1 的 handoff 点名义务。
> **rule6_note**: openspec-archive 侧**照跑 AB**; phase-d-closer 与 state-scanner 两侧 **substitute**。跨 Skill 作用域歧义 ⇒ **SC-11 阻塞 C.2**, 见 E-0。

---

## Phase A.3 — Agent 分配与顺序

| Task Group | 主责 | 理由 |
|---|---|---|
| TG-B SKILL.md / README 收口 | `aria:knowledge-manager` | 文档与实现一致性、指令面措辞 |
| TG-C 三个脚本 + 测试 | `aria:qa-engineer` | 多态 (三/四/五) 可证伪性是其专长 |
| TG-D 开单 | 主控 | 对外动作不外派 |
| TG-E AB + 发版 + 集成 | 主控 | git / 发版 / 闸门不外派 (memory `workflow-file-domain`: **subagent 一律不 commit, 主控统一提交**) |

### 并行性与顺序依赖 (post_planning R1 订正)

**TG-B 与 TG-C 的文件域不是完全 disjoint** —— C-3 的**基线态**要**读** TG-B 正在改的 `openspec-archive/SKILL.md`。约束:

- **C-3 基线态必须在 B-1/B-2 落盘之前跑**, 否则基线已被改掉, 「基线 FAIL」不可复现。
- C-3 的**其余三态**在 scratchpad 的**同构插件树**里跑, **不写仓内任何文件**。⛔ **不是设 `CLAUDE_PLUGIN_ROOT`** —— C-1 明令探针用 `parents[3]`, 该 env **在本设计下完全惰性** (post_planning R5 F1 实测: 设与不设的 ROOT/锚点数/输出/rc 逐字节相同)。正确做法见 C-3。
- **C-4 必须排在 B-2 之后** (不是 B-1 —— 见 C-4 说明)。
- **TG-C 与 TG-B 之间**文件域 disjoint, 可并行。
- ⛔ **但 TG-B 内部**不是 —— **12 条 B 任务用绝对行号打同一个 `openspec-archive/SKILL.md`** (`:4 :17 :40 :47 :56 :87 :247 :251 :259 :318 :588 :607`), 它们**互相移动对方的行号**, 必须**严格串行**。原文写「其余 TG-B / TG-C 任务文件域 disjoint, 可并行」是**错的** (**post_planning R5 完备性批评席 Critical**; proposal 自己在「Part B 自身会移动行号」处早就知道这件事, 但该洞见此前只被用来修验收项 B-V3 / SC-1 / B-V7, **从没回头改 B 任务本身** —— memory `fix-the-class` 本 cycle 第七次)。
- **实证照字面执行会坏**: `:251-257` 是 **7 行**, B-8a 换成 **3 行** ⇒ 下方整体上移 4 行 ⇒ 原 `:263-265` 的 **Step 6** 恰好落到 `:259-261`, 而 B-8b 正按绝对 `:259-261` 下手 ⇒ **删掉的是 Step 6, 真正的 Step 5 原封不动**。
- ⛔ **强制护栏 (对每条 B 任务, 逐条)**: 落盘**前**先 `sed -n '<N>p' <目标文件>` 打印该行, **逐字确认内容与任务描述相符**; 不符即**停下重新定位**, 不得照行号硬改。这条护栏与执行顺序无关, 是唯一对「前面的编辑移了位」免疫的判据。
- **推荐执行序**: 同一文件内**按行号从大到小**做 (`:622 → :607 → :588 → :318 → :317 → :259 → :251 → :247 → :87 → :56 → :47 → :40 → :17 → :4`) —— 自下而上编辑时, 每次改动只移动它**下方**的行, 而下方的都已做完, 上方待做的行号仍然有效。B-2 的 Step 7 段落部分在 `:318` **上方**, 不受 `:318` 改动影响。

---

## TG-B — CLI 漂移类级收口 (**18 条**, 两个 SKILL.md + 两份 README)

> ⚠️ **post_planning R2 Critical (F-1) 订正**: R1 修订 (`240ea4c`) **静默删除了 B-14**, 同时把标题计数从「20 行」改成「17 条」⇒ 删完自洽, **数数核不出来**。而 proposal 的 B14 行仍在册、Rule #6 判定表 `openspec-archive` 行的范围写的是「B1-B14」(按内容引, 不锚行号), 且 SC-1 的 pattern 对 `:622` **命中 0** ⇒ **零验收能发现**。已补回并加专属验收 B-V8。

> **通用 post-condition**: 每条改写后该行**不再命中 SC-1 pattern**。
> ⚠️ **B-2 例外**: `:317`/`:318` 本来就不命中该 pattern, 故 post-condition 对 B-2 是**空检查**, 它另有专属验收 (见 B-V7)。
> ⛔ **禁全局 `sed`** (`:275` 的 `§Step2 warn_overlay` 是正确交叉引用) · ⛔ **不重编 Step 编号** (Step 7 被 `spec_complete.py:1251` 引用)

### 有完整字面目标 (照抄即验收)

- [x] **B-1** `openspec-archive/SKILL.md:317` `Step2` → `Step 7`
- [x] **B-4** `:17` → `> **历史**: 2026-02-08 - 初始版本，修复归档目录落点错误 (彼时经由外部工具链, 现已改为 git mv)`
- [x] **B-7** `:247` → `Step 3 - 执行归档 (git mv):` / `:248` → `  命令: git mv openspec/changes/{change_name} openspec/archive/{YYYY-MM-DD}-{change_name}` / `:249` → `  等待: git mv 返回`
- [x] **B-8a** `:251-257` 整块 → Step 4 **四条断言** (落地复审订正, 原为三条 —— 实测 git mv 静默嵌套时前三条全为真) (字面见 proposal B8)
- [x] **B-8b** `:259-261` 整块 → `Step 5 - (已并入 Step 3: git mv 使源目录必然消失)`, **其下无正文**
- [x] **B-10** 示例 1 四行 → 字面见 proposal SC-3(c)
- [x] **B-15** `phase-d-closer/SKILL.md:41` → 字面见 proposal B15
- [x] **B-16** `aria/README.md:85` → `- openspec-archive — Archive completed OpenSpec changes to openspec/archive/ with post-move location checks`
- [x] **B-14** `openspec-archive/SKILL.md:622` 悬空引用 → `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality/` (**R2 补回**)
- [x] **B-17** `aria/README.zh.md:85` → `- openspec-archive — 归档已完成的 OpenSpec 变更到 openspec/archive/ 并做落点校验`

### 只给方向 (落盘前逐条自测 pattern)

- [x] **B-2** `:318` **+ Step 7 段落** (作用域按 proposal B2, **不是只改 `:318` 单行**): `:318` 只留 `{sha}` 模板; 可验证约束 (必须含 7-40 位十六进制 SHA) 与 C2 调用行写进 **Step 7 段落**。**硬约束: `:318` 不得以「填入」二字结尾**
- [x] **B-3** `:4` frontmatter `description` 删「自动修正 CLI bug」
- [x] **B-5** `:40` + `:41` 核心功能表**两行的两个单元格全部重写** (`:40` 执行归档 → `git mv …`; `:41` 自动修正 → 位置校验)
- [x] **B-6** `:56`「本 Skill 会自动修正此问题」→ 对采用者的条件表述
- [x] **B-9** `:87` 退役 `keep_changes_copy`, 移入**新增小节 `## 已退役配置项`** (放在 `## 错误处理` 之前; 格式: 标题 + 一行说明 + 一行退役理由)
- [x] **B-11** `:588` 错误表 CLI 行 → `git mv` 失败三分支 (目标已存在 → BLOCKED-already-archived / 源未跟踪 → 先 `git add` / 其余按 stderr 原文)
- [x] **B-12** `:607` 流程图行 (「Step 3-6 执行归档 / 修正 CLI bug / 验证结果」→ 去掉「修正 CLI bug」)
- [x] **B-13** `:47-58` 已知 Bug 节保留 + 时限限定行插在**标题行之后、`**问题**:` 行之前**; 该行须含「本仓从未安装该 CLI」与「归档走 git mv」两个事实

### TG-B 验收

> 📏 **本 Spec 全部验收项的类级规则 (post_planning R5 后定向 sweep 补, memory `spec-acceptance-needs-baseline-run`)**: **每一条都必须标注基线色** —— 🔴 基线红 (真变更断言) 或 🟢 基线即绿 (不变量/回归/污染守卫, 且须写明它**证明不了**什么)。R5 后 sweep 实测: 17 条验收里 **11 条原本没标**, 其中 B-V7(a) 实为恒绿却被当作 B-2 的变更断言。新增验收项一律照此标注。

- [x] **B-V1a** SC-1 前半: 四文件**区段外命中 == 0** (基线 15) 🔴 **基线红**
- [x] **B-V1b** SC-1 后半 (**post_planning R1 补**): **区段内命中集合按内容钉死** —— 恰为 (a) `## ⚠️ 已知 Bug` 标题行 / (b) `**问题**: …CLI 命令有 bug…` 行 / (c) CHANGELOG 表 `1.0.0 … 初始版本，实现 CLI bug 自动修正` 行 / (d) B-13 新插的时限限定行 (若命中)。**其余一律不允许** —— 缺这半会让 B-6 的守卫消失 🔴 **基线**: 区段内除 (a)(b)(c) 外还有 `:56`「**本 Skill 会自动修正此问题**」, B-6 改写后它才离开该集合 ⇒ 基线**不满足**
- [x] **B-V2** SC-1b **语义复核** (非机械, 独立勾选): 对着 §Why 反转 1 重读 B-3/B-5/B-6/B-15/B-16/B-17 改后原文, 断言不再承诺自动处理 CLI 问题。**须把六条改后原文逐条抄进本文件 + 一句理由**, 不接受「已复核」四字带过 🔴 **基线**: 六条原文 (`:4` `:40-41` `:56` + phase-d-closer `:41` + 两份 README `:85`) **全部仍在承诺自动处理 CLI 问题** ⇒ 基线复核结论为「未通过」
  > **B-V2 语义复核实录 (Phase B 执行时填, 逐条原文 + 理由)**:
  >
  > - **B-3** `openspec-archive/SKILL.md:4` 改后原文: `归档已完成的 OpenSpec 变更到 openspec/archive/ 目录，并做归档后落点校验。`
  >   理由: `description` 只陈述做什么 (归档 + 落点校验), 删掉了「自动修正 CLI bug」这句现时能力承诺
  > - **B-5a** `同 :40` 改后原文: `| **执行归档** | 'git mv openspec/changes/{name} openspec/archive/{date}-{name}' |`
  >   理由: 把「调用 openspec archive CLI」换成实际执行的 `git mv` 命令 —— 描述的是真实路径, 不再指向未安装的工具
  > - **B-5b** `同 :41` 改后原文: `| **位置校验** | 归档后断言目标存在 / 源已消失 / 无 'changes/archive/' 残留 |`
  >   理由: 「自动修正」整行改为「位置校验」, 从「我替你修」降为「我检查结果对不对」, 不承诺修复
  > - **B-6** `同 :58` 改后原文: `**本 Skill 自 v1.72.0 起改走 'git mv', 不再经由上述工具链** —— 故本仓不会产生该错位; 仍使用旧工具链归档的采用方需自行处置。`
  >   理由: 从无条件现时承诺改为对采用者的条件表述: 本仓因改走 git mv 不会遇到; 仍用旧工具链的采用方**需自行处置**
  > - **B-15** `phase-d-closer/SKILL.md:41` 改后原文: `| D.2 | openspec-archive | Spec 归档 (**#95 完成度 + C 分级证据闸 tri-state verdict, verdict=block 时本步 BLOCK**) | spec_archived |`
  >   理由: 删掉括号内「自动修正 CLI bug」的跨 Skill 声称, 只留 `10CG/aria-plugin#95` 完成度与 C 分级证据闸这两个真实职责
  > - **B-16** `aria/README.md:85` 改后原文: `- openspec-archive — Archive completed OpenSpec changes to openspec/archive/ with post-move location checks`
  >   理由: 英文名册行从 `(auto-fixes CLI bugs)` 改为 `with post-move location checks`, 门面文档不再对外承诺自动修复
  > - **B-17** `aria/README.zh.md:85` 改后原文: `- openspec-archive — 归档已完成的 OpenSpec 变更到 openspec/archive/ 并做落点校验`
  >   理由: 中文名册行同步, 与 B-16 语义一致 (i18n 实质变更, 故 B16/B17 同批改)
  >
  > **断言**: 七条改后原文**均不再承诺自动处理 CLI 问题** —— B-6 是唯一保留条件表述的一条, 且已明写「需自行处置」而非「本 Skill 会修」。⇒ SC-1b 通过。
- [x] **B-V3** SC-2: `grep -n 'Step2' openspec-archive/SKILL.md` 命中 **1** 处, 且该行**内容**为 `# "全部 unverified_claims" (无论 §Step2 warn_overlay 是否写了 --ack-unverified) 而来;` (**按内容不按行号** —— 前面几个 B 任务会移动行号) 🔴 **基线**: 实测命中 **2** 处 (`:275` 交叉引用 + `:317` 待改锚点), 验收要 1 ⇒ 基线**红**
- [x] **B-V4** SC-3: Step 5 正文 **0 行** / Step 4 **恰 4 条 `断言 N:` 行** (落地复审订正, 原为 3) / 示例四行逐行等于目标文本 🔴 **基线**: 实测 Step 5 正文 **2 行** (要 0) / Step 4 正文 **6 行** (要 3) ⇒ 基线**红**
- [x] **B-V5** SC-4: `keep_changes_copy` 命中全落 `## 已退役配置项` 内 🔴 **基线**: `已退役配置项` 小节命中 **0** (尚不存在), 两处 `keep_changes_copy` (`:87` `:261`) 全在小节外 ⇒ 基线**红**
- [x] **B-V6** Rule #3: `aria/skills/openspec-archive/CHANGELOG.md` `[Unreleased]` 加条目, **且该条目须点名本次改的 Step 3/4/5 与退役的 `keep_changes_copy`** (防恒绿) 🔴 **基线**: `[Unreleased]` 段**已有条目** (关于 `10CG/aria-plugin#95` 的 C 分级证据闸), 但**零条点名本 Spec 的 Step 3/4/5 改动或 `keep_changes_copy` 退役** ⇒ 基线**红**。⚠️ 判据必须是「点名了这几项」而**不是**「段内有条目」—— 后者基线即绿
- [x] **B-V8** (**R2 补**, B-14 专属 —— SC-1 的 pattern 对 `:622` 结构上命中 0, 抓不到它): `grep -n 'aria-archive-gate-runtime-reality' aria/skills/openspec-archive/SKILL.md` 的命中行须含 `openspec/archive/2026-07-05-` 前缀; 且 `openspec/changes/aria-archive-gate-runtime-reality` 不存在。**基线该断言为红** (现文本指向 `openspec/changes/...`, 而该目录已不存在) 🔴
- [x] **B-V9** (**R5 完备性批评席 Major 补**, B-13 专属 —— B-13 是 TG-B 十八条里**唯一零验收覆盖**的交付物: 唯一提到它的 B-V1b(d) 写的是「B-13 新插的时限限定行 (**若命中**)」, 而实测该行的两个事实串对 SC-1 pattern **零命中** ⇒「若命中」是恒真子句, 等于没验): `grep -n` B-13 新插的那行, 须**同时**含「本仓从未安装该 CLI」与「归档走 git mv」两个字符串, 且位置在 `## ⚠️ 已知 Bug` 标题行**之后**、`**问题**:` 行**之前**。**基线该断言为红** (该行尚不存在) 🔴
- [x] **B-V7** B-2 专属验收 (**post_planning R1 补**, 因通用 post-condition 对它是空检查; **R5 F2 订正: 改为按内容不按行号, 并按落点分派** —— 原文把三条断言全钉在绝对行 `:318` 上, 而 TG-B 自身会把该行上移约 5 行 ⇒ (a) 会在随机行上恒真、(b)(c) 必然误红)。**本项在 TG-B 全部落盘后跑**: (a) `grep -c '填入"' SKILL.md` == **1** (只剩 `:317` 那条锚点串) 🟢 **(a) 基线即绿 (实测命中已是 1), 它是 C-1 锚点唯一性的不变量守卫, 不是 B-2 的变更断言** —— 按 memory `assert-this-action`「验动作发生了须钉本次新产生的对象」, B-2 是否真做了由下面 (b)(c) 判定 (**R5 后 sweep 补**: 原写「不以『填入』二字结尾」基线亦已满足, 换成 (a) 只是把一个恒真换成另一个恒真); (b) **Step 7 段落内** `grep -q '7-40 位十六进制'`; (c) **Step 7 段落内** `grep -q 'archive_tracker_verify.py'`

---

## TG-C — 三个脚本 + 测试

- [x] **C-1** `skill_md_literal_sync_probe.py` → `aria/skills/state-scanner/scripts/`。**路径解析用 `Path(__file__).resolve().parents[3]`** (= 插件根, 实测 `scripts → state-scanner → skills → aria`), **不用 `CLAUDE_PLUGIN_ROOT`**。**须含三条判断**: (a) 两侧锚点各提取 1 处否则 **rc 1** (**R5 订正: 原写 `rc 2`, 与本文件 C-3、proposal 四态表、以及 A.1 实跑脚本三者均不符** —— 删掉 SKIP 态后 C1 已无「判不了」这一档, 锚点数异常是**真失败** (措辞被改动, 探针需人工对齐), 归 rc 1); (b) 两侧逐字相等; (c) **命中串必须含 `Step 7`** (挡「两侧同改回 Step2」)
- [x] **C-2** 注册 C-1 进 `.aria/state-checks.yaml`: **`name: skill-md-sha-backlink-literal-sync`** (该 name 被 C-V3 逐字断言, **不得另拟**) / `severity: warning` (参照 `issue-cache-freshness` 体例)
- [x] **C-3** **四态实跑留证** (原五态里的「插件源码不可见 → SKIP」已删 —— 用 `parents[3]` 后该态永不触发, 保留即测量剧场)。⚠️ **基线态必须在 B-1/B-2 之前跑** (跑真仓); **其余三态在 scratchpad 同构插件树里跑**:
  > 📄 **实跑输出留证**: [`evidence/phase-b-probe-runs.md`](./evidence/phase-b-probe-runs.md) (由脚本重新实跑生成, 非对话转抄)
  > 🔧 **同构插件树怎么造** (post_planning R5 F1 Critical 订正 —— 原文写「设 `CLAUDE_PLUGIN_ROOT` 指向夹具」是**惰性指令**, C-1 明令用 `parents[3]` 不读 env, 实测设与不设逐字节相同; 照原文执行会让三个非基线态全部读真仓, 其中两态**恰好返回期望的 rc ⇒ 假绿**):
  > `mkdir -p $FX/skills/state-scanner/scripts/lib $FX/skills/openspec-archive` → 把探针**复制进** `$FX/skills/state-scanner/scripts/` → 在 `$FX/skills/openspec-archive/SKILL.md` 与 `$FX/skills/state-scanner/scripts/lib/spec_complete.py` 放该态所需内容 → **跑那份副本** (`parents[3]` 自然解析到 `$FX`)。
  > ⛔ **仓内两个目标文件全程只读**; 每态跑完核 `git status --porcelain` 与 `git -C aria status --porcelain` 均**不含** `spec_complete.py` 与 `openspec-archive/SKILL.md` (它们是本 Spec 明文非目标, 见已知风险 5)。
  - 基线 (当前仓, 两侧不等) → FAIL rc1 且打印两侧原文
  - 目标 (夹具: SKILL.md 已改 `Step 7`) → PASS rc0
  - 锚点提取数≠1 (夹具: 两个空文件) → FAIL rc1
  - **坏实现「两侧同改回 Step2」** (夹具: SKILL.md 原样 + spec_complete.py 副本改成 `Step2`) → FAIL rc1
- [x] **C-4** ⚠️ **B-2 落地后**立即重跑 C-1 锚点唯一性 (SKILL.md 侧命中数须仍为 1)。**不是 B-1** —— B-1 只改 `:317` 内的 `Step2`, 不动 `:318`, 锚点数恒为 1 ⇒ 在 B-1 后跑是恒绿; 唯一能把锚点数推到 2 的是 B-2 对 `:318` 的改写
- [x] **C-5** `archive_tracker_verify.py` → **新建** `aria/skills/openspec-archive/scripts/`
- [x] **C-6** 单测 → **新建** `aria/skills/openspec-archive/tests/`, **必须带 `conftest.py`**。⚠️ **不是照抄 `phase-d-closer/tests/conftest.py` 的内容** (那份 docstring 逐句是 phase-d-closer 专属事实), 而是照抄它的**做法**: 写成**纯 docstring 零代码**的文件, 内容说明 (a) 它为什么存在 (触发 `is_pytest_suite()` 第一条判据); (b) 删掉它会退回 `OK (0 tests)` 的回归判据。**sys.path 由测试文件自己做** (照 `test_fetch_gate.py:17` 的 `sys.path.insert(0, parent.parent / "scripts")`)
- [x] **C-7** 夹具 → `tests/fixtures/`, **冻结快照**。抓取命令: `forgejo GET /repos/10CG/Aria/issues/<n> | jq -r '.body' > fixtures/issue-<n>.md`, 对 `201` / `185` / `186` 各一份; 每份**首行加注释**记来源 `10CG/Aria#<n>` 与抓取 UTC 时刻。另建合成夹具 `synth-short.md` (回链行尾部含短十六进制 `abc`) —— 真语料证不了长度下限
- [x] **C-8** C2 五态实跑: `10CG/Aria#201` rc0 / `10CG/Aria#185` rc1 NO_SHA / `10CG/Aria#186` rc1 MISSING / `synth-short` rc1 / body 取不到 rc2
  > 📄 **实跑输出留证**: [`evidence/phase-b-probe-runs.md`](./evidence/phase-b-probe-runs.md) (由脚本重新实跑生成, 非对话转抄)
- [x] **C-9** `check_bare_issue_refs.py` → `aria/skills/state-scanner/scripts/` (SC-12); **外加主仓 `.aria/bare-issue-ref-allowlist.txt`** (允许清单外置, 脚本零项目专属字面; 落地复审 M4 补)
- [x] **C-10** C-9 三态留证 (目标态 rc0 / 正控 `d81873b^` rc1, **命中数由脚本产出不写死 —— 实跑 4 处, 原规格写「3 处」已订正** / 坏实现裸 grep 任一版报非零 ⇒ 判无效)。**具体命中数只贴脚本产出, 不写进 proposal 正文**
  > 📄 **实跑输出留证**: [`evidence/phase-b-probe-runs.md`](./evidence/phase-b-probe-runs.md) (由脚本重新实跑生成, 非对话转抄)
- [x] **C-V1** `bash aria/skills/run_all_tests.sh` 里 `openspec-archive` 那行测试数 **非 0** (基线该行不存在 ⇒ 真红→绿) 🔴 **基线红**
- [x] **C-V2** 全套件 ≥ **2122** 且 0 FAIL; state-scanner `run_tests.py` ≥ **1575 / OK** 🟢 **基线即绿 (2122 == 2122), 这是回归守卫** —— 它防的是「本 Spec 把别的测试跑挂」, 不证明本 Spec 做了什么; 新增测试的证明在 C-V1
- [x] **C-V4** (**R2 补**, 对应已知风险 5): C-3 四态跑完后核 `git status --porcelain` 与 `git -C aria status --porcelain`, 确认 `spec_complete.py` **未被修改** (它是本 Spec 明文非目标)。若曾误改须 `git checkout` 还原并复核 🟢 **基线即绿 (实测 `git -C aria status --porcelain` 为空), 这是污染守卫**
- [x] **C-V3** (**post_planning R1 补**) C-2 注册生效核验: 跑一次 `/state-scanner`, 确认 snapshot 的 `custom_checks.results` 里**出现** `skill-md-sha-backlink-literal-sync` 这一项**且 `status == "pass"`** (**R5 完备性批评席 Major 订正: 原写「status 非 `error`」把红当绿** —— 实读 `custom_checks.py:373-379`, `error` 只给 rc 127, **rc 非零一律映射为 `fail`** ⇒ 原判据对一个正在报 FAIL 的闸门也放行, 而全 Spec 再无第二处要求 C-1 在真仓转绿)。⚠️ **本项须排在 TG-B 全部落盘之后** —— 在此之前 C-1 本就该是红的。🔴 **基线**:该 check **尚未注册**, snapshot 里根本没有这一项 ⇒ 基线**红** —— 否则「注册了但没被扫到」与 Part A 的零触达故事同构

---

## TG-D — 开单 (六条待开 + 三条已开)

- [x] **D-1** AB 套件缺 Step 7 / D auto-issue 维度 → `10CG/aria-plugin`  ⇒ **已开 `10CG/aria-plugin#190`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
- [x] **D-2** openspec-archive evals 三处缺 `YYYY-MM-DD-` 前缀 + `cli_wrong_path` 与 SOT 矛盾 + 断言首句零判别力 → `10CG/aria-plugin`  ⇒ **已开 `10CG/aria-plugin#191`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
  > ⚠️ **落地复审订正 (2026-09-08)**: 开单时只覆盖了本条列出的**一条半**子缺陷 —— 第三条「断言首句是次句的真子串 ⇒ 零增量判别力」完全没写进 `10CG/aria-plugin#191`, 且修复面漏了源文件 `openspec-archive/evals/evals.json` (4 个 eval, 派生的 ab-suite 只有 2 个)。**已在该 issue 追评论补齐**, 但本条的「已开」不等于「已覆盖全」。
- [x] **D-3** `unverified_claims`/`unverified_ack` frontmatter 只写不读 → `10CG/aria-plugin`  ⇒ **已开 `10CG/aria-plugin#192`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
- [x] **D-4** `standards/openspec/AGENTS.md:57` 悬空脚本 → `10CG/aria-standards`  ⇒ **已开 `10CG/aria-standards#21`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
- [x] **D-5** `spec-drafter/SKILL.md:192 :507 :510` 指示运行未安装的 `openspec validate` → `10CG/aria-plugin`  ⇒ **已开 `10CG/aria-plugin#193`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
- [x] **D-6** **C 分级死码检查对非 Python 符号结构性失明** (Phase B 实跑订正 —— 起草时写的「`:353` ⇒ dead ⇒ block」两半皆被推翻, 见 proposal D6 行的实测原文) → `10CG/Aria`。⛔ 不得改任务行措辞绕开 / 不得 AI 自行豁免  ⇒ **已开 `10CG/Aria#208`** (D-V1 回读核验: state=open, title 与正文首行均已实读)
- [x] **D-7** `10CG/aria-plugin#187` · [x] **D-8** `10CG/aria-plugin#188` · [x] **D-9** `10CG/aria-plugin#189`
- [x] **D-V1** 六条新单全部**回读核验** (title + 正文首行), issue 号**带仓限定**记回本文件 🔴 **基线**: 六条 (D-1..D-6) **尚未开** ⇒ 基线**红**
- [x] **D-V2** 跑 `check_bare_issue_refs.py` 对 proposal.md 与本文件, rc == 0 🔴 **基线**: 脚本**尚未落盘** (C-9 未做) ⇒ 基线**跑不了**; C-9 落盘当天须立刻补跑一次并记结果, 不得把「跑不了」当成绿

---

## TG-E — Rule #6 AB + 发版 + 集成

- [ ] **E-0** ⛔ **SC-11 阻塞项**: 把「SOT §1『整个变更』跨多 Skill 时的作用域」写进 handoff 请 owner 裁 (a) ratify v1.69.1 形状为成文 lane / (b) 另裁。**取得答复前不得进入 C.2 —— 即不得执行 E-7a 起的任何步骤 (含 E-7a 的 fetch/断言前置)**。
  ⚠️ **卡住时怎么办** (**边界已并入上方主句; 本段只留 rationale** —— post_planning R3 Critical R3-C1: R2 只在此加脚注纠正范围却没回头改主句, 致同一任务两个边界, 而主句权重更高): E-0 不阻塞 TG-B/TG-C/TG-D 与 **E-1..E-6**; 它挡 **E-7a 起的全部步骤**。若 owner 长时间不答复, **停在 E-6c 之后**, 把已完成部分写进 handoff, **不合并也不推任何 remote**。
  ⚠️ **停在那里时 `plugin-cache-currency` 必然是红的** (E-6b) —— 这是**已知且已登记**的状态, **不得**为了「让它绿」而自行豁免或跳过 (那正是 R4 GOV 逐字点名过的自行豁免形状); handoff 须如实写明该 check 红及其原因。
  > **为什么范围要收到 E-6**: R1 版写「不阻塞 E-2..E-8」是错的 —— **E-7b 就是「子模块本地 merge + 双推」**, 它会在 owner 裁定前把 `<vNEXT>` (含 SC-11 正要问的 B-15 phase-d-closer 与 C-1/C-9 state-scanner 改动) **不可逆地发布到两个公共 remote**。proposal SC-11 明写「取得答复前不得进入 C.2」, 而**子模块合并推送就是 C.2 的一部分**, 不只是主仓 PR 合并。
  > R1 那条修复本身造了一个新的自行豁免 (memory `fix-recurs-in-fallback`: 修复类改动最易在自己新写的兜底路径重犯要治的病)。
- [ ] **E-0b** (**post_planning R1 补**) SC-11 若得 (b) 裁定: 补跑 `phase-d-closer` 与 `state-scanner` 两个 AB 套件, 结果同样存 `ab-results/`
> 🛑 **TG-E 的阻塞面 (2026-09-08 订正后: 从两个门减为一个)**:
>
> **阻塞 (E-0, SC-11 owner 裁定)** ⛔ 挡 **E-7a 起**的全部步骤 (含子模块本地 merge + 双推 —— 不可逆地发布到两个公共 remote)。
> 判据可机械核: handoff 里该问题的 owner 答复段非空; 若为 (b) 裁定则对应 `ab-results/` 目录存在。
>
> ✅ **原「阻塞 1」已撤销**: 那是我在 post_planning R5 自己加的一道 SOT 不要求、机制上也够不着的前置 (详见 E-1 的订正史)。**E-1 → E-6c 现在没有前置阻塞**, 可以执行。
>
> ---
>
> 📐 **预备测量 (不依赖上述两个阻塞, 已实跑; 执行时须重跑取新值, 不得照抄本段)**:
>
> **E-4 三腿实测 (2026-09-07T14:5xZ)**:
> - **(a) 已发布集合**: `github` 与 `origin` 两端一致, 最高 = **`v1.71.1`** (两端并集无分歧)
> - **(b) 并发轨自报号普查**: 遍历 `origin/master:openspec/changes/` 全部子目录, 命中两条轨,
>   **自检基线通过** (`handoff-multibranch-subdir-path-fidelity` 与 `pre-merge-completeness-gate-change-scope`
>   均在普查结果内)。两轨各自的 proposal 都出现 **`v1.71.2`** 与 **`v1.72.0`** 两个候选号。
> - **(c) 全 handoff 面 `vNEXT` 扫描**: 本地 6 份 + `origin/master` 6 份命中 `vNEXT`,
>   **声明的全部是已发布的 `1.70.0`**, 无对未来号的活声明。⇒ 如实登记「扫了 12 份, 零未来号声明」。
> - ⇒ **本时刻推得 `<vNEXT>` = `v1.73.0`** (排除已发布 ≤`v1.71.1` 与两轨已宣告的 `v1.71.2` / `v1.72.0`;
>   级别 MINOR)。**该值随并发轨推进而变, E-4 执行时必须重跑三腿。**
>
> **E-5 版本串面重测 (2026-09-07)**: `1.71.1` 全仓 **23 处 / 13 文件** —
> `aria/.claude-plugin/plugin.json` 1 · `marketplace.json` 2 · `aria/VERSION` 2 · `aria/CHANGELOG.md` 1 ·
> `aria/README.md` 1 · 主仓 `VERSION` 1 · `CLAUDE.md` 2 · `README.md` 2 · `README.zh.md` 3 ·
> `README.ja.md` 3 · `README.ko.md` 3 · `system-architecture.md` 1 · `version-scheme.md` 1。
> 减去两处 append-only (`aria/CHANGELOG.md:13` 段标题 / `aria/VERSION:4` 当期发布日期) ⇒
> **要改 21 处 / 12 文件** —— `aria/CHANGELOG.md` 唯一那处就是 append-only 段标题, 故该文件整体退出计数。
> **⇒ 与起草时基线逐字一致, 重测未发现漂移。**

- [ ] **E-1** AB 前置 —— **逐条实测后的判定 (2026-09-08; 本条被订正过两次, 完整链条见下)**:

  **结论: 本套件不需要 `ARIA_COORDINATION_NO_PUSH=1` 会话级前置。** 依据两条独立证据:

  1. **SOT 的触发条件不匹配** (memory `exact-exception-condition`: 逐字核对确切触发条件): `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 1 运行前置 的判据是「凡被测 Skill **能触达** `skills/state-scanner/scripts/phase1_gate.py` / `release_gate.py` 的套件」, 并给出封闭枚举「今天是 `phase-b-developer.json` / `branch-manager.json` / `state-scanner.json` + `phase-d-closer.json`; spec `a1-entry-claim-duplicate-work-guard` ship 后再加 `phase-a-planner.json` / `spec-drafter.json`」。**`openspec-archive.json` 不在其中**。
  2. **判据本体实测不成立**: `grep -c 'phase1_gate\|release_gate' openspec-archive/SKILL.md` = 5, 但**五处全在示例输出块里** (`:520` `:527` `:536` `:540` `:545` 演示 `blocking_reasons` 长什么样, 用 `multi-terminal-coordination` 当例子), **零处是调用**。该 env 只被 `phase1_gate.py` / `release_gate.py` / `lib/failure_handlers.py` 读, openspec-archive 的 Step 1-7 一个都不碰。

  **另一半 —— 真仓触达风险, 逐 eval 分档**:
  - **eval 1 `correct-archive-path`**: 会**写** (归档动作), 但带 `project_root=/workspace/my-project` (合成) ⇒ 不触真仓。
  - **eval 2 `already-archived-detection`**: **无 `project_root`**, 两个路径 (`openspec/changes/user-auth` / `openspec/archive/user-auth`) 是仓相对 —— 但动作是**检测 (只读)**, 且这两个路径在真仓**都不存在** (实测) ⇒ 读空, 无写入面。

  > 🔁 **本条的订正史 (留着是因为它本身是个教训)**:
  > - **起草版**: 「两个选中 eval 用合成路径 ⇒ 不需要该前置」—— 结论对, 但**证据不准** (「两个」只对 eval 1 成立)。
  > - **post_planning R5**: tech-lead 席抓到「eval 2 无 `project_root`」—— **事实对**, 但它推出的结论 (要那个 env) 不成立, 而我采纳时**没有验证这条推理链**, 把「摸到真仓树」与「推协调 ref」两个不同的风险混成一条, 于是写了一个 SOT 不要求、机制上也够不着的前置, 并据此把 E-2 起全部步骤自我阻塞。
  > - **本版**: 证据订正 + 结论按实测恢复, 两个风险分开处置。
  > 教训: memory `exact-exception-condition` 是**双向**的 —— 既不能松引豁免, 也不能凭一个「事实正确但推理断裂」的 finding 加一道 SOT 没有的闸门。

  ⚠️ **仍然成立的运行纪律** (与上述无关, 出自 memory `ab-harness-real-repo`): AB 跑在**真仓 + 真 origin + 无 sandbox**, 被测臂是自主 agent, 可能做出超出 eval prompt 的动作。⇒ E-2 跑完须核 `git status --porcelain` 与 `git -C aria status --porcelain`, 确认无意外写入; 并按 SOT §场景 1 第 3 条做事后清理 (`git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐) —— **即便本套件不推 claim, 这条清理是无害的**。

- [ ] **E-2** 跑 openspec-archive AB (`/skill-creator`)。两臂 = **v_new vs v_old**。**隔离条款 (post_planning R1 补)**: 各臂输出写各自 `outputs/`, 不写仓内固定路径 (`10CG/aria-plugin#180`); AB 跑在真仓无沙箱 (memory `ab-harness-real-repo`)
- [ ] **E-3** 结果存 **`aria-plugin-benchmarks/ab-results/`**`2026-09-XX-v<vNEXT>-archive-skill-drift/RESULT.md` (**R5 订正: 原写裸相对 `ab-results/`, 仓根无此目录**; 真根见 CLAUDE.md 信息地图); **须显式记录本次 AB 对本改动的区分力评估** (预期零); `WITHOUT_BETTER` 逐条解释或回退
- [ ] **E-4** 版本 bump `aria/.claude-plugin/plugin.json` (SOT = 该文件)。⛔ **版本号不得从本文件照抄** —— 本 Spec 起草时写的是 `1.72.0`, 而同期有**两条并发轨在抢同一号段**且本 Spec 对它们结构性不可见 (见已知风险 7)。**执行时现算, 三条前置全过才写**:
  - **(a) 已发布集合**: `for r in $(git -C aria remote); do git -C aria ls-remote --tags $r 'v1.7*'; done` —— **动态枚举 remote, 不写死名字** (R5 后 sweep: 原写死 `origin` + `github` 是正向枚举, 今天恰好完整但加第三个 remote 即 fail-OPEN, 同 memory `invariant-needs-failclosed-default`); 取**全部 remote 并集**的最高号 (单端会漏: 镜像可能半推, memory `partial-push`)。**任一 remote 的 `ls-remote` 失败即停**, 不得拿部分结果当全集
  - **(b) 并发轨已宣告号 —— 普查, 不是点名** (**R5 F4 订正**: 原文写死两条路径是**正向枚举**, 对第三条轨 fail-OPEN, 与本 Spec 要治的盲区同形状, memory `fix-recurs-in-fallback`): 遍历 `git ls-tree -d --name-only origin/master openspec/changes/` 的**全部**子目录, 逐个 `git show origin/master:<d>/proposal.md 2>/dev/null | grep -oE 'v?1\.7[0-9]\.[0-9]+'`。**自检基线**: 普查结果必须**包含** `handoff-multibranch-subdir-path-fidelity` 与 `pre-merge-completeness-gate-change-scope` 两条; 不含即说明扫描写错了, 重写再跑
  - **(c) 同伴 handoff 的 `<vNEXT>` —— 扫全面, 不锚指针** (**R5 F4 订正**: 原文「读 `latest.md` 指向的两份」实测 **vNEXT 命中恒为 0** —— 带声明的 6 份 handoff 一份都不在那两个指针上 ⇒ 该腿在健康常态下就是空的, 零信息量却占三分之一置信度, 判据同 memory `false_green_dual_is_permanent_red`): `grep -rln 'vNEXT' docs/handoff/` **并**对 `git show origin/master:docs/handoff/` 同扫, 取近 14 天内文件里的 `<vNEXT>=` 声明。**零命中时必须显式写下「扫了 N 份, 零声明」**, 不得留空 —— 留空与「没扫」不可分辨
  ⇒ 取号 = **不在 (a) 已发布集合、且不等于 (b)(c) 任一已宣告号** 的下一个可用号。**本文件与 `proposal.md` 中一律以 `<vNEXT>` 指代这个执行时才确定的号** (**R5 F11 订正: 区分 Spec 内占位符与交付物字符串**) —— **交付物**里凡以 `<vNEXT>` 描述的字符串 (`plugin.json` / `marketplace.json` / `VERSION` / `aria/CHANGELOG.md` 段标题 / `ab-results/` 目录名 / README badge 等) 落地时写实取号; **本文件与 `proposal.md` 内的 `<vNEXT>` 一律保留占位符不替换** (否则 SC-9 会同时含字面号和「不得照抄本文任何字面号」而自相矛盾)。**级别仍是 MINOR** (本 Spec 新增三个探针脚本 + 退役一个声明接口)。
  > 📌 **为什么这条是硬约束而非建议**: 本仓 `docs/handoff/2026-09-06-session-close-v1.70.0-shipped-170-closed-195-199-triaged.md:13` 开篇第一句就是「**本 session 最该记住的一件事**: 两个容器并行发版会**撞版本号**」; `:80` 记录代价是「他们的 5 文件 + 同步面**全部重做**」。同型事故发生在**本 Spec 起草前一天**。
- [ ] **E-4a** ⛔ **取号后立刻双向登记**: (i) 把实取号**追加到本文件 E-4 行末** (`实取号 = <号>`) —— **这是 Spec 内唯一登记处, 其余 `<vNEXT>` 占位符全部保留**; (ii) 在 handoff §6 公布 `<vNEXT>=<所取号>`。
  **(ii) 是并发轨能看见本轨的唯一通道** —— 本 Spec 的 `proposal.md` 只在**未推送的 feature 分支**上 (他们 `git show origin/master:` 取不到), 协调板上的 claim **无 `linked_issue`** 且本轨的 issue 在**另一个仓** (`10CG/aria-plugin#186` vs 他们的 `10CG/Aria#195` / `10CG/Aria#199`) ⇒ `linked_issue_overlap` 对本轨结构性返回 `[]`。
  **验收 = 对 handoff 文件 `grep -n 'vNEXT'` 有命中且号与 E-4 实取号逐字相等**。
- [ ] **E-5** 版本串同步。⚠️ **append-only 豁免有两处, 不是一处** (post_planning R1 抓到第一处, **R3-M2 抓到我只修了实例没修类**):
  - `aria/CHANGELOG.md:13` `## [1.71.1] - 2026-09-06` —— 段标题, **不改**; 动作是在其**上方新增** `## [<vNEXT>]`
  - **`aria/VERSION:4`** `> **发布日期**: 2026-09-06  # patch: v1.71.1 …` —— **当期发布说明**, 其下已排着一串 `发布日期(旧)`; 发版时是**新增**一条并把这条降格成 `(旧)`, **不是改写它**。(同文件 `:3` 的 `> **版本**: 1.71.1` **要改**)
  ⇒ **要改的是 21 处 / 12 文件** (23 − CHANGELOG:13 − VERSION:4), 外加 CHANGELOG 与 VERSION 各**新增**一条。
  ⚠️ **「21 处 / 12 文件」是起草时的测量, 不是可照抄的常量** —— 任一并发轨先 ship 都会改变它 (CHANGELOG 多一段 / VERSION 多一行 / README badge 换号)。**执行时重测一遍**, 与本数不符时**以重测为准并在本行记下差异及原因**, 不得反过来把仓里改成 21。
  逐文件 `grep -c` 实测并把计数**全部**贴进本文件 (含上述两处标注「append-only, 不改」) —— proposal §Part E「覆盖面诚实登记」段要求「不留不对称缺口」(按内容引, 不锚行号)
- [ ] **E-6a** **五个仓内 check 全绿**: `m6-version-badge-match` / `m6-claude-md-version` / `i18n-readme-translation-currency` / `main-project-version-consistency` / `plugin-version-arch-docs-match`。它们的输入全在仓内, E-5 落地后必然可绿
- [ ] **E-6b** ⚠️ **`plugin-cache-currency` 在 E-4 之后期望 STALE, 不是绿** (post_planning R3 R3-M1): 它比的是**运行时** `~/.claude/plugins/installed_plugins.json` 与 SOT `plugin.json`。E-4 一 bump 到 `<vNEXT>` 它立刻转红, 且**在 TG-E 的任何位置都转不绿** —— 转绿要 owner 终端跑 `/plugin marketplace update` + `/plugin update` + 重启 session (memory `session-level-precondition`: 会话内补不上)。
  **验收 = 贴出它的实跑输出**, 确认红的原因是「installed 落后 SOT」而非别的; **不得把它算进「全绿」**。
  ⚠️ 该例外**尚未成文**: 上一周期 (`docs/handoff/2026-09-06-session-close-v1.70.0-...`) 已把「SC-7 十三条全绿 + plugin-cache-currency 例外」上呈 owner, **写就时尚未裁定** ⇒ 按 memory `exact-exception-condition`「N 次非正式援引 ≠ 成文 lane」, **现在不能援引它当豁免**, 只能如实登记并在 handoff 再次点名
- [ ] **E-6c** ⚠️ 六个 check 合计只覆盖 23 处版本点里的约 6 处, **不能只靠它们判绿** (E-5 的逐文件实测是主判据)
- [ ] **E-7a** (**post_planning R1 补, memory `stale-local-main`**) 子模块 merge **前置**: `git -C aria fetch origin --prune && git -C aria fetch github --prune`; 断言 `local master == origin/master` (不等则先 FF)。**同一断言对主仓也要做** —— 本文件写就时主仓本地 master 实测**落后 origin/master 8 个 commit** (并发轨在飞)
- [ ] **E-7b** aria 子模块**本地** `git merge` feature → master + 双推 (⛔ 禁 Forgejo 服务端合并, 硬约束 1) + 逐 remote `ls-remote` 核验
- [ ] **E-8** 主仓 gitlink bump; **SC-9 两条断言**: (a) `git ls-tree HEAD aria` == `git -C aria rev-parse HEAD`; (b) 子模块 HEAD == `origin/master`
- [ ] **E-9** 主仓 PR → **Rule #8 pre-merge gate** → 合并 (主仓例外可走 Forgejo merge)。⚠️ **服务端合并后 GitHub 镜像不会自动拿到** (`10CG/Aria#165` 形状) ⇒ 必须本地 FF master + `git push github master`
- [ ] **E-10** **逐 remote `ls-remote` 独立核验**两仓, 不信 push 回执 (硬约束 2); gitlink orphan 守卫 (三个子模块 SHA 在两端均可达)
- [ ] **E-11** D.1 进度 → D.2 归档 → D.2b release claim → D.3 handoff
- [x] **E-V1** handoff 须点名六项, **逐项在 handoff 里给可 grep 的锚点**: (1) `SC-11 owner 裁定`; (2) `keep_changes_copy 声明接口移除`; (3) `post_spec converged=false`; (4) `D-6 定时风险`; **(5) `<vNEXT>` (E-4a(ii), 并发轨可见性)**; **(6) `plugin-cache-currency` (E-0/E-6b 两次明文要求的如实登记 —— Rule #10 §5 规定「AI 任何自作主张的流程判断必须写进 handoff 请复议」, 本项是它在本 Spec 里的唯一机械兜底)**。**验收 = 对 handoff 文件 grep 这六个字符串, 缺一即红** (防纯自证) 🔴 **基线**: 本 cycle handoff **尚未写** ⇒ 基线**红**  ⇒ **已写 `docs/handoff/2026-09-07-archive-gate-drift-phase-b-landed-blocked-on-two-owner-gates.md`; 六项 grep 逐条核验全中** (SC-11 owner 裁定 1 / keep_changes_copy 声明接口移除 1 / post_spec converged=false 1 / D-6 定时风险 1 / vNEXT 3 / plugin-cache-currency 1)

---

## 已知风险

1. **自证循环**: D.2 归档要走的正是本 Spec 改的那条路径的邻近面。独立证据: 改前必红测试 (C-3/C-8/C-10 三态) + SC-1 基线 15 → 0 的对跑。
2. **AB 零区分力**: 已在 proposal 登记, RESULT.md 须显式写明, 不把「跑过了」当「验过了」。
3. **`aria-orchestrator` 指针全程 dirty** (他轨 `feature/m6-cost-model-telemetry`) —— 本 Spec 全程不动它, C.1 提交时须核 `git status` 确认未卷入。
4. (**post_planning R1 补**) **并发轨在飞**: 主仓本地 master 写就时落后 origin/master **8 个 commit**, aria 子模块 `3a28339` **未推任何 remote**。每次实质 git 动作前必 fetch (memory `concurrent-duplicate-audit-fetch-before-start`)。
5. (**post_planning R1 补**) **负控夹具必须还原**: C-3 的坏实现态改的是 scratchpad 夹具而非仓内文件; 若执笔者图省事直接改仓内 `spec_complete.py`, **必须在跑完后 `git checkout` 还原并核 `git status`** —— 该文件是本 Spec 的明文非目标。
6. (**post_planning R1 补**) **服务端合并的 GitHub 补推**: 主仓走 Forgejo merge 后 GitHub 镜像落后一个 commit (本 session 在 PR `10CG/Aria#202` 上实测过一次), E-9 已含补推步骤。
7. (**post_planning R5 主控 sibling-spec 交叉审计补, Critical**) **两条并发轨与本轨共享发版面, 且它们看不见本轨**:
   - `openspec/changes/handoff-multibranch-subdir-path-fidelity` (`10CG/Aria#195`) —— `proposal.md:352` 逐字「推荐默认改为 **MINOR / v1.72.0**, 但须 owner 拍板后 Task 5.1 才动手」。**这正是本 Spec 起草时硬编码的那个号**。
   - `openspec/changes/pre-merge-completeness-gate-change-scope` (`10CG/Aria#199` / `10CG/aria-plugin#161`) —— 目标 `v1.71.2`, 并在 `:315` 逐字写「真正在飞、同抢 v1.71.2 的是 **`10CG/Aria#195`**」—— **它枚举并发轨时没有本轨**。
   - **共享面**: 版本 SOT `aria/.claude-plugin/plugin.json` + 派生 5 文件 + 主仓版本引用面 + `aria/CHANGELOG.md` (三方都要 append 一段)。**代码落点零交叠**, 碰撞全部在发版面 ⇒ `git` 不会报冲突 (memory `same-value-merge-silent`: 两侧改成同一个串 ⇒ 零冲突零标记静默采纳, 已有**四处静默合成已发布号**的实证)。
   - **实测 (2026-09-07T09:0xZ)**: `git -C aria ls-remote --tags origin` 最高已发布 = **`v1.71.1`**; `v1.71.2` 与 `v1.72.0` **均未被占** ⇒ 撞号**尚未发生**, 但三轨在抢两个号。处置 = E-4 三条前置 + E-4a 双向登记。
   - **为什么 R1-R5 十五个审计席位都没抳到**: 它们审的是**本地树**, 而两份同期 Spec 只存在于 `origin/master`。印证 memory `combined-mode-sister-spec-audit-value`「single-Spec 漏率 100%」。
