"""
api/send_code.py
Demana el codi SMS a Telegram per iniciar sessió.
POST /api/send_code
Body: { "api_id": 12345, "api_hash": "xxx", "phone": "+34612345678" }
"""
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telethon import TelegramClient
from telethon.sessions import StringSession

def cors(handler):
    def wrapper(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        handler(self)
    return wrapper

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length))

        api_id   = int(body.get("api_id", 0))
        api_hash = body.get("api_hash", "").strip()
        phone    = body.get("phone", "").strip()

        if not api_id or not api_hash or not phone:
            self._respond(400, {"ok": False, "error": "Falten api_id, api_hash o phone"})
            return

        async def _send():
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.connect()
            result = await client.send_code_request(phone)
            # Guardem la sessió parcial per poder completar el login
            partial_session = client.session.save()
            await client.disconnect()
            return partial_session, result.phone_code_hash

        try:
            partial_session, phone_code_hash = asyncio.run(_send())
            self._respond(200, {
                "ok": True,
                "partial_session": partial_session,
                "phone_code_hash": phone_code_hash,
            })
        except Exception as e:
            self._respond(500, {"ok": False, "error": str(e)})

    def _respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args): pass
