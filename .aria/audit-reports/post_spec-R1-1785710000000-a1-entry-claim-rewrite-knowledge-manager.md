# post_spec R1 (重写 v2) — knowledge-manager

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=2 minor=1
**审计对象**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` @ `c6aa29a` (工作树无未提交差异)

---

## 指针核实表

> 全部逐条实读/实跑; 命令与输出见各行「实测」列。

### 1. §Why 实测表

| 声称 | 位置 | 实测命令/方法 | 结果 | 判定 |
|---|---|---|---|---|
| `phase-a-planner` 零调用 phase1_gate | proposal.md:40 | `grep -n "phase1_gate\|linked-issue\|linked_issue" aria/skills/phase-a-planner/SKILL.md` | 零命中 | ✅ 属实 |
| `phase-b-developer` :88-93 = Phase B 入口 claim | proposal.md:41 | `sed -n '80,100p' aria/skills/phase-b-developer/SKILL.md` | 88行`if_missing:`~93行`goal直驱...`, 中含 90-92 行完整 `phase1_gate.py --raw-track-id ... --phase B --mode advisory [--linked-issue ...]` 调用 | ✅ 行号精确匹配 |
| `branch-manager` :149 = Phase B 入口 claim | proposal.md:41 | `sed -n '140,158p' aria/skills/branch-manager/SKILL.md` | 149行原文即 `` `phase1_gate.py --raw-track-id <carry-id> --phase B --mode advisory` `` | ✅ 行号精确匹配 |
| ref 实测: 竞品轨 `07-27T11:53:12Z` 认领, 在其 4 轮 post_spec **之后** | proposal.md:43 | `git ls-tree -r refs/aria/coordination --name-only` 定位 → `git grep "2026-07-27T11:53:12" $(git rev-parse refs/aria/coordination)` | 命中 `claims/bfe8285d/s-6cd0@1153.yaml:1:claimed_at: '2026-07-27T11:53:12Z'`；R1 tech-lead 报告 (`...-tech-lead.md:150-155`) 交叉证实该 claim 携带 `--phase B --linked-issue aria-plugin#122`,晚于该轨自己 4 轮 post_spec | ✅ 属实, 直接在真实 git ref 中核验到, 非转引 |

### 2. 代码/文档行号引用

| 声称 | 位置 | 实读结果 | 判定 |
|---|---|---|---|
| `collision.py:210` 的 `_TERMINAL` skip done/abandoned/**yielded** | §2.4 | 实读 210 行: `_TERMINAL = ("done", "abandoned", "unknown")` | ⚠️ **行号对, 内容不对** — 见 Finding F3 |
| `collision.py:219-220` 明写 `if c.track_id == own_track_id: continue` | §2.1 脚注 | 实读 219: `if c.track_id == own_track_id:` / 220: `continue  # same-name collision — reconcile's job, not ours` | ✅ 逐字匹配 |
| `claim_lifecycle.py:425` = `release_claim_by_track` 只匹配自己 container | §2.3 | 实读 425 行: `if rec.container == resolved.container_id` | ✅ 精确匹配 |
| `phase1_gate.py:1232` = `_main()` 现有调用处 | §2.4 | 实读 1232 行: `out["linked_issue_overlap"] = linked_issue_overlaps(` | ✅ 精确匹配 |
| `phase1_gate.py:210` = `GateResult.error` docstring 预留 `fetch_degraded` 但从未赋值 | §2.5 | 实读 210 行: `Possible values: "not_a_git_repo", "identity_error", "fetch_degraded",`；并追踪 `_run_gate_impl` 全函数体确认 Step 4 fetch 降级分支 (468-482 行) 只 `logger.warning`, 未设置任何返回路径的 `error="fetch_degraded"` | ✅ 双重确认(字面 + 语义): token 存在且确实从未被赋值 |
| `audit-engine/SKILL.md:85` 明写 Step 0 是「Round 1 启动前一次性」 | §4 | 实读 85 行: "入口逻辑完成后、**Round 1 启动前一次性**执行: 固化本次审计的原始目的 anchor。" | ✅ 逐字匹配 |
| `execution-modes.md` Convergence `:84-111` / Challenge `:113-144` | §4 | `sed -n '80,150p'` 逐行计数: 84行=`## Convergence 模式`标题, 111行=该 Round N 代码块收尾```` ``` ````; 113行=`## Challenge 模式`标题, 144行=文件最后一行 | ✅ 两段边界均精确 (Challenge 段止于文件末行) |
| `DEFAULTS.json:124-128` 的 `adaptive_rules.level_3 → challenge` | §4 | 实读 124-128 行: `"adaptive_rules": {` … `"level_3": "challenge"` … `},` | ✅ 精确匹配 |
| `spec-drafter/SKILL.md:9` `user-invocable: true` | §3 | 实读 9 行: `user-invocable: true` | ✅ 精确匹配 |
| `handoff_multibranch.py` 已因 440 条远端分支踩坑并做 scan cap | §4 | `grep -n "440"` 命中该文件 108-112 行注释 "Large repos (e.g. 440 remote branches)…"；并交叉查 `aria/CHANGELOG.md:965` "实证第三方仓 440" + `docs/handoff/2026-06-01-...-71-72-spec.md:35` "440 大仓实证" | ✅ 属实, 440 是真实历史实证数字 (非虚构示例), scan cap 机制 (`resolve_max_branches_scanned` + `soft_error`) 确实存在且确实 `log()` 披露 |
| `layer-l-integration.md` 断言「闸门仅在 Phase B 触发」, 本 Spec 后即过时 | §Impact | 实读该文件 15 行: "**Design A 条件触发**: 闸门仅在用户确认要进入 Phase B 时调用, **不在 scan.py 内自动执行**" | ✅ 属实, Impact 表列此文件正确 |
| `identity.py` 新增直取 `uuid` 字段 accessor 的必要性 (现有 `get_container_id()` label 优先) | §2.1 | 实读 191-244 行: 222 行 `return label if label else uuid`; 214-222 行确认 label 优先分支 | ✅ 属实, 现有函数确实不能直接复用 |

### 3. 数字

| 声称 | 核算方法 | 结果 | 判定 |
|---|---|---|---|
| 141 篇 proposal 语料 | `find openspec/changes openspec/archive -mindepth 2 -maxdepth 2 -iname proposal.md \| wc -l` | **141** | ✅ 精确 |
| 13 篇有「关联 Issue」字段 (9%) | 先用严格正则 `^\s*>?\s*\*\*关联\s*Issue\*\*` → 12; 因格式变体 (`interactive-session-dedup-coordination/proposal.md:220` 用 `- 关联 Issue:` 而非 `**关联 Issue**:`) 手工复核后 12+1=**13**；另 2 处广义命中 (`state-scanner-issue-awareness` 正文提"关联 Issue"概念、本 Spec 自身正文引用该词) 经读取确认是**正文提及**而非字段, 剔除 | **13** (含 1 处格式变体, 需人工复核才能对齐) | ✅ 最终精确, 但**朴素 grep 拿不到该数字**, 提醒: 该数字对格式高度敏感 |
| 128 篇不回填 (141-13) | 算术 | 141-13=128 | ✅ 算术正确 |
| 9 种 owner-container / 2 个容器 | `grep -rhoE "^owner-container:\s*\S+" docs/handoff/*.md \| sort -u \| wc -l` = 9; `git ls-tree -r refs/aria/coordination --name-only \| grep -oE "^claims/[^/]+" \| sort -u` = 2 (`023236f2`,`bfe8285d`) | **9 vs 2** | ✅ 精确匹配 (注: 9 值中另含 `f9c6e8cd` 一个从未出现在 claim ref 里的第三 uuid, 支持"至少 7 种从未留下 claim"的下界成立) |
| 13.8s fetch 均值 | (12.5+13.4+14.1+15.9+13.0)/5 | 13.78 ≈ 13.8 | ✅ 算术正确 |
| 16⁸ ≈ 4.3e9 碰撞域 | 16^8 = 4,294,967,296 | 4.29×10⁹ | ✅ 正确 |
| SC 数量演进 7→15→19 | `git show <sha>:proposal.md \| grep` 三个提交点 (`552ec5a` 原始 / `efca1d5` R1-fix / `23f34a6` R2-fix) 逐一读 Success Criteria 表 | 原始表 SC-1~SC-7 (**7**, 非加粗格式) → efca1d5 加粗格式行数 **15** → 23f34a6 **19** → 当前 HEAD 仍 **19** (SC-1~19 连续无缺号) | ✅ 精确 (原始提交用非加粗 `\| SC-1 \|` 格式, 朴素同正则会误判为 0, 需读表内容核实) |

### 4. spike 全部到位 + 审计轨迹表

| 声称 | 核实 | 判定 |
|---|---|---|
| S1-S6 六条 spike 全部完成 | `.aria/spikes/2026-08-02-S1-heartbeat-feasibility.md` / `-S2-S4-S5-S6-batch.md` / `-S3-track-id-derivation.md` 三文件覆盖 S1/S2/S3/S4/S5/S6 六个编号, 逐份读完 | ✅ 属实 |
| R1(5席) 4C/8M/7m | `post_spec-R1-...-aggregated.md` frontmatter 外加正文 "去重后 4 个 critical 簇" / "Major 簇(去重后 8 条)" / "Minor (7 条" | ✅ 精确 |
| R2(新眼睛) 2C/4M/4m, 两条critical都在R1-fix自己逻辑上 | `post_spec-R2-...-aggregated.md` frontmatter `critical=2 major=4 minor=4`；正文标题 "两条 critical 都落在 R1-fix 自己新写的逻辑上" | ✅ 精确, 转述未夸大未削弱 |
| R3(第三双新眼睛) 2C/6M/3m, 判不收敛 | `post_spec-R3-...-aggregated.md` frontmatter `critical=2 major=6 minor=3`; 正文 "R2→R3 是唯一同口径的相邻两轮: critical 2→2 持平, major 4→6 上升" + "未收敛" | ✅ 精确 |
| 前置依赖 `linked-issue-normalization` 真的承载 basename 归一 (含 S5 追加 ./_→-) | 全文读 `openspec/changes/linked-issue-normalization/proposal.md` | 该 Spec §What Changes 第 3 点确有 "⭐ `repo_basename` 内的 `.` 与 `_` 一律译为 `-` (spike S5 追加)" 且给出 SC-5b 断言 | ✅ 依赖真实存在, 非空引用 |

**5. memory 引用**: 全文 `grep -n "memory" proposal.md` **零命中** — 本 Spec 正文不直接引用任何 `MEMORY.md` fact file (与 R1 原版不同), 故本项无对象可核, 非缺陷。

---

## spike 转述保真度表 (本轮核心)

| Spike | Spec 转述 (位置) | Spike 原文 (位置) | 保真度判定 |
|---|---|---|---|
| **S1** 保护窗 | "事故窗实测 48–72h" + "heartbeat 匹配键改 `(container_id, normalized track_id)`, 刷新全部匹配 active claim" (§2.2) | §1 "事故窗 (母 Spec §3a): 第 4 次 ~48h / 第 5 次 ~72h" (该数字**本身**是 spike 从「母 Spec §3a」承接的既有断言, 非 S1 自己新测); §5 结论 1 逐字对应刷新键与"全部匹配" | ⚠️ **轻微弱化未标注**: 提案用「实测」二字统称, 但 48h/72h 这对数字是 spike **承接**的既有前提, 并非 S1 本轮新测量得出 (S1 本轮新测的是"生产 claim 计数 7+20 条"与"release_claim_by_track 先例"这两件事)。不影响 §2.2 的技术结论(可行性判断成立), 但"实测"用词对这两个数字略有过度授权 |
| **S1** 冗余再认领 | "冗余: 每次调 phase1_gate 都写一条新 claim (生产 ref 实证 27+ 条)" (§2.2) | §4 "生产 ref 实证: `claims/023236f2/` → 7 条 / `claims/bfe8285d/` → 20+ 条" | ✅ 7+20=27, "27+" 用词精确对应(20+ 是下界, 故 27 也只能是下界) |
| **S2** 探针 fetch 代价 | "双远端 fetch ×5 12.5/13.4/14.1/15.9/13.0s(均值~13.8s); 3 轮审计净增~41s; 瞬时失败2次SSH,重试恢复" (§4) | 数值表逐字一致; "本 Spec 自己经历的 3 轮则是 ~41s" 逐字一致; "github 出现过 2 次瞬时 SSH 失败(kex_exchange_identification), 重试即恢复" | ✅ 忠实转述, 无夸大无弱化 (省略了具体错误名 kex_exchange_identification, 对结论无影响) |
| **S3** track-id 派生 | "`<归一后 basename>-<str(int(number))>-<container_uuid>`" + "接手不是一键动作...无任何函数支持释放别的容器的 claim" (§2.1, §2.3) | §3 派生规则逐字一致; §4 "grep 复核: 无任何函数支持释放别的容器的 claim" 逐字一致 | ✅ 忠实转述 |
| **S3 内部瑕疵** (未传导入 proposal) | — | spike 原文 "`identity.py:222` 是 `return label if label else uuid`, `:244` 是 hostname 兜底" — **实读 identity.py:244 为 `return uuid`(全新生成分支的返回, 非 hostname), 真正的 hostname 兜底在 :242 (`return _hostname()`)** | ⚠️ **spike 自身行号引用有 2 行误差**; 但 proposal.md 正文对 identity.py 未引用具体行号(只泛称"hostname 兜底分支"), 该误差**未传导**进当前受审文档。留痕供未来引用者避免沿用错误行号 |
| **S4** basename 别名 | "全文 19 vs 802(比例是反的); 在真正会被传给 `--linked-issue` 的总体里别名实例=0" (§Why 表) + "141篇仅13篇有该字段—9%" (⭐段) | §S4 "openspec/ 全文任意上下文: 19 / 802"; "「关联 Issue」字段值内: 0 / 0"; "语料总数 141 篇…有该字段 13 篇=9%" | ✅ 忠实且强化正确: "比例是反的"准确刻画了 R2 原判断(24 vs 10, aria-orch更多)与实测(19 vs 802, aria-orchestrator远多)方向相反,不是单纯"数字对不上" |
| **S5** 分隔符碰撞 | "10CG/10cg.local 是真实仓(Forgejo API实测,11 open issues,handoff引用过)⇒活跃,非dormant" (§Why 表) | §S5 "Forgejo API 实测 `full_name: 10CG/10cg.local`, 11 个 open issue, 且本项目 handoff 里引用过它(`10cg.local #20`)" | ✅ 忠实转述; 独立抽查 `grep -rn "10cg.local" docs/handoff/` 亦命中 #20 引用, 交叉印证 spike 本身没有编造 |
| **S6** 入口覆盖率 | "coordination ref 里 2 个容器, 而 handoff 的 owner-container 出现过 9 种 ⇒ 至少 7 种从未留下 claim" (§3) | §S6 "coordination ref 里 2 个容器; 而 handoff 的 owner-container 出现过 9 种…⇒至少 7 种身份从未在 ref 里留下 claim" | ✅ 忠实转述, 且本报告独立复算 9/2 两数均命中(见上表) |

**结论**: 六条 spike 的核心技术结论在 proposal.md 正文中转述**忠实, 无实质性加强/削弱/曲解**。发现的两处瑕疵都很轻: (a) S1 的"48-72h 实测"措辞对承接自旧稿的前提用词略满; (b) S3 spike 自身一处行号误差(`:244`)未传导入当前受审文档。两者均不构成本轮 Finding, 仅供记录。

---

## Findings

### [CRITICAL] F1 — track-id 加容器段后, A.1 claim 与 Phase B/D.2b 之间的释放链断裂; 与 DEC-20260519-001「track-id 是脊柱」不变量未对齐

- **位置**: proposal.md §2.1(D3, 90-103行) + §5(174-180行) + 非目标"不动 Phase B 入口现有认领"(272行) vs `docs/decisions/DEC-20260519-001-multi-terminal-coordination.md:43` + `aria/skills/phase-b-developer/SKILL.md:92` + `aria/skills/branch-manager/SKILL.md:149`
- **问题**: 三个既定事实拼在一起产生矛盾:
  1. DEC-20260519-001 (Layer L 协调系统的建仓决策记录) 明文: "**track-id 是脊柱: 1:1 绑分支恒成立**"(:43) — 这是 reconcile / track board collision 分组能够跨容器识别"同一份工作"的根本前提。
  2. 本 Spec §2.1 把 A.1 的 track-id 定义为 `<basename>-<number>-<container_uuid>` — 同一个 issue 在**不同容器**手上会派生出**不同**的 track-id (这正是本 Spec 为解决 R2/C1 而刻意设计的行为)。
  3. 本 Spec 明确"不动 Phase B 入口现有认领"、"逐字节不变"(非目标, 272行) — 而 `phase-b-developer:92` / `branch-manager:149` 现有 `--raw-track-id` 用的是**不含容器段**的 "`<本 cycle carry-id/Spec id>`" / "`<carry-id>`"。
  - ⇒ 同一份工作在 A.1 与 Phase B 会派生出**两个不同**的 track-id, `derive_track_id()` 各自归一后仍是两个不同字符串。
- **§5 自身的矛盾**: §5「D.2b 对偶」一行断言"只有走完循环的轨才到 D.2b"暗示 D.2b 的 `release_claim_by_track`(按 `(container, track_id)` 定位)能在周期完成时把 A.1 claim 一并关闭。但 `release_claim_by_track` 用的 `track_id` 是**调用现场**传入并 `derive_track_id()` 归一后的值——D.2b 现场传入的必然是 Phase B/D 沿用至今的**不含容器段**的 track-id, 与 A.1 当初写入的**含容器段**的 track-id 是两个不同字符串, **匹配不上**。⇒ A.1 claim **不会**被 D.2b 释放, 只能等 `SWEEP_TTL`(24h, 或被本 Spec §2.2 的 heartbeat-by-track 意外续期)才消亡——而这恰是走完整个「成功」路径(不放弃、不改名)的**最常见**情形, 不是边角案例。
- **危害**: 每一条**成功**从 A.1 走到 Phase B 的 track, 都会在 coordination ref 里留下一条 A.1 阶段的孤儿 active claim, 且不落在本 Spec §5 枚举的任何一条"新退出路径"里(探索性放弃/slug改名/D.2b 都不覆盖这个最常见的 happy path)。这与本 Spec §Why 反复强调的"机制要经得起最常见路径检验"精神直接相悖, 且没有被 R1/R2/R3/S1/S3 中任何一份文档提及或反驳 (`grep -ln "DEC-20260519\|脊柱\|DEC-20260704" .aria/audit-reports/post_spec-R*-a1-entry-claim*.md .aria/spikes/2026-08-02-*.md openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 零命中)。
- **建议修法** (与危害方向一致): 本 Spec 进 A.2 前必须显式设计 A.1→B 的 track-id 过渡, 二选一并写清楚: (a) 在 A.1→B.0 的衔接点补一步"release 旧(含容器段) + 复用/acquire 新(不含容器段)"(仿 §5 已有的 slug 改名两步模式), 并把这一步补进 §5 表格与 SC; 或 (b) 重新评估是否真的需要把容器段并入**持久化的** track_id 字段——例如让"同 issue、不同容器"在 A.1 阶段直接复用 Phase B 既有的、不含容器段的 track-id, 依赖**已经在跑的** reconcile "occupied/cross_owner" 告警通路(而非新增的 `linked_issue_overlap`)去捕获碰撞, 把容器辨识度需求限定在**调用参数/session 层**而非 track_id 本身。两条路径任选其一都需要与 DEC-20260519-001 的"脊柱"表述做一次显式对账并在决策记录里留痕(修订或注记豁免), 不能silent绕过。

### [CRITICAL] F2 — `--include-terminal` 的"三段传递链"漏了必要的第 0 段: `collision.py::linked_issue_overlaps()` 签名/逻辑变更; Impact 表零覆盖 `lib/collision.py`

- **位置**: proposal.md §2.4(129-135行) + Impact 表(281-294行) vs `aria/skills/state-scanner/lib/collision.py:177-181`
- **问题**: §2.4 描述接线为"三段缺一不可": (1) CLI flag; (2) `_main()` 现有调用处(`:1232`)加关键字参数; (3) A.1 调用模板显式带该 flag。但实读 `linked_issue_overlaps(claims, own_track_id, own_linked_issue)` 的当前签名(177-181行) **不含 `include_terminal` 形参、也无 `**kwargs`**,其内部 `_TERMINAL` 过滤(210行定义、213-214行使用)完全在函数体内部完成, 调用方**无法从外部**改变这个判定。若真的只按"三段"字面实现——只在 `_main():1232` 加一个关键字参数而不改 `linked_issue_overlaps` 本身——Python 会在该行**直接抛 `TypeError: linked_issue_overlaps() got an unexpected keyword argument 'include_terminal'`**。
- **反讽对照**: 本 Spec §2.4 明确引用 "R3/C2" 作为"三段"结论的依据; 但 R3 aggregated 报告(`post_spec-R3-...-aggregated.md` C2 小节)给出的示范代码本身就是:
  ```python
  out["linked_issue_overlap"] = linked_issue_overlaps(
      claims, result.track_id, args.linked_issue,
      include_terminal=args.include_terminal,
  )
  ```
  ——这段代码**已经隐含**了 `linked_issue_overlaps` 需要新增 `include_terminal` 形参。本轮重写忠实吸收了 R3/C2「不碰 `run_gate`/`_run_gate_impl` 签名」的结论,却把同一段代码里隐含的「`collision.py` 需要新增形参」这一必要前提遗漏了——Impact 表因此对**本 Spec 唯一定义`_TERMINAL`常量的文件**反而空白。
- **危害**: Phase B 实现者若只照 Impact 表清单动工, 会漏掉这个文件; 照抄"三段"清单在 `_main()` 加关键字参数会在开发早期就触发运行时报错, SC-8(CLI 全链路)会红在一个 Spec 阶段本可以说清楚的地方。
- **建议修法** (与危害方向一致): 在 Impact 表新增一行 `skills/state-scanner/lib/collision.py`, 变更为"`linked_issue_overlaps()` 新增 `include_terminal: bool = False` 形参, 为真时调整 `_TERMINAL` 的应用范围(具体排除哪些状态还需回答 Finding F3)"; 并把"三段"改写为"四段", 新增段 0 置于最前。

### [MAJOR] F3 — `_TERMINAL` 现状是 `{done, abandoned, unknown}`, 不是提案陈述的 `{done, abandoned, yielded}`; "yielded" 今天已经可见, "unknown" 未被讨论

- **位置**: proposal.md §2.4(126-127行, 244行 SC-8) vs `collision.py:210` + `claim_schema.py:56-59` + `release_gate.py:219`
- **问题**: §2.4 原文"`done` / `abandoned` / `yielded` 的同 issue claim 必须可见…`collision.py:210` 的 `_TERMINAL` 会直接 skip 它们"。实读 210 行: `_TERMINAL = ("done", "abandoned", "unknown")` ——被排除的第三态是 **`unknown`**, 不是 **`yielded`**。交叉核实 `claim_schema.py:56-59`(`STATUS_ENUM`/`STATUS_WRITABLE` 均含 `"yielded"`)与 `release_gate.py:219`(CLI `--status` 的 `choices=["done","yielded","abandoned"]`)确认 `yielded` 是真实可写入生产的合法状态——即**一条 status=yielded 的同 issue claim, 在今天的代码里已经不会被跳过, 已经会出现在 `linked_issue_overlap` 输出里**。
- **连带影响 SC-8**: "同 issue 他轨 claim 为 `done`/`abandoned`/`yielded` 时经 CLI 可见…`_TERMINAL` skip 的现状必红"——对 `yielded` 这一分支,现状**不红**(它已经可见), "必红"对三态里的一态不成立。`grep -n "linked_issue_overlaps\|_TERMINAL\|yielded" aria/skills/state-scanner/tests/test_collision.py` 确认当前**零测试**覆盖这个函数的终态过滤行为, 没有安全网会提前暴露这个前提错误。
- **危害**: 实现者若照字面把 SC-8 拆成"给 yielded 也加可见性逻辑", 会做无用功(它已经可见)且可能因为改动 `_TERMINAL` 的方式不当反而影响到目前完全没被讨论过的 `unknown` 语义(它是 schema 层"读不懂"的哨兵值, 与"任务终态"是两个维度的概念,是否也要在 `include_terminal=True` 时放行需要独立决策, 当前提案完全没有触及)。
- **建议修法** (与危害方向一致): 重新按 `{done, abandoned, unknown, yielded}` 四态(而非预设的三态)逐一核实现状与目标行为, SC-8 拆分或至少加注"`yielded` 现状已可见, 本 Spec 只需新增 `done`/`abandoned`的可见性"; 并在设计 `include_terminal` 参数时显式决定 `unknown` 在 `include_terminal=True` 时是否仍应保持过滤(建议保持过滤, 因为它不代表真实的任务终态)。

### [MAJOR] F4 — 文档同步面遗漏: `session-handoff.md`(track_id.py 自称的 SOT) 与 `coordination-ref-schema.md`(claim 结构 SOT) 均未入 Impact 表

- **位置**: proposal.md Impact 表(281-294行) vs `standards/conventions/session-handoff.md` + `aria/skills/state-scanner/docs/coordination-ref-schema.md`
- **问题**:
  1. `aria/skills/state-scanner/lib/track_id.py` 自己的模块 docstring 第一行写明 "Authority: `standards/conventions/session-handoff.md` §2.3.1"——该文档是 track-id 概念的**指定权威**。而 session-handoff.md §2.3.8 还定义了**第三个** claim 消费入口: §6 carry-id → `phase1_gate.run_gate()` 的 `raw_track_id`(`session-handoff.md:246`),与本 Spec 新增的 A.1 入口、既有的 Phase B 入口并列。本 Spec 改变了 A.1 场景下 track-id 的构造方式(加容器段), 却完全没有在 session-handoff.md 里对这第三入口的既有描述做任何同步检查或声明二者是否兼容(参见 F1——事实上并不兼容), Impact 表对该文件零覆盖。
  2. `aria/skills/state-scanner/docs/coordination-ref-schema.md` 是 claim YAML 结构的 schema 文档 (`claim_schema.py` docstring 明确引用它), 已经记录了 `status` 枚举、`track_id` 语义等字段说明。本 Spec 新增 heartbeat-by-track 变体、`linked_issue` 驱动的可见性语义变化, 均是对该 schema 文档所描述行为的实质性扩展, Impact 表同样零覆盖。
- **危害**: 与本 Spec 自己在 §Impact 表里已经正确列出 `layer-l-integration.md`(因为它会"过时")的逻辑一致——这两份文档同样会因本 Spec 实施而在**是否兼容/是否完整**上过时或不完整, 却没有被同等对待, 造成"部分同步、部分遗漏"的不一致治理, 后续读者(尤其是把 session-handoff.md 当权威来源的其他 Skill 作者)会依据过时描述做出与本 Spec 冲突的假设。
- **建议修法** (与危害方向一致): Impact 表补两行: `standards/conventions/session-handoff.md`(§2.3.8 补充"A.1 阶段可能出现的第三种 track-id 构造形态及其与 carry-id 消费路径的关系"或明确注记二者不统一的后果, 与 F1 的裁决联动) 与 `aria/skills/state-scanner/docs/coordination-ref-schema.md`(补 heartbeat-by-track 与 `linked_issue` 可见性语义)。

### [MINOR] F5 — 自举缺口: 本 Spec 要求「关联 Issue」无值时必须显式写「无」, 但本 Spec 自己的 proposal.md 从未携带该字段

- **位置**: proposal.md 全文头部(1-17行) vs 本 Spec §1.1(70行)自定的规则
- **问题**: §1.1 规定"无关联时显式写 `无`, 不留空——空与「忘了写」不可区分"。`grep -n "关联" openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 的全部命中都是正文讨论该概念的散句, 本文档头部**没有任何一行**是 `> **关联 Issue**: ...` 格式的字段(无论是具体 issue 还是显式的"无")。对照其前置依赖 `linked-issue-normalization/proposal.md` 头部第 6 行明确写着 "`> **关联 Issue**: 无 (由 ... 发现...)`"——同一天由同一流程产出的姊妹 Spec 做到了, 本 Spec 自己没做到。
- **危害**: 低(不影响机制正确性), 但与本 Spec §Why 反复强调的"提出纪律的人自己第二天违反了它——知道也做不到"是同一形状的反例, 若不修会成为未来审计"举证本 Spec 治理有效性"时的一个显眼反证。
- **建议修法**: 在本 Spec 头部补一行 `> **关联 Issue**: 无`(或指向真实存在的、催生这条方法论修复的某个 issue 编号, 如果存在的话), 使其符合自己制定的规则。

---

## 附注 — 核实通过, 无需在 findings 中重复

- §审计与 spike 轨迹表的 R1/R2/R3 counts(4C/8M/7m, 2C/4M/4m, 2C/6M/3m)与三份 aggregated 报告逐字对齐。
- SC 数量演进 7→15→19 经三个历史提交(`552ec5a`/`efca1d5`/`23f34a6`)直接读取验证, 当前 HEAD 的 SC-1~19 连续无缺号。
- 前置依赖 `linked-issue-normalization` 的 basename 归一(含 S5 追加的 `./_→-`)真实存在于该 Spec 正文, 非空引用; 两份 Spec 的非目标/依赖声明互相吻合。
- `.aria/config.json` 的 `audit.checkpoints.post_spec = "convergence"` 与 `coordination.enabled = true` 均核实属实, "闸门待裁"一节引用准确。
- `phase1_gate.py` 全文确认不读取任何 config 文件, "skip 判断在调用方 SKILL.md 层"的框架性判断成立。
- `.aria/state-checks.yaml` 现有 `checks:` 列表 schema(name/description/command/severity/fix/timeout_seconds/enabled)与 Impact 表"新增字段校验 check"的隐含格式假设一致, 无需额外说明。
