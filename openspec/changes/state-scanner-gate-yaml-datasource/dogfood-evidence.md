# Dogfood evidence — state-scanner-gate-yaml-datasource (aria-plugin #113)

> SC-10 端到端实测记录 (Phase B.2, 2026-07-20)。真实命令 + 真实输出, 非合成断言。
> aria @ `feature/state-scanner-gate-yaml-datasource` (基于 v1.62.1 `6e1eb24`)。

## 1. scan.py 端到端 (合成 yaml-only 项目)

Fixture: 单 change `yaml-only-live`, 仅 `proposal.md` + `detailed-tasks.yaml`
(2 tasks: 1 done / 1 pending + 1 行内标注 + `execution_order:`/`summary:` 兄弟键
+ `metadata.status` 叙事串 — 同时覆盖 SC-3f(ii) / SC-15 / SC-16 危险形状)。

```
$ python3 aria/skills/state-scanner/scripts/scan.py --output .aria/state-snapshot.json
exit=0

carry_forward: {"active_change_count": 1, "by_change": {"yaml-only-live":
  {"count": 1, "samples": ["<行内标注>"]}}, "total": 1}
design_deferred ids: []
changes total: 1
errors: []
```

**判读**: `carry_forward.total=1` — 改动前该字段对 yaml-only spec **结构性恒 0**
(triage case-3 的展示假绿)。`design_deferred` 空 = 无误报噪音。`errors=[]` =
新解析未引入 soft_error。

## 2. `spec_complete.py --gate` CLI

### 2a. 残留 fixture (SC-1)

```
$ python3 .../lib/spec_complete.py --gate openspec/changes/yaml-only-live
verdict: pass | claims: []
deferred: [('TASK-002', 'status=pending'), (None, 'carry-forward annotation')]
complete: False | detailed-tasks.yaml has 1/2 non-done task(s); normalized Status = 'approved' …
```

**判读**: 残留被**精确列举**为两 shape (status 残留 + 标注残留, ∪ 两半齐全);
verdict 保持 `pass` (残留走 `complete` 轴, 不抬 verdict — 与 tasks.md 路径对称);
无 blanket claim (v1.61.0 会在此发 `-source-unsupported`)。

### 2b. 干净 fixture (SC-2 full-pass)

```
$ python3 .../lib/spec_complete.py --gate openspec/changes/clean-live
verdict: pass | claims: [] | d_payload: None
complete: True
```

**判读**: 真干净 → **零 tracker、零 warn**。这是本 change 的核心诉求 (v1.61.0 对
同一形态也会 warn + 建 tracker)。`complete=True` 来自新增的 OR 中支 (SC-6)。

## 3. 自反性检查点 (决策 14) — gate 跑本 spec 自己

本 spec 是 Level 2 / path B, 自身即 yaml-only 类, 是本 change 之后**新产**的活体实例。

```
$ python3 .../lib/spec_complete.py --gate openspec/changes/state-scanner-gate-yaml-datasource
verdict: pass | claims: []
complete: False
deferred count: 12 → TASK-001..010 (status=pending) + 2× carry-forward annotation
```

**dogfood 抓到的真问题**: 那 2 条标注残留**不是真残留** —— 是 yaml 的
verification 文字里为描述测试 fixture 而写的标注**字面量**, 被 `_CARRY_FORWARD_RE`
命中。同 memory `reference_secret_guard_false_positive_on_spec_docs` 一类
(讨论某模式的文档被该模式的检测器命中)。

**处置**: 按同一解药改写措辞 (描述性提及不写字面量) + 在该行留 ⚠️ 注记说明原因。
复跑确认:

```
自反 dogfood 复跑: 标注残留 = 0 (应为 0); status 残留 = 10 (10 任务未勾, 归档前会转 done)
```

**Phase D 归档时预期**: 10 任务转 `done` 后, 本 spec 应落 **SC-2 full-pass** 或
**SC-2b scoped warn** (取决于届时 done-family task title 是否含集成关键词 —
TASK-001「切片器物理归位」/ TASK-006「carry_forward yaml fallback」等标题需届时实测)。
归档执行者须核对实际 gate 输出与该预期一致 (决策 14 的检查点)。

## 4. 全量回归 (SC-9)

```
$ python3 aria/skills/state-scanner/tests/run_tests.py
Ran 1318 tests — OK   (基线 1250 @ v1.62.1 + 68 新增)
# 计数说明: B.2 实施期 1310 → pre-merge review 处置后 1318
#   (+2 silent-failure-hunter: fold-crash 锁定 / directory-yaml 负控;
#    +6 code-review: I-4 字段列锚定 ×4 / I-3 tasks.md 不可读臂 / M-5 重复 tasks: 守卫)
```

carve-out 账目: `test_gate_yaml_only_source.py::test_yaml_only_warns_and_builds_payload`
按新三态契约改写 (原断言钉死已退役的 blanket 行为); 同文件
`test_both_sources_no_false_warn` 语义不变原样保留;
`TestRuntimeProbeFoldL2ProposalOnlyEvaporates` 断言**未动** (仅 docstring 泛化措辞
按 SC-13 收窄), 作为未触碰护栏保绿。

## 5. Pre-merge review 处置 (2026-07-20)

两路独立 review (config 里 `pre_merge` checkpoint 为 `off`, 属 Rule #10 白名单显式豁免;
仍按姊妹 spec 惯例跑轻量 review)。

### silent-failure-hunter — 1 CRITICAL (fix-introduced) + 2 MEDIUM + 2 LOW, 全修

| 级别 | Finding | 处置 |
|------|---------|------|
| **CRITICAL** | `_fold_yaml_only_datasource` 的崩溃处理器 **fail-toward-GREEN**: 唯一完成度数据源评估崩溃时 gate 报干净 pass (注入缺陷实证 `verdict=warn → pass` / `d_payload=set → None`)。`soft_errors` 无人路由 (openspec-archive 只看 `verdict` 与 `d_payload != null`) —— **#166 同款静默假绿在消灭它的 change 内复发** | 改 fail-toward-warn + 追 unverified_claim (使 d_payload 非 None, D tracker 仍触发); 加**可证伪测试** (旧处理器下 `'pass' != 'warn'` RED 实证) |
| MEDIUM | `test_unreadable_yaml_is_fail_soft` 用目录作 fixture, `.is_file()` 直接 False, **永不进 OSError 分支**; 断言 `total==0` 恒真 (删掉生产 soft_error 行仍绿) | 改真不可读文件 (chmod 000 + root 环境 skipTest) 并断言 soft_error kind 真发出; 另拆一条 directory 负控 |
| MEDIUM | probe 测试断言全被无保护 `if` 包裹, 若 outcome 被重分类即静默退化 no-op | 先 pin fixture 前提再消费 |
| LOW | golden 语料部分缺失静默降覆盖 | 改 all-or-nothing, 缺一即响亮失败 |
| LOW | `project_root` 双推导 / `_yaml_unparseable` 未用参数 | 收成单一推导点 (可传入) + 清参数 |

### code-reviewer — Phase 1 PASS / 0 Critical / 4 Important + 8 Minor

**独立实证 (非纸面)**: 对 **128 份真实 archive spec** 跑改动前/后全量对拆 —— 归一化
`Step2`→`Step 7` 一处文案后, 非-yaml-only spec 残差 **0/125**, 证明
`_fold_probe_and_build_payload` 抽取是真行为保持; 三份 golden 输出与 proposal 预测逐字吻合;
parser 在 8 组对抗形状下边界判定全对。

| 级别 | Finding | 处置 |
|------|---------|------|
| **I-4** (唯一实现缺陷, 新假绿方向) | `_STATUS_LINE_RE` 匹配任意缩进 → **更深缩进的 `status:` 遮蔽任务真实 status** (折叠标量行 / 嵌套子映射键, 两形状复现均误判 `done`) | 提取改锚到任务**自身字段列** (由 `- id:` 的 `id:` 起始列推出), 浅于/缺失 → None → 计残留 (fail-CLOSED); 4 条新测试 |
| I-1 | SC-4「byte-identical」字面为假: `Step2`→`Step 7` 改到了 `d_payload.body` 这一**运行时输出** (64/128 spec body 变化) | 裁定**保留改名** (原文对该动作是事实错误引用) + 补 **amendment A-5** + SC-4 改述为「除该处文案顺改外 byte-identical」+ 测试改为显式断言 d_payload 全结构 |
| I-2 | `detailed_tasks_read_failed` 零覆盖 | 已由 silent-failure-hunter 同类 finding 修复 (chmod 测试实测真发出该 kind) |
| I-3 | SC-13 第二半 (tasks.md present-but-unreadable 早退臂) 完全未测, 同名测试实际测的是可读路径 | 用 `patch.object(Path, "read_text")` 定向抛 OSError 真覆盖该臂; 原测试拆名为 `test_readable_tasks_md_folds_probe_as_before` |
| M-1/M-2/M-4/M-5/M-7 | import 惯例 / 抽取时丢失的三段设计理据 / CRLF docstring 过度声称 / 重复顶层 `tasks:` 静默丢块 / 计数账目 | 全部处置 (M-5 加 fail-closed 守卫 + 测试) |
| M-3/M-6/M-8 | soft_errors 顺序理论差异 (不可达) / SC-10 无自动化回归 (薄接线层) / `SKILL.md:274` 排版 | 记录不改 —— M-8 属 owner 已裁定的幽灵范围边界外 |

**两路 review 的共同教训**: 4 条 Important 里 3 条同型 —— **测试的名字与 docstring 声称了它没有验证的东西**,
正是本 spec 上游 #95「勾选完成≠运行现实」在测试层的复发。
