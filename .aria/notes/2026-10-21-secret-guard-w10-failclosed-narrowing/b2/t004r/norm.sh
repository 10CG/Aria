#!/usr/bin/env bash
# norm.sh FILE : drop the header lines (# <date> ...), mask floats (wall clock, loads) -> stdout
grep -v -E '^# 20[0-9]{2}-' "$1" | sed -E 's/[0-9]+\.[0-9]+/F/g'
