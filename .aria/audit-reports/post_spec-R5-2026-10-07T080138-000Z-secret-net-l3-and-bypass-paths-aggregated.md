---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T08:01:38.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/7M/14m
counts_dedup: 0C/6M/11m
sibling_probe: no_sibling_found
---

# post_spec R5 聚合 — secret-net-l3-and-bypass-paths — 未收敛

> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。

## 判定

| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |
|---|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/2M/3m | 0C/2M/3m | REVISE | `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-tech-lead.md` |
| backend-architect | PASS_WITH_WARNINGS | 0C/2M/2m | 0C/2M/2m | REVISE | `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-backend-architect.md` |
| qa-engineer | PASS_WITH_WARNINGS | 0C/2M/3m | 0C/2M/3m | REVISE | `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-qa-engineer.md` |
| code-reviewer | PASS_WITH_WARNINGS | 0C/1M/3m | 0C/1M/3m | REVISE | `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-code-reviewer.md` |
| knowledge-manager | PASS | 0C/0M/3m | 0C/0M/3m | PASS | `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-knowledge-manager.md` |

## 全部 finding (按席位原编号, 不转述)

| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |
|---|---|---|---|---|---|---|---|---|
| tech-lead | M1 | `66d6eb81` | `66d6eb81` | major | issue | architecture | proposal.md SC-3 | L3 对失败的工具调用整体失明: Claude Code 2.1.285 的 PostToolUse 只在工具成功时触发, Bash 非零退出 (默认语义) 即抛 ShellError, 输出装在错误文本里送给模型, 触发的是 PostToolUseFailure (字段 error, 无 tool_response); secret-scan 未注册该事件、提取链也不读 error。Spec 把它误述为「字符串形 tool_response 会不会到达 PostToolUse 未证实」并钉成 SC-3 3b; W8 / W10 / W11 的「交给 L3 兜底」(含 systemctl status, 对未运行或失败单元退出 3) 对非零退出命令不成立; 该缺口未进已知限制、Out of scope、7.x、Impact 与关单披露。 |
| tech-lead | M2 | `755aab21` | `755aab21` | major | issue | implementation | proposal.md What.W2 | W2 的取值线性规则只禁前导 * 的 # / ##, 不足以保证线性: bash 的 # / ## / % / %% 删除在不命中时每个位置 O(长度)。参考原型的 kv 去引号 ${V#["']} 在不带引号的长值上平方级, 约 300 KB 单值在 4 s CPU 上限下被杀 (KEY = v / export / YAML 三形), 同输出里的基线检出随之丢失; 只改这一句为首字符判断即 2.2 s 告警。34b 与 (i3) 都没有该形态, 验收恒绿。R4 簇 W 部分关闭。 |
| tech-lead | m1 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | 包裹 × printenv 备选把带参数的 printenv (docker exec / docker compose exec / ssh / nomad alloc exec / pct exec / sh -c / bash -c / watch 下的单变量读取) 由放行变拦, 而 W11 写「只拦裸」、Impact 只按文本提及申报并称日常核对不变、22bj 只钉 env 词: 两种实现都全绿。R4 6ff1d962 的 printenv 一侧。 |
| tech-lead | m2 | `0033f2f4` | `0033f2f4` | minor | issue | documentation | proposal.md 待 owner 复议 | 待复议 23 (及 W11 :196、22br 描述) 称 25898 把「读一个变量」列为正当核对; 25898 原文只列「读长度、读 env 变量名」, 锚定 grep '^X=' 会打印该变量的值, 引文误导 owner 对待复议 23 的复议。 |
| tech-lead | m3 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | W9 文档落点 (§5.6 / README, SC-26 26c / 26e) 未要求写保护边界: 列入路径只获得内建 app.ini 行的覆盖, .env 族会拦的 source / . / dd / 重定向读 / tee < / mapfile < / xargs cat / find -exec / cp /dev/stdout / perl -ne 对列入条目都放行 (实跑 10/10), Grep / Write / 第 65 处之后同样不受保护; 采用方会以为得到 .env 级保护。(与 R4 同四元组的 684e9a24 不是同一问题) |
| backend-architect | M1 | `6bd285b1` | `6bd285b1` | major | issue | testing | proposal.md SC-30 | 既有测试内 SC-8 五档延迟闸 (owner 2026-08-24 裁定, 不改阈值 / 口径 / 档位) 用 awk 按函数名只抽 `_sg_judge_one` 与 `_sg_per_segment_eval`, 而 W9 / W10 / W12 要求的重构让前者调用定义在 source 闸门之下的 `_sg_core_eval`; Spec 未规定这些辅助函数的位置、也无活性断言, 写手原型下该闸对 `_sg_per_segment_eval` 计到的是 rc=127 的瞬时返回 (0.7-0.9 ms/call 对基线 6.8-42 ms), 五档恒绿, SC-30 的「SC-8 全绿」失去判别力。 |
| backend-architect | M2 | `df25d271` | `df25d271` | major | issue | testing | proposal.md SC-19 | W9 条目文件的输入面有三个常见条件没有任何 SC 行 (清单末行无换行、项目根路径含空格、`CLAUDE_PROJECT_DIR` 置空而 stdin `cwd` 有值), 两个自然的错误实现过得了 SC-19 / SC-20 全部 54 行, 却让扩展静默丢条目或整体失效。 |
| backend-architect | m1 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | W9 已知限制与 §5.6 / README 的必写内容 (SC-26 26c 的关键词清单) 没有警告采用方: 完整路径条目对 `..` 回绕、`//`、`/./` 与 `cd` 后相对名的写法失效, 只有最短特征子串能覆盖。 |
| backend-architect | m2 | `cfb2fb14` | `cfb2fb14` | minor | issue | testing | proposal.md Tasks | Tasks 1.12 拒绝加 NUL 腿的理由 (返修报告 §6.8(1)「加了腿也只能记『未验证』」) 不成立: 惰性的 NUL 记录腿对「NUL 以 `\u0000` 到达 hook」这一 W1 视图 N 的唯一前提有判别力, 而该前提至今无端到端样本。 |
| qa-engineer | M1 | `12a776ac` | `12a776ac` | major | issue | testing | proposal.md Success Criteria | W11 描述的是语义而 SC-22 只钉规范拼写: 命令位置锚点的 `&` `{` 反引号、pgrep/pstree 的 `-a` 位置、ps -o 列表关键字位置、ps -F、docker ps -a --no-trunc、launcher 时长后缀六类自然窄化实现在全部相关探针行 0 行红, 却放行 pgrep -fa 等进程列举命令。 |
| qa-engineer | M2 | `6bd285b1` | `6bd285b1` | major | issue | testing | proposal.md SC-30 | W9 把 _sg_per_segment_eval 的函数体提出为 _sg_core_eval (闸门之下) 后, 既有测试内 SC-8 五档延迟闸只抽到壳、每次调用 rc=127, 真 git checkout 里新侧耗时降 97% 五档全绿, SC-30 这一腿恒绿且 W14 耦合清单与探针都没有这一项。 |
| qa-engineer | m1 | `c7bff9bd` | `c7bff9bd` | minor | issue | testing | proposal.md SC-12 | W4 规定指纹只对被计数的 span 取, SC-12 没有行钉住被分类器排除的 span 不记指纹; 先记指纹再分类的实现在 99 行相关探针上全绿, 并会让占位符挤掉真凭据的指纹。 |
| qa-engineer | m2 | `0033f2f4` | `0033f2f4` | minor | issue | documentation | proposal.md 待 owner 复议 | W2 与 W8 的已知限制写 FORGEJO__/GITEA__ 环境变量覆写并入建议开单 7.8/7.9, 但 7.8/7.9 正文没有这一项, 引用悬空。 |
| qa-engineer | m3 | `f410df76` | `f410df76` | minor | issue | documentation | proposal.md Impact | Impact 覆盖关系写 10CG/aria-plugin#154 有两处有意偏离, 同节关单口径与 Tasks 1.13 都是三处, 数字不一致可能导致关单评论漏披露 (c)。 |
| code-reviewer | M1 | `ac42f607` | `ac42f607` | major | issue | implementation | proposal.md What.W11 | W11 (:196) 与 SC-22 (:291) 称「基线对 docker\|kubectl\|podman\|lxc exec … env 已拦」, 并据此把这四个包裹的转储备选判为等价变异, 与 secret-guard.sh:858 / :862-863 / :938 / :940 的实际覆盖面不符。22bo 对这四个包裹只用基线已拦的写法 (基线 10/22 恒绿), 执笔自己的 remote_env_split:{lxc,kubectl,docker} 坏实现过全部 74 行 SC-22 与 8 行 SC-25, 却放行目标原型会拦的整环境转储 (lxc exec c env、kubectl exec pod 'env'、x=$(kubectl exec pod env)、docker exec c "env"、podman exec c "env")。另「只拦裸 printenv」与原型对包裹下 printenv NAME 的拦截相反, 且无行钉住; Impact 对这两类新拦截都未申报。 |
| code-reviewer | m1 | `5d12116d` | `5d12116d` | minor | issue | documentation | proposal.md Tasks | Tasks 1.7 (:376) 写 _sg_ext_path_pass 经内建的 _sg_core_eval 判定, 与 W9 (:165) 对 Read/Edit 面的定义 (小写化路径做字面子串比对) 相矛盾, 是 v5 引入的接缝; 照 Tasks 走的实现会让 Read/Edit 判定受 [^\|]* 与引号结构影响, SC-19 的 Read 行抓不到。 |
| code-reviewer | m2 | `ed638210` | `ed638210` | minor | issue | testing | proposal.md SC-9 | 9z 把凭据形值挂在紧贴词字符的大写键上 (abc_API_TOKEN=<24 alnum>) 的静默钉成 allow-guard (误报守卫), 实为 kv 左边界造成的漏报类; W2 已知限制与待复议 31 只列了 cli 的同类情形 (10o, known-limit)。本席实测 prod_API_TOKEN=… 与 export my_DB_PASSWORD = '…' 在目标上静默, 而全大写的对照会检出。 |
| code-reviewer | m3 | `eb6c5b5e` | `eb6c5b5e` | minor | issue | testing | proposal.md SC-25 | W9 未规定扩展拦截时 Matched pattern / Triggering segment 写什么, SC-25 25f 的归一化把这两行抹掉。让内建判定直接输出替换副本文案的变体回显 Triggering segment: cat /etc/gitea/app.ini (用户从未用过的路径), 仍过 SC-19 37/37、SC-20 17/17、SC-25 8/8; 同类的 W12 由 25h 钉住, W9 没有对应行。 |
| knowledge-manager | m1 | `f410df76` | `f410df76` | minor | issue | documentation | proposal.md Impact | 四处同一事实在 Spec 内写法不一致: 覆盖关系写「两处有意偏离」而 Impact 与 Tasks 1.13 写「三处」; Why 表 SC-23 的「6/6」是 v5 新增 23j 之前的运行数 (现为 10 个基线 exit 2 运行); Impact 性能百分比 (+13% / +16%) 与 W14 比值 (1.14 / 1.14) 及 1.5 下界与 (g-a) 1.42 不符; 19ak「另有两行以 forgejo 为锚」实为 4 行 (secret-guard.sh:778 与 :1006-1008)。都不改变实现者要写的代码。 |
| knowledge-manager | m2 | `0c3c6ed4` | `0c3c6ed4` | minor | issue | documentation | baseline_probe.py | 探针行描述与注释里留有版本相对词: 22bp 行描述「v4 additions」(baseline_probe.py:1753) 经 stdout 原样进入 baseline-evidence.md:398, 另有「(v2)」「# v3:」注释; 执笔的叙事 lint 只扫 proposal.md, 是 R4 km/m2 同类的兄弟位置; 批准后成悬空引用且修改须连带重生成证据。 |
| knowledge-manager | m3 | `a305732c` | `a305732c` | minor | issue | testing | baseline_probe.py | 探针执行器 (baseline_probe.py:2525-2526) 对行任务没有逐行异常隔离: 任一行里一次 hook 调用超过 timeout=300 即整个探针 traceback 退出 rc 1、其余行结果全部丢失 (实测: loadavg 约 20 的主机上 ext_perocc_judge 坏实现整探针 PROBE-ERROR; 仅跑 34c 则正常红); 坏实现红退化成整探针崩溃。 |

## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)

- 主控定稿键映射 (同一问题不同四元组, 比较前先映射): `51e90cab` → `eb350937`; `5ce95ecf` → `eb350937`; `5fd1f356` → `ce6fc59c`; `8fbbee80` → `e2459206`; `e7e041c6` → `eb350937`; `fc97f926` → `e8d39a8a`
- 本轮 Critical+Major 键集 (6): `12a776ac`, `66d6eb81`, `6bd285b1`, `755aab21`, `ac42f607`, `df25d271`
- 上一轮 Critical+Major 键集 (6): `0a8380fd`, `1038b8da`, `22bdd143`, `755aab21`, `e2459206`, `eb350937`
- conclusions_stable = False
- unanimous_pass = False (1 PASS / 4 REVISE)
- converged = False

## 机械核对

- 席位数 5 / 5; incomplete = False
- frontmatter 开头: tech-lead=ok, backend-architect=ok, qa-engineer=ok, code-reviewer=ok, knowledge-manager=ok
- 自报 counts 与 findings 计数不一致的席: 无
- finding id 与四元组重算不一致: 0 条
- 竞品 Spec 探针 (本轮入口): status=ok / verdict=no_sibling_found

## 主控记录

> 2026-10-07 主控追加。只在这里写主控的核验与裁定; 上面各节是脚本生成的机械聚合, 未改动。

### 簇归并

R1-R4 已用过 A-W 各字母, 本轮新簇从 X 起编; 沿用 R4 的键 (`755aab21`) 仍记 W。

| 簇 | 问题 | 席位编号 (键) | 性质 |
|---|---|---|---|
| X | L3 对失败的工具调用整体失明: Bash 非零退出走 `PostToolUseFailure` (只带 `error`, 无 `tool_response`), secret-scan 未注册该事件; Spec 把它误述为「字符串形 `tool_response` 未证实」并钉成 SC-3 3b, W8 / W10 / W11 多处「交给 L3」对失败调用不成立且未申报 | tl/M1 `66d6eb81` | 既有设计缺口 (自 v1 起的平台模型), 本轮首次发现 |
| W | W2 的线性规则只禁前导 `*` 的 `#` / `##`, 不足以保证线性: 原型 kv 去引号 `${V#["']}` 在不带引号的长值上是平方级, 约 300 KB 在负载下越过 CPU 上限, 同输出的基线检出随之丢失; 34b 与 (i3) 无此形态 | tl/M2 `755aab21` | R4 簇 W 残余 (v5 写下的线性规则本身不充分) |
| Y | 按 W9 把 `_sg_per_segment_eval` 函数体移到 `_sg_core_eval` (source 闸门之下) 后, 既有测试内 SC-8 五档延迟闸只抽到壳、每次 rc=127, 新侧 -97% 五档恒绿; W14 耦合清单与探针都没有这一项 | qa/M2 · ba/M1 `6bd285b1` | **v5 返修引入** (簇 T 修法造成的接缝) |
| Z | W11 `:196` 与 SC-22 `:291` 称「基线对 `docker\|kubectl\|podman\|lxc exec … env` 已拦」并据此判四个包裹的转储备选为等价变异, 与源码覆盖面不符; 删掉它们的坏实现过全部 SC-22 / SC-25; 包裹下 `printenv NAME` 的边界与「只拦裸」相反且无行; Impact 未申报 | cr/M1 `ac42f607` | **v5 返修引入** (簇 F 修法的文字与等价论证) |
| AA | W11 写的是语义, SC-22 只钉规范拼写: 命令位置锚点的 `&` `{` 反引号、`pgrep` / `pstree` 的 `-a` 位置、`ps -o` 列表关键字位置、`ps -F`、`docker ps -a --no-trunc`、launcher 时长后缀六类自然窄化在全部相关行 0 行红 | qa/M1 `12a776ac` | 既有缺口 (W11 引入以来; R2 簇 K / M、R3 簇 K / M 同族) |
| AB | W9 条目文件输入面三个常见条件无行 (清单末行无换行、项目根路径含空格、`CLAUDE_PROJECT_DIR` 置空而 stdin `cwd` 有值), 两个自然错误实现过 SC-19 / SC-20 全部 54 行 | ba/M2 `df25d271` | 既有缺口 (W9 引入以来) |

键去重是有损的 (memory 「aggregation-lossy」): `0033f2f4` 下是两件不同的事 (tl/m2 待复议 23 误引 25898; qa/m2 「并入 7.8 / 7.9」悬空), `684e9a24` 下也是两件 (tl/m3 W9 文档未写保护边界; ba/m1 完整路径条目对 `..` / `//` / `/./` / `cd` 后相对名失效); `f410df76` 的 qa/m3 与 km/m1 是同一事实。机械去重的 11 条 minor 实为 13 件。

### 主控独立核实

- 簇 X: 在本机 Claude Code 2.1.285 二进制中逐字核对:
  - 事件表原文 `| PostToolUse | Tool name | Run after successful tool |` 与 `| PostToolUseFailure | Tool name | Run after tool fails |`;
  - 失败事件输入 schema `hook_event_name:R("PostToolUseFailure"),tool_name,tool_input,tool_use_id,error:o(),is_interrupt?,duration_ms?`, 无 `tool_response`;
  - Bash 默认退出码语义 `isError:e!==0`, 失败时 `throw new _U({stdout:"",stderr:<合并输出>,code:…})`, `_U` 即 `ShellError` ("Shell command failed");
  - 失败事件同样产出 `hook_additional_context` (`hookName:"PostToolUseFailure:<tool>"`);
  - 已安装的 v1.74.1 `hooks.json` 中 secret-scan 只注册在 `PostToolUse`。
  - 主控**未做**端到端实测 (未构造「打印后失败」的命令观察 L3 是否触发)。
- 簇 Z: 实读 aria `268da8f` `hooks/secret-guard.sh`: `:858` docker 行要求 `env` 前为空白、后为空白 / 行尾 / 分隔符; `:862-863` kubectl 两行要求 `--`, 或 `env` 后接行尾 / `|`; `:938` podman 行要求 `env` 前为空白; `:940` lxc 行要求 `--`。席位列举的引号形、`$(…)` 形、重定向形、无 `--` 的 lxc 形都不在其内, 「基线已拦」不成立, 前提属实。主控未复跑席位的坏实现。
- 簇 W: 微基准 (bash 5.2.15, `C.UTF-8`, 主机 1 分钟负载约 1): 不以引号起头的值上 `${V#["']}` 用户态 CPU 25 KB 0.014 s → 50 KB 0.061 s → 100 KB 0.276 s, 每翻倍约 4.4 倍 (平方级); 改为首字符判断后三档均 ≤ 0.001 s。平方级属实; 绝对耗时随负载变 (席位在负载约 20 时测得 100 KB 1.38 s), 触发尺寸在数百 KB 量级。
- 簇 Y: qa 与 ba 两席各自在带 `af87cae` 历史的副本上独立复现 (新侧 -97%, 调用 rc=127, 把 `_sg_core_eval` 移到闸门之上即恢复真测); 主控未复跑。
- 簇 AA / AB: 主控未复跑, 依据席位给出的坏实现与直调结果。

### R4 对账汇总

- 五席对 R4 六簇: U / T / V / F / M 五席一致判 closed; W 四席判 closed, tl 判 partially closed, 其残余即本轮 tl/M2 (沿用同键)。
- R4 minor 的遗留 (席位认定): `6ff1d962` 的 printenv 一侧 (tl/m1, 与簇 Z 的 printenv 部分同一处); `984b1c3d` 的「并入 7.8 / 7.9」悬空 (= 本轮 qa/m2); `91a89f9b` (km R4/m6) partially closed —— Spec 侧已关, 研究笔记 `research/secret-guard.md:20` / `:371` 仍含量化配方, 已推到公开镜像的部分属 owner (7.20)。

### 趋势与判断

- Critical: 6 → 1 → 0 → 1 → 0。Major (定稿去重): 24 → 11 → 10 → 5 → 6。
- 本轮 6 个 major 键: v5 返修引入 2 个 (Y、Z), R4 残余 1 个 (W), 其余 3 个 (X、AA、AB) 是早几版就存在、本轮才被找到的既有缺口。按 memory 「本轮 fix 引入的 major 占比 > 1/2 即到拐点」, 本轮是 2/6 (连 W 算是 3/6), 没有越过拐点。但 major 数持平, 且 W9 / W11 自 R2 起每轮都有 major (R2 K / M, R3 K / M / R / T, R4 T / V / F, R5 Y / Z / AA / AB): 每轮都能在这两节找到新的「语义写了、行没钉」缺口, 加轮的边际产出在这两节不会很快变小。
- 五席对「以 v5 进入 A.2」的表态一致: **足以, 但须先定点修补** (tl / ba / qa / cr 附前置条件, km 无条件 PASS)。没有一席建议再开全轮; 四席建议「定点修补 + 只对修补处做一次非作者定向核验」后进入 A.2, 并由 `post_planning` 收敛审计兜底。
- **收敛判断**: R5 有 major 且 4 席 REVISE ⇒ `post_spec` 在 `max_rounds` 5 内未收敛 (MAX_ROUNDS_EXHAUSTED)。按 audit-engine 降级策略与 Rule #10 交 owner 裁定; 主控不自行降级, 也不自行修补后宣布通过。

### 席位提出、不计 finding 的事项 (供 owner 裁定时参考)

- tl (自报薄弱点 5): W14 (f) 档的实际判据退化为主机属性 —— 参考设计比值 1.53-1.67 恒高于 1.5, 判据变成「基线 CPU ≤ 约 0.09 s」, 主机稍忙时正确实现随机转红; 建议改为纯比值上界或增量上界, 作为进 A.2 前的定点勘误。
- qa (风险 2 / 3) 与 km/m3: 探针退出码不反映红行; 任一行 hook 调用超时会让整个探针 traceback 退出。
- cr (风险 2): Tasks 1.13 只写「1.12 / 1.13 勾选后归档」; 若归档闸门把 rule6_note 的 dogfood 声称判为未验证, headless 归档可能自动开 issue, 而开 issue 不在一次性授权内。
- ba/m2 · tl · qa · km: 四席都认为执笔不采纳「post-ship 加 NUL 腿」的理由不成立 (该腿恰能产生缺的那个端到端样本), 其中 ba 立为 minor。
- km (风险 1): 建议在下一次提交前对研究笔记两处量化配方做前向去量化 (不改历史)。主控本轮未做: 是否处理、怎样处理属 7.20 的产品级披露决定, 一并呈 owner。
- km (风险 2): W5 是 AI 增补 (10CG/aria-plugin#154 评论 19339 说告警措辞「现行已满足」), 建议给 owner「删除 W5」选项。
- km (风险 3) / ba (风险 6) / qa (自报薄弱点 7 的表态): 体量 (proposal 449 行 / 214 KB, 单行常 1-5 KB) 使席位只能抽样审阅; 本轮 major 正出在最密的 SC-22 与耦合清单。ba 建议 A.2 为每个 W 附一页实现者摘要, 把「写在别处的耦合」收拢进去。

### 流程记录

- 竞品 Spec 探针 (本轮入口): `ok / no_sibling_found` (github 157 / origin 162)。
- 派单指纹: tl `bc80a13eaeb5c786` / ba `950eec59fbc5dd8b` / qa `3f13d012fabfdb57` / cr `2c2af06ed5e64002` / km `ab939a6411812cf0`。
- 运行: A 组 (tl / qa / ba 并行, 主机并发上限 2, ba 排到 09:07Z 才启动) 08:01Z-10:14Z; B 组 (cr → km 顺序) 08:01Z-09:59Z。每席一个最终结果, 无自动重试。
- tl / ba / cr / km 四席都报告现行 v1.74.1 L1 拦下了自己 heredoc 里仅为文本提及的命令 (W12 / 22bj 误拦类的现网实例), 均改用 Write 落脚本, 未用 `# guard:ack`。
- 公开镜像: 工作分支 origin 在 `6efb9b2`, GitHub 仍停在 `b07f69a` (v4, 含研究笔记量化配方); 自 R4 起只推 origin 的做法不变, 仍列 owner 复议。

### 呈 owner 的降级裁定

本轮之后即 MAX_ROUNDS_EXHAUSTED。主控把 audit-engine 降级三选一 (接受当前结论 / 增加轮次 / 降级为单轮) 与 owner 2026-08-16 决策单列过的「缩小被审对象」一并呈 owner。各选项的代价按本 Spec 实测:
- 历次返修墙钟 3.7-6.9 h, 且逐版变长;
- 每轮五席审计 2.1-2.5 h (R1-R5 实测)。

簇 X 的处置方向 (本 Spec 内补齐失败事件注册, 或列为已知限制) 涉及保护边界, 同时呈 owner。裁定结果在本节之后追加。
