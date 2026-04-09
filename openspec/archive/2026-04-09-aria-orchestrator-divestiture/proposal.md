# aria-orchestrator 剥离: 身份澄清 + 子模块移除

> **Level**: Full (Level 3 Spec)
> **Status**: **Rejected (archived 2026-04-09)**
> **Archived**: 2026-04-09
> **Rejection Reason**: 方向错误 — 产品负责人希望 Aria 作为整体项目升级 (v2.0), 不是剥离。参考 GSD 2 (gsd-build/gsd-2) 一体化模型。新讨论见 aria-2.0-integration OpenSpec。
> **Re-confirmed**: 2026-04-09 (state-scanner v2.9 post-merge review, 用户再次确认 "不剥离")
> **Created**: 2026-04-09
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.5.0
> **Discussion**: 5 轮 Agent Team 收敛 (讨论组 4 + 挑战组 3)
> **DRI**: Tech Lead

## Why

第三方使用 aria-orchestrator 的可行性讨论暴露了一个**根本性的方法论矛盾**:

- Aria CLAUDE.md 明确 "❌ 不提供 CI/CD 配置、❌ 不绑定特定 AI 模型、❌ 不提供部署脚本"
- 但 aria-orchestrator 包含: Dockerfile、Nomad HCL、bash 脚本、飞书 webhook 配置、GLM-4.5-Air 集成
- aria-orchestrator 当前唯一真实部署是 Aether light-1 单一节点 (n=1)
- 5 轮 Agent Team 讨论一致裁定: **aria-orchestrator 不是 Aria 方法论的必要组成部分，而是 Aether 项目的运维产物**

### 讨论收敛过程

```
R1: 路径 A (第三方自部署) — 讨论组 4 票通过
    挑战组反对: 事实纠正 (ARIA_PROJECT_DIR 已参数化)、
              工作量低估 (5-7d vs 4-6h)、
              "参考实现" 标签法律无效

R2: 分裂为 X (删除) / Y (修硬约束) / 极简 三立场
    挑战组洞察: 三立场是时间阶段非互斥、aria-orchestrator 已是独立仓库

R3: 5 阶段执行计划 (DRI 裁定身份)
    挑战组反对: 历史 tag 责任、SCOPE.md 位置、工时再修正

R4: 锁定细节 (DISCLAIMER 独立、SCOPE.md 双写、CHANGELOG 前置声明)
    挑战组: 全部 "无阻塞反对"，仅细节建议

R5: 集成 R4 全部建议，DRI 最终签字
    挑战组: 全部 "✅ 接受", 收敛达成
```

### 关键决策记录

| ID | 决策 | 理由 | 来源 |
|----|------|------|------|
| **D1** | aria-orchestrator 不是 Aria 方法论组成部分，是 Aether 运维产物 | DRI 裁定 (R3 tech-lead) | 5 轮一致 |
| **D2** | CLAUDE.md 硬约束保持不变 | 修改硬约束会破坏 #1-#5 规则权威性，引发滑坡 | R3 QA + R4 全员 |
| **D3** | 拒绝路径 B (多租户) 和 C (SaaS) | 违反 "不做 CI/CD"、"不绑定 AI 模型" 硬约束；超出研究项目定位 | R1-R2 一致 |
| **D4** | 主仓库通过 git rm 移除子模块引用，独立仓库保留 | aria-orchestrator 已是独立仓库，rm 只删指针 | R2 Code Reviewer 实锤 |
| **D5** | scan.sh Level 漂移修复为独立 P0 (rename 方案) | 方法论可重现性的底线，与剥离决策无耦合 | R3 全员 |
| **D6** | DISCLAIMER.md 独立文件，不合并到 SCOPE.md | 法律工具识别度优先 | R4 Legal |
| **D7** | SCOPE.md 双写 (主仓库子模块路径 + 独立仓库根) | 过渡期可见性 + P4 后永久声明 | R4 architect/knowledge-manager |
| **D8** | CHANGELOG v1.4.x 废弃声明 P1 前置执行 | 历史 tag 责任尽早切割 | R4 tech-lead |
| **D9** | 撤回 /dispatch-agent Skill 提案 | Skill 在 session 内 shell-out claude -p 有 token 叠加 + 无流式 | R3 ai-engineer |
| **D10** | US-007 标注 "[路径已变更]" 而非 "[已废弃]" | 语义精确，需求未废弃，仅实现路径迁移 | R4 QA |
| **D11** | 不重命名为 aria-runtime-reference | 由 Aether 团队接管后自行命名，避免延续 aria- 前缀 | R3 tech-lead |
| **D12** | PRIVACY.md 不必须 (仅在处理 PII 时立项) | aria-orchestrator 不处理用户个人数据 | R5 DRI + Legal 接受 |

### 被拒绝的方案

- **路径 A 原版** (R1): 用"参考实现"标签掩盖矛盾，4-6h 估算错误 10 倍
- **方案 Y** (R2 knowledge-manager): 修改 CLAUDE.md 硬约束 — 滑坡风险，权威性自我腐蚀
- **方案 C** (SaaS): 与方法论研究身份不可调和
- **重命名为 aria-runtime-reference**: 延续 aria- 前缀模糊归属
- **PRIVACY.md**: 当前数据范围不构成 GDPR PII

## What

### 1. scan.sh Level 漂移修复 (P0, 独立)

**问题**: scan.sh 中 `level` 变量 (1=quick-fix, 2=OpenSpec, 3=讨论) 与 `standards/openspec/project.md` 的 OpenSpec Level 定义 (1=Skip, 2=Minimal, 3=Full) **语义不一致**，造成方法论可重现性破坏。

**修复方案**: variable rename `level` → `complexity_tier`
- aria-orchestrator/scan.sh (19 处实测引用)
- aria-orchestrator/schema/scan-result.json
- aria-orchestrator/skills/heartbeat-scan/SKILL.md
- 不引入对 standards 子模块的运行时依赖

### 2. 身份澄清三件套

**主仓库** (P1):
- README 加粗品牌声明: "aria-orchestrator 是 Aether 运维参考实现，非 Aria 方法论组成部分"
- CHANGELOG.md v1.4.x 段落追加废弃声明 + 交叉引用 `2026-04-09-heartbeat-observability` 归档
- MEMORY 索引: `feedback_feishu_hermes_gotchas.md` 描述行更新为中性表述

**独立仓库 aria-orchestrator/ 根目录** (P3):
- **SCOPE.md** — 项目边界声明 (内容: Aether 运维产物，非 Aria 方法论)
- **DISCLAIMER.md** — 独立法律文件 (含 "无主动维护承诺" 条款)
- **DEPENDENCIES.md** — Hermes/GLM-4.5-Air/飞书 license 审查
- **CONTRIBUTING.md** — bug/feature 分类策略 + 无 SLA 承诺
- **ISSUE_TEMPLATE.md** — 强制版本/环境信息

### 3. Aether 部署迁移 (P2)

**前置 ssh 调查**:
```bash
ssh light-1 "nomad job inspect aria-orchestrator-light | grep -iE 'source|path|artifact'"
ssh light-1 "find /etc/nomad.d /opt/nomad -name '*orchestrator*' 2>/dev/null"
ssh light-1 "systemctl list-units --all | grep orchestrator; crontab -l | grep orchestrator"
ssh light-1 "docker ps -a | grep orchestrator; podman ps -a 2>/dev/null | grep orchestrator"
```

**迁移**: 从主仓库子模块路径迁移到独立 clone (具体步骤待 ssh 调查后确定)

### 4. 子模块切割 (P4)

**前置: openspec 归档** (独立提交):
```bash
mv openspec/changes/aria-orchestrator/proposal.md \
   openspec/archive/2026-04-09-aria-orchestrator-removal/proposal.md
git add openspec/ && git commit -m "archive: aria-orchestrator openspec before submodule removal"
```

**切割命令**:
```bash
git submodule deinit -f aria-orchestrator
git rm -f aria-orchestrator
rm -rf .git/modules/aria-orchestrator
# 手动编辑 .gitmodules 删除 [submodule "aria-orchestrator"] 段
git config --file .gitmodules --list | grep orchestrator  # 应无输出
git ls-files | grep orchestrator                          # 最终 gate, 应无输出
git commit -m "..."
```

**主项目同步**:
- US-007.md: 添加 "[路径已变更 - aria-orchestrator 迁移至独立仓库]" 标注
- US-005.md: 同步引用更新 (如有)
- VERSION + CHANGELOG: v1.5.0 release notes 含 "aria-orchestrator 子模块不再内嵌"

### 范围边界 (本 Spec 不做)

- ❌ 不修改 CLAUDE.md 硬约束 (D2)
- ❌ 不创建 PRIVACY.md (D12)
- ❌ 不重命名 aria-orchestrator (D11)
- ❌ 不实现 /dispatch-agent Skill (D9)
- ❌ 不删除独立仓库 aria-orchestrator (仅删主仓库引用)
- ❌ 不在主仓库保留 stub/指针 (双写策略 P4 后主仓库无内容)

## Acceptance Criteria

### Phase 0: scan.sh Level 漂移修复
- [ ] scan.sh 中 19 处 `level` 引用全部 rename 为 `complexity_tier`
- [ ] schema/scan-result.json 同步更新字段名
- [ ] skills/heartbeat-scan/SKILL.md 文档更新
- [ ] 手动回归测试: scan.sh 输出 JSON 格式正确，by_level 聚合正确
- [ ] 与 standards/openspec/project.md 的 Level 定义无语义混淆

### Phase 1: 主仓库身份澄清
- [ ] aria-orchestrator/README.md 首行加粗品牌声明
- [ ] CHANGELOG.md v1.4.0 + v1.4.1 段落追加废弃声明
- [ ] CHANGELOG 交叉引用 `openspec/archive/2026-04-09-heartbeat-observability/`
- [ ] feedback_feishu_hermes_gotchas.md description 行改为中性表述

### Phase 2: Aether 迁移
- [ ] ssh light-1 调查完成，部署路径已确认
- [ ] 迁移到独立 clone (具体路径由调查结果决定)
- [ ] 心跳服务在新路径上运行验证 (至少 1 次完整 cron 周期)

### Phase 3: 独立仓库运维文档
- [ ] aria-orchestrator/ 独立仓库根目录新增 SCOPE.md
- [ ] aria-orchestrator/ 独立仓库根目录新增 DISCLAIMER.md (含 "无主动维护承诺")
- [ ] aria-orchestrator/ 独立仓库根目录新增 DEPENDENCIES.md (Hermes/GLM/飞书 license)
- [ ] aria-orchestrator/ 独立仓库根目录新增 CONTRIBUTING.md
- [ ] aria-orchestrator/ 独立仓库根目录新增 ISSUE_TEMPLATE.md
- [ ] 主仓库 aria-orchestrator/ 子模块路径同步以上文件 (双写)

### Phase 4: 子模块切割 + 主项目清理
- [ ] openspec/changes/aria-orchestrator/proposal.md 归档 (独立提交)
- [ ] `git submodule deinit -f aria-orchestrator` 执行成功
- [ ] `git rm -f aria-orchestrator` 执行成功
- [ ] `.gitmodules` 中无 `[submodule "aria-orchestrator"]` 段
- [ ] `.git/modules/aria-orchestrator` 已删除
- [ ] `git config --file .gitmodules --list | grep orchestrator` 无输出
- [ ] `git ls-files | grep orchestrator` 无输出 (最终 gate)
- [ ] US-007.md 添加 "[路径已变更]" 标注 + 链接独立仓库
- [ ] 主项目 VERSION → v1.5.0
- [ ] 主项目 CHANGELOG.md v1.5.0 段落含 "aria-orchestrator 子模块移除"

## 总工时

| Phase | 工时 | 累计 |
|-------|------|------|
| P0 | 4h | 4h |
| P1 | 3h | 7h |
| P2 | 4h | 11h |
| P3 | 4h | 15h |
| P4 | 5h | 20h |
| **总计** | **20h ≈ 2.5d** | |

## 参与 Agents (5 轮收敛)

**讨论组** (4): aria:tech-lead (DRI), aria:backend-architect, aria:knowledge-manager, aria:ai-engineer
**挑战组** (3): aria:qa-engineer, aria:code-reviewer, aria:legal-advisor

**收敛轮次**: R1 → R2 → R3 → R4 → R5 (5 轮)
**最终判定**: R5 挑战组 3/3 表态 "无阻塞反对"

## 相关 OpenSpec

- [aria-orchestrator](../aria-orchestrator/proposal.md) — 父 Spec (将在 P4 归档)
- [heartbeat-observability](../../archive/2026-04-09-heartbeat-observability/proposal.md) — 关联归档
