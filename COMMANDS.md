# sub — Full Command Reference

> Version 2.0.0 | by Subhobhai | [github.com/subhobhai943/sub](https://github.com/subhobhai943/sub)

---

## INFO

| Command | Usage | Description |
|---|---|---|
| `banner` | `sub banner` | Show the SUB ASCII art banner |
| `whoami` | `sub whoami` | Full author info (Subhobhai) |
| `info` | `sub info` | OS, CPU, hostname, local IP, user, shell, time |
| `version` | `sub version` | Show sub version number |
| `langs` | `sub langs` | List all language implementations in the repo |

---

## NETWORK

| Command | Usage | Description |
|---|---|---|
| `myip` | `sub myip` | Local IP + public IP, city, ISP, timezone via ipinfo.io |
| `ping` | `sub ping <host> [-c N]` | Ping a host (default 4 packets) |
| `traceroute` | `sub traceroute <host>` | Trace route to a host |
| `dns` | `sub dns <host>` | DNS lookup (IPv4 + IPv6 + reverse DNS) |
| `headers` | `sub headers <url>` | Fetch HTTP response headers |
| `scan` | `sub scan <host> [--full]` | nmap service scan; `--full` scans all 65535 ports |
| `ports` | `sub ports <host> [-p 22,80,443]` | TCP port scan with banner grab on 30 common ports |

---

## RECON

| Command | Usage | Description |
|---|---|---|
| `whois` | `sub whois <domain>` | WHOIS domain lookup |
| `subdomains` | `sub subdomains <domain>` | Brute-force 60+ common subdomains via DNS |
| `robots` | `sub robots <domain>` | Fetch and print robots.txt |

---

## CRYPTO & ENCODING

| Command | Usage | Description |
|---|---|---|
| `hash` | `sub hash <text>` | Hash text with MD5, SHA1, SHA256, SHA512, BLAKE2b |
| `encode` | `sub encode <mode> <text>` | Encode: `base64` `base32` `hex` `url` `binary` `rot13` `morse` |
| `decode` | `sub decode <mode> <text>` | Decode: `base64` `base32` `hex` `url` `binary` `rot13` |
| `genpass` | `sub genpass [-l 20] [-n 3] [-s]` | Generate secure passwords; `-s` adds symbols |

---

## SYSTEM

| Command | Usage | Description |
|---|---|---|
| `procs` | `sub procs` | Running processes sorted by CPU |
| `diskuse` | `sub diskuse` | Disk usage + top 10 largest dirs in home |
| `netstat` | `sub netstat` | Active TCP/UDP connections via ss or netstat |

---

## FUN

| Command | Usage | Description |
|---|---|---|
| `matrix` | `sub matrix` | Matrix rain animation (Ctrl+C to stop) |
| `morse` | `sub morse <text>` | Convert text to Morse code |
| `figlet` | `sub figlet <text>` | Big ASCII text via figlet/toilet |

---

## MISC

| Command | Usage | Description |
|---|---|---|
| `update` | `sub update` | Pull latest from GitHub |

---

## Examples

```bash
sub whoami
sub myip
sub dns github.com
sub headers https://github.com
sub ports scanme.nmap.org
sub scan 192.168.1.1 --full
sub subdomains example.com
sub hash "hello world"
sub encode base64 "Subhobhai"
sub decode base64 "U3ViaG9iaGFp"
sub genpass -l 24 -n 3 -s
sub morse "SUB TOOL"
sub matrix
sub figlet sub
```
