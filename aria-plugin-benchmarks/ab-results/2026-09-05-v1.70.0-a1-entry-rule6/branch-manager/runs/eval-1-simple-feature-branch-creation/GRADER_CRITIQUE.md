# GRADER_CRITIQUE — eval-1 simple-feature-branch-creation

评分结果: `with_skill` 2/2, `old_skill` 2/2。**本 eval 本轮区分度 = 0**。

---

## 1. 恒真 / 恒假断言

两条断言**都**接近恒真, 本 eval 目前是零信息量的。

**断言 1「Should generate correct branch name format」** —— prompt 已把 `module=backend` /
`task_id=TASK-001` / `description=user-auth` 三个槽位逐字交给模型, 分支名模板又写死在 SKILL.md
里, 拼装是纯机械动作; 任何能加载到技能文件的臂都会产出
`feature/backend/TASK-001-user-auth`。两臂逐字相同。

附带缺陷: 断言没写**期望字符串本体**, 也没引模板 (`{branch_type}/{module}/{task_id}-{description}`)。
"correct" 由 grader 自行判定 ⇒ 尺子在断言外面。想留这条就该写成
「输出中出现字面串 `feature/backend/TASK-001-user-auth`」。

**断言 2「Should indicate Branch mode was selected」** —— B.1.0 评分表对「单模块 / 单任务 /
无并行」这种最小任务的结果是确定性的: 只有 `risk_level=medium` 加 1 分, 1 < 3 恒为模式 A。
两臂算出的分数表逐行一致 (0/0/0/+1/0 = 1)。要让这条有信息量, 必须换一个落在阈值附近的
eval 输入 (跨目录 + 多任务), 在这个 prompt 上它永远是 pass。

结论: 这两条只能验「技能被加载了吗」, 验不了「哪版技能更好」。

---

## 2. 断言完全没覆盖的重要差异 (按重要性排序)

### 2.1 认领命令里的 track-id 从哪来 —— 恰好是本轮唯一的技能差异, 零覆盖

两臂都写了 Part A1 的 claim 前置, 但对 `--raw-track-id` 的处置**相反**:

- `old_skill` 把占位符原样抄出 (`--raw-track-id <carry-id>`), 随即自己**替它取值**:
  「(`<carry-id>` 用本任务的 carry id, 例如 `TASK-001-user-auth`」, 并在「阻断项解除后执行」的
  可执行命令块里落成 `--raw-track-id TASK-001-user-auth`。也就是**用 task_id+description 现场
  编造了一个 track-id**, 且以可复制粘贴的形态交付。
- `with_skill` 写 `--raw-track-id <A.1 认领时派生的那一串>`, 并**停下来要输入**:
  「你这次是直接从 B.1 进来的，没给 A.1 track-id。请二选一」, 选项 2 还要求「跑完在输出里标注
  『派生值，未经 A.1 确认』」; YAML 里落成 `blocking_input: "raw-track-id (A.1 认领时派生)"`。

这正是「防止 B.1 用一个与 A.1 不同的 id 去认领, 从而认领不到同一条 track」的行为面。信号**已经
出现在回答里了**, 而当前 2 条断言一条都没碰到它 —— eval 白白丢掉了本轮唯一可测的区分点。

建议补一条 (可证伪, 且两臂会分开):
> 认领命令中的 track-id 必须指明来源为 A.1 认领时派生的那一串; 不得由 task_id / description
> 现场拼造后直接落进可执行命令; 缺该输入时须索取或显式标注「派生值, 未经 A.1 确认」。

### 2.2 环境验证: 真去实测 vs 照模板复述 (方向与 2.1 相反)

- `old_skill` 实跑了仓库探查, 抓到三条硬事实: 当前不在基线分支、**本仓根本没有 `develop`
  (主干是 `master`)**、工作目录脏 (三个子模块指针 + 一个未跟踪目录), 并据此把 `base_branch`
  改成 `master`、给出 `error:` / `suggestion:` 输出块、明确「没有创建任何分支」。
- `with_skill` 只把 B.1.1 的模板命令列出来 (`git branch --show-current` / `git status --porcelain`
  / `git pull origin develop`), 没有任何实测值; 它给出的执行序列
  `git checkout develop && git pull origin develop` 在这个仓里**会直接失败**, 因为 develop 不存在
  (它只加了一句「若本项目基线分支是 main/master，按项目实际替换」的免责)。

这是两臂之间最大的实用质量差, 断言完全没覆盖。注意这条也是**本次运行的不可复现产物**:
脏工作树是当时的瞬时状态 (见 §3), 换一次跑就可能不成立, 不宜当作版本差归因。

### 2.3 .gitignore / 生态检测的实测粒度

`old_skill` 对真实 `.gitignore` (37 行) 逐条比对并给出「已有 `__pycache__/` 和 `worktrees/`,
缺 `.env`/`.env.local` 风险最高」的裁剪建议, 还判定 `ecosystem: none` 并说明依据 (仓根无
package.json / pyproject.toml 等)。`with_skill` 只把必需规则清单和「Python 就查 poetry/pip/uv」
的分支复述了一遍。同样零覆盖。

### 2.4 两臂都没有真的建分支

两臂最终都停在「等你确认」, `remote_push: "pending"`。当前断言只验「说了什么」, 不验「做了什么」,
所以两臂都 pass。若这个 eval 想验行为而非文本, 需要一条关于是否执行 / 为何不执行的断言。

---

## 3. 仓内语料污染 (`openspec/changes/a1-entry-claim-duplicate-work-guard/`)

**两臂都没有引用该目录下的任何文档。** grep `openspec` / `proposal` / `tasks.md` /
`duplicate-work` 在两份 answer.md 上均无命中 (除下述一处分支名)。两臂对 Part A1 的表述都
指向技能文件本身 (「命令模板见 phase-b-developer SKILL.md §B.0」), 不是 spec 文本。

需要点名的**相邻通道** (不是 spec 文档引用, 但同源):
`old_skill` 因为实跑了 git 探查, 把在制分支名和 AB 目录写进了回答:

- 第 52 行: `当前分支 : feature/a1-entry-claim-duplicate-work-guard`
- 第 56 行: `?? aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/`
- 第 137 行: `error: "... 当前在 feature/a1-entry-claim-duplicate-work-guard 而非基线分支 ..."`

判定: 这是**仓库运行态泄漏**, 不是 spec 文档泄漏 —— 分支名只被当作「非基线分支」这一事实使用,
没有任何行为 (含 claim/track-id 处置) 是从这个名字推出来的; 而且它出现在**没有**改动那行的
那一臂, 方向上也无法解释 §2.1 的差异。但它确认了两件事, 应记进本轮运维记录:

1. eval 跑在真仓无沙箱 (与 `reference_ab_harness_runs_in_real_repo_no_sandbox` 一致), 在制分支名
   与 AB 目录名对被评 AI 可见, 名字本身就带着「a1-entry-claim-duplicate-work-guard」这几个词;
   本轮无害, 但换成会去 `openspec/changes/` 里翻的 eval 就是直接的基线污染路径
   (`feedback_ab_baseline_leaks_via_co_landing_docs_and_repo_corpus`)。
2. 两臂看到的仓库状态是同一个脏工作树, 但只有一臂去看了 ⇒ §2.2 的差异里混着「愿不愿意实测」
   和「当时仓库恰好脏」两个因素, 单跑一次不可归因。
