{# 场景: 手头有未提交变更, 想要 AI 决定下一步走什么流程 — 典型触发 state-scanner 的工作流推荐 #}
你是一位虚构软件项目的开发者。请生成**一段第一人称的口头请求**, 发送给一个 AI 助手, 描述你**手上已经有一些未提交的变更, 不确定下一步该走什么流程** (提交? 再改? 走评审?) 的场景, 希望 AI 帮你判断。

## 严格约束

1. **禁止出现任何具体行业/领域名词**, 包括但不限于:
   - 电商 / 博客 / 待办 / 天气 / 聊天机器人 / 社交平台 / CMS / 管理后台 / 论坛 / 地图 / 支付 / 物流 / 教育 / 医疗 / 金融 / 游戏
   - TodoApp / UserService / OrderService / PaymentGateway 等常见练习项目名
2. **禁止虚构具体功能名**
3. 允许通用占位: "改了几个文件", "这些变更", "这个修改"
4. 必须暗示**存在未提交/未处理的变更** (如 "刚写完一些", "改了几个文件", "手上这堆东西")
5. 必须暗示**不确定下一步** (如 "不知道直接提交还是...", "不确定该先干啥")
6. 语气**犹豫, 寻求外部判断**, 口语化
7. 长度 {{ length_min | default(40) }}-{{ length_max | default(90) }} 字
8. 语言: {{ language | default("中文") }}

## 输出格式 (关键)

- 仅输出任务描述本身, 直接以第一人称开头
- **禁止前缀**如 "好的, 这是..."
- **禁止后缀**如 "谢谢"
- **禁止 markdown 代码块包裹**
- **禁止引号包裹**
- **禁止内心独白 / 思考过程**, 如 "让我想想...", "先分析一下..."

## 风格示例

✅ **正确风格** (仅示范语气, 不要复用具体措辞):

{%- if language == "en" %}
> just finished a bunch of changes, not sure if I should commit directly or if something else needs to happen first — you tell me
{%- else %}
> 手上改了一堆东西还没提交, 不知道是直接 commit 还是得先走点啥流程, 你帮看看下一步咋办
{%- endif %}

❌ **错误示例** (展示要避免的业务纹理):

{%- if language == "en" %}
> wrote the checkout flow, ready to push to the e-commerce app?
{%- else %}
> 博客的评论功能改完了, 是不是可以直接提交了
{%- endif %}

## 变量种子

seed: `{{ seed | default("c3") }}`
volume_hint: `{{ volume_hint | default("几个文件") }}`

---

现在开始生成:
