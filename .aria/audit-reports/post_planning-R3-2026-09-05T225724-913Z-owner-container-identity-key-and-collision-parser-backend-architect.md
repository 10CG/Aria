---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T22:57:24.913Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — backend-architect 席位报告

被审对象: `openspec/changes/owner-container-identity-key-and-collision-parser/{tasks.md, detailed-tasks.yaml}` v3 (commit `c27826e`, post_planning R2 rework 后, 39 TASK) 对照 `proposal.md` v9。镜头: TASK-020 独立数据路径可实现性 / `metadata.test_runner` 双跑法实跑 / TASK-042+TASK-038 依赖可执行性 / TASK-034 新依赖无环。

实读环境: 主仓工作树当前 HEAD, `git status` clean。全部行号/命令实读实跑, 无引用未跑证据。

## R2 处置核对

| R2 处置项 | 本轮复核 | 三态 |
|---|---|---|
| PP2-C1 (Critical): `run_tests.py` unittest discover 对 `test_collision.py` 裸函数 `countTestCases()==0` → 接受处置「两种跑法都必跑」, `metadata.test_runner` 写入 (a) `run_tests.py` (b) `/home/dev/.local/bin/pytest -q -p no:cacheprovider aria/skills/state-scanner/tests` | 实跑 (a): `Ran 1476 tests ... OK`, 与 v3 claim 一致。实跑 (b) 逐字命令: `Interrupted: 12 errors during collection`, **0 个测试执行** (pytest 默认遇 collection error 即中止, 不带 `--continue-on-collection-errors` 不会往下跑); 加该 flag 后仍有 26 个真失败 (非 collection error) + 12 个模块仍 0 收集 + 环境缺依赖导致假红 (细节见镜头 2) | **not_resolved** — 声称的"双跑法" (b) 侧在本容器实测完全跑不起来, 不是"结果差 16"式的部分问题 |
| M5: TASK-020 改独立数据路径 (顶层 `render_track_board` 于 dedupe `:744` 前调 `identity_drift_advisories`, 输出为 `:796` collision 段之后独立段) | 实读 `track_board.py:583-808`, deps 已去掉 TASK-016 | **resolved** (本轮镜头 1 逐条核验) |
| M1: TASK-042 新增 S1 手动 tracker 承载体 | 实读 TASK-042 (`:626-641`) 及其与 TASK-038/039/040/000 的依赖边 | **resolved** (本轮镜头 3 核验) |
| M2: 组 0 (TASK-000/040) 接入 TASK-034 (merge) 传递闭包前置 | 实读 `dependencies` 字段 | **resolved** (本轮镜头 3 核验) |

三态计数: **resolved 3 / not_resolved 1 / partially 0**。

## 审计结论

### 镜头 1 — TASK-020 独立数据路径可实现性

实读 `aria/skills/state-scanner/scripts/renderers/track_board.py`:

- `:110` `tracks: list[dict] = tmb.get("tracks") or []` — 原始 (未 dedupe) tracks 在 `render_track_board` 顶层作用域整函数生命周期内可得。
- `:744` `_dedupe_tracks_for_collision(tracks)[0]` — dedupe 调用点, TASK-020 要求在此之前对原始 `tracks` 调 `identity_drift_advisories`。`tracks` 变量在 `:110`→`:744` 之间未被重新赋值 (仅 `:122` 起的 `for track in tracks:` 循环只读遍历), 插入点结构上可行。
- `:796` `collision_lines = _render_collision_lines(verdicts, tracks_by_tid)` 为 collision 段渲染点; `:805-806` `for cl in collision_lines: lines.append(cl)`; `:808` `return "\n".join(lines)`。TASK-020 描述的"独立段"应落在 `:806` 之后、`:808` 之前 (即 collision 段渲染完、`return` 前), 结构上有明确空隙可插入, 不与 P1/P2 (`_detect_collisions`/`reconcile_all`) 两条 collision 渲染路径 (`:783-802`) 交叉或互相依赖。
- 与 TASK-016 (族键剥离, 只作用于 `track_to_claim_record`/`tracks_by_tid`) 互不依赖成立: `identity_drift_advisories` 按 D3 定义直接消费 collector 原始 `tracks` 字典 (`owner_container` 字段), 不经过 `ClaimRecord`/`track_to_claim_record` 转换, 与 TASK-016 的族键剥离逻辑无共享代码路径; TASK-020 `dependencies: [TASK-014, TASK-009]` 已不含 TASK-016, 与此结论一致。

TASK-009 反事实夹具 (对 dedupe 后行算 → 0) 可构造性核验: dedupe 键 (D1/TASK-015) = `(track_id, identity_key)`, 折叠同 `identity_key` 的多行为按 `updated_at` 最新一行; `identity_drift_advisories` 的判据是"同一 `identity_key` 出现 ≥2 个非空非 `unknown` owner 串"。构造 fixture: 同 track_id、同 uuid `identity_key`、两行不同 `owner` 段 (漂移场景, 如 proposal §Why 第 2 层 `bfe8285d` 案例) + 不同 `updated_at`；对原始 tracks 调用 → 命中 (2 个 owner); 对 dedupe 后 tracks 调用 → 只剩 1 行 (最新 owner) → owner 集合大小 1 → 不命中 → 0 条。逻辑自洽, 反事实可真实构造, 非空谈。

**镜头 1 结论: 无 Critical/Major。**

### 镜头 2 — `metadata.test_runner` 双跑法实跑核验 (Critical)

按审计任务书逐字实跑 v3 `metadata.test_runner` (`detailed-tasks.yaml:32`) 指定的两条命令, 工作目录 `/home/dev/Aria` (仓根, 与容器内 B.2 执行环境一致):

**(a) `python3 aria/skills/state-scanner/tests/run_tests.py`**: `Ran 1476 tests in 397.403s` / `OK`。与 v3 claim 一致。

**(b) `/home/dev/.local/bin/pytest -q -p no:cacheprovider aria/skills/state-scanner/tests`** (逐字, 未加任何额外 flag): 输出 `=========================== short test summary info ============================` / 十二行 `ERROR test_architecture.py` 等 / `!!!!!!!!!!!!!!!!!!! Interrupted: 12 errors during collection !!!!!!!!!!!!!!!!!!!` / `12 errors in 4.80s`。**pytest 默认遇 collection error 即整体中止, 0 个测试被执行** —— 不是"漏 16 个", 而是**这条命令本身一个测试都不跑**, `test_collision.py` (TASK-032 双跑法要保护的目标文件) 在此调用形态下从未被执行。

**根因** (实读确认): `aria/skills/state-scanner/tests/__init__.py` 存在 (`ls` 确认), 使 `tests/` 成为 Python package; pytest 默认 "prepend" import mode 下, 含 `__init__.py` 的测试目录会把**包的顶层父目录** (`state-scanner/`) 插入 `sys.path[0]`, 而非 `tests/` 自身。12 个模块 (`test_architecture.py` / `test_audit.py` / `test_changes.py` / `test_custom_checks.py` / `test_detailed_tasks.py` / `test_forgejo_config.py` / `test_gate_yaml_datasource.py` / `test_gate_yaml_golden_corpus.py` / `test_gate_yaml_only_source.py` / `test_gate_yaml_probe_reach.py` / `test_git.py` / `test_git_operation_detection.py`) 内部用**绝对导入** `from _helpers import ...` (`_helpers.py` 是 `tests/` 内的同级模块), 在该 sys.path 布局下解析为 `ModuleNotFoundError: No module named '_helpers'` (需写成 `from tests._helpers import ...` 或靠 conftest.py 补 `tests/` 自身进 sys.path, 两者本仓均无)。`cd aria/skills/state-scanner/tests && pytest .` 复测同样失败 (package 语义与 cwd 无关)。全仓无 `conftest.py` / `pytest.ini` / `pyproject.toml` / `setup.cfg` (`find` 确认), 无任何兜底配置。

加 `--continue-on-collection-errors` 后 (仍非 metadata.test_runner 逐字命令, 属推断修补): `26 failed, 1256 passed, 1 skipped, 12 errors, 160 subtests passed in 132.25s` —— 上述 12 模块仍 0 收集 (grep 确认这 12 文件共 209 个 `def test_` 函数, 全部缺席); 另 26 个**真实失败** (`test_release_by_track.py` 18 个 + `test_coordination_no_push.py` 8 个), 抽样 1 例 (`test_release_from_fresh_session`) 报错原文 `WARNING lib.claim_lifecycle: write_claim failed: error=yaml_unavailable`。核实: `/home/dev/.local/bin/pytest` 是 `uv tool install` 的隔离虚拟环境 (`/home/dev/.local/share/uv/tools/pytest/bin/python`), 该环境 `import yaml` 报 `ModuleNotFoundError: No module named 'yaml'`; 而 `run_tests.py` 用的系统 `python3` 有 `PyYAML` (`/usr/lib/python3/dist-packages/yaml/__init__.py`)。**两条命令跑在两个依赖集不同的 Python 解释器上**, pytest 侧缺 PyYAML 导致大量与代码正确性无关的假红。

**"≥1492" 数字来源核实**: `grep -rhoE "^\s*def test_[a-zA-Z0-9_]*" aria/skills/state-scanner/tests/*.py | wc -l` = **1492**, 与 v3 记录的 "def test_ 1492" 精确吻合 —— 证实该数字是**静态 grep 计数**, 不是任何一次实际 pytest 收集/执行的输出行。metadata.test_runner 据此写下的 "pytest 全套零失败 且收集数 ≥ 1492" (TASK-032 verification (b)) 目标, 在本容器当前工具链下**结构性不可达**: 即便 TASK-012..020 全部正确实现, 12 个模块的收集失败 (与本 Spec 代码改动无关的既有绝对导入问题) 与 PyYAML 缺失导致的假红 (同样与代码无关) 都会持续拉低收集数/推高失败数, 使 SC-7(b) 永远判红。

**结论**: post_planning R2 接受的 "两跑法都必跑" 处置, 是本轮 R2→R3 rework 对 PP2-C1 的**唯一**修复手段; 但该修复措施本身**从未被实际执行验证过** (数字来自静态 grep, 命令未曾逐字跑过), 实测该命令逐字执行 0 测试运行、加 flag 后仍有 209 个测试缺席 + 26 个环境性假红。这不是可以在 B 期顺手补的记录型 minor —— TASK-031 (RED→GREEN 记录汇总) 与 TASK-032 (全套回归) 两个组 4 收尾任务的验收判据 (SC-7(b)) 当前**不可满足**, 会在 B.2 落地阶段直接卡死, 且卡死原因与本 Spec 的业务代码 (collision/identity/track_board) 完全无关, 纯粹是任务书写的验证命令本身跑不通。

**判定: Critical。** 需要 rework 至少覆盖: (1) `metadata.test_runner` 的 pytest 命令需补 `--continue-on-collection-errors` 或修掉 `tests/__init__.py` 与 `_helpers` 绝对导入的包语义冲突 (二选一, 需 owner/tech-lead 裁决取舍面, 非本席单方案决定); (2) 需在 TASK-032 (或新任务) 里显式处理 `/home/dev/.local/bin/pytest` 隔离环境缺 PyYAML 的问题 (装依赖到该 uv tool 环境, 或改用另一个自带 PyYAML 的 pytest 调用形态), 否则 "零失败" 判据永远不可达; (3) "≥1492" 若继续沿用, 需注明这是静态计数而非可执行收集数的近似值, 或改成"实测收集数基线 + 本 Spec 新增"两段式判据 (仿 (a) 侧写法), 不能再原样保留成分号连写的合取判据。

### 镜头 3 — TASK-042/TASK-038 依赖可执行性 + TASK-034 无环

逐条核对 `dependencies` 字段构成的边:

- `TASK-000` (`:69-83`, deps `[]`) → `TASK-040` (`:84-...`, deps `[TASK-000]`) → `TASK-034` (`:537-550`, deps `[TASK-035, TASK-037, TASK-000, TASK-040]`) → `TASK-036` (`:551-...`, deps `[TASK-034]`)。这是 aria/standards 子模块合并轨。
- `TASK-039` (`:599-611`, deps `[TASK-041, TASK-033]`) 是主仓 feature 分支推送/PR/merge 轨, **不依赖** `TASK-034`/`TASK-036`/`TASK-038`/`TASK-042`, 因此推送 PR 不受这两个"merge 后、归档前"任务阻塞。
- `TASK-038` (`:612-625`, deps `[TASK-039, TASK-040]`) 与 `TASK-042` (`:626-641`, deps `[TASK-039, TASK-000, TASK-040]`) 均以 `TASK-039` (主仓 merge) 为前置, 结构上落在"merge 后"; 两者互不依赖对方, 不构成串行阻塞; 都在 `TASK-040` (完成 #174 ack 请求) 之后, 与"归档前"的时序要求 (D.2 归档发生在这些收尾任务之后, tasks.md 未把它们排在归档任务之后) 一致。
- 反向检查环: `TASK-000`/`TASK-040` 均不出现在 `TASK-039`/`TASK-038`/`TASK-042` 的下游 (它们是纯前置, 无回边); `TASK-034`/`TASK-036` (子模块轨) 与 `TASK-039`/`TASK-038`/`TASK-042` (主仓轨) 之间除共享 `TASK-000`/`TASK-040` 两个前置外无交叉引用, 不构成环。

**镜头 3 结论: 无 Critical/Major, DAG 拓扑正确, 两个"merge 后、归档前"任务不阻塞 PR。**

## Verdict

FAIL — **1 Critical / 0 Major**。Critical 为 R2 用以关闭上一轮 Critical (PP2-C1) 的"两跑法"修复本身在本容器逐字实跑不通: (b) 侧命令 0 测试执行 (未加 flag) 或 209 测试缺席 + 26 个环境性假红 (加 flag 后), "≥1492" 判据数字来源是静态 grep 而非实际收集结果。镜头 1 (TASK-020 插入点) / 镜头 3 (TASK-042/038 依赖与 TASK-034 无环) 均实读通过, 无新增问题。

## Vote

REVISE

## 轮次记录

- Round 1 (backend-architect 单席, `60808b2`): 2 Major + 4 Minor, 五席聚合 FAIL (2 Critical, 非本席贡献)。
- Round 2 (backend-architect 单席, `03c6a9e`): R1 处置全部 resolved; 五个深挖镜头全部实读通过; 投 PASS。五席聚合 FAIL (1 Critical: qa-engineer 发现的双跑法 collection 缺口), rework → v3。
- Round 3 (本轮, backend-architect 单席, `c27826e`): 复核 R2 四项处置 (PP2-C1 双跑法 / M5 TASK-020 / M1 TASK-042 / M2 组0前置), 3 项 resolved、**1 项 not_resolved**——实跑 `metadata.test_runner` 双跑法命令, 发现 (b) 侧逐字命令 0 测试执行 (package-mode 绝对导入冲突), 加修补 flag 后仍缺 209 测试 + 26 个因隔离环境缺 PyYAML 产生的假红, "≥1492" 数字系静态 grep 计数非实测。判定 **Critical**, 投票 REVISE。
