#!/usr/bin/env bash
# build.sh — one-shot build helper (delegates to Makefile)
# Usage: ./build.sh [target]   default target: all
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"   # always run from repo root

TARGET="${1:-all}"

echo "[build.sh] Running: make ${TARGET}"
make "${TARGET}"
