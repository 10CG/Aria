---
audit_type: post_spec
verdict: PASS
agent: code-reviewer
round: 2
checkpoint: convergence
timestamp: 1783054040265
spec_id: aria-2.0-m6-dispatch-input-delivery
vote: PASS
---

# post_spec R2 — code-reviewer — dispatch-input-delivery (convergence)

**审计对象**: `openspec/changes/aria-2.0-m6-dispatch-input-delivery/proposal.md` + `tasks.md`
**代码基线**: `aria-orchestrator` HEAD `daf7c79` (与 spec §Recon provenance 声明一致, 已核实 `git rev-parse HEAD`)
**职责**: R1 修复落地验证 (spec-vs-code 忠实度) + 新增 file:line 断言独立核实 + fix-introduced regression 抓取

---

## 判定: **PASS** / Vote: **PASS**

R1 提的 M1 (Major, ISSUE_URL 现状误述) 已**真落地**且逐条 file:line 核实全对；本轮 spec 大改新引的全部代码断言 (§What C 三档 outcome / §What B.5 fail-marker / Alternatives META cap / How AD 表) 逐条打开核实**行号+语义全部忠实**；spec 内部 (§What ↔ AC ↔ tasks) 对同一机制的三处描述一致，无自相矛盾；无 fix-introduced regression。仅 4 条 Minor 精度注记，均不构成语义误述或误导实施者的行号漂移。

---

## R1 遗留 finding 复核

### M1 (R1 Major) — ISSUE_URL 现状误述 → **RESOLVED (verified)**

修订后 §What B.3 (proposal:103-111) 现为忠实描述, 三处 file:line 独立核实全对:

- `extension.py:1176` = `issue_id = str(issue.get("id") or issue.get("number") or "")` — **id-first** 属实 (Forgejo issue 恒有 truthy `id` → 用内部 cross-repo id 非 per-repo number)。✅ B.3 "internal cross-repo id, not the per-repo number" 忠实。
- `extension.py:2149-2152` = `issue_url = ( f"{self.forgejo_base_url.rstrip('/')}" f"/{forgejo_org}/{forgejo_repo}/issues/{issue_id}" )` — 直接内插 `issue_id` 属实。✅
- `extension.py:2147-2148` = `forgejo_org = os.environ.get("FORGEJO_ORG", "10CG")` / `forgejo_repo = os.environ.get("FORGEJO_REPO", "Aria")` — org/repo 硬编码属实。✅

R1 M1 要求的"忠实描述"已完整落地, 且前瞻性 rationale (复合 issue_id 直接内插 → `/issues/ARIA-Aria-147` → 404) 逻辑成立。

---

## 本轮新增 file:line 断言 — 逐条独立核实 (全新)

### §What C 三档 outcome (false-green 修)
- `compute-assertions.sh:37-39` — `if [[ ! -f "$ISSUE_YAML" ]]; then ... exit 1` **die 属实**。✅
- `compute-assertions.sh:94-120` — `FILE_HIT=true`(:96) + loop skip-on-empty(:97-103) / `DIFF_HIT=true`(:113) + loop(:114-120)；空列表→loop 不迭代→两者恒 true。✅ Why:43-46 语义精确。
- `initial.sh:513` — call-site block (`if [[ -f "$LIB_DIR/compute-assertions.sh" ]]`)，实际调用在 :514，无 ISSUE_YAML 存在性条件 → "unconditionally with $ISSUE_YAML" 语义成立。✅ (block anchor, 见 Minor-3)
- `initial.sh:526-535` — `if PENDING`(:526) + 5-AND(:527-531) → SUCCESS(:532) else ASSERTION_MISMATCH(:534)。✅
- `initial.sh:591-596` — `if SUCCESS → exit 0`(:592-593) else `exit 1`(:595)。✅ 逐行精确。

### §What B.5 fail-marker 消费
- `extension.py:2593-2640` (_handle_s5_await terminated 分支) — `elif alloc_state=="terminated"`(:2593) → 读 `exit_code`(:2594) → 非零 else 分支(:2620) → `FailReason.CONTAINER_CRASH`(:2632)。✅ "只读 exit_code, 非零→CONTAINER_CRASH" 忠实。函数 def 在 :2467，但 spec 引用的是 exit_code-routing 逻辑所在区间 (2593-2640)，语义准确非误导。
- `interfaces.py:67-86` — `class FailReason(str, Enum)`(:67) ... `CONTAINER_CRASH = "container_crash"`(:86)；docstring "no implicit 'other' fallthrough" = **closed enum** 属实。✅ 区间 67-86 精确 bracket 至 CONTAINER_CRASH。
- `get_alloc_logs()` 先例 — `alloc_status_provider.py` logs API grep 通道存在 (DEC:14 + `:259` 引用)，redo.sh marker 同通道先例成立。✅

### Alternatives + Prereq
- `prompt_render.py:42` — `META_VALUE_CAP_BYTES: int = 100 * 1024  # 100 KB`。✅ 逐行精确。
- `m0-report.md §1.2` R7 辟谣 — §1.2(:77) 内 R7(:85-89): 原 "Nomad meta 64KB" → 实测 `MAX_ARG_STRLEN = 131072 (128 KiB)`, 阈值改 100KB per field。✅ "R7 debunked 64KB myth, 真上限 128 KiB" 完全忠实。与 arch-decisions:384 风险表 "64KB (R7)" 互证。

### §How AD 表
- AD-M6-10 "下一可用" — 核实全部 AD-M6 heading: M6-1/2/4/5/6/7/9 used, M6-3 无 heading(skipped), M6-8(:3969)="Reserved slot (Retired)", M6-9(:3987) last → **AD-M6-10 确为下一可用**。✅ 编号声明完全正确。
- AD4 cell `architecture-decisions.md:384` — 位于 `## AD4`(:326) 的 `### 风险`(:379) 表；:384 = `| 2 | ... 64KB 限制 (R7) | 中 | AD-M0-5 约定: prompt 写 bind mount 文件, meta 只传 ISSUE_ID + 小参数 ... |`。✅ "AD4 风险表 cell 把 bind-mount 前提误标为 AD-M0-5 约定" 属实。
- AD-M0-5 body `:1035` — `### AD-M0-5 — m0-handoff.yaml schema 锁定 12 字段`，与 bind-mount 无关。✅ "误标"判定成立 + "leave untouched"正确。

### D.1/D.2 recon 修正 (vs DEC decision-point 8)
- `schema.sql:61` issue_id TEXT / `:245` PK (issue_id, dispatch_id) / `:273` partial-unique `uq_issue_active_partial`。✅ "value reformat 非结构迁移" 判定成立。
- `db.py:622` json_extract issue_type_hint — audit_extra top-level annotation (非 dispatches 列)，AC-2 走 json_extract 非 issue_id join。✅ recon 修正忠实 (见 Minor-4)。
- `host-volume.hcl:26` — host_volume "aria-runner-inputs" stanza, path=/opt/aether-volumes/aria-runner/inputs, read_only；本地非 NFS → D 诚实否决成立。✅ (见 Minor-2)

---

## 内部一致性 (fix-introduced regression 抓取) — **无矛盾**

- **5-AND gate 多处引用**: Why:46(`:524-536`) / What C:132(`:526-535`) / 审计注:129(`:526-596`) — 均 bracket 同一 gate，范围互洽无冲突。
- **_handle_s5_await 多处引用**: B.5(`:2593-2640` 全 terminated 分支) / 审计注 + What C + tasks 2.5(`:2620-2640` 非零 else 子分支) — 两范围均正确，无矛盾。
- **AD-M0-5 处理一致性**: proposal:12/185/187/203/277 + tasks 5.2 **全部**统一为"correct AD4 cell mislabel + leave AD-M0-5 body untouched"；**无任何残留 "amend AD-M0-5"** (DEC 原 line 22/88 的 "amend AD-M0-5" 已被 spec recon 修正取代，且 line 203 显式记 "DEC line 22 carried the same misattribution — corrected here")。这是本轮最易踩的 fix-introduced 矛盾点，**已确认干净**。
- **AUTONOMOUS_COMPLETED 三处描述一致**: What C.2(:146) = tasks 1.9 = AC-4(b/c)，定义 (claude_exit==0 AND commit AND PR / `assertion_verified:false` / 排除 verified-SUCCESS corpus) 三处对齐。✅
- **ISSUE_URL 修复三处一致**: B.3 = tasks 2.3 = AC-11 (`{target_repo}/issues/{raw_number}` + raw number 单独保留不从复合 id 解析)。✅

---

## Findings

### Minor (精度注记, 非阻塞, 建议 Phase B 实施时留意)

- **Minor-1 (全新)** — proposal:104 B.3 把 `issue_id` 引作 `str(issue.get("id") or issue.get("number"))`，实际源码含尾部 `or ""`(`extension.py:1176`)。省略不改 id-first 语义，纯 cosmetic。
- **Minor-2 (全新)** — proposal:213 Alternatives 把 `path=/opt/...` 归到 `host-volume.hcl:26`；`path` 字面在 :27，:26 是 host_volume stanza 声明行。Prereq 表 (proposal:220) 的 `:26-29` 区间正确；语义 (local not NFS) 100% 成立。stanza anchor 可接受。
- **Minor-3 (全新)** — proposal:132 / tasks 1.8 引 `initial.sh:513` 为 compute-assertions 调用点；:513 是 `if [[ -f ... ]]` guard，实际 invocation 在 :514。block anchor 可接受 (skip 接线点即此 block)。
- **Minor-4 (全新)** — Prereq (proposal:223) 引 `db.py:622` 佐证 AC-2 json_extract 路径；:622 是**注释**行 (描述 audit_extra→issue_type_hint→json_extract 机制) 而非实际 acceptance SQL。作为 "issue_type_hint 存于 audit payload_json 非 issue_id join" 的证据充分，可接受。

无 Major，无 Critical。

---

## Rationale

新旧行号全对 + 语义忠实 → PASS。R1 M1 修复真落地 (非 paper-fix): 修订后 B.3 的三处 file:line (1176/2147-2148/2149-2152) 独立打开核实全部命中，且现状描述从 R1 的误述转为忠实 (internal id-first + org/repo hardcode)。本轮 spec 大改最易滋生的两类风险——(a) 新引代码断言行号漂移、(b) fix-introduced 内部矛盾——均已排查: 20+ 条新增 file:line 全部逐行核实命中或语义准确 bracket；AD-M0-5 "amend→leave untouched" 的修正在 proposal 5 处 + tasks 1 处完全统一无残留旧措辞。4 条 Minor 均为 anchor/引用精度问题，不误导实施者，不阻塞收敛。
