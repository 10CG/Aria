# Tasks: state-scanner 陈旧 ref 假同步修复 (v8 — D15′ 双角色谓词 + F10″ 八分支 + prune 前提; R7 8C/12M/10m 全折)

> **Spec**: [proposal.md](./proposal.md) | **Level**: 3
> **Status**: Draft v6 (v1→R1→v2→R2→v3→R3→v4→R4→v5→**R5 FAIL [公式的上游数据不存在]**→**v6 + F10′**; 待 **R6** 收敛 → A.2/A.3 lock)
> **范围**: 核心机制 (F1′/F2′/F3′/F4′/F5′/F6′/F9′) + 🆕 **F10′** (detached-HEAD commit-based parity — **R5-C-A 的解药**, owner 裁定)。Rule #7 → [姊妹 Spec B](../state-scanner-snapshot-stderr-secret-leak/); `issue-cache-freshness` → [姊妹 Spec C](../state-scanner-issue-cache-freshness-assertion/)。
> **编号不可变**。v1/v2/v3 编号已作废 (两次机制重写 + 一次拆分)。
> ⚠️ **v6 修复了 v5 的重号**: 原有**两个 `2.13`** (R5-m-3) ⇒ 设计闸改编号 **2.14**。#95 归档门按 checkbox 计数, 重号会算错。

---

## 1. 前置裁决 (Phase A 内锁死, 不留给 Phase B 即兴)

- [x] 1.1 **OQ-A**: `read_only_remotes` 默认值 (倾向 `[]`, 不自动推断)。**必须与 2.7 的非空护栏捆绑裁定**
- [x] 1.2 **OQ-B**: `coordination_fetch` 块 shape (倾向: 保留原块 + 另开 `remote_refresh` 新块 = 纯 additive)
- [x] 1.3 **OQ-C**: 离线 debounce (倾向: 不造新机制, 用 `has_unreachable_remote` gate 建议层)
- [x] 1.4 **OQ-D (v8 已裁, D15′)**: 旧单键 `freshness_window` **退役**; 双键 `sync_freshness.evidence_window_seconds` (3600, 须 > TTL 30s 且 > scan 全程 17.6s) + `sync_freshness.hard_cap_days` (7) + `sync_freshness.k_min` (3); 见 proposal OQ-D v8
- [x] 1.5 🆕 **OQ-E**: F9′ 二选一 —— **必须锁死** (US-008 数据丢失护栏在此路径; AC-10 的断言字段跟着定)
- [x] 1.6 **enforced_remotes 命名空间**: 必须对齐 `phase-c-integrator/SKILL.md:574` 已发布的**顶层 `multi_remote.*`** 跨 skill 契约。**不得另立门户** (否则 state-scanner 与 phase-c-integrator 对「该强制的 remote 集合」产生 split-brain = 本 Spec 的病在跨 skill 层复现) (✅ Phase 4 收口, v1.62.0)
- [x] 1.7 `multi_remote.py` **绕过 config-loader** (直读 `.aria/config.json`, 默认值来自代码内常量) ⇒ 接上或显式声明 (决定 `DEFAULTS.json` 对本 collector 是否真是 SOT)
- [x] 1.8 **schema SOT**: 真 SOT = `references/state-snapshot-schema.md` (**AD-SSME-6**, `validate_schema_doc.py` 机械强制)。`multi_remote.py:4` 的 "canonical SOT is git-remote-helper" 是**被取代的 stale docstring** ⇒ 改 docstring 指向真 SOT。**不得**把 SOT 迁到代码 (会推翻 AD-SSME-6 并架空 validator) (✅ Phase 4 收口, v1.62.0)
- [x] 1.9 fetch 并发: **per-host 上限** (默认 ≤4/host) + 丢连重试退避 + **全局 `refresh_deadline_seconds`** (默认 15s)。**删除 `fetch_all: false` 旋钮** (`enforced_remotes: ["origin"]` 已够; 不为收窄 fetch 发明第 4 个键)
      🔴 **v6: 「per-host」= 按解析后的 hostname 去重** (跨仓库/跨 remote 名聚合), **不是按 remote 名字个数** (R5-C-C)。实测本仓 4 仓 × 2 remote = **仅 2 个物理 host** (forgejo.10cg.pub / github.com)。
      ⚠️ **R4 的 `ceil(60/4)×7s≈105s` 算式错了** (把 cap-4 当全局单池)。正确: `max(ceil(20/4)×7.0s, ceil(20/4)×3.5s) = 35s`。**方向不变但量级差 3 倍** ⇒ 若按 remote 名字个数限流, 真会跑出 105s 那档
- [x] 1.10 🆕 **OQ-F**: `verify_mode: "ls_remote"` 路径归宿 (倾向 **退役** —— F3′ 全量 fetch 已让它冗余; 保留 = **第三个独立可达性计算点 + 双倍网络**)。R5-M-5 (✅ Phase 4 收口, v1.62.0)
- [x] 1.11 🆕 **Spec B 的词表裁定 (OQ-B1) 是本 Spec 的前置** —— `error_kind` 复用 Spec B 的分类器 (3.6), 而 Spec B v1 的 §1/AC-4/task-1.1 **三处互斥且无裁定任务** (R5-M-4)。**Spec B v2 已裁定 = (b) 保留旧词表** ⇒ 本 Spec 的 `error_kind` 取值域 = `network`/`auth_403`/`non_ff`/`git_missing`/`other`。
      ✅ **好消息: 本 Spec 的正确性不依赖此词表** —— `has_unreachable_remote` 已三态化 (`fetch_ok == false`, **零枚举**), `blocking_unknown` 是补集定义 ⇒ **两者都无枚举可漏**

## 2. 红测试先行

> 命令: `python3 aria/skills/state-scanner/tests/run_tests.py`

- [x] 2.1 **一次性缺陷证据**: 往既有 `test_multi_remote_mocked.py:685` `test_local_refs_stale_flag` 加 `overall_parity` 断言 —— 它**早已构造事故 fixture**, 只是从没断言那个会暴露矛盾的字段 (跑出 `local_refs_stale=True` 而 `overall_parity=True`)。**⚠️ 豁免 2.14 设计闸** (v6 修交叉引用: 原写「2.9」, 但 renumber 后 2.9 是 AC-13, 设计闸是 **2.14** — R5-m-3)。F2′ 退役 `local_refs_stale` 后它注定转不绿, 由 **12.3** 重写
- [x] 2.2 **AC-1**: remote **¬E∧¬X** (v10 三档词汇) + 真实落后 → `parity != equal` ∧ `reason == "not_refreshed"`
- [x] 2.3 **AC-2**: origin 刷新成功且 equal + github fetch 失败且真落后 → github `unknown` + network 类 reason + `overall_parity: false`。**fixture 钉死: github 无窗口内成功 `fetched_at`; 用 mock `_run` 注入精确 stderr, 不打真实域名** (实测 TLS 失败 stderr 是 `gnutls_handshake() failed`, 不落在任何已知 pattern ⇒ 真实网络会环境相关误判)
- [x] 2.4 **AC-6**: 子模块 remote 从未 fetch → 不得提供 `equal` 正证据 (✅ Phase 4 收口, v1.62.0)
- [x] 2.5 **AC-7**: **¬E∧¬X** 且 `behind` 不得降级; **¬E∧¬X** 且 `ahead` 不得让 `has_pending_push` 变 false (v10 词汇: 降级豁免只看档位, 下界信号恒真)
- [x] 2.6 **AC-8** (**owner 裁定**: `ahead` 不阻断, 但**也不是正证据**; `overall_parity` 语义 = 本地与远端一致): `origin=equal + github=ahead` (golden fixture 场景) → `overall_parity: true` ∧ `has_pending_push: true`。**前提: ≥1 remote 为 `证据资格 ∧ equal [v9]`**。单 remote 且 ahead → `false` (见 AC-12, 二者现已自洽不再互斥)
- [x] 2.7 🆕 **AC-11 (防 R3-C5 恒红)**: **detached-HEAD 子模块** + 全部 remote 刷新成功 + 主仓 equal → `overall_parity` **仍 true**。**本仓可直接 dogfood** (`aria` 子模块正是 detached)
- [x] 2.8 🆕 **AC-12 (防 R3-N1 vacuous true)**: 空参与集 (零 remote / 全 read-only) → **必须 false**; 无任何 `证据资格 ∧ equal [v9]` (单 remote 且 ahead) → **必须 false**
- [x] 2.9 🆕 **AC-13 (两轴独立)**: fetch 失败(auth) 但 `fetched_at` 仍在窗内 → parity **不降级**, **但** `error_kind` 记录 ∧ `has_unreachable_remote: true` (✅ Phase 4 收口, v1.62.0)
- [x] 2.10 **AC-9 (TTL)**: 30s 内连跑两次 → TTL 命中 → 不降级 + diff==0; fetch 失败 + stale cache → `fetched_at` 不推进 (✅ Phase 4 收口, v1.62.0)
- [x] 2.11 **AC-10 (F9′)**: origin fetch 失败时 `current_branch` 与 `multi_remote[origin]` 不矛盾 (**断言字段由 OQ-E 定**)
- [x] 2.12 🆕 **AC-5 (v4 拆分时把任务弄丢了 — R4 code-reviewer X-6)**: `tracks_multibranch` 中**与 HEAD 同分支**的 track commit 对 HEAD 不可达时 ⇒ `overall_parity == false` 或该 remote `reason` 非空。**这恰恰是本 Spec 叙事的起点** (「同一份 snapshot 自相矛盾 = collector 编排缺陷的指纹」)。无任务 ⇒ 会作为「**AC 勾了但从没实现**」ship = **本仓刚 ship 的 #95 归档门会 block 它** (✅ Phase 4 收口, v1.62.0)
- [x] 2.13 确认 2.2-2.12 **及 2.15-2.18** 在**未修改代码**上全部 RED。任一意外 GREEN ⇒ 诊断有误, **回 Phase A**
- [x] 2.14 **设计闸** (v6: 原为重复的 `2.13`, R5-m-3 修): 修复后若任一红测试 (2.1 除外) **仍无法转绿** ⇒ 设计缺陷, **回 Phase A**

### 🆕 v6 红测试 (R5 的 5 个 Critical 各配一条; **每条成对给「健康必绿」+「故障必红」两个 fixture**)

- [x] 2.19 🆕 **v8 (RC-6; v9 补全枚举): §13.2 八分支各配红测试, 成对给「健康必绿 + 故障必红」** — 全八支: **¬豁免(S,R) ⇒ orphan_unverified** (断言必须**精确 status == orphan_unverified** [agent3 m-4 — ≠orphaned/不阻断类弱断言会放过忽略豁免的实现]; 化石态构造: S 的 R ref 钉 G 父提交 + G 经 origin 在 odb + R 腿 fetched_at=null) / shallow ⇒ 不阻断可见 / no_matching_remote ⇒ 可见不阻断 / rc=129 ⇒ orphaned / 非 gitlink tree ⇒ skip 可见 / **no_published_ref** / **uninitialized** / **soft-error (rc=128)** / D18 ≥k_eff ⇒ 升级 (fixture 另注: (f) 代差态构造走「R 腿 fetch 失败/退避 + cache 预置 gen 差」— deadline 砍腿会被防饥饿优先刷, 造不出 [agent3 m-6])。全部纳入 2.13 全-RED 闸 (健康侧除外)。
- [x] 2.15 🔴 **AC-16 (F10″ 正向 — 本 Spec 的存在理由; v7 按 D14 重述)**: 主仓在 R 上**已发布** commit 引用的子模块 gitlink 在该子模块的 R 上**不可达** ⇒ `gitlink_orphaned(R) == true` ⇒ blocking ⇒ `overall_parity` **必须 false** + `multi_remote_drift` 给出 `git -C S push R <branch>` 修复建议。
      **fixture = 2026-07-12 活体事故态**: 主仓 github/master=`dfb3118` 引用 `standards@79b7cd6`, standards 的 github 只到 `9df1722` (G 不可达)。
      ⚠️ **未修改代码上必须 RED** (事故当天 scanner 报 `overall_parity: true`)。
      ⚠️ fixture 的 parity 断言写法 (v8 按 qa m-1 精化): **parity 相关字段与未修改代码基线逐字相等** (生产代码对 detached 子模块 leg 恒 unknown/detached_head, 不会真产出 ahead — 那是审计手工 rev-list 的反事实); 若要共验 AC-8, fixture 另加一条主仓 ahead leg (第二 bare remote + 本地领先 1 commit)
      🆕 **v8 两个新 fixture (RC-1/RC-5)**: **(prune)** 远端删支后本地化石 ref 仍 contains G ⇒ 无 --prune 必须 RED (假绿), 有 prune 正确报警; **(rc=129)** G 不在 S 本地 odb ∧ 豁免(S,R) ⇒ 必须判 orphaned (fail-soft 直觉实现下 RED)
- [x] 2.16 🆕 **AC-17 (F10″ 对偶 — 防过冲成恒红; v7 按 D14 重述, 四分支)**:
      **(a)** 已发布 gitlink 全 remote 可达 (detached-HEAD 子模块) ⇒ 不阻断 — **CI fixture = 合成 bare-remote** (v9 agent3 m-7: 本仓 dogfood 态是环境依赖, 归 12.5 人工任务, 不做自动化断言)
      **(b)** 本地 HEAD 领先 (新 gitlink 未发布) ⇒ **零误报** (F10″ 只看已发布 C)
      **(c1)** 🔴 反惯例·故障侧: 默认分支叫 `trunk` + `refs/remotes/R/HEAD` 不存在 + orphaned ⇒ 必须报警
      **(c2)** 🔴 反惯例·健康侧: 同环境 + 可达 ⇒ 必须不报警 (v8 拆两 checkbox, qa m-2; 锁死零分支名假设 — 本仓三子模块恰好全叫 master, dogfood 测不出命名依赖)
      **(d)** pin 住旧 commit 但 branch-可达 ⇒ 不报警 (R6-M-4)
      **(e)** 🆕 tag-only pin (RM-11; v9 锁咬合条件 [agent3 M-5]): fixture **必须在 S 本地造 tag 指向 G** (`git -C S tag pin-t <G>` — 采用者历史 fetch 遗留 tag 的真实态; 本地无 tag 则与普通 orphaned 字节级同像, 未来加 tag--contains 消音的实现测不出) ⇒ 断言**仍报警** — 钉死 branch-可达收窄 (逃生口 read_only_remotes)
      **(f)** 🆕 跨腿代差 (RM-2): 主仓 R leg 本代 fetch (C 含新 gitlink) + S 的 R leg 上代 fetch (豁免内, gen(S,R) < gen(主仓,R)) ⇒ 不判 orphaned, 记 orphan_unverified (时序假象非破损)
- [x] 2.17 🆕 **AC-14 (`has_unreachable_remote` fail-CLOSED — 防第六次复发, R5-C-B)**: 分类器返回 **catch-all** (`other`/`unknown`/`git_error`) ⇒ `has_unreachable_remote` **必须 true**。
      **fixture 注入 owner 实测的真实 stderr** (今天全部落 `other`): `Failed to connect to <host> port 443` / `gnutls_handshake() failed` / `Permission denied (publickey)`。
      **对偶**: `fetch_ok == "not_attempted"` (deadline 砍掉) ⇒ **必须 false** (我们没试 ≠ 对方不可达)
- [x] 2.18 🆕 **AC-15 (deadline 三态 + 防饥饿 — 防 C-C 恒红 **和** v6 起草期差点引入的假绿)**:
      **(a)** leg 被砍但 **E** 成立 (墙钟 ≤1h) ⇒ evidence_grade=fresh ⇒ 作证 ⇒ overall **不得** false (v9 D20; fixture 参数钉死: 8 腿/scan + 30/30 拆分 + 间隔 30min); **(a′)** ¬E∧X ⇒ stale_unverified 三断言配对 (不作证 [全腿 ¬E∧X ⇒ false] / 不阻断 [另加 E 腿 ⇒ true 配对 fixture] / 必渲染); **(a″)** 稀疏节律 fixture (间隔 2h 多轮, k_eff 路径真执行); **(a‴)** 边界 fixture (72 腿单 host); **(a⁗)** 🆕 v10 D20 核心格: E∧¬X 腿 (50min+gen>k_eff) ⇒ evidence_grade=fresh ∧ 作证 (v8 式「¬X 一律 blocking」实现必 RED)
      **(b)** 🔴 leg **¬E ∧ ¬X** ⇒ evidence_grade=expired ⇒ 降级 blocking ⇒ overall **必须 false** —— 即使 origin 提供新鲜正证据 (防假绿)。🆕 v9: **¬X 三分支单变量 fixture 各一** (代际>k_eff [叠加墙钟>1h] / 墙钟>hard_cap [cache 预置 8d, 免时钟 seam] / null)
      **(c)** 防饥饿 (v8 RM-7 carve-out): 连续 N 次 scan ⇒ 每条**非退避** leg 至少被刷新一次 (优先级 = `fetched_at` 升序); 退避腿按 3.5d 节律 + `backoff` 标记, 不入全称量词
      **(d)** `remote_refresh.skipped_count > 0` 必须出现在输出区块

## 3. F3′ — 新鲜度靠获取 (`remote_refresh`)

- [x] 3.1 `coordination_fetch` 泛化 + **改名 `remote_refresh`**: fetch **所有 enforced remote** (主仓 + 全部子模块)。🔴 **v8 (RC-1): Fetch 1 必须带 `--prune`** — 无 prune 时 fetch 只增不删, 远端删支/force-push 后本地化石 ref 使 F10″ contains 假绿 (第十次复发最强候选); prune 语义进 F3′ 正文 + 横扫表前提列 + AC-16 prune fixture
- [x] 3.2 **改名波及 ≥11 个引用点**, 逐一处理: `normalize_snapshot.py` / `renderers/track_board.py` / `lib/coordination_ref.py` / `collectors/__init__.py` / `scan.py` / `tests/test_coordination_fetch.py` / `tests/test_p1_layer_h.py` / `SKILL.md` / `state-snapshot-schema.md` / `phase-1-collectors.md` / `docs/rule9-5layer-matrix.md` + 🆕 v8 (backend m-1 grep 实证补 2): `collectors/handoff_multibranch.py` (:9 依赖声明 + :109 remote 常量) / `collectors/_common.py` (✅ Phase 4 收口, v1.62.0)
- [x] 3.3 **`fetch_ok` 锚定 Fetch 1** (#141 two-fetch 语义)。**benign-missing 的 `refs/aria/coordination` 不得置 `fetch_ok=false`** —— github/子模块远端几乎必然没有它, 否则**每个非-origin remote 恒 false ⇒ 恒红**
- [x] 3.4 **非交互契约**: `stdin=DEVNULL` + `GIT_TERMINAL_PROMPT=0` + `GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=N"`; auth 失败**只提示一次** (✅ Phase 4 收口, v1.62.0)
- [x] 3.5 🔴 **并发 + deadline 三态 (v6 重写 — R5-C-C)**: 全并行 + per-host 上限 (按 **hostname 去重**, 见 1.9) + 丢连重试退避 + 全局 deadline。
      **到点未完成的 leg ⇒ `fetch_ok = "not_attempted"` (三态之一)**: 不推进 `fetched_at` / **不置** `has_unreachable_remote` (我们没试, 不是对方不可达) / 🔴 **但也不直接标 `not_refreshed`** —— **裁决权交回三档全分割 (v10 D20)**:
      ```
      被砍 ⇒ fetched_at 保持上次的值 (v9 D20 全分割三档 — 守卫两两互斥 ∪ 全覆盖):
         E  (证据资格, 墙钟 ≤1h)    ⇒ evidence_grade=fresh — equal 供 ∃ 正证据        ✅ 不恒红
         ¬E ∧ X (豁免资格)          ⇒ evidence_grade=stale_unverified (可见/不作证/不阻断) ✅ 诚实中间态
         ¬E ∧ ¬X                    ⇒ evidence_grade=expired — equal 降级 not_refreshed ⇒ blocking ✅ 诚实
      ```
      🔴 **不得把 `deadline_skipped` 归入 benign 桶** (v6 起草时一度采纳 backend-architect 的此建议, **owner 自查推翻**):
      benign ① 的判据是「**fetch 不能改变它**」; 「我们没去问」**fetch 完全能改变** ⇒ 属「我们不知道真相, 而这是可以知道的」⇒ **过期则照常 blocking**。
      **归 benign 的后果 (可推)**: 大仓 origin 快腿提供 ∃ 证据 + github 被砍判 benign ⇒ `overall_parity: true`, 而 github 可能真领先 100 commit ⇒ 🔴 **假绿 = 本 Spec 要杀的 bug 经由新机制复活 = 第八次复发**
      ⚠️ **v5 无条件标 `not_refreshed` 也是错的** (另一端): 那会让稳态大仓恒红。**正解是两者都不做 —— 只把 `fetched_at` 留在原地, 让三档谓词说话 (v10)。**
- [x] 3.5a′ 🆕 **v9 (agent1 m-3) deadline 到点 in-flight 语义写死**: **已起跑的 fetch 允许跑完, 只砍未起跑腿** — 保证每 scan ≥1 腿推进 (慢网单腿 >15s 采用者不致恒零覆盖); 超长挂死由 _run 自身 timeout 兜底
- [x] 3.5b 🔴 **防饥饿 — fetch 优先级 = 最久未刷新者优先** (`fetched_at` 升序, `null` 最优先):
      **若 fetch 顺序固定 ⇒ deadline 每次砍掉同一批靠后的 leg ⇒ 它们的 `fetched_at` 永远推不进 ⇒ 恒 blocking 且永不翻身。**
      🔴 **这才是 C-C「大仓恒红」的真正根因 —— 不是分桶, 是饥饿。** (v6 起草时误诊为分桶问题, 差点用「归 benign」这个假绿方案去治它。)
- [x] 3.5c 🆕 **advisory-only 覆盖率信号** (**不进裁决层**): `remote_refresh.skipped_count` + `skipped_remotes[]`; 输出区块提示「本次有 N 条 remote 未刷新 (预算用尽) —— 调大 `refresh_deadline_seconds` 或收窄 `enforced_remotes`」
- [ ] 3.5d 🆕 **永久失败 leg 退避 (v7 — R6-M-2)**: per-leg 持久化 `consecutive_failures`; `fetch_ok=false` 连续 n 次 ⇒ 之后 2^n 次 scan 跳过该 leg (cap 8), 成功即清零。被退避跳过 = `fetch_ok="not_attempted"` (裁决权照常归三档全分割 (v10: ¬E∧¬X 则 blocking) — **退避不豁免诚实**) + advisory 列入 `skipped_remotes[]` 并标 `backoff`。 (TODO: 永久失败 leg 退避 (per-leg `consecutive_failures` 持久化 + 2^n 退避 cap 8) 未找到实现, `remote_refresh.py` 仅注释提及「non-backoff leg」概念, 无退避计数器/跳过逻辑, 无对应测试)
      > 无退避 ⇒ 吊销的 deploy key 恒在防饥饿队首 (`fetched_at` 最老) ⇒ 每次 scan 白烧同 host 预算, 挤占健康 leg。
- [x] 3.6 snapshot 记 per-remote `{fetched_at, fetch_ok, error_kind, evidence_grade}` (v10 R9-M4 补: evidence_grade 三值见 F4′)。`error_kind` **复用姊妹 Spec B 的分类器** (枚举, 永不含 stderr 原文)
- [x] 3.7 **`fetched_at` 只在 Fetch 1 真成功刷新时推进** —— stale-serve/degraded (`coordination_fetch.py:379-390` 现返回 `cached:True` + 任意陈旧 `last_fetch_at`) **不得**推进
- [x] 3.8 **TTL 命中时逐 remote replay** per-remote map (现 cache schema 只有 3 个标量键, **无 per-remote 结构**)。🔴 **v8 (RM-8) cache 键形状写死**: 键 = **(repo 相对路径, remote 名)** — 按 remote 名单键会让主仓与子模块同名腿碰撞 (子模块从未 fetch 的 origin 借主仓 origin 的 fetched_at/generation 变可信 = 违反形态 #3 经 cache 键复活); AC-6 fixture 钉成「主仓 origin 已 fetch + 子模块 origin 从未 fetch」碰撞形态
- [x] 3.9 **落点 Phase 0.5** (`collect_git_state` 之前) —— 否则 `git.upstream.behind`(陈旧) 与 `sync_status.current_branch.behind`(新鲜) 在同一 snapshot 打架
- [ ] 3.10 逐一核对全部 15 个 collector 的先后依赖 (TODO: 「逐一核对全部 15 个 collector 的先后依赖」属人工审计产出, 未找到显式核对记录/清单 (SKILL.md 已列出 Phase 顺序, 但未见「逐一核对依赖」的独立产出))
- [x] 3.11 **SKILL.md 写死可关闭性契约**: 「关闭 `remote_refresh` ⇒ 所有 parity 变 unknown」
- [x] 3.12 fetch 结果缓存**原子写** (tmp+rename) —— 它现在承载**裁决输入**
- [x] 3.13 **跨进程同仓并发** (两个终端同时 scan) 写明为**已知可接受降级**: 依赖 git 自身 ref lock; 争用 ⇒ `fetch_ok=false` ⇒ 降级 unknown (**假红方向, 可接受**)。🆕 **v8 (RM-6a) 声明扩到 cache 层**: tmp+rename 防损坏不防 lost-update — 迟写者覆盖早写者的 per-leg 更新 ⇒ 偏红/重复 fetch (可接受, 方向正确); 计数器回退的 fail-OPEN 缝由 3.16 钳位封死。否则 dogfood 时会被当 bug 追
- [x] 3.14 🆕 **三态→旧契约 shim 映射写死 (v7 R6-M-3; v8 按 R7 RM-4 扩格)**: 旧 `coordination_fetch.success` := (fetch_ok == true) (`not_attempted` 映射 false, 保守); 🔴 **真实红条字段是 `degraded` (track_board.py:513), 不是 success** — 派生规则写死 `degraded := (fetch_ok == false) ∧ served_stale_cache`、`cached := served_stale_cache` (🆕 v9 定义 `served_stale_cache` := 本次 Fetch 1 失败且 TTL cache 内存在可服务的旧结果并被端出 — 锚定 coordination_fetch.py:379-390 现行 cached-on-failure 语义)、`degradation_reason` 沿用分类器枚举 (三字段是 12.10 通道 #3 与 DROP_KEYS 的工作键, 不得悬空)。**track_board 改读三态**: `⚠离线` 仅 `fetch_ok == false`; `not_attempted` 渲染「未刷新」。映射表配 lock 测试: **3 态 × {success, degraded, cached} = 9 格全断言**; 若红条语义变更 (失败+无 cache 也红) 属有意 ⇒ 进 13.6 式行为公示, 本 v8 默认**不变更** (保留 degraded 派生)。
- [x] 3.15 🆕 **#141 two-fetch 保留声明 (v7 R6-M-7; v8 补限定)**: `remote_refresh` 对**主仓** origin 的 coordination orphan-ref fetch (Fetch 2) **独立于 branch-refs (Fetch 1), 不合并**; F6′「一次往返」量词只作用于 branch-refs 层。测试: mock `_run` 断言**仅主仓 origin 恰好 2 次** fetch (branch + coordination); **子模块 origin 与一切非-origin 恰好 1 次** (backend m-2 — 防 N 子模块白烧 N 次 Fetch 2)。🆕 **prune 无害断言 (RC-1; v9 修断言对象 [agent2 m-1])**: Fetch 1 的 `--prune` 作用域 = Fetch 1 refspec; Fetch 2 是 src-only refspec (**本地不产生 ref, 只进 FETCH_HEAD** — coordination_fetch.py:408 实读) ⇒ 断言对象改为 **`coordination_ref_present` 采集值不因 prune 改变** (实验已证: refspec 限定 prune 连手造本地 ref 都不碰, 结论比 v8 声称更强)。
- [ ] 3.16 🔍 **双角色新鲜度谓词 (v8 — D15′ 取代 v7 D15; R8 重点对抗, 第 11 次复发候选位)**: (DEFERRED: fail-CLOSED, observed_rotation 未持久化, k_eff=k_min 冷启动 (multi_remote.py:1290-1297 docstring 明确自述: 「does NOT yet persist a per-host observed_rotation statistic... k_eff = k_min cold-start fallback... a follow-up increment that adds observed_rotation persistence must replace this constant」))
      **谓词** (SOT = proposal F4′ v8 公式块, 此处为实施任务):
      ```
      证据资格(r) := fetched_at ≠ null ∧ 0 ≤ (now − fetched_at) ≤ evidence_window (默认 1h; 负值⇒视同 null, v10 钳位)
      豁免资格(r) := fetched_at ≠ null ∧ generation_age(r) ≤ k_eff
                   ∧ (now − fetched_at) ≤ hard_cap (默认 7d)
                   ∧ consecutive_unverified(r) < k_eff                    # D18
      ```
      **配置键**: `sync_freshness.evidence_window_seconds` (3600) / `sync_freshness.hard_cap_days` (7) / `sync_freshness.k_min` (3); `K_CAP = 8` 常量。旧键 `freshness_window` **退役** → F2′ 清扫清单 + 配置迁移注。
      **k_eff 收敛耦合 (RC-3; v9 8C-3 修分母 scope)**: `k_eff = min(K_CAP, max(k_min, observed_rotation))`, 🔴 `observed_rotation = **max over hosts** ⌈该host腿数 / max(1, 该host上轮实际覆盖数)⌉` — **逐 host 记录覆盖数** (全局单标量在异速双 host [本仓 forgejo 7s vs github 3.5s] 下算偏小 ⇒ 恒红); **rotation 记录缺失 (冷启动/缓存损坏) ⇒ k_eff = k_min (偏红 fail-CLOSED)**。**双收敛条件 (v9 8M-11)**: 不恒红 ⇐ rotation ≤ k_eff **∧ rotation × scan间隔 ≤ hard_cap** (墙钟臂独立可击穿)。fixture 参数钉死: 8 腿/scan + 30/30 host 拆分 + scan 间隔 30min (全部实测/批准值, 不得反推); 边界 fixture 批准参数 = 72 腿单 host (rotation 9 > K_CAP 8)。
      **D18 求值先序 (v9 D20 附带)**: 本 scan 该腿 fetch 成功 ⇒ `consecutive_unverified` **先清零再评豁免** — 恢复腿不落旧计数器阴影 (消灭 E∧¬X 恢复路径); 计数器处于 expired(blocking)/backoff 态时**冻结** (不 +1 不清零); 🆕 v10 (R9-M6′): **「本 scan fetch 成功」事件优先于冻结** — expired 态腿 fetch 成功 ⇒ 清零照常发生 (先序链: fetch 成功 > 冻结 > 递增)。**D18 锁存 (agent1 m-4)**: 升级 blocking 后锁存至「本 scan fetch 成功」才解锁 — k_eff 动态增大不解锁 (无 fetch 不翻转裁决)。
      **generation 写入侧 (RM-5/RM-9/RM-6b, 三条全 fail-CLOSED)**:
      - `scan_generation` **仅在 remote_refresh 实际执行 fetch 轮次 (TTL miss) 时 +1**; TTL 命中 replay ⇒ 计数器与全部 generation_fetched 原样保留 (lock 测试: TTL 命中连跑 N 次 ⇒ 代龄不变 — 防快速连跑恒红)
      - `generation_fetched` **只在该 leg Fetch 1 真成功时推进** (逐字镜像 3.7; stale-serve/degraded/not_attempted/backoff 不得推进; lock 测试: 失败 fetch 后 generation 未动 — 防写入侧污染架空代际窗)
      - **负代龄钳位**: `generation_fetched > scan_generation` (并发 lost-update 回退产物) ⇒ 视同 null ⇒ ¬豁免; 计数器写入取 `max(磁盘现值, 内存值)` 单调不回退
      **D18 升级**: per-leg `consecutive_unverified` 计数 (cache): 该 leg 本 scan 处于 stale_unverified/orphan_unverified ⇒ +1, 恢复证据资格 ⇒ 清零; ≥ k_eff ⇒ 豁免失效 ⇒ blocking。两 unverified 状态**必须渲染进输出区块** (进 AC, 不许只活在枚举)。
      > **为什么拆双谓词**: 单谓词 可信 兼任「∃ 作证」与「¬blocking 豁免」两角色是 R7 三 Critical 的共同根 — 作证要**世界时间**新鲜 (远端由并发 session 独立推进, 创始事故 14h), 豁免要**注意力节律**新鲜 (防大仓恒红)。量纲不同, 必须分键。

## 4. F1′ — 两个正交轴

- [x] 4.1 🔴 **可达性轴 (v6: fail-CLOSED, 不得正向枚举 — R5-C-B, 同一不变量第六次复发)**:
      ```
      has_unreachable_remote(r) := fetch_ok(r) == false      # 试了 → 失败 = 不可达, 与 error_kind 无关
                                                             # not_attempted ≠ false ⇒ deadline 砍掉的不置位
      ```
      🔴 **三态使枚举白名单变得多余** —— 这是最彻底的 fail-CLOSED: **零枚举, 无补集可漏**
      ⚠️ **v5 写的是「按 network 类置位」= 正向枚举 ⇒ 未列举值 fail-OPEN**。owner 用生产分类器跑真实 stderr 实测: **5 种真实故障, 3 种落 catch-all `other`** (HTTPS 连不上 / TLS 握手失败 / **SSH 公钥被拒**) ⇒ **不置位**。
      **加重情节**: auth 被拒也落 `other`, 而 **AC-13 正是要测 auth ⇒ has_unreachable 必须 true** ⇒ **v5 的措辞让 AC-13 自己测不出来**。
      🔴 **必须「替换」而非「叠加」触发器** (R5-m-4): 默认 `verify_mode=local_refs` 下 `reachable` **恒 True** (`:163/:182` 硬编码), `:410` 的触发集 (`network_timeout`/`auth_failed`/`not_found`) **只产自 ls_remote 路径** ⇒ **`has_unreachable_remote` 今天在生产默认模式下结构性恒 False**
- [x] 4.2 **新鲜度轴按 D15′ 双谓词实现** (v8: 原 wall-clock 单窗定义作废, SOT = proposal F4′ v8 公式块 + tasks 3.16; 本任务 = 把 证据资格/豁免资格 接进 parity 降级与 ∃ 子句, **不得留任何 freshness_window 引用** — 5.1d 单一定义闸校验)
      ```
      证据资格(r) := fetched_at(r) ≠ null ∧ 0 ≤ (now − fetched_at(r)) ≤ evidence_window (1h)   # ∃ 侧; 负墙钟龄 ⇒ 视同 null (v10 钳位)
      豁免资格(r) := fetched_at(r) ≠ null ∧ generation_age(r) ≤ k_eff
                   ∧ (now − fetched_at(r)) ≤ hard_cap (7d) ∧ consecutive_unverified < k_eff  # 降级侧
      ```
      ⚠️ null 兜底教训保留 (v5 未定义 `fetched_at = null` ⇒ 与违反形态 #3 同形, `multi_remote.py:497` 的 None 判「不陈旧」bug): 双谓词对 null/generation 缺失/负代龄**全部 fail-CLOSED ⇒ false** (3.16 钳位)。
      ⇒ 证据资格 gate ∃ 子句; 豁免资格 gate equal 降级三档 (作证/stale_unverified/not_refreshed)
- [x] 4.3 **降级只作用于 `equal`** → `unknown` + `reason: not_refreshed`; `behind`/`diverged`/`ahead` **原样保留**
- [x] 4.4 `reason` 优先级: **后置降级只在 parity 本会是 `equal` 时改写** —— 不覆盖 `detached_head` / `shallow_clone` / `no_local_tracking_ref`
- [x] 4.5 `reason` enum 补齐 schema (代码已发 `rev_list_failed` / `rev_list_parse_failed`, 未记录)

## 5. F4′ — `overall_parity` 裁决表 (核心)

- [x] 5.1 🔴 **`benign_unknown` 按「fetch 能否改变它」分层 (v6 修正分桶 — R5-M-2)**:
      ```
      benign_unknown(r) := parity(r)=="unknown" ∧ (
            reason(r) ∈ {detached_head, shallow_clone,                      # ① fetch-无关 ⇒ 恒 benign, 不看新鲜度
                         remote_branch_missing}                             #    🆕 v6 从 ② 移入 (见下)
         ∨ (reason(r) == "no_local_tracking_ref" ∧ 证据资格(r))             # ② fetch-依赖 ⇒ 断言「没发布」需世界时间新鲜 (v8)
        )
      # 🔴 deadline_skipped 不在此 —— 「没去问」≠「不适用」, 它由双角色谓词裁决 (v8, 见 3.5/3.16)
      ```
      🔴 **`remote_branch_missing` 从 ② 移入 ①** (backend-architect 代码实测): 它产自 `_remote_parity_ls_remote:253` 的 **实时 `git ls-remote` 网络往返** —— 「这一秒对方**权威地**回答『没有』」, **新鲜度内建在自己的调用里**; 而 `no_local_tracking_ref` (`:181`) 是读**可能陈旧的本地缓存**失败。
      **v5 把它塞进依赖 `可信(r)` 的 ② 桶的后果**: `可信(r)` 挂在**另一个 collector** (`remote_refresh`, Phase 0.5) 的 `fetched_at` 上, 而 ls_remote 是 Phase 1.12 内**自己发起**的独立调用 ⇒ **拿不到那个 `fetched_at`** ⇒ `可信` 恒 false ⇒ **永远落 blocking ⇒ 又一次自造恒红**
- [x] 5.1b 🔴 **`blocking_unknown` 必须 fail-CLOSED (兜底反向定义), 不得写成正向枚举** (R4 **四方独立收敛**):
      ```
      blocking_unknown(r) := parity(r)=="unknown" ∧ ¬benign_unknown(r)
      ```
      ⚠️ v4 初稿写成 `reason ∈ {6 个显式值}` ⇒ **任何未列举值 fail-OPEN (不阻断)**。实测可达的漏网之鱼:
      - **`reason = None` + `parity = unknown`**: `multi_remote.py:308/312/317` **三条 best-effort 返回路径**
      - **`parse_error`** (`:281`)
      - **姊妹 Spec B 分类器的兜底值** `unknown` / `git_error` / `permission_denied` / `timeout` —— backend-architect 用**真实 `git fetch` 连接失败**复现: 其 stderr **一个已知 pattern 都没中** ⇒ 落 catch-all ⇒ 按正向枚举**不阻断**
      ⇒ **同一不变量的第五次复发**。**教训: 「把不变量写进文档」≠「把它写进兜底默认值」。**
- [x] 5.1c 🆕 **机械防漏格 pin 测试** (把「逐格填」从纪律变成机制): 构造一个**代码里不存在的** reason 值 ⇒ **必须阻断**。断言公式实现走 `¬benign` 兜底而非正向 blocking 枚举
- [x] 5.1d 🆕 **谓词定义域横扫闸 (v6 新增; v7 按 D16 落位; v8 补单一定义断言)**: 横扫表 **SOT 搬 aria-plugin** (`skills/state-scanner/references/predicate-domain-table.md`), 主仓 proposal §横扫表保留为审计快照 (表头注明 SOT=插件侧)。**机械 lock 测试** (插件 unit test): (a) multi_remote/sync 代码布尔谓词集合 ⊆ 表中登记集合; (b) 🆕 **v8 (RC-2)**: 同一谓词在 spec 语料中的**定义出现次数 = 1 或全部逐字节相等** — 语料范围 **v9 扩到含 DEC** (8M-2: DEC 公式一律指针引用 F4′, 不复制); (c) 🆕 **v9 (D20 附带)**: **守卫全分割断言** — N 档谓词组的守卫两两互斥 ∧ 并集=全域 (R8 两 agent 独立命中 E∧¬X 重叠格 = 第 11 次复发); (d) 🆕 **v9 (8M-1)**: **退役谓词零 live 引用** — `可信(r)`/`freshness_window` 等退役符号在非溯源区 (无 SUPERSEDED/历史标记的活文本) 出现 ⇒ FAIL (定义单一化闸查不出引用漂移, 本轨两轮各抓 15/6 处残留实证)。
      > **D16 理由**: 表在主仓则插件测试结构性读不到 (R6-M-5); review checklist 被否 — 9 次复发史证明纪律不守恒, 机制才守恒。
      > **R5 元教训**: R4 把「类修不能点修」**只点修在 `blocking_unknown` 上**, 没横扫「还有哪些谓词是正向枚举 / 定义域不完整」⇒ **第六次复发在 `has_unreachable_remote`** (4.1), **第七次在 `可信` 的 null** (4.2)。横扫**当场又抓出** `has_unpublished_branch` **被引用 4 次却从未定义** (5.4) —— **前五轮 25 个 agent-round 无人发现**。
      > ⇒ **把「类修」从纪律变成机制。**
- [x] 5.2 **公式** (⚠️ `∀` 里**没有**独立的新鲜度谓词项 [原 可信(r), v8+ 双谓词同理]):
      ```
      overall_parity = (enforced_set ≠ ∅)                             # 防 vacuous true (Python all([])==True)
                     ∧ (∃ r: 证据资格(r) ∧ parity(r)=="equal")        # QA-C1 正证据 (v8: ∃ 侧用证据资格)
                     ∧ (∀ r: parity(r) ∉ {behind,diverged} ∧ ¬blocking_unknown(r))
                     ∧ (∀ R: ¬gitlink_blocking(R))                    # v10 (R9-M6): gitlink 层, 定义见 13.4 (镜像 F4′ 第 4 子句)
      ```
      **新鲜度谓词从 ∀ 删掉的理由** (qa-engineer R4 实证, 原谓词 可信(r); v10 三档下同理): 它在那里冗余且有害 —— 对 `equal` 的 r, F1′ 降级**已经**把不可信的变成 `not_refreshed`(∈blocking) 挡住了; 对 `behind`/`ahead` 的 r, 新鲜度**没有正确语义** (下界仍为真); 对 benign 的 r, 会让「该 remote 恰好这次 fetch 失败」把 `overall_parity` **拖成恒红**
- [x] 5.2b 🆕 **AC-11b**: benign_unknown (fetch-无关类) 的 remote **自身 fetch 失败** ⇒ `overall_parity` **仍不受它阻断** (只要其它 remote 提供 `证据资格 ∧ equal [v9]`)。**现有 AC-11 只测「全部刷新成功」, 没覆盖这一格**
- [x] 5.3 `ahead` 不阻断, 经 `has_pending_push` 单独承载 (对 `multi_remote.py:400-402` 既有决策的**保留**; 三处证据一致: 代码注释 / golden fixture / AB rubric)
- [x] 5.4 🔴 **「分支未发布」拆出独立 flag `has_unpublished_branch` (v6 首次给出谓词定义 — R5 谓词横扫新发现)**:
      ```
      has_unpublished_branch(r) := parity(r)=="unknown" ∧ reason(r)=="no_local_tracking_ref" ∧ 证据资格(r)
      ```
      (**per-remote**; `证据资格` [v8] 才能断言「真的没发布」而非「我们没 fetch 过」)
      ⚠️ **v5 引用它 4 次** (proposal L197/L250 + tasks 5.4/9.2) **却从未定义它何时置位 / 是 per-remote 还是 repo 级**; 代码中零命中。**这是 v6 谓词横扫抓出的、前五轮无人发现的缺口。**
      不压在 `overall_parity` 上 —— **把三种语义挤进一个 bool 正是它今天撒谎的原因**
- [ ] 5.5 更新 `_aggregate_flags` docstring: **三次违反并列** (零证据 / 陈旧证据 / 从未获取) + **对偶不变量** (假绿的反面是恒红) + **unknown 二分表** (TODO: `_aggregate_flags` docstring 要求的「三次违反并列 (零证据/陈旧证据/从未获取) + 对偶不变量 (假绿的反面是恒红) + unknown 二分表」未见于代码 —— 该函数现已是 dead code (Phase 1 起改用 `_overall_parity`/`_has_unreachable_remote`), docstring 只记录了 QA-C1 历史修复, 未补三段式新框架说明)

## 6. F5′ — enforced remote 集合

- [x] 6.1 消费既有键 `enforced_remotes` / `read_only_remotes` (**按 1.6 的命名空间裁定**) (✅ Phase 4 收口, v1.62.0)
- [x] 6.2 **read-only 排除同时作用于** `overall_parity` **和** `has_unreachable_remote` **和** `multi_remote_drift` 触发 —— 只挂 `overall_parity` 会让「我不关心它」的 remote 抖一下网络仍全局告警 (✅ Phase 4 收口, v1.62.0)
- [x] 6.3 **修假文档** `sync-detection.md:515`
- [x] 6.4 **CHANGELOG 显著标注**: 已设 `enforced_remotes` 的采用者其配置**今天是惰性的**, 本 Spec 让它承重 ⇒ **直接改变网络行为** (✅ Phase 4 收口, v1.62.0)

## 7. F2′ — 退役 mtime 实现 (保留概念)

- [x] 7.1 退役 `local_refs_stale` / `warn_after_hours` 的 FETCH_HEAD-mtime 路径
- [ ] 7.2 **无条件清扫 ≥8 处 SOT** (⚠️ v2 曾把条件写反成「若保留才清扫」—— **退役 = 死配置键, 清扫更必须**): `config-loader/DEFAULTS.json:38` / `.aria/config.template.json:21` (**采用者模板**) / `.aria/config.json` / `config-loader/SKILL.md:79` / `sync-detection.md` ×4 / `git-remote-helper/schema.md:58` / `state-snapshot-schema.md:490` (⚠️ **post_planning R1 M-A 回退勾选**: 本 cycle 清扫的是 `verify_mode`/ls_remote 的 SOT (属 task 1.10 的退役), **不是本条要求的 F2′ `warn_after_hours`/`local_refs_stale` 清扫** —— 7.2 在 `## 7. F2′ 退役 mtime` 章节下。实测至少 4 处仍带退役键: `config-loader/DEFAULTS.json:38` / `config-loader/SKILL.md:79` / `.aria/config.template.json:21` (**采用者模板**) / `.aria/config.json:20`。**另有一处理由互斥待 owner 裁**: `multi_remote.py:164` 写「`sync_check.warn_after_hours` remains for sync.py's own consumption」, 而 `sync-detection.md:358` 写「三个字段从未被任何代码路径消费」—— 二者不可能同真, 保留决定本身缺一个成立的理由。)
- [x] 7.3 清理 `_scan_repo` 的 `stale` 死返回值

## 8. F9′ — `sync.py` 平行计算点 (按 OQ-E 裁定)

- [x] 8.1 `_collect_current_branch` 按 1.5 的裁定处理 ((a) 消费新鲜度 / (b) 声明本地视角 + 输出区块区分)
- [x] 8.2 `sync_status.submodules[].drift` 的 `remote_commit`/`behind_count`/`hint`/`hint_type` 从陈旧变新鲜 ⇒ 核 `submodule update --remote` 建议触发的变化。**US-008 数据丢失护栏在此路径** (`sync.py:312-328` directional guard)
- [x] 8.3 `sync.py` 从不读 `sync_check` config, 而 `phase-1-collectors.md:34` 声称可关闭 ⇒ 修代码或修文档
- [x] 8.4 `remote_refs_age` 在 F3′ 后恒 "1m" ⇒ 标注废弃或删除

## 9. 下游消费者

- [x] 9.1 `handoff_autofill.py:52` 把降级后的 `reason` 升级为 warning —— 否则 F1′ 的 `unknown` 被 session-closer **静默吞掉** = 新假绿通道
- [x] 9.2 `multi_remote_drift` 建议**按 ≥6 种成因分派** (behind/diverged→pull / ahead→push / benign unknown→**不触发** / no_local_tracking_ref→`has_unpublished_branch` / not_refreshed·network·auth→查网络凭据)。**不是一律 fetch/pull** (US-008 directional guard)
- [x] 9.3 `multi_remote_drift` 规则**无去重/冷却** (grep 零命中) ⇒ 按 OQ-C 处理
  > **2026-07-19 进展**: 已在 `references/rules/basic-rules.md` §1.35 补充 OQ-C 说明 (文档层, prompt-based
  > skill 无代码实现面)。~~**OQ-C 本身仍未裁定** (1.3 checkbox 未勾)~~ **[已过时 — OQ-C 由 owner 2026-07-19 裁定「不造有状态冷却」, 1.3 已勾, `degrade_when` 已落 basic-rules.md §1.35; post_planning R1 抓出本段为反向残留]** ⇒ 本条**记为需 owner 在 Phase A 裁定
  > OQ-C 后再落地**, 未强行实现去重/冷却机制 (倾向记录见 proposal.md OQ-C: 用 `has_unreachable_remote`
  > 在建议层降级, debounce 不作用于裁决层)。
- [x] 9.4 **`aria-2.0-m7-fleet-aggregation` (Approved) 消费 `overall_parity`** ⇒ 语义变更需同步该 Spec (其 TB-health-3 pin 到 schema doc)
  > **2026-07-19 完成**: 已在 `openspec/changes/aria-2.0-m7-fleet-aggregation/proposal.md` (TB-health-1
  > 信号表 sync-不齐 行下) + `tasks.md` (TB-health-3 任务下) 各补一条 CAVEAT-parity/同步注, 说明
  > `overall_parity` 现含 gitlink_integrity 阻塞层 + per-remote evidence_grade 新鲜度门 (v8 四子句),
  > 指向新版 schema doc 章节。**只改文档, 未改 m7 代码** (m7 Phase B 未启动, 无代码可改)。
- [x] 9.5 重新生成 golden fixture `tests/fixtures/reference-snapshot-aria.json` (现记 `overall_parity: true` + 子模块全 `equal`, 采自事故现场)
- [x] 9.6 `validate_schema_doc.py` **会真跑 scan.py** ⇒ F3′ 后每次校验触发全量网络 fetch。加 offline/mock 模式; 且它只校验 top-level key, per-remote 嵌套字段无守护
- [x] 9.7 🔴 **offline 旁路 — 12.10 指定的稳定性根治主手段, v8 (RM-12) 从一行扩成完整契约**:
      `ARIA_SCAN_OFFLINE=1` 冻结**三个面** (只冻网络不够 — 通道 #5 是文件 mtime、#6 是墙钟):
      - **网络面**: remote_refresh 全 leg `fetch_ok=not_attempted` + issue_scan 强制 cache 路径 (不打 live); 各 collector 的 offline emit 值逐一定义 (fetch_ok/source/degraded — 15 collector 逐格表, 不留实现者即兴)
      - **缓存态面**: 双跑共用**预置缓存** (测试 fixture 提供), scan **不得改写** `.aria/cache/*` (含 issue_scan 1.13 的重写 — offline 下跳过写盘)
      - **时钟面**: 接受注入时间源 (`ARIA_SCAN_NOW=<iso>`), 天数型 output 与 age 计算读注入值 — 否则跨午夜 CI 跑仍 flaky (通道 #6)。**scope 声明 (v9 8M-13)**: ARIA_SCAN_NOW 是通用 seam, **非 offline 专属** — AC-15 等非 offline fixture 同样可用
      - 🆕 **持久态面 (v9 — 8C-4, lag-1 第四冻结输入)**: 上一份 `.aria/state-snapshot.json` 是 Phase 1.11 (lag-1 check) 的环境输入 — 稳定性双跑必须**预置同态健康上一份** 且 offline 下 scan 不覆写它 (否则 run1 读遗留/run2 读 run1 产物 ⇒ 结构性 diff≠0)
      - 🆕 **计数器面 (v9 — 8M-5)**: offline scan **不递增** scan_generation 与 consecutive_unverified (不计入 D18 代数 — 防离线连跑把健康 leg 升级 blocking 的假红; 明写, 非默认)
      - 🆕 **budget seam (v9 — 8M-13)**: 每 scan 覆盖 N 腿的确定性注入点 (`ARIA_SCAN_FETCH_BUDGET=<n>` 测试专用) — mock `_run` 即时返回时 deadline 永不砍腿, rotation/防饥饿类 fixture 无此 seam 不可构造
      **覆盖损失诚实声明 (进 12.10 与测试 docstring)**: offline 后该稳定性测试对「环境依赖类回归」(缓存新鲜度翻转/网络降级/时钟边界) **永久失明** — 换取确定性; 这些类的守护改由各自单元测试承担 (通道 #1→8.4 / #5→Spec C AC-4 单通道断言 / 其余→各 collector 测试)。**通道 #5 的真序缺陷** (1.11 读 mtime 早于 1.13 重写 = snapshot 非幂等的真产品缺陷) **由 Spec C 的 check 重定义承载修复** (D19 lag-1), 不靠 offline 静音

## 10. 文档同步 (Rule #3)

- [x] 10.1 `references/state-snapshot-schema.md` (**真 SOT**): per-remote 字段 (**含 `evidence_grade`**, v10) + `gitlink_integrity[]` 结构 + `reason` 枚举 + **unknown 二分** + `overall_parity` v8 公式 + **v8 有界承诺** (∃ 证据陈旧容忍 ≤1h; ¬blocking 豁免 ≤ min(k_eff 代, 7d) 且以 stale_unverified 全程可见 — 与本 Spec 修的无界陈旧 bug 是两个量级, 不要被未来审计员误认成同一缺陷复发)
- [x] 10.2 `SKILL.md`: collector 顺序 (Phase 0.5) + 网络行为 + 性能预期 + 可关闭性契约
- [x] 10.3 `references/phase-1-collectors.md` / `sync-detection.md`
- [x] 10.4 `references/output-formats.md`: 🔄 区块呈现不可信 remote + `overall_parity: false` 的**成因分派** 🆕 **v9 (agent1 m-5)**: 输出区块渲染清单点名 — `evidence_grade=stale_unverified` 腿列表 (aging) + `orphan_unverified` 对列表 + `skipped_remotes[backoff]` 标注; 措辞从 v6「不可信 remote」更新为三档词汇。 (✅ Phase 4 收口, v1.62.0)
- [x] 10.5 `RECOMMENDATION_RULES.md` **+ `references/rules/basic-rules.md:69-82`** (规则定义在**两处**; `:78` 注释写死旧语义)
- [x] 10.6 **`docs/architecture/system-architecture.md:892-895`** (主仓 L1 架构文档, **且已 drift**: 记 `overall_parity` 为枚举, 代码发 bool) (✅ Phase 4 收口, v1.62.0)
- [x] 10.7 `config-loader/SKILL.md:79` + `DEFAULTS.json` + `.aria/config.template.json` (✅ Phase 4 收口, v1.62.0)
- [x] 10.8 CHANGELOG: 网络行为变更 + parity 语义 + 惰性配置变承重 + opt-out 方法 + **不把 +4% 写成通用承诺** (✅ Phase 4 收口, v1.62.0)

## 11. Rule #6 (不可协商) — Skill benchmark

- [ ] 11.1 `/skill-creator` benchmark (with/without AB), 结果存 `aria-plugin-benchmarks/ab-results/` (TODO: `/skill-creator` benchmark 未见本 cycle 产出 —— `aria-plugin-benchmarks/ab-results/latest/` 时间戳为 2026-05-13, 早于本 Spec 起始 (2026-07-12), 未重跑)
- [x] 11.2 **修 AB rubric** `ab-suite/state-scanner.json:143` —— 现明写 `"Should exclude parity: ahead and parity: unknown from overall_parity computation"`。v4 下 **ahead 排除 ✓ 但 unknown 需二分** ⇒ rubric 必须精确化, 否则会把正确的新行为判为错 (✅ Phase 4 收口, v1.62.0)

## 12. 验证与收尾

- [x] 12.1 §2 全部红测试转 GREEN (2.1 除外)
- [x] 12.2 🔴 **无回归 (v6 修正 baseline 假前提 — R5-C-E)**: `run_tests.py` → **0 failed** ∧ 无既有绿测试转红 ∧ 新增测试数 = N。
      ⚠️ **baseline 不是 0 failed** —— owner 连跑两次实测 (未修改代码 `0964496`): `Ran 1006 tests ... FAILED (failures=1)`, 失败的是 `test_two_consecutive_runs_diff_zero`。
      ⇒ **本 Spec 认领消除它** (见 12.10)。**Spec B / Spec C 的判据改为「0 failed **除** 该测试 (由母 Spec 消除)」** —— 否则 **Spec B (被指定应先落地) 按自己的 AC-3 结构性无法 ship**
- [x] 12.10 🆕 **消除 `test_two_consecutive_runs_diff_zero` 的漂移通道 (v6 新增 — R5-C-E; v7 按 CE 复验实测修正: 4 条 → 6 条, 见下补充)**:
      | # | 漂移键 | 根因 | 修法 |
      |---|--------|------|------|
      | 1 | `remote_refs_age` | `sync.py:396/405` 读 FETCH_HEAD mtime; **scan 自己的 Phase 1.16 会改写 FETCH_HEAD** | 已由 8.4 覆盖 (F3′ 后恒 "1m" ⇒ 废弃/删除) |
      | 2 | `issue_status.repos[].source` | `issue_scan.py:822` cache 命中返 `"cache"` / live 返 `"live"` (900s TTL 两跑间翻转) | 加入 `normalize_snapshot.DROP_KEYS` |
      | 3 | `coordination_fetch.degraded` / `degradation_reason` | 真实网络抖动 ⇒ 一跑降级一跑不降级 | 加入 `DROP_KEYS` |
      | 4 | `errors[]` 数组 | 同上 soft error 时有时无 | 按 collector 归一 (或与 9.7 的 offline 旁路合并解决) |
      🔴 **数组/嵌套键粒度 (v7 — R6-M-6)**: `DROP_KEYS` 现按**键名全局**丢弃 — 对 `errors[]`/`source` 这类**多处出现**的键会连承重字段一起误伤 (如 handoff.latest_source 与 issue_status.repos[].source 同名不同义)。⇒ drop 规则必须**带路径限定** (JSONPath 式, 如 `issue_status.repos[*].source`), 数组元素按 (collector, kind) 匹配归一而非按 index; 加反向测试: drop 后承重字段 (如 `latest_source`) 仍在。
      📌 **仓内已有逐字先例**: `DROP_KEYS` 的 `cached`/`age_seconds`/`refs_fetched` 注释 (v1.30.2) **明写**「TTL-based, varies between consecutive runs… Stability test requires drop」—— **同一 class 已解过一次, 别再原样引入**
      🔬 **v7 CE 归因复验 (2026-07-14, 干净条件 + 冷/热/陈旧 5 组对照, 结案)**: **custom_checks 确是漂移通道 — 但条件限定** (issues.json **缺失或 mtime>30min** 时触发; 新鲜热缓存 <15min 下不是)。R5「无一是 custom_checks」与 R6「冷缓存复现」**都对, 各自在不同缓存态观察** — 矛盾根源是缓存新鲜度这个隐藏变量。⇒ v6 本行原写的「Spec C §3 归因错」**撤回**, Spec C 的归因是**条件性正确** (其修法可杀通道 #1, 但仅此一条 — flaky 整体消除仍归本任务)。
      **v7 通道清单修正 (4→6)**: 上表 4 条外补: (5) `custom_checks.results[issue-cache-freshness].{status,output}` + `custom_checks.{passed,failed}` — 缓存缺失/mtime>30min, 4 路径 (CE 实测; scan.py Phase 1.11 先于 1.13 执行、check 读 mtime 而 1.13 随后重写缓存 = 机制级确认); (6) 结构性潜伏 — custom_checks 天数型 output 跨午夜日界翻转 + 缓存恰跨 30min 边界的热态时间窗。
      🆕 **v9 (8M-5) 通道 #7 + 新键防线**: `consecutive_unverified`/`scan_generation`/`generation_fetched` (计数器逐 scan 递增) + `fetch_ok` (true↔not_attempted 随调度) + `skipped_remotes[]` + `gitlink_integrity[].status` + `evidence_grade` — v8/v9 新键全部是**环境依赖易变键**; 承重契约键 (计数器/status/evidence_grade) 不可 DROP ⇒ **全部依赖 9.7 offline 旁路冻结** (计数器面 + budget seam); **实施序硬依赖**: 9.7 必须先于或同 PR 于新键落地 (先 ship 新键后 ship offline ⇒ 稳定性测试以第 7+ 通道翻红, 本清单结案失效); 13.8 golden 重采集须附新字段期望说明 (健康态: gitlink_integrity 全 ok / evidence_grade 全 fresh / 计数器全 0)。
      🔴 **根治手段排序 (CE 数据裁定)**: **主 = 9.7 offline 旁路** (两次 scan 钉在同一冻结环境态, 一次封死全类) — 因为 (a) custom_checks 的 `output`/`status` 是**契约字段**, 测试 `test_rule_4_output_NOT_scrubbed` 明确 pin 住不许 scrub ⇒ **DROP_KEYS 结构性不可用于通道 #5**; (b) 6 通道共性 = 环境状态依赖, 通道数随 check 数线性涨, 逐条 DROP 是打地鼠。DROP_KEYS 仅作通道 #2/#3 的辅助。
- [x] 12.3 处理会机械性破裂的既有测试: `test_local_refs_stale_flag` / `test_scan_with_two_remotes_local_refs` / `test_full_main_repo_flow_with_config_overrides`
- [x] 12.4 **AC-3**: mock `_run` 断言「每个 (repo,remote) 恰好 fetch 一次」(**集合/计数不变量, 非 strict order** —— 真并行下调用序由线程调度决定)
- [x] 12.5 **dogfood (本仓)**: `aria` 子模块 detached-HEAD + 全 remote 真 equal ⇒ `overall_parity` **仍 true** (AC-17); **`standards` / `aria-orchestrator` 的 github 镜像若落后 ⇒ 必须报出来** (AC-16); `sync_status` 与 `tracks_multibranch` 不再自相矛盾 (✅ Phase 4 收口, v1.62.0)
      > ⚠️ **v5 的 12.5 已经写了「github 镜像若落后 ⇒ 必须报出来」, 但 v5 的设计做不到** —— **F10′ 之前, 这条 dogfood 任务在 Phase B 必然失败** ⇒ 会撞上 2.14 设计闸 ⇒ 打回 Phase A。**R5 在 Phase A 就抓住了它。** 这正是「dogfood 任务写了但设计不支持」的活体案例。
- [x] 12.6 归档语料 sweep 无新 block (✅ Phase 4: 已跑, `gate_result` verdict=warn / **blocking_reasons=[]** 即 0 block — 见 commit `e7883b0`。原批注「本 Spec 尚未进入 Phase D」为陈旧文本, post_planning R1 M-F 抓出。)
- [x] 12.7 **跨仓落地**: aria-plugin PR → merge → **submodule pointer bump 到 post-merge master SHA** (C.2.4.5 block-default gate) → 主项目 `VERSION` → **多远程推送 (origin + github, 两仓)** (✅ Phase 4 收口, v1.62.0)
- [x] 12.8 版本 bump + 5 处 SOT 同步 + 主仓 badge (✅ Phase 4 收口, v1.62.0)
- [x] 12.9 释放 track claim (✅ Phase 4: 已释放 — `refs/aria/coordination:claims/bfe8285d/s-123d@1436.yaml` 记 `status: done`。原批注「工作进行中, 收尾前不应释放」为陈旧文本, post_planning R1 M-F 抓出。)

## 🔴 13. F10″ — orphaned-gitlink 跨仓可达性 (v7, 按 D14 重写; 取代已证伪的 F10′)

> **不变量**: 主仓在 R 上**已发布**的 commit 引用的每个子模块 gitlink, 必须在该子模块的 R 上**可达** — 否则 `clone --recursive` from R 断裂 (2026-04-10 + 2026-07-12 两次真实事故形态)。**完全不经 parity 表达** (F10′ 教训: 该事故在 git 眼里是 `ahead`, 与 AC-8 互斥)。

- [x] 13.1 🔴 **`gitlink_orphaned(R)` 实现 (v8 按 R7 修)** (multi_remote.py 新函数, per-remote per-submodule):
      ```
      C = git rev-parse refs/remotes/{R}/{main_branch}       # main_branch = 主仓当前分支名 (scan 已知, 非猜测)
      entry = git ls-tree {C} -- {submodule_path}            # v8 (RC-5/M-1): mode 必须 == 160000
      G = entry.sha  (mode ≠ 160000 ⇒ 「非 gitlink」分支, 不入 contains)
      # v9 (8M-3) 前置滤: S 无 remote R ⇒ 直接走 13.2 分支 8 (no_matching_remote), 不进本判定
      #   (rc=0 空输出与真 orphan 同像 — 必须在 leg 枚举层区分, 不可依赖 contains 结果)
      contains_rc, out = git -C {S} branch -r --contains {G} --list "{R}/*"
      no_object  = (rc == 129 ∧ stderr ~ no such commit/bad object)   # G 无处存在 = 更重破损
      unreachable = (rc == 0 ∧ out 空) ∨ no_object                    # v9 收窄: 其它 rc≠0 (如 128 仓损坏)
                                                                      #   ⇒ 13.2 分支 7 soft-error, 不入 orphaned
      orphaned(R,S) = unreachable ∧ ¬shallow(S)
                    ∧ 豁免资格(主仓,R) ∧ 豁免资格(S,R)                 # v8 (RM-1): C 陈旧 ⇒ 不判 (假绿防)
                    ∧ gen(S,R) ≥ gen(主仓,R)                          # v8 (RM-2): 跨腿代差 ⇒ 不判 (假红防)
      ```
      **主仓侧基准分支零猜测**: 用主仓 scan 的 `current_branch`; `refs/remotes/R/{current_branch}` 缺失 ⇒ skip 记 `no_published_ref` (不猜 HEAD/main)。**主仓 detached HEAD (current_branch=None, CI checkout 态) ⇒ 全部 (R,S) skip + 记可见 reason** (backend m-3)。**前提: Fetch 1 --prune** (3.1)
- [x] 13.2 🔴 **定义域八分支逐一落位 (v8; 横扫表 v8 行为 SOT, 5.1d 闸校验)**:
      1. C 缺失 ⇒ `no_published_ref` skip 可见 (含主仓 detached)
      2. **path 非 gitlink (ls-tree mode ≠ 160000)** ⇒ `not_a_gitlink` skip 可见 — v8: rev-parse 对普通目录 rc=0 返 tree sha, **不能按 rc 探** (R7 backend M-1 实测)
      3. S 未 init ⇒ `uninitialized` skip 可见
      4. shallow(S) ⇒ `shallow_unverifiable` 可见非阻断 — 定性 (hunter m-3): 「unshallow 可知但代价不成比例, **有意豁免**」(非「不能知道」), 输出可见
      5. ¬豁免资格(S,R) ∨ ¬豁免资格(主仓,R) ∨ gen 序不满足 ⇒ `orphan_unverified` — 不判 (陈旧/时序假象防); **D18: 连续 ≥ k_eff 代 ⇒ 升级 blocking**
      6. **contains rc=129 (no such commit/bad object) ∧ 豁免(S,R)** ⇒ **orphaned 候选** (G 无处存在比只缺镜像更重, 不得落 soft-error — R7 backend C-4 严重度倒挂防)
      7. 其它 rc≠0 (S 仓损坏等) ⇒ soft-error 可见
      8. **S 无 remote R** ⇒ `no_matching_remote` 可见非阻断 (R7 RM-3: 与真 orphan 在 contains 原语层同像 [rc=0 空输出], **必须在 leg 枚举层先行区分**, 不可依赖 contains 结果)
- [x] 13.3 **裁决接线**: `gitlink_orphaned(R) == true` ⇒ 进 F4′ **blocking** ∀ 子句; `multi_remote_drift` 建议文案「主仓在 R 上引用的子模块 commit 在 R 上不存在 — 从 R clone --recursive 会断裂。修法: git -C S push R <branch>」 (✅ Phase 4 收口, v1.62.0)
- [x] 13.4 **gitlink 层独立结构 (v8 — R7 RM-10; v9 补计数器语义)**: 🆕 **双分区计数器写死 (8M-6)**: parity 层 `consecutive_unverified` 键 = (repo, remote) 按腿计 (stale_unverified +1, **清零绑「本 scan 该腿 fetch 成功」且先序在豁免判定前** [D20]); gitlink 层同名字段键 = (R, S) 按对计 (orphan_unverified +1, **清零绑「本 scan 该对完成裁决 (status ∈ {ok, orphaned})」** — 非证据资格; 一腿多子模块各对独立计数)。`豁免资格(r)` 只读 per-leg 份。上述状态**不进 parity.reason 枚举** (与 AC-16「完全不经 parity 表达」一致 — 进 reason 会被 `blocking_unknown` 补集全判 blocking, 与 13.2 的「skip/不判」字面矛盾)。新增 snapshot 字段 `multi_remote.gitlink_integrity[]` per-(R,S): `{remote, submodule, status ∈ {ok, orphaned, orphan_unverified, no_published_ref, not_a_gitlink, uninitialized, shallow_unverifiable, no_matching_remote, soft_error}, consecutive_unverified}`。**F4′ 补「gitlink 层裁决」小节逐格填**: `orphaned` ⇒ blocking (∀ 子句); `orphan_unverified ∧ consecutive ≥ k_eff` ⇒ blocking (D18); 其余全部 benign-可见 + 各自理由。机械检查: **status 枚举 ⊆ 裁决表已登记格** (blocking ∪ benign-可见 全覆盖, 补集断言)。schema doc + 横扫表同步
- [x] 13.5 **依赖 F3′ 新鲜度**: contains 判定读的是**本地 remote-tracking refs** — 只有 F3′ fetch (--prune) 后才反映远端现实; leg ¬豁免资格 ⇒ 13.2 的 unverified 分支 (与 D15′ 代际窗联动 [v9: D15 已废])
- [x] 13.6 ⚠️ **行为变更公示 (CHANGELOG 显著标注)**: (1) 事故形态下 `overall_parity` true→**false** — 有意; parity 语义 (含 `ahead` 非阻断) **零变更**; (2) 🆕 v8: **Fetch 1 带 --prune** — 本地化石 remote-tracking ref 会被清理 (只影响 remote-tracking 命名空间, 不碰本地分支); (3) 🆕 **已知盲窗** (backend m-4): C 锚定 current_branch ⇒ feature 分支期间 (未推 R 的分支) 该 R 的 orphan 检查记 no_published_ref 休眠, master 上既有 orphan 不被检出 — 两次真实事故都在 master+scan-on-master, 可接受, 显式声明防未来审计员当缺陷重报; 锚定集扩展 ({current_branch} ∪ R 上实际存在的默认分支 ref, 仍零猜测) 记为 Phase B 可选增强 (hunter m-1)
- [ ] 13.7 **性能**: contains 检查纯本地 (无网络), per (R,S) 一次 `branch -r --contains`; 60 腿仓 ≤ 秒级 — 落 §承重性能实测 附表 (TODO: 「per (R,S) 一次 branch --contains, 60 腿仓 ≤ 秒级」的承重性能实测附表未找到 (schema doc/proposal 均未见性能测量数据表))
- [x] 13.8 **golden fixture 重新采集** (`tests/fixtures/reference-snapshot-aria.json` 采自事故现场, F10″ 下该现场应报警 — 必须换镜像修复后的健康态重采, 并另存事故态为 AC-16 fixture)
- [x] 13.9 **AC-16/AC-17 四分支 fixture 见 2.15/2.16** (含反惯例 trunk 分支 fixture — 锁零分支名假设)

### ~~F10′ 原方案~~ **SUPERSEDED (R6 证伪) — 勿实施, 保留仅供溯源**

> 🔴 **R6 三方独立证伪**: F10′ 要修的事故在 git 眼里是 **`ahead`** 不是 `behind` (`rev-list --left-right` → `2 0`), 而 `ahead` 的非阻断性被 **AC-8/D7 + golden fixture + AB rubric** 三重锁死 ⇒ **F10′ 上线后 `overall_parity` 仍是 `true`**。
> 另有 C-2 (`{HEAD,master,main}` 是又一个正向枚举; 实测三个子模块的 `refs/remotes/github/HEAD` **全不存在**) + C-3 (伪码丢了 shallow 守卫) + M-4 (pin 住的子模块恒红)。
> ✅ **owner 裁定: 换原语 → F10″ (见上)。** 证据: [R6 报告](../../../.aria/audit-reports/post_spec-R6-2026-07-12T2300Z-state-scanner-stale-refs-false-parity-aggregated.md)。

### ~~以下为 F10′ 原任务, 保留仅供溯源~~

> **R5 的决定性发现**: R1-R4 反复打磨 F4′ 的**裁决公式**, 但从未问过「**这个公式要裁决的 `parity` 值, 真的会被生成出来吗?**」
> 答案: **对 detached-HEAD 子模块 (子模块的规范常态), 不会。** 一个完美的裁决公式, 裁决的是一个**从不存在的输入**。

- [ ] 13.1 🔴 **`_remote_parity_local_refs` (`multi_remote.py:148-183`) 在 `branch is None` 时不再早退**:
      ```python
      # 今天 (:169): 在触碰任何 remote-tracking ref 之前就返回, 对每一个 remote 都一样
      if branch is None:
          base["reason"] = "detached_head"
          return base
      ```
      ⇒ **无论 F3′ 把 github 的 ref fetch 得多新鲜, 这个函数从未看过它一眼。网络成本已经付了, 但比较从未发生。**
- [ ] 13.2 **改走 commit-based 比较** (**不是发明新机制** —— 复用 `sync.py:200-330` 已验证可工作的算法, 只是把它从「硬编码 origin」参数化到任意 remote):
      ```
      if branch is None:                       # detached HEAD (子模块常态)
          remote_ref = 首个存在者 of refs/remotes/{remote}/{HEAD,master,main}
          if 不存在:  reason = "no_remote_head_ref"; parity = "unknown"   # → blocking (fail-CLOSED)
          else:
              behind/ahead = git rev-list --left-right --count local_head...remote_ref
              parity = equal | behind | ahead | diverged                   # ← 真 parity, 不再是 unknown
      ```
- [ ] 13.3 **`sync.py:36-41` 的 `_ORIGIN_HEAD_REFS` 硬编码只查 origin** ⇒ 参数化为 per-remote fallback 链 (与 13.2 共享同一实现, **不得两处各写一份** —— 否则又是「两个平行计算点」)
- [ ] 13.4 **新 reason `no_remote_head_ref` 归 blocking 桶** + 登记进 F4′ 裁决表 + schema doc enum + **5.1d 谓词横扫表**
- [ ] 13.5 **`detached_head` 保留在 benign ① 桶** (为 `ls_remote` 路径 `:250/:293` 与 shallow 交叉场景兜底), 但**默认路径 (`local_refs`) 上它不再产生 `unknown`**
- [ ] 13.6 ⚠️ **行为变更公示 (CHANGELOG 显著标注)**: `overall_parity` 在**本仓当前状态**下会从 `true` 变 **`false`** (若 github 镜像落后)。**这是有意的 —— 也正是本 Spec 存在的理由。**
- [ ] 13.7 **对偶检查 (防 F10′ 自己过冲成恒红)**: F10′ 让子模块**能产出 `equal` 正证据** (今天它连 `equal` 都产不出来) ⇒ 方向是**从恒 unknown 走向可判定**, 不是走向恒红。**AC-16 (真落后必报) + AC-17 (真一致必 true) 成对验收**
- [ ] 13.8 **golden fixture 重新采集** (`tests/fixtures/reference-snapshot-aria.json` 现记子模块全 `equal` —— 采自事故现场, 且在 F10′ 下语义完全不同)

> **活体证据 (2026-07-12, 本 Spec R5 审计当天, 本仓自己复现)**:
> ```
> scan.py:  overall_parity: true                            ← 报「已同步」
>           standards github parity=unknown reason=detached_head
> ls-remote: standards gitlink=79b7cd6 / origin=79b7cd6 ✅ / github=9df1722 ❌ 落后 2 commit
>            aria-orchestrator gitlink=8b947fa / origin=8b947fa ✅ / github=daf7c79 ❌ 落后 2 commit
> ⇒ 主仓 master (已在 GitHub 上) 引用的两个 gitlink 在 GitHub 上根本不存在
> ⇒ `git clone --recursive` from GitHub = 断裂, 而 state-scanner 报「已同步」
> ```
> 与 **CLAUDE.md 记载的 2026-04-10 事故** (aria v1.11.1 发版后未推 GitHub, 市场版本滞后) **同一模式** —— **本项目已发生两次, 不是假想。**
