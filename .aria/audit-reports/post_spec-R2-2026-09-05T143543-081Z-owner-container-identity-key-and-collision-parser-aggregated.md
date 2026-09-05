---
checkpoint: post_spec
round: 2
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 4C/16M/6m (五席原始合计, 去重前)
clusters: 3C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer, aria:knowledge-manager]
sibling_probe: no_sibling_found
timestamp: 2026-09-05T15:05:00.000Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
---

# post_spec R2 — owner-container-identity-key-and-collision-parser (v2 `d23f103`)

> **对象**: v2 (R1 rework)。**Sibling probe (R2 入口)**: `no_sibling_found`, 双远端 152/156 份全部扫描。**drift-checker**: convergence 未 opt-in, 未跑。
> **R1 处置核对 (五席)**: R1 的 3C/11M/14m 无一 open; closed 为主, partial 6 条 (全部是「闭合了主体、留了一半」: a1-entry 耦合未覆盖 track-id / SOT 侧假全称 / Level 理由非判据层 / advisory 取数路径 / D-2 后果不对称已改)。**本轮 Critical/Major 全部来自 v2 新引入的「owner 等价类」机制**, 不是旧问题复发 (五席一致陈述)。

## 判定

| 席 | verdict | counts | 一句话 |
|---|---|---|---|
| tech-lead | FAIL | 1C/7M/2m | a1-entry 把 container uuid 拼进 track-id, 与本 Spec「同 track_id 内分组」正面冲突, 两 Spec 都没定义; 等价类只合不拆、随语料翻转、渲染器看不到 advisory; D-1(a)+D-2(a) 让 cross_owner 生产不可达而 Positive 无条件 |
| backend-architect | FAIL | 2C/1M/0m | 按 v2 字面实现三步, 零段 vs 两段同主机名组判 cross_owner (空 owner 比较规则没写清); 生产路径只把 dedupe 后的行传 classify, 等价类拿不到全语料; T3b 守卫挂载点未定 |
| qa-engineer | FAIL | 1C/2M/0m | 隔离夹具的既有测试 (两串从未共现) 在等价类下仍翻转 cross_owner, SC-7 零回归不可达; 等价类不可逆 (两人交接一台机后永久假阴性); `len==8` 冒充 `^[0-9a-f]{8}$` 无夹具可辨 |
| code-reviewer | PASS_WITH_WARNINGS | 0C/2M/4m | 等价类在两个 classify 调用点都没有数据通路; 唯一需要等价类的用例只在 prose, 去掉步骤 3 结果与 D 完全相同 (零 baseline-failing SC) |
| knowledge-manager | PASS_WITH_WARNINGS | 0C/4M/0m | `advanced-rules.md` 路径错 (在 `references/rules/`); 漏第四消费面 `phase-d-closer/scripts/fetch_gate.py`; §2.3.5 用 `identity_key`/等价类做判据主语但标准文本未定义它们; §2.3.9 交叉引用会把 Lab 私有文档耦合进共享 SOT |

**合并判定: FAIL / 五席全 REVISE, 未收敛。** 与 R1 比较键集合不同 (R1 的簇全部闭合, 新簇全部围绕 v2 新机制) —— 不是振荡, 是「修 R1 时引入的新面」(memory `feedback_multiround_audit_catches_fix_introduced_regression` 同形)。

## Critical 簇 (去重后 3 个)

| # | 簇 | 席位 | 执笔处置 (rework v3) |
|---|---|---|---|
| **R2-C1** | **owner 等价类机制不可用**: (a) 只合不拆, 两个真人先后用过同一 uuid 容器 ⇒ 之后真撞车永久 🟡 (QA M1 · TL M-1, erin/frank 反例实跑); (b) 由全语料建, 语料随 `branches_scanned` 变化, 同输入不同容器可得相反结论, 且方向是「fetch 越全越不告警」(TL M-2); (c) 生产路径 `handoff_multibranch.py:714` 只传 dedupe 后的行给 `classify()`, 渲染器 `track_board.py:430` 又独立重算, 等价类在两处都没有数据通路 (BA R2-2 · CR M1 · TL M-6); (d) 空 owner 在比较阶段的处置没写清, 字面实现在冻结语料第二组判出 cross_owner (BA R2-1); (e) 唯一需要等价类的用例只在 prose, 去掉它结果与 D 相同 (CR M2); (f) 隔离夹具既有测试在其下仍翻转 (QA C) | BA R2-1/R2-2 · QA C/M1 · TL M-1/M-2/M-6 · CR M1/M2 | **接受: 撤销等价类 (步骤 3 整段删除)**。v3 判定改为**纯输入确定性规则**: 每 track 取每个 `identity_key` 的最新行; ≥2 个 key 时, 取**非空、非 unknown** 的 owner 串集合, ≥2 → cross_owner, ≤1 → self_multi_container; 空 owner 不可归属, 不计为独立 owner (写成规则, 不留给实现者)。在冻结语料上按生产路径实测: 两组均 🟡; 合成 7 例 (两人两机 🔴 / 同容器双 owner none / 同人两机 🟡 / 漂移后无共现证据 🔴 / 隔离夹具对 🔴 / 零段 vs 两段同主机名 🟡 / 两人共用一机 none)。漂移导致的 🔴 是**诚实的 🔴**: 数据上就是两个不同提交身份, 由 ⚪ 漂移 advisory 并排解释, 由 D-2 停止未来漂移; 不再靠推断「同一个人」。既有测试 `test_both_latest_active_still_reports_self_multi_container` 的期望**改为 cross_owner** (它原本绿的原因是 owner 段被解析丢了, 不是语义), 并加一条同 owner 串变体断 🟡 |
| **R2-C2** | **a1-entry 的 track-id 含 `<container_uuid>` 段 + §2.3.8.2 要求 carry-id 与 frontmatter track-id 同串 ⇒ 两容器对同一 Spec 的 handoff 落不同 track_id, 本 Spec 全部分类 (在 `track_id` 内) 对 A.1 认领的 Spec 恒 none**; 本 Spec 又把自己硬排在 a1-entry 之后 | TL C-1 | **上呈为决策点 D-0** (不是执笔能定的): (a) 本 Spec 加「track 族键」= `track_id` 去掉尾部 `-<8hex>` (仅当该 8hex 是语料中出现过的 identity_key) 后分组 — Aria 侧可独立落地, 确定性, 不改 a1-entry; (b) 请 a1-entry 把容器段留在 claim 的 raw id、不写进 frontmatter `track-id` — 跨 Spec 改动, 需对方容器同意; (c) 接受 A.1 认领的 Spec 不走 Layer H collision, 只靠 Layer L overlap。执笔建议 (a), 并在 Aria #174 留言征求 a1-entry 侧意见 |
| **R2-C3** | **§2.3.5 / §2.3.1 写进共享 SOT 的文本不可机械消费且自相矛盾**: 判据主语 `identity_key` / 等价类未在标准里定义 (KM C); 「`<container-id>` = uuid 字段」全称与本 Spec 自己的主机名分支互斥, §2.3.1 零 SC (TL M-7); §2.3.9 交叉引用 Lab 私有文档 (KM D) | KM C/D · TL M-7 | **接受**。v3 D2 把 `identity_key` 的构造规则 (三态: uuid 形 / 主机名 / 只读 fs 兜底) 与 owner 计数规则**写进 §2.3.1/§2.3.5 标准文本本身**; §2.3.9 只写 Aria 侧规则 + 「采用方的人机账号治理不在本规范」, Lab 内部指针放 Aria 主仓 `docs/` 不进 standards; §2.3.1 加 SC |

## Major (去重后 8 条) 与处置

| # | 簇 | 席位 | 处置 |
|---|---|---|---|
| M1 | D-1(a)+D-2(a) 组合让 owner 段成常量 ⇒ 同一 owner 的 AI 会话之间 cross_owner 不可达, 而 Positive 无条件写「真两人撞车 = 🔴」; 两决策点被当独立呈给 owner | TL M-3 | **接受**。v3 把 D-1/D-2 写成**一组耦合决策**, Positive 改为条件句: 「另一位人类操作者 (另一提交身份) 的容器 = 🔴; 同一提交身份多机 = 🟡」; 并写明 (a)+(a) 下 🔴 的真实含义 = 「不同提交身份」 |
| M2 | 硬排序 (i) 把 flip 无限期挂在对方容器的 a1-entry 上, 未写「a1-entry 未落地时的 ship 形态」; (ii)「知会」非「取得同意」 | TL M-4 | **接受**。v3 写两种 ship 形态 S1 (a1-entry 未落: 不 flip, label 陷阱**不**消除, Positive 相应条件化) / S2 (a1-entry 已落且对方同意改其 SC-3: flip); (ii) 改为「在 #174 取得对方容器 ack 后才动其 SC-3」 |
| M3 | D-3 人口低估: 8 种非 enum status (280/996 行, 含 `complete`/`closed`/`superseded`) 被 `track_to_claim_record` 静默映射为 active; 新阈值与 `:374-379` 捞回 stale winner 叠成三档 | TL M-5 | **接受**。v3 D-3 明写人口 = 「被映射为 active 的全部行 (含 280 行非 enum)」; 截止在 Layer H 记录构造前应用 (被截止的行不进 reconcile, `:374-379` 看不到它们, 无三档); 非 enum status 的终态归一属 #182, 本 Spec 只记数字不改映射 |
| M4 | T3b 守卫挂载点/时机未定; 挂进 `get_container_id()` 会让每次身份解析多一趟 git 子进程并反向依赖 coordination_ref | BA R2-3 | **接受**。v3 钉死: 守卫是**一次性迁移检查**, 挂在 `phase1_gate` / `release_gate` 启动路径 (它们本就读 coordination ref), 不进 `identity.py`; `get_container_id()` 保持零依赖 |
| M5 | `advanced-rules.md` 路径错 (实为 `references/rules/advanced-rules.md:544-572`), SC-9 未覆盖; 漏第四消费面 `phase-d-closer/scripts/fetch_gate.py:251` (`collision_kind != "none"`, 测试硬编码枚举字面) | KM A/B | **接受**。v3 D4/T7/SC-9 全列: `layer-l-integration.md:25-27,73,77` / `RECOMMENDATION_RULES.md:31` / `references/rules/advanced-rules.md:544-572` / `phase-d-closer/scripts/fetch_gate.py:251` + `tests/test_fetch_gate.py` / `state-snapshot-schema.md:1085` / `phase-1-collectors.md:75`; SKILL.md:149-154 只引用字段名不引用取值, 不在同步面 (Rule #6 零 SKILL.md 改动仍成立) |
| M6 | `len(container)==8` 冒充 `^[0-9a-f]{8}$` 在全部夹具上不可辨 | QA M2 | **接受**。SC-4 加对抗夹具: 8 位非 hex 主机名 (如 `devbox01`) 必须走主机名分支 (不折叠) |
| M7 | Level 段给的是规模理由, SOT 判据问的是性质 | TL m-1 (升簇) · CR m | **接受**。v3 按判据逐项自评: architecture = 否 (不引入新原语, 改一个 collector 内部判定) / cross-module = **是** (aria + standards) / breaking = 否 (enum 取值不变, 字段 additive)。按 SOT 流程图 cross-module 即 Level 3 ⇒ 执笔结论「判据上是 Level 3」; owner 若维持 Level 2 属显式 override, 在头部记录 |
| M8 | 8 位 hex 主机名 / label 会被形状嗅探误判为 uuid (只读 fs 兜底路径) | TL m-2 (升簇, 与 M6 同面) | **接受为已知限制成文** (Impact Risk): 兜底 hostname 恰为 8 位小写 hex 的机器会被当 uuid; 缓解 = 该路径本身是降级路径 + D3 advisory 可见 |

## Minor (6 条, 摘要)

头部计数 4 个 .py / 10 个 checkbox (CR) · 消费方行号精度 release_gate :132 / phase1_gate :486 / handoff_autofill :391 是 def 行 (CR) · D-3(a) 截止是否套到 advisory 语料 (CR; v3: advisory 不受截止, 它是漂移史) · ⚪ 行渲染无 SC (CR; v3 加) · 等价类相关 minor 随撤销失效 (TL m-2 保留为 M8)。

## 收敛判断

R2 不收敛。但方向已清: **v2 的新机制被五席从五个方向证伪, v3 撤回到确定性规则**; 剩余 Critical 中 R2-C2 是跨 Spec 契约问题, 只能作为决策点上呈, 不能在本 Spec 内单方解决。R3 席位继续同 team, 镜头改为「v3 是否还有隐含的『推断同一人』逻辑」+「决策点 D-0/D-1/D-2/D-3 是否穷尽且后果对称」+「standards 文本可机械消费性」。

## 归档

- 席位报告: 同目录 `post_spec-R2-2026-09-05T143543-081Z-owner-container-identity-key-and-collision-parser-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
- 席位实验脚本 (scratchpad, 不入库): `r2_repro.py` / `exp_r2.py` 等
