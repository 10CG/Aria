# Tasks — branch-risk-build-gate-alignment

> Spec: [proposal.md](./proposal.md) | Linked: `10CG/Aria#231` | 执行轨: interactive

- [ ] 1. branch-manager SKILL.md: 风险检测节重排 (裸 api/核心 出表 + 共现规则 + 双源统一表) + 新增「配置 (config-loader)」节 (2 新键)
- [ ] 2. MODE_DECISION_LOGIC.md: 伪码同步 (表 + 共现函数)
- [ ] 3. branch-finisher SKILL.md: 构建验证三态 (表 + 流程 yaml + 输出示例)
- [ ] 4. config-loader SKILL.md schema 2 新键 + 主仓 config.template.json 同步 (config-template-key-currency 兜底)
- [ ] 5. Rule #6 场景 1 AB: branch-manager + branch-finisher 双 skill 定向套件 (#231 原例必含) + rule6_note
- [ ] 6. 发版 v1.77.1: plugin.json/marketplace(×2)/VERSION/CHANGELOG/README (+名册若无新 skill 则不动) + 主仓 gitlink + root README badge + arch §2.8/version-scheme 版本行 (机械兜底三 check)
- [ ] 7. C 阶段: PR + 本地合并 + 双推 + ls-remote 核验 (约束 1/2); D 阶段: 归档 spec + 关 #231 + handoff
