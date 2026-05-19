"""
local_trigger.py — roda na sua máquina local.
Expõe http://localhost:9000/refresh para o frontend disparar a coleta.

Uso:
    cd D:\Downloads\ADSFILES\backend
    python local_trigger.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Garante que usa o banco do Render via .env
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

_running = False


def run_pipeline_thread():
    global _running
    _running = True
    try:
        print("[TRIGGER] Iniciando pipeline...")
        from app.pipeline.runner import run_pipeline
        run_pipeline()
        print("[TRIGGER] Pipeline concluído.")
    except Exception as e:
        print(f"[TRIGGER] Erro: {e}")
    finally:
        _running = False


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/status":
            self._json({"running": _running})
        else:
            self._json({"status": "local_trigger_ok"})

    def do_POST(self):
        global _running
        if self.path == "/refresh":
            if _running:
                self._json({"status": "already_running"})
                return
            t = threading.Thread(target=run_pipeline_thread, daemon=True)
            t.start()
            self._json({"status": "started"})
        else:
            self._json({"error": "unknown"}, 404)

    def _json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        print(f"[TRIGGER] {self.address_string()} {format % args}")


if __name__ == "__main__":
    port = 9000
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"[TRIGGER] Servidor local rodando em http://localhost:{port}")
    print(f"[TRIGGER] POST http://localhost:{port}/refresh para disparar coleta")
    server.serve_forever()