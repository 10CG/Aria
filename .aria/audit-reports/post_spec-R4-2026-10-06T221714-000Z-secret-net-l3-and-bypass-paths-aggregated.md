---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-10-06T22:17:14.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 1C/9M/15m
counts_dedup: 1C/6M/13m
sibling_probe: no_sibling_found
---

# post_spec R4 聚合 — secret-net-l3-and-bypass-paths — 未收敛

> 本节为机械聚合 (脚本从运行记录生成; 各席报告原文见同目录同轮次文件)。主控独立核验与处置意见见文末「主控记录」节。

## 判定

| 席 | verdict | counts (自报) | counts (按 findings 计) | vote | 报告文件 |
|---|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | 0C/2M/2m | 0C/2M/2m | REVISE | `post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-tech-lead.md` |
| backend-architect | FAIL | 1C/2M/1m | 1C/2M/1m | REVISE | `post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-backend-architect.md` |
| qa-engineer | PASS_WITH_WARNINGS | 0C/2M/3m | 0C/2M/3m | REVISE | `post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-qa-engineer.md` |
| code-reviewer | PASS_WITH_WARNINGS | 0C/2M/2m | 0C/2M/2m | REVISE | `post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-code-reviewer.md` |
| knowledge-manager | PASS_WITH_WARNINGS | 0C/1M/7m | 0C/1M/7m | REVISE | `post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-knowledge-manager.md` |

## 全部 finding (按席位原编号, 不转述)

| 席 | 编号 | 键 (重算) | 席位所写 id | severity | type | category | scope | summary (席位原文) |
|---|---|---|---|---|---|---|---|---|
| tech-lead | M1 | `e2459206` | `e2459206` | major | issue | architecture | proposal.md What.W11 | W11 未规定包裹下 env / printenv 整环境转储 (22bo 的 22 个成员) 的 credit 制度。原型因 tight 拷贝与包裹规则行同源, 把它们并入 tight, 使基线经锚定 grep / cut / sed 放行的既有形态 (docker\|kubectl\|podman exec … env \| grep '^X=' / \| cut -d= -f1) 由放行变拦。该变化未申报、无 SC 钉住任一方向, 且与同族 /proc environ (Spec 明文保留基线语义) 和裸 env 的判定相反; 两种实现在 411 行上都全绿。 |
| tech-lead | M2 | `22bdd143` | `22bdd143` | major | issue | testing | proposal.md What.W14 | W14 没有任何时档覆盖 W9 的命中路径 ((f) 用 ls -la, (h) 的命令与条目不相交, (g) 不带扩展)。原型逐出现点用 ${before##*[;&\|\n]} 计算阶段, 在无分隔符前缀上是 O(前缀长²), 再乘以至多 64 个出现点; v4 的引号掩码又让内联程序变成无分隔符。实测单处 4 KB 为基线 1.70 倍, 2 KB 内 64 处约 10 倍, 8 KB 内 64 处单次超过 90 s CPU。W9 的「64/200/32 KiB 即成本上界、命中 O(命令长度)」与实测不符, SC-30 对此恒绿; 超时即放行。 |
| tech-lead | m1 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | 包裹 × env / printenv 备选不要求 env 处在被包裹命令的命令位置, 因此 bash -c "python3 -m venv env && …"、sh -c "…; python3 -m venv env"、watch "du -sh env"、含 ssh / sshd 与 env 词的提交信息都由放行变拦。这与 W11「只拦裸 env / printenv」不符; W11 已知限制、Impact 与 22bj 只申报了「包裹词 + 进程表形态」的文本提及。 |
| tech-lead | m2 | `984b1c3d` | `984b1c3d` | minor | issue | documentation | proposal.md What.W2 | Forgejo / Gitea 容器部署的 FORGEJO__<section>__<KEY> 环境变量形态 (section 小写, 如 FORGEJO__security__SECRET_KEY) 承载与 #203 同一批凭据, 在基线与目标两层都静默 (L1 只认 app.ini, L3 的 kv / env-line 都要求全大写键), 但 W2 / W8 已知限制、SC-10 与 7.8 / 7.9 都未列。 |
| backend-architect | C1 | `1038b8da` | `1038b8da` | critical | issue | implementation | proposal.md What.W1 | W1 的 `tr '\000' '\n'` 使 ASCII 字符间夹 NUL 的文本 (UTF-16LE 经 Bash 输出) 的基线检出变成静默, 而 Spec 称「命中不会因此减少」, 与实跑相反, 构成安全回退。 |
| backend-architect | M1 | `755aab21` | `755aab21` | major | issue | implementation | proposal.md What.W2 | W2 称 6 个新模式是线性 ERE, 但 `cli-secret-flag` 的自然写法 (及去掉左边界的 `kv-secret-assign`) 在单行长连续段上是二次方的, 8 KB 行即超过 5 s 超时使同一输出里基线可检出的凭据失检; 全部 SC 与 W14 时档 (i) 都放过这类实现。 |
| backend-architect | M2 | `0a8380fd` | `0a8380fd` | major | issue | implementation | proposal.md What.W9 | W9 声称扩展对同形命令的判定与内建 `app.ini` 行一致, 但扩展自写的阶段 / 尾部切分与内建分段不同: 反斜杠换行续行与 `\|\|` 后管道被放行 (内建拦), `2>&1` / `&>` 等重定向与引号内计数管道被误拦 (内建放), 差分 324 对中 36 对相反, 而 SC-19 只钉了引号一类。 |
| backend-architect | m1 | `6f503728` | `6f503728` | minor | issue | implementation | proposal.md What.W9 | 纯非 ASCII 条目被静默跳过 (19ae 钉现状), 对中文环境是默认静默失效; 替代 (含任一非 ASCII 字节即有效) 只是一处条件且同样与 locale 无关, 属技术级可直接裁定。 |
| qa-engineer | M1 | `0a8380fd` | `0a8380fd` | major | issue | implementation | proposal.md What.W9 | W9 引号感知阶段切分 (_sg_ext_mask) 的反斜杠转义与 $'…' 状态没有行钉住 (19z/19aa 只含未转义的双/单引号程序): 三个自然的坏实现 (mask_noesc_q / mask_noesc_all / mask_noansi) 在 SC-19+SC-20 共 46 行上 0 行红, 却对内建 app.ini 行必拦的同形命令放行, 与 W9「与内建同形命令判定一致」相反; R3 簇 T 只部分关闭。 |
| qa-engineer | M2 | `eb350937` | `eb350937` | major | issue | testing | baseline_probe.py | W8.3 原位改写 Read/Edit 面正则行 (secret-guard.sh:641, 32 个基线备选), 但 W14「原位改写通则」清单漏了这一行, 其中 16 个备选没有任何用例会因删除而转红: 删掉它们的坏实现通过探针 SC-16..25 全部 197 行与现有套件 584/585 (仅已知无 git 伪影), 基线拦的 Read/Edit 由拦变放; R3 簇 M 的残余。 |
| qa-engineer | m1 | `65fb3fcf` | `65fb3fcf` | minor | issue | testing | proposal.md SC-23 | SC-23 只钉四个单键读取子串各出现一次, 不钉同一子串多处出现全部归一 (只替换第一处的坏实现 SC-23 9 行 0 行红, 含两处 os.environ.get 的命令仍被拦), 且 W12「Command was: 仍是原文 (SC-25 不变)」的锚点被 SC-25 的归一化抹掉。 |
| qa-engineer | m2 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | W9 格式规则没有提 UTF-8 BOM: Windows 工具写出的清单首行带 BOM 时首行条目静默失效 (目标原型 BOM+路径 与 BOM+CRLF 均 exit 0, 无 BOM 同内容 exit 2), 与已成文的 CRLF / 纯非 ASCII 条目同族但未列入已知限制或测试。 |
| qa-engineer | m3 | `aa08f71d` | `aa08f71d` | minor | issue | testing | proposal.md SC-32 | 32d 的第二 locale 缺省仍是 UTF-8 (en_US.UTF-8), 而 Layer 2 的 aria-runner 镜像 (node:20-bookworm-slim, 无 LANG/LC_ALL) 里 hook 跑在 POSIX locale: 按字符判 … 后缀的坏实现 ell_lastchar 在 107 行 SC-4..11 与默认 32d 下 0 行红, WPA_LOCALE_B=C 时 32d 转红 (11v/11x/11y); 目标原型本身在 C 下一致, 属验收覆盖缺口。 |
| code-reviewer | M1 | `0a8380fd` | `0a8380fd` | major | issue | implementation | proposal.md What.W9 | W9 的 Bash 面扩展判定没规定出现点偏移与切片用同一单位: v4 只要求读条目的 tr/sed/awk 在 LC_ALL=C 下执行 (:163), 又允许 grep -b 偏移量作算术操作数 (:166)。照字面实现 (grep 给字节偏移, ${s:off} 在 UTF-8 locale 按字符切片) 时, 出现点之前有约 20 个以上中文字符 (单行 echo 或多行脚本的中文注释) 会漏拦, 内建 app.ini 行对同形命令照拦。原型只因另写了 Spec 没有的 local LC_ALL=C 才能拦; 照字面的坏实现在 SC-19/20/25/32 共 57 行 (含真 bash 3.2 的 32c 与 32d) 全 yes。 |
| code-reviewer | M2 | `8fbbee80` | `8fbbee80` | major | issue | testing | proposal.md What.W11 | 包裹 × env/printenv 转储 (22bo, 11×2) 的 credit 是否 tight 没定, 22bm/22bn 不含这些成员, 探针对「转储 + 行级过滤」两个方向都没有行。把转储拆成不进 tight 拷贝的独立行的实现在 124 行全 yes, 却放行 nomad alloc exec … env \| grep -v PATH、ssh host env \| grep -v X 等整份环境输出。反过来, 原型使基线 docker/kubectl exec 转储加锚定 grep 或只出键名的 sed/cut 由放变拦, 未申报。4 个 remote_env_split 被论证为等价变异, 在带过滤的转储上不成立。属 R3 簇 M 残余。 |
| code-reviewer | m1 | `6ff1d962` | `6ff1d962` | minor | issue | documentation | proposal.md What.W11 | W11 新增误拦与 Impact 只申报了包裹词之后出现进程表形态的文本提及。另有两类由放变拦且未成文未钉行: 包裹词 (v4 扩到 watch / sh -c / bash -c / 不加引号的 ssh) 之后出现 env/printenv 词, 包括提交信息、echo 与 bash -c "… venv env" 这类参数词; 新增 /proc 读取器 (grep / rg / sed) 对含真实 pid 记号的 /proc 路径文本的检索与编辑。 |
| code-reviewer | m2 | `684e9a24` | `684e9a24` | minor | issue | documentation | proposal.md What.W9 | W9 :165 的「+6–9 ms (Bash 面 0.052 → 0.061 s)」与 Impact :346 的「200 条扩展条目约 +27 ms」仍是 v3 时档数; v4 的 W14 已改为 (f0) 0.048→0.058 / 0.041→0.048 s、(f) 0.049→0.072 / 0.042→0.067 s。是 R3 cr/m8 旧数未同步的兄弟位置。 |
| knowledge-manager | M1 | `0a8380fd` | `0a8380fd` | major | issue | implementation | proposal.md What.W9 | W9 声称引号掩码覆盖 `$'...'` 与转义并与内建 _sg_split_top 同一套状态机, 但 SC-19 只有无转义的单/双引号形; 不认反斜杠转义或把 `$'...'` 当普通单引号的自然掩码让 SC-19 29/29、SC-20 17/17 全绿, 却放行内建 app.ini 行会拦的同形命令 (R3 簇 T 残余)。 |
| knowledge-manager | m1 | `a8f5db8c` | `a8f5db8c` | minor | issue | documentation | proposal.md What.W1 | W1 设计取舍的两句理由与实测相反: 不带 tr 的实现并非两层皆静默 (kv-secret-assign=1 仍告警, 执笔的 mut_summary 也如此记), NUL 换空格也不是修不了 (kv-secret-assign=3); 选 A' 的结论仍对, 理由写错。 |
| knowledge-manager | m2 | `13e1f258` | `13e1f258` | minor | issue | documentation | proposal.md 待复议 | v4 把版本/审计叙事写回 Spec 正文 9 处 (v3 的已知限制曾写、v4 另加七类、本版、上两轮、eval 式实现曾全绿等), 重蹈 R1 km 381efd94 与 audit-trail 备忘覆辙; 不改变实现者动作, 但 Approved 后成悬空引用。 |
| knowledge-manager | m3 | `7b20c975` | `7b20c975` | minor | issue | documentation | proposal.md SC-30 | 执笔称时档数字已按终版重测更新, 但 W9 的无扩展开销 (0.052→0.061 s, +6-9 ms) 与 Impact 的扩展开销 (含 200 条扩展条目 +20-25%、+27 ms; 1.4-2.3 倍) 仍是 v3 的数, 与 W14 / timing_summary 的 v4 终测不符。 |
| knowledge-manager | m4 | `60eea71e` | `60eea71e` | minor | issue | testing | proposal.md SC-26 | SC-26 26g 只查 7 个子串, 撑不起 Impact 所称『六条逐条披露』; 28m 的『Hooks 小节』在两份 README 里各有两个同名/近名小节而 Spec 未指明是第二个 (探针取最后一个)。 |
| knowledge-manager | m5 | `cfd9ca0b` | `cfd9ca0b` | minor | issue | testing | proposal.md SC-19 | W9 的『LC_ALL=C 使结果与 awk 实现无关』在 mawk 主机上无法被 19ad/19ae 证伪: 删掉 LC_ALL=C 的坏实现在本机 (mawk 1.3.4) SC-19 29/29、SC-20 17/17 全绿; 缺 gawk 腿 (R3 ba/m2 残余)。 |
| knowledge-manager | m6 | `91a89f9b` | `91a89f9b` | minor | risk | documentation | proposal.md 待复议 | 工作分支 docs/secret-net-l3-and-bypass-paths-phase-a 已推到 origin 与公开 GitHub 镜像 (匿名可读; 派单背景写『未推送』), 其中待复议 7.1/7.2 与 research 笔记含未修复旁路的可操作配方, owner 门未登记; 本席 R3 风险 6(b) 的前提已不成立。 |
| knowledge-manager | m7 | `8936aa07` | `8936aa07` | minor | issue | documentation | proposal.md SC-22 | 四处引用精度: W14 陈旧表述清单漏 secret-guard.sh:8 『~100 most common patterns』(基线 145 行/目标 149); 22av 清单摊平 `ps -w -x`; W11 launcher 小节 22bk 清单列 10 个包裹而行里 11 个; Impact 称 git-commit.md §6.1『要求』Closes (要求在 COMMIT_FOOTER_GUIDE.md:199, 且部分实现本就写 Refs)。 |

## 收敛计算 (本仓先例口径: 相邻两轮 Critical+Major 键集相等 且 全票 PASS)

- 主控定稿键映射 (同一问题不同四元组, 比较前先映射): `51e90cab` → `eb350937`; `5ce95ecf` → `eb350937`; `5fd1f356` → `ce6fc59c`; `8fbbee80` → `e2459206`; `e7e041c6` → `eb350937`; `fc97f926` → `e8d39a8a`
- 本轮 Critical+Major 键集 (6): `0a8380fd`, `1038b8da`, `22bdd143`, `755aab21`, `e2459206`, `eb350937`
- 上一轮 Critical+Major 键集 (10): `05982c10`, `0a8380fd`, `1c49d896`, `28af0372`, `44b5bb44`, `4f713847`, `8d258b19`, `8fbbee80`, `ac42f607`, `eb350937`
- conclusions_stable = False
- unanimous_pass = False (0 PASS / 5 REVISE)
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

| 簇 | 问题 | 席位编号 (键) | 性质 |
|---|---|---|---|
| U | W1 为处理 NUL 分隔内容加的 `tr '\000' '\n'` 把 ASCII 字符间夹 NUL 的文本 (UTF-16LE 经 Bash 输出) 拆散, 基线能检出的凭据变静默 —— 检出回退 | ba/C1 `1038b8da` | **v4 返修引入** |
| T | W9 扩展的共现判定与内建 app.ini 行不一致: 引号掩码不认反斜杠转义与 `$'…'`; 出现点偏移按字节、切片按字符 (中文前缀漏拦); 扩展自写的阶段切分与内建分段不同 (续行、`||` 后管道放行, `2>&1` 等误拦; 差分 324 对中 36 对相反) | qa/M1 · cr/M1 · km/M1 · ba/M2 `0a8380fd` | R3 簇 T 残余, 多处 v4 引入 |
| V | W14 没有时档覆盖 W9 命中路径; 逐出现点计算阶段在无分隔符前缀上是平方级, 8 KB 内 64 处单次超过 90 s CPU, 超时即放行 | tl/M2 `22bdd143` | v3 / v4 实现 |
| W | W2 `cli-secret-flag` (及去掉左边界的 `kv-secret-assign`) 的自然写法在单行长连续段上是平方级, 8 KB 行越过 5 s 超时, 同一输出里基线可检出的凭据失检 | ba/M1 `755aab21` | 既有设计缺口 |
| F | W11 包裹下 env / printenv 整环境转储的 credit 制度未规定 (tight 与否), 两个方向都没有行钉住; 原型使基线经锚定 grep / cut 放行的 docker / kubectl exec 转储由放变拦且未申报 | tl/M1 `e2459206` · cr/M2 `8fbbee80` → `e2459206` | R1 簇 F 的延伸 |
| M | W8.3 原位改写的 Read / Edit 面正则行有 16 个基线备选没有任何行钉住 | qa/M2 `eb350937` | R3 簇 M 残余 |

### 趋势与判断

- Critical: 6 → 1 → 0 → 1 (本轮这条由 v4 返修引入)。Major (定稿去重): 24 → 11 → 10 → 5。
- 本轮六键里 U、T 的大部分、V 由 v3 / v4 返修引入, 占比过半 —— 按本仓 memory 的判据已到边际拐点。
- **收敛判断**: R4 有 critical / major, 按收敛口径 R5 无论结果如何都不可能与 R4 键集相等且全票 PASS ⇒ post_spec 在 `max_rounds` 5 内不可能收敛。按 audit-engine 流程, 第 4 轮未收敛且未到上限仍须进入第 5 轮; 第 5 轮之后即 MAX_ROUNDS_EXHAUSTED, 由 owner 在降级策略三选一 (接受当前结论 / 增加轮次 / 降级为单轮) 中裁定, owner 2026-08-16 决策单列过的另两种处置 (换执笔人 / 缩小被审对象) 一并呈上。主控不自行降级、不自行缩小范围。
- 第 5 轮的意义因此是: 修掉本轮的 critical, 并给 owner 提供「最后一版是否干净」的独立证据。

### 主控独立核实

- 簇 U: 实读 v4 W1 改动条, 确有 `tr '\000' '\n'` 一步且写明「命中不会因此减少」; ba 席的反例 (UTF-16LE 经 Bash) 与之直接矛盾, 前提属实。
- 簇 T: 四席独立指向同一处, 其中 ba 席给出 324 对差分结果; 主控未复跑。

### 流程记录

- **竞品 Spec 探针**: 本轮入口首次运行 `status=degraded / verdict=not_established / reason=remote_unresolved` (按规范渲染「未能核实」); 重试一次即 `ok / no_sibling_found` (github 157 / origin 162, 各比上一轮多 1 份 —— 即本 Spec 自身推到远端分支后的副本, 探针按 own-spec 排除)。派单用重试后的结果重新生成 (指纹见下)。
- 派单指纹 (重新生成后): tl `e6574e1a917f6e90` / ba `773bb1143457101a` / qa `05d60e723270dcf5` / cr `0964bbae03132da8` / km `a8800d459998e7b3`。
- A 组运行记录显示 tl 与 qa 各被启动 4 次 (平台对中途出错的 agent 自动重试), 每席只有一个最终结果落盘。
- **公开镜像风险 (km/m6)**: 工作分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 此前已推到 origin 与公开的 GitHub 镜像 (属 owner 一次性授权的「两个 remote 推送」), 其中研究笔记与「待 owner 复议」节含未修复旁路的可操作复现方法。已在公开端的内容, 删除需要强推或删分支, 属破坏性动作, 主控不做, 列为 owner 裁定项; 主控从本轮起该分支**只推 origin、暂停推 GitHub** (可逆), 作为 AI 自作主张的流程判断请 owner 复议。

### 主控裁定 (v5 返修据此执行; 均为技术级, 列入 handoff 请 owner 复议)

1. **簇 U**: NUL 处理不得减少任何基线检出 —— 例如原视图照扫、仅当输出含 NUL 时再追加一个视图并取并集; 补 UTF-16LE (ASCII 间夹 NUL) 仍检出的反向守卫行与进程环境形检出行。
2. **簇 T**: 扩展的共现判定必须**复用内建的分段 / 切分逻辑** (同一函数), 从构造上与内建 app.ini 行一致; 用一组覆盖转义、`$'…'`、续行、`||`、重定向、引号内管道的命令形态做差分, 要求零分歧, 并钉进 SC。
3. **簇 V / W**: 新增的匹配与扫描必须对输入长度线性 (写明为什么线性), 并补能暴露平方级行为的时档行 (例如 8 KB 单行、64 处出现点)。
4. **簇 F**: 明确规定包裹下整环境转储的 credit 制度, 两个方向都用 SC 钉住, 行为变化在 Impact 申报。
5. **簇 M**: W8.3 改写的 Read / Edit 面正则行逐备选钉住。
6. **全部 minor** 照返修模板逐条处置。
7. **方针**: 第 5 轮是 `max_rounds` 内的最后一轮。v5 优先复用已有机制, 不写新机制; 每改一处都配会转红的坏实现; 只能靠新机制才能修的, 收窄语义或列为已知限制并论证 (写进「待 owner 复议」), 但不得降低既有检出。
