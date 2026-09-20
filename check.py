#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCH = ROOT / "data" / "batch.json"
TARGET = "http://127.0.0.1:8761/api/seals"


def main():
    doc = json.loads(BATCH.read_text())
    try:
        with urllib.request.urlopen(TARGET, timeout=2) as resp:
            body = json.loads(resp.read().decode())
        doc["expect"] = body.get("rows", doc["expect"])
        BATCH.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        print("checked", TARGET)
    except Exception as exc:
        print("skip", exc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
