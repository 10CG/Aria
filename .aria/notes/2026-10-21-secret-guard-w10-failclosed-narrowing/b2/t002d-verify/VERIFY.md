# T002c-3b 主控复核记录 (2026-10-24 UTC 12:37-12:57; 预期见同目录 PREDICT.md, 写于开跑前)

对象: worktree 未提交改动 (套件 3a64827 之上 +145 / -45) 与主仓 v31/commentsync.py (+92 / -0)。hook af4658b6f935 不变。
驱动 drive.sh: 串行, 每轮开跑前等一分钟负载 < 1.2, 重实验 taskset -c 0,1 nice -n 19; 读数在 drive.log。

## 代码审读 (要点)
- sg_w10_cases 只在一处调用 (移植块之后、第一条旧用例之前); SG_W10_ONLY 设了时打印过滤轮汇总后退出; SC-13 前的调用已删。
- 6 组的分支判据 wpa_rx6 只算一次: sg_w10_relax_rule 问 `env bash` (PATH 上的 bash, 与 hook 的 shebang 同一查找), 加内核串、WSLInterop 文件, 且套件环境里
  WSL_DISTRO_NAME、WSL_INTEROP 都为空。sg_w10_relax_rule 与移植用例原来那行逐项等价 (缺参时 MAJ / MIN 取 0, WSLInterop 缺省 yes: 都按不放宽)。
- 6 组放宽支: wpa_x_longline (退出码 2、has a line longer than、Matched pattern:、不是尺寸文案、全文 < 3000 字符)、wpa_x_hit (退出码 2、
  value-REDACTING filter、不是 longline 文案)、21ag / 21aj 用 wpa_x_toolarge 配增长原因串; 基线支原断言一字不改; 每组仍是一个用例。
- Expects 行按实查改写: 跑套件的 bash 须 5.0 以上 (SC-8 与 sg_w10_run 直接读 $EPOCHREALTIME); jq; python3 (SC-20 与 SC-19 census); timeout; ps; git; zsh 可选。
- commentsync.py 只加不删: SUITE_TEXT (第 9-15、21、22 处的旧句与新句) 与 check_suite_text。

## 结果对照预期
| 项 | 预期 | 实测 | 一致 |
|---|---|---|---|
| R4 21ab (b) 放行命令 x3 | rc 0, 2.2-2.7 s | rc 0, 2.37 / 2.48 / 2.39 s (负载 1.17-1.64) | 是 |
| R4 21ab (c) 放行命令 x3 | rc 0, 2.2-2.7 s | rc 0, 2.52 / 2.54 / 2.58 s | 是 |
| R4 两条命令关门 (WSL_DISTRO_NAME) | rc 2、尺寸文案, < 1 s | rc 2、尺寸文案, 2.39 s 与 3.08 s | **否 (预期错)**: 时间主要花在先跑的基线那一遍, 放宽重跑只占约 0.1-0.2 s |
| R3 commentsync target (worktree hook + 套件) | GREEN | GREEN (194 项 ok) | 是 |
| R3 commentsync baseline (59e333c, sha256 e83c5e30f2cc) | GREEN | GREEN (184 项 ok) | 是 |
| R3 构造 c1: 第 9 处一条新句里唯一的词 rulings 改一个字母 | RED | RED (1): 第 9 处那条新句 n=0 | 是 |
| R3 构造 c2: 删掉 21ag 前的整段注释 (4 行) | RED | RED (3): 定位不到注释段 + 两条新句 n=0 | 是 |
| R1 整轮 PATH 上的 bash | 961, FAIL 0, SKIP 0, judged, relaxed branch, SC-13 绿 | 961 PASS, FAIL 0, SKIP 0; 计时批 1.15 -> 1.29 judged; 6 组 relaxed branch; 移植 136 PASS | 是 |
| R2 整轮只导出 WSL_INTEROP | 961, FAIL 0, baseline branch, 移植 136, judged | 961: PASS 932 / FAIL 0 / SKIP 29 ([void]); 6 组 baseline branch; 移植 136 个编号 (107 PASS + 29 SKIP [void]) | 是, 计时批一项除外: 批末负载 2.04, 按 INV-7 作废 (负载规则如设计起作用; 移植用例与 R1 同样清掉两个 WSL 变量, R1 已判过) |

## 发现与裁定依据
1. 21ab 的放宽支命令整个 hook 约 2.4-2.6 s, 离 3 s 截止 0.4-0.6 s; 关门时同一命令也要 2.4-3.1 s。所以主机稍慢, hook 就按 What 4 回落成基线拦截
   (_sg_relax_left 只在截止已过时才关门, 回落时墙钟约 >= 3 s)。执笔席的 3.2.57 第一轮 21ab (c) 得 exit 2 就是这一情形。
2. 不宜加负载门: 6 组排在套件后部, 3b 的 7 次整轮与本复核的 2 次整轮, 整轮结束时的负载都 >= 2.21, 加门后几乎每轮 SKIP。
   主控裁定 (交 3c 实现): 触发点上的命令, 放宽支断言成立即通过; 否则同一份输出满足基线支断言、且墙钟 >= 2.85 s 时也通过并计为「截止回落」; 都不成立为 FAIL。
