# GRADER_CRITIQUE — eval 9 forgejo-config-detection

评分结果: `with_skill` 6/7 · `old_skill` 7/7 (唯一分歧在断言 7)。

本 eval 是回归臂, 下面按要求答三问, 并额外点名「恒真断言」与「断言测不到的质量差」。

---

## 1. 有没有恒真 / 恒假的断言?

**有, 而且是多数 —— 7 条里 4 条 (1 / 2 / 4 / 5) 对本 fixture 恒真, 第 6 条近似恒真。**

### 1.1 断言 1 / 2 / 4 / 5 = 机械 collector 的转录题, 零区分力

我实读了两臂的 `outputs/state-snapshot.json`, 二者 `forgejo_config` 字段**取值完全相同**:

```json
{"config_status": "missing", "forgejo_remote_detected": true,
 "instance": "forgejo.10cg.pub", "suggestion": "运行 /forgejo-sync 可引导创建配置 (需确认)"}
```

也就是说:

- 断言 1 (检测 Forgejo 远程 / 已知实例) → `forgejo_remote_detected: true` + `instance` 已由 `scan.py` 给出;
- 断言 2 (查 `CLAUDE.local.md` 是否存在) → `config_status: "missing"` 已经把答案写死;
- 断言 4 (输出 `forgejo_config` 与 `config_status`) → 字段名和取值直接抄即可;
- 断言 5 (建议跑 `/forgejo-sync`) → **`suggestion` 字段的字面值就是那句话**, 连措辞都不用自己想。

这四条**任何一臂只要把 snapshot 原样渲染出来就会 pass**, 与 SKILL.md 散文无关 —— 它们量的是
Python collector (`scripts/collectors/forgejo_config.py`), 不是被 AB 对比的技能文本。实测两臂
4/4 全过, 符合预期。**在回归臂里这四条的信息量 ≈ 0 bit。**

### 1.2 断言 6 = 负向断言, 靠「不作为」即可满足, 近似恒真

「不得自动创建 `CLAUDE.local.md`」只有在某一臂**主动写文件**时才会 fail。我独立核验:
`/home/dev/Aria/CLAUDE.local.md` 不存在 (`ls` → No such file), 两臂都没建。而任务本身是「扫描
+ 告诉我怎么设置」, 两臂结尾都停在工作流菜单等确认。这条作为回归护栏合理 (真出事时能抓到),
但在健康常态下恒绿 —— 属于「假绿的反面」类信号, 别把它算进区分力。

### 1.3 真正有区分力的只有 2 条 (3 / 7), 且只有 1 条真的分开了两臂

- 断言 3 (文件存在时查 `forgejo:` 块) 与断言 7 (非 Forgejo 项目跳过检测) **在本 fixture 里根本
  没有被执行到**: 文件不存在, 远程恰恰就是 Forgejo。所以两条只能靠**回答里的机制叙述**来判,
  实质是「这一臂有没有写出机制说明」而不是「行为对不对」。
- 结果: 断言 3 两臂都写了 (pass/pass), 断言 7 只有 `old_skill` 写了明确的「远程不是 Forgejo →
  整个 🔗 区块不显示 (非 Forgejo 项目零噪音)」+ fail-soft 塌缩说明; `with_skill` 全文只有一句
  「若你的 Forgejo 域名不是 `forgejo.10cg.pub`, 检测器认不出来 (会退化成
  `forgejo_remote_detected: false`)」—— 那是把未知主机名当**缺陷提醒**在讲, 没有一句说明
  「无 Forgejo 远程时跳过 / 不输出该区块」, 按尺子判 false。

**没有恒假断言**: 7 条全部可达, `old_skill` 实现了 7/7。

### 1.4 附带的方法论问题

断言 5 要求出现 `/forgejo-sync`, 而这个串是 snapshot `suggestion` 字段的原文;
断言 4 要求的三态词也全在 collector docstring / 模板里。**这类「断言只要求复述机械字段」的写法
无法证伪任何技能文本改动** —— 若要让本 eval 在回归臂上还有信号, 建议把 1/2/4/5 降级为
smoke 前置 (不计分), 把计分重心放在 3 / 7 这种「fixture 未触发、只能靠机制知识回答」的分支,
并补一条**真正的负控 fixture** (在非 Forgejo 仓里跑一次, 看该区块是否真的静默)。

---

## 2. 两臂有没有断言完全没覆盖的重要差异?

**有, 4 处, 其中 (a) 与 (c) 方向相反 —— 两臂各错一处, 断言一处也没测到。**

### (a) 多远程 parity 的诚实度 —— `with_skill` 报了一个与 snapshot 矛盾的汇总 (本轮最大质量差)

- `old_skill`: 「`aria-orchestrator @92acce5` … origin ✅ equal / github ⚠️ **unknown**
  (reason: `no_local_tracking_ref`) ↳ 逐条点名而非只报汇总: 这条不是 "equal", 是 "没有证据"。」
- `with_skill`: 「多远程 parity: **`overall_parity: true`** — `origin` + `github` 两端,
  主仓与 3 个子模块全部 `equal` (fresh)」

我去 snapshot 核了:
`sync_status.multi_remote.submodules[2].remotes[0] = {"name": "github", "parity": "unknown",
"reason": "no_local_tracking_ref", "remote_head": null}`。
**`with_skill` 的「全部 equal」是错的** (`overall_parity: true` 这个字段本身没错, 但把一条
`unknown` 折叠进「全部 equal」属于把「没有证据」谎报成「已核验一致」)。这正是本仓
`partial-push` / `freshness-must-be-fetched` 两条教训针对的失真形状, 却没有任何断言碰它。

### (b) 独立核实 vs 只信 snapshot

`old_skill` 在 snapshot 之外自己跑了三条命令并报出结果: `git remote -v`、`ls CLAUDE.local.md`、
`git check-ignore -v CLAUDE.local.md` (rc=1)。我逐条复跑, **全部属实** (repo 根无
`CLAUDE.local.md`; `git check-ignore` rc=1; `.gitignore` 里只有 `.claude/settings.local.json`,
无 `CLAUDE.local`)。`with_skill` 也提到 gitignore 缺口但没有给核验命令/证据等级。
断言里没有任何一条奖励「证据等级」, 这个差异全额落空。

### (c) 手工配置模板的 schema 保真度 —— 这次方向相反, `old_skill` 给错了字段名

- `with_skill` 的手工模板: `url` / `repo` / `api_token: "${FORGEJO_TOKEN}"` /
  `cloudflare_access.{enabled, client_id_env, client_secret_env}` —— 我对照
  `aria/skills/forgejo-sync/SKILL.md` §生成模板 + §必需配置, **逐字段吻合**。
- `old_skill` 的手工模板: `instance: / owner: / repo:` —— 这三个键**不在真实 schema 里**
  (它自己加了「字段以 `/forgejo-sync` 实际引导的为准」的免责句)。照它写出来的文件会因为含顶层
  `forgejo:` 键而被检测器判成 `configured` (⇒ 提示消失), 但 `forgejo-sync` 读不到 `url` /
  `repo` —— 是一个**会造出假绿的建议**。断言 3/4/5 都只管「有没有讲块检测 / 有没有报三态 /
  有没有建议 forgejo-sync」, 完全测不到「你给用户的那份配置是不是真 schema」。

### (d) 顺序性安全建议

`old_skill` 把「先补 `.gitignore` 再建文件」列为硬顺序 (「顺序反了, 本地配置以及任何不小心
写进去的凭据就有入库风险」); `with_skill` 只把 gitignore 放在「三个坑」的第 2 条, 未给顺序约束。
两臂都遵守了 Rule #7 (只写 `${ENV_VAR}` 不写字面值), 但顺序这一层没有断言覆盖。

### (e) 机制叙述的覆盖面不同 (只被断言 3/7 部分探到)

`old_skill` 给了完整四态表 + fail-soft 契约 + 「只看 `origin`, `github` remote 不参与判定」;
我对照 `scripts/collectors/forgejo_config.py` 源码 (`git remote get-url origin`、
`ARIA_FORGEJO_HOSTS > .aria/config.json > legacy` 优先级、四态、任何异常塌缩成 state 1),
**old_skill 的机制描述与源码逐条相符**。`with_skill` 换了另一组细节 (fenced code block 先剔除、
主机名覆盖优先级、「这一处同时作用于 `forgejo_config` 与 `issue_scan` 两个 collector」),
也属实。两种覆盖面差异只有断言 7 抓到一半。

---

## 3. 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**没有。两臂都未引用该目录下的任何文档** (grep `openspec|proposal\.md|tasks\.md|design\.md`:
两臂命中的只有变更**名字**本身, 而变更名来自 snapshot 的 openspec 活跃变更列表, 例如
`with_skill:17 关联 OpenSpec: a1-entry-claim-duplicate-work-guard (approved)` /
`old_skill:18 OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)`)。

**但要点名一条同形状的旁路污染通道: 两臂都实读并逐段引用了仓内 handoff。**

- `with_skill`: 「已按 H0 强制项读完 `docs/handoff/2026-09-05-2200-...md`」, 并引用
  「上次 handoff (§2 M2) 实测四仓 API 合计 **65**」「按 handoff §3 第 4 条**先 fetch 再
  `--heartbeat-only`**」「见 handoff §3 第 1 条, 必须在启动 claude 进程时设」。
- `old_skill`: 「上一份 handoff (§2 M2) 实测四仓真实合计 **65**」「来源: 最新 handoff §6 的
  首选项 (0.8h 前写的)」「按 handoff §3 第 4 条 "先 fetch 再刷 heartbeat"」, 并进一步点名
  `ARIA_COORDINATION_NO_PUSH` 当前 UNSET。

该 handoff (`docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`)
正是 in-flight a1-entry 轨道自己的会话记录。两臂关于 31/40 进度、Rule #6 AB 的会话级前置、
claim sweep 死线、fetch-then-heartbeat 顺序的叙述**全部来自这个仓内文件, 而非技能文件**。
对本 eval 的 7 条断言 (全是 Forgejo 范围) 它不影响任何一条判定, 但它与
`feedback_ab_baseline_leaks_via_co_landing_docs_and_repo_corpus` 记的是同一条通道 —— 若后续有
eval 想测「claim / 协调闸门」类行为, 这条 handoff 会同时喂饱两臂, 结论必须按「落地前已证 /
ship 态边际未证」拆开表述。

另注: `old_skill` 列出的具体 issue 号 (Aria #195 / #196 / #193, aria-plugin #169,
aria-standards #19) 来自 snapshot 的 issue cache, 不是变更文档;
`with_skill` 引的 `forgejo_config.py::_has_forgejo_block` 来自技能自带 `scripts/` 源码,
也不属于 `openspec/changes/` 语料。
