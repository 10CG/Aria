---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T19:55:35.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [backend-architect]
---

# post_spec 审计报告 (Round 4) — pre-merge-completeness-gate-change-scope · 席位 backend-architect

席位透镜: 数据契约与实现可行性 (字段语义变更的消费方枚举 / 错误路径穷举 / 判据与真代码结构对齐)。本轮只审不改, 未编辑任何仓库文件 (`git status --porcelain` 空)。所有事实断言均自行实读或实跑, 不采信 proposal 自述。

## 审计结论

### Decisions

- [minor] testing/§1.2 与 §1.4 计数契约的语料复算: 本席对活体语料 (顶层 837 份 `.md`, `C`=153) 独立实现规则 1-3 复算, 得末段族 **62** / 真 legacy **6** / unattributed **170** (全 8 checkpoint 口径) 与 **160** (本仓 `checked={post_planning,post_spec}` 口径) / 多归属 **0**, 与文中逐字吻合; 归属 650 + legacy 6 + unattributed 170 = 826 = 带 checkpoint 前缀的文件数, 三桶互斥且穷尽 (证据: proposal.md:154,239 与 `.aria/audit-reports/` 实跑)
  - 附带验证: 有界包含排除 (规则 3) 对末段形态同样生效 —— 我构造前缀/后缀/中缀三型代入均无双重归属, SC-3 的三型断言可实现。
  - 附带验证: `openspec/archive/` 146 条目中只有 `README.md` 无 `YYYY-MM-DD-` 前缀 ⇒ S1 的「去日期前缀后逐字相等」在本仓语料上 100% 成立, 不会与写盘侧 `pre-write-validation.md:25` 的 glob 产生现存分歧。

- [minor] documentation/R3 缺陷落地核验: R3 的 C3 + M12 共 15 条均落进正文实体改动 (非批注), 本席逐条定位 (§1.0 求值总序 / §1.3 2b-2d + 级 3 / §1.1 S3 三条核验 + `--anchor-base` / §1.4 stderr 通道 + 格 B 人群 / SC-13 分块计数 / Tasks unittest 与 B.0 仲裁规则 / 复议 #4b + #10); 判据 1 的「首命中 >15 恰 7 份」与行首形态 **139/3/2/0** 我实跑复算一致, 聚合席的 6 份与「其它 1」确系宽正则伪影 (证据: proposal.md:180-181, rework-R3.md 条目 A1)

### Issues

- [major] implementation/§1.0 P3 与 §1.3 Level 取法: 求值总序把 Level 解析写成无条件的 P3, 而同一份 spec 另外两处按「仅 adaptive 档需要 Level」写, 三处不能同真 (证据: proposal.md:98,103,186,286)
  - `:98` P3 逐字「逐 change 解析 Level N (§1.3)」, 依赖只有 P2, 排在 P4 之前 = **eager**。
  - `:186` 的 ERROR 文案给的第二个 fix 是「在 `audit.checkpoints` 里显式写该 checkpoint」——只有 **lazy** (显式档不解析 Level) 时该 fix 才有效; `:286` §5 第 6 条同样限定「`audit.mode="adaptive"` **且某 checkpoint 无显式值时**」才读 proposal 取 Level。
  - `:103` 硬约束 (2) 只要求「凡 `mode` 走 adaptive 档的 fixture」补可解析 Level 行 —— 这条指引只在 lazy 下成立。若 Phase B 照 P3 字面实现 eager, 则 SC-8 (`mode:'manual'` + 显式 checkpoints + 「锚点」但未要求 Level 行) / SC-16 / SC-9(1)(2)(3) 这批 fixture 会全部落 `spec_level_undetermined` exit 2, 与各自期望的 exit 0/1 冲突 = 与已判 Major `3f817a3b` 同型的「Phase B 结构性必红」。
  - 生产面后果同样可达: 本仓 `.aria/config.json` 的四个非排除 checkpoint **全部显式** (实测 `post_spec`/`post_planning`=convergence, 其余 off), Level 永不被消费; 但 eager 下只要被审 change 的 proposal 无可解析 Level 行 (真实语料实测 **9/153**) 即 exit 2 硬阻, 且文案给的 fix 无效。
  - 建议: 把 P3 改成「按需解析 (仅当某对落到级 2a 时)」并同步 `:103` 的 fixture 指引; 「循环依赖」不因此复活 —— Level 来源是 `proposal.md`, 与 `resolved_mode` 无环。

- [major] architecture/§1.4 格 B 判据: 第四个合取项对**空**纳入集做全称量化, 两种读法各有一个坏后果, 且无 SC 区分 (证据: proposal.md:233; config-loader/config-example.md:276)
  - 逐字是「纳入集空 **且** 该空集的每一项 `enabled_by` 都是 `explicit`/`manual-default`/`adaptive:level_{N}` 之一」。空集上「每一项…」**真空成立** ⇒ 该合取项恒真 ⇒ spec 把它记为「补上之后本格再无法被非配置决定的空集触及」的守卫实际是 inert; 真正封口的是级 3 改判 `config_unreadable` exit 2。
  - 若按括注的意图读成「每个**被解析**的 checkpoint 的 `enabled_by`」, 则存在可达输入落不进任何一格: config `{enabled:true, mode:"convergence", checkpoints:{post_brainstorm/post_spec/post_planning/post_implementation 四键显式 "off"}}` —— 四个非排除项显式 off ⇒ 纳入集空; 四个排除项 (`pre_merge`/`post_closure`/`mid_post_spec`/`mid_implementation`) 走 2b 得 `mode:convergence` ∉ 允许集 ⇒ 格 B 假; `resolved(pre_merge)="convergence"` ≠ off ⇒ 格 C 假; `enabled=true` ⇒ 格 A 假。**三格穷举失败**, 行为未定义。
  - 这正是本 spec 反复清扫的那一族缺陷 (同一份判据两个合法实现判决不同), 且是 R3 修 Critical `7877bac6` 时新加的文本。建议: 把量化对象改写成「每个被解析 checkpoint 的 `enabled_by`」并把 `mode:convergence`/`mode:challenge` 的处置显式写死 (它们结构上不产生空集时应说明, 或补一格兜底), SC-15 补该 config 形态一格。

- [major] architecture/§1.1 S2 作用域解析面: R3 把 S3 核验面移到锚点仓的同一条理由未同步给 S2, 使 `scope_source=diff` 在自述主力场景下结构不可达 (证据: proposal.md:81,82,84,110,339)
  - `:81` 定义 `--diff-repo-path` = 「只用于 `git diff`/`merge-base`」, S2 (`:110`) 未另行指定仓 ⇒ 用 diff 面 + `--base`; 只有 S3 被 R3 改成锚点面 + `--anchor-base` (`:84`)。
  - 我实测 `aria/openspec` 与 `aria/.aria` **均不存在** (与 proposal 一致) ⇒ 子模块 PR 时 diff 面永远取不到 `openspec/changes/<id>/` 前缀 ⇒ S2 恒空 ⇒ 必落 S3/S4。SC-5(5) (`:339`) 已顺带承认这一点 (「跨仓时 S2 从 diff 仓解析不到本仓的 change 目录」), 但只写在 fixture 注里, 不是契约, 也无 SC 断言。
  - 连带失效: S4 (`:111`) 的 ERROR 文案给的第二个 fix「在分支里带上 change 目录变更」在跨仓形态下不可执行 (往子模块分支加 change 目录不会进 diff 面的 `openspec/`)。
  - `:84` 给 S3 的理由逐字是「Rule #5 规定 spec 落主仓, `openspec/changes/**` 的家本来就在锚点仓」——「本 cycle 的 spec 是哪几个」与「本 cycle 有没有 spec」是同一个问题面。`:82` 自己也写着「本 cycle 主仓 diff 全是 `openspec/**` 而代码全在子模块」, 即锚点面 S2 本可正确解析。建议: S2 改取锚点面 (或锚点面优先、diff 面兜底), 并补一条跨仓无 `--change-id` 的 SC; 若刻意保留现状, 需把「跨仓下 S2 恒空、必须显式传 `--change-id`」写成契约并改 S4 文案。

- [major] implementation/§1.3 判据 2 与实跑校准段: 校准数字与同节新增的删除线剥离规则自相矛盾, 且「无取值漂移」的结论被该规则自己的例子证伪 (证据: proposal.md:181,184; openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:13,29)
  - `:184` 写「上述判据对 153 份的结果 = 解析成功 144 (Level 3 → 57 / Level 2 → 86 / Level 1 → 1)」。我按 `:180-181` 三条判据 (含 `:181` 新增的「取值前先剥 `~~…~~`」) 实跑: **144 成功 / 9 失败**一致, 但分布是 **L3 58 / L2 85 / L1 1**; 不剥删除线才得 57/86/1。⇒ `:184` 引用的是**未含**本节自己新增子规则的旧结果。
  - 同句「另实跑『严格判据 vs 原稿宽松正则』逐份对照, 144 份取值**逐个相同**, 判据收窄未引入取值漂移」同样为假: `premerge-gate-branch-existence` 的 `:13` 叙述句含 `Spec Level: 2`, 宽正则先命中取 **2**; 严判据落到 `:29` 的 `> **Spec Level**: ~~2 (proposal only)~~ → **3**` 剥线后取 **3**。这恰是 `:181` 自述「不剥就静默取错值」的那一例。
  - 影响: 该段是判据 1/2 的经验支撑, 也是 Phase B 判断「要不要实现剥线」的依据; SC-20(4) 虽已单独锁死剥线, 但正文留着一句与之相反的实证结论会让执行者二选一。建议: 把分布改为 58/85/1, 把「逐个相同」收窄为「除删除线那 1 例外逐个相同」。

- [minor] testing/SC-1 与 SC-22(2) 输出通道: Major `1b189d49` 的 stderr 清扫遗留两处 (证据: proposal.md:335,356,237)
  - SC-1 (`:335`) 仍写「stderr/stdout 文案含 `post_implementation@x`」。stdout 是 15 键封闭 JSON, `results` 元组字段也是封闭集, **没有任何字段承载 `post_implementation@x` 这个拼接串** ⇒ 若读成合取, 与 SC-10 不可同绿; 若读成析取则无碍。属 `:238`「全部 SC 里『stdout 含文案』的断言一律改到 stderr」漏扫的一条。
  - SC-22(2) (`:356`) 仍用「trail 含 `[WARN] .aria/audit-reports/ 不存在`」——「trail」在 R3 后已不是被定义的输出通道名 (人读行恒 stderr), 建议逐字改 stderr, 顺带与 `:230` 的 WARN 全文对齐 (两处文案长短不一, 现在只能按子串断言)。

- [minor] documentation/§5 行为变更枚举: 自称穷举的八条漏掉「门首次引入 git 依赖」这一类 (证据: proposal.md:281-288,301; audit-engine/SKILL.md:404-405)
  - 改前的门 (`execution-modes.md:54-65`) 只做文件名 glob, 零 git 调用; 改后 `--base`/`--anchor-base` 解析失败或 `merge-base` 失败一律 `git_failed` exit 2 + 消费方 fail-closed ⇒ 浅克隆 / 无远程跟踪 ref / git 不可用的采用方会从「静默通过」变成「硬阻合并」。
  - 同一 skill 的既有约定方向相反: `audit-engine/SKILL.md:405` 对 base 解析失败逐字「全部失败 → file-scope skip + warn, **不 crash**」。这与已列入第 5 条的「坏 config JSON 刻意不同于 config-loader 散文」同性质, 应同样成条。
  - 载重点: 复议 #4b (PATCH vs MINOR) 的论证正是按「§5 自述八条」做的, owner 拿到的行为变更面仍不完整 (方向不改变 MINOR 的推荐, 但改变理由的完整性)。

### Risks

- [minor] architecture/§1.4 stdout 15 键契约: 缺「运行面」字段, 扫描受损与扫完确无同形 (证据: proposal.md:222,237; execution-modes.md:185)
  - `.aria/audit-reports/` 不存在时按零报告继续评估 (`:222`), 只在 stderr 留 WARN; stdout 的 `matched==[]` + `status=missing` 与「目录存在且确实没有报告」逐字节同形。
  - 本 spec 自称镜像的 sibling probe 恰恰为此把**运行面** (`status`: ok/degraded/skipped + `reason`) 与**判定面** (`verdict`) 拆开, 并在 `execution-modes.md:185` 明写「消费方不得从 `hits == []` 推断结论」; 本门只继承了后半句 (`results` 恒 list) 而没继承前半句的字段。
  - 方向是 fail-closed (两种情形都走 missing ⇒ 阻断), 故列 Risk 而非 Issue; 但机器消费方 (未来的 workflow report / dashboard) 无法机读区分环境缺陷与真缺报告。缓解成本极低: 加一个 `scan_status` 或复用 `reason` 即可。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **4** / Minor **3** (另 Decisions 2 条不计入缺陷计数)。

理由: v4 相对 v3 是实质推进 —— R3 的 15 条缺陷全部落进正文实体改动而非批注, 我抽样复算的语料数字 (62/6/170/160/C=153/多归属 0) 与判据 1 的 7 份深行号、139/3/2/0 分布全部实跑吻合, 数据契约主干 (15 键封闭集 / 9 项 `error_kind` / 三桶互斥 / 规则 1-3 无双重归属) 在真实语料上站得住, 消费方枚举经我全树 grep 复核无遗漏 (代码消费方仅 `state-scanner/collectors/audit.py` 顶层 `glob("*.md")` 与 `aria-dashboard/references/parse-rules.md`, 与本 spec 的 depth-1 选择同向)。

但本轮仍有 4 条 Major 落在 R3 修法自身引入的新面上: 求值总序 eager 与两处 lazy 表述互斥 (会让一批 fixture 结构性必红, 且 ERROR 文案给的 fix 无效)、格 B 守卫对空集全称量化 (真空成立 or 三格穷举失败)、S2 未随 S3 一起迁到锚点面 (主力场景下 `scope_source=diff` 不可达)、Level 分布数字与新增的剥线规则相反。四条都不是假绿方向, 故不判 FAIL; 但每条都会在 Phase B 当场变成「两个合法实现判决不同」或「必红一条」, 需在进入 B 之前收敛。

## 轮次记录

### Round 4

- Agents: backend-architect (五席之一, 本报告只覆盖本席透镜)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 9 (Issues 6 = major 4 + minor 2; Risks 1 = minor 1; Decisions 2)
- Vote: **REVISE**

#### 本轮机械核验 (可复现, 全部本席实跑)

1. Level 判据全枚举 (`openspec/{changes,archive}/*/proposal.md`, 按 `:180-181` 三条判据实现): 153 份 → 成功 144 / 失败 9 (9 份与文中点名逐字同集); 首命中 >15 的 **7** 份 (最深 `2026-09-06-a1-entry-claim-duplicate-work-guard` L58) 与文中同集; 含 `Spec Level` 的 **15** 份; 行首形态 `>` 139 / `-` 3 / `#` 2 / 其它 0。剥删除线 → L3 58 / L2 85 / L1 1; 不剥 → 57/86/1 (文中数字)。
2. 归属规则 1-3 全语料代入 (顶层 837 `.md`, `C`=153): 归属 650 (末段族 62) / 真 2-field legacy 6 / unattributed 170; 换本仓 config 的 2-checkpoint 口径 → unattributed 160, legacy 6; 多归属文件 0。
3. `.aria/config.json` 实测: `enabled=true`, `mode="convergence"`, `checkpoints` 7 键 (`post_spec`/`post_planning`=convergence, 其余 off, 无 `mid_post_spec`), 无 `adaptive_rules`, 无两个 `allow_*` 键 ⇒ F1 与 §1.4「本仓实测正是纳入集非空 + `pre_merge=off`」成立, SC-11 可跑 (post_spec 现存 18 份归属本 change, post_planning 0)。
4. SOT 行号抽验 (对 v1.71.1 缓存副本): `execution-modes.md:15/44/46-52/54-61/63-65/82/90/121/159/185` · `audit-engine/SKILL.md:49-54/381-388/391/398-400/404-406/410-411` · `phase-c-integrator/SKILL.md:131/132/133-136/137/157/252/253/260/265/299` · `report-storage.md:8/18/34-39/37/39` · `pre-write-validation.md:14/16-18/20-26/25/28-30` · `config-loader/SKILL.md:8-10/37/305-331` · `config-example.md:276/277/280/381-400/402-417/442` · `DEFAULTS.json:109-152` · `spec_complete.py:924-930` (bash 围栏判据属实) · `collectors/audit.py:52/62-69/245` (顶层 `glob("*.md")`) · `sibling_spec_probe.py:147-151/380/684` · `test_sibling_spec_probe.py:303/319` —— 全部与 proposal 引用一致, 本轮未发现新的行号/引文错误。
5. 消费方枚举复核: 全插件树 `--include=*.py --include=*.json --include=*.yaml --include=*.sh` 对 `allow_incomplete_checkpoints` / `missing_checkpoint` **零命中** (与 §5 一致); `audit-reports` 的代码消费方只有 `collectors/audit.py` 与 `spec_complete.py` (后者只在注释里出现, 非文件名 schema 消费方); `lint_stderr_typed_channel.py` / `collectors/_common.py` 里的「completeness gate」是 Rule #7 stderr 泄漏 lint 的同名不同义, **不是**本门消费方。
6. 边界抽验: 语料无非 ASCII 文件名、无非 `.md` 文件; 子目录恰 2 个 (`wf-r1fix` / `pr19-submodule-scan`, 与 §1.2b 同集); 无 checkpoint 前缀的顶层 `.md` 现存 11 份 (含 §1.2b 点名的 5 份 `*-audit-trail.md`), 三桶都不收的规则对它们全部适用。
7. SC-2 选样硬约束复算: 同 id 同时有 F-a (末段) 与 F-b (role 后缀) 且各 ≥3 的 id 在活体语料里**恰 1 个** (`state-scanner-mechanical`, 6+9=15 份), 且该族 15/15 无 `context:`/`spec_id:`/`change_id:` 独立源字段 ⇒ Tasks B.0(4) 的「最坏样本」判断属实, 规则 (c) 的降级支必被走到。
8. 工作区: `git status --porcelain` 空, 本席未落任何仓库文件 (草稿只写 scratchpad)。
