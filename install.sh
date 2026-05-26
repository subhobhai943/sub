#!/usr/bin/env bash
# install.sh — build every available backend, then install
# Usage: sudo ./install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${PREFIX:-/usr/local/bin}"
cd "$ROOT"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " sub — Polyglot installer"
echo " Backends: C · Rust · Kotlin · Java · Haxe · CUDA · ASM · M4 · Python"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "[1/3] Toolchain check..."
make check || true
echo
echo "[2/3] Building native components..."
make build
echo
echo "[3/3] Installing to ${PREFIX}..."
make install PREFIX="${PREFIX}"
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Done!  Run: sub help"
echo "        Run: sub check-tools"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
