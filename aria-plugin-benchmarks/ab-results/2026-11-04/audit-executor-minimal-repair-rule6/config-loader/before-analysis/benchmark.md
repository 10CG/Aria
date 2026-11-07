# config-loader Rule #6

每case每臂n=1；所有case均JUDGED。

| 指标 | with_skill | without_skill | 差值 |
|---|---:|---:|---:|
| 逐case通过率均值 | 100.00% | 77.78% | +22.22% |
| Token usage | unknown | unknown | unknown |

精确主差值：`2/9`。

新增行为 with_skill 失败项：0。

## 限制与流程状态

- 每case/臂实际n=1；跨case标准差不是重复运行稳定性；临时定向eval不外推生产成功率。
- Token usage未知（null），未拿上下文指标、字符数或0替代。官方viewer省略未知token行，此处明确缺失。
- 实际执行仅mock/描述性决策层，不替代TASK016真实接线。
- 官方raw聚合已亲跑并保留；其写死n=3/token fallback不采信。本JSON为官方允许的真实统计派生，不修改官方库。
- 只作部分来源遮蔽，不声称完全盲评；所有饱和断言保留。
- 真实人类review/feedback尚未收到，TASK017未验收。
