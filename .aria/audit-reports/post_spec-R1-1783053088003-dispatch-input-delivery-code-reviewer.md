---
checkpoint: post_spec
mode: convergence
round: 1
agent: code-reviewer
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783053088003
converged: false
---

# post_spec R1 — code-reviewer (spec-vs-actual-code fidelity)

审计对象: `aria-2.0-m6-dispatch-input-delivery` proposal.md + tasks.md (Level 3 草稿, 未实施).
核实基准: `aria-orchestrator` HEAD `daf7c79` (逐条打开 spec 声称的 file:line).
权威决策源: `DEC-20260702-001`.

## Verdict: REVISE (0 Critical, 1 Major)

spec 中 15+ 处 file:line 断言逐条核实, **14 处行号全对 + 语义忠实**; 1 处 `ISSUE_URL` 现状断言与代码及 DEC 矛盾 → Major。

---

## Findings

### [Major][spec-fidelity:extension.py] §What B.2 "ISSUE_URL already number today" 与代码及 DEC 矛盾

**核实 file:line**: `extension.py:2149-2152` (`issue_url = f".../issues/{issue_id}"`) → `issue_id` 来源 `extension.py:2108` (`ctx.dispatch_row.get("issue_id","")`) → DB 值由 `extension.py:1176` 构造 `str(issue.get("id") or issue.get("number") or "")` = **internal Forgejo id (id-first, 非 number)**。

**问题**: spec §What B.2 写 "fix `ISSUE_URL` to use issue **number** (**already number today** at `extension.py:2149**, but re-verify against new id scheme)"。但代码在 2149-2152 内插的是 `issue_id` = 内部 id (1176 `id or number` 取 id 优先), **不是** issue number。该 "already number today" 断言:
1. 与代码事实不符 (当前用内部 id);
2. 直接矛盾权威 DEC 决策点 5: "修 ISSUE_URL 用 issue number (**非内部 id**)" —— DEC 明确说当前用内部 id、需修正。

**衍生实施隐患 (被 "already number" 掩盖)**: TG-2.1 把 `issue_id` 改成 `ARIA-<repo>-<number>` 字符串后, 直接内插 `f".../issues/{issue_id}"` 会产出**非法 URL** `/issues/ARIA-Aria-147` (Forgejo 需裸 number) → fetch 404 → FETCH_FAILED。故 B.2 实际须**从复合串抽取裸 number 重建 URL**, 而非 spec 暗示的"仅 re-verify"。"already number today" 会诱导实施者 under-scope B.2 (尤其 Aria 早期 issue 恰好 id==number 时表面能跑, 掩盖结构错误)。

**fix**: 删除/改写 B.2 括注 —— 改为忠实现状 "ISSUE_URL 当前内插 `issue_id`=内部 id (`extension.py:2108←1176` id-first), **非 number**; 新 scheme 下须从 `ARIA-<repo>-<number>` 抽取裸 number 重建 URL"。TG-2.2 相应从"verify uses number"升级为"rework URL 构造抽裸 number"。与 DEC 决策点 5 对齐。

---

## 逐条核实通过清单 (行号全对 + 语义忠实)

| spec 断言 | 核实结果 |
|-----------|----------|
| `initial.sh:106` 正则 `^[A-Z][A-Z0-9-]+$` (Step 1, 在输入加载前 die) | ✅ 行号+语义准确 |
| `initial.sh:145-147` `ISSUE_INPUT_DIR/${ISSUE_ID}/issue.yaml` + `-f` die | ✅ 准确 (key=ISSUE_ID) |
| `initial.sh:286` envsubst 白名单 **5 变量** `$ARIA_ISSUE_ID $ARIA_ISSUE_TITLE $ARIA_ISSUE_DESCRIPTION $ARIA_FILES_LISTING $ARIA_EXPECTED_CHANGES` | ✅ 逐字匹配; body 经 `$ARIA_ISSUE_DESCRIPTION` 不二次展开 |
| `initial.sh:524-536` AD-M1-4 **5-AND** (exit0 ∧ COMMIT_SHA ∧ PR_URL ∧ FILE_TOUCHED_HIT ∧ DIFF_CONTAINS_HIT) | ✅ 准确 |
| `initial.sh:243/251/396` FORGEJO_BOT_PAT 仅 clone+PR API; 无 issue-content fetch 代码 | ✅ grep 确认 initial.sh 无 issues API 调用 (仅 :396 PR-check + :485 PR-create curl) |
| `extension.py:1176-1177` 数字 id 构造 `id or number` | ✅ 准确 (自主传内部 id, 触发 106 正则 die) |
| `extension.py:2143` `prompt.txt` 按 `dispatch_id` (`/opt/aria-inputs/<dispatch_id>/prompt.txt`) | ✅ 准确; filename+key 双维错位描述成立 |
| `extension.py:2989` `head_branch = f"aria/{issue_id}"` 对齐容器 `BRANCH=aria/${ISSUE_ID}` (initial.sh:266) | ✅ 准确 |
| `compute-assertions.sh:94-120` 空 expected 恒真 (FILE_HIT/DIFF_HIT init=true, 空列表 loop 不迭代→留 true) | ✅ 准确, false-green 复现路径成立 |
| `schema.sql:61` `issue_id TEXT` / `:245` PK `(issue_id,dispatch_id)` / `:273` partial-unique `uq_issue_active_partial` WHERE state NOT IN (S_FAIL,S9_CLOSE) | ✅ 三行全对; "值内嵌 repo+number 无结构迁移"结论成立 |
| `host-volume.hcl:26-29` `aria-runner-inputs` local host_volume `/opt/aether-volumes/aria-runner/inputs` read_only, 非 NFS | ✅ 准确; 否 D 依据成立 |
| `RENDERING_CONTRACT.md:61-78` expected_changes 双段 + `:76` "always non-empty (validator enforces)" | ✅ 逐字匹配; "validator 仅 file 路径" 推理成立 |
| `db.py:622` AC-2 `json_extract('$.issue_type_hint')` 顶层非 issue_id join | ✅ 准确; audit_extra seeded-first reserved-key 保护存在 |
| `alloc_status_provider.py:259` 输出侧 stderr marker + nomad logs API 节点无关通道 | ✅ 准确 (259-267 NOTE) |
| TG 符号可实施性: `build_nomad_meta` (prompt_render.py:232, import ext:77) / `_handle_s4_launch` (ext:2093) | ✅ 均存在, 无引用不存在符号 |

## 任务可实施性 (TG-1..6)

- 无循环依赖: TG-1↔TG-2 co-dependent (spec 明示"one integrated change"), TG-4 gates TG-1+2+3, TG-6 gates TG-4 — DAG 合理。
- 无引用不存在符号 (build_nomad_meta / _handle_s4_launch 均在)。
- RED-first (1.7/C.1) 有真代码锚点 (compute-assertions.sh:94-120)。
- 唯一实施风险 = 上述 B.2/TG-2.2 ISSUE_URL under-scope (Major finding 已提修正)。

## 非阻塞说明 (不计 finding)

- §Prerequisite #2 "PAT used only for clone :251 + PR API :396" 省略 `:485` PR-create POST (同属 PR API, 非 issue-content fetch) — 核心断言"无 issue-content fetch"成立, 不误导修复方向。
