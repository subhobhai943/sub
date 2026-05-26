#!/usr/bin/env bash
# sub - One-line installer for any Debian/Ubuntu system
# Usage: curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash

set -e

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e ""
echo -e "${CYAN}  ███████╗██╗   ██╗██████╗ ${RESET}"
echo -e "${CYAN}  ██╔════╝██║   ██║██╔══██╗${RESET}"
echo -e "${CYAN}  ███████╗██║   ██║██████╔╝${RESET}"
echo -e "${CYAN}  ╚════██║██║   ██║██╔══██╗${RESET}"
echo -e "${CYAN}  ███████║╚██████╔╝██████╔╝${RESET}"
echo -e "${CYAN}  ╚══════╝ ╚═════╝ ╚═════╝ ${RESET}"
echo -e "${YELLOW}  ─────────────────────────────────────────${RESET}"
echo -e "${GREEN}  Installing sub v1.0.0 by subhobhai943${RESET}"
echo -e "${YELLOW}  ─────────────────────────────────────────${RESET}"
echo ""

# Check for required tools
for dep in python3 curl; do
  if ! command -v $dep &>/dev/null; then
    echo -e "${YELLOW}  [*] Installing dependency: $dep${RESET}"
    apt-get install -y "$dep" -qq
  fi
else
  echo -e "${GREEN}  [✓] $dep found${RESET}"
done

# Recommend optional tools
for opt in nmap whois dig; do
  if ! command -v $opt &>/dev/null; then
    echo -e "${YELLOW}  [!] Optional tool missing: $opt (some features limited)${RESET}"
  fi
done

# Download main script
INSTALL_DIR="/usr/local/bin"
RAW_URL="https://raw.githubusercontent.com/subhobhai943/sub/main/src/sub.py"

echo ""
echo -e "  ${CYAN}[*] Downloading sub...${RESET}"
curl -fsSL "$RAW_URL" -o "$INSTALL_DIR/sub"
chmod +x "$INSTALL_DIR/sub"

# Make it executable as 'sub' directly (already a Python3 script with shebang)
echo ""
echo -e "  ${GREEN}[✓] sub installed at $INSTALL_DIR/sub${RESET}"
echo -e "  ${GREEN}[✓] Run: sub help${RESET}"
echo ""
sub help || true
