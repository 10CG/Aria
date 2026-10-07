# WP-A Phase A 进度 (会话中途记录, 供中断后续接)

> 正式的会话交接按 Rule #9 写在 `docs/handoff/`; 本文件只是会话中途的进度锚, 防止长会话被额度或其它原因打断后无从续接。最近更新: 2026-10-07 (R5 完成, 未收敛, 待 owner 降级裁定)。

## 目标 (owner 2026-09-30 指令)

按 Aria 规范, 用 agent team + 动态工作流一次做完两件事, 执行前先确认与双子星 (simonfish/bfe8285d, 在做 10CG/Aria#199) 不冲突:

1. **WP-A Phase A**: Level 2 Spec `secret-net-l3-and-bypass-paths` (10CG/aria-plugin#154 / 10CG/aria-plugin#203 / 10CG/Aria#221), 走 A.1 认领 → spec → post_spec 收敛审计 → A.2/A.3 → post_planning 收敛审计。
2. **issue 卫生清扫**: 已完成 (见下)。

## 已完成

- 冲突确认 (2026-09-30 与 2026-10-06 各一次): 四仓 master 两端未变、双子星无新分支 / 提交, 10CG/Aria#199 计划不改 hooks 文件 (只断言 `aria/hooks/hooks.json` 不含 `completeness_gate` 字面)。
- A.1 认领: `secret-net-l3-and-bypass-paths-023236f2` (协调 ref `claims/023236f2/s-3e77@1757.yaml`), 心跳最近 2026-10-07T10:24:05Z (origin `ls-remote` 核验一致)。
- issue 卫生清扫: 六单 triage + 对抗核验 + 改稿 + 发布 (评论 27446 / 27450 / 27451 / 27460 / 27468 / 27471), 只关闭 10CG/aria-plugin#194; 留痕在分支 `docs/issue-hygiene-2026-09-30`, PR 10CG/Aria#228 **待 owner 合并**。
- post_spec R1 (v1 `47aa15f`): 8C/25M/42m → v2 (`b3e3123`) → R2: 1C/15M/34m (定稿 7 簇) → v3 (`c0a6654`) → R3: 0C/12M/23m (去重 10 键) → v4 (`b07f69a`) → R4: 1C/9M/15m (定稿 6 键) → v5 (`6efb9b2`) → R5: 0C/7M/14m (去重 6 键, 4 席 REVISE / km PASS), 均未收敛。报告与主控记录在 `.aria/audit-reports/post_spec-R{1..5}-*`。Critical 6→1→0→1→0, Major (定稿去重) 24→11→10→5→6。R4 六簇五席复核全部关闭 (W 有残余); R5 六个 major 键里 v5 引入 2 个、R4 残余 1 个、既有缺口首次发现 3 个。五席一致表态「定点修补后足以进入 A.2」。**`max_rounds` 5 用尽未收敛 ⇒ MAX_ROUNDS_EXHAUSTED, 待 owner 降级裁定**。

## 进行中 / 下一步

1. **owner 降级裁定** (audit-engine 三选一: 接受当前结论 / 增加轮次 / 降级为单轮, 另加「缩小被审对象」; 同时问簇 X 失败调用盲区的处置方向)。选项与代价见 R5 聚合报告「主控记录」末节。
2. 按裁定执行: 定点修补 (新执笔实例) / 加轮 (派单模板 `dispatch/post_spec-seat-template-r2.md`, 生成器 `tooling/gen_dispatch.py` + `dispatch/mk_round_cfg.py`, 聚合 `tooling/aggregate.py`) / 缩小范围。
3. 收敛判据 (本仓先例口径): 相邻两轮 Critical+Major 键集相等且全票 PASS —— 实际等于连续两轮零 C/M。`max_rounds` 5; 用尽未收敛 ⇒ audit-engine 降级策略三选一由 owner 裁。
4. post_spec 收敛后: task-planner (Level 2 走路径 B, 只出 `detailed-tasks.yaml`) → post_planning 收敛审计。
5. 会话收尾: Rule #9 handoff (`docs/handoff/`, follower 只 prepend `latest.md` History 与 track 表, 不改 bare pointer)。

## 待 owner 裁定 / 复议 (汇总, 详见各处原文)

- PR 10CG/Aria#228 合并; WP-A docs 分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 最终的 PR 与合并。
- proposal「待 owner 复议」节 (L3 是否升级为检测 + 脱敏 / 拒绝文案选项 A-B-C / 10CG/aria-plugin#203 与 10CG/Aria#221 的评论口径 / Level 2 维持与否 / 版本定级 / 建议开单清单等)。
- 各审计轮「主控记录」里的主控裁定 (技术级, 请复议), 含 R2 的主控自我订正。
- issue 卫生清扫各评论里「已提请 owner 决定」的开单事项。

## 流程处置 (AI 判断, 请 owner 复议)

- 2026-10-07 起 WP-A docs 分支**只推 origin、暂停推 GitHub**: R4 km/m6 指出该分支此前已推到公开 GitHub 镜像, 研究笔记与「待 owner 复议」节含未修复旁路的复现方法; 已公开的部分删除需强推 / 删分支 (破坏性), 交 owner 裁。

## 环境要点

- 本机 4 核 ⇒ 每条工作流并发 2; 审计五席分两组, 同时在跑最多 3 席 (audit-engine `hard_cap: 3`)。
- 真 bash 3.2.57 由 v2 执笔从源码构建 (scratchpad `exp/writer-v2/bash32/bash-3.2/bash`); 会话结束后需重建 (方法见 `writer-reports/v2-writer-report.md` §4)。
- 现行 secret-guard 会拦带 `.env` 字样的 `python3 -` heredoc 命令: 写含敏感形状讨论的文字用 Write 工具落文件。
- 周用量额度: 前 16 小时约消耗 1400 万 subagent token 后触顶; 每轮五席审计约 250–320 万。
