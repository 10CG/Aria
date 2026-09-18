---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-18T16:43:27.817Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席 (10CG/Aria#199, A.2/A.3 v2.1 `5d435e9`)

## 已实读文件

被审对象 (全文):

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (224 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (1613 行: metadata 全部 30 键 + 31 个 TASK)

规范与决策:

- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` —— §1.0 求值总序 (`:103-151`)、canonical 调用串 (`:76-81`)、§5 向后兼容全段 (`:370-391`)、SC-5 (`:461`)、SC-6 (`:462`)、SC-7 (`:463`)、SC-9 (`:465`)、SC-11 (`:467`)、SC-15 (`:471`)、SC-20 (`:476`)、SC 表目录 (`:453-479`)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文, §1–§5)
- `CLAUDE.md` 多远程推送两条硬约束与不可协商规则 3 / 6 / 8 / 10 (session 自动加载)
- `standards/conventions/skill-benchmark-exemption.md` (现行全文 + `21748d4..940cb5b` 全 diff)

源码 (实读, 行号以我实读为准):

- `aria/skills/phase-c-integrator/SKILL.md` `:55-60` / `:128-136` / `:153-160` / `:595-700` / `:748-758`
- `aria/skills/audit-engine/SKILL.md` `:418-426`
- `aria/skills/git-remote-helper/scripts/push_all_remotes.sh` `:19` `:49` `:60-125`
- `aria/skills/git-remote-helper/scripts/verify_post_push.py` `:15-185`
- `aria/skills/config-loader/DEFAULTS.json` `:1-20`
- `aria/skills/state-scanner/scripts/phase1_gate.py` `:52-136` (import) / `:140-200` (GateOutcome / AdvisorySurface) / `:1125-1200` (`_heartbeat_only`)
- `aria/skills/state-scanner/lib/claim_lifecycle.py` `:475-524` (`heartbeat_by_track`)
- `aria/skills/state-scanner/scripts/release_gate.py` `:10` `:253`
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` `:2-60` / `:186-303`
- `aria/skills/state-scanner/scripts/lib/carry_forward.py` `:14-30`
- `aria/skills/state-scanner/SKILL.md` `:178-186`
- `aria/skills/run_all_tests.sh` `:35-50`

其他实读: `.aria/audit-reports/post_planning-R1-...-aggregated.md` (全文)、`.aria/config.json` audit 块、`.aria/state-checks.yaml` `:25-50`、`docs/handoff/latest.md`、`docs/handoff/2026-09-17-199-a2-a3-v2-r1-paused-handover-to-twin.md` §0、`refs/aria/coordination` 上的三份本轨 claim 文件、`aria-plugin-benchmarks/ab-suite/version.yaml` 与 `audit-engine.json`。

实跑 (全部只读, 或只在我自己的 scratch 目录 `…/scratchpad/audit-R2-tech-lead/` 内写):

- 把 yaml 的 `metadata.commit_attribution.code` 原样取出, 跑在真仓历史上: `a563192..5d435e9` (21 提交) 与 `1b9734a^..1b9734a` / `5fe15b0^..5fe15b0` / `c9fe08f^..c9fe08f`
- 模拟 TASK-031 的一次性勾选 (scratch 副本) 后调 `spec_complete.is_spec_complete`
- `git ls-remote origin refs/aria/coordination` 与本地值比对; `git -C standards diff 21748d4 940cb5b`; 各子模块 `remote -v` / `rev-parse --abbrev-ref HEAD`
- 真仓内零写入, 零 git 写操作 (只用 log / show / diff / diff-tree / ls-tree / merge-base / ls-remote / rev-parse)

## Findings

按 critical → major → minor 排序; 本轮 0 critical。

---

### M1 · `ecee072b` · major · issue · architecture · scope: `detailed-tasks.yaml TASK-001`

**一句话**: B.1 入口把 claim 身份写死在容器 `023236f2` 的某一份具体 claim 文件上, 而该 claim 现为 `yielded`、持 active claim 的是执行容器 `bfe8285d`; 任务只枚举了 active / abandoned 两态, 现态两态都不是, 照字面执行没有合法下一步。

**证据 (实读)**:

计划侧四处把身份钉死:

- `detailed-tasks.yaml:15` — `container: simonfish/023236f2`
- `detailed-tasks.yaml:16` — `claim: 'A.2 实读: … 的 claims/023236f2/s-86f7@1836.yaml, track_id pre-merge-completeness-gate-change-scope …, status active, phase A.2, heartbeat 2026-09-17T08:47:15Z'`
- `detailed-tasks.yaml:990` (TASK-001) — `'claim: 读 git show refs/aria/coordination:claims/023236f2/ 下 track_id 逐字为 pre-merge-completeness-gate-change-scope 的 active 条目 …'`, 之后只有一条替代分支: `'claim 已被扫成 abandoned ⇒ 获授权 (owner_gates 第 14 项) 后 … 重新认领'`
- `detailed-tasks.yaml:559` — `own_claim_files: 'TASK-001 读到的本容器同 track 的 active claim 文件 (A.2 时: claims/023236f2/s-86f7@1836.yaml); 重新认领后换成新文件'`

协调 ref 现态 (本地 = origin = `6ddf089`, 我用 `git ls-remote origin refs/aria/coordination` 与 `git rev-parse` 各取一次, 两值相同):

```
claims/023236f2/s-86f7@1836.yaml   status: yielded   heartbeat_at: '2026-09-17T11:54:49Z'   phase: A.2
claims/bfe8285d/s-73b9@1606.yaml   status: active    heartbeat_at: '2026-09-18T16:23:55Z'   phase: A.2
```

两份 `track_id` 都逐字是 `pre-merge-completeness-gate-change-scope`。执行侧身份: `hostname` = `dev-claude2`, 即 `bfe8285d`。`docs/handoff/2026-09-17-…-handover-to-twin.md` §0 第 2 条逐字记了这次让出: 「本容器 `023236f2` 的两条 claim 已于 09-17T11:55Z 经 owner 授权 `release_gate --status yielded` 让出」。

状态词表比计划枚举的宽: `release_gate.py:253` 的 `choices=["done", "yielded", "abandoned"]`, 加上 `active` 共四态; 计划只覆盖两态。

心跳的匹配面与容器绑定: `lib/claim_lifecycle.py:475-493` 的 `heartbeat_by_track` 文档串逐字「Refresh THIS container's active claims for a track」, 且「same three-way conjunction on container / normalized track_id / `active`」。

前置检查的判据: `detailed-tasks.yaml:541` `own = set(sys.argv[1:])`, `:553` `hb = (bool(files) and set(files) <= own and len(changed) == 2 * len(files) …)`。

**失败场景 (照字面执行)**:

路径一 (严格照 `:990` 读): 执行者 `git show refs/aria/coordination:claims/023236f2/s-86f7@1836.yaml` 得 `status: yielded` —— 不是 `active` (走不了心跳分支), 也不是 `abandoned` (进不了 owner_gates 第 14 项的条件)。计划在此没有第三条分支 ⇒ 停在 TASK-001 且没有可执行的下一步。若执行者硬套第 14 项去请授权重新认领, 请求的是一个并不需要的授权 (本容器已持 active claim), 而 `--mode advisory` 下的再次认领会写出第二条 claim —— 正是 tasks.md 判断清单第 11 条要防的那件事。

路径二 (按 `:559` 的意图换成自己的 claim): 心跳 `phase1_gate.py --heartbeat-only` 经 `heartbeat_by_track` 写的是 `claims/bfe8285d/s-73b9@1606.yaml`; 而 `own_claim_files` 仍是 `023236f2` 那份 ⇒ 下一次 `coord_ref_precheck` 里该领先提交的 `files` 不是 `own` 的子集 ⇒ `hb=False` ⇒ `kind="other"` ⇒ exit 1 ⇒ 按 `hard_constraints` 与 owner_gates 第 15 项: 心跳改 `--no-push`、本会话不调 `/state-scanner`、停下请授权。同样停在 TASK-001, 而且此后每个会话都会再撞一次。

**它怎么会红 (三态)**: 基线 = `own` 钉 `023236f2` 而执行者是 `bfe8285d` ⇒ 首次心跳落地后 `coord_ref_precheck` 恒 exit 1 (此刻还是 exit 0, 因为本地与 origin 协调 ref 相同, `local_ahead=0`, 尚无领先提交); 目标 = `own` 由 TASK-001 实读回填 ⇒ 心跳后 exit 0 且领先项 `kind=own-heartbeat`, 与 `metadata.v2_state_runs` 的 N6 目标态输出一致; 坏实现 = 把 `own` 放宽成整个 `claims/` 前缀 ⇒ 他轨 claim 写入也判 `own-heartbeat`, 该检查失去全部意义。

**建议修法**: (1) TASK-001 第一步改为「先取本容器标识 (`phase1_gate` 输出里的 `own_claim` / `container`), 再按 (container, 归一 track_id) 在协调 ref 里定位」, 不写死容器目录; (2) 状态分支补齐四态 —— `yielded` 且本容器已有 active claim ⇒ 直接心跳, `yielded` 且本容器无 claim ⇒ 走授权重认领 (这才是第 14 项的真实触发条件, 现在的措辞「已被扫成 abandoned」过窄); (3) `own_claim_files` 明确为「由 TASK-001 实读结果回填的运行时值」, metadata 里的路径标成示例; (4) `metadata.container` / `metadata.claim` 改成「A.2 执笔容器」, 与「执行容器」分列。

**与 v2.1 返修的关系**: 同一根因。v2.1 修掉的是 N6 **fixture** 与执笔容器身份的耦合 (换容器必判 `other`); 这一处是同一耦合留在**执行面参数**上的那一半, 返修没有一并扫到。

---

### M2 · `9122f4a9` · major · issue · implementation · scope: `detailed-tasks.yaml metadata.commit_attribution`

**一句话**: 提交归属检查的 `FIXED` 路径集把「并发发版轨的主仓同步面提交」整条判为 `own`, 而这正是它 (R1-M7 的处置) 要拦的那一类; 我用计划自己的代码在真仓历史上实测三例, 全部判 `own` 并 exit 0。

**证据 (实跑, 代码原样取自被审 yaml)**:

判据本体 `detailed-tasks.yaml:580` 与 `:585-604`:

```
FIXED = {"aria", "VERSION", "README.md", "README.zh.md", "README.ja.md", "README.ko.md", "CLAUDE.md",
         "docs/architecture/system-architecture.md", "docs/architecture/version-scheme.md",
         "aria-plugin-benchmarks/ab-suite/audit-engine.json", "aria-plugin-benchmarks/ab-suite/version.yaml"}
…
kinds.append("own" if files and all(own_path(c, p) for p in files) else "foreign")
```

跑在真仓三个他轨提交上 (只读):

```
1b9734a  chore(release): aria-plugin v1.73.3 主仓同步面 — gitlink fcbc8ac→1cb3872 (aria-plugin#196)
         触及 CLAUDE.md / README.md / README.zh.md / README.ja.md / README.ko.md / aria /
              docs/architecture/system-architecture.md / docs/architecture/version-scheme.md
         ⇒ {"verdict": "ok", "commits": 1, "kinds": ["own"]}
5fe15b0  chore(release): aria-plugin v1.73.2 主仓同步面 (同形态)   ⇒ {"verdict": "ok", …, "kinds": ["own"]}
c9fe08f  chore(aria): gitlink 308ccce→fcbc8ac (只动 aria 一个 gitlink) ⇒ {"verdict": "ok", …, "kinds": ["own"]}
```

这一形态在本仓是常态而非边角: `git log --grep='chore(release)'` 最近 8 条全是「aria gitlink + VERSION + 四份 README + CLAUDE.md + 两份架构文档」这一固定组合, 与 `FIXED` 几乎逐一对应。

对照组说明检查在别处是好的: 同一段代码跑 `a563192..5d435e9` 得 21 个提交 `4 own / 17 foreign` —— 他轨提交只要多碰一个非 `FIXED` 路径 (如 `openspec/changes/rule6-…/proposal.md`、`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`) 就正确判 `foreign`。漏的恰恰是「整条提交全落在 `FIXED` 集里」的纯发版同步面。

**失败场景**: TASK-001 的回落分支 (主仓起点回落为含规划提交的本地 master) 与 TASK-030 开 PR 前, 都要对 `origin/master..<ref>` 跑这个检查。若该区间含并发发版轨尚未推送的同步面提交, 检查 exit 0 ⇒ owner_gates 第 16 项不触发 ⇒ 该提交随本轨一起被推两端 / 随 PR 合入 master。最坏形态是它携带的 `aria` gitlink bump: 若对应的 aria 提交还没推两端, 就当场复制出 CLAUDE.md 多远程硬约束 1 点名的 orphaned gitlink (GitHub `clone --recursive` 断裂, 2026-07-14 事故形态)。R1-M7 的处置原话是「有非本轨提交即停」, 对本仓最高频的那一形态没有兑现。

**为什么是 major 不是 critical**: owner_gates 第 2 / 9 项仍要求把 `git log --oneline origin/master..<ref>` 清单随授权请求呈 owner, 人这一关还在, 所以不是静默误推。若哪天把「清单呈递」省掉或只呈机器判据, 同一缺口即升 critical。

`metadata.commit_attribution.cannot_catch` 已自报「本轨路径集内的他轨改动会判 own」, 但自报的是「同一个文件被他轨改动」这一较弱形态; 实测命中的是「整条提交全在本轨路径集内」, 更强, 且正是该检查的设计目标人群。

**它怎么会红 (三态)**: 基线 (今天的判据) = 他轨发版提交 `ok/own` (上面三例实测); 目标 = 同样输入判 `stop/foreign`; 坏实现 = 只把 `aria` 从 `FIXED` 删掉 ⇒ 他轨的「只改 README + CLAUDE.md」提交仍判 `own`, 仍漏。

**建议修法**: 把 `FIXED` 从「充分条件」降为「必要不充分」—— 一条提交判 `own` 需同时命中至少一条本轨强证据 (`openspec/changes/<SID>/`、本次 ab-results 目录、或本轨 handoff 的 `track-id`); 纯 `FIXED`-only 的提交一律判 `foreign` 请裁。本轨自己的发版同步面提交 (TASK-029) 也会是这一形态, 代价是它要被 owner 看一眼 —— 而它本来就在 owner_gates 第 9 项的授权面里, 多停一次远低于误推一次。

---

### M3 · `4013aad9` · major · issue · documentation · scope: `detailed-tasks.yaml metadata.baseline_rebase`

**一句话**: 基线复核面结构性地不含 `standards`, 而 Rule #6 的 SOT 在 A.2 之后已升到 1.1.0 并新增了一条 `rule6_note` 必填格式; 计划的 `rule6_note` 是散文, 五个字段一个都没有, 且 SOT 自己写明这五字段无机械 enforcement。

**证据 (实读 + 实跑)**:

- `detailed-tasks.yaml:78` 逐字: `standards: … conventions/skill-benchmark-exemption.md / conventions/version-management.md 对 proposal 定稿时的 gitlink 21748d4 零 diff; …`
- `detailed-tasks.yaml:995` (TASK-001 基线复核) 只跑三组: `metadata.baseline_rebase.aria_zero_diff` 的每个文件、`aria_shifted` 各条冒号前的文件、`main_repo` 的文件。`standards` 不在复核面内。
- 实跑 `git -C standards diff --stat 21748d4 940cb5b -- conventions/skill-benchmark-exemption.md` ⇒ `21 insertions(+), 3 deletions(-)`; 提交 `643bdf3` + `42261a1`, 经 `940cb5b` 合入 —— 是本容器 2026-09-17 合并 10CG/Aria#211 轨带进来的, 即**在 A.2 之后**。
- 该 diff 新增 `## 4.1 rule6_note 最小模板`, 五字段 `decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`, 并逐字写明「`description_changed: yes` 而 `scenario1` 或 `scenario4b` 为空、`not_required` 或 `n/a` ⇒ 不合规」。
- 计划的 `metadata.rule6_note` 是一整段散文 (档位标签 / 照跑面 / 三义务 / substitute 集 / description 零改动), 五个字段名一个都不出现。
- 同一 SOT `§6` 新增第三条局限, 逐字含「`rule6_note` 五字段无机械 enforcement」。

我另核了两处没坏的, 以免把范围说大: 该 SOT `§2` 判据表四行本体 (`:28-31`) 在这次 diff 中未改 ⇒ 计划「档位标签 = 判据表第三行」仍成立; `conventions/content-integrity.md` 在 `8b49562..940cb5b` 区间零 diff ⇒ TASK-026 与 `hard_constraints` 对 `§4.4 / §4.5` 的引用仍成立。

**失败场景**: 执行者照 TASK-001 复核基线, `standards` 不在清单里 ⇒ 不会发现 Rule #6 的 SOT 已换版本并多了必填格式; TASK-024 出结果、TASK-031 落笔时照现有散文 `rule6_note` 交付 ⇒ 产出物不符合 SOT 现行 `§4.1`。因为 SOT 自己说这五字段没有机械 enforcement, 没有任何检查会拦, 这条会一路 ship 到归档。Rule #6 是不可协商规则, 其 SOT 规定的 `rule6_note` 格式属必做项, 不是风格建议。

**建议修法**: (1) TASK-001 的基线复核清单补上 `standards` 的五个被引文件, 做法与 aria / 主仓一致 (逐文件 `git -C standards diff --shortstat 21748d4 <B.1 实测 gitlink> -- <文件>`, 有 diff 即实读被引处并记偏移表); (2) `metadata.rule6_note` 追加 SOT `§4.1` 的五字段, 本 cycle 预期取值: `description_changed: no` (TASK-015 / 016 / 017 的 frontmatter sha256 相等断言已守住)、`scenario1: <本次 ab-results 目录>` (TASK-024 回填)、`scenario4b: not_required`、`negctrl: n/a`; `decision_table_row` 需要额外处理 —— SOT 的字段只收单值或 `n/a`, 而本 spec 按裁定 5 走第二行与第三行的**并集**, 建议在字段旁显式注明并集口径, 并把「SOT 的单值字段表达不了并集档」写进 TASK-031 的第 6 张 issue 反馈给 SOT。

---

### m1 · `0c14e6bd` · minor · issue · documentation · scope: `detailed-tasks.yaml TASK-030`

TASK-030 记「A.2 实测 `aria-orchestrator` 为 detached 的 `237045a`」; 现测 `git -C aria-orchestrator rev-parse --abbrev-ref HEAD` = `master`, 且 `HEAD` = `master` = `237045a`, reflog 顶条为 `checkout: moving from feature/m6-dispatch-input-delivery to master`。该任务的断言是「本地 master 等于 HEAD 等于 origin/master 等于 github/master」, detached 与否都成立 ⇒ 不改执行者动作, 只是这条实测记录已过期。B.1 复核时顺手更新即可。

### m2 · `2a3c18f4` · minor · issue · documentation · scope: `detailed-tasks.yaml metadata`

被审对象是 v2.1, 版本标识三处仍写 v2: `detailed-tasks.yaml:1` 头注释「v2 (2026-09-17, post_planning R1 rework)」、`:6` `title: … (A.2 / A.3 v2)`、`:11` `updated: '2026-09-17'`; `tasks.md:6` 的 Status 行同样是「A.2/A.3 v2 … — 待 post_planning R2」。不改执行者动作。R1 的 m20 判过同型 (头注释与 title 仍写 v1) 并「接受」。**可被驳回的理由**: v2.1 只动证据层、计划内容未变, 不 bump 标识是有意的。若主控采纳该驳回, 建议把「版本标识只随计划内容变更 bump」一句写进 `metadata.revision_log`, 免得每轮重报。

### m3 · `2cb26bed` · minor · issue · documentation · scope: `tasks.md 读前必看 4`

读前必看第 4 条写「并发轨 10CG/Aria#211 的 T4 也要把它升过 1.5.0 (其 proposal `:135` / `:146`), 被占即顺延」。实测: 10CG/Aria#211 已于 2026-09-17 随 PR `10CG/Aria#215` 合并 (`df3c274`), 而 `git diff --stat a563192 5d435e9` 的文件清单里**没有** `aria-plugin-benchmarks/ab-suite/version.yaml`, 现值仍 `version: "1.5.0"` (`changelog` 顶条仍是 2026-09-05 那条)。即该轨最终没有占号, 1.6.0 现在是空的。不改执行者动作 (TASK-023 的规则是「读 `origin/master` 现值的下一个 MINOR」, 与占不占号无关), 建议 B.1 复核时把这句括注更新为事实, 省掉一次「在飞轨看不见」的推理。

## 对执笔人自报薄弱点的表态

**(a) `stage_cells` 39 格「在 P6 之前以终局结束」按求值总序推出、实现前无法验证 —— 可接受。** 我按 proposal 原文逐条回读了风险最高的一批格 (SC-15 的 (2)(3)(4)(5)(6)(7)(8)(9)、SC-7 的 (b)(e)、SC-9 的 (2)(3)(4)、SC-20(3)、SC-5(8)、SC-17 的 (4)(5)(7)、SC-22(3)), 全部能在 P0–P5 内以 error / bypassed / 格 A–E 终局, 或只依赖参数与常量。最能证明切分是按**终局态**而不是按 SC 编号做的是 SC-15(5): 它的主断言 (三对或四对 `missing` + `verdict=fail` + exit 1) 需要走完 P6, 因此**没有**被放进 TASK-010, 放进去的是同一条第二条反事实的 `typo-mode` 格 (在 P4 的优先级链上以 `config_unreadable` exit 2 终局)。另外 `metadata.v2_state_runs` 的 C1 三态已覆盖 not-run / 执行两次 / 格名改动三种假绿形态。残余风险只是格名与测试写法耦合 (改名显示 not-run 判红), 方向保守, 接受。

**(b) 两个检查偏严、方向是 fail-closed —— 一半可接受, 一半不成立。** `coord_ref_precheck` 偏严 (心跳 commit 格式变、同容器同轨多 claim 文件、会话收尾改 `docs/handoff/latest.md` 都停下请裁) 我接受, 它确实是 fail-closed。但把 `commit_attribution` 一并描述成「偏严」不成立: 它在本仓最高频的那一类他轨提交 (发版同步面 / 纯 gitlink bump) 上**偏松**, 三例实测全判 `own` 并 exit 0 (M2)。自报的定性会让复核者以为这道闸的风险只在「误停」, 而实际风险在「漏放」, 方向相反。

**(c) 三态脚本第 99 行仍 `git fetch /home/dev/Aria` 取真仓协调 ref 作 base tree —— 可接受, 建议参数化。** 我实读 `metadata.v2_state_runs` 的 N6 块确认该 fetch 只把真仓协调 ref 读进临时裸仓 (`git init --bare` 后 fetch 到 `refs/aria/coordination`), 对真仓零写入; 执笔人也已证明对结论零影响 (空 ref 变体同输出), 且它只在证据层, 不进 Phase B 执行面。但它使「席位在别的机器复跑这份证据」不成立, 而 v2.1 返修的起因恰恰就是「换容器复跑不一致」—— 同类环境耦合就剩这一处。建议取 argv 或环境变量, 缺省回落到空 ref 变体。不计 finding。

**(d) `own_claim_files` 描述生产用法、与 fixture 自造 claim 并列可能被读成矛盾 —— 不可接受。** 但问题不在自报的那个层次 (读起来像矛盾)。那段生产用法本身现在就是错的: 它钉的 `claims/023236f2/s-86f7@1836.yaml` 现为 `yielded`, 而持 active claim 的是执行容器 `bfe8285d` (M1)。自报把它归为措辞问题, 实际是执行面缺陷 —— 这恰好是 v2.1 返修在 fixture 层修掉、却没有在参数层扫到的同一处耦合。

## 风险 / 疑问 (不计入 finding)

1. **本轨的 active claim 属执行本轮审计的这个容器** (`claims/bfe8285d/s-73b9@1606.yaml`, heartbeat `2026-09-18T16:23:55Z`)。同时 `docs/handoff/latest.md` 把 10CG/Aria#195 标为「yielded, 待双子星认领, B.1 待起」。TASK-001 的入口前置 (owner_gates 第 1 项) 是「10CG/Aria#195 已完成 C.2 合并或 owner 明示改序」—— 按计划字面, 即使本轮 R2 通过, 下一步大概率仍是 owner 门而不是 Phase B。这不是计划缺陷 (它就是这么设计的等待点), 只是提醒复核者别把「审计收敛」读成「可以开工」。
2. **Phase B 预估 97–143h 跨多会话, 但计划只写了周期 handoff (TASK-031), 没写会话收尾 handoff** (Rule #9 的另一个正交入口)。每次会话收尾都要改 `docs/handoff/latest.md`, 而 `commit_attribution` 对该文件一律判 `foreign` ⇒ 每个会话边界都会命中 owner_gates 第 16 项。这是有意的 fail-closed, 但频次是「每会话一次」而非例外, 建议在 owner_gates 第 16 项旁注明这是预期路径, 免得第一次撞上被当成异常。
3. 我**没有**独立复跑 `metadata.a2_state_runs` 与 `metadata.v2_state_runs` (主控 C1 已做过逐字节核验与独立副本复跑, 本轮不重复烧), 对这两块的使用限于实读其嵌入代码与输出。
4. 我**未核** TASK-021 引用的 catalog 行号精度 (`test_pre_merge_gate.py:266` 等) 与 TASK-029 的 16 个版本点各自行号 —— 后者计划已写明「行号以执行时 grep 为准」。
5. 顺带核过、结论是**没问题**的几处, 记在这里免得下轮重复挖: `metadata.c25_five_questions` 五问逐条对源码属实 (`push_all_remotes.sh:49` 的 `PRE_LOCAL_HEAD=$(git rev-parse HEAD)` 与 `:119` 的成功判据、`DEFAULTS.json:6-15` 的 `fail_on_partial_push: true` 与本仓 `.aria/config.json` 无 `multi_remote` 段、`SKILL.md:613/:614/:638` 的枚举与 detached 处置); 主仓与三个子模块都只有 `origin` + `github` 两个 remote, C.2.5 的自动发现不会多推第三个; TASK-031 的归档门在 31 个 checkbox 全勾后实测 `complete=True`(`tasks.md 全 [x] (31 task(s), 无 carry-forward/defer 注释)`), 不会被 `_CARRY_FORWARD_RE` 卡住; 裁定 1 对 SC-15(5) 的期望值重算 (四个 checkpoint 减 `post_brainstorm` 得三个) 与 SC-15(3)(7)(9) / SC-20(7) 实算不变的判断, 对 proposal 原文核对无误。

## Verdict

**PASS_WITH_WARNINGS · 0C / 3M / 3m · Vote: REVISE**

## 是否足以开始 Phase B

**不足以** —— 三条 Major 都落在 B.1 入口与发布段的闸门上: M1 不修, 执行者在 TASK-001 第一步就没有合法下一步 (或让协调 ref 前置检查在首次心跳后恒红); M2 不修, 本仓最高频的他轨提交形态会绕过刚为它建起来的那道闸, 最坏是把他轨未推送的 gitlink bump 推上两端; M3 不修, Rule #6 的交付物会以不合 SOT 现行格式的形态 ship 且无任何机械检查会拦。三条都是定点修订, 不涉及任务结构重排或 proposal 设计取舍, 改完可直接进 R3 复核。
