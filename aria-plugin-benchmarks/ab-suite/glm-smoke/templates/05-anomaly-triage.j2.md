{# 场景: 开发者感觉项目/分支"有点不对劲", 想自查 — 典型触发 state-scanner 的异常诊断 #}
你是一位虚构软件项目的开发者。请生成**一段第一人称的口头请求**, 发送给一个 AI 助手, 描述你**察觉到项目/仓库/分支"有点不对劲"** (状态奇怪 / 历史混乱 / 子模块异常 / 改动过多 / 不知道自己怎么到现在这状态), 想让 AI 帮你诊断自查的场景。

## 严格约束

1. **禁止出现任何具体行业/领域名词**, 包括但不限于:
   - 电商 / 博客 / 待办 / 天气 / 聊天机器人 / 社交平台 / CMS / 管理后台 / 论坛 / 地图 / 支付 / 物流 / 教育 / 医疗 / 金融 / 游戏
   - TodoApp / UserService / OrderService / PaymentGateway 等常见练习项目名
2. **禁止描述具体技术细节**, 如 "npm install 报错", "Docker 启动失败", "端口被占" (这些是有明确症状的故障, 不是"感觉不对")
3. 允许模糊不适感词汇: "怪", "不对劲", "乱", "乱套了", "有点飘", "卡住了"
4. 允许状态类描述: "分支状态奇怪", "改动比我记得的多", "子模块看起来不太对", "提交历史有点乱"
5. 语气**疑虑、求诊断、不急**, 口语化
6. **禁止明确指派修复方案** (如 "帮我 rebase", "重置 HEAD") — 本模板的要点是"我不知道咋了, 你看看"
7. 长度 {{ length_min | default(40) }}-{{ length_max | default(100) }} 字
8. 语言: {{ language | default("中文") }}

## 输出格式 (关键)

- 仅输出任务描述本身, 直接以第一人称开头
- **禁止前缀**如 "好的, 这是..."
- **禁止后缀**如 "帮个忙"
- **禁止 markdown 代码块包裹**
- **禁止引号包裹**
- **禁止内心独白 / 思考过程**, 如 "让我想想...", "先分析一下..."

## 风格示例

✅ **正确风格** (仅示范语气, 不要复用具体措辞):

{%- if language == "en" %}
> something feels off with this branch, not sure if I messed up the submodules or what — can you just diagnose it and tell me what's weird
{%- else %}
> 这个分支看着有点不对劲, 也说不清哪里怪, 子模块看起来也乱糟糟的, 你先看一圈告诉我啥情况吧
{%- endif %}

❌ **错误示例** (违反"感觉不对劲"而非"明确故障"的精神):

{%- if language == "en" %}
> docker build is failing on the payment service, help me debug
{%- else %}
> 待办应用的登录接口 500 了, 帮我排查下
{%- endif %}

## 变量种子

seed: `{{ seed | default("e5") }}`
vibe: `{{ vibe | default("unease") }}`

---

现在开始生成:
