你是 WP-A Spec `secret-net-l3-and-bypass-paths` 的**返修执笔实例** (backend-architect, 新派实例, 与上一版执笔不是同一个), 任务是把 proposal **v4** (主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 提交 `b07f69a`) 返修为 **v5**, 处置 post_spec 第 4 轮审计的 finding。全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。主控会独立核验你的每一处改动并复跑证据脚本; 之后是第 5 轮五席审计 (只审 v4 → v5 的改动及其与未改文字的接缝, 并逐条对账本轮 finding)。

## 输入 (全部先读)

1. 当前三份文件 (主仓工作树即 `b07f69a`): `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`、`baseline_probe.py`、`baseline-evidence.md`。
2. 本轮聚合报告与五席报告原文: `/home/dev/Aria/.aria/audit-reports` 下 `post_spec-R4-*` 六个文件 (聚合报告的「全部 finding」表按席位原编号列出每一条; 「主控记录」节是主控的核验与处置意见 —— 其中标为「主控裁定」的条目按裁定执行, 你若有反证须写进报告而不是自行改向)。
3. 背景: 三个 issue (`/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/aria-plugin-154.md`、`aria-plugin-203.md`、`Aria-221.md`)、决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`、四份研究笔记 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/research/*.md`、上一版执笔派单 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/dispatch/writer-v1.final.md` (其中「主控范围裁定」仍有效, 除非本轮聚合报告的主控记录另有裁定)。
4. 源码: `aria/hooks/`、`standards/conventions/` 等 (基线 aria `268da8f`、standards `2bc1c4c`)。

## 要求

1. **逐条处置**: 聚合报告「全部 finding」表里的**每一条** (含 minor) 都要有处置: `fixed` (写明改了哪里) / `rejected` (必须附你亲自核验的证据: file:line 原文或实跑命令与输出) / `deferred` (只允许用于超出本 Spec 范围、且已在「待 owner 复议」或 Out of scope 记录的事项)。多席指向同一问题的可以合并处置, 但每个席位编号都要出现在处置表里。
2. **修类不修例**: 每修一处, 问「这个形状在 proposal / 探针里还有几个兄弟位置」, 一并修掉并在报告里列出。
3. **证据只经脚本生成**: 改了 SC 就改 `baseline_probe.py`, 然后在你的实验目录新副本上实跑, 把 stdout **原样**放进 `baseline-evidence.md` 的代码块 (不手改一个字符); 基线形态 (baseline-failing 与 doc-sync 全 `no`、其余类别全 `yes`) 必须 holds; 报告里写明 stdout 的 sha256 前 16 位与字节数。新增或改写的 SC 必须先在基线上跑出预期状态再写进 proposal (「它怎么会红」三态)。
4. **不引入新的问题**: 改动越小越好; 不要借返修扩大范围。任何「改变实现者动作」的改动单列一节 (主控会重点核)。
5. **纪律延续**: Rule #7 (不出现可被现行或拟议 L1 / L3 规则命中的凭据形状字面, 一律占位写法; 夹具运行时拼装); issue 引用全限定; 编号只用 `1.` `2.` 或「第 1 类」, **不用带圈数字**; 不写 AI 署名行; 机读 token 英文 canonical; 审计叙事**不写进** proposal 正文 (Status 行只写一句当前状态, 例如「Draft — post_spec 审计中」); 头部 Level / Status / Created / Linked Issue 四行中只允许按需改 Status 一行。
6. **硬性纪律**: 你不写仓内文件、不 commit、不 push、不 fetch, 不开 issue、不发评论, 不使用 Agent 工具; 实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5/` 下 (cp -a aria 与 standards 到那里再跑; HOME 指向该目录下的 `home/`)。三份文件与返修报告放在结构化输出里返回, 由主控落盘。

## 交付 (结构化输出)

- `proposal_markdown` / `probe_script` / `evidence_markdown`: 三份文件全文 (v5)。
- `writer_report_markdown`: 返修报告 (将落为 `.aria/notes/` 下的独立文件, 不进 Spec), 含: 处置表 (席位 · 编号 · 键 · 处置 · 改动位置或拒绝证据) / 同族扫描清单 / 改变实现者动作的改动 / 证据复跑记录 (命令、sha256 前 16 位、字节数、基线形态结论) / 执笔自报薄弱点 / 请裁项 (需要主控或 owner 裁的取舍)。
- `dispositions`: 与处置表一致的结构化列表。

## 本轮补充说明 (主控)

- **交付形态 (覆盖上文「交付」节的前三项)**: 三份文件写到你实验目录的 `deliver/` 下 (`proposal.md` / `baseline_probe.py` / `baseline-evidence.md`), 连同 `dispositions.json`、你的原型与复跑脚本 (`deliver/writer-v5-proto/`, 只放脚本与汇总, 不放树副本) 和证据所用的探针 stdout 文件, 生成 `MANIFEST.sha256`。结构化输出里三份文件字段只放一句指向母本的说明; `writer_report_markdown` 与 `dispositions` 放全文。
- **这是 `max_rounds` 内最后一次返修**: 第 5 轮是最后一轮审计。R4 主控记录第 7 条是硬要求 —— 优先复用已有机制 (尤其簇 T: 扩展的共现判定直接复用内建分段函数), 不写新机制; 每改一处都配会转红的坏实现; 只能靠新机制才能修的, 收窄语义或列为已知限制并论证 (写进「待 owner 复议」), 但不得降低既有检出。上一版的教训: v4 为修 NUL 加的一步把 UTF-16LE 的基线检出变成了静默 (R4 critical) —— 任何「换一种方式处理输入」的改动, 都要先证明它对既有检出是超集。
- **可复用的基础设施** (只读, 要改先 cp -a): 真 bash 3.2.57 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2/bash32/bash-3.2/bash`; v4 的原型、坏实现复跑脚本与汇总在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4/` (仓内归档 `.aria/notes/2026-09-30-wpa-phase-a/writer-v4-proto/`)。
- 主控裁定见 R4 聚合报告 (`.aria/audit-reports/post_spec-R4-2026-10-06T221714-000Z-secret-net-l3-and-bypass-paths-aggregated.md`) 的「主控记录」节。R1–R3 已关闭的问题不要改回去 (处置: `.aria/notes/2026-09-30-wpa-phase-a/writer-reports/` 下 v2 / v3 / v4 的处置文件)。
- **不要再往 Spec 正文写审计叙事** (km/m2: 「v3 的已知限制曾写」「上两轮」「eval 式实现曾全绿」这类版本 / 审计叙事放返修报告, 不放 proposal)。
- 写含敏感形状讨论的文件内容时, 用 Write 工具或脚本文件, 不要把这类文字放进 `python3 -c` / heredoc 命令行。探针完整跑一次约 5–6 分钟, 注意命令超时设置。
