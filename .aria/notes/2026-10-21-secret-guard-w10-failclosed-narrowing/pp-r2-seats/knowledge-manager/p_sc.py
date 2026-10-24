import re
prop=open('/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md',encoding='utf-8').read().split('\n')
ids=[l.split()[1] for l in open('/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/knowledge-manager/sc-proto.out') if l[:5] in('PASS ','FAIL ')]
def cells(l): return [c.strip() for c in l.strip().strip('|').split('|')]
P={};SC={}
for l in prop:
    if re.match(r'\| P\d+ \|',l): c=cells(l); P[c[0]]=c[2]
    if l.startswith('| SC-V'): c=cells(l); SC[c[0]]=c[2]
def expand(cell):
    out=set()
    for m in re.finditer(r'`(V\d+-[A-Z])(\d+)([a-z]?)(?:-\*)?`(?:–`(V\d+-[A-Z])(\d+)([a-z]?)`)?',cell):
        p,n,s,p2,n2,s2=m.groups()
        if p2:
            for i in ids:
                mm=re.match(r'(V\d+-[A-Z])(\d+)([a-z]?)',i)
                if mm.group(1)==p and int(n)<=int(mm.group(2))<=int(n2):
                    if int(mm.group(2))==int(n) and mm.group(3)<s: continue
                    if int(mm.group(2))==int(n2) and s2 and mm.group(3)>s2: continue
                    out.add(i)
        else:
            for i in ids:
                mm=re.match(r'(V\d+-[A-Z])(\d+)([a-z]?)',i)
                if mm.group(1)==p and int(mm.group(2))==int(n) and mm.group(3)==s: out.add(i)
    return out
for k in range(1,11):
    a=expand(P[f'P{k}']); b=expand(SC[f'SC-V{k}'])
    # P-table V2-G* wildcard
    if 'V2-G*' in P[f'P{k}']: a|={i for i in ids if i.startswith('V2-G')}
    print(f'P{k} vs SC-V{k}: only in P: {sorted(x.split("-")[0]+"-"+x.split("-")[1] for x in a-b)} only in SC: {sorted(x.split("-")[0]+"-"+x.split("-")[1] for x in b-a)}')
