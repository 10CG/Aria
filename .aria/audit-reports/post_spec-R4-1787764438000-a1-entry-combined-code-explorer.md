---
checkpoint: post_spec
round: 4
role: code-explorer
verdict: REVISE
scope_ok: true
counts: 0C/1M/1m
---

# post_spec R4 — a1-entry 三份 Spec 联审 — code-explorer 席 (跨文件追踪与事实核验)

> **⚠️ 落盘说明**: 本席被分配的工具集不含 Bash/Write, **无法自行写盘**, 回执以正文形式返回,
> 由**主控代为落盘**并逐条复核。主控对 Finding 1 做了独立逐字复跑 (见下方「主控复核」)。
> 因同一约束, 任务第 4 项 (逐 commit diff 找「覆盖掉原依据」) 未能按字面执行; 本席改用
> 「直接对比 Spec 引文与源码原文」的等价手段, 并由此抓到 Finding 1。

## Finding 1 (Major, 母 Spec §5.3) — `release_claim_by_track` docstring 被误引

母 Spec §5.3 声称该 docstring「逐字写着」:
`If several active claims match (same session), ALL matching active claims are released`

**实读 `claim_lifecycle.py:396-399` 原文**:
```
the caller passes the raw carry-id. If several active claims match (same
container re-claimed a track across sessions — the NORMAL case, since
every session mints a fresh session_id and B.0 REQUIRE-claim runs per
session), **ALL matching active claims are released** (review I1: releasing
```
`(same session)` 是**编造的替换**, 真实文本恰恰在说「**跨 session**」——语义方向被改写。
「ALL matching active claims are released」半句逐字为真, 但整句「逐字」断言不成立。

**更关键**: 审计轨 §5 的核验表 #9 只核对了同一 docstring 里**另一句**引文
(「locates by (normalized track_id, container) and ignores session」), **从未核对过 §5.3 用的这句**
—— 这句新引文**绕过了机械核验表**, 与 R3 code-reviewer 点名的「机械核验全过、内容全错」同形。

C-B 的**设计结论不受影响** (该函数确实按 (container, track_id) 释放全部匹配项), 但引用完整性有缺陷。

### 主控复核 (2026-08-25, 已订正)

**本席判定成立, 主控确认自己错了。** 错误机制已查明并记录:
主控当初跑的是 `sed -n '387,400p' | grep -iE "all|matching"` —— grep **过滤掉了不含关键词的
`:397-398` 两行**, 主控把返回的 `:396` 与 `:399` **当作相邻行拼接**成一句, 于是造出一句
原文不存在、且语义方向相反的引文。**「该行存在」类机械核验对此天然免疫** (两行都真实存在)。

⇒ 订正后 **C1 的结论不但不弱反而更强**: 原文明说多条 claim 匹配同一 track 是
「同一容器跨 session 重新认领 — **the NORMAL case**」⇒ 同 track 多 claim 是**常态**,
D.2b 的 ALL-matching 释放因此**几乎必然**触及仍在制的其他方向。§5.3 已按此加强论证。

## Finding 2 (minor, sibling-spec-probe) — `fetch_gate.py:23` 行号误引

引用 `fetch_gate.py:23` 指「state-scanner sync.py::_resolve_default_branch」两处;
实读该句在 **`:21`**, `:23` 是另一句 (「state-scanner git.py — but the original locks `@{upstream}`」)。
断言内容本身独立核实为真 (`sync.py` 8 个顶层 def 无 `_resolve_default_branch`), 仅行号偏差 2 行。
**主控已订正** (两处 `:23` → `:21` + 加订正注)。

## 逐条核验结果 (抽样约 60/90 条, 除上述 2 条外**全部一致**)

`collision.py:230-234/:265-266/:268/:278-279` · `constants.py:36/:51/:43-44` ·
`identity.py:191/:222/:242/:244` · `claim_lifecycle.py:228/:377/:425-427` ·
`phase1_gate.py:1173/:1032/:335/:1191(--phase required=True)/:1230/:1233-1235/:1236-1238` ·
`phase-b-developer/SKILL.md:86-96` · `branch-manager/SKILL.md:146` · `phase-a-planner:9` ·
`spec-drafter:9-10` · `session-handoff.md:101(§2.3)/:217(§2.3.8)/:238(§2.3.8.3 硬约束)` ·
`DEFAULTS.json` 确认**无** `coordination` 键 (baseline 必红断言属实) · `config-loader/SKILL.md:134/:140` ·
`.aria/state-checks.yaml` 实测 **11** 条 · `openspec/changes/` 实测 **9** 份 ·
`multi_remote.py:255` · `audit-engine/SKILL.md:83,85` · `execution-modes.md:84,113` ·
`report-format.md:50+` · `remote_refresh.py:227/568/691` + `scan.py:312` (唯一生产调用点) ·
`run_all_tests.sh:48,71` · `release_gate.py:237` · `coordination_probe.py:80-83` ·
`track_id.py:61` · `claim_schema.py:130/:165` · `coordination_ref.py:119/:596` ·
`layer-l-integration.md:15,45` (悬空函数名 `update_heartbeat()` 确认真不存在) ·
`coordination-ref-schema.md:129,133-139` · `fetch_gate.py:50-55,86-101,108-128,111-112`

## 跨文档承接核验 (任务第 2 项 — **全部成立, 无缺失**)

- 母 SC-13→字段 §5(D1) · SC-16→探针 SC-1 · SC-17→探针 SC-2 · SC-18→探针 SC-3/SC-4 ·
  SC-19(a)(c)→探针 SC-5/SC-6 · **SC-19(b)→探针明确不迁入, 由母 SC-29 承担** (SC-29 原话
  「承接原 SC-19 的 (b) 子项」) —— **双向对齐**。
- 字段 Spec 称「探针已补逐格映射并采并集」→ 探针 §3 层 1 分派表的 `BAD_TOKEN` 行确为
  「层 1 与层 2 都跑, 取并集」—— **属实**。
- 探针称「姊妹已承诺 E0–E6 交付为可 import 纯函数」→ 字段 Spec 确有该整段含签名 —— **属实**。
- 三份头部「四条不同步声明」: 字段/探针逐字相同; 母 Spec 拆三段但语义完全覆盖, 无缺项。
- 母「§1 逐字搬 / §5 先重测重生成再搬」的分节陈述 —— 与审计轨自身记载及实际体例**相符**。

## Verdict

| Spec | verdict | counts |
|---|---|---|
| a1-entry-claim-duplicate-work-guard (母, R4) | REVISE | 0C/1M/0m |
| linked-issue-field-availability (子, R2) | **PASS** | 0C/0M/0m |
| sibling-spec-probe (子, R2) | REVISE | 0C/0M/1m |
| **combined** | **REVISE (轻)** | **0C/1M/1m** — 均为引用完整性, 不触及设计结论 |

## 局限性声明

未能执行 `git show <SHA>` 逐 hunk diff (工具约束); 抽样 ~60/90 条断言, 优先覆盖任务点名与
高风险/新表面项; 未逐条覆盖 §2.2 heartbeat 三级回落细节与探针 §5 fetch 代价数字。
