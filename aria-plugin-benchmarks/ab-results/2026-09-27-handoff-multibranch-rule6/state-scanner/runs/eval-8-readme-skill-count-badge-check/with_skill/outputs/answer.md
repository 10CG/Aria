## 先说结论

扫描结果和你的说法有两处对不上，先说清楚：

1. **v1.14.0 不是刚发布的版本。** `aria/.claude-plugin/plugin.json` 当前是 **1.73.3**（marketplace.json、VERSION、CHANGELOG 顶部都一致）。`v1.14.0` 是 2026-04-12 的旧版本（提交 `06a0edf`，内容是「Phase 1.8 README 检查增强 + Phase 1.14 Forgejo 配置检测」），不是新增 3 个 Skill 的版本。本地也没有 `v1.14.0` 这个 tag。你可能记错了版本号，或者说的是别的仓库。请确认一下。
2. **badge 版本没问题**：主项目 README 的 Plugin badge 是 `v1.73.3`，和 plugin.json 一致。
3. **Skill 列表有真问题**：数量写对了（42），但**列表里漏了 2 个 Skill：`issue-triage` 和 `session-closer`**。中文版 `aria/README.zh.md` 的问题更多，数量也没更新（写的是 41）。

下面是按 state-scanner 格式给出的完整报告。

---

## Step 0: scan.py

```
python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output <评测产出目录>/state-snapshot.json
退出码: 0 (全部采集成功), errors[] = []
```

scan.py 在 snapshot 里只比对 README 的**版本号**，不统计 Skill 数量，也不核对 Skill 列表。所以数量和列表是扫描之后我读 README 原文、对照 `aria/skills/*/SKILL.md` 核对出来的（SKILL.md 规定允许「scan.py 成功后读取外部文件」）。

---

### 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity`（没有配置 upstream）
- Phase/Cycle: UPM 未配置
- 未提交变更: 3 个。`aria`、`standards` 两个子模块指针有改动，另有 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- `aria` 子模块当前在 `b181678`（`v1.73.3-9-gb181678`，比 v1.73.3 tag 多 9 个提交，主仓 gitlink 还没更新到这里）
- 中断状态: 无（`interrupt.status = none`）；没有进行中的 git 操作

### 📊 变更分析
- 变更类型: other 3（只有子模块指针和未跟踪目录）/ 复杂度 Level 2 / 架构影响: 否
- 🔬 Skill 变更 AB: 没检测到 SKILL.md 改动（`skill_changes.detected = false`）

### 📄 需求状态
- PRD: `prd-aria-v1.md` (Active)、`prd-aria-v2.md` (Approved)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在，Active，最后更新 2026-09-02，需求链路完整

### 📋 OpenSpec 状态
- 活跃变更 8 个 / 已归档 146 个 / 待归档 0 个
- ⚠️ 设计未实施 5 个: `aria-2.0-m6-cost-model-telemetry` (79 天)、`aria-2.0-m6-e2e-resilience` (77 天)、`aria-2.0-m6-release-closeout` (124 天)、`aria-2.0-m7-agent-lifecycle` (100 天)、`aria-2.0-m7-fleet-aggregation` (70 天)

### 🛡️ 审计状态
- 已启用；上次审计 `post_planning` R7，PASS，已收敛（2026-09-24）

### 🔧 自定义检查（16/16 通过）
和你的问题直接相关的几项：
- ✅ `m6-version-badge-match`: OK badge=1.73.3
- ✅ `i18n-readme-translation-currency`: 3 个 i18n README 都标注在 1.73.3
- ✅ `plugin-version-arch-docs-match`、`main-project-version-consistency`: 通过

注意：这些检查**只核对版本号，不核对 Skill 列表**。所以下面的列表缺漏没被机械检查拦住。

### 🔄 同步状态
- 当前分支: 没有 upstream（`no_upstream`）
- 多远程一致性: `overall_parity = true`。主仓和 `aria`、`standards` 子模块在 github/origin 上都一致；gitlink 完整性 6/6 ok
- ⚠️ 协调 ref 获取失败，用的是 265 秒前的缓存（`coordination_fetch.degraded = fetch_failed_using_stale_cache`）

#### 📝 README 版本一致性（重点）

| 核对项 | 期望（来源） | 实际 | 结果 |
|---|---|---|---|
| `aria/README.md` 版本行 | 1.73.3 (plugin.json) | 1.73.3 | ✅ |
| `aria/README.zh.md` 版本行 | 1.73.3 | 1.73.3 | ✅ |
| 主项目 `README.md` Plugin badge | v1.73.3 | v1.73.3 | ✅ |
| `README.zh.md` / `README.ja.md` / `README.ko.md` badge | v1.73.3 | v1.73.3 | ✅ |
| 主项目 `README.md` 第 242 行 "Plugin Version" | 1.73.3 | 1.73.3（写的是 42 Skills） | ✅ |

#### 📦 Skill 数量与列表（重点，扫描后人工核对）

实际目录: `aria/skills/` 下有 **42 个含 SKILL.md 的目录**（另有一个 `issue-triage-workspace/` 没有 SKILL.md，是评测工作目录，不算 Skill）。其中 7 个是 `user-invocable: false`（agent-router、agent-team-audit、arch-common、aria-token-telemetry、audit-engine、config-loader、git-remote-helper），所以 35 个面向用户，7 个内部。

| 文件 | 声称的数量 | 数量对吗 | 列表条目数 | 漏掉的 Skill |
|---|---|---|---|---|
| `aria/README.md` | 35 + 7 = 42 | ✅ 对 | 40 | ❌ `issue-triage`、`session-closer` |
| `aria/README.zh.md` | 34 + 7 = 41 | ❌ 少 1 | 40 | ❌ `issue-triage`、`session-closer` |
| 主项目 `README*.md` / system-architecture.md | 42 Skills | ✅ 对 | 没有逐项列表 | 不适用 |

- 漏掉的两个都不是最近才加的：`issue-triage` 在 2026-05-13 加入（`d2d7cb6`），`session-closer` 在 2026-06-25 加入（`7801bd4`）。英文 README 更新了总数，却没把条目补进列表。
- 列表里**没有**多出来的、目录里不存在的 Skill。
- 内部 Skill 的标注（7 个）和 frontmatter 一致。

### 🎫 Open Issues
- 已配置 issue_scan。最新几条: #221 secret-guard 进程列举旁路、#220 latest.md History prepend 缺少机械核验、#219 只读进度接口、#218 handoff mtime 判最新…（完整列表见 snapshot 的 `issue_status`）

### 🌲 多终端协调提示
- `tracks_multibranch.collision.kind = self_multi_container`：同一 owner 在多个容器（simonfish / aria-runner-bot）上有活跃轨道。**进入 Phase B 之前**，编排层按规定要调用下面这条命令（本次是只读评测，**我没有执行**）：
  ```
  python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "<最新 handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria
  ```

---

### 🎯 推荐工作流

匹配规则: `readme_outdated`（README 内容和实际不一致）→ **doc-update**。这里要修的是 Skill 列表内容，版本号本身没问题。

**[1] 文档修复（推荐）**: 单开一条分支修 README 列表
- 步骤: B.1 在 `aria` 子模块基于 master 新建分支（例如 `docs/readme-skill-list-sync`）→ B.2 修改 →  C.1 提交 → C.2 合并（子模块必须本地 merge + 双推 + 对每个 remote 做 `ls-remote` 核验，禁止用 Forgejo 服务端合并）
- 要改的内容:
  - `aria/README.md`: 在合适分类下补上 `issue-triage`（例如 Feedback & Reporting 或 Dev Tools）和 `session-closer`（Ten-Step Cycle Core，与 phase-d-closer 并列，注明是会话收尾、不是周期收尾）
  - `aria/README.zh.md`: 标题改成「35 个面向用户 + 7 个内部 = 42 个」，同样补上这两项
- 跳过: A.1–A.3（只改 README，Level 1，不需要 OpenSpec）；Rule #6 不适用（没改 SKILL.md）
- 理由: 当前分支 `feature/handoff-multibranch-subdir-path-fidelity` 是另一条在做的工作（#195），不要把无关的文档修复混进去
- 置信度: 85%（按 `readme_outdated` 规则不自动执行）

**[2] 在当前 feature 分支顺手修**: 改动小，但会把无关内容混进 #195 的交付范围，将来 review 和回溯都会更难

**[3] 只登记不修**: 开一个 issue 记下「README 列表漏 issue-triage/session-closer + zh 版计数 41」，再加一个自定义检查 `skill-list-readme-match`（目录集合和 README 列表集合做比对），防止以后再漏

**[4] 自定义**: 例如 [1] + [3] 里的新检查一起做

另外，请先确认「v1.14.0 新增 3 个 Skill」具体指什么。如果你真的刚加了 3 个新 Skill，但它们还没提交或没合进 `aria` 子模块，那这次扫描看不到它们（当前目录里是 42 个，没有未提交的 SKILL.md 改动）。
