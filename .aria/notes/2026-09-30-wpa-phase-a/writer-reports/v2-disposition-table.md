| 席位 | 编号 | 键 | 处置 | 改动位置 / 证据 |
|---|---|---|---|---|
| tech-lead | C1 | `e8d39a8a` | fixed | 簇 A: W3 整值占位形态; SC-7 7h/7i + SC-11 两面; 变异 wl_prefix/wl_contains/wl_nocase 红 |
| tech-lead | C2 | `7e0343bd` | fixed | W9 隔离 (`_sg_ext_*` 只经 `$( )`) + 内建先判; SC-20 20i-20m; 变异 ext_bare / ext_first 红 |
| tech-lead | C3 | `e600e931` | fixed | 簇 B: W12 单键读取归一化; SC-23 23a-23e; 变异 env_boundary 红 |
| tech-lead | M1 | `44b5bb44` | fixed | 真 bash 3.2.57; SC-32 32a/32b/32c + SC-29 29h/29i; 变异 b4 / vx_patsub 红 |
| tech-lead | M2 | `e2459206` | fixed | W11 纳入包裹下 env / printenv; SC-22 22ao-22ar + 22at 对照 |
| tech-lead | M3 | `d8e7b380` | fixed | W14 时档 (f)(g)(h) 入 SC-30; SC-31 31a <=150; 内建先判 (SC-20 20l/20m, SC-21 21v/21w); 变异 vx_interleave 红 |
| tech-lead | m1 | `5ac56a9f` | fixed | W11 取舍改以意图保持立论; 竞态句限定; 实读 aria/hooks 无 updatedInput |
| tech-lead | m2 | `efd4c1c5` | fixed | W8 已知限制 + W9 已知限制写明 Grep 工具读这些路径两层都不经过 (两层 matcher 均不含 Grep, hooks.json 冻结); 待复议 7.7 建议开单; Out of scope 记录 |
| tech-lead | m3 | `f410df76` | fixed | Impact 同步面: 16 版本点 + aria 6 文件 + 2 gitlink; 版本定级改引 §2.2; Tasks 1.11 |
| tech-lead | m4 | `68e80369` | fixed | 簇 D: W4 逐 tag 取值表; SC-12 12a-12j; 变异 fp_span 红 |
| tech-lead | m5 | `684e9a24` | fixed | W9 语义: 扩展条目与 W8 同一打印型读取器组 + `python3 -c` / `node -e` 源组组合, 对每一处出现判读取器; SC-19 19o (python3 -c 读列入路径) / 19r (第二处出现才在读取器之后) |
| tech-lead | m6 | `ab625935` | fixed | W9「失效是否对用户可见」段论证选保持静默 (PreToolUse 上 systemMessage 通道端到端未验证、热路径新增输出通道、无状态时重复提示), 并写明「超限整体忽略」的悬崖代价; 选项 B / C 列入待复议第 18 条 (主控裁定 3(e) 要求执笔论证) |
| tech-lead | m7 | `bdf4778c` | fixed | W14 陈旧清单加 secret-scan.sh:15-20; SC-28 28l |
| tech-lead | m8 | `60eea71e` | fixed | SC-26 限定到具体小节; 变异 docs_bad2 使 26a-26d 红 |
| backend-architect | C1 | `14b7e703` | fixed | 簇 A: W3 整值占位形态; SC-7 7h/7i + SC-11 两面; 变异 wl_prefix/wl_contains/wl_nocase 红 (同 tl C1) |
| backend-architect | C2 | `179045cd` | fixed | 簇 B: W12 单键读取归一化; SC-23 23a-23e; 变异 env_boundary 红 (同 tl C3) |
| backend-architect | M1 | `a3054a20` | fixed | W2 路径形字符级定义; 强制首字符生成器; 变异 loosepath/nopath/path_firstlower 红 |
| backend-architect | M2 | `d4bcaf7c` | fixed | W9 固定字符串单遍 + 200 条 / 32 KiB / 64 处上界; W14 时档与实测; 变异 ext_regex 红 |
| backend-architect | M3 | `7deac83f` | fixed | Impact 收尾口径默认理解 B; 10CG/aria-plugin#154 关单在 post-ship 复验后; 待复议 3 |
| backend-architect | M4 | `719ae05c` | fixed | SC-19 19j / 19k + SC-20 20h; 变异 ext_regex 使 19j / 20h 红 |
| backend-architect | m1 | `1b61303c` | fixed | W2 已知限制补全; SC-10 10g 三个独立运行; 已知误报类成文 |
| backend-architect | m2 | `369a8b32` | fixed | 簇 D: W4 逐 tag 取值表; SC-12 12a-12j; 变异 fp_span 红 |
| backend-architect | m3 | `b9d73d73` | fixed | W12 jq 已知限制: `map_values(length)` 对数值型字段回显数值本身 (jq length 取绝对值, 实测 -4821 → 4821), 「只出元数据」对数值字段不成立; Nomad Variable Items 恒为字符串, 不影响 10CG/Aria#221 的核对场景 |
| backend-architect | m4 | `60eea71e` | fixed | SC-26 限定到具体小节; 变异 docs_bad2 使 26a-26d 红 (同 tl m8) |
| backend-architect | m5 | `c941e4e1` | fixed | W8 名字组: 词内前缀允许 (16l `/srv/git-forgejo/app.ini`)、右边界 `[^[:alnum:]_]\|$` (16m `app.ini.bak` 被拦; 模板 / 示例也被拦, 成文并说明因备份与模板在命令文本上不可区分)、`cp` 后读副本 (17b) 与相对名 (21r) 写入已知限制 |
| qa-engineer | C1 | `f42265a1` | fixed | 簇 B: W12 单键读取归一化; SC-23 23a-23e; 变异 env_boundary 红 (同 tl C3) |
| qa-engineer | M1 | `ab6a3123` | fixed | SC-23 重写: 23d 要求 .env_prod / .env2 / .envprod / .envs 仍拦; 23g 钉非解释器现状 |
| qa-engineer | M2 | `8645b99f` | fixed | 簇 A + W3 已知限制改准确口径 |
| qa-engineer | M3 | `1c0bc16f` | fixed | 五个存活变异对应 7h / 4o / 11s 并复跑转红 (ent_on_old / wl_contains / wl_nocase / ent_digit / wl_envline) |
| qa-engineer | M4 | `634eac5c` | fixed | 簇 D: W4 逐 tag 取值表; SC-12 12a-12j; 变异 fp_span 红 |
| qa-engineer | M5 | `8e77d1ca` | fixed | 分类器 + SC-9 9v / 9w + SC-33 语料普查 (归因清单 2 个) + W7 |
| qa-engineer | M6 | `27f6c3ce` | fixed | 簇 C4: SOT §5.6 + README x2 + 头注释 + CHANGELOG; SC-26c/e/f/g; 同步面 |
| qa-engineer | m1 | `47c3900d` | fixed | Impact 收尾口径默认理解 B; 10CG/aria-plugin#154 关单在 post-ship 复验后; 待复议 3 (同 ba M3) |
| qa-engineer | m2 | `7d4fec1c` | fixed | W11 已知限制写明 Read 工具读 `/proc/<pid>/cmdline\|environ` 两层都不拦; SC-22 22au 钉现状 (Read 三个路径 exit 0, known-limit); 待复议 7.5 建议开单 |
| qa-engineer | m3 | `b976c610` | fixed | W2 路径形重定义 (不再要求小写首段) + SC-9 9w (`/Users/…`、`~/Library/…`、`/Users/…/.gh_token` 静默); 不带起头标记的相对路径值 (如 `Config/Prod/Db2Password`) 实测仍告警, 作为已知误报类成文 (原型实测) |
| qa-engineer | m4 | `d70f228c` | fixed | SC-23 23a 原文多行形态; SC-24 24o 钉 map(.name) / map(.key) |
| qa-engineer | m5 | `b5bbd88c` | fixed | SC-18 18f (有 ACK 无 nonce 仍拦) / 18g (有效一次性 ACK 放行); SC-19 19p (大小写不敏感: 大写路径 Read / 含大写条目 / 混合大小写命令) / 19s / 19t |
| qa-engineer | m6 | `6b5eb047` | fixed | 真 bash 3.2.57 + 32c; W10 的 3.2 引号语义钉住 |
| qa-engineer | m7 | `a0cb1abc` | fixed | SC-26 限定小节 + SC-28 新旧文本双判; 变异 docs_bad2 红 |
| qa-engineer | m8 | `9519ae32` | fixed | Impact 覆盖关系与 10CG/aria-plugin#154 关单口径逐条披露两处有意偏离: 值长门槛 16 (评论 19339 为 8; 8–15 位值不覆盖, SC-10 10c 钉住) 与指纹前 8 位只对 ≥16 字符记、逐 tag 取裸值 |
| code-reviewer | C1 | `e8d39a8a` | fixed | 簇 A: W3 整值占位形态; SC-7 7h/7i + SC-11 两面; 变异 wl_prefix/wl_contains/wl_nocase 红 (同 tl C1) |
| code-reviewer | M1 | `d9308fba` | fixed | 簇 B; .env2 / .envprod / .envs 在 23d 钉住 |
| code-reviewer | M2 | `53c140c4` | fixed | 簇 C4: SOT §5.6 + README x2 + 头注释 + CHANGELOG; SC-26c/e/f/g; 同步面 |
| code-reviewer | M3 | `9db51a43` | fixed | W11 /proc 放宽仅 environ\|cmdline; SC-22 22as / 22aj; 变异 proc_status 红 |
| code-reviewer | M4 | `2ce0049b` | fixed | 簇 D: W4 逐 tag 取值表; SC-12 12a-12j; 变异 fp_span 红 |
| code-reviewer | M5 | `d9986b27` | fixed | SC-13 13d 改为全串等值 (删去插入段后与基线文本逐字节相等, 追加任何句子转红); W5 同步; 变异 w5_append (在原文末尾追加处方性句子) 使 13d 转红 |
| code-reviewer | M6 | `44b5bb44` | fixed | 真 bash 3.2.57; SC-32 32a/32b/32c + SC-29 29h/29i; 变异 b4 / vx_patsub 红 |
| code-reviewer | m1 | `26c4c8b4` | fixed | W4 改引 `secret-guard.sh:626` (实读核对: :624 是 hash 赋值, `${hash:-unknown}` 在 :626) |
| code-reviewer | m2 | `60eea71e` | fixed | SC-26 限定到具体小节; 变异 docs_bad2 使 26a-26d 红 (同 tl m8) |
| code-reviewer | m3 | `5856b370` | fixed | SC-9 9h 改 24 位值 (只验键名封闭性)、9l / 9m 改 24 / 25 字符的变量引用 (只有值规则能让它们静默); 强制首字符生成器 `_gen_first` 覆盖首字符边界 (4n / 5l / 5m / 7h) |
| code-reviewer | m4 | `23cb20d9` | fixed | SC-20 20g + 各行同查 Bash / Read 面; W9 规定位置与隔离 |
| code-reviewer | m5 | `41434a8e` | fixed | W11 纳入 BSD pid 操作数 `ps 123` (COMMAND 列 = 完整命令行); SC-22 22am (基线 exit 0) |
| code-reviewer | m6 | `81da6556` | fixed | W4 新增「与 10CG/aria-plugin#92 的接缝」段: 只追加 fp= 字段、不起事件记录; fp 算法 / 16 字符门槛 / 值不进任何输出是 10CG/aria-plugin#92 事件 schema 应复用的口径 |
| code-reviewer | m7 | `a6304dd1` | fixed | SC-28 旧文本消失且替换在场; W14 清单 |
| code-reviewer | m8 | `78425781` | fixed | 同 tl m5: 扩展条目纳入 `python3 -c` / `node -e` 源组 (SC-19 19o) |
| code-reviewer | m9 | `6de9b7e2` | fixed | Impact 同步面补主仓 README.zh/ja/ko 各 3 处 (translated-from 标记、badge、Plugin Version 行) 与 root README 2 处; 复跑 m6-version-badge-match / i18n-readme-translation-currency |
| code-reviewer | m10 | `61c4987f` | fixed | rule6_note 块 A: n/a 是分类非免验; 待复议 8; 请裁项 2 |
| code-reviewer | m11 | `0061040b` | fixed | 同 ba m3: W12 jq 已知限制写明数值回显 (`-4821` → `4821`) |
| knowledge-manager | C1 | `e8d39a8a` | fixed | 簇 A: W3 整值占位形态; SC-7 7h/7i + SC-11 两面; 变异 wl_prefix/wl_contains/wl_nocase 红 (同 tl C1) |
| knowledge-manager | M1 | `5831f8c0` | fixed | SC-26 限定到具体小节; 变异 docs_bad2 使 26a-26d 红 |
| knowledge-manager | M2 | `ba98e41f` | fixed | Impact 同步面: 16 版本点 + aria 6 文件 + 2 gitlink; 版本定级改引 §2.2; Tasks 1.11 |
| knowledge-manager | M3 | `b73ab606` | fixed | 簇 C4 + Impact 五向申报 + SC-26g |
| knowledge-manager | M4 | `cf0ae932` | fixed | 全部研究笔记引用改指仓内 `.aria/notes/2026-09-30-wpa-phase-a/research/*.md` (别名 scan / guard / prec / cc + 节号, 三十余处, 已逐条核对节号存在); 头部声明承重判据只靠 `baseline_probe.py` 的 SC 行复现, 笔记仅作背景 |
| knowledge-manager | M5 | `846b21f8` | fixed | W13 新增 §3.8 并精确限定适用面 (长时进程), 短命令 argv 示例 (§3.1 / §3.2 / §3.4 / §3.5 / §4.4) 保持不变; SC-26h 钉 §3.1–§3.7 与 §4.1–§4.4 逐字节等于基线, SC-26a 锚定 §3.8 |
| knowledge-manager | M6 | `2779a016` | fixed | Impact 收尾口径默认理解 B; 10CG/aria-plugin#154 关单在 post-ship 复验后; 待复议 3 (同 ba M3) |
| knowledge-manager | m1 | `b7387216` | fixed | 同 qa m8: Impact 覆盖关系与关单评论披露两处有意偏离 (值长 16 vs 8; 指纹前 8 位只对 ≥16 字符) |
| knowledge-manager | m2 | `d8e2f426` | fixed | 头部「决策来源」重写: 第 4 项边界补「主仓 PR 的合并、删除远端分支」, 第 2 项写明不产出清单; W5 把「四张待轮换 issue (10CG/aria-plugin#203 / 10CG/Aria#221 / 10CG/Aria#170 / 10CG/Aria#136)」与凭据区分 |
| knowledge-manager | m3 | `8e1df30a` | fixed | Impact 版本定级改引 `version-management.md` §2.2, 写明 CLAUDE.md 只对 Skill 有明文; 先例 v1.47.0 (MINOR) 与 v1.65.4 / v1.66.3 / v1.66.4 (PATCH) 双向列出 |
| knowledge-manager | m4 | `852deadc` | fixed | Impact 接缝命令改用 guard_config_hooks 写法 (绝对路径 -C + rc 判据) |
| knowledge-manager | m5 | `381efd94` | fixed | proposal 不再含「执笔自报薄弱点」(审计叙事不入 Spec); 移入本返修报告「执笔自报薄弱点」一节; Status 行只写一句 Draft — post_spec 审计中 |
| knowledge-manager | m6 | `0f70cf57` | fixed | 头部「Level 对账」列三条判据 (LEVEL_GUIDE 跨模块 / proposal-minimal 的 >10 files / project.md 的 1-3 days) + 四份同型先例 + 一份反例; 待复议第 4 条 |
| knowledge-manager | m7 | `67e73dab` | fixed | W11 与 W13 已知限制记录 tight 族与 Acceptable filters 的不一致 (SOT §2.5 末尾注 + hook 头注释 residual gaps); 待复议第 2 条选项 C 含此收益 |
| knowledge-manager | m8 | `a1d19fe7` | fixed | W4 增 10CG/aria-plugin#92 接缝、W12 增 10CG/aria-plugin#131 关联; 待复议 7 要求开单前对 open issue 去重 (至少含 10CG/aria-plugin 的 131 / 138 / 139 / 141 / 142 / 143 / 144 / 146 号) |
| knowledge-manager | m9 | `b63b7640` | fixed | 头部新增「Rule #7 声明」(SC-15 15e / 15f 钉住自扫描静默); Tasks 1.10 写明 post-ship 腿取值规程 (运行时生成合成值并直接打印, 不写文件、不取自任何真实凭据, 因此不用 secret-leak-ok-explicit) |
| knowledge-manager | m10 | `a6304dd1` | fixed | SC-28 旧文本消失且替换在场; W14 清单 (同 cr m7) |
