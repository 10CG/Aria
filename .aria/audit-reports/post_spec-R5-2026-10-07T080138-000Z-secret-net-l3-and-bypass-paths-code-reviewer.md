---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T08:55:38.053Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审文件 (`6efb9b2`; sha256[:16] proposal `cedbdfce05575891` / probe `cf331b4aa264a863` / evidence `b41e86d796bb583c`, 与返修报告一致):
  - `proposal.md` 全文 1-449; v4 → v5 词级 diff (`git diff --word-diff b07f69a 6efb9b2`)。
  - `baseline-evidence.md` 1-60、末尾计数段, 以及 SC-1 / 9 / 10 / 22 / 25 / 27-34 各行。v4 → v5 证据行逐行对比: 新增 26 行, 改期望 6 行 (1c / 1d / 19aa / 19ae / 19z / 22bj), 删除 0 行。
  - `baseline_probe.py` 1-120、318-600 (L3 帮助函数与 SC-1..SC-4)、805-810 (9z)、1283-1300 (18j / 18k)、1484-1530 (19af / 19ag)、1696-1712 (包裹表)、1741-1776 (22bo / 22br / 22bs / 22at)、2232 (28o)、2400-2480 (SC-34); 全文检索 `printenv`。
- issue 与决策单: `aria-plugin-154.md` (含评论 19339)、`aria-plugin-203.md`、`Aria-221.md` (含评论 25898) 全文; 决策单全文; CLAUDE.md 规则 #6 / #7 / #10 与多远程两条硬约束。
- 源码与规范 (aria `268da8f` / standards `2bc1c4c`):
  - `secret-scan.sh` 全文; `secret-guard.sh` 1-1120 (头注释、`_sg_safe_to_split` / `_sg_split_top`、`_sg_compute_credit`、Read/Edit 分派、`risky_patterns` 全表、`_sg_judge_one` / `_sg_per_segment_eval`); `hooks.json` 全文。
  - `secret-guard.test.sh` :11 / :841 / :1602-1622 / :2018-2033; `secret-hygiene.md` 节标题与 :3 / :23 / :96 / :277-296 / :287 / :288 / :319 / :402; `skill-benchmark-exemption.md` §4 / §4.1 / §5 / §6。
  - `COMMIT_FOOTER_GUIDE.md:195-203`; `git-commit.md` §6.1; 10CG/Aria#199 `detailed-tasks.yaml:336-350`; `.aria/probes/plugin-cache-currency.py` 的判定与全部输出串; `openspec-archive/SKILL.md` Step 7 (:282-300); `state-scanner/scripts/lib/spec_complete.py` 里 unverified_claims 的来源 (检索)。
- 研究笔记: `cc-hooks.md` 1-60; `secret-guard.md` 中包裹 / 容器 env 规则段 (检索)。
- 上一轮: R4 聚合报告全文 (全部 finding 表与主控记录); 本席 R4 报告。
- 返修材料: `v5-writer-report.md` 全文; `writer-v5-proto/` 的 README、`build_full.sh` / `runprobe.sh` / `onemut.sh`、`patch_l1.py` (W9 原型 440-620 行、包裹与 tight 构造 225-300 行、主流程 820-960 行)、`patch_l3.py` 变体表、`timing.py` 判据、`mut_summary_v5.txt` 的等价变异节与回归节; 实验目录 `out/numbers.json`。

**独立复算 (成立的部分, 不计 finding)**

1. **基线证据逐字节复现**: 私有副本 (aria `268da8f` + standards `2bc1c4c`), 带真 bash 3.2.57, 非 root。rc=0, stderr 0 字节, stdout 97972 字节, sha256[:16] `526efaa2b5a9d52e`, 与 `baseline-evidence.md` 内嵌块逐字节相同 (主机负载 10-27, 用时 33 分 11 秒)。
2. **计数**: 证据共 437 行。本席按 SC 与类别重计, SC-1 / 9 / 10 / 11 / 12 / 13 / 18-28 / 32 / 34 的类别数与 proposal 各条的 `×N` 全部相符; 基线类别为 0/213、0/26、79/79、70/70、39/39、9/9, 基线形态 holds。
3. **目标态原型** (实验目录 `work/t5f` 复制到本席目录): `WPA_ONLY` 依次取 SC-1 / 2 / 18 / 19 / 20 / 22 / 25 / 34 与 SC-9 / 10 / 15 / 23 / 28, 共 226 行全 `yes`, rc=0, stderr 空。
4. **file:line 抽核成立**:
   - secret-scan.sh: :112-122 (1 MB 上限作用于原始信封, 不作用于提取后的扫描缓冲) / :135-144 / :152-231 (31 条) / :355-361 / :367。
   - secret-guard.sh: :8 / :21-23 / :62 / :405-408 / :427 / :564 / :617-620 / :641 (32 个备选) / :698-700 / :736-1009 (145 行) / :858 / :862-863 / :867 / :873 / :893-894 / :930-933 / :938 / :940 / :974 / :1043-1071 / :1111。
   - 其它: `COMMIT_FOOTER_GUIDE.md` :199-200 (`Closes` 必需) 与 :201-202 (`Refs`); `detailed-tasks.yaml:342` = `guard_config_hooks`; `plugin-cache-currency.py` 的输出 `OK …` / `##SKIP##` / `MALFORMED` / `STALE` / `AHEAD` 与 Tasks 1.12 的描述一致。

## Findings

### Major

**M1** `ac42f607` · major · issue · implementation · `proposal.md What.W11`

**Summary**: W11 与 SC-22 断言「基线对 `docker|kubectl|podman|lxc exec … env` 已拦」, 并据此把这四个包裹的转储备选判为等价变异。这与源码不符。
- 22bo 对这四个包裹只用基线已拦的写法, 因此删掉它们的坏实现能过全部 74 行 SC-22, 却放行目标原型会拦的整环境转储。
- 「只拦裸 `printenv`」的边界 (带变量名的 `printenv NAME`) 与原型行为相反, 也没有行钉住。
- Impact 没有申报这两类新拦截。
- 本条是新问题, 不是簇 F 的残余: F 的 credit 制度已关闭, 见对账。键 `ac42f607` 与 R3 的簇 K 同键, 但内容无关。

**证据**:

- Spec 原文:
  - `proposal.md:196`:「基线对 `docker|kubectl|podman|lxc exec … env` 已拦, 而 `nomad alloc exec`、`pct exec`、不加引号的 `ssh`、`sh|bash -c`、`watch` 漏」;同行又写「只拦裸 `env` / `printenv`, `env FOO=1 cmd` 这种 `env` 作 launcher 的形态放行 (22at)」。
  - `:291` SC-22「怎么会红」:「`docker` / `kubectl` / `podman` / `lxc` 四个因基线另有独立规则而删除不可观察 —— … —— 是等价变异」。
  - `:344` Impact 新拦截只列 `nomad alloc exec` / `pct exec` / `ssh` / `sh -c` / `bash -c` / `watch` 包裹下的「裸」`env` / `printenv`。
- 源码事实 (`268da8f`): 这四条既有规则都只覆盖很窄的写法。
  - `secret-guard.sh:858` (docker): `env` 前必须是空白, 后面只能接空白、行尾或分隔符; 引号形不在内。
  - `:862-863` (kubectl): 要么带 `--`, 要么 `env` 之后是行尾或 `|`; `$(…)` 与重定向形不在内。
  - `:938` (podman): `env` 必须紧跟在空白之后; 引号形不在内。
  - `:940` (lxc): 必须带 `--`。
- 探针:
  - `baseline_probe.py:1700-1702` 的 `WRAP_T` 对这几个包裹用的是 `docker exec c CMD`、`docker compose exec web CMD`、`podman exec c CMD`、`kubectl exec pod -- CMD`、`lxc exec c -- CMD`, 全是基线已拦的写法。
  - 证据 22bo 的基线实得是 `10/22 as expected`, 即这 10 个成员在基线上就已拦, 在本行里恒绿。
  - `grep -n printenv baseline_probe.py`: 没有任何「包裹 + `printenv <变量名>`」的行; 22at 只有 `… ls` 与 `… env FOO=1 true`。
- 本席实跑 (hook 直调, `LANG=LC_ALL=C.UTF-8`, 命令只作 stdin 文本):
  - `mut_X` = 执笔自己的 `patch_l1.py --variant remote_env_split:X`, 即只从新的转储备选里删掉包裹 X。
  - 下面是原样输出。

```
base=0 tgt=2 mut_lxc=0     :: lxc exec c env
base=0 tgt=2 mut_lxc=0     :: lxc exec c 'printenv'
base=0 tgt=2 mut_kubectl=0 :: x=$(kubectl exec pod env)
base=0 tgt=2 mut_kubectl=0 :: kubectl exec pod 'env'
base=0 tgt=2 mut_kubectl=0 :: kubectl exec pod env > /tmp/x
base=0 tgt=2 mut_docker=0  :: docker exec c "env"
base=0 tgt=2 mut_docker=0  :: docker exec c 'printenv'
base=0 tgt=2 mut_podman=0  :: podman exec c "env"
base=0 tgt=2 mut_podman=0  :: podman exec c 'printenv'
```

- 把 `mut_lxc` / `mut_kubectl` / `mut_docker` 各换进目标原型树 (只换 `secret-guard.sh`), 跑 `WPA_ONLY=SC-22,SC-25`: 三个都是 rc=0、`SC-22: 74/74`、`SC-25: 8/8`, 没有一行转红。
- `mut_summary_v5.txt:13-16` 把这四个变体记为「The mutated program behaves exactly like the correct one: the baseline already has its own, older rules that block `<this wrapper> ... env` … changes the verdict of no input」。上表推翻了这一论断。
- 带变量名的 `printenv` (base / tgt; 目标原型的 printenv 备选是「`printenv` 后接任一空白」, 对应基线裸 printenv 行 `:867` 的写法):

```
base=0 tgt=2 :: docker exec c printenv HOME
base=0 tgt=2 :: nomad alloc exec abc printenv HOME
base=0 tgt=2 :: ssh host printenv PATH
base=0 tgt=2 :: sh -c 'printenv HOME'
base=0 tgt=2 :: watch printenv HOME
base=0 tgt=0 :: nomad alloc exec abc env FOO=1 ls
```

**失败场景**:
1. 实现者读到 `:196`「基线对 docker|kubectl|podman|lxc exec … env 已拦」, 又照主控方针「优先复用已有机制」, 只给 6 个漏掉的包裹补转储备选。
2. 探针全 `yes`, Tasks 1.10 验收通过。Tasks 1.8 的非作者 review 以 `writer-v5-proto` 的汇总为对照, 而汇总把这四个变体标成等价, 所以同样漏过。
3. 上线后 `lxc exec c env`、`kubectl exec pod 'env'`、`x=$(kubectl exec pod env)`、`docker exec c "env"`、`podman exec c "env"` 仍放行。这些输出都是整份容器环境, 与 W11 要堵的是同一类。
4. 反方向: 实现者照抄原型的 printenv 备选, 则 `ssh host printenv PATH`、`docker exec c printenv HOME` 由放变拦。这与 `:196`「只拦裸」和 Impact 相反, 且未申报。照字面不拦也同样过验收。两种实现都全绿, 结果取决于偶然。
5. 两侧都不比基线差 (不是安全回退), 但 Spec 自称的 22 个成员覆盖与行为申报都没有被验收证实。

**怎么会红 (按下面修法新增的成员)**:
- 「四个包裹的非基线写法」成员, 如 `lxc exec c env`、`kubectl exec pod 'env'`、`docker exec c "env"`、`podman exec c "env"`:
  - 基线 exit 0, 行为 `no`。
  - 目标原型 exit 2, 行为 `yes`。
  - `remote_env_split:X` exit 0, 转红。
- 「包裹 + `printenv NAME`」行: 期望按裁定取 0 或 2。另一种实现在该行转红。

**修法**:
1. `:196`: 把「基线已拦」改成准确的覆盖面 (引 `:858` / `:862-863` / `:938` / `:940`), 写明新的转储备选覆盖全部 11 个包裹, 含这四个。
2. `:291`: 删去「是等价变异」一句。22bo (或新增一行) 为每个基线包裹至少放一个基线不拦的写法; 原有的基线写法改作 reverse-guard。
3. 裁定「包裹下 `printenv NAME`」拦还是放:
   - 两条理由在 W11 内互相冲突。按「只拦裸」与 W12 的单键读取逻辑应放; 按「外壳里的转储与直接执行同一」以及基线 `:867` 应拦。
   - 裁定后用一行钉住, 并同步 `:196` 与 Impact。
4. Impact 新拦截补申报这四个包裹新增被拦的写法: 引号形、`$(…)` 形、`… env > 文件`、不带 `--` 的 lxc。
5. 订正 `mut_summary_v5.txt` / `equiv_reasons.py` 里这四个等价论证。

### Minor

**m1** `5d12116d` · minor · issue · documentation · `proposal.md Tasks`

**Summary**: Tasks 1.7 写「`_sg_ext_pass` / `_sg_ext_path_pass` 经内建的同一个 `_sg_core_eval` 判定」, 与 W9 对 Read/Edit 面的定义 (对小写化路径做字面子串比对) 相矛盾。这是 v5 引入的接缝。

**证据**:
- `proposal.md:376` (Tasks 1.7) 原文如上。v4 的同一行 (`b07f69a` :373) 只写「W9 扩展入口 (`_sg_ext_pass` / `_sg_ext_path_pass`, 全部扩展代码只经 `$( )` 调用)」。
- `:165`:「Read/Edit 面: `file_path` (小写化后) 含该子串 → 拦」。
- 返修报告 §2(a):「Read / Edit 面的扩展入口 `_sg_ext_path_pass` 是对小写化路径的字面子串比对」。
- 原型 `patch_l1.py:489-499` 同样只做一次 `grep -qFi`。

**失败场景**: 实现者照 Tasks 1.7, 把 Read/Edit 路径拼成一条 Bash 命令交给 `_sg_core_eval`。这样 Read/Edit 面的判定就受 `[^|]*` 与引号结构影响, 例如路径里含 `|` 时漏拦。SC-19 的 Read 行 (19p / 19s / 19t / 19am) 都不含这类路径, 抓不到这种实现。

**修法**: Tasks 1.7 改为「`_sg_ext_pass` 把替换副本交 `_sg_core_eval`; `_sg_ext_path_pass` 对小写化路径做字面子串比对 (W9)」。

**m2** `ed638210` · minor · issue · testing · `proposal.md SC-9`

**Summary**: 9z 把「凭据形的值挂在紧贴词字符的大写键上 → 静默」钉成 `allow-guard` (误报守卫)。实质上这是 kv 左边界带来的漏报类。
- W2 的已知限制只列了 cli 的同类情形 (旗标紧贴字母数字, 10o 为 `known-limit`), 没列 kv 的。
- 两类同一机制, 类别却相反。

**证据**:
- `baseline_probe.py:805-806`: 9z 的两个用例是 `x` + `JWT_SECRET=<24 alnum>` 与 `abc_API_TOKEN=<24 alnum>`, 值是凭据形, 类别 `allow-guard`。
- `proposal.md:80` 的已知限制只写「旗标紧贴在字母数字之后 (`abc--token=<值>`…)」; `:448` (待复议 31) 同样只提旗标。
- 本席实跑 (Read 真实信封, 值在进程内生成):

```
lower-prefix glued key, no spaces              | base: silent | tgt: silent
export + lower-prefix glued key, spaced, quoted | base: silent | tgt: silent
control: same key upper-case, spaced           | base: silent | tgt: kv-secret-assign=1
```

**失败场景**:
- 采用方的 `prod_API_TOKEN=…` / `export my_DB_PASSWORD = '…'` 一类赋值不告警, 已知限制里也查不到。
- 日后有人放宽左边界去覆盖这类键 (例如把 `_` 也算作边界; 上界仍在, 依旧线性), 9z 会按 allow-guard 的语义被读成「引入了误报」, 改进反而被回退。

**修法**:
- 9z 改为 `known-limit`, 已知限制写入「小写前缀 + `_` 紧贴的大写键」。
- 或者论证并钉住「为什么不把 `_` 算作左边界」, 并把该备选列进待复议 31。

**m3** `eb6c5b5e` · minor · issue · testing · `proposal.md SC-25`

**Summary**: 扩展拦截时 BLOCKED 文案里的 `Matched pattern:` / `Triggering segment:` 该写什么, W9 没有规定。SC-25 25f 的归一化把这两行抹掉, 因此「让内建判定直接输出它对替换副本的文案」的实现照样全绿。这时 AI 收到的触发段是 `/etc/gitea/app.ini`, 一个它从未用过的路径。

**证据**:
- `proposal.md:165` 只写「拒绝时复用同一份 BLOCKED 文案 (SC-25 25f), 不为扩展另写文案」。
- 同类的 W12 由 25h 钉住「回显原命令」(`:294`); W10 明文「不作规定」(`:188`), 但 W10 的副本里是真实路径, W9 的副本里是替身路径。
- 原型输出 `Matched pattern: (extension) .aria/secret-guard.paths` 与 `Triggering segment: echo hi; cat /srv/billing/conf/prod.toml`。
- 本席变体只改三处: `_sg_ext_pass` 不丢内建判定的 stderr; 两个调用点不加 `2>/dev/null`; 去掉合成的 `_sg_emit_blocked`。该变体对 `echo hi; cat /srv/billing/conf/prod.toml` 输出 `Triggering segment:  cat /etc/gitea/app.ini`, `Matched pattern:` 为 app.ini 行的正则。它在 `WPA_ONLY=SC-19,SC-20,SC-25` 下得到 `37/37`、`17/17`、`8/8`。

**失败场景**: 被拦的 AI 看到一个它没碰过的路径和一条 app.ini 规则, 容易判断为 hook 误报, 转向 `# guard:ack`。这正是 10CG/Aria#221 评论 25898 所说的疲劳诱因。

**修法**:
- W9 写明扩展拦截时 `Matched pattern:` 点名扩展文件, `Triggering segment:` / `Command was:` 回显原命令文本。
- SC-25 加一行 25h 同款断言: 扩展拦截的 stderr 不含替身名 `/etc/gitea/app.ini`, 且含原路径。

## 上一轮对账

| 簇 (键) | R4 问题 | 本轮 | 本席核验 |
|---|---|---|---|
| U `1038b8da` (ba/C1) | NUL → 换行替换了基线视图, UTF-16LE 文本的检出变静默 | **closed** | 原型保留基线视图 D, 仅当信封含 `\u0000` 且 N≠D 时追加视图 N。本席直调: UTF-16 形 AWS 行 / JSON 行经 Bash, base 与 tgt 都检出, `nul_replace` 变体静默; NUL 分隔环境经 Read, base 静默, tgt 为 `env-line-secret-keyword=2 kv-secret-assign=1`, `nul_off` 只有 `kv=1`。目标 SC-1 7/7、SC-2 6/6。1e 在基线上是 `yes` (反向守卫成立)。 |
| T `0a8380fd` (ba/M2 · qa/M1 · cr/M1 · km/M1) | 扩展的阶段 / 引号 / 偏移切片与内建不一致 | **closed** | W9 改为替换成 `/etc/gitea/app.ini ` 后交给内建的同一个 `_sg_core_eval`, 不再有第二份状态机; 偏移与切片统一用字节 (`local -x LC_ALL=C`)。目标 SC-19 37/37、SC-20 17/17。本席另造 34 个形态 (含 `time` / `nohup … &` / `env FOO=1` / 子 shell / CJK 前缀 / 注释 / 制表符等) 比对内建名与条目: 1 处不同 (`cat <条目>x`), 是 19aj 钉住的「条目为字面子串」, 属设计差异。 |
| V `22bdd143` (tl/M2) | W14 没有覆盖扩展命中路径, 逐出现点计算是平方级 | **closed** | 设计变为一次 grep + 至多 64 次按字节拼接 + 再判一遍内建, 是线性的。新增 W14 (f-hit) 档 (上界 3.0, 实测 2.01 / 2.01) 与探针 34c。目标 34c 在本席负载 15-27 的主机上为 `yes`。 |
| W `755aab21` (ba/M1) | `cli-secret-flag` (及去掉左边界的 kv) 自然写法是平方级 | **closed** | 原型 kv / cli 改为有界前后缀加左边界, 取值只用 `%%` / `${s:N}` / `=~`。34a / 34b 在目标为 `yes`。本席把每进程 CPU 上限从 4 s 降到 1 s 再跑 `cli-dash-run` / `kv-upper-run` / 34a 长键形, 目标仍检出, 余量 ≥ 4 倍。 |
| F `e2459206` (tl/M1 · cr/M2 `8fbbee80`) | 包裹下 env / printenv 转储的 credit 制度未定, 原型未申报地改拦基线放行的核对形 | **closed** (credit 制度) | `:196` 明文「credit 沿用默认, 不属 tight 族」, 22br 钉放行 44 个、22bs 钉限制 22 个, Impact 已申报。本席直调 (base / tgt): `nomad alloc exec abc env \| grep '^PATH='` 0/0、`… env \| grep -v X` 0/0、`… env` 0/2、`… ps aux \| grep -v x` 0/2、`docker exec c env \| cut -d= -f1` 0/0。同一规则族的覆盖面与边界另有新缺陷, 见 **M1**: 本席 R4 曾说等价论证「对裸转储成立」, 实测并不成立。 |
| M `eb350937` (qa/M2) | 原位改写的 `:641` 有 16 个基线备选无行钉住 | **closed** | `:641` 实为 32 个备选。本席逐一比对 18j 的 32 条路径, 每条恰好命中一个备选 (32/32 覆盖, 0 条多中或不中)。W14 通则已列 `:641`。目标 SC-18 11/11。 |

R4 的 minor 全部处置, 本席未见遗留: 6ff1d962 / 984b1c3d / 6f503728 / 65fb3fcf / 684e9a24 (BOM 与旧时档数两条) / aa08f71d / a8f5db8c / 13e1f258 / 7b20c975 / 60eea71e / cfd9ca0b / 91a89f9b (Spec 侧; 清理属 owner, 见 7.20) / 8936aa07。

一处微小残差 (不计): (f0) Read 档同一份原始数据 (0.045 → 0.052 s), Impact 写「+16%」(按取整后的两位小数算), W14 写比值 1.14 (按未取整值算), 不影响任何判据。

## 对执笔人自报薄弱点与请裁项的表态

**自报薄弱点**

1. 34c 是唯一带比值的行 —— **可接受**。它比的是 CPU 时间, 交错取 3 次最小值; 设计约 2 倍, 上界 3.5, 坏实现 7.6-64.8 倍。本席在负载 15-27 下实跑为 `yes`。
2. 19af 只对有限形态零分歧 —— **可接受**。含元字符的条目已列进 W9 已知限制; 本席另 34 形态仅 1 处设计内差异。
3. 上界 64 / 40 无数据支撑 —— **可接受**, 已列待复议 31。但同一左边界造成的 kv 漏报被钉成 allow-guard, 见 m2。
4. NUL 前提未端到端验证 —— **可接受**。前提不成立时 N 视图空转, 行为等同基线。
5. 耗时回升与 (i3) 上界 2.5 —— **可接受**。(i3) 的坏实现另有 34b 功能行兜底 (cli_unbounded 在 (i3-b) 为 3.4 倍, 余量不大, 但 34b 会转红)。(f) 靠 100 ms 地板通过, 与判据原文 (`1.5 × max(基线, 100 ms)`) 一致。
6. 靠重跑旧坏实现做回归、29 个 `drop_extreader_*` 被取代 —— **可接受**。扩展改用内建读取器表后, `drop_reader:*` 同时使 16q 与 19u 转红, 替代充分。但 `remote_env_split:{docker,kubectl,podman,lxc}` 的「等价」论证 **不可接受**, 见 M1。
7. proposal 增至 214 KB —— **可接受** (记为审阅成本风险)。
8. 研究笔记与已推送分支 —— **可接受**。Spec 侧已处置, 其余属 owner (7.20)。
9. 时档是单主机测量 —— **可接受**。判据是比值与活性, 不是绝对值。

**请裁项**

1. 7.20 披露范围 —— **可接受**作为产品级上呈。实测: 远端 origin 的分支已在 `6efb9b2`, GitHub 仍停在 `b07f69a` (v4, 含 v4 的 7.1 / 7.2 原文)。
2. W9 条目规则 (纯非 ASCII 有效、剥 BOM) —— **可接受**。
3. 簇 F 取默认 credit —— **可接受**。与基线 docker / kubectl 行一致、两向有行。但该规则的成员覆盖与 `printenv NAME` 边界须按 M1 补。
4. 上界 64 / 40 —— **可接受**, 但请把 m2 的 kv 漏报类一并列进待复议 31。
5. (i3) 上界与参数、`timing.py --judge` —— **可接受**。
6. SC-34 用每进程 CPU 上限与 CPU 总量比 —— **可接受**。本席降到 1 s 上限仍通过, 不会在慢主机上恒红。
7. 采纳的两条席位备注 (Layer 2 一句、MINGW64 / macOS 未验证) —— **可接受**。
8. 未采纳三项 (post-ship NUL 腿、时档进探针、gawk 腿) —— **可接受**。不依赖 awk 后 gawk 腿已无必要。
9. Rule #10 自作主张清单 —— **可接受**作为留痕。其中「旧变体按设计已不存在移出回归」成立。

## 风险 / 疑问

1. **派单背景与远端事实不符**: 派单写 `6efb9b2`「未推送」, 但 `git ls-remote` 显示 origin 上的 `docs/secret-net-l3-and-bypass-paths-phase-a` 已是 `6efb9b2`, github 是 `b07f69a`。这与主控「只推 origin、暂停推 GitHub」一致。两端分叉是有意为之, 已列 owner 复议。
2. **Tasks 1.13 的归档守卫可能不够**: `openspec-archive` Step 7 的触发源有三类。
   - `tasks.md` 未勾选项; Level 2 无 `tasks.md` 时改看 `detailed-tasks.yaml` 的非 done 项。
   - 全部 unverified_claims, 「无论 ack 与否」, 其中含无可链接产物的 dogfood / benchmark 声称 (`spec_complete.py:1126-1185`)。
   - Spec 只写「1.12 / 1.13 勾选之后归档」。若 gate 把 rule6_note 的 dogfood 声称判为 unverified, headless 归档仍会自动开 issue, 而开 issue 不在一次性授权内。本席未对本 Spec 实跑该 gate。
3. **macOS / BusyBox 的 `grep -o -b`**: W9 的 Bash 面依赖它给出逐匹配的字节偏移。BSD grep 的语义与 BusyBox 是否支持 `-b` 本席未验证; 不支持时扩展静默失效 (按设计 fail-open)。Spec 只申报了 Linux 验证范围。
4. **长命令超时**: 基线 secret-guard 本身对命令长度是超线性的。本席在负载约 20 时实测 8 KB 命令, 基线与目标都约 3.8 s CPU。所以「内建放行之后」的 W10 第二遍与扩展判定在长命令上可能越过 5 s 超时。损失的只是它们追加的拦截, 内建拦截不受影响; 与 7.1 同源。
5. **一个旁证**: 本轮本席会话的现行 L1 (v1.74.1) 两次拦下本席的测试脚本, 原因是 heredoc 文本里出现 `kubectl exec pod env` 与 `python3 -c … .environ.get(` 的字面。这佐证了 W12 与 22bj 所述的误拦类和 ack 疲劳风险。
6. W1 写「4 KB 约 0.391 s、60 KB 约 0.322 s」, 大小倒挂。本席在负载约 17 时实测 0.485 / 0.505 s (基线 0.194 / 0.211 s), 倒挂只是噪声, 量级成立。

## Verdict

**PASS_WITH_WARNINGS** —— counts `0C/1M/3m`。

**Vote: REVISE**

## 是否足以进入 A.2

**足以 (附前置条件)**:
- v5 关闭了 R4 的全部六簇 (U / T / V / W / F / M), 本席逐一复核成立, 基线证据也逐字节复现。
- 剩下的 M1 是一处局部的验收缺口与一句错误的基线前提, 不构成安全回退。修法是机械的: 改正 `:196` 与 `:291` 两句; 22bo 为四个基线包裹换上基线不拦的写法; 裁定并钉住 `printenv NAME` 的边界; Impact 补申报。
- 建议在进入 A.2 前以定向修补关闭 M1, 并由非作者复核这一处, 不必为此再开一整轮。三条 minor 可在 A.2 拆任务时一并处理。
