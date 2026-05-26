#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  SUB — One-line installer
#  Usage: curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
# ─────────────────────────────────────────────────────────────

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
EOF
echo -e "${YELLOW}  SUB Installer — by Subhobhai943${NC}\n"

# Check root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Please run as root (sudo).${NC}"
  exit 1
fi

# Check python3
if ! command -v python3 &>/dev/null; then
  echo -e "${YELLOW}[*] Python3 not found. Installing...${NC}"
  apt-get install -y python3
fi

echo -e "${CYAN}[*] Downloading SUB...${NC}"
TMP=$(mktemp -d)
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/src/sub.py -o "$TMP/sub"

chmod +x "$TMP/sub"
mv "$TMP/sub" /usr/local/bin/sub

echo -e "${GREEN}[+] SUB installed successfully!${NC}"
echo -e "${YELLOW}[*] Recommended: sudo apt install nmap whois${NC}"
echo -e "\n  Run ${CYAN}sub --help${NC} to get started.\n"
