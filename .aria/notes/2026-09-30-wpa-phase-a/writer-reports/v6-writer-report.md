# 返修报告: WP-A `secret-net-l3-and-bypass-paths` 定点修补 (post_spec 第 5 轮之后)

> 本报告随结构化输出返回, 不入仓。交付母本在实验目录 `deliver/` (`proposal.md`、`baseline_probe.py`、`baseline-evidence.md`、`dispositions.json`、`logs/`、`writer-v6-proto/`、`MANIFEST.sha256`)。叙述中文, 代码 / 命令 / 路径 / SHA 保留英文; 审计叙事只在本报告里, 不在 proposal 正文。

## 0. 概览

- **范围与依据**: 把 proposal v5 定点修补为 v6, 依据 owner 2026-10-07「接受当前结论 + 定点修补」与主控裁定 1-8。处置 R5 全部 21 条席位条目 (7 条 major、14 条 minor; `0033f2f4` 与 `684e9a24` 各对应两件不同的事, 分条处置) 与主控裁定 7 的 6 项非 finding 勘误, 共 27 条: **fixed 27, rejected 0, deferred 0**。owner 批准的唯一扩范围是簇 X (本 Spec 内补齐失败事件)。按主控裁定 8 留给 owner、执笔未处理的两项见 §8。
- **探针**: 454 行 / 35 组 SC (v5: 437 行 / 34 组); 新增 17 行 (12p、19an、19ao、19ap、22bw、22bx、22by、22bt、22bu、22bv、25i、30b、35a、35b、35c、35d、35e), 改写 16 行 (3b、9z、17d、22bo、22bp、26c、26e、26g、26k、28f、31d、32c、32d、32e、34a、34b; 其中 32c / 32d / 32e 只是被比对的行数变了)。基线形态 holds: baseline-failing 0/226、doc-sync 0/26、reverse-guard 82/82、allow-guard 70/70、known-limit 40/40、zero-regression 9/9; 目标原型 (带 `WPA_BASH32` 与 `WPA_REQUIRE_ALL=1`) 全部行 `yes` (30a 按设计 `n/a`), 目标形态 holds, 退出码 0。
- **每个新增或改写的行都有会让它转红的坏实现** (§5.4; 汇总 `writer-v6-proto/mut_summary_v6.txt`, `coverage_check6.py` 逐行核对相对 v5 新增或改写的 33 行全部覆盖): 本轮坏实现 95 个 (L3 / L1 / hooks.json / 文档类), 全部至少让一行转红, 未转红 0 个。前几版坏实现的回归重跑 601 个, 丢行 0 个 (明细与基准见 §5.4)。
- **体量**: proposal 214093 → 240156 字节 (+12.2%), 探针 222199 → 245249 (+10.4%), 证据 104900 → 113560 (+8.3%); 明细见 §6。
- **修补过程中自查发现并已改正的缺陷** (审计报告没有点名) 共 11 项, 见 §3.5; 仍然开放的见 §7。

## 1. 处置表

本表只留要点; 每条的改动位置、坏实现与转红的行、实测数字逐条写在结构化输出的 `dispositions` 字段 (与 `deliver/dispositions.json` 同源)。

| # | 席位 / 编号 | 键 | 处置 | 要点 |
|---|---|---|---|---|
| 1 | tech-lead / M1 | `66d6eb81` | fixed | 簇 X: hooks.json 增 PostToolUseFailure 注册, 提取链读 .error, 输出事件名随输入 (二进制 2.1.285 核实); W1 新条、SC-35 (35a-35e)、SC-31 31d / 31e 及 W8 / W10 / W11 / Impact / 7.7 / 待复议 33 / Tasks 1.12 第 6 腿与 1.13 同步; 12 个坏实现全红 |
| 2 | tech-lead / M2 | `755aab21` | fixed | 簇 W: 取值代码里的 # ## % %% 删除须常数次命中 (_cut_pfx 一次 [[ =~ ]] 加 ${s:N}, 单字符剥离 ${V:0:1}); W2 线性段、W4 kv 行注、SC-34 34a 9 成员 / 34b 14 成员 (500 KB)、W14 (i3-f / g / h); 7 个取值类坏实现按成员转红 |
| 3 | tech-lead / m1 | `6ff1d962` | fixed | W11 包裹下带变量名的 printenv 与基线一致一律拦: 新行 22bx (11 个包裹, 基线 0/11)、Impact 新拦截申报、待复议 23 备选 D (放行); printenv_bare_only 转红 |
| 4 | tech-lead / m2 | `0033f2f4` | fixed | 待复议 23 / W11 / 22br 的引文改为 25898 原文「读长度、读 env 变量名」; 锚定 grep 一句改述为来自基线 docker / kubectl 行与共用 BLOCKED 文案 |
| 5 | tech-lead / m3 | `684e9a24` | fixed | W9 文档落点: secret-hygiene.md §5.6 与 README 写保护边界和「最短特征子串」; SC-26 26c / 26e 关键词; 8 个文档类坏实现转红 |
| 6 | backend-architect / M1 | `6bd285b1` | fixed | 簇 Y: W14 耦合条 (SC-8 抽取装配要求被调函数在闸门之上)、探针 30b (7 个运行, 基线 7/7); git 副本上基线 593/593、原型 596/596, SC-8 五档 13.4-55.1 ms/call (天花板 100); core_below_gate 使 30b 0/7 |
| 7 | backend-architect / M2 | `df25d271` | fixed | 簇 AB: SC-19 19an / 19ao / 19ap + W9 格式 (末行无换行) / 位置 (置空) / 展开加引号; ext_nonl / ext_unquoted / ext_unsetonly 各转红 |
| 8 | backend-architect / m1 | `684e9a24` | fixed | W9 已知限制加粗: 完整路径条目对 .. // /./ 与 cd 后相对名失效, 只有最短特征子串覆盖; 文档要求最短子串 (与第 5 条同一落点) |
| 9 | backend-architect / m2 | `cfb2fb14` | fixed | Tasks 1.12 加第 5 腿: L3 NUL 腿 (不作关单门), W1 已知限制同步指向 |
| 10 | qa-engineer / M1 | `12a776ac` | fixed | 簇 AA: W11 写入语义 (命令位置字符集 / 簇内与操作数任意位置 / 列表任一位置 / --no-trunc / 时长后缀); SC-22 22bt (9) / 22bu (18) / 22bv (7) 三个枚举行; Tasks 1.8 加四类窄化; 17 个窄化坏实现全红 |
| 11 | qa-engineer / M2 | `6bd285b1` | fixed | 簇 Y 同第 6 条: 「套件全过」类陈述写明运行条件 (scan 50/50; guard 无 git 历史的副本上 PASS ≥ 581 且至多一个环境性 FAIL); 30b 与 git 腿 |
| 12 | qa-engineer / m1 | `c7bff9bd` | fixed | SC-12 12p: 被分类器排除的 span 不占指纹项; fp_all_spans 转红 |
| 13 | qa-engineer / m2 | `0033f2f4` | fixed | 建议开单 7.8 正文加入 FORGEJO__ / GITEA__ 容器环境变量覆写; W2 的引用改为只指 7.8 |
| 14 | qa-engineer / m3 | `f410df76` | fixed | Impact 覆盖关系「两处」改为「三处有意偏离」; 旧说法全文检索 0 处 |
| 15 | code-reviewer / M1 | `ac42f607` | fixed | 簇 Z: W11 的 :196 改准基线覆盖面 (:858 / :862-863 / :938 / :940), 删 SC-22 的 :291 等价论证; 22bo 取基线不拦的写法, 基线写法留作 22bw (3/3); 四个包裹及 ssh / sh / nomad / pct / watch 的坏实现各转红 |
| 16 | code-reviewer / m1 | `5d12116d` | fixed | Tasks 1.7: _sg_ext_path_pass 做字面子串比对, 不经 _sg_core_eval; 只有 _sg_ext_pass 交内建的 _sg_core_eval |
| 17 | code-reviewer / m2 | `ed638210` | fixed | 9z 改 known-limit (基线 26/26 不变); W2 已知限制加大写键紧贴小写前缀; 待复议 31 加备选; kv_left_boundary_off 转红 |
| 18 | code-reviewer / m3 | `eb6c5b5e` | fixed | W9: 扩展拒绝文案点名扩展并回显原命令, 替身名不出现; SC-25 25i; ext_echo_subst 转红 |
| 19 | knowledge-manager / m1 | `f410df76` | fixed | 四处不一致订正: 三处偏离、SC-23 10/10 机算、Impact 性能数字取自实测、19ak 四行; 同族 SC-22 0/57 改占位符 0/62 |
| 20 | knowledge-manager / m2 | `0c3c6ed4` | fixed | 探针行描述与注释里的版本相对词全部去掉 (patch_probe_v6 逐处带断言); 证据随之重生成 |
| 21 | knowledge-manager / m3 | `a305732c` | fixed | 探针逐行异常隔离: 单行超时或异常只记该行为 no 并写 error: <异常名>; iso_test.sh 实测 35e 红、其余 4 行 yes |
| 22 | master-ruling-7 / (f) 档判据 | `m7-f-tier` | fixed | W14 (f) 档改纯比值 ≤ 3.0 (参考 1.60 / 1.55), (f0) 保留 1.5 × max(基线, 100 ms); 15 对复测 f / f0 全 PASS |
| 23 | master-ruling-7 / 探针验收模式退出码与逐行隔离 | `m7-probe-exit` | fixed | 验收模式 exit 4 (形态不成立) / exit 3 (缺腿), 普通模式 exit 0; 判定命令段、Tasks 1.10、待复议 17 / 34 同步 |
| 24 | master-ruling-7 / _sg_core_eval 的 locale | `m7-core-locale` | fixed | W9 写明 _sg_core_eval 在调用方 locale 下运行 (LC_ALL=C 只作用于条目读取、匹配与切片) |
| 25 | master-ruling-7 / Tasks 1.13 归档门与 rule6_note dogfood 声称 | `m7-archive-gate` | fixed | Tasks 1.13 写明归档门行为 (只读勾选的任务行文本, 含 dogfood / benchmark 等字样而无 ab-results 路径恒判 unverified, 自动建 tracker) 与处置 (先请 owner 授权开 tracker, 不改写措辞躲门) |
| 26 | master-ruling-7 / 17d 读取器表之外的写法 | `m7-17d` | fixed | 17d 表外读取器加 expand / unexpand / shuf / split / csplit (26 个运行, 基线 26/26); add_reader:* 各转红; W8 已知限制同步 |
| 27 | master-ruling-7 / NUL post-ship 腿 | `m7-nul-leg` | fixed | Tasks 1.12 第 5 腿, 与第 9 条是同一处改动; W1 已知限制与 Impact 的「NUL 首次可检出」指向它 |

### 1.1 主控裁定 1-8 的落点

裁定 1 (簇 X) → 第 1 条; 裁定 2 (簇 W) → 第 2 条; 裁定 3 (簇 Y) → 第 6、11 条; 裁定 4 (簇 Z) → 第 3、4、15 条; 裁定 5 (簇 AA) → 第 10 条; 裁定 6 (簇 AB) → 第 7 条; 裁定 7 (minor 与非 finding 勘误) → 第 4、5、8、9、12-14、16-27 条; 裁定 8 (只改点名位置与同族兄弟位置、不新增机制、净增长尽量小) → 全表, 体量见 §6, 留给 owner 的两项见 §8。

## 2. 同族扫描清单

机械部分由 `writer-v6-proto/family_scan.py` 生成 (`logs/family_scan.txt`), 其余是实跑矩阵 (`logs/l1_wrapper_matrix.txt`、`logs/l1_sibling_matrix.txt`)。

1. **簇 X 的兄弟位置 (「交给 L3」类表述与事件假设)**: 对 proposal 全文检索「交给 L3 / L3 兜底 / 输出侧由 / 事后兜底」: 命中 10 行 (14 处)。已写明「成功与失败的调用都经 L3」的: Why 平台事实、W8 已知限制 (2 处)、W10 已知限制、W11 已知限制、待复议 5 (`systemctl status` 刻意放行)、待复议 33; Impact「覆盖关系」里 10CG/aria-plugin#203 一句原先漏了, 已补; 与失败调用无关、不改的: W1 NUL 设计取舍与待复议 21 里的「唯一事后兜底」(讲 NUL 视图)、W10 现状里「设计意图就是交给 L3」(对 10CG/aria-plugin#203 原文的转述)。事件假设的其它落点: hook 头注释的契约行 (加 `"error":` 行, SC-28 28f)、SOT §5.1 的 secret-scan 行 (写两个事件, 26k)、CHANGELOG 草稿标记词 (`PostToolUseFailure`, 26g)、README 两语种 (26e)。hooks.json 里另一个 PostToolUse 注册 (`submodule-gate-telemetry.sh`, 遥测) 同样看不到失败的调用, 但它不是安全层, 不在范围; Out of scope 限定为「失败事件上的脱敏与 matcher 之外的工具」。
2. **簇 W 的兄弟位置 (`#` `##` `%` `%%` 删除)**: L3 原型里全部 14 个站点逐个归类 (`family_scan.txt` B): 3 处 `${x%$'\r'}` (短串, 工具名与事件名, 非工具输出)、`${V#\"}` / `${V%\"}` 共 4 处 (JSON 与 gcp 的值各一对; 模式保证值两端是引号, 一次命中)、`${span%%:*}` 两处 (cf / x-api-key 与 gcp, 在固定头名之后, 冒号在 ≤ 25 个字符内)、`${entry%%|*}` / `${entry#*|}` (基线的 tag 表条目, 常数)、`${matches_breakdown% }` 三处 (基线, 短串); 取值表里其余全部走 `_cut_pfx` (一次 `[[ =~ ]]` 加 `${s:N}`) 或 `${V:0:1}`。L1 原型比基线多 12 个站点: W10 的 `${s%%"$pat"*}` / `${rest%%"$m"*}` / `${s%"$m"}` 都在 `[[ == *"$pat"* ]]` 或正则命中之后调用 (分隔符必在), 串长被 W10 的 4000 字节与 16 × 8 上限封顶, 由时档 (g-a) / (g-b) 把关; `${line%%:*}` / `${line#*:}` 取 `grep -ob` 输出的偏移 (数字之后的第一个冒号); W9 命中路径的切片按偏移与长度取, 在 `LC_ALL=C` 下, 由 (f-hit) 与 34c 把关; W12 的四处 `${subj%%".environ…"*}` 外有 `[[ == *…* ]]` 守卫。这些 L1 站点不在簇 W 规则的字面范围 (「取值代码」= L3), 列此备查。Spec 文本里这类写法的出现点: W2 线性段 (改写)、W4 kv 行 (注)、W9 匹配实现 (已有「禁止 `${before##*[;&|]}`」)、W10 (已有「余量按长度取」); 探针里每个站点都有 34a / 34b 成员 (成员 ↔ 站点矩阵见 `logs/member_matrix.txt`: 每个取值类坏实现至少被 1 个成员抓到)。
3. **簇 Y 的兄弟位置 (测试内抽取装配)**: 在 `secret-guard.test.sh` 里 `source "$HOOK"` 的位置共 3 处: `sts_case` (`:74`) 与 `split_case` (`:93`) 只调 `_sg_safe_to_split` / `_sg_split_top` (闸门之上、本 Spec 不动); SC-8 新侧抽取 (`:1771-1775`) 是唯一依赖函数位置的装配; SC-9a 直接运行新旧两份完整 hook 文件 (`:1268-1300`), 不经抽取。故 W14 与 30b 里的「SC-8 / SC-9a 的抽取装配」改为「SC-8 的抽取装配」并注明 SC-9a 不受约束 (审计席与主控裁定都写成「SC-8 / SC-9a」, 实读源码后改准)。SC-20 注入自测依赖的两段文本 (`wc` 那段、`local nl=$'\n'`) 逐字节不变, 沿用 v5 的耦合条。
4. **簇 Z 的兄弟位置 (「基线已拦」类论断)**: 对 W11 / SC-22 / Impact 里全部「基线已拦 / 基线放行」的论断, 凡带具体命令的都实跑核对 (35 条包裹命令 `l1_wrapper_matrix.txt` + 40 条兄弟位置 `l1_sibling_matrix.txt`): `ssh host 'env'` 基线拦、`ssh host env` 放行; `docker exec c printenv` 基线拦、`docker exec c printenv HOME` 放行; podman / kubectl `--` / lxc `--` 的带名 `printenv` 基线拦; `docker exec c python3 -m venv env` 基线拦 (W11 的文本提及误拦同样适用于基线); nomad / pct / 不加引号 ssh / `sh -c` / `bash -c` / `watch` 基线全部放行 (22ao-22ar)。全部与正文相符。`top` 的簇内 `c` 位置另测: `top -bc` / `-cb` / `-bcn1` / `-b -n1 -c` 都拦, `top -bn1c` 放行 (它不是合法写法: `-n` 吃走 `1c`)。
5. **簇 AA 的兄弟位置 (语义写了、行没钉)**: 对 W11 正文每个「任意位置 / 任一位置 / 逐成员」表述核对有没有成员行: 命令位置字符集 (22bt, 9 成员)、`a` 簇内与操作数位置 (22bu)、SysV `f` / `F` 簇内与操作数位置 (22bu)、`-o` 列表 (22bv)、`--no-trunc` (22bu)、launcher 时长 (22bu)、`/proc` pid 位置 (22bp、22F-22I)、包裹 × 转储 (22bo、22by)。`;` 在逐段判定下被段切分吸收, 只在整串判定下需要 (见 §3.5), 已增整串成员。
6. **簇 AB 的兄弟位置 (扩展输入面)**: 清单读取 (末行无换行)、项目根解析 (置空、含空格 / 括号 / 非 ASCII)、展开加引号 (`wc -c < "$f"`、`tr … < "$f"` 两处, 变异实现把三处不加引号, 19ao 红)、Read / Edit 面 (19ao 同行含 Read)、`cwd` 回落 (19ap)。
7. **其它同形**: 「SC-n 基线 a/b」类手写计数 (Why 表、W11 现状) 改为占位符机算 (`mk_numbers6.py`); 其余手写计数由 `check_counts.py` 与 `family_scan.py` D 节逐 SC 对账 (baseline-failing 行数: SC-22 62、SC-34 2、SC-35 3 等全部与探针一致)。

## 3. 交叉一致性检查

**3.1 新改条款之间**:

- 簇 X ↔ 其它: W1 新条 (hooks.json 注册 + `.error` + 事件名) ↔ SC-35 (35a / 35b 提取与事件名, 35c 成功路径不翻转, 35d 注册, 35e 误报守卫) ↔ SC-31 31d / 31e (注册面只多这一条、全文不含 `completeness_gate`) ↔ SC-3 3b (字符串形 `tool_response` 的 known-limit 不再把失败调用当未证实) ↔ W8 / W10 / W11 的「成功与失败的调用都经 L3」↔ Impact (新告警、接缝、同步面、覆盖关系) ↔ rule6_note 块 A 的可证伪锚点 (31d) ↔ Out of scope ↔ 7.7 (matcher 缺 Grep 一并写 PostToolUseFailure) ↔ Tasks 1.12 第 6 腿 / 1.13 披露 ↔ 待复议 33。
- 簇 W ↔ 其它: W2 线性规则 ↔ W4 kv 行注 ↔ 34a / 34b 成员 (9 + 14) ↔ W14 (i3-f / g / h) ↔ Tasks 1.8 的坏实现清单 ↔ 待复议 31 / 34; 成员尺寸 (500 KB、`export` 空白串 100 KB) ↔ 「2 倍以上余量」「线性写法不到 1 s」两句都有实测 (`cap_lin.txt`、`bad_cost500.txt`)。
- 簇 Y ↔ 其它: W14 耦合条 ↔ 30b (7 个运行) ↔ SC-30 怎么会红 ↔ Tasks 1.7 (`_sg_core_eval` / `_sg_emit_blocked` 在闸门之上) ↔ W9 语义里的 `_sg_core_eval` locale 句。
- 簇 Z ↔ 其它: W11 `:196` 与「同一批包裹下」条 ↔ 22bo / 22bw / 22bx / 22by / 22br / 22bs ↔ SC-22 的怎么会红 (删去等价论证) ↔ Impact 新拦截 ↔ 待复议 23 备选 D ↔ `mut_summary_v6` (四个包裹的坏实现全部转红)。
- 簇 AA / AB ↔ 其它: W11 正文 ↔ 22bt / 22bu / 22bv ↔ SC-22 baseline-failing ×62 ↔ Tasks 1.8 四类窄化; W9 格式 / 位置 / 展开 ↔ 19an / 19ao / 19ap ↔ SC-19 baseline-failing ×29 ↔ 怎么会红。

**3.2 新改条款与未改条款**:

- SC-26 26c / 26e / 26g / 26k 与 SC-28 28f 的关键词随新条款扩 (保护边界、最短、Grep、PostToolUseFailure、`"error":` 契约行), 文档类坏实现 (`patch_docs.py` 的 `--drop56=` / `--readme-drop=` / `--cl-drop=PostToolUseFailure` / `--sot51-nofail` / `--hdr-noerr`) 逐个转红; 未改的 26a / 26b / 26d / 26f / 26h-26j 与 SC-27 / SC-28 其余行不受影响 (全部 `yes`)。
- Impact「同步面」的 aria 文件数: hooks.json 加入后 aria 10 → 11 个 (Level 对账里的数同步); 主仓 16 个版本点、aria 6 个发版文件不变。
- 待复议 17 / 20 / 34 对「探针验收模式」「(f) 纯比值」「(i3-f / g / h) 5.0」的叙述与 W14 item 2 / 判定命令段一致。
- 31d 比较 hooks.json 的 `hooks` 对象 (注册), 顶层 `description` 字符串不在比较内; 原型把 `description` 改为点名新事件, 31d 保持 `yes` (证明该行不过度约束)。

**3.3 机械检查** (输出在 `deliver/logs/`):

- `check_counts.py` (proposal 各 SC 条目声称的类别计数对探针): 与 v5 相同的 5 条启发式提示 (SC-11 / SC-15 / SC-17 / SC-20 / SC-27: 条目里同一类别分两处写、或未写计数), 其余全部对上; 「共 N 行」「(N 行探针)」两处都是 454。
- `xref_check.py` (正文引用的行 id 对探针输出): 引用的 `SC-n id` 对 260 处, 「id 不在该 SC 下」0; 新增的 17 行里未被正文引用的: 无 (整体未被逐个点名的 160 个行是区间写法 `4b–4m` 一类的中间成员, 与 v5 同形)。
- `format_lint.py`: CR / 制表 / 带圈数字 / emoji / AI 署名 / 裸 issue 号 / 正文版本与审计叙事 / Status 行全部 0 (proposal 与探针); 探针另做一次人工扫描 (§3.5)。
- `refs_check.py` (Impact 关闭关键字三步检查的三态实跑)、`scan_all.py` (Rule #7 自扫: 全部交付文件当 Bash 输出与 Read 结果各扫一遍, 基线与目标两个 `secret-scan.sh` 都静默)、`readface_check.py` (SC-18 的 32 条路径各只命中一个基线备选): 见 `logs/`。

**3.4 机算的数字**: 全部时档 / 倍数 / 计数占位符 (`@NAME@`) 由 `mk_numbers6.py` 从原始输出解析, 共 232 个键, 正文里没有手填的时档数字; 本轮删去了 v5 遗留的两个无本轮来源的耗时数 (W2 线性段「16 KB 的值 36 s」「300 KB 的值 7 s」), 换成 `timing_bad6.txt` 与 `bad_cost500.txt` 的实测值。

**3.5 由本轮检查发现并已改正的接缝缺陷** (审计报告没有点名):

1. `ext_unsetonly` 的第一版变异只改了赋值默认值的写法, 回落判断没动, 是空操作 (19ap 不红); 改为 `${CLAUDE_PROJECT_DIR+x}` 判断后 19ap 红。教训同 memory 「adversarial-fixture」: 新坏实现先单独证明它与目标的行为确有差别 (`proto/emptyroot_try.py`)。
2. `anchor_drop:semi` 对第一版 22bt 是等价变异: 简单的 `true; ps aux` 被逐段判定的段切分吸收, 字符集里的 `;` 只在整串判定下起作用。增补成员 `true; ps aux &` (后台 `&` 使整条命令整串判定) 后转红。
3. SC-34 的 `export` 之后空白串成员最初取 400 KB: `stage_cost.py` 实测目标原型的 `grep -oE` 对该形态约每字节 6 微秒、单进程近 3 s, `member_matrix.py` 在三并发下复现目标自己越过 4 s 上限 (正确实现被判红; 原始输出留作 `member_matrix.400KB_under_load.txt`)。改取 100 KB (目标 < 1 s); 终版成员矩阵 `member_matrix.txt`: 目标 0 个不检出, 每个取值类坏实现恰好失败各自该失败的成员。
4. W14 与 30b 把 SC-9a 也算进「抽取装配」: 实读 `secret-guard.test.sh:1268-1300`, SC-9a 直接运行新旧两份完整 hook, 只有 SC-8 抽取; 已在 Spec、探针行描述、处置表里改准。
5. W1「两个套件在不带 git 历史的副本上全部照过」缺运行条件: 无 git 历史的副本上 guard 套件有且仅有测试内 SC-13 头注释计数一条环境性 FAIL (基线同样: 582 对 599 / 593), 与 SC-29 的口径一致; 已改为带条件的陈述。
6. 原型的 guard 套件头注释计数没有随 3 个新增的族探针同步 (599 / 593 → 602 / 596), 在带 git 历史的副本上第一次跑时 SC-13 红; `patch_tests.py` 与 `patch_docs.py` 现在同步头注释与 SOT 三处, 副本上 596/596 全绿。
7. 31d 原先比较整份 hooks.json, 实现者顺手更新 `description` 字符串即红; 改为只比较注册 (`hooks` 对象)。
8. Why 表与 W11 现状里陈旧的 SC-22「0/57」(现为 0/62) 改占位符机算; 覆盖关系里 10CG/aria-plugin#203 一句补「成功与失败的调用都经 L3」。
9. 覆盖核对 (`coverage_check6.py`: 相对上一版新增或改写的每个探针行都要被至少一个坏实现转红) 第一次只覆盖了其中的一部分: 3b (known-limit) 没有坏实现 → `string_response` (把字符串形 `tool_response` 也扫); 22bw (reverse-guard) 没有 → `envrows_replaced` (五条基线行并进共享交替式并丢掉空白分隔的写法); 35e (allow-guard) 的两个成员对任何实现都静默 → 增两个文档式占位符成员并加 `fail_noclassify` (失败路径漏掉分类器与白名单)。现为全部覆盖。
10. 文档类坏实现第一次并发跑 (3 个探针同时跑) 有 3 个标志在 27b / 27c 上出现与变体无关的红 (顺序重跑只红各自的行, `sc27_concurrency.sh` 四并发空载也全绿), 视为并发噪声; 最终汇总取顺序重跑的结果, 第一次的原始汇总作为 `doc_SUMMARY.first_run.txt` 一并交付。
11. 文档类坏实现的驱动脚本 (`docvariants6.py`) 有两处工具缺陷, 都在汇总里造成过错行: 非 ASCII 关键字的几个标志 (`--drop56=读取器` / `前 64 处` / `最短`) 共用同一个树目录名而在并发时互相覆盖; `--only` 合并时把带 `=` 的标志名还原错 (7 个标志的行丢成 0 行红, `--cl-drop=fp=` 同)。树目录名加标志哈希后缀、合并还原改为全部 `:` → `=`, 受影响的标志全部重跑, 终汇总里每个标志都红在它该红的行上。

## 4. 改变实现者动作的改动 (单列)

以下改动让「照 v5 写的实现」需要多做或改做某件事 (其余是文字订正、数字订正、证据重生成):

1. **hooks.json 多一条注册** (`PostToolUseFailure` → `secret-scan.sh`, matcher / 命令 / 超时同 `PostToolUse` 条目); `secret-scan.sh` 提取链末尾加 `.error`、输出的 `hookEventName` 取输入的 `hook_event_name` (缺省 `PostToolUse`; 先子串预检再 jq 确认); hook 头注释契约行加 `"error":`; hooks.json 不再是「零改动」, 同步面 aria 文件数 10 → 11, rule6_note 理由随之改写; 顶层 `description` 可更新。
2. **取值代码的写法受限**: 任何 `#` `##` `%` `%%` 删除都要常数次命中, 单字符剥离用 `${V:0:1}` 或 `[[ =~ ]]` (`${V#["']}` 一类写法在 300 KB 不带引号的值上越过 CPU 上限); 34a / 34b 的 500 KB 成员和 (i3-f / g / h) 时档会抓。
3. **`_sg_core_eval` / `_sg_emit_blocked` 以及 `_sg_judge_one` / `_sg_per_segment_eval` 调用的全部新函数定义在 source 闸门之上**, 否则测试内 SC-8 五档恒绿 (30b 在探针内抓)。
4. **W11 的覆盖面变宽**: 包裹下的 `printenv <NAME>` 由放变拦 (改走 `# guard:ack`; 「放行」是待复议 23 备选 D); 五个基线包裹的引号形、`$(…)` 形、重定向形、不带 `--` 的 lxc 形由放变拦; 命令位置字符集、簇内字母 / 操作数位置、`-o` 列表、`--no-trunc`、launcher 时长后缀按语义而不是规范拼写实现 (22bt / 22bu / 22bv)。
5. **W9 扩展入口**: 清单末行无换行也算一行; 清单与项目根路径的所有展开加引号; `CLAUDE_PROJECT_DIR` 置空等同未设; 拒绝文案的 `Matched pattern:` 写 `(extension) .aria/secret-guard.paths`、`Command was:` / `Triggering segment:` 回显原命令文本、替身名永不出现; §5.6 / README 要写保护边界与「条目选最短特征子串」。
6. **9z 由 allow-guard 改 known-limit**: 实现者若放宽 kv 左边界, 9z 转红并须同步已知限制与待复议 31。
7. **时档与探针参数**: (f) 档判据纯比值 ≤ 3.0; 新增 (i3-f / g / h) ≤ 5.0; 验收模式 (`WPA_REQUIRE_ALL=1`) 目标形态不成立 exit 4、缺腿 exit 3; 单行超时只记该行。
8. **Tasks**: 1.12 加第 5 腿 (NUL, 不作关单门) 与第 6 腿 (失败事件, post-ship 验证, 不作关单门); 1.13 加归档门处置与失败事件送达披露; 1.7 的 `_sg_ext_path_pass` 不经 `_sg_core_eval`; 1.8 的坏实现清单加四类窄化、失败事件、判定函数位置与「分隔符可能很远的删除」。
9. **测试套件头注释计数**: guard 套件新增 3 个族探针后 `Coverage` 头注释须同步 (原型 602 / 596) 并同步 SOT 三处; 这一条 v5 已要求, 本轮给出原型实测数。

## 5. 证据复跑记录

### 5.1 探针完整运行 (`deliver/logs/final_*`)

| 运行 | 树 | `WPA_BASH32` | 验收模式 | 退出码 | stdout sha256 前 16 位 | 字节 | stderr |
|---|---|---|---|---|---|---|---|
| final_A | 基线 | 有 | 否 | 0 | `a3603d2ee85cd552` | 106384 | 空 |
| final_B | 基线 (复现孪生) | 有 | 否 | 0 | `a3603d2ee85cd552` | 106384 | 空 |
| final_N | 基线 | 无 | 否 | 0 | `d6c30a27ed2e3e1b` | 106358 | 空 |
| final_T | 目标原型 | 有 | 是 (`WPA_REQUIRE_ALL=1`) | 0 | `1cd3e506e9653c50` | 103563 | 空 |
| final_TN | 目标原型 | 无 | 否 | 0 | `451632cfb849c692` | 103570 | 空 |
| final_C | 基线 (证据文件已就位) | 有 | 否 | 0 | `a3603d2ee85cd552` | 106384 | 空 |

内嵌进 `baseline-evidence.md` 的是 final_A (带 `WPA_BASH32`)。final_A / final_B / final_C 三份 stdout 逐字节相同 (final_C 是在最终证据文件就位之后重跑的, 证明基线输出与证据文件无关); final_N 与 final_A 只差 29h / 29i / 32c / 32d 四行 (`not-run`) 和末尾三行。基线形态 holds (baseline-failing 0/226、doc-sync 0/26, 其余类别全 `yes`); final_T: 目标形态 holds, 类别全满 (baseline-failing 226/226, doc-sync 26/26, reverse-guard 82/82, allow-guard 70/70, known-limit 40/40, zero-regression 9/9), 30a 按设计 `n/a`。

### 5.2 时档 (`logs/timing_summary_v6.txt`)

- 主机: Linux 6.17.9-1-pve, 4 核共享, 测量时 1 分钟负载 0.9–2.0; 每侧交错取最小整进程 CPU 时间, 每档 5 对 (f / f0 另做 15 对)。目标原型 19 个受判档 + 15 对 f / f0 的 4 档全部 PASS (`--judge`)。
- 目标 / 基线比值: (f) Bash 1.60、Read 1.55 (上界 3.0); (f0) 1.25 / 1.09; (f-hit) 2.01 / 2.04、对照 1.05; (g-a) 1.45、(g-b) 2.11 (2.5); (h2) 1.21 (1.5); (i1) 1.26、(i2) 1.18 (2.0); (i3-a..e) 1.37 / 1.47 / 1.24 / 1.75 / 1.19 (2.5); (i3-f / g / h) 3.21 / 3.10 / 3.31 (5.0)。
- 坏实现 (超界或活性断言失败): 每条目一个 grep 13.2× / 9.4×; `${s#*"$pat"}` 5.1× / 13.5×; 不设迭代上界 4.8× / 6.9×; 前缀删除取值 36.5× / 32.6×; `${V#["']}` 剥引号 11.0× / 11.1× / 12.1×; 逐出现点算阶段 20.7×; 逐出现点重判 65.5×; 无界 cli pattern 3.8×、无左边界 10.9×、无界 kv pattern 4.3×。
- SC-34 的 CPU 上限腿 (`cap_lin.txt` / `bad_cost500.txt` / `member_matrix.txt`): 23 个线性成员在每进程 1 s 的 CPU 上限下全部仍检出; 平方级取值写法在 500 KB 成员上整进程 CPU 9.99-19.4 s (目标 1.2-1.9 s), 每个取值类坏实现至少被 1 个成员抓到。

### 5.3 簇 Y 的 git 腿 (`logs/gitcopy_summary_v6.txt`)

带 `af87cae` 历史的本地 clone (源 `.git/modules/aria` 只读), 基线 `268da8f` 的工作树; 基线 = 原样, 原型 = 叠上原型的 hooks / hooks.json / 两个套件 (未提交)。bash 5.2.15, 4 核共享主机, SC-8 块开始时的 loadavg 如下; 天花板每档 100 ms/call (`max(100ms, old × 1.5)`), 阈值 / 口径 / 档位 / 抽取方式未改。

| 运行 | guard 套件 | scan 套件 | SC-8 开始时 loadavg | 五档 new ms/call (a)-(e) | 五档 old ms/call |
|---|---|---|---|---|---|
| 基线 | 593/593 | 49/49 | 1.14 1.61 2.03 | (a) 5.5 / (b) 11.2 / (c) 6.4 / (d) 9.5 / (e) 38.1 | 24.2 / 24.7 / 24.3 / 24.9 / 25.8 |
| 原型 (头注释计数已同步) | 596/596 | 50/50 | 2.98 5.74 8.05 | (a) 13.4 / (b) 20.5 / (c) 16.6 / (d) 20.0 / (e) 55.1 | 25.2 / 26.1 / 27.3 / 27.3 / 26.4 |
| 原型 (头注释计数未同步) | 595/596 | 50/50 | 1.81 4.06 7.45 | (a) 12.9 / (b) 19.4 / (c) 14.8 / (d) 19.5 / (e) 54.3 | 24.1 / 25.2 / 25.6 / 24.8 / 26.0 |
| 对照: 两函数留在闸门之下 | 596/596 | 50/50 | 2.01 4.91 8.10 | (a) 0.7 / (b) 0.8 / (c) 0.8 / (d) 0.7 / (e) 0.8 | 25.4 / 25.4 / 25.8 / 26.2 / 26.6 |

读法: 原型五档 new 比基线慢 (SC-8 抽取的 `_sg_per_segment_eval` 现含 W10 第二遍与 W9 扩展入口), 最慢的 (e) 档约天花板的一半; 全部在天花板内。头注释计数未同步的原型只有测试内 SC-13 一条 FAIL, 同步后 596/596; SC-9a 对拍随套件跑完 (含在计数里)。对照行复现了审计席的发现: `_sg_core_eval` 留在闸门之下时, 五档 new 降到约 0.7-0.8 ms/call (−97%), 套件照样全绿 —— 这正是探针 30b (0/7, 每个运行 rc=127) 要抓的。

### 5.4 坏实现汇总 (`writer-v6-proto/mut_summary_v6.txt`)

- 本轮坏实现 95 个 (L3 / L1 / hooks.json / 文档类), 全部至少让一行转红, 未转红 0 个; 分计: L3 15 个、hooks.json 6 个、L1 38 个、文档类 36 个。
- 回归: 上一版: 重跑 92 个, 87 个保住原先转红的全部行 (其中 0 个现在红的行更多), 丢行 0 个, 原先就是等价变异的 5 个 (现在 4 个转红); 上两版的: 重跑 118 个, 113 个保住原先转红的全部行 (其中 0 个现在红的行更多), 丢行 0 个, 原先就是等价变异的 5 个 (现在 5 个转红); 更早几版的: 重跑 391 个, 377 个保住原先转红的全部行 (其中 0 个现在红的行更多), 丢行 0 个, 原先就是等价变异的 14 个 (现在 0 个转红); 另有 29 个 `drop_extreader_*` 属被取代的设计, 只列不判。
- 簇对应: X = `fail_*` 5 个 (含 `fail_noclassify`) + `string_response` (3b) + `hooks_*` 6 个; W = `val_*` 7 个 + `fp_all_spans` + `kv_left_boundary_off`; Y = `core_below_gate`; Z = `remote_env_split:*` 9 个 + `printenv_bare_only` + `envrows_replaced` (22bw); AA = `anchor_drop:*` 7 个 + pgrep / pstree / ps / docker / launcher 窄化 10 个; AB = `ext_nonl` / `ext_unquoted` / `ext_unsetonly`; cr/m3 = `ext_echo_subst`; 17d = `add_reader:*` 5 个; 文档类 36 个标志。
- 等价变异与时档类 (无行转红, 逐个点名并给理由): 见汇总文件头; v5 汇总把 `remote_env_split:{docker,kubectl,podman,lxc}` 判为等价变异, 本轮订正 —— 它们现在各转红 22bo (kubectl 另转红 22by)。
- 回归基准是上一版终跑的同名计划同名标签 (`WPA_PREV_CAMPAIGN`), 要求「那时红的行现在必须仍红」。

### 5.5 其它实跑

- `proto/iso_test.sh` (探针逐行隔离): 把单次超时压到 20 s、hook 对标记文本睡 30 s, 35e 红且实得 `error: TimeoutExpired`, 其余 4 行 `yes`, 探针 exit 0; 验收模式 exit 4。
- 二进制片段 (`logs/binary_fragments.txt`, 2.1.285): 事件表 `Run after successful tool` / `Run after tool fails`; 失败事件输入 schema 无 `tool_response`、有 `error`; 输出 schema `{hookEventName, additionalContext?}`; harness 校验 `hookEventName`: `Hook returned incorrect event name: expected '…' but got '…'`; Bash 退出码语义 `isError:n!==0&&n!==1` 仅对 grep / rg / egrep / fgrep / findstr, robocopy `e<0||e>=8`。
- `family_scan.py`、`emptyroot_try.py`、`scale_try.py`、`stage_cost.py`、`sc27_concurrency.sh` 的输出同在 `logs/`。
- 交付目录 `MANIFEST.sha256` 覆盖 171 个文件 (sha256sum 格式, 相对路径), 定稿后 `sha256sum -c` 全部 OK; 对交付目录的 Rule #7 自扫 (`logs/scan_all_deliver.txt`) 0 个告警。

## 6. 字节数变化 (v5 → v6)

| 文件 | v5 (`6efb9b2`) | v6 | 变化 |
|---|---|---|---|
| `proposal.md` | 214093 | 240156 | +26063 (+12.2%) |
| `baseline_probe.py` | 222199 | 245249 | +23050 (+10.4%) |
| `baseline-evidence.md` | 104900 | 113560 | +8660 (+8.3%) |

增长的主要来源: 簇 X (W1 新条、SC-35、Why 平台事实、Impact / rule6_note / Tasks / 待复议 33 的同步) 约占编辑新增字节的 37% (按含失败事件字样的编辑统计, 编辑合计新增约 24 KB, 其余是数字占位符展开与头部); 其余是 SC-22 / SC-19 / SC-34 的新成员行与 W11 / W2 的语义写入、Tasks 的两个新腿与归档门说明。没有新增机制 (簇 X 除外); 证据文件的增量来自 17 个新增行与被改写的行描述。proposal 比 v4 → v5 的增量 (+30 KB) 小, 但仍是净增长, 见 §7 第 7 条。

## 7. 自报薄弱点

1. **失败事件上 `additionalContext` 能否端到端送达没有本机样本** (二进制里送达路径与 `PostToolUse` 同形): 只有 Tasks 1.12 第 6 腿能证, 它是 post-ship 验证、不作关单门; 关单评论照实披露。若不送达, 簇 X 退化为「失败的调用已注册、已提取、告警写日志但不进模型上下文」, 价值缩小。
2. **时档与 CPU 上限的余量随主机而变**: (g-b) 2.11 对 2.5 只有 1.18× 余量 (v5 已有); (i3-f / g / h) 3.21 / 3.10 / 3.31 对 5.0 约 1.5×; (f) 1.60 对 3.0 约 1.9×; SC-34 的线性成员 < 1 s 对 4 s 上限 4×, 平方级写法 ≥ 8 s 对 4 s 约 2×。忙主机上 (g-b) 是最先可能随机转红的判据; 判据是纯比值, 不随负载漂, 但小分母的噪声仍在。
3. **SC-34 成员尺寸是 AI 自裁的折中**: 500 KB (取值类坏实现 ≥ 8 s) 与 `export` 空白串 100 KB (目标自己的 grep 线性开销) 是在这台机器上实测定的; 更慢或更快的主机上 2 倍余量会变。已列入待复议 34。
4. **`printenv <NAME>` 在包裹下一律拦** 是对「与基线对直接执行面一致」的取舍 (主控裁定 4); 代价是容器内单变量核对改走 `# guard:ack`, 与 10CG/Aria#221 评论 25898 警告的 ack 疲劳同向。备选 D 已写进待复议 23, 取舍交 owner。
5. **回归基准只到上一版终跑**: 前几版 (v4 / v3) 的坏实现以上一版终跑结果为基准, 而不是各自首跑的结果; 上一版终跑本身已对首跑做过回归 (0 回归)。
6. **原型是文本替换产物**: 簇 W 的 `_cut_pfx` 写法、簇 X 的事件名预检只证明设计可达, 不是实现; 真实现者的写法可能在别的边缘上不同, 靠 Tasks 1.8 的非作者对抗 review 与探针行兜住。
7. **体量**: proposal 仍在增长 (§6), 单行 1-5 KB 的体例使席位只能抽样审阅 (R5 三席已指出); 本轮没有拆分或重写任何段落 (主控裁定 8), A.2 为每个 W 附实现者摘要的建议仍有效。
8. **文档类坏实现第一次并发跑有 3 个标志出现 27b / 27c 的并发噪声** (§3.5 第 10 条): 原因没有查到根 (四并发空载复现不了), 只能说明「并发三探针叠加忙主机」下套件行有极低概率偶发; 最终证据运行 (final_A/B/N 三并发) 若出现不一致须顺序重跑。
9. **3b / 22bw / 35e 的坏实现 (`string_response` / `envrows_replaced` / `fail_noclassify`) 是覆盖核对发现缺口后为满足「每个新行配坏实现」而补的**, 比其它行的坏实现更人为: 它们证明这些行不是恒绿、各有一个像样的反例, 不代表真实现者会犯这些错。
10. **v4 / v3 的 `plans_*` 沿用上一版归档**, 其中已移除设计不存在的变体 (上一版汇总点名); 本轮没有重新审阅这些移除。

## 8. 请裁项

**产品级 / 范围级:**

1. **研究笔记 `research/secret-guard.md:20` / `:371` 的前向去量化** (km 风险 1): 属 7.20 的产品级披露决定, 按主控裁定 8 未处理。
2. **「删除 W5」选项** (km 风险 2; W5 是 AI 增补, 10CG/aria-plugin#154 评论 19339 称告警措辞「现行已满足」): 按主控裁定 8 未处理, Spec 里也没有登记 (待复议 19 只涉 W5 是否带文件信息); 请 owner 决定是否要把它列成选项。

**技术级 (AI 已裁, 待复议; 已写进 Spec 的「待 owner 复议」技术级各条):**

3. 技术级 33: 失败事件纳入本 Spec 的具体写法 (同 matcher、`.error`、事件名预检加 jq 确认; 备选 B 列已知限制 / C 事件名写死不可行)。
4. 技术级 34: (f) 纯比值 ≤ 3.0; (i3-f / g / h) ≤ 5.0 与 300 KB; SC-34 长值成员 500 KB、`export` 空白串 100 KB; 验收模式 exit 4 / 3; 单行超时只记该行。
5. 技术级 23 备选 D: 包裹下 `printenv <NAME>` 拦 (默认) 还是放行。
6. 技术级 31 备选: 把 `_` 也算作 kv 左边界 (关掉 9z 的漏报类, 代价是检出面与误报面扩大、未做语料普查)。
7. **本轮 AI 自作主张、未被裁定点名的小决定** (Rule #10: 须请复议): (a) 31d 只比较 hooks.json 的注册、`description` 字符串自由 (并让原型更新它); (b) 22bt 增补整串成员 `true; ps aux &`; (c) 9z 由 allow-guard 改 known-limit 而不是放宽边界; (d) 两处「SC-8 / SC-9a」改为「SC-8」(实读源码); (e) 回归基准取上一版终跑; (f) 文档类坏实现取顺序重跑结果作最终汇总。

**流程提示:** 路径引用 `writer-v5-proto` 已全部改为 `writer-v6-proto`; 主控归档时须把 `deliver/writer-v6-proto/` 放到 `.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/`, 否则 proposal 头部与 W14 / SC 里的引用悬空。本轮没有写任何仓内文件, 没有 commit / push / fetch (簇 Y 的本地 clone 除外), 没有开 issue、发评论。
