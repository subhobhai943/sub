# sub — The SUB Hacking & Info Tool

> A mixed-purpose CLI tool by Subhobhai — hacking utilities + personal info + system recon.

## Install

```bash
curl -sL https://raw.githubusercontent.com/subhobhai943/sub/main/install.sh | sudo bash
```

Or via apt (after adding PPA):
```bash
sudo apt install sub
```

## Usage

```
sub whoami           # Info about Subhobhai (author)
sub banner           # ASCII art intro
sub scan <host>      # Network scan (nmap wrapper)
sub ports <host>     # Open port checker
sub info             # System info (OS, IP, CPU, uptime)
sub whois <domain>   # WHOIS lookup
sub update           # Self-update from GitHub
```

## Languages

- **Python** — Primary CLI (`src/python/sub.py`)
- **Kotlin** — JVM CLI (`src/kotlin/Sub.kt`)
- **Java** — JVM CLI (`src/java/Sub.java`)

## Build

```bash
bash build.sh
```

## Author

**Subhobhai (sub)**  
GitHub: [subhobhai943](https://github.com/subhobhai943)  
Portfolio: https://sub-portofolio.netlify.app  
Location: Durgapur, West Bengal, India
