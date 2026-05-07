# aria-secret-hygiene-rule

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Draft
> **Created**: 2026-05-07
> **Type**: Aria methodology rule addition (standards/ 新文件 + 主 CLAUDE.md 规则 #7)
> **Source**: Forgejo Issue [#78](https://forgejo.10cg.pub/10CG/Aria/issues/78) (filed by truffle-hound team after 2026-05-06 secret leak incident); memory `feedback_secrets_never_in_conversation.md` (2026-05-02 教训, 4 keys leaked via `nomad inspect` 全量 dump)
> **Scope decision**: **Path (1) Documentation only** for this Spec; Path (3) PreToolUse hook defer 至独立后续 Spec (false-positive 调优 + 多 shell 兼容是其独立设计议题)
> **Owner authority**: Aria methodology owner (10CG Lab); proposer 是 truffle-hound 项目 (creationhikari@gmail.com), 同 10CG 组织内但不同项目
> **Related**: `feedback_nomad_inspect_secret_leak.md` (Aria 自身 2026-05-02 教训), `.aria/decisions/2026-05-02-secret-rotation-deferred.md` (rotation SOP)

---

## Why

### Incident pattern (cross-project)

2026-05-06 truffle-hound v0.3.2 chat MVP deploy 期间 AI session 跑:

```python
subprocess.run(['nomad', 'var', 'put', '-force', 'nomad/jobs/th-orch', ...])
```

未指定 stdout/stderr redirect → Python `subprocess.run` 默认 inherit parent stdio → `nomad var put` 成功响应回显完整 Items map (含 secret plaintext) → ssh tunnel → AI tool result → **chat 历史持久化**。

4 个生产密钥曝光: `feishu_app_secret` / `LUXENO_API_KEY` / `FORGEJO_TOKEN` / `cf_access_client_secret`。

### Aria 自身已 2 次中招

| 日期 | Project | 命令 | Memory |
|------|---------|------|--------|
| 2026-05-02 | Aria (US-022 T8) | `nomad job inspect / aether status --json` 全量 dump runtime env | `feedback_nomad_inspect_secret_leak.md` |
| 2026-05-02 | Aria | `LUXENO_API_KEY` session 期 | `feedback_secrets_never_in_conversation.md` |
| 2026-05-06 | truffle-hound (cross-project) | `nomad var put` subprocess inherit stdio | this Issue |

Pattern 跨项目重复 → memory feedback 不足以阻止再发 → **需机械化 SOP**。

### 类问题命令不止本项目 (per Issue body)

```
nomad var put / nomad var get  (full output with secret values)
kubectl create secret / kubectl apply -f (manifest 含 secret)
vault kv put / vault write
gh secret set
Forgejo POST /tokens API
aws secretsmanager (create|put|update)-secret
docker login (without --password-stdin)
ssh-keygen 后 cat priv key
DB password set/reset
```

**根因**: AI assistant 默认假设 stdout "只是日志"。但运维领域有一类命令——secret 写入/读取——**正常成功流就回显 secret 值**。Subprocess inherit + bash 不显式 redirect 同样 leak。

### Verifiability HIGH

`feedback_nomad_inspect_secret_leak` + 现 Issue + truffle-hound incident report (`reports/incident-2026-05-06-secret-leak-via-subprocess.md`) 共 3 处独立来源, 非 prose-only 描述。

---

## What

### 1. New canonical SOP file: `standards/conventions/secret-hygiene.md`

**File**: `standards/conventions/secret-hygiene.md` (~200 行)

**Frontmatter 风格** (与 `standards/conventions/git-commit.md` 一致):

```markdown
# Secret Hygiene 规范 (Aria 规范 #7)

> **Version**: 1.0.0
> **Status**: Active
> **Source incident**: 2026-05-06 (truffle-hound) + 2026-05-02 (Aria)
> **Forgejo Issue**: 10CG/Aria#78
```

**核心条款**:

> **Secret-writing/reading commands MUST NOT echo secret values to chat-visible streams.**
>
> Any shell command that reads or writes a secret value MUST:
>
> - Bash: `cmd >/dev/null 2>&1` 或 `cmd 2>&1 | grep -v '<secret-pattern>'`
> - Python: `subprocess.run(..., stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)` 或 `capture_output=True` 且不 print stdout
> - Verification: 通过 metadata (HTTP status code / exit code / 字段 length) 而非 echo value
>
> **Forbidden**:
>
> - Pipe secret command output 到任何 chat-visible / log-persistent stream
> - subprocess 默认继承 stdout (Python 默认行为, 必须显式 override)
> - `cat <key-file>`, `echo $SECRET_VAR`, `env | grep <secret>` 在 AI session 内
>
> **Exception annotation** (rare): 若必须 echo (e.g., debugging in isolated env), 用 `# secret-leak-ok-explicit` 注释标识豁免。该注释**必须**包含理由 + 隔离环境证据 + owner sign-off。

**Scope (受限命令清单)** — non-exhaustive 启发式:

```
nomad var put | nomad var get
kubectl create secret | kubectl apply -f
vault kv put | vault write
gh secret set | gh api /repos/.../secrets
forgejo POST /tokens | forgejo POST /users/.../tokens
aws secretsmanager (create|put|update)-secret
docker login (无 --password-stdin)
ssh-keygen 后 cat <key>
DB password set/reset (psql ALTER USER, mysql SET PASSWORD)
gcloud secrets versions access
az keyvault secret show
```

**正向 pattern 示例 (Python subprocess)**:

```python
# ✅ 正确 — capture + ignore stdout
result = subprocess.run(
    ['nomad', 'var', 'put', ...],
    capture_output=True, check=True, timeout=30
)
# 用 returncode / 字段 length 验证, 不 print(result.stdout)
assert result.returncode == 0

# ✅ 正确 — 显式 DEVNULL
subprocess.run(
    ['nomad', 'var', 'put', ...],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    check=True, timeout=30,
)

# ❌ 错误 — 默认继承 stdio
subprocess.run(['nomad', 'var', 'put', ...])  # leaks to chat
```

**正向 pattern 示例 (Bash)**:

```bash
# ✅ 正确 — 全部 redirect
nomad var put -force nomad/jobs/X KEY=$VAL >/dev/null 2>&1

# ✅ 正确 — pipe filter (但脆弱, 建议 DEVNULL 优先)
nomad var put ... 2>&1 | grep -v -E '(Items|Value|secret)'

# ❌ 错误 — 默认 stdio
nomad var put ...
```

**Validation guidance**:
- 用 metadata 验 (HTTP 200 / exit 0 / `nomad var get -out=keys` 仅取 key 名)
- 不读 secret value 字面验 round-trip

### 2. Update `CLAUDE.md` (Aria project root) — add rule #7

**File**: `/CLAUDE.md` 主项目根 (Aria methodology owner CLAUDE.md, 不是 aria-orchestrator 子项目的)

**位置**: `## 不可协商规则` 章节, 在规则 #6 (`/skill-creator` benchmark) 之后追加 #7。

**Diff**:

```diff
6. **Skill 基准测试必须使用 `/skill-creator`** - 不得使用自研 runner

**规则 #6 要点:** ... (existing content unchanged)

+7. **Secret 写入/读取命令必须 redirect output** - 详见 `standards/conventions/secret-hygiene.md`
+
+**规则 #7 要点:** Secret 命令的 stdout/stderr 不得流入 chat-visible 通道。Bash 强制 `>/dev/null 2>&1`; Python 强制 `capture_output=True` 或 `stdout=DEVNULL`。验证用 metadata (status code / 字段 length), 不读 value 字面。Exception 必须 `# secret-leak-ok-explicit` 注释 + owner sign-off。
+
+**触发场景:** `nomad var put/get` / `kubectl create secret` / `vault kv put` / `gh secret set` / `forgejo POST /tokens` / cloud secret manager / DB password commands / `cat <key>` / `echo $SECRET`。
+
+**详细规范 + 正向 pattern:** `standards/conventions/secret-hygiene.md`
```

### 3. Optional: cross-reference in existing memory feedback files

不在本 Spec scope (memory 文件是 user 级 auto-memory 不是 project doc); 但若 owner 希望, 可手工或后续 chore commit 加 `Related: standards/conventions/secret-hygiene.md` 到 `feedback_secrets_never_in_conversation.md` + `feedback_nomad_inspect_secret_leak.md`。

---

## 非目标 (out of scope, deferred to follow-up Specs)

- **Path (3) PreToolUse hook enforcement** — 独立 Level 2-3 Spec; 含 false-positive 调优 / 多 shell 兼容 / regex 维护 / exception annotation 解析。本 Spec 仅 doc 教育路径。Issue #78 §强制路径建议 explicitly suggests "(1)+(3)" but 我们 phase 化以降低单 Spec 风险。
- **Path (2) Skill enforcement** — Issue 显式说 "(2) 中间形态, 但 hook 落地后 (2) 价值降低"。本 Spec 不引入。
- **不修改 aria/.claude-plugin/** — Plugin 本身是 Skills 集合, 不是 methodology rules 载体 (rules 在 standards/)。
- **不修改 aria-orchestrator/** — 这是子项目, 不是 Aria methodology 定义。aria-orchestrator 自身的 CLAUDE.md (如有) 通过 standards/ 共享继承本规则。
- **不写 secret detection regex / scanner** — Path (3) 议题, 本 Spec 不涉及。
- **不引入 secret rotation 调度 / vault 部署** — Aether 已有独立 issue (Aether#32) 和 .aria/decisions/2026-05-02-secret-rotation-deferred.md SOP。

---

## 验收

- [ ] `standards/conventions/secret-hygiene.md` 创建, 含 v1.0.0 frontmatter + 核心条款 + scope 命令清单 + 正向 pattern 示例 + exception annotation 规则
- [ ] 主项目 `/CLAUDE.md` `## 不可协商规则` 章节追加规则 #7 + cross-ref 到 `standards/conventions/secret-hygiene.md`
- [ ] `git mv` not needed (新文件); 现有 standards/conventions/ 文件不动
- [ ] standards 子模块独立 commit + branch + PR
- [ ] 主项目 commit (CLAUDE.md + standards submodule pointer bump + proposal.md)
- [ ] 4 路推送 (origin + github × 2 repos)
- [ ] 2 PRs (standards + main)
- [ ] Forgejo Issue #78 close + comment ref archive + 显式注明 Path (3) hook 仍 open as follow-up
- [ ] follow-up tracking issue: file new Forgejo Issue "secret-hygiene PreToolUse hook enforcement" 或在 Issue #78 close comment 引用之后再 reopen pattern 让 owner 决定

---

## 价值

- **跨项目 SOP 统一**: standards/ 是 Aria methodology 共享层, 任何 aria 规范项目通过 submodule 继承本规则
- **教训机械化**: `feedback_secrets_never_in_conversation` + truffle-hound incident → 可执行 SOP, 不再依赖 memory 个性化
- **未来 hook 路径已铺**: Path (3) hook 落地时 hook 引用本 SOP 命令清单作为 matcher pattern source-of-truth, 不重复定义
- **proportionality 兑现**: Level 2 doc-only ~2-3h, Level 2 audit overhead 最低 (per `feedback_agent_team_for_level1`)
- **owner 体验**: rule #7 在 CLAUDE.md 不可协商规则区, 与 #1-#6 同等强度; AI 每 session SessionStart 加载 CLAUDE.md → 规则进 context

---

## 风险与回滚

| # | 风险 | 影响 | 缓解 |
|---|------|------|------|
| 1 | rule 文字太严格致 owner 调试 secret 时操作不便 | 低 | exception annotation `# secret-leak-ok-explicit` + owner sign-off 提供 escape hatch |
| 2 | scope 命令清单不全, 真实 leak 命令不在列表 | 中 | 清单标注 "non-exhaustive 启发式"; 加 catch-all 原则 ("任何输出 contains secret value 的命令"); Path (3) hook 时用 regex pattern matcher 兜底 |
| 3 | 主 CLAUDE.md rule #7 + 子项目 CLAUDE.md 规则号冲突 | 低 | 主项目独立编号, 子项目继承时通过 "see standards/conventions/secret-hygiene.md" 引用而非编号 |
| 4 | 现存代码已有违反 instances → backfill 工作量 | 低 | 本 Spec 仅 forward-looking; 已发生 leak (4 keys + Aria 内 leaks) 通过 secret rotation 处理 (.aria/decisions/2026-05-02 SOP), 不在本 Spec scope |
| 5 | Path (3) hook 永不落地, 教育路径不足以阻止再发 | 中 | 本 Spec close comment 显式注明 Path (3) 是 follow-up; owner 可后续 prioritize |

**回滚路径**:

- **Level 1 (revert this Spec)**: 反向 git revert standards/ + main repo 改动; Issue #78 reopen
- **Level 2 (rule #7 文字过严)**: minor patch Spec 调整 rule wording, 保留文件存在
- **Level 3 (no-op)**: 不存在 — 本 Spec 全新增内容, 不修改 existing 行为

---

## 实施顺序 (Phase B 内部)

1. **B.2.1** Write `standards/conventions/secret-hygiene.md` v1.0.0 (frontmatter + 5 sections: 条款 / scope / 正向 pattern / exception / 与 Path 3 hook 关系)
2. **B.2.2** Update 主 `/CLAUDE.md` 不可协商规则区, 追加 rule #7 + cross-ref
3. **B.2.3** Self-review (per Level 2 proportionality, 无 multi-agent audit; 检查 markdown 渲染 + cross-ref 链接 valid)
4. **B.2.4** Commit standards submodule
5. **B.2.5** Commit main (CLAUDE.md + Spec proposal + standards submodule pointer bump)
6. **B.2.6** 4-path push + 2 PRs

预估总: ~2-3h (doc-only, no tests, no code)。
