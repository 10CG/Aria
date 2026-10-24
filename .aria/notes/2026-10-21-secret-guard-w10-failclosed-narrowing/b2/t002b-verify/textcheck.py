# main-loop textcheck: the longline expectation in sc-direct.sh vs the What 5 code block of proposal.md, and vs the heredoc of the implementation hook
import re, sys
R = '/home/dev/Aria/'
prop = open(R + 'openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md', encoding='utf-8').read()
w5 = prop.split('### 5. 文案（逐字）', 1)[1].split('### 6.', 1)[0]
blk = re.search(r'\n```\n(.*?)\n```\n', w5, re.S).group(1) + '\n'
sd = open(R + '.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-direct.sh', encoding='utf-8').read()
exp = re.search(r'cat > "\$X/ll-want" <<EOF\n(.*?\n)EOF\n', sd, re.S).group(1)
hook = open(sys.argv[1], encoding='utf-8').read()
hd = re.search(r'if \[\[ "\$kind" == longline \]\]; then\n    cat >&2 <<EOF\n(.*?\n)EOF\n', hook, re.S).group(1)
def norm_prop(t):   # the proposal / hook template with its three parameters named as sc-direct.sh fills them
    return t.replace('${_SGV_LMAX}', '$L').replace('$pat', 'PAT-X').replace('$(_sg_redact_echo "${command:0:200}")', 'cat /tmp/sc-x')
for name, t in (('proposal What 5 block', blk), ('implementation heredoc', hd)):
    n = norm_prop(t)
    print(f'{name:24s} vs sc-direct expectation: {"IDENTICAL" if n == exp else "DIFFERENT"} ({len(n.encode())} / {len(exp.encode())} bytes, {n.count(chr(10))} lines)')
print('proposal block vs implementation heredoc (raw):', 'IDENTICAL' if blk == hd else 'DIFFERENT')
