# GRADER_CRITIQUE — eval-13 a1-heartbeat-on-entry-TARGETED

评分结果: `with_skill` 6/6, `old_skill` 2/6。

---

## 1. 有没有恒真 / 恒假的断言?

**断言 6 (负向, 遥测分区) 在本 eval 里接近恒真, 零区分力。**

它只在某一臂**主动提到**心跳遥测的分区归属并且说错时才会 fail。不掌握该机制的臂根本没有理由谈论遥测分区 —— `old_skill` 全文一次都没提, 于是「空缺式通过」。也就是说这条断言唯一可能 fail 的臂, 恰恰是掌握机制的那一臂 (它会主动写分区), 而它写对了就 pass。**结构上它奖励沉默、只惩罚开口**, 与预期的方向相反。

建议改成正向承重断言: 「明确说心跳遥测走独立 `heartbeat` 分区、不进 production、且不计入 `coordination_probe`」—— 这样它就变成了一条真正的知识点探针 (以本次两臂的实际输出看, 改成正向后区分度是 1/0)。

**断言 5 (负向, 不答成认领/完整闸门) 是本轮唯一的判定边界案例, 需要点名。**

`old_skill` 明确写了「入口不该跑 `phase1_gate`」, 从字面看它没主张「入口先跑认领」。但用户 (A) 问的就是「写出它该跑的完整命令行」, 而 `old_skill` 唯一给出的 phase1_gate 命令行是完整闸门 acquire 模式, 并逐字标注「(这就是你要的完整命令行)」。按 GRADER_INSTRUCTIONS「回答中主张了被禁项即判 false」, 我判 `false`。若把这条断言按「是否声称入口应当立刻执行完整闸门」的窄读法, `old_skill` 会翻成 `true` —— **断言措辞没有把「入口该做什么」与「(A) 要的那条命令行长什么样」这两个提问面区分开**, 建议改写为: 「(A) 给出的 phase1_gate 命令行不得是 acquire/完整闸门形态 (不含 `--phase B` / `--mode`)」, 这是可机检的、无歧义的。

其余四条 (1/2/3/4) 都有真实区分力, 本轮实测区分度 1/0 或有实际差异。

**断言 3 有半恒真风险 (本轮 pass/pass, 零区分力)。**
两臂都答对 (B), 但答对的**理由完全相反**: `with_skill` 是「本该跑的心跳因 opt-out 而不跑, 且不得因 claim 重要就破例」; `old_skill` 是「入口本来就从不跑心跳, 所以 enabled 取什么值都一样」。后者的 (B) 命题在其自身世界观下是**平凡真**(前件与后件无因果关系), 却拿到与前者相同的分。若要让断言 3 有区分力, 需加一句「且说明 enabled==false 是 opt-out 的既定代价 / 不得绕过配置替 claim 续期」。

---

## 2. 断言完全没覆盖的重要差异

1. **stale 时间轴用了不同常量, 且 `old_skill` 有一处事实错误 (完全不在断言射程内)。**
   `old_skill` 写「`STALE_TTL = 1800s`（30 min）…… 下一次 `--sweep-stale` 会把它判成 `abandoned`」。查 `lib/constants.py`: `STALE_TTL = 1800`, 但 `--sweep-stale` 判据是 `SWEEP_TTL = 86400` (24h)。6h claim 只是 stale (影响 reconcile 接管资格), **不会**被 sweep 成 abandoned。`with_skill` 用的是 `SWEEP_TTL` 24h、「现在离扫描线还剩约 18h」, 与代码一致。一条 6/6 的臂与一条含实质事实错误的臂, 在当前断言集下这个差异**完全不计分**。

2. **`--raw-track-id` 的取值来源之争, 无断言覆盖。**
   `old_skill` 判定用户给的 `a1-entry-claim-duplicate-work-guard-023236f2` 是「已归一后的 track_id, 不是 carry-id 原始串」, 因而拒绝把它填进命令行 (改写成 `<handoff §6 选定 carry-id 的原始串>` 占位符)。`with_skill` 走三级回落, 第一级就是「本 session 已持有的 claim 的 track_id」, 直接原样填。断言 1 只要求命令行含三个 token, 对**参数值填得对不对**完全无感 —— 而这恰是实操中最容易写错的一项。建议补一条: 「命令行把 `--raw-track-id` 填成用户给的 `a1-entry-claim-duplicate-work-guard-023236f2` 实值, 而非占位符」。

3. **两臂对「缺口」的姿态截然不同, 无断言覆盖。**
   `old_skill` 把结论收在「这看起来是当前设计的一个真实缺口, 值得开单 / 请你复议」, 并拒绝「替它编一个不存在的机制」—— 在旧世界观下这是**正确且克制**的行为。断言集只测「有没有答对新机制」, 完全不体现基线臂在无知识时的诚实降级质量。这不必然要修, 但读结果的人应知道: `old_skill` 的 4 个 fail 全部是「知识缺失」, 没有一个是「胡编」。

4. **三级回落 / fail-CLOSED 新鲜度谓词 / degraded 不重跑 fetch (13.8s 代价), 只有 `with_skill` 讲, 无断言覆盖。**
   这三项都是 `references/layer-l-integration.md` 里的实质设计点, 是本次变更的知识面主体之一, 却整个落在断言集之外。

---

## 3. 有没有哪一臂引用了 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**没有。两臂的可追溯引用全部指向技能文件本身, 未见仓内 in-flight Spec 语料污染。**

- `with_skill` 的引用锚点逐字为「与 SKILL.md「Layer L A.1 heartbeat 集成」小节逐字节一致」。核对 `aria/skills/state-scanner/SKILL.md:180` 确有 `### Layer L A.1 heartbeat 集成` 段, `:188` 逐字含 `--heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path "<repo root>"`, `:183` 含 `SWEEP_TTL` (24h), `:191` 逐字含「独立 `heartbeat` 分区, 不进 production」与 `skipped_no_track`。其余细节 (`coordination_probe` 计数口径 / fail-CLOSED 谓词 `coordination_fetch.success == true` **且** `coordination_ref_present == true` / degraded 不重跑 fetch 的 **13.8s** 代价) 逐条命中 `aria/skills/state-scanner/references/layer-l-integration.md:74 / :80 / :88`。**该臂全部实质内容都能在技能文件内闭合, 无需借助 openspec 文档解释。**
- `old_skill` 自述依据为「state-scanner SKILL.md v3.1.1 的成文契约」, 并引「layer-l-integration.md:15 Design A」「R1-m6」「rule 1.54 `concurrent_churn_detected`」「#133 AC-2」「DEC-20260519-001」。逐条核对 baseline snapshot: `skill-snapshot/skills/state-scanner/SKILL.md:149` 逐字含「(layer-l-integration.md:15 Design A: 闸门仅在用户确认进 Phase B 时调用, 不在只读 collector 内自动跑)」, `:162` 含「(R1-m6)」, `:174` 含「零调用 `run_gate`, collision 由 rule 1.54 advisory surface」, `RECOMMENDATION_RULES.md:31` 含 `concurrent_churn_detected` 与 `(#133)`。**这些看似「仓内知识」的编号全部来自技能文件自身语料, 不构成污染证据。**
- 反向证据: baseline snapshot 里 `grep -n "heartbeat-only\|A.1 heartbeat\|SWEEP_TTL\|13.8\|coordination_probe\|skipped_no_track"` 对 `state-scanner/SKILL.md` **零命中**, 与 `old_skill` 全文不含这些 token 完全一致 —— 基线臂的知识面与其技能快照严格同构, 没有从别处漏进新世界的迹象。
