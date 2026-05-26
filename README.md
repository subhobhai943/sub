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
![License](https://img.shields.io/github/license/subhobhai943/sub?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=flat-square)

</div>

---

## ⚡ Install (One-Line)

```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

## 📦 Install via .deb

Download the latest `.deb` from [Releases](https://github.com/subhobhai943/sub/releases) and:

```bash
sudo dpkg -i sub_*.deb
```

## 🔧 Manual Install

```bash
git clone https://github.com/subhobhai943/sub.git
cd sub
sudo make install
```

---

## 📋 Commands

### ℹ️ Info
| Command | Description |
|---|---|
| `sub whoami` | Show info about the creator (Subhobhai) |
| `sub sysinfo` | System info: OS, IP, CPU, uptime, disk |
| `sub myip` | Show your public IP + geolocation |
| `sub version` | Show version |
| `sub banner` | Show ASCII banner |

### 🔴 Recon / Hacking
| Command | Description |
|---|---|
| `sub scan <host>` | Nmap scan (`--flags` for custom nmap args) |
| `sub ports <host>` | TCP port scan (`--start N --end N`) |
| `sub subdomain <domain>` | Brute-force subdomains (`--wordlist path`) |
| `sub banner-grab <host> --port N` | Grab service banner |
| `sub dns <domain>` | DNS records: A, AAAA, MX, TXT, NS, CNAME |
| `sub whois <domain>` | WHOIS lookup |
| `sub ipinfo <ip>` | IP geolocation via ipinfo.io |
| `sub ping <host>` | Ping (`--count N`) |
| `sub traceroute <host>` | Trace network route |
| `sub headers <url>` | HTTP response headers |
| `sub netstat` | Active network connections |

### 🔐 Crypto / Encoding
| Command | Description |
|---|---|
| `sub hash <text\|file>` | Hash with MD5/SHA* (`--algo sha256`) |
| `sub hashid <hash>` | Identify hash type |
| `sub encode <text> --mode b64` | Encode/decode (b64, b64d, hex, hexd, url, urld) |

### 🛠️ Utilities
| Command | Description |
|---|---|
| `sub generate --type password` | Generate: password/pin/hex/token/uuid (`--length N`) |
| `sub weather [city]` | Check weather (default: Durgapur) |
| `sub myrepos --user <github_user>` | List GitHub repos |

---

## 🧰 Optional Dependencies

Some commands need external tools:

```bash
sudo apt install nmap whois dnsutils traceroute
```

---

## 🚀 Examples

```bash
sub whoami                          # About Subhobhai
sub sysinfo                         # Your machine info
sub myip                            # Public IP + location
sub scan 192.168.1.1                # Nmap scan
sub scan google.com --flags '-sV'   # Custom nmap flags
sub ports scanme.nmap.org           # Port scan 1-1024
sub ports 10.0.0.1 --start 1 --end 65535  # Full port scan
sub subdomain example.com           # Find subdomains
sub dns github.com                  # DNS records
sub ipinfo 8.8.8.8                  # Google DNS info
sub hash "hello world" --algo sha256
sub hash /etc/passwd
sub hashid 5f4dcc3b5aa765d61d8327deb882cf99
sub encode "hello" --mode b64       # Base64 encode
sub encode "aGVsbG8=" --mode b64d   # Base64 decode
sub encode "hello world" --mode url
sub generate --type password --length 24
sub generate --type uuid
sub weather "Kolkata"
sub myrepos --user torvalds --limit 10
```

---

## 📜 License

MIT License — © 2026 [Subhobhai Sarkar](https://github.com/subhobhai943)

---

<div align="center">

Made with ❤️ from Durgapur, West Bengal, India

</div>
