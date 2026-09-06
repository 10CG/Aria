# GRADER_CRITIQUE — eval-2 module-identifier-validation (branch-manager)

评分结果: `with_skill` 1/1 pass, `old_skill` 1/1 pass。以下批判 eval 本身。

## 1. 恒真 / 恒假断言

本 eval 只有一条断言 —— `Should list valid module identifiers` —— 且它对**任何读过 SKILL.md 的臂恒真**, 零信息量。

- prompt 逐字是「列出支持的模块标识符」, 而 branch-manager SKILL.md 里有一个标题就叫「### 模块标识符」的现成 6 行表 (`aria/skills/branch-manager/SKILL.md:325-331`, 同 snapshot 完全一致)。任务退化成「把那张表抄出来」。
- 两臂都原样抄了同一张表 (backend / mobile / shared / cross / docs / standards), 连「说明」列的措辞都与源文件逐字相同。
- 也就是说这条断言测的是「臂有没有拿到技能文件」(with_skill vs **no_skill** 那种对照), 不是「新旧两版技能」的区分。本轮对照恰恰是 with vs old, 所以判别力 = 0。

没有恒假断言 (只有一条断言, 且它恒真)。

## 2. (a) 有没有断言碰得到那一行差异

**没有。结构性地碰不到。**

本轮两版 branch-manager 的唯一差异在 `SKILL.md:149`, 「前置: REQUIRE claim (Part A1, MUST)」段内的命令占位串:

```
- `phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory`            (old)
+ `phase1_gate.py --raw-track-id <A.1 认领时派生的那一串> --phase B --mode advisory`  (with)
```

三层都不通:

1. **触发不到**: 那段的适用条件是 `action: create` (进 Phase B.1)。本 prompt 是纯查询, 两臂都没进入建分支流程, 也就都没有场合去生成 `phase1_gate.py` 命令行 —— 占位串的可读性差异只在「AI 要填那个参数」时才可能显形。
2. **断言不问**: 唯一那条断言的语义面是模块标识符枚举, 与 claim / track-id / phase1_gate 无交集。即使某一臂偶然把命令行抄出来, 也不会被打分。
3. **回答里也确实没出现**: 对两份 answer.md grep `carry-id|raw-track-id|phase1_gate|认领|track` 全部零命中。唯一沾边的是 with_skill 结尾的免责句「本次是纯查询，我没有执行任何 git 操作，也没有创建分支或 claim」—— 但「REQUIRE claim」那一节两版**都有**且仅差占位串, 这句话不能归因到那一行改动 (它更像是回答风格差异), 而且没有任何断言碰它。

结论: 用 eval-2 给这次一行改动做 Rule #6 区分是无效的。要让那一行进入可观测面, 需要一条 prompt 真正走到 `action: create` 且**没有** active claim 的场景, 断言钉「是否生成了 `phase1_gate.py --raw-track-id ...` 命令, 且 `--raw-track-id` 的取值来源被正确理解为 A.1 认领时派生的 id (而非凭空造一个 / 直接抄占位符字面)」。当前套件里这条 eval 不该被计入区分力证据, 只能当「技能存在性」冒烟测试。

## 3. (c) 断言完全没覆盖的重要差异

两臂内容都正确、都可回溯到 SKILL.md, 但**取向明显不同**, 而这些差异全部落在断言之外:

1. **old_skill 给了 6 条一一对应的分支名示例** (`feature/backend/TASK-001-user-auth` … `feature/standards/TASK-040-commit-convention`), 每个标识符各一条; with_skill 只给 2 条 (backend / mobile)。对「照着选值」的用户, old_skill 的可操作性更强。
2. **old_skill 有选值决策规则 + 反例清单**: 「单模块改动 / 同时动到 2 个以上模块 / 只改文档 vs 改 standards 子模块」, 并点名不要自造 `api`、`web`、`fe`。with_skill 只泛说「不要自造拼接值 (如 `backend-mobile`)」。
3. **with_skill 独有的消歧: `module` 不是 `branch_type`**, 并把 branch_type 的另一组取值 (`feature`/`bugfix`/`hotfix`/`release`/`experiment`, 默认 `feature`) 列出来明说「两组不要互相代入」。这是本问题最现实的误答形态, old_skill 虽然列了三种例外格式, 但从未把它命名成一个混淆点。
4. **with_skill 独有: `in_submodule: true` 场景** —— module 取值集不变、需 `cd` 进子模块建分支、完成后回主仓更新子模块指针。old_skill 完全没提子模块。
5. **with_skill 独有: 显式声明本次无副作用** (未跑 git、未建分支、未 claim) 并说明要真正走 B.1 还缺 `task_id` + `description`; old_skill 只是问「要不要帮你建分支」。
6. **一处措辞精度差**: SKILL.md 对 `cross` 的定义是「多模块变更」(即 ≥2)。with_skill 写「同时动 backend 和 mobile 时写 `cross`」(明确 ≥2); old_skill 写「同时动到 2 个以上模块」, 字面可被读成 ≥3, 对「恰好 2 个模块」的情形有歧义。断言碰不到这类精度差。
7. **共同盲点 (两臂都没答)**: 都没说明这 6 个值是 branch-manager 自己钉死的 SKILL.md 约定、在 `backend/` `mobile/` 这类目录不存在的项目 (如 Aria 本仓) 该怎么落, 也都没提 `module` 在 §输入参数表里标 `✅ 必需` 之外是否有校验机制。断言不覆盖。

## 4. 仓内语料污染检查

**两臂都没有**引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的任何文档, 也没有引用其他 openspec 产物。

- grep `a1-entry|openspec|proposal|tasks\.md` 的全部命中只有 `experiment/openspec-pilot` 一处 (with_skill:31, old_skill:44) —— 那是 SKILL.md:320 分支命名规范表里的逐字示例, 不是仓内 Spec 引用。
- 两份回答的每一项事实都能钉回 SKILL.md 的既有段落: `:262` (输入参数表 module 取值)、`:316-320` (分支命名规范, 含 hotfix/release/experiment 格式)、`:325-331` (模块标识符表)、`:335+` (子模块操作)、`:824` (Red Flag「分支名不规范」)。无外部来源、无幻觉新增值。

即本 eval 的结果**未被仓内语料污染** —— 但这也不构成好消息: 未污染 + 恒真断言 = 一次干净的零信息测量。
