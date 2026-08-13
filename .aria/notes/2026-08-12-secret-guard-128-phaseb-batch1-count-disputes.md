# #128 Phase B 批 1 — census 落地逼出的两个计数争议 (owner 复议项)

## ✅ owner 裁定 (2026-08-13) + 落实

owner 2026-08-13 逐条裁定 (大白话解释后确认): **family 采 57 · newline 采 13 · 两个反事实表按实测改**。主 loop 已落实到 proposal.md + detailed-tasks.yaml:

| 争议 | 裁定 | 落实点 |
|------|------|--------|
| family 55→57 | 采 census 实测 57 + 写死「`\b` 视作停止字面 token 串」约定 | proposal §转出1/§Impact/SC-18/SC-19 (全覆盖 57 / 余 45 补齐 = 57−12) + yaml TASK-010/016 |
| newline 11→13 | 采 13 (两基线均 13/13) | proposal §6 表 + §6 论证 + SC-18 |
| SC-6 恒split 15→16 | 采实测 16 (case 隔离断言在完整 stub 下同红) | proposal SC-6 反事实表 |
| SC-1 粘性 | 厘清两变体 (急切版红 2/3/5 / 最小版仅红 #3) | proposal §What.3 + SC-1 反事实 |

**解锁**: SC-18 现可绿 (census 输出 57/13 == 正文); TASK-016 (SC-19 探针补齐 57 家族) + TASK-020 (SC-13 回填) 可施工。下方原始复议记录保留作审计轨迹。

### 附: census 语料面口径澄清 (主 loop 2026-08-13 定, 第 5 个 Phase B 逼出的设计点)

落实裁定时发现 **census 挂了** (`extracted 331 triples but found 360 bash_case source lines`): 批 2 加的多行 bash_case (反斜杠续行, 如 SC-12) 破坏了 census 单行抽取。深层是**语料面口径**: `65/49/16` 是改前 305 条基线语料的属性, census 却扫会随批 2 增长的活文件 (直接扫得 `with_top_boundary=111`)。

**处置 (主 loop 定, 未改正文数字, 属实现约定)**:
1. **修 census extract 支持反斜杠续行** (`corpus_census.py`, 让默认扫活文件不再 crash + 防将来)。
2. **SC-18 语料面口径写死**: 须 `census --corpus <(git show af87cae:…/secret-guard.test.sh)` 对改前基线跑; family/判据/pattern 面 `--hook` 默认当前 hook, 一次调用自洽 (实测: 基线语料 65/49/16/15/5 + 当前 hook family 57 + newline 13/13, 全对正文)。已写进 proposal SC-18。
3. **census 默认无 `--corpus` 扫活文件的语料数无 SC-18 意义** (仅当前参考)。

这是 census 落地又一次逼出的口径缺陷 (同 family/newline 族), 但主 loop 判定为实现约定 (不改正文断言值, 只定调用方式), 未拦 owner。

### 附 2: printf 族 SC-19 gap (第 6 个 Phase B 逼出点, **待 owner 裁**)

TASK-016 (SC-19 补 57 族探针) 落地时发现 **printf 族 (pattern idx88 `printf -v NAME <进程替换读 env>`) 无法构造 rule 5 合规探针**:
- idx88 pattern 要求字面「进程替换重定向读 env」记号 (含 `(`) 才能匹配。
- 含该记号的命令**必被 safe_to_split 块字符判据降级**走 fallback (整条判定) → 改后仍 exit=2 (主 loop 实测两形态 canon=2 curr=2)。
- ⇒ **printf 族天然不属于跨段 fail-open 风险面** (它由 SC-6 块字符降级族间接覆盖), 但也因此**无法构造 SC-19 探针**: 2→0 探针不可能 (天然不翻转); 反例探针须含块字符, 违反 rule 5「探针不含块字符哪怕引号内」。单成员族无替代 pattern。

**agent 处置 (正确)**: 按 SC-19 明文「不自行缩口径 / 不 special-case pass / 不 ship 违规探针」, self-check 诚实 FAIL (56/57), 回归 531/532, 写 handoff 请复议。

**主 loop 建议 (owner 裁)**: **豁免 printf 族** —— SC-19 完备判据「57 族全覆盖」改为「覆盖全部**可跨段** family」; printf (唯一 pattern 要求块字符, 天然不可跨段) 排除; self-check 改 56/56 → PASS → 回归 532/532 全绿; 正文记 printf 天然安全的理由。备选 (不建议): 重写 idx88 去 `(` 要求 (改检测行为, 风险大) / 放松 rule 5 (依赖引号内块字符不降级的实现细节)。

**此 gap 卡 TASK-020/021 的「回归全绿」口径**, 待 owner 裁后收尾 B-验证。

---


> 归档时间: 2026-08-12 | 执笔: 主 loop | 语境: secret-guard-per-segment-evaluation Phase B 批 1
> (TASK-001..010 落地)。census (`corpus_census.py`) 首次实跑, SC-18 机械比对 23 个数, **21 MATCH /
> 2 MISMATCH**。两个 MISMATCH 恰好都落在 spec 正文自己声明「无脚本背书 / 不要凑数」的数上。
> 本 note 记录主 loop 对两处 MISMATCH 的**独立核验结论**, 供 owner 复议。**未 land 任何凑数改动。**

## 争议 1: `family_count` — spec 正文 55, 实跑 57

- **spec 出处**: proposal §转出 1 (行 444)「55 个家族」; SC-18 (行 868); TASK-010。spec **自己**声明
  (TASK-010 notes / 行 267): 「55 / 28 / 14 三个数无脚本背书 … census 落地后若与这三个数不一致,
  唯一合法动作 = 写 handoff 请 owner 复议, **不得**调分组器凑成 55/28/14」。
- **census 实跑**: 57 (82 条 spanning pattern 归键)。
- **主 loop 独立核验 (不看 census 实现, 另写归键器)**: 同样得 **57**。差异根源 = 3 条 `\b` 开头的
  pattern (`\b(echo|printf|find|ls)…` idx37 / 两条 `\bcp…` idx49,138) 的归键。census 把 `\b` 当
  「停止字面 token 串」→ 3 条各成 EMPTY 单例族; 主 loop 版把 `\b` 剥掉取后随字面 → 两条 `\bcp` 并成
  `cp` 族、`\b(echo|…)` 归 `b` 族 —— **两种约定成员不同, 但家族总数都是 57**。agent 另探一种约定得 56。
- **结论**: 55 这个人工数在**三种**合理归键约定下 (57 / 57 / 56) **无一复现**。不是 census bug,
  是 spec 正文的人工计数错。**28 分支 / 14 零覆盖两个数 census 实跑 MATCH** (spec 同批声明无背书的
  另两个数, 这次对上了), 唯 55 错。
- **下游影响**: SC-19 (TASK-016) 的「补齐至 55 家族全覆盖」完备判据 —— family 若定为 57, 探针集
  规模从 55 变 57 (agent 12 条已覆盖 12 族, 余 43→45 族待补)。**TASK-016 在 owner 裁 55 vs 57 前
  不宜施工** (会返工)。

## 争议 2: `newline_affected.strict` — spec 正文 11, 实跑 13

- **spec 出处**: proposal §6 (行 304-311) 的两基线表 (严格 11/13 · 宽松 13/13); SC-18 (行 865)。
- **census 实跑**: 严格 13/13 · 宽松 13/13 (两基线都 13)。
- **主 loop 独立核验 (数学论证, 非跑脚本)**: 13 处 credit 判据**每一处都含 `[[:space:]]`**, 而 POSIX
  `[[:space:]]` 字符类**含换行符**。故对任一处判据, 都能构造一个含换行的输入, 把该判据的 `[[:space:]]`
  位置放一个换行 → bash `[[ =~ ]]` 整串求值命中 (吃换行) / grep -qE 逐行求值不命中 (换行劈行) ⇒
  **每处判据都「受换行影响」, 机械上必然 13/13**。spec 的「严格 11」依赖一个口径 —— 「只在基线命令
  **已存在的空白字符**位置注入」—— 但 spec 举的基线 `cat x >/dev/null` 只能触发 13 处判据里的**1 处**
  (`>/dev/null` 那处), 拿一条只命中 1 处判据的命令去数「11/13 处判据受影响」, 口径与数字之间没有可机械
  复现的桥。agent 试过最接近的口径 (排除纯 `*` 判据) 得 10, 仍非 11。
- **结论**: 13 在「判据是否可能受换行影响」这一清晰口径下**可证为真**; 11 无可复现口径支撑。同 §6 自己的
  判断: 「这个数被五次尝试给出结果, 根因是数法未固化, 该靠计数器不靠人复述」—— 计数器给出 13。
- **下游影响**: SC-18 断言该数; secret-hygiene.md 回填的是 366 (另一个数, 不受影响)。影响面仅 SC-18
  自身的这一格比对值。

## 主 loop 对两争议的处置 (Rule #10 + SC-18 明文)

1. **不 land 凑数改动** —— 不调 census 实现凑 55/11, 不改 proposal 正文迁就 57/13。两者 spec 明禁。
2. **census 与 hook 改造正交** —— 争议在 spec 正文的**期望值**, 不在 census 或 hook 代码。hook 改造
   (13 正则字节一致 / 47 探针 / 全语料对拍) 与 census 工具本身均经核验成立, 批 1 代码可提交。
3. **SC-18 在 owner 裁前无法变绿** —— 它是 enabled SC, 不自行豁免/改序 (Rule #10)。Phase B 完成度
   卡在此 owner 决策点。
4. **owner 复议请求** (二选一 × 2):
   - family: 采 census 的 **57** (改 proposal 正文 55→57 + 定归键约定) / 还是坚持 55 (须给出能复现
     55 的归键约定)。建议采 57 + 写死「`\b` 视作停止字面 token 串」这条约定 (census 现约定)。
   - newline: 采 census 的 **13** (改 proposal §6 表 11→13, 严格口径并入宽松) / 还是坚持 11 (须给出
     能复现 11 的注入口径定义)。建议采 13 (口径清晰可证)。

## 批 2 追加: 两处 proposal 反事实表描述误差 (owner 复议, 非阻塞)

批 2 (测试族) 落地时, qa-engineer + 主 loop 独立反事实核验各自撞出 proposal 两处反事实表的
**描述精度**误差 —— 不影响 fixture 正确性 (fixture 对真实坏实现有完整鉴别力, 主 loop 已实证),
但 proposal 正文的预测数字/描述需修:

1. **SC-6 反事实表「恒 split」行**: proposal (行 687) 写「恒 split → 15/18 (全部端到端 false 项;
   隔离断言不受影响)」。**实测 16/18** —— 「恒 split」= safe_to_split 完整 stub 恒 return 0, 对**任何**
   输入 (含裸 token `case x in`) 都返回 safe, 故 case 隔离断言 (16/18 项, want degrade) 同样翻红。
   proposal 说它「不受影响」不成立。**修法**: 若 proposal 指的是更窄的「部分 stub」须写明是哪种构造;
   否则该行数字 15→16。主 loop 独立复现确认 16 (counterfactual.sh 恒 split leg)。
2. **SC-1 反事实表「粘性实现」描述**: proposal (§What.3 行 172 / SC-1 反事实) 写「has_filter 不按段
   重置的粘性实现 → 第 2/3/5 条红」。**这是「急切版」粘性** (credit 对每段无条件预算)。另有一种同样
   合理的「最小版」粘性 (credit 仍挂 pattern 命中后才算, 但不重置) → **只红 #3** (Aria#170 本体)。
   两版都是客观不同、都算「粘性」的 naive 实现。**不影响 fixture 正确性**: SC-1 的 5 条对两版合起来
   有完整鉴别力 (#3 抓最小版, #2/#5 抓急切版)。**修法**: proposal 宜注明「3/5」对应急切版, 以免复核者
   拿最小版对不上 3/5 而误判 fixture 有问题。主 loop 实测: 最小版 SC-1 红 1 (#3) / 急切版红 3 (#2/#3/#5)。

这两处与 F-1 / 两个计数争议同族 —— 都是 Phase B 施工 (把设计落成可执行测试) 逼出的 proposal 精度
缺陷。**均不阻塞代码正确性** (批 1+批 2 回归 474/474 全绿, 反事实鉴别力全部主 loop 实证成立), 归
proposal 下一版修订 + owner 过目。

## 附: 批 1 其余状态 (无争议)

- **hook 改造 (TASK-001..007+029)**: 13 处 credit 正则**逐字节一致**; risky_patterns 块**逐字节一致**;
  SC-1/6/9a/14/20/21 探针 **47/47**; safe_to_split 单元 18/19 (1 条是探针 fixture 自身构造冲突,
  非实现错, 见 backend-architect 报告); split_top 10/10。子 shell fail-closed + 每段重置 credit 均落地。
- **既有测试冲突 (第 1 类 0→2 申报变更)**: `secret-guard.test.sh` 的 `put: KNOWN-LIMIT compound
  credit leak` 用例 (want=0) 与 SC-1#3 / Aria#170 形态同文, 改后 exit=2 ⇒ 该用例期望值须由 0 改 2
  (测试作者原就埋了「到时转红强制翻新」的注释)。归 TASK-015 施工时改。
- **census 21/23 MATCH**: 65/49/16/15/1/5 · 13 · 10/12/13 · 141(139+2)/81/79/7/5/1 · 16 · 82 ·
  28/14 全对; 唯 55→57 / 11→13 两处待裁。
