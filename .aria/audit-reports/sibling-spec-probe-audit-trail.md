# sibling-spec-probe — 审计轨 (append-only)

> **本文件是 `openspec/changes/sibling-spec-probe/proposal.md` 的审计史与核验证据**, 由主控于 2026-08-25 按
> 姊妹 Spec `linked-issue-normalization` (owner 2026-08-07 裁定「交付面与审计史切开」) 的体例切出。
> **按字节搬运, 未重写任何一句**, 只加了本文件头部与下方节标题 —— 主控搬迁时用程序逐行断言
> 「原内容每一行都 `in` 新文件」, 结果**缺失行 0**。
> **⚠️ 该断言的可证伪性边界 (R3/CR-M-M1 订正)**: 本文件的内容在被搬出前**从未提交过**,
> 因此**不存在可供第三方 diff 的已提交前身** —— 上述无损断言是主控对搬迁**前后工作树**做的,
> 真实但**结构性不可独立复核**。读者若要复核, 只能核对本文件与 proposal 存根所述范围是否自洽。
>
> ⚠️ 本文件 **append-only**, 且**显式不维护与 proposal 的一致性**; 二者不一致时**以 proposal 为准**,
> **不得**因本文件的历史记述而回改 proposal。

---

## §1 事实断言逐条实读清单 (2026-08-25 起草时实测, 基线 aria `d50f9c3` / 主仓 `cc1bdef`)

> **方法**: 本 Spec 全文引用的每一条 `文件:行号` / 函数名 / 文件存在性 / 度量数字, 都在下表给出**可复跑的命令**与**本轮实跑结果**。
> **实读环境**: 主仓 `cc1bdef` (2026-08-25); aria 子模块引用一律以 **`d50f9c3`** 为准 (= `origin/master`); 本机 `git version 2.39.5`。
> **⚠️ 母 Spec `proposal.md` 正在被另一执笔席并发修改** ⇒ 语料类度量一律跑在**已提交的 `cc1bdef`** 上, 不跑工作树, 结果不受并发影响。
> **⚠️ 承接自 spike S2 的 fetch 耗时 (~13.8s / 3 轮净增 ~41s) 与 `handoff_multibranch` 的 440 分支先例, 是历史一次性测量, 本轮未复跑** —— 标注为承接, 不冒充本轮实测。

| # | 断言 | 命令 | 本轮结果 |
|---|------|------|---------|
| 1 | `normalize_linked_issue` 的确切签名与返回契约 | `git -C aria show d50f9c3:skills/state-scanner/lib/collision.py \| sed -n '178,229p'` | `def normalize_linked_issue(value: str) -> "Optional[tuple[str, int]]"`; key = `(repo_basename, number)`, org 不参与; 三类不可解析值返回 `None`; docstring 逐字「Callers must fall back to raw-string equality on `None` — never treat `None` as "no match"」。其下 `_linked_issue_matches` (私有) 实现 rule 4/5 |
| 2 | `ab-suite/audit-engine.json` 存在性 | `ls aria-plugin-benchmarks/ab-suite/` + `test -f .../audit-engine.json` | **NOT EXISTS**。目录实测含 **31** 个 `.json` + **4** 个子目录 + `version.yaml`; `phase-a-planner.json` / `spec-drafter.json` / `state-scanner.json` 均在 |
| 3 | 本仓 `github` 无本地 symbolic-ref | `git symbolic-ref refs/remotes/github/HEAD; echo $?` | `fatal: ref refs/remotes/github/HEAD is not a symbolic ref` / **exit 128** |
| 4 | 本仓 `origin` 有本地 symbolic-ref | `git symbolic-ref refs/remotes/origin/HEAD; echo $?` | `refs/remotes/origin/master` / **exit 0** |
| 5 | `ls-remote --symref` 对 `github` 可用 | `time git ls-remote --symref github HEAD` | `ref: refs/heads/master<TAB>HEAD` + SHA 行; **real 4.506s** |
| 6 | `ls-remote --symref` 对 `origin` 可用 | `time git ls-remote --symref origin HEAD` | `ref: refs/heads/master<TAB>HEAD`; **real 5.961s** |
| 7 | `aria` 子模块同款故障 | `git -C aria symbolic-ref refs/remotes/github/HEAD; echo $?` | `fatal: ... is not a symbolic ref` / **exit 128** |
| 8 | `aria` 子模块上 `ls-remote --symref` 可用 | `git -C aria ls-remote --symref github HEAD` | `ref: refs/heads/master<TAB>HEAD` + `d50f9c3a...` |
| 9 | 本机 git 不会由 fetch 补写 remote HEAD | `git --version` ; `man git-fetch \| grep -c followRemoteHEAD` | `git version 2.39.5` ; **0** (该配置项在本版本 man 页不存在) |
| 10 | `ls-remote` 失败的退出码 | `git ls-remote --symref nosuchremote HEAD >/dev/null 2>&1; echo $?` | **128** (⚠️ 注: 若把它放进管道再取 `$?`, 拿到的是管道末端的码 —— 实现须直接取子进程返回码) |
| 11 | 配置面 vs ref 面的 remote 集合不等 | `git remote` ; `git for-each-ref refs/remotes/ \| cut -d/ -f3 \| sort -u` ; `git config --get remote.probe.url; echo $?` | `git remote` = `github` `origin`; ref 面 = `github` `origin` **`probe`**; `remote.probe.url` **无输出 / exit 1** |
| 12 | `resolve_enforced_remotes` 的签名与语义 | `git -C aria show d50f9c3:skills/state-scanner/scripts/collectors/multi_remote.py \| grep -n "def resolve_enforced_remotes" -A 32` | `:255-286`; `(configured, actual_remotes, read_only=()) -> (enforced, no_matching)`; docstring 逐字「an EMPTY list `[]` OR `None` means **AUTO-DISCOVER all remotes**, NOT the empty set」 |
| 13 | scan cap 的披露形态先例 | `git -C aria show d50f9c3:.../handoff_multibranch.py \| sed -n '586,600p'` + `skills/state-scanner/scripts/collectors/_common.py` (**主控消歧**: 全仓两个同名 `_common.py`; `def resolve_max_branches_scanned` 实读在 `d50f9c3:skills/state-scanner/scripts/collectors/_common.py:175`) `grep -n "def resolve_max_branches_scanned" -A 12` | `:589-598` = `soft_error("handoff_multibranch_branch_cap", ...)` + `log.warning` + 逐字消息含总数/cap/保留数; `_common.py:175-187` = 三层优先级 (env > config > 默认 20) |
| 14 | 语料规模与字段合规率 (基线 `cc1bdef`, 不含工作树) | `find openspec -name proposal.md \| wc -l` ; `git grep -n '\*\*关联 Issue\*\*:' cc1bdef -- 'openspec/**/proposal.md'` | 语料 **147** 篇 (`changes/` 7 + `archive/` 140)。字段行: **宽松** grep `'\*\*关联 Issue\*\*:'` 得 **15** 条 / 15 文件; **层 0 的行首规则** `'^> \*\*关联 Issue\*\*:'` 得 **14** 条 —— 差的那 1 条正是母 Spec `:75` 的嵌套引用示例。14 条按冒号后首字符分布: `[` 7 · `F` 4 · `a` 2 · `无` 1 · **反引号 0** ⇒ **canonical 合规 = 0 条** |
| 15 | §3 谓词原型实跑 (加载 `d50f9c3` 的真实 `normalize_linked_issue`) | 见 §实读清单脚注 A | `archive/2026-07-31-...:6` → `URL_FALLBACK` → `{('k','aria-plugin',122)}`; `archive/2026-08-22-...:22` → 同; **交集非空 ⇒ 命中**。坏实现「行内任意位置第一个 code span」在前者上抽到 **`'confirmed'`**。`normalize_linked_issue('无')` → **`None`**; `normalize('10CG/aria-plugin#122')` 与 `normalize('10CG/aria-plugin #122')` 均 → `('aria-plugin', 122)` |
| 16 | 全语料分层分布与命中簇 + **三种定位规则对照** | 同脚注 A, 在 `cc1bdef` 上扫全部 147 篇, 分别用「宽松 / 行首 `> ` / 行首+仅头部区」三种层 0 定位规则各跑一遍 | **本 Spec 采用的行首 `> ` 规则**: `no_field` **133** / `url_fallback` **13** / `no_token_no_url` **1** (合计 147); 可见 proposal **13** 篇; 同 key 簇 **3** 个 —— `("k","aria-plugin",95)` / `(…,122)` / `(…,137)`, 各 2 份, **全部在 `archive/`**。**宽松规则**: `url_fallback` 升到 14, `#122` 簇混入 `a1-entry-claim-duplicate-work-guard` (**假阳性**, 其 `cc1bdef:75` 是一行嵌套引用示例)。**行首+仅头部区**: `url_fallback` 降到 10, **簇只剩 1 个** (`#122` 与 `#95` 两个真簇被误杀) |
| 17 | 本地扫描代价 | `time git ls-tree -r --name-only origin/master -- openspec/ \| grep -c '/proposal\.md$'` ; `time git grep -n '\*\*关联 Issue\*\*:' github/master -- 'openspec/*/*/proposal.md'` ; 循环全部 11 条远端跟踪 ref | ls-tree **147 条 / 5ms**; git grep **15 行 / 12ms**; 11 条 ref 全扫合计 **151ms** |
| 18 | audit-engine 的 Step 0 是一次性 | `git -C aria show d50f9c3:skills/audit-engine/SKILL.md \| sed -n '80,100p'` | `:83` = `### Step 0: Anchor 固化 (Drift Guard #17, v1.44.0)`; `:85` 逐字「入口逻辑完成后、**Round 1 启动前一次性**执行」 |
| 19 | 两个模式块的位置 | `git -C aria show d50f9c3:.../execution-modes.md \| grep -n "^##"` ; `\| wc -l` | `:84` `## Convergence 模式`; `:113` `## Challenge 模式`; 全文 **144** 行 |
| 20 | 下游 Level-3 走 Challenge | `git -C aria show d50f9c3:skills/config-loader/DEFAULTS.json \| sed -n '118,132p'` | `:124-128` = `"adaptive_rules": { "level_1": "off", "level_2": "convergence", "level_3": "challenge" }` |
| 21 | 新建 tests 目录会被自动发现 | `git -C aria show d50f9c3:skills/run_all_tests.sh \| sed -n '48,72p'` | `:48` `for tests_dir in $(find "$SKILLS_DIR" -type d -name tests \| sort); do`; `:50` 无 `test_*.py` 则 `continue`; `:71` `python3 -m unittest discover -s . -p "test_*.py"` 兜底 |
| 22 | `remote_refresh` 缓存的唯一写入链 | `git -C aria grep -n "_write_cache_atomic" d50f9c3 -- 'skills/**/*.py'` ; `grep -n "^def " \| awk '$1<=691'` ; `git -C aria grep -n "collect_remote_refresh" d50f9c3` | 写入 `remote_refresh.py:691` (def 在 `:227`), 位于 `collect_remote_refresh()` (`:568`); 该函数**唯一生产调用点** = `scan.py:312` (其余命中为 `__init__.py` 导出与 tests) |
| 23 | 既有默认分支解析器是 origin 硬编码 + 名字猜测 | `git -C aria show d50f9c3:skills/phase-d-closer/scripts/fetch_gate.py \| sed -n '46,140p'` | `:50-54` `_ORIGIN_HEAD_REFS` 三候选全为 `refs/remotes/origin/*`; `:55` `_DEFAULT_BRANCH_FALLBACKS = ("master", "main")`; `:108-128` `_resolve_default_branch` 末端按名字猜; `:86-101` `_classify_error` docstring 逐字「Raw stderr is intentionally never returned — remote URLs in stderr may embed credentials」, 枚举 `network\|auth_403\|non_ff\|git_missing\|other` |
| 24 | `sync.py` 上**没有** `_resolve_default_branch` | `git -C aria show d50f9c3:.../collectors/sync.py \| grep -n "^def "` | 8 个顶层 def, **无** `_resolve_default_branch`; 只有同族常量 `_ORIGIN_HEAD_REFS:46` (用于 `:384` 的子模块 remote_commit 回落链) ⇒ `fetch_gate.py:23` (逐字「state-scanner sync.py::_resolve_default_branch (module-private, other skill)」) 与 `:111` 的引用都是悬空名 (记 follow-up) |
| 25 | 报告的轮次记录模板 | `git -C aria show d50f9c3:.../report-format.md \| sed -n '50,73p'` | `:50` `## 轮次记录`; `:52/:58/:67` `### Round 1` / `### Round 2` / `### Round N (Final)`, 每项为 `- Agents:` / `- Conclusions:` / `- Vote:` / `- Duration:` 列表 |
| 26 | `#150` 的号与标题 | `.aria/state-snapshot.json` → `issue_status.repos["10CG/aria-plugin"].items` (fetched_at `2026-08-23T18:21:38Z`, `source: "live"`) | **`10CG/aria-plugin#150`** = 「[benchmark] Rule #6 判据表第三行的兜底「缺一照跑」对 14/43 个 skill 结构上不可执行 — 它们根本没有 AB 套件」; 同源另有 **#157** 「[benchmark][state-scanner] ab-suite 对 SKILL.md Layer L / --linked-issue 段零覆盖」 |
| 27 | `refs/aria/*` 私有命名空间已在用 | `git for-each-ref --format='%(refname)' \| grep '^refs/aria/'` | 3 条: `refs/aria/coord-check` / `refs/aria/coordination` / `refs/aria/coordination-remote` |
| 28 | audit-engine 现无 `scripts/` 与 `tests/` | `git -C aria ls-tree -r --name-only d50f9c3 \| grep "^skills/audit-engine/"` | 8 个文件: `SKILL.md` + `references/` 下 7 个 `.md`。**无 `scripts/`, 无 `tests/`** |

**脚注 A — #15/#16 的原型脚本**: 以 `git -C aria show d50f9c3:skills/state-scanner/lib/collision.py` 的源码切片 (从 `def normalize_linked_issue` 到 `def linked_issue_overlaps` 之前) `exec` 出真实的 `normalize_linked_issue`, 再按 §3 的四层顺序对语料求键并两两求交。切片而非整模块导入的原因: `collision.py:46` 有包内相对 import (`from .claim_schema import ClaimRecord`), 单文件 `exec` 无法解析 —— **这不影响结论**, 因为被测的两个函数是纯函数、无模块级依赖。

---



---

## 2. 2026-08-30 round-3 落版清单 (R5/C1, M2, M3, m1; SC-19/20 入表; 哨兵集合镜像), append-only

> 裁定见决策单 `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`。原文由 git 历史保留, 本节只记「改了什么、为什么」。

| 落点 | 改动 | 来源 |
|---|---|---|
| Status 行 / 头部 `Linked Issue: none` | 轮次口径 + dogfood 英文 canonical | 决策单 3b / 6i |
| §3 层 0 / 映射表 / 层 2 触发集 / 层 1.5 / P5 / dogfood 观察 / SC-9·10·11 / `own_layer` | 哨兵集合 `{none, 无}` 镜像姊妹 §2; `"wu_empty"` → `"none_sentinel"`; 层 0 两拼写 | 6i / O-2 (姊妹定义, 本 Spec 引用) |
| §8 | 插入串从 9 字名词短语改为**可执行两行** (命令行 + verdict 三档消费), 首行前缀保留供 SC-17 计数; 补 SC-17 保守性说明 (m1); SKILL.md 概述 + `execution-modes.md` 权威版分工 (M3) | R5/C1, M3, m1; 母 D17 |
| SC 表 | **SC-19** (placeholder 常量黑名单, 原只在映射表格内提及) 与 **SC-20** (SKILL.md 小节四字面量 + 完整命令行, 块边界) 入表 | R4/C-M3 + 姊妹 K8; R5/C1 |
| Impact | 探针 CLI 入参 `--own-spec-dir` / `--repo-path`; SKILL.md 与 execution-modes.md 两行按 C1/M3 改写; `:519`「复制或 import 由 A.2 定」改为指向 §3 import 块 + `resolve_enforced_remotes` 经 `state-scanner/scripts` 路径 import (M2: 同文件两处相反指令) | R5/C1, M2, M3 |
| 新表面 #8–#10 / 闸门状态 | 给 R6 的输入 | — |

---

## 3. 2026-08-30 post_spec R6 清账清单 (round-3.1), append-only

> 聚合与逐条处置见 `.aria/audit-reports/post_spec-R6-1788084727388-a1-entry-combined-aggregated.md`。

| 落点 | 改动 | 来源 |
|---|---|---|
| §3 import 代码块 + 已知限 | 唯一代码块钉死两条 `sys.path` 插入顺序 (`_SS_SCRIPTS` 先插、`_SS_ROOT` 后插即排前) 与三条 import; 已知限改为「同名包 `scripts/lib` 今天就存在」; Impact 段不再复述 | BA 探针 M1 |
| SC 表 | **新增 SC-21** (import 顺序断言); SC-17 改分块计数 + 负控「其余 0 次」; SC-20 锚定标题起首 (禁 `Step 0.5:` 前缀) + (ii) 契约节存在断言; 编号说明补「旧 SC-NN 指母 Spec」 | BA M1 / TL M7 M8 m7 / CR 探针 m1 m2 |
| §3 层 1 / 对 E6 的引述 | `:116` 写死判据改哨兵集合; `:186` 改引 E6 四态表 | CR 探针 M1 |
| §4/§5 `read_only` | 来源钉为 `.aria/config.json` `state_scanner.multi_remote.read_only_remotes` (`multi_remote.py:1376`) | CR 探针 m3 |
| Impact execution-modes 行 | 契约节不得出现前缀字面 (SC-17 负控); 存在由 SC-20 (ii) 钉 | TL M7 / M8 |
| 杂项 | 「请 R4 优先审」→「请审计席优先审」; 段尾「最实的跨 Spec 风险」句标为历史; `:236-237` → `:237` | TL m6 / CR 探针 m1 |
| 闸门状态 / 新表面 | 待裁 (2 项): P11 + 依赖方向 (接缝 C2, 执笔倾向硬前置); 新表面 #10 改为「已实测顺序敏感, 已钉死」 | CR 接缝 C2 / BA M1 |
