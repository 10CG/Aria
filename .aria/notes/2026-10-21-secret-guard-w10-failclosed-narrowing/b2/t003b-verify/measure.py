# measure.py <instrumented hook> <shape file> <runs> <label>: my own e2e measure (independent of w14-matrix.sh). One call per run: the JSON on stdin from a file,
# stderr to a file, HOME and cwd a fresh dir, LC_ALL=C.UTF-8, the budget variable removed. W = wall from just before the launch to the exit (time.time());
# T_trigger = the first relax-start probe (EPOCHREALTIME) minus the same launch time; bound = max(T_trigger or W, 3) + 0.3 (v31/run-evidence.sh:47).
import json, os, subprocess, sys, tempfile, time
hook, shape, n, label = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
cmd = open(shape, encoding='utf-8').read()
base = os.path.dirname(os.path.abspath(sys.argv[0]))
for r in range(1, n + 1):
    d = tempfile.mkdtemp(prefix='m-', dir=os.path.join(base, 'runs'))
    jf = os.path.join(d, 'in.json'); open(jf, 'w', encoding='utf-8').write(json.dumps({'tool_name': 'Bash', 'tool_input': {'command': cmd}}))
    env = {k: v for k, v in os.environ.items() if k not in ('SECRET_GUARD_TIME_BUDGET_S', 'CLAUDE_PROJECT_DIR', 'SECRET_GUARD_RAW_GATE')}
    env.update(HOME=d, SG_DBG=os.path.join(d, 'dbg'), LC_ALL='C.UTF-8')
    with open(jf, 'rb') as fi, open(os.path.join(d, 'err'), 'wb') as fe:
        t0 = time.time(); p = subprocess.run(['bash', hook], stdin=fi, stdout=subprocess.DEVNULL, stderr=fe, cwd=d, env=env, timeout=60); t1 = time.time()
    w = t1 - t0
    trig = None
    if os.path.exists(env['SG_DBG']):
        for ln in open(env['SG_DBG'], encoding='utf-8', errors='replace'):
            f = ln.split()
            if len(f) == 2 and f[1] == 'relax-start': trig = float(f[0].replace(',', '.')) - t0; break
    err = open(os.path.join(d, 'err'), encoding='utf-8', errors='replace').read()
    kind = 'allow' if p.returncode == 0 else ('finding' if 'reads a secret-bearing source' in err else ('size' if 'too large to scan' in err else ('longline' if 'has a line longer than' in err else 'other')))
    b = max(trig if trig is not None else w, 3.0) + 0.3
    print(f'{label} run {r} rc={p.returncode} {kind:8s} W={w:6.3f} T_trigger={"-" if trig is None else f"{trig:6.3f}"} bound={b:5.3f} over={"YES" if w > b else "no"}', flush=True)
