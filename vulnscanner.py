#!/usr/bin/env python3
import subprocess
import sys
import os
import importlib.util
from colorama import Fore, Style, init
import pyfiglet

# Auto-install missing python modules
def install_module(module):
    if importlib.util.find_spec(module) is None:
        print(f"[+] Installing Python module: {module}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_module("colorama")
install_module("pyfiglet")

from colorama import Fore, Style, init
import pyfiglet
init(autoreset=True)

# Auto-install nmap system package if missing
def install_package(pkg):
    try:
        subprocess.run(["which", pkg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"[+] Installing system package: {pkg}")
        subprocess.run(["sudo", "apt", "update", "-y"])
        subprocess.run(["sudo", "apt", "install", "-y", pkg])

install_package("nmap")

def banner():
    ascii_banner = pyfiglet.figlet_format("VulnScanner")
    print(Fore.CYAN + ascii_banner)
    print(Fore.YELLOW + "Vulnerability Scanner ")
    print(Fore.YELLOW + "By Antic-Pankaj\n")

def show_help():
    print(Fore.GREEN + "Usage:")
    print(Fore.WHITE + "  vulnscanner <target>")
    print(Fore.WHITE + "  vulnscanner <target1,target2,...>")
    print(Fore.WHITE + "  vulnscanner --help\n")
    print(Fore.GREEN + "Examples:")
    print(Fore.WHITE + "  vulnscanner 192.168.1.1")
    print(Fore.WHITE + "  vulnscanner scanme.nmap.org")
    print(Fore.WHITE + "  vulnscanner 192.168.1.1,192.168.1.2\n")
    print(Fore.YELLOW + "Note: Requires root privileges for full scans.")

def colorize_line(line):
    l = line.lower()
    if "critical" in l or "high" in l:
        print(Fore.RED + line)
    elif "medium" in l:
        print(Fore.YELLOW + line)
    elif "low" in l:
        print(Fore.GREEN + line)
    else:
        print(line)

def scan_target(target):
    print(Fore.CYAN + f"\n[+] Scanning target: {target}\n")
    try:
        # Run nmap with version detection and vuln scripts
        proc = subprocess.Popen(
            ["nmap", "-sV", "--script", "vuln", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in proc.stdout:
            colorize_line(line.rstrip())
        proc.wait()
        if proc.returncode != 0:
            print(Fore.RED + f"[!] Nmap exited with code {proc.returncode}")
    except FileNotFoundError:
        print(Fore.RED + "[!] Nmap is not installed or not found in PATH.")

def auto_install_or_update():
    current_file = os.path.abspath(__file__)
    target_path = "/usr/local/bin/vulnscanner"

    try:
        if not os.path.exists(target_path):
            print(Fore.YELLOW + "[*] Installing vulnscanner to /usr/local/bin/ ...")
        else:
            print(Fore.YELLOW + "[*] Updating existing vulnscanner ...")

        subprocess.run(["chmod", "+x", current_file])
        subprocess.run(["sudo", "cp", current_file, target_path])
        subprocess.run(["sudo", "chmod", "+x", target_path])

        print(Fore.GREEN + "[+] VulnScanner installed/updated successfully! You can now run 'vulnscanner' from anywhere.\n")
    except Exception as e:
        print(Fore.RED + f"[!] Installation/Update failed: {e}")

def main():
    auto_install_or_update()
    banner()

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        show_help()
        sys.exit(0)

    targets = sys.argv[1].split(",")
    for target in targets:
        scan_target(target.strip())

if __name__ == "__main__":
    main()