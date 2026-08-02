---
verdict: REVISE
agent: backend-architect
round: R2
critical_count: 0
major_count: 2
minor_count: 2
r1_resolved: 3/3
---

# post_spec R2 审计报告 — secret-guard-nomad-var-put-echo (convergence, 复审)

## 审计对象

`/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`（按 R1 五方 findings 大改后版本）。方法：逐条核销 R1 backend-architect (M-1/m-1/m-2) 三项 findings；对新设计五个技术点做正则/shell 机制层复核，全部用 `bash -c` 对真实 `secret-guard.sh`（688 行，尚未改动，仅读取核对现有结构：L323-400 has_filter 计算区 / L401-646 risky_patterns 数组 / L648-686 匹配循环 / L78 `set -uo pipefail`）做等价实测验证，不修改仓库任何文件。

## R1 三项 findings 核销结果 — 3/3 已解决

**Major-1 (AND 合取被拆成析取风险) — 已解决，且解法强于建议**：proposal 在 Success Criteria 正上方新增「实现约束」段，明文禁止 `_pat_scoped_safe` 写成 `has_filter=1` 风格独立 if，并点名 SC-9/SC-10 为可证伪锚点。更重要的是 §What 1 的架构改动本身就是结构性防呆：新豁免机制完全脱离 `has_filter` 变量（改用 `_pat_scoped_safe(...) && continue` 的函数返回值驱动 `continue`），不再是"在 L323-400 现有风格区块里加第 15 条 if"的形态——R1 担心的"照抄主导代码风格"这条具体路径在新设计下已不存在（该风格区块与新豁免逻辑物理上不在同一循环阶段）。判定：解决。

**Minor-1 (`-out=none` 缺尾边界) — 已解决**：决策表 L85 明确要求"须有尾边界"，SC-2 用与 R1 报告完全同源的两条边界用例（`-out=nonelegit` / `-out=none-such` 须 exit=2）钉死行为。实测 `-out[=[:space:]]+none([[:space:]]|$)`：`-out=none`/`-out none` 匹配，`-out=nonelegit`/`-out=none-such` 不匹配——SC-2 描述的行为可达成。

**Minor-2 (`nomad var put` 缺尾边界) — 已解决**：§What 2 给出的新 pattern `nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)` 已实测验证：
```
MATCH   : nomad var put path k=v
no-match: nomad var putty x        ← R1 举的具体误配例, 现已排除
MATCH   : nomad var put            (行尾 $ 边界)
MATCH   : nomad  var   put   path  (多空白)
no-match: nomad-var-put x          (连字符不匹配, 符合预期)
```
判定：解决，且范围克制（proposal 明确"既有 `(get|list)` 条不动，另开 issue"，未借机扩大 diff）。

## 新设计五点技术复核

### (1) 三条 R1 findings 落地位置与措辞 — 见上，3/3 已解决，不重复。

### (2) `_pat_scoped_safe "$pat" "$command"` 的身份判定契约 — Minor，机制未落定，有具体漂移演示

proposal 只写了函数签名意图（"对特定 pattern 检查其自身语义的安全形态"），未指定 `_pat_scoped_safe` 内部如何判断"当前 `$pat` 是不是 `nomad var put` 那一条"。最直觉的实现是把 `risky_patterns` 数组里那条 ERE 字符串在 helper 内部**手抄一遍**做 `==` 字面比较（如 `[[ "$pat" == 'nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)' ]]`）。这个写法功能上可行，但身份判定的"真源"分裂成两处字面量：数组里一份、helper 里一份。实测演示一次典型漂移（helper 里的字符串被手误改了一个字符）：

```
NOT exempted -> falls through to has_filter check for pattern: nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)
```

即：数组里的 pattern 本身照常命中风险面（拦截生效，不构成安全回归），但豁免分支静默不触发——`-out=none` 会被误拦成 exit=2。**好消息**：这类漂移会被 SC-2/SC-4 直接测红（SC 断言的是行为不是实现细节），所以不是"会静默出货的坑"，而是"实现阶段容易踩、踩了会立刻被测试网接住"的坑。**更稳的身份标记法**（建议补进 Tasks 1.1，降低返工概率）：不用字符串二次抄写做身份判定，改用两者之一：
  - 共享变量：`_pat_nomad_put='nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)'`，数组元素与 helper 比较式都引用同一个 `$_pat_nomad_put`，物理上只有一处真源，无法漂移；
  - 或索引对齐：把 `risky_patterns` 改为按下标遍历（`for i in "${!risky_patterns[@]}"`），豁免规则用一个平行的关联数组 `pattern_safe_check[$i]=...` 而非对 pattern 文本做值比较。

两种都比"裸字符串 `==` 比较两份独立抄写的 ERE 文本"更稳，建议在 tasks.md 1.1 里选一种写死，避免实现者自然选择最脆的那种写法。

### (3) §What 3 的 `has_filter=0` 覆写规则 — 位置正确 (Major-1 不重开)，但**触发条件本身有未锚定的新回归面** (新 Major)

**位置层面**：proposal 文字"has_filter 计算末尾的一条撤销规则"与现有代码结构吻合——L323-400 是线性无分支的 credit 累加区，L648 起才进入按 pattern 的判定循环；`has_filter` 是**命令级单值**（循环内每次判断都读同一个值），撤销规则只要放在 L400 之后、循环开始之前执行一次即可对所有 pattern 迭代生效，语义上不存在"部分 pattern 看到旧值、部分看到新值"的顺序歧义。且这是**只减不增**的覆写（1→0，不会像 R1 C-1 那样把 BLOCK 全局降级成 ALLOW）——最坏后果是过拦截，不是新的泄漏面，方向上安全。

**但触发条件本身是新问题**：proposal 原文"`-v` / `--trace-ascii` / `--trace` 类…flag 出现时不接受纯 stdout redirect"，没有把检测锚定到"这些 flag 出现在同一个 curl 调用里"——如果实现按字面做成"命令全文裸扫 `-v`/`--trace` token"，会命中大量与 curl 无关、语义完全不同的同名短选项：`grep -v`、`ssh -v`、`docker -v`（挂载卷）、`python -v`。更关键的是，这不只是"新命令可能被误拦"的抽象风险——**能具体构造出一条现有风险 pattern 家族里、`>/dev/null` 本来合法拿到 credit、会被新规则误撤销的回归用例**：

```
grep -v FORGEJO_TOKEN ~/.bashrc >/dev/null
```

此命令本就命中 L462 的 `.bashrc` risky pattern，`>/dev/null` 本应给 credit (exit=0)；若撤销规则对 `-v` 做裸 token 扫描（不分辨这是 grep 的 `-v` 还是 curl 的 `-v`），会把 has_filter 错误撤销为 0，此命令从 exit=0 退化为 exit=2——即从"过去合法可用的写法"变成"新版本里被拦"。这属于**回归**而非单纯新命令的 FP，且 SC-6 只覆盖了 curl 场景本身（`-v`/`--trace-ascii` 配 `>/dev/null` 两条 baseline-failing 用例 + `2>&1`/`&>` 两条修复后仍放行），**没有任何一条 SC 断言"非 curl 场景下 `-v` 不得触发撤销"**，SC-13 的 347 条基线回归也不保证覆盖到这个具体组合（`.bashrc` + `grep -v` + `>/dev/null` 三者叠加是新的排列，不确定既有语料是否已含）。

**建议**：在 §What 3 明确把撤销规则的检测范围锚定到"同一个 curl 调用内"（例如复用现有 `curl[^|]*` 前缀惯例：`curl[^|]*(-v|--trace(-ascii)?)\b` 而非裸 `-v`/`--trace`），并在 Tasks 里补一条 SC（如"`grep -v secret file >/dev/null` 类非 curl 命令的 `-v` 不触发撤销"）把这道防线钉成可证伪锚点，否则这条修复本身可能在 ship 后开出与本 spec 试图堵住的同一类"看似安全实则被绕过/误伐"问题的镜像版本（这次是误伐而非漏放，但性质是同一类"检测粒度太粗"）。

### (4) `$pattern_hint` 在 heredoc 里的展开风险 — **注入风险为零，但发现一个未被识别的新 Major：`set -uo pipefail` 下的 nounset 崩溃面**

**注入层面**：heredoc (`cat >&2 <<EOF...EOF`，未加引号分隔符，会做 `$`/反引号替换) 里插入 `$pattern_hint` 本身零风险——只要 `$pattern_hint` 的取值来自实现者写死的字面量集合（`"-out=none"` / `"-out=keys"` / 空），不从 `$command` 派生，就不含用户可控内容，谈不上转义/注入问题。proposal §What 5 描述的正是"仅当匹配到 nomad var 家族 pattern 时填入…建议"，取值来源是字面量，判定：安全。

**但发现新风险**：本文件头部 L78 是 `set -uo pipefail`（**nounset 已启用**，文件其余处处可见 `${VAR:-}` 防御写法，如 L237/L238/L668 等，说明这是团队已知且必须遵守的约束）。BLOCKED heredoc 是**全局共享**代码块（§What 5 原文即承认这点），任何 risky pattern 触发都会走到同一处 `cat >&2 <<EOF ... $pattern_hint ... EOF`。若实现只在"匹配到 nomad 家族 pattern"的分支里才赋值 `pattern_hint="..."`，而在其余 ~99 条既有 pattern 触发的路径上从未初始化过这个变量，`set -u` 下第一次非 nomad pattern 触发 BLOCKED 就会在变量展开处直接报错，实测复现：

```
environment: line 25: pattern_hint: unbound variable
```

该错误发生在 heredoc 内容求值阶段，`cat` 命令本身**不会执行**——意味着预期的 BLOCKED 提示文本（含 SC-7/SC-9 依赖的 pattern 名、Acceptable filters 清单等）**完全不会打印**，stderr 里出现的是这行 bash 内部错误信息而非设计好的提示，随后脚本会继续往下执行到既有的 `exit 2`（因为文件未开 `-e`，单条命令失败不终止脚本）——**exit code 仍是 2，不构成安全回归**（fail-closed 语义不受影响），但 BLOCKED 提示文案整体失效。这直接影响 SC-7（要求 stderr 含 `-out=none`/`-out=keys`）会失败（因为压根没打印），而 SC-8（要求非 nomad 场景不含这两串）反而会"意外通过"（因为什么都没打印，自然不含）——**这是一个会被 SC-13 全量回归（347+ 条基线）大范围测红、但初次实现极易踩、且 proposal 文本完全没提及"要不要默认初始化 pattern_hint"这道防线的坑**，比 (2) 的漂移风险更严重：(2) 只影响 2 条新 SC，这里影响的是**全部**既有 BLOCKED 路径的提示文案完整性。

**建议**：在 Tasks 1.3（`$pattern_hint` 条件插入）里显式要求"每次进入循环体判断前先 `pattern_hint=''` 兜底赋值"（或 heredoc 内用 `${pattern_hint:-}` 展开），把这条 nounset 约束从"隐含在文件已有风格里、容易被新代码遗漏"变成"写进 Tasks 的显式一条"。

### (5) 新 pattern `nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)` 的 POSIX ERE 正确性 — 确认正确

已用 `[[ "$command" =~ $pat ]]`（与 L649-652 现有 bash builtin 匹配机制完全一致，非 `grep -qE` 子进程）实测：`(...)` 分组与 `|` 交替、`[[:space:]]` 括号表达式、`$` 行尾锚定四者组合语义符合预期，命中/不命中集合与 §What 2 意图一致（见 (1) 中的实测表）。无需转义顾虑（bash `=~` 对未加引号的模式变量按 ERE 解释，`(` `|` `)` 均为元字符，proposal 里这条 pattern 写法正确）。判定：确认无误。

## 总结

R1 三项 findings（AND 合取风险 / `-out=none` 边界 / `nomad var put` 边界）全部核销，且合取风险的解法是结构性的（脱离 has_filter 机制），比单纯加注释更牢固。新设计五点复核中，(1)(5) 确认无误，(4) 的"注入风险"确认为零，但复核过程中定位到两处**新的、proposal 文本未覆盖、SC 清单未钉住**的实现期地雷：`$pattern_hint` 在 `set -u` 下缺省初始化会让全部 BLOCKED 提示文案（不止新增部分）失效（新 Major，实测复现）；stderr-flag 撤销规则若按裸 token 扫描 `-v`/`--trace`（而非锚定到 curl 调用）会对既有合法命令（如 `grep -v ... >/dev/null` 命中 `.bashrc` pattern 的场景）产生回归性误拦（新 Major，给出具体可复现命令）。另有 (2) 的 `_pat_scoped_safe` 身份判定机制未落定（Minor，可测但脆，给出更稳写法）与 `-out=none` 安全形态正则未在 proposal 正文给出字面量（Minor，行为已被 SC-2 钉死但建议补全便于实现）。四项均为"实现阶段的具体缺口"而非"设计方向错误"，建议 tasks.md 补齐后再入 Phase B，故判 REVISE（非 PASS）。
