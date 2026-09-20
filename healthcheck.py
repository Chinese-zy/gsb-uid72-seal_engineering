#!/usr/bin/env python3
import json
import os
import sys
import urllib.request


def main():
    port = int(os.environ.get("PORT", "8080"))
    url = f"http://127.0.0.1:{port}/health"
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            if resp.status != 200:
                return 1
            body = json.loads(resp.read().decode())
    except Exception:
        return 1
    return 0 if body.get("up") is True else 1


if __name__ == "__main__":
    sys.exit(main())
