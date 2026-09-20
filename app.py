#!/usr/bin/env python3
import json
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "seal.db"
WEB = ROOT / "web"
MIGRATE = ROOT / "migrate.sql"


def migrate():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    try:
        con.executescript(MIGRATE.read_text(encoding="utf-8"))
        con.commit()
    finally:
        con.close()


def db_ready():
    try:
        con = sqlite3.connect(DB)
        try:
            con.execute("SELECT 1 FROM seals LIMIT 1")
        finally:
            con.close()
    except sqlite3.Error:
        return False
    return True


def load_rows():
    if not DB.exists():
        return []
    con = sqlite3.connect(DB)
    try:
        cur = con.execute("SELECT code, grams FROM seals ORDER BY id")
        return [{"code": row[0], "grams": row[1]} for row in cur]
    except sqlite3.OperationalError:
        return []
    finally:
        con.close()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type):
        raw = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/seals":
            self._send(200, json.dumps({"ok": True, "rows": load_rows()}), "application/json")
            return
        if path == "/health":
            if db_ready():
                self._send(200, json.dumps({"up": True}), "application/json")
            else:
                self._send(503, json.dumps({"up": False}), "application/json")
            return
        if path == "/":
            path = "/index.html"
        file_path = (WEB / path.lstrip("/")).resolve()
        if not str(file_path).startswith(str(WEB.resolve())) or not file_path.is_file():
            self._send(404, "missing", "text/plain; charset=utf-8")
            return
        kind = "text/html; charset=utf-8" if file_path.suffix == ".html" else "text/javascript; charset=utf-8"
        self._send(200, file_path.read_bytes(), kind)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/seals":
            self._send(404, "missing", "text/plain; charset=utf-8")
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if not DB.exists():
            self._send(200, json.dumps({"ok": True, "stored": False}), "application/json")
            return
        con = sqlite3.connect(DB)
        try:
            con.execute(
                "INSERT INTO seals(code, grams) VALUES (?, ?)",
                (payload.get("code", ""), int(payload.get("grams", 0))),
            )
            con.commit()
        except sqlite3.OperationalError:
            self._send(200, json.dumps({"ok": True, "stored": False}), "application/json")
            return
        finally:
            con.close()
        self._send(200, json.dumps({"ok": True, "stored": True}), "application/json")

    def log_message(self, fmt, *args):
        return


def main():
    try:
        migrate()
    except (OSError, sqlite3.Error) as exc:
        print(f"migrate failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
    port = int(os.environ.get("PORT", "8761"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
