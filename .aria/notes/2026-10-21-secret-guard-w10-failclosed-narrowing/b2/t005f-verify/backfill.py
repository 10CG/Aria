# backfill.py <aria worktree> <base sha> <out.md>: the literal comment changes of the hook between <base sha> and the working tree, hunk by hunk, as
# "before / after" code blocks for proposal What 7 补充 2 -- generated from git diff, not typed (the code lines of What 1 补充 2 are listed as such)
import subprocess, sys
wt, base, out = sys.argv[1:4]
d = subprocess.run(['git', '-C', wt, 'diff', '-U0', base, '--', 'hooks/secret-guard.sh'], capture_output=True, text=True).stdout.split('\n')
hunks = []; cur = None
for l in d:
    if l.startswith('@@'):
        cur = {'head': l, 'old': [], 'new': []}; hunks.append(cur)
    elif cur is not None and l.startswith('-') and not l.startswith('---'): cur['old'].append(l[1:])
    elif cur is not None and l.startswith('+') and not l.startswith('+++'): cur['new'].append(l[1:])
lines = []
for n, h in enumerate(hunks, 1):
    code = any(not x.lstrip().startswith('#') for x in h['old'] + h['new'])
    lines.append(f'{n}. `{h["head"].split("@@")[1].strip()}`' + ('（含代码行：What 1 补充 2 的那部分以上文代码块为准）' if code else '（只有注释）'))
    lines.append('\n   改前：\n\n```\n' + '\n'.join(h['old']) + '\n```\n\n   改后：\n\n```\n' + '\n'.join(h['new']) + '\n```\n')
open(out, 'w', encoding='utf-8').write('\n'.join(lines)); print('hunks', len(hunks))
