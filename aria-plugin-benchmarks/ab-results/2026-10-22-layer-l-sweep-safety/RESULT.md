# RESULT — 2026-10-22 layer-l-sweep-safety (Aria#233) Rule #6 场景 1

> **套件**: iteration-1, 3 evals × 2 臂 (with=feature 分支工作树 / old=v1.77.0 `f2e801d` origin/master 快照: phase-d-closer + state-scanner SKILL.md) | **判分**: 机械 (grade_reports.py, 锚定决策字段)
> **Verdict: PASS** — 6/6 达各自预期; 三个判别面全部按 spec 翻转; 旧臂忠实复现 #233 病灶。

## 判别结果

| eval | 旧行为 (old_skill) | 新行为 (with_skill) |
|------|-------------------|---------------------|
| 0 claim-swept-signal | 无明文分支 → AI 自由裁量为「终态等价 ⇒ 按 benign 处置」并自标「这是 AI 判断, 请 owner 复核」 | **非 benign** 精确命中三分表; ⚠️ + swept_by/swept_at 出处入报告; 收尾场景不 restore; owner 复议三选项 |
| 1 routine-sweep-neighbor | 30h 邻居 claim **被扫** (24h 全域单层; skill 自证「还在干活的轨道会从碰撞面消失」= 本场景形态) | **untouched** — 分层 7d (SWEEP_TTL_CROSS), 30h < 168h; 旧语义须显式 --sweep-stale-all 且仅限运维确知死寂 |
| 2 long-session-heartbeat | **仅入口刷** — 心跳唯一挂载点 = /state-scanner 入口, 无周期机制, <24h 频率「靠自觉」; 被扫后「未必复活 abandoned, 重新认领」 | **周期刷 ≤12h** 明文义务 + 看返回 (claim_swept → 先 --restore 再继续) + fail-soft 契约 |

## 套件区分力

旧臂三例均给出完整规则链引用且忠实于旧文 (含旧 skill 自己承认的后果描述) — 非随机命中; 新臂三例均引用新条款原文并正确组合 (三分表/分层/义务+恢复链)。污染 caveat 同 A 套 (#116 既知, 两臂同条件)。

## 评分断言勘误记录 (同类第二次)

首版 forbid `周期` 命中旧臂合法的「无**周期**刷新机制」描述性用词 → 1 假红; 修正为「must: 子代理结论行 仅入口刷; must NOT: 12h (新义务专属数值)」。与 A 套勘误同型 (负向断言禁子串级敏感词) — 已入 memory 候选。
