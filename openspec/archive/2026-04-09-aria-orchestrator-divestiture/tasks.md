# aria-orchestrator-divestiture: Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Total**: 20h ≈ 2.5d, 5 阶段
> **Strategy**: P0 可独立并行, P1-P4 顺序执行

## P0 — scan.sh Level 漂移修复 (4h, 独立 P0)

> **Owner**: Backend Architect
> **依赖**: 无 (可立即执行)

- [ ] T0.1 grep 并定位 scan.sh 中 19 处 `level` 引用 (1h)
- [ ] T0.2 rename `level` → `complexity_tier` (含 by_level → by_complexity_tier 聚合) (1h)
- [ ] T0.3 同步更新 schema/scan-result.json 字段名 (0.5h)
- [ ] T0.4 同步更新 skills/heartbeat-scan/SKILL.md 文档 (0.5h)
- [ ] T0.5 手动回归测试: `bash scan.sh /home/dev/Aria --json` 验证输出 (1h)

**验收**: 与 standards/openspec/project.md Level 定义无语义混淆

---

## P1 — 主仓库身份澄清 (3h)

> **Owner**: Tech Lead (人类确认措辞)
> **依赖**: P0 完成

- [ ] T1.1 aria-orchestrator/README.md 首行加粗品牌声明 (0.5h)
  ```markdown
  > **⚠️ aria-orchestrator 是 Aether 运维参考实现，非 Aria 方法论组成部分。**
  > Aria 核心库见 [aria-plugin](https://github.com/10CG/aria-plugin)。
  ```
- [ ] T1.2 主项目 CHANGELOG.md v1.4.0 + v1.4.1 段落追加废弃声明 (0.5h)
  ```markdown
  > **NOTE**: 此版本包含 aria-orchestrator 子模块指针。
  > v1.5.0 起子模块已移除，aria-orchestrator 迁移至独立仓库。
  > 旧 tag checkout 仍可拉取子模块，但不受主项目支持。
  ```
- [ ] T1.3 CHANGELOG 交叉引用 `openspec/archive/2026-04-09-heartbeat-observability/` (0.5h)
- [ ] T1.4 更新 MEMORY 文件 `feedback_feishu_hermes_gotchas.md` description 行为中性表述 (0.5h)
  ```
  原: 部署 aria-orchestrator 时发现...
  改: 部署 Hermes Agent + Feishu 集成时发现...
  ```
- [ ] T1.5 显式提交 (独立 commit, 不与 P4 合并) (1h)

**验收**: P1 提交后, 即使 P4 未执行, 用户也能从 CHANGELOG 看到废弃声明

---

## P2 — Aether 部署迁移 (4h)

> **Owner**: Backend Architect + 运维 (人类执行 ssh)
> **依赖**: P1 完成

- [ ] T2.1 ssh light-1 调查 (1h)
  ```bash
  ssh light-1 "nomad job inspect aria-orchestrator-light | grep -iE 'source|path|artifact'"
  ssh light-1 "find /etc/nomad.d /opt/nomad -name '*orchestrator*' 2>/dev/null"
  ssh light-1 "systemctl list-units --all | grep orchestrator"
  ssh light-1 "crontab -l | grep orchestrator"
  ssh light-1 "docker ps -a | grep orchestrator; podman ps -a 2>/dev/null | grep orchestrator"
  ```
- [ ] T2.2 记录调查结果到 `/tmp/aether-orchestrator-survey.md` (0.5h)
- [ ] T2.3 根据调查结果决定迁移路径 (0.5h)
  - 如果是 git artifact: 改 artifact URL 指向独立仓库
  - 如果是 bind mount: 在独立路径 clone, 修改 mount
  - 如果是 raw_exec /opt/aria-orchestrator/: 替换内容来源
- [ ] T2.4 执行迁移 + Nomad job 重新部署 (1.5h)
- [ ] T2.5 验证心跳: 至少 1 次完整 cron 周期 + 飞书消息送达 (0.5h)

**验收**: light-1 不再依赖主仓库子模块路径, 心跳持续运行

**回滚方案**: 如失败, Nomad job 恢复旧 spec, 心跳服务恢复原状, 重新评估

---

## P3 — 独立仓库运维文档套件 (4h)

> **Owner**: 法务 (DISCLAIMER) + Backend Architect (其他)
> **依赖**: P2 完成

**写入位置**: aria-orchestrator 独立仓库根目录 (主仓库子模块路径自动同步, 双写策略)

- [ ] T3.1 SCOPE.md (0.5h)
  - 项目边界: Aether 运维产物
  - 与 Aria 关系: 非 Aria 方法论组成部分
  - 维护责任: Aether 运维团队
- [ ] T3.2 DISCLAIMER.md (1h, 人类法务确认)
  - MIT 标准免责
  - "无主动维护承诺" 条款
  - "更新周期与 Aria 主项目一致, 不单独保证 Hermes/Feishu/GLM 兼容性"
- [ ] T3.3 DEPENDENCIES.md (1h)
  - Hermes Agent (NousResearch): MIT, 无商用限制
  - GLM-4.5-Air (智谱): 商用条款 (含中国数据留存说明)
  - 飞书 OpenAPI: ToS 链接 + 第三方应用申请说明
  - Anthropic Claude API (claude -p): 商用条款链接
- [ ] T3.4 CONTRIBUTING.md (0.5h)
  - bug 报告: 接受, 需附 Aria 版本 + 部署环境
  - feature 请求: 需提交 OpenSpec 或 GitHub Discussion
  - 无 SLA, 优先级基于社区投票
- [ ] T3.5 ISSUE_TEMPLATE.md (0.5h)
  - 强制字段: aria 版本, aria-orchestrator commit, Hermes 版本, 部署环境
- [ ] T3.6 提交到独立仓库, 主仓库 git submodule update 同步指针 (0.5h)

**验收**: 独立仓库根目录有完整文档套件, 主仓库子模块路径同步

---

## P4 — 子模块切割 + 主项目清理 (5h)

> **Owner**: Backend Architect (执行) + 人类 (review commit)
> **依赖**: P3 完成 + Aether 验证通过

### Phase 4a: openspec 归档 (前置独立提交)

- [ ] T4.1 创建归档目录 (0.25h)
  ```bash
  mkdir -p openspec/archive/2026-04-09-aria-orchestrator-removal
  mv openspec/changes/aria-orchestrator/proposal.md \
     openspec/archive/2026-04-09-aria-orchestrator-removal/
  rmdir openspec/changes/aria-orchestrator
  ```
- [ ] T4.2 在归档 proposal.md 顶部追加迁移去向说明 (0.25h)
  ```markdown
  > **MOVED**: aria-orchestrator 已剥离为独立仓库,
  > 详见 OpenSpec aria-orchestrator-divestiture
  ```
- [ ] T4.3 独立提交 (0.5h)
  ```bash
  git add openspec/
  git commit -m "archive: aria-orchestrator openspec before submodule removal"
  ```

### Phase 4b: 子模块切割

- [ ] T4.4 deinit 子模块 (0.25h)
  ```bash
  git submodule deinit -f aria-orchestrator
  ```
- [ ] T4.5 git rm 子模块 (0.25h)
  ```bash
  git rm -f aria-orchestrator
  ```
- [ ] T4.6 清理 .git/modules (0.25h)
  ```bash
  rm -rf .git/modules/aria-orchestrator
  ```
- [ ] T4.7 手动编辑 .gitmodules 删除 `[submodule "aria-orchestrator"]` 段 (0.25h)
- [ ] T4.8 验证清理 (0.5h)
  ```bash
  git config --file .gitmodules --list | grep orchestrator   # 应无输出
  git ls-files | grep orchestrator                            # 最终 gate, 应无输出
  git status                                                  # 确认变更
  ```

### Phase 4c: 主项目文档清理

- [ ] T4.9 US-007.md 标注更新 (0.5h)
  ```markdown
  > **Status**: in_progress
  > **[路径已变更]**: aria-orchestrator 实现已迁移至独立仓库,
  > 详见 OpenSpec aria-orchestrator-divestiture
  ```
- [ ] T4.10 检查 US-005.md / 其他文档中的引用并更新 (0.5h)
- [ ] T4.11 更新 CLAUDE.md "信息地图" 移除 aria-orchestrator 条目 (0.25h)
- [ ] T4.12 主项目 VERSION → v1.5.0 (0.25h)
- [ ] T4.13 CHANGELOG.md v1.5.0 段落 (0.5h)
  ```markdown
  ## [1.5.0] - 2026-04-XX
  ### Removed
  - **aria-orchestrator 子模块** — 剥离为独立运维参考实现
    - 决策: 5 轮 Agent Team 收敛, DRI 裁定为 Aether 运维产物
    - 影响: 子模块不再内嵌, 用户需独立部署
    - 详见 OpenSpec aria-orchestrator-divestiture (Level 3)
  ```
- [ ] T4.14 提交 release v1.5.0 + tag + push (0.5h)
- [ ] T4.15 归档本 OpenSpec 到 `openspec/archive/2026-04-XX-aria-orchestrator-divestiture/` (0.25h)

**验收**: 主仓库零 aria-orchestrator 引用, v1.5.0 已 tagged 和 pushed

---

## 总览

| 阶段 | 工时 | Owner | 依赖 |
|------|------|-------|------|
| P0 | 4h | Backend Architect | 无 (独立 P0) |
| P1 | 3h | Tech Lead | P0 |
| P2 | 4h | Backend Architect + 运维 | P1 |
| P3 | 4h | 法务 + Backend Architect | P2 |
| P4 | 5h | Backend Architect + 人类 | P3 |
| **总计** | **20h ≈ 2.5d** | | |

## 风险与回滚

- **P0 失败**: scan.sh rename 引入 bug → git revert, 影响范围仅 aria-orchestrator
- **P2 失败**: Aether 部署中断 → Nomad job 回滚, 心跳服务恢复
- **P4 失败**: git rm 后发现遗漏引用 → git revert, 重新规划清理
- **整体回滚**: P1 之前可完全无痕回滚; P2 之后需要逆向迁移

## 不需要测试的部分

- DEPENDENCIES.md, DISCLAIMER.md 等纯文档变更 (人类 review 即可)
- CHANGELOG / VERSION 等元数据更新

## 参考文档

- [proposal.md](./proposal.md) — 详细决策记录
- [CLAUDE.md](../../../CLAUDE.md) — Aria 项目硬约束
- [US-007](../../../docs/requirements/user-stories/US-007.md) — 父 User Story
