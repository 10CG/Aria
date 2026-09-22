---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-22T04:30:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

> `drift_check_skipped` 填 `true`: 本轮独立复核 `.aria/config.json` 的 `audit` 块 (`python3 -c "import json; d=json.load(open('.aria/config.json')); print(sorted(d['audit'].keys()))"` → `['_comment', 'checkpoints', 'enabled', 'max_rounds', 'mode', 'teams']`), 无 `drift_guard` 键, 与 R1–R4 结论一致。

## 已实读文件

派单 sha256[:16] = 897ca3e49042ea00

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (全文 233 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (全文 1818 行, 分 6 段读)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `## Success Criteria` SC-1~SC-22 全文 (`:457-478`, 逐条完整取行而非截断); `## Tasks` B.0 语料冻结节全文 (`:409-428`)
- `.aria/audit-reports/post_planning-R4-2026-09-20T033000-000Z-pre-merge-completeness-gate-change-scope-aggregated.md` (全文, R4 四题 Major 与 8 条 minor 原文)
- `.aria/audit-reports/post_planning-R4-2026-09-20T033000-000Z-pre-merge-completeness-gate-change-scope-qa-engineer.md` (我自己 R4 报告全文, 用于核对本轮是否有"无新证据重提")
- `git diff 71c500e b686185 -- openspec/changes/.../tasks.md .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 全 hunk (detailed-tasks.yaml diff 因单行超长改用 `--stat` 定位 + 逐 TASK 全文比对)
- `aria/skills/audit-engine/tests/test_sibling_spec_probe.py:299-337` (`TestNoPytestImport` / `TestRunAllTestsDiscovery` 两条守卫全文)
- `aria/skills/run_all_tests.sh:1-72` (`is_pytest_suite()` 全文与调用处)
- `aria/skills/phase-d-closer/references/execution-steps.md` (E1 命令行, grep 定位 `head -8`/`grep -cE`)
- `aria/skills/phase-d-closer/references/handoff-mechanics.md` (latest.md 两子步骤与 Forbidden patterns 段, grep 定位)
- `aria/skills/phase-d-closer/SKILL.md` (grep 定位 `post_closure`/`ai_native_estimator` 触发条件原文)
- `standards/conventions/session-handoff.md:111-260` (§2.3.1 五字段定义、§2.3.7 E1 表行)
- `aria/.gitignore:1-10`、主仓 `.gitignore:25-38`(workspace 相关条目原文)
- `/home/dev/.claude/skills/synced/.../skill-creator/SKILL.md:167`(workspace 位置措辞原文, grep 定位)
- **实跑核验**(全部在 `/tmp/claude-1000/-home-dev-Aria/82379761-f707-4902-a23a-45070cee8ae7/scratchpad/audit-R5-qa-engineer/` 下, 真仓内零写入, 仅用只读 git 命令):
  1. 把 `gen_yaml.py` 与已提交 yaml `cp -a` 到自己目录, 从委托 yaml 抽出 `a2_state_runs`/`v2_state_runs` 的 script+output 落盘, 补齐生成器所需 5 个 CLI 参数后重新生成 `detailed-tasks.yaml`, `diff` 委托版本 —— **逐字节 IDENTICAL** (独立复现 REGEN_IDENTICAL, 未采信主控自报)
  2. 从 yaml 抽出 `baseline_rebase.standards_files_derivation.script`, 在真仓根(`/home/dev/Aria`)以只读 git 命令(`ls-tree`/`show`, 无 checkout/fetch/写操作)直接执行, 输出与 yaml 内嵌 `output` **逐字节 IDENTICAL**;执行后 `git status --short` 核实真仓无新变化(除既有的 backend-architect 报告 untracked 文件)
  3. 把 `/tmp/.../p199-r5/state-base`(主仓 `a563192` + aria `1cb3872` 嵌套 clone)`cp -a` 到自己目录, 用真实 `tasks.md`/`detailed-tasks.yaml` 作输入重跑 `a2_state_runs.py` 全部 7 态(SC-12 liveness A/B/C/D/D2/E/F)+ N1/N2/N3 三态 —— 输出与 yaml 内嵌 `output` **逐字节 IDENTICAL**
  4. `git -C aria merge-base --is-ancestor 301641b 1cb3872`、`git merge-base --is-ancestor a563192 cf05d8b`、三端点 `cat-file -e` —— 验证 R4-M1 修法所称"aria/主仓两组端点按构造已在本地"为真
  5. `git diff --stat <不存在SHA> HEAD -- path` 与 `git -C standards diff --stat <伪SHA> 940cb5b -- path` —— 复现"端点不可达时 stdout 空串 + exit 128"的 R4-M1 同族信号(用于核验下方 M1 finding)
  6. `git grep --recurse-submodules -l -F completeness_gate | grep -E '...'` 在真仓与在未初始化子模块的 scratch 副本两态各跑一次 —— 确认 guard 基线目前无输出、且未初始化子模块不会造成该 pipeline 假失败
  7. `git log --oneline --diff-filter=A -- '**/state-scanner-workspace/**'`(1 个提交, 23 个文件)、`git log --since=2026-04-10 -- aria-plugin-benchmarks/ab-results/` 逐提交扫 workspace 路径(51 个提交, 0 命中)、`git show --stat 2a46d08`(0 workspace 路径) —— 核验 R4-M3 证据面
  8. `git init` 造仓测试 `git worktree remove` 在脏工作树下 exit=128("contains modified or untracked files"), `checkout -- .` 清理后 exit=0 —— 核验 TASK-019/020 三步法的可执行性

## R4 对账

| 项 | 判定 | 我亲验的证据 |
|---|---|---|
| R4-M1 (`d7f5b04c`, TASK-001 standards 组 rc128 假绿) | **closed** | `tasks.md:21` 与 yaml TASK-001 验收条现要求: standards 组先 `git -C standards fetch origin`, 三组端点各先 `cat-file -e <端点>^{commit}` 不成立即停, 零 diff 判据改为"退出码为 0 且输出为空"。我独立复现了修法要防的场景: `git diff --stat <bad-sha> <good-sha>` 给出空 stdout + exit 128, 与"真零 diff"(exit 0 + 空 stdout)在旧判据("只看输出为空")下不可区分, 新判据(加验退出码)可区分。`git -C aria merge-base --is-ancestor 301641b 1cb3872` 与 `git merge-base --is-ancestor a563192 cf05d8b` 均退出 0, 印证"aria/主仓两组端点按构造已在本地"的论证前提为真 |
| R4-M2 (`8d2e93ff`, TASK-031 手写 Phase D 漏 E1 与 latest.md 两子步) | **closed** | TASK-031 verification 现列 5 条(起稿/五字段全写/写后自校验/latest.md 两子步/单独提交请裁)。我逐字核对: `aria/skills/phase-d-closer/references/execution-steps.md:106` 的 `head -8 <handoff> \| grep -cE '^(track-id\|owner-container\|phase\|status\|updated-at):'` 与 TASK-031 引用的命令逐字相同(含 `:108` 的"勿插注释行"口径注); `handoff-mechanics.md:135` "跳过 latest.md 子步骤 1 ... 任何 cycle 都不可跳过" 与 TASK-031 的子步骤 1 描述逐字对应; `session-handoff.md:111-115`(§2.3.1 五字段)与 `:218`(§2.3.7 E1 表行)与 TASK-031 引用一致。另核实两个门控事实性声明: `phase-d-closer/SKILL.md:65` 确有 D.post 触发条件、`:228` 确有 `ai_native_estimator.enabled != false`; 真仓 `.aria/config.json` 的 `audit.checkpoints.post_closure` 现值确为 `'off'`, 且无 `ai_native_estimator` 键 —— 与 TASK-031 声称的"2026-09-21 实读"结果一致 |
| R4-M3 (`dec4ac57`, TASK-024 skill-creator 工作区无归属) | **closed** | 裁为 (b): 工作区不入库。我独立复核证据面而非采信自报: `aria/.gitignore:6-7` 确为 `skills/*-workspace/` + 注释"kept locally, archived in aria-plugin-benchmarks/ab-results/"; 主仓 `.gitignore:37-38` 确为 `aria-plugin-benchmarks/ab-workspace/` + 注释"结果已落 ab-results/, 无需入库"; 生效版 `skill-creator/SKILL.md:167` 逐字为 "Put results in `<skill-name>-workspace/` as a sibling to the skill directory"; `git log --oneline --diff-filter=A -- '**/state-scanner-workspace/**'` 只有 1 个提交(`2892c6f`)覆盖全部 23 个被追踪文件; `git log --since=2026-04-10 -- aria-plugin-benchmarks/ab-results/` 51 个提交逐一 `git show --stat` 扫描零命中 workspace 路径; `git show --stat 2a46d08` 同样零命中。六项证据全部独立复现, 与 revision_log 所述吻合 |
| R4-M4 (`5891aaeb`, `standards_files` 漏 `session-handoff.md`) | **closed** | `standards_files` 现列 8 条(第 8 条为 `conventions/session-handoff.md`), `standards` 键的零 diff 断言范围句改为"六个文件"。我用 `standards_files_derivation.py`(从 yaml 抽出, 在真仓根用只读 `git ls-tree`/`git show` 跑)独立复算, 输出与嵌入表**逐字节相同**: 第一步字面计数 10 族→排除 3 族(封闭清单)→余 7; 第二步按 CLAUDE.md Rule #N→SOT 映射补出 `conventions/session-handoff.md`(Rule #9)→合计 8。求法本身可独立复跑, 不再是"读上下文剔除"式的开放判断 |
| `f5b3afad` (standards_files_basis 求法复现不出七文件) | **closed** | 已随 R4-M4 一并解决: 新增 `baseline_rebase.standards_files_derivation` 把求法程序化, 我独立重跑得到与嵌入 `output` 逐字节相同的结果(10 族→排除 3 族→7+Rule#N 映射 1=8) |
| `0f027861` (集合判据"语义" vs 求法"字面"的分歧) | **closed** | 现求法明确分两步: 第一步字面(可机械复现), 第二步语义(Rule #N→SOT 映射, 同样可机械复现, 只在"该 SOT 内容是否被依赖"这一判断点上保留人工确认, 且已注明"两步都覆盖不到的形态...不在本求法的保证范围内")。三方(cr/tl/km)此前复跑得到不同结果的根因(排除清单不封闭)已被"封闭为三族"解决 |
| `cb1529a3` (粗体范围句与文件数不一致的自相矛盾) | **closed** | `grep -n "四个文件\|五个文件\|六个文件\|七份\|八份"` 核对: 现行文本(`standards` 键、`scope_repos.standards.head_at_a2`、`tasks.md:21`)全部同步为"六个零 diff + 八个被引全集", 唯一残留的"四/五/七"字样只出现在 `revision_log` 对历史版本(v2.2/v2.3)的如实转述里, 不构成当前自相矛盾 |
| `f0e78a1e` (revision_log 的 v2.3 条声称与 TASK-029 实际改动不符) | **closed** | v2.4 revision_log 保留 v2.3 原文不改、在 v2.4 条目里勘正, 并"本轮实证判定 deliverables 该改"—— 我核对 TASK-029 当前 `deliverables` 字段(9 项: gitlink + 8 个版本文件)确已不含台账, 且姊妹任务 TASK-025 的 `deliverables`(5 项版本文件)同样不含台账, 两者口径一致 |

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| M1 | major | issue | implementation | `detailed-tasks.yaml TASK-027` | 与 R4-M1 同族的"命令失败空输出被当通过"缺陷, 在 TASK-027 第 4 步 (b) 未被同步修复 |

### M1 · `c287d217` · TASK-027 第 4 步 (b) 的 `git diff --stat` 判据与 R4-M1 刚修复的缺陷同构, 未被同步修复(已知项)

- **证据(亲自实跑)**: `detailed-tasks.yaml:1711`(TASK-027 第 4 步)逐字为: "(b) `git -C aria diff --stat <TASK-024 记下的 A> S3 -- skills/audit-engine skills/phase-c-integrator` **有输出** ⇒ AB 实测的处方文本与将要合并的不同, 停下"。这条判据只看"有无输出", 不看退出码。我实测: `git -C aria diff --stat 0000000000000000000000000000000000dead HEAD -- skills/audit-engine` 给出**空 stdout**、`fatal: bad revision`(stderr)、**exit 128**; 对 `standards` 子模块用不可达 SHA 重复同一测试同样是空 stdout + exit 128。这与 `metadata.baseline_rebase` 里 R4-M1 刚刚修复的那类信号(2026-09-21 自检记录: "端点对象不在本地...时 git diff 的 stdout 同样是空串,退出 128,只看输出为空会把『没比成』读成『零 diff』")**逐字同构**, 只是这次的字段是 `--stat` 而非 `--shortstat`, 判据字段是"有无输出"(等价于"输出为空⇒判无风险")而非直接的"零 diff"结论, 但失效模式完全一致。
- **为什么这不是虚构的边缘情形**: `A`(TASK-024 记录的 aria `origin/master` SHA)由 TASK-024 写入台账(一份 markdown 文本), 经 owner_gates 第 4/5 项两次会话切换(AB 会话→非 AB 会话)后, 在 TASK-027(5.5, 执行序上远晚于 TASK-024)里被"读回"重新组装成命令行参数。这正是 R4-M1 自检结论点名的两类真实触发源之一("SHA 抄错、整行误喂")在本计划里唯一还会发生的位置 —— TASK-001/TASK-030 的 `commit_attribution` 调用不涉及手抄 SHA(全部由脚本内部 `git rev-parse`/`git ls-remote` 现取), 只有这里的 `A` 是"一次写、隔多个任务和至少一次会话切换后再读"的手抄值。
- **失败场景**: 执行者在 TASK-027 第 4 步严格按字面执行: 若台账里的 `A` 因抄写误差或(理论上更罕见的)本地对象不可达而导致 `git diff --stat A S3 -- ...` 报错退出 128 且 stdout 为空, 执行者会读到"无输出"并按判据字面**误判为"AB 实测内容与将合并内容一致, 继续"**, 从而在**未重新走 Rule #6 AB**(TASK-024)的情况下把可能已经偏离 AB 基准的 `skills/audit-engine`/`skills/phase-c-integrator` 内容并入 aria master —— 这与"漏掉某个必做项(Rule #6 AB 验证)"以及"得出不可证伪的验收结论"两条 major 判据都对应得上。
- **不构成 finding 的反例已排除**: 我另测了`sc12_liveness.guard_config_hooks`(dispatch 背景事实 (B) 点名的第二处同族嫌疑, `git grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'`) —— 未初始化子模块不会让 `git grep --recurse-submodules` 出错(实测仍是"跳过该子模块", 干净退出), 唯一会让它产生同类"假空"信号的场景是"根本不在 git 仓库内运行", 而该命令的运行上下文(主仓根)结构上排除了这种可能, 与 TASK-027 的"跨任务手抄 SHA"这一真实触发路径不是同一风险量级, 故不升级为 finding, 已在下方"风险/疑问"记录评估过程供裁。
- **建议修法**: 把 TASK-027 第 4 步 (b) 的判据改成与 TASK-001 同口径 —— 先对 `A`、`S3` 各跑 `git -C aria cat-file -e <sha>^{commit}`, 不成立即停(与"取号终核不符"同一 owner_gates 第 6 项出口, 不新开等待点); `diff --stat` 本身的零判据改为"退出码为 0 且输出为空⇒相同, 非 0⇒停"。

## 对执笔人自报薄弱点的表态

1. **R4-M1 发生条件比 R4 原文窄**: 可接受。这是执笔人在自检时主动发现并如实记录的前提收窄(`fetch.recurseSubmodules=on-demand` 的递归拉取细节), 不影响修法本身(fetch+cat-file+退出码判据), 我独立验证了"aria/主仓两组端点按构造已在本地"的论证前提为真(见上表证据), 修法有效性不受这一措辞收窄影响。
2. **R4-M3 按 (b) 裁没有实跑依据**: 可接受。二选一的判据是"仓内 SOT 怎么规定"而非"这次 AB 实际产生了什么副作用", 全跑一轮 AB 只为观察工作区落点纯属浪费; 我独立复核了全部六项书面/历史证据(gitignore 注释、SKILL.md 原文、单一添加提交、51 个提交零命中、先例提交零命中), 结论稳固。
3. **TASK-031 latest.md History 落点是执笔解读**: 可接受。我亲自读了 `docs/handoff/latest.md` 全文结构, 确认它确实没有字面 "History" 表格, 只有 `**Latest**:` 指针 + 按日倒序的说明段落; 计划把"具体落在哪"留给执行时读版式判断、但用 `grep -cF` 断言可观测的完成结果, 这个折中是诚实且可核的, 不构成隐患。
4. **"latest.md 改动单独成提交"是执笔新加的做法**: 可接受。这是对 `commit_attribution` 判据(共享指针一律 `foreign`)的合理适配, 不这样做反而会让周期 handoff 提交的归属判定被 latest.md 的改动拖累; 判断清单第 28/38 条已把这条新增动作登记为"AI 流程判断"请 owner 复议, 符合 Rule #10 的自证要求。
5. **TASK-029 deliverables 去掉台账**: 可接受, 且是改进而非缺陷。我核对了姊妹任务 TASK-025 的 `deliverables` 同样不含台账(只列 5 个版本文件), 两者现在口径一致; 台账追加改随 TASK-030 第一条提交, 与 `commit_attribution.cannot_catch` 和 `owner_gates` 第 16 项的措辞("TASK-029 的交付物结构上不含 exclusive 路径")完全对齐, 不再有 R3 minor `638d2a0f` 指出的自相矛盾。
6. **同体自检**: 可接受, 且本轮方法论上有额外印证。v2.4 的执笔实例是新派实例(与 v2.2/v2.3 不同容器会话), 严格说不算完全"同体", 但"作者审视自己刚写的东西"这一结构性盲区依然成立; 我这一轮没有停留在"读文本判断合理"上, 而是独立重跑了生成器(REGEN_IDENTICAL)、`standards_files_derivation.py`、`a2_state_runs.py` 三个可执行证据链, 三者均逐字节吻合执笔人嵌入的输出 —— 这印证了"多轮独立复算"这一补偿机制本身是有效的(没有发现执笔人编造或误报的三态证据), 但也确实是我(而非执笔人)主动做了这层验证, 支持 R4 聚合报告提出的"把独立复算流程制度化"的建议。

## 风险 / 疑问

- **(A, dispatch 背景事实) TASK-031 第 10 条"track-id 写错⇒停在 owner_gates 第 16 项"在 Phase D 不可达**: 我用 `grep`/程序化扫描确认 yaml 全文里 `commit_attribution` 真正被"跑...退出非 0 ⇒ 停"式调用的只有 TASK-001 与 TASK-030 两处(TASK-031 里的同名提法只是叙述性论证句, 不是一次真实调用), 而 TASK-031 执行时序晚于 TASK-030 的最后一次调用, 其自身产生的 Phase D 提交(含周期 handoff)在双推前没有第三次 `commit_attribution` 校验。**我的严重度评估**: 不到 major —— 因为 TASK-031 给出的实际可执行指令("track-id 逐字写 `pre-merge-completeness-gate-change-scope`")本身是对的, 只是配套的"写错会被挡"这句后果描述对本任务自己的提交不成立; 一个照字面正确执行的执行者不会因为这句失真的后果描述而做错任何事, 只是失去了一层本不存在的安全网幻觉。按严重度口径("不影响执行者会不会做错/做漏/卡住的, 最高只能是 minor")这本该是 minor, 但 dispatch 明确要求"非 major 则只记风险不计 finding", 故按指示记于此, 不计入 finding。
- **(B, dispatch 背景事实) `sc12_liveness.guard_config_hooks` 的"须无输出"判据同族嫌疑**: 已实测排除(见 Finding M1 内"不构成 finding 的反例已排除"段) —— 未初始化子模块不会让该 pipeline 假失败, 唯一的失效路径("不在 git 仓库内运行")在其固定调用上下文(主仓根)下结构上不成立, 与 TASK-027(b)真实存在的"跨任务手抄 SHA"路径不同量级。按 dispatch 指示不计入 finding。
- **R4 另四条独立 minor(`9c0dcb27`/`d931db51`/`0dd2d3f2`/`ea958583`)与前轮未动的 minor**: 本轮未发现超出 R4 已记录范围的新证据, 不重提为 finding。其中 `0dd2d3f2`(我自己 R4 提出的 SC-12 liveness 三态证据不可复现)在本轮有**积极的新证据**: 用官方指定的 scratch 环境(`state-base` = 主仓 `a563192` + aria `1cb3872` 嵌套 clone, 而非"当前真实仓库的完整副本")重跑 `a2_state_runs.py`, 输出与嵌入表逐字节相同 —— 我 R4 报告观察到的偏差, 根因正是我当时用的"共享基准副本"包含了 `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py`(该文件在 `a563192` 上尚不存在, 已用 `git show a563192:.../gen_yaml.py` 确认), 而 `a2_state_runs.py` 设计上就是要在**不含该文件**的冻结快照上跑。这不改变 `0dd2d3f2` 当初"不影响 L2 判据"的 minor 结论, 但把"为什么会不一致"的根因坐实为"测试环境选错", 而不是嵌入证据本身失实 —— 供 owner 参考, 不重开 finding。
- **TASK-027 步骤 6 的 `comm -23` 判据**: 顺带检查了同一任务里另一处"靠输出是否为空判断"的地方(`comm -23 <第 3 步集合文件> <(git -C aria show master:CHANGELOG.md | grep ...)>`)。若 `git show` 因故失败, `<()` 进程替换会给出空集合, `comm -23 A <空>` 的结果是 **A 的全部内容**(非空), 该判据本身在这种失败模式下会正确地判"不为空⇒停", 不会假绿 —— 与 Finding M1 不同构, 未发现问题, 记录于此说明我对同一任务做过差异化检查而非按 pattern 一刀切。

## Verdict

verdict: **PASS_WITH_WARNINGS**(0C / 1M / 0m)

**Vote: REVISE**

## 是否足以开始 Phase B

**从我的视角(验收设计与可证伪性)尚不足以**: 本轮独立复核确认 R4 四题 Major 与四条同处 minor 全部真实闭合(逐条亲验, 非采信自报或转述), REGEN_IDENTICAL、`standards_files_derivation`、`a2_state_runs` 三条可执行证据链均独立重跑到位、逐字节吻合。但新发现的 M1(TASK-027 第 4 步 (b) 与 R4-M1 同构的失败模式未同步修复)会让"照计划字面执行"在 SHA 抄写/跨会话传递出错时**放行未经 Rule #6 AB 复验的 skill 内容**, 属于计划自己刚建立的判据规范("零 diff 判据须验退出码")在同一文档内未被一致应用, 建议随下一版返修一并处理(修法简单, 与 TASK-001 同口径, 不涉及任务结构重排)。与本视角无关的 `owner_gates` 第 1 项(10CG/Aria#195 完成 C.2 或 owner 明示改序)仍是独立于本次审计结论的外部前置门。
