# 派单: WP-A TASK-014 非作者对抗审查 (单轮, qa-engineer)

你是 Aria 仓 (`/home/dev/Aria`) WP-A Spec `secret-net-l3-and-bypass-paths` 的**实现审查席** (aria:qa-engineer, 新派实例)。

- 实现由另外两位执笔完成, 文档由第三位完成; 你和他们都不是同一个实例。
- owner 2026-10-07 裁定「实现优先 + 单轮审查」(`.aria/decisions/2026-10-07-wpa-implementation-first-owner-rulings.md` 第 22、39 行)。本次就是那一轮, 也是本 Spec 唯一的审查轮。
- 全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 任务定义

见 `openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml` 第 185–199 行 (TASK-014):

1. Spec Tasks 1.8 (`proposal.md` 第 383 行; 一行很长, 用 `sed -n '383p'` 读) 列出了一批坏实现类。每一类都由你**独立构造**至少一个, 并让对应的探针行或套件用例转红。
2. 审查实现的代码质量。
3. 本轮发现的 major 之后由实现者修, 你只复核修补处; 不会再有新一轮全审。

## 被审对象 (主控实测)

| 对象 | 基线 | 被审 |
|---|---|---|
| aria 子模块 `/home/dev/Aria/aria`, 分支 `feature/secret-net-l3-and-bypass-paths` | `268da8f` | `69af7cd` |
| standards 子模块 `/home/dev/Aria/standards`, 同名分支 | `2bc1c4c` | `be842ce` |

- **改动面**:
  - aria: `git -C /home/dev/Aria/aria diff 268da8f 69af7cd`, 共 8 个文件 (+2187 / −130)。主体是 `hooks/secret-guard.sh`、`hooks/secret-scan.sh`、`hooks/hooks.json` 与两个套件。
  - standards: `conventions/secret-hygiene.md`。
- **`69af7cd` 的 sha256 前 16 位**:
  - `hooks/secret-guard.sh` `061d15f16e7c6d39`
  - `hooks/secret-scan.sh` `77d747e63402fdbb`
  - `hooks/hooks.json` `20529435a4533428`
  - `hooks/tests/secret-guard.test.sh` `0cadad2f2a2b06ea`
  - `hooks/tests/secret-scan.test.sh` `0e009b821504520b`
  - standards `be842ce` 的 `conventions/secret-hygiene.md` `f7a8fb9363ed5d57`
- **主控在真 checkout 上的实测**:
  - 两个套件全绿: guard 783 / 783 (含 zsh 共 789), scan 122 / 122。
  - 探针验收行除 SC-26 26g 外全部 `yes`。26g 要求 `aria/CHANGELOG.md` 有对应的最上一节, 按计划在 TASK-010 落入。**本次 26g 为 `no` 是预期**, 不算 finding。

## 工作区 (只在这里改, 真仓一个字节都不动)

下文 `W` 指 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/audit/task014-qa`。

1. **参考树**: 用 `git archive` 取提交字节 (只读操作):
   ```
   mkdir -p $W/ref/aria $W/ref/standards
   git -C /home/dev/Aria/aria archive 69af7cd | tar -x -C $W/ref/aria
   git -C /home/dev/Aria/standards archive be842ce | tar -x -C $W/ref/standards
   ```
   - 取出后先核对上面的 sha256 前 16 位。
   - 探针按 `<aria>/../standards` 找 standards, 所以 aria 与 standards 必须是同级目录。
   - 基线树 (`268da8f` / `2bc1c4c`) 需要时同法取到 `$W/base/`。
2. **每个坏实现**:
   - 把参考树 `cp -a` 成一个新的同级对: `$W/mut/<id>/aria` 和 `$W/mut/<id>/standards`。aria 树约 7 MB、495 个文件, 整份拷贝不贵。
   - 只改一处, 跑完即删。
   - 不要用硬链接拷贝 (`cp -al`): 原地改写会连参考树一起改掉。
3. 运行 hook 或套件时, HOME 指向 `$W/home/`。套件自身也会隔离 HOME, 这是双保险。

## 怎么跑 (前任执笔与主控一直在用)

- **探针**:
  - 用法见 `baseline_probe.py` 第 1–60 行的文件头 (全文 245 KB, 不要整份读)。
  - 命令: `WPA_ONLY=<SC 列表> WPA_ROWS=<行号列表> python3 /home/dev/Aria/openspec/changes/secret-net-l3-and-bypass-paths/baseline_probe.py <aria 目录>`。
  - 输出写文件, 只读分组统计与相关行。
- **套件**:
  - 在 aria 目录的上一级用相对路径调用 `bash aria/hooks/tests/secret-guard.test.sh` 或 `bash aria/hooks/tests/secret-scan.test.sh`, 输出写文件。
  - 失败集合比对: `python3 /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/failset_diff.py <旧目录> <新目录>`。每个目录里放 `secret-scan.out` 与 `secret-guard.out`; 用例名以第一个 `]: ` 结尾。
  - 先在参考树上各跑一次两个套件, 作为你自己的比对基准。
- **bash 3.2**:
  - 真二进制是 `/home/dev/.aria/tools/bash-3.2.57/bash`; 探针里用 `WPA_BASH32=<该路径>` 打开。
  - 前任把整套 PATH 做成了 `.../scratchpad/impl/bin32/` (其中 `bash` 指向 3.2)。目录里有上千个软链, **不要 `ls` 它**。
  - 探针形态的套件运行方式见 `.../scratchpad/impl/work/run32.sh` 与 `runprobeform.sh`。
  - 探针形态下 guard 套件会多一条已知的「SC-13 头注释计数」假红: 没有 git 历史时 SC-8 / SC-9a 被跳过。这不是回归。
- **其它现成脚本** (都在 `.../scratchpad/impl/work/`):
  - Rule #7 扫描: `rule7_t5.sh` / `scan_file.sh`;
  - SC-32a 的 bash 4+ 构造自查: `sc32a.py`。

## 你要做的

### 1. 坏实现矩阵 (主体)

范围是 Tasks 1.8 (第 383 行) 列出的全部类别:

- 前面点名的十二种, 加「另含下列十四类」。各类后面的括号里, 是起草期点名会转红的行。
- 每个枚举集合各做一个「删掉任一成员」的缺项坏实现; 每个上界各做一个「差一」的边界坏实现。先列出你认定的枚举集合与上界清单 (带 `file:line`), 再逐个构造。
- 另外四组: W11 的自然窄化四类; 失败事件的三类 (35a–35d); 判定函数留在 source 闸门之下 (30b); 取值代码里远距离的 `#` / `##` / `%` / `%%` 删除 (34a / 34b)。

要求:

1. **独立构造**: 坏实现要像真实的错误, 即一个实现者真可能写出的写法。在正式代码 (`69af7cd`) 上改, 不在原型上改。
2. **先构造、后对照**:
   - `.aria/notes/2026-09-30-wpa-phase-a/writer-v6-proto/` 里有起草期的变异脚本与汇总 (`build_mut_summary6.py`、`dispositions_data6.py`、`cmds_*.txt` 等)。
   - **在你自己的矩阵跑完之前不要读它们**。本仓教训: 执笔自带的夹具与执笔同源盲区, 曾四轮零命中。
   - 跑完后再对照其汇总, 只看结论不同的类别, 查清原因。这就是第 383 行末句说的「复核其复现」。
3. **判红**:
   - 每个坏实现先读 Spec 里对应 SC 行的「怎么会红」, 再跑点名的探针行 (`WPA_ONLY` + `WPA_ROWS`)。
   - 点名的是套件用例时, 跑套件并做失败集合比对。
   - 记录三项: 预期转红的行 / 实际转红的行 / 是否被抓住。
4. **没被抓住的** (所有点名行与两个套件都保持绿):
   - 先再试 1–2 个变体, 确认不是构造失误;
   - 仍抓不住, 就记为 finding (验收缺口)。
5. **批量化**:
   - 把矩阵写成一个数据文件加一个驱动脚本 (用 Write 工具落文件), 一次跑一批; 不要每个坏实现都花好几次工具调用。
   - 单次前台 Bash 最长 10 分钟。超长的批次拆小, 或改用后台运行并等它的完成通知 (见「硬性纪律」的后台任务一条)。

**覆盖优先级**: 时间不够时按下面的顺序取舍。没做的必须在报告里逐项列为「未覆盖」, 不能静默略过。

1. 第 383 行点名的十二种与十四类;
2. W11 四类、35a–35d、30b、34a / 34b;
3. 枚举集合缺项与上界差一。

### 2. 重点三处 (主控与执笔留给本轮的疑问)

1. **SC-28 28f 的写法**:
   - 背景: 执笔把 Write 工具的响应形状写成 `"filePath": …, "content": …` 一行 (真实键序), 这样契约行就不以顶层 `"content":` 起头。
   - 主控的判断是「内容如实、不算迁就检查器: 该判据针对的是旧的错误 Read 形状, 对 Write 形状过宽」(`.aria/notes/2026-10-08-wpa-phase-b/PROGRESS.md` 第 227–229 行)。
   - 请独立判断两点:
     - 这算不算「挑措辞让检查器过关」。判据是: 换一个同样如实的写法 (例如键序不同、分行写), 检查器还过不过。
     - 28f 的判据本身是否过宽, 会不会对如实的文档恒红。
   - 定位: 用 `grep -n` 在 `proposal.md` 里找 SC-28 / 28f, 在 `standards/conventions/secret-hygiene.md` 里找那一行。
2. **W12 归一化循环的代价**:
   - 背景: 执笔实测代价约为「出现次数 × 命令长度」, 10.8 KB 的命令里有 500 次出现时多 0.65 s; W14 的时档表里没有 W12 这一档 (`PROGRESS.md` 第 188–190 行)。
   - 请判断: 在最坏的真实输入下, 它会不会把 L1 推过 `hooks.json` 的 5 s 超时, 而基线在同一输入上不会。
   - 测法:
     - 只比较同一输入上基线 (`268da8f`) 与被审版本的耗时比值;
     - 测量前看 `/proc/loadavg`, 一分钟值低于 2 才测 (主控派单时约 1.4)。
   - 基线 hook 本身对长命令就是超线性的 (26 KB 约 17.9 s)。这是本 Spec 之前就有的问题, 已在等 owner 定夺, **不在本次范围**; 你只量 W12 带来的增量。
3. **`_sg_per_segment_eval` 里的 `(( ${#_SGV_N[@]} ))`**:
   - 要回答: 在真 bash 3.2.57 下, `_SGV_N` 未赋值或为空数组时, 有 `set -u` 和没有 `set -u` 各是什么行为。
   - 先查两件事: hook 执行到这里时是否处于 `set -u`; 哪些路径会让 `_SGV_N` 处于未赋值状态。再在真二进制上实测。
   - 主控没有单独实测过, 只知道 bash 3.2 下全量套件通过。

### 3. 代码质量审查

范围是上面的改动面, 着重看以下几项:

- **fail-open**: 有没有错误路径让 hook 以放行告终 (报错、超时、提前 `exit 0`), 而基线在同一输入上会拦或会告警。
- **回退**: 基线能拦或能检出的输入, 现在是否仍然能。
- **误拦**: 常见的良性命令有没有被新规则拦下。
- **bash 3.2 与 locale**: 两者下是否健壮。
- **性能**: 新代码的性能上界。
- **一致性**: 注释与代码、SOT 文字与代码是否一致。

不要重写代码, 只出 finding 与建议修法。

## 严重度口径

- **critical**: 符合任一:
  - 被审版本本身相对基线有安全回退, 即基线能拦或能检出的输入, 现在被放行;
  - 有让 hook 失效放行的崩溃或挂死路径;
  - 有难以撤销的外向后果。
- **major**: 符合任一:
  - 某类坏实现让所有点名行与两个套件都保持绿 (验收缺口);
  - Spec 明写的要求没实现, 或实现反了;
  - bash 3.2 或 locale 下行为出错;
  - 常见良性命令被误拦;
  - 新代码使某个真实长度的输入越过 5 s 超时, 而基线在同一输入上不会;
  - 与 SOT 矛盾 (Spec、决策单、owner 裁定、CLAUDE.md、源码事实)。
- **minor**: 措辞、注释、可读性, 不改变行为。

一条 finding 若既不影响行为, 也不影响验收能否抓住错误实现, 最高只能是 minor。

## 证据要求

- 每条 finding 附你亲自核验的证据: `file:line` 原文片段, 或实跑命令与输出 (可截断, 不得改写)。没有证据的推测写进「风险 / 疑问」。
- 每条 finding 写清失败场景, 并回答「它怎么会红」。
- `id` = `sha256(f"{category}:{scope}:{severity}:{type}")[:8]`, 其中 scope 写成 `<相对路径>#<函数名或节名>`。

## 资源纪律 (宿主机是共享的 4 核)

你的命令已在 nice 19、只用 0–1 号核的环境下运行。这是自动继承的, 不要改回。另外:

1. 同一时刻只跑一个重负载实验。探针、套件批量、时档测量、大输入性能用例都算重负载。
2. **不跑探针全量** (TASK-010 会跑), 一律用 `WPA_ONLY` / `WPA_ROWS` 子集。
3. 模糊 / 差分用例每类不超过 30 个。
4. 时档测量只在一分钟负载低于 2 时串行跑, 结论只依据比值。
5. 不跑 `find /` 一类的全盘扫描。

## 上下文卫生 (硬要求, 直接决定成本)

- 先 `grep -n` 定位, 再用 Read 的 `offset` / `limit` 只读需要的段。
- 不整份读以下文件: `proposal.md` (240 KB)、`baseline_probe.py` (245 KB)、`baseline-evidence.md` (113 KB)、原型脚本。
- 大输出一律落文件, 只读摘要或相关行。
- 工具调用宁少勿碎。

## 硬性纪律

- **真仓一个字节都不动**:
  - `/home/dev/Aria` 及其子模块里不写任何文件;
  - 不做任何 git 写操作 (commit / push / fetch / pull / checkout / switch / stash / reset / tag / update-ref);
  - `git archive`、`git diff`、`git show`、`git log` 这类只读命令可以用。
- 不派子代理 (不得使用 Agent 工具), 不开 issue, 不发评论。
- **后台任务**:
  - 能前台跑的就前台跑。
  - 确需后台时, 等它的完成通知。不要用 `pgrep -f '<名字>'` 写等待循环: 它会匹配到等待循环自己的命令行, 永远等不完 (本会话实证, 空转了 70 小时)。
  - 交报告前确认你起的后台任务都已结束或已停掉, 并在报告里写一句「无残留后台任务」。
- **Rule #7**:
  - 不读取、不打印任何真实凭据;
  - 需要像凭据的值时, 在 Python 进程内用 `secrets` 运行时生成, 经 stdin 喂给 hook (`capture_output=True`), 绝不打印;
  - 报告只写退出码、是否告警、命中规则等元数据。
- **会话 hook 的副作用**: 会话里生效的是插件缓存里的旧版 hook, 不受被审代码影响。
  - 它会拦下 heredoc 或 `python3 -c` 命令行里仅为文字提及的敏感读取形状。这类文本先用 Write 工具落文件, 再执行。
  - 用 Bash 输出含凭据形状夹具的文本可能触发告警; 看测试文件用 Read 工具。

## 交付

1. 报告写到 `$W/report.md` (用 Write 工具)。主控核对后落到 `.aria/audit-reports/`。
2. 最后一条消息只写以下几项, 不要贴报告全文:
   - verdict 与各级计数;
   - 每条 critical / major 的一行摘要;
   - 报告路径;
   - 用量;
   - 「无残留后台任务」。

报告以下列 YAML frontmatter 开头:

```
---
checkpoint: post_implementation
mode: adversarial_single_round
rounds: 1
converged: true
oscillation: false
overridden_by_user: true
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: <写完报告时的 UTC ISO 8601 毫秒>
context: openspec/changes/secret-net-l3-and-bypass-paths/
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---
```

verdict 规则: 有 critical ⇒ FAIL; 无 critical 有 major ⇒ PASS_WITH_WARNINGS; 否则 PASS。

正文依次为:

1. `## 已实读文件` (带行号范围)
2. `## 坏实现矩阵`
   - 先附你认定的枚举集合与上界清单。
   - 然后是一张表, 每行写: 类别 (照第 383 行原词) / 坏实现 (改了哪个 `file:line`、怎么改) / 预期转红的行 / 实际转红的行 / 是否被抓住。
   - 最后逐项列出「未覆盖」的类别及理由。
3. `## 与起草期汇总对照` (只列结论不同的类别及原因)
4. `## 重点三处` (28f / W12 代价 / `_SGV_N`, 各给结论与证据)
5. `## Findings`
   - 按 critical → major → minor 排序, 编号 C1 / M1 / m1 …;
   - 每条含: `id` / severity / type / category / scope / summary / 证据 / 失败场景 / 怎么会红 / 建议修法。
6. `## 证据复跑记录` (命令、参考树 sha256 前 16 位、探针子集与套件各跑了几次)
7. `## 风险 / 疑问` (不计入 finding)
8. `## Verdict`: verdict + counts, 再加一句结论: 修完 major 之后能否进入 TASK-010 验收。
9. `## 用量`: 实际工作墙钟、探针子集次数、套件次数、坏实现个数。
