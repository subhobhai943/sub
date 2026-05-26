#!/usr/bin/env python3
# =============================================================
#  SUB - A powerful Linux CLI tool by Subhobhai (Subhobhai943)
#  GitHub  : https://github.com/subhobhai943
#  Website : https://sub-portofolio.netlify.app
# =============================================================

import argparse
import os
import sys
import subprocess
import socket
import platform
import datetime

# ─── ANSI Colors ─────────────────────────────────────────────
R  = "\033[91m"   # Red
G  = "\033[92m"   # Green
Y  = "\033[93m"   # Yellow
B  = "\033[94m"   # Blue
M  = "\033[95m"   # Magenta
C  = "\033[96m"   # Cyan
W  = "\033[97m"   # White
BOLD = "\033[1m"
RESET = "\033[0m"

# ─── Banner ──────────────────────────────────────────────────
BANNER = f"""
{C}{BOLD}
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
{RESET}{Y}  By Subhobhai (subhobhai943) — v1.0.0
  {W}https://github.com/subhobhai943{RESET}
"""

# ─── whoami ──────────────────────────────────────────────────
def cmd_whoami():
    print(f"""
{C}{BOLD}╔══════════════════════════════════════════╗
║           ABOUT THE DEVELOPER           ║
╚══════════════════════════════════════════╝{RESET}

  {Y}Name     {W}: {G}Subhobhai (Subhobhai Sarkar){RESET}
  {Y}Handle   {W}: {G}@subhobhai943{RESET}
  {Y}Location {W}: {G}Durgapur, West Bengal, India{RESET}
  {Y}Role     {W}: {G}Developer | Systems Programmer | OS Builder{RESET}
  {Y}GitHub   {W}: {C}https://github.com/subhobhai943{RESET}
  {Y}Website  {W}: {C}https://sub-portofolio.netlify.app{RESET}
  {Y}Skills   {W}: {G}C, C++, Python, Rust, Assembly, Java, Kotlin, PHP{RESET}
  {Y}Projects {W}: {G}AIOS (custom OS), SUB Lang, Discord Bots, Game Engines{RESET}
  {Y}Interests{W}: {G}OS Dev, Compilers, Hacking, AI/ML, 3D Graphics{RESET}
""")

# ─── banner ──────────────────────────────────────────────────
def cmd_banner():
    print(BANNER)
    print(f"  {G}Type {W}'sub --help'{G} to see all available commands.{RESET}\n")

# ─── sysinfo ─────────────────────────────────────────────────
def cmd_sysinfo():
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
  {Y}Distro   {W}: {G}{platform.platform()}{RESET}
  {Y}Hostname {W}: {G}{hostname}{RESET}
  {Y}Local IP {W}: {G}{local_ip}{RESET}
  {Y}Machine  {W}: {G}{uname.machine}{RESET}
  {Y}CPU      {W}: {G}{uname.processor or 'N/A'}{RESET}
  {Y}Python   {W}: {G}{platform.python_version()}{RESET}
  {Y}Uptime   {W}: {G}{uptime}{RESET}
""")

# ─── scan ────────────────────────────────────────────────────
def cmd_scan(target):
    print(f"\n{C}[*]{W} Scanning target: {Y}{target}{RESET}\n")
    try:
        subprocess.run(["nmap", "-sV", "--open", target])
    except FileNotFoundError:
        print(f"{R}[!] nmap is not installed. Run: sudo apt install nmap{RESET}")
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Scan interrupted.{RESET}")

# ─── ports ───────────────────────────────────────────────────
def cmd_ports(host):
    common_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443]
    print(f"\n{C}[*]{W} Quick port scan on: {Y}{host}{RESET}\n")
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"  {G}[OPEN]  {W}Port {Y}{port}{RESET}")
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    if not open_ports:
        print(f"  {R}[!] No common ports found open on {host}{RESET}")
    print()

# ─── whois ───────────────────────────────────────────────────
def cmd_whois(domain):
    print(f"\n{C}[*]{W} WHOIS lookup for: {Y}{domain}{RESET}\n")
    try:
        subprocess.run(["whois", domain])
    except FileNotFoundError:
        print(f"{R}[!] whois is not installed. Run: sudo apt install whois{RESET}")

# ─── dns ─────────────────────────────────────────────────────
def cmd_dns(domain):
    print(f"\n{C}[*]{W} DNS lookup for: {Y}{domain}{RESET}\n")
    try:
        ips = socket.getaddrinfo(domain, None)
        seen = set()
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                print(f"  {G}[A] {W}{ip}{RESET}")
                seen.add(ip)
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RESET}")
    print()

# ─── ping ────────────────────────────────────────────────────
def cmd_ping(host):
    print(f"\n{C}[*]{W} Pinging: {Y}{host}{RESET}\n")
    try:
        subprocess.run(["ping", "-c", "4", host])
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{RESET}")

# ─── headers ─────────────────────────────────────────────────
def cmd_headers(url):
    import urllib.request
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\n{C}[*]{W} HTTP Headers for: {Y}{url}{RESET}\n")
    try:
        req = urllib.request.urlopen(url, timeout=5)
        for k, v in req.headers.items():
            print(f"  {Y}{k:<25}{W}: {G}{v}{RESET}")
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RESET}")
    print()

# ─── version ─────────────────────────────────────────────────
def cmd_version():
    print(f"\n  {C}SUB {W}v{G}1.0.0{RESET} — Built by {Y}Subhobhai943{RESET}\n")

# ─── Main Parser ─────────────────────────────────────────────
def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        prog="sub",
        description=f"{BOLD}SUB — Hacking toolkit & developer info tool by Subhobhai{RESET}",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # whoami
    subparsers.add_parser("whoami",   help="Show info about the developer (Subhobhai)")
    # banner
    subparsers.add_parser("banner",   help="Print the SUB ASCII banner")
    # sysinfo
    subparsers.add_parser("sysinfo",  help="Show current system information")
    # version
    subparsers.add_parser("version",  help="Show SUB version")

    # scan
    p_scan = subparsers.add_parser("scan",    help="Run nmap scan on a target")
    p_scan.add_argument("target", help="IP or hostname to scan")

    # ports
    p_ports = subparsers.add_parser("ports",  help="Quick check of common open ports")
    p_ports.add_argument("host",   help="IP or hostname")

    # whois
    p_whois = subparsers.add_parser("whois",  help="WHOIS lookup for a domain")
    p_whois.add_argument("domain", help="Domain name")

    # dns
    p_dns = subparsers.add_parser("dns",     help="DNS resolution for a domain")
    p_dns.add_argument("domain",   help="Domain name")

    # ping
    p_ping = subparsers.add_parser("ping",   help="Ping a host")
    p_ping.add_argument("host",    help="IP or hostname")

    # headers
    p_hdr = subparsers.add_parser("headers", help="Fetch HTTP headers from a URL")
    p_hdr.add_argument("url",      help="Target URL")

    args = parser.parse_args()

    if   args.command == "whoami":  cmd_whoami()
    elif args.command == "banner":  cmd_banner()
    elif args.command == "sysinfo": cmd_sysinfo()
    elif args.command == "version": cmd_version()
    elif args.command == "scan":    cmd_scan(args.target)
    elif args.command == "ports":   cmd_ports(args.host)
    elif args.command == "whois":   cmd_whois(args.domain)
    elif args.command == "dns":     cmd_dns(args.domain)
    elif args.command == "ping":    cmd_ping(args.host)
    elif args.command == "headers": cmd_headers(args.url)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
