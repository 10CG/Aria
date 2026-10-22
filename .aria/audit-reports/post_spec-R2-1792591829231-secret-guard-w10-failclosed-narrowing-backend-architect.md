---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-21T16:24:27.041Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — backend-architect 席（实现者试派生）

## 审计结论

### 0. 方法与范围

本席的做法是「照 v2 实现一遍，再用实测去对规格」。

- **试派生补丁**：把 v1.76.1 的 `hooks/secret-guard.sh`（`59e333c`）复制出来，严格按 What Changes 1–6 落地。helper 两个函数和 `longline` 文案正文直接从 proposal 里按行抽出（`diff` 确认与 `traffic/deadline-helper.sh` 逐字相同）。
  - 补丁脚本：每处替换都做「恰好匹配 1 次」断言，15 处替换一次全部落地，没有一处因为行号或代码对不上而失败。
  - `bash -n` 在 5.2.15 与真 3.2.57 下都通过。
  - 路径见文末「产物」。
- **实测**：e2e 用 `jq -nc --arg c "$cmd" '{tool_name:"Bash",tool_input:{command:$c}}' | <bash> <hook>`；直调用「source hook + 按锚点抽出闸门以下的 `risky_patterns` / `_sg_redact_echo` / `_sg_judge_one`」。命令一律 `taskset -c 0,1 nice -n 19`，凭据形路径在运行时拼装。
- **既有用例**：从套件抽出 W10 块（`:2493–2695`）和 `wpa_*` 助手，拼成迷你套件，基线 19/19 绿；再对补丁副本跑，结果见 F-18。
- **机器负载**：本机同时有别的席位在跑，同一条命令的墙钟抖动可达 2–3 倍（W4 的 bash 3.2 单次 regexec 存档 3.18 s，我这次重跑是 10.48 s）。下文所有秒数都带这个底噪。

**结论先行**：没有发现 Critical。硬截止机制本身在真实判定下行为正确（准时、文案干净、不占管道、`set -u` 下无未绑定变量、返回码映射符合规格）。主要问题集中在两处：**测试可抖动 / 不可实现的 SC 形状**，以及**硬截止的「硬」依赖一个规格没写、也没有任何 SC 守住的不变量**。

### 1. Findings

每条标注：针对 **[v2 新文本]** 还是 **[v1 沿用]**。

---

#### F-01　时延敏感：断言「完整判定完成」的 SC 在 3 s 硬截止下对负载敏感

- type: risk　severity: **Major**　category: testing
- scope: Success Criteria（SC-N4、N4d、N3 在 8192 处、N12、N1c、N16）；What Changes 2「截止时长」
- 针对：**[v2 新文本]**
- 摘要：硬截止从 hook 启动算起、含首遍，上限固定 3 s，环境变量与 helper 都只能缩短不能延长；一批 SC 要求「判定在截止内跑完并给出 exit 0 / 指定文案」，空闲时只有约 1.5–2× 的余量，机器稍慢就从 exit 0 翻成时间文案，红灯与代码对错无关。
- 证据：
  - SC-N4 形状（`(true); v=ab; echo $v` + 恰 8192 字符的一行 + `cat <app.ini 路径> | wc -l`）：空闲时 5 次里 4 次 1.83–1.85 s、1 次 2.64 s，全部 exit 0。
  - 同一条命令，在同一核上放一个 `while :; do :; done`（约等于 2 倍慢机）：5/5 次变成 `time` 文案、exit 2，墙钟 2.90–3.16 s。
  - 事后用 `n4load.sh` 在宿主机 1 分钟负载约 7（4 核，别的席位在跑）时重跑同一条命令：不加压的 5 次与加压的 5 次共 10/10 都是 `time`，墙钟 2.5–22 s。这一组不是受控实验，只说明该 SC 的结果取决于宿主机当时的负载，而不取决于代码。
  - 总耗时里首遍的 credit 与第二遍的 credit 各约 0.9 s；SC-N1c（24 KB 良性）在 bash 3.2、本机较空闲时 1.35–1.45 s，2 倍负载就贴近 3 s 的线。
  - 脚本：`.../backend-architect/n4load.sh`（空闲 5 次 + 单核放一个空转进程 5 次）、`lib.sh`（`hk`）。
- 建议改法：
  1. 在规格里把 SC 分成两类：「判定结果类」（要求跑完）与「护栏类」（允许时间文案）。前者的形状要选「判定 ≤ 0.3 s」，后者才用大判定。
  2. 给直调测试一个**非环境变量**的缩放口，例如把 helper 里的字面量 3 改成 `_SGV_DMAX=3`（常量，与其他 `_SGV_*` 同处定义），直调时可以设大；e2e 保持不可延长，这样「环境变量只能调短」的安全性质不受影响。
  3. SC-N4 一类的断言改为「exit 0，或时间文案且判定耗时超过 X」之类的二值判据，或者放到有 CPU 保证的验收机上（SC-N16 也是同理）。

---

#### F-02　硬截止的「硬」依赖一个未写明的不变量：判定路径上不得有比判定本身活得更久的外部子进程

- type: risk　severity: **Major**　category: architecture
- scope: What Changes 2「参考实现」与「要点」；helper 头注释
- 针对：**[v2 新文本]**
- 摘要：计时作业只 `kill -KILL "$jp"`，杀的是判定子 shell；若判定留下了仍持有捕获管道的后代进程，命令替换会等到它退出才返回，截止就不再准时。规格只论证了「计时作业的 sleep 不占管道」，没有论证（也没有任何 SC 守住）「判定自己的子进程」。
- 证据（直调，`/bin/bash` 5.2.15 与 3.2.57 结果相同）：
  - 假判定 `_sg_vx_big_judge() { sleep 6; return 0; }`，`_SG_TIME_BUDGET=3`、`_SG_P0=$SECONDS`：`_sg_vx_big` 返回 3（方向对），但**墙钟 6.00 s**，不是 3 s。判定留一个后台子进程持有 stderr 的变体同理（返回 `rc=3`，且要等子进程退出命令替换才返回；该变体未单独计时）。
  - 真实判定今天只有两类毫秒级后代：`_sg_emit_blocked` 里的 `cat` 与 `_sg_redact_echo` 的 `sed`，所以 W4/W6 与我的 e2e（杀掉后 2.3–3.6 s 内返回）都成立。
  - 一旦以后有人在 `_sg_judge_one` / `_sg_compute_credit` 链上加一个 `grep` / `awk` / `jq`（这些恰好是「更快的正则」的常见替换），硬截止悄悄变软，而所有 SC-N5 / N9 在小输入下仍然是绿的。
  - 脚本：`.../backend-architect/rcmap.sh`（「judge leaves a child still holding stderr」一行）、`negclock.sh` 第一行。
- 建议改法：
  1. 在 helper 头注释和「要点」里写明不变量：「判定闭包内不得出现可长时间运行的外部命令；`cat` / `sed`（仅块路径、仅回显 ≤ 200 字符或段）除外」。
  2. 新增一条结构类 SC（仿 SC-30b 的闭包扫描）：对 `_sg_vx_big_judge` 的调用闭包列出所有外部命令，断言集合等于 `{cat, sed}`。
  3. 再加一条行为类 SC：直调，假判定 `sleep 6` 且预算 3，断言返回码与墙钟（< 3.5 s）。如果它红，说明要换实现，例如让判定把输出写到临时文件而不是管道，或者 `set -m` 后按进程组杀。

---

#### F-03　SC-N9 / SC-N5c / SC-N4e 的对抗形状：关键约束没写，第三种形状不满足自己的前提

- type: issue　severity: **Major**　category: testing
- scope: Success Criteria（SC-N9、SC-N5c、SC-N4e）；Tasks TASK-001
- 针对：**[v2 新文本]**
- 摘要：规格把形状留给 TASK-001「选定并实测」，但没有写出决定判定快慢的三个约束，按字面构造会得到「看起来对抗、实际很快」的输入，使 SC-N5c（期望时间文案）在正确实现上变红；第三种形状还与自己的「首遍 < 1 s」前提矛盾。
- 证据（bash 5.2，新版 hook，e2e）：
  1. **字面量次序**：k 行 8000 字符 token 加经变量的读取，若 `f=<app.ini 路径>` 写在 token 之前（最自然的写法），`tight` 探测的 `$_SG_SRVCFG` 一开始就命中，k=3/5/8 分别在 0.39 / 0.58 / 0.86 s 以普通 finding 结束；把路径字面量放到 token 之后，才得到 k=3 finding 2.73 s、k=5 时间文案 3.34 s、k=8 时间文案 3.49 s（3.2：2.60 / 2.98 / 2.53 s，全是时间文案）。
  2. **读取路径**：读取若命中 `_SG_SRVCFG` / `_SG_CLAUDE_CFG`，`tight=1` 后不再跑 `_SG_PROCTAB_ALL`，watch 一族的 credit 代价被短路。
  3. **第三种形状（1500 行 `watch watch watch watch`）违反「首遍 < 1 s」**：基线首遍单独就是 4.38 s（5.2）/ 4.94 s（3.2）。规则级代价随行数平方增长：N=400 / 800 / 1200 / 1500 行只匹配规则分别 0.39 / 1.36 / 2.79 / 4.87 s，加上读取后 credit 只多出 0.2–1.2 s。也就是这一族里**不存在**「首遍 < 1 s、判定 > 3 s」的 N；它只能证明首遍（#228）很贵。
  4. 因此「bash 3.2 下墙钟 < 5 s」对这一形状不可满足：基线 4.94 s，新版 5.15 s，全部是首遍时间。
  5. SC-N4e 的可行性我验证了：单行 24 KB + 路径字面量在 token 之后，`longline` 0.27 s 拦下；4 行 × 6000 字符分行（走 credit）2.55 s，所以「含 credit > 3 s」需要更大的数字，但形状族成立。
- 建议改法：
  - 在 SC-N9 里写死三个约束：路径字面量在长 token 之后；读取路径不得命中 `_SG_SRVCFG` / `_SG_CLAUDE_CFG`（用 `.aws/credentials` 一类）；形状的「首遍」实测值要写进用例注释并断言 < 1 s。
  - 删掉第三种 watch 形状，或把它改成「首遍 + 判定」合计的 SC，并明说它属于 #228 的范围。
  - SC-N5c 直接引用「token-after-path 的 k=5」，不要再绕 SC-N9。

---

#### F-04　SC-N12 后半「套件 20 条 BLOCK 用例各自包进超长行 → 全部 longline」不可实现且有抖动

- type: issue　severity: **Major**　category: testing
- scope: Success Criteria（SC-N12）
- 针对：**[v2 新文本]**
- 摘要：只有变量形的 BLOCK 用例（W10 一族）才可能走到 C；字面读取形在首遍就以普通 finding 拦下，永远不会出 `longline`。「包进超长行」的做法也没写，不同做法落在不同路径，还有一种会因首遍变慢而抖成时间文案。
- 证据（新版 hook，bash 5.2）：
  - 取套件里 19 条变量形 BLOCK（21a–21h、21j×9、21x、21x2，见 `n12cmds.sh`），三种包法：
    - 整串包（前缀 `(true); echo <8300 个 x>; `）：19/19 `longline`，每条 0.13–0.17 s。
    - 后缀包（命令后拼 8300 字符，分段模式、读取段自己变长）：16 条 `longline`，**3 条（#3、#6、#9）是 `time`**，墙钟 2.09–2.70 s；推测原因（未做分段插桩）：分段模式首遍对 8 KB 字符逐个扫描（空跑一条 `echo` + 8000 字符的首遍约 1.9–2.0 s），`SECONDS` 进位后 `left` 只剩 1 s 或 0 s。
    - 前缀包（分段模式、独立的长段）：读取段仍很短，不进大副本路径（该变体仅按构造推理，未单独跑完）。
  - 套件里绝大多数 BLOCK 用例是字面读取（`cat .env` 一类），它们在首遍被拦，文案是普通 finding。
  - 前半（四种 W12 单键形在 > 8192 的行里不误拦、整表形仍拦）实测成立：四种单键形 exit 0，`os.environ` 整表两种仍 finding，基线是 oversize。
- 建议改法：写明用例清单（这 19 条）、包法（整串包，必要时前缀 `(true);`），断言口径为「exit 2 且文案是 longline」；明确字面读取形不适用。

---

#### F-05　`left` 公式没有对 `SECONDS - _SG_P0` 取非负；读数为负时截止被拉长

- type: risk　severity: Minor　category: implementation
- scope: What Changes 2「截止时长」与 helper 第一行
- 针对：**[v2 新文本]**
- 摘要：规格的「3 s + 1 s」上界假定 `SECONDS` 单调。`left` 没有夹到 `min(预算, 3)` 以内；墙钟回拨（NTP 步进、虚机恢复）或测试里把 `_SG_P0` 设在未来，都会让截止超过 3 s，进而超过 5 s。
- 证据：直调，`_SG_P0=$((SECONDS+10))`（即 `SECONDS-_SG_P0=-10`）时 `left=13`；一个跑 6 s 的假判定被放行，`rc=0`，墙钟 6.00 s（5.2 与 3.2 一致）。脚本 `negclock.sh`。触发条件（墙钟回拨）罕见，我没有在本机观察到时钟步进（`uptime` 与 `date` 的增量一致），所以只是加固建议。
- 建议改法：helper 里先 `e=$(( SECONDS - _SG_P0 )); (( e < 0 )) && e=0`，再 `left=$(( cap - e ))`；加一条直调 SC（`_SG_P0` 在未来 → 返回码仍按 3 s 封顶）。

---

#### F-06　`lim` 的措辞与声明：「长出 8192 以上」与代码、SC 的边界相反；`lim` 是否 `local` 未写

- type: issue　severity: Minor　category: documentation
- scope: What Changes 1
- 针对：**[v2 新文本]**
- 摘要：正文「任一中间副本比原串长出 8192 以上，就停下并返回 2」按中文字面是「≥ 8192」，而代码 `> lim`、SC-N3（8192 进判定、8193 拦）、文案「grows by more than」都是「> 8192」。另外「在函数入口计算一次 `lim=...`」没有说 `local`，不声明会泄漏成全局。
- 证据：我按代码（`> lim`）实现后，SC-N3 的 8192 / 8193 两侧在 `$NAME` 与 `${NAME}` 两种写法下、整串 e2e 与分段直调下，在 5.2 与 3.2 上全部符合规格（共 16 组，见对照表）；按字面「≥」实现会在 8192 处翻边。
- 建议改法：把「以上」改成「超过」，并在 `local` 行里写出 `lim`。

---

#### F-07　SC-N15 / 9 处注释清单：行号错一格、一处是空操作、漏了 `_sg_judge_one` 自己的契约注释、短语表缺失

- type: issue　severity: Minor　category: documentation
- scope: Impact「注释同步」；SC-N15
- 针对：**[v2 新文本]**
- 摘要：
  1. 第 1 处 `:86–94` 应为 `:87–95`（`:86` 是上一条的尾行，`:95` 才是 W10 条的收尾行 `calls pass; the output side is left to secret-scan.sh.`）。
  2. 第 4 处（`:630–631`，`_sg_vx_collect` 契约）「只删去与死代码有关的措辞（如有）」——这两行里没有任何此类措辞，改动为空；SC-N15 对它的断言「退役短语不在、新关键词在」两头都是空的，恒绿。
  3. 封闭清单漏了 `_sg_judge_one` 自己的头注释（`:1492–1496`，现写 `$1 = string ... $2 = mode`），而它的签名在 What 3 里变成三参。
  4. SC-N15 的「退役短语」「新关键词」清单没有写进规格，只给了两个例子；由执笔人自拟、自写 grep，正是项目记忆里「迎合检查器」的假绿形状。
  5. 7 个预计会变的用例的**用例名与注释**也含旧语义（例如 21ab 的名字「the copy is not judged」），清单只列了三个块头。
- 证据：`sed -n '84,97p'` 与 `sed -n '574,600p'` 对 `secret-guard.sh`；`secret-guard.test.sh:2552`、`:2597–2599`、`:2628–2630`。
- 建议改法：改行号；第 4 处从清单中删去，或改成「补写 `_SG_P0`、`status 3` 说明」；清单加上 `_sg_judge_one` 头注释；把每处的退役短语与新关键词逐条写进 SC-N15。

---

#### F-08　SC-N8 的 TMAX 例：按字面算不到 65536，换一种读法则成本高到不可用

- type: issue　severity: Minor　category: testing
- scope: Success Criteria（SC-N8）
- 针对：**[v2 新文本]**
- 摘要：「5 段，每段约 8 KB、各自增长约 6 KB」：若 8 KB 指副本，5 × 8 = 40 KB < 65536，TMAX 永远不触发；若指原文，副本约 14 KB、合计 70 KB 才过线，但分段模式首遍对原文逐字符扫描，5 段 8 KB 的首遍实测极慢。另外这一行标「直调（改写 21an）」，而 TMAX 的比较在 `_sg_vx_pass`，不在 `_sg_vx_apply`，21an 的探针碰不到它。
- 证据：
  - 原文约 8 KB / 段的形状：基线 bash 5.2，3 段（26 KB，单 token 填充）首遍就要 17.55 s；5 段（42 KB，短词填充）在 40 s 处被我杀掉。
  - 可用的便宜形状：`p` 为 1024 字符，每段 ` echo $p $p $p $p $p $p $p $p`（8 个引用，副本 8205、增长约 8176，原文极短）：k=7 段新版 exit 0（0.49 s；3.2 为 1.78 s），k=8 段新版按 `wpa_L_total` 拦，基线任何 k 都按 `wpa_L_seg` 拦；k=9 同 k=8。
- 建议改法：把 TMAX 例换成「≥ 8 段、每段 8 个引用 × 1 KB 值」，并标为对 `_sg_vx_pass` 的直调或 e2e。

---

#### F-09　SC-N1 / N2 / N3 没有规定行结构；`longline` 与普通 finding 在既有助手里分不开

- type: issue　severity: Minor　category: testing
- scope: Success Criteria（SC-N1、N2、N3）；「预计会变的既有用例」表
- 针对：**[v2 新文本]**，加一条 **[v1 沿用]** 的助手特性
- 摘要：SC-N2 要求「finding 模板，逐字」，但 SC-N1 的 9.7 KB 形状是单行还是多行没说。单行时副本最长行 > 8192，走 `longline`（`Matched pattern:` 也在，但首行是另一句）；多行才是普通 finding 模板。SC-N3 在 8192 处同理。
- 证据（5.2 / 3.2 一致）：SC-N2 单行形 → `longline`；多行形（三行各 3000）→ 普通 finding。SC-N3 整串 8192 处：单行 `longline`，多行 `finding`。「预计会变」表里 21ab 第 1 条、21ac 第 3 条、21al 第 2 条、21ao 第 2 条都写「finding」，实测全是 `longline`（都是单行副本）。21an 还多一处没写：探针 `edge8193` 的期望状态由 2 变为 0（建成的副本 8193 > 8192）。
- 沿用的助手特性：套件的 `wpa_x_finding` 只检查「含 `reads a secret-bearing source`、不含 `too large to scan`」，而 `longline` 首行恰含前一个短语，所以它分不出 `longline` 与普通 finding；上述四个既有用例即使 C 路径误写成「所有大副本都不算 credit」也保持绿。能区分的只有 SC-N4 / N4d。
- 建议改法：SC-N1 写明「多行，每行 ≤ 8000」或「单行」，SC-N2 / N3 相应写文案；预计表把四条改成 `longline`，并补上 `edge8193`；`longline` 另给一个专用断言助手（匹配 `in a line longer than`）。

---

#### F-10　SC-N11：比值判据在毫秒级抖动；直调需要桩掉 `_sg_judge_one`

- type: issue　severity: Minor　category: testing
- scope: Success Criteria（SC-N11）
- 针对：**[v2 新文本]**
- 摘要：「4N 与 N 的耗时比 < 8」所测的循环只有 10–150 ms，计时噪声同量级；且 `_sg_vx_big_judge` 末尾会调用闸门以下的 `_sg_judge_one`，直调时要桩掉，规格没写。
- 证据（桩判定后，5.2）：单行 60 KB 0.05 s、240 KB 0.01 s；4000 行 0.06 s、16000 行 0.15 s（比 2.5）、64000 行 0.60 s；3.2 对应 0.05 / 0.16 / 0.09 / 0.33 / 1.56 s。线性成立（循环确为线性），但单行那组比值会因噪声乱跳。
- 建议改法：改成绝对上限（如 64000 行 < 2 s）加「16N 不超过 N 的 40 倍」之类的宽松比；写明要桩掉 `_sg_judge_one`。

---

#### F-11　SC-N14：`en_US.UTF-8` 不一定存在，缺失时用例空转

- type: risk　severity: Minor　category: testing
- scope: Success Criteria（SC-N14）
- 针对：**[v2 新文本]**
- 摘要：容器常无 `en_US.UTF-8`，bash 静默退回 C，两次结果相同，「两种结果」就测不出口径。套件本身已有 `C.UTF-8` 的惯例（`wpa_lang_only`）。
- 证据：本机 `locale -a` 有 `C.utf8`、`en_US.utf8`；用多字节行（两行各 5000 个汉字，30066 字节 / 10066 字符）实测：UTF-8 下 exit 0（credit 生效），C 下 `longline`，5.2 与 3.2 一致，符合规格。
- 建议改法：用 `C.UTF-8`，并在用例里先断言 `locale charmap` 为 UTF-8，否则 skip。

---

#### F-12　扩展生效的项目里，大副本判定是纯开销

- type: decision　severity: Minor　category: architecture
- scope: What Changes 4；Decision 7
- 针对：**[v2 新文本]**
- 摘要：扩展门保持绝对尺寸门，所以有扩展条目时任何副本 > 8192 的命令最终都以 `wpa_L_ext` 拦下。但 W10 已经先把大副本放进 `_sg_vx_big` 判完（最多约 3–4 s），再轮到扩展门，这段判定对最终结论没有任何影响，只增加耗时，并且之后还要再跑一遍扩展的 `_sg_core_eval`。
- 证据：SC-N6 的逐分支等价我核对成立（整串 8193 + 扩展：基线 `wpa_L_whole` → 新版 `wpa_L_ext`；无扩展：基线 oversize → 新版 exit 0；段模式 21ap 形不变）。我试图构造「新版超过 5 s、基线不超」的输入（扩展生效、原文约 7–13 KB、分段模式），**没有复现**：原文一大，首遍就吃掉 `SECONDS`，`left` 立刻 ≤ 0，新版很快返回时间文案，墙钟与基线同量级。因此这条只是设计冗余，不是已证实的新超时。
- 建议改法：先查扩展条目是否存在（便宜），存在则在 `_sg_vx_big` 之前直接走扩展的 oversize 文案。

---

#### F-13　计时作业 fork 失败不在「失败方向都是拦」的清单里

- type: risk　severity: Minor　category: implementation
- scope: What Changes 2「要点」
- 针对：**[v2 新文本]**
- 摘要：规格列了 `sleep` 不可用、拿不到数字状态、判定内部出错三种失败。没有列「计时子 shell 本身 fork 失败」：此时 `tp=$!` 沿用判定的 PID，计时作业不存在，`wait` 一直等到判定自然结束，截止消失。
- 证据：**未复现**（没有稳定办法让第二次 fork 失败而第一次成功）。判定本身 fork 失败的方向按推理是对的（未实测）：新开的命令替换里 `$!` 未设置，`set -u` 使子 shell 以状态 1 结束，`out` 为空，走 `[[ "$rc" =~ ^[0-9]+$ ]] || return 3`。
- 建议改法：`tp=$!` 之后检查 `kill -0 "$tp"`，失败则立即杀判定并返回 3；规格里补一条。

---

#### F-14　孤儿 `sleep`：数量上界与存活时长

- type: risk　severity: Minor　category: implementation
- scope: What Changes 2「要点」
- 针对：**[v2 新文本]**（规格已声明「孤儿」，未给数量上界）
- 摘要：每次判定提前结束就留一个 `sleep`，存活到截止点；分段模式下一条命令最多可有 7–8 个大副本（TMAX 65536 / 8192），即最多 7–8 个同时存活。对管道无影响。
- 证据：`| cat` 包一层并计时：整串良性大副本 hook|cat 管道 0.32 s（5.2）/ 0.79 s（3.2）结束，而孤儿 `sleep` 分别活到 2.24 s / 3.35 s；被杀的情形 hook|cat 管道在杀死时刻（3.35 s / 3.81 s）结束，没有额外等待。3 个良性大段（分段模式）同时存活的孤儿 `sleep` 数量实测为 3（5.2）。进程树按会话 id 查，脚本 `orphan.sh`。
- 建议改法：规格里写一句「至多每个大副本一个，存活不超过 left 秒」；若在意，可让计时作业在判定结束时由父进程 `kill` 其子 `sleep`（`pkill -P`）。

---

#### F-15　措辞与小遗漏（合并）

- type: issue　severity: Minor　category: documentation
- scope: What Changes 2/5；Why
- 针对：**[v2 新文本]**
- 摘要：
  1. What 5 说 `longline` 正文「含两处展开」，实际是三处：`${_SGV_LMAX}`、`$pat`、`$(_sg_redact_echo ...)`。
  2. `_SGV_LMAX` 的定义位置没写（对照 `_SGV_GMAX`「与其他 `_SGV_*` 定义在一处」）。
  3. `_SG_P0` 声明在 `:178` 之后，而说明它的注释在 `:597–607`，相隔约 400 行；定义点本身没有注释要求。
  4. Why 说 oversize 模板「开头是 Nothing was matched」，实际首行是 `command too large to scan ... Limit hit:`，`Nothing was matched` 在第二段。
  5. `_sg_vx_collect` 契约（`:630–631`）漏写既有的状态 3（超时），这条是 v1 沿用的缺口，借本次注释同步顺手补上最划算。
- 证据：`sed -n '851,868p'`（基线）；proposal 正文。
- 建议改法：逐条改。

---

#### F-16　证据与复现：W4 / W5 / W6 可凭仓内文件复跑；SC-N16b 的 `traffic/standin.sh` 尚不存在

- type: issue　severity: Minor　category: documentation
- scope: 「证据与复现」；SC-N16 / N16b
- 针对：**[v2 新文本]**
- 摘要：W5 用 `traffic/deadline-estimate.sh` 重生成，与存档（去掉头行）逐字一致；W6 在两种 bash 上重生成，结论一致（计时有噪声）；W4 重生成一致，仅 bash 3.2 的「单次 regexec」存档值 3.18 s 对我这次的 10.48 s（宿主机负载）。W0 清单行数为 2412，与规格一致。W1–W3 与 SC-N16 需要仓外的 `TRAFFIC_DIR`，规格已声明。SC-N16b 引用的 `traffic/standin.sh` 与「入库的期望结果」目前仓里没有（前向引用）。
- 证据：`ls .aria/notes/2026-10-21-.../traffic/`；`bash traffic/deadline-estimate.sh | diff - <(tail -n +2 evidence/W5-deadline.txt)`。
- 建议改法：TASK-001 或 TASK-004 里把 `standin.sh` 与期望结果列为交付物，进「完成判据」。

---

#### F-17　bash 3.2 在本机的绝对速度远低于「×4」估算

- type: risk　severity: Minor　category: testing
- scope: 「证据与复现」口径；SC-N17
- 针对：**[v1 沿用]**（首遍与扩展的代价本就如此），但 **[v2 新文本]** 的 SC-N17「全部 SC-N 在真 bash 3.2.57 下实跑」会撞上
- 摘要：基线在 bash 3.2 下，4.5 KB 三段命令的首遍就 5.5 s；扩展生效、8 KB 的段模式命令基线 10–21 s。SC-N6、N6b、N8 在 3.2 上因此每次要几十秒，且结果与本改动无关。
- 证据：同上；基线与新版在该形状上同量级（噪声很大）。
- 建议改法：SC-N17 对 3.2 注明「带扩展的 SC 允许慢」，或把这些用例的形状缩到首遍 < 1 s。

---

#### F-18　（非缺陷，核对结果）「预计会变的既有用例」表的**成员**预测完全正确

- type: decision（核对）　severity: 无　category: testing
- scope: 「预计会变的既有用例」
- 针对：**[v2 新文本]**
- 结果：迷你套件（W10 块 19 个用例）基线 19/19；补丁副本 12/19，失败的**恰好是** 21ab、21ac、21ag、21aj、21al、21an、21ao 七个，预计不变的 21aa、21ad、21ae、21af、21ah、21ai、21ak、21am、21ap 以及 21z、21v、21w 全绿。
  - 逐条：21ab 第 2、3 条 exit 0 ✓；21ag、21aj 只换文案（`grows by more than 8192`）✓；21ac 第 3 条、21al 第 2 条、21ao 第 2 条、21ab 第 1 条是 judged-and-blocked，文案是 `longline`（见 F-09）。
  - SC-30b（调用闭包都在闸门之上）在补丁副本上通过：`_sg_vx_big`、`_sg_vx_big_judge`、`_SG_P0`、`_SGV_GMAX`、`_SGV_LMAX` 都被闭包检查覆盖且已定义。

---

### 2. 已核实无误（不再展开）

- **代码事实**：proposal 引用的 40 余个行号，对 `59e333c` 逐个核对，除 F-07 第 1 条外全部正确（含 `:178`、`:594–596`、`:645/:659/:668–669`、`:685/:694`、`:725/:728/:740/:744/:748–750`、`:926`、`:1506–1509`、`:1554–1555`、`:1563`、`:1581`、`:666` 死代码）。`_sg_compute_credit` 里恰有 14 次 `_sg_line_match`；standards 三处计数 822 / 816 与套件头注释 831 / 825 的陈旧关系属实；W10 预算数值确实没有写进 standards / README / CHANGELOG。
- **硬截止在真实判定下的行为**（本席重点）：
  - 退出码：被掐断、判定内部出错、预算为 0，都是 exit 2；时间文案 804 字节，除预算数字与 `Command was` 行外与基线的时间文案逐字相同，没有 `Killed` 作业提示、没有残缺文案。
  - 墙钟：被掐断 10 次随机相位 2.30–3.57 s（5.2）；理论上界约 4.0 s，与规格「3 s + 1 s」一致。预算 1 / 2 / 3 / 4 / 99 → 约 1.3 / 2.3 / 3.4 / 2.3 / 3.4 s，确认 4 与 99 都被封在 3。
  - 管道：`| cat` 下判定提前结束时，管道不被孤儿 `sleep` 占住（F-14）。
  - `set -u`：补丁副本 e2e 与 W10 迷你套件无未绑定变量；判定内部制造未绑定变量 → 状态 1 → 内部错误 exit 2。
  - 返回码映射（`rcmap.sh`，两种 bash 一致）：0 → 0，2 → 2，1 / 7 / 126 / 127 原样上抛，3 → 3，≥ 128 或被信号杀 → 3，无数字状态 → 3，截断文案被丢弃。
  - 故障注入（SC-N10）：在 `_sg_vx_big_judge` 或 `nocredit` 分支注入 `exit 1`、未绑定变量、`return 1` → exit 2（内部错误）；`return 3` → 时间文案；`exit 0` → exit 0（任何 `exit 0` 故障与放行不可区分，与基线同）。
- **两个时钟**：`_SG_P0` 在 e2e 里恒为 0（新进程），环境预设 `SECONDS=100000` / `-5000` / `abc` 都不影响（exit 0）；协作式预算 `_SG_T0` 的各检查点行为不变。套件 source hook 时 `_SG_P0` 陈旧只影响直调的大副本（SC-N5a 已要求显式设置）；既有直调测试里只有 21an 触及这些函数，它不调用 `_sg_vx_big`。
- **扩展门**：逐分支等价，仅有一个角落：中间副本曾超过 8192、终态 ≤ 8192 时，基线 `ar=2`，新版 `ar=0`（按 ≤ 8192 副本正常判定）——属于姿态 A 的自然延伸，未单独申报也无安全影响。
- **nocredit 与 W12**：W12 中和先于规则循环，四种单键形在超长行里不误拦、整表形仍拦（F-04 末条）。
- **放宽面申报**：我没找到未申报且确实读到凭据的反例；唯一补充：整串模式下 credit 是整份副本共享的，多行大脚本里更容易在某处出现 `>/dev/null` 或 `| wc -l`，所以大副本的实际检出率可能低于小命令——这是 BA-F-15 的放大（未量化），建议 CHANGELOG 对此加一句提示。
- **R1 处置到位**：A4（扩展门）、A5（线性 `read` 循环，SC-N11）、A6（C 复用 `_sg_judge_one`，W12 单份）、A8（`_SG_P0` 与封顶，SC-N5a–f）、A12（既有用例逐条预测，成员全对）、A19（`lim` 入口计算，8 次替换上限与两种写法的边界在 8192 / 8193 精确）、A21（口径，SC-N14）均有对应实现且实测成立；A13（9 处）与 A22（证据）见 F-07、F-16。

### 3. SC 期望 vs 实测

「基线」为 v1.76.1 原 hook；「新」为试派生补丁副本。无特别说明时 5.2.15 与真 3.2.57 结果一致。

| SC | 我构造的输入 | 规格期望（新版） | 基线实测 | 新版实测 | 备注 |
|---|---|---|---|---|---|
| N1 | `(true); v=ab; echo` + 300 个 `$v` + 填充，9.7 KB，单行 / 多行 | exit 0 | exit 2，`wpa_L_whole` | **exit 0** | ✓ 3.2 墙钟约 0.6 s |
| N1b | 引用全在第 8193 字符之后，单行 / 多行 | exit 0 | oversize | **exit 0** | ✓ |
| N1c | 24 KB 多行 / 25 KB 单行，增长 < 100 | exit 0 | oversize | **exit 0** | ✓ 3.2 空闲 1.35–1.45 s（F-01） |
| N2 | N1 形状 + 变量值为 app.ini 路径 + `cat $f` | 「finding 模板」 | oversize | 单行 `longline`；多行普通 finding | 均 exit 2、含 `Matched pattern:`；规格未定行结构（F-09） |
| N3 整串 e2e | 增长恰 8192 / 8193；`$NAME` 与 `${NAME}`；单行 / 多行 | 8192 进判定；8193 拦 `grow_whole` | 两侧 oversize | 8192：单行 `longline` / 多行 finding；8193：`the command grows by more than 8192 characters...` | ✓ 8 组全对 |
| N3 分段直调 | 同上，预置 `_SG_SEGS`，调 `_sg_vx_pass` | 同上，`grow_seg` | — | 同上 | ✓ 8 组全对 |
| N4 | 大副本，最长行恰 8192，读取 + `\| wc -l` | exit 0 | oversize | **exit 0**，约 1.85 s | ✓ 但 2 倍负载下 5/5 变 `time`（F-01） |
| N4b | 同上，最长行 8193 | `longline` | oversize | **`longline`** | ✓ |
| N4c | 8193 行但无读取 | exit 0 | oversize | **exit 0** | ✓ |
| N4d | 3 行 × 4000，读取 + `\| wc -l` | exit 0 | oversize | **exit 0**，约 1.56 s | ✓ |
| N4e | 单行 24 KB，读取，路径在 token 之后 | `longline`，< 2 s | oversize | **`longline`**，0.27 s | ✓；「含 credit > 3 s」需更大数字（4×6000 只有 2.55 s） |
| N5a | `_SG_P0=$((SECONDS-100))`，段内副本 8192 / 8193 | 8192 返回 0；8193 时间拦 | — | rc=0；rc=2 + 时间文案 | ✓ |
| N5b | 环境 `SECONDS=100000`（另试 -5000、abc） | exit 0 | oversize | **exit 0** | ✓ |
| N5c | `SECRET_GUARD_TIME_BUDGET_S=1`，k=5 个 8000 字符 token 行，路径字面量放在 token 之后 | 时间文案，< 2.5 s | oversize | **时间文案**，1.32 s（3.2：1.27 s）；对照（默认预算）路径放在 token 之前：finding 0.58 s | 形状不当则红（F-03） |
| N5d | `_SG_TIME_BUDGET=99`、`_SG_P0=$((SECONDS-3))`，良性大副本 | `_sg_vx_big` 返回 3 | — | rc=3（对照 `_SG_P0=$SECONDS` 得 0） | ✓ |
| N5e | `sleep() { return 127; }`，对抗形状 | 返回 3，< 0.5 s | — | rc=3，0.01 s（另试 PATH 无 sleep：同） | ✓ |
| N5f | `_SG_TIME_BUDGET=0` | 返回 3，不 fork | — | rc=3，0.00 s | ✓ |
| N6 | 扩展生效（条目 = 某路径），整串副本 8193 含该路径 | `wpa_L_ext` | `wpa_L_whole` | **`wpa_L_ext`** | ✓ |
| N6b | 同上无扩展 | exit 0 | oversize | **exit 0** | ✓ |
| N7 | 常量设为 GMAX=300 / LMAX=200 / SMAX=100，逐个触发 | 各认各的 | — | 增长 296 → 0、444 → `grows by more than 300`；最长行 200 → 0、201 → `longline`；副本 ≤100 正常判、>100 进大副本（陈旧 P0 → 时间） | ✓ 6 行全对 |
| N8 | `_sg_vx_apply` 契约；TMAX | 前两条成立；TMAX 按 `wpa_L_total` | TMAX 例按 `wpa_L_seg` | 便宜形状：k=7 exit 0，k=8 `wpa_L_total`；21an 的 `edge8193` 翻边 | 规格字面形状不可用（F-08） |
| N9 | k 行 8000 字符 token（k=3/5/8）、2000 短行、1500 行 watch，经变量读取 | 只能是 finding / longline / time，墙钟 < 5 s | oversize | 路径在后：finding 2.73 s / time 3.34 s / time 3.49 s；2000 行：finding 1.81 s（3.2：2.54 s）；1500 watch：time 4.26 s（3.2：5.15 s） | 3.2 下 watch 形不满足 < 5 s（F-03） |
| N10 | 在 `_sg_vx_big_judge`、`nocredit` 分支内注入故障 | exit 2 | — | `exit 1` / 未绑定 / `return 1` → 2；`return 3` → 时间文案 | ✓ |
| N11 | 最长行测量：60 KB 单行、4000 行，N 与 4N | < 1 s，比值 < 8 | — | 0.05 / 0.01 s；0.06 / 0.15 s（比 2.5） | 比值判据在毫秒级抖动（F-10） |
| N12 | W12 单键形在 > 8192 的行里；19 条变量形 BLOCK 包超长行 | 前者不误拦；后者全 `longline` | 前者 oversize | 前者 exit 0（整表形仍 2）；后者整串包 19/19，后缀包 16 + 3 条 `time` | 后半不可实现 / 抖动（F-04） |
| N13 | 模式 × 值长 {0,1,100,4096} × 引用 {0,1,8,9} × 花括号 × 敏感/良性，估计副本 ≤ 8192 | 新旧退出码与 stderr 逐字节相同 | — | 104 组，**0 组不同**（24 组估计超限已跳过） | 仅在 5.2 上跑；3.2 **未核实** |
| N14 | 两行各 5000 个汉字 + 读取 + `\| wc -l`，`LC_ALL` 分别为 en_US.UTF-8 / C | 按各自口径 | oversize | UTF-8：exit 0；C：`longline` | ✓（F-11） |
| N15 | 9 处注释的 grep 断言 | 退役短语不在，新关键词在 | — | **未核实**（断言本身待写） | F-07 |
| N16 / N16b | 真实流量回放 / 合成替身 | 见规格 | — | **未核实**：语料不可读；`standin.sh` 不存在 | F-16 |
| N17 | `bash -n`；SC-30b；全部 SC-N 在 3.2 | 全绿 | — | `bash -n` 两版本通过；SC-30b 通过；SC-N 在 3.2 的逐条结果见本表；**全套件未跑**（任务书禁止） | F-17 |
| N18 | 套件全部 BLOCK 用例 | 仅 7 条变化 | — | 迷你套件 12/19，失败恰为预测的 7 条 | F-18；全套件范围**未核实** |

### 4. 未核实

- Windows MINGW64、真 macOS 上的 `kill -KILL` / `sleep` / 管道行为（规格已声明未实测）。
- SC-N16 / N16b（语料禁读；`traffic/standin.sh` 不在仓内）。
- 全套件（任务书禁止），因此「套件头注释计数」「SC-13」没有跑；SC-N13 在 bash 3.2 上的版本也没有跑。
- F-13 的 fork 失败路径：没有稳定复现手段。
- F-04 的「前缀包」变体：只按构造推理，没有单独跑完。

### 5. 产物（均在本席工作目录，只读审计，不涉及仓内文件）

目录：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217audit-r2/backend-architect/`

- 试派生补丁副本：`secret-guard.sh`（基线副本 `secret-guard.base.sh`；统一 diff `trial-patch.diff`，187 行；生成脚本 `apply-patch.py`，helper 与 `longline` 正文从 proposal 逐字抽出：`spec-helper.txt`、`spec-longline-body.txt`）。
- 迷你套件：`mini/hooks/tests/mini.test.sh`（补丁副本）、`mini-base/...`（基线）；输出 `mini-new.out`、`mini-base.out`。
- 实验脚本：`lib.sh`、`direct.sh`、`n5.sh`、`n7.sh`、`n11.sh`、`n12*.sh`、`n13.sh`、`orphan.sh`、`rcmap.sh`、`negclock.sh`、`watchscale*.sh`、`seg3.sh`、`probe-growth.sh`。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical，4 Major：F-01、F-02、F-03、F-04；Minor 13 条：F-05 至 F-17；F-18 为核对结果，不计）。

理由：硬截止机制按规格实现后在两种 bash 上行为正确，未发现新的 fail-open 路径，也没有「照规格做不出来」的部分；但硬截止的硬度依赖一个没写、没测的不变量（F-02），且好几条 SC 的形状要么不可实现、要么对负载敏感（F-01、F-03、F-04），在 SC-N17「全部 SC-N 全绿」的要求下会反复红灯。

## 轮次记录

- 第 2 轮，本席为 backend-architect，全新实例，未参与第 1 轮，也没有读取同轮其他席位的报告。
- 先读任务书与 proposal v2 全文，再核对基线 hook 与套件的行号；随后在副本上落地 What Changes 1–6，再做实验。
- 实验范围：SC-N1、N1b、N1c、N2、N3、N4 族、N5a–f、N6、N6b、N7、N8（便宜形状）、N9（四种形状）、N10、N11、N12、N13（5.2）、N14；既有 21aa–21ap 的迷你套件；SC-30b 闭包检查；W4 / W5 / W6 证据重生成。
- 与第 1 轮的关系：R1 的 3 个 Critical 在 v2 里均有对应实现，试派生没有发现它们回潮；R1 的 A5、A6、A8、A12、A19 处置实测到位。本轮的 4 个 Major 全部落在 v2 新写的部分（硬截止的不变量、SC 形状、SC 抖动），没有一条来自 v1 沿用文本；v1 沿用的只有 F-17 与 F-09 中关于 `wpa_x_finding` 的一句。
- 时间：超出任务书建议的 90 分钟（约 2 小时，其中大量时间花在 bash 3.2 与首遍很慢的形状上，且宿主机负载高）。
