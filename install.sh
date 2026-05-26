#!/usr/bin/env bash
# install.sh — build + install sub (polyglot edition)
# Usage: sudo ./install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${PREFIX:-/usr/local/bin}"

cd "$SCRIPT_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " sub — Polyglot CLI installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Check available toolchains
echo
echo "[1/3] Checking toolchains..."
make check || true

# 2. Build native components
echo
echo "[2/3] Building native components..."
make build

# 3. Install
echo
echo "[3/3] Installing to ${PREFIX}..."
make install PREFIX="${PREFIX}"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Installation complete!"
echo " Run: sub help"
echo " Run: sub check-tools    (see backend status)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
