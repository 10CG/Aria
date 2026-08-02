---
checkpoint: post_spec
round: 3
converged: false
overridden_by_user: false
incomplete: false
---

# post_spec R3 (第三双新鲜眼睛, 定向轮) — a1-entry-claim-duplicate-work-guard

> **席位**: 1 — `feature-dev:code-architect` (未参与 R1 五席与 R2)。**选席理由**: 前两轮审「规格对不对」, 本轮审「**照着它能不能建出来**」—— 该 agent 的专长是从既有 codebase 推导实现蓝图, 正对本轮风险 (三版叠加修订后的可实现性)。
> **verdict**: **REVISE** · `scope_ok` true · **counts**: critical=2 major=6 minor=3
> **执行注记**: 该 agent 无 Write 工具, 报告正文由主控落盘。两条 critical 均经**主控独立实读复验**。
> **timestamp**: 1785680000000 · 审计对象: 主仓 `23f34a6`

---

## 🔴 收敛性判断 —— 本轮最重要的结论

**未收敛, 且这是第一次出现同口径可比的证据。**

| 轮 | 席位数 | critical | major |
|---|---|---|---|
| R1 | 5 (config 全员) | 4 | 8 |
| R2 | 1 (type-design-analyzer) | 2 | 4 |
| **R3** | **1 (code-architect)** | **2** | **6** |

- R1→R2 席位数不同, **不可比**。
- **R2→R3 是唯一同口径 (1 席 vs 1 席) 的相邻两轮**: critical **2→2 持平**, major **4→6 上升**。
- 按本项目既有判据 (memory `feedback_stop_adding_rounds_when_major_count_flattens`): **加轮判据是 major 数是否还在同口径下降; 持平即「每轮 fix 引入约等量同形状缺陷」= 不收敛。** 本轮 major 不只是持平, 是上升。

**更值得警惕的是形状 (三条, R3 席位独立指出, 主控认同)**:

1. **R3 的 2 critical + 3 major 几乎全部命中 R2-fix 自己在「供下轮」里点名的三处未审新表面** (`container-short` / `--include-terminal` / 归一组合顺序) —— 「自认存疑」是真信号, 一审即中, 不是过度谨慎。
2. **C3 (R1 原始四个 critical 之一) 经两轮「全量吸收」仍未获得可执行方案** —— 不是新引入的问题, 是**从未被真正关闭的旧问题**。⇒「全量吸收」存在系统性盲区: 每轮注意力被最新一批 critical 吸走, 早前 critical 处置里标「Phase A.2 二选一定死」的占位符**从未被验证是否真能定**。
3. **全文标「Phase A.2 定 / 穷举 / 重评 / 定稿」的待办共 7 处**, 其中至少 3 处 (归一组合碰撞域 / 探针 fetch 机制 / C3 heartbeat-vs-TTL) 是**直接决定机制是否真正工作**的设计决策。⇒ 本 proposal 目前**不构成可以开工的实现任务书**。

**注**: 本项目 memory 的处方是「换新鲜眼睛 > 加轮」。**R2/R3 已经连续两轮换新眼睛, 仍未收敛** —— 该处方在本条修订线上已经用过且未奏效。

---

## Critical (2 条, 均经主控实读复验)

### C1 — C3 的首选修法 (heartbeat) 在当前架构下不可按字面实现, 且 Impact 表零文件覆盖

- **位置**: `proposal.md:181`「(i) 更可取」 vs `lib/claim_lifecycle.py:200-205` / `lib/identity.py:250-254` / `lib/constants.py:43-44`
- **主控复验实据 (逐字)**:
  - `constants.py:43-44`: 「**NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)**, so every live claim's heartbeat_at is frozen at acquire time」
  - `identity.py:252`: 「**Each call returns a fresh value.**」
  - `heartbeat()` 生产调用点 grep: **零**
- **问题**: `heartbeat()` 按 `(container_id, session_id)` 定位既有 claim, 而 `get_session_id()` 每次调用生成全新值, 且**代码库无任何 session_id 持久化机制**。phase-a-planner 与 phase1_gate 之间只有 subprocess 边界, 无跨调用共享 Identity 实例的路径。
- **⇒ R2-fix 写的「(i) heartbeat 更可取, 因为加长 TTL 与 sweep 设计意图相反」是错的判断** —— (i) 比 (ii) **更难**, 不是更易。而且 Impact 表 (`:278-292`) **没有一行**提到 `lib/claim_lifecycle.py` 或 `lib/identity.py`, 整条实现路径缺失。
- **修法方向**: 要么设计 session-identity 持久化 (acquire 时落盘 session_id 供后续复用, 需处理并发/过期), 要么把 heartbeat 匹配键改为 `(container_id, track_id)` (仿 `release_claim_by_track`, 不依赖 session), 并补进 Impact 表。**在此之前「(i) 更可取」不能作为 A.2 的默认结论。**

### C2 — R2-fix 自己写的 `--include-terminal` 传递链第 2 步指错函数

- **位置**: `proposal.md:154`「(2) `run_gate` 签名透传至 `linked_issue_overlaps`」 vs `phase1_gate.py:1229-1234` / `:334-1075`
- **主控复验实据**: `linked_issue_overlaps` 在生产代码里**只有一处调用** —— `phase1_gate.py:1232`, 位于 `_main()` (CLI 层), 在 `run_gate` 返回**之后**独立追加到输出 dict。`_run_gate_impl` 函数体 (334-1075 行) 对它的 grep 命中 **0**。
- **⇒ 「`run_gate` 签名透传」在架构上就是错的。** 实现者按字面走会在**错误的函数**上做工, 且很可能不会回头去改 `_main()` 里那行真正的调用点 —— **精确复现 R2 刚刚诊断的「SC-5 生产不可达」故障**。
- **这是本轮最讽刺的一条**: R2-fix 是为修「参数写了但没接到生产路径」而写的, 而它给出的接线指令本身指向了一条不存在的路径。
- **修法**: 直接在 `_main()` 现有调用处加关键字参数, **不碰** `run_gate` / `_run_gate_impl` 签名:
  ```python
  out["linked_issue_overlap"] = linked_issue_overlaps(
      claims, result.track_id, args.linked_issue,
      include_terminal=args.include_terminal,
  )
  ```

## Major (6 条)

| # | 要点 |
|---|---|
| **M1** | `container-short` 取前 8 位可能让不同容器塌成同一段 —— `get_container_id()` 返回的是 **label (若非空) 否则 uuid**, 而 `identity.py:132-135` 的文件模板**明确邀请**用户设 human-readable label (示例 `devbox-A`)。两容器命名 `devbox-A1` / `devbox-A2` ⇒ 截断后同为 `devbox-A` ⇒ 同 track_id ⇒ **被 `:219-220` 互相排除 = R2-fix 刚修好的 C1 后果换个触发对象复现**。修法: 取 `uuid` 字段本身 (跳过 label) 或不截断 |
| **M2** | **「接手」选项在 track_id 含容器段后失去可操作定义** —— R2-fix 前它天然映射到同 track_id takeover; 之后两容器**必然**不同 track_id (正是 C1 修复要的效果), 于是「接手」只能是「己方 acquire + 对方 release」。而 `release_claim_by_track` 只按**调用者自己的** container 匹配 (`claim_lifecycle.py:425`), **无任何函数支持释放别的容器的 claim** |
| **M3** | 归一 + `derive_track_id` 组合碰撞域**已由 R3 穷举**, 两类未覆盖: (a) basename 分隔符碰撞 (`aria.orch`/`aria_orch`/`aria-orch` 在 §0 判不同、在 `derive_track_id` 的 translate 后塌成同一 track_id) —— **本组织当前无含 `.`/`_` 的仓名, 属结构性 dormant**; (b) `<number>` 段未定义用归一后 int 还是原串 ⇒ `#007` 与 `#7` 派生不同 track_id ⇒ 自排除失效, 自己较早的 claim 被误判为他人碰撞 |
| **M4** | 探针 fetch「自带 vs 复用 `remote_refresh` 缓存」被当**对等选项**, 实际结构性冲突: `remote_refresh` 是 state-scanner **Phase 0.5 专属**子系统, 只在 `/state-scanner` 运行时刷新; audit-engine 多轮循环跨天运行, **无机制保证每轮之间跑过 state-scanner** ⇒ 复用缓存 = D3 要修的「首轮扫描不够」换个更深的路径复现 |
| **M5** | Impact 表未指明 `execution-modes.md` 的 **Convergence (`:84-111`) 与 Challenge (`:113-144`) 两套独立 Round N 循环**改哪个。本仓 post_spec pin 死 convergence 不受影响, 但 aria-plugin 是**跨项目分发**的, `DEFAULTS.json:124-128` 的 `adaptive_rules.level_3 → challenge` 意味着下游 Level-3 Spec 会走 Challenge ⇒ 只 patch 前者会让那些项目**静默漏掉探针**, 且无测试能发现 |
| **M6** | `phase-a-planner/SKILL.md` 的认领步骤**插入点/结构未定** —— 仿 `phase-b-developer` 的 `### B.0` 独立标题, 还是塞进现有 A.1 YAML 块的 `action:` 列表? **这不是格式偏好**: 本 Spec 的 §Why 自己用真实案例证明了「AI 执行多步骤 prose 指令时会遗漏步骤」(起草者 08-02 为 #124 认领却忘了为本轨认领), 埋进长列表的单行指令比独立标题级 gate 更容易被静默跳过 —— **而这恰恰是本 Spec 存在的理由** |

## Minor (3 条)

`--include-terminal` 无 `--linked-issue` 时静默无效 (`:1229` 的 `if args.linked_issue:` 门控整块), 与「零裁量」基调不符 · SC 表头摘要「代码类 (SC-1a/4~9)」是 R1-fix 时写的, 此后新增的 SC-10~13 与 SC-1d/1e/1f/5b 均未回填 (纯摘要过期, 下方权威表完整, 危害低) · `GateResult.error` 的 docstring (`:210`) **早已预留 `"fetch_degraded"` token 但从未被赋值** —— 又一个「已 ship ≠ 能用」同形实例, 但因有现成 token 名而属最易修一类; Spec 正文未点名引用它

## R3 确认**够实现**的部分 (下轮免重复)

- **§0 四步归一算法**钉到字符级, R2 已验证等价关系良定义 ⇒ `collision.py` 核心改动**可直接照写, 无需实现者猜**
- `--phase` 自由字符串无 `choices` 约束 —— R3 复核 `phase1_gate.py:1189-1191` 属实
- **§3c 的 release-by-track 路径可直接照字面实现** —— `release_claim_by_track` (`claim_lifecycle.py:422-427`) 按 `(container, track_id, active)` 匹配、**不依赖 session**, 不会撞上 heartbeat 那类新鲜度问题
- `layer-l-integration.md` / `config-loader/SKILL.md` 两处文本级更新描述已足够具体
- **SC 表的「代码类/行为类」分层给出了真实测试宿主**, 且与 rule6_note 的三条定向 fixture 一一对应 —— 验证面设计本身完整 (除 heartbeat 部分因机制未定而测不了)
- **§3c「A.1 统一用 issue 派生 track-id」这句 R1-fix 原文与 R2-fix 的容器段形态不矛盾** (R3 主动排查后判定): 容器段形态仍不依赖 spec-slug, 「改名不变」性质仍成立, 且该句显式转发 §1

---

## 下轮建议 (R3 席位提出, 主控转述)

若再跑, 聚焦三点: (i) heartbeat / session 持久化可行性; (ii) `--include-terminal` 真实接线点; (iii) `container-short` 碰撞域。**且下一轮应显式做「新条款交叉一致性检查」** (R2 已提出的元教训), 而非仅逐簇吸收。

**AI 不预判裁决。** 但收敛性数据 (同口径 major 4→6) 与「换新鲜眼睛已连用两轮仍未奏效」这两点, 是 owner 决定「继续加轮 / 改变策略 / 降级 Spec 范围」时应当知道的事实。
