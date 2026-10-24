#!/usr/bin/env python3
"""w14-shapes.py <shape> <out file> | --list      (TASK-003 second segment, 10CG/aria-plugin#217)

Adversarial command shapes aimed at the COST OF THE RELAXED RERUN of the secret-guard hook: a substituted copy over 8192 characters is judged in full by a
background job under a hard deadline (hook start + 3 s). Inputs only; no credential VALUES; credential-shaped PATHS are assembled at run time (the convention of
v3/gen-v3.py). The limits below are mirrored from the hook only to size the inputs: SMAX 8192 (one copy), LMAX 8192 (longest line of a big copy: longer = rows
only), GMAX 8192 (growth over the input), VMAX 4096 (one value), TMAX 65536 (all copies of one command), and in the baseline pass 16 assignments / 8 for-lists /
8 replacements per variable (none of the three counts bounds the rerun).
--list prints "<shape><TAB><source><TAB><what it is meant to test>" for every shape of the matrix: the 8 of v3/gen-v3.py first (source gen-v3), then these (w14)."""
import re
import sys

DOT = "."
CRED = "~/" + DOT + "aw" + "s/cred" + "entials"
SMAX = LMAX = GMAX = 8192
VMAX = 4096
TMAX = 65536


def expand(raw, vals):
    """the text after substitution of $NAME (followed by a non-identifier character or the end), in dict order"""
    s = raw
    for k, v in vals.items():
        s = re.sub(r"\$" + k + r"(?![A-Za-z0-9_])", lambda m, v=v: v, s)
    return s


def cat_line(lensub, fill="x", var="C"):
    """raw line 'cat $C | wc -c <fill...>' whose copy (the reference replaced by the path) is exactly lensub characters long"""
    head = "cat $" + var + " | wc -c "
    n = lensub - len(head) - (len(CRED) - 1 - len(var))
    assert n > 0
    return head + fill * n


def multiline(lines):
    """whole mode (the leading subshell), the path only in an assignment on the first line"""
    return "(true); C=" + CRED + "\n" + "\n".join(lines)


def head_trigger(xlen=2000, nref=4, filler=150):
    """a segment whose copy is over SMAX only after substitution (growth 7992, under GMAX): the baseline stops here, the rerun judges it"""
    return "x=" + "x" * xlen + "; echo " + " ".join(["$x"] * nref) + " y" * filler


def storm(n):
    return " ".join("a%04d=1" % i for i in range(n)) + " true"


def cat_line_bytes(nbytes, var="C"):
    """raw line whose copy is exactly nbytes BYTES long in UTF-8 (3-byte CJK characters, ASCII x for the remainder): in the C locale that is nbytes characters"""
    head = "cat $" + var + " | wc -c "
    room = nbytes - (len(head) + len(CRED) - 1 - len(var))
    k, r = divmod(room, 3)
    return head + "说" * k + "x" * r


def s_multiline_cred():
    return multiline([cat_line(7900) for _ in range(8)])


def s_lmax_below():
    return multiline([cat_line(LMAX) for _ in range(3)])


def s_lmax_above():
    return multiline([cat_line(LMAX + 1)] + [cat_line(LMAX) for _ in range(2)])


def s_cjk_lines_lmax():
    return multiline([cat_line(LMAX, fill="说") for _ in range(3)])


def s_cjk_bytes_lmax():
    return multiline([cat_line_bytes(LMAX) for _ in range(3)])


def gmax(target):
    x = "x" * 4096

    def build(ylen):
        lines = ["cat $C | wc -c $x", "cat $C | wc -c $y"] + [cat_line(3000) for _ in range(4)]
        return "(true); C=" + CRED + "; x=" + x + "; y=" + "y" * ylen + "\n" + "\n".join(lines)

    def growth(ylen):
        raw = build(ylen)
        return len(expand(raw, {"C": CRED, "x": x, "y": "y" * ylen})) - len(raw)

    ylen = 1000 + (target - growth(1000))
    assert 1 <= ylen <= VMAX and growth(ylen) == target, (ylen, growth(ylen))
    return build(ylen)


def s_lmax_race():
    return multiline([cat_line(LMAX) for _ in range(3)] + [cat_line(4000)])


def s_gmax_exact():
    return gmax(GMAX)


def s_gmax_over():
    return gmax(GMAX + 1)


def s_assign_storm():
    return "(true); " + head_trigger() + "; " + storm(3000)


def s_forlist_storm(n=250, words=20):
    loops = "; ".join("for i%03d in %s; do :; done" % (k, " ".join("w%03d_%02d" % (k, j) for j in range(words))) for k in range(n))
    return "(true); " + head_trigger() + "; " + loops


def s_repl_storm(n=15000):
    return "(true); x=a; echo " + " ".join(["$x"] * n)


def s_repl_storm_cjk(n=6000):
    return "(true); x=a; echo " + " ".join(["$x 说明"] * n)


def late(k, padlen=8100, nstorm=0):
    """whole mode (the splitter bails out at once): the first pass is the credit computation of k raw lines that read the path literally (~0.9 s per line of 8192
    characters, quadratic in the length), then a variable reference makes the copy over SMAX: the rerun begins at about k x 0.9 s. A line of 8192 characters or less is
    computed again by the rerun (deadline path), a longer one goes to the rows-only path of the rerun (fast)"""
    lines = ["cat " + CRED + " | wc -c " + "x" * padlen for _ in range(k)]
    return "(true); x=1; echo $x" + ("; " + storm(nstorm) if nstorm else "") + "\n" + "\n".join(lines)


def s_late_core2():
    return late(2)


def s_late_core3():
    return late(3)


def s_late_long3():
    return late(3, 8400)


def s_late_core4():
    return late(4, 7120)


def s_late_near3():
    return late(3, 8580)


def s_late_core2_storm():
    return late(2, nstorm=1500)


def s_caps_old_limits():
    x = "x" * 600
    assigns = "x=" + x + "; " + "; ".join("a%02d=1" % i for i in range(2, 17)) + "; C=" + CRED     # C is the 17th assignment (the baseline collects 16)
    loops = "; ".join("for f%d in p q; do :; done" % i for i in range(1, 10))                         # 9 for-lists (the baseline takes 8)
    return "(true); " + assigns + "; " + loops + "\necho " + " ".join(["$x"] * 9) + "\n" + cat_line(8100) + "\n" + cat_line(8100)   # 9 references (the baseline replaces 8)


def s_seg_assign(n=1700):
    return head_trigger() + "; " + storm(n)


def s_seg_late2():
    return "; ".join(["cat " + CRED + " | wc -c " + "x" * 8100 for _ in range(2)]) + "; " + head_trigger()


def s_many_segs(n=120):
    return "v=a; " + "; ".join(["echo $v"] * n) + "; " + head_trigger()


def s_degrade_late(n=120):
    return head_trigger() + "; v=abc; " + "; ".join(["echo $v 说明"] * n) + "; (true)"


def big_segs(n):
    return "x=" + "x" * 2000 + "; " + "; ".join(["echo $x $x $x $x" + " y" * 150] * n)


def s_multi_big_seg():
    return big_segs(7)


def s_tmax_edge():
    return big_segs(8)


def s_heredoc_vars():
    lines = ["entry %04d: path=$D/file%04d name=$N value=%s" % (i, i, "v" * 70) for i in range(250)]
    return "D=/srv/app/data; N=" + "n" * 20 + "\ncat > /tmp/gen.conf <<EOF\n" + "\n".join(lines) + "\nEOF\n"


GEN_V3 = [
    ("apply-heavy", "whole mode (leading subshell), 60 KB: 16 variables x 16 references, the reference block twice; apply cost of the rerun, which has no count bound"),
    ("apply-heavy-seg", "the same without the subshell: segment mode, one 60 KB segment"),
    ("apply-heavy-cjk", "multibyte filler (characters != bytes) around the same reference block: string operations cost more per character"),
    ("shrink", "two 600-character variable names referenced 8 times each (copies shrink), a source read after them"),
    ("segfinding", "4000-character value referenced twice, 12 filler lines, a source read last: a finding that is found late"),
    ("f5like", "a relaxable big segment followed by three expensive small segments (credit ~1 s each): the rerun runs into the deadline"),
    ("km-ext", "24000-character line inside a subshell, run WITHOUT a project extension (the relaxation is in effect)"),
    ("km-ext-small", "the 100-character sibling of km-ext (control)"),
]

SHAPES = [
    ("lmax-below", s_lmax_below, "whole mode, 3 lines of exactly 8192 characters (= _SGV_LMAX, the credit path, ~0.9 s per line)"),
    ("lmax-race", s_lmax_race, "lmax-below plus a fourth credit line of 4000 characters: the rerun needs about as long as the deadline leaves (~2.9 s of 3.0 s), so some runs finish and some are killed"),
    ("lmax-above", s_lmax_above, "like lmax-below but the first line has 8193 characters: the rows-only path (longline text), should be fast"),
    ("gmax-exact", s_gmax_exact, "growth over the input exactly 8192 (= _SGV_GMAX), whole mode: the largest copy the rerun accepts, judged in full"),
    ("gmax-over", s_gmax_over, "growth 8193 (limit + 1): the growth text without any judgement, should be fast"),
    ("caps-old-limits", s_caps_old_limits, "just past the old counts: the 17th assignment holds the path, 9 for-lists, 9 references to one variable; two 8100-character credit lines"),
    ("multiline-cred", s_multiline_cred, "whole mode, 8 lines of 7900 characters, each reads the credential-shaped path through $C only after substitution: eight credit computations under one deadline"),
    ("assign-storm", s_assign_storm, "whole mode, a trigger segment, then 3000 assignments: the baseline collects 16, the rerun collects all (regex per assignment, O(n^2) de-duplication)"),
    ("forlist-storm", s_forlist_storm, "whole mode, a trigger segment, then 250 for-lists of 20 words: the baseline takes 8, the rerun all; O(vars^2) chaining on 140-character values"),
    ("repl-storm", s_repl_storm, "whole mode, one 45 KB command with 15000 references to one variable: the baseline stops at the first replacement, the rerun replaces them all"),
    ("repl-storm-cjk", s_repl_storm_cjk, "the same with CJK words between 6000 references (UTF-8: every offset computation scans characters)"),
    ("cjk-lines-lmax", s_cjk_lines_lmax, "whole mode, 3 lines of exactly 8192 CJK characters (24.5 KB each in bytes): characters != bytes at the LMAX edge"),
    ("cjk-bytes-lmax", s_cjk_bytes_lmax, "whole mode, 3 lines of exactly 8192 BYTES of CJK text (2730 characters each): small in UTF-8, the LMAX edge in the C locale"),
    ("late-core2", s_late_core2, "trigger point late: two raw lines of 8131 characters with a literal source read (credit ~0.9 s each) come before the oversize copy; the rerun repeats them"),
    ("late-core3", s_late_core3, "the same with three lines: the first pass takes ~2.6 s, the rerun starts with little time left and runs into the deadline"),
    ("late-core4", s_late_core4, "four raw lines of 7151 characters: the first pass takes ~2.9 s, so the rerun begins with about 0.1 s left and repeats the credit lines"),
    ("late-near3", s_late_near3, "three raw lines of 8611 characters (over LMAX): the first pass ends at ~2.9 s, right at the deadline: the rerun begins with almost no time left, or not at all"),
    ("late-long3", s_late_long3, "three raw lines of 8431 characters (over LMAX): slow first pass, but the rerun takes the rows-only path (fast), so the rerun begins late and ends at once"),
    ("late-core2-storm", s_late_core2_storm, "late-core2 plus a 1500-assignment storm: the rerun has to collect the storm and repeat the credit lines"),
    ("seg-assign-1700", s_seg_assign, "segment mode (no subshell), a trigger segment, then 1700 assignments: the baseline first pass alone takes ~6 s (10CG/aria-plugin#228), no rerun"),
    ("seg-late2", s_seg_late2, "segment-mode twin of late-core2: the baseline first pass takes ~10 s (10CG/aria-plugin#228), no rerun"),
    ("many-segs", s_many_segs, "120 tiny reference segments before the oversize copy (segment mode): the first pass and the rerun both walk all of them"),
    ("degrade-late", s_degrade_late, "120 CJK reference segments, the subshell that forces whole mode only at the very end (whole and segment handling mixed)"),
    ("multi-big-seg", s_multi_big_seg, "7 segments, each 8308 characters after substitution (each could enter a rerun), 58 KB together = under _SGV_TMAX"),
    ("tmax-edge", s_tmax_edge, "8 such segments: 66 KB together, the rerun reaches _SGV_TMAX at the 8th"),
    ("heredoc-vars", s_heredoc_vars, "realistic: a 30 KB unquoted heredoc with two variable references per line, growth 7250 (under the limit), no secret source"),
]

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        for n, d in GEN_V3:
            print("%s\tgen-v3\t%s" % (n, d))
        for n, f, d in SHAPES:
            print("%s\tw14\t%s" % (n, d))
        sys.exit(0)
    if len(sys.argv) != 3:
        raise SystemExit("usage: w14-shapes.py <shape> <out file> | --list")
    name, out = sys.argv[1], sys.argv[2]
    m = re.fullmatch(r"late:(\d+):(\d+)", name)          # free-form, for sizing only (not in --list)
    if m:
        text = late(int(m.group(1)), int(m.group(2)))
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(name, len(text))
        sys.exit(0)
    for n, f, d in SHAPES:
        if n == name:
            text = f()
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(name, len(text))
            sys.exit(0)
    raise SystemExit("unknown shape " + name)
