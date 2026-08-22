---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T15:10:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 0
minor_count: 2
---

## 摘要

末轮 (max_rounds=6) 复核 v6, 基线仍 `aria @ 400f0bc`。核对范围按主控指派: (1) SC-5 (c)(d) 回填断言能否真的红; (2) `record` verdict≠wait 文件缺失 exit 2 + `reset_retry_count` 具名 helper 的吸收; (3) `DISPATCH_VIABLE` 读取方式留 Phase B 是否可接受; (4) v6 13 处 diff 有无新引入的矛盾。方法: 实读 `pre_merge_gate.py` (`compute_verdict:172-227` / `gate_check:387-527` / `_verify_main_branch_exists:302-352` / `_build_output` / `DEFAULT_CONFIG:56-69`)、`ci_backends/aether.py:216-232` (F1 仍在)、`gate_state_helper.py` 全文 247 行 (确认无 `main()`/CLI, F7 仍成立)、`path_coverage.py:1-40` + `_result` 调用点、`test_pre_merge_gate.py:361-362` (`[] → "pending"` 现状), 不采信 spec 文本自述。

结论: 我 R5 报的 A2-R5-M1 (`<pr_branch>` 回填 + raw_message 重同步零 SC) **真实收敛** —— v6 SC-5 加的 (c)(d) 子项同时钉死"漏 `.replace()`"与"漏同步 `raw_message`"两种坏实现, 且逻辑上覆盖 `gate_check` 里回填代码唯一的执行路径 (verify-failed 分支也流经同一段 `if out.get("gate_error")` 代码, 不需要为它单独复制断言)。R4 遗留两条 Minor (record 非-wait+文件缺失未定义 / `reset --retry-count` 无具名函数) 均在 v6 §3.1 落地为可读的显式规格。`DISPATCH_VIABLE` 读取方式仍未写进 spec 正文, 但这是 R5 聚合裁定"非强制, 留 Phase B 实施时顺手"的既定处置, 非新缺口。本轮新鲜眼睛复查 v6 §3.1 新增的"`record` 文件缺失+非wait → exit 2"分支, 发现它同样零 SC 覆盖, 但结构上被 §3.2 步骤 2 的调用序列不变量 (首次调用恒为 wait) 挡在可达路径之外, 与 A2-R5-m2 同类, 判 Minor 不判 Major。0 Critical / 0 Major / 2 Minor, 投 **PASS**。

## R5 处置核对

| 簇# | 内容 (节选, 归本席) | 状态 | 证据 |
|---|---|---|---|
| 2 (A2-R5-M1) | v5 新加 `<pr_branch>` 回填 + `raw_message` 重同步, 全 SC 表零覆盖 | **closed** | v6 SC-5 新增 (c)(d): "(c) **回填断言**: 两变体 message 均**含** `feat/x`、**不含**字面 `<pr_branch>`, 且 `raw_message == gate_error.message`; (d) 核验 mock 返 `("verify-failed","boom")` → message 末尾含「核验失败: boom」且 raw_message 同步"。逐一核对两种坏实现: (a) 漏 `.replace()` → message 仍含字面 `<pr_branch>`, 被"不含 `<pr_branch>`"断言直接抓红; (b) 漏同步 `out["raw_message"]` → 两者不再相等, 被 `raw_message == gate_error.message` 抓红。verify-failed 分支复用同一段 `if out.get("gate_error"):` 代码 (§2.1 伪码单一入口, 未分叉两条实现路径), SC-5(d) 不必重复断言占位替换即可依赖(c)的覆盖保证同款正确性。 |
| 3 (A2-R4-m1 子项) | CLI `record` 对 `verdict != wait` 且文件缺失时行为未定义 | **closed** | v6 §3.1: "`record` 在文件缺失且 `verdict != wait` 时亦 exit 2 (只有首个 wait 才建骨架)"。规格文字已显式定义 (原为完全未定义)。 |
| 3 (A2-R4-m2 子项) | `reset --retry-count` 无对应具名 helper, 与 `reset_no_run_observations` 不对称 | **closed** | v6 §3.1: "具名 helper `reset_retry_count(state)` 与 `reset_no_run_observations` 对称"。命名对称性问题已解决。 |
| 4 (A2-R5-m1) | `DISPATCH_VIABLE` 读取方式 (裸全局 vs 默认参数捕获) 未钉死 | **not_addressed (裁定内)** | `grep -n "DISPATCH_VIABLE\|裸全局\|默认参数" proposal.md` 确认正文未新增约束句。但 R5 聚合表簇 #4 已明示处置 = "非强制, 留 Phase B 实施时顺手 (不阻塞)" —— 这是已裁定的降级, 非遗漏; 我 R5 本就判 Minor (TDD 会强迫收敛, 不构成两实现分叉不可辨), 维持原判, 不升级、不重复计入本轮 Major。 |

## 新 Findings

无 Major。一条新 Minor, 见下。

## Minor Findings

### [A2-R6-m1] Minor (新) — `record` 新增的 "文件缺失 + `verdict != wait`" 分支零 SC 覆盖, 但结构上不可达

**锚点**: proposal §3.1: "`record` 在文件缺失且 `verdict != wait` 时亦 exit 2 (只有首个 wait 才建骨架)"。

**问题**: 这是 v6 才补全的行为定义 (响应 A2-R4-m1)。逐查 SC-11 (helper 契约的唯一 SC), (a)(b)(c)(d) 四个子项没有一条构造"文件不存在 + `--verdict green` 或 `--verdict fail`"的调用来验证这条新分支真的走到 `exit 2`; SC-11(d) 的"缺 `--source` exit 2"断言测的是另一个校验轴 (必填参数), 不能替代它。

**为何仍是 Minor 非 Major**: 与 A2-R5-m2 (record 非-wait+文件缺失未定义) 同一根因、同一护栏——§3.2 步骤 2 规定"首个 wait verdict → 创建 gate_state 也经 CLI record", 即 gate_state 文件在 workflow-runner 的文档化调用序列里只会先经一次 `--verdict wait` 调用被创建, 之后 §3.2 步骤 3c′ 才会传入任意 verdict; 因此"文件缺失且 verdict≠wait"在文档化的正常生产路径上结构性不可达, 只有脱离 workflow-runner 直调 CLI (交互式误用) 才可能触发。两个实现者即便这条分支各写各的 (一个真 exit 2, 一个例如尝试读 `None` 抛未捕获异常), 也不会在 SC-1~SC-16 全绿的前提下产生"生产环境里行为不同"的可观测分叉——这正是它保持 Minor 而非 Major 的判据 (对比 A2-R5-M1: 那条回填缺陷落在**每次零 run 都会触达**的主路径上)。

**建议**: 在 SC-11 追加一句"(e) 文件不存在 + `--verdict green`(或 `fail`) → exit 2, stderr 含缺文件说明", 复用 (d) 已有的"独立重读断言"模式, 成本很低(一次 subprocess 调用 + 一次 returncode 断言)。不阻塞批准, 可在 Phase B 实施时顺手补。

### [A2-R6-m2] Minor (R5 残留, 裁定内不阻塞) — `DISPATCH_VIABLE` 读取方式未钉死

同 A2-R5-m1。R5 聚合表已裁定"非强制, 留 Phase B 实施时顺手 (不阻塞)"。本轮复核结论不变: `_no_run_gate_error` 若被实现为默认参数捕获 (`dispatch_viable: bool = DISPATCH_VIABLE`) 而非裸全局引用, SC-2 的 `monkeypatch.setattr(gate, "DISPATCH_VIABLE", False)` 负控会对合规实现持续报红, 但 TDD 红→绿纪律会强制实现者定位并改成与 `evaluate_path_coverage` 打桩先例一致的裸全局引用写法——不存在"错误实现蒙混过关"路径, 只是排查成本, 不构成两实现分叉不可辨。维持 Minor, 建议 Phase B 落地时在 `_no_run_gate_error` 函数体注释处补一句实现约束(不需要改 spec)。

## v6 13 处 diff 机制层稳定性复核 (未发现新矛盾的部分, 按要求记录)

- **§2.1 "第七个早退 return 点" vs §3.7/SC-7 "六个早退 return 点 (八变体)"**: `grep "七个\|六个早退\|八个变体"` 核对, 两处用词自洽 —— "六个 (八变体)" 指**既有、不变**的六点, "第七个"指本 spec **新增**的 PR 分支消歧点, 二者是"存量 + 新增 1"的关系, 非同一计数口径下的矛盾。SC-7 "main 核验那支本就是七键" 与既有代码实读 (main-verify 分支 `gate_error={"kind":kind,"message":msg}` 外加 verdict/pr_ci_status/in_flight_runs/primitive_used/raw_message = 6 通用键 + gate_error = 7) 吻合。
- **R-e vs §3.2 步骤 3d**: 两处均为"CLI 退出码 2 → surface + 直接 abort, 禁止回退手写 JSON", 逐字一致, 已消解此前的不一致 (簇 3 "R-e 与 3d 不一致" 已 closed)。
- **`path_coverage.py:36` "共 9 个" → 8**: 实读 docstring 判定规则 1-8 (`:24-31`) 逐条数, 终态 reason 值 = 7 条规则终态 (git-diff-failed / empty-diff / workflow-files-changed / no-workflow-files / workflow-trigger-matched / workflow-parse-failed / no-triggering-paths, 规则 5 是中间步骤不产终态) + 横切 `internal-error` = 8, 现状文档写"9"确系笔误, spec 勘正为"8"准确。
- **SC-2 "6 档对应的 6 个 reason + None"**: 逐行核对 §2.3 message 表 6 行 (trigger-matched/files-changed/empty-diff/unknown 组(内含 3 个真实 reason: git-diff-failed·workflow-parse-failed·internal-error)/pc=None/not_applicable-不可达), 1+1+1+3=6 个真实 reason 值 + 单独的 pc=None 一档, 与 SC-2 措辞吻合, 非漏项。
- **`<owner>/<repo>` 占位 + "禁用 `str.format`" 理由**: 新增说明"占位统一尖括号; 渲染禁用 str.format — JSON 体的花括号本就在串内"逻辑自洽(`-d '{"ref":"<pr_branch>"}'` 若走 `.format()` 会被 JSON 花括号误判为格式槽)。
- **§3.1 reset 语义**: `reset --observations`(条件 2.5 continue) 与 `reset --retry-count --observations`(条件 1 continue) 两处调用的字段影响范围逐一核对无交叉污染, `write_gate_state` 的 `started_at` 承接逻辑 (`existing.get("started_at") or _utcnow_iso()`) 与 `reset --retry-count` 显式覆盖 `started_at=now` 分属不同函数, 不产生隐藏耦合 (同 R5 已判定"无新问题")。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 0 Major / 2 Minor)

vote: **PASS** —— 我 R5 报的 Major (A2-R5-M1) 经 v6 SC-5 (c)(d) 真实收敛, 逻辑上能同时抓住"漏 replace"与"漏同步 raw_message"两类坏实现; R4 两条 Minor (record 非-wait 文件缺失未定义 / reset --retry-count 无具名函数) 均已在 v6 落地为显式规格。残余 2 条 Minor (record 新分支零 SC 覆盖但结构不可达; DISPATCH_VIABLE 读取方式仍未钉死但已裁定非阻塞) 均不满足 Major 门槛 (无法造成错误行为 / fail-open / 契约破坏 / 两实现必然分叉且全绿不可辨) —— 两者共同特征是"文档化正常调用序列结构性挡住了危险输入", 与已收敛的 A2-R5-M1(落在每次零 run 都触达的主路径上)性质不同。可挑但非必须改: SC-11 可选择性补一条 exit-2 断言; DISPATCH_VIABLE 读取方式可选择性在实现阶段加注释约束。均可留 Phase B 顺手处理, 不构成阻塞批准进 A.2 的理由。
