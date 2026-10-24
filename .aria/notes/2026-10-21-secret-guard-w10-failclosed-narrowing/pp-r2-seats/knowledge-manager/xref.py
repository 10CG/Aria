import re,sys
S=sys.argv[1]
prop=open('/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md',encoding='utf-8').read()
tasks=open('/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml',encoding='utf-8').read()
disp=open('/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/dispositions.md',encoding='utf-8').read()
ids=[l.split()[1] for l in open(S+'/sc-proto.out') if l[:5] in('PASS ','FAIL ')]
print('cases emitted:',len(ids))
# prefix-normalised: case id forms like V2-G2-platform:x86...:5.0 -> V2-G2
short=lambda i: re.match(r'(V\d+-[A-Z]\d+[a-z]?)',i).group(1)
emitted={short(i) for i in ids}
print('distinct short ids:',len(emitted))
def expand(tok):
    # expand ranges like V2-G1–V2-G11, V4-S6–V4-S8, V5-S10–V5-S10d, V8-D1–V8-D3, V10-N1–V10-N4, V9-E10–V9-E12, V3-E3–V3-E5, V7-E13–V7-E15, V2-E6–V2-E9, V4-S1–V4-S3
    return tok
cited=set(re.findall(r'`(V\d+-[A-Z]\d+[a-z]?)(?:-[^`]*)?`',prop))
# ranges "`A`–`B`"
rng=re.findall(r'`(V\d+-[A-Z])(\d+)([a-z]?)`–`(V\d+-[A-Z])(\d+)([a-z]?)`',prop)
print('ranges:',len(rng))
missing=set()
for p1,n1,s1,p2,n2,s2 in rng:
    assert p1==p2,(p1,p2)
    for n in range(int(n1),int(n2)+1):
        for suf in ['']+list('abcd'):
            pass
    # check each integer in range exists as some emitted id with that number
    for n in range(int(n1),int(n2)+1):
        base=f'{p1}{n}'
        if not any(e==base or (e.startswith(base) and e[len(base):].isalpha()) for e in emitted):
            missing.add(base)
print('range members with no emitted case:',sorted(missing))
print('cited singles not emitted:',sorted(c for c in cited if not any(e==c or e.startswith(c) for e in emitted)))
print('emitted not cited anywhere in proposal:',sorted(e for e in emitted if not (any(e==c or c==e for c in cited) or any(e.startswith(f'{p1}') and False for p1,_,_,_,_,_ in rng))))
