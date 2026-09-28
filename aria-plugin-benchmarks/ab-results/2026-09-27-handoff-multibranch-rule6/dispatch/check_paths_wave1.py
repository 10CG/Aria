import json,sys,glob,re
S='/tmp/claude-1000/-home-dev-Aria/87a07f9d-886a-487e-9880-865fa0d8393b/scratchpad'
mp=json.load(open(S+'/arm_map.json'))
for r in sys.argv[1:]:
    t=json.load(open(f'{S}/runs/{r}/timing.json'))['agent_output']
    cmds=[];gate=[]
    for line in open(t):
        try: o=json.loads(line)
        except: continue
        m=o.get('message',{})
        c=m.get('content') if isinstance(m,dict) else None
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_use' and b.get('name')=='Bash':
                cmd=b['input'].get('command','')
                if 'scan.py' in cmd: cmds.append(re.findall(r'\S*scan\.py',cmd))
                if re.search(r'phase1_gate|release_gate',cmd) and 'python' in cmd: gate.append(cmd[:200])
            if b.get('type')=='tool_result':
                s=json.dumps(b.get('content'))
                if 'push_skipped' in s: gate.append('RESULT:'+s[:200])
    print(r, mp[r]['arm'], 'scan:',cmds, 'gate:',gate)
