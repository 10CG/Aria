```
╔══════════════════════════════════════════════════════════════╗
║              PHASE D - CLOSURE                               ║
╚══════════════════════════════════════════════════════════════╝
```

你点名的是 **D.1 (进度更新)**。先说结论: **D.1 现在跑不了 —— 前置探测两项都落空**, 缺的是输入不是权限。下面是实测证据、缺什么、以及补齐后 D.1 会逐字段写什么。

---

## 0. 先做 skip 评估 (SKILL.md §跳过规则, 不能跳过这步)

D.1 的 skip 判据是「UPM 文档是否存在」, D.2 的是「openspec/changes/ 是否有该 Spec」。两条都实跑了:

```bash
$ ls mobile/docs/project-planning/unified-progress-management.md \
     backend/project-planning/unified-progress-management.md
ls: cannot access 'mobile/docs/project-planning/unified-progress-management.md': No such file or directory
ls: cannot access 'backend/project-planning/unified-progress-management.md': No such file or directory

$ find . -name 'unified-progress-management*.md' -not -path './.git/*'
./standards/core/upm/unified-progress-management-spec.md        # ← 这是 UPM **规范本体**, 不是某模块的 UPM 实例

$ ls openspec/changes/
a1-entry-claim-duplicate-work-guard      aria-2.0-m6-release-closeout
aria-2.0-m6-cost-model-telemetry         aria-2.0-m7-agent-lifecycle
aria-2.0-m6-dispatch-input-delivery      aria-2.0-m7-fleet-aggregation
aria-2.0-m6-e2e-resilience
# 无 oauth2-social-login

$ python3 -c "import json; c=json.load(open('.aria/config.json')); print(c.get('upm'))"
None      # 无 upm 配置节 ⇒ milestone_driven 取默认 false ⇒ D.1 走 single-pass 完整更新模式
```

**两种解释, 需要你裁一下**:

1. **`oauth2-social-login` 属于另一个仓** (当前 cwd 是 Aria meta-repo)。那么请告诉我目标仓路径 —— 我在那边重跑探测再执行 D.1。
2. **确实是本仓**。那么按 SKILL.md 跳过规则, **D.1 = skip (模块无 UPM 配置)**、**D.2 = skip (无该活跃 Spec)** —— 但 6 个任务全完成、PR 已 merge 的事实说明 Spec 目录应该在某处, 更可能是解释 1 而不是「真的没有」。

我**不**替你在本仓凭空造一份 UPM 或 `openspec/changes/oauth2-social-login/` —— 那是把「找不到」伪装成「已完成」。

---

## 1. 还缺的输入 (补齐即可执行)

| 参数 | 必需性 | 现状 | 说明 |
|------|--------|------|------|
| `module` | ✅ 必需 | **缺** | 决定 UPM 路径 (`mobile` / `backend` / `shared` / `standards`)。你给的 "oauth2-social-login" 是 spec_id 不是 module |
| `commit_ref` | ⚠️ 强烈推荐 | **缺** | 需要 merge commit SHA 才能构造 `lastUpdateRef`。PR #143 的 URL 也一并给我 |
| `completed_tasks` | ❌ 可选 | **半缺** | 你说「6 tasks complete」, 但我需要 **TASK-ID 列表** 才能写 `completedTasks[]`; 有 `detailed-tasks.yaml` 的话我自己读 |
| `kpi_updates` | ❌ 可选 | 缺 | 覆盖率等指标, 不给就沿用旧 `kpiSnapshot` |
| `spec_path` | ❌ 可选 | 缺 | 给了才做 D.1.6 双层架构后向同步 (`detailed-tasks.yaml` → `tasks.md` checkbox) |

最小可执行集合 = **`module` + 目标仓路径**。其余我能从仓里读出来。

---

## 2. 补齐后 D.1 会做什么 (逐步, 供你先审)

按 `progress-updater` v2.0 的 D.1.1–D.1.6:

```yaml
D.1.1 读取当前状态:
  - 读 <module> 的 UPM, 取出当前 UPMv2-STATE
  - 记下当前 stateToken  ← 并发冲突检测的基线, 写入前要再校验一次

D.1.2 准备更新数据:
  lastUpdateAt:  <UTC now, ISO 8601>            # 用 date -u, 不用 datetime.now()
  lastUpdateRef: "git:<merge-sha>-oauth2 social login (PR #143)"
  completedTasks: [<6 个 TASK-ID>]              # 待你/detailed-tasks.yaml 提供
  kpiSnapshot:   合并 kpi_updates (未提供则沿用旧值)
  nextCycle.candidates / risks: 未提供则不动

D.1.3 重算 stateToken:
  输入 = module|stage|cycleNumber|lastUpdateAt|kpiSnapshot
  SHA256 取前 12 位 → "sha256:xxxxxxxxxxxx"

D.1.4 周期文档: cycle_doc 默认 false → 不写 (你要就说)

D.1.5 回写 UPM:
  - 写前校验 stateToken 与 D.1.1 记录一致
  - 不一致 → 重读-合并-重算-重试, 最多 3 次, 仍冲突则停下报你

D.1.6 双层后向同步 (仅在给了 spec_path 时):
  - detailed-tasks.yaml 中 completed 的任务 → 按 parent 字段回填 tasks.md 的 [ ] → [x]
  - 三类冲突: 进度不匹配=自动修复+警告 / parent 引用失效=**中止同步并报错** / 任务定义相似度<80%=继续+警告
```

**cycleNumber 提醒**: 「+1 还是保持」取决于本 PR 是否收掉整个 cycle。你给的信息是「1 个 Spec 的 6 个任务全完」——如果该 cycle 只含这一个 Spec 就 +1, 若 cycle 里还有别的 Spec 在飞就保持。这条我不替你猜, 执行前会按 UPM 里的 cycle 定义再确认一次。

**模式判定已定**: `.aria/config.json` 无 `upm.milestone_driven` ⇒ 默认 `false` ⇒ **single-pass**, 即 D.1 做完整更新, 而不是 milestone-driven 那种「只把 `[~]` finalize 成 `[x]` + 挂 archive 路径」。如果目标仓开了 `milestone_driven: true`, 我会切到 finalize 口径, 不重建 C.2.6 已实时写入的 sub-bullets。

---

## 3. D.1 不是 Phase D 的全部 —— 其余 4 步的状态

你只点了 D.1, 我不擅自替你跑完; 但按 SKILL.md 收尾闭环是 5 步, 漏掉的后果分别列在这里, 你决定跑哪些:

| 步骤 | 现在的判定 | 说明 |
|------|-----------|------|
| **D.post** post_closure 审计 | **skip (确定)** | 实读 `.aria/config.json` → `audit.checkpoints.post_closure: "off"`。这是 config 显式 off, 属合法豁免, 非我自行裁量 |
| **D.2** Spec 归档 | **待定** | 本仓无该 Spec 目录; 定位到之后必须先跑 gate, 见下 |
| **D.2b** claim 释放 | **建议跑** | 见下, advisory 但漏了会让 claim 永久 active 累积 |
| **D.3** session handoff | **待评估** | 4 级 fallback 触发; 输出**只能**写 `docs/handoff/{YYYY-MM-DD}-{slug}.md`, 绝不写 `.aria/handoff/` |
| **D.4** estimator capture | **末位跑** | advisory 非阻塞, 幂等可重跑 |

**D.2 的 gate 不能省, 也不能只看 exit code** —— 定位到 Spec 后第一步是:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
  --gate "openspec/changes/oauth2-social-login"
```

解析 stdout JSON 的 **`verdict` 字段**做三路路由 (exit 0 把 pass 和 warn 合并了, 区分不出来):

1. `verdict == "block"` → D.2 **BLOCKED**, 回显 `blocking_reasons`。我**不会**自动加 `--archive-design-only` 绕过 —— 强制归档是 owner/AI 的显式决定, 得另行直接调 `openspec-archive` 并带上 reason。注意 block 可以和 `complete == true` 并存 (点名符号零生产语义引用 = 死代码判定), 「6 个任务都打勾了」不构成豁免。
2. `complete == false` 且 `verdict != "block"` → skip 不归档, 回显 `complete_reason`。
3. `complete == true` 且 `verdict ∈ {pass, warn}` → 调 `openspec-archive` 归档。`warn` 的 frontmatter 写入和 deferred/unverified 的 issue 创建**全部由 openspec-archive 自己 Step 2/Step 7 处理**, 我这边不重复开 issue (单一 owner)。

**D.2b claim 释放** (归档后, 或 D.2 跳过但本 session 在 Phase B-entry 过了 phase1_gate):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/release_gate.py" \
  --raw-track-id "<A.1 认领时派生的那一串原始 carry-id>" --sweep-stale --gc --repo-path "<repo root>"
```

- carry-id 必须是 **A.1 认领时那一串原始值**, 与 Phase B-entry 传给 phase1_gate 的同源 —— 现在重新拼一串会 release 不到自己那条。**这串你得给我, 或告诉我从哪读**。
- 判定不只看 exit code: `released.success=true` 但 `push_success=false` = 只在本地释放, 远端/其他终端仍看到 active claim, 我会如实报「本地已释放, 待下次 fetch/reconcile 收敛」而不是报「已释放」。
- `released.error == "claim_not_found"` 是 benign (早已释放/未认领)。
- 就算本 session 没认领, 也建议跑不带 `--raw-track-id` 的 `--sweep-stale --gc` 做 ref 卫生。

---

## 4. 我需要你回一句

最少给我这两项就能开跑:

1. **目标仓路径 + `module`** (决定 UPM 落点; 若确认就是本 Aria 仓, 我按 skip 规则如实记 D.1 skipped, 不造 UPM)。
2. **PR #143 的 merge commit SHA** (构造 `lastUpdateRef`)。

顺带确认三个可选项: 6 个任务的 TASK-ID 列表 (或让我读 `detailed-tasks.yaml`) / 要不要连 D.2–D.4 一起收完 / 本 cycle 的 carry-id。

```
🚀 当前执行结果
───────────────────────────────────────────────────────────────
  ⏸  D.1 progress-updater   → 未执行 (UPM 未定位, 缺 module)
  ⏭  D.post audit           → skip (config post_closure = off)
  ⏸  D.2 openspec-archive   → 未执行 (Spec 目录未定位, gate 未跑)
  ⏸  D.2b release_gate      → 未执行 (缺 carry-id)
  ⏸  D.3 session-handoff    → 未评估 (待 D.1/D.2 结果)
  ⏸  D.4 estimator capture  → 未执行 (收尾末位)

  状态: 阻塞于输入缺失, 非失败。本仓零写入。
```
