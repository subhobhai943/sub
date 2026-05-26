#!/usr/bin/env python3
"""
sub - A powerful multi-purpose CLI tool by Subhobhai
Hacking utilities, personal info, system tools, and more.
"""

import argparse
import sys
import os
import socket
import subprocess
import platform
import datetime
import urllib.request
import urllib.parse
import json
import shutil
import time
import re

# ─────────────────────────────────────────────
# ANSI Colors
# ─────────────────────────────────────────────
class C:
    RED    = "\033[1;31m"
    GREEN  = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE   = "\033[1;34m"
    CYAN   = "\033[1;36m"
    WHITE  = "\033[1;37m"
    MAGENTA= "\033[1;35m"
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"

def c(color, text):
    return f"{color}{text}{C.RESET}"

# ─────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────
def show_banner():
    print(f"""{C.CYAN}
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ {C.RESET}
{C.YELLOW}  ─────────────────────────────────────────{C.RESET}
{C.WHITE}  Created by {C.GREEN}Subhobhai (subhobhai943){C.RESET}
{C.WHITE}  GitHub   : {C.BLUE}https://github.com/subhobhai943{C.RESET}
{C.WHITE}  Portfolio: {C.BLUE}https://sub-portofolio.netlify.app{C.RESET}
{C.WHITE}  Version  : {C.MAGENTA}1.0.0{C.RESET}
{C.YELLOW}  ─────────────────────────────────────────{C.RESET}
""")

# ─────────────────────────────────────────────
# WHOAMI - Personal info about Subhobhai
# ─────────────────────────────────────────────
def cmd_whoami():
    show_banner()
    info = [
        ("Name",        "Subhobhai Sarkar"),
        ("Alias",       "subhobhai943 / sub"),
        ("Location",    "Durgapur, West Bengal, India"),
        ("Role",        "Student · Developer · Open-Source Contributor"),
        ("Languages",   "C, C++, Python, Rust, Assembly, JS, PHP, Kotlin, Ruby"),
        ("Interests",   "OS Dev, Compiler Design, Game Engines, Hacking, AI/ML"),
        ("GitHub",      "https://github.com/subhobhai943"),
        ("Portfolio",   "https://sub-portofolio.netlify.app"),
        ("Repos",       "52 public · 44 private"),
        ("Followers",   "112"),
        ("Fun Fact",    "Building AIOS (custom OS with local LLM) + SUB lang (compiler in C/C++/Rust)"),
    ]
    print(c(C.CYAN, "  ◈ About the Creator"))
    print()
    for k, v in info:
        print(f"  {c(C.GREEN, k+':'): <30} {c(C.WHITE, v)}")
    print()

# ─────────────────────────────────────────────
# SYSINFO - Local machine info
# ─────────────────────────────────────────────
def cmd_sysinfo():
    print(c(C.CYAN, "\n  ◈ System Information\n"))
    uname = platform.uname()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "N/A"

    # Public IP
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=4) as r:
            public_ip = r.read().decode().strip()
    except:
        public_ip = "N/A (no internet)"

    rows = [
        ("OS",          f"{uname.system} {uname.release}"),
        ("Hostname",    hostname),
        ("Machine",     uname.machine),
        ("Processor",   uname.processor or platform.processor() or "N/A"),
        ("Python",      platform.python_version()),
        ("Local IP",    local_ip),
        ("Public IP",   public_ip),
        ("Date/Time",   now),
        ("Platform",    platform.platform()),
    ]

    # Uptime (Linux only)
    try:
        with open("/proc/uptime") as f:
            up_seconds = float(f.read().split()[0])
            m, s = divmod(int(up_seconds), 60)
            h, m = divmod(m, 60)
            rows.append(("Uptime", f"{h}h {m}m {s}s"))
    except:
        pass

    # Disk usage
    try:
        total, used, free = shutil.disk_usage("/")
        rows.append(("Disk (/ )", f"Total: {total//2**30}GB  Used: {used//2**30}GB  Free: {free//2**30}GB"))
    except:
        pass

    for k, v in rows:
        print(f"  {c(C.GREEN, k+':'): <30} {c(C.WHITE, v)}")
    print()

# ─────────────────────────────────────────────
# SCAN - Nmap wrapper
# ─────────────────────────────────────────────
def cmd_scan(target, flags=None):
    if not shutil.which("nmap"):
        print(c(C.RED, "  [!] nmap not found. Install it: sudo apt install nmap"))
        return
    print(c(C.CYAN, f"\n  ◈ Scanning {target}...\n"))
    nmap_flags = flags if flags else "-sV --open -T4"
    cmd = f"nmap {nmap_flags} {target}"
    print(c(C.DIM, f"  $ {cmd}\n"))
    os.system(cmd)

# ─────────────────────────────────────────────
# PORTS - Quick TCP port scan
# ─────────────────────────────────────────────
def cmd_ports(host, start=1, end=1024):
    print(c(C.CYAN, f"\n  ◈ Port Scan: {host} [{start}-{end}]\n"))
    open_ports = []
    try:
        ip = socket.gethostbyname(host)
        print(c(C.DIM, f"  Resolved: {host} → {ip}\n"))
    except:
        print(c(C.RED, f"  [!] Cannot resolve: {host}"))
        return
    print(c(C.YELLOW, f"  Scanning {end - start + 1} ports..."))
    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"  {c(C.GREEN, f'[OPEN]')} Port {c(C.WHITE, str(port)):<10} {c(C.DIM, service)}")
            open_ports.append(port)
        sock.close()
    print()
    if not open_ports:
        print(c(C.YELLOW, "  No open ports found in range."))
    else:
        print(c(C.GREEN, f"  Total open: {len(open_ports)} port(s)"))
    print()

# ─────────────────────────────────────────────
# WHOIS - Domain WHOIS lookup
# ─────────────────────────────────────────────
def cmd_whois(domain):
    if not shutil.which("whois"):
        print(c(C.RED, "  [!] whois not found. Install: sudo apt install whois"))
        return
    print(c(C.CYAN, f"\n  ◈ WHOIS: {domain}\n"))
    os.system(f"whois {domain}")

# ─────────────────────────────────────────────
# DNS - DNS record lookup
# ─────────────────────────────────────────────
def cmd_dns(domain):
    print(c(C.CYAN, f"\n  ◈ DNS Lookup: {domain}\n"))
    tools = [
        ("A Record",    f"dig +short A {domain}"),
        ("AAAA Record", f"dig +short AAAA {domain}"),
        ("MX Record",   f"dig +short MX {domain}"),
        ("TXT Record",  f"dig +short TXT {domain}"),
        ("NS Record",   f"dig +short NS {domain}"),
        ("CNAME",       f"dig +short CNAME {domain}"),
    ]
    if not shutil.which("dig"):
        print(c(C.RED, "  [!] dig not found. Install: sudo apt install dnsutils"))
        return
    for label, cmd in tools:
        result = subprocess.getoutput(cmd).strip()
        if result:
            print(f"  {c(C.GREEN, label+':'): <30} {c(C.WHITE, result)}")
    print()

# ─────────────────────────────────────────────
# IPINFO - IP geolocation info
# ─────────────────────────────────────────────
def cmd_ipinfo(ip):
    print(c(C.CYAN, f"\n  ◈ IP Info: {ip}\n"))
    try:
        url = f"https://ipinfo.io/{ip}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "sub-tool/1.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode())
        fields = ["ip","hostname","city","region","country","loc","org","timezone"]
        for f_ in fields:
            if f_ in data:
                print(f"  {c(C.GREEN, f_.capitalize()+':'): <30} {c(C.WHITE, data[f_])}")
    except Exception as e:
        print(c(C.RED, f"  [!] Failed: {e}"))
    print()

# ─────────────────────────────────────────────
# PING - Ping a host
# ─────────────────────────────────────────────
def cmd_ping(host, count=4):
    print(c(C.CYAN, f"\n  ◈ Pinging {host} (count={count})\n"))
    flag = "-c" if platform.system() != "Windows" else "-n"
    os.system(f"ping {flag} {count} {host}")
    print()

# ─────────────────────────────────────────────
# TRACEROUTE
# ─────────────────────────────────────────────
def cmd_traceroute(host):
    print(c(C.CYAN, f"\n  ◈ Traceroute: {host}\n"))
    tool = "traceroute" if shutil.which("traceroute") else "tracepath"
    os.system(f"{tool} {host}")
    print()

# ─────────────────────────────────────────────
# HASH - Hash a string or file
# ─────────────────────────────────────────────
def cmd_hash(target, algo="all"):
    import hashlib
    algos = ["md5","sha1","sha224","sha256","sha384","sha512"]
    if algo != "all" and algo not in algos:
        print(c(C.RED, f"  [!] Unknown algorithm. Choose: {', '.join(algos)}"))
        return

    print(c(C.CYAN, f"\n  ◈ Hash: {target}\n"))
    is_file = os.path.isfile(target)
    if is_file:
        with open(target, "rb") as f_:
            data = f_.read()
        print(c(C.DIM, f"  Mode: File ({os.path.getsize(target)} bytes)"))
    else:
        data = target.encode()
        print(c(C.DIM, f"  Mode: String"))
    print()

    chosen = algos if algo == "all" else [algo]
    for a in chosen:
        h = hashlib.new(a, data).hexdigest()
        print(f"  {c(C.GREEN, a.upper()+':'): <30} {c(C.WHITE, h)}")
    print()

# ─────────────────────────────────────────────
# ENCODE / DECODE - Base64
# ─────────────────────────────────────────────
def cmd_encode(text, mode="b64"):
    import base64
    print(c(C.CYAN, f"\n  ◈ Encode [{mode}]\n"))
    if mode == "b64":
        result = base64.b64encode(text.encode()).decode()
    elif mode == "b64d":
        try:
            result = base64.b64decode(text.encode()).decode()
        except Exception as e:
            print(c(C.RED, f"  [!] Decode error: {e}")); return
    elif mode == "hex":
        result = text.encode().hex()
    elif mode == "hexd":
        try:
            result = bytes.fromhex(text).decode()
        except Exception as e:
            print(c(C.RED, f"  [!] Decode error: {e}")); return
    elif mode == "url":
        result = urllib.parse.quote(text)
    elif mode == "urld":
        result = urllib.parse.unquote(text)
    else:
        print(c(C.RED, f"  [!] Unknown mode: {mode}"))
        print(c(C.DIM, "  Available: b64, b64d, hex, hexd, url, urld"))
        return
    print(f"  {c(C.GREEN, 'Input :')} {text}")
    print(f"  {c(C.GREEN, 'Output:')} {c(C.WHITE, result)}")
    print()

# ─────────────────────────────────────────────
# GENERATE - Password / token generator
# ─────────────────────────────────────────────
def cmd_generate(gentype="password", length=16):
    import secrets
    import string
    print(c(C.CYAN, f"\n  ◈ Generate: {gentype} (len={length})\n"))
    if gentype == "password":
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        result = "".join(secrets.choice(chars) for _ in range(length))
    elif gentype == "pin":
        result = "".join(secrets.choice(string.digits) for _ in range(length))
    elif gentype == "hex":
        result = secrets.token_hex(length)
    elif gentype == "token":
        result = secrets.token_urlsafe(length)
    elif gentype == "uuid":
        import uuid
        result = str(uuid.uuid4())
    else:
        print(c(C.RED, f"  [!] Unknown type. Choose: password, pin, hex, token, uuid"))
        return
    print(f"  {c(C.GREEN, 'Generated:')} {c(C.WHITE, result)}")
    print(f"  {c(C.DIM,   'Length   :')} {len(result)} chars")
    print()

# ─────────────────────────────────────────────
# HEADERS - HTTP headers of a URL
# ─────────────────────────────────────────────
def cmd_headers(url):
    if not url.startswith("http"):
        url = "https://" + url
    print(c(C.CYAN, f"\n  ◈ HTTP Headers: {url}\n"))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "sub-tool/1.0", "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=8) as r:
            status = r.status
            headers = dict(r.headers)
        print(f"  {c(C.GREEN, 'Status:')} {c(C.WHITE, str(status))}\n")
        for k, v in sorted(headers.items()):
            print(f"  {c(C.GREEN, k+':'): <40} {c(C.WHITE, v)}")
    except urllib.error.HTTPError as e:
        print(f"  {c(C.YELLOW, 'HTTP Error:')} {e.code} {e.reason}")
        for k, v in sorted(dict(e.headers).items()):
            print(f"  {c(C.GREEN, k+':'): <40} {c(C.WHITE, v)}")
    except Exception as e:
        print(c(C.RED, f"  [!] Error: {e}"))
    print()

# ─────────────────────────────────────────────
# MYREPOS - Show GitHub repos
# ─────────────────────────────────────────────
def cmd_myrepos(username="subhobhai943", limit=20):
    print(c(C.CYAN, f"\n  ◈ GitHub Repos: {username}\n"))
    try:
        url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "sub-tool/1.0", "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=8) as r:
            repos = json.loads(r.read().decode())
        print(f"  {'Name':<40} {'Stars':>6}  {'Lang':<15} {'Updated'}")
        print(f"  {'─'*40} {'─'*6}  {'─'*15} {'─'*20}")
        for repo in repos:
            name  = (repo['name'] or "")[:38]
            stars = repo.get('stargazers_count', 0)
            lang  = (repo.get('language') or "N/A")[:14]
            upd   = (repo.get('updated_at') or "")[:10]
            print(f"  {c(C.GREEN, name):<50} {c(C.YELLOW, str(stars)):>6}  {c(C.BLUE, lang):<25} {c(C.DIM, upd)}")
    except Exception as e:
        print(c(C.RED, f"  [!] Failed: {e}"))
    print()

# ─────────────────────────────────────────────
# SUBDOMAIN - Subdomain brute-force
# ─────────────────────────────────────────────
def cmd_subdomain(domain, wordlist=None):
    print(c(C.CYAN, f"\n  ◈ Subdomain Finder: {domain}\n"))
    default_subs = [
        "www","mail","ftp","admin","api","dev","test","staging","app",
        "blog","shop","vpn","cdn","static","media","portal","dashboard",
        "secure","login","auth","beta","m","mobile","support","help",
        "docs","wiki","status","monitor","git","gitlab","jenkins","ci"
    ]
    subs = default_subs
    if wordlist and os.path.isfile(wordlist):
        with open(wordlist) as wf:
            subs = [l.strip() for l in wf if l.strip()]
        print(c(C.DIM, f"  Wordlist: {wordlist} ({len(subs)} entries)\n"))
    else:
        print(c(C.DIM, f"  Using built-in wordlist ({len(subs)} entries)\n"))
    found = 0
    for sub in subs:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            print(f"  {c(C.GREEN, '[FOUND]')} {c(C.WHITE, host): <50} → {c(C.CYAN, ip)}")
            found += 1
        except:
            pass
    print()
    print(c(C.GREEN if found else C.YELLOW, f"  Found: {found} subdomain(s)"))
    print()

# ─────────────────────────────────────────────
# BANNER GRAB - Grab service banner
# ─────────────────────────────────────────────
def cmd_banner_grab(host, port):
    print(c(C.CYAN, f"\n  ◈ Banner Grab: {host}:{port}\n"))
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((host, int(port)))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        print(c(C.WHITE, banner))
    except Exception as e:
        print(c(C.RED, f"  [!] Failed: {e}"))
    print()

# ─────────────────────────────────────────────
# NETSTAT - Active connections
# ─────────────────────────────────────────────
def cmd_netstat():
    print(c(C.CYAN, "\n  ◈ Network Connections\n"))
    os.system("ss -tulpn 2>/dev/null || netstat -tulpn")
    print()

# ─────────────────────────────────────────────
# CRACK (educational) - Hash identifier
# ─────────────────────────────────────────────
def cmd_hashid(hashval):
    print(c(C.CYAN, f"\n  ◈ Hash Identifier: {hashval}\n"))
    patterns = [
        (r"^[a-f0-9]{32}$",  "MD5"),
        (r"^[a-f0-9]{40}$",  "SHA-1"),
        (r"^[a-f0-9]{56}$",  "SHA-224"),
        (r"^[a-f0-9]{64}$",  "SHA-256"),
        (r"^[a-f0-9]{96}$",  "SHA-384"),
        (r"^[a-f0-9]{128}$", "SHA-512"),
        (r"^\$2[ayb]\$.{56}$", "bcrypt"),
        (r"^\$1\$.{22}$",    "MD5-crypt"),
        (r"^\$6\$.{86}$",    "SHA-512-crypt"),
        (r"^[a-z0-9]{13}$",  "DES (Unix)"),
        (r"^[A-Za-z0-9+/]{43}=$", "SHA-256 (base64)"),
    ]
    matched = []
    for pat, name in patterns:
        if re.match(pat, hashval, re.IGNORECASE):
            matched.append(name)
    if matched:
        for m in matched:
            print(f"  {c(C.GREEN, '[+]')} Possible type: {c(C.WHITE, m)}")
    else:
        print(c(C.YELLOW, "  [?] Unknown or custom hash format"))
    print(f"  {c(C.DIM, 'Length:')} {len(hashval)} chars")
    print()

# ─────────────────────────────────────────────
# WEATHER - Quick weather check
# ─────────────────────────────────────────────
def cmd_weather(city="Durgapur"):
    print(c(C.CYAN, f"\n  ◈ Weather: {city}\n"))
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=v2"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = r.read().decode()
        print(data)
    except Exception as e:
        print(c(C.RED, f"  [!] Failed: {e}"))

# ─────────────────────────────────────────────
# MYIP - Get own public IP
# ─────────────────────────────────────────────
def cmd_myip():
    print(c(C.CYAN, "\n  ◈ My Public IP\n"))
    services = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://checkip.amazonaws.com",
    ]
    for svc in services:
        try:
            req = urllib.request.Request(svc, headers={"User-Agent": "sub-tool/1.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                ip = r.read().decode().strip()
            print(f"  {c(C.GREEN, 'Public IP:')} {c(C.WHITE, ip)}")
            cmd_ipinfo(ip)
            return
        except:
            continue
    print(c(C.RED, "  [!] Could not determine public IP"))
    print()

# ─────────────────────────────────────────────
# VERSION / HELP
# ─────────────────────────────────────────────
def cmd_version():
    print(f"  sub v1.0.0 — by Subhobhai (subhobhai943)")
    print(f"  {c(C.DIM, 'https://github.com/subhobhai943/sub')}")
    print()

def cmd_help():
    show_banner()
    print(c(C.WHITE, "  USAGE: sub <command> [options]\n"))
    commands = [
        ("whoami",               "",                   "Show info about the creator (Subhobhai)"),
        ("sysinfo",              "",                   "System info: OS, IP, CPU, uptime, disk"),
        ("myip",                 "",                   "Show your public IP + geolocation"),
        ("scan",                 "<host> [--flags]",   "Nmap scan a host/IP"),
        ("ports",                "<host> [--start] [--end]", "TCP port scan (built-in)"),
        ("subdomain",            "<domain> [--wordlist]","Brute-force subdomains"),
        ("banner-grab",          "<host> <port>",      "Grab service banner from port"),
        ("dns",                  "<domain>",           "DNS record lookup (A/AAAA/MX/TXT/NS)"),
        ("whois",                "<domain>",           "WHOIS domain lookup"),
        ("ipinfo",               "<ip>",               "IP geolocation (ipinfo.io)"),
        ("ping",                 "<host> [--count]",   "Ping a host"),
        ("traceroute",           "<host>",             "Trace network route"),
        ("headers",              "<url>",              "HTTP response headers"),
        ("netstat",              "",                   "Show active network connections"),
        ("hash",                 "<text|file> [--algo]","Hash a string or file (MD5/SHA*)"),
        ("hashid",               "<hash>",             "Identify hash type"),
        ("encode",               "<text> --mode",      "Encode: b64/hex/url + decode variants"),
        ("generate",             "--type --length",    "Generate: password/pin/hex/token/uuid"),
        ("weather",              "[city]",             "Check weather (default: Durgapur)"),
        ("myrepos",              "[--user] [--limit]", "List GitHub repos"),
        ("version",              "",                   "Show version"),
    ]
    cat = None
    cats = {
        "─── Info ──────────────": ["whoami","sysinfo","myip","version"],
        "─── Recon / Hacking ──": ["scan","ports","subdomain","banner-grab","dns","whois","ipinfo","ping","traceroute","headers","netstat"],
        "─── Crypto / Encoding": ["hash","hashid","encode"],
        "─── Utilities ────────": ["generate","weather","myrepos"],
    }
    cmd_dict = {c_[0]: c_ for c_ in commands}
    for cat_label, cmd_list in cats.items():
        print(f"\n  {c(C.YELLOW, cat_label)}")
        for name in cmd_list:
            if name in cmd_dict:
                _, args, desc = cmd_dict[name]
                arg_str = c(C.DIM, args) if args else ""
                print(f"    {c(C.GREEN, 'sub '+name):<40} {arg_str:<30} {desc}")
    print()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    parser = argparse.ArgumentParser(prog="sub", add_help=False)
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("target",  nargs="?", default=None)
    parser.add_argument("--flags",    default=None)
    parser.add_argument("--start",    type=int, default=1)
    parser.add_argument("--end",      type=int, default=1024)
    parser.add_argument("--count",    type=int, default=4)
    parser.add_argument("--algo",     default="all")
    parser.add_argument("--mode",     default="b64")
    parser.add_argument("--type",     default="password")
    parser.add_argument("--length",   type=int, default=16)
    parser.add_argument("--user",     default="subhobhai943")
    parser.add_argument("--limit",    type=int, default=20)
    parser.add_argument("--wordlist", default=None)
    parser.add_argument("--port",     default=None)
    args = parser.parse_args()

    cmd = args.command.lower()

    if   cmd in ("help", "-h", "--help"):   cmd_help()
    elif cmd == "whoami":                    cmd_whoami()
    elif cmd == "sysinfo":                   cmd_sysinfo()
    elif cmd == "myip":                      cmd_myip()
    elif cmd == "scan":
        if not args.target: print(c(C.RED, "  Usage: sub scan <host> [--flags '...']")); return
        cmd_scan(args.target, args.flags)
    elif cmd == "ports":
        if not args.target: print(c(C.RED, "  Usage: sub ports <host> [--start N] [--end N]")); return
        cmd_ports(args.target, args.start, args.end)
    elif cmd == "subdomain":
        if not args.target: print(c(C.RED, "  Usage: sub subdomain <domain> [--wordlist path]")); return
        cmd_subdomain(args.target, args.wordlist)
    elif cmd == "banner-grab":
        if not args.target or not args.port: print(c(C.RED, "  Usage: sub banner-grab <host> --port <port>")); return
        cmd_banner_grab(args.target, args.port)
    elif cmd == "dns":
        if not args.target: print(c(C.RED, "  Usage: sub dns <domain>")); return
        cmd_dns(args.target)
    elif cmd == "whois":
        if not args.target: print(c(C.RED, "  Usage: sub whois <domain>")); return
        cmd_whois(args.target)
    elif cmd == "ipinfo":
        if not args.target: print(c(C.RED, "  Usage: sub ipinfo <ip>")); return
        cmd_ipinfo(args.target)
    elif cmd == "ping":
        if not args.target: print(c(C.RED, "  Usage: sub ping <host> [--count N]")); return
        cmd_ping(args.target, args.count)
    elif cmd == "traceroute":
        if not args.target: print(c(C.RED, "  Usage: sub traceroute <host>")); return
        cmd_traceroute(args.target)
    elif cmd == "headers":
        if not args.target: print(c(C.RED, "  Usage: sub headers <url>")); return
        cmd_headers(args.target)
    elif cmd == "netstat":                   cmd_netstat()
    elif cmd == "hash":
        if not args.target: print(c(C.RED, "  Usage: sub hash <text|file> [--algo md5|sha256|...]")); return
        cmd_hash(args.target, args.algo)
    elif cmd == "hashid":
        if not args.target: print(c(C.RED, "  Usage: sub hashid <hashvalue>")); return
        cmd_hashid(args.target)
    elif cmd == "encode":
        if not args.target: print(c(C.RED, "  Usage: sub encode <text> --mode b64|b64d|hex|hexd|url|urld")); return
        cmd_encode(args.target, args.mode)
    elif cmd == "generate":                  cmd_generate(args.type, args.length)
    elif cmd == "weather":                   cmd_weather(args.target or "Durgapur")
    elif cmd == "myrepos":                   cmd_myrepos(args.user, args.limit)
    elif cmd == "version":                   cmd_version()
    elif cmd == "banner":                    show_banner()
    else:
        print(c(C.RED, f"  [!] Unknown command: '{cmd}'"))
        print(c(C.DIM, "  Run 'sub help' to see all commands."))

if __name__ == "__main__":
    main()
