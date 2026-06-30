---
track-id: m6-runtime-remediation
owner-container: simonfish/dev-claude
phase: make-ready
status: complete
updated-at: 2026-06-30T05:30:00Z
---

# Aria — Session Handoff (2026-06-30) — M6 #147 runtime remediation → 168h 跑 now make-ready

> **Status**: complete — M6 Layer1 runtime 降级 (#147) 逐项修复 + prod tick 验证; 168h 跑现 100% AI-side make-ready, 剩 owner 运营仪式。
> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` → §6。

## §0 入口 (新 session 优先读)
1. **本 session 主线**: 起于 `/state-scanner` 等待期偶然发现 M6 acceptance `check-m6-e2e-acceptance.py` AC-6 pre-flight 闸 **false-green** → 修 (#146/PR #26) → 为启动 168h 跑查 light-1 集群 → **深挖出 M6 Layer1 runtime 全面降级** (误以为"只差启动")→ 开 #147 逐项修复 → **168h 跑 now make-ready**。
2. **认知大纠正**: M6 不是"差一个启动动作", 之前是 runtime 降级 (LLM 旧日志误读/Feishu 断/stale deploy/tick 空转); 现已全修复 + prod 05:00 tick 验证。
3. **剩余 = owner 不可代劳的 168h 运营仪式** (pre-flight → Day-1 anchor → B4-label → 每日 probe → corpus+评分 → AC-5)。AI 侧阻塞全清。
4. 详尽 trail: CLAUDE.md footer 2026-06-30 + Forgejo #147 (多条评论) + 3 审计报告 `.aria/audit-reports/`。

## §1 已完成 (按时间顺序)
1. **CLAUDE.md footer 悬空 staged 编辑** 收 (`4539df2`)。
2. **M7 agent 集合库 deep-research** (owner A+B): VoltAgent/awesome-claude-code-subagents 首选 + wshobson/agents 确认血缘源; cherry-pick 非整库 vendor。notes `2026-06-27-agent-collection-backing-library-research.md` + #128 评论 + memory (`b716604`)。
3. **M6 启动 runbook** `.aria/probes/m6-7d-run-startup-checklist.md` (`1b5653e`)。
4. **AC-6 false-green 修复 (#146 → PR #26 `dd52d34`)**: 占位检测 (3 非占位 dispatch_id + provenance∈{A,B,C}); **audit-engine pre_merge 3 轮收敛** (R2 qa 抓 R1 修复自身引入的 `[:3]` 窗口二次假绿) → R3 PASS; spec §A.8 RESOLVED; #146 closed。
5. **M6 runtime live 诊断 (#147)**: aether-status + deploy-doctor → **真核实纠正 deploy-doctor 4 处**; 实地 root@light-1 诊断。
6. **#147 逐项修复**: B1 Luxeno (实地核实早已配, z.ai 是 stale 进程旧日志); B2 Feishu WS (凭据有效+egress 通, gateway 重启复连稳定); B3 stale (重启重载 0.4.0); **B4-code issue_type_hint (PR #28)** audit-engine **2 轮收敛 PASS** (R1 qa REVISE 2 important: gate-chain 两半未合验 + 三类型仅测 bug); B5 scan.sh exit 127 (PR #27)。
7. **节点 fetch 凭据卡点**: 只读 deploy key (forgejo SSH user=**forgejo** 非 git) 注册两 repo + remote 切 ssh。
8. **#28 部署 light-1** (git pull + submodule a7afaaa, pip editable); **M1 handoff 放置** (prod 05:00 tick 验证 "not found" 消失); 镜像 claude-m5-91b8975-v11 ∈ registry; feature/stale labels 建。
9. **CLAUDE.md 项目状态更新** make-ready (`f7498e6`)。

**Cycles shipped this session**: AC-6 fix (PR #26) + B5 scan.sh (PR #27) + B4-code (PR #28), 均 aria-orchestrator 侧; 主仓多 doc/gitlink commits; **无 aria-plugin 版本变更**。

## §2 未完成 / Carry-forward 清单

### 高优先级
- **M6 168h 运营仪式 (owner, 不可 AI 代劳)**: pre-flight 3 dispatch (选 provenance) → 落 Day-1 alloc anchor (启动时钟) → 跑 `.aria/probes/seed-aria-auto-issues.sh --apply` (B4-label, 造 ≥10 aria-auto issue) → 每日 probe + Day-3 闸 → corpus 采集 + **owner 7 维评分 (AC-5 median≥7)** → acceptance gate → 归档 #2。

### 中优先级
- **Feishu WS 稳定性观察**: B2 gateway 重启后 WS 连 `msg-frontier.feishu.cn` 稳定**仅观察 3+ min**; owner 留意未来数小时是否保持。若再现 keepalive 掉线 → 查网络 conntrack (凭据/egress 已排除)。

### 低优先级 / cleanup
- **B4-label 故意未跑** (造 issue=启动自主派发, 须 Day-1 anchor 后做, 见 §4)。
- **M1 handoff 校验器对运行时副本 FAIL** = memo_path 相对路径假象 (repo 原件 PASS, tick 不跑校验器), 非内容错; 可忽略或日后把 memo 也放运行时目录。
- **gateway heartbeat scan.sh 循环**: B5 修复 (PR #27) 已在节点 submodule (a7afaaa); gateway 长驻进程可能仍用旧 skill 缓存, 下次 gateway 重启后彻底消除 (无害)。
- **#147 保持 open** (跟踪 owner 运营仪式); M6 #2 spec 待 168h 跑后归档。

## §3 关键风险 / 已知陷阱
1. **长驻进程加载旧模块 vs editable 磁盘已更新**: gateway (2026-05-22 启动) 跑旧代码而磁盘是 0.4.0 → "no register()"/z.ai 旧日志是这来的; cron tick (每小时新进程) 立即用新代码, gateway 需重启。
2. **stale 日志误读为现状**: deploy-doctor 把 May-12 的 z.ai 429 旧缓冲读成"当前", 须看时间戳/最新窗口判断 ([[feedback_verify_agent_diagnosis_against_live_state]])。
3. **B4-label 时序**: 造 dispatch 语料 = 启动自主实验, 别在 make-ready 阶段/泛指"继续"时触发 ([[feedback_experiment_start_action_not_generic_prep]])。
4. **forgejo SSH user = forgejo (非 git)**; 内网 192.168.69.200:22 / 外网 cloudflared ([[reference_forgejo_ssh_node_deploy_key]])。

## §4 实战教训 (memory 沉淀来源)
本 session 5 条 memory (见 §8)。核心:
- 多轮收敛审计抓单轮漏的 bug (含修复自身引入的回归) — 两个 cycle (PR #26 R2 / PR #28 R1) 都是 qa REVISE 抓到真缺口。
- 诊断 agent 结论须对 live state + 真代码核实再转述 ('running'≠健康, '仓库有'≠'部署有')。
- make-ready vs 启动实验的纪律。

## §5 多维度同步状态
| 维度 | 状态 |
|------|------|
| 多远程 parity | ✅ 全 equal: main `f7498e6` / standards `350a7cf` / aria `daa3945` / aria-orchestrator `a7afaaa` (origin+github) |
| OpenSpec | 4 active (M6 #2/#4 + M7 ×2); #2 待 168h 跑后归档; consistency_check 4 advisory flag = **已知 Aria-self UPM 缺口** (无 runtime UPM, fixture-only, 非真不一致) |
| Forgejo issues | #146 closed (AC-6); #147 open (M6 runtime, 剩 owner 仪式); #128 (M7 tracker) |
| aria-plugin | 版本不变 (v1.50.1); 本 session 全在 aria-orchestrator + 主仓 |
| 节点 (light-1) | aria-orchestrator a7afaaa 部署; deploy key + ssh remote; M1 handoff 放置; tick prod 验证 OK |

## §6 Next session 入口 + 优先级建议
**命令**: `/aria:state-scanner`。
**优先级建议**:
1. ⭐ **M6 168h 跑** (owner kickoff — 唯一主线推进点; AI 可辅助 pre-flight 验证/probe 起草/acceptance 评分, 但 anchor+评分+启动是 owner)。
2. Feishu WS 稳定性复查 (数小时后)。
3. 等待期填空: M7 立项 (受 M6 ship 门) / open issue triage。
**不应该做的**: 别在 owner 正式 kickoff 前跑 B4-label / 落 anchor (出窗口浪费); 别重启 gateway 除非必要。

## §7 提交清单 (multi-remote parity)
| 仓 | 分支 | HEAD | origin | github |
|----|------|------|--------|--------|
| 主仓 Aria | master | `f7498e6` | ✅ | ✅ |
| aria-orchestrator | master | `a7afaaa` (PR #27+#28) | ✅ | (单 origin) |
| aria-plugin | master | `daa3945` (未变) | ✅ | ✅ |
| standards | master | `350a7cf` (未变) | ✅ | ✅ |

**PRs merged**: aria-orchestrator #26 (AC-6) / #27 (scan.sh) / #28 (issue_type_hint)。**Tags**: 无 (无插件版本变更)。

## §8 Memory entries this session (5 new)
1. `feedback_multiround_audit_catches_fix_introduced_regression` — 加固防-false-pass 闸时加固本身可能重开同类 bug; 多轮审计 R2 抓到。
2. `feedback_verify_agent_diagnosis_against_live_state` — 诊断 agent 结论须对 live state+真代码核实; 'running'≠健康; '仓库有'≠'部署有'。
3. `reference_agent_collection_backing_libraries` — M7 集合库候选 (VoltAgent 首选/wshobson 血缘源)。
4. `reference_forgejo_ssh_node_deploy_key` — forgejo SSH user=forgejo; 节点 deploy key + pip editable cron tick 自动生效。
5. `feedback_experiment_start_action_not_generic_prep` — make-ready vs 启动实验纪律; 别让泛指"继续"触发启动动作。

## Cross-references
- CLAUDE.md footer 2026-06-30 / Forgejo #147 / `.aria/audit-reports/pre_merge-R3-*-m6-ac6-146-*` + `pre_merge-R2-*-m6-b4-*` / runbook `.aria/probes/m6-7d-run-startup-checklist.md` + `seed-aria-auto-issues.sh`

**Created**: 2026-06-30 EOD
**Status**: complete — next session 主推 M6 168h 跑 (owner kickoff)
