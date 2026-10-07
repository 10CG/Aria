---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T09:41:20.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — qa-engineer 席报告 (WP-A secret-net-l3-and-bypass-paths, proposal v5 @ 6efb9b2)

视角: 每条 Success Criteria 的可证伪性 (基线 / 目标 / 坏实现三态)。

**摘要**: R4 的 1C/9M 六个簇 (U `1038b8da` / T `0a8380fd` / V `22bdd143` / W `755aab21` / F `e2459206` / M `eb350937`) 我独立复核**全部关闭**, 本轮无 critical。新发现 2 条 major + 3 条 minor, 全部是「补行 / 补一条耦合清单项」型, 不涉设计取舍:

- **M1** (SC-22): W11 写的是语义 (命令位置字符集、「簇内含 `a`」、「列表含 `args|cmd|command`」、「`-f` / `-F`」), SC-22 钉的只是规范拼写。命令位置锚点的 `&` / `{` / 反引号, `pgrep` / `pstree` 的 `-a` 不在簇首或不在首个操作数, `ps -o` 列表里关键字不在末位, `ps -F`, `docker ps -a --no-trunc`, launcher 时长后缀 `m` / `h` / `d`, 这六类自然的单点窄化实现在全部相关探针行上 0 行红, 却放行 `pgrep -fa curl` 一类 10CG/Aria#221 同型的列举命令。
- **M2** (SC-30): W9 把 `_sg_per_segment_eval` 的函数体提出为 `_sg_core_eval` 后, 既有测试内 SC-8 五档延迟闸 (owner 2026-08-24 裁定、SC-30 点名的一条腿) 用 awk 锚点只抽到「壳」, 每次调用 `_sg_core_eval: command not found` (rc 127)。我在含 `af87cae` 历史的真 clone 上实跑: 「新侧」耗时从 10–123 ms 降到 1.8–3.2 ms, 五档全绿, 而同一主机上基线本身 (e) 档红。W14 的耦合清单没有这一项, SC-30 没有活性断言。

**方法**: 全部在 `.../audit/post_spec-R5-qa-engineer/` 下做, 真仓 HEAD 仍是 `6efb9b2`、`git status` 与开始时一致 (仅 `git clone` 读本地仓与 `git grep`, 无 git 写操作)。(1) 副本 (aria `268da8f` + standards `2bc1c4c`, 删子模块 gitfile, uid 1000, HOME / TMPDIR 在本席目录) 带真 bash 3.2.57 全量复跑基线探针; (2) 用执笔归档的补丁脚本重建目标原型并带 `WPA_REQUIRE_ALL=1` 全量复跑; (3) 抽样复跑执笔坏实现, 并自造「自然窄化」坏实现 (对原型 hook 的单点正则 / 位置改动) 找存活者; (4) 手写、不经探针的差分与普查; (5) 在含 `af87cae` 的私有 clone 上跑既有 `secret-guard.test.sh` (SC-30 的 git 腿) 基线与目标原型各一遍。Rule #7: 值只在进程内生成、从不打印, 本报告只写退出码 / 计数 / tag 名 / 占位。

## 已实读文件

- 被审对象: `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-449 (Why / W1-W14 / Out of scope / SC-1…SC-34 / rule6_note / Impact / Tasks / 待 owner 复议 1-32); v4 到 v5 的差异: `git diff b07f69a 6efb9b2` 的词级片段 diff (101 KB) 全部过目; `baseline-evidence.md` 头部 1-60 + 437 行逐行解析 (类别 / 形态 / case id 与 proposal 双向交叉: 无悬空 id; 内嵌 stdout 块与我的实跑逐字节相等); `baseline_probe.py` 精读 1-120、296-330、394-600、882-1012、1333-1470、1510-1760、1990-2110、2402-2500、2510-2682, 其余以 evidence 的行描述加抽样执行代替 (**未逐行通读 2682 行**)。三份文件 sha256 前 16 位 `cedbdfce05575891` / `cf331b4aa264a863` / `b41e86d796bb583c`, 与执笔报告一致。
- issue 与决策: aria-plugin-154 / aria-plugin-203 / Aria-221 正文加全部评论; `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; CLAUDE.md #6 / #7 / #10 与多远程两条硬约束。
- 源码与规范: `aria/hooks/secret-scan.sh` 1-377 全文; `aria/hooks/secret-guard.sh` 1-1120 (risky_patterns 段抽读, 其余精读); `aria/hooks/hooks.json` 全文; `aria/hooks/tests/secret-guard.test.sh` (1-120、:1258-1330、:1660-1900 与全部对内部函数的引用点); `standards/conventions/skill-benchmark-exemption.md` 全文; `secret-hygiene.md` (版本行 / 标题 / 引用面); `COMMIT_FOOTER_GUIDE.md:196-203` 与 `git-commit.md` §6.1 (核 Impact 引用: `:199-200` / `:201-202` 属实); `aria/README.md` / `README.zh.md` 的 Hooks 标题; 主仓 `72cb02b` / `a99dd8d` 文件清单 (核 16 个版本点: 2+2+3x3+1+1+1)。
- 上一轮与执笔材料: R4 聚合报告全文; 我 R4 的报告全文; `v5-writer-report.md` 全文; `writer-v5-proto/` 的 README、`patch_l1.py` / `patch_l3.py` 变体表与关键段、`mut_summary_v5.txt`; 主控 `tooling/canon-R4.json` (只用于避开 id 别名, 见 Findings 说明)。
- 未读: 四份研究笔记 (背景材料; 其中的平台事实我用本会话真实 transcript 实测代替); 10CG/Aria#199 的 `detailed-tasks.yaml` (只跑了它的守卫命令)。

### 实跑核验 (三态摘要)

1. **基线 (独立复现)**: `WPA_BASH32=<真 3.2.57> python3 baseline_probe.py <副本>/aria`, 非 root, rc 0, stderr 空, stdout 97972 字节, sha256 前 16 位 `526efaa2b5a9d52e`, 与 evidence 内嵌块逐字节相同。baseline-failing 0/213, doc-sync 0/26, reverse-guard 79/79, allow-guard 70/70, known-limit 39/39, zero-regression 9/9 (30a 设计上不执行), 基线形态 `holds`。即 Rule #6 substitute 所依赖的 213 + 26 条结构化测试确实 baseline-failing。
2. **目标原型 (我重建)**: hook 指纹 `4b2ddba40b080619` / `a7b8109bb3f8e576` (与执笔 final_T 相同); `WPA_BASH32` + `WPA_REQUIRE_ALL=1` 全量: rc 0, stderr 空, stdout 95688 字节, sha256 前 16 位 `baf7c962e4e78392`, 与执笔 `final_T.out` 逐字节相同; 436 行 yes + 30a n/a, 目标形态 `holds` (含 32c / 32d / 32e 各 382 行一致、29h / 29i 在真 3.2 下 49/49 与 581/582)。「基线红 / 目标绿」两态没有一行说谎。
3. **手写、不经探针的复核**:
   - 47 条 L1 命令 (包裹 x env 转储、ps 家族、/proc、`os.environ`、`app.ini`、jq) 基线 / 目标对照, 与 Spec 声明逐条一致: `docker exec c env | grep '^PATH='` 两侧 0; `nomad alloc exec -task t a1 env` 0 到 2; 同命令接 `| grep '^X='` 两侧 0; 接 `| grep -v PATH` 两侧 0 (22bs 的既有限制); `ps aux | wc -l` 两侧 0; `bash -c "python3 -m venv env && echo ok"` 0 到 2 (22bj 已申报误拦)。
   - 良性命令模糊 520 条 (赋值 / `for` / heredoc / 引号 / 替换 / 多赋值): 基线与目标零差异, 无内部错误, 无 fail-closed 假拦。
   - 原位改写族回归差分 938 例 (/proc 读取器 x pid 记号 x 文件、`python3 -c` / `node -e` / `lua -e` x 名字、claude-config tight x 读取器 x 17 种过滤、非 tight 源 x 过滤、`os.environ` 20 种写法): 基线拦到目标放共 58 条, **全部**落在已申报的 W12 (`os.environ` 单键 22、`os.environb` 单键 6、jq `keys_unsorted` / `map_values(length)` 30), 0 条未申报回退; 基线放到目标拦共 150 条: `app.ini` 6、新增 /proc 读取器与新 pid 记号 144, 占位词 `N` / `<pid>` 与 `status` 均未被拦 (与 22bf / 22as 一致)。
   - L3 检出回退差分: 31 个基线 tag x 10 种上下文 (行首 / 行中 / 缩进 / CRLF / 制表 / JSON 内嵌 / 同行三次 / 4 KB 前缀 / 相邻另一凭据 / Write 信封) = 310 次, 目标计数 >= 基线计数全部成立, 0 回退。
   - 误报普查 (SC-33 语料之外: 主仓 `docs/` `openspec/` `aria-orchestrator/` `.aria/` 与根级 md, 1510 个候选文件): 预筛命中 8, 目标告警 5; 命中新 tag 的只有 3 个 (编排器两个 redaction 测试夹具与一份 T2 证据文档, 值是占位 / 夹具), 与 W2 已知误报类一致; 另 2 个是 Read 首次被扫描后既有 tag 的命中。
   - W2 线性论据: GNU grep 对 kv pattern 的 CPU: 有界 (目标) 100 KB 0.06 s / 200 KB 0.11 s; 无界加左边界 1.49 s / 6.88 s; 无界且无左边界 40 s 被杀。
   - 时档 (`timing.py --judge`, 每档 3 对, 整进程 CPU 最小值之比): (f0) 1.13 / 1.09; (f-hit) 2.01 (1 次出现) / 1.97 (64 次), 对照 1.08, 活性 `_sg_core_eval` x2; (i3) 1.41 / 1.46 / 1.29 / 1.89 / 1.16; 9 个有界档 0 失败。
   - ext 对 builtin 随机差分 (执笔的 `fuzz_ext_builtin.py`, 我换种子 424242, 500 条): 371 条被 builtin 拦, 0 分歧。
   - W1 的 NUL 平台前提 (Spec 称本机无端到端样本): 本会话实测 Bash 输出 `printf 'HOME=/x\0PATH=/y\0'` 与 Read 一个含 NUL 的 `.txt`, 两个工具结果在 transcript 里都**保留 NUL** (JSON `\u0000`), 即 NUL 确实到达模型侧 tool_result; hook 载荷本身未直接观测。
   - 10CG/Aria#199 的守卫命令 (`git grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'`) 真仓只读运行: 末行 `rc=0,1`, 其前无输出 = 通过。
   - 既有 `secret-guard.test.sh` 在含 `af87cae` 的真 clone 上: 见 M2。
4. 坏实现: 见下表与 M1 / M2 / m1。

### 逐 SC 三态表

图例: bf = baseline-failing, doc = doc-sync, rev = reverse-guard, allow = allow-guard, kl = known-limit, zr = zero-regression; 「我跑」= 本席亲自对原型复跑, 「执笔」= 执笔汇总里的记录 (未复跑)。

| SC | 基线 (我跑) | 目标 (我跑) | 坏实现 → 转红的行 | 判断 |
|---|---|---|---|---|
| 1 | bf 0/5, rev 2/2 | 全 yes | `nul_off` → 1c 1d; `nul_replace` → 1e 1f; `nul_always_append` → 1g (我跑) | 可证伪 |
| 2 | rev 6/6 | 全 yes | `drop_extract` → 2e 2f (执笔) | 可证伪 |
| 3 | kl 2/2 | 全 yes | known-limit, 扩面即转红 | 设计如此 |
| 4 | bf 0/19 | 19/19 | `ent_digit` → 4o; `path_plus` → 4n (我跑); `drop_name:*` 58 个 (执笔) | 可证伪 |
| 5 | bf 0/14 | 14/14 | `path_plus` → 5l (我跑); `drop_kwkv:*` (执笔) | 可证伪 |
| 6 | bf 0/11 | 11/11 | `drop_flag:token` → 6i; `drop_scheme:Basic` → 6j; `drop_vsym:kv:~` → 6k (我跑) | 可证伪 |
| 7 | rev 14/14 | 14/14 | `wl_prefix` → 7h 7i 7j; `order_first` → 7j 7k 7l 等 35 行; `order_before_json` → 13 行 (我跑); `order_end` 存活 (等价, 见风险 9) | 可证伪 |
| 8 | bf 0/1 | 1/1 | `order_first` → 8a (我跑) | 可证伪 |
| 9 | allow 26/26 | 26/26 | `name_loose` → 9x 9j (我跑); 与 SC-4/5/6 同形正例成对才有鉴别力 (Spec 已自述) | 可证伪 (成对) |
| 10 | kl 14/14, bf 0/1 | 全 yes | `floor15` → 10h (我跑) | 可证伪 |
| 11 | allow 13/13, bf 0/11, rev 2/2 | 全 yes | `wl_*` 系列 (执笔); `wl_prefix` → 7h 7j (我跑) | 可证伪 |
| 12 | bf 0/12, rev 3/3 | 全 yes | `fp_span` → 12g 12h; `fp_le16` → 12n; `hash_noshasum` → 12o (我跑); **`fp_all_spans` 存活 (m1)** | 缺一行 (m1) |
| 13 | bf 0/4, rev 3/3 | 全 yes | `w5_append` → 13d (我跑) | 可证伪 |
| 14 | bf 0/2 | 2/2 | 没隔离 HOME 即红 (基线 33 行 / 12 条) | 可证伪 |
| 15 | bf 0/1, allow 6/6 | 全 yes | 我另扫三份文件: 基线与目标静默 | 可证伪 |
| 16 | bf 0/16, rev 2/2 | 全 yes | `drop_reader:*` `drop_interp_name:*` (执笔) | 可证伪 |
| 17 | allow 2/2, kl 2/2 | 全 yes | `bash_boundary_wide` `appini_anywhere` (执笔) | 可证伪 |
| 18 | bf 0/6, allow 3/3, rev 2/2 | 全 yes | `readface16` → 18j 18k 各 16/32; `readface_check.py` 32 路径各只命中一个基线备选 (我跑) | 可证伪 |
| 19 | bf 0/26, allow 7/7, rev 2/2, kl 2/2 | 全 yes | `ext_v4stage:noesc_q` / `:noansi` → 19af 50/73 与 52/73、19al; `ext_charslice` → 19ag; `ext_localnoexp` → 19ah 19am; `ext_nobom` → 19ai (我跑) | 可证伪 |
| 20 | rev 15/15, bf 0/2 | 全 yes | `ext_bare` `ext_emptypat` (执笔); 20g 在 root 下 n/a | 可证伪 (有 n/a 腿) |
| 21 | bf 0/11, allow 1/1, kl 9/9, rev 2/2 | 全 yes | `vx_eval` → 21z (执笔) | 可证伪 |
| 22 | bf 0/57, rev 2/2, allow 10/10, kl 5/5 | 全 yes | `env_tight` → 22br 0/44、22bs 0/22; 锚点去 `;` → 22az 0/5; 去 `|` → 22ax 12/14; 去 `(` → 22w (我跑); **六类自然窄化存活 (M1)** | 缺口 (M1) |
| 23 | bf 0/3, rev 4/4, kl 3/3 | 全 yes | `w12_once` → 23j (我跑) | 可证伪 |
| 24 | bf 0/5, rev 1/1, allow 1/1, kl 2/2 | 全 yes | `jq_loose` (执笔) | 可证伪 |
| 25 | rev 4/4, bf 0/4 | 全 yes | `w12_echo_norm` → 25h (我跑) | 可证伪 |
| 26 | doc 0/9, rev 2/2 | 全 yes | 文档类坏实现 (执笔) | 可证伪 (关键词判据, 性质所限) |
| 27 | rev 2/2, doc 0/2 | 全 yes | 无自检变体 (执笔) | 可证伪 |
| 28 | doc 0/15 | 15/15 | 半截改写变体 (执笔) | 可证伪 |
| 29 | zr 9/9 | 9/9 | 反回归, 不作功能证据 | — |
| 30 | 探针外 | 探针外 | 时档 (f0)(f-hit)(i3) 我跑 PASS; SC-8 腿对「壳」实现恒绿 (M2) | 缺口 (M2) |
| 31 | rev 5/5 | 5/5 | (执笔) | 可证伪 |
| 32 | rev 5/5 | 5/5 | `ent_range` → 32d, `ell_lastchar` → 32e (执笔; 本席未复跑: 全量 hook 直调差分单次约 10 分钟以上) | 可证伪 |
| 33 | allow 1/1 | 1/1 | `noentropy` (执笔) | 基线恒绿 (设计所限) |
| 34 | rev 1/1, bf 0/2 | 全 yes | `cli_unbounded` `cli_v4` `cli_noleft` → 34b (cli-dash-run); `kv_unbounded` → 34b (kv-upper-run); `val_quadratic` → 34a 34b (我跑); `ext_perocc_judge` → 34c 在本机以探针 TimeoutExpired 崩溃而非红行 (风险 3) | 可证伪 |

## Findings

> id 说明: M1 的 scope 取 `proposal.md Success Criteria` 而不是 `SC-22`, 因为 (testing, SC-22, major, issue) 的键 `5ce95ecf` 在主控 `canon-R2..R4.json` 里已别名到 `eb350937` (簇 M); 本条与簇 M 无关, 用别名键会被自动并入。行级定位见正文。

### Critical

无。我没有找到「照 Spec 字面实现会使现有拦截或检出变成放行」的路径: 938 例原位改写差分里基线拦到目标放的 58 条全部是已申报的 W12; 310 例 L3 检出差分 0 回退; 簇 U 的 UTF-16LE 回退已关闭 (见对账)。

### Major

**M1** — id `12a776ac` / major / issue / testing
scope: `proposal.md Success Criteria` (行级: SC-22 与 W11 `proposal.md:194-195`)
summary: W11 描述的是语义, SC-22 只钉了规范拼写; 命令位置锚点的 `&` `{` 反引号三个成员、`pgrep` / `pstree` 的 `-a` 位置、`ps -o` 列表关键字位置、`ps -F`、`docker ps -a --no-trunc`、launcher 时长后缀六类自然的窄化实现在全部相关探针行 0 行红, 却放行 10CG/Aria#221 同型的进程列举命令。
证据:
- W11 原文 (`proposal.md:194-195`): 「命令位置 = 行首、`;` `&` `|` `(` `{` 与反引号之后、控制字符之后, 或 `then` `do` `else` `elif` 之后」; 「第 3 类 SysV `-f` / `-F` 簇」; 「第 4 类 `-o` / `--format` **列表含** `args|cmd|command`」; 「`pgrep -a` / `--list-full`; `pstree -a` / `--arguments`」; 「`docker ps --no-trunc` / `docker container ls --no-trunc`」; launcher 后「数字 / 时长操作数 (`5`、`5s`)」。SC 导言 (`proposal.md:263`) 称「每个枚举集合 (…) 都做过『删掉任一成员』的坏实现」, 列出的 W11 集合是 launcher / `/proc` 读取器 / 远程包裹 / ps 备选 / pid 位置 / 关键字位置 / 非 ps 拼写, **不含命令位置字符集**。
- SC-22 的构造器 (`baseline_probe.py:1695-1712`、`:1726`) 与 74 个行 id: `pgrep` 只出现 `-a` `-af` `--list-full` (簇首、首个操作数); `pstree` 只 `-a` `-ap` `--arguments`; `-o` 列表只出现关键字在末位或以 `=` 结尾 (`pid,args`、`pid,command -p`、`args=`、`pid,cmd`); 无任何 `-F`; `--no-trunc` 只在 `docker ps` / `docker container ls` 的首个操作数; launcher 时长只有 `5` 与 `5s`; 命令位置只覆盖行首、`(` (22w)、`|` (22ax 的 `pgrep -f x | xargs ...`)、`;` (22az 的 then/do 形)、换行 (22bj)、关键字 (22az)。
- 坏实现 (均为对目标原型 `secret-guard.sh` 的单点正则改动, 每处拷贝都改) 与结果:

| 坏实现 | 跑的行 | 非 yes | 直接喂 hook: 命令 → 基线 / 目标 / 坏实现 |
|---|---|---|---|
| `anchor_combo`: 命令位置类 `(^|[;&|(){]|`|[[:cntrl:]])` 改成 `(^|[;|()]|[[:cntrl:]])` (去掉 `&` `{` 反引号) | SC-16 至 SC-25 全部 211 行 | 0 | `sleep 1 & ps aux` 0/2/0; `{ ps aux; }` 0/2/0; `` echo `ps aux` `` 0/2/0 |
| `pgrep_afirst`: `(-a[a-zA-Z]*\|--list-full)` | SC-22 全部 74 行 | 0 | `pgrep -fa curl` 0/2/0; `pgrep -la curl` 0/2/0; `pgrep -ifa curl` 0/2/0 |
| `pgrep_firstonly`: 去掉 `([^\|;&]*[[:blank:]])?` 前缀 | SC-22 的 68 行 | 0 | `pgrep -u root -a curl` 0/2/0; `pgrep -x -af nginx` 0/2/0 |
| `pstree_afirst` / `pstree_firstonly` | 74 行 / 68 行 | 0 / 0 | `pstree -pa` 0/2/0; `pstree -ua` 0/2/0; `pstree -p -a` 0/2/0 |
| `ps_o_end`: `(args\|cmd\|command)([[:blank:]=]\|$)` | SC-22 全部 74 行 | 0 | `ps -eo args,pid` 0/2/0; `ps -o cmd,%mem -p 1` 0/2/0 |
| `ps_F_lower`: `-F` 簇只认小写 `f` | 68 行 | 0 | `ps -eF` 0/2/0; `ps -F -p 123` 0/2/0 |
| `docker_notrunc_first`: `--no-trunc` 只认首个操作数 | 68 行 | 0 | `docker ps -a --no-trunc` 0/2/0; `docker container ls -a --no-trunc` 0/2/0 |
| `launcher_dur_s`: 时长后缀只认 `s` | 68 行 | 0 | `timeout 5m ps aux` 0/2/0; `timeout 2h ps -ef` 0/2/0 |

  「68 行」= SC-22 去掉六个大枚举行 (22bm 22bn 22bo 22bq 22br 22bs) 的其余行; 这六行的构造器 (`WRAP_T` / `NONPS_FORMS` / `PS_CLASSES` / `LAUNCH15`) 只含首位 `-a` / `-af`、末位关键字、小写 `-f`、首个操作数 `--no-trunc`、无时长, 对前五类窄化不可能转红 (我对 `ps_o_end` / `pgrep_afirst` / `pstree_afirst` 另跑这六行实证 0 行红)。
- 对照 (被钉住的成员): 去掉 `;` → 22az 红 (0/5); 去掉 `|` → 22ax 红 (12/14); 去掉 `(` → 22w 红; `)` 是惰性成员 (去掉后 0 行红且行为不变, 等价变异)。即 7 个锚点成员里 `&` `{` 反引号三个没有任何行。这三者只在「整串降级」路径起作用 (`&` 后台、`{ }`、反引号会使 `_sg_safe_to_split` 返回 1), 正是内建 `env` / `printenv` 行用同一字符集要覆盖的形态; `cd /tmp && ps aux` 因分段不受影响 (坏实现仍拦)。
失败场景: 实现者照 W11 的规范拼写写正则 (自然地把 `-a` 写在簇首、`-o` 关键字写在列表末、`--no-trunc` 写在首个操作数、锚点类写成 `[;|()]`、时长只认 `s`) → 探针 + 既有套件全绿 → 发版后 `pgrep -fa <名>`、`docker ps -a --no-trunc`、`ps -eo args,pid`、`timeout 5m ps aux`、`sleep 1 & ps aux` 等进程完整命令行的列举放行, 凭据 (`Authorization: token …` / `CF-Access-Client-Secret`) 经进程表进入 tool output (L3 只事后告警, 无预防); 「规范拼写都被拦」的假象还让使用者以为整族已覆盖。这些窄化只是自然可能 (W11 文字没写「任意位置」), 不是笔误; 按本仓 R3 / R4 同类先例 (`eb350937`、`0a8380fd`) 定 major, 未升 critical。
建议修法: (a) SC-22 增三个 `baseline-failing` 枚举行 (每成员一次独立运行, 期望退出 2, 基线全 0): 命令位置成员 (`true & ps aux`、`{ ps aux; }`、`` echo `ps aux` ``、`true; ps aux`、`true | xargs ps aux`、`(ps aux)`); 簇 / 操作数 / 拼写位置 (`pgrep -fa curl`、`pgrep -la curl`、`pgrep -u root -a curl`、`pstree -pa`、`pstree -p -a`、`ps -eF`、`ps -F -p 123`、`docker ps -a --no-trunc`、`docker container ls -a --no-trunc`、`timeout 5m ps aux`、`timeout 2h ps -ef`); `-o` 列表关键字位置 (`ps -eo args,pid`、`ps -o cmd,%mem -p 1`、`ps -eo pid,args,etime`); (b) W11 把语义写进文字: 「任意位置含 `a` 的短横簇与任意操作数位置」「列表任一位置含」「`--no-trunc` 在 `ps|ls` 之后的任一位置」「时长后缀 `s` `m` `h` `d`」; (c) Tasks 1.8 的缺项类清单加「命令位置字符集缺成员 / 簇内字母只认首位 / 列表关键字只认末位 / 操作数只认首个」。

**M2** — id `6bd285b1` / major / issue / testing
scope: `proposal.md SC-30` (耦合清单在 W14 `proposal.md:241-242`)
summary: 按 W9 的设计把 `_sg_per_segment_eval` 的函数体提出为 `_sg_core_eval` 后, 既有测试内 SC-8 五档延迟闸只抽到壳、每次调用 rc=127, SC-30 的这一腿对该实现恒绿; W14 的耦合清单与探针都没有这一项。
证据:
- W9 (`proposal.md:165`): 「`_sg_core_eval` (即基线 `_sg_per_segment_eval` 的函数体, 原样: ...)」; 执笔报告 §3.4: `_sg_per_segment_eval` 与 `_sg_ext_pass` 各调用它。原型 (我重建, 与执笔相同) 中 `_sg_per_segment_eval` 是只调用 `_sg_core_eval` 的壳, `_sg_core_eval` 定义在测试 source 闸门**之下** (`secret-guard.sh:1297`, 闸门 `:665`)。W10 / W14 的「新函数放在 source 闸门之上」只对新辅助函数说, 没有规定 `_sg_core_eval` 的位置。
- 既有测试 `aria/hooks/tests/secret-guard.test.sh:1771-1785`: `source "$HOOK"` (只带闸门之上的部分) 后用 `awk` 锚点抽取 `risky_patterns`、`_sg_judge_one`、`_sg_per_segment_eval` 三段; `:1849-1853` 的 `_sc8_bench_new` 计时 `_sg_per_segment_eval`; `:1800-1808` 的 `_sc8_time_calls_us` 丢弃返回码与输出 (`>/dev/null 2>&1`)。
- 复现 (抽取原样复刻, `t_sc8.sh`): 基线 hook 对 benign / `wget … | wc -l` / `nomad var put … >/dev/null` 三条返回 rc 0, 对 `cat .env` 返回 2; 目标原型对四条全部 `_sg_core_eval: command not found`, rc=127。把 `_sg_core_eval` 移到闸门之上: rc 0/0/0/2 恢复正常。
- 真 git checkout (aria `268da8f` 的私有 clone, `af87cae` 可达, 叠上目标原型的 hooks 与两个测试套件), 跑 `bash hooks/tests/secret-guard.test.sh`, 负载约 19: 基线 592/593, SC-8 new = 10.1 / 23.9 / 17.4 / 18.8 / 123.1 ms/call, **(e) 档 123.1 ms 超天花板 100 ms 而红** (主机负载所致); 目标原型 595/596, SC-8 new = **1.8 / 2.0 / 1.9 / 1.7 / 3.2 ms/call (increase(min) = -97%)**, 五档全绿, 唯一 FAIL 是 SC-13 头注释计数 (B.2 回填, 与探针 29b 的环境性假红同一条)。SC-9a 在两侧都过。
失败场景: 实现者最自然的做法 (原位把 `_sg_per_segment_eval` 改名为 `_sg_core_eval`, 再写一个壳) → B.2 跑全量套件, SC-8 五档「新侧」缩水 97% 全绿 → 勾选 SC-30 → 没有任何 SC 在测「每条命令多一遍判定」的绝对耗时 (W14 的整进程 CPU 时档不含 SC-8 的最坏档 (e): 4 段各命中数组末位加 `| wc -l`); hook 超时即放行, 这是 owner 2026-08-24 专门设的延迟闸。W1 的「既有 L3 行与两个套件在原型上全部照过」只在无 git 的副本上成立 (SC-8 在那里被跳过)。
建议修法: (a) W14「其它耦合」加一条: 测试内 SC-8 / SC-9a 按名字抽取并 `source` 闸门之上的部分, `_sg_core_eval` 及其依赖必须定义在 source 闸门之上 (或保持 `_sg_per_segment_eval` 自包含、让 `_sg_core_eval` 调它); (b) 探针加一行 `reverse-guard` (不需 git): 复刻 SC-8 的抽取, 断言五档负载的新侧返回 0 且 `cat .env` 返回 2、不是 127 (基线 yes / 目标 yes / `_sg_core_eval` 在闸门之下 no); (c) Tasks 1.1 记 SC-30 基线时同时记 loadavg (见风险 5)。

### Minor

**m1** — id `c7bff9bd` / minor / issue / testing
scope: `proposal.md SC-12`
summary: W4 规定指纹只对「被计数的 span」取, SC-12 没有任何行钉住「被分类器排除的 span 不记指纹」; 先记指纹再分类的实现在 99 行相关探针上全绿, 并会让占位符挤掉真凭据的指纹。
证据: W4 `proposal.md:108` 「对每个被计数的 span 取凭据本体 … 最多记 10 项」。坏实现 `fp_all_spans` (在原型 `secret-scan.sh` 的分类循环里把 `_fp_add "$v"` 提到白名单 / 熵 / 路径判断之前, 删去计数后的那次): `WPA_ONLY=SC-4,5,6,7,11,12` 共 99 行 `non-yes: 0`; 直接喂: 12 个被白名单排除的 `{"token": "<…>"}` 占位后接 1 个真凭据, 目标日志 fp 字段含真凭据的 sha256 前 8 位 (1 项), 坏实现 fp 字段 10 项且不含它。SC-12 的 12a-12o 全部只含被计数的 span。
失败场景: 实现者在取值处顺手记指纹 → 验收全绿 → 文档类输出里出现 10 个以上占位符时日志对不上真凭据, 违背 10CG/aria-plugin#154 交付物 3 (日志里留可与台账比对的指纹)。无检出 / 拦截回退, 故 minor。
建议修法: SC-12 增一行 `baseline-failing`: 11 个被白名单排除的占位 span 后接 1 个真凭据, 期望 fp 恰为该凭据的 sha256 前 8 位一项。

**m2** — id `0033f2f4` / minor / issue / documentation
scope: `proposal.md 待 owner 复议`
summary: W2 与 W8 的已知限制都写「FORGEJO__ / GITEA__ 环境变量覆写并入建议开单 7.8 / 7.9」, 但 7.8 与 7.9 的正文没有这一项, 引用悬空。
证据: `proposal.md:80` 与 `:157` 写「并入建议开单 7.8 / 7.9」; `:409-410` 的 7.8 (飞书 webhook / Consul SecretID / PascalCase 键) 与 7.9 (grafana.ini / nomad.d / .netrc …) 不含 `FORGEJO__` / `GITEA__`。我对其余全部 `7.N` 与「待 owner 复议第 N 条」引用做了机械核对: 只有这一处主题不符 (`7.88` 是 curl 版本号的误匹配)。
失败场景: 开单时按 7.x 清单逐条建 issue, 这个与 10CG/aria-plugin#203 同一批凭据的缺口 (R4 tl/m2 `984b1c3d` 的处置) 不会被开出来。
建议修法: 在 7.8 或 7.9 加一句 `FORGEJO__<section>__<KEY>` / `GITEA__<section>__<KEY>` 覆写 (SC-10 10m), 或把 W2 / W8 的「并入」改成「另列」。

**m3** — id `f410df76` / minor / issue / documentation
scope: `proposal.md Impact`
summary: Impact「覆盖关系」写 10CG/aria-plugin#154 有「两处有意偏离」, 同节关单口径与 Tasks 1.13 都是「三处」。
证据: `proposal.md:364` 「(两处有意偏离见上 …)」; `:357` 「三处**有意偏离**: (a) (b) (c)」; `:387` 「评论逐条披露三处有意偏离」。
失败场景: 实现者按「覆盖关系」写关单评论只披露两处, 漏掉 (c) `[REDACTED` 前缀值的偏离。
建议修法: 把 `:364` 改成「三处」。

## 上一轮对账

R4 聚合报告里 1 条 critical 与 9 条 major 按主控记录归并为六簇; 我对每簇独立核验:

| 簇 (键) | 席位编号 | 状态 | 我核验的证据 |
|---|---|---|---|
| **U** `1038b8da` | ba/C1 | **closed** | W1 改为两视图并集 (基线视图 D 照扫, 含 `\u0000` 且 N 与 D 不同才追加 N)。`nul_replace` (用 N 替换 D) → 1e 1f 红 (UTF-16 形态四例全静默); `nul_always_append` → 1g 红 (`aws=2`); `nul_off` → 1c 1d 红 (`kv=1`); 目标 1a-1g 全 yes, 基线 1e 1g yes。L3 检出差分 310 例 0 回退。W1 的 NUL 前提另有 transcript 实测支持 (Bash 与 Read 都保留 NUL)。 |
| **T** `0a8380fd` | ba/M2, qa/M1, cr/M1, km/M1 | **closed** (设计整体替换); 但替换引入新的耦合 **M2** | 掩码 / 阶段切分机制已删, 扩展把条目出现换成内建 `app.ini` 名后交 `_sg_core_eval`。19af 73/73 且 10 个锚点形态 ok (目标 yes); 旧设计作为坏实现 (`ext_v4stage:noesc_q` / `:noansi`) → 19af 50/73、52/73 红且 19al 红; `ext_charslice` → 19ag 红; `ext_localnoexp` → 19ah 19am 红; `ext_nobom` → 19ai 红; 独立种子随机差分 500 条 0 分歧。 |
| **V** `22bdd143` | tl/M2 | **closed** | 一次 `grep -oFib -f` + 至多 64 次拼接 + 一遍 `_sg_core_eval`; 时档我复测 (f-hit) 2.01 / 1.97 (64 次出现), 对照 1.08, 活性 `_sg_core_eval` x2; 34c yes。无扩展文件 (f0) 1.13 / 1.09。 |
| **W** `755aab21` | ba/M1 | **closed** | kv / cli 有界加左边界, 取值只用 `%%` / `${s:N}` / `[[ =~ ]]`。GNU grep 实测有界线性 (0.06 s → 0.11 s) 对无界二次 (1.49 s → 6.88 s) 与无左边界 (>40 s 被杀); `cli_unbounded` `cli_v4` `cli_noleft` → 34b (cli-dash-run) 红, `kv_unbounded` → 34b (kv-upper-run) 红, `val_quadratic` → 34a 34b 红; (i3) 五档 1.16-1.89 对上界 2.5。 |
| **F** `e2459206` | tl/M1, cr/M2 (`8fbbee80`) | **closed** | credit 取默认 (不属 tight); 我的 47 命令对照表与基线 docker / kubectl 行的 credit 一致; `env_tight` → 22br 0/44、22bs 0/22 红; 22bo 22 个成员在目标 yes。 |
| **M** `eb350937` | qa/M2 | **closed** | 18j / 18k 各 32 个独立运行目标 yes; `readface16` → 各 16/32 红; `readface_check.py` 32 路径各只命中一个基线备选 (0 偏差)。 |

R4 minor: 我抽核的均已落地 (23j / 25h / 19ai / 32e、W1 理由重写、版本 / 审计叙事清除 (正文无 `v3` / `R3` / `本版` 等残留)、旧时档数字清除、26g 13 个标记词、`secret-guard.sh:8` 并入 28o、22av / 22bk 清单、`COMMIT_FOOTER_GUIDE.md:199-202` 引用)。**我认为仍未处置的 minor**: `984b1c3d` (FORGEJO__ 覆写) 只落了一半 — 已知限制与 10m 在场, 但「并入 7.8 / 7.9」悬空 (= 本轮 m2)。

## 对执笔人自报薄弱点与请裁项的表态

执笔报告 §5 (自报薄弱点):
1. 34c 是唯一带比值的探针行: **可接受**。我的全量目标运行 34c yes; (f-hit) 比值 2.01 / 1.97 对上界 3.5 余量约 1.7 倍。注意绝对耗时, 见风险 1。
2. 19af 的零分歧只对有限形态表成立: **可接受**。表有鉴别力 (旧设计 50/73、52/73), 我的独立种子随机差分 500 条 0 分歧; 条目含 shell 元字符时前提不成立已写进已知限制。
3. 64 / 40 上界无数据支撑: **可接受**。我实测线性论据成立, 覆盖代价已由 10n / 10o 成文。
4. W1 的 NUL 前提无端到端样本: **可接受, 且前提比执笔认为的更有支撑** — 见实跑核验第 3 项 (Bash 与 Read 都保留 NUL)。
5. 耗时回升与 (i3) 上界 2.5 是自作主张: **可接受**。(i3) 实测 1.16-1.89 (最紧的 (i3-d) 1.89, 距 2.5 约 24%), 坏实现 3.4 倍起, 仍可区分。
6. 回归覆盖靠重跑旧坏实现、7 个旧变体与 29 个 `drop_extreader_*` 移出: **可接受**; 替代者在新设计下确实转红 (`ext_v4stage:*` → 19af)。
7. proposal 增长约 30 KB: **可接受, 附注**: 本轮两条 major 都出在最密的 SC-22 文字与耦合清单; 体量使逐字审阅更难, 我的审阅是抽样加坏实现驱动, 非逐行通读。
8. 研究笔记与已推送分支 (km/m6): **属 owner**; Spec 侧的去量化与 7.20 登记合格, 主控「暂停推 GitHub」属 AI 自作主张, 请 owner 复议 (主控已列)。
9. 时档数字是单次主机上的测量: **可接受** (判据是比值与活性断言)。

执笔报告 §6 (请裁项):
1. 披露范围 (7.20): 产品级, 不由我裁; Spec 侧登记合格。补充一点供 owner 参考: W8 / W10 / W11 的「已知限制」段本身就是旁路形态目录 (不只 7.1 / 7.2), 选项 A 的描述「只写类别与证据位置」没有覆盖它们。
2. W9 条目规则 (含 ASCII 字母数字或任一非 ASCII 字节; 剥 BOM): **同意**, 19ad / 19ae / 19ah / 19ai 各有行且坏实现转红。
3. 簇 F 的 credit 取舍 (默认): **同意**, 我的对照表证明与基线 docker / kubectl 行一致; 备选 B 会把基线放行的日常核对改拦。
4. W2 的 64 / 40: **同意**。
5. W14 时档参数 ((i3) 2.5、(i3-b/c) 取 60 KB / 100 KB、`--judge`): **同意**; `--judge` 回应了我 R4 的风险 2, 我复跑通过。
6. SC-34 口径 (每进程 4 s CPU 上限、34c 比值 3.5): **同意, 附注**: 判据对机器快慢敏感, 见风险 4。
7. 采纳席位备注两条 (Layer 2 一句、验证范围一句): **同意**。
8. 未采纳项: (1) post-ship 腿不加 NUL 腿 — **不完全同意**: 既然 Bash / Read 都把 NUL 带进 tool_result, 惰性 NUL 腿 (合成值、不触真实存储) 可行, 建议作为 1.12 的可选一腿, 不阻塞; (2)(3) **同意**。
9. Rule #10 自作主张清单: **可接受**。

## 风险 / 疑问 (不计入 finding)

1. **钩子超时是墙钟, 时档判据是 CPU 比**: 我的 `timing.py` 在负载 15-20 的主机上, 4 KB 单行命令的基线 CPU 已 1.28-1.96 s (墙钟 2.7-5.3 s), (f-hit) 目标 CPU 2.57-3.87 s、墙钟 5.7-9.0 s, 越过 5 s 钩子超时 (超时即放行, 7.1)。Spec 的墙钟兜底是 20 s (超时的 4 倍)。另: 基线对良性单行命令 2 KB / 8 KB / 16 KB 已是 0.45 / 3.9 / 13.7 s CPU (目标比值 1.07 / 0.99 / 1.01), 即基线在约 9 KB 以上就越过超时 — 既有缺口 (7.1 范围), 非本 Spec 引入; 但「扩展命中路径约 2 倍」会把这条线再前移。
2. **探针退出码不反映红行**: `main()` 只在 `WPA_REQUIRE_ALL` 且有缺腿时 exit 3, 行红时仍 exit 0 (`baseline_probe.py:2510` 起)。Tasks 1.10 要求读「目标形态行」, 所以不构成缺陷; 但有人把探针接进 `&&` 链会假绿。建议末尾 `exit 1 if not target_shape` (一行)。
3. **慢主机上坏实现使探针崩溃而非记红**: `ext_perocc_judge` 在我的主机上令 34c 的 `subprocess.run(timeout=300)` 抛 `TimeoutExpired`, 整个探针以 traceback 退出 (rc 1) 而不是记该行为 no。仍是「未通过」, 只是丢了其余行的诊断。
4. **SC-34 的 4 s CPU 上限随机器快慢移动**: `kv_unbounded` 在 300 KB 上我的主机约 13 s (余量 3 倍); 执笔记 `cli_noleft` 在其主机 6.1 s, 余量只 1.5 倍 — 快 1.5 倍的机器上该形态不再红。
5. **SC-8 腿对主机负载敏感**: 基线本身在负载 19 的主机上 (e) 档 123.1 ms 超 100 ms 天花板而红 (见 M2)。B.1 记录 SC-30 基线时应同时记 loadavg, 在空闲主机复跑。
6. **`# guard:ack:` 逃生口对新增 Bash 拦截族没有行钉住** (R4 风险 4 未处置): 我手测八族 (`ps aux`、`pgrep -af`、`cat /etc/forgejo/app.ini`、变量间接、扩展条目、`sh -c 'printenv'`、`docker top`、`cat /proc/$$/environ`) 带 `# guard:ack: <理由>` 都放行 (无 ack 都 exit 2), 行为符合设计; 只是日后把扩展 / 第二遍提到 ack 之前的实现不会被发现。
7. **`app.ini` 的 29 读取器表比 `.env` 族 R3-C-3 的表窄**: 我实测 `expand` / `unexpand` / `shuf` / `split` / `csplit` 读 `app.ini` 放行、读 dotenv 文件被拦; 17d 只点名 `bat` 一例。低风险, 可在 17d 成文。
8. **发版 / 工作区**: 仓根有未跟踪的 `gawk_1%3a5.2.1-2_amd64.deb` (R4 遗留), 提交时勿 `git add -A`。
9. **新 tag 排在 `bcrypt-hash` 之后** (`order_end`) 全部 SC-1..13 共 161 行 0 行红: 行为差别只在「JSON 值是 crypt 哈希形」时报哪个 tag 名, 7i 两者都接受, 是等价变异; 但 W2 文字写了「bcrypt-hash 之前」。
10. **BSD / macOS / Windows Git-Bash 语义仍未验证** (`grep -b -o -F -i -f` 的偏移语义、`sed -E`、`pgrep -fl`、MINGW64 下的 Read 扫描成本); Spec 已把「未验证」写进关单披露。
11. **post-ship 腿的执行条件** 与 `.aria/probes/plugin-cache-currency.py` 的真实输出一致 (R4 已核, 本轮未改)。

## Verdict

**PASS_WITH_WARNINGS** — counts: **0C/2M/3m**。

Vote: **REVISE** (有 major)。

## 是否足以进入 A.2

**足以 (有条件)**: R4 的 critical 与全部 major 六簇我独立复核关闭, 目标 / 基线两态在我的全量复跑里没有一行说谎, 两条新 major 都是「补行 / 补一条耦合清单项」(M1 加三个 SC-22 枚举行加 W11 一句语义; M2 在 W14 加一条耦合加一行不需要 git 的活性探针行), 无设计取舍。建议把这五条 (M1 / M2 / m1 / m2 / m3) 作为进入 A.2 之前的一次小修合入, 并把它们同时写进 detailed-tasks 的「测试先行」(Tasks 1.2) 与对抗 review 清单 (1.8); 以我的证据看, 不需要再开第 6 轮全席审计 —— 边际产出已经降到「补行」级, 而 1.8 的非作者对抗 review 与 post_planning 审计正是为这类自然窄化设的。这是 AI 的建议; 降级策略三选一 (接受当前结论 / 增加轮次 / 降级为单轮) 是 owner 的裁定。