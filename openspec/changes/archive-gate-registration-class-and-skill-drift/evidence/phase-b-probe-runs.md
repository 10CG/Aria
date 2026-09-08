# Phase B 探针实跑留证 (C-3 四态 / C-8 五态 / C-10 三态)

> **本文件由脚本重新实跑生成, 不是从对话里抄的** (memory `pasted-evidence-is-derived`: 贴进文档的输出是派生物, **每次探针改动后必须重生成**)。
> 生成时刻 (UTC): 2026-09-08T10:58:41Z · **与本文件所在 commit 同版** (不写死 SHA —— 写文件时 gitlink 尚未 bump, 落地复审实测标错过一次)
> ⚠️ 落地复审抓到两件事: (1) C-3/C-8/C-10 三项验收逐字写「留证」, 但此前仓内**零输出** —— 勾是凭对话里的运行勾的; (2) 首版留证用的是**改前**的探针, 探针经复审重写后本文件已重生成。
> 📌 **本文件不在 D-V2 / SC-12 的扫描范围内** (那两条逐字只覆盖 `proposal.md` 与 `tasks.md`)。原因: 本文件收录探针在**正控版本**上的输出, 而那份输出按设计就是一串裸 issue 引用清单 —— 拿检查器扫自己的取证输出必然恒红且零信息量。如实登记而非加进允许清单 (加进去会让**未来真的写错**的同形状字面一并免检)。

## C-3 — `skill_md_literal_sync_probe.py` 四态

### 态 1/4 基线 — 期望 FAIL rc 1 且打印两侧原文

> B-1/B-2 已落地, 真仓现为目标态 ⇒ 基线用 `aria` 子模块 `origin/master` 版的两个目标文件在同构插件树里复现 (探针本体用当前版, 只回退被测对象)。

```
FAIL SHA 回链占位串两侧漂移:
  SKILL.md         : '> 归档 SHA 回链: 由 openspec-archive Step2 归档提交后填入'
  _build_d_payload : '> 归档 SHA 回链: 由 openspec-archive Step 7 归档提交后填入'
rc=1
```

### 态 2/4 目标 (真仓, B-1/B-2 落地后) — 期望 PASS rc 0
```
OK 两侧一致: '> 归档 SHA 回链: 由 openspec-archive Step 7 归档提交后填入'
rc=0
```

### 态 3/4 锚点提取数 ≠ 1 (同构插件树, 两个空文件) — 期望 FAIL rc 1
```
FAIL 锚点提取数异常 (期望各 1): SKILL.md=0 spec_complete.py=0 — 措辞被改动, 需人工对齐后更新本探针
rc=1
```

### 态 4/4 坏实现「两侧同改回 Step2」— 期望 FAIL rc 1 (只有第三条断言挡得住)
```
FAIL 两侧一致但值错了 (缺 'Step 7'): '> 归档 SHA 回链: 由 openspec-archive Step2 归档提交后填入'
  该值有 2026-07-22 成文裁定背书, 不得改回 Step2
rc=1
```

## C-8 — `archive_tracker_verify.py` 五态 (全部用冻结夹具, 不实时抓 API)

### 10CG/Aria#201 — 期望 rc 0 OK
```
OK: '> 归档 SHA 回链: 4c3c826 (Step 1-6 归档动作完成时的 HEAD; 本 Skill 自身不 commit, 归档变更的实际提交 SHA 见本 issue 后续评论或 Phase D 收尾 commit)'
rc=0
```

### 10CG/Aria#185 — 期望 rc 1 NO_SHA (挡「只查行存在」)
```
NO_SHA: 回链行存在但不含 7-40 位十六进制 SHA — '> 归档 SHA 回链: 归档提交落地后追评补充'
rc=1
```

### 10CG/Aria#186 — 期望 rc 1 MISSING
```
MISSING: 未找到以 '> 归档 SHA 回链:' 开头的行
rc=1
```

### 合成夹具 — 期望 rc 1 NO_SHA (真语料证不了长度下限)
```
NO_SHA: 回链行存在但不含 7-40 位十六进制 SHA — '> 归档 SHA 回链: abc (归档动作完成时的 HEAD)'
rc=1
```

### body 取不到 — 期望 rc 2 fail-CLOSED
```
FETCH_FAIL: 取不到 issue body — fail-CLOSED, 不当作通过
rc=2
```

## C-10 — `check_bare_issue_refs.py` 三态 (探针经落地复审重写后重跑)

### 态 1/3 目标态 (两份 Spec + handoff) — 期望 rc 0
```
裸 issue 引用: 0
rc=0
```

### 态 2/3 正控 (`d81873b^` 版) — 期望 rc 1, 命中数由脚本产出
```
  proposal.md:130 #185  坏实现拒绝: 「只查行存在」在 #185 上 GREEN ⇒ 无效; 「`[0-9a-f]+` 无长度下限」在 **#185 上也红** (该真语料尾部纯中文, 零 ASCII 十六进制) ⇒ **真
  proposal.md:130 #185  坏实现拒绝: 「只查行存在」在 #185 上 GREEN ⇒ 无效; 「`[0-9a-f]+` 无长度下限」在 **#185 上也红** (该真语料尾部纯中文, 零 ASCII 十六进制) ⇒ **真
  proposal.md:156 #140  - **机械兜底须全绿**: `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-
  proposal.md:202 #187  - **SC-10** (回归): `cd aria/skills/state-scanner/tests && python3 -B run_tests.py` ≥ **1575 / OK** (c
裸 issue 引用: 4
rc=1
```

### 态 3/3 坏实现「裸 grep 不排除三类」— 两版都报非零 ⇒ 判无效
```
目标态裸 grep 命中: 75
正控裸 grep 命中:   28
⇒ 两版均非零, 无法区分 ⇒ 坏实现判无效
```

## 探针自身判据的对抗性验证 (落地复审补 — memory `adversarial-fixture`)

`check_bare_issue_refs.py` 的封闭豁免集对六种形态的判定:
```
  adv.md:3 #199  c 多级路径 + 扩展名 + #数字          应违规 (路径伪装) 见 docs/x/y.md#199
  adv.md:4 #197  d 半限定 Aria#197                     应违规
  adv.md:5 #198  e 裸号 #198                           应违规
裸 issue 引用: 3
rc=1
⇒ 恰命中 c/d/e 三条, a/b/f 正确豁免
```
