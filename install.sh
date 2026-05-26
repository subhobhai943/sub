#!/bin/bash
# One-line installer for sub
# Usage: curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
set -e

INSTALL_DIR="/usr/local/bin"
RAW_URL="https://raw.githubusercontent.com/subhobhai943/sub/main/src/python/sub.py"

echo "[*] Installing sub..."
curl -sL "$RAW_URL" -o "$INSTALL_DIR/sub"
chmod +x "$INSTALL_DIR/sub"
sed -i '1s|.*|#!/usr/bin/env python3|' "$INSTALL_DIR/sub"
echo "[+] sub installed! Run: sub banner"
