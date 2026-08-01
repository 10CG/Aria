# session-closer autofill yaml datasource (aria-plugin #121)

> **Level**: Minimal (Level 2 Spec)
> **Status**: ✅ **Approved** (owner sign-off 2026-08-01; post_spec R1→R3 CONVERGED, R3 5/5 PASS 零 Critical/Major 残留)
> **Created**: 2026-08-01
> **Issue**: [aria-plugin #121](https://forgejo.10cg.pub/10CG/aria-plugin/issues/121) (triage confirmed, repro 2/2, severity major — [issuecomment-17136](https://forgejo.10cg.pub/10CG/aria-plugin/issues/121#issuecomment-17136))
> **根因谱系**: aria-plugin #113 `state-scanner-gate-yaml-datasource` (已归档 `openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/`) 的同根因**第四处消费方**

## Why

`skills/session-closer/scripts/handoff_autofill.py::grep_unchecked_tasks` (L160-175) 只拼 `tasks.md` 路径。对只有 `detailed-tasks.yaml` 的 spec (task-planner path B 产出, 常见 L2), §2 carry-forward 汇编报 **0 未完成** — 静默假绿, 直接误导下一 session 的 carry-forward 判断。triage 隔离 fixture 实测: yaml-only spec 实际 2 pending → 报 0; 对照组 tasks.md 正常 2/2。

#113 已修同病根三处 (`gate_result` / `is_spec_complete` / `collectors/openspec.py` carry_forward), 本处是跨 skill (state-scanner → session-closer) 的第四处, 在 #113 Impact 分析之外。

**范围界定 (R1 tech-lead M-2)**: 本 spec 修 yaml-only 形态, **不是**该函数盲区的全量收口 — 还存在第三形态「Level 2 任务内联 `proposal.md`」(proposal-only spec 的 `- [ ]` 同样报 0, 本 spec 自身即实例)。该形态数据源语义不同 (proposal 内 `- [ ]` 混含 Success Criteria 复选框, 直扫会把 SC 项灌进 carry-forward, 需独立语义设计), 不搭本车 — ship 时开 follow-up issue (Tasks 1.4)。

## What

`grep_unchecked_tasks` 增加 yaml fallback 分支, 复用 #113 parser SOT, **不第二次实现 yaml 解析**:

1. **取数语义镜像 #113 决策 6 (fallback-only, 防双报)**: 逐 spec 目录 — `tasks.md` 存在 (`isfile`, 现判据不动) ⇒ 现行为不变, yaml **不看** (陈旧 A.3 期 yaml 不得双计); 否则走 yaml 分支。**yaml 侧「存在性判断」= 尝试打开, 不设 `isfile()` 前置闸门** (R2 qa M-3 + tech-lead m-2 独立互证: `isfile()` 对目录等异常形态返回 False, 会把「文件在场但不可读」静默送进「双缺席」分支报 0 — 以新机制复刻病根): 直接 `open(..., encoding="utf-8", errors="replace")` (**`errors="replace"` 必带** — `UnicodeDecodeError` 非 `OSError` 子类, 裸 open 会让它逃出三形态闭包; 照抄本函数 L169 tasks.md 分支既有先例; R3 backend+tech-lead 收敛点) — `FileNotFoundError`/`NotADirectoryError` ⇒ 视为 yaml 缺席, 零条目无 sentinel (断链 symlink 归此类: 指向物不存在, 语义上等同无文件, **刻意不入 sentinel**, R3 tech-lead 措辞勘正); 其它 `OSError` (`IsADirectoryError`/`PermissionError`/symlink 循环等) ⇒ 形态 (b) sentinel。
2. **yaml 分支 (happy path)**: `parse_detailed_tasks(text)` 返回**包装 dict `{parse_ok, tasks, reason}`** (非裸 task 列表 — R1 四方命中点)。仅当 `parse_ok=True` 时遍历 `tasks` (逐项 `{id, raw_status, title}`); **fail-CLOSED 残留判据** = `not is_done_status(raw_status)` (done-family 仅 {done, completed}; pending/deferred/blocked/in_progress/unknown/None 全算未完成 — 与 SOT 白名单同源, 不另写字面量)。输出 `{"source": f"detailed-tasks.yaml:{name}", "item": ...}`, item 拼接 = `id if not title else f"{id} {title}"` (**title 空时不产尾随空格**, R1 三方 minor)。下游 `assemble_unfinished` (L223-238) 把 source 当自由显示串, 新前缀零改动兼容。
3. **不可用三形态统一 sentinel 通道 (R1 主收敛点, 决策 4 泛化)**: 以下任一形态**都不得静默回 0**, 每个命中的 yaml-only spec 产一条 sentinel item:
   - (a) 跨 skill SOT 加载失败 (skill 目录被复制到隔离路径等);
   - (b) yaml 读取 OSError — 除「视为缺席」的两个异常类外 (见第 1 点; **不得**照抄 tasks.md 分支的静默 `continue`, R1 qa M-1);
   - (c) `parse_ok=False` (parser 三条代码分支覆盖的四种输入形态: 无 `tasks:`/重复 `tasks:`/零 `- id:`/结构自不一致 — `tasks` 恒 `[]`, 与真 0 条**返回形态不可区分**, 必须显式分诊; 措辞按 R2 backend m-2 勘正)。
   **sentinel 稳定判别位 (R2 tech-lead m-4 + backend m-1)**: `source = f"detailed-tasks.yaml:{name}:unavailable"` (机器可判别后缀), `item = f"(unavailable: {kind} — {reason}) 需人工核对"`, `kind` ∈ {`sot_load_failed`, `read_failed`, `parse_failed`}, reason 为 helper 异常串或 `parsed["reason"]` 透传。SC 断言锚定 source 后缀与 kind, 不断自由文本。
   先例: 姊妹消费方 `spec_complete.py::_yaml_only_tasks_verdict` L204-212 已把 OSError 与 `parse_ok=False` 当独立态处置 (#113 血缘内已验证必要), 本 spec 把同一纪律带到 session-closer 侧。哲学同本文件 `_BENIGN_IMPORT_FAILED`: 宁噪音勿假绿。
4. **跨 skill SOT 加载机制 (R2 tech-lead m-1 升级裁定: 弃 sys.path, 改 importlib 直载)**:
   - R1 版方案 (插 `scripts/lib` 进 sys.path + 裸模块导入) 在 R2 被证仍有残余顺序风险: `collectors/__init__` 链会无条件带出 `handoff_multibranch.py:92-100` 的带守卫插入, root 已在 path 且排序靠前时顶层 `lib` 绑错并连带废掉 `owner_container()` — 「加注释」兜不住顺序不变量。
   - **裁定方案**: `importlib.util.spec_from_file_location("aria_sc_detailed_tasks", <path>)` **按文件直载**, 唯一模块名注册 — **零 sys.path 变更**, 双 `lib` 包名碰撞 (权威论证 `collectors/openspec.py:18-31`) 与插入顺序问题**结构性消失**, 本文件 sys.path 插入点维持既有两处不新增 (R1 backend m-2 的顺序注释要求随之降为对既有两处的现状记录)。
   - 可行性前提 (已核): `detailed_tasks.py` 仅 import stdlib `re`, 零包内相对导入 — 文件直载无依赖缺口; `scripts/lib/__init__.py` 为 0 字节, 不载也无副作用。
   - SOT 路径定位沿用本文件既有跨 skill 先例 (`_benign_unconditional_reasons` L46-50 / `owner_container` L317-321 的 `Path(__file__).resolve().parents[2]` 兄弟 skill 模式); `spec_complete.py` L350-356 / L441-451 是同目录 CLI bootstrap 场景先例 (该块导三符号, 本 spec 用其中 `parse_detailed_tasks` / `is_done_status` 两个), 仅作 SOT 复用谱系引用, 不作机制先例 (R1 knowledge m-3 / R2 code-reviewer minor 归因收紧)。
5. **加载时机与可测缝**: 收拢为 helper `_load_detailed_tasks_api(sot_path=None)` — 惰性调用 (仅 yaml fallback 命中时), 成功返回 `(parse_fn, done_fn)`, 任何异常返回 `None`; `sot_path=None` 时用 parents[2] 计算真实路径。测试两层 (R2 qa m-4 加固): (a) 消费方降级 — monkeypatch helper 返回 `None`, 断言 sentinel (绕开 `sys.modules` 缓存维度, R1 qa M-2; importlib 直载下模块以唯一名注册, 亦不污染裸名空间); (b) helper 自身 — 传入不存在的 `sot_path` 直测返回 `None` (端到端验证失败路径真实可达, 对齐 `_benign_unconditional_reasons` 的验证强度)。

### Key Deliverables

- `aria/skills/session-closer/scripts/handoff_autofill.py` — `grep_unchecked_tasks` yaml fallback 分支 + `_load_detailed_tasks_api` helper (唯一生产代码变更)
- `aria/skills/session-closer/tests/test_handoff_autofill.py` — SC-1~SC-9 结构化测试 (rule6_note substitute)

## 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 解析器 | 复用 `state-scanner/scripts/lib/detailed_tasks.py` | #113 parser SOT (range-bounded + indent-anchored + fail-CLOSED), 不双写 |
| 并存优先级 | tasks.md 在场 ⇒ yaml 不看 | 镜像 #113 决策 6, 双层输出 byte-identical, 防双计 |
| SOT 加载 | `importlib.util.spec_from_file_location` 文件直载, 唯一模块名 | 零 sys.path 变更 ⇒ 双 `lib` 名碰撞与插入顺序问题结构性消失 (R2 tech-lead m-1 裁定; R1 sys.path 方案被证残余顺序风险) |
| 不可用处置 | 导入失败/OSError/`parse_ok=False` 三形态统一 sentinel | 假绿是本 issue 病根, 降级不可复刻病根; 姊妹消费方 L204-212 先例 |
| 残留判据 | `not is_done_status(...)` | fail-CLOSED 白名单与 SOT 同源, 不另写 done 字面量 |
| 否决: snapshot 加字段路线 | 不改 state-scanner collector/schema | 更"简"仅表面: 需 snapshot schema additive bump + 两 skill 发版耦合; autofill 直扫 changes_dir 是既有拓扑 (AD-2 backstop 定位), 本修复零 state-scanner 改动 (R1 tech-lead 核实后同意否决, 此行补记录) |
| 范围 | 仅 yaml-only 形态 | proposal-inline 第三形态语义不同 (SC 复选框混入), 独立 follow-up issue (Tasks 1.4) |

## Impact

- 影响面: session-closer 单 skill 单函数 + helper + 其测试; state-scanner 侧零改动 (只读复用)。
- 版本: bug 修复 = PATCH → aria-plugin v1.65.1。
- 兼容: 输出 schema 不变 (`[{source, item}]`), source 新前缀为纯显示串; 无 breaking change。
- ship 同步面: aria 子模块 5 文件 + 主仓 gitlink + VERSION + README badge (i18n 正文无实质变更, #140 B 档免重译)。
- issue 收尾: ship 后 #121 发 close comment + PATCH state (两步分开, per convention); 同时开 proposal-inline 形态 follow-up issue。

## rule6_note

`handoff_autofill.py` 是 deterministic 机械脚本 (非 prose 指令面), 行为由代码而非 SKILL.md 措辞决定, AB 套件对此不适用 → **substitute: SC 级 baseline-failing 结构化测试** (SC-1/SC-7 必须在未修代码上 FAIL、修后 PASS, 防真空绿)。SKILL.md / description 零变动, 无照跑面。

## Tasks

- [x] 1.1 `grep_unchecked_tasks` yaml fallback 分支 (open-attempt 存在性语义) + `_load_detailed_tasks_api` importlib 直载 helper + 三形态 sentinel (稳定判别位) — aria-plugin `1180d08`
- [x] 1.2 SC-1~SC-9 测试 (先写 SC-1/SC-7 验证 baseline FAIL — 已验 4 FAIL + 2 error → 全绿) — 同 commit
- [x] 1.3 双侧回归 (session-closer 50 OK + state-scanner 1322 OK) + 真数据 dogfood 零噪音 + Rule #6 substitute 留痕 (本文件 rule6_note)
- [x] 1.4 follow-up issue 已开: [aria-plugin #123](https://forgejo.10cg.pub/10CG/aria-plugin/issues/123) (proposal-inline 第三形态)

## Success Criteria

- [ ] SC-1 (baseline-failing): yaml-only fixture (含 1 个 title 正常 + 1 个 title 缺失 task, 全 pending, 无 tasks.md) → 报 2 条, source=`detailed-tasks.yaml:{name}`; title 缺失项 item == task id (无尾随空格); 该测试在未修代码上必须 FAIL (报 0), 修后 PASS。须走 helper **默认路径** (真实仓布局解析 SOT), 兼作 lib 迁移红灯 (见 SC-6)
- [ ] SC-2 (precedence): 同 spec 目录 tasks.md + detailed-tasks.yaml 并存 → 仅出 tasks.md 条目, yaml 条目零出现
- [ ] SC-3 (done-family 不误报): yaml 全 `status: done` / `completed` → 0 条
- [ ] SC-4 (fail-CLOSED, 混合态): 同一 yaml 内 done + {deferred, blocked, in_progress, unknown-token, status 缺失} 混排 → 仅非 done-family 计入残留, 逐态断言
- [ ] SC-5 (降级可见, 双层): (a) monkeypatch `_load_detailed_tasks_api` 返回 None → yaml-only spec 产 `sot_load_failed` sentinel, 非静默 0 (不得依赖 sys.path 操纵 — import 缓存维度); (b) helper 直测 — 传不存在 `sot_path` → 返回 None (失败路径端到端可达, R2 qa m-4)
- [ ] SC-6 (回归面): session-closer 全测试绿 + state-scanner 全测试绿 (纯回归纪律)。lib 迁移红灯不靠此: SC-1 在真实仓布局下经 helper 默认路径实算 SOT 解析 — state-scanner 侧 `scripts/lib/detailed_tasks.py` 挪位时 SC-1 即红 (R2 tech-lead m-3 勘正, 替代 R1 版不成立的「基线留存」论证)
- [ ] SC-7 (baseline-failing, parse_ok=False): 畸形 yaml fixture (零 `- id:` 条目; 另一 fixture 重复 `tasks:` 键) → `parse_failed` sentinel 且 `parsed["reason"]` 透传进 item, source 后缀 `:unavailable`, 非静默 0; 未修代码上 FAIL
- [ ] SC-8 (读取异常): `detailed-tasks.yaml` 为目录 → open-attempt 语义下必触发 `IsADirectoryError` → `read_failed` sentinel, 非静默落双缺席 (R2 qa M-3 裁定后 fixture 与语义自洽)
- [ ] SC-9 (双缺席): spec 目录 tasks.md 与 yaml 都缺 → 0 条且无 sentinel; 追加子 case: yaml 为断链 symlink → `FileNotFoundError` 归入缺席同样 0 条无 sentinel (open-attempt 语义边界锁定)
- [ ] fixture 全部用独立 tempdir (不依赖 repo 布局, memory `feedback_test_worktree_fixture_isolated_tmpdir`)
