# 决策单 2026-10-07 — WP-A (`secret-net-l3-and-bypass-paths`) 转「实现优先」及相关裁定

> **决策人**: owner (全部经会话内 AskUserQuestion 作答)
> **记录人**: 主控 (simonfish/023236f2)
> **关联**:
> - Spec `openspec/changes/secret-net-l3-and-bypass-paths/`
> - R5 聚合报告 `.aria/audit-reports/post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-aggregated.md`
> - handoff `docs/handoff/2026-10-07-session-close-wpa-phase-a-stopped-by-owner.md`

## 背景

post_spec 收敛审计 5 轮未收敛。owner 当日上午裁定「接受当前结论 + 定点修补」(记录在 R5 聚合报告「主控记录」), v6 已落盘 (`596102f`)。

傍晚 owner 以「投入产出严重失衡」(约 40% 周额度, 代码 0 行) 叫停, 并要求严格复盘。复盘见 handoff §4; 机制问题已开 `10CG/aria-plugin#209`。

随后 owner 重新确认待决事项, 作出以下裁定。

## 裁定

| # | 事项 | 裁定 | 执行结果 |
|---|---|---|---|
| 1 | WP-A 方向 | **实现优先**: 以 v6 原型 (已通过全部 454 行验收) 为基础直接实现, 单轮审查; 每一步向 owner 报成本 | 本决策单之后进入 B.1 |
| 2 | 本 Spec 的 `post_planning` | **本 Spec 跳过** (`overridden_by_user: true`), 只对本 Spec 生效, 不改 `.aria/config.json` 全局配置; 规划质量由 Tasks 1.8 的非作者对抗审查兜底 | `detailed-tasks.yaml` 的 `metadata.a2_entry` 记录 |
| 3 | Tasks 1.2 测试移植范围 | **探针作验收 + 关键子集**: `baseline_probe.py` 继续作为验收工具 (Tasks 1.10); 两个测试套件只移植回归关键子集 (每个 W 至少一组) | Spec Tasks 1.2 已按此改写 |
| 4 | GitHub 上已公开的 WP-A 分支 (v4 `b07f69a`, 研究笔记含旁路复现方法) | **删除 GitHub 分支**, origin 保留完整历史。已知局限: 内容已公开约一周, 按提交号仍可能访问到 | 已删除, `ls-remote github` 查无该分支 |
| 5 | PR `10CG/Aria#228` (issue 卫生清扫留痕) | **授权合并** | C.2.4 green (not_applicable: 变更路径无 CI workflow 覆盖, main 上无进行中的运行); C.2.4.5 PASS; 合并提交 `6675291`, 已同步 GitHub, 两端 `ls-remote` 一致 |
| 6 | Aria 审计机制的成本缺陷 | **开 issue**, 先看稿后按稿发布 | `10CG/aria-plugin#209` |

## 仍然有效的约束

- 合并到 aria master、打 tag、发版、主仓版本同步提交与合并, 不在一次性授权内, 到时逐次请示。
- 研究笔记的前向去量化 (Spec 7.20) 仍待 owner 裁定; 本分支合并到 master 之前必须先定。
- 资源纪律: 本会话进程树 nice 19、只用 0–1 号核; 审计席不超过 2; 派单写明实验规模上限。

## 主控的技术级决定 (列此请复议)

1. `detailed-tasks.yaml` 由主控按 Tasks 1.1–1.13 精简生成, 不另派规划 agent。
2. 实现交给 1 个新派 backend-architect 实例, 以 `writer-v6-proto/` 的补丁脚本为起点写成正式代码, 不做批量坏实现回归。
3. Tasks 1.8 拆成两条任务: W14 元耦合同步归实现者; 对抗审查归 1 个非作者 qa-engineer 席。后者即 owner 所说的「单轮审查」。
