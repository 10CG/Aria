# Tasks — `premerge-gate-mainbranch-failclosed`

> **Spec**: [proposal.md](./proposal.md) | **审计轨**: [audit-trail](../../../.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md)
> **Level**: 3 | **Status**: 📝 **A.2 产物 (2026-08-09 初稿 · 2026-08-10 勘正)** — 由 owner「进 Phase B, 用 TDD 接管」裁定产出; 勘正轮由**非原作者执笔**, 原作者只做独立核验
> **ship target**: **MAJOR** —— **已确认, 不再待裁** (见 proposal §版本)。承重腿是 (i) 本仓可自证的现实缺陷 (`--main-branch` 缺省 `"main"` ≠ 本仓主干 `master`) + (ii) 对外 CLI 契约由可选变必填。⚠️ 上一版写的「破坏性签名变更 / 24 处 TypeError」**已作废** —— 那 24 处全在本 skill 自测内, 不构成对外破坏面
>
> ⚠️ **本文件的性质与既往不同**: post_spec 跑满 R1–R5 (25 个 agent-run) **未收敛**, owner 裁定停止「审计→改文档」循环。五轮量化证据显示 —— 席位稳定找到真问题, 而**编排层每轮 fix 引入 73–100% 的新 Major**。⇒ 本文件**不再试图在文档层把实现钉死**, 而是把「编排层验证不了的部分」组织成 **TDD 前置 + spike**, 让缺陷在实施时自己发红。
>
> **判据**: proposal 的 SC 表钉住「什么算对」; 本文件钉住「按什么顺序让它发红」。**任何 spike 的结论回写 proposal, 不在本文件里另立规定。**

---

## 组 0 — TDD 前置 (必须先做, 且必须先看到红)

> 这五条对应 R5 后仍阻塞的项。**每条都要求先写出会红的测试, 看到红, 再实现。** 五轮实证: 这些缺陷在代码里分钟级暴露, 在文档里要五个 agent 一轮。

- [ ] **TASK-001** 建**全部机械断言的空壳**, 先跑一次确认**该红的都红**: SC-M1 (`aether ci status`=0) · SC-M2 (`"branch": "main"`=0) · **SC-M3a** (`--main-branch "<MAIN_BRANCH>"`=2) · SC-M4 (三处字面量=0/0/0) · SC-M5 (help 文案=0); 另两条负控 **SC-M3b** (无 `--main-branch main|master`) · **SC-M3c** (折叠块内不含调用) 今日已绿, 属负控。
      **验收**: 贴出实施前实跑输出证明该红的确实红。⚠️ 五轮里编排层两次写出**恒红**、一次**恒绿**的断言, 故**先验红窗**再往下走。
      ⚠️ **另须做对抗性验证**: 建「写死 `--main-branch main`」与「调用藏进折叠块」两个 fixture, **断言集必须拒绝它们** —— post_planning R1 实证上一版全套验收对 `--main-branch` 失明 (写死 main 能全过)。

- [ ] **TASK-002** **spike: helper 路径解析形态**。输入见 proposal §1 —— ⚠️ 该节的输入行**上一版整体错过一次** (变量方向反了 / 副本数错了 / 计数混口径), 已逐条更正并标注计数法, **照读 §1 表, 不要凭记忆**。
      🔴 **题目是「锚点未定论」, 不是「变量名选错」**: `SKILL.md:610` 逐字「路径相对**项目根**」 vs `:242` 逐字「**目标仓根**」(⚠️ `:242` 的作用域**限于步骤 2.5「Path coverage 评估」**, 讲的是 `evaluate_path_coverage()` 的调用上下文, **不是 C.2 合并全流程的契约**) —— 两个互斥锚点; 而两个变量都 unset 时 `${VAR:-aria}` 的回落把二者压成同一个相对路径, 换变量名**治不到它**。⇒ **先定锚点** (项目根 / 目标仓根 / 仓外安装根, 或给出显式优先序), **再**谈用什么机制表达它。
      **验收 = SC-M12**: **五种 cwd** (主仓根 / `aria` 子模块根 / `standards` 子模块根 / `aria-orchestrator` 子模块根 / **采用方仓根 —— 有 `.aria/`、无 `aria/` 无 `skills/`, 插件装在仓外**) **全部可达**; 且不可达时 abort, 但健康常态下不得 abort。
      **产出**: 形态定稿 + 回写 proposal §1。**变量归属 (`ARIA_` vs `CLAUDE_`) 是本 spike 的产出, 不是它的输入** —— 本文件与 proposal 均不预先定死 (TASK-014 依赖本条, 依赖方向不可反)。
      ⛔ **两个已被实测否决的形态都不得沿用**: (a) R4-fix 的「两分支 `git rev-parse` 解析」—— 在第 3/4/5 种 cwd 下恒红; (b)「cwd 相对多候选探测**为主路径** + 把 `CLAUDE_PLUGIN_ROOT` 降为非承重可选覆盖」—— 在第 5 种下**结构上**够不到 (实测 `/home/dev/Kairos` `/home/dev/SilkNode` 两个真实采用方都只有 `.aria/`, helper 在仓外 `~/.claude/plugins/marketplaces/10CG-aria-plugin/skills/...`), 那是原样重犯 (a) 的病。

- [ ] **TASK-003** **spike: 存在性核验的精确比对实现**。判据已定 (proposal §5): 「返回的 ref 名列表中存在 `== "refs/heads/" + main_branch` 的精确匹配」。spike 决定取列表的方式与解析形态。
      **验收 = SC-M6 + SC-M13**。SC-M13 是 R2 承重 Critical 的**真正闭合腿** —— 锚定 pattern 实现必须在此转红。
      🔴 **两条底层事实 (2026-08-10 受控裸仓实跑, 六轮审计从未浮出)**: (a) `ls-remote` **零命中亦返 `rc=0`** (传 `refs/heads/wibble` ⇒ rc=0 + 零行输出) ⇒ **判据必须落在解析出的 ref 名列表上, 不得读退出码** —— 以退出码判存在性对本 Spec 的主场景天然 fail-OPEN; (b) ⛔ **不得用 `--exit-code`** —— 实测无命中返 **rc=2**, 会被 §5 的 catch-all 误分类成 `main-branch-verify-failed` 而非 `main-branch-not-found`。
      **零命中用例 (必须单列)**: 受控裸仓远端只有 `refs/heads/master`, 传 `--main-branch develop` ⇒ 须得 `kind=="main-branch-not-found"`。⚠️ SC-M6 与 SC-M13 的场景**都有命中**, 结构上碰不到这条分支, **不能靠它们代管**; 用 `--exit-code` 的实现在此必红。

- [ ] **TASK-004** **异常/重试的复用形态 —— 主干形态已裁 (D-4, 2026-08-10), 但仍保留 spike 成分 (下列四条缺口)**。
      **复用是按轴分派的两个先例, 不是三选一** (⚠️ 把 A/B/C 框成单选是误框, 已更正): **异常轴 ← `path_coverage.py:93` 的 `(TimeoutExpired, FileNotFoundError, OSError)` 三元组枚举** · **重试轴 ← `aether.py:38` `RETRY_BACKOFF=(5,15,45)` + `:164-187` `_run_with_retry`**。
      **裁定**: `ci_backends/aether.py` **入 scope**; 把 `_run_with_retry` 的重试循环抽成与 binary/argv 无关的共享 helper, `AetherBackend._run_with_retry` 改薄包装, gate 层核验调同一个 helper。**理由**: 它的参数正是 `SKILL.md:259` 逐字规定的那套 —— 本 Spec 治的就是「同一算法两份实现」, 在其修复里造第二份是自相矛盾 (R5 两席命中)。
      ⛔ **被否决的只有「调 `path_coverage._run_git()` 函数本身」这一种读法** —— `:78-101` 把异常路径 (`:93-94`) 与非零退出码 (`:99-100`) 双双折叠成 `ok=False` ⇒ SC-M7 (128, 不重试) 与 SC-M8 (timeout, 重试 3 次) 在其返回形状上无从分辨; 且撞 §非目标。**那条 `except` 元组的枚举仍是异常轴的唯一成文先例, 不在否决范围内。**
      🔴 **四条使「薄包装 + 字节等价」低估改动面的缺口, 须在本条内解决**:
      (1) **`_run_with_retry` 结构上交付不出 §5 的 catch-all** —— `:168` docstring 逐字「other exceptions bubble up」, `:180` 只 `except TimeoutExpired`; 而 §5 兜底行要求 `FileNotFoundError`/`OSError`/输出不可解析/任何未枚举情形一律 fail ⇒ **gate 层仍必须自建异常包裹层** (用异常轴那条元组)。
      (2) **解码轴**: `aether.py:176` 用 `text=True`; gate 要跑的恰是 `git ls-remote`, 而 git **不保证** ref 名是合法 UTF-8 ⇒ `UnicodeDecodeError` 不是 `TimeoutExpired`, 不被捕, **违反 §5**。同包 `path_coverage.py:78-84` 正是为此写 bytes + `surrogateescape` (#124, docstring 逐字记载) ⇒ 共享 helper 至少要多出 **decode 策略** 与 **timeout** 两个参数。
      (3) **`cwd` 承重而 `_run_with_retry` 没有该参数** (`_run_git` 有): D3 + §5「同一个 cwd」使「`ls-remote` 跑在哪个仓」承重 —— 主仓与 `aria` 子模块**都有 `master`**, 查错仓即假通过 ⇒ 共享 helper 须显式接 `cwd`。
      (4) **超时哨兵 `return -1` (`:187`) 与信号致死的 `-1` (SIGHUP) 别名**, 而 D7 要求 gate「退出码分区自带完整表」⇒ gate 不得把 helper 的 `-1` 直接当退出码读, 须有可区分的 timeout 信号。
      **验收 = SC-M7 + SC-M8 + 针对 `_run_with_retry` 本身的新建直接用例**: (a) **只有** `TimeoutExpired` 触发重试、其余异常照旧 bubble up; (b) backoff `5/15/45` × 3 attempts (须 mock `time.sleep`); (c) 超时哨兵与真实退出码可区分。
      🔴 ⚠️ **「`test_ci_backends.py` 25 tests 保持全绿」是恒绿判据, 不得当等价证据** —— 实测 `grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 那 25 条系统性绕过它 (改 mock `subprocess.run` 或 `_query`), **异常选择行为零覆盖** ⇒ 抽取时把 `except TimeoutExpired` 放宽成三元组 (为服务 gate 的 catch-all, 这是最自然的写法) 会**静默改掉 aether 的异常契约而 25 条全绿**。⇒ 25 tests 全绿降为**必要不充分**条件。

- [ ] **TASK-005** **测试隔离接缝**。既有 `test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效** (`import subprocess` 使模块对象共享 —— 受控实验证实, 编排层早先的相反陈述已作废)。
      ⇒ 新增 gate 层 subprocess 后该守卫会**转红**。本条须建独立打桩接缝, 使守卫**保持有效而非被放宽**; 同时保证 SC-M6/SC-M13 能用真实 git 受控裸仓。**粒度 (函数级 vs subprocess 级) 由 spike 定。**

---

## 组 1 — 实现 (组 0 全绿后)

- [ ] **TASK-006** `pre_merge_gate.py` 三处字面量 (`:21` docstring / `:300` 签名 / `:427` CLI) + **help 文案**; 参数改必填。
- [ ] **TASK-007** 新增 `--remote` / `remote` 参数 (默认 `origin`)。
      **须写下失效方向不对称的理由** (R5): 错 `remote` 走 128 ⇒ fail-CLOSED; 错 `branch` 走 `runs:[]` ⇒ fail-OPEN。这就是为什么 `remote` 可以有缺省而 `main_branch` 不可以。
- [ ] **TASK-008** `_verify_branch_exists()` 按 TASK-003 定稿实现; 插入点 = 三个早退**之后**、`evaluate_path_coverage` **之前**。
- [ ] **TASK-009** 诊断信息写入 **`raw_message` (主通道, `SKILL.md:255` 逐字规定)** + `gate_error` additive 副本。
- [ ] **TASK-010** 既有 **24 处** `gate_check(` 调用补 `main_branch="master"`; `test_sc12_default_true_lock` (`:663`) 断言由 `"main"` 改 `"master"`。
      **24 的三项口径 (必须带着读)**: 总体 = `tests/test_pre_merge_gate.py` **单文件** · 范围 = 该文件全部行 · 计数法 = 含 `gate_check(` 的**行数**。放宽总体到全 `phase-c-integrator/**/*.py` 得 **31** 行 (去掉 `def gate_check(` 为 30), 多出的 6 处中 5 处是 docstring/散文提及、1 处是 CLI `:435` 的真实调用而它**已显式传参**不在本任务范围。⚠️ 不写明口径, 下一个复核者会数出 30/31 并以为 Spec 错了。

## 组 2 — SKILL.md (承重, D1)

- [ ] **TASK-011** `### 步骤执行` (:99 段) 与 `### C.2.4` (:218 段) **两处**散文流程改为 helper 调用; 5 步移入折叠块并**去掉全部可执行命令字面量**。
      ⚠️ `:99` 段的 C.2.4 条目在 `:101` 开 `:216` 闭的 **yaml 围栏内**且**没有「5 步」结构** (R5/tech-lead) —— 该处的改法须 spike, 不得照搬 `:218` 段的形态。
- [ ] **TASK-012** **步骤 6 (`:252-255`) 不动** —— 纯 AI 义务 + `DEC-20260731-001` owner 交换条件。仅在其 `fail` 分支确认 `raw_message` 会被 surface (若既有措辞已覆盖则**不加句**, 避免 no-op 编辑)。
- [ ] **TASK-013** `:270` 示例 · `:267` schema 增 `gate_error` · `:279` **四类**早退注记同步 (逐字是四类, 含 backend query 失败)。
- [ ] **TASK-014** **本 Spec 触及的 2 个 helper 定位落点 (`SKILL.md:262` `:559`) 改为 TASK-002 的定稿形态**; 其余同类形态本 change **一处不动**, 逐条转 TASK-019 follow-up (6)。
      **分界依据是「角色」不是「形态」** (三处逐字同形): `:262`/`:559` 是**无消费者的文档指针** —— 实证 `submodule_gate.sh` 的真实调用者是 `aria/hooks/submodule-gate-telemetry.sh:60-62`, 它用自己的定位逻辑, **从不读 `:559`** ⇒ 改动零行为风险。`:610` 是**可执行探测 + 降级分支**, 且其等价类有一个成员在本文件**之外** (`state-scanner/references/sync-detection.md:587` —— 与 `:262`/`:559` 同属 v1.15.2 一次按同一意图拉平的等价类) ⇒ 只改 `:610` 会**新造**一处跨文件不一致, 恰是本任务要防的病。
      **验收 —— 三条都不依赖裁量的量** (⚠️ 本任务的验收量已被换过**两次**, 作废记录见下):
      1. **旧形态命中集合封闭**: `grep -n '${ARIA_PLUGIN_ROOT:-aria}/skills/' SKILL.md` 的命中集合**恰为 `{:610}`**。今日实测 = **`{:262, :559, :610}`** ⇒ 实施前必红; 只改一处、或别处新增一条旧形态, 亦红。
      2. **`:262` 与 `:559` 各恰 1 处 TASK-002 定稿形态** (不是 0, 也不是 2)。
      3. **负控 (封闭白名单, 之外零例外)**: `:310` · `:392` · `:557` · `:610` · `:737` 在本 change 的 diff 中**零改动**。内容锚 (落地时按锚重定位): `:310` = `**Backend 抽象**` 段里裸 `aria/skills/.../ci_backends/` · `:392` = ``**执行流程** (Bash gate, 见 `scripts/submodule_gate.sh`)`` · `:557` = v1.28.0 host-cron 段的 `scripts/submodule-tripwire-audit.sh` · `:610` = `**降级策略**` 段 · `:737` = `${CLAUDE_PLUGIN_ROOT:-aria}/skills/aria-token-telemetry/...`。
      ⚠️ **行号必然位移**: TASK-011 改动 `:99-:216` 与 `:218` 起两段 ⇒ `:262+` 全部前后移。验收一律**按内容锚重定位, 不得按行号核**。
      🔴 **声明留痕必须写到这个精度**: 实施后不是「文件里并存两套约定」, 而是「**一套经五-cwd 认证 (`:262`/`:559`) + 一套实测在多数 cwd 不可达 (`:610`)**」。后者比「看着不一致」硬得多, 须在 TASK-019 (6) 的 issue 正文里逐字写出, 不得含糊成「风格不统一」。
      **`:559` 现在就改的硬理由**: TASK-019 第 (5) 项要把 C.2.4.5 的 `SKILL.md:189-191` 裸 git 命令收敛为 `submodule_gate.sh` 调用 —— **那一天 `:559` 就从「无消费者的文档指针」升级为「定位依据」**。现在顺手同步比那时再补划算。
      ⚠️ **两条已作废的验收量, 留痕防复发**: (a) 初版「`:262`/`:559`/`:610` 全文无互斥两套」—— 今日已假, 同一文件实存 **4 套**形态 (`${ARIA_...}` `:262`/`:559`/`:610` · 裸 `aria/` `:310` · skill 目录相对 `:392`/`:557` · `${CLAUDE_...}` `:737`), 照写只有恒红或被静默重解释成假绿两种结局; (b) 勘正轮一度改成「本 Spec 触及的 **2** 个落点全部为定稿形态」—— **同样 false-by-construction**: `SC-M3a` 逐字要求实施后**新增 2 条**携带新形态的 helper 调用 ⇒「新形态出现数」实为 **4** 而非 2; 且「哪些行算本 skill 自有 helper 指针」不是机械可判集合 (新增 2 条指向 `pre_merge_gate.py`, 而 `:310` 指向 `ci_backends/` —— 更近承重对象), 两个独立实施者会得出不同覆盖集 (memory `spec-underdetermination`)。
      **今日另发现一处未被上述任何枚举覆盖的同类**: `:742` = markdown 相对链接 `../session-closer/scripts/closeout_trigger.py`。判定**不入本任务** —— 它是文档链接不是执行路径, 不参与 helper 定位, 故既不进白名单也不进负控; 若复核认为同类, 转 TASK-019 (6), **不要塞回本任务**。

## 组 3 — 合规与同步面

- [ ] **TASK-015** **Rule #6 照跑 AB** (判据表第二行, 零裁量): `ab-suite/phase-c-integrator.json` + `phase-c-integrator-pre-merge-gate.json`, 结果存 `ab-results/`。**不得以「套件覆盖薄」降档。**
- [ ] **TASK-016** `CLAUDE.md` 规则 #8 同步 —— 本 change 新增第三条阻断腿。先例: `commit 7661e96` (v1.31.0 在同一提交同步过)。
- [ ] **TASK-017** 发版同步面: **整仓引用点差集**枚举 (非文件白名单), 类级根因见 **Aria #177**。
- [ ] **TASK-018** blast-radius 核验 (含 `pre-merge gate` 这个不含下划线的写法, 否则搜不到 `CLAUDE.md`); 外部采用方 (Kairos 等) 通告项。
- [ ] **TASK-020** **v2.0 弃用到期承诺的承接 —— 条件任务 (触发条件: `ship_target == MAJOR`)**。**该条件已于 2026-08-10 满足** (裁定确认 MAJOR ⇒ v2.0.0) ⇒ 本任务**当前生效**。⚠️ **条件性不得抹掉**: 若 `ship_target` 在 handoff 复议中被改档, 整条 **cancelled 并在本文件留痕**, 不得静默删除。
      **删除面跨两个仓、5 个文件、两个 legacy key** —— `_OLD_TO_NEW` 实读有**两个** key (`primitive_preference`→`ci_backends` **和** `no_aether_fallback`→`no_ci_fallback`; Spec 早先版本只谈了前者):
      `pre_merge_gate.py` (键名 **6** 行 / 承诺措辞 **2** 行) · `phase-c-integrator/SKILL.md` (**6** / **4**) · `config-loader/SKILL.md` (**2** / **2**) · `tests/test_pre_merge_gate.py` (**17** / **3**) · **主仓 `.aria/config.template.json` (**2** / 0, 即 `:75` `:78`)**。
      ⚠️ **枚举命令必须中英并列, 否则枚举本身 fail-OPEN**: `SKILL.md:49` 逐字是「alias **仍读**, 发 deprecation warning, **v2.0 移除**」—— 单跑 `grep 'removed in v2.0'` 抓不到它。口径 = 键名面 `grep -nE 'no_aether_fallback|primitive_preference'` **加** 承诺面 `grep -nE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除'`, **两条都跑**。
      🔴 **fail-CLOSED**: v2.0 后 legacy key 在场**必须发红**, 不得静默忽略。理由要按精确口径写: 模板 `:75-77` 的 `primitive_preference: ["aether-ci-cli"]` **恰等于** `ci_backends/__init__.py:17` auto-detect 首位, `:78` 的 `"skip_with_warning"` **恰等于** `pre_merge_gate.py:56` `DEFAULT_CONFIG` ⇒ 对**逐字照抄模板者**删 alias 近乎 no-op; 真正会漂移的是**改过这些值**的采用方 (设了 `no_aether_fallback: "abort"` 的会被无声换回 `skip_with_warning`) —— **静默忽略恰好对他们是 fail-OPEN**。⛔ **不得写成「所有采用方都会炸」那类不可证伪的主张。**
      🔴 **红必须落在既有被路由的通道上**: 实测 `grep -rn 'gate_error' aria/` = **0 命中**, 且 `workflow-runner/SKILL.md:354-357` 的 verdict 路由只有四条臂 (green / fail / timeout / Ctrl-C), **没有「gate 抛异常」这条臂** ⇒ 直接 `raise` 会落进无人接住的路径, 即**在自己新写的兜底里重犯本 Spec 要治的病**。⇒ 硬失败走 **`verdict="fail"` + `raw_message`** (`SKILL.md:255` 逐字规定的 surface 通道); 若最终仍要抛异常, 须**先**在 `workflow-runner` 加对应臂, 并把它写进本任务 deliverables。
      🔴 **错误文案必须指路** (仓内范例 `ci_backends/github_actions.py:37-42` 的 NotImplementedError 逐字给出出口「set `ci_backends: []` in `.aria/config.json` to explicitly disable」): `raw_message` 须逐字含 (a) 命中的 legacy key 名 · (b) 对应新键名 · (c) 一条可照做的改法。**缺任一即红** —— 否则采用方拿到的是一个无出口的硬失败。
      ⚠️ **模板必须同批改**, 否则每个新采用方一开箱就撞硬失败。
      **已核, 判定不入删除面**: `aria-plugin-benchmarks/aria-ci-backend-abstraction/README.md:103`/`:215` —— 那是 AB 归档材料对**已完成迁移**的记述 (逐字 "Rewritten (key `no_aether_fallback` → `no_ci_fallback`)" 与一条历史 warning 文案), 不是「仍可读」的在效承诺; 且改动 benchmark 材料会污染 AB baseline (CLAUDE.md #116)。

## 组 4 — follow-up issue (本 Spec 不修)

- [ ] **TASK-019** 开 issue: (1) `main_branch` 自动解析设计面 (R2 实测 `ls-remote --symref` 有 RC=0 无 `ref:` 行两态); (2) `fetch_gate.py` 字面 `("master","main")` 回落 + `worktree_manager.py:170` 同形; (3) `workflow-runner` `gate_state` 无 `gate_error` 位置; (4)「显式传错分支名」此前零测试覆盖; (5) **C.2.4.5 的 `SKILL.md:189-191` 裸 git 命令 + `submodule_gate.sh`** —— 与 D1 根因**同类**的最近兄弟 (R5/code-reviewer); (6) **helper 定位形态的其余落点** (TASK-014 刻意不动的那些): `SKILL.md:310` (裸 `aria/`) · `:392` `:557` (skill 目录相对) · `:610` (`ARIA_` + 可执行探测/降级分支) · `:737` (`CLAUDE_`) · **跨文件** `state-scanner/references/sync-detection.md:587` —— 后者与 `:262`/`:559` 同属 v1.15.2 一次按同一意图拉平的等价类, 只改一半会劈开它。
      ⚠️ (3) 补一条实测输入: `grep -rn 'gate_error' aria/` = **0 命中**, `workflow-runner/SKILL.md:354-357` 的 verdict 路由只有四条臂, **无「gate 抛异常」臂** —— issue 正文须带上这两个数, 否则读者无从判断缺口大小。

---

## 已裁 (原「未决」四条, 2026-08-10 结清)

> ✅ **已闭 (2026-08-09)**: `detailed-tasks.yaml` 已建 (owner 裁定「写」); `post_planning` 已跑 R1 (owner 裁定「跑」)。
> 原「detailed-tasks.yaml 是否补」的真正待决项是 **`standards/openspec/project.md` 自身 `:21` (双层) 与 `:118` (单层) 两处表述矛盾** —— 应转记给 standards 维护者, 不属本 Spec (TASK-019 已纳入)。
>
> 🔴 **Rule #10 留痕**: 下列四条原标注「须 owner 裁」。owner 于 2026-08-10 session 显式授权 AI 依调研结论定夺, **故这四条是 AI 作出的裁定, 不是 owner 的逐条签字** —— **全部须写入 handoff 请复议**。

1. ✅ **版本 = MAJOR** (D-1)。承重腿**已换**: 上一版用的「24 处 `gate_check(` TypeError」实测全在本 skill 自测内, 不构成对外破坏面; 改为 (i) 本仓可自证的现实缺陷 (缺省 `"main"` ≠ 本仓主干 `master`) + (ii) 对外 CLI 契约变更。详见 proposal §版本。⇒ **TASK-020 的触发条件已满足, 当前生效** —— 但它**仍是条件任务**, 复议改档则整条 cancelled 留痕 (条件性不得抹掉)。
2. ✅ **变量归属 = 不在本文件裁, 由 TASK-002 spike 产出** (D-2, 经对抗复核**改口**)。真正的病灶是 **`:610`「项目根」 vs `:242`「目标仓根」两个互斥锚点**, 换变量名治不到它 ⇒ 先定锚点再定机制。
   ⛔ 曾一度倾向的「退役 `ARIA_PLUGIN_ROOT` + 把 `CLAUDE_PLUGIN_ROOT` 降为非承重」**已被实测否决** —— `CLAUDE_PLUGIN_ROOT` 是目前唯一能指向仓外安装根的机制, 降级它会让承重路径在采用方仓根 (第 5 种 cwd) 下**结构上不可达**, 即原样重犯 R5 杀掉的那条恒红。
3. ✅ **TASK-014 覆盖 `:262` + `:559`, 不覆盖 `:610`** (D-3 的**覆盖集**存活, 但**验收量被证伪并第二次换掉**)。分界依据是角色不是形态 (三处逐字同形): 前两者是无消费者的文档指针 (零行为风险), `:610` 是可执行探测 + 降级分支且其等价类跨到 `state-scanner` ⇒ 转 TASK-019 (6)。
   🔴 **验收量换过两次, 两次作废理由都在 TASK-014 正文留痕**: 初版「全文无互斥两套」今日实测已假 (4 套形态并存); D-3 给的替代「2 个落点全部为定稿形态」**同样 false-by-construction** (SC-M3a 要求新增 2 条新形态调用 ⇒ 实为 4; 且覆盖集不是机械可判集合)。现行量 = **旧形态命中集合恰为 `{:610}`** + **`:262`/`:559` 各恰 1 处新形态** + **封闭白名单负控**。
   ⚠️ 实施后的真实状态是「**一套经五-cwd 认证 + 一套实测在多数 cwd 不可达**」, 不是「两套约定」—— 留痕必须写到这个精度。
4. ✅ **`ci_backends/aether.py` 入 scope** (D-4 方向存活, 但**四处不完整已补**)。只抽 `_run_with_retry` (`:164-187`) 的重试循环为共享 helper, 自身改薄包装; `scope_repos.paths` 已同步补入。
   🔴 **等价判据已换量**: 曾写「`test_ci_backends.py` 25 tests 全绿」—— 实测 `grep -c '_run_with_retry'` 该文件 = **0**, 那 25 条系统性绕过它 ⇒ 该判据**恒绿**。改为针对 `_run_with_retry` 本身的新建直接用例 (详见 TASK-004)。
   🔴 **另补四条缺口**: 复用是**双轴分派**非三选一 (异常轴 ← `path_coverage.py:93` 元组枚举 / 重试轴 ← `aether.py`) · `_run_with_retry` 交付不出 §5 catch-all (只捕 `TimeoutExpired`) · `text=True` 的 `UnicodeDecodeError` 未被考虑 (#124) · `cwd` 与超时哨兵 `-1` 两个参数缺口。
   ⚠️ 该条的席位自评为 **medium 置信**, 是四条里最该被复议的一条。
