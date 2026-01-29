#!/usr/bin/env python3
"""
DNS Server Ping Test
Tests both ICMP ping and DNS query response times for various DNS servers.
"""

import subprocess
import time
import dns.resolver
import statistics
from typing import Dict, List, Tuple
from tabulate import tabulate


# DNS servers to test
DNS_SERVERS = {
    "Cloudflare Primary": "1.1.1.1",
    "Cloudflare Secondary": "1.0.0.1",
    "Google Primary": "8.8.8.8",
    "Google Secondary": "8.8.4.4",
    "Quad9 Primary": "9.9.9.9",
    "Quad9 Secondary": "149.112.112.112",
    "OpenDNS Primary": "208.67.222.222",
    "OpenDNS Secondary": "208.67.220.220",
    "AdGuard Primary": "94.140.14.14",
    "AdGuard Secondary": "94.140.15.15",
    "Comodo Secure": "8.26.56.26",
    "Level3": "209.244.0.3",
}

# Number of pings/queries to perform
PING_COUNT = 4
TEST_DOMAIN = "google.com"


def ping_server(ip: str, count: int = PING_COUNT) -> Tuple[float, float, float, bool]:
    """
    Ping a server using ICMP and return min, avg, max response times.
    Returns (min, avg, max, success)
    """
    try:
        # Run ping command
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "2000", ip],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return (0, 0, 0, False)
        
        # Parse output to get ping times
        output = result.stdout
        times = []
        
        for line in output.split('\n'):
            if 'time=' in line:
                try:
                    time_str = line.split('time=')[1].split()[0]
                    times.append(float(time_str))
                except:
                    continue
        
        if not times:
            return (0, 0, 0, False)
        
        return (min(times), statistics.mean(times), max(times), True)
    
    except Exception as e:
        return (0, 0, 0, False)


def query_dns(ip: str, domain: str = TEST_DOMAIN, count: int = PING_COUNT) -> Tuple[float, float, float, bool]:
    """
    Query a DNS server and return min, avg, max response times.
    Returns (min, avg, max, success)
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        resolver.timeout = 2
        resolver.lifetime = 2
        
        times = []
        
        for _ in range(count):
            try:
                start = time.time()
                resolver.resolve(domain, 'A')
                end = time.time()
                times.append((end - start) * 1000)  # Convert to ms
            except:
                continue
        
        if not times:
            return (0, 0, 0, False)
        
        return (min(times), statistics.mean(times), max(times), True)
    
    except Exception as e:
        return (0, 0, 0, False)


def test_all_servers() -> List[Dict]:
    """Test all DNS servers and return results."""
    results = []
    
    print(f"Testing {len(DNS_SERVERS)} DNS servers...")
    print(f"ICMP Pings: {PING_COUNT}, DNS Queries: {PING_COUNT} ({TEST_DOMAIN})\n")
    
    for i, (name, ip) in enumerate(DNS_SERVERS.items(), 1):
        print(f"[{i}/{len(DNS_SERVERS)}] Testing {name} ({ip})...", end=" ", flush=True)
        
        # ICMP Ping test
        ping_min, ping_avg, ping_max, ping_success = ping_server(ip)
        
        # DNS Query test
        dns_min, dns_avg, dns_max, dns_success = query_dns(ip)
        
        results.append({
            "name": name,
            "ip": ip,
            "ping_min": ping_min if ping_success else None,
            "ping_avg": ping_avg if ping_success else None,
            "ping_max": ping_max if ping_success else None,
            "ping_success": ping_success,
            "dns_min": dns_min if dns_success else None,
            "dns_avg": dns_avg if dns_success else None,
            "dns_max": dns_max if dns_success else None,
            "dns_success": dns_success,
        })
        
        print("✓" if (ping_success or dns_success) else "✗")
    
    return results


def format_time(ms: float, success: bool) -> str:
    """Format time value for display."""
    if not success or ms is None:
        return "FAILED"
    return f"{ms:.2f} ms"


def display_results(results: List[Dict]):
    """Display results in a formatted table."""
    print("\n" + "=" * 100)
    print("DNS SERVER PING TEST RESULTS")
    print("=" * 100 + "\n")
    
    # Prepare table data
    table_data = []
    
    for r in results:
        table_data.append([
            r["name"],
            r["ip"],
            format_time(r["ping_min"], r["ping_success"]),
            format_time(r["ping_avg"], r["ping_success"]),
            format_time(r["ping_max"], r["ping_success"]),
            format_time(r["dns_min"], r["dns_success"]),
            format_time(r["dns_avg"], r["dns_success"]),
            format_time(r["dns_max"], r["dns_success"]),
        ])
    
    headers = [
        "DNS Provider",
        "IP Address",
        "ICMP Min",
        "ICMP Avg",
        "ICMP Max",
        "DNS Min",
        "DNS Avg",
        "DNS Max"
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100 + "\n")
    
    successful_ping = [r for r in results if r["ping_success"]]
    successful_dns = [r for r in results if r["dns_success"]]
    
    if successful_ping:
        best_ping = min(successful_ping, key=lambda x: x["ping_avg"])
        print(f"🏆 Fastest ICMP Ping: {best_ping['name']} ({best_ping['ip']}) - {best_ping['ping_avg']:.2f} ms")
    
    if successful_dns:
        best_dns = min(successful_dns, key=lambda x: x["dns_avg"])
        print(f"🏆 Fastest DNS Query: {best_dns['name']} ({best_dns['ip']}) - {best_dns['dns_avg']:.2f} ms")
    
    print(f"\n✓ Successful ICMP Pings: {len(successful_ping)}/{len(results)}")
    print(f"✓ Successful DNS Queries: {len(successful_dns)}/{len(results)}")


def main():
    """Main function."""
    try:
        results = test_all_servers()
        display_results(results)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
