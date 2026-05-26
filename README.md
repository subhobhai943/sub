<div align="center">

```
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
```

**A powerful multi-purpose hacking & utility CLI tool**  
by [Subhobhai Sarkar](https://github.com/subhobhai943)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![C](https://img.shields.io/badge/C-GCC-blue?style=flat-square&logo=c)
![Rust](https://img.shields.io/badge/Rust-stable-orange?style=flat-square&logo=rust)
![Kotlin](https://img.shields.io/badge/Kotlin-JVM-purple?style=flat-square&logo=kotlin)
![Java](https://img.shields.io/badge/Java-17+-red?style=flat-square&logo=openjdk)
![Haxe](https://img.shields.io/badge/Haxe-C%2B%2B-yellow?style=flat-square&logo=haxe)
![CUDA](https://img.shields.io/badge/CUDA-C%2B%2B-76b900?style=flat-square&logo=nvidia)
![ASM](https://img.shields.io/badge/ASM-x86__64%2FAArch64-lightgrey?style=flat-square)
![M4](https://img.shields.io/badge/M4-macros-blueviolet?style=flat-square)
![License](https://img.shields.io/github/license/subhobhai943/sub?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=flat-square)

</div>

---

## 🧬 Architecture

`sub` is a **polyglot CLI** — a single `sub` bash dispatcher that routes every command to the best available native backend, with graceful fallback to Python if a binary isn't compiled.

```
  sub <command>
       │
       ├─ C (gcc)          sub-scan      → ports, scan
       ├─ Rust (rustc)     sub-recon     → hashid, pwcheck, subdomain, caesar, b64
       ├─ Kotlin (kotlinc) sub-net.jar   → banner-grab, traceroute, geoip, rdns, ifaces
       ├─ Kotlin (kotlinc) sub-kt.jar    → whoami, info
       ├─ Java (javac)     Sub.class     → whoami, info, ports
       ├─ Haxe→C++ (haxe)  sub-haxe     → whoami, banner, info
       ├─ CUDA C++ (nvcc)  sub-cuda      → gpuinfo, whoami, banner
       ├─ ASM NASM/GAS     sub-asm       → sysinfo  (x86_64 or aarch64)
       ├─ ASM NASM         sub-sysinfo   → sysinfo
       ├─ M4 macros (m4)   sub-whoami.txt→ whoami  (pre-rendered at build time)
       └─ Python (python3) sub.py        → everything else + final fallback
```

Every backend is **optional** — `sub` works out of the box with just Python. Install more toolchains and rebuild to unlock native speed.

---

## ⚡ Install (One-Line)

```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

## 🔧 Manual Install

```bash
git clone https://github.com/subhobhai943/sub.git
cd sub
make check        # see which toolchains you have
make build        # compile all available backends
sudo make install
```

## 📦 Install via .deb

Download the latest `.deb` from [Releases](https://github.com/subhobhai943/sub/releases) and:

```bash
sudo dpkg -i sub_*.deb
```

---

## 🛠️ Toolchains

Install any or all — every toolchain is optional:

```bash
# C
sudo apt install gcc

# Rust
curl https://sh.rustup.rs -sSf | sh

# Kotlin + Java
sudo apt install kotlinc default-jdk

# Haxe
sudo apt install haxe hxcpp

# CUDA (requires NVIDIA GPU)
# https://developer.nvidia.com/cuda-downloads

# ASM (x86_64)
sudo apt install nasm

# M4
sudo apt install m4
```

Then rebuild:
```bash
make build
```

---

## 📋 Commands

### ℹ️ Info
| Command | Description | Backend |
|---|---|---|
| `sub whoami` | Info about the creator | M4 → Haxe → CUDA → Kotlin → Java → Python |
| `sub sysinfo` | OS, IP, CPU, uptime, disk | ASM → Python |
| `sub info` | System info (JVM edition) | Kotlin → Java → Haxe → Python |
| `sub myip` | Public IP + geolocation | Python |
| `sub banner` | ASCII banner | CUDA → Haxe → Kotlin → Java → Python |
| `sub version` | Show version | Python |

### 🔴 Recon / Hacking
| Command | Description | Backend |
|---|---|---|
| `sub ports <host>` | TCP port scan (`--start N --end N`) | C → Kotlin → Python |
| `sub scan <host>` | Nmap scan (`--flags '...'`) | C → Kotlin → Python |
| `sub subdomain <domain>` | Subdomain brute-force (`--wordlist path`) | Rust → Python |
| `sub banner-grab <host> --port N` | Grab service banner | Kotlin → Python |
| `sub geoip <ip>` | IP geolocation (ip-api.com, no key) | Kotlin → Python |
| `sub rdns <ip>` | Reverse DNS lookup | Kotlin |
| `sub ifaces` | Network interfaces | Kotlin → Python |
| `sub traceroute <host>` | Trace network route | Kotlin → Python |
| `sub dns <domain>` | DNS records: A, AAAA, MX, TXT, NS, CNAME | Python |
| `sub whois <domain>` | WHOIS lookup | Python |
| `sub ipinfo <ip>` | IP geolocation via ipinfo.io | Python |
| `sub ping <host>` | Ping (`--count N`) | Python |
| `sub headers <url>` | HTTP response headers | Python |
| `sub netstat` | Active network connections | Python |

### 🔐 Crypto / Encoding
| Command | Description | Backend |
|---|---|---|
| `sub hashid <hash>` | Identify hash type | Rust → Python |
| `sub pwcheck <password>` | Password strength checker | Rust |
| `sub caesar <text> <shift>` | Caesar cipher | Rust |
| `sub b64 <text>` | Base64 encode | Rust → Python |
| `sub hash <text\|file>` | Hash with MD5/SHA* (`--algo sha256`) | Python |
| `sub encode <text> --mode b64` | Encode/decode (b64, b64d, hex, hexd, url, urld) | Python |

### 🖥️ GPU / CUDA
| Command | Description | Backend |
|---|---|---|
| `sub gpuinfo` | CUDA GPU details + live kernel launch demo | CUDA C++ |
| `sub cuda` | Alias for gpuinfo | CUDA C++ |

### 🔩 Assembly
| Command | Description | Backend |
|---|---|---|
| `sub sysinfo` | Native bare-metal sysinfo | NASM x86_64 / GAS aarch64 |

### 🧩 M4
| Command | Description | Backend |
|---|---|---|
| `sub m4` | Print M4 macro-expanded whoami | M4 pre-rendered / live m4 |
| `sub macro` | Alias for m4 | M4 |

### 🛠️ Utilities
| Command | Description | Backend |
|---|---|---|
| `sub generate --type password` | Generate: password/pin/hex/token/uuid (`--length N`) | Python |
| `sub weather [city]` | Check weather (default: Durgapur) | Python |
| `sub myrepos --user <github_user>` | List GitHub repos | Python |
| `sub build` | Compile all native backends | Makefile |
| `sub check-tools` | Audit toolchain + backend status | Makefile |

---

## 🚀 Examples

```bash
# Info
sub whoami                          # served by M4 if available
sub sysinfo                         # native ASM if NASM built
sub info                            # JVM sysinfo (Kotlin/Java)
sub banner                          # CUDA banner if nvcc built
sub gpuinfo                         # GPU info + kernel launch

# Recon
sub ports scanme.nmap.org           # C scanner (fast, non-blocking)
sub ports 10.0.0.1 --start 1 --end 65535
sub scan 192.168.1.1
sub scan google.com --flags '-sV'
sub subdomain example.com           # Rust TCP-connect probe
sub geoip 8.8.8.8                   # Kotlin ip-api.com
sub rdns 8.8.8.8                    # Kotlin reverse DNS
sub ifaces                          # Kotlin network interfaces
sub traceroute github.com
sub banner-grab example.com --port 22
sub dns github.com
sub ipinfo 1.1.1.1

# Crypto
sub hashid 5f4dcc3b5aa765d61d8327deb882cf99
sub pwcheck "MyP@ssw0rd123"
sub caesar "hello world" 13
sub b64 "hello world"
sub hash "hello world" --algo sha256
sub hash /etc/passwd
sub encode "hello" --mode b64
sub encode "aGVsbG8=" --mode b64d
sub encode "hello world" --mode url

# M4
sub m4                              # raw M4 macro output

# Utilities
sub generate --type password --length 24
sub generate --type uuid
sub weather "Kolkata"
sub myrepos --user torvalds --limit 10

# Build
sub check-tools                     # see all backend status
sub build                           # compile everything
```

---

## 🗂️ Source Layout

```
sub/
├── sub                  ← bash dispatcher (entry point)
├── src/
│   ├── sub.py           ← Python master CLI (fallback for everything)
│   ├── python/sub.py    ← standalone Python edition
│   ├── core/
│   │   ├── scanner.c    ← C fast port scanner
│   │   ├── recon.rs     ← Rust recon & crypto engine
│   │   ├── NetUtils.kt  ← Kotlin threaded network utils
│   │   ├── OsintTools.java ← Java OSINT tools
│   │   └── sysinfo.asm  ← NASM sysinfo module
│   ├── java/Sub.java    ← Java standalone CLI
│   ├── kotlin/Sub.kt    ← Kotlin standalone CLI
│   ├── haxe/Sub.hx      ← Haxe cross-platform CLI
│   ├── cuda/sub.cu      ← CUDA C++ GPU module
│   ├── asm/
│   │   ├── x86_64/sub.asm  ← NASM x86_64
│   │   └── aarch64/sub.s   ← GAS AArch64
│   └── m4/sub.m4        ← M4 macro whoami
├── Makefile             ← polyglot build system
├── build.sh             ← one-shot build helper
└── install.sh           ← build + install
```

---

## 🧰 Optional System Dependencies

Some Python commands need external tools:

```bash
sudo apt install nmap whois dnsutils traceroute
```

---

## 📜 License

MIT License — © 2026 [Subhobhai Sarkar](https://github.com/subhobhai943)

---

<div align="center">

Made with ❤️ from Durgapur, West Bengal, India  
**Python · C · Rust · Kotlin · Java · Haxe · CUDA · Assembly · M4**

</div>
