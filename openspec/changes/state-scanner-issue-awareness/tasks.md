# Tasks: state-scanner Issue 感知能力

> **Parent Spec**: [proposal.md](./proposal.md)
> **Level**: 3 (Full)
> **Estimated Total**: 10.25-14.25 小时
> **Revised**: 2026-04-09 (audit Round 1 修复 M5/M9 + T10/T11 顺序违规)

## Task Breakdown

### T0: Config Schema 前置扩展 [0.25h]  **NEW** (修复 M5)

- [ ] 扩展 `.aria/config.template.json`，新增 `state_scanner.issue_scan` block (9 个字段, 见 proposal Schema)
- [ ] 更新 `aria/skills/config-loader/SKILL.md` 默认值表格，列出所有 `state_scanner.issue_scan.*` 字段和默认值
- [ ] 确保 config-loader 读取缺失字段时返回默认值而非报错
- [ ] 单元验证: 用空 `.aria/config.json` 调用 config-loader，应返回完整默认 block

### T1: 平台检测与 CLI 适配层 [2h]

- [ ] 在 `references/issue-scanning.md` 定义平台检测算法 (4 级优先级，见 proposal)
- [ ] 从 `.aria/config.json` 读 `state_scanner.issue_scan.platform` (显式声明)
- [ ] hostname 匹配: 从 `git remote get-url origin` 解析 hostname，对比 `platform_hostnames` 映射表
- [ ] 兜底推断: `github.com` → github; 已知 Forgejo 域名 → forgejo
- [ ] 定义统一的 `IssueProvider` 抽象接口 (概念层，skill 用 bash 实现)
- [ ] Forgejo 分支: `forgejo GET /repos/{owner}/{repo}/issues?state=open&limit=20`
- [ ] GitHub 分支: `gh issue list --state open --json number,title,labels,url,body --limit 20`
- [ ] 定义 **IssueItem Normalize 映射表** (修复 m6): Forgejo `.labels[].name` / GitHub `.labels[].name` → 统一 `labels[]`，字段缺失 → 空字符串/数组
- [ ] 未知平台: 输出 `fetch_error: "platform_unknown"` 并跳过

### T2: 缓存机制 [1.5h]

- [ ] 定义 `.aria/cache/issues.json` schema (JSON with fetched_at, platform, issues)
- [ ] 读缓存逻辑: 比较 `fetched_at + ttl` vs 当前时间
- [ ] 写缓存逻辑: 原子写 (tmp + mv)
- [ ] **同步 refresh** (修复 M10): 缓存失效 → 同步 API 调用 → 成功覆写 / 失败沿用旧缓存 + `warning: "stale_cache_api_failed"`
- [ ] `.gitignore` 中添加 `.aria/cache/`
- [ ] 明确 `.aria/cache/` 路径命名空间边界 (config-loader 不扫描，修复 m3)

### T3: 错误分类与降级 [2h]

覆盖 **10 个** `fetch_error` 枚举值 (修复 M9: 与 proposal 失败处理表完全对齐):

- [ ] `network_unavailable` — CLI exit ≠ 0 且 stderr 含网络错误关键字
- [ ] `cli_missing` — `command -v forgejo/gh` 失败 (exit 127)
- [ ] `auth_missing` — `.aria/config.json` 缺 token 字段或相应环境变量
- [ ] `auth_failed` — HTTP 401/403 响应
- [ ] `rate_limited` — HTTP 429，读 `Retry-After` 头
- [ ] `not_found_or_no_access` — HTTP 404 (真无此仓库 或 私有+无权限伪 404)
- [ ] `timeout` — API 响应超过 `api_timeout_seconds` (默认 5s)
- [ ] `platform_unknown` — T1 平台检测 4 级全部失败
- [ ] `parse_error` — jq 解析 API 响应失败
- [ ] `unknown` — 兜底未分类，附 stderr 片段

- [ ] 输出降级状态到用户面板 (与 standards_status 一致的视觉模式)
- [ ] 总阶段超时 **12s** 硬限制 (修复 m9: `timeout 12 bash -c ...`)

### T4: 启发式关联 [1.5h]

- [ ] 正则匹配 Issue 标题/正文中的 `\bUS-\d{3,}\b` → `linked_us` (修复 m7: 单词边界)
- [ ] 扫描 `openspec/changes/*/` 目录名 → 对每个 change 名生成正则 `(?<![a-z0-9/-])<change-name>(?![a-z0-9/-])` → 匹配 Issue title/body
- [ ] **URL 路径保护**: Issue 正文中的 `https://.../openspec/changes/my-change/proposal.md` 不应匹配到 `my-change` (测试 case 见 proposal AC9)
- [ ] `linked_openspec` / `linked_us` 字段标注为启发式 (输出中明确 "heuristic": true)
- [ ] 无匹配时为 `null`，不报错
- [ ] 仅扫描 `title` 和 `body`，不扫描 comments (首版)

### T5: SKILL.md 主文档更新 [1h]

- [ ] SKILL.md 新增阶段 1.13 摘要 (~25 行)
- [ ] 配置表格新增 `state_scanner.issue_scan.*`
- [ ] "阶段 1.13" 章节链接到 `references/issue-scanning.md`
- [ ] 确保总行数控制 (预计 ~850 行)

### T6: references/issue-scanning.md 新建 [2h]

- [ ] 完整检测逻辑 (bash 命令示例)
- [ ] 平台适配表格
- [ ] 所有边界场景处理流程
- [ ] 错误码参考
- [ ] 缓存策略说明

### T7: RECOMMENDATION_RULES.md 更新 [0.5h]

- [ ] 新增 `open_blocker_issues` 规则定义
- [ ] 优先级插入现有规则链中合适位置
- [ ] 明确触发条件 (label 包含 `blocker` 或 `critical`)

### T8: output-formats.md 更新 [0.5h]

- [ ] 新增 "🎫 Open Issues" 输出区块示例
- [ ] 各场景变体 (正常/离线/token 缺失/限速)

### T9: config-loader 默认值 [0.5h]

- [ ] `state_scanner.issue_scan.enabled` = false
- [ ] `state_scanner.issue_scan.cache_ttl_seconds` = 900
- [ ] `state_scanner.issue_scan.limit` = 20
- [ ] `state_scanner.issue_scan.label_filter` = []

### T10: AB Benchmark [1.5h]  **(原 T11, 修复规则 #6 顺序违规)**

- [ ] **Mock 策略前置说明** (修复 minor m2): 由于 Skill 在 LLM 运行时执行，fixture 以 prompt 引导方式提供，而非替换真实 CLI 调用
- [ ] 准备 test fixture 1: 模拟 3 open issues 场景 (JSON 注入 prompt)
- [ ] 准备 test fixture 2: 降级场景 `auth_missing`
- [ ] 准备 test fixture 3: 边界场景 `rate_limited` (HTTP 429 + Retry-After)
- [ ] 准备 test fixture 4: 启发式匹配正例 (`US-006` + OpenSpec name)
- [ ] 准备 test fixture 5: 启发式匹配负例 (URL 中的 OpenSpec name，验证单词边界)
- [ ] 运行 `/skill-creator benchmark` with/without AB 对比 (`enabled=true` vs `enabled=false`)
- [ ] 验证 delta ≥ +0.3
- [ ] 结果归档到 `aria-plugin-benchmarks/ab-results/`
- [ ] **若 delta 为负: 暂停所有后续任务 (包括 T11 版本号)，回到 T1-T6 调整**

### T11: 版本号同步 [0.5h]  **(原 T10, 必须在 T10 AB Benchmark 通过后执行)**

**协调策略**: 与 `state-scanner-remote-sync-check` 共享 5 个版本号文件，避免 merge conflict:

- [ ] 确认 `sync-check` PR 是否已先合并
- [ ] **若本 Spec 先合并** (issue-awareness 在前):
  - [ ] `aria/.claude-plugin/plugin.json` → 2.9.0
  - [ ] `aria/.claude-plugin/marketplace.json` → 2.9.0
  - [ ] `aria/VERSION` → 2.9.0
  - [ ] `aria/CHANGELOG.md` → 新增 [2.9.0] 条目 (含 issue-awareness feature bullet)
  - [ ] `aria/README.md` → 版本号 + Skills 描述 (新增 issue-awareness 项)
- [ ] **若 `sync-check` 已先合并** (issue-awareness 在后):
  - [ ] 仅在 `aria/CHANGELOG.md` 的 [2.9.0] 条目追加 issue-awareness feature bullet
  - [ ] 仅在 `aria/README.md` 的 Skills 列表追加 issue-awareness 项
  - [ ] 其他 3 个版本号文件已是 2.9.0，无需修改

### T12: 集成验证 [0.5h]

- [ ] 在 Aria 本仓库运行 state-scanner (需先启用 `issue_scan.enabled=true`)
- [ ] 确认能扫到 Issue #5, #6
- [ ] 确认启发式匹配本 Spec 名称 (`state-scanner-issue-awareness`)
- [ ] 确认离线场景不报错 (手动断网测试)
- [ ] 确认 `auth_missing` 场景展示降级文本
- [ ] 确认 `source: cache` 在 15 分钟内重复调用时生效
- [ ] 确认 `.aria/cache/issues.json` 不被 Git 追踪

## Dependencies (修复 T10/T11 顺序违规)

```
T0 (config schema)──┬──> T1 (平台检测)
                    └──> T9 (config-loader 默认值)

T1 ──┬──> T3 (错误分类 10 种)
     ├──> T2 (缓存)
     └──> T4 (启发式关联)

T2, T3 ────────────> T5 (SKILL.md 摘要)
T2, T3 ────────────> T6 (references/issue-scanning.md)

T5, T6, T7, T8, T9 ──> T10 (AB Benchmark)   ← 先 benchmark
T10 (delta ≥ +0.3) ──> T11 (版本号同步)      ← 后 bump 版本
T11 ────────────────> T12 (集成验证)
```

**关键变更**: T10 (benchmark) **必须**先于 T11 (版本号) 执行。若 benchmark delta 为负，版本号文件不会被修改，避免回滚提交。

## Agent Assignment (Phase A.3)

| Task | Primary Agent | 辅助 Agent | 理由 |
|------|---------------|-----------|------|
| T0 Config Schema 前置 | `aria:backend-architect` | `aria:knowledge-manager` | Schema 扩展 + 文档同步 |
| T1 平台检测与 CLI 适配 | `aria:backend-architect` | - | 多平台 API 设计 |
| T2 缓存机制 | `aria:backend-architect` | `aria:qa-engineer` (TTL 边界) | 核心缓存 + 测试 |
| T3 错误分类 (10 枚举) | `aria:qa-engineer` | `aria:backend-architect` | 边界场景主导 |
| T4 启发式关联 | `aria:backend-architect` | `aria:qa-engineer` (正则边界) | 正则 + URL 保护测试 |
| T5 SKILL.md 主文档 | `aria:knowledge-manager` | `aria:backend-architect` | 文档组织 + 技术准确 |
| T6 references/issue-scanning.md | `aria:knowledge-manager` | `aria:backend-architect` | 完整技术文档 |
| T7 RECOMMENDATION_RULES | `aria:backend-architect` | - | 规则设计 |
| T8 output-formats 区块 | `aria:knowledge-manager` | - | 输出格式 |
| T9 config-loader 默认值 | `aria:backend-architect` | - | Schema 默认值 |
| T10 AB Benchmark | `aria:qa-engineer` | - | 质量验证 + mock 策略 |
| T11 版本号同步 | **主 agent** (协调) | - | 需跨 Spec 协调 |
| T12 集成验证 | `aria:qa-engineer` | `aria:code-reviewer` | 最终验证 |

**Code Review 门禁**: 所有任务完成后由 `aria:code-reviewer` 做 final review (C.2 前)

**关键里程碑审计建议**:
- T3 完成后 (错误处理层建成): post_implementation 检查点可触发 mid_implementation 审计
- T10 完成后 (benchmark 通过): pre_merge 检查点强制审计

## Merge Gate (不可协商)

- ✅ T0 config schema 扩展已合并，config-loader 默认值生效
- ✅ T10 AB Benchmark delta ≥ +0.3 (严格于之前 "正值" 标准)
- ✅ T11 版本号同步 (仅在 T10 通过后执行)
- ✅ T12 集成验证全部通过
- ✅ 本 Spec 影响 **12 个文件** (其中 **5 个版本号文件**: `plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md` 一致为 2.9.0)
- ✅ **与 `state-scanner-remote-sync-check` 共享 5 个版本号文件**: 两 Spec 必须协调同时 bump，由先合并的 PR 完成 `2.8.0 → 2.9.0`，后合并的 PR 仅追加 CHANGELOG 条目 (避免 merge conflict)
- ✅ 无前置阻塞关系 (`sync-check` 不阻塞本 Spec)
- ✅ Code review 通过 (`aria:code-reviewer`)
