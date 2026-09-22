---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-22T04:16:11.427Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R5 — tech-lead 席 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v2.4, source_sha `cf05d8b`)

## 已实读文件

派单 sha256[:16] = 966064f15d7ba98f

- 派单原件 `scratchpad/r5-prompts/tech-lead.md` (全文, 12864 字节)。
- 被审: `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (全文 232 行); `detailed-tasks.yaml` (全文 1818 行)。
- v2.4 实际改动: `git diff 71c500e b686185 -- openspec/changes/pre-merge-completeness-gate-change-scope/ .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` (全部 hunk)。
- R4 聚合 `.aria/audit-reports/post_planning-R4-2026-09-20T033000-000Z-...-aggregated.md` (全文)。
- 决策单 `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文 116 行)。
- proposal: `:1-22` (头部), `:103-125` (§1.0), `:356-406` (§4 / §5 / Impact), `:407-451` (Tasks), `:467-470` (SC-11 / SC-12 / SC-13 / SC-14), `:480-486` (rule6_note)。
- CLAUDE.md「多远程推送 — 两条硬约束」与不可协商规则 #3 / #6 / #8 / #10 (会话上下文已载入)。
- aria 子模块 (`1cb3872`): `skills/phase-c-integrator/SKILL.md` `:40-50` `:150-270` `:404-470` `:596-660` (CRLF, python 切行); `skills/git-remote-helper/scripts/push_all_remotes.sh` `:1-160`; `skills/git-remote-helper/SKILL.md` `:30-120`; `skills/config-loader/DEFAULTS.json` `:1-40`; `skills/phase-d-closer/SKILL.md` `:40-66` `:205-245`; `references/execution-steps.md` (全文); `references/handoff-mechanics.md` (全文); `templates/session-handoff.md` `:1-40`; `skills/state-scanner/SKILL.md` `:170-195`; `lib/constants.py` (SWEEP_TTL 行); `lib/claim_lifecycle.py` `:470-520`; `lib/reconcile.py` (Rule 6 段); `lib/collision.py` `:500-560`; `scripts/release_gate.py` `:85-175`; `scripts/lib/spec_complete.py` (status 读法段); `skills/phase-b-developer/SKILL.md` `:80-118`; `skills/openspec-archive/SKILL.md` (步骤目录与 Step 7); `skills/session-closer/scripts/handoff_autofill.py` (`--owner-container` 实跑)。
- standards (`940cb5b`): `conventions/session-handoff.md` (小节目录与 §2.3.7 E1 行)。
- 主仓: `.aria/config.json` (全文); `.aria/state-checks.yaml:29-46`; `.gitignore` / `aria/.gitignore` (workspace 条目); `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` `:87` `:200-240`; `aria-plugin-benchmarks/ab-suite/version.yaml` (头部); `docs/handoff/latest.md` `:1-30` 及 History 字样的历史; `docs/handoff/2026-09-13-aria-plugin-196-checker-hint-and-dotted-repo-shipped-v1.73.3.md:38`; 生效版 skill-creator (`installed_plugins.json` 指向 `ea0a38e1d671`) `SKILL.md:167`; 提交 `16b5bf1` / `ecb6296` / `2a46d08` / `71c500e` 的相关改动。
- 实跑 (全部在 `scratchpad/audit-R5-tech-lead/` 下, 共享副本经 `cp -a` 后使用, 真仓零 git 写): 生成器重放 `REGEN_IDENTICAL`; `standards_files_derivation` 以 `71c500e` 为输入复跑与嵌入 output 逐字节相同、以 `b686185` 为输入复跑; R4-M1 临时仓三态; 八个 standards 文件基线 diff; 版本点双边改动的同步合并模拟; 副本内 fetch origin `refs/aria/coordination` (`375517c`) 读本轨 claim 心跳史与 sweep 史。

## R4 对账

| R4 编号 | 键 | 判定 | 亲验证据 |
|---|---|---|---|
| R4-M1 | `d7f5b04c` | **closed** | `detailed-tasks.yaml:1193` 三组同口径 (standards 组先 `git -C standards fetch origin`、gitlink 取 `ls-tree` 第三字段、两端点 `cat-file -e`、零 diff = 退出码 0 且输出为空)。临时仓亲跑 (上游 standards 有新提交改 `git-commit.md`, 本地 clone 未 fetch): v2.3 做法 `stdout=[] rc=128` (按「输出为空」即假绿); v2.4 做法 fetch 后两端点 `cat-file rc=0`、`diff --shortstat` 得 `1 file changed, 1 insertion(+)` `rc=0` (转红); 真零 diff 文件 `stdout=[] rc=0`; gitlink 指向 origin 也没有的对象时 `cat-file rc=128` (停)。 |
| R4-M2 | `8d2e93ff` | **closed (原缺陷)**; 修法引入新 Major, 见 M1 | TASK-031 `detailed-tasks.yaml:1813-1817` 逐条对上 SOT: 五字段与 `aria/templates/session-handoff.md:1-7` 一致; 写后自校验命令与 `phase-d-closer/references/execution-steps.md:105-108` 逐字相同 (含 `head -8` 与口径注); latest.md 两子步与 `handoff-mechanics.md:106-124` 对上; `handoff_autofill.py --owner-container` 实跑得 `simonfish/bfe8285d` rc=0; 判断清单第 25 条 (`tasks.md:79`) 覆盖 `phase-d-closer/SKILL.md:65` 的 D.1 / D.post / D.2 / D.2b / D.3 与 `:226` 的 D.4。 |
| R4-M3 | `dec4ac57` | **closed** | TASK-030 `detailed-tasks.yaml:1779` 的 extra 只剩本次 ab-results 目录, 与 `commit_attribution` 用法注释一致; 生效版 skill-creator `SKILL.md:167`「Put results in `<skill-name>-workspace/` as a sibling to the skill directory」、`aria/.gitignore:6-7` `skills/*-workspace/`、主仓 `.gitignore:36-37` `aria-plugin-benchmarks/ab-workspace/` 实读与 v2.4 引述一致; 2026-04-10 之后提交 iteration 产物的 5 个提交全部落在 `ab-results/<结果目录>/` 内; `2a46d08` 结果目录形状 (PREDICTION / RESULT / benchmark.json / benchmark.md / `runs/eval-*/{eval_metadata.json, with_skill/*, without_skill/*}`) 与 v2.4 所列一致。 |
| R4-M4 | `5891aaeb` | **closed** | `standards_files` 8 条 (`detailed-tasks.yaml:79-86`); `21748d4..940cb5b` 八文件逐个亲跑: content-integrity `+56/-2`、skill-benchmark-exemption `+21/-3`, 其余六个 `rc=0` 且输出为空; `git -C standards diff --name-only` 全仓只这两文件; 派生脚本换 v2.4 自身 (`b686185`) 为输入复跑: 11 族 / 排除 3 / 保留 8 (session-handoff.md 已被第一步命中), 第二步补集 `[]` —— 集合稳定。 |
| `f5b3afad` | — | **closed** | 抽出 `standards_files_derivation.script` 在副本复跑, 与嵌入 `output` 逐字节相同 (`BYTE_IDENTICAL`): 10 族, 封闭排除 3 族 (含 README.zh.md), 余 7。 |
| `0f027861` | — | **closed** | 求法已是输入钉在冻结快照的可执行脚本, 复跑无歧义; 「语义判据 vs 字面求法」之差由第二步 (Rule #N → SOT) 补足, 剩余盲区已自述 (两个具体候选见「风险 / 疑问」第 4 条)。 |
| `cb1529a3` | — | **closed** | `detailed-tasks.yaml:163` 两处「六个文件」、`tasks.md:21`「这六个文件」「八份」、`detailed-tasks.yaml:39`「八个被引文件」互相一致; 旧计数只留在 revision_log 的历史条目。 |
| `f0e78a1e` | — | **closed** | TASK-029 deliverables 实读 9 项、无台账; revision_log v2.4 minor 条 (`detailed-tasks.yaml:758`) 勘正 v2.3 那句而不改原文。 |

## Findings

### M1 — `9c294cca` · major · issue · implementation · `detailed-tasks.yaml TASK-031`

**summary**: v2.4 把「latest.md 的 diff 在等待点 13 的授权请求里点明」定为判断清单第 28 条在 Phase D 的唯一落点, 但等待点 13 的「同批」授权在更早的 D.2b (release) 就必须用掉, 那时周期 handoff 与 latest.md 都还没写 —— 照字面执行不存在一条同时满足计划自身约束的路径。由 v2.4 返修 (R4-M2) 自身引入。

**证据**:
- `detailed-tasks.yaml:1811`: 「claim: 获授权 (owner_gates 第 13 项) 后先跑 metadata.coord_ref_precheck, 退出 0 才跑 … release_gate.py …; 未获授权或检查不过 ⇒ 不 release (不写仅本地的 release), 记周期 handoff」—— release 要第 13 项授权, 其结果还要写进之后才起稿的周期 handoff。
- `detailed-tasks.yaml:1817`: 「该提交按第 28 条「一律请裁」呈 owner: 在 owner_gates 第 13 项的授权请求里单独点明它的 diff」; `tasks.md:92` (第 38 条): 「在等待点 13 的授权请求里点明 —— … 不另立等待点」。
- `tasks.md:115`: 「| 13 | 5.9 | 推送: Phase D 提交与 `release_gate` 协调 ref | 同批授权 |」; `detailed-tasks.yaml:215`: 「Phase D 提交双推与 release_gate 的协调 ref 推送 (同批)」。
- 顺序: `tasks.md:178` 的 5.9 行 release 排在「周期 handoff … 再做 `docs/handoff/latest.md` 两子步」之前; `aria/skills/phase-d-closer/SKILL.md:65`「→ **D.2b claim 释放** … → **D.3 Session handoff**」, 计划第 25 条自称逐步对应。
- release 当场推送: `aria/skills/state-scanner/scripts/release_gate.py:96`「Library entry — fetch → release → optional sweep/gc → push.」
- 引入点: `detailed-tasks.yaml:755` (revision_log v2.4 R4-M2)「latest.md 的改动单独成提交, 在 owner_gates 第 13 项的授权请求里点明」。
- 旁证: `detailed-tasks.yaml:191` 硬约束「新写 claim、release_gate 的 release / sweep / gc、推 master / tag / gitlink 仍逐项授权」(owner 09-17 原意), 第 13 项把 release 与 Phase D 推送捆成「同批」, 该捆绑本身也未进判断清单。

**失败场景**: 执行者到 D.2b 必须先拿第 13 项授权才能 release → 按「同批」一次请求 (release + Phase D 提交双推) → 此刻 latest.md 未改, 请求里无从点明其 diff → owner 批准 → 之后写 handoff、改 latest.md、单独提交, 在这份已批准的同批授权下双推 → 共享指针改动未经 owner 过目即上两端, 第 28 条落空。另两条路各违反一条: 授权推迟到末尾 ⇒ release 晚于 handoff, 违反 `:1811`「记周期 handoff」与 D.2b→D.3 顺序; 分两次请 ⇒ 违反「同批」与第 38 条「不另立等待点」。

**建议修法**: 拆第 13 项为 13a (D.2b release 的协调 ref 推送, 逐项, release 前请) 与 13b (Phase D 提交双推, 在 latest.md 提交之后请, 请求附 latest.md 的 diff); `detailed-tasks.yaml:1811` / `:1817` / `:1818`、tasks.md 表第 13 行与第 38 条同步; 判断清单补一条说明拆分与「release 逐项」的关系。

### M2 — `3e6a8483` · major · issue · implementation · `detailed-tasks.yaml metadata.owner_gates 第 14 项`

**summary**: 全计划只在 TASK-001 解析一次本轨 claim 是否 active, 第 14 项 (重认领) 也只挂 TASK-001; 此后 Phase B–D 跨多日多会话, claim 存活全靠非强制、fail-soft 的 `/state-scanner` 入口心跳, TASK-024 的 AB 会话还按设计压制心跳推送 —— 而本轨实测心跳间隔多次超过 SWEEP_TTL (24h), 本仓 sweep 真实且反复发生。claim 中途被扫成 abandoned 时, 计划到 TASK-031 之前没有任何一步看得见, 到 TASK-031 也没有对应的合法下一步。

**证据**:
- 只有 TASK-001 处理 claim 状态: 对 31 个 TASK 的 verification 用 python 检索 `claim_not_found|abandoned|三元组|心跳|/state-scanner`, 实跑输出 `TASK-001 ['/state-scanner', 'abandoned', 'claim_not_found', 'heartbeat', '三元组', '心跳']` / `TASK-024 ['/state-scanner', '心跳']` / `TASK-026 ['/state-scanner']` / `TASK-031 ['/state-scanner']` —— 解析与 `claim_not_found` 分流只在 TASK-001。
- `detailed-tasks.yaml:216`: 「14 · TASK-001 (条件: 三元组解析不到本容器同轨的 active claim …)」—— 只挂 TASK-001。
- `detailed-tasks.yaml:1653` (TASK-024): 「被丢弃的只有本轨 --no-push 心跳, 下个会话重新刷新」—— 假设下个会话 claim 仍 active, 无核验。
- `detailed-tasks.yaml:192`: 「Phase B–D 的每个会话在调用 /state-scanner 之前也先跑 (…), 不通过则本会话不调 /state-scanner」—— 条件式, 不强制每会话心跳。
- SOT: `aria/skills/state-scanner/SKILL.md:183`「A.1 认领写下的 claim 若无人刷新, `SWEEP_TTL` (24h) 一到就被扫成 `abandoned` —— 一条还在干活的轨道会从所有碰撞面上消失」; `:191`「心跳失败只记遥测 … 绝不阻断扫描或后续阶段」; `lib/constants.py:58` `SWEEP_TTL: int = 86400`; `lib/claim_lifecycle.py` 的 `heartbeat_by_track` 只匹配 `active` (文档串「a claim nobody can refresh is swept to ``abandoned`` once ``SWEEP_TTL`` elapses」); `lib/reconcile.py:254-258` 唯一 active winner 心跳超 STALE_TTL (1800s) 即 `sole_active+stale_takeover_eligible`, `winner = None`。
- 实测可达 (副本 fetch origin `refs/aria/coordination` = `375517c`): 本轨当前 claim `claims/bfe8285d/s-73b9@1606.yaml` 在 origin 上的心跳提交 `2026-09-17T16:06:57` → `09-18T16:23:55` → `09-18T18:50:10` → `09-20T11:51:31` → `09-21T14:18:23`, 四段间隔 24h17m / 2h26m / 41h01m / 26h27m, **三段超过 24h**; 同一 ref 历史 `gc: sweep N stale active claim(s) → abandoned` 共 6 次 (`2026-07-11` … `2026-09-09`), 决策单 §3 第 3 条记两轨原 claim「09-10 已 sweep 为 abandoned」。本轨 A.2 期间没被扫, 只是这几个窗口恰好没人跑 sweep。
- 终局只在 TASK-031 显形: `release_gate.py:149-156` 无 active 匹配时 `released.success=False`、不写不推, `push_success` 停在 `:115` 的 `None` ⇒ `coord_push_verify` (a) 不成立 ⇒ 第 15 项; 第 15 项登记的是前置检查 / 推后核验失败, 不对应「claim 中途被扫」, 第 14 项又不挂 TASK-031。

**失败场景**: TASK-001 心跳核验通过 → Phase B 多日推进, 若干会话因等 owner (第 4 / 5 / 7 项等) 间隔超 24h, TASK-024 的 AB 会话按设计不推心跳 → 任一他轨 Phase D 的 D.2b 跑 `release_gate --sweep-stale` → 本轨 claim 变 abandoned → 之后每次入口心跳都 `claim_not_found`, 只记遥测 → 计划无一步复核, 执行者照常推进 → 本轨在所有他容器的碰撞面上数日显示无人认领 / 可接管, 计划自己在 `coord_push_verify.why` (`detailed-tasks.yaml:629`) 点名要防的后果「他容器据此接手本轨」经「时间间隔」这条路重新可达 → 直到 TASK-031 release 才撞上第 15 项, 且无登记的合法下一步。

**建议修法**: (1) 把 TASK-001 的三元组解析 + 心跳 + `coord_push_verify` 提为「每个 Phase B–D 会话的第一步」写进 `hard_constraints`, 解析不到 active ⇒ 第 14 项 (第 14 项挂载从 TASK-001 扩到任意会话); (2) TASK-024: owner 开 AB 会话前的最后一个普通会话补一次核验过的心跳, AB 结束后第一个普通会话先做 (1); (3) TASK-031 release 返回 `claim_not_found` 时单列处置 (呈 owner, 可选先走第 14 项补认领再 release); (4) 判断清单补一条「会话间隔须小于 SWEEP_TTL, 否则由 (1) 兜底」。

### M3 — `3782becc` · major · issue · implementation · `detailed-tasks.yaml TASK-030`

**summary**: 主仓 PR 恰是 bump aria gitlink 的 PR, phase-c-integrator 的 C.2.4.5 子模块指针回退闸在本仓取缺省 `block` (已启用), 但计划三文件对它零提及, TASK-030 与范围边界表只列 C.2.4 与 C.2.5 —— 照字面执行会静默略过一道已启用闸 (Rule #10), 而它正是 gitlink 回退的专设闸。

**证据**:
- `aria/skills/phase-c-integrator/SKILL.md:47`「`phase_c_integrator.submodule_gate.mode` | `"block"` (v1.49.0+ default)」; `:187-191` C.2.4.5 触发「C.2.4 verdict=green … 配置 … `"block"` (v1.49.0+ default)」; `:414`「v1.49.0+ (current): `mode=block` 默认 — 检测到 regression/divergence + 无 override → 拒绝 merge」; `:409` 源于 PR #123 静默子模块指针回退事故。
- `.aria/config.json` 中 `submodule_gate` 计数 0 ⇒ 取缺省 `block`。
- 计划零提及: python 统计 `C.2.4.5` / `submodule_gate` / `子模块指针` / `指针回退` / `pointer regression` / `Submodule Pointer` 在 yaml 与 tasks.md 均为 0; `C.2.4` 只出现在 `detailed-tasks.yaml:1781`「经 phase-c-integrator 过 C.2.4 pre-merge gate, 结论记台账」与 `tasks.md:126`「| C.2.4 pre-merge gate (Rule #8) / C.2.5 | `phase-c-integrator`, 由 5.8 调用 |」。
- 本仓实践当必跑闸记录: `docs/handoff/2026-09-13-aria-plugin-196-checker-hint-and-dotted-repo-shipped-v1.73.3.md:38`「C.2.4.5 submodule gate PASS (aria forward bump, mode=block)」。
- 结构性前提成立 (被审对象存在: PR 改 aria gitlink), 不属 Rule #10 白名单第四类; 前四轮报告对 C.2.4.5 零提及 (检索 R1–R4 全部 24 份, 0 命中)。

**失败场景**: 执行者照 TASK-030 逐条做: 同步合并 → 推分支 → PR → C.2.4 → 以 merge commit 合并 → 快进 → C.2.5, 台账只记 C.2.4 结论与 C.2.5 矩阵 → C.2.4.5 未跑、无记录 = 已启用闸被计划流程静默略过。其后果不止合规: 在 m2 描述的同步合并冲突里, 若人手解冲突时把 aria gitlink 取错一侧, TASK-029 的「只前进」断言早已跑过 (且基线是 feature 分支的旧 gitlink), 没有别的一步会拦。

**建议修法**: TASK-030 在 C.2.4 green 之后、合并之前加一条「经 phase-c-integrator 跑 C.2.4.5 (`scripts/submodule_gate.sh`, mode 读配置, 缺省 block), verdict 与逐子模块 GATE 行记台账; block ⇒ 停下上报」; tasks.md 5.8 行与范围边界表同步。

### m1 — `1453c41f` · minor · issue · testing · `detailed-tasks.yaml TASK-027`

**summary**: TASK-027 第 4 步 (b) 只比上游一侧 (`A..S3`), 不比 feature 一侧 AB 之后的改动 (W 之后); 而 TASK-026 第一次自检按设计会改本 cycle 新增行 (含两个 skill 目录与主仓 `ab-suite/audit-engine.json`), 再由 TASK-027 第 2 步提交 —— AB 实测的文本可能不是最终合并的文本, 且无一步看得见。

**证据**: `detailed-tasks.yaml:1711`「(b) git -C aria diff --stat <TASK-024 记下的 A> S3 -- skills/audit-engine skills/phase-c-integrator 有输出 ⇒ AB 实测的处方文本与将要合并的不同, 停下」; `:1690` TASK-026 第一次「aria: git -C aria diff <aria 起点>..HEAD 的 + 行 … 命中逐条改为全限定写法」; `:1709` 第 2 步「不为空 ⇒ 查明归属后在 feature 分支只 add 被改文件提交」; `tasks.md:73` 第 19 条只按「AB 基线与合并基线之间两个 skill 目录的 diff」判重跑。

**它怎么会红 (三态)**: 基线 (W 之后两目录无改动) —— 现判据与补全判据都无输出, 正确; 目标 (补 `git -C aria diff --stat W <feature HEAD> -- skills/audit-engine skills/phase-c-integrator` 与主仓 `git diff --stat <TASK-024 提交> HEAD -- aria-plugin-benchmarks/ab-suite/audit-engine.json`) —— TASK-026 改了处方文件即出输出, 逐 hunk 按 Rule #6 判据表分类; 坏实现 (现计划) —— TASK-026 改了 `execution-modes.md` Step 4–5 区间一句处方, 现判据仍无输出, 静默合并 AB 没跑过的文本。

**建议修法**: 第 4 步加 (c) 上述两条 diff; 非空时逐 hunk 判描述性 (substitute, 记入 `rule6_note`) 或处方性 (按第 4 项重跑 TASK-024)。

### m2 — `27cee280` · minor · risk · implementation · `detailed-tasks.yaml TASK-029`

**summary**: 主仓 feature 分支在 TASK-029 改九个版本同步面之前从不并入 `origin/master` (aria 侧 TASK-025 明确「改任何版本文件之前」先并入), 于是计划自称「常规情形」的 Phase B 期间他轨 aria 发版, 必然在 TASK-030 的同步合并里与本轨在同一批行上冲突, 落进第 19 条的「罕见路径 → 停下上报」。

**证据**: `detailed-tasks.yaml:1672` TASK-025「并入上游 (改任何版本文件之前)」; `:739` revision_log v2 PP1-M8 自检「TASK-025 的 merge 在改版本文件之前, 不会与自己的版本改动冲突」; TASK-029 (`:1756-1763`) 无主仓同步步骤, 同步只在 TASK-030 `:1781`「同步 origin/master 用 git merge」; `tasks.md:73`「Phase B 期间 aria 发版属常规情形 … 其余罕见路径 (并入冲突 / … / 合并冲突 …) 停下上报」。副本实跑: 从 `cf05d8b` 起两分支, 一侧把 README.md / CLAUDE.md 的 `1.73.3` 改成 `1.75.0`, 另一侧改成 `1.73.4`, `git merge` 退出 1, 冲突文件 `CLAUDE.md` 与 `README.md` (副本已复原)。另 `:1758` 的「只前进」基线取「动手时 git ls-tree HEAD aria」= 未同步的 feature 分支旧 gitlink, 而非 `origin/master` 当时的 gitlink。

**失败场景**: B–C 期间他轨发一次 patch (09-12 至 09-13 两天内发了三次) → 主仓 `origin/master` 的版本行改成他轨号 → TASK-029 在未同步的 feature 上把同一批行改成本轨号 → TASK-030 同步合并冲突 → 按第 19 条停下等 owner; 常规情形每次都停, 且人手解冲突时 gitlink 取错侧无闸 (见 M3)。

**建议修法**: TASK-029 第一步 `git fetch origin` 并在主仓 feature 分支 `git merge origin/master` (不 rebase; 冲突 ⇒ 第 6 项), 再改版本点; 「只前进」基线改取 `git ls-tree origin/master aria` 的第三字段。

## 对执笔人自报薄弱点的表态

1. **可接受**。修法不以递归 fetch 为前提, 临时仓三态已亲验 (见 R4 对账 R4-M1 行); 严重度前提窄于 R4 原文只影响「多常见」, 不影响「必须修」—— 按 git 对 on-demand 的定义, 只有超级仓这次 fetch 恰好取回改 gitlink 的提交时才下钻, 显式 fetch 加 `cat-file` 加退出码是对的。
2. **可接受**。依据是代码级而非猜测: 生效版 skill-creator `SKILL.md:167` 的默认落点在被测 skill 位于 `aria/skills/<name>` 时即 `aria/skills/<name>-workspace/`, 正被 `aria/.gitignore:7` 忽略; 2026-04-10 后提交 iteration 产物的 5 个提交全落结果目录。且计划有 fail-closed 兜底: TASK-024 快照比较的总则「本地面除结果目录外有变化 ⇒ 停下」对工作区落到未忽略位置照样触发, 不依赖「*-workspace/」词形。
3. **可接受, 但依据不完整 (新证据)**: 本仓 latest.md 曾有按 SOT 的 History 节 —— `16b5bf1` (2026-09-06) 加入「### History (收尾条目, 倒序; 每次 handoff 写出时 prepend — handoff-mechanics 子步骤 1)」, 同日在合并提交 `ecb6296` (aria-runner-bot) 中丢失, 此后 `grep -c History docs/handoff/latest.md` 为 0 (逐提交二分定位)。「本仓没有这张表」是一次合并吞掉的结果, 不是本仓约定。建议台账记这段来历, 并在呈 owner 的 latest.md diff 里给出「恢复 History 节」选项 —— 前提是 M1 修好, 否则 owner 根本看不到这份 diff。
4. **可接受** (无害, 多一个提交)。但 `detailed-tasks.yaml:1817` 给的理由「使周期 handoff 与归档的归属仍由 track-id 与归档路径判定」依赖一个 TASK-031 从不运行的归属判据 (与已知项 A 同根: `commit_attribution` 只在 TASK-001 / TASK-030 调用); 在 Phase D 它的实际价值只剩「让 owner 看到一份独立的 latest.md diff」, 而这恰被 M1 破坏。
5. **可接受**。去台账后 TASK-029 的 deliverables (实读 9 项) 与「主控只 add 九个文件」(`:1763`)、「trailer 无条件必带」(`:1761`)、第 16 项措辞、`cannot_catch` 的「共两组」四处字面一致; 另一选项 (保留台账、改第 16 项措辞) 会重新制造「deliverables 含 exclusive 路径」与「整条落 shared 集」的矛盾。
6. **可接受** (换人判据未触发), 但本轮再次印证同体自检的盲区类型: 我用与执笔不同的方法独立复算 (派生脚本换 v2.4 自身为输入、生成器重放、R4-M1 临时仓三态、八文件逐个亲跑), 四题返修结论无一被推翻; 出入全落在「没看到的面」—— M1 由 v2.4 返修自身引入, M2 / M3 是 v1 遗留、前四轮无人从「claim 跨会话存活」与「C.2 的全部已启用闸」这两个角度看过。

## 风险 / 疑问

1. **已知项 (A) 重评, 维持 minor 级, 不立 finding**: TASK-031 `:1813`「写成别的或漏写 ⇒ 判 foreign, 停在 owner_gates 第 16 项」在 Phase D 不可达属实 (`commit_attribution` 只在 TASK-001 / TASK-030 调用); 但漏写会被 `head -8` 五字段自校验 (须 ==5) 拦下, 只有「写了但值错」漏网, 后果是一份 handoff 被错归轨, 可事后修。建议删掉该虚设的兜底句, 或在五字段自校验后加一行 `grep -cx 'track-id: pre-merge-completeness-gate-change-scope' <handoff>` 须为 1。
2. **已知项 (B) 重评, 维持 minor 级**: TASK-027 第 4 步 (b) 的 A 与 S3 按构造在本地, 只有台账抄错 SHA 才会 `rc=128` 空串放行 —— v2.4 在 TASK-001 正是用同一「SHA 抄错」理由给 aria / 主仓两组补了退出码判据 (第 36 条), 4(b) 同口径补一句即可; `guard_config_hooks` 是管道, `git grep` 失败时后一个 grep 空输入照样「无输出」, 且 TASK-021 `:1587`「先跑 guard …; 再在主仓根 …」的「主仓根」只修饰后一条, 前一条 (`:1586`) 刚 `cd aria/skills/audit-engine/tests`, 在那里跑 `git grep` 只搜 aria 仓、看不到主仓 `.aria/config.json`。计划不改 config, 概率低。
3. **判断清单漏记的新对象** (与 R4 minor `ea958583` 同类、未获 owner 处置, 故不作 finding 重提): 第 13 项把 release 与 Phase D 推送「同批」(owner 09-17 原意为逐项, 见 M1); 5.9 行把 D.4 estimator 排在 D.3 之前 (`phase-d-closer/SKILL.md:226`「收尾**末位**子步 (D.3 之后)」), 周期 handoff 那几轮的 token 会记进下一 cycle; 主仓同步推迟到 TASK-030 (见 m2); TASK-001 之后 claim 存活只靠入口心跳 (见 M2)。
4. **standards 集合求法自述盲区的两个具体候选**: `conventions/changelog-format.md` (TASK-025 的 `### Added` / `### Changed` 与 TASK-027 第 3 / 6 步的 `^## \[x.y.z\]` 抽取都依赖它定义的格式; 当前 aria CHANGELOG 该抽取得 138 个小节, 判据非真空) 与 `conventions/submodule-pointer-hygiene.md` (其 Rule 4 即 TASK-028→029 先子模块后 gitlink 的顺序)。二者在 `21748d4..940cb5b` 零 diff (全仓只两文件变动, 实跑), 当前无害; 若并发轨在 B.1 前改它们, TASK-001 看不见。是否点名入集合由 owner 定。
5. TASK-031 要把 yaml 各任务 status 改成 completed 并回填 `rule6_note.scenario1`, 计划未说经生成器还是手改; 归档门在 tasks.md 存在时不读 yaml 的 status (`spec_complete.py` 模块头 `:13-16` 与 `:191-229`), 无功能影响, 只是归档后的 yaml 不再能由生成器重放。
6. frontmatter 的 `drift_check_skipped` 我写 `true`: 实读 `.aria/config.json` 的 `audit` 段无 `drift_guard` 键, convergence 未 opt-in, 与 R4 聚合对该字段的口径一致; 照抄派单模板的 `false` 会与事实不符。
7. **其余视角核查 (未立 finding)**:
   - 粒度: 31 项均 1–8h; 组 2 六项与 §1.0 的 P0/P1 (+同仓判定) → P2a/P2 (+ref 解析与陈旧比对) → P3/P4 → P5 (+早退豁免) → P6 → 收口一一对应 (proposal `:107-116`)。
   - DAG: TASK-007 起每项依赖前一项, TASK-002 / 003 并列后汇入 TASK-004, 与编号序一致; 后序读前序产物处均有传递依赖。
   - C.2.5 五问: 与 `phase-c-integrator/SKILL.md:603-638`、`push_all_remotes.sh:101-127` (推本地 master, 以 `refs/remotes/<remote>/master == HEAD` 判成功)、`DEFAULTS.json:6-15` (`fail_on_partial_push: true`, `read_only_remotes: []`)、`git-remote-helper/SKILL.md:40` (`verify_parity_post_push` 纯 ls-remote) 逐条一致; 本仓 config 无 `multi_remote` 段。
   - 两条硬约束: 5.5 本地 `merge --no-ff` + 双父断言; 5.6 每端一条 `--atomic` 推送 + 逐 remote `ls-remote` 核 master / tag / peeled; 5.7 双端核验一致后才 bump、只前进断言; 5.8 主仓走 Forgejo 合并属约束 1 的主仓例外, C.2.5 前断言三个子模块本地 master = HEAD = 两端 (他轨子模块前进时会停, 方向 fail-closed)。
   - 10CG/Aria#195 / #211: 取号「三者取高」+ TASK-027 / 028 两次 tag 查重可执行; `ab-suite/version.yaml` 现为 1.5.0 (#211 的 T4 已 deferred), 执行时读 `origin/master` 的口径可执行。等待点 1 仍卡 (#195 轨 yielded、无人推进), 属已知 owner 门。
   - 外向动作登记: 除 M1 的时序问题外, 推送 / 开单 / 回帖 / tag / 协调 ref 写入均有对应等待点; openspec-archive 唯一的外向动作 (Step 7 建 tracker) 由第 11 项管住。

## Verdict

**PASS_WITH_WARNINGS** — counts **0C/3M/2m** — **Vote: REVISE**

## 是否足以开始 Phase B

不足以: M2 从 Phase B 的第一个会话起就生效 (TASK-001 之后不再复核 claim 存活), M1 / M3 虽落在 C / D 段, 但计划是执行 SOT, 应先改; 另等待点 1 (10CG/Aria#195 完成 C.2 或 owner 明示改序) 仍未满足。
