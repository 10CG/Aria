#!/usr/bin/env python3
"""handoff / 派生文档「当前态陈述」陈旧扫描 (PR #190 pre_merge 审计 R3/R4 教训: 同一事实在 handoff /
latest.md / proposal / tasks.md / yaml / PR body 多处复述, 逐轮修实例必残余; memory `fix-the-class` /
`no-code-host-no-assertion`).

用法 (主仓根):
  python3 .aria/repro/handoff-current-state-scan.py <handoff.md> [--pr 190] [--extra file ...]
判据: 逐行找 STALE (推送授权类 / 轮次进度类 / 旧版本·计数类 token) 命中; 每个命中再看它**所在的
  子句**是否被 HIST_OK_NEAR (历史记述短语) 豁免, 或整行是否被 HIST_OK_LINE (结构性行: 时间线表行 /
  标题 / latest.md 更新段) 豁免。二者皆不命中 ⇒ 残余, 打印 `<file>:<line>: <text>`。
exit: 0 = 扫完且零残余 · 1 = 有残余 · 2 = **未能完成扫描** (文件不可读 / `--pr` 取不到 body) —— 后者
  绝不打印 `residual = 0`, 「没扫成」不得被读成「零残余」。

fail-CLOSED 的三处 (2026-09-04, PR #190 pre_merge R5 findings d61b5fc9 / d711ce91 清账):
  (i) **子句级豁免**: 旧版 HIST_OK 按整行求值 —— 同一行里任意一个无关的白名单词 (`已完成` /
      `已推` / `aggregated` …) 会把该行的 STALE 命中一起豁免。R5 的三条合成对抗输入全部被吞,
      且 R4 写进派生文档的指针短语本身含 `aggregated`, 使那批最易陈旧的行**结构上永不可扫**。
      现改为: 短语类白名单只在**命中所在子句**内求值 (子句按 `;；,，。` 切), 结构性白名单仍按整行。
  (ii) **STALE 补 R5–R9 族**: 旧版正向枚举只到 R4, 对 R5 期措辞天然 fail-OPEN。
  (iii) **`--pr` 不可读 ⇒ exit 2**: 旧版只打一行 stderr 仍 exit 0 + `residual = 0`。
另: frontmatter `status` 已收口 (done/superseded/abandoned) 或 Status 行以 Superseded 起首的文档
  **整份跳过**并在 stderr 打印一行 —— 历史记述里的「当前态」是写下时的当前态, 不是今天的陈旧。
自测: `python3 .aria/repro/test_handoff_current_state_scan.py` (含 R5 点名的三条对抗输入)。
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, pathlib

STALE = re.compile(
    r"未推|推送授权|待授权|待 owner merge|待 owner 一句"          # 推送授权类
    r"|R1/R2 已清账|R3/R4|R3 \(\+R4\)|R1–R3 已清账|R[1-9] 稳定性确认|R[1-9] 待"  # 轮次进度类 (派生文档不得写轮次数字)
    r"|R[5-9]/R[5-9]|R[5-9] 清账|max_rounds 最后一轮"            # (ii) R5–R9 族: 旧版枚举只到 R4, 对 R5 期措辞 fail-OPEN
    r"|22/25|48/48|\b1457\b|\b1889\b|48 条 RED|1\.68\.0|fe32441|fad8b4b"      # 旧版本 / 计数类
)

# (i) 白名单拆两半 —— 这是本工具唯一的 fail-OPEN 面, 拆开是为了让它的作用域可被说清:
#   HIST_OK_LINE: **结构性**行 (整行就是历史记述: 时间线表行 / 含轮次的标题 / latest.md 更新段)。
#                 按整行求值是对的 —— 这类行的身份由行首形态决定, 与 STALE 命中位置无关。
#   HIST_OK_NEAR: **短语级**历史标记, 只在 STALE 命中所在的子句内求值。放宽到整行就是 d711ce91:
#                 「H1 四处推送已完成; …R3/R4 稳定性确认后合并」里的 `已完成` 会把后半句的真陈旧一起赦免。
HIST_OK_LINE = re.compile(
    r"^\| (0[678]:|1[0-9]:)"                                  # §1 时间线表行 (历史)
    r"|^\| \*\*H[0-9]"                                           # §2「高优先级 (owner 动作门)」表行:
    # 这类行的**本职**就是记「还没做、等 owner」的动作, 说「待授权」是它的正确内容而非陈旧。
    # 风险 (成文): 一条真陈旧的 H 行不会被抓到。补偿控制 = 本 cycle 一收尾, 该 doc 的
    # frontmatter status 收口为 done ⇒ 整份走上面的历史文档跳过, 不再有人把它读成当前态。
    r"|^#+ .*(R1|R2|R3|R4|R5) "                                # 含轮次的小节标题 = 历史章节
    r"|^> \*\*2026-0[0-9]-[0-9]{2} (更新|补记|会话收尾)"        # latest.md 历史更新段
)
HIST_OK_NEAR = re.compile(
    r"前一|原文保留|历史|亦在两端|→ v1\.68\.1|→ 清账|v1\.68\.0 → |ab-results/2026-09-0[0-9]-v1\.68\.0"
    r"|1\.68\.0 `fe32441` 亦|\(fe32441\)|R1 清账|前一 fe32441|前一 fad8b4b|d1caa66 ⊇ fe32441|两 tag"
    r"|tag v1\.68\.0 / standards `fad8b4b` / 主仓 PR #190|aria `fe32441`\+tag v1\.68\.0|1\.68\.0 \+ 1\.68\.1|1\.68\.0\]"
    r"|已推|类推自授权|以「通过后合并」|推送授权已于|不再推|B9-补|\(R[1-5]\)|R[1-5] [a-z-]+ (major|minor)|第[三四五]轮"
    r"|aggregated|决策单 [BCD][0-9]"
    r"|<vNEXT>|占位|外向, 待授权|均已双推|Tags published"
    # ⚠️ 刻意**不收**「已完成」「已推送」「已 ship」这类泛词: 它们与任意 STALE 命中同行的
    # 概率极高, 收进来等于把 d711ce91 的整行赦免换个写法复活 (第 3 条对抗输入
    #「H1 (a)-(d) 已完成, R4 稳定性确认」就是靠它被吞的)。
)

# 子句分隔: 中英文分号 / 逗号 / 句号。跨子句的白名单词不再赦免本子句的 STALE 命中。
_CLAUSE_SEP = re.compile(r"[;；,，。]")
NEAR_WINDOW = 8      # 子句之外再给一个 ±8 字符窗口, 容纳自身含逗号的白名单短语


def _near_scopes(line: str, start: int, end: int) -> tuple[str, str]:
    """STALE 命中的两个豁免作用域, 命中任一即豁免。

    - **子句**: 按 `;；,，。` 切出命中所在的一段。它挡住 d711ce91 那类「无关白名单词与
      真陈旧同行但不同子句」。
    - **±8 字符窗口**: 因为白名单短语**自己可能含子句分隔符** (如「外向, 待授权」——
      按逗号切会把它劈成两半, 于是它永远匹配不到自己)。窗口小到不会把邻近子句整段带进来。
    两者是 OR: 子句挡跨子句的误赦免, 窗口保住含分隔符的合法短语。
    """
    left = 0
    for m in _CLAUSE_SEP.finditer(line, 0, start):
        left = m.end()
    right_m = _CLAUSE_SEP.search(line, end)
    right = right_m.start() if right_m else len(line)
    clause = line[left:right]
    window = line[max(0, start - NEAR_WINDOW):min(len(line), end + NEAR_WINDOW)]
    return clause, window


# 历史文档整份跳过 (2026-09-04): frontmatter `status:` 已收口为 done/superseded/abandoned,
# 或 prose Status 行以 Superseded 起首 ⇒ 该文档是**历史记述**, 里面的「当前态」按定义就是
# 写下时的当前态, 不该被当作今天的陈旧。跳过时打印一行说明 —— 「跳过」必须可见, 不静默
# (否则又是一个把「没扫」读成「零残余」的面)。
_HISTORICAL_FM = re.compile(r"^status:\s*(done|superseded|abandoned)\s*$", re.M)
_HISTORICAL_PROSE = re.compile(r"^> \*\*Status\*\*:\s*Superseded", re.M)


def is_historical(text: str) -> bool:
    head = text[:4000]
    return bool(_HISTORICAL_FM.search(head) or _HISTORICAL_PROSE.search(head))


def scan_text(name: str, text: str) -> list[tuple[str, int, str]]:
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        if HIST_OK_LINE.search(line):
            continue                                  # 结构性历史行, 整行豁免
        for m in STALE.finditer(line):
            clause, window = _near_scopes(line, m.start(), m.end())
            if HIST_OK_NEAR.search(clause) or HIST_OK_NEAR.search(window):
                continue                              # 同子句 / 紧邻窗口内有历史标记 ⇒ 该命中豁免
            out.append((name, i, line.strip()[:170]))
            break                                     # 一行最多报一次
    return out

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("handoff"); ap.add_argument("--pr", type=int); ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args(argv)
    residual = []
    for f in [a.handoff, *a.extra]:
        try:
            text = pathlib.Path(f).read_text(encoding="utf-8")
        except OSError as exc:  # (iii) 读不到 = 没扫成, 不是「零残余」
            print(f"扫描未完成: {f} 不可读: {exc.__class__.__name__}", file=sys.stderr)
            return 2
        if is_historical(text):
            print(f"跳过 (历史文档: status=done/superseded): {f}", file=sys.stderr)
            continue
        residual += scan_text(f, text)
    if a.pr:
        r = subprocess.run(["forgejo", "GET", f"/repos/10CG/Aria/pulls/{a.pr}"], capture_output=True, text=True)
        try:
            body = json.loads(r.stdout)["body"]
        except Exception as exc:  # noqa: BLE001 — (iii) 同上: 取不到 body ⇒ exit 2, 不打 residual
            print(f"扫描未完成: PR#{a.pr} body 不可读: {exc}", file=sys.stderr)
            return 2
        residual += scan_text(f"PR#{a.pr}/body", body)
    for name, i, line in residual:
        print(f"{name}:{i}: {line}")
    print(f"residual = {len(residual)}")
    return 1 if residual else 0

if __name__ == "__main__":
    sys.exit(main())
