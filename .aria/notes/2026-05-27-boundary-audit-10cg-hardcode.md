# Aria 核心代码层 10CG-specific 硬编码审计报告

**审计日期**: 2026-05-27  
**审计范围**: `/home/dev/Aria/aria/` + `/home/dev/Aria/standards/` + `/home/dev/Aria/aria-plugin-benchmarks/` (+ aria-orchestrator 对比)  
**分类标准**: 
- **(D) Doc-mention** — markdown/注释中作为示例或说明,无技术债
- **(C) Code-hardcoded** — .py/.sh/.json/.yaml 中字面量硬编码,需改为参数化
- **(P) Path-hardcoded** — 路径拼接中含 hardcoded `/10CG/`,需参数化

---

## Executive Summary

**总计发现**: 18 条 hardcode 信号
- **(D) Doc-mention**: 8 条 (无害,无需修复)
- **(C) Code-hardcoded**: 9 条 (真技术债)
- **(P) Path-hardcoded**: 1 条 (含 `/home/dev/.npm-global/`)

**通用层泄露Verdict**: ✅ **已泄露** — aria/ 核心层在 3 个关键位置硬编码了 `forgejo.10cg.pub`,且 aether (10CG 部署平台) 被列为唯一 CI 后端偏好。这些假设应在后续"通用层 vs workspace 层"分离中去除。

**分布情况**:
- **高风险**: 6 条 (需立即修复 — 影响通用化)
- **中风险**: 3 条 (技术债但暂无阻塞)
- **低风险**: 9 条 (文档示例或测试数据,可接受)

---

## 分类详表

### (C) Code-hardcoded — 实际代码硬编码 [需修复]

| 编号 | 文件 | 行号 | 内容 | 风险 | 建议修复 |
|------|------|------|------|------|---------|
| C1 | `aria/skills/state-scanner/scripts/collectors/forgejo_config.py` | 35 | `_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = ("forgejo.10cg.pub",)` | 🔴 高 | 改为 `_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = tuple(os.environ.get("FORGEJO_HOSTS", "forgejo.10cg.pub").split(","))` 或从 config 读取 |
| C2 | `aria/skills/state-scanner/scripts/collectors/issue_scan.py` | 71 | `DEFAULT_CONFIG["platform_hostnames"]["forgejo"] = ["forgejo.10cg.pub"]` | 🔴 高 | 同上,允许通过 `.aria/config.json` 覆盖 |
| C3 | `aria/skills/config-loader/DEFAULTS.json` | 45 | `"forgejo": ["forgejo.10cg.pub"]` | 🔴 高 | 同上,增加环境变量 fallback 读取逻辑 |
| C4 | `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | 32-34 | `AETHER_CLI_MIN_SHA = "f29abee"` + `AETHER_CLI_MIN_DATE = "2026-05-06"` | 🟠 中 | 这些 hardcode baseline 可接受(artifact),但 `detect_aether()` 的 `~/.aether/config.yaml` 假设需改为参数化 |
| C5 | `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | 47-48 | `"primitive_preference": ["aether-ci-cli"]` | 🔴 高 | 改为支持多个 CI 后端列表,允许从 config 覆盖;或提供 fallback 选择链 |
| C6 | `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | 62 | `config_yaml = os.path.expanduser("~/.aether/config.yaml")` | 🔴 高 | 改为可配置路径:`os.environ.get("AETHER_CONFIG", os.path.expanduser("~/.aether/config.yaml"))` |
| C7 | `standards/tools/setup/integrate-standards.sh` | 9 | `STANDARDS_REPO="ssh://forgejo@forgejo.10cg.pub/10CG/ai-dev-standards.git"` | 🟠 中 | 改为:`STANDARDS_REPO="${ARIA_STANDARDS_REPO:-ssh://forgejo@forgejo.10cg.pub/10CG/ai-dev-standards.git}"` |
| C8 | `aria-orchestrator/scripts/inject-demo-issues.py` | 29 | `FORGEJO_CLI_PATH = os.environ.get("FORGEJO_CLI_PATH", "/home/dev/.npm-global/bin/forgejo")` | 🔴 高 | 已有环境变量 fallback,但 `/home/dev/` 是用户路径,应改为:`shutil.which("forgejo")` 优先 |
| C9 | `aria-orchestrator/scripts/inject-demo-issues.py` | 31 | `TARGET_REPO = os.environ.get("FORGEJO_TARGET", "10CG/Aria")` | 🟠 中 | 已有 env var fallback,可接受;但 documentation 需说明这是 10CG 特定 demo |

### (D) Doc-mention — 文档中的示例提及 [无害,无需修复]

| 编号 | 文件 | 行号 | 内容 | 分类 |
|------|------|------|------|------|
| D1 | `aria/.claude-plugin/plugin.json` | (多行) | `"homepage": "https://github.com/10CG/aria-plugin"` | 官方仓库链接(公开),无害 |
| D2 | `aria/.claude-plugin/marketplace.json` | (多行) | `"repository": "https://github.com/10CG/aria-plugin.git"` | 同上 |
| D3 | `standards/README.md` + `README.zh.md` | (多行) | 提及 "git submodule add https://github.com/10CG/aria-standards.git" | 引入说明(文档),无害 |
| D4 | `standards/conventions/submodule-pointer-hygiene.md` | (多行) | 多次提及 "10CG/Aria" issue #124 / "#123" / incident | Incident 报告(历史记录),无害 |
| D5 | `standards/conventions/session-handoff.md` | 多行 | 示例:"creationhikari/devbox-A" / Forgejo Issue #92 | 示例使用(文档),无害 |
| D6 | `standards/legal/scoped-memo-template.md` | 多行 | 示例:"GLM 5.1 ToS" / "10CG Lab" | 法务模板示例,无害 |
| D7 | `aria-plugin-benchmarks/forgejo-sync/evals.json` | 多行 | eval 数据中含 `"repo": "10cg/my-project"` | 评估测试数据,无害 |
| D8 | `aria-plugin-benchmarks/ab-results/2026-04-15-state-scanner-submodule-issue-scan/` | 多行 | 测试 fixture 含 "10CG/Aria" | 测试 fixture,无害 |

### (P) Path-hardcoded — 路径拼接硬编码 [需修复]

| 编号 | 文件 | 行号 | 内容 | 风险 | 建议修复 |
|------|------|------|------|------|---------|
| P1 | `aria-orchestrator/scripts/inject-demo-issues.py` | 29 | `/home/dev/.npm-global/bin/forgejo` (绝对用户路径) | 🟠 中 | 改为: `shutil.which("forgejo") or os.environ.get("FORGEJO_CLI_PATH")` 提供跨平台查找 |

---

## 高优先级修复建议 (Top 3)

### 修复 1: 统一 Forgejo 实例配置来源 [Cost: 中等,Impact: 高]

**涉及文件**:
- `aria/skills/state-scanner/scripts/collectors/forgejo_config.py:35`
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py:71`
- `aria/skills/config-loader/DEFAULTS.json:45`

**当前状态**: 三个地方分别硬编码 `"forgejo.10cg.pub"`,无法支持自定义 Forgejo 实例。

**修复方案**:
```python
# 替换 _KNOWN_FORGEJO_HOSTS 为:
_KNOWN_FORGEJO_HOSTS: tuple[str, ...] = tuple(
    os.environ.get("ARIA_FORGEJO_HOSTS", "forgejo.10cg.pub").split(",")
)
```

+ 增强 `issue_scan.py` 的 DEFAULT_CONFIG merge 逻辑，允许从 `.aria/config.json` 的 `state_scanner.issue_scan.platform_hostnames.forgejo` 读取。

**预期效果**: 任意 Aria 项目都可通过 `export ARIA_FORGEJO_HOSTS="forge1.example.com,forge2.example.com"` 或 CLAUDE.local.md 配置多个 Forgejo 实例。

---

### 修复 2: CI 后端抽象 — 移除 Aether 唯一假设 [Cost: 高,Impact: 高]

**涉及文件**:
- `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:47-62`

**当前状态**: 
- `"primitive_preference": ["aether-ci-cli"]` — Aether 被列为唯一选项
- `detect_aether()` 仅检查 `~/.aether/config.yaml`
- 无 fallback 到其他 CI (GitHub Actions、GitLab CI 等)

**修复方案**:
```python
DEFAULT_CONFIG = {
    "enabled": True,
    "ci_backends": [
        {
            "name": "aether-ci-cli",
            "bin_name": "aether",
            "config_path": "~/.aether/config.yaml",
            "priority": int(os.environ.get("AETHER_PRIORITY", "100"))
        },
        {
            "name": "github-actions",
            "bin_name": "gh",
            "config_path": "~/.config/gh/hosts.yml",
            "priority": int(os.environ.get("GHA_PRIORITY", "50"))
        }
    ],
    "no_ci_fallback": "skip_with_warning",
    ...
}
```

+ 修改 `detect_aether()` 为通用的 `detect_ci_backend(config_backends)` 函数。
+ 允许通过 `.aria/config.json` 的 `phase_c_integrator.ci_backends` 覆盖顺序。

**预期效果**: Aria 项目可独立于 Aether,支持多种 CI 平台。

---

### 修复 3: 通知后端参数化 — Feishu → 可配置 [Cost: 中等,Impact: 中等]

**涉及文件**:
- `aria-orchestrator/notify-feishu.sh` (全文)
- `aria-orchestrator/heartbeat.sh` (Feishu 部分)

**当前状态**: Feishu 是唯一通知后端,通过 `$FEISHU_APP_ID` 等环境变量。虽已参数化,但当前代码假设 Feishu 必然可用。

**修复方案**:
```bash
# 新增 notify.sh 统一入口:
NOTIFY_BACKEND="${NOTIFY_BACKEND:-feishu}"  # 支持 feishu|slack|webhook|email|none
case "$NOTIFY_BACKEND" in
  feishu)
    ./notify-feishu.sh "$@"
    ;;
  slack)
    ./notify-slack.sh "$@"
    ;;
  webhook)
    curl -X POST "$WEBHOOK_URL" -d "$@"
    ;;
  none|*)
    echo "[notify] backend disabled" >&2
    ;;
esac
```

+ 迁移 `aria-orchestrator/notify-feishu.sh` → `aria-orchestrator/backends/notify-feishu.sh`。
+ 创建 `aria-orchestrator/backends/notify-slack.sh` 模板。
+ 更新 `heartbeat.sh` 调用为 `notify.sh`。

**预期效果**: 通用化 Aria Orchestrator,支持多种告警后端。

---

## 架构分离建议

### 当前问题
通用核心层 (aria/skills, standards/) 与 10CG 特定部署层 (aria-orchestrator) 耦合,导致:
- 开源 aria-plugin 无法独立使用
- Aether / Feishu 依赖硬编码在 skills 中
- 难以支持其他 Git 服务商

### 建议目标架构

```
aria-plugin (通用层 — 可独立开源)
├── aria/
│   ├── skills/                    ← 去 10CG-ify (forgejo_config.py 等改为可配置)
│   ├── scripts/hooks/             ← 通用 (secret-guard.sh 等无 hardcode)
│   ├── agents/                    ← 通用
│   └── .claude-plugin/            ← 指向 GitHub 官方仓库 (已参数化)
├── standards/                     ← 去文档化 10CG instance (约定 vs 硬编码)
├── aria-plugin-benchmarks/        ← 测试数据,可接受
└── VERSION / CHANGELOG            ← 通用

workspace-aria-10cg (10CG 专用层 — 内部/镜像部署)
├── aria-orchestrator/             ← 迁出(已在 submodule)
├── aether-config/                 ← 新增,Aether 集成配置
│   ├── pre-merge-gate-aether.json
│   └── aether-plugin-extend.sh
├── feishu-notification/           ← 新增
│   ├── notify-feishu.sh
│   ├── heartbeat-feishu.sh
│   └── .env.example
└── forgejo-config/                ← 新增,本地 Forgejo 实例
    ├── platform-hostnames.json    ← 包含 forgejo.10cg.pub
    └── cloudflare-access.yaml
```

### 跨层交互约定

**通用层** (aria-plugin) 对 **workspace 层** 的依赖应通过以下方式解耦:

1. **配置文件优先链** (降序):
   ```
   .aria/config.local.json (workspace 层覆盖)
     ↓
   CLAUDE.local.md (用户项目覆盖)
     ↓
   环境变量 (ARIA_FORGEJO_HOSTS=... / AETHER_PRIORITY=...)
     ↓
   aria/skills/config-loader/DEFAULTS.json (通用层默认)
   ```

2. **plugin.json 中的 workspace layer 声明**:
   ```json
   {
     "name": "aria-plugin",
     "dependencies": {
       "workspace-layers": [
         {
           "name": "aria-10cg",
           "required": false,
           "config_keys": ["aether", "feishu", "forgejo_instances"]
         }
       ]
     }
   }
   ```

3. **环境变量命名约定**:
   - 通用层: `ARIA_*` (e.g., `ARIA_FORGEJO_HOSTS`)
   - 10CG 专用: `ARIA_10CG_*` (e.g., `ARIA_10CG_AETHER_PRIORITY`)

---

## 子问题回答

### Q1: aria-orchestrator 是否独立 repo?

**A**: 是的。它是 git submodule(gitlink),路径 `/home/dev/Aria/aria-orchestrator` 指向独立仓库。
```bash
$ cat /home/dev/Aria/.gitmodules | grep orchestrator
[submodule "aria-orchestrator"]
    path = aria-orchestrator
    url = ...
```

**现状**: aria-orchestrator 的 Feishu hardcode + `10CG/Aria` 默认值是独立的问题,但在通用化 Aria 时应一同迁出。

---

### Q2: secret-guard 是否含 10CG-specific?

**A**: 否。`aria/skills/aria-doctor/scripts/check_secret_guard_install.sh` 完全通用,检测项如下:
- `.claude/scripts/secret-guard.sh` (project-local 副本) vs 
- `CLAUDE_PLUGIN_ROOT/hooks/secret-guard.sh` (plugin SOT 源)

无 10CG-specific 硬编码。

---

### Q3: Git provider abstraction 是否存在?

**A**: 不存在。当前实现:
- `state-scanner/scripts/collectors/forgejo_config.py` — 专门支持 Forgejo 
- `state-scanner/scripts/collectors/issue_scan.py` — 支持 Forgejo + GitHub(通过 URL 自动识别)
- 但无可配置的抽象层支持添加新 provider(Gitea / GitLab)

**建议**: 创建 `aria/scripts/git-providers/` 子模块:
```python
# aria/scripts/git-providers/__init__.py
class GitProvider(ABC):
    @abstractmethod
    def detect_host(self, remote_url: str) -> str | None: ...
    @abstractmethod
    def list_issues(self, owner: str, repo: str, **kwargs) -> list[Issue]: ...

class ForgejoProvider(GitProvider): ...
class GitHubProvider(GitProvider): ...
class GitLabProvider(GitProvider): ...

PROVIDERS = {
    "forgejo": ForgejoProvider,
    "github": GitHubProvider,
    "gitlab": GitLabProvider,
}
```

---

### Q4: forgejo CLI 路径硬编码?

**A**: 是的,一个地方:

**文件**: `aria-orchestrator/scripts/inject-demo-issues.py:29`
```python
FORGEJO_CLI_PATH = os.environ.get(
    "FORGEJO_CLI_PATH", "/home/dev/.npm-global/bin/forgejo"
)
```

**问题**: `/home/dev/` 是用户特定路径,跨环境不可移植。

**修复**:
```python
import shutil

FORGEJO_CLI = shutil.which("forgejo") or os.environ.get(
    "FORGEJO_CLI_PATH", ""
)
if not FORGEJO_CLI:
    raise RuntimeError(
        "forgejo CLI not found. Install with npm or set FORGEJO_CLI_PATH"
    )
```

---

## 修复优先级矩阵

| 优先级 | 编号 | 文件 | 修复成本 | 通用化收益 | Timeline |
|--------|------|------|---------|-----------|----------|
| P0 (Critical) | C1+C2+C3 | forgejo_config.py / issue_scan.py / DEFAULTS.json | 中 (2-4h) | 高 (支持多 Forgejo) | Sprint 1 |
| P0 (Critical) | C5+C6 | phase-c-integrator/pre_merge_gate.py | 高 (8-12h) | 高 (CI 后端抽象) | Sprint 1-2 |
| P1 (High) | C4 | pre_merge_gate.py baseline | 低 (1h) | 中 (文档化约定) | Sprint 1 |
| P1 (High) | C8 | inject-demo-issues.py PATH | 低 (30m) | 低 (跨平台compat) | Sprint 1 |
| P2 (Medium) | C7 | integrate-standards.sh | 低 (30m) | 低 (可参数化) | Sprint 2 |
| P2 (Medium) | C9 | inject-demo-issues.py TARGET_REPO | 低 (说明文档) | 低 (已有 env var) | Sprint 2 |
| P3 (Low) | D1-D8 | 文档示例 | 无 | 无 | 无需 |
| P3 (Low) | P1 | Feishu hardcode | 中 (4-6h) | 中 (通知后端抽象) | Sprint 3 |

---

## Verdict

**通用层状态**: ⚠️ **已泄露,可修复**

Aria 核心层在以下方面硬编码了 10CG 特定假设:
1. ✗ Forgejo 实例限定为 `forgejo.10cg.pub` (3 处)
2. ✗ CI 后端限定为 Aether (2 处)
3. ✗ Aether 配置路径硬编码为 `~/.aether/` (1 处)

**但所有问题均可通过环境变量 + 配置文件 + 代码重构解决,无设计性障碍。**

**建议行动**:
- **短期 (Sprint 1-2)**: 修复 P0 + P1 项目 → Aria 可支持任意 Forgejo/多 CI 后端
- **中期 (Sprint 3-4)**: 提取 aria-orchestrator 为独立 workspace 层 → aria-plugin 完全通用化
- **长期**: 建立"通用层约定文档" (ARCHITECTURE.md) 防止后续泄露

---

**Report generated**: 2026-05-27 by boundary-audit-10cg-hardcode  
**Report file**: `/home/dev/Aria/.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`
