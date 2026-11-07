# audit-engine Rule #6

每case每臂n=1；所有case均JUDGED。

| 指标 | with_skill | without_skill | 差值 |
|---|---:|---:|---:|
| 逐case通过率均值 | 97.50% | 32.83% | +64.67% |
| Token usage | unknown | unknown | unknown |

精确主差值：`97/150`。

新增行为 with_skill 失败项：0。

## 限制与流程状态

- 每case/臂实际n=1；跨case标准差不是重复运行稳定性；临时定向eval不外推生产成功率。
- Token usage未知（null），未拿上下文指标、字符数或0替代。官方viewer省略未知token行，此处明确缺失。
- 实际执行仅mock/描述性决策层，不替代TASK016真实接线。
- 官方raw聚合已亲跑并保留；其写死n=3/token fallback不采信。本JSON为官方允许的真实统计派生，不修改官方库。
- 只作部分来源遮蔽，不声称完全盲评；所有饱和断言保留。
- 真实人类review/feedback尚未收到，TASK017未验收。

## 分项分析

- 本轮36条配对断言中，11条两臂都通过、1条两臂都失败、24条仅with_skill通过，没有仅without_skill通过的项；每项只有一个样本，不能据此声称重复稳定。
- 固定case 1第二条格式断言两臂均失败。with_skill已正确写出计数、archive已完成状态和红色HTML文字，但未写原断言指定的红点；原FAIL保留，没有改断言、删项或重跑求绿。固定组with为12/13断言，逐case均值11/12；without为3/13，逐case均值7/30。
- case101三条均两臂通过，本轮无法证明Skill在该原始字符串守卫/disabled优先级输入上的额外收益；该饱和case与全部断言保留。
- 7个新增行为case的with_skill合计23/23断言通过，without_skill为8/23；本轮差异主要位于完整legacy路径、独占prepare/final/check/消费链、unknown资源与真实耗尽处置协议，而非仅能识别非法类型。
- case2 with_skill的四条探针断言均通过，但额外声称Challenge必须全部resolved。实读冻结before与current，execution-modes的全部resolved简述与convergence-algorithm的resolved/overruled均可处理条件两版都并存；这是已存在的措辞差异观察，不把它隐去，也不在本次评测中改源或断言。
- 审计侧with_skill平均135.4587秒，without_skill平均77.5001秒，差57.9586秒。这里是描述性eval执行者耗时，不是生产审计的120/300秒界限验证；不能仅凭相关性把全部耗时差归因于某一条新指令。
- 97.50%与32.833333%是每个case等权的通过率均值，不是把不同断言数直接相除的微平均；精确差值97/150。
- 正式主比较是当前Skill与无Skill，不是旧Skill与新Skill；它不独立证明本次改动相对旧Skill的边际提升。TASK013旧/新兼容观察和TASK016真实接线另有来源，不能互相替代。
- 模型原生标识为Codex API/gpt-6.1-sol，两臂相同且无override；来源仅部分遮蔽。token消耗未知，原usage观察保留，不使用上下文指标、字符数或0充当消耗。
- 真实人类review/feedback尚未收到；数值门为正不等于TASK017或Phase B已完成。
