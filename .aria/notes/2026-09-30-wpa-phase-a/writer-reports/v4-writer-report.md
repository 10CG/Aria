# WP-A `secret-net-l3-and-bypass-paths` proposal v3 到 v4 返修报告 (post_spec R3)

执笔: backend-architect 新派实例。交付母本目录: `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4/deliver/` (101 个文件, `MANIFEST.sha256` 100 条, 实跑 `cd deliver && sha256sum -c MANIFEST.sha256` 全部 OK; MANIFEST 自身 sha256 前 16 位 b35f132bc23ee2a3)。未写仓内任何文件、未 commit / push / fetch、未开 issue / 评论、未用 Agent 工具; 仓 HEAD 仍是 c3c7ece, `git status` 干净。

## 0. 结论

1. R3 的 35 条 finding (0C/12M/23m, 去重 10 个 C+M 键) **全部 fixed**: 0 条 rejected, 0 条 deferred; 每个席位编号都在第 1 节出现。主控 10 条裁定全部照办, 没有反证。
2. 三份母本: proposal 151287 -> 184049 字节 (425 -> 443 行); 探针 160820 -> 191479 字节 (2095 -> 2414 行), 行数 383 -> 411 (新增 28 行, 其中 baseline-failing 190 -> 202); 证据 79998 -> 92635 字节。
3. 探针形态 (终版三份文件上的实跑): 基线 `holds` (baseline-failing 0/202、doc-sync 0/25、reverse-guard 72/72、allow-guard 67/67、known-limit 35/35、zero-regression 9/9); 目标态 `holds` (带真 bash 3.2 与 `WPA_REQUIRE_ALL=1`: 410 行 yes, 30a 按设计 n/a)。
4. 坏实现: 本版 115 个 (111 个转红, 4 个等价变异逐个点名与论证); v3 的 420 个坏实现在 v4 原型上**回归复跑**: 406 个保持 v3 里红过的全部行, 14 个是 v3 就有的等价变异, **0 个退化**; 相对 v3 新增或改写的 40 行 (27 新增 + 7 改写 + 28a / 28e / 28f / 28j / 28k 等判据加强) 全部被至少一个坏实现转红 (33 行由计划内坏实现, 7 行由文档类手工坏实现), 0 行未覆盖。
5. 不引入新机制: 代码面新增只有 (a) L3 提取命令替换内一行 `tr '\000' '\n'`, (b) L1 W9 的引号掩码函数 `_sg_ext_mask` 与条目读取处的 `LC_ALL=C`, (c) 正则里的几个备选 (pid 记号、docker top、包裹 x env / printenv); 其余改动全是探针行、坏实现与文字。

## 1. 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或证据)

键 `cfb2fb14` 被四个席位编号共用, 但是两个不同的问题 (tl/m1、qa/m4、km/m2 = Tasks 1.12 的执行条件措辞; ba/m4 = Tasks 1.10 的 20g 在 root 下不可构造; qa/m5 的 20g 问题键是 `9ce750ed`); 键 `4447c607` 是两个不同的问题 (cr/m7 = W14 (f0) 时档覆盖; km/m3 = W14 的 K = 50); 键 `6ff1d962` 三个席位编号 (tl/m2、qa/m2 = 同族进程列举; cr/m2 = 文本提及误拦)。下面按席位编号逐条处置。

1. tech-lead · M1 · `4f713847` · fixed — W1 (改动 + 设计取舍 A' + 已知限制): 提取的命令替换内 `jq` 之后接一行 `tr '\000' '\n'`; Why 表 / SC-1 新行 1c (Read 信封) 与 1d (Bash 信封) 钉 NUL 分隔的进程环境形 (`env-line-secret-keyword=3`); 22au / 7.5 / 7.10 如实写成 L3 事后检出; 待复议 21。三态: 基线 4/4 静默 (1c / 1d 为 no) / 原型 yes / 坏实现 `nul_off` 使 1c、1d 转红 (writer-v4-proto/mut_summary_v4.txt, plan_v4_l3)。L1 对 Read `/proc/<pid>/environ` 的规则未加 (新拦截规则 = 新机制), 并入建议开单 7.5。
2. tech-lead · m1 · `cfb2fb14` · fixed — Tasks 1.12 执行条件改按 `.aria/probes/plugin-cache-currency.py` 的真实输出写: stdout 首行以 `OK ` 开头且 exit 0 才通过; `##SKIP##` (exit 0) 不是通过; `STALE` / `AHEAD` / `MALFORMED` 或 exit 非 0 = 未生效。实跑该探针: 首行 `OK installed=1.74.1 (scope=user) sot=1.74.1`, rc=0 (logs/plugin_cache_currency.out); 待复议 20 同步。
3. tech-lead · m2 · `6ff1d962` · fixed — W11 已知限制新增「同族的其它进程命令行列举」: 本地 `systemd-cgls` / `pidstat -l` / `w` / `busybox ps` / AIX 格式 `ps -o '%p %a'` 放行, 不加规则 (最小改动, 不新增机制); SC-22 22bh 逐项钉现状 (known-limit); 7.10 同步。tl 给的另一选项 (本地 systemd-cgls 也拦) 未取: 属新拦截规则。
4. backend-architect · M1 · `8d258b19` · fixed — 不执行不变量成文: W9 隔离条 (两个 hook 的全部新增代码共用: L1 的 W9 / W10 / W12, L3 的取值 / 分类 / 指纹) + W10「不执行不变量」+ W12 末句 + W14「其它耦合」; 诱饵行 SC-19 19ab (5 个运行 / 3 个诱饵)、SC-21 21z (5 种载荷)、SC-23 23i (2 种载荷); 同族 (L3 是不可信文本的另一个入口) 同批补 W2「不执行不变量 (L3)」+ SC-7 7n (5 种载荷 x Bash / Read 两种信封, 10 个独立运行)。坏实现 ext_eval (19ab 红: CANARY-EXECUTED)、ext_glob (19ab 红)、vx_eval (21z 红: 4/5 载荷创建诱饵)、w12_eval (23i 红 0/2)、val_eval (L3 取值后 eval 去引号, 7n 红 0/10) 全部转红; 待复议 25。
5. backend-architect · M2 · `8fbbee80` · fixed — W11 逐成员段 + W8 tight: SC-22 22bm (tight 逐成员, 91 个独立运行) / 22bn (87 个成员后接 wc -l 放行 + 2 = 89 个) / 22bq (launcher x 包裹 x 非 ps 程序 78 个) / 22bh (`/proc` 行不属 tight, 钉现状); SC-16 16r (app.ini tight 逐名字形态 11 个)。坏实现 tight_without (3)、tdrop_launch (15)、tdrop_remote (11)、tdrop_psalt (7)、tight_plainps、notight_proc、proc_nocredit、tight_ini_literal、notight_ini、launcher_ps_only、proc_tight 全部转红; 待复议 28。
6. backend-architect · M3 · `0a8380fd` · fixed — W9「语义」条: 阶段切分对引号感知 (`_sg_ext_mask` 在算阶段前把引号内的 `;` `&` `|` 与换行换成同长空格, 只删切分点); SC-19 19z (14 个独立运行: 6 形 x 内建与扩展两侧 + 2 形引号内 `|`) / 19aa (8 形: 7 形引号外仍切 + 引号内 `;` 之后真实的计数管道仍是 credit, 与内建一致)。坏实现 ext_nomask、ext_mask_{nosemi,noamp,nopipe,nonl} (各使 19z 红)、ext_mask_all (19aa 红) 全部转红; 待复议 24。
7. backend-architect · M4 · `ac42f607` · fixed — W11 `/proc` 条: pid 位置闭集 = `self` / `thread-self` / 数字 / `$$` / `$!` / 含 `*` 或 `?` 的 glob 记号 / `$name` / `${…}` / `$(…)`; 花括号、无 `*` `?` 的方括号类、反引号、路径归一化列已知限制; SC-22 22bp (10 个独立运行) + 22bh (逐项钉放行) + 22be / 22bf; 坏实现 drop_pid:2 / 6 / 7 (22bp 红)、pidtok_placeholders (22bf 红); 待复议 22。
8. backend-architect · M5 · `1c49d896` · fixed — W2「作用面 (闭集)」段: 第 2 步只作用于 6 个新 tag + json-secret-field, 第 3–5 步只作用于 6 个新 tag; SC-7 7k (既有键表 10 个键) / 7l (24 个独立运行) / 7m (9 个独立运行) / 7h / 7j。坏实现 step_on (30 个逐 (tag, 步骤) 对)、cls_all、pd_on_old、oldkey_drop (webhook_secret / encryption_key) 全部转红; 待复议 28。
9. backend-architect · m1 · `dcba7939` · fixed — W11: `docker container top` 与 `docker compose top` 纳入 (备选写成 `((compose|container)[[:space:]]+)?top`), SC-22 22bl 13 个拼写; `ps aux | grep -c X` 写入 W11「新增误拦」与 Impact 新拦截。坏实现 drop_dockerform:ctop 使 22bl 红; 基线 0 / 目标 2。
10. backend-architect · m2 · `6f503728` · fixed — W9 格式条: 长度按字节、「字母或数字」指 ASCII, 读取条目的 tr / sed / awk 固定 `LC_ALL=C`; SC-19 19ad (含 ASCII 字母数字的混合条目有效) / 19ae (纯非 ASCII 条目被跳过且静默, KNOWN-LIMIT); 待复议 24 给出备选。坏实现 ext_charlen (19ad 红)、ext_uniclass (19ae 红)。
11. backend-architect · m3 · `2f76563e` · fixed — Impact「提交页脚 / PR 描述的关键字」机械检查改为三步, 取生产者 `${PIPESTATUS[0]}` 并回显消费者 `${PIPESTATUS[1]}`, 判据 `rc=0,1` 且其前无输出 = 通过, 其它 = 没跑成, 引 10CG/Aria#199 的 detailed-tasks.yaml:342 原文; 三态实跑 writer-v4-proto/refs_check.py (v4 wrong: 0; v3 写法在 5 个跑坏态下真空通过); 待复议 29。
12. backend-architect · m4 · `cfb2fb14` · fixed — Tasks 1.1: 探针须由非 root 用户运行 (SC-20 20g 在 root 下不可构造; aria-runner 容器默认 root, 先降权, 如 `setpriv --reuid=<uid> --regid=<gid> --clear-groups …`; 降不了权上报 owner, 不得把 20g 的 n/a 当通过); 1.10 验收模式下 20g 不得 n/a 的条件由此可满足; 证据文件「怎么跑」记「本输出由非 root 用户产生」。
13. backend-architect · m5 · `f410df76` · fixed — Impact「issue 收尾口径」: 10CG/aria-plugin#154 关单评论须披露三处有意偏离, 新增 (c) `[REDACTED` 前缀值只在整值闭合时放行, 不闭合者仍检出 (SC-7 7j, 理由见 W3 保留判据); Tasks 1.13 同步「三处」。
14. qa-engineer · M1 · `eb350937` · fixed — 8 个存活坏实现逐一落行: 既有 json-secret-field 的 10 个键 -> SC-7 7k; 提取链的 tool_result 两分支 -> SC-2 2e / 2f; W4 阈值 -> SC-12 12n (15 / 16 字符两侧); 两个哈希工具回退腿 -> SC-12 12o; W9 首尾空白 -> SC-19 19ac。坏实现 oldkey_drop (2)、drop_extract (2)、fp_le16 / fp_lt20 / fp_lt13、hash_nosha256sum / hash_noshasum、ext_nostrip 全部转红; Tasks 1.8 列表同步。
15. qa-engineer · M2 · `05982c10` · fixed — 同 backend-architect/m3: Impact 关闭关键字检查三步 (范围非空 `rev-list --count` 须 >= 1 且 rc=0 -> 取 `${PIPESTATUS[0]},${PIPESTATUS[1]}` -> PR 文本非空前置), 判据 `rc=0,1`; refs_check.py 9 个场景 (含错起点 / 空起点 / 非仓路径 / 空文本 = 没跑成), v4 全部符合预期, v3 写法在其中 5 个真空通过。
16. qa-engineer · M3 · `28af0372` · fixed — W9 失败处理: 有效条目为零 (只含注释 / 空白行 / 条目全被跳过) = 扩展不生效, 且不得把空模式交给 `grep -F -f`; SC-20 20o / 20p / 20q (三种文件, 各 6 条命令, 金丝雀 Read / Edit / Bash 不变)。坏实现 ext_emptypat 使 20o / 20p / 20q 全红 (Read / Edit 全被拦)。
17. qa-engineer · M4 · `44b5bb44` · fixed — W2「字符类判定与 locale 无关」段 (新写 bash 层字符类用显式枚举或 POSIX 类, 不用范围; ERE 范围同基线写法不动, glibc < 2.28 列已知限制) + W14 其它耦合 + SC-32 32d (第二 locale 下对全部 hook 直调行 (361) 跑默认 bash 与真 bash 3.2 并与第一 locale 逐行比对; locale 缺则 localedef 构造, 构造不了即 n/a 上报) + Tasks 1.1 / 1.10 + 待复议 26。坏实现 ent_range (32d 红, 点名 9p / 10a / 10k)。
18. qa-engineer · m1 · `b298cc56` · fixed — SC-28 28c / 28d 的判据改为头注释不得出现任何 pattern / 类别总数字面 (数字 + 至多两个词 + patterns / tags / classes / forms); W14 陈旧表述段同步; 文档坏实现 --hdr-count (写入 `37 patterns, ~12 key-shape forms, 6 new tags`) 使 28c / 28d 红, 目标全 yes, 基线全 no。
19. qa-engineer · m2 · `6ff1d962` · fixed — 同 tech-lead/m2: W11 已知限制「同族的其它进程命令行列举」+ SC-22 22bh + 7.10 (w / systemd-cgls / pidstat -l 等放行, 钉现状)。
20. qa-engineer · m3 · `44510e65` · fixed — W4 的 12k 清单文字改为「3 个头 tag」(22 + 3 + 1 + 1 + 3 + 1 + 4 + 1 + 1 + 1 = 38), 与探针 W4 表 38 项一致 (SC-12 12k 实跑 38/38)。
21. qa-engineer · m4 · `cfb2fb14` · fixed — 同 tech-lead/m1: Tasks 1.12 执行条件按探针真实输出 (`OK ` + exit 0 才通过; `##SKIP##` 不是通过)。
22. qa-engineer · m5 · `9ce750ed` · fixed — 同 backend-architect/m4: Tasks 1.1 写明探针须由非 root 运行、root 下先降权 (`setpriv`), 降不了权按 Rule #10 上报, 不得把 20g 的 n/a 当通过; 探针行为不变 (root 下 20g = not-constructible, n/a, 验收模式 exit 3)。
23. code-reviewer · M1 · `05982c10` · fixed — 同 backend-architect/m3 与 qa-engineer/M2: Impact 关闭关键字机械检查 (三步 + `rc=0,1` 判据 + 与 10CG/Aria#199 `guard_config_hooks` 逐项对齐的引文), refs_check.py 三态; 待复议 29。
24. code-reviewer · M2 · `eb350937` · fixed — W11 整环境转储段: 11 个包裹 x {env, printenv} 共 22 个成员逐个出行 (SC-22 22bo); `sh -c 'printenv'` / `bash -c env` / `watch env` 改为**纳入** (v3 已知限制原文与原型相反, 已删, Impact 新拦截已申报; 待复议 23 给出收窄备选); 22bq 补 launcher / 包裹 x 非 ps 程序矩阵。坏实现 remote_env_split:{ssh,sh,watch,nomad,pct} 各使 22bo 红; docker / kubectl / podman / lxc 四个删除不可观察 (基线另有独立规则), 作为等价变异逐个点名。
25. code-reviewer · m1 · `467c8b54` · fixed — 同 backend-architect/M4: `/proc` pid 闭集纳入 `$$` / `$!` / `thread-self` / `[0-9]*` `1*` `1?` 一类 glob (22bp), 花括号 / 反引号 / 无 `*?` 方括号类列已知限制并钉 22bh。
26. code-reviewer · m2 · `6ff1d962` · fixed — W11 已知限制「新增误拦」成文: 远程 / 外壳包裹词不锚在命令位置 (沿用基线 env / printenv 行写法), `sshd` / `stopwatch` 子串与提交信息 / echo / 文档检索里先有包裹词再有进程表形态的文本被拦; Impact 新拦截申报; SC-22 22bj 扩为含包裹词的样例 (6 个独立运行, baseline-failing: 转红 = 有人收窄锚点); 坏实现 remote_anchored 使 22bj 红; 待复议 27。
27. code-reviewer · m3 · `5d12116d` · fixed — 同 tech-lead/m1: Tasks 1.12 执行条件改为首行 `OK ` + exit 0, 并按真实 token 列出 `##SKIP##` / `STALE` / `AHEAD` / `MALFORMED` / exit 非 0。
28. code-reviewer · m4 · `5e342bfd` · fixed — W14「secret-scan 计数」: 删去「目标态 K = 50」的具体数, 改为 K = 实跑总数 (含自检本身), SOT 的 secret-scan 计数同步为同一个数; 括号注明 50 只是未落 L3 用例的起草期原型的产物; SC-27 27b / 27c 以实跑总数为准 (判据未变, 基线 3/3 一致)。
29. code-reviewer · m5 · `f410df76` · fixed — 同 backend-architect/m5: Impact 10CG/aria-plugin#154 关单披露 (a) 门槛 16 vs 8 / (b) 指纹 >= 16 才记哈希 / (c) `[REDACTED` 仅整值闭合放行三处。
30. code-reviewer · m6 · `26e1a7a9` · fixed — W7 已知限制订正: `no-plan-fallback.md` 这类文件今天 `cat` (基线 Bash) 静默, W2 的 `kv-secret-assign` 之后 Bash 与 Read 都告警 —— 是 W2 带来的新增面 (已知误报类), 不是 W1 的; SC-33 归因清单 (测试夹具之外现 2 个: no-plan-fallback.md 与 MARKDOWN_TEMPLATE.md) 逐一点名。
31. code-reviewer · m7 · `4447c607` · fixed — W14 时档: (f0) 改为两面各一档 (无扩展文件 x {benign Bash 命令, benign Read 路径}), 并写明测试内 SC-8 只给 `_sg_per_segment_eval` 计时、不能代替这一档 (扩展入口的调用位置不由 Spec 规定); (g) 两档都跑 ((g-a) 4000 B / 8 x 300 B / 40 引用, (g-b) 16 x 100 B / 128 引用), timing.py 的档位 `g` = g-a、`gmax` = g-b, 默认参数与 W14 定义一致。
32. code-reviewer · m8 · `15da802b` · fixed — What 里的旧计数全部对账: W8 现状 SC-16 0/16、SC-18 0/6; W11 现状 SC-6 基线 0/11; 12k 枚举合计 38 (3 个头 tag); 另跑 check_counts.py / xref_check.py (逐 SC 类别数与行号引用 vs 探针 stdout) 与全文数字复核, Why 表 SC-2 行的「4/4」订正为 6/6 (2e / 2f 两个旧信封), 22bn 的残留旧数「79」订正为 87 + 2 = 89。
33. knowledge-manager · m1 · `a6304dd1` · fixed — SC-28 判据加强: 28l 要求两个半句 (`version-dependent behaviour` 与 `exposes no field to`) 都消失; 28b 另要求不含 `§1.3` (SOT 第 1 节只有 §1.1 / §1.2); W14 把 `§1.3` 改为 `§1` 写明。同类 (半截改写) 兄弟位置同批修: 28a (三行旧句两个片段都须消失)、28e (`argon2` 全文不得出现)、28f (无顶层 `"content":` 契约行); 另 28j / 28k 的 change-id 限定在 History 块 / 头注释块内 (只写在代码注释里不算)。文档坏实现 --hdr-half-l / --hdr-dangling / --hdr-half-a / --hdr-argon / --hdr-topcontent / --hdr-nohist 各使对应行红, 目标全 yes, 基线全 no; 待复议 30。
34. knowledge-manager · m2 · `cfb2fb14` · fixed — 同 tech-lead/m1: Tasks 1.12 执行条件 (首行 `OK ` + exit 0; `##SKIP##` 不得当作通过)。
35. knowledge-manager · m3 · `4447c607` · fixed — 同 code-reviewer/m4: W14 删去「K = 50 / SOT 同步为 50」, 改为 K = 实跑总数 (含自检), SOT 同步为同一数; 与 W1「新测试一律用真实信封」、Tasks 1.2、SC-29「总数 >= 49」、27b / 27c 自洽。

## 2. 主控 10 条裁定的落点

1. 簇 S 不执行不变量: W9 隔离条 (现为两个 hook 共用) / W10 / W12 / W14; 诱饵行 19ab / 21z / 23i, 外加同族的 L3 一侧 7n; 5 个 eval 式坏实现转红; 待复议 25。
2. 簇 T 引号感知阶段切分: W9「语义」条 + `_sg_ext_mask`; 19z (14 个运行) / 19aa (8 形); `ext_nomask` 与 5 个掩码缺项 / 过宽坏实现转红; 差分核对 `fuzz_mask.py` (见第 5 节); 待复议 24。
3. 簇 R 有效条目为零: W9 失败处理 + 20o / 20p / 20q; `ext_emptypat` 转红。
4. 簇 E locale: W2 字符类段 + SC-32 32d (第二 locale = 本机 `en_US.utf8`, 缺则 `localedef` 私有构造, 构造不了即 n/a 上报) + Tasks 1.1 / 1.10; `ent_range` 转红; 待复议 26。
5. 簇 P 关闭关键字检查: Impact 三步 + `rc=0,1` 判据 + 对齐 10CG/Aria#199 的 detailed-tasks.yaml:342 原文; refs_check.py 三态; 待复议 29。
6. 簇 Q NUL: 选「纳入」(一行 `tr`), 决定性行 1c / 1d; `nul_off` 转红; 待复议 21。
7. 簇 K `/proc` pid 记号: 纳入 `thread-self` / `$$` / `$!` / 含 `*` `?` 的 glob; 花括号 / 无 `*?` 方括号类 / 反引号 / 路径归一化列已知限制并逐项钉 22bh; 22bp; 待复议 22。
8. 簇 M: 7k / 7l / 7m (作用面)、22bm / 22bn / 22bo / 22bq (tight 与包裹)、16r (app.ini tight)、2e / 2f、12n / 12o、19ac (触及成员与阈值); 对应坏实现全部转红; 待复议 28。
9. 全部 minor: 第 1 节。
10. 方针 (不引入新 major / 不新增机制): 见第 0 节第 5 点与第 6 节; 凡只能靠新增机制的改为已知限制并写进待复议 (tl/m2 的本地 systemd-cgls、M1 的 Read 面 `/proc` 规则)。

## 3. 同族扫描清单 (修类不修例)

1. 内容形态类 (NUL / CR / 超长单行): NUL 已修; CR 已有 `# crlf-ok` 与 SC-29 的 crlf-shim / jq-crlf-guard 两个套件; 超长单行由每 tag 前 200 个 span 的上界 + (i) 档覆盖; 字符串形 `tool_response` 与 Edit / MultiEdit 仍是 SC-3 的已知限制。Tasks 1.8 增列「内容形态」类坏实现。
2. 执行类: 对两个 hook 的全部新增行扫 `eval` / `source` / `declare` / `printf -v` / `bash -c`: 0 处; `$(( ))` 与 `${s:off}` 的操作数只来自 `${#x}` 与 `grep -b` 的字节偏移 (读 `_sg_ext_pass` 解析代码核对), 并把「操作数只许整数」写进不变量。**本版新发现的兄弟位置**: 不变量与诱饵行原本只覆盖 L1 的 W9 / W10 / W12, L3 的取值 / 分类 / 指纹同样处理不可信文本 (工具输出 / 文件文本), 补 W2「不执行不变量 (L3)」与 SC-7 7n。
3. tight 拷贝类: claude-config (16p)、app.ini (16r)、进程表 (22bm / 22bn)、扩展条目 (19b / 19e / 19z / 19aa 最后一形) 全部逐成员出行; `/proc` 行不属 tight, 钉现状 (22bh)。
4. 引号感知类: W9 阶段切分 (本版修)、W10 赋值收集 (引号值 21j)、W12 归一化 (工作在内建切分之后的段上)。**本版新发现**: 掩码不止「多拦」—— 引号内的 `;` 不再截断阶段尾, 引号后真实的计数 / 哈希管道也成为 credit (`cat <路径> ";" | wc -l` 放行, 与内建一致; 实测基线式写法拦、掩码后放), 原文「只会多拦」过强, 已改写, 并给 19aa 增第 8 形钉住该方向。
5. pid 记号类: `/proc` 的全部读取形态 (基线 13 个读取器 22bc、新增 11 个 22bd、`<` 重定向、xargs 文件操作数、内联解释器 22bg、`task/<tid>` 22an) 共用同一个 pid 记号集合, 22bp 在五类入口上各出行。
6. 作用面类: W3 白名单 x tag (7m)、分类器 3–5 步 x tag (7l)、既有键表 (7k)、provider 前缀类 (7h / 7i)、W12 归一化 x 解释器 (23c / 23d / 23e)、W8 名字组 x 两个面 (18i)、launcher / 包裹 x 程序 (22bq)、credit x 家族 (22bm / 22bn)。
7. 枚举 / 边界类 (qa 请求的 W2 / W4 / W9「散文要求 -> 行」反向清点): 逐条核对 W2 (6 个 tag 的名表 / 关键字 / 旗标 / scheme / 值字符类 / 熵下限 / 路径形 / 点分链 / 200 span 上界 / 值长门槛)、W4 (第 9 字段 / 16 字符门槛 / 两个哈希工具 / 遍历序 / 10 项上限 / PEM 项 / 逐 tag 取值表 / 不进输出)、W9 (位置与回落 / 格式 / 只增不减 / 固定字符串 / 64 处出现点 / 200 条 / 32 KiB / 隔离 / 求值顺序 / 失败处理 / 文档落点), 每条都有行; 新补: 7k、2e / 2f、12n、12o、19ac、19ad / 19ae、20o–20q。
8. 文档半截改写类 (km/m1 的兄弟位置): 28b / 28l 之外, 同一形状还在 28a (三行旧句只要求第一个片段消失)、28e (`argon2` 可在别处重述)、28f (顶层 `"content":` 行可保留), 三处同批修; 28j / 28k 名「History 块 / 头注释块」却按整文件找 change-id, 原型自己的代码注释使 `--bad` 文档变体下 28j 假绿 (第一遍手工运行里发现), 已限定到注释块; 28c / 28d 判据从两个旧措辞扩为「任何数量字面」。28g / 28h / 28i 的旧文本是整行 / 整句, 无半截形态。
9. locale 类: 对两个 hook 的新增行扫 bash 字符范围: 0 处; 带范围的新增行全是 ERE 上下文 (grep -E / sed -E / `=~` / awk 正则, 与基线 pattern 同写法)。
10. 数字与引用类 (cr/m8 的兄弟位置): 对 proposal 的全部「N 个独立运行」「基线 a/b」「xN」「共 N 行」逐个对照探针输出, 又找到 2 处残留旧数 (Why 表 SC-2 行 4/4 应为 6/6; 22bn 的 79 应为 89), 已订正; 6 个 SC 条目的「xN」差异与 v3 逐项相同 (类别名未带计数的条目: 11x / 11y / 11z、18f / 18h、20g / 20l 等, 加总后与行数相符)。时档与掩码成本数字按终版原型重测并更新。
11. Tasks 引用外部工具输出类: 1.12 之外, 1.1、1.10、待复议 20 同步改写。
12. 关闭关键字类: 贯穿行、1.11、1.13 引用同一个检查; PR 草稿文本检查与提交信息检查同判据。
13. 文本提及误拦类: 22bj 覆盖含包裹词的文本提及; heredoc 起行形、`sshd` / `stopwatch` 子串形都已成文。另跑 76 条日常良性命令 (ps / pgrep / pstree / top / watch / sh -c / ssh / docker / nomad / /proc 只读元数据 ...) 对照基线: **0 条新增误拦** (`work/cases_benign_v4.py`)。

## 4. 改变实现者动作的改动 (主控重点核)

**甲. 代码面 (实现者须写不同的代码)**

1. W1: 提取的命令替换内, `jq` 之后追加 `tr '\000' '\n'` (一行)。
2. W2: bash 层字符类判定 (熵下限三类、路径形、点分链、`kv` 键前缀剥离) 不得用字符范围, 用显式枚举或 POSIX 类; 另: 取值 / 分类 / 指纹代码不执行被扫描的文本 (L3 不变量, 7n)。
3. W9: (a) 阶段切分前先掩码引号内的 `;` `&` `|` 与换行 (新函数, 引号 / 转义状态机同 `_sg_split_top`); (b) 读取条目的 tr / sed / awk 固定 `LC_ALL=C` (长度按字节、字母数字指 ASCII); (c) 有效条目为零时扩展不生效, 不得把空模式交给 `grep -F -f`; (d) 不执行不变量 (禁 eval 等, 禁未加引号遍历条目, 算术操作数只许整数)。
4. W10 / W12: 不执行不变量 (已是切片实现, 不加 eval)。
5. W11: (a) pid 位置备选增加 `thread-self`、`$$`、`$!`、含 `*` / `?` 的 glob 记号; (b) docker top 备选含 `container top` / `compose top`; (c) 包裹 x 转储的备选覆盖 11 个包裹 (含 `sh|bash -c`、`watch`、不加引号的 `ssh`), **v3 已知限制「`sh -c 'printenv'` 仍放行」反转为纳入**; (d) launcher / 包裹对 `pgrep` / `pstree` / `top` 同样生效; (e) tight 拷贝须与规则行同源 (只从一份去掉一个成员即漂移, 22bm 抓); (f) 接受包裹词不锚命令位置带来的文本提及误拦 (22bj)。

**乙. 测试 / 文档面**

6. SC-28 的头注释判据变严: 不得留半截旧句 (28a / 28b / 28e / 28f / 28l)、不得写任何数量字面 (28c / 28d)、`§1.3` 改为 `§1`、change-id 须在 History / 头注释块里 (28j / 28k)。
7. W14: secret-scan 计数 K = 实跑总数 (含自检), 不是 50; (f0) 两面各一档; (g) 两档。
8. Tasks 1.8: 非作者对抗 review 增列「内容形态」类; v4 另加七类坏实现。

**丙. 流程 / 验收面**

9. Tasks 1.1: 探针须由非 root 用户运行 (root 下先降权); 须准备第二个 locale (`WPA_LOCALE_B`, 缺则 `localedef` 构造, 构造不了即 n/a 上报)。
10. Tasks 1.10: 验收模式下 32d 与 29h / 29i / 32c / 12o / 20g 一样不得是 n/a。
11. Tasks 1.12: 执行条件按 `plugin-cache-currency.py` 的真实输出 (`OK ` 起头且 exit 0)。
12. Impact: 关闭关键字机械检查改为三步 (范围非空 -> 提交信息 -> PR 文本), 判据 `rc=0,1`; 10CG/aria-plugin#154 关单评论披露三处偏离。

## 5. 证据复跑记录

**环境**: Linux 6.17.9-1-pve, 探针由非 root (uid 1000) 运行; aria `268da8f` + standards `2bc1c4c` 的 `cp -a` 副本 (删去子模块 gitfile) 在 `exp/writer-v4/base/`; 目标原型树 `work/t4f` (`proto/build_full.sh` 生成); 真 bash 3.2.57 在 `exp/writer-v4/bash32/bash` (复用 v2 构建); HOME / TMPDIR 指向实验目录; 本机无 zsh; 第二 locale `en_US.utf8` 本机已装 (`localedef` 构造路径另验证可行: 构造出的 locale 同样使真 bash 3.2.57 的 `[[ QWERTY == *[a-z]* ]]` 为真)。主机负载 1.5–30 波动, 只看字节级相等与比值。

**终版三份文件** (全部证据运行都在它们之上): proposal.md 184049 字节 sha256[:16] `f98e719d6036b4f8`; baseline_probe.py 191479 字节 `7da0e53eef5d64da`; baseline-evidence.md 92635 字节 `4e0a94aac6e77058`。评估的 hook 指纹: 基线 `secret-guard.sh` `448b1f71a2af06d7`、`secret-scan.sh` `c5f53f7a164fa72e`; 目标原型 `d94ddf4d6906734f` / `cf2dd857823baf79`。

**运行** (`proto/final_runs.sh stage1|stage2`, 每次由 `proto/runprobe.sh` 先快照 spec 目录; stdout / rc / stderr 在 `deliver/logs/final_*`):

1. final_A: 基线树 + `WPA_BASH32`: rc 0, stderr 空, stdout **86047 字节, sha256[:16] `e588f9e8a57ed720`**, 基线形态 holds。
2. final_B: 同上的并发孪生: 与 A 逐字节相同。
3. final_N: 基线树, 不带 `WPA_BASH32`: rc 0, **86021 字节, `bd8327a7e971cc4e`**, 基线形态 holds `[4 leg row(s) not run]` (29h / 29i / 32c / 32d)。
4. final_C: 基线树 + `WPA_BASH32`, **终版证据文件已在位**: 与 A 逐字节相同 (证据文件内容不影响 stdout; 15g 在两种证据下都静默)。
5. final_T: 目标树 + `WPA_BASH32` + `WPA_REQUIRE_ALL=1`: rc 0, **83988 字节, `7360938f57ee82d0`**; 411 行中 410 行 yes, 30a 按设计 n/a, 目标形态 **holds**; 29a 50/50、29b 584/585 (唯一 FAIL = 测试内 SC-13 的无 git 伪影)、31a patterns=149、31b census 64 = 64、32c / 32d 在 361 个 hook-direct 行上一致、15e / 15f / 15g 静默、7n 10/10。
6. final_TN: 目标树, 不带 `WPA_BASH32`: rc 0, **83995 字节, `15b78d9592a87a0c`**; 执行的行全部 yes, 目标形态 `not established` (4 个腿行未跑, 设计如此)。
7. 基线形态结论: A / B / C / N 都是 baseline-failing 0/202、doc-sync 0/25、其余类别全 yes —— **holds**。证据文件由 `proto/mk_evidence.py logs/final_A.out logs/final_N.out spec/baseline-evidence.md logs/final_B.out` 生成, 内嵌块与 A 的 stdout 逐字节相等 (脚本断言), `build_deliver.py` 再断言一次且断言六次运行的快照与终版文件相等。

**变异与回归** (命令: `proto/run_final_campaign.sh v4`、`proto/run_v3_regression.sh`、`work/regress_compare.py`、`work/build_mut_summary.py`、`work/coverage_check.py`; 汇总 `deliver/writer-v4-proto/mut_summary_v4.txt` sha256[:16] 见 MANIFEST):

1. 本版 115 个坏实现 (L3 43、L1 W9 / W10 / W12 12、L1 W11 / W8 57、字节语义 2、bash 3.2 + 第二 locale 1): 111 个转红, 4 个等价变异 (`remote_env_split:{docker,kubectl,lxc,podman}`: 基线对这四个包裹下的 env 转储本就有独立规则, 删除不可观察; 22bo 对不被基线覆盖的 ssh / sh / watch / nomad / pct 各转红)。这一组在**终版探针**上跑 (快照与终版探针 0 行差异, `logs/probe_diff_campaign_vs_final.txt`)。
2. 回归: v3 的 420 个坏实现全部在 v4 原型上重跑, **只跑它们在 v3 里红过的那些行** (`work/mk_refined_v3_plans.py` 由 v3 汇总生成 `plans_v3r/`; 差分行 32c 保留原 SC 列表): 406 个保持全部红行, 14 个是 v3 的等价变异 (8 个小写 snake 键名、5 个声明前缀词、1 个解释器源组里的重复路径名), 0 个退化; 这一组的探针快照与终版只差 7n 与 28j / 28k 三处 (`logs/probe_diff_regression_vs_final.txt`, 46 行差异, 回归计划不选这些行)。
3. 覆盖: 相对 v3 新增或改写的 40 行全部被转红 (33 行由计划内坏实现, 7 行由文档类手工坏实现), 未覆盖 0 (`logs/coverage_check_final.out`)。
4. 手工运行 (`work/run_manual_runs.py` -> `manual_runs.txt`): 11 个文档坏实现 (--bad-sot / --bad / --bad-layer / --no-scope / --hdr-count / --hdr-half-l / --hdr-dangling / --hdr-half-a / --hdr-argon / --hdr-topcontent / --hdr-nohist) 各只使预期的 SC-26 / SC-28 行转红 (目标全 yes, 基线 14 行全 no); 27d 的头注释无自检变体 27c / 27d 红; 路径形字符类三个坏实现 (path_eq / path_plus / loosepath) 各 10 次运行 4n 与 5l 10/10 红、目标 0/10; SC-33 去熵下限的完整树: flagged 从 2 升到 7 (清单外 5 个文件) 转红; SC-15 负控: 往三份文件副本各追加一行运行时拼装的凭据形状, 目标 hook 下 15e / 15f / 15g 全红、基线 hook 下全 yes; 形态行负控 (缺腿时 `not established`, `WPA_REQUIRE_ALL=1` 为 rc 3)。
5. 差分核对 `work/fuzz_mask.py` (`logs/fuzz_mask.out`): 4000 个随机串 (引号 / 转义 / 分隔符字母表) 上, `_sg_ext_mask` 改动的位置与独立 oracle 的「引号内分隔符」逐位相同, 0 差异; 其中 2743 个被 `_sg_safe_to_split` 判安全的串上 `_sg_split_top` 的分段与 oracle 也相同, 0 差异 (顺带证明 oracle 编码了内建的状态机)。
6. 时档 (`deliver/writer-v4-proto/timing_summary.txt`): (f) Bash 0.049 -> 0.072 s、Read 0.042 -> 0.067 s (上界 0.15 s); (f0) 1.23 / 1.15; (g-a) 1.39、(g-b) 2.03; (h2) 1.25 (活性 ok); (i) 1.31 / 1.16; 坏实现: vx_quadratic 4.9x / 12.8x, ext_perentry 10.9–13.6x, no_cap 12.0x / 4.1x, vx_interleave (h2) 2.2x 且活性失败, ext_first (h2) 1.25x 且活性失败; 引号掩码成本 300 B / 1 KB / 4 KB 约 +10 / +20 / +100 ms (较空闲主机)。proposal W14 与 Impact 的数字已按终测更新。
7. 其它: `refs_check.py` (三态: v4 wrong 0; v3 写法在 5 个跑坏态真空通过); `.aria/probes/plugin-cache-currency.py` 实跑首行 `OK installed=1.74.1 (scope=user) sot=1.74.1` rc 0; `check_counts.py` / `xref_check.py` 对终版 A 的 stdout: 「共 411 行」声称相符, 210 个 `SC-n id` 引用 0 个悬空, 6 个 SC 条目的「xN」提示与 v3 逐项相同且可由未计数的 11x / 18f / 20g 等行解释。
8. Rule #7 与格式自扫: `work/scan_all.py deliver` 把 deliver/ 全部 100 个文件各当 Bash 输出与 Read 结果喂**基线与目标原型两个 secret-scan.sh**: 0 告警; 全部 LF、无裸 `#NN` 议题引用 (除 Rule #10 字样)、无圈数字 / emoji / AI 署名行; 头部 Level / Status / Created / Linked Issue 四行与 v3 逐字相同。

## 6. 执笔自报薄弱点

1. **原型不是实现, 坏实现是自构的 (同源盲区)**。R3 三个席位各自用非作者坏实现找到 v3 的存活者, 本版 115 + 420 个坏实现无法证明没有第四类。我本轮的几处额外发现 (28j 假绿、22bn 与 Why 表的旧数、L3 无不变量行、掩码「只多拦」说法过强) 都来自重读与对照, 不是变异跑出来的 —— Tasks 1.8 的非作者对抗 review 仍不可省。
2. **体量**: proposal +21.7%, 探针 +19%, 新增 28 行。R3 主控已指出「本轮约一半缺陷由上一版返修引入」, 本版的残余风险集中在新文字与新行之间的一致性 (尤其 SC-22 的成员数与段落); 缓解手段是 check_counts / xref_check / 全文数字清点 / 同族扫描, 但没有机械保证。
3. **验收前置变多**: 第二 locale、非 root、真 bash 3.2 都是验收机器的条件; 本机能降权的路径 (`setpriv`) 我只核对了选项存在, 没法在 root 下实测 (我以 uid 1000 运行)。
4. **回归复跑是精化的**: v3 坏实现只重跑「v3 里红过的行」(精确判据: 红过的必须仍红), 不是全量重跑; 它对「原本不红的行」不设判据 (无意义), 但与「全量重跑」不是同一件事。
5. **等价变异**: 本版 4 个 (docker / kubectl / podman / lxc 的 env 转储备选) + v3 的 14 个: 实现者误删它们探针看不见 (已逐个论证行为不变)。
6. **时档是单机比值**: (f) 比值 1.46–1.7 仍只靠 100 ms 地板通过, (g-b) 2.03 距 2.5 余量约 20%; 没有 Windows Git-Bash / macOS / BSD 实测 (沿用 R3 席位提到的未测面)。
7. **新增 / 反转的已知限制与误拦面**: 19ae (纯非 ASCII 条目静默跳过, 10CG Lab 是中文环境, 见待复议 24); 22bj 文本提及误拦面比 v3 更宽 (`sshd` / `stopwatch` 子串); `sh -c 'printenv'` 等由放行反转为拦截 (待复议 23)。76 条日常良性命令 0 新增误拦, 但那是样本, 不是证明。
8. **差分核对的范围**: fuzz 证明掩码与内建切分的「引号状态」一致, 没有覆盖 W9 阶段计算的其余部分 (命中偏移、reader 正则); 后者靠 19z / 19aa / 19r 等行。
9. **L3 7n 防的是「去引号捷径」**: L3 没有自然的 eval 写法 (分类路径零 fork), 这一行是对日后实现的预防, 不是现有缺陷; 若 owner 嫌多可删 (待复议 25 的备选)。
10. 证据运行在负载 10–30 的共享主机上, 单次约 25–30 分钟; 逐字节相等性与负载无关, 但主控复跑要留足时间 (探针超时设置不要按「约 5 分钟」估)。

## 7. 请裁项

**甲. 技术级 (AI 已裁, 已写入 proposal「待复议」21–30, 列出供复议)**

1. 21 W1 的 NUL -> 换行纳入; 22 `/proc` pid 位置闭集; 23 `sh -c` / `bash -c` / `watch` x env / printenv 纳入 (反转 v3 已知限制); 24 W9 的阶段切分与条目字节语义 (含「引号内 `;` 之后的计数管道是 credit」的方向); 25 不执行不变量与 4 个诱饵行 (含 L3 一侧 7n); 26 字符类与 locale 无关 + 32d; 27 W11 文本提及误拦; 28 tight 逐成员与分类器作用面逐 (tag, 步骤); 29 关闭关键字检查三步; 30 SC-28 判据扩到兄弟位置与位置范围。
2. 17 (bash 3.2 腿与第二 locale 腿缺省四行 n/a) 与 20 (post-ship 腿的执行条件) 的文字随之更新。

**乙. Rule #10: 我的自作主张 (请主控写进 handoff 复议)**

1. 回归复跑只跑 v3 红过的行 (第 5 节), 而不是全量。
2. 超出 35 条 finding 的同批改动, 理由都是「同族兄弟位置」: SC-28 的 28a / 28e / 28f 判据与 28j / 28k 位置范围; 19aa 第 8 形与 W9 掩码方向的文字订正; L3 不变量与 7n; Tasks 1.8 增列内容形态类; W9 算术操作数与「大小写不敏感仅 ASCII」两处措辞; Why 表 SC-2 与 22bn 的旧数订正; 时档 / 掩码成本数字重测更新; `fuzz_mask.py` 差分核对。
3. 没有新增 hook 机制 (见第 0 节第 5 点)。
4. 选「纳入」而不是「已知限制」的三处 (Q: NUL; K: `thread-self` / `$$` / `$!` / glob; `sh -c` x env), 理由见各待复议条。
5. 不交付 `tx_*.py` 一次性文本变换脚本 (依赖中间态, 不可重放); 交付的是可重放的原型 / 计划 / 汇总脚本。

**丙. 未采纳的席位备注 (不是 finding, 供主控或 owner 取舍)**

1. tl §6.8(b) / §7.5 与 km §6.8(b): SC-14 加 canary、W6 清理用记下的变量而不写 `rm -rf "$HOME"` 的机械判据 (cr / qa / ba 认为可不入 Spec)。未采纳; 备选: Tasks 1.3 加一句实现注意 + SC-14 预置 canary 与日志行数。
2. ba 风险 1 / km 风险 6: W5 的 `source` (取自 `tool_name`) 无形状校验, 建议 `case` 白名单。未采纳 (新代码, 现行 matcher 下不可达)。
3. ba 风险 2 / km 风险 7 / tl 风险 1: MINGW64 / macOS / BSD 未实测; 可在 10CG/aria-plugin#154 关单评论里披露「未在 MINGW64 验证」。未采纳。
4. km 风险 1: Layer 2 无人值守下新拦截的影响未在 Impact 申报; km 风险 3: 待复议 19 增列「删除 W5」选项; km 风险 5: Tasks 1.1 在冻结副本 (`git archive`) 上复跑; km 风险 2: Impact 引用精度。均未采纳。
5. qa 提醒: timing.py 只打印比值与活性、无判据与 rc (W14 已如实写明, 判据由文字上界给出)。未采纳。
6. qa / ba / km: 建议开单 7.1「约 1400 个空段」配方在公开 GitHub 镜像上的披露范围, 须 owner 在**首次推送前**裁定 (tl 倾向保留); A.1 认领心跳 (2026-09-30T17:57:13Z, TTL 24 h) 早已过期, 属主控例行维护。

## 8. 交付清单与落盘提示

1. 母本: `deliver/proposal.md`、`baseline_probe.py`、`baseline-evidence.md`、`dispositions.json` (35 行, sha256[:16] `3577046701288ed9`, 与本报告第 1 节一致)、`logs/` (六次终版运行的 stdout / rc / err 与其余证据日志, 共 30 个文件)、`writer-v4-proto/` (48 个文件: 补丁脚本、计划与回归计划、复跑脚本、汇总 `mut_summary_v4.txt` / `manual_runs.txt` / `timing_summary.txt`、README)、`MANIFEST.sha256`。
2. proposal 头部「证据位置」指向 `.aria/notes/2026-09-30-wpa-phase-a/writer-v4-proto/`: 落盘时把 `deliver/writer-v4-proto/` 放到该路径; 脚本内的绝对路径 (`EXP`) 须按本机改写 (README 已写)。
3. 主控复跑: 在 aria `268da8f` + standards `2bc1c4c` 的新副本上, 把 `proposal.md` / `baseline_probe.py` / `baseline-evidence.md` 放同一目录, `WPA_BASH32=<真 bash 3.2> python3 baseline_probe.py <副本>/aria` (非 root), 预期 stdout 86047 字节、sha256[:16] `e588f9e8a57ed720`, 基线形态 holds。