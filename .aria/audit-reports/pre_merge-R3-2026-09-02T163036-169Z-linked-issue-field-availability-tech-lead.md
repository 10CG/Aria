---
checkpoint: pre_merge
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-02T16:55:12.678Z
context: PR #190 linked-issue-field-availability (main fdfb183 / aria d1caa66 / standards ffed204)
agents: [tech-lead]
---

# Pre-merge R3 — tech-lead 席 (多仓集成 / 发版面 / 流程合规 / 合并安全)

> 镜头: gitlink 与两远端一致性 · 版本同步面 16 点 · 新 check 三态 · R2 两条 major 的清账完整性 · B9-补 诚实性与推送零动作核验 · 合并安全 (merge-tree / C.2.4 / C.2.4.5 / 探针) · 跨 Spec 接缝 · Rule #6/#8/#10。
> **实物面 (gitlink / tag / 两远端 / 版本 16 点 / 闸门 / 测试 / 接缝 / 三条规则) 全部独立复跑通过, 零 finding。**
> **两条 finding 都是同一个形状的第三次复发**: R1 修实例 → R2 声称「类级修完」→ R3 实测**两个被 R2 逐字点名的落点仍未改** (handoff footer `:178` / PR body L32)。R2 聚合表写「footer 全部对正」「PR 标题 + 本 PR 携带段更正」, 至目标核验不成立 (memory `cross-doc-claim-verify-at-target` + `fix-the-class-not-the-instance`)。

## 审计结论

- [major] documentation/`docs/handoff/2026-09-02-linked-issue-field-b2-implemented-awaiting-push-auth.md`: R2 major `a3bfd693` 的清账**仍不完整** —— R2 声称「footer 全部对正」, 但**文件末行**的 `Status` 仍是推送前的前瞻指令, 与同文件 `:14` 的 `Status` 行**直接矛盾** (同一字段名, 一份文件两个相反取值); 另 §5「多维度同步状态」表的 OpenSpec 行仍写 `tasks.md 22/25` 而实测 24/25。两处都是**当前态陈述**而非带时刻的历史记述 (§1 时间线里的 `1457` / `22/25` / `fe32441` 属历史行, 判为可接受) — 证据: `:178` 逐字 `**Status**: Active — 下个 session 第一件事 = owner 推送授权 → C.2 + PR → D` (R2 tech-lead 报告已把它作为该 major 的 6 条证据之一逐字点名于 `:177`, 行号因 R2 增行位移 1) vs `:14` `> **Status**: Active — H1 四处推送完成; PR #190 pre_merge 收敛审计 R1/R2 已清账…`; `:108` `| OpenSpec | yes | …tasks.md 22/25 + yaml 状态回写 |` vs 实测 `grep -c '^- \[x\]' tasks.md` = **24** / `grep -c '^- \[ \]'` = **1** / yaml `Counter({'done': 24, 'in_progress': 1})`; 该 handoff 是 Rule #9 canonical 且随本 PR 合入 master (finding_id = `a3bfd693`) (type=issue)
- [minor] documentation/`PR#190/body`: R2 minor `8c067861` 的清账不完整 —— R2 报告逐字判定「L32 与 title 不是可辩护的编年叙述」, 清账只改了 title / L7 / L9, **L32 (给 owner 的合并后操作指令) 一字未动仍写 1.68.0**; 另 L15 把 `tests/test_linked_issue_field.py` 记为「48 条」、回归记为「1457 全绿」, 实测 53 / 1462 (type 由 R2 的 risk 改判 issue: 残留部分是确定性错误而非前瞻风险, 故 finding_id 与 `8c067861` 不同) — 证据 (`forgejo GET /repos/10CG/Aria/pulls/190`): body L32「合并后 owner 需 `/plugin update aria@10CG-aria-plugin` 刷本机缓存到 **1.68.0**」, 而实跑 `plugin-cache-currency` 输出 `STALE installed=1.67.2 (scope=user) sot=**1.68.1**`; L15「`tests/test_linked_issue_field.py` **48** 条…state-scanner **1457** 全绿」vs 本轮实跑 `Ran 53 tests OK` / `Ran 1462 tests in 94.282s OK` (finding_id = `b66c5239`) (type=issue)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **1** / Minor **1**。

零 finding 面 (逐项独立复跑, 不采信 R1/R2 摘要): 三仓 gitlink == 两远端 == tag peel · 版本 16 点全 1.68.1 且旧值零残留 · 新 check 六态正确且真被 collector 调用 · Spec 三文件口径与 24/25 计数一致 · B9-补 诚实且 R2 后子模块零推送 · 合并 fast-forward 零冲突且 merged-tree 三 gitlink 在双远端均可解析 · C.2.4 green / C.2.4.5 PASS / 探针 OK · 跨 Spec 导出面与占位串零漂 · Rule #6/#8/#10 无自行豁免。

## 投票

**PASS**

理由: 两条 finding 都是**记录快照与实物脱节**, 无一影响合并安全、发布正确性或运行时行为; merged tree 已实测干净, 三条不可协商规则实测合规。**但建议在 R3 清账内改掉** (共 4 行文本: handoff `:178` + `:108`, PR body L32 + L15) —— 理由不是它们危险, 而是这是同一形状连续第三轮存活, 且 `a3bfd693` 若随 PR 合入 master, 会把一份「自己和自己矛盾的 Rule #9 canonical handoff」永久冻结。不投 REVISE 的边界说明: 本仓既有惯例允许 handoff 成为会话时刻快照、由 `latest.md` 记录其过时 (见 latest.md 09-02 段「那份 handoff 的『未推送 / 待 owner』陈述由此过时」); R1/R2 既已选择就地订正这一条路径, 就应把这条路径走完, 但两种做法本身都不构成合并阻塞。

**给主控的一句话**: 本轮 C∪M = 1 (非 ∅), 故 R3 不可声称收敛; 清账后 R4 仍需跑。

## 核验记录

### 1. gitlink / 两远端 / tag (四条 `ls-remote`, 不信 push 回执 — memory `partial-push`)

```
$ git rev-parse HEAD                       → fdfb18359229e1d7564912453363d14a54dad260
$ git rev-parse origin/feature/linked-issue-field-availability → fdfb183…  (本地 == 远端)
$ git ls-tree origin/feature/linked-issue-field-availability aria standards aria-orchestrator
160000 commit d1caa66cb375c2799f55def453ca232c66a18c22	aria
160000 commit 237045ac2cfed9849c201e18434e9f6cb9036ab5	aria-orchestrator
160000 commit ffed2040dff7964cf9d137e85e174173d2c685b9	standards
$ git ls-tree origin/master … → aria d69091d / aria-orchestrator 237045a / standards 334c609
   ⇒ aria-orchestrator gitlink 本 PR **未动** (master 与 feature 同为 237045a)

$ git -C aria ls-remote origin refs/heads/master 'refs/tags/v1.68*'
d1caa66…	refs/heads/master
c6aad0d…	refs/tags/v1.68.0
fe32441…	refs/tags/v1.68.0^{}
5b9de8e…	refs/tags/v1.68.1
d1caa66…	refs/tags/v1.68.1^{}
$ git -C aria ls-remote github …            → 与 origin **逐字节相同** (含两个 tag 对象与两个 peel)
$ git -C standards ls-remote origin refs/heads/master → ffed204…
$ git -C standards ls-remote github refs/heads/master → ffed204…
$ git ls-remote origin refs/heads/master → c423281… ; git ls-remote github refs/heads/master → c423281…
$ git rev-parse master origin/master     → c423281 / c423281   (memory `stale-local-main`: 本地 master 未陈旧)
$ git submodule status → ` d1caa66 aria (v1.68.1)` / `+92acce5 aria-orchestrator (有意停泊)` / ` ffed204 standards`
```

⇒ aria: gitlink == origin == github == `v1.68.1^{}`; `v1.68.0^{}` = `fe32441` 未被移动, 两 tag 两端 present。standards: gitlink == origin == github。CLAUDE.md 硬约束 1/2 满足, 无孤立 gitlink。

**post-merge tree 的 gitlink 可解析性 (我本轮新加的机械核验)** —— 干跑合并后逐个查子模块双远端是否含该 SHA (GitHub `clone --recursive` 断裂的直接判据, Aria #165 类):
```
$ git ls-tree 5af1893c443716398b6fd9aef98c50a612468e74 aria standards aria-orchestrator
   → d1caa66 / 237045a / ffed204   (= merge-tree 产出的树)
$ git -C aria/standards ls-remote 各自 origin+github  → d1caa66 / ffed204 双端 present (上表)
$ cd aria-orchestrator; for r in github origin: git ls-remote | grep -c 237045a → github: 2 / origin: 2
```
⇒ 合并后 master 树的**三个** gitlink 在各自两个远端都可解析, 无 orphaned gitlink。

### 2. 版本同步面 16 点 (自己 grep, 不引 R2 数字)

```
$ grep -n "1\.68\.1" CLAUDE.md VERSION README.md README.{zh,ja,ko}.md \
      docs/architecture/system-architecture.md docs/architecture/version-scheme.md
CLAUDE.md:139 / CLAUDE.md:141 / VERSION:24 / README.md:8 / README.md:242 /
README.zh.md:3,10,244 / README.ja.md:3,10,244 / README.ko.md:3,10,244 /
system-architecture.md:189 (+ :967 修订史 2.0.2 行) / version-scheme.md:23
   ⇒ 14 点 + arch 两行 = 16 点全 1.68.1

$ grep -n "1\.68\.0\|1\.67\.2" CLAUDE.md VERSION README.md README.{zh,ja,ko}.md docs/architecture/version-scheme.md
   → rc=1, **零命中**
$ grep -n "1\.68\.0\|1\.67\.2" docs/architecture/system-architecture.md
   → 仅 :968 = `| 2.0.1 | … §2.8 版本表 (aria-plugin v1.67.2; …)` = **修订史行 (历史记述), 判定可接受**
      (R2 minor `a04601ce` 的处置 = 补 2.0.2 行 + 头部 Version 2.0.2, 实读 `:3` `> **Version**: 2.0.2` ✅)

$ aria 5 文件: plugin.json:4 / marketplace.json:3,16 / VERSION:3 / CHANGELOG.md:13 (`## [1.68.1] - 2026-09-02`) / README.md:5
   → 全 1.68.1 ✅
```

**CLAUDE.md 发布同步面已把两行纳入清单** (R1 `ac44ace3` 的类级修法): 实读「…+ `docs/architecture/system-architecture.md` §2.8 与 `docs/architecture/version-scheme.md` 的 aria-plugin 版本行 (PR #190 审计补入)。机械兜底: … / `plugin-version-arch-docs-match`」✅。

**新 check 六态副本实跑** (逐字提取 `.aria/state-checks.yaml:381-392` 的 command 到 scratchpad 副本树; 仓内零改动, 事后 `git status --porcelain` = ` M aria-orchestrator`):

| 态 | 构造 | 输出 | rc |
|---|---|---|---|
| 基线 | 原样 | `OK plugin=1.68.1 (2 arch doc rows match)` | 0 |
| DRIFT-A | sa.md → v1.67.9 | `DRIFT plugin=1.68.1 vs system-architecture.md=1.67.9` | 1 |
| DRIFT 双漂 (对抗) | 两侧同时改 | `DRIFT … system-architecture.md=1.67.9 version-scheme.md=1.60.0` (**两点都列, 不早退**) | 1 |
| MISSING-A | 删 sa.md 那行 | `MISSING system-architecture.md §2.8 aria-plugin 行` | 1 |
| MISSING-B | 删 vs.md 那行 | `MISSING version-scheme.md aria-plugin 行` | 1 |
| SKIP | 移走 plugin.json | `##SKIP## aria/.claude-plugin/plugin.json 不可读` | 0 |
| 复原后重跑 | 原样 | `OK plugin=1.68.1 (2 arch doc rows match)` | 0 |

⇒ 好实现绿 / 两类坏实现红 / 缺输入 SKIP, **拒绝能力成立** (memory `adversarial-fixture`), 非恒绿也非恒红。

**运行时真被调用** (memory `completion-signals-vs-runtime-invocation` — 「注册了」≠「被跑了」): 用仓自己的 `collectors.custom_checks._parse_state_checks_yaml` 解析 → **14 条**, 新条为第 14 条 `enabled=True`; 再用 `collect_custom_checks(Path('.'))` 走生产路径全跑:
```
m6-version-badge-match            pass  OK badge=1.68.1
i18n-readme-translation-currency  pass  OK (3 i18n READMEs current @ 1.68.1)
main-project-version-consistency  pass  OK 主项目版本 1.7.5 — 9 个引用点全部一致
linked-issue-field-availability   pass  OK (9 份在范围内, 6 条在册)
plugin-version-arch-docs-match    pass  OK plugin=1.68.1 (2 arch doc rows match)
forgejo-app-token-liveness        pass  OK (2 枚应用级 token 活性正常, 指纹与台账一致)
plugin-cache-currency             fail  STALE installed=1.67.2 (scope=user) sot=1.68.1
其余 8 条                          pass
```
14 条中 13 pass / 1 fail; 唯一 fail = `plugin-cache-currency`, 属 owner 交互动作 (`/plugin update`), handoff §3 已列为已知项, **非仓内缺陷**。跑完 `git status --porcelain` 仍只有 ` M aria-orchestrator`。

`.aria/probes/forgejo-app-token-liveness.py` **独立实跑**: `OK (2 枚应用级 token 活性正常, 指纹与台账一致)` / `aria-layer1-forgejo: OK http=200 fp=c957308a` / `aria-layer2-git: OK http=200 fp=3105220d`, rc=0 (R1 时的指纹漂移已因 merge `origin/master 29c1e4f` 自消, 与 PR body L31 预测一致)。

### 3. R2 两条 major 的清账完整性 (本轮重点)

**`ee23ca88` (Spec 三文件) — 成立, 不重报**:
```
$ grep -n "1\.68\.1\|d1caa66\|ffed204\|1462" proposal.md tasks.md detailed-tasks.yaml
proposal.md:3 (C.2 段: v1.68.1 d1caa66 / ffed204 / 53 测试 / 1462) · tasks.md:5 (v1.68.1 d1caa66 / ffed204 / 53/53 / 1462)
tasks.md:80 (5.3 追记 v1.68.1 d1caa66 + tag 双推核验) · tasks.md:81 (5.4 追记 ffed204) · yaml:66 (metadata.status 同口径)
$ grep -c '^- \[x\]' tasks.md → 24 ; grep -c '^- \[ \]' tasks.md → 1 (仅 `5.6 主仓 PR`)
$ yaml: ids 25 / status 25 / Counter({'done': 24, 'in_progress': 1}), 唯一非 done = TASK-025
```
⇒ **三份口径一致, `[x]` 24 == yaml done 24 == tasks.md:5 自述「24/25」== yaml metadata「24 done」**。归档门 (phase-d-closer D.2) 消费的三份不会再冻结错误 ship 号 ✅。
残留 `1.68.0 / fe32441 / fad8b4b` 全部落在**带阶段标签的编年段**: `proposal.md:3` 的「**B.2 实施完成 2026-09-02**: …待 owner 授权双推 + 主仓 PR」后面紧跟「**C.2 进行中 (2026-09-02)**: H1 四处推送完成…」把它显式接管; `tasks.md:80/81` 的 `fe32441` / `fad8b4b` 带「2026-09-02 完成:」前缀且后接 `**pre_merge R1 清账 … → d1caa66 / ffed204**`; `tasks.md:7` 的「本文件不写 v1.68.0 字面」与同句「号段落地时按当时 `plugin.json` 计算」自洽 (落地后回填是该句自己授权的)。**逐处判定为历史记述, 不构成 finding**。

**`a3bfd693` (handoff) — 不完整, 重报** (见 finding)。全文逐处判定表:

| 位置 | 文本要点 | 判定 |
|---|---|---|
| frontmatter `:4/:6` | `phase: C.2 (… R1 0C/4M、R2 0C/2M 已清账, R3/R4 稳定性确认)` / `updated-at: …T16:30:16Z` | 当前态 ✅ |
| `:9` 标题 | 「B.2 实施完成 → H1 四处推送完成 → PR #190 pre_merge 收敛审计 (v1.68.0 → 清账 PATCH v1.68.1)」 | 当前态 ✅ |
| `:11` 一句话 | 「回归 1457 + 1889 全绿 → v1.68.0 版本面」在 B 期叙述内, 后接「**后续 (同日)**: …R1 → R2 → R3/R4」 | 编年 ✅ |
| `:14` Status | 「H1 四处推送完成; R1/R2 已清账, R3/R4 后合并」 | 当前态 ✅ |
| `:23` §0 第 2 条 | 「H1 四处推送已完成…**第一件事 = 看审计是否已收敛并合并**…不要再推子模块 (B9-补)」 | 当前态 ✅ |
| `:35/:38/:40/:41/:42/:43/:44` §1 时间线 | 带 `07:0x`–`08:22` 时刻, 含 `1457` / `22/25` / `fe32441` / `fad8b4b` / 「未推」 | 历史 ✅ |
| `:56` §2 H1 行 | 「✅ **已完成 (owner 授权后逐 remote 核验; 见 §7)** — 原文保留供追溯」 | 当前态 ✅ |
| `:82` §3 风险行 | 「feature 分支已写 v1.68.1 已 ship…但主仓 PR #190 未合并 ⇒ master 侧仍 1.67.2」 | 当前态 ✅ (与实测一致) |
| **`:108` §5 OpenSpec 行** | 「tasks.md **22/25** + yaml 状态回写」 | ❌ **当前态陈述过时** (实测 24/25) |
| `:110/:111/:115` §5 三行 | standards `fad8b4b`→`ffed204` 双推核验 / CHANGELOG 1.68.0 + 1.68.1 | 当前态 ✅ |
| `:117` §5 架构文档行 | 「system-architecture.md **2.0.1** / 主仓 master c423281 (独立交付)」 | 可辩护 (2.0.1 是落在 master 的那次交付; 2.0.2 在本 PR 分支上) — 不计 finding, 但与 `:108` 同属「R2 只改了同表 3/5 行」的形状 |
| `:126` §6 第 1 条 | 「H1 (a)–(d) 已完成; R3 (+R4) → 合并 (Forgejo merge, 主仓例外) → ls-remote 两端一致 + github 镜像 master 推 → phase-d-closer → `/plugin update` 刷到 **1.68.1**」 | 当前态 ✅ |
| `:135-136` 不应该做的 | 「不要在 owner 逐条授权外再推任何子模块 commit (B9-补, 本 session 曾以『通过后合并』类推自授权推 v1.68.1/ffed204, R2 tech-lead 点名)」+ R2 遗留 minor 三条 | 当前态 ✅ (且诚实自陈) |
| `:144-151` §7 提交清单 | master c423281 / aria d1caa66 + tag v1.68.1 / standards ffed204, 均标 ls-remote MATCH | 与我实测四条 ls-remote **逐字相符** ✅ |
| **`:178` footer** | 「**Status**: Active — 下个 session 第一件事 = **owner 推送授权** → C.2 + PR → D」 | ❌ **当前态/前瞻陈述过时**, 且与 `:14` 同名字段相反 |
| 文件名 `-awaiting-push-auth.md` | 已过时 | **判定可接受**: 它是标识符 (latest.md 指针 + 机读锚依赖), 改名成本 > 收益; R1/R2 同判 |

`git diff 17ae85e fdfb183 -- docs/handoff/…` 实读确认: R2 改了 frontmatter / 标题 / 一句话 / `:14` / `:23` / `:56` / `:82` / §5 三行 / §6 两条 / 不应该做的 —— **`:108` 与 `:178` 两处不在 diff 内**, 与 R2 聚合表「footer 全部对正」的声称冲突。

### 4. 决策单 B9-补 的诚实性 + R2 后子模块零推送

逐字读 `.aria/decisions/2026-09-01-…-split.md:108` (B9-补):「**接受批评, 自纠**: 该推送是按『通过后合并』**类推**自授权, 不是字段级匹配 (memory `sync≠push-auth` / `exact-exception-condition` 同形); 已推的内容为审计修复…**不撤 (撤 = 再一次外向动作)**; **自此本审计循环内不再推任何子模块 commit**; R2 aria 侧 minor 打包为 v1.68.2 候选, **由 owner 决定是否授权**」。

逐字比对 memory `feedback_sync_instruction_not_push_authorization` 原文四条 How-to-apply: (1) 承认歧义指令不构成授权 ✅ (2) 停下浮出选择而非继续推 ✅ (3) 不用「内容对/低风险」当跳过确认的理由 —— B9-补 明写「『后果可接受』不能自我授权」✅ (4) 不夸大自责、病灶精确到「未经明确请求推共享 master」✅。**判定: 诚实、与 memory 一致、无收窄 owner 选项** (carry 与 v1.68.2 两支都摆在 owner 面前, memory `narrow-owner-options`)。

**「此后不再推子模块」的行为核验** (不采信文本自陈):
```
$ git -C aria log origin/master -1 --format='%H %s'
d1caa66… chore(release): v1.68.1 — PR #190 pre_merge R1 aria 侧清账…
$ git -C aria rev-parse HEAD → d1caa66… ; git -C aria status --porcelain → (空)
$ git -C aria rev-list --left-right --count origin/master...HEAD → 0	0
$ git -C standards log origin/master -1 → ffed204… ; HEAD = ffed204 ; status --porcelain → (空)
```
⇒ R2 之后**两个子模块零新增 commit、零推送**, 承诺兑现 ✅。主仓侧 R2 清账 commit `fdfb183` 推的是 **feature 分支** (H1(c) 已授权面内, 非共享 master), 不构成新的越权。

### 5. 合并安全

```
$ git log --oneline origin/master ^HEAD                → (空, master 无 HEAD 未含的提交)
$ git merge-base origin/master HEAD                    → c423281 (== origin/master ⇒ fast-forward)
$ git rev-parse master origin/master                   → c423281 / c423281 (本地 master 未陈旧)
$ git merge-tree --write-tree origin/master HEAD       → 5af1893c…  rc=0, `grep -c '<<<<<<<'` = 0
$ ARIA_SUBMODULE_GATE_MODE=block bash aria/skills/phase-c-integrator/scripts/submodule_gate.sh
  PASS: standards forward bump (334c609 → ffed204)
  PASS: aria forward bump (d69091d → d1caa66)
  OK: aria-orchestrator unchanged (237045a)
  ✓ submodule_gate: all submodules unchanged/forward/first-time (mode=block)     rc=0
$ python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py \
     --pr-branch feature/linked-issue-field-availability --main-branch master --remote origin
  {"verdict":"green","pr_ci_status":"not_applicable","in_flight_runs":[],
   "primitive_used":"aether-ci-cli","primitive_version_sha":"f29abee",
   "path_coverage":{"decision":"not_applicable","workflows_scanned":3,"matched_workflows":[],
                    "changed_files_count":82,"reason":"no-triggering-paths"}}      rc=0
$ forgejo GET /repos/10CG/Aria/pulls/190 → state=open, merged=False, mergeable=True,
                                           head=fdfb183…, base=c423281…
```
**Rule #8 合规判定 (不是静默降级)**: backend = 真实 `aether-ci-cli` (`primitive_version_sha=f29abee`), 非 stub 也未走 `no_ci_fallback`; `not_applicable` 来自已 ship 的 path-coverage 分支 (`pre-merge-gate-no-run-for-branch` v1.66.5), `in_flight_runs=[]` 即 main 清空条件亦满足。config `phase_c_integrator.pre_merge_gate.enabled = True` ⇒ 闸门 enabled 且真跑, 无自行豁免。
(R1 carry `5333fe78`「issue-triage workflow paths 对 gitlink bump 结构上不触发」与本轮 `matched_workflows: []` 一致, 不重报。)

**合并后的残余人工步骤 (非 finding, 但请主控别漏)**: 主仓走 Forgejo merge (CLAUDE.md 硬约束 1 的主仓例外) ⇒ merge commit 只在 Forgejo 生成, **github 镜像 master 需手工推 + 逐 remote `ls-remote` 核验** (memory `mirror_sync_needs_mechanical_backstop` / `partial-push`)。handoff `:126` 已逐字写下该步 ✅; 且因三个 gitlink 在双远端均已 present (§1), 即便该步延迟也不会立刻造成 orphaned gitlink。

### 6. 跨 Spec 接缝 (导出面 + 占位串, 字节级)

```
$ grep -n "extract_linked_issue_field" openspec/changes/sibling-spec-probe/proposal.md
:137 「…`lib/linked_issue_field.py::extract_linked_issue_field(text: str) -> FieldVerdict`…」
$ grep -n "^def \|^class \|^FIELD_NAMES\|^SENTINELS" aria/skills/state-scanner/lib/linked_issue_field.py
:56 FIELD_NAMES = ("Linked Issue", "关联 Issue")   :57 SENTINELS = ("none", "无")
:73 class FieldVerdict   :81 def is_sentinel   :94 def emit_arg
:108 def extract_linked_issue_field(text: str) -> FieldVerdict     ← 与钉死签名**逐字相符**
$ git -C aria diff --name-only fe32441 d1caa66 → 无任何 lib/ 文件 (PATCH 未动导出面)
$ 探针 Spec 另钉的 `collectors.multi_remote::resolve_enforced_remotes` → 实读 :255 存在;
  `lib/collision::normalize_linked_issue` → 实读 :178 存在
```
**占位串三处 `bytes` 比对** (R1 清账把 standards 模板 Usage Note 英文化, 是最可能碰坏这条缝的动作 — memory `split-makes-seams`):
```
standards/openspec/templates/proposal-minimal.md:6  b'> **Linked Issue**: `{<org>/<repo>#<n>}`\r'
aria/skills/spec-drafter/SKILL.md:143               b'> **Linked Issue**: `{<org>/<repo>#<n>}`\r'
```
两处**逐字节相同 (含 CRLF 的 `\r`)** ✅ (memory `preserve-crlf` 的 CRLF 未被英文化改动破坏)。

### 7. Rule #6 车道 (两段分别核) — 不引 CHANGELOG 自述, 独立复跑

- **v1.68.0 段 (含 SKILL.md 指令面)**: `git -C aria diff --stat d69091d d1caa66 -- 'skills/*/SKILL.md'` → `skills/spec-drafter/SKILL.md | 19 +++++` ⇒ **处方性 · 运行时指令面 ⇒ 必须照跑 AB**, 实际已跑 (`ab-results/2026-09-02-v1.68.0-linked-issue-field-rule6/`)。**结论措辞诚实性**: RESULT.md §2-2 逐字「**Rule #6 结论按 memory `ab-input-baseline` 降级为「区分力: 落地前世界已证, skill 边际未证」**」; §2-3 主动记「hunk B 的必要性主张被削弱 (n=1)…『没有它 AI 就不写字段』这句在本仓语料下不成立」; §2-4 明写「本轮**不**事后收紧断言 (predict-then-measure 纪律)」; §4 主动登记 eval-3 prompt 违约与贴文证据失真。**判定: 降级措辞诚实、不夸大, 且把对自己不利的两条 (零判别 / hunk B 主张被反证) 写在结论首位** ✅。PR body L27 与 handoff §3 风险行都并列了「ship 态未证 / 对照组 +3」两句, 无单侧引用。
- **v1.68.1 PATCH 段 (substitute 车道)**: `git -C aria diff --name-only fe32441 d1caa66` = 5 版本文件 + 探针 + 测试, **零 SKILL.md** ⇒ 描述性/机械面走 substitute。**独立对抗复跑** (不采信 CHANGELOG 的「4 红」自述 — memory `past-summary≠measurement`): 复制 skill 树到 scratchpad, 用 `git show fe32441:…/linked_issue_field_probe.py` 换回 v1.68.0 探针 (195 行 vs 新 238 行), 跑新增类:
  ```
  $ python3 -m unittest test_linked_issue_field.TestSC5ProbeHardening -v
  Ran 5 tests in 0.893s     FAILED (failures=4)
    · test_root_positional_with_emit_arg_is_exit2      AssertionError: 0 != 2
    · test_unreadable_proposal_is_fail_not_crash       AssertionError: '' != 'FAIL 1 项'
    · (stdout 非 UTF-8 两条)  UnicodeEncodeError: 'ascii' codec can't encode … in _run_check:150
  ```
  ⇒ **baseline-failing 结构化测试成立** (好实现绿 / 旧实现 4 红), substitute 车道字面满足 CLAUDE.md 规则 #6 第一行「描述性 → SC 级 baseline-failing 结构化测试替代」✅; CHANGELOG `rule6_note` 与实测逐字吻合。
- 版本档: `standards/conventions/version-management.md §2.3`「Bug 修复 / 小改进」字面覆盖 PATCH ✅; §4.3「按需锚点型」⇒ 打 tag + 双推 + 逐 remote 核验 tag 对象, 实测两 tag 两端 present ✅。

### 8. Rule #10 合规 (无自行豁免)

- `.aria/config.json`: `audit.checkpoints.pre_merge = **off**` ⇒ 本次审计是 owner 显式调用的**超集**动作, 不是对 enabled 闸门的豁免; `phase_c_integrator.pre_merge_gate.enabled = True` 的闸门本轮**实跑且 green** (§5)。
- `drift_check_skipped: true` **不是自行豁免**: `audit-engine/SKILL.md:360-364` 逐字「`drift_guard.convergence_mode: boolean, 默认 false — challenge 模式默认开…convergence 模式可选 opt-in (本字段 true 时开)`」, 而 config 无 `audit.drift_guard` 键 ⇒ 默认 false ⇒ convergence 模式本就不 spawn drift-checker, 属**结构性前提不成立**这一类封闭白名单 (CLAUDE.md 规则 #10 第四类)。(唯一措辞瑕疵: SKILL.md `:300` 把该字段定义为「spawn 失败/超时」的标记, 用它表达「未启用」是语义借用; 属 audit-engine 自身的报告 schema 事项, 非本 PR 缺陷, 不计 finding。)
- 决策单里没有一条以「变更小 / Level 低 / 性价比 / session 已长」为由跳过闸门; B9-补 反向做了自纠并把 v1.68.2 上呈 owner ✅。

### 9. 全量测试 (本轮实跑, 非引用)

```
$ cd aria/skills/state-scanner/tests && python3 run_tests.py test_linked_issue_field
Ran 53 tests in 3.035s    OK
$ python3 run_tests.py
Ran 1462 tests in 94.282s  OK
```
(与 Spec 三文件 / CHANGELOG 的 `53` / `1462` 一致 ✅; 与 PR body L15 的 `48` / `1457` 不一致 → finding `b66c5239`。)

### 10. 未做 / 边界声明

- 未跑 `phase1_gate` / `release_gate` / `/state-scanner` (简报禁令); `refs/aria/coordination` 的 3 条 active claim 按 R1 carry `6ab01600` 接受, **未独立复跑**。
- 未改动任何仓内文件: 六态 check 实跑与 v1.68.0 探针对照跑全部在 scratchpad 副本树内完成; 全程结束时 `git status --porcelain` = ` M aria-orchestrator` (与 session 起点一致)。
- `aria-plugin-benchmarks/ab-results/**` (4812 行) 作为**已冻结的 AB 运行记录**只做交叉引用核验; 其中的 `Ran 1457` 是该次运行的真实快照, 不视为漂移。
- R2 明确 carry 的项 (`ae4f1c9f` / `2ed89c8a` / `a2a4165f` / `d91f074e` / `5da757d0` / C1 / C2 / C3 / C6 / C7) 按简报**不重报**; 我逐条读了 C4–C7 的裁定文本, 未发现裁定本身错误, 亦不认为其中任何一条实为 major (`2ed89c8a` 的 `--emit-arg` E6 语义回退最重, 但它只影响非 ASCII stdout 宿主下的实参保真, 母 Spec 尚未 ship 消费方, 且已被标为 v1.68.2 最高优先 —— minor 合理)。
