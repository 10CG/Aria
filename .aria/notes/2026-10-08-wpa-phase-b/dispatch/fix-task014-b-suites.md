# 派单: WP-A TASK-014 修补 B — 其余 7 条 major 补用例 (guard + scan 两套件)

> 新派 aria:backend-architect 实例。**只补测试用例, 不动 hook 代码**, 做完报告停下。
> `impl-handover.md` 全部纪律继续适用 —— 尤其 §5 (上下文卫生: 只按行号/锚点读, 不整份读 proposal/baseline_probe/原型; 资源: nice 19 / 0–1 核; 真仓内不做 git 写, 提交由主控做; 不派子代理 / 不开 issue / 不发评论) 与 §3 验证法 + Rule #7。本任务套件是功能门 (断退出码), 不是时档, 无须等 load<2。

## 现状 (A 已落地)

- 执笔 A 已修完 **M6** 并落地: aria 子模块 `feature/secret-net-l3-and-bypass-paths` 现在 `1902218` (W10 第二遍串长预算)。你在这个树上工作。guard 799/799, scan 122/122 是你的起点绿值。
- 审查报告: `.aria/audit-reports/post_implementation-R1-2026-10-11T142603-595Z-secret-net-l3-and-bypass-paths-qa-engineer.md`。**每条 major 只读它那一段** (锚点见下), 别整份读。
- 审查席产物 (参考, 但坏实现要**自己独立重建** —— 同源盲区): `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/audit/task014-qa/` (`mut/` 坏实现、`out/res_*.jsonl`、`bin/`)。

## 任务本质 (先读懂再动手)

这 7 条 major **都是覆盖缺口, 不是代码 bug**: 当前 hook 行为正确, 但审查席构造的坏实现 (mutant) **没有任何现有用例能让它转红**。你的活是**补用例, 使每一类坏实现转红**。

- **不要改 `secret-guard.sh` / `secret-scan.sh`**。若你发现某一类**无法只靠测试转红** (即它其实是活的代码 bug, 当前 hook 真会漏/错), **停下来写进「请裁」, 不要私自改 hook**。这是主控/owner 要知道的发现。
- 每条新用例必须同时满足 (§adversarial-fixture + §test-claims-vs-verifies):
  1. 在**当前正确 hook** (1902218 工作树) 上**绿**;
  2. 在你**独立重建**的该类坏实现上**红**;
  3. 注释写明它钉的是哪一类坏实现 (「它怎么会红」)。
- 坏实现用**精确文本替换**构造, 每处改动**断言恰好生效一次** (静默没改成会读成假「缺口」); 可参考审查席 `mut/`, 但自己重建。坏实现按**函数/模式 grep 当前树定位**, 别用报告里的旧行号 (A 在闸门上加了约 28 行, 闸门下的行号已位移)。

## 7 条 major → 文件 / 类 / 坏实现形态举例 (自己重建)

报告锚点 (`**M<n> — id ...**`): M1@297, M2@312, M3@331, M4@348, M5@374, M7@428, M8@449; 深挖 "删掉任一成员"@134, "上界差一"@155。Minor@465 只作背景, **本次不修**。

1. **M1 (guard)** — 强化既有用例 **30b**。现在 30b 只能发现 `_sg_core_eval` / `_sg_vx_pass` 落到 source 闸门 (`[[ BASH_SOURCE != $0 ]]`) 之下, 另外 9 个 `_sg_judge_one`/`_sg_per_segment_eval` 经辅助间接调用的函数/初始化发现不了 (用例名声称的比它验证的多, 564 行注释是契约本体)。
   - 改法: 让 30b 断言**从判定入口可达的每一个函数** (含 564 注释列的 `_sg_emit_blocked` / `_sg_ext_*` / `_SGV_*` 初始化等) 都在闸门之上。
   - 坏实现: 把其中任一个当前未被检查的函数/初始化挪到闸门之下 → 30b 必红。

2. **M2 (guard)** — tight 拷贝漂移。命令位置字符类 (`(^|[;&|(){]|...`)、关键字、launcher 时长后缀 (共 14 形), 以及 `ps -O` / 末位 `-u` 的「操作数只认首个」(2 形), 删任一不转红。
   - 坏实现举例: 命令位置类去掉 `;` (grep 当前树定位该类); 去掉某关键字; 改 launcher 后缀。每个子形至少一个代表性坏实现 + 对应用例。

3. **M3 (guard)** — `/proc` 读取器加宽组 (`cat|head|tail|less|more|strings|hexdump|od|xxd|tr|awk|perl|rev|xargs|…`, grep `proc` 定位该交替组) 删任一基线读取器 (12) 不转红。
   - 坏实现: 从组里删 `tail` (或任一读取器) → 该读取器触发 `/proc/.../environ` 的用例必红。每个读取器一条用例。

4. **M4 (guard, 可能含 scan)** — 上下界差一约 16 个: 200-span 帽、kv 键 `{0,64}`、cli 旗标 `{0,40}`、路径形斜杠数、W10 `for` 帽与 `${}` 替换帽、PEM 指纹循环。
   - 坏实现: 把某个界 ±1 (`{0,64}`→`{0,63}`, span 200→199)。
   - 用例: 在**界上 (绿) 与界+1 (红)** 两点各一条, 使差一 mutant 在边界点转红。

5. **M5 (guard + scan)** — 「不执行」不变量两处洞:
   - (a) guard: 命中扩展条目**之后**对命令文本求值 (现 19ab 只测未命中)。坏实现: 在扩展命中分支插 `eval`。用例: 命中路径 + 一个「只有被 eval 才会发生的副作用」(金丝雀文件), 断言金丝雀**未**被建 (正确 hook 绿, eval mutant 红)。
   - (b) scan: `_value_of` 的 URL 分支求值 (现 7n 不含 URL 类)。坏实现: 在 URL 分支插 eval。用例同理, scan 套件里。

6. **M7 (scan)** — L3 逐 tag 分类范围: `json-env-secret-key`、`cf-access-client-secret`、jq `paths`/`leaf_paths`、W8 左边界 `_ . -` 缺项不转红 (都是**漏报**方向)。
   - 坏实现: 从逐 tag 分类表删某 tag / 删 W8 左边界某字符。
   - 用例: 每个 tag / 边界一条 detection 用例 (`expect_detect`), 删该项的 scan mutant 上转红。

7. **M8 (guard)** — Read/Edit 面扩展条目的「**字面子串**」性没有任何行 (定位 `_sg_ext_path_pass` 的 `grep -qFi`)。
   - 坏实现: `grep -qFi` → `grep -qEi` (按 ERE 匹配而非字面)。
   - 用例: 用一个含正则元字符的扩展条目 (如 `x[1]y.txt`): 对字面路径 `/srv/x[1]y.txt` 应命中、对 `/srv/x1y.txt` 不应命中; ERE mutant 会把 `x[1]y` 当字符类 → 两条断言之一翻转 → 红。

## 计数 / census

- 补用例会改两套件头计数 (guard 现 `805 (799 无 zsh)`, scan 现 `122`)。**两处头注释都同步**。
- 跑 `aria/hooks/tests/corpus_census.py` (权威计数器, 覆盖 TASK-008/009/010 族分组); 若族数/分组因新用例变化, 按它的输出同步, 报告里给 census 前后差。

## 交付物

1. `aria/hooks/tests/secret-guard.test.sh`: M1 / M2 / M3 / M4(guard 部分) / M5(a) / M8 用例。
2. `aria/hooks/tests/secret-scan.test.sh`: M5(b) / M7 (及 M4 若有 scan 侧) 用例。
3. 两套件头计数 + `corpus_census.py` 同步。
4. **不改任何 hook 源** (改了就是越界, 写进请裁)。

## 验收 (报告给原文输出)

- 两套件从 `/home/dev/Aria` 调 `bash aria/hooks/tests/secret-*.test.sh`: guard 新总数全绿、scan 新总数全绿、FAIL 0、新增失败 0 (用 `failset_diff.py` 比对 A 落地态基线)。
- **逐用例红证**: 一张表 (用例 id → 钉的坏实现类 → 基线上绿 → 你的 mutant 上红); mutant 独立重建, 每处改动断言恰好生效一次。
- bash 3.2.57: `bash -n` 两文件过; 新用例在 3.2 hook + 3.2 套件下通过; 改动行 SC-32a 自查 (脚本见 handover §3.6)。
- Rule #7: 新增行用基线与当前 `secret-scan.sh` 各扫一遍零命中, 带运行时生成的正控 (handover §5 脚本)。
- census: `corpus_census.py` 输出 + 头计数 old→new + 族分组差。

## 报告格式

1. 逐 major 补的用例 (文件、SC id、钉的坏实现类、红证)。
2. 两套件 PASS/FAIL 原文 + `failset_diff` 结果。
3. census 前后差 + 两处头计数。
4. bash 3.2 + Rule #7。
5. 请裁 / 冲突 / 偏离 (**没有写「无」**; 尤其: 哪条若其实是代码 bug 而非覆盖缺口、哪条做不到既绿又红)。
6. 用量: 实际工作墙钟、全量套件次数; **交报告前列出并停掉自己起的后台任务, 写明「无残留后台任务」** (不用 `pgrep -f` 写等待循环, 用 `kill -0 "$pid"` 或括号写法)。
