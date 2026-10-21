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
| A1 | 镜像经 aether-build-container 构建, digest 钉进 HCL | — | 待测 |
| A2 | job 跑通 ≥1 完整 cycle (gather→report 日志) | ✅ 2026-10-21 | 待测 |
| A3 | gather 中途 SIGKILL → 重启后已完成 chunk `MEMO-HIT skip` 且值与崩溃前逐字同, cycle 补完 | ✅ (run2 首行 MEMO-HIT, value 与 run1 chunk1 相同) | 待测 |
| A4 | wait 中途 SIGKILL → 重启后续睡, 醒在原 deadline (±1s), 不提前 | ✅ (醒在 deadline+26ms) | 待测 |
| A5 | 重启后 `live-tasks=1 (resume)`, 不重复建 task | ✅ | 待测 |
| A6 | build 后 push 凭据 var 无残留 (`/v1/vars?prefix=nomad/jobs/build-container-`) | — | 待测 |

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

## 布局

- `src/sentinel.mjs` — 全部逻辑 (~200 行, 无框架壳)
- `Dockerfile` — node:22-slim + npm ci (Verdaccio .206:4873, lockfile 钉版本)
- `deploy/pi-durable-poc.nomad.hcl` — pin heavy-2, restart mode=delay, nomadVar auth
