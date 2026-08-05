---
verdict: PASS
agent: knowledge-manager
round: R3
critical_count: 0
major_count: 0
minor_count: 2
r2_resolved: 2/3
---

# post_spec R3 — knowledge-manager 视角审计 (convergence)

对象: `openspec/changes/secret-guard-per-segment-evaluation/proposal.md` (第三版设计, fail-safe 降级)

## R2 核销结果 (2M+1m)

- **M-1 (`secret-hygiene.md` 计数同步只落 Task 无 SC) → RESOLVED**: 新增 **SC-13**「`secret-hygiene.md` 中 secret-guard 自测计数与实际测试数一致 (机械 grep 比对, R2 knowledge M-1)」(proposal.md:171), 与 Task 1.7 (:151) 配对, 补齐了 R2 指出的「有 Task 无 SC」不对称。实读核实 `standards/conventions/secret-hygiene.md` 现存三处 `366` (L23 Path↔Layer 表 / L286 §5.1 测试清单 / L318 §5.4 实证边界段), 与 R1/R2 一路核实的「三处」一致, SC-13 的机械 grep 比对可覆盖全部三处 (陈旧值改后不再等于活体测试数即失败)。**完全核销**。
- **M-2 (转出项 2/3 复现证据只挂未提交审计报告) → RESOLVED**: 逐条复核转出 1-7 (proposal.md:127-133), 需要布尔判定的 1/2/3/4/5 项**全部**已内联具体可执行命令: 转出 2 `{ cat /opt/.env; echo x; } >/dev/null` / `for f in a b; do cat /opt/.env; done >/dev/null` / `( cat /opt/.env; echo x ) >/dev/null`；转出 3 `ssh h 'cat /opt/.env; true >/dev/null'`。转出 6 (性能/无 pattern 用例)、转出 7 (运维/指向 issue 链接) 按其性质本不需要 block/allow 复现命令, 现状合理。转出章节标题亦已自我标注「复现命令内联; R2 knowledge M-2: 不得只引用未提交的审计报告」, 闭环完整。**完全核销**。
- **m-1 (Aria#172 issue 补「验收基准点选择」提醒) → 未核销, 仍非阻塞**: 核实 `forgejo GET /repos/10CG/Aria/issues/172/comments` 返回 `[]`, 未新增任何 comment。该建议在 R2 中被我本人明确框定为「不构成本 spec 的阻塞项」的 nice-to-have (目标落点是 #172 issue 本身, 非本 spec 文件)。维持原框定: **不影响本轮 CONVERGED 判定**, 作为遗留建议顺延, 建议在 #172 关闭前一并处理。

## 复核通过项

- **模板符合度**: PASS, 结构未变 (Why→What→关键决策→Impact→转出→rule6_note→Tasks→Success Criteria), 新增 SC-13 未破坏章节顺序。
- **Rule #5**: PASS, 落点仍是 `openspec/changes/secret-guard-per-segment-evaluation/`。
- **rule6_note (含 dogfood 限制声明)**: PASS, substitute 集合 (SC-1/SC-5/SC-6/SC-2/SC-3) 与 dogfood 限制段落 (Aria#172 canonical 优先) 均未变动, R2 已实证核实的判定继续成立。
- **数字自洽性核查 (新)**: Impact 段「65/49/16/15/1」与 SC-2/SC-3/SC-7 的对应数字做加总核对: 49+16=65 ✓, 15+1=16 ✓, SC-2 的「15 条纯管道 + 5 条换行边界」与 SC-3 的「49 条」互斥不重叠、与 SC-7 的「1」真边界 (`KNOWN-LIMIT`) 三方无缺口无重叠。未发现算术漏洞。

## 任务 3 — `corpus_census.py` 的规范定位

**(a) 是否恰当的根治手段**: 恰当但不完整。根因诊断准确 (「数法未固化, 非谁算错」, 本 cycle 五个不同结果的直接证据), 用可复算脚本替代人工数数是正确方向, 与 `standards/conventions/secret-hygiene.md` 版本历史表 L401 记载的 1.1.1 (2026-08-02) 「计数同步」修复属**同一根因的第二次发作**——即这不是孤立事故而是复发模式, 支持交付一个权威计数器。但计数器本身只解决「此刻数对」, 不解决「未来漂移」——它是随 spec 交付的一次性工具, Tasks 1.1-1.9 中无任何一项把它接入持续验证机制 (对照本仓已有的 `m6-version-badge-match` / `i18n-readme-translation-currency` 等 `state-checks.yaml` 机械化判据, 那类检查点会在后续每次相关变更时自动复核, 而 `corpus_census.py` 目前只在本 cycle 「跑一次」)。同一文件已经漂移过两次 (1.1.1 + 本 cycle), 若无接入持续检查的动作, 结构上不排除第三次。

**(b) 该放 `tests/` 还是别处**: `tests/` 是正确选择。核实 `aria/hooks/tests/` 目录下 `bash_case` 语料是**内联在 `secret-guard.test.sh` 内部**的 (非独立 fixture 文件), `corpus_census.py` 的职责是静态解析该文件里的 `bash_case` 调用并按 §2 规则表同口径计数——它与该测试文件强耦合、专属服务于它, 属于「审计/派生该测试文件」的工具而非跨测试套件复用的框架原语 (对照 `aria/hooks/tests/lib/crlf-shim.sh`——那是被 3+ 个测试套件共享的可复用框架, 语义不同)。与其耦合对象同目录 (`tests/`, 而非独立 `lib/` 子目录) 是合理放置, 无需改动。

**(c) 是否值得成为 `standards/conventions/` 通用约定**: **不需要, 现在还不到时候**。理由: (1) 目前只有 1 个具体文件 (secret-guard.test.sh 的 bash_case 语料) 复发过 2 次, 尚未观察到跨文件/跨项目的同类模式, 对照本仓「过早泛化」的既有判据 (本 cycle R2 报告自身对 Minor-1「验收基准点选择」的处置逻辑——触发条件是具体缺陷症状而非稳定架构事实, 不写入 standards/conventions/而是留在 issue 里跟踪)——「交付计数器」目前同样是**针对具体反复出错的语料文件的对症工具**, 未证明是可迁移到任意「数字类断言」场景的通用方法论。(2) 本仓已有的通用机制是 `state-checks.yaml` 声明式检查点 (`m6-version-badge-match` 等), 这些是「一次建立规则、长期机械复核」的基础设施; `corpus_census.py` 若要真正长期见效, **更自然的路径是把它接进 `state-checks.yaml` 作为一个新检查点** (复用现成机制), 而不是另写一条 `standards/conventions/` 文档去描述「何时该交付计数器」这种情境判断——后者容易变成难以判据化的软规则, 前者已有可执行先例。建议: 本条不进 `standards/conventions/`, 但作为 Minor-1 (见下) 建议补一项转出/跟进, 把 `corpus_census.py` 接入 `state-checks.yaml`。

## 任务 4 — 「设计演进三版表」与「7 条被推翻断言」自陈

**方法论价值**: 正面, 且是既有先例的合理延伸而非新发明。2026-08-02 归档 spec (`openspec/archive/2026-08-02-secret-guard-nomad-var-put-echo/`) 已示范同类自陈 (「本 cycle 三次未实测即断言」, 3 条, 逐条附「被什么推翻」), 本版复用同一格式、扩到 7 条。实读核实: 7 条中的具体断言 (`&` 可切分 / 「保守不切=不会少拦」方向反 / 「切错=安全回归」/ `has_filter` 尚有 13 处 subprocess / 60ms 实为 jq 58ms / 141→139 的回改 / 「只切 `;``&&`=最小可靠子集」) 均可在 R1/R2 报告与 proposal 正文的对应「被推翻」引用 (tech-lead M-2/M-3、R2 M-3、R2 C-1 等) 找到外部实测佐证, 非自说自话的 pro-forma 罗列。价值有三层: 防止未来 spec 重新提议已被证伪的方案 (v1/v2 及 7 条断言都留了「为什么不行」的可检索记录); 使「审计确实抓到了实质问题」这一方法论主张本身可验证 (对照 memory `feedback_meta_cycle_dogfood_self_consistency` 的自洽验证精神); 诚实文化的正向示范, 与本 spec 「验收环境」段的诚实声明 (R2 已判定非变相豁免) 风格一致。

**风险**: (1) **永久占用归档篇幅**——这些内容会随 spec 一起进 `openspec/archive/`, 若后续同类 spec 继续以 3→7 的斜率增长, 未来读者 (含 AI) 每次追溯本 hook 的历史都要多读若干行「已作废设计」的说明; 目前 7 条仍是紧凑的表格/要点形式, 尚未构成负担, 但值得关注斜率而非绝对值。(2) **可能掩盖一个更值得关注的过程信号**——本版是**第三次完整设计重写** (v1→v2→v3), 而非局部文本修订, 且 3 版设计中前两版都是在 spec 已提交审计后才被审计方用实测推翻 (而非作者自查或 Phase A 阶段的预先原型验证)。「自陈断言被推翻」本身值得表彰, 但「一个 Level 2 spec 走了 3 轮完整架构重设计才收敛」这件事更适合作为独立的 Phase A 充分性问题被观察, 不应被「诚实自陈」的正面叙事覆盖掉。此点不构成本轮阻塞, 仅供 owner 在后续同类 hook spec 的 Phase A 投入判断上参考。

**结论**: 方法论价值 > 风险, 继续采用该自陈格式; 无需改动本 spec 文本。

## 新发现 (Minor, 均非阻塞)

- **Minor-1 (新)**: `corpus_census.py` 目前是「随 spec 交付、跑一次」的工具, 未接入任何持续复核机制 (`state-checks.yaml` 或等价), 而它要解决的漂移问题在 `secret-hygiene.md` 这同一份文件上已复发 2 次 (1.1.1 + 本 cycle)。建议 Task 1.9 (开转出 issue 那一项) 顺带补一条「把 `corpus_census.py` 接入 `state-checks.yaml` 作为新检查点」的转出项, 或在 CHANGELOG/交付说明里显式标注这是有意的范围外决定。不阻塞本轮收敛。
- **Minor-2 (carry-forward, 原 R2 m-1)**: Aria#172 issue 尚未收到「验收基准点选择: canonical 优先于可能陈旧的本地/仓内运行时」的跟进 comment (核实 `forgejo GET .../172/comments` 为空)。维持 R2 原判: 不阻塞, 建议在 #172 关闭前处理。

## 结论

CONVERGED 判定: **是**。r2_resolved 2/3 (M-1、M-2 完全核销; m-1 维持非阻塞的遗留建议, 未变化不代表退化——R2 本就未把它计入阻塞项)。R3 未发现新 Critical/Major。任务 3/4 的规范定位评估均为正面或中性, 无需改动 spec 文本即可 ship; Minor-1/Minor-2 是可顺延处理的跟进项, 不构成 R4 门槛。
