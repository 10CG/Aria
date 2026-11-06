# audit-executor：本地证据保全与集成范围整理

> **日期**：2026-11-06
> **状态**：本地加密快照已逐成员校验；仅完成保全和范围整理，不是 Phase C 提交/发布验收。
> **授权**：用户“先做本地证据保全与集成范围整理，不推送”。不扩张为 stage、commit、版本修改、PR/merge、发布、部署、Phase D 或 PR #38 恢复。

## 1. 本次产物

- [保全回执](./preservation-receipt.json)：绑定捕获与后验解密校验记录、密文 hash、失败尝试和本轮边界。
- [集成范围](./integration-scope.json)：候选路径、逐文件 bytes/SHA256、归属与禁止整目录加入 Git 的范围；不是 stage 清单的执行许可。
- 仓外快照：`/home/dev/aria-local-preservation/audit-executor-20261106-043056/`。
- 密文：上述目录的 `payload.tar.gpg`。
- 完整清单：上述目录的 `inventory.jsonl`；文件含原路径与归档路径、类型、mode、文件 bytes/SHA256。
- 解密材料：`/home/dev/aria-local-preservation/keys/audit-executor-20261106-043056.passphrase`。文件为 0600，所在 keys 目录为 0700；内容不写入本仓、密文包或聊天。不要只保留密文而遗失解密材料。

## 2. 已实际验证的事实

| 项目 | 结果 |
|---|---|
| 被保全普通文件 | 120,735 |
| 源文件逻辑字节 | 3,270,778,079 |
| 被保全目录 | 45,542 |
| 密文字节 | 961,245,960 |
| 解密流逐成员比对 | 166,277 / 166,277，missing=0、failures=0 |
| 普通文件内容/长度、成员类型和权限 | 全部通过 |
| GPG 解密退出码 | 0 |
| 捕获期间源文件内容变化 | 0 |
| 捕获前后四仓 Git 状态、refs、index | 相同 |
| 资源纪律 | 单一保全任务、nice 19、CPU 0-1 |

密文 SHA256：`eeb5a42cd946f7f6f41ab318aea5cc0d6aa9e280fefded719511cf8d92921123`。

`capture-result.json` 是捕获阶段的原始记录，其 `decrypted_payload_verified=false` 当时属实；后验终态在独立 `verification-result.json`，`passed=true`。不回改捕获记录伪造当时已验证。

## 3. 保全范围与限制

采用保守的完整所选工作目录快照，不宣称是最小引用闭包。范围包括：

- 当前未跟踪的本轨/PR38 证据、Spec、handoff、benchmark 目录，以及三份主仓已修改文件。
- aria 的 17 个产品候选文件与当前发布元数据原件。
- implementation 内嵌 Git 数据与工作文件；没有把它们误当主仓可直接提交的 gitlink。
- 索引确认的两个原生 session 目录及存在的主 JSONL；仅作为数据读取、加密，不执行其脚本。
- 索引发现的外部 baseline 原件；选择规则和入口索引记录在 `source-selection.json`。
- 主仓、aria、standards、aria-orchestrator 的 HEAD/master、当前分支及存在的 stash/coordination ref 的 Git bundles；各 bundle 已运行 `git bundle verify`，没有新增源仓 commit 或改写 ref。

这不是“所有可能外部依赖已穷举”的证明，不是公开外发卫生审查，也没有执行解包后的 clone/产品运行。完整快照提供本地原字节保全；将来进入 Git 的最小证据集合及其跨环境恢复仍需按具体目标核对。

**密文与密钥仍在同一容器、同一磁盘。** 分开目录用于避免误把解密材料随证据包传播，不构成异机/离线密钥保管；该副本只防后续工作树误改，不抵抗本机账号失陷、磁盘或容器损毁。原始目录未删除。

## 4. 集成范围

| 分组 | 候选文件数 | 当前处置 |
|---|---:|---|
| aria 产品完整单元 | 17 | 保留代码、测试、配置和指令接线在一个完整单元；未暂存 |
| 主仓 Spec 与配置采用 | 5 | 仅候选路径及 hash |
| 新 Spec 正式审计/验收索引 | 76 | 须结合引用闭包及外发卫生，不按整目录自动 add |
| Rule #6 benchmark | 292 | 属主仓，须与 TASK-017 来源配对 |
| 本轨 handoff | 4 | 与其他轨分开 |
| 未来发布同步面 | 14 | 仅记录当前原件；未改版本，另有未来 post-merge gitlink |

- 主仓已有 `fd986e21`、`cf0b25d2` 两个 #267 triage/handoff 提交。保留原分支和提交，列为未来干净集成的排除项；本轮没有创建/切换分支，也没有改写历史。
- `docs/handoff/latest.md` 混合多轨 History，整份已保全；未来须按 hunk 选择，不默认整文件纳入本轨提交。
- implementation 全目录、嵌套 `.git`、原生记录、旧 PR38 原件、仓外快照/keys 不是可递归 `git add` 的发布范围。

## 5. plugin.json 的历史保护承接

既有 TASK-001/018 清单将 live `aria/.claude-plugin/plugin.json` 标为 `immutable_history`。本轮实核 live hash 与原期望一致，且相同字节已被解密校验的快照保全：

`15bea0d95d6cd68dda9dc1dbe7908bbfc8a64039183c40f40e1ac7287e52db84`。

本轮不修改旧保护清单、受审快照、接受记录或 plugin.json。未来若明确授权版本发布，应保留旧对象/快照与原清单，在新的 integration evidence 中单列获准版本 delta 和发布候选；不能将旧 live-byte 检查改写为新候选 PASS。此处只保全旧字节并建立承接索引，不授权版本变化，也不替代后续验证。

## 6. 失败尝试与后续边界

前两次选择阶段因索引中像路径的长字符串报错；错误类型/位置记录保留。首次完成捕获后的解密校验发现含 `..` 的路径被 tar 改写，30 条不能逐项匹配；该副本未接受，原校验 FAIL 保留。路径规范化后重建的新副本通过上述完整比对。旧尝试未清理或伪装成功，见保全回执。

仍未做：stage、commit、push（含协调 ref）、版本同步、集成分支、CI/pre-merge gate、PR/merge、tag/release、部署、Spec 归档、Phase D、PR #38 恢复。TASK-020/021 原状态未改；Phase B 的既有接受记录没有被新快照改分或重验。
