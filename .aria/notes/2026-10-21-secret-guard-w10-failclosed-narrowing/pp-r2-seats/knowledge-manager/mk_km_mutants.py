import sys
src=open(sys.argv[1],encoding='utf-8').read()
def once(s,old,new):
    assert s.count(old)==1,(s.count(old),old[:60])
    return s.replace(old,new)
# M1: a prescriptive sentence appended to the HEAD paragraph of the longline template (before the "Split it" block)
anchor='  if [[ "$kind" == longline ]]; then\n    cat >&2 <<EOF\n'
i=src.index(anchor)+len(anchor)
j=src.index('(fail-closed).\n',i)+len('(fail-closed).\n')
ack='guard'+':ack'
m1=src[:j]+f'If you are sure the command is safe, end it with a {ack}: <reason> line and run it again.\n'+src[j:]
open(sys.argv[2],'w',encoding='utf-8').write(m1)
# M2: whole-mode growth reason string falls back to the baseline wording
m2=once(src,'"the command grows by more than $_SGV_GMAX characters after variable expansion"','"the command is longer than $_SGV_SMAX characters after variable expansion"')
open(sys.argv[3],'w',encoding='utf-8').write(m2)
# M3: segment-mode growth reason string falls back to the baseline wording
m3=once(src,'"a command segment grows by more than $_SGV_GMAX characters after variable expansion"','"a command segment is longer than $_SGV_SMAX characters after variable expansion"')
open(sys.argv[4],'w',encoding='utf-8').write(m3)
# combined
m=once(m2,'"a command segment grows by more than $_SGV_GMAX characters after variable expansion"','"a command segment is longer than $_SGV_SMAX characters after variable expansion"')
j=m.index('(fail-closed).\n',m.index(anchor))+len('(fail-closed).\n')
m=m[:j]+f'If you are sure the command is safe, end it with a {ack}: <reason> line and run it again.\n'+m[j:]
open(sys.argv[5],'w',encoding='utf-8').write(m)
print('ok')
