#!/usr/bin/env python3
"""
sub - The SUB Hacking & Info Tool
Author: Subhobhai (subhobhai943)
GitHub: https://github.com/subhobhai943
"""

import argparse
import os
import subprocess
import sys
import platform
import socket
import datetime

BANNER = r"""
  ███████╗██╗   ██╗██████╗ 
  ██╔════╝██║   ██║██╔══██╗
  ███████╗██║   ██║██████╔╝
  ╚════██║██║   ██║██╔══██╗
  ███████║╚██████╔╝██████╔╝
  ╚══════╝ ╚═════╝ ╚═════╝ 
  by Subhobhai | github.com/subhobhai943
"""

def cmd_banner(args):
    print(BANNER)

def cmd_whoami(args):
    info = [
        ("Name",      "Subhobhai Sarkar"),
        ("Alias",     "sub"),
        ("GitHub",    "https://github.com/subhobhai943"),
        ("Portfolio", "https://sub-portofolio.netlify.app"),
        ("Location",  "Durgapur, West Bengal, India"),
        ("Bio",       "PCMB student | Web, AI, C++/C# game dev | Open-source hacker"),
        ("Projects",  "AIOS, SUB lang, Discord bots, 3D web games"),
        ("Languages", "Python, C, C++, Rust, Kotlin, Java, JS, Assembly"),
    ]
    print(BANNER)
    for k, v in info:
        print(f"  \033[1;32m{k:<12}\033[0m: {v}")
    print()

def cmd_info(args):
    print("\n\033[1;36m[*] System Information\033[0m")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        hostname, local_ip = "unknown", "unknown"
    print(f"  OS       : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Hostname : {hostname}")
    print(f"  Local IP : {local_ip}")
    print(f"  Python   : {platform.python_version()}")
    print(f"  Uptime   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def cmd_scan(args):
    host = args.target
    print(f"\n\033[1;33m[*] Scanning {host} ...\033[0m")
    if not _tool_exists("nmap"):
        print("  [!] nmap not found. Install it: sudo apt install nmap")
        sys.exit(1)
    subprocess.run(["nmap", "-sV", "-T4", host])

def cmd_ports(args):
    host = args.target
    common_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5900,8080,8443]
    print(f"\n\033[1;33m[*] Checking common ports on {host} ...\033[0m")
    for port in common_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            s.close()
            status = "\033[1;32mOPEN\033[0m" if result == 0 else "\033[1;31mCLOSED\033[0m"
            print(f"  Port {port:<6}: {status}")
        except Exception:
            print(f"  Port {port:<6}: ERROR")
    print()

def cmd_whois(args):
    domain = args.domain
    print(f"\n\033[1;36m[*] WHOIS: {domain}\033[0m")
    if _tool_exists("whois"):
        subprocess.run(["whois", domain])
    else:
        print("  [!] whois not found. Install it: sudo apt install whois")
        sys.exit(1)

def cmd_update(args):
    print("\n\033[1;36m[*] Updating sub from GitHub...\033[0m")
    subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "pull"])
    print("  [+] Done.")

def _tool_exists(name):
    return subprocess.call(["which", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def main():
    parser = argparse.ArgumentParser(
        prog="sub",
        description="sub — Hacking & Info Tool by Subhobhai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="GitHub: https://github.com/subhobhai943"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("banner", help="Show the SUB ASCII banner")
    sub.add_parser("whoami", help="Info about the author (Subhobhai)")
    sub.add_parser("info",   help="System information")
    sub.add_parser("update", help="Self-update from GitHub")

    scan_p = sub.add_parser("scan", help="Network scan using nmap")
    scan_p.add_argument("target", help="Target IP or hostname")

    ports_p = sub.add_parser("ports", help="Check common open ports")
    ports_p.add_argument("target", help="Target IP or hostname")

    whois_p = sub.add_parser("whois", help="WHOIS lookup")
    whois_p.add_argument("domain", help="Domain name to look up")

    args = parser.parse_args()

    commands = {
        "banner": cmd_banner,
        "whoami": cmd_whoami,
        "info":   cmd_info,
        "scan":   cmd_scan,
        "ports":  cmd_ports,
        "whois":  cmd_whois,
        "update": cmd_update,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        print(BANNER)
        parser.print_help()

if __name__ == "__main__":
    main()
