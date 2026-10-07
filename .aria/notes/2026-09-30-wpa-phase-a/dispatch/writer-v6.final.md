你是 WP-A Spec `secret-net-l3-and-bypass-paths` 的**定点修补执笔实例** (backend-architect, 新派实例, 与 v1–v5 的执笔都不是同一个)。

背景: post_spec 已跑满 `max_rounds` 5 轮仍未收敛。owner 2026-10-07 裁定「接受当前结论 + 定点修补」。你的任务是把 proposal **v5** 修补为 **v6**, 处置第 5 轮审计的全部 finding。v5 在主仓分支 `docs/secret-net-l3-and-bypass-paths-phase-a` 上, 三份文件自 `6efb9b2` 起未变, 当前 HEAD 为 `785209f`。

之后的流程:
- 修补完成后, 由一个非作者席**只核你的修补处**及其与未改文字的接缝, 不再开全轮审计;
- 然后进入 A.2 (task-planner) 与 `post_planning` 收敛审计。

全程中文叙述, 代码 / 命令 / 路径 / SHA 保留英文。

## 输入 (全部先读)

1. 三份文件 (主仓工作树):
   - `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md`
   - `baseline_probe.py`
   - `baseline-evidence.md`
2. 第 5 轮聚合报告与五席报告原文: `/home/dev/Aria/.aria/audit-reports/` 下 `post_spec-R5-2026-10-07T080138-000Z-secret-net-l3-and-bypass-paths-*` 六个文件。
   - 聚合报告的「全部 finding」表按席位原编号列出每一条。
   - 「主控记录」节含簇归并、主控核实、**owner 裁定**与**主控裁定 1–8**, 按裁定执行。你若有反证, 写进报告, 不要自行改向。
3. v5 的返修材料: 返修报告 `.aria/notes/2026-09-30-wpa-phase-a/writer-reports/v5-writer-report.md` 与 `v5-dispositions.json`。历版处置在同目录; R1–R4 已关闭的问题不要改回去。
4. 背景材料:
   - 三个 issue: `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/issues/` 下 `aria-plugin-154.md`、`aria-plugin-203.md`、`Aria-221.md`;
   - 决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`;
   - 研究笔记 `.aria/notes/2026-09-30-wpa-phase-a/research/`;
   - 首版派单 `.aria/notes/2026-09-30-wpa-phase-a/dispatch/writer-v1.final.md` 的「主控范围裁定」。未被后续主控记录或 owner 裁定改变的部分仍有效。
5. 源码与平台:
   - 源码基线: aria `268da8f`、standards `2bc1c4c`。
   - 平台二进制 `/home/dev/.local/share/claude/versions/2.1.285`: 簇 X 的事件与输出 schema 以它为准。只读; 用 `LC_ALL=C /usr/bin/grep -a -o '<片段>.\{0,N\}'` 取片段, 不要整文件读。主控已核实的片段:
     - 事件表原文 `| PostToolUse | Tool name | Run after successful tool |` / `| PostToolUseFailure | Tool name | Run after tool fails |`;
     - 失败事件输入 `hook_event_name:R("PostToolUseFailure"),tool_name,tool_input,tool_use_id,error:o(),is_interrupt?,duration_ms?`;
     - Bash 默认 `isError:e!==0`, 失败时抛 `_U` (`ShellError`), 其 stderr 是合并输出;
     - 失败事件同样产出 `hook_additional_context`。
     - **输出 JSON 里 `hookSpecificOutput` 对失败事件要求什么字段值 (尤其 `hookEventName`), 由你在二进制里核实后写明。**

## 要求

1. **逐条处置**: 以下都要有处置记录:
   - R5「全部 finding」表的每个席位条目 (7 条 major 席位条目、14 条 minor 席位条目)。注意 `0033f2f4` 与 `684e9a24` 各自对应两件不同的事, 两件都要处置。
   - 主控裁定 7 列出的非 finding 定点勘误。

   处置取值:
   - `fixed`: 写明改了哪里;
   - `rejected`: 附你亲自核验的证据 (file:line 原文, 或实跑命令与输出);
   - `deferred`: 只用于超出本 Spec 范围、且已登记在待 owner 复议或 Out of scope 的事项。
2. **定点修补的边界** (主控裁定 8):
   - 只改点名的位置及其同族兄弟位置; 不重写未点名的段落。
   - 不新增机制。簇 X 是 owner 批准的唯一扩范围。
   - Spec 净增长尽量小。报告里写明 v5 → v6 三份文件各自的字节数变化。
3. **修类不修例 + 接缝自查**:
   - 每修一处, 问「这个形状在 proposal / 探针 / 原型里还有几个兄弟位置」, 一并修掉并列出。
   - 全部改完后做一次条款间交叉一致性检查, 覆盖新改条款之间、新改条款与未改条款之间, 结果写进报告。
   - 本仓教训: 多处修补逐条看都对, 合起来却互相违反隐含前提; 第 5 轮的两个新 major 正是上一次返修在接缝处引入的。
4. **证据只经脚本生成**:
   - SC 有改动就改探针, 在新副本上实跑, 把 stdout **原样**放进 `baseline-evidence.md` 的代码块。
   - 基线形态 (baseline-failing 与 doc-sync 全 `no`、其余类别全 `yes`) 必须 holds。
   - 分别带与不带 `WPA_BASH32` 各跑一次, 写明 sha256 前 16 位与字节数。内嵌进证据的是带 `WPA_BASH32` 的那次。
   - 新增或改写的行, 先在基线上跑出预期状态。
   - 每个新行配一个会让它转红的坏实现 (在你的原型上做), 汇总放进 `deliver/writer-v6-proto/`。
   - 目标原型带 `WPA_REQUIRE_ALL=1` 全量跑一次, 目标形态必须 holds。
5. **簇 Y 的 git 腿**:
   - 用本地 `git clone` 在实验目录得到带 `af87cae` 历史的副本 (源 `/home/dev/Aria/.git/modules/aria`, 只读)。
   - 在副本上叠上基线与原型, 各跑一次既有的 `hooks/tests/secret-guard.test.sh` (至少 SC-8 / SC-9a 块), 记录 loadavg 与五档 ms/call。
   - SC-8 的抽取方式、阈值、口径、档位一律不改。
6. **纪律延续**:
   - Rule #7: 不出现可被现行或拟议 L1 / L3 规则命中的凭据形状字面, 一律用占位写法; 夹具运行时拼装。
   - issue 引用一律全限定。
   - 编号只用 `1.` `2.` 或「第 1 类」, 不用带圈数字。
   - 不写 AI 署名行。
   - 机读 token 用英文 canonical。
   - 审计叙事不写进 proposal 正文: 版本号、审计轮次、「本版」「曾写」这类词放返修报告。
   - 头部四行里只允许改 Status 一行, 改为 `Draft — post_spec 定点修补中`。
7. **硬性纪律**:
   - 不写仓内文件、不 commit、不 push、不 fetch (第 5 条的本地 clone 除外);
   - 不开 issue、不发评论;
   - 不使用 Agent 工具。
   - 实跑只在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6/` 下进行: 把 aria 与 standards 用 `cp -a` 复制到那里再跑, HOME 指向该目录下的 `home/`。
   - 含敏感形状讨论的文字用 Write 工具落文件, 不要放进 heredoc / `python3 -c` 命令行 (现行 L1 会拦)。
   - 探针完整跑一次约 6 分钟; 超过 10 分钟的命令放后台跑。

## 可复用的基础设施 (只读; 要改先 cp -a)

- 真 bash 3.2.57: `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v2/bash32/bash-3.2/bash`, 以 `WPA_BASH32=<路径>` 传给探针。
- v5 的原型构建脚本、坏实现复跑脚本与汇总: `.aria/notes/2026-09-30-wpa-phase-a/writer-v5-proto/` (会话内原件 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5/`)。
- 第 5 轮各席的复现脚本 (只读参考), 在 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/audit/post_spec-R5-<role>/` 下:
  - qa 的六类窄化坏实现与 SC-8 复刻;
  - ba 的 `sc8/` 与 `h/` 下各用例;
  - cr 的 `remote_env_split` 直调;
  - tl 的 `PostToolUseFailure` 信封与 300 KB kv 用例。

## 交付

- 写到实验目录的 `deliver/` 下:
  - `proposal.md`、`baseline_probe.py`、`baseline-evidence.md`;
  - `dispositions.json`;
  - `writer-v6-proto/`: 只放脚本与汇总, 不放树副本;
  - 证据所用的探针 stdout 文件;
  - `MANIFEST.sha256`: `sha256sum` 格式, 用相对路径。
- 结构化输出:
  - `proposal_markdown` / `probe_script` / `evidence_markdown`: 各只放一句指向 `deliver/` 母本的说明;
  - `writer_report_markdown`: 返修报告全文。依次包含:
    - 处置表;
    - 同族扫描清单;
    - 交叉一致性检查;
    - 改变实现者动作的改动 (单列);
    - 证据复跑记录;
    - 字节数变化;
    - 自报薄弱点;
    - 请裁项。
  - `dispositions`: 与处置表一致的结构化列表。
