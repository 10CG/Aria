# eval-13 a1-heartbeat-on-entry-TARGETED 评分员意见

结果: 臂 X 6/6, 臂 Y 6/6 (匿名, 评分员不知道哪臂对应哪个版本)。

## 逐条断言可判别性

1. **[承重] (A) 给出 `--heartbeat-only` 调用, 含 `phase1_gate.py` 与 `--phase A.1`**: 可判别。前提是某一臂的 skill 文本里有这条命令行模板。两臂都读了 skill 文本并照抄了模板 (X 的 exec_notes 写明读的是 `old-arm-1cb3872` 目录下的 SKILL.md)。如果两个版本都带这段, 这条断言对 AB 来说**实际恒真**, 测不出版本差异。
2. **[承重] 目的是刷新既有 claim 的 heartbeat_at, 不是新认领**: 可判别, 但判定标准偏宽。X 只写了「刷新心跳 / TTL 重新计时」, 没有明说「不新建 claim」; Y 明说「只改写 heartbeat_at … 也不新建 claim」。两臂都按实质判过。建议把断言拆开: 把「显式否定新认领」单独列成一条, 这样才能区分两臂。
3. **[承重] (B) enabled==false ⇒ 零 heartbeat / 不写 claim / 不推送**: 可判别。三项用斜杠连接, 写法有歧义: 是三项都要显式写出, 还是写出等价的「零调用」就够? X 三项都显式写了; Y 写的是「两条闸门入口都零调用」, 按等价判过。建议明确这条断言的判定口径。
4. **[承重] (C) 不改变, 触发不依赖 collision.kind**: 可判别, 但在本 prompt 里接近恒真。题面 (C) 的问法已经暗示了答案, 而 SKILL.md 触发条件那行原文就有「不依赖 `collision.kind`」。只要能读到这行, 模型几乎不会答错。
5. **不把 (A) 答成认领或完整闸门**: 否定式断言, 只要没有写错就算过, 判别力弱。两臂都主动把 A.1 心跳和 Phase B 认领闸分开写了, 这是超过断言要求的表现, 但断言本身奖励不到。
6. **不声称心跳遥测进 production 分区**: 否定式断言, 对「压根不提遥测」的回答也恒真。两臂都正面写了「heartbeat 分区, 不进 production」, 但都没有提到「coordination_probe 不计」这半句。建议改成正向断言: 「说明心跳遥测走独立 heartbeat 分区, 且 coordination_probe 不计入」。

无法从产出核验的断言: 无。本 eval 是只答不跑, 全部证据都在 answer.md 里。

## 两臂差异是否来自断言测得到的东西

**不是。** 6 条断言两臂全过, 分数上零差异。实际差异都落在断言覆盖不到的地方:
- Y 核对了代码: 读了 `heartbeat_by_track`、`derive_track_id`, 验证了 track_id 长度 44 ≤ 64、原样传入可以对上; 还说明退出码恒为 0、outcome 是 `refreshed`/`error`, (B) 应在报告里记 `skipped_disabled`。评分员已核对, `skipped_disabled` 确实存在于 phase1_gate.py 的 outcome 词汇表里 (1142-1143 行), 由调用方上报。
- X 额外讲了 Step 0 的 scan.py 硬约束和 fail-CLOSED 新鲜度谓词。Y 也提到了新鲜度谓词。
- 两臂对 scan.py 与心跳的先后顺序说法不同: X 是先 scan 再心跳, Y 是心跳后再 scan。SKILL.md 没有规定这个顺序, 断言也没测。

## 建议

- 增加一条可判别的断言: (B) 是否建议在报告里写明 `skipped_disabled`, 让读者能区分「被配置关闭」和「心跳从没跑过」。这正是 SKILL.md 强调的可分辨性原则 (对应 `skipped_no_track` 那一段)。
- 增加一条可判别的断言: carry-id 是否原样传入 (由 CLI 内部归一, 编排层不预先处理)。
- 本 eval 名为 TARGETED, 但 6 条断言在两臂上都不失分。如果目的是测新旧版本的差异, 需要先确认旧版 skill 文本里是否已经有「Layer L A.1 heartbeat 集成」这一节。如果已经有, 这个 eval 对本次改动没有判别力。
