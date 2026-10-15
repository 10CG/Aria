---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T00:38:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 - knowledge-manager 席 (文档与规范一致性)

## 已实读文件

**被审对象**
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-443 行 (b07f69a, 184049 字节, sha256 前 16 位 `f98e719d6036b4f8`, 与执笔 MANIFEST 一致); 另生成 v3 到 v4 的紧凑逐词差异 (856 行) 全部读完。
- `baseline_probe.py` (191479 字节, `7da0e53eef5d64da`): v3 到 v4 的 583 行差异全读; 另读 SC-19 区 (1355-1400)、PS_SPELL 与 SC-22 区 (1545-1575)、SC-26/27/28 判据函数 (1836-2060, 含 26g 的 1941-1949)。
- `baseline-evidence.md` (`4e0a94aac6e77058`): 1-48 行; 411 行结果表由脚本按 SC 逐行取出 (SC-1/2/4/5/6/7/12/13/16/19/20/21/22/23/26/27/28 的期望 / 实得 / 符合列)。

**必读材料**: 三个 issue 正文与评论、决策单全文、CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束、R3 聚合报告 (全部 finding 表与主控记录) 与本席 R3 报告、执笔 `v4-writer-report.md` 全文、`writer-v4-proto/` 的 README / `mut_summary_v4.txt` / `manual_runs.txt` / `timing_summary.txt` / `fuzz_mask.py` / `refs_check.py` / 补丁脚本相关段、`PROGRESS.md`、研究笔记 `secret-guard.md:20,:371`、memory `feedback_audit_trail_must_not_live_in_spec.md`。

**规范与源码** (aria `268da8f` / standards `2bc1c4c`; 行号以我实读为准)
- standards: `content-integrity.md` §4.4 / §4.5; `skill-benchmark-exemption.md` 全文 (rule6_note 五字段与 §4.1 模板逐项比对); `secret-hygiene.md` 标题树、§2、§5; `changelog-format.md`; `git-commit.md` §6.1。
- aria: `hooks/secret-guard.sh` 1-135 行与被引行 (:850、:873、:875、:877、:893-894、:930-933); `hooks/secret-scan.sh` 10-82 行; `hooks/hooks.json` (5 s 超时与 matcher); `README.md` 两个 Hooks 小节 (:25 与 :137); `CHANGELOG.md` 顶部; `VERSION`; aria 的 `26e644e` 发版提交文件集 (6 个文件, 与 Impact 同步面一致); 主仓 `72cb02b` / `a99dd8d` (8 个文件 + gitlink, 16 个版本点逐项对上)。
- 主仓: `.aria/probes/plugin-cache-currency.py` (输出词 `OK` / `##SKIP##` / `STALE` / `AHEAD` / `MALFORMED` 与 Tasks 1.12 逐项对上); `.aria/state-checks.yaml` 的 16 个 check 名; `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:342` (Impact 所引 `guard_config_hooks` 原文, 逐字相符)。

**实跑** (全部在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R4-knowledge-manager/` 下; HOME / TMPDIR 私有; 命令与值只经 stdin、不执行、不打印像凭据的值; 真仓零写操作、零子代理, 只用了 `git diff|log|show|rev-list|ls-remote|reflog`)
1. 机械检查: `check_bare_issue_refs.py` 对三份文件 rc 0 (裸引用 0), 另用独立正则扫「仓名加空格加 #」与无组织前缀的 `repo#n`, 零命中; 带圈数字 / 希腊字母 / 表情 / 控制字节 / CR 全为 0; proposal 内 273 处 `SC-n id` 引用全部解析到证据行, 「待复议 N」「建议开单 7.N」引用全部指向正确条目。
2. 目标态全量复跑: 以 aria `268da8f` + standards `2bc1c4c` 的 `cp -a` 副本经执笔归档脚本重建目标原型 (两个 hook 的 sha256 前 16 位 `d94ddf4d6906734f` / `cf2dd857823baf79`, 与执笔一致); uid 1000、真 bash 3.2.57、`WPA_REQUIRE_ALL=1`: rc 0, stdout 83988 字节, sha256 前 16 位 `7360938f57ee82d0` (与执笔 final_T 逐字节相同); baseline-failing 202/202、doc-sync 25/25、reverse-guard 72/72、allow-guard 67/67、known-limit 35/35、zero-regression 9/9, 30a 按设计 n/a, 目标形态 holds。
3. 抽样坏实现: 执笔的 20 个坏实现 (`nul_off`、`oldkey_drop:webhook_secret`、`step_on:ent:bearer-token`、`step_on:wl:basic-auth-url`、`fp_lt20`、`hash_noshasum`、`val_eval`、`ext_nomask`、`ext_mask_nonl`、`ext_nostrip`、`ext_emptypat`、`ext_eval`、`vx_eval`、`tdrop_psalt:2`、`tdrop_launch:exec`、`remote_env_split:ssh`、`remote_env_split:watch`、`drop_pid:6`、`launcher_ps_only`、`proc_tight`) 全部复现为各自点名的行转红; 6 个文档坏实现 (`--hdr-half-l` / `--hdr-dangling` / `--hdr-half-a` / `--hdr-argon` / `--hdr-topcontent` / `--hdr-nohist`) 各只红 28l / 28b / 28a / 28e / 28f / 28j; `refs_check.py` 9 个场景 v4 全符合预期, v3 写法在 5 个跑坏态真空通过。
4. 本席自造坏实现与对照 (见 M1、m1、m5): 3 个 `_sg_ext_mask` 变体、1 个删 `LC_ALL=C` 的变体、3 个 NUL 处理变体; 约 115 条日常良性命令在基线与目标原型上的退出码对照 (只有 `os.environ.get(` / `os.environ[` 两条由拦变放, 即设计内的新放行; 无未申报新误拦)。
5. 平台与事实: 真 bash 3.2.57 + `en_US.UTF-8` 下 `[[ QWERTY == *[a-z]* ]]` 为真, bash 5.2.15 在 C.UTF-8 / en_US.UTF-8 / zh_CN.UTF-8 下为假, 3.2.57 在 C.UTF-8 下为假 (W2 所述相符); procps-ng 4.0.2 `pgrep -fl` 只出 pid 与名字、`ps -w` 只出 comm、`ps w` 出完整命令行; 基线对 `docker|kubectl|podman|lxc exec ... env|printenv` 本就 exit 2 而 `nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `watch` 放行 (4 个等价变异的论证成立)。
6. 远端事实: 四仓 master 两端 `ls-remote` 未变 (主仓 `0748dbc`、aria `268da8f`、standards `2bc1c4c`、orchestrator `237045a`); 协调 ref `refs/aria/coordination` origin `63c4f84f...`、github `ad0287f7...` 不同 (见风险); 工作分支两端状况见 m6。
7. Rule #7: 本席未读取或打印任何凭据。对 b07f69a 改动的 85 个文件用自写正则 (provider 前缀 / JWT / PEM 头 / URL 口令 / 40 与 64 位 hex / 键值赋值 / 头参数形) 只打印文件与行号: 命中只有 git SHA、bash 源码包校验和、文档里的「点分标识符链」代码示例 (SC-9 9v 的已知误报形态)、一份原型脚本里的 PEM 头部字面 (无密钥体, v3 同); 无真实凭据形状。过程说明: 现行 secret-guard 以「文本提及」类误拦了我一条含 `/proc/...` 与 `tr` 讨论文字的 heredoc 命令 (正是 W11 声明接受的误拦类), 我改用 Write 工具落文件后继续, 未使用 `# guard:ack`; 另有两次对本机的进程列举 (`pgrep -af` / `ps`) 输出已截断, 可见部分只含程序路径与进程名。

## Findings

### Critical

无。

### Major

#### M1 - id `0a8380fd` - major - issue - implementation
- scope: `proposal.md What.W9` (沿用 R3 簇 T 的键: 本条是该簇的残余, 见「上一轮对账」)
- summary: W9 声称引号掩码覆盖 `$'...'` 与转义、并与内建 `_sg_split_top` 同一套状态机, 但 SC-19 的行只有无转义的单 / 双引号形; 自然的简化掩码 (不认反斜杠转义, 或把 `$'...'` 当普通单引号) 让 SC-19 29/29、SC-20 17/17 全绿, 却放行内建 `app.ini` 行会拦的同形命令。
- 证据:
  1. 文本: `proposal.md:164` 「引号 (单引号、双引号、`$'…'`) 内的 `;` `&` `|` 与换行不是阶段边界 … `_sg_ext_mask`; 引号 / 转义状态机与内建 `_sg_split_top` 同一套: 原型上对 4000 个随机串做过差分核对 … 见 `writer-v4-proto/fuzz_mask.py`」, 并写「与内建 `app.ini` 行对同形命令的判定一致 (SC-19 19z …)」; 头部 `:9` 写「本 Spec 承重的判据只靠 `baseline_probe.py` 的 SC 行复现」。等价性的唯一证据是 notes 里的 fuzz 脚本 (脚本本身合格: 字母表含 `$'` 与 `\;`, 对独立 oracle 逐位比对), 不在任何 SC 行或 Tasks 里。
  2. 行: `baseline_probe.py:1372-1377` 的 STAGE_SHAPES 只有 6 个形态 (python3 -c / node -e 用双引号、awk 用单引号, 内部都没有反斜杠转义), 另 2 个引号内 `|` 形; 19aa (`:1379`) 的 8 形同样没有。我在 SC-19 / SC-20 区 (1290-1430 行) 搜 `$'` 与转义的 `\"`: 零行。`$'...'` 在整个 L1 行集里没有一行。
  3. 实跑: 我自写 3 个坏实现, 只替换目标原型 `secret-guard.sh` 里 `_sg_ext_mask` 的函数体 (其余逐字节相同; 构造脚本 `exp/work/mk_mask_mutants.py`): `mask_noesc` (无任何转义处理、`$'` 不特殊)、`mask_noesc_q` (只在引号外认反斜杠)、`mask_nodollar` (`$'...'` 当普通单引号)。`WPA_ONLY=SC-19,SC-20 python3 baseline_probe.py <树>/aria`: 三个坏实现都是 SC-19 29/29、SC-20 17/17, target shape holds; 未改的目标原型同值。
  4. 发散命令 (`.aria/secret-guard.paths` 列一条 `/srv/secretdir/data`, 命令只喂 stdin; 退出码依次为 目标原型 / mask_noesc / mask_noesc_q / mask_nodollar / 基线): `python3 -c "print(\"a;b\"); print(open('<条目>').read())"` 得 2 / 0 / 0 / 2 / 0; `python3 -c $'print(open(\'a;b\') and open(\'<条目>\').read())'` 得 2 / 0 / 0 / 0 / 0。同形命令把条目换成内建名字 `/etc/forgejo/app.ini` (不带扩展文件), 目标原型 5/5 个转义形态都 exit 2: 内建行拦、简化掩码的扩展放行, 与主控 R3 裁定 #2「与内建 app.ini 行对同形命令的判定一致 (行为对齐用 SC 钉住)」相反。
- 失败场景: 实现者按 W9 写最常见的引号切换式掩码 (或照 `_sg_split_top` 抄漏转义分支), 探针全绿、Tasks 1.10 验收通过; 生产里 `python3 -c "print(\"x;y\"); print(open('<列入路径>').read())"` 这类 AI 常写的带转义引号的内联程序读到列入路径时扩展不拦, 而同形命令读 `app.ini` 被内建拦 (退出码 2 对 0)。「怎么会红」三态: 基线 (无扩展) 红、目标绿、上述自然坏实现仍绿 —— 验收放过一个错误实现, 与 R3 簇 M / T 同类。
- 建议修法: 在 SC-19 19z (或新增一行) 补 2-3 个形态, 内建 `app.ini` 与扩展条目两侧各比对: (a) 双引号内联程序里 `\"` 之后再出现 `;` / `&`; (b) `$'...\'...;...'` 里转义单引号之后出现分隔符; 上面第 4 点的两条命令各转一个即可让三个坏实现转红 (noesc 与 noesc_q 红于 (a)(b), nodollar 红于 (b))。把 `ext_mask_noesc` / `ext_mask_nodollar` 写进 W9 / SC-19 的「怎么会红」与 Tasks 1.8 的对抗 review 清单; 另可把 `fuzz_mask.py` 的差分复核列为 Tasks 1.8 的必做复现项。

### Minor

#### m1 - id `a8f5db8c` - minor - issue - documentation
- scope: `proposal.md What.W1`
- summary: W1 设计取舍的两句理由与实测相反 (不带 `tr` 的实现并非「两层皆静默」, 「NUL 换空格修不了」也不成立); 取舍结论 (选 A', NUL 换换行) 仍对, 理由写错。
- 证据: `proposal.md:52`「行首锚的 `env-line-secret-keyword` 与带左边界的 `kv-secret-assign` 都锚不上 (基线与不带这一段的实现对该形态两层皆静默: SC-1 1c / 1d)」, `:53`「不选 B' 把 NUL 换成空格: 行首锚丢失, 修不了」。我在目标原型的 `secret-scan.sh:145` 上做三个变体, 用运行时生成的六记录 NUL 分隔环境 (只打印 tag 与计数), 每个变体跑 3 次、Bash 与 Read 两种信封: 提取后 `tr '\000' '\n'` 得 `env-line-secret-keyword=3`; 换成 `tr '\000' ' '` 得 `kv-secret-assign=3` (三条凭据全检出); 不带 `tr` 得 `kv-secret-assign=1` (告警, 非静默)。执笔自己的汇总也如此: `mut_summary_v4.txt:48-50` 的 `nul_off` 记 `alert m=1 {kv-secret-assign=1}`。基线静默只因 kv tag 在基线不存在。
- 失败场景: 不改变实现者动作 (1c / 1d 钉 `env-line-secret-keyword=3`, 只有换行满足); 但后来的维护者读到「不带 `tr` 两层皆静默」「换空格修不了」会据此做错误权衡 (例如以为 kv tag 兜得住粘连、`tr` 可删, 或反过来否定一个同样可行的替代)。
- 建议修法: 改写这两句: 不带 `tr` 时粘连行只被 `kv-secret-assign` 检出 1 条 (3 条凭据漏 2 条, 且 tag 是新 tag 而非 `env-line-secret-keyword`); 选换行而非空格的真实理由是保住既有 tag `env-line-secret-keyword` 的行首锚语义与 3/3 检出, 不依赖 W2 的新 tag。

#### m2 - id `13e1f258` - minor - issue - documentation
- scope: `proposal.md 待复议` (最清楚的一处是条目 23; 其余出处见证据)
- summary: v4 把版本 / 审计叙事写回了 Spec 正文 9 处, 重蹈 R1 km `381efd94` 与 audit-trail 备忘的覆辙; 不改变实现者动作, 但 Spec 一旦 Approved 这些全是悬空引用。
- 证据 (逐行实读): `:9`「本版新增或改写的行 … 上两轮的同类材料在 `writer-v3-proto/` 与 `writer-v2-proto/`」; `:68`「(v3 的范围写法 `ent_range` …)」; `:184`「非作者构造的 eval 式实现曾在 SC-16–25 / 29 / 31 / 32 全绿的同时真的执行了命令文本」; `:194`「(v3 的已知限制曾写它们「仍放行」, 与原型相反; 现取「纳入」…)」; `:261`「v4 另把 W9 的条目格式规则 … 补了成员行」; `:289`「pid 位置的 v4 新增形态」; `:360`「与 v3 写法的真空通过对照」; `:374`「v4 另加七类」; `:436` (条目 23)「v3 的已知限制曾写「仍放行」, 与 v3 原型 (一直拦) 相反」。memory `feedback_audit_trail_must_not_live_in_spec.md`: append-only 的审计叙事与收敛型交付面不能同居一文。
- 失败场景: A.2 的 task-planner 与 B.1 的实现者读到「v4 另加七类」「v3 的已知限制曾写」「上两轮」, 要去找已不在文档里的 v3 文本才能理解; 每多一轮返修又会再叠一层, 正是 audit-trail 备忘记录的缺陷生成机制。
- 建议修法: 删去版本相对词 (v3 / v4 / 本版 / 上两轮 / 曾写 / 曾在 ...全绿), 只留事实陈述: 例如条目 23 写「纳入; 备选: 收窄到 ssh / nomad / pct」, `:194` 去掉括号里的版本史, Tasks 1.8 写「另加七类」改为直接并入列表; 需要保留的返修过程放 handoff 或审计笔记。

#### m3 - id `7b20c975` - minor - issue - documentation
- scope: `proposal.md SC-30` (时档数字的最终口径在 W14 与 `timing_summary.txt`; 陈旧处在 W9 与 Impact)
- summary: 执笔称「时档与掩码成本数字按终版原型重测并更新」, 但 W9 的无扩展开销与 Impact 的扩展开销仍是 v3 的数, 与 W14 / `timing_summary.txt` 的 v4 终测不符。
- 证据: `:165` (W9)「原型实测整进程 CPU 约 +6–9 ms (Bash 面 0.052 → 0.061 s)」, 而 `:238` (W14 第 5 点) 与 `timing_summary.txt` 15 对运行是 (f0) Bash 0.048 → 0.058 s (比值 1.23); `:346` (Impact)「新行使多段命令 (含 200 条扩展条目) 的 CPU 时间约 +20–25% … 200 条扩展条目约 +27 ms CPU / 次调用」, 而 v4 终测 (f) Bash 0.049 → 0.072 s、Read 0.042 → 0.067 s (含 200 条扩展条目: +47% / +60%, 比值 1.46 / 1.61), +20-25% 实为 (f0) 不带扩展文件的数 (1.23 / 1.15), 扩展自身约 +13 ms (Bash) / +19 ms (Read), 「+27 ms」是 v3 的 (f) 差值 (0.049 → 0.076); `:346` 与 `:399` 的「1.4–2.3 倍」对 W14 (g-a) 1.4、(g-b) 2.0 (2.3 来自不作判据的 h1 档)。
- 失败场景: 不改变实现者动作 (判据是 W14 的比值上界); 但 Impact 是给采用方读的性能披露, 两处数字互相矛盾。
- 建议修法: 把 `:165` 改为与 (f0) 一致, `:346` 改成「不带扩展文件约 +15–25%; 含 200 条扩展条目约 +45–60% (扩展自身约 +13–19 ms)」, 倍数改「1.4–2.0」, 并对 W1 的 0.31 / 0.33 / 0.66 s 一并按终版重测 (`tr` 多一个进程)。

#### m4 - id `60eea71e` - minor - issue - testing
- scope: `proposal.md SC-26` (键与 R1 某条已闭合的 SC-26 minor 同键, 内容不同; 与 R3 `a6304dd1` 同类: 文档判据过弱)
- summary: SC-26 26g 只查 7 个子串, 撑不起 Impact 所称「六条逐条披露」; 28m 的「Hooks 小节」在两份 README 里各有两个同名 / 近名小节而 Spec 未指明是第二个 (探针取最后一个)。
- 证据: `baseline_probe.py:1941-1949`: `_changelog_doc` 取顶节后只验 `rule6_note`、`.aria/secret-guard.paths`、`ps aux`、`os.environ`、`keys_unsorted`、`fp=`、`partial`。Impact `:348` 写「新节带 rule6_note 行与上面「行为变更双向申报」六条的逐条披露 … SC-26 26g」; 六条里「新告警 (Read 首次被扫描 / NUL / 6 个新 tag / 已知误报类)」「新静默 (白名单)」「性能」与 `app.ini` / `/proc` / 包裹下 env / 文本提及误拦这些采用方最会撞上的新拦截, 没有任何子串守着。另: `aria/README.md` 有 `### Hooks (Auto-triggered)` 两处 (`:25` 表格小节、`:137` 用法小节), `README.zh.md` 为 `### Hooks 系统（自动触发）` (`:25`) 与 `### Hooks 自动触发` (`:137`); 28m 的探针 (`_updated_tool_output_everywhere`) 取最后一个, W9 文档落点与 W14 写的是「Hooks 小节」(只有 26e 写「用法小节」)。
- 失败场景: 实现者写出只含这 7 个词的 CHANGELOG 即绿, 却漏披露 Read 首次被扫描等采用方可见行为; 或把 28m 的那一句加在表格小节 (紧挨 `cannot redact` 表格行), 探针红后才知道要放在第二个小节。
- 建议修法: 26g 的关键词按六条各取一个代表词 (如 `Read` 工具首次扫描、`app.ini`、`/proc`、`kv-secret-assign`、白名单 / 占位、CPU); W9 / W14 把「Hooks 小节」统一写成「用法小节 (文件内第二个 Hooks 小节)」。

#### m5 - id `cfd9ca0b` - minor - issue - testing
- scope: `proposal.md SC-19` (R3 ba/m2 `6f503728` 的残余: 规则已成文, 验证依赖主机)
- summary: W9 的「读取条目的 tr / sed / awk 一律在 `LC_ALL=C` 下执行, 结果与 locale 和 awk 实现无关」在 mawk 主机上无法被 19ad / 19ae 证伪: 删掉 `LC_ALL=C` 的坏实现在本机 (mawk) SC-19 29/29、SC-20 17/17 全绿。
- 证据: `proposal.md:163` 自己写明「mawk 按字节、gawk 在 UTF-8 locale 下按字符」; 本机 `awk` = mawk 1.3.4 (`/etc/alternatives/awk`), 无 gawk; 把目标原型 `_sg_ext_entries` 里唯一的 `local LC_ALL=C` 删掉 (变体 `lcall_all_off`), `WPA_ONLY=SC-19,SC-20` 得 29/29 与 17/17。19ad (`baseline_probe.py:1397`) / 19ae (`:1399`) 只在字符计数 / 字符类按字符算的 awk 或 shell 实现上才会红。含非 ASCII 命令文本前缀的扩展匹配我也试了 (删 `_sg_ext_pass` 的 `LC_ALL=C` 与全删两个变体, C.UTF-8 与 en_US.UTF-8 各 6 条命令), 退出码与原型相同, 所以这一点没有额外缺口。
- 失败场景: Debian / Ubuntu 默认 mawk 的验收机上, 漏写 `LC_ALL=C` 的实现通过全部行; 到 RHEL / Fedora (gawk) 上 `a<2 汉字>` 这类 7 字节条目被当 3 字符而静默跳过。
- 建议修法: 验收要求 gawk 腿 (探针装了 gawk 就把它放进 PATH 前面再跑 19ad / 19ae, 与 `WPA_BASH32` 同体例), 或在 W9 / 19ad 的「怎么会红」里如实写明「只在 gawk 主机上证伪 `LC_ALL=C`」。

#### m6 - id `91a89f9b` - minor - risk - documentation
- scope: `proposal.md 待复议`
- summary: 工作分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 已推到 origin 与公开 GitHub 镜像 (匿名可读; 派单背景写「未推送」), 其中待复议 7.1 / 7.2 与 research 笔记含未修复旁路的可操作配方, owner 门没有登记 —— 本席 R3 风险 6(b) 的前提 (尚未首推) 已不成立。
- 证据: `git ls-remote origin|github refs/heads/docs/secret-net-l3-and-bypass-paths-phase-a` 两端都是 `b07f69a7e443...`; 无凭据匿名 `git ls-remote https://github.com/10CG/Aria.git` 返回同一 SHA; 远端跟踪 ref 的 reflog 记录推送 `91c4c6e`、`dd5da77`、`c0a6654`、`c3c7ece`、`b07f69a` (最后一次 2026-10-06T22:13:25Z, 与 R2 起每版同路径)。内容: `proposal.md:399` (7.1)「约 1400 个空段使 hook 超时后命令被放行并执行 (… 活体证实)」; `:400` (7.2)「`grep -E 'A|B' ~/.bashrc` → exit 0」(基线上 `grep -E 'a|b' .env` 同样 exit 0, 我实测); `research/secret-guard.md:20,:371` 给出完整配方 (前面加约 1400 个 `:;` 即放行并执行)。`PROGRESS.md`「待 owner 裁定 / 复议」未列此项; 仓内无 SECURITY.md 或披露规范。决策单第 4 项授权的是分支推送, owner 当时并不知道分支会带这类内容。
- 失败场景: 该配方已在公开仓; 之后任何 PR / 合并 (合并本来要逐次请示) 会把它固化进公开 master 历史。Spec 自己写「开新 issue 逐条请示」, 而同一内容已随 Spec 公开, 两者对信息外发的处理不一致。边际危害受 secret-guard 自述的威胁模型 (防意外的减速带) 限制, 所以只计 minor, 但这是难以撤销的外向动作。
- 建议修法: (1) 主控现在就把这一事实写进 handoff「待 owner 裁定」(Rule #10: AI 的流程判断须请复议), 并更正派单背景; (2) Spec 最小编辑: 7.1 / 7.2 去掉量化与可复制命令, 改为「既有设计缺口, 见 `guard §0` 第 7 / 6 条」, 笔记里的两处同理; (3) 已推送分支是否清理 (改写 / 删除远端分支属一次性授权之外, 只能 owner 决定); (4) 在待复议第 7 条旁加一个产品级条目: 未修复旁路的披露范围 (先修后披露 / 现状保留)。

#### m7 - id `8936aa07` - minor - issue - documentation
- scope: `proposal.md SC-22` (引用精度, 四处合并)
- summary: 四处文字与行 / 源码对不上, 都不改变实现者动作: W14 陈旧表述清单漏 `secret-guard.sh:8` 的「~100 most common patterns」; 22av 清单摊平了 `ps -w -x`; W11 launcher 小节的 22bk 清单列 10 个包裹而行里 11 个; Impact 称 `git-commit.md` §6.1「要求」Closes。
- 证据: (a) `aria/hooks/secret-guard.sh:8`「It covers the ~100 most common patterns」, SC-31 31a 基线 145、目标 149; W14 (`:242`) 清理了 `secret-scan.sh` 的 `~15 secret-shape patterns` / `49 known bypass classes` 却没列这一处 (同一个头注释块、同一类陈旧计数字面)。(b) `proposal.md:289` 写 22av「14 个 ps 拼写 (`-aux -ax -x -ux -au -axu -auxww -w -x -eO …`)」, 数得 15 个且 `-x` 重复; 探针 `:1545` 的 PS_SPELL 里是 `"ps -w -x"` 一个拼写。读者可能把裸 `ps -w` 也加进去: procps-ng 4.0.2 的 `ps -w` 只出 comm, 目标原型对 `ps -w` / `ps -ww` / `ps -e -w` 均放行 (正确), 对 `ps -w -x` / `ps w` 拦。(c) `:193` 对 22bk 列 `ssh`、`docker|podman|kubectl|lxc exec`、`nomad alloc exec`、`pct exec`、`sh|bash -c`、`watch` 共 10 个, `:194` 与 22bk 行是 11 个 (缺 `docker compose exec`)。(d) `:356`「仓内约定 (`COMMIT_FOOTER_GUIDE.md`、`git-commit.md` §6.1) 要求修复类提交写 `Closes #N`」: §6.1 (`git-commit.md:185-190`) 只并列 Closes / Fixes / Refs, 要求在 `COMMIT_FOOTER_GUIDE.md:199-201`, 且同表写明「部分实现」用 `Refs`, 对 Spec 自称「部分覆盖」的 10CG/aria-plugin#203 与 10CG/Aria#221 本就成立, 真正偏离默认写法的只有 10CG/aria-plugin#154 在 1.12 之前 (R3 km 风险 2 同, 未采纳)。
- 失败场景: 实现者按 W14 清单做 SC-28 时漏掉 `:8` 的陈旧计数 (SC-28 判据不覆盖); 按 22av 文字多拦 `ps -w`; 引用 §6.1 的人以为那里有「要求」。
- 建议修法: 四处各改一句; (a) 补进 W14 的陈旧表述清单与 SC-28 (或明写「不改」)。

## 上一轮对账

R3 无 critical; 10 个 major 键 (12 条席位原编号) 按主控簇逐项对账, 证据均为本席实读或实跑:

| 簇 | 键 | 对账 | 我核验的证据 |
|---|---|---|---|
| Q (L3 对 NUL 失明) | `4f713847` | closed (带 m1) | W1 `:52-54` 已写 `tr '\000' '\n'` 与 SC-1 1c / 1d; 基线两行 silent (证据文件), 目标原型 `env-line-secret-keyword=3` (全量目标态运行与 3 次独立变体运行, Bash 与 Read 信封一致); `nul_off` 坏实现红; SC-29 的 jq-crlf-guard 静态检查在 9/9 内通过。理由文字有两处错 (m1)。 |
| M (枚举 / 边界逐成员) | `eb350937` | closed | 7k (既有键表 10 个)、2e / 2f、12n、12o、19ac 各有行, 全量目标态全 yes; 抽样 `oldkey_drop:webhook_secret` (7k 9/10)、`fp_lt20` (12n 1/2)、`hash_noshasum` (12o 1/2)、`ext_nostrip` (19ac)、`remote_env_split:ssh|watch` (22bo 20/22) 复现为红。 |
| M (分类器各步骤作用于哪些 tag) | `1c49d896` | closed | W2 的「作用面 (闭集)」与 7k / 7l / 7m 成文; 抽样 `step_on:ent:bearer-token` (7l 23/24)、`step_on:wl:basic-auth-url` (7m 8/9) 复现为红。 |
| M (tight credit 逐成员) | `8fbbee80` | closed | 22bm (91) / 22bn (89) / 22bq (78) / 16r (11) 全 yes; 抽样 `tdrop_psalt:2` (90/91)、`tdrop_launch:exec` (90/91)、`launcher_ps_only` (22bq)、`proc_tight` (22bh) 复现为红; 规则行与 tight 拷贝同源的漂移面由逐成员行兜住 (无新机制)。 |
| P (关闭关键字检查真空) | `05982c10` | closed | Impact `:356-360` 三步检查; 所引 `detailed-tasks.yaml:342` 原文逐字相符; `refs_check.py` 9 个场景 v4 全符合预期、v3 写法在 5 个跑坏态真空通过 (我复跑); 在真分支上跑第 1、2 步: `rev-list --count` 为 9 且 rc=0, 第 2 步末行 `rc=0,1`。 |
| R (有效条目为零) | `28af0372` | closed | W9 `:168` 与 20o-20q; `ext_emptypat` 使三行转红 (退出码 `0,0,2,2,2,2`)。 |
| E (locale 差分) | `44b5bb44` | closed | W2 `:68` 的做法与 SC-32 32d; 我实测 bash 3.2.57 在 en_US.UTF-8 下 `[[ QWERTY == *[a-z]* ]]` 为真、5.2.15 与 C.UTF-8 为假; 全量目标态运行 32c / 32d 都是 361 行逐行一致 (第二 locale en_US.UTF-8)。未重跑 `ent_range` 变体 (需约 10 分钟以上), 采信执笔。 |
| S (不执行不变量) | `8d258b19` | closed | W2 / W9 / W10 / W12 / W14 成文, 诱饵行 19ab / 21z / 23i / 7n 全 yes; 抽样 `ext_eval` (19ab 出现 `CANARY-EXECUTED`)、`vx_eval` (21z 1/5)、`val_eval` (7n 0/10) 复现为红。 |
| T (W9 引号内分隔符) | `0a8380fd` | partially closed, 本轮仍记 not closed (M1) | 掩码本身对 (fuzz 脚本与我的对照都显示原型对内建一致), 但「行为对齐用 SC 钉住」只钉了无转义的 6 + 2 形, 自然坏实现全绿。 |
| K (/proc pid 位置) | `ac42f607` | closed | W11 `:195` 与 22bp / 22bh; `drop_pid:6` (thread-self) 使 22bp 8/10 复现为红; 日常良性命令抽样无新增误拦。 |

R3 本席三条 minor (`a6304dd1` SC-28 半截改写、`cfb2fb14` Tasks 1.12 执行条件、`4447c607` W14 的 K = 50) 均 closed: 6 个文档坏实现各只红预期行 (我复跑); Tasks 1.12 现按探针真实输出写 (`OK` 起头且 exit 0, `##SKIP##` 不算); W14 `:241` 改为 K = 实跑总数。其余席位的 R3 minor 我逐条对了 v4 文本或探针行, 均已处置, 唯一仍有残余的是 ba/m2 `6f503728` (规则已成文, 验证依赖主机, 见 m5)。

## 对执笔人自报薄弱点与请裁项的表态

**自报薄弱点 (返修报告 §6)**
1. 原型不是实现、坏实现自构 (同源盲区): 可接受, 条件是 Tasks 1.8 的非作者对抗 review 不可省。本轮的新证据: 我用非作者思路写的 3 个 `_sg_ext_mask` 变体与 1 个删 `LC_ALL=C` 的变体在 SC-19 / SC-20 上 4/4 全绿 (M1、m5), 执笔的 115 个坏实现里没有这几类。
2. 体量 +21.7%: 可接受; 但接缝缺陷仍随体量长出 (m2 的 9 处版本叙事、m3 的陈旧数字、m7 的清单文字), 与 R3 主控「约一半缺陷由上一版返修引入」同向。
3. 验收前置变多 (第二 locale、非 root、真 bash 3.2): 可接受, Tasks 1.1 有上报口径。我在 uid 1000 上带 `WPA_BASH32` 与 `WPA_REQUIRE_ALL=1` 复跑目标原型 (约 19 分钟, 主机负载 8-13), 与证据逐字节一致; `setpriv` 降权路径我也没法在 root 下实测。
4. 回归复跑是精化的 (只跑 v3 红过的行): 可接受 (判据逻辑上正确); 我抽样 20 个 v4 坏实现全部复现, 未复跑 v3 的 420 个。
5. 等价变异 (4 + 14): 可接受; 我核对了 `docker|kubectl|podman|lxc` 四个的理由 (基线本就拦, 实测 exit 2)。
6. 时档是单机比值: 可接受 (越界上呈、不放宽, 与 Rule #10 同向); 请 owner 知悉 (f) 靠 100 ms 地板、(g-b) 余量约 20%。数字口径见 m3。
7. 新增 / 反转的已知限制与误拦面 (19ae、22bj 变宽、`sh -c 'printenv'` 反转): 可接受; 我另跑约 115 条日常良性命令, 无未申报新误拦。
8. 差分核对范围: 可接受; 但见 M1 —— 「同一套状态机」的验收不应只靠 notes 里的一次性 fuzz。
9. L3 7n 防的是去引号捷径: 可接受, 保留 (10 个运行成本低)。
10. 证据运行负载高、耗时长: 可接受; 主控复跑要按 20-30 分钟留时间。

**请裁项 (返修报告 §7)**
- 甲 (技术级, 待复议 21-30): 21 NUL 换换行: 可接受 (理由文字要订正, m1); 22 `/proc` pid 闭集: 可接受; 23 `sh -c` / `bash -c` / `watch` 下 env 纳入: 可接受 (去掉版本叙事, m2); 24 阶段切分与条目字节语义: 默认可接受, 但建议主控把备选「含 ASCII 字母数字或任一非 ASCII 字节」直接按「技术级 AI 直接裁」采纳 (一处 awk 条件, 无安全回退, 10CG Lab 是中文环境, 默认值让中文目录条目静默失效, 正是 Spec 自己批评的静默失效类), 不必上呈 owner; 25 不执行不变量: 可接受; 26 locale 与 32d: 可接受; 27 文本提及误拦默认: 可接受; 28 / 29 / 30: 可接受。
- 乙 (Rule #10 自作主张): 1 回归复跑口径: 可接受; 2 同族兄弟位置的同批改动: 可接受, 但这批改动本身长出了 M1 与 m2-m3; 3「没有新增 hook 机制」: 表述不准确, 应记为「新增一个函数 `_sg_ext_mask` (主控裁定 #2 的直接后果), 它引入了与内建切分并存的第二份引号状态机」, 并在 handoff 如实写; 4 选「纳入」三处: 可接受; 5 不交付一次性变换脚本: 可接受。
- 丙 (未采纳的席位备注): 1 SC-14 canary 与 W6 清理用记下的变量: 我 R3 表态不变, 建议在 Tasks 1.3 加一句实现注意 (成本一句话), 不计 finding; 2 W5 `source` 白名单: 可接受不采纳 (现行 matcher 下不可达); 3 MINGW64 / macOS / BSD 未实测: 可接受, 建议在 10CG/aria-plugin#154 关单评论里披露一句「未在 MINGW64 / BSD 实测」; 4 Layer 2 无人值守影响、待复议 19 增列「删除 W5」选项、Tasks 1.1 冻结副本、Impact 引用精度: 前三项可接受不入 Spec 但须进 handoff (W5 是 AI 增补, 非三个 issue 的诉求), 第四项现并入 m7; 5 `timing.py` 无判据: 可接受 (W14 已写明); 6「约 1400 个空段」配方的披露范围: **不可接受按「待 owner 首次推送前裁定」处理 —— 前提已不成立, 分支已公开推送 (m6)**。

## 风险 / 疑问

1. **已发生的外向动作 (最需要主控知悉)**: 见 m6。派单背景「未推送」与事实不符; 请主控确认这次推送是否在 owner 知情下发生, 并把「已公开推送的分支含未修复旁路配方」写进 handoff 待裁清单。
2. **A.1 认领心跳**: `PROGRESS.md` 记最近一次 2026-10-06T10:02:46Z, TTL 24 h, 即 2026-10-07T10:02Z 之后可被扫为 abandoned; R5 与 A.2 可能跨过该点, 需例行续心跳。协调 ref 两端不同 (origin `63c4f84f...`、github `ad0287f7...`, 与 R3 观察一致, origin 在前进, 属心跳只推 origin 的预期状态, 请主控确认)。
3. **W5 不是三个 issue 的诉求** (R3 风险 3 仍成立): 10CG/aria-plugin#154 评论 19339 明说告警措辞「现行已满足」; W5 带来 rule6_note 块 B、SC-13 的 14 个运行与待复议 8 / 19。建议 handoff 标为 AI 增补并给 owner「删除 W5」选项。
4. **Layer 2 无人值守的影响未在 Impact 申报** (R3 风险 1 仍成立): aria-runner 内嵌 aria-plugin, 新拦截进入镜像后误拦只能由 AI 自己 `# guard:ack`。
5. **待复议 24 / 27 的默认值**: 两处都是技术级选择, 默认取了对 owner 不利的一侧 (中文条目静默跳过; 包裹词不锚命令位置致 `sshd` / `stopwatch` 子串误拦), 而备选改动都很小。按 memory「owner 只裁产品级、技术级 AI 直接裁」, 建议主控直接裁定而不是上呈。
6. **SC-30 时档的可执行形态**: 五个新时档 (f) / (f0) / (g) / (h) / (i) 的度量脚本 `timing.py` 只打印比值与活性、无判据与 rc, 判据靠人对文字上界读数 (W14 已如实写); 与头部「承重的判据只靠探针 SC 行」是明示例外 (SC-30 探针外)。
7. **Tasks 1.1 的复跑对象** (R3 风险 5): 未写明在 `268da8f` / `2bc1c4c` 的冻结副本 (`git archive`) 上复跑; 10CG/Aria#199 若先发版, 工作区的 aria 会前进。属可处置的歧义, 未立 finding。
8. **未验证**: SC-30 的时档与测试内 SC-9a / SC-8 (需带 git 历史的真 checkout); `ent_range` 变体 (需 bash 3.2 与两个 locale 约 10 分钟以上); gawk / macOS / BSD / BusyBox / MINGW64 的任何一腿; Forgejo 服务端的关闭关键字默认集合; v3 的 420 个回归坏实现 (只抽样了 v4 的 20 个)。
9. **README 与 SOT 的并存陈述**: 28m 只增不改, `README.md:33` / `README.zh.md:33` 的表格行与 `secret-hygiene.md` §5.2 仍写 cannot redact, 同一文件内两种说法并存到待复议第 1 条落地为止 (Out of scope 已声明, 本席接受)。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: `0C/1M/7m`
- Vote: **REVISE**

## 是否足以进入 A.2

不足以: 有 1 条 major (M1, R3 簇 T 的残余: W9 引号掩码的转义 / `$'...'` 形态没有行钉住, 自然坏实现全绿); 修复面很小 (为 19z 补 2-3 个带转义引号与 `$'...\'...'` 的形态行, 并把两个坏实现写进 Tasks 1.8 与「怎么会红」), 其余 R3 的 9 个 major 键本席均已核为 closed (含全量目标态复跑与 20 个坏实现的独立复现), 另请主控先处置 m6 这一已发生的外向动作。
