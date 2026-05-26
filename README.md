<h1 align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&pause=1000&color=00FFFF&center=true&vCenter=true&width=500&lines=SUB+CLI+Tool;Python+%C2%B7+C+%C2%B7+Rust+%C2%B7+Assembly;By+Subhobhai943" alt="SUB" />
</h1>

<p align="center">
  <b>A multi-language Linux CLI tool — Hacking utilities + Developer profile + System recon</b><br/>
  <a href="https://github.com/subhobhai943">@subhobhai943</a> • 
  <a href="https://sub-portfolio.netlify.app">Portfolio</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-cyan?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/C-GCC-orange?style=flat-square&logo=c" />
  <img src="https://img.shields.io/badge/Rust-stable-red?style=flat-square&logo=rust" />
  <img src="https://img.shields.io/badge/Assembly-x86--64-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/platform-Linux-lightgrey?style=flat-square&logo=linux" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
</p>

---

## 🧠 Architecture

```
sub (Python — dispatcher)
  ├── sub-scan     (C)          ── Fast TCP scanner + banner grabbing
  ├── sub-recon    (Rust)       ── Subdomain enum, hash ID, crypto tools
  └── sub-sysinfo  (Assembly)   ── Raw syscall system info
```

---

## 📦 Installation

### One-line Install
```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

### Build from Source
```bash
git clone https://github.com/subhobhai943/sub.git
cd sub

# Install build deps
sudo apt install gcc rustc nasm binutils python3

# Build everything
make build

# Install to /usr/local/bin
sudo make install
```

### Install .deb
```bash
sudo dpkg -i sub_2.0.0-1_amd64.deb
sudo apt-get install -f
```

---

## 🚀 Commands

### 🔵 Python (Built-in)
| Command | Description |
|---|---|
| `sub whoami` | Developer info (Subhobhai) |
| `sub sysinfo` | System info (uses ASM binary if available) |
| `sub ports <host>` | Quick 16-port checker |
| `sub whois <domain>` | WHOIS lookup |
| `sub dns <domain>` | DNS resolution |
| `sub ping <host>` | Ping a host |
| `sub headers <url>` | HTTP response headers |
| `sub banner` | ASCII art banner |
| `sub version` | Version info |

### 🔴 C-powered
| Command | Description |
|---|---|
| `sub scan <target>` | Fast TCP port scan + banner grabbing |
| `sub scan <target> --start 1 --end 65535` | Full port range scan |

### 🟠 Rust-powered
| Command | Description |
|---|---|
| `sub hashid <hash>` | Identify hash type (MD5/SHA1/SHA256...) |
| `sub pwcheck <password>` | Password strength analysis |
| `sub subdomain <domain>` | Subdomain enumeration |
| `sub caesar <text> <shift>` | Caesar cipher encrypt/decrypt |
| `sub b64 <text>` | Base64 encode |

### 🟣 Assembly-powered
| Command | Description |
|---|---|
| `sub rawsys` | Raw system info via x86-64 syscalls |

---

## 💡 Examples

```bash
# Hacking
sub scan 192.168.1.1
sub scan scanme.nmap.org --start 1 --end 65535
sub subdomain github.com
sub hashid 5f4dcc3b5aa765d61d8327deb882cf99
sub pwcheck "MyP@ssw0rd!"

# Recon
sub whois google.com
sub dns github.com
sub headers https://example.com

# Crypto
sub caesar "Hello World" 13
sub b64 "Subhobhai943"

# Info
sub whoami
sub rawsys
sub sysinfo
```

---

## 📁 Project Structure

```
sub/
├── src/
│   ├── sub.py              ← Python dispatcher
│   └── core/
│       ├── scanner.c       ← C: fast TCP scanner
│       ├── recon.rs        ← Rust: recon & crypto
│       └── sysinfo.asm     ← Assembly: raw syscall sysinfo
├── debian/                 ← .deb packaging
├── .github/workflows/      ← CI: auto-build all + release
├── Makefile                ← Build everything with one command
├── install.sh              ← One-line installer
└── README.md
```

---

## 🛠️ Build Individual Components

```bash
# C only
gcc -O2 -Wall -o src/core/sub-scan src/core/scanner.c

# Rust only
rustc -O -o src/core/sub-recon src/core/recon.rs

# Assembly only
nasm -f elf64 src/core/sysinfo.asm -o src/core/sysinfo.o
ld -o src/core/sub-sysinfo src/core/sysinfo.o
```

---

## 📄 License

MIT — © 2026 [Subhobhai Sarkar](https://github.com/subhobhai943)
