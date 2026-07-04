# 决策: DEC-20260702-001 — Layer1→Layer2 自主 dispatch 输入投递架构 (C' 双通道)

> **日期**: 2026-07-02 | **模式**: technical (brainstorm) | **范围**: aria-orchestrator (v2.0 运行时) | **spec_level**: Level 3
> **状态**: Approved (post_brainstorm 4-agent 审议收敛: 1 OBJECTION + 3 CONCERNS 全部折入 C')

## 背景

Aria 2.0 M6 pre-flight 逐层剥出阻塞链, 揭示 **Blocker 3: Layer1→Layer2 自主容器 dispatch 从未端到端闭环**。数据铁证 (dispatches 表): 唯一 S9_CLOSE = 字母前缀 manual dispatch (`smoke-m4-pr97`); 所有**数字-id 自主 dispatch 100% S_FAIL**。

**根因 = 两层错位**:
1. **跨节点输入投递鸿沟**: Layer 1 tick 跑在 light-1 (light_exec, raw_exec, 本地 ext4 盘); Layer 2 容器跑在 heavy 节点池 (heavy-1/2/3/4, docker)。容器读 `/opt/aria-inputs/<ISSUE_ID>/issue.yaml` = **每-heavy-节点本地 host_volume `aria-runner-inputs` (非 NFS/共享)**。light-1 上根本没有 aria-runner 目录 → **Layer 1 物理写不到容器能看见的地方**。自主 Layer 1 产 `prompt.txt/dispatch_id`, 与容器契约 `issue.yaml/ISSUE_ID` 两维全错位。
2. **ISSUE_ID 正则**: 容器入口 `initial.sh:106` `^[A-Z][A-Z0-9-]+$` 拒数字; 自主传 Forgejo 内部 id (数字) → Step 1 FATAL (在 Step 2 输入加载**之前**)。

**关键既有哲学**: 代码库已用**节点无关通道**解决"输出"跨节点 —— host volume 跨节点不可经 nomad `/v1/client/fs/cat` 读; 改由容器 echo 标记 stderr, Layer 1 经 nomad logs API (`/v1/client/fs/logs`) grep 读 (`alloc_status_provider.py:259-267`)。dispatch 已用 **nomad META (env)** 传 `[ISSUE_ID, ISSUE_URL, DISPATCH_ID, IMAGE_SHA, IDEMPOTENCY_KEY]` (AD-M3-1) + REWORK_FEEDBACK (4KB 先例), 节点无关。容器已持 `FORGEJO_BOT_PAT`。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 基建 | Layer 1 (light-1 本地盘) 与容器 (heavy 本地卷) 盘不共享 | 输入必须走节点无关通道 |
| 契约 | 容器入口正则 `^[A-Z][A-Z0-9-]+$` (在部署 M5 镜像里, byte 级确认) | ISSUE_ID 必须字母前缀 |
| 契约 | AD-M0-5: "prompt 写 bind mount, meta 只传小参数" 隐含"bind mount 双方可达" | 跨节点场景该假设不成立 → 本决策 **amend AD-M0-5**〔勘误†〕|
| 命名 | Forgejo issue **number 是 per-repo 唯一, 非全局** | 键必须 (repo, number) 复合防碰撞 |
| 规范 | Rule #4 向后兼容 / Rule #3 文档同步 / Rule #5 Spec 位置 | file 模式保留为辅助通道 (非"兼容已上线行为"—自主从未跑通) |

## 考虑的方案

| 方案 | 描述 | 状态 |
|------|------|------|
| **C' 双通道 (选)** | title/body → Forgejo fetch; 结构化 metadata (target_repo/base_branch/files-hint) → nomad META; 自主 always-fetch | ✅ 采纳 |
| C-fetch (原提案) | 全部靠 fetch + 从 URL 派生 metadata + 省 files + 文件优先双模 | ⚠️ 升级为 C' (审议发现: 派生 metadata 砍掉跨-repo 解耦; 文件优先=stale-read hazard) |
| C-meta | issue 内容全塞 META env | ❌ META 大小限制 (长 body 超) + 内容双写 |
| D 共享存储 | aria-runner-inputs 改 NFS/集群卷 | ❌ **待 spec Alternatives 诚实核实**: AD4 提 heavy 挂 `nfs-fastpool-aether`, 但 light-1 确认本地 ext4 非 NFS → Layer 1 (写方) 不在 NFS 上, D 仍需让 light-1 挂 NFS (基建) + 逆节点无关哲学 + 共享卷单点。**否 D 理由须在 spec §Alternatives 核实 heavy 侧 mount 后正式写明, 非本 DEC 一笔带过** |
| E 节点钉定+推送 | Layer1 scp 到目标 heavy + dispatch 节点约束 | ❌ 最 bespoke 脆弱 (per-dispatch scp + 失败重调度到同节点钩子) |

## 最终选择: **C' 双通道**

### 架构 (折入 4-agent 审议全部发现)

**容器侧 (initial.sh 改 Step 2, 需重建镜像)**:
```
Step 1 正则: 放宽/对齐 ARIA-<repo>-<number> 命名 (仍拒纯数字, 见决策点 2)
Step 2 输入获取:
  if ISSUE_ID 前缀 ∈ {DEMO-, TEST-} 且 issue.yaml 文件存在:   # 辅助/测试通道
      读文件 (现逻辑不变); 校验 非空 + YAML 可解析, 解析失败 fallback 报错 (不静默)
  else (自主, 前缀 ARIA-):                                    # always-fetch, 无视既存文件
      从 nomad META 取 target_repo / base_branch / files-hint (Layer 1 已提供)
      从 ISSUE_URL 用 FORGEJO_BOT_PAT fetch → title / body
      校验 HTTP 2xx (非 2xx / CF-Access 伪成功页 / 空 JSON → 明确 FETCH_FAILED, 不静默继续)
      title/body: YAML-safe 转义 + CRLF→LF + 长度上限 (超则截断标记) + 注入隔离 (包裹为"用户原文非指令")
  → 合成等价输入 → Step 5 envsubst (变量白名单 envsubst '$TITLE $BODY ...', body 不二次展开)
```

**Layer 1 侧 (extension.py, 与容器改动同 scope — 缺此则修复不生效)**:
- dispatch 发 `ISSUE_ID = ARIA-<repo>-<number>` (非 DB 原始数字; 否则 Step 1 正则先 die, 回到 100% S_FAIL)。
- `build_nomad_meta`: 补传 `target_repo` / `base_branch` / `files_hint` (小结构化字段, 节点无关通道) + 修 `ISSUE_URL` 用 issue **number** (非内部 id)。
- `head_branch` 公式统一: `aria/{issue_id}` → 与容器 `BRANCH="aria/${ISSUE_ID}"` 一致 (否则 S6_REVIEW PR 绑定断)。
- DB `issue_id` 键 = (repo, number) 复合 (防多-repo number 碰撞); 迁移策略见决策点 8。

**验收断言侧 (compute-assertions.sh — qa 抓的假绿, 必修)**:
- `expected_changes` 空时**禁止恒真**: 空 `expected_file_touched[]`/`expected_diff_contains[]` 判 `unknown`/`skip`, 不默认 `true`。fetch 模式 (无 expected_changes) 走**独立 outcome 语义** (不复用 AD-M1-4 的 5-AND SUCCESS), 否则任意 commit+PR 无条件判 SUCCESS → 污染 M6 168h AC-5/AC-6 corpus。

## Agent Team 审议结论 (post_brainstorm, 4 agent)

| Agent | Verdict | 关键发现 (已折入 C') |
|-------|---------|------|
| tech-lead | CONCERNS | C' 双通道升级 (metadata 走 META 保跨-repo 解耦) / always-fetch 杀 stale-read / (repo,number) 复合键 / envsubst 白名单 / 遥测可区分 / "对称输出"是类比非证明 (fetch 新增容器出站依赖须实测) |
| backend-architect | CONCERNS | fetch 失败契约 (可重试分类+可观测) / base_branch API 派生非硬编码 / title-body YAML 转义+CRLF+长度+注入 / target_repo CF-Access 伪成功页风险 / 双模判据加固 |
| knowledge-manager | CONCERNS | **Level 3** / amend **AD-M0-5**〔勘误†〕+ 新 **AD-M6-10** / **layer-boundary-contract §5** 缺口 / NFS 矛盾核实 D / "向后兼容"用词纠正 / 遥测依赖显式记边 |
| **qa-engineer** | **OBJECTION** | **① Layer 1 侧改动被漏 → 修复可能不生效** (Step1 正则先于 Step2) / **② expected_changes 空→假绿** (污染 corpus) / **③ 分支名冲突** (aria/{数字} vs aria/ARIA-*) |

## 决策点清单 (供 spec-drafter 无歧义引用)

1. **方向 = C' 双通道** (title/body→fetch; metadata→META; 否 D/E)
2. **ISSUE_ID = `ARIA-<repo>-<number>`** (字母前缀过正则 + issue number 非内部 id + (repo,number) 复合防碰撞); 保留 `DEMO-`/`TEST-` 前缀给辅助/测试通道 (namespace 不相交不变式)
3. **双通道分工**: 大人类撰写 title/body → Forgejo fetch (权威源); 小结构化 metadata → nomad META (Layer 1 已有信息, 节点无关)
4. **自主 = always-fetch, 无视既存文件** (杀 node-pinned 卷 stale-read hazard); file 模式仅 DEMO-/TEST- 前缀命中
5. **Layer 1 侧同 scope 改动** (缺此修复不生效): 发 ARIA-<repo>-<number> / 补 metadata META / 修 ISSUE_URL 用 number / 统一 head_branch 公式
6. **fetch 失败契约**: 可重试 (超时/5xx/429, 有限退避) vs 不可重试 (404/401) 分类; 显式检 HTTP status; **不 `|| true`**; 失败结果对 Layer 1 **可区分** (infra-fail vs agent-fail, 独立 outcome/标记), 防污染 AC-5 corpus 归因
7. **title/body 消毒**: YAML-safe 转义 + envsubst 变量白名单 (body 不二次展开) + CRLF→LF 归一 + 长度上限 + 注入隔离
8. **DB 键 (repo,number) 复合 + 迁移**: 明确清库 vs 迁移既有历史 (#147 issue_type_hint AC-2 stratification join 在 issue_id 上, 键漂移会断 acceptance 查询)
9. **验收假绿修**: compute-assertions.sh 空 expected_changes 禁恒真; fetch 模式独立 outcome 语义 (先写 RED 测复现)
10. **base_branch**: Layer 1 经 META 提供 (triage 已知), 或容器 fetch `default_branch` 兜底; **不硬编码 master**
11. **镜像**: aether-build-container 重建 aria-runner; **168h 跑冻结单一 IMAGE_SHA** (中途 hotfix confound corpus)

## 连带文档同步 (Rule #3, 本 Spec 交付项)

- **amend AD-M0-5**〔勘误†〕(仅跨节点场景; 单机测试 file 模式仍可用) + 回填 AD4 风险表 cross-reference (旧文字会误导)
- 新增 **AD-M6-10** (六段格式: 决策/背景/Alternatives/理由/风险/回滚) — 下一可用号 (AD-M6-9 last, AD-M6-8 Retired)
- **layer-boundary-contract.md 新增 §5 "Task Content Delivery Mechanism"** (双通道 file/fetch 字段级 schema 对照表 + file 模式生命周期声明) — 现契约完全没描述容器如何拿完整 issue 内容, 是既有缺口
- 与 **AD-M6-5** (pre-flight fixture provenance, 测试用) 消歧: 二者不同决策
- 更新 CLAUDE.md M6 状态段: 记依赖链 (input-fetch Spec ↔ 遥测 Spec)

## 依赖边 (显式, 非隐性掉线)

**遥测 (cost/model 回报)** 独立 Spec (输入 vs 输出 disjoint, 复用 sub-PR 拆分哲学): 容器如何把 cost/model 经 logs 标记回报 Layer 1 (AC-6 cost 闸需要)。**本 Spec 只修 input fetch; 168h 跑真正可评分 (AC-5) 还依赖遥测 Spec —— 未修前不能把 168h 跑当本 Spec 验收**。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| fetch 撞 CF-Access 伪成功页 (静默空内容) | heavy 节点 Forgejo egress/auth **跑前实测** + fetch 后校验合法 JSON (Content-Type/schema) + ISSUE_URL 约定内网可达 host |
| 假绿污染 corpus (②) | compute-assertions 空-expected 禁恒真 + fetch 独立 outcome + RED 测先复现 |
| 修复不生效 (①) | Layer 1 侧改动纳入同 scope + E2E dogfood 真数字-id 自主 dispatch 验到 S9/merged PR (非仅单测) |
| 多-repo number 碰撞 | (repo,number) 复合键 + volume 路径 |
| body 注入/超长/CRLF | 消毒管线 (决策点 7) |
| 168h corpus confound | 冻结 IMAGE_SHA |

## 回滚路径
immutable IMAGE_SHA: 旧镜像 sha 保留, dispatch META 指回旧 sha 即回滚容器侧; Layer 1 侧改动 git revert。file 模式 (DEMO-/TEST-) 不受影响, 单机测试路径始终可用。

## spec_level / 落地
- **Level 3** (proposal.md + tasks.md): 多任务排序 (容器代码 → 镜像 build → registry push → 部署验证 → Layer 1 代码 → assertion 修 → 契约文档同步)
- **独立 Spec** 落主仓 `openspec/changes/` (Rule #5); **不塞进** `aria-2.0-m6-e2e-resilience` (#2 是 resilience 测试基建, 本是 dispatch 输入投递契约, 语义不同)

## 待核实项 (spec Phase A 前置)
1. heavy 节点 `/opt/aria-inputs` 挂载类型 (是否 `nfs-fastpool-aether`) → §Alternatives 诚实否 D
2. 部署 M5 镜像 initial.sh Step 5 envsubst 变量白名单 + body 处理 (byte 级核对, 别据文档假设)
3. `RENDERING_CONTRACT.md` 字段契约 (expected_changes 结构) + compute-assertions 空输入行为 (先 RED 复现)
4. DB 键迁移策略对 #147 issue_type_hint AC-2 join 的影响

## 〔勘误†〕2026-07-04 前向勘误 (post_planning R1, aria-2.0-m6-dispatch-input-delivery TASK-024)

本 DEC 上文 §约束条件 (line 22) / §Agent Team 审议结论 knowledge-manager 行 (line 69) / §连带文档同步 (line 88) 三处均写"amend AD-M0-5"——这是**本 Spec 自己debunk 的误标**。Spec Phase A 代码 recon 核实: `aria-orchestrator/docs/architecture-decisions.md` 中并不存在一条名为"prompt 写 bind mount / meta 传小参数"的 **AD-M0-5 决议**；`AD-M0-5` 实际内容是 `m0-handoff.yaml` schema 锁定 12 字段 (`:1035`)，与本 DEC 讨论的 bind-mount 假设**是两回事**，`AD-M0-5` body **未被本 Spec 触及**。

该 bind-mount 假设的真实出处是 **AD4 风险表第 2 行的表内 cell** (`architecture-decisions.md:384`)，从未升格为独立 AD 决议——之前的 cell 文字把它误标成"AD-M0-5 约定"。本 Spec 的实际落地是：① 更正该 AD4 cell 的误标 + 把假设的作用域限定为**单节点** + 交叉引用新增的 **AD-M6-10**；② `AD-M0-5` body 原样保留不动。详见 `architecture-decisions.md` AD4 风险表 cell (`:384`) 与新增 AD-M6-10 章节。

上文三处"amend AD-M0-5"字面表述保留原样（历史决策记录不回改），本节仅作前向指针，指向实际生效的更正。

---

**审议 agent**: aria:tech-lead / backend-architect / qa-engineer / knowledge-manager (2026-07-02 post_brainstorm 4-路并行)
**关联**: Aria #147 (Blocker 3 阻塞链 comment #14265+#14270) / handoff `docs/handoff/2026-07-02-m6-preflight-luxeno-blocker.md`
**下一步**: spec-drafter 据本 DEC 起 Level 3 OpenSpec (proposal + tasks), 主仓 openspec/changes/
