#!/usr/bin/env python3
"""
sub - The SUB Hacking & Info Tool
Author : Subhobhai Sarkar (subhobhai943)
GitHub : https://github.com/subhobhai943
Version: 2.0.0

Commands:
  INFO      : banner, whoami, info, version
  NETWORK   : scan, ports, ping, traceroute, dns, headers, myip
  RECON     : whois, subdomains, robots
  CRYPTO    : encode, decode, hash, genpass
  SYSTEM    : procs, diskuse, netstat
  FUN       : matrix, morse, figlet
  MISC      : update, langs
"""

import argparse
import os
import sys
import subprocess
import platform
import socket
import hashlib
import base64
import random
import string
import datetime
import urllib.request
import urllib.error
import json
import time
import shutil

# ─────────────────────────────────────────────
# ANSI Colors
# ─────────────────────────────────────────────
R  = "\033[0m"
G  = "\033[1;32m"
C  = "\033[1;36m"
Y  = "\033[1;33m"
RD = "\033[1;31m"
B  = "\033[1;34m"
M  = "\033[1;35m"
W  = "\033[1;37m"

VERSION = "2.0.0"

BANNER = f"""
{G}  ███████╗██╗   ██╗██████╗ {R}
{G}  ██╔════╝██║   ██║██╔══██╗{R}
{G}  ███████╗██║   ██║██████╔╝{R}
{Y}  ╚════██║██║   ██║██╔══██╗{R}
{Y}  ███████║╚██████╔╝██████╔╝{R}
{Y}  ╚══════╝ ╚═════╝ ╚═════╝ {R}
  {C}by Subhobhai{R} | {B}github.com/subhobhai943{R} | {W}v{VERSION}{R}
"""

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _exists(tool):
    return shutil.which(tool) is not None

def _run(cmd):
    subprocess.run(cmd)

def _header(title):
    print(f"\n{C}{'─'*50}{R}")
    print(f"{C}  {title}{R}")
    print(f"{C}{'─'*50}{R}")

def _ok(msg):   print(f"  {G}[+]{R} {msg}")
def _warn(msg): print(f"  {Y}[!]{R} {msg}")
def _err(msg):  print(f"  {RD}[x]{R} {msg}")
def _info(msg): print(f"  {C}[*]{R} {msg}")
def _row(k, v): print(f"  {G}{k:<14}{R}: {v}")

# ─────────────────────────────────────────────
# INFO COMMANDS
# ─────────────────────────────────────────────
def cmd_banner(args):
    print(BANNER)

def cmd_version(args):
    print(f"\n  sub version {G}{VERSION}{R}")
    print(f"  GitHub: {B}https://github.com/subhobhai943/sub{R}\n")

def cmd_whoami(args):
    print(BANNER)
    _header("Author Info")
    rows = [
        ("Name",      "Subhobhai Sarkar"),
        ("Alias",     "sub"),
        ("GitHub",    "https://github.com/subhobhai943"),
        ("Portfolio", "https://sub-portofolio.netlify.app"),
        ("Location",  "Durgapur, West Bengal, India"),
        ("Bio",       "PCMB student | Web, AI, C++/C# game dev | Open-source hacker"),
        ("Projects",  "AIOS, SUB lang, Discord bots, 3D web games"),
        ("Languages", "Python, C, C++, Rust, Kotlin, Java, JS, Haxe, CUDA, M4, x86-64/AArch64 ASM"),
        ("Tools",     "nmap, git, docker, ghidra, burpsuite, metasploit"),
        ("Interests", "Compilers, OS dev, Game engines, AI/ML, CTF"),
    ]
    for k, v in rows:
        _row(k, v)
    print()

def cmd_langs(args):
    _header("sub — Language Implementations")
    langs = [
        ("Python",       "src/python/sub.py",      "Primary CLI (this file)"),
        ("Kotlin",       "src/kotlin/Sub.kt",       "JVM — kotlinc + jar"),
        ("Java",         "src/java/Sub.java",       "JVM — javac + jar"),
        ("x86-64 ASM",   "src/asm/x86_64/sub.asm", "NASM — Linux Intel/AMD"),
        ("AArch64 ASM",  "src/asm/aarch64/sub.s",  "GAS — Raspberry Pi, Termux, ARM"),
        ("M4",           "src/m4/sub.m4",           "GNU Macro Processor"),
        ("CUDA",         "src/cuda/sub.cu",         "NVIDIA GPU — nvcc"),
        ("Haxe",         "src/haxe/Sub.hx",         "Compiles to JS/Python/C++/Java"),
    ]
    for lang, path, desc in langs:
        print(f"  {G}{lang:<14}{R}  {Y}{path:<32}{R}  {desc}")
    print()

# ─────────────────────────────────────────────
# SYSTEM COMMANDS
# ─────────────────────────────────────────────
def cmd_info(args):
    _header("System Information")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        hostname, local_ip = "unknown", "unknown"
    uname = platform.uname()
    _row("OS",       f"{uname.system} {uname.release}")
    _row("Kernel",   uname.version[:60] if len(uname.version) > 60 else uname.version)
    _row("Arch",     uname.machine)
    _row("Hostname", hostname)
    _row("Local IP", local_ip)
    _row("CPU",      uname.processor or platform.processor() or "unknown")
    _row("Python",   platform.python_version())
    _row("User",     os.environ.get("USER") or os.environ.get("USERNAME") or "unknown")
    _row("Home",     os.path.expanduser("~"))
    _row("Shell",    os.environ.get("SHELL", "unknown"))
    _row("Time",     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()

def cmd_procs(args):
    _header("Running Processes (top 20 by CPU)")
    if _exists("ps"):
        subprocess.run(["ps", "aux", "--sort=-%cpu"], )
    else:
        _err("ps not found.")

def cmd_diskuse(args):
    _header("Disk Usage")
    if _exists("df"):
        subprocess.run(["df", "-h"])
    else:
        _err("df not found.")
    print()
    _header("Top 10 Largest Dirs in Home")
    home = os.path.expanduser("~")
    if _exists("du"):
        subprocess.run(f"du -ah {home} 2>/dev/null | sort -rh | head -10", shell=True)

def cmd_netstat(args):
    _header("Active Network Connections")
    if _exists("ss"):
        subprocess.run(["ss", "-tulnp"])
    elif _exists("netstat"):
        subprocess.run(["netstat", "-tulnp"])
    else:
        _err("Neither ss nor netstat found. Install: sudo apt install iproute2")

# ─────────────────────────────────────────────
# NETWORK COMMANDS
# ─────────────────────────────────────────────
def cmd_myip(args):
    _header("Your IP Information")
    # Local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "unknown"
    _row("Local IP", local_ip)
    # Public IP via ipinfo.io
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=5) as r:
            data = json.loads(r.read().decode())
        _row("Public IP", data.get("ip", "unknown"))
        _row("City",      data.get("city", "unknown"))
        _row("Region",    data.get("region", "unknown"))
        _row("Country",   data.get("country", "unknown"))
        _row("ISP",       data.get("org", "unknown"))
        _row("Timezone",  data.get("timezone", "unknown"))
    except Exception:
        _warn("Could not fetch public IP (no internet or blocked).")
    print()

def cmd_ping(args):
    host = args.target
    count = str(args.count)
    _header(f"Ping: {host} (x{count})")
    flag = "-c" if platform.system() != "Windows" else "-n"
    subprocess.run(["ping", flag, count, host])

def cmd_traceroute(args):
    host = args.target
    _header(f"Traceroute: {host}")
    if _exists("traceroute"):
        subprocess.run(["traceroute", host])
    elif _exists("tracert"):
        subprocess.run(["tracert", host])
    else:
        _err("traceroute not found. Install: sudo apt install traceroute")

def cmd_dns(args):
    host = args.target
    _header(f"DNS Lookup: {host}")
    try:
        results = socket.getaddrinfo(host, None)
        seen = set()
        for res in results:
            ip = res[4][0]
            if ip not in seen:
                seen.add(ip)
                family = "IPv6" if res[0].name == "AF_INET6" else "IPv4"
                _row(family, ip)
    except Exception as e:
        _err(f"DNS lookup failed: {e}")
    # Reverse DNS
    print()
    try:
        rev = socket.gethostbyaddr(socket.gethostbyname(host))
        _row("Reverse", rev[0])
    except Exception:
        pass
    print()

def cmd_headers(args):
    url = args.url
    if not url.startswith("http"):
        url = "http://" + url
    _header(f"HTTP Headers: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"sub/{VERSION}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            _row("Status", str(r.status))
            for k, v in r.headers.items():
                _row(k, v)
    except Exception as e:
        _err(f"Request failed: {e}")
    print()

def cmd_scan(args):
    host = args.target
    _header(f"Network Scan: {host}")
    if not _exists("nmap"):
        _err("nmap not found. Install: sudo apt install nmap")
        sys.exit(1)
    flags = ["-sV", "-T4", "--open"]
    if args.full:
        flags = ["-sV", "-T4", "-p-", "--open"]
    subprocess.run(["nmap"] + flags + [host])

def cmd_ports(args):
    host = args.target
    custom = args.ports
    if custom:
        try:
            port_list = [int(p) for p in custom.split(",")]
        except ValueError:
            _err("Invalid port list. Use comma-separated integers: 22,80,443")
            return
    else:
        port_list = [21,22,23,25,53,80,110,143,389,443,445,
                     587,993,995,1433,1521,2181,3000,3306,
                     3389,4444,5432,5900,6379,8080,8443,8888,9200,27017]
    _header(f"Port Scan: {host}")
    open_count = 0
    for port in port_list:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            s.close()
            if result == 0:
                open_count += 1
                # Try banner grab
                banner = ""
                try:
                    bs = socket.socket()
                    bs.settimeout(1)
                    bs.connect((host, port))
                    bs.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    raw = bs.recv(256).decode(errors="ignore").split("\n")[0].strip()
                    banner = f"  {raw[:60]}" if raw else ""
                    bs.close()
                except Exception:
                    pass
                print(f"  {G}OPEN{R}  {port:<6} {banner}")
            else:
                print(f"  {RD}CLOSED{R} {port}")
        except Exception:
            print(f"  {Y}ERROR{R}  {port}")
    print(f"\n  {G}[+]{R} {open_count} open port(s) found on {host}\n")

# ─────────────────────────────────────────────
# RECON COMMANDS
# ─────────────────────────────────────────────
def cmd_whois(args):
    domain = args.domain
    _header(f"WHOIS: {domain}")
    if _exists("whois"):
        subprocess.run(["whois", domain])
    else:
        _err("whois not found. Install: sudo apt install whois")
        sys.exit(1)

def cmd_subdomains(args):
    domain = args.domain
    _header(f"Subdomain Recon: {domain}")
    wordlist = [
        "www","mail","ftp","smtp","pop","imap","webmail","remote","blog",
        "dev","stage","staging","test","api","portal","vpn","admin","cp",
        "cpanel","ns1","ns2","dns","cdn","shop","store","m","mobile",
        "app","dashboard","support","help","forum","community","beta",
        "git","gitlab","github","jenkins","ci","static","assets","media",
        "img","images","upload","uploads","docs","status","monitor","grafana",
        "kibana","elk","analytics","track","auth","login","sso","id","oauth",
    ]
    found = []
    _info(f"Testing {len(wordlist)} subdomains...")
    for sub in wordlist:
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            found.append((fqdn, ip))
            _ok(f"{G}{fqdn:<40}{R} -> {ip}")
        except socket.gaierror:
            pass
    print(f"\n  {G}[+]{R} Found {len(found)} subdomains for {domain}\n")

def cmd_robots(args):
    domain = args.domain
    url = f"https://{domain}/robots.txt"
    _header(f"robots.txt: {domain}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"sub/{VERSION}"})
        with urllib.request.urlopen(req, timeout=8) as r:
            content = r.read().decode(errors="ignore")
            print(content)
    except Exception:
        url = f"http://{domain}/robots.txt"
        try:
            with urllib.request.urlopen(url, timeout=8) as r:
                print(r.read().decode(errors="ignore"))
        except Exception as e:
            _err(f"Could not fetch robots.txt: {e}")

# ─────────────────────────────────────────────
# CRYPTO / ENCODING COMMANDS
# ─────────────────────────────────────────────
def cmd_hash(args):
    text = args.text
    _header(f"Hash: \"{text}\"")
    algos = ["md5","sha1","sha224","sha256","sha384","sha512","sha3_256","blake2b"]
    for algo in algos:
        try:
            h = hashlib.new(algo, text.encode()).hexdigest()
            _row(algo.upper(), h)
        except Exception:
            pass
    print()

def cmd_encode(args):
    text = args.text
    mode = args.mode
    _header(f"Encode [{mode}]: \"{text}\"")
    if mode == "base64":
        result = base64.b64encode(text.encode()).decode()
    elif mode == "base32":
        result = base64.b32encode(text.encode()).decode()
    elif mode == "hex":
        result = text.encode().hex()
    elif mode == "url":
        import urllib.parse
        result = urllib.parse.quote(text)
    elif mode == "binary":
        result = " ".join(format(ord(c), "08b") for c in text)
    elif mode == "rot13":
        import codecs
        result = codecs.encode(text, "rot_13")
    elif mode == "morse":
        result = _to_morse(text)
    else:
        _err(f"Unknown mode: {mode}")
        return
    _ok(result)
    print()

def cmd_decode(args):
    text = args.text
    mode = args.mode
    _header(f"Decode [{mode}]: \"{text}\"")
    try:
        if mode == "base64":
            result = base64.b64decode(text).decode()
        elif mode == "base32":
            result = base64.b32decode(text).decode()
        elif mode == "hex":
            result = bytes.fromhex(text).decode()
        elif mode == "url":
            import urllib.parse
            result = urllib.parse.unquote(text)
        elif mode == "binary":
            result = "".join(chr(int(b, 2)) for b in text.split())
        elif mode == "rot13":
            import codecs
            result = codecs.encode(text, "rot_13")
        else:
            _err(f"Unknown mode: {mode}")
            return
        _ok(result)
    except Exception as e:
        _err(f"Decode failed: {e}")
    print()

def cmd_genpass(args):
    length = args.length
    count  = args.count
    _header(f"Password Generator ({length} chars x {count})")
    chars = string.ascii_letters + string.digits
    if args.symbols:
        chars += string.punctuation
    for i in range(count):
        pw = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        print(f"  {G}{i+1:>2}.{R} {pw}")
    print()

# ─────────────────────────────────────────────
# FUN COMMANDS
# ─────────────────────────────────────────────
MORSE_MAP = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....',
    'I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
    'Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--',' ':'/'
}

def _to_morse(text):
    return " ".join(MORSE_MAP.get(c.upper(), "?") for c in text)

def cmd_morse(args):
    text = args.text
    _header("Morse Code")
    _row("Input",  text)
    _row("Morse",  _to_morse(text))
    print()

def cmd_matrix(args):
    cols = shutil.get_terminal_size((80, 24)).columns
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    _info("Matrix rain — press Ctrl+C to stop")
    time.sleep(0.5)
    try:
        while True:
            line = G + "".join(random.choice(chars) if random.random() > 0.1 else " " for _ in range(cols)) + R
            print(line)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print(f"\n{R}")

def cmd_figlet(args):
    text = args.text
    _header(f"Figlet: {text}")
    if _exists("figlet"):
        subprocess.run(["figlet", "-f", "banner", text])
    elif _exists("toilet"):
        subprocess.run(["toilet", "-f", "future", text])
    else:
        _warn("figlet/toilet not found. Install: sudo apt install figlet")
        # Fallback: block letters for short text
        print(f"  >>> {text.upper()} <<<")
    print()

# ─────────────────────────────────────────────
# MISC
# ─────────────────────────────────────────────
def cmd_update(args):
    _header("Self Update")
    _info("Pulling latest from GitHub...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root  = os.path.abspath(os.path.join(script_dir, "../.."))
    result = subprocess.run(["git", "-C", repo_root, "pull"], capture_output=True, text=True)
    if result.returncode == 0:
        _ok(result.stdout.strip())
    else:
        _err(result.stderr.strip())
    print()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="sub",
        description=f"{G}sub v{VERSION}{R} — Hacking & Info Tool by Subhobhai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"  {C}INFO     :{R} banner  whoami  info  version  langs\n"
            f"  {C}NETWORK  :{R} myip  ping  traceroute  dns  headers  scan  ports\n"
            f"  {C}RECON    :{R} whois  subdomains  robots\n"
            f"  {C}CRYPTO   :{R} hash  encode  decode  genpass\n"
            f"  {C}SYSTEM   :{R} procs  diskuse  netstat\n"
            f"  {C}FUN      :{R} matrix  morse  figlet\n"
            f"  {C}MISC     :{R} update\n\n"
            f"  GitHub: {B}https://github.com/subhobhai943/sub{R}"
        )
    )
    sp = parser.add_subparsers(dest="command")

    # ── INFO
    sp.add_parser("banner",  help="Show ASCII banner")
    sp.add_parser("whoami",  help="Author info")
    sp.add_parser("info",    help="System information")
    sp.add_parser("version", help="Show version")
    sp.add_parser("langs",   help="List all language implementations")

    # ── SYSTEM
    sp.add_parser("procs",   help="Running processes (top by CPU)")
    sp.add_parser("diskuse", help="Disk usage + largest dirs")
    sp.add_parser("netstat", help="Active network connections")

    # ── NETWORK
    sp.add_parser("myip",    help="Your local + public IP info")

    ping_p = sp.add_parser("ping", help="Ping a host")
    ping_p.add_argument("target")
    ping_p.add_argument("-c", "--count", type=int, default=4, help="Packet count (default 4)")

    tr_p = sp.add_parser("traceroute", help="Traceroute to a host")
    tr_p.add_argument("target")

    dns_p = sp.add_parser("dns", help="DNS lookup")
    dns_p.add_argument("target", help="Hostname to resolve")

    hdr_p = sp.add_parser("headers", help="Fetch HTTP headers")
    hdr_p.add_argument("url", help="URL or domain")

    scan_p = sp.add_parser("scan", help="Network scan via nmap")
    scan_p.add_argument("target")
    scan_p.add_argument("--full", action="store_true", help="Scan all 65535 ports")

    ports_p = sp.add_parser("ports", help="TCP port scan with banner grab")
    ports_p.add_argument("target")
    ports_p.add_argument("-p", "--ports", help="Custom ports: 22,80,443")

    # ── RECON
    whois_p = sp.add_parser("whois", help="WHOIS lookup")
    whois_p.add_argument("domain")

    sub_p = sp.add_parser("subdomains", help="Subdomain brute-force")
    sub_p.add_argument("domain")

    rob_p = sp.add_parser("robots", help="Fetch robots.txt")
    rob_p.add_argument("domain")

    # ── CRYPTO
    hash_p = sp.add_parser("hash", help="Hash text (MD5/SHA256/etc.)")
    hash_p.add_argument("text")

    enc_p = sp.add_parser("encode", help="Encode text")
    enc_p.add_argument("mode",
        choices=["base64","base32","hex","url","binary","rot13","morse"],
        help="Encoding mode")
    enc_p.add_argument("text")

    dec_p = sp.add_parser("decode", help="Decode text")
    dec_p.add_argument("mode",
        choices=["base64","base32","hex","url","binary","rot13"],
        help="Decoding mode")
    dec_p.add_argument("text")

    gp_p = sp.add_parser("genpass", help="Generate secure passwords")
    gp_p.add_argument("-l", "--length",  type=int, default=16, help="Length (default 16)")
    gp_p.add_argument("-n", "--count",   type=int, default=5,  help="Count (default 5)")
    gp_p.add_argument("-s", "--symbols", action="store_true",  help="Include symbols")

    # ── FUN
    sp.add_parser("matrix", help="Matrix rain animation")

    morse_p = sp.add_parser("morse", help="Text to Morse code")
    morse_p.add_argument("text")

    fig_p = sp.add_parser("figlet", help="Big ASCII text via figlet")
    fig_p.add_argument("text")

    # ── MISC
    sp.add_parser("update", help="Self-update from GitHub")

    args = parser.parse_args()

    dispatch = {
        "banner":     cmd_banner,
        "whoami":     cmd_whoami,
        "info":       cmd_info,
        "version":    cmd_version,
        "langs":      cmd_langs,
        "procs":      cmd_procs,
        "diskuse":    cmd_diskuse,
        "netstat":    cmd_netstat,
        "myip":       cmd_myip,
        "ping":       cmd_ping,
        "traceroute": cmd_traceroute,
        "dns":        cmd_dns,
        "headers":    cmd_headers,
        "scan":       cmd_scan,
        "ports":      cmd_ports,
        "whois":      cmd_whois,
        "subdomains": cmd_subdomains,
        "robots":     cmd_robots,
        "hash":       cmd_hash,
        "encode":     cmd_encode,
        "decode":     cmd_decode,
        "genpass":    cmd_genpass,
        "matrix":     cmd_matrix,
        "morse":      cmd_morse,
        "figlet":     cmd_figlet,
        "update":     cmd_update,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        print(BANNER)
        parser.print_help()

if __name__ == "__main__":
    main()
