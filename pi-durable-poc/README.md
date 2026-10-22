# pi-durable PoC — cost-sentinel 耐久执行试点

> Aria #232 follow-up / Pi Durable 继任架构评估的第一步。
> 2026-10-21 owner 批准试水: 拿 cost-sentinel (单一日任务/无 Lark 依赖/失败无害)
> 验证 `@earendil-works/pi-durable` 在真 Nomad 下的耐久语义, **不动** orchestrator 主链。

## 验证的问题

Pi Durable 的三个承诺, 在 Nomad docker task 的 kill/restart 之下是否成立:

1. **进程死于 phase 中途 → 重启后从 checkpoint 续, 已提交的工作不重做**
2. **进程死于 durable sleep 中 → 重启后睡到原 deadline, 不提前醒、不丢失**
3. **task 身份跨重启稳定 → 不重复建 task**

## 设计

```
wait ──sleep(nextAt)──▶ gather (3 chunks, 每块 work + memo 提交) ──▶ report ──▶ wait (cycle+1)
```

- **storage**: SQLite (WAL, synchronous=NORMAL) 于容器本地盘。heavy 节点 docker
  data-root 在本地 SSD (Aether #67), 即 alloc 容器 fs = 本地 SSD。
  库文档明说 JSONL "keeps the whole history in memory... use SQLite for long-running
  agents" — 长跑选 SQLite 是库自己的建议。
- **单 owner 模型**: pi-durable 无跨进程锁 → job pin 到 heavy-2, count=1。
  reschedule 到别的节点 = 状态丢失, PoC 接受此边界 (继任架构若上 Postgres backend 可解)。
- **耐久 sleep 由构造保证**: deadline 存 `checkpoint.nextAt`, 重启后 wait phase 从顶部
  重跑、读同一 deadline 续睡 — 不赌库的 sleep 持久化实现。
- **幂等 gather**: 每块结果存 `runtime.memo(key)`; key 含 task 创建时的 epoch
  (存 task input, 创建后不变), 防「task fault 后新建 task、cycle 计数重来」撞键。

## 验收判据 (集群演练前写定)

| # | 判据 | 本地(进程级 kill -9) | 集群(docker kill) |
|---|------|----------------------|-------------------|
| A1 | 镜像经 aether-build-container 构建, digest 钉进 HCL | — | ✅ sha256:e9d790c4…, 48s, build 6982ebb |
| A2 | job 跑通 ≥1 完整 cycle (gather→report 日志) | ✅ 2026-10-21 | ✅ 17:17 cycle 0 完整 |
| A3 | gather 中途 SIGKILL → 重启后已完成 chunk `MEMO-HIT skip` 且值与崩溃前逐字同, cycle 补完 | ✅ (run2 首行 MEMO-HIT, value 与 run1 chunk1 相同) | ✅ 17:27:36 kill → 17:27:43 resume, chunk1 MEMO-HIT (value=…3654 逐字同), 2/3 补算, report 复用旧值 |
| A4 | wait 中途 SIGKILL → 重启后续睡, 醒在原 deadline (±1s), 不提前 | ✅ (醒在 deadline+26ms) | ✅ 17:27:02 kill → resume 续睡 remaining 22.0s, 醒在 deadline+14ms |
| A5 | 重启后 `live-tasks=1 (resume)`, 不重复建 task | ✅ | ✅ 两次重启均 `live-tasks=1 (resume: ready)` |
| A6 | build 后 push 凭据 var 无残留 (`/v1/vars?prefix=nomad/jobs/build-container-`) | — | ✅ 0 残留 (trap finally purge) |

## 演练方法 (集群)

```bash
# A3: 等 [gather] enter 出现、chunk1 computed 后:
ssh root@192.168.69.81 "docker ps --filter name=pi-durable --format '{{.ID}}' | head -1 | xargs docker kill"
# A4: 等 [wait] ... remaining 出现后同样 docker kill
# 证据: nomad alloc logs -f <alloc> 里 grep MEMO-HIT / remaining / 醒来时刻
```

## 已知锐边 (试水发现, 继任评估输入)

1. **`sleepUntil` 是 main 分支 API, 1.3.0 没有** — 只有 `runtime.sleep(until, ctx)`。
   按网上最新文档写代码会 phase fault (TypeError), 且默认**无任何输出**。
2. **phase fault 默认静默** — 必须自挂 `onReport`, 否则 task 死了日志一行都没有。
3. **chord unref 全部定时器** — 进程不会因 pending task 而驻留事件循环, host 必须
   自持 keep-alive; 反过来 crash 后重启续跑的语义不受影响。
4. **graceful stop (SIGTERM→close) 打断 phase 中途 = 该 cycle fault** — "must commit
   durable progress" 约束; 已存的 memo 不丢, 但 cycle 不补完。生产化时要让 work()
   响应 `runtime.signal` 提前退出。
5. **memo 是 at-least-once 语义** — work 完成到 memo 提交之间 crash, 重启重做该块。
   有外部副作用的块需要自带幂等键。
6. **容器内任意路径 ≠ 持久存储** — 集群演练实测: storage 写容器可写层 (`/data`) 时,
   Nomad 容器重启 = 冷启动 (live-tasks=0, cycle 归零)。必须指 `NOMAD_ALLOC_DIR` 下的
   路径 (宿主盘, 同 alloc 重启保留)。reschedule 到别的节点仍会丢 — 单 owner 模型的
   已知边界, 继任架构上 Postgres/Redis backend 才能根除。

## 结论 (2026-10-21 集群演练后)

耐久语义三承诺 (checkpoint 续跑 / durable timer / task 身份稳定) 在 Nomad docker
task + SIGKILL 下全部成立, 判据 A1-A6 全绿。生产化前要消化: 锐边 1/2 (静默 fault)、
锐边 4 (graceful stop 语义)、锐边 6 的 reschedule 边界。**验证的是耐久执行模型,
不是 cost-sentinel 的业务逻辑** — 真实业务是 M6 cost snapshot (Zhipu 30d 阈值告警 +
Luxeno 量下限 + 飞书卡片, 见 aria-layer1-cost-sentinel.nomad.hcl 头注), 接入是
Phase-2 候选。

## PoC-L — 轻节点可行性 (exec driver, 零 Docker) (added 2026-10-22)

回应「docker 太重」的原始担忧: 同一 sentinel 以 **exec task** (chroot + cgroup,
无容器层) 跑在 light-4 (1GiB 节点, 当前最空 935MB 可用)。运行时与依赖经 artifact
分发: 官方 Node 22.23.3 tarball (30MB, 自包含 glibc 构建) + npm ci bundle
(91 包, 15MB, lock 内无 photon)。heavy 版实测 RSS 39.7MiB / 256MiB 预留。

验收判据 (演练前写定):

| # | 判据 | 结果 |
|---|------|------|
| L1 | exec task 在 light-4 启动: artifact 解包 + node 起来 + boot 日志 | ✅ 01:22:36 boot → cycle 0 完整 |
| L2 | 实测 RSS ≤ 150MB (memory 预留), 不挤压 1GiB 节点其余负载 | ✅ cgroup 115.9MB (含 file cache; docker 版工作集 39.7MiB) < 150MB 预留, light-4 尚有 935MB 可用 |
| L3 | mid-gather kill -9 → MEMO-HIT 续跑 (同 A3) | ✅ 01:24:28 kill → resume `MEMO-HIT skip (value=…2267 逐字同)`, 2/3 补算, report 复用旧值 |
| L4 | mid-wait kill -9 → 醒在原 deadline (同 A4) | ✅ kill 后续睡 remaining 32.9s, 醒在 deadline+2ms |
| L5 | 全程零 Docker (driver=exec, 无 image/auth) | ✅ 同 alloc 7d097f08 内 pkill 重启两次, 状态不丢 |

### PoC-L 打包发现 (Nomad artifact 边界, 2026-10-22)

1. **artifact getter 不支持 `file://`** (这版 Nomad): 改走节点本机 http.server
   (`aether-dist.service` — 2026-10-22 收编为永久 systemd unit, enabled, 重启存活;
   内容仍手工 scp staging)
2. **tar 解包有 4096 文件上限** — Node 官方 tarball 5866 个文件直接超限。裁掉
   `lib/node_modules/{npm,corepack}` + share + include → **11 个文件** 28MB,
   `node --version` 及全部运行不受影响 (运行时不需要 npm)
3. **依赖树同样超限**: npm ci 全量 13775 文件 — pi-ai 静态拖进全部 provider SDK
   (openai 3589 / @smithy 1924 / @anthropic-ai 1829 / @aws-sdk 1577 文件), 我们零
   provider。剥 `.ts/.map/.md` + 整删 provider SDK → **2663 文件**, 本地 kill 演练
   复验 MEMO-HIT 不回归, gzip 后 4MB
4. **`.tgz` 后缀必须真 gzip** — `tar -cf` 裸 tar 命名 .tgz, getter 按后缀当 gzip 解,
   报download failed。`file <tar>` 先验再传
5. `nomad job run` 默认会阻塞等部署 — 脚本里用 `-detach`

**轻节点结论**: 可行。耐久语义与 heavy docker 版逐判据等价 (L3/L4 与 A3/A4 同形),
零容器层, 内存足迹不构成约束。代价是把「镜像构建」换成了「bundle 工程」: 文件数/
压缩格式/运行时裁剪都要自己管 — 这正是 docker 在重节点替我们扛掉的复杂度。分发通道
(file:// 不支持 → 本机 http.server) 是生产化前最大缺口, 见下。

**PoC-L 局限**: artifact 走 light-4 本机 http.server (永久 systemd unit `aether-dist.service`,
2026-10-22 收编, enabled 重启存活; 内容仍手工 scp staging; 这版 Nomad getter 不支持 file://) — 生产化
分发候选是 Forgejo generic packages (内网 HTTP) + artifact `header` 带 package-read
token (token 不落 job spec 明文的问题要单独解, e.g. agent 侧 mirror)。

## 布局

- `src/sentinel.mjs` — 全部逻辑 (~200 行, 无框架壳)
- `Dockerfile` — node:22-slim + npm ci (Verdaccio .206:4873, lockfile 钉版本)
- `deploy/pi-durable-poc.nomad.hcl` — pin heavy-2, restart mode=delay, nomadVar auth
