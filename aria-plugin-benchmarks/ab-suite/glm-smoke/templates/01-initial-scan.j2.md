{# 场景: 开发者初次打开项目/仓库, 想快速了解整体状态 — 典型触发 state-scanner #}
{# 渲染: 不传任何变量时使用默认值; 可传 {{ seed }} / {{ register }} / {{ length_min }} / {{ length_max }} 增加多样性 #}
你是一位虚构软件项目的开发者。请生成**一段第一人称的口头请求**, 发送给一个 AI 助手, 描述你**刚切换到一个仓库/分支, 想快速了解当前状态**的场景。

## 严格约束

1. **禁止出现任何具体行业/领域名词**, 包括但不限于:
   - 电商 / 博客 / 待办 / 天气 / 聊天机器人 / 社交平台 / CMS / 管理后台 / 论坛 / 地图 / 支付 / 物流 / 教育 / 医疗 / 金融 / 游戏
   - TodoApp / UserService / OrderService / PaymentGateway 等常见练习项目名
2. **禁止虚构具体业务功能**, 如 "登录页 / 购物车 / 用户中心 / 消息推送"
3. 允许使用通用占位: "这个项目", "当前分支", "这个仓库", "我们的代码库"
4. 语气**口语、松散、不正式** (模拟真实开发者随手打字, 非工单风格)
5. 长度 {{ length_min | default(30) }}-{{ length_max | default(80) }} 字
6. 语言: {{ language | default("中文") }}

## 输出格式 (关键)

- 仅输出任务描述本身, 直接以第一人称开头
- **禁止前缀**如 "好的, 这是...", "以下是..."
- **禁止后缀**如 "希望帮到你", "请告诉我..."
- **禁止 markdown 代码块包裹**
- **禁止引号包裹**
- **禁止内心独白 / 思考过程**, 如 "让我想想...", "先分析一下..." (Flash-tier 偶发泄露)

## 风格示例

✅ **正确风格** (仅示范语气, 不要复用具体措辞):

{%- if language == "en" %}
> just switched to this repo and lost track of things, can you take a quick look and tell me where I should pick up
{%- else %}
> 刚切回来这个项目, 忘记上次做到哪了, 先帮我看下现在整体啥情况吧
{%- endif %}

❌ **错误示例** (展示要避免的业务纹理):

{%- if language == "en" %}
> just opened the e-commerce repo, can you check where the shopping cart feature stands
{%- else %}
> 刚打开这个电商项目, 帮我看下购物车模块进展到哪了
{%- endif %}

## 变量种子 (用于避免多次生成重复)

seed: `{{ seed | default("a1") }}`
register: `{{ register | default("casual") }}`

---

现在开始生成:
