<h1 align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&pause=1000&color=00FFFF&center=true&vCenter=true&width=600&lines=SUB+CLI+Tool;Python+%C2%B7+C+%C2%B7+Rust+%C2%B7+Assembly+%C2%B7+Kotlin+%C2%B7+Java;By+Subhobhai943" alt="SUB" />
</h1>

<p align="center">
  <b>6-language Linux CLI tool — Hacking · OSINT · Recon · Network · Crypto</b><br/>
  <a href="https://github.com/subhobhai943">@subhobhai943</a> • 
  <a href="https://sub-portofolio.netlify.app">Portfolio</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.0.0-cyan?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/C-GCC-orange?style=flat-square&logo=c" />
  <img src="https://img.shields.io/badge/Rust-stable-red?style=flat-square&logo=rust" />
  <img src="https://img.shields.io/badge/Assembly-x86--64-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Kotlin-2.0-blueviolet?style=flat-square&logo=kotlin" />
  <img src="https://img.shields.io/badge/Java-17+-brown?style=flat-square&logo=openjdk" />
  <img src="https://img.shields.io/badge/platform-Linux-lightgrey?style=flat-square&logo=linux" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
</p>

---

## 🧠 Architecture

```
sub  (Python — dispatcher)
 ├── sub-scan       (C)          ─ Fast TCP scanner + banner grabbing
 ├── sub-recon      (Rust)       ─ Subdomain enum, hash ID, cipher, crypto
 ├── sub-sysinfo    (Assembly)   ─ Raw x86-64 syscall system info
 ├── sub-net.jar    (Kotlin)     ─ Threaded scanner, GeoIP, traceroute, rdns
 └── sub-osint.jar  (Java)       ─ OSINT: username, email headers, URL expand
```

---

## 📦 Installation

### One-line
```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

### Build from Source
```bash
git clone https://github.com/subhobhai943/sub.git
cd sub

# Install deps
sudo apt install gcc rustc nasm binutils python3 default-jdk
# Install Kotlin compiler
curl -sL https://github.com/JetBrains/kotlin/releases/download/v2.0.21/kotlin-compiler-2.0.21.zip -o kotlin.zip
unzip kotlin.zip -d /opt/kotlin && export PATH=$PATH:/opt/kotlin/kotlinc/bin

# Build all 5 engines + install
make build && sudo make install
```

---

## 🚀 All Commands

### 🔵 Python
| Command | Description |
|---|---|
| `sub whoami` | Developer info |
| `sub sysinfo` | System info (ASM or Python) |
| `sub ports <host>` | Quick 16-port checker |
| `sub whois <domain>` | WHOIS lookup |
| `sub dns <domain>` | DNS resolution |
| `sub ping <host>` | Ping |
| `sub headers <url>` | HTTP headers |

### 🔴 C
| Command | Description |
|---|---|
| `sub scan <target>` | Fast TCP scan + banner grab |
| `sub scan <t> --start 1 --end 65535` | Full range |

### 🟠 Rust
| Command | Description |
|---|---|
| `sub hashid <hash>` | Hash type identifier |
| `sub pwcheck <password>` | Password strength |
| `sub subdomain <domain>` | Subdomain probe |
| `sub caesar <text> <n>` | Caesar cipher |
| `sub b64 <text>` | Base64 encode |

### 🟣 Assembly
| Command | Description |
|---|---|
| `sub rawsys` | Raw system info via syscall |

### 🟡 Kotlin
| Command | Description |
|---|---|
| `sub netscan <host>` | Threaded port scan (100 threads) |
| `sub geoip <ip>` | IP geolocation (ip-api.com) |
| `sub rdns <ip>` | Reverse DNS lookup |
| `sub grab <host> <port>` | TCP banner grabber |
| `sub traceroute <host>` | Traceroute |
| `sub ifaces` | Network interfaces |

### 🟢 Java
| Command | Description |
|---|---|
| `sub username <name>` | Check username on 12 platforms |
| `sub emailhdr <file>` | Parse + analyse email headers |
| `sub expand <url>` | Follow + expand short URLs |
| `sub httpstat <url>` | HTTP status + server fingerprint |

---

## 💡 Examples

```bash
# Scanning
sub scan 192.168.1.1
sub netscan 10.0.0.1 --start 1 --end 9999 --threads 200
sub grab scanme.nmap.org 22

# OSINT
sub username subhobhai943
sub geoip 8.8.8.8
sub rdns 1.1.1.1
sub expand https://bit.ly/example
sub httpstat https://github.com

# Crypto & Analysis
sub hashid 5f4dcc3b5aa765d61d8327deb882cf99
sub pwcheck "MyP@ssw0rd!"
sub caesar "Attack at dawn" 13
sub b64 "subhobhai943"

# Raw
sub rawsys
sub whoami
```

---

## 📁 Structure
```
sub/
├── src/
│   ├── sub.py              ← Python dispatcher
│   └── core/
│       ├── scanner.c       ← C
│       ├── recon.rs        ← Rust
│       ├── sysinfo.asm     ← Assembly
│       ├── NetUtils.kt     ← Kotlin
│       └── OsintTools.java ← Java
├── debian/
├── .github/workflows/
├── Makefile
├── install.sh
└── README.md
```

---

## 📄 License
MIT — © 2026 [Subhobhai Sarkar](https://github.com/subhobhai943)
