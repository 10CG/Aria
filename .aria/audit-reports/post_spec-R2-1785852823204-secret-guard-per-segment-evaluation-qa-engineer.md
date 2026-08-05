---
verdict: REVISE
agent: qa-engineer
round: R2
critical_count: 1
major_count: 0
minor_count: 2
r1_resolved: 5/7
---

# post_spec R2 — QA 审计 (convergence 复审): secret-guard-per-segment-evaluation

审计对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (owner 裁定缩范围后版本, 只切顶层 `;` `&&`)
方法: canonical `aria/hooks/secret-guard.sh` **直调** (不经仓内 harness, 规避 Aria#172 陈旧 cache); 用 R1 同款「改 `bash_case` 函数体 dump JSON 后照常调用 `run_case`」技术精确抽取 305 条命令字面值; 独立写**两套互不复用代码的** quote-aware 顶层分隔符扫描器 (`scan.py` 状态机 / `scan2.py` token 流), 交叉验证结果完全一致 (0 处分歧), 用于对抗单一实现的自我复现偏差。

## 1. R1 (1C+3M+3m) 核销

| # | R1 结论 | R2 处置 | 证据 |
|---|---------|---------|------|
| C-1 | SC-2/SC-3 数字(15/52)与独立复算(53/17/2)不一致, 遗漏 `#152 FP` | **未解决 (以新形态复发)** — 见下 §2 新 Critical | 双扫描器复算 |
| M-1 | 除 SC-4 外全是端到端断言, 无分段器直接单元测试 | **已解决** — Task 1.3 + SC-5 新增 8 条 `split_top_level()` 直接断言 (数组基数, 非 `wc -l`) | 读 proposal.md SC-5 |
| M-2 | 「未建模边界」清单遗漏 `{ …; }` 与裸 `(...)` | **已解决 (转出#2)** — 且实测验证转出理由本身成立: `{ nomad var put p @f; } >/dev/null` 整体 exit=0(重定向护体), 天真切分后段 1 `' { nomad var put p @f'` 变 exit=2 = 真实「安全写法翻红」; 同时验证 `{ env; }`/`{ printenv; }` 两条现有回归用例切分后仍 exit=2, 不破 SC-3 | 实测 (见 §3) |
| M-3 | SC-8 绝对基线(69/76ms)不可移植 | **已解决** — SC-8 改「相对同机即时基线, 20 轮取中位数, ≤50%」; 本沙箱实测 n=20 中位数法 (单条 vs 4段, 均未改动) 相对差仅 **-5%**, 远低于 R1 单轮 92% 散布, 阈值有合理裕度 | 实测 (见 §4) |
| m-1 | `bash_case` 语料 1 条字节级重复("FP-fix timeout run-env") | **静默丢弃** — 本版全文无一处提及, 语料实测仍重复(行 641/673) | grep 核实 |
| m-2 | SC-9"全绿"总数依赖 zsh 在场 | **已解决** — SC-11 显式"总数须注明 zsh 在场与否(366 vs 360)" | 读 proposal.md SC-11 |
| m-3 | SC-7 未设定期望极性, 只锁现状不锁正确性 | **已解决 (设计优于 R1 建议)** — SC-7 改为显式断言"改后 exit=0" + honest KNOWN-LIMIT 标注, 而非 R1 原建议的"应为 exit=2"(该建议与本版缩范围后的固有跨段 fail-open 机制冲突, 不可达); 实测 `set -o posix; set \| grep foo` 整体 exit=2, 两段独立求值均 exit=0, 证实 2→0 机制成立且 SC-7 断言值(0)与机制一致 | 实测 (见 §3) |

**r1_resolved = 5/7** (M-1/M-2/M-3/m-2/m-3 解决; C-1 以新形态复发, 未真正解决; m-1 静默丢弃)。

## 2. Critical (新): Impact 表"口径已统一"后数字仍与独立复算不一致 — C-1 的第二次复发

proposal.md 第 106 行称"口径已统一"("顶层 `;` `&&` `\|\|` `\|`"), 并列出**已定案**的 `68 / 52 / 16(15+1)`。但用两套独立实现(状态机 + token 流, 交叉验证零分歧)对精确抽取的 305 条 `bash_case` 重新扫描:

| 分类 | proposal.md 声称 | 独立复算 (双扫描器一致) |
|------|----|----|
| 305 条中含顶层 `;`/`&&`/`\|\|`/`\|` | 68 | **65** |
| ├ `expected=2` | **52** | **49** |
| └ `expected=0` | 16 | 16 (**一致**) |
| &nbsp;&nbsp;├ 纯管道 | 15 | 15 (**一致**) |
| &nbsp;&nbsp;└ 含真命令边界 | 1 | 1 (**一致**) |

`expected=0` 一侧(含 SC-2 的 15+5=20 条)**逐条实跑核实完全准确**(见 §3), 说明本次数字错误**局限于 `expected=2` 侧**, 与 R1 C-1 当时"仅 want=0 侧遗漏 1 条"的错误形态不同 —— 这是一次**新的、独立的**计数错误, 不是同一个错误的延续。

**可能根因**(供收口者定位, 非断言): 语料中有 5 条 `want=2` 用例的命令字面值里含裸 `;`/`\|` 字符, 但该字符实际处于单引号/双引号**内部**(如 `ssh root@host 'find / -name .env.production -exec cat {} \;'` / `python3 -c 'import urllib.request; ...'` / `kubectl exec pod -- sh -c 'env\|cat'` 等) —— 若沿用非 quote-aware 的粗略计数(如裸 `grep -c` 或人工目测), 这 5 条极易被误判为"顶层含分隔符"。`49 + 3 = 52` 恰好吻合"5 条候选中误记 3 条"这一假说, 但**未在候选 5 条中定位到具体是哪 3 条**(需收口者用等价脚本自行复现, 不应再次依赖人工计数 —— 本 spec 头部已明确记录同一作者在同一 cycle 内**三次**类似数字错误: 141→139 回退 / R1 三方 68 vs 72 vs 53 互斥 / 本次 52 vs 49, 无一次由作者自查发现)。

**为何这条必须判 Critical**: SC-3 原文把 `52` 写进验收标准本体("52 条含分隔符的 `expected=2` 用例改后仍 `exit=2`"), 若 Phase B 实现者按文字"52"去核对/统计覆盖率而非重新机械枚举, 会产生一个**目标数字本身就错**的验收基线; 且这正是本 spec 头部反复强调"无一由作者自查发现"的**同类模式**在 post-owner-narrowing 版本里的第三次实例 —— 审计存在的意义就是拦住这类模式, 拦不住即为失职。

**处置建议**: Phase B 实现前, 用**提交进仓库的**脚本(而非本报告这种一次性 scratchpad 脚本)重新机械枚举并把 65/49/16 或复核后的确数写回 Impact 表与 SC-3, 使其可被任何人重跑复现(而不是第三次"信作者复算")。

## 3. 逐条实跑结果 (canonical 直调, 全部核实通过)

**SC-1 (4 条, 管道形态已移出)**:

```
cat /opt/.env; echo hi >/dev/null                          exit=0  (改前, 一致)
nomad var put p1 @f1 >/dev/null; nomad var put p2 @f2       exit=0  (改前, 一致)
vault read secret/x; nomad var put p @f >/dev/null          exit=0  (改前, 一致)
nomad var get nomad/jobs/x && echo done >/dev/null          exit=0  (改前, 一致)
对照: cat /opt/.env                                          exit=2
移出验证: cat /opt/.env | head -5 >/dev/null                exit=0 (管道不切, 改前改后均 0 → 移出 SC-1 正确, 它不属于"baseline-failing")
```

**SC-2 (15 纯管道 + 5 换行边界 = 20 条, 逐条可执行)**: 20/20 全部核实, 改前 exit code 与 spec 声称完全一致(15 条纯管道全 `0`; 4 条换行边界 `2`, 含 `#152 FP: multiline benign` 为 `0`)。20 条命令名与字面值均可在 `hooks/tests/secret-guard.test.sh` 现有语料中精确定位, 无需新增 fixture。

**SC-4 (3 条, 含新增可证伪 fixture)**:

```
ssh find env                                exit=2  (改前, 一致)
python -c HTTP wrapper                      exit=2  (改前, 一致)
新增: python3 -c 'import os; print(open("/opt/.env").read())'   exit=2  (改前, 一致)
```

**新增 fixture 的可证伪性构造验证**(手工构造"切错版" —— 模拟若在引号内 `;` 处误切会发生什么): 把整条命令在 `import os` 后面那个引号内 `;` 处硬切成两段, 分别单独喂给 hook:

```
段 1: python3 -c 'import os                          exit=0
段 2:  print(open("/opt/.env").read())'               exit=0
```

两段均 `exit=0`。深挖机制: `python3` 段命中不了 pattern `python3?[[:space:]]+-c[^\|]*(...\|\.env\|...)` —— 因为该 pattern **要求 `python3 -c` 与 `.env` 落在同一段**, 段 1 有 `-c` 无 `.env`, 段 2 虽字面含 `/opt/.env` 但缺 `-c` 前缀, 两段各自都凑不齐同一条 pattern 的完整锚点。**证实**: 该 fixture 确系"切错必 exit=0"的真锚点, 非空断言 —— proposal.md 该条描述完全准确。

**转出 #2 (`{ …; }` 整体重定向) 的实测验证** (非 SC 义务项, 但用于判定 M-2 转出理由是否站得住):

```
{ nomad var put p @f; } >/dev/null           exit=0   (整体, 现状)
' { nomad var put p @f'  (天真切分段1)        exit=2   ← 安全写法翻红, 证实转出#2 的"5/5 误伤"论证成立
' } >/dev/null'          (天真切分段2)        exit=0
{ env; }                                      exit=2   (整体, 现状 = SC-3 语料内既有用例)
' { env' (天真切分段1)                        exit=2   ← 未破坏, SC-3 该条不受影响
' }' (天真切分段2)                            exit=0
```

**SC-7 KNOWN-LIMIT 实测**:

```
set -o posix; set | grep foo   (整体, 改前)    exit=2
set -o posix                    (天真切分段1)  exit=0
set | grep foo                  (天真切分段2)  exit=0
```

证实"跨段 fail-open, 2→0"机制成立, SC-7 断言的"改后 exit=0"与机制预测一致。

## 4. SC-8 相对基线阈值实测 (非阻断项, 供参考)

同一沙箱、零代码改动前提下, 对单条 benign 命令与 4 段 `;` 命令各跑 20 轮取中位数: A(单条)=177ms, B(4段)=168ms, 相对差 **-5%**。远低于 R1 记录的单轮 92% 散布, 证实"n=20 中位数"这一方法学选择本身已大幅压低噪声, ≤50% 阈值在本环境下有合理裕度、不会被测量噪声本身触发假红。**Minor 观察**(非阻断): `has_filter` 13 处 subprocess(转出#6)在真实分段实现后会随段数线性增多 fork 次数, 若某条多段命令恰好命中多个 `has_filter` 分支, 实测增幅可能高于本次基线噪声实验反映的量级 —— 建议 Phase B 拿到真实实现后第一时间用 SC-8 方法复测, 若逼近 50% 视为转出#6 提前收口的信号, 不必现在动 spec。

## 5. SC 完整性判断

缩范围后 SC-1~SC-11 逐条复核: 均非真空成立(vacuously true)、均有鉴别力 —— SC-1/SC-3/SC-7 有真实的"会变"预期(0→2 或 2→0), SC-2/SC-5 是有具体反例可失败的回归锁/单元断言, SC-4 经手工验证具备真实的可证伪性(非空摆设), SC-6/SC-9/SC-10/SC-11 是未来 Phase B 产物上的机械可判定项。集合完整性上未发现遗漏的边界类别(转出 1-7 覆盖了 R1 暴露的全部子问题面)。**唯一缺口是 §2 的数字准确性 Critical**, 不是覆盖面缺口。

## 6. Minor (新)

**m-1(R1) 静默丢弃**: 语料 1 条字节级重复(`"FP-fix timeout run-env"`, 行 641/673)本版未提及、未修、未转出。影响极小(不影响正确性), 但按"静默丢弃=finding"判据仍需记录, 建议顺手清理或至少在 Tasks 补一行。

**SC-8 阈值前瞻观察**: 见 §4, 非阻断, 建议 Phase B 落地后第一时间复测。

## 结论

R1 的 1C+3M+3m 中 5 项(M-1/M-2/M-3/m-2/m-3)已妥善解决, 其中 M-2/m-3 的解决方式优于 R1 原始建议(用实测重新校准了转出理由与断言极性, 而非机械照做)。但 C-1 的核心症状——"SC 验收标准里的硬编码数字与独立机械复算不一致"——在"口径已统一"的包装下**以新形态复发**: `expected=2` 桶从 52 变为独立复算的 49(总数 68→65), want=0 桶(15+1=16)本次核实完全准确。叠加 m-1 静默丢弃, 判定 **REVISE**。收口路径明确且范围小: 重新用可复现脚本机械核对 Impact 表与 SC-3 的确数并回填, 顺手清理 m-1 重复用例; 不影响本版"仅切顶层 `;`/`&&`"的范围决策与其余全部设计结论。
