```
╔══════════════════════════════════════════════════════════════╗
║              PHASE A - PLANNING                              ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  A.1-pre 认领闸门     → phase1_gate (MUST, 早于起草)
  A.1     spec-drafter → 创建 Spec (无既有 Spec, 不跳过)
  A.post  audit-engine → post_spec 检查点 (config: convergence)
  A.2     task-planner → 任务规划
  A.3     task-planner → Agent 分配

🚀 执行中...
───────────────────────────────────────────────────────────────
  ⚠️ A.1-pre 未能执行 → 见下「1. 认领闸门」(执行条件不具备, 非豁免)
  ✅ A.1   完成 → Spec: add-oauth2-social-login (Level 3, draft)
  ⚠️ A.post 跑了 3 轮 → PASS_WITH_WARNINGS (第 4 轮欠着, 见下「3.」)
  ✅ A.2   完成 → 任务数: 20 (72-104h)
  ✅ A.3   完成 → Agent 已分配 (4 类)

📤 上下文输出
───────────────────────────────────────────────────────────────
  spec_id: add-oauth2-social-login
  task_count: 20
  ready_for: Phase B (但有 3 项须 owner 先裁, 见文末)
```

---

## 1. A.1 前置 — 认领闸门 (MUST, 本次**未能执行**)

按 Phase A 的规定, 起草任何 Spec **之前**先认领。我把实参逐条推导好了, 但**没有真的执行**这条命令, 原因见下。

**推导出来的命令** (实参都是实测来的, 不是模板):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "add-oauth2-social-login-023236f2" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path /home/dev/Aria
```

实参怎么来的:

1. **`--raw-track-id`** = `<spec-slug>-<container_uuid>` 逐字拼。slug = `add-oauth2-social-login` (即 `openspec/changes/<slug>/` 的目录名, 不预归一); uuid 段 = `~/.aria/container-id` 的 **`uuid` 字段** = `023236f2` —— 不是 `label` (该文件里 label 本身就是空的, 且注释写明这台机器的协调身份钉在 `023236f2`)。
2. **`--linked-issue`**: 两阶段取法的第一阶段命中 —— `linked_issue_field_probe.py` **存在**, 我实跑了 `--emit-arg <本 Spec 的 proposal.md>`, **stdout 为空** (proposal 的 Linked Issue 字段是哨兵 `none`)。按规定 **输出为空 ⇒ 整个参数省略**, 所以命令里没有这一行。哨兵绝不能当值传 —— 任何非空字符串都 truthy, 两份毫无关系的 Spec 只要都写 `none` 就会互相命中。
3. **`--mode advisory`** 取自 `.aria/config.json` 的 `state_scanner.coordination.mode`。

**skip 三条逐条核过, 一条都不成立**: `coordination.enabled` 实测为 `true` (不是显式 false); 本次是 Level 3 不是 Level1; `unattended` 未置 true (是交互会话)。所以本块**该跑**。

**那为什么没跑**: 本次会话被明确约束为不得改动仓库内任何文件, 而 `phase1_gate.py` 即使加 `--no-push`, 仍会 fetch 并写本地 `refs/aria/coordination`。这是**执行条件不具备, 不是规则豁免** —— 该闸门仍然欠着。

**后果按四态如实标注**: `linked_issue_overlap` 键**缺席** ⇒ 措辞是「**本轮未检测**」。不是「无碰撞」—— 零证据不是正证据。进 Phase B 之前必须补跑这条命令, 若届时 overlap 非空, 要按对方 claim 的 `status` 分档请你裁 (`active` / `unknown` 视同 active / `done`·`abandoned` 同档请裁但注明终态也可能是 GC 产物), 我不会自行放行。

另外两条退出义务先记在这里: Spec 目录若改名 = 换 track-id, 必须 release 旧的再 acquire 新的; 若整个方向放弃, 要跑 `release_gate.py --raw-track-id add-oauth2-social-login-023236f2 --status abandoned`, 否则留下永不释放的僵尸 claim。

---

## 2. A.1 — Spec 创建

- **Spec ID**: `add-oauth2-social-login`
- **Level 3 (Full)**, 依据: 跨模块 (认证/数据模型/路由/会话/CI) + 安全承重 + 明显超过 10 个文件, 不是 Level 2 的量级
- **状态**: Draft (未 approved —— 见下面第 3 节和文末待裁项)
- **产物**: `proposal.md` (§A–§H + Impact + 30 条 Success Criteria) 与 `audit-trail.md`

范围上做了一个明确取舍: 两家提供方一起做, 不做"先上 GitHub 再补 Google"。理由是两家的差异 (GitHub 邮箱可能不可见/多个, Google 有 `email_verified` 与 OIDC `sub`/`nonce`) 恰好把 provider 抽象层的接缝一次性压出来; 只做一家, 抽象层的正确性会推迟到接第二家时才暴露。

明确划到 out of scope 的: 第三家及以上提供方、终端用户自助解绑与多身份管理 UI、管理员只读视图、用社交身份做 API 授权、refresh token 存储。

---

## 3. A.post — post_spec 审计 (这一段是本次最需要你看的)

`.aria/config.json` 里 `audit.enabled = true`、`checkpoints.post_spec = "convergence"`、`max_rounds = 5`、team 是 5 个 agent。这是 enabled 的闸门, 我没有资格以「Spec 还行 / 性价比不高」跳过, 所以照跑了。

**跑了 3 轮, 每轮 5 个席位。计数由脚本按两种口径机械重算** (口径定义与逐簇表在 `audit-trail.md`):

| 轮次 | 簇口径 CRITICAL / MAJOR / MINOR | 本轮发现里「由上一轮修复自己引入」的占比 |
|---|---|---|
| R1 | 7 / 14 / 4 | — |
| R2 | 5 / 12 / 3 | 26/27 = **96%** |
| R3 | 7 / 8 / 2 | 16/21 = **76%** (本轮每席上限由 6 降为 5, 绝对值与前两轮不严格可比) |

三轮抓到的东西是真的, 举几个代表: Google 的 `nonce` 在接口签名里根本没有通道 (校验形同虚设); `email_verified=false` 的自动绑定判定顺序有洞; 分支表把"同一邮箱命中 ≥2 个既有账号"漏进了新建分支; 只信提供方的 `email_verified` 而不问**本地**邮箱是否验证过, 等于把每个存量未验证账号变成一键接管入口; 好几条 Success Criteria 是恒绿的 (SC-4 原来用 "users 计数不变" 做指标 —— 正确拒绝和误绑定两种实现下这个数一模一样)。这些全部已吸收进现在的 `proposal.md`。

**但我要如实说两件不好看的事**:

**【1】这个 Spec 在当前执笔配置下没有收敛。** 两条判据给出**相反**结论, 我不替你选:
  - 「MAJOR 还在不在降」⇒ 14 → 12 → 8, 还在降 ⇒ 继续加轮仍有产出
  - 「本轮发现里由上一轮修复引入的占比是否 > 1/2」⇒ 96% / 76%, 两轮都远超 ⇒ 已过边际拐点, 该换执笔席而不是接着刷轮次

  CRITICAL 簇数 7 → 5 → 7 基本持平, 而且**每轮的 CRITICAL 都落在上一轮新写的章节上** (R2 落在 R1 新写的 §D.2/§G, R3 落在 R2 新写的 §C 校验链/§E.2/§E.3)。这个形状本身就是结论: 规格面每轮都在长大, 新表面带来新缺陷。

**【2】第 4 轮 (表决轮) 我没跑成 —— 会话级 subagent 配额耗尽。** 这同样是**执行条件不具备, 不是规则豁免**。所以现在这一版 `proposal.md` (吸收 R3 之后的版本) **是没有被任何一双眼睛看过的**。

**我给出的 verdict 是 `PASS_WITH_WARNINGS`, 理由和它的边界**: 本轮表决问的是「够不够进入 A.2」, 判据是"任务分解会不会因此分错、Phase B 一动手会不会推翻分解", 不是"规格是否完美"。我逐条过了 R3 的 17 个簇 —— **全部是模块内部的细节** (哪一列、哪个顺序、哪个 cookie 属性、哪条断言), 没有一条会让工作在模块之间搬家或增删模块。所以任务分解可以做。这条判断是**我作为编排层做的**, 不是 5 个席位投出来的, 请你复议; 如果你认为该按 FAIL 处理, A.2/A.3 的产物就作废重来。

**欠着的 R4 已经写进 `detailed-tasks.yaml` 的 `gates` 里**, 须在 B.2 完成前补跑。

---

## 4. A.2 — 任务规划 (20 个任务, 72-104h)

双层产物: `tasks.md` (Layer 1, checkbox) + `detailed-tasks.yaml` (Layer 2), 编号已机械对账 (20 条一一对应, 无跳号/重号/悬空依赖)。

| Phase | 任务 | 估时 |
|---|---|---|
| 1. 数据层与抽象层 | 4 (三个迁移 + provider 抽象层) | 14-20h |
| 2. Provider Adapter | 2 (GitHub 四形态判定表 / Google OIDC 五项校验) | 10-14h |
| 3. 路由、事务与会话 | 5 (start / callback 八步链 / error_code 枚举 / 会话轮换 / 启动期配置校验) | 20-28h |
| 4. 账号解析 | 2 (七行判定表 + 字符级匹配 / 建号事务与两类冲突恢复) | 10-14h |
| 5. 待确认流程 §G | 2 (**被门禁挡着**) | 8-12h |
| 6. 运维与 CI | 3 (unlink / 过期清理 / CI 三项) | 6-10h |
| 7. 验收与文档 | 2 (SC 覆盖矩阵 / 文档同步) | 4-6h |

拆分口径是**按文件域**分的, 同一文件的工作不跨任务并行。三条硬依赖写进了 `tasks.md` 的依赖图: 4.1 依赖 1.2 的 `users.email_verified` 列 (否则判定表第 5/6 行无法表达); 3.2 的 PKCE 本地预检依赖 1.3 的 `code_challenge` 列; 5.2 依赖 5.1 与 4.2。

另外, TASK-009 (callback 八步链) 标了一句约束: **拆子任务时不得把八步拆到不同 PR** —— 顺序本身就是不变量, 拆开就没人守得住。

---

## 5. A.3 — Agent 分配

| Agent | 任务数 | 任务 |
|---|---|---|
| `backend-architect` | 17 | TASK-001~017 (迁移 / 抽象层 / 两个 adapter / 路由与八步校验链 / 账号解析与事务 / pending 流程 / 运维命令) |
| `tech-lead` | 1 | TASK-018 CI 三项 (流水线与工程流程设计, 不是单系统实现) |
| `qa-engineer` | 1 | TASK-019 SC 覆盖矩阵对账 (需要独立于实现者的眼睛) |
| `knowledge-manager` | 1 | TASK-020 架构与接入文档同步 |

17/20 落在 `backend-architect` 上 —— 这不是分配偷懒, 是这个 feature 的性质 (整块都是后端认证实现)。制衡放在验收侧: TASK-019 由 qa-engineer 独立对账 30 条 SC, 且每条负向 SC 要求**用坏实现验证它的拒绝能力**, 不是只看当前取值绿不绿。

---

## 6. context_for_next

```yaml
spec_id: add-oauth2-social-login
spec_level: 3
spec_status: draft          # 不是 approved
task_list: [TASK-001 ... TASK-020]
task_count: 20
estimated_hours: "72-104"
assigned_agents:
  backend-architect: 17
  tech-lead: 1
  qa-engineer: 1
  knowledge-manager: 1
blocked_tasks:
  TASK-014: [D-1, D-2]      # §G pending 流程
  TASK-015: [D-1, D-2]      # §G 两个端点
owed_gates:
  - phase1_gate A.1 认领 (未执行: 执行条件不具备)
  - post_spec R4 表决轮 (未执行: subagent 配额耗尽)
ready_for: Phase B          # 条件: 下面三项先清
```

---

## 7. 要你拍板的三件事 (都不是我能自己定的)

1. **D-1 (产品级)**: 社交身份要绑到既有账号、但邮箱未验证时, 走 **密码确认页** 还是 **确认邮件**? 现在正文里写的是密码确认页, 状态标的是 `awaiting_owner_ratification` —— **写进正文不等于已获批准**, 我没有按"无回应即批准"处理。
2. **D-2 (产品级)**: GitHub 用户邮箱不可见时, **强制补填邮箱** 还是 **允许无邮箱账号**? 现在写的是强制补填, 同样待批。
3. **流程复议 (Rule #10 相关)**: 上面第 3 节那个 `PASS_WITH_WARNINGS` 是我作为编排层下的判断, 不是审计席位投出来的, 而且 R4 欠着、当前这版规格没有被任何席位看过。请复议: 是接受它进 A.2 (现状), 还是按 FAIL 处理、把 A.2/A.3 产物作废、先补 R4?

另外一件不用你决定但要知会: **A.1 的认领闸门这次没跑成**, 所以「远端有没有人在做同一件事」这个问题目前是**未检测**状态, 不是"没碰撞"。进 Phase B 前我会先补跑。

---

**本次落盘的文件** (都在 `openspec/changes/add-oauth2-social-login/`):
`proposal.md` / `tasks.md` / `detailed-tasks.yaml` / `audit-trail.md`
