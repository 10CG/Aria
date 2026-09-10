# 已归档检测: `user-auth` **未归档** — precheck 放行

按 openspec-archive Step 1 的 `already_archived_precheck` 做了只读检测。未执行归档、未写入任何文件。

---

## 1. 检测结果

Step 1 前置检查 (日期前缀锚定):

```bash
ls openspec/archive/ | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-user-auth$'
```

零命中 (exit 1)。

| 检查项 | 结果 |
|--------|------|
| 锚定式匹配 `^\d{4}-\d{2}-\d{2}-user-auth$` | 0 命中 |
| 宽松子串对照 `grep -i user-auth` | 0 命中 (排除「命名变体已归档」的可能) |
| 你给的裸路径 `openspec/archive/user-auth` | 不存在 |
| CLI bug 残留目录 `openspec/changes/archive/` | 不存在 (无错位归档待修正) |

判定: **未触发 `BLOCKED-already-archived`**, precheck 放行。

语料背景: `openspec/archive/` 共 145 个条目 = 144 个目录 + 1 个 `README.md`, 目录命名 100% 是 `YYYY-MM-DD-{change_name}` 形态。也就是说锚定式检查在这个仓库里没有盲区 —— 不存在「归档了但没带日期前缀因而查不到」的条目。

---

## 2. 你给的三个参数, 有两个需要修正

### 【1】`check_archive=openspec/archive/user-auth` — 路径形态不对, 这个检查恒为假阴性

归档条目带日期前缀 (`openspec/archive/YYYY-MM-DD-user-auth/`), 所以直接 stat `openspec/archive/user-auth` **永远查不到已归档条目**。危害是单向的: 即使 spec 真的已经归档过, 这个检查也会回答「没归档」, 然后放行一次重复归档 —— 而重复归档正是这道 precheck 唯一要防的东西。检查器本身失效, 比没有检查更糟, 因为它给出的是绿灯。

正确形式就是上面那条 grep。另外锚定符 (`^...$`) 也不是装饰: 裸 `grep user-auth` 会把 `2026-01-01-user-auth-v2`、`2026-01-01-legacy-user-auth` 一起算成命中, 造成反方向的假阳性误 block。两端锚定同时挡住这两类误判。

### 【2】`detect_duplicates=true` — openspec-archive 没有这个选项

Skill 的 options 集合是封闭的: `skip_verification` / `keep_changes_copy` / `dry_run` / `archive_design_only` / `reason` / `ack_unverified`。传 `detect_duplicates` 不会报错也不会生效, 它会被静默忽略 —— 你以为打开了一道检查, 实际什么都没打开。

去重在本 Skill 里是**内建行为**, 分两处且各管各的, 都不由开关控制:

- **Step 1 `already_archived_precheck`** — 归档条目去重。命中即立刻 abort, 且**不进入完成度判定、不写任何标记** (标记写入属 Step 2, 所以 abort 路径零残留)。
- **Step 7 tracker issue 去重** — search-before-create, marker = `<!-- archive-tracker:{spec_id} -->` 精确子串匹配 (非模糊 title 匹配), 分页遍历全部 open issue (每页 50 逐页翻, 避免仓库 open issue > 50 时漏掉既有 tracker 而重复开单)。

如果你想表达的是「只检测不执行」, 对应的真实开关是 `dry_run=true`。本次我就是按这个语义走的。

### 【3】`spec_path=openspec/changes/user-auth` — 形态正确

「检测是否已归档」这个问题只需要 archive 侧的证据, 所以本次我没有去读 spec 内容 —— 它属于下一道门 (完成 gate) 的输入, 见下。

---

## 3. 下一步 (若确实要归档 user-auth)

precheck 放行只是第一道门, 它只回答了「没重复归档过」, 没有回答「该不该归档」。接下来是 Step 1 的完成 gate + C 分级证据闸, 单次调用同时拿到二元 completeness 和 tri-state verdict:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/lib/spec_complete.py" \
  --gate "openspec/changes/user-auth"
```

读 stdout JSON 的 `verdict` 字段做路由, **不能只看 exit code** —— exit 0 是 `pass|warn` 二合一的粗粒度信号, 区分不出 warn, 而 warn 需要额外写 frontmatter `unverified_claims` 并 surface 提示。

四种组合的处置:

| 组合 | 处置 |
|------|------|
| `complete=true ∧ verdict=pass` | 正常归档 (Step 2 路径 a) |
| `complete=true ∧ verdict=warn` | 正常归档 + warn_overlay 写 frontmatter + Step 7 建 tracker issue |
| `complete=true ∧ verdict=block` | **BLOCK** — 高置信死代码, tasks.md 全 `[x]` 也不放行 (完成是跑出来的, 不是勾出来的) |
| `complete=false` | BLOCK, 除非配 `--archive-design-only` + ≥10 非空白字符的 reason |

另一个容易混的分支: 如果 `openspec/changes/user-auth` 根本不存在, 那**不是**「已归档」, 而是错误处理表里的「变更目录不存在 (change_name 拼写错误)」。两者结论都是「别继续」, 但原因与处置完全相反 —— 前者该去 archive 里找那份已完成的记录, 后者该去核对拼写。别把后者读成前者。

---

## 4. 本次动作声明

- 全程只读 (`ls` + `grep`)。无写入、无 `git mv`、无 `openspec archive` 调用、无 issue 创建。
- 未写任何标记 —— 标记写入属 Step 2, precheck 阶段零残留。
- 需要我接着跑 `--gate`, 或先 `dry_run=true` 完整过一遍归档流程看结果, 说一声。
