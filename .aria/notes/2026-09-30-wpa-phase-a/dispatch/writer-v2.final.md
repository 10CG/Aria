你是 WP-A Spec `secret-net-l3-and-bypass-paths` 的**返修执笔实例** (backend-architect, 新派实例, 与上一版执笔不是同一个), 任务是把 proposal **v1** (主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 提交 `47aa15f`) 返修为 **v2**, 处置 post_spec 第 1 轮审计的 finding。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。主控会独立核验你的每一处改动并复跑证据脚本; 之后是第 2 轮五席审计 (只审 v1 → v2 的改动及其与未改文字的接缝, 并逐条对账本轮 finding)。

## 输入 (全部先读)

1. 当前三份文件 (主仓工作树即 `47aa15f`): `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`、`baseline_probe.py`、`baseline-evidence.md`。
2. 本轮聚合报告与五席报告原文: `/home/dev/Aria/.aria/audit-reports` 下 `post_spec-R1-*` 六个文件 (聚合报告的「全部 finding」表按席位原编号列出每一条; 「主控记录」节是主控的核验与处置意见 —— 其中标为「主控裁定」的条目按裁定执行, 你若有反证须写进报告而不是自行改向)。
3. 背景: 三个 issue (`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-154.md`、`aria-plugin-203.md`、`Aria-221.md`)、决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`、四份研究笔记 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/*.md`、上一版执笔派单 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/dispatch/writer-v1.final.md` (其中「主控范围裁定」仍有效, 除非本轮聚合报告的主控记录另有裁定)。
4. 源码: `aria/hooks/`、`standards/conventions/` 等 (基线 aria `268da8f`、standards `2bc1c4c`)。

## 要求

1. **逐条处置**: 聚合报告「全部 finding」表里的**每一条** (含 minor) 都要有处置: `fixed` (写明改了哪里) / `rejected` (必须附你亲自核验的证据: file:line 原文或实跑命令与输出) / `deferred` (只允许用于超出本 Spec 范围、且已在「待 owner 复议」或 Out of scope 记录的事项)。多席指向同一问题的可以合并处置, 但每个席位编号都要出现在处置表里。
2. **修类不修例**: 每修一处, 问「这个形状在 proposal / 探针里还有几个兄弟位置」, 一并修掉并在报告里列出。
3. **证据只经脚本生成**: 改了 SC 就改 `baseline_probe.py`, 然后在你的实验目录新副本上实跑, 把 stdout **原样**放进 `baseline-evidence.md` 的代码块 (不手改一个字符); 基线形态 (baseline-failing 与 doc-sync 全 `no`、其余类别全 `yes`) 必须 holds; 报告里写明 stdout 的 sha256 前 16 位与字节数。新增或改写的 SC 必须先在基线上跑出预期状态再写进 proposal (「它怎么会红」三态)。
4. **不引入新的问题**: 改动越小越好; 不要借返修扩大范围。任何「改变实现者动作」的改动单列一节 (主控会重点核)。
5. **纪律延续**: Rule #7 (不出现可被现行或拟议 L1 / L3 规则命中的凭据形状字面, 一律占位写法; 夹具运行时拼装); issue 引用全限定; 编号只用 `1.` `2.` 或「第 1 类」, **不用带圈数字**; 不写 AI 署名行; 机读 token 英文 canonical; 审计叙事**不写进** proposal 正文 (Status 行只写一句当前状态, 例如「Draft — post_spec 审计中」); 头部 Level / Status / Created / Linked Issue 四行中只允许按需改 Status 一行。
6. **硬性纪律**: 你不写仓内文件、不 commit、不 push、不 fetch, 不开 issue、不发评论, 不使用 Agent 工具; 实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2/` 下 (cp -a aria 与 standards 到那里再跑; HOME 指向该目录下的 `home/`)。三份文件与返修报告放在结构化输出里返回, 由主控落盘。

## 交付 (结构化输出)

- `proposal_markdown` / `probe_script` / `evidence_markdown`: 三份文件全文 (v2)。
- `writer_report_markdown`: 返修报告 (将落为 `.aria/notes/` 下的独立文件, 不进 Spec), 含: 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或拒绝证据) / 同族扫描清单 / 改变实现者动作的改动 / 证据复跑记录 (命令、sha256 前 16 位、字节数、基线形态结论) / 执笔自报薄弱点 / 请裁项 (需要主控或 owner 裁的取舍)。
- `dispositions`: 与处置表一致的结构化列表。

## 本轮补充说明 (主控)

- 研究笔记已入仓: `.aria/notes/2026-09-30-wpa-phase-a/research/` (secret-guard.md / secret-scan.md / precedent.md / cc-hooks.md); proposal 里所有对研究笔记的引用改指这些仓内路径 (簇 I)。上一版执笔的自报薄弱点、待 owner 复议与设计取舍在 `.aria/notes/2026-09-30-wpa-phase-a/writer-reports/v1-writer-meta.json`。
- 主控裁定 11 条见 R1 聚合报告的「主控记录」节, 按裁定执行。
- 一个现成的用例: 本轮五席报告里有 4 份会被**现行** secret-scan 的 `json-secret-field` 命中, 命中的都是占位描述 (例如 `"password":"<16 位混合值, 首字符 $>"`、`"password":"$2b$12$…"`)。W3 返修后: 文档里这类占位要静默, 而真实形态 (完整长度的 crypt 口令哈希、`$` / `<` 开头的随机值) 仍须检出 —— 两面都要有 SC 行。
- 体量: v1 已 365 行 / 326 个用例行, 被一席判「可能规格膨胀」。返修以「收紧」为主, 不要靠堆用例行来回应 finding; 能用一条更强的判据替代多条弱判据的, 优先替代。
- 写含敏感形状讨论的文件内容时, 在你的实验目录里用 Write 工具或脚本文件, 不要用 `python3 -c` / heredoc 把这类文字放在命令行上 (现行 secret-guard 会拦, 主控本轮就撞上一次)。
