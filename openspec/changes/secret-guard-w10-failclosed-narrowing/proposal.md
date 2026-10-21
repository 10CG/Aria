# secret-guard W10 尺寸预算收窄：按增长量判 + 大副本在硬截止下完整判定（10CG/aria-plugin#217）

> **Level**: 2（本 proposal + A.2 产出的 `detailed-tasks.yaml`）
> **Status**: Draft v2 —— post_spec R1 判 FAIL（去重后 3C/14M/7m），据此修订；owner 2026-10-21 二次裁定撤回 D；待 post_spec R2
> **Created**: 2026-10-21（v1 `acd6a95`）；v2 同日
> **Linked Issue**: `10CG/aria-plugin#217`
> **关联**：
> - W10 的来源：`10CG/aria-plugin#154`（WP-A `secret-net-l3-and-bypass-paths` TASK-014 的 M6 返工，owner 2026-10-14 裁定 fail-closed）。
> - `10CG/aria-plugin#228`：已转积压，用的是同一批真实流量证据；它的 proposal §v3 指向本 change。
> - `10CG/aria-plugin#216`：时间预算（v1.76.1），下文称「协作式时间预算」。
> - `10CG/aria-plugin#219`：Windows MINGW64 约为 Linux 的 2.6 倍（慢平台倍率的出处）。
>
> **证据**：`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`（`evidence/` W0–W6，脚本在 `traffic/`）和 `.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E12-base-real-traffic.txt`。命令原文不入库，原因见「证据与复现」。
> **基线**：aria v1.76.1（`59e333c`）+ standards `a611136`。下文行号都指这一版，B.1 重锚。
> **编号约定**：下文裸写的 `#n` 一律指 `10CG/aria-plugin#n`。
> **审计**：post_spec R1 汇总见 `.aria/audit-reports/post_spec-R1-1792577352602-secret-guard-w10-failclosed-narrowing-aggregated.md`，本版逐簇处置见文末「R1 处置对照」。

## Why

### 现状

v1.76.1 的 W10（变量展开第二遍）有三道尺寸上限，超限一律 fail-closed 拦截。三个常量定义在 `hooks/secret-guard.sh:594–596`：

| 上限 | 判据（基线代码） | 触发后 |
|---|---|---|
| `_SGV_VMAX` = 4096 | 收集到的单个值超过 4096 字符：赋值 `:645`、for 列表 `:659`、一层链式代入后 `:668–669` | `_sg_vx_collect` 返回 2 → 拦，**不管变量有没有被引用** |
| `_SGV_SMAX` = 8192 | 代入中的副本**总长**超过 8192：`${NAME}` 分支 `:685`、`$NAME` 循环 `:694` | `_sg_vx_apply` 返回 2 → 拦。**数的是总长，不是增长量**；整串模式下副本约等于整条命令 |
| `_SGV_TMAX` = 65536 | 分段模式下各段副本长度之和（`:744`） | 拦 |

尺寸拦截用 `_sg_emit_blocked` 的 oversize 模板，开头是「Nothing was matched」。

后果：任何超过 8 KB、又引用了一个已赋值变量的整串模式命令都会被拦，哪怕展开只多出几个字符。

### 真实流量（本机 Claude Code 会话记录）

| 问题 | 结果 | 证据 |
|---|---|---|
| 超过 8 KB 的真实命令有多少被 W10 尺寸上限拦下 | 739 条里 130 条，占 **17.6%** | E12 |
| 超过 4 KB 的真实命令里被 W10 尺寸上限拦下的 138 条，按原因分 | SMAX（总长）137 条，全部是整串模式；VMAX（值长）1 条；for 列表 0 条 | W1 |
| 那 137 条的增长量 | ≤ 0：2；1–256：60；257–1 K：64；1–4 K：10；> 4 K：1（最大 6200）。**全部不超过 8192** | W1 |
| 那 1 条 VMAX | 4594 字符的带引号「赋值」，位于命令里的 heredoc 开始之后，很可能是 heredoc 正文被 `_sg_vx_collect` 误认成了 shell 赋值；命令里另有一处 `eval` | W1；`traffic/dprobe.py` |
| 完整判定（含 credit）代入后的 138 个副本 | 平均 0.19 s，最慢 0.97 s；138 条全部判为无害 | W1 |
| 加上首遍耗时后，硬截止设为 3 s / 4 s 时会被按时间拦的条数 | Linux 0 / 0；Windows（×2.6，粗估）8 / 3；bash 3.2（×4，粗估）35 / 17。这些全是基线本来就拦的命令 | W5 |
| 只匹配规则、不算 credit 的话 | 31 条命中规则（今天靠 credit 放行），匹配平均 0.16 s | W2 |
| 代入后副本的最长行 | 中位数 566，最大 4457（字节，见「证据与复现」）；没有超过 8192 的 | W3 |

**结论**：这 138 次拦截里，137 次是总长上限的误伤，增长量都很小，而完整判定它们很便宜。

### 8192 原本要防什么，以及 v2 为什么改用时间兜底

基线头注释（`:577–596`）给 SMAX 的立论是：BLOCK 判定的代价随副本长度平方增长，判定一旦晚于超时就会丢失。R1 审计实测后，判定成本应更正为三项（BA-F-01、CR-M1、QA-F1）：

1. **逐行固定项**：`_sg_compute_credit` 对约 14 个过滤器各调用一次 `_sg_line_match`（`:182`），每次都对副本的**每一行**求一遍正则，约 0.5–0.9 ms/行。2000 行、每行 16 字符（34 KB）时，credit 要 1.4–1.6 s。
2. **逐 token 平方项**：`:476` 的 tight 检测里，`$_SG_SRVCFG` 以 `[A-Za-z0-9._-]*` 开头，一个 8000 字符的 token 单独就要约 1.0–1.2 s（W4：16000 字符约 3–5 s）。k 行各有一个长 token 时，成本乘以 k。
3. **跨行项**：`$_SG_PROCTAB_ALL` 里的 `_SG_PS_REMOTE_T`（`:446`）含 `[^|]*`，会跨空白、也跨换行。1000 行 `watch watch watch watch`（24 KB）时，单这一条正则就要 2.1–3.0 s。

所以 v1 的前提「最长行 ≤ 8192 ⇒ credit 成本有上界」不成立。任何只看形状（行数、行长、总长）的门都封不住第 3 项；真正的上界只能来自**时间**。v2 让大副本的判定在硬截止下进行，到点没判完就拦，这就是 B 的实现方式。

另外，v1 对 `:476` 说「它的通配段不跨空白」也不准确：`_SG_PROCTAB` 的 `[^|;&]*` 包含空白和换行，阻止它跨行**匹配**的是其后的 `[[:blank:]]`。而第 3 项表明，同组里的 `_SG_PS_REMOTE_T` 在包装词密集的文本上依然昂贵。

M6 当初用「总长 > 8192 一律拦」，防的是「判定迟到 → 超过 Claude Code 的 5 s → fail-open」。v2 用硬截止保住同一个保证，同时把大而不膨胀的命令放回正常判定。

## What Changes

只改 `hooks/secret-guard.sh` 的 W10，以及相邻的一处扩展接缝。

### 1. 增长上限代替总长上限（姿态 A）

- 新常量 `_SGV_GMAX=8192`，与其他 `_SGV_*` 定义在一处。
- `_sg_vx_apply S`：在函数入口计算一次 `lim=$(( ${#1} + _SGV_GMAX ))`。必须用 `${#1}`，因为循环里 `s` 会被改写（BA-F-12）。原来与 `_SGV_SMAX` 比较的两处都改为与 `lim` 比较：
  - `${NAME}` 分支（`:685`）：`_sg_vx_replace "$s" "\${$n}" "$v" "$lim"`；
  - `$NAME` 循环（`:694`）：`(( ${#out} + ${#s} > lim )) && return 2`。

  语义：代入过程中，**任一中间副本**比原串长出 8192 以上，就停下并返回 2，`_SG_SUB` 保持原串。这与基线一样是边构建边检查，不会构建出超限的串。整串模式和分段模式用同一个函数，所以口径相同。
- `_sg_vx_pass` 里 apply 返回 2 的两处拦截（`:725`、`:740`）改用新的原因串，逐字见第 5 项。
- `_SGV_SMAX`（8192）保留，但含义改为「大副本」的分界：代入成功后 `${#_SG_SUB} > _SGV_SMAX` 的副本走第 2 项，不再直接拦。W9 扩展仍按它判尺寸，见第 4 项。
- 不变的部分：
  - `_SGV_VMAX` 4096：值长上限，变量被不被引用都拦（D 已撤回）。
  - `_SGV_TMAX` 65536：分段模式下各段**副本完整长度**之和，不按增长计。因此多段的大命令仍可能被 TMAX 拦，这一点如实申报。

### 2. 大副本在硬截止下判定（姿态 B，承载 A 与 C）

**调用点**：在 `_sg_vx_pass` 里，凡是 apply 返回 0、且 `${#_SG_SUB} > _SGV_SMAX` 的副本（整串模式的那一份，或分段模式的某一段），原来的 `_sg_judge_one` 改为新 helper `_sg_vx_big`：

- 返回 3：由 `_sg_vx_pass` 写时间文案（`_sg_emit_blocked "time" "$cmd" <mode> timeout`，与基线的时间拦截同文），并返回 2。
- 其他返回值：原样返回。
- 不大于 `_SGV_SMAX` 的副本照旧调用 `_sg_judge_one`，行为不变。

整串模式（替换 `:728` 那一行）：

```bash
    if [[ $ar -eq 0 ]]; then
      if (( ${#_SG_SUB} > _SGV_SMAX )); then
        _sg_vx_big "$_SG_SUB" whole; rc=$?
        if [[ $rc -eq 3 ]]; then _sg_emit_blocked "time" "$cmd" whole timeout; return 2; fi
        return "$rc"
      fi
      _sg_judge_one "$_SG_SUB" whole; return $?
    fi
```

分段模式（替换 `:748–750` 三行）：

```bash
    if (( ${#_SG_SUB} > _SGV_SMAX )); then
      _sg_vx_big "$_SG_SUB" segment; rc=$?
      if [[ $rc -eq 3 ]]; then _sg_emit_blocked "time" "$cmd" segment timeout; return 2; fi
    else
      _sg_judge_one "$_SG_SUB" segment; rc=$?
    fi
    [[ $rc -ne 0 ]] && return "$rc"
```

**时钟**：

- 新增 `_SG_P0=$SECONDS`，放在 `:178` 的 `set -uo pipefail` 之后。这是 hook 进入 bash 后最早的可执行语句之一。
- `SECONDS - _SG_P0` 是「hook 启动以来经过的整秒数」。它包含首遍；也不受环境里预设的 `SECONDS` 影响——bash 会把环境值导入为起点，相减之后正好抵消（W6 envcase）。
- 协作式预算的时钟 `_SG_T0`（`:607`，在 `_sg_vx_collect` 入口重置，不含首遍）保持不变，仍管现有各检查点。

两个时钟各管各的：`_SG_T0` 判断本次判定在各检查点是否超预算，`_SG_P0` 只供硬截止使用。

**截止时长**：`left = min(_SG_TIME_BUDGET, 3) - (SECONDS - _SG_P0)`。

- `_SG_TIME_BUDGET` 就是 `10CG/aria-plugin#216` 的预算：默认 3 s，可用 `SECRET_GUARD_TIME_BUDGET_S` 调整，`_sg_time_budget` 将其封顶在 4。
- 硬截止**另外封顶在 3 s**。`SECONDS` 是整秒粒度，读数最多比真实流逝时间少约 1 s，所以总耗时不超过 3 s + 1 s + 收尾时间，在 Claude Code 的 5 s 之前留出约 1 s。环境变量只能把截止调**短**（测试用 0 或 1），调到 4 对硬截止无效。
- `left ≤ 0` 时不 fork，直接返回 3。这就是 v1「判定前已没有时间就拦」的那一半。

**参考实现**（逐字；`traffic/deadline-helper.sh` 与此相同，W6 就是用它跑出的证据）。两个函数放在 `_sg_vx_pass` 之前，即源码闸门 `:926` 之上，所以套件 source hook 时能看到：

```bash
# _sg_vx_big COPY MODE -- #217: judge a copy longer than _SGV_SMAX under a hard deadline (owner posture B: a judgement that cannot finish in time BLOCKs).
# The judgement (_sg_vx_big_judge) runs as a background job inside a command substitution, and a timer job kills it with SIGKILL at the deadline: the time budget
# (_SG_TIME_BUDGET, capped at 3 s here) counted from the hook's start _SG_P0, so the first pass is inside it. Status: 0 allow; 2 blocked (the judgement's block text,
# captured and written here only after it finished, so a killed judgement never leaves a partial text); 3 out of time or no time left (nothing judged, the caller
# writes the time text); any other status of the judgement (an internal error) is returned as is and fails closed upstream.
_sg_vx_big() {
  local left out rc nl=$'\n'
  left=$(( (_SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3) - (SECONDS - _SG_P0) ))
  (( left > 0 )) || return 3
  out="$( _sg_vx_big_judge "$1" "$2" 2>&1 &
          jp=$!
          ( sleep "$left"; kill -KILL "$jp" ) >/dev/null 2>&1 </dev/null &
          tp=$!
          wait "$jp" 2>/dev/null; r=$?
          kill -KILL "$tp" >/dev/null 2>&1
          printf '\n%s' "$r" )"
  rc="${out##*"$nl"}"; out="${out%"$nl"*}"
  [[ "$rc" =~ ^[0-9]+$ ]] || return 3
  (( rc >= 128 )) && return 3
  [[ -n "$out" ]] && printf '%s' "$out" >&2
  return "$rc"
}
# _sg_vx_big_judge COPY MODE -- runs inside the deadline: the longest line (one linear read loop) routes the copy -- longer than _SGV_LMAX: rows only, no credit
# (owner posture C, _sg_judge_one ... nocredit); otherwise the normal judgement with credit (owner posture A).
_sg_vx_big_judge() {
  local line max=0
  while IFS= read -r line; do (( ${#line} > max )) && max=${#line}; done <<< "$1"
  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi
}
```

要点（每一条都有对应的 SC）：

- 判定作为命令替换里的后台作业运行，计时作业到点 `kill -KILL`。`wait` 加 `2>/dev/null`，吃掉 shell 的 `Killed` 作业提示，否则它会混进拦截文案（W4）。
- 判定的输出（拦截文案）先被捕获，等判定正常结束后才由父进程写到 stderr。被掐断的判定即使写了半截文案也会被丢弃，只出时间文案。
- 失败的方向都是拦：
  - `sleep` 不可用或失败 → 计时作业立即 kill → 返回 3；
  - 命令替换没拿到数字状态 → 返回 3；
  - 判定内部出错（状态不是 0 也不是 2）→ 原样上抛，由 `:1581` 的父进程按 internal error 拦下。
- 判定提前结束时，计时作业里的 `sleep` 会成为孤儿，一直睡到截止点。它的 fd 全部重定向到 `/dev/null`，不占 Claude Code 的管道（W4：管道在 2–4 ms 内收到 EOF）。
- 开销：Linux 上每次约 1–2 ms（W4），只有大副本才付。

**分流**（`_sg_vx_big_judge`，在截止内运行）：

- 最长行用一次线性的 `while IFS= read -r line` 循环求出。参数展开剥离法和 `{8193,}` 正则都是超线性的，禁止使用（R1-A5）。
- 最长行 > `_SGV_LMAX`（新常量 8192）：**只匹配规则、不算 credit**（姿态 C），调用 `_sg_judge_one "$copy" <mode> nocredit`，见第 3 项。
- 否则调用 `_sg_judge_one "$copy" <mode>`：含 credit，与小副本是同一个判定（姿态 A）。
- 「字符」的口径：`${#line}` 按 hook 当时的 locale 计数，UTF-8 下一个多字节字符算 1，C locale 下按字节算。这与基线 `_SGV_*` 的口径一致，不另作规定（R1-A21，由 SC-N14 钉住）。

### 3. `_sg_judge_one` 增加 `nocredit` 模式（姿态 C）

- 签名变为 `_sg_judge_one SEG MODE [nocredit]`。不传第三个参数时，行为与基线逐字节相同（SC-N13）。
- W12 中和（`:1506–1509`）照旧在最前面执行，所以 C 路径和普通路径共用同一份中和代码。这样也不再需要搁置分支 `b2ed608` 里的 `_sg_environ_neutral`（R1-A6）。
- 第一处改动是局部变量声明：`local seg="$1" mode="$2" pat nocredit="${3:-}"`。
- 第二处改动在规则循环里，命中后、计算 credit 之前插入：

```bash
      if [[ "$nocredit" == nocredit ]]; then   # #217 C: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
        _sg_emit_blocked "$pat" "$seg" "$mode" longline
        return 2
      fi
```

### 4. W9 扩展保持绝对尺寸门（R1-A4）

`_sg_per_segment_eval` 在 `:1554–1555` 对整条命令调用 `_sg_vx_apply "$cmd"`、取得 `ar` 之后，紧接着加一行：

```bash
    [[ $ar -eq 0 ]] && (( ${#_SG_SUB} > _SGV_SMAX )) && ar=2   # #217: the extension keeps the ABSOLUTE copy limit; _sg_vx_apply's 2 is growth-based now
```

这样，扩展对「代入后副本 > 8192」的处理与基线完全相同：有扩展条目时按原文案（`:1563`）拦，没有条目就不看。扩展本身的代价（在副本上重跑 `_sg_core_eval`）不变，也不放进硬截止。

### 5. 文案（逐字）

| 场合 | `_sg_emit_blocked` 的参数 | 模板 |
|---|---|---|
| 增长超限，整串（`:725`） | `"the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize` | oversize；`Limit hit:` 行即左列原因串 |
| 增长超限，分段（`:740`） | `"a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize` | 同上 |
| 大副本判定超时，或开始前已无时间 | `"time" "$cmd" <mode> timeout` | 现有时间模板，不变 |
| 超长单行命中规则 | `"$pat" "$seg" "$mode" longline` | 新模板，见下 |

增长超限沿用 oversize 模板是准确的：这时没有任何规则被求值，确实「Nothing was matched」。超长单行则是命中了规则，所以不能借用 oversize 模板（R1-A7）。

新的 `longline` 分支插在 oversize 分支之后，heredoc 正文如下（逐字，含两处展开）：

```
[secret-guard] BLOCKED: command reads a secret-bearing source in a line longer than
${_SGV_LMAX} characters after variable expansion. Matched pattern: $pat

At this size the guard does not look for value-REDACTING filters (| jq 'keys',
| wc -c, >/dev/null, ...): on a line this long that check alone can outlast
Claude Code's 5s hook timeout and let the command through UNSCANNED, so the
match alone blocks the command (fail-closed).

Split it into smaller commands and run them one at a time:
  - keep every variable value, and every command after expansion, short;
  - write long files with the Write / Edit tool instead of a heredoc.
命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令

Command was (first 200 characters): $(_sg_redact_echo "${command:0:200}")
```

分段模式下不追加「Triggering segment」行，因为副本可能很长。

### 6. 清理与注释

- 删掉 `_sg_vx_collect` 链式循环里恒为假的 `[[ -z "${_SGV_V[j]}" ]] && continue`（`:666`）。空值在收集时已经跳过（`:646`、`:660`），链式代入只会把非空串替换成非空值（CR-D1 已核实）。这是 #217 的小项。
- 注释同步：见 Impact 里 9 处位置的封闭清单。

## 不变量与范围外（如实）

**放宽了什么**（放行面扩大，CHANGELOG 要申报）：

- 代入后副本 > 8192、但增长 ≤ 8192 的命令，不再按尺寸拦，改为完整判定：没有规则命中、或 credit 成立，就放行。
- credit 沿用现有语义：整串模式下，命令里**任一处**脱敏过滤（比如无关位置的 `>/dev/null`、`| wc -l`）都会给整份副本 credit（BA-F-15）。E11 显示这在小命令上已是基线常态（71 条）。这是姿态 A 的固有含义。

**仍然拦什么**：

- 增长 > 8192（新原因串）；
- 任一值 > 4096（VMAX，不管是否被引用，不变）；
- 分段副本总和 > 65536（TMAX，不变）；
- 大副本里有超长单行且命中规则（C，新模板）；
- 大副本判定超时，或开始前已经没有时间（B，时间模板）；
- 扩展生效时，整条命令的副本 > 8192（不变）。

**时间上不新增 fail-open**：大副本判定受硬截止约束，在 Linux 的 bash 5.2.15 与 3.2.57 上实测准时掐断（W4、W6）。**未实测**的是 Windows MINGW64 和真 macOS：如果这些平台上 `kill -KILL` 不能及时终止判定，大副本会退回「判定迟到 → 5 s 超时 → fail-open」，比基线（按尺寸拦）差。发版前要么实测，要么在 CHANGELOG 申报（TASK-004）。

**范围外**：

- D（放行未被引用的超大值）：owner 2026-10-21 撤回（Decision 5）。
- for 列表止于换行（#217 第 2 项）：本版撤下（Decision 6），转入残余 issue。
- count 轴（从第 17 个赋值、第 9 个引用、第 9 条 for 起放行，fail-open）：不变；#217 自己建议暂不改。
- 首遍（`_sg_core_eval` 判原命令）不计时：不变，属于 `10CG/aria-plugin#228`。把硬截止挪到 `:1581`、包住整个 `_sg_per_segment_eval`，只需十来行就能把首遍也纳入；但这会改变首遍的超时姿态，慢平台上一些本来「慢但放行」的命令会改为被拦。这是 owner 的决定，留给 #228 重启时裁定（Decision 9）。
- `# guard:ack` 逃生口、协作式时间预算（`_SG_T0` 的各检查点）：不变。

## Owner 裁定点

| | 内容 | 裁定（owner 2026-10-21） |
|---|---|---|
| A | 大而不膨胀的命令：由「一律拦」改为「完整判定后按结果判」 | 放宽 |
| B | 时间护栏：大副本判定来不及完成就拦，文案用时间预算 | 保留 fail-closed。v2 把实现方式从「判定前看已用时间」改为「判定在硬截止下进行」，姿态不变；R1 汇总后已向 owner 通报 |
| C | 代入后有超长单行（> 8192）又命中规则：不评估脱敏过滤，直接拦 | 保留 fail-closed |
| D | 放行未被引用的超大值 | **撤回**（二次裁定，依据见 Decision 5）。维持基线：超大值一律拦 |

## Success Criteria

「bf」= baseline-failing，即在 v1.76.1 上必红。编号用 `SC-N`，不与套件里已有的 `SC-<n>`、`SC-T`、`SC-R` 撞号。

两种跑法：

- **e2e**：以子进程把 JSON 输入喂给 hook（套件 `wpa_*` 的做法），每次都得到新的 `_SG_P0`。
- **直调**：在新 shell 里 source hook，按锚点抽出源码闸门之后的函数（套件 `:1801` 起的做法），并显式设置 `_SG_P0`。

凭据形路径一律在运行时拼装（套件惯例）。

| SC | 类型 | 输入 | 期望（新版） | 基线 | 抓哪类坏实现 |
|---|---|---|---|---|---|
| SC-N1 | bf，e2e | issue 复现形：命令开头有 `(`，走整串模式；约 9.7 KB；300 个对短变量的引用；良性 | exit 0 | 尺寸拦（`wpa_L_whole`） | 仍按总长 8192 判 |
| SC-N1b | bf，e2e | 大命令，所有引用都在第 8193 字符之后，增长小，良性 | exit 0 | 尺寸拦 | 增长按被改写的剩余串计算 |
| SC-N1c | bf，e2e | ≥ 24 KB、增长 < 100 的良性整串命令 | exit 0 | 尺寸拦 | 按 SMAX + GMAX 的总长判 |
| SC-N2 | bf，e2e，逐字 | SC-N1 的形状，再加一个值为凭据形路径的变量，并经变量读取 | finding 模板，`Matched pattern:` 是对应规则 | 尺寸拦 | 大副本没被真正判定 |
| SC-N3 | bf，e2e + 直调 | 增长恰为 8192 与 8193；`$NAME` 与 `${NAME}` 两种写法；整串用 e2e，分段直调 `_sg_vx_pass` 并预置 `_SG_SEGS` | 8192：进入判定，含读取则 finding；8193：按 `wpa_L_grow_whole` / `wpa_L_grow_seg` 拦 | 两侧都按总长拦 | 边界差一；`${NAME}` 分支漏改 |
| SC-N4 | bf，e2e | 大副本，最长行恰为 8192，含「凭据读取 + `\| wc -l`」 | credit 生效，exit 0 | 尺寸拦 | 一律只匹配规则 |
| SC-N4b | bf，e2e，逐字 | 同上，最长行 8193 | `longline` 模板拦，`Matched pattern:` 是对应规则 | 尺寸拦 | 一律算 credit；用原串量行长 |
| SC-N4c | bf，e2e | SC-N4b 的形状去掉读取（不命中规则） | exit 0 | 尺寸拦 | 超长行一律拦 |
| SC-N4d | bf，e2e | 大副本，全是短行，含读取 + `\| wc -l` | exit 0 | 尺寸拦 | 大副本一律不算 credit |
| SC-N4e | e2e，时延 | 一行 24 KB、含读取。形状由 TASK-001 实测选定，须满足「只匹配规则 < 1 s，含 credit 的判定 > 3 s」，两个实测值写进用例注释 | `longline` 模板拦，墙钟 < 2 s | 尺寸拦 | 先算 credit 再丢弃 |
| SC-N5a | 直调 | `_SG_P0=$((SECONDS-100))`；副本 8192 与 8193 各一份，良性 | 8192：照常判定，返回 0；8193：返回时间拦 | — | 硬截止作用于所有副本；分界差一 |
| SC-N5b | bf，e2e | 环境预设 `SECONDS=100000`，默认预算，良性大副本 | exit 0 | 尺寸拦 | 截止用了绝对 `SECONDS` |
| SC-N5c | bf，e2e，时延 | `SECRET_GUARD_TIME_BUDGET_S=1`，对抗形状（SC-N9 中 k = 5 的那一种） | 时间模板拦，墙钟 < 2.5 s | 尺寸拦 | 没有真正掐断，只在判定前看表 |
| SC-N5d | 直调 | `_SG_TIME_BUDGET=99`，`_SG_P0=$((SECONDS-3))`，良性大副本 | `_sg_vx_big` 返回 3 | — | 截止没有另封顶 3 s（那样会返回 0） |
| SC-N5e | 直调，故障注入 | 先定义 `sleep() { return 127; }`，再对对抗形状调用 `_sg_vx_big` | 返回 3，墙钟 < 0.5 s | — | 计时失败时放行或挂起 |
| SC-N5f | 直调 | `_SG_TIME_BUDGET=0` | 返回 3，不 fork | — | 没有时间了仍去判定 |
| SC-N6 | bf，e2e，逐字 | 扩展生效（`.aria/secret-guard.paths` 列出某个路径）；整串副本 8193、增长小、含该路径 | 按扩展的尺寸文案（`wpa_L_ext`）拦 | W10 尺寸拦（`wpa_L_whole`） | 扩展也用了增长口径（会放行） |
| SC-N6b | bf，e2e | 同 SC-N6，但没有扩展 | exit 0 | W10 尺寸拦 | — |
| SC-N7 | 直调 | 探针里把 `_SGV_GMAX`、`_SGV_LMAX`、`_SGV_SMAX` 设成互不相同的值（如 300 / 200 / 100），逐个触发 | 每个检查点只认自己的常量 | — | 三者同为 8192 时被掩盖的接线错误 |
| SC-N8 | 直调（改写 21an） | `_sg_vx_apply`：建成的副本 ≤ `${#S}+8192`；被拒时 `_SG_SUB` 不变。TMAX：5 段，每段约 8 KB、各自增长约 6 KB | 前两条成立；TMAX 例按 `wpa_L_total` 拦 | TMAX 例按 `wpa_L_seg` 拦 | TMAX 被误改为按增长计 |
| SC-N9 | e2e，对抗成本 | 首遍 < 1 s 的对抗形状（入库时把基线首遍的实测值写进用例注释）：k 行各一个 8000 字符 token，加经变量的读取（k = 3、5、8）；2000 行短行加读取；1500 行 `watch watch watch watch` 加读取 | 结局只能是 finding、longline 或 time，不得 exit 0；墙钟 < 5 s；bash 5.2 与 3.2 各跑一遍 | 尺寸拦 | 大副本判定无上界（R1-A1 的闸） |
| SC-N10 | 直调，故障注入 | 套件 `wpa_fault_case` 的手法：让 `_sg_vx_big_judge`、`_sg_judge_one` 的 `nocredit` 分支内部出错 | exit 2，不得 exit 0 | — | 新 helper 的错误被吞成放行 |
| SC-N11 | 直调，线性 | 最长行测量：60 KB 单行；4000 行短行；各取 N 与 4N 两档 | bash 5.2 下 < 1 s，且 4N 与 N 的耗时比 < 8 | — | 二次方实现 |
| SC-N12 | e2e | 超长行（> 8192）里的 W12 形单键读取（四种形式见 `:1500`）；另把套件中 20 条 BLOCK 用例的命令各自包进超长行 | 前者不误拦；后者全部按 `longline` 拦 | 尺寸拦 | C 路径漏了 W12 中和或漏了规则 |
| SC-N13 | 差分 | 副本 ≤ 8192、值 ≤ 4096 的命令网格：模式 × 值长 {0, 1, 100, 4096} × 引用数 {0, 1, 8, 9} × 花括号与否 × 敏感/良性读取 | 新旧两版的退出码与 stderr 全文逐字节相同 | — | 阈值以下的行为漂移 |
| SC-N14 | e2e | 同一条多字节命令，在 `LC_ALL=en_US.UTF-8` 与 `LC_ALL=C` 下各跑一次 | 分界按各自 locale 下 `${#}` 的口径判定，两种结果都写进用例注释 | — | 口径被改成固定按字节或按字符 |
| SC-N15 | 文档同步 | Impact 列出的 9 处注释 | 每处一条 grep 断言：退役短语不在，新语义的关键词在 | — | 注释没改 |
| SC-N16 | 单机验收 | 真实流量回放：冻结清单 `evidence/W0-corpus-manifest.tsv`（2412 条，按 sha256）经 `traffic/refreeze.py` 复原后，基线与新版各跑一遍（Linux，bash 5.2） | 判定变化只有 oversize → allow，且恰好是 W1 的那 137 条（按 n 核对）；n = 666 仍按 VMAX 拦；其余各类变化（finding → allow、allow → block、oversize → finding、oversize → time 等）都为 0；没有命令新超过 5 s（n = 630 基线就要 14 s，不计）；复原缺失的条目逐条列出，不计入 | — | 真实流量上的意外漂移 |
| SC-N16b | 可复现 | `traffic/standin.sh` 生成的合成替身语料（W1 四类形状各若干，生成脚本入库） | 与入库的期望结果逐条一致 | — | 供第三方复跑 |
| SC-N17 | 回归 | 全套件；`bash -n` 在 3.2.57 与 5.2.15 下；全部 SC-N 在真 bash 3.2.57 下实跑 | 全绿；计数同步（套件头注释、standards 三处） | — | — |
| SC-N18 | 差分 | 套件里全部 BLOCK 用例 | 判定与文案不变，**除了**下表「预计会变的既有用例」里的条目 | — | 意外波及 |

**预计会变的既有用例**（读码推演；TASK-001 用草稿实现实跑确认，确认结果写回本表）：

| 用例 | 现在 | v2 预计 | 理由 |
|---|---|---|---|
| 21ab（`:2552–2554`） | 三条命令都按 `wpa_L_seg` 拦：8193 字符的读取段；`f=x; echo $f` 加 9000 字符填充；同形加 4500 个 ` a` | 8193 字符的读取段：增长约 8 KB → 大副本判定 → finding。后两条：增长约 0 → 判定为良性，exit 0 | 由总长改为增长。21ab 的注释钉的正是「数总长、不数增长」，语义翻转 |
| 21ac 第 3 条（`:2566`） | 4096 字符 for 列表的整串副本按 `wpa_L_whole` 拦 | 增长约 4094 → 判定 → finding | 由总长改为增长 |
| 21ag（`:2586`） | 36 KB 的稠密副本按 `wpa_L_seg` 拦 | 增长约 31 KB → 按 `wpa_L_grow_seg` 拦 | 只换文案 |
| 21aj（`:2606`） | 1 / 7 / 8 个超长段排在读取之前，按 `wpa_L_seg` 拦 | 每段三次引用 4000 字符的值，增长约 12 KB → 按 `wpa_L_grow_seg` 拦，读取段仍不被判定 | 只换文案 |
| 21al 第 2 条（`:2634`） | 花括号形、8193 字符的整串副本按 `wpa_L_whole` 拦 | 增长约 5.4 KB → 判定 → finding | 由总长改为增长 |
| 21an（`:2676`） | 断言「建成的副本 ≤ 8192」 | 改为「≤ `${#S}+8192`」（SC-N8） | 函数契约变化 |
| 21ao 第 2 条（`:2683`） | 8193 字符的整串副本按 `wpa_L_whole` 拦 | 增长约 4 KB → 判定 → finding | 由总长改为增长 |

预计不变：21aa、21ad（VMAX；D 已撤回）、21ae、21af、21ah、21ai、21ak、21am、21ap（扩展的绝对门，见第 4 项）。

块头注释（`:2510–2520`、`:2544–2549`、`:2556–2562`）随之改写，即 Impact 第 9 处。

新字面量：

- `wpa_L_grow_whole='the command grows by more than 8192 characters after variable expansion'`
- `wpa_L_grow_seg='a command segment grows by more than 8192 characters after variable expansion'`
- `longline` 模板的首行另设一条断言。

## Impact

- **版本**：PATCH——收窄误拦，时间上不新增 fail-open（Windows / macOS 未实测的情况除外，见上）。版本号由 owner 定。
- **aria `hooks/secret-guard.sh`**：
  - 改：`_sg_vx_apply`、`_sg_vx_pass`、`_sg_per_segment_eval`（扩展门一行）、`_sg_judge_one`（第三参数）、`_sg_emit_blocked`（`longline` 分支）、`_sg_vx_collect`（删死代码）。
  - 新：常量 `_SGV_GMAX`、`_SGV_LMAX`、`_SG_P0`；函数 `_sg_vx_big`、`_sg_vx_big_judge`。
- **注释同步**（封闭清单，9 处，KM-F-03；行号为基线）：
  1. `:86–94`：文件头 Residual gaps 里的 W10 条。
  2. `:577–596`：LENGTH BUDGET 段。按 Why 的三项成本模型重写，写明 GMAX、LMAX、SMAX 各自的含义，删去「blocking is as cheap as passing was」。
  3. `:597–607`：时间预算段。点名第二个时钟 `_SG_P0` 和硬截止，保留「`_SG_T0` 在 collect 入口重置」的说明。
  4. `:630–631`：`_sg_vx_collect` 契约。VMAX 不变，只删去与死代码有关的措辞（如有）。
  5. `:674–676`：`_sg_vx_apply` 契约。返回 2 的条件改为增长。
  6. `:701–703`：`_sg_vx_pass` 契约。新增大副本、时间、超长行三个出口。
  7. `:826–828`：`_sg_emit_blocked` 注释。新增 `longline`。
  8. `:1534–1536`：`_sg_per_segment_eval` 注释。「too large to build」改为「副本 > 8192」的绝对门。
  9. 测试 `:2510–2520`、`:2544–2549`、`:2556–2562` 的块头。退役「the WHOLE judged string, not its growth」等表述，把 GMAX、LMAX 加进「契约数字」清单。
- **aria `hooks/tests/secret-guard.test.sh`**：SC-N1–N18；上表 7 个既有用例；新字面量；计数。
- **aria `CHANGELOG.md`**：草稿见下。
- **standards `conventions/secret-hygiene.md`**：`:23`、`:316`、`:352` 三处测试计数，现为 822 / 816，已比套件头注释的 831 / 825 陈旧，改为发版时实跑的权威值。W10 的预算数值在 standards 和 README 里都没有写，不需要同步。
- **发布同步面**（owner 门，TASK-005）：按 CLAUDE.md「发布同步面」执行——aria 5 文件、主仓 gitlink（aria 与 standards 都变时是两个）、主仓 VERSION、root README badge、`system-architecture.md` §2.8 与 `version-scheme.md`。机械兜底：`m6-version-badge-match`、`i18n-readme-translation-currency`、`plugin-version-arch-docs-match`。
- **Rule #6**：只改 hook，不是 Skill 变更，按 substitute 处理（bf SC + 套件回归 + 差分 + 非作者对抗 + 真实流量回放）。`rule6_note` 写进 A.2 的 `detailed-tasks.yaml`。

**CHANGELOG 草稿**（R1-A15）：

- **收窄**：W10 的副本上限由「代入后总长 > 8192 即拦」改为「代入后增长 > 8192 即拦」。大于 8192、但增长不超过 8192 的命令，改为在硬截止内完整判定。真实流量上，超过 4 KB 的命令里此前被尺寸上限误拦的 137 条，在 Linux 上全部放行。
- **申报（放宽面）**：这些大命令的判定沿用现有的 credit 语义——整串模式下，命令里任一处脱敏过滤都会给整条命令 credit。
- **申报（仍然拦）**：增长 > 8192；任一值 > 4096（是否被引用都拦）；分段副本总和 > 65536；代入后有超过 8192 的单行且命中规则（新文案，不评估脱敏过滤）；大副本判定超过时间预算（时间文案）；扩展生效时副本 > 8192（不变）。
- **申报（残余）**：首遍判定不计时（`10CG/aria-plugin#228`）；count 轴仍放行；Windows / macOS 上硬截止未实测（届时若已实测，改写为实测结果）。

## 证据与复现

| 文件 | 内容 | 生成方式 |
|---|---|---|
| `evidence/W0-corpus-manifest.tsv` | 冻结语料：2412 条 > 4096 字节的真实命令，每条记 `n`、字节数和 sha256，不含原文 | `traffic/manifest.py`（`TRAFFIC_DIR` 指向抽取目录） |
| `evidence/W1–W3` | 138 条的分类、只匹配规则的结果、最长行 | `traffic/w10-traffic.sh`、`rowhit-traffic.sh`、`expline-traffic.sh`。只有 W2 需要 `NEUT_SRC`，即带 `_sg_environ_neutral` 的 hook（搁置分支 `b2ed608`） |
| `evidence/W-summary.txt` | W1–W3 的摘要 | 目前是手写摘要（R1-A22）；B 阶段改为脚本生成 |
| `evidence/W4-watchdog.txt` | 硬截止机制在两版 bash 上的可行性 | `traffic/watchdog-probe.sh` |
| `evidence/W5-deadline.txt` | 硬截止在真实流量上的代价估算 | `traffic/deadline-estimate.sh` |
| `evidence/W6-deadline-helper.txt` | 本文参考实现 × hook 的真实判定 | `traffic/deadline-probe.sh` + `traffic/deadline-helper.sh` |
| `evidence/W7-d-case.txt` | D 唯一救下的那 1 条命令的结构（只有是非与计数） | `traffic/dprobe.py` |

**复现**：命令原文不入库，因为真实会话里的命令可能含内部路径和凭据形文本。复现步骤：

1. 用 `10CG/aria-plugin#228` 的 `traffic/extract.py` 把本机会话记录抽到仓外的 `TRAFFIC_DIR`。
2. 用 `traffic/refreeze.py` 按 W0 的 sha256 复原到冻结编号。

新会话会让抽取编号漂移（KM 实测重抽得到 2426 / 745），所以只认哈希。第三方没有这批会话记录，靠 SC-N16b 的合成替身复跑。

**口径**：

- W3 用 mawk 的 `length`，按**字节**计。`${#line}` 在 UTF-8 下按字符计，字符数不会超过字节数，所以「没有超过 8192 的行」在字符口径下同样成立。
- `judge_s` 只计 `_sg_judge_one`，不含收集、首遍和护栏；W5 已把 E12 的整条耗时加回。
- Windows ×2.6、bash 3.2 ×4 是从 `10CG/aria-plugin#219` 和 E12 借来的粗估，没有为 #217 重测。

## Decision record

1. **先量真实流量，再设计**（#228 的教训）。E12 与 W1–W3 定下了主项：137/138 是总长上限的误伤，增长量都很小。
2. **为什么不直接调大 SMAX**：大副本的判定成本没有形状上的上界（Why 第 3 项），调大只会让构造出来的输入重新「判定迟到 → fail-open」。
3. **为什么用硬截止，而不是「判定前看表」**（R1-A1、A17）：
   - 贵的是判定本身，判定前看表看不到它：BA 的实验 C 里，bash 5.2 上 6 次 0 次拦住。
   - 硬截止在两版 bash 上实测准时（W4、W6），失败的方向都是拦。
   - BA 提出的三条路（加成本门、先做 #228 的根治、申报残余）都以「没有技术收口」为前提，硬截止让这个前提不再成立。
   - 姿态没变，仍是 B，所以按技术裁定采用，并已向 owner 通报。
4. **时钟锚在 hook 启动，截止另封顶 3 s**：Claude Code 的 5 s 从 hook 启动算起，所以截止必须把首遍算进去。`SECONDS` 是整秒粒度，读数最多少约 1 s，3 s 加 1 s 仍在 5 s 之内，留有收尾余量。
5. **撤回 D**（owner 二次裁定，2026-10-21）：
   - v1 的立论「未被引用的值不参与任何代入」不成立：`${NAME:-x}`、`eval` 拼接、`${!NAME}` 等写法都会读到这个值（R1-A3；实测出现基线拦、新版放、且真的读到凭据的情况）。
   - 要判准「未被引用」，就得枚举 shell 读变量的各种间接方式，而这枚举不完。
   - 能挡住审计反例的保守判定，会把真实流量里 D 唯一救下的那 1 条也拦下：那条的「赋值」位于 heredoc 之后，命令里另有 `eval`（W7）。所以收益为 0。
   - 根因是 `_sg_vx_collect` 把 heredoc 正文里形似赋值的文本当成了 shell 赋值，转入残余 issue。
6. **撤下「for 列表止于换行」**（R1-A2）：照字面实现会截断反斜杠续行的列表，新增漏检；真实流量 0 例。转入残余 issue，以 R1 QA-F2 验证过的续行感知正则为起点。
7. **扩展保持绝对尺寸门**（R1-A4）：扩展会在副本上重跑 `_sg_core_eval`，长副本的代价是真实的；本机启用扩展的项目为 0。
8. **C 复用 `_sg_judge_one`**（R1-A6）：W12 中和只有一份代码；C 路径不另写规则循环，也不移植搁置分支里的 `_sg_environ_neutral`。
9. **整体硬截止留给 #228**：同一机制挂在 `:1581`，能把首遍也纳入，从而关上 `10CG/aria-plugin#228` 的对抗超时残余。但这会改变首遍的超时姿态，属于 owner 的决定，作为 #228 重启时的选项之一。
10. **count 轴不在范围内**：#217 自己建议维持 fail-open。

## Tasks（A.2 细化为 detailed-tasks.yaml）

| 任务 | 阶段 | 内容 | 执行 |
|---|---|---|---|
| TASK-001 | B.1 | 入场：续用认领、建分支、重锚行号；基线红（SC-N 中的 bf 项在 v1.76.1 上实跑为红）；用草稿实现实跑「预计会变的既有用例」，把结果写回该表；为 SC-N4e、SC-N9 选定并实测形状 | 主控 |
| TASK-002 | B.2 | 实现 What Changes 1–6 | 执笔席 |
| TASK-003 | B.2 | 非作者对抗复核：坏实现由非作者构造，至少覆盖 SC 表最后一列的每一类 | qa 席 |
| TASK-004 | B.2 | 验收：SC-N16 真实流量回放、SC-N16b 替身、全套件、bash 3.2；Windows / macOS 实测，或在 CHANGELOG 申报 | 主控 |
| TASK-005 | C | 发版（owner 门）：版本号、发布同步面、双推核验 | owner + 主控 |
| TASK-006 | D | 收口：先开残余 issue（for 列表的续行感知；collect 把 heredoc 内的赋值形文本当作 shell 赋值），再在 #217 下逐项对账并关闭——第 1 项和小项完成；第 2 项转残余 issue；第 3 项由 owner 撤回；count 轴不变。提交信息里只对 `10CG/aria-plugin#217` 使用关闭关键词；`10CG/aria-plugin#154`、`10CG/aria-plugin#203`、`10CG/Aria#221` 只用 `Refs`（INV-6），每次推送前做关键词核对 | 主控 |

## R1 处置对照

| R1 簇 | 级别 | v2 处置 |
|---|---|---|
| A1 | C | 硬截止（What 2；Decision 3、4；SC-N5、SC-N9）；Why 的成本模型重写 |
| A2 | C | 撤下第 4 项（Decision 6） |
| A3 | C | D 撤回（owner；Decision 5） |
| A4 | M | 扩展的绝对尺寸门（What 4；SC-N6） |
| A5 | M | 最长行用线性的 `read` 循环（What 2；SC-N11） |
| A6 | M | C 复用 `_sg_judge_one` 的 W12 中和（What 3；Decision 8；SC-N12） |
| A7 | M | 文案逐字（What 5） |
| A8 | M | `_SG_P0` 锚 + 截止封顶；时间类 SC 改为 e2e 环境变量与直调设 `_SG_P0`（SC-N5a–f） |
| A9 | M | 冻结清单 + `refreeze.py` + 判据钉到逐条（SC-N16）；合成替身（SC-N16b） |
| A10 | M | 逐条写明 SC 的形状、bf 前提和要抓的坏实现（SC 表） |
| A11 | M | 采纳 QA 附录 C；去掉与 D、for 列表相关的 REF、CONT |
| A12 | M | 既有用例逐条预测（上表），TASK-001 实跑确认 |
| A13 | M | 9 处注释的封闭清单 + standards 三处计数（Impact；SC-N15） |
| A14 | M | TASK-006 收口与残余 issue |
| A15 | M | CHANGELOG 草稿去歧义，列全放宽面与残余 |
| A16 | M | 重写「不变量与范围外」 |
| A17 | M | Decision 3 |
| A18 | m | 更正 Why 里对 `:476` 的说明 |
| A19 | m | `lim` 入口计算、「任一中间副本」、TMAX 口径（What 1） |
| A20 | m | 逐条消歧；v1 的「一半预算」等措辞已删除 |
| A21 | m | 写明字符口径（What 2）；SC-N14 |
| A22 | m | 「证据与复现」一节 |
| A23 | m | 完整引用、互链、SC 命名空间、基线含 standards、`rule6_note` 归 A.2 |
| A24 | m | 按平台写明收益（Why 表的 W5 行；CHANGELOG 写「Linux 上全部放行」） |
