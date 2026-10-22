heartbeat_state: 严重过期 (~72h ≈ 3×SWEEP_TTL), 「下一次例行收尾必被扫」状态 — 心跳唯一挂载点 = /state-scanner 入口 (触发条件原文), 无入口外周期刷新机制; 任何其他 session 的 D.2b 收尾就会扫掉本条 active claim。
action: 立即补刷一次, 此后 B.2 期间间隔 <24h (由 SWEEP_TTL 反推; skill 未给显式刷新周期, 长会话只能靠自觉手动执行 --heartbeat-only 或重进 /state-scanner)。要点: 同一原始串; fail-soft 但刷完须确认成功; 若已被扫: 补心跳未必复活 abandoned, 需查实际状态必要时重新认领 (earliest claimed_at 仲裁); 收尾对偶走 D.2b 显式释放。
(注: 子代理 Write 被 harness 拒, 内容由主控从其最终回复落盘)

done: 仅入口刷 (子代理原文结论行)
