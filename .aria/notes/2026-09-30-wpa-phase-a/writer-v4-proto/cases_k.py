CASES = [
 ("Bash", "cat /proc/$$/environ"), ("Bash", "cat /proc/$!/environ"), ("Bash", "cat /proc/thread-self/environ"), ("Bash", "cat /proc/[0-9]*/cmdline"),
 ("Bash", "cat /proc/1*/cmdline"), ("Bash", "cat /proc/1?/environ"), ("Bash", "tr '\\0' '\\n' < /proc/$$/environ"), ("Bash", "xargs -0 -a /proc/$$/environ echo"),
 ("Bash", "python3 -c \"print(open('/proc/$$/environ').read())\""), ("Bash", "grep -a x /proc/thread-self/task/1/cmdline"),
 ("Bash", "cat /proc/{1,2}/environ", 0), ("Bash", "cat /proc/[0-9]/environ", 0), ("Bash", "cat /proc/`pgrep -o x`/cmdline", 0), ("Bash", "cat /proc/./self/environ", 0),
 ("Bash", "cat /proc//self/environ", 0), ("Bash", 'for p in /proc/[0-9]*; do cat "$p/environ"; done', 0), ("Bash", "cat /proc/123/environ | grep '^PATH='", 0),
 ("Bash", "systemd-cgls", 0), ("Bash", "pidstat -l 1 1", 0), ("Bash", "w", 0), ("Bash", "busybox ps", 0), ("Bash", "ps -eo '%p %a'", 0),
 ("Bash", "cat /proc/N/cmdline", 0), ("Bash", "cat /proc/<pid>/cmdline", 0), ("Bash", "cat /proc/[pid]/environ", 0), ("Bash", "cat /proc/{pid}/environ", 0),
 ("Bash", "grep VmRSS /proc/$$/status", 0), ("Bash", "cat /proc/cpuinfo", 0),
 ("Bash", "docker container top abc"), ("Bash", "docker top abc"), ("Bash", "docker compose top"),
 ("Bash", 'git commit -m "docs: explain why watch ps aux is blocked"'), ("Bash", 'echo "the sshd log shows ps aux output"'), ("Bash", 'grep -n "ssh host ps aux" README.md'), ("Bash", "echo 'stopwatch: ps -ef'"),
]
