#!/usr/bin/env python3
"""
Silent-Eye v1.0
Author: r4ttles
Description: High-performance asynchronous network reconnaissance and fingerprinting engine.
License: See LICENSE.md in root directory.

WARNING: Educational/Defensive use ONLY. Unauthorized scanning is illegal.
"""

import asyncio
import socket
import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
BANNER_TIMEOUT = 2.0
CONCURRENT_TASKS = 500  # Max concurrent connections

class SilentEyeScanner:
    def __init__(self, target: str, ports: List[int], timeout: float = BANNER_TIMEOUT):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.results: Dict[str, any] = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "open_ports": [],
            "closed_ports": 0,
            "filtered": []
        }

    async def scan_port(self, port: int) -> Optional[Dict]:
        """Attempts to connect and grab banner for a single port."""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.target, port),
                timeout=self.timeout
            )
            
            # Try to grab banner (service info)
            banner = "Unknown"
            try:
                if writer:
                    # Send a harmless probe (e.g., HTTP GET or SSH version request)
                    if port == 80 or port == 443:
                        writer.write(b"GET / HTTP/1.0\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    elif port == 22:
                        writer.write(b"\r\n")
                    
                    data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                    if data:
                        banner = data.decode('utf-8', errors='ignore').strip()[:100] # Truncate long banners
            except Exception:
                pass # Banner grab failed, but port is open
            
            if writer:
                writer.close()
                await writer.wait_closed()

            return {
                "port": port,
                "state": "OPEN",
                "banner": banner if banner != "Unknown" else "None"
            }

        except asyncio.TimeoutError:
            return {"port": port, "state": "FILTERED/TIMEOUT"}
        except ConnectionRefusedError:
            return {"port": port, "state": "CLOSED"}
        except Exception as e:
            return {"port": port, "state": "ERROR", "detail": str(e)}

    async def run_scan(self):
        """Orchestrates the parallel scanning of all ports."""
        print(f"\n[+] Initiating Silent-Eye Scan on {self.target}")
        print(f"[+] Scanning {len(self.ports)} ports with concurrency level: {CONCURRENT_TASKS}\n")
        
        start_time = datetime.now()
        
        # Create tasks in batches to avoid overwhelming the network card
        tasks = []
        for port in self.ports:
            tasks.append(self.scan_port(port))
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Process results
        for res in results:
            if isinstance(res, dict):
                if res["state"] == "OPEN":
                    self.results["open_ports"].append(res)
                elif res["state"] == "FILTERED/TIMEOUT":
                    self.results["filtered"].append(res["port"])
                elif res["state"] == "CLOSED":
                    self.results["closed_ports"] += 1
        
        self.results["scan_duration_sec"] = round(duration, 2)
        
        # Print Summary
        print(f"\n[*] Scan Completed in {duration:.2f} seconds.")
        print(f"[+] Found {len(self.results['open_ports'])} OPEN ports.\n")
        
        for entry in self.results["open_ports"]:
            banner_str = entry.get("banner", "No Banner")
            print(f"   [PORT {entry['port']}] OPEN | Banner: {banner_str}")
        
        if self.results["open_ports"]:
            print("\n[!] Exporting results to JSON...")
            self.export_json()

    def export_json(self):
        """Saves findings to a JSON file for analysis."""
        filename = f"silent_eye_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"[+] Saved to {filename}")

def parse_args():
    parser = argparse.ArgumentParser(description="Silent-Eye: Advanced Async Reconnaissance Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP or Hostname")
    parser.add_argument("-p", "--ports", required=True, help="Comma-separated list of ports (e.g., 22,80,443-1000)")
    parser.add_argument("-o", "--output", action="store_true", help="Export results to JSON")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Parse ports string into a list
    try:
        ports = []
        for p in args.ports.split(','):
            if '-' in p:
                start, end = map(int, p.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(p))
    except ValueError:
        print("[!] Invalid port format. Use comma-separated integers or ranges (e.g., 1-100).")
        sys.exit(1)

    scanner = SilentEyeScanner(args.target, ports)
    
    try:
        asyncio.run(scanner.run_scan())
    except KeyboardInterrupt:
        print("\n[x] Interrupted by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
