# Tasks — state-scanner-status-extraction-range

> **Spec**: `state-scanner-status-extraction-range` · **Level**: 2
> **Trigger**: Forgejo aria-plugin #50
> **Target files**: `aria/skills/state-scanner/scripts/collectors/_status.py` (主) ·
> `collectors/openspec.py` + `collectors/requirements.py` (T3 仅新增 soft_error 发出) ·
> `aria/skills/state-scanner/SKILL.md` (T5) · `aria/skills/state-scanner/tests/` (T4)
> **post_spec audit**: R1 收敛后 tasks (soft_error = option (b),无悬空决策)

---

## T1 — `_status_lifecycle_head()` + `_status_field_overlong()` + 接入

- [x] `_status.py` 新增 `_STATUS_HEAD_SEPARATOR_RE` (regex:em-dash/en-dash 可无空格 `\s*[—–]\s*` | 空格包围 ASCII hyphen `\s-\s` | `[;；。]`) + `_STATUS_HEAD_MAX_CHARS = 200` (注释说明 derivation)
- [x] 实现 `_status_lifecycle_head(raw: str | None) -> tuple[str, bool]` — **None-guard 返回 `("", False)`** + 截最早分隔符 + char-cap 兜底
- [x] 实现 `_status_field_overlong(raw: str | None) -> bool` — `return _status_lifecycle_head(raw)[1]`
- [x] `_normalize_status` 内部改用 `head` (经 `_status_lifecycle_head`) 而非整个 `raw` 做归类
- [x] `_normalize_status` 签名保持 `(raw: str | None) -> str` 不变 (#101 13 + #73 8 个 regression test 依赖)
- [x] 模块 docstring 注明:逗号 `,` 与 ASCII 句号 `.` 刻意排除分隔符集

## T2 — 扩 token 字典 `delivered` / `shipped`

- [x] `_normalize_status` 的 `implemented` 分支加 `_has_token(low, "delivered")` / `"shipped"`
- [x] 确认优先级正确 — `approved` 仍在 `implemented`-family 之前 (#101 BA-M2 不破坏)
- [x] docstring 优先级注释同步更新

## T3 — `status_field_truncated` soft_error 接入 (option (b),已收敛)

- [x] `openspec.py` collect 函数:`_extract_status` 后,`if _status_field_overlong(raw): r.soft_error("status_field_truncated", f"{d.name}: Status head 超 {_STATUS_HEAD_MAX_CHARS} chars 无分隔符")` (detail 含 spec id,对齐 `openspec.py` 既有 soft_error 惯例)
- [x] `requirements.py` 同样接入 (prd 路径 ~L132 + US 路径 ~L151,凡调 `_extract_status` 处);soft_error 调用须在 `try/except OSError` 块外、`raw` 已定义后
- [x] 确认 `_status_field_overlong` 的 None 输入安全 (raw 可能为 None)
- [x] 确认 soft_error 走 scan.py exit 10 路径,不阻塞 snapshot 产出;**不改** `pending_archive` 触发逻辑与 `raw_status` 赋值

## T4 — Regression tests (`tests/test_openspec.py` 或同级新测试类)

核心 #50:
- [x] triage case-1 长单行 Status → `_normalize_status` 归 `implemented` (不归 `done`)
- [x] em-dash 截断:`"Approved — Phase A done"` → `approved`
- [x] 空格包围 ASCII hyphen:`"WIP - 子任务 done"` → `unknown` (NOT `done`)
- [x] 分号截断:`"Approved; Phase A done"` → `approved`
- [x] 全角句号截断:`"WIP。Phase A done"` → `unknown` (NOT `done`)
- [x] ASCII `.` 不截:`"v2.0 implemented"` → `implemented`
- [x] #73 短语跨分隔符 (NEW-IM-1):`"implementation — complete"` 类输入 → 行为钉死 (头段 = `implementation`,短语被分隔符切断,预期 `unknown`);锁定截断逻辑首次插在 #73 transitional 分支前的边界,把 proposal Risk 声明升格为 test 锚点

Bug 2:
- [x] `delivered` / `shipped` → `implemented`;大写 `"DELIVERED"` → `implemented` (case-insensitivity)
- [x] shadow guard:`"undelivered work remaining"` / `"preshipped artifacts"` 不归 `implemented`
- [x] ordering:`"Approved (delivered by PR)"` → `approved`

边界:
- [x] char-cap:head 恰 200 字符 → `truncated=False`;201 字符 → `truncated=True`
- [x] 分隔符在位置 0 (`" — narrative"`) → head=`""` → `_normalize_status` 归 `unknown`
- [x] 多个 em-dash → 截在第一个
- [x] 分隔符在括号内 (`"In Progress (Phase 1。Phase 2)"`) → 行为钉死 (归 `in_progress`)
- [x] 逗号存活:`"Approved, revised"` → `approved`
- [x] `_status_lifecycle_head(None)` → `("", False)`;`_status_field_overlong(None)` → `False`

契约 / e2e:
- [x] raw_status 完整性:`collect_openspec()` 对长单行 Status spec → snapshot `raw_status` 长度 == 完整 raw,`status` == 截断归类结果
- [x] soft_error e2e (openspec):`collect_openspec()` 对 head 超 200 无分隔符的 spec → `r.errors` 含 `{"error": "status_field_truncated", ...}`
- [x] soft_error e2e (requirements,NEW-QA-3):`collect_requirements()` 对 head 超 200 无分隔符的 prd → `r.errors` 含 `{"error": "status_field_truncated", ...}` (T3 改了 `requirements.py` 两处,e2e 须对称覆盖,不能只测 openspec)

无 regression:
- [x] `TestStatusNormalizationIssue101Fix` 13 test 全过
- [x] `TestStatusNormalizationIssue73Fix` 8 test 全过 (既有 8 个 fixture 的 #73 短语均在头段内,截断后行为不变;新引入的"短语跨分隔符"行为由上方核心 #50 段的 NEW-IM-1 case 单独钉死)

## T5 — state-scanner SKILL.md 三处更新

- [x] "Status 字段最佳实践" 段:在 `<token> — <narrative>` 示例旁补**显式警告** —— 分隔符 (` — `/` - `/`;`/`。`) 后的 narrative 不参与 lifecycle 归类 (`raw_status` 仍保留完整文本供展示)
- [x] "Supported token set" 表:`implemented` 行 tokens 列补 `delivered` / `shipped` (Rule #3 文档↔代码同步)
- [x] "Implementation note" 段:描述更新含 `_status_lifecycle_head` / `_status_field_overlong`;regression test 数量更新 (13 + 8 + 本 fix 新增)

## T6 — 全量验证 + 版本号

- [x] 全量 state-scanner test suite 通过 (stdlib unittest,无 regression)
- [x] live 验证:`pending_archive` 在 Aria 当前所有 active spec 返回空数组 (signal 限于当前 active spec,fix 正确性主要靠 T4)
- [x] aria-plugin 5 处版本文件 PATCH bump (v1.23.0 → v1.23.1):plugin.json (SoT) / marketplace.json / VERSION / CHANGELOG.md / README.md
- [x] 主仓 `VERSION` 更新插件版本记录 (per CLAUDE.md 版本发布检查清单 "主项目" 段)

## T7 — Phase C ship

- [x] aria 子模块:feature 分支 → PR (`_status.py` + `openspec.py` + `requirements.py` + tests + SKILL.md + 版本文件)
- [x] pre-merge gate (Rule #8) — aether 不可用时按 `.aria/config.json` fallback
- [x] Aria 主仓:submodule 指针 bump PR + 主仓 VERSION
- [x] 多远程推送 (origin + github) + post-push SHA 校验

## T8 — Phase D archive

- [x] proposal.md Status → Complete,归档到 `openspec/archive/{date}-state-scanner-status-extraction-range/`
- [x] aria-plugin #50 关闭 (附 PR 链接)
- [x] memory 同步 (本仓不使用 UPM);Rule #9 handoff 由 phase-d-closer D.3 评估触发条件 — 单 cycle bug-fix 通常豁免
