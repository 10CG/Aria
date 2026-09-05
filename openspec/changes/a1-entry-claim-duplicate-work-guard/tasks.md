# A.1 Entry Claim Duplicate-Work Guard — Tasks

> **Spec**: [proposal.md](./proposal.md) (rework v4.1, owner 2026-08-30 批准进 A.2)
> **Level**: 2 → 本文件由 A.2 (task-planner) 派生, 使 Spec 具备 OpenSpec 双层架构 (tasks.md + detailed-tasks.yaml)
> **Status**: ✅ **A.2/A.3 complete** (2026-08-30; post_planning R1 FAIL → R2 PwW → R3 PwW → **R4 CONVERGED 2026-08-31 (五席 5/5 PASS, 0C 0M)**) — 全部任务 `pending`, ready for B.1 (版本档 = MINOR 各占一号 + 流程判断 #2 = 选项 A 成立, 均已裁 2026-09-01, 决策单 `2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`)
> **Scope repo**: 代码落 `aria/` 子模块 @ **d69091d** (v1.67.2, 含 `--no-push` 修复); 一行落 `standards/` 子模块 (5.8); Spec / AB 结果落主仓
> **行号基线**: Spec 正文写的是 aria `d50f9c3`; 本轮全部锚点按 **d69091d 实读**, 与 Spec 不一致处记在 detailed-tasks.yaml 各任务 `notes` 与末尾「行号复核」段 (**不改 proposal.md**)
> **决策源**: `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md` (六项裁定; 第 4 项 `--no-push` 已 ship v1.67.2) · R6 聚合 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md`
> **编号纪律**: 本文件 `N.M` 编号一经确立**不可变** (DUAL_LAYER_SPEC); 新增只追加, 取消只标 `(CANCELLED)`

---

## Task Group Overview

| Group | 主题 | Spec 落点 |
|-------|------|-----------|
| 1 | Phase B.1 前置断言 (`--no-push` 已在 origin/master / 子 Spec 导出物 / 行号锚点复核) | 头部前置依赖 · 闸门状态 #7 · `:763-766` 待办 (1) |
| 2 | TDD 红测 — 代码类 SC 的夹具先行 (好实现 + 坏实现; baseline 即绿者单独标明) | Success Criteria 代码类全部 |
| 3 | lib 代码 (`identity` / `claim_lifecycle` / `collision`) | Impact 表 lib 三行 |
| 4 | `phase1_gate.py` 两处变更 (`--include-terminal` 六处 / `fetch_degraded` / `--heartbeat-only` ⑦) | Impact 表 `phase1_gate.py` 两行 + `coordination_probe.py` 行 |
| 5 | SKILL.md / references / config / standards 文本层 (A.1 双落点 · carry-id 三处 · heartbeat 小节 · 登记) — **GREEN, 各任务依赖对应第 6 组 RED** (R1 C1) | Impact 表文档行 |
| 6 | 结构化测试 (SC-22 / SC-34 / rule6_note 三条 substitute + 两条补充 substitute, 各带负控) — **RED, 位于第 5 组上游**, 在 d69091d 上先跑出全红并留痕 (R1 C1) | SC-22 · SC-34 · rule6_note #6/#10/#11/#12 · `:763-766` 待办 (4) |
| 7 | Rule #6 — 照跑 AB 六套件 + 覆盖外定向 fixture + 套件缺口 issue | rule6_note 12-hunk 表 · Impact AB 三行 |
| 8 | 文档 / CHANGELOG / 发版同步面 / follow-up 开单 | Impact follow-up 表 · CLAUDE.md §版本管理 |

> **顺序**: 1 → 2 → 3/4 → **6 (RED) → 5 (GREEN)** → 7 → 8 (R1 C1 翻转第 5/6 组, 编号不变)。全部顺序约束已编码进 detailed-tasks.yaml `dependencies` (非散文): 第 2 组全部 + 第 6 组链首挂 TASK-001 (B.1 硬阻断门) 与 TASK-003 (锚点核对); 第 3/4/5 组首任务挂 TASK-003; **同文件一律串行** (`phase1_gate.py` 4.1→4.2→4.3 / `test_heartbeat_by_track.py` 2.2→2.3 / `test_a1_entry_gate_cli.py` 2.4→2.5→2.6 / `test_coordination_default_lockin.py` 6.1→…→6.6 / `ab-suite/version.yaml` 7.3→7.5), 组内并行仅限不同文件。**任何组 7 任务运行前 harness 会话必须以 `ARIA_COORDINATION_NO_PUSH=1` 启动** (`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:222-228`)。

---

## 1. Phase B.1 前置断言

- [x] 1.1 断言 aria-plugin `--no-push` 修复已在 `origin/master` 且主仓 gitlink 指向它 (v1.67.2 = `d69091d`); 双远端 `ls-remote` 一致 (闸门状态 #7 硬前置) — ✅ **2026-09-05 B.1 起点重核**: `d69091d` ∈ origin/master ∧ github/master 历史 (`merge-base --is-ancestor`); 双远端 `ls-remote` + 主仓 gitlink 三者同为 `7dd0135`; `--no-push` 代码在 origin/master 实读在场; 负控 `test_coordination_no_push.py` 16/16。**verification 第 1 条配方已陈旧** —— `log --oneline -5` 窗口此后 ship 5 版, 现 0 命中 `d69091d`, 实质改用 `merge-base` 断言 (窗口宽度问题, 非实质不成立)
- [x] 1.2 记录两份子 Spec 导出物存在性 (`linked_issue_field_probe.py --emit-arg` + `lib/linked_issue_field.py` / `sibling_spec_probe.py`) 与 §2 两阶段模板哪一分支 live (**advisory, 不阻塞** — proposal :96/:423「均非阻塞前置」; 缺席 ⇒ 手工 E6 / 「无覆盖」), 不自建替身 — ✅ **2026-09-05**: 三导出物均在场且与 yaml deliverables 路径逐条一致 (`state-scanner/scripts/linked_issue_field_probe.py` · `state-scanner/lib/linked_issue_field.py` [Layer L 包, 非 `scripts/lib/`] · `audit-engine/scripts/sibling_spec_probe.py`); §2 两阶段模板 **分支 1 (`--emit-arg`) live** —— 对本 Spec proposal 实跑产出 `10CG/Aria#174`, 与本 cycle B.0 认领所传 `--linked-issue` 值一致; 另记录项 `grep 'Linked Issue' spec-drafter/SKILL.md` **4 命中 ⇒ TASK-018 走分支 (i)** (字段 Spec hunk A/B 已 ship); 未自建替身
- [x] 1.3 B.1 起点重跑行号锚点核对 (7a/7c/7d 分支 + Step 9 推送点 + `_main()` 门控/except + `release_gate` 三选一 + 各 SKILL.md 锚点), 与 detailed-tasks.yaml 锚点表比对, 漂移则更新 `notes` (`:763-766` 待办 (1)) — ✅ **2026-09-05 零真漂移**。方法: 基线-对照 (正则须先在 `d69091d` 命中表列那一行才算钉对锚点, 否则判为检查器自身问题而非漂移 — memory `check-runs-at-baseline-first`); 17 个校验通过的锚点全部未漂。**决定性判据**: 15 个承载锚点的文件里 **14 个与 `d69091d` 逐字节相同** (hash-object 比对), 唯一变更 `spec-drafter/SKILL.md` (+26/−2) 的三处 hunk 全在 `:107`/`:131`/`:333` 之后, 与本 Spec 两锚点 (`:10` frontmatter / `:73` `## 执行流程`) **区域不相交** ⇒ 决策单 C8「hunk A 与前置块冲突」担忧证伪。锚点表照原样成立, `notes` 无需更新

## 2. TDD 红测 (代码类 SC, 夹具先于实现)

- [x] 2.1 SC-3: `get_container_uuid()` 单测 — 设了 `label` 的 container-id 夹具仍取 `uuid` 字段; 坏实现 = 直接调 `get_container_id()` (baseline 必红: accessor 不存在) — ✅ **2026-09-05**: 新建 `tests/test_identity_container_uuid.py` 5 用例 (SC-3 主断言 / 夹具区分力 / 空 label 对照 / `:244` 落盘臂 / `:242` hostname 兜底臂)。**baseline 红已亲验** (`ImportError: cannot import name 'get_container_uuid'`); **两个坏实现负控实跑**: A 委派型 (`return get_container_id`) ⇒ 主断言红 · B 不落盘型 (跳过 `_write_container_file`) ⇒ 落盘臂 + hostname 兜底臂双红; 负控后按 `git hash-object` 核验已还原
- [x] 2.2 SC-5 / SC-6 / SC-7: `heartbeat_by_track` 单测 — 跨 subprocess 第二次不同 session_id 仍刷新 / 一对多全部刷新 / SC-7 两臂 (超 `SWEEP_TTL` 仍被 sweep **且** 调新变体后不被 sweep) — ✅ **2026-09-05**: 新建 `tests/test_heartbeat_by_track.py`, SC-5/6/7 共 8 用例 (跨 session 刷新 / 既有 heartbeat 区分力臂 / raw 串归一 / 一对多全刷 / 跨容器·跨 track 负控 / 11 字段保留 / SC-7 两臂)。baseline 红亲验 = `ImportError: heartbeat_by_track`; 三条夹具前提先在基线单独证过 (既有 heartbeat 跨 session 返回 `claim_not_found` / `derive_track_id('A1.Spec_1a2b3c4d')=='a1-spec-1a2b3c4d'` / 未刷新 claim 过 SWEEP_TTL 被 abandoned)。**四个坏实现负控实跑**: 沿用 session 键 ⇒ 5 红 · 只刷第一条 ⇒ SC-6 红 · 不归一 ⇒ 归一用例红 · 逐字段重建漏 `linked_issue` ⇒ 保留用例红
- [x] 2.3 SC-15 (baseline 即绿回归守卫): 改名两步 `release_claim_by_track(旧)` + `acquire_claim(新)` 无孤儿 + 无关第三方 claim 负控 (不共享前缀/后缀、不同容器段); 坏实现 = 匹配键改按 `linked_issue` / 按 container 批量 — ✅ **2026-09-05**: 同文件加 `TestRenameTwoStep` 4 用例;「baseline 即绿」四条前提先在基线单独实证。**⚠️ 发现 Spec 夹具缺陷并已补**: 原文要求第三方 claim「与旧/新不共享任何前缀/后缀」(`zzz-unrelated-9f8e7d6c`, 容器 B), 同时要求它在「去掉 `rec.container` 合取」的坏实现下变红 —— 二者不相容, 因 `track_id` 走精确相等, track 不同的 claim 无论有无 container 合取都匹配不到 ⇒ **该断言结构上恒绿, 零信息**。实跑负控当场证实 (NC5 全绿)。处置 = **加**一条容器 B 中**同 track_id** 的 claim (不动原第三方夹具), 补后 NC5 红。三个坏实现负控现全部实跑变红: 去 container 合取 / 按 container 批量 (由同容器 sibling 捕获) / 子串匹配
- [ ] 2.4 SC-2 / SC-8 / SC-29 (CLI 全链路 subprocess): 同 issue 不同 track-id 双方互含 (SC-2, baseline 即绿) / 终态 `done`·`abandoned` 带 `--include-terminal` 可见 (SC-8, baseline 必红) / 自排除两组 own=active 与 own=terminal (SC-29, baseline 即绿); 负控 = 删 `lib/collision.py:278-279` 两行验红
- [ ] 2.5 SC-24 / SC-33 / SC-25 代码臂 / SC-10 (CLI 全链路): `unknown_schema_claims` 计数且不入 overlap[] / `read_claims` 抛异常 ⇒ 双 `null` + error 非空 / overlap 抛异常 ⇒ `null` + error / fetch 降级 ⇒ `error == "fetch_degraded"` (四条 baseline 必红)
- [ ] 2.6 SC-23 / SC-14(a) (CLI 全链路, baseline 即绿回归守卫): A.1 原串 X acquire → `release_gate.py --raw-track-id X` ⇒ 不再 active; `--status abandoned` 臂; **补 SC-2 ↔ SC-23 相容性断言** (同一 `<slug>-<uuid>` 串既能 overlap 互见又能 release 命中; `:763-766` 待办 (3))
- [ ] 2.7 SC-32 + SC-28 第二臂 + argparse 负控 (CLI 全链路): 无 carry-id 跑 `--heartbeat-only --phase A.1 --repo-path` ⇒ 遥测恰一条 `_source="heartbeat"` / `outcome="skipped_no_track"`, 不写 claim 不推远端; `coordination_probe` production 计数不变; 非 heartbeat 模式缺 `--raw-track-id` 仍 `parser.error` (baseline 必红: 模式不存在)

## 3. lib 代码

- [x] 3.1 `lib/identity.py` 新增 `get_container_uuid(home_dir=None) -> str` (直取 `uuid` 字段, 跳过 label; hostname 兜底 `:242` 成文) — ✅ **2026-09-05**: 纯插入 **+61 −0** 于 `:247` (`get_container_id` `:191-244` 逐字节不变, 硬约束满足); TASK-004 5/5 绿; 除定义与测试外**零调用点**; 全 aria 套件 10 skill OK / 2017 tests 零回归。**技术级裁定留痕**: `lib/__init__.py` 未加再导出 —— identity 公开函数由 5/5 变 5/6, 理由 = deliverables 只列 `identity.py` 一个文件 + verification 的 grep 口径在多一处出现时可争议 + 设计上该 accessor 经 `from lib.identity` 直调 (§2.1a 不建拼接宿主)。若 Group 3 复核认为应对齐导出面, 一行即可补
- [x] 3.2 `lib/claim_lifecycle.py` 新增 `heartbeat_by_track(raw_track_id, identity=None, repo_path=None, *, now=None) -> AcquireResult` (按 `(container, 归一 track_id)` 刷全部 active; `dataclasses.replace`; 既有 `heartbeat()` `:228` 键不动; `ClaimRecord` 11 字段零改动) — ✅ **2026-09-05**: `heartbeat_by_track` 落 `release_claim_by_track` 之后, 匹配用同款三合取, 刷新用 `dataclasses.replace` (函数体内 `ClaimRecord(` 出现 **0** 次); `claim_schema.py` diff 为空; `heartbeat()` 函数体**逐字节相同**。**锚点位移 (本任务引入, 已量清)**: 为 `dataclasses.replace` 加了一行模块级 `import dataclasses`, 使 `claim_lifecycle.py` 全部锚点**统一 +1** — `acquire_claim` :99→:100 · `heartbeat` :178→:179 · `(container, session)` 键 **:228→:229** · `release_claim_by_track` :377→:378; 文件 471→579 行。后续任务引用这些行号须按 +1 读
- [ ] 3.3 `lib/collision.py::linked_issue_overlaps` 增 keyword-only `include_terminal: bool = False` (默认路径逐字节不变; `:278-279` 自排除对终态同样生效)

## 4. `phase1_gate.py`

- [ ] 4.1 第一处变更 ①②③④⑥: `--include-terminal` flag / `_main()` 调用处加关键字参数 / 门控放宽为 `if args.linked_issue or args.include_terminal:` + `read_claims` 只调一次 + `unknown_schema_claims` 键 / `except` 改写 `linked_issue_overlap = None` + `linked_issue_overlap_error` + `unknown_schema_claims = None`
- [ ] 4.2 第一处变更 ⑤: `GateResult.error` 真正携带 `"fetch_degraded"` (Step 4 `health_check_fetch` 降级时; `:219` docstring 已预留)
- [ ] 4.3 第二处变更 ⑦ + `--heartbeat-only` 模式: `--raw-track-id` `required=False` + `_main()` 模式校验; 三级回落由编排层传入, CLI 不推断; 按 `(container, 归一 track_id)` 刷全部匹配 active claim; 遥测 `_source="heartbeat"` + `outcome ∈ {refreshed, skipped_no_track, skipped_disabled, error}`; 不写 claim / 不判碰撞 / 不自带 fetch; `coordination_probe.py` 口径注释

## 5. 文本层 (SKILL.md / references / config / standards) — GREEN, 各依赖对应 6.x RED (R1 C1; 段落位置不变, 执行序在第 6 组之后)

- [ ] 5.1 `phase-a-planner/SKILL.md`: frontmatter `:9` `allowed-tools` 加 `Bash, AskUserQuestion` + 独立标题级 `### 前置: REQUIRE claim (A.1, MUST)` 块 (放 `### 步骤执行` `:60` 之前; 七字面量 + 完整命令行 + 幂等谓词 + `--linked-issue` 两阶段取法含 `--emit-arg`) + A.1 YAML 项 (`:63`) 首键 `precondition:` 指针 (**委派动作行 = `:64` `skill: spec-drafter` / `:68-70` `action:`; `skip_if: complexity: Level1` = `:67`**, `:763-766` 待办 (2)) + §2.3 按 status 分档选项集 + §5.2 release 义务 + `coordination.enabled`/Level 1 零调用 + `unattended` 分支
- [ ] 5.2 `spec-drafter/SKILL.md`: frontmatter `:10` `allowed-tools` 加 `Bash` + 第二落点 `## 前置: REQUIRE claim (A.1, MUST)` 块 (放 `## 执行流程` `:73` 之前; 同款字面量 + 幂等谓词; 无 Level 1 例外)
- [ ] 5.3 carry-id 三处占位措辞 (§2.1b, 逐字 `A.1 认领时派生的那一串`): `phase-b-developer/SKILL.md:92` + `:96-97` push 机制注释勘正 + `skip_if` 补「`--no-push` 只抑制推送不是 skip 条件」/ `branch-manager/SKILL.md:149` (命令行; R1/A4 实读, 原记 `:148` 是前一句; 标题 `:146` **不改**) / `phase-d-closer/SKILL.md:51-52` + `:55` (`:56` STALE_TTL 误写不改, follow-up)
- [ ] 5.4 `state-scanner/SKILL.md`: Layer L 段 (`:143-178`) 新增「Layer L A.1 heartbeat 集成」四句小节 (触发条件 / `--heartbeat-only` 完整命令行 / fail-soft / 指针) + `:168` 键集补 `push_skipped` / `push_skipped_reason` + `:176` 消费契约同步四态 (`list | null | 缺席`); 同批同步 `lib/constants.py:43-44` / `:50` 注释 (前提消失)
- [ ] 5.5 `state-scanner/references/layer-l-integration.md` 四处: `:15` Design A 句同步 A.1 触发点 / `:45` `update_heartbeat()` → `heartbeat()` + caller/节律改真实 / 新增「Layer L A.1 heartbeat 集成」设计段 (三级回落表 / 遥测分区边界 / fail-CLOSED 谓词 `success == true ∧ coordination_ref_present == true` / 完整命令行)
- [ ] 5.6 `config-loader/SKILL.md` 登记 `coordination` A.1 skip 语义 + 新 key `state_scanner.coordination.unattended` (boolean, default false; 取值路径 = aria-runner 镜像内 `.aria/config.json`); `config-loader/DEFAULTS.json` 注册 `state_scanner.coordination.{enabled, mode, unattended}` 三键 (现状: `coordination` 整段缺席)
- [ ] 5.7 `state-scanner/docs/coordination-ref-schema.md` §3.2 (`:129`) 追加第 6 条: `unknown_schema_claims` 语义 (独立键 / 措辞 / 不并入 overlap[] / 不与 done·abandoned 同档)
- [ ] 5.8 `standards/conventions/session-handoff.md` §2.3.8 (`:217`; **非** §2.3): 结构化 `{id, desc}` 之 `id` = 本 cycle carry-id = A.1 原串 (standards 子模块: 本地 merge + 双推 + 逐个 `ls-remote`)

## 6. 结构化测试 (文本层 SC + rule6_note substitute, 均扩 `test_coordination_default_lockin.py`) — RED, 位于第 5 组上游; 同文件串行 6.1→6.6 (R1 C1)

- [ ] 6.1 SC-22 ①–⑦: 两文件各自断言 (标题正则 + 围栏外 / 切片边界 `^#{1,4}[ \t]` / 七字面量 / 幂等谓词逐字 + `claims/` / 禁 `--phase B` / ⑤ `phase-a-planner` 切片外按 `A.1 - Spec 管理:` 锚点定位 yaml 围栏 (**实读 8 处 ```yaml, Spec 写 7**) / ⑥ 两条退出义务字面 / ⑦ 续行折叠后含 `python3 … phase1_gate.py … --phase A.1` 完整命令行); docstring 写明与 `test_phase_b_require_claim_present` (`:53-56` 裸 `assertIn`) 的强度差异是有意的
- [ ] 6.2 SC-34: `phase-b-developer` / `branch-manager` / `phase-d-closer` 三文件各 ≥1 逐字 `A.1 认领时派生的那一串` (baseline 必红; 只改两处 ⇒ 红)
- [ ] 6.3 substitute (rule6 #6): `DEFAULTS.json` `state_scanner.coordination.{enabled, mode, unattended}` 三键与 `config-loader/SKILL.md:134`/`:140`/新登记值逐字一致 (baseline 必红); **负控** = 注册三键但 `unattended` 默认写 `true` / 漏 `mode` 键 ⇒ 红 (`:763-766` 待办 (4))
- [ ] 6.4 substitute (rule6 #10a): `layer-l-integration.md` 不含字面 `update_heartbeat` **且** 含 `heartbeat(` (baseline 必红); **负控** = 把 `:45` 改成 `heartbeat_by_track()` 却在别处新写一句 `update_heartbeat` ⇒ 红; 只删不补 `heartbeat(` ⇒ 红
- [ ] 6.5 substitute (rule6 #11): `coordination-ref-schema.md` §3.2 切片 (`### 3.2` 起至 `### 3.3` 止) 含字面 `unknown_schema_claims` (baseline 必红); **负控** = 字面写进 §4.2 而非 §3.2 ⇒ 红 (切片外)
- [ ] 6.6 补充 substitute (rule6 #10b + #12): `layer-l-integration.md` 含标题字面 `Layer L A.1 heartbeat 集成` 且该节切片含 `--heartbeat-only` (baseline 必红; 负控 = 标题在、命令行在别节 ⇒ 红); `state-scanner/SKILL.md` `:168` 一带 (`### JSON 消费` 切片) 含字面 `push_skipped` (baseline 必红; 负控 = 写进 `## 相关文档` ⇒ 红)

## 7. Rule #6 (allowed-tools 扩权 = 能力面变更 ⇒ 照跑; 覆盖外 ⇒ 定向 fixture + issue)

- [ ] 7.1 照跑 `ab-suite/phase-a-planner.json` (当时套件全部 eval, d69091d 时 2; 零裁量; 前置 `ARIA_COORDINATION_NO_PUSH=1`; 结果落 `ab-results/<date>-<vNEXT>-a1-entry-rule6/`, `<vNEXT>` = 落地时按 plugin.json 计算, 不预写)
- [ ] 7.2 照跑 `ab-suite/spec-drafter.json` (当时套件全部 eval, d69091d 时 2 / 字段 Spec ship 后 3; 同上)
- [ ] 7.3 `ab-suite/state-scanner.json` 新增 eval (id = 当时 max(id)+1, d69091d 时 13) 钉点名行为 (d) (`enabled == true` 且持 active claim ⇒ 每次入口触发 `--heartbeat-only`; `enabled == false` ⇒ 零触发; SC-21 / SC-28 第一臂) 后照跑全部 eval (当前值 + 1); 同批程序化重算 `ab-suite/version.yaml`
- [ ] 7.4 照跑 `ab-suite/phase-b-developer.json` / `branch-manager.json` / `phase-d-closer.json` (占位串 hunk, 各按当时套件全部 eval, d69091d 时各 2)
- [ ] 7.5 覆盖外档定向 fixture: `phase-a-planner.json` 增 (a) 拼串 + `--linked-issue` 省略/传递 (SC-9(A)(B) / SC-12 两臂 / SC-14(b)) · (b) overlap 非空请裁 + status 分档 (SC-11) · (c) fetch 降级/异常渲染「未能核实」(SC-25 行为臂) · (e) `unattended` 臂 (SC-26); `spec-drafter.json` 增 (a)(b) 两条 (新 eval id = 当时 max(id)+1, 不与字段 Spec 的 id 3 冲突; 不改任何既有 eval); 双臂可分辨; 同批程序化重算 `ab-suite/version.yaml` (串行于 7.3 后)
- [ ] 7.6 套件缺口 issue: **新开** aria-plugin issue「phase-a-planner / spec-drafter 套件零覆盖 A.1 入口认领编排行为」, 正文交叉引用 `#117` (同族: 处方性 · 套件覆盖外) 与 `#127`, **不归并** (理由见 detailed-tasks.yaml TASK-036 notes)

## 8. 文档 / 发版 / follow-up

- [ ] 8.1 `aria/CHANGELOG.md` 条目 + 版本 SOT 5 文件同步 (`.claude-plugin/plugin.json` / `marketplace.json` / `VERSION` / `README.md` / CHANGELOG); 号 = `<vNEXT>`, **落地时按 plugin.json 计算, 本文件不锁字面量** (A.2 倾向 MINOR: 新 CLI 模式 + 2 flag + 2 lib API + 能力面扩权; **档位 = MINOR (2026-09-01 技术裁定, 决策单 §H1)**, 三份串行 ship 各占一号, 不合并一版; 号落地时按当时 plugin.json 计算)
- [ ] 8.2 主仓发版同步面 (与 086ee32 同口径 14 处版本点, R1 C2): gitlink `aria` bump 到 post-merge master SHA (index 条目, 非 `.gitmodules`) + 主仓 `VERSION:24` + `CLAUDE.md:139/:141` + root `README.md:8/:242` + i18n ×3 (`README.zh.md` / `README.ja.md` / `README.ko.md` 各 `:3` translated-from 标记 + `:10` badge + `:244` Plugin Version; 正文按 #140 B 档判是否重译, **标记与版本串必改**) → 全部改完后才断言机械兜底 `m6-version-badge-match` / `i18n-readme-translation-currency` 绿
- [ ] 8.3 follow-up 开单 (不在本 Spec, 各带去处): Impact follow-up 表 #1–#7 (`owner-container` 口径 / `SWEEP_TTL`→`STALE_TTL` 三处措辞 / `unknown_schema_claims` 路径 / B.0 YAML-键形态 / `unattended` Layer 1→2 env 三腿契约 / 跨容器定向 release / `ClaimRecord` swept 标记) + §2.2 已知限「audit-engine 轮间 heartbeat」
- [ ] 8.4 aria 子模块本地 merge → master + 双推 + 逐 remote `ls-remote` 核验 + tag (CLAUDE.md 硬约束 1/2 的任务宿主; 两 remote 一致后才做 8.2 gitlink bump) — R2/A1 3221f943 残留补; **执行序 8.1 → 8.4 → 8.2** (编号不可变, 列于末不代表最后做; 见 yaml dependencies)

---

## SC → TASK 覆盖表 (现行 23 / 撤销 6 / 迁出 5 = 34)

| SC | 类 | 状态 | TASK (verification 落点) |
|----|---|------|---|
| SC-1 | — | ⛔ 撤销 (1A) | — |
| SC-2 | 代码 CLI, baseline 即绿 | 现行 | TASK-007 (红测) · TASK-013/014 (实现后回归) · TASK-009 (相容性) |
| SC-3 | 代码 | 现行 | TASK-004 · TASK-011 |
| SC-4 | — | ⛔ 撤销 (1A) | — |
| SC-5 / SC-6 / SC-7 | 代码 | 现行 | TASK-005 · TASK-012 |
| SC-8 | 代码 CLI | 现行 | TASK-007 · TASK-013 · TASK-014 |
| SC-9 (A)(B) | 行为 | 现行 | TASK-035 (fixture a) · 文本义务 TASK-017 |
| SC-10 | 代码 CLI | 现行 | TASK-008 · TASK-015 |
| SC-11 | 行为 | 现行 | TASK-035 (fixture b) · 文本 TASK-017 |
| SC-12 | 行为 | 现行 | TASK-035 (fixture a 两臂) · 文本 TASK-017/018 |
| SC-13 | — | 迁出 → `linked-issue-field-availability` | — |
| SC-14 (a) | 代码 CLI, baseline 即绿 | 现行 | TASK-009 |
| SC-14 (b) | 行为 | 现行 | TASK-035 (fixture a) |
| SC-15 | 代码, baseline 即绿 | 现行 | TASK-006 · TASK-012 (实现后回归) |
| SC-16 / SC-17 / SC-18 | — | 迁出 → `sibling-spec-probe` | — |
| SC-19 (a)(c) | — | 迁出 → `sibling-spec-probe` | — |
| SC-19 (b) | — | 由 SC-29 承担 | 见 SC-29 |
| SC-20 | — | ⛔ 撤销 (owner 2026-08-23) | — |
| SC-21 | 行为 | 现行 | TASK-033 (eval-13 臂 A) · 文本 TASK-020 |
| SC-22 ①–⑦ | 代码 (文本层) | 现行 | TASK-025 · 被测文本 TASK-017/018 |
| SC-23 | 代码 CLI, baseline 即绿 | 现行 | TASK-009 · TASK-019 (文本半由 SC-34) |
| SC-24 | 代码 CLI | 现行 | TASK-008 · TASK-014 |
| SC-25 ① 代码臂 | 代码 CLI | 现行 | TASK-008 · TASK-014 |
| SC-25 ② 行为臂 | 行为 | 现行 | TASK-035 (fixture c) |
| SC-26 | 行为 | 现行 | TASK-035 (fixture e) · key TASK-022 · 文本 TASK-017 |
| SC-27 | — | ⛔ 撤销 (1A; AI 流程判断 #4 待复议) | — |
| SC-28 第一臂 | 行为 | 现行 | TASK-033 (eval-13 臂 B) |
| SC-28 第二臂 | 代码 CLI | 现行 | TASK-010 · TASK-016 |
| SC-29 | 代码 CLI, baseline 即绿 | 现行 | TASK-007 · TASK-013/014 |
| SC-30 / SC-31 | — | ⛔ 撤销 (1A) | — |
| SC-32 | 代码 CLI | 现行 | TASK-010 · TASK-016 |
| SC-33 | 代码 CLI | 现行 | TASK-008 · TASK-014 |
| SC-34 | 代码 (文本层) | 现行 | TASK-026 · 被测文本 TASK-019 |

**未覆盖**: 无。**注意**: SC-32 的遥测文件名与 `_telemetry_path` 分区路由存在 Spec 内部歧义 (见「待 owner 裁」#3), TASK-010 的断言对象钉为 `_telemetry_path(repo, "heartbeat")` 的返回路径而非硬编码文件名。

## Impact 行 → TASK 覆盖表

| Impact 行 | TASK |
|---|---|
| `lib/claim_schema.py` 零改动 | TASK-012 verification (`git diff --stat` 对该文件为空) |
| `scripts/coordination_probe.py` 口径注释 | TASK-016 |
| `scripts/release_gate.py` 零改动 | TASK-009 verification (`git diff --stat` 为空) |
| `lib/claim_lifecycle.py` | TASK-012 |
| `lib/identity.py` | TASK-011 |
| `lib/collision.py` | TASK-013 |
| `lib/constants.py` 注释 | TASK-020 |
| `scripts/phase1_gate.py` 第一处 ①–⑥ | TASK-014 (①②③④⑥) · TASK-015 (⑤) |
| `scripts/phase1_gate.py` 第二处 `--heartbeat-only` + ⑦ | TASK-016 |
| `tests/` 既有宿主 | TASK-004~010 · TASK-025~030 |
| `phase-a-planner/SKILL.md` 正文 + frontmatter | TASK-017 |
| `spec-drafter/SKILL.md` 正文 + frontmatter | TASK-018 |
| `state-scanner/SKILL.md` | TASK-020 |
| `phase-b-developer` / `branch-manager` / `phase-d-closer` SKILL.md | TASK-019 |
| `standards/conventions/session-handoff.md` §2.3.8 | TASK-024 |
| `state-scanner/docs/coordination-ref-schema.md` §3.2 | TASK-023 |
| `state-scanner/references/layer-l-integration.md` | TASK-021 |
| `config-loader/SKILL.md` · `config-loader/DEFAULTS.json` | TASK-022 |
| ⛔ `audit-engine/*` · `.aria/state-checks.yaml` · `proposal-minimal.md` | 迁出 (子 Spec), 无任务 |
| AB 照跑档六套件 | TASK-031 / 032 / 033 / 034 |
| AB 覆盖外档 (a)(b)(c)(e) | TASK-035 |
| `state-scanner.json` eval (d) | TASK-033 |
| follow-up #1–#7 | TASK-039 |

**flag / config / JSON 键 → TASK**: `--include-terminal` (014) · `--heartbeat-only` (016) · `--no-push` / `ARIA_COORDINATION_NO_PUSH` (001, 031–035) · `--emit-arg` (002, 017, 025) · `--raw-track-id` / `--phase A.1` / `--mode advisory` / `--linked-issue` / `--repo-path` (017, 018) · `--status abandoned` / `--sweep-stale` / `--gc` (009, 019) · `state_scanner.coordination.{enabled, mode, unattended}` (022, 027) · `unknown_schema_claims` / `linked_issue_overlap_error` / `linked_issue_overlap: null` (014, 008) · `push_skipped` / `push_skipped_reason` (020, 030) · `error: "fetch_degraded"` (015) · 遥测 `_source="heartbeat"` / `outcome` 枚举 (016, 010)。

---

## 不落任务的项 (明写)

- **§2.3 已知限「`unattended` 的 Layer 1→2 env 传递三腿契约」** → Impact follow-up #5, 由 TASK-039 开单, **本 Spec 不实现** (缺 import 静默 fallback 到 `false` 的风险已成文于 §2.3)。
- **§2.2 已知限「长审计轮期间 heartbeat 一次不刷」** → 属 audit-engine 变更面, 不在本 Spec; TASK-039 一并开单。
- **§3 口径待定「`owner-container` 与 claim container 段」** → follow-up #1, 不统一。
- **闸门状态「本轮 AI 流程判断」8 条** → 不是任务, 是 owner 复议项, 下段照录。
- **`.aria/` 目录 / 其他 Spec 目录 / proposal.md** → 本轮 A.2 不动 (行号差异只记 `notes`)。

## 待 owner 复议 (照录 proposal.md 闸门状态「本轮 AI 流程判断」8 条, Rule #10)

| # | 判断 | 为什么须复议 | 状态 (08-30 → 2026-09-01 分工裁定, 决策单 `2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`) |
|---|---|---|---|
| 1 | 切出审计轨 (D-J) + 1A 移出原文追加进审计轨 §6 | 仿姊妹 Spec owner 2026-08-07 先例; 搬运无损 | ✅ 维持 (2026-09-01 技术级: owner 08-07 先例 + memory `audit-trail-not-in-spec`, 搬运无损可逆) |
| 2 | carry-id 统一采 editlist 选项 A (改三处 SKILL.md 占位串取值口径, §2.1b) | R3–R5 未推翻, 但 owner 从未显式确认「这不算动 Phase B」 | **✅ 已裁 2026-09-01 (技术级): 选项 A 成立, 不算动 Phase B — 判据 = TASK-019 三条 git diff / 测试字节级约束 + TASK-034 三套件照跑 (无闸门被跳过)** |
| 3 | §2.3 选项集按 status 分档 | 执笔综合裁断, 扩大 A.1 决策面 | ✅ 维持 (2026-09-01: 每档选项 = 机械可达动作的枚举 (`claim_lifecycle.py:427` / `gc.py:324` 实读), active 档三选项逐字保留, 无产品级选项被移除) |
| 4 | SC-27 整条撤销 (而非只撤 (C) 臂) | (A)(B) 两臂在 1A 下与 SC-14(b)/SC-23 重合; 若 owner 要保留「放弃方向 1 ⇒ 方向 2 仍 active」回归守卫, 恢复为 baseline-绿守卫行即可 | ✅ 维持撤销 (2026-09-01: 1A 后无「N 方向共用 track_id」机制 (proposal :456), 两臂已由 SC-14(b)/SC-23 覆盖; 要回归守卫时恢复 baseline-绿行即可) |
| 5 | O-2 字段名与第 6 项哨兵同批落「英文 canonical + 中文 alias」 | owner 只对哨兵裁了 (i), 字段名是延伸推定 | ✅ 维持 (2026-09-01: owner 08-30 对「只认中文」的反驳要求 + memory `machine-tokens-english` 同规则; R6-2 大小写折叠已裁 (i)) |
| 6 | R6 沿用 config 五席但镜头由执笔指派 | 镜头指派未经 owner 点头 | ✅ 关闭 (2026-09-01: R6 已于 08-30 跑完且 owner 裁不再加轮, 镜头指派不在 config 管辖面, 无后续动作) |
| 7 | Phase B.1 前置断言: `--no-push` 须已合入 `origin/master` | 执笔判断把 Level 1 独立变更列为硬前置 | **已闭环**: v1.67.2 = `d69091d` 已在 `origin/master` 与 `github/master` (本轮 `ls-remote` 实核) |
| 8 | R6 清账未换执笔席 | 与 owner 既往「换人执笔」处方相左 | **已裁**: owner 2026-08-30 (R6 后) 不换席 |

## 待 owner 裁 (A.2 本轮新增, 不自行拍板)

> **2026-09-01 分工裁定** (owner: 产品级 owner / 技术级 AI): #1 已闭合; #6 (版本号) 已裁 MINOR 各占一号 (决策单 §H1); #2–#5 与 #7 属技术级, 由 AI 在 B 期落点裁定并追记决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`, 不再等 owner。

1. ~~子 Spec 导出物「不存在 ⇒ 阻塞」(1.2) 与 Spec §1/§4 矛盾~~ **已闭合 (非 owner 事项)**: 「阻塞」来自主控 A.2 指令的误写, 2026-08-30 核实 proposal :96/:423 后撤回, 1.2 / TASK-002 / `ship_order_note` / P2-P3 已按 Spec 改为 advisory (任意顺序 ship 自洽, 字段缺席退化为零输入)。留痕供复议。
2. **探针 Spec 的输出母 Spec 并不消费** (探针 §1 依赖方向第 2 条逐字; 母 Spec 只有 §6 缺口表两行依赖它「覆盖」) — 已按此落版: 1.2 对探针只记录「脚本存在与否」, 不写消费契约。留痕供复议。
3. **SC-32 遥测文件**: SC-32 写 `.aria/coordination-telemetry.jsonl`, 但 `phase1_gate.py:1010-1013` `_telemetry_path` 把非 `production` 源一律路由到 `coordination-telemetry-nonprod.jsonl`。三选一: (a) `_source="heartbeat"` 走既有路由落 nonprod 文件 (SC-32 文件名随之改); (b) 新增第三分区文件; (c) 写 production 文件但 `_source="heartbeat"` (probe 已忽略非 production 记录, 但违背结构性分区设计)。A.2 倾向 (a), TASK-010 断言钉 `_telemetry_path(repo, "heartbeat")` 返回路径以对三案免疫。
4. **SC-22 ⑤「文件内共 7 处 yaml 围栏」实读为 8 处** (`:47/:62/:103/:146/:161/:230/:249/:265`); 断言按 `A.1 - Spec 管理:` 锚点定位不受影响, 但 Spec 数字错, 是否勘正 proposal 请裁。
5. **SC-26 的 handoff 宿主未定义**: 「handoff 待复议段出现 `awaiting_owner`」—— A.1 阶段无 handoff 产物 (handoff 由 phase-d-closer D.3 / session-closer 写), `awaiting_owner` 字面在 aria 全仓零命中。请裁 `unattended` 分支写到哪 (候选: `docs/handoff/latest.md` §待复议 追加 / `.aria/notes/` 待复议记录)。
6. ~~**版本号**: 待 owner~~ **✅ 已裁 (2026-09-01, 决策单 §H1)**: 档位 = **MINOR** (SOT `version-management.md §2.2`「功能增强 (向下兼容)」字面覆盖: 新 CLI 模式 + 2 flag + 2 lib API + allowed-tools 扩权); 三份串行 ship 各占一号 (字段 → 探针 → 母), 不合并一版; 号 = `<vNEXT>` 落地时按当时 plugin.json 计算, 不预写 (R1 C3 撞号教训不变)。TASK-037 可按依赖开工。
7. **SC-10 `error` 优先级**: 同一次运行 fetch 降级且 Step 9 push 失败时 `error` 取哪个 token 未定; TASK-008 夹具以 `--no-push` 隔离, 实现者按「后发硬错覆盖先发软降级」落, 请 owner 确认或改。

---

## 行号复核 (Spec 基线 d50f9c3 → 本轮实读 d69091d)

| 文件 | Spec 写 | d69091d 实读 | 原因 |
|---|---|---|---|
| `scripts/phase1_gate.py` `logger` | `:56` | `:61` | `--no-push` 修复 (v1.67.2) 新增 docstring/import 行, 全文件下移 |
| 同 `GateResult.error` docstring (`fetch_degraded`) | `:210` | `:219` | 同上 |
| 同 `_takeover_eligible` | `:283-294` | `:299-311` | 同上 |
| 同 `_run_gate_impl` def | `:335` | `:351` | 同上 |
| 同 7a self-resume 分支 | 未实读 | `:537-538` (`if _self_resume(...)`), self-resume push `:573`, `no_push` 门 `:554` | 本轮补钉 |
| 同 7c 分支 | 未实读 | `:693-697` (`elif verdict.winner is not None and not _takeover_eligible(verdict)`) | 本轮补钉 |
| 同 7d 分支 | 未实读 | `:761-762` (注释 `No prompt needed: stale / terminal tracks are safe to acquire.`) | 本轮补钉 |
| 同 Step 9 `resilient_push` | `:791-802` | `:835` 注释起, `no_push` 门 `:848`, `resilient_push(` `:856` | 同上 |
| 同 `_telemetry_path` / `_gated` / `run_gate` | `:950` / — / `:1032` | `:1010` / `:1049` / `:1094` (分区句 `:1112`) | 同上 |
| 同 `_main` def | `:1173` | `:1255` | 同上 |
| 同 `--raw-track-id` `required=True` | `:1187` | `:1269` | 同上 |
| 同 `--phase` `required=True` | `:1191` | `:1273` | 同上 |
| 同 `if args.linked_issue:` 门控 | `:1230` | `:1332` | 同上 |
| 同 `linked_issue_overlaps(` 调用 | `:1233-1235` | `:1335-1337` | 同上 |
| 同 `except` 写 `[]` | `:1236-1238` | `:1338-1340` | 同上 |
| `scripts/release_gate.py` `sweep_stale_active(` 调用 | `:141` | `:150` | 同上 (release_gate 同套 `--no-push`) |
| 同 `--sweep-stale` help `STALE_TTL` 误写 | `:225` | `:246` | 同上 |
| 同「三选一」`parser.error` | `:236-237` | `:267-268` | 同上 |
| `phase-a-planner/SKILL.md` ```yaml 围栏数 | 7 | **8** | Spec 计数错 (待 owner 裁 #4) |
| `scripts/phase1_gate.py` CLI 契约注释 `args : --raw-track-id --phase [--mode …] [--linked-issue]` | — (A.2 记 `:1155-1158`) | `:1154` | R1/A4 实读, A.2 漂 1 行 (TASK-014 注释已改) |
| `branch-manager/SKILL.md` `--raw-track-id <carry-id>` 命令行 | `:148` | `:149` | R1/A4 实读, `:148` 是前一句 (TASK-003/019 注释与 5.3 已改) |
| **`lib/claim_lifecycle.py` 全部锚点 (本 cycle TASK-012 引入)** | `:99`/`:178`/`:228`/`:377` | **`:100`/`:179`/`:229`/`:378` (统一 +1)** | 新增一行模块级 `import dataclasses` (TASK-012 verification 要求 `dataclasses.replace` 字面命中); 函数体逐字节不变, 仅整体下移 |
| 其余 (`claim_lifecycle` / `identity` / `collision` / `constants` / `track_id` / `claim_schema` / `coordination_ref` / `gc` / `reconcile` / `coordination_probe` / 各 SKILL.md / references / docs / tests / `session-handoff.md`) | 见 detailed-tasks.yaml | **逐条一致, 未漂** | v1.67.2 只动 `phase1_gate.py` / `release_gate.py` / `failure_handlers.py` / 新增 test + 发布面 |

---

## Notes

- **Phase A.3**: 无需新 Agent — 既有 roster `backend-architect` (lib / CLI) · `qa-engineer` (红测 / 结构测试 / AB) · `knowledge-manager` (SKILL.md / references / config / standards / CHANGELOG) · `tech-lead` (跨仓前置断言 / issue 裁量 / 主仓同步面) 覆盖全部 40 任务。
- **协作原则**: 子 agent 只跑自己域测试、不 commit (主控统一, memory `workflow-file-domain`); 同文件串行 (`phase1_gate.py` 4.1→4.2→4.3; `test_heartbeat_by_track.py` 2.2→2.3; `test_a1_entry_gate_cli.py` 2.4→2.5→2.6; `test_coordination_default_lockin.py` 6.1→6.6; `ab-suite/version.yaml` 7.3→7.5) — **全部已编码为 yaml `dependencies` 边并程序化验证** (R1 C1, 见下「机械核验」)。
- **子 Spec 接缝**: 母 Spec **不编辑**字段 Spec 的 `spec-drafter` hunk A/B 与探针 Spec 的 audit-engine 面; 字段 Spec **不编辑**母 Spec 的 frontmatter `:10` 与「前置」块 (字段 Impact 逐字)。**相邻性不是既成事实**: 后 ship 一方以 `git merge-tree` 干跑核验 (TASK-018 两分支 / 字段 TASK-014 对称, R1 C6)。`ab-suite/spec-drafter.json` 与 `version.yaml` 的跨 Spec 写入约定见 yaml `seam_rules` 第 3 条 (R1 C5)。

---

## R1 清账对账 (2026-08-30)

> post_planning R1 五席 combined (`.aria/audit-reports/post_planning-R1-1788102593777-a1-entry-combined-A{1..5}-*.md`, 聚合 `…-aggregated.md`); 只列 scope 含本 Spec 的 finding 与跨 Spec 统一项。清账按主控方案 (`r1_fix_plan.md`, 随 R2 聚合归档) 定点编辑, 不重写文件、不改编号、不改 proposal.md。

| finding id | 席 | 簇 | 处置 | 改动落点 |
|---|---|---|---|---|
| `73809784` | A2 (critical) | C1 同文件缺边 | **closed** | yaml: TASK-016 加 TASK-015; TASK-026←025←…←030 链 (各加前一任务); TASK-006 加 TASK-005; TASK-008 加 TASK-007, TASK-009 加 TASK-008; 另 R1 后新发现 `ab-suite/version.yaml` 共写 ⇒ TASK-035 加 TASK-033。机械核验 (a) 19 个共写文件 40 对全部有边 |
| `bd55ab9c` | A3 (critical) · A4 (critical) | C1 第 6 组依赖第 5 组倒置 | **closed** (处方 (a) 翻转边) | yaml: TASK-025~030 `dependencies` 改为 `[TASK-001, TASK-003]` + 链前一任务, 不再依赖第 5 组; TASK-017/018 加 TASK-025, 019 加 026, 020 加 030, 021 加 028+030, 022 加 027, 023 加 029; 第 5 组各 `verification[0]` 改「本任务落文本后, 对应 TASK-02x 由红转绿 (基线 d69091d 上先红)」; TASK-025 notes「落文本前跑全红」改为可执行措辞; tasks.md 组序自述「5 → 6」改「6 (RED) → 5 (GREEN)」(段落与编号不动)。机械核验 (c) 通过 |
| `3221f943` | A3 (major) | C1 TASK-001 不在第 2 组边 | **closed** | yaml: TASK-004~010 全部加 TASK-001; 第 6 组链首 TASK-025 同加 (bd55ab9c 处方「与 Group 2 同款」); 第 3/4/5 组首任务 (TASK-011/014/017) 加 TASK-003; TASK-017/018 加 TASK-002 (018 原有)。机械核验 (c') 除 TASK-001/002/003/039 外全部传递到达 TASK-001 与 TASK-003; `phase_b_preconditions` P1/P4 改为指向真实边 |
| `73809784` | A1 (critical) | C2 TASK-038 发布同步面 | **closed** | yaml TASK-038: 删 `.gitmodules` (不承载 gitlink) 与不存在的 `README.zh-CN.md`; 改列 `aria` gitlink / `VERSION:24` / `CLAUDE.md:139,:141` / `README.md:8,:242` / `README.zh.md` `README.ja.md` `README.ko.md` 各 `:3/:10/:244` (= 086ee32 的 14 处版本点, 与字段 TASK-024 同口径); verification 改为「全部改完后才断言两条 check 绿」+ 「B 档不重译但标记与版本串必改 (check 读的是 `translated-from` 标记)」; tasks.md 8.2 同步 |
| `518a7d7f` | A4 (major) | C2 `README.zh-CN.md` | **closed** | 同上 (与 A1 73809784 同一改动) |
| `3221f943` | A1 (major) | C3 版本档撞号 + ab-results 字面量 | **closed** (留痕, 不拍板) | yaml: TASK-031~035 五处 `ab-results/<YYYY-MM-DD>-v1.68.0-…` → `<vNEXT>` 占位 (目录形态沿既有 `<date>-<ver>-<slug>-rule6/` 惯例); TASK-037 标题 / CHANGELOG 条目 / `grep '1.68.0'` 断言全部去字面量, notes 写入三份统一句 (档位与号由 owner 裁; 串行各占一号; 合并一版由母承接; 未裁不开工 status 仍 `pending`); tasks.md 7.1 / 8.1 / 待 owner 裁 #6 同步。两文件 `grep '1\.68\.0'` 零命中 |
| `af9f0c47` | A5 (minor) | C3 阻塞语义不一 | **closed** | 统一为「未裁 ⇒ 不开工, status 仍 `pending`, 不用 `blocked`」(TASK-037 notes + tasks.md #6) |
| `6698004d` | A1 (major) | C5 `version.yaml` 无人维护 | **closed** | yaml: TASK-033 / TASK-035 各加 `ab-suite/version.yaml` deliverable, verification 写程序化重算命令 (`ls *.json \| wc -l` + python 遍历 `len(evals)` 求和), 不写字面; `seam_rules` 加第 3 条「改 `ab-suite/*.json` 同批重算 `version.yaml`」; 035 加 033 边 (同文件) |
| `35dad35d` | A1 (major) | C5 `spec-drafter.json` eval id 无约定 / 「2 evals」陈旧 | **closed** | yaml: TASK-035 deliverable + verification 写「新 eval id = 当时 max(id)+1, ship 时读取不硬编码; 字段先 ship 取到 3, 母顺延」, 「不修改既有 eval 1/2」扩为「不修改任何既有 eval」; TASK-031/032/034 标题「2 evals」→「当时套件全部 eval (d69091d 时 2)」, TASK-033「13 evals」→「当前值 + 1」; `seam_rules` 第 3 条覆盖该文件; tasks.md 7.1-7.5 同步 |
| `05b5c605` | A1 (major) | C6 TASK-018 不相邻断言在字段未 ship 分支不可求值 | **closed** | yaml TASK-018 verification 改两分支: 字段 hunk 已 ship ⇒ 断言不相邻 + `git merge-tree` 干跑无冲突; 未 ship ⇒ 不断言, PR 说明记「由字段 TASK-014 对称分支在其 ship 时验」; `seam_rules` 第 2 条从断言式改为义务式; tasks.md Notes 接缝句同步 |
| `fead49d5` | A4 (major) | C10 SC 覆盖表 17 对不真 + SC-3 零命中 | **closed** | yaml verification 逐对补 `SC-NN` token: (SC-3) 004 首条前缀 + 011 「TASK-004 全绿 (SC-3)」; (SC-2/8/29) 014 「TASK-007 全绿 (SC-2 / SC-8 / SC-29)」; (SC-9/11/12/26) 017 新增文本义务落点一条; (SC-12) 018 新增命令行六字面一条; (SC-15) 006 首条前缀; (SC-21) 020 新增文本义务一条; (SC-22) 025 首条前缀; (SC-23) 019 新增文本半一条; (SC-26) 022 新增 config key 半一条; (SC-28) 033 v[1] 补第一臂; (SC-34) 026 首条前缀; 012 `SC-5/6/7` 展开为 `SC-5 / SC-6 / SC-7`。机械核验 (d) 51 对全部命中, (e) 现行 23 条 SC 全部有 verification 命中。flag 映射表 018 / 019 列的字面同批补进对应 verification |
| `b0e8b171` | A3 (minor) | C10 「12-hunk 表」无明细 | **closed** | 下方「rule6_note 12-hunk 明细表」 |
| `b0e8b171` | A4 (minor) | 锚点 `:1155-1158` → `:1154`; `:148` → `:149`; task_group 形态 | **closed** (前两项) / **不动** (task_group 形态, 主控裁「三份内部各自一致即可」) | yaml TASK-014 deliverable 注释 / TASK-003 与 TASK-019 branch-manager 注释 / tasks.md 5.3 + 行号复核表两行 |
| C11 (A5 `c8a425c2`) | A5 (major) | proposal 尾句陈旧 | **已闭合 (主控)** | proposal :798 由主控回改, 本席不动 proposal |

**方案与实况/Spec 的出入 (本席不自行偏离, 报主控)**:

1. 方案 C3 写 ab-results 占位形态为 `ab-results/<suite>/<vNEXT>-…`; 仓内既有惯例 (`2026-08-23-v1.67.0-linked-issue-rule6/`, 086ee32 前一版同款) 是 `ab-results/<date>-<ver>-<slug>-rule6/<suite>/`。本席只替换版本字面量为 `<vNEXT>`, 目录形态沿惯例; 若主控要改形态请另裁。
2. 方案 C1 只点名「第 2 组全部 RED 任务加 TASK-001 边」; 若不给第 6 组链首加 TASK-001, 第 5 组 TASK-019 / TASK-022 (只经 026/027 链与 TASK-003) 将不经传递到达 TASK-001 (A3 3221f943 点名的「Group 2~6 全部起点」缺口仍留两处)。本席按 bd55ab9c 处方 (a)「TASK-025~030 deps 与 Group 2 同款」给 TASK-025 加了 TASK-001; 机械核验 (c') 因此全绿。请主控确认此读法。
3. proposal 自身对 hunk 数不一致: `:511` rule6_note 写「实数 12 hunk / 9 文件」并列 12 行表, 但 Impact 表 `:683` 写「rule6_note 11-hunk 表」、闸门状态 `:754` 写「重算为 11 hunk / 9 文件」。tasks.md 沿 rule6_note 正文 12 行 (下表逐行对照 proposal `:513-525`); 不改 proposal, 留 owner。
4. 方案 C5 未提 `seam_rules`; A1 6698004d 处方 (c) 要求三份 metadata 各加一条 seam rule。本席在母 yaml `seam_rules` 加了第 3 条 (覆盖 `spec-drafter.json` eval id + `version.yaml` 重算); 字段 / 探针两份不在本席 scope, 请各自执笔席对齐。
5. 同文件核验 (a) 的排除规则: deliverable 注释含「只读」或路径以 `/` 结尾 (`docs/handoff/` 追加型宿主, TASK-001/002/036/039 共用) 不计为写入方; 为此把 TASK-002 三条存在性断言的注释补了「只读」字样。TASK-003 (锚点核对) 的 `phase1_gate.py` / `release_gate.py` 两条 deliverable 在 R2 由主控补「只读核验」标注 (其余锚点 deliverable 亦为只读核对); R3 起 TASK-003 不计为写入方 —— 本条原文「未标只读, 只更严不更松」已勘正 (R3/A4 64cf8dd9)。

### rule6_note 12-hunk 明细表 (proposal `:513-525` 逐行 → 落地 TASK)

| # | hunk (proposal 行) | 判据表落档 | 处置 | 写 hunk 的 TASK | 验/跑的 TASK |
|---|---|---|---|---|---|
| 1 | `phase-a-planner/SKILL.md:9` `allowed-tools` 加 `Bash, AskUserQuestion` | 第二行 (能力面, 照跑) | 照跑 `phase-a-planner.json` | TASK-017 | TASK-031 |
| 2 | `spec-drafter/SKILL.md:10` `allowed-tools` 加 `Bash` | 第二行 | 照跑 `spec-drafter.json` | TASK-018 | TASK-032 |
| 3 | `phase-a-planner/SKILL.md` 「前置: REQUIRE claim (A.1, MUST)」块 + A.1 项 `precondition:` 指针 | 第三行 (覆盖外) | 点名行为 (a)(b)(c)(e) 定向 fixture + 套件缺口 issue | TASK-017 | TASK-035 (fixture) · TASK-036 (issue) · 结构断言 TASK-025 |
| 4 | `spec-drafter/SKILL.md` 「前置: REQUIRE claim (A.1, MUST)」块 (第二落点) | 第三行 | 同上 (a)(b) 两条 | TASK-018 | TASK-035 · TASK-036 · TASK-025 |
| 5 | `state-scanner/SKILL.md` 新「Layer L A.1 heartbeat 集成」四句小节 | 第二行 | 照跑 `state-scanner.json` + 套件内加 1 eval (点名行为 (d)) | TASK-020 | TASK-033 |
| 6 | `config-loader/SKILL.md` 登记 `coordination` A.1 skip 语义 + `unattended` key | 第一行 (描述性, substitute) | substitute: `DEFAULTS.json` 三键 ↔ SKILL.md 逐字一致 (baseline 必红 + 负控) | TASK-022 | TASK-027 |
| 7 | `phase-b-developer/SKILL.md:92` 占位串口径 + `:96-97` push 注释勘正 + `skip_if` 补句 | 第二行 | 照跑 `phase-b-developer.json` | TASK-019 | TASK-034 · 结构断言 TASK-026 |
| 8 | `branch-manager/SKILL.md:149` 占位串口径 (标题 `:146` 不改) | 第二行 | 照跑 `branch-manager.json` | TASK-019 | TASK-034 · TASK-026 |
| 9 | `phase-d-closer/SKILL.md:51-52` 模板 + `:55` 说明句 carry-id 口径 | 第二行 | 照跑 `phase-d-closer.json` | TASK-019 | TASK-034 · TASK-026 |
| 10 | `references/layer-l-integration.md` (a) `:45` `update_heartbeat()` 勘正 (b) 新「Layer L A.1 heartbeat 集成」设计段 | (a) 第一行 / (b) 第二行 | (a) substitute「无 `update_heartbeat` 且含 `heartbeat(`」; (b) 与 #5 同一次照跑 + 结构断言「标题在且切片含 `--heartbeat-only`」 | TASK-021 | (a) TASK-028 · (b) TASK-033 + TASK-030 |
| 11 | `docs/coordination-ref-schema.md` §3.2 追加第 6 条 `unknown_schema_claims` | 第一行 | substitute「§3.2 切片含字面」(负控: 写进 §4.2 ⇒ 红) | TASK-023 | TASK-029 |
| 12 | `state-scanner/SKILL.md:168` 键集补 `push_skipped` / `push_skipped_reason` | 第一行 | substitute「`### JSON 消费` 切片含字面」(负控: 写进 `## 相关文档` ⇒ 红) | TASK-020 | TASK-030 |

计数核对: 照跑 6 套件 (#1/#2/#5/#7/#8/#9 → TASK-031~034) · 覆盖外 2 hunk (#3/#4 → TASK-035/036) · 描述性 substitute 4 处 (#6/#10a/#11/#12 → TASK-027/028/029/030) · #10b 处方性半归 #5 照跑 + TASK-030 结构断言。9 文件 = phase-a-planner / spec-drafter / state-scanner SKILL.md / config-loader SKILL.md / phase-b-developer / branch-manager / phase-d-closer / layer-l-integration.md / coordination-ref-schema.md。

### 机械核验 (R1 C1 / C10, 2026-08-30 亲跑, 主仓工作树 + aria d69091d)

脚本 (逐字内嵌于下, 唯一 SOT; 会话 scratch 副本不入仓):

```python
#!/usr/bin/env python3
"""post_planning R1 清账机械核验 (母 Spec a1-entry-claim-duplicate-work-guard).
(a) 同文件对全部有边 (直接或传递)  (b) 无环  (c) Group 6 不依赖 Group 5, Group 5 各含对应 Group 6 边
(d) tasks.md SC→TASK 覆盖表每对 (SC, TASK) ⇒ TASK.verification 含该 SC token
(e) proposal.md 现行 SC 集合每个至少一处 verification 命中 (撤销/迁出除外)
"""
import re, sys, yaml
from collections import defaultdict

ROOT = "/home/dev/Aria/openspec/changes/a1-entry-claim-duplicate-work-guard/"
raw = open(ROOT + "detailed-tasks.yaml", encoding="utf-8").read()
doc = yaml.safe_load(raw)
tasks = {t["id"]: t for t in doc["tasks"]}
deps = {tid: list(t.get("dependencies") or []) for tid, t in tasks.items()}
fails = []

# ---- 从原文抽 deliverables 路径 + 行尾注释 (safe_load 会丢注释) ----
deliv = defaultdict(list)  # tid -> [(path, comment)]
cur = None; in_deliv = False
for line in raw.splitlines():
    m = re.match(r"^  - id: (TASK-\d{3})", line)
    if m: cur = m.group(1); in_deliv = False; continue
    if cur and re.match(r"^    deliverables:", line): in_deliv = True; continue
    if cur and in_deliv:
        if re.match(r"^    \w", line): in_deliv = False; continue
        m = re.match(r"^      - (\S+)\s*(#.*)?$", line)
        if m: deliv[cur].append((m.group(1), m.group(2) or ""))

# ---- 传递闭包 ----
def ancestors(tid, seen=None):
    seen = seen if seen is not None else set()
    for d in deps[tid]:
        if d not in seen:
            seen.add(d); ancestors(d, seen)
    return seen
anc = {tid: ancestors(tid) for tid in tasks}

# (a) 同文件对: 排除 只读 deliverable 与目录 (以 / 结尾, 如 docs/handoff/ 追加型宿主)
writers = defaultdict(list)
for tid, items in deliv.items():
    for path, cmt in items:
        if "只读" in cmt or path.endswith("/"): continue
        writers[path].append(tid)
pairs_checked = 0
for path, ws in sorted(writers.items()):
    if len(ws) < 2: continue
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            a, b = ws[i], ws[j]; pairs_checked += 1
            if not (a in anc[b] or b in anc[a]):
                fails.append(f"(a) 同文件无边: {path}: {a} <-> {b}")
print(f"[a] 同文件写入对 {pairs_checked} 对 (共写文件 {sum(1 for w in writers.values() if len(w)>1)} 个) — 全部有边: {not any(f.startswith('(a)') for f in fails)}")
for path, ws in sorted(writers.items()):
    if len(ws) > 1: print(f"      {path}: {' -> '.join(sorted(ws, key=lambda w: len(anc[w] & set(ws))))}")  # 依赖序 (R4/A1 9db42f0a: 原按文件序, 块移位后与依赖方向相反)

# (b) 无环 + 悬空
dangling = [(t, d) for t in tasks for d in deps[t] if d not in tasks]
if dangling: fails.append(f"(b) 悬空依赖: {dangling}")
WHITE, GRAY, BLACK = 0, 1, 2
color = {t: WHITE for t in tasks}
def dfs(u, stack):
    color[u] = GRAY; stack.append(u)
    for v in deps[u]:
        if v not in tasks: continue
        if color[v] == GRAY: fails.append(f"(b) 环: {' -> '.join(stack + [v])}")
        elif color[v] == WHITE: dfs(v, stack)
    stack.pop(); color[u] = BLACK
for t in tasks:
    if color[t] == WHITE: dfs(t, [])
print(f"[b] 无环: {not any(f.startswith('(b)') for f in fails)}; 悬空: {dangling}")

# (c) Group 6 不依赖 Group 5; Group 5 各含对应 Group 6 边
g5 = [t for t in tasks if tasks[t]["task_group"] == 5]
g6 = [t for t in tasks if tasks[t]["task_group"] == 6]
for t in g6:
    bad = [d for d in anc[t] if d in g5]
    if bad: fails.append(f"(c) Group 6 任务 {t} (传递) 依赖 Group 5: {bad}")
expect = {"TASK-017": ["TASK-025"], "TASK-018": ["TASK-025"], "TASK-019": ["TASK-026"],
          "TASK-020": ["TASK-030"], "TASK-021": ["TASK-028", "TASK-030"],
          "TASK-022": ["TASK-027"], "TASK-023": ["TASK-029"]}
for t, reds in expect.items():
    for r in reds:
        if r not in deps[t]: fails.append(f"(c) {t} 缺直接边 -> {r}")
g1 = {"TASK-001", "TASK-003"}
print(f"[c] Group 6 = {g6}; 无一 (传递) 依赖 Group 5: {not any('Group 6' in f for f in fails)}; "
      f"Group 5 各含对应 RED 直接边: {not any('缺直接边' in f for f in fails)}; "
      f"Group 6 祖先集 ⊆ {{TASK-001,TASK-003}} ∪ Group 6: {all(anc[t] <= g1 | set(g6) for t in g6)}")

# 前置门可达性 (R1/A3 3221f943): 除 TASK-001/002/003/039 外全部 (传递) 依赖 TASK-001 与 TASK-003
exempt = {"TASK-001", "TASK-002", "TASK-003", "TASK-039"}
miss1 = [t for t in tasks if t not in exempt and "TASK-001" not in anc[t]]
miss3 = [t for t in tasks if t not in exempt and "TASK-003" not in anc[t]]
print(f"[c'] 不经传递到达 TASK-001 的任务 (豁免 {sorted(exempt)}): {miss1}; 不到达 TASK-003: {miss3}")

# (d) 覆盖表
md = open(ROOT + "tasks.md", encoding="utf-8").read()
sec = md.split("## SC → TASK 覆盖表")[1].split("## Impact 行")[0]
def has_token(text, n): return re.search(rf"SC-{n}(?!\d)", text) is not None
def ver_text(tid): return "\n".join(tasks[tid].get("verification") or [])
pairs, bad = [], []
for row in sec.splitlines():
    if not row.startswith("| SC-"): continue
    cells = [c.strip() for c in row.strip("|").split("|")]
    scs = re.findall(r"SC-(\d+)", cells[0])
    ts = []  # 展开 `TASK-013/014` 缩写 (R2/A4 minor 9db42f0a)
    for m in re.finditer(r"TASK-(\d{3})((?:/\d{3})*)", cells[3]):
        ts.append(f"TASK-{m.group(1)}"); ts += [f"TASK-{x}" for x in m.group(2).split("/") if x]
    for n in scs:
        for t in ts:
            pairs.append((f"SC-{n}", t))
            if not has_token(ver_text(t), n): bad.append((f"SC-{n}", t))
for p in bad: fails.append(f"(d) 覆盖表对 {p} 在 verification 无该 token")
print(f"[d] 覆盖表 (SC, TASK) 对 {len(pairs)}; verification 无 token 的对: {bad}")

# (e) proposal 现行 SC 集合
prop = open(ROOT + "proposal.md", encoding="utf-8").read()
all_sc = sorted({int(n) for n in re.findall(r"SC-(\d+)", prop)})
excluded = {1, 4, 20, 27, 30, 31, 13, 16, 17, 18, 19}  # 撤销 1/4/20/27/30/31; 迁出 13/16/17/18/19(a)(c); 19(b) 由 SC-29 承担
allver = "\n".join(ver_text(t) for t in tasks)
missing = [n for n in all_sc if n not in excluded and not has_token(allver, n)]
if missing: fails.append(f"(e) 现行 SC 无 verification 命中: {missing}")
print(f"[e] proposal SC 集合 {all_sc[0]}..{all_sc[-1]} 共 {len(all_sc)}; 排除 {sorted(excluded)}; 现行 {len(all_sc)-len(excluded)} 条无命中: {missing}")

# 附: parent 1:1 与 tasks.md 编号
md_ids = set(re.findall(r"^- \[ \] (\d+\.\d+) ", md, re.M))
parents = [t["parent"] for t in tasks.values()]
print(f"[+] total_tasks={len(tasks)} (metadata {doc['metadata']['total_tasks']}); parent 唯一={len(set(parents))==len(parents)}; parent ⊆ tasks.md 编号={set(parents)<=md_ids}; 编号数={len(md_ids)}")
print("RESULT:", "PASS" if not fails else "FAIL"); [print("   ", f) for f in fails]
sys.exit(1 if fails else 0)
```

输出 (逐字, exit 0; R4 收敛后重跑 2026-08-31, 同文件链改按依赖序打印):

```text
[a] 同文件写入对 38 对 (共写文件 20 个) — 全部有边: True
      aria: TASK-040 -> TASK-038
      aria-plugin-benchmarks/ab-suite/version.yaml: TASK-033 -> TASK-035
      aria/skills/branch-manager/SKILL.md: TASK-003 -> TASK-019
      aria/skills/config-loader/SKILL.md: TASK-003 -> TASK-022
      aria/skills/phase-a-planner/SKILL.md: TASK-003 -> TASK-017
      aria/skills/phase-b-developer/SKILL.md: TASK-003 -> TASK-019
      aria/skills/phase-d-closer/SKILL.md: TASK-003 -> TASK-019
      aria/skills/spec-drafter/SKILL.md: TASK-003 -> TASK-018
      aria/skills/state-scanner/SKILL.md: TASK-003 -> TASK-020
      aria/skills/state-scanner/docs/coordination-ref-schema.md: TASK-003 -> TASK-023
      aria/skills/state-scanner/lib/claim_lifecycle.py: TASK-003 -> TASK-012
      aria/skills/state-scanner/lib/collision.py: TASK-003 -> TASK-013
      aria/skills/state-scanner/lib/constants.py: TASK-003 -> TASK-020
      aria/skills/state-scanner/lib/identity.py: TASK-003 -> TASK-011
      aria/skills/state-scanner/references/layer-l-integration.md: TASK-003 -> TASK-021
      aria/skills/state-scanner/scripts/phase1_gate.py: TASK-014 -> TASK-015 -> TASK-016
      aria/skills/state-scanner/tests/test_a1_entry_gate_cli.py: TASK-007 -> TASK-008 -> TASK-009
      aria/skills/state-scanner/tests/test_coordination_default_lockin.py: TASK-025 -> TASK-026 -> TASK-027 -> TASK-028 -> TASK-029 -> TASK-030
      aria/skills/state-scanner/tests/test_heartbeat_by_track.py: TASK-005 -> TASK-006
      standards/conventions/session-handoff.md: TASK-003 -> TASK-024
[b] 无环: True; 悬空: []
[c] Group 6 = ['TASK-025', 'TASK-026', 'TASK-027', 'TASK-028', 'TASK-029', 'TASK-030']; 无一 (传递) 依赖 Group 5: True; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: True
[c'] 不经传递到达 TASK-001 的任务 (豁免 ['TASK-001', 'TASK-002', 'TASK-003', 'TASK-039']): []; 不到达 TASK-003: []
[d] 覆盖表 (SC, TASK) 对 55; verification 无 token 的对: []
[e] proposal SC 集合 1..34 共 34; 排除 [1, 4, 13, 16, 17, 18, 19, 20, 27, 30, 31]; 现行 23 条无命中: []
[+] total_tasks=40 (metadata 40); parent 唯一=True; parent ⊆ tasks.md 编号=True; 编号数=40
RESULT: PASS
```

解析器: PyYAML `safe_load` 通过; `aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` ⇒ `parse_ok=True`, 40 tasks, status 集合 `{pending}`。残留字面量: 两文件 `grep '1\.68\.0\|README.zh-CN\|\.gitmodules'` 只剩本对账段与 TASK-038 notes 里的「已改」留痕。

**可证伪性 (memory check-runs-at-baseline-first / adversarial-fixture)**: 两份文件 R1 前版本未入 git (untracked), 无法对基线复跑; 改在 scratch 副本上故意回退三处 (TASK-016 删 TASK-015 边 / TASK-025 重新依赖 TASK-017 / TASK-004 抹掉 `SC-3` token) 复跑同一脚本, 输出 (逐字, exit 1):

```text
[a] 同文件写入对 40 对 (共写文件 19 个) — 全部有边: False
[b] 无环: False; 悬空: []
[c] Group 6 = [...]; 无一 (传递) 依赖 Group 5: False; Group 5 各含对应 RED 直接边: True; Group 6 祖先集 ⊆ {TASK-001,TASK-003} ∪ Group 6: False
[d] 覆盖表 (SC, TASK) 对 51; verification 无 token 的对: [('SC-3', 'TASK-004')]
RESULT: FAIL
    (a) 同文件无边: aria/skills/state-scanner/scripts/phase1_gate.py: TASK-015 <-> TASK-016
    (b) 环: TASK-017 -> TASK-022 -> TASK-027 -> TASK-026 -> TASK-025 -> TASK-017
    (c) Group 6 任务 TASK-025 (传递) 依赖 Group 5: ['TASK-017', 'TASK-022']   (026~030 同, 略)
    (d) 覆盖表对 ('SC-3', 'TASK-004') 在 verification 无该 token
```

三处破坏分别被 (a) / (b)+(c) / (d) 抓到, 脚本非恒绿。(b) 环是翻转后的新性质: 第 5 组依赖第 6 组之后, 第 6 组任何一条回指第 5 组的边都成环 — 倒置不再是「静默可执行」而是结构性报错。
