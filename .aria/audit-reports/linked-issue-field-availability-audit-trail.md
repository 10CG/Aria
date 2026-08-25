# linked-issue-field-availability — 审计轨 (append-only)

> **本文件是 `openspec/changes/linked-issue-field-availability/proposal.md` 的审计史与核验证据**, 由主控于 2026-08-25 按
> 姊妹 Spec `linked-issue-normalization` (owner 2026-08-07 裁定「交付面与审计史切开」) 的体例切出。
> **按字节搬运, 未重写任何一句**, 只加了本文件头部与下方节标题 —— 主控搬迁时用程序逐行断言
> 「原内容每一行都 `in` 新文件」, 结果**缺失行 0**。
> **⚠️ 该断言的可证伪性边界 (R3/CR-M-M1 订正)**: 本文件的内容在被搬出前**从未提交过**,
> 因此**不存在可供第三方 diff 的已提交前身** —— 上述无损断言是主控对搬迁**前后工作树**做的,
> 真实但**结构性不可独立复核**。读者若要复核, 只能核对本文件与 proposal 存根所述范围是否自洽。
>
> ⚠️ 本文件 **append-only**, 且**显式不维护与 proposal 的一致性**; 二者不一致时**以 proposal 为准**,
> **不得**因本文件的历史记述而回改 proposal。

---

## §1 实读与重测清单 (2026-08-25 起草时实测, 基线 主仓 `cc1bdef` / aria `d50f9c3`)

> 硬约束「零发明行号」: 本文件出现的每个 `文件:行号` 与每个数字, 要么取自主控说明书的 F-* 表, 要么由本席实跑并在此贴出命令。

| # | 断言 | 来源 / 命令 | 结果 |
|---|---|---|---|
| 1 | **语料终值** 149 / 松谓词 17 文件 37 行 / 严谓词 17 文件 **19 行** / `changes/` 9 / `archive/` 140 | §Why「重测 — 终值」的 7 条命令 (逐字) | 已贴输出。⚠️ **数字是当日观测, 口径(命令)才是规范** —— 语料自修改, 见 §Why 顶部黄框 |
| 2 | 唯一假阳性行 = 母 Spec `:88`, 前缀 `   > > ` | §Why 的 `grep -v` 命令 | 已贴输出 |
| 3 | 14/14 存量字段直喂 `normalize_linked_issue()` = `None` | 本席脚本: `sys.path.insert(0,"aria/skills/state-scanner")` + `from lib.collision import normalize_linked_issue`, 对严谓词命中行的「冒号后 strip 全串」逐条调用 | 14 条全 `None` |
| 4 | 「第一个 code span」坏实现在 **6** 条真实字段上抽出 `confirmed`/`partial-repro` | 同上脚本 + `re.compile(r'`([^`]*)`')` | 已贴 6 条 path:line |
| 5 | **FIX-08 原列 4 条反例的复跑核对** | 逐条实跑 | ① `openspec/changes/linked-issue-normalization/proposal.md:6` → 该目录**已归档**为 `openspec/archive/2026-08-23-linked-issue-normalization/`, 且 `:6` 内容已改为裸 `> **关联 Issue**: 无` (`cat -A` 逐字: `> **M-eM-^EM-3M-hM-^AM-^T Issue**: M-fM-^WM- $`, 行尾无其他内容) ⇒ FIX-08 所述「会抽出 `a1-entry-claim-duplicate-work-guard`」**不复现**, 已弃用该条; ② `archive/2026-07-19-…:14` ✅ 复现 (`confirmed`); ③ `archive/2026-07-22-…:6` ✅ 复现; ④ `archive/2026-07-31-…:6` ✅ 复现。**另新增 3 条** (`2026-06-10-handoff-frontmatter-enforcement:4` / `2026-06-11-audit-drift-guard:5` / `2026-06-11-cross-worktree-handoff-discovery:4`) ⇒ 本 Spec 用 **6 条** |
| 6 | 「只扫头部 N 行」被否决的实证 | 严谓词逐行输出 | 真字段落在 `:61` (`archive/2026-08-16-premerge-gate-branch-existence`) 与 `:45` (`archive/2026-08-16-premerge-gate-mainbranch-failclosed`) |
| 7 | standards 模板无该字段 | `grep -c "关联 Issue" standards/openspec/templates/proposal-minimal.md` | `0` (= F-39) |
| 8 | spec-drafter 目录无该字段 | `grep -rn "关联 Issue" aria/skills/spec-drafter/ \| wc -l` | `0` (= F-40) |
| 9 | spec-drafter 委托 standards 模板 | `sed -n '429p' aria/skills/spec-drafter/SKILL.md` | `- [proposal-minimal 模板](../../../standards/openspec/templates/proposal-minimal.md)` |
| 10 | `.aria/probes` 不在 plugin 分发面 (**该实读仍成立, 但 round-2 后不再承载「check 无法分发」的推论**) | `grep -rn "\.aria/probes" aria/` | 零命中 |
| 10b | **plugin 侧 check 宿主实存 (D3 改判的承重实证)** | `ls -la aria/skills/state-scanner/scripts/issue_cache_freshness_probe.py aria/skills/state-scanner/scripts/coordination_probe.py` | 两文件均存在, **7716** / **11115** bytes; 对应注册行 `.aria/state-checks.yaml:22` / `:235` |
| 10c | plugin 侧两条探针的入参惯例 | `grep -n "sys.argv\|argv\[" <上述两脚本>` | 二者逐字同形: `argv = argv if argv is not None else sys.argv[1:]` (`:148` / `:140`) 与 `repo = Path(argv[0]) if argv else Path.cwd()` (`:149` / `:141`) |
| 10d | `spec-drafter` 无 `scripts/` 目录 | `ls -la aria/skills/spec-drafter/` | 只有 `SKILL.md` / `LEVEL_GUIDE.md` / `LEVEL3_TEMPLATE.md` 三个文件 |
| 10e | 既有 check **无一** 使用 `${CLAUDE_PLUGIN_ROOT}` | `grep -n CLAUDE_PLUGIN_ROOT .aria/state-checks.yaml` | **零命中** ⇒ 采用方可移植写法本轮未验, 已成文不预写 |
| 11 | check 宿主三形态 + 行号 + 条数 | §4 的 `grep -n` 命令 + `grep -c '^  - name:'` + 逐条归类脚本 | 共 **10** 条 = (i) 6 / (ii) 2 / (iii) 2, 已贴 |
| 12 | 先例「项目侧探针 import plugin 侧模块」(**round-1 用它论证形态 iii; round-2 宿主改判后它只作为「跨 skill import 可行」的旁证**) | `grep -n PMG_SCRIPTS .aria/probes/config-template-key-currency.py` | `32:PMG_SCRIPTS = "aria/skills/phase-c-integrator/scripts"` / `60:    sys.path.insert(0, PMG_SCRIPTS)` |
| 12b | **同目录邻居的相反 import 选择及其理由** | `sed -n '76,92p' aria/skills/state-scanner/scripts/coordination_probe.py` | 逐字含「Deliberately NOT `import lib.runtime_probe`: in some test sys.path layouts the top-level name `lib` resolves to state-scanner/lib (Layer L — a DIFFERENT package, claim_schema.py etc.), not scripts/lib」+ `_LIB_DIR = str(Path(__file__).resolve().parent / "lib")` |
| 13 | `normalize_linked_issue` 位置与两 SHA 一致 | `git -C aria show d50f9c3:skills/state-scanner/lib/collision.py \| grep -n "def normalize_linked_issue"` 与 `58a49e7` 同; `git -C aria diff --stat 58a49e7 d50f9c3 -- skills/state-scanner/lib/collision.py` | 两者均 `178:`; diff 为空 |
| 14 | 导入方式的字符级坑 (**round-2 在改判后的宿主目录 `state-scanner/scripts/` 内重跑**) | 在 `aria/skills/state-scanner/scripts/` 下放一个临时脚本, 两种写法各跑一次 (跑完即删, `git status` 已复核工作树无残留) | `sys.path.insert(0, parent.parent)` + `from lib.collision import` ⇒ ✅ 返回 `('aria-plugin', 122)`; `sys.path.insert(0, parent.parent/'lib')` + `from collision import` ⇒ ❌ `ImportError: attempted relative import with no known parent package` (`collision.py:46` 是 `from .claim_schema import ClaimRecord`) |
| 15 | `##SKIP##` 协议 | `grep -rn '##SKIP##' aria/skills/state-scanner/` | `references/state-snapshot-schema.md:583` 逐字「stdout line beginning with `##SKIP##` and exiting 0. **Visible but counted as neither pass nor fail**」 |
| 16 | custom check 的 severity 取值域 | `sed -n '574p'` 一带 `references/state-snapshot-schema.md` | `severity: str,  # "info" \| "warning" \| "error"` |
| 17 | `state-checks.yaml` 由确定性代码读取, 非 AI 指令面 | `grep -rn "state-checks.yaml" aria/skills/` | 消费者 = `scripts/collectors/custom_checks.py:399`; `state-scanner/SKILL.md:119` 仅记为「Opt-in 子阶段」的存在条件 |
| 18 | `spec-drafter.json` AB 套件 2 evals | `python3 -c` 读该 JSON 的 `evals` | `n=2`; id 1「判断规范等级」/ id 2「双语输入处理」 (与 F-38 一致) |
| 19 | §3 规则原型在真实语料上的判定 (**终值**) | 本席原型脚本跑 `openspec/changes/**` / `openspec/archive/**` / 全语料 | `changes/` **9 份**: **3 OK** (母 Spec `:12` / 本文件 `:6` / 探针 Spec `:6`) **+ 6 NO_FIELD**; `archive/` 140 份: **126 NO_FIELD + 14 NO_TOKEN + 0 OK**; 全语料 149: **132 / 14 / 3** |
| 20 | **10 份对抗夹具的拒绝能力** | 本席原型脚本跑合成夹具 | 合规→OK · markdown 链接→NO_TOKEN · `` `无` ``→OK(省参) · 裸 `无`→NO_TOKEN · 多值→OK(首元素 `10CG/a#1`) · 混合→BAD_TOKEN(点名 `[b](url)`) · 仅 fence 内→NO_FIELD · depth-2→NO_FIELD · 真字段+fence 内示例→OK(取真字段) · **blockquote 内围栏 (`j-bq-fence`)→加 `(?:> ?)?` 前 OK(假阳), 加后 NO_FIELD** |
| 21 | fence 谓词两变体在真实语料上的等价性 | 本席对**全语料逐份**跑 **不含**与**含** `(?:> ?)?` 前缀的两版 fence 谓词 (逐字见 §3 E0 谓词 2) 并 diff, **147 份 (round-1) 与 149 份 (round-2 终值) 各跑一次** | **两次差异数均 = 0** ⇒ 加 `(?:> ?)?` 对存量零影响, 只多堵一类合成假阳性 (夹具 `j-bq-fence`: 不含 ⇒ `OK`(假阳) / 含 ⇒ `NO_FIELD`) |
| 22 | minimal YAML parser 的窄性自陈 | `sed -n '61,64p;119,126p' aria/skills/state-scanner/scripts/collectors/custom_checks.py` | `:63` 逐字 `# Minimal YAML parser — strictly scoped to state-checks.yaml shape.`; `:122-123` 逐字 `Raises ValueError on any structural issue. This is a narrow parser — it / intentionally rejects YAML features outside the documented schema.` |
| 23 | **本文件自校 (dogfood)** | 用 §3 规则原型跑本文件 | `OK` @ `:6`, token 串 `无` ⇒ 本 Spec 自己过自己的 check; 文件内 §3/§4/§5 的全部字段示例均在围栏内或深度 ≥2, 对本文件零命中 |
| 24 | **探针 Spec 已自行 dogfood** | `grep -nE '^> \*\*关联 Issue\*\*:' openspec/changes/sibling-spec-probe/proposal.md` | `6:> **关联 Issue**: \`无\` — 本 Spec 由母 Spec 的 owner 裁定 (2026-08-23 方向 b「缩 scope」) 拆出, 无独立 issue 号。…` ⇒ 过 E0/E2/E5, 判 `OK` |
| 25 | **与探针 Spec 的术语逐条比对** | 实读 `openspec/changes/sibling-spec-probe/proposal.md` 的 `:85` (层 0 定位) / `:100`(层 1 三态契约) / `:103`(canonical 合规 0 行) / `:107-109`(`无` 层 1.5) / `:116-120`(URL 回落触发条件与作用域分离) / `:262`(`own_layer` 枚举) / `:509`(自陈未交叉核对) | 定位规则/`无`/`NO_TOKEN`/`NO_FIELD` **语义一致**; 本 Spec 多一条**围栏排除**谓词 (当前无实际分叉); **唯一实质差异 = `BAD_TOKEN` 在其三态契约里无归宿** —— 已在 §3「术语对齐」块给出建议映射并标注归属由主控协调 |
| 26 | 探针 Spec 的计数与本 Spec 不同源 | 对比其 §实读清单 #14/#16 与本 Spec §Why | 其 `147 / 严 14 行 / no_field 133` 测的是 **committed `cc1bdef`**; 本 Spec `149 / 严 19 行 / NO_FIELD 132` 测的是**当前工作树**, 且分层法不同 ⇒ **总体/范围/计数法三项全不同, 不可比** (memory `critique-repeats-error`), 已在 §Why 成文 |

---

