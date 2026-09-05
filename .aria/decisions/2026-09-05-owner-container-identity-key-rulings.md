# 决策单 — owner-container-identity-key-and-collision-parser (owner 裁定 2026-09-05)

> **Spec**: `openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md` (v6 → v7 回填)
> **裁定人**: owner (simonfish) · **执笔**: aria-runner-bot/bfe8285d (本容器) · **依据**: post_spec R1–R5 聚合 (`.aria/audit-reports/post_spec-R*-…-aggregated.md`) + proposal §决策点各选项后果
> **owner 原话**: 「审计可以接受当前结论」「Level 3，D-0 a，D-1 a，D-2 a，D-3 a 同意你的建议」

| # | 事项 | 裁定 | 后果 (回填落点) |
|---|------|------|------|
| 0 | post_spec 终局 (R5 max_rounds, 五席全票 PASS 0C/0M, 严格键集合未稳定 ⇒ MAX_ROUNDS_EXHAUSTED) | **[1] 接受当前结论** | R5 聚合 `overridden_by_user: true`, verdict PASS; post_spec 闸门关闭 |
| 1 | Spec Level (owner 原指令 Level 2; 判据 cross-module 成立) | **Level 3** | proposal 头部 Level 行改 Full; 需 A.2 tasks.md + A.3 detailed-tasks.yaml + post_planning 收敛审计 (convergence) |
| 2 | D-0 a1-entry track-id 含 `<container_uuid>` 与同 track 分组冲突 | **(a) 本 Spec 在 Layer H 侧纯形状剥离** (`track_to_claim_record` 一处, 尾段 `-[0-9a-f]{8}$`) | T9 由条件任务转为正式任务; §2.3.1 加尾段族键语义句 (限定仅用于 §2.3.5 Layer H 分组); 在 Aria #174 留言告知 a1-entry 侧 (不改其契约) |
| 3 | D-1 `<owner>` 段语义 | **(a) 提交身份** (git `user.email` local-part; 取值可为 `unknown`, 判据排除) | §2.3.1 文本 |
| 4 | D-2 AI runner 提交身份 | **(a) 统一机器身份**; local-part 与采用方机器账号名一致 (10CG Lab 现名 `10cg-ci-bot`; 本容器现用 `aria-runner-bot` 为 07-01 前旧名, 改名产生一次性漂移由 ⚪ 解释) | §2.3.9 文本 (只写 Aria 侧规则; 容器 `git config` 供给与 Aether 账号治理不在范围); Lab 内部指针决策单即本文件 |
| 5 | D-3 Layer H 新鲜度截止 | **(a) 本 Spec 内加** `LAYER_H_ACTIVE_WINDOW_DAYS = 30` 共享谓词 | T13 由条件任务转为正式任务; §2.3.5 加一句 |

## 与 Aether 两账号模型的关系 (Lab 内部指针, 不进 standards)

Aether 侧 SOT: `Aether/docs/guides/forgejo-token-map.md` §两账号模型 (`simonfish` 人 / `10cg-ci-bot` 机, 2026-07-01 由 `aria-runner-bot` 改名)。Aria 规范 §2.3.9 只规定「AI 会话署机器身份, local-part 与采用方机器账号名一致」, 具体账号名由采用方自定; 10CG Lab 内该名即 `10cg-ci-bot`。本容器 git 身份的实际变更是 owner 的环境动作 (10cglocal 范围), 不由本 Spec 执行。

## 执行顺序 (裁定后)

1. proposal v7 回填 (本次 commit) → 2. A.2/A.3 (`task-planner`: tasks.md + detailed-tasks.yaml, 14 任务 + 条件转正) → 3. post_planning convergence 审计 → 4. B.1 (起手 fetch a1-entry 分支实况定 S1/S2; #174 留言) → B.2 → C → D。
