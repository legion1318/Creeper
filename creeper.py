#!/usr/bin/env python3

import socket
import threading
import argparse

results = []  # Store results

def get_service_name(port):
    """Try to resolve port → service name from system database."""
    try:
        return socket.getservbyport(port, "tcp")
    except:
        return "?"

def scan_port(target, port, timeout=1):
    """Attempt to connect to a port (no banner grabbing)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))  # 0 = open
        if result == 0:
            service = get_service_name(port)
            results.append((port, "open", service))
        sock.close()
    except:
        pass

def scan_range(target, ports, threads=100):
    """Scan a list of ports using threading."""
    try:
        resolved_ip = socket.gethostbyname(target)
        print(f"[*] Scanning {target} ({resolved_ip}) ...\n")
    except socket.gaierror:
        print(f"[!] Could not resolve {target}")
        return

    thread_list = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(target, port))
        thread_list.append(t)
        t.start()

        if len(thread_list) >= threads:
            for thread in thread_list:
                thread.join()
            thread_list = []

    for thread in thread_list:
        thread.join()

    if results:
        print("PORT      STATE   SERVICE")
        for port, state, service in sorted(results, key=lambda x: x[0]):
            print(f"{str(port)+'/tcp':<9} {state:<7} {service}")
    else:
        print("[!] No open ports found.")

def parse_ports(port_arg):
    """Parse -p argument into a list of ports."""
    ports = set()
    for part in port_arg.split(","):
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(list(ports))

def main():
    parser = argparse.ArgumentParser(description="Creeper Custom Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g. 80,443 or 20-1000)", default="1-6335")
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    scan_range(args.target, ports)

if __name__ == "__main__":
    main()
