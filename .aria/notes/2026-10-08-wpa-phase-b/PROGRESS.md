# WP-A Phase B 进度 (会话中途记录, 供中断后续接)

> 正式的会话交接按 Rule #9 写在 `docs/handoff/`; 本文件只是 Phase B 的进度锚 (Phase A 的进度锚见 `../2026-09-30-wpa-phase-a/PROGRESS.md`)。任务定义见 `openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml`, 每完成一条任务向 owner 报一行成本 (决策单 `.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md`)。

## 成本账 (每条任务一行)

| 任务 | 墙钟 (UTC) | 子代理 token | 产出 |
|---|---|---|---|
| TASK-001 | 09:43Z – 10:15Z 约 32 分钟 (探针复跑占 24 分钟) | 0 (主控独做; 主控上下文 10:14Z 为 23.6 万 / 100 万) | B.0 认领、两个特性分支、行号核验、SC-30 基线、环境核验、探针复跑逐字节一致; 代码 0 行 (本任务不改代码) |
| TASK-002 | 10:18Z – 12:19Z 约 2 小时 (执笔首轮约 72 分钟 + 返修约 35 分钟 + 主控复核) | 执笔 169 次调用: 缓存读 100,173,589 / 缓存写 1,631,422 / 输出 42,965 (上下文峰值 86.5 万; 原记的 867,303 是上下文大小, 见下方口径更正); 主控上下文 23.6 万 → 33.5 万 | 测试 +1471 / −1 行 (新增 260 条用例), aria `ec99e6c` (本地); 主控复核抓到 1 个缺陷 (相对路径调用退 127), 已由执笔返修 |
| TASK-003 | 12:21Z – 13:20Z 约 1 小时 (执笔约 46 分钟 + 主控复核) | 执笔 115 次调用: 缓存读 38,200,311 / 缓存写 1,120,533 / 输出 9,407 (12:39Z 上下文压缩, 段末上下文约 21 万); 主控上下文 33.5 万 → 38.4 万 | aria `7567fe5`: secret-scan.sh +31 / −6 (W1)、hooks.json +12、两个套件 W6 / W7; 转绿 10 条, 新增失败 0 |
| TASK-004 | 13:21Z – 13:54Z 约 33 分钟 (执笔约 23 分钟 + 主控复核) | 执笔 47 次调用: 缓存读 14,444,557 / 缓存写 353,399 / 输出 12,574 (段末上下文约 35 万); 主控上下文 38.4 万 → 42.7 万 | aria `2e2a2a8`: secret-scan.sh +152 / −7 (W2–W5); scan 套件 122 / 122; 「上下文卫生」要求后真实用量约为 TASK-002 首轮的四分之一 |
| TASK-005 | 13:57Z – 14:4xZ 约 45 分钟 (执笔约 30 分钟 + 主控复核) | 执笔 52 次调用: 缓存读 22,149,851 / 缓存写 477,816 / 输出 2,527 (段末上下文约 48 万, 又在累积) | secret-guard.sh +49 / −6 (W8 + W11)、测试 +19 / −4 (census 61 → 64 与 3 条 family 探针); guard 转绿 66 条, 新增失败 0 |
| TASK-006 | (待派, 换第二位执笔) | — | 派单 `dispatch/impl-task006.md`; 交接说明 `dispatch/impl-handover.md` |

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

### 运行要点 (供后续任务)

- 真 bash 3.2 已在持久位置 (见上), 不必再按 Phase A 进度锚第 64 行的说法重建。
- 探针全量 (带 bash 3.2) 在 2 核限流下约 17–24 分钟, 按资源纪律每席最多两次全量; 实现期的单项验证用 `WPA_ONLY=SC-…` 子集。
- 时档类测量 (W14 的 (f) / (f0) / (f-hit) / (g) / (h) / (i) / (i3) 与测试内 SC-8) 只在一分钟负载低于 2 时串行跑, 判据只看比值。
