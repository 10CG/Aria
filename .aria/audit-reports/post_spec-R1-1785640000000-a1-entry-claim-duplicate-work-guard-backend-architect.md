# post_spec R1 — backend-architect
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=3 minor=1

> 审计对象: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` (全文已读, 176 行)。
> 全部结论基于实读代码 (`aria/skills/state-scanner/scripts/phase1_gate.py`, `lib/collision.py`, `lib/track_id.py`, `lib/claim_schema.py`, `lib/constants.py`, `scripts/release_gate.py`, `scripts/collectors/handoff_multibranch.py`) + 两次真实 dogfood 执行 (`phase1_gate.py --phase A.1` 与 `release_gate.py` 清理) + 一次生产环境 `refs/aria/coordination` 跨 remote 现场取证。未修改任何文件, 未 commit。

---

## Findings

### [CRITICAL] fetch 降级状态不进 JSON `error` 契约, SC-1/SC-2 赖以成立的"新鲜度"信任前提不成立 (已实测复现, 非推断)
- **位置**: `aria/skills/state-scanner/scripts/phase1_gate.py:471-481`(降级分支) 与 `:818-827`(尤其 `:825 error=None`); 契约声明见 `:189-217`(`GateResult` docstring `:210` 明文把 `"fetch_degraded"` 列为 `error` 字段的合法取值)。
- **问题**: Step 4 `health_check_fetch` 失败时, 代码在 `:472-481` 打印警告并注释 "we continue with whatever is locally available and warn the caller **via the error field**"——但沿这条路径往下走到 Step 9 push 成功后的返回语句 (`:818-827`), `error=None` 是**硬编码常量** (`:825`), 与 Step 4 是否降级完全无关联变量。也就是说: 只要 push 最终成功, 无论 Step 4 的 fetch 是否失败, JSON 输出的 `error` 永远是 `null`。这与 docstring 自身写的契约矛盾, 是代码内部不自洽 (注释/docstring 承诺的行为与实现不符), 不是我的推测。
  该结论直接连带 `linked_issue_overlap` 的可信度: CLI 在 `:1229-1237` 对 overlap 的第二次 `read_claims(repo)` 调用**不会重新 fetch**——用的还是 Step 4 那次（可能已降级）之后的本地 ref 快照。也就是说 fetch 失败时, `linked_issue_overlap` 和 `error` 会**同时**呈现"一切正常"的假象。
- **证据 (实跑)**: 在主仓按 Spec §1 给出的调用形态实测 (`--raw-track-id` 用明显测试串, 完成后已用 `release_gate.py --status abandoned` 清理):
  ```
  $ python3 aria/skills/state-scanner/scripts/phase1_gate.py \
      --raw-track-id "postspec-r1-DELETE-ME-a1-entry-claim-audit-test" \
      --phase "A.1" --mode advisory \
      --linked-issue "AUDIT-TEST-DO-NOT-USE#0" --repo-path /home/dev/Aria

  coordination_ref.fetch_coordination_ref: fetch failed (rc=128, kind=fetch_failed, remote=origin)
  failure_handlers.health_check_fetch: fetch failed (kind=fetch_failed) — marking partial_fetch
  phase1_gate.run_gate: fetch degraded (kind=fetch_failed) — proceeding with stale local ref (elevated collision risk)
  {
    "outcome": "passed",
    "proceed": true,
    ...
    "error": null,          ← docstring 承诺这里该是 "fetch_degraded"
    "push_success": true,
    "linked_issue_overlap": []
  }
  EXIT_CODE=0
  ```
  这是我**独立于 Spec 作者、第一次真实调用就复现**的降级路径 (D6/D7 引用的那次 dogfood 运气好走的是干净 fetch 路径, 没有触发这个分支)。复测两次手工 `git fetch origin refs/aria/coordination:refs/aria/coordination` 均成功 (`up to date`), 说明这不是永久性网络故障, 而是间歇性——恰恰更危险: 它不可预测, 且**无法从 JSON 输出分辨**"确认无重叠"和"用旧快照判的无重叠"。
- **建议修法**: 本 Spec 明确"不改 phase1_gate 自身代码" (非目标), 因此建议在 proposal §1 的"消费"条款里显式加一条: phase-a-planner 调用 phase1_gate **前**自行 `git fetch origin refs/aria/coordination:refs/aria/coordination` 一次并检查退出码 (该 fetch 的 exit code 对调用方是可见的, 不依赖 phase1_gate 内部字段), fetch 失败时把 `linked_issue_overlap` 当**不可信**处理 (fail-closed: 视同"无法确认, 需人工复核", 而非视同"[]=安全")。同时应对 `phase1_gate.py` 的 `error=None` 硬编码开一条独立缺口 issue (不在本 Spec 范围内修, 但本 Spec 的安全论证不能假装它不存在)。

### [CRITICAL] 主/副两机制对"sibling 已完工并归档"这一 Spec 自己的头号事故场景结构性失明, §3 残余缺口未坦白此情形
- **位置**: 副机制描述见 proposal.md `:101-105`("对本 spec 的关联 Issue grep 全部远端 ref 上的 `openspec/changes/*/proposal.md`"); 真实归档路径见 `aria/skills/openspec-archive/SKILL.md:60-71`("✅ 正确的目录结构": `openspec/archive/YYYY-MM-DD-{feature}/`, 与 `openspec/changes/` 同级而非子目录) 及本仓 `openspec/archive/` 目录的真实存在 (已用 `find` 核实, 另在 `/home/dev/Aether`、`/home/dev/Kairos`、`/home/dev/SilkNode` 等仓一致复现同一顶层布局)。主机制的排除条件见 `aria/skills/state-scanner/lib/collision.py:210`(`_TERMINAL = ("done", "abandoned", "unknown")`)与 `:213`(`if c.status in _TERMINAL: continue`)。
- **问题**: 一份 Spec 一旦走完十步循环并被 `openspec-archive` 归档, 它的 `proposal.md` 会被**移出** `openspec/changes/` 挪到**同级**的 `openspec/archive/YYYY-MM-DD-{name}/` 下——不是 `openspec/changes/archive/`(那是 SKILL.md 自己文档化的已知 CLI bug, 会被自动修正掉)。副机制给出的 glob `openspec/changes/*/proposal.md` 结构上**永远够不到** `openspec/archive/` 下的任何文件。同时, 主机制的 `linked_issue_overlaps` 按设计排除 `done`/`abandoned` 状态 (这本身对"避免与仍在进行的工作打架"是正确设计, 不是 bug), 但结果是: **一旦某条 track 走完全部十步循环 (claim 状态变 done) 并归档, 这两个机制对它都同时失明。**
  这正是 proposal 自己在 §Why 里举的最重的例子: "并发轨已于 07-31 把同一个 #122 走完十步循环 ship 为 v1.65.0 **并归档**"(`:17`)。按字面实现这两个机制, 换作是现在, 面对同一个事故复现, 依然**抓不到**——因为 v1.65.0 那份 proposal.md 此刻理应已经在 `openspec/archive/` 下, 副机制的 glob 看不见; 而如果对方的 claim 也已经 release 成 `done`, 主机制的 overlap 检查也看不见。§3"残余缺口"只坦白了"对方既未 claim 又未 push"一种情形 (`:107-113`), 完全没提这个更常见、代价更高 (完整重复劳动 vs. 半路撞见) 的情形。
- **证据**:
  ```
  $ find openspec/changes/archive -maxdepth 2 -iname "proposal.md"
  bfs: error: openspec/changes/archive: No such file or directory.   # 该路径从不存在(已被 skill 自动修正)

  $ find / -maxdepth 6 -type d -iname "archive" -path "*openspec*" 2>/dev/null
  /home/dev/Aether/openspec/archive
  /home/dev/SilkNode/openspec/archive
  ...
  /home/dev/Aria/openspec/archive        # 与 changes/ 同级, 不在 changes/ 下
  ```
  `aria/skills/openspec-archive/SKILL.md:52-53`: "❌ CLI 输出: `openspec/changes/archive/...`" / "✅ 正确位置: `openspec/archive/...`" ——两条路径都不满足 `openspec/changes/*/proposal.md`(前者深两层, 后者压根不在 `changes/` 下)。
- **建议修法**: §2 的 glob 描述必须同时覆盖 `openspec/archive/*/proposal.md`(注意目录深度是 `archive/{date}-{name}/proposal.md`, 比 `changes/{name}/proposal.md` 多一层日期前缀, 通配符要按实际深度写, 不能直接复用同一个 pattern); 并在 SC-4 里补一个"命中已归档 sibling"的显式场景。同时 §3 残余缺口应如实新增一条: "对方已完工并 release claim (status=done) 时, 主机制不再示警——这是设计使然 (done 不算碰撞), 但意味着两机制组合仍不能回答『这件事是不是已经有人做完了』, 只能回答『现在是否有人正在做』"。这个措辞上的诚实退让, 和 D4 的既有原则 (盲区必须写进正文) 完全一致, 不是新增负担。

### [MAJOR] track_id 由裸字符串规范化产生、无重命名迁移/别名机制; A.1 阶段改 spec-slug 会产生孤儿 active claim
- **位置**: `aria/skills/state-scanner/lib/track_id.py:61`(`def derive_track_id`) 及其算法体 `:155-168`(纯函数: lower → 替换 `/._` → 截断/哈希, 无任何跨调用状态、无历史映射表); 精确匹配点 `aria/skills/state-scanner/scripts/phase1_gate.py:488`(`track_claims = [c for c in all_claims if c.track_id == track_id]`, 字符串全等); TTL 常量 `aria/skills/state-scanner/lib/constants.py:36`(`STALE_TTL = 1800`)、`:51`(`SWEEP_TTL = 86400`), 及 `:40-46` 明文写"现实中没有生产级 heartbeat loop"。sweep 触发点 `aria/skills/phase-d-closer/SKILL.md:48-59`(D.2b, 仅在**某个** session 完整走到 Phase D 收尾时才会捎带执行 `--sweep-stale --gc`, 不是独立调度/不是定时任务)。
- **问题**: `derive_track_id` 是对**原始输入字符串**的确定性变换, 不认识"这其实是同一份工作、只是改了名字"。proposal.md 自己在 §1 (`:88`) 把 A.1 阶段的 `--raw-track-id` 定为"`<spec-slug 或 handoff §6 carry-id>`"——而 spec-slug 在起草阶段被改名 (换标题/换目录名) 是常见操作 (甚至本 Spec 自己 07-30→07-31 的修订过程就跨了至少一次 A.3 修订)。一旦改名, 新调用产生的 `track_id` 与旧的不再相等, 旧的那条 claim:
  1. 不会被"self-resume"识别为同一份工作 (`_self_resume` 靠 reconcile 结果里 winner 是否匹配本机身份, 而 reconcile 的输入 `track_claims` 已经是按**新** `track_id` 过滤过的——旧记录根本不在候选集里, `phase1_gate.py:511-526`);
  2. 依然以 `status=active` 挂在 `refs/aria/coordination` 上, 直到 (a) 有人手工用**旧**的 raw-track-id 跑 `release_gate.py`(Spec 全文没提这一步), 或 (b) 该记录 heartbeat age 超过 `SWEEP_TTL`(24h) **且**日后某个 session 真的跑到 D.2b 触发 `--sweep-stale`——这是"至少 24h, 经常更久"而非自动即时。
  期间, 若第三方 session 用**同一个** `--linked-issue` 调用 `phase1_gate --phase A.1`, `linked_issue_overlaps` 会把这条"改名前的自己"当成一条独立的、仍然 active 的竞品 claim 报出来——一次因为改名产生的假警报; 反过来, 若本 session 自己后续又用新名字重新调用, 也不会主动发现并清理旧名字下的残留, 旧记录成为噪音持续污染后续所有对同一 `linked_issue` 的 overlap 查询。
- **建议修法**: proposal §1 的调用形态里加一条: 若本 session 在同一 cycle 内**曾经**用不同的 raw-track-id 调过 phase1_gate (即发生过改名), 在改名后**必须**先对旧 raw-track-id 跑一次 `release_gate.py --status abandoned` 再用新名字重新认领, 使残留窗口从"最长 24h+"收窄到"秒级"(与主机制标榜的"不像 spec 文件躺两天"这个卖点保持一致)。

### [MAJOR] `sibling_spec_probe.py`"全部远端 ref"的规模/代价未定义; 同代码库已有先例踩过同一个坑却未被引用
- **位置**: proposal.md `:101-105`(副机制描述, 只说"每轮"+"全部远端 ref", 未定义范围/上限/超时); 对照先例 `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:53-55`("If the remote branch count exceeds the resolved scan cap (default 20, ... ) only the first N branches ... are processed")、`:108-112`("v1.38.0 (#71): the cap is now 3-layer configurable (env > config > default 20) ... 440 remote branches")、`:304-338`(实际 cap 解析与截断逻辑)。已核实此文件确属同一 `state-scanner` skill 家族, 与 `phase1_gate.py` 同目录树下的 `scripts/collectors/`。
- **问题**: "全部远端 ref"在 git 语义上不是免费操作: 要看到某个远端分支上的 `openspec/changes/*/proposal.md`, 至少要 (a) 枚举该 remote 下所有分支引用 (`git for-each-ref refs/remotes/<remote>/`) (b) 对每条候选分支跑 `git ls-tree`/`git show` 取内容。这正是 `handoff_multibranch.py` 已经解决过的问题——它的模块 docstring 直接写明现实中见过"440 条远端分支"的仓库, 因此做了三层可配置 scan cap (默认 20) 并在超限时输出 `soft_error`, 不静默截断。`audit-engine` 的 Step 0.5 按 D3 是**每轮**跑 (不是仅首轮), 而本 Spec 给出的历史事故本身就有 10 轮审计的先例——若 `sibling_spec_probe.py` 每轮都对"全部远端 ref"做无上限枚举+逐条 ls-tree, 在长期活跃、分支多的仓库上, 审计延迟/网络负载会随分支数线性增长且没有任何上限声明。Spec 完全没有提及是否要复用 `handoff_multibranch.py` 已有的 `_list_origin_branches`/`resolve_max_branches_scanned` helper, 也没有给出等价的 cap/超时/降级策略——实现者要么重新发明一遍同样的安全阀 (多花功夫且可能漏掉 440-分支这类现实教训), 要么干脆不做, 留下一个规模不设防的每轮开销。
- **建议修法**: §2 增补: `sibling_spec_probe.py` 复用 (或至少显式参照) `handoff_multibranch.py` 的分支枚举与 scan cap 模式 (`_list_origin_branches` + `resolve_max_branches_scanned`), 并在 SC-6 的"degraded"场景里把"超过 scan cap 截断"也算作一种需要显式声明的降级 (而不仅是"fetch 失败/无远端"), 保持与既有 `soft_error` 惯例一致。

### [MAJOR] 生产环境 `refs/aria/coordination` 已实测在 origin/github 两个 remote 间分叉; D7"已实测非推断"的举证范围小于其结论
- **位置**: 结论所需的 remote 范围前提未见于 proposal.md 任何一处 (D7 位于 `:127`); fetch/push 均只认一个 `--remote`(默认 `origin`), 见 `phase1_gate.py:1207`(`--remote`, default "origin") 与 `aria/skills/state-scanner/lib/coordination_ref.py:1367-1369`(`fetch_coordination_ref` 固定 refspec `refs/aria/coordination:refs/aria/coordination`, 单 remote)。
- **问题**: CLAUDE.md 明文把"多远程一致"列为不可协商的硬约束 (本仓是 Forgejo `origin` + GitHub `github` 双远程项目), 并记录过因缺少机械兜底导致镜像静默分叉的先例 (`feedback_mirror_sync_needs_mechanical_backstop`)。`phase1_gate.py`/`release_gate.py` 对协调 ref 的 fetch/push 从未做双 remote 处理, 只认默认的 `origin`。我现场验证了这不是假设性风险, 而是**已经发生的现实**:
- **证据 (实跑, 只读, 未做任何写入/修改)**:
  ```
  $ git ls-remote origin refs/aria/coordination
  474cb123879c1189394b124b1dc5f75eca1ffae2   refs/aria/coordination
  $ git ls-remote github refs/aria/coordination
  ad0287f759c23f9ee85d02fe0b47842eb5f71103   refs/aria/coordination

  $ git fetch origin refs/aria/coordination:refs/tmp-audit-origin-coord
  $ git fetch github refs/aria/coordination:refs/tmp-audit-github-coord
  $ git merge-base --is-ancestor refs/tmp-audit-github-coord refs/tmp-audit-origin-coord \
      && echo "github IS ancestor of origin (origin ahead)"
  github IS ancestor of origin (origin ahead)

  $ git log --oneline -3 refs/tmp-audit-github-coord
  ad0287f claim: bfe8285d/s-468d@1659 status=done phase=D.2
  62e181b claim: bfe8285d/s-468d@1659 status=active phase=B.1
  ad45cd0 Aria coordination ref bootstrap (2026-05-24)     ← github 侧停在 2026-05-24 引导提交后仅一条 claim
  $ git log --oneline -5 refs/tmp-audit-origin-coord
  474cb12 claim: 023236f2/s-b291@1154 status=active phase=A.1
  babe90c claim: bfe8285d/s-9aa1@1542 status=done phase=B
  ...                                                        ← origin 侧已推进数十条 claim, 一直到今天
  ```
  (以上两个临时本地 ref 仅用于本次只读比对, 已在取证后立即 `git update-ref -d` 删除, 未产生任何推送/提交。)
  这证明: `github` 侧的协调 ref 已经**停滞两个多月**, 完全没收到 origin 侧那几十次 claim 写入。proposal D7 写"主机制的承重前提『claim 立即推远端』已实测, 非推断"——但那次 dogfood (`aria-plugin#124`) 和我这次复测一样, 验证的都只是"对默认 remote 的一次 push 退出码"; 它从未、也不可能验证"任何可能 fetch 该 ref 的位置都看得到"。只要存在一个只从 `github` 侧拉取的场景 (例如某容器的 `origin` 被配置指向 GitHub、或未来接入的外部协作者), 这个场景下"claim 立即可见"的核心卖点就是假的, 而这不是理论推演, 是我五分钟前刚从生产 ref 里读出来的数据。
- **建议修法**: 不要求本 Spec 修复这个既有分叉 (超出"不改 phase1_gate 代码"的既定范围), 但 D7 的措辞需要收窄为"已实测**单 remote (origin)** 场景下 push 成功"; 并在 §3 残余缺口里补一条"多 remote 环境下, 认领对**其他** remote 不可见"——这本质上和"两个机制都不覆盖对方既未 claim 又未 push 的窗口"是同一类盲区的另一种成因, 理应并列声明。

### [MINOR] SC-7"排除自身 track-id"的表述与副机制实际 I/O 不一致, 实现者不清楚拿什么值判"是不是自己"
- **位置**: proposal.md `:143`(SC-7: "不得自命中 (排除自身 track-id / 自身目录)"); 对照 §2 对 `sibling_spec_probe.py` 的输入描述 (`:101-105`) 与 Impact 表 (`:158-165`)——全篇没有任何地方说 `sibling_spec_probe.py` 会接收 `track_id` 作为参数或读取 claim 数据; 它的输入始终描述为"本 spec 的关联 Issue"+ 远端 proposal.md 内容。
- **问题**: "track-id"是主机制 (claim/`derive_track_id`) 的词汇; 副机制按 Spec 描述是纯粹在远端 refs 上 grep `openspec/changes/*/proposal.md` 找同 Issue 引用, 天然的自然排除键应该是"自身当前 spec 的目录名"或"自身当前分支名", 而不是 track_id (副机制的实现里根本不存在这个变量, 除非额外新增一个参数)。SC-7 把两套机制的术语混用, 会让实现者不清楚: 究竟要不要给 `sibling_spec_probe.py` 增加一个 `--own-track-id` 或 `--own-dir` 参数, 用哪个值来源做排除比较。这是可证伪的: 照 Impact 表列出的文件清单去实现, 排除逻辑没有输入可用。
- **建议修法**: 把 SC-7 的表述改成对副机制而言可执行的具体判据, 例如"排除: 远端 ref 上路径等于`<own spec 目录名>`的条目, 以及(如可判定)与本地当前分支同名的远端分支上的条目", 并在 Impact 表里显式给 `sibling_spec_probe.py` 补一个"自身目录名/当前分支名"输入参数, 使其与主机制的 track_id 排除逻辑(`collision.py:219`)在语义上各自独立、各自完整, 不共享一个实际不存在的字段。

---

## 附: 已验证为非问题的两点 (backend-architect 关注但排查后放行)

- **`--phase A.1` 不需要改 `phase1_gate.py` 代码 (D6)**: 已核实 `phase1_gate.py:1189-1191` 的 `--phase` 确无 `choices=` 约束 (对照 `:1192-1197` 的 `--mode` 确有 `choices=["advisory","block"]`), 且已用明显测试用的 `--raw-track-id "postspec-r1-DELETE-ME-a1-entry-claim-audit-test"` 独立实跑 `--phase "A.1"` 成功 (`outcome=passed`, `push_success=true`), 跑完已用 `release_gate.py --status abandoned` 释放清理, 不留污染。D6 本体成立——但过程中意外复现了上面第一条 CRITICAL。
- **audit-engine 目前零 `scripts/` 目录, 新建是否影响测试发现/打包**: 已读 `aria/skills/run_all_tests.sh:36-38`, 其对测试目录的发现是 `find "$SKILLS_DIR" -type d -name tests`(通用扫描, 不依赖预先登记的 skill 清单), 新增 `skills/audit-engine/tests/` 会被自动纳入, 无需额外接线。另确认 `aria/.claude-plugin/plugin.json` 不含 `files`/`include` 一类的显式清单字段, 仓内也没有其它 manifest/pack 脚本按目录白名单打包。新建 `scripts/`(+`tests/`) 目录本身不会破坏任何现有扫描或打包路径。
