#!/usr/bin/env python3

import nmap
import requests
import os
import subprocess

def scan_ports(target):
    """Scan for open ports using nmap."""
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='-p 1-1024')
    print(f"Scanning {target} for open ports...")
    for host in scanner.all_hosts():
        print(f"Host: {host}")
        for proto in scanner[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = scanner[host][proto].keys()
            for port in ports:
                print(f"Port: {port}\tState: {scanner[host][proto][port]['state']}")

def check_vulnerabilities(target):
    """Check for common vulnerabilities."""
    print(f"Checking vulnerabilities on {target}...")
    # Example: Check for outdated software versions
    try:
        response = requests.get(f"http://{target}")
        if "Apache" in response.headers.get("Server", ""):
            print("Apache server detected. Check for updates.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    target = input("Enter the target IP or hostname: ")
    scan_ports(target)
    check_vulnerabilities(target)

if __name__ == "__main__":
    main()
