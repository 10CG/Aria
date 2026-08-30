---
checkpoint: post_spec
round: 6-cleanup-verification
role: cleanup-verifier
verdict: PASS
counts: 2未落/1部分落/1新矛盾
---

# post_spec R6 清账定向复核 — a1-entry 三份 Spec (rework v4.1, 2026-08-30)

> **本席镜头 (唯一)**: R6 五席点名的 finding 有没有**真的**落进三份 proposal 与决策单, 以及清账本身有没有造出新的条款矛盾。**不做新一轮通用审计, 不扩大范围, 不评价设计取舍。**
>
> **方法**: 报告里所有「逐字」均为 `sed -n 'Np'` 实读后抄录, `grep -n` 只用于定位。代码行号基线 aria `d50f9c3` (`git -C aria show d50f9c3:<path> | sed -n 'Np'`)。**本席未修改任何被审文件, 未 `git add/commit/push`, 未动 aria 子模块工作树 (停在 `fix/phase1-gate-no-push` @ `007d355`)。唯一写入 = 本报告。**
>
> **编号约定**: Spec 原文里的带圈数字 (SC-22 / D17 / Impact 的分项) 在本报告一律写成「第 1 条」…「第 7 条」, 不是原文拼写。

---

## (a) 一句话结论

R6 五席的 **8 个 critical 簇里 7 个已逐条落进当前文本** (证据均为实读逐字), 第 8 个 (探针依赖方向) 与「字段名折叠」已按 Rule #10 正式列为 owner 待裁项 (决策单 R6-1 / R6-2); 九对交叉一致性核完 **九对全部自洽**; 只剩 **2 条 minor 未落 + 1 条部分落**, 部分落那条同时构成 **1 条新矛盾** (决策单声称「母 §2.3 已钉死 `unattended` 取值路径」, 而母 `:270` 实读仍并列两条路径)。

---

## (b) 任务 A — 逐条落地核验表

> 席位缩写: CR = code-reviewer · TL = tech-lead · BA = backend-architect · QA = qa-engineer · KM = knowledge-manager。
> 「簇」= 跨席去重后的编号。文件缩写: **母** = `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` · **字** = `openspec/changes/linked-issue-field-availability/proposal.md` · **探** = `openspec/changes/sibling-spec-probe/proposal.md` · **决** = `.aria/decisions/2026-08-30-a1-entry-six-rulings-slug-form-and-no-cjk-only-tokens.md`。

### B.1 Critical 簇 (8 簇, 覆盖 CR 3C + TL 6C)

| 席位 | finding id | 簇 | 判定 | 证据 (文件:当前行号 + 逐字) |
|---|---|---|---|---|
| CR / TL | 接缝 C1 / 跨 C4 | **CL-1 `--linked-issue` 省略门统一为 E6 四态** | **已落** | 母 `:111`「token **不产生合法 canonical 值**时 —— 哨兵 (canonical `none`, alias `无`…) / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` (四态判据引字段 Spec §3 E6 四态表, 本 Spec 不重定义) —— 整个 `--linked-issue` 参数必须省略…R6 接缝 C1/C4 订正: 旧版只豁免哨兵, 与字段 E6「三格省略」相反」; 母 SC-12 `:585` 场景改为「spec 的字段判 `OK` 且非哨兵…但 AI 未传」+ 反向句「哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 时**必须**省略, 与字段 E6 四态表一致, 不再相反」+ 新增第二臂 (存量 markdown 链接形 ⇒ 复现 K8 ⇒ 必红); 母 §6 首行 `:463` 缺口描述已扩为四态; 母 rule6 (a) `:534`「只有字段判 `OK` 且非哨兵才传; 哨兵 / `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD` 省略 —— R6 接缝 C1」 |
| CR / TL | 接缝 C1 / 跨 C5 | **CL-2 `--emit-arg` 切换的实现归属 + 悬空引用** | **已落** | 母 `:125` 新段「**`--linked-issue` 实参的取值 —— 两阶段, 模板一次写死, 不需要字段 Spec ship 后二次编辑 (R6 接缝 C1/C5 的归属处置)**…**该模板行归本 Spec Impact** (`phase-a-planner` / `spec-drafter` 两行), 字段 Spec 只负责 `--emit-arg` 模式存在 (其 SC-9); 两份 Spec 任意顺序 ship 均自洽, 不存在第二次编辑。SC-22 ② 含字面 `--emit-arg`。」; 母 SC-22 `:612` 第 2 条七个字面量含 `--emit-arg`; 母 Impact `:666` 该行含「命令行 = §2 的模板 + `--linked-issue` 两阶段取法含 `--emit-arg`」 |
| CR | 接缝 C2 | **CL-3 探针「可先 ship」× 「E0–E6 不复制」× 「钉死 import」三者不可同时成立** | **属 owner 待裁** | 探 `:133`「⛔ 本 Spec 不得内含第二份抽取实现 (E0–E6 一条都不复制)。」与 `:137`「本 Spec **可先于姊妹 ship** —— 此时层 1 恒 `NO_TOKEN`、**全部走层 2**」**原文未动** (符合 CR 自陈「属 owner 决定, 它改变 2026-08-23 拆分时的成文前提」); 决 `:78` 已把它列为 **R6-1** 待裁: 「探针 Spec 对字段 Spec 纯函数 `lib/linked_issue_field.py` 的依赖方向 (接缝 C2: …三者不可同时成立)」, 选项 (i) 硬前置 / (ii) 模块缺席时 `verdict="not_established"` |
| CR | 母 C1 | **CL-4 Level 1 前置 claim 零调用 (三落点)** | **已落 (三处齐)** | 母 §2.5 `:370` 新 bullet「**Level 1 例外 (R5/skill-reviewer M4 → R6/CR 母 C1 入正文)**: `phase-a-planner` 判定 **Level 1** (`skip_if: complexity: Level1` 命中, 实读 `phase-a-planner/SKILL.md:67`) ⇒ **前置 claim 零调用** (不写 claim、不推远端)…由 **SC-9 (B)** 臂钉住; rule6_note (a) 同步。」; 母 SC-9 `:582`「**两臂**: (A) `coordination.enabled == false`; (B) `phase-a-planner` 判定 **Level 1**…两臂均: A.1 **零调用**」; 母 rule6 (a) `:534`「(**Level 1 与 `coordination.enabled == false` 时零调用**, §2.5)」 |
| CR / TL | 母 M2 / 母 C2 | **CL-5 SC-22 未落 D17 第 2 要件 (完整命令行)** | **已落** | 母 SC-22 `:612` 新增第 7 条:「**(D17 ②, R6/TL C2 + CR M2 补)** 切片内含**一条以 `python3` 起首、含 `phase1_gate.py` 与 `--phase A.1` 的完整命令行**」+「怎么会红」列新增「**「参数子串齐全但没有一条可执行命令」的散文实现因 ⑦ ⇒ 必红** (R6/TL C2 给出的那段反例)」 |
| CR / TL / QA | 母 M3 / 母 C1 / 母 m1 | **CL-6 SC-22 第 5 条与块边界规则互斥 + 落点未钉 + 7 个 yaml 围栏** | **已落 (三半齐)** | 母 SC-22 `:612` 块边界句改为「**②③④⑥⑦ 只在该切片内求值; ⑤ 是切片外的独立断言** (R6/TL C1: 旧写「②–⑥ 只在切片内」与 ⑤ 互斥)」; 落点钉死:「**新标题的落点钉死: 放在 `### 步骤执行` (`phase-a-planner/SKILL.md:60`) 之前**, 使切片止于 `:60`、不吞下步骤表 (§2「不塞进 YAML 列表」)」; 第 5 条内补「**文件内共 7 处 yaml 围栏, 宿主实现须先按该锚点定位, 不可抓第一个** —— R6/QA m1」 |
| TL / BA | 母 C3 / 母 M1 | **CL-7 SC-32 要求松绑 `--raw-track-id` 而 Impact 写「零改动」** | **已落 (四处齐)** | 母 Impact 第二处变更 `:664` 新增第 7 项:「**⑦ `--raw-track-id` 由 `required=True` (`:1187`) 改为 `required=False` + `_main()` 内模式校验** (R6/BA M1 + TL C3): 非 `--heartbeat-only` 模式缺参仍 `parser.error(...)` (acquire 路径的 fail-fast 不放松, 负控)…三种落法中**钉死 (a)**…不用 subparsers、不拆独立脚本 (旧写…作废)」; 母 Impact 第一处 `:663`「**除 `--raw-track-id` 的 `required` 见第二处变更 ⑦ 外零改动**」; 母 SC-32 `:622`「**坏实现 1** (R6/BA M1 + TL C3): 只加 `--heartbeat-only` 开关而不松绑 `:1187` 的…⇒ argparse 在进入 `_main()` 前即 `error:…` ⇒ 零记录 ⇒ 必红」 |
| TL | 字段 C6 | **CL-8 hunk B 预览骨架默认哨兵 = 零证据当正证据** | **已落** | 字 `:144`「**hunk B (新)**: 预览围栏内 `:140` 后插 `> **Created**: {YYYY-MM-DD}` 与 `` > **Linked Issue**: `{<org>/<repo>#<n>}` `` 两行 (**placeholder, 与 SOT 同串** —— R6/TL C6: 旧写 `none` 会把「已核实无关联」这条正证据做成写入侧默认值, check 恒绿、母 Spec 主机制对每份新 Spec 恒零输入)」; 字 SC-7a `:546` 新增负控「(ii) **负控 (R6/TL C6)**: 该 `Linked Issue` 行的值**不得**是哨兵集合成员 (`none` / `无`), 须为 SOT 同串 placeholder `` `{<org>/<repo>#<n>}` ``」 |

### B.2 Major 簇 (覆盖 CR 11M + TL 9M + BA 2M + QA 3M + KM 3M)

| 席位 | finding id | 簇 | 判定 | 证据 (文件:当前行号 + 逐字) |
|---|---|---|---|---|
| CR | 母 M1 | **CL-9 `Part A1` → `Part B1` 改名是事实错误** | **已落 (三处统一撤回)** | 母 `:127`「⚠️ 该标题里的 `Part A1` 是已 ship Spec `coordination-claim-lifecycle-and-overlap` 的**部件名**…**不是** Phase A.1 —— R5/M2 误读, rework v4 一度落成改名, R6/CR M1 撤回; 本 Spec **不改**该标题」; 母 rule6 #8 `:522`「**标题不改** —— …rework v4 曾按 R5/M2 的误读落成改名, R6/CR M1 撤回」; 母 Impact `:672`「**标题不改**: `Part A1` 是…部件名…rework v4 曾按 R5/M2 的误读落成改名, R6/CR M1 撤回」。全文 `Part B1` 仅 2 处 (`:134` / `:507`), 均为「= `linked_issue` 部件」的正确用法 |
| CR | 母 M4 | **CL-10 SC-23 / SC-14(a) 的 baseline 标注为假** | **已落 (含新 SC-34)** | 母 SC-23 `:613`「**⚠️ baseline 即绿的回归守卫** (R6/CR M4 订正: …同一串 X 先 acquire 后 release 在 `d50f9c3` 上今天就过…旧写「现状必红」把三处 SKILL.md 模板的**文本**缺陷误当成了代码缺陷)。坏实现 = `derive_track_id` 去容器段 或 `release_claim_by_track` 匹配键…改坏 ⇒ 必红」; 母 SC-14 `:592` 同款订正; 新增 母 SC-34 `:624`「(新, R6/CR M4 + m4; 文本层)…三个文件**各自**含逐字 `A.1 认领时派生的那一串`…**baseline 必红** (三文件今天 0 命中)」 |
| CR / TL | 母 M5 / 母 M6 | **CL-11 §瓶颈「可当场复核」段复核即错** | **已落** | 母 `:78` 口径命令改为两拼写 `grep -rlE '\*\*(Linked Issue\|关联 Issue)\*\*' openspec --include=proposal.md`; 母 `:83`「**落盘后的现状 (2026-08-30 订正; 复核以命令为准, 数字是当日观测)**…本文件按 FIX-19 补了**真的**字段 (第 **13** 行, 现为 `> **Linked Issue**: \`10CG/Aria#174\``…)。**中文单拼写的 grep 已不再命中本文件**…按两拼写**行首**谓词才是 3 份真字段…(R6/CR M5 + TL M6 + QA M1 订正旧句「1 条真阳」)」 |
| CR / KM | 母 M6 / 母 M1 | **CL-12 `coordination_probe.py:4-25` 引文出处错标** | **已落** | 母 `:237` 改为「实读 `skills/state-scanner/scripts/coordination_probe.py:18-21`…(该文件逐字「The production partition file is written only when ``_source==\"production\"``」)」。**本席实读基线核对**: `git -C aria show d50f9c3:skills/state-scanner/scripts/coordination_probe.py \| sed -n '18,21p'` 首行逐字 `  The production partition file is written only when ``_source=="production"``,` ⇒ 出处与引文现在对得上 |
| CR | 母 M7 | **CL-13 K6「加 swept 标记」follow-up 无落点** | **已落** | 母 Impact follow-up 表新增第 7 行 `:697`「`ClaimRecord` 加 **swept 标记** (分辨 `abandoned` 来自显式 release 还是 `--sweep-stale` 的 GC 产物, §2.3 K6) \| 改 schema 字段, 须与 `coordination-ref-schema.md` §3 演进契约同批评估…(R6/CR M7…)」 |
| CR | 母 M8 | **CL-14 `unattended` 取值路径「容器镜像 / Nomad env」二选一混写** | **部分落 (见新矛盾 N-1)** | **决策单侧已落**: 决 `:93`「§3-9 / M4 \| `unattended` 取值路径钉死或整条删 \| **已采纳前者**: 钉死为 aria-runner 镜像内 `.aria/config.json` (母 §2.3), env 三腿仍 follow-up \| R6/CR M8 同判」。**母 Spec 侧未落**: 母 `:270` 实读仍为「…在 `config-loader` 登记并在 `DEFAULTS.json` 注册, **由 aria-runner 容器镜像 / Nomad task env 显式置 true**」—— 两条路径仍并列, 未钉死任何一条 |
| CR | 探针 M1 | **CL-15 探针 §3 两处哨兵判据只写 `无`** | **已落** | 探 `:116`「靠**姊妹 E3 的 token 串本身** (未 strip) 判是否为哨兵: **逐字节等于 `无` (单个 U+65E0), 或 ASCII 大小写折叠后等于 `none`**, 两端无空白 (姊妹 §2 集合 + E5 原文; R6/CR 探针 M1 同步旧句「只比 `无`」)」 |
| CR | 字段 M1 | **CL-16 字段头部「代码落点」缺两个新建文件** | **已落** | 字 `:7`「…`skills/state-scanner/lib/linked_issue_field.py` (**新建**, 纯函数, 探针 Spec 的承重依赖) 与 `skills/state-scanner/scripts/linked_issue_field_probe.py` (**新建**, 含 `--emit-arg` 模式) + 主仓 `.aria/state-checks.yaml` (注册) 与 `.aria/linked-issue-field-grandfathered.txt` (**新建**, 仓本地白名单)…(R6/CR 字段 M1 补齐)」 |
| CR | 字段 M2 | **CL-17 SC-5 臂数在同文档三个值 + §4 判据表缺白名单缺失行** | **已落 (三处统一为六臂)** | 字 `:420`「**探针的判据分割 (fail-CLOSED, 六臂 (R6/CR 字段 M2 统一臂数))**」+ 表体新增第 6 行 `:427`「`--grandfathered` 缺省或文件不存在 \| 白名单视为**空集**, **照常判定** (不是错误; 缺白名单 ⇒ 无人被豁免, 采用方的正确默认)…」; 字 SC-5 `:543`「**探针判据分区六臂** ((a)–(d) + (e1)(e2); R6/CR 字段 M2 统一臂数)」 |
| TL | 母 M1 | **CL-18 `derive_track_id` 超长写成截断, 实为 sha256 回落** | **已落 (含新缺口行)** | 母 `:140`「归一由 `derive_track_id` 在 acquire 内部做 —— lower / `./_`→`-` / **原串 >64 字符或含非 ASCII ⇒ 整串 sha256 回落, 结果形如 `sha256-<16 hex>`, 不保留 slug 与容器段的可读形式** (`lib/track_id.py:70-76` 步骤 4 + `:155` `use_fallback`; 步骤 3 的截断…)」; 母 §6 新增缺口行 `:470`「**slug 过长 ⇒ track-id 退化为不可读哈希** (slug > 55 字符时…本仓 `archive/` 历史最长 slug 53 字符, 离阈值 2 字符…) \| 无界 \| 机制仍成立…只丢「人类可读」这半条 D18」 |
| TL | 母 M2 | **CL-19 §2.4b 四态表「键缺席」定义在门控放宽后为假** | **已落** | 母 `:344`「键**缺席** \| **未检测** —— 未传 `--linked-issue` (**与是否传 `--include-terminal` 无关**: 后者独立控制 `unknown_schema_claims` 键, 与本表正交。R6/TL M2 订正旧定义「既未传 A 也未传 B」—— 哨兵轨恒带 `--include-terminal` 而不传 `--linked-issue`, 是最常见形态而非例外) \| 「本轮**未检测**」」 |
| TL | 母 M3 | **CL-20 §5.2 退出路径表不穷尽 §2.3 (并轨 / done 档)** | **已落 (两行 + §2.3 措辞)** | 母 §5.2 新增两行 `:448`「**并轨** (§2.3 `active` 档裁决) \| 两轨合一: **被并掉的一方各自 release 自己的 claim**…对方那条**不由本容器释放** (D6: 不引入跨容器 release), 成文接受它挂到 `--sweep-stale` (R6/TL M3 补行)」与 `:449`「**复用对方产出, 本轨不起 Spec** (§2.3 `done` 档裁决) \| 同「探索性放弃一个方向」…本行是它指向的落点 (R6/TL M3 补行)」; §2.3 `active` 格措辞改为「**请对方容器的 owner 释放其 claim 后再开始**」(人工协作动作 —— 本容器**无**任何可执行命令…D6; R6/TL M3 改措辞) |
| TL | 母 M4 | **CL-21「放弃整个 issue」缺方向枚举机制** | **已落** | 母 §5.2 `:447`「**方向的枚举机制 (R6/TL M4, 不靠 AI 记忆)**: 跑一次 A.1 认领命令 (带该 `--linked-issue`) 读 `linked_issue_overlap[]` 中 `container` 等于本容器的条目 —— 实读 `lib/collision.py:271-279` 该函数**不按 container 过滤**, 只按 `track_id` 自排除」 |
| TL | 母 M5 | **CL-22 `--no-push` 是事实 ship 前置却不在前置依赖/闸门** | **已落 (两处齐)** | 母 `:16` 尾部新增「**· aria-plugin `--no-push` 修复** (决策单第 4 项; aria 分支 `fix/phase1-gate-no-push` @ `007d355`, **2026-08-30 状态: 未推任何 remote, 非 `origin/master` 祖先**, R6/TL M5 核) —— 它是 rule6_note 六条照跑的硬前提与 Impact 两处描述性 hunk…的依据, **须先合入 `origin/master`** (闸门状态表 #7)」; 闸门状态表 `:768`「**第 4 项修复 (`--no-push`) 已升格为硬前置** (头部「前置依赖」+ 闸门状态表 #7, R6/TL M5)…Phase B.1 前须断言它已合入 `origin/master`」 |
| TL / CR | 探针 M7 / 探针 m2 | **CL-23 SC-17「全文恰 2 次」与同文件新契约节相冲** | **已落** | 探 SC-17 `:503`「(§8 双落点; **R6/TL M7 + CR 探针 m2 收窄计数域**)…对…`## Convergence 模式` 与 `## Challenge 模式` **两节的围栏块切片**分别计数…\| **每块恰 1 次** (共 2); **负控**: 除这两处围栏外, 全文 (含新增的 `## 竞品 spec 探针 (per-round 入口)` 契约节) 该字面 **0 次** —— 契约节用「探针的 stdout 契约如下」之类措辞, 不复用该前缀」 |
| TL | 探针 M8 | **CL-24 新契约节无存在断言 (SKILL.md 指针可悬空)** | **已落** | 探 SC-20 `:506` 新增第 (ii) 臂:「(ii) `references/execution-modes.md` 含标题字面 `## 竞品 spec 探针 (per-round 入口)`」+ 期望列「(ii) 该节切片 (至下一个 `^## ` 行) 内含 §7 的 `verdict` / `status` / `hits` 三个字面与 §9 三档措辞的字面 `未能核实` / `已完整扫描` / …」 |
| TL | 字段 M9 | **CL-25 D17 未声明适用范围** | **已落 (含 CR m1 围栏边界)** | 母 D17 `:506`「**适用范围**: ① 适用于任何被机械断言的块; ②③ **仅适用于指令块** (块的目的是让 AI 执行动作), **不适用于模板 / 骨架块** (块的目的是被复制成产物 —— 往骨架里塞命令行会被 AI 原样复制进每份产物)。**引用本条的 SC 须写明自己落了哪几件**: 母 SC-22 落 ①②③ / 字段 SC-7a 仅 ① / 探针 SC-20 落 ①②③」; ① 内另补「**围栏内的 `#` 行不作为边界; 被测块本身是 ``` 围栏时, 边界即该围栏**」(CR 母 m1) 与「切片外的独立断言须**显式声明**其求值域」 |
| BA | 探针 M1 | **CL-26 `sys.path` 双插入顺序敏感 + 已知限写成「将来」** | **已落 (合并成一份 + 新 SC-21)** | 探 `:160-164` 唯一合并代码块逐字含「`_SS_ROOT = …` `# 供 lib.* (Layer L)` / `_SS_SCRIPTS = …` `# 供 collectors.*` / `for _p in (_SS_SCRIPTS, _SS_ROOT):   # 顺序承重: 最后插入的 _SS_ROOT 排在 sys.path 最前 (R6/BA 探针 M1)`」; 探 `:169`「**已知限 (成文; R6/BA 探针 M1 订正 —— 同名碰撞的另一方**今天就存在**, 不是「将来」)**: `state-scanner/scripts/lib/` 是一个既有的、带 `__init__.py` 的包…」; 新增 探 SC-21 `:507` (断言 `sys.modules["lib"].__file__` 落在 `state-scanner/lib/__init__.py`; 坏实现 = 把 `_SS_SCRIPTS` 插在 `_SS_ROOT` 之后 ⇒ `ModuleNotFoundError` ⇒ 红) |
| QA | 字段 M1 | **CL-27 §Why「两级假阳性剔除」数字与自引行号不可复现** | **已落 (SHA 锚 + 行号订正 + 双拼写注)** | 字 `:58` 行尾补「← 行号按主仓 `cc1bdef` (稳定锚点, D2…)」且行号已由 `:88` 改为 `:75`; `:65-68` 的自引行号已由 `:65`/`:86` 订正为 `:95`/`:116`; 新增 `:70`「**2026-08-30 注 (R6/QA M1 + CR M5)**: 本节命令写的是中文单拼写 `关联 Issue`; 6i/O-2 落版后三份在制 Spec 头部改为 `Linked Issue`, **复核须用两拼写谓词** `grep -rlE '^> \*\*(Linked Issue\|关联 I…'」 |
| QA | 字段 M2 | **CL-28 SC-4(f) 依赖「E5 吃 E3 原始 token 串」未写明** | **已落** | 字 SC-4 `:542` 期望列「(e)(f) **`BAD_TOKEN`** (集合封闭; (f) 按 E3「不 strip」+ E5「两端无空白」—— **E5 的哨兵判定必须吃 E3 原始 token 串**)」+「怎么会红」列结尾「**(f) 的坏实现** (R6/…)」 |
| QA | 字段/探针 M3 | **CL-29 字段名是否做 ASCII 大小写折叠** | **属 owner 待裁** | 决 `:79`「**R6-2** \| 字段名 E0 谓词 1 是否做 ASCII 大小写折叠 (QA M3: GitHub 原生术语 `Linked issues` 是真实假阴性来源) \| (i) 折叠 (不放宽单复数); (ii) 维持不折叠 (集合封闭) \| 无强倾向; QA 席倾向 (i) 且指出它不违反本文件「拼写 ≠ 判定」的论证」 |
| KM | 决策单 M1 | **CL-30 反驳 1 的 grep 数字「15」今天复算不出** | **已落** | 决 `:23`「…母 Spec rework v3 在主仓 `cc1bdef` 上的观测: `grep -rl '**关联 Issue**' openspec --include=proposal.md` 得 15 份 = **14 份 archive/ (稳定子集, 2026-08-30 仍是 14) + 1 份 changes/**…」—— 已钉 SHA + 拆出稳定子集 |
| KM | 决策单 M2 | **CL-31 测试计数 1393 → 1409 与实测不符** | **已落** | 决 `:58`「…state-scanner 套件 `unittest discover` 在 `007d355` 上 `Ran 1409 tests … OK`; 静态 `def test_` 计数 `d50f9c3` 1409 → `007d355` 1425 (**+16**, 与新增数吻合)。R6/KM M2 订正: 早前写…」 |
| CR | 流程 m1 | **CL-32 R5 code-simplifier 8 条既未上呈也无留痕** | **已落 (决策单建台账)** | 决 `:82`「**R5 code-simplifier 席未呈项的台账** (R6/CR 流程 m1: 该席 13 项「去掉它会不会漏缺陷」判定与 C3 此前未进任何处置建议; 按 memory `narrow-owner-options` 逐条留痕, 采纳/拒绝理由如下, 「待裁」项由 owner 定)」+ 逐行台账 (含 `:93` 的 M4 行) |
| TL | (收敛判断) | **CL-33 建议换执笔席 / 不加 R7** | **属 owner 待裁** | 决 `:80`「**R6-3** \| tech-lead 席的收敛判断…建议**换执笔席**清账 + 定向复核, 不加 R7 \| (i) 接受主控本轮已做的清账 + 一个新席位定向复核; (ii) 换执笔席重做清账 \| 主控已按 (i) 落版 (母 Spe…)」 |

### B.3 带具体锚点的 minor (行号 / 引文订正类)

| 席位 | finding id | 判定 | 证据 |
|---|---|---|---|
| CR / TL / KM | 母 m2 / 母 m2 / 母 m1 (`complexity: Level1` 在 `:66` 应为 `:67`) | **已落** | 母 §2.5 `:370`「实读 `phase-a-planner/SKILL.md:67`」; 母 SC-9 `:582`「(`skip_if: complexity: Level1` 命中, `phase-a-planner/SKILL.md:67`)」 |
| TL | 母 m1 (Impact 写「五处」实列六项) | **已落** | 母 `:663`「本行只改下列六处 —— R6/TL m1 订正计数」, 逐项 ①–⑥ 齐 |
| CR | 母 m3 (SC-11「四档选项集不同」) | **已落** | 母 SC-11 `:584`「**措辞按 status 分档** (§2.3 选项表: 四档**渲染**不同; `abandoned` 与 `active` **共用选项集**, `unknown` 视同 `active` —— R6/CR m3 订正「四档选项集不同」)」 |
| CR | 母 m4 (三处 B/D 占位串无文本层断言) | **已落** | 新增 母 SC-34 `:624` (见 CL-10 行) |
| CR | 母 m5 (rule6 11-hunk 表漏一个描述性 hunk) | **已落** | 母 rule6 表新增第 12 行 `:526`「`state-scanner/SKILL.md:168` 输出键集补 `push_skipped` / `push_skipped_reason` (aria-plugin `--no-push` 修复引入的 additive 键) \| **描述性** (键集登记) \| 第一行 \| substitute = 结构化断言「`:168` 一带含字面 `push_skipped`」, **baseline 必红**」 |
| CR | 母 m6 (一批引用 minor, 含「字段 Spec 全文 `FIX-07` = 0」) | **部分落 → 该子项未落** | 已落的抽样: 母 Impact `:679` 已订正为「现枚举 reader 侧 unknown 行为 5 条于 `:133-140` (R6/CR m6 订正)」。**未落**: 本席实测 `grep -c 'FIX-07' 字段 Spec` = **0** ⇒ 母 `:716` 称「随 §1 迁出」的承接方仍零锚点 |
| CR / TL | 字段 m2 / 字段 m4 (母 Spec 字段在 `:12` 应为 `:13`) | **已落** | 字 §5 表 `:463`「**OK** (`:13` token 串 `10CG/Aria#174` —— **真 token**…R6/KM m2)」; 母 `:83` / FIX-19 `:737` 均已写「第 **13** 行」 |
| TL | 字段 m5 (`:469` 同格自相矛盾的失效引文) | **已落** | 字 §5 表探针行 `:472`「(2026-08-25 实读其 `:6` 为中文哨兵形; 2026-08-30 已改 `> **Linked Issue**: \`none\` —`, R6/TL m5 订正失效引文)」 |
| CR | 字段 m3 (「共 10 条 check」vs 实测 11) | **已落** | 字 `:328`「实读 `.aria/state-checks.yaml` (共 **10** 条 check (2026-08-25 当日观测; §4 骨架注已记 08-30 前后为 11, 以命令为准)…」 |
| CR / TL | 探针 m1 / 流程 (「请 R4 优先审」残留) | **已落** | 三份 `请 R4 优先审` / `请 R4` / `给 R3` 命中均为 **0**; 探 `:138` 已改为「**⚠️ 本条是 R3 之后新增的订正 (未经审计轮) —— 请审计席优先审 (R4–R6 已审)。**」 |
| CR | 探针 m1 (「本轮最实的跨 Spec 风险」段尾自相矛盾) | **已落** | 探 `:561`「**⚠️ R3/M7 状态更新 (主控 2026-08-25)**: 本条原自陈「单方面声明、未交叉核对、本轮最实的跨 Spec 风险」。**该风险已闭环**…」—— 段尾旧断言句已并入撤销说明 |
| CR | 探针 m3 (`read_only` 来源未定义) | **已落** | 探 `:219`「**`read_only` 的来源**: `.aria/config.json` 的 `state_scanner.multi_remote.read_only_remotes` (缺省空元组; 实读 `collectors/multi_remote.py:1376` 生产调用即如此取值, R6/CR 探…)」 |
| TL | 探针 m7 (SC-20 正则 `.*` 前缀不禁 `Step 0.5:`) | **已落** | 探 SC-20 `:506`「正则 `(?m)^#{2,4}[ \t]+per-round 入口探针`, **锚定标题起首, 不允许 `Step 0.5:` 之类前缀** —— R6/TL m7」 |
| TL | 探针 m6 (`audit-engine/SKILL.md:236-237` 锚点多含一行, 被引句只在 `:237`) | **未落** | 探 `:531` 实读仍为「…与本 skill 既有 progressive-disclosure 体例一致, `SKILL.md:236-237`「权威可执行版见 references/…」」—— 行号区间未收窄到 `:237` |
| QA | 母 m2 (SC-15 负控 track_id 前缀夹具约束) | **未核 (断线前未到)** | — |
| BA | 母 m1 (`get_container_uuid` 复刻样板, 建议抽 helper) | **未核 (断线前未到)** | — |
| KM | 母 m2 (dogfood `none` 与生产 ref 真实 claim 不一致) | **已落** | 母 `:13`「**Linked Issue**: `10CG/Aria#174` — 本 Spec 的立项 issue…生产 coordination ref 里本轨两条 claim 的 `linked_issue` 即此值 —— R6/KM m2 抓到头部曾写哨兵 `none` 与之不一致, 2026-08-30 订正为真 token」 |

---

## (c) 任务 B — 九对交叉一致性

### 对 1 — 真 token 四处一致 ✅ **一致**

| 处 | 当前行号 | 逐字 |
|---|---|---|
| 母头部 | `:13` | `> **Linked Issue**: \`10CG/Aria#174\` — 本 Spec 的立项 issue…2026-08-30 订正为真 token` (`cat -A` 逐字节确认 `10CG/Aria#174` 在 inline-code span 内) |
| 字段 §5 作用域表 | `:463` | `\| a1-entry-claim-duplicate-work-guard (母 Spec) \| **OK** (\`:13\` token 串 \`10CG/Aria#174\` —— **真 token**: 2026-08-30 由哨兵改为立项 issue, 与生产 claim 的 \`linked_issue\` 一致; R6/KM m2) \|` |
| 母 §Why 落盘后现状 | `:83` | `本文件按 FIX-19 补了**真的**字段 (第 **13** 行, 现为 \`> **Linked Issue**: \`10CG/Aria#174\`\` —— 英文 canonical + 真 token)` + `前者真 token, 后两者哨兵 \`none\`` |
| 母 editlist FIX-19 | `:737` | `本文件 \`> **Linked Issue**: \`10CG/Aria#174\`\` (第 **13** 行; …rework v4.1 把哨兵改为真 token —— 生产 ref 里本轨 claim 的 \`linked_issue\` 即 \`10CG/Aria#174\`, R6/KM m2…)` |

四处口径一致 (真 token, 非哨兵), 行号一致 (`:13`), 且都点名 R6/KM m2 为来源。字段 §5 同表另两行仍写两子 Spec 为哨兵 `none`, 与 母 `:83`「后两者哨兵 `none`」对得上。

### 对 2 — SC-22 新版 ↔ §2 触发时机 ↔ Impact `phase-a-planner` ↔ D17 ✅ **自洽**

- **求值域不再互斥**: SC-22 `:612`「**②③④⑥⑦ 只在该切片内求值; ⑤ 是切片外的独立断言** (R6/TL C1: 旧写「②–⑥ 只在切片内」与 ⑤ 互斥)」, 与 D17 `:506` 第 1 要件「切片外的独立断言须**显式声明**其求值域」互为呼应。
- **落点不再欠定**: SC-22 同行「**新标题的落点钉死: 放在 `### 步骤执行` (`phase-a-planner/SKILL.md:60`) 之前**, 使切片止于 `:60`、不吞下步骤表 (§2「不塞进 YAML 列表」)」; 母 §2 `:127`「**不塞进现有 A.1 的 YAML 动作列表**」; 母 Impact `:666`「A.1 **独立标题级** `前置: REQUIRE claim (A.1, MUST)` 步骤块, **放在 `### 步骤执行` (`:60`) 之前**」—— 三处同一落法, TL 母 C1 的「实现者甲/乙」分叉被消除 (甲的落法被明文选定, 乙的落法被 §2 + Impact 双向排除)。
- **第 7 条续行折叠 ↔ §2 模板续行形对应**: SC-22 第 7 条「§2 的模板是多物理行反斜杠续行形, 断言须**先做续行折叠** (`\\\n` 连同后续缩进折成一个空格) 再判, 单行正则直接判会误红」; 实读 母 §2 模板 `:103-109` 确为六物理行反斜杠续行, `:103` 逐字 `python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \`, `:105` 逐字 `  --phase A.1 --mode advisory \` ⇒ 折叠后**同时**含 `python3` 起首 / `phase1_gate.py` / `--phase A.1`, 第 7 条可满足且不误红。**对应成立。**
- **字面量计数一致**: SC-22 第 2 条自称「**七个字面量**」, 实际列出 7 个 (`phase1_gate.py` / `--linked-issue` / `--include-terminal` / `--phase A.1` / `--raw-track-id "<spec-slug>-<container_uuid>"` / `--emit-arg` / `未能核实`); Impact `:666` 同步写「七个字面量与完整命令行见 SC-22 ①–⑦」。
- **D17 适用范围与三消费者自述一致**: D17「母 SC-22 落 ①②③ / 字段 SC-7a 仅 ① / 探针 SC-20 落 ①②③」↔ SC-22 头「本条落 D17 ①②③」↔ 字 SC-7a `:546`「引母 Spec D17 —— **只落 ①**…②③ 对骨架块不适用, D17 适用范围」↔ 探 SC-20 `:506`「引母 Spec **D17**, 落 ①②③」。四处对得上。

### 对 3 — 省略门统一 ✅ **一致 (五处同一判据)**

母 `:111` (四态整参省略) · 母 SC-12 `:585` (场景限定为「判 `OK` 且非哨兵」+ 反向句) · 母 §6 首行 `:463` (缺口扩为四态) · 母 rule6 (a) `:534` (「只有字段判 `OK` 且非哨兵才传」) · 母 `:125` (两阶段取法, `--emit-arg` 存在则用 stdout, 否则按 E6 手工判) —— **五处口径完全一致**, 与字段 E6 `:211-218` 的「一句话判据」同义。
**归属不再悬空**: 母 `:125`「**该模板行归本 Spec Impact** (`phase-a-planner` / `spec-drafter` 两行), 字段 Spec 只负责 `--emit-arg` 模式存在 (其 SC-9); 两份 Spec 任意顺序 ship 均自洽, 不存在第二次编辑。」↔ 字 §非目标 `:551` 仍写「不做 A.1 入口认领…母 Spec 范围」↔ 字 Impact 探针行仍只声明脚本存在 —— **两侧不再重叠也不再留空**, TL 跨 C5 的「无人认领」形状消除。字 `:602` 旧括注「(母 Spec §2 一句)」现在在母 `:125` 有真实对应文本, 悬空引用消除。

### 对 4 — SC-32 ↔ Impact 两行 ↔ §非目标 ✅ **不再互斥**

Impact 第一处 `:663`「**除 `--raw-track-id` 的 `required` 见第二处变更 ⑦ 外零改动**」—— 「零改动」措辞已加例外限定; Impact 第二处 `:664` 第 7 项把 `required=True → required=False + _main() 内模式校验` 登记为本 Spec 的显式变更, 并写死负控「非 `--heartbeat-only` 模式缺参仍 `parser.error(...)` (acquire 路径的 fail-fast 不放松)」; SC-32 `:622`「坏实现 1」把 argparse 层失败明写为必红臂。**BA 母 M1 指出的「argparse 早于应用层退出」这条更根本的失败模式已被 SC 覆盖。**
与 §非目标的关系: `:664` 的负控句 (acquire 路径 fail-fast 不放松) 正是 §非目标「不动 Phase B 入口现有认领 / 不改 acquire 路径」的守卫条款 —— **TL 母 C3 第 2 点 (「摘掉 required 对 `--phase B` 的 acquire 调用同样生效」) 已由该负控闭合**; 三种落法的欠定 (TL C3 第 3 点) 由「三种落法中**钉死 (a)**…不用 subparsers、不拆独立脚本 (旧写…作废)」闭合。与 `--phase` 的不对称也已给出理由 (heartbeat 模式 `--phase` 有占位值可传, `--raw-track-id` 没有值可传)。

### 对 5 — §5.2 两新行 ↔ §2.3 选项措辞 ↔ D6 ✅ **一致**

§5.2 `:448` 并轨行「对方那条**不由本容器释放** (D6: 不引入跨容器 release), 成文接受它挂到 `--sweep-stale`」↔ §2.3 `active` 格「**请对方容器的 owner 释放其 claim 后再开始**」(人工协作动作 —— 本容器**无**任何可执行命令: 实读只有无差别 `--sweep-stale`, 无定向 release, D6; R6/TL M3 改措辞) ↔ §2.3 尾「**跨容器 release 不在本 Spec 引入**」↔ Impact follow-up #6「跨容器**定向** release \| 写别人的 claim 是权限面变更, 应独立评估 (D6)」。**四处同一立场。**
§2.3 `done` 格「⇒ 按 §5.2 走 `release_gate.py --raw-track-id "<本轨 A.1 原串>" --status abandoned`」现在指向 §5.2 `:449` 的真实行 —— **TL 母 M3 点名的「指针指到不存在的行」已闭合**。

### 对 6 — hunk B placeholder ↔ SC-7a ↔ SC-6 ↔ §1 Usage Note ✅ **一致**

hunk B 两处 (字 `:144` 落版说明 / 字 Impact `:574`) 均写 `` > **Linked Issue**: `{<org>/<repo>#<n>}` `` 并注「placeholder 与 SOT 同串」; SC-7a `:546` 第 (ii) 臂负控「值**不得**是哨兵集合成员 (`none` / `无`), 须为 SOT 同串 placeholder `` `{<org>/<repo>#<n>}` ``」且「怎么会红」列点名「骨架默认写 `none` 的实现 (把正证据做成默认值) ⇒ (ii) 红」; SC-6 `:544` 断言 SOT 模板含 canonical 字段行 + `## Template Usage Notes` 段含「无关联时逐字写 `` `none` ``」并明写「⚠️ 本条**不断言** E5 (D8: 模板值是 placeholder)」。
⇒ **三处口径统一**: 模板与骨架的**值**都是 placeholder (判 `BAD_TOKEN`, 被 check 点名), 「无关联写 `none`」只出现在 Usage Note 的**教学文字**里, 不是默认值。与 D8 (`:497`「模板里用 placeholder…不要求模板自身过 E5」) 一致。

### 对 7 — 探针 §3 唯一 import 代码块 ↔ Impact「跨 skill 复用」段 ↔ SC-21 ✅ **只剩一份, 顺序一致**

探 `:160-164` 是**唯一**一份合并后的完整代码块 (两条 `sys.path` 插入 + 三条 import 同处), 顺序注释逐字「`for _p in (_SS_SCRIPTS, _SS_ROOT):   # 顺序承重: 最后插入的 _SS_ROOT 排在 sys.path 最前 (R6/BA 探针 M1)`」; Impact `:537` 逐字「**跨 skill 复用的形态 —— 已在 §3「跨 skill import 的可运行模式」逐字钉死, 本段不再另说**」⇒ 第二份片段已撤; SC-21 `:507` 的坏实现臂逐字「把 `_SS_SCRIPTS` 插在 `_SS_ROOT` **之后** (即排在 `sys.path` 更前) 的实现 ⇒ `lib` 绑定到 `scripts/lib` ⇒ `ModuleNotFoundError: lib.collision` ⇒ 红」—— **与代码块的顺序方向一致** (代码块用 `for` 元组顺序 `(_SS_SCRIPTS, _SS_ROOT)` + 每次 `insert(0, …)`, 故 `_SS_ROOT` 最终排最前 = SC-21 期望的安全序)。

### 对 8 — 探针 SC-17 ↔ Impact `execution-modes.md` 行 ↔ SC-20 (ii) ✅ **一致**

SC-17 `:503` 计数域已收窄到「两节的围栏块切片」+ 负控「除这两处围栏外, 全文 (**含新增的 `## 竞品 spec 探针 (per-round 入口)` 契约节**) 该字面 **0 次** —— 契约节用「探针的 stdout 契约如下」之类措辞, 不复用该前缀」; SC-20 (ii) 断言的是**契约节存在 + 其切片内含 §7 三字面与 §9 三档措辞字面**, 断言对象与 SC-17 的计数字面 (`每轮入口: 竞品 spec 探针`) **不重叠** ⇒ 正确实现同时满足两条, 不互相判红。TL 探针 M7 的「一个完全正确的实现会被判红」形状消除。

### 对 9 — `Part A1` 处置三处 ✅ **统一撤回**

母 §2 触发时机 `:127` / rule6 #8 `:522` / Impact `branch-manager` 行 `:672` —— 三处逐字都写「标题不改」+「rework v4 曾按 R5/M2 的误读落成改名, R6/CR M1 撤回」+ 同一理由 (部件名 vs Phase A.1, 引归档件 `:35,:50`)。母 `:127` 另补了替代守法:「SC-22 ① 要求新标题含带点的 `A.1` 且 ④ 禁 `--phase B`, 足以与它区分」—— 与 SC-22 `:612` 第 1/4 条对得上。**无残留改名指令。**

### 新矛盾 (1 条)

**N-1 — 决策单声称「母 §2.3 已钉死 `unattended` 取值路径」, 母 §2.3 实读仍并列两条路径**

- **决策单侧** `.aria/decisions/2026-08-30-…md:93` 逐字:
  > `| §3-9 / M4 | \`unattended\` 取值路径钉死或整条删 | **已采纳前者**: 钉死为 aria-runner 镜像内 \`.aria/config.json\` (母 §2.3), env 三腿仍 follow-up | R6/CR M8 同判 |`
- **母 Spec 侧** `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:270` 逐字:
  > `> **判据 (可机械)**: \`state_scanner.coordination.unattended == true\` (**新 config key**, type boolean, **default false**; 在 \`config-loader\` 登记并在 \`DEFAULTS.json\` 注册, 由 aria-runner 容器镜像 / Nomad task env 显式置 true) ⇒ 走本分支…`

「容器镜像 / Nomad task env」仍是**并列二选一**, 未钉死任一条; 而母 `:275` 同段仍写「**Layer 1→2 的 env 传递三腿契约**…**不在本 Spec**」。⇒ CR 母 M8 点名的原病 (「实现者按后者读时 SC-26 只在夹具里为真, 生产分支永不进入」) **在母 Spec 上原样存活**, 决策单的「已采纳」是一条**在目标处不成立的跨文档声称** (memory `cross_doc_claim_verify_at_target`)。这条矛盾是清账当轮**新写**的 (决策单 `:82-93` 的台账是本轮为回应 CR 流程 m1 才建的)。
**处置建议 (只建议)**: 把母 `:270` 括注改为「由 aria-runner **镜像内 `.aria/config.json`** 的 `state_scanner.coordination.unattended: true` 置真 (env 三腿见 follow-up #5, 不在本 Spec)」, 与决策单 `:93` 逐字对齐; 或反向把决策单 `:93` 改为「待 A.2 钉死」。**一处两行的文本改动, 不动任何机制。**

---

## (d) 任务 C — 机械复跑 (**由主控提供, 本席未复跑**)

> 本席在该步骤上被 watchdog 断线, 按主控指示直接引用其已跑结果, **未独立复跑 `verify_spec.py`**。

**`python3 verify_spec.py <proposal.md>` — 三份全部 `PASS`**:

| Spec | 不变量 1 (每个 `SC-NN` 在 SC 表内有一行) | 不变量 2 (每个 `--flag` 在 Impact 节内被点名) | 行号存在性 (aria `d50f9c3`) |
|---|---|---|---|
| 母 `a1-entry-claim-duplicate-work-guard` | ✅ 34 条 SC 全部有表行 | ✅ 正文全部 `--flag` 均在 Impact 内 | ✅ 80 条 file:line 全部存在 |
| 字段 `linked-issue-field-availability` | ✅ 9 条 | ✅ | ✅ 23 条 |
| 探针 `sibling-spec-probe` | ✅ 21 条 | ✅ | ✅ 26 条 |

**残留 grep** (同样由主控提供):

| 模式 | 期望 | 结果 |
|---|---|---|
| `派生形` / `回落形` / `track_form` / `spec_slug` | 只在撤销说明与审计轨指针 | ✅ 符合 (全部落在 ⛔ 行 / 「已随 1A 撤销」/ 「不新增」/ 审计轨 §6 指针) |
| `wu_empty` | 只在改名说明 | ✅ 字段 1 处 / 探针 2 处, 均为「原 `"wu_empty"`, 2026-08-30 改名」 |
| `Part B1` | 只在「撤回改名」的说明里 | ✅ 母 2 处 (`:134` / `:507`), 均为「= `linked_issue` 部件」的正确用法 (**本席另核**: 撤回说明本身在 `:127` / `:522` / `:672`, 用的是 `Part A1` 不改) |
| `请 R4 优先审` | 0 | ✅ 三份均 0 (**本席另核**: `请 R4` / `给 R3` 亦均为 0) |

---

## (e) 本席判断: 清账后能否交 owner 批准进 A.2

**verdict: PASS** —— 就本席被授权判的两件事而言:

1. **R6 点名的项是否落干净**: **是, 实质落干净。** 8 个 critical 簇 6 个已实文落地 (证据见 (b) B.1, 全部实读逐字), 另 2 个 (探针依赖方向 R6-1 / 字段名折叠 R6-2) 按 Rule #10 正确地**上呈而非自裁** —— 这两条本来就是 CR / QA 两席自己标注「属 owner 决定」的范围决策, AI 自行拍板反而违规。28 条 Major 逐簇核完全部有实文落点, 无一条停在「Impact 括注声称 SC 已改而 SC 没动」这种 R5 判「不可进 A.2」的形状; 带锚点的 minor 中 13 条已落、1 条部分落、1 条未落 (探针 m6 行号区间)、2 条本席断线前未核。

2. **是否有新矛盾**: **只有 1 条, 且是文本层。** N-1 (决策单声称母 §2.3 已钉死 `unattended` 取值路径, 母 `:270` 实读未钉) 是一处跨文档声称在目标处不成立, 改两行即闭合, 不触及任何机制或 owner 已裁的六项。九对指定核验中另外八对全部自洽 —— 尤其 memory `fixes-contradict` 最担心的「A 条修好但违反 B 的隐含前提」在本轮**没有出现**: SC-22 的三条修复 (求值域 / 落点 / 第 7 条) 彼此相容且与 §2、Impact、D17 四面对齐; SC-32 的松绑与 §非目标由一条显式负控接住; §5.2 两新行与 D6 的边界一致。

**给 owner 的一句话**: 建议**带 3 个待办批准进 A.2** —— (1) 裁 R6-1 / R6-2 两项 (它们决定探针 Spec 能否独立排期、以及字段 SC-1 是否加一个分支), (2) 让执笔席顺手闭掉 N-1 与探针 m6 / `FIX-07` 两条 minor (三处共约 4 行), (3) A.2 起草前按母 Impact `:652` 自己的提醒重新 fetch aria (行号基线 `d50f9c3`, 主仓 gitlink 现指 `58a49e7`)。**本席不建议再加通用审计轮** —— 与 R6 五席中 CR / TL 两席的收敛判断一致, 本轮定向复核已把「落没落」这个问题回答完, 再跑通用轮只会重新产出同形自伤。

---

**本席未修改任何被审文件, 未 `git add/commit/push`, 未动 aria 子模块工作树。唯一写入 = 本报告。** 全部行号可在主仓当前工作树 (三份 proposal 均 `M`) 与 aria `d50f9c3` 上按 (b)(c) 各格的命令重跑。
