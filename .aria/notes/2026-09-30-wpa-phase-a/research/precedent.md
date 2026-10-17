# WP-A Phase A 研究笔记: precedent (先例 / 约束 / 规范落点)

范围: `secret-net-l3-and-bypass-paths` (Level 2), 关联 `10CG/aria-plugin#154` / `10CG/aria-plugin#203` / `10CG/Aria#221`。本笔记只给「执笔人可直接引用的约束清单」, 不含设计方案。

标注约定: 【实测】= 我亲跑; 【读码】= 我亲读并给 file:line; 【判断】= 我的判断; 【推测】= 未验证。

## 0 基线与方法

- 基线: 主仓 HEAD `0748dbc` (分支 `docs/secret-net-l3-and-bypass-paths-phase-a`, 工作树仅既有 untracked `openspec/changes/secret-net-l3-and-bypass-paths/`, 其中 `proposal.md` 是 6 行 stub: 标题 + Level/Status/Created/Linked Issue 四字段, LF); aria `268da8f` (v1.74.1); standards `2bc1c4c`。
- 真仓零写入: 收尾前复核 `git status` 主仓仅该既有 untracked 目录, aria / standards 干净。只做读类 git (`for-each-ref` / `ls-tree` / `show` / `log` / `grep` / `ls-files --eol` / `branch -r`) 与一次 `git clone` (源 `.git/modules/aria`, 目的地在实验目录, 用于取得带 `.git` 的真 checkout)。
- 实验目录 `/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/precedent/`: `aria-clone/` (@268da8f 真 clone), `probe_scan_shapes.py` / `probe_guard_baseline.py` / `probe_env_boundary_class.py` / `probe_jq_forms.py` / `probe_jq_shape.py` (凭据类值运行时由 `secrets` 生成, 经 stdin 喂 hook, 只输出退出码 / 是否告警 / 长度; 命令文本类探针不执行命令)。

## 1 归档先例

### 1.1 清单与相关度

`ls openspec/archive | grep -i -E 'secret|credential|echo|guard'` 命中 12 份, 其中 2 份是关键词撞名 (`2026-06-11-audit-drift-guard`, `2026-09-06-a1-entry-claim-duplicate-work-guard`), 与本案无关。

| 归档 Spec | 级别 / 发版 | 与 WP-A 的关系 |
|---|---|---|
| `2026-05-07-aria-secret-hygiene-rule` | L2, doc-only | Rule #7 起点; Path 1 (doc) / Path 2 (skill) / Path 3 (hook) 三路模型; Path 3 hook 明确延后 (`proposal.md:179-188`) |
| `2026-05-23-aria-secret-guard-plugin-default` | L3, v1.24.0 | 两个 hook 的来源 (SilkNode PR #429 cherry-pick `8eef709`); `Write`/`MultiEdit` 只占注册位、脚本 pass-through; aria-doctor 状态 schema 只可 append |
| `2026-06-19-secret-guard-exfil-coverage-iteration` | L2, v1.47.0 MINOR | substitute 框定的「历史先例」(08-02 Spec 点名引用), Rule #6 行 `:9` / `:54` |
| `2026-07-03-secret-scan-honest-downgrade` | L2, v1.51.0 MINOR | **L3 (secret-scan) 现状的来源**: PostToolUse 只能 detect+warn, 不能 redact |
| `2026-07-11-secret-guard-multiline-and-anchor-fix` / `...-bash3-multiline-hardening` | L2 v1.55.2 / L3 | bash 3.2 + zsh re-exec + NUL 分隔字段提取; 后者把「PreToolUse secret-guard」按 blast radius 定 L3 (`:21`) |
| `2026-07-16-state-scanner-snapshot-stderr-secret-leak` | (非 hook) | 给出「哨兵运行时拼装」与「RED fixture 打错靶」两条教训 |
| `2026-08-02-secret-guard-nomad-var-put-echo` | L2, v1.65.4 | **owner 对 hook 走 substitute 的框定原文**; 并明确拒绝过「BLOCKED 文案加 per-pattern 建议」 |
| `2026-08-18-secret-guard-per-segment-evaluation` | L2 (巨型, 10 版), v1.66.1 | SC-8 性能闸 / SC-19 family census / SC-9a+9b 双腿 / 三组件 substitute 表 |
| `2026-08-22-secret-guard-manifest-precision` | L2, v1.66.4 | **最近邻先例**: 清单缺口 (双平面) + credit 收紧 + 误报前置白名单; 与 WP-A 的 203 / 221 两半同型 |

### 1.2 三份 rule6_note 逐字

**(a) `2026-08-02-secret-guard-nomad-var-put-echo/proposal.md:126-141`** (owner 2026-08-02 框定):

> `:128` **框定裁决 (owner 2026-08-02)**: 走 **substitute 框定**, 与同一 hook 的历史先例 `openspec/archive/2026-06-19-secret-guard-exfil-coverage-iteration/` 一致。前一版曾写成「Rule #6 不适用 — Rule #10 白名单第四类·结构性前提不成立」, R4 code-reviewer m-3 指出该框定与提供 substitute 逻辑上二选一, 且与先例不一致; 按 Rule #10「AI 自作主张的流程判断须请复议」上报后由 owner 裁定统一为本框定。
>
> `:130` **Rule #6**: deterministic detector hook → structural fixture + unit-test corpus + dogfood (per memory `feedback_deterministic_structural_skill_rule6_substitute`); **不**走 `/skill-creator` AB —— hook 非 capability skill, 无 SKILL.md / 无 description / 不参与 skill 触发, AB 套件的被测对象 (触发准确率 / 输出质量 / token 效率) 与之无交集。
>
> `:132-139` substitute 实证表四行: structural fixture (RED→GREEN, 未加 pattern 时 7 条断言 FAIL) / corpus 零回归 (347 -> 366) / 真 hook dogfood (起草期间真实撞到 5 次) / **指令面未触碰 (可证伪)**: `git diff` 显示 `secret-guard.sh` 仅 +10 行且全部落在 risky_patterns 数组内, BLOCKED heredoc 零改动。
>
> `:141` 跨仓核实: 本 cycle 零 SKILL.md 改动。

**(b) `2026-08-18-secret-guard-per-segment-evaluation/proposal.md:552-564`**:

> `:554` **Rule #6**: deterministic detector hook → structural fixture + unit-test corpus + dogfood (memory `feedback_deterministic_structural_skill_rule6_substitute`); 不走 `/skill-creator` AB (hook 非 capability skill)。框定与 owner 2026-08-02 对 `secret-guard-nomad-var-put-echo` 的裁定一致。
>
> `:556-562` 三组件逐一兑现表: structural fixture = SC-1 / SC-6 / SC-4; unit-test corpus = SC-5 / SC-2 / SC-3 / SC-11 / SC-15; **dogfood = SC-9a (canonical 直调, pre-merge 主闸)**。
>
> `:564` 三组件里最脆的是 dogfood 这条腿 ... 「挑哪几条」本身没有机械约束 ... v9 把它从「一句要求」变成「一张写死的表 + 每类各有能打红它的坏实现」。

**(c) `2026-08-22-secret-guard-manifest-precision/proposal.md:80-82`**:

> `:82` 变更为 hook bash 代码 + 测试 + 文档计数, **零 SKILL.md description/指令面变更**。hook 判定逻辑 AB 套件结构上测不到 (#128 同款先例) -> substitute = 上述 SC-1..SC-6 baseline-failing 结构化测试 (红绿窗口留痕)。SOT: `standards/conventions/skill-benchmark-exemption.md`。

**直接推论**:

1. 三份框定一致; 但 (a) 的第四行「指令面未触碰」是**可证伪锚点**, 只在 BLOCKED heredoc 零改动时成立。`10CG/Aria#221` 要求在拒绝文案加一句「凭据不要放命令行参数」, WP-A 若照办就**不能原样沿用该锚点**, 这正是决策单 §3 (`.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md:42`) 说「提示文案的 hunk 单独判」的原因。
2. 【实测/读码】BLOCKED heredoc 的处方性行 (`Acceptable filters` / `NOT acceptable` / `Reviewed one-off bypass`) 自初版 cherry-pick `e8e847c` (2026-05-23) 起**从未被改过** (`git log -S` 三串均只命中 `e8e847c`); #145 (v1.66.2) 只改了 `Command was:` 与 `Triggering segment:` 两处回显 (数据脱敏, 非处方)。WP-A 将是**首次改处方性文案**, 无先例可抄。
3. 三份 rule6_note 引用的 memory `feedback_deterministic_structural_skill_rule6_substitute` 在本容器 memory store 中不存在 (`ls memory | grep` 与 `MEMORY-archive.md` 均无) —— 引用时应指向上述归档 Spec 原文, 不要只引 memory 名 (与 memory `memory-store-local` 同一结论)。
4. 这六份 hook Spec 全部早于 SOT §4.1 五字段模板 (SOT Version 1.1.0, 2026-09-17, commit `42261a1`); **WP-A 是第一份需要按五字段写 rule6_note 的 hook Spec**。唯一已落地的五字段样例是 `2026-09-17-rule6-description-change-trigger-eval-lane/proposal.md:173-182` (`decision_table_row: n/a` + 其后散文列出 AI 自作主张项)。

### 1.3 各先例的设计要点 / 已知限制 / 延后项

**L3 与输出检测相关 (最重要)**

- `2026-07-03-secret-scan-honest-downgrade`: PostToolUse 架构上不能改写 tool_response (hooks-guide line 891), 所以 L3 = 检测+告警: `hookSpecificOutput.additionalContext` **和** `systemMessage` 两渠道**皆必需** (AC-1 `:90`), `exit 0` always, 零 tool_response 改写键 (AC-3 `:97` 用「结构性缺席」断言防 vacuous-pass)。`:85` 明写**「扩大 secret-shape 检测 regex 覆盖 (检测质量话题, 非 honesty change)」不做** —— 即 WP-A 的 L3 补缺口正是当年划出去的那一块; `:82-84` 结构化事件流 `.aria/secret-leak-events.jsonl` / 置信度分级 block / aria-report 闭环一律归 `10CG/aria-plugin#92`, 并保留 `~/.claude/logs/secret-scan.log` 仅改 tag (SCAN-REDACT -> SCAN-DETECT)。AC-2 (`:91-96`) 是「具名虚假短语零残留 + scope-based 内涵门」: 枚举行号连续两轮漏残留, 换成内涵定义才收敛 (`:110`)。
- `DEC-20260703-001` (`.aria/decisions/DEC-20260703-001-secret-scan-honest-downgrade.md`): 约束表 `:22` 「Rule #7: 告警文本只能提元数据, 不复述 secret 值」; `:44` 置信度分级 block 归 #92; `:74` 降级后要 reframe 为「检测+告警仍有值」而非删除。
- `2026-08-02` 备选表 `:99`: 「PostToolUse `secret-scan.sh` 替代 PreToolUse」被否决 (保留为纵深): 它在事故中确实检出, 但在执行之后, 值已进上下文。
- `2026-06-19` `:61`: 「PostToolUse content-scan REDACT (hook 注释 Phase 2)」长期 out of scope —— 该 Spec 起就把 L3 当「纵深」。

**PreToolUse 清单 / 误报类 (203 / 221 的直接先例)**

- `2026-08-22` (`#179`): 双平面 (Bash 面 reader 行 + Read/Edit 面 `lower_path` 正则) 同时补; credit 收紧只对 claude-config 源 (因 `jq '{...}'` 形状 credit 纯看形状不看字段名); 误报用**前置字符白名单两族** (全名型 / 后缀型) 应用到 14 行, `/`-根名不套白名单 (Amendment-2)。**Phase B 对抗 review 抓到 C-1 真回归** (`cat ${HOME}/.aws/credentials` 由拦变放, 591 全绿是假绿); 教训: 守卫集必须按**名字形态族**穷举 (basename / `/`-根 / 后缀), 自写 fixture + 自写实现 = 自洽假绿 (`docs/handoff/2026-08-22-issue179-secret-guard-manifest-precision-ship-v1.66.4.md:48-49`)。
- `.aria/notes/secret-guard-179-pattern-rows.md`: 逐行枚举「哪些行应用白名单、哪些不」的理由表。**行号已漂移**: 该表记 `python3 -c` / `node -e` 行在 `:785/:786` (基线 `400f0bc`), 现在是 `secret-guard.sh:893/:894` (+108)。结论: Spec 里引行号必须钉基线 SHA (本案建议 aria `268da8f`) 并在 ship 前重取。
- `2026-08-02` 转出 3 / 5 (`:121` / `:123`) 分别是 `10CG/aria-plugin#130` (guard:ack 文案与实现不符) 与 `10CG/aria-plugin#132` (BLOCKED 提示按 pattern 给定向建议, 须先解决 `set -u` 缺省初始化)。`10CG/Aria#221` 要加的拒绝文案与 #132 **同根**; `:96` 决策表曾明确拒绝「加 nomad 专属内容」的理由是「全局共享 heredoc, 会污染 vault / aws 等无关拦截」, `:123` 记 R2 backend M-1 实测「未初始化的 `$pattern_hint` 会让全部 BLOCKED 文案崩成 unbound variable」。
- `2026-08-18` 转出列表 `10CG/aria-plugin#138` (跨段 fail-open) / `#139` (块结构内泄漏) / `#140` (`ssh host '...'` / `sh -c '...'` 外壳逃逸) / `#141` / `#142` (`$(...)` / heredoc 内部) / `#143` (残余误报面) / `#144` (可移植性) / `#146` —— 全部仍 open。`10CG/aria-plugin#203` 的事故原形 (ssh -> pct exec -> sh -c, 内含变量间接) 与 #138 / #140 / #142 同面; #203 自己写明「② 在命令侧基本堵不住, 本事件是 #154 的真实案例」—— 即问题 ② 的**设计意图就是交给 L3**, WP-A 不应试图在 L1 命令侧根治。
- `2026-08-02` 的 SC 体例: SC-8 用 `KNOWN-LIMIT` 命名锁住「已知不覆盖」的现状, 「该用例转红 = 转出已收口」(`:164`); 并要求表述为「部分覆盖」而非「已受保护」(`:104`)。

**流程与审计教训 (影响 post_spec 策略)**

- `2026-08-02` 头部「流程留痕」: R3 审计进行中作者改了被审文件, 致五席读到不同版本 —— 纪律: 审计只审不改, 编辑落在轮间。同头部记录本 cycle「三次未实测即断言」(`-out=keys` 非法 flag 等), 全部由审计方实跑推翻。
- `2026-08-18` 10 版 / R6: 执笔与复核同一人时「勘正里新引入错误」系统性逃逸; 换执笔人; 机械闸取代第七轮。`2026-08-22` 仅 R1->R2 + post_planning R1 + 确认即收敛 (Level 2, 单点问题) —— WP-A 体量应向后者靠。
- `2026-08-22` 归档 frontmatter (`:1-7`) 与 `2026-08-18` (`:1-7`) 都带 `unverified_claims: archive-safety-net-integration-claims-unverified` + `unverified_ack: true` + `unverified_ack_reason` (人工核验证据): hook 类 Spec 归档时归档闸门会给 warn, 需人工 ack 并留证据 (相关 open issue: `10CG/aria-plugin#192` frontmatter 只写不读; `10CG/aria-plugin#206` 纯文档 Spec 恒报假 warn)。
- `2026-08-22` `:108-123` Amendments 体例: mid_post_spec 配置 off 时, Phase B 发现的范围修正由主 loop 追加 Amendment 并请 owner 复议, 不就地自行裁定。

## 2 决策与笔记: 对 WP-A 有约束力的结论

来源: `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` (下称「决策单」), `DEC-20260703-001`, `.aria/decisions/2026-08-24-sc8-absolute-latency-gate.md`, `.aria/notes/secret-guard-179-pattern-rows.md`, `.aria/notes/2026-08-12-secret-guard-128-phaseb-batch1-count-disputes.md`, `docs/handoff/2026-09-30-session-close-urgent-plan-wpc-v1.74.1-shipped.md`, `docs/handoff/2026-08-22-session-close-credential-defense-and-mirror-collisions.md`, `docs/handoff/2026-08-20-issue-batch-...md` §6 续。

| # | 约束 | 出处 |
|---|---|---|
| C1 | WP-A = Level 2; `post_spec` / `post_planning` **均 enabled convergence, 不豁免**; 凭据轮换**不在范围** | 决策单 `:39-42`, `:30-35` |
| C2 | 轮换相关 issue 「保持 open、本项之下不评论」, 不产出轮换清单、不逐条提示 | 决策单 `:34`; 与 `:44-52` 的「issue 评论 / 关闭」一次性授权存在字面张力 (见 open_questions) |
| C3 | 一次性授权仅四类: feature 分支推送 (两 remote + 推后逐个 `ls-remote`) / 开 PR / issue 评论 / issue 关闭。**不含**: 合并到任一 master (含子模块本地 merge 后的推送) / 推 master / tag 与发版 / 主仓 PR 合并 / 删远端分支 | 决策单 `:46-52` |
| C4 | Rule #6: 沿用 owner 2026-08-02 substitute 框定, **提示文案的 hunk 单独判** | 决策单 `:42`; handoff `:50` |
| C5 | 串行推进 WP-C -> WP-A -> WP-B; 文件域与 `10CG/Aria#199` 不相交; 发版串行, 版本号在 ship 时刻取, 合并前重新核 `plugin.json`; 这条顺序是 AI 建议、owner 未单独裁 | 决策单 `:54-59` |
| C6 | L3 只能检测+告警: 不 redact、不 block、`exit 0`; 告警文本只含元数据; 事件流 / 分级 block / 自动开 issue 归 `10CG/aria-plugin#92`, **不在 WP-A** | DEC `:22,44`; 07-03 Spec `:82-84` |
| C7 | 分层: L1 = `10CG/aria-plugin#153` (v1.66.3, 端点锚定 3 pattern) / L2 = `10CG/Aether#317` (wrapper 方法感知 DENY + 打印点脱敏, merge `08d9700`, 只覆盖走 `forgejo` wrapper 的调用) / L3 = `10CG/aria-plugin#154` | 08-20 batch handoff `:69-73` |
| C8 | `10CG/aria-plugin#154` 评论 19339 已把交付物收窄为三件小改动: (1) PATTERNS 增通用键形条目 (键集 token / sha1 / client_secret / secret / password / api_key, 与 L2 wrapper 同一字段清单); (2) FP 白名单 (FAKE / PLACEHOLDER / NOT-REAL / `[REDACTED` 前缀值跳过); (3) 日志留痕: 命中值以 sha256 前 8 位入日志、不留明文 (「若现行为已如此则只加断言」) | issue 评论 (`scratchpad/issues/aria-plugin-154.md:43-63`) |
| C9 | 基线 RED fixture 已有现成口径: `secret-scan.sh` 对「`JWT_SECRET` 等号两侧带空格 + base64」与「JSON 键 `token` + 40 位 hex」零输出, 阳性对照 (JSON 键 `client_secret` / 无空格 `JWT_SECRET=`) 被检出; **值一律运行时生成, 不落盘真值** | handoff `:50`; 决策单 `:28` (我已独立复现, 见 §6.4) |
| C10 | SC-8 性能闸: 每次调用绝对耗时 <= `max(100ms, 改前基线 x 1.5)`; `SC8_ABS_CEILING_MS=100` 硬编码、刻意不读环境变量; FAIL 时记全数据进 handoff 请 owner 复议, 不得自行降阈值 / 换口径 / 删档 | `.aria/decisions/2026-08-24-sc8-absolute-latency-gate.md:24-47`; `secret-guard.test.sh:1877` |
| C11 | 计数口径必须可复算 (family / 用例数等), 争议由 census 实测定案; printf 族 SC-19 探针豁免是 owner 2026-08-16 的逐次裁定 | count-disputes note `:5-14,:27-38` |
| C12 | AI 自作主张的流程判断必须写进 handoff (跳了什么 + 理由 + 请复议), 无论是否落在白名单内 | `standards/conventions/configured-gate-authority.md:107-117` |
| C13 | fixture 假值与真值零关联 (连前缀都不借); 新机制立案前 `ls hooks/` + grep (「不存在」也是未测量的摘要) | 08-22 handoff `:50-51` |

## 3 规范

### 3.1 `standards/conventions/secret-hygiene.md` (Rule #7 SOT, Version 1.1.2)

- **「凭据不要放命令行参数」没有成文条款** 【读码 + grep】。全文无 `argv` / 命令行参数 / 进程表 / `ps` 字样; 最近的三处: `:111-112` (§2.4 `docker login` 无 `--password-stdin` 时 / `helm registry login` 无 stdin pipe 时列为受限命令), `:214-219` (§3.6 `--password-stdin` 正例), 以及另一份 `nomad-docker-registry-auth.md:259` 的一句「cred 不进 process args」。
- 自然落点: §2.5 「Inspection 命令含 secret 字段」(`:114-120`, 现列 `nomad job inspect` / `kubectl describe pod` / `kubectl exec ... env` / `aether status --json`) 加 `ps` 家族一行; §3 加「凭据走 env / `--config` / stdin」正例 (curl 本机 7.88.1 帮助含 `-K, --config <file>` 与 `-H, --header <header/@file>`; `--config -` 读 stdin 我**未**实跑, 【推测】须执笔实测)。
- 必须是 code + test + doc 三位一体 (memory `paper-fix-antipattern`): 只改 SOT 散文是 paper fix。`2026-08-02` 教训: SOT 里的「安全写法」示例须逐工具实跑 (当时 4 处 `-out=keys` 推荐位全是非法 flag)。
- 版本: 加新条款属 additive, 先例 1.0.0 -> 1.1.0 (`:404` 「Additive (Layer 2 ship)」); 计数同步 / 事实订正走 PATCH (1.1.1 / 1.1.2)。`:397-404` 版本历史表须追加一行。
- 与 WP-A 相关的其余条款: `:97` (§2.2 claude 配置文件, #179 补入); `:295` (§5.2 secret-scan `exit 0` always, detect-only); `:285` (表里写 secret-guard 是「Bash + Read/Edit/Write/MultiEdit blocker」, 但 `secret-guard.sh:698-700` 对 Write / MultiEdit 是 `exit 0` pass-through —— 表述偏强, 改该表时顺手核); 三处 599 / 593 计数在 `:23` / `:287` / `:319`, secret-scan 的 49 在 `:288`。

### 3.2 `standards/conventions/skill-benchmark-exemption.md` (Rule #6 SOT, Version 1.1.0)

- **全文无「hook」一词** 【grep 0 命中】; `aria-plugin-benchmarks/ab-suite/` 对 `secret-guard` / `secret-scan` / `BLOCKED` / `guard:ack` / `hook` **0 命中** (`AB_TEST_OPERATIONS.md:486-495` 的「Hook 型 Skill」指 tdd-enforcer 这类 Skill, 不是 plugin hook)。所以 hook 的归类完全靠 owner 2026-08-02 框定 + 先例, 不是 SOT 成文。
- §1 (`:12-22`): 「不要按目录判」; `:22` 「逐 hunk 判, 不逐文件判; 只要有任一 hunk 落在『处方性且在测量范围内』, 整个变更就照跑」。
- §2 决策表原文 (`:26-31`):
  1. `:28` **描述性** (schema / 字段 / 命令语法 / 溯源注释 / 行号勘正) | 不适用 | deterministic substitute: SC 级 baseline-failing 结构化测试 (必须在场)
  2. `:29` **处方性**, 且属运行时指令面 (SKILL.md 正文 / `references/rules/*` dispatch / 判定规则) | 能 | 照跑 AB, 零裁量
  3. `:30` **处方性**, 但治的行为在固定测试集覆盖范围之外 (典型: authoring 向导) | 不能 | 见 §3 —— 不是简单豁免, 是「AB 测不到 => 换定向 fixture + 记套件缺口」
  4. `:31` 拿不准 | 照跑 (宁跑勿豁)
- §3 (`:35-47`) 第三行须**同时**满足三条, 缺一回落照跑: (1) 点名行为 + 说明为什么现有固定测试集结构上测不到; (2) 新建定向 fixture, 可证伪性须实证 (回退改动, 该 fixture 必须转红); (3) 把「固定测试集缺该维度」开成 issue。
- §4 (`:49-57`): 无论走哪一行都要留 `rule6_note` 引用本规范; 落「拿不准」格默认照跑。
- §4.1 (`:59-72`) rule6_note 字段 (逐字):

```yaml
rule6_note:
  decision_table_row: 1 | 2 | 3 | 4 | n/a   # SOT §2 决策表第几行 (4 = 拿不准照跑); n/a = 本 spec 不属 Skill 变更
  description_changed: yes | no
  scenario1: <结果目录> | not_required | n/a
  scenario4b: <结果目录> pass | <结果目录> fail | <结果目录> void | not_required | n/a
  negctrl: <被评命中>/10 vs <负控命中>/10 | n/a
```

- **hook 改动历来归类**: 6 份全走 substitute (见 §1.2; 另 v1.66.2 #145 的 CHANGELOG 也是「AB 不适用; substitute = 两组 baseline-failing 结构化测试」, `aria/CHANGELOG.md:441-452`)。`CHANGELOG [1.66.3]` / `[1.66.4]` 条目末行都带一行 `rule6_note:` 散文 (`:415-440`), 是 CHANGELOG 侧的写法样例。
- **hook 拒绝/告警文案是否算「处方性 · 运行时指令面」【判断】**: SOT 枚举的「运行时指令面」示例只有 SKILL.md 正文 / `references/rules/*`; 但 SOT §1 对「处方性」的定义是「AI 读了照做」(`:20`), secret-guard 的 BLOCKED stderr 与 secret-scan 的 `additionalContext` 正是 harness 回喂给 AI、AI 会照做的文字 (我在本 session 就被 BLOCKED 文案回喂过一次, 也被 secret-scan 的 `additionalContext` 注入过两次)。所以**新增/改写其中的处方句 (如「凭据不要放命令行参数, 改用 env / --config / stdin」「疑似, 若为 fixture 请说明」)属处方性**; 又因 ab-suite 零覆盖, 落**第 3 行**, 须满足 §3 三条 (点名行为 / 可证伪定向 fixture / 开套件缺口 issue); 三条不齐 => 第 4 行「照跑」, 而无套件可跑 => 测量剧场 (`:45`), 所以实际只能把三条做齐或改为不改文案。纯数据回显 (#145 类 redaction)、头注释、计数、测试代码属描述性 => 第 1 行 substitute。
- 五字段模板对「同一 Spec 内 hook 代码 hunk + 文案 hunk」只有单值槽位; 【推测】需要两块 rule6_note (代码 hunk: `n/a` + 2026-08-02 框定; 文案 hunk: `3` + 三条), 模板未定义多块写法 —— 列入 open_questions。
- §6 已知局限 (`:86-94`) 第三条: 五字段无机械 enforcement; 场景 4b 只在 Claude 模型上实测。

### 3.3 `standards/conventions/configured-gate-authority.md` (Rule #10)

- `.aria/config.json` `audit` 段 【实读】: `enabled: true`, `mode: convergence`, `max_rounds: 5`; `checkpoints`: `post_spec` = convergence, `post_planning` = convergence; `post_brainstorm` / `mid_implementation` / `post_implementation` / `pre_merge` / `post_closure` = off; 五席团队 tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager。
- 含义: WP-A 必须跑 post_spec (Spec 成稿后) 与 post_planning (A.2/A.3 产出后), 「Spec 小 / 只是 hook 补丁 / 任务是已审 SC 的 1:1 派生」都不是跳过理由 (`:15-21`); 白名单封闭四类 (`:31-38`), 其中「A.2 没做所以没东西审」合法、「A.2 做了但很简单」不合法 (`:40`)。其余五个 checkpoint 是**配置显式 off**, 跳过合法, 但 AI 也不得代 owner 打开它们。
- `:107-117` 配套习惯: 任何自作主张的流程判断写进 handoff。

### 3.4 `standards/openspec/templates/proposal-minimal.md`

- 63 行, **CRLF** (`git ls-files --eol`: `i/crlf w/crlf`)。所有 WP-A 要编辑的目标文件 (hooks / tests / 六个发版文件 / `secret-hygiene.md` / CLAUDE.md / 主仓 VERSION / 架构文档) 与 `openspec/` 下 2026-04 起的全部 Spec 都是 **LF**; 仅此模板、`aria/skills/spec-drafter/SKILL.md`、`LEVEL_GUIDE.md` 与 2026-03 及更早的 82 个旧 openspec 文件是 CRLF。用脚本从模板拷贝会把 CRLF 带进 LF 仓 (memory `preserve-crlf`)。stub 已是 LF, 保持。
- 节结构: `# {Feature Name}` / 头 blockquote 四字段 (`Level: Minimal (Level 2 Spec)` / `Status` / `Created` / `Linked Issue`) / `## Why` / `## What` + `### Key Deliverables` / `## Impact` (表 Type | Description, 行 Positive / Risk) / `## Tasks` (checkbox) / `## Success Criteria` (checkbox) / `---` 后 `Template Usage Notes` (不进成品)。Linked Issue 行: 反引号内 `<org>/<repo>#<n>`, 多个用 `, ` 分隔; 无则逐字写 `none`。
- 陷阱: `standards/openspec/templates/README.md:48-52` 的「使用方法」教的是 `standards/openspec/changes/{feature-name}`, 与 CLAUDE.md Rule #5 (`:100`) 相反 —— 忽略该路径, 用主仓 `openspec/changes/`。
- 【实跑】stub 过 `linked-issue-field-availability` 探针 (`OK (1 份在范围内, 0 条在册)`) 与 `check_bare_issue_refs.py` (`裸 issue 引用: 0`)。

### 3.5 `standards/conventions/content-integrity.md` §4.4 / §4.5

- §4.4 (`:161-187`): 规则 1 引用 issue / PR 一律全限定 `<org>/<repo>#<n>` (例 `10CG/Aria#195` 与 `10CG/aria-plugin#195` 是两件事); 规则 2 `#` 只留给 issue / PR, 文内自己的编号 (条目 / 表格行 / 清单项) 直接写数字, 例外仅 `Rule #N`。执行口径: 新写或本次改动到的文字按此写, 存量不批量回改。自检 `aria/skills/state-scanner/scripts/check_bare_issue_refs.py <文件>`; 它**不是已启用闸门**, Spec **不得**把「整份文件 rc 0」写成验收门槛 (`:185-186`)。
- §4.5 (`:189-210`): 文内编号只用 1 2 3 / A B C / (1) (2) / `1.`; 不用带圈数字等 (U+2460-24FF / U+2776-2793 / U+3251-325F / U+32B1-32BF), 不用希腊字母做编号; 自查一行 python 命令在 `:208`。(旧 Spec 里的 `SC-22` 等处有带圈数字, 属存量, 不要照抄。)
- 本案提示: 旧先例 Spec 大量写裸 `#170` / `#128` / `#154` (指不同仓的不同 issue), 引用时必须补全限定名, 例如 `10CG/Aria#170`、`10CG/aria-plugin#128`; 注意 `10CG/aria-plugin#154` 与归档 Spec `2026-07-11-secret-guard-bash3-multiline-hardening` 里的裸 `#154` (那是 `10CG/Aria#154`, readarray / bash3) 是两件事。

## 4 本仓 Level 2 proposal 的实际骨架与写法惯例

参照: `2026-08-22-secret-guard-manifest-precision/proposal.md` (hook, 最近邻), `2026-08-02-...-nomad-var-put-echo/proposal.md`, `2026-09-17-rule6-description-change-trigger-eval-lane/proposal.md` (五字段样例 + Open Questions 体例)。

**节结构 (顺序)**

1. (归档后才有) YAML frontmatter `unverified_claims` / `unverified_ack` / `unverified_ack_reason`。
2. `# 标题` -> 头 blockquote: `Level` / `Status` (生命周期 + 审计轨迹一行: R1 `xC+yM+zm` -> ... 收敛或 overridden) / 可选 `converged` yaml 块 (`converged` / `rounds` / `overridden_by_user` / `pending_owner`) / `Created` / `Linked Issue` / `Issue` 细节 (triage verdict) / `认领` (track, 容器, phase1_gate) / **`基线冻结`** (「aria @ `<sha>` -- 行号/计数均对此 SHA」) / `代码落点` (Spec 落主仓, Rule #5)。
3. `---` -> `## Why` (**先放实测基线表**: 形态 x 现状 x 证据, 四处来源可复现) -> `## What Changes` (编号条目 1, 1b, 2 ...; 每条写机制 + 「实现路径语义」「陷阱点名」「范围边界 (已知限)」) -> `## Out of scope` / `## 转出` (ship 时逐条开 issue, 复现命令内联) -> `## 关键决策` 表 (决策 | 选择 | 理由) -> `## Success Criteria` -> `## rule6_note` -> `## Impact` (**行为变更两向申报**: 新拦截 / 新放行) -> `## Tasks` (A.2 骨架, 粗粒度内联; 细粒度在 `detailed-tasks.yaml` 路径 B) -> `## Open Questions` / 待 owner 复议 (每项给推荐 + 代价; 裁定逐条记在各项末尾) -> `## Amendments (append-only, Phase B 实现期)`。
4. `Status` 收口: archive 前置条件是 `tasks.md` 全 `[x]` 或 `Status == done` (`standards/openspec/project.md:122-136`), Level 2 没有 tasks.md, 所以 Status 要写成 `Done` / `Complete` 并带 ship 证据 (先例 `2026-08-02` 头 `:4`)。
5. Level 2 + post_planning enabled 的实际产物: proposal 内联粗粒度 Tasks + task-planner 产 `detailed-tasks.yaml` (`metadata.spec_level: 2`, `datasource: "proposal.md"`, `exec_order`, `carries_sc`, `sc_coverage_crosscheck`; `2026-08-22-.../detailed-tasks.yaml:1-33`)。

**SC 写法惯例 (可证伪)**

- 每条 SC 过反事实「不实现会红吗」, 并写明基线: 「`<命令>` -> exit 2 (基线 0, baseline-failing)」(`2026-08-22 :70,:72`)。
- 五类 SC 分工: (1) 核心 baseline-failing; (2) 既有 credit 仍生效 (改前改后均放行); (3) **误杀守卫** (`2026-08-22` SC-5: 「前置白名单写错方向本条必红」, 先写守卫再动 pattern, `:55`); (4) 全量回归, 且写明**只承担「无外溢」, 不得当作功能正确的证据** (`2026-08-02 :159`); (5) 文档同步 (换人执笔 + 计数与头注释)。
- 已知不覆盖用 `KNOWN-LIMIT` 命名锁现状 (`2026-08-02 :164`); 表述「部分覆盖」。
- 每条 SC 写「它怎么会红」: 删 / 弱化某半句 -> 转红 (`2026-09-17 :146-159` 逐条列反事实; v11 自检实测)。
- 数字一律脚本统计、写明「权威值 = 实跑输出」; 三点机械比对 (测试头注释 / SOT / Spec 正文) 是 SC-13 体例。
- 判据用 python `re` 而非 `grep` (Claude Code shell 的 `grep` 是 ugrep, 带有界重复的多字节正则报 `exceeds complexity limits`, `2026-09-17 :150` 已记; 我在本 session 亲遇一次)。
- **基线三态实跑**: 基线 / 好实现 / 坏实现 (memory `check-runs-at-baseline-first`); 坏态须像真实坏情形且由非作者独立构造 (`#179` C-1 是唯一抓手)。
- hook 双腿 dogfood: SC-9a canonical 直调 (pre-merge 主闸) + SC-9b ship 后经 harness hook 链复验, 前置 `cmp` **指名版本目录** (`2026-08-18 :761`; 本机缓存现有 `1.73.3` / `1.74.0` / `1.74.1` 并存, 【实测】`1.74.1/hooks/secret-guard.sh` 与 canonical 字节相同)。SC-9b 需 owner 更新插件缓存并重启 session, 属 session 级前置, 应写成 post-ship 腿并声明执行条件。`10CG/Aria#178` (open) 提议把「SC 须显式声明测的是哪份副本」成文, 尚非 SOT, 但本案宜照做。
- 头部要带「基线冻结 SHA」, 行号 / 计数对该 SHA; 版本号不写死 (`<vNEXT>`, ship 时现取 + 两端 `ls-remote --tags` + 与 `10CG/Aria#199` 协商)。

## 5 文档同步面 (改名单 / 模式 / 文案时要联动的面)

### 5.1 机械耦合 (改了不同步会红)

| 面 | 位置 | 说明 |
|---|---|---|
| 测试头计数 | `aria/hooks/tests/secret-guard.test.sh:11` | `Coverage: 599 cases (593 without zsh)`; 由 SC-13 (`:2018-2033`) 断言 == 实跑总数 (接受双值之一) |
| SC-19 census | `secret-guard.test.sh:1602-1622` | `family_count` 硬编码 `61` (`:1620` / `:1622`), `:1617` 要求每个 family 在测试里有 `# family='<name>'` 探针注释; `corpus_census.py` 实测基线 61 (我跑过); 新增 risky_patterns 行若引入新 family, 必须补跨段探针 + 改该数 (`#153` 57->60、`#179` 60->61 的先例, `:1602-1605`) |
| SC-8 性能闸 | `:1877` | tier (e) 最坏档, 我在低负载 (load 4-9) 下测得 39.5 ms/call, 上限 100 ms; 余量约 60 ms |
| secret-scan 用例数 | `secret-hygiene.md:288` = 49 | `secret-scan.test.sh` **没有** SC-13 等价断言 (【读码】头部无计数), 49 -> N 只能手工同步或新增断言 |
| secret-hygiene 计数 | `secret-hygiene.md:23,287,319` | 599 / 593 三处 (SC-13 失败文案也点名「secret-hygiene.md 三处」) |
| jq CRLF 静态守卫 | `aria/hooks/tests/jq-crlf-guard.sh` | 新增 jq 消费点须 `tr -d '\r'` / `${VAR%$'\r'}` / `# crlf-ok` 注释 (`secret-scan.sh:126,130,135` 是体例) |

### 5.2 描述性文档 (行为 / 清单 / 计数描述)

| 文件:行 | 现状 | WP-A 触及时 |
|---|---|---|
| `aria/hooks/secret-guard.sh:4-63` 头部 THREAT MODEL | **`:19-23` 仍写「Phase 2 would add PostToolUse hook that regex-scans output ... + redacts — out of scope」**: secret-scan 自 v1.24.0 就存在且 v1.51.0 已声明不能 redact, 这是 07-03 Spec (AC-6 要求 secret-guard.sh 零改动) 遗留的过时表述 | 改 History 时顺手订正, 否则 WP-A 的 L3 补洞与该头注释自相矛盾 |
| `secret-guard.sh:62` | 引 `docs/operations/secret-rotation-runbook.md §1.3`; 【实测】主仓无 `docs/operations/` 目录, 全仓仅此一处引用 => 悬空引用 | 与轮换延后有关, 可留可删, 需裁 |
| `secret-guard.sh:65-113` History | `#179` 条目是体例: 双平面 / credit / 白名单 / 「Coverage gaps」已知限三类 | 追加 WP-A 条目 + 更新已知限 |
| `aria/hooks/secret-scan.sh:2-94` 头部 | `:33-34` 写「49 known bypass classes」「~15 secret-shape patterns」; 【读码】PATTERNS 实有 **31 条** (`:152-231`) + PEM 预处理; `:58-68` 「What this does NOT catch」把「base64 / hex 无 telltale prefix 的 secret」列为**接受的残余风险** | WP-A 正是在移动这条边界: 必须同步改 `:58-68` 与 `:33-34` |
| `aria/README.md:31-33`, `aria/README.zh.md:31-33` | 三行 hook 表; `:33` 描述 secret-scan「detect secret-shaped output + warn」; `:7` 「5 Hooks」; `:155` 注释「does NOT rewrite tool_response」 | 仅当描述变了才改; i18n 只在**正文实质变更**才重译 (CLAUDE.md `:82`) |
| `aria/hooks/hooks.json:2` | description 串 | 仅新增 hook 脚本时改 |
| `aria/.claude-plugin/plugin.json:3`, `marketplace.json:4,15` | 「含默认 secret-guard」 | 除版本号外一般不动 |
| `aria/.github/secret_scanning.yml:21-22` | GitHub push-protection `paths-ignore` **只列两个测试文件** | 新增含逼真形状 fixture 的新测试文件要加进去 (见 §6.8) |
| `standards/conventions/secret-hygiene.md` | `:3` 版本, `:23,:97,:111-120,:214-219,:285-288,:295,:319,:397-404` | 见 §3.1 |
| `standards/conventions/shell-jq-crlf-hygiene.md:14,95` | 提到 secret-scan 同款 gate | 仅当 secret-scan 的 jq 处理变了 |
| `docs/architecture/system-architecture.md:251,404` | hook 清单只列 secret-guard / handoff-location-guard / host-docker-logout-guard (**不含 secret-scan**) | 仅新增 hook 文件时联动 |
| `.aria/notes/secret-guard-179-pattern-rows.md` | 行号已漂移 (见 §1.3) | 若复用该枚举, 重取行号 |
| `aria/CHANGELOG.md` | 新增 `## [x.y.z]` 节; `[1.66.4]` (`:415-428`) / `[1.66.3]` (`:429-440`) 是 hook 发版体例 (背景 / 修复 / 测试计数 / rule6_note 行) | 必改 |
| 发版同步面 | aria 六文件 (见 §7) + 主仓 gitlink + 16 个版本点 | 必改 |

### 5.3 「不要新增 hook 文件」的隐含代价【推测】

新增一个 hook 脚本要联动 `hooks.json`、README 两份表、`system-architecture.md` 两处、`aria-doctor`、`secret_scanning.yml`、archive 闸门的 alive 判定 (`spec_complete.py:733-744` 只认 `hooks.json` / `.aria/config.json` 为注册面)。在既有两个 hook 里加 pattern 行 / 分支则联动面小得多。

## 6 已知陷阱

### 6.1 按形状匹配会在「讨论 secret 模式」的文本上误触发

- memory `secret-guard-fp` 的仓内出处: `docs/handoff/2026-07-12-state-scanner-false-parity-spec-r4.md:107,147` (哨兵必须运行时拼装); `openspec/archive/2026-07-16-state-scanner-snapshot-stderr-secret-leak/proposal.md:172,201`; `openspec/archive/2026-09-04-sibling-spec-probe/detailed-tasks.yaml:326`; `aria/hooks/secret-guard.sh:1004-1005` (「讨论文本请用 Write 工具或运行时拼装」)。
- **仓内运行时拼装实证**: `aria/skills/state-scanner/tests/test_stderr_typed_channel.py:78` `sentinel = "SENT" + "INEL_TOKEN_" + "abc123"` (字符串拼接, 完整字面量不落源文件)。
- 对照: `aria/hooks/tests/secret-scan.test.sh:101-123` 的 23 条检测 fixture **全是字面量** (只有 `:95-100` 的 PEM 用 `printf` 拼); 该文件与 `secret-guard.test.sh` 靠 `secret_scanning.yml` 白名单过 GitHub。即仓内实践是「旧测试字面量 + 白名单, 新 Spec 要求运行时拼装」两套并存; WP-A 新增 RED fixture 应走运行时生成 (handoff `:50` 已写明)。
- **本 session 活体实证 (三次, 均为假阳性, 无需轮换)**: (a) `cat .claude/settings.json` 被 secret-guard 1.74.1 拦 (合法: 该文件在 #179 清单里), BLOCKED 回显把整条命令原样打回; (b) 把 `secret-scan.test.sh` 的低熵假 fixture 行打到 Bash 输出里, PostToolUse 报 `DETECTED 12`; (c) 我用 Write 写探针脚本, 脚本里一行 L2 wrapper 占位串 (JSON 键 `client_secret` 配 `[REDACTED-BY-WRAPPER len=40]`) 触发 `DETECTED 1` —— 这同时**证明现有 `json-secret-field` 对 wrapper 输出已在误报** (见 §6.4)。
- 所以写 WP-A Spec / 测试时: 含 `\.env`、`os.environ`、`/v1/var/`、`registration-token`、`map_values(length)` 等字面量的文字, 用 **Write 工具**落盘 (PreToolUse 对 Write / MultiEdit 直接 `exit 0`, 只对 Read / Edit 按路径判, `secret-guard.sh:631-700`), 不要走 bash heredoc (heredoc 内容属 `$command`, 整串被 risky_patterns 扫)。
- `# guard:ack:` 理由首 token 须 >= 8 连续非空白字符 (`secret-guard.sh:719` 正则 `[^[:space:]][^[:space:]]{7,}`; `reading` 7 字符恒失效, 用 `inspecting`; `10CG/aria-plugin#130` 仍 open)。

### 6.2 RED fixture 必须在基线上红

`2026-07-16` Spec `:200`: v1 写的「凭据 sentinel 红测试」打错靶 —— 那三处是纯本地命令, argv 里没有 remote URL, 用「凭据 URL 的失败 fetch」做 fixture **在未修改代码上就 PASS**, 违反自我否证闸。WP-A 每条 RED 都要先在 `268da8f` 上实跑确认红。

### 6.3 PostToolUse 无法 redact 的仓内出处 (aria-plugin#91 -> v1.51.0)

`aria/hooks/secret-scan.sh:15-23` (架构限制说明, 引 hooks-guide line 891), `:89`, `:341-344`, `:363-367`; `secret-guard.sh:1002-1003`; `secret-scan.test.sh:7`; `secret-guard.test.sh:1179`; `aria/README.md:33,155` / `README.zh.md:33,155`; `standards/conventions/secret-hygiene.md:295`; `DEC-20260703-001:10-13`; `2026-07-03` Spec `:16-20`; `aria/CHANGELOG.md:1159` (`[1.51.0] - 2026-07-03`) 与 `:433` (`[1.66.3]` 背景)。不要在任何新文字里写「L3 会 redact / 兜底」。

### 6.4 基线实测 (v1.74.1 真 clone, 我亲跑; 值运行时生成, 只看元数据)

**secret-scan.sh** (`probe_scan_shapes.py`; `warned` = 是否发出检测告警):

| 形态 | 结果 |
|---|---|
| `JWT_SECRET` / `SECRET_KEY` / `INTERNAL_TOKEN` / `LFS_JWT_SECRET` 加**空格**等号 + 44 位 base64 | 全部 **未告警** |
| `PASSWD` 加空格等号 + 16 位字母数字 | 未告警 |
| 无空格 `JWT_SECRET=<base64>` (对照) | 告警 |
| JSON 键 `token` + 40 位 hex (紧凑 / 带空格两种) | **未告警** |
| JSON 键 `sha1` + 40 位 hex | **未告警** |
| JSON 键 `client_secret` / `password` / `api_key` + 40 位 hex (对照) | 告警 |
| yaml `token: <hex>` / `Authorization: token <hex>` (Forgejo 风格) / 裸 64 位 hex 行 | 未告警 |
| JSON 键 `client_secret` + `FAKE` 开头假值 | **告警 (无 FAKE 白名单)** |
| JSON 键 `client_secret` + `[REDACTED-BY-WRAPPER len=40]` 占位 | **告警 (FP: 无 `[REDACTED` 白名单)** |
| 干净输出 | 不告警 |

即决策单 `:28` 的两形态零输出属实, 且范围比 #154 原稿更宽 (INI 空格形 / `sha1` / yaml / Authorization 头); 另外**FP 白名单不是 nice-to-have 而是既有缺陷**: 已安装的 L2 wrapper (`/home/dev/.npm-global/bin/forgejo:138-141,170-184`) 对 JSON 键 `token` / `sha1` / `client_secret` / `secret` 的值输出 `[REDACTED-BY-WRAPPER len=N]` (sed 降级路径为不带 len 的同前缀串), 对 L3 现有键集里的 `client_secret` / `secret` 已经会误报; 给 L3 加 `token` / `sha1` 后, 每次走 wrapper 的凭据类调用都会误报, 不加 `[REDACTED` 前缀白名单就是恒红。
- 现行日志 (`secret-scan.sh:357-361`) 只写 `时间 用户 PWD SCAN-DETECT tool matches breakdown size`, **既无值也无值的 hash** —— #154 评论的「若现行为已如此」只对「无明文」成立, 「sha256 前 8 位」**未实现**。仓内 fingerprint 口径: `.aria/pat-inventory.yaml:21` `fingerprint_algo: sha256-hex-prefix-8`; `.aria/probes/forgejo-app-token-liveness.py:87`; hook 内先例 `secret-guard.sh:624` (`sha256sum | head -c 16`, 仅写入失败路径、`${hash:-unknown}` fail-soft, 且 TSV 行内 CR/LF/TAB 折叠 `:614-615`)。`sha256sum` 在 macOS 默认不存在, 注意可移植。

**secret-guard.sh** (`probe_guard_baseline.py` / `probe_env_boundary_class.py` / `probe_jq_forms.py` / `probe_jq_shape.py`; 命令文本不执行):

| 探针 | 退出码 |
|---|---|
| 对照 `cat .env`、`cat ~/.bashrc` | 2 (拦) |
| `sed -n 120,140p /etc/forgejo/app.ini`、`cat /etc/forgejo/app.ini` | 0 (放) |
| `f=/etc/forgejo/app.ini; cat $f`、`f=~/.bashrc; cat $f` | 0 (放) |
| `ps aux`、`ps -eo pid,args`、`ps auxww \| grep curl`、`pgrep -af curl` | 0 (放) |
| `cat /proc/1234/cmdline` | 2 (拦; 先例行 `secret-guard.sh:932-933` 已把 `/proc/<pid>/cmdline` 当含密源) |
| `python -c` 内含 `os.environ` | 2 (FP1); 换 `os.getenv` 则 0 |
| `curl .../v1/var/... \| jq '.Items \| map_values(length)'` | 2 (FP2); `\| jq '.Items \| keys'` 为 0 |

- **`\.env` 右边界缺失是「类」问题, 不止 `10CG/Aria#221` 点名的一行**: 用 `conf.environ.sample` 这个名字对 20 种 reader 形态实测 **16/20 被拦** (head / tail / less / more / strings / hexdump / od / xxd / awk / perl / tac / nl / sort / diff / python -c / node -e); 只有 cat / sed / grep / base64 放行 (cat 行 `:782` 自带 `(\b|/|$|[[:space:]])` 右边界)。根因行 `:893` (`python3? -c`) 与 `:894` (`node -e`) 的源组 `\.env` 无右边界。修类不修例 (memory `fix-the-class`)。
- **jq 白名单基线** (`| curl ... /v1/var/ | jq '<f>'`): 放行 `.Items | keys` / `keys` / `length` / `.Items | length` / `.Items | keys | length`; 拦 `keys_unsorted` / `map_values(length)` / `to_entries | map(.key)` / `map(.name)` / `map(.key)` / `map_values(type)` / `with_entries(...)` / `.Items` / `.`。**另实测: `jq '{a: .Items}'` 与 `jq '{a: .Items.password}'` 被形状 credit 放行** (含值的投影), 所以「只出长度」形态被拦而「整块取值」形态被放 —— 正是 #221 评论说的激励反向; 同时说明不能把任何白名单当作「按构造安全」。#221 评论建议的 `length` / `... | length` **已经放行**, 真正缺的是 `keys_unsorted` / `map_values(length)` / `map(.name)` / `map(.key)` 这几条。

### 6.5 跑测试的陷阱【实测】

- 真 checkout (clone @268da8f, 无 zsh): secret-guard **593/593 PASS**; secret-scan **49/49 PASS**。全量 secret-guard 约数分钟 (SC-8 五档: a-d 档改后比改前快 52-78%, e 档 27.6 -> 39.5 ms)。
- `cp -a /home/dev/Aria/aria <目录>` 得到的副本**没有可用 `.git`** (子模块的 `.git` 是 gitlink 文件): `git show af87cae:...` 取不到 => SC-9a 对拍 / SC-8 / zsh 用例被 SKIP, 总数变 582, 且 **SC-13 头注释计数同步断言假红** (`Coverage: 599 != 582`)。要忠实复现基线必须在带 `.git` 的真 checkout / clone 里跑, 并把 `HOME` 指到实验目录 (hook 会写 `~/.claude/logs/`)。
- 探针 (喂 hook JSON) 的体例见 `.aria/audit-reports/phase-b-review-179-...md:85-118`: `jq -n ... | bash hooks/secret-guard.sh`, 基线列 + 改后列, 命令文本不执行。

### 6.6 hook 代码的硬性可移植 / 结构约束

- 必须 bash 3.2 (macOS `/bin/bash`) 兼容, 且 zsh 下经顶部 re-exec 守卫 (`secret-guard.sh:120-130`, `10CG/Aria#154` (readarray / bash3) 的根因修复): 禁 `readarray` / `mapfile` 做字段提取, 禁 bash 4 专有 (`declare -A` / `${x,,}`); 我 grep 过两个 hook 的可执行代码无此类结构。源码里不得有裸 NUL (字段分隔用字面 `\u0000`, `:564`)。
- `secret-guard.sh` fail-CLOSED (`:1111-1120` 内部错误一律 `exit 2`, 逐段判定整段跑在子 shell 里以把 `set -u` 死亡转成非零); `secret-scan.sh` 是 `set -uo pipefail` (无 `-e`) 且 jq 缺失 fail-OPEN (`:96,:100-110`)。新增变量在 `set -u` 下必须有缺省 (#132 / `2026-08-02` R2 backend M-1)。
- BLOCKED 回显必须经 `_sg_redact_echo` (`:1023-1027`, #145): 任何新增「回显命令或片段」的文字都要过它。
- `_sg_judge_one` 注释 `:1032-1033`: whole 模式「reproduces canonical stderr byte-for-byte, zero new lines」—— 改 heredoc 会打破「canonical stderr 字节不变」的既有不变量 (该不变量由 per-segment Spec 立, 我未逐条核对哪些测试断言了它, 【推测】须 grep)。
- 不新增读取项目文件的逻辑是今日事实: 两个 hook **不读任何 `.aria/*`** (grep 仅 `secret-guard.sh:111` 一处注释命中), 也不解析 `cwd` / `CLAUDE_PROJECT_DIR`; 只有 `submodule-gate-telemetry.sh:60` 用 `CLAUDE_PLUGIN_ROOT`。「项目级扩展入口」是**新输入面** (见 §7.3)。

### 6.7 改 risky_patterns 的固定联动

新增行 -> 数组基数变 (基线 **145 项**, `secret-guard.sh:736-1009`, 【实测】) -> SC-8 性能 -> SC-19 census family 与探针 (每条探针须满足 rule 5: 不含块字符, 否则像 printf 族那样只能靠 owner 逐次豁免) -> 测试头计数 (SC-13) -> `secret-hygiene.md` 三处计数 -> 头注释 History。

### 6.8 GitHub push protection

`aria/.github/secret_scanning.yml:1-22` 的注释: 逼真 fixture (sk_live_ / ghp_ / Slack URL / Postgres URL 形状) 会挡住 push 到 GitHub 镜像, 2026-05-23 发 v1.24.0 时被 5+ 个 unblock-secret URL 挡过; 白名单 `paths-ignore` **只有 `hooks/tests/secret-guard.test.sh` 与 `hooks/tests/secret-scan.test.sh`**, 明写「production hook code / skill code / documentation 不在豁免内」。该 yml 引的 memory `feedback_github_secret_scanning_push_range_blocks_history` 在本容器不存在 (memory 容器本地)。主仓没有 `.github` 目录。【推测】: GitHub 只认其已知 provider 格式, 通用「键名 + hex」形状风险低, 但任何 provider 形状字面量 (含 Spec 文字) 都可能挡 push, 且「push range」会带上历史提交 —— 这是 fixture 必须运行时生成、Spec 只写散文描述的第二条理由。

### 6.9 其它

- 执行惯例: 「子模块合并一律本地做、推后逐个 `ls-remote`」(CLAUDE.md `:88-90`); 子模块 detached HEAD 上推送用 `HEAD:master`; 取号前 `ls-remote --tags` 两端。
- aria 无 hook CI: `aria/.forgejo/workflows/` 只有 `issue-triage-tests.yml` (`paths: skills/issue-triage/**`), 所以 hook 类改动的 C.2.4 是 `not_applicable`, hook 测试证据只能靠本地实跑并落 Spec / ledger。陈旧分支 `origin/feat/69-exfil-coverage-corpus` (tip `3c85f24`, 落后 master 304) 含一个 26 探针的 `hooks/tests/exfil_coverage_corpus.sh` + 未合并的 `hook-tests.yml`; 【实测】其语料只有 `/proc/self/environ` 一条相关, **没有 `ps` 或服务端配置文件探针** —— 对 WP-A 的价值在体例 (covered 门控 / gap 只告知 / 「gap 转拦则打印 PROMOTE」), 不在内容。

## 7 与在飞轨的接缝

### 7.1 `10CG/Aria#199` 的守卫 (核实: 属实)

- 原文: `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml:342` 的 `sc12_liveness.guard_config_hooks`: `git -C <主仓根> grep --recurse-submodules -l -F completeness_gate | grep -E '(^|/)(hooks\.json|\.aria/config\.json)$'; echo "rc=${PIPESTATUS[0]}"`; 判据: 末行 `rc=` 为 0 或 1 且其前**无任何输出**才通过 (有输出 => L2 可能被配置文件带绿, 停下查明)。`:341` `blind_spots` 写明原因: 归档闸门分类器 `spec_complete._is_hooks_or_config_path` (`aria/skills/state-scanner/scripts/lib/spec_complete.py:733-744`) 把 basename 为 `hooks.json`、或 `.aria/` 下 `config.json` 里出现的符号判为 `aria_plugin_integration`; 且「本计划也不改 config」。`tasks.md:119` (第 64 条) 说明守卫正则不放宽; N10 用例在 `detailed-tasks.yaml:1166-1198,1545-1549`。
- 【实测】我按原命令在主仓根 (`--recurse-submodules`) 跑: `rc=0`, 全仓 43 个文件含该字面量, **其中无一是 `hooks.json` / `.aria/config.json`** (守卫当前通过); 仓内被跟踪的 `config.json` / `hooks.json` 只有 `.aria/config.json`、`aria-orchestrator/.aria/config.json`、`aria/hooks/hooks.json`、`aria-plugin-benchmarks/runner/config.json` (`detailed-tasks.yaml:341`)。
- 结论: WP-A 只要不把 `completeness_gate` 字面量写进这两类文件就**不撞**; 新增 / 修改 `aria/hooks/hooks.json` 的条目或 `.aria/config.json` 的键本身不触发该守卫。`.aria/config.template.json` 不在守卫正则内。建议 WP-A 每次动这几个文件后复跑该命令。

### 7.2 发版文件两轨都要改 (核实: 属实) 与取号

- aria 发版文件六个: `.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md` / `README.zh.md`; 9 个取值点: plugin.json 1、marketplace.json 2 (顶层 + `plugins` 里 `aria` 项)、VERSION 3 (头部版本行 / 当前发布行说明里的号 / 「## 版本号」代码块)、CHANGELOG 首个版本节标题 1、README 各 1 (`openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md:36,120,127`; owner 裁定 `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md:32-36`, 先例 `10CG/Aria#195` v1.74.0「六个文件一次提交」)。**CLAUDE.md `:81` 仍写「aria 子模块 5 文件」** (该裁定文件 `:36` 明写通用口径未裁); 主仓 16 个版本点 (含 `VERSION:24`, `CLAUDE.md:138,142`, 两份架构文档 `system-architecture.md` §2.8 / `version-scheme.md`, 四份 README badge / i18n 标记) 见 `10CG/Aria#195` 归档 `detailed-tasks.yaml` TASK-030 deliverables。
- `10CG/Aria#199` 计划不写字面版本号, 用 `<vNEXT>` (`tasks.md:8`), ship 时现取 MINOR (`tasks.md:209` 5.3, `:213` 5.7)。串行与取号: 决策单 `:59` (AI 建议、owner 未单独裁, 待复议); 09-30 handoff `:90` 与 `:137` (「取号前 `ls-remote --tags` 两端并与 `10CG/Aria#199` 协商, 号的裁定归 owner」)。
- 先例可比: 新增检测覆盖 v1.47.0 为 MINOR; 同型 hook 清单 / 模式扩展 v1.65.4 / v1.66.3 / v1.66.4 均为 PATCH。级别归 owner 定。
- 协调板 (本地 `refs/aria/coordination` @ `bf05ee9`, 读类操作, 【推测】可能落后远端): 两条 active claim: `bfe8285d/s-73b9@1606` (`pre-merge-completeness-gate-change-scope`, `10CG/Aria#199`, 心跳 2026-09-30T06:57:09Z => SWEEP_TTL 24h 后 2026-10-01T06:57Z 起可被扫为 abandoned, 只能由 bfe8285d 刷新); **我方 `023236f2/s-3e77@1757`** (`track_id: secret-net-l3-and-bypass-paths-023236f2`, `linked_issue: 10CG/aria-plugin#154`, phase A.1, 2026-09-30T17:57:13Z) —— 该 claim 同样受 24h TTL, 长 post_spec 轮次期间须 `phase1_gate.py --heartbeat-only` 刷新; `--linked-issue` 只接受**单个**值, 所以 #203 / `10CG/Aria#221` 对其它容器不可见 (Aria#174 同类盲区), 靠 Spec 头与决策单声明; track_id 带 `-023236f2` 后缀而 change 目录 slug 没有, handoff `track-id` 与后续 claim 须自洽。
- 另: 审计报告文件名 `.aria/audit-reports/<checkpoint>-R<n>-<ts>-<change-id>-<seat>.md` 里的 change-id 应与 change 目录 slug 逐字一致 (`10CG/Aria#199` 的完整性门按 change-id 计席位报告, `proposal.md:217`), 审计期间不要改 slug。

### 7.3 新增项目级配置 / 改 `.aria/config*.json` 会不会撞车

- **现有 custom checks** (`.aria/state-checks.yaml`): `config-template-key-currency` (`:295-315`) 的作用域**仅** `phase_c_integrator.pre_merge_gate` 段 (探针 docstring `.aria/probes/config-template-key-currency.py:4,14-18` 明写 knob-granularity: 其他段无注册表、不做全模板断言); 所以新增顶层键如 `secret_guard` **不会被它判红, 也不会被它保护**。`linked-issue-field-availability` (`:397-420`) 只看 `openspec/changes/**/proposal.md` 的 Linked Issue 字段 (stub 已 OK)。版本类五个 check (`m6-version-badge-match` `:135`、`i18n-readme-translation-currency` `:188`、`plugin-version-arch-docs-match` `:423`、`main-project-version-consistency` `:340`、`plugin-cache-currency` `:317`) 只在发版时相关; `plugin-cache-currency` 在发版后对本机恒 STALE 直到 owner 更新插件, 属预期。`claude-md-changelog-free` (`:237`): CLAUDE.md 现 152 行 / 13,636 字节, 预算 200 / 24,000, 余量充足。
- **config 注册面缺口 (F8)**: `10CG/Aria#199` 的 `proposal.md:59` 已记「`.aria/config.template.json` 无 `audit` 块; `config-loader/DEFAULTS.json` 的 audit 键集缺键」; 现 `DEFAULTS.json` 顶层 12 键 (version / workflow / multi_remote / phase_c_integrator / state_scanner / context_monitor / ai_native_estimator / tdd / phase_b_developer / benchmarks / experiments / audit) **无 secret 段**, `.aria/config.json` 与 `config.template.json` 也没有。新增顶层键 = 要同时登记 `config.template.json` + `DEFAULTS.json` + `config-loader/SKILL.md` / `config-example.md`, 而 `config-loader` 是 **Skill**, 会把 Rule #6 的 hunk 分析从「纯 hook」扩到「含 SKILL.md / DEFAULTS.json」。`10CG/Aria#199` 自己因此选择「不新增 config 键」(`proposal.md:59,67`)。
- **仓内「项目本地路径清单」先例** (纯文本, 不进 config): `.aria/bare-issue-ref-allowlist.txt` (`#` 起首注释, fail-CLOSED, 每行一条) 与 `.aria/linked-issue-field-grandfathered.txt` (`:1-12` 体例: 格式 / 位置 / 语义 / 陈旧守卫三类 / 来源; 明写「仓本地数据, 不进 aria-plugin 分发件」)。【判断】这是「项目级扩展入口」最省接缝的宿主形态 (不碰 config.json / config.template.json / DEFAULTS.json / config-loader); 代价是 hook 今天不解析项目目录 (§6.6), 需要新增 project-dir 解析与「缺文件 / 坏文件 / 路径含 `..`」的 fail 方向设计, 且 hook 跑在采用方项目里 (路径清单归采用方, 不是 Aria 仓)。
- **与 `10CG/Aria#199` 计划的实质接缝只有发版六文件 + 主仓版本点**; 其 N10 守卫对 WP-A 新增的键 / 文件零影响 (前提见 §7.1); `aria-plugin-benchmarks/ab-suite/version.yaml` 只有 #199 会动 (WP-A 不碰 AB 套件)。

### 7.4 其它在飞项

- aria 远端未合并分支只有两条陈旧的 (`feat/69-exfil-coverage-corpus`, `feature/secret-guard-per-segment-evaluation`), 无其它在飞轨触及 `aria/hooks/`; `10CG/Aria#199` 的 `proposal.md` 对 hooks 的提及仅为审计报告文件名实例, 不改 hook。
- 起 WP-B 前要核对 `10CG/Aria#199` 进度 (同改 `phase-c-integrator/SKILL.md`), 不是 WP-A 的接缝。

## 8 给执笔人的速查 (约束摘要)

1. 头部写基线冻结 SHA (aria `268da8f`), 行号 / 计数 / 基线红绿全对该 SHA, 版本号不写死。
2. Linked Issue 行沿用 stub 的三个全限定 issue; 文内引用一律全限定, 不用带圈数字, 不把 `check_bare_issue_refs.py` rc 0 写成门槛。
3. rule6_note: 代码 / 测试 / 文档 hunk = substitute (引 08-02 L128/L130 原文 + 五字段); 文案 hunk 单独判 (第 3 行三条件); 写明归类是 AI 判断, 请 owner 复议 (Rule #10)。
4. SC: baseline-failing + 误杀守卫 + 全量回归 (只承担无外溢) + 文档同步 + 双腿 dogfood (canonical / harness 链, 后者 post-ship 且需 owner 更新缓存) + KNOWN-LIMIT; 每条写反事实。
5. post_spec (R1 起, max 5) 与 post_planning 必跑; 审计期间被审文件零编辑; 不把「改动小」当跳过理由。
6. 凭据轮换不做、不提示、不产清单; 代码侧兜底网照做。
7. 所有测试哨兵运行时生成; Spec 里只写散文, 含敏感字面量的文字用 Write 工具落盘。
