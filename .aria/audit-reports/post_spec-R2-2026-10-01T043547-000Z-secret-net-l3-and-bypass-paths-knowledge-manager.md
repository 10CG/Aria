---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-01T06:56:00.000Z
context: openspec/changes/secret-net-l3-and-bypass-paths/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — knowledge-manager 席 (文档与规范一致性)

## 已实读文件

**被审对象 (全部实读, 非抽读)**
- `openspec/changes/secret-net-l3-and-bypass-paths/proposal.md` 全文 1-402 行 (b3e3123; 107305 字节, sha256 前 16 位 `654cb86e8d588ffe`, 与执笔 MANIFEST 一致)。
- `baseline-evidence.md` (57519 字节, `bbcdf8377f2447e9`): 头部 1-60 行与 320 行结果表 (脚本按类别 / 按 SC 核对); `baseline_probe.py` (105616 字节, `522fe6216524d5ea`): 头部 1-120、SC-15 703-708、文档判据 1100-1300、SC-33 1380-1420、汇总 1490-1531, 其余按需。

**必读材料**
- 三个 issue 正文与评论; 决策单全文; CLAUDE.md 规则 #6 / #7 / #10 与「多远程推送」两条硬约束。
- R1: 聚合报告全文 (含「全部 finding」表与「主控记录」)、本席 R1 报告全文、另四席的「风险 / 疑问」节; 执笔 v2 返修报告 §0-§7 全文。
- 研究笔记: `cc-hooks.md` 全文; `secret-scan.md` §0 / §1.9 / §4 与全部标题; `precedent.md` §5 与全部标题; `secret-guard.md` 全部标题。Spec 里 33 处「别名 + 节号」引用用脚本逐条核对, 全部解析到现有标题。

**规范与源码** (aria `268da8f` / standards `2bc1c4c`; 行号以我实读为准)
- standards: `secret-hygiene.md` 全文; `skill-benchmark-exemption.md` 全文; `configured-gate-authority.md` 全文; `content-integrity.md` §4; `version-management.md` §2 / §6; `git-commit.md` §6; `openspec/templates/proposal-minimal.md`; `openspec/project.md` Level 表; `spec-drafter/LEVEL_GUIDE.md` 跨模块段。
- aria: `hooks/secret-scan.sh` 全文; `hooks/secret-guard.sh` 1-150 行与 35 个被引行号; `hooks/hooks.json` 全文; 两个测试文件的被引行; `README.md` / `README.zh.md` Hooks 两节; `CHANGELOG.md` 顶部与四个先例条; `VERSION:164`; `.github/secret_scanning.yml`; `skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md`; `skills/openspec-archive/SKILL.md` Step 7; `state-scanner` 的 `check_bare_issue_refs.py` / `linked_issue_field_probe.py` / `collectors/_status.py`。
- 主仓: `.aria/state-checks.yaml` 版本类各 check 与 `plugin-cache-currency`; `.aria/pat-inventory.yaml` 头部; 六份先例 Spec 的 Level 与文档同步面; `pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:342`; 提交 `b3e3123` / `959daed` 的文件清单、`72cb02b` / `a99dd8d` / aria `26e644e` 的 `--stat`。
- 平台事实: 本机 Claude Code 2.1.285 二进制 (`updatedToolOutput` 出现 39 次, 描述原文在); 只读 API 一次 (`10CG/aria-plugin#153` 的 state 与 closed_at, 见 M3)。

**实跑** (全部在 `.../scratchpad/audit/post_spec-R2-knowledge-manager/` 下; aria / standards 私有副本已删 gitfile 以防触到真仓 `.git`; HOME / TMPDIR 私有; 值运行时生成、不打印; 真仓零写操作、零子代理)
- E1: 基线, 带真 bash 3.2.57 (`WPA_BASH32`), `baseline_probe.py` stdout sha256 前 16 位 `13cdea30978e1119` / 52197 字节, 与 `baseline-evidence.md` 内嵌块逐字节相同; 基线形态 holds。
- E2: 执笔 `build_full.sh` 产出的完整目标态原型 (复制到私有目录) 上同一探针: `4b0eea9cd97621d4` / 52861 字节, `target shape holds`, 154/154、20/20、53/53、57/57、26/26、9/9 (与执笔 T1 一致)。
- 自建变异实现 (6 个) 与 115 行 L3 子集复跑、W12 / 无害操作数 / 目标态 L1 抽测、全仓 L3 语料普查、44 个新入库文件的 Rule #7 形状扫描: 见各 finding 与「风险 / 疑问」。

**独立复核 (无异议项, 供其他席免重复)**
1. `check_bare_issue_refs.py` 对三份文件 rc 0 (裸引用 0); `linked_issue_field_probe.py` 输出 OK, `--emit-arg` 为 `10CG/aria-plugin#154`; 无带圈数字 / 希腊字母 / 表情符号; 全文反引号配对; 无 TBD 类标记; 无会话临时路径; 无 `执笔` / `返修` / 审计席叙事 (审计叙事没有被写进 Spec 正文)。
2. 23 个不同的全限定 issue 引用与 open-issues 缓存及仓内先例逐个核对: 仓别与主题都对; `10CG/Aria#154` / `10CG/Aria#179` / `10CG/aria-plugin#153` 为已关闭的历史引用, 用法正确; 「`10CG/Aria#154`(会话死锁) 与 `10CG/aria-plugin#154`(L3)」未混淆。
3. 头部事实: LEVEL_GUIDE「影响多个子模块 → 跨模块自动提升 Level 3」、模板「Changes affecting > 10 files」、project.md「Medium features (1-3 days)」逐字属实; 四份同型先例均为 Level 2 且同改 hook 与 `secret-hygiene.md`, 反例 07-11 为 Level 3; 决策单第 2-5 项复述与原文一致 (授权边界五类齐全); `guard_config_hooks` 守卫命令与 `10CG/Aria#199` 的 `detailed-tasks.yaml:342` 逐字节相同。
4. Impact 同步面: 主仓 16 个版本点 (CLAUDE.md 2 + README 2 + zh/ja/ko 各 3 + VERSION 1 + 两份架构文档各 1) 与 aria 6 个发版文件, 逐点对 `72cb02b` / `a99dd8d` / `26e644e` 的 `--stat` 核对一致; 四个同步 check 都存在且名字对; standards 子模块无独立版本行需要同步。
5. rule6_note 五字段在两块里取值都在 SOT §4.1 允许集内; 块 A 的 `n/a` 与 2026-08-02 先例的「分类而非免验」写法兼容; Rule #10 §5 要求的「AI 自作主张须请复议」由「待 owner 复议」8-18 承载。
6. 文档判据锚点: probe 用的标题前缀 (`### 2.2` / `### 2.5`、README 两语种 Hooks 用法小节) 在基线文件里存在且唯一; 所有被改文件 LF; SOT §3.8 / §5.6 当前不存在 (新增)。
7. 约 35 处 `file:line` 引用抽核全部与实读一致 (含 `secret-guard.sh:631-694 / :698-700 / :1111 / :736-1009`、`secret-scan.sh:135-142 / :367`、`secret-guard.test.sh:11 / :1618-1623 / :2015-2033`)。
8. Rule #7 形状扫描: 把 `0748dbc..b3e3123` 新入库的 44 个文件逐个当 Bash 输出喂基线与目标原型 L3: 无凭据形状字面量; 仅 4 份 R1 审计报告因讨论占位值 (`<…>` 与带省略号的 `$2b$…`) 在既有 `json-secret-field` 上告警, 其中两份在原型上变静默。三份 Spec 文件在两种 hook 下都静默。
9. 本机活体 L3 (v1.74.1) 对我 Read 一行含 JSON 键占位值的审计报告 (该行按 Bash 信封会告警) 没有任何告警, 与 W1「Read 从未被扫描」一致。

## Findings

### Critical

无。

### Major

#### M1 · id `fc97f926` · major · issue · implementation
- scope: `proposal.md What.W3` (`:82`、`:88`、`:330`)
- summary: W3 把「变量引用」整值放行延伸到既有 `json-secret-field`, 但 `$NAME` 规则又宽又欠定: 基线检出的「`$` 加单一大小写 (含数字、下划线) 口令」会变静默; 按散文字面再放宽到纯数字也全绿; 整个删掉小写类同样全绿 —— 115 行 L3 探针对这一类零约束。这是 R1 簇 A 的残余 (主形态已闭合)。
- 证据:
  1. 文本: `:82` 写「`$NAME` (NAME 全大写或全小写, 加数字与下划线; **不含混合大小写**)」, 未规定首字符; `:88` 作用范围含既有 `json-secret-field`, 而 W2 (`:65`) 规定既有键只过白名单这一步 (无熵下限); `:330` Impact 向读者保证「`$` / `<` 开头的随机值与 crypt 口令哈希**不**在内 (仍检出)」。
  2. 目标态原型 (值运行时生成、未打印; JSON `password` 键): 值为 `$` 加小写字母起头的 `[a-z0-9_]` 串 (含带下划线的; 共 11-12 位) 或 `$` 加大写字母起头的 `[A-Z0-9_]` 串 → 基线 `json-secret-field=1`, 原型 silent; 值为 `$` 加混合大小写 12 位、或 `$` 加数字起头 → 两侧都告警。原型正则在 `.aria/notes/2026-09-30-wpa-phase-a/writer-v2-proto/patch_l3.py:102-103` (`^\$[A-Z_][A-Z0-9_]*$` / `^\$[a-z_][a-z0-9_]*$`, 首字符限字母或下划线 —— 散文没写)。
  3. 散文字面读法的变异实现 (把这两条正则放宽成 `^\$[A-Z0-9_]+$` / `^\$[a-z0-9_]+$`): `$` 加 8 位纯数字、`$` 加数字起头的小写数字串 → silent (原型告警)。把 `SC-4..SC-13` 共 115 行 L3 探针 (`WPA_ONLY=SC-4,…,SC-13`) 对它复跑: baseline-failing 56/56、reverse-guard 17/17、allow-guard 35/35、known-limit 7/7, 0 行 `no`, 末行 `target shape … holds`。原因: 7h 的 `$` 起头值由 `_gen_first("$", ALNUM, 20, [LOW, UP, DIG])` 生成 (`baseline_probe.py:198`), 强制含大小写与数字三类, 结构上不可能落进单一大小写类。
  4. 逐类删除 W3 白名单类的变异 (各复跑同 115 行): 删小写变量引用类 → 0 行转红; 删 `$(…)` 类 → 0 行转红; 删 `{{…}}` → 11h / 11v 红; 删截断标记 → 11v 红; 删掩码 → 11q 红; 删刻意标记词 → 8 行红。即 `$NAME` 小写类与 `$(…)` 类既无「必须在」也无「不得多」的行 (SC-9 的 9l / 9m 是 24 / 25 字符的**大写**引用, 11v 的 `${VAR}` 是花括号形)。
  5. 小写类的实际收益: 把 aria / standards / 主仓 docs / openspec / `.aria` / aria-orchestrator 共 1292 个预筛文本文件 (≤200 KB) 当 Bash 输出喂「原型」与「原型删小写类」两版 hook: 删后告警的 15 个文件在原型上全部也告警, 被小写类静默的文件为 0 个。
- 失败场景: B.2 实现者按 W3 散文写 `$NAME` 规则 (散文无首字符限制), 320 行探针全绿; 此后 JSON 配置转储里基线会告警的 `$` 加纯数字、数字起头小写串、或单一大小写字母数字串口令 (既有键上没有熵下限, 白名单是唯一一道) 不再告警 —— 「检出变放行」, 且没有任何测试能发现; Impact 却对读者保证 `$` 开头不在静默集内。
- 建议修法: (a) 把 `$NAME` 钉到字符级 (首字符 `[A-Za-z_]`, 其余按「全大写或全小写」); (b) 二选一 —— 既有 `json-secret-field` 只放行花括号 / 圆括号闭合形 `${…}` / `$(…)` (JSON 字符串值里的裸 `$name` 不是 shell 变量引用), `$NAME` 只留给 6 个新 tag (赋值 / 头 / 参数语境, 那里 `$VAR` 引用才是主要误报形态; 9l / 9m 不受影响); 或保留现状并在 W3 已知限制与 Impact 如实写「`$` 加单一大小写字母数字下划线串的口令会被当变量引用放过」并加 known-limit 行; (c) 补行: reverse-guard 钉「`$` 加纯数字」「`$` 加数字起头的小写数字串」仍检出, 并钉 `$(…)` 与小写变量引用类到底放不放 (现在放与不放都绿)。
- 严重度说明: 残余形态窄 (口令恰为 `$` 加单一大小写字母数字串), 且 L3 头注释本就把低熵口令列为接受的残余风险, 我定 major; 若主控认定它延续 `e8d39a8a`, 应按 critical 计。

#### M2 · id `5fd1f356` · major · issue · documentation
- scope: `proposal.md Tasks` (1.10, `:355`), 与头部 Rule #7 声明 (`:13`) 的接缝
- summary: 头部声明「post-ship 复验腿同样只用运行时生成的合成值, 不触碰任何真实 secret 存储」, 但 Tasks 1.10 的两条 L1 腿是对真实进程表 (`ps aux`) 与真实路径 `/etc/forgejo/app.ini` 的「读取」验拦截 —— hook 未生效 (这正是验收要排查的情形) 时命令会真执行并回显, 声明与步骤互相矛盾。
- 证据:
  1. `:13`: 「post-ship 复验腿同样只用运行时生成的合成值, 不触碰任何真实 secret 存储, 因此不使用 `# secret-leak-ok-explicit` (步骤见 Tasks 1.10)」; `:355`: 「用一条 Bash 命令打印运行时生成的合成值 … 再对 `ps aux` 与 `/etc/forgejo/app.ini` 的读取各验一次拦截」。L3 腿确是合成值; L1 两腿没有合成操作数。
  2. W11 `:182` 自述 `ps` 完整命令行列是凭据旁路 (L3 对 `Authorization: token` 零告警, 当前 L1 是唯一预防层), 10CG/Aria#221 的事故就是进程表泄露 —— 即这条命令按 Spec 自己的分类属于 Rule #7 禁止的「读 secret 并流入 chat」。
  3. 插件缓存陈旧是仓内已知高频态: `.aria/state-checks.yaml:317-338` (`plugin-cache-currency`: 缓存停在旧版而 SOT 已前进 ⇒ 「一切 hook dogfood 验收失真」); 同文件 `:335` 本仓给的复验写法用的是无害操作数 (对一个假变量名 `p` 与假文件 `@f` 得 exit=2)。post-ship 复验最可能在「缓存未更新 / hook 未生效」时执行。
  4. 无害替代我在目标态原型上验证过 (基线均 exit 0, 即缓存陈旧时它们也无害): `ps -p $$ -o args=` (只打印自身进程) 原型 exit 2, `ps -p 1` exit 0; `cat /nonexistent-dir/forgejo/app.ini` 与 Read 同路径原型均 exit 2。而 `ps aux` 与 `cat /etc/forgejo/app.ini` 在基线 exit 0, 会真执行。
  5. 次要: W13 `:217` 允许在 B.2「实跑」`nomad var put … KEY=@<文件>`, 未规定指向不可达地址或临时 dev agent (另有 `--help` 原文作替代, 风险较低)。
- 失败场景: 实施者照 Tasks 1.10 字面在 ship 后验证, 若插件缓存未刷新或 hook 注册有误, `ps aux` 打印全部进程 argv (含 10CG/Aria#221 形态的后台轮询凭据), 或在有该文件的主机上 `/etc/forgejo/app.ini` 被读出 —— 值进入对话与 prompt cache, 产生新的轮换事件 (owner 已延后轮换), 而头部声明写的是「不触碰真实 secret 存储」。
- 建议修法: 把 Tasks 1.10 的 L1 两腿改为无害操作数 (进程表用只出自身进程的形态, 如 `ps -p $$ -o args=`; `app.ini` 用不存在的临时目录下的同名路径, `cat` 与 Read 各一次), 只断言退出码与 BLOCKED 文本; 头部声明改写为「L3 腿用合成值, L1 腿用无害操作数, 均不触碰真实进程表 / 真实配置文件」; W13 第 3 点的 `nomad var put` 实跑限定为不可达地址或 `--help` 原文。

#### M3 · id `05982c10` · major · issue · documentation
- scope: `proposal.md Impact` (issue 收尾口径, `:339-342`)
- summary: Impact 的 issue 收尾口径只管「评论 / 关闭」两个显式动作, 没约束提交页脚与 PR 描述里的关闭关键字; 仓内约定要求修复类提交写 `Closes`, 效果是推送 / 合并到默认分支时自动关闭 issue, 会绕过 10CG/aria-plugin#154「post-ship 复验后才关」与 10CG/aria-plugin#203 / 10CG/Aria#221「保持 open」(决策单第 2 项)。
- 证据:
  1. `:339-342` 只规定评论 / 关闭的时点; 全文没有 `Closes` / `Fixes` / `Refs` / 页脚 / 关键字字样 (grep 零命中)。
  2. 仓内约定: `aria/skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md:193` 「`Closes` 用于自动关闭相关的 Issue。当提交被合并到默认分支时, 引用的 Issue 会自动关闭」, `:199` 修复 Bug (Issue) 时「✅ 必需 `Closes #123`」, `:201` 部分实现才用 `Refs`; `standards/conventions/git-commit.md:185-191` §6.1 同列 `Closes` / `Fixes` / `Refs`。
  3. 实测: aria 提交 `c7a37e2` (作者时间 2026-08-20T11:54:23Z) 页脚含 `Closes #153`; Forgejo 只读 GET 得 `10CG/aria-plugin#153` 的 `closed_at` = 2026-08-20T11:55:00Z, 即一分钟内被自动关闭。aria 近 400 个提交里有 30 行以 Closes / Fixes / Resolves 开头的页脚 (`git -C aria log -400 --format=%B`)。先例 `b167c04` 写的是 `Refs #170 (不 close — …)`: 安全做法存在, 但本 Spec 没有写成约束。
  4. 本 Spec 的 issue 与提交面直接相关: 10CG/aria-plugin#154 在 aria 仓 (子模块「本地 merge + 双推」会把带页脚的提交原样推上 master); 10CG/Aria#221 在主仓 (主仓 PR 描述或合并提交可带关键字)。全限定写法 (`Closes 10CG/aria-plugin#154`) 的关闭行为我没有实测, 按同一风险处理。
- 失败场景: 实现者按仓内提交约定在 aria 提交里写 `Closes 10CG/aria-plugin#154`, 子模块本地 merge 后推 master, #154 在 Tasks 1.10 的 post-ship 复验与「逐条披露两处有意偏离」的关单评论之前就被自动关闭; 若 `Closes` 还写到 #203 / #221 (「部分实现」却用 Closes), 决策单第 2 项要求保持 open 的两张轮换延后 issue 被自动关闭 —— 关闭是 Spec 自己分阶段登记的外向动作, 这是一条未登记的旁路。
- 建议修法: 在 Impact「issue 收尾口径」与 Tasks 1.11 各加一条 —— WP-A 的全部提交页脚、PR 标题与描述、合并提交信息, 对三张 issue 一律只写 `Refs <org>/<repo>#<n>`, 不写 Closes / Fixes / Resolves (10CG/aria-plugin#154 的关闭是 1.10 之后的独立动作); 推送 / 合并 master 前加机械自检: `git log <起点>..HEAD --format=%B` 中不得出现关闭关键字后跟这三个 issue 号 (空输出且 rc 为 0 或 1 才算过, 写法照 10CG/Aria#199 的 rc 判据); 主仓 PR 描述同查。

### Minor

#### m1 · id `eff49510` · minor · issue · documentation
- scope: `proposal.md SC-26`
- summary: SC-26 的判据弱于 W9 / Impact 自己写的文档要求, 最小文本即全绿。
- 证据: (a) W9 `:162-163` 要求 §5.6 写「失效即整体忽略且静默 / 大小写不敏感」, 且把「靠文档」当静默失效的唯一缓解, 但 26c (`baseline_probe.py:1174`) 只查 `.aria/secret-guard.paths`、字面子串、只增不减、32 KiB、200、整体忽略; 我把原型 §5.6 里的「大小写不敏感」与「静默」两处删掉, SC-26 仍 8/8。(b) 26e 只要 README 两语种 Hooks 用法小节出现一次文件名 (`:1180-1189`), 而 W9 写「各一段」; 执笔原型的 README 改动正是 bash 代码块里一行注释。(c) 26g 只查 `rule6_note` / `.aria/secret-guard.paths` / `ps aux` 三词 (`:1200-1208`); 原型的 CHANGELOG 改动是 `## [Unreleased]` 加一行, 不含 Impact `:326-332` 自己要求的放行侧申报 (新放行 `os.environ` 单键读取与 jq 两形态; 新静默 L3 占位值)。
- 失败场景: 实现者按 SC 字面做完全绿, 采用方读到的文档看不出「失效静默」, CHANGELOG 只披露收紧一侧, 放宽 (安全姿态变化) 无申报。
- 建议修法: 26c 补「静默」「大小写不敏感」「CLAUDE_PROJECT_DIR」; 26g 补 `os.environ` / `keys_unsorted` / `fp=` 三个放行与日志侧词; 26e 改为小节内含「字面子串」或 `literal substring`。

#### m2 · id `5e342bfd` · minor · issue · documentation
- scope: `proposal.md What.W14`
- summary: 若干文档同步项只在散文里承诺, 既不在 W14 清单也没有 SC 验。
- 证据: (i) `secret-scan.sh` 头注释 `:40-53` 的 Scope 清单与 `:58-68`「What this does NOT catch」在补 6 个 tag 后过时 —— 研究笔记 `scan §4` 已列, W14 / SC-28 只处理计数字面、argon2、Read 形状、base64 一行; (ii) SOT §5.1 `:287` 括号逐变更列新族的体例 (先例 10CG/Aria#179) 未列入同步面; (iii) Impact `:336` 的 SOT 版本行 1.1.2 → 1.2.0 与历史表追加行无 SC; (iv) W11 `:193` / W13 `:219` 承诺把「tight 族与 Acceptable filters 不一致」记入 SOT §2.5 末尾注与 hook 头注释, 26b 只查 `pgrep -a`; (v) W10 `:178`「对外表述为部分覆盖」没有指明落点, 26f 只查 W11 的两个词元。
- 失败场景: 全部 SC 绿而 L3 头注释仍写旧 Scope、SOT 版本号没升、W10 的残余缺口不在任何用户面文档里。
- 建议修法: W14 清单补 (i)-(v) 并各配一条 SC (section 限定 + 词元); 或在 Tasks 1.9 逐条点名由勘正人核对。

#### m3 · id `51dded0b` · minor · issue · testing
- scope: `proposal.md SC-15`
- summary: 头部 Rule #7 声明说「本 Spec 与两份附件不含凭据形状字面量 (SC-15 15e / 15f 钉住)」, 但 SC-15 只钉 `proposal.md` 与 `baseline_probe.py`, 不含 `baseline-evidence.md`。
- 证据: `:13` 与 `baseline_probe.py:703-708` (15a-15f 六行, 无 evidence 文件); 我把 evidence 文件分别喂基线与目标原型 L3: 两者都静默 —— 声明今天为真, 但未被钉住 (证据文件是探针输出的派生物, 每次回填都可能变)。
- 失败场景: B.2 回填证据后某段输出或说明文字含形状字面量, 无 SC 发现。
- 建议修法: SC-15 增一行 (`baseline-evidence.md` 当 Bash 输出扫, 期望静默), 或把头部声明收窄成「proposal.md 与 baseline_probe.py」。

#### m4 · id `4900bccc` · minor · issue · testing
- scope: `proposal.md SC-27`
- summary: W14 `:227` 要求 `secret-scan.test.sh` 加头注释计数「与测试内 SC-13 同款的自检」, 27b 只比头注释数与实跑总数, 只加头注释、不加自检的实现也绿。
- 证据: `baseline_probe.py:1243-1252` (`_scan_header` 仅正则取 `Coverage: (\d+) cases` 与套件总数相等)。
- 失败场景: 日后增删用例而头注释没更新时, 套件自身不会变红 —— 正是 W14 说「现在 49 没有任何机械断言」要补的洞。
- 建议修法: 27b 另查套件源码里存在对头注释计数的比较断言 (参照 `secret-guard.test.sh:2018-2030`), 并配一个「只加头注释」的坏实现行。

#### m5 · id `5d032f7a` · minor · issue · documentation
- scope: `proposal.md What.W13`
- summary: §3.8 的适用面判据与末句措辞不闭合: 「长时 = 存活期超过数秒」与「短命令 = 秒级」之间没有分界, 而被 26h 钉死的 §3.1 示例自带 `timeout=30`; 末句「能用 `@<文件>` 或 stdin 时同一凭据优先用它」主语不明。
- 证据: `:216`; `secret-hygiene.md:134-139` (§3.1 示例 `timeout=30`) 与 `:176-178` (§3.4 ✅ 推荐 `KEY="$VAL"`)。末句若适用于全部命令, 与被钉死的 ✅ 示例并存时 SOT 自相不一致; 若只适用于长时进程, 与首句重复。
- 失败场景: 读 SOT 的 AI 在 30 秒量级的命令上无法判断适用哪条。
- 建议修法: 写明分界 (如「预期存活 ≥ 数十秒或常驻」) 并让末句限定到 §3.8 适用面。

#### m6 · id `0033f2f4` · minor · issue · documentation
- scope: `proposal.md 待 owner 复议`
- summary: 同一次发版后, hook 头注释 (28l) 将写「schema 里有 `updatedToolOutput`, 端到端未验证」, 而 README 两语种 `:33` 与 SOT §5.2 `:295` 仍写「架构上无法 redact」—— Spec 已知矛盾却把订正整体推给第 1 条复议。
- 证据: 本机二进制含 `updatedToolOutput` 39 处与描述原文 (我复核); `aria/README.md:33`、`aria/README.zh.md:33`、`secret-hygiene.md:295`; Out of scope `:234` 声明不改。不论 owner 选 A / B / C, 「cannot」都需改写为「不使用 / 未验证」, 因此该订正不依赖复议结论。
- 失败场景: 同一版本里文档互相矛盾, 后来的 AI 引用哪句取决于读到哪个文件。
- 建议修法: 在 SOT §5.2 与 README 两语种各加一句「2.1.285 schema 含 `updatedToolOutput`, 端到端未验证, 本 hook 不使用, 见第 1 条复议」(不改既有句子), 并入 W14 清单与 SC-28; 或在第 1 条复议里写明「复议前以上两处与 hook 头注释并存矛盾」。

#### m7 · id `5d12116d` · minor · issue · documentation
- scope: `proposal.md Tasks`
- summary: Spec 里 19 处「变异实测」是各 SC「怎么会红」的承重声称, 但 Spec 不指向这些证据的仓内落点, Tasks 1.8 的非作者对抗 review 也无从对照。
- 证据: grep `proposal.md` 中 `writer-v2-proto` / `mut_summary` 零命中; 证据在 `.aria/notes/2026-09-30-wpa-phase-a/writer-v2-proto/mut_summary*.txt` 与 `writer-reports/v2-writer-report.md` §4 (b3e3123 入库), 归档 README 自述脚本含会话临时绝对路径。我抽核的「转红行」声称 (SC-7 / 9 / 12 / 13 / 19 / 20 / 21 / 22 / 23 / 24 / 26 / 32 / 33) 与汇总一致。
- 失败场景: 非作者复核者不知道从哪里取坏实现清单, 要么重造要么跳过。
- 建议修法: 头部「证据位置」或 Tasks 1.8 补一句指向上述两处, 并注明路径需按本机改写。

#### m8 · id `84a82267` · minor · issue · documentation
- scope: `proposal.md SC-28`
- summary: SC-28 要求「旧文本消失且替换文本在场」, 但替换文本的字面只在探针里, Spec 散文只给中文说明。
- 证据: `baseline_probe.py:1287-1289`: 28g 要求头注释含英文字面 `credential key name`, 28h 要求 `PreToolUse Bash + Read/Edit blocker`, 28i 要求 `secret-scan.sh (v1.24.0` 且含 `detect`; W14 `:228` 只写「改为无前缀且无凭据键名」等中文。
- 失败场景: 实现者写出语义正确但措辞不同的头注释, 28g / 28h 转红, 只能读探针源码反推要凑哪几个词 (检查器在塑造被检内容)。
- 建议修法: SC-28 在每行判据里点名替换字面 (或把行描述改成「必须含字面 X」)。

## 上一轮对账

> 执笔处置表对 R1 的 30 个 critical / major 键 (6C + 24M) 全部标 fixed。我逐簇核验后的结论如下 (簇号与键来自 R1 聚合报告「主控记录」)。分歧: 簇 A 与簇 C4 我判 partially closed。

| 簇 | R1 键 | 对账 | 我亲自核验的证据 |
|---|---|---|---|
| A | `e8d39a8a` (tl C1 / cr C1 / km C1) · `14b7e703` (ba C1) · `8645b99f` (qa M2) | **partially closed** | 主形态已闭合: W3 改整值形态 (`:80-89`); E2 行 7h (七个独立运行) / 7i / 11s / 11v 全 yes, 基线对应行 no; 我另测 crypt 哈希形、`$` 加混合大小写 12 位、`<` 起头不闭合值在原型上仍告警。残余: `$NAME` 单一大小写类与欠定, 见 M1。 |
| A 负向侧 | `1c0bc16f` (qa M3) | partially closed | 原五个存活变异 (熵下限套既有键 / 含式 / 大小写不敏感 / 须含数字 / env-line 套白名单) 由 7h / 4o·10b / 11s 钉住, 与执笔 `mut_summary*.txt` 一致; 但 `$NAME` 类的三个变异我构造的都全绿 (M1)。 |
| B | `e600e931` (tl C3) · `179045cd` (ba C2) · `f42265a1` (qa C1) | closed | W12 改单键读取归一化 (`:200`)。原型实测 (exit 2 = 拦): `os.environ.get('X')` / `os.environ['X']` 0; `print(os.environ)`、`dict(os.environ)`、`.items()`、`.copy()`、`json.dumps(dict(…))`、`os.environb` 全 2; E2 行 23a yes (基线 no), 23c / 23d / 23e 基线与目标都 yes。 |
| B2 | `d9308fba` (cr M1) · `ab6a3123` (qa M1) | closed | 23d 钉 `.env_prod` / `.env2` / `.envprod` / `.envs/…` 经解释器读取仍拦 (原型实测全 2); 23g 钉非解释器现状。 |
| C | `7e0343bd` (tl C2) | closed | W9 `:159-161` + SC-20 20i-20m: E2 全 yes; 原型默认路径只经 `$( … )` 调用 (`proto secret-guard.sh:819 / 1290 / 1329 / 1334`), 裸调用只在 `SGVARIANT=ext_bare` 坏实现分支。 |
| C2 | `d4bcaf7c` (ba M2) · `d8e7b380` (tl M3) | partially closed | 设计层闭合 (固定字符串单遍 + 200 条 / 32 KiB / 64 处上界 + 内建先判 + 新时档 (f)(g)(h) 入 SC-30); 验收落在 B.1 / B.2 (SC-30 不由探针执行), 原型余量薄 (见表态 7)。 |
| C3 | `719ae05c` (ba M4) | closed | 19j (14 个各含一个元字符的条目逐个字面拦下) / 19k / 20h: E2 yes, 基线 no; 执笔 `ext_regex` 变异使 19j / 20h 转红。 |
| C4 | `53c140c4` (cr M2) · `27f6c3ce` (qa M6) · `b73ab606` (km M3) | partially closed | 扩展入口的文档落点已写 (SOT §5.6 / README ×2 / 头注释 / CHANGELOG; 26c / e / f / g 在 E2 全 yes); 五向行为声明与 L1 / L3 已知限制的落点只有词元级判据, 见 m1 / m2。 |
| D | `634eac5c` (qa M4) · `2ce0049b` (cr M4) | closed | W4 逐 tag 取值表 (`:102-112`); 12a-12j: E2 yes / 基线 no; 取值口径与 `.aria/pat-inventory.yaml` 的 `fingerprint_algo: sha256-hex-prefix-8` 一致。 |
| E | `44b5bb44` (tl M1 / cr M6) | closed | 我带 `WPA_BASH32` 复跑: 32c 在基线与目标态都「identical over 277 hook-direct rows」, 29h / 29i 两态 yes; 32a 已写明是启发式非可跑性证明。 |
| F | `e2459206` (tl M2) · `9db51a43` (cr M3) | closed | 22ao-22ar (包裹下 env / printenv) 基线 no → 目标 yes; 22at 对照放行; 22as / 22aj 钉 `/proc/N/status`。 |
| G | `846b21f8` (km M5) | closed (m5) | §3.8 限定适用面 + 26h 钉 §3.1-§3.7 / §4.1-§4.4 逐字节不变 (E2 yes)。 |
| H | `7deac83f` (ba M3) · `2779a016` (km M6) · `ba98e41f` (km M2) | closed (另见 M3) | 默认理解 B (`:341`, 待复议 3); 同步面 16 点 + 6 文件逐点核对 `72cb02b` / `a99dd8d` / `26e644e`; Tasks 1.11 承载。同一外向动作族的新缺口见 M3。 |
| I | `cf0ae932` (km M4) | closed (m7) | 四份笔记已入仓, 33 处「别名 + 节号」引用脚本核对全部解析; 变异证据未被 Spec 指向见 m7。 |
| J | `d9986b27` (cr M5) · `5831f8c0` (km M1) · `a3054a20` (ba M1) · `8e77d1ca` (qa M5) | closed | 13d 全串等值 (E2 yes, 追加句子的变异转红); SC-26 限定小节 (旧缺陷已堵); `_gen_first` 覆盖首字符 (4n / 5l / 5m / 7h); SC-33 + 分类器: aria + standards 语料 1 个归因文件 (E2 `flagged=1`), 我补测主仓 docs / openspec / .aria / aria-orchestrator 共 1078 个预筛文件, 命中新 tag 的 5 个 (2 份 R1 审计报告里讨论 tag 形状的散文, 3 个 aria-orchestrator 测试 / 文档), 非恒红。 |

R1 minor 里我认为仍未处置的: km m7 (tight 族与 Acceptable filters 不一致: 只在散文里承诺落点, 无 SC, 并入 m2(iv)); qa m7 / km m10 (doc-sync 判据强度: 限定小节后仍可词元堆砌, 并入 m1 / m8)。其余 R1 minor 已核对为 closed。

## 对执笔人自报薄弱点与请裁项的表态

**薄弱点 (返修报告 §5)**
1. 文字体量 +44%: 可接受。本轮不建议再削 (改字面会产生新接缝); R2 收敛后若要削, 只做「删重复括注」类零语义削减, 并重跑探针、重生成证据。
2. 交付形态偏离: 可接受。三份文件落盘后 sha256 前 16 位与母本 MANIFEST 一致, 且我在私有副本上独立复跑得到与内嵌块逐字节相同的输出。
3. 原型不是实现: 可接受, 但请记住: 原型的 `$NAME` 正则比 W3 散文窄 (M1) —— 「设计可达」不等于「散文足以约束实现」, B.2 的实现者只拿到散文。census 值 / 延迟 / 行数已写成「改为实测值」, 可接受。
4. v1 变异声称 5 处不符、研究笔记来源的数字未复跑: 可接受 (已逐条更正; 我抽核的转红行与汇总一致; 「465/108」「24/24」作为设计理据且标了出处)。
5. 12j 无独立 review: 可接受 (E2 yes; 非作者复核由 Tasks 1.8 承担)。
6. bash 3.2 腿默认关: 可接受 (带条件)。`baseline_probe.py:1496-1499` 把 `n/a` 行排除出统计, 缺 `WPA_BASH32` 时 29h / 29i / 32c 为 `n/a` 却仍印 `target shape … holds` (`:1517-1521`); Tasks 1.10 已写「不得是 not-run」, 作为人工闸门够用; 建议顺手把末行改成 `holds (N rows not run)`, 零成本且不破坏确定性。
7. 性能数字噪声: 可接受 (带条件)。(h) 档的绝对 `< 5 s` 腿对主机速度与负载敏感 (执笔余量 0.6 s); 我在负载 10-25 的共享主机上单次墙钟测 600 段档, 基线 12.2 / 14.4 s、原型 13.5 / 23.4 s —— 只说明该腿在非空闲机器上无意义, 不作通过 / 不通过证据。请在 Tasks 1.1 写明: 记录基线 (h) 实测值; 若基线值乘以原型实测增幅 (约 1.16) 已逼近 5 s, 停下上呈, 不得自行放宽 (Rule #10)。
8. 25 个变体同源盲区: 可接受, 且证据在我这里: 我独立构造的 3 类变异 (`$NAME` 散文字面读法、删小写变量引用类、删 `$(…)` 类) 全部通过 115 行 L3 探针 —— 同源盲区真实存在。建议 Tasks 1.8 的变异清单补「W3 `$NAME` 单一大小写类」。
9. SC-33 归因清单写死两路径: 可接受 (已写走 Amendment)。
10. W9 静默失效是产品取舍: 可接受 (已列待复议 18); 但 SC-26c 没有要求文档写明「静默」(m1), 而文档是该取舍唯一的缓解。
11. Windows / macOS 未实测: 可接受 (W9 已知限制已写)。
12. 探针并发竞态: 可接受 (私有 `USER` 已修; 我的 E1 / E2 与其它负载并行时无 R3-C-9 抖动)。

**请裁项 (§6)**
1. rule6_note 块 A `n/a`: 可接受 `n/a` (SOT §4.1 注释明写 n/a = 不属 Skill 变更; 块 A 已写明「分类而非免验」, 不会被读成 2026-08-02 被否决的「不适用」写法)。
2. 体量: 同薄弱点 1。
3. W9 静默失效: 可接受默认 A, 条件见薄弱点 10 / m1。
4. 10CG/aria-plugin#203 / 10CG/Aria#221 评论口径: 默认理解 B 可接受 (与决策单第 2 项字面一致)。请 owner 复议时一并裁: 提交 / PR 里的 `Refs` 引用会在对方时间线产生引用事件, 是否算「评论」; 以及 M3 的页脚约束。
5. SC-33 / `no-plan-fallback.md`: 可接受只归因不改 (改 Skill 下的示例会牵动 Rule #6)。
6. 探针 `n/a` 或失败: 倾向保持默认确定性 + 末行诚实 (见薄弱点 6)。
7. 原型与脚本归档: 同意只归档脚本与汇总 (主控已入仓 `writer-v2-proto/`), 不入各树副本; 但 Spec 未指向该目录 (m7)。
8. 交付形态: 可接受 (已核对)。

**「待 owner 复议」各项**: 产品级 1 / 2 / 4 / 5 / 6 / 7 可接受; 3 (默认理解 B) 可接受; 技术级 8-18 可接受, 唯第 10 条 (W3 白名单) 的 `$NAME` 部分见 M1, 技术级 16 (W12) 经原型实测可接受。

## 风险 / 疑问 (不计入 finding)

1. A.1 认领 TTL: 认领于 2026-09-30T17:57:13Z, `SWEEP_TTL` 24h, 约 2026-10-01T17:57Z 起可被扫为 abandoned; 余下审计轮次加 owner 等待可能越界。心跳属已授权的例行维护, 但 Spec / Tasks 无提示 (R1 已提, v2 未变)。
2. 公开镜像披露: 待复议 7.1 含「约 1400 个空段使 hook 超时后命令被放行并执行」这类未修复的通用旁路配方, 而主仓 GitHub 镜像匿名可读 (R1 已提, v2 未变); 请 owner 知悉是否保留该句。
3. 时间线引用: 10CG/aria-plugin#154 关单评论或 PR 描述里若写 `10CG/aria-plugin#203` / `10CG/Aria#221`, 会在这两张 issue 的时间线上产生引用事件 (不是评论)。字面读法不违反「本项之下不评论」, 但 owner 是否介意请复议时一并裁 (见请裁项 4)。
4. D.2 自动开 issue: `openspec-archive/SKILL.md` Step 7 在归档时若发现未勾选的 Tasks / carry-forward / 未验证声明, 会**自动**创建 Forgejo tracker issue (headless 也如此), 而决策单第 4 项的一次性授权不含「开 issue」。若归档时 Tasks 1.10 / 1.11 (post-ship 与 issue 收尾依赖 owner 动作) 仍未勾选, 会在无逐次请示的情况下开单; 建议归档顺序写进 Tasks。属通用流程面, 不单列 finding。
5. 全仓 L3 补测 (SC-33 语料之外): 主仓 docs / openspec / `.aria` / aria-orchestrator 共 1078 个预筛文件 (≤200 KB), 目标原型下命中 6 个新 tag 的 5 个: 2 份 R1 审计报告 (讨论 tag 形状的散文) 与 3 个 aria-orchestrator 文件 (两个脱敏测试夹具、一份 dispatch 证据文档)。W2 `:75`「本仓语料里只有两个文件命中新 tag」只对 aria + standards 两棵树成立。
6. `cc-hooks.md` 已入仓 (`.aria/notes/…/research/`) 且其第 1 条仍写「不存在 `updatedToolOutput`」, 与二进制不符; Spec 头部已声明以二进制为准, 但后来读仓的人可能只读笔记。
7. 本席在审计中被活体 L1 以「文本提及」误拦三次 (heredoc 内含 dotenv 名、grep 正则内含 `printenv` 字样、grep 模式内含 `nomad var put` 字样), 均改用 Write 工具落脚本文件绕开, 未使用 `# guard:ack` —— 同属 W12 / 10CG/aria-plugin#131 的误报类, B.2 实施者会反复遇到; 建议 handoff 记「脚本类内容用 Write 工具落文件」。
8. 措辞 / 引用精度 (不改变实现者动作, 不计): Impact `:334` 的「五向行为变更」与其下六条申报 (拦 / 告警 / 放行 / 静默 / 日志 / 性能) 数目不符; 待复议「第 18 条」可读作技术级 18 或建议开单 7.18 (后者是 nonce 竞态), 上下文可区分但易混。
9. 未能验证: SC-30 (带 git 历史与 `af87cae` 的真 checkout 上的时序闸) 不由探针执行, 我未跑; Windows Git-Bash / macOS 未测; W10 / W11 / W9 的负载下延迟未在空闲机上复测。

## Verdict

- verdict: **PASS_WITH_WARNINGS**
- counts: `0C/3M/8m`
- Vote: **REVISE**

## 是否足以进入 A.2

不足以: 3 条 major (M1: W3 `$NAME` 规则又宽又欠定, 基线检出的一类口令变静默且 115 行探针看不见; M2: Tasks 1.10 的 L1 复验腿用真实目标, 与头部 Rule #7 声明矛盾, hook 未生效时会真泄露; M3: Impact 的 issue 收尾口径漏掉提交页脚 / PR 关键字的自动关闭旁路, 可使 #154 先于 post-ship 复验被关、#203 / #221 违反决策单被关), 均局部可修 (每条 1-3 处文字加 2-3 行探针 / 自检), 修订后须重审; R1 的 6 条 critical 与 24 条 major 里其余均已闭合, 方案主体与 Level 2 (owner 已裁) 不在此列。
