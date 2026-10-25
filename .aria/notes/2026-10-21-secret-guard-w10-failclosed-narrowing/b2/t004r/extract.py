import sys, re, textwrap
C='/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/'
out=open(sys.argv[1],'w')
def W(s):
    for line in str(s).split('\n'):
        out.write('\n'.join(textwrap.wrap(line, 260, drop_whitespace=False) or [''])+'\n')
try:
    import yaml
    d=yaml.safe_load(open(C+'detailed-tasks.yaml'))
except Exception as e:
    W('YAMLFAIL %r'%e); d=None
def walk(o, want, acc):
    if isinstance(o, dict):
        if o.get('id') in want: acc[o['id']]=o
        for v in o.values(): walk(v, want, acc)
    elif isinstance(o, list):
        for v in o: walk(v, want, acc)
acc={}
walk(d, {'INV-1','INV-7','INV-8','TASK-003','TASK-004','TASK-005'}, acc)
W('TOPKEYS %s'%(list(d.keys()) if isinstance(d,dict) else type(d)))
for k in ['INV-1','INV-7','INV-8']:
    W('##### %s'%k); W(yaml.safe_dump(acc.get(k), allow_unicode=True, width=10**6))
W('##### TASK-003 keys %s'%list(acc['TASK-003'].keys()))
W(yaml.safe_dump({'acceptance':acc['TASK-003'].get('acceptance')}, allow_unicode=True, width=10**6))
W('##### TASK-004'); W(yaml.safe_dump(acc['TASK-004'], allow_unicode=True, width=10**6))
W('##### TASK-005 keys %s'%list(acc['TASK-005'].keys()))
W(yaml.safe_dump({'notes':acc['TASK-005'].get('notes')}, allow_unicode=True, width=10**6))
W('##### PROPOSAL markers')
for i,l in enumerate(open(C+'proposal.md'),1):
    if re.match(r'^#+ ', l) or re.search(r'What (1|6|7) ?补充|What 6', l):
        W('%d: %s'%(i, l.rstrip()[:200]))
out.close()
