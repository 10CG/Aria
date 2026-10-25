1. `-93,6 +93,9`（只有注释）

   改前：

```
#     blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in
#     effect; where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no
#     project extension, time left), the pass is re-run under a
#     hard deadline with no count bound, the growth over the input as the limit and the
#     copy judged in full, and growth over 8192 characters, the deadline or any failure of
#     the rerun still blocks. The pass substitutes text; it does not run the shell: a
```

   改后：

```
#     blocked for its size wherever the relaxed rerun of 10CG/aria-plugin#217 is not in
#     effect, and also where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL,
#     no project extension, time left) whenever that rerun falls back. The rerun runs the
#     pass again under a hard deadline with no count bound, the growth over the input as
#     the limit and the copy judged in full: growth over 8192 characters blocks with the
#     growth text, a value over 4096 characters with the value text (the rerun reaches
#     values that the counts cut off in the baseline pass), and the deadline, a time
#     checkpoint, the self-check or any other failure of the rerun falls back to that size
#     block. The pass substitutes text; it does not run the shell: a
```

2. `-599,3 +602,4`（只有注释）

   改前：

```
# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text, byte for byte as before (the
# W9 extension's look at the substituted whole command, after the pass, blocks on such a copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8
# replacements, 8 for statements -- bound the baseline pass and still pass beyond the limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)
```

   改后：

```
# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun neither allows nor blocks on its own (the deadline, a time checkpoint, the self-check, any other
# failure), the command is blocked with the size text, byte for byte as before (the W9 extension's look at the substituted whole command, after the pass, blocks on such a
# copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- bound the baseline pass and still pass beyond the
# limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)
```

3. `-720,4 +724,4`（只有注释）

   改前：

```
# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline block text is kept
# in _SG_OV_PAT / _SG_OV_MODE for the fallback), else with the oversize BLOCK. Inside the relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy
# over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text: the caller falls back to the baseline block). Nothing behind an overrun is built
# or judged.
```

   改后：

```
# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline reason string and mode are
# kept in _SG_OV_PAT / _SG_OV_MODE -- not a text: on a fallback _sg_emit_blocked writes the baseline block text from them again), else with the oversize BLOCK. Inside the
# relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text:
# the caller falls back to the baseline block). Nothing behind an overrun is built or judged.
```

4. `-792 +796`（只有注释）

   改前：

```
# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
```

   改后：

```
# returns 4 instead and keeps the baseline reason and mode in _SG_OV_PAT / _SG_OV_MODE; _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
```

5. `-798,2 +802,4`（只有注释）

   改前：

```
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on an x86_64
# GNU/Linux build of bash 5.0-5.3 outside WSL (the versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
```

   改后：

```
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. The one exception (What 4):
# a fatal error of bash itself inside the job that makes it exit with status 2 and write its error message is passed on as the block text -- the command is
# still blocked, but with bash's message instead of the baseline text. In effect only on an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL (the
# versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
```

6. `-823 +829,2`（含代码行：What 1 补充 2 的那部分以上文代码块为准）

   改前：

```
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" || -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wsl=wsl   # WSL marks; the environment can only switch the relaxation off with them
```

   改后：

```
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read
```

7. `-831 +838,8`（含代码行：What 1 补充 2 的那部分以上文代码块为准）

   改前：

```
_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off
```

   改后：

```
_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads, and no binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc), or one is and holds no entry named WSLInterop*. The entries are looked at only under a mounted binfmt_misc, so the look never triggers an automount (an autofs mount point there that nobody serves can hold a stat until the hook is killed, and a killed hook lets the command through); a mount table that cannot be read keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
  local d="${2:-/proc/sys/fs/binfmt_misc}" l e m=0
  { while IFS= read -r l; do if [[ "$l" == *" $d binfmt_misc "* ]]; then m=1; fi; done; } 2>/dev/null < "${1:-/proc/self/mounts}" || return 1   # if, not &&: a last line that does not match must not make the loop's status 1 (that would read as an unreadable table); 2>/dev/null before <, so a table that cannot be opened writes nothing to stderr
  (( m )) || return 0
  for e in "$d"/WSLInterop*; do [[ -e "$e" ]] && return 1; done
  return 0
}
_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root is found (_sg_ext_root prints nothing, which includes a cwd that jq cannot read: without a root no extension can be in effect), or there is no .aria/secret-guard.paths under it. A file there, in any state, keeps the relaxation off
```
