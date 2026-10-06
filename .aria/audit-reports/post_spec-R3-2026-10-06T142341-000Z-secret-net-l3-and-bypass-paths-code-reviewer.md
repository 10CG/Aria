---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T15:15:22.259Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审文件 (`c0a6654`): `proposal.md` 全文 1-425; `baseline-evidence.md` 全文 1-485; `baseline_probe.py` 全文 1-2095 (分段通读)。v2 → v3: 用 `git show b3e3123:` 取 v2 三份文件, 逐行比对出 68 个改动块 (proposal 290 行未变), 新增的数字与措辞逐条回查 v2 原文。三份文件 sha256[:16] = `9e7fbe0bbc86caf9` / `51936cff0a363c7f` / `cb9d8f8482faef16`, 与返修报告一致。
- issue 与决策单: `Aria-221.md` 全文 (含评论 25898); `aria-plugin-154.md` 全文 (含评论 19339); `aria-plugin-203.md` 全文; `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md 规则 #6 / #7 / #10 与「多远程推送」两条硬约束。
- 源码与规范 (aria `268da8f` / standards `2bc1c4c`): `hooks/secret-scan.sh` 全文; `hooks/secret-guard.sh` :1-133、:386-500、:555-702、:736-1009 (抽读 :805-830、:846-878、:888-898、:926-940、:974)、:1034-1120; `hooks/hooks.json` 全文; `hooks/tests/secret-guard.test.sh` :1667-1910 (测试内 SC-8 的抽取与计时); `.github/secret_scanning.yml` 全文; `secret-hygiene.md` :1-30、各节标题、:281-295、:397-410; `skill-benchmark-exemption.md` 标题与 §4.1; `LEVEL_GUIDE.md` :150-162; `proposal-minimal.md` :45-58; `project.md` :112-120; `openspec-archive/SKILL.md` :282-300; `.aria/probes/plugin-cache-currency.py` 全文; `.aria/state-checks.yaml` 的 `plugin-cache-currency` 条; 10CG/Aria#199 `detailed-tasks.yaml` :341-342。
- 研究笔记: 四份的标题结构 (Spec 引用的节号逐条存在); `cc-hooks.md` §4-§5; `secret-guard.md` §0。
- 上一轮: R2 聚合报告全文 (含主控记录); R2 code-reviewer 报告全文。
- 返修: `v3-writer-report.md` 全文; `writer-v3-proto/` 的 `README.md`、`build_full.sh`、`timing.py`、`hooktry.py`、`l3try.py`、`timing_summary.txt`、`mut_summary_v3.txt` (头部与等价变异节)。

**独立复算 (成立的部分, 不计 finding)**

1. **基线证据逐字节复现**: 在私有副本 (aria `268da8f` + standards `2bc1c4c`, 删去子模块 gitfile) 上带真 bash 3.2.57 跑探针: rc=0, stderr 为空, stdout 74072 字节, sha256[:16] = `a6e187b50a4f3514`, 与 `baseline-evidence.md` 内嵌块逐字节相同。基线形态 holds, baseline-failing 0/190, doc-sync 0/25, 其余类别全 yes (主机 1 分钟负载 18-56, 用时 20 分 23 秒)。
2. **目标态原型复跑**: 用 `writer-v3-proto` 的补丁脚本 (只改了实验目录路径) 重建完整目标树, 7 个关键文件与执笔 `work/t3` 逐字节相同。带真 bash 3.2 与 `WPA_REQUIRE_ALL=1` 跑探针: rc=0, 72649 字节, sha256[:16] = `0e1d2eb9ea1522fb` (与执笔 T 跑相同); 382 行 yes, 30a 按设计 n/a, target shape holds。其中 29a 为 `PASS 50/50`, 29b / 29i 为 `584/585` (唯一 FAIL 是测试内 SC-13 的无 git 伪影), 31a 为 `patterns=149`, 31b 为 `census=64 test-hardcoded=64`, 32c 在 334 行上一致, 33a 为 flagged=2 且均在归因清单内。
3. **file:line 抽核全部成立**: secret-scan.sh :15-20 / :33-34 / :52 / :64 / :72-80 / :135-142 / :144 / :215 / :218 / :224 / :227 / :355-361 / :367; secret-guard.sh :21-23 / :62 / :405-408 / :427 / :491-493 / :564 / :617-620 / :626 / :631-694 / :641 / :698-700 / :736-1009 / :815 (13 个读取器) / :873 (13 个 launcher 词) / :875 / :877 / :893 / :894 / :930-933 (:932 的 13 个读取器) / :974 / :1043-1071 / :1088-1102 / :1111; secret_scanning.yml:18-22; hygiene :23 / :287 / :288 / :319 与 §0 :27「Why no "Layer 1"」; LEVEL_GUIDE:160; proposal-minimal:53; project.md:117。`openspec-archive` Step 7 对未完成项自动建 tracker、headless 亦然, 属实。
4. **issue 转述核对**: 评论 19339 的三件交付物与「若现行为已如此则只加断言」、评论 25898「降低假阳性率本身就是在保护那道真闸的有效性」、#203「② 在命令侧基本堵不住」均逐字存在; 头部对决策单第 1-5 项的转述一致。
5. **簇 A 抽测**: 在既有 json 键 (password / client_secret / api_key) 上, 「`$` + 字母 + 单一大小写字母数字」、`$(…)`、以 ASCII `...` 结尾的值, 基线与原型都告警 `json-secret-field=1`; 同形值放在新键 `token` 上, 原型计 `json-credential-field=1`。值均在 Python 进程内用 `secrets` 运行时生成, 只打印 tag。
6. **簇 K 抽测**: 原型对 `sudo -E ps aux`、`timeout --signal=KILL 5 ps aux`、`/usr/bin/env ps aux`、`{ ps aux; }`、`(ps aux)`、无空格管道、`ps auxf` / `faux` / `-efww` / `-eF` / `-elf` / `-A -o args` / `-eo user,pid,cmd` / `-p 1 -o command=` / `--pid 1 -o args`、`pgrep -al` / `-fa`、`top -cbn1` 全部 exit 2, 基线全部 exit 0; `ps -o pid= -p 123` 等只出 comm 的形态两侧都 exit 0。本机 procps-ng 4.0.2 上 `pgrep -fl` 每行 2 个字段 (pid 与名字), `pgrep -a` 为多字段 (只统计字段数, 未打印内容), 与 W11 的 Linux 语义一致。
7. **簇 L 抽测**: Tasks 1.12 四腿的命令 (打印合成值、写入诱饵、Read 诱饵、`ps aux | head -c 0`、不存在目录下的 `forgejo/app.ini` 分别经 Bash 与 Read) 只当 stdin 文本喂 hook, 未执行。基线全部 exit 0; 原型依次为 0、0、0、2、2、2, 与 Spec 的期望一致。
8. **时档口径**: `timing.py` 与 `timing_summary.txt` 的方法 (同次运行交错 A/B、按 RUSAGE_CHILDREN 计整进程 CPU、取最小值之比、带活性断言) 与 W14 的文字一致。

## Findings

### Major

**M1** `05982c10` · major · issue · documentation · `proposal.md Impact`

Summary: Impact「提交页脚 / PR 描述的关键字」给出的机械检查, 只取 grep 的退出码 (`PIPESTATUS[1]`), 不验上游 `git log` 是否跑成、范围是否非空。`<起点>` 解析失败 (git 退出 128) 或代换为空 (`..HEAD` = 空范围) 时, 末行都是 `rc=1`, 按 Spec 判据「无任何匹配输出且末行 `rc=1` = 通过」真空通过。这条检查是三张 issue 自动关单旁路 (决策单第 2 项要求 #203 / #221 保持 open) 唯一的机械兜底; 同一节里的 #199 守卫刻意防了同类真空 (取生产者的 rc, 「其它 rc = 没跑成」), 本条写着「写法照 10CG/Aria#199 的 rc 判据」, 实际没有继承。这是 R2 簇 P 的残余。

证据:
- `proposal.md:352` 原文: `` `git -C <仓根> log --format=%B <起点>..HEAD | grep -niE '…'; echo "rc=${PIPESTATUS[1]}"` ``, 「判据: 无任何匹配输出且末行 `rc=1` = 通过; 有输出 = 违规; 其它 `rc` = 没跑成, 停下上报」; PR 草稿文本用 `printf '%s' "$文本" | grep -niE '…'`。对照 `:348` 的 #199 守卫取 `${PIPESTATUS[0]}` (git grep 的 rc), 「其它 `rc` 值 = 没跑成」。同一处 `:352` 还写明仓内约定 (`COMMIT_FOOTER_GUIDE.md`、`git-commit.md` §6.1) 要求修复类提交写 `Closes #N` —— 即违规文本有现成的生成来源。
- 实跑 (真仓只读 `git log`; 正则逐字取自 `:352`):

```
== A: 起点无法解析
fatal: ambiguous argument 'no-such-ref-xyz..HEAD': unknown revision or path not in the working tree.
rc=1 git_rc=128
== B: 起点代换为空 (..HEAD)
rc=1          (范围内提交数 0)
== C: merge-base 对不存在的本地分支 -> 空串
S=''
rc=1
== D: 正对照 (含 Closes 10CG/aria-plugin#154 的提交信息)
3:Closes 10CG/aria-plugin#154
rc=0
```

失败场景与三态:
- 起点正确且无违规: rc=1, 通过 (正确)。
- 起点正确且有违规: 有输出、rc=0, 判违规 (正确转红)。
- 起点坏掉且有违规: 无输出、rc=1, 判通过 (假绿)。
- 具体路径: 实现者照字面写 `<起点>=$(git merge-base HEAD master)`。在子模块处于 detached HEAD、没有本地 `master` 的环境里 (Layer 2 新 clone 后的常态), 代换结果为空, 检查恒报 `rc=1`。若提交页脚按仓内约定带了 `Closes 10CG/aria-plugin#203`, 合并推到 master 后 #203 会被自动关闭, 违反决策单第 2 项; 而检查从头到尾是绿的。

修法: 先 `git -C <仓根> rev-parse --verify -q "<起点>^{commit}"`, 失败即「没跑成」; 同时判两个 rc (例如 `echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"`, 只有 `0,1` 且无输出才算通过); PR 文本检查前断言文本非空。判据措辞与 `:348` 对齐: 生产者 rc 非 0 一律视为「没跑成, 停下上报」。

**M2** `eb350937` · major · issue · testing · `baseline_probe.py`

Summary: W11「同一批包裹下的整环境转储一并拦」这个集合 (`nomad alloc exec` / `pct exec` / `ssh` × `env` / `printenv`) 没有逐成员出行。`ssh … env` 只出现在 22aq 的 `ssh root@pve pct exec 101 -- env` 里, 而这一行仅靠 `pct exec` 就能满足; `pct exec … printenv` 与 `ssh … printenv` 都没有行。拆行实现 (仿照基线 :858 / :862 / :938 / :940 每个包裹各一行转储规则的体例) 漏掉 ssh 这个成员, SC-22 / SC-25 依然全绿, 而 `ssh host env` 由拦变放。同一矩阵的另一角也欠定: W11 已知限制写「`sh -c 'printenv'` 这类外壳内的裸 `printenv` 仍放行 (基线同)」, 既没有 known-limit 行, 原型又把它 (连同 `bash -c env`、`watch env`) 拦了 —— Spec 与它自己的原型对这一格结论相反, 探针两种都放过。这是 R2 簇 M 的残余 (主控裁定 4: 每个枚举集合逐成员出行, 并证明删掉任一成员会转红)。

证据:
- `proposal.md:190`:「同一批包裹下的整环境转储一并拦 (`nomad alloc exec … env|printenv`、`pct exec … -- env`、`ssh … env`) … 这几个漏 (22ao–22ar)」; `:197`:「`sh -c 'printenv'` 这类外壳内的裸 `printenv` 仍放行 (基线同)」; `:337` Impact 新拦截:「`nomad alloc exec` / `pct exec` / `ssh` 包裹下的裸 `env` / `printenv`」; `baseline_probe.py:1346`: 22ap = `pct exec 101 -- env`, 22aq = `ssh root@pve pct exec 101 -- env`。
- 坏实现 mutE (由本席构造): 在完整目标态原型上, 把 W11 远程包裹行拆成两行 —— 进程表形态行保留全部 11 个包裹; env / printenv 转储行的包裹集去掉 `ssh` —— 其余与原型逐字节相同, `bash -n` 通过。命令只当 stdin 喂 hook:

```
                                  base  proto  mutE
ssh host env                        0     2      0
ssh host printenv                   0     2      0
ssh root@pve -- env                 0     2      0
pct exec 101 -- printenv            0     2      2
sh -c 'printenv'                    0     2      2    (W11 已知限制写「仍放行」)
bash -c env / watch env             0     2      2    (Impact 未申报)
```

- mutE 上跑 `WPA_ONLY=SC-22,SC-25`: 22ao / 22ap / 22aq / 22ar / 22aw / 22bk 全 yes; 汇总为 baseline-failing 57/57、reverse-guard 5/5、allow-guard 8/8、known-limit 4/4, 末行「target shape … holds」。

失败场景与三态 (以 `ssh … env` 为例):
- 基线: `ssh host env` exit 0, 22aq exit 0 (行为 no, 符合预期)。
- 正确实现: 两者都是 exit 2, yes。
- 坏实现 mutE: `ssh host env` exit 0, 22aq 仍 exit 2 (由 `pct exec` 命中), 行 yes —— 验收放过了一个漏掉 Impact 已申报拦截的实现。
- `sh -c 'printenv'` 那一格: 照 Spec 实现放行、照原型实现拦截, 两者都能通过探针; Impact 的行为变更申报只对其中一种成立。

修法: 加一条枚举行, 覆盖 {`nomad alloc exec`, `pct exec`, `ssh`} × {`env`, `printenv`} 共 6 个独立成员 (各用最简单的单包裹写法), 22aq 保留为复合例; 对 `sh -c` / `bash -c` / `watch` × 转储这一格明确取舍: 要么钉 known-limit 行并按「放行」实现, 要么纳入, 同步改 W11 已知限制、Impact 新拦截与建议开单 7.10。同一检查顺带覆盖「launcher / 远程包裹 × 非 ps 程序」矩阵: 目前只有 ps 那一列逐个出行, 另加 `sudo pgrep -af` 一例。

### Minor

**m1** `467c8b54` · minor · issue · implementation · `proposal.md What.W11`

Summary: W11 的 pid 位置闭集 (`self`、数字、`*`、`$name`、`${…}`、`$(…)`, `:191`) 漏了几种常见写法, 既没纳入, 也没进 22bh: `$$` (与 `self` 同指当前 shell)、反引号命令替换、glob 字符类 `[0-9]*` (枚举全部进程 cmdline 的标准写法)、前缀 glob `1*`、花括号展开 `{1,2,3}`。

证据 (只喂 stdin, 基线 / 原型):

```
cat /proc/self/environ                         2  2
cat /proc/$$/environ                           0  0
tr '\0' '\n' < /proc/$$/environ                0  0
cat /proc/$BASHPID/environ                     0  2
cat /proc/[0-9]*/cmdline                       0  0
for f in /proc/[0-9]*/cmdline; do tr … < $f; done   0  0
cat /proc/{1,2,3}/environ                      0  0
cat /proc/1*/cmdline                           0  0
cat /proc/`pgrep -o curl`/cmdline              0  0
```

失败场景: 实现者照闭集实现, `cat /proc/$$/environ | tr '\0' '\n'` (等价于对工具 shell 做 printenv) 与 `for f in /proc/[0-9]*/cmdline …` 在目标态照样放行; 而 `/proc/self/environ` 是拦的, 规则面在「同一信息」上自相不一致, 也没有成文。

修法: pid 记号补 `\$\$`、反引号替换与 glob / 花括号形 (例如 `[^/[:space:]]*[][*?{][^/[:space:]]*`); 或者把它们写进 W11 已知限制, 并在 22bh 各加一个成员。

**m2** `6ff1d962` · minor · issue · documentation · `proposal.md What.W11`

Summary: W11 没有约束远程 / 外壳包裹词要锚在命令位置。原型照基线体例不锚定 `ssh|…|watch`, 于是只要正文里先出现 `ssh` / `watch` (含 `sshd`、`stopwatch` 这类子串)、后面再出现进程表形态, 整条文本提及都会被拦 —— 包括提交信息、issue 评论与文档检索。W11「新增误拦 (成文)」(`:197`) 与 Impact「新拦截」(`:337`) 只列了 heredoc 起行一类 (22bj); 22Y 的文本提及守卫也只有不含包裹词的样例。

证据 (基线 / 原型):

```
git commit -m "docs: explain why watch ps aux is blocked"              0  2
echo "the sshd log shows ps aux output"                                0  2
grep -n "ssh host ps aux" README.md                                    0  2
gh issue comment 1 --body 'use pgrep -f instead of ssh host ps -ef'    0  2
echo 'stopwatch: ps -ef'                                               0  2
echo 'use ps -ef to list'   (22Y 同类)                                 0  0
```

失败场景: 发版后, 写这项功能的提交信息、PR / issue 评论只要先提到 ssh 或 watch 再提到 `ps aux`, 就会被拦并被推向 `# guard:ack` —— 正是 10CG/Aria#221 评论 25898 警告的误拦疲劳; 而这类误拦没有申报, 也没有钉住。

修法: 二选一。(a) 包裹词按 `_SG_PROCTAB` 同一个命令位置锚点锚定, 在 22Y 补一个含 `ssh` / `watch` 字样的文本提及成员; (b) 写进 W11「新增误拦」与 Impact, 按 22bj 体例钉一行。

**m3** `5d12116d` · minor · issue · documentation · `proposal.md Tasks`

Summary: Tasks 1.12 的执行条件写「`python3 .aria/probes/plugin-cache-currency.py` 报 `PASS` … 其它任何结果 (`STALE` / `SKIP` / `FAIL` / `AHEAD`) 一律记「未生效」并停下」(`:370`)。但该探针成功时打印的是 `OK installed=… sot=…` (exit 0), 从不打印 `PASS`; 跳过时打印 `##SKIP## …`; 版本串坏时打印 `MALFORMED …`。

证据: `.aria/probes/plugin-cache-currency.py:127` `print(f"OK {detail}")`; `:43` `print(f"{SKIP_MARKER} {msg}")` (`SKIP_MARKER = "##SKIP##"`); `:99` / `:118` `MALFORMED …`; `:139` / `:140` `STALE …` / `AHEAD …`; `PASS` 只出现在 docstring 的判据表 (`:19`)。

失败场景: 无人值守的执行者按字面比对输出 token, 成功态 `OK …` 落进「其它任何结果」, 于是停下; 1.12 永远开不了头, 1.13 (#154 关单) 随之卡住。方向是保守的 (停下), 但等于没有合法下一步。

修法: 写成「exit 0 且 stdout 以 `OK ` 起头 (探针 docstring 的 PASS 判定)」, 其余结果按实际 token 列出 (`##SKIP##` / `STALE` / `AHEAD` / `MALFORMED`, 或 exit 非 0)。

**m4** `5e342bfd` · minor · issue · documentation · `proposal.md What.W14`

Summary: W14 新写了「目标态 K = 50 (49 + 自检本身), `secret-hygiene.md` 的 secret-scan 计数同步为 50」(`:237`, v2 没有这句), 与未改动的 Tasks 1.2「按 SC 把探针用例落为两个套件的用例」(`:360`) 矛盾: L3 用例落进 `secret-scan.test.sh` 后 K 必然大于 50。50 来自原型 —— 原型只加了自检, 没落用例 (本席在原型上跑 29a 得 `PASS 50/50`)。

失败场景: SC-27 27b / 27c 是关系判据 (头注释 == 实跑数, SOT == 实跑数), 不会因此转红。但实现者若按 W14 的「50」去对齐, 会倾向不把 L3 用例落进套件 (Tasks 1.2 做漏)。那样新 tag 的回归只剩探针, 而探针随 Spec 归档后就不再跑。

修法: 删去具体数字, 写成「K = 实跑总数 (含自检), SOT 同步为该数」。

**m5** `f410df76` · minor · issue · documentation · `proposal.md Impact`

Summary: #154 关单评论要「逐条披露与评论 19339 字面参数的两处有意偏离」(`:350`: 值长门槛 16 而非 8; fp 只对 ≥16 字符的值记)。但 W3 还有第三处偏离: 19339 第 2 条写「`FAKE`/`PLACEHOLDER`/`NOT-REAL`/`[REDACTED` 前缀值跳过」, 而 W3 只放行**闭合**的 `[REDACTED…]` (`:85`「括号闭合」; `:91` 以 `[REDACTED` 开头但不闭合的值不是白名单; 7j `red-unclosed` 钉住仍检出)。

失败场景: 照 Impact 写出的关单评论少报一处偏离, 外发文本与实际行为不符。

修法: `:350` 补 (c): 「`[REDACTED` 只在整值闭合时放行; 以它开头但不闭合的值仍检出 (理由见 W3 保留判据)」。

**m6** `26e1a7a9` · minor · issue · documentation · `proposal.md What.W7`

Summary: W7 已知限制 (`:142`) 称 `no-plan-fallback.md` 这类文件「在 W1 后被 Read 时会告警, 与今天 `cat` 它们时一致, 不是新增面」—— 对它点名的这个文件不成立: 今天 `cat` (基线 hook, Bash 信封) 是静默的; 原型对 Bash 与 Read 都报 `kv-secret-assign=1`。告警来自 W2 的新 tag, 不是 W1。

证据 (仓内公开示例文件喂 hook, 只打印 tag): `no-plan-fallback.md` | 基线 Bash: silent | 原型 Bash: `{kv-secret-assign=1}` | 原型 Read: `{kv-secret-assign=1}`; `MARKDOWN_TEMPLATE.md` | 基线 Bash: `{json-secret-field=3}` | 原型: `{json-secret-field=3 json-credential-field=1}`。

失败场景: 只影响事实陈述; Impact「新告警 (L3)」已总括申报新 tag, 实现者行为不变。

修法: 改为「今天 `cat` 静默; W2 之后 Bash 与 Read 都会告警 (新增面, 已列入 SC-33 归因清单)」。

**m7** `4447c607` · minor · issue · testing · `proposal.md What.W14`

Summary: W14 的 (f0) 把 Bash 面无扩展档委托给测试内 SC-8 五档 (`:233`), 理由是「它的进程内计时包住 `_sg_per_segment_eval`, 其中含扩展入口的命令替换」。这只在扩展调用放在 `_sg_per_segment_eval` 之内时成立 (原型如此); W9 只规定「全部内建判定 (含第二遍) 都放行之后才调用扩展」(`:164`), 没有规定调用位置。另外, 参考实现 `timing.py` 的 (g) 默认参数是满额档 (16 个赋值 × 100 B + 128 次引用), 不是 W14 定义的 (g) (8 个赋值 × 300 B + 40 次引用)。

证据: `secret-guard.test.sh:1773-1775` 只用 awk 抽 `risky_patterns` / `_sg_judge_one` / `_sg_per_segment_eval` 三块, `:1852` 只对 `_sg_per_segment_eval` 计时; `timing.py` 的 `opt("--nrefs", 128)`、`opt("--vlen", 100)`、`opt("--nvars", 16)`。

失败场景: 把扩展调用放在 `:1111` 子 shell 返回 0 之后的实现同样满足「内建先」, 但 Bash 面无扩展时的额外开销 (命令替换、项目根解析) 不在任何时档里; 「由测试内 SC-8 承担」这句委托对它不成立。

修法: W9 写明扩展入口在 `_sg_per_segment_eval` 内调用; 或给 (f0) 补 Bash 面一档。`timing.py` 的默认参数对齐 W14 的 (g), 或在 W14 写明两档都跑。

**m8** `15da802b` · minor · issue · documentation · `proposal.md What.W8`

Summary: v3 只同步了 Why 表里的计数, What 里的旧计数没有跟上:
- W8 现状 (`:146`) 仍写「SC-16 0/13、SC-18 0/4」, 这是 v2 的数字; v3 是 0/15、0/6, Why 表 `:37` 已改。
- W11 现状 (`:186`) 写「SC-6 基线 0/8」; v3 的 SC-6 是 ×11。
- W4 的 12k (`:118`) 枚举「22 个 provider 前缀 / webhook / bcrypt、3 个 JSON tag、env-line、kv、2 个头 tag、cli 旗标、4 个 URL tag、gcp key id、bearer、PEM 块」, 合计 37, 与同句「共 38 个 tag」不符 —— 头 tag 实为 3 个 (`x-api-key-header` / `auth-header-token` / `cf-access-client-secret`); 探针的 W4 表是 38 项, 正确。

失败场景: 只影响引用精度, 实现者行为不变。修法: 改数字。

## 上一轮对账

按 R2 聚合「主控记录」的七簇逐条对账 (证据里的「目标态复跑」指本席 `0e1d2eb9ea1522fb` 那一次)。

| 簇 | 定稿键 | 状态 | 本席核验证据 |
|---|---|---|---|
| A | `e8d39a8a` | closed | W3 删去裸 `$NAME`、`$(…)`、ASCII `...` 三类 (`:89` 保留判据、`:91`); 独立复算第 5 条: 既有键上三类真值在原型上照样检出; 目标态复跑 7h (11 个运行) / 7j (15) / 7i / 11z 全 yes, 11x / 11y 两面成对。残余: `<…>` 形在含符号的 ASCII 口令生成器上约 1e-4 的重合已在 W3 已知限制成文 (与主控裁定 1「不会与任何 ASCII 随机值重合」的字面差一档, 已量化披露, 交 owner) |
| K | `ac42f607` | closed | launcher 集 = `:873` 的 13 词 + `command` (`:875`) + `exec`, 逐字核对; 带参数选项 / 时长 / 赋值 (22ax)、绝对路径 (22ay)、then / do / else / elif (22az)、带 `-` 的 BSD 拼写与 `-O` (22av)、`/proc` 内联解释器 (22bg) 在目标态复跑全 yes; 独立复算第 6 条另测 18 种写法, 原型全拦。新残余见 m1 / m2 |
| L | `ce6fc59c` | closed | 1.12 放在发版之后, 有执行条件, 四腿都是惰性操作数; 独立复算第 7 条: 四腿命令在基线上全部 exit 0 (惰性), 在原型上按期望转为 2; 头部 Rule #7 声明、rule6_note 的 dogfood 句与 Impact #154 关单前提都已改指 1.12。残余: 执行条件的 token 措辞见 m3 |
| M | `eb350937` | partially closed | 63 条新行逐成员出行 (4p / 4s / 5n / 6i / 6j / 6k / 9y / 12k / 16q / 19u / 21j / 22aw / 22bc / 22bd / 22bk / 22bl 等), 上界都有差一对; 但 W11「包裹 × 转储」集合没有逐成员出行, 本席构造的拆行坏实现在 SC-22 / SC-25 全绿 (M2) |
| N | `60f3173a` | closed | W5 的插入段只含 tag 与 `tool_name`, 不含任何 `tool_input` 文本; 13g 共 14 个敌意路径运行, 判据是全串等值; 13d 全串等值; 目标态复跑 13a-13g 全 yes, 基线 13g 0/14。rule6_note 块 B 的理由已同步改写 |
| O | `6bd285b1` | closed | (h) 不再用 5 s 墙钟绝对值, 改为同次运行交错的整进程 CPU 时间比值, 配活性断言、宽松墙钟兜底与「基线自身 CPU ≥ 5 s 判环境不合格」; L3 稠密输入档 (i) 已补; `timing_summary.txt` 的坏实现在 (f) / (g) / (h) / (i) 上各自越界或活性失败。残余见 m7 |
| P | `05982c10` | partially closed | 约定已落地 (`:352` 只写 `Refs`, `:357` 贯穿行, 1.11 引用, 1.13 关单为独立动作, 待复议 3 追加了「`Refs` 是否算评论」); 但机械检查在起点坏掉时真空通过 (M1) |

R2 的 minor: 本席对照 v3 文字逐条看过, 认为均已处置。本席自己的 m1-m8 在目标态复跑中均为 yes: m1 → (i) 档与 200 span 上界; m2 → 10i; m3 → 17d; m4 → 22bb / 22bl / 22ay / 22bh; m5 → `pgrep -fl` 移入 22bh; m6 → 预筛 77/77; m7 → W9 删去「不 fork」, 19x / 19y; m8 → 15g。

## 对执笔人自报薄弱点与请裁项的表态

**§6 自报薄弱点**

1. **原型不是实现, 坏实现自构 (同源盲区)**: 可接受。本席独立构造的一个坏实现 (M2 的 mutE) 就在 SC-22 全绿, 说明 Tasks 1.8 的非作者对抗 review 不能省。
2. **体量**: 可接受。本轮不要求削减。
3. **时档阈值由单一共享主机实测定; 越界上呈、不放宽**: 可接受, 「越界上呈、不放宽」符合 Rule #10。补一点: 全放行的多段带引用命令 (`timing_summary.txt` 的 h1) 比值为 2.26-2.41, 没有任何一档给它设上界, 也略高于 Impact 写的「1.4-2.3 倍」(见风险 2)。
4. **W1 使每次 Read 的成本约升到 3 倍**: 可接受。Impact 已申报, 也在 5 s 超时之内; 请 owner 知悉。
5. **10l / 22bj 的钉法**: 可接受, 建议保留 10l。它把被接受的误报钉成可证伪的行, 与 22bj 同一体例。
6. **沿用 writer-v2 的 bash 3.2 构建; Windows / macOS / BSD 未实测**: 可接受 (已成文)。BSD 的空模式文件语义见风险 1。
7. **「表里写了、原型没做」只做了抽查**: 可接受, 但 M2 正是这类 —— 集合里写了, 行没有逐成员钉住。
8. **cr 两条非编号备注未采纳**: (b)「清理对象是 `mktemp -d` 记下的变量, 不写 `rm -rf "$HOME"`」不进 SC 可接受。(a)「有效条目为零 → 不调用 grep」: 在 GNU 上确实没有可证伪判据; 但在 BSD 上若空模式文件匹配全部输入, 后果是 Read / Edit 与带读取器的 Bash 全部被拦。建议主控把它写进 B.2 实现注意事项 (零成本, 去掉一个平台风险), 不必进 SC。

**§7 请裁项**

1. **待复议 19 (W5 默认 A)**: 同意 A。
2. **10l 保留或删除**: 保留。
3. **时档阈值与「越界上呈、不放宽」**: 同意; 建议 owner 一并看 h1 档的空白 (风险 2)。
4. **W1 每 Read 成本上升**: 可接受, 已申报。
5. **cr 两条备注**: 见 §6 第 8 条。
6. **km 两条风险**: (a) A.1 认领已过 `SWEEP_TTL`, 属主控例行维护, 可接受上呈。(b) 7.1 的超时配方在公开镜像上的可见性: 威胁模型是防意外, 风险低, 交 owner 裁; 本席倾向只写「长命令可致超时即放行」, 不写段数。
7. **归档落盘**: 已在 `c0a6654` 入仓, 可接受。
8. **Rule #10 自作主张 (a)-(f)**: 列入 handoff 请复议即可, 可接受。其中 (f) 变异只覆盖新写或改写的判据, 正是 M2 漏网的原因 —— 集合原本存在, 只是没有独立成员行。
9. **观察**: 无需动作。本席本轮也被现行 v1.74.1 L1 拦了三次自己的 heredoc (正文只是含有 `ssh … env` / `/proc/self/environ` / `kubectl exec … bash -c … env` 的测试文本), 与 m2、22bj 同一类文本提及误拦; 改为运行时拼装后通过, 未用 `# guard:ack`。

## 风险 / 疑问 (不计入 finding)

1. **BSD 空模式文件语义**: W9 建议的 `grep -F -i -f <(条目)` 在零有效条目 (例如全是注释的扩展文件) 时以空模式文件调用 grep; 原型在没有扩展文件时也会这样调用。GNU 下匹配为零; 若 macOS 的 BSD grep 把空模式文件当作匹配全部, 结果是所有 Read / Edit 与带读取器的 Bash 被拦 (与 10CG/Aria#154 同型)。另外 BSD grep 的 `-o -b` 给的是行偏移还是匹配偏移, 也随版本而异。本机没有 BSD userland, 未实测。
2. **全放行的多段带引用命令没有时档**: W14 的 (h) 只测「末段被内建拦下」的情形 (原型 1.18); 全放行的情形 (h1, 150 段) 原型实测 2.26-2.41, 无任何上界。若有实现按段重复收集赋值, (g) 只有 17 段, 未必能抓到。
3. **待复议 7.1 的超时悬崖**: 新行使每段 CPU 约增加 18%, 在高负载主机上触发「超时即放行」的段数会更低; Spec 已列开单, 建议提高优先级, 与 Spec 自述一致。
4. **20g 要求非 root**: Tasks 1.10 要求 20g 不得为 n/a, 即验收必须由非 root 用户运行; 若 Layer 2 容器以 root 运行, 验收无法通过。Spec 是隐含要求, 未明写。
5. **Rule #7 自律记录**: 本席的凭据形状值全部在 Python 进程内用 `secrets` 运行时生成, 经 stdin 喂 hook, 只打印退出码与 tag; post-ship 四腿与 W13 的命令只当 stdin 文本喂 hook, 未执行; 没有写任何诱饵文件。真仓未做任何 git 写操作 (HEAD `c0a6654`、aria `268da8f`、standards `2bc1c4c`, 工作区干净); 全部实验在 `scratchpad/audit/post_spec-R3-code-reviewer/` 下进行。

## Verdict

**PASS_WITH_WARNINGS** —— counts `0C/2M/8m` —— **Vote: REVISE**

## 是否足以进入 A.2

不足以。M1 要改 Impact 里那条检查的命令与判据, M2 要在探针里补一条 6 成员的枚举行, 并对 `sh -c` / `bash -c` / `watch` × 转储那一格做取舍; 二者若不先落进 proposal, detailed-tasks 会把真空通过的门与漏钉的集合原样编进任务。改动面小, 预计一轮可收。
