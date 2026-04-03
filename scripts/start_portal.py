#!/usr/bin/env python3
"""Start the CSA roadmap portal locally and print follow-along guidance.

Usage:
  python scripts/start_portal.py
  python scripts/start_portal.py --port 8000 --no-open
"""

from __future__ import annotations

import argparse
import http.server
import socket
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.connect_ex(("127.0.0.1", port)) != 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local portal with onboarding guidance.")
    parser.add_argument("--port", type=int, default=5500, help="Port to host portal (default: 5500)")
    parser.add_argument("--no-open", action="store_true", help="Do not auto-open browser")
    return parser.parse_args()


def print_follow_along(url: str) -> None:
    print("\n" + "=" * 72)
    print("CSA Roadmap Portal is running")
    print("=" * 72)
    print(f"Portal URL: {url}")
    print()
    print("Follow-along steps:")
    print("1. Open README.md for program context")
    print("2. In portal, go to Day-One Quick Start section")
    print("3. Open docs/PLAN_TEMPLATE.md and fill owner/date/pace")
    print("4. Open projects/INDEX.md and map your projects to A-D")
    print("5. Start week-01/WEEK_ASSIGNMENT.md and week-01/STATUS.md")
    print("6. Track gaps in docs/SKILL_ASSESSMENT_TEMPLATE.md")
    print()
    print("Tip: Press Ctrl+C to stop the local portal server.")
    print("=" * 72 + "\n")


def main() -> int:
    args = parse_args()

    if not ROOT.joinpath("index.html").exists():
        print("ERROR: index.html was not found. Run this from inside the repository.")
        return 1

    if not is_port_available(args.port):
        print(f"ERROR: Port {args.port} is already in use.")
        print("Try another port, for example: python scripts/start_portal.py --port 5600")
        return 1

    # Serve from repository root so local links and assets resolve correctly.
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *handler_args, **handler_kwargs):
            super().__init__(*handler_args, directory=str(ROOT), **handler_kwargs)

    url = f"http://127.0.0.1:{args.port}/index.html"
    print_follow_along(url)

    if not args.no_open:
        webbrowser.open(url)

    try:
        with socketserver.TCPServer(("", args.port), Handler) as httpd:
            httpd.serve_forever()
        return 0
    except KeyboardInterrupt:
        print("\nPortal server stopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
