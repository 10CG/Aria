# phase-c-integrator AB Benchmark 评分报告

- **日期**: 2026-07-31 | **cycle**: aria-plugin #122 (v1.64.1 → v1.65.0-draft) | **suite**: 1.1.0
- **三臂**: with_skill (v1.65.0 候选) / old_skill (v1.64.1 快照) / without_skill (无 skill, 但含 CLAUDE.md + memory 自动加载污染面)
- **评分依据**: AB_TEST_OPERATIONS.md「Expectations 编写原则」(三臂全过 → 先语义分档, 不直接判无区分度) +「产出形态钉死」(descriptive 统一核对)
- **分制**: 0-1 分档; pass 阈值 = 0.8

---

## 1. 产出形态核对 (先决)

| eval | with_skill | old_skill | without_skill | 判定 |
|------|-----------|-----------|---------------|------|
| 1 | descriptive (自述, 未实跑) | descriptive | descriptive (「全程只描述, 不实跑」) | 一致 |
| 2 | descriptive | descriptive | descriptive | 一致 |
| 3 | descriptive | descriptive | descriptive (「未实跑命令」) | 一致 |

三个 eval 九臂全部遵守 descriptive: 无一臂实跑仓库命令, 无一臂以真实仓库当前态否证场景前提。**无 genre confound, 三 eval 全部可计入 delta。**

---

## 2. 逐 eval 三臂分档

### eval-1: C.1 conventional commits 生成 (规范性 + 分组)

| 臂 | 分 | 档 | 要点 |
|----|----|----|------|
| with_skill | 1.0 | A | `feat(auth)` 正确; 单 commit 分组论证充分 (纵向切片原子性); 跳过规则评估 + commit-msg-generator 委派 + 增强标记 (Executed-By/Context/Module) + C.1 输出契约 (context_for_next) 完整; 占位符处理诚实 (「若确无, 省略而非编造」) |
| old_skill | 1.0 | A | 与 with 臂几乎同档: `feat(auth)` + 单 commit + 增强标记 + 输出契约; 额外含 branch-finisher completion_option 前置 (v1.64.1 面) 与混入无关变更的兜底 |
| without_skill | 0.8 | B | conventional commit 本体优秀 (`feat(auth)`, 分组判据、amend 兜底、migration/路由注册遗漏嫌疑排查是三臂最细); 但 **无增强标记、无 skill 输出契约、无 commit-msg-generator 委派** — skill 价值面整体缺席 |

**档位差**: with = old (A) > without (B)。C.1 在 v1.65.0 未变更, with vs old 零差异符合预期。skill vs 无 skill 的区分度在「流程契约与标记」而非 git 常识 — without 臂 git 常识甚至更细, 但那不是本 skill 的价值点。

### eval-2: C.2 合并冲突处理 (冲突流程 + pre-merge gate/C.2.4) — 本次 change 定向观察面

| 臂 | 分 | 档 | 要点 |
|----|----|----|------|
| with_skill | 1.0 | A+ | 冲突处置完整 (停下/不自动挑边/rebase 手工解/测试重跑/force-with-lease); **gate 链重走**论证到位 (新 SHA 使旧判定失效); **正确反映 v1.65.0 新语义**: 显式做 path coverage 评估并正确推断 `backend/config/settings.py` → `decision=covered` → 不落 not_applicable 短路、照走 CI wait; 输出 yaml 含 `path_coverage` 键; (b) 轴 main in-flight 保留 |
| old_skill | 1.0 | A | 冲突处置同样完整且更细 (union vs 同键裁决表、race window 说明); **按旧语义正确执行**: pending 恒 wait+retry (`[30,60,120,300,300]`), 无 path coverage 概念 — 忠实于 v1.64.1, 非缺陷; no_ci_fallback / stub NotImplementedError abort / C.2.4.5 / C.2.5 全链在场 |
| without_skill | 0.7 | B | 冲突解决工艺一流 (三类冲突分型、dict 重复键静默覆盖、双向意图核对、abort 保底); **提及 pre-merge gate**: Rule #8 (a) PR CI passing + (b) main 无 in-flight + 无 backend 显式降级 — 但这来自 CLAUDE.md 泄漏面 (见 §4); 缺 wait/fail 三态语义、退避重试、C.2.4.5 submodule gate、audit 检查点、结构化输出契约 |

**档位差**: with (A+) > old (A) > without (B)。**定向问题裁定**: with 臂正确内化 not_applicable 新语义 — 且是以「负向验证」形态 (正确判定本场景 covered 不短路, 未滥用新短路); old 臂按旧语义 pending 恒 wait, 两臂各自忠实于所载版本, **新语义正向反映、无回归、无误用**。注意: 本 eval 只踩中 covered 分支; not_applicable 短路 + surface 警告行的正路径无 eval 直接踩中 (见 §5 caveat)。

### eval-3: C.2.5 多远程推送 (双推 + 逐 remote ls-remote SHA 核验 + 子模块顺序)

| 臂 | 分 | 档 | 要点 |
|----|----|----|------|
| with_skill | 1.0 | A | 六步全: expected_sha 快照 → 子模块枚举 → enforced_remotes 解析链 → per-remote matrix (子模块先/主仓后/verify 三段, 子模块失败挡该 remote 主仓推送) → 失败优先级表 (read_only/fail_on_partial_push) → 修复指引; verify 4-attempt + possible race; detached HEAD; helper 降级; 与 CLAUDE.md 约束 1/2 显式对齐 |
| old_skill | 1.0 | A | 同等完整 (C.2.5 两版本间无变更): 六步 + matrix + 失败分支 7.1-7.4 + 不变量小结; 与 with 臂内容基本同构 |
| without_skill | 0.85 | B+ | 三个关键点**全部命中**: 双推、逐 remote ls-remote 全等判据、子模块先落两端再 bump gitlink; 另有本地合并形态前置核验、分叉三前置核验后才 force-with-lease; 缺 skill 机制面: per-remote matrix gating、fail_on_partial_push/read_only_remotes 配置、helper/重试参数、输出 schema — 且高分**显著受 CLAUDE.md 硬约束段泄漏抬升** (近逐字复现, 见 §4) |

**档位差**: with = old (A) > without (B+)。without 臂在本 eval 的高分是污染最重的一格 — 外部采用者 (无本仓 CLAUDE.md) 拿不到「假阴性诱发误 force / 半推镜像分叉」这级表述, 真实区分度大于表观 0.15。

---

## 3. Delta 结论

| 对比 | mean 差 | 结论 |
|------|---------|------|
| **new vs old (核心)** | 0.00 (3.0 vs 3.0) | 数值零 delta = **无回归**。定向语义面 (eval-2): with 臂正确执行 v1.65.0 not_applicable 新流程 (path coverage 评估 → covered → 不短路, (b) 轴保留, 输出含 path_coverage 键), old 臂按 v1.64.1 pending 恒 wait — 行为分叉方向与 spec 预期一致。additive 变更 + 原有面无损, 符合发版预期 |
| with vs without | +0.22 (1.00 vs 0.78) | 正向 delta, 且按 #116 语义分档原则真实差距更大: without 的 0.78 里有 CLAUDE.md 泄漏红利 (eval-2 gate 判据、eval-3 硬约束段近逐字), 扣除污染面后 skill 独有价值 (输出契约/matrix gating/三态语义/配置面/重试参数) 全部为 without 不可达 |
| old vs without | +0.22 | 同上 |

**pass_rate** (阈值 0.8): with 3/3 = 1.00 | old 3/3 = 1.00 | without 2/3 = 0.67 (eval-2 0.7 未达线)。

---

## 4. 污染实测 (DEC-20260722-001 决策 4 重测门)

逐臂检查 3 个 without_skill answer, 三分类:

### (c) 真污染 — SKILL.md 专有设计术语: **零命中**

检查词表: `wait_recoverable` / `not_applicable` / `path_coverage` / `path_coverage_enabled` / `C.2.4.5` / `submodule_gate` / `verify_parity_post_push` / `push_all_remotes` / `git-remote-helper` / `fail_on_partial_push` / `read_only_remotes` / `enforced_remotes` (配置键形态) / `no_ci_fallback` (键名形态) / `per-remote matrix` / 增强标记 (Executed-By/Context/Module) / `commit-msg-generator` / `context_for_next` — **三个 without 臂均未出现任何一个**。(eval-3 without 的「enforced remote」来自 eval prompt 原文, 不计。) #116 根因修复 (CLAUDE.md 去 skill 术语) 在本次重测中**持续有效**。

### (b) 合法留存面泄漏 — CLAUDE.md 规则判据本体词汇 (DEC 裁定合法, 出现即记录)

| 臂 | 命中 |
|----|------|
| eval-1/without | 「OpenSpec/issue 跟踪」(信息地图面); feature 分支命名 `feature/oauth2-social-login` 与 Phase B.1 概念 (十步循环面); 全程无带圈数字 (全局 CLAUDE.md 禁令被遵守, 中性) |
| eval-2/without | 「Rule #8 pre-merge gate」+ (a) 本分支 CI passing / (b) main 无 in-flight run 两轴判据 (规则 #8 段本体); 「无可用 CI backend 时显式降级并记录, 不静默跳过」(no_ci_fallback 概念转述, 未用键名); 「本地双推后对每个 remote git ls-remote 取 SHA 比对, 全部一致才算推成功, 不信 push 回执」(硬约束 2 近逐字); Rule #7 secret 处置 |
| eval-3/without | 最重: 「orphaned gitlink」「clone --recursive 断裂」「禁服务端合并/Do: merge 语义」(硬约束 1 整段复现); 「双推」「逐个 ls-remote 核验」「push 退出码/回执两个方向都会骗人: 假阴性…诱发误 force; 半推…镜像分叉」(硬约束 2 **近逐字**); 「Rule #10 …写进 handoff 请复议」; 「force-with-lease 前三项前置核验」+「aria-runner-bot 并行写入」+「GitHub Secret Scanning 扫整个 push range」+「CF Access 抖动」(注: 这四条来自 **memory/MEMORY.md 自动加载面**, 不在 CLAUDE.md 本体 — DEC 重测门标的是 CLAUDE.md, 但 memory 同属仓内 baseline 结构性污染面, 一并记录) |

### (a) 模型自身 git 常识 (可独立推出, 不计污染)

`feat(auth)` 类型/scope 判定、单 commit vs 拆分的原子性论证、heredoc 提交、`--force-with-lease` 优于 `--force`、union 合并 vs 同键裁决、`git ls-remote` 验证远端 SHA 的一般做法、merge --abort 保底、dict 重复键静默覆盖 — 均为通用工程常识。

**污染判定小结**: 真污染 (c) = 0, #116 治理面干净; 合法留存面 (b) 泄漏显著且集中在 eval-2/eval-3 的 without 臂 — 这如 AB_TEST_OPERATIONS.md 所述抬高了 baseline 表观分, 解读 with-vs-without delta 时须按语义分档扣算 (§3 已做), **不得**据「without 也命中关键点」削减断言。

---

## 5. Caveats

1. **定向新路径未被正面踩中**: v1.65.0 核心新行为是 not_applicable 短路 (零覆盖 → 跳过 (a) 轴 wait + surface 警告行)。eval-2 只提供了 covered 分支的负向验证 (with 臂正确地*不*短路); 套件内无「变更路径零 CI 覆盖」场景 (如 docs-only 变更) 直接驱动短路 + 警告行产出。建议: ab-suite 补一条 not_applicable 正路径 eval (升 MINOR), 或按 Rule #6 表 3 行以定向 fixture 补 (spec 侧 `rule6_note` 留痕)。
2. **数值零 delta 的解读**: new vs old mean 0.00 不是「无效变更」信号 — #122 是 additive gate 行为变更, 本套件三 eval 均落在旧行为保持面, 零回归即达标; 语义分档已确认新语义正向在场。
3. **without 臂分数含污染红利**: 对外部采用者的真实 skill 价值 delta 大于表观 +0.22 (eval-3 尤甚)。
4. pass 阈值 0.8 为本报告设定并全程一致使用; 换阈值只影响 without pass_rate (0.7 阈值下为 3/3), 不影响档位与 delta 结论。
5. memory/MEMORY.md 是 CLAUDE.md 之外第二个自动加载污染面 (eval-3 without 四处命中), DEC-20260722-001 重测门未覆盖它 — 建议下轮把 memory 面纳入污染检查参照面。
