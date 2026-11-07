# 执行器修复交付证据与访问边界

> **版本**: aria-plugin v1.78.0
> **范围**: 原执行器修复的实现、配置采用与发布证明；不含推荐机制change实现，不恢复PR #38。

## 1. 已交付产品

插件master合并提交`2d8e223f2d7ae03ff07a9ddde67290704ac2f231`与tag`v1.78.0`均已逐端核验origin/GitHub一致。原Phase B提交`3ed43ff`作为真实祖先保留，主仓历史gitlink不依赖未发布对象。

Guard默认false维持旧入口；显式true启用固定团队、逐席原生计时、参与集合可比性、固定scope与来源闭包以及collect/check消费链。仅读取兼容已识别的legacy模式字段，原报告字节不改；当前scope旧周期、真实矛盾、未知归属与读取不完整仍按契约拒绝。

## 2. 原验收与新修订分开记录

| 证明用途 | 原证据入口 | 本次新增/补充 |
|---|---|---|
| SC-1/SC-7真实接线与消费者 | `probe-evidence.json`的实际链与authoritative_state | 新host真实仓build已记录legacy解释；不要求另一个Spec先收敛 |
| SC-2/SC-3/SC-4/SC-5/SC-6边界与负控 | `unit-evidence.json`、`negative-controls-evidence.json`及原接受索引 | `release-compatibility-evidence.json`：56项相关回归、非作者两类坏实现CAUGHT、原件hash不变 |
| SC-8默认兼容与本仓显式采用 | `config-adoption-evidence.json` | 原配置/DEFAULTS采用保持；legacy修订未改守卫开关或预算 |
| SC-9旧周期与历史保全 | `integrity-before.json`、`integrity-after.json` | 原件保持；旧B19/19与旧报告不回写，原生来源不公开 |
| SC-10实现验收/Rule #6 | `implementation-acceptance.json`、`rule6-evidence.json` | 新parser/schema hunk按成文第1行结构化替代；独立负控及实际结果分开记录 |

旧297项接受记录保持原时点和来源。因新增公共build读取修改，另跑一次当前候选的完整回归：**312/312 judged，0fail/error/skip**，详见`release-validation/candidate-full-suite.json`及同目录原日志；这不是重新写旧验收或把312伪装成原297。

原Rule #6的n=1、固定case1格式FAIL和baseline局限保留，未重写为全绿；人工反馈的当前状态依原root.human_review消费。legacy兼容未改SKILL.md、description或AI调度指令，结构化替代只适用于这些新增代码/schema hunk，不替代原指令面义务。

## 3. 公开与受限两类来源

- 本次按已核对清单选取76份正式报告/验收索引及292个benchmark文件，逐文件原hash匹配；未递归加入整个implementation或历史工作树。
- 原生Workflow/会话JSONL、原始人类问答来源、保全payload与解密材料不加入公开Git。索引中的相关locator/hash只说明来源身份，不声明任意第三方clone后已有访问权限。
- 受限原件仍在当前owner环境和既有保全单元；若接收方需要独立核验这类来源，须另有实际访问/披露安排。不能用“本地存在”或“0形状命中”替代权限，也不因未承诺公开全部原件而自动增加跨环境恢复门。
- 同盘保全不是异机灾备，旧bundle不冒称含后来提交对象；当前公开Git master/tag承载已发布产品对象，二者用途不同。

## 4. 原始数据格式检查实况

全量`git diff --cached --check`对7处原始数据格式给出非零结果：两份CLI原始JSON输出的尾空行、一份旧Markdown报告的双空格硬换行，以及四份viewer原始stdout的尾空行。旧报告与benchmark按原hash保留，不为让检查变绿而改写；新代码、版本文件及新写说明另做源文件范围检查。未关闭Git hook、CI或已配置审计门，也不把全量检查记录成通过。

这项格式探针不是当前配置中的阻断门；项目提交规范和Phase C规范没有将原始stdout/历史证据的空白标准化设为发布前置。若实际配置的hook/CI拒绝，仍须按其真实结果处理，不能用本说明豁免。

## 5. 当前集成状态

插件已发布；主仓PR/gitlink及周期收口以`integration-evidence.json`及后续实际closeout记录为准。该索引在候选准备时允许保留pending，不从文档存在推导主仓合并或归档已经发生。

插件PR #239由本地Git完成合并并附真实commit证据后关闭；Forgejo的merged字段未自动设true，未为补UI标签调用被禁止的子模块服务端merge。
