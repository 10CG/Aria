# 派发前拒绝恢复 — 粗粒度任务

> **Status**: In Progress — post_spec真实accept_current、规划R5合法OSCILLATION末轮PASS（均非收敛）；TASK001–017完成，插件v1.79.0本地merge/双远端master与tag及fresh完成审查均PASS；018主仓采用进行中，实际恢复未执行，展示/AB不重开
> **Spec**: [proposal.md](./proposal.md)
> 这里只定义功能粗任务；详细任务及Agent分配见 detailed-tasks.yaml，按实际完成证据反向同步勾选。scope授权不替代审计，不回写原票或将合法非收敛终态改称收敛。

## 1. 容量与证据

- [x] 1.1 在外部派发前校验最终脚本容量，拒绝过大主构建的任何scope/run写入，并防止过大checker脚本发布。普通resume保留仅限六源兼容且尺寸合规的合法状态；保留旧同源超限resume/仅改源码已拒绝的baseline对照，不新增跨源码超限pending迁移或先写锁/record的容量例外。
- [x] 1.2 严格绑定一次真实原生输入拒绝和本机静态 loader→resolver→Tool call 拒绝顺序，保留完整冻结证据；实现独立 operator 来源 adapter，将已有 locator 机械归一化、重读真实 root 问答和 toolUseResult.answers/preview，派生英文 canonical sourceData 与精确 head/reservation/script 绑定。复用已有真实声明，不以索引布尔、API副本、模拟答复或固定容量证书代替；缺失承重字段则具体报阻塞，不伪造或自行重签。

  同时按 design.md §3.2.1 实现**独立** EvidenceAcceptanceIndex → EvidenceAcceptance adapter：重读第二份真实 root 问答及 questions/answers/annotations.preview，复用既有签字并重算完整 TargetBinding；不以旧独占声明替代。仅对旧对象接受历史执行映像身份未独立验证，不从当前窗口/PID/版本推断相同或要求补造历史身份；其他全部容量、静态路径、旧绑定和反证检查不变。

  对任务 2.1–2.3：政策为额外必要条件而非审计 override；将其派生 FileRef、原生 snapshot、locator 与 target 冻结入恢复 evidence 和闭包，历史重放重派生；幂等绑定政策工具对，任何短路前仍查反证，保留首次真实 build 的 §6.1 续接门、source_transition、四未变源和双闭包。

  对任务 3.1、3.3：两份实际已观察 UI 布局分别作合法派生正控；覆盖缺/错政策、错对象/拒绝、非 root/API 副本、只验索引布尔及政策覆盖已知成功/未知运行的坏态，捕获须命中指定业务断言。真实恢复前继续完成所有启用审计、实现测试和发布，不以政策当 PASS、`accept_current` 或即时恢复许可；不要求 owner 重签。

## 2. 有界恢复

- [x] 2.1 支持首个准备物的单一追加拒绝事件与只读预检：一次输入拒绝、真实有界历史授权域声明、当前唯一首reserve/全部旧绑定及已知反证检查共同准入；成功/未知关联运行即使有签字仍否决。不改原件、不生成审计票、不建设全平台网关、无人值守不由AI造声明。
- [x] 2.2 通过精确来源兼容和双闭包承接恢复后的同cycle调用链，保持attempt单调、有效轮/累计预算及普通拒绝语义。
- [x] 2.3 保证幂等、崩溃与并发安全，并在全链重放/collect/check中一致处理恢复事件；同输入可复用签字，首提交前head变化即过期。幂等返回前检查当前载体尾追加及新增已知来源的反证，不返回旧成功。按design.md §6.1将首次续接门落在实际build→_reserve_build：消费必需的recovery-sources、独立live读取与最终字节复核；以固定run-dir handoff、snapshot叶子、新build closure和_record的条件字段冻结证据。_native_build/_HistoryGraph/_resume_build共享冻结验证，不将新root bytes覆盖旧闭包，不把合法attempt2当旧反证；不新增撤销事件或全平台网关。

## 3. 验证与交付

- [x] 3.1 完成测试先行、非作者坏态、必要回归/类型检查及逐hunk Rule6处置，保留真实红绿证据。覆盖合法真实问答布局对照、静态拒绝顺序、非root/API副本、错对象/过期、签字覆盖反证、幂等早返回及双root关联运行。新增从合法seq2直接普通build的反证负控，禁止先再次recover；对原root尾追加/已知第二root、capture后reserve前变动、漏live capture/只读旧snapshot坏实现及handoff缺失错绑逐项验证。合法对照须走到attempt2，反例须命中counterevidence或最终复核的指定业务断言而非缺参数/未知事件/容量旁路；合法attempt2 pending resume零重派、离线check不依赖live原件。SKIP/not_judged不计通过，SC-1..10编号保留，fixture成功不代替启用规范/规划审计。
- [ ] 3.2 按规范完成版本同步、CI/指针门、跨仓本地合并与多远端逐SHA核验。
- [ ] 3.3 对真实冻结准备物先执行只读预检，严格adapter复用既有真实声明，发布与主仓采用完成后才实际恢复、完成原规划审计；来源不齐如实保持pending。仅交付推荐机制PhaseA、实现任务仍pending、PR #38继续暂停，不改v2正常业务人类节点；准备本修复周期收尾所需的功能交付与验证证据。本项完成不声称归档、最终handoff或claim释放已发生。

## Phase D 后置交付义务（不作为归档前任务完成条件）

全部功能任务真实完成后，仍必须按配置执行 Phase D：D.1进度核对、D.2正常归档及落点验证、D.2b真实claim释放尝试、D.3 docs/handoff五字段与latest增量、D.4实际区间estimator，以及启用的post_closure。每一步发生后才记录其真实回执；完整目标在这些后置义务也完成后才结束。不得为解除循环提前勾选、改Status冒充完成、design-only归档或跳过归档门。
