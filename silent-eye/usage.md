# Silent-Eye: Advanced Reconnaissance Engine

**License:** Restricted Educational License
**Author:** r4ttles | **Project:** offensive-engine

Silent-Eye is a high-performance, asynchronous network scanner designed for rapid enumeration and service fingerprinting. Built on Python's asyncio framework, it leverages non-blocking I/O to scan hundreds of ports across multiple targets simultaneously, far outperforming traditional sequential scanners.

Key Features:
Asynchronous Concurrency: Scans thousands of ports per second without thread overhead.
Banner Grabbing: Automatically attempts to retrieve service versions (HTTP, SSH, FTP, etc.).
Subnet Support: Accepts port ranges (e.g., 1-1000) or specific lists.
JSON Export: Automatically generates a structured JSON report for SIEM integration or further analysis.
Cross-Platform: Runs natively on Linux, macOS, and Windows via Python.

Requirements:
Python 3.8+ (Standard library only; no external pip packages required). Administrator/root privileges may be required for raw socket operations on some OS configurations.

Usage:

Linux/macOS:
python3 silent_eye.py -t 192.168.1.1 -p 22,80,443
python3 silent_eye.py -t 192.168.1.1 -p 1-1000

Windows:
Ensure Python is installed and added to PATH, then run:
python silent_eye.py -t <IP> -p <PORTS>
Or use run_silent.bat for interactive prompts.

Example Output:
[+] Initiating Silent-Eye Scan on 192.168.1.1
[+] Scanning 1000 ports...
[+] Scan Completed in 4.21 seconds.
[+] Found 3 OPEN ports.
   [PORT 22] OPEN | Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu
   [PORT 80] OPEN | Banner: Apache/2.4.41 (Ubuntu)
   [PORT 443] OPEN | Banner: None

Future Roadmap:
UDP scanning support.
Nmap XML parsing integration.
TLS handshake verification for HTTPS services.

Legal Warning:
AUTHORIZED USE ONLY. Scanning networks without explicit permission is illegal and unethical. This tool is provided strictly for educational research, authorized penetration testing, and defensive security auditing. The author assumes no liability for misuse.
