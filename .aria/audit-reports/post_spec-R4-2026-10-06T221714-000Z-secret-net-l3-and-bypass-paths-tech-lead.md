---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-06T23:37:30.981Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审对象 (`b07f69a`):
  - `proposal.md` 全文 (1-443); v3 → v4 的逐词差异 (`git diff --stat c0a6654 b07f69a` + 本席 difflib 逐词对照, 覆盖全部改动行)。
  - `baseline_probe.py`: 549-550 (2e / 2f), 699 (7k), 750 / 772 / 791-792 (9p / 10a / 10k / 10l), 1059 / 1071 (12n / 12o), 1395 (19ac), 1525-1640 (SC-22 全部定义: `WRAP_T` / `WRAP_T_ENV` / `WRAP_PS` / `TIGHT_MEMBERS`、22bc-22au); 另对 28 个新增行逐个核对在场 (1c 1d 2e 2f 7k 7l 7m 7n 12n 12o 16r 19z 19aa 19ab 19ac 19ad 19ae 20o 20p 20q 21z 22bm 22bn 22bo 22bp 22bq 23i 32d, 各 1 处定义)。
  - `baseline-evidence.md`: 1-60, 58 (1c), 125 (7n), 275 (19z), 288 (20o), 321-323, 375-377, 465 (32d), 505-512 (形态行)。
- 三个 issue 全文与全部评论 (10CG/aria-plugin#154 含评论 19339; 10CG/aria-plugin#203; 10CG/Aria#221 含评论 25898)。
- 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; `CLAUDE.md` 规则 #6 / #7 / #10 与多远程推送两条硬约束。
- 源码 @ aria `268da8f`: `hooks/secret-scan.sh` 全文 (1-377); `hooks/secret-guard.sh` 全文 (1-1120); `hooks/hooks.json` 全文; `hooks/tests/secret-scan.test.sh` 1-40。
- 规范 @ standards `2bc1c4c`: `secret-hygiene.md` 1-30、节目录、`:45` / `:96` / `:118-119`; `skill-benchmark-exemption.md` 全文。
- 研究笔记: `cc-hooks.md` 全文; `secret-scan.md` / `secret-guard.md` 定向检索 (`FORGEJO__` / `GITEA__`, 0 处)。
- R3: 聚合报告全文 (全部 finding 表、收敛计算、主控记录); 本席 R3 报告全文。R1 / R2 聚合报告中 `e2459206` / `6bd285b1` / `ac42f607` 所在行。
- 返修报告 `v4-writer-report.md` 全文。
- 归档 `writer-v4-proto/`: `README.md`、`build_full.sh`、`runprobe.sh`、`patch_l1.py` 100-300 / 380-540 / 700-790、`patch_l3.py` 425-440、`timing.py` 全文、`mask_cost.py` 全文、`timing_summary.txt` 58-65、`cases_benign_v4.py`、`hooktry.py`。
- 接缝: 10CG/Aria#199 的 `detailed-tasks.yaml:330-345` (`guard_config_hooks` 在 `:342`) 与其 proposal 头部; `.aria/probes/plugin-cache-currency.py` 输出标记。
- 实跑 (全部在 `scratchpad/audit/post_spec-R4-tech-lead/` 下; HOME / TMPDIR 指向该目录; 命令只作 stdin 文本喂 hook、从不执行; 像凭据的值在进程内由 `secrets` 生成、不打印):
  - 用归档补丁脚本在本席目录重建目标态原型 `t4`: 两个 hook 指纹 `d94ddf4d6906734f` / `cf2dd857823baf79`, 与执笔报告第 5 节逐一相同。
  - 对照脚本: `l1cmp.py` (用例 `cases_envwrap.tsv` / `cases_envtight.tsv` / `cases_envtight2.tsv` / `cases_k.tsv` / `cases_ext.tsv` / `cases_tight.tsv` / `cases_proc_status.tsv`)、`l3cmp.py`、`l3nul.py`、`l3locale.py` (真 bash 3.2.57)、`l3scope2.py`、`evalcheck.py`、`refs3.sh`、`maskhit.py` / `maskhit2.py` / `maskhit3.py`、`stagebench.sh`。
  - 非作者复构的坏实现 (用归档补丁脚本的变体开关): `vx_eval`、`ext_emptypat`、`ent_range`、`step_on:path:bearer-token`、`pd_on_old`。
  - 收尾: 真仓 `git status` 干净, HEAD `b07f69a`, aria `268da8f`, standards `2bc1c4c` 均未变; 未做任何 git 写操作。

## Findings

### M1 [e2459206] major · issue · architecture · proposal.md What.W11

**summary**: W11 没有规定「包裹下的 env / printenv 整环境转储」(22bo 的 22 个成员) 适用哪种 credit 制度。原型把 ps 备选与 env 备选写进同一个包裹正则, 而 tight 拷贝与规则行同源, 结果这类转储被整体并入 tight:
- 基线经锚定 grep / `cut` / `sed` / `grep -v` 放行的既有形态 (`docker|kubectl|podman exec … env | grep '^X='`、`… env | cut -d= -f1`) 由放行变拦;
- Impact 未申报, 也没有任何 SC 行钉住任一方向;
- 同一族的 `cat /proc/<pid>/environ | grep '^X='` 与裸 `env | cut -d= -f1` 却被明文保留放行。

**证据**:
- proposal 原文:
  - `:196` tight 段的「逐成员」清单 (10 类 ps 参数 … 11 个包裹 … 13 个非 ps 写法) 全是 ps 族;
  - `:196` 同段「**`/proc` 行不属 tight 族** (基线语义不变 …)」;
  - `:201`「tight 族 (claude-config / `app.ini` / 进程表 / 扩展条目)」;
  - `:194` 包裹 × {env, printenv}「一并拦」;
  - `:341` Impact 新拦截只列 nomad / pct / ssh / sh -c / bash -c / watch 包裹下的**裸** env / printenv。
- 原型 `writer-v4-proto/patch_l1.py` 的 `compose()`:
  - `remote_re = "(" + "|".join(remote_.values()) + ")[^|]*" + sep + "(" + ps_cmd + "|" + env_part + ")"`;
  - tight 判据 `_SG_PROCTAB_ALL="(${_SG_PROCTAB}|${_SG_PS_REMOTE}|${_SG_PS_DOCKER})"` 由 `_sg_compute_credit` 消费。env 备选因此随包裹正则进入 tight。
- 探针:
  - `TIGHT_MEMBERS` (`baseline_probe.py:1585-1586`) 只含 ps 族;
  - 22bo (`:1592`) 只钉无过滤成员;
  - 本席用正则 `(env|printenv)\b[^"']*\| *(grep|cut|sed|awk)` 扫全文件: 0 行。
- 实跑 (列依次为 基线 | 目标原型 `t4`):
```
exit=0 | exit=0 | B | "env | grep '^PATH='"
exit=0 | exit=2 | B | "docker exec web env | grep '^PATH='"
exit=0 | exit=2 | B | "docker compose exec web env | grep '^NODE_ENV='"
exit=0 | exit=2 | B | "kubectl exec pod -- env | grep '^HOSTNAME='"
exit=0 | exit=2 | B | "podman exec web env | grep '^PATH='"
exit=0 | exit=2 | B | "ssh host 'env' | grep '^PATH='"
exit=0 | exit=2 | B | 'docker exec web env | cut -d= -f1'
exit=0 | exit=2 | B | "docker exec web env | sed 's/=.*//'"
exit=0 | exit=2 | B | 'kubectl exec pod -- env | cut -d= -f1'
exit=0 | exit=2 | B | 'nomad alloc exec -task server abc123 env | cut -d= -f1'
exit=0 | exit=0 | B | 'env | cut -d= -f1'
exit=0 | exit=0 | B | "cat /proc/123/environ | tr '\\0' '\n' | cut -d= -f1"
exit=0 | exit=0 | B | "cat /proc/123/environ | grep '^PATH='"
exit=0 | exit=0 | B | 'docker exec web env | wc -l'
```

**失败场景**:
1. 实现者照「规则行与 tight 判定是同一份定义的两份拷贝」写, 得到与原型相同的行为, 411 行全绿。
2. ship 后, AI 在容器里做 10CG/Aria#221 评论 25898 明确称为「正当核对」的「读 env 变量名」(`kubectl exec pod -- env | cut -d= -f1`), 或用冻结的 BLOCKED 文案自己列为可接受的 `| grep '^SAFE_PREFIX='` 过滤 —— 被拦。
3. 照文案重试仍被拦, 于是转向 `# guard:ack` (评论 25898 警告的形态)。
4. CHANGELOG (26g) 与 Impact 都没有这条, owner 不知情。
5. 反过来, 照 `:201` 的 tight 族清单字面实现的人 (env 备选不进 tight) 同样全绿。两个实现者得到相反结果, 验收不可证伪。

**三态** (以建议新增的允许侧行为例: `docker exec web env | grep '^PATH='`、`kubectl exec pod -- env | cut -d= -f1` → exit 0):
- 基线: yes;
- 原型: no;
- 按 tight 族清单字面实现: yes。

现状没有此行 ⇒ 两种实现都是 yes。

**建议修法** (技术级, 二选一并写入「待复议」; 都是一句话加一行, 不新增机制):
- (A) 推荐: tight 拷贝只含 ps 族备选; 包裹 × env / printenv 只在规则行, 沿用默认 credit, 与基线 docker / kubectl / podman 行、裸 env 和 `/proc` environ 一致。补一条 allow-guard 行 (上面的过滤形 → 0); 22bo 不变。
- (B) 刻意 tight (安全收益: `… env | grep '^DB_PASSWORD='` 不再靠锚定 grep 放行): 把这一族加进 `:201` / W13 / SOT §2.5 注 / hook 头注释的 tight 族清单; Impact 新拦截申报 (含包裹下 `cut -d= -f1` 列名被拦); 补一条 baseline-failing 行; 并写明它与裸 env、`/proc` environ 判定不一致的理由。

本条与 R1 F 簇 (`e2459206`, 包裹下转储「既不补也不申报、SC 两不钉」) 同族: v2-v4 补了拦截, 留下的是它的 credit 归属与申报。

### M2 [22bdd143] major · issue · testing · proposal.md What.W14

**summary**: W14 的时档没有一档走到 W9 的**命中路径** (命令里出现列入的路径时才执行的引号掩码与逐出现点循环):
- (f) 用 `ls -la`;
- (h) 的命令与条目不相交;
- (g) 不带扩展文件。

原型逐出现点计算阶段用 `stage="${before##*[;&|$'\n']}"`, 在无分隔符的前缀上是 O(前缀长²), 再乘以至多 64 个出现点, 另加每个出现点一次 `printf | tr` 派生。v4 的引号掩码把内联程序里引号内的分隔符抹成空格, 恰好让这类前缀变成无分隔符。

W9 / Impact 对这部分开销的说法与实测不符, SC-30 对它恒绿:
- W9 写「条目数上限 200、文件上限 32 KiB 即是成本上界」「命中时多一遍 … O(命令长度)」;
- Impact 只给掩码自身的开销。

**证据**:
- proposal 原文:
  - `:165`「即是成本上界」;
  - `:164`「命中时多一遍 bash 字符循环 (O(命令长度) …)」;
  - `:346` Impact 性能段只量掩码 (`mask_cost.py`);
  - `:233-237` 档位与上界: (f) / (f0) ≤ 1.5 × max(基线, 100 ms), (h) ≤ 1.5。
- `writer-v4-proto/timing.py`:
  - (f) 用 `bash_payload("ls -la")`;
  - (h) 的条目是 `/srv/filler/entry-%03d.conf`, 命令里是 `/srv/data/…`, 两者不相交。
- `writer-v4-proto/mask_cost.py`: 比较的是「有掩码 / 无掩码」两个都带逐出现点循环的 hook, 填充每约 33 字节就有一个 `;`。
- 原型 `t4` 的 `_sg_ext_pass` 循环体逐出现点执行 `match="$(printf '%s' "$match" | tr …)"`、`before="${lc:0:off}"`、`stage="${before##*[;&|$'\n']}"`。
- 实跑。测量条件: 4 核共享主机, 本席测量期间 1 分钟负载 20-37 (其它席位探针并发); 数值为整进程 CPU (user+sys, 含子进程), 只看比值与增长趋势。
  - 同一条单行命令 `echo <pad> <路径>`, 交错 3 轮取最小, 用来隔离命中开销:
```
~2000 B single line | (a) base 0.45s | (b) target, no extension 0.48s | (c) target, listed path once 0.74s | (d) target, extension but no hit 0.49s | hit cost (c)-(d) +0.25s
~4000 B single line | (a) base 1.21s | (b) target, no extension 1.23s | (c) target, listed path once 2.06s | (d) target, extension but no hit 1.23s | hit cost (c)-(d) +0.83s
```
  - 约 2 KB 单行, 出现点数 k 递增 (单次运行):
```
k= 1 | base cpu 0.47s | target cpu 0.76s
k= 8 | base cpu 0.47s | target cpu 1.61s
k=16 | base cpu 0.46s | target cpu 2.40s
k=32 | base cpu 0.48s | target cpu 3.61s
k=64 | base cpu 0.47s | target cpu 4.87s
```
  - 同形约 8 KB、64 个出现点: 目标 hook 单次运行超过 90 s CPU 仍未结束, 本席中止。
  - 微基准 (`LC_ALL=C`, 与 `_sg_ext_pass` 同): 在无分隔符的前缀上, `${before##*[;&|$'\n']}` 对 1000 / 2000 / 4000 / 8000 字节分别耗时 0.22 / 1.05 / 2.55 / 9.04 s (负载下墙钟); 求同一结果的逆向逐字符扫描是 0.18 / 0.80 / 1.15 / 2.75 s, 两者结果逐字节相同。

**失败场景**:
1. 实现者照散文写出同样自然的 `##*` 写法 (或每个出现点重跑一次掩码)。(f) (f0) (g) (h) (i) 全在界内, SC-30 绿。
2. 生产中, 命令里出现列入路径的形态会让 hook 越过 `hooks.json` 的 5 s 超时, 被 harness 杀掉, 命令照常执行 (fail-open)。这类形态包括:
   - 多 KB 的内联程序 (掩码后无分隔符), 或一条长单行;
   - 同一路径出现多次。
3. 扩展判定排在内建与 W10 之后, 所以丢的是扩展自己的拦截。
4. 19x 钉的「第 64 处仍被检查」只在无超时的探针直调里成立。按本 Spec 自己的比值上界加一档命中档, 参考原型本身就不过: 4 KB 单处 2.06 / 1.21 = 1.70; 2 KB 64 处约 10 倍。

**三态** (建议的命中档, 比值 = 目标 / 基线):
- 原型: 红 (1.70 / 约 10);
- 线性实现 (在掩码那一遍顺带记录未被引号包住的分隔符偏移, 按出现点偏移单调推进; 只小写化一次): 预期在界内 (微基准中逆向扫描近线性);
- 坏实现「每个出现点重跑一次掩码」: 红。

**与 R3 cr/m7 (同属时档覆盖缺口, 定 minor) 的区别**: cr/m7 是假设的放置位置。本条是参考设计实测超线性, 且 Spec 的成本上界声明被实测推翻, 后果是超时放行。故按「验收会放过一个错误实现」定 major。

**建议修法** (不新增机制):
1. W14 增一档 (f-hit):
   - 200 条条目, 用会命中的 Bash 命令: (a) 约 4 KB 单行 (或内联程序) 末尾出现一次; (b) 约 2 KB 内出现 64 次;
   - 上界同 (f);
   - 活性断言: 逐出现点循环确实运行。
2. W9 / Impact 改写成本表述: 上界由「命令长度 + 出现点数」决定, 每个出现点的阶段查找不得是 O(前缀); 写一句实现注意 (分隔符偏移一遍记录、只小写化一次)。

### m1 [6ff1d962] minor · issue · documentation · proposal.md What.W11

**summary**: 22bo 的包裹 × {env, printenv} 备选按原型写法, 只要求 env 前是空白 / 引号 / `(` / 反引号、后接行尾或 `;&|)}<>'"` 与反引号, 不要求 env 处在被包裹命令的命令位置。于是两类文本被拦:
- 「env 作参数词」(venv 名、目录名);
- 「包裹词 + env 词」的文本提及。

这与 W11「只拦裸 env / printenv」(`:194`) 不符。W11 已知限制 (`:201`)、Impact (`:341`) 与 22bj (`baseline_probe.py:1629-1631`, 成员全是 ps 形) 只申报了「包裹词 + 进程表形态」的文本提及。

**证据** (基线 | 目标):
```
exit=0 | exit=2 | B | 'bash -c "python3 -m venv env && env/bin/pip install -r requirements.txt"'
exit=0 | exit=2 | B | 'sh -c "cd /srv/app; python3 -m venv env"'
exit=0 | exit=2 | B | 'ssh deploy@host "cd /srv/app && python3 -m venv env && env/bin/pip install -r requirements.txt"'
exit=0 | exit=2 | B | 'watch -n 5 "du -sh env"'
exit=0 | exit=2 | B | 'bash -c "conda activate env && pytest"'
exit=0 | exit=2 | B | 'git commit -m "refactor ssh helper to read the token from env"'
exit=0 | exit=2 | B | 'echo "configure sshd, then source env"'
exit=0 | exit=0 | B | 'python3 -m venv env'
exit=2 | exit=2 | B | 'ssh host "python3 -m venv env"'
```
- 最后一行是基线 `secret-guard.sh:849` 已拦, 不是新增。
- 22at 的放行侧只有 `env FOO=1 true` 与 `ls` 两形。
- 本席对四仓最近 3000 个提交信息按行检索同形: 0 行。频度低, 故定 minor。

**失败场景**: 实现者照原型写, 部署脚本里常见的 `bash -c "python3 -m venv env && …"`、`sh -c "…; python3 -m venv env"` 被拦, 推向 ack; CHANGELOG 与 Impact 均无此类。

**建议修法** (二选一):
- 把 env 备选限定在被包裹文本的命令位置 (包裹参数边界、开引号、未被引号包住的 `;` `&&` `|` 之后), 并补一条 allow-guard 行;
- 或保留现写法, 在 W11「新增误拦」、Impact 与 22bj 各补 env 成员。

### m2 [984b1c3d] minor · issue · documentation · proposal.md What.W2

**summary**: Forgejo / Gitea 容器部署用 `FORGEJO__<section>__<KEY>` / `GITEA__<section>__<KEY>` 环境变量覆写 app.ini, section 名常为小写 (如 `FORGEJO__security__SECRET_KEY`、`GITEA__oauth2__JWT_SECRET`、`FORGEJO__database__PASSWD`)。这与 10CG/aria-plugin#203 是同一批凭据。该形态在基线与目标两层都不可见:
- L1 只认 `app.ini` 名;
- L3 的 `kv-secret-assign` 要求全大写键、左边界为非词字符 (`:62`), `env-line-secret-keyword` 同样要求全大写。

而 W2 已知限制 (`:79`)、W8 已知限制、SC-10、建议开单 7.8 / 7.9 都没有它。

**证据**:
- 实跑 (基线 | 目标; 值运行时生成):
```
compose env list, Forgejo mixed-case section key via Bash | exit=0 silent | exit=0 silent
compose env list, Forgejo mixed-case section key via Read | exit=0 silent | exit=0 silent
compose env map, Gitea mixed-case section key via Bash | exit=0 silent | exit=0 silent
docker inspect Env array (Forgejo) via Bash | exit=0 silent | exit=0 silent
control: same values, all-uppercase keys via Bash | exit=0 alert {env-line-secret-keyword=2} | exit=0 alert {env-line-secret-keyword=2}
control: same values, all-uppercase keys via Read | exit=0 silent | exit=0 alert {env-line-secret-keyword=2}
```
- proposal 与研究笔记检索 `FORGEJO__` / `GITEA__` / `__security`: 0 处。
- 四仓 `git grep --recurse-submodules` 同形: 0 处 (10CG 自身的 Forgejo 用 app.ini, 故定 minor)。

**失败场景**: owner 读到 W8「输出侧由 W1 + W2 兜底」与 Impact「10CG/aria-plugin#203 部分覆盖」, 以为 Forgejo 凭据在输出侧已兜住。容器部署的 compose 文件或 `docker inspect` 输出照样静默泄露。

**建议修法**: 列入 W2 已知限制 + SC-10 known-limit 行 + 7.8 / 7.9。若 owner 要覆盖, 可让 kv 的键段接受 `__` 作边界, 这是技术级决定。

## 上一轮对账

R3 的 12 条 C+M 归为 10 个定稿键, 逐簇对账如下。

| 簇 | 定稿键 (席位编号) | 状态 | 本席亲自核验的证据 |
|---|---|---|---|
| Q | `4f713847` (tl/M1) | closed | 改动在 W1 `:52-54`。`l3nul.py`: 以 NUL 分隔、含 6 条记录 (其中 3 个凭据键) 的 environ 形, 经 Read 与 Bash 都是「基线 silent → 目标 alert {env-line-secret-keyword=3}」; NUL 分隔的 cmdline 形 (带鉴权头的 curl) 两种信封都是「silent → alert {auth-header-token=1}」。1c / 1d 在场 (`baseline-evidence.md:58`) |
| S | `8d258b19` (ba/M1) | closed | `evalcheck.py` 5 种载荷: 基线与目标 5/5 诱饵不存在; 非作者复构的 `vx_eval` 有 3/5 诱饵被创建。19ab / 21z / 23i / 7n 在场 |
| M | `8fbbee80` (ba/M2) | closed (就 Spec 列入的 ps 族与 app.ini 族而言) | `cases_tight.tsv`: `pgrep -af` / `pstree -a` / `top -c` / `sudo -u svc ps -ef` / `/usr/bin/ps` / `docker top` / `ssh host 'ps aux'` 接 `grep -v` 或锚定 grep, 以及 app.ini 接 `grep '^JWT_SECRET'` / awk, 全部「基线 0 → 目标 2」; 接 `| wc -l` 两侧都是 0。22bm / 22bn / 16r 在场。包裹 env 备选的 tight 归属是新问题, 见 M1 |
| T | `0a8380fd` (ba/M3) | closed | `cases_ext.tsv`: python3 -c / node -e / awk 内联程序里含 `;` 时, 目标对扩展条目 exit 2; `cat x; echo P`、`cat P ";" \| wc -l`、`cat P \| wc -l` 都是 0。19z / 19aa 在场。副作用见 M2 (掩码拉长了无分隔符前缀) |
| K | `ac42f607` (ba/M4) | closed | `cases_k.tsv`: `$$` / `$!` / `thread-self` / `[0-9]*` / `for f in /proc/[0-9]*/cmdline` 都是「0 → 2」; `{1,2}`、`N`、`<pid>`、status 两侧都是 0。22bp / 22bh / 22bf 在场 |
| M | `1c49d896` (ba/M5) | closed | W2「作用面 (闭集)」`:67`。`l3scope2.py`: `bearer-token` 的路径形值在基线与目标都检出; 非作者复构的 `step_on:path:bearer-token` 静默 (7l 对应成员会转红)。7k / 7l / 7m 在场 |
| M | `eb350937` (qa/M1 · cr/M2) | closed | qa/M1 点名的 8 个存活者都有了对应行, 定义均已实读: 2e / 2f (`baseline_probe.py:549-550`)、7k (`:699`)、12n (`:1059`, 15/16 两侧)、12o (`:1071`, 两条回退腿)、19ac (`:1395`)。cr/M2: 22bo 22 个成员在场; `ssh host env` / `bash -c env` / `watch env` 均为「0 → 2」; W11 `:194` 已改为纳入 |
| P | `05982c10` (qa/M2 · cr/M1) | closed | `refs3.sh` 对本分支照 `:357-360` 原样实跑: 第 1 步 `9` / `rc=0`; 第 2 步干净 `rc=0,1`; 起点不可解析 `rc=128,1` (即「没跑成」); 第 3 步空文本 `rc=1,`; 违规文本有输出且 `rc=0,0`。引文 `detailed-tasks.yaml:342` 已实读并与原文对上 |
| R | `28af0372` (qa/M3) | closed | 只含注释的扩展文件 (`proj_c`): 目标对 Read / Edit `/x/README.md`、`/x/notes.txt` 都是 0; 非作者复构的 `ext_emptypat` 都是 2。20o-20q 在场 |
| E | `44b5bb44` (qa/M4) | closed | `l3locale.py`: 40 位纯大写与纯小写值作 json:token, 目标在 {默认 bash, 真 bash 3.2} × {C.UTF-8, en_US.UTF-8} 四种组合下都静默; `ent_range` 只在 bash 3.2 + en_US.UTF-8 告警 `json-credential-field=1`。32d 在场 |

R3 minor 中本席认为仍未处置的: 无。抽查结果如下:
- `cfb2fb14`: `:367` 与 `:378`, 输出标记与 `plugin-cache-currency.py` 的 `OK ` / `##SKIP##` / `STALE` / `AHEAD` / `MALFORMED` 一致;
- `6ff1d962` (本席 R3 m2): 22bh 已含 systemd-cgls / pidstat-l / w / busybox-ps / ps-aix-format;
- `15da802b`: `:149`;
- `44510e65`: `:121`;
- `5e342bfd` / `4447c607`: `:237` 与 `:241`;
- `26e1a7a9`: `:145`;
- `f410df76`: `:354`;
- `b298cc56` / `a6304dd1`: `:242` 与 SC-28。

## 对执笔人自报薄弱点与请裁项的表态

**§6 自报薄弱点**

1. **同源盲区**: 可接受。本轮再次印证, 本席两条 major 都不在「成员缺项 / 上界差一 / 作用面 (tag × 步骤)」三类变异之内:
   - M1 属「tight 作用面越界」, 即 tight 拷贝覆盖了未列入 tight 族的备选;
   - M2 属「命中路径的时间复杂度」。

   建议 Tasks 1.8 增列这两类。
2. **体量**: 可接受。执笔预警的「新文字与新行的一致性 (尤其 SC-22)」确实落在 22bo 与 tight 定义的接缝上 (M1)。
3. **验收前置**: 可接受。`setpriv` 降权路径未在 root 下实测, 由 1.1 的「降不了权上报」兜底。
4. **精化回归**: 可接受。「红过的仍红」正是回归判据。
5. **等价变异 (4 + 14)**: 可接受, 均已逐个论证。
6. **时档单机比值**: 有条件可接受。(f) 仍靠 100 ms 地板 (R3 已提); 另有 M2, 命中路径无档。
7. **新增 / 反转的已知限制与误拦面**: 部分可接受。
   - 19ae 交 owner (待复议 24);
   - `sh -c 'printenv'` 反转为纳入可接受;
   - 但「env 作参数词 / 文本提及」未申报 (m1)。76 条良性样本里没有 venv / 目录名为 env 的包裹形态。
8. **差分核对范围**: 可接受。但它不覆盖命中路径的阶段计算成本 (M2)。
9. **7n**: 可接受, 建议保留 (廉价、可证伪)。
10. **证据运行负载**: 可接受。本席测量期间负载 20-37。

**§7 甲 技术级请裁 (待复议 21-30)**

- 21 可接受: 实测 environ / cmdline 两形均转为检出。
- 22 可接受: 已实测。
- 23 原则可接受: 但它的两个后果须写清, 即 tight 归属 (M1) 与 env 作参数词 (m1)。
- 24 可接受: 但掩码拉长了无分隔符前缀, 放大了 M2。
- 25 可接受: 实测目标 0/5 诱饵, `vx_eval` 3/5。
- 26 可接受: 已实测。
- 27 可接受: 范围须扩到 env 备选 (m1)。
- 28 可接受: 但缺「tight 覆盖哪些备选」这一维 (M1)。
- 29 可接受: 三态已实跑。
- 30 可接受。
- 甲.2 (17 / 20 的文字更新): 可接受。

**§7 乙 Rule #10 自作主张**

1-5 均可接受。第 2 条抽查了 28a / 28e / 28f 与 7n 的定义在场。

**§7 丙 未采纳的席位备注**

1. **SC-14 canary**: 可接受不采纳 (不阻塞)。建议在 Tasks 1.3 写一句实现注意, 成本很低。
2. **W5 `source` 形状校验**: 可接受不采纳 (受 matcher 限定)。
3. **MINGW64 / macOS 未实测**: 不可接受不采纳。在 10CG/aria-plugin#154 关单评论里加一句「未在 MINGW64 / macOS 验证」成本为零, 而 10CG/aria-plugin#203 的报告环境正是 MINGW64; 关单评论又是不可撤回的外发动作, 宜如实。
4. **km 风险**: 「Layer 2 无人值守下新拦截的影响」建议在 Impact 写一句 (见风险 2); 其余可接受不采纳。
5. **timing.py 无判据输出**: 可接受。补 M2 的档位时建议一并输出判据。
6. **7.1 配方披露范围**: 交 owner, 本席倾向保留, 同 R3。**认领心跳**: 属主控例行维护, 进 A.2 前须续期或重新认领。

## 风险 / 疑问

1. **主机负载与 5 s 墙钟超时**:
   - 本席测量期间 (负载 20-37), **基线** hook 对约 2 KB 单行命令的墙钟为 1.5-4.6 s, 对约 8 KB 为 22 s。也就是说, 在这台共享开发机上, 既有的超时即放行悬崖 (7.1) 单靠基线就能触到。
   - W14 的「基线 CPU ≥ 5 s 判环境不合格」只管测量口径, 生产行为看的是墙钟。建议 7.1 开单时写入负载下的墙钟实测。
2. **Layer 2 (aria-runner)**: 新拦截在无人值守运行里同样生效, 包括 `ps aux | grep`、M1 / m1 两类, 而那里的 `# guard:ack` 只能由 AI 自己写 (与 Rule #10 的精神有张力)。建议 Impact 加一句。
3. **待复议 18 的定级**: 扩展失效静默仍列技术级。本席仍认为它属产品级 (R3 风险 3), 只提示, 不重报。
4. **W1「命中不会因此减少」**: 对现实内容成立。只有人为构造的「NUL 落在值中间」才会丢掉基线靠拼接得到的命中, 可忽略, 不计 finding。
5. **macOS libc 正则 / MINGW64 未实测**: 沿用 R3 的提示。
6. **本席自身操作**:
   - 有两条 Bash 命令被现行 v1.74.1 的 L1 拦下, 原因是命令文本 (正则参数与用例清单) 提到了 `ssh … "…env"` / `| printenv`。本席改用 Write 工具落文件, 未用 `# guard:ack`。这本身也是文本提及误拦族的一个实例。
   - 全程未读取或打印任何真实凭据。
   - 查看忙碌子进程时只读了自起 hook 进程的 fd 255 链接 (脚本路径), 没有读任何进程的 cmdline 或 environ。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: **0C / 2M / 2m**
- **Vote: REVISE**

## 是否足以进入 A.2

**不足以。** 两条 major 都是局部改动, 不需要新机制, 但在进 A.2 前必须先落地:
- M1: 一句 tight 归属的决定 + 一行 SC + Impact 申报;
- M2: 一个命中时档 + 改写 W9 / Impact 的成本表述。

R3 的 10 个 C+M 键本席核验均已关闭。