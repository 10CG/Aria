# Proposal: phase-c-gate-path-coverage-not-applicable (aria-plugin #122)

> **Status**: ✅ **Complete** (shipped aria-plugin **v1.65.0**, 2026-07-31) — Phase A: post_spec R1→R4 CONVERGED + owner sign-off 2026-07-27 (两项均批含默认 true)。Phase B: path_coverage.py + gate 集成 + SC-1~28 全落 (测试 62→97, 全量跨 skill 1546 绿); 文档四面同步 (SKILL.md 八处/config-loader/workflow-state-schema)。Rule #6 照跑 AB (三臂 descriptive 统一): new-vs-old 零回归 + 定向语义正向; without 臂真污染零命中 → DEC-20260722-001 决策 4 重测门裁 [C] 关闭 (#116 闭环)。Phase C: 本地 --no-ff 合并 → aria master `5a9ca18`, 双远程 ls-remote 核验一致 (origin 首查撞 SSH 瞬断, 重试即恢复 — 10cg.local #20 再添一例); **C.2.4 meta-dogfood = not_applicable 首个生产判定** (aether backend 真在场, verdict=green + 双留痕, 六次复发场景第一次零人工裁决)。Phase D: DEC-20260731-001 先存档后改写 + `_lane` 过渡规则 (2) 退役与 gitlink bump 同 commit co-land + #122 关闭。
> **Created**: 2026-07-27
> **Spec Level**: 2 (Minimal — 单域 [C.2.4 gate 增路径覆盖感知三态], 全部落点在 phase-c-integrator; blast radius 限 gate 输出 additive 扩展, covered 路径既有字段逐字段不变)
> **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; triage verdict=`confirmed`/`major`/`next-cycle`, 3/3 复现, [issuecomment-16979](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122#issuecomment-16979))
> **授权链 (Rule #10)**: 本 spec 修改 enabled gate (Rule #8 C.2.4) 的判定语义 — 授权 = owner 2026-07-25 复议定案「#122 (路径覆盖感知 not_applicable 态) 优先落地, 是唯一真机制」(`.aria/config.json` `phase_c_integrator._lane` 留痕; 该裁决全文将在 Phase D 改写 `_lane` **之前**抽取存独立 DEC, 见 §7) + 本 spec owner sign-off。**sign-off 面显式含两项**: (1) 机制本体; (2) `path_coverage_enabled` **默认 true** (TL-8 — 翻默认影响所有装机仓, 单独点名不随整体默认批准)。落地前, 过渡规则 (2) (verdict=wait 一律上报 owner) 继续有效。
> **复发序数口径 (KM-4)**: 「第 5 次」= 历史总复发人工裁决数 (v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0 / v1.64.1); 「手工特批第 2 次」= 2026-07-25 owner 新规 (过渡规则 (2)) 确立**后**的上报-特批次数 (v1.64.0 一次性 ratify 为第 1 次, v1.64.1 为第 2 次)。两口径并存, 下文标注取前者。
> **ship target**: aria-plugin v1.65.0 (MINOR — 新模块 + SKILL.md §C.2.4 指令面扩展; 当前 SOT plugin.json = v1.64.1)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 `openspec/changes/` (meta-repo 惯例, Rule #5)
> **审计轨迹 (post_spec, convergence)**: R1 5-agent [5/5 REVISE; SCOPE_OK ×5] → 4 Critical (TL-1 执行上下文 / BA-1 glob 未建模方向 / BA-2 仓边界 / QA-1 workflow 自身变更反向假绿) + 15 Major 簇 (三处 3-agent 交叉命中: build-aria-runner 语料错 [TL-3=BA-3=CR-1] / covered-unknown 谓词矛盾 [TL-2=BA-4=CR-2] / 文档同步面 [KM-1/2/3]) + 12 Minor → R1-fix 全量吸收 → **R2 5-agent [code-reviewer PASS / tech-lead PASS_WITH_WARNINGS / backend-architect + qa-engineer + knowledge-manager REVISE]**: R1 findings 24 条中 22 条 CLOSED + 2 PARTIAL (BA-2 残留负向 SC / KM-5 指针错字); 新 findings 全部「文字补完级」— 规则 7/8 空真重叠 **四方独立命中** (TL-Major-1 = BA-R2-M1 = QA-9 = CR-N-1) / R2-C1 `pull_request_target` 兜底方向 (BA, 唯一新 Critical) / SC-19 具体化 (QA-10 = CR-N-4 = TL-Minor-2) / KM-9 指针 / 各家 Minor → R2-fix 全量吸收 (判定规则重排为数据依赖序 + reason 封闭集 + D7 精确白名单 + SC-25~27 + KM-9/10) → **R3 2-agent 定向 [backend PASS_WITH_WARNINGS (三残留全 CLOSED + 全分割独立复验通过) / qa REVISE 窄口径 (SC 回填机械缺口)]** → R3-fix (SC-4/5/20/23 reason 回填 + SC-28 empty-diff) → **R4 1-agent 终轮 [qa PASS 0/0/0] → CONVERGED**。报告: `.aria/audit-reports/post_spec-R{1,2,3,4}-1785112156889-phase-c-gate-path-coverage-*.md`

---

## Why

Rule #8 C.2.4 pre-merge gate 对**路径过滤型 CI** 的仓库结构性恒 `wait`:

- `ci_backends/aether.py:223-224` `_normalize_pr_ci_status`: `if not runs: return "pending"` — 「CI 还没跑完」与「CI 永远不会为这些路径跑」折叠为同一值 (函数注释自述保守映射意图, 但未区分两种零 run 成因);
- `pre_merge_gate.py:187-188` `pending → VERDICT_WAIT` — 调用方 (workflow-runner `wait_recoverable`) 指数退避等满 `wait_timeout_seconds` (1800s) 也不会变。

**真实语料 (2026-07-27 probe; R1 三 agent 勘正 build-aria-runner 行)**:

| 仓库 | workflow | 自动触发 | paths 过滤 |
|------|----------|----------|-----------|
| aria (plugin) | `issue-triage-tests.yml` | push + pull_request | `skills/issue-triage/**` |
| Aria (主仓) | `issue-triage-tests.yml` | push (branches+paths) + pull_request (paths) | `aria/skills/issue-triage/**` |
| Aria (主仓) | `build-aria-runner.yaml` | **workflow_dispatch + push (branches: [feature/aria-2.0-m0-prerequisite], paths)** | `aria-orchestrator/docker/aria-runner/**` |
| Aria (主仓) | `submodule-gate-tripwire.yml` | ❌ 仅 workflow_dispatch (deprecated; schedule 被注释) | n/a |

⇒ 两仓中**绝大多数变更** (state-scanner / session-closer / tdd-enforcer / 文档 / 版本文件) 零 CI run, C.2.4 恒 `wait`。语料同时给出评估器必须正确处理的三种触发形态: 纯 paths 过滤 (aria 仓) / branches+paths 组合 (主仓 issue-triage, build-aria-runner) / 纯 dispatch (tripwire)。

**复发史 (历史口径共 5 次)**: v1.54.0 / v1.55.0 / v1.55.2 / v1.64.0(#113, owner 一次性 ratify) / v1.64.1 (2026-07-26, 新规后特批第 2 次) — 每次都消耗人工现场裁决。owner 2026-07-25 复议已认定: 把 verdict=wait 当 skip 是 Rule #10 反模式, 真解法只有把「无覆盖」从「pending」里分出来。

**为什么恒红是伤害**: 假绿的反面是恒红, 同样零信息量 — 永远返回 wait 的闸门会被学会忽略, 对真 pending / 真 failing 也失去拦截力。`ci_backends: []` 糊不过去 (对所有变更跳过闸门, 含真有覆盖的路径; `_not_ci_backends_empty` 已留痕)。

---

## What Changes

**核心原则 (D2, R1 按 CR-2/TL-2/BA-4 重写): fail-toward-covered 是「行为」承诺 — 任何不确定, gate 行为一律退回与现状逐字段一致 (正常查询→wait); `not_applicable` 只在高置信「零 workflow 会为本变更自动触发」时产生。`decision` 字面值按失败层级分两档 (见 §1 判定全分割), 两档 gate 行为均=现状。绝不把「解析不了」当「无覆盖」; 同时「评估失败」不得静默 (D9 可观测性义务)。**

### 0. 执行上下文契约 (R1 TL-1/BA-2 新增, Critical 修复)

- **仓根 = 评估进程 cwd 的 `git rev-parse --show-toplevel`**。调用方契约: **在执行 C.2 合并的目标仓根内调用** — 子模块本地合并 (约束 1 场景) 时 cwd = 子模块根 (dogfood 即 aria/), 主仓 PR 时 cwd = 主仓根。SKILL.md §C.2.4 执行流程写明此契约 (既有 `--config-file .aria/config.json` 相对路径已隐含同一契约, 本 spec 把它成文)。
- **`main_branch` 不依赖默认值**: 评估必须使用调用方显式传入的 `--main-branch` 真值 (本项目为 `master`; `pre_merge_gate.py` CLI default="main" 仅为向后兼容保留)。main ref 不存在 → `git diff` 失败 → `unknown`, reason=`git-diff-failed: <stderr 摘要>` — 与「diff 成功但空」(reason=`empty-diff`, 判 covered, 见 §1) 是**不同 reason, 可辨**。
- **gitlink-only diff 语义 (成文, 非巧合)**: 主仓评估时 submodule bump 在 `git diff --name-only` 输出为 gitlink 路径单 token (如 `aria`), 按普通路径参与 glob 匹配 — 与 forgejo/GHA 对 gitlink 变更的 paths 匹配行为一致 (gitlink 不展开为子路径)。SC-19 锁定。
- **rename 策略 (QA-6)**: `git diff` 调用显式加 `--no-renames` — rename 呈现为 delete(旧路径) + add(新路径) 两条, changed_files 同时含两侧, 「从覆盖路径重命名移出」保守地保持 covered。SC-18 锁定。
- **非浅克隆前提 (BA-9)**: 评估假定本地为完整 clone (gate 运行环境 = agent 本地开发仓, 非 CI runner); shallow 导致 merge-base 失败 → 落 `git-diff-failed` → unknown, 不误判。

### 1. 新增 `scripts/path_coverage.py` — workflow 触发覆盖评估器 (stdlib-only)

- **发现**: 仓根 `.forgejo/workflows/` + `.gitea/workflows/` + `.github/workflows/` 下 `*.yml` / `*.yaml`。
- **触发子集解析** (手写最小 parser, 不引 PyYAML — stdlib-only 硬约束, 先例 `custom_checks.py` minimal parser + `lib/detailed_tasks.py`): 只解析 `on:` 块的 `push` / `pull_request` 两类自动触发及其 `paths:` 列表 (块映射 + block list / flow list 两形)。
  - `on: push` 标量形 / `on: [push, pull_request]` 列表形 = 该触发**无 paths 过滤** → 该 workflow `covered` (D6);
  - **块映射形 + paths 子块是本仓 4 份语料的全部形态** (BA-9), 单独 SC-20 锁定 (不只靠语料测试隐式兜底);
  - **push 与 pull_request 逐触发独立判定, 任一会触发即该 workflow covered (OR 语义, QA-4)** — 两者 paths 不一致时不得只看其一。SC-17 双向锁定;
  - 「零覆盖贡献」触发键 = **精确白名单 {`workflow_dispatch`, `schedule`} 两键** (D7, 语料: tripwire); **其余任何未建模顶层触发键 (`pull_request_target` / `repository_dispatch` / `workflow_call` 等) 一律按未建模构造 → 该 workflow `covered`** (R2-C1 — 与 glob 未建模语法同一 fail 方向: `pull_request_target` 是真自动触发, 按字面归零贡献会产生假 not_applicable; SC-25 钉死); **混合触发** workflow (如 build-aria-runner: dispatch + push) 仅自动触发臂参与判定;
  - `paths-ignore` 在场 / anchors / 其他无法辨识的**构造级**内容 → 该 workflow 记 `covered` (per-workflow 级不确定, D2);
  - `branches` 过滤**不建模** — 只会减少触发, 不建模方向落 covered, 行为不劣于现状 (语料正例: build-aria-runner 的 branches+paths, 按 paths 交集判)。
- **glob 匹配**: 自研 matcher, `**` (跨目录) / `*` (单段) / `?` 语义对齐 forgejo/GHA paths 规则 (SC-14 表驱动, **期望值来源标注 forgejo 官方 paths 文档条目**, TL-7); **对任何未建模 glob 语法片段 (字符类 `[abc]` / 否定 `!` / 其他) 一律判定为「匹配」→ 该 workflow covered** (BA-1, matcher 层的 fail 方向显式钉死; SC-14 含字符类/否定用例); 大小写敏感 (QA-8, SC-14 含不匹配用例)。
- **changed files**: `git diff --name-only --no-renames <main_branch>...<pr_branch>` (merge-base 三点, §0 契约)。
- **判定 (全分割, 互斥+全覆盖 — R2 修正: 规则序 = 数据依赖执行序; reason 字面值全封闭, R2 四方交叉命中 [TL-Major-1 / BA-R2-M1 / QA-9 / CR-N-1])**:
  1. `git diff` 失败 (含 main ref 缺失 / 非 repo / shallow 缺 merge-base) → 整体 `unknown`, reason=`git-diff-failed: <stderr 摘要>`;
  2. diff 成功但输出为空 → 整体 `covered`, reason=`empty-diff` (异常形态, 保守);
  3. changed_files 中**任一条位于三个 workflows 目录下** → 整体 `covered`, reason=`workflow-files-changed` (D10 硬规则: 对 CI 配置本身动刀的 PR 永不 not_applicable);
  4. workflow 文件枚举: **零 workflow 文件 → `not_applicable`, reason=`no-workflow-files`** — **循环前置短路, 不进入规则 5** (消除规则 8 旧版全称谓词在空集上的空真重叠);
  5. 逐 workflow 解析: 解析成功 → 判触发 (covered / 零贡献); 文件读取或 YAML 结构解析失败 → 记 `parse_failed`;
  6. 任一解析成功的 workflow 判 covered → 整体 `covered`, reason=`workflow-trigger-matched` (+ `matched_workflows` 列全; **covered 优先于 parse_failed 的存在** — 已证明真实覆盖是更强信号, BA-4);
  7. 无 covered ∧ 存在 `parse_failed` → 整体 `unknown`, reason=`workflow-parse-failed: <files>`;
  8. 无 covered ∧ 全部解析成功 (此时必有 ≥1 个 workflow, 由规则 4 保证) ∧ 全部判不触发 → `not_applicable`, reason=`no-triggering-paths` (与规则 4 语义区分:「有 workflow 但都不命中」vs「压根没 workflow」)。
  规则 1-8 互斥且穷尽; **此序即数据依赖执行序** (diff 先行 → diff 结果三分 [规则 1/2/3] → 文件枚举短路 [规则 4] → 解析与聚合 [规则 5-8]), 可直译为 if/elif 实现 (QA-11); 8 条规则中**产生终态判定的 7 条** (规则 5 为中间处理步骤, 不产终态 reason) 的 reason 字面值构成**封闭集** (`git-diff-failed` / `empty-diff` / `workflow-files-changed` / `no-workflow-files` / `workflow-trigger-matched` / `workflow-parse-failed` / `no-triggering-paths`), 全部可断言 (QA-9/BA-R2-M1; 计数措辞 R3-N1 勘正)。
- **返回契约**: `{"decision": "covered"|"not_applicable"|"unknown", "workflows_scanned": int, "matched_workflows": [str] (相对仓根的 workflow 文件路径, QA-7), "changed_files_count": int, "reason": str}`。永不 raise (内部全捕获 → unknown + reason)。

### 2. `gate_check()` 集成 (`pre_merge_gate.py`)

评估点: backend 解析成功 + precheck 通过之后、**(a) PR CI 查询之前; (b) main in-flight 查询保持无条件执行, 顺序仍 (b) 先 (a) 后** (TL-6 — 与代码真实 query 顺序 :317→:330 一致表述)。**集成符号 (QA-12)**: 评估器以模块级函数 `evaluate_path_coverage` 挂在 `pre_merge_gate.py` 命名空间 (镜像 `resolve_ci_backend` 可 mock 先例), SC-9/10/21/22 的测试骨架统一 `mock.patch.object(gate, "evaluate_path_coverage", ...)`。

- `decision == "not_applicable"` → **跳过 (a) PR CI 查询与其 wait** (实现须保证 `backend.query_pr_ci` 不被调用, SC-9/10 以 `assert_not_called` 钉死, QA-2); `pr_ci_status = "not_applicable"`; **(b) 照跑不减** (D3 — SilkNode PR-321 事故是 (b) 轴, 正交不放松);
- `compute_verdict` 扩展: 写**显式** `elif pr_ci_status == "not_applicable":` 分支 (BA-8 — 不依赖现有 fallthrough 隐式兜底, 防未来改兜底逻辑时悄悄改变语义): in-flight 空 → `green` (raw_message 留痕); in-flight 非空 → `wait` (仅 (b) 轴驱动, message 指明);
- **NIE 交叉不变量 (TL-4)**: not_applicable 只免 (a); stub backend 的 NIE 经 (b) 查询照常 propagate (abort), 不被 not_applicable 掩盖。「(b) 无条件先跑」这一正交性前提锁进测试 (SC-21);
- `covered` / `unknown` → gate 输出**既有字段逐字段不变** + additive `path_coverage` 键 (CR-5 口径; SC-11 断言口径=既有字段; 承认行为面增量: covered 路径每次 gate 新增 1 次 git diff subprocess + workflow 文件 IO);
- no-backend (`no_ci_fallback`) / `enabled:false` / `ci_backends:[]` / NIE-propagation 各路径**全部不变** (正交 — 评估只在 backend 可用臂内发生);
- gate_check docstring 「matches current Aether subprocess invocation count」同步更新 (BA-7 — not_applicable 使 (a) 调用数条件化)。

### 3. Output schema (additive-only)

- `pr_ci_status` 增值 `"not_applicable"` (gate 侧产生, **backend `CIStatus` Literal 不动** — 该态从不来自 backend 查询, D1);
- 新增顶层 `path_coverage` object (§1 返回契约原样)。**键出现范围 (BA-6)**: 仅在「评估已执行且流程走到 `compute_verdict` 最终路径」的输出携带; backend-query-failure 早退分支 / precheck 失败 / no-backend / enabled:false 输出保持既有六键不变。`_build_output` 增可选参数 (Impact 表列入);
- SKILL.md Output schema 行改写时一并处置预存漂移: 注明 `not_found` 来自 backend `CIStatus` 层、`not_applicable` 来自 gate 层 (CR-6)。

### 4. Config (additive)

`phase_c_integrator.pre_merge_gate.path_coverage_enabled`: bool, **默认 `true`** (D4; 扁平键名 — namespace 内不嵌套是本仓惯例, KM-8)。默认值锁定测试 (SC-12)。**既有 62 测试隔离方法论 (QA-3)**: Phase B 统一给既有 GateCheckTests/FallbackTests mock path_coverage 评估器入口 (不改测试语义), 并新增卫生断言 SC-22「既有套件运行期间零真实 git 子进程」。

### 5. 可观测性义务 (D8+D9, R1 BA-5 扩展)

- `not_applicable` → AI 必须在 workflow report surface 警告行:「C.2.4: 变更路径无 CI workflow 覆盖, PR CI wait 已跳过 (not_applicable), main in-flight 已核」;
- **`unknown` 同样进 surface 面 (D9)**: 警告行含 reason (`git-diff-failed` / `workflow-parse-failed`),「评估失败, gate 已按 covered 现状行为处理」 — 防评估器自身静默失效 (与本 spec 批评的「零信息量→被忽略」同病, 不能换个位置复发);
- 两义务写入 SKILL.md §C.2.4 指令面。

### 6. SKILL.md 同步清单 (KM-1/2/3 修正, 逐处点名不数数)

phase-c-integrator/SKILL.md:
- `:39-53` 顶部总览配置表 (KM-3) — 增 `path_coverage_enabled` 行;
- `:176` 紧凑 YAML 预览块 `pr_ci_status` 枚举 (KM-2 — 历史上从不随详细版同步, 显式点名);
- 执行流程插「2.5 Path coverage 评估 (v1.65.0+)」(KM-7 版本标注) + §0 执行上下文契约;
- `:241-245` verdict 计算 (bullet list, CR-3 措辞) 增 not_applicable 两行;
- `:246-249` 路由决策 + D8/D9 surface 义务;
- `:258-270` Output schema (含 CR-6 漂移处置);
- `:272-281` §C.2.4 内配置参数表;
- `:283-289` 降级行为 (补 fail-toward-covered 边界与判定全分割摘要)。

`aria/skills/config-loader/SKILL.md:241-281` (KM-1, 第二权威 config schema 登记, CR-N-3 范围勘正至 `user_escape_hatch` 末条): 增 `path_coverage_enabled` 条目 (type: boolean, default: true, v1.65.0+ 注记)。

`aria/skills/workflow-runner/references/workflow-state-schema.md:125` (KM-10): `raw_message` 字段说明补注「v1.65.0+ 起 not_applicable/unknown 态的 path_coverage 提示文案也经此字段传递, 非仅 fail」(gate_state.status 三态不变, 无结构性同步)。

### 7. 主仓 `.aria/config.json` 注释退役 + DEC 存档 (Phase D, 主仓侧; R1 TL-5/KM-5/KM-6 重写)

- **先存档后改写 (KM-5)**: 改 `_lane` 之前, 把 2026-07-25 owner 裁决全文抽取存 `docs/decisions/DEC-2026MMDD-NNN-*.md` (canonical 目录, 近期命名惯例), `_lane` 改写后留指针;
- **co-land 硬时序 (TL-5)**: `_lane` 过渡规则 (2) 的退役编辑必须与「主仓 gitlink bump 到含 not_applicable 机制的 v1.65.0」**同一个主仓 commit** 落地 — 消除「规则已退、pinned 子模块无机制」的裸奔窗口;
- **三注释字段同批处置 (KM-6)**: `_comment` (现状陈述改写) / `_lane` (退役+指针) / `_not_ci_backends_empty` (前瞻引用改「已实现」过去时); `_open_question_no_ci_fallback` 保持挂起 (非目标);
- 改写稿须 owner 过目 (它是 owner 的裁决记录)。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| D1 | 评估落 gate 侧, 非 backend 侧 | backend-agnostic; `CIStatus` Literal 不动 (代码级已核: not_applicable 从不来自 backend) |
| D2 | fail-toward-covered = 行为承诺; decision 字面分两档 | **构造级**不确定 (可读 YAML 但含不建模特性) → 该 workflow covered; **解析失败** (读不了/YAML 坏) → per-workflow 记 parse_failed → 聚合无 covered 时整体 unknown (TL-Minor-3 二分); 两档 gate 行为均=现状 (CR-2 重写) |
| D3 | (b) 轴不免除 | not_applicable 只跳 (a); NIE 经 (b) 照常 propagate (SC-21) |
| D4 | `path_coverage_enabled` 默认 true | owner sign-off 单独点名此项 (TL-8); SC-12 锁定; 既有测试隔离 SC-22 |
| D5 | stdlib-only 手写触发子集 parser | 语料 = 本仓 4 真实 workflow (含三种触发形态) + GHA 文档形态 |
| D6 | 无 paths 的 push/pull_request → covered | 标量/列表/块映射三形; 块映射+paths 单独 SC-20 |
| D7 | 零覆盖贡献 = 精确白名单 {workflow_dispatch, schedule} | 其余未建模触发键 (pull_request_target 等) → covered (R2-C1); 纯 dispatch 语料 = tripwire (唯一); 混合触发仅自动臂参与 (build-aria-runner 正例, TL-3 勘正) |
| D8 | not_applicable 双留痕 + AI surface 义务 | raw_message + path_coverage field + SKILL.md 指令警告行 |
| D9 | unknown 同样 surface (BA-5) | 评估器自身失效必须可见, reason 可辨 (TL-1c) |
| D10 | workflow 文件自身变更 → 强制 covered (QA-1) | 判定规则 3 (diff 层最先的语义规则); 对 CI 配置动刀的 PR 永不 not_applicable |
| D11 | 执行上下文成文 (TL-1/BA-2) | cwd=目标仓根 + main_branch 显式传值 + gitlink 语义 + --no-renames + 非浅克隆前提 |

**Rule #6 (rule6_note)**: SKILL.md §C.2.4 为**处方性·运行时指令面** (新增 verdict 分支的 AI 处理指令 + surface 义务) → 判据决策表第二行, **照跑 AB** (phase-c-integrator: ab-suite 3 selected evals [source 5]; `phase-c-integrator-pre-merge-gate.json` 6 fixtures 一并纳入执行面 — 其形态与 SC-2/9/10 天然相关, CR-4), 零裁量。config-loader/SKILL.md 登记条目为描述性 schema 同步 (substitute: 结构化测试)。确定性代码层 (path_coverage.py / pre_merge_gate.py) 由 SC-1~28 结构化测试覆盖 (计数经 CR-N-2 / QA-14 两轮勘正), 与 AB 并行不互替。

**Rule #8 自指说明**: 本 cycle 自身的 C.2 合并 (aria 子模块内, cwd=aria/, 变更路径 `skills/phase-c-integrator/**`, aria 仓唯一 workflow paths=`skills/issue-triage/**` 零交集) 即 not_applicable 的**首个生产用例** — 实现完成后用新机制走正门, meta-dogfood。若新机制对自身产出非预期判定, 即为发版前最后一道真实性检验。注意 §0 契约: 评估发生在 aria 子模块根, 非主仓根 (BA-2 双树歧义在 dogfood 场景的正确侧)。

---

## Success Criteria (SC, 全部可测)

| SC | 场景 | 期望 |
|----|------|------|
| SC-1 | 零 workflow 文件 | `not_applicable`, reason=`no-workflow-files` (规则 4 前置短路产出) |
| SC-2 | aria 仓真实语料回归 (issue-triage paths workflow + 变更 `skills/run_all_tests.sh`) | `not_applicable`, reason=`no-triggering-paths` (复发形态钉死) |
| SC-3 | 变更含 `skills/issue-triage/x.py` | `covered`, reason=`workflow-trigger-matched`, matched_workflows 含该 workflow 路径 |
| SC-4 | push 无 paths 过滤 (块映射形) | `covered`, reason=`workflow-trigger-matched` |
| SC-5 | `on: [push]` 列表形 / `on: push` 标量形 | `covered`, reason=`workflow-trigger-matched` |
| SC-6 | `paths-ignore` 在场 | `covered` (per-workflow 档) |
| SC-7 | 全部 workflow 畸形 YAML (构造) | `unknown`, reason=`workflow-parse-failed` → gate 行为=现状 |
| SC-8 | git diff 失败 (ref 不存在 / 非 repo) | `unknown`, reason=`git-diff-failed` → gate 行为=现状 |
| SC-9 | not_applicable ∧ main in-flight 非空 | `verdict=wait` + **`query_pr_ci.assert_not_called()`** |
| SC-10 | not_applicable ∧ in-flight 空 | `verdict=green` + raw_message 非空 + `path_coverage` 在场 + **`query_pr_ci.assert_not_called()`** |
| SC-11 | covered / unknown | 既有字段逐字段回归 (断言口径=既有六键; 既有 62 tests 全绿) |
| SC-12 | config 无 `path_coverage_enabled` | 评估执行 (默认 true 锁定) |
| SC-13 | `path_coverage_enabled: false` | 评估不执行, 输出无 `path_coverage` 键, 现行为 |
| SC-14 | glob 表驱动: `**` / 尾 `/**` / `*` 单段 / `?` / **字符类 `[abc]` → 判匹配** / **`!` 前缀 → 判匹配** / **大小写不匹配用例** | 期望值来源标注 forgejo 官方 paths 文档 |
| SC-15 | Output schema | 老键全保留 (additive-only); 早退分支不带 `path_coverage` 键 |
| SC-16 | PR 仅修改 workflow 文件自身 (真实语料: `.forgejo/workflows/issue-triage-tests.yml`) | `covered`, reason=`workflow-files-changed` |
| SC-17 | push 无 paths + pull_request 有 paths (及反向) | OR 语义: 任一触发即 covered |
| SC-18 | 文件从覆盖路径 rename 移出 / 移入 (`--no-renames` 下) | 新旧路径都进 changed_files → covered |
| SC-19 | 主仓语境 gitlink-only bump (changed_files=[`aria`]) + 主仓 3-workflow 真实语料 | **`not_applicable`, reason=`no-triggering-paths`, matched_workflows=[]** (gitlink 单 token 对主仓 workflow 的 `aria/skills/issue-triage/**` 与 `aria-orchestrator/docker/aria-runner/**` 均不命中, CR-N-4 勘正语料归属; QA-10 钉死终态; 补充正证 fixture: 合成 paths 含 `aria` 精确 token 的 workflow → `covered`, 验证 gitlink 按不透明单段路径参与匹配不展开) |
| SC-20 | 块映射形 + paths 子块 (本仓语料全部形态), 双子用例 (QA-9-residual 具体化) | (a) changed_files 命中 paths → `covered`, reason=`workflow-trigger-matched`; (b) 不命中 (单 workflow 语料) → `not_applicable`, reason=`no-triggering-paths` |
| SC-21 | not_applicable ∧ stub backend (query 抛 NIE) | gate 仍 raise NIE ((b) 无条件先跑, 不被 not_applicable 吞) |
| SC-22 | 既有 GateCheckTests/FallbackTests 套件运行 | 零真实 git 子进程 (评估器入口被 mock, 卫生断言) |
| SC-23 | 主仓 3 workflow 联合语料 (branches+paths / dispatch+push 混合 / 纯 dispatch) + 变更 `docs/x.md` | `not_applicable`, reason=`no-triggering-paths`; 同语料 + 变更 `aria-orchestrator/docker/aria-runner/Dockerfile` → `covered`, reason=`workflow-trigger-matched` (QA-5, D5 语料承诺兑现) |
| SC-24 | 一 workflow covered ∧ 另一 workflow 解析失败 (混合) | 整体 `covered`, reason=`workflow-trigger-matched` (规则 6 优先级, BA-4) |
| SC-25 | 仅 `pull_request_target` 触发的 workflow (手造 fixture) + 任意变更 | 该 workflow `covered` (未建模自动触发键白名单方向, R2-C1) |
| SC-26 | 在主仓根对子模块分支名评估 (该 ref 不存在于主仓) | `unknown`, reason=`git-diff-failed` (BA-2 残留负向用例: cwd 错仓的自然安全网) |
| SC-27 | cwd 位于仓内子目录 | 仍以 `git rev-parse --show-toplevel` 定仓根扫描 workflows (D11 机制锁定) |
| SC-28 | diff 成功但输出为空 (changed_files=[]) | `covered`, reason=`empty-diff` (规则 2 覆盖行, QA-14 — 封闭集与测试矩阵满射) |

---

## 非目标

- **不动 `no_ci_fallback` 政策** (`_open_question_no_ci_fallback` 归 owner, 正交);
- 不实现 GitHub Actions backend 真查询 (stub 现状不变);
- 不建模 `branches` 过滤 (conservative 方向已论证, 语料正例锁定);
- 不消除 gate→merge race window (SKILL.md :291 现状声明不变);
- 不动 workflow-runner `wait_recoverable` 机制本身 (not_applicable 在 gate 内消化, 不产生 wait)。

---

## Impact

| 文件 | 变更 |
|------|------|
| `skills/phase-c-integrator/scripts/path_coverage.py` | **新增** (评估器; §0 契约 + §1 全分割判定) |
| `skills/phase-c-integrator/scripts/pre_merge_gate.py` | `gate_check` 插评估点 + docstring 更新 (BA-7) / `compute_verdict` 显式分支 (BA-8) / `_build_output` 增可选参数 (BA-6) / `DEFAULT_CONFIG` 增键 |
| `skills/phase-c-integrator/tests/test_path_coverage.py` | **新增** (SC-1~8, 14, 16~20, 23~28; fixture 用独立 tempdir 非 repo.parent — memory `feedback_test_worktree_fixture_isolated_tmpdir`, QA-13) |
| `skills/phase-c-integrator/tests/test_pre_merge_gate.py` | 扩展 (SC-9~13, 15, 21~22) |
| `skills/phase-c-integrator/SKILL.md` | §6 清单逐处 (含 :39-53 总览表 + :176 紧凑块) → Rule #6 照跑 AB |
| `aria/skills/config-loader/SKILL.md` | :241-281 登记 `path_coverage_enabled` (KM-1) |
| `aria/skills/workflow-runner/references/workflow-state-schema.md` | :125 `raw_message` 用途补注 (KM-10) |
| 发版 5 文件 + 主仓 gitlink | v1.65.0 MINOR |
| 主仓 `docs/decisions/DEC-*` | **新增** 2026-07-25 裁决存档 (KM-5, 先于 `_lane` 改写) |
| 主仓 `.aria/config.json` | `_comment`/`_lane`/`_not_ci_backends_empty` 三字段退役改写, **与 gitlink bump 同 commit co-land** (TL-5/KM-6) |

测试基线: phase-c 62 → 预计 ~110+; 全量跨 skill 套件须绿 (`run_all_tests.sh`)。
