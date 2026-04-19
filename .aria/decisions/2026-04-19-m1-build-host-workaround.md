# Decision: M1 aria-runner Build Host — Workaround via `aether dev run`

> **Status**: Decision recorded
> **Date**: 2026-04-19
> **Parent**: [US-021 Phase B.2 T1.b](../../openspec/changes/aria-2.0-m1-mvp/tasks.md)
> **Session context**: 2026-04-19 T1.b spike 执行期间, owner-AI 对话暴露架构 gap, 经 Aether 工具深度调查后定案

---

## 背景

### 触发链

1. Owner 按 `spike-procedure.md` 执行 Step 2c (保存 Bot PAT), save-pat.sh 暴露 CF Access + scope + jq boolean 三个 bug (已修复, 见 aria-orchestrator@874faa9)
2. Step 3 `docker login` 前置检查: **本机 `dev-claude` 没装 docker**
3. AI 起初误判 308/309 为 Aether heavy 节点 → owner 纠正: 308/309 是 **开发容器**, Aether 是独立的 10CG 生产 Nomad 集群
4. Owner 指出: "aether 内可以随时搭建容器, Nomad 方便管理" → 建议 build 动作归回 Aether
5. AI 使用 Aether 工具 (`aether status --nodes`, `aether dev --help`, `aether env --help`, Nomad API) 深度调查, 修正理解

### Aether 集群真实拓扑 (本次调查获得)

```
Nomad Leader: 192.168.69.71:4647
Forgejo:      192.168.69.200:3000 (内网)

8 节点 / 2 class:
├── heavy_workload (3): heavy-1/2/3 @ 192.168.69.80-82  [driver: docker + exec]
└── light_exec     (5): light-1..5   @ 192.168.69.90-94 [driver: exec only]
```

关键事实:
- 只有 `heavy_workload` 3 节点有 **docker driver**, 可做 build/run
- 20 个 running job 全是 `type=service`, 无 batch/dispatch 先例
- `aria-orchestrator` 已作 service 在 Aether 跑 (Aria 在 Aether 的落地点)
- Nomad Variables 有 3 个项目使用, 功能可用

---

## 决策 (3 part)

### D1. M1 aria-runner 镜像构建主机 = Aether 集群内 `aria-build` 容器

通过 **`aether dev run aria-build.hcl --name aria-build`** 部署:
- Service type (长期存在, M1 期间复用)
- Constraint `node.class == heavy_workload` (只有这 3 节点有 docker)
- Docker driver + mount `/var/run/docker.sock` (复用 heavy 节点已有 docker daemon, 免 DinD 开销)
- 使用方式: `nomad alloc exec` 进入容器, 手动 `docker login + build + push`

**Rejected alternatives**:

| 候选 | Rejected 理由 |
|------|------|
| 本机 (dev-claude) 装 docker + build | 偏离 "build in cluster" 原则; dev-claude 是 AI sandbox, 不是生产 infra 一部分 |
| 308 / 309 开发容器上 build | 它们是 dev sandbox 不是生产环境; 镜像 push 路径走开发机 → 生产 = 错位 |
| 直接 SSH 到 heavy-1 docker build | 混淆 "build" 与 "run" 职责; heavy-1 是生产 Nomad worker, 不应接受 SSH-direct 操作 |
| DinD (Docker-in-Docker) | M1 MVP 范围内过度工程化, mount socket 足够 |
| `aether dev deploy` 内置的 build+push+deploy 流程 | 它仍假设**本地** docker 执行 `docker build`, 且与 deploy 绑死, 不适合 M1 parameterized dispatch 场景 |

### D2. Secret 存储 = Nomad Variables (非本地 `~/.tmp/`)

通过 **`aether env set --job aria-build FORGEJO_BOT_PAT ...`** 设置, Nomad job 经 template stanza 注入为环境变量。

**锁 AD-M1-1 Secret store 选型字段为 "Nomad native"** (而非引入 Vault / AWS SM):
- Aether 已有 3 项目实践 Nomad Variables, 无需额外基础设施
- 符合 "最小可行" M1 MVP 精神
- M2 演进到更严格方案 (Vault) 可平滑迁移 (template stanza 不变, 变 source)

dev-claude 上的 `~/.tmp/.aria-runner-bot-pat-20260419` **降级为初次验证副本**, M1 执行期不再使用, 可保留或删除。

### D3. **不为 Aria 在 Aether 封包单独工具**

评估后**否决** "Aether 增加 Aria-specific 命令/skill" 的方向。

**理由**:

1. **通用原语已足够**: Aria 的真实需求 (搭 build 容器 / 存 secret / dispatch aria-runner / 查日志) 全部可由 Aether 现有通用命令覆盖:
   - `aether dev run <hcl>` — 任意 HCL 容器部署
   - `aether env set/get` — Nomad Variables CRUD
   - `nomad job dispatch` (直调 Nomad) — parameterized dispatch
   - `aether logs / status / doctor` — 观察

2. **Meta-repo 对等原则** (memory `project_meta_repo_pattern`): Aria / Aether / standards 在 10CG org 下是一等同级 repo, 不是父子关系. Aether 为 Aria 特权封包 = 引入耦合, 破坏对等性; 其他项目 (Kairos / Hermes) 会效仿索要特权 → Aether 膨胀失焦.

3. **AI-DDD 领域边界**: Aria-specific 的 dispatch / orchestration 逻辑 (ISSUE_ID 协议 / PR 回写验证 / legal_assumptions 签字链) 属于 **Aria 领域**, 应留在 `aria-orchestrator/`:
   - `dispatch-issue.sh` 已在 `aria-orchestrator/scripts/` ✅
   - 未来 `build-aria-runner.sh` wrapper (调 `aether dev run`) 也应放那边
   - Aether 保持 infra primitive, Aria 组合原语 — 这才是正确边界

4. **YAGNI**: 若 M1/M2 暴露出 "AI agent parameterized dispatch" 是**跨项目重复模式** (Hermes AI agent / Luxeno AI workflows 等也需要), 届时再提取为 Aether 原语, 有多实例数据支撑。现在提议是空中楼阁。

**Traceability 用途**: 下次 AI session 若再提"让 Aether 支持 Aria 专属工具", 本 §D3 是现存决策, 直接引用, 避免重复思考 cycle.

---

## 已提交的 Aether 改进 issue (保留, 不撤回)

**[Aether#27](https://forgejo.10cg.pub/10CG/Aether/issues/27)** — feat: 缺 build-container 原语 + 节点自省能力

提此 issue 时尚未发现 `aether dev run` 已部分覆盖需求。基于本次调查 reframe:

- **部分冗余**: generic build-container 原语可由 `aether dev run` + 自带 docker.sock HCL 实现
- **保留有价值部分**:
  - `aether build` 专用命令 (比 dev run 明确语义)
  - `aether status --nodes --capabilities` — 节点 driver/role 自省 (本次只能通过 Nomad API 直查)
- Issue 正文未 amend, 由 Aether 维护方 triage 时决定范围

---

## 对 M1 其他文档的影响 (需同步)

| 文档 | 改动 | 优先级 |
|------|------|------|
| `aria-orchestrator/spikes/m1-registry-auth/spike-procedure.md` §Step 3-6 | 执行主机从 "本地" 明确为 **`aria-build` 容器内**; 注册 URL 保持 `forgejo.10cg.pub` (容器从 host 网络可直连) | T1.b 执行前必改 |
| `aria-orchestrator/nomad/registry-push-guide.md` §1 前置条件 | "本地 Docker daemon" → "Aether `aria-build` 容器内 docker CLI" | T1.c 执行前必改 |
| `aria-orchestrator/spikes/m1-registry-auth/access-audit-report.md` §4 Residual | PAT 风险宿主从 "dev 工作站" → "Aether 生产集群 Nomad Variables" — 风险模型需重评 | access-audit 执行时更新 |
| `aria-orchestrator/docs/architecture-decisions.md` §AD-M1-1 Rotation policy | "Injection method" 字段锁定 = **Nomad Variables + template stanza** (不再 TBD) | T6.3 回填时 |

---

## M2 演进路径

1. **Aether#27 落地** → M2 时迁 aria-build 到 `aether build` 专用命令 (语义更干净)
2. **Forgejo Actions runner 部署** (M2 CI 必做) → 很可能也走 Aether 同样 `aria-build` 容器路径, 或直接挤入 runner pool; 本决策为 CI 接入铺路, 非阻塞
3. **Vault 引入** (若 10CG 其他项目先引入): `template` stanza 的 `nomadVar` 换成 Vault source, HCL 主体不变
4. **跨项目 AI agent dispatch 归一** (若 Hermes / Luxeno 后续出现同类需求): 届时向 Aether 提 `aether:ai-agent-dispatch` 原语 issue (有数据支撑再提)

---

## 产出文件

- 本决定 doc
- `aria-orchestrator/nomad/jobs/aria-build.hcl` — 实现 HCL (配套产出)

---

## 签字

```
Decision author: ai:aria-session @ 2026-04-19
Based on:        Aether tool investigation + owner architectural correction
Advisory-only:   per AD-M0-9; 最终采纳 / 执行 / 修正由 owner (simonfish) 决策
Review cycle:    若 T1.b 实操发现本决策假设偏差 (如 heavy 节点 docker.sock mount 被拒),
                 回本 doc 记 v0.2 并 reopen
```
