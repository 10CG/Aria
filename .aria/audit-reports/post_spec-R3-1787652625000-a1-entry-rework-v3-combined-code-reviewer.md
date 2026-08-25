---
checkpoint: post_spec
round: 3
role: code-reviewer
mode: convergence
combined: true
verdict: REVISE
scope_ok: true
counts: 1C/4M/10m
specs:
  - name: a1-entry-claim-duplicate-work-guard
    round: 3
    verdict: PASS_WITH_WARNINGS
    counts: 0C/1M/5m
    scope_ok: true
  - name: linked-issue-field-availability
    round: 1
    verdict: REVISE
    counts: 1C/3M/3m
    scope_ok: true
  - name: sibling-spec-probe
    round: 1
    verdict: PASS_WITH_WARNINGS
    counts: 0C/1M/2m
    scope_ok: true
timestamp: 2026-08-25T10:30:25.000Z
context: >
  openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md (R3) +
  openspec/changes/linked-issue-field-availability/proposal.md (R1) +
  openspec/changes/sibling-spec-probe/proposal.md (R1)
agents: [code-reviewer]
---

# post_spec R3 (母) / R1 (两子) — combined — code-reviewer

> **镜头**: 事实纪律与自述准确性 —— 逐条实读全部 `文件:行号`, 比对**断言说的内容**与**那行实际写的内容**;
> 找「自述已做而实际未做」「引用不存在的锚点」「对账表与实际落点不符」。

## 审计对象与实读环境

| 项 | 值 |
|---|---|
| 主仓 HEAD | `027a50f` (工作树仅 ` M aria-orchestrator` gitlink, 与本审无关) |
| 本轮 diff | `git show --stat 027a50f` = 6 文件 / +1702 / −193 |
| 前一 commit | `2ae012f` (**同 session**, 加了第 11 条 state-check — 见 LIFA-M2) |
| 母 Spec 引的语料基线 | 主仓 `cc1bdef` (实测: 147 篇 / 15 文件 / changes 7 — **逐条复现成立**) |
| aria 基线 | `d50f9c3` — 实读命令 `git -C aria show d50f9c3:<path> \| sed -n '<N>p'` |
| 主仓 gitlink | `58a49e7` (落后 2 commit, 已知且有意) |

本席实跑的核验面 (非转述): aria 代码/文档 **约 60 处** `文件:行号` 逐行 `cat -v` 比对 · 主仓语料 **10 处**归档件字段行逐行 · `git show 86540f2` 两段 owner 裁定 `diff` · 母 Spec 两条「实跑复现」在 `d50f9c3` 上重跑 · 探针 SC-18 **三臂全量重算** (147 篇) · lifa E0–E6 规则原型**全量重跑** (149 篇) · 本机 git 事实 (remote/refs/symbolic-ref/version) · Forgejo issue #150/#135/#157 标题 · 审计轨搬运的**逐段 `in` + 连续块**双断言。

---

## 一、R1/R2 finding 逐条 closed / open (本席 R2 报告体例)

### R2-CR 本轮新 findings (6 条) — **6/6 closed**

| R2 id | 状态 | 本轮实读证据 |
|---|---|---|
| **R2-CR-C1** 抽取规则 defer ⇒ check 恒红 | ✅ **closed** | §1 整节迁出; lifa §3 **E0–E6** 钉到字符级 + 四态穷尽表。本席重跑其规则原型: 149 篇 → `NO_FIELD` 132 / `NO_TOKEN` 14 / `OK` 3, `changes/` 9 份 = OK 3 + NO_FIELD 6 —— **与 lifa §Why/§5 表逐格一致**。⚠️ 但派生出新 Critical **LIFA-C1** |
| **R2-CR-M1** heartbeat track 来源未定义 | ✅ **closed** | §2.2 三级回落 (① 编排层 telemetry — 实读 `phase-b-developer/SKILL.md:88` 逐字 `check: phase1_gate telemetry / 编排层记忆…` 成立; ② handoff §6 carry-id; ③ 跳过+`log()` 不猜) + CLI 显式传入 + **正面答复本席 CR-M1 并显式否决其 B 方案** (僵尸 keep-alive 与 SC-7 结构相反) |
| **R2-CR-M2** 「无条件」× `enabled` 门控 | ✅ **closed** | `:208-209` 把「无条件」限定为「不依赖 `collision.kind`」, 明写 heartbeat 同受 `coordination.enabled` 门控, **SC-28** 钉 `false ⇒ 零调用` |
| **R2-CR-M3** `STALE_TTL` 消费者漏查 | ✅ **closed by withdrawal** | (iii) 撤销 ⇒ 常量不动 ⇒ 影响面整体消失 (`:230` 明写)。全文 grep 无任何残余「改 `STALE_TTL`」断言 |
| **R2-CR-M4** 三处「R1-fix 已全量吸收」不实 | ✅ **closed** | 全文 grep「已全量吸收/已全部处理」**仅命中 3 处否定式/引述** (`:7` `:654` `:720`); 换成 FIX-01…19 **逐条对账表**。⚠️ 对账表自身残 2 条 minor (M-m2/M-m3) |
| **R2-CR-M5** `unknown` 处方结构性不可达 | ✅ **closed** | §2.4a 独立键 `unknown_schema_claims` + **本席重跑其实测**: `parse_claim({schema_version:'99', linked_issue:'10CG/aria-plugin#122'})` → `status='unknown'`, `linked_issue=None`, `track_id=''`/`container=''`/`claimed_at=''`; `linked_issue_overlaps([rec],'my-track','10CG/aria-plugin#122')` → **`[]`** — 与 Spec `:293` 逐字一致 |

### R2-CR minor (6 条) — **5 closed / 1 still-open**

| R2 id | 状态 | 证据 |
|---|---|---|
| m1 SC-20 无上界 | ✅ closed by withdrawal | SC-20 `:556` = ⛔ 撤销 |
| m2 129 vs 128 两套数字 | ✅ closed | 换 `cc1bdef` 实测口径; 本席复现 147 / 15 (14 archive + 1 changes) / changes 7 —— **三个数全中** |
| m3 清单不含 §4 引用 | ✅ closed | §4 迁出 + 清单扩到 **34 行** (审计轨 §5 实测 #1–#34 齐全, 正文交叉引用的 #22/#26/#28/#29/#30/#33 **全部指得到**) |
| m4 D6 依据格未随动 | ❌ **still-open (minor)** | D6 `:456` 依据格仍写「**S3** 实测无该函数」, 未加 `:268` 已订正的**「定向」**限定词; §2.3 正文与 D6 表两读 |
| m5 姊妹协调项措辞过时 | ✅ closed | `:322` 已改引姊妹 `:257`/`:260` (⚠️ `:260` off-by-one, 见 M-m3) |
| m6 heartbeat fetch 代价未披露 | ✅ closed | `:221-225`「fetch 代价与复用」段: 复用 Phase 0.5 结果 ⇒ 增量 **0**, 并披露违规自带 fetch 的 ~13.8s。本席实读 `state-snapshot-schema.md:1029-1041`/`:1043`/`:1056`/`:1061-1064` **四处全部逐字成立**, 其 fail-CLOSED 谓词 (`success==true` **且** `coordination_ref_present==true`) 与 schema 语义一致 |

### R1 聚合簇与本席 R1 残项 — **全部 closed 或经 owner 裁定迁出**

C1 ✅ / C2 ✅ / **C3 → 迁 lifa** / C4 ✅ / C5 ✅ / C6 ✅;
M2 ✅(§5.1+SC-27) · **M3/M7 → 迁 sibling** · **M4/CR-M9 → 迁 lifa** · M5 ✅(§2.5+§6 首行) · M6 ✅(§2.4b+SC-25) · M8 ✅(SC-22) · M9/M10 ✅(SC-8/9/10 拆+类别订正) · CR-M1 ✅(SC-1 钉 issue 派生形) · CR-M2 ✅(§2.1a 两层) · CR-M3 ✅(D16 增并存变体) · CR-M4 ✅(§2.3 status 分档) · CR-M5 ✅(unattended+D15+SC-26) · CR-M8 ✅(DEFAULTS.json 入 Impact+substitute) · CR-m1/m2 ✅ · **CR-m3 → 迁 sibling §8** · CR-m4 ✅(FIX-19, `:12`) · BA-minor ✅(§5.2 命令形态订正) · TL-minor ✅(`layer-l-integration.md:45` 入 Impact + 清单 #33) · KM-minor ✅(两文件入 Impact)。

> **同口径 major: 15 → 1。** 本席 R2 的 1 Critical 已 closed。按 memory `stop-adding-rounds`「加轮判据是 major 数是否还在降」—— 母 Spec 侧已收敛。

---

## 二、本轮新 findings

### 母 Spec `a1-entry-claim-duplicate-work-guard` (R3) — 0C / 1M / 5m

| id | severity | category | 定位 | 标题 | 证据 (本席实跑) | 处方 (字符级) |
|---|---|---|---|---|---|---|
| **M-M1** | **Major** | self-description-accuracy / audit-trail-integrity | `proposal.md:19` · `:439` · `.aria/audit-reports/a1-entry-claim-audit-trail.md:15` | 「**按字节搬运, 未重写任何一句**」对审计轨 §5 **不成立**; 审计轨头部「唯一新增的是本文件的标题与各节标题」**三重不实** ⇒ 「无损搬运」在任何**已提交**产物上不可复核 | 取唯一已提交前身 `git show 2ae012f:…/proposal.md`, 其 `## 事实断言逐条实读清单` = 29 行 (`:283-311`)。程序比对: **连续块匹配 = 无**; **22/29 行在整个审计轨中一个字都找不到**。原因: 本轮把 #1–#17 从 `cb6bd5d` 口径**整表重生成**为 `d50f9c3` 口径 + 新写 #18–#34。对照: §1 (审计与 spike 轨迹) 25 行**连续块命中于审计轨 `:31`** ✅; §2/§3/§4 各**多一条本轮新写的编者注**(「> **现状**: owner 2026-08-23 裁定…」/「> **闭环**: owner 已于 2026-08-23 回应…」/「> **闭环**: 该条自陈…」), 三条在 `2ae012f` 中均无 | ① `:19` 与 `:439` 分节陈述, 逐字改为:「**§1–§4 = 逐字搬运** (可用 `git show 2ae012f:…` 逐块比对), **§5 = 本轮整表重新实读后直接落审计轨** (#1–#17 由 `cb6bd5d` 口径改写为 `d50f9c3`, #18–#34 为新增) —— **§5 不是搬运**」; ② 审计轨 `:15` 的「唯一新增的是本文件的标题与各节标题」改为「新增 = 本文件标题 / 各节标题 / §2–§4 各一条状态注 / **§5 整表**」; ③ commit message 的「无损搬运经程序断言 (缺失行 0)」须注明**其比对基线是未提交的中间工作树**, 不是 `2ae012f` |
| **M-m1** | minor | false-self-assertion | `:662` (FIX-04 行) | 对账表自述「全文 grep `A1_SWEEP_TTL` = **0 命中**」实测 = **1** —— 命中的正是该行自身 | `grep -n 'A1_SWEEP_TTL' proposal.md` → 仅 `662:| FIX-04 \| C2 — 删 \`A1_SWEEP_TTL\` 72h 分档 \| … \| 全文 grep \`A1_SWEEP_TTL\` = 0 命中 \|`。与本批三份 Spec 反复论证的「check 被自己的文档触发」是**同一形状** | FIX-04 状态格改为「**已落**; 复核命令 `grep -c A1_SWEEP_TTL proposal.md` 应 = **1** (仅本行自身), 正文/SC/Impact/决策记录四段内 = 0」 |
| **M-m2** | minor | anchor-not-greppable | `:655` (对账表锚点承诺) · `:663` (FIX-05) · `:673` (FIX-15) | 对账表 `:655` 承诺「锚点串可直接在本文件内 grep」, 但 FIX-05 / FIX-15 的锚点串在其声称的三个落点里各只落到 **两处**, 且 FIX-15 的「三处逐字同一句谓词」自述不成立 | FIX-05 锚点 `超 STALE_TTL` → 实测命中 `:268` `:614`; 而声称的 §非目标 `:584` 与 follow-up #2 `:633` 用的是「`SWEEP_TTL`→`STALE_TTL` 措辞」, **零命中**。FIX-15 锚点 `形态是否含 slug` → 实测命中 `:393` `:402` `:462`(D12); 而 SC-1 `:520` 写「**不含 slug**」、SC-15 `:544` 写「**含 slug**」, **两者都不含该整句** —— 而 `:393`/`:402`/`:462` 三处均自称「§5.1 / SC-1 / SC-15 **逐字同一句谓词**」 | FIX-05 锚点改 `SWEEP_TTL` 或直接给行号; FIX-15 二选一: (a) 把 SC-1/SC-15 的括注改为逐字嵌入「track-id 形态是否含 slug」整句, 或 (b) 把 §5.1/D12/SC-1/SC-15 四处的「**逐字**同一句谓词」改为「**同一个**谓词 (含 slug / 不含 slug 两分支)」 |
| **M-m3** | minor | line-ref-off-by-one | `:322` · `:669` (FIX-11) · 审计轨 `:116` (#16) | 归档姊妹 Spec 的关闭条款引 `:260`, 实际在 **`:259`** | `sed -n '256,260p' openspec/archive/2026-08-23-linked-issue-normalization/proposal.md`: `:257` = `⭐ **include_terminal 形参由 a1-entry-claim 引入…** (owner 裁定 2026-08-08)` ✅ **准确**; `:259` = `⇒ **D6 与 §接口面…**: 本 Spec 不改签名; 母 Spec 落地时追加 keyword-only 形参**不视为对本 Spec 的违反, 也不构成回归**` ← Spec 引作 `:260`; `:260` 实为 `*(R2′ 曾把该协调项记为「随 Q6 消失」…)*`。三处同错 | 三处 `:260` → `:259` |
| **M-m4** | minor | stale-self-check | `:82` | 「**落盘后的现状 (可当场复核)**: … `changes/` 下的 **1 条**命中现在是**真阳**」—— 当场复核得 **3 条** | `grep -rl '\*\*关联 Issue\*\*' --include=proposal.md openspec/changes/` → 母 / lifa / sibling **三份**。承重结论 (母 Spec `:12` 已是真字段) 本席**实读成立** ✅, 只是计数已被同批两个新 Spec 改写 | 改为「`changes/` 下现有 **3** 条命中 (母 `:12` / `linked-issue-field-availability:6` / `sibling-spec-probe:6`), **三条都是真阳**」 |
| **M-m5** | minor | evidence-range-mismatch | `:176` (§2.1b 第 3 点) | 「实读 `lib/track_id.py:61-76` 的归一四步**不含任何去容器段逻辑**」—— `:61-76` 是 `def` + docstring 前半, **结论须读实现体** | `git -C aria show d50f9c3:skills/state-scanner/lib/track_id.py`: `:61` = `def derive_track_id(`, `:70-76` = docstring 四步枚举, **可执行体在 `:154-170`** (`use_fallback` / sha256 / `lower()` / `translate` / `[:64]`)。本席代读 `:154-170` —— **结论成立** ✅ | 行号改 `:61-76` (契约) **+ `:154-170`** (实现), 或直接改成 `:154-170` |

**母 Spec 经本轮实读确认成立 (下轮免重复)** — 以下**全部**逐字核过, 无一失配:

1. **两段 owner 裁定 blockquote 与 `86540f2` 逐字节相同** —— `diff <(git show 86540f2:…| sed -n '150p') <(sed -n '201p' 现文 | sed 's/^> > /> /')` 与 `:214`↔`:367` 同法, **两次 diff 均为空**;
2. **(iii) 撤销的四个落点全部执行**: SC-20 `:556` ⛔ / Impact `constants.py` 行 `:603` 只留 `:43-44`+`:50` 注释同步 / §2.3 `:269-273` 重写为双向 (a)(b) / 闸门状态 item 3 `:721`; 全文**零残余** `STALE_TTL` 变更断言;
3. **两条「实跑复现」在 `d50f9c3` 上重跑输出与 Spec 逐字一致** (NEW-01 `无`×`无` 互相命中 → `[{'track_id':'spec-b-uuid2','linked_issue':'无',…}]`; unknown sentinel → overlap `[]`);
4. **aria 侧行号断言逐条成立** (本席实读, 非清单转述): `collision.py` `:46`/`:178`/`:219`/`:230-234`/`:265-266`/`:268`/`:272-275`/`:278-279`/`:265-292`(体) · `claim_schema.py` `:130`/`:165`/`:222-229` · `identity.py` `:191`/`:222`/`:242`/`:244` · `track_id.py` `:61`/`:70-76` · `constants.py` `:32`/`:36`/`:40-42`/`:43-44`/`:50`/`:51` · `claim_lifecycle.py` `:178`/`:228`/`:274`/`:377`/`:425`/`:427`/`:430` · `reconcile.py:154-163` · `gc.py:338-344` · `coordination_ref.py` `:119`(仅 claims/errors/ref_exists)/`:596` · `phase1_gate.py` `:210`/`:283-294`/`:335`/`:1032`/`:1173`/`:1230`/`:1233-1235`/`:1236-1238` · `release_gate.py` `:141`/`:225`/`:236-237` · `phase-b-developer/SKILL.md` `:86`/`:88`/`:89`/`:91-93` · `branch-manager/SKILL.md:146` (标题逐字全中) · `phase-d-closer/SKILL.md` `:42`/`:51-52`/`:55`/`:56` · `state-scanner/SKILL.md` `:149`/`:176` · `layer-l-integration.md` `:15`/`:45` · `config-loader/SKILL.md` `:134`/`:140` · `DEFAULTS.json`(无 `coordination`) · `coordination-ref-schema.md` `:129`/`:133-139` · `test_coordination_default_lockin.py` `:53`/`:55-56` · `state-snapshot-schema.md` `:1029-1041`/`:1043`/`:1056`/`:1061-1064`;
5. **三条被点名的「未实读」项本席代验后成立**: 7c 条件 `and not _takeover_eligible(verdict)` 在 `phase1_gate.py:652`, `kind="occupied"` 在 `:669`, 7d 注释 `# No prompt needed: stale / terminal tracks are safe to acquire.` 在 `:718` (存疑 #2 声明未取行号 —— **原文引用逐字正确**);
6. **`update_heartbeat()` 确为悬空**: `git -C aria grep -n update_heartbeat d50f9c3` **全仓只命中 `layer-l-integration.md:45` 自身**, 真名 `heartbeat()` 在 `claim_lifecycle.py:178` —— Impact 行的 ①②③ 三项**全部属实**;
7. **`fetch_degraded` 确实只在 docstring**: 全仓 3 处命中中 `phase1_gate.py` 仅 `:210`, **无任何 `error=` 赋值**;
8. **`linked_issue_overlaps` 生产调用点确为唯一**: 全仓命中里 `phase1_gate.py` 只有 `:81`/`:119`(import) + `:1233`(唯一调用), `_run_gate_impl` 零命中;
9. **AB 套件计数属实**: `phase-a-planner.json` evals=**2** / `spec-drafter.json`=**2** / `state-scanner.json`=**12**;
10. **语料口径 (`cc1bdef`) 属实**: 147 / 15 (14 archive + 1 changes) / changes 7;
11. **SEAM-1 的自查订正属实**: SC-2 `:521` 期望列**只有**「双方 `linked_issue_overlap` 各含对方」这一条正向断言, **确无反向臂** ⇒ 旧版「由 SC-2 反向臂承担」确为不实, SC-29 接得对;
12. **审计轨 §5 表结构完整**: #1–#34 齐全, 正文所有 `见清单 #N` (#1/#2/#3/#4/#5/#6/#11/#14/#16/#17/#22/#26/#28/#29/#30/#33) **无一指空**。

---

### 子 Spec `linked-issue-field-availability` (R1) — 1C / 3M / 3m

| id | severity | category | 定位 | 标题 | 证据 (本席实跑) | 处方 (字符级) |
|---|---|---|---|---|---|---|
| **LIFA-C1** | **Critical** | clause-contradiction / perpetual-red | **D3 `:382`** × **D6 `:385`** × §5 陈旧守卫 `:318` × §1 已知限 `:140-142` × SC-5(c) `:413` | **D3 (宿主改判到 plugin 分发面) 与 D6 (硬编码 Aria 专属 6 条 `GRANDFATHERED` 路径) 相撞**: 白名单写在**随 aria-plugin 分发到每个采用方**的脚本里, 而陈旧守卫子情形 **(a)「该路径当前不存在」** 在任何非 Aria 仓上对 6 条**全部命中** ⇒ 探针 **exit 1 恒红**, 输出「allowlist 陈旧: openspec/changes/aria-2.0-m6-cost-model-telemetry/proposal.md (a)」这种对采用方毫无意义的文案。这正是 D6 自己援引 memory `false-green-dual-is-permanent-red` 要避免的**恒红**, 只是换了个仓 | 逐条链: `:264` 宿主 = `aria/skills/state-scanner/scripts/linked_issue_field_probe.py` (随 plugin 分发, `:136` 自陈「随 aria-plugin 一并到达采用方」); `:317-318` 五臂表第 4 行 = `GRANDFATHERED` 含陈旧条目 (a)/(b)/(c) **任一命中即 `FAIL` exit 1**; `:355-360` 白名单内容 = 6 条 `openspec/changes/aria-2.0-m{6,7}-*/proposal.md` **Aria 专属路径**; `:303-304` fix 文案要采用方「删除 `linked_issue_field_probe.py` 的 GRANDFATHERED 里那一行」= 要采用方改 plugin 分发件。⇒ **采用方每轮恒 FAIL 且无正当修法**。而 `:140-142` 自述「残余缺口**只剩注册那一步**」「比『拿不到校验』**弱得多**」—— **不成立**: 注册了反而恒红 | 二选一 (推荐 (a)): **(a) 数据与机制分离** —— 脚本只带 `GRANDFATHERED` 的**读取机制**, 名单本身移到**项目侧**数据 (例如 `.aria/state-checks.yaml` 该 check 的一个已在用键内, 或项目内一个 allowlist 文件路径由 `argv[1]` 之后的第二个实参传入); 脚本内置名单**逐字为空**。同批把 §1 已知限改为「残余缺口 = 注册 + 各自维护本仓 allowlist」, SC-5 加第五臂「**脚本内置 allowlist 为空**」钉住不回退。**(b)** 若坚持内置, 必须在陈旧守卫 (a) 前加一条 fail-CLOSED 的前置判据并成文其代价 —— 但任何「路径都不存在就整体 SKIP」都是 fail-OPEN, 与 §5 的白名单极性相反, **不推荐** |
| **LIFA-M1** | **Major** | fact-assertion / invented-line-number | §Why `:58` · `:64-67` · **D2 `:381`** · **SC-1 `:409`** | **§Why 的三处行号引用在被审 commit 上全部指错**, 其中 `母 Spec :88` 这个「**真实的**假阳性实例」在**任何已提交 SHA 上都不在 `:88`**, 且它是 E0 谓词 1 的**唯一真实语料证据**, 被 D2 与 SC-1「怎么会红」两处当承重实证 | ① `sed -n '88p' openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (被审 `027a50f`) = `### §1 「关联 Issue」字段可得性 — ⛔ **整节已迁出**`; 前一 commit `git show 2ae012f:…\|sed -n '88p'` = `  --phase A.1 --mode advisory \`。母 Spec 全文现只有 3 处 `**关联 Issue**` (`:12` 真字段 / `:81` 散文 / `:677` 对账表), **深度-2 的 `> > ` 示例行已随 §1 一并删除, 语料中不复存在**。② 真实位置是 `cc1bdef:75` —— 本席实读 `git show cc1bdef:…\|sed -n '75p'` = `   > > **关联 Issue**: [10CG/aria-plugin #122](…)` ✅, **姊妹探针 Spec `:99` 正是这样引的 (钉 SHA + `:75`)**, 两份 Spec 对同一实例一对一错。③ `:64-67` 自引「多出的 2 行都在本文件内 (`:65` / `:86`)」—— 实测本文件严谓词命中在 **`:6` / `:95` / `:116`**; `:65` 现为该 grep 输出块内的一行文本, `:86` 现为「与探针 Spec 的计数差异」blockquote。**机械核验器判「该行存在」全过, 内容全错** | ① `:58` / D2 / SC-1 三处的 `母 Spec :88` 全部改为 **`母 Spec(cc1bdef):75`** 并在句中钉 SHA, 同时补一句「**该实例已随母 Spec §1 迁出而不复存在于当前语料; 形状的现存实证由 `sibling-spec-probe` SC-18(b) 臂在 `cc1bdef` 语料上承担**」; ② `:65`/`:86` 改 `:95`/`:116`; ③ 采纳姊妹探针 Spec 的纪律 (`sibling-spec-probe:16`「**不引用母 Spec 的任何行号**」) —— 本文件 `:12` 的 `母 Spec :92` 一并改成小节名引用 |
| **LIFA-M2** | **Major** | stale-measurement / incomplete-enumeration | §4 `:239` · `:242-260` · `:262` · **D3 理由 1 `:270`** · `:283`/`:309` · 新表面 #6 `:469` | 「实读 `.aria/state-checks.yaml` (共 **10** 条 check — `grep -c '^  - name:'` = 10)」在**被审 commit 上实测 = 11**; 形态 (iii) 实为 **3** 条且「也是**最近两条**新增」已被本审计范围的**前一个 commit** 推翻; D3 归属判据建立在「既有**两条** `.aria/probes/`」这个**穷尽枚举**上, 而枚举不完整 | `grep -c '^  - name:' .aria/state-checks.yaml` → **11**。第 11 条 `main-project-version-consistency` (`:289`, `command: python3 .aria/probes/main-project-version-consistency.py` `:307`) 由 `git log -1 -S… ` 查得引入于 **`2ae012f`** = `027a50f` 的**父 commit**, 同 session。⇒ (i) `:239` 的 `= 10` 与 `:262` 的 `6+2+2=10` 分档均假; (ii) `:262` 的「(iii) … 也是**最近两条新增**」假; (iii) `:270` 的「既有两条 `.aria/probes/` 探针**都只对 Aria 本仓有意义**…⇒ 与既有先例**性质不同**」是**正向枚举式论证**, 漏掉第三条 (本席核: 第三条同属 Aria 自检, **结论侥幸存活**, 论证前提不完整)。注: `:283` 的「只用既有 10 条已在用的键」结论**存活** —— 本席读第 11 条, 用的仍是同一 7 键。⚠️ `:31` 的全局免责 (「全文凡引数字处均适用」) 挡得住计数, **挡不住被当作穷尽集的枚举** | ① `:239` 改「共 **11** 条 (复核 `grep -c '^  - name:'`)」; ② `:242-260` 的 grep 输出块补 `:289`/`:307` 两行; ③ `:262` 改「(i) 6 · (ii) 2 · (iii) **3** (config-template-key-currency / plugin-cache-currency / **main-project-version-consistency**)」并删「最近两条新增」; ④ D3 理由 1 补第三条的性质判定一句 (它同属「Aria 对自己的自检」⇒ 结论不变), 并把措辞由穷尽枚举改为「**截至 `027a50f` 的全部 3 条**」 |
| **LIFA-M3** | **Major** | cross-spec-seam / stale-claim (与 **SSP-M1** 同一接缝, 两侧各一处落点) | §3 对照表 `:225` · `:230` · `:232` · 引言 `:219` | 主控 SEAM-2/SEAM-3 的修复**只落在探针 §3, 未回灌本文件的对照表** ⇒ 本文件对姊妹现状的 4 条断言在**同一 commit 内**即为假, 而这张表的立项理由恰是「**防 spec-underdetermination**」 | 逐条比对被审 commit 的 `sibling-spec-probe/proposal.md`: ① `:225` 断言姊妹「围栏排除: **无该谓词**」/「本 Spec 多一条」/「**不要求探针 Spec 加这条**」—— 探针 `:89` 谓词 (2) **已逐字采纳围栏排除**, 且 `:101` 明写「姊妹侧原文写『不要求探针 Spec 加这条』—— **本席仍加**」; ② `:230` 断言 `BAD_TOKEN`「其**三态**契约里没有这一格」—— 探针 `:107-113` 已是**四态分派表**且 `BAD_TOKEN` 独占一行 (层 1 ∪ 层 2); ③ `:232`「⇒ **唯一实质差异** = `BAD_TOKEN` 在探针的三态契约里无归宿」—— 已无该差异; ④ `:219`「探针 §3 层 1 **单方面**声明…三态, 并在其『新表面』第 6 条自陈**未与本席交叉核对**」—— 前半已假 (探针 §3 已四态), 后半仍真但那正是 **SSP-M1** | ① `:225` 第 3 列改「**已逐字采纳** (探针 §3 层 0 谓词 (2))」, 第 4 列改 ✅ 一致; ② `:230` 第 3 列改「**层 1 ∪ 层 2 并集** (探针 §3 层 1 分派表)」, 第 4 列由 ❌ 改 ✅; ③ `:232-235` 整段改为「姊妹已采纳并加强 (层 1 已解析元素不丢弃), 本 Spec 四态**不改**; 探针 `:131` 已回应本 Spec 的『反向不成立』并划清 `--linked-issue` 实参面 vs 只读比较键面 —— **分歧已消解, 不再需要主控协调**」; ④ `:219` 删「单方面声明…三态」改「探针 §3 层 1 现按**四态**分派」 |
| **LIFA-m1** | minor | stale-number | `:36` · `:45` · `:50-52` · `:79` | 松谓词行数 / 松→严差额 / 逐文件分布已被同批编辑改写 | 被审 commit 实测: 松谓词**行** = **39** (Spec 记 37); 松→严差 = **20** (记 18); 逐文件 = 母 **2** / 本 **11** / 探针 **7** (记 3 / 11 / 4)。其余 6 个数 (149 / 17 / 17 / 19 / 9 / 140) **全中** ✅; 结构性结论「差额全部落在三份讨论该字段的 Spec 里, 无一是真字段」**仍成立** ✅ | 重跑一次把 4 个数刷新, 或在 `:45` 加一行「本节数字含**本文件自身**, 每次编辑本文件即变 —— 结构性结论 (差额全落在三份讨论该字段的 Spec 内) 不随之变」 |
| **LIFA-m2** | minor | dangling-reference | `:13` | `(F-10)` 指向仅存在于 scratchpad 的主控说明书, **仓内无锚** | `git grep -n 'F-10'` 在仓内零命中; 对照 `F-39`/`F-40` **在审计轨 `:24`/`:25` 有显式锚**(「(= F-39)」/「(= F-40)」)。F-10 的事实本身 (`phase1_gate.py:1230` 整块门控) 本席实读**成立** ✅ | 删 `(F-10)` 或在审计轨 §1 补一行带 `(= F-10)` 的锚 |
| **LIFA-m3** | minor | anchor-name-mismatch | `:90` · `:185` · `:412` · `:457` | 正文四处写「见 §**实读清单**」, 实际节名是「**实读与重测**清单」(`:452`) | `grep -n '§实读清单' proposal.md` → `:90` `:185` `:412`; 节标题 `:452` = `## 实读与重测清单 — ⛔ **整表已切出**` | 统一为「§实读与重测清单」或把节名改短 |

---

### 子 Spec `sibling-spec-probe` (R1) — 0C / 1M / 2m

| id | severity | category | 定位 | 标题 | 证据 (本席实跑) | 处方 (字符级) |
|---|---|---|---|---|---|---|
| **SSP-M1** | **Major** | self-contradiction (同文件内) / stale-claim | 新表面 **#6 `:508`** · **#7 `:509`** vs §3 `:105-116` · `:101` · `:120` · `:131` | 「本轮引入的新表面 (未审)」段仍自陈「本 Spec **单方面声明**了姊妹的抽取器返回**三态**」「**本席未与其交叉核对**」「**未与姊妹席对齐**」—— 与**同一文件** §3 的现状**直接矛盾**: §3 已按四态分派、已逐字采纳姊妹 E0 三谓词、已逐条回应姊妹的建议映射与「反向不成立」论证。这一段是给 R1 审计席的输入, 陈述失真会让审计席在**错误的完成度假设**上工作 (正是母 Spec `:699` 自己援引的 memory `past-summary≠measurement`) | `:105` 逐字「**消解 SEAM-2** (主控 2026-08-25 核验): **上一版本节声明消费契约是三态**…下表逐格补全」+ `:107-113` 四态分派表 (含 `BAD_TOKEN` 行) ⇒ #6 的「三态」已被本文件自己推翻; `:101` 逐字「姊妹侧原文写『不要求探针 Spec 加这条』—— **本席仍加**」+ `:120` 「**采纳姊妹席的建议**…并在其上追加一条」+ `:131` 「**对姊妹席『反向不成立』那条论证的回应**」⇒ #6/#7 的「未交叉核对 / 未对齐」已被本文件自己推翻 | ① #6 改为:「**已消解 (SEAM-2)**: §3 层 1 现按姊妹**四态**分派, `BAD_TOKEN` = 层 1 ∪ 层 2。**残余风险改为**: 姊妹侧改动四态定义时本节映射表须同批改 (`:85` 已成文该义务), **无机械护栏**」; ② #7 改为:「**已消解 (SEAM-3)**: 层 0 逐字采纳姊妹 E0 三谓词, 不再自带第二份定位规则。**残余**: 两侧仍是两份文本 (非一份 SOT + 一处引用), 漂移只能靠人 —— 建议 A.2 加一条断言两侧 E0 文本一致的结构化测试」; ③ 同批把 **LIFA-M3** 的对照表回灌, 两侧必须同一批改 (memory `fixes-contradict`) |
| **SSP-m1** | minor | internal-number-contradiction | rule6_note `:408` vs 新表面 #4 `:506` vs follow-up #2 `:488` | 同一文件对 `ab-suite/` 的 `.json` 数给出**两个互相矛盾**的值 (**30** vs **31**); 实测 **31** | `ls aria-plugin-benchmarks/ab-suite/*.json \| wc -l` → **31**; 4 个 fixture 目录 (`glm-smoke` / `m1-mvp` / `multi-terminal-coordination` / `phase-c-integrator-pre-merge-gate-fixtures`) + `version.yaml` ✅。`:408` 写「目录 **30** 个 `.json` + 4 个 fixture 目录 + `version.yaml`」; `:506` 写「从实测的 **31** 增到 **32**」; `:488` 写「实测 `ab-suite/` 有 **31** 个 `.json`」。承重结论 (**无 `audit-engine.json`**) 本席实读**成立** ✅ | `:408` 的 `30` → `31` |
| **SSP-m2** | minor | line-ref-off-by-two | 非目标 `:468` · follow-up #1 `:487` | 悬空函数名引用实际在 `fetch_gate.py:21`, 引作 `:23`; `:23` 是**另一条** provenance 项 | `git -C aria show d50f9c3:skills/phase-d-closer/scripts/fetch_gate.py \| grep -n 'sync.py\|_resolve_default_branch'` → `21:    state-scanner sync.py::_resolve_default_branch (module-private, other skill).` / `49:` / `108:` / `111:` / `217:`。`:23` = `state-scanner git.py — but the original locks \`\`@{upstream}\`\`; 切口1 needs` (ahead/behind 那条)。同句的另一半 `:111` **准确** ✅; 「`sync.py` 在 `d50f9c3` 上 8 个顶层 def 中无该函数」本席实核 **8 个 def, 无该名** ✅; `_ORIGIN_HEAD_REFS:46` ✅ | 两处 `:23` → `:21` |

**探针 Spec 经本轮实读确认成立 (下轮免重复)** —— 本席**独立全量重算**, 非核对其表格:

1. **SC-18 三臂在 `cc1bdef` 147 篇语料上逐格复现**: (a) 行首 `> ` → `no_field` **133** / `url_fallback` **13** / `no_token_no_url` **1**, 3 簇, **不含** `a1-entry-claim-duplicate-work-guard`; (b) 宽松 → `url_fallback` **14**, `#122` 簇**含**母 Spec (**假阳性复现**); (c) 头部区 → `url_fallback` **10**, 簇**只剩 1 个** (`#95`/`#122` 两真簇被误杀)。**九个数字一个不差**;
2. **三个同 key 簇的 6 份路径逐条正确**, 且 `changes/` 下 0 份;
3. **canonical 合规 = 0 行** (`:134`) 复现 ✅; `normalize_linked_issue("无")` → `None` ✅;
4. **10 处语料字段行逐字命中** (6 条「第一个 code span 抽错」实例 + SC-7 的 `:6`/`:22` + SC-4 的 `linked-issue-normalization:6` 裸 `无` + 长头部 `:61`/`:45`);
5. **本机 git 事实全中**: `git remote` = github/origin · `refs/remotes/` 三名含 `probe` 且 `git config --get remote.probe.url` 空 exit 1 · `refs/aria/*` 恰 3 条 (`coord-check`/`coordination`/`coordination-remote`) · `git version 2.39.5` · `symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/master` exit 0 · `refs/remotes/github/HEAD` → **exit 128**;
6. **aria 代码/文档引用全中**: `multi_remote.py:255-286` (含 `:285` auto-discover 注释) · `fetch_gate.py` `:50-54`/`:55`/`:86-101`(含 `Raw stderr is intentionally never returned` 逐字 + 5 值枚举)/`:108-128`/`:111-112`(逐字 `no cross-skill runtime import`)/`:124-127` · `remote_refresh.py:691`/`:568` · `scan.py:312` · `handoff_multibranch.py:589-598` (`soft_error`+`log.warning`+逐字消息) · `run_all_tests.sh` `:48`/`:50`/`:71` · `audit-engine/SKILL.md` `:83`/`:85` · `execution-modes.md` `:84`/`:113` · `report-format.md:50-71` · `DEFAULTS.json:124-128` (`level_3: challenge`) · audit-engine **8 文件, 确无 `scripts/`/`tests/`**;
7. **三个 issue 标题逐字命中** (`#150` / `#135` / `#157`), `ab-suite/audit-engine.json` **确不存在**;
8. **`AB_TEST_OPERATIONS.md:76`「Skill eval suites \| 28 个 \| ✅ 全量覆盖」逐字属实** ⇒ follow-up #2 的「三方互不一致 + 假绿标注」成立;
9. **`state_scanner.handoff_multibranch.max_branches` 确为真实旋钮** (`state-snapshot-schema.md:1125` + `CHANGELOG:1104/1107`), P10 的「作用域不匹配」论证前提成立;
10. **审计轨 §1 的 #1–#28 齐全**, 正文引用的 #1..#28 子集**无一指空**。

---

## 三、主控两个流程判断的独立裁定 (**不因是主控做的就默认成立**)

### 判断 ① 三份实读清单切出审计轨 — **方向成立, 执行有一处实缺陷**

- **成立的部分**: memory `audit-trail-not-in-spec` 的处方逐字就是「**切开不重写**」, 且 owner 2026-08-07 对姊妹 Spec 有同类裁定; 母 Spec 头部四条不同步声明齐全、并给了可复核命令; 交叉引用 `见清单 #N` 三份**实测全部指得到**; §1/§2/§3/§4 的搬运本席用**连续块**断言核过 (§1 25 行连续命中审计轨 `:31`)。
- **不成立的部分 (= M-M1)**: 「按字节搬运, 未重写任何一句」**对 §5 是假的** —— 表在同一 commit 内被整表重生成 (22/29 行与唯一已提交前身不同 + 新增 17 行)。这**恰好销毁了这条流程判断的安全性论证**: 「无损搬运 ⇒ 撤回成本低 ⇒ 值得先做后复议」只有在搬运可被独立核验时才成立; 现在 diff 里「搬」和「重写」不可分离, 正是 memory `rewrite-discards-fixes`「整体重写使已付出的修复静默归零且无机制发红」的入口。
- **本席建议 owner**: **采纳切分**, 但要求执笔侧先执行 M-M1 的处方 (分节陈述哪几节是搬运、哪一节是重生成)。**并追加一条**: 两份**新建**子 Spec 的审计轨头部同样写着「按字节搬运, 未重写任何一句」, 而它们的 proposal 从无已提交前身 ⇒ 该句在两子 Spec 上**结构性不可证伪**, 应改为「本文件内容由起草席直接落盘, 未经 proposal 中转」。

### 判断 ② 判定字段 spec 的 `GRANDFATHERED` allowlist 可接受 — **不成立 (见 LIFA-C1)**

- **设计形状本身全部正确**: fail-CLOSED (封闭白名单 + 其余阻断, memory `feedback_invariant_needs_failclosed_default`) ✅ · 粒度恰等于情形集 (6 条具名, memory `knob-granularity`) ✅ · **换量不调阈值** (被测量从「有几份缺字段」换成「有没有名单外的份缺字段」, memory `redfix-change-quantity`) ✅ · 陈旧条目守卫三子情形 = 漂移护栏 (memory `feedback_validator_repo_drift_guard_test`) ✅ · 拒绝跨轨回填 (memory `sync≠push-auth`) ✅ · 与回填方案严格包含、不排除 owner 选 O-1 ✅。
- **不可接受的原因**: 它与**同一份 Spec 的 round-2 宿主改判 (D3)** 相撞 —— 白名单是 **Aria 专属数据**, 却被放进 **plugin 分发件**。任何采用方注册后陈旧守卫 (a) 对 6 条全命中 ⇒ **exit 1 恒红**, 而 D3 理由 1 的立论恰恰是「这是**每个采用方都要的**通用检查」。这是 memory `fixes-contradict` 的典型形状 (「每条单独看都对, 但 A 违反 B 的隐含前提」), 也是 memory `feedback_false_green_dual_is_permanent_red` 换个仓复现。
- **本席建议 owner**: 判 **allowlist 机制可接受、当前落法不可接受**, 按 LIFA-C1 处方 (a) 把**名单数据移出分发件**后再定。O-1 (是否授权回填 6 份) 与本条正交, 可独立裁。

---

## 四、scope_ok

| Spec | scope_ok | 依据 |
|---|---|---|
| 母 | **true** | 变更面严格落在 owner 2026-08-23「方向 b 缩 scope」裁定内 (§1/§4 迁出, 主体只留 A.1 认领 + track-id 契约); C-B/C-C 在此解是 owner 点名; 新表面 7 条已逐条声明 |
| lifa | **true** | 承接 C-A/M-10/M-2 + FIX-06/07/08 + 旧 SC-13, 与母 Spec `:92` 的迁出清单**逐项对得上**; 三仓写入面已声明 |
| sibling | **true** | 承接 M-1/M-5/M-6(audit-engine 半)/M-17(§4 stdout) + FIX-10 + 旧 SC-16/17/18/19, 与母 Spec `:383` 迁出清单**逐项对得上**; SC-19(b) 两侧一致地留在母 Spec (母 `:548` → SC-29) —— **无条款落在接缝之间** |

**迁出 ≠ 丢弃的核对结果**: 母 Spec `:708` 存疑 #6 要求 R3 跨三份联审「迁出项是否真被接住」。本席逐项核: C-A → lifa §3 E0–E6 ✅ · M-10 → lifa §4 宿主 ✅ · M-2 → lifa §1 SOT 表 + Impact `standards/…/proposal-minimal.md` 行 ✅ · FIX-06 → lifa §Why 重测 ✅ · FIX-07 → lifa D5+D6 ✅ · FIX-08 → lifa E4 (逐字「消解母 Spec 旧文本里第 4/5 条互斥, editlist FIX-08(2)」) ✅ · M-1 → sibling §3 ✅ · M-5a/b → sibling §4/§10 ✅ · M-6(audit-engine 档) → sibling rule6_note ✅ · M-17(§4 stdout) → sibling §7 ✅ · FIX-10 → sibling 层 1.5 ✅。**零丢弃。**

---

## 五、本席未能核实的部分 (诚实声明)

1. **审计轨 §5 与「搬运前的工作树中间态」是否逐字节一致** —— 该中间态从未提交, 无任何可核对产物; 本席只能证明它**与唯一已提交前身 `2ae012f` 不同** (M-M1);
2. **`.aria/spikes/2026-08-02-S3-track-id-derivation.md:72`** —— 母 Spec 存疑 #1 已声明未实读; 本席亦未读 (其**结论** `identity.py:242` = hostname 兜底, 本席已独立实读确认 ✅);
3. **`phase-a-planner/SKILL.md` 内部委派动作 / skip 条件的行号** —— 母 Spec 存疑 #3 已声明不写, 本席未代补;
4. **S1/S2/S4/S6 的一次性历史测量** (事故窗 48–72h / fetch ~13.8s / 入口覆盖 9 vs 2) —— 非可重复 grep 的代码事实, 未复跑;
5. **`.aria/state-checks.yaml` 的 minimal YAML parser 对未知键的行为** —— lifa 新表面 #6 已声明未验, 本席亦未跑 (其结论「只用既有 7 键」本席核过第 11 条 check 后**仍成立** ✅);
6. **`${CLAUDE_PLUGIN_ROOT}` 是否被导出到 Phase 1.11 check 子进程** —— lifa `:281` 已升格为 A.2 验收项; 本席只核到「现有 11 条 check 零使用该变量」✅。

---

## 六、一句话结论

**母 Spec 的事实纪律本轮达标** —— 约 60 处 `文件:行号` 逐行实读全部内容属实、两段 owner 裁定 `diff` 逐字节相同、两条「实跑复现」在 `d50f9c3` 上重跑输出一致、(iii) 四落点全撤、R2 的 1C/15M 已 **closed 至 0C/1M**, 唯一 Major 是「按字节搬运」这句对审计轨 §5 不成立 (**R3: PASS_WITH_WARNINGS**);
**探针子 Spec 的实证质量是三份里最高的** —— SC-18 三臂九个数字本席独立全量重算一个不差、10 处语料行逐字命中、本机 git 事实与 issue 标题全中, 唯一 Major 是「新表面 #6/#7」还停在修复前的自述 (**R1: PASS_WITH_WARNINGS**);
**字段子 Spec 有一条 Critical** —— D3 把宿主改判到 plugin 分发面后, D6 的 Aria 专属硬编码 `GRANDFATHERED` 未随之改, 使这条 check 对**每一个采用方恒红**, 而 §1 自述「残余缺口只剩注册那一步」因此不成立; 另有两条 Major 是同一根因的两个面 —— **对被审 commit 之外的树状态做的测量没有回刷** (`母 Spec :88` 实例已随 §1 迁出而消失 / `state-checks.yaml` 10→11 被本 session 前一个 commit 改写) (**R1: REVISE**)。
⇒ **combined verdict: REVISE**, 阻塞点**仅在 `linked-issue-field-availability`**; 母 Spec 与探针 Spec 的问题都是一句话级别的自述订正, 不需要重开设计。
