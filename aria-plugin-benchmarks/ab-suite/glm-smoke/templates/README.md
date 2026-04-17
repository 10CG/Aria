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

- **Pass**: `claude -p "<generated-prompt>"` 输出 grep 命中 `Phase/Cycle:` (人类可读格式) 或 `phase_cycle:` (内部 YAML key) — state-scanner 被触发 + 输出结构化状态
- **正则**: `grep -E "Phase/Cycle:|phase_cycle:"` (双格式容忍, 见 T3.5 AI 预审 Finding #1)
- **Fail**: 5 种 failure_mode
  - `not_triggered`: state-scanner 未启动
  - `triggered_empty_yaml`: 启动但 YAML 为空
  - `triggered_invalid_yaml`: 启动但 YAML 格式错误
  - `partial_response`: 回答偏离 state-scanner 输出格式
  - `timeout`: 超时

**阈值**: 5 条中 ≥ 4 条 pass = T3.4 通过 → 继续 M0 Phase D
**失败**: < 4 条 pass = 升级 R8 评估

---

## 执行协议 (🔶 ILLUSTRATIVE — 实际脚本待 T3.4 真跑前补齐)

以下代码块为**示意性伪代码**, 演示整体数据流。实际 T3.4 真跑前需补齐:

- `scripts/render-template.py` — Jinja2 渲染 (将 `.j2.md` + 变量 → 系统 prompt)
- `scripts/run-glm-smoke.sh` — 编排: 5 轮 (render → Luxeno API → claude -p → grep)
- `scripts/summarize-t3.4.py` — 汇总 summary.yaml

```bash
# 伪代码 — 展示数据流, 不可直接跑

# 1. 渲染模板 + 调 Luxeno (GLM-4.7-flashx) 生成拟人 prompt
for tpl in templates/*.j2.md; do
  system_prompt=$(python3 scripts/render-template.py "$tpl")
  payload=$(python3 -c "import json,sys; print(json.dumps({
    'model': 'glm-4.7-flashx',
    'messages': [{'role': 'user', 'content': sys.argv[1]}],
    'temperature': 0.8,
    'max_tokens': 200
  }))" "$system_prompt")
  response=$(curl -sS --max-time 30 https://api.luxeno.ai/v1/chat/completions \
             -H "Authorization: Bearer $LUXENO_API_KEY" \
             -H "Content-Type: application/json" \
             -d "$payload")
  prompt=$(python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])" <<< "$response")
  echo "$prompt" > "failed-samples/$(date +%s)-$(basename "$tpl" .j2.md).txt"
done

# 2. 每条 prompt 喂 claude -p (aria-runner 容器内; Nomad parameterized dispatch)
for p in failed-samples/*.txt; do
  output=$(docker exec -i \
    --user claude \
    -e LUXENO_API_KEY="$LUXENO_API_KEY" \
    aria-runner \
    claude -p --plugin-dir /opt/aria-plugin "$(cat "$p")")
  echo "$output" > "$p.output"
  if grep -qE "Phase/Cycle:|phase_cycle:" "$p.output"; then
    echo "PASS: $p"
  else
    echo "FAIL: $p"
  fi
done

# 3. 汇总 summary.yaml
python3 scripts/summarize-t3.4.py failed-samples/ > failed-samples/summary.yaml
```

**Luxeno API payload 说明**:
- 符合 OpenAI `/chat/completions` schema (Portkey gateway 透传)
- `temperature=0.8` 保证 5 条之间有多样性
- `max_tokens=200` 足够覆盖所有模板的长度约束 (最长 40-100 字 ≈ 200 token)

**Docker exec 说明**:
- `-i` 必需 (stdin 不连 TTY, 因 `-t` 在 headless 下报错)
- `--user claude` 对齐 Dockerfile 非 root 用户 (T3.3 约束)
- `-e LUXENO_API_KEY` 注入运行时 env (Nomad dispatch 场景下由 template 注入)

---

## 审核 (T3.5)

- **ai-engineer** (自动): 检查模板是否含禁用词 + Jinja2 正确性 + GLM 友好度 + 覆盖度 + 执行协议正确性
- **legal-advisor** (人类必签): 确认无业务纹理泄露 + 授权 T3.4 真跑
- 审核结果写入 `templates/REVIEW.md`, 产品负责人签字后才能用于 T3.4

---

## 归档 Schema

`failed-samples/<timestamp>-<seq>.yaml`:

```yaml
prompt: "<generated-prompt>"
failure_mode: not_triggered | triggered_empty_yaml | triggered_invalid_yaml | partial_response | timeout
raw_output: "<claude -p stdout>"
expected_grep: "Phase/Cycle:|phase_cycle:"
glm_model_version: "glm-4.7-flashx"
status: pass | fail
```

---

## 变量命名空间 (Minor)

当前默认 seed 值 `a1/b2/c3/d4/e5` 互斥, 但若 render 时通过 CLI 传 `--seed X` 会全局覆盖所有模板的默认值。建议渲染器实现 **per-template seed namespacing**: e.g. `--seed-01=X --seed-02=Y`, 或使用 `{{ run_id }}_{{ seed }}` 复合键。

---

**最后更新**: 2026-04-16 (T3.5 AI 预审 Finding #1-#9 全部修复)
**维护**: 10CG Lab
