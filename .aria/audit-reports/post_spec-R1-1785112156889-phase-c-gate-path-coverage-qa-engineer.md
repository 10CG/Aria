---
agent: qa-engineer
round: R1
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 1
major_count: 5
minor_count: 2
---

# QA 审计报告：phase-c-gate-path-coverage-not-applicable (aria-plugin #122)

方法: code-grounded — 实读 pre_merge_gate.py (386 行) / test_pre_merge_gate.py (562 行) / test_ci_backends.py / base.py Literal / workflow-runner gate_state_helper.py (下游消费方) / custom_checks.py / 4 份真实 workflow; git diff 重命名形态经隔离沙箱实测。

## Critical

### QA-1｜workflow 文件自身在变更集里 — 结构性反向假绿盲区

判定算法从未把「changed_files 含 workflow 文件自身路径」纳入决策。真实语料证实: issue-triage-tests.yml 的 paths 不含它自己。只改 workflow 文件本身的 PR (加 paths / 改 glob / 收窄触发) → changed_files 唯一条目不匹配任何 paths → 全部 workflow 判不触发 → not_applicable → 放行。本应是「对 CI 配置动刀的 PR」被判「CI 与我无关」— 与恒红同构, 方向翻到 green。
**修法**: 硬规则 — changed_files 任一条落在三个 workflows 目录下 → 整体强制 covered。新增 SC-16 锁定「仅修改 workflow 文件自身 → covered」。

## Major

### QA-2｜SC-9/SC-10 未钉「(a) 查询被跳过」因果机制本身
只断言 verdict 值; 若实现没真 short-circuit 而 mock pr_state=passing, SC-10 照绿但机制坏。
**修法**: 测试构造显式加 `mock_backend.query_pr_ci.assert_not_called()` (复用 test_case_f 既有模式)。

### QA-3｜默认开启使既有 62 测试隐性依赖真实 git 子进程
既有测试不传 path_coverage_enabled=False 也不 mock → 按字面接线会在真实 CWD 对真实仓跑 git diff main...feat/x — 今天靠 SC-8 unknown 兜底侥幸绿, 但脆弱 (CWD/分支名巧合会翻转 verdict) + 62 测试每次多一次真实子进程。
**修法**: SC-11 验收方法论二选一 (统一注入 False / mock 评估器入口); 新增 SC「既有套件运行期间零真实 git 子进程」卫生断言。

### QA-4｜push 与 pull_request 的 paths 列表不一致时语义未钉
本仓语料两者恰好一致掩盖歧义。须锁「按触发类型逐个判断、任一命中即 covered」OR 语义。
**修法**: 新增 SC-17 (push 无 paths + pull_request 有 paths, 及反向)。

### QA-5｜多 workflow 混合判定没有对齐真实语料的 SC
D5 宣称语料=4 真实 workflow, SC-2 只用子模块 1 份。主仓 3 份 (branches+paths 组合 / dispatch+push 组合 / 纯 dispatch) 从未锁为 SC fixture。
**修法**: 新增主仓 3 文件联合语料活性 SC。

### QA-6｜git diff --name-only 对重命名只吐新路径, 未建模
沙箱实测: rename 只输出新路径 (对照: 纯删除会输出被删路径)。「从覆盖路径重命名移出」的 PR 可能被判 not_applicable。rename 检测策略 (-M / --no-renames / 是否纳入旧路径) 未声明。
**修法**: 新增 SC-18 双向重命名用例 + proposal 声明 rename 策略。

## Minor

### QA-7｜matched_workflows 元素类型未定义 (文件路径 vs name: 字段) — 建议钉「相对仓根的 workflow 文件路径」。
### QA-8｜glob 大小写敏感性未被 SC-14 显式覆盖 — 补一行防御性用例。

## 结论

骨架自洽且 D1 代码级成立 (CIStatus Literal 从未被赋 not_applicable; 下游 gate_state_helper.py 只读 verdict, 值域不变, 跨 skill 消费方回归风险可控)。但 1 Critical + 5 Major 全部发生在真实语料/真实代码交界处 — QA-1/QA-3 直接命中「机制换形态失效」风险类别。**REVISE**: 进 Phase B 前至少补 SC-16 + assert_not_called + SC-11 隔离方法论; QA-4/5/6 本轮补齐或转显式已知缺口留痕。
