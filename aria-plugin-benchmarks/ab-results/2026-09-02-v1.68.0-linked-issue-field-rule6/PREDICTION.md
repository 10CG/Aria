# 测前预期 (在看到任何 run 结果之前写下) — spec-drafter hunk A + hunk B (Spec linked-issue-field-availability TASK-016/017)

**被测 hunk** (`aria/skills/spec-drafter/SKILL.md`, feature/linked-issue-field-availability, 19 行新增, CRLF 保持):
- **hunk A**: 新增小节 `## proposal.md 头部字段要求` (落 `## tasks.md 格式要求` 之前) —— 声明 `Linked Issue` 为 Level 2/3 必填 + 写法三条 (code span 形 / 多值 `, ` / 无关联逐字 `none`, 不留空不删行, `N/A`·`TBD` 非哨兵 / 不写 markdown 链接形 / 新写用英文 canonical); 外加 A.1.4 yaml 项下一行指针。
- **hunk B**: `### Level 2 预览` 围栏内头部 `> **Status**: Draft` 后插 `> **Created**: {YYYY-MM-DD}` 与 `` > **Linked Issue**: `{<org>/<repo>#<n>}` `` 两行 (与 SOT 模板逐行对齐; placeholder 非哨兵)。

**基线** = aria `d69091d` (v1.67.2) 的 spec-drafter 三文件快照 (`ab-workspace/…/skill-snapshot/spec-drafter/`, 实测 `grep -c 'Linked Issue'` = 0); **新版** = 工作树 (实测 4 处)。套件 = `ab-suite/spec-drafter.json` v1.1.0 全部 eval (当日观测 3 条: id 1 / id 2 (expectations +2) / id 3 新建定向 fixture), 每 eval 两臂各 1 run。

| eval | 预期 delta | 依据 |
|---|---|---|
| 1 level-judgment (「修复登录页面一个 typo」判 Level 1) | **无 delta** (两臂各 2/2 或同分) | hunk 只涉 Level 2/3 proposal 头部字段, 不触及 Level 判定规则 (LEVEL_GUIDE.md 零改动) |
| 2 bilingual-support (英文 proposal), 原 3 条 expectations | **无 delta** (双语解析 / 英文产出 / 意图保留 两臂同分) | hunk 不改语言处理 |
| 2 新增 2 条 (头部含 `> **Linked Issue**:` canonical 行 / 无 issue ⇒ 值逐字 `none`) | **应有 delta**: 新版 2/2, 基线 0/2 (最多 1/2) | 基线 SKILL.md 与其预览骨架都没有该字段, 基线 AI 无从得知要写它; CLAUDE.md (subagent 自动加载, 已知污染面 #116) 实测 `grep -c 'Linked Issue'` = 0, 不构成基线泄漏源 |
| 3 linked-issue-field-authoring-TARGETED (中文, 无关联 issue 的 Level 2 proposal), 5 条 | **应有 delta**: 新版 ≥4/5, 基线 ≤1/5 | 同上; 基线最可能形态 = 省略该行 (0/5) 或写成 `关联 Issue`/裸文本 (≤1/5) |

**合计预期**: 新版 ≥ 基线 + 6 (12 条断言中新增 7 条里至少 6 条只有新版过); 既有 5 条断言零负 delta; **无 WITHOUT_BETTER**。

## 可证伪点 (哪种结果会推翻什么)

- **若 eval 2/3 新版也没写出 `> **Linked Issue**:` 行** ⇒ hunk 措辞没传达到 (2026-08-23 v1.67.0 AB 的同款: 括注写了但 AI 没照做) ⇒ 改写 hunk A (更靠近 A.1.4 生成步 / 更祈使) 后重跑 iteration-2; **不带着发版**。
- **若新版写出了行但值是 placeholder `{<org>/<repo>#<n>}` 而非 `none`** ⇒ hunk B 的 placeholder 被当成默认值照抄, hunk A 第 2 条「无关联逐字 none」没被读到 ⇒ 同上改写重跑。这是 R6/TL C6 担心的形状的对偶 (骨架默认 none 会造假绿; 骨架 placeholder 若被照抄则造假红), 本次实测能分辨。
- **若基线也写出合规行** ⇒ 定向 fixture 无区分力: 查基线 transcript 是否读到了工作树 SKILL.md (快照路径错) 或 CLAUDE.md/仓内其他文档泄漏; 若是模型先验, 记入 RESULT 并保留 fixture (仍是 SC-7 的行为锚点), 但 Rule #6「有区分力」结论要降级为「本轮未证」。
- **若 eval 1 或 eval 2 既有 3 条出现负 delta** ⇒ 有外溢或 flaky, 逐条查 transcript; 预期为 0。
- **若基线在 eval 1 上也判 Level 1** (预期如此) 不构成任何结论 —— 该 eval 是回归护栏不是区分力来源。

## 运行前置核验 (跑前实测)

- `grep -c phase1_gate aria/skills/spec-drafter/SKILL.md` = **0** ⇒ 被测 skill 不可能把评测 AI 引到 `phase1_gate.py` / `release_gate.py` (母 Spec 前置块**未** ship); `ARIA_COORDINATION_NO_PUSH` 在本会话 = UNSET 因而**不构成**风险 (AB_TEST_OPERATIONS.md §场景 1 前置的适用条件「被测 Skill 能触达闸门」不成立)。评测 subagent 另被明令禁止运行 git 写命令 / 闸门脚本 / state-scanner。跑后仍执行 `git ls-remote origin refs/aria/coordination` 与本地比对以核验零推送。
- 基线快照三文件来自 `git -C aria show d69091d:skills/spec-drafter/<f>` (非工作树复制), 与新版的唯一差异应恰为本 hunk (`diff` 核验)。
