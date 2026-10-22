---
track-id: substrate-eval-poc-phase1
owner-container: simonfish/bfe8285d
phase: session-close
status: done
updated-at: 2026-10-22T10:10:00Z
---

# Aria — Session Handoff (2026-10-21 晚 ~ 10-22, 会话收尾) — pi-durable 双 PoC + 全集群镜像 CI 化收口 (#232 终局) + 发布漏步修复

> **性质**: 会话收尾 (session-closer, leaf; Rule #9)。本会话从「调研 pi durable」起,
> 经 owner 两批批准 (试水 → 1+3 → layer1 CI 化含 HCL 切换), 到 #232 的镜像/发布两条
> 脱全线收口。与 10-22 周期收尾 (v1.77.1 双轨, issue-groomer 轨) 平行无碰撞。

## §0 入口

本轨 Phase-1 已终结 (全部交付 + 合并 + 生产切换验证)。候选接续 (owner 决):

1. **DEC-20261022-001 Phase-2** — ops-tier 轻档动词试点 (issue-groomer 收录/打标承载于
   pi-durable), 验证剩余评估维度 (多 harness 适配 / Layer L claim 接驳); 执行主体未指派
2. **PoC 两 job 去留** — `pi-durable-poc` (heavy-2 docker) / `pi-durable-poc-light`
   (light-4 exec) 持续在跑 (~40MB 工作集 ×2); 转真实业务 (M6 cost snapshot 的
   pi-durable 版) / 保持观察 / 下线, 均可
   - **Soak 基线 (2026-10-22T16:52Z, 复查时对照)**: H = 23.4h / cycle 1562 /
     RSS 55.6MiB (较晨间 39.7MiB **+40% 漂移**, 主观察项); L = 15.4h / cycle 1031 /
     cgroup 61.8MB (自 116 回落) / SQLite 主库 643KB + WAL 4.4MB。
     **复查建议 ~7 天后或 Phase-2 启动时**; 期间不 redeploy (调间隔会换 alloc 丢
     状态, 污染连续性 — 2026-10-22 已裁定不动)
3. ~~**PoC-L 分发通道生产化**~~ **已落地收编** (2026-10-22 当日, PR #252): transient
   systemd-run → 永久 `/etc/systemd/system/aether-dist.service` (enabled, 重启存活);
   剩余手工面 = 内容 scp staging, 生产化候选 (Forgejo generic + token 不落明文) 仍开放
4. (Aether 侧) #453 PAT 轮换 — 等 owner 铸 Q4 token
5. (Aether 侧) npm token 轮换 — owner 裁定先记录暂不动 (memory 有步骤)

## §1 已完成 (会话时间线摘要)

- **10-21 晚**: 调研纠正 (pi durable = `@earendil-works/pi-durable`, 非编码代理) →
  owner 批 cost-sentinel PoC → **PoC-H** (heavy-2 docker, A1-A6 全绿: MEMO-HIT 值逐字同
  / deadline+14ms 醒 / live-tasks resume) → 构建时撞破 **#232 发布漏步** (meta gitlink
  d726be5d 在子模块远端不可达, recursive clone 全断) → 修复 (子模块 PR #34 master FF +
  meta PR #245 gitlink 重指 + **issue #246** 发布收尾三步 checklist) → 凭据卫生
  (9/9 push-cred var 泄漏清除 + 共享卷 293MB→130K)
- **10-22**: **PoC-L** (light-4 exec 零 Docker, L1-L5 全绿; 打包五坑: file:// 不支持 /
  tar 4096 文件上限 → Node 裁 11 文件、依赖剥 provider SDK 至 2663 / .tgz 须真 gzip) →
  **DEC-20261022-001** (C1-C4, 挂 DEC-20261018-002 评估轨) → **orchestrator 镜像 CI 化**
  (PR #248; run 51958 Verify 拦截 **certifi 脱节实锤** — repo Dockerfile 从未产出过可用
  镜像, 线上 7d02d7c5 是 docker commit 产物 → 子模块 PR #35 修 Dockerfile (vendored pip
  删 + ensurepip + 内网 devpi + 构建内断言 + 补 bash) → run 51959 绿) → **生产切换**
  (PR #249/#36, Lark WebSocket 验证) → **layer1 同法** (PR #250; run 52301 Verify 拦
  多行 python -c 缩进坑 → 修 → 52302 绿 → 子模块 PR #37 四 HCL 切 `c3290150` → 4 parent
  注册 → force child exit 0) → **cost-sentinel 迁移后首跑三层验证** (调度 exit 0 /
  业务 cost-2026-10-22.json 落卷 dual-row schema / freshness 02:00:09) → **全集群运行
  镜像 100% repo 可复现**

## §2 未完成 / Carry-forward

- **AI 内省 (load-bearing)**:
  - §0 五条候选均未排期 (Phase-2 主体 / PoC 去留 / 分发通道 / #453 / npm token)
  - PoC-L 的 http.server 与 /opt/aether-dist 两个 artifact 是**手工 staging**, light-4
    重启后 http.server 消失 (systemd-run transient) — PoC job 会进 artifact download
    重试循环; 重启该节点前需重挂 (或先收编下线)
- **机械补漏 (backstop)**:
  - 上一 session handoff §2 记的四维 advisory「aria-orchestrator gitlink ef5506d vs
    主仓 237045a, 待下次涉 orchestrator 时核」— **本会话已修复闭合** (即 PR #34/#245
    那次发布漏步; 修复后递归 clone smoke ×3 全 0 错)
  - 本会话无新 advisory: master 递归 clone 0 错误, gitlink = 子模块 master tip
    (d929f680), 已合并分支 8 条全清

## §3 关键风险 / 已知陷阱

1. **「registry 里躺着的手工 digest」物种已灭绝但要防复发**: 两个 CI workflow 各带
   Verify 承重门 (orchestrator: hermes + certifi CA>100KB; layer1: aria_layer1 导入 +
   m6 布局 + 系统 CA>100KB)。51958/52301 两次拦截证明门有效 — 改镜像相关内容必须
   保持这两个 workflow 绿
2. **Dockerfile 内严格断言不可放进 `|| true` 射程** (certifi 事故的根因形态):
   orchestrator Dockerfile 的构建内断言已独立成步
3. **layer1 periodic job 无状态**: reschedule 换节点安全 (状态全在 aria-layer1
   host_volume); orchestrator 同 (hermes-home 在卷上)
4. **YAML workflow 里多行 `python -c`**: 字面缩进原样进 python = IndentationError;
   单行分号式 (build-aria-layer1.yaml 有注释)
5. Forgejo dispatch 触发的 run **不写 commit status** — 监视用 actions tasks API
   (`/repos/{o}/{r}/actions/tasks` 按 workflow_id+head_sha 过滤)

## §4 实战教训 (memory 沉淀)

- 新: `abandoned-build-rounds-leak-push-creds` — build 轮中途弃用时 push-cred var +
  共享卷产物双残留, 事后必扫 (本会话 9/9 泄漏实证)
- 更新: `pi-durable-vs-hermes-eval` — 补 PoC-L 结果 + CI 化止损已交付段
- 新: `npm-token-echoed-rotation-deferred` — 凭据文件过滤要 `-vi token` (大小写),
  owner 裁定先记录
- 复用生效的旧 memory: dispatch 不写 status (改用 actions tasks API)、CLI 输出落文件
  再读 (管道 head 吞输出的坑本会话又踩两次)、`;` 链与双前缀循环小坑自纠

## §5 多维度同步状态 (收尾实测, 2026-10-22T10:05Z)

- git: master 全同步 (本轨所有 PR 已合并); 递归 clone (`--recurse-submodules
  --shallow-submodules --depth=1`) 0 错误; gitlink = 子模块 master tip d929f680
- 集群: 5 Aria job 全在 CI 产物镜像上 (orchestrator 20f9cb5a + 4×layer1 c3290150);
  2 PoC job 运行中; 无 failed/pending 残留
- registry: ci-verify-20261022 / ci-layer1-20261022 + sha tags 各双推
- 并行轨: secret-guard-w10-failclosed-narrowing (另一 session) 同期在 master 活跃,
  路径无碰撞

## §6 Next session 入口

最省事的接续: 若 owner 只想收尾观察 → 等 PoC job 跑数日看漂移; 若推进评估轨 →
从 DEC-20261022-001 Phase-2 起步 (先定试点动词); 若维护面 → PoC-L http.server 收编
(挂 systemd unit 或换分发通道) 是唯一有时效的小活 (light-4 重启前)。

## §7 提交清单 (本会话, 按仓)

- **10CG/Aria** (meta): PR #245 (gitlink 修复), #247 (PoC+DEC), #248 (orchestrator CI),
  #249 (orchestrator 切换), #250 (layer1 CI+切换); issue #246 (发布 checklist);
  本 handoff
- **10CG/aria-orchestrator** (子模块): PR #34 (master FF 收尾), #35 (Dockerfile certifi
  修真), #36 (orchestrator digest), #37 (layer1 4×digest)
- **Forgejo CI**: run 51958/51959 (orchestrator), 52301/52302 (layer1)
- 无 tag (plugin/CLI 未动)

## §8 Memory entries this session

- 新: feedback_abandoned_build_rounds_leak_push_creds
- 新: project_npm_token_echoed_rotation_deferred
- 重写: reference_pi_durable_vs_hermes_eval (纠正目标 + PoC 结果 + 止损交付)
- MEMORY.md 索引同步
