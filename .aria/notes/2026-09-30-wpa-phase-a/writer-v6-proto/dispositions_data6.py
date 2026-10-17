# -*- coding: utf-8 -*-
"""Dispositions of the 21 seat entries of post_spec R5 and the 6 non-finding items of main-control ruling 7 (27 entries).
Each entry: seat / label / key / disposition (fixed | rejected | deferred) / where_or_evidence.  The report's disposition table is generated from this list, so the table and the
structured output cannot drift.  Rule #7: no credential-shaped literal in this file (placeholders only)."""
D = [
    dict(seat="tech-lead", label="M1", key="66d6eb81", disposition="fixed", where_or_evidence=(
        "簇 X (owner 裁定「本 Spec 内补齐」)。设计: hooks.json 为 secret-scan 增一条 PostToolUseFailure 注册 (matcher / 命令 / 超时同其 PostToolUse 条目, 不碰别的条目, 不含 completeness_gate 字面); "
        "提取链末尾加 .error, 失败信封与成功信封走同一条提取 → 分类 → 告警路径; 输出 hookSpecificOutput.hookEventName 取输入的 hook_event_name (先子串预检再 jq 确认, 文本里只是提到事件名不翻转)。"
        "二进制核实 (2.1.285, logs/binary_fragments.txt): 事件表 Run after successful tool / Run after tool fails; 输入 schema 无 tool_response、有 error; harness 抛 "
        "「Hook returned incorrect event name: expected '…' but got '…'」, 所以事件名写死 PostToolUse 的实现会丢告警 (备选 C 不可行)。"
        "落点: Why「平台事实 (失败的工具调用)」与基线实测表新行; W1 新条「失败事件」(改动 1-3 / 设计取舍 A-B-C / 已知限制: 送达未验证、契约取自 2.1.285); SC-3 3b 重述 (失败调用走 SC-35); "
        "W8 / W10 / W11「交给 L3」各处改「成功与失败的调用都经 L3」; Impact (新告警 / 与 10CG/Aria#199 的接缝 / 同步面 / 覆盖关系); rule6_note 块 A 理由与可证伪锚点 31d; Out of scope; 待复议 7.7 与技术级 33; "
        "Tasks 1.12 第 6 腿 (post-ship 验证, 不作关单门) 与 1.13 披露。新行 SC-35: 35a / 35b / 35d baseline-failing (基线 0/3、0/3、no), 35c reverse-guard, 35e allow-guard; SC-31 31d / 31e; 文档行 26g (标记词 PostToolUseFailure)、26k、28f。"
        "坏实现: fail_noextract → 35a + 35b 红; fail_noclassify (失败路径漏掉分类器与白名单) → 35e; string_response (把字符串形 tool_response 也扫, 即收口 3b 的已知限制) → 3b 红; fail_event_name → 35b; fail_event_always → 35c; fail_event_substr → 35c; hooks_nofail / hooks_wrong_matcher / hooks_two_entries / hooks_other_hook → 35d; "
        "hooks_touch_other → 31d + 35d; hooks_gate_literal → 31e (31d 只比较注册, 不比较 description 字符串; mut_summary_v6 PART A)。目标原型 35a-35e 全 yes。")),
    dict(seat="tech-lead", label="M2", key="755aab21", disposition="fixed", where_or_evidence=(
        "簇 W (同族不止 tl 复现的 kv 去引号, json / kv / env 行 / URL 的取值全部会在远分隔符上平方级)。规则: 取值代码里的任何 #  ## % %% 删除必须在常数次尝试内命中 (分隔符必然存在且位置靠前: 固定头名后的 `:`、至多 40 字符旗标名后的 `=`、JSON 值两端的引号、scheme 后的 `://`); "
        "可能很远的分隔符用一次 [[ =~ ]] 找到再按 ${s:N} 切; 可能不命中的单字符剥离用 ${V:0:1} 判断后切片。落点: W2「线性」段重写 (原句改写, 实测数字取自本轮 timing / bad_cost500 输出); W4 取值表 kv 行加实现注意; "
        "SC-34 34a 扩为 9 成员 (500 KB env 行长键 / postgres 长口令与长用户名 / basic-auth 长口令 / JSON 键与冒号间空白串) 与 34b 扩为 14 成员 (含 500 KB 不带引号 kv 值三形、键与 = 之间 500 KB 空白串、JSON 键与冒号间 500 KB 空白串、export 后 100 KB 空白串); "
        "W14 时档新增 (i3-f / g / h) 300 KB 不带引号 kv 值三形 ≤ 5.0 (目标 3.21 / 3.10 / 3.31, 平方级写法 11.0 / 11.1 / 12.1); Tasks 1.8 坏实现清单加「分隔符可能很远的删除」; 待复议技术级 31 / 34。"
        "原型: _cut_pfx 一次 [[ =~ ]] 找前缀再 ${s:N} 切, 引号剥离改 ${V:0:1}。同族扫描: L3 里全部 14 处 #  ## % %% 站点逐处归类 (均为必然命中且靠前, 或短串), L1 的 12 处另列 (W10 / W9 有界或保证命中, 由 (g) / (f-hit) 时档把关), 见报告 §2。"
        "实测: 23 个线性成员在每进程 1 s 的 CPU 上限下全部仍检出 (cap_lin); 平方级写法在 500 KB 成员上整进程 CPU 9.99-19.4 s (bad_cost500: 9 个成员; 目标 1.2-1.9 s)。"
        "坏实现: val_quote_strip → 34b 三个长不带引号成员 (tl 复现的形态); val_kv_blank → 34b kv-blank-before-delimiter; val_json_colon → 34a json-secret-blank-before-colon + 34b json-blank-before-colon; "
        "val_url_at → 34a 三个 URL 成员; val_envline_eq → 34a env-line-long-key; val_far_delim (以上合集) → 34a 5 + 34b 5; val_quadratic → 34a 6 + 34b 7。"
        "另: export 后空白串成员最初取 400 KB, 实测 grep 自身对空白串约每字节 6 微秒、单进程近 3 s, 主机忙时目标原型自己越过 4 s 上限 (member_matrix 三并发下复现), 故取 100 KB (其余成员的取值类坏实现各有别的成员抓到)。")),
    dict(seat="tech-lead", label="m1", key="6ff1d962", disposition="fixed", where_or_evidence=(
        "W11「同一批包裹下的整环境转储」: env 只拦裸, printenv 与基线一致带变量名也拦 (基线 secret-guard.sh:867 对命令位置 printenv NAME 拦; :938 podman、:862-863 kubectl 带 --、:940 lxc 带 -- 的行也拦带名 printenv)。"
        "新行 22bx (baseline-failing, 11 个包裹逐个: 基线 0/11); Impact「新拦截」申报「包裹下带变量名的 printenv: 以往放行的容器内单变量核对由放变拦、改走 # guard:ack」; 待复议技术级 23 加备选 D (放行, 附 ack 疲劳论证, 取舍交 owner)。"
        "实跑 35 条命令基线 vs 目标 (logs/l1_wrapper_matrix.txt): 基线 docker exec c printenv HOME = 0, podman / kubectl -- 同形 = 2; 目标全 2。坏实现 printenv_bare_only → 22bx 0/11 红。")),
    dict(seat="tech-lead", label="m2", key="0033f2f4", disposition="fixed", where_or_evidence=(
        "待复议 23 / W11 / 22br 的引文改为 25898 的原文「正当核对（读长度、读 env 变量名）→ 拦」(saved issue Aria-221.md 评论 25898), 对应 `| wc` 与 `| cut -d= -f1`; "
        "锚定 `| grep '^X='` 的口径改写为来自基线 docker / kubectl 行与共用 BLOCKED 文案的 Acceptable filters (「前提是前缀安全; 对凭据名做锚定 grep 会打印其值」, 与基线共享的限制), 不再借 25898 的名义。"
        "其余 5 处 25898 引用逐处核对原文, 相符。(本键下另一件事 qa/m2 见下一条。)")),
    dict(seat="tech-lead", label="m3", key="684e9a24", disposition="fixed", where_or_evidence=(
        "W9「文档落点」: secret-hygiene.md §5.6 与 aria README 段各另写两件事 —— 保护边界 (覆盖面 = 内建 app.ini 行的读取器集 29 个打印型读取器 + python3 -c / node -e, 加 Read / Edit; 重定向读 / source / dd / xargs cat / find -exec 等写法、Grep 工具、Write、每条命令第 64 处之后的出现不受保护) "
        "与「条目选最短的特征子串」; SC-26 26c 关键词加 读取器 / Grep / 前 64 处 / 最短, 26e 加 SHORTEST (最短) / Grep / PostToolUseFailure。坏实现 (patch_docs --drop56=读取器 / Grep / 前 64 处 / 最短, --readme-drop=SHORTEST / 最短 / Grep / PostToolUseFailure) 各转红, 见 mut_summary_v6 doc 块。"
        "(本键下另一件事 ba/m1 见下方。)")),
    dict(seat="backend-architect", label="M1", key="6bd285b1", disposition="fixed", where_or_evidence=(
        "簇 Y。W14「其它耦合」加一条: 测试内 SC-8 的抽取装配 (先 source hook, 只带入闸门之上的函数; 再按锚点抽 risky_patterns / _sg_judge_one / _sg_per_segment_eval) 要求这两个函数直接或间接调用的全部函数 (含 _sg_core_eval、_sg_emit_blocked、_sg_vx_pass、_sg_ext_pass 及下游) 都定义在 source 闸门之上 "
        "(基线已在闸门下的 _sg_redact_echo 只产生被丢弃的回显文本, 保持原位); SC-8 的抽取方式 / 阈值 / 口径 / 档位一律不改 (测试内 SC-9a 直接运行新旧两份完整 hook 文件, 不经抽取, 实读 secret-guard.test.sh:1268-1300, 不受此约束)。新行 SC-30 30b (reverse-guard, 7 个运行, 探针内, 无需 git 历史): 复刻该装配, 五档命令各 rc 0、两条必拦命令 rc 2, 不得是 127; 基线 7/7。"
        "原型: _sg_core_eval / _sg_emit_blocked 定义在闸门之上; 坏实现 core_below_gate → 30b 0/7 (7 个运行全返回 127)。git 腿: 带 af87cae 历史的本地 clone (源 .git/modules/aria 只读), 基线与原型各跑既有套件 —— 基线 593/593; 原型 596/596 (含 SC-9a 对拍; 头注释计数随 3 个新增族探针同步为 602 / 596), "
        "SC-8 五档 new 13.4 / 20.5 / 16.6 / 20.0 / 55.1 ms/call 对天花板 100 ms (基线 5.5 / 11.2 / 6.4 / 9.5 / 38.1); 对照: 把两函数留在闸门下的原型在同一副本上五档 new 降到 0.7-0.8 ms/call (−97%)、套件 596/596 照样全绿 (logs/gitcopy_summary_v6.txt)。")),
    dict(seat="backend-architect", label="M2", key="df25d271", disposition="fixed", where_or_evidence=(
        "簇 AB。SC-19 加 19an (清单末行无换行: proj(nonl_one) 与 proj(nonl_two) 两形)、19ao (项目根含空格、括号、非 ASCII 字符, Bash 与 Read 两面)、19ap (CLAUDE_PROJECT_DIR 置空而 stdin cwd 有值); "
        "W9 格式段补「末行没有换行同样算一行」「对清单与项目根路径的所有展开一律加引号」, 位置段补「置空等同未设」。坏实现: ext_nonl (while read 丢末行) → 19an 红; ext_unquoted (路径展开不加引号) → 19ao 红; "
        "ext_unsetonly (只在未设时回落 cwd, 用 ${CLAUDE_PROJECT_DIR+x} 判) → 19ap 红。复核时发现 ext_unsetonly 的第一版变异是空操作 (只改了赋值那一行的默认值写法, 回落判断没动), 已改正后重跑转红。")),
    dict(seat="backend-architect", label="m1", key="684e9a24", disposition="fixed", where_or_evidence=(
        "W9 已知限制加粗: 完整路径条目对 `..` 回绕、`//`、`/./` 与 cd 后相对名的写法不命中, 只有最短的特征子串 (如文件名) 能覆盖; 文档要求「条目选最短的特征子串」(§5.6 与 README, SC-26 26c / 26e 关键词 最短 / SHORTEST, 与 tl/m3 同一处落点)。"
        "(本键下另一件事 tl/m3 见上。)")),
    dict(seat="backend-architect", label="m2", key="cfb2fb14", disposition="fixed", where_or_evidence=(
        "Tasks 1.12 加第 5 腿: L3 NUL 腿 (不作关单门: 结果记 handoff 并写进关单评论) —— 一条 Bash 命令用 printf 输出两条以 NUL 结尾的记录 (其中一条是运行时生成的合成值, 不读任何真实来源); 有 env-line / kv 告警即「NUL 以 \\u0000 到达 hook, W1 第二视图有效」, "
        "无告警即「前提不成立, 第二视图是空操作」, 两种结果都把 Impact 里 NUL 首次可检出那句从推测变为事实。W1 已知限制同步指向该腿。此项同时是主控裁定 7 的 NUL 腿一项。")),
    dict(seat="qa-engineer", label="M1", key="12a776ac", disposition="fixed", where_or_evidence=(
        "簇 AA。W11 正文写入语义: 命令位置字符集逐成员 (; & | ( ) { 反引号、控制字符含换行, 与基线 env / printenv 行 secret-guard.sh:867-868 同集)、pgrep / pstree 的 a 在簇内任意位置与任意操作数位置、ps 的 SysV -f / -F 任意位置与任意操作数位置、-o / --format 列表任一位置含 args|cmd|command、"
        "--no-trunc 在 ps / ls 之后任一位置、launcher 时长后缀 s m h d。SC-22 新增 3 个 baseline-failing 枚举行 22bt (9 成员, 每个一次独立运行)、22bu (18)、22bv (7); Tasks 1.8 坏实现清单加四类窄化 (命令位置字符集缺成员 / 簇内字母只认首位 / 列表关键字只认末位 / 操作数只认首个)。"
        "坏实现 (全部转红, 红的成员见 mut_summary_v6): anchor_drop:{amp, brace, backtick, pipe, paren_open, paren_close, semi} → 22bt 各 1 成员; pgrep_afirst → 22bu 3 成员, pgrep_firstonly → 2, pstree_afirst → 2, pstree_firstonly → 1; ps_F_lower → 3; ps_f_first → 2; ps_operand_first → 2; docker_notrunc_first → 2; launcher_dur_s → 3; ps_o_end → 22bv 5 成员。"
        "anchor_drop:semi 的第一版 22bt 成员表对它是等价变异 (简单的 `;` 被逐段判定的段切分吸收, 只有整串判定才靠字符集里的 `;`), 已增补整串成员 `true; ps aux &` 后转红。")),
    dict(seat="qa-engineer", label="M2", key="6bd285b1", disposition="fixed", where_or_evidence=(
        "簇 Y, 同 backend-architect/M1: W14 耦合清单新增 SC-8 抽取装配条、探针 30b 复刻装配 (rc 不得为 127)、原型把 _sg_core_eval / _sg_emit_blocked 放在闸门之上、「两个套件在原型上全部照过」类陈述写明运行条件 "
        "(W1 设计取舍: scan 套件 50/50; guard 套件在不带 git 历史的副本上 PASS ≥ 581 且至多一个环境性 FAIL —— 测试内 SC-13 头注释计数; 带 git 历史的真 checkout 上全绿含 SC-9a 与 SC-8 五档, 见 SC-29 / SC-30)。"
        "git 腿实跑数字与 core_below_gate 对照见报告 §5 与 logs/gitcopy_summary_v6.txt。")),
    dict(seat="qa-engineer", label="m1", key="c7bff9bd", disposition="fixed", where_or_evidence=(
        "SC-12 加 12p: 一个文本里既有被分类器排除的占位符 span (标记词 / 尖括号等) 又有真凭据 span, 日志 fp= 字段里被排除的 span 不占指纹项, 真凭据的指纹不被挤掉 (W4「只对被计数的 span 取」)。"
        "坏实现 fp_all_spans (对每个 span 先取指纹再分类) → 12p 红 (fp or tags differ)。")),
    dict(seat="qa-engineer", label="m2", key="0033f2f4", disposition="fixed", where_or_evidence=(
        "W2 已知限制「并入建议开单 7.8 / 7.9」悬空: 建议开单清单 7.8 正文加入 Forgejo / Gitea 容器环境变量覆写 FORGEJO__<section>__<KEY> / GITEA__<section>__<KEY> (键含小写段, 两层都不覆盖; W2 / W8 已知限制, SC-10 10m); "
        "W2 的引用改为只指 7.8 (7.9 是服务端配置候选名单, 不含此项); W8 的同一句本就指向 W2 与 SC-10 10m。(本键下另一件事 tl/m2 见上。)")),
    dict(seat="qa-engineer", label="m3", key="f410df76", disposition="fixed", where_or_evidence=(
        "Impact「覆盖关系」: 10CG/aria-plugin#154 的有意偏离由「两处」改为「三处 (见上)」, 与同节关单口径和 Tasks 1.13 一致 (a 长门槛 16 / b 指纹只记 ≥16 字符 / c [REDACTED 前缀值); 全文检索「两处有意偏离」为 0。")),
    dict(seat="code-reviewer", label="M1", key="ac42f607", disposition="fixed", where_or_evidence=(
        "簇 Z。W11 `:196` 改为准确的基线覆盖面, 引 secret-guard.sh:858 (docker: env / printenv 前空白、后空白 / 行尾 / 分隔符, 引号形与带名 printenv 不在内)、:862-863 (kubectl: 带 --, 或 env 后行尾 / |)、:938 (podman: env 前空白)、:940 (lxc: 要求 --); nomad alloc exec / pct exec / 不加引号 ssh / sh|bash -c / watch 基线无行。"
        "新的转储备选覆盖全部 11 个包裹, 含五个基线包裹的引号形、$(…) 形、重定向形与不带 -- 的 lxc 形 (22bo 逐个出行, 22by 另钉 $(…) 与重定向); 基线自己的写法留作 reverse-guard 22bw (基线 3/3); 删去 SC-22 `:291` 的「等价变异」论证。"
        "实跑 35 条命令基线 vs 目标核对每一条覆盖面表述 (logs/l1_wrapper_matrix.txt)。原型汇总里四个包裹的等价论证订正: remote_env_split:docker → 22bo 4 成员 (docker, docker compose 各 env / printenv), kubectl → 22bo 2 + 22by 2, podman → 22bo 2, lxc → 22bo 2, "
        "全部转红 (mut_summary_v6; 上一版汇总把它们判为等价变异, 该论证不成立)。另 ssh / sh / nomad / pct / watch 各转红 22bo; envrows_replaced (把五条基线行并进共享交替式并丢掉空白分隔的写法) → 22bw 10 个运行红 (reverse-guard 行的坏实现)。")),
    dict(seat="code-reviewer", label="m1", key="5d12116d", disposition="fixed", where_or_evidence=(
        "Tasks 1.7 改为: _sg_ext_path_pass 对小写化路径做字面子串比对 (W9 Read / Edit 面), 不经 _sg_core_eval; _sg_ext_pass 才把替换副本交内建的同一个 _sg_core_eval; _sg_core_eval 与 _sg_emit_blocked 定义在 source 闸门之上 (W14)。与 W9 对 Read / Edit 面的定义一致。")),
    dict(seat="code-reviewer", label="m2", key="ed638210", disposition="fixed", where_or_evidence=(
        "SC-9 9z 由 allow-guard 改为 known-limit (kv 左边界造成的漏报类, 不是误报守卫; 基线 26/26 不变); W2 已知限制加「大写键紧贴在小写前缀与下划线之后」(prod_API_TOKEN=<值>、export my_DB_PASSWORD = '<值>'); 待复议技术级 31 加备选 (把 _ 也算作 kv 左边界, 代价: 检出面与误报面扩大且未做语料普查, 9z 须随之改 baseline-failing)。"
        "坏实现 kv_left_boundary_off (去掉左边界) → 9z 红 (known-limit 行转红 = 有人放宽了左边界, 须同步已知限制与待复议 31)。")),
    dict(seat="code-reviewer", label="m3", key="eb6c5b5e", disposition="fixed", where_or_evidence=(
        "W9 语义补: 扩展拒绝时 Matched pattern: 写 `(extension) .aria/secret-guard.paths`, Command was: 与 Triggering segment: 回显原命令文本, 替身名 /etc/gitea/app.ini 永不出现; SC-25 加 25i (baseline-failing; 25f 的归一化会抹掉这几行, 所以单列; 基线未拦故无文本)。"
        "坏实现 ext_echo_subst (内建判定对替换副本的文案直接透传) → 25i 红。")),
    dict(seat="knowledge-manager", label="m1", key="f410df76", disposition="fixed", where_or_evidence=(
        "四处不一致逐一订正: (1) 覆盖关系「两处」→「三处」; (2) Why 表 SC-23 的「6/6」→ 由探针基线输出机算 (23a 1 + 23b 5 + 23j 4 个独立运行 = 10/10; mk_numbers6.py 解析, 不手填); "
        "(3) Impact 性能: 百分比与比值全部取自本轮 timing 原始输出 (无扩展文件 Bash 面 +24% / Read 面 +7%, 200 条目 +30 / +26 ms, 比值 1.60 / 1.55; W14 item 2 (f) 的 1.5 下界改纯比值 ≤ 3.0); "
        "(4) 19ak「另有两行」→ 四行 (secret-guard.sh:778 与 :1006-1008, 实读 grep 核对)。同族: Why 表与 W11 现状里的 SC-22「0/57」随新增的 5 个 baseline-failing 行改为占位符 0/62 (机算), 其余手写计数交 check_counts / xref_check 对账。")),
    dict(seat="knowledge-manager", label="m2", key="0c3c6ed4", disposition="fixed", where_or_evidence=(
        "探针行描述与注释里的版本相对词全部去掉 (22bp「v4 additions」、「(v2)」、「# v3:」等, patch_probe_v6.py 逐处带断言); 复核扫描 (\\bv[2-9]\\b、added in、previous design / round、this round、R1-R6、round N、earlier design) 余下只有 fixture 数据 (oauth2/v2.0 URL、credentials-v2) 与「wrappers added in W11」(W11 是 Spec 条款号, 非版本)。"
        "format_lint 的叙事检查扩到 v3-v6 与 writer-v6-proto 路径白名单, proposal 正文 0 处。因探针描述进入证据文件, 证据随之重生成。")),
    dict(seat="knowledge-manager", label="m3", key="a305732c", disposition="fixed", where_or_evidence=(
        "探针执行器逐行异常隔离: _safe(job) 包住每个行任务, 任一异常 (含 hook 调用超过 300 s 的超时) 只记该行为 no、实得 `error: <异常名>`, 其余行照跑。实测 (proto/iso_test.sh, 把单次超时压到 20 s、hook 对标记文本睡 30 s): 35e 红 `error: TimeoutExpired`, 其余 4 行 yes, 探针 exit 0; 验收模式 exit 4 (logs/iso_test.txt)。"
        "W 判定命令段与待复议技术级 34 同步写明。")),
    dict(seat="master-ruling-7", label="(f) 档判据", key="m7-f-tier", disposition="fixed", where_or_evidence=(
        "W14 item 2: (f) 改为 ≤ 3.0 的纯比值上界, 不带 100 ms 的绝对地板 (参考设计 1.60 / 1.55, 每条条目起一个 grep 的坏实现 13.2 / 9.4); (f0) 保留 1.5 × max(基线, 100 ms) (无扩展文件时基线只有几十毫秒, 固定开销把比值放大); 待复议技术级 34 写明理由与备选 (增量上界)。"
        "15 对复测 f / f0: 1.64 / 1.61 / 1.16 / 1.12 全 PASS (logs/timing_t6_f15.txt)。")),
    dict(seat="master-ruling-7", label="探针验收模式退出码与逐行隔离", key="m7-probe-exit", disposition="fixed", where_or_evidence=(
        "WPA_REQUIRE_ALL=1 下目标形态不成立 exit 4、缺腿 exit 3, 普通模式总是 exit 0 (探针 main 末尾); 单行超时只记该行 (见 km/m3); Spec「判定命令」段、Tasks 1.10、待复议技术级 17 / 34 同步; 目标原型带验收模式全量跑 rc=0。 logs/iso_test.txt 实测 exit 0 / 4。")),
    dict(seat="master-ruling-7", label="_sg_core_eval 的 locale", key="m7-core-locale", disposition="fixed", where_or_evidence=(
        "W9「语义」写明: _sg_core_eval 在调用方的 locale 下运行 —— 扩展里的 local -x LC_ALL=C 只作用于条目读取、匹配与切片, 在各自的命令替换里, 不带进判定函数 (原型即如此: 判定函数在命令替换的子 shell 里被调用, 导出的 LC_ALL=C 只在条目读取函数的局部作用域)。")),
    dict(seat="master-ruling-7", label="Tasks 1.13 归档门与 rule6_note dogfood 声称", key="m7-archive-gate", disposition="fixed", where_or_evidence=(
        "Tasks 1.13 写明: 归档 (D.2) 须在 1.12 / 1.13 勾选之后; 先对 Spec 目录跑 openspec-archive Step 1 的 --gate 看 d_payload; 该门只读 tasks / detailed-tasks 的勾选状态与任务行文本, 不读 proposal 的 rule6_note; 已勾选的任务行含 dogfood / benchmark / ab-test / deploy / 部署 / 上线 字样而无可链接产物路径 (门只认 ab-results / ab-suite 路径) 恒判 unverified, "
        "d_payload 非 null → 归档会自动创建 tracker issue (headless 亦然); d_payload 非 null 时先请 owner 授权开该 tracker; 不以改写任务行措辞躲过该门。依据 (实读): aria/skills/state-scanner/scripts/lib/spec_complete.py:1129-1140 (关键词与 ab-results / ab-suite 路径记号)、:1191-1198 (只遍历已勾选 [x] 的任务项); aria/skills/openspec-archive/SKILL.md 示例 5 (unverified_claims 非空无论 ack 与否都进 d_payload, Step 7 建 issue)。")),
    dict(seat="master-ruling-7", label="17d 读取器表之外的写法", key="m7-17d", disposition="fixed", where_or_evidence=(
        "SC-17 17d (known-limit) 的表外读取器成员加 expand / unexpand / shuf / split / csplit (26 个独立运行, 基线 26/26 放行); W8 已知限制同步列出。坏实现 add_reader:{expand, unexpand, shuf, split, csplit} (把该读取器收进读取器表) → 17d 各红 1 成员 (known-limit 行转红 = 已知限制被收口, 须同步 Spec)。")),
]
D.append(dict(seat="master-ruling-7", label="NUL post-ship 腿", key="m7-nul-leg", disposition="fixed", where_or_evidence=(
    "Tasks 1.12 第 5 腿 (不作关单门, 结果记 handoff 并写进关单评论), 与 ba/m2 是同一处改动 (tl / qa / km 三席同意); W1 已知限制与 Impact 的「NUL 首次可检出」两句指向它: 该腿的结果把推测变为事实 (有告警 = NUL 以 \\u0000 到达 hook; 无告警 = 第二视图是空操作, 行为同基线)。")))
assert len(D) == 27, len(D)
