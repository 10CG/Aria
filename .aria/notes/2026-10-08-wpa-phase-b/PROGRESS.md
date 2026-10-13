# WP-A Phase B 进度 (会话中途记录, 供中断后续接)

> 最近更新: 2026-10-11 15:xxZ (TASK-001 – 009 完成; TASK-014 审查完成 —— 0 critical / 8 major / 5 minor, 主控独立复核 6 条成立, 修补进行中; 期间停掉第一位执笔遗留 70 小时的自匹配等待循环, 认领心跳过期 31 小时后续上)。正式的会话交接按 Rule #9 写在 `docs/handoff/`; 本文件只是 Phase B 的进度锚 (Phase A 的进度锚见 `../2026-09-30-wpa-phase-a/PROGRESS.md`)。任务定义见 `openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml`, 每完成一条任务向 owner 报一行成本 (决策单 `.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md`)。

## 成本账 (每条任务一行)

| 任务 | 墙钟 (UTC) | 子代理 token | 产出 |
|---|---|---|---|
| TASK-001 | 09:43Z – 10:15Z 约 32 分钟 (探针复跑占 24 分钟) | 0 (主控独做; 主控上下文 10:14Z 为 23.6 万 / 100 万) | B.0 认领、两个特性分支、行号核验、SC-30 基线、环境核验、探针复跑逐字节一致; 代码 0 行 (本任务不改代码) |
| TASK-002 | 10:18Z – 12:19Z 约 2 小时 (执笔首轮约 72 分钟 + 返修约 35 分钟 + 主控复核) | 执笔 169 次调用: 缓存读 100,173,589 / 缓存写 1,631,422 / 输出 42,965 (上下文峰值 86.5 万; 原记的 867,303 是上下文大小, 见下方口径更正); 主控上下文 23.6 万 → 33.5 万 | 测试 +1471 / −1 行 (新增 260 条用例), aria `ec99e6c` (本地); 主控复核抓到 1 个缺陷 (相对路径调用退 127), 已由执笔返修 |
| TASK-003 | 12:21Z – 13:20Z 约 1 小时 (执笔约 46 分钟 + 主控复核) | 执笔 115 次调用: 缓存读 38,200,311 / 缓存写 1,120,533 / 输出 9,407 (12:39Z 上下文压缩, 段末上下文约 21 万); 主控上下文 33.5 万 → 38.4 万 | aria `7567fe5`: secret-scan.sh +31 / −6 (W1)、hooks.json +12、两个套件 W6 / W7; 转绿 10 条, 新增失败 0 |
| TASK-004 | 13:21Z – 13:54Z 约 33 分钟 (执笔约 23 分钟 + 主控复核) | 执笔 47 次调用: 缓存读 14,444,557 / 缓存写 353,399 / 输出 12,574 (段末上下文约 35 万); 主控上下文 38.4 万 → 42.7 万 | aria `2e2a2a8`: secret-scan.sh +152 / −7 (W2–W5); scan 套件 122 / 122; 「上下文卫生」要求后真实用量约为 TASK-002 首轮的四分之一 |
| TASK-005 | 13:57Z – 14:4xZ 约 45 分钟 (执笔约 30 分钟 + 主控复核) | 执笔 52 次调用: 缓存读 22,149,851 / 缓存写 477,816 / 输出 2,527 (段末上下文约 48 万, 又在累积) | secret-guard.sh +49 / −6 (W8 + W11)、测试 +19 / −4 (census 61 → 64 与 3 条 family 探针); guard 转绿 66 条, 新增失败 0 |
| TASK-006 | 10-08 14:43Z 派出 → 10-09 00:2xZ 提交; 实际工作约 30 分钟 + 主控复核 (中间整个会话停了约 9 小时, 见下) | 第二位执笔 69 次调用: 缓存读 10,582,994 / 缓存写 584,966 / 输出 6,461 (段末上下文约 23 万) | secret-guard.sh +19 / −2 (W12); guard 转绿 4 条, 新增失败 0 |
| TASK-007 | 10-09 00:27Z – 01:25Z 约 1 小时 (执笔约 40 分钟 + 主控复核) | 第二位执笔 65 次调用: 缓存读 20,608,851 / 缓存写 1,119,921 / 输出 3,120 (段末上下文约 40 万) | aria `db4f8b8`: secret-guard.sh +258 / −42 (W9 + W10 + `_sg_emit_blocked`); **两个套件全绿** (783 / 783、122 / 122) |
| TASK-008 | 10-09 01:25Z 结项 (主控核对, 不派执笔) | 0 | W14 元耦合已随各任务同步, 以 TASK-007 的复核结项; SC-27 / SC-28 移入 TASK-009 (见 TASK-008 节) |
| TASK-009 | 10-09 01:27Z – 02:20Z 约 53 分钟 (执笔约 40 分钟 + 主控复核与两处补正) | knowledge-manager 144 次调用: 缓存读 42,550,367 / 缓存写 874,811 / 输出 5,360 (段末上下文约 44 万; 本轮最「碎」的一位) | aria `69af7cd` (README 两语种、两个 hook 只改注释、VERSION 描述、hooks.json description) + standards `be842ce` (secret-hygiene 1.2.0) + changelog 草稿; 探针 SC-25/27/28 全 yes, SC-26 10/11 (26g 移 TASK-010) |
| TASK-014 | 10-11 10:08Z – 14:28Z 审查约 4 小时 20 分 (新 qa-engineer 实例, 派单 `dispatch/review-task014.md`); 修补进行中 | 审查席 280 次调用: 缓存读 148,784,301 / 缓存写 10,945,111 / 输出 558,452 (上下文峰值 91.5 万; 缓存写的 92% 来自 13 次「单次调用超过 5 分钟 → 整份重写」; 折算约等于 TASK-002 – 009 全部执笔之和); 另记一笔非任务开销: 10-11 停遗留 shell 唤醒第一位执笔 1 次调用, 缓存写 499,584 (缓存已过期) | 审查报告 `.aria/audit-reports/post_implementation-R1-2026-10-11T142603-595Z-…-qa-engineer.md`: 0 critical / 8 major / 5 minor, 667 个坏实现; 修补见 TASK-014 节 |

### 计量口径更正 (2026-10-08 13:1xZ)

harness 在子代理完成通知里给的 `subagent_tokens` **不是消耗量**, 而是该子代理**最后一次调用时的上下文大小**: TASK-003 完成时它报 217,566, 比 TASK-002 返修后的 867,303 还小 —— 中间 12:39Z 发生过一次上下文压缩。上表 TASK-002 行里的 779,280 / 867,303 应读作「上下文峰值」。Phase A 进度锚里「1400 万 subagent token」一类数字若取自同一字段, 口径相同, 也不是消耗量。

真实消耗用脚本从执笔的 transcript 按 `requestId` 去重汇总 (只输出聚合数, 不读内容):

| 段 | API 调用 | 缓存读 | 缓存写 | 输出 | 段末上下文 |
|---|---|---|---|---|---|
| TASK-002 首轮 | 123 | 62,717,897 | 766,806 | 39,463 | 766,808 |
| TASK-002 返修 | 46 | 37,455,692 | 864,616 | 3,502 | 864,618 |
| TASK-003 | 115 | 38,200,311 | 1,120,533 | 9,407 | 205,963 |
| 合计 | 284 | 138,373,900 | 2,751,955 | 52,372 | — |

成本的主因是**大上下文 × 多次工具调用**: 执笔把 240 KB 的 proposal 与 245 KB 的探针整份读进来, 上下文到 77–86 万 token, 之后每次调用都重读一遍 (缓存读)。压缩后约 21 万。后续派单加「上下文卫生」要求 (只按行号范围读需要的节、大输出落文件只看摘要)。

## TASK-001 (B.1 入场) — 2026-10-08

### 认领与分支

- B.0 认领: `phase1_gate.py --raw-track-id secret-net-l3-and-bypass-paths-023236f2 --phase B --mode advisory --linked-issue 10CG/aria-plugin#154` → `outcome=passed`, 新 session `s-d2f7@0945` (phase B, active), `linked_issue_overlap=[]`; 协调 ref 推后 `ls-remote origin` 与本地一致 (`6b75e07`)。
  - 注意: carry-id 必须用全称 `secret-net-l3-and-bypass-paths-023236f2`; 只传 Spec 名时心跳返回 `claim_not_found`。
- 分支 (只在本地, 尚无提交, 未推送):
  - aria `feature/secret-net-l3-and-bypass-paths` @ `268da8f39d8bc33967e7cdaa5681e3a221fb9e4b`
  - standards `feature/secret-net-l3-and-bypass-paths` @ `2bc1c4c619c5125a1bb2963864c1683fd9a87739`
  - 建分支前核验: 两个子模块 master 的本地、origin、github 三处一致, 远端无同名分支。

### 行号 (对 `268da8f` 核差异)

被测文件 sha256 前 16 位与 `baseline-evidence.md` 逐个一致, aria 相对 `268da8f` 无差异 ⇒ Spec 内行号全部有效, 无需重取:

| 文件 | sha256[:16] |
|---|---|
| `aria/hooks/secret-guard.sh` | `448b1f71a2af06d7` |
| `aria/hooks/secret-scan.sh` | `c5f53f7a164fa72e` |
| `aria/hooks/tests/secret-guard.test.sh` | `72f8e7d5d58a4b80` |
| `aria/hooks/tests/secret-scan.test.sh` | `78e0e4ca15078177` |
| `standards/conventions/secret-hygiene.md` | `dcf203f1f25ef0c0` |

### SC-30 基线 (真 checkout, 带 git 历史)

- 对象: `/home/dev/Aria/aria` (子模块真 checkout, `af87cae` 可达), 命令 `HOME=<scratchpad 私有目录> bash aria/hooks/tests/secret-guard.test.sh`。HOME 指向私有目录是 INV-5 的要求 (W6: 套件本身不隔离 HOME)。
- 结果: **`PASS: 593 / 593`, `FAIL: 0 / 593`**, 退出码 0, stderr 为空, 墙钟 140 s。
  - zsh 未安装, zsh 用例按设计跳过; 593 等于头注释的「593 without zsh」(测试内 SC-13 一致)。
  - 测试内 SC-9a 的 `af87cae` 对拍实际执行 (输出里没有 SC-9a 的 SKIP 行)。
- 测试内 SC-8 五档 (N=10, rounds=20, min-of-rounds, `BASH_VERSION=5.2.15(1)-release`, 测时 loadavg `2.32 1.54 1.14`), 全部低于天花板 100 ms (absolute 腿):

  | 档 | old (ms/call) | new (ms/call) | 天花板 |
  |---|---|---|---|
  | (a) | 29.6 | 6.9 | 100.0 |
  | (b) | 29.2 | 12.8 | 100.0 |
  | (c) | 29.1 | 7.8 | 100.0 |
  | (d) | 28.8 | 12.0 | 100.0 |
  | (e) | 29.9 | 47.1 | 100.0 |

- loadavg: 开跑前 `1.27 1.23 1.01`, 跑完 `3.69 2.25 1.42`。本会话进程树 nice 19、ionice best-effort 7、只用 0–1 号核。
- 外溢核验: 真实 `~/.claude/logs/guard-bypass.log` 跑前跑后大小与 mtime 不变; 私有 HOME 下的 `guard-bypass.log` 写入 1571 字节, 记录之间没有换行 (`wc -l` 为 0, 即 10CG/Aria#229 描述的形态); aria 工作区跑后干净。

### 环境 (SC-32 / SC-29 的腿)

- 非 root: uid 1000 (SC-20 20g 可构造)。
- `WPA_BASH32=/home/dev/.aria/tools/bash-3.2.57/bash`: sha256 前 16 位 `5997a028c645039d` (与上一会话记录一致), `GNU bash, version 3.2.57(2)-release (x86_64-unknown-linux-gnu)`。
- 第二个 locale: `locale -a` 列出 `en_US.utf8` (`WPA_LOCALE_B` 用默认值 `en_US.UTF-8`); `C.utf8` 也在。`localedef` 与 `/usr/share/i18n/locales/en_US` 都在 (本次用不到)。

### 探针复跑 (带 `WPA_BASH32`)

- 布局与 `baseline-evidence.md`「怎么跑」第 1 条相同: 把 `aria` 与 `standards` 用 `cp -a` 复制到 scratchpad 的 `<X>/base/`, 删去两处 `.git` gitfile; 探针原地运行 (`openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py`, 旁边是当前分支上的 `proposal.md` 与 `baseline-evidence.md`)。
- 命令: `WPA_BASH32=/home/dev/.aria/tools/bash-3.2.57/bash TMPDIR=<X>/tmp HOME=<X>/home python3 <spec 目录>/baseline_probe.py <X>/base/aria`。与文档命令相比只多了 `HOME=<私有目录>` (INV-5); 探针本身也给 hook 自建私有 HOME (`baseline_probe.py:37/126`)。
- 运行前写下的预测: stdout 等于证据内嵌块, 即 sha256 前 16 位 `a3603d2ee85cd552`、106384 字节、stderr 为空; 唯一的风险点是 15e (它扫描 `proposal.md` 全文, 而 `proposal.md` 在证据生成后又被 `3b6c5c9` 改过)。
- 结果: **stdout 与证据内嵌块 (`baseline-evidence.md` 第 47–557 行) `cmp` 逐字节相同**, sha256 前 16 位 `a3603d2ee85cd552`, 106384 字节; stderr 0 字节; 退出码 0。预测全部成立, 15e 没有变化。
  - 末尾形态行: `rows not run (n/a): by design 1 (30a); leg missing or not constructible 0 (-)`; 基线形态 `holds`; 目标形态 `does not hold` (基线上本应如此)。
  - 墙钟 1431 s (约 24 分钟; 2 核限流, 跑完时 loadavg `9.20 11.03 10.48`, 主要是探针自身的进程)。上一会话同样限流下约 17 分钟。
  - 私有 `TMPDIR` 已被探针清理, 私有 HOME 下没有留下文件。

### TASK-001 验收 (`detailed-tasks.yaml` 的三条 verification)

1. 两个特性分支存在且基于 `268da8f` / `2bc1c4c`: ✅ (`merge-base --is-ancestor` 两个都成立, HEAD 即基线 SHA)。
2. 带 `af87cae` 历史的真 checkout 上 `secret-guard.test.sh` 基线结果与 loadavg 记入 `.aria/notes`: ✅ (本文件「SC-30 基线」节)。
3. `WPA_BASH32` 指向可执行的 bash 3.2.57; `locale -a` 含 `WPA_LOCALE_B`: ✅。

另: Tasks 1.1 要求的「复跑 `baseline_probe.py` (带 `WPA_BASH32`), 输出与 `baseline-evidence.md` 逐字节一致」: ✅ (上节)。

## TASK-002 (测试先行, 关键子集) — 2026-10-08

- 派单: `dispatch/impl-task002.md` (10:18Z); 执笔 = 1 个新派 aria:backend-architect 实例 (TASK-002 – 009 同一实例逐条续派)。
- 执笔首轮报告 (11:28Z; harness 计 779,280 token / 146 次工具调用 / 约 72 分钟): `secret-scan.test.sh` 49 → 122 条, `secret-guard.test.sh` 593 → 780 条 (含 zsh 786; 头注释已同步); +1459 / −1 行; 自报基线上失败集合恰等于新增 bf 集合 (scan 44 / guard 115)。
- **主控独立复现 (同一真 checkout, 新的私有 HOME, 从 `/home/dev/Aria` 用相对路径调用)**:
  - scan: `PASS 78 / 122`, `FAIL 44`, 失败全是 bf ⇒ 与报告一致;
  - guard: **`PASS 603 / 780`, `FAIL 177`** ⇒ 与报告 (665 / 115) 不符。多出的 62 条是新增守卫类 (rg 25 / ag 21 / kl 16), 失败信息全是 `got 127`。
  - 根因: `$HOOK` 由 `dirname "$0"` 派生, 相对调用时是相对路径; 新增 helper `wpa_rc` / `wpa_err` 先 `cd "$wpa_cwd"` 再执行它 ⇒ 127。执笔用绝对路径调用, 没碰到。探针正是用相对路径跑套件 (`baseline_probe.py:2034-2043`), 不修则 TASK-010 验收必撞; 且相对调用下 115 条 bf 的「红」来自 127 而不是基线 hook 的行为。
  - 外溢核验: 真实 `guard-bypass.log` / `secret-scan.log` 跑前跑后大小与 mtime 不变。
- 返修单 `dispatch/impl-task002-rework.md` 已交回同一执笔实例 (修法: 新增块内一次性解析绝对路径并同类全查; 验收: 三种调用方式结果相同、失败集合恰等于 bf 集合、`got 127` 计数为 0)。
- 主控对执笔报告第 5 节的技术级裁定 (待 owner 复议): SC-35 35a / 35b 移到 TASK-004 验 (已核 `baseline_probe.py:2634`: 每行三个成员里两个依赖 W2); SC-14b 并入 TASK-003; 27b / 27d 接受执笔做法 (派单里「基线应红」是主控写错)。`detailed-tasks.yaml` 的 TASK-003 / TASK-004 已按此修订。
- 执笔返修报告 (12:10Z, 约 34 分钟): 两个套件新增块里把 hook 与套件自身路径一次性解析为绝对路径 (含 `wpa_tmp`), 同类全查到 `wpa_hook_copy` / SC-31c / SC-32b 等处; 自报三种调用方式 × 两个套件结果相同, `got 127` 为 0。
- **主控复核 (返修后, 从 `/home/dev/Aria` 相对路径调用, 新的私有 HOME)**:
  - scan `PASS 78 / 122`、`FAIL 44`; guard `PASS 665 / 780`、`FAIL 115`; stderr 皆空; `got 127` 计数皆 0。
  - 失败集合 vs 源码里的 bf 用例名: scan 44 = 44 逐名相等; guard 115 = 115 (检查器第一版未做 shell 反转义、且用 `\[(.*?)\]` 提取会在含 `]` 的用例名处截断 —— 两处都是检查器自身的问题, 修正后只剩 SC-19j 一条截断前缀, 与源码名对应)。
  - Rule #7: 两个文件的新增行 (各约 735 行) 作为 Bash 输出喂基线 `secret-scan.sh`, 零告警; 正控 (同一文本末尾拼一行进程内生成的 AWS key id 形状, 不打印) 告警为真, 检查有效。
  - 范围: aria 只有两个测试文件变动, LF, 权限未变。
- 提交: aria `feature/secret-net-l3-and-bypass-paths` 上 `ec99e6c` (**仅本地**, 尚未推送; 主仓的 aria gitlink 暂不提交, 避免主仓分支推送后指向远端不可达的子模块提交)。
- 返修报告的建议 (未改, 记录): 套件变慢无低成本大改法; SC-12k 与 SC-35a/35b 各对同一输入跑两遍, 合并约省 4 秒; 可加一条「helper 能到达 hook」的前置用例防复发 (会让计数变 787 / 781)。

## TASK-003 (W1 提取 + W6 两个套件隔离 HOME + W7 既有夹具拼装) — 2026-10-08

- 派单 `dispatch/impl-task003.md` (12:21Z); 执笔报告 13:07Z。交付字节 sha256[:16]: `secret-scan.sh` `159690401f786cda` / `hooks.json` `9977397a3908d052` / `secret-scan.test.sh` `0e009b821504520b` / `secret-guard.test.sh` `e19767ec2d8a03ee` (主控提交前逐个核对一致)。
- W1 实现要点 (主控审读 diff): 提取链只加 `.tool_response.file.content` 与链尾 `.error`; 事件名经子串预检 + jq 全等确认, 输出只取两个字面量之一; NUL 第二视图只在含 `\u0000` 且与第一视图不同时追加。
- **主控独立复核**:
  - 套件 (相对路径, 私有 HOME): scan `87 / 122`, guard `666 / 780`, stderr 空, `got 127` 为 0; 失败集合比对脚本 (`scratchpad/failset_diff.py`, 先在 TASK-002 返修前后两次已知结果上自检: 转绿 62 / 新增 0, 与已知一致) 给出: 转绿 scan 9 条 + guard 1 条, 恰为 W1 SC-1a/1b/1c/1d/1f、W1 SC-35 的 AWS 行与 35d、W6 SC-14a/14b、W7 SC-15a; 新增失败 0。
  - 探针子集 `WPA_ONLY=SC-1,SC-2,SC-3,SC-14,SC-15,SC-35`: 29 行, SC-1 7/7、SC-2 6/6、SC-3 2/2、SC-14 2/2、SC-15 7/7、SC-35 3/5 (35a / 35b `no`, 依赖 W2, 按修订归 TASK-004), stderr 空, 218 s。
- 执笔自报的另外几项 (未由主控复跑): 不设 HOME 的运行不改真实日志; bash 3.2 下 `bash -n` 与 scan 套件结果相同; 改动行零 bash 4+ 构造; 新增行在三个 hook 下零命中 (带正控); W7 拆分前后 49 条输入逐字节相同。
- 执笔自报的偏离: 一次误跑 `find /` 与探针并发约 2 分钟 (已杀); TASK-004 派单已明令禁止。
- 请裁 (执笔): `hooks.json` 顶层 `description` 是否随之更新 —— 主控裁定归 TASK-009 (Spec 原文「可随之更新」, 属文档同步)。
- 提交: aria `7567fe5` (已推 origin, `ls-remote` 一致)。

## TASK-004 (W2 键形模式 + W3 白名单 + W4 值指纹 + W5 告警文案) — 2026-10-08

- 派单 `dispatch/impl-task004.md` (13:21Z); 执笔报告 13:44Z。只改 `secret-scan.sh` (+152 / −7), 交付字节 sha256[:16] `4e946eef0648e4d3` (主控提交前核对一致)。
- 主控审读 diff:
  - 6 个新 tag 位置与顺序合 W2;
  - 分类路径零 fork, 字符类枚举不用范围;
  - 前 200 个 span 分类, 超出部分 fail-closed 计数;
  - 计数替换失败时回滚指纹表;
  - 告警文案只加 tag 与 tool 名。
  - 曾担心「被分类器排除的 span 仍被哨兵消费」会吃掉排在后面的既有 tag 的检出。核对 pattern 顺序后排除: 既有 tag 中只有 `bcrypt-hash` 排在新 tag 之后, 其余 (含 `jwt` 第 1 位) 都先消费; crypt 哈希一情形由 SC-7 7h / 7i / 7j 钉住。
- **主控独立复核**:
  - 套件 (相对路径): scan `122 / 122`, 相对 TASK-003 转绿 35 条 (W1+W2 1、W2 19、W3 7、W4 6、W5 2); guard `666 / 780`, 失败集合不变; 新增失败 0; `got 127` 为 0。
  - 探针子集 (SC-4 … SC-13、SC-15、SC-33、SC-34、SC-35): 165 行, 164 行 `yes`; 唯一 `no` 是 SC-34 34c (测 secret-guard 的 W9 扩展命中路径, `baseline_probe.py:2622`), 按裁定归 TASK-007; stderr 空, 199 s。
- 执笔自报 (未由主控复跑):
  - bash 3.2 下结果相同; 改动行零 bash 4+ 构造。
  - Rule #7 日志核查: 5 个运行时生成的值在日志、stdout、stderr 中出现 0 次。
  - 时档 `i` / `i3` 十档全 PASS: i1 / i2 为 1.18 / 1.20 (上界 2.0); i3-a … e 为 1.17 – 1.73 (上界 2.5); i3-f / g / h 为 3.33 / 3.32 / 3.41 (上界 5.0, 余量偏小, TASK-010 验收时留意)。
- 主控裁定 (待 owner 复议): TASK-004 的 SC-34 只验 34a / 34b, 34c 归 TASK-007; 已改 `detailed-tasks.yaml`。
- 提交: aria `2e2a2a8` (已推 origin, `ls-remote` 一致)。

## TASK-005 (W8 服务端配置文件 + W11 进程表列举) — 2026-10-08

- 派单 `dispatch/impl-task005.md` (13:57Z); 执笔报告 14:26Z。交付字节 sha256[:16]: `secret-guard.sh` `9824e48ebcf09d30`、`secret-guard.test.sh` `0cadad2f2a2b06ea` (主控提交前核对一致)。
- 主控审读 diff:
  - 共享名字块位于 `_sg_compute_credit` 与 source 闸门之上;
  - W11 三条规则是字面行;
  - `/proc` 两行与 `python3` / `node` 两行原位改写, 基线部分原样保留, 只追加备选;
  - tight 只并入 ps 家族 (`env` / `printenv` 保持基线 credit);
  - Read/Edit 正则只追加 `app.ini` 名字组;
  - `risky_patterns` 145 → 149。
- **主控独立复核**:
  - 套件 (相对路径): guard `735 / 783`, 相对 TASK-004 转绿 66 条 (W11 45、W8 20、W13 1), 新增失败 0; scan `122 / 122`; `got 127` 为 0。
  - 测试内 SC-8 五档 (load `2.26 2.23 2.74`): (a) 7.1 / (b) 14.1 / (c) 8.5 / (d) 12.2 / (e) 47.6 ms, 天花板 100 ms。
  - 探针子集 `WPA_ONLY=SC-16,SC-17,SC-18,SC-22,SC-31`: 118 / 118 `yes` (SC-16 18、SC-17 4、SC-18 11、SC-22 80、SC-31 5; 31b `census=64 test-hardcoded=64`), stderr 空, 265 s。
- 执笔请裁两条 (主控裁定, 待 owner 复议):
  1. family 探针本身是 `bash_case` (先例 aria-plugin#153 / Aria#179 都是可执行用例), 净增 3 条, 头注释同步为 789 / 783 —— **采纳**; 派单里「不加新用例」指不加功能用例, 只写注释行的探针是纸面修复。
  2. W14 原文点名的第三个新族 (「`<` 重定向行」) 与 census 实测 (W8 读取器行 `GRP:()`) 不符, 数量一致 —— 归 TASK-009 文档同步时订正。
- **主控裁定 (待 owner 复议)**:
  - **从 TASK-006 起换第二位实现执笔**: 第一位的上下文累积到约 48 万, 每次调用重读; 新实例从干净上下文开始, 交接说明由主控写 (`dispatch/impl-handover.md`), 不额外消耗旧实例。
  - **TASK-009 改派 `aria:knowledge-manager`**: Spec Tasks 1.9 写明「勘正执笔人 ≠ 实现执笔人」, 原 `detailed-tasks.yaml` 的「与实现同一执笔实例」与 Spec 冲突 (上一会话精简计划时引入)。

## TASK-006 (W12 两处误拦) — 2026-10-08 / 09

- 派单 `dispatch/impl-task006.md` + 交接说明 `dispatch/impl-handover.md` (10-08 14:43Z); 由**第二位执笔**完成, 报告于 10-09 00:15Z。
- **停顿**: 第二位执笔的 transcript 在 10-08 14:52:57Z 与 23:54:36Z 之间没有任何记录 (32,499 s), 主控这边同期也无活动。原因无法从记录确认 (可能是额度限流, 也可能是会话或主机挂起)。实际工作时间约 30 分钟。
- 交付字节 sha256[:16]: `secret-guard.sh` `40f61ef56563f5f9` (主控提交前核对一致)。
- 主控审读 diff:
  - jq 锚定 credit: 用既有 `_sg_line_match`, 不并入宽松词表;
  - 单键读取归一化: 只改匹配用副本 `$subj`, credit 与 BLOCKED 仍用原文; 整表形态不在替换表内, 照拦;
  - 前缀 + 按长度切, 无 `${s//p/r}`、无 eval。
- **主控独立复核**:
  - 套件 (相对路径): guard `739 / 783`, 相对 TASK-005 转绿 4 条 (W12 SC-23a / 23b / 23j、SC-24a–24e), 新增失败 0; scan `122 / 122`; `got 127` 为 0。
  - 测试内 SC-8 五档 (load `2.04 1.69 1.56`): (a) 7.4 / (b) 14.4 / (c) 8.9 / (d) 13.0 / (e) 48.3 ms, 天花板 100 ms。
  - 探针子集 `WPA_ONLY=SC-23,SC-24,SC-31`: 24 / 24 `yes` (SC-23 10、SC-24 9、SC-31 5), stderr 空, 226 s。
- 提交: aria `ef656df` (已推 origin, `ls-remote` 一致)。
- **执笔实测的性能观察 (待 owner 定夺, 交 TASK-010 / TASK-014)**:
  1. W12 的归一化循环代价约为「出现次数 × 命令长度」(10.8 KB / 500 次出现时多 0.65 s); W14 的时档表没有 W12 一档。
  2. **基线 hook 自身**对长命令超线性: 等长良性命令 2.1 / 4.2 / 10.8 KB 分别 0.26 / 0.66 / 3.32 s, **26 KB 约 17.9 s, 超过 `hooks.json` 的 5 s 超时**。超时后 harness 是否放行未验证; 若放行, 就是一个本 Spec 之前就存在的绕过面 (足够长的命令让 L1 来不及判定)。W14 的「兜底: 目标单次进程墙钟 < 20 s」只防挂死, 不覆盖这一点。开 issue 需 owner 授权。

## TASK-007 (W10 变量展开 + W9 项目级扩展入口) — 2026-10-09

- 派单 `dispatch/impl-task007.md` (00:27Z); 第二位执笔报告 01:07Z。交付字节 sha256[:16]: `secret-guard.sh` `067dd6f621f23300` (主控提交前核对一致)。
- 主控审读 (只看安全关键部分):
  - 11 个新函数 (第 536–730 行) 全在 source 闸门 (第 748 行) 之上, `_sg_judge_one` / `_sg_per_segment_eval` / `_sg_redact_echo` 仍在闸门之下 (INV-4);
  - 源码无被执行的 `eval`; `${s//p/r}` 只出现在注释里 (基线 6 处、现在 8 处, 多出的两处都是注释);
  - 扩展条目只经 `grep -F` 作字面串, 不拼正则不执行; `LC_ALL=C` 下按字节计长度与偏移; 超限或含 NUL 的文件整体忽略; 仓库内容只能增加拦截, 不能放宽;
  - 求值顺序: 内建 → W10 → 扩展, 内建拦下即返回; 扩展只在 `$( )` 里跑, 只认字面 `BLOCK`; 整体仍在 fail-closed 子 shell 内。
- **主控独立复核**:
  - 套件 (相对路径, 带 git 历史): **guard `783 / 783`、scan `122 / 122`, 全绿**; 相对 TASK-006 转绿 44 条 (W9 30、W10 12、W13 2), 新增失败 0; SKIP 只有 zsh 一条 (SC-9a 对拍照常执行)。
  - 测试内 SC-8 五档 (load `2.33 2.98 3.09`): (a) 13.6 / (b) 20.7 / (c) 15.8 / (d) 20.7 / (e) 57.1 ms, 天花板 100 ms (W9 扩展的那次命令替换每档约 +6.5 ms 固定开销)。
  - 探针子集 `WPA_ONLY=SC-19,SC-20,SC-21,SC-25,SC-27,SC-28,SC-30,SC-31,SC-34` (527 s, stderr 空): SC-19 40/40、SC-20 17/17、SC-21 23/23、SC-25 9/9、SC-31 5/5、SC-34 3/3 (含 34c)、SC-30 30b `yes` (30a 按设计 `n/a`); **SC-27 2/4 (27a / 27c: SOT 计数)、SC-28 0/15 (全部 doc-sync 勘正行)** —— 后两者是 TASK-009 的范围。
- 执笔自报 (未由主控复跑): bash 3.2 下结果一致; 11 个新函数逐个注入未绑定变量 92 项全部符合; 时档 f / f0 / fhit / g / gmax / h 共 9 档全部低于上界、活性断言成立 (f 1.56 / 1.54, f0 1.22 / 1.13, fhit 2.00 / 2.03, g-a 1.41, gmax 2.01, h2 1.21)。
- 提交: aria `db4f8b8` (已推 origin, `ls-remote` 一致)。

## TASK-008 (W14 元耦合同步) — 2026-10-09 结项 (主控核对)

- **主控裁定 (待 owner 复议)**: 不再派执笔。W14 的元耦合已按 TASK-005 起的裁定在各任务里随改随同步 —— census 64 与 3 条 family 探针、头注释计数 789 / 783 与 122、闸门之上的函数 (探针 30b)、未绑定变量注入自测 (TASK-007 执笔 92 项)。
- 结项证据 (即 TASK-007 的主控复核): 带 af87cae 历史的真 checkout 上两个套件全绿 (含套件内 SC-13 / SC-16 / SC-17 / SC-19 / SC-20 自检), 测试内 SC-8 五档为真测; 探针 30b `yes`、SC-31 5 / 5。
- 原先挂在本任务下的 SC-27 (SOT 计数) 与 SC-28 (陈旧表述勘正) 移入 TASK-009: 它们的交付物 (`secret-hygiene.md`、README、hook 头注释、`aria/VERSION`) 本就在 TASK-009, 且 Spec Tasks 1.9 要求「勘正执笔人 ≠ 实现执笔人」。原计划 SC-28 同时挂在两条任务下、TASK-008 标题写着同步「SOT 三处」却不交付 SOT 文件 —— 精简计划时引入的接缝缺陷, 至此消除。

## TASK-009 (文档同步与勘正) — 2026-10-09

- 派单 `dispatch/impl-task009.md` (01:27Z), 执笔为新派的 aria:knowledge-manager (Spec Tasks 1.9「勘正执笔人 ≠ 实现执笔人」); 报告 02:08Z。
- 主控派单的疏漏: 派单写「没过的只有 27a / 27c 与 SC-28」, 漏了 SC-26 (主控此前那次探针复跑没带 SC-26)。执笔起点实测 SC-26 2/11, 照样处理到 10/11。
- **主控独立复核**:
  - 范围: aria 6 个文件 (两份 README、VERSION、hooks.json、两个 hook), standards 只有 `secret-hygiene.md`, 主仓多 `changelog-draft.md`, 全在交付物内。
  - 两个 hook 去掉整行注释后与 `db4f8b8` 逐字节相同 (只改注释); 新增行无 `(?:`; `hooks.json` 的 `hooks` 对象与原来相等, 只改 `description`。
  - 8 个改动文件经当前 `secret-scan.sh` 扫描零命中, 拼上运行时生成的 AWS key 形状后都告警 (正控有效)。
  - 探针子集 `WPA_ONLY=SC-25,SC-26,SC-27,SC-28` (243 s, stderr 空): SC-25 9/9、SC-26 10/11、SC-27 4/4、SC-28 15/15; 唯一 `no` 是 26g。
- **主控补正两处** (执笔按派单「只加 SC 点名的句子」未改, 属 Rule #3 文档与代码同步的事实遗漏; 几个词, 主控直接改, TASK-014 一并复核):
  1. 两份 README 第 33 行注册表, secret-scan 一行的事件改为 `PostToolUse` + `PostToolUseFailure` (同一行的 cannot redact 原句不动);
  2. SOT §5 引言补「secret-scan.sh 另注册 PostToolUseFailure, 扫描失败工具调用的错误文本」(标题不动, 免得改锚点)。
  - 补正后重跑 `WPA_ONLY=SC-25,SC-26,SC-28`: 结果不变 (9/9、10/11、15/15); 三个文件扫描零命中 (带正控)。
- **26g 的处理 (主控裁定, 待 owner 复议)**: 26g 要求 `aria/CHANGELOG.md` 最上一节含 14 个标记词, CHANGELOG 是发版文件。执笔已把草稿拼进 CHANGELOG 副本、用 26g 判据实测 `yes`。移到 TASK-010: 验收前先把草稿作为最上一节落入, 版本号用 `<vNEXT>` 占位, TASK-011 取号后替换。
- 执笔请裁 / 备注 (记录, 待 owner 或 TASK-014):
  - 28f 的写法: Write 响应形状写成 `"filePath": …, "content": …` 一行 (真实键序), 以免契约行以顶层 `"content":` 起头。主控判断: 内容如实, 不算迁就检查器 —— 该判据针对的是旧的错误 Read 形状, 对 Write 形状过宽; 交 TASK-014 复核。
  - 「cannot redact」表述按 Spec 保留, 等「待 owner 复议」第 1 条统一订正。
  - SOT 版本历史行日期写 2026-10-09, 发版日不同时 TASK-011 顺手改。
- 提交: aria `69af7cd`、standards `be842ce` (均已推 origin, `ls-remote` 一致; standards 特性分支首次推送, 未推 GitHub)。

### 运行要点 (供后续任务)

- 真 bash 3.2 已在持久位置 (见上), 不必再按 Phase A 进度锚第 64 行的说法重建。
- 探针全量 (带 bash 3.2) 在 2 核限流下约 17–24 分钟, 按资源纪律每席最多两次全量; 实现期的单项验证用 `WPA_ONLY=SC-…` 子集。
- 时档类测量 (W14 的 (f) / (f0) / (f-hit) / (g) / (h) / (i) / (i3) 与测试内 SC-8) 只在一分钟负载低于 2 时串行跑, 判据只看比值。

## TASK-014 (非作者对抗审查, owner 所说的单轮审查) — 2026-10-11

- 派单 `dispatch/review-task014.md` (09:5xZ), 席位是新派的 aria:qa-engineer 实例; 工作 10:08Z – 14:28Z。
- **报告落地**: harness 拒绝子代理写报告文件 (Write 返回 "Subagents should return findings as text, not write report files"), 全文在最终消息里。主控用脚本从 transcript 抽出 (不经对话转抄), 去掉开头的摘要段, 存为 `.aria/audit-reports/post_implementation-R1-2026-10-11T142603-595Z-secret-net-l3-and-bypass-paths-qa-engineer.md` (sha256[:16] `15ab8e5d95d1b2a3`)。当前 `secret-scan.sh` 扫描零命中, 拼一行运行时生成的 AWS key 形状后告警 (正控有效)。
- **结论: PASS_WITH_WARNINGS, critical 0 / major 8 / minor 5。** 667 个独立构造的坏实现; `proposal.md:383` 点名的各类每类至少一个让对应行转红 (TASK-014 第一条 verification 成立)。120 个全绿, 其中 70 个是真缺口, 归并为 8 条 major:
  - M1: 30b 只能发现 `_sg_core_eval`、`_sg_vx_pass` 落在 source 闸门之下, 另 9 个辅助函数 / 初始化发现不了 (用例名声称的比它验证的多)。
  - M2: tight 拷贝的命令位置字符、关键字、launcher 时长后缀漂移 (14 个), 以及 `ps -O`、末位 `-u` 的「操作数只认首个」(2 个), 都不转红。
  - M3: `/proc` 加宽组删掉任一个基线读取器 (12 个) 不转红。
  - M4: 上下界差一约 16 个不转红 (200-span 帽、kv 键 `{0,64}`、cli 旗标 `{0,40}`、路径形斜杠数、W10 `for` 帽与 `${}` 替换帽、PEM 指纹循环)。
  - M5: 「不执行」不变量两处覆盖洞: 命中扩展条目之后对命令文本求值 (19ab 只测未命中); `_value_of` 的 URL 分支求值 (7n 不含 URL 类)。
  - M6: W10 第二遍判定串长无上界, 5.45 KB 命令 1.15 → 5.48 s, 越过 5 s 超时; 是唯一要改 hook 代码的一条。
  - M7: L3 逐 tag 分类范围 (`json-env-secret-key`、`cf-access-client-secret`)、jq `paths` / `leaf_paths`、W8 左边界 `_ . -` 缺项不转红 (都是误报方向)。
  - M8: Read/Edit 面扩展条目的「字面子串」性没有任何行。
  - minor: m1 28f 判据对写法敏感 (内容如实, 不是迁就检查器); m2 顺序行按函数名插桩; m3 W10 声明前缀组多余 (Spec 已注); m4 W12 归一化循环可改成一次 `sed`; m5 `app.ini.example` 与 `git diff -- …/app.ini` 被拦。
  - 派单点名的三处: 28f 如实 (即 m1); W12 循环比值 1.03 – 1.19, 只在基线自身 5 s 悬崖下方约 3% 宽的带内越线, 不升级; `(( ${#_SGV_N[@]} ))` 在正式代码里不会遇到未赋值, 人为去掉初始化时 fail-closed (3.2.57 与 5.2.15 一致), 无 finding。
  - 风险 (审查席未能验证): `hooks.json` 新增的 `PostToolUseFailure` 键, 在不认该事件的旧版 Claude Code 上可能让整份 hooks 不加载 (含 secret-guard)。发版前须核 aria-runner 容器里的 Claude Code 版本。
- **主控独立复核** (参考树 = 自建的 `git archive 69af7cd`; 坏实现由主控自己构造, 每处改动断言恰好生效一次):
  - M6: 16 个 300 B 赋值、每个变量引用 8 次 (命令 5459 B), 负载 1.55: 基线 1.24 s, 被审 5.30 s (4.28×), 越过 5 s; 与报告的 1.15 → 5.48 s 一致。
  - M2 (tight 拷贝去掉 `;`)、M3 (加宽组去掉 `tail`)、M5 (命中后对替换副本 eval)、M8 (Read 面改成 `grep -E`): 直接调用 hook 都复现了行为差异 (M5 的金丝雀文件被建出); 对应探针整组在坏实现上与参考树逐行相同 (SC-22 80/80, SC-19 40/40, SC-20 17/17), 确实不转红。
  - M1: 静态核对成立。套件 30b (`secret-guard.test.sh:2757-2764`) 只断言退出码; `_sg_ext_*` 只在 `$( … )` 里调用且丢弃 stderr; `_sg_emit_blocked` 的返回值不参与判定。
  - M4、M7 与 M5 的 7n 一侧没有单独复现; 修补执笔须先在审查席的坏实现上逐条转红, 等于逐条复现。
  - 审查席收尾后核进程树: 没有残留 (只有会话自身的 MCP 与 pyright)。
- **成本**: 见成本账。审查席上下文从 5.2 万累积到 91.5 万 (未压缩)。缓存写的 92% (约 1006 万) 来自 13 次整份重写: 每次都是一次工具调用 (前台长命令或等后台) 超过 5 分钟 (间隔 359 – 612 s), 子代理的缓存 TTL 只有 5 分钟, 下一次调用把 61.5 – 86.6 万的上下文整份重写一遍。后续派单: 单次工具调用不超过 4 分钟 (长任务拆段), 修补按文件域拆给几个新实例。
- **主控裁定 (待 owner 复议)**:
  1. 修补落在两个套件里 (随 hook 一起发布, 防的正是报告里「以后有人改漏」的那类漂移), 不加探针行。探针是本 Spec 一次性的验收物; 加行还得在基线上整份重跑 (约 24 分钟)、重新生成 `baseline-evidence.md` 并改 SC 正文。TASK-014 第二条写的是「探针行或套件用例」, 两者都可以。
  2. M6 改 hook: W10 第二遍设串长预算, 并改成线性替换。`timing.py` 只增加一档 (g-c), 已有各档不动; 实测后由主控以修订记录的方式订正 `proposal.md` 的 Impact 与 W14 时档表 (只增不改原句)。
  3. 复核席换新实例。审查席上下文 91.5 万、缓存早已过期, 唤醒一次至少整份重写, 再干活就会触发压缩; 新实例凭 `$W` 下的坏实现与 `out/res_*.jsonl` 只复核修补处。TASK-014 原文「审查者只复核修补处」指的是角色, 不是同一实例。
  4. 5 条 minor 本轮不修, 记作待办 (m1 / m2 涉及探针行, m5 是行为取舍)。
  5. SOT 里的测试计数 (三处 789 / 783、一处 122, 以及 1.2.0 版本历史行) 等修补全部落地后由主控一次同步, 免得并行的执笔同改一个文件。
- **修补安排**: 执笔 A (新 backend-architect 实例) 先修 M6 (改 hook; 测时档时主机上只跑它一个)。之后执笔 B (guard + scan 两个套件的其余 7 条 major 补用例; 不按文件拆, 免接缝缺陷) 串行接上。最后新派一个 qa-engineer 只复核修补处。

### M6 复核加固 + owner 决定 (2026-10-13)

- **M6 比报告更尖**: 主控复核时额外确认, 单层链式赋值在 W10 上限内会让值**成倍放大** —— 一条一百多字节的命令可把第二遍拖到十几秒 (depth-6 链实测约 16.5 s, 基线约 0.08 s)。含义: M6 的修法必须是「对**展开后串长**设预算」, 只卡赋值个数/引用次数挡不住这条。派单 `dispatch/fix-task014-m6.md` 已据此写明 (串长预算 + 值长帽 + 线性替换)。
- **超时 fail-open (Spec:410) = owner 决定**: 钩子被拖过 5 s 后按现状放行; 这不是相对基线的回退 (基线无 W10/W9), 是既有缺口被新能力拉近。owner 2026-10-13 裁定:**维持 WP-A 范围** (M6 只做串长预算, 不碰超时策略), **另开 issue 提优先级**。已开 **10CG/aria-plugin#216** ([安全][secret-guard] hook 5 s 超时后 fail-open, Refs #154/#203/#221)。fail-closed 化 (误拦长命令的代价) 留 #216 由 owner 定优先级, 不入本次。
- **进展**: 执笔 A (M6) 已于 2026-10-13 派出, 后台运行中。brief 要求三态 CPU 比值表 + `timing.py` 新 g-c 档 (修补前参考树 FAIL / 修补后 PASS) + 套件转红。
