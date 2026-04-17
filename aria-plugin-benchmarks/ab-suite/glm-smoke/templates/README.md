# GLM Smoke Templates — 拟人 Prompt 生成模板

> **Spec**: `openspec/changes/aria-2.0-m0-prerequisite/tasks.md` §T3.4
> **目的**: 用 GLM 5.1 API 从模板生成 5 条合成 prompt, 跑 `claude -p` 触发 state-scanner, 二值化验证 headless plugin 在容器内的可用性
> **路由**: Luxeno (`LUXENO_API_KEY` / `glm-4.7-flashx`); 参见 AD-M0-8

---

## 模板契约

### 禁止业务纹理 (Hard Constraint)

**禁用所有具体行业/领域名词**, 防止 prompt 被特定业务语料污染使其更容易/更难触发:

- ❌ 电商 / 博客 / 待办 / 天气 / 聊天机器人 / 社交平台 / CMS / 管理后台
- ❌ TodoApp / UserService / OrderService / PaymentGateway 等常见练习项目名
- ❌ 金融 / 医疗 / 教育 / 游戏等行业上下文
- ✅ 通用占位: "这个项目", "当前分支", "这个仓库", `{{my_project}}` (留空由 GLM 填充无意义代号)

### 模板格式

每个模板是一个 Jinja2 文件 (`.j2.md`), 包含:

1. **系统指令** (给 GLM): 生成什么样的用户输入
2. **约束条件**: 禁用词 / 长度 / 语气 / 风格
3. **输出格式**: 仅输出拟人任务描述本身 (GLM 常见毛病是输出 "好的, 这是..." 前缀, 要显式禁止)
4. **变量占位**: `{{ seed }}` 等让相同模板产出多样化

### 5 类场景 (覆盖 state-scanner 触发轴线)

| 模板 | 场景 | 典型触发 |
|------|------|----------|
| `01-initial-scan.j2.md` | 初次打开项目, 想了解整体状态 | "看一下现在什么情况" |
| `02-resume-after-break.j2.md` | 暂别一段时间回来, 想知道接续点 | "上次做到哪了" |
| `03-pre-action-guidance.j2.md` | 手上有变更, 想要 AI 决定下一步 | "帮我看下该做啥" |
| `04-ambiguous-request.j2.md` | 模糊请求, 不明确指向任何 phase | "继续" / "走一遍" |
| `05-anomaly-triage.j2.md` | 感觉哪里不对, 想自查 | "这个分支有点怪" |

### 二值化判定

- **Pass**: `claude -p "<generated-prompt>"` 输出 grep 命中 `current_phase:` (state-scanner 被触发 + 输出结构化 YAML)
- **Fail**: 4 种 failure_mode
  - `not_triggered`: state-scanner 未启动
  - `triggered_empty_yaml`: 启动但 YAML 为空
  - `triggered_invalid_yaml`: 启动但 YAML 格式错误
  - `partial_response`: 回答偏离 state-scanner 输出格式
  - `timeout`: 超时

**阈值**: 5 条中 ≥ 4 条 pass = T3.4 通过 → 继续 M0 Phase D
**失败**: < 4 条 pass = 升级 R8 评估

---

## 执行协议

```bash
# 1. 从每个模板生成 prompt (GLM via Luxeno)
for tpl in templates/*.j2.md; do
  prompt=$(python3 scripts/render-template.py "$tpl" | \
           curl -s https://api.luxeno.ai/v1/chat/completions \
             -H "Authorization: Bearer $LUXENO_API_KEY" \
             -d @-)
  echo "$prompt" > failed-samples/$(date +%s)-$(basename "$tpl" .j2.md).txt
done

# 2. 每条 prompt 喂 claude -p (容器内)
for p in failed-samples/*.txt; do
  docker exec aria-runner claude -p --plugin-dir /opt/aria-plugin "$(cat "$p")" > "$p.output"
  if grep -q "current_phase:" "$p.output"; then
    echo "PASS: $p"
  else
    echo "FAIL: $p"
  fi
done

# 3. 汇总 summary.yaml
python3 scripts/summarize-t3.4.py > failed-samples/summary.yaml
```

---

## 审核 (T3.5)

- **ai-engineer** (自动): 检查模板是否含禁用词
- **legal-advisor** (人类必签): 确认无业务纹理泄露
- 审核结果写入 `templates/REVIEW.md`, 产品负责人签字后才能用于 T3.4

---

## 归档 Schema

`failed-samples/<timestamp>-<seq>.yaml`:

```yaml
prompt: "<generated-prompt>"
failure_mode: not_triggered | triggered_empty_yaml | triggered_invalid_yaml | partial_response | timeout
raw_output: "<claude -p stdout>"
expected_grep: "current_phase:"
glm_model_version: "glm-4.7-flashx"
status: pass | fail
```

---

**最后更新**: 2026-04-16
**维护**: 10CG Lab
