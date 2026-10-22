> **版本**: 1.76.0 | **发布日期**: 2026-10-15
| `PostToolUse` + `PostToolUseFailure` | Bash\|Read\|Edit\|Write\|MultiEdit | **secret-scan.sh** | Rule #7 Layer 2 — 检测 secret 形态输出 + 告警（additionalContext/systemMessage）；无法 redact（PostToolUse 架构限制），真实防线 = PreToolUse secret-guard，v1.24.0+ |
# 项目级敏感路径 (可选): <项目根>/.aria/secret-guard.paths
# → 一行一个字面子串 (大小写不敏感, `#` 起首为注释); 只在内建名单之上追加拦截, 不能放宽
# → 条目选最短的特征子串 (如文件名), 不要列完整路径
# → 覆盖内建 Forgejo/Gitea app.ini 规则的读取器集 + Read/Edit; 不覆盖 Grep 工具
# → 文件无效 (超过 32 KiB、超过 200 条、不可读) 时整体忽略, 且静默

# → Claude Code 2.1.285 的 PostToolUse 输出 schema 含 updatedToolOutput — 端到端未验证, 本 hook 不使用
# PostToolUseFailure — 同一扫描也作用于失败工具调用 (非零退出) 的错误文本
