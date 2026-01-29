# DNS Server Ping Test

A Python script to test and compare the performance of various DNS servers including Cloudflare, Google, Quad9, OpenDNS, AdGuard, and more.

## Features

- **ICMP Ping Test**: Measures basic network connectivity and latency
- **DNS Query Test**: Measures actual DNS resolution performance
- **Multiple Providers**: Tests 12 popular DNS servers
- **Detailed Statistics**: Shows min, average, and max response times
- **Beautiful Table Output**: Formatted results with summary statistics

## DNS Servers Tested

- **Cloudflare**: 1.1.1.1, 1.0.0.1
- **Google Public DNS**: 8.8.8.8, 8.8.4.4
- **Quad9**: 9.9.9.9, 149.112.112.112
- **OpenDNS**: 208.67.222.222, 208.67.220.220
- **AdGuard DNS**: 94.140.14.14, 94.140.15.15
- **Comodo Secure DNS**: 8.26.56.26
- **Level3**: 209.244.0.3

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python dns_ping.py
```

Or make it executable:
```bash
chmod +x dns_ping.py
./dns_ping.py
```

## Sample Output

The script will display a comprehensive table showing:
- DNS provider name
- IP address
- ICMP ping times (min/avg/max)
- DNS query times (min/avg/max)

Plus a summary showing the fastest servers for both ICMP and DNS queries.

## Requirements

- Python 3.6+
- dnspython
- tabulate

## Notes

- The script performs 4 pings and 4 DNS queries by default
- DNS queries test resolution of `google.com`
- Failed tests are marked as "FAILED" in the results
- Requires network connectivity to test servers
