# 决策: a1-entry 三份 Spec 的 6 项裁定 (post_spec R5 用尽后) + 「只认中文的机器 token」被否决

- **日期**: 2026-08-30 | **裁定人**: owner (逐项) | **执行容器**: simonfish/023236f2
- **对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/` (母) · `linked-issue-field-availability/` (字段) · `sibling-spec-probe/` (探针)
- **输入**: `.aria/audit-reports/post_spec-R5-1787840920000-a1-entry-combined-aggregated.md` §主控处置建议 (6 项) + handoff `docs/handoff/2026-08-29-a1-entry-post-spec-r5-exhausted-six-owner-decisions.md` §【1】
- **关联**: Aria#174 (立项 issue) · aria-plugin#135 · aria-plugin#150

## 裁定 (owner 原话逐字: 「1.A 2.b 3.b 4.i 5.可以采纳 6.i，我有一点疑惑，为什么会有只认中文的规范？这个需要质疑和反驳」)

| # | 事项 | 裁定 | 落版含义 |
|---|---|---|---|
| 1 | 挂号单的身份证号用什么 | **A — 恒用 `<spec-slug>-<container_uuid>`, 取消 issue 派生形** | 「同一 issue 是否撞车」改靠 claim 的 `linked_issue` 字段 (Part B1 已存在) 比对; 两个新字段 `spec_slug` / `track_form`、§5.1 二分谓词、§5.3 三元组 release、D12、SC-1/4/27C/30/31 **结构性消失**。**代价成文**: (a) 改 Spec 目录名 = 换身份证, 须 release 旧 + acquire 新两步 (SC-15); (b) 同容器在同一 issue 上开多个方向时, 互报一条 `linked_issue_overlap` advisory 噪声 (同 issue 不同 track-id, 语义上正确 —— 它们确实是同 issue 的两条轨) |
| 2 | 要不要写「发号码机」(派生的代码宿主) | **b — 不建** | 与 1A 一致: 派生退化为一行拼接, 继续在 SKILL.md 模板里由 AI 拼; 验收 = SC-22 文本层 (占位串字面) + 行为类定向 fixture |
| 3 | 收尾方式 | **b — 再跑一轮通用审计 (post_spec R6)** | `max_rounds=5` 已用尽, R6 是 **owner 显式加的一轮** (Rule #10: 加轮/不加轮都是 owner 的决定, AI 不预判)。执行侧先把三条机械不变量跑绿 (每个 `SC-NN` 在 SC 表内 / 每个 `--flag` 在 Impact 表内 / 同一枚举全文一种拼写), 再进 R6, 让 R6 的席位不必花在机械项上 |
| 4 | AB 评测会往生产 `refs/aria/coordination` 推数据 (R5-3) | **i — 单独先修** | 与三份 Spec 的收敛无关, 作为独立 Level 1 变更处置 (落点见本文件末「第 4 项的处置」) |
| 5 | 四条验收项降级的部分回滚 | **采纳** | SC-15 (改名 ⇒ release 旧 + acquire 新, 无孤儿) 回滚为代码类; SC-2 改写声称对象 (钉 `linked_issue_overlaps` 经 CLI 的行为, 不钉派生); SC-1 / SC-4 随 1A 消失 (原判「维持降级」已无对象) |
| 6 | 「无关联 issue」哨兵只认中文 `无` | **i — 扩为 `{"无", "none"}`**, 并要求**质疑和反驳「只认中文」这条规范本身** | 见下节。落版形态比原选项 (i) 多一层: **英文 canonical + 中文 alias**, 且同一结论**同时适用于字段名** (子 Spec O-2, 此前上呈未裁) |

## 「为什么会有只认中文的规范」—— 来源、反驳、处方

### 来源 (实读)

- **字段名 `关联 Issue`**: 子 Spec §3 E0 谓词 1 把行首串钉成逐字节 `> **关联 Issue**:`。这条规则是从**本仓存量语料反推**出来的 —— 母 Spec rework v3 在主仓 `cc1bdef` 上的观测: `grep -rl '**关联 Issue**' openspec --include=proposal.md` 得 15 份 = **14 份 archive/ (稳定子集, 2026-08-30 仍是 14) + 1 份 changes/**, 全部用这个中文字段名。`changes/` 侧随三份在制 Spec 的编辑持续变动 (同命令 2026-08-30 得 17, 且 changes 侧 3 条全是讨论式匹配, 三份头部已改英文) —— **论点只依赖那 14 份** (R6/KM 决策单 M1 订正口径)。子 Spec D9 随后把它写进**跨项目 SOT 模板** `standards/openspec/templates/proposal-minimal.md` (该模板其余三行 `> **Level**:` / `> **Status**:` / `> **Created**:` 全是英文), 理由是「不新增英文别名 = 不新增第二个谓词面」, 并自知有问题, 上呈为 **O-2** (owner 此前未裁)。
- **哨兵 `无`**: 母 Spec NEW-01 + R1 editlist FIX-19 (dogfood) —— 「已核实无关联」这个语义是从本仓 proposal 的中文写法里捡来的, 然后被子 Spec E5 钉成逐字节 U+65E0。

### 反驳 (四条)

1. **把「描述本仓习惯」当成了「规定跨项目规范」。** 规则的证据基础是 14 份中文归档件; 结论却写进了全英文的、随 aria-plugin 分发到所有采用方的模板。样本决定不了分发面。
2. **「单一谓词面」论证混淆了「拼写唯一」与「判定唯一」。** 机械判定需要的是**归一之后只有一个谓词**。别名在读取侧归一 (`Linked Issue` 与 `关联 Issue` 同一字段; `none` 与 `无` 同一哨兵) 只多一行正则, 谓词仍是一个。D9 把「多一个拼写」错当成了「多一个谓词面」。
3. **违反项目自己的工作语言约定。** CLAUDE.md「工作语言」逐字: 「中文叙述为主。保留英文技术 token: 代码 / 命令 / 路径 / … / spec 术语」。**被机器解析的字段名与哨兵值是技术 token**, 按项目自己的规则本该是英文; 把它们写成中文, 是叙述语言的偏好泄漏进了机器接口。
4. **代价落在别人身上且不可见。** 英文项目的作者或 AI 自然会写 `Linked Issue` / `none` / `N/A` ⇒ 全部判 `NO_FIELD` / `BAD_TOKEN` ⇒ 采用方注册 check 后恒红或大量假阳性 (memory `false_green_dual_is_permanent_red`)。本仓 AB 套件 `ab-suite/spec-drafter.json` eval 2「双语输入处理」明确要求生成英文 proposal, 与之直接冲突 (R5/skill-reviewer M2 实测)。

**D9 对在哪 (公平陈述)**: 「第二谓词面」的担心在**写入侧**成立 —— 若模板与 SKILL.md 同时教两种写法, AI 会随机选。所以处方不是「两种都教」, 而是「**教一种 (英文 canonical), 读一种以上 (中文 alias 兼容存量)**」。

### 处方 (第 6 项 + O-2 的落版形态)

| 面 | canonical (模板 / SKILL.md 只教这一个) | 读取侧接受 (归一, 不进任何实参) | 存量处置 |
|---|---|---|---|
| 字段名 | **`Linked Issue`** (与 SOT 模板其余三行同语言; 对应 claim 字段 `linked_issue` / CLI `--linked-issue`) | `{Linked Issue, 关联 Issue}` 两拼写, 大小写按逐字节 | `archive/` 14 份不回填 (D5 作用域只含 `changes/`); 本仓 3 份在制 Spec 本轮改成 canonical (dogfood) |
| 「已核实无关联」哨兵 | **`none`** (ASCII 小写) | `none` 大小写不敏感 (`none`/`None`/`NONE`) 或逐字节 `无` | 同上 |

- 两处 alias 都是**读取侧归一**; E6 的门不变: 哨兵 (任一拼写) ⇒ `--linked-issue` **整参省略**。
- 探针 Spec 的层枚举值 `"wu_empty"` (拼音) 同批改为 `"none_sentinel"`; 常量黑名单里的「字面 `无`」改为「哨兵集合 (canonical + alias)」。
- **回撤成本**: 若 owner 只想改值不改字段名, 回撤只涉及 E0 谓词 1 的两拼写集合 + 模板一行 + 三份在制 Spec 的头部一行; 不涉及任何机制。

## 第 4 项的处置 (单独先修, 不入三份 Spec)

**核查结论 (2026-08-30, 独立 subagent 实读, 与 R5 的说法有一处重要出入)**:
- 评测跑在**真仓、真 `origin`、无沙箱**: `AB_TEST_OPERATIONS.md` 全篇与 `skill-creator` 的 subagent prompt 模板均无 cwd / git init / 隔离机制; 历史 run 产物直接落在 `aria-plugin-benchmarks/ab-workspace/` 真仓路径下 ⇒ **风险真实**。
- 推送点**不是** R5 引的 `write_claim` auto_bootstrap (`coordination_ref.py:800` 是 `bootstrap(..., push=False)`), 而是 `phase1_gate.py` 第 9 步 `resilient_push` (`:791-802`, 另有 7a self-resume 一处), **无条件**; `release_gate.py:172` 同样推。`phase1_gate.py` **自己不读 config**, `coordination.enabled` 只在 SKILL.md 层判 ⇒ AI 直接调脚本就会推。
- 今天 `phase-a-planner/SKILL.md` 尚无闸门调用 ⇒ `phase-a-planner.json` eval 1 **今天不推**; 母 Spec 一 ship 就推。生产 `refs/aria/coordination` 里已有一条 2026-08-02 的合成 `audit-test` claim (非 benchmark 产物, 但证明非生产写入进得去)。
- ⇒ R5-3 的**结论**成立, **机制描述**须勘正 (已写进母 Spec Impact `phase-b-developer` 行 `:96-97`)。

**修复 (已落, 未推, 待 owner 授权 ship)**: aria 子模块分支 `fix/phase1-gate-no-push` @ `007d355` (基于 `d50f9c3` = origin/master, 一个 commit):
- `phase1_gate.py`: `--no-push` flag + env `ARIA_COORDINATION_NO_PUSH` (`1`/`true`/`yes`, 大小写不敏感); keyword-only `no_push` 穿 `run_gate` → `_gated` → `_run_gate_impl` (公共签名向后兼容); **两个**推送点 (7a self-resume + Step 9) 都门控; 本地写 claim 不变; JSON additive 键 `push_skipped` / `push_skipped_reason` (`cli_flag` | `env_var` | `null`), 跳过时 `push_success=false` 永不 `true` ⇒ 跳过 / 失败 / 未到推送步三态可辨。
- `release_gate.py`: 同套 (`--no-push` / env / `run_release(no_push=)` / Step 5 跳过) —— 修类不修实例。
- `lib/failure_handlers.py`: 共享 env 解析 `no_push_requested_by_env()`; `resilient_push` 本身不读环境。
- 测试 `tests/test_coordination_no_push.py` 16 条 (TDD: 实现前全红; 负控 `test_c_negative_control_no_flag_no_env_attempts_push` 用硬编码 `push_skipped=True` 亲验会红后还原); state-scanner 套件 `unittest discover` 在 `007d355` 上 `Ran 1409 tests … OK`; 静态 `def test_` 计数 `d50f9c3` 1409 → `007d355` 1425 (**+16**, 与新增数吻合)。R6/KM M2 订正: 早前写的「1393 → 1409」里的 1393 是 subagent 在同容器动态跑基线的数, 与静态计数口径不同 (临时 worktree 复跑基线得 1389 含 1 fail 1 error, 属环境相关), 以 +16 为准。
- 主仓 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:222-228` 新增「运行前置: 协调 ref 推送隔离」(射程套件清单含 `phase-d-closer.json` —— 它直调 `release_gate.py` 且 `--sweep-stale/--gc` 会改写真实 claim; `ARIA_COORDINATION_NO_PUSH=1 claude …` 启动; transcript 核验 `push_skipped: true`; 事后清理)。

**残留 (类级, 已实证, 本修复未治, 待 owner 定)**: (1) `--no-push` 后合成 claim 留在**本地** ref; fetch refspec 非强制 (`coordination_ref.py:1367`) ⇒ 下一次正常 session 的 fetch 被 non-FF 拒 (fail-soft) → FF push 成功 → **合成 claim 延迟落到远端**。runbook 第 3 条写了「跑完先 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐」为必做; 根治候选 = no_push 模式写 scratch ref / harness 跑在独立 worktree。(2) benchmark 跑 `_main` 仍写生产遥测分区 `.aria/coordination-telemetry.jsonl` (`_source=production`) ⇒ `coordination-gate-invocation` check 会把评测当成真实生产调用, 不在本次范围。(3) `phase-b-developer/SKILL.md:96-97` 的 push 机制描述不准 + `state-scanner/SKILL.md:168` 输出键集缺两个 additive 键 —— 均已登记进母 Spec Impact 表, 随母 Spec 落地。

## 对三份 Spec 的执行顺序 (owner: 先结构 → 再宿主 → 后清账)

1. 结构 (1A) 落版: 母 Spec §2.1 / §5 / D3 / D12 / SC 表 / Impact 表; 删除 K1/K2/K4 块 (原文按字节搬入审计轨, append-only);
2. 宿主 (2b): 不建模块; §2.1a 保留「无代码宿主」成文, K3 块按第 5 项重写;
3. 清账: R5-1 五项实测 (SC-32/33 进 SC 表 / Impact `:721` 措辞 / `:642` compose 残留 / gc.py+heartbeat 行) 逐项落; R5-4/5/6 三条 critical + skill-reviewer 的 major 一并落; 三份 Status 行更新; 三条 grep 不变量跑绿;
4. 第 6 项 + O-2 落版 (两子 Spec + 母 Spec 头部 dogfood);
5. post_spec **R6** (五席, 全新镜头) → 聚合 → 回 owner。


## R6 结果 (2026-08-30, owner 第 3 项加轮) 与新增待裁

五席 (config `teams.post_spec`, 全新镜头) 判 **REVISE**: code-reviewer 3C/11M/13m · backend-architect 0C/2M/1m · tech-lead 6C/9M/7m · qa-engineer 0C/3M/2m · knowledge-manager 0C/3M/2m (PASS)。去重后 **7 个 critical 簇**, 其中 6 个已在 rework v4.1 逐条清账 (清单见 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md` §处置), 1 个属 owner 权限:

| # | 待裁 | 选项 | 执笔倾向 |
|---|---|---|---|
| **R6-1** | 探针 Spec 对字段 Spec 纯函数 `lib/linked_issue_field.py` 的依赖方向 (接缝 C2: 「可先 ship 全走层 2」与「E0–E6 一条不复制」+「钉死 import」三者不可同时成立) | (i) 字段纯函数是探针的**硬前置**; (ii) 探针可先 ship, 模块缺席时 `verdict="not_established"` + `reason="extractor_unavailable"` | (i) —— (ii) 让先 ship 的探针恒「未能核实」, 交付价值为零。改变 08-23「均非阻塞前置」的成文前提, 故上呈 |
| **R6-2** | 字段名 E0 谓词 1 是否做 ASCII 大小写折叠 (QA M3: GitHub 原生术语 `Linked issues` 是真实假阴性来源) | (i) 折叠 (不放宽单复数); (ii) 维持不折叠 (集合封闭) | 无强倾向; QA 席倾向 (i) 且指出它不违反本文件「拼写 ≠ 判定」的论证 |
| **R6-3** | tech-lead 席的收敛判断: 「R5 那版设计收敛为真, 今天这版为假」(86% finding 落在 08-30 新写文本), 建议**换执笔席**清账 + 定向复核, 不加 R7 | (i) 接受主控本轮已做的清账 + 一个新席位定向复核; (ii) 换执笔席重做清账 | 主控已按 (i) 落版 (母 Spec 闸门状态表 #8 留痕请复议) |

**R5 code-simplifier 席未呈项的台账** (R6/CR 流程 m1: 该席 13 项「去掉它会不会漏缺陷」判定与 C3 此前未进任何处置建议; 按 memory `narrow-owner-options` 逐条留痕, 采纳/拒绝理由如下, 「待裁」项由 owner 定):

| 项 | 内容 | 处置 | 理由 |
|---|---|---|---|
| C1 | 双 track-id 形态是自造复杂度 | **已采纳** = 裁定 1A | — |
| C2 | K1 修类不修实例 (`dataclasses.replace`) | **已采纳** (母 §5.3 保留纪律 + Impact heartbeat 行) | 对新代码有效 |
| C3 | 审计对账层再次长回交付面 (editlist 对账表 / 新表面 / 未做 / 闸门状态 / ⛔ 占位节 ≈35KB) | **部分采纳**: 1A 移出的原文与两份旧「新表面」已入审计轨 §6; **未删** editlist 对账表、⛔ 占位节、闸门状态节 | 这三段是 Rule #10 与 R2/M-13「零容忍自述不实」的落点, 删除属 owner 决定; **待裁**: 是否把 editlist 对账表迁回其 SOT 文件的状态列 |
| §3-5 | `heartbeat_by_track` 保留 | 采纳 (保留) | 事故窗 > SWEEP_TTL |
| §3-6 / M2 | 删 `--heartbeat-only` 全套, 改为入口重跑既有 acquire (幂等) | **待裁** | 更小的等价物成立与否取决于「同 session 覆写同一 claim 文件」是否等价于刷新 `heartbeat_at` (未实测); 删掉会连带 SC-21/28/32 与 K7 遥测分区; 执笔不自裁 |
| §3-7 / M1 | 删 `get_container_uuid()` accessor + SC-3 | **未采纳** | §2.1 容器段依据 (label 优先 ⇒ 碰撞域不可控) 仍成立; 该席自己标「基本不漏」而非「不漏」 |
| §3-8 / M3 | `unknown_schema_claims` 全套整条转 follow-up | **待裁** | 场景本仓零实例为真; 但 R2/M-4 + R4/K5 的「零证据不当正证据」修复在它身上; 转出即回到 `_TERMINAL` 静默 skip 的现状 |
| §3-9 / M4 | `unattended` 取值路径钉死或整条删 | **已采纳前者**: 钉死为 aria-runner 镜像内 `.aria/config.json` (母 §2.3), env 三腿仍 follow-up | R6/CR M8 同判 |
| §3-10 | `lib/linked_issue_field.py` 纯函数保留 | 采纳 (保留) | 真承重 |
| §3-11 / M8 | 探针保留但 §6 cap 四件套缩为 `degraded + reason` | **未采纳** | 决定性排序契约是为「两人独立实现得同一截断点」写的 (memory `spec-underdetermination`), 与规模余量无关 |
| §3-12 | `ab-suite/audit-engine.json` 保留 | 采纳 (保留) | Rule #6 |
| §3-13 / M6 | 白名单改为注册行参数 (`--exclude a,b,c`), 删数据文件 + 陈旧守卫 | **待裁** | 零新文件确实更简; 但陈旧守卫 (白名单退化成永久豁免) 是 memory `validator-repo-drift-guard` 的落点, 注册行参数同样会陈旧且更难守 |
| M5 | §2.3 四档选项表缩两档 | **部分采纳**: `abandoned` 与 `active` 共用选项集、`unknown` 视同 `active` (SC-11 已改); 四档**渲染**仍分 | 渲染差异承载 K6「可能是 GC 产物」措辞 |
| M7 | 字段 E0 谓词 2 的论证篇幅进审计轨 | **未采纳 (本轮)** | 篇幅项, 不改设计; 留给 owner 定是否再切一刀 |
| m1–m6 | 引用/坟头行/矛盾句 | m6 (`:519` 矛盾) **已采纳**; m1 (Impact `--spec-slug` 措辞) 随 1A 消失; m2/m3/m4/m5 (篇幅) 未动 | — |
