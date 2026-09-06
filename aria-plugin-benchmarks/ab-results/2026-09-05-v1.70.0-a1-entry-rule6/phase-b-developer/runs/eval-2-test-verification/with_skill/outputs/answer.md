# Phase B 测试验证 — TASK-006

先说结论: **测试门本身通过了 (代码侧 0 真实失败)**, 但 **Phase C 入口现在还不能进** —— 卡的不是测试, 是另外三条前置。下面按 phase-b-developer 的真实步骤号逐条给证据。

---

## 0. 一处步骤编号需要纠正

你写的是「Phase B B.3」, 但按 phase-b-developer 的步骤表:

| 步骤 | Skill | 职责 |
|------|-------|------|
| B.1 | branch-manager | 分支创建 |
| **B.2** | **test-verifier** | **测试验证 (你要的这件事)** |
| B.2.5 | (framework build) | 框架 build 验证 (可选) |
| B.3 | arch-update | 架构同步 |

「跑测试 + 进 Phase C 前把关」= **B.2**; 增强版里 B.3 (branch-finisher) 另有一道「测试前置验证」质量门。两者我都跑了, 下面按真实步骤号报, 免得后面 handoff 里编号对不上。

---

## 1. 前置: config-loader 实读 `.aria/config.json`

不靠默认值猜, 本仓实际配置:

| 字段 | 实际值 | 对本次的影响 |
|------|--------|--------------|
| `audit.enabled` | `true` | 审计引擎开着 |
| `audit.checkpoints.post_implementation` | `"off"` | **B.post 不触发** (config 显式 off — 属封闭豁免白名单第一类, 不是我自行跳过) |
| `audit.checkpoints.mid_implementation` | `"off"` | B.mid 不触发 |
| `audit.checkpoints.mid_post_spec` | 未配置 → off | B.drift 不触发 |
| `experiments.agent_team_audit` | `false` | 旧配置无映射 |
| `phase_b_developer.framework_build_check` | **整块缺失** → enabled=false | B.2.5 → `not_configured` |
| `state_scanner.coordination.enabled` | `true` / mode `advisory` | **B.0 认领闸门适用** (见 §3) |
| `tdd.strictness` | `advisory` | TDD 告警不阻塞 |
| `benchmarks.require_before_merge` | `true` | Rule #6 是 Phase C 前置 (见 §9) |

---

## 2. TASK-006 身份核对 — 和你的描述对不上, 需要你确认

你说 TASK-006 是「OAuth2 integration tests」。我在本工作区实读到的 TASK-006 有两条, **都不是 OAuth2**:

| 出处 | TASK-006 标题 | status |
|------|--------------|--------|
| `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml:281` | SC-15 回归守卫 (baseline 即绿): 改名两步无孤儿 + 无关第三方 claim 负控 | `done` |
| `openspec/changes/aria-2.0-m6-dispatch-input-delivery/detailed-tasks.yaml:116` | base_branch from META with Forgejo default_branch fallback | `done` |

另外全仓 `test_*.py` 里含 "oauth" 的只有 1 个文件 (`aria-orchestrator/hermes-extensions/aria-layer1/tests/test_t_redaction.py`), 是脱敏测试, 与 OAuth2 集成测试无关。

**我的处置**: 按**当前分支**上那条真实的、状态为 `done` 的 TASK-006 执行验证 —— 它就在你现在这个分支 `feature/a1-entry-claim-duplicate-work-guard` 的 Spec 里, 交付物是 `aria/skills/state-scanner/tests/test_heartbeat_by_track.py`。

**如果你说的 OAuth2 TASK-006 在另一个仓**, 给我仓路径, 我按同一套流程重跑一遍 —— 下面的结论对那个仓不成立。

---

## 3. B.0 认领闸门 (MUST) — 未满足, 需要你一句话

`coordination.enabled=true`, 所以按 B.0 这是**进 B.1 前的 MUST**: 本 session 必须已有一条 active claim。我查不到本 session 跑过 `phase1_gate` 的记录 —— 属于「goal 直驱 / B-entry 手动补 claim」那种情况。

补跑命令 (carry-id 逐字取 A.1 认领时那一串, 不重新拼):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "a1-entry-claim-duplicate-work-guard-<container_uuid>" \
  --phase B --mode advisory \
  --linked-issue "10CG/Aria#174" --repo-path /home/dev/Aria
```

**我没有替你跑**, 原因有两条, 都不是「这次不值得」:

1. 它的 Step 9 会向 `origin` 推 `refs/aria/coordination` —— 外向且难撤销的动作, 需要你显式点头, 我不自我授权。
2. 当前 shell 里 `ARIA_COORDINATION_NO_PUSH` 是**设着的** (见 §4.4), 这时候跑只会写本地 claim 而不同步远端, 等于制造一条别人看不见的认领, 比不跑更坏。

这是「执行条件不具备 + 需要授权」, 不是我判它可以豁免。要跑请回一句「跑 B.0」。

---

## 4. B.2 — test-verifier 实跑结果

### 4.1 变更面 → 测试映射

`git diff --name-only master...HEAD` 在 `aria/` 子模块里 **22 个文件**, 代码落点集中在 state-scanner:

- `skills/state-scanner/lib/` — `claim_lifecycle.py` / `collision.py` / `constants.py` / `identity.py`
- `skills/state-scanner/scripts/` — `phase1_gate.py` / `coordination_probe.py`
- `skills/state-scanner/tests/` — 6 个测试文件 (含 TASK-006 的 `test_heartbeat_by_track.py`)
- 另有 6 个 `SKILL.md` (phase-a-planner / phase-b-developer / phase-d-closer / spec-drafter / state-scanner / branch-manager) + `config-loader/DEFAULTS.json`

映射结论: 测试范围 = `aria/skills/state-scanner/tests/` (69 个 `test_*.py`)。**不是降级模式** —— 变更文件有对应测试。

### 4.2 定向: TASK-006 自己的交付物

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest \
  aria/skills/state-scanner/tests/test_heartbeat_by_track.py -q -p no:cacheprovider
```

```
............                                                             [100%]
12 passed in 1.68s
```

**12 通过 / 0 失败 / 0 跳过**, 1.68s。SC-5 / SC-6 / SC-7 / SC-15 全绿。

### 4.3 模块全量回归

先记一条坑: **从仓根跑会 12 个 collection error** (`ModuleNotFoundError: No module named '_helpers'`) —— `tests/_helpers.py` 靠 pytest 的 basedir 注入, 必须先进 tests 目录:

```bash
cd aria/skills/state-scanner/tests
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest . -q -p no:cacheprovider
```

```
FAILED test_heartbeat_only_cli.py::TestHeartbeatPush::test_refresh_without_no_push_publishes_to_remote
1 failed, 1557 passed in 216.50s (0:03:36)
```

| 指标 | 数值 |
|------|------|
| 用例总数 | **1558** |
| 通过 | **1557** |
| 失败 | **1** |
| 错误 / 跳过 | 0 / 0 |
| 耗时 | 216.50s |
| 测试文件 | 69 |
| 运行环境 | Python 3.11.2 / pytest 8.3.4 |

### 4.4 那 1 条失败的根因 + 反证 (**不是代码回归**)

```
test_heartbeat_only_cli.py:218: in test_refresh_without_no_push_publishes_to_remote
>       self.assertIs(parsed["push_skipped"], False)
E       AssertionError: True is not False
```

根因: **当前 shell 环境里 `ARIA_COORDINATION_NO_PUSH` 被设着**。这条用例的语义正是「不带 `--no-push` 时必须真推」, 该变量把推送抑制掉了, 于是 `push_skipped=True`。测试没错, 代码也没错 —— **是执行环境污染了被测行为**。

反证 (两组, 都实跑过):

```bash
# (a) 单文件, 去掉该变量
env -u ARIA_COORDINATION_NO_PUSH python3 -B -m pytest \
  test_heartbeat_only_cli.py -q -p no:cacheprovider
→ 7 passed in 5.12s

# (b) 全部 15 个涉及 push 的测试文件, 去掉该变量
env -u ARIA_COORDINATION_NO_PUSH python3 -B -m pytest <15 files> -q -p no:cacheprovider
→ 393 passed in 20.35s
```

(b) 是必要的第二组: 该变量若还造成了**反向的假绿** (断言「不该推」的用例因为它恒真而白过), 单看 (a) 看不出来。393/393 说明这 15 个文件在干净环境下同样全绿, 两个方向都没有被环境掩盖的问题。

我确认过这些用例全部跑在 `tempfile.mkdtemp()` 的临时 repo + 临时 bare remote 里 (`_fresh_repo()`), 去掉变量不会向生产 origin 推任何东西; 跑完 `git status` 与开跑前逐行一致, 工作树无新增物。

**净结论: 代码侧真实失败数 = 0。** 但我**不会**把 1557/1558 直接写成「全绿」—— 在你自己的 shell 里它现在就是红的。要么先 `unset ARIA_COORDINATION_NO_PUSH` 复跑一次全量拿到干净的 1558/1558, 要么在 handoff 里把这条环境依赖写明。

### 4.5 覆盖率 — **未测得, 不报 pass**

`pytest-cov` 没装 (`ModuleNotFoundError: No module named 'pytest_cov'`), 覆盖率**拿不到数**。

- 阈值本应是 80% (B.2 默认) / 85% (branch-finisher 与两阶段评审 Phase 2)
- 现状记为 `coverage: not_measured`, **不是 pass** —— 「没测」和「测了达标」是两回事, 写成 pass 就是假绿
- 按 Phase 2 定义覆盖率属**警告级, 不阻塞**, 所以它不拦 Phase C; 要拿数就先 `pip install pytest-cov` 再 `--cov`

---

## 5. B.2.5 框架 build 验证

`.aria/config.json` 里没有 `phase_b_developer.framework_build_check` 块 → enabled=false → **no-op**。

输出 `framework_build_passed: not_configured` (三态, **skip 不等于 pass**, 别让下游把「没跑」读成「已验证」)。Aria 本身是文档 + Python 脚本仓, 没有 framework build 环节, not_configured 是正确状态。

---

## 6. B.3 架构同步 (arch-update) — 跳过

跳过判据: 变更文件里没有匹配 `*ARCHITECTURE*.md` 的。实测主仓 9 个变更文件全在 `docs/handoff/` / `openspec/changes/` / `aria-plugin-benchmarks/ab-suite/*.json`, `docs/architecture/` 下**零改动** → **skip, 理由: 无架构文档变更**。

一条 Phase C 的提醒 (不属 B.3): 本分支改了 6 个 `SKILL.md`, 按发布同步面, 真发版时 `docs/architecture/system-architecture.md §2.8` 的 aria-plugin 版本行要一起动。那是 C 阶段的事, 这里只做记录。

---

## 7. B.post 审计检查点 — 结构性不触发

`audit.enabled=true` **但** `audit.checkpoints.post_implementation="off"` → 按 B.post 的 condition 第 3 步直接跳过, `on_skip: 继续到 Phase C`。

补一句免得误会: 这不是我在自行豁免闸门。「config 显式 off」是封闭豁免白名单的第一类, 是 owner 写在配置里的决定。真正 enabled 的两个 (`post_spec` / `post_planning`) 都不在 Phase B 的触发点上。

---

## 8. 两阶段评审 (B.Review)

**Phase 1 — 规范合规性 (阻塞)**

| 检查项 | 结果 |
|--------|------|
| OpenSpec 格式 | **PASS** — `proposal.md` 有 Status / Spec Level (2) / Linked Issue (`10CG/Aria#174`) / Why / What Changes / Success Criteria / Impact; `tasks.md` 编号连续无缺口; `detailed-tasks.yaml` 结构有效, TASK-006 `status: done` |
| UPM 状态同步 | **N/A** — 本仓没有 `unified-progress-management.md` (检查对象整个不存在 = 结构性前提不成立)。进度以 `tasks.md` 为准: **31/40** |
| 架构文档同步 | **PASS** — 无架构变更需同步 (同 §6) |

无 critical / high → **不阻塞**。

**Phase 2 — 代码质量 (警告, 不阻塞)**

| 检查项 | 结果 |
|--------|------|
| 测试覆盖率 (目标 85%) | **WARN — 未测得** (pytest-cov 缺失) |
| 代码复杂度 | 未跑 (radon 未装) |
| 安全扫描 | 未跑 |

三项都是「没跑」而不是「跑了没问题」, 按定义不阻塞, 但也不能记成通过。

---

## 9. Phase C 闸门判定

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE B - DEVELOPMENT                           ║
╚══════════════════════════════════════════════════════════════╝

执行计划
───────────────────────────────────────────────────────────────
  B.0   phase1_gate      -> 认领闸门 (MUST)
  B.1   branch-manager   -> 分支创建 (跳过 - 已在功能分支)
  B.2   test-verifier    -> 测试验证
  B.2.5 framework build  -> 框架 build (未配置)
  B.3   arch-update      -> 架构同步 (跳过 - 无架构变更)

执行结果
───────────────────────────────────────────────────────────────
  [PEND] B.0   -> 本 session 无 active claim, 需授权后补跑
  [SKIP] B.1   -> 已在 feature/a1-entry-claim-duplicate-work-guard
  [OK]   B.2   -> 定向 12/12 通过 (test_heartbeat_by_track.py)
                  模块全量 1557/1558 通过; 唯一 1 红 = 环境诱发,
                  干净环境复跑 393/393 绿 -> 代码侧真实失败 0
  [WARN] B.2   -> 覆盖率 not_measured (pytest-cov 未安装), 非阻塞
  [SKIP] B.2.5 -> framework_build_passed: not_configured
  [SKIP] B.3   -> 无 ARCHITECTURE.md 变更

上下文输出
───────────────────────────────────────────────────────────────
  branch:       feature/a1-entry-claim-duplicate-work-guard
  test_passed:  true (环境校正后)
  tests_run:    1558    passed: 1557    failed: 1(env)    real_failed: 0
  coverage:     not_measured
  framework_build_passed: not_configured
  arch_updated: false (skip)
  audit_verdict: skipped (post_implementation=off)
  ready_for_phase_c: NO
```

**测试门: PASS。Phase C 入口: 尚不满足。** 拦住的三条都不是测试:

1. **任务未做完 — 31/40**。`tasks.md` 还有 9 条未勾。Phase C 是「提交 + 合并」, 实现没收口不能进。
2. **Rule #6 AB benchmark 未跑**。本分支动了 6 个 `SKILL.md` (含指令流程面), 且 `benchmarks.require_before_merge=true` —— 合并前必须过 `/skill-creator` 的 AB。这是硬前置, 不是建议。
3. **aria 子模块工作树是脏的** — `skills/phase-a-planner/SKILL.md` 与 `skills/spec-drafter/SKILL.md` 有未提交改动。Phase C 提交前得先决定它们进不进本次提交。

外加 §3 的 B.0 认领: 严格讲也该在进 C 之前补上, 否则 reconcile 时这一轮工作没有认领记录。

---

## 10. 需要你定的两件事

1. **TASK-006 是哪一个?** 我按本分支那条真实的 (SC-15 回归守卫) 跑的。你要的 OAuth2 集成测试如果在别的仓, 给路径我重跑。
2. **要不要现在补 B.0 认领?** 它会向 origin 推 `refs/aria/coordination`, 需要你明确点头; 而且得先 `unset ARIA_COORDINATION_NO_PUSH`, 否则只会写一条不同步的本地 claim。

顺手建议 (不阻塞): 先 `unset ARIA_COORDINATION_NO_PUSH` 复跑一次全量拿到干净的 1558/1558, 再 `pip install pytest-cov` 把覆盖率从 `not_measured` 变成真数 —— 这两条都是为了让 Phase C 的证据面上不留「靠解释才成立」的项。
