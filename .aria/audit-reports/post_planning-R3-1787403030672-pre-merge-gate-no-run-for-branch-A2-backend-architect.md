---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787407802724
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 1
minor_count: 1
---

# post_planning R3 — A2 (backend-architect) 审计报告

## 摘要

透镜 = R2 归本席三簇 (#1 exec_order 机检字段 / #5 INV-1 git show 核验 / #8 `:404-408` 参考锚点) 处置核对 + TASK-003/005/006 新依赖边与 INV-2 配对核查 + v3 diff 机制层新矛盾扫描。三簇均**已按承诺内容落地** (证据见下表)。但对 #5 落地方式本身做可执行性复核 (本席 R3 专项任务) 时发现一处**新** Major: `git show <commit>^:path` 两处 (metadata.invariants.INV-1.encoded_as / TASK-013.verification) 均未加 `-C aria` 或等效 cwd 声明, 而 TASK-013 同一任务内另两条 verification 命令 (`pytest aria/skills`、`grep -rn ... aria/skills/...`) 都是从**主仓根**、以 `aria/` 前缀路径执行 —— 三条命令并列, 天然读法是"同一 cwd 顺序执行", 但 git show 目标 commit 是 aria 子模块自己 git 历史里的 SHA, 从主仓根跑会因"objects 不在同一仓"直接报错 (非静默错误, 但会阻断 INV-1 核验被真正执行), 且该文件在 TASK-000b 已确立 `git -C aria <cmd>` 的显式写法先例却未在此复用 (同类问题两处写法, 一实一虚)。另有 1 处 Minor: INV-1 的 `grep -c 'return "pending"'` 对基线 aether.py 实测命中 2 处 (zero-run 分支 `:226` + fallback 分支 `:238`), 计数本身不能定位到"零 run"这一支, 精度弱于旁边并列的 `--stat` 双文件核验 (后者才是真正承重的"同 commit"信号)。

TASK-003/005/006 新增依赖边 (→ TASK-003) 逐条核验：TASK-005 deps=[004,003]、TASK-006 deps=[005,003,001]、TASK-010 deps=[009,003] 均确认存在且不产生环；与 INV-2 (qa RED→be GREEN 配对) 无冲突 — 新边只是让"写测试"多了一个"等前置行为已实现"的前提, 不改变各自 RED/GREEN 配对内部的先后 (005 仍先于其 GREEN 伙伴 006; 010 是文档任务无 RED/GREEN 配对适用)。TASK-010 跨轨依赖 (helper 轨任务却依赖 gate 轨的 TASK-003) 与 `parallel_tracks` 段落"两轨 disjoint 可并行"的泛化表述形成局部张力, 但 `execution_order` 段已显式写明"010 需 003", 不构成静默矛盾, 不计入 finding。

## R2 处置核对

| R2 簇 (归本席) | 承诺内容 | v3 证据 | 判定 |
|---|---|---|---|
| #1 (A1-M1+A2-M1+A3-M1+A4-m4+A5-M2): TASK-004 exec_order 未随「前移」处置改写 | exec_order 全表重编 (004=3, 002=4, 003=5…); TASK-002 依赖 004 (机检边) | 实读: TASK-004.exec_order=3 dependencies=[TASK-000b]; TASK-002.exec_order=4 dependencies=[TASK-000b, **TASK-004**]; TASK-003.exec_order=5 dependencies=[TASK-002]。逐任务核验 exec_order > 所有依赖 exec_order (19 任务全表核对, 见下方核验记录) 全部成立; metadata.exec_order_note 新增机检不变量声明 | **closed** |
| #5 (A2-M2+A1-m1): TASK-003 INV-1「父提交 checkout」验证模糊, 无自动化兜底 | 非破坏性 `git show <commit>^:path` 核验; 落 TASK-013 (main-loop) verification | 实读: INV-1.encoded_as 给出具体命令 `git show <commit>^:skills/phase-c-integrator/scripts/ci_backends/aether.py \| grep -c 'return "pending"'` + `git show --stat <commit>`, 明文"不 checkout, R2 A2-M2 detached-HEAD 先例"; TASK-013.verification 复述同一核验并落到 main-loop。承诺内容如约落地 | **closed** (但落地方式本身引入新缺口, 见下方 [A2-backend-architect-PP3-M1]) |
| #8 (含 A2-m1): `:404-408` 系派生层自行推算, 未标"参考锚点" | 参考锚点标注 | 实读: TASK-006 deliverables 现为 "`:404-408` 参考锚点 (派生层推算)", 与 TASK-007b `_result :67 参考锚点` 同一标注格式 | **closed** |

r2_closed=3, r2_partial=0, r2_not_addressed=0 (计数范围: 本表 3 行, 均为 R2 聚合表归本席贡献的簇)。

## 已核验无误 (逐条抽样)

- **exec_order 全表拓扑核验 (19 任务)**: 000(0,deps[])→000b(1,[000:0])→001(2,[000b:1])→004(3,[000b:1])→002(4,[000b:1,004:3])→003(5,[002:4])→005(6,[004:3,003:5])→006(7,[005:6,003:5,001:2])→007a(8,[001:2,006:7])→007b(9,[007a:8])→008(10,[000b:1])→009(11,[008:10])→010(12,[009:11,003:5])→011(13,[006:7,007b:9,010:12,001:2])→012(14,[010:12,011:13])→013(15,[003:5,006:7,007b:9,009:11,011:13])→014(16,[009:11,010:12,011:13,013:15])→015(17,[012:14,013:15,014:16,001:2])→016(18,[015:17,001:2])。每任务 exec_order 严格大于其全部 dependencies 的 exec_order, 无一例外, 与 metadata.exec_order_note 声明的机检不变量一致。
- **TASK-003 ∈ 11 任务下游闭包**: 005/006/010 直接依赖 003; 007a/007b 经 006 传递; 011/012 经 006 或 010 传递; 013 直接依赖 003; 014/015/016 经 013/011/010/015 传递。11 项全部核实成立, 与 metadata.exec_order_note 断言数字吻合。
- **19 任务 reason 字段覆盖**: `grep -c "^    reason:"` = 19, `grep -c "^  - id: TASK-"` = 19, 1:1 无缺口。
- **estimated_hours 求和 = metadata.estimated_hours**: 逐任务加总 (0.5+0.5+1.5+2+3+4+3+3+2+2+4+5+3+4+4+1+3+2+2) = 49.5, 与 metadata.estimated_hours: 49.5 一致；`estimation_note`「19 任务中 14 个 <4h」逐一核对 (000/000b/001/004/002/005/006/007a/007b/010/013/014/015/016 = 14 个) 数字准确, 非旧结论沿用。
- **TASK-005 title 措辞替换未改变技术含义**: proposal §7 表 SC-10 原文「旧名包装对 `main_branch=` 关键字**调用**仍可用」→ TASK-005 title 改写为「旧名包装以关键字**形参** `main_branch=` 仍可用」——回避了「调用」这个会命中归档门集成关键词启发式的字面词 (R2 A1-m8/cluster#8), 但"形参"与"调用"描述的是同一个 Python 关键字实参调用约定的两面 (定义侧 vs 调用侧), 不构成字段级语义漂移。
- **TASK-004/005/006 新依赖边不产生环、不破坏 INV-2 配对内部序**: TASK-005 (RED, 依赖 004+003) 仍先于其 GREEN 伙伴 TASK-006 (依赖 005); TASK-010 (docs, 依赖 009+003) 无 RED/GREEN 配对适用, 依赖 003 只是"文档需引用已实现的 DEFAULT_CONFIG 新 key"的前提, 不涉及 TDD 顺序。
- **INV-1 rule 与 encoded_as 分离后语义未漂移**: `rule` 字段聚焦"为什么必须同 commit"(fail-open 论证), `encoded_as` 聚焦"怎么核验"; 两者与 proposal INV-1 原意 (同 commit, 避免盲区从恒 wait 退化为恒 green) 一致, 无方向错误。

## Findings

### [A2-backend-architect-PP3-M1] TASK-013/INV-1 的 `git show <commit>^:path` 核验命令缺 `-C aria` (或等效 cwd 声明), 与同任务内另两条命令的 cwd 隐含约定冲突

- **Category**: executability
- **Scope**: `metadata.invariants.INV-1.encoded_as` / `TASK-003.verification` / `TASK-013.verification`
- **问题**: TASK-003 的提交 (承载 §1 aether.py + §2.2 compute_verdict 改动) 发生在 **aria 子模块自己的 git 历史**里 (TASK-000b 已确立: aria 分支创建用 `git -C aria checkout -b ...`; TASK-015 (i) 单独把 aria 子模块的本地 merge/tag/双推列为独立步骤, 与主仓 gitlink bump 分列——两处均印证 TASK-003 commit sha 是 submodule 自己 objects 库里的对象, 不在主仓 `.git` 里)。
  INV-1.encoded_as 给出的命令是: `git show <commit>^:skills/phase-c-integrator/scripts/ci_backends/aether.py | grep -c 'return "pending"'` + `git show --stat <commit>`——路径**不带** `aria/` 前缀 (与全文件其余所有文件路径引用一律带 `aria/` 前缀的写法不一致), 隐含"这条命令应以 aria 子模块目录为 cwd"运行, 但**没有显式写出** `-C aria` 或 `cd aria &&`。TASK-013.verification 原样复述同一条 (`git show <TASK-003 commit>^:…/aether.py`), 同样未加 cwd 声明。
  TASK-013 同一任务的另外两条 verification 命令——`python3 -m pytest aria/skills -q`、`grep -rn dispatches aria/skills/phase-c-integrator aria/skills/workflow-runner`——都是**从主仓根**、用 `aria/` 前缀路径执行 (pytest/grep 是纯文件系统操作, 不关心 git 仓边界, 从主仓根天然可行)。三条命令并列写在同一 verification 列表里, 最自然的读法是"同一 shell / 同一 cwd 顺序跑", 若 main-loop 照此读法把 git show 也从主仓根执行, 会因为 `<commit>` 是子模块自己 objects 库里的 SHA、主仓 `.git` 完全不含该对象而**直接报错** (`fatal: bad revision` / `Not a valid object name`)——不是取错文件那种"静默偏差", 而是命令层面就跑不通, 但正因为如此也可能被 main-loop 简单"解释掉"(如误判为该 SHA 尚未存在、INV-1 核验此次跳过), 使这条本应是刚性核验的 INV-1 检查变成又一次实施者临场发挥。
  本文件其实已有解法先例: TASK-000b 的 "`git -C aria checkout -b feature/152-no-run-for-branch`" 正是同一类"从主仓根操作子模块仓"的写法, 但这里没有复用——与 R2 A2-M2 原本指出的"同类问题两种修法, 一实一虚"是同一形状 (fix-the-class 视角: 上一轮把「检查手段」从 checkout 换成了 git show 修实了, 但「检查手段该在哪跑」这条没有跟着补实)。
- **实测影响**: 不影响运行时行为, 但会使 INV-1 唯一的机制化核验点 (TASK-013) 在字面执行时大概率报错; 报错本身可见, 但下一步是被 main-loop 正确诊断为"少了 -C aria"并修正, 还是被当作"这条核验暂时无法跑, 记 handoff 跳过", 取决于临场判断——正是 A2-M2 当初想消除的不确定性。
- **建议**: 在 INV-1.encoded_as 与 TASK-013.verification 两处的命令前一律加 `git -C aria`, 例如: `git -C aria show <commit>^:skills/phase-c-integrator/scripts/ci_backends/aether.py | grep -c 'return "pending"'`、`git -C aria show --stat <commit>`——与 TASK-000b 先例统一写法, 消除"三条命令同 cwd"的误读空间。

### [A2-backend-architect-PP3-m1] INV-1 的 `grep -c 'return "pending"'` 计数对基线文件命中 2 处, 无法定位到「零 run」这一支

- **Category**: executability
- **Scope**: `metadata.invariants.INV-1.encoded_as`
- **问题**: 实测 aria @ 9e6a17c `skills/phase-c-integrator/scripts/ci_backends/aether.py` 的 `_normalize_pr_ci_status`, 字面量 `return "pending"` 出现 **2 次** (`:226` 零-run 早退分支 `if not runs: return "pending"`; `:238` 函数尾部未匹配状态兜底分支)。INV-1 要核验的是"父提交仍含**零 run → pending** 这一支", 但 `grep -c` 是对整个文件的字符串计数, 不区分匹配落在哪个分支——只要文件里"存在至少一处"该字面量（哪怕零-run 分支已经被意外改写、只剩 fallback 分支还留着这个字符串), 计数检查依然会"命中"。
  这不是独立生效的漏洞: 紧邻的 `git show --stat <commit>` (核验两文件同 commit 变更) 才是真正承重的"INV-1 同 commit"信号, `grep -c` 只是辅助确认"确实在核对正确的 commit 附近"; 但既然 encoded_as 把它并列写成两个核验条件, 就应具备各自独立的判别力, 目前它不具备。
- **建议**: 改用能定位到具体分支的模式, 例如 `grep -c 'if not runs:'`（该行在当前实现里只出现一次, 且直接锚定零-run 分支）或 `grep -A1 'if not runs:' | grep -c 'return "pending"'`, 而非对整个文件做无方向的字面量计数。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE（1 Major 建议在 B.1 起跑前收敛: TASK-013/INV-1 的 `git show` 两处补 `-C aria`, 与 TASK-000b 先例统一, 消除三条并列命令的 cwd 误读空间；1 Minor 可选顺手改, 不阻塞。R2 归本席三簇 #1/#5/#8 均已如约落地, TASK-003/005/006 新依赖边核验无环、无 INV-2 冲突, exec_order/闭包/reason/estimated_hours 四项机检不变量全表核验通过, 未发现新的 Critical 或违反 spec 不变量情形）。
