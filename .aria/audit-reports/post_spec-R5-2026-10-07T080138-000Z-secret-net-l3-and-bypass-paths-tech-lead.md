---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-07T09:12:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

- 被审对象 @ `6efb9b2`:
  - `proposal.md` 全文 (1-449); `git diff -U0 b07f69a 6efb9b2` 的全部 hunk 位置。
  - `baseline_probe.py`: 1-140 (环境与生成器); 559-600 (SC-1 / SC-2 / SC-4 定义与 `UTF16_CASES`); 1283-1300 (`READ_ALT_PATHS`、18j / 18k); `DIFF_SHAPES` 与 19af / 19ag; 1675-1676、1703-1748、1770、1785 (22ao-22ar、`WRAP_T_ENV`、22bo / 22br / 22bs、22at、22bj); 2380-2480 (SC-33、SC-34)。
  - `baseline-evidence.md`: 1-40。
- 三个 issue 全文与全部评论: 10CG/aria-plugin#154 (含评论 19339)、10CG/aria-plugin#203、10CG/Aria#221 (含评论 25898)。
- 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` 全文; `CLAUDE.md` 规则 #6 / #7 / #10 与多远程推送两条硬约束。
- 源码 @ aria `268da8f`:
  - `hooks/secret-scan.sh` 全文;
  - `hooks/secret-guard.sh` 全文;
  - `hooks/hooks.json` 全文;
  - `skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md:195-204`。
- 规范 @ standards `2bc1c4c`: `secret-hygiene.md` 节目录、§2.5 (114-126)、§5-§10 (277-404)。
- 研究笔记:
  - `cc-hooks.md` 全文;
  - `secret-guard.md` 节目录与 §2(d) (110-134);
  - `secret-scan.md` 节目录与 §1.2 (35-62);
  - `precedent.md` 节目录。
- 上一轮: R4 聚合报告全文 (全部 finding 表、收敛计算、主控记录); R4 tech-lead 报告全文。
- 执笔材料: `v5-writer-report.md` 全文; `writer-v5-proto/README.md`; `timing.py` 头部。
- 原型: 会话内原件 `exp/writer-v5/work/t5f/` (两个 hook 指纹 `4b2ddba40b080619` / `a7b8109bb3f8e576`, 与 `deliver/logs/final_T.out` 第 2-3 行一致), 对基线两个 hook 的完整 diff。
- 接缝: `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:330-350` (`guard_config_hooks`)。
- 平台事实:
  - 本机 Claude Code 二进制 2.1.285 (Spec 引用的版本) 与 2.1.292 (`~/.local/share/claude/versions/`), 用字符串抽取读: hook 事件表、`PostToolUseFailure` 输入 schema、Bash 工具的退出码语义与 ShellError 抛出点;
  - `systemctl(1)` 手册 (systemd 252) EXIT STATUS 表。
- 实跑。全部在 `scratchpad/audit/post_spec-R5-tech-lead/` 下: 基线与原型两棵树都是 `cp -a` 副本; HOME / TMPDIR 指向该目录; 命令只作 stdin 文本喂 hook、从不执行; 像凭据的值在进程内由 `secrets` 生成、不打印。
  - L1 差分与核对: `diff_t.py` (139 个形态的扩展 / 内建差分)、`clusterF.py`、`pe.py`、`m3_cov.py`、`readface.py`;
  - L3 核对: `u_superset.py` (NUL 形态的超集检查)、`w1perf.py`、`longval.py`、`oldtag_long.py`、`kvcost.py`、`kvlong.py`、`kv34b.py`、`kv34b_fix.py`、`failure_env.py`;
  - 微基准 `hashbench.sh`;
  - 归档 `timing.py`: 跑 `f,f0` 与 `f,fhit` 两次, 均带 `--judge`;
  - 探针 `WPA_ONLY=SC-34` 对原型跑一次。
  - 按派单控制规模: 未重跑全量探针与全量坏实现。

## Findings

### M1 [66d6eb81] major · issue · architecture · proposal.md SC-3

**summary**: L3 对「失败的工具调用」整体失明。Spec 把它误述为「字符串形 `tool_response` 会不会到达 PostToolUse 未证实」, 并钉成 SC-3 3b。平台事实如下:
- PostToolUse 只在工具成功时触发;
- Bash 命令按默认语义非零退出即失败, 其输出装在错误文本里送给模型, 触发的是 `PostToolUseFailure` (输入字段 `error`, 无 `tool_response`);
- secret-scan 既未注册该事件, 提取链也不读 `error`。

因此 W8 / W10 / W11 多处「交给 L3 兜底」(含 `systemctl status` 放行) 对非零退出的命令不成立。这个缺口不在已知限制、Out of scope、建议开单, 也不在 Impact 与关单披露里。

**证据**:
- 平台 (二进制 2.1.285 与 2.1.292 都有):
  - 事件表原文: `| PostToolUse | Tool name | Run after successful tool |` / `| PostToolUseFailure | Tool name | Run after tool fails |`;
  - 失败事件输入 schema: `hook_event_name:R("PostToolUseFailure"),tool_name,tool_input,tool_use_id,error:o(),is_interrupt?,duration_ms?` (无 `tool_response`);
  - Bash 退出码语义: 默认 `isError: e!==0`; 例外只有 grep / rg / egrep / fgrep / findstr 的 1、diff / fc / where 的 1、robocopy;
  - 抛出点: `if(ve.isError&&!Sr){i("tengu_bash_tool_command_failed",…); … throw new _U({stdout:"",stderr:<合并输出>,code:xe.code,…})}`。`_U` 即 ShellError ("Shell command failed"), 展示文本 = `Exit code N` + stderr + stdout;
  - 失败事件的 hook 同样支持 additionalContext (`hook_additional_context … hookEvent:"PostToolUseFailure"`);
  - 旁证: 本会话里非零退出的 Bash 调用都以 `Exit code 1` 开头的错误结果返回。
- 注册与提取面:
  - `hooks.json`: secret-scan 只注册在 `PostToolUse` (matcher `Bash|Read|Edit|Write|MultiEdit`);
  - `secret-scan.sh:135-142`: 只读 `.tool_response.*` / `.tool_result.*`。
- `systemctl(1)` EXIT STATUS: LSB 码 3 = "program is not running" / unit is not active。即 `systemctl status <unit>` 对未运行或失败的单元退出 3。
- Spec 原文:
  - `:53`「字符串形 `tool_response` 会不会到达 PostToolUse 未证实」;
  - `:54`「字符串形 `tool_response` 不扫 (… 以 KNOWN-LIMIT 钉住, SC-3)」; `:269` SC-3;
  - `:203`「`systemctl status` 放行 … W2 之后其输出里的 `Authorization: token …` / `CF-Access-Client-Secret` 由 L3 检出」;
  - `:157`「输出侧由 W2 的 `kv-secret-assign` 兜底」;
  - `:188`「这些交给 L3 (W1 + W2 在输出侧兜底 …)」;
  - Out of scope (`:246-253`) 与 7.1-7.20 无失败事件。
- 实跑 (hook 直调, 值运行时生成): 用三行文本 —— AWS key id 行、`JWT_SECRET = <43>`、`> Authorization: token <40 hex>` —— 各测两种信封:
  - 包成 `PostToolUseFailure` 输入 (`error` = `Exit code 22⏎<行>`): 基线与原型都 `exit 0`、无告警;
  - 包成成功的 Bash 结果: 原型三行都告警, 基线只告警 AWS 行。

**失败场景**:
1. 照 v5 实现并 ship。
2. 一个凭据在 argv 里的轮询单元崩溃, AI 运行 `systemctl status poller.service` 排障。L1 按 W11 放行。
3. 命令退出 3, 工具失败; 带 `Authorization: token …` 的 CGroup / ExecStart 行进入模型上下文。
4. PostToolUse 不触发: 无告警、无日志、无 `fp`。
5. 同理, 任何「先打印、后失败」的命令都不经过 L3, 例如 W8 已知限制里的读取写法后接一个失败步骤, 或 `curl -f -v -H 'Authorization: token …'` 遇 4xx 退出 22。

owner 读到 W8 / W10 / W11 的「交给 L3」与 Impact 的「新告警」, 会以为这些路径有事后兜底。

**怎么会红** (建议补的行):
- 若作 known-limit: 一条 `PostToolUseFailure` 信封行, 基线与目标都静默 (都 yes)。
- 若采纳下文方案 A: 它是 baseline-failing (基线 no, 目标 yes)。「只提取 `error` 不注册」的坏实现由 hooks.json 结构行抓; 「只注册不提取」的坏实现在本行转红。
- 现有 3b 钉的是一个到不了 PostToolUse 的形态, 对真实缺口恒绿。

**建议修法** (技术级, 二选一, 最少做 B):
- **B (不扩范围)**:
  - W1 已知限制与 SC-3 改写为「失败的工具调用 (Bash 非零退出等) 触发 PostToolUseFailure, L3 不注册、不扫描」, 3b 换成失败信封的 known-limit 行;
  - W8 / W10 / W11 每处「交给 L3」加限定「仅对成功的调用」, `systemctl status` 一处点名退出 3 的情形;
  - Out of scope 与 7.x 各加一条, 建议高优先级;
  - Impact「新告警」与 10CG/aria-plugin#154 关单评论各加一句。
- **A (补齐 W1 同族)**:
  - `hooks.json` 为 secret-scan 增一条 `PostToolUseFailure` 注册 (同 matcher), 提取链加 `.error`;
  - 补 baseline-failing 行与结构行 (31d 由「字节一致」改为「只多这一条注册」), 再加一条 post-ship 惰性腿 (合成值打印后 `exit 1`);
  - 不撞 10CG/Aria#199 的守卫 (不出现 `completeness_gate` 字面), 但失去「hooks.json 零改动」这一 Rule #6 锚点;
  - 失败事件上 additionalContext 的端到端送达需要一次 spike。

### M2 [755aab21] major · issue · implementation · proposal.md What.W2

**summary**: W2「值抽取与去空白同样线性」给出的规则只禁「前导 `*` 的 `#` / `##`」, 不足以保证线性。bash 的 `#` / `##` / `%` / `%%` 删除在不命中 (或命中点靠后) 时逐个试位置, 每次 O(长度), 任何模式都是平方级。

参考原型按这条规则写出的 kv 去引号 `V="${V#[\"\']}"` —— 即 W4 表「去空白与一层引号」的自然写法 —— 在不带引号的长值上就是平方级:
- 约 300 KB 的单个值让 L3 越过 4 s 的每进程 CPU 上限被杀;
- 同一输出里基线本来检出的凭据随之丢失;
- SC-34 34b 与 W14 (i3) 都没有「长且不带引号的 kv 值」形态, 验收对这条退化恒绿。

这是 R4 簇 W 的残余, 该簇部分关闭。

**证据**:
- Spec:
  - `:69`「取值只用 `${s%%X*}` 找分隔符 … **不用前导 `*` 的 `#` / `##` 最短 / 最长前缀删除**」;
  - `:115` W4 表 kv 行「去空白与一层引号」;
  - `:306` 34b 的 9 个形态里, kv 只有「300 KB 大写连续段接在键前」与「export 形 8 KB 空白串」, 值都短;
  - `:239` (i3) 同样没有长 kv 值。
- 原型 `t5f/aria/hooks/secret-scan.sh` 的 `_value_of` kv 分支: `…; _trimV; V="${V#[\"\']}" ;;`。
- 微基准 (bash 5.2.15, `C.UTF-8`, 主机 1 分钟负载约 20), 对不以引号起头的串:

  | 写法 | 100 KB | 200 KB |
  |---|---|---|
  | `${V#[\"\']}` | 1.38 s | 6.85 s |
  | `${V#\"}` | 1.54 s | 7.72 s |
  | `${V%%[=:]*}` (不命中) | 1.80 s | 7.31 s |
  | 对照: 以引号起头 | 0.02 s | 0.08 s |

- 原型整钩子 (Bash 真实信封, 单行 `SVC_TOKEN = <值>`):
  - CPU 时间: 64 KB 1.13 s; 128 KB 2.08 s; 400 KB 12.0 s;
  - 300 KB 时, `KEY = v` / `export KEY=v` / YAML `  KEY: v` 三形在 4 s CPU 上限下都被杀 (rc -9, 无告警);
  - 对照: 加单引号的同值 2.2 s, 告警。
- 归因: 只把那一句换成 `[[ "${V:0:1}" == [\"\'] ]] && V="${V:1}"` 的副本, 三形都是 2.2 s、告警。
- 同输出里的基线检出: AWS key id 行加一条 200 KB 的 kv 行, 原型 3.87 s, 已逼近上限。
- 34b 恒绿: 原型在负载约 22 下跑 `WPA_ONLY=SC-34`, 34a 7/7、34b 9/9、34c 2/2 全 yes。

**失败场景**:
1. 实现者照 W2 的规则与 W4 表写去引号 (原型即如此), 437 行全 yes。
2. 生产中某个工具输出含一个约 250-300 KB 以上、不带引号的 kv 值 (`KEY = …` / `export KEY=…` / YAML 冒号形)。
3. L3 越过 5 s 超时被 harness 杀掉, 该输出里的其它凭据 (含基线可检出的) 全部不告警。

触发尺寸远大于 R4 簇 W 的 8 KB, 实际暴露面小。但它正是主控裁定 3「写明为什么线性」要防的那一类, 而且参考设计本身就不满足 Spec 宣称的不变量。

**怎么会红** (建议新增的 34b 成员: 300 KB 不带引号的 kv 值, 4 s CPU 上限):
- 基线 no (tag 不存在);
- 原型 (`${V#…}`) no, 被杀;
- 改为首字符判断的实现 yes。

**建议修法**:
- `:69` 的规则改为: 取值代码里的任何 `#` / `##` / `%` / `%%` 删除都必须在常数次尝试内命中 (分隔符必在且靠前); 可能不命中的单字符剥离 (引号、空白) 用 `${V:0:1}` 判断再切片, 或用 `[[ =~ ]]` 捕获。
- W4 表 kv 行补同一句实现注意。
- 34b 与 (i3) 各加一个「长且不带引号的 kv 值」成员。

### m1 [6ff1d962] minor · issue · documentation · proposal.md What.W11

**summary**: 包裹 × `printenv` 备选会把带参数的 `printenv`(单变量读取, 是真实命令而非文本提及) 一并拦下。现状:
- 参考原型对下列 8 条都由放行变拦: `docker exec web printenv NODE_ENV`、`docker compose exec web printenv NODE_ENV`、`ssh host printenv PATH`、`nomad alloc exec … printenv …`、`pct exec 101 -- printenv HOME`、`sh -c 'printenv HOME'`、`bash -c "printenv LANG"`、`watch printenv X`;
- W11 写「只拦裸 env / printenv」;
- Impact 只把「包裹词之后出现 printenv 这个词」作为文本提及申报, 并称「以往放行的日常核对形态不变」;
- 22bj 只钉 env 词成员, 没有任何行钉这一形态。

所以「只拦裸」与「后接空白即拦」两种实现都全绿。这是 R4 `6ff1d962` 的 printenv 一侧, 该条部分关闭。

**证据**:
- Spec:
  - `:196`「只拦裸 `env` / `printenv`」;
  - `:203`「包裹词之后出现 `env` / `printenv` 这个词同样被拦 (… `env` 作参数词也算 …)」;
  - `:344`「以往放行的日常核对形态不变」与「包裹词 … 之后出现 `env` / `printenv` 这个词的文本被拦」。
- 探针: 22bj (`baseline_probe.py:1785`) 与 22at (`:1770`) 都没有带参数的 `printenv`。
- 实跑 (基线 | 原型):
  - 上述 8 条均为 `0 | 2`;
  - `podman exec web printenv NODE_ENV`、`kubectl exec pod -- printenv HOSTNAME`、`lxc exec c -- printenv HOME`、本地 `printenv HOME` 均为 `2 | 2` (基线已拦);
  - `docker exec web printenv NODE_ENV | wc -c` 为 `0 | 0`。

**失败场景**: 若 ship 的是原型写法, 容器里常用的单变量核对 `docker exec <c> printenv <VAR>` 被拦, 而 CHANGELOG 未列。用户转向 `# guard:ack`, 正是 10CG/Aria#221 评论 25898 担心的方向。

**建议修法**: 定一个方向并钉行。
- 倾向拦: 这与基线本地 `printenv <VAR>`、podman / kubectl / lxc 包裹一致, 而且单变量也可能是凭据。
  - W11 改为「拦裸 env 与任意 printenv」;
  - Impact 新拦截点名 `docker exec <c> printenv <VAR>` 一类;
  - 22bo 或 22bj 加 `docker exec web printenv NODE_ENV` → 2。
- 反之: 规则里限定 `printenv` 后只能接分隔符或行尾, 并加一条 allow-guard 行。

### m2 [0033f2f4] minor · issue · documentation · proposal.md 待 owner 复议

**summary**: 待复议 23 (以及 W11 `:196`、22br 的描述) 把「转储后接锚定 `grep '^X='`(读一个变量)」说成 10CG/Aria#221 评论 25898 称为正当核对的形态。25898 原文只把「读长度、读 env 变量名」列为正当核对, 没有「读一个变量的值」。后者会把该变量的值打进输出, 对凭据名就是泄露。

**证据**:
- 25898 原文:「**正当核对**（读长度、读 env 变量名）→ 拦」。
- Spec:
  - `:196`「锚定的 `| grep '^X='` (读一个变量)、`| cut -d= -f1` (列变量名) … 放行 (SC-22 22br; 这是 10CG/Aria#221 评论 25898 称为正当核对的形态)」;
  - `:440`「理由: 10CG/Aria#221 评论 25898 把「读一个变量」与「列变量名」当正当核对」。
- R4 本席 M1 原文把两个来源分开写: 25898 对应变量名; 冻结的 BLOCKED 文案对应 `grep '^SAFE_PREFIX='`。
- 实跑 (原型): `nomad alloc exec -task server abc env | grep '^PATH='` → 0。

**失败场景**: 不改变实现者行为 (22br 已钉放行)。影响的是 owner 对待复议 23 的复议依据:
- owner 会以为 issue 报告者认可了「读一个变量的值」;
- 备选 B (并入 tight) 的代价被说成「与 25898 的正当核对相冲突」。

**建议修法**:
- 锚定 grep 一半改引基线语义与 BLOCKED 文案的 `| grep '^SAFE_PREFIX='` (前提是前缀安全); 25898 只对应 `cut -d= -f1` 与长度。
- 在 22br / 22bs 旁注明: 对凭据名做锚定 grep 会打印其值, 这是与基线共享的限制。

### m3 [684e9a24] minor · issue · documentation · proposal.md What.W9

(与 R4 同四元组的 `684e9a24` (BOM / 旧时档数) 不是同一问题)

**summary**: W9 的文档落点 (§5.6、README Hooks 小节, 判据 SC-26 26c / 26e) 只要求写位置、字面子串、大小写、只增不减、限额、失效静默, 没要求写**保护边界**。列入的路径只获得内建 `app.ini` 行的覆盖, 即 29 个打印型读取器、`python3 -c` / `node -e` 与 Read / Edit。内建 `.env` 族会拦而列入条目放行的写法有:
- `source` / `.`、`dd if=`;
- 重定向读、`tee <`、`mapfile <`;
- `xargs cat`、`find -exec cat`、`cp … /dev/stdout`、`perl -ne`。

另有 Grep 工具、Write 与第 65 处之后的出现不受保护。采用方照 SOT 写清单, 会以为得到了 `.env` 级保护。

**证据**:
- Spec: `:171` 文档落点; `:298` 26c / 26e。
- 实跑 (原型): 上述 10 种写法对内建 `.env` 均为 2, 对列入条目均为 0。对内建名 `/etc/forgejo/app.ini` 同样是 0 (见本席 139 形态差分)。

**失败场景**: 采用方把 `/srv/billing/conf/prod.toml` 列入清单, AI 用 `source` 或 `while read … < …` 读取时放行, 采用方按文档以为已拦。

**建议修法**:
- §5.6 与 README 段各加一句保护边界: 覆盖面 = 内建 `app.ini` 行的读取器集加 Read / Edit; 不覆盖的写法按类别列出并指向 W8 已知限制; 不覆盖 Grep / Write; 只看前 64 处出现。
- 26c 增一个判据词 (如 `app.ini` 或「读取器」)。

## 上一轮对账

| 簇 | 定稿键 | 状态 | 本席亲自核验的证据 |
|---|---|---|---|
| U | `1038b8da` (ba/C1) | closed | 1. W1 `:52-53` 改为两视图并集: 基线视图 D 原样保留, 原始信封含 `\u0000` 且 N ≠ D 时才追加 N。<br>2. 原型 `_content_prog` 单一定义, 条件追加 (diff 实读)。<br>3. 本席 28 例超集核对: 四种形态 (UTF-16LE、带 BOM 的 UTF-16LE、NUL 分隔记录、CRLF 后夹 NUL) × 七种内容 (AWS / env 行 / JSON client_secret / gh PAT / postgres URL / 两行混合 / bearer)。原型逐 tag 计数都 ≥ 基线, 0 例丢失。<br>4. `final_T.out` 中 1e / 1f / 1g 均为 yes。 |
| T | `0a8380fd` (ba/M2 · qa/M1 · cr/M1 · km/M1) | closed | 1. W9 `:165` 改为: 前 64 处出现换成内建 `app.ini` 名, 交内建同一函数 `_sg_core_eval`; 原型 `_sg_ext_subst` / `_sg_ext_pass` 实读。<br>2. 本席用另一个内建名 `/etc/forgejo/app.ini` 对 139 个自拟形态做差分, 覆盖转义、`$'…'`、续行、`\|\|`、`\|&`、`2>&1` / `&>` / `>&`、引号内管道与分隔符、heredoc、子 shell / 花括号 / 后台 `&`、for / if、各类包裹、变量间接、注释、制表符、大小写。<br>3. 唯一分歧是 `cat <条目>xyz`, 属成文的字面子串语义 (19aj)。 |
| V | `22bdd143` (tl/M2) | closed | 1. 机制改为「命中只多一遍内建判定」; W14 (f-hit) 与 SC-34 34c 已加。<br>2. 负载约 14-16 时跑 `timing.py fhit --judge`: fh-a 1.99、fh-b (64 处) 2.01、fh-0 1.04; 活性为 `_sg_core_eval` 命中档 ×2、对照档 ×1; PASS。<br>3. 负载约 22 时 34c 2/2 yes。<br>4. 绝对耗时的残余见风险 1。 |
| W | `755aab21` (ba/M1) | partially closed | 1. R4 的形态已修: kv / cli 有界加左边界, 34b 9/9 在负载下 yes。<br>2. 但取值线性规则只禁前导 `*`, 原型 kv 去引号仍是平方级, 见 M2。 |
| F | `e2459206` (tl/M1 · cr/M2) | closed | 1. W11 `:196` 定为默认 credit (不属 tight); 22br (44 个运行) / 22bs (22 个运行) 两向钉住; Impact 已申报。<br>2. 本席实跑 (基线 \| 原型):<br>- `docker exec web env \| grep '^PATH='` 0\|0<br>- `kubectl exec pod -- env \| cut -d= -f1` 0\|0<br>- `docker exec web env \| grep -v PATH` 0\|0<br>- `nomad alloc exec … env` 0\|2<br>- `… env \| cut -d= -f1` 0\|0<br>- `pct exec 101 -- env \| sort` 0\|2<br>- `ps aux \| grep -v x` 0\|2<br>- `docker exec web sh -c 'env; ps aux' \| grep -v x` 0\|2<br>3. 同族残余: printenv 带参数形 (m1)、理由引文 (m2)。 |
| M | `eb350937` (qa/M2) | closed | 1. W14 `:241` 的原位改写通则已列入 `:641`; 18j / 18k 各 32 个运行。<br>2. 本席把 `:641` 正则按 `\|` 拆成 32 个备选, 逐条对 `READ_ALT_PATHS` 的 32 条路径做 `grep -E`: 每条路径恰命中 1 个备选, 没有落空的备选。 |

R4 minor 中本席认为仍未处置的:
- `6ff1d962` 只处置了 env 一侧, printenv 带参数形见 m1。

其余经抽查已处置:
- `984b1c3d`: 10m 在 `:276`;
- `6f503728`: 19ae;
- `65fb3fcf`: 23j / 25h;
- `684e9a24`: 19ai, W9 不再复述时档数;
- `aa08f71d`: 32e;
- `a8f5db8c`: W1 理由已按实测重写;
- `13e1f258`: 本席检索版本 / 审计叙事, 除合法路径与测试编号外 0 处;
- `7b20c975`: 已处置;
- `60eea71e`: 26g 13 个标记词, W9 已指明第二个 Hooks 小节;
- `cfd9ca0b`: 条目过滤只用 sed;
- `91a89f9b`: 7.20 已登记;
- `8936aa07`: 28o 在场, 22av 14 个逐个写全, 22bk 11 个, `COMMIT_FOOTER_GUIDE.md:199-202` 与引文一致。

## 对执笔人自报薄弱点与请裁项的表态

**§5 自报薄弱点**

1. **34c 是探针里唯一带比值的行**: 可接受。负载约 22 时对原型跑 `WPA_ONLY=SC-34`, 34a / 34b / 34c 全 yes。(f-hit) 两档比值 1.99 / 2.01, 坏实现是数十倍。
2. **19af 的「零分歧」只对有限形态表成立**: 可接受。本席 139 形态独立差分只有一处分歧, 且属成文的字面子串语义; 含元字符的条目已列已知限制。
3. **上界 64 / 40 是量级判断**: 可接受。真实键名与旗标名远短于此; 10n / 10o 钉现状; 待复议 31 已列备选。
4. **NUL 前提无端到端样本**: 作为已知限制可接受。但 Impact「新告警」把 NUL 检出写成了事实, 没带「前提未验证」的限定; 这个前提可以用一条惰性 post-ship 腿判定, 见请裁项 8(1)。
5. **时档余量**: (i3) 上界 2.5 可接受。**(f) 不可接受**, 理由如下:
   - 本席同主机连跑两次 (1 分钟负载约 14-16), Bash 面:
     - 第一次: 基线 0.099 s → 目标 0.151 s, judge **FAIL** (上界 0.150 s);
     - 第二次: 0.093 → 0.145 s, PASS。
   - 参考设计的比值 1.53-1.67 恒高于 1.5, 所以 (f) 档的实际判据退化成「基线 CPU ≤ 约 0.09 s」—— 这是主机属性, 不是实现属性。
   - 主机稍忙或稍慢时, 正确实现的 SC-30 会随机转红, 且没有合法下一步: 「环境不合格」只在基线 ≥ 5 s 时触发。
   - 修法: (f) 改为纯比值上界 (如 ≤ 3.0, 与 (f-hit) 同; 参考设计 1.5-1.7, 坏实现「每条一个 grep」9.7-13.3×), 或改为增量上界; (f0) 保留。
   - 本条按派单不计入 finding, 但应作为进 A.2 前的定点勘误。
6. **旧变体的回归覆盖**: 可接受。被取代者逐个写了替代者。
7. **体量 +30 KB**: 可接受 (事实陈述)。
8. **研究笔记与已推送分支**: 可接受。超出执笔权限, 已登记 7.20。
9. **单机数字**: 原则可接受。但第 5 条说明 (f) 的绝对地板对主机负载并不稳健。

**§6 请裁项**

1. **7.20 披露范围 (产品级)**: 交 owner。本席意见: 选 A, 并维持「分支暂停推 GitHub 至 ship」这一可逆措施。B 无法一致执行: Spec 正文的已知限制节 (W8 / W9 / W11、SC-17 17d、SC-22 22bh 等) 本身就是逐形态的放行清单, 「先修后披露」等于撤掉「已知限制逐项钉住」。
2. **W9 条目规则 (纯非 ASCII 条目有效、剥 BOM)**: 可接受。
3. **簇 F 的 credit 取舍**: 默认 credit 可接受, 与基线 docker / kubectl 行、裸 env、`/proc` 一致。但理由引错了 25898 (m2), 且 printenv 带参数形未定 (m1)。
4. **上界 64 / 40**: 可接受。
5. **(i3) 2.5、尺寸、`--judge`**: 可接受。但 (i3) 与 34b 都缺「长且不带引号的 kv 值」形态 (M2)。
6. **SC-34 判据口径**: 可接受, 负载下实测稳定。另请补 M2 的成员。
7. **Layer 2 句与关单验证范围句**: 可接受, Impact `:344` 与 `:357` 均已在场。
8. **未采纳项**:
   1. NUL post-ship 腿: **不可接受**。理由:
      - 一条两记录的 `printf 'HOME=/x\0JWT_SECRET=%s\0' <合成值>` 在 D 视图里不命中: 首记录无关键字, 第二记录左侧是词字符;
      - 它只在 N 视图里命中 `env-line-secret-keyword`;
      - 告警 = 前提成立, 不告警 = N 视图在生产是空操作; 两种结果都把 Impact 那句从推测变为事实;
      - 成本一条命令, 符合惰性诱饵口径。
   2. 时档判据不并入探针: 可接受。
   3. gawk 腿: 可接受 (已去掉对 awk 的依赖)。
9. **Rule #10 自作主张清单**: 可接受 (均已登记待复议)。另请把 (f) 档判据的改动作为新的技术级裁定登记。

## 风险 / 疑问

1. **负载下的绝对耗时**: 1 分钟负载约 14-16 时, 4 KB 单行命令里出现列入路径:

   | 档 | 基线墙钟 / CPU | 目标墙钟 / CPU |
   |---|---|---|
   | fh-b (64 处) | 4.4 s / 1.9 s | 8.6 s / 3.9 s |
   | fh-a (1 处) | — | 4.8 s 墙钟 |

   扩展自己的拦截因此会被 5 s 超时吃掉。内建先判, 所以不影响内建拦截。根因是基线逐字符循环在 UTF-8 locale 下超线性 (既有问题), 这支持把 7.1 提前。
2. **NUL 视图的开销**: 对接近 1 MB 信封的 UTF-16LE 文本, CPU 0.82 → 1.18 s; 无检出损失 (28 例)。
3. **待复议 18 的定级**: 扩展失效静默, 本席仍认为属产品级 (用户可见的保护契约), 同 R4 本席风险 3; 只提示。
4. **W9 `LC_ALL=C` 的作用域**: Spec 只规定读条目、匹配、切片用字节语义。若实现者把 `local -x LC_ALL=C` 写在 `_sg_ext_pass` 顶部, 替换副本会在 C locale 下判, 而内建在调用方 locale 下判: 非 ASCII 字符紧贴读取器或边界时两侧可分歧 (只会多拦)。建议加一句「`_sg_core_eval` 在调用方 locale 下运行」。
5. **BSD grep 的 `-b` 语义**: W9 依赖 `grep -o -b` 给出每个命中点的字节偏移。macOS BSD grep 在 `-o` 下的 `-b` 语义未验证 (本 Spec 只在 GNU 工具链上跑过); 偏移错位时扩展会漏拦或误拦, 内建不受影响。关单评论的验证范围披露只覆盖 10CG/aria-plugin#154。
6. **SOT §5.5 已陈旧 (既有)**: `secret-hygiene.md` §5.5 自称「Layer 2 known-limitation 全集」, 但只列了 v1.24.0 的两条。WP-A 新增大量已知限制, 建议 §5.5 改为指向 CHANGELOG / Spec。
7. **Level**: 体量已是 Level 3 量级 (三条判据字面命中), 但现在拆分只会制造接缝。维持单 Spec, Level 标签由 owner 定 (待复议 4)。
8. **接缝与认领**: 10CG/Aria#199 在 origin 上仍无 B.1 分支 (本席只读 `git ls-remote` 核对), 主仓 master 仍为 `0748dbc`。A.1 认领时间为 2026-09-30T17:57Z, 进 A.2 前须核对心跳或续期。
9. **本席自身操作**:
   - 两条 Bash 命令被现行 v1.74.1 L1 拦下 (heredoc 里的 `podman exec … env` 字样、grep 模式里带反引号的 `printenv`)。均改用 Write 工具落脚本, 未用 `# guard:ack`; 这本身是 W11 已知文本提及误拦族在基线上的实例。
   - 全部 hook 运行的 HOME 指向本席目录; 未读取或打印任何真实凭据。
   - 真仓 HEAD `6efb9b2`、aria `268da8f`、standards `2bc1c4c` 均未变; 未做任何 git 写操作。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: **0C / 2M / 3m**
- **Vote: REVISE**

## 是否足以进入 A.2

**足以**, 但须先完成定点勘误, 再按「接受当前结论 + 定点勘误 + 只对勘误处做一次定向核验」进入 A.2, 不建议再开全轮。理由:
- R4 六簇中五簇已关闭, 只剩局部残余;
- 剩余问题都是 Spec / 探针的定点勘误, 不改方案:
  - M1: 失败路径的申报与平台模型更正 (最少做方案 B);
  - M2: 线性规则与 34b 成员;
  - (f) 档判据改为与主机无关;
  - 三条 minor 的文字修正。
