---
round: R3
checkpoint: post_spec
mode: convergence
spec: pre-merge-gate-no-run-for-branch
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: PASS_WITH_WARNINGS, A2: PASS_WITH_WARNINGS, A3: PASS_WITH_WARNINGS, A4: PASS_WITH_WARNINGS, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: REVISE}
verdict: FAIL
converged: false
incomplete: false
r2_disposition: {closed: 33, partial: 5, not_addressed: 1}
totals: {critical: 0, major: 18, minor: 15}
dedup_clusters: 10
major_trend: "R1 23 → R2 21 → R3 18; Critical 2→1→0。R3 Major 全在 v3 新文字, 但五席一致判「无子设计级发生器, 修法为行级钉死 + 一处机制替换」(A1 明言); 设计收缩本身 0 席反对"
timestamp: 2026-08-22T10:40:00Z
---

# post_spec R3 聚合 — pre-merge-gate-no-run-for-branch (aria-plugin#152)

五席 REVISE, 0 Critical。v3 的两项结构决定 (删自动动作 / helper 接 CLI) **无一席反对**; 第八早退插入点 (A1 复核「唯一可推」) 与 t≈90 首次 prompt 时间轴 (A1 逐轮重算成立) 两个 R1/R2 反复复发的点本轮**钉住**。残余 Major 集中在: 运行时探针形态 (恒红 + 交付面错位) / CLI 签名漏承重参数 / 伪码作用域与消毒 / `dispatch_viable` 运行时不可达 / 版本引用点 cite≠apply / NEG-4 零执行风险。

## 去重后处置表 (→ v4)

| # | 来源 | 内容 | v4 处置 |
|---|------|------|---------|
| 1 | A1-R3-M1 + A1-R3-M2 + A5-R3-M2 + A1-R3-m5 | 14d liveness state-check **健康常态值=红** (162 篇 handoff 仅 2 篇有 wait episode; dogfood 后 14d 即永久红); telemetry 无 `source` 分区 (单测与生产同分区 ⇒ 可 spoof); 探针放主仓 `.aria/probes/` 而非插件交付面; **项目已有声明式 `runtime_probe:` 归档门探针 (DEC-20260705-001) 专为此场景设计且等待首个采用者**; telemetry 分区须 .gitignore | **切除** state-check; telemetry 记录加 `source: production\|test` + `ts` (CLI 默认 production, `--source test` 供单测; 镜像 coordination 先例 anti-spoof); spec frontmatter 声明 `runtime_probe:` (partition `.aria/gate-state-telemetry.jsonl`, symbol `record`, max_age_days 14) — 归档门 D.2 一次性核验, 非常驻; `.gitignore` 加分区; SC-13 活体证据抄进 traps §6 作 tracked 证据 |
| 2 | A1-R3-M3 + A4-R3-M2 + A4-R3-m2 + A1-R3-m1 | CLI `record` 漏 `--name` / `--intervals` (`is_first` 按 name 判, `next_check_at` 按 intervals 算 ⇒ 配置被静默忽略, resume 断); `--verdict wait` 与 helper `GATE_STATUS_WAITING="waiting"` 枚举未映射 (实跑 retry_count 恒 0 / status 非法); 无 gate_error 时 3c' 解引用; stdout 缺 `elapsed_seconds` | CLI 签名封闭钉死: `record --name pre_merge --verdict {wait\|green\|fail}` (gate 枚举, CLI 内映射 wait→waiting) `[--gate-error-kind K] [--threshold N=3] [--intervals JSON] [--in-flight-runs JSON] [--raw-message S] [--source production\|test]`; stdout `{retry_count, no_run_observations, should_prompt, elapsed_seconds, next_check_at}`; 无 gate_error 时省略两旗标 |
| 3 | A1-R3-M4 + A2-R3-M1 + A4-R3-M1 | 2.1 `verify_note` / 2.2 `gate_error` 分支外读取 ⇒ 非 not_found 路径 UnboundLocalError (两实例); verify-failed `detail` 是 surrogateescape 的 git stderr, `+=` 进 message 绕过 `_sanitize_for_json` | 伪码各加哨兵初始化 (`gate_error = None` / `verify_note = ""`); 后缀整体经 `_sanitize_for_json` |
| 4 | A1-R3-M5 + A1-R3-m4 + A4-R3-M3 | 「continue 后 ~210s 再 prompt」算错 (逐轮实算 t≈810); exit 2 continue 只 reset retry_count 下 obs 可能下一轮即达阈 ⇒ 30s 内双 prompt; 「禁手写 JSON」下 exit 2 的 reset 无 CLI 可走 | 时间轴改 810; CLI `reset` 子命令 `--retry-count` / `--observations` 旗标; **exit 2 continue = 两者都 reset**; exit 2.5 continue = 只 reset observations |
| 5 | A1-R3-M6 + A4-R3-M4 + A3-R3-M1 | `dispatch_viable` 只在 traps, 运行时渲染无机制; `dispatchable_workflows` 是 `.forgejo/workflows/x.yml` 相对路径, 逐字拼 URL ⇒ 404 (须 basename); TASK-0a 对「2xx 但 600s 零 run」无布尔映射; false 时 §4 成零消费方 | `DISPATCH_VIABLE: bool` **模块常量** (`pre_merge_gate.py`, 注释引 traps §6 证据); `_no_run_gate_error` 在常量 true 且列表非空时把 dispatch 命令行 (basename) **渲染进 message**; `dispatch_viable := 600s 内观测到 run` (2xx-无 run → false, 证据标 `queued-unobserved`); **false ⇒ §4 整段 + SC-8/SC-9 dispatch 部分从本 spec 删除** (条件 scope 只此一处, 明写) |
| 6 | A2-R3-M2 | `empty-diff` 档 `<main>...<pr>` 占位无数据来源 (三层签名都不带分支名) | 文案去分支名: 「三点 diff 为空」 |
| 7 | A2-R3-M3 + A2-R3-m1 | state 文件不存在时 `load_state` 返 None ⇒ CLI 崩; SC-11(d) 未独立重读文件 | `record --verdict wait` 在文件缺失时创建骨架 `{"format_version":"1.1","gate_state":null}` 再写; `reset`/`clear` 缺失 → exit 2; SC-11(d) 加独立重读落盘文件断言 |
| 8 | A4-R3-M5 + A5-R3-M1 | 版本引用点 cite≠apply: #177 点名 `CLAUDE.md:139/:141` (项目状态段含 `aria-plugin v1.66.3`, 无 custom check 兜底), v3 写成 `:5 不动`; i18n 9 点未枚举 | 主仓侧枚举 14 点: `CLAUDE.md:139,:141` / `VERSION:24` / `README.md:8,:242` / i18n ×3 各 (badge + Plugin Version 行 + `translated-from` 标记) / gitlink |
| 9 | A3-R3-M2 + A4-R3-m4 | NEG-3 自 v1.65.3 ship **从未被执行** (ab-results 零记录; v1.66.0 Rule #6 跑的是 throwaway eval) ⇒ NEG-4 只登记会复制零执行; catalog version/changelog/元键集 | SC-15 加「**真跑一次**并落 `ab-results/<date>-<spec>/`」; catalog `version` bump + `changelog` 行 + NEG-4 元键集 = NEG-3 全集 |
| 10 | A1-R3-m2 / A1-R3-m3 / A2-R3-m2 / A4-R3-m1 / A4-R3-m3 / A5-R3-m1 / A3 minors | verify-failed 象限注记 / SC-7 计数法 (六个 return 点八个变体, 与 SKILL:288/290 taxonomy 对齐) / 包装保留 timeout 默认 / 新名桩放 mixin / 代码注释 + `--remote` help + Impact 补 artifact / **Why 段「~2/3」统计张冠李戴 (严格 15/44≈34%, 从宽 19/44≈43%)** 改准确 | 逐条吸收 |

## 席位实测亮点

- A1: 162 篇 handoff grep (`gate_state`/`wait_recoverable` 仅 2 篇 vs `C.2.4` 35 篇) 证探针恒红; `_next_check_at` 逐轮重算 810s。
- A2: 三层签名逐一核对分支名无来源; `load_state(None)` 路径实读。
- A3: `ab-results/` 全目录 grep NEG-3 零执行记录; `test_gate_state_helper.py` 加形参全绿。
- A4: `r3_a4_demo.py` 实跑 UnboundLocalError 与 `wait`≠`waiting`; `dispatchable_workflows` 路径形态 `:391-407,489`。
- A5: DEC-20260705-001 + `runtime-probe-declaration.md` 机制考古; R1+R2 聚合逐簇点算 Major 归属。

## 收敛判定

R3 REVISE (5/5, 0C) → v4 落上表 10 簇 → **R4 = max_rounds 末轮**: 五席复核 R3 簇闭合 + 稳定性确认 (memory `premerge_iteration_pattern`: 首个 0-finding 轮不能直接声称收敛, 但本为 post_spec 且 R4 为配额末轮, 若 R4 全 PASS 即 CONVERGED; 若仍 REVISE → audit-engine 降级三路径交 owner)。
