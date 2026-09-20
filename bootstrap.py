#!/usr/bin/env python3
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "seal.db"
MIGRATE = ROOT / "migrate.sql"
SEED = ROOT / "data" / "seed.json"


def main():
    con = sqlite3.connect(DB)
    try:
        con.executescript(MIGRATE.read_text(encoding="utf-8"))
        count = con.execute("SELECT COUNT(*) FROM seals").fetchone()[0]
        if count == 0 and SEED.is_file():
            rows = json.loads(SEED.read_text(encoding="utf-8"))
            con.executemany(
                "INSERT INTO seals(code, grams) VALUES (?, ?)",
                [(row["code"], int(row["grams"])) for row in rows],
            )
        con.commit()
    finally:
        con.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"bootstrap failed: {exc}", file=sys.stderr)
        sys.exit(1)
