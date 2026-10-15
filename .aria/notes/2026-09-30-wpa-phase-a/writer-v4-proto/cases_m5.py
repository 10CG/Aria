B = "Bash"
CASES = [
    (B, "export -p"), (B, "declare -x"), (B, "declare -p"), (B, "typeset -x"), (B, "set"), (B, "env -0"), (B, "env -u X"), (B, "env --null"),
    (B, "nomad alloc exec abc123 env -0"), (B, "docker exec abc env -0"), (B, "systemctl show -p Environment foo"), (B, "systemctl cat foo"),
    (B, "kubectl get pod p -o yaml"), (B, "kubectl get pod p -o json"),
    (B, "kubectl exec pod -- env -0"),
    (B, "kubectl exec pod -- env"),
    (B, "printenv"),
]
