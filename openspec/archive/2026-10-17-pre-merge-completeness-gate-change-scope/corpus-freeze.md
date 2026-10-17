# corpus-freeze.md — TASK-002 语料冻结产物

> **交付物身份**: 本文件是 proposal.md `## Tasks` **B.0 语料冻结产物** (`:409-428`) 的直接交付物,
> 是 SC-2 (`:458`) 六族样本与 SC-4 (`:460`) 判据口径的**标注列来源**。TASK-004 写测试时,
> 本文件各族样本表里「标注结果」列的字面量可直接抄进断言, **不得**改由调用被测谓词
> (`completeness_gate.py`, 本次由另一实例实现, 本文件作者未写、未读该脚本的任何一行) 现算。
> 执笔: qa-corpus-A (标注者), 与实现者不同席, 满足 proposal 内联 Tasks B.0 段首「标注必须
> 双列交叉」前置的角色分离要求。
> 前置门状态: tasks.md「读前必看」第 18 条 —— B.0 段内 R5 rework 第 5 条设的「复议项前置门
> (复议条目 1 / 7 / 8 / 10 / 11 / 13 未裁不进 TDD RED)」(转述: 原文条目号带 `#` 前缀, 按 content-integrity §4.4 改为纯数字)已由决策单全部裁定并解除; 本文件属于
> B.0 的「语料冻结与双列标注」部分, 该门原文也未拦这部分, 现状态与本文件的产出方式无冲突。

## 0. 冻结坐标

| 项 | 值 |
|---|---|
| 冻结提交 F (主仓) | `8d2ff8b1ce1dada8ef70729f136739db60f42a4b` |
| F 的性质 | 主控指定为本 cycle B.1 起点; 取样时刻同时等于 `origin/master` 与本地 `HEAD` (`git rev-parse` 三者一致) |
| F 的提交时间 | `2026-09-30 02:34:24 +0000` (`git log -1 --format=%ci`) |
| 取样执行 UTC 时刻 | `2026-09-30T07:19:04Z` (`date -u +%Y-%m-%dT%H:%M:%SZ`, 与下方 STEP 0-2 同一次连续终端会话执行, 见 1.1) |
| 标注者 / 执行标签 | qa-corpus-A (执行实例), 不写、不读 `completeness_gate.py` 任何实现代码 |
| 依据 (proposal.md 行号, 冻结于本 change 自身工作树, 未 rebase) | Tasks B.0 `:409-428`; §1.2 报告归属匹配规则 `:187-208`; §1.2b 枚举范围 `:210-224`; SC-2 `:458`; SC-4 `:460` |
| 依据 (tasks.md) | 读前必看 第 18 条 (`:34`, 复议前置门解除) |

---

## 1. 取样

### 1.1 取样命令与退出码 (原样终端记录)

以下命令在主仓根 `/home/dev/Aria` 连续执行 (未 `cd` 进子目录, 未 `checkout`/`fetch`/`pull`, 只读):

```text
$ git cat-file -e 8d2ff8b1ce1dada8ef70729f136739db60f42a4b && echo COMMIT_EXISTS_OK
COMMIT_EXISTS_OK                                                    # exit 0

$ git rev-parse origin/master
8d2ff8b1ce1dada8ef70729f136739db60f42a4b                            # exit 0

$ git rev-parse HEAD
8d2ff8b1ce1dada8ef70729f136739db60f42a4b                            # exit 0

$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-09-30T07:19:04Z

$ python3 -B freeze_corpus.py 8d2ff8b1ce1dada8ef70729f136739db60f42a4b \
    --repo-root /home/dev/Aria --json classify_F.json
commit F = 8d2ff8b1ce1dada8ef70729f136739db60f42a4b
C size = 154 (changes_raw=7, archive_raw=147, union_before_dedupe=154)
top-level .aria/audit-reports/*.md count = 987
top-level subdirs excluded (not recursed) = ['pr19-submodule-scan', 'wf-r1fix']
bucket counts: {'legacy_shaped': 6, 'matched': 800, 'no_checkpoint_prefix': 11, 'unattributed_shaped': 170}
                                                                      # exit 0

$ python3 -B select_samples.py classify_F.json /home/dev/Aria > select_samples_output.txt
                                                                      # exit 0 (完整输出见 3/4 两章)

$ sha256sum classify_F.json
8e7db8fb2f26afbc64bc7d3cf841159d5388928204abd8b5dd0f1a38592a65cd  classify_F.json
```

第二次独立重跑 (改动仅一处引号剥离逻辑的字面等价重写后自我复核, 非跨实例复现) 得到
**逐字节相同**的 `classify_F.json` (同一 sha256) 与逐字节相同的 `select_samples.py` 输出
(`diff` 退出 0)。跨实例复现见第 6 章。

### 1.2 C 的计算 (openspec/changes/\* ∪ openspec/archive/\* 去日期前缀)

```
$ git ls-tree --name-only -d 8d2ff8b1ce1dada8ef70729f136739db60f42a4b -- openspec/changes/ | wc -l
7
$ git ls-tree --name-only -d 8d2ff8b1ce1dada8ef70729f136739db60f42a4b -- openspec/archive/ | wc -l
147
```

`openspec/changes/*` 的 7 个 (原样目录名, 无日期前缀需去):

```
aria-2.0-m6-cost-model-telemetry
aria-2.0-m6-dispatch-input-delivery
aria-2.0-m6-e2e-resilience
aria-2.0-m6-release-closeout
aria-2.0-m7-agent-lifecycle
aria-2.0-m7-fleet-aggregation
pre-merge-completeness-gate-change-scope        # 本 spec 自身, 在 C 内
```

`openspec/archive/*` 147 个原始目录名去 `^\d{4}-\d{2}-\d{2}-` 前缀后, 与上面 7 个取并集:
**`|C| = 154`**, 与 7 + 147 的算术和相等 ⇒ **两侧 id 无重名碰撞** (去重前后大小相同)。

> 对照: A.2 阶段 (`a563192`, 2026-09-12 附近) 记的 `|C| = 154` 与本次在 F (2026-09-30,
> 晚 18 天) 实测的 `154` **数值巧合相等**, 但不是同一批 id —— 期间有 change 被归档、有新
> change 开工, 具体构成已变 (例如本 spec 自身在 A.2 时也在 `openspec/changes/` 下, 现在
> 仍在, 未归档)。**本文件的 `|C|=154` 以 F 为准, 不外推**, 后续若在别的提交上复现, 概不
> 假设这个数字不变 (语料是活体, tasks.md 读前必看多处强调此点)。

### 1.3 `.aria/audit-reports/` 顶层文件集 (不递归)

```
$ git ls-tree 8d2ff8b1ce1dada8ef70729f136739db60f42a4b -- .aria/audit-reports/ | \
    awk '{print $2}' | sort | uniq -c
    987 blob
      2 tree
```

顶层两个子目录 (§1.2b 已定义的边界: 只扫顶层, 不递归) 按定义**排除**, 不计入下列任何族:

```
.aria/audit-reports/pr19-submodule-scan/
.aria/audit-reports/wf-r1fix/
```

987 个顶层 blob 全部以 `.md` 结尾 (非 `.md` 顶层 blob 命中数 = 0)。`scanned_dir_depth = 1`
的口径 (§1.2b) 在本次取样与之完全一致: 两个子目录内容一份也未读。

---

## 2. 可复跑脚本 (全文)

两个脚本均只用 Python 标准库 (`subprocess` / `re` / `json` / `argparse` / `collections`)
调 `git`, 不 `import` 也不调用 `aria/skills/audit-engine/scripts/completeness_gate.py`
(该脚本本次由另一实例实现, 未写入本仓; 本文件全程未读它的任何字节)。两个脚本都不写盘、
不 `git` 任何写操作, 只读 `git ls-tree` / `git cat-file --batch`。

### 2.1 `freeze_corpus.py` — 取样 + 双列标注 + 六族候选归类

```python
#!/usr/bin/env python3
"""corpus-freeze.py — TASK-002 可复跑取样脚本 (qa-corpus-A)

用途: 对主仓某个冻结提交 F, 重建:
  1. C = openspec/changes/* 与 openspec/archive/* (去 YYYY-MM-DD- 前缀) 的目录名集合
  2. .aria/audit-reports/ 顶层 .md 文件全量清单 (不递归)
  3. 对每个文件计算:
     - 第一列 (frontmatter 来源定序 + prose->id 归一化, 只读 frontmatter, 不读文件名)
     - 第二列 (§1.2 规则 1-3 的文件名匹配: 末段/中缀双侧界定 + 有界包含排除)
     - 六族候选归类 (F-a..F-f) 与 (b1)/(b2) 机械仲裁

不依赖、不导入 aria/skills/audit-engine/scripts/completeness_gate.py (该脚本本次未写,
本脚本是独立的标注工具, 不是被测实现)。

用法:
    python3 -B freeze_corpus.py <commit-sha> [--json OUT.json]

只用 subprocess 调 git 与标准库, 无第三方依赖。
"""
import subprocess
import re
import sys
import json
import argparse
from collections import defaultdict

CANONICAL_CHECKPOINTS = [
    "post_brainstorm",
    "post_spec",
    "post_planning",
    "mid_implementation",
    "mid_post_spec",
    "post_implementation",
    "pre_merge",
    "post_closure",
]

ARCHIVE_DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
LEGACY_REST_RE = re.compile(r"^[0-9TZ:.\-]+$")
ROUND_MARKER_RE = re.compile(r"-R\d+-")


def run_git(args):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=REPO_ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed rc={r.returncode}: {r.stderr}")
    return r.stdout


def compute_C(commit):
    """C = (openspec/changes/* 目录名) ∪ (openspec/archive/* 目录名去 YYYY-MM-DD- 前缀)"""
    changes = run_git(["ls-tree", "--name-only", "-d", commit, "--", "openspec/changes/"])
    archive = run_git(["ls-tree", "--name-only", "-d", commit, "--", "openspec/archive/"])
    changes_names = [l.rsplit("/", 1)[-1] for l in changes.splitlines() if l.strip()]
    archive_names_raw = [l.rsplit("/", 1)[-1] for l in archive.splitlines() if l.strip()]
    archive_names = [ARCHIVE_DATE_PREFIX_RE.sub("", n) for n in archive_names_raw]
    C = set(changes_names) | set(archive_names)
    return C, {
        "changes_dir_count_raw": len(changes_names),
        "archive_dir_count_raw": len(archive_names_raw),
        "union_before_dedupe": len(changes_names) + len(archive_names),
        "C_size": len(C),
    }


def list_audit_report_files(commit):
    """顶层 (不递归) .aria/audit-reports/ 下的 blob, 含 sha, 用于批量 cat-file。"""
    out = run_git(["ls-tree", commit, "--", ".aria/audit-reports/"])
    files = []  # (basename, blob_sha)
    trees = []
    for line in out.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t", 1)
        _mode, otype, osha = meta.split(" ")
        basename = path.rsplit("/", 1)[-1]
        if otype == "blob":
            if basename.endswith(".md"):
                files.append((basename, osha))
            # 非 .md 的顶层 blob: 本仓实测 0 个, 若未来出现则落 unclassified, 不计入任何族
        elif otype == "tree":
            trees.append(basename)
    return files, trees


def batch_read_blobs(shas):
    """git cat-file --batch 一次性读全部内容, 避免 987 次子进程。返回 {sha: bytes}。"""
    input_data = ("\n".join(shas) + "\n").encode("utf-8")
    r = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=input_data,
        capture_output=True,
        cwd=REPO_ROOT,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git cat-file --batch failed rc={r.returncode}: {r.stderr}")
    data = r.stdout
    out = {}
    pos = 0
    for sha in shas:
        header_end = data.index(b"\n", pos)
        header = data[pos:header_end].decode("utf-8")
        parts = header.split(" ")
        _sha, _type, size = parts[0], parts[1], int(parts[2])
        content_start = header_end + 1
        content = data[content_start : content_start + size]
        out[sha] = content
        pos = content_start + size + 1  # skip trailing \n after object content
    return out


def extract_frontmatter_fields(text):
    """只解析开头 --- ... --- 之间的顶层 `key: value` 行, 取 change_id/spec_id/context。
    不做完整 YAML 解析 (逃避 list/嵌套块语法), 逐字取冒号后原始字符串。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):[ \t]?(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            if key not in fields:
                fields[key] = val
    return fields


QUOTE_CHARS = "`\"'"


def strip_quote_ends(s):
    """『去掉首尾的 ` / " / \'』按字面独立处理两端: 左端是这三者之一就去掉左端一个字符,
    右端独立同理 (不要求两端字符相同, 也不要求成对出现)。"""
    if s and s[0] in QUOTE_CHARS:
        s = s[1:]
    if s and s[-1] in QUOTE_CHARS:
        s = s[:-1]
    return s


def normalize_first_column(raw_value):
    """Tasks B.0 三步算法 step 2-3。raw_value 为 None 表示该字段不存在/空 (由调用方在 step1 处理)。
    返回归一化字符串; 空串表示『取不到』。"""
    v = strip_quote_ends(raw_value.strip())
    m = re.match(r"^openspec/changes/([^/\s]+)", v)
    if m:
        return m.group(1)
    m = re.match(r"^openspec/archive/(?:\d{4}-\d{2}-\d{2}-)?([^/\s]+)", v)
    if m:
        return m.group(1)
    tokens = v.split()
    token = tokens[0] if tokens else ""
    token = strip_quote_ends(token)
    return token


def column1_value(fields):
    """来源定序 change_id > spec_id > context, 取第一个存在且值非空的字段。
    返回 (status, source_key, raw, normalized):
      status = 'ok' | 'missing'
    """
    for key in ("change_id", "spec_id", "context"):
        if key in fields and fields[key].strip() != "":
            raw = fields[key]
            norm = normalize_first_column(raw)
            if norm == "":
                return ("missing", key, raw, "")
            return ("ok", key, raw, norm)
    return ("missing", None, None, None)


def checkpoint_of(basename):
    for cp in CANONICAL_CHECKPOINTS:
        if basename.startswith(cp + "-"):
            return cp
    return None


def rule2_hits(stem, C):
    """§1.2 规则 2: f 命中 c 当且仅当 f'-{c}-' in f 或 stem.endswith(f'-{c}')。
    这里用 stem (已去 .md) 即可, 因为规则 2 原文对 f (含 .md) 判断 `-{c}-` 子串,
    对 stem 判断末段; 用 stem 判断子串子集不受影响 (.md 不含 '-'), 在此统一用 stem。"""
    hits = set()
    for c in C:
        if (f"-{c}-" in stem) or stem.endswith(f"-{c}"):
            hits.add(c)
    return hits


def rule3_filter(raw_matches):
    """§1.2 规则 3: 有界包含排除 (对称)。若 c' 是 cid 的『超串』(以 cid- 开头 / 以 -cid 结尾 /
    含 -cid-) 且 c' 也在 raw_matches 中 (即 f 按规则 2 命中 c'), 则 cid 被排除。"""
    final = set()
    for cid in raw_matches:
        superseded = False
        for c2 in raw_matches:
            if c2 == cid:
                continue
            if c2.startswith(cid + "-") or c2.endswith("-" + cid) or (f"-{cid}-" in c2):
                superseded = True
                break
        if not superseded:
            final.add(cid)
    return final


def classify_file(basename, content_bytes, C):
    text = content_bytes.decode("utf-8", errors="replace")
    fields = extract_frontmatter_fields(text)
    col1_status, col1_source, col1_raw, col1_norm = column1_value(fields)

    stem = basename[:-3] if basename.endswith(".md") else basename
    cp = checkpoint_of(basename)

    rec = {
        "file": basename,
        "checkpoint": cp,
        "col1_status": col1_status,
        "col1_source": col1_source,
        "col1_raw": col1_raw,
        "col1_normalized": col1_norm,
    }

    if cp is None:
        rec["bucket"] = "no_checkpoint_prefix"
        return rec

    rest = stem[len(cp) + 1 :]
    is_legacy_shaped = bool(LEGACY_REST_RE.match(rest)) and len(rest) > 0

    raw_matches = rule2_hits(stem, C)
    final_matches = rule3_filter(raw_matches)

    if is_legacy_shaped and not final_matches:
        rec["bucket"] = "legacy_shaped"  # F-e candidate
        rec["final_matches"] = []
        return rec

    if not final_matches:
        rec["bucket"] = "unattributed_shaped"  # F-f candidate (pre b2 screen)
        rec["final_matches"] = []
        return rec

    # matched (one or more, after rule3 — 真实语料预期恰为 1)
    rec["final_matches"] = sorted(final_matches)
    shapes = []
    for cid in final_matches:
        tail = stem.endswith(f"-{cid}")
        aggregated = bool(re.search(r"-(aggregated|aggregate)(-|$)", stem)) or stem.endswith(
            f"-{cid}-aggregated"
        ) or stem.endswith(f"-{cid}-aggregate")
        no_round = not bool(ROUND_MARKER_RE.search(stem))
        shapes.append(
            {
                "change_id": cid,
                "shape_tail": tail,
                "shape_role_suffix": not tail,
                "shape_aggregated": aggregated,
                "shape_no_round_marker": no_round,
            }
        )
    rec["bucket"] = "matched"
    rec["shapes"] = shapes
    return rec


def main():
    global REPO_ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument("commit")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    REPO_ROOT = args.repo_root

    C, c_stats = compute_C(args.commit)
    files, trees = list_audit_report_files(args.commit)

    shas = [sha for _, sha in files]
    blob_map = batch_read_blobs(shas)

    records = []
    for basename, sha in files:
        rec = classify_file(basename, blob_map[sha], C)
        records.append(rec)

    result = {
        "commit": args.commit,
        "C_size": len(C),
        "C_stats": c_stats,
        "top_level_md_count": len(files),
        "top_level_subdirs_excluded": sorted(trees),
        "records": records,
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=False)

    # ---- 摘要打印 (供台账/报告摘录) ----
    print(f"commit F = {args.commit}")
    print(f"C size = {len(C)} (changes_raw={c_stats['changes_dir_count_raw']}, "
          f"archive_raw={c_stats['archive_dir_count_raw']}, union_before_dedupe={c_stats['union_before_dedupe']})")
    print(f"top-level .aria/audit-reports/*.md count = {len(files)}")
    print(f"top-level subdirs excluded (not recursed) = {sorted(trees)}")

    bucket_counts = defaultdict(int)
    for r in records:
        bucket_counts[r["bucket"]] += 1
    print("bucket counts:", dict(sorted(bucket_counts.items())))

    return result


if __name__ == "__main__":
    main()
```

### 2.2 `select_samples.py` — 六族确定性选样 + 争议归类

```python
#!/usr/bin/env python3
"""select_samples.py — TASK-002 六族样本确定性选取 + 争议归类 (qa-corpus-A)

输入: freeze_corpus.py --json 产出的分类结果。
输出: 六族最终样本 (F-a..F-f) + (b1)/(b2) 争议分组统计, 全部确定性 (sorted 后取前 K)。

选取规则 (逐条对应 proposal Tasks B.0 / SC-2):
  F-a/F-b: 不做自由选取, 钉死同一 id `state-scanner-inter-cycle-surfacing` 的全部
           matched 记录 (该 id 由 corpus-freeze.md 正文的实测过程钉定, 不是本脚本的
           搜索结果 —— 本脚本只做双列核验, 不重新搜索候选 id)。
  F-c/F-d: 候选池 = matched 记录里 shape 标记为真的集合; 按文件名 sorted() 升序扫描,
           跳过 (b1) 不一致的 (记入『跳过争议』), 取前 3 个一致的作为样本。
  F-e:     legacy_shaped 全量 (本仓当前实测 6 份, 全数收录, 不做取舍)。
  F-f:     先对 unattributed_shaped 全量做 (b2) 独立源回查, 归一化值 ∈ C 的整份移入
           争议表 (不进 F-f 样本池); 剩余池按文件名 sorted() 取前 3。

用法:
    python3 -B select_samples.py classify_F.json
"""
import json
import sys
from collections import defaultdict

PINNED_SAME_ID = "state-scanner-inter-cycle-surfacing"


def consistent(r):
    if not r.get("final_matches"):
        return False
    cid = r["final_matches"][0]
    return r["col1_status"] == "ok" and r["col1_normalized"] == cid


def shape_flags(r):
    tails = [s["shape_tail"] for s in r["shapes"]]
    roles = [s["shape_role_suffix"] for s in r["shapes"]]
    aggs = [s["shape_aggregated"] for s in r["shapes"]]
    norounds = [s["shape_no_round_marker"] for s in r["shapes"]]
    return any(tails), any(roles), any(aggs), any(norounds)


def first_k_consistent(pool, k):
    """候选池按文件名升序扫描, 一致的计入样本 (至多 k 个), 期间遇到的不一致候选记入
    『跳过争议』(用于争议表); 一旦样本凑满 k 个即停止扫描 (故只记录凑够之前跳过的那些,
    不做全量普查 —— 全量普查另由 main() 里『全量 matched (b1) 统计』一次性给出)。"""
    chosen, skipped = [], []
    for r in sorted(pool, key=lambda r: r["file"]):
        if len(chosen) >= k:
            break
        if consistent(r):
            chosen.append(r)
        else:
            skipped.append(r)
    return chosen, skipped


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    recs = d["records"]
    C_size = d["C_size"]

    matched = [r for r in recs if r["bucket"] == "matched"]
    legacy = [r for r in recs if r["bucket"] == "legacy_shaped"]
    unattr = [r for r in recs if r["bucket"] == "unattributed_shaped"]

    print(f"commit = {d['commit']}  C_size = {C_size}  top_level_md = {d['top_level_md_count']}")
    print()

    # ---- F-a / F-b: 钉死同 id ----
    pinned = [r for r in matched if PINNED_SAME_ID in r["final_matches"]]
    fa = [r for r in pinned if any(s["shape_tail"] for s in r["shapes"])]
    fb = [r for r in pinned if any(s["shape_role_suffix"] for s in r["shapes"])]
    print(f"=== F-a (末段, id={PINNED_SAME_ID}) n={len(fa)} (下界 2) ===")
    for r in sorted(fa, key=lambda x: x["file"]):
        print(f"  {r['file']} | col1={r['col1_source']}={r['col1_normalized']!r} | consistent={consistent(r)}")
    print(f"=== F-b (role 后缀, id={PINNED_SAME_ID}) n={len(fb)} (下界 3) ===")
    for r in sorted(fb, key=lambda x: x["file"]):
        print(f"  {r['file']} | col1={r['col1_source']}={r['col1_normalized']!r} | consistent={consistent(r)}")
    print()

    # ---- F-c: aggregated ----
    agg_pool = [r for r in matched if shape_flags(r)[2]]
    fc, fc_skipped = first_k_consistent(agg_pool, 3)
    print(f"=== F-c (aggregated) pool={len(agg_pool)} chosen={len(fc)} (下界 3) ===")
    for r in fc:
        print(f"  {r['file']} | id={r['final_matches'][0]} | col1={r['col1_source']}={r['col1_normalized']!r}")
    print(f"  跳过的 (b1) 不一致候选: {len(fc_skipped)}")
    for r in fc_skipped:
        print(f"   DISPUTE {r['file']} | id={r['final_matches'][0]} | col1_status={r['col1_status']}")
    print()

    # ---- F-d: no round marker ----
    nr_pool = [r for r in matched if shape_flags(r)[3]]
    fd, fd_skipped = first_k_consistent(nr_pool, 3)
    print(f"=== F-d (无 -R\\d+- 族) pool={len(nr_pool)} chosen={len(fd)} (下界 3) ===")
    for r in fd:
        print(f"  {r['file']} | id={r['final_matches'][0]} | col1={r['col1_source']}={r['col1_normalized']!r}")
    print(f"  跳过的 (b1) 不一致候选: {len(fd_skipped)}")
    for r in fd_skipped:
        print(f"   DISPUTE {r['file']} | id={r['final_matches'][0]} | col1_status={r['col1_status']}")
    print()

    # ---- F-e: legacy 全量 ----
    print(f"=== F-e (真 2-field legacy) 全量 n={len(legacy)} (下界 3) ===")
    for r in sorted(legacy, key=lambda x: x["file"]):
        note = ""
        if r["col1_status"] == "ok":
            note = f"  [(b2) 记名: 独立源归一化值={r['col1_normalized']!r}]"
        print(f"  {r['file']} | col1_status={r['col1_status']}{note}")
    print()

    # ---- F-f: unattributed, 先做 (b2) 回查 ----
    # 需要 C 的实际集合才能判『归一化值 ∈ C』——这里用 matched 记录反推 C 不可靠(只含被
    # 命中的部分), 因此 select_samples.py 要求调用方已经在 freeze_corpus.py 阶段做好
    # 判断; 本脚本改为直接信任 freeze_corpus.py 输出里尚未提供的 in_C 标记时, 退化为
    # 用一个轻量二次 git 调用重建 C (与 freeze_corpus.compute_C 等价)。
    import subprocess
    import re

    def run_git(args, repo_root):
        r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=repo_root)
        return r.stdout

    repo_root = sys.argv[2] if len(sys.argv) > 2 else "."
    commit = d["commit"]
    changes = run_git(["ls-tree", "--name-only", "-d", commit, "--", "openspec/changes/"], repo_root)
    archive = run_git(["ls-tree", "--name-only", "-d", commit, "--", "openspec/archive/"], repo_root)
    changes_names = [l.rsplit("/", 1)[-1] for l in changes.splitlines() if l.strip()]
    archive_names = [re.sub(r"^\d{4}-\d{2}-\d{2}-", "", l.rsplit("/", 1)[-1]) for l in archive.splitlines() if l.strip()]
    C = set(changes_names) | set(archive_names)
    assert len(C) == C_size, f"C 重建大小不符: {len(C)} != {C_size}"

    reclass = [r for r in unattr if r["col1_status"] == "ok" and r["col1_normalized"] in C]
    genuine = [r for r in unattr if not (r["col1_status"] == "ok" and r["col1_normalized"] in C)]
    print(f"=== F-f (unattributed) 候选池={len(unattr)}  (b2) 回查改归={len(reclass)}  genuine 余={len(genuine)} ===")
    by_id = defaultdict(list)
    for r in reclass:
        by_id[r["col1_normalized"]].append(r["file"])
    print("  (b2) 改归分组 (按独立源归一化 id):")
    for cid, files in sorted(by_id.items(), key=lambda x: -len(x[1])):
        print(f"    {cid} : {len(files)} 份 (如 {files[0]})")
    ff = sorted(genuine, key=lambda x: x["file"])[:3]
    print(f"  F-f 最终样本 (genuine 池按文件名 sorted 取前 3, 下界 3):")
    for r in ff:
        print(f"    {r['file']} | col1_status={r['col1_status']}")
    print()

    # ---- 全量 matched (b1) 统计 (信息性, 供争议表汇总) ----
    incons = [r for r in matched if not consistent(r)]
    missing = [r for r in incons if r["col1_status"] != "ok"]
    mismatch = [r for r in incons if r["col1_status"] == "ok" and r["col1_normalized"] != r["final_matches"][0]]
    print(f"=== 全量 matched (b1) 统计 (信息性, 非样本池): total={len(matched)} consistent={len(matched)-len(incons)} "
          f"inconsistent={len(incons)} (missing={len(missing)} mismatch={len(mismatch)}) ===")
    by_pair = defaultdict(list)
    for r in mismatch:
        by_pair[(r["final_matches"][0], r["col1_normalized"])].append(r["file"])
    for (cid, norm), files in sorted(by_pair.items(), key=lambda x: -len(x[1])):
        print(f"  mismatch name={cid!r} col1_norm={norm!r} : {len(files)} 份 (如 {files[0]})")


if __name__ == "__main__":
    main()
```

### 2.3 运行命令

```bash
cd /home/dev/Aria
python3 -B freeze_corpus.py 8d2ff8b1ce1dada8ef70729f136739db60f42a4b \
    --repo-root /home/dev/Aria --json classify_F.json
python3 -B select_samples.py classify_F.json /home/dev/Aria
```

两条命令均退出 0。`classify_F.json` 的 sha256 (供另一实例复现后逐字节比对, 非唯一判据,
见第 6 章): `8e7db8fb2f26afbc64bc7d3cf841159d5388928204abd8b5dd0f1a38592a65cd`。

---

## 3. 六族标注结果 (SC-2 / SC-4 期望值来源)

标注列约定: **标注结果** = 若两列一致, 即该 change_id (F-a~F-d) 或桶名 `legacy` /
`unattributed` (F-e/F-f); 这一列是 TASK-004 断言里 `matched` / `excluded_legacy_count` /
`unattributed_count` / `unattributed` 列表的字面来源。

### 3.1 F-a (末段族, proposal `:458` 「末段族 `…-{id}.md` 无 role 段」) + F-b (role 后缀族)

**同一 id 钉死** (proposal `:426` 「同 id 双族候选」+ TASK-002 verification 第 2 条): id =
`state-scanner-inter-cycle-surfacing`。下界 F-a ≥ 2、F-b ≥ 3, 本仓在 F 上实测**恰好** 2 与 3
(与该 id 在 `.aria/audit-reports/` 里的全部记录数相等, 不是从更大候选池里挑出来的子集)。

| 文件 (blob sha) | 族 | 第一列来源 = 原始值 | 第一列归一化 | 第二列(名匹配) | 两列一致 | 标注结果 |
|---|---|---|---|---|---|---|
| `post_spec-R1-2026-05-08-state-scanner-inter-cycle-surfacing.md`<br>`d013e3426cfbc3aff449ea8bff649f4e72dfd854` | F-a | `change_id: state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` (末段) | 是 | `state-scanner-inter-cycle-surfacing` |
| `post_spec-R2-2026-05-08-state-scanner-inter-cycle-surfacing.md`<br>`724fd68dd0d74e4887df66c208d179db1fb50aa9` | F-a | `change_id: state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` (末段) | 是 | `state-scanner-inter-cycle-surfacing` |
| `pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md`<br>`54ed9e5c40cf07324a4106c1b8ae5e01c61cb288` | F-b | `context: state-scanner-inter-cycle-surfacing sub-PR (a) — TX.0 + TX.1 prerequisite` | `state-scanner-inter-cycle-surfacing` (第一空白 token) | `state-scanner-inter-cycle-surfacing` (中缀 `-id-sub-pr-a`) | 是 | `state-scanner-inter-cycle-surfacing` |
| `pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md`<br>`e8b3d2be8efaee156f665ab772851186bb2eec66` | F-b | `context: state-scanner-inter-cycle-surfacing sub-PR (c) — TX.2 + TX.3 + TX.4 + TX.6 + TX.7 cleanup` | `state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` | 是 | `state-scanner-inter-cycle-surfacing` |
| `pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md`<br>`863710aa822c2c1dcef6a06c8e4a6e4628099942` | F-b | `context: state-scanner-inter-cycle-surfacing sub-PR (b) — G2 + G3 + G4 collectors + 2 recommendation rules` | `state-scanner-inter-cycle-surfacing` | `state-scanner-inter-cycle-surfacing` | 是 | `state-scanner-inter-cycle-surfacing` |

> **F-b 三份的可用性见文末 owner 裁定一节**(标题「owner 2026-09-30 裁定: F-b 按 SC-2 规则 (c) 降下界」)。

**下界核验**: F-a = 2 (满足 ≥2) / F-b = 3 (满足 ≥3)。**5/5 双列一致**, 零剔除, 无需换 id
重采、无需降下界。

反事实自查 (对照 proposal `:458` 给出的两条反事实, 不改任何断言, 只确认本样本能暴露它们):
若把规则 2 退回纯中缀 `-{id}-` (删掉末段 `stem.endswith` 分支), 上表两份 F-a
(`post_spec-R1`/`R2`) 的文件名 `…-state-scanner-inter-cycle-surfacing.md` 结尾没有第二个
`-`, 纯中缀规则会判它们**不命中任何 id** ⇒ 从 `matched` 漏成 `unattributed`, 会拉低
`matched` 计数、拉高 `unattributed_count` ⇒ 该反事实在本样本上确实会变红, 样本有区分力。

### 3.2 F-c (aggregated / aggregate 族)

候选池 (`matched` 里文件名含 `-aggregated`/`-aggregate` 的): **136** 份。选取规则: 按文件名
`sorted()` 升序扫描, 跳过 (b1) 两列不一致的, 取前 3 个一致的 (本族扫描 0 次跳过, 全部见
4.1)。

| 文件 (blob sha) | 归属 id (名匹配) | 第一列来源 = 原始值 | 第一列归一化 | 两列一致 | 标注结果 |
|---|---|---|---|---|---|
| `post_planning-FINAL-1783300200007-runtime-probe-archive-gate-integration-aggregated.md`<br>`24f4d8f04425ff6673e12cf0ee0d221aeedf50a1` | `runtime-probe-archive-gate-integration` | `context: openspec/changes/runtime-probe-archive-gate-integration/detailed-tasks.yaml` | `runtime-probe-archive-gate-integration` (走 `^openspec/changes/` 捕获组分支) | 是 | `runtime-probe-archive-gate-integration` |
| `post_planning-R1-1785010000000-phase-c-integrator-ci-path-coverage-aggregated.md`<br>`a08fc7edccf9f3231e5daded1aa775eba9eb4852` | `phase-c-integrator-ci-path-coverage` | `context: phase-c-integrator-ci-path-coverage` | `phase-c-integrator-ci-path-coverage` (走首 token 分支, 值本身无路径前缀) | 是 | `phase-c-integrator-ci-path-coverage` |
| `post_planning-R1-1786280000000-premerge-gate-mainbranch-failclosed-aggregate.md`<br>`67c344f8a8362e5bce426c19698676ab8d3554b1` | `premerge-gate-mainbranch-failclosed` | `context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml` | `premerge-gate-mainbranch-failclosed` (`^openspec/changes/` 分支) | 是 | `premerge-gate-mainbranch-failclosed` |

**下界核验**: 3 (满足 ≥3)。三份分别落在归一化算法的两条不同分支 (`^openspec/changes/…`
捕获组 与 首 token 回退) 且第三份文件名用的是 `-aggregate` (无 `d`) 而非 `-aggregated`,
两种拼法都在样本里覆盖到。

### 3.3 F-d (无 `-R\d+-` 族: `CONVERGED` / `FINAL` / `R5.5` / `R1prime` / `usN-mN` / `A1-` 席位前缀)

候选池 (`matched` 里整串文件名不含 `-R\d+-` 形态的): **17** 份。同样按 `sorted()` 升序扫描
跳过不一致的; 本族扫描时跳过了 3 个 (见 4.1), 第 4 个起才凑满 3 个一致样本。

| 文件 (blob sha) | 归属 id (名匹配) | 位置标记 | 第一列来源 = 原始值 | 第一列归一化 | 两列一致 | 标注结果 |
|---|---|---|---|---|---|---|
| `post_planning-FINAL-1783300200007-runtime-probe-archive-gate-integration-aggregated.md`<br>`24f4d8f04425ff6673e12cf0ee0d221aeedf50a1` | `runtime-probe-archive-gate-integration` | `FINAL` | `context: openspec/changes/runtime-probe-archive-gate-integration/detailed-tasks.yaml` | `runtime-probe-archive-gate-integration` | 是 | `runtime-probe-archive-gate-integration` |
| `post_spec-FINAL-1783275800006-runtime-probe-archive-gate-integration-aggregated.md`<br>`3dc001b6ef76932d968a87f5b0b5997ec06cfd1e` | `runtime-probe-archive-gate-integration` | `FINAL` | `context: openspec/changes/runtime-probe-archive-gate-integration/proposal.md` | `runtime-probe-archive-gate-integration` | 是 | `runtime-probe-archive-gate-integration` |
| `post_spec-R1R2-2026-06-04-state-scanner-git-operation-awareness.md`<br>`02dc56b2c5471dfe6de0289fda75597a02a8e1ee` | `state-scanner-git-operation-awareness` | `R1R2` (合并轮标记, 不匹配 `-R\d+-`: `R1` 后紧跟字母 `R` 而非连字符) | `spec_id: state-scanner-git-operation-awareness` | `state-scanner-git-operation-awareness` | 是 | `state-scanner-git-operation-awareness` |

**下界核验**: 3 (满足 ≥3)。位置标记覆盖了 proposal 举例清单里的 `FINAL` 与一个清单外但
同样符合定义的真实变体 `R1R2` (合并轮次标记, 正则 `-R\d+-` 要求数字后紧跟连字符, `R1R2`
里 `R1` 后是字母 `R` 不是连字符, 结构上确实不匹配, 与 `CONVERGED`/`R5.5`/`R1prime`/
`usN-mN`/`A1-` 同属「不解析成 `-R\d+-` 但仍应正确归属」的验证目的)。跳过的 3 个候选见
4.1, 均因第一列『取不到』被剔, 不是因为它们不是无-round-marker 形态。

> **与 3.2 的重叠说明 (非错误)**: 本表第 1 行 `post_planning-FINAL-…-aggregated.md` 与
> 3.2 表第 1 行是同一份文件。proposal `:458` 只要求六族各自独立满足下界, 未要求六族样本
> 两两不相交 (F-a/F-b 之外的四族之间没有互斥关系), 该文件同时是「aggregated 族」与
> 「无 round marker 族」的真实例证, 两族各自的选取规则 (2.2 节 `first_k_consistent`) 独立
> 运行, 出现同一份文件落进两个族的结果表, 是候选池天然重叠 + 确定性排序取前 3 的直接
> 后果, 不是手工去重疏漏。

### 3.4 F-e (真 2-field legacy 族)

判据: `f` 匹配 `^{checkpoint}-[0-9TZ:.\-]+\.md$`
(`checkpoint` ∈ 8 个规范值, 见 `aria/skills/config-loader/DEFAULTS.json` 的
`audit.checkpoints` 键集: `post_brainstorm`/`post_spec`/`post_planning`/
`mid_implementation`/`mid_post_spec`/`post_implementation`/`pre_merge`/`post_closure`)
且不含任何 `C` 中 id (proposal `:205`)。本仓在 F 上**全量实测 6 份**, 高于下界 3, **全数
收录**不做取舍 (总体本来就小, 抽样无意义):

| 文件 (blob sha) | 第一列状态 | (b2) 记名 |
|---|---|---|
| `post_planning-2026-04-11T0530Z.md`<br>`d6190921c9eb5258b56daa2d8e0937e224ed6415` | missing (三键皆缺) | — |
| `post_spec-2026-04-01T23.md`<br>`d26f66f1e23315d2a905b4aded48988e07e9101b` | ok, `context: openspec/changes/auto-audit-system/proposal.md` → 归一化 `auto-audit-system` | **`auto-audit-system` ∈ C** — 按 (b2), F-e 按文件名形态分桶, 与独立源指向哪个 change 正交, **仍算 F-e**, 此处只作记名, 不改归、不剔除 |
| `post_spec-2026-04-09T1240Z.md`<br>`e617cce93f4db64e0dd799e645d048ce847daa44` | missing | — |
| `post_spec-2026-04-09T1315Z.md`<br>`4e6efc4af36a41e3d226197afe1d6f945b0d6a09` | missing | — |
| `post_spec-2026-04-12T0400Z.md`<br>`2cdf43ab1ca70219f7e1b3f38c0d4f3426a9a5ef` | missing | — |
| `post_spec-2026-04-12T0800Z.md`<br>`29ba318f9152ff146a8ed120879cd197b7f14973` | missing | — |

标注结果: **6 份全部 = `legacy`**, 成员集互不相交于 `matched` 与 `unattributed` (由构造
保证: legacy 判据要求 `rest` 只含 `[0-9TZ:.\-]`, 任何真实 change_id 必含小写字母, 结构上
不可能同时满足 legacy 形态与 rule2 命中)。

**下界核验**: 6 (满足 ≥3)。

### 3.5 F-f (unattributed 族)

候选池 (`unattributed_shaped`, 名匹配对任何 `c ∈ C` 都不命中且非 legacy 形态): **170** 份,
与 proposal `:206` 记的历史观测值「170」**巧合相等** (语料在两次快照之间于此桶净变化为
0, 不代表桶内文件完全相同, 见第 7 章)。

按 (b2) 先做独立源回查: **105** 份的独立源字段归一化值落在 `C` 内 ⇒ 整份移入争议表 (4.2),
**不**进 F-f 样本池; 余下 **65** 份 (`genuine`) 才是真正候选池。按文件名 `sorted()` 取前 3:

| 文件 (blob sha) | 第一列状态 | (b2) 回查结果 | 标注结果 |
|---|---|---|---|
| `post_planning-R2-CONVERGED-dispatch-input-delivery.md`<br>`c4c537ca6eef7492e066f14b3945c1c3bf3a03f4` | missing (三键皆缺) | 无独立源可回查, 保留 F-f | `unattributed` |
| `post_spec-R1-1785112156889-phase-c-gate-path-coverage-backend-architect.md`<br>`20ba5ea12e2548becc75d25832699ccefd731aa6` | missing | 无独立源可回查, 保留 F-f | `unattributed` |
| `post_spec-R1-1785112156889-phase-c-gate-path-coverage-code-reviewer.md`<br>`0b626fa7eefcf00ee90e51039a51f51679ed535c` | missing | 无独立源可回查, 保留 F-f | `unattributed` |

**下界核验**: 3 (满足 ≥3, genuine 池余量 65, 远高于下界)。

---

## 4. 机械仲裁与争议表

### 4.1 (b1) 抽样过程中实际剔除的候选 (F-c/F-d 选样时遇到的不一致者)

F-c 扫描 0 次跳过。F-d 扫描时按文件名升序遇到并剔除以下 3 个 (均在 4 个考察对象之列,
且在这 3 个被剔除之后的下一个即第 3.3 节表格里的第 3 行):

| 文件 | 归属 id (名匹配) | 第一列取值 | 剔除理由 |
|---|---|---|---|
| `mid_implementation-2026-04-23T2130Z-state-scanner-mechanical.md`<br>`2b322def68db1c7ca656920f29188184410a82e3` | `state-scanner-mechanical` | 取不到 (frontmatter 只有 `spec: state-scanner-mechanical-enforcement`; 键名是 `spec` 不是 `spec_id`, 三键白名单 `change_id`/`spec_id`/`context` 均未命中) | 第一列取不到 ⇒ 按 (b1) 剔出 |
| `post_spec-2026-04-23T2058Z-state-scanner-mechanical.md`<br>`f4bdb95859fe4cecb84c2af64887e75026e7789d` | `state-scanner-mechanical` | 取不到 (同上, 键名同样是 `spec` 非 `spec_id`) | 第一列取不到 ⇒ 按 (b1) 剔出 |
| `post_spec-FINAL-1783602519132-aria-2.0-m6-cost-model-telemetry-aggregated.md`<br>`1a61ae4528f9bc541ffb32aa41fc7c0ac45d255e` | `aria-2.0-m6-cost-model-telemetry` | 取不到 (该文件**没有** `---`/`---` frontmatter 块, 正文直接以 `# post_spec FINAL …` 标题开头) | 第一列取不到 ⇒ 按 (b1) 剔出 |

前两条是同一类真实边界: 报告作者写的字段名是 `spec:` (历史命名), 不是算法白名单里的
`spec_id:`, 机械算法**不做同义改写**, 按字面判「三者皆缺」直接判取不到 —— 这不是本脚本
的 bug, 是「无裁量」机械仲裁按设计应有的行为 (一个更「聪明」会把 `spec:` 当 `spec_id:`
读的实现, 反而是在替标注引入裁量)。

### 4.2 (b2) F-f → F-a~F-d 改归后按 (b1) 剔出 (105 份, 按独立源归一化 id 分组)

这批文件的文件名对 `C` 中任何 id 都不命中 (故先落 `unattributed_shaped`), 但其独立源
字段 (`context:` 为主) 归一化后指向一个**确实在 `C` 内**的 id —— 按 Tasks B.0 (b2):
「若某份 F-f 候选的独立源字段归一化值 ∈ C ⇒ 它的正确归属其实是那个 change_id ⇒ 改归
F-a~F-d 并按 (b1) 处理」。改归后两列 (第一列 = 该 id; 第二列 = 名匹配, 结构上必为空,
因为它们本就是因为名匹配空才落进 F-f 候选池的) 必然不一致 ⇒ 逐份剔出, 不进任何族样本池。

| 改归目标 id | 份数 | 示例文件 |
|---|---|---|
| `agent-router-auto-project-agent-injection` | 41 | `post_planning-R1-1783560677747-agent-router-injection-backend-architect.md` |
| `a1-entry-claim-duplicate-work-guard` | 29 | `post_planning-R1-1788102593777-a1-entry-combined-A1-tech-lead.md` |
| `aria-2.0-m6-dispatch-input-delivery` | 16 | `post_spec-CONVERGED-1783055160721-dispatch-input-delivery-summary.md` |
| `aria-2.0-m4-human-gate-feishu-approval` | 7 | `post_spec-R1-2026-05-07T1811Z-us024-m4.md` |
| `aria-2.0-m3-cycle-close-glm-routing-recovery` | 5 | `post_spec-2026-05-04T103702Z-us023-m3.md` |
| `aria-archive-gate-runtime-reality` | 2 | `post_planning-R4-CONVERGED-archive-gate-runtime-reality.md` |
| `aria-2.0-m5-replay-reconciler-drift-review-loop-audit` | 2 | `post_spec-R1-2026-05-10T1506Z-aria-2.0-m5.md` |
| `aria-2.0-m6-e2e-resilience` | 2 | `pre_merge-R2-1782748609419-m6-b4-issue-type-hint-convergence.md` |
| `aria-2.0-m2-layer1-state-machine` | 1 | `post_spec-2026-04-28T1700Z-us022-m2-layer1.md` |
| **合计** | **105** | 9 个不同 id |

完整 105 份文件名清单 (9 组, 每组内按文件名排序):

<details>
<summary>展开完整清单 (Phase D「写侧命名约定无强制」issue 的实证材料)</summary>

```
### agent-router-auto-project-agent-injection (41 份)
post_planning-R1-1783560677747-agent-router-injection-backend-architect.md
post_planning-R1-1783560677747-agent-router-injection-code-reviewer.md
post_planning-R1-1783560677747-agent-router-injection-knowledge-manager.md
post_planning-R1-1783560677747-agent-router-injection-qa-engineer.md
post_planning-R1-1783560677747-agent-router-injection-tech-lead.md
post_planning-R2-1783563475800-agent-router-injection-backend-architect.md
post_planning-R2-1783563475800-agent-router-injection-code-reviewer.md
post_planning-R2-1783563475800-agent-router-injection-qa-engineer.md
post_planning-R2-1783563475800-agent-router-injection-tech-lead.md
post_planning-R3-1783565523840-agent-router-injection-backend-architect.md
post_planning-R3-1783565523840-agent-router-injection-code-reviewer.md
post_planning-R3-1783565523840-agent-router-injection-knowledge-manager.md
post_planning-R3-1783565523840-agent-router-injection-qa-engineer.md
post_planning-R3-1783565523840-agent-router-injection-tech-lead.md
post_planning-R4-1783565997093-agent-router-injection-backend-architect.md
post_planning-R4-1783565997093-agent-router-injection-code-reviewer.md
post_planning-R4-1783565997093-agent-router-injection-knowledge-manager.md
post_planning-R4-1783565997093-agent-router-injection-qa-engineer.md
post_planning-R4-1783565997093-agent-router-injection-tech-lead.md
post_planning-R4-CONVERGED-agent-router-auto-injection.md
post_spec-R1-1783541662234-agent-router-injection-backend-architect.md
post_spec-R1-1783541662234-agent-router-injection-code-reviewer.md
post_spec-R1-1783541662234-agent-router-injection-knowledge-manager.md
post_spec-R1-1783541662234-agent-router-injection-qa-engineer.md
post_spec-R1-1783541662234-agent-router-injection-tech-lead.md
post_spec-R2-1783545343184-agent-router-injection-backend-architect.md
post_spec-R2-1783545343184-agent-router-injection-code-reviewer.md
post_spec-R2-1783545343184-agent-router-injection-knowledge-manager.md
post_spec-R2-1783545343184-agent-router-injection-qa-engineer.md
post_spec-R2-1783545343184-agent-router-injection-tech-lead.md
post_spec-R3-1783548952591-agent-router-injection-backend-architect.md
post_spec-R3-1783548952591-agent-router-injection-code-reviewer.md
post_spec-R3-1783548952591-agent-router-injection-knowledge-manager.md
post_spec-R3-1783548952591-agent-router-injection-qa-engineer.md
post_spec-R3-1783548952591-agent-router-injection-tech-lead.md
post_spec-R4-1783553248742-agent-router-injection-backend-architect.md
post_spec-R4-1783553248742-agent-router-injection-code-reviewer.md
post_spec-R4-1783553248742-agent-router-injection-knowledge-manager.md
post_spec-R4-1783553248742-agent-router-injection-qa-engineer.md
post_spec-R4-1783553248742-agent-router-injection-tech-lead.md
post_spec-R4-ACCEPTED-agent-router-auto-injection.md

### a1-entry-claim-duplicate-work-guard (29 份)
post_planning-R1-1788102593777-a1-entry-combined-A1-tech-lead.md
post_planning-R1-1788102593777-a1-entry-combined-A2-backend-architect.md
post_planning-R1-1788102593777-a1-entry-combined-A3-qa-engineer.md
post_planning-R1-1788102593777-a1-entry-combined-A4-code-reviewer.md
post_planning-R1-1788102593777-a1-entry-combined-A5-knowledge-manager.md
post_planning-R1-1788102593777-a1-entry-combined-aggregated.md
post_planning-R2-1788105806616-a1-entry-combined-A1-tech-lead.md
post_planning-R2-1788105806616-a1-entry-combined-A2-backend-architect.md
post_planning-R2-1788105806616-a1-entry-combined-A3-qa-engineer.md
post_planning-R2-1788105806616-a1-entry-combined-A4-code-reviewer.md
post_planning-R2-1788105806616-a1-entry-combined-A5-knowledge-manager.md
post_planning-R2-1788105806616-a1-entry-combined-aggregated.md
post_planning-R3-1788108293825-a1-entry-combined-A1-tech-lead.md
post_planning-R3-1788108293825-a1-entry-combined-A2-backend-architect.md
post_planning-R3-1788108293825-a1-entry-combined-A3-qa-engineer.md
post_planning-R3-1788108293825-a1-entry-combined-A4-code-reviewer.md
post_planning-R3-1788108293825-a1-entry-combined-A5-knowledge-manager.md
post_planning-R3-1788108293825-a1-entry-combined-aggregated.md
post_planning-R4-1788184755899-a1-entry-combined-A1-tech-lead.md
post_planning-R4-1788184755899-a1-entry-combined-A2-backend-architect.md
post_planning-R4-1788184755899-a1-entry-combined-A3-qa-engineer.md
post_planning-R4-1788184755899-a1-entry-combined-A4-code-reviewer.md
post_planning-R4-1788184755899-a1-entry-combined-A5-knowledge-manager.md
post_planning-R4-1788184755899-a1-entry-combined-aggregated.md
post_spec-R2-1787481000000-a1-entry-claim-rewrite-backend-architect.md
post_spec-R2-1787481000000-a1-entry-claim-rewrite-code-reviewer.md
post_spec-R2-1787481000000-a1-entry-claim-rewrite-knowledge-manager.md
post_spec-R2-1787481000000-a1-entry-claim-rewrite-qa-engineer.md
post_spec-R2-1787481000000-a1-entry-claim-rewrite-tech-lead.md

### aria-2.0-m6-dispatch-input-delivery (16 份)
post_spec-CONVERGED-1783055160721-dispatch-input-delivery-summary.md
post_spec-R1-1783053088003-dispatch-input-delivery-backend-architect.md
post_spec-R1-1783053088003-dispatch-input-delivery-code-reviewer.md
post_spec-R1-1783053088003-dispatch-input-delivery-knowledge-manager.md
post_spec-R1-1783053088003-dispatch-input-delivery-qa-engineer.md
post_spec-R1-1783053088003-dispatch-input-delivery-tech-lead.md
post_spec-R2-1783054040265-dispatch-input-delivery-backend-architect.md
post_spec-R2-1783054040265-dispatch-input-delivery-code-reviewer.md
post_spec-R2-1783054040265-dispatch-input-delivery-knowledge-manager.md
post_spec-R2-1783054040265-dispatch-input-delivery-qa-engineer.md
post_spec-R2-1783054040265-dispatch-input-delivery-tech-lead.md
post_spec-R3-1783055160721-dispatch-input-delivery-backend-architect.md
post_spec-R3-1783055160721-dispatch-input-delivery-code-reviewer.md
post_spec-R3-1783055160721-dispatch-input-delivery-knowledge-manager.md
post_spec-R3-1783055160721-dispatch-input-delivery-qa-engineer.md
post_spec-R3-1783055160721-dispatch-input-delivery-tech-lead.md

### aria-2.0-m4-human-gate-feishu-approval (7 份)
post_spec-R1-2026-05-07T1811Z-us024-m4.md
post_spec-R2-2026-05-07T1845Z-us024-m4.md
pre_merge-R1-2026-05-09T0642Z-us024-m4.md
pre_merge-R2-2026-05-09T0735Z-us024-m4.md
pre_merge-R3-2026-05-09T0750Z-us024-m4.md
pre_merge-R4-2026-05-09T0820Z-us024-m4.md
pre_merge-R5-2026-05-09T0840Z-us024-m4.md

### aria-2.0-m3-cycle-close-glm-routing-recovery (5 份)
post_spec-2026-05-04T103702Z-us023-m3.md
post_spec-r2-2026-05-04T1130Z-us023-m3.md
pre_merge-R1-2026-05-06T1626Z-us023-m3.md
pre_merge-R2-2026-05-06T1652Z-us023-m3.md
pre_merge-R3-2026-05-06T1700Z-us023-m3.md

### aria-archive-gate-runtime-reality (2 份)
post_planning-R4-CONVERGED-archive-gate-runtime-reality.md
post_spec-R5-CONVERGED-archive-gate-runtime-reality.md

### aria-2.0-m5-replay-reconciler-drift-review-loop-audit (2 份)
post_spec-R1-2026-05-10T1506Z-aria-2.0-m5.md
post_spec-R2-2026-05-12T2351Z-aria-2.0-m5.md

### aria-2.0-m6-e2e-resilience (2 份)
pre_merge-R2-1782748609419-m6-b4-issue-type-hint-convergence.md
pre_merge-R3-1782648957294-m6-ac6-146-convergence.md

### aria-2.0-m2-layer1-state-machine (1 份)
post_spec-2026-04-28T1700Z-us022-m2-layer1.md
```

</details>

层次分解 (与 proposal `:423` 记的历史分层实测同构, 数字按 F 重算): 170 份 F-f 候选池 =
**105** 份 (b2) 改归 (本表, 计入争议表) + **64** 份第一列彻底无字段 (留在 genuine 池) +
**1** 份第一列有字段但归一化值不在 `C` (同样留在 genuine 池, 不算争议, 见下作为附注)。

> **附注 (非争议, 不计入 4.4 统计)**: genuine 池里那 **1** 份『有字段但不在 C』的样本,
> 与 proposal `:423` 描述的「散文噪声」同一份文件 (本次在 F 上重新定位): 文件
> `post_spec-R3-1787652625000-a1-entry-rework-v3-combined-code-reviewer.md` 的
> `context:` 字段值逐字只有一个 `>` 字符 (Markdown blockquote 语法残留, 非真实内容),
> 归一化后是 `>`, 不在 `C` 内。它**没有**被 (b2) 改归、**没有**被排除, 仍是合法的 F-f
> genuine 候选, 只是排序上没有落进前 3 个最终样本 (3.5 节)。列在此处仅作语料形态记录。

### 4.3 全量 `matched` (b1) 一致性统计 (信息性, 不是样本池, 供审计留痕)

对 `matched` 桶全部 800 份 (不止本文件实际抽样用到的 11 份) 做 (b1) 一致性全量普查,
供 Phase D「写侧命名约定无强制」issue 与「config-loader 无程序化入口」issue 参考, **不
作为 SC-2/SC-4 的样本来源**:

| 类别 | 份数 |
|---|---|
| 两列一致 | 583 |
| 两列不一致, 合计 | 217 |
| — 其中第一列彻底取不到 (三键皆缺或皆空) | 183 |
| — 其中第一列有值但归一化后 ≠ 名匹配 id (真·不一致) | 34 |

「真·不一致」34 份只落在 2 组 (name, 归一化值) 组合, 均为可解释的边界, 不是标注/实现
的随机噪声:

| 文件名归属 id (名匹配) | 第一列归一化值 | 份数 | 成因 |
|---|---|---|---|
| `linked-issue-field-availability` | `PR` | 25 | `context:` 原文以 `PR` 开头, 第二个空白 token 是裸写的 PR 号 (即 `10CG/Aria#190`), 第三个才是 `linked-issue-field-availability`, 其后接 `(main …)`; 三步算法第 2 步「否则取第一个空白分隔 token」只取到 `PR`, 真正的 id 是第三个 token, 机械算法按字面不往后取 (主控 2026-09-30 订正: 原写「第二个 token」, 按 F 上原文实读为第三个; 原文裸写的 PR 号按 content-integrity §4.4 改写为全限定) |
| `state-scanner-gate-yaml-datasource` | `state-scanner-gate-yaml-datasource/detailed-tasks.yaml` | 9 | `context:` 原文是裸相对路径 `state-scanner-gate-yaml-datasource/detailed-tasks.yaml`, **没有** `openspec/changes/` 前缀, 两条路径正则都不命中, 退到「第一个空白 token」= 整个字符串 (含 `/detailed-tasks.yaml` 后缀), 与裸 id 逐字不等 |

这两组连同 4.2 的 105 份、4.1 的 3 份, 共同印证 proposal `:398` 的 R-a 风险描述: 「采用方
历史 change 报告不服从写侧命名约定」——`context:` 字段的书写形态在真实语料里至少有
4 种 (裸 id / `openspec/changes/<id>/文件名` 路径 / `PR #n <id> (...)` 散文 / 裸相对路径
`<id>/文件名`), 机械三步算法只对前两种给出与文件名一致的结果。

### 4.4 争议表条数小结 (供台账摘录)

争议表分两级, 口径不同, 不合并计数:

**必要争议 (为凑够六族样本, 按 (b1)/(b2) 规则实际执行剔除的)**:

| 章节 | 行数 | 覆盖文件数 | 来源桶 |
|---|---|---|---|
| 4.1 (F-d 选样时逐份剔除) | 3 行 (个体) | 3 份 | F-d 候选池 (matched 桶) |
| 4.2 ((b2) 改归后按 (b1) 剔除) | 9 行 (按 id 分组) | 105 份 | F-f 候选池 |
| **必要争议合计** | **12 行** | **108 份** | 两个来源桶互不相交 (F-d 候选取自 `matched`, F-f 候选取自 `unattributed_shaped`, 二者定义互斥) |

**信息性附录 (不是选样过程的一部分, 供 Phase D 开 issue 取证, 不计入上面的『必要』口径)**:

| 章节 | 行数 | 覆盖文件数 |
|---|---|---|
| 4.2 附注 (genuine 池内 1 份『字段值为 `>`』) | 1 行 (个体, 未剔除) | 1 份 |
| 4.3 (`matched` 全量 (b1) 真·不一致分组) | 2 行 (按 id 分组) | 34 份 |

必要争议的 108 份已从对应候选池里剔除, **不在**任何一个最终样本表 (3.1-3.5) 里出现
(已逐份核对: 3.1-3.5 的 11 份最终样本与 4.1/4.2 的 108 份剔除对象零重叠)。信息性附录
的 35 份**未被剔除**, 其中 34 份仍留在 `matched` 桶且计入其 `excluded_legacy_count` /
`unattributed_count` 之外的正常归属, 另 1 份仍是合法的 F-f genuine 候选。

---

## 5. 与 SC-4 的关系 (澄清, 避免 TASK-004 误读)

SC-4 (proposal `:460`) 的四份语料 (`post_spec-2026-04-11T0530Z.md` /
`post_planning-2026-04-11T0530Z.md` / `post_spec-R1-2026-05-01-x.md` /
`post_planning-R2-CONVERGED-trunc-id.md`, 其中 `x`/`trunc-id` 是 proposal 正文直接给出的
占位符) 是 **proposal 正文自带的手造 hermetic fixture**, 与本仓真实 `.aria/audit-reports/`
语料**无关**——`excluded_legacy_count == 2` / `unattributed_count == 1` /
`unattributed == ['post_planning-R2-CONVERGED-trunc-id.md']` 这些期望值已是 proposal 正文
的字面量, 不需要、也不应该从本文件另行采样。

本文件对 SC-4 唯一的支撑面: 3.4/3.5/4.2/4.3 用来对 legacy 正则
`^{checkpoint}-[0-9TZ:.\-]+\.md$` 与 unattributed 判据 (§1.2 规则 2 对任何 `c∈C` 不命中)
在**真实语料**上做了独立验证, 与 SC-4 在**手造语料**上验证的是同一套规则, 两者互补,
不是同一份数据的两次使用。TASK-004 实现 SC-4 时, 若发现手造的 `x`/`trunc-id` 与本仓
真实 `C` 中某个 id 意外冲突, 应在其自建的 hermetic 目录内核实 (SC-4 的测试语料本就该
建在独立临时仓, 不落在真实 `.aria/audit-reports/`), 不在本文件处理。

---

## 6. 复现说明 (供未参与标注的另一实例核验, TASK-002 verification 第 6 条)

1. 在干净检出的主仓 (`origin/master` 或任意包含 `8d2ff8b1ce1dada8ef70729f136739db60f42a4b`
   祖先历史的 checkout) 执行第 2.3 章两条命令, `--repo-root` 换成本地路径。
2. 核对 `select_samples.py` 输出与本文件第 3/4 章逐字相同, 重点核对:
   - `C_size = 154`, `top_level_md = 987`;
   - F-a/F-b 在 id `state-scanner-inter-cycle-surfacing` 下分别为 2 与 3, 5 份文件名逐字
     与 3.1 表相同;
   - F-c/F-d 选出的 3+3 份文件名逐字与 3.2/3.3 表相同, F-d 跳过的 3 份与 4.1 相同;
   - F-e 6 份文件名逐字与 3.4 表相同 (含 `post_spec-2026-04-01T23.md` 的 (b2) 记名);
   - F-f 候选池 170 / 改归 105 / genuine 65, 选出的前 3 份与 3.5 表相同;
   - `classify_F.json` 的 sha256 与本文件 2.3 章给出的值相同 (在同一 Python/git 版本组合
     下预期逐字节相同; 若版本不同导致 JSON 序列化细节差异, 以上面列出的**语义**核对项
     为准, sha256 只作附加信号)。
3. 若任一核对项不一致, 按 proposal Tasks B.0 (b1)/(b2)/(c) 规则重新走一遍仲裁, 不得直接
   拿不一致的新结果覆盖本文件 —— 按台账流程上报主控裁定 (本文件作者无权限写台账, 见任务
   派工说明)。

---

## 7. 已知边界与历史数字对照 (纯记录, 不改动 proposal 断言)

| 指标 | 历史快照数值 (proposal 引用) | 本次 F 实测 | 说明 |
|---|---|---|---|
| `.aria/audit-reports/` 顶层 `.md` 总数 | 837 (R3 rework) → 843 → 849 (R5 rework) | **987** | 语料持续增长, proposal 多处已强调「以冻结时实测为准」, 本文件即该「冻结时实测」 |
| `\|C\|` | 152 (R1) → 153 (R5 rework) → 154 (A.2, `a563192`) | **154** | 与 A.2 数值巧合相等, 构成已变 (见 1.2 节说明) |
| F-a (末段族) 全库候选 | 62 (proposal `:458`) | **62** | 逐字相等, 交叉验证本文件判据实现与 proposal 描述一致 |
| `excluded_legacy_count` (F-e 全库) | 6 (proposal `:205`) | **6** | 逐字相等 |
| `unattributed_count` (F-f 候选全库) | 170 (proposal `:206`) | **170** | 逐字相等 (桶内构成未逐份核对是否完全相同文件, 仅总数巧合相等) |
| F-f 分层: 无字段/字段值∈C/字段值∉C | 64 / 105 / 1 (proposal `:423`, R5 rework) | **64 / 105 / 1** | 三个子数字逐一相等, 且「1」那份的具体文件与 proposal 描述的「散文噪声、`>` 开头」特征一致 (本次定位到具体文件名, 见 4.2) |
| 同 id 候选 `state-scanner-inter-cycle-surfacing` | F-a 2 / F-b 3, 5/5 带独立源字段 (proposal `:458`, R5 rework) | **F-a 2 / F-b 3, 5/5 一致** | 逐字相等 |

以上巧合相等**不是**因为本次复用了 proposal 里的数字 (本文件的取样脚本从未读 proposal
正文的数字, 只读 git 历史与文件内容) —— 是两次独立测量 (相隔约 18 天) 在会持续增长的
活体语料上, 恰好在这些具体维度上未发生净变化。凡本章列出「历史值」而本次实测不同的维度
(顶层总数 837→987 即是), 均以**本次实测**为准, 不回退去匹配历史值。

---

## 8. owner 2026-09-30 裁定: F-b 按 SC-2 规则 (c) 降下界

> **执笔**: qa-corpus-C (补记执笔人) —— 未参与第 1-2 章的取样实现 (执笔者 qa-corpus-A), 未参与
> 第 3-7 章的复现核验 (执笔者 qa-corpus-B), 未写、未读 `completeness_gate.py` 任何一行 (该脚本
> 截至本节落笔时仍未写入 `aria/` 子模块, 已用 `find` 核实)。本节**只做补记**: 3.1 表格与
> 2.1/2.2 两个脚本**一字未改**, 原标注保留作溯源, 本节是关于 F-b 样本可用性的唯一口径变更记录。
> **出处**: `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` `## 1. SC-2 的 F-b
> 样本 —— 按 SC-2 自带兜底规则 (c) 降下界` (owner 2026-09-30 裁定)。

### 8.1 事实

3.1 表格为钉死 id `state-scanner-inter-cycle-surfacing` 冻结的 3 份 F-b (role 后缀族) 样本,
文件名逐字为 (与 3.1 表格第 3-5 行完全相同, 原样抄录不改):

```text
pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md
pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md
pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md
```

三份**全部**以 `pre_merge-` 开头, 即其 `checkpoint` 字段值均为 `'pre_merge'` (8.2 第二步独立核验)。

`pre_merge` 是 `execution-modes.md` §Pre-merge **Step 3 的固定排除项**: proposal.md `:39`
(hermetic case-1 核对表) 逐字「Step 3 (`:46-52`) 的排除清单 (`pre_merge` / `post_closure` /
`mid_post_spec`) 只处理「启用但合法不产出 → 误阻」」, `:253` 再补「**Step 3 枚举 (`:46-52`)
追加一条排除: `mid_implementation`**」。这四项排除是**无条件的** —— 与 `audit.checkpoints` /
`audit.mode` 等 config 取值无关, 不经 §1.3 的 `resolved_mode` 三级优先级链求值; Step 3 在枚举
待查 checkpoint 集合这一步就把它们剔除, 该 checkpoint 上的任何报告文件因此**不会**进入
Step 4/5 的证据扫描, 结构上不出现在门的 `results` 数组, 也不计入任何下游统计口径 (`matched` /
`excluded_legacy_count` / `unattributed_count`)。这 3 份样本因此不是「归属判定判错了」, 而是
**在正确实现下, 这个 checkpoint 的证据扫描步骤本就不会对它们执行**——SC-2 若断言它们被正确
attribute 给 `state-scanner-inter-cycle-surfacing`, 在正确实现上必然拿不到对应的 `results` 条目
可比对, 断言必红。(`post_brainstorm` 经裁定 1 已确定为 Step 3 固定排除项第五项, 与前四项
(`pre_merge` / `post_closure` / `mid_post_spec` / `mid_implementation`) 同属无条件排除,
**非**待裁候选; 依据 tasks.md 读前必看第 6 条与
`.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md`
(10CG/Aria#199 表第 1 行「追加排除」)。本节的过滤与统计口径含它, 8.2 第三步按五项复算。)

### 8.2 复算 (在冻结语料 F 上独立重跑, 命令与原样输出如下)

以下全部在本节作者自己的 scratchpad 工作目录执行 (未写主仓任何文件, 只读 `git ls-tree` /
`git cat-file --batch`, 与主仓工作区无写交互):

**第一步 —— 核对本文件 §2.1/§2.2 两个已发布脚本从本文件正文提取后仍可复现** (只为确认
下面用的就是本文件自己发布、已冻结的算法, 不引入新分类逻辑; 提取用 Python 正则抓本文件
第 2 章两处 Python 代码围栏块的正文, 逐字节写盘, 与 qa-corpus-A 独立产出的同名脚本文件
`diff` 为空, 先行确认无转录误差):

```text
$ python3 -B freeze_corpus.py 8d2ff8b1ce1dada8ef70729f136739db60f42a4b \
    --repo-root /home/dev/Aria --json classify_F.json
commit F = 8d2ff8b1ce1dada8ef70729f136739db60f42a4b
C size = 154 (changes_raw=7, archive_raw=147, union_before_dedupe=154)
top-level .aria/audit-reports/*.md count = 987
top-level subdirs excluded (not recursed) = ['pr19-submodule-scan', 'wf-r1fix']
bucket counts: {'legacy_shaped': 6, 'matched': 800, 'no_checkpoint_prefix': 11, 'unattributed_shaped': 170}
                                                                      # exit 0
$ sha256sum classify_F.json
8e7db8fb2f26afbc64bc7d3cf841159d5388928204abd8b5dd0f1a38592a65cd  classify_F.json
```

sha256 与本文件 §2.3 记录值**逐字节相同** ⇒ 独立重跑可复现, `matched` 桶恰 800 份, 与 3.1-3.5
章的抽样前提一致。

**第二步 —— 核对 3.1 表格 3 份 F-b 样本的 `checkpoint` 字段实测值**(证实它们确实落
`pre_merge`, 不是别的以 `pre_merge` 打头但实际是别的 checkpoint 的形近文件名):

```text
$ python3 -B -c "
import json
d = json.load(open('classify_F.json', encoding='utf-8'))
target = {
    'pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md',
    'pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md',
    'pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md',
}
for r in d['records']:
    if r['file'] in target:
        print(r['file'], '| checkpoint=', repr(r['checkpoint']))
"
pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md | checkpoint= 'pre_merge'
pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md | checkpoint= 'pre_merge'
pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md | checkpoint= 'pre_merge'
                                                                      # exit 0
```

**第三步 —— 新写脚本 `cross_id_fa_fb_check.py`**, 对 `matched` 桶全量 800 份按「可纳入
checkpoint + 两列一致」过滤后按 id 分组, 统计同一 id 同时具有 F-a 形态 (末段, `shape_tail`)
与 F-b 形态 (role 后缀, `shape_role_suffix`) 记录的 id 数。「可纳入 checkpoint」定义为
**不在** Step 3 固定排除集合 `{pre_merge, post_closure, mid_post_spec, mid_implementation,
post_brainstorm}` 内 (五项, 见 8.1 末句); 「两列一致」与 `select_samples.py`
的 `consistent()` 逐字同定义 (`col1_status == 'ok'` 且 `col1_normalized == final_matches[0]`)。
脚本全文:

```python
#!/usr/bin/env python3
"""cross_id_fa_fb_check.py -- qa-corpus-C 独立复算脚本

用途: 回答决策单 (.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md)
「## 1. SC-2 的 F-b 样本」一节里的关键数字 --
在冻结语料 F 上, 按「可纳入 checkpoint (排除 Step 3 固定排除项) + 两列一致」过滤后,
同一 change_id 同时具有 >=1 份 F-a 形态 (末段, shape_tail=True) 与 >=1 份 F-b 形态
(role 后缀, shape_role_suffix=True) 记录的 id 有多少个。

不读、不调用 completeness_gate.py。只读 classify_F.json (本目录内, 由
freeze_corpus.py 对 F 独立重跑产出, sha256 与 corpus-freeze.md §2.3 记录值相同,
见同目录 verify_sha256.txt)。

Step 3 固定排除项 (前四项为 proposal.md 逐字依据, 第五项 post_brainstorm 经裁定 1 追加;
本脚本按此五项过滤, 见 tasks.md 读前必看第 6 条):
  - pre_merge        (execution-modes.md Step 3 原始三项之一; proposal.md:39)
  - post_closure     (同上)
  - mid_post_spec    (同上)
  - mid_implementation (R1 rework 追加; proposal.md:253)
  - post_brainstorm  (裁定 1 追加; tasks.md 读前必看第 6 条)

用法: python3 -B cross_id_fa_fb_check.py classify_F.json
"""
import json
import sys
from collections import defaultdict

FIXED_EXCLUDED_CHECKPOINTS = {"pre_merge", "post_closure", "mid_post_spec", "mid_implementation", "post_brainstorm"}


def consistent(r):
    """与 select_samples.py 的 consistent() 逐字同定义 (两列一致)。"""
    if not r.get("final_matches"):
        return False
    cid = r["final_matches"][0]
    return r["col1_status"] == "ok" and r["col1_normalized"] == cid


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    recs = d["records"]

    matched = [r for r in recs if r["bucket"] == "matched"]
    print(f"matched 桶全量 = {len(matched)}")

    # 过滤: 可纳入 checkpoint (非 Step 3 固定排除项) + 两列一致
    includable = [
        r for r in matched
        if r["checkpoint"] not in FIXED_EXCLUDED_CHECKPOINTS and consistent(r)
    ]
    print(f"过滤后 (可纳入 checkpoint + 两列一致) = {len(includable)}")

    excluded_by_checkpoint = [r for r in matched if r["checkpoint"] in FIXED_EXCLUDED_CHECKPOINTS]
    print(f"  其中被 checkpoint 固定排除剔除 = {len(excluded_by_checkpoint)}")
    by_cp = defaultdict(int)
    for r in excluded_by_checkpoint:
        by_cp[r["checkpoint"]] += 1
    print(f"  按 checkpoint 分布: {dict(sorted(by_cp.items()))}")

    inconsistent_count = len([r for r in matched if r["checkpoint"] not in FIXED_EXCLUDED_CHECKPOINTS and not consistent(r)])
    print(f"  其中 checkpoint 可纳入但两列不一致而被剔除 = {inconsistent_count}")

    # 按 id 分组, 记录该 id 在过滤后的集合里是否出现过 F-a 形态 / F-b 形态
    id_has_fa = defaultdict(bool)
    id_has_fb = defaultdict(bool)
    id_fa_files = defaultdict(list)
    id_fb_files = defaultdict(list)
    for r in includable:
        cid = r["final_matches"][0]
        for s in r["shapes"]:
            if s["change_id"] != cid:
                continue
            if s["shape_tail"]:
                id_has_fa[cid] = True
                id_fa_files[cid].append(r["file"])
            if s["shape_role_suffix"]:
                id_has_fb[cid] = True
                id_fb_files[cid].append(r["file"])

    all_ids = set(id_has_fa) | set(id_has_fb)
    both = sorted(cid for cid in all_ids if id_has_fa[cid] and id_has_fb[cid])

    print(f"\n过滤后出现过的 id 总数 = {len(all_ids)}")
    print(f"其中同时具有 >=1 F-a 形态与 >=1 F-b 形态记录的 id 数 = {len(both)}")
    for cid in both:
        print(f"  {cid} | F-a: {id_fa_files[cid]} | F-b: {id_fb_files[cid]}")

    # 对照: 钉死 id state-scanner-inter-cycle-surfacing 本身在过滤后集合里的状态 (应仍是 F-a=2/F-b=3, 因其 5 份都不是 pre_merge 被排除的那 3 份, 见下方核对)
    pinned = "state-scanner-inter-cycle-surfacing"
    print(f"\n对照 (钉死 id, 不受本次过滤影响, 因其 checkpoint 非固定排除项): "
          f"has_fa={id_has_fa.get(pinned, False)} has_fb={id_has_fb.get(pinned, False)} "
          f"fa_files={id_fa_files.get(pinned, [])} fb_files={id_fb_files.get(pinned, [])}")

    # 单独核对: 3.1 表里那 3 份 pre_merge- 开头的 F-b 样本, 在本次「可纳入 checkpoint」
    # 过滤前 checkpoint 字段的实际值 (证实它们的 checkpoint 就是 'pre_merge', 因而
    # 被本脚本的过滤条件剔除)
    target_files = {
        "pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md",
        "pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md",
        "pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md",
    }
    print("\n§3.1 表格 3 份 F-b 样本的 checkpoint 字段实测:")
    for r in matched:
        if r["file"] in target_files:
            print(f"  {r['file']} | checkpoint={r['checkpoint']!r} | in_fixed_excluded={r['checkpoint'] in FIXED_EXCLUDED_CHECKPOINTS}")


if __name__ == "__main__":
    main()
```

运行 (与本节第一步产出的 `classify_F.json` 在同一目录):

```text
$ python3 -B cross_id_fa_fb_check.py classify_F.json
matched 桶全量 = 800
过滤后 (可纳入 checkpoint + 两列一致) = 576
  其中被 checkpoint 固定排除剔除 = 47
  按 checkpoint 分布: {'mid_implementation': 1, 'post_brainstorm': 3, 'pre_merge': 43}
  其中 checkpoint 可纳入但两列不一致而被剔除 = 177

过滤后出现过的 id 总数 = 38
其中同时具有 >=1 F-a 形态与 >=1 F-b 形态记录的 id 数 = 0

对照 (钉死 id, 不受本次过滤影响, 因其 checkpoint 非固定排除项): has_fa=True has_fb=False fa_files=['post_spec-R1-2026-05-08-state-scanner-inter-cycle-surfacing.md', 'post_spec-R2-2026-05-08-state-scanner-inter-cycle-surfacing.md'] fb_files=[]

§3.1 表格 3 份 F-b 样本的 checkpoint 字段实测:
  pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md | checkpoint='pre_merge' | in_fixed_excluded=True
  pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-c.md | checkpoint='pre_merge' | in_fixed_excluded=True
  pre_merge-R1-R5-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-b.md | checkpoint='pre_merge' | in_fixed_excluded=True
                                                                      # exit 0
```

**读数**: 800 = 576 (可纳入 checkpoint + 两列一致) + 47 (checkpoint 落 Step 3 固定排除,
`pre_merge` 43 份 + `mid_implementation` 1 份 + `post_brainstorm` 3 份; `post_closure` /
`mid_post_spec` 在本仓 `matched` 桶实测均为 0 份, 是语料本身没有该形态, 不是排除逻辑未生效)
+ 177 (checkpoint 可纳入但两列不一致而被剔除), 三者之和逐字核验为 800, 无遗漏无重复。过滤后
出现过的 38 个不同 id 里, **同时具有 F-a 与 F-b 两种形态记录的 id 数 = 0** —— 连各自 ≥1 的
组合都不存在。该数字系本节独立复算所得 (脚本、命令、原始输出均在上方), 与决策单第 1 项给出的
数字一致, 但不是抄决策单得来。

**补正说明** (2026-09-30, qa-corpus-D): 本节原稿 (qa-corpus-C 执笔) 的 Step 3 固定排除集漏列
`post_brainstorm`, 只按四项过滤, 得旧读数 579/44 (`pre_merge` 43 份 + `mid_implementation`
1 份); 已按上文 8.1 末句改正为五项并重新复算, 得 576/47 (`post_brainstorm` 计 3 份, 命令与
原样输出见上方代码块)。五项 (正确) 结果是四项 (原稿) 结果的子集 —— 原稿只是少排除一项,
统计面更大, 子集内「同时具有 F-a/F-b 的 id 数」不可能超过超集里的同一数字; 四项与五项两次
复算此数字均为 0, 结论不受影响。出处: 主控核验。

钉死 id `state-scanner-inter-cycle-surfacing` 本身在此过滤下降为 `has_fb=False` —— 它的 3 份
F-b 形态样本清一色是刚被剔除的 `pre_merge` checkpoint, 过滤后该 id 只剩 2 份 F-a 形态证据。
这与它在 3.1 表格「两列一致」列全部标「是」**不矛盾**: 两列一致 (frontmatter 归一化值与名匹配
是否相同) 与 checkpoint 是否落入 Step 3 固定排除集合是两个正交维度, 3.1 表格从未断言过
checkpoint 维度, **该表本身不需要、也未被改动**。

### 8.3 裁定

依决策单第 1 项, 走 SC-2 原文 (proposal.md Tasks B.0 (b1) 段) 自带的兜底规则 (c) ——「剔除后
某族样本不足 SC-2 规定的下界 ⇒ 换 id 重新采样, 换不到则该族在 SC-2 里按实测上限记名降低下界,
不得为了凑数把争议条目放回去, 也不得用 `--change-id` 自造样本顶替真实语料」:

1. **8.1 列出的 3 份 F-b 样本标为不可用并记名** —— 原因: `pre_merge` 是 Step 3 的固定排除项,
   门在正确实现下的 `results` 与统计面结构上不会观测到落在该 checkpoint 上的报告, SC-2 若
   断言这 3 份被正确 attribute 给 `state-scanner-inter-cycle-surfacing`, 在正确实现上必红。
2. **「换 id 重采」不可行**: 8.2 第三步的复算证明, 整个冻结语料 F 上按「可纳入 checkpoint +
   两列一致」过滤后, 不存在任何一个 id 同时具有 ≥1 F-a 形态与 ≥1 F-b 形态记录 —— 没有可换的
   候选 id, 该族在真实语料上没有第二条路。
3. **F-b 下界按本节实测上限降为 0。**
4. **SC-2 的断言面相应收窄**: (i) 用 F-a / F-c / F-d 三族验归属判定 (F-b 退出该断言面);
   (ii) 照旧验 F-e / F-f 与 `matched` 三桶两两不交 (`excluded_legacy_count` 与
   `unattributed_count` 的成员集互不相交, 且两者都不与 `matched` 相交), 此项判据未受影响。

3.1 表格与 §2.1/§2.2 两个脚本原样保留, 不因本节改动 —— 原标注留作溯源, 本节是关于 F-b 样本
可用性的唯一口径变更记录。
