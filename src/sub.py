#!/usr/bin/env python3
# =============================================================
#  SUB - Multi-language Linux CLI tool by Subhobhai (subhobhai943)
#  GitHub  : https://github.com/subhobhai943
#  Stack   : Python + C + Rust + Assembly + Kotlin + Java
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

VERSION = "3.0.0"

# ─── Binary / JAR paths
BIN_SCAN    = shutil.which("sub-scan")    or "/usr/local/bin/sub-scan"
BIN_RECON   = shutil.which("sub-recon")   or "/usr/local/bin/sub-recon"
BIN_SYSINFO = shutil.which("sub-sysinfo") or "/usr/local/bin/sub-sysinfo"
JAR_NET     = "/usr/local/share/sub/sub-net.jar"
JAR_OSINT   = "/usr/local/share/sub/sub-osint.jar"

BANNER = f"""
{C}{BOLD}
  ███████╗██╗   ██╗██████╖
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝
{RESET}{Y}  v{VERSION} — Python · C · Rust · Assembly · Kotlin · Java
  {W}By Subhobhai (subhobhai943){RESET}
  {C}https://github.com/subhobhai943{RESET}
"""

# ─── Helpers
def run_binary(path, *args):
    if not os.path.isfile(path):
        print(f"\n{R}[!] Binary not found: {path}{RESET}")
        print(f"{Y}[*] Run: make build && sudo make install{RESET}\n")
        return
    try:
        subprocess.run([path, *args])
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{RESET}")

def run_jar(jar_path, *args):
    if not os.path.isfile(jar_path):
        print(f"\n{R}[!] JAR not found: {jar_path}{RESET}")
        print(f"{Y}[*] Run: make build && sudo make install{RESET}\n")
        return
    try:
        subprocess.run(["java", "-jar", jar_path, *args])
    except FileNotFoundError:
        print(f"{R}[!] Java not installed. Run: sudo apt install default-jre{RESET}")
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{RESET}")

# ─── Python commands
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
  {Y}Stack    {W}: {G}C, C++, Rust, Python, ASM, Kotlin, Java, PHP{RESET}
  {Y}Projects {W}: {G}AIOS (OS), SUB Lang, Discord Bots, Game Engines{RESET}
  {Y}Interests{W}: {G}OS Dev, Compilers, Hacking, AI/ML, 3D Graphics{RESET}
""")

def cmd_sysinfo_py():
    hostname = socket.gethostname()
    try: local_ip = socket.gethostbyname(hostname)
    except: local_ip = "Unavailable"
    uname = platform.uname()
    try:
        with open("/proc/uptime") as f:
            uptime = str(datetime.timedelta(seconds=int(float(f.read().split()[0]))))
    except: uptime = "Unavailable"
    print(f"\n{C}{BOLD}╔{'='*42}╗\n║{'SYSTEM INFORMATION':^42}║\n╚{'='*42}╝{RESET}")
    print(f"  {Y}OS       {W}: {G}{uname.system} {uname.release}{RESET}")
    print(f"  {Y}Hostname {W}: {G}{hostname}{RESET}")
    print(f"  {Y}Local IP {W}: {G}{local_ip}{RESET}")
    print(f"  {Y}Machine  {W}: {G}{uname.machine}{RESET}")
    print(f"  {Y}CPU      {W}: {G}{uname.processor or 'N/A'}{RESET}")
    print(f"  {Y}Python   {W}: {G}{platform.python_version()}{RESET}")
    print(f"  {Y}Uptime   {W}: {G}{uptime}{RESET}\n")

def cmd_sysinfo():
    if os.path.isfile(BIN_SYSINFO): run_binary(BIN_SYSINFO)
    else: cmd_sysinfo_py()

def cmd_scan(target, start=1, end=1024):    run_binary(BIN_SCAN, target, str(start), str(end))
def cmd_ports(host):
    common = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443]
    print(f"\n{C}[*]{W} Quick port scan: {Y}{host}{RESET}\n")
    found = []
    for port in common:
        try:
            s = socket.socket(); s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                print(f"  {G}[OPEN]  {W}Port {Y}{port}{RESET}"); found.append(port)
            s.close()
        except: pass
    if not found: print(f"  {R}[!] No common ports open{RESET}")
    print()

def cmd_whois(domain):
    print(f"\n{C}[*]{W} WHOIS: {Y}{domain}{RESET}\n")
    try: subprocess.run(["whois", domain])
    except FileNotFoundError: print(f"{R}[!] sudo apt install whois{RESET}")

def cmd_dns(domain):
    print(f"\n{C}[*]{W} DNS: {Y}{domain}{RESET}\n")
    try:
        seen = set()
        for info in socket.getaddrinfo(domain, None):
            ip = info[4][0]
            if ip not in seen: print(f"  {G}[A] {W}{ip}{RESET}"); seen.add(ip)
    except Exception as e: print(f"  {R}[!] {e}{RESET}")
    print()

def cmd_ping(host):
    try: subprocess.run(["ping", "-c", "4", host])
    except KeyboardInterrupt: print(f"\n{Y}[!] Interrupted.{RESET}")

def cmd_headers(url):
    import urllib.request
    if not url.startswith("http"): url = "http://" + url
    print(f"\n{C}[*]{W} Headers: {Y}{url}{RESET}\n")
    try:
        req = urllib.request.urlopen(url, timeout=5)
        for k, v in req.headers.items(): print(f"  {Y}{k:<25}{W}: {G}{v}{RESET}")
    except Exception as e: print(f"  {R}[!] {e}{RESET}")
    print()

# ─── Rust commands
def cmd_hashid(h):      run_binary(BIN_RECON, "hashid",    h)
def cmd_pwcheck(pw):    run_binary(BIN_RECON, "pwcheck",   pw)
def cmd_subdomain(d):   run_binary(BIN_RECON, "subdomain", d)
def cmd_caesar(t, s):   run_binary(BIN_RECON, "caesar",    t, str(s))
def cmd_b64(t):         run_binary(BIN_RECON, "b64",       t)

# ─── Kotlin (JAR) commands
def cmd_net_scan(host, start, end, threads):  run_jar(JAR_NET, "scan",       host, str(start), str(end), str(threads))
def cmd_rdns(ip):                             run_jar(JAR_NET, "rdns",       ip)
def cmd_banner_grab(host, port):             run_jar(JAR_NET, "banner",     host, str(port))
def cmd_traceroute(host):                    run_jar(JAR_NET, "traceroute",  host)
def cmd_geoip(ip):                           run_jar(JAR_NET, "geoip",       ip)
def cmd_ifaces():                            run_jar(JAR_NET, "ifaces")

# ─── Java (JAR) commands
def cmd_osint_geoip(ip):       run_jar(JAR_OSINT, "geoip",    ip)
def cmd_email_header(f):       run_jar(JAR_OSINT, "email",    f)
def cmd_username(u):           run_jar(JAR_OSINT, "username",  u)
def cmd_expand_url(url):       run_jar(JAR_OSINT, "expand",   url)
def cmd_httpstat(url):         run_jar(JAR_OSINT, "httpstat",  url)

def cmd_version():
    print(f"\n  {C}SUB {W}v{G}{VERSION}{RESET} — {Y}Python · C · Rust · Assembly · Kotlin · Java{RESET}")
    print(f"  {W}Built by {C}Subhobhai (subhobhai943){RESET}\n")

# ─── Main
def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        prog="sub",
        description=f"{BOLD}SUB — 6-language hacking toolkit by Subhobhai{RESET}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    sp = parser.add_subparsers(dest="command", metavar="<command>")

    # ─ Python
    sp.add_parser("whoami");  sp.add_parser("sysinfo")
    sp.add_parser("version"); sp.add_parser("banner")
    sp.add_parser("rawsys",  help="[ASM] Raw syscall sysinfo")
    sp.add_parser("ifaces",  help="[Kotlin] Network interfaces")

    def a(cmd, hlp, **kw):
        p = sp.add_parser(cmd, help=hlp)
        for k, v in kw.items(): p.add_argument(k if k.startswith('--') else k, **v)
        return p

    a("ports",      "[Python] Quick port checker",          host=dict())
    a("whois",      "[Python] WHOIS lookup",                domain=dict())
    a("dns",        "[Python] DNS resolution",              domain=dict())
    a("ping",       "[Python] Ping host",                   host=dict())
    a("headers",    "[Python] HTTP headers",                url=dict())

    p = sp.add_parser("scan",   help="[C] Fast TCP scan + banner")
    p.add_argument("target"); p.add_argument("--start",type=int,default=1); p.add_argument("--end",type=int,default=1024)

    a("hashid",     "[Rust] Hash identifier",               hash=dict())
    a("pwcheck",    "[Rust] Password strength",             password=dict())
    a("subdomain",  "[Rust] Subdomain enumeration",         domain=dict())
    p = sp.add_parser("caesar", help="[Rust] Caesar cipher"); p.add_argument("text"); p.add_argument("shift",type=int)
    a("b64",        "[Rust] Base64 encode",                 text=dict())

    p = sp.add_parser("netscan",   help="[Kotlin] Threaded port scan")
    p.add_argument("host"); p.add_argument("--start",type=int,default=1); p.add_argument("--end",type=int,default=1024); p.add_argument("--threads",type=int,default=100)
    a("rdns",       "[Kotlin] Reverse DNS",                 ip=dict())
    p = sp.add_parser("grab",    help="[Kotlin] TCP banner grab"); p.add_argument("host"); p.add_argument("port",type=int)
    a("traceroute", "[Kotlin] Traceroute",                  host=dict())
    a("geoip",      "[Kotlin] IP geolocation",              ip=dict())

    a("username",   "[Java] Username presence check",       username=dict())
    a("emailhdr",   "[Java] Email header analysis",         file=dict())
    a("expand",     "[Java] Expand short URL",              url=dict())
    a("httpstat",   "[Java] HTTP status + fingerprint",     url=dict())

    args = parser.parse_args()

    match args.command:
        # Python
        case "whoami":    cmd_whoami()
        case "sysinfo":   cmd_sysinfo()
        case "rawsys":    run_binary(BIN_SYSINFO)
        case "version":   cmd_version()
        case "banner":    print(BANNER)
        case "ports":     cmd_ports(args.host)
        case "whois":     cmd_whois(args.domain)
        case "dns":       cmd_dns(args.domain)
        case "ping":      cmd_ping(args.host)
        case "headers":   cmd_headers(args.url)
        # C
        case "scan":      cmd_scan(args.target, args.start, args.end)
        # Rust
        case "hashid":    cmd_hashid(args.hash)
        case "pwcheck":   cmd_pwcheck(args.password)
        case "subdomain": cmd_subdomain(args.domain)
        case "caesar":    cmd_caesar(args.text, args.shift)
        case "b64":       cmd_b64(args.text)
        # Kotlin
        case "netscan":   cmd_net_scan(args.host, args.start, args.end, args.threads)
        case "rdns":      cmd_rdns(args.ip)
        case "grab":      cmd_banner_grab(args.host, args.port)
        case "traceroute":cmd_traceroute(args.host)
        case "geoip":     cmd_geoip(args.ip)
        case "ifaces":    cmd_ifaces()
        # Java
        case "username":  cmd_username(args.username)
        case "emailhdr":  cmd_email_header(args.file)
        case "expand":    cmd_expand_url(args.url)
        case "httpstat":  cmd_httpstat(args.url)
        case _:           parser.print_help()

if __name__ == "__main__":
    main()
