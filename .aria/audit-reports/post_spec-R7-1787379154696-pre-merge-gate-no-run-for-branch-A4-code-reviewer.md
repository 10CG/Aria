---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T11:40:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 0
minor_count: 1
---

# post_spec R7 (形式全票确认轮) — A4 code-reviewer 席 (spec↔代码逐行 / 引用稳定性 / 实施者分叉末扫)

审计对象: v7 (R6-fix) `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` (untracked, 无 git 史; v6→v7 对比以我 R6 报告记录的 v6 行号/原文为基准)。基线 aria @ `400f0bc` (`git rev-parse` 实核, 工作树干净, 与 R6 同)。本轮实读: `pre_merge_gate.py:292-300` (`_sanitize_for_json` = `encode("utf-8","replace").decode`, `feat/x` 回填后字面保留 ⇒ SC-5 (c2) 可满足) / `:449-471` (既有 2 kind = `main-branch-not-found` / `main-branch-verify-failed` ⇒ 2.3「kind 封闭集 4」成立) / `:544-556` (`--config-file` 缺省相对 cwd, 同 R6) · `gate_state_helper.py:104-162` (`_next_check_at` 按 `min(retry_count, len-1)` 取 intervals ⇒ SC-11(d) `[5,7]` 两次调用 next_check_at 可算; `is_first` / `clear_gate_state` 存在 ⇒ SC-13 `clear` 与 §3.1 `clear` = `clear_gate_state` 成立) · `test_pre_merge_gate.py:49-89` (`self.pc_eval.return_value` 可改 ⇒ SC-5 (c2) pc stub 带 `dispatchable_workflows` 可构造) · `workflow-runner/SKILL.md:332-358/:377-392` (2.5 abort 留 `status=waiting` 与既有 timeout abort 同形, 非新分叉) · `workflow-state-schema.md:128-132/:308-316` (§3.3 新 workflow 覆写整个 state 文件 ⇒ §3.1「终态可被下一 workflow 覆盖 = 新 episode」引用准确, `is_first` 跨 episode 不串计数) · `runtime-probe-declaration.md:54-56/:118` (partition 相对路径 / symbol 仅标签 / `source=="production"` ⇒ frontmatter 三字段合约一致) · 主仓 `CLAUDE.md:139/:141` `VERSION:24` `README.md:8/:242` `.gitignore:19-21` `config.template.json:73-91` (两 key 确缺) `config-loader/SKILL.md:283` `openspec-archive/SKILL.md:234` `DEC-20260702-001:124-128` `DEC-20260731-001-*` 存在 — §5 表全部主仓行号对当前树实核一致 · R5/R6 五席报告 (核 §7 与 Status 行引用的 finding ID)。

## R6 处置核对 (归我席: 簇 #1 共报 + 簇 #2 + 簇 #3 一项)

| R6 条目 | 簇 | 状态 | 证据 (实读 v7) |
|---|---|---|---|
| A4-R6-m1 (SC-5 (c) 与封闭表互斥; 3.5 清单漏) | #1 (与 A1-R6-M1 同题) | **closed** | SC-5 `:266` 拆 **(c1)** 「所有变体: message 不含字面 `<pr_branch>` 且 `raw_message == gate_error.message`」/ **(c2)** 「仅 `dispatch_viable=true`: enabled + pc stub trigger-matched 含 dispatchable + `DISPATCH_VIABLE=True` → 含 `feat/x`」+ 括注「其它档封闭表无占位符, 不得断言含分支名」— 与我给的修法逐字等价; §3.5 `:196` 删除清单补「SC-5 (c2) + 3.3 (a) 行 + §2.1 末段的 `<pr_branch>` `.replace` ((c1) 的「不含占位」断言保留作守卫)」✓。`_sanitize_for_json` 不动 `/` ⇒ (c2) 在正确实现下可绿; (c1) 对 `.replace` 漏做 / 副本漏同步两类坏实现各红 ✓ |
| A4-R6-m2 (`--state-file` 缺省未钉) | #2 (与 A1-R6-m4 同题) | **closed** | `:151`「**`--state-file` 必填无缺省**, 缺失 exit 2 — 与 `--source` 同形 fail-closed; Python API 默认 cwd 相对不变, 仅测试/复用面」; SC-11(d) `:272`「缺 `--source` 或缺 `--state-file` 各 exit 2」✓; synopsis 改 `--state-file <绝对路径>` ✓; §3.2 `:162` 的「显式传绝对路径」保留为调用点纪律, 与必填结构不矛盾 ✓ |
| A4-R6-m3 (Impact 漏 `reset_retry_count`) | #3 | **closed** | Impact `:253` 新函数清单 `… reset_no_run_observations reset_retry_count + CLI` ✓ |

小计: closed 3 / partial 0 / not_addressed 0。

### 非本席簇交叉复核 (只记事实, 供主控核「全部吸收」声明)

- 簇 #3 / **A1-R6-m1 有两半**: (i) `workflow-files-changed` 档 message 加 `branches` 成因 — v7 `:128` 已加 ✓; (ii) §3.3 处方 (b) 末尾加「若 message 提示 branches 过滤成因, 推 commit 无效, 改用 (a) 或改 workflow `branches:`」— v7 `:185` (b) 原文**未动** (仍「第二次 push 是普通 diff, paths 正常评」)。R6 聚合行 3 只登记了 (i) ⇒ 「全部吸收」对此条是**半吸收**。详见下方 m1 (判 minor, 不影响本席 vote)。
- 簇 #3 / A1-R6-m3 (SC-13 `clear`): `:274` 已加, 且 telemetry 行不随 `clear` 消失 (分区 append-only, `clear` 只置 `gate_state=null`) ⇒ 与 SC-16(c) 不冲突 ✓。
- 簇 #3 / A1-R6-m5 (§7 checklist): `:233-238` 四项; 引用 ID 逐一对上原报告 (A2-R5-m1 + A2-R6-m2 = 「A2-R5/R6-m」/ A3-R5-m1 / A5-R5-m1 / A2-R6-m1) ✓。
- 簇 #3 / A5-R6-m1/m2: Cross-refs `:307` 补 R3-R6 四个聚合指针; DEC 行 `:223` 前缀「主仓」✓。

## v7 13 处 diff 一致性 (引用 / 编号 / 行号 / 占位)

| 点 | 结论 |
|---|---|
| Status 行「R6 4 PASS / 1 REVISE (0C/1M …)」/ `rounds: 6` / owner_rulings 第三条 | 与 R6 聚合 frontmatter 一致; `rounds: 6` = 已完成轮数, R7 后应改 7 (叙述字段, 不核) |
| SC-5 (c1)(c2) ↔ 2.3 `:127` 唯一 `<pr_branch>` 槽位 ↔ 2.1 `:92` `.replace` ↔ 3.3 (a) ↔ 3.5 条件 scope | **一致** (v6 互斥已清) |
| 3.5 删除清单 (`.replace` 随 dispatch 行删) ↔ 2.1 `:91-93` 块其余两句 (`+ verify_note` / 副本重同步) ↔ SC-5 (d) / SC-10 verify-failed | 一致: 清单只点名 `.replace`, 其余两句由 SC-5(d)+SC-10 钉住 ⇒ 「整块删除」的坏实现必红 |
| CLI `:151` 必填 ↔ SC-11(d) ↔ §3.2 `:162/:164` 绝对路径 ↔ SC-13 `--state-file` 显式传 | 一致 |
| Impact `:253` ↔ §3.1 `:150/:153` 两个具名 reset helper | 一致 |
| 2.3 `:128` files-changed 档 `branches` ↔ `:127` trigger-matched 档 `branches` ↔ 3.3 (b) | message 两档一致; **3.3 (b) 未随动** → m1 |
| SC-13 `clear` ↔ §3.1 `clear` = `clear_gate_state` ↔ `--state-file` 必填 (主仓绝对路径) | 一致 |
| §7 四项 ↔ 各原报告 ID ↔ §6 格式 | 一致 |
| Cross-refs `:307` ↔ 聚合文件名前缀 | 一致 |
| DEC `:223`「主仓」↔ §5 表头「主仓 vs 插件分列」 | 一致 |
| SC-7 十一处行号 / §2.1 `:387-527` 五区间 / test `:85-89` `:363` / helper schema SKILL 行号 | 基线 SHA 未动, R6 实核结论沿用 ✓ |
| §5 主仓侧行号 (CLAUDE/VERSION/README/.gitignore/template/config-loader/archive SKILL/DEC) | 本轮对当前主仓树逐一 grep/sed 实核一致 ✓ (主仓近 5 commit 只动 handoff/gitlink, 未触及) |
| frontmatter `runtime_probe` 三字段 ↔ `runtime-probe-declaration.md:54-56` 合约 | 一致 (相对路径 / symbol 仅标签 / `source` 字段名) |

## 新 Findings

### 必须改 (Minor, 一行; 可与 A.2 转 tasks 同 pass 落)

#### [A4-R7-m1] Minor — R6 簇 #3 A1-R6-m1 (ii) 半边未吸收: 2.3 两档 message 已告知「`branches` 过滤不含本分支」成因, §3.3 处方 (b) `:185` 仍断言「第二次 push 是普通 diff, paths 正常评」

- 事实: `:127` / `:128` 两档 message 均含第三成因「`branches` 过滤不含本分支」; `:185` (b) 原文未变, 对该成因下「推 commit 必然无效」零提示。R6 聚合行 3 只登记 (i) 半边, v7 也只落了 (i)。
- 为什么只是 minor: (b) 是给人的处方文案, 人先看到 message 里的三成因再选处方; 不动 verdict / kind / 副本通道 / 键集, 不 fail-open; 两实施者分叉可见面 = (b) 是否多一句, 无 SC 区分但不满足 Major 四门槛。
- 修法 (A1 原句): (b) 末尾加「若 message 提示 `branches` 过滤成因, 推 commit 无效 — 改用 (a) 或修 workflow `branches:`」。

### 还能挑 (不要求改, 零权重)

- 2.2 `:114`「`cfg.get(key)`; 非 int / bool / <2 → warn + 回落 3」字面上把「缺键 (`.get` 返 None)」也归进 warn, 而 SC-3 `:264`「…/缺键→3, **前四者**各 warn 一次」暗示缺键不 warn。仅 `compute_verdict` 直调 `cfg={}` 时可见 (gate_check 路径恒合并 `DEFAULT_CONFIG`, 缺键不可达); SC-3 测试若断言 warn 计数即单向收敛。一词修: 2.2 加「缺键/None → 静默 3」。我 R4 曾判两处一致, 本轮逐字再读才见此缝, 记录备 A.2 裁量。
- SC-5 (d)「message **末尾**含『核验失败: boom』」: 2.1 `:88` 附注格式为 `" (PR 分支存在性核验失败: {detail})"`, 真末尾是 `)`; 用 `in` 断言无事, 用 `endswith` 会红。测试作者与格式作者同一人, 不构成分叉。
- 2.5 `abort` 留 `gate_state.status=waiting` (与既有 timeout abort `:356` 同形, resume 入口 `:379` 会再 poll 一次) — 既有形状, 非本 spec 引入, 不报。

## 实施者分叉点末次扫描 (Major 门槛)

逐条过四门槛 (错误 verdict/kind · fail-open · 既有契约破坏 · 两实施者必然分叉且无 SC 区分): `.replace` 删除范围 (SC-5(d)/SC-10 钉住) · `--state-file` (必填, 结构消歧) · SC-5 (c2) pc stub (mixin `return_value` 可改) · `DISPATCH_VIABLE` 读法 (§7 钉裸全局) · `record` 缺失文件 × verdict (`:153` 钉 + §7 补单测) · 缺键 warn (直调路径, 零生产可见) · (b) 处方句 (人读文案)。**无一满足 Major**。

## Verdict

**PASS** (0 Critical / 0 Major / 1 Minor) — **vote: PASS**

归我席 R6 三条 minor 全部逐字吸收 (3 closed / 0 partial / 0 not_addressed)。v7 13 处 diff 在本席核查面 (引用 / 编号 / 行号 / 占位) 零新矛盾; v6 唯一 Major (SC-5 互斥) 的修法与 §3.5 条件 scope、2.1 回填块、mixin 打桩能力、`_sanitize_for_json` 行为四面互证可实现。唯一新 minor 是 R6 簇 #3 一条两半式 finding 的半边漏吸收 (处方 (b) 未随 message 新增的 `branches` 成因更新), 一句话修, 不触 verdict / kind / fail-closed。v7 可批准进 A.2; m1 随 A.2 转 tasks 同 pass 落 (或由主控直接补句, 不需 R8)。
