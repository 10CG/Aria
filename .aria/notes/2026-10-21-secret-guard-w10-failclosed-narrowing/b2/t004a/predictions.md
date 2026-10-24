# T004a 预期 (先写后跑; 2026-10-24)
## run-evidence.sh 改动
- P0 改后 bash -n 通过; git diff 只动 run-evidence.sh: 头注释、第 8-9 行 (readlink -m / OUT 默认 / 被测 bash 与用例脚本与 OUT 的前置检查 / mkdir -p 核验)、hdr、W8 页眉、W13 循环、五处 cp 目的地 "$HERE/" -> "$OUT/"。
- P1 检查一 (父目录不存在且建不出: /r217-t004a-noparent/sub/work, uid 1000, / 不可写): 退出 3; 该路径不存在; $HERE、OUT、探针目录里没有新文件。
- P1b 两种读法探针 (父目录不存在但建得出: scratchpad 下 probe-noparent/sub/work, 未知阶段 NONE, IMPL 与 OUT 指 scratchpad): 按 design 6 的字面 (mkdir -p 成功即继续) 目录被建出, 写出 base.sh 与 impl.sh, 退出 2 (未知阶段) —— 即「父目录不存在 -> 退出 3」只在建不出时成立。
- P2 检查二 (BASH32=/nonexistent/bash32 跑 W12, TRAFFIC_DIR=冻结语料): 退出 3, 报被测 bash 缺失; 工作目录未建、OUT 无新文件。
- P2b 附加 (不设 BASH32 跑 W13; BASH32 指向非可执行文件跑 W13): 都退出 3, 不起任何重实验。
- P3 OUT 不设: OUT=${OUT:-$HERE}, 五处 cp 都到 "$OUT/" == 原来的 "$HERE/" (读代码)。
## 在实现上跑 W8 W11 W9 (OUT=v31/impl)
- P4 三阶段都打印 done, 退出 0; v31/impl/ 新增 W8-v31.diff、W11-adversarial.txt、W9-suite.txt, 首行 # 页眉含 base e83c5e30f2cc、hook af4658b6f935 与三个用例脚本前缀。
## 对照
- P5 (验收 1) mkv31.py 从基线生成的原型与 95cf1de7 的 W8-v31.diff (去掉前两行路径) 逐字节相同; diff 原型 实现 的每个 hunk 只属于三类: What 1 补充 (_sg_relax_ok 与 _sg_relax_platform 两段, 很可能合成一个 hunk)、What 6 (删一行)、What 7 补充 (四处注释); 五段字面 (What 1 补充一段 + What 7 补充四段) 在实现里逐字连续出现, 原型里不出现; What 6 那一行原型 1 处、实现 0 处; 无「其他」类 hunk。
- P6 (验收 3) 新 W9: impl 节相对 base 节的变化恰为 21ab 21ac 21ag 21aj 21al 21ao 六组; 每条变化断言与 95cf1de7 W9 的原型节逐条相同; SC-13 在 base 节与 impl 节都红 (非 git 副本), 且 95cf1de7 两节同样, 不算变化; 新 W9 的 base 节与 95cf1de7 base 节一致。
- P7 (验收 4) 新 W11 每个形状 (7 个 + 扩展项目 2 个) 的 rc 与文案种类, base 与 impl 两节都与 95cf1de7 W11 相同。
