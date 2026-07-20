# Proposal: state-scanner-gate-yaml-datasource (aria-plugin #113)

> **Status**: ✅ **Approved** (owner sign-off 2026-07-19) — post_spec R1→R5 CONVERGED (PASS, owner 裁决延长 R5) + A.2/A.3 done (detailed-tasks.yaml 10 tasks, path B) + post_planning R1→R2 CONVERGED (PASS; R1 6 Major 簇均属 A.2/A.3 派生盲区 — 规则 #10 照跑首战抓实); ready for Phase B.1 (claim `aria-plugin-113-gate-result-yaml-20260719` active)
> **Created**: 2026-07-19
> **Spec Level**: 2 (Minimal — 单域 [detailed-tasks.yaml 数据源接入], 三消费点同根同修; blast radius 限 yaml-only spec 类, dual-layer 类 byte-identical)
> **关联 Issue**: [10CG/aria-plugin #113](https://forgejo.10cg.pub/10CG/aria-plugin/issues/113) (open; triage verdict=`confirmed`/`major`/`next-cycle`, 3/3 复现, [issuecomment-16285](https://forgejo.10cg.pub/10CG/aria-plugin/issues/113#issuecomment-16285))
> **上游**: `state-scanner-openspec-collector-false-green` (#166 缺陷2, shipped v1.61.0, 已归档) §非目标明示的 follow-up — 本 change 以精确 per-spec verdict **取代**其 blanket unverified 兜底
> **ship target**: aria-plugin v1.63.0 (MINOR; 当前 SOT plugin.json = v1.62.0; 本 cycle 已 claim track `aria-plugin-113-gate-result-yaml-20260719`)
> **代码落点**: `aria/` 子模块; Spec 落主仓 `openspec/changes/` (meta-repo 惯例)
> **审计轨迹 (post_spec, convergence)**: R1 5-agent [5/5 PASS_WITH_WARNINGS / REVISE / SCOPE_OK] → 0 Critical + 8 Major 簇 + 11 Minor → R1-fix 全量吸收 → R2 5-agent [5/5 PASS_WITH_WARNINGS, 5/5 SCOPE_OK; R1 全闭合] → 新 3 Major 簇 (P probe fold 撞 v1.54.0 designed 三件套 [4/5 命中] / Q 属实性轴静默降格 / R parser 规格三缺口) + 8 Minor → R2-fix 全量吸收 (决策 9 重写 + 15-18 新增) → **R3 3-agent [tech-lead PASS + qa PASS + backend REVISE; 簇 P 6/6 闭合 + 簇 Q 自洽性确认 + 簇 R (a)(b) 闭合]** → 1 Major (簇 R-c 收敛延伸: SC-3e 计数缺 indent-anchored 算法, 朴素读法 17/17 语料恒 mismatch) + 2 Minor (golden 集成 title 4→3 双 agent 勘正 / status 滤波非对称观察) → R3-fix 吸收 → **R4 3-agent [code-reviewer PASS (算法 17 语料实跑零误伤) + knowledge-manager PASS (1 机械 Minor: Step2 命名 ×5 顺改) + backend REVISE]** → 1 Major (F-R3 残留: 计数缺 tasks: 块**结束边界**锚定 — 0 缩进兄弟键同缩进项 11/17 误伤含 3/3 golden; cr 与 backend 按同一规格实现结果相反 = 欠定实证) → R4-fix 吸收 (计数范围 range-bounded + SC-3f 双反例) → max_rounds=4 耗尽, owner 裁决延长 → **R5 1-agent [backend (R4 REVISE 方) PASS: V2 算法独立复现 16/16 真实语料零误伤, R4 Major 闭合, 0 新 C/M] → CONVERGED (verdict=PASS)**。报告 `.aria/audit-reports/post_spec-R5-*-aggregated.md`。R5 非阻塞 Minor 已吸收: 计数误伤叙事数字以落地实测为准 (R5 独立口径 9/16); base indent 取**计数范围内**首个 `_TASK_ID_LINE_RE` 匹配 (非全文件, Phase B docstring 钉死)

---

## Why

v1.61.0 (#166 缺陷2) 让归档安全网对 `detailed-tasks.yaml`-only spec (task-planner path B 正常产出) 从「完全失明」变为「诚实的无法核验」: `gate_result()` 对该类 spec 一律 `verdict=warn` + blanket `unverified_claims` 条目 + 非 None `d_payload`。这是**有意留的债** (v1.61.0 proposal §非目标明示 follow-up): gate 的 **yaml-only 分支**只 `.is_file()` 探测、不打开 yaml (注: `spec_complete.py` 别处已按 `- id:` 边界解析该文件供 #95 符号提取用, 见决策 8 — 「从未打开」仅对 yaml-only 分支成立), 于是:

1. **真干净的 spec 也被 warn + 建 tracker** — 每次归档 yaml-only spec 都产生一条无信息量的 Forgejo tracker + warn_overlay frontmatter, blanket 噪声 (triage case-2: 全 done fixture 与有残留 fixture 输出逐字段相同);
2. **有残留的 spec tracker 无实际内容** — d_payload 只含 blanket 条目, 不列举残留任务 (triage case-1);
3. **同根第三处**: collector 快照侧 `carry_forward_inventory` 只读 `tasks.md` (`collectors/openspec.py:265-283`, `tasks_file = d / "tasks.md"` @ :266), yaml-only spec 的行内 `[TODO: ...]`/`[deferred: ...]` 标注贡献恒 0 — 展示侧假绿 (triage case-3: 正控组证明 regex 正常, 缺口在 collector 该路径不读 yaml)。

**Probe-first 实证 (2026-07-19; R1 补语料+生产者双侧, R2 精化措辞)**:

- **观测语料**: `openspec/` 下 17 份 detailed-tasks.yaml (16 archive + 1 changes; repo 另有 benchmarks fixture ×2 + standards 模板 ×1, 非生产语料排除)。**至少 16 份**遵循「顶层 `tasks:` 块 + `- id:` 条目」形状; 1 份 (`2026-02-07-superpowers-two-phase-review`) 是 markdown 围栏伪 yaml (无顶层 tasks: 键、零 status 行) — dual-layer 被 precedence 屏蔽, 且是 `parse_ok=False` 的**真实语料形状** (SC-3a 采用)。
- **生产者 schema SOT**: task-planner `DUAL_LAYER_SPEC.md:123` 文档化值域 `pending | in_progress | completed | blocked` — 观测语料中的 `done`/`deferred` 反而不在生产者文档 (漂移; 本 change 按语料+文档**并集**设计白名单语义)。
- **yaml-only spec 的 per-task `status` 是被维护的**: 3 个真实 yaml-only 归档 spec (`2026-05-29-aria-context-monitor` / `2026-05-30-ai-native-estimator` / `2026-05-30-emergency-hotfix-and-audit-file-scope`) 25/25 全 `done`。
- **dual-layer spec 的 yaml per-task status 不被维护** (`archive-gate-runtime-reality` 已 ship 但 yaml 25×`pending`; SC-4 fixture `dispatch-input-delivery` 30×`pending`) — gate 的 yaml 分支只在 tasks.md **缺失**时触发, 该类天然不喂新 parser; **precedence (tasks.md 在场则 yaml 不咨询) 三消费点一致**。
- **值域**: `pending` (221) / `done` (45) / `completed` (44) / `deferred` (1, 含尾注 `# not in current cycle`)。**CRLF (R2 措辞精化)**: 5 份语料带 CRLF, 其中 **4 份的 status 行带 `\r\n`** (第 5 份为零 status 行的伪 yaml); `completed` 全部 44 实例带尾部 `\r`。⚠️ **披露**: 全部 CRLF 实例来自 dual-layer 文件 (被 precedence 排除), yaml-only 子集零观测 — SC-11 是**防御性合成负控** (契约钉合成的合法应用), 非真实 bug 复现; 但项目 `shell-jq-crlf-hygiene` 规范证明 CR 是复发型风险类别, 防御必要。
- ⚠️ **issue 诉求中的 `deferred_out_of_scope` 字段在生产语料与双 SOT 文档中均不存在** — aspirational 引用; 本 change 按真实 schema 落地。
- **行号勘正**: `_build_d_payload` :1115; `gate_result` def :1272 (yaml-only 分支 :1298-1327); `is_spec_complete` :184-248 (tasks.md 分支 :207-238, 单信号态 :210-211); `_split_task_blocks` def :376; `_strip_inline_comment` def :95; collector carry_forward :265-283 (issue 引 :244 已漂移)。

---

## What Changes

**核心原则: 单一 parser SOT (物理归位) + fail-CLOSED 白名单 + 「干净」定义三消费点统一 + parse 失败退回 v1.61.0 诚实态 + 属实性轴不静默降格 (绝不因新解析引入新假绿)。**

### 1. 新增 `lib/detailed_tasks.py` — detailed-tasks.yaml 解析单一 SOT (含既有切片器物理归位)

stdlib-only 硬约束下不引入 PyYAML; 先例 `custom_checks.py:62` minimal parser + `carry_forward.py` 物理搬迁 (#134 A1.1b)。

**既有切片器归位 (R1 簇 A)**: `_TASK_ID_LINE_RE` (:293) + `_split_task_blocks` (:376) 物理搬入 `lib/detailed_tasks.py`, `spec_complete.py` re-import (carry_forward.py 先例同型; `_extract_yaml_key_list` :391 留原地消费搬迁后切片器)。搬迁纯机械, #95 行为由既有测试 + SC-9 + 边界一致性回归测试锁定。

**status 抽取层** (新增, 建立在切片器之上):
- 每任务块内取**行首锚定** `^[ \t]*status:` 的第一个匹配 (语料 footgun: 折叠块内嵌 `{status:insufficient}` 与散文 `status: unknown` 均被锚定排除)。
- **块边界二次后处理 (R2 簇 R-b 精化)**: 0 缩进顶层键截断是**新抽取层对 `_split_task_blocks` 返回文本的二次后处理, 不修改/不影响共享本体返回值** (共享 SOT 照旧延伸到 EOF, #95 消费方零变) — 仅对末块有意义 (非末块天然被下一 `- id:` 截断)。顶层键判定字符级规则: 行匹配 `^[A-Za-z_][A-Za-z0-9_-]*:` (0 缩进, 泛化 `frontmatter_block.py:81 _TOP_KEY_RE` 单键先例); 折叠标量 (`execution_order: >`) 在**键行本身**截断。SC-15 合成负控钉死。
- **归一化链 (R2 簇 R-a 顺序修正, 对齐先例真实执行序)**: 值 → 剥 `\r` → quote-aware 剥尾部 `# 注释` → **strip 空白** → **剥首尾引号** → `raw_status` (先例 `custom_checks.py:158` comment-strip 后立即 `.strip()`, `_coerce_scalar` :75 先 strip 再 :79 引号判断 — 引号检测必须发生在已 trim 串上, 否则 `status: "done"  # x` 因前导空格致引号不剥 → 误判残留)。剥注释**复用** `collectors/custom_checks.py::_strip_inline_comment` (quote-aware SOT; lib→collectors import 已有 `spec_complete.py:148` 先例; **不用** `frontmatter_block.py:90` 同名 naive 副本 — 无引号感知, 选错源击穿 SC-1/SC-14)。`title` 仅剥 `\r` + strip + 首尾引号, 不做注释剥离 (语料存在未引号含 `#` 的合法 title)。白名单比较用 `raw_status.lower()`。
- **done-family 白名单 fail-CLOSED**: `{"done", "completed"}`。其余一切值 (语料实存 `pending`/`deferred`、文档声明 `in_progress`/`blocked`、未知新值) 一律算残留。不复用 `_normalize_status`: (a) 它是 token/substring 匹配, 对含 token `complete` 的叙事串 (metadata.status 形态 "A.3 complete — ...") 会误判 done, exact-match 免疫; (b) 裸 `complete` 分歧点白名单取残留 (fail-CLOSED)。
- **返回契约**: `{"parse_ok": bool, "tasks": [{"id": str|None, "raw_status": str|None, "title": str}...], "reason": str}`。**parse_ok=False 文件级四态**: 不可读 / 无顶层 `tasks:` 块 / 零 `- id:` 条目 / **结构自洽失败** (R2 簇 R-c: 隐形条目「既不完成也不残留」= 理论新假绿; 计数自洽即主 spec AC-5「检测集=裁决集」先例纪律; 不一致 → 结构可疑 → 退 case-3 blanket, SC-3e)。**计数算法 (R3 补规格 + R4 backend 补结束边界, indent-anchored + range-bounded)**: **计数范围** := 从顶层 `tasks:` 行的下一行起, 到**下一个 0 缩进顶层键行** (复用本节顶层键字符级规则 `^[A-Za-z_][A-Za-z0-9_-]*:`) **或 EOF (取更近者)** — 该边界在计数前统一计算, **不依赖** `_split_task_blocks` 「末块延伸到 EOF」的本体现状 (R4 实证: 不裁剪则 `execution_order:`/`execution_groups:`/`execution_dag:`/`agent_allocation:` 等 0 缩进兄弟键内部的**同缩进** `- ` 项混入计数 → 11/17 语料假触发含 3/3 golden [16/9、14/8、13/8] — 与 R3-fix 中 4→3 勘正同款的 execution_order 污染坑, 教训须对称应用)。base indent := 首个 `_TASK_ID_LINE_RE` 匹配的捕获组 `([ \t]*)` 逐字节串; 范围内**只数**匹配 `^<base_indent>-\s` 的行 (tasks: 序列**直接子项**); 更深缩进嵌套 `- ` 项 (deliverables/verification 子列表, 语料 17/17 存在, golden 全文比值 63/9、48/8、38/8) **不计入** (SC-3f 双反例负控钉死)。同缩进技术先例: `_extract_yaml_key_list` :405-419 indent-tracking。**条目级缺陷不整文件失败**: 缺 `status` 键**或值为空/纯引号空** (对齐 `custom_checks` `if rest else None` 惯例, 空串归一为 None) → 计残留 (reason `status-missing`); 缺 `id` → `id=None` 透传。永不 raise。

### 2. `gate_result()` yaml-only 分支: blanket → 精确 (取代 v1.61.0 兜底)

`:1298-1327` yaml-only 分支 (tasks.md 缺失 ∧ detailed-tasks.yaml 存在) 改为三态。**残留集 (与 §3/§4 统一)**: `{status 非白名单条目} ∪ {yaml 原始文本的 _CARRY_FORWARD_RE 标注}` — 完整镜像 `_extract_deferred_or_unchecked_items` :1102-1112 两半; 「真干净 (残留轴)」= 全白名单 ∧ 零标注。

1. **parse_ok ∧ 有残留**: `deferred_items` = status 残留 `{"parent_id": <id|None>, "line": "<id>: <title> [status=<raw_status|missing>]", "reason": "status=<raw_status>" 或 "status-missing"}` + 标注残留 `{"parent_id": None, "line": "<annotation>", "reason": "carry-forward annotation"}` (`_build_d_payload` :1133-1136 消费契约零改) → d_payload 列举真实残留; 不追 blanket 条目; verdict 不因残留升 warn (对称 tasks.md 路径 :1471→:1477)。
2. **parse_ok ∧ 残留轴干净**: 无 deferred_items、无 blanket 条目; 是否 full-pass 取决于属实性轴 (下段)。
3. **parse 失败**: 退回 v1.61.0 行为 — `{"claim": "archive-safety-net-source-unparseable", "reason": "detailed-tasks.yaml 存在但解析失败 (<reason>) — 完成声称无法核验; 需人工复核", "symbols": []}` + `verdict=warn` + 非 None d_payload + soft_error。串字面量文档化于 `spec_complete.py` 分支相邻注释 (决策 11)。

**属实性轴: scoped 披露, 不静默降格 (R2 簇 Q, 决策 15; R3 精化)**: v1.61.0 blanket 同时覆盖「残留不可见」与「声称无法核验」两轴; #95 C-gate 的 symbol-liveness (:1341-1410) 与 `_check_artifact_claims` (:1412-1425) 均吃 `tasks_text`, **对 yaml-only 分支不适用** (显式声明, R2 backend F8)。三态设计若只取代残留轴, 「yaml title 声称集成工作但代码 dead-on-arrival」的 spec 会从诚实 warn 静默变 pass (golden 语料实测 **3 条**集成类 title — per-fixture: context-monitor 2 / ai-native-estimator 1 / emergency-hotfix 0, R3 qa/tech-lead 双实测勘正 [原「4」系未限定 title 字段的裸扫混入 execution_order 注释假命中], 非假设)。**修复 (精确披露, 非 blanket)**: parse_ok ∧ ≥1 个 **done-family** task 的 `title` 命中 `_line_has_integration_keyword` → 追**一条 scoped** unverified 条目 `{"claim": "archive-safety-net-integration-claims-unverified", "reason": "detailed-tasks.yaml 含 <n> 条已完成集成类 task title (<列举>) — yaml 数据源暂无 symbol-liveness 核验; 需人工复核", "symbols": []}` + verdict=warn — 仅对**声称了已完成集成工作**的 spec 发。**status 滤波 (R3 tech-lead 观察采纳)**: 只看 done-family 任务的 title, 与 tasks.md 路径 :1342 `it["checked"]` 滤波语义对称 — 非 done 的集成任务是「未完成」不是「无法核验的完成声称」, 已由残留轴列举, 不双报。**full-pass = 残留轴干净 ∧ 零 done-family 集成类 title**。完整 C-gate parity (合成 claim 喂 `extract_claim_symbols` — 它已解析 yaml deliverables :476-488, 扩展自然) 留显式 follow-up (Phase D 开 issue, cross-link 本 spec)。

**runtime_probe fold 可达性 (R2 簇 P, 决策 9 重写)**: 重构**仅覆盖 yaml-present 臂** — yaml-only 分支三态判定后 fall through 到 probe fold (:1427-1467), d_payload 组装移到 fold 之后 (镜像 tasks.md 路径 :1429→:1477 顺序; `project_root` 在该臂内计算); **proposal-only (两文件皆无) 与 tasks.md-unreadable (:1329-1333) 两子类维持 designed 早退不变**。`:1430-1431` 注释同步改写为「独立于 tasks.md 早退路径的 **yaml-only** 分支亦达 fold; 两文件皆缺的 proposal-only spec 仍零评估」。**本项有意反转** `runtime-probe-archive-gate-integration` (shipped v1.54.0, DEC-20260705-001) §What Changes ③ R3 裁决在 **yaml-only 子类**上的适用 — 原裁决前提「spec 结构性不完整时探针无意义」随本 change 的精确解析失效 (yaml-only 不再结构性不完整); proposal-only/unreadable 子类前提仍成立, 维持原裁决。配套文档/测试 docstring 双改入 Impact; SC-12 (可达) + SC-13 (边界负控) 双向钉死。

### 3. `is_spec_complete()` yaml tasks-branch (同根第三轴, 对称扩展)

`:210-211` 单信号态, 在 tasks.md 缺失 ∧ yaml 存在 ∧ parse_ok 时插入 yaml tasks-branch (OR 左半, 对称 :207-238):

- 全白名单 ∧ 零标注 → `complete=True`, reason `"detailed-tasks.yaml 全 done (<N> task(s), 无 carry-forward/defer 注释)"` (「干净」与 §2 残留轴同一定义; complete 轴不看集成 title — 它载完成态, 属实性由 verdict/unverified 载, 正交);
- 有残留 → `tasks_reason = "detailed-tasks.yaml has <k>/<N> non-done task(s)"` (标注计入 k), fall through 到 Status 分支 (OR 右半不变);
- parse 失败 → `tasks_reason` 记失败, fall through (等价现状)。

**同步 `:12-16` 模块 docstring** — :12-13 形式化定义三支化 **及 :15-16 prose bullet**「tasks.md absent → verdict 仅由 Status 归一化决定」(R2 tech-lead: 同样漂移) 一并改写。

**下游效应**: `design_deferred` (`openspec.py:248-255`) 对 yaml-全-done spec 不再误入; 方向只减噪。

### 4. collector `carry_forward_inventory` yaml fallback (issue 诉求 3)

`collectors/openspec.py:265-283`: tasks.md 缺失时 fallback 读 yaml **原始文本**过 `_extract_carry_forward_annotations` (regex SOT 零改)。precedence 与 gate 一致 (tasks.md 在场不扫, 含 present-but-unreadable 时 :272 `continue` 不落 fallback — R2 tech-lead 核验)。

---

## Success Criteria (可证伪; 每条配 baseline-failing 测试)

| SC | 验收 (二值 metric) | Baseline |
|----|---------|--------|
| **SC-1** | yaml-only fixture (1 `pending` + 1 `deferred  # 尾注`, 零集成 title) → `d_payload.deferred_items` 恰 2 项, 第 2 项 `reason == "status=deferred"` ∧ `line == "<id>: <title> [status=deferred]"`, 无 blanket 条目, verdict=pass | 当前: blanket claim + deferred_items=[] |
| **SC-2** | yaml-only fixture 全 done/completed ∧ 零标注 ∧ **零集成类 title** → `verdict=pass` ∧ `unverified_claims=[]` ∧ `d_payload=None` (full-pass) | 当前: blanket warn (triage case-2) |
| **SC-2b** (属实性 scoped, R2 簇 Q; R3 加 status 滤波) | yaml-only 全 done ∧ ≥1 **done-family** 集成类 title → **恰一条** `archive-safety-net-integration-claims-unverified` 条目 (reason 列举命中 title) + verdict=warn + 非 None d_payload; **无** blanket 条目; 负控: 集成 title 挂在 pending 任务上 → **不**发 scoped 条目 (归残留轴, 不双报) | 当前: blanket warn (无差别); 若无此 SC 则新设计沉默 pass (属实性轴降格) |
| **SC-3a/b/c/d** | 文件级: (a) markdown 围栏伪 yaml (真实语料形状) / (b) 无顶层 `tasks:` / (c) 零 `- id:` 条目 → 各自 warn + `-unparseable` + 非 None d_payload + soft_error。(d) 条目级: 缺 `status` 键**或空值/纯引号空** → 计残留 `status-missing`; 缺 `id` → parent_id=None 透传 | 护栏 |
| **SC-3e** (计数自洽, R2 簇 R-c; R3 补算法) | `tasks:` 块内 **base-indent 直接子项** `- ` 行数 ≠ `_TASK_ID_LINE_RE` 匹配数 (如 `- \n  id:` 分行 / id 非首字段条目) → parse_ok=False → case-3 blanket (隐形条目不静默消失) | 护栏: 无此项则隐形条目 = 理论新假绿 |
| **SC-3f** (计数负控**双反例**, R3+R4) | (i) 深缩进嵌套 `- ` 子列表 (deliverables/verification) 不计入; (ii) **`tasks:` 之后的 0 缩进兄弟顶层键 (`execution_order:` 等) 内部的同缩进 `- ` 项不计入** (计数范围止于该键行) — 两反例下 parse_ok=True 正常三态; fixture 用真实 golden 形状 (3 份皆含 execution_order:, 无边界裁剪时 baseline-failing: 16/9、14/8、13/8 假 mismatch) | 护栏: 朴素读法两个方向各自恒 mismatch 退 blanket → 全语料失活 |
| **SC-4** | dual-layer (真实 fixture `dispatch-input-delivery` 形态) → tasks.md 路径, yaml status 不被读取, 输出与 v1.62.0 byte-identical | 保护性 |
| **SC-5** | `blocked`/`in_progress` (生产者文档声明、语料未观测) 及未知新值 → 计残留 | 护栏 |
| **SC-6** | yaml-only 全 done 零标注 → `complete=True`; 有残留 ∧ Status≠done → False; 有残留 ∧ Status=done → True (OR 右半) | 当前: 恒单信号 (实测 3/3 False) |
| **SC-7** | yaml-only 含 `[TODO: ...]` → inventory 命中; dual-layer 同标注 → 不计 | 当前: 恒 0 |
| **SC-8** | 3 golden 真语料: 全部达「残留轴干净」(无 deferred_items / 无 blanket 条目 / complete=True); 其中含 done-family 集成类 title 者 (实测 **3 条**: context-monitor 2 / ai-native-estimator 1) 额外带 SC-2b scoped 条目 (RED baseline 钉精确 per-fixture 预期), `emergency-hotfix` (0 条) 预期 full-pass | 当前: 3/3 blanket warn |
| **SC-9** | 既有基线 1248 中, 除 `test_gate_yaml_only_source.py::test_yaml_only_warns_and_builds_payload` (改写) 外全绿 (`test_both_sources_no_false_warn` 保留); **`TestRuntimeProbeFoldL2ProposalOnlyEvaporates` 保绿为未触碰护栏** (仅 docstring 泛化措辞收窄, R2 簇 P); #95 符号提取测试经搬迁零行为变化 + 边界一致性回归测试; 最终 before→after 计数 Phase B 落地时记账 | R2: 无此注则宽读重构致字面不可满足 |
| **SC-10** | 合成 yaml-only fixture 项目端到端 scan.py + `--gate` CLI; 自反性检查点: 本 spec 归档时核对 gate 实际输出 (预期: path B 产出后按其 title 是否含集成关键词落 SC-2 或 SC-2b 态) | — |
| **SC-11** (CRLF) | `status: done\r\n`/`completed\r\n`/`pending\r\n` → 与无 CRLF 判定一致, id/title 无 `\r` 残留 (防御性合成负控 — 语料 CRLF 全在 dual-layer, 见 §Why 披露) | 护栏 |
| **SC-12** (probe 可达) | yaml-only + `runtime_probe:` 声明 → 探针被评估, probe-warn 条目进 unverified_claims + d_payload | 当前: 声明被静默跳过 |
| **SC-13** (probe 边界负控, R2 簇 P) | proposal-only (两文件皆无) + `runtime_probe:` 声明 → 探针**仍不评估**, 零痕迹 (`test_l2_proposal_only_declaration_never_evaluated` 字面保绿); tasks.md-unreadable 早退不变 | 护栏: designed 边界不被 fall-through 误扩 |
| **SC-14** (归一化顺序, R2 簇 R-a) | `status: "done"  # x` → raw_status=done (剥注释→strip→剥引号顺序); `title: "Rule #6..."` → d['line'] 无裸引号残留 | 护栏: proposal 原顺序下 '"done"' 误判残留 |
| **SC-15** (末块边界, R2 簇 R-b) | 多任务 + 末任务后跟内容含 `status:` 形态子串的 0 缩进顶层键 (`summary:` 等) → 末任务 status 提取不受污染 | 护栏: SC-8 golden 尾随段恰不含 status 形态, 无法证伪此缺陷 |
| **SC-16** (metadata 隔离) | parser 级直喂真实 dual-layer 全文 (`dispatch-input-delivery`) → 返回 tasks 不含 metadata.status 值 (脱离 precedence 前提的隔离不变量) | 护栏 |

> SC 设计: SC-1~7/11~16 钉合成 fixture (主契约), SC-8 补真实语料有界抽样 (memory `feedback_gate_tracks_reality_synthetic_fixture` 正向应用: 契约钉合成, 真实语料只作零误伤佐证)。

---

## Impact

**Files (aria 子模块)**:
- `skills/state-scanner/scripts/lib/detailed_tasks.py` — **新增**: parser SOT + `_TASK_ID_LINE_RE`/`_split_task_blocks` 物理归位
- `skills/state-scanner/scripts/lib/spec_complete.py` — `gate_result` yaml-only 分支三态化 + scoped 属实性条目 + probe fold 可达性重构 (仅 yaml-present 臂) + `is_spec_complete` yaml tasks-branch + **:12-16 docstring 同步** (公式 + prose bullet) + 切片器 re-import + claim 串相邻注释 + 顺改 :41 「Step2」陈旧命名注 (实为 Step 7, R2 cr N-4)
- `skills/state-scanner/scripts/collectors/openspec.py` — carry_forward yaml fallback (:265-283)
- `skills/state-scanner/tests/` — SC-1~SC-16 新测试; **改写** `test_gate_yaml_only_source.py::test_yaml_only_warns_and_builds_payload`; **`test_spec_complete.py::TestRuntimeProbeFoldL2ProposalOnlyEvaporates` docstring 泛化措辞收窄** (「无 tasks.md 即不评估」→「无 tasks.md 且无 detailed-tasks.yaml」; 断言不动, 保绿)
- `skills/state-scanner/references/runtime-probe-declaration.md` — **:26-30 前置条件段两子态改写** (无 tasks.md 无 yaml → 仍零评估 / 无 tasks.md 有 yaml → v1.63.0 起被评估; 「L2 想用探针先补 tasks.md」向导语对 yaml-only 不再成立) (R2 簇 P)
- `skills/state-scanner/references/state-snapshot-schema.md` — 仅 `carry_forward_inventory` yaml fallback 语义 (:329)
- `skills/openspec-archive/SKILL.md` — 消费契约无需改 (**Step 7** D auto-issue 门控 `d_payload != null` :272-278 零变; Step 2 是 warn_overlay :167 — R2 勘正 step 名); :273 溯源注释一行顺改 (d_payload 第三来源: yaml status/标注残留)
- `skills/task-planner/DUAL_LAYER_SPEC.md` (**路径勘正**: 该 skill 无 references/ 子目录) — 一行反向指针: status 枚举现由 state-scanner archive gate 消费

**Files (主仓, 发版时)**: `aria/CHANGELOG.md` + 版本五处 + gitlink bump + README badge (v1.63.0)

**Downstream 行为变化 (方向: 只减噪/只增信息量/属实性轴不降格)**:
- yaml-only 归档: 残留轴干净 ∧ 无集成 title → full-pass (不建 tracker); 有残留 → tracker 精确列举; 有集成 title → scoped 属实性 warn (窄于 blanket 全类 warn)。
- `-unsupported` 串退役; `-unparseable` (文件级 parse-fail) 与 `-integration-claims-unverified` (scoped) 两新串。
- yaml-only 的 `runtime_probe` 声明从静默跳过 → 被评估; proposal-only/unreadable 维持零评估。
- collector: carry_forward 恒 0 → 真实计数; design_deferred 减噪。
- dual-layer 全路径 byte-identical。无 schema 破坏。

**非目标 (out-of-scope)**:
- `deferred_out_of_scope` 字段 (生产者侧不存在)。
- `_normalize_status` / `_status.py`。
- **yaml-only 完整 C-gate liveness parity** (合成 claim 喂 `extract_claim_symbols`) — scoped 披露先行 (决策 15), parity 留 follow-up issue (Phase D 开, cross-link 本 spec)。
- `_check_artifact_claims` 对 yaml-only 的适配 (吃 tasks_text, 同 parity follow-up)。
- #114 / task-planner schema 演进 (一行指针除外) / `_extract_yaml_key_list` 重构 / Aether。

---

## 设计决策记录 (供 R3 对焦; 15-18 为 R2-fix 新增, 9 为 R2 重写)

1. **issue 诉求按真实 schema 重框** (probe-first; `feedback_verify_predicate_inputs_exist`)。
2. **白名单 fail-CLOSED 不复用 `_normalize_status`**: exact-match vs token-match 对叙事串的防御力 (R1 更正后论证; R2 cr 实测语料 3 条 `"A.3` 引号叙事 status 佐证)。
3. **parse-fail 退回 blanket**: 文件级四态 (含 R2 新增计数自洽) 才 parse-fail; 条目级 fail-CLOSED 计残留。
4. **残留不升 verdict=warn**: 对称 tasks.md 路径; **Step 7** D-tracker 门控 d_payload≠null 不看 verdict (R2 勘正 step 名), warn_overlay 门控 verdict=warn — allow-with-tracker 正交成立。
5. **is_spec_complete 纳入 scope**: R1 5/5 + R2 复核维持非 creep。
6. **precedence 三消费点一致**: 探测点 :1299/:210/:267 + unreadable `continue` :272 核验一致。
7. **「干净」(残留轴) 三消费点统一 = 全白名单 ∧ 零标注**: 完整镜像 :1102-1112 两半。
8. **切片器物理归位**: 零跨文件引用 (R2 tech-lead grep 证), blast radius 完全内含; carry_forward.py 先例同型。
9. **(R2 重写) probe fold 可达性 — 窄化 + 显式反转先例**: 重构仅 yaml-present 臂; proposal-only 与 tasks.md-unreadable 维持 v1.54.0 designed 早退 (`TestRuntimeProbeFoldL2ProposalOnlyEvaporates` 保绿为未触碰护栏, SC-13)。**有意反转** DEC-20260705-001 §What Changes ③ R3 裁决在 yaml-only 子类的适用: 原前提「结构性不完整→探针无意义」随精确解析失效; 两配套文档 (runtime-probe-declaration.md :26-30 / 测试 docstring) 同步收窄入 Impact (`feedback_spec_precedent_verify_execution_history`: 反转 designed 裁决必须点名出处 + 前提失效论证)。
10. **CRLF 归一入规格**: 44/44 completed 带 `\r` 语料现实 (全在 dual-layer, §Why 已披露适用范围); SC-11 防御性负控。
11. **claim 串文档化落点 = spec_complete.py 相邻注释** (schema.md 零先例经 R2 km grep 证实)。
12. **条目级缺陷不整文件失败**: 含空值归一 None (`if rest else None` 惯例, R2 qa)。
13. **测试改写显式化**: carve-out 点名; 防「保旧测试绿焊回假绿」。
14. **自反性 dogfood**: 本 spec 归档时按自身 title 落 SC-2/SC-2b 态, Phase D 核对。
15. **(新, R3 精化) 属实性轴 scoped 披露, 不静默降格** (R2 簇 Q): blanket 覆盖的两轴中, 残留轴精确取代、属实性轴以 scoped 条目保留诚实态 (仅 **done-family** 集成类 title spec 发 — R3 采纳 status 滤波对齐 tasks.md 路径 `checked` 语义, pending 集成任务归残留轴不双报; 窄于 blanket); golden 实测 3 条 (2/1/0, R3 双 agent 勘正)。完整 liveness parity 留显式 follow-up。拒绝沉默 pass。
16. **(新) 归一化顺序对齐先例真实执行序** (R2 簇 R-a): 剥注释→strip→剥引号; quote-aware SOT 复用 custom_checks (非 frontmatter_block naive 副本); SC-14。
17. **(新, R3 补算法 + R4 补边界) 结构自洽计数为 parse_ok 第四态** (R2 簇 R-c): 隐形条目「既不完成也不残留」是理论新假绿, 计数不一致退 blanket (AC-5 先例纪律)。**计数必须 indent-anchored 且 range-bounded**: base indent 取首个 `- id:` 匹配捕获组, 只数同缩进直接子项 (R3: 深嵌套 17/17 误伤); 计数范围止于下一个 0 缩进顶层键 (R4: 同缩进兄弟键 `execution_order:` 等 11/17 误伤含 3/3 golden — **两位 R4 审计员按同一规格文本各自实现得出 16/16 MATCH vs 11/17 MISMATCH 相反结果, 即规格欠定的实证**); SC-3e + SC-3f (双反例) 钉死。
18. **(新) 块边界截断 = 新层二次后处理**: 不改共享 `_split_task_blocks` 本体 (SC-9 carve-out 严防方向); 顶层键字符级规则 + 折叠标量在键行截断; SC-15。
