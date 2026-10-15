你是 WP-A Spec `secret-net-l3-and-bypass-paths` 的**返修执笔实例** ({WRITER_ROLE}, 新派实例, 与上一版执笔不是同一个), 任务是把 proposal **{FROM_VERSION}** (主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 提交 `{FROM_SHA}`) 返修为 **{TO_VERSION}**, 处置 {CHECKPOINT} 第 {ROUND} 轮审计的 finding。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。主控会独立核验你的每一处改动并复跑证据脚本; 之后是第 {NEXT_ROUND} 轮五席审计 (只审 {FROM_VERSION} → {TO_VERSION} 的改动及其与未改文字的接缝, 并逐条对账本轮 finding)。

## 输入 (全部先读)

1. 当前三份文件 (主仓工作树即 `{FROM_SHA}`): `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`、`baseline_probe.py`、`baseline-evidence.md`。
2. 本轮聚合报告与五席报告原文: `{REPORT_DIR}` 下 `{CHECKPOINT}-R{ROUND}-*` 六个文件 (聚合报告的「全部 finding」表按席位原编号列出每一条; 「主控记录」节是主控的核验与处置意见 —— 其中标为「主控裁定」的条目按裁定执行, 你若有反证须写进报告而不是自行改向)。
3. 背景: 三个 issue (`{SP}/issues/aria-plugin-154.md`、`aria-plugin-203.md`、`Aria-221.md`)、决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`、四份研究笔记 `{SP}/research/*.md`、上一版执笔派单 `{SP}/dispatch/writer-v1.final.md` (其中「主控范围裁定」仍有效, 除非本轮聚合报告的主控记录另有裁定)。
4. 源码: `aria/hooks/`、`standards/conventions/` 等 (基线 aria `268da8f`、standards `2bc1c4c`)。

## 要求

1. **逐条处置**: 聚合报告「全部 finding」表里的**每一条** (含 minor) 都要有处置: `fixed` (写明改了哪里) / `rejected` (必须附你亲自核验的证据: file:line 原文或实跑命令与输出) / `deferred` (只允许用于超出本 Spec 范围、且已在「待 owner 复议」或 Out of scope 记录的事项)。多席指向同一问题的可以合并处置, 但每个席位编号都要出现在处置表里。
2. **修类不修例**: 每修一处, 问「这个形状在 proposal / 探针里还有几个兄弟位置」, 一并修掉并在报告里列出。
3. **证据只经脚本生成**: 改了 SC 就改 `baseline_probe.py`, 然后在你的实验目录新副本上实跑, 把 stdout **原样**放进 `baseline-evidence.md` 的代码块 (不手改一个字符); 基线形态 (baseline-failing 与 doc-sync 全 `no`、其余类别全 `yes`) 必须 holds; 报告里写明 stdout 的 sha256 前 16 位与字节数。新增或改写的 SC 必须先在基线上跑出预期状态再写进 proposal (「它怎么会红」三态)。
4. **不引入新的问题**: 改动越小越好; 不要借返修扩大范围。任何「改变实现者动作」的改动单列一节 (主控会重点核)。
5. **纪律延续**: Rule #7 (不出现可被现行或拟议 L1 / L3 规则命中的凭据形状字面, 一律占位写法; 夹具运行时拼装); issue 引用全限定; 编号只用 `1.` `2.` 或「第 1 类」, **不用带圈数字**; 不写 AI 署名行; 机读 token 英文 canonical; 审计叙事**不写进** proposal 正文 (Status 行只写一句当前状态, 例如「Draft — post_spec 审计中」); 头部 Level / Status / Created / Linked Issue 四行中只允许按需改 Status 一行。
6. **硬性纪律**: 你不写仓内文件、不 commit、不 push、不 fetch, 不开 issue、不发评论, 不使用 Agent 工具; 实跑只在 `{SP}/exp/{EXP_DIR}/` 下 (cp -a aria 与 standards 到那里再跑; HOME 指向该目录下的 `home/`)。三份文件与返修报告放在结构化输出里返回, 由主控落盘。

## 交付 (结构化输出)

- `proposal_markdown` / `probe_script` / `evidence_markdown`: 三份文件全文 ({TO_VERSION})。
- `writer_report_markdown`: 返修报告 (将落为 `.aria/notes/` 下的独立文件, 不进 Spec), 含: 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或拒绝证据) / 同族扫描清单 / 改变实现者动作的改动 / 证据复跑记录 (命令、sha256 前 16 位、字节数、基线形态结论) / 执笔自报薄弱点 / 请裁项 (需要主控或 owner 裁的取舍)。
- `dispositions`: 与处置表一致的结构化列表。
