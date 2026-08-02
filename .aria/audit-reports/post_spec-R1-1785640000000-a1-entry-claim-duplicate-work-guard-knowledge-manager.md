# post_spec R1 — knowledge-manager

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=0 major=2 minor=2

## 指针核实表

| 声称 | 位置 | 实测命令 | 结果 | 判定 |
|------|------|---------|------|------|
| `phase-a-planner` 零调用 phase1_gate | proposal.md:70 | `grep -rn "phase1_gate" aria/skills/phase-a-planner/` | exit 1, 无输出 | ✅ 属实 |
| `phase-b-developer` :88-93 = `--phase B` + `[--linked-issue]`(可选) | proposal.md:71 | `grep -n "phase1_gate\|--phase B\|linked-issue" aria/skills/phase-b-developer/SKILL.md` | 命中行 88/91/92/93, 92行`--phase B`, 93行`[--linked-issue ...]` | ✅ 属实, 行号精确 |
| `branch-manager` :149 = `--phase B --mode advisory` | proposal.md:72 | `grep -n "phase1_gate\|--phase B" aria/skills/branch-manager/SKILL.md` | 149行原文即 `` `phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory` `` | ✅ 属实, 行号精确 |
| `--linked-issue` help 原文「同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)」 | proposal.md:64 | Read `phase1_gate.py:1198-1204` | help 全文: "可选语义重叠信号 (Part B1, 如 '10CG/Aria#160'): 写入 claim 并检测 同 linked_issue 不同 track-id 的 active claim (advisory 告警, 不阻断)" | ✅ 逐字匹配 |
| `--phase` 无 `choices` 约束 (D6 承重前提) | proposal.md:95,126 | Read `phase1_gate.py:1189-1191` | `parser.add_argument("--phase", required=True, help=...)` 无 choices; 对照 `--mode` 同段落有 `choices=["advisory","block"]` | ✅ 属实, 且有鲜明代码内对照 |
| dogfood `outcome=passed`/`push_success=true`/`linked_issue_overlap=[]` (aria-plugin#124) | proposal.md:15-28, D6/D7 | `grep -rn "aria-plugin-124-path-coverage-z-flag" .aria/` + `git show <coordination-ref-sha>:claims/023236f2/s-b291@1154.yaml` | telemetry: `{"ts":"2026-08-02T11:54:59Z","source":"production","outcome":"passed","track_id":"aria-plugin-124-path-coverage-z-flag","claim_written":true}`; claim yaml 含 `phase: A.1`, `linked_issue: aria-plugin#124`, `status: active`; 本地 ref 与 `origin` ls-remote 一致(474cb12...) | ✅ 属实, 证据比声称更扎实(claim yaml 直接给出 `phase: A.1` 字段) — 见 MINOR-2 |
| memory `feedback_concurrent_duplicate_audit_fetch_before_start` 存在 + 内容匹配 | proposal.md:36 | Read `/home/dev/.claude/projects/-home-dev-Aria/memory/feedback_concurrent_duplicate_audit_fetch_before_start.md` | 文件存在, 含 "#133" (2026-05-31) 与 "2026-07-11 实证(secret-guard, 一个 session 内三重复现)" 两段 | ✅ 属实, 但见 MINOR-1(计数口径) |
| memory `feedback_verify_predicate_inputs_exist` 存在 + 语义匹配 | proposal.md:58 | Read `/home/dev/.claude/projects/-home-dev-Aria/memory/feedback_verify_predicate_inputs_exist.md` | 核心论点"审计判定机制必须分两层: 逻辑对吗 + 它要判的输入真的会被生成吗"逐字对应 Spec 引用 | ✅ 属实 |
| `audit-engine` 目前零 `scripts/` 目录 | proposal.md:103 | `find aria/skills/audit-engine -maxdepth 2 -type d` | 仅 `references/`, 无 `scripts/` | ✅ 属实 |
| 反事实: `linked_issue_overlaps` 会检测跨2天/跨track_id的同issue active claim | proposal.md:76 | Read `aria/skills/state-scanner/lib/collision.py::linked_issue_overlaps()` | 逻辑确认: 遍历 claims, 排除 terminal 状态 + 排除同 track_id, 仅按 `linked_issue` 精确匹配即命中, 与 claim 写入时间无关 | ✅ 反事实推理成立 |
| L handoff §6 把认领列为"未来 Phase B 步骤" | proposal.md:74 | Read `docs/handoff/2026-07-27-issue122-phase-a-dual-gate-convergence.md` §6 | 原文: "**Phase B 起手**...( b) 经 phase1_gate 认领 (`--linked-issue aria-plugin#122`, collision.kind=self_multi_container)" | ✅ 逐字匹配 |
| §Why 症状表 L/R 轮数/agent数 (10轮/33实例, 4轮/13实例) | proposal.md:32-34 | Read 同上 handoff line 12,17,31 | L: "10 轮 / 33 个 agent 实例" 匹配; R: `post_spec R1→R4 (5/5/2/1 席)` = 5+5+2+1=13, 4轮, 精确匹配 | ✅ 属实 |
| `.aria/config.json` `audit.checkpoints.post_spec` enabled=convergence | proposal.md:171 | `grep -n -B3 -A3 '"post_spec"' .aria/config.json` | `"post_spec": "convergence"` | ✅ 属实 |
| phase1_gate.py 不读取 config (skip_if 判断只在调用方) | (核实第8条文档同步面用) | `grep -n "config" aria/skills/state-scanner/scripts/phase1_gate.py` | 仅 docstring 注释提及一次 "matches config default", 无任何实际 `.aria/config.json` 读取逻辑 | ✅ 确认 — 支撑 MAJOR-2 |

## Findings

### [MAJOR] layer-l-integration.md 文档同步缺口未纳入 §Impact 表
- **位置**: `aria/skills/state-scanner/references/layer-l-integration.md:4,15,38-48` vs `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` §Impact (158-165)
- **问题**: 这份"活参考文档"当下时态明确断言「**Design A 条件触发**: 闸门仅在用户确认要进入 Phase B 时调用, **不在 scan.py 内自动执行**」(line 15), 第4行同样写"CLI 调用, 非 scan.py 自动执行", 第38-48行调用关系表写死 `acquire_claim | phase1_gate | Phase B 启动前`。本 Spec 实施后 phase1_gate 会在 A.1 也被调用, 这些断言将变为过时且错误的陈述。proposal.md 的 §Impact 表(仅列 phase-a-planner/SKILL.md + audit-engine/SKILL.md + 两个新脚本/测试)完全没有列出这份文件。
- **证据**: `Read aria/skills/state-scanner/references/layer-l-integration.md` 全文; `grep -c "layer-l-integration" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` → 0 命中。
- **建议修法**: 把 `layer-l-integration.md` 加入 §Impact 表, 同步更新: (a)「何时触发 phase1_gate」一节新增 A.1 触发条件; (b) `acquire_claim` 调用关系表补 A.1 行; (c) 顶部状态说明纳入本 Spec 的扩展范围。此文档正是本 Spec 自己在 §Why 反复强调的"文档过时=AI误解"活教材, 遗漏它会讽刺地重演本 Spec 要根治的那类问题。

### [MAJOR] A.1 新调用点未声明与 Phase B 对称的 skip_if 条件
- **位置**: proposal.md §1 (82-97) vs `aria/skills/phase-b-developer/SKILL.md:96-100` / `aria/skills/branch-manager/SKILL.md:150-153`
- **问题**: 已核实 `phase1_gate.py` 本身不读取任何 config —— `coordination.enabled` 的判断完全在调用方(SKILL.md 指令文本层, 由 AI 编排时人工检查)。`phase-b-developer` 和 `branch-manager` 现有的 Phase B 认领步骤都明确写了 skip_if 条件(`coordination.enabled` 显式 false / 非 git repo 或无 origin remote), 但 proposal.md §1「A.1 入口认领」完全未提及这组条件是否/如何延伸到新的 A.1 调用点。
- **证据**: `grep -n "config" aria/skills/state-scanner/scripts/phase1_gate.py` → 仅 1 处 docstring 注释, 无实际读取逻辑; `sed -n '96,100p' aria/skills/phase-b-developer/SKILL.md` 显示既有 `skip_if` 段落, proposal.md §1 无对应段落。
- **建议修法**: 在 §1 补充与 Phase B 对称的 skip_if 条件, 并在 SC 表补一条覆盖该 skip 分支的验收标准。若不补, 按字面实现会导致 `coordination.enabled=false` (opt-out) 的第三方项目在 A.1 阶段仍被写 claim + push 到远端 coordination ref, 与项目的显式 opt-out 意图相悖(advisory 模式下不阻断流程, 但产生不受欢迎的副作用)。

### [MINOR] 历史实证次数计数口径不一致
- **位置**: proposal.md:36
- **问题**: Spec 称 #122 事故为「memory ... 的**第四次实证** (前三次: #133 / 2026-07-11 secret-guard 一 session 三重复现)」。memory 原文明确用"三重复现"描述 07-11 事件(session 内三个子复现: 整条冗余/R2基于失效前提/差分对陈旧版本做)。若按字面计数, #133(1)+secret-guard(3)=4, 与"前三次"矛盾; 若 secret-guard 算1个事件则=2, 同样不等于"三次"。("第四次"这个整体判断本身在 `docs/handoff/2026-07-27-issue122-phase-a-dual-gate-convergence.md` line 37 有独立且逐字吻合的佐证, 只是"前三次"的分项列举在数字上未对齐。)
- **证据**: Read `feedback_concurrent_duplicate_audit_fetch_before_start.md` line 10("2026-05-31 实证 #133") + line 21("2026-07-11 实证...一个 session 内三重复现")。
- **建议修法**: 明确 secret-guard 的"三重复现"在此处计为1个历史列举项(与#133并列共2项, 不称"三次"), 或改用不依赖精确计数的表述(如"此前多次"), 与 line 15 "第五次"的计数口径统一。

### [MINOR] coordination ref 在 origin/github 两个远端不同步(顺带发现, 非本 Spec 引入)
- **位置**: `refs/aria/coordination` (跨 remote)
- **问题**: dogfood claim 记录已确认成功推送到 `origin`(本地 ref `474cb123879c1189394b124b1dc5f75eca1ffae2` 与 `git ls-remote origin refs/aria/coordination` 一致), 但 `git ls-remote github refs/aria/coordination` 返回不同的 SHA `ad0287f759c23f9ee85d02fe0b47842eb5f71103`, 落后于 origin。根源是 `phase1_gate.py` 的 `resilient_push` 默认且仅 push `remote="origin"`, 不做多remote镜像 —— 这是已 ship 机制(coordination-claim-lifecycle-and-overlap)的既有行为, 不是本 Spec 引入的新问题。
- **证据**: `git ls-remote origin refs/aria/coordination` → `474cb12...`; `git ls-remote github refs/aria/coordination` → `ad0287f...`(不同)。
- **建议修法**: 非本 Spec 应处理范围。dogfood `push_success=true` 声称对 `origin` 而言完全成立(已证实), 此发现不影响本 Spec 结论。若 owner 认为"只 fetch github 的消费方会看不到 claim"值得关注, 可另开 issue 跟进, 不阻塞本 Spec。

---

## 附注 — 未发现的问题(核实通过, 无需在 findings 中重复)

- Rule #6 `rule6_note` 判断合理: SKILL.md 指令文本变动(处方性·运行时指令面)照跑 AB, 新增 `sibling_spec_probe.py`(确定性代码)用结构化测试替代, 两者判据边界清晰, 符合 CLAUDE.md 判据表第二行。
- D5「不做中心化 spec 登记表」危害描述("彻底消除需中心化登记表")与建议修法(不做, 理由 owner 未授权+性价比不成立)方向一致。
- `#133` 确认对应 `openspec/archive/2026-05-31-concurrent-session-upm-safety`(目录存在, 日期吻合)。
- 末尾「闸门待裁」部分对 `.aria/config.json` 配置现状的引用准确。
