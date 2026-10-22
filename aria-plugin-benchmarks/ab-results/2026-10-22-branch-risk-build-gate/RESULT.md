# RESULT — 2026-10-22 branch-risk-build-gate (Aria#231) Rule #6 场景 1

> **套件**: iteration-1, 8 evals × 2 臂 (with_skill=feature 分支工作树 / old_skill=v1.77.0 `f2e801d` git archive 快照) | **判分**: 机械 (grade_reports.py, 断言锚定决策字段行)
> **Verdict: PASS** — 16/16 runs 达各自预期; 判别面按 #231 spec 精确翻转; 回归面零退化。

## 判别 eval (预期两臂行为不同 — 全部翻转正确)

| eval | 旧行为 (old_skill) | 新行为 (with_skill) |
|------|-------------------|---------------------|
| 0 api-mention-small-fix (**#231 原例**) | high → **Worktree** (裸 api 子串误判) | medium → **Branch** (共现不成立) |
| 3 keyword-override-empty | 忽略 config → high → Worktree | 覆盖生效 (空表) → medium → Branch |
| 5 build-disabled-skip (**#231 原例**) | 构建验证 **阻塞** (无条件, 无 config 通道) | **跳过** 非阻塞 (三态表第 1 行, 注明归属 CI) |
| 7 build-advisory-fail | **阻塞** (无视 mode:advisory) | **警告** 可继续 (三态表第 2 行) |

## 回归 eval (预期两臂一致 — 零退化)

| eval | 两臂一致行为 |
|------|-------------|
| 1 api-change-real | high → Worktree (真 API 变更未放掉) |
| 2 refactor-core-module | high → Worktree (flat 表仍有效; 旧臂还引用了裸「核心」— 出表证据) |
| 4 typo-low-regression | low → Branch |
| 6 build-blocking-fail | 阻塞 (blocking 档保留) |

## 聚合

| 臂 | pass_rate | tokens_mean | duration_mean |
|----|-----------|-------------|---------------|
| with_skill | 8/8 (100%) | 67.7k | 137s |
| old_skill | 8/8 (100%) | 65.3k | 196s |

**读法**: 两臂各对**各自预期**评分 (with=expected_new / old=expected_old), pass 率平价是设计使然; 判别信号 = 上表行为翻转。token 差 +3.6% (新增节的阅读成本); duration 差无意义 (分批 spawn 的批次混杂, 方差大)。

## 套件区分力 / 污染面声明

- **负控**: 无独立负控臂; 区分力由判别 eval 的旧臂忠实复现 bug 体现 (四例旧臂均引用旧规则链推理, 非随机)。
- **污染 caveat** (#116 既知): 两臂均在 aria 仓环境运行 (CLAUDE.md/MEMORY.md 自动加载面), 快照隔离仅限 skill 目录; 两臂同条件受染, 差分仍有效。
- eval-0 with 臂读了 feature 树的 tests/ (self-documenting 新面) — 轻度线索泄漏, 但其断言依据链落在 SKILL.md 条文本身。
- **附带发现 (已修)**: eval-7 with 臂暴露 branch-finisher `internal/TEST_PRE_VALIDATION.md` 未随三态化更新 (构建仍写死 BLOCKING) — 本 cycle 一并同步 (双源债)。

## 评分脚本断言勘误记录

首版断言 forbid `阻塞|跳过` 命中「**非**阻塞」「阻塞项: 空」与其他验证项的合法跳过 → 4 假红; 修正为锚定 `build_verdict:`/`overall:` 决策行后 16/16。教训入 memory 候选: 负向断言禁用子串级敏感词, 须锚定结构化字段。
