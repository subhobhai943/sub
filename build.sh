#!/bin/bash
# Build script for sub .deb package
set -e

echo "[*] Building sub .deb package..."

# Requires: fpm
# Install: gem install fpm
if ! command -v fpm &> /dev/null; then
    echo "[!] fpm not found. Install: gem install fpm"
    exit 1
fi

fpm -s dir -t deb \
    -n sub \
    -v 1.0.0 \
    --description "SUB Hacking & Info CLI Tool by Subhobhai" \
    --url "https://github.com/subhobhai943/sub" \
    --maintainer "Subhobhai Sarkar" \
    --depends python3 \
    --depends nmap \
    --depends whois \
    src/python/sub.py=/usr/bin/sub

echo "[+] Build complete: sub_1.0.0_all.deb"
