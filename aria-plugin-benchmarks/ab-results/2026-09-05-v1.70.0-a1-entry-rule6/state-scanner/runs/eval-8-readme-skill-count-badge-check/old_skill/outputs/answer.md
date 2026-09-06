先说结论前的一个前提校正 —— 它会影响你下面每一条判断:

> **本仓 `aria/.claude-plugin/plugin.json` 当前版本是 `1.69.1`，不是 v1.14.0。** 根 README badge、aria/README、i18n README、架构文档版本行全部指向 1.69.1，工作区也没有任何 SKILL.md 变更 (`changes.skill_changes.detected = false`)。所以「刚发布 v1.14.0 + 新增 3 个 Skill」这个前提在本仓状态里找不到对应物。若你说的是另一个仓 / 另一个时间点的状态，请确认后我按那个基线重扫。
>
> 不过你要查的三件事本身仍然成立，而且**其中一件真的有漂移**。

Step 0 已机械执行 `scan.py`（exit **0**，`errors[] = []`，snapshot schema 1.0，采集于 2026-09-05T23:20:13Z）。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/a1-entry-claim-duplicate-work-guard (detached: 否)
  模块: — (UPM 未配置)
  Phase/Cycle: — (UPM 未配置; workflow-state.json 为已完成记录, 见下)
  变更: 4 个 (3 个 dirty 子模块 aria/standards/aria-orchestrator + 1 个未跟踪目录 ab-results/2026-09-05-v1.70.0-a1-entry-rule6/)
  OpenSpec 关联: a1-entry-claim-duplicate-work-guard (approved)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.8h ago, via pointer, status=active, phase=B.2)
  git 操作中: 无 (operation=none, 无冲突)
  中断状态: .aria/workflow-state.json 为 status=completed 的旧记录
            (spec_id=linked-issue-field-availability, 停在 D.4; git_anchor.branch=master
             与当前分支不匹配) → 非中断, 不触发 Resume/Abandon 分支

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: other × 4 (code 0 / test 0 / docs 0 / config 0)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 不适用 (无代码变更)
  Skill 变更: 未检出 (needs_benchmark 空 — 本次不触发 Rule #6)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved)
  User Stories: 21 个 (done 17, in_progress 2, approved 1, pending 1)
  OpenSpec 覆盖: — (snapshot 不产出该比率字段)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active | 最后更新: 2026-09-02
  需求链路: ✅ 完整 (PRD v1 + v2 → Architecture)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 7 个 (全部 approved)
  已归档: 142 个 | 待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred, 设计定稿但实施未做, 勿误判完成)
    - aria-2.0-m6-release-closeout (approved, 41/41 未勾, staleness 103d)
    - aria-2.0-m7-agent-lifecycle   (approved, 18/18 未勾, staleness 65d)
    - aria-2.0-m6-cost-model-telemetry (approved, 25/38 未勾, staleness 58d)
    - aria-2.0-m6-e2e-resilience    (approved, 25/40 未勾, staleness 55d)
    - aria-2.0-m7-fleet-aggregation (approved, 20/20 未勾, staleness 48d)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 off)
  上次审计: pre_merge — PASS (converged=false, R5, 2026-09-02T18:10:11Z)
            报告: .aria/audit-reports/pre_merge-R5-...-linked-issue-field-availability-aggregated.md

🔧 自定义检查
───────────────────────────────────────────────────────────────
  ✅ 14/14 全部通过 (0 FAIL / 0 SKIP)，与本次提问直接相关的四条:
    ✅ m6-version-badge-match: OK badge=1.69.1
    ✅ plugin-version-arch-docs-match: OK plugin=1.69.1 (2 处架构文档版本行一致)
    ✅ i18n-readme-translation-currency: OK (3 份 i18n README 均 @1.69.1)
    ✅ plugin-cache-currency: OK installed=1.69.1 (scope=user) sot=1.69.1
    ✅ main-project-version-consistency: OK 主项目 1.7.5 — 9 个引用点全部一致

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: ahead 0 / behind 0 vs origin/feature/a1-entry-claim-duplicate-work-guard
  多远程 parity: ✅ overall_parity = true (enforced: origin + github, 新鲜度 fresh, 缓存 1m)
    主仓 5d9b568 — origin equal / github equal
    standards bb5d375 — 两端 equal
    aria      ab3dbd0 — 两端 equal
    aria-orchestrator 92acce5 (分支 feature/m6-cost-model-telemetry) — origin equal /
      github unknown (no_local_tracking_ref, 属另一条 track, 非本轨问题)
  gitlink 完整性: ✅ 6/6 ok (3 子模块 × 2 remote, 无 orphaned)

  📝 README 版本一致性 ← 你问的第三件事
    ✅ Plugin badge: 一致 — README.md:8 `Plugin-v1.69.1` == plugin.json `1.69.1`
    ✅ aria/README 版本: 一致 — readme_version 1.69.1 == plugin_version 1.69.1
    ℹ️ 根 README 无 `**版本**:` 行 (snapshot readme.root.version = null)，
       主项目版本走 README.md:241 `Project Version: 1.7.5` + VERSION，
       由探针 main-project-version-consistency 覆盖，9 个引用点全一致

  📦 插件依赖: ✅ standards 子模块已注册且已初始化

  🔗 Forgejo 配置: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但配置缺失
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues
───────────────────────────────────────────────────────────────
  open_count: 47 (来源 cache, 拉取于 2026-09-05T23:19:26Z, 平台 forgejo)
    10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  ⚠️ 计数不可信下限: config `issue_scan.limit = 20`，Aria 与 aria-plugin 恰好各报 20 =
     顶到上限且无截断标记 (上次 handoff §2 M2 已实测 46 vs 真实 65)。真实 open 数 > 47。
  近期关键: Aria#196 (Layer1→2 env 三腿契约) / Aria#195 (handoff_multibranch basename bug) /
            Aria#193 (owner-container 身份漂移) / Aria#188 (四维一致性恒假阳性)
```

---

## 你问的三件事 — 逐条核对

### [1] README 中的 Skill 数量 vs 实际目录 → ✅ 一致 (42)

| 口径 | README 声称 | 实测 | 判定 |
|------|------------|------|------|
| 总数 | `aria/README.md:44` "35 user-facing + 7 internal = **42** total" | **42** 个含 `SKILL.md` 的目录 | ✅ |
| 内部 (`user-invocable: false`) | `aria/README.md:46` 列 7 个 | **7** 个 (agent-router / agent-team-audit / arch-common / audit-engine / config-loader / git-remote-helper / aria-token-telemetry) | ✅ 逐名吻合 |
| user-facing | 35 | 42 − 7 = **35** | ✅ |
| 根 README 交叉引用 | `README.md:242` "42 Skills + 11 Agents" | 42 skills / 11 agents (`aria/agents/*.md`) | ✅ |

计数口径提示: `aria/skills/` 下有 **43** 个子目录，但 `session-closeout/` 只含 `scripts/`、**没有 SKILL.md**（是 `session-closer` 的脚本宿主，不是一个 Skill）。按「有 SKILL.md 才算」的口径才得 42 —— 如果哪天有人用 `ls -d */ | wc -l` 去核这个数，会得到 43 并误报一次不一致。

### [2] Skill 列表是否完整 → ❌ 不完整，漏 2 条

`aria/README.md` 的分组 bullet 清单实际只列了 **40** 条，缺这两个 user-facing Skill:

- **`issue-triage`** — issue 系统化核对 (版本 / 代码路径 / in-flight 分支 / 复现)，产出 triage-report.json
- **`session-closer`** — 会话收尾 leaf skill，写 `docs/handoff/`（与 phase-d-closer 正交，Rule #9 的两个入口之一）

这两条都不在任何分组下（"Ten-Step Cycle Core" / "Requirements" / "Feedback & Reporting" 都没有）。

**这正是本次扫描最该被看见的一点**: 头部计数 `35 + 7 = 42` 是**对的**，清单却少 2 条 —— 33 条 user-facing bullet + 7 条 internal = 40 ≠ 42。也就是说**只核计数不核清单，这个漂移查不出来**；反过来，如果当初是照清单去数的，计数早就该是 33 而不是 35。计数与清单是两个独立的检查项，必须分开跑。

### [3] Plugin badge 版本 vs plugin.json → ✅ 一致 (1.69.1)

- `README.md:8` → `https://img.shields.io/badge/Plugin-v1.69.1-blue`
- `aria/.claude-plugin/plugin.json` → `"version": "1.69.1"`
- 机械兜底 `m6-version-badge-match` 独立复核: **OK badge=1.69.1**
- 相邻同步面同样全绿: `aria/README` 版本行、3 份 i18n README、`system-architecture.md §2.8` + `version-scheme.md` 两处架构版本行、本机已装 plugin 副本 —— 全部 1.69.1

---

## ⚠️ 关于本次核对的方法学，有一件事必须交代

`scan.py` 的 `readme` collector **只产出版本一致性三个字段**（`root.version` / `submodules.aria.readme_version` / `plugin_version` / `version_match`），schema 里**没有 skill 数量、没有 skill 列表**。而 `references/output-formats.md` 的「📝 README 同步状态」区块却写着 `✅ Skill 数量: 一致 (33)` / `ℹ️ Skill 列表: 完整` 两行 —— **这两行在 v3.0 机械化 snapshot 里没有数据源**。

所以上面 [1][2] 两项是我在 snapshot 之外**补测**的（只读 `ls aria/skills/*/SKILL.md` + `grep` README 清单，没有替代任何一个 scan.py 字段的采集）。这构成一个真实的 collector 缺口:

- 输出模板承诺了两个字段，采集端从来没生产过它们 —— 靠 AI 每次临场手数，等于把一条**本该机械化的检查交给了裁量**，而这次恰好就是这条检查抓到了唯一的漂移。
- 建议开单: 给 `collectors/readme.py` 补 `skill_count` / `skill_list_missing[]`（口径钉死为「含 SKILL.md 的目录」，把 `session-closeout/` 这类脚本宿主排除），或者做成一条 `.aria/state-checks.yaml` 自定义检查（与 `m6-version-badge-match` 同一形状，那条已经证明可行）。

另外两条与本次提问无关但值得知道:

- ℹ️ `aria/README.md:7` 声称 "5 Hooks"：`hooks.json` 注册了 6 条 entry / **5 个不同脚本**（session-start-check / handoff-location-guard / secret-guard ×2 / secret-scan / submodule-gate-telemetry），按「不同脚本」口径一致；但 `aria/hooks/host-docker-logout-guard.sh` 存在却**未在 hooks.json 注册**。不是 README 错，是有个脚本没接线，值得确认是有意还是漏了。
- ℹ️ Forgejo 配置缺失（见上）。

---

## 🎯 推荐工作流

上次 handoff（0.8h 前，status=active，phase=B.2）写明本 cycle 在 **31/40**，Group 8 发版三条的执行序是 **8.1 → 8.4 → 8.2**，而 **8.1 的同步面正好包含 `aria/README.md`**。所以 [2] 发现的漏 2 条，天然属于 8.1 的作业面，不建议单开一个 drive-by 提交去修。

```
  ➤ [1] doc-fix: aria/README.md 补齐 issue-triage + session-closer (推荐)
      执行: B.2 (编辑 + 自查) → C.1 (提交)
      跳过: A.* (Level 1 文档修复, 无需 OpenSpec) / B.1 (已在 feature 分支) / B.3 (无架构影响)
      理由: 漂移已定位到字符级 (两条 bullet + 分组归属), 修复面 < 5 行;
            但注意它与 8.1 同一文件, 若你更想一次做完请选 [2]

  ○ [2] 把这条并入 Group 8 的 8.1, 现在只登记不动手
      执行: 在 tasks.md / 8.1 清单里追加「aria/README skill 列表补 2 条」一行
      理由: 8.1 本来就要改 aria/README (版本 SOT 5 文件之一, <vNEXT> = 1.70.0),
            两次改同一文件不如一次改完; 且 8.1 当前**卡在 H1 (Rule #6 AB 未跑)**,
            AB 是会话级前置 (ARIA_COORDINATION_NO_PUSH 未设), 本会话内补不上

  ○ [3] 先补 collector 缺口 (开 issue + 写 .aria/state-checks.yaml 检查)
      执行: A.1 (Level 2 spec, 若改 collector) 或直接开单
      理由: 这次是手数才抓到的; 不机械化, 下次同样的漏项还会漏

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B"
```

**并发提示**: `tracks_multibranch.collision.kind = self_multi_container`（组: `dev-claude` / `simonfishgit/dev-claude`）。按 Layer L 契约，认领闸门只在你确认**进入 Phase B** 时才调用 `phase1_gate`，本次只读扫描不触发。另外上次 handoff §3 第 1 条明确写着: **AB 评测会话期间不要做真实 heartbeat / acquire**（`NO_PUSH` 下 claim 只落本地，随后手册要求的 `+` 强制 fetch 会连真 claim 一起抹掉）。本轨 sweep 死线 `2026-09-06T21:40Z`，时间充裕，等 AB 跑完清理后再刷。

🤔 选择 [1-4] 或输入自定义:
