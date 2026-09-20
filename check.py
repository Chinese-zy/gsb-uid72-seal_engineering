#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "data" / "seed.json"
EXPECT = ROOT / "data" / "expect.json"
TARGET = os.environ.get("CHECK_TARGET", "http://127.0.0.1:8762")


def wait_ready(tries=30, delay=1.0):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(TARGET + "/health", timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def post_sample(sample):
    req = urllib.request.Request(
        TARGET + "/api/seals",
        data=json.dumps(sample).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = json.loads(resp.read().decode())
    if not body.get("stored"):
        raise RuntimeError(f"sample not stored: {sample}")


def get_rows():
    with urllib.request.urlopen(TARGET + "/api/seals", timeout=5) as resp:
        return json.loads(resp.read().decode()).get("rows", [])


def main():
    samples = json.loads(SEED.read_text(encoding="utf-8"))["samples"]
    expect = json.loads(EXPECT.read_text(encoding="utf-8"))["expect"]
    if not wait_ready():
        print(f"not ready: {TARGET}", file=sys.stderr)
        return 1
    try:
        for sample in samples:
            post_sample(sample)
        rows = get_rows()
    except Exception as exc:
        print(f"check failed: {exc}", file=sys.stderr)
        return 1
    if rows != expect:
        print(f"mismatch: got {rows}, expect {expect}", file=sys.stderr)
        return 1
    print("ok", TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
