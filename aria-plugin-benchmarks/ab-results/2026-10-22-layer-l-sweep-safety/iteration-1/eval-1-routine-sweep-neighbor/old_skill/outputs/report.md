disposition: 会被改写 — active ∧ heartbeat 30h > STALE_TTL(24h) ⇒ --sweep-stale 机械标 abandoned; 规则无「容器可能仍在长会话干活」豁免通道。
basis: phase-d-closer §D.2b「--sweep-stale 顺带把全 ref 内 heartbeat 超 STALE_TTL 的 active claim 标 abandoned」(判据只看 status==active ∧ 年龄>24h, 全 ref 含邻容器); state-scanner「Layer L A.1 heartbeat 集成」自证该语义会误伤仍在干活的轨道 (「一条还在干活的轨道会从所有碰撞面上消失」正是本场景形态); 邻容器 30h 内未再进 /state-scanner 入口则心跳不刷新, sweep 纯按年龄处置。--gc 只归档 done; advisory 契约只管命令级错误处理, 不给单条 claim 判定留裁量。
(注: 子代理 Write 被 harness 拒, 内容由主控从其最终回复落盘)
