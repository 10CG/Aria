---
verdict: REVISE
agent: qa-engineer
round: R1
critical_count: 1
major_count: 3
minor_count: 3
---

# post_spec R1 — QA 审计: secret-guard-per-segment-evaluation

审计对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md`
视角: SC 可证伪性与覆盖完整性 (只审不改, 实跑 hook 于 scratchpad 副本)

## 方法论

- 实跑对象: 当前仓库 `aria/hooks/secret-guard.sh` (未改动, `git status`/`git log` 确认此分支未触碰该文件 — 是真实"改前"基线)。
- 305 条 `bash_case` 的精确命令字符串: 复制 `secret-guard.test.sh` 到 scratchpad, 将 `bash_case()` 函数体改为额外 dump `{name, want, cmd}` JSON 到文件后照常调用 `run_case`（不改变原断言行为), 跑一遍拿到 bash 自身求值后的**精确** cmd 字面值(规避手工 regex 抽取整行的转义/引号误差)。
- 独立写 Python quote-aware 扫描器: 识别顶层 `;` `&&` `||` 单独 `&` 换行 为边界, `|` 不算边界(与 spec 决策一致), 引号(`'…'`/`"…"`)/反斜杠转义/`` `…` ``/`$(...)`/`(...)`内部视为不透明(不扫描其内容), 并修正了 `&>`/`>&` 重定向误判为 `&` 边界的陷阱。

## Critical

### C-1 SC-2/SC-3 硬编码的数字口径 (15/52) 与独立复算不一致, 且遗漏至少 1 条 want=0 真边界用例

独立复算 (quote-aware, 方法见上): 305 条 `bash_case` 中 **70** 条含分隔符(含顶层管道), 非 68:

| 分类 | spec 声称 | 实测复算 |
|------|-----------|---------|
| 含分隔符 (68) | 68 | **70** |
| ├ expected=2 | 52 | **53** |
| └ expected=0 | 16 | **17** |
| &nbsp;&nbsp;├ 纯管道 | 15 | 15 (**一致**) |
| &nbsp;&nbsp;└ 含真命令边界 | 1 | **2** |

多出的 1 条 `expected=0` 真边界用例是具体、可复现的:

```
bash_case "#152 FP: multiline benign" 0 $'echo begin\necho done'
```

该命令含**真实顶层换行**(spec 决策表明确列"换行(顶层) — 切"), 实测改前 `exit=0`(已用真实 hook 验证, 见下)。这条既不在 spec Impact 表的"1 条真边界"(即 `put: KNOWN-LIMIT compound credit leak`)之列, 也不落在 SC-2 的 15 条纯管道枚举里 —— **SC-2/SC-3 均未显式点名它**, 唯一兜底是 SC-9 的全量 366 回归(能测到, 但 SC-2/SC-3 "逐条列名断言, 不用总数代替" 的设计初衷被削弱: 若实现者按 spec 文字里的"52"/"16(15+1)"去枚举锁定列表, 会漏掉这一条独立锁定)。

SC-2/SC-3 原文均把数字写进验收标准本体("15 条纯管道"/"52 条含分隔符"), 而不是"以脚本机械重新枚举"为准 —— 这使得数字本身成为可证伪的断言目标, 但目标数字有误。

**实测证据** (真实 hook, 改前基线):

```
SC-1 五条泄漏形态 (改前 exit code, 全部核实与 spec 一致):
  cat .env; echo hi >/dev/null                exit=0
  nomad var put x2 >/dev/null (批量写)         exit=0
  vault read; nomad var put >/dev/null (跨家族) exit=0
  cat .env | head -5 >/dev/null (管道+redirect) exit=0
  nomad var get && echo done >/dev/null        exit=0
  对照: cat /opt/.env (单命令)                  exit=2   [SC-1 全部核实通过]

SC-2 15 条纯管道 (改前 exit, 逐条实测, 全部 =0, 与 spec 一致):
  curl /v1/var | jq keys                       exit=0
  curl /v1/var | jq allowlist                   exit=0
  cat .env | grep specific                      exit=0
  cat .env | wc -l                              exit=0
  cat .env | sha256sum                          exit=0
  R2-C-1: jq -r projection ALLOW                 exit=0
  known-limit: cut -f1- all-fields ALLOW         exit=0
  R4-C-2: grep ^safe= prefix ALLOW               exit=0
  R4-C-2: grep -v secret invert ALLOW            exit=0
  R4-C-2: sed s/.*/redacted/ ALLOW               exit=0
  R4-C-2: cut -d= -f1 field ALLOW                exit=0
  R4-C-2: awk $1 print col ALLOW                 exit=0
  #69 FP: base64 encode benign string            exit=0
  #69 FP: tar .sshconfig (not .ssh dir)          exit=0
  var read: SOT projection allowed               exit=0   [SC-2 全部核实通过, 数字 15 本身正确]

SC-4 两条 quote-aware 用例 (改前 exit, 与 spec 一致):
  ssh find env                                   exit=2
  python -c HTTP wrapper                         exit=2

额外发现 (SC-3 覆盖口径缺口的具体反例):
  R3-C-2: exec 3< redirect  'exec 3< /opt/.env; cat <&3'          exit=2 (真边界, want=2, 已计入 53 但 spec 只数了 52)
  #152 FP: multiline benign  $'echo begin\necho done'             exit=0 (真边界, want=0, spec 完全未提及)
  PartB combined { env; }                                          exit=2 (真边界, 但落在 `{ }` 组内 — 见 M-2)
```

**处置建议**: Phase B 实现前, 用机械脚本(而非人工正则抽取)重新枚举 SC-2/SC-3/Impact 表的确切数字与用例清单, 并把"#152 FP: multiline benign"补进 SC-2/SC-3 未覆盖真空的显式回归锁定(即便逻辑上会被 SC-9 兜住, 也应像 SC-5 对待 KNOWN-LIMIT 那样给出**具名**断言, 否则"逐条列名, 不用总数代替"这条设计原则本身不成立)。

## Major

### M-1 除 SC-4 外, 其余 SC 全部是端到端 exit-code 断言, 无分段器直接单元测试

spec 第 62 行自己承认"第二例切开后, 段 2 仍含裸 `/v1/var/` 字符串, **可能**被兜底 pattern 兜住而仍然 `exit=2` —— 这是推测, 未实测", 并只用 SC-4 的"断言返回单段"为这**两条具体用例**做了分段正确性的机制断言。

但 SC-1/SC-2/SC-3/SC-5/SC-7/SC-9 全部是"整条命令 → hook → exit code"黑盒断言, 没有任何一条断言"给定输入 → 分段器应返回的段列表"这一分段正确性本身。这正是 audit 任务描述里点名的风险: **"切错但被其他 pattern 兜住"可以让端到端断言全绿, 而分段逻辑本身是错的**。

rule6_note 引用的 `feedback_deterministic_structural_skill_rule6_substitute` memory 要求"结构性 fixture + unit-test 语料", 分段器作为本次改动的核心新增函数, 理应至少对若干代表性输入(含引号内分隔符 / 管道 / 顶层多段 / 转义分隔符)有独立于 risky_patterns 匹配结果的分段清单断言, 而不只是 SC-4 两条个案。

**建议**: 补充一组"segment(cmd) 应等于 [...]"形式的直接单元断言(覆盖至少: 纯管道保留单段 / `;`&&`\|\|` 顶层切分 / 引号内分隔符不切 / 转义分隔符不切), 与端到端 exit-code 断言并行, 不是替代关系。

### M-2 「未建模边界」清单遗漏花括号 `{ ...; }` 组与裸子 shell `(...)` 分组

Key Decision 表与 SC-7 只列了"子 shell `$(…)` / 反引号 / heredoc"三类未建模边界, 但**既有语料已经包含** `{ env; }` / `{ printenv; }`(PartB combined 两条, want=2, 已实测改前 `exit=2`)。这类花括号复合命令组内的 `;` 是否应被顶层切分, spec 未置一词 —— 若分段器天真地在花括号/圆括号内部也切分 `;`, 会产生 `"{ env"` / `" }"` 这类语法不完整的伪段(是否仍能被现有 `env` 家族 pattern 的 `[;&|(){]` 锚点类兜住取决于实现细节, 本审计未验证, 因为分段器尚未实现)。

**建议**: 把 `{ ...; }` 与裸 `(...)` 显式加入 Key Decision 表 + SC-7 的锁定清单(各补 1 条 fixture), 与 `$(...)`/backtick/heredoc 同等对待, 不要留成隐性假设。

### M-3 SC-8 的 69ms/76ms 基线数字不可移植, "基线"指代不清

在本沙箱环境实测同类场景(单条 benign 命令 vs 4 段命令, 各 20 次均值): 均为 **~140ms**, 与 spec 记录的 69ms/76ms(单条/4段)量级不同、且两者本身在本环境下几乎无区分度(测量噪声 > 分段增量, 与 bash 循环调度开销有关)。这证实 SC-8 的绝对基线数字是**宿主机相关**的。

SC-8 原文"较基线(69ms/76ms)增幅 ≤30%"未说明: Phase B 该用 spec 记录的固定数字做分母, 还是在**同一台机器**上改动前重新测一遍基线再和改动后比较相对增幅。若照字面用固定 69/76ms 作分母, 在任何比 spec 作者机器慢的宿主上都会假阳性超标(如本沙箱, 单条命令基线已是 140ms, 若在此基础上比"69ms"算增幅会直接 >100%, 但那是宿主机差异不是本次改动的性能回归)。

**建议**: SC-8 明确改为"以同一宿主机改动前立即重新测得的基线为分母", 69ms/76ms 仅作为 spec 记录的参考量级, 不作为跨机器绝对锚点。

## Minor

### m-1 `bash_case` 语料中有 1 条字节级重复用例

`"FP-fix timeout run-env" 0 'timeout 5 ./run-env-check'` 在测试文件中出现两次(name/want/cmd 三者完全相同)。不影响正确性, 但会让"305"这个基数在未来任何人工/半自动重新核对时多算 1 条冗余, 建议顺手去重。

### m-2 SC-9 的"全绿"用例总数依赖宿主机是否装 zsh

`secret-guard.test.sh` 的 zsh 端到端小节(6 条 `zsh_case`)仅在 `command -v zsh` 成立时才跑; 本沙箱装了 zsh, 实测 `PASS: 366 / 366`。没装 zsh 的宿主会是 360/360。此为既有测试架构特性(非本 spec 引入), 但 SC-9"全绿"字面对照的具体数字会因机器而异, 建议在 SC-9 或 Phase B 验收记录里注明"366(zsh 可用时)/360(否则)", 避免 CI/dogfood 机器差异被误读成回归。

### m-3 SC-7 未设定期望极性, 只是"锁定现状"而非"锁定正确性"

SC-7 原文"锁定实现后的实际 exit code…用例转红即提示该边界被触碰" —— 这是纯粹的漂移探测器, 没有断言"预期应该是 exit=2"(尽管 Key Decision 表的"不切=偏保守=可能多拦不会少拦"逻辑已经暗示三条 fixture 理应全部落在 `exit=2`)。若实现在这三个未建模边界上意外退化成 `exit=0`(即从 fail-safe 方向失守), SC-7 字面上会把这个错误值原样"锁定"为新基线, 而不会被判定为红。

**建议**: SC-7 显式写明期望值(按 fail-safe 推理应为 `exit=2`), 把它从纯漂移探测升级为正确性断言; 若 Phase B 实测真的出现 `exit=0`, 那应直接算 Critical bug 而不是"新现状"。

## 结论

SC-1/SC-2/SC-4 的改前 exit code 标注经逐条实跑核实**全部准确**; 366 总用例数、305 `bash_case` 基数经独立重算**准确**。但支撑 SC-2/SC-3"逐条列名, 不用总数代替"设计原则的具体数字(52/16/1)本身有误(应为 53/17/2), 且遗漏的那 1 条用例(`#152 FP: multiline benign`)在 SC 列表中处于覆盖真空。叠加分段器缺乏独立单元断言(M-1)、未建模边界清单不全(M-2)、性能基线不可移植(M-3), 建议 REVISE 后再进入 Phase B。
