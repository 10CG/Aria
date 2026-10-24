import re
prop=open('/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md',encoding='utf-8').read().split('\n')
def cells(l): return [c.strip() for c in l.strip().strip('|').split('|')]
sc={}; bi={}
for l in prop:
    if l.startswith('| SC-V'):
        c=cells(l); sc[c[0]]=(c[1],c[2],c[3])
    if l.startswith('| BI-'):
        c=cells(l); bi[c[0]]=(c[1],c[2],c[3],c[4])
def members(cell):
    """expand a case cell into a list of (prefix,num,suffix) selectors and exact tokens"""
    toks=[]
    for m in re.finditer(r'`(V\d+-[A-Z])(\d+)([a-z]?)`(?:–`(V\d+-[A-Z])(\d+)([a-z]?)`)?',cell):
        p,n,s,p2,n2,s2=m.groups()
        if p2: toks.append(('range',p,int(n),s,int(n2),s2))
        else: toks.append(('one',p,int(n),s))
    return toks
def covers(toks,case):
    m=re.match(r'(V\d+-[A-Z])(\d+)([a-z]?)',case); p,n,s=m.group(1),int(m.group(2)),m.group(3)
    for t in toks:
        if t[0]=='one' and t[1]==p and t[2]==n and (t[3]==s): return True
        if t[0]=='range' and t[1]==p:
            lo,hi=t[2],t[4]
            if lo<=n<=hi:
                # suffix bounds only matter at the ends
                if n==lo and s<t[3]: continue
                if n==hi and t[5] and s>t[5]: continue
                return True
    return False
# SC cells contain things like V1-E16-* handled by regex 'V1-E16'
for k,(prop_,cases,bis) in sc.items():
    toks=members(cases)
    # also treat literal  `V1-E16-*`
    star=re.findall(r'`(V\d+-[A-Z]\d+)-\*`',cases)
    for b in re.findall(r'BI-\d+',bis):
        des=re.findall(r'`([^`]+)`',bi[b][1])
        un=[d for d in des if not covers(toks,d) and not any(d.startswith(s) for s in star)]
        print(f'{k} requires {b}: designated {len(des)}; NOT inside the SC row case list: {un}')
