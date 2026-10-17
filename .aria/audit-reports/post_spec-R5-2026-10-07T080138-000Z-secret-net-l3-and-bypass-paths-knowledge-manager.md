---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-07T09:58:30.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 - knowledge-manager 席 (文档与规范一致性)

## 已实读文件

**被审对象 (v5, 提交 `6efb9b2`)**
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-449 行 (214093 字节, sha256 前 16 位 `cedbdfce05575891`, 与派单一致)。另用自写脚本生成 v4 (`b07f69a`) 到 v5 的逐词差异 (75 段改动), 全部读完。
- `baseline_probe.py` (222199 B, `cf331b4aa264a863`): 读 SC-19 / SC-22 / SC-26 / SC-28 / SC-31 / SC-34 区、`run_guard` / `run_guard_cpu_total` / `main` 执行器 (约 395-412、488-512、2080-2125、2200-2303、2440-2534 行) 与 6j / 22bp 行定义; 其余按行 ID 解析。
- `baseline-evidence.md` (104900 B, `b41e86d796bb583c`): 1-60 行全读; 437 行结果表由脚本逐行解析 (类别计数、行 ID 存在性、期望 / 实得)。

**必读材料**: 三个 issue 正文与评论、决策单全文、CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束、R4 聚合报告全文与本席 R4 报告、执笔 `v5-writer-report.md` 全文、`writer-v5-proto/` 的 README / `format_lint.py` / `refs_check.py` / `timing.py` (头与 i3 档) / `patch_*.py` 相关段 / `mut_summary_v5.txt` (只读本轮抽样的 24 个坏实现条目)、`PROGRESS.md`、四份研究笔记 (标题树与 Spec 引用到的节)。

**规范与源码** (aria `268da8f` / standards `2bc1c4c` / 主仓 `0748dbc`, 行号以实读为准)
- standards: `skill-benchmark-exemption.md` 全文 (rule6_note 五字段与 §4.1 逐项比对)、`content-integrity.md` §4.4 / §4.5、`secret-hygiene.md` 标题树与 §0 / §2.2 / §2.5 / §3.1-§3.7 / §5.1-§5.5 / §8-§10、`changelog-format.md`、`openspec/templates/proposal-minimal.md`、`git-commit.md` §6.1。
- aria: `hooks/secret-guard.sh` (被引行 :8、:21-23、:62、:405-408、:427、:491-493、:564、:617-626、:631-641、:698-700、:736、:778、:815、:850、:873-877、:893-894、:930-933、:974、:1006-1008、:1088-1111)、`hooks/secret-scan.sh` (:13-22、:31-36、:50-53、:62-66、:70-82、:120-260)、`hooks/tests/secret-guard.test.sh` (:11、:1607-1622、:2016-2032)、README.md / README.zh.md (:25-33、:137-160)、CHANGELOG.md 顶部、VERSION 相关行、`skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md:195-204`、`skills/spec-drafter/LEVEL_GUIDE.md`、`skills/state-scanner/lib/linked_issue_field.py`。
- 主仓: `.aria/state-checks.yaml` (16 个 check 名与 m6 三条)、`docs/architecture/system-architecture.md` (:210、:251、:404)、`openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:340-344`、`git show a99dd8d --stat` (上次发版同步面)。

**实跑** (全部在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R5-knowledge-manager/` 下; HOME / TMPDIR 私有; 命令与像凭据的值只经 stdin、不打印; 真仓零写操作、零子代理, 只用了 `git diff|show|log|ls-remote|rev-parse|status|count-objects`; 为读取 A.1 认领心跳, 我把 `refs/aria/coordination` fetch 进了**我自己目录里的一个私有裸仓**, 未动真仓)
1. 机械检查: `check_bare_issue_refs.py` 对三份文件 rc 0 (裸引用 0); 独立正则扫「无组织前缀的 repo#n」「裸 #n」, 只剩 `Rule #N`; 带圈数字 / 希腊字母 / emoji / 控制字节 / CR 全为 0; `extract_linked_issue_field` 对 proposal 头部得 `OK` 与 3 个 token; 证据文件每个被 Spec 引用的行 ID 都存在; 凡 SC 头部带 `×N` 的 (SC-1 至 SC-34 中 23 个) 都与证据行的类别计数逐项对上; 32 条技术级复议与 20 条建议开单的内部引用指向正确; 全部 SC 行 ID 引用无悬空。
2. **目标原型完整探针** (以 aria `268da8f` + standards `2bc1c4c` 的 `cp -a` 副本, 经执笔归档脚本重建, 非 root, 不带 `WPA_BASH32`, 主机 loadavg 17-25): rc 0, stdout 95695 字节, sha256 前 16 位 `cedf4efff40d6e67`, **与执笔 `final_TN` 逐字节相同**; baseline-failing 213/213、doc-sync 26/26、reverse-guard 77/77、allow-guard 70/70、known-limit 39/39、zero-regression 7/7, 仅 29h / 29i / 32c / 32d (无 b32) 与 30a (设计上不执行) 未跑。
3. **基线完整探针** (同法, 不带 `WPA_BASH32`): rc 0, 97946 字节, sha256 前 16 位 `da4c5c185abea1ec` (= 执笔 `final_N`); 与 `baseline-evidence.md` 内嵌 stdout 块相比只差 29h / 29i / 32c / 32d 四行与末尾三行汇总, 与证据文件自述一致。
4. **24 个坏实现** (执笔归档的 `patch_l1.py` / `patch_l3.py` 变体, 在我的目标树上各只跑其点名的行) 的转红行, 与执笔 `mut_summary_v5.txt` 记录逐行相同: 簇 U `nul_off` (1c 1d) / `nul_replace` (1e 1f, 即 R4 critical 的写法) / `nul_always_append` (1g) / `nul_space` (1c 1d); 簇 T `ext_v4stage` 四个子变体与旧设计整体 (19af 分歧 43 至 23 个形态; 旧设计另红 19al 与 34c) / `ext_charslice` (19ag) / `ext_localnoexp` (19ah 19am) / `ext_nobom` (19ai) / `ext_ascii_only` (19ae 19ah) / `ext_first` (20l) / `ext_noc` (19ad 19ae 19ag 19ah 19am, 在本机 mawk 上亲验, 对应 R4 km/m5); 簇 V `ext_perocc_judge` (34c: `64-occurrences-after-4KB[cost>3.5x]`); 簇 W `cli_unbounded` (10o 34b) / `kv_unbounded` (10n 34b) / `val_quadratic` (34a 34b) / `kv_left_boundary_off` (9z 34b); 簇 F `env_tight` (22br 0/44, 22bs 0/22) 与等价变异论证 (`remote_env_split:docker` 0 行红, `:nomad` / `:ssh` 各红 22bo 20/22); 簇 M `readface16` (18j 18k 各 16/32) / `readface_drop:1` (31/32); R4 qa/m3 `ell_lastchar` (32e 点名 11v 11x 11y); 文档类 `--cl-drop=CPU` / `--cl-drop=partial` (26g) 与 `--hdr-count` (28c 28d 28o)。
5. 簇 U 的**超集模糊测试** (本席自写, 值运行时生成不打印): 30 个随机输入 (14 类基线 tag 片段任意组合) x 9 种 NUL 变换 (无 / UTF-16LE / 换行换 NUL / 随机插 NUL / 空格换 NUL / 首尾 / 半 UTF-16 / NUL 连串 / 每 5 字符一个 NUL) x 基线与目标两个 hook = 540 次运行, 目标对每个基线报出的 tag 计数都不小于基线: 0 例回退。
6. 簇 T 的**独立形态差分** (本席自写 72 个命令形态, 与执笔的 73 / 93 / 2500 不重叠, 含续行、`||`、`|&`、`&>`、`$'...'`、嵌套 `bash -c`、`case`、heredoc 等): 内建 `app.ini` 名与扩展条目逐形态退出码 0 例分歧 (两侧各拦 60 个); 真 bash 3.2.57 在 `en_US.UTF-8` / `C.UTF-8` / `C` 三种 locale 下, 列入路径之前带 25 个汉字的命令仍 exit 2 (对应 R4 cr/M1)。
7. 簇 V: `occ_cost.py` 复测 4 KB 之外的两档: 2 KB 目标 1.7 倍、8 KB 目标 1.9 倍 (与 W9 引用的数一致); 基线 8 KB 自身 2.36 s CPU、目标 4.51 s (见风险 5)。簇 U 的大输入成本: 约 400 KB NUL 分隔输入基线 0.58 s / 目标 0.79 s, 约 240 KB 且每条记录都命中的输入基线 0.67 s / 目标 1.49 s。
8. `refs_check.py` 复跑: 3-step wrong 0, 且 Impact 里的正则与脚本里的 RX 逐字符相等; Rule #7: 对 v5 改动的 95 个文件用自写正则扫 (provider 前缀 / JWT / PEM 头 / URL 口令 / 40 与 64 位 hex / 键值赋值), 只命中 git SHA、bash 源码包校验和、带键名的行描述与补丁脚本里的 PEM 头字面, 无真实凭据形状。
9. 远端事实: 四仓 master 两端 `ls-remote` 未变 (主仓 `0748dbc`、aria `268da8f`、standards `2bc1c4c`、orchestrator `237045a`); 工作分支 origin = `6efb9b2`, github = `b07f69a`; 协调 ref origin `63c4f84f...` / github `ad0287f7...`。

**未做**: 带 `WPA_BASH32` + `WPA_REQUIRE_ALL=1` 的全量验收模式 (主控已跑)、499 个历史坏实现的全量回归、SC-30 / `timing.py` 全档 (只复测了 `occ_cost.py` 与 SC-34)、gawk / macOS / BSD / MINGW64 任何一腿。

## Findings

### Critical

无。

### Major

无。

### Minor

#### m1 - id `f410df76` - minor - issue - documentation
- scope: `proposal.md Impact` (四处同一事实多处不一致, 取主要出处)
- summary: 四处「同一事实在 Spec 内写法不一致」(偏离处数、Why 表 SC-23 的 6/6、Impact 性能百分比、「另有两行以 forgejo 为锚」), 都不改变实现者要写的代码。
- 证据 (逐处实读):
  1. 偏离处数: `proposal.md:364` (Impact「覆盖关系」)「10CG/aria-plugin#154 全覆盖 (两处有意偏离见上; …」, 而 `:357` 写「关单评论须逐条披露与评论 19339 字面参数的三处**有意偏离**: (a)(b)(c)」, Tasks 1.13 `:387` 写「评论逐条披露三处有意偏离与验证范围」。`git show b3e3123 / c0a6654 / b07f69a` 的同一行 (`:342` / `:353` / `:361`) 都是「两处」, 是 v2 起遗留的兄弟位置。
  2. Why 表: `proposal.md:40`「L1 `\.env` 无右边界误拦 (`os.environ` 单键读取) | 6/6 误拦 | SC-23」。SC-23 的基线 exit 2 运行现为 23a 1 个 + 23b 5 个 + 23j 4 个 = 10 (`baseline-evidence.md:412` `exit=2`、`:413` `exit=2,2,2,2,2`、`:417` `exit=2,2,2,2`); 6 是 v5 新增 23j 之前的 23a + 23b。SC-23 头 `:292` 写「基线 3/3」(按行计), 所以这一格既不是行数也不是运行数。
  3. 性能百分比: `proposal.md:349`「无扩展文件时 Bash 面约 +13%、Read 面约 +16% CPU 时间」与 `:240` W14 第 5 项「(f0) … 比值 1.14 与 1.14」不是同一个数 (执笔交付的 `logs/timing_main.txt:8-9` 原始行 `ratio 1.14` 两条, 即 +14% / +14%); 同句「约为基线的 1.5–2.3 倍」的下界与紧随括号里的 `(g-a) 1.42` 不符。
  4. 内建行数: `proposal.md:288` (19ak)「内建里另有两行以 `forgejo` 一词为锚」; 实读 `aria/hooks/secret-guard.sh:778` (`forgejo[[:space:]]+(GET[[:space:]])?…(actions/secrets|variables)`) 与 `:1006-1008` (三行 `\b(forgejo|curl)\b…`) 共 4 行; 19ak 的两个探针命令对应 `:1006` 与 `:1007`。
- 失败场景: 实现者要写的代码不变; 但 Tasks 1.13 关单评论的撰写者与验收者会读到「两处 / 三处」两个数, Why 表的数与 SC-23 对不上, 与 R4 km/m3 (`7b20c975`)、km/m7 (`8936aa07`) 同类 (v5 新增行时没有同步兄弟位置)。
- 建议修法: 四处各改一句: 「三处」; Why 表改「10/10 (23a 1 + 23b 5 + 23j 4)」或统一按行计「3/3」; 性能百分比以 W14 比值为准写「约 +14%」, 下界写「1.4」; 「另有四行 (`:778`、`:1006-1008`)」。

#### m2 - id `0c3c6ed4` - minor - issue - documentation
- scope: `baseline_probe.py` (证据文件 `baseline-evidence.md:398` 是它的 stdout 快照)
- summary: 探针行描述与注释里留有版本相对词: 22bp 行描述写「v4 additions」并原样进入证据文件, 另有 `(v2)` / `# v3:` 注释; 执笔的叙事 lint 只扫 `proposal.md`, 是 R4 km/m2 (`13e1f258`) 同类的兄弟位置。
- 证据: `baseline_probe.py:1753` 行描述 `"pid positions of the /proc rows, v4 additions: …"`, 经探针 stdout 原样出现在 `baseline-evidence.md:398`; `:1752` 注释「the pid positions added in v4」; `:264`「first-character / shape variants (v2)」; `:272`「# v3: members and boundaries …」。`writer-v5-proto/format_lint.py` 的版本叙事检查写成 `if path.endswith("proposal.md"):` 且词表是 `\bv[34]\b` 等, 探针与证据文件不在其内 (返修报告 §2「`format_lint.py` 对三份文件的输出」只证明了换行 / 制表 / 带圈数字 / emoji / 裸 issue 号这些通用项)。
- 失败场景: Spec 批准后, 证据里 22bp 行仍写「v4 additions」, 指向一个已不存在的修订; 该行属于「探针输出须与证据文件逐字节一致」的快照 (Tasks 1.1 / 1.10), 要改它必须同时重生成探针与证据两个文件, 越晚改越贵。
- 建议修法: 把行描述改成不带版本的写法 (「pid positions of the /proc rows: `$$`, `$!`, `thread-self`, …」), 同批去掉三处注释里的版本词, 重生成证据; `format_lint.py` 的叙事检查扩到三份文件 (词表补 `v2` / `added in v`)。

#### m3 - id `a305732c` - minor - issue - testing
- scope: `baseline_probe.py`
- summary: 探针的执行器没有逐行的异常隔离, 任一行里一次 hook 调用超过 `timeout=300` 就使整个探针以 traceback 退出 (rc 1), 其余 436 行结果全部丢失; 「坏实现红」在这种情形退化成整探针崩溃。
- 证据: `baseline_probe.py:2525-2526`: `for f in cf.as_completed(case_futs): results[case_futs[f]] = f.result()` 没有 try / except; hook 调用处 `:403`、`:501`、`:2455` 都是 `subprocess.run(…, timeout=300)`。实测: 我在 loadavg 约 20 的主机上对执笔的 `ext_perocc_judge` 坏实现 (对每个出现点各判一遍内建判定) 跑其汇总点名的行 `34c,19x,19y,19r`, 结果是 `PROBE-ERROR rc=1: … secret-guard.sh']' timed out after 300 seconds`, 没有任何一行结果 (19x / 19y / 19r 的 64 个出现点命令没有 CPU 上限, 在坏实现上要数十秒 CPU)。同一坏实现只跑 34c (有 `ulimit -t 4`) 则得 `1/2 as expected; wrong: 64-occurrences-after-4KB[cost>3.5x]`。
- 它怎么会红 (三态): 基线 = 整探针 rc 0 无超时 (我跑过, `da4c5c185abea1ec`); 目标 = rc 0 (`cedf4efff40d6e67`); 平方级坏实现 = 在负载高的验收机上整探针崩溃 (红, 但没有行级信息, 也不是 Spec 规定的 exit 3)。
- 失败场景: Tasks 1.8 要求非作者对抗 review 构造坏实现并用探针复核; 审阅者在繁忙的 CI 机上跑到一个平方级实现, 得到的是 traceback 而不是「19x / 34c 红」, 无法判断是哪条 SC 抓住了它; 验收模式下的 rc 语义 (0 / 3) 也被 rc 1 绕开。
- 建议修法: `main()` 里用 try / except 把 `subprocess.TimeoutExpired` 与一般异常转成该行的 `("error: <类型>", False)`, 只让该行转 `no`; 同时给 19x / 19y / 19r 一类带出现点填充的行也传 `cpu=` 上限 (与 34c 同体例)。

## 上一轮对账

R4 的 1 个 critical + 9 个 major 席位条目按主控记录归并为 6 个键, 我逐簇核为 **closed**:

| 簇 / 键 | R4 席位条目 | 对账 | 我亲自核验的证据 |
|---|---|---|---|
| U `1038b8da` | ba/C1 | closed | v5 W1 (`:52-54`) 改为「基线视图照扫 + 含 `\u0000` 且与基线视图不同才追加换行视图」; 探针 1e / 1f / 1g 在目标态 `yes`; 坏实现 `nul_replace` (R4 critical 的写法) 红 1e / 1f、`nul_off` 红 1c / 1d、`nul_always_append` 红 1g、`nul_space` 红 1c / 1d (均与执笔汇总一致); 我的 540 次超集模糊测试 0 例回退。附带成本: 大 NUL 输入 (约 240 KB 且每条都命中) CPU 为基线的 2.2 倍, 目前没有时档 (风险 4)。 |
| T `0a8380fd` | ba/M2、qa/M1、cr/M1、km/M1 | closed | W9 (`:164-168`) 不再自写引号掩码 / 阶段切分, 改为把条目的前 64 处出现换成内建 `app.ini` 名后交 `_sg_core_eval` (原型里 `_sg_per_segment_eval` 与 `_sg_ext_pass` 调用同一函数, 实读 `secret-guard.sh` 原型); 19af 73 形态零分歧, 我另做 72 形态独立差分 0 例分歧; 旧设计 4 个子变体各红 19af (50 / 53 / 52 / 57 个形态相等, 少于 73); 偏移 / 切片同一单位: 真 bash 3.2 三种 locale 下 25 个汉字前缀仍 exit 2, `ext_charslice` 红 19ag。 |
| V `22bdd143` | tl/M2 | closed | W14 (f-hit) / (i3) 与 SC-34 34c 新增; `occ_cost.py` 复测 2 KB 1.7 倍 / 8 KB 1.9 倍 (旧写法 7.6 / 24.7 倍见 W9 `:166`); `ext_perocc_judge` 红 34c; 目标态 SC-34 3/3 在 loadavg 17-25 的主机上仍 yes。(SC-30 的 `timing.py` 时档我没有复跑。) |
| W `755aab21` | ba/M1 | closed | W2 (`:59-69`) 的 6 个新 pattern 带有界量词与左边界, 实读原型 `secret-scan.sh:241` / `:244` 为 `[A-Z0-9_]{0,64}` 与 `[A-Za-z0-9-]{0,40}`; 34a / 34b 目标态 yes; 4 个坏实现 (`cli_unbounded` / `kv_unbounded` / `val_quadratic` / `kv_left_boundary_off`) 各红其点名的行。 |
| F `e2459206` (含 `8fbbee80`) | tl/M1、cr/M2 | closed | W11 (`:196`) 明文规定包裹下转储沿用默认 credit、不属 tight; 22br (44 个运行放行) / 22bs (22 个运行限制) / 22bo (22 成员拦) 三行两个方向钉住, Impact (`:344`) 申报, 待复议 23 列备选 B / C; `env_tight` 使 22br 0/44、22bs 0/22 全红; 等价变异论证 (`docker` 分裂 0 行红, `nomad` / `ssh` 分裂红 22bo) 在带过滤的转储上也成立。 |
| M `eb350937` | qa/M2 | closed | W8.3 (`:154`) 与 W14 通则 (`:241`) 列入 `:641`; 18j / 18k 各 32 个运行目标态 yes; 我用自己的解析器数 `:641` 正则顶层备选恰为 32 个, 与 Spec 的枚举逐项对上; `readface16` 红 16/32、`readface_drop:1` 红 31/32。 |

R4 其余 15 条 minor (本席 7 条 + 其他席 8 条) 我逐条对了 v5 文本或探针行, 除下面两条外均已处置:
- **km/m6 `91a89f9b` (已公开推送的分支含旁路配方): partially closed**。Spec 侧已关: 7.1 / 7.2 去量化 (全文搜不到「1400」「空段」), 新增 7.20 登记为产品级请裁项。未关的部分不在执笔权限内: (a) 研究笔记 `research/secret-guard.md:20,:371` 仍在 v5 提交里保留量化配方, 而 Spec 的 7.1 写「复现细节只留在研究笔记」, 去量化只是把细节放在同一提交的另一个文件里; (b) GitHub 上分支停在 `b07f69a` (我 `ls-remote` 实测), 清理属 owner; (c) 7.20 的默认选项 A 是「现状保留」, 主控实际在做的「暂停推 GitHub」是 B 的方向, handoff 要并列写。已列入风险 1, 不重复立 finding。
- **km/m3 `7b20c975` (陈旧时档数字): closed, 残余并入 m1 的第 3 点**。W9 已不再复述时档数字, Impact 与 W14 改用 v5 终测数; 残余只是百分比取整不一致。
- 其余核为 closed 的 minor, 各一句: tl/m1 (W11 `:203` 成文 + 22bj 14 个运行、基线 0/14); tl/m2 (W2 `:80` / W8 `:157` / 10m 6 个运行); qa/m1 (23j + 25h, 目标态 yes); qa/m2 (19ai); qa/m3 (32e, `ell_lastchar` 红并点名 11v / 11x / 11y); cr/m1 (同 tl/m1); cr/m2 (同 km/m3); ba/m1 (采纳, 19ae 改 baseline-failing); km/m1 (W1 `:53` 理由按实测重写, 不再写「两层皆静默」「修不了」); km/m2 (Spec 正文已无 v3 / v4 / 本版 / 上两轮 / 曾写 / 返修; `\bv[0-9]\b` 只剩外部版本号与 `writer-v5-proto` 路径; 残余在探针与证据, 见 m2); km/m4 (26g 标记词 13 个逐个删各红, `--cl-drop=CPU` / `partial` 亲验; README 两个 Hooks 小节核实为 `:25` / `:137`, 探针按标题取最后一个); km/m5 (扩展代码区 0 处 `awk`, `ext_noc` 在 mawk 主机上红 5 行); km/m7 (四处全改: `:8` 入 W14 与 28o; 22av 逐个写全 14 个; 22bk 11 个; `COMMIT_FOOTER_GUIDE.md:199-200` 与 `:201-202` 我实读对上)。

## 对执笔人自报薄弱点与请裁项的表态

**自报薄弱点 (返修报告 §5)**
1. 34c 是探针里唯一带比值的行: 可接受。我在 loadavg 17-25 的 4 核主机上完整跑目标原型, SC-34 3/3 仍 yes 且 stdout 与执笔的 `final_TN` 逐字节相同, 说明该行在重负载下没有抖动 (正面证据); 它对坏实现的行级证伪见 m3 的注意点。
2. 19af 的零分歧只对有限形态表成立、条目含 shell 元字符时「由构造一致」的前提不成立: 可接受。已写进 W9 已知限制; 我独立做的 72 形态差分 0 分歧, 不要求再钉行。
3. 键名 / 参数名上界 64 / 40 是取舍: 可接受 (技术级)。理由成立, 且 10n / 10o 钉住现状、两个无界坏实现各红 34b。
4. W1 的 NUL 前提无端到端样本: 可接受 (Spec 明写「前提不成立时是无害空操作」)。建议 (不计 finding): 执笔不采纳「post-ship 加 NUL 腿」的理由 (「加了也只能记未验证」) 不完全成立, 因为这一腿恰好能**产生**缺的那个样本 (对自造的 NUL 分隔诱饵文件做一次 Read, 看告警是否带 N 视图的 tag), 结果无论正负都是新知识; 但它不应作为关单门, 现行写法可接受。
5. 耗时回升与 (i3) 上界 2.5: 可接受。好实现 (i3) 1.15-1.74 与坏实现 3.4 倍起之间的间隙里取 2.5, 不是把阈值挪向方便的一侧; 须在 handoff 的「AI 自作主张」里列出 (执笔 §6.5 已列)。
6. 回归覆盖靠重跑旧坏实现、移出 7 个旧变体与 29 个 `drop_extreader_*`: 可接受。我抽样 24 个 v5 坏实现与汇总逐行相同, 未全量复跑 499 个。
7. proposal 增长约 30 KB: 可接受, 但体量本身是风险 3。
8. 研究笔记与已推送分支 (km/m6): Spec 侧可接受; 笔记里的配方段落建议主控在下一次提交前做前向去量化 (不改历史), 否则 7.20 选项 A「只写类别」的承诺与同一提交里的笔记不一致。
9. 时档是单机单次测量: 可接受 (判据是比值与活性, 不是数字)。

**请裁项 (返修报告 §6)**
1. 7.20 产品级披露范围: 可接受登记; handoff 须把「默认 A 与主控暂停推 GitHub」并列, 让 owner 一次看清 (风险 1)。
2. W9 条目规则 (含 ASCII 字母数字或任一非 ASCII 字节即有效、剥 BOM): 可接受, 与我 R4 的建议一致, 技术级直接裁定即可。
3. 簇 F 的 credit 默认 (转储后锚定 grep / cut 放行, `grep -v x` 同样放行): 可接受。与基线 `docker|kubectl|podman|lxc exec … env` 行同一 credit, 两个方向由 22br / 22bs 钉住, 备选 B / C 在待复议 23 有论证; 新包裹的保护力因此弱于字面「拦转储」, 已在 22bs 与 Impact 如实申报。
4. W2 上界 64 / 40: 可接受 (待复议 31)。
5. W14 的 (i3) 上界 2.5 与 (i3-b / c) 取 60 KB / 100 KB: 可接受 (基线自己对 300 KB 同类输入要约 5 s, 取更大档会判「环境不合格」)。
6. SC-34 判据口径 (每进程 CPU 上限 + 34c 的 3.5 倍): 可接受。
7. 采纳席位备注两条 (Impact 的 Layer 2 一句 `:344`、关单评论的验证范围一句 `:357`): 可接受。
8. 未采纳三项 (post-ship NUL 腿 / timing 并入探针 / gawk 腿): 可接受; gawk 腿已因「不再依赖 awk」消解, 我在 mawk 主机上验证 `ext_noc` 红 5 行。
9. Rule #10 自作主张清单: 可接受; 其中「`build_deliver5.py` 把 stage-1 的 proposal 快照相等断言放宽为只要求探针相等」是验证工具自我放宽, 理由 (proposal 文字不进基线 stdout, 由 `final_C` 逐字节相等证明) 成立, 且我对基线完整探针的独立复跑与 `final_N` 逐字节相同, 也印证了这一点。

## 风险 / 疑问

1. **公开镜像与 7.20**: GitHub 上分支停在 `b07f69a` (v4, 含 7.1 / 7.2 的量化配方与 `research/secret-guard.md:20,:371` 的完整配方, 匿名可读); origin 已有 `6efb9b2` (v5)。派单背景写「未推送」与我 `ls-remote` 的事实不符 (origin = `6efb9b21e36a…`)。请主控 (1) 把「已公开分支含未修复旁路配方 + 主控自作主张暂停推 GitHub」写进 handoff 待 owner 裁定, 并与 7.20 默认 A 并列; (2) 在下一次提交前对研究笔记那两处做前向去量化。
2. **W5 是 AI 增补** (R3 / R4 风险 3 仍成立): 10CG/aria-plugin#154 评论 19339 明说告警措辞「现行已满足」, W5 不是任一 issue 的诉求, 却带来 rule6_note 块 B、SC-13 的 14 个运行与待复议 8 / 19。建议 handoff 标为 AI 增补并给 owner「删除 W5」选项。
3. **体量与可确认性**: proposal 449 行 / 214 KB (最长一行 5240 字符, 超 2000 字符的行 5 条), 探针 2682 行 / 222 KB, 证据 105 KB; `standards/openspec/templates/proposal-minimal.md` 对 Level 2 的预期约一页, Spec 自己的 Level 对账 (`:13`) 承认三条升级判据字面命中。决策单第 3 项已裁 Level 2, 本席不就 Level 立 finding; 但 owner 做降级裁定时「人类能否确认这份 Spec」值得作为考虑因素 (这与 memory 里「拆 Spec 是净负」不矛盾: 问题在体量与确认成本, 不在是否拆分)。
4. **NUL 大输入没有时档**: W14 的 (i) / (i3) 不含 NUL 分隔的大输入; 实测 240 KB 每条都命中的 NUL 输入目标是基线的 2.2 倍 (0.67 s 到 1.49 s), 信封封顶 1 MB 下的上界未测。不构成回退 (基线先出的检出仍在, 超时只会让追加的 N 视图失效), 但属 W1 唯一没被 W14 覆盖的成本面。
5. **命中路径的绝对成本**: 8 KB 单行命令且列入路径出现 64 处时, 目标 CPU 4.51 s (基线 2.36 s), 逼近 hook 5 s 超时; (f-hit) 档只测 4 KB 且判据是比值 (<= 3.0)。内建判定先于扩展, 超时只会让扩展自己的拦截失效 (与基线同), 所以不是回退, 但 7.1 的「延迟悬崖」措辞可以顺带提一句这个量级。
6. **未验证项**: 带 `WPA_BASH32` + `WPA_REQUIRE_ALL=1` 的验收模式 (主控已跑)、SC-30 与 `timing.py` 全档、gawk / macOS / BSD / MINGW64、499 个历史坏实现的全量回归。
7. **认领与在飞轨**: A.1 认领心跳 2026-10-06T22:17:33Z, 状态 active (24 h TTL, 无需立即续; R4 风险 2 已无); 双子星 `10CG/Aria#199` 的认领 (phase A.2) 最后心跳 2026-10-02T11:53:52Z, 已 5 天无心跳 —— Spec 的「串行发版、取号前协商」对它停摆或先发版两种情形都成立, 不影响条款。
8. **仓根杂物**: 起始 `git status` 就有一个未跟踪的 `gawk_1%3a5.2.1-2_amd64.deb`; 提交请用显式路径, 勿 `git add -A`。
9. **W12 的活体实例**: 本席工作中现行已安装的 secret-guard 又一次因 heredoc 里的 `os.environ` / `.env` 子串误拦了一条命令 (正是 W12 要修的误拦类), 我改用 Write 工具落文件继续, 未使用 `# guard:ack`。
10. **README 与 SOT 并存陈述** (R4 风险 9): 28m 只增不改, `README.md:33` / `README.zh.md:33` 表格行与 SOT §5.2 的「cannot redact」在待复议 1 落地前并存, Out of scope 已声明, 本席接受。

## Verdict

- verdict: **PASS**
- counts: `0C/0M/3m`
- Vote: **PASS**

## 是否足以进入 A.2

足以。R4 的 1 个 critical 与 6 个 major 键 (U / T / V / W / F / M) 在本席的独立复核里全部关闭 (目标与基线完整探针 stdout 与执笔 `final_TN` / `final_N` 逐字节相同, 24 个抽样坏实现的转红行与执笔汇总逐行一致, 另有本席自写的 540 次 NUL 超集运行与 72 形态扩展 / 内建差分均零回退零分歧); 本席视角下文档同步面、rule6_note 五字段、issue 引用写法、机读词英文 canonical、Rule #7 / #9 / #10 与决策单各项均无 major, 3 条 minor 都不改变实现者要写的代码, 可在 A.2 之前顺手改 (m2 需连带重生成证据), 也可并入 task-planner 的 B.1 入场项。这一判断只限本席的文档与规范一致性视角; 请 owner 在降级裁定时一并看风险 1 (已公开分支与 7.20 默认值的方向不一致)、风险 2 (W5 是 AI 增补) 与风险 3 (体量)。
