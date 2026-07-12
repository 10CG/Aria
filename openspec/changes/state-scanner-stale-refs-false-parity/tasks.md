# Tasks: state-scanner 陈旧 ref 假同步修复 (v4 — 拆分后的核心机制)

> **Spec**: [proposal.md](./proposal.md) | **Level**: 3
> **Status**: Draft v4 (v1→R1 FAIL→v2→R2 FAIL→v3→R3 FAIL→v4 + 拆 Spec; 待 R4 收敛 → A.2/A.3 lock)
> **范围**: **仅核心机制** (F1′/F2′/F3′/F4′/F5′/F6′/F9′)。Rule #7 → [姊妹 Spec B](../state-scanner-snapshot-stderr-secret-leak/); `issue-cache-freshness` → [姊妹 Spec C](../state-scanner-issue-cache-freshness-assertion/)。
> **编号不可变**。v1/v2/v3 编号已作废 (两次机制重写 + 一次拆分)。

---

## 1. 前置裁决 (Phase A 内锁死, 不留给 Phase B 即兴)

- [ ] 1.1 **OQ-A**: `read_only_remotes` 默认值 (倾向 `[]`, 不自动推断)。**必须与 2.7 的非空护栏捆绑裁定**
- [ ] 1.2 **OQ-B**: `coordination_fetch` 块 shape (倾向: 保留原块 + 另开 `remote_refresh` 新块 = 纯 additive)
- [ ] 1.3 **OQ-C**: 离线 debounce (倾向: 不造新机制, 用 `has_unreachable_remote` gate 建议层)
- [ ] 1.4 **OQ-D**: `freshness_window` 默认 (倾向 300s; 须 > TTL 30s 且 > scan 全程 17.6s)
- [ ] 1.5 🆕 **OQ-E**: F9′ 二选一 —— **必须锁死** (US-008 数据丢失护栏在此路径; AC-10 的断言字段跟着定)
- [ ] 1.6 **enforced_remotes 命名空间**: 必须对齐 `phase-c-integrator/SKILL.md:574` 已发布的**顶层 `multi_remote.*`** 跨 skill 契约。**不得另立门户** (否则 state-scanner 与 phase-c-integrator 对「该强制的 remote 集合」产生 split-brain = 本 Spec 的病在跨 skill 层复现)
- [ ] 1.7 `multi_remote.py` **绕过 config-loader** (直读 `.aria/config.json`, 默认值来自代码内常量) ⇒ 接上或显式声明 (决定 `DEFAULTS.json` 对本 collector 是否真是 SOT)
- [ ] 1.8 **schema SOT**: 真 SOT = `references/state-snapshot-schema.md` (**AD-SSME-6**, `validate_schema_doc.py` 机械强制)。`multi_remote.py:4` 的 "canonical SOT is git-remote-helper" 是**被取代的 stale docstring** ⇒ 改 docstring 指向真 SOT。**不得**把 SOT 迁到代码 (会推翻 AD-SSME-6 并架空 validator)
- [ ] 1.9 fetch 并发: **per-host 上限** (默认 ≤4/host) + 丢连重试退避 + **全局 `refresh_deadline_seconds`** (默认 15s)。**删除 `fetch_all: false` 旋钮** (`enforced_remotes: ["origin"]` 已够; 不为收窄 fetch 发明第 4 个键)

## 2. 红测试先行

> 命令: `python3 aria/skills/state-scanner/tests/run_tests.py`

- [ ] 2.1 **一次性缺陷证据**: 往既有 `test_multi_remote_mocked.py:685` `test_local_refs_stale_flag` 加 `overall_parity` 断言 —— 它**早已构造事故 fixture**, 只是从没断言那个会暴露矛盾的字段 (跑出 `local_refs_stale=True` 而 `overall_parity=True`)。**⚠️ 豁免 2.9 设计闸** (F2′ 退役 `local_refs_stale` 后它注定转不绿), 由 **12.3** 重写
- [ ] 2.2 **AC-1**: remote 不可信 + 真实落后 → `parity != equal` ∧ `reason == "not_refreshed"`
- [ ] 2.3 **AC-2**: origin 刷新成功且 equal + github fetch 失败且真落后 → github `unknown` + network 类 reason + `overall_parity: false`。**fixture 钉死: github 无窗口内成功 `fetched_at`; 用 mock `_run` 注入精确 stderr, 不打真实域名** (实测 TLS 失败 stderr 是 `gnutls_handshake() failed`, 不落在任何已知 pattern ⇒ 真实网络会环境相关误判)
- [ ] 2.4 **AC-6**: 子模块 remote 从未 fetch → 不得提供 `equal` 正证据
- [ ] 2.5 **AC-7**: 不可信且 `behind` 不得降级; 不可信且 `ahead` 不得让 `has_pending_push` 变 false
- [ ] 2.6 **AC-8**: 有未推送 commit 的健康仓 → `overall_parity` 仍 true
- [ ] 2.7 🆕 **AC-11 (防 R3-C5 恒红)**: **detached-HEAD 子模块** + 全部 remote 刷新成功 + 主仓 equal → `overall_parity` **仍 true**。**本仓可直接 dogfood** (`aria` 子模块正是 detached)
- [ ] 2.8 🆕 **AC-12 (防 R3-N1 vacuous true)**: 空参与集 (零 remote / 全 read-only) → **必须 false**; 无任何 `可信 ∧ equal` (单 remote 且 ahead) → **必须 false**
- [ ] 2.9 🆕 **AC-13 (两轴独立)**: fetch 失败(auth) 但 `fetched_at` 仍在窗内 → parity **不降级**, **但** `error_kind` 记录 ∧ `has_unreachable_remote: true`
- [ ] 2.10 **AC-9 (TTL)**: 30s 内连跑两次 → TTL 命中 → 不降级 + diff==0; fetch 失败 + stale cache → `fetched_at` 不推进
- [ ] 2.11 **AC-10 (F9′)**: origin fetch 失败时 `current_branch` 与 `multi_remote[origin]` 不矛盾 (**断言字段由 OQ-E 定**)
- [ ] 2.12 🆕 **AC-5 (v4 拆分时把任务弄丢了 — R4 code-reviewer X-6)**: `tracks_multibranch` 中**与 HEAD 同分支**的 track commit 对 HEAD 不可达时 ⇒ `overall_parity == false` 或该 remote `reason` 非空。**这恰恰是本 Spec 叙事的起点** (「同一份 snapshot 自相矛盾 = collector 编排缺陷的指纹」)。无任务 ⇒ 会作为「**AC 勾了但从没实现**」ship = **本仓刚 ship 的 #95 归档门会 block 它**
- [ ] 2.13 确认 2.2-2.12 在**未修改代码**上全部 RED。任一意外 GREEN ⇒ 诊断有误, **回 Phase A**
- [ ] 2.13 **设计闸**: 修复后若任一红测试 (2.1 除外) **仍无法转绿** ⇒ 设计缺陷, **回 Phase A**

## 3. F3′ — 新鲜度靠获取 (`remote_refresh`)

- [ ] 3.1 `coordination_fetch` 泛化 + **改名 `remote_refresh`**: fetch **所有 enforced remote** (主仓 + 全部子模块)
- [ ] 3.2 **改名波及 ≥11 个引用点**, 逐一处理: `normalize_snapshot.py` / `renderers/track_board.py` / `lib/coordination_ref.py` / `collectors/__init__.py` / `scan.py` / `tests/test_coordination_fetch.py` / `tests/test_p1_layer_h.py` / `SKILL.md` / `state-snapshot-schema.md` / `phase-1-collectors.md` / `docs/rule9-5layer-matrix.md`
- [ ] 3.3 **`fetch_ok` 锚定 Fetch 1** (#141 two-fetch 语义)。**benign-missing 的 `refs/aria/coordination` 不得置 `fetch_ok=false`** —— github/子模块远端几乎必然没有它, 否则**每个非-origin remote 恒 false ⇒ 恒红**
- [ ] 3.4 **非交互契约**: `stdin=DEVNULL` + `GIT_TERMINAL_PROMPT=0` + `GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=N"`; auth 失败**只提示一次**
- [ ] 3.5 并发: 全并行 + per-host 上限 + 丢连重试退避 + **全局 deadline** (超时 leg ⇒ `not_refreshed`, 走既有降级路径, **零新机制**)
- [ ] 3.6 snapshot 记 per-remote `{fetched_at, fetch_ok, error_kind}`。`error_kind` **复用姊妹 Spec B 的分类器** (枚举, 永不含 stderr 原文)
- [ ] 3.7 **`fetched_at` 只在 Fetch 1 真成功刷新时推进** —— stale-serve/degraded (`coordination_fetch.py:379-390` 现返回 `cached:True` + 任意陈旧 `last_fetch_at`) **不得**推进
- [ ] 3.8 **TTL 命中时逐 remote replay** per-remote map (现 cache schema 只有 3 个标量键, **无 per-remote 结构**)
- [ ] 3.9 **落点 Phase 0.5** (`collect_git_state` 之前) —— 否则 `git.upstream.behind`(陈旧) 与 `sync_status.current_branch.behind`(新鲜) 在同一 snapshot 打架
- [ ] 3.10 逐一核对全部 15 个 collector 的先后依赖
- [ ] 3.11 **SKILL.md 写死可关闭性契约**: 「关闭 `remote_refresh` ⇒ 所有 parity 变 unknown」
- [ ] 3.12 fetch 结果缓存**原子写** (tmp+rename) —— 它现在承载**裁决输入**
- [ ] 3.13 **跨进程同仓并发** (两个终端同时 scan) 写明为**已知可接受降级**: 依赖 git 自身 ref lock; 争用 ⇒ `fetch_ok=false` ⇒ 降级 unknown (**假红方向, 可接受**)。否则 dogfood 时会被当 bug 追

## 4. F1′ — 两个正交轴

- [ ] 4.1 **可达性轴**: `fetch_ok == false` (本次尝试) ⇒ **永远**记 `error_kind` + 按 network 类置 `has_unreachable_remote`。**与窗口无关**
- [ ] 4.2 **新鲜度轴**: `可信(r) := now - fetched_at <= freshness_window` ⇒ **只** gate parity 降级
- [ ] 4.3 **降级只作用于 `equal`** → `unknown` + `reason: not_refreshed`; `behind`/`diverged`/`ahead` **原样保留**
- [ ] 4.4 `reason` 优先级: **后置降级只在 parity 本会是 `equal` 时改写** —— 不覆盖 `detached_head` / `shallow_clone` / `no_local_tracking_ref`
- [ ] 4.5 `reason` enum 补齐 schema (代码已发 `rev_list_failed` / `rev_list_parse_failed`, 未记录)

## 5. F4′ — `overall_parity` 裁决表 (核心)

- [ ] 5.1 🔴 **`benign_unknown` 必须按「fetch 能否改变它」再分一层** (R4 化解 tech-lead ↔ backend-architect 的正面冲突; 代码实测):
      ```
      benign_unknown(r) := parity(r)=="unknown" ∧ (
            reason(r) ∈ {detached_head, shallow_clone}                      # ① fetch-无关 (:169/:173 在读任何 ref
                                                                           #    之前就返回) ⇒ 恒 benign, 不看可信
         ∨ (reason(r) ∈ {no_local_tracking_ref, remote_branch_missing}      # ② fetch-依赖 (:181 是"读 ref 失败"才返回)
              ∧ 可信(r))                                                    #    ⇒ 只有本次刷新成功才 benign; 否则
        )                                                                   #    「没这个 ref」可能只是「我们没 fetch 过」
      ```
- [ ] 5.1b 🔴 **`blocking_unknown` 必须 fail-CLOSED (兜底反向定义), 不得写成正向枚举** (R4 **四方独立收敛**):
      ```
      blocking_unknown(r) := parity(r)=="unknown" ∧ ¬benign_unknown(r)
      ```
      ⚠️ v4 初稿写成 `reason ∈ {6 个显式值}` ⇒ **任何未列举值 fail-OPEN (不阻断)**。实测可达的漏网之鱼:
      - **`reason = None` + `parity = unknown`**: `multi_remote.py:308/312/317` **三条 best-effort 返回路径**
      - **`parse_error`** (`:281`)
      - **姊妹 Spec B 分类器的兜底值** `unknown` / `git_error` / `permission_denied` / `timeout` —— backend-architect 用**真实 `git fetch` 连接失败**复现: 其 stderr **一个已知 pattern 都没中** ⇒ 落 catch-all ⇒ 按正向枚举**不阻断**
      ⇒ **同一不变量的第五次复发**。**教训: 「把不变量写进文档」≠「把它写进兜底默认值」。**
- [ ] 5.1c 🆕 **机械防漏格 pin 测试** (把「逐格填」从纪律变成机制): 构造一个**代码里不存在的** reason 值 ⇒ **必须阻断**。断言公式实现走 `¬benign` 兜底而非正向 blocking 枚举
- [ ] 5.2 **公式** (⚠️ `∀` 里**没有**独立的 `可信(r)` 项):
      ```
      overall_parity = (enforced_set ≠ ∅)                             # 防 vacuous true (Python all([])==True)
                     ∧ (∃ r: 可信(r) ∧ parity(r)=="equal")            # QA-C1 正证据 —— 可信只需在此出现
                     ∧ (∀ r: parity(r) ∉ {behind,diverged} ∧ ¬blocking_unknown(r))
      ```
      **`可信(r)` 从 ∀ 删掉的理由** (qa-engineer R4 实证): 它在那里冗余且有害 —— 对 `equal` 的 r, F1′ 降级**已经**把不可信的变成 `not_refreshed`(∈blocking) 挡住了; 对 `behind`/`ahead` 的 r, 新鲜度**没有正确语义** (下界仍为真); 对 benign 的 r, 会让「该 remote 恰好这次 fetch 失败」把 `overall_parity` **拖成恒红**
- [ ] 5.2b 🆕 **AC-11b**: benign_unknown (fetch-无关类) 的 remote **自身 fetch 失败** ⇒ `overall_parity` **仍不受它阻断** (只要其它 remote 提供 `可信 ∧ equal`)。**现有 AC-11 只测「全部刷新成功」, 没覆盖这一格**
- [ ] 5.3 `ahead` 不阻断, 经 `has_pending_push` 单独承载 (对 `multi_remote.py:400-402` 既有决策的**保留**; 三处证据一致: 代码注释 / golden fixture / AB rubric)
- [ ] 5.4 **「分支未发布」拆出独立 flag** `has_unpublished_branch` —— 不压在 `overall_parity` 上。**把三种语义挤进一个 bool 正是它今天撒谎的原因**
- [ ] 5.5 更新 `_aggregate_flags` docstring: **三次违反并列** (零证据 / 陈旧证据 / 从未获取) + **对偶不变量** (假绿的反面是恒红) + **unknown 二分表**

## 6. F5′ — enforced remote 集合

- [ ] 6.1 消费既有键 `enforced_remotes` / `read_only_remotes` (**按 1.6 的命名空间裁定**)
- [ ] 6.2 **read-only 排除同时作用于** `overall_parity` **和** `has_unreachable_remote` **和** `multi_remote_drift` 触发 —— 只挂 `overall_parity` 会让「我不关心它」的 remote 抖一下网络仍全局告警
- [ ] 6.3 **修假文档** `sync-detection.md:515`
- [ ] 6.4 **CHANGELOG 显著标注**: 已设 `enforced_remotes` 的采用者其配置**今天是惰性的**, 本 Spec 让它承重 ⇒ **直接改变网络行为**

## 7. F2′ — 退役 mtime 实现 (保留概念)

- [ ] 7.1 退役 `local_refs_stale` / `warn_after_hours` 的 FETCH_HEAD-mtime 路径
- [ ] 7.2 **无条件清扫 ≥8 处 SOT** (⚠️ v2 曾把条件写反成「若保留才清扫」—— **退役 = 死配置键, 清扫更必须**): `config-loader/DEFAULTS.json:38` / `.aria/config.template.json:21` (**采用者模板**) / `.aria/config.json` / `config-loader/SKILL.md:79` / `sync-detection.md` ×4 / `git-remote-helper/schema.md:58` / `state-snapshot-schema.md:490`
- [ ] 7.3 清理 `_scan_repo` 的 `stale` 死返回值

## 8. F9′ — `sync.py` 平行计算点 (按 OQ-E 裁定)

- [ ] 8.1 `_collect_current_branch` 按 1.5 的裁定处理 ((a) 消费新鲜度 / (b) 声明本地视角 + 输出区块区分)
- [ ] 8.2 `sync_status.submodules[].drift` 的 `remote_commit`/`behind_count`/`hint`/`hint_type` 从陈旧变新鲜 ⇒ 核 `submodule update --remote` 建议触发的变化。**US-008 数据丢失护栏在此路径** (`sync.py:312-328` directional guard)
- [ ] 8.3 `sync.py` 从不读 `sync_check` config, 而 `phase-1-collectors.md:34` 声称可关闭 ⇒ 修代码或修文档
- [ ] 8.4 `remote_refs_age` 在 F3′ 后恒 "1m" ⇒ 标注废弃或删除

## 9. 下游消费者

- [ ] 9.1 `handoff_autofill.py:52` 把降级后的 `reason` 升级为 warning —— 否则 F1′ 的 `unknown` 被 session-closer **静默吞掉** = 新假绿通道
- [ ] 9.2 `multi_remote_drift` 建议**按 ≥6 种成因分派** (behind/diverged→pull / ahead→push / benign unknown→**不触发** / no_local_tracking_ref→`has_unpublished_branch` / not_refreshed·network·auth→查网络凭据)。**不是一律 fetch/pull** (US-008 directional guard)
- [ ] 9.3 `multi_remote_drift` 规则**无去重/冷却** (grep 零命中) ⇒ 按 OQ-C 处理
- [ ] 9.4 **`aria-2.0-m7-fleet-aggregation` (Approved) 消费 `overall_parity`** ⇒ 语义变更需同步该 Spec (其 TB-health-3 pin 到 schema doc)
- [ ] 9.5 重新生成 golden fixture `tests/fixtures/reference-snapshot-aria.json` (现记 `overall_parity: true` + 子模块全 `equal`, 采自事故现场)
- [ ] 9.6 `validate_schema_doc.py` **会真跑 scan.py** ⇒ F3′ 后每次校验触发全量网络 fetch。加 offline/mock 模式; 且它只校验 top-level key, per-remote 嵌套字段无守护
- [ ] 9.7 **测试套件本身**: `test_two_consecutive_runs_diff_zero` **真跑两次 live `scan.py` 子进程** ⇒ F3′ 后单测每跑一次打 8 条网络腿 ×2。加 offline 旁路 (如 `ARIA_SCAN_OFFLINE=1`)

## 10. 文档同步 (Rule #3)

- [ ] 10.1 `references/state-snapshot-schema.md` (**真 SOT**): per-remote 字段 + `reason` 枚举 + **unknown 二分** + `overall_parity` 新公式 + **`freshness_window` 是有意的有界陈旧容忍 (≤5min), 与本 Spec 修的无界陈旧 bug 是两个量级 —— 不要被未来审计员误认成同一缺陷复发**
- [ ] 10.2 `SKILL.md`: collector 顺序 (Phase 0.5) + 网络行为 + 性能预期 + 可关闭性契约
- [ ] 10.3 `references/phase-1-collectors.md` / `sync-detection.md`
- [ ] 10.4 `references/output-formats.md`: 🔄 区块呈现不可信 remote + `overall_parity: false` 的**成因分派**
- [ ] 10.5 `RECOMMENDATION_RULES.md` **+ `references/rules/basic-rules.md:69-82`** (规则定义在**两处**; `:78` 注释写死旧语义)
- [ ] 10.6 **`docs/architecture/system-architecture.md:892-895`** (主仓 L1 架构文档, **且已 drift**: 记 `overall_parity` 为枚举, 代码发 bool)
- [ ] 10.7 `config-loader/SKILL.md:79` + `DEFAULTS.json` + `.aria/config.template.json`
- [ ] 10.8 CHANGELOG: 网络行为变更 + parity 语义 + 惰性配置变承重 + opt-out 方法 + **不把 +4% 写成通用承诺**

## 11. Rule #6 (不可协商) — Skill benchmark

- [ ] 11.1 `/skill-creator` benchmark (with/without AB), 结果存 `aria-plugin-benchmarks/ab-results/`
- [ ] 11.2 **修 AB rubric** `ab-suite/state-scanner.json:143` —— 现明写 `"Should exclude parity: ahead and parity: unknown from overall_parity computation"`。v4 下 **ahead 排除 ✓ 但 unknown 需二分** ⇒ rubric 必须精确化, 否则会把正确的新行为判为错

## 12. 验证与收尾

- [ ] 12.1 §2 全部红测试转 GREEN (2.1 除外)
- [ ] 12.2 **无回归**: `run_tests.py` → 0 failed ∧ 无既有绿测试转红 ∧ 新增测试数 = N
- [ ] 12.3 处理会机械性破裂的既有测试: `test_local_refs_stale_flag` / `test_scan_with_two_remotes_local_refs` / `test_full_main_repo_flow_with_config_overrides`
- [ ] 12.4 **AC-3**: mock `_run` 断言「每个 (repo,remote) 恰好 fetch 一次」(**集合/计数不变量, 非 strict order** —— 真并行下调用序由线程调度决定)
- [ ] 12.5 **dogfood (本仓)**: `aria` 子模块 detached-HEAD ⇒ `overall_parity` **仍 true** (AC-11); `aria-orchestrator` github 镜像若落后 ⇒ **必须报出来**; `sync_status` 与 `tracks_multibranch` 不再自相矛盾
- [ ] 12.6 归档语料 sweep 无新 block
- [ ] 12.7 **跨仓落地**: aria-plugin PR → merge → **submodule pointer bump 到 post-merge master SHA** (C.2.4.5 block-default gate) → 主项目 `VERSION` → **多远程推送 (origin + github, 两仓)**
- [ ] 12.8 版本 bump + 5 处 SOT 同步 + 主仓 badge
- [ ] 12.9 释放 track claim
