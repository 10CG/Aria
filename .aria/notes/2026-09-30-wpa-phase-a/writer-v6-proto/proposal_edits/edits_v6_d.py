# edits_v6_d.py -- rule6_note, Impact, Tasks, open questions, the two places that quote measured time.   Executed by apply_edits_v6.py (shares sub1 / after / NUM / t).


def repl_line(prefix, new, count=1):
    """replace the whole physical line that starts with `prefix`"""
    global t
    lines = t.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == count, (prefix, len(idx))
    for i in idx:
        lines[i] = new
    t = "\n".join(lines)


# ---------------------------------------------------------------- W8 / 7.7: hooks.json is no longer frozen
sub1("两层 matcher 都不含 Grep, 本 Spec 冻结 `hooks.json`, 结构上无法修, 建议开单)", "两层 matcher 都不含 Grep, 本 Spec 对 `hooks.json` 只增失败事件的一条注册、不改 matcher, 结构上无法修, 建议开单)")
sub1("(`scan §1.1`; `hooks.json` 在本 Spec 冻结, 结构上无法修)", "(`scan §1.1`; 本 Spec 对 `hooks.json` 只增失败事件的一条注册、不改 matcher, 结构上无法修)")
sub1("7. **两层 matcher 都缺 Grep** (PreToolUse `Read|Edit|Write|MultiEdit`、PostToolUse `Bash|Read|Edit|Write|MultiEdit`), 另缺 PowerShell:",
     "7. **两层 matcher 都缺 Grep** (PreToolUse `Read|Edit|Write|MultiEdit`、PostToolUse 与 PostToolUseFailure `Bash|Read|Edit|Write|MultiEdit`), 另缺 PowerShell:")
sub1("8. 未覆盖形状: 飞书 webhook URL、Nomad / Consul `SecretID`、封闭表外的 PascalCase 键如 AWS `SecretAccessKey` / `SessionToken` (`scan §5.6`; SC-10 10f)。",
     "8. 未覆盖形状: 飞书 webhook URL、Nomad / Consul `SecretID`、封闭表外的 PascalCase 键如 AWS `SecretAccessKey` / `SessionToken` (`scan §5.6`; SC-10 10f)、Forgejo / Gitea 容器的环境变量覆写 `FORGEJO__<section>__<KEY>` / `GITEA__<section>__<KEY>` "
     "(section 小写, 键含小写段, 两层都不覆盖; W2 / W8 已知限制, SC-10 10m)。")
sub1("`systemctl status` 刻意放行 (交给 L3)。", "`systemctl status` 刻意放行 (交给 L3: 成功与失败的调用都经 L3)。")

# ---------------------------------------------------------------- the two places that quote measured time
repl_line("  5. 原型实测",
          "  5. 原型实测 (Linux 6.17, 4 核共享主机, 测量时 1 分钟负载约 @LOAD_TIMING@; 每侧交错取最小整进程 CPU 时间, 每档 5 对; 数值随主机而变, 只给量级): "
          "(f) Bash @fB_b@ → @fB_t@ s、Read @fR_b@ → @fR_t@ s (比值 @fB_r@ 与 @fR_r@), (f0) @f0B_b@ → @f0B_t@ s 与 @f0R_b@ → @f0R_t@ s (比值 @f0B_r@ 与 @f0R_r@), "
          "(f-hit) @fha_r@ (出现一次) 与 @fhb_r@ (出现 64 次), 无出现的对照档 @fh0_r@, (g-a) @ga_r@、(g-b) @gb_r@, "
          "(h) @h2_r@ (全部放行的对照档 @h1_r@: 内建、W10 第二遍与扩展各判一遍, 不受 (h) 上界约束), (i) @i1_r@ 与 @i2_r@, "
          "(i3) 依 a–e 档为 @i3a_r@ / @i3b_r@ / @i3c_r@ / @i3d_r@ / @i3e_r@, (i3-f / g / h) 为 @i3f_r@ / @i3g_r@ / @i3h_r@。"
          "同法的坏实现: W10 余量用 `${s#*\"$pat\"}` 取, 在 (g) 上 @bad_vx_quadratic_g-a_r@× (满额档 @bad_vx_quadratic_g-b_r@×); "
          "每条扩展条目一个 grep 进程, 在 (f) 上 @bad_ext_perentry_fB_r@× 与 @bad_ext_perentry_fR_r@×; L3 不设迭代上界, 在 (i) 上 @bad_no_cap_i1_r@× 与 @bad_no_cap_i2_r@×; "
          "第二遍按段交错, 在 (h) 上 @bad_vx_interleave_h2_r@× 且活性断言失败 (内建已拦时它仍调用第二遍); 扩展先于内建在 (h) 上比值只有 @bad_ext_first_h2_r@ (没越界), "
          "由活性断言抓到 (内建已拦时扩展入口仍被调用, SC-20 20l 同样抓到); 逐出现点算阶段的手写实现, 在 (f-hit) 的 64 处出现档上 @bad_ext_v4stage_fh-b_r@×; "
          "对每个出现点各判一遍内建判定的实现 @bad_ext_perocc_judge_fh-b_r@× (活性断言同样失败: 内建判定函数被调用 65 次而不是 2 次); "
          "L3 取值用前缀删除写法, 在 (i3) 上 @bad_val_quadratic_i3-a_r@× (8 KB 头值) 与 @bad_val_quadratic_i3-e_r@× (既有 bearer tag 的 8 KB 值); "
          "kv 取值用 `${V#[\"']}` 剥引号的写法, 在 (i3-f / g / h) 的 300 KB 不带引号的值上 @bad_val_quote_strip_i3-f_r@× / @bad_val_quote_strip_i3-g_r@× / @bad_val_quote_strip_i3-h_r@×; "
          "参数名前缀无界的 cli pattern 在 (i3) 的 `-` 串档上 @bad_cli_unbounded_i3-b_r@×、无左边界的 @bad_cli_noleft_i3-b_r@×, 键名后缀无界的 kv pattern 在大写连续段档上 @bad_kv_unbounded_i3-c_r@×。")
repl_line("  - **性能**:",
          "  - **性能**: Read 面每次多一次扫描 (W1: 整进程 CPU 时间由约 @W1_BASE@ s 增至约 @W1_4K@ s; 60 KB 无命中文本约 @W1_60K@ s, 180 KB 稠密 INI 赋值约 @W1_180K@ s, 均在 hook 的 5 s 超时之内); "
          "进程调用延迟的判据与原型实测见 W14: 无扩展文件时 Bash 面约 +@PCT_F0B@%、Read 面约 +@PCT_F0R@% CPU 时间; 含 `$VAR` 引用的命令因 W10 第二遍约为基线的 @GA_R@–@H1_R@ 倍 "
          "((g-a) @ga_r@、(g-b) @gb_r@、全部放行的 (h) 对照 @h1_r@; 引用越密越近 2×; 内建先判, 已被内建拦下的命令不付第二遍); "
          "200 条扩展条目约 +@MS_FB@ ms (Bash 面) / +@MS_FR@ ms (Read 面) CPU / 次调用 (比值 @fB_r@ 与 @fR_r@); "
          "命令里出现列入的路径时扩展多付**一遍**内建判定, 约为基线的 @fha_r@ 倍 (4 KB 单行; 出现 64 处仍是 @fhb_r@ 倍: 与出现点数无关); 长单行 L3 输入的匹配与取值对长度线性 (W14 (i3))。")
sub1("约为基线的 @GA_R@–@H1_R@ 倍", "约为基线的 @ga_r@–@h1_r@ 倍")

# W1: the Read-scan cost numbers quoted in the W1 known limits
sub1("基线对 Read 因提取为空而提前退出, 约 0.142 s; 目标态 4 KB / 60 KB 无命中文本约 0.391 / 0.322 s, 180 KB 稠密 INI 赋值约 0.948 s,",
     "基线对 Read 因提取为空而提前退出, 约 @W1_BASE@ s; 目标态 4 KB / 60 KB 无命中文本约 @W1_4K@ / @W1_60K@ s, 180 KB 稠密 INI 赋值约 @W1_180K@ s,")

# ---------------------------------------------------------------- rule6_note
sub1("改动对象是两个 PreToolUse / PostToolUse hook 脚本、它们的测试、", "改动对象是两个 PreToolUse / PostToolUse hook 脚本、`hooks.json` 里 secret-scan 的一条 `PostToolUseFailure` 注册、它们的测试、")
sub1("SC-31 31d (`hooks.json` 零改动)", "SC-31 31d (`hooks.json` 只多一条 `PostToolUseFailure` 注册)")

# ---------------------------------------------------------------- Impact
sub1("`nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `bash -c` / `watch` 包裹下的裸 `env` / `printenv` (转储之后接锚定的 `grep` / `cut` 等行级过滤沿用基线 `docker|kubectl|podman|lxc exec … env` 的 credit, 仍放行: SC-22 22br / 22bs; 以往放行的日常核对形态不变);",
     "全部 11 个包裹 (`nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `bash -c` / `watch`, 以及基线只窄窄覆盖的 `docker` / `docker compose` / `kubectl` / `podman` / `lxc` 的 `exec`) 下的 `env` / `printenv` 转储 —— "
     "含引号形 `docker exec <c> \"env\"`、命令替换形 `x=$(kubectl exec <pod> env)`、输出重定向形 `kubectl exec <pod> env > 文件` 与不带 `--` 的 `lxc exec <c> env` (SC-22 22bo / 22by); "
     "**包裹下带变量名的 `printenv <NAME>`** (`docker exec <c> printenv NODE_ENV`、`ssh <host> printenv PATH`、`sh -c 'printenv HOME'`: 与基线对命令位置 `printenv <NAME>` 的处置一致, 以往放行的容器内单变量核对由放变拦、改走 `# guard:ack`; 「放行」是待复议第 23 条的备选, SC-22 22bx); "
     "转储之后接 `cut -d= -f1` / `wc` / `>/dev/null` / 锚定 `grep` 等行级过滤沿用基线 `docker|kubectl|podman|lxc exec … env` 的 credit, 仍放行 (SC-22 22br / 22bs);")
sub1("Read 工具结果首次被扫描 (读含逼真示例值的文件会告警);",
     "Read 工具结果首次被扫描 (读含逼真示例值的文件会告警); **失败的工具调用的错误文本** (Bash 非零退出等, `PostToolUseFailure`) 首次被扫描 (新注册; 该事件上 `additionalContext` 的端到端送达待 post-ship 验证, Tasks 1.12 第 6 腿);")
sub1("- **与 10CG/Aria#199 的接缝**: `aria/hooks/hooks.json` 与 `.aria/config.json` 不得出现字面 `completeness_gate` —— 本 Spec 两者都不改 (SC-31 31d / 31e 钉住 `hooks.json`);",
     "- **与 10CG/Aria#199 的接缝**: `aria/hooks/hooks.json` 与 `.aria/config.json` 不得出现字面 `completeness_gate` —— 本 Spec 不改 `.aria/config.json`, 对 `hooks.json` 只增 secret-scan 的一条 `PostToolUseFailure` 注册、增补内容不含该字面 (SC-31 31d / 31e、SC-35 35d 钉住 `hooks.json`);")
sub1("10CG/aria-plugin#154 全覆盖 (两处有意偏离见上;", "10CG/aria-plugin#154 全覆盖 (三处有意偏离见上;")
sub1("第 2 类变量间接: 部分修复 + KNOWN-LIMIT, 输出侧由 L3 兜底)", "第 2 类变量间接: 部分修复 + KNOWN-LIMIT, 输出侧由 L3 兜底, 成功与失败的调用都经 L3)")
sub1("(该 issue 的报告环境是 MINGW64)。", "(该 issue 的报告环境是 MINGW64), 并披露失败事件上 `additionalContext` 的端到端送达结果 (Tasks 1.12 第 6 腿: 送达 / 未送达 / 未验证)。")

# ---------------------------------------------------------------- Tasks
sub1("在带 git 历史的真 checkout 实跑 `secret-guard.test.sh` 记录 SC-30 基线 (含测试内 SC-8 五档);",
     "在带 git 历史的真 checkout 实跑 `secret-guard.test.sh` 记录 SC-30 基线 (含测试内 SC-8 五档, 同时记下 loadavg: 负载高时基线自己的 (e) 档就可能越过天花板, 须在空闲主机复跑);")
sub1("`_sg_ext_pass` / `_sg_ext_path_pass` 经内建的同一个 `_sg_core_eval` 判定; 不另写阶段切分;",
     "`_sg_ext_pass` 把替换副本交内建的同一个 `_sg_core_eval` 判定, `_sg_ext_path_pass` 对小写化路径做字面子串比对 (W9 Read/Edit 面, 不经 `_sg_core_eval`); `_sg_core_eval` 与 `_sg_emit_blocked` 定义在 source 闸门之上 (W14); 不另写阶段切分;")
sub1("另须对每个枚举集合做「删掉任一成员」的缺项类坏实现、对每个上界做「差一」的边界坏实现 (起草期",
     "另须对每个枚举集合做「删掉任一成员」的缺项类坏实现、对每个上界做「差一」的边界坏实现, 并覆盖: W11 的自然窄化四类 (命令位置字符集缺成员 / 簇内字母只认首位 / 列表关键字只认末位 / 操作数只认首个: 22bt / 22bu / 22bv)、"
     "失败事件只注册不读 `error` / 只读不注册 / 事件名写死 (35a–35d)、判定函数留在 source 闸门之下 (30b)、取值代码里分隔符可能很远的 `#` / `##` / `%` / `%%` 删除 (34a / 34b) (起草期")
sub1("目标形态行必须是 `holds`, 不得是 `not established`)", "目标形态行必须是 `holds`, 不得是 `not established`; 该模式下目标形态不成立时探针以 exit 4 退出, 缺腿 exit 3)")
sub1("hook 未生效时只得「No such file or directory」;\n",
     "hook 未生效时只得「No such file or directory」;\n"
     "  5. L3 NUL 腿 (**不作关单门**: 结果记 handoff 并写进关单评论): 一条 Bash 命令 `printf 'HOME=/x\\0JWT_SECRET=%s\\0' \"$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')\"` (合成值, 不读任何真实来源); "
     "有 `env-line` / `kv` 告警即「NUL 以 `\\u0000` 到达 hook, W1 的第二视图有效」, 无告警即「前提不成立, 第二视图是空操作」(两种结果都把 Impact 里 NUL 首次可检出那句从推测变为事实);\n"
     "  6. L3 失败事件腿 (**post-ship 验证, 不作关单门**: 结果如实写进关单评论): 一条 Bash 命令用 `python3 -c` 里 `secrets.token_urlsafe(32)` 生成合成值, 打印成一行 `JWT_SECRET = <值>` 后以非零状态退出 (`sys.exit(3)`), "
     "期望工具以失败返回、L3 告警且 additionalContext 含 `(tags: kv-secret-assign=1; source: Bash)`; 未送达则记「失败事件已注册、已提取, 送达未证」并照实披露;\n")
sub1("评论逐条披露三处有意偏离与验证范围 (未在 MINGW64 / macOS 验证) 后关闭;", "评论逐条披露三处有意偏离、验证范围 (未在 MINGW64 / macOS 验证) 与失败事件送达结果 (1.12 第 6 腿) 后关闭;")
sub1("会自动创建 tracker issue (headless 亦然), 而开 issue 不在一次性授权内",
     "会自动创建 tracker issue (headless 亦然), 而开 issue 不在一次性授权内。归档前先对 Spec 目录跑该技能 Step 1 的 `--gate` 看 `d_payload`: 该门只读 tasks / detailed-tasks 的勾选状态与任务行文本, **不读** proposal 的 `rule6_note`; "
     "已勾选的任务行含 `dogfood` / `benchmark` / `ab-test` / `deploy` / `部署` / `上线` 字样而行内没有可链接的产物路径时 (门只认 `ab-results` / `ab-suite` 路径, 本 Spec 没有这类产物) 恒判 unverified, `d_payload` 非 null, 归档会自动开 tracker issue (headless 亦然)。"
     "`d_payload` 非 null 时先请 owner 授权开该 tracker; 不以改写任务行措辞来躲过该门")

# ---------------------------------------------------------------- open questions
sub1("时档判据改为同次运行交错的整进程 CPU 时间之比 (上界 1.5 / 1.5 × max(基线, 100 ms) / 2.0 / 2.5 / 3.0 按档, 见 W14;",
     "时档判据改为同次运行交错的整进程 CPU 时间之比 (上界 3.0 (f) / 1.5 × max(基线, 100 ms) (f0) / 1.5 / 2.0 / 2.5 / 3.0 / 5.0 按档, 见 W14;")
sub1("理由: 10CG/Aria#221 评论 25898 把「读一个变量」与「列变量名」当正当核对; 同族 `/proc/*/environ` 与裸 `env` 也是默认 credit; 收紧会把基线已放行的形态改拦。",
     "理由: 10CG/Aria#221 评论 25898 列的正当核对是「读长度、读 env 变量名」(对应 `| wc` 与 `| cut -d= -f1`); 锚定 `| grep '^X='` 的口径来自基线 docker / kubectl 行与共用 BLOCKED 文案的 `| grep '^SAFE_PREFIX='` (前提是前缀安全; 对凭据名做锚定 grep 会打印其值, 是与基线共享的限制); "
     "同族 `/proc/*/environ` 与裸 `env` 也是默认 credit; 收紧会把基线已放行的形态改拦。")
sub1("备选 C: 把 env / printenv 备选收窄到 `ssh` / `nomad` / `pct` (22bo 少 6 个成员, 已知限制写「外壳里的 env 仍放行」)。",
     "备选 C: 把 env / printenv 备选收窄到 `ssh` / `nomad` / `pct` (22bo 少 6 个成员, 已知限制写「外壳里的 env 仍放行」)。"
     "备选 D (包裹下带变量名的 `printenv <NAME>`): 本 Spec 默认**拦** (与基线对命令位置 `printenv <NAME>` (`secret-guard.sh:867`) 及 podman / kubectl `--` / lxc `--` 行一致; 单变量也可能是凭据; SC-22 22bx); "
     "备选**放行** (把 `printenv` 限定为后只接分隔符或行尾, 并加一行 allow-guard) —— 好处: 容器内单变量核对 (`docker exec <c> printenv NODE_ENV`) 不被拦; 代价: 与基线对直接执行的处置不一致 (本地拦、外壳放), 且对凭据名会打印其值; "
     "而拦的代价是这类以往放行的核对改走 `# guard:ack`, 正是 10CG/Aria#221 评论 25898 警告的 ack 疲劳诱因 —— 取舍交 owner。")
sub1("备选: 不设上界 (覆盖更宽, 但平方退化可被一行超长输入触发); 更大的上界 (如 256: 漏报更少, 线性代价更高)。",
     "备选: 不设上界 (覆盖更宽, 但平方退化可被一行超长输入触发); 更大的上界 (如 256: 漏报更少, 线性代价更高); 把 `_` 也算作 kv 的左边界 (覆盖 `prod_API_TOKEN=<值>` 一类小写前缀加下划线的大写键, 上界仍在、仍线性; 代价: 检出面扩大、误报面随之扩大且未做语料普查, 9z 须随之由 known-limit 改为 baseline-failing)。")
t = t.rstrip("\n") + "\n" + (
    "33. **失败事件 (`PostToolUseFailure`) 纳入本 Spec**: 注册同一个 hook、同 matcher; 提取链末尾加 `.error`; 输出事件名取输入的 `hook_event_name` (先做子串预检、再用 jq 确认); SC-31 31d 只比较 hooks.json 的注册 (`hooks` 对象), 顶层 `description` 字符串可随之更新。"
    "备选 B: 不注册, 把失败调用列为已知限制 (W8 / W10 / W11 的「交给 L3」各加「仅对成功的调用」, Out of scope 与建议开单各加一条) —— 代价: 先打印后失败的命令 (`systemctl status` 对未运行单元退出 3、`curl -f -v` 遇 4xx 退出 22) 的输出没有任何事后兜底。"
    "备选 C: 只注册、事件名写死 `PostToolUse` —— 不可行: harness 按触发的事件校验 `hookEventName`, 不符即丢告警。失败事件上 `additionalContext` 的端到端送达待 post-ship 验证 (Tasks 1.12 第 6 腿), 结果写进关单评论。\n"
    "34. **W14 时档与探针的验收参数**: (f) 档判据取纯比值 ≤ 3.0, 不带 100 ms 的绝对地板 (参考设计的比值恒高于 1.5, 带地板的判据会退化成「基线 CPU 约 0.09 s 以下」这一主机属性); (i3-f / g / h) 取 300 KB 不带引号的 kv 值、上界 5.0 (固有开销约 3 倍, 平方级写法约 11 倍); "
    "SC-34 的长值 / 长空白串成员取 500 KB (`export` 之后的空白串取 100 KB: 该形态里 grep 自身对空白串的线性开销约每字节 6 微秒, 取到 400 KB 时单进程近 3 s, 主机忙时正确实现也会越过 4 s 上限), 使平方级取值写法离每进程 4 s 的上限有 2 倍以上余量; 探针在验收模式 (`WPA_REQUIRE_ALL=1`) 下目标形态不成立时 exit 4, 单个用例超时只记该行失败。"
    "备选: 把 (f) 改为增量上界 (如 ≤ 0.1 s 的 CPU 增量); 把 SC-34 的长值成员留在 300 KB (运行更快, 但平方级写法离上限只有 1.0–1.3 倍, 随主机快慢可能不转红)。\n")
