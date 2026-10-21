// cost-sentinel PoC — Pi Durable (@earendil-works/pi-durable 1.3.0)
//
// 目的: 验证 pi-durable 的 durable execution 模型在 Nomad docker task 下的行为,
// 不是真的成本扫描。三个 phase 的无限循环:
//
//   wait   ──sleepUntil(nextAt)──▶ gather ──▶ report ──▶ wait (cycle+1)
//
// 验收判据 (drill 详见 README.md, 跑之前写定):
//   A3 mid-gather SIGKILL → 重启后已完成 chunk 走 MEMO-HIT 跳过, 未完成的重算, cycle 补完
//   A4 mid-wait  SIGKILL → 重启后仍睡到原 deadline (不提前醒)
//
// 存储模型: SQLite (WAL, synchronous=NORMAL) 于容器本地盘 (= heavy 节点本地 SSD,
// docker data-root 不在 NFS 上, 见 Aether #67)。单 task 单 owner; nomad job pin 到
// 单节点 (pi-durable: "One process owns a storage at a time; there is no
// cross-process locking")。

import { mkdir } from "node:fs/promises";
import { writeSync } from "node:fs";
import path from "node:path";
import { createModels } from "@earendil-works/pi-ai/models";
import { BACKGROUND_CONTEXT } from "@earendil-works/chord/context";
import {
  Harness,
  createRegistry,
  defineExtension,
  defineTask,
} from "@earendil-works/pi-durable";
import { openNodeSqliteStorage } from "@earendil-works/pi-durable/storage/sqlite/node";

const context = BACKGROUND_CONTEXT;

const DATA_DIR = process.env.DATA_DIR ?? "./data";
const INTERVAL_MS = Number(process.env.POC_INTERVAL_MS ?? 45_000);
const CHUNK_MS = Number(process.env.CHUNK_MS ?? 3_000);
const CHUNKS = Number(process.env.POC_CHUNKS ?? 3);
const TASK_KIND = "poc.cost-sentinel";

const iso = (ms) => new Date(ms).toISOString();
const log = (tag, msg) =>
  console.log(`${iso(Date.now())} up=${process.uptime().toFixed(1)}s [${tag}] ${msg}`);
// 退出路径上的日志必须同步写, 否则 process.exit 抢在管道 flush 前, 行会丢。
const slog = (tag, msg) => {
  try { writeSync(2, `${iso(Date.now())} [${tag}] ${msg}\n`); } catch {}
};
process.on("uncaughtException", (e) => { slog("uncaught", e?.stack ?? String(e)); process.exit(70); });
process.on("unhandledRejection", (e) => { slog("unhandled", e?.stack ?? String(e)); process.exit(71); });

// 模拟的 gather 工作单元: 纯计算 + 延时, 无外部副作用 (PoC 只验耐久语义)。
const work = async (i, ms) => {
  await new Promise((r) => setTimeout(r, ms));
  return `chunk-${i}-value-${Math.floor(Date.now() / 1000)}`;
};

// ---- durable task ----
// input: { epoch } — task 创建时刻的 epoch ms。memo key 用它: 防止「task fault 后
// 新建 task、cycle 计数从 1 重来」与旧 cycle 的 memo 撞键。input 创建后不变, 重启后
// 同一 task 读到同一 epoch (放 checkpoint 的话要在每个 phase commit 里手工搬运, 容易漏)。
// checkpoint S: { phase, cycle, nextAt }
const Sentinel = defineTask({
  name: TASK_KIND,
  version: 1,
  initial: () => ({ phase: "wait", cycle: 0, nextAt: 0 }),
  phases: {
    wait: async (task, runtime, ctx) => {
      const s = task.state.checkpoint;
      // 首次进入: +500ms — 避开 deadline=now 的零延迟边缘
      const until = s.nextAt > 0 ? s.nextAt : runtime.now() + 500;
      const remain = ((until - runtime.now()) / 1000).toFixed(1);
      log("wait", `cycle=${s.cycle} durable sleep until ${iso(until)} (remaining ${remain}s)`);
      // pi-durable 1.3.0 的 API 是 runtime.sleep(until, ctx) (sleepUntil 是 main 分支
      // 的, 未随 1.3.0 发布 — 调不存在的方法 = phase fault)。
      // deadline 存 checkpoint.nextAt: 重启后本 phase 从顶部重跑、读同一 deadline 续睡,
      // 耐久性由构造保证, 不依赖库的 sleep 自身持久化。
      await runtime.sleep(until, ctx);
      await runtime.commit(
        () => ({ status: "running", checkpoint: { phase: "gather", cycle: s.cycle, nextAt: until } }),
        ctx,
      );
    },

    gather: async (task, runtime, ctx) => {
      const s = task.state.checkpoint;
      const epoch = task.input.epoch;
      log("gather", `cycle=${s.cycle} enter (${CHUNKS} chunks × ${CHUNK_MS}ms)`);
      for (let i = 1; i <= CHUNKS; i++) {
        const key = `e${epoch}#c${s.cycle}#chunk${i}`;
        const existing = await runtime.memo(key, ctx);
        if (existing !== undefined) {
          log("gather", `cycle=${s.cycle} chunk ${i}/${CHUNKS} MEMO-HIT skip (value=${existing.value})`);
        } else {
          const value = await work(i, CHUNK_MS);
          await runtime.memo(key, { value, at: runtime.now() }, ctx);
          log("gather", `cycle=${s.cycle} chunk ${i}/${CHUNKS} computed value=${value}`);
        }
      }
      await runtime.commit(
        () => ({ status: "running", checkpoint: { phase: "report", cycle: s.cycle, nextAt: s.nextAt } }),
        ctx,
      );
    },

    report: async (task, runtime, ctx) => {
      const s = task.state.checkpoint;
      const results = [];
      for (let i = 1; i <= CHUNKS; i++) {
        const m = await runtime.memo(`e${task.input.epoch}#c${s.cycle}#chunk${i}`, ctx);
        results.push(m?.value ?? "MISSING");
      }
      const nextAt = runtime.now() + INTERVAL_MS;
      log("report", `cycle=${s.cycle} results=[${results.join(", ")}] → next wait at ${iso(nextAt)}`);
      await runtime.commit(
        () => ({ status: "running", checkpoint: { phase: "wait", cycle: s.cycle + 1, nextAt } }),
        ctx,
      );
    },
  },
});

// ---- boot ----
await mkdir(DATA_DIR, { recursive: true });
const storage = await openNodeSqliteStorage(path.join(DATA_DIR, "session.sqlite"));
const registry = createRegistry();
registry.install(defineExtension({ name: "cost-sentinel", tasks: [Sentinel] }));

const harness = await Harness.open(storage, {
  models: createModels(),
  registry,
  // phase 内的非致命失败默认静默 — 上面 sleepUntil 误用就是这么无声死掉的。必须可见。
  onReport: (e) => slog("report", e?.stack ?? String(e)),
}, context);
const root = await harness.root(context);

// 幂等启动: inspect() 列 live tasks ("Writes nothing and runs no task code"),
// 已有本 kind 的活 task 就复用, 不重复创建。(不用 taskGraph — 其 state 异步填充,
// 启动时立即读 .value 会拿到空初值, 每次重启都误建新 task。)
const insp = await harness.inspect(context);
const mine = insp.tasks.filter((t) => t.record.kind === TASK_KIND);
log("boot", `storage=${DATA_DIR} live-tasks=${mine.length}${mine.length ? ` (resume: ${mine.map((t) => t.state.kind).join(",")})` : ""}`);

if (mine.length === 0) {
  const epoch = Date.now();
  await root.commit((tx) => tx.createTask(Sentinel, { epoch }, { ownership: { kind: "conversation" } }), context);
  log("boot", `created task ${TASK_KIND} epoch=${epoch}`);
}
harness.resume();

// keep-alive: 不让事件循环在 task 驻留 waiting 时排空 — 进程只经 closed/SIGTERM 退出。
setInterval(() => {}, 1 << 30);

// storage error → harness 自闭; 退出非零让 Nomad (mode=delay) 拉起, 重开即恢复。
harness.closed.then((end) => {
  slog("closed", `reason=${end.reason} end=${JSON.stringify(end)}`);
  process.exit(end.reason === "failed" ? 1 : 0);
});

// SIGTERM: 限时优雅关闭 (Nomad stop); 超时硬退 — 对耐久模型等价于 crash, 重启续跑。
process.on("SIGTERM", () => {
  slog("sig", "SIGTERM — closing (3s budget)");
  const t = setTimeout(() => process.exit(0), 3_000);
  harness.close(context).finally(() => {
    clearTimeout(t);
    process.exit(0);
  });
});
process.on("exit", (code) => slog("exit", `code=${code}`));
