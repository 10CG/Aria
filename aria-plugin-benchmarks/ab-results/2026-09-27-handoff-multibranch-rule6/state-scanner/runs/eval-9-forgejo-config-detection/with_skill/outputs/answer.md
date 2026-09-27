已跑完 state-scanner Step 0 (`scan.py` 退出码 0，`errors[]` 为空，snapshot 可以直接用)。

先说结论：
- **确实缺一项配置**：检测到 Forgejo 远程 (`forgejo.10cg.pub`)，但仓库根目录下没有 `CLAUDE.local.md` (`forgejo_config.config_status = "missing"`)。
- **不过 Forgejo API 访问现在已经能用**：这次扫描通过 `forgejo` CLI wrapper 拉到了 4 个仓的 49 个 open issue，`fetch_error` 为空。所以缺 `CLAUDE.local.md` 不影响 issue 扫描，也不影响 `forgejo` 命令行；受影响的是 `/forgejo-sync` (User Story 和 Issue 双向同步、把 PRD 发布到 Wiki)，它要从 `CLAUDE.local.md` 读 `forgejo:` 配置块。
- **创建前要先处理一个坑**：`CLAUDE.local.md` 目前**没有被 git 忽略** (`git check-ignore` 没有命中)。直接创建的话，它会以未跟踪文件的形式出现，很容易被 `git add -A` 一起提交上去。

---

## 当前状态

- 分支：`feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`)，没有 git 操作卡在中途，也没有中断的工作流 (`interrupt.status = none`)
- 模块 / Phase：UPM 未配置 (Aria 本仓没有运行时 UPM，这是已知状态)
- 变更文件：3 个
  - `aria`、`standards` 两个子模块指针有改动 (子模块检出的 commit 和主仓记录的 gitlink 对不上)
  - 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 关联 OpenSpec：`handoff-multibranch-subdir-path-fidelity` (Approved)
- 上次 handoff：`2026-09-24-session-close-199-post-planning-converged.md` (60.3h 前，来源：pointer)。注意这份 handoff 早于本分支今天的提交：它 §6 写的是「#195 B.1 待起」，而本分支最新提交已经做到「台账记录 owner 2026-09-27 裁定」。以分支上的实际进度为准，handoff §6 这一条已经过时。

## 变更分析

- 变更类型：3 个都是 `other` (2 个子模块指针 + 1 个 AB 结果目录)，没有代码、测试、文档类改动
- 复杂度：Level 2 | 架构影响：无 | 没有检测到 SKILL.md 改动

## 需求状态

- 已配置
- PRD：`prd-aria-v1.md` (active)；`prd-aria-v2.md` 原文写的是 Approved，归一化后被判成 pending。这是已知的归类缺陷 10CG/aria-plugin#198，不是文档本身有问题
- User Stories 共 21 个：done 17 / in_progress 2 (US-007、US-026) / approved 1 (US-028) / pending 1 (US-003)

## 架构状态

- `docs/architecture/system-architecture.md` 存在，Active，最后更新 2026-09-02，需求链路完整

## OpenSpec 状态

- 活跃变更 8 个 (都是 approved)；已归档 146 个；待归档 0 个
- 设计完成但未实施：5 个 (`m6-release-closeout` 124 天、`m7-agent-lifecycle` 100 天、`m6-cost-model-telemetry` 79 天、`m6-e2e-resilience` 77 天、`m7-fleet-aggregation` 70 天)，都在等 M6 那几道门，和 CLAUDE.md 项目状态段的描述一致

## 审计状态

- 审计已启用；最近一次是 post_planning R7，PASS，已收敛 (2026-09-24)

## 自定义检查

- 16/16 全部通过，没有失败或过期项

## 同步状态

- 当前分支没有配置 upstream (`no_upstream`)，但多远程对比显示 `origin` 和 `github` 都等于 `4f91772`，`overall_parity = true`
- 子模块 gitlink 可达性：两个远程 × 3 个子模块，全部 `ok`
- README 版本一致：aria-plugin 1.73.3
- **Forgejo 配置检查**
  - [警告] 检测到 Forgejo 远程 (forgejo.10cg.pub)，但缺少 CLAUDE.local.md
  - 建议：运行 `/forgejo-sync`，它会引导你创建配置 (需要你确认)

## Open Issues

- 平台：Forgejo，共 49 个 open (10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 7 · 10CG/aria-orchestrator 2)。数据来源是缓存，获取于 2026-09-27T17:09:50Z，没有错误
- 和当前分支有关的：10CG/aria-plugin#204 (handoff 读侧仍按扁平布局处理，已关联 `handoff-multibranch-subdir-path-fidelity`)
- 带 bug 标签的 4 个：Aria#221 (secret-guard 能被进程列举绕过)、#218、#217、#199

---

## 如何设置 Forgejo 集成

### 第 1 步：先让 `CLAUDE.local.md` 不进版本库

`CLAUDE.local.md` 是个人本地配置，不应该提交。有两种做法，二选一：

```bash
# 做法 A：只在本机忽略，不改动仓库文件 (推荐)
echo 'CLAUDE.local.md' >> .git/info/exclude

# 做法 B：写进 .gitignore，所有协作者都生效 (这是一次仓库改动，要走正常提交流程)
echo 'CLAUDE.local.md' >> .gitignore
```

改完用 `git check-ignore -v CLAUDE.local.md` 确认有命中。

### 第 2 步：创建配置 (两条路)

**路 A (推荐)：运行 `/forgejo-sync`。** 它会根据 git remote 推出 `owner/repo`，对 `forgejo.10cg.pub` 默认开启 Cloudflare Access，先把完整配置给你看，再问 [y/N]，确认后才创建文件。

**路 B：手动创建。** 在仓库根目录新建 `CLAUDE.local.md`，写入：

```yaml
## Forgejo Integration
forgejo:
  url: "https://forgejo.10cg.pub"
  repo: "10CG/Aria"
  api_token: "${FORGEJO_TOKEN}"        # 只写环境变量名，不写 token 本身
  cloudflare_access:
    enabled: true
    client_id_env: "CF_ACCESS_CLIENT_ID"
    client_secret_env: "CF_ACCESS_CLIENT_SECRET"
```

要注意几点：
- `forgejo:` 必须是**顶格的真实 YAML 键**。scan.py 在判断时会先把 ``` 代码块里的内容去掉，所以如果你把上面整段连同代码围栏一起贴进去，扫描结果仍然是「未配置」。直接写裸 YAML 行，或者用 `## forgejo` 标题。
- `/forgejo-sync` 自动生成的模板里没有 `api_token` 这一行，但它的「必需配置」一节又要求有。手动创建时建议按上面写上，引用环境变量即可。
- 如果还有别的 Forgejo 实例，用 `ARIA_FORGEJO_HOSTS` 环境变量 (逗号分隔) 或 `.aria/config.json` 里的 `state_scanner.issue_scan.platform_hostnames.forgejo` 追加主机名。优先级是：环境变量 > config > 默认值。

### 第 3 步：准备环境变量 (不要让 secret 出现在对话里)

`FORGEJO_TOKEN`、`CF_ACCESS_CLIENT_ID`、`CF_ACCESS_CLIENT_SECRET` 放在你的 shell 环境或 secret 存储里，**不要**写进 `CLAUDE.local.md`，也不要贴到对话里。按 Rule #7，验证时只看元信息，不回显值：

```bash
for v in FORGEJO_TOKEN CF_ACCESS_CLIENT_ID CF_ACCESS_CLIENT_SECRET; do
  val="${!v}"   # 只存到局部变量里，不打印
  if [ -n "$val" ]; then echo "$v: set (len=${#val})"; else echo "$v: MISSING"; fi
done
unset val
# 连通性只看退出码
forgejo GET /repos/10CG/Aria >/dev/null 2>&1; echo "exit=$?"
```

不确定该用哪个 token (人账号、bot 账号、应用级 token) 时，可以用 `/aether:aether-forgejo-creds`；本仓应用级 token 的台账在 `.aria/pat-inventory.yaml`。

### 第 4 步：确认配置生效

重新运行 `/state-scanner`，「Forgejo 配置检查」一行应该变成「已配置 (forgejo.10cg.pub)」，也就是 `config_status = "configured"`。

---

## 推荐工作流

- **[1] 配置 Forgejo 集成 (推荐，对应你这次的问题)**
  - 执行：先做第 1 步 (忽略文件)，再运行 `/forgejo-sync` 引导创建配置 (需要确认)，然后做第 3 步验证环境变量，最后重跑 `/state-scanner` 复核
  - 跳过：十步循环的各个 Phase。这是本地配置，不是需求变更，不需要 OpenSpec
  - 理由：扫描结果里唯一的配置缺口就是 `CLAUDE.local.md` 缺失；其余 16 项检查全部通过，多远程也完全同步
- **[2] 继续本分支的 #195 track (`handoff-multibranch-subdir-path-fidelity`)**
  - 执行：先处理 3 个未提交项 (子模块指针和 AB 结果目录，要不要提交)，然后按 phase-c-integrator 继续
  - 注意：`tracks_multibranch.collision.kind = self_multi_container` (simonfish 和 aria-runner-bot 同时持有同一个身份)。进入 Phase B 或恢复 Phase B 之前，编排层应该跑下面这条认领门命令。这次是只读评测，**我没有执行**，只列出来：
    `python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --mode advisory --repo-path /home/dev/Aria`
- **[3] 只看状态，不做操作**
- **[4] 自定义组合** (输入格式如 "B.2 + C.1" 或 "Phase C")

请选择 [1-4] 或输入自定义组合。
