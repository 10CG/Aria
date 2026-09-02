# Rule #6 AB 结果 — spec-drafter hunk A + hunk B (Aria Spec `linked-issue-field-availability` TASK-016 / TASK-017; ship aria-plugin v1.68.0)

**基线** aria `d69091d` (v1.67.2) spec-drafter 三文件快照 vs **新版** feature/linked-issue-field-availability `b47fe11` (hunk A 小节 + A.1.4 指针 + hunk B 预览骨架两行, 19 行新增)。
执行: /skill-creator 流程 (`agents/grader.md` 独立评分席 + `scripts.aggregate_benchmark`), 每 eval 两臂各 1 run, 6 个独立 executor subagent + 1 个独立 grader subagent; 机械可判断言 (字段行 / `none` 哨兵 / 顺序 / 链接形 / 别名) 由真实 extractor `lib/linked_issue_field.py` 程序化预判后交 grader 引用。套件 = `ab-suite/spec-drafter.json` v1.1.0 全部 eval (3 条: id 1 / id 2 expectations +2 / id 3 新建定向 fixture)。
`benchmark.json` 由 `aggregate_benchmark.py` 生成 (⚠️ 其 `tokens` 取 grader 写的 output-chars 代理, 非 executor 真实 token; 真实值在各 `timing.json`, 下表用它)。

## §1 结果

### iteration-1 — 环境 = ship 态 (新 SOT 模板已在工作树; 旧 skill vs 新 skill)

| eval | 新版 | 基线 | delta | 基线臂 token / 时长 | 新版臂 token / 时长 |
|---|---|---|---|---|---|
| 1 level-judgment | 2/2 | 2/2 | — | 74.0k / 92s | 75.4k / 105s |
| 2 bilingual-support (原 3 + 新 2) | 5/5 | **5/5** | — | 131.3k / 549s | 114.9k / 358s |
| 3 linked-issue-field-authoring-TARGETED (新建) | 5/5 | **5/5** | — | 168.6k / 743s | 142.3k / 504s |
| 合计 | 12/12 | 12/12 | **0** | | |

**零判别的原因 (基线臂自证)**: 基线 eval-3 `answer.md:9` 逐字「按 `standards/openspec/templates/proposal-minimal.md` 的 Usage Notes 要求, 已核实无关联 issue 时逐字写 `none`」—— 旧 SKILL.md `## 相关文档` 链到 SOT 模板, 评测 AI 顺着链接读到了**本 Spec 同批 (TASK-013) 改过的新模板**, 于是写出合规行。这是 PREDICTION.md 可证伪点 3 预告的「仓内其他文档泄漏」形状 (memory `ab-input-baseline` 同形: 基线输入必须是旧世界的产物)。

### control-old-template — 环境 = 本 Spec 落地前 (模板临时回到 standards `334c609`, 旧 skill 新跑; 新版臂复用 iteration-1 run)

| eval | 新版 | 基线 (旧 skill + 旧模板) | delta | 基线臂 token / 时长 |
|---|---|---|---|---|
| 2 bilingual-support | 5/5 | **3/5** (A4 `> **Linked Issue**:` 行 FAIL: `verdict=NO_FIELD`, 全文 0 命中; A5 值 `none` FAIL) | **+2** | 118.7k / 454s |
| 3 TARGETED | 5/5 | **4/5** (A4 四行顺序 FAIL: 无 `> **Level**` 行, 改名 `> **Spec Level**: 2` 且挪到第三位; A1/A2/A3/A5 过) | **+1** | 173.3k / 668s |
| 合计 (2 eval) | 10/10 | 7/10 | **+3** | |

**control eval-3 基线仍写出字段行的来源**: 该 run 读了仓内在制 `openspec/changes/sibling-spec-probe/proposal.md` (`:6` 正是 `` > **Linked Issue**: `none` — <散文> ``) 与 `a1-entry-claim-duplicate-work-guard/proposal.md` (`:13` `` `10CG/Aria#174` ``) 作 house style, 输出形态与前者同形 —— **第二条泄漏通道 = 在制 proposal 语料** (9 份在制里 3 份自 2026-08-30 起带该行), 不是 skill 也不是模板。这一条在本仓无法用 pin 模板消除。

### 测前预期 vs 实测 (PREDICTION.md)

| 预期 | 实测 | |
|---|---|---|
| eval 1 无 delta | 2/2 vs 2/2 | ✅ |
| eval 2 原 3 条无 delta | 双臂 3/3 (iteration-1 与 control 皆是) | ✅ |
| eval 2 新 2 条 新版 2/2 / 基线 0/2 | iteration-1 基线 **2/2** (模板泄漏); control 基线 **0/2** | 可证伪点 3 命中 (泄漏源 = 同批新模板); control 复现预期 |
| eval 3 新版 ≥4/5 / 基线 ≤1/5 | 新版 5/5; iteration-1 基线 5/5; control 基线 **4/5** | 新版侧 ✅; 基线侧**未达预期** —— 第二泄漏通道 (在制 proposal 语料) 使基线靠模仿通过 4 条; 唯一区分项 = 头部 Level 行名与顺序 (hunk B 对齐 SOT 的那两行) |
| 合计 新版 ≥ 基线 + 6 | ship 态 0; 落地前世界 +3 | 部分成立 (见 §2 结论) |
| 无 WITHOUT_BETTER / 既有断言零负 delta | 全部 run 无一条基线过而新版败 | ✅ |

## §2 结论 (Rule #6 判据表)

1. **照跑 (第二行)**: 全部现有 eval 已跑, **无 WITHOUT_BETTER**, 既有 5 条断言零负 delta, 无回归 ⇒ hunk A/B 可 ship。
2. **定向 fixture 的区分力 (第三行)**: eval id 3 对「本 Spec 落地前的世界」有区分力 (+1, 且 eval id 2 英文臂 +2), 对「ship 态里只换 skill」**本轮未证** (0)。原因不是断言无力 (grader: 「需修的是 AB 环境隔离, 不是断言」), 而是本仓基线有两条语料泄漏通道 (同批新模板 / 在制 proposal)。**Rule #6 结论按 memory `ab-input-baseline` 降级为「区分力: 落地前世界已证, skill 边际未证」**, fixture 仍保留为 SC-7 的行为锚点。
3. **hunk B (R5/C1) 的必要性主张被削弱** (n=1): R5/C1 判「预览骨架才是 AI 真正照抄的对象, 不改它字段大概率缺失」; 实测 3 个写出字段的基线 run 都不是靠骨架, 而是靠读 SOT 模板 / 在制 proposal。hunk B 仍保留 —— 它是 SC-7a 钉住的 SOT 对齐 (骨架与模板不一致本身是缺陷), 且 AB 零负 delta; 只是「没有它 AI 就不写字段」这句在本仓语料下不成立, 记入 proposal 下次触碰时勘正。
4. **grader 提出的候选判别特征 (n 小, 仅记录)**: 5/5 次 with_skill 都写裸哨兵 `` > **Linked Issue**: `none` ``, 而所有产出该行的 old_skill run 都带破折号尾注 (模仿 sibling-spec-probe:6 形态)。若将来要在 ship 态里也量出 skill 边际, 可把 SC-7 断言收紧为「该行逐字 = 裸哨兵行」—— 本轮**不**事后收紧 (predict-then-measure 纪律)。

## §3 套件覆盖缺口三件套 (判据表第三行)

1. **点名行为** = SC-7: spec-drafter 新建 Level 2 proposal 时写出过 E0+E2+E5 的 `Linked Issue` 行, 无关联时逐字 `none`。
2. **可证伪定向 fixture** = `ab-suite/spec-drafter.json` 新 eval **id 3** `linked-issue-field-authoring-TARGETED` (中文臂) + eval id 2 expectations +2 (英文臂, R5/M2); `ab-suite/version.yaml` 1.2.0 程序化重算 (skills_covered 31 / total_eval_cases 74)。
3. **套件缺口 issue** = 归并 **aria-plugin#117** (类级「AB 测试集缺 authoring 维度」; 本 Spec 为第二实例; 评论 URL 见下方「#117 评论」)。

**逐 hunk 处置表 (五格)**: 见 [SUBSTITUTE.md](./SUBSTITUTE.md) §3 (模板 / 探针 / 注册 / 纯函数 走 substitute 且基线红→绿逐字留痕; hunk A/B 走本文 AB)。

## §4 过程记录

- **运行前置 `ARIA_COORDINATION_NO_PUSH=1` 不适用但已核验**: `grep -c phase1_gate aria/skills/spec-drafter/SKILL.md` = 0 (母 Spec 前置块未 ship) ⇒ 被测 skill 不可能把评测 AI 引到闸门脚本; 会话 env 该变量 UNSET; 跑前后 `git ls-remote origin refs/aria/coordination` 与本地 `refs/aria/coordination` 均为 `ab1d3e05…`, 零推送。评测 subagent 被明令禁止 git 写 / 闸门脚本 / state-scanner / openspec CLI; 全部 run 自陈只写 outputs/ 且仓内 `git status` 无其写入。
- **违约记录**: eval-3 任务 prompt 字面「不要运行 git 或任何脚本」, iteration-1 eval-3 基线 run 自陈跑了**只读** git 命令 (`log` / `branch -r` / `rev-parse` / `describe`) 并把约束解读为「git 写命令」; control eval-3 亦跑 `python3 -c` 只读校验。无仓内写入, 不影响判分, 记录在此。
- **基线污染两通道** (§1): (a) 同批改的 SOT 模板 (control 已隔离); (b) 在制 proposal 语料 (未隔离, 本仓结构性存在)。AB_TEST_OPERATIONS.md 目前只记 CLAUDE.md 污染面 (#116); 本轮把「同批 co-landing 文档 + 在制 proposal」补为第二、三类, 建议归入 #116 追记 (handoff carry-forward, 外向动作待授权)。
- **贴文证据失真** (grader claims 侧): eval-2 基线 `proposal.md:19` 的 grep「0 hits」实跑 5 命中; control eval-2 行号引用恒差 40 (88→128 等); 均不影响本 AB 判分, 记为 memory `pasted-evidence-is-derived` 的又一实证。
- **产物**: 按先例只提交 PREDICTION / RESULT / SUBSTITUTE / benchmark / eval_metadata / grading / timing / answer / proposal; skill 快照与 `ab-workspace/` (gitignored) 不入库。`ab-results/latest` 指针按近期惯例不动。
- **执行者**: 执行容器 simonfish/023236f2, 2026-09-02 07:5x–08:2x UTC; 6 + 2 executor run + 1 grader (两次), 主控不亲评。

## #117 评论 (TASK-018)

- URL: https://forgejo.10cg.pub/10CG/aria-plugin/issues/117#issuecomment-20573 (comment id 20573, `forgejo POST …/issues/117/comments` 2026-09-02)
- 回读核验 (ground-truth, 非回执): `forgejo GET …/issues/117/comments` ⇒ 共 1 条, id 20573 存在, body 含「第二实例」与 `linked-issue-field-authoring-TARGETED` = True; created_at 2026-09-02T08:18:45Z, user simonfish
- 内容: 第二实例说明 / 首条 authoring fixture (eval id 3 + id 2 更新) 登记 / 结果目录路径 / authoring eval 基线语料泄漏两通道教训
