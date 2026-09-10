---
track-id: collision-dedupe-test-clock-asymmetry
owner-container: simonfish/023236f2
phase: C
status: done
updated-at: 2026-09-10T01:12:11Z
---

# Aria — Session Handoff (2026-09-10, session-closer 会话收尾) — 五条口子全部落成机械物, 外加一个正在按日历腐烂的测试套件

> **一句话**: 上一份 handoff §2 记的「5 条我自己开的口子, 只活在文字里」**全部落成机械物**; 兑现其中「全量留证」那条时挖出一个**确定性的新缺陷** —— 一份测试文件半冻结时钟, 已经在按日历逐条变红。修复已进 master。
> **本 session 最该记住的一件事**: **我为了查这个缺陷而写的普查器, 被它自己的基线自检抓出撒谎三次** —— 第一版会给出「全套件零腐烂」的结论, 而我会采信它。三次 bug 与我要查的那个生产缺陷**是同一个形状: 半冻结**。

---

## §0 入口 (新 session 优先读)

1. **已进 master 未发版**: `aria-plugin` `f314785` (collision_dedupe 测试时钟修复) + 主仓 gitlink `c02b0ef`。owner 裁定本轮不发版 ⇒ **已发布的 v1.73.0 与采用方装的副本仍是红的**, `aria-plugin#194` 保持 open。
2. **四张新单**: `aria-plugin#194` (时钟半冻结) · `aria-plugin#195` (协调板权威 remote 无校验) · `Aria#211` (Rule #6 description 面测不到) · 外加 6 条证据评论。
3. **🔐 一次假警报 (已查实并撤销)**: 我一度报「secret rotation 逾期 38 天」—— **错的**。canonical record `.aria/decisions/2026-05-02-secret-rotation-deferred.md` §Resolution 写着 **Resolved 2026-05-22**, 4 key 已全部处置。根因是 memory fact 文件停在 05-20 快照、未跟进闭环。已修 memory + 索引; 教训见 §4.7。

---

## §1 已完成 (按时间顺序)

| # | 动作 | 产物 |
|---|---|---|
| 1 | 上一份 handoff §2 五条口子逐条实测 | 见下 |
| 2 | 口子 1「全量留证后开单」 | `aria-plugin#194` — 兑现承诺时挖出**新的确定性缺陷** |
| 3 | 口子 2「description 触发率评测」 | `Aria#211` — 先去源码核实臂确实被直接喂 SKILL.md |
| 4 | 口子 3+4「版本点 / Released 日期类级封堵」 | **并入 `Aria#177`** (comment 23105) — 未新开单 |
| 5 | 口子 5「v_old 复现命令没验证过」 | **跑了, 是错的** ⇒ commit `8d2903e` |
| 6 | 附带: skill 计数漂移 (34/41 vs 真值 35/42) | `aria-plugin#181` comment 23106 |
| 7 | #194 修复 + 2 条回归锁 + 三态负控 + 时间旅行验到 2040 | `aria` `f314785` → master, 主仓 gitlink `c02b0ef` |
| 8 | 扫除 `bfe8285d` 两条过期 claim (dry-run 先行) | 协调 ref `87147af`; 在 `Aria#195`/`#199` 留可查记录 |
| 9 | 顺带发现协调板 github 死板 (停 2026-05-24, 落后 113 commit) | `aria-plugin#195` + `Aria#165` 交叉指针 |

### 口子 1 的实况 (值得单独记)

兑现「下个 session 再见就全量留证后开单」时, `FAIL: state-scanner` **当场复现**。但把时钟冻结到 2026-09-08 实测**全绿** ⇒ **上次那个 transient 不是这个缺陷**, 它的证据确实已被 `| tail -5` 销毁, 不可恢复。我没有为它编一个解释。

今天这个是新的、确定性的: `test_handoff_multibranch_collision_dedupe.py` 给 renderer 传了 `_FIXED_NOW` (6/6 全钉) 却没给 collector 传 (**0/16 全不钉**), 夹具全是绝对日期, 撞上 `LAYER_H_ACTIVE_WINDOW_DAYS = 30`。逐日期冻结实跑的腐烂表: **09-08 全绿 → 09-09 两红 → 09-14 三红 → 09-18 五红 → 09-22 起稳定七红**。变红的 6 条里 5 条自称 negative control ⇒ 护栏本身已死。

⚠️ **开单时我把根因写反了**: 正文说「collector 没有 `now` 形参, 修它要改生产签名」—— 实际那个形参**一直都有**, 注释还逐字写着 "tests pin it", 同目录 `test_collision.py:439` 就是正确先例。已在 comment 23108 勘正。**症状与测量全对, 修复方向那段是没读源码就写的推论。**

---

## §2 未完成 / Carry-forward 清单

### 高优先级 (建议下次 session 优先评估)

- ~~`{id: secret-rotation-overdue}`~~ **已撤销 (假警报)** — owner 追问后实读 canonical record: `.aria/decisions/2026-05-02-secret-rotation-deferred.md` §Resolution **Resolved 2026-05-22** —— `FEISHU_APP_SECRET` / `FEISHU_VERIFICATION_TOKEN` / `FEISHU_ENCRYPT_KEY` 三个已轮换 (2026-05-22), `GLM_API_KEY` 经 Hermes→Luxeno 重定向**架构性退役** (2026-05-21); 原文逐字「2026-08-02 hard cap 已可撤销对应 calendar reminder」。**这条不是 carry-forward, 是我读错了。** 残留仅「`/root/.hermes/.env` 仍明文 dotenv 落盘」, 已成文在 2026-05-21 handoff §2 S7, 非本决议范畴。
- **`{id: aria-plugin-194-release, desc: "#194 修复未发版, 已发布 v1.73.0 仍红"}`** — 采用方装的副本实测同样 2 红并按同一时间表恶化。发版需动整个同步面 (见下条)。
- **`{id: aria-177-points-probe, desc: "Aria#177 建议 3 的 plugin-version POINTS 探针"}`** — 我已实测枚举 6 个版本点 + 3 个日期点贴进 #177, **未实现**。#177 原文写着「是否合并掉 `m6-version-badge-match` 的窄覆盖面请 maintainer 判」⇒ **待 owner 裁**。

### 中优先级

- **`{id: aria-211-scenario4-baseline, desc: "Aria#211 的场景 4 触发率基线未跑"}`** — 该单验收第 1 条要求先测「两个 description 的触发率区分力是否非零」; **没跑**。若区分力为零, 结论应反过来 (开单说场景 4 同样测不到), 而非把它写进 Rule #6。**这是我这个 session 新开的口子。**
- **`{id: scan-now-must-violation, desc: "lib/ 一族裸调 datetime.now 不走 scan_now 的 MUST"}`** — `_common.py::scan_now()` docstring 逐字写着「Every freshness … computation **MUST** read the current time through this single injection point」, 而 `lib/collision.py:232` / `claim_lifecycle.py:76` / `gc.py:94` / `identity.py:102` / `reconcile.py:194,367` / `scripts/lib/spec_complete.py:1500` 全是裸调。我只在 #194 comment 里点名, **没开单**。⚠️ 这条与上一份 handoff §2 的五条**同形状** (发现类级问题→写一句建议→没做)。
- **`{id: aria-plugin-195-disposition, desc: "协调板权威 remote 无校验, 单已开未处置"}`** — github 上那块 2026-05-24 的死板还在。三个方案已写进单, 未裁。
- **`{id: aria-plugin-181-count-fix, desc: "skill 计数漂移只留证未修"}`** — `aria/README.zh.md` 与 `aria/VERSION` 停在 34/41, 真值 35/42。**当前正错着。**

### 低优先级 / cleanup

- `{id: plugin-cache-currency, desc: "运行时副本 1.71.1 落后 SOT"}` — 需 owner 在终端 `/plugin marketplace update` + `/plugin update` + 重启; AI 做不了。
- `{id: pending-specs-unowned, desc: "#195/#199 两条 Spec claim 已扫, 本体仍 pending 无人推进"}`
- `{id: aria-orchestrator-dirty, desc: "他轨 feature 分支指针全程 dirty"}` — 全程未卷入, 每次提交前核过。

### 机械补漏 (backstop, AC-3b)

`cross_check_unfilled` 报 **132 项**机械有而 AI 没提, 按来源: m6-release-closeout 41 / m6-cost-model-telemetry 25 / m6-e2e-resilience 25 / m7-fleet-aggregation 20 / m7-agent-lifecycle 18 / m6-dispatch-input-delivery 3 —— **全部属他轨**, 分布与上一 session 逐项相同 (零变化)。

⚠️ **本轨机械补漏 = 0, 但这不是完整性证据**: 本轨是 Level 1, **没有 tasks.md**, 机械面结构上看不见它。上面 §2 那 9 条全部来自 AI 内省, backstop 一条都验证不了。

---

## §3 关键风险 / 已知陷阱

1. **带 deadline 的 project memory 在闭环后不会自己变绿** —— secret rotation 的 fact 文件停在 2026-05-20 amendment, 05-22 已闭环却从未回写, 索引行仍写「hard cap 2026-08-02」⇒ 本 session 据它误报逾期。已修文件 + 索引。⚠️ **同形状的还有几条?未普查** —— 没有任何机制在事情闭环时回写 memory。
2. **已发布版本是红的** —— v1.73.0 与采用方装的 1.71.1 跑 `run_all_tests.sh` 均 exit 1, 且 09-14 / 09-18 / 09-22 逐步恶化到 7 红。不发版就修不到他们。
3. **`issue_scan.limit=20` 会让查重判错** —— 本 session 实证: `Aria#165` 是 open 却不在清单里, 差点新开一张与它重叠的单。**任何基于 issue 清单的否定性判断都不可靠。**
4. **心跳不是可靠的存活信号** —— `gc.py` docstring 逐字: "no production heartbeat loop exists (heartbeat_at freezes at acquire)"。实测: 对方心跳停在 09-06T16:15, 而真实提交持续到 09-07T06:43, **心跳早停 14 小时**。判「对方停工」不能只看心跳。
5. **`latest.md` 的 track 表已陈旧** —— 表中称 M6 轨「claim 09-05 重新认领 active」, 而协调板实测该 claim 状态为 **abandoned** (`claims/bfe8285d/s-00ec@0720.yaml`, heartbeat 2026-09-05T07:20Z)。我的 sweep **没碰它**, 它早就是 abandoned。

---

## §4 实战教训 (memory 沉淀来源)

1. **半冻结**: 冻住一个状态源却漏掉同段代码读的另一个源 ⇒ 结论不可信, 且**红绿方向随机**。一天四例同形 —— #194 的生产缺陷 + 我的普查器三个版本 (补丁只生效一次 / 连 `time.time` 冻但 mtime 是真的 / 只冻生产不冻测试)。判据不是「我冻住时钟了吗」而是「**我控制了几分之几的世界**」。→ memory
2. **检查器自身必须先过基线自检**。我的普查器第一版会报「全套件零腐烂」并被我采信; 三次撒谎全是「09-08 须 0 红 ∧ 09-09 须恰为已知那 2 条」这个自检当场抓下的。**没有它, 这个 session 就是个假绿收场。**
3. **截断的清单让「没找到」变成假结论**。最刺眼的是: 同一天早些时候我刚亲手标注过「49 是下界, 两仓各撞 20 上限」, 几小时后仍据那份清单判「无重复」。**知道它截断 ≠ 用它时记得。** → memory
4. **不是所有同族问题都该并单**。同一天两个相反判定都对, 判据是「**把它塞进那张单, 那张单的现有处方需要改写吗**」: #177 的建议 3 逐字覆盖 ⇒ 并入; #165 的两条约束作用域锁在分支头+gitlink, 够不到非分支 ref ⇒ 新开 + 交叉链。→ 追记进既有 memory
5. **诊断对了不等于修复方向对了**。#194 正文把「测试冻结不了 collector」直接推成「collector 没有可冻结的入口」, 而形参一直在。开单时一眼 `sed -n '556,560p'` 就能避免。
6. **fix-the-class 一天三次**: 修 `RESULT.md` 漏了 `:8` 那个兄弟位置 (复扫抓到) / 回归锁的 docstring 差点写进一个会被它自己扫成违规的字面量 (收尾断言抓到) / 普查器的一次性补丁守卫 (基线自检抓到)。**三次都是自己设的核验网兜住的, 没有一次是靠想起来。**

7. **带 deadline 的 memory 在闭环后不会自己变绿**。我据 memory 报「secret rotation 逾期 38 天」, owner 追问后实读 canonical record —— **2026-05-22 就 Resolved 了**, 原文还逐字写着「hard cap 已可撤销对应 calendar reminder」。**判据: 任何带 deadline / status 的 project memory, 据它下结论前必须去 canonical record 核当前 status。** 这与 §4.3「截断清单」同族 —— 都是**拿一份不新鲜/不完整的东西当权威**, 而两次都发生在同一个 session 里。

[候选 memory]
- 半冻结使结论不可信且方向随机, 检查器自身先过基线自检 — type: feedback ✅ 已写
- 截断清单上的「没找到」是零信息 — type: feedback ✅ 已写
- 同族但作用域够不到 ⇒ 新开单而非并单 — type: feedback ✅ 已追记进 `feedback_ai_narrows_owner_decision_space`

[未写下经验]
- 「心跳不是存活信号」目前只写在本 handoff §3.4 与两条 issue 评论里, **未落 memory** (判断: 强绑本仓当前实现, 待 `aria-plugin#180` 修好后语义会变, 现在固化可能很快过期)。

---

## §5 多维度同步状态 (Aria 4 维度)

| 维 | 状态 |
|---|---|
| UPM | present; cycle=null (未配置) |
| OpenSpec | 活跃 8 (approved 6 / pending 2) · 归档 145 · **待归档 0** ✅ · design_deferred 5 (最陈旧 m6-release-closeout **107 天**) |
| User Story | 21 (done 17 / in_progress 2 / approved 1 / pending 1) |
| PRD | present (v1 Active / v2 Approved) |

`consistency_check`: **8 条 advisory flag, 全为 `active_change_not_in_upm`**, 全部指他轨 m6/m7, 非本 session 引入。

自定义检查 15 OK / 1 FAIL (`plugin-cache-currency`, 见 §2 低优先级)。

---

## §6 Next session 入口 + 优先级建议

1. ⭐ **裁 `Aria#177` 建议 3 的档位** (是否合并掉 `m6-version-badge-match`) —— 它挡着 plugin-version POINTS 探针, 而那个探针是 §2 里三条版本类问题的共同处方。
2. **决定 `aria-plugin#194` 是否发 v1.73.1** —— 不发就修不到采用方, 发则要动整个同步面 (而那个面正是 #177 说的零机械覆盖区)。**这两条是同一个结**。
3. 🔐 **普查其余带 deadline / status 的 project memory 是否也停在旧快照** —— secret rotation 这条已修, 但它暴露的是**类**: memory 记的是写下那天的事实, 闭环时无人回写它。
4. 把 §2 中优先级那条 `scan-now-must-violation` **开成 issue** —— 否则它就是这个 session 版本的「只活在 handoff 文字里」。

---

## §7 提交清单 (commit hash + multi-remote parity)

| 仓 | SHA | origin | github |
|---|---|---|---|
| `10CG/Aria` | `c02b0ef` (含 `8d2903e`) | ✅ equal | ✅ equal |
| `10CG/aria-plugin` | `f314785` | ✅ equal | ✅ equal |
| `10CG/aria-standards` | `21748d4` (未改) | ✅ equal | ✅ equal |
| `refs/aria/coordination` | `87147af` | ✅ equal | ⚠️ `ad0287f` (2026-05-24, 落后 113) — 见 `aria-plugin#195` |

`handoff_autofill` 的 sync 段: **0 warning**。gitlink 完整性 **6/6 ok** (首扫时 aria/github 曾报 `orphan_unverified` counter=1, `ls-remote` 取地面真相确认可达, 重扫翻回 ok —— 是 push 后单次 generation skew, 机制按设计 fail-closed 工作)。

合并路径: aria 子模块本地 `merge --ff-only` + 双推, **未走 Forgejo 服务端合并** (CLAUDE.md 硬约束 1)。四次 `ls-remote` 逐端独立核验。

---

## §8 Memory entries this session (2 new + 1 updated)

- **新增** [[feedback_partial_freeze_makes_results_unfalsifiable]] — 半冻结使结论不可信且方向随机; 检查器自身先过基线自检
- **新增** [[feedback_truncated_listing_makes_no_duplicate_a_false_conclusion]] — 截断清单上的「没找到」是零信息
- **更新** [[feedback_ai_narrows_owner_decision_space]] — 追记形态 3 的反面: 作用域够不到 ⇒ 该新开而非并单

索引压缩: MEMORY.md 24558 → 24343 B (余 233)。移 3 条窄指针入 `MEMORY-archive.md` (validate-convention-assumption / combined-mode-sister-spec / premerge-iteration-pattern), **fact 文件全部保留在 memory/**。
