---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-18T11:32:10.026Z
context: issue-groomer-p1-mvp
agents: [backend-architect]
---
drift_terminated: false
drift_check_skipped: false
is_refocus: false

## 审计结论

{"id": "BA-M1", "severity": "Medium(Major)", "lens": "三面指纹", "finding": "comments 分量的全分页未钉死。proposal 修 plugin#208 只写了 issue-list 面; 指纹① 的「comments 最新 updated_at」需逐 issue 调 comments 端点, 而仓内现行先例 aria/skills/issue-triage/scripts/collectors/_issue.py:93 恰是 ?limit=50 单页无翻页 — 照抄即在本 spec 自己声明的目标上重蹈同类静默截断。且 Forgejo/Gitea comments 端点默认按创建序返回, 首页 = 最旧 50 条: >50 评论的 issue 其最新评论结构性不可见 ⇒ 状态⑩ 假阴性。SC「全分页 fetch 零丢失」未显式覆盖 comments 轴; 语料样本仅 6 comment, fixture 抓不到该形态。", "fix": "SC 或 detailed-tasks 显式声明 comments 端点同样全分页 + 终止条件, 并补一条 >50-comment 的截断反例 fixture (或采用 sort/direction 参数取最新页的等价方案, 但需钉死排序语义)。"}

{"id": "BA-M2", "severity": "Medium(Major)", "lens": "增量引擎边界", "finding": "Tier B assessment 的持久化回路未定义。task 1.2 要实现「Tier B provenance 门 + stale-assessment」, 但 assessment 产自 SKILL.md 适配层 (AI), 其跨 run 存储位置 (并入 groom-state.json 还是旁文件)、写回者、与 groom.py 对状态文件全量 read-modify-write 的合并语义 (groom.py 重写时必须保留非自有 assessment 键)、原子性归属均未规定 — 这使 groom-state.json 出现第二写者, 与第 11 态 last-writer-wins 议题叠加后该议题不再只关并发跑。", "fix": "spec 钉死 assessment 存储面: 建议独立文件 (如 groom-assessments.json) 或 state 内专属区 + groom.py 写时保留约定; schema v1 预留该面字段 (与 additive-only 契约一致), 并把「adapter 写回」纳入第 11 态裁定的考量面。"}

{"id": "BA-M3", "severity": "Medium(Major)", "lens": "tasks 粒度/依赖", "finding": "2.2 五项待裁中至少三项 (groom.py 最终路径 / 第 11 态二选一 / provenance 取值源, 另 labels.yaml 落点同性质) 是 1.1/1.2 的实现输入, 却排在 Phase 1 之后 — 依赖倒置。若第 11 态裁定选 per-terminal 后缀路径, 1.2 的状态写层按 proposal 钉死的单一 .aria/cache/groom-state.json 实现后需重做; proposal 把状态路径写死与「第 11 态随 2.2 裁」存在内部 tension (已自注, 但未给出消解顺序)。路径类裁定返工便宜 (git mv), 状态写层与 provenance 采集点返工不便宜。", "fix": "A.2 detailed-tasks 把上述四项列为 Phase B 入口早门 (owner interactive 轨成本低), 或在 tasks.md 显式标注 1.1/1.2 的对应选择为 provisional pending 2.2。"}

{"id": "BA-m4", "severity": "Minor", "lens": "Tier A 规则引擎", "finding": "title-前缀→分类键 映射的配置落点未指定。labels.yaml 只定义 分类键→forgejo label 名; 若前缀表 hardcode 在 groom.py, 它就是未被任何指纹覆盖的重分类输入 — taxonomy hash 只盖 labels.yaml, 主仓 HEAD 只随发版 gitlink bump 移动 ⇒ Tier A 规则升级后存量 issue 分类静默不刷新且 diff 段不报漂移, 侵蚀「判据输入快照」复用契约的完备性。", "fix": "前缀表并入 labels.yaml (taxonomy hash 天然覆盖), 或把规则表版本/groom.py 版本纳入指纹输入集并写进 1.2 判据快照。"}

{"id": "BA-m5", "severity": "Minor", "lens": "apply_payload", "finding": "「forgejo 对已有 label 的 add 为 no-op」是写进 SC 的外部 API 行为断言, P1 只产不写、无执行面可自证。按本项目「事实断言写进 spec 前必实跑」教训, 该断言当前依赖未标注来源。", "fix": "P1 期 SC 用 mock 构造即可; 在 4.1 dogfood 或 P2 立项前做一次性 live 验证或钉官方 API 文档引用, 作为 P2 apply CLI 的前置门。"}

{"id": "BA-m6", "severity": "Minor", "lens": "groom.py 契约", "finding": "单文件体量预估 ~1000-1200 行; 仓内先例容忍单文件 (spec_complete.py 1823 行) 但 state-scanner 自身已用 scripts/lib/ 拆分。Key Deliverables 只列单文件, 未声明可拆分。另: per-issue comments fetch 的失败语义未定义 — fetch 瞬态失败与零评论若同为 null, ⑩ 反事实被破坏; issue_scan 的 fetch_error/truncated 枚举纪律应复刻到指纹分量 (null vs unknown 二态)。成本面核实: forgejo wrapper 是 bash 脚本, dogfood ≈150 次顺序调用可接受; 仅 P3 fleet 定期化时需重评估。", "fix": "deliverables 措辞允许 scripts/ 下模块拆分; 指纹 comments 分量增加 unknown 态并在 1.3 加对应 fixture。"}

{"id": "BA-I7", "severity": "info", "lens": "其余镜头项核实", "finding": "逐项核实为可行, 无 finding: ① issue-list 全分页先例齐备, 配置形态可落地; 卫星仓枚举走 submodule origin 解析, 多仓采集成立。② openspec/changes/ 全树内容级 hash 在本项目体量下成本可忽略, archive/ 显式排除合理。③ additive-only 先例真实存在。④ tasks 双层架构下可执行可验证; 1.3 偏大建议 A.2 拆分; 2.1 可在 1.1 后并行。⑤ Rule #5 落点正确; 「路径暂定」自洽。⑥ 语料三份快照实存且形态核验, 但 full-378 无 body 字段, ⑩ 态 body 维度 fixture 需从 5-issue 样本合成 — 形态够用, 数量偏薄, 实现期可再采样。"}

## Verdict

PASS_WITH_WARNINGS — spec 可实现性成立: stdlib-only 单脚本契约在仓内先例支撑下可落地, 体量在容忍带内; 三面指纹、Tier A 逐信号 confidence、apply_payload 差集幂等与 DEC 裁定-7/8/9 逐条对得上, tasks 粒度经 detailed-tasks.yaml 细化后可执行可验证。但 3 条 Medium 精度缺口 (comments 轴分页陷阱复刻 plugin#208 形态 / Tier B assessment 持久化回路缺失 / 2.2 裁定项与 Phase 1 依赖倒置) 应在 A.2 细化或 Phase B 入口补齐, 均不阻塞立项。

## 轮次记录

Round 1 单轮: 通读 proposal/tasks + DEC-001 裁定-7/8/9, 对仓内实现先例与三份语料快照实核后按 implementation 镜头产出 3M/3m/1info, 判 PASS_WITH_WARNINGS。
