---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-22T11:42:50.875Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席

审查对象: `detailed-tasks.yaml` (a136dbf) + `proposal.md` v3 (910d9fa) + `v3/` 原型与证据。侧重: 计划结构与作废关系、INV-1–7、准入门与裁定 E、`#228` 接缝、发版线、截止时间账。

实验脚本都在 `S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r1/tech-lead/`; hook 副本 `$S/base.sh` (sha256 前缀 `e83c5e30f2cc`, 即 aria v1.77.1 `68c7f65` 的 hook, `hooks/` 与 `59e333c` 零差异已核) 与 `$S/v3.sh` (`mkv3.py` 生成)。

## 审计结论

### 汇总

| # | severity | category | scope | 针对 | 一句话 |
|---|---|---|---|---|---|
| F1 | Critical | architecture | proposal 放宽面 R-a–R-c、CHANGELOG 放宽面申报、TASK-007 | proposal v3 + 任务计划 | W10「部分覆盖」的既有缺口 (count 轴等) 随放宽外延到基线按尺寸拦的大命令; 实测一条读凭据路径的命令基线拦、v3 放行, 规格未申报, 且 #217 关闭后无载体 |
| F2 | Major | architecture | TASK-003/004/005/006 依赖 | 任务计划 | 没有修复回路与作废规则, 证据不绑 hook 版本; TASK-004 不依赖 TASK-005, 审查后的修复会让验收证据过期 |
| F3 | Major | testing | TASK-001「基线红」 | 任务计划 | SC-V 用例到 TASK-002 才写, TASK-001 无法在基线上实跑它们; 该交付物没有可行的落点 |
| F4 | Major | testing | TASK-004 acceptance | 任务计划 | 阈值 136/137 与证据 (137/137) 不符; 「不低于」对多放行失明; 只给放行限时, 迟到的拦截不受约束; 判据要的分段计时 W12 根本没记 |
| F5 | Major | testing | SC 表、BI 清单、TASK-003 | proposal v3 + 任务计划 | 三个像真实执笔错误的坏实现没有任何用例能抓 (截止漏 min(…,3)、作业结束后不杀计时器、准入门只看 EPOCHREALTIME 有无); 「至少一条用例变红」允许误命中 |
| F6 | Major | testing | SC-V3、SC-V6、INV-7 | proposal v3 + 任务计划 | BI-13 的 e2e 检出依赖夹具组成与宿主速度, 规格没钉; 套件里的时延断言与 INV-7 没有对齐 |
| F7 | Major | documentation | INV-6、TASK-002/006/007 | 任务计划 | 关键词核对只落在 TASK-007; 发版推送与 PR 描述不查; 名单式禁止 (3 张) 而非白名单, #228 / 残余 issue 等不受保护; 不核验 #217 的实际状态 |
| F8 | Major | architecture | 阶段 C/D | 任务计划 | 关单前没有上线后运行时复验 (插件缓存更新 + 新会话), 也没有认领释放、归档、周期 handoff (WP-A TASK-012/013 先例) |
| F9 | Major | documentation | `rule6_note` | 任务计划 | 单块 `decision_table_row: n/a` 与 note 里对 AI 可见 hunk 按 §2 第 1 行判定自相矛盾; `longline` 模板含祈使指令行, 按 WP-A 先例不属第 1 行; 「逐字复用」没有断言钉住 |
| F10 | Minor | implementation | W8 `_sg_relax_run` 的 `2>/dev/null` | 原型 | 只有赋值的命令后接重定向, 不作用于命令替换本身 (5.2 与 3.2 实测); 计时器 fork 检查那条 `kill` 的报错会出现在回落文案之前 |
| F11 | Minor | implementation | W8 `_sg_relax_run` 的 `wait` 之后 | 原型 | 组长先退出、组员仍占管道时, 截止失效 (实测截止 1 s, 3.31 s 才返回); 现有代码路径到不了, 一行可加固 |
| F12 | Minor | implementation | 准入门 `_sg_relax_ok` | 原型 | `OSTYPE` 与 bash < 5 下的 `EPOCHREALTIME` 都可由父进程环境改写 (实测); 裁定 E 与 P2 不是结构保证 |
| F13 | Minor | architecture | 准入门扩展探测、`_sg_vx_big_judge` | proposal v3 + 原型 | 两处「判不出就走宽松分支」: 扩展探测出错等于没有扩展; 最长行测量失败时 max 留在 0, 走带 credit 的普通判定 |
| F14 | Minor | documentation | What 3 耗时上界、INV-7 | proposal v3 + 任务计划 | 时间账漏了锚点之前、扩展探测、计时器启动三项; 「与负载无关」说过头 |
| F15 | Minor | documentation | INV-1、INV-2 | 任务计划 | INV-2 与 TASK-001/003/004 自己的交付物冲突; INV-1 与 TASK-002「以补丁为准」各有一种读法 |
| F16 | Minor | documentation | TASK-006、Impact | 任务计划 + proposal v3 | 发版线已到 v1.77.1; 同步面要按最新一次发版重新列; 版本号与本地 master 新鲜度要在合并前重核; standards 三处计数没有验收落点 |
| F17 | Minor | testing | TASK-002/003/004 遗漏项 | 任务计划 | 处置 A22 (locale 用例用 C.UTF-8 并断言字符集) 没进 TASK-002; TASK-004 的语料前置没写; TASK-003 的耗时矩阵不在 INV-7 之下, 13 次整套件的成本没约束 |
| F18 | Minor | documentation | R-c、SC-V9 | proposal v3 | 放宽重跑里还能出现 TMAX 文案, R-c 与 CHANGELOG 没列; SC-V9「直调」没说是否走放宽路径 |
| F19 | Minor | testing | TASK-002 acceptance (bash 3.2) | 任务计划 | 只在 bash 5 生效的 SC-V 用例在 3.2 下怎么算没定, 与 SC-13 双值计数可能打架 |
| F20 | Minor | documentation | TASK-001 的 `#228` 留言 | 任务计划 | CHANGELOG 把「≤ 8192 单次判定可超 5 s」归给 #228, 但留言内容只写 Decision 12, 这条残余没有落到载体 |

### 已核实成立的部分 (不出 finding)

- `mkv3.py` 在当前 aria master 上逐字复现 `W8-v3.diff` (`$S/w8-regen.diff` 与之 `cmp` 相同)。
- `run-w10-w11.sh` 在 scratch 副本复跑 (负载 1.34–1.64): W10 16/16 PASS、残留 0; W11 结局与入库版本逐项相同, 回落墙钟 3.01–3.04 s。`w10b.sh`: P6 四次 IDENTICAL, P10 三项符合预期。`commentsync.py` baseline 模式 GREEN, 对原型跑 target 模式 RED (22)。
- 组杀覆盖面 (`$S/pg-exp.sh`): 作业里的命令替换、管道、heredoc 内命令替换都留在作业的进程组 (E5 实测 pgid 相同), 截止 1 s 时都在 1.00 s 返回, 残留 0。只有主动 `setsid` 的子进程能逃出 (E4, 4.41 s), 判定代码不会这样做。
- 作业自己 SIGSTOP (`$S/stop-exp.sh stop`): 1.00 s 返回 4, 没有挂死。我原本预测 `wait` 在 job control 下会因停止而提前返回, 实测不成立, 撤回。
- P1 由结构保证: 新增分支只在 `_SG_RELAXED` 已设或两个触发点内生效; 不在基线拦的命令到不了 `_sg_relax_ok`; 新全局变量与基线无重名。
- 原型 `_sg_relax_run` 在作业正常结束后会清掉计时器 (安静 1.5 s 后复测, 无残留)。

### F1 — Critical — W10 部分覆盖的既有缺口随放宽外延, 未申报, 关单后无载体

- type: issue | category: architecture | scope: proposal `:371-378` (放宽面)、`:434`、`:442` (CHANGELOG 标题与放宽面申报)、`:386`、`:484` (Decision 13); 任务计划 TASK-007 (`detailed-tasks.yaml:118`) | 针对: proposal v3 + 任务计划
- 摘要: 基线的尺寸上限顺带挡住了「count 轴」这类既有 fail-open (第 17 个赋值、每个变量第 9 个引用、第 9 个 for 不收集也不代入, hook `:583`、`:639`、`:687`、`:624`、`:655`)。放宽之后, 这些大命令改为「完整判定」, 而判定在 count 轴触顶时并不完整, 于是一条基线拦、确实读凭据路径的命令被 v3 放行。规格逐个点名了放宽后覆盖面变大的缺口 (#139、#142、#229、#230, `:376`, CHANGELOG `:442`), 唯独没有 count 轴; CHANGELOG 标题写「不新增 fail-open」(`:434`), 而 proposal 自己在 Decision 13 把 count 轴称为 fail-open。count 轴目前唯一的记录在 #217 正文「相关 (count 轴同款 fail-open, 建议暂不改)」, TASK-007 关闭 #217 之后它就没有开着的载体。
- 证据: `$S/count-axis.sh` (路径运行时拼装, hook 只判文本, 不执行命令)。命令为 `F=<forgejo app.ini 路径>; { echo $F×8; cat $F; }` 加约 9.4 KB 良性短行:

  ```
  small, base: rc=0          (count 轴缺口, 基线已有)
  small, v3:   rc=0
  big,   base: rc=2  oversize ("the command is longer than ...")
  big,   v3:   rc=0          <- 新版放行, 基线拦, 读的是凭据路径
  ctl,   v3:   rc=2  finding (同一大命令, 读取放在第 1 个引用)
  ```

  post_spec R1、R2 汇总都没有涉及这一点 (已 grep)。
- 定级理由: 任务书把「新版放行、基线拦、确实读到凭据、规格没有申报」列为安全退化。这一例四项都满足; 而且裁定 A 的原文是「完整判定后按结果判」, count 轴触顶的判定并不完整, 不在 A 的字面范围之内。攻击者的能力没有增加 (小命令形态基线本来就放行), 所以修法不需要换机制。
- 建议 (二选一, 属 owner 姿态决定, memory `failopen-posture-owner`: 旧裁定延伸到新的命令类就是新决定。应在 TASK-002 开工前上呈):
  1. 申报: proposal 放宽面增加一条 R-d, 写明「W10 部分覆盖的既有缺口 (count 轴、单层链式、collect 认不出的值形状) 随放宽外延到基线按尺寸拦的大命令」, 并附这一例; CHANGELOG 放宽面申报同步, 标题里的「不新增 fail-open」改成准确表述; TASK-001 为 count 轴开残余 issue (或明确挂到某张开着的 issue), TASK-007 对账写「转 #NNN」, 不写「不变」。
  2. fail-closed 微调 (只在 `_SG_RELAXED` 下生效): `_sg_vx_collect` 数到 16 仍有可收集项、`_sg_vx_apply` 的 guard 到 8 仍有引用、`_sg_vx_replace` 的 g 到 8 仍有命中时返回 3, 回落基线拦。由 TASK-004 在 W12 上量收益损失。
  - 两种都要补 SC 与 BI (例如 SC-V1/P9 增加「count 轴触顶的大命令」形状)。

### F2 — Major — 修复回路、作废规则、证据与 hook 版本的绑定都缺

- type: issue | category: architecture | scope: `detailed-tasks.yaml:71`、`:83`、`:96`、`:105`; INV 清单 | 针对: 任务计划
- 摘要:
  1. TASK-003 与 TASK-005 都只依赖 TASK-002, 两者都可能要求改 hook 或套件, 但计划没写谁来改。TASK-002 的 reason 写了「主控不亲写 hook 码」, 修复却没有指定执笔人。
  2. TASK-004 依赖 TASK-003, 不依赖 TASK-005。TASK-005 在 TASK-004 之后提出 Major, 修复后 W14 就是旧版本的证据, TASK-006 仍会放行。
  3. 没有作废规则: hook 改动之后, TASK-003 的 BI 是「旧好实现 + 改动」, 补丁可能已经打不上或者语义变了; 套件改动之后, W9 类证据过期。
  4. 证据不绑版本: W9 页眉记了 `v3 hook sha256 3eb4389103e8`, 是好做法, 但计划没要求 W13、W14 记录实现 hook 与套件的 sha256, TASK-006 也不核对「发版的 hook = 证据里的 hook」(memory `pasted-evidence-is-derived`)。
  5. 发版线上还可能有并发轨改 `hooks/secret-guard.sh`。TASK-001 的重锚只在入场做一次。
  6. TASK-005 的验收「无未处置的 Critical / Major」没说谁有权处置; Critical 若不修, 应交 owner。
- 建议: 顺序改为 002 → 005 → 修复 → 003 → 修复 → 004 (最后跑, 在冻结的 sha 上) → 006。若保留 003 与 005 并行, 就新增 INV-8:「W13 / W14 页眉记录 hook 与套件的 sha256; 003 开工之后 hook 或套件有任何改动, 受影响的 BI 与整个 004 都重跑; 006 断言发版提交里 hook 的 sha256 = W14 页眉; 合并前 aria master 若动过 `hooks/`, 就 rebase 并重跑 002 与 004 的验收」。修复一律回到执笔席 (同一实例或新实例)。另加停止规则: 同一任务修两轮仍有 Major, 就上报 owner (memory `stop-adding-rounds`)。

### F3 — Major — TASK-001 的「基线红」在计划里做不出来

- type: issue | category: testing | scope: `detailed-tasks.yaml:44`、`:46`; proposal `:490` | 针对: 任务计划
- 摘要: TASK-001 (主控) 要求 SC-V2–V5、V7、V8、V10「在基线上实跑为红」并逐条记录, 但这些用例要到 TASK-002 才由执笔席写出。按现在的顺序, TASK-001 的验收「基线红 / 绿逐条记录」没法满足, 只能留空或用别的东西顶替。另外:
  1. SC-V6 与 SC-V2 的 bash 3.2 e2e 在基线上是自己和自己比, 恒绿, 不能算回归闸;
  2. SC-V11 (新函数在闸门之上) 与 SC-V12 (注释清单 target 模式) 在基线上是红的, 清单却漏了。
- 建议: 把「基线红」挪到 TASK-002, 按 TDD 做: 先写 SC-V 用例, 在基线 hook 上跑, 逐条记录红绿, 再落 hook。也可以放进 TASK-003 作为 BI-0: 新套件对基线 hook 必须在 SC-V2–V5、V7、V8、V10、V11、V12 上为红。TASK-002 体量很大 (约 35–40 条新用例 + 6 组改写 + 注释同步), 可以拆成 002a (套件与基线红) 和 002b (hook 落地), 让每块回到 4–8 h 的粒度。

### F4 — Major — TASK-004 的验收判据

- type: issue | category: testing | scope: `detailed-tasks.yaml:86-88` | 针对: 任务计划
- 摘要:
  1. 「放行数不低于原型 (136/137)」与证据不符。W12 与 W12b 都是 size 类 137/137 放行, VMAX 那 1 条拦 (`W12-real-traffic.txt`、`W12b-rerun.txt`)。照现在的写法, 实现少放行一条也算过。
  2. 「不低于」是单边判据。一个把 VMAX 那条也放行的坏实现 (BI-8 一类) 是 138 ≥ 137, 照样过。
  3. 只约束「越界的放行」。迟到的拦截 (回落) 不受约束; 回放里一条 6 s 后才拦的命令, 到了生产就是 Claude Code 5 s 超时后的 fail-open, 这恰恰是最危险的方向。
  4. 判据要的「首遍 + 基线前段」逐条数据, W12 的管线没有产出: `run-w12.sh` 把未埋点的 `v3.sh` 交给 `replay138.sh`, 所以 `W12-replay-138.tsv` 第 5–7 列 138 行全是 `-` (已核)。照「其余不变」重跑, 判据的输入不存在 (memory `verify-predicate-inputs-exist`)。
  5. W9、W10、W11 的重跑判据不在验收里, 包括 P1 的套件级证据「旧套件在实现上恰好只有 21ab、21ac、21ag、21aj、21al、21ao 失败」。
  6. 脚本输出写死在 `$HERE/W9…W12*.txt`, 照「其余不变」改成接收实现路径, 会原地覆盖 proposal 引用的原型证据, 却产不出 W14。
- 建议: 判据改为:
  - 逐条结局对照 `W12-replay-138.tsv`。允许的差异只有「放行 ↔ 基线回落」这一种时间型差异; VMAX 那条必须仍是 oversize (value)。放行数按负载 < 2 时实测。
  - 所有结局 (不只放行) 的墙钟 ≤ max(同时段同命令的基线墙钟, 3 s) + 0.3 s。基线墙钟由同一窗口内回放基线 hook 取得, 或者改用 `mkdbg.py` 埋点版。
  - 补上 W9 (旧套件失败集合 = 原型) 与 W10 16/16、W11 结局逐项相同。
  - 脚本增加输出路径参数, 全部写进 W14, W8–W12 不动。

### F5 — Major — BI 清单与 SC 的覆盖缺口

- type: issue | category: testing | scope: proposal SC 表 `:403-416`; `detailed-tasks.yaml:73-76` | 针对: proposal v3 + 任务计划
- 摘要: 下面三个坏实现都像真实的执笔错误, 但没有任何 SC 能抓:
  1. 截止漏了 `min(…, 3)` (`cap=$_SG_TIME_BUDGET`)。没有用例用预算 4。CHANGELOG `:441` 明说「设为 4 时截止仍封顶 3 s」, 这是没有测试的行为声明; 截止变成 4 s, 把 5 s 之前的余量从约 2 s 压到约 1 s。
  2. 作业结束后不杀计时器 (删掉 W8 `:158`)。实测 (`$S/v3-notimerkill.sh` + `$S/stop-exp.sh timerkill`): 返回 0 之后 `sleep 0.999946` 仍在运行, 到点还会对已回收的 pgid 发一次 KILL。SC-V5 按桩进程的精确参数数残留, 看不到计时器那条 `sleep`。
  3. 准入门只看 `EPOCHREALTIME` 是否非空, 不看 bash 版本。实测 (`$S/gate-env.sh`): bash 3.2 继承一个 `EPOCHREALTIME` 时准入门 OPEN。3.2 下作业随后因 `$BASHPID` 未定义而回落, 是碰巧安全; bash 4.x 有 `BASHPID`, 截止会锚在一个冻结的时钟上, 结果是「作业启动 + 3 s」而不是「hook 启动 + 3 s」(4.x 未实测, 按代码推得)。SC-V2 没有这一项。
  - 另外两点: TASK-003 的验收「每个 BI 至少让一条用例变红」允许误命中, 例如 BI 改动碰到注释同步或计数检查而变红; BI-1–13 全部由规格作者列出, qa 席只负责实现它们 (memory `adversarial-fixture`: 坏态要由非作者独立构造)。
- 建议: 增补 BI-14 (cap 漏 min)、BI-15 (不杀计时器)、BI-16 (准入门不看 bash 版本), 对应用例分别为: SC-V3 直调「预算 4、`_SG_P0`=now → `_SG_LEFT` ≤ 3.000000」; SC-V5「S1 放行返回后 0.1 s 内, 以计时器 pgid 或父链精确识别, 无计时器进程」; SC-V2「bash 3.2 + 导出 `EPOCHREALTIME` → 不放宽」。TASK-003 验收改为「每个 BI 让规格 SC 表为它点名的那条 SC 变红 (W13 逐条记录变红的用例名)」, 并要求 qa 席至少自拟 3 个清单外的坏实现。

### F6 — Major — SC-V3 与 BI-13 的检出依赖夹具与宿主; 时延断言与 INV-7 没对齐

- type: issue | category: testing | scope: proposal `:407` (SC-V3)、`:410` (SC-V6); `detailed-tasks.yaml:30-31` (INV-7) | 针对: proposal v3 + 任务计划
- 摘要:
  1. BI-13 (锚点设在 `_sg_per_segment_eval` 入口) 只有在「首遍够长、并且放宽重跑也够长」时才和好实现分得开。f5like 首遍便宜, BI-13 也只是约 3.1 s, 低于 3.3 s, 抓不到。「首遍约 2 s 的形状」没写放宽重跑需要多长; 放宽判定若在 0.5 s 内完成, 两种实现同为约 2.5 s 放行, 也抓不到。首遍时长还随宿主速度变化, 换一台快一倍的机器, 余量就没了。
  2. e2e 阈值 3.3 s 的余量约 0.27 s (W11 实测 3.01–3.04 s)。INV-7 要求时档测量只在负载 < 2 时做, 可套件在 CI 和任意负载下都会跑, 计划没说这几条时延断言是否受 INV-7 约束。
  3. SC-V6「会回落的输入」靠截止触发 (apply-heavy-cjk、f5like), 在更快的宿主上可能判完而不回落, 断言就会因错误的原因变红。规格也没要求整串与分段两种模式都覆盖。
- 建议: BI-13 加一条结构断言 (归入 SC-V11): `_SG_P0=` 只在 `set -uo pipefail` 的下一行赋值一次, `_sg_relax_left` 只读 `_SG_P0`, 这条与宿主无关。e2e 保留作二道闸, 阈值改为相对值: v3 墙钟 ≤ max(同次跑的基线墙钟, 3 s) + 0.5 s。SC-V6 用预算 1 s, 配放宽判定 ≥ 5 倍截止的输入, 两种模式各一条。时延类用例在输出里记录负载。

### F7 — Major — INV-6 的核对时点与名单形式

- type: issue | category: documentation | scope: `detailed-tasks.yaml:28-29`、`:105-109`、`:117-119` | 针对: 任务计划
- 摘要:
  1. 关键词核对只写在 TASK-007。TASK-002 的提交、TASK-006 的 aria 合并提交与版本提交、主仓 gitlink 提交、PR 描述都不查。最容易误写的地方恰恰是 aria 仓的提交: 在 aria-plugin 仓里, 裸写的 `#217` 就是本 issue, 带关闭关键词推到 master 会直接关掉它, 那时 TASK-007 的对账还没做。
  2. INV-6 是禁止名单 (#154、#203、Aria#221), 外加一个允许项。#228、#139、#142、#229、#230 和两张新残余 issue 都不受保护, 而它们正是残余的载体 (memory `invariant-needs-failclosed-default`: 枚举分区要用 fail-closed 白名单)。
  3. 没有用 GET 核验状态: 不查 TASK-006 之后 #217 仍是 open, 也不查 TASK-007 之后 #217 已关闭。主仓提交里的跨仓关闭关键词在 Forgejo 上是否生效, 本席没有核实。
- 建议: INV-6 改成白名单:「除 TASK-007 的主仓提交对 10CG/aria-plugin#217 外, 所有提交信息与 PR 描述对任何 issue 只写 Refs」。TASK-002、006、007 每次推送前机械核对, 例如 `git log --format=%B <range> | grep -niE '(close|fix|resolve)[a-z]*[[:space:]:]+[^[:space:]]*#[0-9]+'`, PR 描述走 API GET。TASK-006 验收加「GET #217 state=open」, TASK-007 验收加「GET #217 state=closed」; 关键词没生效时用 API 关闭, 并在对账评论里链接该提交。

### F8 — Major — 阶段 C/D 不完整: 缺上线后复验、认领释放、归档、handoff

- type: issue | category: architecture | scope: `detailed-tasks.yaml:100-120` | 针对: 任务计划
- 摘要: hook 的改动要等插件缓存更新、会话重启之后才在生产生效。计划在发版 (TASK-006) 之后直接关 #217 (TASK-007), 中间没有运行时复验。本计划继承 INV 的 WP-A 有 TASK-012「post-ship 复验 (owner 更新插件缓存并重启会话后在新会话执行)」, 关单任务 TASK-013 依赖它 (`openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml:235-258`)。本计划把这一步丢了 (memory `completion-signals-vs-runtime-invocation`)。TASK-007 也没有认领释放、`openspec-archive`、周期 handoff (Rule #9)。
- 建议: 在 006 与 007 之间加 TASK-006b (owner 门): owner 更新插件缓存并重启, 新会话跑 `plugin-cache-currency`, 再跑一条大而良性的真实命令 (基线拦、新版放行) 作活体复验, 通过后才关单。TASK-007 补上认领释放 (phase1_gate)、D.2 归档、周期 handoff 落 `docs/handoff/`。

### F9 — Major — `rule6_note` 的形式与判定

- type: issue | category: documentation | scope: `detailed-tasks.yaml:8-14`; proposal `:429`; SOT `standards/conventions/skill-benchmark-exemption.md` §1、§2、§3、§4.1 | 针对: 任务计划
- 摘要:
  1. 形式自相矛盾。五个字段是一块 `decision_table_row: n/a` (§4.1: 本 spec 不属 Skill 变更), note 却又对 AI 可见文案 hunk 适用「SOT §2 row 1」。WP-A 的先例是分两块: 块 A 是代码 (n/a); 块 B 是 AI 可见文本 hunk, 填 `decision_table_row: 1` (`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md:315-345`)。
  2. 判定依据不足。WP-A 把块 B 判为第 1 行的前提是「不含任何指示行为的措辞」。本次 `longline` 模板含「Split it into smaller commands …」加两条祈使 bullet, 以及中文「请拆成更小的命令」。逐字复用不改变它们的处方性质 (SOT §1: 按内容判, 不按目录判)。按 §2,「拿不准」应照跑; 而 AB 套件对 hook 零覆盖, 照跑等于测量剧场, 所以诚实的落点是第 3 行, 并满足 §3 的三条 (点名行为、可证伪的定向 fixture、开套件缺口 issue)。至少要像 WP-A 那样标「AI 自作主张、待 owner 复议」。
  3. 「逐字复用」没有被钉住。SC-V7 只钉首行与 `Matched pattern:` 行; 已核实 `longline` 的指令块 = oversize 指令块去掉「do not repeat one long $VAR」那一行, 但没有任何断言会在指令行被改动时变红。
  4. 一个观察 (不单独定级): 路由变化让基线按尺寸拦的大命令现在看到普通命中文案, 里面有「Acceptable filters」和 `# guard:ack` 指引, AI 下一步的行为会随之改变。这条应在 rule6_note 里点名。
- 建议: 拆成块 A (代码、套件, n/a) 与块 B (`longline` 模板与两条增长原因串, 第 1 行或第 3 行二选一, 并写明理由与「待 owner 复议」)。新增断言:「`longline` 文案的 Split 段与 oversize 文案对应各行逐字节相同」, 作为可证伪锚点。

### F10 — Minor — 原型里 `out="$(…)" 2>/dev/null` 的重定向不作用于命令替换

- type: issue | category: implementation | scope: `W8-v3.diff:151-159` (proposal `:251-259`) | 针对: 原型
- 摘要: 只有赋值的简单命令后接的重定向, 不作用于赋值里的命令替换。bash 5.2 与 3.2 实测: 命令替换里写到 stderr 的内容和 `kill` 的报错都直达调用者的 stderr。原型里唯一没加重定向的是计时器 fork 检查那条 `kill -KILL -- "-$jp"` (`:156`)。作业已经退出时 (例如自检失败、立即返回 9), 它的「No such process」会出现在回落文案之前, P6 在这条路径上不成立。只有 fork 失败时才会走到。
- 建议: 改为 `{ out="$( … )"; } 2>/dev/null`, 或在命令替换开头 `exec 2>/dev/null`, 并给 `:156` 的 `kill` 加重定向。照 INV-1, 这是原型与规格意图 (静默) 冲突, 上报后改。

### F11 — Minor — 组长先退出时截止失效 (潜在)

- type: risk | category: implementation | scope: `W8-v3.diff:157-158`; proposal P5 `:364` | 针对: 原型
- 摘要: `wait "$jp"` 返回后, 原型先杀计时器。若此时作业组里还有成员持有管道 (组长已退出), 就再也没有人杀它, 外层命令替换会一直等它结束。实测 (`$S/leader-exit.sh`, 桩里留一个进程替换子进程): 截止 1 s, 3.31 s 才返回 2。现在的判定路径不含 `&` 或 `<( )`, 到不了这里; 但 P5「作业结束后没有残留进程」靠的是「代码里恰好没有异步结构」, 不是机制。SC-V5 的桩是 `sleep & wait` (组长会等子进程), 覆盖不到这个形状。
- 建议: 在 `wait` 之后、杀计时器之前加 `kill -KILL -- "-$jp" >/dev/null 2>&1`。这与既有竞争窗口同级, 回收后 pgid 只有在组里已无成员时才可能被复用。SC-V5 增加一个「组长先退」的桩。

### F12 — Minor — 准入门的平台与版本条件可被继承的环境改写

- type: risk | category: implementation | scope: `W8-v3.diff:7`、`:136`; proposal What 1 `:73-74`、P2 | 针对: 原型
- 摘要: 实测 (`$S/gate-env.sh`): bash 5.2 下, 父进程导出的 `OSTYPE=darwin23` 胜过 bash 自己的值 (反过来, 非 Linux 平台上导出 `linux*` 就能让准入门打开); bash 3.2 继承的 `EPOCHREALTIME` 让准入门 OPEN (见 F5 第 3 点)。macOS 没有 `/proc`, 自检会回落, 是安全的; MINGW64 有 Cygwin 的 `/proc`, 未实测。这两种情形都需要异常的环境, 不在命令文本威胁模型之内, 所以定 Minor。但裁定 E 和 P2 的「与基线逐字节相同」靠的是可改写的变量。
- 建议: `_sg_relax_ok` 加 `(( BASH_VERSINFO[0] >= 5 ))`。`BASH_VERSINFO` 只读, 不会从环境导入。平台改为免 fork 读 `/proc/sys/kernel/ostype` (= `Linux`), 或者在触发点 fork 一次 `uname -s`, 触发点本身就少见。

### F13 — Minor — 新代码里两处「判不出就走宽松分支」的默认值

- type: risk | category: architecture | scope: proposal What 1 `:76`; `W8-v3.diff:138`、`:119-123` | 针对: proposal v3 + 原型
- 摘要:
  1. 准入门用 `$( _sg_ext_entries 2>/dev/null )` 为空来认定「没有扩展」。读取出错 (fork 失败、文件读取中途被改、校验失败) 同样是空, 于是放宽。基线对这类命令无论扩展状态如何都拦, v3 在扩展出错时可能放行一条读扩展所列路径的命令。这是把扩展「出错即不生效」的既有姿态延伸到一个新的判定点, 按 memory `failopen-posture-owner` 应知会 owner。
  2. `_sg_vx_big_judge` 的 here-string 建不出来时 (临时文件失败), 循环不执行, `max` 留在 0, 走带 credit 的普通判定, 违反裁定 C。持续性失败时 `_sg_line_match` 同样会失败、没有 credit, 结果仍是拦; 只有瞬时失败才有影响。
- 建议: 准入门改成「扩展文件存在就不放宽」(`[[ -e "$root/.aria/secret-guard.paths" ]]`, 失败方向是拦, 也省掉 wc/tr/cmp/sed 的 fork)。`_sg_vx_big_judge` 用一个便宜的完整性检查: 累计各行长度 + 1 应等于 `${#1} + 1`, 不等就按长行处理。

### F14 — Minor — 截止时间账漏项; INV-7 措辞

- type: issue | category: documentation | scope: proposal `:269`、`:275`、P3 `:362`; `detailed-tasks.yaml:31` | 针对: proposal v3 + 任务计划
- 摘要: 完整的账从 Claude Code 拉起进程算起: T_pre (到 `:178` 赋锚点为止) + T_fp + T_front + T_gate (准入门的扩展探测, 无扩展文件时 1 次 fork, 有扩展文件时约 8–9 次, 无 `CLAUDE_PROJECT_DIR` 时另加 jq) + T_job (≤ 截止 − 当前 + δ, δ 为计时器 fork 加 exec `sleep` 的延迟) + T_post (回落文案: fork cat 与 sed)。上界是 T_pre + max(T_fp + T_front + T_gate, cap + δ) + T_post, cap = min(预算, 3)。距 5 s 的余量约为 2 s − T_pre − δ − T_post, 正常不到 0.1 s。proposal 只写了「max(首遍 + 基线前段, 截止) + 几毫秒」, 漏了 T_pre、T_gate、δ。INV-7「硬截止是绝对上界, 与负载无关」只对截止那一项成立; 首遍与前段随负载变化, 和基线一样。
- 可越界的路径 (都不由命令文本触发): 首遍加前段 ≥ 5 s (#228, 基线同样越界); F11 的组长先退; F12 的 bash 4.x 加继承锚点; F5 的 cap 漏 min。
- 建议: 在 What 3 要点里写明这条完整的账与四条越界路径; INV-7 改为「截止那一项与负载无关; 首遍与前段与基线一样随负载变化」。

### F15 — Minor — INV-1、INV-2 与任务自身冲突

- type: issue | category: documentation | scope: `detailed-tasks.yaml:18-21`、`:57`、`:46`、`:72`、`:84-86` | 针对: 任务计划
- 摘要: INV-2 把改造面限定在 hook、套件、CHANGELOG、standards 三处计数与 TASK-006 同步面。可是 TASK-001 要改 proposal (写入 issue 号), TASK-003/004 要写 `.aria/notes/…/W13、W14` 并改证据脚本, TASK-005 要写 `.aria/audit-reports/`, 都在 INV-2 之外。INV-1 说「冲突时以 Spec 为准」, TASK-002 说「以 mkv3.py 的补丁为准逐字落地」; 遇到 F10–F12 这类原型与规格意图不一致的情形, 执笔席有两种读法。
- 建议: INV-2 限定为「aria 子模块内的改造面」, 另列主仓允许的证据、规格、审计文件。TASK-002 改成「以补丁为起点逐字落地; 与规格文字或意图冲突时停下, 按 INV-1 上报」。

### F16 — Minor — 发版线与 TASK-006 的细节

- type: issue | category: documentation | scope: proposal `:420`、`:428`; `detailed-tasks.yaml:7`、`:105-109` | 针对: 任务计划 + proposal v3
- 摘要: aria 已在 v1.77.1 (`68c7f65`, `hooks/` 未变), proposal 仍写「基线已是 v1.77.0」「照 v1.77.0 的实际改动列全」。版本号若与并发轨同值, 合并时会静默合成 (memory `same-value-merge-silent`)。本地 master 新鲜度在合并前没有断言 (memory `stale-local-main`)。standards 三处计数与 SC-V12 的跨仓部分, 套件断言不了 (SC-13 注释自己写着「跨仓, 不在本 test 内断言」), TASK-006 的验收里也没有。双推的 `ls-remote` 核验没列出三个仓 (aria、standards、主仓)。
- 建议: TASK-006 增加以下几步: 合并前 fetch, 断言本地 master = origin = github; 按最新一次发版提交重新列同步面; 版本号取「当时最新 + 1」并 grep 全仓确认; 用 grep 核对 standards 三处计数 = 实跑数; 三个仓都逐个 `ls-remote`。

### F17 — Minor — 计划遗漏的几项

- type: issue | category: testing | scope: `dispositions.md:68` (A22); `detailed-tasks.yaml:56-63`、`:74-76`、`:86-87` | 针对: 任务计划
- 摘要:
  1. R2 处置 A22「涉及 locale 的用例用 C.UTF-8 并先断言字符集 (TASK-002)」没有进 TASK-002 的 design。
  2. TASK-004 的 W12 需要按 W0 的 sha256 重抽语料 (`extract.py` + `refreeze.py`), 这是会话级前置, 计划没写。
  3. TASK-003 的对抗耗时矩阵是时档测量, 没有写负载与串行要求。13 个 BI 若各跑一次整套件 (约 12 分钟一次), 共约 2.6 小时 CPU, 与共享宿主的纪律冲突。
- 建议: 把 A22 写进 TASK-002。TASK-004 加前置「语料已按 W0 复原, `TRAFFIC_DIR` 已就位」。TASK-003 写明: 耗时矩阵受 INV-7 约束; 每个 BI 只跑相关的 SC-V 子集, 整套件只对好实现跑一次。

### F18 — Minor — R-c 漏了 TMAX 文案; SC-V9 的「直调」有两种读法

- type: issue | category: documentation | scope: proposal `:375`、`:441`、`:413` | 针对: proposal v3
- 摘要: 放宽重跑里分段副本可以超过 8192, 所以 `spent` 超过 65536 时会以 TMAX 文案拦。基线对同一条命令给的是 SMAX 文案。R-c 与 CHANGELOG「行为变更」只列了增长、`longline`、普通命中三种文案。SC-V9「TMAX 直调廉价形状」没说是在 `_SG_RELAXED` 下直调, 还是走基线路径; 要抓「放宽重跑里也放宽 TMAX」这类坏实现, 必须走放宽路径。
- 建议: R-c 与 CHANGELOG 补上 TMAX 文案; SC-V9 写明「在 `_SG_RELAXED=1` 下直调 `_sg_vx_pass`」。

### F19 — Minor — 只在 bash 5 生效的用例在 bash 3.2 下如何计数

- type: issue | category: testing | scope: `detailed-tasks.yaml:63`; 套件 `:3221-3228` (SC-13) | 针对: 任务计划
- 摘要: 在 3.2 下 `_sg_relax_run` 一律立即返回 4, 所以 SC-V3/V4/V5/V7/V8/V10 的直调用例要么改成断言 3.2 下的预期, 要么跳过。跳过会让实跑数在 5.2 与 3.2 之间不同; SC-13 只接受「N 或无 zsh 时的 M」两个值, 就会在其中一边恒红。CHANGELOG 先例「825 (无 zsh) … bash 3.2.57 + 5.2」说明 3.2 下的计数必须对得上。
- 建议: 写明 bash < 5 下这些用例断言「不放宽: 返回 4, 或与基线逐字节相同」, 用例数不变, 不靠 SKIP。

### F20 — Minor — `#228` 留言应带上 TL2-F5 这条残余

- type: issue | category: documentation | scope: `detailed-tasks.yaml:40`; proposal `:383`、`:443` | 针对: 任务计划
- 摘要: CHANGELOG 草稿把「≤ 8192 的副本单次判定可超 5 s (TL2-F5, 基线 e2e 7–19 s 后放行)」归到「#228 及新开残余 issue」, 但两张新残余 issue 是 for 列表与 heredoc 收集, TASK-001 给 #228 的留言也只写 Decision 12。这条已知的 fail-open 因此没有落到任何载体 (memory: 有记录不等于有路由)。评论 28512 第 2 点 (扩展整串口径) 在 TASK-007「写明残余」后也随 #217 关闭。
- 建议: TASK-001 的 #228 留言加上 TL2-F5 的形状与证据位置; 扩展整串口径与 F1 的 count 轴一样, 在关单前确认有开着的载体。

## Verdict

**FAIL** — 1 Critical (F1)、8 Major (F2–F9)、11 Minor (F10–F20)。

F1 不要求换机制, 修法是「申报 + owner 姿态裁定 + 载体」或者「放宽重跑里 count 轴触顶就回落」二选一, 应在 TASK-002 开工前定。F2–F4 主要是计划层面的顺序、判据与证据绑定, 改的是 `detailed-tasks.yaml`, 不碰设计。

## 轮次记录

- 读了: 任务书; `detailed-tasks.yaml` 全文; `proposal.md` 全文; `dispositions.md` 的 R2 段; `v3/README.md`、`W8-v3.diff` 全文、`W9`–`W12b` 各输出、`v3unit.sh`、`run-w10-w11.sh`、`w10b.sh`、`replay138.sh`、`run-w12.sh` 头部、`mkdbg.py` 头部、`commentsync.py` 头部; hook 的 `:140-158`、`:560-830`、`:829-930`、`:1486-1590`; 套件的 sourcing 点、SC-8 与 SC-13 段; SOT `skill-benchmark-exemption.md` §1–§6; WP-A 的 `rule6_note` (proposal `:315-345`) 与 TASK-010–013 定义; post_spec R1、R2 汇总 (只 grep 了 count 相关内容); Forgejo `#217`、`#228` 正文 (只读 GET)。按任务书要求, 没有读本轮其他席位的报告。
- 跑了 (都在 scratch, `taskset -c 0,1 nice -n 19`, 每个不超过 1 分钟, 串行): W8 复现; `run-w10-w11.sh` (scratch 副本, 37 s); `w10b.sh`; `commentsync.py` 的 baseline 与 target; 实验 `pg-exp.sh` (组杀覆盖)、`stop-exp.sh` (不杀计时器的变体与 SIGSTOP)、`gate-env.sh` (环境改写)、`count-axis.sh` (F1)、`leader-exit.sh` (F11), 以及 bash 5.2 与 3.2 下的重定向语义。只按自己记下的 PID 清理过一个已停止的作业。仓内文件没有改动: `git status` 只有任务书开始时就有的两份未跟踪报告。
- 没有核实:
  1. bash 4.x 下继承 `EPOCHREALTIME` 的实际行为 (本机没有 4.x, 按代码推断);
  2. MINGW64 与 macOS 上的表现;
  3. 主仓提交里的跨仓关闭关键词在 Forgejo 上是否生效;
  4. 是否存在别的 issue 承载 count 轴 (没有做全量检索, 只看了 #217、#228 与 proposal);
  5. SC-V3/V5 在高负载 (> 4) 下的稳定性 (受资源纪律限制, 没有加压);
  6. `_sg_vx_big_judge` 的 here-string 失败路径 (按代码推断);
  7. 套件在 bash 3.2 下的现行计数;
  8. 按任务书要求, 没有跑 `run-w9.sh` 与 `run-w12*.sh`。
- 工具调用约 57 次。
