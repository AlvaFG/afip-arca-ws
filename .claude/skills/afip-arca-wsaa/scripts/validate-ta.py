"""
Inspect a TA.xml: print token, sign (truncated), and time until expiration.
Usage: python validate-ta.py path/to/ta.xml
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate-ta.py <path/to/ta.xml>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    root = ET.fromstring(path.read_bytes())
    creds = root.find("credentials")
    header = root.find("header")
    if creds is None or header is None:
        print("ERROR: not a valid TA — missing <credentials> or <header>", file=sys.stderr)
        return 1
    token = creds.findtext("token", "")
    sign = creds.findtext("sign", "")
    exp = header.findtext("expirationTime", "")

    print(f"Token (first 40):  {token[:40]}…")
    print(f"Sign  (first 40):  {sign[:40]}…")
    print(f"Expiration:        {exp}")

    if exp:
        try:
            exp_dt = datetime.fromisoformat(exp)
            remaining = exp_dt - datetime.now(exp_dt.tzinfo)
            mins = int(remaining.total_seconds() // 60)
            if mins <= 0:
                print(f"Status:            ✗ EXPIRED {abs(mins)} min ago")
                return 2
            print(f"Status:            ✓ valid for {mins} more minutes")
        except ValueError:
            print("Status:            ⚠ could not parse expirationTime")
    return 0


if __name__ == "__main__":
    sys.exit(main())
