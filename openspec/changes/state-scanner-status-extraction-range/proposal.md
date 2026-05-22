# state-scanner — fix `_status` lifecycle-head extraction range + extend token dict (aria-plugin #50)

> **Level**: 2 (Minimal — collector 逻辑 fix + regression tests + doc note)
> **Status**: Approved (post_spec audit R1→R2→R3 CONVERGED 2026-05-21,5-agent convergence,verdict PASS)
> **Change ID**: `state-scanner-status-extraction-range`
> **Trigger**: Forgejo aria-plugin [#50](https://forgejo.10cg.pub/10CG/aria-plugin/issues/50) — `_extract_status` 提取范围无上限 → 长单行 Status 里子任务 token shadow lifecycle 归类
> **Triage evidence**: [issuecomment-7980](https://forgejo.10cg.pub/10CG/aria-plugin/issues/50#issuecomment-7980) (local: `.aria/triage-report.json` + `.aria/triage-comment.md`)
> **Triage verdict**: `confirmed` (v1.23.0 实测复现 1/1) · severity `major` · action `next-cycle`
> **Sibling**: `openspec/archive/2026-05-13-aria-issue-101-status-normalize/` — #101 修了 substring-shadow (word boundary),#50 是同类 bug 的另一面 (提取范围)
> **post_spec audit**: R1 5-agent (1 Critical + ~10 Important) → R2 (全 RESOLVED,4/5 CONVERGED) → R3 (全 CONVERGED) — 报告 `.aria/audit-reports/post_spec-R3-2026-05-21-state-scanner-status-extraction-range-aggregate.md`
> **Created**: 2026-05-21

---

## Why

`state-scanner` v3.0 的 `aria/skills/state-scanner/scripts/collectors/_status.py` 在大型 spec 上仍会错归 lifecycle status,根因有两个独立但同根的问题。

### Bug 1 (主因): `_extract_status` 提取范围无上限 → 长单行 Status 里子任务 token shadow lifecycle

`_STATUS_PATTERNS` 用 `re.MULTILINE` 的 `^...(.+?)\s*$` 抓取 —— **只截单行,但对单行长度无任何上限**。大型 spec (nexus us-036、Aria 自身的 US-022 等) 习惯把 `> **Status**: ...` 字段当 mini-changelog 写成一长行 (子任务状态 + 归档历史 + 阻塞项),raw 长达 1500+ chars。

`_normalize_status` 的 `done / complete` fallback 用 word-boundary `\bdone\b` 在**整个 raw 字符串**上搜索 —— 头部主语义 phrase 若不含已识别 lifecycle token,埋在子任务叙述里的 `done` 就会命中 fallback。

**实测复现** (v1.23.0,triage case-1):

```python
raw = "🟢 **Phase B Sprint 2 delivered** — archival blocked; (2) TASK-101 closed (PR #53, docs sync 标 done); blockers: live verify outstanding"
_normalize_status(raw)   # → "done"  ❌  应是 "implemented" (头部 = delivered,archival-blocked)
```

下游影响: still-blocked spec 被错归 `done` → 错放进 `openspec.pending_archive[]` → state-scanner 推荐 `openspec-archive` 工作流 → user 跟推荐会 **silent 归档活跃 spec**。这与 #101 下游影响同类。

### Bug 2 (次生): `delivered` / `shipped` 不在 token 字典

即使修了提取范围,Bug 1 复现案例的头部 `🟢 **Phase B Sprint 2 delivered**` 仍不含任何已识别 token (`delivered` 不在字典) → 归 `unknown`。`unknown` 虽不污染 `pending_archive`,但依赖 status 的 surfacing 规则 (carry-forward / priority_items) 会漏报。这与 #101 Bug 2 (`Implemented` 缺失) 同型。

---

## What

### In scope

1. **修 Bug 1 — lifecycle-head 截断**: 新增 `_status_lifecycle_head(raw)` helper,把 raw Status 截到 **lifecycle 主语义头段** 再交给 `_normalize_status` 分类。截断点 = 第一个文档化分隔符 (em-dash / en-dash,可无空格 / 空格包围的 ASCII hyphen / 全半角分号 / 全角句号),并加 hard char-cap 兜底。**接受 `None` 输入** (返回 `("", False)`)。
2. **修 Bug 1 附带 — `status_field_truncated` soft_error**: 新增 `_status_field_overlong(raw) -> bool` 瘦谓词,collectors (`openspec.py` / `requirements.py`) 在 char-cap 兜底触发时调 `r.soft_error("status_field_truncated", ...)`,信号经 scan.py 聚合进 snapshot `errors[]` (exit 10 路径)。
3. **修 Bug 2 — 扩 token 字典**: `_normalize_status` 在 `implemented` 分支加 `delivered` / `shipped` token,映射到既有 `implemented` lifecycle state。
4. **加 regression tests**: #50 nexus case + 截断 case + `delivered`/`shipped` case + shadow guards + 边界 case + `raw_status` 完整性 + #101 (13) + #73 (8) 既有 regression 全过。
5. **state-scanner SKILL.md doc** (T5): "Status 字段最佳实践" 段补显式警告 + "Supported token set" 表加 `delivered`/`shipped` + "Implementation note" 段同步新 helper 与 test 数量。

### soft_error 通道 — audit R1 收敛决策 (RESOLVED)

R1 audit (BA-6 / CR-1 / TL-2 / QA-2 / QA-6) 一致指出原 "Design note 开放子问题" 必须在本 audit 收敛。**收敛结论: 采纳 option (b)**。

- `_normalize_status` 签名**保持** `(raw: str | None) -> str` 不变 (`openspec.py` + `requirements.py` 共 5+ 处 caller、#101 的 13 + #73 的 8 个 regression test 依赖)。
- 新增独立瘦谓词 `_status_field_overlong(raw: str | None) -> bool`,内部 `return _status_lifecycle_head(raw)[1]`。
- collectors 各处: `raw = _extract_status(...)` 后,`status = _normalize_status(raw)` (现状不变) + `if _status_field_overlong(raw): r.soft_error("status_field_truncated", ...)`。
- **被否选项**: option (a) 让 `_normalize_status` 返回 `(str, bool)` —— 破坏签名承诺,否决;option (c) 推迟 soft_error —— 与 In scope #2 + Success Criteria 自相矛盾,否决。
- **双调用声明 (TL-3)**: 一个 Status 字段处理时 `_status_lifecycle_head` 被调两次 (一次经 `_normalize_status`,一次经 `_status_field_overlong`)。这是**有意取舍** —— 纯函数、确定性、O(短行) 成本可忽略,换 `_normalize_status` 签名稳定。不视为缺陷。

### Out of scope

- `_extract_status` 签名/返回值不变 —— 仍返回**完整单行 raw**;6 个 `_STATUS_PATTERNS` regex 一个字不增不改 (snapshot 的 `raw_status` 字段依赖完整叙述供人类展示;截断仅用于 lifecycle 归类)。
- `openspec.py` / `requirements.py` 仅新增 soft_error 发出一行 —— **不改** `pending_archive` 触发逻辑 (仅 `status == "done"` 触发是正确的)、不改 `raw_status` 字段赋值。
- `_normalize_status` 优先级链整体 rewrite (priority-chain 模式保留,#101 已定型)。
- 新增 lifecycle state 超出既有 enum (`delivered`/`shipped` 复用 `implemented`,不引入新 state)。
- snapshot schema 变更 (本 fix 不动 schema;`status` 字段值域不变)。
- 逗号 `,` **不作分隔符** (lifecycle 短语如 `Approved, revised` 必须存活);ASCII 句号 `.` **不作分隔符** (避免误切 `v2.0` 版本串)。

### 截断放在 `_normalize_status` 内而非 `_extract_status` (设计依据)

issue 选项 1 字面建议改 `_extract_status` 只返回首句。但 snapshot 的 `openspec.changes.items[].raw_status` 与 `requirements.stories.items[].raw_status` 依赖**完整** Status 文本供展示 (issue 自身亦承认 "Status 长描述是 useful narrative,不应被 truncate")。R1 audit (CR MN-2) 实地核实 `openspec.py` + `requirements.py` 确存完整 raw 到 `raw_status`。

因此 `_extract_status` 不变 → 新 helper `_status_lifecycle_head()` 做截断 → `_normalize_status` 内部调用它。`raw_status` (full) 与 `status` (normalized-from-head) 职责分离,向后兼容。

### Fix sketch (R1-fixed)

```python
import re

# 文档化的 lifecycle-head 分隔符 (R1 audit BA-1/BA-2/IM-1 加固):
#   - em-dash U+2014 / en-dash U+2013, 可无空格 (\s* 两侧)
#   - 空格包围的 ASCII hyphen ` - ` (\s-\s — 强制两侧空白, 不误切 PR-A / 2026-05-09)
#   - 半/全角分号 ; ；, 全角句号 。
# 逗号 , 与 ASCII 句号 . 刻意排除 (见 Out of scope)。
_STATUS_HEAD_SEPARATOR_RE = re.compile(r"\s*[—–]\s*|\s-\s|[;；。]")

# char-cap 兜底: Aria/nexus 语料中合法 head 段实测 < ~90 chars; 200 给 2× 余量。
# 仅在 head 内无任何分隔符时才可能触发。
_STATUS_HEAD_MAX_CHARS = 200


def _status_lifecycle_head(raw: str | None) -> tuple[str, bool]:
    """Return (lifecycle-bearing head segment, truncated_by_cap).

    截到第一个文档化分隔符; 仍超 cap 则硬截并置 truncated=True。
    None-safe: raw is None → ("", False) (collector 独立调用路径必需)。
    """
    if raw is None:
        return "", False
    m = _STATUS_HEAD_SEPARATOR_RE.search(raw)
    head = (raw[:m.start()] if m else raw).strip()
    truncated = False
    if len(head) > _STATUS_HEAD_MAX_CHARS:
        head = head[:_STATUS_HEAD_MAX_CHARS]
        truncated = True
    return head, truncated


def _status_field_overlong(raw: str | None) -> bool:
    """True 当 Status head 段超 char-cap (无分隔符的超长行)。collector 用它发 soft_error。"""
    return _status_lifecycle_head(raw)[1]


def _normalize_status(raw: str | None) -> str:
    # 签名不变。Bug 1 fix: 只看 lifecycle 头段。
    if raw is None:
        return "unknown"
    head, _ = _status_lifecycle_head(raw)
    low = head.lower()
    # ... 既有优先级链不变 (terminal → #73 transitional → pending → in_progress → approved → ...) ...
    # Bug 2 fix: implemented 分支扩 delivered / shipped
    if (_has_token(low, "implemented") or _has_token(low, "delivered")
            or _has_token(low, "shipped")):
        return "implemented"
    # ... done/complete LAST fallback 不变 ...
```

---

## Impact

| Type | Description |
|---|---|
| **Positive** | 长单行 Status 不再让子任务 token shadow lifecycle;still-blocked spec 不再误进 `pending_archive` |
| **Positive** | `delivered`/`shipped` 头部 spec 正确归 `implemented`,carry-forward / priority_items surfacing 不再漏报 |
| **Positive** | `status_field_truncated` soft_error 给 spec 作者可见反馈 (Status 字段写法引导) |
| **Risk** | 截断分隔符误切合法 lifecycle 文本;缓解: 分隔符集经 R1 audit 加固 (em-dash 变体 + ASCII hyphen 须空格包围 + 排除逗号/ASCII 句号) + T4 regression 覆盖既有真实 Status |
| **Risk** | #73 transitional 短语 (`implementation-complete`/`implementation-done`) 若被作者写在分隔符后会被截掉;缓解: 属 Status 写法违规 (T5 doc 明确),且 T4 跑全部 8 个 `TestStatusNormalizationIssue73Fix` 锁定头段内行为不变 |
| **Risk** | 分隔符 (分号/句号) 出现在括号内被当截断点;缓解: 实测当前 token 集下不产生错误归类 (lifecycle token 总在分隔符前),T4 加括号内分隔符 case 钉死行为 |
| **Risk** | `delivered`/`shipped` 加入字典误命中 narrative;缓解: 截断已先去分隔符后叙述 + `\b` word-boundary (`undelivered`/`preshipped` 不命中) + shadow-guard test |
| **Note** | 这是 mechanical collector (确定性纯函数) 改动,非 Skill LLM 触发逻辑;验证用 unit/regression test (Rule #6 适用性见 References) |

---

## Tasks

详见 [tasks.md](./tasks.md)。简版:

- [ ] T1 — `_status.py`: `_status_lifecycle_head()` (regex 分隔符 + None-guard + char-cap) + `_status_field_overlong()` + 接入 `_normalize_status`
- [ ] T2 — `_status.py`: 扩 token 字典 `delivered` / `shipped` → `implemented`
- [ ] T3 — `openspec.py` + `requirements.py`: char-cap 触发时发 `status_field_truncated` soft_error (option (b),已收敛)
- [ ] T4 — regression tests (#50 case + 截断 + delivered/shipped + shadow guards + 边界 case + raw_status 完整性 + #101 13 + #73 8 全过)
- [ ] T5 — state-scanner SKILL.md: 最佳实践警告 + Supported token set 表 + Implementation note 三处更新
- [ ] T6 — 全量 state-scanner test suite 通过 + aria-plugin PATCH 版本号 (5 文件) + 主仓 VERSION 插件版本记录
- [ ] T7 — Phase C ship (pre-merge gate Rule #8;aria-plugin PR + Aria submodule-bump PR + 多远程推送)
- [ ] T8 — Phase D archive + 关闭 aria-plugin #50

---

## Success Criteria

- [ ] **Bug 1 — 截断**: `_normalize_status` 对长单行 Status 返回 ≠ 误归值:
  - `"🟢 **Phase B Sprint 2 delivered** — archival blocked; ... 标 done; ..."` → `implemented` (配合 Bug 2)
  - `"Approved — Phase A done, ready for Phase B"` → `approved` (em-dash 后 `done`/`ready` 不参与)
  - `"⏸ DRAFT pending review — Phase B PR-A done 2026-05-09"` → `pending`
  - `"WIP - 子任务 done"` (空格包围 ASCII hyphen) → 头部 `WIP` 无 token → `unknown` (NOT `done`)
- [ ] **Bug 2 — token 字典**: `"Phase B delivered"` → `implemented` / `"Shipped to prod"` → `implemented` / `"DELIVERED"` (大写) → `implemented`
- [ ] **Shadow / ordering guards**: `"undelivered work remaining"` → 不归 `implemented`;`"Approved (delivered by PR)"` → `approved` (优先级不变)
- [ ] **soft_error**: Status head 超 `_STATUS_HEAD_MAX_CHARS` 且无分隔符 → collector `r.errors[]` 含 `{"error": "status_field_truncated", ...}` (经 scan.py 聚合进 snapshot `errors[]`)
- [ ] **raw_status 完整性**: 长单行 Status 的 spec,snapshot `raw_status` 字段长度 == 原始完整 raw (未被截断),`status` 字段 == 截断归类结果
- [ ] **无 regression**: `tests/test_openspec.py` 的 `TestStatusNormalizationIssue101Fix` (13) + `TestStatusNormalizationIssue73Fix` (8) 全部通过;全量 state-scanner test suite 无 regression;`pending_archive` 在 Aria 当前所有 active spec 上仍返回空数组 (live 验证,signal 限于当前 2 个 active spec)
- [ ] 新 regression test 全部通过
- [ ] aria-plugin 5 处版本文件同步 (PATCH bump v1.23.0→v1.23.1) + 主仓 VERSION 更新;CHANGELOG 记录

---

## References

- Trigger issue: [Forgejo aria-plugin #50](https://forgejo.10cg.pub/10CG/aria-plugin/issues/50)
- Triage: [issuecomment-7980](https://forgejo.10cg.pub/10CG/aria-plugin/issues/50#issuecomment-7980) (local: `.aria/triage-report.json`)
- Sibling Spec: `openspec/archive/2026-05-13-aria-issue-101-status-normalize/proposal.md` (#101 substring-shadow,word-boundary 引入)
- Related Spec: `openspec/archive/2026-05-20-state-scanner-bugfix-locale-and-transitional-status/proposal.md` (#73 transitional-status 短语)
- Target file: `aria/skills/state-scanner/scripts/collectors/_status.py`;collector callers: `collectors/openspec.py`、`collectors/requirements.py`;soft_error API: `collectors/_common.py::CollectorResult.soft_error`
- Rule #6 (CLAUDE.md): `_normalize_status` / `_status_lifecycle_head` 属 state-scanner v3.0 mechanical collector 的确定性纯函数。`/skill-creator` AB 衡量 LLM prompt/触发质量,对纯函数逻辑改动无信息增益;正确质量门禁是 unit/regression test (state-scanner-mechanical Spec 确立的 mechanical 验证契约;参 `feedback_python_script_importlib_smoke`)。
- Rule #8 (CLAUDE.md): Phase C pre-merge gate
