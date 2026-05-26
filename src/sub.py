#!/usr/bin/env python3
# =============================================================
#  SUB - Multi-language Linux CLI tool by Subhobhai (subhobhai943)
#  GitHub  : https://github.com/subhobhai943
#  Website : https://sub-portofolio.netlify.app
#  Stack   : Python (dispatcher) + C (scanner) + Rust (recon) + ASM (sysinfo)
# =============================================================

import argparse
import os
import sys
import subprocess
import socket
import platform
import datetime
import shutil

# ─── ANSI Colors
R     = "\033[91m"
G     = "\033[92m"
Y     = "\033[93m"
B     = "\033[94m"
M     = "\033[95m"
C     = "\033[96m"
W     = "\033[97m"
BOLD  = "\033[1m"
RESET = "\033[0m"

VERSION = "2.0.0"

# ─── Binary paths (installed by Makefile into /usr/local/bin)
BIN_SCAN    = shutil.which("sub-scan")    or "/usr/local/bin/sub-scan"
BIN_RECON   = shutil.which("sub-recon")   or "/usr/local/bin/sub-recon"
BIN_SYSINFO = shutil.which("sub-sysinfo") or "/usr/local/bin/sub-sysinfo"

BANNER = f"""
{C}{BOLD}
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
{RESET}{Y}  v{VERSION} — Python · C · Rust · Assembly
  {W}By Subhobhai (subhobhai943){RESET}
  {C}https://github.com/subhobhai943{RESET}
"""

# ─── Helpers
def run_binary(path, *args):
    """Run a compiled binary, falling back to a friendly error."""
    if not os.path.isfile(path):
        print(f"\n{R}[!] Binary not found: {path}{RESET}")
        print(f"{Y}[*] Build it first: cd /path/to/sub && make build{RESET}\n")
        return
    try:
        subprocess.run([path, *args])
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{RESET}")

# ─── Commands
def cmd_whoami():
    print(f"""
{C}{BOLD}╔══════════════════════════════════════════╗
║           ABOUT THE DEVELOPER           ║
╚══════════════════════════════════════════╝{RESET}
  {Y}Name     {W}: {G}Subhobhai (Subhobhai Sarkar){RESET}
  {Y}Handle   {W}: {G}@subhobhai943{RESET}
  {Y}Location {W}: {G}Durgapur, West Bengal, India{RESET}
  {Y}Role     {W}: {G}Developer · Systems Programmer · OS Builder{RESET}
  {Y}GitHub   {W}: {C}https://github.com/subhobhai943{RESET}
  {Y}Website  {W}: {C}https://sub-portofolio.netlify.app{RESET}
  {Y}Stack    {W}: {G}C, C++, Rust, Python, Assembly, Java, Kotlin, PHP{RESET}
  {Y}Projects {W}: {G}AIOS (custom OS), SUB Lang, Discord Bots, Game Engines{RESET}
  {Y}Interests{W}: {G}OS Dev, Compilers, Hacking, AI/ML, 3D Graphics{RESET}
""")

def cmd_sysinfo_asm():
    """System info via raw Assembly binary."""
    run_binary(BIN_SYSINFO)

def cmd_sysinfo_py():
    """Fallback Python sysinfo if ASM binary not built yet."""
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unavailable"
    uname = platform.uname()
    uptime = ""
    try:
        with open("/proc/uptime") as f:
            secs = float(f.read().split()[0])
            uptime = str(datetime.timedelta(seconds=int(secs)))
    except Exception:
        uptime = "Unavailable"
    print(f"""
{C}{BOLD}╔══════════════════════════════════════════╗
║              SYSTEM INFORMATION          ║
╚══════════════════════════════════════════╝{RESET}
  {Y}OS       {W}: {G}{uname.system} {uname.release}{RESET}
  {Y}Hostname {W}: {G}{hostname}{RESET}
  {Y}Local IP {W}: {G}{local_ip}{RESET}
  {Y}Machine  {W}: {G}{uname.machine}{RESET}
  {Y}CPU      {W}: {G}{uname.processor or 'N/A'}{RESET}
  {Y}Python   {W}: {G}{platform.python_version()}{RESET}
  {Y}Uptime   {W}: {G}{uptime}{RESET}
""")

def cmd_sysinfo():
    if os.path.isfile(BIN_SYSINFO):
        cmd_sysinfo_asm()
    else:
        cmd_sysinfo_py()

def cmd_scan(target, start=1, end=1024):
    """Fast port scan via compiled C binary."""
    run_binary(BIN_SCAN, target, str(start), str(end))

def cmd_ports(host):
    """Quick 16-port check (Python fallback)."""
    common = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443]
    print(f"\n{C}[*]{W} Quick port scan on: {Y}{host}{RESET}\n")
    found = []
    for port in common:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                print(f"  {G}[OPEN]  {W}Port {Y}{port}{RESET}")
                found.append(port)
            s.close()
        except Exception:
            pass
    if not found:
        print(f"  {R}[!] No common ports open on {host}{RESET}")
    print()

def cmd_whois(domain):
    print(f"\n{C}[*]{W} WHOIS: {Y}{domain}{RESET}\n")
    try:
        subprocess.run(["whois", domain])
    except FileNotFoundError:
        print(f"{R}[!] Install: sudo apt install whois{RESET}")

def cmd_dns(domain):
    print(f"\n{C}[*]{W} DNS: {Y}{domain}{RESET}\n")
    try:
        ips = socket.getaddrinfo(domain, None)
        seen = set()
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                print(f"  {G}[A] {W}{ip}{RESET}")
                seen.add(ip)
    except Exception as e:
        print(f"  {R}[!] {e}{RESET}")
    print()

def cmd_ping(host):
    print(f"\n{C}[*]{W} Pinging: {Y}{host}{RESET}\n")
    try:
        subprocess.run(["ping", "-c", "4", host])
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{RESET}")

def cmd_headers(url):
    import urllib.request
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\n{C}[*]{W} Headers: {Y}{url}{RESET}\n")
    try:
        req = urllib.request.urlopen(url, timeout=5)
        for k, v in req.headers.items():
            print(f"  {Y}{k:<25}{W}: {G}{v}{RESET}")
    except Exception as e:
        print(f"  {R}[!] {e}{RESET}")
    print()

# ─── Rust-powered commands (dispatched to sub-recon)
def cmd_hashid(hash_val):
    run_binary(BIN_RECON, "hashid", hash_val)

def cmd_pwcheck(password):
    run_binary(BIN_RECON, "pwcheck", password)

def cmd_subdomain(domain):
    run_binary(BIN_RECON, "subdomain", domain)

def cmd_caesar(text, shift):
    run_binary(BIN_RECON, "caesar", text, str(shift))

def cmd_b64(text):
    run_binary(BIN_RECON, "b64", text)

def cmd_version():
    print(f"\n  {C}SUB {W}v{G}{VERSION}{RESET} — {Y}Python · C · Rust · Assembly{RESET}")
    print(f"  {W}Built by {C}Subhobhai (subhobhai943){RESET}\n")

# ─── Main
def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        prog="sub",
        description=f"{BOLD}SUB — Multi-language hacking toolkit by Subhobhai{RESET}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # ── Python commands
    sub.add_parser("whoami",   help="About the developer")
    sub.add_parser("sysinfo",  help="System info (ASM binary if built, else Python)")
    sub.add_parser("version",  help="Show version")
    sub.add_parser("banner",   help="Print ASCII banner")

    p = sub.add_parser("ports",   help="Quick common-port checker (Python)")
    p.add_argument("host")
    p = sub.add_parser("whois",   help="WHOIS lookup")
    p.add_argument("domain")
    p = sub.add_parser("dns",     help="DNS resolution")
    p.add_argument("domain")
    p = sub.add_parser("ping",    help="Ping a host")
    p.add_argument("host")
    p = sub.add_parser("headers", help="HTTP response headers")
    p.add_argument("url")

    # ── C-powered commands
    p = sub.add_parser("scan",    help="[C] Fast TCP port scanner with banner grab")
    p.add_argument("target")
    p.add_argument("--start", type=int, default=1,    help="Start port (default: 1)")
    p.add_argument("--end",   type=int, default=1024, help="End port (default: 1024)")

    # ── Rust-powered commands
    p = sub.add_parser("hashid",    help="[Rust] Identify hash type")
    p.add_argument("hash")
    p = sub.add_parser("pwcheck",   help="[Rust] Password strength checker")
    p.add_argument("password")
    p = sub.add_parser("subdomain", help="[Rust] Subdomain enumeration")
    p.add_argument("domain")
    p = sub.add_parser("caesar",    help="[Rust] Caesar cipher")
    p.add_argument("text")
    p.add_argument("shift", type=int)
    p = sub.add_parser("b64",       help="[Rust] Base64 encode")
    p.add_argument("text")

    # ── Assembly-powered
    sub.add_parser("rawsys", help="[ASM] Raw system info via Assembly syscalls")

    args = parser.parse_args()

    dispatch = {
        "whoami":    cmd_whoami,
        "sysinfo":   cmd_sysinfo,
        "version":   cmd_version,
        "banner":    lambda: print(BANNER),
        "ports":     lambda: cmd_ports(args.host),
        "whois":     lambda: cmd_whois(args.domain),
        "dns":       lambda: cmd_dns(args.domain),
        "ping":      lambda: cmd_ping(args.host),
        "headers":   lambda: cmd_headers(args.url),
        "scan":      lambda: cmd_scan(args.target, args.start, args.end),
        "hashid":    lambda: cmd_hashid(args.hash),
        "pwcheck":   lambda: cmd_pwcheck(args.password),
        "subdomain": lambda: cmd_subdomain(args.domain),
        "caesar":    lambda: cmd_caesar(args.text, args.shift),
        "b64":       lambda: cmd_b64(args.text),
        "rawsys":    cmd_sysinfo_asm,
    }

    if args.command in dispatch:
        dispatch[args.command]()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
