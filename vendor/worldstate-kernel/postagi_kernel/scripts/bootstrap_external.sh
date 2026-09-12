#!/usr/bin/env bash
set -euo pipefail
mkdir -p external/src
clone_at() {
  local url="$1" dir="$2" ref="$3" branch="${4:-}"
  if [ -d "external/src/$dir/.git" ]; then return 0; fi
  if [ -n "$branch" ]; then git clone --branch "$branch" "$url" "external/src/$dir"; else git clone "$url" "external/src/$dir"; fi
  git -C "external/src/$dir" checkout "$ref"
}
clone_at https://github.com/yecchen/MIRAI.git MIRAI badda88c4ddc48992708c783d684a3feebf15a61
clone_at https://github.com/snap-stanford/supply-chains.git supply-chains 9283f085bc3ecd23dea0b13f437f5d08ceffb106 tgb
clone_at https://github.com/songma/patent-firm-link-share.git patent-firm-link-share 17f2f473a878036dfa8c87fdf969ac835b6edd24
clone_at https://github.com/kernc/backtesting.py.git backtesting.py ca2e2611621e472542ba90f7243a1fa06a7d7108
clone_at https://github.com/microsoft/qlib.git qlib 79633dd9506ea689e5400dea0197717b5b3d74b7
