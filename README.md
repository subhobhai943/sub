<h1 align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&pause=1000&color=00FFFF&center=true&vCenter=true&width=435&lines=SUB+CLI+Tool;By+Subhobhai943" alt="SUB" />
</h1>

<p align="center">
  <b>A powerful Linux CLI tool — Hacking utilities + Developer profile + System recon</b><br/>
  <a href="https://github.com/subhobhai943">@subhobhai943</a> • 
  <a href="https://sub-portfolio.netlify.app">Portfolio</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-cyan?style=flat-square" />
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/platform-Linux-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
</p>

---

## 📦 Installation

### One-line Install (Recommended)
```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

### Manual Install
```bash
git clone https://github.com/subhobhai943/sub.git
cd sub
sudo make install
```

### Install .deb Package
Download the latest `.deb` from [Releases](https://github.com/subhobhai943/sub/releases), then:
```bash
sudo dpkg -i sub_1.0.0-1_all.deb
sudo apt-get install -f   # fix any missing deps
```

### Recommended Dependencies
```bash
sudo apt install nmap whois
```

---

## 🚀 Commands

| Command | Description |
|---|---|
| `sub whoami` | Info about the developer (Subhobhai) |
| `sub banner` | Print the SUB ASCII banner |
| `sub sysinfo` | Show current system info (OS, IP, CPU, uptime) |
| `sub version` | Show version |
| `sub scan <target>` | nmap scan on an IP or hostname |
| `sub ports <host>` | Quick check of 16 common ports |
| `sub whois <domain>` | WHOIS lookup for a domain |
| `sub dns <domain>` | DNS resolution |
| `sub ping <host>` | Ping a host |
| `sub headers <url>` | Fetch HTTP response headers |

---

## 💡 Examples

```bash
sub whoami
sub sysinfo
sub scan 192.168.1.1
sub ports scanme.nmap.org
sub whois google.com
sub dns github.com
sub headers https://github.com
```

---

## 🛠️ Build .deb from Source

```bash
git clone https://github.com/subhobhai943/sub.git
cd sub
bash build.sh
sudo dpkg -i ../sub_1.0.0-1_all.deb
```

---

## 📁 Project Structure

```
sub/
├── src/sub.py          # Main CLI script
├── debian/             # Debian packaging files
│   ├── control
│   ├── changelog
│   ├── copyright
│   ├── rules
│   └── install
├── .github/workflows/  # GitHub Actions (auto-build .deb)
├── Makefile
├── build.sh
├── install.sh          # One-line installer
└── README.md
```

---

## 📄 License

MIT — © 2026 [Subhobhai Sarkar](https://github.com/subhobhai943)
