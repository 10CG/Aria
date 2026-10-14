# 派单: WP-A TASK-014 修补复核 (新 qa-engineer, 只复核修补处)

> 新派 aria:qa-engineer 实例 (非原审查席 —— 原席上下文 91 万已过期)。**只复核 TASK-014 的修补处, 不开新一轮全审** (TASK-014 定义: 「发现的 major 由实现者修完、审查者只复核修补处」)。
> `impl-handover.md` §5 纪律继续适用: 上下文卫生 (按行号/锚点读, 别整份读 proposal/baseline_probe/原型)、资源 (nice 19 + 0–1 核, 套件是功能门无须等 load<2)、真仓不做 git 写、不派子代理、不开 issue、不发评论。

## 复核对象 (aria `feature/secret-net-l3-and-bypass-paths`)

审查基线 `69af7cd` (W9+W10 落地态) → 最终 `52d0964`。三个修补 commit:
- `1902218` M6 原始 (W10 串长预算, 当时 fail-open)
- `626e567` B (其余 7 条 major 补用例, 两测试文件)
- `52d0964` M6-rework (W10 超限改 **fail-closed** = 拦截+提示拆小, owner 2026-10-14 裁定; 翻转 21aa-21ap)

审查报告 `.aria/audit-reports/post_implementation-R1-2026-10-11T142603-595Z-secret-net-l3-and-bypass-paths-qa-engineer.md` (8 major 锚点 M1@297 M2@312 M3@331 M4@348 M5@374 M6@396 M7@428 M8@449)。**每条只读对应段**。
审查席旧 mutant 产物 (参考, 但你**自己独立重建**坏实现 —— 同源盲区): `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/audit/task014-qa/`。两位执笔的产物在 `.../scratchpad/m6/`、`.../scratchpad/fixb/`、`.../scratchpad/m6rw/` (同样只作参考)。

## 要复核的 (8 条 major 的修补是否成立)

对**每条 major**: 独立重建该类坏实现 (精确文本替换, 每处改动断言恰好生效一次), 确认 (a) 对应用例在当前正确 hook/52d0964 上**绿**; (b) 在你的坏实现上**红**。不要重跑全 667 mutant 语料, 聚焦这 8 类 + 下面的专门裁决。

- **M6 (fail-closed, 改了 hook)**: 重点。确认 ① W10 三超限点 (值/副本/合计) 越界时**拦截** (rc=2 + oversize 文案), 不是放行; ② 真阳性检测未坏 (界内 + 小命令里的密钥仍以**真阳性**文案拦, 与 oversize 文案区分); ③ 有界 (几何链 / 密集 16×300×8 仍 <5s, 现 rc=2); ④ 翻转前的 fail-open 坏实现 (超限仍放行) 让 21aa-21ap 转红。
- **M1**: 把任一「判定入口可达但 30b 未检」的函数/变量初始化挪到闸门下 → 强化后的 30b 转红。
- **M2 / M3 / M4 / M5 / M8**: 各类坏实现 (命令位置/关键字/时长漂移; /proc 删读取器; 各界 ±1; 扩展命中后 eval / _value_of URL eval; Read/Edit 面 `grep -qFi`→`-qEi`) 在对应 SC-R1M* 用例上转红。

## 专门裁决 (执笔与审查席/派单有分歧处 —— 你来定)

1. **M7 方向之争**: 审查报告写「漏报方向, 由 10i 抓 `auth-header-token`/`cli-secret-flag` 缺项」; 执笔 B 实测是**误报方向**, 且称从 NEW_TAGS 删这两个 tag 后 W2/W3 全绿 (10i 抓不到), 故做成**六 tag 全矩阵** (`SC-R1M7a`)。**复跑两方**: 10i 到底抓不抓得到这两个 tag 的缺失? B 的六 tag 矩阵是否覆盖了审查席真正指的缺口? 给结论。
2. **等价 mutant (执笔称不可杀)**: scan `count>199` (对任何 count 同 `>200`)、`FP_N<11` (`_fp_push` 自封顶 10)、tight 三拷贝之一删 `(`/反引号 (三拷贝 or 关系)。确认这些**确实行为等价、无法转红** (= 非测试缺口), 还是执笔漏构造。
3. **M2f 一致性断言**: 执笔超出派单加的「规则行==拷贝文本」断言。确认它是**真守卫** (拷贝漂移时转红), 不是恒真的 author-to-match-checker。
4. **M6 误拦面 (#217)**: 确认 fail-closed 的误拦面与记录一致 (>8192 字符且引用变量的命令被拦, 含多行 for 循环), **不比记录更糟**; #217 已记收窄项, 你只需确认现状如实, 不必修。

## 验收 / 报告格式 (报告给原文输出)

1. 两套件从 `/home/dev/Aria` 调 `bash aria/hooks/tests/secret-*.test.sh` 全绿原文 (guard 816/816 无 zsh、scan 129/129)。
2. 逐 major 复核表: major → 你独立重建的坏实现 → 基线绿 → 坏实现红 (或「修补不足, 缺口仍在」+ 证据)。
3. 四条专门裁决的结论 (尤其 M7, 给复跑证据)。
4. bash 3.2.57 (`bash -n` + 新用例在 3.2 下过); Rule #7 (若你新增扫描行, 带正控)。
5. 结论: 8 条 major 的修补是否全部成立 (PASS / 哪条仍有缺口)。**若某修补不足, 只报出来给主控派定向修, 不自行改、不开新一轮全审。**
6. 用量: 墙钟、全量套件次数、你构造的 mutant 数; **交报告前列停自己的后台任务, 写「无残留后台任务」** (kill -0, 不用 pgrep -f 等待循环)。
