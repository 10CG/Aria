# OpenSpec 归档: user-auth (Phase D.2)

## 结论先行: 你给的 `expected_archive` 路径是错的

你写的 `expected_archive=openspec/archive/user-auth` 缺了日期前缀。归档目录名必须带 `YYYY-MM-DD-` 前缀:

```
正确目标:      openspec/archive/2026-09-08-user-auth/
你写的:        openspec/archive/user-auth/                    ← 缺日期前缀
CLI 实际会输出: openspec/changes/archive/2026-09-08-user-auth/ ← 已知 CLI bug, 父目录错
```

这里有**两处独立的偏差**, 别混成一件事:

【1】**日期前缀** —— `openspec archive` 生成的归档目录名恒为 `YYYY-MM-DD-{change-name}`, 按归档日期分桶。今天是 2026-09-08, 所以本次归档落点是 `openspec/archive/2026-09-08-user-auth/`。这不是我加的装饰, 归档流程的 already-archived 前置检查用的就是日期锚定正则:

```bash
ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-user-auth$'
```

一个不带日期前缀的 `openspec/archive/user-auth/` **不会**被这条检查识别为"已归档"。所以路径写错不只是命名不统一的问题 —— 它会让重复归档的幂等保护直接失效, 同一个 spec 可以被归档两次而无人报警。

【2】**父目录 (CLI bug)** —— `openspec archive` CLI 有已知 bug, 会把结果写到 `openspec/changes/archive/` 而不是 `openspec/archive/`。归档流程的 Step 4 会自动检测并修正 (移动 + `rmdir` 清理空的 `openspec/changes/archive/`), 这一步不用你手动做。

正确的目录结构长这样:

```
openspec/
├── archive/                          # 正确的归档位置
│   └── 2026-09-08-user-auth/
│       ├── proposal.md
│       ├── tasks.md
│       └── detailed-tasks.yaml
└── changes/                          # 只放活跃变更
    └── {其它未归档的 change}/
```

---

## 当前阻塞: `project_root` 在本环境不可达

我在动手前先核了一遍工作目录, `/workspace/my-project` 不存在 (`/workspace` 本身也没有):

```
$ ls -d /workspace/my-project
ls: cannot access '/workspace/my-project': No such file or directory
```

所以本次**没有执行任何归档动作**, 没有移动/删除/新建任何文件, 也没有跑 gate。下面给出完整的执行计划与逐条命令, 你把可达的 `project_root` 给我 (或确认换成实际路径) 之后我照此执行。

需要说明的是: 归档的放行与否**不是我拍脑袋定的**, 由 `spec_complete.py --gate` 这个可执行 SOT 给出裁决。在拿到它的实际输出之前, 我不能预判 `user-auth` 这个 spec 能不能归档 —— 它可能任务没勾完 (complete=false), 也可能任务全勾但存在零生产引用的死代码声称 (verdict=block)。这两条都是硬门。

---

## 归档执行计划

### Step 1 — 完成 gate + C 分级证据闸

先做 already-archived 前置检查 (最前, 命中即 abort, 不写任何标记):

```bash
ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-user-auth$'
```

命中 → `BLOCKED-already-archived`, 立即中止。

未命中 → 调 gate 拿三态裁决:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
  --gate "openspec/changes/user-auth"
```

读 stdout JSON 的 `{complete, complete_reason, verdict, blocking_reasons[], warnings[], unverified_claims[], d_payload, soft_errors[]}`。

关键: **读 JSON 的 `verdict` 字段做路由, 不能只看 exit code**。exit code 把 pass 和 warn 合并成一个 0, 分不出来 —— 但 warn 需要额外写 frontmatter 并向你 surface 提示, pass 不需要。

路由 (completeness 与 verdict 是两根正交的轴):

| complete | verdict | 处置 |
|----------|---------|------|
| true | pass | 放行, 正常归档 |
| true | warn | 放行 + surface warnings + 写 frontmatter `unverified_claims` |
| true | block | **BLOCK** —— 高置信死代码, 任务全勾也不放行 (完成是跑出来的, 不是勾出来的) |
| false | pass/warn | BLOCK, 回显 `complete_reason` 列出缺口 |
| false | block | BLOCK, 回显 `complete_reason` **和** `blocking_reasons` 两组缺口 |

如果被 BLOCK 且你确认残留待补但仍需归档设计稿, 逃生舱是 `--archive-design-only` + `reason` (≥10 个非空白字符), 且输出里会显式回显被豁免的 `blocking_reasons`, 不静默吞掉。

### Step 2 — 写 `proposal.md`

- 路径 (a) 正常归档: `Status` 非 done 时更新为 Complete。
- 路径 (b) design-only: 不改 Status, frontmatter 追加 `archive_type: implementation-deferred` + `archived_reason`。
- warn 覆盖层 (verdict=warn 时, 与 a/b 正交叠加): frontmatter 写入 `unverified_claims` (逐条 claim/reason/symbols) + `unverified_ack`。

### Step 3 — 执行 CLI

```bash
openspec archive user-auth --yes
```

### Step 4 — 检测并修正归档位置 (CLI bug 修正, 关键步)

```bash
# CLI 大概率把结果落在这里
test -d openspec/changes/archive && {
  mv openspec/changes/archive/* openspec/archive/
  rmdir openspec/changes/archive
}
```

若 `openspec/changes/archive/` 不存在, 则直接验证 `openspec/archive/2026-09-08-user-auth/` 是否已就位。

### Step 5 — 清理活跃变更目录

```bash
rm -rf openspec/changes/user-auth      # 除非 keep_changes_copy=true
```

### Step 6 — 验证归档结果

```bash
ls -la openspec/archive/2026-09-08-user-auth/
# 期望: proposal.md / tasks.md / detailed-tasks.yaml 齐全
test ! -d openspec/changes/archive && echo "wrong_dir_cleaned: true"
```

### Step 7 — D auto-issue (归档不吞未完成)

仅当 Step 1 的 `gate_result.d_payload != null` (存在 deferred 项或 unverified 声称) 才触发; 干净归档直接跳过, 零输出。

触发时: 解析 `git remote get-url origin` 拿 `{owner}/{repo}` → 分页遍历全部 open issue,用 marker `<!-- archive-tracker:user-auth -->` 精确子串去重 → 未命中才 `forgejo POST` 建 tracker issue。非 Forgejo 后端 / API 失败 → 打印草稿 + WARN, 但**归档本身不 abort**。

---

## 预期输出 (执行成功后)

```yaml
success: true
change_name: "user-auth"
archive_path: "openspec/archive/2026-09-08-user-auth"    # 注意日期前缀
cli_bug_fixed: true
warnings: []
verification:
  archive_exists: true
  contains_proposal: true
  contains_tasks: true
  contains_detailed_tasks: true
  wrong_dir_cleaned: true
```

---

## 需要你确认两件事

【1】**路径更正**: `expected_archive` 改为 `openspec/archive/2026-09-08-user-auth` (带日期前缀)。如果你的下游有硬编码 `openspec/archive/user-auth` 的检查/脚本, 那处也要一并改, 否则归档成功了它仍会报找不到。

【2】**可达的 project_root**: `/workspace/my-project` 在当前环境不存在。给我真实路径后我就按上面的 Step 1-7 执行 —— 建议第一步先跑 `dry_run=true`, 它会完整跑 Step 1 的 gate 判断并报告三路结果 (ALLOWED / BLOCKED / ALLOWED-design-only), 同时保证不落任何写入, 这样你能在真正动文件之前看到 `user-auth` 到底过不过门。
