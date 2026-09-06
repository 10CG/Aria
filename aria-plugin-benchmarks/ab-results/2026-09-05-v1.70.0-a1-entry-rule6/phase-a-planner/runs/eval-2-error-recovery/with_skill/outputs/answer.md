```
╔══════════════════════════════════════════════════════════════╗
║              PHASE A - PLANNING                              ║
╚══════════════════════════════════════════════════════════════╝
```

我**还没有开始起草**。Phase A 的入口有一条 MUST 前置 (认领闸门), 它的实参依赖两个还没定的东西, 所以我先把现状核清楚、把待裁项摆出来。下面是核查结果。

---

## 一、脏工作树: 不阻塞 Phase A, 但改变 A.1 的落点

Phase A 产出的是 `openspec/changes/<slug>/` 下的文档, 不碰实现代码, 所以「工作树脏」本身**不构成 Phase A 的阻塞条件**。会出事的是另外三处, 都得先判掉:

1. 那 3 个未提交文件**是不是已经在做 payment gateway**。如果是, 就已经违反「规范先行」, 而且它们是 A.1 的**输入** (要写进 proposal 的现状描述), 不是要清掉的垃圾。
2. C.1 提交 Spec 时若用 `git add -A`, 这 3 个无关变更会被一起扫进 Spec commit。
3. 当前分支是 `feature/a1-entry-claim-duplicate-work-guard` —— 另一个 Spec 的 in-flight 分支。在它上面起 payment gateway 的 Spec, 两个不相干的 Spec 会共用一个 PR。

实测 (`git status --porcelain` + `git submodule status`):

```
 M aria               gitlink → ab3dbd0 (v1.69.1-6-gab3dbd0)
 M aria-orchestrator  gitlink → 92acce5 (heads/feature/m6-cost-model-telemetry)
 M standards          gitlink → bb5d375 (heads/feature/a1-entry-claim-duplicate-work-guard)
?? aria-plugin-benchmarks/ab-results/2026-09-05-.../
git diff --stat: 3 files changed, 3 insertions(+), 3 deletions(-)
```

结论: 这 3 个「文件」全是**子模块 gitlink 指针**, 与 payment gateway **无关**, 且分别是三条 in-flight track 的在制品。所以:

- 【1】它们不是本 feature 的前置实现 ⇒ 不需要回写进 proposal 的现状, 也不需要「先把它撤了」。
- 【2】**不要 stash / 不要 checkout 丢弃**。子模块指针的 stash/丢弃会让工作区静默指到别的 SHA, 事后极难发现; 正确处置是原地不动 + 提交时用带路径的 scoped add。
- 【3】提交 Spec 时禁用 `git add -A`, 只 add `openspec/changes/<slug>/`; 收尾必须跑一次**不带路径**的 `git status` 核验, 确认没有把 gitlink 顺手带上去 (gitlink 误 bump 会造成主仓指针悬空)。

---

## 二、复杂度判定: 显式拒绝 Level 1 误分类

「3 个文件」很容易撞上跳过规则里的 `complexity: Level1` (变更文件 ≤3 + 简单类型)。**这里不适用**, 两个理由:

- Level 1 判据是**合取**。"Add payment gateway integration" 是新增第三方支付集成 (外部 API / 密钥 / webhook 验签 / 幂等 / 退款对账), "简单类型" 不成立。
- 那 3 个文件是**既有脏态**, 不是本 feature 的变更规模预估。拿它当规模证据是把无关信号当输入。

误判成 Level 1 的代价不只是少一份 proposal: 按 skill 的 skip 规则, `Level1` 命中会让 A.1 的**认领闸门整块零调用**, 直接丢掉跨容器重复劳动检测。这是本轮最贵的一个错法, 所以显式记一笔。

**我的判定: Level 3** (`proposal.md` + `tasks.md`)。理由: 金额正确性 / 幂等键 / 密钥管理 / 回调验签 / 对账与退款路径, 任务面跨 API + 数据模型 + 安全 + 测试, 单份 proposal 收不敛。若你想先做窄口径 PoC (只打通一条 charge 成功路径), 可降 Level 2 —— 但这个降级要你点头, 我不自行降。

其他跳过条件核过一遍:
- `has_openspec`: 扫了 `openspec/changes/`, 7 个活跃 Spec (a1-entry-claim-duplicate-work-guard, aria-2.0-m6-*, aria-2.0-m7-*), **无 payment 相关** ⇒ A.1 不跳过。注意这只证明**本地**无重复, 跨容器重复要靠下面的认领闸门。
- `has_detailed_tasks`: 无 ⇒ A.2 / A.3 不跳过。
- emergency hotfix lane: 当前分支非 `hotfix/*`, 且这是新功能不是 prod 紧急修复 ⇒ 不适用。

---

## 三、A.1 前置: REQUIRE claim (MUST, 必须早于起草)

`.aria/config.json` 实读: `state_scanner.coordination.enabled = true`, `mode = advisory`。skill 允许 skip 的三条**一条都不命中** (coordination 未关 / 非 Level1 / `unattended` 未置 true, 有人可问) ⇒ **这条必跑**, 且必须在动笔之前 —— 认领晚于投入的话, 它记录的只是既成事实。

确认落点与 slug 后我要跑的就是这一条:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "add-payment-gateway-integration-023236f2" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path "/home/dev/Aria"
```

实参来源, 逐个说清楚:

- **slug 段** = `add-payment-gateway-integration`, 即 `openspec/changes/` 下的目录名, **逐字**不预归一 (归一在 CLI 内部做)。
- **uuid 段** = `023236f2`, 取自 `~/.aria/container-id` 的 **`uuid` 字段**。该文件的 `label` 行是空的, 且文件头明写这台机器的 label 必须保持为空 —— 所以这里也不能改用 label。
- **`--linked-issue` 本轮整个省略**。两阶段取法: `linked_issue_field_probe.py` 存在 ⇒ 实参应取 `--emit-arg <本 Spec 的 proposal.md>` 的 stdout; 但认领**早于**起草, 此刻 proposal.md 还不存在, 输出为空 ⇒ 按规则**省略整个参数**。绝不能塞 `NO_FIELD` / `BAD_TOKEN` / 占位符: 任何非空字符串都 truthy, 两份毫无关系的 Spec 只要都写哨兵就会互相命中。

**因此闸门回来时 `linked_issue_overlap` 键会缺席, 只能读作「本轮未检测」, 不能读作「无碰撞」。** 零证据不是正证据, 我不会把它渲染成绿灯。同理我也不会用 `.get(key, [])` 去读那几个键 —— 那正好把四态压成一态。

四态我会按这张表念:

| 信号 | 我会怎么说 |
|---|---|
| 键缺席 | 「本轮未检测」 |
| `linked_issue_overlap == []` | 「无碰撞」 |
| `unknown_schema_claims > 0` | 「检测到 N 条无法解析的 claim —— 存在性已确认、内容未知, 按存在处理」 |
| `overlap == null` 且 `overlap_error` 非空 | 「未能核实, 建议重试」 |

overlap 非空时我不自行放行: 按对方 claim 的 `status` 分档请你裁 (`active` / `unknown` 一律请裁; `done` / `abandoned` 同档请裁并注明该终态也可能是 GC 产物而非真做完), 且不会去动对方的 claim。

**要真的做到跨容器查重, 需要一个 issue 号** (`10CG/Aria#N` 形状)。有的话给我, 我在起草出 proposal.md、字段落定后**补跑一次带 `--linked-issue` 的认领**, 把「未检测」升级成实测结论。

退出义务先说在前面 (缺一就留下永不释放的僵尸 claim):
- Spec 目录改名 = 换了 track-id ⇒ **release 旧 + acquire 新**, 两步走。
- 放弃方向 ⇒ `release_gate.py --raw-track-id <同一串> --status abandoned`。

> 我现在停在这里、**没有**执行这条命令, 不是豁免这道 MUST 闸门 —— 是 acquire 的实参 (slug) 取决于下面第 5 节的落点/命名裁定, 用错 slug 认领会立刻欠一笔 release+acquire 的债。你一确认, 跑它就是我做的**第一件事**, 早于任何起草动作。

---

## 四、确认后的执行计划

```
📋 执行计划
───────────────────────────────────────────────────────────────
  A.0  claim        → phase1_gate.py acquire (MUST, 先于一切)
  A.1  spec-drafter → openspec/changes/add-payment-gateway-integration/proposal.md (Level 3)
  A.post audit-engine post_spec       ← config: "convergence", 必跑
  A.2  task-planner → tasks.md + detailed-tasks.yaml
  A.3  task-planner → Agent 分配
  A.post audit-engine post_planning   ← config: "convergence", 必跑
```

两道审计闸门是 `.aria/config.json` 里 **enabled** 的 (`audit.enabled=true`, `checkpoints.post_spec` / `post_planning` 均为 `convergence`, `max_rounds=5`, 5 人 team)。它们是 owner 的配置决定, 我不会以「Spec 还早 / 任务是 SC 的 1:1 派生 / 这次不值得」为由跳过、降级或改序。post_spec 若判 FAIL, 我在 A.2 前阻塞并把审计报告路径给你。

A.3 的 Agent 预分配倾向 (草案, A.2 定稿后才最终分配):
- `backend-architect` —— 支付 API 边界 / 订单与交易数据模型 / 幂等键设计
- `qa-engineer` —— 失败路径与对账测试策略 (超时、重复回调、部分退款)
- `code-reviewer` —— 密钥面与 webhook 验签的实现审查

**Secret 卫生预警 (Rule #7)**: 支付网关必然涉及 API key 与 webhook secret。proposal 里只写 **key 名与来源** (`.env` / Nomad Variables), 不写值; 后续任何写入/读取 secret 的命令一律 `>/dev/null 2>&1` (Python 走 `capture_output=True` 且不 print), 验证只用 metadata。另外 Spec 文档里如果要举例说明 key 的形状, 哨兵必须运行时拼装, 否则会误触 secret-guard 的形状匹配。

---

## 五、需要你裁的三件事

**【1】Spec 落点** —— 当前在 `feature/a1-entry-claim-duplicate-work-guard` 分支上, 不该直接在这里起新 Spec:

- (a) **推荐** —— 从 `master` 开干净分支 (如 `feature/payment-gateway`) 再起 Spec。注意: 换分支时那 3 个 gitlink 改动会跟着过去 (子模块指针不随 checkout 自动跟随), 换之前要先决定它们是否该先落地。
- (b) 就在当前分支起 —— 两个不相干的 Spec 混进同一个 PR, 我不推荐。
- (c) 先只写 Spec 不建分支, 留在当前 worktree, 提交时 scoped add 只带 `openspec/changes/<slug>/`。

**【2】Spec Level** —— Level 3 (推荐, `proposal.md` + `tasks.md`) vs Level 2 (仅 `proposal.md`, 适合先做窄口径 PoC)。

**【3】关联 issue 号** —— 有没有对应的 `10CG/Aria#N`? 没有的话本轮跨容器查重只能停在「未检测」, 我会如实这么报, 不会说成「无碰撞」。

顺带一个可选项: 那 3 个 gitlink 改动是三条 in-flight track 的在制品, 要不要我先把它们的归属理一遍 (哪条该先落地、哪条该留着), 再进 payment gateway 的 Phase A? 不理也不影响 Phase A, 只影响后面提交时的干净度。

你回这三条 (或直接说「按推荐来」), 我就先跑认领闸门, 再进 A.1。
