# v6 预登记: 逐调用健康检查 (2026-09-15, 跑前写定)

## 目的

owner 2026-09-15 裁定: 场景 4b 的故障识别「先做实验再重新设计」。v7 的同批参照臂在 post_spec R6 被判两处漏洞: 故障只落在一臂或落在 should-not 半程时接不住; 有意改套件划分、新增 skill、修复已坏 description 三种正当情形下必然作废。本轮验证替代方案: 垫片为每次 `claude -p` 调用另存一份输出流, 检查脚本逐次判断这次调用有没有正常完成。

## 设计 (跑前冻结)

- 垫片 `claude-shim-logging.sh`: 追加 `--setting-sources project`; stdout 经 `tee` 原样转交 run_eval.py 并另存一份; 首尾各写一行起止时间; stderr 另存。
- 检查脚本 `classify_calls.py`:
  - 判定事件 = 输出流里出现 tool_use 开始 / message_stop / 含 tool_use 的 assistant 消息 / result 帧, 与 run_eval.py 的提前返回点一一对应。
  - 单次调用健康 = 起止记录齐全, 且有判定事件, 且没有报错的 result 帧, 且耗时小于超时阈值减 1 秒。
  - 一臂健康 = 日志数等于 run_eval 输出里各 query 的 runs 之和, 且每次调用都健康。
  - 退出码 0 健康 / 1 不健康 / 2 无法判定。

## 实验与预期

A. 假 claude 故障矩阵 (不调用任何 API; 2 条 query 的单元用例 + 20 条真实套件的场景用例):
- 正常四类 (触发 / 不触发 / 先调别的工具 / 带 api_retry 帧): run_eval 判定与假 claude 的设定一致; 检查判健康。
- 故障七类 (result 帧报错 / 只有 init 就退出 / 无输出即退出 / 开了消息但没到判定点就退出 / 挂起到超时 / 判定事件晚于超时 / 垫片指向的真 claude 不存在): run_eval 记成「未触发」且 stderr 无 Warning; 检查判不健康。
- 垫片不在 PATH 上: run_eval 打 Warning, 日志数 0; 检查判不健康。
- 场景: 过宽被评臂在 should-not 半程故障 ⇒ run_eval 门通过 (假绿), 检查判不健康; 正确被评臂在一条 should-trigger 上故障 ⇒ 门判 fail (假红), 检查判不健康; 无故障的正确臂、过宽臂、负控臂 ⇒ 检查健康。

B. 真实报错探针 (真 claude, 2 条 query, runs 1): 不存在的模型名 ⇒ 检查判不健康; `--timeout 3` ⇒ 超时的调用判不健康。

C. 真实全量两臂 (`claude-opus-5`, 20 条 × 3 runs, 单 worker, 各自独立项目根与日志目录, 同批并行): 被评 = 现行 openspec-archive description (与 v5 的 new 臂同一字符串); 负控 = 「对一个事项做处理。」。预期: 两臂检查均健康 (120 次调用零误报); run_eval 结果与 v5 同向 (被评门通过; 负控 should-trigger query 级命中 ≤ 5/10, v5 为 0/10)。

## 判读规则 (跑前写定)

- A 或 B 中任一预期不成立 ⇒ 设计不成立, 不写进 v8, 如实报 owner。
- C 出现误报 (真实调用被判不健康) ⇒ 逐条查原因; 若须改规则, 改后 A、B、C 全部重跑, 并在 RESULT 记录改动与原因。
- C 的 run_eval 结果与 v5 不同向 ⇒ 如实记录, 不据此改检查规则; 垫片对 run_eval 透明这一点由 A 的正常用例佐证。
- 成本上限: C 约 120 次调用 (约 10 美元, 并行约 15–20 分钟); 超出一倍即停下报 owner。
