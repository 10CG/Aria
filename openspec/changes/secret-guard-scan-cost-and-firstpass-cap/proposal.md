# secret-guard 首遍扫描器 O(n²) 根治 + 扫描前风险闸门（收口 #228）

> **Level**: 2（proposal + detailed-tasks.yaml）
> **Status**: **Approved（方向 v2，设计 v2.2）** — owner 2026-10-20（B.1 实测后改向）：**先发临时闸门（R1，PATCH）再根治（R2）**；在 #228 贴更正。v1 的「`_sg_compute_credit` 入口 cap」经 B.1 实测**无效、已作废**（见 §Decision record）。fail-closed 关洞的姿态（owner 2026-10-20 拍板）不变，只换机制。
> **版本史**: v1（2026-10-20，B.1 前，按头注释归因设计）→ v2（2026-10-20，B.1 实测改写）→ v2.1（2026-10-21，TASK-002 实现复核后定案：按字节计长 / 双副本匹配 / 覆盖项目扩展 / pregate 文案 / 删 `_SG_RAW_MAX` / 跨段误拦作临时期子类接受）→ **v2.2（2026-10-21，修正轮复核：闸门自身的检测在对抗形状上超线性（F7）→ R1 照发、如实申报残余；R2 前提改正为「检测也须线性」（r2f）；清理 `_SG_RAW_MAX` / oversize 文案残留；既有缺口另立 #229 / #230）**。v1 → v2 的更正细节在 B.1 记录，不在本文（审计叙事不与交付面同居）。
> **Linked Issue**: `10CG/aria-plugin#228`（resolve）；上游 C = `secret-guard-time-budget-failclosed`（v1.76.1，已归档）；关联 `#216` `#219` `#203` `#154`。
> **证据**: `.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/`（`b1-baseline.md` 记录 + `evidence/E2–E6` + `pilot-8-32.tsv`，均由同目录脚本 `b1_run_all.sh` / `b1_curve.py` 重生成）。基线 aria v1.76.1（`59e333c`），分支 `feature/secret-guard-scan-cost-and-firstpass-cap`。

## B.1 实测（v2 的依据）

| 事实 | 数据（证据文件） |
|------|------------------|
| 主成本 = 首遍两个扫描器，逐字符 `${_cmd:_i:1}`（`:215` `:294` 在 `_sg_safe_to_split`，`:331` 在 `_sg_split_top`）→ **O(n²)**，换 C locale 仍平方级（只快 ~2.5×） | E2：UTF-8 下 safe_to_split 0.41 / 1.42 / 4.99s、split_top 0.23 / 0.80 / 2.89s @ 4 / 8 / 16KB |
| 它们在**切分之前、任何时间预算之前**对**每条**命令跑；与形状 / 是否命中密钥形无关 | pilot：良性 ≈ 密钥形（8KB 2.0–2.8s，32KB 27–31s） |
| `_sg_compute_credit` 只是次要项（仅单个长 token：+0.9s@8KB）；头注释 `:587` 的归因把它当成了主成本 | pilot：A 形密钥 vs 良性 |
| **已发布 v1.76.1 在 Linux 生产默认预算下可被绕过**：凭据读取 + 填充（单管道或**独立成段**）14KB → 首遍 ~6s → CC 5s 杀 hook → fail-open | E3：C 形 6.21s / S 形（凭据读取单独首段）5.98s |
| bash 3.2.57（macOS 系统 bash）：~3KB 以上任何命令 > 5s | E4：2 / 4 / 8KB = 2.1 / 8.4 / 34.2s |
| risky_patterns 检测循环在**实测形状**（`\| cat` 填充）上线性且快；**对抗形状超线性**（v2.2 更正，F7：E5 只测了这一种填充，「线性」是外推） | E5：bash 3.2 32KB 0.53s；bash 5.2 0.14s；密钥形命中 #28 用 0.02–0.13s。F7（E8）：60KB `curl ` 重复填充 9.6s、32KB 密集 `.environ.get(` 16.4s、60KB `;` 密集良性 6.6s |
| g-c tier（7.2KB）1.87s，几乎全是首遍扫描器（第二遍被 M6 尺寸预算快速拒绝）；#219 的 Windows 5.037s 同源 | E6 + E2 插值 |
| C 的时间预算时钟在首遍**之后**才开始（`:1542` 在 `_sg_core_eval` 之后；`_sg_vx_collect` `:633` 再重置）→ 覆盖不到首遍 | 读码 |
| 整串检测与逐段检测一致（11 种分隔符写法，含无空格 `;`） | B.1 记录 §闸门完备性 |

## Why

secret-guard 的首遍扫描器是 O(n²)，且在任何时间预算之外运行。于是：（1）**任意命令**只要足够大（Linux ~13KB、Windows 估 ~5KB、macOS bash 3.2 ~3KB）首遍就越 Claude Code 的 5s hook 超时 → fail-open；对凭据读取，填充即绕过，**填充放在哪一段都行**；（2）C 的时间预算（v1.76.1）只覆盖第二遍与 W9，**没修到 #219 的触发场景**；（3）大命令每次都要等扫描（macOS 3.2 上等满 5s）。#228 原定的 B（`_sg_vx_collect` / `_sg_compute_credit`）对 g-c 几乎无贡献。

## What Changes

### R1 — 扫描前风险闸门（临时，先发 PATCH）

在 `_sg_per_segment_eval` 的**第一条语句**（`# guard:ack` 已在主体先判并放行，闸门在其后，逃生口不变）调用 `_sg_pregate "$cmd" || return $?`。新 helper **必须定义在源码闸门之上**（SC-8 时延 harness 只 source 闸门以上；闸门以下的 helper 在 harness 里是 rc 127，测试会对空操作恒绿 —— W14 规则）：

```bash
_sg_raw_limits [MAJOR] # 每命令解析一次：_SG_RAW_GATE = 4096（MAJOR < 4 时 1536；MAJOR 缺省 = BASH_VERSINFO[0]，参数供套件测两档）；
                       # SECRET_GUARD_RAW_GATE 只能【调低】（非整数 / 空 → 默认；10# 防八进制）
_sg_bytelen STR        # → _SG_BLEN：字节长度（local -x LC_ALL=C 下取 ${#}）。扫描成本跟字节走 —— 按字符计长时，
                       # 4000 个 CJK 字符（12KB）能藏在 4096 闸门下、首遍 6s
_sg_environ_neutral S  # → _SG_NEUT：W12 的 os.environ 单键读取中和，从 _sg_judge_one 原样【抽出】（逐字节同语义，差分验证）
_sg_pregate CMD        # 0 = 继续正常判定；2 = 已拦（文案已发）
  ① _sg_bytelen；_SG_BLEN ≤ _SG_RAW_GATE → return 0（闸门惰性：与 v1.76.1 逐字节同）
  ② 中和得 _SG_NEUT；用【一次】sed 在 ; & | ) ` 前各插一个空格得「分隔副本」（文件不用 ${s//p/r}）；
     对 risky_patterns 逐条：原串【或】分隔副本命中 → _sg_emit_blocked "<原因>" "$cmd" whole pregate; return 2
     （分隔副本修「右边界紧贴 ;」的漏检：整串里 token 后面是 ;，逐段里是段尾；保留原串是为了需要 >& 之类紧贴的规则）
  ③ 项目扩展生效（_sg_ext_entries 非空）时：sub=$(_sg_ext_subst "$cmd")（扩展命中映射到内建高危路径，线性），
     对 sub 同 ② 检测，命中 → 同上拦（不调 _sg_core_eval —— 那正是 O(n²) 路径）
  ④ return 0
_sg_emit_blocked 新增 kind=pregate：中英文案如实说明「超过 N 字节且含疑似凭据读取（或 .aria/secret-guard.paths 所列路径），
  完整扫描可能超过 Claude Code 的 5s hook 超时而被放行，故拦；请拆小或用 Write 工具写文件」
  （复用 oversize 文案会写「Nothing was matched」，与拦截原因自相矛盾）
```

- **阈值推导**（取「首遍扫描在该档最慢平台 ≤ ~2s」的最大字节数）：bash ≥ 4 → 4096（E2：Linux 扫描器 @4KB ≈ 0.64s，Windows ×2.6 ≈ 1.7s）；bash < 4 → 1536（E4：@2KB 2.1s，平方外推 @1.5KB ≈ 1.2s）。超过 65536 字符的 Bash 命令**早已**被主体的既有检查拦截（基线 `:1156`），闸门不另设上限。R2 线性化后**重测重设**。
- **不变量**：闸门只**加**拦截、从不放行正常路径会拦的东西（返回 0 即落回原路径）；≤ 阈值的命令行为逐字节不变；`# guard:ack` 不变；C 的时间预算不变（R1 不动时钟）。
- **误拦面（如实）**：（a）> 阈值且含密钥形 token 的命令一律拦（即便管道到 `wc -l` 等本可得 credit 的过滤器）；（b）**整串匹配的跨段误拦**：一段里的读取动词与另一段里的敏感文件名可能被整串连起来（例：先读一个普通文档、再列出一个 dotenv 文件的两段命令，补到 > 阈值）—— R1 临时期接受，R2 扫描器线性后改用真逐段匹配。（v2 曾写「R1 新拦 > 64KB 的良性命令」—— 错，那是既有行为。）（c）**分隔副本使闸门比核心严**：超阈值时，token 紧贴 `| & )` 或反引号的写法（例：nomad var put 紧贴管道）会被闸门拦，而闸门以下的核心放行 —— 这暴露的是核心的既有漏检（右边界只认空白 / 行尾，#229），不算误拦。
- **R1 不修的（如实）**：（1）良性大命令仍要付 O(n²) 扫描时间（体验问题，超时放行无害）；（2）**变量间接**的凭据读取（原文无密钥形 token，W10 partial 类 #203）加填充仍可超时 fail-open，且闸门对它的良性全扫耗时（现实形 ≤ 0.17s @14KB）把既有放行尺寸下推约 3%；（3）**闸门自身的检测在对抗形状上超线性（F7）**：带无界间隙（`X[^|]*Y`）的行遇到大量重复 X、又没有 `|` 截断的填充，glibc 逐起点搜索 O(n·k)；W12 中和循环 O(k·n)。实测（Linux bash 5.2，UTF-8，E8）：60KB `curl ` 重复填充 + 读取 → 闸门 9.6s；32KB 密集 `.environ.get(` + 读取 → 16.4s。这些输入在基线上同样（且更早）fail-open，R1 不使其更糟；现实形状不受影响（E8：多行脚本、读取在末尾，4.7–64KB 闸门 0.01–0.06s 拦下）。以上均 R2 修（r2f）。

### R2 — 根治（线性扫描器 + 按命令累计时钟）

- **(r2a) 线性扫描器**：`_sg_safe_to_split` / `_sg_split_top` 去掉逐字符 `${_cmd:_i:1}`，改 O(n) 遍历，**判定逐字节一致**（同 safe/unsafe 结论、同段边界、同 `_SG_SEGS`）。手法由 R2 的小型 spike 在 bash 5.2 **与** 3.2 上实测择定（候选：here-string 上 `read -r -n1`；单条正则跳过非特殊字符串段；awk 移植作最后手段）。
- **(r2b) 按命令累计的时钟**：`_SG_T0` 重置移到 `_sg_per_segment_eval` 入口（闸门与 `_sg_core_eval` 之前）；删 `:1542` 的首遍后重置；`_sg_vx_collect` 的重置只在「非命令求值内」的直接调用（sourced 套件）时生效；`_sg_core_eval` 每段 `_sg_judge_one` 前加检查点。
- **(r2c) compute_credit 残余**（单个长 token 的平方项）：线性化后实测，择「修正则（b2）」或「据它设 R2 的闸门阈值」。
- **(r2d) 重设阈值**：线性化后重测，`_SG_RAW_GATE` 提到「最慢档首遍 ≤ ~2s」的新值。
- **(r2e) `_sg_vx_collect` O(vars²)**（原 b1）：线性化后实测其占比；不显著则不做（记录决定）。
- **(r2f) 检测线性化（v2.2 新增，F7）**：闸门与核心逐段判定共用的检测本身在对抗形状上超线性。（i）W12 中和改线性实现（一次 sed 或等价手法），与 `_sg_environ_neutral` 差分一致；（ii）带无界间隙的行择线性匹配手法 —— 候选：`LC_ALL=C grep -E` 的 DFA 一遍匹配全部行（与 `=~` 逐行差分，含大小写 / 换行 / GNU 扩展语义）、有界间隙、按段字节上限 —— 由 spike 在 bash 5.2 与 3.2 上实测择定。若都做不到「检出不变 + 线性」，退到**尺寸硬上限**（超过 N 字节一律拦，良性大命令也拦）：那是姿态变更，届时带数据请 owner 决定。

## Out of scope

- 不改 CC 的 5s 超时；不改 L3 `secret-scan`；不改 `_SGV_*` 语义。
- **既有检出缺口不在本 change 修**：右边界类（#229）、W9 扩展只替换前 64 处命中（#230）—— TASK-002 复核中顺带确认，另立 issue。
- **不号称挡住能写文件的对手**：guard 只看命令文本，「写文件再执行文件」本就扫不到（既有边界）。

## Success Criteria（可证伪；baseline-failing 优先）

**R1**
- **SC-G1（baseline-failing，判据=文案变体）**：`SECRET_GUARD_RAW_GATE` 调低到 64，凭据读取 + 填充到 ~200 字符 → 新版 exit 2 + **pregate** 文案；基线 exit 2 + **普通 risky** 文案。另附生产默认下的时延佐证：E3 的 14KB 输入，新版 < 1s、基线 > 5s。
- **SC-G2（防位置回归）**：> 阈值的良性命令 → exit 0（两版同）；坏实现「闸门不看命中、超长就拦」→ 红。
- **SC-G3**：已删（`_SG_RAW_MAX` 去掉 —— 默认值下是死代码，> 64KB 由既有检查覆盖）。
- **SC-G4（baseline-failing，exit；误拦面 a 的钉）**：凭据读取 `| wc -l` + 填充 > 阈值 → 新版 exit 2；基线 exit 0。
- **SC-G5（中和生效）**：> 阈值、只含 `os.environ.get(` 单键读取 → exit 0；坏实现（不中和）→ 红。
- **SC-G6（只能调低）**：`SECRET_GUARD_RAW_GATE=999999` / 非法值 / 前导零 → 生效值仍是默认。
- **SC-G7（阈值下惰性）**：典型短凭据读取 → 文案与 verdict 与基线逐字节同（非 oversize）。
- **SC-G8（bash 3.2 档）**：套件内用 `_sg_raw_limits 3` / `5` 测两档阈值（不依赖 3.2 二进制）；真 bash 3.2 实跑（~2KB 凭据读取 → pregate，bash 5 下同输入 → 普通路径）放 TASK-004 验收。
- **SC-G9（闸门完备性，对抗）**：现有套件中**每一条**正常路径会拦的命令，前后补填充到 > 阈值（多种分隔符写法，含无空格）→ 闸门必拦；漏一条即红。
- **SC-G10（多字节）**：闸门调低到 64，凭据读取 + 多字节填充，字符数 ≤ 64 < 字节数 → pregate 文案；按字符计长的实现 → 红。
- **SC-G11（分隔符紧贴）**：`cp … key`、Forgejo PAT `…/users/<u>/tokens`、`nomad var put` 三族，token 后紧贴 `;`（另含 `)`、反引号写法）补到 > 阈值 → pregate；只测原串的实现 → 红。
- **SC-G12（项目扩展）**：`.aria/secret-guard.paths` 所列路径的读取补到 > 阈值 → pregate；扩展未生效时同命令 → 非 pregate。
- **SC-G13（文案）**：pregate 文案含新措辞、不含「Nothing was matched」。
- **SC-R1**：全套件绿（计数同步）+ C 的 SC-T 系列绿 + `_sg_environ_neutral` 抽出前后差分一致。

**R2**
- **SC-L1（线性，v2.2 扩到检测）**：扫描器**与检测**（中和 + 全部行）在 32KB / 8KB 的耗时比 ≤ 5（线性 ≈ 4），输入族含良性 `| cat` 填充、`;` 密集、前缀重复填充（如 `curl ` × n）、密集 `.environ.get(`；bash 5.2 与 3.2 各自成立；Linux 32KB 整进程 < 1s（各族）。
- **SC-L2（零漂移，差分）**：旧 / 新 `_sg_safe_to_split` rc 与 `_sg_split_top` 段序列在「现有全部测试输入 + ≥10k 随机生成命令（引号 / 转义 / 分隔符 / 多字节）」上逐项一致。
- **SC-C1（累计时钟，baseline-failing）**：预算 1s，首遍慢但可得 credit（~1.5s）+ 轻量变量第二段 → 新版 time BLOCK；基线 ALLOW。
- **SC-C2**：预算 0、多段命令 → 首遍检查点 time BLOCK。
- **SC-B1（成本）**：g-c tier CPU ≤ 0.4× 基线（E6：1.87s → ≤ ~0.75s）。
- **SC-R2**：零检出回归（套件 + 现有检出语料逐条）+ C 的 SC-T + R1 的 SC-G（按新阈值）+ bash 3.2 / 5.2。

## Impact

- **版本**：R1、R2 各一个 PATCH（fail-open → fail-closed 修复 + 性能，向下兼容）；号归 owner。R2 收口 #228。
- **同步面**：aria `hooks/secret-guard.sh` + `hooks/tests/secret-guard.test.sh`（计数再同步）+ 头注释（`:587` 归因改正、`:582` 的 #216 措辞、C 时钟注释）+ `CHANGELOG`（误拦面双向申报）；standards `secret-hygiene.md`（additive 一句）。
- **披露**：#228 贴更正（owner 已批）；#154 / #219 的关单披露按 R1 / R2 实际落地更新（另请 owner）。

## Decision record（v2 现行理由，owner 2026-10-20）

1. **洞是真的、比 v1 说的更宽**：任意形状、填充放任何段都行（E3 S 形），Linux 生产默认即可复现；macOS bash 3.2 下 ~3KB 即越线（E4）。
2. **机制换成「扫描前」**：主成本在切分前的扫描器（E2），任何放在其后的 cap（含 v1 的 compute_credit 入口）触发时 5s 已耗尽；扫描前唯一便宜的东西是检测循环（E5 线性 —— 只对实测形状成立，见第 7 条），所以闸门 = 检测循环 + 尺寸。
3. **仍按命中门控**（v1 事实 3 的「门控」思路保留、位置改到扫描前）：良性大命令（≤64KB）不受闸门影响，误拦面压在「大且像密钥读取」。
4. **先闸门后根治**：闸门小、复用现有检测（文案 v2.1 起改为专用 pregate）、当天关掉直接读 + 填充的绕过；根治（线性扫描器）是正确性关键改写，需差分 + 对抗复核，周期长。
5. **v1 的三条「硬事实」更正**（详见 B.1 记录）：事实 1 面更宽（「分段救不了」是错的）；事实 2 只在平方模型下成立、R2 后反转；事实 3 的位置无效 —— 根因是照搬头注释 `:587` 的成本归因、写设计前没实测。
6. **R1 实现复核定案（v2.1）**：执笔席实测出闸门设计的 6 处问题（多字节绕过、分隔符紧贴漏检、扩展未覆盖、文案矛盾、跨段误拦、`_SG_RAW_MAX` 死代码），主控裁定前 4 处与第 6 处修、跨段误拦接受为临时期子类（经过记在 TASK-002 notes）。
7. **闸门自身超线性（F7，v2.2）**：修正轮执笔席实测、主控独立复现（E8）。主控技术裁定 R1 不加尺寸硬上限，照发并如实申报，理由：不比基线差（同样输入基线更早 fail-open）；现实形状不受影响；能构造这类填充的对手同样能「写文件再执行」（见 Out of scope）；硬上限要取 ~8KB 才稳妥，会拦 8–64KB 的良性命令，是姿态变更，归 owner —— owner 可在 R1 发版授权（TASK-005）时选「加硬上限再发」。R2 前提改正为「检测也须线性」（r2f）。根因：B.1 的 E5 只测了 `| cat` 一种填充，把形状特例外推成了「检测循环线性」。复核记录：`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/r1-task002-review.md`。
8. **可迭代**：阈值随 R2 实测重设；误拦 / 平台差异等衍生问题带数据复议（owner 2026-10-20）。

## Tasks（细粒度见 `detailed-tasks.yaml`）

R1：TASK-002 闸门实现 → TASK-003 回归 + 非作者对抗（含 SC-G9）→ TASK-004 验收 → TASK-005 发版（owner 门）。
R2：TASK-006 扫描器与检测线性化（spike + 实现 + 差分）→ TASK-007 累计时钟 + 首遍检查点 → TASK-008 compute_credit 残余 / vx_collect / 重设阈值 → TASK-009 回归 + 对抗 → TASK-010 验收 → TASK-011 发版 + #228 收口（owner 门）。
