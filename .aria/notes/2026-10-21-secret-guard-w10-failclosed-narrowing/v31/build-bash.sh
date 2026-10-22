#!/usr/bin/env bash
# build-bash.sh <work dir> : builds GNU bash 5.0 / 5.1 / 5.3 with every official patch, for the version rounds of sc-cases.sh (the system bash is 5.2.15).
# Tarballs and patches come from ftp.gnu.org and are verified with gpgv against the GNU keyring before anything is extracted; binaries go to ~/.aria/tools/bash-<x.y.z>/bash.
# bash 3.2.57 (~/.aria/tools/bash-3.2.57/bash) was built earlier on this host; its recipe is not recorded (README).
set -uo pipefail
B=$1; OUT=/home/dev/.aria/tools
log(){ printf '%s %s\n' "$(date -u +%H:%M:%S)" "$*"; }
mkdir -p "$B/dl-keyring" && curl -sSfo "$B/dl-keyring/gnu-keyring.gpg" https://ftp.gnu.org/gnu/gnu-keyring.gpg || { log "keyring download failed"; exit 1; }
K=$B/dl-keyring/gnu-keyring.gpg
for spec in 5.0:50:18 5.1:51:16 5.3:53:20; do
  v=${spec%%:*}; rest=${spec#*:}; pp=${rest%%:*}; n=${rest#*:}
  D=$B/dl-$v; S=$B/src-$v; rm -rf "$D" "$S"; mkdir -p "$D" "$S"
  log "== $v: download"
  curl -sSfo "$D/bash-$v.tar.gz" "https://ftp.gnu.org/gnu/bash/bash-$v.tar.gz" && curl -sSfo "$D/bash-$v.tar.gz.sig" "https://ftp.gnu.org/gnu/bash/bash-$v.tar.gz.sig" || { log "$v tarball download failed"; continue; }
  gpgv --keyring "$K" "$D/bash-$v.tar.gz.sig" "$D/bash-$v.tar.gz" >/dev/null 2>&1 || { log "$v tarball SIGNATURE FAILED"; continue; }
  ok=1
  for i in $(seq -f '%03g' 1 "$n"); do
    f=bash$pp-$i
    curl -sSfo "$D/$f" "https://ftp.gnu.org/gnu/bash/bash-$v-patches/$f" && curl -sSfo "$D/$f.sig" "https://ftp.gnu.org/gnu/bash/bash-$v-patches/$f.sig" || { log "$v patch $f download failed"; ok=0; break; }
    gpgv --keyring "$K" "$D/$f.sig" "$D/$f" >/dev/null 2>&1 || { log "$v patch $f SIGNATURE FAILED"; ok=0; break; }
  done
  (( ok )) || continue
  log "$v: signatures OK (tarball + $n patches)"
  tar -xzf "$D/bash-$v.tar.gz" -C "$S" || { log "$v extract failed"; continue; }
  src=$S/bash-$v
  for i in $(seq -f '%03g' 1 "$n"); do patch -p0 -s -d "$src" < "$D/bash$pp-$i" || { log "$v patch $i failed to apply"; ok=0; break; }; done
  (( ok )) || continue
  log "$v: configure+make"
  ( cd "$src" && taskset -c 0,1 nice -n 19 ./configure --prefix="$S/inst" >"$S/configure.log" 2>&1 && taskset -c 0,1 nice -n 19 make -j2 >"$S/make.log" 2>&1 ) || { log "$v build FAILED (see $S/make.log)"; continue; }
  full=$("$src/bash" -c 'echo "${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}.${BASH_VERSINFO[2]}"')
  mkdir -p "$OUT/bash-$full" && cp "$src/bash" "$OUT/bash-$full/bash" && log "$v: installed $OUT/bash-$full/bash ($("$OUT/bash-$full/bash" --version | head -1))"
done
log "done"
