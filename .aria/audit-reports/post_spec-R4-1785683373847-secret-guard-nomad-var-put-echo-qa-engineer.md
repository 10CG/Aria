---
verdict: PASS
agent: qa-engineer
round: R4
critical_count: 0
major_count: 0
minor_count: 2
r3_resolved: 1/3
---

# post_spec R4 审计（收敛终验）— secret-guard-nomad-var-put-echo (qa-engineer 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md` +
`/home/dev/Aria/standards/conventions/secret-hygiene.md`。只审不改，未修改仓库任何文件；
所有验证均在 scratchpad (`/tmp/claude-1000/.../scratchpad/r4work/`) 内构建注入版 hook 副本
完成。

## 任务 1 — 核销 R3 的 1M（SC-4 两条 FP 探针）

现读 proposal §Success Criteria SC-4：

> 尾边界使「`put` 后紧跟引号」不匹配, 故 `grep -rn 'nomad var put' aria/` 与
> `echo "改用 nomad var put"` **改后仍 exit=0 (放行)**; 仅 `put` 后**真有空格**的文本
> 提及被拦, 以 `git commit -m "fix: nomad var put 回显"` **exit=2** 锁定。附阳性对照:
> 真执行形态 `nomad var put <path> @f` exit=2。

实测（`sg-patched.sh`，唯一改动 = 插入
`'nomad[[:space:]]+var[[:space:]]+put([[:space:]]|$)'`，位置紧邻既有 `(get|list)`）：

```
[SC-4a]  before=0 after=0 | grep -rn 'nomad var put' aria/
[SC-4b]  before=0 after=0 | echo "改用 nomad var put"
[SC-4c]  before=0 after=2 | git commit -m "fix: nomad var put 回显"
[SC-4pos] before=0 after=2 | nomad var put <path> @f
```

与改写后的 spec 文字**逐字一致**。R3 M-1 的根因（尾边界正则要求 "put" 后紧跟空白/行尾,
"put" 前跟引号的两条不触发）在当前文本中已如实描述，不再与实测矛盾。**M-1(R3) 核销**。

Impact 段"风险"小节的 FP 描述（"仅当被引文本里 `put` 后真有空格时才拦"）与 SC-4 正文
同步一致，未发现文档内部自相矛盾。

## 任务 2 — SC-1~SC-7 逐条实跑

方法: 真实 `aria/hooks/secret-guard.sh`（改前, HEAD 未打补丁, `sg-before.sh`）与逐字
按 proposal §What 唯一改动构建的补丁副本（`sg-patched.sh`）做双侧 `exit code` 对照,
用与仓库测试文件相同的调用契约 (`jq -n '{tool_name:"Bash", tool_input:{command:$c}}' | HOOK`)。

```
=== SC-1 (baseline-failing: before=0, after=2) ===
[SC-1a]  before=0 after=2 | nomad var put -in=json <path> @file
[SC-1b]  before=0 after=2 | nomad var put <path> KEY=<literal>
[SC-1c]  before=0 after=2 | nomad var put -out=json <path> @f
[SC-1d]  before=0 after=2 | nomad var put -out=table <path> @f
[SC-1e]  before=0 after=2 | nomad var put -out=none <path> @f

=== SC-2 (existing credit unaffected: before=0, after=0) ===
[SC-2a]  before=0 after=0 | nomad var put <path> @f >/dev/null
[SC-2b]  before=0 after=0 | nomad var put <path> @f &>/dev/null
[SC-2c]  before=0 after=0 | nomad var put -out=none <path> @f >/dev/null
[SC-2verbose] before=0 after=0 | nomad var put -verbose <path> @f >/dev/null   ← 警示注记锚点(转出2相邻面), 按spec"本spec不收口, 已实测放行"描述一致

=== SC-3 (tail boundary: after=0, no misfire) ===
[SC-3]   before=0 after=0 | nomad var putty foo

=== SC-4 (见任务1, 已逐字核对) ===
[SC-4a]  before=0 after=0 | grep -rn 'nomad var put' aria/
[SC-4b]  before=0 after=0 | echo "改用 nomad var put"
[SC-4c]  before=0 after=2 | git commit -m "fix: nomad var put 回显"
[SC-4pos] before=0 after=2 | nomad var put <path> @f

=== SC-6 (读向不回归, 双锚点) ===
[SC-6a]  before=2 after=2 | nomad var get <path>
[SC-6b]  before=2 after=2 | nomad var list
[SC-6c-pos] before=0 after=0 | nomad var get -out=json <path> | jq '.Items | keys'      ← 正向锚点: 投影放行
[SC-6c-neg] before=2 after=2 | nomad var get -out=json <path> | jq '.Items | keys[]'    ← 负向锚点: 方括号破坏 jq filter 识别, 拦
```

全部 15 条命令 (SC-1 五条 + SC-2 三条+1 条警示注记 + SC-3 一条 + SC-4 三条+1 阳性对照
+ SC-6 四条) 的实测 exit code 与 proposal 文字**逐字一致**，零偏差。

### SC-5（全量回归, 命令实跑而非纸面推定）

用完整 `aria/hooks/` 目录树拷贝到 scratchpad (`plugin-after/hooks/`, 保留
`tests/../..` 相对路径以使 `${CLAUDE_PLUGIN_ROOT}` 子测试可解析 `hooks.json`)、
仅替换 `secret-guard.sh` 为补丁版:

```
real repo (改前, 原地跑):        secret-guard.test.sh   PASS 347/347
scratchpad (改后, 补丁版全目录树): secret-guard.test.sh   PASS 347/347
其余 5 个 hook 测试脚本 (real repo, 改前基线, 与本 spec 改动无交集):
  crlf-shim.test.sh                    PASS 8/8
  host-docker-logout-guard.test.sh     PASS 20/20
  jq-crlf-guard.sh / .test.sh          clean / PASS 7/7
  secret-scan.test.sh                  PASS 49/49
  submodule-gate-telemetry.test.sh     PASS 7/7
```

347 基线在补丁版下零回归（不同于 R3 只验证改前基线绿, 本轮额外对**补丁后**版本
补跑同一 347 条全量回归, 确认新增 pattern 不破坏任何既有断言）。SC-5 成立。

### SC-7 可执行性核验（本机 `nomad v1.11.2`）

**(a) 正向**：环境代理 (`HTTP_PROXY`) 会让 `192.0.2.1` 之类的"文档保留地址"经代理
返回 502 而非直接拒连, 干扰"只验 flag 层"判别；改用 `no_proxy` 列表内的
`http://127.0.0.1:1`（本机保留端口, 直连拒绝, 不走代理）复现出与 R3 相同的判别信号：

```
nomad var get -out=json ...  → "dial tcp 127.0.0.1:1: connect: connection refused"  (flag 通过)
nomad var put -out=json ...  → "dial tcp 127.0.0.1:1: connect: connection refused"  (flag 通过)
nomad var get -out=keys ...  → "Invalid value for \"-out\"; valid values are [...]" (flag 层拒绝, 对照组)
```

全文 grep `secret-hygiene.md` 内所有 `-out=` 推荐用法，逐处均为 `-out=json`（L166 python /
L182 bash / L185 bash / L39 §1 Verification 行 / L8 incident 引用），零处使用非法枚举值
作推荐写法——SC-7(a) 成立。

**(b) 负向（机械可执行性, 给出执行方法）**：全文 grep `-out=keys` 共 2 处命中
（L163 / L188）。机械判定法：对每处命中取一个上下文窗口（本次用"命中行 + 前 2 行",
可按段落/句子边界调整), 检查窗口内是否含负向标记词集合（"不存在" / "不要用" / "误写" /
"Invalid value" / "旧版本" / "❌" 等固定小集合，可作为 lint 规则常量维护）。用
Python 脚本实跑：

```python
neg_markers = ["不存在", "不要用", "误写", "Invalid value", "不可用", "错误", "旧版本", "❌"]
# 结果:
# line 163: WARNING-CONTEXT markers=['误写', 'Invalid value', '旧版本']
# line 188: WARNING-CONTEXT markers=['不存在', '不要用']
```

2/2 命中均落入警示语境，零处位于推荐语境。该方法可直接封装为 CI/pre-commit 脚本
（grep 找命中行号 + 窗口取词 + 负向词表匹配 + 命中数与窗口覆盖率断言），非仅靠人工
读段落判断——SC-7(b) 声称的"机械断言"具备可执行性，方法本身也已在本轮验证。

## 任务 3 — SC 集合完整性终验

零豁免设计下状态空间基本闭合，本轮未发现新缺口：

- 无真空成立 (vacuous truth) 的 SC：每条断言都存在至少一个可能翻转的失败模式
  (SC-2/SC-6 虽是"应保持不变"型断言, 但已实测证明其对"新 pattern 与既有 credit
  逻辑交互出错"这类真实设计风险 (R2 C-1 的攻击面即为此类) 具备鉴别力，不是摆设)。
- 无恒绿无鉴别力的 SC：SC-4 现在同时含 allow (a/b) 与 block (c/阳性对照) 两类结果，
  不再是清一色断言、可反证"pattern 未生效"或"pattern 过宽"两个方向的错误实现。
- "14 条断言" 数字与 SC-1(5)+SC-2(4)+SC-3(1)+SC-4(4) 精确吻合，SC-5/SC-6/SC-7 正确地
  未计入该数字（回归聚合 / 既有行为核验 / SOT 订正核验，性质不同于"新增断言"）。
- 覆盖面对照 R1/R2/R3 三轮全部往返过的争议点（SC-3 方向、SC-6 读向、SC-2 credit
  语义、SC-4 FP 现状）均在本轮逐条复核，未见新缺口。

## R3 三条 finding 核销状态（本轮 r3_resolved: 1/3）

| 编号 | 严重度 | R3 结论 | R4 核验 | 状态 |
|------|--------|---------|---------|------|
| M-1(R3) | Major | SC-4 三条 FP 探针中 2 条未真正触发新 pattern, 与"改后 exit=2"矛盾 | SC-4 已改写为按实测结果描述 (grep/echo 放行, commit 拦), 实测逐字一致 | **已核销** |
| m-1(R3) | Minor | Key Deliverables「SC-1~SC-5, 共 14 条断言」区间标注比实际来源 (SC-1~SC-4) 多算 SC-5 | 全文 grep 仍见两处 "SC-1~SC-5"（Key Deliverables L62 + Tasks 1.2 L126），未订正 | **未核销（原样遗留）** |
| m-2(R3) | Minor | 转出 1「影响 140 pattern」计数会在 ship 后（141 条）过期 | 全文 grep 仍见两处 "140 pattern"（Why 段 L38 + 转出1 L104），未订正为 "141 (含本次新增)" | **未核销（原样遗留）** |

两条未核销项均为 R3 自己定性的"纯文字精度问题，不影响实现正确性"级别（Minor，非
Major/Critical），且都是一行字面替换、无逻辑歧义 —— 不构成本轮新增风险面，也未在
本轮产生任何新的 Major/Critical。按本 spec 三轮以来的一贯裁断口径（R1/R2/R3 均只对
Critical/Major 计入 REVISE 阻断条件, Minor 累积但不单独否决收敛), 不因这两条未处理
的文字项否决 PASS，但作为遗留项在此明确记录，建议在 B.2 落地测试文件时顺手一并改掉
（成本近零，且两处位置与本轮改动的 SC-4/`标准`文件均无关，不会引入新审计面）。

## 结论

0 Critical, 0 Major, 2 Minor（均为 R3 遗留、未升级、未新增）。R3 唯一 Major 已用
补丁副本 + 阳性/阴性双向实测核销；SC-1~SC-7 全部命令逐条实跑，exit code 与 proposal
文字逐字一致；SC-5 首次针对**补丁后**版本补跑 347 条全量回归 + 其余 5 个 hook 测试
脚本，全绿；SC-7(a)(b) 均验证可执行且给出可复用的机械化方法；SC 集合状态空间完整，
无真空/恒绿项。判 **CONVERGED (PASS)**。遗留 2 条 Minor（区间标注 SC-1~SC-5→SC-4、
"140 pattern"→"141"）建议 B.2 顺手订正，不阻塞收敛。
