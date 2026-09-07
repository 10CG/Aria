# DEC-20260907-001 — `handoff_multibranch` 的 `filename` 语义取舍 + pointer 写侧守卫

> **Spec**: `openspec/changes/handoff-multibranch-subdir-path-fidelity/` (Aria #195, Level 2)
> **裁定人**: AI (aria-runner-bot/bfe8285d), **owner 不在场** —— 按 CLAUDE.md 规则 #10「AI 任何自作主张的流程判断必须写进 handoff 请复议」, 本单是**待复议**记录, 不是既成授权
> **时间**: 2026-09-07 (UTC)
> **来源**: post_spec R1 critical `63d1ce08` (4/5 席) + decision `109b412c`; R1 rework 已把取舍升级为 §待 owner 复议 2 并设为 Phase B 前置门
> **触发背景**: 用户以 `/goal` 设定「一口气完成当前推荐的所有工作流」的无人值守目标, 期间 owner 未在场; 前置门若不裁决则 Phase B 无法开工。故按「陈述假设并推进」处理, 全部理由与反证据留在本单供事后复议

---

## 裁定

**采纳 A′ + 写侧守卫** (原三选项的 (i) 与 (iii) 的组合, 但对 (i) 的前提做了一处订正):

1. **`tracks[].filename` 保持 basename 语义不变**。
2. **新增 additive 字段 `relpath`** = `git ls-tree` 输出相对 `docs/handoff/` 的路径 (平铺仓 ⇒ 与 `filename` 逐字节相同)。
3. **四个 git 路径消费方一律改读 `relpath`**: `_read_file_content` · `_get_file_commit_date` · `_make_legacy_track_id` · `scan.py:186` (`_same_branch_head_unreachable_tracks`)。
4. **`latest_md_writer._render_pointer` 加写侧守卫**: 仅当 `relpath == filename` (即该 track 的文件在 `docs/handoff/` 顶层) 才写真指针; 否则走**既有**的 `_render_pointer_unavailable` 分支并写明原因 (目标在子目录, 姊妹 collector 目前不能解析)。
5. **遗留缺口另开 issue**: 让 `handoff.py::_parse_latest_pointer` / `_scan_md_files` 支持子目录 (= 原选项 (ii) 的工作), 由该 issue 独立立项, 不并入本 Level 2。

---

## 为什么不是原样的 (i)

R1 rework 在 §5 消费方表里写「**注意 A′ 案不会新增这条失败面**, 但也修不好它」。**这句不成立**, 实读证据:

- `writers/latest_md_writer.py::_get_active_tracks` (`:89-95`) 只把 `status == "active"` 的行放进候选, docstring `:78-81` 明写 legacy 行被**有意排除**。
- 今天子目录文件走的是 `git show` 失败分支 ⇒ `status: "legacy"` ⇒ **永远不会**被选为 pointer。
- A′ 修好路径后, 该文件的 frontmatter 被正常解析 ⇒ `status: "active"` ⇒ **进入候选集**。
- 此时 `_render_pointer` (`:143`) 写 `[{filename}](./{filename})` = `[x.md](./x.md)`, 而真实文件在 `archive/x.md`。
- `handoff.py::_parse_latest_pointer` (`:288`) 取 `Path(target).name` = `x.md`, 到 `_scan_md_files` (`:300,318` **非递归** `iterdir()`) 的候选索引 (`:389` 按 `p.name` 建) 里查 —— **查不到** ⇒ `handoff_pointer_target_missing` (`:399`) + `latest_source` 由 pointer 退回 mtime。

也就是说 A 案与 A′ 案**都会**新增 pointer 往返断裂, 只是断点不同 (A 断在「写了带目录的路径」, A′ 断在「写了顶层不存在的 basename」)。**写侧守卫在两案下都是必需项, 不是折中选项。** 这是本单对 R1 结论的一处订正。

## 为什么不是 (ii) (同 cycle 修姊妹 collector)

(ii) 是最彻底的修法, 但它把本 spec 的触点面从「一个 collector + 一处跨文件消费方」扩到「两个 collector + pointer 语义权威 (H5) + 其既有测试面」。理由:

- H5「pointer 是语义权威」是一条已 ship 的既有修复, 改它的解析与扫描逻辑需要自己的 SC 与反事实, 不能顺手带过。
- 本 spec 已经在 R1 长出 2 critical / 15 major, 再扩面会让收敛更远。
- 记忆里的教训 (`feedback_sub_pr_scope_splitting_pattern`): 大 Spec 三段式拆分, 强依赖项留主 loop, 低耦合项另立。姊妹 collector 的子目录支持与本 spec 无强依赖 —— 守卫落地后, 子目录采用方拿到的是**诚实降级**而非静默损坏, 可以等。

## 为什么不是 A (改既有字段语义)

三条独立理由, 任一成立即足够:

1. **来源原文就是 A′**。issue-195 正文第 41 行:「`filename` / `track_id` 等需要 basename 的字段**另行派生**」; triage comment `:53`:「`filename` 字段另派生 basename」。本 spec v1 称「issue 与 triage 均倾向 A」系转述失实 (R1 已订正)。
2. **additive-only 契约**。`state-snapshot-schema.md` 的演进声明是「新字段兼容, 删/改字段需 bump」。A 案改的是既有字段的**取值语义**, 与 `snapshot_schema_version` 保持 `"1.0"` 不相容; A′ 只加字段, 契约自然成立。
3. **两处下游副作用在 A 案下才出现**: (a) `_dedupe_sort_key` 第 3 级按 `filename` 字典序取大, `archive/…` 会压过 `2026-…`, 三重并列时归档副本胜出; (b) `state-snapshot-schema.md:1125` 那条「字典序更大 = 更晚」的 tie-break 论据在相对路径下直接变假, 需要连带订正。A′ 下这两条都不发生。

## 代价 (明写, 不粉饰)

- 子目录布局的采用方在本 spec ship 后**仍拿不到 pointer**, 只拿到 `(pointer 不可用)` 横幅 + 原因说明。他们拿到的净收益是: 交接文件不再被伪造成 legacy、`updated_at` 不再是空串、看板不再混入假 track、`scan.py` 不再恒 exit 10。
- 多一个输出字段 `relpath`, 消费方需要知道「拼 git 路径用 `relpath`, 展示用 `filename`」。该约定必须写进 schema 文档与 collector docstring, 否则就是本 spec 自己制造的第二个契约错配。

## 落地约束 (Phase B 必须遵守)

- `relpath` 与 `filename` 的**双字段不变量**: 平铺仓下两者恒相等; 该等式要有一条 SC 钉住 (平铺仓零行为变化的机械表达)。
- 写侧守卫的判据用 `relpath != filename`, **不要**用 `"/" in filename` 之类的字符串嗅探 —— 前者是数据事实, 后者是猜测。
- 守卫命中时必须写明原因, 不得静默退化 (否则就复制了本 spec 正在修的那类「无声失败」)。
- SC-15 必须是**端到端往返**断言: 同一临时仓上 `collect_handoff_multibranch` → `write_latest_md` → `collect_handoff` 三步真跑, 断言顶层 track 走真指针且能读回、子目录 track 走守卫分支且**不产生** `handoff_pointer_target_missing`。

## 请 owner 复议的三点

1. 是否接受「子目录采用方本轮只拿降级 pointer」这个代价, 还是要求本 cycle 内一并做 (ii)。
2. 遗留缺口的 issue 开在 `10CG/aria-plugin` 还是 `10CG/Aria` (前者是代码宿主, 后者是本 spec 宿主; 先例两种都有)。
3. 本单由 AI 在 owner 不在场时裁定, 是否追认。若不追认, Phase B 已落地的 `relpath` 字段与守卫需要回退, 成本约一个 commit。
