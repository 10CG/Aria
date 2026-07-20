---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-19T19:15:15.818Z
context: state-scanner-gate-yaml-datasource
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

被审 proposal 的核心方向 (status-based fail-CLOSED 白名单 + tasks.md 优先 precedence + 三态 gate) 架构上成立, probe-first 语料实证扎实。逐条 code-ground 后发现 **2 Major + 3 Minor**, 无 Critical。

### F1 — Major / architecture / lib/detailed_tasks.py + spec_complete.py / decision

「单一 SOT」决策未真正达成 — spec_complete.py:293 已有 _TASK_ID_LINE_RE + :376 _split_task_blocks + :391 _extract_yaml_key_list (live 于 #95 符号提取路径 :435)。本 change 落地后将有两个 detailed-tasks.yaml 块切分器各持一份 `- id:` 边界知识 — 恰是所引 carry_forward.py 先例要防的 double-write。缓解张力: 搬迁会把 blast radius 打进已 ship 的 #95 子系统。fix 二选一: (a) lib 承接 _TASK_ID_LINE_RE/_split_task_blocks 成真 SOT, #95 路径 re-import; (b) 诚实降级措辞为「status-抽取维度独立 parser, 有意不合并以限 blast radius」+ consolidation follow-up。不接受保留「单一 SOT」表述而实为两 parser。

### F2 — Major / testing / tests/test_gate_yaml_only_source.py + SC-9 / issue

test_gate_yaml_only_source.py:32 _SOURCE_UNSUPPORTED_CLAIM, :38 fixture status: pending, :48 断言 verdict==warn, :51 断言 claim in claims — 新设计下必然翻红, 与 SC-9「既有测试绿 1248」直接冲突; Impact 未把该文件列为「须改写」。风险: 为保老测试绿而削弱新行为 = 把 blanket 假绿焊回去。fix: SC-9 显式区分「编码已退役行为的测试须随行为改写 (点名)」vs「无关测试保持绿」; Impact 把该文件列为修改; 基线 1248 重述。

### F3 — Minor / implementation / gate_result yaml 分支 §2.1 / risk

§2.1 声称镜像 _extract_deferred_or_unchecked_items 实际只镜像一半 — :1102-1112 抽两类 (未勾项 :1108 + carry-forward 标注 :1110-1111), yaml 版只抽 status 非白名单项, 未抽 yaml 文本内 _CARRY_FORWARD_RE 标注。全 done ∧ 含 [TODO:] 标注的 yaml-only spec → gate 判 clean 无 tracker, 但 is_spec_complete=incomplete、carry_forward 命中 — 三点分叉, gate 侧新假绿。corpus 实测缓解: 17 份 yaml 零 inline 标注, 今日 blast radius=0; 但 SC-7 自己会构造该 fixture。fix: gate yaml d_payload 也 fold inline 标注 (真镜像), 或显式声明不对称理由。

### F4 — Minor / implementation / gate_result :1327 early-return / risk

yaml-only 分支 :1327 早退于 :1451 runtime_probe fold 之前 — yaml-only spec 的 runtime_probe 声明被静默跳过。属既存行为 (v1.61.0 已如此), 3 个真实 yaml-only spec 均无声明, 影响 0。建议 (非阻塞): proposal 记 known-limitation。

### F5 — Minor / implementation / lib/detailed_tasks.py §1 parser / risk

§1 未显式规定 status: 抽取须行首锚定。真实语料含 embedded status: token (ai-native-estimator TASK-004 description 折叠块 {status:insufficient, :94-95; multi-terminal-coordination deliverables 散文 status: unknown :191/194)。非锚定扫描 → 误抽 → fail-CLOSED 判残留 → 击穿 SC-8。fix: §1 显式规定 ^[ \t]*status: 行首锚定, 与 _TASK_ID_LINE_RE 同风格。

### 验证通过 (无 finding) 的关键设计点

- precedence 三消费点一致成立 (gate :1299 / is_spec_complete :210 / collector :267)。
- #95 tri-state 正交保持 (「残留不升 warn」与 tasks.md 路径同构; d_payload 与 verdict 解耦)。
- fail-CLOSED 白名单不复用 _normalize_status 论证正确。
- 退役串影响面: unsupported 仅 2 live 引用 (spec_complete.py:1313 + test:32→F2); openspec-archive 无需改成立。

## SCOPE_OK 判定

SCOPE_OK = True。primary_goal 三点全命中未逾越; is_spec_complete 非 scope creep (anchor 显式点名); out_of_scope 全尊重; source_sha 一致。

## Vote

REVISE (F1 + F2 两 Major)。两 Major 均可低成本收敛不动主线; 3 Minor 建议同轮吸收, 尤以 F3 (三点分叉) 与 F5 (SC-8 前置假设) 值得钉进设计决策记录。
