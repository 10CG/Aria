---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T05:00:04.354Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [backend-architect]
---

# post_spec R2 单席报告 — backend-architect (数据契约与实现可行性)

本席为 R2 新席位, 不继承 R1 结论。所有事实对 SOT 副本 (`~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/`, = `301641b`) 与本仓语料实读/实跑复核; 语料统计一律对冻结快照 `3f4b379` 跑 (活体目录本轮仍在增长: 快照 778 顶层 `.md`, 实读时 802)。本轮只审不改, 未触碰仓库任何文件。

## 审计结论

### Decisions

- [minor] testing/R1 五条 Critical 的落地复算: R1 五条 Critical 均在正文落地且本席独立复算无误差 (对 `3f4b379`): 末段形态 **62** 份、**25** 个 (checkpoint, change_id) 组合的全部自有报告都是末段形态、`excluded_legacy_count`=**6** 与 `unattributed_count`=**170** 的拆分 (原合并口径 238)、`C`=**152** (9 changes + 143 archive; 前缀碰撞 1 对 `aria-orchestrator ⊂ aria-orchestrator-divestiture`, 后缀 0, 中缀 0)、§1.3(c) 的 **52 / 15 / 37**、旧 schema `{timestamp}` 残留恰 **4** 处、case-2 的 499 / 209 / 3。F2 的 `-R\d+-` 缺失计数 (24 / 2 / 1 / 1) 亦逐个复现。(证据: proposal.md:49-53,113-115,153 vs 本席对 `git ls-tree 3f4b379 .aria/audit-reports/` 的全枚举)
- [minor] architecture/§5 向后兼容消费方枚举: §5 的枚举实测成立 —— 全 skill 树对 `allow_incomplete_checkpoints` / `missing_checkpoint` 零代码消费方 (仅两处 `.py` 命中, 是 stderr lint 里同名散文: `state-scanner/scripts/lint_stderr_typed_channel.py:9-10,78` 与 `collectors/_common.py:465`, 与本门无关); 文件名 schema 消费方 `collectors/audit.py:52,62-114` 与 `aria-dashboard/references/parse-rules.md:76-105` 均只读文件名, `spec_complete.py:930` 仅注释提及 ⇒ 「本 spec 只读文件名、不改 writer schema ⇒ 两者零影响」成立。

### Issues

- [critical] architecture/§1.4 空集短路 (no_checkpoints_configured): 空集短路把 **owner 显式把其余 checkpoint 设为 off** 判成「零证据」并硬失败。官方文档的两个采用场景直接被击穿 —— 场景 A「仅启用合并前审计 (低成本起步)」(`config-loader/config-example.md:381-400`: `mode=manual`, `pre_merge=convergence`, 其余全 off) 与场景 B (`:402-417`: `mode=adaptive`, 无 `checkpoints` 块) 都得 `checked_checkpoints == []` ⇒ `verdict=error` exit 2 ⇒ 按 §1.4 的消费方 fail-closed 义务, **pre_merge 审计恒不执行且合并恒阻断**。而 `allow_incomplete_checkpoints` 只豁免 S4 / missing (proposal.md:95), 对 `error` 明示不豁免 ⇒ **无任何配置逃生口**。该路由还与 Rule #10 白名单**第一类**正面冲突 (`standards/conventions/configured-gate-authority.md:35`「配置显式关闭」是合法豁免来源, 不是缺证据); SC-15 (proposal.md:259) 的三个 fixture 全是 `audit` 未启用的场景 (那些本就由 `phase-c-integrator/SKILL.md:131` 早退), 恰恰**没有**覆盖危险的那格 (enabled=true + 只开 pre_merge), 却把这条路由钉进测试。 (证据: proposal.md:163,95,259 · config-example.md:381-400,402-417 · configured-gate-authority.md:35)
- [critical] architecture/§1.3 Step 3 checkpoint 枚举源: Step 3 原样继承「对 `audit.checkpoints` 中每个 key」, 不过 SOT 的优先级链「`checkpoints` 显式值 > `adaptive_rules` 推导值 > 默认 off」(`audit-engine/SKILL.md:391`, `config-example.md:280`, `execution-modes.md:15`)。后果两向: (1) 场景 B (adaptive 且无 `checkpoints` 块) 经 config-loader 与 `DEFAULTS.json` 合并后八键字面全 `"off"` ⇒ 空集 (叠加上一条的硬红); (2) 场景 C「混合模式」(`config-example.md:419-440`: adaptive + 只显式写 `post_spec`/`post_closure`) 下 `post_implementation` 由 `adaptive_rules.level_2=convergence` 启用, 却因字面值是 DEFAULTS 填的 `"off"` 而**不被枚举** ⇒ 该 checkpoint「该跑没跑」查不出 = **与被修 bug 同型的假绿**。把散文 Step 3 机械化, 恰恰是必须定义「用户显式值 vs DEFAULTS 填充值」如何区分的时刻 (散文时代 AI 还能看原始 `config.json`, 脚本拿到的是合并后的对象), 本 spec 全文未定义。 (证据: proposal.md:141,163 · audit-engine/SKILL.md:391 · config-example.md:276-280,402-440 · config-loader/DEFAULTS.json audit.checkpoints 八键全 off)
- [major] implementation/§1.4 config 读取「一律经 config-loader」: 该条对一个 stdlib-only Python 脚本不可实现 —— `skills/config-loader/` 只有 `SKILL.md` / `DEFAULTS.json` / `config-example.md`, `find -name '*.py'` 空, 且 `SKILL.md:8-10` 标 `user-invocable: false` / `disable-model-invocation: true` / `allowed-tools: Read, Glob`, 它是**给 AI 读的散文 Skill**, 没有程序化入口。可行形态只剩「自读 `.aria/config.json` + 自读 `../config-loader/DEFAULTS.json` + 在 Python 里重实现 §旧配置兼容层 (`config-loader/SKILL.md:305-331`) 的映射」= **第二份副本**, 正是 §5 宣称随 `scope_skip_paths` 一并消失的那类漂移风险, 且无相等性 SC。另: 调用契约 (proposal.md:73-76) 没有给脚本定位 `DEFAULTS.json` 的参数 (只能靠 `__file__` 相对路径, 跨 skill 依赖未成文), `error_kind` 封闭集只有 `config_unreadable` 覆盖 `.aria/config.json`, 没有 DEFAULTS 缺失/损坏一格。 (证据: proposal.md:159,164 · config-loader/SKILL.md:1-11,305-331 · 目录实读)
- [major] implementation/§1.2b 与 §1.4 的 stdout 顶层键集: §1.2b (proposal.md:134) 与 SC-19 (:262) 要求 stdout 输出 `scanned_dir_depth: 1`, 而 §1.4 (:164) 声明「顶层键集**逐字**为」的 13 键里没有它, SC-10 (:253) 又断言「顶层键集逐字 = 1.4 列表」⇒ **SC-10 与 SC-19 结构上不可能同绿**。根因是 §1.2b 为 2026-09-07 追加 (提交 `8da3518`), 未回灌 §1.4 的键集与 SC-10。 (证据: proposal.md:134,164,253,262)
- [major] testing/SC-14(a) 照跑面第三腿: SC-14(a) 与 rule6_note 把 `ab-suite/phase-c-integrator-pre-merge-gate.json` 当第三个 AB 套件「各跑一次 with/without 臂 … 无回归」。实读该文件: `type: "workflow_skill_subextension"`、**无 `evals` 键**、8 条 `fixtures[]` 每条带 `test_case_in_unit_tests: test_pre_merge_gate.GateCheckTests.*` (它驱动的是单测, 不是 `/skill-creator` AB); `ab-suite/version.yaml` 的 `total_eval_cases: 84` 按 `sum(len(evals))` 计其为 **0**。对 0 eval 的文件断言「无回归」恒真 ⇒ 这条 Rule #6 证据腿是假证据。另 `phase-c-integrator.json` 的 3 evals 实读为 C.1 commit 生成 / C.2 冲突处置 / C.2.5 多远程推送, 无一触 pre_hook 步骤 4/4.5 ——「照跑验漂移」的理由成立, 但「本 spec 改其处方面所以要跑它」的因果在这两个文件上不成立, 应改写。 (证据: proposal.md:239,257 · ab-suite/phase-c-integrator-pre-merge-gate.json 全文 · ab-suite/phase-c-integrator.json evals[1-3] · version.yaml:5)
- [major] documentation/§4 ab-suite/version.yaml 版本基线: 头部 Rule #6 段与 §4 表两处称 `ab-suite/version.yaml`「(套件版本) 现值实测 **1.4.0**」并计划「1.4.0 → **1.5.0**」。实读 `version.yaml:1` 已是 **`1.5.0`** (`last_modified: 2026-09-05`, changelog 顶条即同伴轨 `a1-entry-claim-duplicate-work-guard`)。溯源: `git show 3f4b379:…/version.yaml` = 1.4.0, 但 `ecb6296` (Merge origin/master) 已把同伴的 `5697477` 合进本地 master, 且该轨 PR #202 已 merged (`9f25a66`) ⇒ **撞号已经发生, 不是「在飞轨的未来风险」**; 照 §4 字面执行会用一个已发布的号并覆写他人 changelog 条目。 (证据: proposal.md:12, §4 version.yaml 行 · ab-suite/version.yaml:1-3 · git log 5697477 / ecb6296 / 9f25a66)
- [major] implementation/§1 `--base` 绑定与 S3 交叉核验: `--base` 定义为「主干真实名 (本项目 `master`)」= 裸本地分支名 (proposal.md:83), 而它自称「与 `audit-engine/SKILL.md:406` 同命令」的那段 SOT, base 是**远程跟踪 ref** (`:404-405`: config 的 base 或 `git symbolic-ref refs/remotes/origin/HEAD`, fallback `origin/main`→`origin/master`)。命令形一致但 `<base>` 绑定不同: 子模块 detached HEAD / 本地 `master` 陈旧 (本项目常态) 下 `merge-base HEAD master` 偏移且**不报错**, diff 偏小 ⇒ S3 的机械交叉核验「diff 不触 `openspec/changes/**`」假通过 ⇒ 全部 checkpoint 记 `not_applicable/level1-no-spec` = 假绿 (R-b 只写了「调用方声明可绕」, 没写「核验本身会被陈旧 ref 悄悄弱化」)。另 §3 (proposal.md:183) 给 phase-c-integrator 的接线只追加 `change_id` / `repo_path` / `diff_repo_path`, 漏了必填的 `--base` (SC-10 断言其缺失即 argparse exit 2)。 (证据: proposal.md:83,92,183,253 · audit-engine/SKILL.md:404-406)
- [minor] implementation/§1.1 S3 的 results 形状: S3 (`--no-spec`) 下 `change_ids=[]` 却要求「全部纳入校验的 checkpoint 记 `not_applicable(reason=level1-no-spec)`」, 而 `results` 元组含 `change_id` 字段, 其取值 (null / 省略 / 空串) 未定义; not_applicable 的 trail 模板 `[INFO] … {cp}@{change_id} …` (proposal.md:170) 在无 change_id 时无从渲染。对照 S4-bypassed 已显式定义 `results=[]` (:103), 这一格是同类漏定义。 (证据: proposal.md:92,103,164,170)
- [minor] implementation/错误路径: 报告目录不存在: `.aria/audit-reports/` 不存在这一格全文未定义 —— 首次启用 pre_merge 的采用方正是这种状态。`iterdir()` 对不存在的目录抛 `FileNotFoundError`; `error_kind` 封闭集 (proposal.md:164) 无对应项; SC-10「四种 verdict 下 stdout 均可 `json.loads`」与 R-d「失败落 `git_failed` exit 2, 不 crash」对该路径都无源 (方向上被消费方 fail-closed 兜住, 但契约与断言口径不闭合)。 (证据: proposal.md:134,164,253 · R-d 行)
- [minor] implementation/§1.1 S1-S2 作用域解析边界: (1) S2 只取 `openspec/changes/<id>/` 前缀 (proposal.md:91), 而 §1.3(b) 的路径集显式含 `openspec/archive/**` (:148) ⇒ 纯归档 PR (D.2) 走到 S4 `change_scope_unresolved` exit 2, (b) 的 archive 分支只有显式 `--change-id` 时可达 (两条条款不自洽); (2) S1 锚点沿用 `pre-write-validation.md:25` 的 glob `archive/*-{id}/`, 前缀不设界, 与 §1.1 自述「逐字目录名」矛盾 —— `--change-id orchestrator` 会匹配 `2026-…-aria-orchestrator`, 拼错的短 id 变成假红 `missing` 而非 `change_id_unanchored` (S1 的设计目的正是把拼写错拦成 error)。 (证据: proposal.md:90-91,148 · pre-write-validation.md:24-26)
- [minor] documentation/头部基线冻结与本地状态: 头部 (proposal.md:10)「本地 checkout 仍停在 `0545f86` 且本地 master 与 origin/master 已分叉: Phase B/C 开工前必须先 fetch + 对齐, 否则主仓同步会把 gitlink 回退到 v1.70.0」现已不成立 —— 实测 `git ls-tree HEAD aria` = `301641b`、`git ls-tree origin/master aria` = `301641b`、`master` = `origin/master` = `git ls-remote origin master` = `e58ac22f5f04`, 无分叉、无回退风险。动作本身 (fetch 对齐) 无害, 但前提已过期, 会误导 Phase B 去处理一个不存在的风险。 (证据: proposal.md:10 · 本席 git ls-tree / ls-remote 实测)

### Risks

- [minor] implementation/§1.4 unattributed 输出面: `unattributed` 契约上是**全局扁平**文件名列表 (proposal.md:165), 但 audit trail 行按 checkpoint 参数化 —— `[WARN] unattributed reports ({cp}): <文件名逐个>` (:169), 而 JSON 里没有 checkpoint 维度 (SC-4 断言的就是一个扁平 list)。可由文件名前缀反推分组, 但契约没写。更实际的问题: 本仓实测 **170** 份, 而写侧强制被显式 defer (R-a) ⇒ 该数不会自然收敛 ⇒ 每次 pre_merge 运行往 audit trail 倒 170 个文件名, R-a 所依赖的「显影」会退化成被读者跳读的固定噪声。建议契约给出分组或截断口径 (前 N + 计数, 或落独立文件) 并配 SC。 (证据: proposal.md:124,165,169,250 · 本席对 3f4b379 的全枚举 = 170)

## Verdict

**FAIL** — Critical 2 / Major 5 / Minor 5 (另 2 条 decision 不计入缺陷计数)。

rationale: 本轮不是「R1 的修法没落地」—— 恰恰相反, R1 五条 Critical 的修法在正文全部落地, 且其载重数字经本席对冻结快照 `3f4b379` 独立全枚举后**逐个复现无误差** (62 / 25 / 6 / 170 / 152 / 52-15-37 / 4 处 / 499-209-3), §5 的消费方枚举亦实测成立。判 FAIL 的是 R1 rework **新引入**的两条: (1) 为堵「真空绿」而加的空集短路, 把 Rule #10 白名单第一类 (owner 显式 off) 误判成零证据并硬失败, 且明示不受 `allow_incomplete_checkpoints` 豁免 ⇒ 官方文档场景 A/B 两个采用路径变成无逃生口的 exit 2 恒阻断; (2) Step 3 的枚举源仍是字面 `audit.checkpoints`, 没过 SOT 的 `adaptive_rules` 优先级链 ⇒ 场景 C 下经 adaptive_rules 启用的 checkpoint 根本不被枚举, 造出与被修 bug **同型**的新假绿。两条同根: 把散文闸门机械化时, 「checkpoint 到底启没启用」这个输入端的判据没有随之机械化。五条 Major 里三条是可执行性硬伤 (config-loader 无程序化入口、`scanned_dir_depth` 使 SC-10 与 SC-19 互斥、0-eval 的 fixture 套件被当 AB 腿), 两条是事实/绑定错 (version.yaml 已 1.5.0、`--base` 裸分支名弱化 S3 核验)。

## 待 owner 复议

- **「只开 pre_merge、其余 checkpoint 显式 off」应判 pass 还是 error**: 这是语义选择, 不是实现细节 —— 本席认为它落在 Rule #10 白名单第一类 (owner 已显式关闭 ⇒ 无前置对象可查), 与 S4「有 change 但零证据」不同类, 故应 `verdict=pass` 并 surface `[INFO] 无前置 checkpoint 纳入校验 (全部由 config 显式 off)`; 若 owner 坚持 error, 则至少需要一个可配置逃生口 (现设计连 `allow_incomplete_checkpoints` 都不豁免它)。本条不改变上面两条 Critical 的存在性 (场景 B/C 的 adaptive 枚举缺口独立于此裁决)。

## 轮次记录

### Round 2

- Agents: backend-architect (本席; 五席并行, 本报告仅本席结论, 不代表聚合)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 14 (Decisions 2 / Issues 11 / Risks 1)
- Vote: REVISE (Critical 2 ⇒ verdict FAIL)
