---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T13:05:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 0
minor_count: 4
---

# post_spec R5 (稳定性确认轮) — A4 code-reviewer 席 (spec↔代码逐行 / 引用稳定性 / 实施者分叉)

审计对象: v5 (R4-fix) `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md`。基线 aria @ `400f0bc` (实核 `git rev-parse`, 工作树干净)。无 v4 快照 (proposal.md 未入 git), v4→v5 diff 以我 R4 报告逐字引用的 v4 文本为对照。实读: `gate_state_helper.py` 全文 (`:1-18` docstring / `:41-43 _utcnow_iso` / `:104-156 write_gate_state` / `:30 CURRENT_SCHEMA_VERSION="1.1"`) · `pre_merge_gate.py:262-276 _build_output` / `:355-380 _no_ci_output` / `:546-553` argparse · `lib/runtime_probe.py:185-192 _parse_ts` / `:253-300 _scan_partition` / `:316-320` outcome 表 · `lib/spec_complete.py:1232-1262` probe fold / `:1589-1599` yaml-only 臂 / `:1522 gate_result` · `openspec-archive/SKILL.md:108-113` (`--gate` CLI) · `workflow-runner/SKILL.md:332-358, :385-392` · `workflow-state-schema.md:36-52, :110-131, :308-318` · `phase-c-integrator/SKILL.md:248-263, :288-290` · 主仓 `CLAUDE.md` / `VERSION` / `README*.md` (`grep 1.66.3` 14 点复核) / `.gitignore:19-21` / `.aria/config.template.json:73-91` / `config-loader/SKILL.md:283` / `runtime-probe-declaration.md:133-140` · NEG-3 fixture 元键 (`json.load` 实数 8)。

## 摘要

归我席的簇 #5 与簇 #6 中我的 5 条 minor **全部 closed**, 且吸收文本与我 R4 给的修法逐字等价或更强 (m2 把 `started_at=now` 钉进 exit 2 + SC-11(d); m5 把 `ts` 格式与 `fromisoformat` 断言都落了)。v5 的 27 处定点替换里我复核了全部与本席相关的 18 处引用/编号/行号, 稳定; 发现 **4 处 v5 新引入 (或 v5 未同步) 的文本级自相矛盾**, 全部是一字/一句修法, 无一满足 Major 门槛 (不造成错误行为、不 fail-open、不破坏契约; 唯一的「实施者分叉」是 message 里 owner/repo 占位符的写法, 两种写法对消费者 (AI/人) 功能等价)。**vote PASS**。

## R4 处置核对

| 簇# | 状态 | 证据 (实读 v5 + 源码) |
|---|---|---|
| #5 (A4-R4-M1: §3.2 两条 CLI 行漏 `--in-flight-runs` / `--raw-message`) | **closed** | v5 `:162-163` 3c' 逐字含 `--in-flight-runs <json(out.in_flight_runs)> --raw-message <out.raw_message> --source production`; `:160` 步骤 2 「同 3c' 全旗标」(首个 wait 时 `out` 在场, 可传); `:166` 注释点名 R4 A4-M1 与 schema `:123` / §5 row 互斥关系; SC-11(d) `:263` 加「`--in-flight-runs '[{"run_id":1}]' --raw-message 'x'` 透传到落盘 `gate_state.in_flight_runs` / `raw_message`」—— 我 R4 给的坏实现 (照 3c' 抄进 SKILL 不传) 在此必红。对照 `write_gate_state:151,153` 默认 `[]`/`""` ⇒ 透传断言确能区分 ✓。§5 row 11 对 `:345` 的改后文案仍只写「§3.1-3.3」(我 R4 建议写明「五字段全部由 CLI record 填充」) — 语义已由 3c' 承载, 不另立项 |
| #6 / A4-R4-m1 (旗标仅 `no-run-for-branch` kind 时传) | **closed** | `:165` 逐字「两旗标仅 `out.gate_error.kind == "no-run-for-branch"` 时传 (fail 类 kind 无 threshold 键, R4 A4-m1)」= 我给的修法原文 |
| #6 / A4-R4-m2 (exit 2 continue 置 `started_at`) | **closed** | `:172`「`reset --retry-count` 同时置 `started_at=now`」+ 理由「exit 2 实际只由 elapsed 触发, 不重置则 continue 后每 30s 再弹」(与 `DEFAULT_INTERVALS_SECONDS[0]=30` 一致); SC-11(d)「`reset --retry-count` 后 `started_at` 更新」。**残余**: §3.1 `:152` 的 `reset` 签名句「只动指定字段」未同步 → 新 m2 (见下) |
| #6 / A4-R4-m3 (SC-2 8→6 档) | **closed** | SC-2 `:254`「2.3 表 6 档对应的 6 个 reason (真实载荷形态) + None (not_applicable 两 reason 不可达, 由 SC-6 覆盖, R4 A4-m3)」— reason 集 = covered×3 + unknown×3 = 6, 与 2.3 表 `:126-130` 及 `path_coverage.py` reason 族 8 − not_applicable 2 一致 ✓ |
| #6 / A4-R4-m4 (§5 四处引用漂移) | **closed** | (1) 标题去掉「17 处」, 改「逐位置; 主仓 vs 插件分列于『文件』栏」, 主仓行已标「主仓」(config.template / .gitignore / DEC / CHANGELOG 行) ✓; (2) 元键集枚举 8 键 `:223`, 与 NEG-3 `json.load` 实物 8 键**集合相等** (文件内顺序 `_why_…` 在 `_discriminating_question` 前, 集合语义无影响) ✓; (3) 步骤 4/5/6 行号改 `:252-263`, 实核步骤 4 `:252` / 5 `:253` / 6 `:260` ✓; (4) config-loader 行改「`path_coverage_enabled` 已在 `:283`, 只加新 key」+ 模板「两 key 都缺, 补两个」, 与 `config-loader/SKILL.md:283` 实存 / `config.template.json:73-91` 实缺一致 ✓; §3.4 `:190` 与 Impact `:244` 的「模板补 `path_coverage_enabled`」口径同步 ✓ |
| #6 / A4-R4-m5 (`ts` ISO + helper docstring) | **closed** | `:154`「`ts` = `_utcnow_iso()` (ISO 8601, 探针 `fromisoformat` 可解析, epoch 会恒 warn)」— 实核 `_utcnow_iso:43` 产 `%Y-%m-%dT%H:%M:%SZ`, `_parse_ts:189` 先 `replace("Z","+00:00")` 再 `fromisoformat` ⇒ 可解析 ✓; SC-11(d)「telemetry `ts` 可被 `datetime.fromisoformat` 解析」✓; §5 新行 `gate_state_helper.py :2-18 模块 docstring` 实核 docstring 恰为 `:2-18` ✓ |

小计: closed 6 / partial 0 / not_addressed 0 (簇 #5 一项 + 簇 #6 归我 5 项)。

### 非本席簇的交叉复核 (只记事实, 不立项)

- 簇 #1/#2/#3 (A1): `_scan_partition:267` partition 不存在 → `missing` → `probe():317` 映射 `warn` ⇒ SC-16(b) 红窗成立; `spec_complete.py:1589-1598` yaml-only 臂确实 fall through 到 probe fold、`:1599` proposal-only 早退 ⇒ SC-16(a) 前置条件正确; `openspec-archive/SKILL.md:113` 存在 `spec_complete.py --gate` 命令 ⇒ SC-16「同一命令 / 机读 gate JSON」可执行; `_scan_partition:287` 只计 `source == "production"` ⇒ 单测 `--source test` 不污染探针 ✓。
- 簇 #4 (A2): SC-2 dispatch 子项的负断言「不含 `.forgejo/workflows/x.yml/dispatches`」是真正的判别式 (正断言 `workflows/x.yml/dispatches` 是坏实现输出的子串, 单独不能区分), 两条并用正确 ✓。

## v5 引用 / 编号 / 行号稳定性 (主控点名项)

| 点 | 结论 |
|---|---|
| §2.1 `:72`「第七个早退 return 点 (现六点八变体之外新增一点)」↔ SC-7 `:259`「六个早退 return 点 (八个变体)」↔ Impact `:246`「六个早退 return 点契约」 | **一致** (6 点 = enabled:false / no-backend / precheck / main 核验 / (b) AetherQueryError / (a) 腿; 变体 8 = 6 + fallback 两值 + main 两 kind, 行号 R4 已逐一实核) |
| 2.3 `:134`「**既有七个**早退落点键集逐字不变 (SC-7)」 | **不一致** → m1 (v4 计数法残留, 与上面三处冲突) |
| `<owner>/<repo>` 占位 2.3 `:126` ↔ 3.3 (a) `:182` | 散文两处一致 (都是尖括号 `<owner>/<repo>`); 但 2.3 **同一格内的命令模板字面**仍是 `{o}/{r}` → m3 |
| `<pr_branch>` 占位: 2.3 `:126` (gate 回填, 2.1 末段) ↔ 2.1 `:90-92` 回填代码 ↔ 3.3 (b) `:183` (prompt 模板) | 一致; 2.1 末段 `out.get("gate_error")` 对照 `_build_output:273-274` (None 不入键) 安全; 只有 `no-run-for-branch` 能到达该段 (两类 fail 都早退) ✓ |
| §3.1 `:143` episode 定义引「schema §3.3」 | 实核 `workflow-state-schema.md:308-318` §3.3 Cleanup 「On next workflow creation, the old file is overwritten」✓ |
| §3.1 `:151` 骨架 `{"format_version": "1.1", "gate_state": null}` | `CURRENT_SCHEMA_VERSION = "1.1"` (`:30`), `_migrate_state` 对 1.1 不动 ✓ |
| §3.1 `:154` 「沿既有三个 telemetry 分区 `:19-21`」 | 主仓 `.gitignore:19-21` 恰三个 `.aria/coordination-*telemetry*.jsonl` ✓ |
| §5 `:222` 主仓 14 版本点 | `grep 1.66.3` 本轮复跑: `CLAUDE.md:139,:141` / `VERSION:24` / `README.md:8,:242` / 三 i18n 各 `:3,:10,:244` = 14, 行号未漂 ✓ |
| §5 `:219` `runtime-probe-declaration.md:135-139` 预言句 | 实核 `:137-139`「未来第一个真实声明者, 会是下一个自带 telemetry 分区的活跃中 spec」在该区间 ✓ |
| SC-13 `pre_merge_gate.py --main-branch master --pr-branch <b>` | argparse `:546-547` 两旗标存在 ✓ |
| SC-11(d) `--intervals '[5,7]'` 两次调用 | `_next_check_at:110` `idx=min(retry_count, len-1)`: 第一次 retry 0→5s, 第二次 retry 1→7s, 可断言 ✓ |
| Status 行 / R1-R4 簇号引用 / Cross-refs R4 行 | 与四份聚合表一致 ✓ |

## 新 Findings

### 必须改 (一字/一句级, 全部 Minor)

#### [A4-R5-m1] Minor — 2.3 `:134`「既有**七个**早退落点键集逐字不变 (SC-7)」与 §2.1 `:72` / SC-7 `:259` / Impact `:246` 的「六个 (八变体)」冲突

- v5 把 §2.1 从「第八个」改成「第七个」(吸收 A1-R4-m1) 后, 2.3 这句的「既有七个」没同步 — 它要么把新增那点算成「既有」, 要么沿用 v4 的计数法。SC-7 是 SOT (6 点 8 变体, 行号实核)。
- 不满足 Major 门槛: 纯叙述, 实施者照 SC-7 行号写测试不受影响。
- 修法: 「既有六个早退落点 (八变体) 键集逐字不变 (SC-7)」。

#### [A4-R5-m2] Minor — §3.1 `:152` `reset` 签名句「只动指定字段」与 §3.2 `:172` / SC-11(d) 「`reset --retry-count` 同时置 `started_at=now`」矛盾

- v5 吸收我 R4 m2 时只改了 §3.2 与 SC-11(d), §3.1 的签名定义 (实施者最先读的那句) 仍说 `reset` 只动指定字段。照 §3.1 实现的人不会碰 `started_at`; SC-11(d)「`reset --retry-count` 后 `started_at` 更新」能把他抓红 ⇒ 分叉**有 SC 区分**, 不到 Major。
- 修法: `:152` 改为「`reset [--observations] [--retry-count]` (至少一个旗标; `--observations` 只置 0; `--retry-count` 置 0 **并同时置 `started_at=now`** (重开计时, 见 3.2 exit 2); 其余字段不碰)」。

#### [A4-R5-m3] Minor — 2.3 `:126` 同一格内: 命令模板字面 `/repos/{o}/{r}/…` 用**花括号**, 紧随的散文说「`<owner>/<repo>` 由 AI 填 … 占位用尖括号, 避免 `.format()` 花括号雷」; 3.3 (a) `:182` 也是 `<owner>/<repo>`

- v4 两处都是 `{o}/{r}` (我 R4 核过「字符级一致」); v5 改散文与 3.3 为尖括号、加了「避免花括号雷」的理由, 但模板字面没改 ⇒ **v5 新引入**。实施者 A 抄模板渲染 `{o}/{r}`, 实施者 B 照散文渲染 `<owner>/<repo>`; SC-2 dispatch 子项两条断言 (`workflows/x.yml/dispatches` 正 / `.forgejo/…` 负) 对两种写法都绿。
- **为何不到 Major**: 占位符的消费者是 AI/人 (3.3 (a)「AI 只填」), 两种写法功能等价, 无错误行为。但「避免 `.format()` 花括号雷」这个理由本身**不成立**: 同一串里 `-d '{"ref":"<pr_branch>"}'` 的 JSON 花括号无论如何都在, 任何 `.format()` 都会炸, 尖括号占位并没有消掉雷 —— 实施者若信了这句而用 `.format()` 渲染, SC-2 会以 KeyError/IndexError 红掉 (可发现, 所以仍是 minor), 但理由句在误导。
- 修法: 模板改 `forgejo POST /repos/<owner>/<repo>/actions/workflows/<basename(file)>/dispatches -d '{"ref":"<pr_branch>"}'`; 理由句改「整串含 JSON 花括号, **禁用 `.format()`**, 用拼接或 f-string 双花括号转义; 三个占位统一尖括号」。

#### [A4-R5-m4] Minor — R-e `:289`「CLI exit 2 ⇒ AI surface + **按 exit 2 prompt 处理**」与 3d `:167`「CLI 退出码 2 → surface 错误 → **直接 abort** (不再调 reset)」不一致

- v5 在 3d 吸收 A1-R4-m4 (exit 2 双义 + reset 同样会退 2 ⇒ 直接 abort), 但 Risks R-e 仍是 v4 文案「按 exit 2 prompt 处理」— 这里的「exit 2」读作 exit condition 2 (user prompt continue/abort), 与 3d 的「不 prompt 直接 abort」相反。无人值守下二者等价 (prompt ≡ abort), 交互式下不同。3d 是 normative 段, R-e 是 risk 叙述 ⇒ minor。
- 修法: R-e 改「CLI 退出码 2 ⇒ AI surface stderr + 直接 abort (3d), 禁回退手写 JSON」。

### 还能挑 (不要求改, 记录备 A.2 裁量)

- **2.1 末段 `<pr_branch>` 回填零 SC**: SC-5/SC-10 都不断言 message 里 `<pr_branch>` 已替换成真实分支名。实施者漏做 replace 只影响处方行的可粘贴性 (人/AI 可手填), 不算错误行为。若要钉: SC-5(a) 在 `dispatch_viable=true` 时加「message 不含 `<pr_branch>` 且含 pr_branch 实名」。另: 若 TASK-0a 判 false, 2.1 末段的 `.replace("<pr_branch>")` 成为无消费方的 no-op (`verify_note` 拼接仍需要), 3.5 删除清单可顺带提一句。
- **SC-2「2.3 表 6 档对应的 6 个 reason」措辞**: 6 个 reason 实际分布在表的 4 行 (unknown 行含 3 reason); reason 集本身无歧义, 措辞可改「2.3 表 covered×3 + unknown×3 = 6 reason」。
- **CLI `record` 在 state 文件缺失 + verdict∈{green,fail} 时的行为未钉** (`:151` 只钉 wait 时建骨架): 按 `:153`「2 输入或文件错」推断 exit 2; 运行时不可达 (loop 恒以 wait 起步), 一句补齐即可。
- **CLI 无 `--primitive-used` 旗标**: 落盘恒取 helper 默认 `aether-ci-cli`; 实核 `_no_ci_output:355-380` 的 `manual` 只伴随 green/fail 早退, 不进 wait loop ⇒ 不可达, 不立项。

## Verdict

**PASS** (0 Critical / 0 Major / 4 Minor) — **vote: PASS**

归我席的 R4 簇 #5 与 5 条 minor 全部按我给的修法逐字落地且有 SC 钉住 (透传断言对照 helper 默认值确能区分坏实现)。v5 的 27 处替换在本席核查面 (18 处引用/行号/编号) 无漂移, 主控点名的「第七个 vs SC-7 六个」与「`<owner>/<repo>` 两处」两问的答案分别是: 一致 / 散文一致但同格模板字面未同步。四条新 minor 都是 v5 定点替换时的**邻句未同步** (计数残留 / reset 签名句 / 占位符字面 / Risks 段), 每条一行修法, 无一满足 Major 四门槛; 建议在 A.2 转 tasks 前由 fix-writer 一次 4 处定点改, 不需要 R6。
