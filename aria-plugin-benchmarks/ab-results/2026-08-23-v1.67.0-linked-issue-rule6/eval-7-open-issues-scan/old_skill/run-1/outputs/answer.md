已按 state-scanner Step 0 机械跑完 `scan.py` (退出码 10 = 部分软错误, snapshot 可用; 唯一一条 `errors[]` 是 AC-5 跨 remote 一致性自检在 164 条历史 handoff 上无法评估, 属已知问题 Aria #176, 只影响「parity 裁决可信度」, 不影响 issue 扫描)。以下是扫描结果。

## 📍 当前状态

- 分支: `feature/linked-issue-normalization` (与 origin 同步, ahead 0 / behind 0); 无 git 中间态, 无中断的 workflow
- UPM: 未配置 (无 Phase / Cycle 信息)
- 变更文件: 2 个 (子模块 `aria` 工作区与 gitlink 不一致 + 1 个未跟踪的 benchmark 目录), 无代码/测试变更 → 复杂度 Level 1
- 关联 OpenSpec: `linked-issue-normalization` (status pending, 最近 5 个 commit 全是它的 post_planning R5 审计 + owner override 进 Phase B)

## 📊 变更分析

变更类型: other 2 / code 0 / docs 0 / test 0 | 架构影响: 否 | 测试覆盖: 无 | Skill 变更: 未检出

## 📄 需求状态

- PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved, 归一为 pending)
- User Stories 21 条: done 17 / in_progress 2 / approved 1 / pending 1

## 🏗️ 架构状态

`docs/architecture/system-architecture.md` 存在, Active, 最后更新 2026-05-27。**需求链路 `chain_valid=false`** (Parent PRD 未识别) — 这是 aria-plugin #151 描述的正则问题 (文档有链接但带限定词), 非真缺失。

## 📋 OpenSpec 状态

- 活跃变更 9 个: approved 7 / pending 2 (`linked-issue-normalization`, `a1-entry-claim-duplicate-work-guard`); 已归档 138; 待归档 0
- ⚠️ 设计未实施 6 个 (全是 Aria 2.0 轨, approved 但 tasks 大量未勾): m6-release-closeout (41/41 未做, 89 天) / m7-agent-lifecycle (65 天) / m6-dispatch-input-delivery (49 天) / m6-cost-model-telemetry (44 天) / m6-e2e-resilience (41 天) / m7-fleet-aggregation (34 天) — 与 CLAUDE.md 「卡 owner/基建门」描述一致

## 🛡️ 审计状态

审计系统 enabled。最近报告 `.aria/audit-reports/linked-issue-normalization-audit-trail.md`, 但 collector 没解析出 verdict / checkpoint / 收敛轮数 (字段为 null); 按 git log, post_planning R5 结论是 **FAIL 不收敛, owner override 进 Phase B** (Rule #10 已留痕)。

## 🔧 自定义检查

`.aria/state-checks.yaml` 已配置, 本次无 FAIL / STALE 项。

## 🔄 同步状态

- 当前分支: ahead 0 / behind 0, 证据新鲜 (刚 fetch)
- 多远程 (origin + github): origin parity equal; github 对本 feature 分支无 tracking ref (`parity=unknown`, 正常 — feature 分支没推 github)。`overall_parity=true`, 但因上面那条 AC-5 错误, 本次裁决**视为未验证**
- 子模块 `aria`: 工作区 HEAD (0fe2e0d) ≠ gitlink (9e6a17c) ≠ 远程 (a0fe720), 远程领先 15 commit → 建议 `git submodule update --remote aria` (只读模式下我没动)
- gitlink 完整性: origin 三个子模块全 ok; github 侧三个均 `no_published_ref` (feature 分支未发布到 github, 非 orphaned)
- 📝 README 版本: aria plugin.json 1.66.4 = README 1.66.4 一致
- 🔗 Forgejo 配置: 检出 forgejo.10cg.pub 远程, 但 `.aria/forgejo.json` 缺失 (可运行 /forgejo-sync 引导创建)
- 🌲 多终端: 扫到 8 条分支, collision kind = `self_multi_container` (dev-claude 与 simonfishgit/dev-claude; aria-runner-bot/023236f2 与 simonfish/bfe8285d) — 进 Phase B 前会触发 advisory 认领闸 (本次只扫不调)

## 🎫 Open Issues (Forgejo, 共 44 open, 4 个 repo, 数据来源: cache, 刚获取)

先说判据: 所有 issue **都没有 label**, 所以 scanner 给不出机械的 severity; 下面的「阻塞 / 非阻塞」是我按标题读出来的, 把「会让你做新 feature 时流程本身出错或产生安全/数据风险」的归为阻塞候选。

### A. 建议开新 feature 前先处理 (阻塞候选, 7 条)

| Issue | 为什么算阻塞 |
|---|---|
| Aria #188 | 四维一致性检查恒假阳性 + UPM collector 认不到根 UPM.md — 直接让 state-scanner 自己的输出失真 (本次 UPM 就显示「未配置」) |
| Aria #176 | AC-5 未排除不存在的 remote → scan.py 退出码恒 10 (本次就是这条), 每次扫描都带警告, 真问题会被淹没 |
| Aria #173 | gate_result 在无任务文件时静默 pass — 证据越少越宽松, 归档门假绿 |
| aria-plugin #137 | pre_merge_gate `--main-branch` 缺省 main 而本项目是 master → Rule #8 (b) 腿恒绿 (fail-open)。已挂到 `linked-issue-normalization` spec, CLAUDE.md 记为「已修」, issue 仍 open, 建议核实后关 |
| aria-plugin #156 | Rule #8 (b) 对未被领取的 main run 不可见 (分钟级 fail-open) — 已由 `pre-merge-gate-no-run-for-branch` spec 接手 (approved, 待 Phase B) |
| aria-plugin #136 | branch-manager 合并走服务端 API merge, 违反 CLAUDE.md 硬约束 1, 疑为 #165 镜像分叉三次复发根因 — 任何涉及子模块的 feature 都会踩 |
| Aria #165 | GitHub 镜像漏推第三次复发 (orphaned gitlink) — 与上一条同根, 发布面风险 |

### B. 安全 / 凭据类 (不阻塞开发, 但不该拖, 5 条)

Aria #170 (nomad var put 回显泄漏凭据) / Aria #136 (cost-sentinel 日志打印完整 Feishu webhook, 需轮换) / Aria #151 (两个 10cg-ci-bot token 归属待确认) / aria-plugin #154 (L3 tripwire 凭据形状告警, enhancement) / aria-plugin #138 (secret-guard 跨段 pattern fail-open, v1.66.1 唯一 fail-open 方向)

### C. 已被当前 spec `linked-issue-normalization` 覆盖 (本轨 ship 后应关, 5 条)

Aria #177 (CLAUDE.md:81 发布同步面四错) / aria-plugin #137 / #136 / #134 (test_collision.py sys.path 倒置, 已破 70 天) / #133 (_TERMINAL_STATUSES 4 处定义 2 种成员集)

### D. 多终端协调类 (和你「并行开 feature」直接相关, 5 条)

Aria #180 (claim collision surface 30 分钟后静默失效, heartbeat 零调用) / Aria #174 (跨 track-id 同源重叠检测不到 → 重复实现) / Aria #182 (handoff status 从不收口, 31 条历史仍 active) / aria-plugin #155 (已终结线的 handoff 被当活跃 track, collision 永久误报 — 本次扫描的 `self_multi_container` 碰撞可能就是它) / aria-plugin #135 (认领机制三处缺口, 已致重复劳动 4 次)

### E. secret-guard 残余面 (已知降级为现状, 6 条, 非阻塞)

aria-plugin #146 / #144 / #143 / #142 / #141 / #140 / #139

### F. 规范 / 知识层 / 重构 / 功能请求 (非阻塞, 14 条)

- Aria: #184 (brainstorm 被共装插件绕过) / #178 (hook 类 SC 声明测哪份副本) / #175 (契约 2 重写, 关联 US-025, 需 Level 2 Spec) / #171 (TTY 输出格式 convention) / #169 (AC-5 搬独立 collector) / #168 (false-parity 归档 deferred tracker) / #167 (Forgejo API 可插拔 HTTP) / #164 (第三方项目上报约定) / #120 (切换 aether-build-container)
- aria-plugin: #151 (Parent PRD 正则) / #150 (Rule #6 第三行对 14/43 skill 不可执行) / #149 (audit collector 按 mtime 取错报告 — 本次 verdict=null 可能即此) / #148 (重试循环重复实现)
- aria-standards: #16 (Level 3 交付物两种口径) / #15 (fetch 原则扩展)
- aria-orchestrator: #31 (bot dispatch 强制 claim) / #5 (Hermes on Aether 模板)

启发式关联结果: 44 条里 6 条关联到 OpenSpec (#177/#137/#136/#134/#133 → linked-issue-normalization; plugin #156 → pre-merge-gate-no-run-for-branch), 1 条关联 User Story (#175 → US-025), 其余 37 条无关联。

## 🎯 推荐工作流

当前分支正处在 `linked-issue-normalization` 的 Phase A→B 交界 (owner 已 override 进 Phase B), 而且它本身就是在收 A 组里 3 条 + C 组 5 条。所以推荐:

**[1] (推荐) 先把 `linked-issue-normalization` 走完 Phase B→D** — feature-dev 工作流, 跳过 A.1-A.3 (spec 已 approved-by-override)。理由: 一次 ship 同时关掉 #177 / plugin #137 / #136 / #134 / #133 五条, 顺带把 A 组的 fail-open 闸 (#137) 和合并方式 (#136) 堵上, 之后再开新 feature 踩的坑最少。进 B.1 前会跑 advisory 认领闸 (collision = self_multi_container)。
**[2] 先做 Level 1 hotfix 清 #176 + #188** — 让 scan.py 退出码回到 0、UPM 段不再假「未配置」, 之后每次 state-scanner 输出才可信。不需要 OpenSpec, 但改的是 state-scanner 逻辑, Rule #6 要跑 AB。
**[3] 直接开新 feature (Phase A.1 起 spec)** — 不推荐: 当前分支还挂着一个 pending spec 未 ship, 而且 #180/#174/#155 三条协调缺陷会让并行轨的 claim 保护失效, 先 ship [1] 再开更稳。
**[4] 自定义组合** — 比如先 `git submodule update --remote aria` 对齐子模块, 再 [1]。

你选哪个? 另外两件只读模式下没动、需要你决定的: aria 子模块落后远程 15 commit 要不要先对齐; `.aria/forgejo.json` 缺失要不要跑 /forgejo-sync 建。
