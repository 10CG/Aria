---
checkpoint: post_brainstorm
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-18T04:57:41.956Z
context: DEC-20261018-001
agents: [qa-engineer]
---
drift_terminated: false
drift_check_skipped: false
is_refocus: false

## 审计结论

{"type": "issue", "severity": "major", "category": "testing", "scope": "DEC-001 风险表 Rule#6 行 + 下游段; 未来 issue-groomer skill 立项", "summary": "Rule#6 档位矩阵不完整: 只裁了 Tier A(substitute)/Tier B(第三行), 未裁 SKILL.md 适配层与 description 面。新增 skill 必然 description_changed=yes, SOT §4.1 规定 scenario1+4b 必填且空/n/a 即不合规; 而实测 ab-suite/trigger/ 目录不存在 (0 套件), 照 DEC 实施将结构性填不出合规 rule6_note。'trigger 套件随立项评估' 是时点承诺非行动项 (无 issue 锚、无 owner 门), P2 扩展 issue-triage 模板族的 Rule#6 义务同样未预告。档位裁定权应留在 DEC/spec 成文机制内, 此缺口会把决定推成临场判断 (SOT §4 所禁)"}

{"type": "issue", "severity": "major", "category": "testing", "scope": "DEC-001 设计段 4 上下文版本指纹; groom-state.json", "summary": "上下文指纹粒度未定义且存在已知漏检面: 'openspec/changes 清单 hash' 若是文件名级, 在制 spec 内容实质修订 (proposal 改判、tasks 勾选) 不动名不触发全量重评 — 这恰是 Tier B '在制轨' 判断的依据变化, 与 DEC 自引的 plugin#110 实证 (本体未动、评估该翻转) 同类异形, 机制的自我目的可被绕过。'最新 handoff' 判 mtime 还是 latest.md pointer 未指明, 而本项目有 mtime-pointer 分叉的既有实证教训 (collector 以 pointer 为语义权威)"}

{"type": "issue", "severity": "major", "category": "testing", "scope": "DEC-001 设计段 4 '复用上次分类' × 设计段 2 Tier A 活跃度判据", "summary": "增量复用契约结构性歧义: '未变条目复用上次分类仅重算时间敏感字段' 与 '活跃度/staleness 档是 Tier A 分类输入' 冲突 — 若复用的是分类输出, 时间敏感判据跨档 (如 90 天停滞界) 不触发重分类, 漏检方向; 且 diff 段'停滞加深'又依赖档位演进。指纹边界行为未定义: '编辑但内容等价' 与 'rebase 后 updated_at 变' 该判变还是不变 (误判变=安全浪费, 误判不变=危险漏评), 反事实测试 («机制没实现会变红吗») 需要的增量状态机 fixture 矩阵 (新条目/未变/上下文变/已关闭/编辑/跨档) 未被钉为 SC 必测场景"}

{"type": "issue", "severity": "minor", "category": "testing", "scope": "DEC-001 设计段 4 diff 段", "summary": "diff 判定与增量的交互未定义: 优先级漂移只在产生新评估时才有定义 (复用条目结构上无漂移可报; 上下文指纹触发全量重评时漂移面=全体, 报告可能爆量); 新增/已关闭是集合差可机械测, 但首跑/状态文件缺失时 diff 语义 (baseline run 空 diff 标记) 未定义"}

{"type": "issue", "severity": "minor", "category": "testing", "scope": "DEC-001 设计段 3 apply_payload / labels.yaml", "summary": "apply_payload 'delta 只加不删' 的结构面可机械验证 (schema 禁 remove 字段), 但 add 的基准 (suggested 全集 vs suggested−existing 差集) 未定义, 直接决定幂等断言写法 (forgejo 对已有 label 的 add 是 no-op, 两种基准下幂等性声称的测试构造不同); labels.yaml 为 SOT + taxonomy 一致性检查已列入 (好), 但检查挂载点 (groom.py 运行时 vs CI check) 未定"}

{"type": "issue", "severity": "minor", "category": "testing", "scope": "DEC-001 设计段 2 Tier A 契约", "summary": "Tier A 'confidence + 判据来源' 的语义 (算式、逐信号枚举 vs 聚合字符串) 未定义到可逐类反事实测试的程度。建议下游 spec 钉死三件: 每条分类判据一个反事实 fixture; '不假装语义' 的负面 fixture (无显式信号→unknown/低 confidence 而非语义猜测); fixture 从真 Forgejo 响应形态构造 (背景段 378 条实测语料在场, 防复刻旧 scan.py/triage.py 时 fixture 形态与真数据脱节的假绿)"}

{"type": "decision", "severity": "minor", "category": "testing", "scope": "DEC-001 风险表 Rule#6 行", "summary": "两项已裁档位本身与 SOT 逐行对齐, 无误用: Tier A (groom.py 纯代码) → 第一行 substitute, 与 worked examples 'collector 代码层=纯代码 substitute' 同构; Tier B (prose 语义评估行为) → 第三行且三条件 (点名行为+可证伪定向 fixture+套件缺口开 issue) 已在 DEC 预告, 下游有 'Rule#6 套件缺口 issue' 对应"}

{"type": "decision", "severity": "minor", "category": "testing", "scope": "DEC-001 设计段 5 / DEC-002 评估维度 2", "summary": "测试面收敛的结构性优点记录: label 不配独立 skill、reply 扩展模板族不新建 skill、P3 Layer 1 走脚本核 (AD7), 避开了自主运行时禁新增 description 的禁令面; 全分页 fetch 修 plugin#208 limit=50 陷阱可测 (多页 mock + 终止条件); DEC-002 把 DEC-001 可移植面当底座评估测试面, 两 DEC 交叉引用一致"}

## Verdict

PASS_WITH_WARNINGS — 0 Critical / 3 Major: 设计方向与两项已裁 Rule#6 档位均合规, 但档位矩阵漏了新增 skill 必然发生的 description/SKILL.md 面 (0 套件现状下将结构性填不出合规 rule6_note), 且增量机制的上下文指纹粒度与复用契约存在两个危险方向 (漏重评/漏重分类) 的未定义边界, 须在 spec 阶段补齐并钉为反事实 fixture。

## 轮次记录

本轮以 testing/Rule#6 镜头审了 DEC-20261018-001 全部 12 项裁定 (DEC-002 交叉引用核对, 范围外无 finding), 核对 SOT skill-benchmark-exemption.md §2/§3/§4.1 与 CLAUDE.md Rule#6 判据表, 并实测确认 ab-suite/trigger/ 0 套件现状属实。
