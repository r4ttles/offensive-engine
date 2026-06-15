# Silent-Eye: Advanced Reconnaissance Engine

## Overview
Silent-Eye is a high-performance, asynchronous network scanner designed for rapid enumeration and service fingerprinting. Built on Python's asyncio framework, it leverages non-blocking I/O to scan hundreds of ports across multiple targets simultaneously, far outperforming traditional sequential scanners.

## Key Features
-   Asynchronous Concurrency: Scans thousands of ports per second without thread overhead.
-   Banner Grabbing: Automatically attempts to retrieve service versions (HTTP, SSH, FTP, etc.).
-   Subnet Support: Accepts port ranges (e.g., 1-1000) or specific lists.
-   JSON Export: Automatically generates a structured JSON report for SIEM integration or further analysis.
-   Cross-Platform: Runs natively on Linux, macOS, and Windows (via Python).

## Requirements
-   Python 3.8+ (Standard library only; no external pip packages required).
-   Administrator/Root privileges may be required for raw socket operations on some OS configurations (though this tool uses standard sockets).

## Usage

### Linux / macOS
Run via command line:
  python3 silent_eye.py -t 192.168.1.1 -p 22,80,443
  python3 silent_eye.py -t 192.168.1.1 -p 1-1000

### Windows
1.  Ensure Python is installed and added to your PATH.
2.  Double-click run_silent.bat and follow the interactive prompts.
3.  Or run via command line:
    python silent_eye.py -t <IP> -p <PORTS>

## Example Output
  [+] Initiating Silent-Eye Scan on 192.168.1.1
  [+] Scanning 1000 ports...
  [+] Scan Completed in 4.21 seconds.
  [+] Found 3 OPEN ports.
     [PORT 22] OPEN | Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu
     [PORT 80] OPEN | Banner: Apache/2.4.41 (Ubuntu)
     [PORT 443] OPEN | Banner: None

## Ethical Disclaimer
AUTHORIZED USE ONLY.
Silent-Eye is a powerful reconnaissance tool. Scanning networks without explicit permission is illegal and unethical. This tool is provided strictly for educational research, authorized penetration testing, and defensive security auditing. The author (r4ttles) assumes no liability for misuse.

## Future Roadmap
-   Add UDP scanning support.
-   Integrate with Nmap XML parsing.
-   Add TLS handshake verification for HTTPS services.
