好的, 按 A.1 (spec-drafter) 起草。先交代三个前置项怎么处理的, 再给预览和 proposal.md 全文 —— 按你的要求**只输出, 不写入仓库**。

---

## 前置 1 — A.1 认领 (REQUIRE claim, MUST): 本轮**未执行**

spec-drafter 的 A.1 前置要求「起草之前先认领」(跑 `phase1_gate.py`), 而你这次显式要求不要运行 git 或任何脚本。所以我没跑。两点必须说清:

- 这是**执行条件不具备**, 不是我判断「这次不值得跑」而豁免掉 —— 闸门本身仍然成立。
- 因此远端碰撞状态现在是**未知**。按四态读法, 这轮的正确措辞是「本轮未检测」, **不能**写成「无碰撞」—— 零证据不是正证据。真正落盘起草前请补一次:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "state-scanner-issue-label-filter-<container_uuid>" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path /home/dev/Aria
```

注意这条命令里**故意没有** `--linked-issue`: 本 Spec 已核实无关联 issue, 字段值是哨兵 `none`, 而哨兵 (含 `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD`) 一律**省略整个参数**, 绝不可把哨兵当值传 —— 任何非空字符串都 truthy, 两份毫无关系的 Spec 只要都写哨兵就会互相命中。这条与「跑不跑脚本」无关, 补跑时也照此。

`--raw-track-id` 的 uuid 段取 `~/.aria/container-id` 的 `uuid` 字段 (不是 `label`)。后续若改 Spec 目录名 = 换 track-id, 须 `release 旧 + acquire 新`; 放弃方向须 `release_gate.py --status abandoned`。

## 前置 2 — A.1.0 头脑风暴检查

`docs/decisions/` 下 20 份决策记录均为其他主题 (M6 遥测 / 审计闸门 / 多终端协调等), **无**本主题的技术决策。按 OpenSpec 集成的选项 [2] 直接创建。

据此提醒一句: 下面 §What 里「后置过滤 + 追加 `label_filter` 子对象」而不是「直接过滤 `items`」是我做的技术级取舍 (理由见 Impact 风险行), 没经过 brainstorm.technical。若你想并列比较备选方案, 可以回补一次决策记录再让 proposal 引它。

## 前置 3 — Level 判定与落点

| 维度 | 判定 |
|------|------|
| 关键词 | 「加一个可选参数」= 增强改进词 (extend/optional param), 无 refactor / breaking / 跨模块词汇 |
| 影响范围 | 单模块: aria-plugin `state-scanner` skill (scripts + references + tests), 4-6 个文件 |
| 变更类型 | 追加式, 不传参时行为逐键不变 → 非 breaking |
| 结论 | **Level 2 (Minimal)** —— 与你指定的一致, 只出 proposal.md, 不出 tasks.md |

落点 `openspec/changes/state-scanner-issue-label-filter/proposal.md` (**Aria 主仓内**), 不是 `standards/openspec/changes/` —— standards 是共享子模块, 项目变更写进去会对所有采用方可见且无人拥有 (不可协商规则 #5)。slug 与现有 7 个 change 目录无碰撞。

---

## Level 2 预览

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: state-scanner-issue-label-filter
Module: standards (aria-plugin / state-scanner skill)
Location: openspec/changes/state-scanner-issue-label-filter/proposal.md
Status: 本轮仅预览, 未写入 (按你的要求)
```

## proposal.md 全文

```markdown
# state-scanner Open Issues 标签过滤参数

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

🎫 Open Issues (Phase 1.13, opt-in) 目前只有一个**配置级**标签过滤:
`state_scanner.issue_scan.label_filter` (`.aria/config.template.json:51`, 默认 `[]`)。
它的实现位置对「这一次只想看 bug」这个用法是错的, 三个可核对的事实:

1. 它是持久配置, 不是临场参数 —— 想临时收窄只能改 `.aria/config.json` 再改回来。
2. 过滤发生在 `_fetch_repo` 内 (`scripts/collectors/issue_scan.py:536-538`,
   `wanted.intersection(...)`), 即**写缓存之前**; 被滤掉的 issue 不进
   `.aria/cache/issues.json` (`:817` `_write_cache_atomic`), 因此缓存命中路径下换过滤
   条件必须等 TTL (默认 900s) 过期才能拿到全集。
3. `scan.py` 的 CLI 只有 `--project-root` / `--output` / `--log-level` 三个参数
   (`scripts/scan.py:435-462`), 单次调用没有任何过滤入口; `build_snapshot(project_root)`
   (`:288`) 与 `collect_issue_scan(project_root)` (`:589`) 也都只收一个位置参数。

## What

给 `scan.py` 增加可选参数 `--issue-label` (可重复), 在 issue_status 采集完成**之后**
(缓存与实时两条路径合流之上) 做只读的后置过滤, 结果写入新增的 `issue_status.label_filter`
子对象。既有 `items` / `open_count` 语义不变, 缓存 payload 不变, 配置级 `label_filter`
的位置与语义不变。

- **匹配语义**: item 的 `labels` 与参数集合交集非空即命中 (OR), 精确字串、大小写敏感 ——
  与配置级过滤 (`issue_scan.py:536-538`) 同一套判据, 不引入第二种语义。
- **组合**: 配置级过滤仍在 fetch 时先作用, 运行时参数在其结果上再过滤 (构造上即 AND);
  `label_filter.config_labels` 回显配置值, 让「0 命中」可解释。
- **不传参**: 不产生 `label_filter` key, 输出与改动前逐键一致。

新增字段形状:

    issue_status:
      label_filter:                     # 仅在传了 --issue-label 时出现
        labels: ["bug"]                 # 本次请求的标签集
        config_labels: []               # 回显配置级 label_filter, 让 0 结果可解释
        open_count: 1                   # 过滤后条数
        items: [...]                    # 过滤后条目 (items/open_count 原字段不动)

### Key Deliverables
- `aria/skills/state-scanner/scripts/scan.py` — `--issue-label` (action=append) +
  `build_snapshot(project_root, *, issue_labels=None)` keyword-only 追加参数, 既有调用点不改
- `aria/skills/state-scanner/scripts/collectors/issue_scan.py` —
  `collect_issue_scan(project_root, *, label_filter_arg=None)` 后置过滤 + `label_filter` 子对象
- `aria/skills/state-scanner/references/output-formats.md` — §Open Issues 增「过滤生效」
  「零命中」两个变体 (区块头 `🎫 Open Issues` 不变)
- `aria/skills/state-scanner/references/state-snapshot-schema.md` +
  `references/issue-scanning.md` — 新字段定义 + 两级过滤关系说明
- `aria/skills/state-scanner/tests/test_issue_scan_mocked.py` — 新增用例 (见 Success Criteria)

## Out of Scope

- 不改配置级 `label_filter` 的位置与语义 (仍在 fetch 时作用、仍进缓存)。
- 不做 AND / 正则 / 否定匹配, 本版固定 OR 交集。
- 不改 `scan_submodules` 的聚合行为与 `limit` 上限。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 单次扫描即可临时收窄 🎫 区块, 不必为「只看 bug」改 config 再改回来; 过滤集不落缓存, 换条件无需等 TTL |
| **Risk** | 两级过滤叠加会让「0 命中」难归因 → 缓解: `config_labels` 回显 + 渲染层在 config 非空时明写「config label_filter 生效中」 |
| **Risk** | 既有消费者读 `issue_status.items` / `open_count` → 缓解: 新字段纯追加, 不传参时该 key 不出现 (SC-1 钉死) |

## Tasks

- [ ] `collect_issue_scan` 加 keyword-only 参数, 在缓存/实时两路合流后做后置过滤
- [ ] 新增 `issue_status.label_filter` 子对象 (labels / config_labels / open_count / items)
- [ ] `scan.py` 加 `--issue-label` 并透传 `build_snapshot`
- [ ] 三份 references 同步 (output-formats 两变体 / snapshot schema 字段 / issue-scanning 两级过滤)
- [ ] 补测试 (SC-1~SC-6)
- [ ] Rule #6: 本变更动到 state-scanner 的运行时指令面, 发版前用 `/skill-creator` 跑 AB benchmark

## Success Criteria

- [ ] SC-1 不传参零回归: 无 `--issue-label` 时 `issue_status` 与改动前逐键一致, 且**不含**
      `label_filter` key。红: 该 key 出现, 或任何既有键值变化
- [ ] SC-2 缓存命中也过滤: 热缓存 fixture (labels 分别 `[bug]` / `[enhancement, skill]` /
      `[feature]`) + `--issue-label bug` → `label_filter.open_count == 1`,
      同时 `open_count == 3` 且 `len(items) == 3`。红: 过滤只挂在 live 路径, 或误改 `items`
- [ ] SC-3 缓存不被污染: live fetch + `--issue-label bug` 后, `.aria/cache/issues.json` 的
      items 数 == 未过滤数且无 `label_filter` key。红: 过滤集被持久化 (即复刻 `:536-538` 的缺陷)
- [ ] SC-4 零命中形状固定: `--issue-label nonexistent` →
      `label_filter == {"labels": ["nonexistent"], "config_labels": [], "open_count": 0, "items": []}`,
      退出码与不传参相同。红: 抛错 / 缺 key / 退出码变化
- [ ] SC-5 opt-in 边界不变: `issue_scan.enabled=false` 时传 `--issue-label` 仍输出
      `{"enabled": false}` 且不发起任何网络调用。红: 参数意外唤醒 opt-in 区块
- [ ] SC-6 文档同步: `tests/test_output_format_sync.py` 绿 (10 个 canonical 区块头不变),
      且 `output-formats.md` §Open Issues 下可 grep 到两个新变体小节。红: 区块头被改名 / 变体缺失
```

---

## Linked Issue 字段自检 (对照写法三条)

你说了「这个功能没有关联的 issue (已核实)」, 所以走的是哨兵分支:

1. **值是 inline code span**: 写作 `` `none` ``, 不是裸文本 —— ✅
2. **无关联时逐字写 `none`**: 不留空、不删行 (空值与「忘了写」不可区分); `N/A` / `TBD` / `-` 都**不是**合法哨兵, 会被机械 check 判不合规 —— ✅
3. **行首无空白, `>` 后恰一个空格, 字段名两侧各两星号, ASCII 冒号, 不写 markdown 链接形** —— ✅

字段顺序按 SOT 模板 `Level` → `Status` → `Created` → `Linked Issue`, 从模板起草自然满足。顺序只是起草侧建议, 不是机械 check 的判据 (check 按 E0 取文档序第一条 depth-1 命中, 不限行号) —— 所以别为了「对齐」去改动既有 proposal 的头部顺序。

## 后续

1. **补跑 A.1 认领** (见前置 1), 确认远端没有人在做同一件事 —— 认领必须早于投入, 否则它记录的只是既成事实。
2. 落盘后跑 `openspec validate state-scanner-issue-label-filter --strict` 验证格式。
3. 进入 A.2 (`/task-planner`) 做任务分解与 Agent 分配。
4. 这是 state-scanner 的行为面变更, 发版前须过 Rule #6 AB benchmark (已写进 Tasks)。

本轮**没有**创建任何文件、没有跑 git 或脚本, 上面 proposal.md 全文即最终产物, 你确认后我再落盘。
