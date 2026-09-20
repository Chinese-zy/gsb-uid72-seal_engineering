#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = ROOT / "data" / "expected.json"
TARGET = os.environ.get("TARGET", "http://127.0.0.1:8762/api/seals")


def main():
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    try:
        with urllib.request.urlopen(TARGET, timeout=5) as resp:
            if resp.status != 200:
                print(f"check failed: HTTP {resp.status} from {TARGET}")
                return 1
            body = json.loads(resp.read().decode())
    except Exception as exc:
        print(f"check failed: cannot reach {TARGET}: {exc}")
        return 1

    rows = body.get("rows")
    if body.get("ok") is not True or rows != expected:
        print("check failed: rows mismatch")
        print(f"  expected: {json.dumps(expected, ensure_ascii=False)}")
        print(f"  actual:   {json.dumps(rows, ensure_ascii=False)}")
        return 1

    print("checked", TARGET)
    print(f"  rows: {json.dumps(rows, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
