## Claude Code Hook 平台能力调查报告 — WP-A Phase A

**研究环境**: Claude Code v2.1.285 | 项目: /home/dev/Aria (aria-plugin v1.74.1) | 日期: 2026-09-30

---

### 核心发现

#### 1. PostToolUse 无法改写内置工具输出 ✅ (确认)

**文档依据**:  
- hooks-guide.md line 958: "PostToolUse hooks can't undo actions since the tool has already executed"
- secret-scan.sh line 18-23: 明确声明"It CANNOT redact or rewrite the tool output"
- 不存在 `updatedToolOutput` 字段用于内置工具

**可用替代**:
- `hookSpecificOutput.additionalContext` → 注入到 Claude 上下文(system reminder)
- `systemMessage` → 用户终端告警
- 两个通道都是**事后信息补充**, 无法改变已执行的工具输出

**对 WP-A 的含义**:  
L3 tripwire 的设计依赖这一约束 — "检测+告警+轮换" 而非"检测+阻止"。PostToolUse 适合在 secret-scan.sh 中补通用 JSON 凭据键形模式(无需改写),仅需补充正则到 PATTERNS 数组。

---

#### 2. PreToolUse 的 `updatedInput` 能改写 Bash 命令 ✅ (支持)

**文档依据**:  
- hooks-guide.md line 963: "When multiple PreToolUse hooks return updatedInput to rewrite a tool's arguments, the last one to finish takes effect"
- 支持改写 `tool_input.command` 字段

**注意事项**:
- 多 hook 并行时, **最后完成的改写生效** (非确定性顺序)
- 改写仅在允许工具继续执行时有效(未返回 `deny`)
- 版本信息: 至少在 v2.1.x 中支持,无具体"起始版本"记录

**对 Aria#221 的评估**:
- ⚠️ 技术可行(能改写 jq 命令从 `map_values(length)` → `keys`)
- ❌ 语义危险(自动改写违反用户意图)
- ✅ 更优方案: 扩大 secret-guard 的 jq 白名单(如添加 `map_values(length)` / `length` 等)

---

#### 3. PostToolUse 输出通道的可见性与中断能力

| 通道 | 目标 | 呈现方式 | 中断模型 | 能否改写输出 |
|------|------|--------|--------|----------|
| `additionalContext` | Claude(模型) | System reminder 注入上下文 | ❌ 不中断 | ❌ 否 |
| `systemMessage` | User(终端) | 系统告警行 | ❌ 不中断 | ❌ 否 |
| `decision: "block"` | — | — | ❌ 无效 | ❌ 否 |

**关键约束**: 
- `decision: "block"` 在 PostToolUse 中**无效**(tool 已执行,无法撤销)
- `additionalContext` 只能补充信息,无法重写上下文中的已有值
- Exit code 2 也无法阻止(tool 已完成)

---

#### 4. Hook 进程的环境与配置访问

**可用的环境变量**:
- `$CLAUDE_PROJECT_DIR` — 项目根目录
- `$CLAUDE_PLUGIN_ROOT` — 插件安装目录
- `$HOME` / `$USER` / `$PWD` / `$cwd` — 标准 shell 变量

**项目级配置读取**:
- 推荐: 使用 `$CLAUDE_PROJECT_DIR/.aria/` 下的配置文件
- 实现: secret-guard.sh 通过环境变量(如 `SECRET_GUARD_ACK_PATH`)读取动态指示

---

#### 5. Hook 超时与 Fail-Open/Fail-Closed 行为

**超时配置** (hooks.json 中可覆盖 `timeout` 字段):
- command/http/mcp_tool: 10 分钟(默认)
- prompt: 30 秒
- agent: 60 秒
- UserPromptSubmit/PreModelSwitch/PostModelSwitch: 30 秒(特殊)

**Fail 策略**:
- **PreToolUse (secret-guard.sh)**: Fail-Closed
  - 缺 jq 时 `exit 2` 阻止所有 Bash 命令
  - 理由: 错误拒绝 < 错误允许
  
- **PostToolUse (secret-scan.sh)**: Fail-Open
  - 缺 jq 时 `exit 0` 跳过检测
  - 理由: tool 已执行,阻止无意义

---

#### 6. Claude Code 内置 Secret 脱敏/检测

**现状** (v2.1.285):
- ❌ 无内置工具输出自动脱敏
- ❌ 无内置 secret 形状检测
- 工具输出完全呈现给模型

**框架层理由**: 脱敏需求因组织而异,框架无法通用;此故 Aria 采分层防御:
- L1 (PreToolUse): secret-guard.sh 阻止风险命令
- L2 (Wrapper): Aether forgejo wrapper 脱敏已知端点
- L3 (PostToolUse): secret-scan.sh 检测+告警

---

#### 7. 现有实现的正确性核查

**secret-guard.sh (PreToolUse)** ✅ 仍然正确
- 使用 `exit 2` + stderr (line 691, 712) — 标准拒绝方式
- Fail-Closed 设计 (line 517) — 符合安全敏感场景需要
- **无需改用 JSON `permissionDecision`** (当前实现有效)

**secret-scan.sh (PostToolUse)** ✅ 仍然正确
- 使用 `additionalContext` + `systemMessage` (line 369-374) — 符合 PostToolUse 约束
- Fail-Open 设计 (line 109) — 合理
- 明确不改写输出 (line 367) — 符合架构限制

---

### 对 WP-A (Level 2 Spec) 的设计决策依据

#### aria-plugin#154 (L3 tripwire — JSON 键形缺口)
- ✅ **可行**: PostToolUse 已是检测框架,仅需补通用 JSON 键模式 (如 `"(token|secret|password)"[..].{8,}`)
- ✅ **无需改写**: 依赖 additionalContext 告警供 Claude 拒绝重复值
- ✅ **FP 处理**: 补充 FAKE/PLACEHOLDER 白名单避免测试套件恒红

#### aria-plugin#203 (L1 旁路 — 配置文件+变量)
- ⚠️ **路径间接旁路**: 服务端配置文件名单不完整(如 /etc/forgejo/app.ini)
  - 改法 A: 补配置文件清单 + 项目级扩展入口
  - 改法 B: **不用改写**, 这正是 L3 tripwire 要防的场景
  
#### Aria#221 (L1 假阳性 + 真缺口)
- ✅ **假阳性 1**: `\.env` 改为 `\.env([^A-Za-z0-9_]|$)` (避免匹配 `os.environ`)
- ✅ **假阳性 2**: 扩大 jq 白名单 (加 `map_values(length)` / `length` / `keys_unsorted` 等)
- ❌ **真缺口**: 进程列举(ps,pgrep)能暴露其他进程命令行参数中的凭据
  - 需要独立的 secret-guard 规则拦截 ps 完整命令列的输出

---

### 关键技术限制 (项目决策边界)

1. **PostToolUse 的不可逆性**: 工具已执行,无法撤销。`additionalContext` 是事后补救,非防护
2. **Hook 的非确定性序**: 多 PreToolUse hook 的 `updatedInput` 顺序随机,不可依赖编排
3. **黑名单的开放性**: PreToolUse 预防力只覆盖已知模式;新端点/绕过无预防, L3 tripwire 补空白
4. **权限决策的最终裁决**: Hook 的改写在权限检查前,但权限规则的最终裁决生效(Hook 无权改变)

---

### 代码出处与验证

**官方文档**:
- https://code.claude.com/docs/en/hooks-guide.md line 891, 958, 963

**项目代码验证**:
- `/home/dev/Aria/aria/hooks/secret-guard.sh` line 18-23 (fail-closed), line 517 (jq 缺失), line 676-691 (stderr 输出)
- `/home/dev/Aria/aria/hooks/secret-scan.sh` line 18-23 (无法 redact), line 107-109 (fail-open), line 363-375 (两通道实现)

**背景 Issue**:
- 10CG/aria-plugin#154 (L3 tripwire 模式缺口)
- 10CG/aria-plugin#203 (L1 旁路: 服务端配置+变量)
- 10CG/Aria#221 (L1 旁路: 进程列举+假阳性)

---

### 后续行动 (不在本研究范围内)

- WP-A 设计阶段: 已提供技术事实依据,ready for Phase B coding
- L3 tripwire: 补 pattern + FP 白名单 (secret-scan.sh 改动)
- L1 旁路补洞: secret-guard 规则扩展(配置文件+进程列举+FP 边界修复)
- Rule #6 benchmark: 按 decision sheet 第 3 项采用 substitute + baseline-failing 测试
"