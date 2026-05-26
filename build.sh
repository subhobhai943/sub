#!/usr/bin/env bash
# Build a .deb package for SUB
set -e

echo "[*] Installing build dependencies..."
sudo apt-get install -y python3 debhelper dh-python

echo "[*] Building .deb package..."
dpkg-buildpackage -us -uc -b

echo "[+] Build complete! Check parent directory for .deb file."
ls ../*.deb 2>/dev/null || echo "(no .deb found — check for errors above)"
