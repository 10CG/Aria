---
track-id: a1-entry-claim-duplicate-work-guard
owner-container: simonfish/023236f2
phase: C.1 (字段 Spec B 完成 + 本地合并态; C.2 推送/PR 待 owner 授权)
status: active
updated-at: 2026-09-02T08:26:00Z
---

# Aria — Session Handoff (2026-09-02) — 字段 Spec `linked-issue-field-availability` B.2 实施完成 (aria v1.68.0 本地合并态) + 架构文档 2.0.1 复审

> **一句话**: owner 选「1+2」→ 【2】架构文档复审校准 (master 本地 `c423281`) + 【1】字段 Spec 全程 B: B.0 闸门放行 → 三仓 feature 分支 → 测试席 48 条 RED (baseline ImportError) → 实现席 GREEN → 模板 / spec-drafter 两 hunk / 注册 → Rule #6 AB (ship 态 12/12 vs 12/12 零判别, 对照组 基线 3/5·4/5 vs 5/5·5/5, 无 WITHOUT_BETTER) → 回归 1457 + 1889 全绿 → v1.68.0 版本面 + CHANGELOG → aria/standards **本地 --no-ff merge + tag** → 主仓 gitlink + 14 版本点 + 状态回写。**全部未推**: aria master `fe32441` (4 ahead, tag v1.68.0) / standards master `fad8b4b` (2 ahead) / 主仓 feature 分支 `df42891` (8 ahead) + master `c423281` (1 ahead) —— 推共享 master 与建 PR 均为外向动作, 待 owner 一句授权。
> **B 期技术裁定 7 条** (parents[4] 勘正 / 矩阵 3 条豁免 / SC-3(a) 理据待勘正 / standards 不版本化 / #117 归并 / NO_PUSH 前置不适用 / AB 基线两泄漏通道) 已追记决策单 2026-09-01。**产品级待 owner: 零** (只剩推送授权这一动作门)。

> **Status**: Active — Ready for next session
> **Cycle period**: 2026-08-31T14:26Z → 2026-09-02T08:26Z
> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` 自动恢复 → §6 选择下一步

---

## §0 入口 (新 session 优先读)

1. 运行 `/aria:state-scanner`; Phase 1.15 会 surface 本 doc。主仓工作树停在 `feature/linked-issue-field-availability` (不是 master), aria / standards 子模块各停在**本地 master** (post-merge SHA, 与 gitlink 一致); `git status` 只应见 ` M aria-orchestrator` (有意停泊)。
2. **第一件事 = 拿 owner 推送授权** (§2 H1), 拿到后按 §6 第 1 条顺序做: 先两子模块双推 + 逐 remote `ls-remote` + tag 推 → 再主仓 feature 分支推 + PR (TASK-025, `phase-c-integrator` C.2.4 显式 `--main-branch master`) → 最后 master `c423281` 推。**任何一步都不要 force。**
3. 排版硬约束不变: **禁用带圈数字等小字形** (memory `no-tiny-glyphs`)。

---

## §1 已完成 (按时间顺序, UTC)

| 时间 | 事件 | Commit / 落点 | 备注 |
|------|------|-------------|------|
| 06:31 | `/aria:state-scanner`: 四仓 parity equal @ `e1deaf1`; 发现 08-31 handoff §6 第 1 件 (H1–H6) 已于 09-01 落版, latest.md 陈述过时 | — | 推荐 feature_with_spec (88%) → owner 选「1+2」 |
| 06:41 | **B.0** `phase1_gate.py --raw-track-id a1-entry-claim-duplicate-work-guard-023236f2 --phase B --mode advisory --linked-issue 10CG/Aria#174` ⇒ passed, claim `s-0873@0641`, push_success | 遥测 production +1 | linked_issue_overlap 列出本容器两条更早 claim (同轨两名, 已知) |
| 06:5x | **【2】架构文档复审**: `.claude/skills|agents` → `aria/skills|agents` 类级勘正 / 版本表 / §3.1 树 / §4 / §6.5 基准 / §9.2 M6 现状 + M7 / §9.3 / 2.0.1 | 主仓 **master** `c423281` (45+/83−) | `m6-arch-doc-stale` 98d → 0d; 落 master 非 feature (独立 doc-update 交付) |
| 07:0x | **B.1**: standards 本地 master 陈旧 (faaede2 ⊂ 334c609) 先 ff; 三仓 `feature/linked-issue-field-availability` (主仓基 origin/master) | — | memory `stale-local-main` 实证 |
| 06:52 | TASK-012 `${CLAUDE_PLUGIN_ROOT}` 实测: Phase 1.11 子进程 **UNSET**, 两法一致, 只落审计轨 §4 | 主仓 `66556e1` | 临时 check 撤除后 diff 为空 |
| 07:2x | **TASK-001–006** 测试席 (fresh subagent, 契约文件同源): 48 test / 13 `_bad_*` 矩阵; baseline `ModuleNotFoundError` | aria `673ad34` (含下行) | 席位上报 3 处规格出入 (parents[3]→[4] / SC-3(a) 理据 / 矩阵「每条」不可满足) |
| 07:3x | **TASK-007–009** 实现席 (fresh subagent, 同契约): lib 157 行 + 探针 195 行; 45/48 → 文档三 hunk + TASK-011 注册后 **48/48**; 实跑 `OK (9 份在范围内, 6 条在册)`; `--emit-arg` 母 Spec ⇒ `10CG/Aria#174` 逐字节 | aria `673ad34` / `b47fe11`; standards `91096f4`; 主仓 `daac6a9` | **CRLF 事故**: 模板 + SKILL.md 首次编辑被 Python 写成 LF (整文件 diff), diffstat 抓出后恢复 |
| 07:4x–08:2x | **Rule #6 AB** (TASK-016/017/018/019): PREDICTION 先写 → 6 run (3 eval × 2 臂) → 独立 grader → 发现基线经同批新模板合规 → 模板临时回 334c609 补 2 条对照 run → grader 追评 → RESULT / SUBSTITUTE; **aria-plugin#117 comment 20573** (GET 回读核验) | 主仓 `989d14c` (55 文件) | 协调 ref 远端/本地 `ab1d3e05` 零移动 |
| 08:0x | **TASK-020**: `run_tests.py` Ran 1457 OK; 静态 `def test_` 1425→1473; `run_all_tests.sh` 9 套件 OK / 1889; 零改动断言 (collision / SKILL.md / 两既有探针 / `__init__`) 为空; audit-engine 无 `lib/` `collectors/` | — | |
| 08:1x | **TASK-021** v1.68.0 版本面 (plugin.json SOT / marketplace ×2 / README / VERSION 账本 177 行 / CHANGELOG / 探针 `<vNEXT>` 回填) | aria `8eb8876` | 并发 ship 检查: 三端 master 仍 d69091d ⇒ 号 = 1.68.0 |
| 08:2x | **TASK-022/023 本地部分**: stale-local-main 守卫 (三端一致) → aria `--no-ff` merge **`fe32441`** + tag **v1.68.0**; standards merge **`fad8b4b`**; **未推** | 子模块 master | 硬约束 1 (本地 merge) 满足; 硬约束 2 (ls-remote) 待推后执行 |
| 08:21 | 主仓 gitlink ×2 同一 commit; **TASK-024** 14 版本点 → 1.68.0 (badge / 主项目版本 / i18n 三 check OK) | 主仓 `e5947fe` / `42f0292` | |
| 08:22 | 状态回写: tasks.md 22/25 `[x]` (5.3/5.4 注记本地合并态; 5.6 待 PR) / yaml 22 done · 2 in_progress · 1 pending / proposal Status 行追加 | 主仓 `df42891` | |

**Cycles shipped this session**: 0 (C.2 推送 + PR + D 待授权后走)

---

## §2 未完成 / Carry-forward 清单

### 高优先级 (owner 动作门)

| # | 项目 | scope | 来源 |
|---|------|-------|------|
| **H1** | **推送授权** (四处, 全部外向): (a) aria master `fe32441` + tag `v1.68.0` 双推 + **逐个** `ls-remote origin/github master` 与 `git -C aria rev-parse master` 三者一致 (**不要** `--tags` 全量推; 只推 `refs/tags/v1.68.0`); (b) standards master `fad8b4b` 双推 + ls-remote; (c) 主仓 feature 分支推 origin → **TASK-025** PR (`phase-c-integrator`, C.2.4 gate 显式 `--main-branch master`; body 列 2.6 实测 / B1–B7 裁定指针 / SC-3(a) 理据勘正待回写); (d) 主仓 master `c423281` (架构文档) 推; push 显式给足超时 (memory `partial-push`) | 授权一句话 + ~0.5h 执行 | 硬约束 1/2, memory `sync≠push-auth` |
| **H2** | ship 顺序第二份: **`sibling-spec-probe` B.1** —— 硬前置 (aria 双远端含 `lib/linked_issue_field.py`) 在 H1(a) 之后解除; 其 TASK-001 起点 | 下一 cycle | 2026-09-01 决策单 §H1b |

### 中优先级 (技术级, AI 可自裁; 多为 Level 1)

| # | 项目 | 状态 | 备注 |
|---|------|------|------|
| M1 | proposal `linked-issue-field-availability` 两处理据勘正: SC-3(a)「整串直喂归一判不可解析」实测不成立 (返回 `('b', 2)`); R5/C1「不改预览骨架字段大概率缺失」被 3 个基线 run 反证 (它们靠读模板/在制 proposal 写出字段) | pending | 决策单 B3 + RESULT §2-3; 下次触碰 proposal 时同批改 |
| M2 | **AB 基线污染两通道** (同批 co-landing SOT 文档 / 在制 proposal 语料) → `AB_TEST_OPERATIONS.md` §场景 1 补第二、三类污染面 (Level 1 docs) 或 aria-plugin#116 追记评论 (外向, 待授权) | pending | RESULT §4; memory `ab-baseline-leaks-via-repo-corpus` |
| M3 | `standards/conventions/version-management.md:254`「standards-v2.1.0 独立版本」与仓实况 (无 VERSION / CHANGELOG / tag) 不符 — standards 文档漂移 (Level 1) | pending | 决策单 B4 |
| M4 | `spec-drafter/SKILL.md` A.1.4 与预览块路径 `standards/openspec/changes/{feature}/` 与 Rule #5 矛盾 — **5 个评测 run 各自独立发现并 override** | pending | 不在本 Spec scope; Level 1 候选 (改后须 Rule #6 重判) |
| M5 | eval id 3 prompt「不要运行 git 或任何脚本」被两个基线 run 解读为「只读可跑」; 下次 AB 前把 prompt 收紧成可判字面 | pending | RESULT §4 违约记录 |

### 低优先级 / cleanup

- `ab-results/latest` 指针按近期惯例未动 (仍指 05-13); `ab-workspace/2026-09-02-linked-issue-field-rule6/` 为 gitignored 本地产物 (含 skill 快照), 可清。
- `.aria/workflow-state.json` 留 `phase C in_progress` (resume 时接 C.2); Layer L claim `s-0873@0641` active, 归档 (D.2b) 时 release。
- MEMORY.md 24.27KB 贴上限 (24.4KB); 下次新增前先移 archive。
- 探针 Spec `sibling-spec-probe` / 母 Spec 的 proposal 里引用「字段 Spec ship 后」的分支 (`--emit-arg` 两阶段取法) 在 H1 后自动成立, 无需改文。

---

## §3 关键风险 / 已知陷阱

| 风险 | 触发条件 | 缓解 / workaround |
|------|----------|-------------------|
| **CLAUDE.md / README / VERSION 在 feature 分支上已写 v1.68.0「已 ship」**, 但 v1.68.0 尚未推到任何远端 | 有人在 feature 分支上读「已 ship」当真; 或 `plugin-cache-currency` 在该分支 scan 报 STALE (installed 1.67.2 < SOT 1.68.0) | 这是 PR 合并时刻的目标态; 合并前以 master 为准; 合并后 owner 需 `/plugin update` 刷缓存 (与 08-30 H6 同形) |
| **半推 = 镜像分叉** | H1 四处推送任一只成一端 | 每处推后 `ls-remote` 逐 remote 核验; 显式超时; 分叉处置见 memory `partial-push` |
| **本地 master 陈旧** | standards 本地 master 曾落后 origin 1 commit (faaede2), 本 session 已 ff; aria 曾 == | 每次 merge 前重跑三端 rev-parse 断言 (memory `stale-local-main`) |
| **AB 结论已降级**: 定向 fixture 对 ship 态「只换 skill」无判别 (基线靠模板/在制 proposal 学会); 对「落地前世界」+3 | 有人引用 RESULT 说「skill hunk 有区分力」 | RESULT §2 两句并列; 不事后收紧断言 |
| **CRLF 文件**: `standards/openspec/templates/*.md` 与 `aria/skills/spec-drafter/SKILL.md` 是 CRLF | 脚本化编辑用 text 模式 ⇒ 整文件 LF 重写 | 编辑前 `git show HEAD:<f> \| grep -c $'\r$'`; 写后看 diffstat 是否 N+/0− (memory `preserve-crlf`) |
| **远端 master 已前进** (882707f, aria-runner-bot 07:23Z, M6 台账) | 本 session 起点 e1deaf1; feature 分支落后 1 | 零重叠已核 (`comm` 两侧文件集交集为空); master 侧已 rebase; feature 侧 PR 时由 Forgejo merge 处理, 若要 rebase 须同步改 handoff 内 SHA |
| 两条更早的同轨 claim (`a1-entry-claim-duplicate-work-guard` 无后缀, s-26ad / s-6389) 仍 active | 看板显示同轨三 claim | 同容器同 owner, advisory 无碍; D.2b release 时按 track_id 两种串各 release 一次 |

---

## §4 实战教训 (memory 沉淀来源)

- **AB 基线的输入面不止 skill 文件** (→ memory `ab-baseline-leaks-via-repo-corpus`): 旧 SKILL.md 链到的 SOT 模板是本 Spec 同批改的; pin 回旧 SHA 后基线又从在制 proposal 的 house style 学到字段。authoring 类 eval 在真仓里天然靠模仿语料能过 —— 「区分力」结论要拆成两句。
- **CRLF 静默转换** (→ memory `preserve-crlf`): diffstat 63+/57− 这种「插几行却全文件」的形状是唯一信号, 差点把 6 行 hunk 变成 438 行 merge 冲突面。
- **两席同契约互为对方的规格检查**: 测试席按契约写、实现席按契约 + 测试写, 双方独立读同一份契约文件; 测试席抓出 yaml `parents[3]` 差一层与 proposal SC-3(a) 理据错误, 实现席零矛盾上报 —— 「换人执笔」在代码期同样有效 (承 memory `fix-writer-bottleneck`)。
- **手写「主仓根」层数必须逐段核算**: A.2 派生的 `parents[3]` 在四个同目录既有测试全用 `parents[4]` 的情况下仍写错; 一处 off-by-one 会让两条 SC 恒 skip (memory `no-code-host-no-assertion` 的又一形态)。
- **贴文证据再失真**: grader 抓出基线 run 的 grep「0 hits」实跑 5 命中、行号恒差 40 —— memory `pasted-evidence-is-derived` 第 N 次实证, 这次是评测产物侧。

---

## §5 多维度同步状态

| 维度 | 本 session 涉及? | 状态 | 备注 |
|------|------------------|------|------|
| UPM (进度) | no | 未配置 | consistency_check 9 条 `active_change_not_in_upm` 恒亮 (UPM 未配置, 不适用) |
| User Stories | no | — | |
| OpenSpec | yes | 字段 Spec proposal Status 行 + tasks.md 22/25 + yaml 状态回写; 母 / 探针 Spec 零改动 | 归档待 C.2 后 phase-d-closer |
| PRD | no | — | |
| Standards / conventions | yes | `openspec/templates/proposal-minimal.md` +6 行 (standards master `fad8b4b`, 未推) | M3 版本化漂移待另开 |
| Skill docs | yes | `spec-drafter/SKILL.md` +19 行; `state-scanner/SKILL.md` **零改动** (`:508` 承诺) | `aria/CHANGELOG.md` 1.68.0 |
| Auto-memory | yes | 2 new + 索引压缩 (3 条移 archive) | 见 §8 |
| Decision memos | yes | `2026-09-01-a1-entry-h1-h6-…-split.md` 追记 §B 期 B1–B7 | 主仓 `989d14c` |
| Audit reports | yes | `linked-issue-field-availability-audit-trail.md` §4 (TASK-012) | 主仓 `66556e1` |
| CHANGELOG | yes | aria `## [1.68.0] - 2026-09-02` | aria `8eb8876` |
| 架构文档 | yes | `system-architecture.md` 2.0.1 | 主仓 master `c423281` (独立交付) |

---

## §6 Next session 入口 + 优先级建议

```bash
/aria:state-scanner
```

1. ⭐ **`{id: a1-entry-claim-duplicate-work-guard}`** — 拿 owner 推送授权后按序执行 H1 (a)→(b)→(c)→(d): 子模块双推 + tag + 逐 remote ls-remote → 主仓 feature 推 + TASK-025 PR (phase-c-integrator C.2.4, `--main-branch master`; body 见 yaml TASK-025 verification) → merge 后 `ls-remote` 两端一致 → `phase-d-closer` 归档字段 Spec + release claim → owner `/plugin update` 刷到 1.68.0。类型: C.2 + D, ~1h。
2. **`{id: carry-b1-entry-probe-spec}`** — `sibling-spec-probe` 进 B.1 (硬前置 = aria 双远端含 fe32441; 其 TASK-001/003 前置见其 yaml); 同族第二份, ship 号按当时 plugin.json 计算 (1.69.0 若无并发 ship)。类型: B.1, ~1h。
3. **`{id: carry-ab-baseline-contamination-followup}`** — M2: `AB_TEST_OPERATIONS.md` §场景 1 补两类污染面 (Level 1) + 视授权追记 #116。~0.5h。
4. **`{id: carry-spec-drafter-path-rule5-drift}`** — M4 + M1 + M3 三条 Level 1 勘正可合一批 (各自独立 hunk, Rule #6 对 A.1.4 路径 hunk 重判)。~1h。

**不应该做的**:
- 不要 force push 任何 remote; 不要用 `--tags` 全量推 aria; 不要在主仓直接 merge feature 到 master (走 PR + Rule #8 gate);
- 不要 `git add aria-orchestrator` (仍有意停泊 @ 92acce5);
- 不要重跑 AB iteration-2 除非改了 hunk A/B 文本; 不要事后收紧 eval 3 断言 (predict-then-measure);
- 不要把 feature 分支上的「v1.68.0 已 ship」当作已发布 —— 三端 master 仍是 d69091d / e1deaf1 / 334c609 直到 H1 完成。

---

## §7 提交清单 (commit hash + multi-remote parity)

```
[main]      feature/linked-issue-field-availability = df42891 (8 commits: 66556e1 daac6a9 989d14c e5947fe 42f0292 df42891 + 本 handoff) | 未推 (origin/github master = e1deaf1)
[main]      master = c423281 (1 ahead of origin/master 882707f: 架构文档 2.0.1, 已 rebase 到 882707f) | 未推
[main]      ⚠️ origin/github master 已被 aria-runner-bot 推进到 882707f (07:23Z, M6 台账/TASK-028, 与本轨零文件重叠); feature 分支基 e1deaf1 落后 1, PR 合并即可 (未 rebase 以保 §1/§7 SHA 有效)
[aria]      master = fe32441 + tag v1.68.0 | origin = github = fe32441 ✅ (owner 授权 08:3xZ 推, ls-remote 逐 remote MATCH; tag 两端 present)
[standards] master = fad8b4b                                                          | origin = github = fad8b4b ✅ (同上核验)
[aria-orchestrator] 未动 (feature/m6-cost-model-telemetry 92acce5 停泊; gitlink 237045a)
```

**Tags published**: v1.68.0 (aria, origin + github)。**PRs merged**: 无 (TASK-025 待)。**Issue 动作**: aria-plugin#117 comment 20573 (已回读核验)。

---

## §8 Memory entries this session (2 new + 1 索引压缩)

| File | Type | Theme |
|------|------|-------|
| `feedback_ab_baseline_leaks_via_co_landing_docs_and_repo_corpus.md` | feedback | AB 基线臂从同批 SOT 文档 + 在制 proposal 学到目标行为; 区分力结论拆两句 |
| `feedback_preserve_crlf_when_scripted_editing.md` | feedback | 仓内 CRLF 文件被 Python text 模式静默转 LF; diffstat N+/0− 核验 |
| MEMORY.md | index | 24.8KB → 24.27KB: `selfcheck-values-not-questions` / `assertion-swap-severs-link` / `rewrite-discards-fixes` 移入 MEMORY-archive.md |

---

## Cross-references

- 决策单 `.aria/decisions/2026-09-01-a1-entry-h1-h6-technical-rulings-product-vs-technical-split.md` (§B 期追记 B1–B7)
- AB 结果 `aria-plugin-benchmarks/ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/` (PREDICTION / RESULT / SUBSTITUTE / benchmark ×2)
- 审计轨 `.aria/audit-reports/linked-issue-field-availability-audit-trail.md` §4
- Spec: `openspec/changes/linked-issue-field-availability/{proposal,tasks}.md` + `detailed-tasks.yaml`
- aria-plugin#117 comment: https://forgejo.10cg.pub/10CG/aria-plugin/issues/117#issuecomment-20573
- 上一份: `docs/handoff/2026-08-31-a1-entry-a2-a3-landed-post-planning-r4-converged.md` (本 doc 接替其 Latest 指针)

---

**Created**: 2026-09-02 08:26Z
**Session duration**: ~2h (06:31Z → 08:26Z)
**Status**: Active — 下个 session 第一件事 = owner 推送授权 → C.2 + PR → D
