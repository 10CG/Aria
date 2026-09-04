# sibling-spec-probe — Tasks (per-round 竞品 spec 探针)

> **Spec**: [proposal.md](./proposal.md) (578 行, round-3.2; owner 2026-08-30 批准进 A.2)
> **Level**: 2 (Spec 自评) — 本文件为 A.2 派生的粗粒度清单, 细粒度见 [detailed-tasks.yaml](./detailed-tasks.yaml) (`datasource: tasks.md`)
> **Status**: ✅ **Shipped 2026-09-04 — 18/18 done** (owner 授权后: aria v1.69.0 `2eca24b` + tag v1.68.2/v1.69.0 双推核验; 主仓 PR #191 merged `be4417b`, 两端 master MATCH) (post_planning R1 FAIL → R2 PwW → R3 PwW → **R4 CONVERGED 2026-08-31 (五席 5/5 PASS, 0C 0M)**; Amendment A1 2026-09-03) — 原文: 全部任务 `pending`, ready for B.1 (硬前置: 字段 Spec 先 ship; P11 = 扩 / 版本档 = MINOR 各占一号, 均已裁 2026-09-01, 决策单 `2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`)
> **代码落点**: `aria/` 子模块 `skills/audit-engine/` (新建 `scripts/` + `tests/`) + `aria-plugin-benchmarks/ab-suite/audit-engine.json` (新建); 本 Spec 文件落主仓 (Rule #5)
> **实读基线 (A.2 当日)**: 主仓 `c120f9e` / aria 子模块 `d69091d` (v1.67.2) / standards `334c609`。proposal 正文行号基线 = aria `d50f9c3` + 主仓 `cc1bdef`; A.2 逐条复核结果见 detailed-tasks.yaml `metadata.line_anchor_recheck` (全部一致, 语料数 147→149 为已知漂移)
> **硬前置 (owner 2026-08-30 裁 O-4 (i) / R6-1 (i))**: 姊妹 Spec `linked-issue-field-availability` 的纯函数 `aria/skills/state-scanner/lib/linked_issue_field.py::extract_linked_issue_field(text) -> FieldVerdict` **今天不存在** (A.2 实测 `ls` 无该文件)。**1.1 未 done ⇒ 本 Spec 不进 B.2**; 不得自建替身。
> **编号不可变**: `N.M` 一经确立不改 (DUAL_LAYER_SPEC §编号不可变约束); 取消用 `(CANCELLED)` 保号, 新增追加末尾。
> **排序依据**: 硬前置断言 → 测试先行 (RED) → 实现 (GREEN) → audit-engine 指令面接线 → Rule #6 照跑 + 发布同步。**例外**: 1.3 (建 AB 套件文件) 按 proposal :473 是 **Phase B.1 的前置断言**, 故编入第 1 组; 套件的**双臂实跑**留在 5.1 (需 with_skill 臂 = 4.x 产物)。
> **同文件串行 (R1 C1, memory `workflow-file-domain`)**: 凡两任务 deliverables 含同一路径, 后者依赖前者 —— 2.2→2.3→2.4→2.5→2.6 共写 `tests/test_sibling_spec_probe.py` (链式, 不合并任务), 3.1→3.2→3.3→3.4 共写 `scripts/sibling_spec_probe.py`, 3.5 收口两文件; 边已落 detailed-tasks.yaml `dependencies`, `execution_order` 里「并行」只剩第 1 组 (三任务不同文件)。设计/夹具内容可并行构思, 落盘须串行, 不得派给独立并发 subagent。

---

## Task Group Overview

| Group | 主题 | Scope ref |
|-------|------|-----------|
| 1 | 前置断言 + B.1 门 (姊妹模块存在 / 基线三态 / AB 套件文件) | §1 依赖方向第 3 条 · rule6_note 第 2 条 (:468, :473) · memory `check-runs-at-baseline-first` |
| 2 | TDD — `tests/test_sibling_spec_probe.py` (RED first; 承载 SC-1~15 / 17 / 18 / 19 / 20 / 21 / 22~25 (P11)) | Success Criteria 表 · §3 跨 skill import 唯一代码块 · A.2 显式约束 (:171) |
| 3 | 实现 — `scripts/sibling_spec_probe.py` (stdlib-only; §3 谓词 / §4 默认分支 / §5 fetch / §6 cap / §7 契约) | §1–§7 · 决策 P1–P11 |
| 4 | audit-engine 指令面接线 (execution-modes.md 两块 + 契约节 / SKILL.md 小节 / report-format.md 模板行) | §8 · §9 · Impact 表 · rule6_note 点名行为 α/β |
| 5 | Rule #6 照跑 (with/without 双臂 + 坏实现负控) + 发布同步面 | rule6_note · CLAUDE.md Rule #6 / §版本管理 |

> **组间门 (每条都有 yaml 边, 不再只是散文 — R1 C1 第 3 条 / A3 98e71a6a)**: 1.1 (TASK-001) 阻塞 2.x 起的一切 (边: TASK-004~009 `dependencies` 各含 TASK-001; import 目标不存在 ⇒ 探针无宿主, 测试骨架的模块级 skip 守卫也以它为前提); 1.3 (TASK-003) 是 B.1 前置 (proposal :473 逐字: 「该任务未 done 则 Phase B.1 不得开始」 — 边: TASK-004 (第 2 组起点, 主控 R1 追记) / 015 / 016 / 017 的 `dependencies` 各含 TASK-003, 且 TASK-003 ← TASK-002 (R3/A4 10e7cea4 补); 边: TASK-015 / 016 / 017 `dependencies` 各含 TASK-003, 原 R1 裁量落第 4/5 组, R3 起改落第 2 组起点 TASK-004 (见前句)); 2.x 全部 RED 后才进 3.x (3.1 边 ← 2.1 + 2.5, 经串行链传递覆盖 2.2~2.5); 3.5 GREEN 后才进 4.x (3.5 边 ← 2.6 + 3.2~3.4); 5.1 需 1.3 + 3.5 + 4.1 + 4.2 完成。
> **A.2 显式约束 (proposal :171, 硬)**: `aria/skills/audit-engine/` 内**不得**新建名为 `lib/` 或 `collectors/` 的顶层目录; 探针 helper 一律放 `scripts/` 下并以 `sibling_spec_probe_` 为模块名前缀。由 2.1 的结构断言钉住。

---

## 1. 前置断言 + B.1 门

- [x] 1.1 前置断言: `aria/skills/state-scanner/lib/linked_issue_field.py` 已存在且导出 `extract_linked_issue_field(text: str) -> FieldVerdict` (四态 `NO_FIELD` / `NO_TOKEN` / `BAD_TOKEN` / `OK`; 字段 `verdict` / `token_str` / `token_elements` / `line_no`), 接口与姊妹 §3「交付形态」逐字核对; **不存在 ⇒ 阻塞 (status=blocked), 不得自建替身, 不得复制 E0–E6**
- [x] 1.2 基线三态记录: audit-engine 现状 (零 `scripts/` / 零 `tests/` / 零 `lib/` / 零 `collectors/`; SKILL.md `:83/:85/:237`、execution-modes.md `:84/:89/:90/:113/:118/:119`、report-format.md `:50-71`、DEFAULTS.json `:124-128` 锚点复核); `ab-suite/` `.json` 数当日实测记录 (A.2 观测 31, 不钉字面) 且无 `audit-engine.json`; SC-17 / SC-20 / SC-21 在基线上**必红**的亲跑记录 (memory `check-runs-at-baseline-first`)
- [x] 1.3 建 `aria-plugin-benchmarks/ab-suite/audit-engine.json` (**经 `/skill-creator` 产出**, 不手工仿写; 2 个 eval: α「每轮入口调用探针并把结果渲染进 `### Round N`」/ β「`not_established` / exit≠0 / 非 JSON ⇒ 渲染『未能核实』, 不得『无竞品』, 不阻断」= **SC-16**; 产出形态 `descriptive`) + `ab-suite/version.yaml` MINOR 升版 (skills_covered / total_eval_cases **按实际文件程序化重算**后写: `ls ab-suite/*.json | wc -l` + python 遍历各 json 求 `len(evals)` 之和; 断言 = 当前值 + 新增数, 不写字面量 — R1 C5, 见 yaml `metadata.ab_suite_seam_rules`)。**B.1 前置** (proposal :473); 建不成 ⇒ 不自判豁免, 原样上呈 owner (兜底「缺一照跑」在无套件时结构上不可执行, 即 `aria-plugin#150`)

## 2. TDD — 测试宿主 (RED first)

> 2.1 建文件; 2.2 → 2.3 → 2.4 → 2.5 → 2.6 **串行链** (同一新建文件, R1 C1); 每条另含硬前置边 ← 1.1。

- [x] 2.1 新建 `aria/skills/audit-engine/tests/test_sibling_spec_probe.py` 骨架: 模块级前置守卫 (姊妹模块缺席 ⇒ 整套 `skip` 并报「前置未 ship」, §1 第 3 条); 不 `import pytest` (走 `run_all_tests.sh:71` unittest 分支, 避免 `:62-66` SKIP 假绿); **SC-21** import 顺序断言 (`sys.modules["lib"].__file__` 落 `state-scanner/lib/__init__.py` 且 `collectors.multi_remote.resolve_enforced_remotes` 可导入) + **负控** (子进程内按反序插入 `_SS_SCRIPTS` 后于 `_SS_ROOT` ⇒ `import lib.collision` 抛 `ModuleNotFoundError`); **结构断言** (audit-engine 下无 `lib/` `collectors/` 顶层目录; `scripts/` 内除 `sibling_spec_probe.py` 外的 `.py` 一律 `sibling_spec_probe_` 前缀)
- [x] 2.2 谓词层测试 (纯函数, 不打网络): **SC-7** (`#122` 两行原文经层 2 得 `["k","aria-plugin",122]` 命中) / **SC-8** (`:6` 原文经姊妹判 `NO_TOKEN`, 不抽 `confirmed`) / **SC-9** (哨兵三组 `无,无` `none,none` `none,无` 不命中, layer `none_sentinel`) / **SC-10** (哨兵 + 行内 URL 两臂不回落) / **SC-11** (`none_sentinel` vs `no_field` 可辨) / **SC-19** (placeholder 黑名单不产原串键, `own_layer="bad_token_union"`); 键构造 `("k",basename,n)` / `("r",t)` 两类永不相等; `BAD_TOKEN` 反例 A/B 并集; 每条写「它怎么会红」+ 至少一个坏实现被拒
- [x] 2.3 层 0 假阳性拒绝 **SC-18** 四臂 (a 行首 / b 宽松 / c 行首+仅头部 / d 合成围栏夹具) 在主仓 `cc1bdef` 147 篇上同批跑 (跨仓读取 ⇒ 主仓或 `cc1bdef` 不可达时 **skip 并打印原因**, 不 fail; 第四臂为合成夹具, 永不 skip) + **SC-1** (竞品在 `archive/` ⇒ 命中且 `hits[].corpus=="archive"`)
- [x] 2.4 远端解析 / fetch / cap 测试 (注入式 git runner, 仿 `phase-d-closer/tests/test_fetch_gate.py:22` 的 `_runner(seq)` 体例): **SC-12** (无本地 symbolic-ref 仍经 `ls-remote --symref` 解出 `master`) / **SC-13** (非 0 / 超时 / 无 `ref: ` 行 / 前缀不符 ⇒ `default_branch=null` + `error_kind` 非空, stdout 不得出现字面 `master`/`main` 作该 remote 的 `default_branch`) / **SC-14** (`refs/remotes/probe/*` 存在而 `remote.probe.url` 空 ⇒ `remotes[]` 不含 `probe`) / **SC-3** (fetch 失败 ⇒ `degraded` + `not_established` + 另一 remote 命中仍在 `hits[]`) / **SC-4** (enforced 空集 ⇒ `skipped` + `no_enforced_remote`) / **SC-5** (自命中排除, 任一 remote / corpus) / **SC-6** (`MAX_PROPOSALS_SCANNED=1` 留 `changes/`, `caps_applied` 非空, stderr 披露); §5 超时预算断言 (runner 记录每次 `timeout==30`; fetch 首次失败 ⇒ 恰 2 次尝试, 首次成功 ⇒ 恰 1 次; `ls-remote` 恰 1 次); §6 排序决定性 (乱序输入 ⇒ `changes/` 先、各自字节序; 1001 条 ⇒ 保留 1000 且 `dropped_from` 为第 1001 条) / **SC-22~25** (P11 分支维, 2026-09-01 裁定; 注入 runner 夹具: B1 分支命中 / 跨 ref 去重 / 陈旧过滤 / refs cap)
- [x] 2.5 CLI 全链路契约测试 (`subprocess.run([sys.executable, script, ...])`, 仿 `state-scanner/tests/test_coordination_no_push.py:132`): **SC-15** (`ok` / `degraded` / `skipped` 三终局 stdout 各恰一个可 `json.loads` 对象, 含 §7 十二必填键, stderr 内容不在 stdout) / **SC-2** (无命中 ⇒ `status="ok"` `verdict="no_sibling_found"` `hits==[]` **exit 0**) / exit 三分 (`--own-spec-dir` 缺失 ⇒ 非 0; 命中 ⇒ 0); `reason` 非空规则 (`status!="ok"` **或** `verdict=="not_established"`); stderr 不回显 git 原始 stderr (夹具 stderr 内嵌 `https://user:tok@host`, 断言 stdout/stderr 均不含 `tok`)
- [x] 2.6 指令面结构断言 (RED): **SC-17** (execution-modes.md `## Convergence 模式` / `## Challenge 模式` 两节围栏块切片各恰 1 次 `每轮入口: 竞品 spec 探针`, 全文其余处 0 次; docstring 写明「第三个模式块出现时本条会把正确的三处判红, 有意保守」) / **SC-20** (i: SKILL.md 小节切片 (锚 `(?m)^#{2,4}[ \t]+per-round 入口探针` 至下一 `^#{1,4}[ \t]` 行) 含 `sibling_spec_probe.py` / `verdict` / `not_established` / `未能核实` 四字面 + 一条 `python3` 起首含 `sibling_spec_probe.py` 与 `--own-spec-dir` 的完整命令行; ii: execution-modes.md 含 `## 竞品 spec 探针 (per-round 入口)` 节, 切片含 `verdict` / `status` / `hits` + `未能核实` / `已完整扫描` / `检测到`) — 基线上两条必红 (1.2 亲跑)

## 3. 实现 — `aria/skills/audit-engine/scripts/sibling_spec_probe.py` (stdlib-only)

> 3.1 → 3.2 → 3.3 → 3.4 **串行链** (同一新建文件, R1 C1; 原 3.2 与 3.3 标「并行」已废); 3.5 收口, 边 ← 2.6 + 3.2 + 3.3 + 3.4。

- [x] 3.1 骨架 + I/O 边界: CLI `--own-spec-dir <name>` (必需) / `--repo-path <root>` (必需, 不假定 cwd); §3 跨 skill import **唯一代码块**逐字 (`_SS_SCRIPTS` 先插、`_SS_ROOT` 后插 ⇒ `_SS_ROOT` 在 `sys.path` 最前; 三条 import `normalize_linked_issue` / `extract_linked_issue_field` / `resolve_enforced_remotes` 只在此块); 绑定 `lib` 后不再 import `scripts/lib` 下任何模块; 本轨 proposal 从工作树 `<repo>/openspec/changes/<own-spec-dir>/proposal.md` 读 (缺失 ⇒ 参数错, 非 0); git 子进程 runner 可注入 (纯分类逻辑与 I/O 分离, 供 2.x 夹具); §7 stdout 恰一个 JSON (十二字段) + `verdict` 三值表 + exit 三分 + stderr `log()` + `error_kind` 稳定枚举 (形态照抄 `fetch_gate.py:86-101` `_classify_error`, 复制不 import; 加 `timeout` / `no_symref` / `bad_symref_prefix`); `elapsed_ms`
- [x] 3.2 谓词层: 姊妹四态 → 层分派表 (`NO_FIELD`→层 3 / `NO_TOKEN`→层 2 / `BAD_TOKEN`→层 1 ∪ 层 2 / `OK`+哨兵→层 1.5 ∅ 不回落 / `OK`→层 1); 哨兵判定吃姊妹 E3 **未 strip 的 token 串** (`无` 逐字节 或 ASCII 折叠 `none`); 层 2 只扫字段行 (由 `FieldVerdict.line_no` 定位) 抽 `/<org>/<repo>/issues/<n>` 片段; 键构造 `("k",k[0],k[1])` / `("r",t)`; **SC-19 常量黑名单** (SOT placeholder `{<org>/<repo>#<n>}` 逐字 + 哨兵集合; 与姊妹 §2/§3 同源, 模块顶部注释写明同步义务); 集合去重 + 求交; `own_spec_dir` 自命中排除 (任一 remote / corpus); `own_layer` / `hits[].layer` 六值枚举
- [x] 3.3 remote 与默认分支 (§4, fail-closed): `actual_remotes` 取 `git -C <repo> remote` (配置面, 禁 `refs/remotes/*` glob); `configured` / `read_only` 取 `.aria/config.json` `state_scanner.multi_remote.{enforced_remotes,read_only_remotes}` (skill 级 null ⇒ 继承顶层 `multi_remote.*`, 镜像 `multi_remote.py:_resolve_remote_policy` 契约); 经 `resolve_enforced_remotes()` 取 `enforced`; 空集 ⇒ `skipped` + `no_enforced_remote` + exit 0; 逐 remote `git -C <repo> ls-remote --symref R HEAD` 取第一条 `ref: ` 行按 `\t` 切、须 `refs/heads/` 前缀; 任一不成立 ⇒ `default_branch=null` + `error_kind` + `degraded` + `not_established`, **不猜** `master`/`main`, 不读本地 `refs/remotes/<R>/HEAD`; 每 git 子进程 `timeout=30`; fetch `git -C <repo> fetch --no-tags --prune R +refs/heads/*:refs/aria/sibling-probe/R/*` 最多 2 次; 不复用 `remote_refresh` 缓存 / 不动 `refs/remotes/*` / 不依赖 `FETCH_HEAD`; **P11 (2026-09-01 技术裁定: 扩, 决策单 §H3)**: refspec 取全部分支 (上文逐字), 一次 fetch 网络腿数不变; 默认分支解析结果用于标记私有命名空间内的默认 ref; 默认分支解析失败 ⇒ 该 remote 不 fetch、不枚举 (`refs_scanned = 0`, fail-closed 短路)
- [x] 3.4 语料枚举 + 规模上限 (§2 / §6): 在私有 ref 上 `git ls-tree -r --name-only` 过滤 `^openspec/(changes|archive)/[^/]+/proposal.md$` (单层目录, 含 `archive/`); 排序 = `changes/` 先、`archive/` 后, 各自按完整路径字节序 (`sorted(key=str.encode)`) 升序; `MAX_PROPOSALS_SCANNED = 1000` 模块常量 (不做 config key, 不复用 `handoff_multibranch.max_branches`); 超限从尾部截断 ⇒ stderr `log()` 披露截断点路径 + 丢弃条数、`caps_applied[]` 非空、`status="degraded"`、`verdict="not_established"`; blob 经 `git cat-file` / `git show <ref>:<path>` 读, **不读工作树**; 逐 blob 喂 3.2 分类器; **P11 分支维 (SC-22~25)**: `git for-each-ref refs/aria/sibling-probe/R/` 枚举全部私有 ref (默认 ref 先, 其余 refname 字节序), 每 ref 独立 ls-tree, `MAX_PROPOSALS_SCANNED` 按 remote 跨 ref 累计 (默认 ref 先计, 超限从枚举序尾部截断, 不是 per-ref); 非默认 ref 数 cap `MAX_REFS_SCANNED = 100` (模块常量, 同 no-silent-caps 三件套, `caps_applied[].kind='refs'`, 默认 ref 永不被 cap); 陈旧过滤先于去重 (非默认 ref 的 `changes/<spec_dir>` 若同 remote 默认 ref 上有 `openspec/archive/<YYYY-MM-DD>-<spec_dir>/proposal.md` — 日期前缀恰 10 字符, `<spec_dir>` 逐字节, **不做后缀匹配** — ⇒ 跳过, 计 `remotes[].stale_skipped`); hits 按 (remote, corpus, spec_dir, key) 跨 ref 去重 (不跨 remote, 粒度同 a2 (e)) 并带 `refs[]` (整串字节序), branch/标量取枚举序首个命中 ref; SC-5 自命中排除对全部 ref 生效
- [x] 3.5 GREEN + 回归: 2.1–2.5 全绿 (2.6 留红待 4.x); `bash aria/skills/run_all_tests.sh` 自动发现 `audit-engine` 目录并计入; 四个坏实现负控各亲跑一次确认对应 SC 变红后还原 (只扫 `changes/` ⇒ SC-1 红; 只枚举默认 ref ⇒ SC-22 红; 回落条件写成「集合为空」⇒ SC-10 红; `_SS_SCRIPTS` 插在 `_SS_ROOT` 之后 ⇒ SC-21 红); `git -C aria diff --stat -- skills/state-scanner` 为空 (Impact 表「不改 state-scanner」)

## 4. audit-engine 指令面接线

- [x] 4.1 `aria/skills/audit-engine/references/execution-modes.md`: Convergence 块 (`:84`, 围栏内 `Round N:` `:89` 之后、`1. 调用 agent-team-audit 单轮引擎` `:90` 之前) 与 Challenge 块 (`:113`, `Round N (一个完整周期):` `:118` 之后、`Step 1: 讨论组 spawn` `:119` 之前) 各插入 §8 **逐字相同的两行插入串** (首行前缀 `每轮入口: 竞品 spec 探针 —— python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" --own-spec-dir ... --repo-path ...`; 次行三档 verdict 消费), 现有编号 `1.-4.` / `Step 1-5` 不动; 文末**新增节** `## 竞品 spec 探针 (per-round 入口)` 承载 §7 十二字段 stdout 契约 + exit 三分 + §9 三档消费措辞的权威可执行版, 该节**不得**含前缀字面 `每轮入口: 竞品 spec 探针` (SC-17 负控)
- [x] 4.2 `aria/skills/audit-engine/SKILL.md`: 在 `## 执行流程` 内 `### Step 0: Anchor 固化` (`:83`) 段之后、`## 数据 Schema` (`:121`) 之前新增小节, 标题**起首**为 `per-round 入口探针` (不带 `Step 0.5:` 等前缀); 概述 + 指针 (`权威可执行版见 references/execution-modes.md`, 与 `:237` 体例一致); 小节内含四字面量 + 完整命令行 (SC-20 i); 与 Step 0「Round 1 启动前一次性」显式消歧 (本探针每轮跑, 不沿用 Step 编号); 点名行为 α/β; 更新 `## 相关文档` (`:412`) 指针与 `最后更新` (`:421`)。`references/report-format.md` `### Round N` 模板 (`:50-71`) 增一行探针结果, 措辞按 `verdict` 三档 (§9; `archive/` 命中标「已完成的 Spec」; N = 去重后的 `spec_dir` 数)。4.1 + 4.2 落地后 2.6 转绿

## 5. Rule #6 照跑 + 发布同步

- [x] 5.1 `/skill-creator benchmark audit-engine` 双臂实跑 (with_skill = 4.x 后的 SKILL.md; without_skill = 基线) —— α/β 两 eval 在 without 臂**必红**、with 臂过 (= 「两 eval 在坏实现上必红」的实证); 结果落 `aria-plugin-benchmarks/ab-results/` 按手册体例; 会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动 (手册 §场景 1 前置; audit-engine 不触 phase1_gate, 但 eval AI 若实跑探针会 fetch 私有 ref, 无害); 跑不成 / delta 非正 ⇒ 不自判, 上呈 owner (Rule #10)
- [x] 5.2 发布同步面 (R1 C2 统一清单, 与字段 Spec TASK-024 / 上次发布 commit `086ee32` 同口径): **aria 子模块 5 文件** `aria/.claude-plugin/plugin.json` (版本 SOT) / `aria/.claude-plugin/marketplace.json` / `aria/VERSION` / `aria/CHANGELOG.md` / `aria/README.md`; **主仓** gitlink `aria` (bump 到子模块 post-merge master SHA) / `VERSION` / `README.md` badge / `CLAUDE.md` 项目状态版本行 / `README.zh.md` `README.ja.md` `README.ko.md` 顶部 `<!-- translated-from: v<vNEXT> -->` 标记 + 各自 badge 与 `Plugin Version:` 串 (B 档: 正文无实质变更不重译, **但标记必改** —— check `i18n-readme-translation-currency` 读的是标记); 机械兜底 `m6-version-badge-match` / `i18n-readme-translation-currency` 在完成上述**全部**文件后才断言绿。**版本字面一律写 `<vNEXT>` 占位** (R1 C3): 档位 (MINOR/PATCH) 与号由 owner 裁; 三份串行 ship 各占一号 (字段 → 探针 → 母); 若 owner 裁合并一版, 由最后 ship 的母 Spec 发布任务承接, 前两份的发布任务改为 no-op 并留痕。未裁 ⇒ 本任务不开工 (status 仍 `pending`, 不用 `blocked`)。多远程双推 + 逐 remote `ls-remote` 核验按 CLAUDE.md 硬约束 1/2 (子模块合并本地做)

---

## SC → TASK 覆盖表 (25/25)

| SC | 类 | 测试 (RED) | 实现 / 落地 (GREEN) | 备注 |
|----|----|-----------|---------------------|------|
| SC-1 | 代码 | TASK-006 (2.3) | TASK-011 (3.2), TASK-013 (3.4), TASK-016 (4.2 措辞「已完成的 Spec」) | 只扫 `changes/` 的实现必红 |
| SC-2 | 代码 | TASK-008 (2.5) | TASK-010 (3.1) | 无命中 ⇒ exit 0 |
| SC-3 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) | fetch 失败 ⇒ degraded + exit 0, hits 保留 |
| SC-4 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) | enforced 空集 ⇒ skipped + exit 0 |
| SC-5 | 代码 | TASK-007 (2.4) | TASK-011 (3.2) | 自命中排除 |
| SC-6 | 代码 | TASK-007 (2.4) | TASK-013 (3.4) | cap 三件套 + `changes/` 优先 |
| SC-7 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | 立项案例 `#122` 层 2 命中 |
| SC-8 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | 经姊妹 E2 判 `NO_TOKEN` (本 Spec 只 import) |
| SC-9 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | 哨兵三组不命中 |
| SC-10 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | 回落触发 = verdict ∈ {NO_TOKEN, BAD_TOKEN}, 非「集合为空」 |
| SC-11 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | `none_sentinel` vs `no_field` 可辨 |
| SC-12 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) | 无本地 symbolic-ref 仍解出 |
| SC-13 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) | fail-closed, 不猜 master/main |
| SC-14 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) | `probe` 陈旧 ref 不入 `remotes[]` |
| SC-15 | 代码 | TASK-008 (2.5) | TASK-010 (3.1) | 三终局 stdout 恰一 JSON |
| SC-16 | **行为** | TASK-003 (1.3, eval β) | TASK-016 (4.2 措辞), TASK-017 (5.1 双臂实跑) | 无代码宿主, 只由 AB 定向 fixture 覆盖 |
| SC-17 | 代码 | TASK-009 (2.6) | TASK-015 (4.1) | 分块计数恰 2 + 负控 0 |
| SC-18 | 代码 | TASK-006 (2.3) | TASK-011 (3.2) (层 0 经姊妹函数) | 跨仓读 `cc1bdef` 语料 ⇒ 不可达时 skip (已知限, 见「需 owner 裁 / 已知限」#4) |
| SC-19 | 代码 | TASK-005 (2.2) | TASK-011 (3.2) | 常量黑名单, 与姊妹同源 |
| SC-20 | 代码 | TASK-009 (2.6) | TASK-015 (4.1, ii), TASK-016 (4.2, i) | D17 ①②③ |
| SC-21 | 代码 | TASK-004 (2.1) | TASK-010 (3.1) | import 顺序 + 负控 |
| SC-22 | 代码 | TASK-007 (2.4) | TASK-012 (3.3) / TASK-013 (3.4) | P11 B1 补盲: 非默认分支同键竞品命中 (2026-09-01 裁定) |
| SC-23 | 代码 | TASK-007 (2.4) | TASK-013 (3.4) | P11 跨 ref 去重, hits[].refs |
| SC-24 | 代码 | TASK-007 (2.4) | TASK-013 (3.4) | P11 陈旧过滤 (默认 ref 已归档 ⇒ 分支副本跳过), remotes[].stale_skipped |
| SC-25 | 代码 | TASK-007 (2.4) | TASK-013 (3.4) | P11 MAX_REFS_SCANNED no-silent-caps (kind='refs') |

未覆盖: **无**。

## Impact 表 → TASK 对账

| Impact 行 | TASK |
|-----------|------|
| `skills/audit-engine/scripts/sibling_spec_probe.py` (新建, 含 `scripts/`) | TASK-010 ~ TASK-014 |
| `skills/audit-engine/tests/test_sibling_spec_probe.py` (新建, 含 `tests/`) | TASK-004 ~ TASK-009 |
| `skills/audit-engine/SKILL.md` | TASK-016 |
| `skills/audit-engine/references/execution-modes.md` | TASK-015 |
| `skills/audit-engine/references/report-format.md` | TASK-016 |
| `aria-plugin-benchmarks/ab-suite/audit-engine.json` (新建) | TASK-003, TASK-017 |
| `aria-plugin-benchmarks/ab-suite/version.yaml` (Impact 表未列, A.2 补; 计数程序化重算, R1 C5) | TASK-003, TASK-017 (仅拆条时) |
| 发布同步面 (Impact 表无版本行, A.2 补; R1 C2 清单 = aria 5 文件 + 主仓 gitlink / VERSION / README.md / CLAUDE.md / i18n ×3) | TASK-018 |
| 不改 `skills/state-scanner/**` | TASK-014 (`git diff --stat` 为空断言) |
| CLI `--own-spec-dir` / `--repo-path`; exit 0 / 非 0; stdout 十二键 + `reason` 五值 + `verdict` 三值 + `own_layer` 六值 | TASK-008, TASK-010 |
| issue `aria-plugin#150` (套件缺口, 已存在不新开) / `#157` (同族先例) | TASK-003 verification 引其号 |

---

## 待 owner 裁 / 已知限 (A.2 不自行拍板, Rule #10 + memory `narrow-owner-options`)

> **2026-09-01 分工裁定** (owner: 产品级 owner / 技术级 AI): #1 (P11) = 扩、#5 (版本档) = MINOR 各占一号 — 已裁, 见决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md`; #2/#3/#4 属技术级, 由 AI 在 B 期落点裁定并追记该决策单, 不再等 owner。

1. ~~**P11 扫描范围复议**~~ **✅ 已裁 (2026-09-01, 扩)**: 本清单原按「只扫 enforced_remotes × 各自默认分支」派生; 裁定后落点 = 3.3 (refspec `+refs/heads/*:refs/aria/sibling-probe/R/*`) + 3.4 (分支维枚举 / 陈旧过滤 / 去重 / `MAX_REFS_SCANNED`) + 2.4 (SC-22~25 RED) + proposal P11 行 / §7 / §10 B1 / SC 表; 任务集与依赖零改动 (扩展刻意落在既有任务的 verification 内, 回退 = 一句话, 见决策单 §回退指引)。判据: 产品目标 #174 倒推 (in-flight 竞品活在非默认分支) + 成本前提已被 proposal :443-452 实测推翻。
2. **AB 套件的时点拆分** (proposal :473 vs 手册 §场景 2): :473 要求「建成 `audit-engine.json` 且两 eval 在坏实现上必红」为 **B.1 前置**; 但「坏实现上必红」只能由双臂实跑证实, 而 with_skill 臂 = 4.x 产物 (B.2 内)。A.2 处置 = 拆为 1.3 (文件建成, B.1 前, 验收 `test -f` + JSON 结构 + expectations 字面) 与 5.1 (双臂实跑, B.2 末)。**请 owner 确认该拆分满足 :473 的意图**; 若 owner 要求 B.1 前即实跑, 需 with 臂用草稿 SKILL.md, 属另一形态。
3. **`ab-suite/version.yaml` 与 `AB_TEST_OPERATIONS.md` 盘点口径**: Impact 表未列 `version.yaml`, 但手册「修改任何 eval case → 升 MINOR」适用于新增套件 (`.json` 数 = 当前值 + 1; `version.yaml` 自称的 skills_covered / total_eval_cases 与实测文件数 / evals 总和已漂, A1 6698004d 实测 — 故 1.3 改为程序化重算, 不写字面, R1 C5)。A.2 把 `version.yaml` 补进 1.3 deliverables。手册 `:76` 「28 个 ✅ 全量覆盖」/ `:519` 「28 skills, 56 cases」与实测 31 / `#150` 的 14/43 三方互不一致 —— proposal follow-up #2 已记, **本 Spec 不修**, 建议并入 `#150`。
4. **SC-18 跨仓已知限**: 三臂语料 = 主仓 `cc1bdef` 147 篇, 而测试宿主在 `aria/` 子模块内; plugin 单独分发时主仓不存在 ⇒ 该条须 skip 并打印原因 (零证据不当负证据, 与姊妹 SC-6 同款处置)。第四臂 (合成围栏夹具) 不受此限。**Spec 未成文此已知限**, 请 owner 认可或改为把 147 篇快照打包成夹具 (体积 ~数 MB, 不建议)。
5. ~~**版本号档位与号 (R1 C3 三份统一句)**~~ **✅ 已裁 (2026-09-01, 决策单 §H1)**: 档位 = **MINOR** (SOT `version-management.md §2.2`「功能增强 (向下兼容)」字面覆盖本 Spec 的新运行时指令面 + 新脚本 + 新 AB 套件; CLAUDE.md 那两句是缩写); 三份串行 ship 各占一号 (字段 → 探针 → 母), 不合并一版; 号落地时按当时 plugin.json 计算, 版本字面仍 `<vNEXT>` 占位。5.2 可按依赖开工。Impact 表无版本行 (姊妹 Spec 有), 本清单补 5.2。
6. **A.2 裁量 (已定, 请 post_planning 复核, 非 owner 项)** —— 详见 detailed-tasks.yaml `metadata.a2_discretions`: (a) 本轨 proposal 读工作树路径, 缺失 ⇒ 参数错非 0; (b) `error_kind` 在 `_classify_error` 五值外加 `timeout` / `no_symref` / `bad_symref_prefix`; (c) `ls-remote` 腿不重试 (Spec 只给 fetch 腿 2 次); (d) config 读取镜像 `_resolve_remote_policy` 的 skill 级→顶层继承 (Spec 只点名 skill 级键); (e) 消费面「N 份」= 去重后的 `spec_dir` 数 (同一 Spec 在 origin/github 两镜像各成一条 `hits[]` 项, 按 remote 分列是设计如此, 计数须去重); (f) 语料 blob 读取用 `git cat-file --batch` 或逐文件 `git show`, 实现者择一, 均不读工作树。
7. **follow-up (不在本 Spec, 承 proposal §Impact follow-up)**: `fetch_gate.py:21/:111` 悬空引用 `sync.py::_resolve_default_branch`; 手册盘点三方不一致 (并入 `#150`)。

---

## Notes

- **不在本 Spec**: 母 Spec 的 A.1 认领 / track-id / `--linked-issue` 实参 (姊妹 E6 / `--emit-arg`); 本探针**永不**产生 `--linked-issue` 实参 (§3 层 2 作用域分离)。
- **语料数漂移**: proposal 写 147 (主仓 `cc1bdef`), A.2 实测 HEAD `c120f9e` 为 149 (changes 9 + archive 140); SC-18 钉 `cc1bdef` 树 (`git cat-file -t cc1bdef` = commit, 可达), 不钉工作树。
- **Phase A.3**: 无新 Agent; roster = tech-lead (跨 Spec 接缝断言) / qa-engineer (测试 + AB) / backend-architect (探针实现) / knowledge-manager (指令面文档 + 发布同步)。

---

## R1 清账对账 (2026-08-30)

> 依据: post_planning R1 五席报告 `.aria/audit-reports/post_planning-R1-1788102593777-a1-entry-combined-A{1..5}-*.md` 中 scope 含本 Spec 的 finding + 主控三份统一裁量 (C1/C2/C3/C5/C8/C9 + Minors)。修法 = 定点编辑, 不重写、不改编号、不改 proposal。「闭合」= 该 finding 的处方已落到本 Spec 两份文件; 宿主在字段/母 Spec 或 proposal 的统一项 (C4 / C6 / C7 / C10 / C11) 不在本表。

| finding id | 席 · 严重度 | 处置 | 改动落点 |
|-----------|------------|------|----------|
| a257ffa4 (A2) | A2 · critical | **closed** — 共写 `tests/test_sibling_spec_probe.py` 的 2.2~2.6 改链式串行 (不合并任务) | yaml TASK-005~009 `dependencies` (各 ← 前一任务 + TASK-001); `execution_order` 第 3 行「[并行, RED]」→「[串行 (同文件)]」; tasks.md 排序依据 / 组 2 头注 |
| C1 rule 1 同文件 (A2 处方延伸, 主控统一) | 主控 | **closed** — 3.2 与 3.3 共写 `scripts/sibling_spec_probe.py`, 原「[并行]」改串行; 3.5 也写测试文件 ⇒ 加 ← 2.6 | yaml TASK-012 deps 加 TASK-011; TASK-014 deps 加 TASK-009; `execution_order` 第 5/7 行; tasks.md 组 3 头注 |
| 98e71a6a (A3) | A3 · major | **closed (按主控裁量)** — TASK-003 (B.1 前置) 落边到第 4 组接线 + 第 5 组 AB; `phase_b1_preconditions` 每条改为指向真实上游边。A3 原处方是落到 TASK-004 (第 2 组起点), 差异见汇报「冲突」项 | yaml TASK-015 / TASK-016 deps 加 TASK-003 (TASK-017 原有); `metadata.phase_b1_preconditions`; tasks.md 组间门 |
| C1 rule 3 TASK-001 前置边 (主控统一; 同构于 A3 3221f943 对母 Spec 的处方) | 主控 | **closed** — 第 2 组 RED 全部加 TASK-001 边 (TASK-004 原有) | yaml TASK-005~009 deps; tasks.md 组间门 |
| a257ffa4 (A1) | A1 · critical | **closed** — TASK-018 发布同步面补齐主仓 `VERSION` / `README.md` / i18n ×3 / gitlink `aria`, 「不重译」改为「正文不重译, 标记与两处版本串必改」, 两条 check 改为「全部文件完成后才断言绿」 | yaml TASK-018 deliverables (12 项, 与字段 TASK-024 14 点 (R2 后口径, 含 CLAUDE.md :139/:141) + `086ee32` 7 文件对齐) + verification 4 条 + notes; tasks.md 5.2 / Impact 对账表 |
| 3221f943 (A1) / C3 | A1 · major (母/字段为主, 三份统一句) | **closed** — 版本字面 `<vNEXT>` 占位; 统一句 (档位与号 owner 裁 / 串行各占一号 / 合并一版由母承接、前两份 no-op 留痕 / 未裁不开工 pending) | yaml TASK-018 verification[0]; tasks.md 5.2 / 待 owner #5 |
| af9f0c47 (A5) | A5 · minor | **closed** — 「未裁 ⇒ blocked」改「未裁 ⇒ 不开工 (status 仍 `pending`)」, 与三份统一 | 同上 (C3 落点) |
| 6698004d (A1) / C5 | A1 · major | **closed** — `version.yaml` 计数改程序化重算 (`ls *.json \| wc -l` + python 求 `len(evals)` 和), 删 29→30 / 58→60 / == 32 字面; TASK-017 拆条时同批改 version.yaml; seam rule 入 metadata; TASK-002 基线「== 31」改「当日实测值 (A.2 观测 31)」 | yaml TASK-003 deliverables 注释 + verification; TASK-017 deliverables; TASK-002 verification; `metadata.ab_suite_seam_rules[0]`; tasks.md 1.3 / 待 owner #3 / Impact 对账表 |
| 35dad35d (A1) / C5 | A1 · major (字段/母为主) | **closed (本 Spec 侧 = 接缝知会)** — eval id 分配约定 (max(id)+1, ship 时读取; 字段先取 3、母顺延) 三份同写; 本 Spec 只新建 `audit-engine.json` (id 从 1 起), 不写 `spec-drafter.json` | yaml `metadata.ab_suite_seam_rules[1]` |
| f3265bfe (A2) / C8 | A2 · major | **closed** — 删「proposal 实况全部复现」; 该条改为带时戳 + 仓路径的观测 (非断言, 不作 SC 前提), 并写入清账席 2026-08-30T15:40Z 于主仓 `/home/dev/Aria` 亲跑结果 (`git remote` / `for-each-ref refs/remotes/probe` / `for-each-ref refs/aria/` = 3 条 / `ls-remote --symref` ×2 / `symbolic-ref`); 注明 A2 复测用 `git -C aria` (子模块) 故零命中, 两者仓不同。TASK-012 notes「本仓实况」→「环境观测 (非设计前提)」; TASK-007 SC-12 「(本仓实况)」→「(夹具值, 取自观测)」 | yaml `metadata.line_anchor_recheck` 末条; TASK-012 notes; TASK-007 verification[0] |
| df090b25 (A4) / C9 | A4 · major | **closed** — 18 处 `est_hours: <int>` → `estimated_hours: "a-b"` (S "1-2" / M "3-5" / L "6-8", DUAL_LAYER_SPEC :166 + 母 Spec 一致); metadata 加 `estimated_hours: "55-87"`; `complexity_summary` 改区间; `estimation_note` 改 SOT 区间 | yaml 全部 18 task + metadata + complexity_summary |
| 1246445b (A1) / 948363d3 (A4) / 4f76bc57 (A5) | 三席 · minor / decision | **closed** — 三席独立均判 `is_sentinel` 追加不违反 §3 位置唯一约束; TASK-010「恰三条 / 三符号」改『包含』口径 (三条逐字存在 + 同块允许第四符号 + 块外零 `from lib.` / `from collectors.`; `sys.path.insert` 恰 1 处); a2_discretions (i) 追记复核结论 | yaml TASK-010 verification[1]; `metadata.a2_discretions (i)` |
| 4bf32c17 (A4) | A4 · minor | **closed (方案未明列, 按 C10 同形顺手, 可撤)** — 覆盖表 (SC-18, TASK-006) / (SC-16, TASK-016) 两对在 verification 补 SC token | yaml TASK-006 verification[1] 前缀 `SC-18`; TASK-016 verification[2] 「(β = SC-16 …)」 |
| af9f0c47 (A1, token_elements) | A1 · minor | **closed (方案未明列, 顺手, 可撤)** — `interface_expected.token_elements` 去掉「BAD_TOKEN 时须能点名坏元素」这一姊妹未承诺的义务, 改为「全部元素; 点名由姊妹 additive `bad_elements` 承担, 本探针不消费, 层 1 原串键自行逐元素归一得出」 | yaml `metadata.external_dependencies[0].interface_expected.token_elements` |
| c23f47ce (A1) / 96ecdeb4 (A1) / 05b5c605 (A1) / fead49d5 (A4) / 8b2910e2 (A5) | — | **不落本 Spec** (C4 / C7 宿主 = 字段 yaml; C6 / C10 宿主 = 母 yaml/tasks.md; C11 = proposal 尾句, 主控已改 :578) | — |

**主控追记 (2026-08-30, 清账席上报的两条冲突裁定)**: (1) proposal `:473` 字面「Phase B.1 不得开始」⇒ TASK-003 追加为 TASK-004 (第 2 组起点) 的依赖, 原落在 015/016/017 的边保留; (2) TASK-002 断言「无 `audit-engine.json`」与 TASK-003 建该文件存在隐性时序, 追加 TASK-003 ← TASK-002 边。均为一行 `dependencies` 改动, 已重跑 parse + 无环核验。

## 机械核验 (R1 C1 第 4 条; 2026-08-30 清账后亲跑)

不变量: (a) 任意两任务 deliverables 交集非空 ⇒ 后者依赖前者 (直接或传递); (b) 无环; (c) RED (G2) 不依赖 GREEN (G3/G4); (d) TASK-001 ∈ deps(TASK-004~009), TASK-003 ∈ deps(TASK-015/016/017); (e) `execution_order` 标「并行」的行内任务两两无同文件。附: PyYAML 解析 / `state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks` / parent 1:1 (yaml `parent` 序列 == 本文件 checkbox 序列) / `estimated_hours` 形态。

```python
#!/usr/bin/env python3
"""R1 C1 机械核验 — sibling-spec-probe/detailed-tasks.yaml 依赖不变量 (a)-(e)."""
import re, sys, pathlib, yaml

ROOT = pathlib.Path("/home/dev/Aria")
Y = ROOT / "openspec/changes/sibling-spec-probe/detailed-tasks.yaml"
MD = ROOT / "openspec/changes/sibling-spec-probe/tasks.md"
doc = yaml.safe_load(Y.read_text(encoding="utf-8"))
tasks = doc["tasks"]
ids = [t["id"] for t in tasks]
by = {t["id"]: t for t in tasks}
deps = {t["id"]: list(t.get("dependencies") or []) for t in tasks}
deliv = {t["id"]: {str(d).split("#")[0].strip() for d in (t.get("deliverables") or [])} for t in tasks}
fails = []

def reach(a):  # transitive deps of a
    seen, st = set(), list(deps[a])
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); st.extend(deps.get(x, []))
    return seen

# (a)
shared = []
for i, a in enumerate(ids):
    for b in ids[i+1:]:
        inter = deliv[a] & deliv[b]
        if inter:
            ok = a in reach(b)
            shared.append((a, b, sorted(inter), ok))
            if not ok: fails.append(f"(a) {b} shares {sorted(inter)} with {a} but does not depend on it")
print(f"(a) same-file pairs = {len(shared)}; all with edge = {all(s[3] for s in shared)}")
for a, b, inter, ok in shared:
    print(f"    {a} -> {b}  {'OK ' if ok else 'MISSING'}  {inter}")

# (b)
WHITE, GREY, BLACK = 0, 1, 2
color = {i: WHITE for i in ids}
cyc = []
def dfs(u, path):
    color[u] = GREY
    for v in deps[u]:
        if v not in color: fails.append(f"(b) dangling dep {u} -> {v}"); continue
        if color[v] == GREY: cyc.append(path + [v])
        elif color[v] == WHITE: dfs(v, path + [v])
    color[u] = BLACK
for i in ids:
    if color[i] == WHITE: dfs(i, [i])
print(f"(b) cycles = {cyc}")
if cyc: fails.append(f"(b) cycles {cyc}")

# (c)
red = [i for i in ids if by[i]["task_group"] == "G2"]
green = {i for i in ids if by[i]["task_group"] in ("G3", "G4")}
bad = {r: sorted(reach(r) & green) for r in red if reach(r) & green}
print(f"(c) RED={red}; RED depending on GREEN = {bad or 'none'}")
if bad: fails.append(f"(c) {bad}")

# (d)
need = {"TASK-001": ["TASK-004","TASK-005","TASK-006","TASK-007","TASK-008","TASK-009"],
        "TASK-003": ["TASK-015","TASK-016","TASK-017"]}
for up, downs in need.items():
    miss = [d for d in downs if up not in deps[d]]
    print(f"(d) {up} direct in deps of {downs}: {'OK' if not miss else 'MISSING '+str(miss)}")
    if miss: fails.append(f"(d) {up} missing in {miss}")

# (e) execution_order 展示 vs dependencies (R3 扩维: A1 f137dded / A3 d935b128 — 箭头右侧 ⊆ deps[head]; 「并行」声明的任务间不得有依赖)
def ids_in(seg):
    return [f"TASK-{m.group(1)}" for m in re.finditer(r"(?:TASK-)?\b(\d{3})\b", re.sub(r"\([^)]*\)", "", seg))]
for line in doc["execution_order"]:
    stripped = re.sub(r"\([^)]*\)", "", line)
    for seg in stripped.split("→"):
        if "←" not in seg: continue
        left, right = seg.split("←", 1)
        hs = re.findall(r"TASK-\d{3}", left)
        if not hs: continue
        h = hs[-1]; rights = ids_in(right); missing = [r for r in rights if r not in deps.get(h, [])]
        print(f"(e) {h} ← {rights}: {'OK' if not missing else 'NOT IN deps ' + str(missing)}")
        if missing: fails.append(f"(e) {h} arrow {missing} not in dependencies")
    if "并行" in stripped:
        tsp = ids_in(stripped.split("并行")[0]) or ids_in(stripped)
        contra = [(a, b) for i, a in enumerate(tsp) for b in tsp[i+1:] if a in deps.get(b, []) or b in deps.get(a, [])]
        pairs = [(a, b) for i, a in enumerate(tsp) for b in tsp[i+1:] if deliv.get(a, set()) & deliv.get(b, set())]
        print(f"(e) parallel claim {tsp}: dep-contradiction = {contra or 'none'}; same-file pairs = {pairs or 'none'}")
        if contra: fails.append(f"(e) parallel claim contradicts deps {contra}")
        if pairs: fails.append(f"(e) {pairs}")

# extras
sys.path.insert(0, str(ROOT / "aria/skills/state-scanner/scripts"))
from lib.detailed_tasks import parse_detailed_tasks
r = parse_detailed_tasks(Y.read_text(encoding="utf-8"))
print(f"parse_detailed_tasks: parse_ok={r['parse_ok']} n={len(r['tasks'])} reason={r['reason']!r}; statuses={sorted({t['raw_status'] for t in r['tasks']})}")
if not r["parse_ok"] or len(r["tasks"]) != len(tasks): fails.append("parse_detailed_tasks mismatch")
md_ids = re.findall(r"^- \[[ x]\] (\d+\.\d+) ", MD.read_text(encoding="utf-8"), re.M)
parents = [t["parent"] for t in tasks]
print(f"parent 1:1: yaml parents == tasks.md checkboxes -> {parents == md_ids} ({len(parents)} vs {len(md_ids)}); dup ids={[i for i in ids if ids.count(i)>1]}; total_tasks meta={doc['metadata']['total_tasks']}")
if parents != md_ids: fails.append(f"parent mismatch {parents} vs {md_ids}")
hrs = [t.get("estimated_hours") for t in tasks]
HRS_RE = re.compile(r"\d+-\d+")
hrs_ok = all(isinstance(h, str) and HRS_RE.fullmatch(h) for h in hrs)
leftover = any("est_hours" in t for t in tasks)
print(f"estimated_hours present on all = {hrs_ok}; est_hours leftover = {leftover}")
print("RESULT:", "PASS" if not fails else "FAIL " + "; ".join(fails))
sys.exit(0 if not fails else 1)
```

**输出 (清账后, 2026-08-30)** — R2 后重跑 (2026-08-30, 转义修正 + 主控追记两条边后), 逐字:

```
(a) same-file pairs = 34; all with edge = True
    TASK-002 -> TASK-015  OK   ['aria/skills/audit-engine/references/execution-modes.md']
    TASK-002 -> TASK-016  OK   ['aria/skills/audit-engine/SKILL.md', 'aria/skills/audit-engine/references/report-format.md']
    TASK-003 -> TASK-017  OK   ['aria-plugin-benchmarks/ab-suite/audit-engine.json', 'aria-plugin-benchmarks/ab-suite/version.yaml']
    TASK-004 -> TASK-005  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-004 -> TASK-006  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-004 -> TASK-007  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-004 -> TASK-008  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-004 -> TASK-009  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-004 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-005 -> TASK-006  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-005 -> TASK-007  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-005 -> TASK-008  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-005 -> TASK-009  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-005 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-006 -> TASK-007  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-006 -> TASK-008  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-006 -> TASK-009  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-006 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-007 -> TASK-008  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-007 -> TASK-009  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-007 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-008 -> TASK-009  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-008 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-009 -> TASK-014  OK   ['aria/skills/audit-engine/tests/test_sibling_spec_probe.py']
    TASK-010 -> TASK-011  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-010 -> TASK-012  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-010 -> TASK-013  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-010 -> TASK-014  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-011 -> TASK-012  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-011 -> TASK-013  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-011 -> TASK-014  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-012 -> TASK-013  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-012 -> TASK-014  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
    TASK-013 -> TASK-014  OK   ['aria/skills/audit-engine/scripts/sibling_spec_probe.py']
(b) cycles = []
(c) RED=['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']; RED depending on GREEN = none
(d) TASK-001 direct in deps of ['TASK-004', 'TASK-005', 'TASK-006', 'TASK-007', 'TASK-008', 'TASK-009']: OK
(d) TASK-003 direct in deps of ['TASK-015', 'TASK-016', 'TASK-017']: OK
(e) TASK-003 ← ['TASK-002']: OK
(e) parallel claim ['TASK-001', 'TASK-002']: dep-contradiction = none; same-file pairs = none
(e) TASK-004 ← ['TASK-001', 'TASK-002', 'TASK-003']: OK
(e) TASK-005 ← ['TASK-001', 'TASK-004']: OK
(e) TASK-006 ← ['TASK-001', 'TASK-005']: OK
(e) TASK-007 ← ['TASK-001', 'TASK-006']: OK
(e) TASK-008 ← ['TASK-001', 'TASK-007']: OK
(e) TASK-009 ← ['TASK-001', 'TASK-008']: OK
(e) TASK-010 ← ['TASK-004', 'TASK-008']: OK
(e) TASK-011 ← ['TASK-010', 'TASK-005', 'TASK-006']: OK
(e) TASK-012 ← ['TASK-011', 'TASK-010', 'TASK-007']: OK
(e) TASK-013 ← ['TASK-012', 'TASK-007']: OK
(e) TASK-014 ← ['TASK-009', 'TASK-011', 'TASK-012', 'TASK-013']: OK
(e) TASK-015 ← ['TASK-003', 'TASK-009']: OK
(e) TASK-016 ← ['TASK-003', 'TASK-009', 'TASK-015']: OK
(e) TASK-017 ← ['TASK-003', 'TASK-014', 'TASK-015', 'TASK-016']: OK
(e) TASK-018 ← ['TASK-017']: OK
parse_detailed_tasks: parse_ok=True n=18 reason='18 task(s) parsed'; statuses=['pending']
parent 1:1: yaml parents == tasks.md checkboxes -> True (18 vs 18); dup ids=[]; total_tasks meta=18
estimated_hours present on all = True; est_hours leftover = False
RESULT: PASS
```

**拒绝能力 (memory `check-runs-at-baseline-first` / `adversarial-fixture`)**: 同一脚本对「清账前依赖图」(程序化还原: TASK-005~009 deps=[TASK-004], TASK-012=[010,007], TASK-014=[011,012,013], TASK-015=[009], TASK-016=[009,015], `execution_order` 两处「并行」行) 跑 ⇒ `RESULT: FAIL`: (a) 13 对同文件缺边 (005→006/007/008/009, 006→007/008/009, 007→008/009, 008→009, 009→014, 011→012/013); (d) TASK-001 缺于 005~009、TASK-003 缺于 015/016; (e) 「[并行, RED]」行 10 对同文件 + 「[并行] TASK-011 · TASK-012」1 对。(b)(c) 在旧图上本就为真 (旧图无环、RED 未反向依赖 GREEN)。 **注 (R4)**: 本段贴文为 R1 时点旧 (e) 的输出; R3 起 (e) 扩维 (箭头 ⊆ deps + 并行声明无依赖矛盾), 对同一配方会多出 (e) 项; 新 (e) 的拒绝能力由 R4/A3·A4 各用两组对抗输入实测 (见其报告), 本段不重贴。

**已知限 (诚实声明)**: (a) 按 deliverables **路径逐字相等**判同文件; TASK-002 的观测目标 `aria-plugin-benchmarks/ab-suite/` (目录) 与 TASK-003 新建的 `ab-suite/audit-engine.json` 路径不等 ⇒ 不触发, 但 TASK-002 verification 断言「无 `audit-engine.json`」在 TASK-003 先跑时会红 —— 第 1 组「并行」在此语义上有时序依赖, 主控已追记加边 TASK-003 ← TASK-002 (见「主控追记」段)。 (d) (e) 对含多个 head 的箭头段取最后一个 TASK 为 head: 形如「A ‖ B; C ← x」可解析, 但「A, B ← x」双头段只核 B —— R4/A1 de0fab44 已知限, 现行 execution_order 无此形态。
