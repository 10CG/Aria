# Aria — Ten-step cycle: add session-handoff stage (read at start + write at end)

> **Level**: 2 (Minimal — multi-file structural change, +/-doc-heavy, ~19h)
> **Status**: **Complete** 2026-05-15 (Phase A+B+C+D shipped) — R1+R2 SCOPE_OK_R2 (A.2) + pre_merge R1 SCOPE_OK_R1 (B.3) + 3-PR sequenced merge (standards #4 / aria-plugin #46 / Aria #105) + aria-plugin v1.21.0 release. Closes Forgejo Aria #92.
> **Change ID**: `aria-ten-step-session-handoff-stage`
> **Trigger**: Forgejo Aria [#92](https://forgejo.10cg.pub/10CG/Aria/issues/92) — ten-step cycle 缺 session 切换标准化阶段
> **Triage verdict**: `confirmed/minor/next-cycle` ([issuecomment-6170](https://forgejo.10cg.pub/10CG/Aria/issues/92#issuecomment-6170))
> **Dogfood evidence**: 4 incidents (SilkNode 2026-05-09 + Aria self-scan 2026-05-13 ×3 含本 session)
> **Target release**: aria-plugin **v1.21.0** MINOR
> **Created**: 2026-05-13

---

## Why

aria 十步循环目前 **A.0 状态扫描** 之前**没有标准化** "读上次 session handoff" 的步骤,**D.2 归档** 之后**没有标准化** "写本次 session handoff" 的步骤。实战 dogfood 4 起表明:

### 痛点 1: session 开始 AI 看不到 carry-forward 优先级

`/aria:state-scanner` v3.0 snapshot 不含 handoff 字段。AI 拿 snapshot 给推荐就会**错过用户上 session 写的下一步建议**。

**实证**:
- **SilkNode 2026-05-09** (#92 原文): AI 看到 main clean + 44 ready stories → 推荐 "随便挑一个 ready" → 用户反问"你是不是没读交接文档" → AI 才读 `docs/handoff/2026-05-09-session-handoff.md` → handoff §6 明确写 "US-095 first, US-097 是 dead path"
- **Aria self 2026-05-13** (本 session): AI 跑完 state-scanner 直接出推荐,用户问"有查看 handoff 文档吗?" → AI 才读 `docs/handoff/latest.md` + `.aria/handoff/2026-05-13-issue-101-cycle-closeout.md` → §3 H0 写明本 cycle 是优先级 #1

### 痛点 2: session 结束写 handoff 是 ad-hoc,格式不统一

`docs/handoff/` 自发演进出 8 段模板 (TL;DR / 已完成 / 未完成 / 风险 / 教训 / 4 维度同步 / next-session 入口 / 提交清单),但**不是 aria 规范一部分**。phase-d-closer 不提示写 handoff,触发条件未定义,导致:
- 某些 cycle 写了 handoff,某些没写
- 不同项目演进出不同格式,无法跨项目复用经验

### 痛点 3: Aria 自身存在 handoff 路径漂移

Aria 项目本身**同时存在两个 handoff dir**:
- `docs/handoff/` 8 files (May 8-13)
- `.aria/handoff/` 6 files (Apr 23-25 + 1 来自 May 13 #101 closeout)

没 canonical 决策时,即使是 spec 作者本人也会漂移。`docs/handoff/latest.md` pointer 在 May 13 因写入 `.aria/handoff/` 而 stale。**这正是本 spec 必须含"自动纠正机制"的根源** — 即使锁定 canonical,缺主动 enforcement 仍会漂。

---

## What

### In scope (7 tasks)

#### Canonical location 决策

**Canonical = `docs/handoff/`**,`.aria/handoff/` 标记 forbidden。理由 (brainstorm 锁定):

1. `.aria/` namespace 语义是**机器状态** (JSON / cache / audit log / workflow-state),`.gitignore` 已 ignore 5 项 `.aria/*` 都是生成物
2. `docs/` 是**人类/AI 可读 prose**,handoff 是人写给下次 session 读的散文
3. Forgejo #92 issue body T1 显式选 `docs/handoff/*.md`
4. SilkNode 等下游已采用 `docs/handoff/`,跨项目一致性

#### T1 — `collectors/handoff.py` + snapshot field (Layer 2)

新增 `aria/skills/state-scanner/scripts/collectors/handoff.py`:
- 扫 `docs/handoff/*.md` mtime 排序,latest path + age_hours
- 检测 `.aria/handoff/*.md` 存在 → `misplaced_files: [paths]` 字段
- **schema 保持 1.0** (additive top-level field 无需 bump,对齐 v1.18.0 G2/G3/G4 precedent;F1 fix per R1 backend-C1 + qa-C1)
- snapshot 不读 handoff body (避免膨胀),只暴露 path
- `age_hours` 使用 `time.time() - mtime` (UTC epoch float),避免 timezone/DST 陷阱

#### T2 — `phase-d-closer` D.3 session-handoff step + template

Phase D 加 **D.3 session-handoff** (可选触发):
- **触发条件** (任一满足):
  - session 跨度 > 4h *(measured via `.aria/workflow-state.json::session.started_at` if active,fallback 见 tasks.md T2.2)*
  - 本 session 完整 ship ≥ 2 个 US/cycle *(measured via `git log` since last handoff doc mtime)*
  - 本 session 跨 ≥ 2 个 phase *(measured via phase markers in commit messages)*
- **Fallback 信号缺失时**: prompt user "本 session 是否符合 D.3 触发条件?",default `yes` if Phase D 执行到 D.2 archive 成功
- **模板**: `aria/templates/session-handoff.md` (**9 段骨架**,参考 Aria 实战版,F4 fix per R1 knowledge-M1)
- **输出路径**: **硬编码** `docs/handoff/{YYYY-MM-DD}-{slug}.md` (Layer 5: template hardcode)
- **命名 deterministic**: 同日多 session 用 `{YYYY-MM-DD}-{HHMM}-{slug}.md`
- 写完后自动更新 `docs/handoff/latest.md` pointer

**9 段结构** (F4 — 加 §8 Memory entries):
§0 入口 + §1 已完成 + §2 未完成/carry-forward + §3 关键风险 + §4 实战教训 + §5 4 维度同步 + §6 next session 入口 + §7 提交清单 + **§8 Memory entries this session** (auto-memory 新增列表 — 实证 必含 per real-world handoff)

#### T3 — PreToolUse hook (Layer 1: 写入阻断)

新增 `aria/hooks/handoff-location-guard.json`:
- 匹配 PreToolUse: tool_name ∈ {`Write`, `Edit`, `NotebookEdit`}
- Path matcher: **regex on resolved absolute path** `r"^(?:.+/)?\.aria/handoff/[^/]+\.md$"` (F3 fix per R1 backend-M2 — glob 改 regex 防 relative/absolute 歧义,防 nested path 误拦如 `something/.aria/handoff/foo.md` 类配置库)
- Symlink: hook 解析 `realpath` 后再 match (防绕过)
- 报错: "Handoff docs must be written to `docs/handoff/` (canonical per `standards/conventions/session-handoff.md`). `.aria/handoff/` is forbidden."
- AI 见 error → 自动重定向到 `docs/handoff/`
- **不拦截 Bash 工具** (T6 migration 用 `git mv` 经 Bash,不经 Write/Edit,故不自阻塞)

#### T4 — `RECOMMENDATION_RULES.md` handoff_drift rule (Layer 3: 推荐降级)

state-scanner Phase 2 见 `handoff.misplaced_files != []` 时,优先推 "迁移漂移文件" 工作流。优先级在 `audit_unconverged` 之下,在常规工作流之上。

#### T5 — `standards/conventions/session-handoff.md` (Layer 4: Convention SOT)

新增 convention 文档,结构同 Rule #7 (`secret-hygiene.md`):
- §1 Rule: canonical `docs/handoff/`,forbidden `.aria/handoff/`
- §2 Template 9 段定义 + 触发条件
- §3 Enforcement matrix (L1-L5 哪层负责什么)
- §4 Exception (零 — 无 exception)
- §5 Source incidents (4 dogfood 实证,对齐 Rule #7 incident 引用 pattern)
- §6 Migration notes (downstream projects 升级路径)

**CLAUDE.md Rule #9 同步激活**: 本 cycle 直接加入 Rule list (F5 fix per R1 knowledge-M2 — align Rule #7 / #8 precedent at ship time;4 dogfood ≥ Rule #7 (2) / Rule #8 (1) 实证数量,延迟无依据)。新 task T5.4 落实。

**CLAUDE.md 信息地图同步更新**: 目录导航表加 `docs/handoff/` 和 `standards/conventions/session-handoff.md` 入口 (F6 fix per R1 knowledge-m3 — 文档同步原则 #3)。新 task T5.5 落实。

#### T6 — 迁移 6 个 `.aria/handoff/*.md` 到 `docs/handoff/`

```bash
git mv .aria/handoff/*.md docs/handoff/        # 6 files
# 更新 docs/handoff/latest.md 指向真正最新 (2026-05-13 #101 closeout)
git rm -r .aria/handoff/                        # 删空 dir (history preserved by mv)
```

迁移后 `.aria/handoff/` 不存在 → L1 hook 触发的是"新建" 行为,语义清晰。

#### T7 — Tests + dogfood

- Unit tests for `collectors/handoff.py`: mtime sort / age_hours / misplaced detection / additive field (snapshot 仍 schema 1.0)
- Hook smoke test: 模拟 Write to `.aria/handoff/foo.md` → 期望 blocked
- Phase-d-closer template generation test (手动 fixture)
- **Dogfood**: 本 cycle Phase D 写 closeout handoff → `docs/handoff/2026-05-XX-h0-cycle-done.md`,验证 D.3 流程

### Out of scope

- **T3 独立 skill `aria:session-bridge`** (#92 原文 §T3) — 推后续 cycle,本 cycle T1+T2+5 层 enforcement 已足够
- **跨项目 handoff dir migration** — 本 cycle 仅 Aria 自身,SilkNode 等下游 v1.21.0 升级后自动受益于 collector + hook
- **修改模板内容设计** — 沿用 Aria 实战版结构,本 cycle 不重构 template 章节内容,只规范化 9 段骨架到 `aria/templates/`
- **handoff doc 自动归档** (例如 >30 天移到 `docs/handoff/archive/`) — 不在本 cycle,后续 cycle 评估
- **D.3 触发条件机械自检** — 当前用 fallback 启发式 + user prompt,后续 cycle 评估是否加 `interrupt.session_age_seconds` 反推

### Layered defense matrix

| Layer | 机制 | 触发时机 | 实施位置 | 失效时谁兜底 |
|-------|------|----------|----------|--------------|
| L1 | PreToolUse hook 阻断 `.aria/handoff/*.md` 写入 | AI 写入时 | `aria/hooks/handoff-location-guard.json` | L2 detect + L3 推荐 |
| L2 | scan.py 检测 `.aria/handoff/*.md` 存在 → `misplaced_files` | 每次 `/state-scanner` | `collectors/handoff.py` | L3 surface 给 AI |
| L3 | state-scanner 推荐 "迁移漂移文件" 工作流 | 推荐 Phase 2 | `RECOMMENDATION_RULES.md` | 人类 review |
| L4 | Convention SOT 文档化 canonical + forbidden | 引用源 | `standards/conventions/session-handoff.md` | 工具实施引用 |
| L5 | phase-d-closer 模板硬编码输出路径 | session 结束写 | `aria/templates/session-handoff.md` + `phase-d-closer/SKILL.md` | L1 hook 阻断异常 |

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | session 切换有标准化阶段,AI 不再漏读 handoff (痛点 1 解决) |
| **Positive** | handoff 格式统一,跨项目复用 8 段模板 (痛点 2 解决) |
| **Positive** | 5 层 defense-in-depth 防漂移,即使某层失效仍有 fallback (痛点 3 解决) |
| **Positive** | state-scanner snapshot.handoff 字段 surface latest doc,collector AB benchmark 可验证改进 |
| **Risk** | Additive `handoff` 字段在 schema 1.0 内引入,下游 consumer 若严格 schema validate 需识别新字段;缓解: 字段不在 schema enum/required 中,严格 validator 会 ignore unknown additive top-level keys (per Aria v1.18.0 G2/G3/G4 precedent) |
| **Risk** | PreToolUse hook 可能误拦其他工具写 `.aria/handoff/*.md` (理论上不存在,因 dir 已迁移删除);缓解: hook 仅匹配 `.aria/handoff/*.md` 路径 pattern,其他 `.aria/*` 不受影响 |
| **Risk** | phase-d-closer D.3 触发条件可能过于宽松 (4h + 2 US) 导致每次都写 handoff;缓解: 触发条件 v1 保守,后续观察后调整 |
| **Risk** | 8 段模板可能在某些极短 cycle (Level 1 quick fix) 显得过重;缓解: D.3 触发条件已排除此类场景 (≥2 US/cycle) |

---

## Tasks

详见 [tasks.md](./tasks.md)。简版:

- [ ] T1 — `collectors/handoff.py` + snapshot.handoff 字段 (L2)
- [ ] T2 — `phase-d-closer` D.3 step + template (L5)
- [ ] T3 — PreToolUse hook (L1)
- [ ] T4 — RECOMMENDATION_RULES.md handoff_drift (L3)
- [ ] T5 — Convention SOT `session-handoff.md` (L4)
- [ ] T6 — 迁移 6 个 `.aria/handoff/*.md` + 更新 latest.md pointer
- [ ] T7 — Tests + dogfood (Phase D 自身 handoff doc)
- [ ] T8 — Pre-merge audit + Rule #6 benchmark + Phase C ship + Phase D archive + v1.21.0 release

---

## Success Criteria

### Functional

- [ ] `python3 scripts/scan.py` 输出 snapshot 含顶层 `handoff` 字段,`snapshot_schema_version` 保持 `"1.0"` (additive field)
- [ ] `handoff.latest_path` 指向 `docs/handoff/` 中 mtime 最新 `.md`
- [ ] `handoff.age_hours` 是 float (基于 mtime → now)
- [ ] `handoff.misplaced_files` 在迁移后是 `[]`,如果 `.aria/handoff/*.md` 出现则非空
- [ ] state-scanner Phase 2 推荐展示 handoff path 与 age (output-formats.md 文档化)
- [ ] phase-d-closer D.3 在触发条件满足时,prompt AI 写 handoff,模板 fill 后写到 `docs/handoff/{YYYY-MM-DD}-{slug}.md`
- [ ] `docs/handoff/latest.md` pointer 写后自动更新到新 doc

### Enforcement (核心)

- [ ] L1 hook: 试图 Write/Edit `.aria/handoff/foo.md` → blocked,error message 包含 "must use docs/handoff/"
- [ ] L2 detect: 手动 `mkdir -p .aria/handoff && touch .aria/handoff/test.md` → 下次 scan `misplaced_files == ['.aria/handoff/test.md']`
- [ ] L3 推荐: snapshot 见 `misplaced_files != []` → state-scanner 输出 "迁移漂移文件" 作为推荐 [1]
- [ ] L4 convention: `standards/conventions/session-handoff.md` 存在 + 内容含 canonical rule + enforcement matrix
- [ ] L5 template: phase-d-closer 生成 handoff 时**不** prompt 选 dir,deterministic 写 `docs/handoff/`

### Migration

- [ ] 迁移后 `.aria/handoff/` dir 不存在 (`ls .aria/handoff/` → No such file)
- [ ] `docs/handoff/` 包含原 6 + 8 = 14 个 `.md` files (history preserved via `git mv`)
- [ ] `docs/handoff/latest.md` 指向真正最新 `2026-05-13-issue-101-cycle-closeout.md` (或迁移后 rename 的版本)

### Tests & Dogfood

- [ ] `aria/skills/state-scanner/tests/test_handoff.py` 全绿
- [ ] Hook smoke test 全绿
- [ ] Rule #6 benchmark: state-scanner with-handoff-collector vs without — structural metric `handoff field present in snapshot` delta = +100% (deterministic)
- [ ] **Phase D dogfood**: 本 cycle closeout 写 `docs/handoff/2026-05-XX-h0-cycle-done.md`,通过 D.3 流程产出,即第 5 次 dogfood 实证

---

## References

- Trigger issue: [Forgejo Aria #92](https://forgejo.10cg.pub/10CG/Aria/issues/92)
- Triage SOP: `openspec/archive/2026-05-13-aria-issue-triage-sop/` (just shipped)
- Triage record: `.aria/triage-92.json` (本 spec 来源 evidence)
- Triage comment: [#6170](https://forgejo.10cg.pub/10CG/Aria/issues/92#issuecomment-6170) `confirmed/minor/next-cycle`
- 实战 handoff 参考模板: SilkNode `docs/handoff/2026-05-09-session-handoff.md` (8 段结构)
- Aria 实战 handoff 参考: `docs/handoff/2026-05-13-us025-m5-phase-a-b1-done.md`
- 关联 spec (前置 surfacing 工作): `openspec/archive/2026-05-09-state-scanner-inter-cycle-surfacing/` (G2/G3/G4 collectors)
- 关联 #85: state-scanner v3.0 surfacing gap (4 项,本 spec 解 G3 handoff doc 指针)
- Rule #6 (CLAUDE.md): `/skill-creator` benchmark required for Skill logic modification
- Rule #7 reference (CLAUDE.md): `secret-hygiene.md` 的 convention + hook 双层结构是本 spec L1+L4 结构参考
- Rule #8 (CLAUDE.md): pre-merge gate required (aether fallback `skip_with_warning` applies)
