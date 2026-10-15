B = "Bash"
CASES = [(B, c) for c in [
    "export -p", "declare -x", "declare -p", "typeset -x", "set", "env -0", "env -u X", "env --null",
    "nomad alloc exec abc env -0", "docker exec c env -0", "kubectl exec pod -- env -0", "ssh host env -0",
    "systemctl show -p Environment foo", "systemctl cat foo", "kubectl get pod -o yaml", "kubectl get pod -o json",
    "printenv", "env", "set | grep pass",
]]
