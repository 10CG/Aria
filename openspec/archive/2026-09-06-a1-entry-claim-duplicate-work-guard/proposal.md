---
unverified_claims:
  - claim: "SC-24 / SC-33 / SC-25 代码臂 / SC-10 (CLI 全链路): `unknown_schema_claims` 计数且不入 overlap[] / `read_claims` 抛异常 ⇒ 双 `null` + error 非空 / overlap 抛异常 ⇒ `null` + error / fetch 降级 ⇒ `error == \"fetch_degraded\"` (四条 baseline 必红) — ✅ **2026-09-05**: 同文件加四组类 (SC-24 计数与不混入 overlap / SC-33 双 null + error / SC-25 null≠[] / SC-10 降级) + 四态可辨。**注入手段实测后钉 (c)**: Spec 列的 (a)「把 ref 指向非 tree 对象」**结构上做不到** —— `read_claims` 通篇 fail-soft, 损坏 ref 只得 `errors=['ls_tree_failed:fatal: not a tree object']` 而从不抛, 触不到 `except`; (b) 影子化 `lib` 单模块须重导出其余, 脆。钉 (c) = 子进程内模块边界替换, 且**按调用方栈帧限定** (`read_claims` 也被闸门自身 `_run_gate_impl:512` 调用, 无差别替换会把闸门打崩, 实跑一次即暴露 rc=1)。**五个坏实现负控全部实跑变红**: 删自排除 / include_terminal 跳过全部门 / 门控丢 `--linked-issue` / except 只赋 overlap / except 退回写 `[]`"
    reason: "symbol 'unknown_schema_claims' unclassified reference form"
    symbols: ["unknown_schema_claims"]
  - claim: "第一处变更 ①②③④⑥: `--include-terminal` flag / `_main()` 调用处加关键字参数 / 门控放宽为 `if args.linked_issue or args.include_terminal:` + `read_claims` 只调一次 + `unknown_schema_claims` 键 / `except` 改写 `linked_issue_overlap = None` + `linked_issue_overlap_error` + `unknown_schema_claims = None` — ✅ **2026-09-05**: ①②③④⑥ 全落 + `:1154` 契约注释同步。三处 def 签名未触及, except 内字面 `= []` 零命中, 不传两 flag 时 stdout 键集与基线**逐项相同** (11 键实测比对)。**⚠️ 本任务 deliverable 与 SC-33 直接矛盾, 按 proposal 实现**: yaml 写「`linked_issue_overlap=None` **仅当传了 `--linked-issue`**」, 而 proposal `:623` 的 SC-33 明写「带 `--include-terminal` **不带** `--linked-issue` ⇒ 两键都 null」, Impact ④⑥ (`:663`) 亦为无条件「同一 except 分支须同时赋」; §2.4b 四态表 (`:340`) 进一步钉死「键缺席 = 未传 `--linked-issue`, **与是否传 `--include-terminal` 无关**」。⇒ 成功路径按各自 flag 填、异常路径无条件双 null。那句条件式是 A.2/A.3 派生时引入的错 (memory `derived-instruction-outranks-spec`)"
    reason: "symbol 'unknown_schema_claims' unclassified reference form"
    symbols: ["unknown_schema_claims"]
  - claim: "第一处变更 ①②③④⑥: `--include-terminal` flag / `_main()` 调用处加关键字参数 / 门控放宽为 `if args.linked_issue or args.include_terminal:` + `read_claims` 只调一次 + `unknown_schema_claims` 键 / `except` 改写 `linked_issue_overlap = None` + `linked_issue_overlap_error` + `unknown_schema_claims = None` — ✅ **2026-09-05**: ①②③④⑥ 全落 + `:1154` 契约注释同步。三处 def 签名未触及, except 内字面 `= []` 零命中, 不传两 flag 时 stdout 键集与基线**逐项相同** (11 键实测比对)。**⚠️ 本任务 deliverable 与 SC-33 直接矛盾, 按 proposal 实现**: yaml 写「`linked_issue_overlap=None` **仅当传了 `--linked-issue`**」, 而 proposal `:623` 的 SC-33 明写「带 `--include-terminal` **不带** `--linked-issue` ⇒ 两键都 null」, Impact ④⑥ (`:663`) 亦为无条件「同一 except 分支须同时赋」; §2.4b 四态表 (`:340`) 进一步钉死「键缺席 = 未传 `--linked-issue`, **与是否传 `--include-terminal` 无关**」。⇒ 成功路径按各自 flag 填、异常路径无条件双 null。那句条件式是 A.2/A.3 派生时引入的错 (memory `derived-instruction-outranks-spec`)"
    reason: "symbol 'linked_issue_overlap_error' unclassified reference form"
    symbols: ["linked_issue_overlap_error"]
  - claim: "第二处变更 ⑦ + `--heartbeat-only` 模式: `--raw-track-id` `required=False` + `_main()` 模式校验; 三级回落由编排层传入, CLI 不推断; 按 `(container, 归一 track_id)` 刷全部匹配 active claim; 遥测 `_source=\"heartbeat\"` + `outcome ∈ {refreshed, skipped_no_track, skipped_disabled, error}`; 不写 claim / 不判碰撞 / 不自带 fetch; `coordination_probe.py` 口径注释 — ✅ **2026-09-05**: ⑦ `required=False` + `_main()` 模式校验 (落法 (a), 不用 subparsers); `--heartbeat-only` 模式经 `heartbeat_by_track` 刷全部匹配 active; 遥测独立 `source=\"heartbeat\"` 分区 + `outcome ∈ {refreshed, skipped_no_track, error}`; push 复用 `resilient_push` 且受同一 `no_push` 门。verification 逐条实测: heartbeat 分支对 `health_check_fetch`/`acquire_claim`/`reconcile` 各 **0** 次调用 (不自带 fetch/不认领/不判碰撞) · `--heartbeat-only` 缺 `--phase` 仍被拒 · `--phase B` 缺 carry-id 仍 `parser.error` exit 2 · **空串 `--raw-track-id` 在 `derive_track_id` 之前短路** (`track_id: null` + `skipped_no_track`), R6 担心的「空串被归一成 sha256 去刷错 track」结构上不可能发生 · `coordination_probe.py` diff 仅注释行, `test_coordination_probe_cli.sh` 通过 · `test_phase1_gate_telemetry.py` 13 测试全绿 (production 分区不可被 heartbeat 写入)"
    reason: "symbol 'skipped_no_track' unclassified reference form"
    symbols: ["skipped_no_track"]
  - claim: "`phase-a-planner/SKILL.md`: frontmatter `:9` `allowed-tools` 加 `Bash, AskUserQuestion` + 独立标题级 `### 前置: REQUIRE claim (A.1, MUST)` 块 (放 `### 步骤执行` `:60` 之前; 七字面量 + 完整命令行 + 幂等谓词 + `--linked-issue` 两阶段取法含 `--emit-arg`) + A.1 YAML 项 (`:63`) 首键 `precondition:` 指针 (**委派动作行 = `:64` `skill: spec-drafter` / `:68-70` `action:`; `skip_if: complexity: Level1` = `:67`**, `:763-766` 待办 (2)) + §2.3 按 status 分档选项集 + §5.2 release 义务 + `coordination.enabled`/Level 1 零调用 + `unattended` 分支 — ✅ **2026-09-05**: frontmatter `:9` 逐字 = `allowed-tools: Read, Write, Glob, Grep, Task, Skill, Bash, AskUserQuestion`; `### 前置: REQUIRE claim (A.1, MUST)` 插在 `### 步骤执行` 之前 (切片 68 行, 内含七字面量 / 完整命令行 / 幂等谓词逐字 / 四态表含 `未能核实` / §2.3 按 status 分档选项集含「不要提议释放对方 claim」/ 退出义务两条 / skip 三条); A.1 YAML 项首键插 `precondition:` 指针。**④ 实测切片内不含 `--phase B`**"
    reason: "symbol 'unattended' unclassified reference form"
    symbols: ["unattended"]
  - claim: "`state-scanner/SKILL.md`: Layer L 段 (`:143-178`) 新增「Layer L A.1 heartbeat 集成」四句小节 (触发条件 / `--heartbeat-only` 完整命令行 / fail-soft / 指针) + `:168` 键集补 `push_skipped` / `push_skipped_reason` + `:176` 消费契约同步四态 (`list | null | 缺席`); 同批同步 `lib/constants.py:43-44` / `:50` 注释 (前提消失) — ✅ **2026-09-05**: `### Layer L A.1 heartbeat 集成` 四句 + 完整命令行 (与 layer-l 设计段**逐字节相同**, 已实测); `:168` 键集补 `push_skipped`/`push_skipped_reason`/`linked_issue_overlap_error`/`unknown_schema_claims`; 消费契约补三态 (缺席/[]/null+error) 与「不得用 `.get(key, [])` 读」。`constants.py` 的「NO production heartbeat loop exists」改写为落地后事实, **`STALE_TTL`/`SWEEP_TTL`/`HEARTBEAT_INTERVAL` 取值与不变量注释一律未动**"
    reason: "symbol 'push_skipped' unclassified reference form"
    symbols: ["push_skipped"]
  - claim: "`state-scanner/SKILL.md`: Layer L 段 (`:143-178`) 新增「Layer L A.1 heartbeat 集成」四句小节 (触发条件 / `--heartbeat-only` 完整命令行 / fail-soft / 指针) + `:168` 键集补 `push_skipped` / `push_skipped_reason` + `:176` 消费契约同步四态 (`list | null | 缺席`); 同批同步 `lib/constants.py:43-44` / `:50` 注释 (前提消失) — ✅ **2026-09-05**: `### Layer L A.1 heartbeat 集成` 四句 + 完整命令行 (与 layer-l 设计段**逐字节相同**, 已实测); `:168` 键集补 `push_skipped`/`push_skipped_reason`/`linked_issue_overlap_error`/`unknown_schema_claims`; 消费契约补三态 (缺席/[]/null+error) 与「不得用 `.get(key, [])` 读」。`constants.py` 的「NO production heartbeat loop exists」改写为落地后事实, **`STALE_TTL`/`SWEEP_TTL`/`HEARTBEAT_INTERVAL` 取值与不变量注释一律未动**"
    reason: "symbol 'linked_issue_overlap_error' unclassified reference form"
    symbols: ["linked_issue_overlap_error"]
  - claim: "`state-scanner/SKILL.md`: Layer L 段 (`:143-178`) 新增「Layer L A.1 heartbeat 集成」四句小节 (触发条件 / `--heartbeat-only` 完整命令行 / fail-soft / 指针) + `:168` 键集补 `push_skipped` / `push_skipped_reason` + `:176` 消费契约同步四态 (`list | null | 缺席`); 同批同步 `lib/constants.py:43-44` / `:50` 注释 (前提消失) — ✅ **2026-09-05**: `### Layer L A.1 heartbeat 集成` 四句 + 完整命令行 (与 layer-l 设计段**逐字节相同**, 已实测); `:168` 键集补 `push_skipped`/`push_skipped_reason`/`linked_issue_overlap_error`/`unknown_schema_claims`; 消费契约补三态 (缺席/[]/null+error) 与「不得用 `.get(key, [])` 读」。`constants.py` 的「NO production heartbeat loop exists」改写为落地后事实, **`STALE_TTL`/`SWEEP_TTL`/`HEARTBEAT_INTERVAL` 取值与不变量注释一律未动**"
    reason: "symbol 'unknown_schema_claims' unclassified reference form"
    symbols: ["unknown_schema_claims"]
  - claim: "补充 substitute (rule6 #10b + #12): `layer-l-integration.md` 含标题字面 `Layer L A.1 heartbeat 集成` 且该节切片含 `--heartbeat-only` (baseline 必红; 负控 = 标题在、命令行在别节 ⇒ 红); `state-scanner/SKILL.md` `:168` 一带 (`### JSON 消费` 切片) 含字面 `push_skipped` (baseline 必红; 负控 = 写进 `## 相关文档` ⇒ 红) — ✅ **2026-09-05**: layer-l 新节标题 + 切片含 `--heartbeat-only`; state-scanner `### JSON 消费` 切片含 `push_skipped` / `push_skipped_reason`。基线两处均无 ⇒ 红"
    reason: "symbol 'push_skipped' unclassified reference form"
    symbols: ["push_skipped"]
  - claim: "套件缺口 issue: **新开** aria-plugin issue「phase-a-planner / spec-drafter 套件零覆盖 A.1 入口认领编排行为」, 正文交叉引用 `#117` (同族: 处方性 · 套件覆盖外) 与 `#127`, **不归并** (理由见 detailed-tasks.yaml TASK-036 notes) — ✅ **2026-09-06 开单 [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171)** (owner 授权; 依赖 7.5 已于 09-05/06 跑完)。**开单前 fetch 查重** (memory `concurrent_duplicate_audit_fetch_before_start`): 拉全 42 条 open issue 逐条看, 除 Spec 点名的 `#117`/`#127` 外**另发现同族 `#157`** (state-scanner 套件对 Layer L 段零覆盖) —— **不在原 A.2 裁量记述里**; 复核后维持「新开」(宿主套件与 SKILL.md 段均不同: #157 是 state-scanner 套件 × Layer L Phase B 集成段, 本 issue 是 phase-a-planner/spec-drafter 套件 × A.1 REQUIRE-claim 段), 并把三者边界与「若维护者认为应合并, 本 issue 可转评论」写进首段。⚠️ **两处按实测改写而非照抄本文件的 verification**: (a) 本行原写「两套件各 2 eval」—— 实测分支点 `788fac8` 是 phase-a-planner **2** / spec-drafter **4** (#117 的 2/2 是 2026-07-20 时点, 之后 spec-drafter 增至 4, 两处都对只是时点不同); (b) **现状已非 2 条** —— `5697477` 已把 7 条定向 fixture 写进固定套件, 两套件现各 **6** 条, 故 issue 按「落地前零覆盖 / 已做部分补救 / 待做通用维度」三段写。开单后独立 GET 回读核验: 正文 3404 字符, `#117`/`#127`/`#157`/`5697477`/`788fac8`/AB 数字/`unattended`/`v1.71.0` 全部命中 (不信 POST 回执)。"
    reason: "symbol 'concurrent_duplicate_audit_fetch_before_start' unclassified reference form"
    symbols: ["concurrent_duplicate_audit_fetch_before_start"]
  - claim: "套件缺口 issue: **新开** aria-plugin issue「phase-a-planner / spec-drafter 套件零覆盖 A.1 入口认领编排行为」, 正文交叉引用 `#117` (同族: 处方性 · 套件覆盖外) 与 `#127`, **不归并** (理由见 detailed-tasks.yaml TASK-036 notes) — ✅ **2026-09-06 开单 [aria-plugin#171](https://forgejo.10cg.pub/10CG/aria-plugin/issues/171)** (owner 授权; 依赖 7.5 已于 09-05/06 跑完)。**开单前 fetch 查重** (memory `concurrent_duplicate_audit_fetch_before_start`): 拉全 42 条 open issue 逐条看, 除 Spec 点名的 `#117`/`#127` 外**另发现同族 `#157`** (state-scanner 套件对 Layer L 段零覆盖) —— **不在原 A.2 裁量记述里**; 复核后维持「新开」(宿主套件与 SKILL.md 段均不同: #157 是 state-scanner 套件 × Layer L Phase B 集成段, 本 issue 是 phase-a-planner/spec-drafter 套件 × A.1 REQUIRE-claim 段), 并把三者边界与「若维护者认为应合并, 本 issue 可转评论」写进首段。⚠️ **两处按实测改写而非照抄本文件的 verification**: (a) 本行原写「两套件各 2 eval」—— 实测分支点 `788fac8` 是 phase-a-planner **2** / spec-drafter **4** (#117 的 2/2 是 2026-07-20 时点, 之后 spec-drafter 增至 4, 两处都对只是时点不同); (b) **现状已非 2 条** —— `5697477` 已把 7 条定向 fixture 写进固定套件, 两套件现各 **6** 条, 故 issue 按「落地前零覆盖 / 已做部分补救 / 待做通用维度」三段写。开单后独立 GET 回读核验: 正文 3404 字符, `#117`/`#127`/`#157`/`5697477`/`788fac8`/AB 数字/`unattended`/`v1.71.0` 全部命中 (不信 POST 回执)。"
    reason: "symbol 'unattended' unclassified reference form"
    symbols: ["unattended"]
  - claim: "SC-32 + SC-28 第二臂 + argparse 负控 (CLI 全链路): 无 carry-id 跑 `--heartbeat-only --phase A.1 --repo-path` ⇒ 遥测恰一条 `_source=\"heartbeat\"` / `outcome=\"skipped_no_track\"`, 不写 claim 不推远端; `coordination_probe` production 计数不变; 非 heartbeat 模式缺 `--raw-track-id` 仍 `parser.error` (baseline 必红: 模式不存在) — ✅ **2026-09-05**: 新建 `tests/test_heartbeat_only_cli.py` 7 用例 (SC-32 恰一条记录 + 不写 claim + 不推远端 / refreshed 臂 / SC-28 第二臂 production 计数不变 / argparse 负控 / push 三态)。断言对象取 `_telemetry_path(repo, \"heartbeat\")` 的返回值, 对文件名待裁三案免疫。**踩到并记下 memory `ss-two-lib-pkgs` 的一个新变体**: 常见的 `if p not in sys.path: insert(0,p)` 写法在此不可靠 —— `python3 -m unittest` 从 skill root 跑时 cwd 已以绝对路径躺在 `sys.path[0]`, 于是 root 那次插入被守卫跳过、只有 `scripts` 插到最前, 顺序当场反转, 报一个看不出所以然的 `ModuleNotFoundError: No module named 'lib.coordination_ref'`。改用 remove-then-insert (与 `phase1_gate.py:96-108` 的仓内惯例一致)。**三个坏实现负控实跑变红**: 只加 flag 不松 required / 只 `logger.debug` 不落盘 / 心跳写进 production 分区"
    reason: "遥测/运行时-invoke 核验属 fix A (out-of-scope); 静态 C 无法核验 → warn"
    symbols: []
  - claim: "第二处变更 ⑦ + `--heartbeat-only` 模式: `--raw-track-id` `required=False` + `_main()` 模式校验; 三级回落由编排层传入, CLI 不推断; 按 `(container, 归一 track_id)` 刷全部匹配 active claim; 遥测 `_source=\"heartbeat\"` + `outcome ∈ {refreshed, skipped_no_track, skipped_disabled, error}`; 不写 claim / 不判碰撞 / 不自带 fetch; `coordination_probe.py` 口径注释 — ✅ **2026-09-05**: ⑦ `required=False` + `_main()` 模式校验 (落法 (a), 不用 subparsers); `--heartbeat-only` 模式经 `heartbeat_by_track` 刷全部匹配 active; 遥测独立 `source=\"heartbeat\"` 分区 + `outcome ∈ {refreshed, skipped_no_track, error}`; push 复用 `resilient_push` 且受同一 `no_push` 门。verification 逐条实测: heartbeat 分支对 `health_check_fetch`/`acquire_claim`/`reconcile` 各 **0** 次调用 (不自带 fetch/不认领/不判碰撞) · `--heartbeat-only` 缺 `--phase` 仍被拒 · `--phase B` 缺 carry-id 仍 `parser.error` exit 2 · **空串 `--raw-track-id` 在 `derive_track_id` 之前短路** (`track_id: null` + `skipped_no_track`), R6 担心的「空串被归一成 sha256 去刷错 track」结构上不可能发生 · `coordination_probe.py` diff 仅注释行, `test_coordination_probe_cli.sh` 通过 · `test_phase1_gate_telemetry.py` 13 测试全绿 (production 分区不可被 heartbeat 写入)"
    reason: "遥测/运行时-invoke 核验属 fix A (out-of-scope); 静态 C 无法核验 → warn"
    symbols: []
  - claim: "`state-scanner/references/layer-l-integration.md` 四处: `:15` Design A 句同步 A.1 触发点 / `:45` `update_heartbeat()` → `heartbeat()` + caller/节律改真实 / 新增「Layer L A.1 heartbeat 集成」设计段 (三级回落表 / 遥测分区边界 / fail-CLOSED 谓词 `success == true ∧ coordination_ref_present == true` / 完整命令行) — ✅ **2026-09-05**: 四处全落 (Design A 补 A.1 触发点 / `update_heartbeat()` → `heartbeat()`+`heartbeat_by_track()` / caller 与节律改真实 / 新增设计段含三级回落表·遥测分区边界·fail-CLOSED 谓词·degraded 处置·13.8s 代价披露)。⚠️ verification 的「`git grep update_heartbeat aria/` 零命中」**结构上不可满足**: 守卫测试要断言该字面量不在文档里, 自己就必须含有它 —— 现 3 处命中全在 `test_coordination_default_lockin.py` 自身。该条应读作「除 guard 测试自身外零命中」"
    reason: "遥测/运行时-invoke 核验属 fix A (out-of-scope); 静态 C 无法核验 → warn"
    symbols: []
unverified_ack: false
---
# Proposal: a1-entry-claim-duplicate-work-guard

> **Status**: ✅ **Complete (2026-09-06 归档; 40/40)** — 原批准记述见归档前版本: ✅ **Approved (owner 2026-08-30 批准进 A.2/A.3; rework v4.1 — 六项裁定 + R6 后五项裁定已落版; post_spec R1–R6 已跑, 五席 + 复核席一致不再加轮)** — A.2/A.3 产物 `tasks.md` + `detailed-tasks.yaml` (40 tasks; TASK-040 = post_planning R2 补 aria 子模块本地 merge + 双推宿主) 2026-08-30 派生; post_planning (combined 三份) R1→R4 **CONVERGED** 2026-08-31 (R4 5/5 PASS), ready for B.1; 闸门状态「AI 流程判断」#2 (carry-id 选项 A 不算动 Phase B) 仍待 owner 一句话。决策单 `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`; R6 聚合 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md`。
> - **裁定 (2026-08-30, 六项) 已执行** —— 决策单 [`.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`](../../../.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md): **1A** track-id 恒用 `<spec-slug>-<container_uuid>` 单一形态, issue 派生形取消 (§2.1 / §5 / D3 / D18; 两个新字段 `spec_slug`·`track_form`、§5.1 二分谓词、§5.3 三元组 release、D12、SC-1/4/27/30/31 结构性消失, 原文按字节移入审计轨 §6); **2b** 不建派生的代码宿主 (§2.1a); **3b** 收尾走 R6 通用审计 (本 Status 行); **4i** 「AB 评测推生产 ref」单独修 (不入本 Spec, 见 rule6_note 照跑档前提); **5** SC-15 回滚为代码类、SC-2 改写声称对象 (Success Criteria); **6i** 「无关联」哨兵扩为 `{none, 无}` 且字段名改英文 canonical (字段 Spec 承担, 本 Spec 只引用)。R5 五项落版实测 (SC-32/33 未入表 / Impact `fail-CLOSED` 误名 / `compose` 残留 / `gc.py`+`heartbeat` 行) 本轮逐项清账 —— 其中 K1/K2/K4 随 1A 整体消失, 不再需要「回灌」。
> - **裁定 1 已执行**: C2 **(iii) 撤销, 只采 (ii)** —— `STALE_TTL` 维持 `1800` 不改; 四个落点 (SC-20 / Impact 表 `lib/constants.py` 行 / §2.3 残余风险段 / 闸门状态 item 3) 已逐一回撤;
> - **裁定 2 已执行**: 本 Spec 主体**只留 A.1 入口认领 + track-id 契约**。原 §1「关联 Issue」字段可得性/抽取规则 → 拆出 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md); 原 §4 竞品 spec 探针 → 拆出 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)。两份子 Spec 由另外的执笔席并行起草, **均非本 Spec 的阻塞前置** (依赖方向见 §1 / §4 指针段);
> - **R2 三 critical**: C-A 随 §1 迁出; **C-B (连坐 release) 见 §5 + SC-27**, **C-C (carry-id 断链) 见 §2.1b「carry-id 契约」+ SC-23** —— owner 点名必须在此解, 已解;
> - **R1 editlist 残项**: FIX-01…19 的逐条对账见下方「R1-fix editlist 逐条对账」段 (**不写「已全量吸收」**, R2/M-13 零容忍);
> - 前置依赖 `linked-issue-normalization` 已于 2026-08-23 ship (v1.67.0, aria `ca52d1c`), 不再阻塞。
> - R2 聚合: `.aria/audit-reports/post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md` · R1-fix editlist: `.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`。
> **Created**: 2026-07-30 · **重写**: 2026-08-02 · **rework v3 (换人执笔)**: 2026-08-25
> **Spec Level**: 2
> **Linked Issue**: `10CG/Aria#174` — 本 Spec 的立项 issue (「Layer L claim 无法检测跨 track-id 的同源重叠」; 生产 coordination ref 里本轨两条 claim 的 `linked_issue` 即此值 —— R6/KM m2 抓到头部曾写哨兵 `none` 与之不一致, 2026-08-30 订正为真 token)。本 Spec 源自 5 次并发起草事故的直接观察 (§Why)。字段名与哨兵集合按字段 Spec 2026-08-30 的英文 canonical; `关联 Issue` / `无` 仍是合法 alias。
> **代码落点**: `aria/` 子模块; Spec 落主仓 (Rule #5)
> **ship target**: 待定
> **前置依赖**: **[`linked-issue-normalization`](../../archive/2026-08-23-linked-issue-normalization/proposal.md) 已 ship 并归档** (**rework v3 链接订正**: 旧链接 `../linked-issue-normalization/` 在归档后已失效) (**R1 rework 核验订正**: 原文写「v1.66.0 已认领」, 实际以 **v1.67.0** 合并提交 `ca52d1c` 于 **2026-08-23T09:14:07Z** 合入 `origin/master`, 早于本文件本轮修订落盘) —— 前置依赖已满足, 本 Spec 的 overlap 检测可建立在其归一之上; `linked_issue_overlaps` 三参数签名未变 (详见「事实断言逐条实读清单」#16)。**· aria-plugin `--no-push` 修复** (决策单第 4 项; aria 分支 `fix/phase1-gate-no-push` @ `007d355`, **2026-08-30 状态: 未推任何 remote, 非 `origin/master` 祖先**, R6/TL M5 核) —— 它是 rule6_note 六条照跑的硬前提与 Impact 两处描述性 hunk (`phase-b-developer:96-97` 注释 / `state-scanner:168` 键集) 的依据, **须先合入 `origin/master`** (闸门状态表 #7)。

> **📌 本文件只规定「要建什么」。** 「规定是怎么来的」(旧版三轮 + 重写 v2 两轮的审计轨迹 / C2 (iii) 撤销前的落版原文 / 各处**已闭环**的「⚠️ 实读订正 · 请 owner 复议」叙事 / **34 行「事实断言逐条实读清单」核验表**) 已于 rework v3 (2026-08-25) 整体移出至 **[审计轨](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md)** (§1–§5)。
>
> **⚠️ 该审计轨是 append-only 的, 且显式不维护与本文件的一致性。** 二者出现不一致时**以本文件为准**; **不得**因审计轨的历史记述而回改本文件。切分依据: R2 聚合判定「major 17→17 持平, 每轮 fix 引入 ≈ 等量同形缺陷」, 与 memory `audit-trail-not-in-spec` 点名的耦合形状同形; 处方是**切开不重写** —— 搬运按字节, 未改写任何一句。
>
> **⚠️ 本次切分是执笔侧的流程判断, 不是 owner 裁定** (rework v3 说明书 D-J 已标「请 owner 复议」) —— 若 owner 认为审计轨应留在本文件内, 按 Rule #10 撤回即可, 审计轨文件本身是无损搬运。

> ## 📌 这是一次**重写**, 不是修订
>
> 原版经 **post_spec R1 (5 席) → R2 (新眼睛) → R3 (第三双新眼睛)** 三轮, 同口径 major **4→6 上升**, 判定**不收敛**。每一版 fix 都在自己新写的条款上引入等量缺陷 (R2/C1 与 R3/C2 都是「上一版 fix 自己写的逻辑」)。
>
> owner 2026-08-02 裁定 **A+B**: **A** = 抽出 §0 独立交付; **B** = 关键决策转 spike 实测, **完成后重写而非继续打补丁**。
>
> **S1–S6 六条 spike 已全部完成** (`.aria/spikes/2026-08-02-*`)。本版据其结论重写 —— 其中 **S4 与 S5 各推翻了一条上游审计结论**, 若继续打补丁, 那两条错误会被原样吸收进 Spec。

---

## Why

### 问题

两个 AI 容器对**同一个 issue** 各自起草 Spec、各跑数轮审计闸门、互不知情, 直到一方 ship 才发现。**已发生 5 次。**

第 5 次的形态最完整: 本 Spec 于 07-30 起草, 论点是「闸门审产物质量, 不审产物是否该存在」; **起草者在 07-31 做修订前自己没有 fetch**, 而并发轨已把同一个 #122 走完十步循环 ship 并归档 —— 三天投入的修订对象**在修订期间已经作废**。

⇒ **提出这条纪律的人, 在提出后的第二天违反了它。** 不是不知道, 是知道也做不到。这是「纪律不足以替代机制」的最强证据。

### 根因: 闸门审产物质量, 不审产物是否该存在

10 轮闸门的入口断言里**没有任何一条**问过「远端是否已出现同 issue 的竞品 Spec」。SCOPE_OK / anchor 固化都在审**这份产物做得对不对**, 从不问**它该不该存在**。

### 已 ship 但接错位置的机制

`phase1_gate.py --linked-issue` 产出 `linked_issue_overlap[]`, CLI help 原文即「同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)」。实测接线:

| Skill | 认领 |
|---|---|
| `phase-a-planner` (A.1-A.3) | ❌ **零调用** |
| `phase-b-developer` `:86-96` (B.0 块) / `branch-manager` `:146-152` | ✅ Phase B 入口 |

> **rework v3 行号订正**: 旧版写 `phase-b-developer :88-93 / branch-manager :149`。实读 aria `d50f9c3`: `phase-b-developer/SKILL.md` 的 B.0 块起于 `:86` (`B.0 - REQUIRE claim (…)`) 至 `:96` (`skip_if:` 注释段起始一带), 其中调用模板在 `:91-93`; `branch-manager/SKILL.md` 的标题在 **`:146`** (`### 前置: REQUIRE claim …`), 正文至 `:152`。命令 `git -C aria show d50f9c3:skills/phase-b-developer/SKILL.md | sed -n '86,96p'` / 同法读 `branch-manager` `146,152p`。

**ref 实测**: 竞品轨于 `07-27T11:53:12Z` **确实认领过** —— 但那是**在它跑完 4 轮 post_spec 之后**。

⇒ **认领点在 Phase B, 只能保护「已做完 Phase A 的人不被打扰」, 保护不了「正要开始的人不做重复功」。认领必须早于投入, 否则它记录的是既成事实而非预防碰撞。**

### ⚠️ spike 推翻的两条上游结论 (若不重写会被原样吸收)

| 上游结论 | spike 实测 |
|---|---|
| R2/M2:「basename 截断型别名恒漏是活跃问题」 | **S4 (⚠️ 2026-08-04 订正)**: 在**真正会被传给 `--linked-issue` 的总体**里截断型别名 **= 0 实例**, ref 已落盘总体同样 0 ⇒ 降为已知限。**但 S4 原报的「比例是反的 / R2 量错了总体」已作废** —— 逐字复跑 R2 的口径得 25/11 (与其 24/10 一致), 两组口径与范围都不同, **S4 自己做了一次跨总体比较, 与它指控 R2 的错误同形**。R2 的口径其实更贴近 `--linked-issue` 真实取值 |
| R3/M3a:「`./_` 分隔符碰撞属 dormant, 本组织无含 `.`/`_` 的仓名」 | **S5**: `10CG/10cg.local` 是**真实仓** (Forgejo API 实测, 11 open issues, handoff 引用过) ⇒ **活跃, 非 dormant** |

---

## ⭐ 真正的瓶颈: 主机制的输入九成缺席 (S4 的意外发现)

**实测口径 (rework v3 重测, 主仓 `cc1bdef`; 旧版写的 `141 / 13 / 9%` 是 2026-08-04 的过期计数, 已作废)**:

```
find openspec -name proposal.md | wc -l                              # 147
grep -rlE '\*\*(Linked Issue|关联 Issue)\*\*' openspec --include=proposal.md | wc -l   # rework v3 @ cc1bdef (中文单拼写): 15 = 14 archive + 1 changes; 2026-08-30 起字段名两拼写, 复核用本行两拼写命令
find openspec/changes -name proposal.md | wc -l                      # 7
```

⇒ 在**在制**语料 (`openspec/changes/` 7 份) 里, **rework v3 落盘前真有该字段的 = 0 份**: 当时 grep 的唯一 `changes/` 命中来自本文件**旧 §1 里被引用的示例行** (行首 `> > **关联 Issue**: [10CG/aria-plugin #122](…)`) —— 即**形状匹配会在讨论该字段的 Spec 上假阳性** (同 memory `reference_secret_guard_false_positive_on_spec_docs`)。⇒ 「15」这个数**含至少 1 条假阳**, **不可直接当作可得性**。
**落盘后的现状 (2026-08-30 订正; 复核以命令为准, 数字是当日观测)**: 旧 §1 连同那行示例已迁出; 本文件按 FIX-19 补了**真的**字段 (第 **13** 行, 现为 `> **Linked Issue**: \`10CG/Aria#174\`` —— 英文 canonical + 真 token)。**中文单拼写的 grep 已不再命中本文件**: `changes/` 下按中文谓词的命中今天全是围栏内示例 (假阳); 按两拼写**行首**谓词才是 3 份真字段 (母 / 字段 / 探针; 前者真 token, 后两者哨兵 `none`)。主机制靠 `linked_issue` 匹配, 而该输入在在制语料上仍基本不存在 (R6/CR M5 + TL M6 + QA M1 订正旧句「1 条真阳」)。

⇒ **本 Spec 不再承担「把字段搞出来」** (owner 2026-08-23 方向 b): 字段可得性 / 抽取规则 / 机械校验整体迁至 **[`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)**, 依赖方向见下方 §1 指针段。**本 Spec 只承担「字段在场时怎么用它认领, 以及 track-id 契约」**; 字段缺席时主机制退化为零输入, 成文于 §6, 不假装覆盖。

---

## What Changes

### §1 「关联 Issue」字段可得性 — ⛔ **整节已迁出** (owner 2026-08-23 方向 b)

> **迁往**: [`openspec/changes/linked-issue-field-availability/proposal.md`](../linked-issue-field-availability/proposal.md) —— 原 §1 的四条 (进模板 / 格式固定 / 机械校验 custom check / 不追溯) 与「抽取规则」承重问题整体由该 Spec 承担, 连同 R2 簇 **C-A** (抽取规则 defer ⇒ check 上线恒红)、**M-10** (§1.3 custom check 无实现宿主 + SC-13 零验证宿主)、**M-2** (`standards/openspec/templates/proposal-minimal.md` 跨项目 SOT 未入 Impact), 以及 R1 editlist **FIX-06/07/08**; 原 **SC-13** 一并迁出 (见 Success Criteria 表内保留的迁出行); 本 Spec 不再对「字段怎么产生、怎么校验、怎么抽 token」作任何断言。
> **为什么迁**: R2 判定 C-A (抽取规则 defer 到 A.2 ⇒ check 上线恒红) 是 **R1/C3 still-open** 且承重, 与 A.1 认领机制**没有共同的收敛面**; owner 2026-08-23 裁定**方向 b 缩 scope**, 主体只留 A.1 入口认领 + track-id 契约。
> **依赖方向 (逐字, 不得读成隐式前置)**:
> - **字段 spec 与探针 spec 都不是主体的阻塞前置。** 主体在「字段缺席」时退化为**零输入** (`phase1_gate.py:1230` 的 `if args.linked_issue:` 门控整块, 见 §2.5 / §6), 该缺口成文于主体 §6, 不假装覆盖。
> - **主体是两个子 Spec 的语义母体**: 子 Spec 的 track-id / claim 语义一律引用主体, 不得自行重定义。
> - ⇒ 本 Spec 可**先于**两个子 Spec ship; 子 Spec ship 后主机制的输入覆盖率上升, 但主机制的**正确性不依赖它们**。

### §2 A.1 入口认领 (主机制)

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<spec-slug>-<container_uuid>" \
  --phase A.1 --mode advisory \
  --linked-issue "<org>/<repo>#<n>" \
  --include-terminal \
  --repo-path "<主仓根>"
```

> **⚠️⚠️ token 不产生合法 canonical 值时 —— 哨兵 (canonical `none`, alias `无`; 集合定义见字段 Spec §2) / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` (四态判据引字段 Spec §3 E6 四态表, 本 Spec 不重定义) —— 整个 `--linked-issue` 参数必须省略, 绝不可传哨兵或脏串 (R1-fix/NEW-01 + R4/K8, 主控实跑复现; 下方实跑用的是 `无`, 对 `none` 与模板 placeholder 同理 —— 任何非空字符串都 truthy)。R6 接缝 C1/C4 订正: 旧版只豁免哨兵, 与字段 E6「三格省略」相反, 存量 markdown 链接形 (`NO_TOKEN`) 会被整串喂进匹配面。**
>
> `linked_issue_overlaps` **只在 `own_linked_issue` falsy 时短路** (**rework v3 行号订正**: 实读 aria `d50f9c3` 的 `lib/collision.py:265-266` = `if not own_linked_issue:` / `return []`; 原写 `:207-208` 是 `cb6bd5d` 口径, 已随前置 Spec 合并下移), 而 `"无"` 是 **truthy** ⇒ **两份毫无关系的 Spec 只要都写 `无`, 就会互相命中 overlap**。实跑复现:
>
> ```
> linked_issue_overlaps([claimA(linked_issue='无'), claimB(linked_issue='无')], 'spec-a-uuid1', '无')
> → [{'track_id': 'spec-b-uuid2', 'linked_issue': '无', ...}]   # ❌ 误报
> ```
>
> ⇒ **哨兵的语义是「已核实无关联」(一条正证据), 不是一个可参与相等比较的 token。** 此时 track-id 仍是 §2.1 的唯一形态 `<spec-slug>-<container_uuid>` (1A 后没有第二形态), 但主机制对该轨**不产生输入** —— 该已知限须写进 §6 缺口表。
>
> **这条是 (已迁出的) §1「显式写 `无`」与本节「实参逐字节取 token」两条 fix 之间的接缝** —— 三个对抗验证镜头都没抓到 (M3 只在 (已迁出的) §4 探针层处理了 `无` 的归属, 没下移到 CLI 实参层), 由整合者实测发现。**属「多条 fix 互相拆台」的第二类形状。**
> **rework v3 归属**: 「字段值为哨兵时怎么写、哨兵集合是什么」归 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md) (其 §2 / E5); 「**实参必须省略 `--linked-issue`**」是 CLI 调用面, **留在本 Spec** (本节 + §6 缺口表首行)。本 Spec 全文出现的 `无` 一律读作「哨兵集合的任一成员」, 不单指那个汉字。

**`--linked-issue` 实参的取值 —— 两阶段, 模板一次写死, 不需要字段 Spec ship 后二次编辑 (R6 接缝 C1/C5 的归属处置)**: 前置块内的实参取法逐字写成 ——「若 `${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/linked_issue_field_probe.py` 存在: 实参 = `python3 <该脚本> --emit-arg <本 Spec 的 proposal.md>` 的 stdout (空 ⇒ 省略该参数); 否则 (字段 Spec 未 ship): 按字段 Spec E6 手工判 —— 只有字段行冒号后首个 code span 的第一个元素形如 `<org>/<repo>#<n>` 且非哨兵时才传, 逐字节」。**该模板行归本 Spec Impact** (`phase-a-planner` / `spec-drafter` 两行), 字段 Spec 只负责 `--emit-arg` 模式存在 (其 SC-9); 两份 Spec 任意顺序 ship 均自洽, 不存在第二次编辑。SC-22 ② 含字面 `--emit-arg`。

**触发时机**: A.1 **起草前**, 作为**独立标题级步骤** (仿 `branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim (Part A1, MUST — 与 phase-b-developer B.0 同一条约束)`; ⚠️ 该标题里的 `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的**部件名** (A1 = REQUIRE claim + `enabled` 默认翻转, B1 = `linked_issue` 字段; 实读归档件 `openspec/archive/2026-07-11-coordination-claim-lifecycle-and-overlap/proposal.md:35,:50`), **不是** Phase A.1 —— R5/M2 误读, rework v4 一度落成改名, R6/CR M1 撤回; 本 Spec **不改**该标题, SC-22 ① 要求新标题含带点的 `A.1` 且 ④ 禁 `--phase B`, 足以与它区分), **不塞进现有 A.1 的 YAML 动作列表** —— §Why 已证埋进长列表的单行指令会被静默跳过 (R3/M6)。锚点字面钉为 **`前置: REQUIRE claim`** (与 Phase B 的 `B.0` 对称), 断言形态见 **SC-22**。

> **⚠️ 为什么换锚点 (R1-fix/FIX-13, rework v3 落)**: `phase-b-developer/SKILL.md` 的 `B.0 - REQUIRE claim` 在 **`:86`**, 位于 ```` ```yaml ```` 块内 (`:88` `check:` / `:89` `if_missing:` / `:92` `--raw-track-id "<本 cycle carry-id/Spec id>"`), 是 **YAML 键、不是标题**; 该文件 `grep -n "^#\+ "` 的全部标题里**无任何 `B.0`**。⇒ 旧版「仿 `### B.0`」引的是一个**不存在的锚点**, 不可作样板。实存的标题级样板是 `branch-manager/SKILL.md:146`。
> **B.0 自身的 YAML-键形态是既有欠缺**, 与本 Spec 的「前置: REQUIRE claim」落点正交, **不在本 Spec 修** (另开 issue) —— SC-22 的 docstring 须写明这处强度差异是有意的。

#### §2.1 track-id 派生 (spike S3 定案; **owner 2026-08-30 裁定 1A: 单一形态**)

**`<spec-slug>-<container_uuid>` —— 唯一形态, 不分「有无关联 issue」** (D18)。「是不是同一个 issue」由 claim 的 `linked_issue` 字段承载 (Part B1 已 ship, 归一由前置 Spec 提供); 「是不是同一条轨」由 track-id 承载; track-id **不再**编码 issue 号。

> **⛔ 1A 之前的 issue 派生形 `<归一后 basename>-<str(int(number))>-<container_uuid>` 已取消** (owner 2026-08-30, 决策单第 1 项)。随之消失: `number` 段的 `str(int())` 归一规则 / 「回落形」概念 / §5.1 二分谓词 / §5.3 的 `spec_slug` 三元组 release / claim 的两个新字段 `spec_slug`·`track_form` / D12 / SC-1·4·27·30·31。**代价成文**: (a) 改 Spec 目录名 = 换 track-id, 须 release 旧 + acquire 新两步 (§5.2 / SC-15); (b) 同一容器在同一 issue 上开多个方向时, 各方向互报一条 `linked_issue_overlap` advisory (同 issue 不同 track-id —— 它们确实是同 issue 的两条轨, 告警语义正确, 噪声由 §2.3 的 `AskUserQuestion` 一次吸收)。旧版 §2.1 / §5.1 / §5.3 / K1 / K2 / K3 / K4 原文按字节移入 [审计轨 §6](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#6-2026-08-30-owner-六项裁定与-1a-移出原文)。

| 段 | 规则 | 依据 |
|---|---|---|
| `spec-slug` | 本 Spec 的目录名 `openspec/changes/<slug>/` **逐字** (拼接侧**不预归一**; 归一由 `derive_track_id` 在 acquire 内部做 —— lower / `./_`→`-` / **原串 >64 字符或含非 ASCII ⇒ 整串 sha256 回落, 结果形如 `sha256-<16 hex>`, 不保留 slug 与容器段的可读形式** (`lib/track_id.py:70-76` 步骤 4 + `:155` `use_fallback`; 步骤 3 的截断在实现里自陈 no-op —— R6/TL M1 订正旧写法「截断」)) | **D18**: 目录名是 A.1 起草时唯一已知且人类可读的身份; 同一 Spec 跨 session 重新认领得到同一串 (SC-23 的前提); 归一在 acquire 内做, 与 Phase B 现有路径同一函数 |

| `container_uuid` | container-id 文件的 **`uuid` 字段本身**, **不截断、跳过 `label`** | `get_container_id()` (`lib/identity.py:191`) 在 `:222` 是 `return label if label else uuid` (**label 优先**), 而文件模板**明确邀请**用户设 label ⇒ `devbox-A1`/`devbox-A2` 截断后碰撞。uuid 是机器生成定长 hex, 碰撞域 16⁸≈4.3e9 可算 (实测 Lab 仅 2 容器)。**hostname 兜底分支实读落点 = `:242` (`return _hostname()`)**; `:244` 是**另一条**「新生成 uuid」路径 (`return uuid`), 二者不可混。<br>⚠️ **S3 spike 勘误 (editlist FIX-18)**: `.aria/spikes/2026-08-02-S3-track-id-derivation.md:72` 记「`:244` 是 hostname 兜底」为**行号误记** —— 实读 `:242` 才是 `return _hostname()`。**spike 记录不追改, 本 Spec 引用 S3 时以此处为准。** |

**需新增**直取 `uuid` 字段的 accessor (现有 `get_container_id()` 不能直接用)。**hostname 兜底分支** (只读 fs) 同样返回 hostname, 接受其碰撞域 —— 该分支本身已是降级路径。

> **为什么必须含容器段 (rework v3 加强 — 备选方案已被实测证伪, 见决策记录 D3 补注)**:
>
> **备选方案**: 去掉 `container_uuid` 段, 让两容器对同一 issue 派生**同一** track_id, 靠 reconcile 的**同名碰撞** (`phase1_gate.py` 7c 分支的 `AdvisorySurface(kind="occupied", …)`) 报警。它更简、不动 §2.1 拼接规则。**该方案已被实读证伪, 不采**:
>
> 1. **7c 只在竞品 claim 未 stale 时触发** —— 实读 `phase1_gate.py` 7c 分支条件 `verdict.winner is not None and not _takeover_eligible(verdict)`; 一旦 `_takeover_eligible(verdict)` 命中 (`phase1_gate.py:283-294`: `"stale_takeover_eligible" in reason or reason in {"no_active_candidates","empty_claims"}`) 就走 7d, 而 7d 的注释逐字是 `# No prompt needed: stale / terminal tracks are safe to acquire.` ⇒ **stale 竞品零 surface**;
> 2. **竞品 claim 必然 stale** —— `lib/constants.py:43-44` 逐字自陈 `NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)`, 而 `STALE_TTL: int = 1800` (`:36`, 30min); 本 Spec 的事故窗实测 **48–72h** ⇒ 同名通道在整个事故窗内**结构性静默** (= Aria #180);
> 3. **overlap 通道则新鲜度免疫** —— 实读 `lib/collision.py:265-292` (`linked_issue_overlaps` 全函数体) **不含任何 heartbeat/新鲜度过滤**, 对 stale claim 同样可见。
>
> ⇒ **容器段的作用不只是「防 overlap 恒空」**(旧版理据), 更是**把碰撞检测从新鲜度脆弱的同名通道 (7c/7d), 挪到新鲜度免疫的 overlap 通道**。这是它承重的真正原因。
> **原理据仍成立且是同一结论的另一半**: 不含容器段则两轨派生出同一 track_id, 而 `lib/collision.py:278-279` 明写 `if c.track_id == own_track_id:` / `continue  # same-name collision — reconcile's job, not ours` ⇒ **互相被排除 ⇒ overlap 恒空 ⇒ 主机制死** (R2/C1 实证; **rework v3 行号订正**: 旧版写 `:219-220` 是 `cb6bd5d` 口径, aria `d50f9c3` 上为 `:278-279`)。该注释本身也印证了第 1 点 —— 同名碰撞被显式**推给 reconcile**, 而 reconcile 那条路径正是上面证伪的那条。
> **职责分离**: 「是不是同一个 issue」由 `linked_issue` 承载; 「是不是同一条轨」由 `track_id` 承载。原 R1-fix 把前者塞进后者, 两轨遂在 track_id 维度失去可辨性 —— 而 overlap 正靠它工作。

##### §2.1a 拼接的落点与被测对象 (R2/M-17 第 1 项)

**拼接由谁做**: 上表两段的拼接**发生在 A.1 模板里** (`phase-a-planner` / `spec-drafter` 两处 SKILL.md 的 `--raw-track-id "…"` 实参), **没有代码宿主** —— 实读 `lib/track_id.py:61` 的 `derive_track_id(` 只做归一四步 (lower / `./_`→`-` / 截断 `MAX_TRACK_ID_LENGTH: int = 64` / 非 ASCII 走 sha256 回落, `:70-76`), **不含任何拼接语义** (1A 前另有 `str(int(n))` 归一, 已随 issue 派生形取消)。

⇒ **拼接的验收分两层, 缺一即无被测对象** (旧版把它们标成无宿主的断言, 是 R2/M-17 的命中点; **2b 裁定后**这两层就是全部):

| 层 | 被测对象 | 宿主 | 怎么会红 |
|---|---|---|---|
| **文本层 (可机械)** | 两处 SKILL.md 的「前置: REQUIRE claim」步骤块里, `--raw-track-id` 占位串**字面**为 `"<spec-slug>-<container_uuid>"` (含容器段; 不含 `<number>` / `<basename>`) | **SC-22 ②** (与其余五个字面量同一断言, 同宿主 `test_coordination_default_lockin.py`) | 当前两处 SKILL.md **根本没有**该步骤块 ⇒ baseline 必红; 占位串写成旧的 `<basename>-<number>-<uuid>` 或漏容器段 ⇒ 必红 |
| **行为层 (定向 fixture)** | AI 实际拼出的串: slug 段 = 本 Spec 目录名逐字; uuid 段 = container-id 文件的 `uuid` 字段 (**不是** label) | rule6_note 覆盖外档点名行为 **(a)** 的拼串子项 | 「用 label 段」或「拿 issue 号当 slug」的臂与正确臂可分辨 |

**本 Spec 不新增拼接函数** —— 新增代码落点只有 `lib/identity.py` 的直取 `uuid` accessor (见 Impact 表)。「拼接无代码宿主」这一半**成文交付**, 不用「以后加个 helper」把它糊过去 (memory `knob-granularity`: 诚实交付一半 + 说明哪半是哪半)。

> ## ✅ 第 5 项裁定 (owner 2026-08-30) — 「四条 SC 一刀切降级」的部分回滚, 逐条落版
>
> R4/K3 曾把 SC-1 / SC-2 / SC-4 / SC-15 一律降为「行为 (定向 fixture)」, 理由是派生无代码宿主。R5 两席结论相反, 主控逐条裁 (见 R5 聚合报告「席位分歧」节), owner 采纳; 叠加 1A 后的终态:
>
> | SC | 终态 | 为什么 |
> |---|---|---|
> | SC-1 / SC-4 | **⛔ 撤销** (随 1A) | 断言对象 (issue 派生形的改名不变性 / `#007`==`#7`) **不存在了**, 不是「维持降级」而是无对象 |
> | SC-15 | **代码类** (回归守卫, **baseline 即绿**) + **文本层** (SC-22 ⑥) | 宿主 `release_claim_by_track` (`lib/claim_lifecycle.py:377`) 与 `acquire_claim` (`:99`) **都实存**, 夹具手写新旧两串即可测「两步后无孤儿」; 它守的是这对函数的匹配键不被改坏。**AI 改名时记不记得走两步**是行为, 由 SC-22 ⑥ 的字面义务 + rule6_note (a) 覆盖 |
> | SC-2 | **代码类 (CLI 全链路)**, **改写声称对象** | 它钉的是 `linked_issue_overlaps` **经 CLI** 的行为 (两容器同 `linked_issue` 不同 track-id ⇒ 双方各含对方; 同 track-id ⇒ 双方为空), **不是**派生 —— 原文声称钉派生才是恒绿的根源。**baseline 即绿** (该路径今天存在), 价值 = 本 Spec 改 `:1230` 门控与加 `--include-terminal` 时的回归守卫 |
>
> K3 原文 (2026-08-27) 按字节移入审计轨 §6。**2b 裁定 (不建派生宿主) 使「拼接无代码宿主」成为长期成文状态**, 不再标「若 owner 采纳选项 (d) 则回滚」。

##### §2.1b carry-id 契约 — A.1 原串**即**本 cycle 的 carry-id (R2/C-C, editlist FIX-14 选项 A)

**问题 (KM-C1/C2 三处宿主独立复读)**: A.1 派生的 track-id 含 `container_uuid` 段, 而 Phase B / D.2b 既有的 carry-id 占位措辞不含容器段 ⇒ 走完循环时 **B-entry 认领与 D.2b 释放都匹配不到 A.1 那条 claim** —— 这比 §5 的连坐 (C-B) **更早发作**, 且发生在 happy path 上。

**处置 = 统一到一个串, 三处逐字节复用** (owner 的 U-3 选项 A):

> **A.1 认领时派生的那一串, 即本 cycle 的 carry-id。** `phase-b-developer` B.0 (`skills/phase-b-developer/SKILL.md:92` 的 `--raw-track-id "<本 cycle carry-id/Spec id>"`)、`branch-manager` (`skills/branch-manager/SKILL.md:146` 的 `### 前置: REQUIRE claim`)、`phase-d-closer` D.2b (`skills/phase-d-closer/SKILL.md:51-52`, `:55` 逐字「carry-id = Phase B-entry 时传给 phase1_gate 的同一原始串」) **三处逐字节复用同一串, 不再各自派生**。

- **三处 SKILL.md 的占位措辞须改为明示**: 「**A.1 认领时派生的那一串**; 未走 A.1 的 session 沿用 Spec id」⇒ Impact 表补这三行;
- `standards/conventions/session-handoff.md` **§2.3.8** 结构化 `{id, desc}` 的 `id` **同为该串** (**R3/KM-1 订正**: 原写 §2.3 —— 实读该文件 `:101` §2.3 是「机读 frontmatter schema」, `:217` §2.3.8 才是「结构化 Carry-id schema (§6 prose 层, **非 frontmatter**)」, 且 `:238` §2.3.8.3 逐字把「留 §6 prose, 不进 frontmatter」列为**硬约束** ⇒ 引 §2.3 会把实现者引向违反该硬约束) ⇒ Impact 表补该行 (R2/M-14 的一半);
- **为什么必须统一而不是在 D.2b 打补丁**: 实读 `lib/track_id.py:61-76` 的归一四步**不含任何去容器段逻辑** ⇒ 两个不同原串归一后必是两个不同 `track_id`, 而 `release_claim_by_track` 按 `(container, 归一 track_id)` 定位 (`lib/claim_lifecycle.py:377` 定义, `:425` `if rec.container == resolved.container_id`) ⇒ 不统一就**没有任何**归一层能把它们接上;
- **已知限 (成文, 不假装覆盖)**: 存量 active claim 仍是**旧形态** (无容器段), 本 Spec **不改写存量 ref** (见 §非目标) ⇒ 过渡期两形态并存, **新轨用新形态、旧轨自然随 GC 退场**。这段过渡期内, 旧形态轨的 A.1↔D.2b 断链**仍然存在**;
- **闭环由 SC-23 钉住** (A.1 认领 → 走完循环 → D.2b `release_gate.py --raw-track-id <A.1 原串>` ⇒ 该 claim 不再 active)。

> **与 §非目标「不动 Phase B 入口现有认领」的边界 (U-3 的争点, 此处明确)**: 改的是**三处模板里 carry-id 占位串的取值口径**, **不改** Phase B 闸门的调用形态、参数集与判定语义; `--include-terminal` 仍默认 False, Phase B 输出逐字节不变。若 owner 判此仍属「动 Phase B」, 备选是 editlist 的**选项 B** (D.2b 额外用 A.1 原串再调一次 `release_gate.py`) —— 本版按 owner 2026-08-23「主体必须解 C-C」采选项 A, **请 owner 在 R3 时确认**。

#### §2.2 保护窗 (spike S1 定案)

事故窗实测 **48–72h**, 而 `STALE_TTL` = 30min、`SWEEP_TTL` = 24h ⇒ 保护窗短于事故窗。

**处置 = 新增一个 by-track 的 heartbeat 变体**, 按 `(container_id, normalized track_id)` 定位, 刷新**全部**匹配的 active claim。

> **⚠️ 挂载点的真实触发密度 (R3/TL-M1, 主控 2026-08-25 补 —— 原文把常态写成了「漏跑一次」)**: (ii) 把 heartbeat 挂在 `/state-scanner` 入口, 但**审计轮内不会触发它** —— 实读 `skills/audit-engine/references/execution-modes.md` 的 convergence 与 challenge 两个模式块, **轮内均无 `/state-scanner` 调用**。⇒ 一次 post_spec 多轮审计 (本 Spec 自己就跑了 3 轮, 每轮数十分钟) 期间 heartbeat **一次都不刷**, 这是**常态而非「漏跑一次」**。**成文的残余风险**: `STALE_TTL` 维持 30min (owner 撤销 (iii)) ⇒ 长审计轮期间本轨 claim 对 reconcile 呈 stale、7c occupied surface 静默 (= Aria #180 的窗口), **只有 overlap 通道 (新鲜度免疫) 仍可见**。本 Spec **不**为此新增第二个挂载点 (会重蹈 (i) 被否的理由), 而是把它列为**已知限**并指向 follow-up: 若要覆盖长审计轮, 应在 audit-engine 轮间挂一次 heartbeat —— 属 audit-engine 变更面, 不在本 Spec。
>
> **⚠️ 口径统一 (R2/M-17 第 2 项)**: 旧版正文写「匹配键**改**」而 Impact 表写「**增**并存变体」, 两读矛盾。**以「增并存变体」为准** —— 既有 `heartbeat()` 的 `(container, session)` 匹配键**保持不动** (实读 `lib/claim_lifecycle.py:228`: `if rec.container == resolved.container_id and rec.session == resolved.session_id:`), 新增变体与之并存, 形态照抄 `release_claim` / `release_claim_by_track` 的并存模式 (`lib/claim_lifecycle.py:274` / `:377`)。**理由**: 改既有键会改变 Phase B 现有认领路径的行为, 撞 §非目标; 并存则 Phase B 逐字节不变。全文自此只用「增并存变体」这一种措辞。

> **这不是新设计, 是照抄隔壁函数**: `release_claim_by_track` 的 docstring 逐字记载**同一个 defect 已被同款修法解决过** ——「`release_claim` locates by `(container, session)`, but a later invocation runs with a **FRESH session_id** and cannot match... this variant **locates by (normalized track_id, container) and ignores session**」。它顺带给了两个细节: 一对多时**全部**刷新 (release 侧同款选择, review I1 已论证只放最早那条不够); raw→normalized 走 `derive_track_id` 与 acquire 同路径。
>
> **session_id 落盘复用方案判否** —— 被本方案取代, 且引入并发/过期新面。
> **冗余**: 每次调 `phase1_gate` 都写一条新 claim (生产 ref 实证 27+ 条) ⇒ 再调即自然续期。但它依赖「AI 记得再调」—— 而那正是本 Spec 存在的理由 ⇒ **heartbeat 为主, 再调作冗余, 不可只靠后者**。

> ## ✅ 已定项 (R1-fix/C2 — 3 席命中 → 2026-08-22 owner 裁定落版): **谁调、什么时机调**
>
> `heartbeat()` 的**生产调用点仍为 0** (`constants.py:43-44` 自陈:「NO production heartbeat loop exists」)。**换匹配键不产生刷新者** ⇒ 保护窗实质仍是 24h ⇒ **SC-5~7 可以全绿而问题原样存在**。
>
> **spike S1 §6 明确把「谁在什么时机调」交还给 Spec** (「属 Spec 范围不属 spike」), 而重写当时**没有接住**, 转 owner 裁定。**以下逐字取自 `git show 86540f2:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`** (R1 rework 核验 major-3 订正 —— 上一轮此处曾被整段删除换成 AI 转述且与原文有实质偏差, 未请复议; 现按硬约束恢复原文字面, 不再转述):
>
> > **✅ owner 裁定 (2026-08-22): 采 (ii)+(iii) 组合** —— heartbeat 挂 state-scanner 入口的 **AI 编排层** (scan.py collector 保持只读, 与 phase1_gate B-entry 既有挂法同构; 每次 `/state-scanner` 必跑, 不依赖 AI 记性); 同时 `STALE_TTL` 30min → **24h 量级**收窄版兜底, 使「漏跑一次扫描」不至于立即暴露在 `--sweep-stale` 下。落版义务: (ii) 的挂载点写进 state-scanner SKILL.md 编排契约 + (iii) 的 TTL 变更量化 sweep 语义代价 (spike S1 选项 c 的评估框架); 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。
>
> **落版 (AI, 2026-08-23)** ((i) 见下方「候选 (i) 未采纳」, 以下 (ii)/(iii) 即本节落版):
>
> **(ii) 调用点 = `state-scanner` 入口的 AI 编排层; `coordination.enabled == true` 时每次 `/state-scanner` 必跑** (**rework v3 按 R2/M-7 给标题补上门控限定** —— 旧标题的裸「每次必跑」与 §2.5 的 opt-out 条款字面冲突, 详见下方「与 B-entry 的关键差异」):
> - **具体 CLI 入口 (R1 rework 核验 major-1 补钉)**: 「AI 编排层调用 heartbeat CLI」原文未点名具体入口, 现定为 `skills/state-scanner/scripts/phase1_gate.py` 新增 **`--heartbeat-only` 模式** —— 复用其既有 identity/fetch/push 管道; 只刷新**本容器本 track** 的 `heartbeat_at`, **不写新 claim, 不判碰撞** (与 A.1 acquire 调用是同一 CLI 文件下的两个独立模式)。若 A.2 落地时改为独立脚本 `scripts/heartbeat_gate.py`, 亦属同一变更面 (已按此登记进 Impact 表, 见下方)。自本条起, 本节及 SC-21 提到的「heartbeat CLI」均特指该入口;
> - **既有同构先例**: `phase1_gate` 的 Phase B-entry 挂法就是这个模式 —— **实读** `skills/state-scanner/SKILL.md:149`「接线点 = AI 编排层, 不是 `scan.py`」+ `references/layer-l-integration.md:15`「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, 不在 scan.py 内自动执行」。heartbeat 挂同一层 (AI 编排层调用 `--heartbeat-only`, collector 内不跑), `skills/state-scanner/scripts/scan.py` 的 collector 逻辑**保持只读, 零改动**;
> - **与 B-entry 的关键差异 —— 并且「无条件」限定的是什么 (R2/M-7 修正, rework v3)**: B-entry 是**条件触发** (实读 `skills/state-scanner/SKILL.md:149`: 触发条件为 `coordination.enabled == true` **且** `tracks_multibranch.collision.kind` 非空); heartbeat 的「**无条件**」**只**限定后半条 —— 即**不依赖 `tracks_multibranch.collision.kind` 是否非空** (它是维持性动作, 不是碰撞响应动作), 只要本会话在 coordination ref 里持有 active claim, 每次 `/state-scanner` 都刷新。
>   > **⚠️ 它不是「无视 opt-out」**: heartbeat **同样受 `state_scanner.coordination.enabled` 门控** —— `enabled == false` ⇒ **heartbeat 零调用**, 与 §2.5 是**同一条开关**, 不是两条。旧版「每次 `/state-scanner` 必跑」的字面读法会让只读型命令在 opt-out 项目上每次写 claim + 推远端 (对未配 coordination ref 的第三方是外向副作用), 这是 R2/M-7 的命中点。**由 SC-28 钉住** (`enabled == false` ⇒ 入口零 heartbeat 调用), 与 SC-9 是同一开关的两半;
> - **落点**: `skills/state-scanner/SKILL.md` 的 Layer L Phase B 集成段 (`:143-178` 一带) 新增对称的「Layer L A.1 heartbeat 集成」小节, 写明触发条件/调用形态 (`--heartbeat-only`) /失败处置 (fail-soft, 不阻断 `/state-scanner` 主流程);
> - **`--heartbeat-only` 刷哪条 track (R2/M-12 + R2-CR-M1 补, rework v3 —— 旧版只写「只刷本容器本 track」而 track 来源未定义, 且 claim 按 `(container, session)` 键控在跨 subprocess 时不可判定)**。**来源是三级回落, 顺序固定**:
>   - **① 本 session 已跑过 `phase1_gate` ⇒ 该 claim 在 coordination ref 内可按 `(container, session)` 直接定位, 从 `claims/<container>/<session>.yaml` 的 `track_id` 字段读出** —— **机读持久化状态, 非记忆**;
>     > **⚠️ 先例引用订正 (R3/TL-M6 —— 上一轮主控指令误引, 主控担责)**: 上一版此处引 `skills/phase-b-developer/SKILL.md:88` 的 `check: phase1_gate telemetry / 编排层记忆 (本 session 是否已跑 phase1_gate)` 作「同一个 telemetry 通道取 track_id」的逐字先例。**实读证伪**: 该行是**布尔谓词** —— 它回答「**跑没跑**」, **不携带 `track_id`**; Phase B 的 track_id 在同文件 `:92` 另取自 `--raw-track-id "<本 cycle carry-id/Spec id>"`。⇒ 该先例**不能**用来论证「telemetry 提供 track 来源」, 已撤。替代的机读来源见本行正文 (coordination ref 内本 session 自己的 claim)。
>   - **② 回落 = handoff §6 的结构化 carry-id**, 与 B-entry 闸门取 `raw_track_id` 的**同一个来源** —— 即 §2.1b 定义的那一串 (`standards/conventions/session-handoff.md` **§2.3.8** 的 `{id, desc}` 之 `id`);
>   - **③ 两级都取不到 ⇒ 跳过, 但**必须留下可观测的持久化痕迹** (fail-soft)。**⚠️ K7 (R4) 订正 —— 原文写「跳过 + `log()`」是个空信号**: 实读 `def log(` 在全 aria **零命中**; `scripts/phase1_gate.py:56` 只有 `logger = logging.getLogger(__name__)` 而**无 handler** (`basicConfig` 在 state-scanner 内只在 `scan.py` (全 aria 另有 `issue-triage/scripts/triage.py:290`, 与本探针无关 —— R6/CR m6)) ⇒ 独立 subprocess 的 `logger.*` **全丢**。叠加 R3/TL-M2 禁写 production 遥测分区 + SC-28 正向断言计数不增 ⇒ **「跑了但 skip」与「根本没挂载」在任何持久化产物里逐字节相同**, 连续三天静默 skip **无一处会红**。**落版 (2026-08-27, 未经审计轮)**: `--heartbeat-only` **每次调用都向遥测 JSONL 追加一条 `_source="heartbeat"` 记录** (该分区 `coordination_probe` 不计入, 见 R3/TL-M2, 故不会把那条 enabled check 变恒绿), 记录含 `outcome ∈ {refreshed, skipped_no_track, skipped_disabled, error}` 与 `reason`。⇒ 「跑了但 skip」在磁盘上**可辨**。「猜一个 track 去刷」仍禁止 —— 会刷错**别人**的 claim。**新增 SC-32 (代码)**: 在无 carry-id 的环境下跑 `--heartbeat-only` ⇒ 遥测 JSONL **新增恰一条** `_source="heartbeat"` 且 `outcome="skipped_no_track"`; **怎么会红**: 只 `logger.debug` 不落盘的实现 ⇒ 零新增记录 ⇒ 必红。**baseline 必红** (该模式今天不存在)。
>   - **CLI 形态**: `python3 .../phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path <主仓根>` (**`--phase` 不可省 — R3/BA-M1**: `phase1_gate.py:1191` 的 `--phase` 是 `required=True`, 主控实跑 `--raw-track-id x --heartbeat-only` → `error: the following arguments are required: --phase` ⇒ 旧版字面形态**第一次实跑即被 argparse 拒**, 到不了 heartbeat 分支。本 Spec 取「文档补 `--phase`」而**不**放开该参数: 零代码改动; `--heartbeat-only` 不写新 claim, `--phase` 仅作占位不落盘) —— 由 AI 编排层**显式传入**, CLI 侧**不做任何推断**;
>   - **匹配**: 按 `(container, 归一 track_id)` 刷新**全部**匹配的 active claim (与本节「增并存变体」的匹配键一致), **不写新 claim、不判碰撞**;
>   - **⛔ 遥测分区边界 (R3/TL-M2, 主控实读证实 —— 不划这条界会把一个 enabled 的 check 变成恒绿)**: `--heartbeat-only` **不得**写生产遥测分区。实读 `skills/state-scanner/scripts/coordination_probe.py:18-21`: 它是**反死代码探针**, 只数 `.aria/coordination-telemetry.jsonl` 里 `_source=="production"` 的**近期** `run_gate` 记录 (该文件逐字「The production partition file is written only when ``_source=="production"``」); 而该分区的定义在 `scripts/phase1_gate.py:1047-1049` (`run_gate` docstring 逐字「written only by the CLI production path (:func:`_main` → :func:`_gated` with ``_source="production"``)」—— R5 自证 #1 点名、rework v4 漏清、R6/CR M6 + KM 母 M1 再抓, 现按真身改出处)。⇒ 若 `--heartbeat-only` 复用同一条产线, **每次 `/state-scanner` 都会写一条** ⇒ 该 check **永远 OK**, 无论真正的碰撞闸门是否还被调用 —— 它要防的「机制接线了但没人调」正好被自己的心跳掩盖 (memory `feedback_false_green_dual_is_permanent_red` 的镜像)。**落版**: `--heartbeat-only` 走 `_gated(_source="heartbeat")` 或完全跳过 `_emit_telemetry`; `coordination_probe` 的计数口径**保持只认 `production`**, 不放宽。**Impact 表已补 `coordination_probe.py` 行 (仅注释/口径声明, 不改逻辑)**;
>
>   > **⚠️ 对 R2-CR-M1 反对意见的答复 (R3/TL-M6 后重写)**: CR-M1 指「给 heartbeat 指定 track 来源等于回到依赖 AI 记性, 而那正是 (ii) 要消灭的」。**答复**: **① 是 coordination ref 内本 (container, session) claim 的 `track_id` 字段**, **② 是 handoff §6 的结构化机读字段** —— **两级都不是「AI 记性」**, 都是磁盘上可被机械读取、可被测试夹具构造的持久化状态。**⚠️ 但须诚实声明该答复的边界**: ① 只在**同一 session 内**可用 (跨 session 时 `session_id` 是 FRESH 的, 按 `(container, session)` 找不到旧 claim —— 这正是 §2.2 存在的理由); 跨 session 场景**只剩 ②**, 而 ② 依赖「上一次会话写过 handoff §6」。⇒ **本条不主张已彻底消除人为环节, 只主张两级来源都是机读的**; 「handoff §6 缺失时 heartbeat 静默不跑」是**成文的已知限**, 见本节 ③。
>   >
>   > **⚠️ 显式否决 CR-M1 的 B 方案 (「不指定 track, 直接刷新本容器全部 active claim」)**: **不采。** 该方案会把**被遗忘、未 release 的 claim 永久 keep-alive** —— 它们将永不 stale、永不进 `--sweep-stale` 候选, 变成僵尸 claim 长期占据 overlap 告警面。这与 §5.2 的显式 release 义务和 **SC-7**（超 `SWEEP_TTL` 未刷新仍被 sweep）**直接相反**: B 方案下 SC-7 结构性无法为真。
> - **`--heartbeat-only` 的 fetch 代价与复用 (R2-CR-m6 补, rework v3)** —— **它不得自带第二次 fetch**:
>   - **编排层的调用位置保证了这一点**: heartbeat 跑在 `/state-scanner` 入口、即 `scan.py` 之后 ⇒ snapshot 的 `coordination_fetch` 区块里已经有一次**刚完成**的 `refs/aria/coordination` fetch 结果。**复用它, 不重跑。** 该区块自 F6′ 起是 Phase 0.5 `remote_refresh` 的**纯派生**产物 (实读 `skills/state-scanner/references/state-snapshot-schema.md:1029-1041`: 「本区块不再独立发起网络 I/O」), 字段见 `:1043-1056`;
>   - **⚠️ 新鲜度谓词必须用 `coordination_ref_present`, 不能只用 `success` (执笔席实读订正 —— 主控口述的「`coordination_fetch.success == false` ⇒ degraded」按 schema 实读是 fail-OPEN 的)**: 实读 `:1043` 逐字 —— `success: bool  # Reflects FETCH 1 (branch heads, load-bearing)`; 而 coordination ref 是 **Fetch 2**, 其结果在 `:1056` 的 `coordination_ref_present: bool | null`, 语义 `:1061-1064` 逐字 = `true` 已取到 / `false` benign absent (ref 未发布) / `null` unknown (Fetch 1 失败短路, 或 Fetch 2 非 benign 失败)。⇒ **`success == true` 与「coordination ref 没取到」完全可以并存**, 只判 `success` 会把「没取到协调数据」当成「取到了」。**本 Spec 的判据 (fail-CLOSED)**: **仅当 `coordination_fetch.success == true` 且 `coordination_ref_present == true` 时**才视为「本轮协调 ref 已新鲜」; 其余一切取值 (`false` / `null` / 键缺失) 一律按 **degraded** 处理;
>   - **degraded 时的处置**: heartbeat **只写本地** ref, push **尝试一次**, 失败 **fail-soft** (log + 不阻断 `/state-scanner` 主流程), **不重跑 fetch**;
>   - **⚠️ 代价披露 (与原 §4 探针「不得称其轻量」同等义务, 此处不沉默)**: 复用路径下 heartbeat 的**增量网络代价 = 0** (不发起 fetch); 但**若实现者违反本条自带 fetch**, 代价参照 spike S2 的历史实测 —— 双远端 fetch 5 次均值 **~13.8s/次** ⇒ 每次 `/state-scanner` 加 ~13.8s。**这正是「不得自带 fetch」是硬约束而非偏好的原因。** 本 Spec **未实测** `--heartbeat-only` 的本地写 + 单次 push 耗时, 该数字留 A.2 补;
> - 关联 Aria#180 (heartbeat 零调用) 由本裁定一并解。
>
> **(iii) `STALE_TTL` 30min → 24h 量级 — ⛔ 已撤销 (owner 裁定 2026-08-23, 见本节末)**: `STALE_TTL` **维持 `1800` 不改**, 本 Spec **不再对该常量提出任何断言**。
> - **撤销的四个落点** (R3 核验席 minor-1 点名, rework v3 逐一执行): ① **SC-20** 整行改为「⛔ 撤销」; ② **Impact 表 `lib/constants.py` 行**删去「TTL 改 86400 量级」与「不变量注释二选一」, 只保留与 TTL 数值无关的注释同步项; ③ **§2.3 残余风险段**删去「放宽到 `SWEEP_TTL` 同量级」整套推理, 改为成文残余风险; ④ **闸门状态 item 3** 改为「原采 (ii)+(iii), 复议后 (iii) 撤销」;
> - **(iii) 撤销后 R2/M-8 的处置**: M-8 指 (iii) 漏了第三消费者 (`track_board::_freshness_status` / `_takeover_eligible`) 且抹掉 `lib/constants.py:40-42` 的两级顺序 (实读该三行逐字: `Deliberately much longer than STALE_TTL: STALE_TTL only marks a claim` / `"takeover-eligible" (advisory, reversible on next read), but the sweep` / `REWRITES status=abandoned durably and the victim has no recovery path —`) —— **(iii) 既已撤销, 这些影响面整体消失** (常量不动 ⇒ 无消费者受影响 ⇒ 两级顺序原样保留)。M-8 唯一残留的要求是「残余风险分析不得单向」, 见 §2.3;
> - **(iii) 撤销前的落版原文** (含当时的「⚠️ 事实订正」与「落版后的准确效果」两段) **按字节搬入** [审计轨 §2](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#2-22-c2-iii-落版原文-2026-08-23-owner-撤销前) —— 那两段里唯一仍承重的实读事实 (`--sweep-stale` 的阈值是 `SWEEP_TTL` 不是 `STALE_TTL`) 已保留在 §2.3 与「事实断言逐条实读清单」#14, 未随搬运丢失。
>
> **候选 (i) 未采纳**: 挂在 A.1 机械步骤上 (如每次写 proposal 文件后) 被 (ii)「每次 `/state-scanner` 必跑」覆盖同一诉求且触点更集中, 不再单独引入第二个挂载面。
>
> **✅ 上述 (iii) 的「⚠️ 实读订正 · 请 owner 复议」已闭环** (R1 rework 核验 major-3(a) 提出 → owner 2026-08-23 回应 → 结论 = **撤销 (iii), 只采 (ii)**)。**该复议项不再未决**; 其原文 (逐字) 见 [审计轨 §3](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#3-22-实读订正--请-owner-复议原文-已闭环)。
>
> **✅ 协调项已解** (`origin/feature/linked-issue-normalization` 分支状态, R1 rework 核验 major 订正, 主控实读): 该分支已于合并提交 `ca52d1c` (v1.67.0, `2026-08-23T09:14:07Z`) 合入 `origin/master` (`git merge-base --is-ancestor origin/feature/linked-issue-normalization origin/master` 成立), **早于本轮 rework 落盘**。实读 `origin/master` 上的 `lib/collision.py`: 新增 `normalize_linked_issue()` (`:178`) / `_linked_issue_matches()` (`:219`) 两个 helper, 插在 `linked_issue_overlaps` (`:230`) 定义之前 —— **确认未改** `linked_issue_overlaps` 的三参数签名 (`claims, own_track_id, own_linked_issue`)。行号已整体下移: `_TERMINAL` 由 `cb6bd5d:210` → `origin/master:268`; `if not own_linked_issue`/`return []` 由 `:207-208` → `:265-266`; `if c.track_id == own_track_id`/`continue` 由 `:219-220` → `:278-279`。**本节引用的 `lib/gc.py`/`lib/constants.py` 行号已核, 未漂移** (`git diff --stat ca52d1c^1 ca52d1c` 实测只触及 `SKILL.md` / `claim_schema.py` / `collision.py` / **一个** test 文件 `test_release_by_track.py`, 外加发布同步面文件 `marketplace.json`/`plugin.json`/`CHANGELOG.md`/`README.md`/`VERSION`; **R1 rework 核验 minor-2 订正**: 原文「两个 test 文件」为误记, 实为一个; 不含 `gc.py`/`constants.py`)。详见下方「事实断言逐条实读清单」#3/#5/#6/#16。已按 R1 rework 核验 major-2 补入 Impact 表 `lib/collision.py` 一行 (原表零覆盖), 见下方。
>
> **⚠️ rework v3 基线订正 (本段写于上一轮, 其「`origin/master`」指的是当时的 `ca52d1c`)**: `origin/master` 此后已推进到 **`d50f9c3`** (v1.67.1 `58a49e7` + 2 commit)。上面列的三组行号 (`:268` / `:265-266` / `:278-279`) 在 `d50f9c3` 上**逐字复核仍成立** (清单 #3/#5/#6), 但**基线标签一律以 `d50f9c3` 为准**, 不再用会漂移的 `origin/master` 指代。姊妹 Spec 现**已 ship 并归档**, 协调项完全闭环 (含 editlist FIX-11 —— 姊妹自己在 ship 前写入了关闭条款), 详见 §2.4 传递链 item 0 与清单 #16。
>
> **✅ owner 裁定 (2026-08-23): (iii) 撤销, 只采 (ii)。** `STALE_TTL` 维持 30min 不改; 与之相关的 SC-20 / Impact 表 constants.py 行 / §2.3「放宽到 SWEEP_TTL 同量级」残余风险段 / 闸门状态 item 3 中 (iii) 落点, 在 rework v3 一并回撤 (R3 核验席 minor-1 已点名这四处)。

#### §2.3 overlap 消费

`linked_issue_overlap[]` 非空 (或 `unknown_schema_claims > 0`, 见 §2.4) ⇒ **在起草前**经 `AskUserQuestion` 请裁。

> **⚠️ 无人值守 (Layer 2) 降级分支 (R2/M-15, editlist FIX-16)** —— 否则本节与 AD10「唯一人类参与点在 S7_AWAITING_MERGE」正面冲突:
>
> **判据 (可机械)**: `state_scanner.coordination.unattended == true` (**新 config key**, type boolean, **default false**; 在 `config-loader` 登记并在 `DEFAULTS.json` 注册; **取值路径钉死为 aria-runner 容器镜像内 `.aria/config.json` 的 `state_scanner.coordination.unattended: true`** —— R6/CR M8 + R5/code-simplifier M4: 旧写「容器镜像 / Nomad task env」二选一混写, 而 env 三腿明写不在本 Spec, 并列未钉等于生产进入条件未定义; Nomad env 路径仍属 follow-up #5) ⇒ 走本分支: **零 `AskUserQuestion` 调用**, 改为把碰撞写进 handoff 的待复议段并置 `awaiting_owner`, A.1 继续但结论待 owner 复议 (Rule #10: AI 不自行放行, 但也不在无人处死等)。
>
> **不得**以「`AskUserQuestion` 看起来不可用/没人应答」做运行期推断 —— `allowed-tools` 是随 plugin 分发的**静态 frontmatter**, Layer 2 容器加载同一份 SKILL.md, 声明面完全相同; 且 C1 已把 `AskUserQuestion` 加进 `phase-a-planner` (见 §3) ⇒ **两个宿主都声明持有该工具, 该谓词求值恒为「可用」, 本分支永不进入**。这正是「C1 扩权亲手抹平了旧判据」的形状。
>
> **配套三处 (缺一即互相拆台)**: ① `config-loader/SKILL.md` 登记该 key (Impact 表); ② `DEFAULTS.json` 注册 (Impact 表, 与 R2/M-17 第 5 项同一行); ③ **SC-26** 钉行为 (`unattended == true` 且 overlap 非空 ⇒ 零 `AskUserQuestion` + handoff 出现 `awaiting_owner`)。
> **已知限 (成文)**: 本 Spec 只定义 key 与 A.1 侧的消费; **Layer 1→2 的 env 传递三腿契约** (write + HCL declare + consumer import, memory `feedback_env_propagation_3_leg_contract`) **不在本 Spec** —— 缺 import 会静默 fallback 到 `false` (即「照问不误」), 转 A.2/follow-up。

- **告警须含**: 对方 track-id / owner-container / claimed_at / **双方 `linked_issue` 原始串** (org 不参与匹配, 回显原串是误配的唯一人工判别手段) / `status`;
- **选项 (按对方 `status` 分档 —— R2/M-17 第 3 项: §2.4 让终态可见之后, 旧的三选项集不再覆盖新出现的两档)**:

  | 对方 claim 的 `status` | 该档下的选项集 | 为什么不同 |
  |---|---|---|
  | `active` (原有唯一档) | 「另起」/「**请对方容器的 owner 释放其 claim 后再开始**」(人工协作动作 —— 本容器**无**任何可执行命令: 实读只有无差别 `--sweep-stale`, 无定向 release, D6; R6/TL M3 改措辞) /「并轨」(两轨合一: 被并掉的一方各自 release 自己的 claim, 落点见 §5.2) | 对方在做, 三选项都指向「怎么和一个活着的轨共处」 |
  | **`done`** (§2.4 新可见) | 「**复用对方产出, 本轨不起 Spec**」(⇒ 按 §5.2 走 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`) /「基于其产出起后续 Spec」/「另起 (说明差异)」 | **「释放对方 claim」在本档机械上不可达, 不是推理而是实读结论 (rework v3 补证)**: `release_claim_by_track` 的匹配条件含 **`and rec.status == "active"`** (`lib/claim_lifecycle.py:427`), 非 active 的 claim 一律不匹配 ⇒ 对一条 `done` claim 调 release **必然返回 `claim_not_found`** (`:430`)。「并轨」则是**协作决定**而非机械动作, 对已完成的轨无对象可并。⇒ 两项在本档列出来即误导 |
  | **`abandoned`** (§2.4 新可见) | **⚠️ 必须先分辨来源 (R4/K6)** —— 实读 `lib/gc.py:324` 逐字「Number of stale active claims **rewritten to** `status='abandoned'`」, 而 `ClaimRecord` **无 swept 标记** ⇒ `abandoned` 有**两种来源**: (1) 对方**显式** release; (2) `--sweep-stale` 的 **GC 产物** (对方可能仍在做, 只是超 24h 没刷心跳)。**本 Spec 不得把二者合并渲染**: 在两者不可分辨的前提下, `abandoned` 一律按「**可能仍在制, 按 `active` 同档请裁**」处理, 并在告警里写明「该状态可能是 GC 产物」。**代价成文**: 这会让「对方真的退出了」也被请裁一次 —— 用一次多余的请裁换「不误判对方已退出」, 方向正确 (零证据不得当正证据)。**给 `ClaimRecord` 加 swept 标记以真正分辨二者, 记 follow-up, 不在本 Spec** | 见左 |
  | **`unknown`** (§2.4 独立键) | 「**按存在处理**: 视同 `active` 请裁」 | 存在性已确认、内容未知 ⇒ 不得降格为「无碰撞」, 也不得与 `done`/`abandoned` 同档 (§2.4 四态表) |

  上表**不新增机制**, 只是把 §2.4 已经让其可见的 status 值, 在消费面补上对应的选项集。
  > **「接手」不是一键动作 (spike S3 实测)**: `release_claim_by_track` 只匹配调用者**自己的** container (`claim_lifecycle.py:425`), **无任何函数支持*定向*释放某个指定容器的 claim**; 且既有 `_takeover_eligible` 因含容器段后两轨必然不同 track_id 而**对本场景不可达**。
  >   **⚠️ 事实订正 (R1-fix/C5, 主控实读)**: 原文写「无任何函数支持释放别的容器的 claim」**为假** —— `release_gate.py --sweep-stale` 的 help 逐字写着「active 且 heartbeat 超 STALE_TTL → abandoned (**跨 container**)」。存在的是**无差别的陈旧清扫**, 不是定向接手。⇒ 「两步人工」的结论仍成立 (sweep 不能用来「接手某条特定的轨」), 但理由须改为「**只有无差别 sweep, 没有定向 release**」。
  >   **⚠️ 与 §2.2 复合的残余风险 (R1-fix/C2 关联; rework v3 按 (iii) 撤销重写, 并按 R2/M-8 改为双向)**: §2.2 的「谁调 heartbeat」已落版 ((ii): AI 编排层挂 `/state-scanner` 入口, 受 `coordination.enabled` 门控)。**(iii) 已撤销 ⇒ `STALE_TTL` 维持 `1800` (30min)**, 旧版「放宽到 `SWEEP_TTL` 同量级」的整套推理**随之作废**, 不再是本 Spec 的一部分。**现在的准确状态**:
  >   - **信号 A — reconcile 的 takeover-eligible 软信号** (`lib/reconcile.py:154-163` 的 `_is_stale()`, 末行 `return age_seconds > STALE_TTL`): 阈值 = `STALE_TTL` = **1800s / 30min** (`lib/constants.py:36`), **可逆** (下次 read 即可翻转)。本 Spec 之后 **不变** —— 这是**已知的残余风险**: 编排层漏跑一次 (>30min) 即被标 takeover-eligible;
  >   - **信号 B — `--sweep-stale` 的不可逆清扫**: 阈值 = `SWEEP_TTL` = **86400s / 24h** (`lib/constants.py:51`) —— 实读 `lib/gc.py:338-344` 的 `def sweep_stale_active(` 其 `stale_ttl_seconds: int = SWEEP_TTL` (**默认即 `SWEEP_TTL`**), 且 `scripts/release_gate.py:141` 的 `sw = sweep_stale_active(repo, now=ts)` **未传覆盖**。本 Spec 之后 **不变**, 且**与 `STALE_TTL` 无关** (从来就不读它);
  >
  >   ⇒ **残余风险 (成文, 不假装覆盖)**: advisory 的 takeover-eligible 窗口**仍是 30min**。**主检测责任由 overlap 通道承担** —— 实读 `lib/collision.py:265-292` 全函数**不做新鲜度过滤**, 对 stale claim 同样可见 (这正是 §2.1「为什么必须含容器段」第 3 点); **同名通道 (7c) 只在 30min 内有效**, 30min 后走 7d「No prompt needed」零 surface。**两个方向都要说**: (a) 不改 `STALE_TTL` ⇒ 软信号假阳性窗口窄 (漏跑一次即标 stale), 代价是 advisory 噪声; (b) 改大 ⇒ 假阳性少但真 stale 的轨更久不可 takeover。owner 2026-08-23 选 (a), 本 Spec **不再对该权衡提出任何断言**。
  >   ⇒ 措辞即定义, 避免实现者以为有一键路径。**跨容器 release 不在本 Spec 引入** (写别人的 claim 是权限面变更, 应独立评估);
- **不硬阻断** (撞 §非目标与 AD10), 但**也不是 AI 渲染一行后自行决定** —— 「继续起草」是对已知碰撞的处置决定, 属 owner 权限面 (Rule #10)。**advisory 的含义是机制不阻断, 不是 AI 可自行放行。**

#### §2.4 终态可见 + 传递链 (R3/C2)

`done` / `abandoned` 的同 issue claim **必须可见** —— A.1 场景下 `done` 恰恰是最该看见的信号 (「对方已经做完了」)。`lib/collision.py:268` 的 `_TERMINAL` 会直接 skip 它们 (**rework v3 行号订正**: 旧版写 `:210` 是 `cb6bd5d` 口径, aria `d50f9c3` 上为 `:268`)。

> **⚠️ 事实订正 (R1-fix/C4, 3 席 + 主控实读; rework v3 复读 aria `d50f9c3`)**: `lib/collision.py:268` —— `_TERMINAL = ("done", "abandoned", "unknown")` (函数内局部变量)。
> - **不含 `yielded`** ⇒ `yielded` **今天就已可见**, 不需要本机制去救; 原文把它列进来是**错的事实断言**, SC-8 的该子例 **baseline 即绿** ⇒ **SC-8 的场景列已同步删去 `yielded`** (R2/M-9: 旧版订正了正文却没同步 SC, 是「订正与断言脱钩」);
> - **含 `unknown`** ⇒ 它被 skip 而原文**完全没讨论**。**但旧版对 `unknown` 的定性也是错的** (rework v3 按 editlist FIX-12 订正): `unknown` 是 **reader-only sentinel**, 它一定对应一个**真实存在**的 claim 文件 ⇒ 它是「**已确认存在一条竞品 claim, 只是本读者读不懂其 schema 版本**」的**正证据**, **不是**「零证据」。把它和 fetch 降级 (真的什么都没取到) 归为同一极性, 是把正证据降格 —— 与 §2.5「零证据不得当正证据」**互为镜像**的同一类错误。四态措辞见下方表。

##### §2.4a `unknown` 走独立通道 (editlist FIX-03, ⭐ 承重) —— 经 overlap 通道**结构性不可达**

> ## 🔴 K5 (R4) — `unknown_schema_claims` **必须有失败态**, 否则 R2/M-4 在它自己的修复里复发 (2026-08-27 补, 未经审计轮)
>
> **R4/silent-failure 实读**: 本键与 `linked_issue_overlap` 共用 `scripts/phase1_gate.py:1231-1238` 的**同一个 `try:`**, 
> 而现有 `except` **只赋 `linked_issue_overlap`**。按本 Spec 把门控放宽为 `if args.linked_issue or args.include_terminal:` 后,
> `read_claims` 抛异常时 `unknown_schema_claims` **静默缺席** ⇒ 而 §2.5 四态表把「键缺席」定义为「**未检测**」,
> 消费方 `.get(k, 0)` 读成「**0 条 unknown**」—— **零证据被当成正证据**, 正是 R2/M-4 要修的病, 在 M-4 自己的修复里复发
> (memory `feedback_fix_recurs_in_its_own_fallback_path`)。
>
> **落版**: `except` 分支**必须同时**赋两个键 —— `out["linked_issue_overlap"] = None` **与** `out["unknown_schema_claims"] = None`,
> 外加 `out["linked_issue_overlap_error"] = <非空 token>`。⇒ **§2.5 四态表的第四态相应改为**:
> 「`linked_issue_overlap == null` **且** `unknown_schema_claims == null` 且 `linked_issue_overlap_error` 非空 ⇒ 本轮未取到任何证据」。
> **`unknown_schema_claims` 的合法取值域自此为 `int | null`, `null` ≠ `0`** —— 消费方**不得**用 `.get(k, 0)`。
> **新增 SC-33 (代码, CLI 全链路)**: 夹具让 `read_claims` 抛异常, 带 `--include-terminal` 跑 CLI ⇒ 输出中 **两个键都是 `null`** 且 error 非空;
> **怎么会红**: 只赋 `linked_issue_overlap` 的实现会让 `unknown_schema_claims` 缺席 ⇒ 必红。**baseline 必红**。

**先说为什么不能走 overlap**: `unknown` 被**两道门**丢弃, 且第二道**与 `_TERMINAL` 无关** ——

1. `lib/collision.py:272-273` 的 `if c.status in _TERMINAL:` / `continue`;
2. `lib/collision.py:274-275` 的 `if not getattr(c, "linked_issue", None):` / `continue` ← **第二道门**。`lib/claim_schema.py:165` 的 `parse_claim(` 在 unknown 分支构造 sentinel 时 (`:222-229` 一带) **根本没传 `linked_issue`**, dataclass 默认为 `None` (`lib/claim_schema.py:130`: `linked_issue: Optional[str] = None`) ⇒ **即便把 `unknown` 移出 `_TERMINAL`, 下一行立刻丢弃, 行为逐字节不变**;
3. 且 sentinel 的 `track_id` / `container` / `claimed_at` **全为空串** ⇒ 即使强行放行, §2.3 要求回显的三项全是空字符串。

> **实测复现 (rework v3, 直调 lib)**: `parse_claim({... 'schema_version':'99', 'linked_issue':'10CG/aria-plugin#122' ...})` → `status='unknown'`, **`linked_issue=None`**, `track_id=''`, `container=''`, `claimed_at=''`; 随后 `linked_issue_overlaps([rec], 'my-track', '10CG/aria-plugin#122')` → **`[]`**。⇒ **无论加多少 flag, 该通道恒空**, 除非同时改 `parse_claim` 保留 sentinel 的 `linked_issue` (schema 读取语义变更, blast radius 超本 Spec)。

**⇒ 处置 = 另开一条 additive 输出键 `unknown_schema_claims: int`**:

- **取值**: `read_claims(repo).claims` 中 `status == "unknown"` 的**条数**, **不经 `linked_issue` 匹配** (它读不到);
- **门控**: 该键**仅在传 `--include-terminal` 时**出现。A.1 模板恒带该 flag ⇒ 恒有; Phase B 两个入口都不带 ⇒ **输出逐字节不变**, 与 §非目标「不动 Phase B 入口现有认领」自洽;
- **实现落点**: 把 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`, 块内 `read_claims(repo)` **只调一次**, 然后按 `args.linked_issue` / `args.include_terminal` 各自填键 (**rework v3 行号订正**: editlist 写于 2026-08-04, 引的是 `:1229`; 实读 aria `d50f9c3` 为 **`:1230`**);
- **消费面措辞**: 见下方四态表第三行, **不得**并入 `linked_issue_overlap[]`, **不得**与 `done`/`abandoned` 同档;
- **已知限 (成文, 只交付一半并说明哪半)**: 本轮**不给**这 N 条提供**路径/身份** —— `read_claims` 的返回类型 `ReadClaimsResult` (`lib/coordination_ref.py:119` 定义 `class ReadClaimsResult(NamedTuple)`, `:596` 定义 `def read_claims(`) 只有 `claims/errors/ref_exists`, unknown 记录进 `claims` 时既无 path 也不入 `errors` ⇒ 供路径要改 NamedTuple 字段, blast radius 超本 Spec, **转 follow-up**;
- **由 SC-24 钉住** (CLI 全链路)。

##### §2.4b 四态契约 (editlist FIX-12(a) + R2/M-4 的修复)

| 信号 | 含义 | 消费面措辞 |
|---|---|---|
| 键**缺席** | **未检测** —— 未传 `--linked-issue` (**与是否传 `--include-terminal` 无关**: 后者独立控制 `unknown_schema_claims` 键, 与本表正交。R6/TL M2 订正旧定义「既未传 A 也未传 B」—— 哨兵轨恒带 `--include-terminal` 而不传 `--linked-issue`, 是最常见形态而非例外) | 「本轮**未检测**」 |
| `linked_issue_overlap == []` | 已检测, 无碰撞 | 「无碰撞」 |
| `unknown_schema_claims > 0` | **已确认存在** N 条竞品 claim, 本读者读不懂其 schema | 「已检测到 N 条无法解析的 claim —— **存在性已确认、内容未知, 按存在处理**」 |
| `linked_issue_overlap == null` **且** `linked_issue_overlap_error` 非空 | 本轮**未取到任何证据** | 「**未能核实**, 建议重试」 |

> **⚠️ R2/M-4 的修复 (逐字)** —— 没有它, 上表第 2 行与第 4 行在实现上**不可分辨**: 实读 `scripts/phase1_gate.py:1236-1238` 现为 `except Exception as exc:` → `logger.warning(...)` → **`out["linked_issue_overlap"] = []`** ⇒ **异常路径把「什么都没取到」写成了「已检测, 无碰撞」, 且这一步在 `out` 层, 不受 `GateResult.error` 覆盖** (零证据当正证据)。
> **改为**: `except` 分支**不得再写** `out["linked_issue_overlap"] = []`; 改为 `out["linked_issue_overlap"] = None` + `out["linked_issue_overlap_error"] = <非空 token>`。
> **由 SC-25 钉住**「把『已确认存在竞品』与『本轮没取到证据』渲染成同一句的实现必红」+ 断言异常路径的 `null` / `error` 两字段。
> **与 §2.5 的关系**: §2.5 的 `GateResult.error = "fetch_degraded"` 管的是**取 ref 这一步**降级; 本条管的是**算 overlap 这一步**抛异常。**两条都要**, 少任何一条都有一段路径会静默返回 `[]`。

**`include_terminal` 的传递链 (**四**段缺一不可 — R1-fix/C6 补第 0 段)**:

0. **`lib/collision.py` 的 `linked_issue_overlaps` 增 keyword-only 形参** `include_terminal: bool = False` —— 实读 aria `d50f9c3` 的 `lib/collision.py:230-234` 现签名为 `def linked_issue_overlaps(claims, own_track_id, own_linked_issue)`, **三参数, 无该形参**; 不加则 `_main()` 的调用处 (`scripts/phase1_gate.py:1233-1235`) 传参直接 `TypeError`。**⇒ `lib/collision.py` 已补入 Impact 表** (R1 rework 核验 major-2 补, 原表零覆盖)。
   > ⚠️ 与前置 Spec 的边界 (**历史**): `linked-issue-normalization` 的 §非目标写「签名与返回 schema 不变」。本段**要改签名** ⇒ 两 Spec 须协调: 建议由**本 Spec** 承担该签名变更 (前置 Spec 只改内部谓词), 并在前置 Spec 的非目标处加一句「`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面」。
   > **✅ 该协调项已完全闭环, 本轮无须再动姊妹 Spec (rework v3 实读复核, 取代旧版的「已解」记述)**: 姊妹 Spec **已 ship 并归档** (`openspec/archive/2026-08-23-linked-issue-normalization/`, v1.67.0 合并提交 `ca52d1c`), 且它在 ship 前**自己写入了**母 Spec 请求的关闭条款 —— 实读 `sed -n '256,260p' openspec/archive/2026-08-23-linked-issue-normalization/proposal.md` 得 `:257` 「⭐ **`include_terminal` 形参由 `a1-entry-claim` 引入, 不属本 Spec 变更面** (owner 裁定 2026-08-08)」+ `:259` 逐字「母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**」。⇒ **R1 editlist FIX-11 要求的「对姊妹 Spec 的必需编辑」已由姊妹自己完成**, 本 Spec **不编辑归档件** (归档件不可回改)。
   > **行号基线**: 姊妹 Spec 的合并使 `collision.py` 下游行号整体下移 —— `_TERMINAL` 由 `cb6bd5d:210` → **`d50f9c3:268`**; `if c.track_id == own_track_id` 由 `:219-220` → **`:278-279`**; `linked_issue_overlaps` 签名由 `:177-181` → **`:230-234`**。本 Spec 正文与 Impact 表引用的 `collision.py` 行号**统一以 aria `d50f9c3` 为准**, 逐条核对见下方「事实断言逐条实读清单」#3/#4/#5/#6/#16。
1. `phase1_gate.py` 新增 CLI flag `--include-terminal` (store_true);
2. **在 `_main()` 的现有调用处** (`scripts/phase1_gate.py:1233-1235`, 即 `out["linked_issue_overlap"] = linked_issue_overlaps(result.claims…)` 那条语句) 加关键字参数 —— **不碰** `run_gate` / `_run_gate_impl` 签名;
   > R3/C2 实测: `linked_issue_overlaps` 生产代码**只有这一处调用**, 位于 `_main()` (`scripts/phase1_gate.py:1173` 定义)、在 `run_gate` (`:1032` 定义) 返回**之后**独立追加; `_run_gate_impl` (`:335` 定义, 至下一个顶层 def `_telemetry_path` `:950` 前 (R6/CR m6 订正: `run_gate` `:1032` 不是紧邻的下一个顶层定义) —— R1 rework 核验 minor-4 订正: 原文误记 `334-1075`, 见「事实断言逐条实读清单」#17) 对它 grep 命中 **0**。原 R2-fix 写「`run_gate` 签名透传」**架构上就是错的** —— 照它做会改错函数, 精确复现它自己要修的「生产不可达」。
3. A.1 调用模板**显式带该 flag**。

**SC 的断言层必须是 CLI 全链路**, 不是直调库函数 —— 否则「参数没接到 CLI」的实现仍能绿。

#### §2.5 开关与降级

- **受 `state_scanner.coordination.enabled` 控制**, `false` ⇒ **零调用** (与 Phase B 对称; 由 SC-9 钉 A.1 侧、SC-28 钉 heartbeat 侧, 是**同一条**开关的两半)。`phase1_gate` **本身不读 config**, skip 判断在调用方 SKILL.md 层 ⇒ 该条件须**显式写出**, 否则 opt-out 项目在 A.1 仍被强制写 claim + 推远端 (对未配 coordination ref 的第三方是外向副作用);
- **Level 1 例外 (R5/skill-reviewer M4 → R6/CR 母 C1 入正文)**: `phase-a-planner` 判定 **Level 1** (`skip_if: complexity: Level1` 命中, 实读 `phase-a-planner/SKILL.md:67`) ⇒ **前置 claim 零调用** (不写 claim、不推远端) —— 否则每个 typo 修复写一条永不 release 的僵尸 claim + 一次外向 push。由 **SC-9 (B)** 臂钉住; rule6_note (a) 同步。`spec-drafter` 直调路径无 Level 判定 ⇒ 不适用本例外 (它本就只在 Level 2/3 起草时被调);
- **⚠️ 「不传 `--linked-issue`」是键缺席, 不是空列表 (R2/M-3, rework v3 补 —— 旧版全文零提及)**: 实读 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 是**整块门控** —— 不传该实参时, `out` 里**根本不出现** `linked_issue_overlap` 这个键, 而**不是**出现一个空列表。⇒ 消费面必须先判**键是否存在** (四态表第 1 行「本轮未检测」), 把「键缺席」读成 `[]` 就是把「没查」读成「查了没有」。这也是 §6 缺口表首行 (`无` token 轨零输入) 的机制来源;
- **fetch 降级须进 `error` 契约**: `GateResult.error` 的 docstring (`scripts/phase1_gate.py:210`) **早已预留 `"fetch_degraded"` token 但从未被赋值** (全文无任何 `error=` 赋值用到它 —— 又一个「已 ship ≠ 能用」)。降级时消费面按「**未能核实**」措辞, **不得**渲染成「无碰撞」(零证据不得当正证据)。**与 §2.4b 的 `linked_issue_overlap_error` 是两条不同路径, 不可互相顶替**。

### §3 入口覆盖 (S6)

**实测差距**: coordination ref 里 **2 个**容器, 而 handoff 的 `owner-container` 出现过 **9 种** ⇒ **至少 7 种身份从未留下 claim**。

⇒ **A.1 须双落点**, 与 Phase B 对称 (后者有 `phase-b-developer` + `branch-manager` 两处):
1. `phase-a-planner/SKILL.md`;
2. **`spec-drafter/SKILL.md`** —— 它 `user-invocable: true` (实测 `skills/spec-drafter/SKILL.md:9`), 可直接绕过 phase-a-planner。

> **⚠️ 双落点是本 Spec 的核心杠杆, 却在旧版 SC 全表零覆盖 (R2/M-11)** —— rework v3 补 **SC-22**: 断言两处 SKILL.md **各自**含标题级 `前置: REQUIRE claim` 步骤块 (正则形态 + 非围栏内 + 四字面量 + 幂等谓词), 宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py` (**扩它, 不另起文件**)。
>
> **两落点同时命中时谁让步 (幂等分工, R2/M-11 后半 + editlist FIX-13)**: `phase-a-planner` 是**主路径** (它的 A.1 会主动委派 `spec-drafter`); `spec-drafter` 的落点只在 (a) **未经 `phase-a-planner` 直接调用** (`user-invocable: true` 路径), 或 (b) `phase-a-planner` 因 skip 条件未走到认领 时生效。**幂等谓词** (`check:` + `if_missing:`, 即 SC-22 第 ③ 项) 保证正常委派路径上**只写一条 claim** —— 没有它, 一次 A.1 会写两条 claim + 两次外向推送, 该实现必须能被 SC-22 判红。
> **⚠️ 落点内部的具体行号 (`phase-a-planner` 的委派动作在第几行 / skip 条件在第几行) 本轮未实读 ⇒ 不写**; A.2 拆任务时须实读补钉 (零发明行号)。

> ## ✅ 阻塞性前提 — 已裁 (R1-fix/C1 — 4 席独立命中 + 主控实读 → 2026-08-22 owner 裁定落版)
>
> **两个指定落点的 `allowed-tools` 都不支持本机制的核心动作。** 实读 frontmatter (**rework v3 复读 aria `d50f9c3` 仍逐字未变**, 见下方「事实断言逐条实读清单」#1/#2):
>
> | Skill | `allowed-tools` (逐字, 变更前) | 缺 |
> |---|---|---|
> | `phase-a-planner/SKILL.md:9` | `Read, Write, Glob, Grep, Task, Skill` | **无 `Bash`** · **无 `AskUserQuestion`** |
> | `spec-drafter/SKILL.md:10` | `Read, Write, Glob, Grep, AskUserQuestion` | **无 `Bash`** |
>
> ⇒ §2 的 `python3 .../phase1_gate.py` 命令**在两个宿主上都跑不了**; §2.3 的 `AskUserQuestion` 请裁**在 phase-a-planner 上也跑不了**。
>
> **⚠️ 扩权与 AD10 的关系 (R2/M-15 配套, rework v3 补)**: 给 `phase-a-planner` 加 `AskUserQuestion` **不在 Layer 2 新增人类参与点** (AD10: 唯一人类参与点是 S7_AWAITING_MERGE) —— 该分支由 §2.3 的 `state_scanner.coordination.unattended` 谓词在**调用前**短路; 无人值守下走 handoff + `awaiting_owner`, 不发问。**反过来也成立**: 正因为扩权后两个宿主都声明持有 `AskUserQuestion`, 「工具是否可用」**不能**再作为无人值守判据 (详见 §2.3)。
>
> **这是整份 Spec 的阻塞项** —— 主机制在它自己指定的执行位置上不可调用, 而三轮审计 + 六条 spike 全都没查过 frontmatter。
>
> owner 2026-08-22 就此下裁。**以下逐字取自 `git show 86540f2:openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`** (R1 rework 核验 major-3 订正 —— 上一轮此处只保留了「采 (a) 扩权」前半句, 「理由」与「落版义务」两个从句被删并换成下方另起的 (a)/(b) 转述, 与原文有实质偏差且未请复议; 现恢复完整原文字面):
>
> > **✅ owner 裁定 (2026-08-22): 采 (a) 扩权** —— phase-a-planner 加 `Bash, AskUserQuestion`; spec-drafter 加 `Bash`。理由: (b) 放弃 `/spec-drafter` 直调路径的覆盖, 而入口覆盖 (S6: 9 种身份 7 种无 claim) 正是本 Spec 核心目标; 扩权风险由 harness 权限系统兜底 (Bash 调用仍逐条过 permission 配置)。落版义务: Impact 表补两个 SKILL.md 的 `allowed-tools` 变更 + Rule #6 按能力面变更申报 benchmark。
>
> **落版 (AI, 2026-08-23)**:
> - **(a) 扩 `allowed-tools`** [已采纳]: 判否 (b) 是因为 (b) 放弃 `/spec-drafter` 直调路径的覆盖, 而入口覆盖 (S6: 9 种身份 7 种无 claim) 正是本 Spec 核心目标; 扩权风险由 harness 权限系统兜底 (`Bash` 调用仍逐条过 permission 配置);
> - **(b) 改由已持 `Bash` 的宿主代调** [已否]: 例如经 `Task`/`Skill` 委派, 或把认领动作前移到 `state-scanner` 的阶段 4。会改变「A.1 起草前」这个时点的语义且放弃 `/spec-drafter` 直调覆盖, 与 §3 核心目标冲突, 不采纳。
>
> **落版执行** (owner 裁定原文的「落版义务」):
> 1. **Impact 表补两行, 逐字标明变更前后** —— 见下方 §Impact 表 `skills/phase-a-planner/SKILL.md` / `skills/spec-drafter/SKILL.md` 两行 (frontmatter `allowed-tools`);
> 2. **Rule #6 判据影响** (R1 rework 核验 major-4 订正): `allowed-tools` 扩权是 skill **能力面**变更, 影响该 skill **全部**运行场景 (含既有 AB 套件的既有 eval case)。按 `standards/conventions/skill-benchmark-exemption.md` §1「逐 hunk 判, 不逐文件判」核验: `aria-plugin-benchmarks/ab-suite/phase-a-planner.json` / `spec-drafter.json` **两套件均实存** (2026-08-23 实核, 各 2 eval case) ⇒ 该能力面 hunk 落判据表**第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」** —— **须照跑现有两套件**; 与此同时, 本 Spec 新增的 A.1 claim 行为 (a)(b)(c, 见下方 rule6_note 中段) 各自独立归入判据表**第三行「套件覆盖外」**并建定向 fixture。二者**不互相替代**: 照跑 AB 验的是「扩权后 skill 在既有 eval 场景下行为是否漂移」, 定向 fixture 验的是「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」。**订正**: 上一版此处误判「能力面部分不单独申请豁免、也不需要单独判据, 由覆盖该 diff 的定向 fixture 同批覆盖即可」——两套件确实实存, 该误判与 owner 原话「Rule #6 按能力面变更申报 benchmark」(即: 该去申报/跑一次 benchmark) 实质相悖, 现按核实结果订正为「照跑」, 与 owner 原话字面对齐。此判断记入下方 rule6_note 段, 供 A.2 复核。
>
> **✅ 上一轮的「⚠️ 实读订正 · 请 owner 复议」(R1 rework 核验 major-3(b)) 已闭环**: 该条自陈「核实结论 (两套件实存 ⇒ 应照跑) 与 owner 原话字面本就一致, 技术处置**无需另行复议**」, 仅为上一轮措辞偏差的订正留痕; owner 2026-08-23 裁定未对其提出异议。其原文 (逐字) 见 [审计轨 §4](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#4-3-实读订正--请-owner-复议原文-已闭环)。**若 owner 认为「申报 benchmark」另有所指 (例如指走一遍 `/skill-creator` 完整流程, 而非本版采用的「现有两套件全量跑一遍, 零裁量」), 请在 R3 时指出。**

> **口径待定 (S6 附带发现)**: `owner-container` (形如 `simonfish/bfe8285d`) 与 claim 的 container 段 (`bfe8285d`) **口径已经不同**。本 Spec 采用 claim 侧口径 (uuid), 并把「两标识关系需成文」记为 follow-up —— **不在本 Spec 统一二者** (那会牵动 handoff frontmatter 规范, 属 standards 变更)。

### §4 竞品 spec 探针 — ⛔ **整节已迁出** (owner 2026-08-23 方向 b)

> **迁往**: [`openspec/changes/sibling-spec-probe/proposal.md`](../sibling-spec-probe/proposal.md) —— 原 §4 的全部内容 (`sibling_spec_probe.py` 新脚本 / 扫描范围含 `archive/` / per-round 入口挂载 / fetch 代价与超时预算 / 规模上限 / 消费面与 exit code / 盲区声明) 由该 Spec 承担, 连同 R2 簇 **M-1** (「同 issue」匹配谓词未定义)、**M-5** (「各自默认分支」取法未定义 + in-flight 竞品不可见)、**M-6 的 audit-engine 档**、**M-17 的「§4 无 stdout 契约」子项**, 以及 R1 editlist **FIX-10**。原 SC-16/17/18/19 一并迁出 (见 Success Criteria 表内保留的迁出行)。
> **为什么迁**: R2 的 M-1/M-5 都是 **R1 still-open** 且落在 `audit-engine` 这个与 A.1 认领**不同的宿主**上; `ab-suite/audit-engine.json` 实测**不存在** (rework v3 实核), 使原 rule6_note 的「覆盖外」档按判据表「缺一照跑」根本不成立 —— 这三件都属探针自己的收敛面。
> **依赖方向 (逐字, 不得读成隐式前置)**:
> - **探针 spec 不是主体的阻塞前置。** 主体的 §6 缺口表里「legacy 轨 / 一方跳过入口」两行原写「§4 探针**部分**覆盖」(**R3/TL-M5**: 迁出时必须保留「**部分**」这个限定词 —— 探针自测覆盖率 90.5%, 非全覆盖; 丢掉限定词会把一个已知缺口读成已闭合), 现按实际改为「**由 `sibling-spec-probe` 覆盖, 未 ship 前该缺口无覆盖**」—— 成文, 不假装覆盖。
> - **主体是探针 spec 的语义母体**: 探针的「同一条轨」「同一个 issue」判据一律引用主体 §2.1 的 track-id 契约与 `linked_issue` 语义, 不得自行重定义。

### §5 claim 生命周期 — A.1 引入的新退出路径

> **⚠️ 本节按 owner 2026-08-30 裁定 1A 重写。** 旧版 (rework v3 → R5) 的复杂度来自「issue 派生形下同一 issue 的 N 个方向共用同一个 track_id」—— 由此需要二分谓词 (§5.1)、`spec_slug` 三元组 release (§5.3)、`track_form` 字段与 D12。**1A 后每个方向 = 自己的目录名 = 自己的 track-id = 自己的 claim**, 「结束一个方向连坐释放其他方向」在结构上不可能发生: `release_claim_by_track` 按 `(container, 归一 track_id)` 定位 (`lib/claim_lifecycle.py:377` 定义, `:425-427` 三个合取条件含 `rec.status == "active"`), 不同 slug 就是不同 track_id。旧版 §5.1 / §5.3 / K1 / K4 原文见审计轨 §6。

#### §5.1 语义单元 = (container, spec-slug) —— 唯一形态, 无分档

- 一条 claim 表示「**本容器在做这份 Spec**」。同一容器对同一 Spec 跨 session 重新认领会产生多条 claim (每 session 新 session_id), 它们**同 track_id** —— 这正是 `release_claim_by_track` docstring 逐字描述的常态: 「If several active claims match (**same container re-claimed a track across sessions — the NORMAL case, since every session mints a fresh session_id and B.0 REQUIRE-claim runs per session**), **ALL matching active claims are released**」(`lib/claim_lifecycle.py:396-399`)。**ALL-matching 在 1A 下是期望行为** (释放的全是同一份 Spec 的 claim), 不再需要任何额外维度去限定它。
- 「是不是同一个 issue」不在 track-id 里, 在 `linked_issue` 里; 同 issue 的两个方向互相可见靠 §2 的 overlap 通道 (`linked_issue_overlaps`, 容器段保证两条 track_id 可辨, §2.1)。

#### §5.2 退出路径表

> **⚠️ 命令形态订正 (rework v3 实读)**: 旧版全文写的 `release_gate.py --status abandoned` **会直接 `parser.error` 退出** —— 实读 `git -C aria show d50f9c3:skills/state-scanner/scripts/release_gate.py | sed -n '236,237p'` 得
> ```python
>     if not args.raw_track_id and not args.sweep_stale and not args.gc:
>         parser.error("至少需要 --raw-track-id / --sweep-stale / --gc 之一")
> ```
> ⇒ 本节所有 release 调用**一律带 `--raw-track-id "<本轨 A.1 原串>"`** (`--status abandoned` 只指定写入的状态值, 不满足「三选一」)。**这条 baseline 即可证伪**: 照旧版字面写的实现连 CLI 都进不去。

| 路径 | 处置 |
|---|---|
| **探索性放弃一个方向** (A.1 试三个方向弃两个) | 每个被弃方向**各自** `release_gate.py --raw-track-id "<该方向 A.1 原串>" --status abandoned`; 仍在做的方向的 claim **不受影响** (不同 track_id)。义务写进两处 SKILL.md 的「前置: REQUIRE claim」块 (SC-22 ⑥ 字面), 行为由 **SC-14(b)** 的定向 fixture 覆盖 |
| **放弃整个 issue** (不再做这个 issue 的任何方向) | = 对该 issue 下本容器的每个方向各做一次上一行。**方向的枚举机制 (R6/TL M4, 不靠 AI 记忆)**: 跑一次 A.1 认领命令 (带该 `--linked-issue`) 读 `linked_issue_overlap[]` 中 `container` 等于本容器的条目 —— 实读 `lib/collision.py:271-279` 该函数**不按 container 过滤**, 只按 `track_id` 自排除, 所以同容器不同 slug 的 claim 会出现在 overlap 里 (这正是 §2.1 代价 (b) 那条 advisory 的正当用途)。**没有「按 issue 批量释放」的命令, 也不新增** (那会重新引入按 `linked_issue` 定位的跨轨写入面) |
| **并轨** (§2.3 `active` 档裁决) | 两轨合一: **被并掉的一方各自 release 自己的 claim** (`release_gate.py --raw-track-id "<该轨 A.1 原串>" --status abandoned`); 对方那条**不由本容器释放** (D6: 不引入跨容器 release), 成文接受它挂到 `--sweep-stale` (R6/TL M3 补行) |
| **复用对方产出, 本轨不起 Spec** (§2.3 `done` 档裁决) | 同「探索性放弃一个方向」—— 释放本轨 A.1 那条 claim; §2.3 该格已给出命令, 本行是它指向的落点 (R6/TL M3 补行) |
| **slug 改名** (Spec 目录改名) | = 换 track-id ⇒ **release 旧 + acquire 新**两步 (`release_gate.py --raw-track-id "<旧串>" --status abandoned`, 再以新串重跑 A.1 认领); `release_claim_by_track` 按 `(container, 归一 track_id)` 定位、**不依赖 session**, 可直接照字面实现。**由 SC-15 (代码) + SC-22 ⑥ (文本) 钉住**。这是 1A 的成文代价 (a) |
| **A.1 成功并走完循环** (最常见, R2/C-C) | **A.1 原串即 carry-id, B.0 与 D.2b 逐字节复用** (§2.1b) ⇒ D.2b 的 `release_claim_by_track` 能匹配到 A.1 那条 claim, 且 ALL-matching 只触及同一份 Spec 的跨 session claim (§5.1)。**由 SC-23 钉住**。**不靠 sweep 兜底** —— sweep 只是 GC, 不是设计中的释放路径 |
| **D.2b 对偶** | 只有**走完循环**的轨才到 D.2b; 上面「探索性放弃 / 放弃整个 issue / 改名」三条**不经过它**, 故各自显式 release |

#### §5.3 ⛔ 已随 1A 撤销 (原「D.2b 的 release 作用域 —— `spec_slug` 三元组」)

原 R3/TL-C1 判定「方向 1 收尾会把仍在制的方向 2/3 的 claim 一并释放」**只在 issue 派生形下成立** (N 个方向共用 track_id); 1A 后该前提消失, 三元组 release、`--spec-slug` flag、`spec_slug` / `track_form` 字段、K1 (heartbeat 逐字段重建的透传面)、K2 (legacy claim 的 `track_form is None` 悬崖)、K4 (写入端 CLI flag) **全部无对象**。**本 Spec 不新增任何 claim 字段** (§非目标)。原文按字节移入审计轨 §6。

> **保留下来的一条实现纪律 (来自 R5/code-simplifier 选项 B, 对 1A 后仍新写的代码有效)**: `ClaimRecord` 是 `@dataclass(frozen=True)` (`lib/claim_schema.py:69`), 既有 `heartbeat()` 在 `lib/claim_lifecycle.py:244-256` **逐字段重建** 11 个字段。本 Spec 新增的 `heartbeat_by_track` **须用 `dataclasses.replace(existing, heartbeat_at=…)`**, 不复制那段逐字段重建 —— 对未来任何 additive 字段免疫 (memory `fix-the-class`)。已登记进 Impact 表该行。
### §6 残余缺口 (成文, 不假装覆盖)

| 缺口 | 窗口 | 覆盖它的机制 |
|---|---|---|
| **⭐ 本轨的「Linked Issue / 关联 Issue」token 不产生合法 canonical 值 (哨兵 `none`/`无` / `BAD_TOKEN` / `NO_TOKEN`) 或字段缺席 (`NO_FIELD`)** (R2/M-3 + editlist FIX-12(d) 补 —— 旧版全表没有这一行, 而它是**最大的单项缺口**) | 无界 | **无** —— 此时 A.1 模板**必须省略** `--linked-issue` (否则两份无关 Spec 互相误报, 见 §2 的 NEW-01), 而 `scripts/phase1_gate.py:1230` 的 `if args.linked_issue:` 是**整块门控** ⇒ 主机制**零输入**, 且输出里 `linked_issue_overlap` **键缺席** (不是 `[]`, 见 §2.5)。字段可得性由 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md) 承担, **它 ship 前该缺口无覆盖**; 该子 Spec **不是本 Spec 的阻塞前置** —— 本 Spec 在字段缺席时的行为是**已定义的退化** (零输入 + 键缺席), 不是未定义行为 |
| 双方都未 claim 且未 push | 秒级 (claim 推送延迟) | 无 |
| 一方跳过 A.1 直调 `/spec-drafter` | — | **§3 双落点已覆盖** (由 SC-22 钉住两处落点各自存在) |
| 一方 `coordination.enabled=false` | 无界 | 无 (设计如此, opt-out 是项目的权利) |
| legacy 轨 (不用 phase1_gate 的历史/第三方容器) | 无界 | **原写「§4 探针部分覆盖」—— §4 已迁出** ⇒ 现由 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md) 承担, **它 ship 前该缺口无覆盖** (S6: 7/9 身份属此类)。成文, 不假装覆盖 |
| 竞品**已 ship 并归档** (在 `openspec/archive/` 下) | 无界 | **同上** —— 原属 §4 探针的两个专有场景之一, 随 §4 迁出 |
| **存量 active claim 是旧形态** (无容器段) 的过渡期断链 | 至旧 claim 自然 GC 退场为止 | 无 (§2.1b 已知限: 本 Spec **不改写存量 ref**) |
| **slug 过长 ⇒ track-id 退化为不可读哈希** (slug > 55 字符时 `<slug>-<8 hex uuid>` 超 64 ⇒ 整串 sha256; 本仓 `archive/` 历史最长 slug 53 字符, 离阈值 2 字符; hostname 兜底分支 `identity.py:242` 段更长, 更易触发) | 无界 | 机制仍成立 (哈希取完整原串, 两容器仍得不同 id, overlap 通道不死), 只丢「人类可读」这半条 D18 依据; 成文已知限, 不加机制 (R6/TL M1) |

**中心化 spec 登记表: 仍然不做 (spike S6, 依据全换)**。原依据「残余缺口仅秒级」是实质低估, 已作废。新依据: **登记表解决不了这些缺口** —— 它们共同根因是「**没走进入口**」, 换个存储位置不改变这一点, 它是同一问题的另一载体而非解法; 真正的杠杆是**入口覆盖率** (实测 9 vs 2), 即 §3 的方向。登记表的一致性/并发写/GC 是常驻成本, 收益却依赖同一个前提。

---

## 事实断言逐条实读清单 — ⛔ **整表已切出**

> **迁往**: [审计轨 §5](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#5-事实断言逐条实读清单) —— **⚠️ 搬运性质分节陈述 (R3/CR-M-M1 订正 —— 原写「按字节搬运, 未重写任何一句」对 §5 **为假**, 主控担责)**: 审计轨 **§1 (轮次轨迹表)** 是**逐字搬**, CR 席 diff 确认连续块命中; 审计轨 **§5 (事实断言实读清单)** **不是**纯搬运 —— 该表在本轮**先**按新基线 `d50f9c3` 重测重生成 (含新增 #18–#34), **然后**才移出, 与已提交前身相比 22/29 行找不到。§2/§3/§4 各含一条本轮新写的编者注。⇒ 「无损搬运 ⇒ 撤回成本低」这条安全性论证**只对 §1 成立**。34 行断言表 (原 #1–#17 订正 + rework v3 新增 #18–#34) 全部在那里。
> **切分理由 (主控 2026-08-25 裁定, 已标请 owner 复议)**: 该表是**核验证据**不是交付面 —— 与姊妹 Spec 2026-08-07 owner 裁定「交付面与审计史切开」同类; 且它可由 `verify_line_refs.py` 随时重新生成, 不需要人肉维护在交付面里。
> **本文件正文里所有 `文件:行号` 引用的实读基线 = aria 子模块 `d50f9c3`** (= v1.67.1 `58a49e7` + 2 commit)。**复核命令 (逐字)**: `git -C aria show d50f9c3:<path> | sed -n '<N>p'`。主仓语料口径的基线 = `cc1bdef`。
> **正文里形如「见清单 #N」的交叉引用**, 一律指审计轨 §5 表内的第 N 行。
> ⚠️ 审计轨是 append-only 且**不维护与本文件的一致性** —— 若二者行号不一致, **以本文件正文为准**, 并按上面的复核命令重新实读。

---

## 决策记录

| # | 决策 | 依据 |
|---|------|------|
| D1 | ~~「关联 Issue」字段可得性提为 §1~~ ⇒ **⛔ 已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** (owner 2026-08-23 方向 b) | 原依据 `141/13/9%` 已作废 —— rework v3 实测口径见「事实断言逐条实读清单」#30 |
| D2 | ~~字段格式固定 `<org>/<repo>#<n>` + custom check (warning)~~ ⇒ **⛔ 已随 §1 迁出** (同上) | 同上 |
| D3 | track-id = `<spec-slug>-<container_uuid>` (**owner 2026-08-30 裁定 1A 改**; 原 issue 派生形 `<basename>-<str(int(n))>-<container_uuid>` 见审计轨 §6; **容器段的依据不变, 如右**) | **S3**: 不含容器段则两轨同 id ⇒ 被 `lib/collision.py:278-279` 互斥 ⇒ 主机制死 (R2/C1); uuid 不截断不用 label (label 碰撞域不可控且模板鼓励设置)。**⭐ rework v3 补注 —— 更简的备选已被实测证伪**: 「去掉容器段, 靠 reconcile 同名碰撞 (7c) 报警」不成立 —— 7c 只在竞品未 stale 时触发 (`_takeover_eligible` 命中即走 7d「No prompt needed」零 surface), 而 `heartbeat()` 生产调用点为 0 (`lib/constants.py:43-44`) + `STALE_TTL`=1800 ⇒ 事故窗 (48–72h) 内同名通道**结构性静默** (= Aria #180); 而 overlap 通道 (`lib/collision.py:265-292`) **不做新鲜度过滤**, 对 stale claim 同样可见。⇒ **容器段的真正作用是把碰撞检测从新鲜度脆弱的通道挪到新鲜度免疫的通道** (详见 §2.1) |
| D4 (**⛔ 已被 D16 取代 — R3/BA-M2 订正**) | ~~heartbeat 匹配键**改** `(container, track_id)`~~ ⇒ **以 D16 为准: 增 by-track 并存变体, 不改既有 `heartbeat()` 的 `(container, session)` 键**。旧措辞是 R2/M-17 第 2 项点名的两读之一, §2.2「⚠️ 口径统一 (R2/M-17 第 2 项)」段与 D16 已统一而本行残留未同步 (R6/CR m6: 旧引 `:188` 已漂移) | **S1**: `release_claim_by_track` 为**同一 defect** 做过同款修法, 照抄即可; session 落盘方案被它取代 |
| D5 | `include_terminal` 在 **`_main()` 现有调用处**加参数, 不碰 `run_gate` 签名 | **R3/C2** 实测: `linked_issue_overlaps` 只在 `:1233` 被调用 (rework 订正: 原 R3 记 `:1232`, 实读为其下一行), `_run_gate_impl` 零命中 |
| D6 | 「接手」= **两步人工**, 不引入跨容器 release | **S3** 实测无该函数; 既有 takeover 路径对本场景不可达; 写别人的 claim 是权限面变更 |
| D7 | ~~探针自带 fetch, 不称轻量, 配 30s 预算 + 重试~~ ⇒ **⛔ 已随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** (owner 2026-08-23 方向 b) | **S2** 实测数据一并移交该 Spec |
| D8 | A.1 双落点 (phase-a-planner + spec-drafter) | **S6** 实测入口覆盖率是杠杆 (9 身份 vs 2 在 ref); `spec-drafter` `user-invocable: true` 可绕过 |
| D9 | 不建 basename 别名表 | **S4**: 在真实输入总体上别名实例 = 0; 分隔符型别名已由前置 Spec 的 S5 追加覆盖 |
| D10 | 不做中心化登记表 | **S6**: 解决不了「没走进入口」这个共同根因 |
| D11 | ~~探针不阻断, 命中 exit 0; 非 0 仅用于探针自身失败~~ ⇒ **⛔ 已随 §4 迁出** (同 D7) | — |
| **D12** (新) → **⛔ 已随 1A 撤销 (2026-08-30)** | ~~release 的语义单元按 track-id 形态分档; 形态的机械判定式 = additive 字段 `track_form`~~ —— 1A 后只有一种形态, 语义单元恒为 (container, spec-slug) (§5.1); 原文见审计轨 §6 | R2/C-B 的连坐由 1A 结构性消灭, 不再需要判定式; 曾被否决的两个判定式 (从串反推 / 读 `linked_issue`) 也随之无对象 |
| **D13** (新) | **A.1 派生的原串即本 cycle 的 carry-id**, `phase-b-developer` B.0 / `branch-manager` / `phase-d-closer` D.2b 三处逐字节复用 (editlist FIX-14 **选项 A**) | **R2/C-C**: `lib/track_id.py:61-76` 归一四步不含去容器段逻辑 ⇒ 两个不同原串归一后必是两个 track_id, 没有任何归一层能把 A.1 与 D.2b 接上。选 A 而非 B (D.2b 额外再调一次 release) 是因为 A 是**一处定义三处复用**, B 是在收尾处打补丁。**边界**: 只改 carry-id 取值口径, 不改 Phase B 闸门语义 (见 §2.1b) |
| **D14** (新) | `unknown` **另开 additive 键 `unknown_schema_claims: int`**, 不并入 `linked_issue_overlap[]` (editlist FIX-03) | **实测证伪**了「加 flag 让它走 overlap」这一支: `parse_claim` 的 unknown sentinel 不带 `linked_issue` (`lib/claim_schema.py:130` 默认 `None`), 被 `lib/collision.py:274` 第二道门丢弃 ⇒ **该通道恒空**, 与 `_TERMINAL` 无关。只给 count 不给路径 —— 路径需改 `ReadClaimsResult` (`lib/coordination_ref.py:119`) 字段, 超本 Spec, 转 follow-up (**成文声明哪半没给**) |
| **D15** (新) | 无人值守判据 = **新 config key `state_scanner.coordination.unattended`** (boolean, default false), **禁止**用「`AskUserQuestion` 是否可用」做运行期推断 (editlist FIX-16) | **R2/M-15**: C1 扩权后两个宿主都声明持有 `AskUserQuestion` ⇒ 该谓词恒为「可用」, 分支永不进入 (「上一批 fix 亲手抹平了下一批 fix 的判据」)。key 须同时在 `config-loader/SKILL.md` 登记**与** `DEFAULTS.json` 注册 (后者现连 `coordination` 都没注册, 见清单 #26) |
| **D16** (新) | heartbeat **增 by-track 并存变体**, 不改既有 `heartbeat()` 的 `(container, session)` 键 | **R2/M-17 第 2 项**: 旧版正文「改匹配键」与 Impact「增并存变体」两读。改既有键会动 Phase B 现有认领路径 (撞 §非目标); 并存则 Phase B 逐字节不变, 且形态照抄同文件已有的 `release_claim` (`:274`) / `release_claim_by_track` (`:377`) 并存模式 |
| **D17** (新, R5/skill-reviewer 收敛判断第 2 条 → rework v4 采纳; **R6/TL 字段 M9 + CR m1 补适用范围与围栏规则**) | **SKILL.md 指令块的机械断言三要件**: ① **块边界逐字定义** —— 从锚点标题行起至下一个 `^#{1,4}[ \t]` 行止 (**围栏内的 `#` 行不作为边界; 被测块本身是 ``` 围栏时, 边界即该围栏**), 断言只在切片内求值; 切片外的独立断言须**显式声明**其求值域; ② 块内须含**至少一条可直接执行的完整命令行** (脚本路径 + 必需参数; 多物理行反斜杠续行的须先折叠再判), 不得只有概念名 / 名词短语 / 散落的参数子串; ③ 块内须含 fail 分支的**消费措辞字面** (如 `未能核实`)。**适用范围**: ① 适用于任何被机械断言的块; ②③ **仅适用于指令块** (块的目的是让 AI 执行动作), **不适用于模板 / 骨架块** (块的目的是被复制成产物 —— 往骨架里塞命令行会被 AI 原样复制进每份产物)。**引用本条的 SC 须写明自己落了哪几件**: 母 SC-22 落 ①②③ / 字段 SC-7a 仅 ① / 探针 SC-20 落 ①②③ | R5 三份 Spec 的 4 条 critical 里 3 条同形 (母 M1/M5 + 探针 C1 + 字段 C1): 「机械断言钉住了指令的外形, 没钉住指令的可执行性」—— 一处定义消掉三处 (memory `fix-the-class`)。R6 抓到发源地自己没落 ② (TL C2 / CR M2) 与范围未声明 (TL 字段 M9), 本轮补 |
| **D18** (新, owner 2026-08-30 裁定 1A) | **track-id 恒用 `<spec-slug>-<container_uuid>` 单一形态, 取消 issue 派生形**; 「同一 issue」的判定完全交给 `linked_issue` 字段 (Part B1) | R5/code-simplifier 选项 A (此前从未呈给 owner): 两个新字段 / K1 前半 / K2 / K4 / SC-1·4·15(旧谓词)·27C·30·31 / D12 / 5 行 Impact **结构性消失** (≈27KB, 母 Spec 17%); 三方向 = 三 slug ⇒ 连坐被结构性消灭。**代价成文** (§2.1): 改名两步 (SC-15) + 同容器多方向互报 advisory 噪声 |

**Rule #6 (rule6_note)** — **rework v3 整段重写** (R2/M-6: 旧版把 `audit-engine` 列进「覆盖外」档, 但点名行为 (a)(b)(c) **无一是 audit-engine 的**, 且 `ab-suite/audit-engine.json` **实测不存在** ⇒ 按判据表「缺一照跑」该档根本不成立; 另 R2/M-6 指出旧 substitute **SC-9 无效**):

**本 Spec 涉及的 AI 可读面 (SKILL.md / frontmatter / references / docs) 改动 = 实数 12 hunk / 9 文件** (R5/skill-reviewer C1 订正: 旧版写「6 处」且按文件目录划范围, 漏了三处 `--raw-track-id` 占位串 hunk 与两处 reference/doc hunk; Rule #6 判据表逐字「不按文件目录判」, 以下**逐 hunk** 落档):

| # | 落点 (hunk) | 性质 | 判据表落档 | 处置 |
|---|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md` frontmatter `allowed-tools` (`:9`, 加 `Bash, AskUserQuestion`) | **能力面** (影响该 skill **全部**运行场景, 含既有 eval case) | 第二行「处方性 · 运行时指令面 / 能 / 照跑 AB, 零裁量」 | **照跑现有 `ab-suite/phase-a-planner.json`** (实测存在, `evals` = 2) |
| 2 | `spec-drafter/SKILL.md` frontmatter `allowed-tools` (`:10`, 加 `Bash`) | 同上 | 同上 | **照跑现有 `ab-suite/spec-drafter.json`** (实测存在, `evals` = 2) |
| 3 | `phase-a-planner/SKILL.md` 正文新增「前置: REQUIRE claim (A.1, MUST)」步骤块 + A.1 YAML 项的 `precondition:` 指针 (SC-22 ⑤) | 处方性 · **套件覆盖外** | 第三行 | 点名行为 (a)(b)(c) + 定向 fixture, 见下 |
| 4 | `spec-drafter/SKILL.md` 正文新增「前置: REQUIRE claim (A.1, MUST)」步骤块 (第二落点) | 同上 | 同上 | 同上 |
| 5 | `state-scanner/SKILL.md` 新增「Layer L A.1 heartbeat 集成」小节 (按 R5/M6 缩为: 触发条件一句 + CLI 一行 + fail-soft 一句 + 指针) | 处方性 · 运行时指令面 | 第二行「照跑 AB, 零裁量」 | **照跑现有 `ab-suite/state-scanner.json`** (实测存在, `evals` = 12) + 在**该既有套件内新增 1 个 eval case** 钉点名行为 (d) |
| 6 | `config-loader/SKILL.md` 登记 `coordination` 的 A.1 skip 语义 + `unattended` 新 key | **描述性** (登记既有/新增字段, 不改任何 AI 决策路径) | 第一行「描述性 / 不适用 / substitute」 | **substitute 见下方 (已换, 旧 SC-9 无效)** |
| 7 | `phase-b-developer/SKILL.md:92` 的 `--raw-track-id` 占位串取值口径 (§2.1b) + `:96-97` 关于 push 的注释勘正 (2026-08-30 实读: 注释跨 `:96-97`, `:98` 是 `coordination.enabled` skip 项) | **处方性 · 运行时指令面** (AI 逐字复制进命令行的字面) | 第二行 | **照跑现有 `ab-suite/phase-b-developer.json`** (2026-08-30 `ls` 实核存在) |
| 8 | `branch-manager/SKILL.md:146` 块: 占位串取值口径同步 (`:148` 一带)。**标题不改** —— `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的部件名 (非 Phase A.1); rework v4 曾按 R5/M2 的误读落成改名, R6/CR M1 撤回 | **处方性 · 运行时指令面** (占位串是 AI 逐字复制的字面) | 第二行 | **照跑现有 `ab-suite/branch-manager.json`** (实核存在) |
| 9 | `phase-d-closer/SKILL.md:51-52` 调用模板 + `:55` 说明句的 carry-id 口径 | 同上 | 第二行 | **照跑现有 `ab-suite/phase-d-closer.json`** (实核存在) |
| 10 | `state-scanner/references/layer-l-integration.md`: (a) `:45` 悬空函数名 `update_heartbeat()` → `heartbeat()` + caller/节律勘正; (b) 新增「Layer L A.1 heartbeat 集成」设计段 (三级回落表 / 遥测分区边界 / fail-CLOSED 谓词 / 完整命令行, 从 SKILL.md 移来, R5/M6) | (a) **描述性**勘正; (b) **处方性** (AI 按 SKILL.md 指针读它执行) | (a) 第一行; (b) 第二行 | (a) substitute = 结构化断言「该文件不含字面 `update_heartbeat`, 且含 `heartbeat(`」, **baseline 必红** (清单 #33); (b) 与 #5 同一次 `state-scanner.json` 照跑覆盖 + 结构断言「该文件含标题字面 `Layer L A.1 heartbeat 集成`, 且该节切片内含 `--heartbeat-only`」, **baseline 必红** (R6/TL M8: 否则 SKILL.md 的指针可悬空) |
| 11 | `state-scanner/docs/coordination-ref-schema.md` §3.2 追加第 6 条 (`unknown_schema_claims` 语义) | **描述性** (schema 文档) | 第一行 | substitute = 结构化断言「§3.2 含字面 `unknown_schema_claims`」, **baseline 必红** (清单 #28: 该节今天 5 条, 无此字面) |
| 12 | `state-scanner/SKILL.md:168` 输出键集补 `push_skipped` / `push_skipped_reason` (aria-plugin `--no-push` 修复引入的 additive 键) | **描述性** (键集登记) | 第一行 | substitute = 结构化断言「`:168` 一带含字面 `push_skipped`」, **baseline 必红** (R6/CR 实读 `:168` 键集无此二键; R6/CR m5 补档) |

> **⛔ 「照跑 AB」档的硬前提 (owner 2026-08-30 裁定 4i: 单独修, 不入本 Spec 变更面)**: 上表 #1/#2/#5/#7/#8/#9 的照跑**都可能让评测 AI 走到 `phase1_gate.py`**, 而 AB 评测跑在**真仓、真 `origin`、无沙箱** (2026-08-30 实读 `AB_TEST_OPERATIONS.md` 与 `skill-creator` 的 subagent 模板, 均无隔离机制; 历史 run 产物直接落在 `aria-plugin-benchmarks/ab-workspace/` 真仓路径下), 且 `phase1_gate.py` 第 9 步 `resilient_push` (`:791-802`) **无条件**推 `refs/aria/coordination` 到生产 remote —— **推送点不是** R5 引的 `write_claim` auto_bootstrap (它是 `bootstrap(..., push=False)`, `coordination_ref.py:800`)。⇒ **跑本表任何一条照跑前, harness 会话必须以 `ARIA_COORDINATION_NO_PUSH=1` 启动** (对应 aria-plugin 修复: `phase1_gate.py --no-push` / 同名 env var, 输出 JSON 记 `push_skipped: true`; 见决策单第 4 项与 `AB_TEST_OPERATIONS.md` 新增条目)。该修复是 Level 1 独立变更, **本 Spec 只引用其存在, 不承担它**。

**⛔ 旧版的第 7 档 `audit-engine/SKILL.md` + `references/execution-modes.md` 随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)**, 连同它的 AB 缺口问题 (`ab-suite/audit-engine.json` 不存在) 一并由该 Spec 判据。本 Spec **不再对 audit-engine 提出任何 Rule #6 主张**。

**「覆盖外」档的三条 (缺一不可)** —— 对应上表 #3/#4:

1. **点名行为**: (a) A.1 起草前必调 `phase1_gate.py` (**Level 1 与 `coordination.enabled == false` 时零调用**, §2.5), `--linked-issue` 实参按 §2 两阶段取法 (只有字段判 `OK` 且非哨兵才传; 哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 省略 —— R6 接缝 C1), 且 `--raw-track-id` 实参拼成 `<spec-slug>-<container_uuid>` (slug = 本 Spec 目录名逐字; uuid 段取 container-id 文件的 `uuid` 字段, **非** label — §2.1a 行为层) + 改名 / 放弃方向时的 release 义务 (§5.2); (b) overlap 非空 (或 `unknown_schema_claims > 0`) 时经 `AskUserQuestion` 请裁而非自行放行 —— **`unattended == true` 时改走 handoff + `awaiting_owner`**; (c) fetch 降级 / overlap 异常时按「未能核实」而非「无碰撞」;
2. **建可证伪定向 fixture**: 上述三条各一个 eval, **双臂须能分辨**; 另加 (e) `unattended` 臂 (对应 SC-26);
3. **套件缺口开 issue**: 与 `aria-plugin#117` (缺 authoring 维度) / `#127` (缺 D9 surface 维度) 同族, 归并或新开由 A.2 定。

**「照跑 AB」档的点名行为 (d)** —— 对应上表 #5: 「**持有 active claim 且 `coordination.enabled == true` 时, 每次 `/state-scanner` 入口调用都触发 `phase1_gate.py --heartbeat-only` 刷新该 claim; `enabled == false` 时零触发**」(与 SC-21 / SC-28 呼应)。它**属于**「照跑 AB」义务的一部分 (在既有套件内加 case), **不是**另起「覆盖外」fixture —— 刻意不塞进上面 (a)(b)(c) 清单, 否则会把同一处 SKILL.md diff 同时判进两档。

**⭐ 描述性档的 substitute (R2/M-6 命中点, 已换)**: 旧版记 substitute = **SC-9**, 但 SC-9 断言的对象是 **SKILL.md 散文** (「A.1 零调用」这一 AI 行为), **无代码宿主、不可机械断言** ⇒ 作为描述性档的 substitute **无效**。**改为**:

> **substitute = 结构化测试「`DEFAULTS.json` 注册的 `coordination` 三键 (`enabled` / `mode` / `unattended`) 与 `config-loader/SKILL.md` 的登记值逐字一致」** (宿主 `skills/state-scanner/tests/` 或 config-loader 既有测试宿主, A.2 定)。
> **它怎么会红**: **baseline 必红** —— 实读 `git show d50f9c3:skills/config-loader/DEFAULTS.json` 的 `state_scanner` 段**根本没有 `coordination`** 这个键 (见「事实断言逐条实读清单」#26), 而 `config-loader/SKILL.md:134`/`:140` 已登记 `enabled`/`mode`。⇒ 这是一条**真的可机械断言、且现在就是红的**测试, 不是恒真的形式主义 (memory `check-runs-at-baseline-first` / `false-green-dual-is-permanent-red`)。
> **SC-9 本身不删**, 只是**类别订正为「行为 (定向 fixture)」** (见 Success Criteria 表)。

**能力面附注 (C1 落版义务, 2026-08-22; R1 rework 核验 major-4 重判, rework v3 复核数据未变)**: 上表 #1/#2 的 `allowed-tools` 扩权与 #3/#4 的**指令面**变更虽落在同一份 SKILL.md diff 里, 但按 `standards/conventions/skill-benchmark-exemption.md` §1「**逐 hunk 判, 不逐文件判**」分属两档: 能力面 hunk ⇒ **照跑现有两套件** (验「扩权后 skill 在既有 eval 场景下行为是否漂移」); 指令面 hunk ⇒ **覆盖外定向 fixture** (验「新增 A.1 claim 行为本身, 现有 eval 结构性覆盖不到」)。**二者各自独立、互不替代。** 上一版曾误判「能力面部分不单独申请豁免、也不需要单独判据」, 与 owner 原话「Rule #6 按能力面变更申报 benchmark」实质相悖, 已订正 (过程留痕见 [审计轨 §4](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md#4-3-实读订正--请-owner-复议原文-已闭环))。

确定性代码层由 SC 覆盖, 与上述并行不互替。**不申请豁免。**

---

## Success Criteria

> **验证面分层** (R1/C4: 原版把 SC 挂在**不存在的** `phase-a-planner` 测试宿主上):
>
> | 类 | 宿主 | 可机械断言 |
> |---|---|---|
> | 代码类 | `skills/state-scanner/tests/` (既有宿主; `audit-engine/tests/` 随 §4 迁至 `sibling-spec-probe`) | ✅ |
> | 行为类 | **定向 AB fixture** (rule6_note「覆盖外」档第 2 条) | ⚠️ 只能由 eval 覆盖, **不冒充结构化测试** |
>
> **⚠️ 编号纪律 (rework v3 继续遵守)**: SC 编号**只追加, 不重排, 不复用**。迁至子 Spec 的 SC **保留行号并写明去处**, 不删行; 撤销的 SC **保留行号并标 ⛔**, 不删行。子 Spec 各自从 SC-1 重新编号 (独立命名空间), 并在其头部注明与本 Spec 旧编号的对应。

### 四个被推翻版本的红窗 (spike S3 强调: 缺一则第五版会再踩)

> **⚠️ 被测对象与宿主 (R2/M-17 第 1 项补; rework v4 按 1A + 第 5 项裁定重判)**: §2.1 的拼接**没有代码宿主** (§2.1a, 2b 裁定后为长期状态)。**SC-1 / SC-4 随 1A 撤销** (issue 派生形不存在, 无对象); **SC-2** 改钉 `linked_issue_overlaps` 经 CLI 的行为 (代码类, baseline 即绿的回归守卫); **SC-3** 不变 (accessor 单测); 拼接本身的**文本层**由 SC-22 ② 承载, **行为层**由 rule6_note (a) 定向 fixture 承载。

| SC | 钉住哪一版的失败 | 场景 → 期望 | 宿主 | 怎么会红 |
|----|---|---|---|---|
| **SC-1** → **⛔ 已随 1A 撤销 (2026-08-30)** | ~~原始版 (spec-slug ⇒ 改名孤儿): issue 派生形的轨 slug 改名前后 track-id 不变~~ | 1A 后 track-id **就是** slug 形, 改名 = 换 id 是**设计选择**而非缺陷 (代价成文于 §2.1 / §5.2, 由 SC-15 守两步无孤儿) | — | — (编号保留不复用) |
| **SC-2** | R1-fix 版 (纯 issue 派生 ⇒ 主机制死) —— **rework v4 按第 5 项裁定改写声称对象: 钉 overlap 行为, 不钉派生** | 两**不同容器**同 `linked_issue`、不同 track-id (各自 `<slug>-<uuid>`, 夹具**手写**两串 —— 允许且必要, 拼接无代码宿主是 §2.1a 成文交付的一半; 归一仍走 `lib/track_id.py::derive_track_id`) 各自经 CLI 认领 (带 `--linked-issue` + `--include-terminal`) ⇒ 双方 `linked_issue_overlap[]` **各含对方**; **负控**: 两串**相同** (模拟容器段被丢弃) ⇒ 双方 overlap **均为空** (`lib/collision.py:278-279` 自排除) | 代码 (CLI 全链路) —— **⚠️ baseline 即绿** (该 CLI 路径今天存在, 两臂在 `d50f9c3` 上都过); **它是回归守卫不是恒真装饰**: 本 Spec 改 `:1230` 门控为 `or args.include_terminal` 并放宽 `linked_issue_overlap` 类型, **有能力打破它** | 坏实现 A: 门控重写后 `--linked-issue` 路径丢失 ⇒ 正臂双方为空 ⇒ 红; 坏实现 B: `--include-terminal` 实现成「跳过全部 continue 分支」⇒ 负控臂互相命中 ⇒ 红。A.2 须以「删掉 `:278-279` 两行」验证负控臂确实会红 (memory `adversarial-fixture`) |
| **SC-3** | R2-fix 版 (`container-short` 前 8 位 ⇒ label 碰撞) | container-id 的 `label` 设为长字符串时, track-id 仍用 **`uuid` 字段** | 代码 (新 accessor 的单测) + 文本层 | 直接调 `get_container_id()` (`lib/identity.py:191`, `:222` label 优先) 的实现在设了 label 的夹具上必红 |
| **SC-4** → **⛔ 已随 1A 撤销 (2026-08-30)** | ~~R3 指出的 number 表示不一致: `#007` 与 `#7` 派生同一 track-id~~ | track-id 不再含 issue 号; `#007` 与 `#7` 的等价由前置 Spec 的 `normalize_linked_issue` 在 `linked_issue` 维度保证 (已 ship v1.67.0) | — | — (编号保留不复用) |

### 主机制

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-5** (代码) | heartbeat by-track 变体跨 subprocess 两次调用 (第二次 session_id 不同) | 同一 track 的 claim 被刷新 | 只有既有 `heartbeat()` (按 `(container, session)` 匹配, `lib/claim_lifecycle.py:228`) 的现状必红 |
| **SC-6** (代码) | 同 (container, track) 有多条 active claim | **全部**刷新 | 只刷新一条必红 |
| **SC-7** (代码) | 超 `SWEEP_TTL` 未刷新 ⇒ 仍被 sweep; **且**调用新 by-track heartbeat 刷新后 ⇒ **不**被 sweep | 两臂可辨 | **⚠️ 恒绿风险已堵 (R3/QA-F3)**: QA 席实读既有 `test_sweep_stale_cross_container_fresh_untouched` (`tests/test_release_by_track.py:380`) —— 它已覆盖「超时被 sweep」这一臂且**全程不调用任何 heartbeat**, 故 SC-7 若只有那一臂就是**零新代码路径覆盖**。⇒ 本条**必须含第二臂**: 夹具显式调 §2.2 的 by-track heartbeat 变体后再 sweep, 断言该 claim **未被** abandoned; 不调用新变体的实现在第二臂上必红 |
| **SC-8** (代码, **CLI 全链路**) — **⚠️ 已按 R2/M-16 拆掉捆绑, 只留一个可机械断言** | 同 issue 他轨 claim 为 `done` / `abandoned`, A.1 模板带 `--include-terminal` | **该条出现在 `linked_issue_overlap[]` 里** (单一断言: 可见性) | `lib/collision.py:268` 的 `_TERMINAL` skip 的现状必红; **且只测库函数的 SC 在「参数没接到 CLI」的实现上会绿** ⇒ 断言层必须是 CLI。**⚠️ 场景列已删去 `yielded`** —— 实读 `_TERMINAL` 不含它, 该子例 baseline 即绿 (R2/M-9: 旧版订正了正文却没同步 SC)。**「措辞按 status 分档」这半移到 SC-11** (它是消费层措辞, 无代码宿主) |
| **SC-9** (**行为**, 定向 fixture — **⚠️ 类别按 R2/M-16 订正, 旧标「代码」有误**; **R6/CR 母 C1 补 (B) 臂**) | **两臂**: (A) `coordination.enabled == false`; (B) `phase-a-planner` 判定 **Level 1** (`skip_if: complexity: Level1` 命中, `phase-a-planner/SKILL.md:67`) | 两臂均: A.1 **零调用**, 不写 claim, 不推远端 | 它断言的是「AI 是否跳过调用」, 实测对象是 SKILL.md 散文 ⇒ **无代码宿主**; (A) 「无条件调用」的臂与「读 config 后跳过」的臂可辨; (B) 「typo 修复也写一条永不 release 的僵尸 claim + 一次外向 push」的臂可辨 (R5/M4)。**与 SC-28 是同一开关的两半** (SC-9(A) 管 A.1 侧, SC-28 管 heartbeat 侧) |
| **SC-10** (代码, **CLI 全链路**) — **⚠️ 已按 R2/M-16 拆掉捆绑** | fetch 降级 | **`GateResult.error == "fetch_degraded"`** (单一断言: 字段非空且取该 token) | 现状 `error: null` 必红 (`scripts/phase1_gate.py:210` 的 docstring 预留了该 token 但全文无 `error=` 赋值)。**「消费面渲染『未能核实』而非『无碰撞』」这半移到 SC-25** |
| **SC-11** (行为) | overlap 非空 / `unknown_schema_claims > 0` | AI 起草**前**经 `AskUserQuestion` 请裁; 告警含双方 `linked_issue` 原始串 + 对方 `track_id`/`container`/`claimed_at`/`status`; **措辞按 status 分档** (§2.3 选项表: 四档**渲染**不同; `abandoned` 与 `active` **共用选项集**, `unknown` 视同 `active` —— R6/CR m3 订正「四档选项集不同」); **`abandoned` 档须写明「该状态可能是 `--sweep-stale` 的 GC 产物, 对方可能仍在制」并按 `active` 同档请裁** (R4/K6, rework v4 入表) | 定向 fixture; 「渲染一行后自行继续」的臂应可分辨; 「对 `done` 也给出『释放对方 claim』选项」的臂应可分辨 (该选项在 `done` 档语义不成立); 「把 `abandoned` 渲染成『对方已退出』」的臂应可分辨 |
| **SC-12** (行为; **R6 接缝 C1/C4 改写场景**) | spec 的字段判 `OK` 且非哨兵 (code span 首元素形如 `<org>/<repo>#<n>`) 但 AI 未传 `--linked-issue` | AI 不得跳过该参数 (反之: 哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 时**必须**省略, 与字段 E6 四态表一致, 不再相反) | 定向 fixture (**不冒充结构化测试**); 「跳过」与「传了」两臂在 `phase1_gate` 输出里可辨 —— 前者 `linked_issue_overlap` **键缺席** (`scripts/phase1_gate.py:1230` 整块门控), 后者键存在; **第二臂** (存量 markdown 链接形 ⇒ `NO_TOKEN`): 「照传整串」的臂 ⇒ 复现 K8 (脏串进匹配面) ⇒ 必红 |

### 生命周期 / 迁出行

| SC | 场景 | 期望 | 怎么会红 |
|----|------|------|---------|
| **SC-13** | ⛔ **已迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** —— 本 Spec 不再承担「proposal 无字段 / 值不可解析 ⇒ custom check warning」 | — | — (编号保留不复用) |
| **SC-14** — **⚠️ 已按 R2/M-16 拆两层** | (a) **代码**: 给定 A.1 原串调 `release_gate.py --raw-track-id "<原串>" --status abandoned` (`--raw-track-id` 是 `release_gate.py:236-237` 的「三选一」必需项之一, 省了会 `parser.error`) (b) **行为**: A.1 判定「不起该 Spec」时 AI 记得去调 | (a) 该 claim 状态变为 `abandoned` (b) 定向 fixture 两臂可辨 | (a) **baseline 即绿的回归守卫** (R6/CR M4 订正: 代码夹具里同一串 X 先 acquire 后 release 在 `d50f9c3` 上今天就过; 「AI 三处是否逐字复用同一串」是文本层, 由 **SC-34** 守) —— 坏实现 = `derive_track_id` 去容器段 (SC-2 同时红) 或 `release_claim_by_track` 匹配键改坏 ⇒ 必红; (b) 「判定放弃后直接开下一个方向、不 release」的臂必红 |
| **SC-15** (代码 — **rework v4 按第 5 项裁定回滚为代码类**) | 改名 (Spec 目录改名 ⇒ 新 track-id): 夹具手写旧串 `old-slug-<uuid>` 与新串 `new-slug-<uuid>`, 另起一条**无关的**第三方 active claim 作负控 (其 track_id 与旧/新串**不共享任何前缀/后缀**、含不同容器段 —— R6/QA m2: 否则子串匹配的坏实现会误伤负控); 先 acquire 旧串, 再 `release_claim_by_track(旧串)` + `acquire_claim(新串)` | **无孤儿**: 旧 track 无 active claim (其 claim `status == "abandoned"`, 不是被删除), 新 track 恰一条 active; **第三方 claim 仍 active** | **⚠️ baseline 即绿** (宿主 `release_claim_by_track` `lib/claim_lifecycle.py:377` 与 `acquire_claim` `:99` 都实存且今天就这样工作); 它是**回归守卫**: 坏实现 = 把 `release_claim_by_track` 的匹配键改成按 `linked_issue` 或按 container 批量 ⇒ 第三方 claim 也被 abandoned ⇒ 必红。**AI 改名时记不记得走两步**不在本条 —— 由 SC-22 ⑥ (文本层字面义务) + rule6_note (a) 定向 fixture 覆盖 |
| **SC-16** | ⛔ **已迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** (竞品在 `archive/` 下须命中) | — | — |
| **SC-17** | ⛔ **已迁至 `sibling-spec-probe`** (远端无同 issue spec ⇒ exit 0) | — | — |
| **SC-18** | ⛔ **已迁至 `sibling-spec-probe`** (探针 fetch 失败 ⇒ degraded + exit 非 0) | — | — |
| **SC-19** | ⛔ (a)/(c) 两条**已迁至 `sibling-spec-probe`** (不得自命中本轨 spec 目录 / 扫描超上限必须 `log()` 披露)。**(b)「不得把自己的 claim (同 track_id) 计入 overlap」属主机制** ⇒ **由本 Spec 新增的 SC-29 承担** (**⚠️ rework v3 自查订正**: 上一版此处写「由 SC-2 反向臂承担」是**不实断言** —— 实读 SC-2 的期望列只有「双方 `linked_issue_overlap` **各含对方**」这一条正向断言, **没有任何反向臂**; 一个「既返回对方也返回自己」的实现能同时满足 SC-2 而违反 (b)。探针席独立地也判该子项不该迁入 —— claim/track_id 词汇与探针语境错配 —— 两边结论一致, 只是本侧的「接住」动作当时没做实) | — | — |

### 保护窗可生产验证性 (heartbeat, R1 rework 核验 major 补)

> **触发**: 上一轮核验指出 —— §2.2 已自陈「换匹配键不产生刷新者 ⇒ SC-5~7 可以全绿而问题原样存在」, C2 裁定落版后全文却没有任何 SC 或 fixture 钉住它; 这正是 memory `feedback_completion_signals_vs_runtime_invocation` 同形的坑 (「已落版的一段 SKILL.md 文字」≠「会被生产调用的机制」)。

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|---|------|------|---------|
| **SC-20** | — | ⛔ **撤销** (owner 裁定 2026-08-23: (iii) 不采) | **本 Spec 不再对 `STALE_TTL` 提出任何断言** —— 该常量维持 `1800`, 相关的 `reconcile._is_stale()` 行为保持现状 | — (行保留、编号不复用; 回撤的其余三个落点见 §2.2 (iii) 段) |
| **SC-21** | 行为 (定向 fixture, 与 rule6_note 第 5 档「点名行为 (d)」呼应) | `/state-scanner` 入口被调用, 本会话在 coordination ref 持有 active claim, **且 `coordination.enabled == true`** | 两臂可辨: (A) heartbeat 编排层已挂载 ⇒ 每次调用**都**触发 `phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>"` 刷新该 claim —— **判据 = 该 CLI 被 subprocess 调用且 `claim.heartbeat_at` 被刷新**; (B) 未挂载 ⇒ 不触发, `heartbeat()` 生产调用点仍为 0。**⚠️ rework v3 补门控臂**: 本条的场景**显式限定 `enabled == true`**; `false` 的那一半由 **SC-28** 承担, 两条合起来才覆盖 R2/M-7 | 当前实现两臂**不可辨** —— `lib/constants.py:43-44` 自陈「NO production heartbeat loop exists」, 无论挂不挂都是同一 (未触发) 结果 |

### rework v3 新增 (追加编号, 不重排既有 SC)

| SC | 类 | 场景 | 期望 | 怎么会红 |
|----|---|------|------|---------|
| **SC-22** (新; **rework v4 按 D17 三要件扩为 ①–⑦ + 块边界; rework v4.1 按 R6 (TL C1/C2, CR M2/M3/m2, QA m1) 修互斥与缺项**; 本条落 D17 ①②③) | 代码 | `phase-a-planner/SKILL.md` 与 `spec-drafter/SKILL.md` **各自**的 A.1 认领步骤 (R2/M-11: 双落点是核心杠杆却零 SC 覆盖)。**断言对象绑定两个文件路径, 逐一断言, 不拼接** (R5/m2)。**新标题的落点钉死: 放在 `### 步骤执行` (`phase-a-planner/SKILL.md:60`) 之前**, 使切片止于 `:60`、不吞下步骤表 (§2「不塞进 YAML 列表」) | **块边界 (D17 ①, R5/M5)**: 「步骤块」= 从匹配 ① 的标题行起, 至下一个 `^#{1,4}[ \t]` 行 (或文件尾) 止的切片; **②③④⑥⑦ 只在该切片内求值; ⑤ 是切片外的独立断言** (R6/TL C1: 旧写「②–⑥ 只在切片内」与 ⑤ 互斥)。① `assertRegex(text, r"(?m)^#{2,4}[ \t]+前置: REQUIRE claim\b[^\n]*A\.1")` **且匹配行不在 ``` 围栏内** (先按 ``` 切段, 只在围栏外的段跑正则; 标题行须点名带点的 `A.1` —— 与 `branch-manager:146` 那个写着部件名 `Part A1` 却跑 `--phase B` 的既有块可辨); ② 切片内含**七个字面量**: `phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` / `--raw-track-id "<spec-slug>-<container_uuid>"` / `--emit-arg` / `未能核实` (最后一个 = D17 ③ fail 分支消费措辞); ③ 切片内含幂等谓词**逐字** `check: coordination ref 内按 (container_id, session_id) 定位到本 session 的 active claim` **且**含字面 `claims/` (R5/M1: 无「或等价的…」逃逸口); ④ 切片内**不得**出现字面 `--phase B` (R5/M2 负控); ⑤ **仅 `phase-a-planner`, 切片外求值**: 断言对象 = 文件内含 `A.1 - Spec 管理:` 的那个 ```yaml 围栏 (**文件内共 7 处 yaml 围栏, 宿主实现须先按该锚点定位, 不可抓第一个** —— R6/QA m1), 该项下含逐字 `precondition: 见「前置: REQUIRE claim」小节 (MUST, 在本表之前执行)` (R5/M3); ⑥ 切片内含字面 `改名 ⇒ release 旧 + acquire 新` 与 `放弃方向 ⇒ release_gate.py --raw-track-id` (§5.2 两条退出义务的文本层, SC-15 的文本半); ⑦ **(D17 ②, R6/TL C2 + CR M2 补)** 切片内含**一条以 `python3` 起首、含 `phase1_gate.py` 与 `--phase A.1` 的完整命令行** —— §2 的模板是多物理行反斜杠续行形, 断言须**先做续行折叠** (`\\\n` 连同后续缩进折成一个空格) 再判, 单行正则直接判会误红。**宿主 = `skills/state-scanner/tests/test_coordination_default_lockin.py`, 扩它不另起文件** | 两处 SKILL.md 现**均无** A.1 步骤块 ⇒ baseline 必红。**裸 `assertIn` 明确不可接受** —— 子串检查对「把 `前置: REQUIRE claim` 原样塞进 A.1 现有 ```yaml 动作列表」这一种失败**免疫**, 而那正是 §2 明令禁止、§Why 引 R3/M6 论证过的原病。**docstring 须写明**: 与先例 `test_phase_b_require_claim_present` (`:53`, `:55-56` 两条**裸 `assertIn`**) 的断言强度差异**是有意的** —— B.0 的 YAML-键形态是既有欠缺, 另开 issue, 不在本 Spec 修。缺 ③ 的实现 (一次 A.1 写两条 claim + 两次外向推送) 也必红; 把字面量塞进 `## 相关文档` 的实现因**块边界**在切片外 ⇒ 必红 (R5/M5); **「参数子串齐全但没有一条可执行命令」的散文实现因 ⑦ ⇒ 必红** (R6/TL C2 给出的那段反例) **⚠️ 锚点换名 (R3/QA-F1; R5/m1 订正措辞)**: 原用 `A.0 - REQUIRE claim`; `A.0` 在 `spec-drafter/SKILL.md:30` `(A.0)` / `:369` 流程图里是**条目与行内标签**而非标题 (全部 `^#{1,6} ` 标题里无 `A.0`), 真正的理由是「`A.0` 在十步循环 SOT 里 = state-scanner, 本步骤发生在 **A.1**」⇒ 改用 **`### 前置: REQUIRE claim (A.1, MUST)`** 体例 |
| **SC-23** (新) | 代码 (CLI 全链路) | A.1 认领 (原串 X) → 走完循环 → D.2b 跑 `release_gate.py --raw-track-id X` (R2/C-C) | 该 claim **不再 active** | **⚠️ baseline 即绿的回归守卫** (R6/CR M4 订正: 作为 CLI 全链路代码夹具, 同一串 X 先 acquire 后 release 在 `d50f9c3` 上今天就过 —— `tests/test_release_by_track.py` 就是这条路径; 旧写「现状必红」把三处 SKILL.md 模板的**文本**缺陷误当成了代码缺陷)。坏实现 = `derive_track_id` 去容器段 或 `release_claim_by_track` 匹配键 (`lib/claim_lifecycle.py:377`/`:425`) 改坏 ⇒ 必红; 「三处模板逐字复用同一串」由 **SC-34** (文本层) 守。**若实现改的是 `derive_track_id` 去掉容器段, SC-2 会同时变红** (两条互为对方的负控) |
| **SC-24** (新) | 代码 (CLI 全链路) | 夹具写入一份 `schema_version: "2"` (或任何非 `"1"`) 且带匹配 `linked_issue` 的 claim blob, 经 CLI 跑并带 `--include-terminal` | `unknown_schema_claims >= 1` **且**该条**不出现在** `linked_issue_overlap[]` 中 | 现状**无该键** ⇒ 必红; 试图经 `linked_issue_overlap[]` 输出的实现在真实 `parse_claim` 路径下**恒空** (sentinel 的 `linked_issue` 为 `None`, 被 `lib/collision.py:274` 丢弃) ⇒ 也必红。**第二个断言 (不出现在 overlap[]) 是负控**: 它拒绝「强行放行 sentinel」这个坏实现 —— 那样会往告警面塞三个空字符串字段 |
| **SC-25** (新) | 代码 (CLI 全链路) + 行为 | overlap 计算路径抛异常 (夹具: 让 `linked_issue_overlaps` 抛) | ① `linked_issue_overlap == null` **且** `linked_issue_overlap_error` 非空 (代码臂); ② 消费面把「已确认存在竞品」(`unknown_schema_claims > 0`) 与「本轮没取到证据」(`error` 非空) 渲染成**同一句**的实现**必红** (行为臂) | 现状 `scripts/phase1_gate.py:1236-1238` 的 `except` 写 `out["linked_issue_overlap"] = []` ⇒ 异常路径与「查了没有」不可分辨 ⇒ 代码臂必红。行为臂的两个坏实现 (都渲染「未能核实」/ 都渲染「无碰撞」) 均可被判红 |
| **SC-26** (新) | 行为 (定向 fixture) | `state_scanner.coordination.unattended == true` 且 overlap 非空 (R2/M-15) | **零** `AskUserQuestion` 调用 + handoff 待复议段出现 `awaiting_owner` | 「照问不误」的臂可分辨; 用「`AskUserQuestion` 是否可用」做判据的实现在本 fixture 上**恒走问的那一臂** (C1 扩权后该谓词恒为「可用」) ⇒ 必红 |
| **SC-27** (新) → **⛔ 已随 1A 撤销 (2026-08-30; AI 流程判断, 见闸门状态表 #4)** | — | ~~三臂: (A) issue 派生形放弃一个方向 ⇒ claim 仍 active; (B) 放弃整个 issue ⇒ abandoned; (C) `--spec-slug` 三元组~~ | 1A 后「放弃一个方向」= 释放该方向自己的 claim (§5.2), 与 SC-14(b) 同一断言; 「连坐」结构性不可能 (不同 slug = 不同 track_id), 无需负控 | — (编号保留不复用) |
| **SC-28** (新) | 行为 (定向 fixture) | `coordination.enabled == false`, `/state-scanner` 入口被调用, 本会话持有 active claim (R2/M-7) | **零** heartbeat 调用 (不跑 `--heartbeat-only`, 不写 claim, 不推远端) | 把 (ii) 的「每次 `/state-scanner` 必跑」实现成**无视 opt-out** 的臂必红。**与 SC-21 合起来**才覆盖「无条件」的正确语义 (无条件 = 不依赖 `collision.kind`, **不是**无视 `enabled`) **(第二臂, R3/TL-M2)**: 连跑 N 次 `--heartbeat-only` 后, `coordination_probe.py` 的 **recent production 计数不变** (仍只反映真正的 `run_gate` 调用); 把 heartbeat 记进 production 分区的实现 ⇒ 计数增长 ⇒ **必红** |
| **SC-29** (新, ⚠️ **回归守卫 — baseline 即绿**) | 代码 (CLI 全链路) | 单容器单轨: 本轨自己已有一条 active claim 且 `linked_issue` 与本次查询相同, 经 CLI 跑 A.1 认领 (带 `--include-terminal`) —— 承接原 SC-19 的 (b) 子项 | 返回的 `linked_issue_overlap[]` 中**不出现本轨自己的 claim** (同 `track_id` 者必须被排除) | **⚠️ 本条 baseline 即绿** —— `lib/collision.py:278-279` 现在就写着 `if c.track_id == own_track_id:` / `continue`。**它不是恒真装饰, 是回归守卫**: 本 Spec 动了 `include_terminal` 形参与 `:1230` 的门控条件, **有能力打破它** (例如把 `--include-terminal` 实现成「跳过全部 continue 分支」就会连自排除一起跳掉)。判据「它怎么会红」= **在该负控实现上必红**; A.2 须以「删掉 `:278-279` 两行」作为坏实现验证它确实会红 (memory `adversarial-fixture`)。**⚠️ 与 SC-2 的关系**: SC-2 只断言「各含对方」(正向, baseline 红), 本条断言「不含自己」(反向, baseline 绿) —— **两条分开列而不合并进 SC-2**, 因为把 baseline-红与 baseline-绿的断言捆进同一条会让「怎么会红」失去分辨力 (R2/M-16 的同一教训) **⚠️ 夹具补强 (R3/QA-F4)**: 原夹具 own claim = `active`, 而**本 Spec 真正新开的风险面**是 `--include-terminal` 放行终态后 —— own claim 为 `done`/`abandoned` 时是否仍被排除。⇒ 夹具**必须含第二组**: own claim 状态为 **terminal** 且带 `--include-terminal` 跑, 断言 `linked_issue_overlap[]` 中**仍不出现本轨自己**。只测 active 那组的实现视为未满足本条 |
| **SC-30** (R4/K1 新增) → **⛔ 已随 1A 撤销 (2026-08-30)** | — | ~~acquire 带 `--spec-slug` → heartbeat → 读回 `spec_slug`/`track_form` 不变~~ | 字段不存在了 | — (编号保留不复用) |
| **SC-31** (R4/K2 新增) → **⛔ 已随 1A 撤销 (2026-08-30)** | — | ~~无 `track_form` 的 legacy claim 跑 D.2b release ⇒ 非零退出~~ | 字段不存在了; legacy claim 与新 claim 形态一致 (都只有既有 11 字段), 无「day-one 悬崖」 | — (编号保留不复用) |
| **SC-32** (R4/K7 → **rework v4 入表**) | 代码 | 编排层两级来源 (§2.2 ①②) 都取不到 ⇒ **仍**调用 `phase1_gate.py --heartbeat-only --phase A.1 --repo-path <repo>` 且**不传** `--raw-track-id` (该模式下 argparse 不得要求它) | 遥测 JSONL (`.aria/coordination-telemetry.jsonl`) **新增恰一条** `_source="heartbeat"` 且 `outcome="skipped_no_track"` 的记录; **不**写 claim, **不**推远端; `coordination_probe.py` 的 production 计数**不变** | **坏实现 1** (R6/BA M1 + TL C3): 只加 `--heartbeat-only` 开关而不松绑 `:1187` 的 `--raw-track-id` `required=True` ⇒ argparse 在进入 `_main()` 前即 `error: the following arguments are required` ⇒ 零记录 ⇒ 必红 (落点 = Impact 第二处变更 ⑦); **坏实现 2**: 只 `logger.debug` 不落盘的实现 ⇒ 零新增记录 ⇒ 必红 (R4/K7: `phase1_gate.py:56` 的 logger 无 handler, 独立 subprocess 的 log 全丢 ⇒ 「跑了但 skip」与「没挂载」在磁盘上不可辨); 把记录写进 `_source="production"` 的实现 ⇒ probe 计数增长 ⇒ 必红 (与 SC-28 第二臂同源)。**baseline 必红** (该模式今天不存在) |
| **SC-33** (R4/K5 → **rework v4 入表**) | 代码 (CLI 全链路) | 夹具让 `read_claims` 抛异常, 带 `--include-terminal` (**不带** `--linked-issue`) 跑 CLI | 输出中 `linked_issue_overlap == null` **且** `unknown_schema_claims == null` **且** `linked_issue_overlap_error` 非空 (§2.4b 四态表第四态; `unknown_schema_claims` 取值域 `int \| null`, `null` ≠ `0`) | 只赋 `linked_issue_overlap` 的实现让 `unknown_schema_claims` **缺席** ⇒ 消费方 `.get(k, 0)` 读成 0 (零证据当正证据 —— R2/M-4 在自己的修复里复发, memory `fix-recurs-in-fallback`) ⇒ 必红。**baseline 必红** (`:1236-1238` 的 except 今天写 `[]` 且不赋该键) |
| **SC-34** (新, R6/CR M4 + m4; 文本层) | 代码 | `phase-b-developer/SKILL.md` (B.0 块 `:92` 一带) / `branch-manager/SKILL.md` (`:146` 块内 `:148` 一带) / `phase-d-closer/SKILL.md` (D.2b `:51-55` 一带) 三个文件**各自**含逐字 `A.1 认领时派生的那一串` (§2.1b 的占位措辞) | 三文件各 ≥1 命中 | 只改一处或两处的实现 ⇒ 红; **baseline 必红** (三文件今天 0 命中)。它守的是「三处模板逐字复用同一串」这个文本层承诺 —— SC-23 / SC-14(a) 的代码夹具对它感知不到 |

---

## 非目标

- **不改** `linked_issue` 归一本身 —— 属前置 Spec [`linked-issue-normalization`](../../archive/2026-08-23-linked-issue-normalization/proposal.md) (**已 ship 并归档**, v1.67.0 `ca52d1c`);
- **不做** basename 截断型别名归一 (D9; 分隔符型已由前置 Spec 覆盖);
- **不做**中心化 spec 登记表 (D10);
- **不引入**跨容器 release (D6);
- **不把** advisory 升级为 block;
- **不动** Phase B 入口现有认领 —— `include_terminal` 默认 `False` 保既有语义逐字节不变; **`--heartbeat-only` 是同一 CLI 下的独立模式, 不改 acquire 路径; heartbeat 是增并存变体不改既有键** (D16)。**⚠️ 主要的边界争点已成文 (另有两处 Phase B 文档面的描述性勘正: `phase-b-developer:96-97` 注释 / `state-scanner:168` 键集, R6/CR m4)**: §2.1b 的 carry-id 统一会改三处模板的 **占位串取值口径** (不改闸门语义), 见该节的 U-3 边界说明 —— R3–R5 三轮未被推翻, 但 owner **从未显式确认**「这不算动 Phase B」, 仍待一句话 (闸门状态表 #2); **⚠️ 限定 (R3/BA-M3 + TL-M3)**: 本条指「不改 Phase B 的 **acquire 路径、默认参数与 outcome 语义**」; **不包括** advisory 键 `linked_issue_overlap` 的**类型放宽** (`list` → `list | null | 缺席`) —— 该放宽是 R2/M-4「零证据不得当正证据」修复的必然结果, 且 Phase B **可选传** `--linked-issue` (`phase-b-developer/SKILL.md:93`) ⇒ 它**会**看到新形态。二者原先并列成文即自相矛盾, 现按此拆开。**⚠️ 第二处限定 (R6/TL C3)**: `--heartbeat-only` 模式使 `--raw-track-id` 在 argparse **定义层**由 `required=True` 改为条件必需 (Impact 第二处变更 ⑦); acquire 模式 (`--phase B`) 缺参仍 `parser.error` (负控), 故「不改 acquire 路径」在**行为层**成立, 在解析层是一处受模式守卫的改动 —— 与本条并列成文, 不再互斥。
- **不改写**存量 coordination ref 数据 (⇒ §2.1b 的过渡期两形态并存已知限, §6 已列);
- **不新增**任何 claim 字段 (1A: `spec_slug` / `track_form` 已撤; `ClaimRecord` 既有 11 字段不动) —— 新写的 `heartbeat_by_track` 用 `dataclasses.replace` 而非逐字段重建 (§5.3 保留纪律);
- **不新增**「按 issue 批量释放」的命令 (§5.2: 放弃整个 issue = 逐方向各自 release);
- **不统一** `owner-container` 与 claim container 段的口径 (§3 已记为 follow-up, 属 standards 变更);
- **不修** `release_gate.py:225` help / `state-scanner/SKILL.md:176` / `phase-d-closer/SKILL.md:56` 三处把 `SWEEP_TTL` 行为写成 `STALE_TTL` 的**代码库既有措辞缺陷** —— 实读事实见「事实断言逐条实读清单」#14, 记 **follow-up**, 不混进本 Spec 变更面;
- **不改 `STALE_TTL`** (owner 2026-08-23 撤销 (iii));
- **不承担**「关联 Issue」字段的产生/校验/抽取规则 (整节迁 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md), 含**不回填存量 proposal** 这条);
- **不承担**竞品 spec 探针 (整节迁 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md));
- **不编辑**已归档的姊妹 Spec (`openspec/archive/2026-08-23-linked-issue-normalization/`) —— editlist FIX-11 要求的编辑**已由姊妹自己在 ship 前完成** (清单 #16);
- **不给** `unknown_schema_claims` 提供**路径/身份** (只给 count; 需改 `ReadClaimsResult` 字段, 转 follow-up — D14);
- **不定义** `unattended` 的 Layer 1→2 env 传递三腿契约 (§2.3 已知限, 转 A.2/follow-up)。

---

## Impact

> **⚠️ 行号基线 = aria `d50f9c3`** (见「事实断言逐条实读清单」表头); 主仓 gitlink 现指向 `58a49e7` (v1.67.1), 落后 2 个不触及本表文件行的 commit, A.2 实施前须重新 fetch 复核。

| 文件 | 变更 | 来源 |
|------|------|------|
| `skills/state-scanner/lib/claim_schema.py` | **零改动** (rework v4 / 1A: 不新增 `spec_slug` / `track_form`; 旧行原文见审计轨 §6) | 1A (owner 2026-08-30) |
| `skills/state-scanner/scripts/coordination_probe.py` | **仅口径声明/注释**: 明确 `--heartbeat-only` 的遥测**不进** production 分区, 本探针计数口径不放宽 (防 enabled check 被心跳变恒绿) | **R3/TL-M2** |
| `skills/state-scanner/scripts/release_gate.py` | **零改动** (rework v4 / 1A: 不新增 `--spec-slug`)。本 Spec 只调用其**既有**参数: `--raw-track-id "<本轨 A.1 原串>"` (三选一必需项, `:236-237`) / `--status abandoned` (§5.2 三条退出路径) / `--sweep-stale` + `--gc` (D.2b 既有模板, `phase-d-closer/SKILL.md:51-52`) | §5.2 + 1A |
| `skills/state-scanner/lib/claim_lifecycle.py` | heartbeat **增 by-track 并存变体** —— **签名 (R4/C-2 补, 镜像 `release_claim_by_track`; rework v4 去掉 `spec_slug` kwarg)**: `def heartbeat_by_track(raw_track_id: str, identity: Optional[Identity] = None, repo_path: Optional[Path] = None, *, now: Optional[datetime] = None) -> AcquireResult` (仿同文件 `release_claim` `:274` / `release_claim_by_track` `:377` 的并存模式; **既有 `heartbeat()` 的 `(container, session)` 匹配键 `:228` 不动** — D16)。**实现纪律**: 刷新 `heartbeat_at` 时用 `dataclasses.replace(existing, heartbeat_at=now)`, **不复制** `:244-256` 的逐字段重建 (R5/code-simplifier 选项 B; `ClaimRecord` 为 frozen dataclass, `claim_schema.py:69`) | **S1** (原版 Impact 表零覆盖) + R5 选项 B |
| `skills/state-scanner/lib/identity.py` | 新增直取 `uuid` 字段的 accessor —— **签名 (R4/C-2 补, 镜像 `get_container_id`)**: `def get_container_uuid(home_dir: Optional[Path] = None) -> str` (跳过 label) —— 现有 `get_container_id()` (`:191`) 在 `:222` 是 `return label if label else uuid`, 不能直接用; hostname 兜底分支 (`:242` `return _hostname()`) 成文, 与新生成 uuid 路径 (`:244` `return uuid`) 区分 | **S3** (原版 Impact 表零覆盖) |
| `skills/state-scanner/lib/collision.py` | `linked_issue_overlaps` 增 keyword-only 形参 `include_terminal: bool = False` (现三参数签名 `:230-234`; `_TERMINAL` 定义 `:268`; 详见清单 #3/#4/#5/#6/#16) | **R1-fix/C6** (R1 rework 核验 major-2 补, 原表零覆盖) |
| `skills/state-scanner/lib/constants.py` | ⚠️ **rework v3 回撤 (iii)**: **不改 `STALE_TTL`** (`:36` 维持 `1800`), **不动** `:32` 的「`STALE_TTL == 3 × HEARTBEAT_INTERVAL`」不变量注释 (前提未变)。**本行保留的唯一变更**: `:43-44`「NO production heartbeat loop exists (heartbeat() has zero production call sites…)」与 `:50`「Revisit when a heartbeat loop ships」两处注释, 在本 Spec 落地 heartbeat 编排层后**前提消失**, 须同步改写 —— **与 TTL 数值无关** | **C2 落版 (ii)** (owner 2026-08-22) + **(iii) 撤销** (owner 2026-08-23) |
| `skills/state-scanner/scripts/phase1_gate.py` | **A.1 模板调用的完整 flag 集 = `--raw-track-id` / `--phase A.1` / `--mode advisory` / `--linked-issue` (按 §2 两阶段取法; 非 `OK`·非真 token 时省略) / `--include-terminal` / `--repo-path`** (前四个与 `--repo-path` 为既有参数; **除 `--raw-track-id` 的 `required` 见第二处变更 ⑦ 外零改动**; 本行只改下列六处 —— R6/TL m1 订正计数): ① CLI flag `--include-terminal` (store_true); ② **在 `_main()` 的调用处 `:1233-1235` 加关键字参数** (不碰 `run_gate` `:1032` / `_run_gate_impl` `:335` 签名); ③ **门控 `:1230` 由 `if args.linked_issue:` 改为 `if args.linked_issue or args.include_terminal:`** + 新增 `unknown_schema_claims` 键 (D14); ④ **`:1236-1238` 的 `except` 分支不再写 `out["linked_issue_overlap"] = []`, 改写 `None` + `linked_issue_overlap_error`** (R2/M-4); ⑤ `error` 契约真正携带 `fetch_degraded` (`:210` docstring 已预留但从未赋值); ⑥ **同一 `except` 分支须同时赋 `out["unknown_schema_claims"] = None`** (R4/K5 → SC-33): 否则该键缺席被消费方 `.get(k, 0)` 读成 0, M-4 在自己的修复里复发 | **R3/C2** + **R2/M-3, M-4** + editlist **FIX-03** + **R4/K5** |
| `skills/state-scanner/scripts/phase1_gate.py` (第二处变更, 与上一行同文件不同能力) | 新增 **`--heartbeat-only` 模式**: 复用其 identity/fetch/push 管道; 入参 `--raw-track-id "<carry-id>"` (**来源 = §2.2 三级回落: ① 本 session claim 的 `track_id` → ② handoff §6 结构化 carry-id → ③ 两级都取不到 ⇒ 编排层仍调用且不传该参数, CLI 向遥测 JSONL 追加 `_source="heartbeat"` / `outcome="skipped_no_track"` 记录后退出 —— R4/K7: 独立 subprocess 的 logger 无 handler, 「只 log」= 空信号 (SC-32); 不猜 track**); 遥测一律走 `_source="heartbeat"` 分区, **不进** production 分区 (R3/TL-M2, SC-28 第二臂); 按 `(container, 归一 track_id)` 刷新全部匹配的 active claim 的 `heartbeat_at`, **不写新 claim, 不判碰撞**; 受 `coordination.enabled` 门控。**⑦ `--raw-track-id` 由 `required=True` (`:1187`) 改为 `required=False` + `_main()` 内模式校验** (R6/BA M1 + TL C3): 非 `--heartbeat-only` 模式缺参仍 `parser.error(...)` (acquire 路径的 fail-fast 不放松, 负控); `--heartbeat-only` 模式下可省 (SC-32)。与 `--phase` 的不对称理由: `--phase` 在 heartbeat 模式有占位值可传且不落盘 (§2.2), `--raw-track-id` 在「两级都取不到」时**没有值可传** (传空串会被 `derive_track_id` 归一成 sha256 哈希, 刷错 track)。三种落法中**钉死 (a)** `required=False` + 模式校验, 不用 subparsers、不拆独立脚本 (旧写「若 A.2 改为独立脚本 `scripts/heartbeat_gate.py` 亦属同一变更面」作废) | **C2 落版 (ii)** + **R2/M-12** + R6/BA M1, TL C3 |
| `skills/state-scanner/tests/` (既有宿主) | SC-2 / SC-3 / SC-5~8 / SC-10 / SC-14(a) / SC-15 / **SC-22** (扩 `test_coordination_default_lockin.py`, 同时承载 §2.1a 拼接的**文本层**) / **SC-23** / **SC-24** / **SC-25(代码臂)** / **SC-29** / **SC-32** / **SC-33** / **SC-34** + rule6_note 的三条 substitute 结构化测试 (`DEFAULTS.json` ↔ `config-loader/SKILL.md` 三键一致 / `layer-l-integration.md` 无 `update_heartbeat` 字面 / `coordination-ref-schema.md` §3.2 含 `unknown_schema_claims`)。**⚠️ SC-20 已撤销、SC-1/4/27/30/31 已随 1A 撤销, 均不在本行** | R1/C4 + rework v3 + rework v4 |
| `skills/phase-a-planner/SKILL.md` | A.1 **独立标题级** `前置: REQUIRE claim (A.1, MUST)` 步骤块, **放在 `### 步骤执行` (`:60`) 之前** (锚点、七个字面量与完整命令行见 SC-22 ①–⑦; 命令行 = §2 的模板 + `--linked-issue` 两阶段取法含 `--emit-arg` 分支) + A.1 YAML 项加 `precondition:` 指针 (SC-22 ⑤) + overlap/`unknown` 消费 (§2.3 按 status 分档的选项集) + release 义务 (§5.2: 放弃方向逐个 release / 改名两步) + `coordination.enabled` skip + **Level 1 (`skip_if: complexity: Level1`, 实读 `:67`) 时前置 claim 零调用** (R5/M4: 否则每个 typo 修复写一条永不 release 的僵尸 claim + 一次外向 push; SC-9 补该臂) + `unattended` 分支 | R3/M6 + R2/C-B + R2/M-15 + R5/M3, M4 |
| `skills/phase-a-planner/SKILL.md` frontmatter `allowed-tools` | **`:9`** `Read, Write, Glob, Grep, Task, Skill` → `Read, Write, Glob, Grep, Task, Skill, Bash, AskUserQuestion` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/spec-drafter/SKILL.md` | 第二落点 (同上的「前置: REQUIRE claim」步骤块 + 幂等谓词)。**⚠️「proposal 模板增『关联 Issue』字段」已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)**, 不在本 Spec | **S6** (原 **S4** 部分已迁出) |
| `skills/spec-drafter/SKILL.md` frontmatter `allowed-tools` | **`:10`** `Read, Write, Glob, Grep, AskUserQuestion` → `Read, Write, Glob, Grep, AskUserQuestion, Bash` | **C1 落版** (owner 2026-08-22, 采 (a)) |
| `skills/state-scanner/SKILL.md` | Layer L Phase B 集成段 (`:143-178` 一带, 触发条件在 `:149`) 新增对称的「Layer L A.1 heartbeat 集成」小节, **按既有 progressive-disclosure 体例缩为四句** (R5/M6): 触发条件一句 (本会话持有 active claim 且 `coordination.enabled == true` 的每次 `/state-scanner` 入口; 不依赖 `collision.kind` —— 这是「无条件」的准确含义, R2/M-7) + `--heartbeat-only` 完整命令行一行 + fail-soft 一句 + 指向 `references/layer-l-integration.md` 新设计段的指针; 三级回落表 / 遥测分区边界 / fail-CLOSED 新鲜度谓词 **整体落 reference** (否则 `:178`「完整设计意图见 references/…」变假指针, memory `delegate-verify`); 另 `:168` 列举的 CLI 输出键集补 additive 键 `push_skipped` / `push_skipped_reason` (aria-plugin `--no-push` 修复引入, 2026-08-30; 描述性同步, 与本行同 hunk) | **C2 落版 (ii)** + **R2/M-7, M-12**; **(R3/BA-M3 补) `:176` 的 Layer L 消费契约段同步四态**: `linked_issue_overlap` 现为 `list \| null \| 缺席`, 须写明「`null` + `linked_issue_overlap_error` 非空 ⇒ 渲染『未能核实』, **不得**渲染成『无碰撞』」—— Phase B 编排层读的就是这一段 |
| **`skills/phase-b-developer/SKILL.md`** (新增行) | B.0 步骤块 `:92` 的 `--raw-track-id "<本 cycle carry-id/Spec id>"` 占位措辞改为明示「**A.1 认领时派生的那一串**; 未走 A.1 的 session 沿用 Spec id」(**只改占位串取值口径, 不改闸门语义**) + **`:96-97` 注释勘正**: 该处写「write_claim auto_bootstrap 会自动建 ref 并 push 到项目 origin」, 2026-08-30 实读: `write_claim` 的 bootstrap 是 `push=False` (`lib/coordination_ref.py:800`), 真正的推送点是 `phase1_gate.py` 第 9 步 `resilient_push` (`:791-802`; 另有 7a self-resume 路径一处) —— 结论 (会推到 origin) 不变, 机制描述改为实际推送点; 同段 `skip_if` 补一句「`--no-push` / `ARIA_COORDINATION_NO_PUSH` 只抑制推送, 不是 skip 条件」(描述性勘正, 与占位串同 hunk) | **R2/C-C** + editlist **FIX-14 选项 A** + 2026-08-30 实读 |
| **`skills/branch-manager/SKILL.md`** (新增行) | `:146` 的 `### 前置: REQUIRE claim (Part A1, MUST — …)` 步骤块内同款 carry-id 占位措辞同步 (`:148` 一带)。**标题不改**: `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的部件名 (A1 = REQUIRE claim + `enabled` 默认翻转, B1 = `linked_issue`; 实读归档件 `:35,:50` 与 aria 内 `phase-b-developer:86` / `config-loader:136` / `state-scanner:149` / `test_coordination_default_lockin.py:1` 同名用法), **不是** Phase A.1 —— rework v4 曾按 R5/M2 的误读落成改名, R6/CR M1 撤回 | 同上 + R6/CR M1 |
| **`skills/phase-d-closer/SKILL.md`** (新增行) | D.2b (`:42` 表行, `:51-52` 调用) 的 `--raw-track-id "<本 cycle 的 carry-id 原始串>"` 与 `:55` 的说明句同步为同一口径。**⚠️ `:56` 的「超 STALE_TTL」误写属既有缺陷, 记 follow-up, 不在本 Spec 改** | 同上 + 清单 #14 |
| **`standards/conventions/session-handoff.md`** (新增行) | **§2.3.8** (非 §2.3 —— R3/KM-1) 结构化 `{id, desc}` 的 `id` 即本 cycle carry-id (= A.1 原串) —— **`track_id.py` 自称该文件为 SOT** ⇒ 不登记就是让 SOT 与实现脱钩 | **R2/M-14** (一半) |
| **`skills/state-scanner/docs/coordination-ref-schema.md`** (新增行) | **§3.2 (`:129` 起, 现枚举 reader 侧 unknown 行为 5 条于 `:133-140` (R6/CR m6 订正))** 后**追加第 6 条**: unknown claim 在 A.1 消费面的可见性与措辞语义 (经独立键 `unknown_schema_claims`; 措辞「已检测到 N 条无法解析的 claim, 存在性已确认、内容未知」; **不得**并入 `linked_issue_overlap[]`, **不得**与 `done`/`abandoned` 同档)。**断言形登记** (该文件**已实读确认存在**, 见清单 #28), 不写「若存在」条件形 | **R2/M-14** (另一半) + editlist **FIX-17** |
| `skills/state-scanner/references/layer-l-integration.md` | **三处, 缺一即留悬空引用**: ① `:15` 断言「Design A 条件触发: 闸门仅在用户确认要进入 Phase B 时调用, 不在 scan.py 内自动执行」, 本 Spec 增 A.1 触发点后即过时, 须同步; ② **`:45` 的函数名是悬空的** —— 该行逐字 `` \| `heartbeat` \| `phase-b-developer` mid-cycle \| 每 10min (caller 负责调度) \| `lib/claim_lifecycle.py::update_heartbeat()` \| ``, 而 `git grep update_heartbeat` 全 aria **只命中这一行自身** (清单 #33) ⇒ **`update_heartbeat()` 这个函数不存在**, 真名是 `heartbeat()` (`lib/claim_lifecycle.py:178`), 须改名; ③ **同一行的 caller/节律也与事实矛盾** —— 它写 caller = `phase-b-developer` 每 10min, 而 `lib/constants.py:43-44` 逐字自陈 `NO production heartbeat loop exists (heartbeat() has zero production call sites…)` ⇒ 该行描述的是一个**从未存在过的调度**, 须改写为本 Spec 落地后的真实 caller/节律 (`/state-scanner` 入口 AI 编排层, 每次调用, 受 `coordination.enabled` 门控); ④ **新增「Layer L A.1 heartbeat 集成」设计段** (从 SKILL.md 移来, R5/M6): 三级回落表 (§2.2 ①②③) / 遥测分区边界 (`_source="heartbeat"`, R3/TL-M2) / fail-CLOSED 新鲜度谓词 (`success == true` 且 `coordination_ref_present == true`) / `--heartbeat-only` **完整命令行** (D17 ② 在此落) | R1/M8 + **rework v3 实读新增 (A-8)** + R5/M6 |
| `skills/config-loader/SKILL.md` | ① `coordination` 在 A.1 的 skip 语义登记 (既有 `enabled` `:134` / `mode` `:140` 同节); ② **新增 `state_scanner.coordination.unattended` (boolean, default false) 登记** | R1/M3 + **R2/M-15** (editlist FIX-16) |
| **`skills/config-loader/DEFAULTS.json`** (新增行) | **注册 `state_scanner.coordination.{enabled, mode, unattended}` 三键**, 值与 `config-loader/SKILL.md:134`/`:140` 的登记逐字一致。**实测现状: `state_scanner` 段根本没有 `coordination`** (清单 #26) ⇒ 这是「登记了但没注册」的实缺口, 也是 rule6_note 描述性档 substitute 的被测对象 | **R2/M-17 第 5 项** |
| ⛔ `skills/audit-engine/SKILL.md` + `references/execution-modes.md` | **已随 §4 迁至 [`sibling-spec-probe`](../sibling-spec-probe/proposal.md)** | (原 R3/M5) |
| ⛔ `skills/audit-engine/scripts/sibling_spec_probe.py` + `tests/` | **已随 §4 迁出** (含目录新建) | — |
| ⛔ `.aria/state-checks.yaml` | **已随 §1 迁至 [`linked-issue-field-availability`](../linked-issue-field-availability/proposal.md)** (「关联 Issue」字段校验 check) | (原 **S4**) |
| ⛔ `standards/openspec/templates/proposal-minimal.md` (跨项目 SOT) | **R2/M-2 指出旧版漏登记该 SOT** ⇒ 该项**随 §1 整体迁至 `linked-issue-field-availability`** —— 「机械回声只覆盖 Aria 仓」是**字段可得性**的问题, 不是 A.1 认领的问题 | **R2/M-2** |
| AB 套件 — **照跑档** (`phase-a-planner.json` / `spec-drafter.json` [能力面 hunk] + `phase-b-developer.json` / `branch-manager.json` / `phase-d-closer.json` [占位串 hunk, R5/C1] + `state-scanner.json` [heartbeat 小节]) | **六套件均实存** (2026-08-30 `ls aria-plugin-benchmarks/ab-suite/` 实核) ⇒ 现有 AB 全量照跑, 零裁量; 验「扩权 / 占位串 / 新小节后既有 eval 场景行为是否漂移」。**硬前提**: harness 会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动 (rule6_note ⛔ 段; 对应的 `phase1_gate.py --no-push` flag 属 aria-plugin 独立修复, **不在本 Spec 变更面**) | rule6_note 11-hunk 表 |
| AB 套件 — `phase-a-planner` / `spec-drafter` (**覆盖外档**) | 定向 fixture: (a)(b)(c) 三条 + (e) `unattended` 臂 (SC-26); 与上一行「照跑现有 AB」**互不替代**。**⚠️ 旧版此行含的 `audit-engine` 已随 §4 迁出** (且 `ab-suite/audit-engine.json` **实测不存在**, 清单 #29) | rule6_note + **R2/M-6** |
| `aria-plugin-benchmarks/ab-suite/state-scanner.json` (照跑 AB 档) | 在**既有套件内**新增 1 eval case 钉点名行为 (d)「持 active claim 且 `enabled == true` 时 `/state-scanner` 入口每次触发 `phase1_gate.py --heartbeat-only`; `enabled == false` 时零触发」, 与 SC-21 / SC-28 呼应 (套件实存, `evals` = **12**) | rule6_note |

**follow-up (不在本 Spec, 各带去处)**:

| # | follow-up | 为什么不在本 Spec |
|---|---|---|
| 1 | `owner-container` (形如 `simonfish/bfe8285d`) 与 claim container 段 (`bfe8285d`) 的口径统一 | 牵动 handoff frontmatter 规范, 属 standards 变更 (S6 附带发现) |
| 2 | `release_gate.py:225` help / `state-scanner/SKILL.md:176` / `phase-d-closer/SKILL.md:56` 三处 `SWEEP_TTL`→`STALE_TTL` 措辞勘正 | 代码库**既有**缺陷, 非本 Spec 引入; 混进变更面会把「文档措辞勘正」和「机制变更」搅在一起 (清单 #14) |
| 3 | `unknown_schema_claims` 的**路径/身份**信息 | 需改 `ReadClaimsResult` (`lib/coordination_ref.py:119`) 的 NamedTuple 字段, blast radius 超本 Spec (D14) |
| 4 | `phase-b-developer` B.0 的 **YAML-键形态**升级为标题级 | 既有欠缺, 与本 Spec 的「前置: REQUIRE claim」落点正交; 拉平会扩大 Phase B 改动面, 撞 §非目标 (SC-22 docstring 已写明强度差异是有意的) |
| 5 | `unattended` 的 **Layer 1→2 env 传递三腿契约** (write + HCL declare + consumer import) | 会把 Layer 1/2 契约拉进本 Spec; 缺 import 时静默 fallback 到 `false` (即「照问不误」), 该风险已成文于 §2.3 |
| 6 | 跨容器**定向** release | 写别人的 claim 是权限面变更, 应独立评估 (D6) |
| 7 | `ClaimRecord` 加 **swept 标记** (分辨 `abandoned` 来自显式 release 还是 `--sweep-stale` 的 GC 产物, §2.3 K6) | 改 schema 字段, 须与 `coordination-ref-schema.md` §3 演进契约同批评估; 本 Spec 只在消费面按「可能是 GC 产物」保守渲染 (R6/CR M7 补行) |

---

## 审计与 spike 轨迹 — ⛔ **整节已切出**

> **迁往**: [`.aria/audit-reports/a1-entry-claim-audit-trail.md`](../../../.aria/audit-reports/a1-entry-claim-audit-trail.md) §1 —— **按字节搬运, 未重写任何一句**, 只加了节标题。
> 一并搬出的还有: §2.2 的 **(iii) 落版原文** (2026-08-23 owner 撤销前) 与两处**已闭环**的「⚠️ 实读订正 · 请 owner 复议」叙事 (审计轨 §2/§3/§4)。
> **owner 裁定原文 blockquote 留在本文件内** (§2.2 的 2026-08-22 与 2026-08-23 两条、§3 的 2026-08-22 一条) —— 它们是**承重设计输入**, 不是审计叙事; 上一轮把它们删掉换 AI 转述已被核验席判 major。
> **切分的四条声明** (append-only / 不维护一致性 / 以本文件为准 / 不得因审计轨回改本文件) 见本文件头部。**本次切分是执笔侧的流程判断, 已标请 owner 复议。**

报告索引 (未搬, 留此便于定位): 旧版三轮 `.aria/audit-reports/post_spec-R{1,2,3}-*-a1-entry-claim-duplicate-work-guard-*` (`b7c4933` 之前) · **重写 v2 R1** `post_spec-R1-1785710000000-a1-entry-claim-rewrite-*` (5 席 + 聚合 + **R1-fix editlist**) · **重写 v2 R2** `post_spec-R2-1787481000000-a1-entry-claim-rewrite-aggregated.md` (5 席, 3C/17M, REVISE 未收敛) · spike `.aria/spikes/2026-08-02-*`

---

## R1-fix editlist 逐条对账 (R2/M-13 —— **零容忍自述不实**)

> **为什么有这一段**: R2/CR-M4 命中「Spec 三处自述『R1-fix 已全量吸收』, 而 editlist 的 12 项实际未落」。**本段用逐条对账取代任何形式的总结句**; 全文**不再出现**「已全量吸收 / 已全部处理」之类无锚点的自述 (memory `past-summary≠measurement`)。
> **锚点**: 「本文小节」列给的字符串可直接在本文件内 grep。editlist SOT = `.aria/audit-reports/post_spec-R1-fix-editlist-a1-entry-claim.md`。

| FIX | 主题 (editlist 原题) | 状态 | 锚点 / 去处 |
|---|---|---|---|
| FIX-01 | C1 — `spec-drafter` allowed-tools 行号错一行 + 表下补取证命令 | **已落 (上一轮)**, 本轮复核行号 | grep `spec-drafter/SKILL.md:10` (§3 表 + Impact 表 + 清单 #2) |
| FIX-02 | C6 — 「实读现签名」代码块与真实文本不符 | **已落 (上一轮)**, 本轮换 `d50f9c3` 口径 | grep `:230-234` (§2.4 传递链 item 0 + 清单 #4) |
| FIX-03 | C4 — `unknown` 改走独立 additive 键 ⭐ 承重 | **本轮落** | grep `§2.4a` + `unknown_schema_claims` (§2.4a / SC-24 / D14 / Impact `phase1_gate.py` 行③) |
| FIX-04 | C2 — 删 `A1_SWEEP_TTL` 72h 分档 | **已落 (重写 v2 起即无该分档)** | 全文 grep `A1_SWEEP_TTL` 只命中本行自身 (自指), 无其他命中 (R6/CR m6) |
| FIX-05 | C5 — `--sweep-stale` 阈值误写是**三处** | **本轮定性为 follow-up** (硬约束: 文档措辞勘正不混进变更面) | grep `超 STALE_TTL` (§非目标 + Impact follow-up #2 + 清单 #14) |
| FIX-06 | C3-a — 语料统计数字全文回灌 | **⛔ 随 §1 迁至 `linked-issue-field-availability`**; 本轮另把主体内残留的 `141/13/9%` **换成 rework v3 实测口径** | grep `⭐ 真正的瓶颈` + 清单 #30 |
| FIX-07 | C3-b — check 作用域 + 回填 6 篇 ⭐ 承重 | **⛔ 随 §1 迁出** | §1 指针段 |
| FIX-08 | C3-c — canonical token 抽取规则自相矛盾 | **⛔ 随 §1 迁出** | §1 指针段 |
| FIX-09 | ⭐ NEW-01 — `无` 绝不可作 `--linked-issue` 实参 | **已落 (上一轮)**, 本轮补行号订正 + 归属划分 | grep `token 为「无关联」哨兵时` (§2 模板下 blockquote; rework v4 措辞随哨兵集合 `{none, 无}` 调整); 「字段值怎么写」归子 Spec, 「实参必须省略」留主体 |
| FIX-10 | M3 — 探针「同 issue」谓词对 `无` 归属未定义 | **⛔ 随 §4 迁至 `sibling-spec-probe`** | §4 指针段 |
| FIX-11 | M1 — 姊妹 Spec SC-8 的字面禁止加 keyword-only 形参 ⇒ 必需编辑 | **不适用 (前提已消失)** —— 姊妹**已 ship 并归档**, 且**它自己**在 ship 前写入了关闭条款 (`archive/2026-08-23-linked-issue-normalization/proposal.md:257`/`:260`) ⇒ 本轮**不改归档件** | grep `该协调项已完全闭环` (§2.4 传递链 item 0) + 清单 #16 |
| FIX-12 | M5 — 三态扩为四态 + §6 缺口表补最大一项 | **本轮落** | grep `§2.4b 四态契约` + §6 缺口表首行 (grep `token 为哨兵`) |
| FIX-13 | M8 — SC-21 断言形态对「塞进 YAML 列表」免疫; `### B.0` 不存在 | **本轮落** (三处: 锚点换 `branch-manager:146` / 新 **SC-22** 正则形态 / §3 幂等分工) | grep `前置: REQUIRE claim` (§2 触发时机 + §3 + SC-22) |
| FIX-14 | M2 — §5 漏「A.1 成功并走完循环」, D.2b 匹配不到 | **本轮落 (选项 A)** | grep `§2.1b carry-id 契约` + §5.2 第 4 行 + **SC-23** + Impact 三行 SKILL.md + `session-handoff.md` 行 |
| FIX-15 | CR-M1 — SC-1/SC-15 二分谓词换「track-id 形态是否含 slug」 | **⛔ 已随 1A 失效 (2026-08-30)** —— 二分谓词连同 issue 派生形一并取消; 语义单元恒为 (container, spec-slug) | §5.1 (rework v4) + 审计轨 §6 |
| FIX-16 | CR-M5 — 无人值守判据被 C1 抹平 | **本轮落** | grep `unattended` (§2.3 blockquote + §3 AD10 句 + D15 + **SC-26** + Impact `config-loader` / `DEFAULTS.json` 两行) |
| FIX-17 | KM — `coordination-ref-schema.md` **存在**, 改断言形 | **本轮落** | Impact 表 `coordination-ref-schema.md` 行 (断言形 + `:129`/`:133-139` 锚点) + 清单 #28 |
| FIX-18 | MINOR — S3 spike 的 `identity.py:244` 是「补」不是「改」, 且替换项本身也错 | **本轮落 (三处出处 + S3 勘误注)** | §2.1 表格 `container_uuid` 行的依据格 (grep `S3 spike 勘误`) + Impact 表 `identity.py` 行 (`:191`/`:222`/`:242`/`:244`) + 清单 #11。**存疑项见「本轮未做 / 存疑」#1** |
| FIX-19 | dogfood — 本 Spec 自身补「关联 Issue」字段 | **本轮落 (本文件头部)**; **姊妹 Spec 那一半不适用** (已归档, 不改归档件) | 本文件 `> **Linked Issue**: \`10CG/Aria#174\`` (第 **13** 行; 冒号后第一个非空白是 inline-code span; rework v4 按字段 Spec 2026-08-30 英文 canonical 改写, rework v4.1 把哨兵改为真 token —— 生产 ref 里本轨 claim 的 `linked_issue` 即 `10CG/Aria#174`, R6/KM m2; 中文拼写仍是合法 alias) |

**editlist 的 deferred / owner 裁项**: D-a (sweep vs 自愿 abandon 的 provenance 可分辨) 与 D-b (`unknown` 的路径/身份) **维持 deferred**, 各自记入 Impact follow-up #3 与另开 issue; D-c (B.0 YAML-键形态) 记入 follow-up #4。U-1 (删 S1 产出) **未采** —— heartbeat by-track 变体保留, 但已按其备选要求成文写明「`heartbeat()` 至今零生产调用点 ⇒ 改匹配键不产生刷新者」(§2.2 首段 + SC-21), 不冒充保护窗。U-2 (回填 6 份 aria-orchestrator proposal) **随 §1 迁出**。U-3 (carry-id 选项 A/B) **本轮采 A 并标请 owner 确认** (§2.1b)。U-5 (改姊妹 Spec) **前提消失** (FIX-11)。U-6 (`unattended` 消费侧接线) **本轮按其倾向办**: 只登记 key + 加 SC-26, 接线转 A.2, 并成文声明三腿契约缺口 (§2.3)。

---

## rework v4 (2026-08-30) 引入 / 改动的表面 —— **R6 已审** (五席结论与逐条处置见 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md`); 本表保留为 R6 输入的原样, 「请 R6 看什么」列的答案在聚合报告 §处置

> 按硬约束「任何新表面必须列出」逐条声明。**本段是给 R6 审计席的输入, 不是完成度自述。** rework v3 与 R3 清账轮的两份「新表面」清单及「本轮未做 / 存疑」表已随 1A 失效大半, 原文按字节移入审计轨 §6; 其中仍成立的条目在下表重列。

| # | 表面 | 性质 | 请 R6 看什么 |
|---|---|---|---|
| 1 | **§2.1 单一形态 `<spec-slug>-<container_uuid>`** (1A) | owner 裁定的结构变更 | 是否还有残留在按「有无 issue」分形态 (全文 grep `派生形` / `回落形` / `track_form` / `spec_slug` 应只命中撤销说明与审计轨指针) |
| 2 | **§5 整节重写** (三退出路径 + 改名两步; §5.3 撤销) | 结构变更 | SC-14(b) / SC-15 / SC-23 三条是否把退出路径覆盖完; 「放弃整个 issue = 逐方向 release」有没有漏掉一种退出 |
| 3 | **SC-2 / SC-15 改为 baseline 即绿的回归守卫** (第 5 项) | 验收分类 | 坏实现是否像样 (memory `adversarial-fixture`); 「怎么会红」是否真能红 |
| 4 | **SC-22 扩为 ①–⑥ + 块边界定义 + 两文件路径绑定** (R5/skill-reviewer M1/M2/M3/M5/m2 + D17) | 机械断言强化 | 是否仍存在「插几行字面即绿」的实现; 边界定义是否有歧义 (例如切片内出现 ```yaml 围栏时 ⑤ 与「不在围栏内」的关系) |
| 5 | **D17 三要件** (块边界 / 至少一条完整命令行 / fail 分支消费措辞字面) | 类级处方, 两子 Spec 引用 | 三份 Spec 是否各自真的按它写了 SC (字段 SC-7a / 探针 SC-20) |
| 6 | **rule6_note 重算为 11 hunk / 9 文件 + 照跑档前提 `ARIA_COORDINATION_NO_PUSH=1`** (R5/C1/C2) | Rule #6 落档 | 逐 hunk 落档是否有错档; 前提引用的修复是否真实存在 (aria 分支 `fix/phase1-gate-no-push`) |
| 7 | **SC-32 / SC-33 进表; SC-11 补 K6 措辞; SC-1/4/27/30/31 ⛔** | 回灌 | 三条 grep 不变量 (每个 `SC-NN` 在表内 / 每个 `--flag` 在 Impact 表内 / 枚举拼写唯一) 执笔侧已亲跑, R6 只需复跑 |
| 8 | **哨兵集合 `{none, 无}` + 字段名英文 canonical** (6i + O-2) | 跨 Spec 接缝 | 母 Spec 只引用字段 Spec 的定义; R6 须核三份 Spec 对哨兵/字段名的措辞一致 (memory `split-makes-seams`) |
| 9 | **`heartbeat_by_track` 须用 `dataclasses.replace`** (R5 选项 B, 只约束新代码) | 实现纪律 | 是否越界改了既有 `heartbeat()` (§非目标: 不动既有键) |

**本轮未做 / 存疑 (给 R6)**:

| # | 未做 / 存疑 | 影响 |
|---|---|---|
| 1 | **7c / 7d 两个分支的具体行号未实读** (承前, 清单 #22 已声明) | A.2 实施时须先定位 |
| 2 | **`phase-a-planner/SKILL.md` 内部委派动作的行号未钉**: 本轮实读 A.1 YAML 项在 `:62-73` (`skip_if: complexity: Level1` 在 `:67`), 但委派 `spec-drafter` 的具体动作行未钉 | SC-22 ⑤ 的 `precondition:` 落点由 A.2 钉 |
| 3 | **SC-2 / SC-23 的相容性无断言** (承前) | 二者设计相容 (carry-id 就是含容器段那一串), A.2 须补一条 |
| 4 | **rule6_note 三条 substitute 的负控未验** (DEFAULTS 三键 / layer-l 无 `update_heartbeat` / schema §3.2 第 6 条) | 只验了 baseline 必红; A.2 须各验一个坏实现 |
| 5 | **两子 Spec 的 6i / O-2 落版由主控本轮一并执笔** (未换人) | R6 须专门看三份的哨兵/字段名措辞是否一致 (新表面 #8) |
| 6 | **第 4 项修复 (`--no-push`) 已升格为硬前置** (头部「前置依赖」+ 闸门状态表 #7, R6/TL M5); 该分支 2026-08-30 **未推、非 `origin/master` 祖先** | Phase B.1 前须断言它已合入 `origin/master`, 否则 Rule #6 六条照跑无法进行 (ship 需 owner 授权推送 + 发版) |

---

## 闸门状态 (Rule #10 — AI 不自行判定)

`audit.checkpoints.post_spec = "convergence"` **enabled**, 封闭豁免白名单四类无一适用 ⇒ **本版按默认跑 post_spec, 不豁免**。

**已裁事实** (rework v4 更新):

1. 重写 v2 的 post_spec **R1 (5 席) / R2 (5 席)** 已跑完, 均 REVISE (R2: 3C/17M, major 持平);
2. **owner 2026-08-22 裁 C1/C2** (C1 采 (a) 扩权; C2 原采 (ii)+(iii), 08-23 复议后 (iii) 撤销); **owner 2026-08-23 裁方向 b** (缩 scope, 拆两子 Spec, 换人执笔);
3. rework v3 后 **R3 (五席联审三份, 3C/19M) → 清账 → owner 08-27 裁方向 a → R4 (五席全新镜头, ≈9C, 判定发散, 8/9 由上轮 fix 引入) → 清账 → R5 (五席第三批镜头, ≈6 簇)** 全部跑完, **`max_rounds=5` 用尽**; R5 判定「设计侧收敛, 落版侧系统性失败」;
4. **owner 2026-08-30 六项裁定** (决策单 `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`): 1A / 2b / **3b = 加跑 R6** / 4i / 5 采纳 / 6i + 否决「只认中文的机器 token」; 本版 (rework v4) 即其落版;
5. **post_spec R6 已跑完 (2026-08-30, owner 显式加轮)**: 五席 (config `teams.post_spec`, 全新镜头) 判 **REVISE** —— CR 3C/11M/13m · BA 0C/2M/1m · TL 6C/9M/7m · QA 0C/3M/2m · KM 0C/3M/2m (PASS); 去重后 **7 个 critical 簇** (E6 省略门与 `--emit-arg` 归属 / 探针依赖方向 / Level 1 零调用 / SC-22 ⑤ 与切片互斥 / SC-22 缺完整命令行 / SC-32 撞 argparse `required` / 预览骨架默认哨兵), **本轮 (rework v4.1) 已逐条清账** (清单见 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md` §处置; 探针依赖方向属 owner 裁, 未动)。五席一致**不建议 R7**, 建议清账后只做定向复核。**AI 不预判 owner 对 R6 结果的裁决。**
6. **owner 2026-08-30 (R6 后) 裁定**: (a) 探针依赖方向 → **(i) 字段纯函数是探针硬前置** (探针 §1/§3 + 字段 O-4 已落版); (b) 字段名 E0 大小写折叠 → **(i) 折叠, 单复数不放宽** (字段 E0/SC-1 已落版); (c) R5 code-simplifier 四项范围建议 (删 `--heartbeat-only` / 转出 `unknown_schema_claims` / 白名单改注册行参数 / editlist 对账表迁回 SOT) → **都不采纳**; (d) 清账执笔 → **不换席** (流程判断表 #8 复议闭合); (e) **授权推送** (主仓 6 commit + aria 修复分支按 PATCH 发版)。**下一步 = owner 批准进 A.2/A.3。**

**本轮的 AI 流程判断 (Rule #10 — 请 owner 复议, 不自行落定)**:

| # | 判断 | 为什么须复议 |
|---|---|---|
| 1 | **切出审计轨** (D-J, 承前) + 本轮把 1A 移出的原文 (旧 §2.1/§5.1/§5.3/K1/K2/K3/K4、两份「新表面」清单、旧「未做/存疑」表) 追加进审计轨 §6 | 仿姊妹 Spec 的 owner 2026-08-07 先例; 搬运无损 |
| 2 | **carry-id 统一采 editlist 选项 A** (改三处 SKILL.md 占位串取值口径, §2.1b) | R3–R5 三轮未被推翻, 但 owner **从未显式确认**「这不算动 Phase B」; 仍待一句话 |
| 3 | **§2.3 选项集按 status 分档** (承前) | 执笔的综合裁断, 扩大了 A.1 决策面 |
| 4 | **SC-27 整条撤销** (而非只撤 (C) 臂) | R5 报告只说选项 A 让 SC-27**C** 消失; 主控判定 (A)(B) 两臂在 1A 下与 SC-14(b)/SC-23 重合 (放弃方向 = 逐方向 release), 故整条撤销。若 owner 认为应保留「放弃方向 1 ⇒ 方向 2 仍 active」作回归守卫, 恢复为 baseline-绿的守卫行即可 |
| 5 | **O-2 (字段名) 与第 6 项 (哨兵) 同批落版为「英文 canonical + 中文 alias」** | owner 只对哨兵裁了 (i), 对字段名的 O-2 是「质疑只认中文」的延伸推定; 回撤成本见决策单 |
| 6 | **R6 沿用 config `teams.post_spec` 五个 agent, 但各席镜头由执笔侧指派** (实现者试派生 A.2 / 「怎么会红」逐条实证 / 对抗夹具三态 / 跨 Spec 接缝 / 断言内容事实核) | 席位组成在 config 里, 镜头指派不在; 沿用 R4/R5「换新鲜眼睛」的做法, 但具体指派未经 owner 点头 |
| 7 | **Phase B.1 前置断言: aria-plugin `--no-push` 修复须已合入 `origin/master`** (头部前置依赖新增行, R6/TL M5) | 该修复是 Level 1 独立变更, 其 ship 需 owner 授权推送 + 发版; 把它列为本 Spec 硬前置是执笔判断 |
| 8 | **R6 清账由主控 (同一执笔) 一次落版, 未换人** —— tech-lead 席建议「换执笔席落 6C/9M」, 主控未采 (理由: 7 个簇里 6 个是条款级文本修正, 有五席给出的字面级处方; 换席的交接成本高于收益) | 与 owner 既往「换人执笔」处方 (memory `fix-writer-bottleneck`) 相左 → **owner 2026-08-30 (R6 后) 复议: 不换席, 维持** (定向复核已由新席位做, PASS) |

> **2026-09-01 归类裁定** (owner 分工: 产品级 owner / 技术级 AI): 上表 #1–#6 属技术/流程级, 逐条裁定 = **全部维持** (#2 = 选项 A 成立, 不算动 Phase B; 判据见 TASK-019 verification); #7 已闭环 (v1.67.2 = `d69091d` 双远端); #8 owner 2026-08-30 已裁。全文与回退指引见决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`。

~~本 Spec 在 R6 跑完并经 owner 批准前不进 A.2/A.3。~~ **owner 2026-08-30 已批准进 A.2/A.3**; A.2/A.3 产物 `tasks.md` + `detailed-tasks.yaml` 已派生, `audit.checkpoints.post_planning = "convergence"` enabled ⇒ 按默认跑 post_planning (combined 三份), 不豁免。
