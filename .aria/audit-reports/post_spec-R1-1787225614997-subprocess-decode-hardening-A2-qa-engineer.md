---
seat: A2-qa-engineer
round: R1
checkpoint: post_spec
spec: subprocess-decode-hardening
verdict: REVISE
critical_count: 1
major_count: 3
minor_count: 2
timestamp: 2026-08-20T00:00:00Z
---

# post_spec R1 A2 (qa-engineer) — subprocess-decode-hardening (aria-plugin#147)

透镜: SC 可证伪性 / 测试策略。方法: 逐条 SC 反事实检验 + 对冻结基线 SHA `3b97c35`
(当前 `aria/` submodule HEAD, 已核实一致) 的真代码抽查 (12 处「接不住」全部 12
处 + 4 处「接得住」全部 4 处逐行读过, 覆盖census全部16 生产站点; 另抽样 7/12 测试
文件)。全程只读 (grep/sed/python3 -c/git show), 未改任何文件。

## 结论先行

SC-4 的第二条 sink 链在当前代码里**不存在可达路径**——16 个生产迁移目标里唯一的文件
写入点写的是结构化字段, 从不吃 subprocess 解码文本; `verify_post_push.py` 也不做
"stderr 展示", 其 `json.dumps` 用的是默认 `ensure_ascii=True` (已实测: 该路径本来
就不会因代理码位崩溃)。这不是文字瑕疵——是 SC-4 要求实现方构造一个不对应任何真实
代码路径的 fixture, 属于教训 `feedback_reused_code_fixture_shape_drift_false_green`
同类风险的镜像形态 (这次是"sink 不存在"而非"fixture 与真数据形态脱节")。另外
census 的"16 生产站点/12 接不住"计数本身有一处可验证的误判 (`coordination_ref.py:255`
早已用 `errors="replace"` 结构性免疫, 却被归入"接不住"), 说明产出这张表的普查脚本
(未随仓提交, 只留下 `.aria/notes/2026-08-20-census-147.md` 的结果) 对 `errors=`
参数不敏感——SC-2 声称"普查脚本与结构化测试同源"目前是愿望, 不是事实。

## Critical

**[A2-C1] SC-4 的第二条 sink 链 ("文件写") 在 16 个生产站点里找不到可达代码路径; 第一条链
的具名脚本 (`verify_post_push.py`) 也对不上其自身的 sink 类型分类。**

anchor: proposal.md §Success Criteria SC-4 + §What Changes 第 2 条 ("两类已证实 sink")

实测过程 (对 16 个生产站点的宿主文件逐一 grep `\.write(\|open(.*['\"]w\|\.dump(`):

```
仅 1 处命中: aria/skills/state-scanner/scripts/phase1_gate.py:983
    fh.write(_json.dumps(record, ensure_ascii=False) + "\n")
```

读取 `_emit_telemetry` (phase1_gate.py:955-985) 确认 `record` 的字段全部来自
`GateResult`/调用参数 (`ts`/`source`/`arm`/`outcome`/`track_id`/`claim_written`/
`collision_surfaced`/`surface_kind`/`latency_ms`) —— 没有一个字段承接
`subprocess.run` 解码后的原始文本; 该函数所对应的 `_is_git_repo`
(phase1_gate.py:233-248, census 里 line 240 的站点) 只返回 `bool`, 从未把
subprocess 输出传进 `_emit_telemetry`。也就是说, "文件写"型 sink 在 16 个迁移
目标的宿主文件里**唯一的实例, 恰好不是任何一个迁移站点的下游**。

再查 SC-4 具名的第二条链 "verify_post_push → stderr 展示": 读 `verify_post_push.py`
全文 (main() 236 行) 只有一处输出:

```python
print(json.dumps(output, indent=2))   # 默认 ensure_ascii=True, 打到 stdout, 非 stderr
```

没有 `ensure_ascii=False`, 没有 `.encode(`, 没有文件写, 也没有任何 `sys.stderr` 输出。
且用 python3 实测验证了 spec 自己在 "两种修法" 段落的技术主张:

```
b = bytes([0xff, 0xfe])
s = b.decode('utf-8', errors='surrogateescape')   # '\udcff\udcfe'
json.dumps({'x': s})                # 默认 ensure_ascii=True → 成功, 不炸
json.dumps({'x': s}, ensure_ascii=False).encode('utf-8')   # 炸 UnicodeEncodeError
```

即 `verify_post_push.py` 走的正是"默认 ensure_ascii=True 不炸"那条安全路径——它当前
版本 (`text=True`) 崩溃的**唯一原因**是 `subprocess.run` 自己解码这一步本身抛
`UnicodeDecodeError`, 与"下游 sink 是否安全"完全无关。迁移后它不再崩溃, 是因为
**上游** decode 不再抛, 而不是因为验证了某个"sink 安全"命题。

唯一真实可验证的 sink 链是 `aether.py:150/173`
(`except (TimeoutExpired, FileNotFoundError, OSError)` 接不住解码异常)
→ 若解码不抛而是走 `AetherQueryError`, `str(exc)` 在
`pre_merge_gate.py:495` / `:518` 被赋给 `raw_message`, **未经** `_sanitize_for_json`
→ `pre_merge_gate.py:568` `json.dumps(output, ensure_ascii=False)` 落地。这条链
是真实的、可构造的, 唯一属于 `dumps(ensure_ascii=False)+encode` 类型。

后果: SC-4 要求"两类 sink 各覆盖 ≥1 条链", 但可达证据只支持 1 类 (`dumps
ensure_ascii=False`) 1 条链。实现方面对这条 SC 只有两条路: (a) 硬造一个不对应
16 个迁移站点真实下游的"文件写"fixture 让 SC-4 字面通过, 制造一个不代表任何
生产风险的绿灯 (假绿); (b) 悄悄把 verify_post_push.py 的 stdout-JSON 也算作
"sink 覆盖", 但它既不是 file write, 也不是 ensure_ascii=False——等于重新定义 SC-4
的判据来凑数。两条路都不满足 SC 应有的可证伪性。

建议: SC-4 改为只主张已证实的 1 条链 (aether.py → pre_merge_gate.py:568), 并把
"防再长"的责任转交给 SC-2/SC-3 的结构化断言 (不依赖识别第二个 sink 类型); 或者
如果 owner 确实要保 2 类覆盖, 需要先在 16 个站点之外找到一个真实的文件写链
(当前找不到), 否则应在 spec 里明确降级为"1 类 sink 覆盖 + 1 条已证实链"。

## Major

**[A2-M1] census 对 `coordination_ref.py:255` 的"接不住"分类是误判——该站点已用
`errors="replace"` 结构性免疫, 拉低了"12 处接不住"的真实计数, 且暴露普查脚本对
`errors=` 参数不敏感。**

anchor: `.aria/notes/2026-08-20-census-147.md` "prod uncovered sites" 表 +
`aria/skills/state-scanner/lib/coordination_ref.py:255-268`

实读代码:

```python
result = subprocess.run(
    cmd, cwd=str(cwd), capture_output=True,
    text=True,
    encoding="utf-8",   # #61: git output is UTF-8 by spec
    errors="replace",   # #61: never raise UnicodeDecodeError to the caller
    ...
)
```

`errors="replace"` 使该 decode **结构上不可能**抛 `UnicodeDecodeError`, 与 except
元组是否含 `OSError`/`ValueError` 无关——这正是「prod covered」表里
`collectors/_common.py:406` 用来"接得住"的同一手法 (逐字比对: 两处都是
`encoding="utf-8"` + `errors="replace"`, 注释都引用 #61 修复)。但 census 把
`_common.py:406` 归入"prod covered"、把 `coordination_ref.py:255` 归入
"prod uncovered", 对同一防护手法给出了相反的分类。

产生这张表的"普查脚本"本身不在仓库里 (`find . -iname '*census*'` 只命中
`.aria/notes/2026-08-20-census-147.md` 这份笔记本身, 无任何 `.py` 脚本), 只能
推断其判据是"有 `text=True` + 逐层向上找 except 是否含 ValueError 族", **没有检查
`errors=`/`encoding=` 关键字参数是否已经中和风险**。

连带影响:
- "16 生产站点/12 接不住"的叙事计数至少高估 1 (真正"接不住"的应 ≤11), triage
  report 的 severity/次数判断继承自这张表, 同样被拉高。
- SC-1 "对照组 text=True 同输入必抛 UnicodeDecodeError（锁定改前红）" 若被逐站点
  实例化 (而非只做一次通用 helper 演示), 对 `coordination_ref.py` 会**不成立**——
  它改前就不红。这正是本轮审计被要求警惕的"改前红"假设未经逐站点验证的具体案例。
- SC-2 "普查脚本与第 4 条测试同源, 防口径漂移"目前不成立——没有脚本可"同源",
  A.2 要重新手写, 若不显式要求检查 `errors=`, 会重复同一盲区。

建议: A.2 detailed-tasks 里加一步"逐站点核对是否已有 `errors=`/`encoding=` 中和",
并把 `coordination_ref.py:255` 重新分类为"已结构性安全, 迁移仅为统一模式"而非
"接不住"; 把普查脚本本身 (含 `errors=` 检查) 提交进仓库, 使 SC-2 的"同源"断言可核实。

**[A2-M2] SC-3 "对基线树跑"没有给出可执行口径; 引用的 #181 先例不是同类机制。**

anchor: proposal.md SC-3 ("结构化测试对基线树跑 = 红...三态都要实测留痕") +
`.aria/probes/config-template-key-currency.py`

SC-2/SC-3 都是纯静态 AST 计数断言, 不需要真的跑代码, 理论上对 baseline 用
`git -C aria show 3b97c35:<path>` 取文本内容做 `ast.parse` 即可, 完全不需要
`git worktree` 签出——但 spec 没写这个口径, 只写了"对基线树跑"这个动作名, 留给
B.1 的实现者自己猜是"物理签出旧 SHA 的 worktree"还是"git show 取快照文本"。两者
成本和风险都不同 (worktree 签出子模块 SHA 有引入额外 submodule 状态副作用的
风险)。

读了 spec 引用的先例 `.aria/probes/config-template-key-currency.py` (Aria #181
baseline-failing 先例) 后确认: 它是**单棵当前树上跑一次的探针**, 用
"若模板键与 DEFAULT_CONFIG 不同步就 FAIL"的语义描述来说明"这条检查若在 bug 存在
时跑会红", 并没有真的对一棵历史/基线 git 树执行代码或做三态对比。SC-3 要求的
"三态都要实测留痕"(基线树跑红 / 迁移树跑绿 / 注入 text=True 后迁移树跑红) 比 #181
的先例严格得多, 在本仓找不到可复用的操作范式, B.1 需要从零发明——这正是
post_spec 审计应该在这里挡住、要求 spec 把口径写清楚的地方, 而不是留到 B.1 现造。

建议: SC-3 补一句机制口径, 例如"基线态经 `git -C aria show 3b97c35:<path>` 取快照
文本喂给同一 AST 计数函数, 不做 worktree 签出", 消除歧义。

**[A2-M3] SC-6 "except 元组成员集合逐一相等"没有指定基线/迁移两侧站点的匹配键;
若按 `file:line` 匹配 (census 现有索引方式), 迁移改动行号后会自我打假。**

anchor: proposal.md SC-6 + `.aria/notes/2026-08-20-census-147.md` 索引格式
(`file:line`)

census 现有的 16 个站点全部以 `file:line` 索引 (如
`verify_post_push.py:65`/`:89`, `spec_complete.py:863`/`:874`)。迁移本身就会
删掉 `text=True,` 这一行、加入若干行 bytes-decode 代码, 使同文件里每个站点之后
的行号整体偏移。若 SC-6 的"结构化断言"按 `file:line` 做迁移前后的一一匹配 (最直白
的实现方式, spec 未排除这种读法), 那么 `verify_post_push.py:89`(第二个站点)在
迁移后大概率已经不在原行号——断言会因为"匹配不到"而不是因为"except 元组真的变了"
报错, 属于永假/永红或干脆被实现者悄悄改成"按文件汇总而非按站点比对", 稀释了
"逐一相等"这个字面承诺的精度。

建议: SC-6 明确匹配键为"每站点的 enclosing 函数名 + 站点在该函数内的序号", 不用
原始行号, 避免上述自我打假。

## Minor

**[A2-m1] SC-5 的基线计数延后到 B.1 才实测, post_spec 阶段不可证伪——这本身可接受
(Level 2 spec 允许), 但要显式提醒: 必须对冻结 SHA `3b97c35` 记录, 不能偷懒记成
B.1 当时的活跃分支状态。**

anchor: proposal.md SC-5 ("基线数在 B.1 入场时对 3b97c35 实测记录")

`3b97c35` 是 `aria` 子模块的冻结基线 SHA, 我核对过当前 `aria/` submodule 的
HEAD 正好等于它 (`git -C aria rev-parse HEAD` = `3b97c35c45f45ffbdb472658d002e8859545f9ed`)。
但 B.1 执行时子模块大概率已经前进 (16 站点迁移会在同一分支上做), "对 3b97c35 实测"
要求的是对**这个具体 SHA** 单独跑一次 (`git -C aria show 3b97c35:... | 跑测试`
或等效的一次性快照跑, 而非直接读当前分支上跑出来的数字), 否则"零回归"比较的
基线和当前值可能已经悄悄变成同一棵在演进的树——即 memory 教训
`feedback_baseline_corpus_stat_must_run_against_frozen_snapshot` 描述的同类陷阱。
建议 A.2 detailed-tasks 把"对冻结 SHA 而非活分支取基线"写成显式步骤。

**[A2-m2] "30 处测试调用点范围外"的"测试输入受控"论证只抽样核实了 7/12 个测试
文件, 未覆盖全部。**

anchor: proposal.md §Out of scope 第一条 + census "test sites" 表

抽样读了 `corpus_census.py`、`test_path_coverage.py`、`test_consistency_check.py`、
`_helpers.py`、`test_release_by_track.py`、`test_scan_integration.py`、
`test_spec_complete.py` 共 7 个文件 (占 30 处调用点里的多数), 全部命中的
`subprocess.run(text=True)` 都是对**本地临时构造的 git 仓/`--help`/`scan.py`
子进程**调用, 不触达真实外部网络, 与 spec 的"测试输入受控"论证一致。但还有 5 个
文件未读 (`test_collision.py`、`test_handoff.py`、`test_normalize_snapshot.py`、
`test_p1_layer_h.py`、`test_phase1_gate_advisory.py`), 论证目前是"抽样支持",
不是"逐一核实"。不构成 REVISE 理由 (抽样已支持出 scope 判断成立的方向), 但建议
A.2 或复核轮补上剩余 5 个文件的核实, 完整回答本轮审计被要求回答的"有没有测试点
实际会吃真实外部输入"。

## 建议新增/强化的 SC (对照 memory 教训: fixture 参数反推=假绿 / 防御 fix 在测试
是 no-op 时全绿=循环论证)

- **SC-9 (建议)**: 「census 复核」——A.2 锁定 12/4 分档前, 重跑分类脚本时须显式
  检查每个"接不住"站点的 `subprocess.run` 调用是否已带 `errors=`/`encoding=`
  中和参数; 产出脚本本身提交进仓库 (而非只留结果笔记), 使 SC-2 的"普查脚本与
  结构化测试同源"从愿望变成可核实的事实。
- **SC-10 (建议)**: 「sink 链证据前置」——SC-4 的每条具名 sink 链, 在写 fixture 前
  必须先给出一条从"迁移站点的 subprocess.run"到"该 sink 调用"的静态调用链证据
  (file:line 序列, 如本报告给出的 `aether.py:150→pre_merge_gate.py:495→:568`),
  写不出这条证据链的 sink 类型不得计入"已覆盖"; 直接堵死"造一个不对应真实代码的
  fixture 让 SC 字面通过"这条路。

## 判据

Critical 1 (A2-C1) → REVISE (已满足"任一 Critical"条件; Major 3 条同时满足
"≥2 Major"条件, 双重触发 REVISE)。
