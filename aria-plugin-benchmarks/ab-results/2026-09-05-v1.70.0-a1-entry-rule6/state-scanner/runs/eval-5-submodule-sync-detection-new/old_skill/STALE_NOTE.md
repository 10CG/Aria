# 作废说明

`grading.STALE.json` 评的是一份**已被覆盖的答卷** —— 主控调度失误, 该臂被重复派发一次,
第二次的 `answer.md` 覆盖了第一次, 而评分发生在覆盖之前 (mtime 实测: grading < answer)。

留档不删 (审计痕迹), **不参与任何计分**。以同目录下重新生成的 `grading.json` 为准。
