# v5 预登记 (2026-09-14, 跑前写定, 不事后改)

目的: 回应 post_spec R3 qa 席 major —— 地板守卫对「自然措辞扩张」(无强制指令, 只多几个泛化词) 的敏感度零证据。

模型: claude-opus-5 (基线 v1–v4 用 claude-fable-5-1; Fable 额度已耗尽, 故本轮三臂全部在 opus-5 上同批跑, 只做臂间比较, 不与 v3 数字直接比)。
配置: 同 v3/v4 —— 中性名 `helper` 壳 / 每臂独立项目根 / --num-workers 1 / --runs-per-query 3 / --trigger-threshold 0.5 / --timeout 120 / --setting-sources project。

三臂:
- mildcreep (被评): 「归档已完成的 OpenSpec 变更与相关文档到 archive/ 目录，整理项目收尾材料，并做归档后落点校验。 使用场景："归档 Spec"、"Phase D.2"、"完成变更归档"、"整理归档文档"、"收尾整理"」
- new (参照): v1.73.0 原 description
- negctrl (同批负控): 「对一个事项做处理。」(按 v3 §D2 新构造规则: 删去领域名词与特有动作词, 只留「处理一件事项」级)

预期与判读 (写定):
- new 须通过门 (should 10/10 query 级, should-not 0 条 ≥ 0.5); 否则本轮在 opus-5 上的套件/环境不可用, 不解读 mildcreep。
- negctrl query 级命中须 ≤ 5/10; 否则本轮作废 (v3 §D2)。
- mildcreep 判「守卫对自然扩张敏感」当且仅当: 至少一条 should-not 的 trigger_rate ≥ 0.5 (即门判 fail)。最可能被误触的四条: handoff 归档 / 审计报告 tar 归档 / archive 分层脚本 / sprint changelog 归档。
- mildcreep 若门通过 (0 条 should-not ≥ 0.5): 判「在本套件上, 该幅度的自然扩张不被守卫判为改坏」—— 这是对 §D2「只承诺两类破坏」局限的实证确认, 不是守卫失效的证据 (守卫的定义就是看套件里的近似误触)。
