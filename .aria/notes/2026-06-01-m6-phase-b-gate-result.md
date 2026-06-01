# M6 Phase B Gate Check — auto-run 2026-06-01T02:30:01Z

> 自动任务 (2026-05-30 设的 crontab one-shot)。在 light-1 上跑 3-day rolling history 闸门。
> snapshot 是 node-local (Blocker #2),故 validator 必须在 light-1 上跑。

## 1. 3-day rolling history check (validator on light-1)
```
3-day rolling history: PASS (3 files, latest 2026-06-01)
EXIT=0
```

## 2. snapshot files on node
```
-rw-r--r-- 1 root root 483 May 31 13:27 /opt/aether-volumes/aria-layer1/data/cost-snapshots/cost-2026-05-30.json
-rw-r--r-- 1 root root 483 May 31 13:28 /opt/aether-volumes/aria-layer1/data/cost-snapshots/cost-2026-05-31.json
-rw-r--r-- 1 root root 483 Jun  1 02:00 /opt/aether-volumes/aria-layer1/data/cost-snapshots/cost-2026-06-01.json
```

## 3. cost-sentinel cron 近期运行 (exit 状态)
```
Status               = running
Periodic             = true
Next Periodic Launch = 2026-06-02T02:00:00Z (23h29m58s from now)
Children Job Summary
Pending  Running  Dead
ID                                             Status
aria-layer1-cost-sentinel/periodic-1780279200  dead
```

## 结论
- section 1 见 `EXIT=0` → ✅ 3-day 闸门 PASS,M6 e2e-resilience Phase B 可启动。
- `EXIT≠0` → 看 section 2/3:缺哪天 snapshot / cron 是否某日 exit≠0(若某天 dead 非 complete)。

_下一步详见 docs/handoff/2026-05-30-m6-cost-snapshot-hotfix-deployed.md §6_
