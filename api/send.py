"""
api/send.py
Envia un missatge de Telegram com a l'usuari autenticat.
POST /api/send
Body: {
  "api_id": 12345,
  "api_hash": "xxx",
  "session_string": "xxx",
  "command": "/llum_on",
  "chat_id": -1003082954760
}
"""
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telethon import TelegramClient
from telethon.sessions import StringSession

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

        api_id         = int(body.get("api_id", 0))
        api_hash       = body.get("api_hash", "").strip()
        session_string = body.get("session_string", "").strip()
        command        = body.get("command", "").strip()
        chat_id        = body.get("chat_id")

        if not all([api_id, api_hash, session_string, command, chat_id]):
            self._respond(400, {"ok": False, "error": "Falten dades"})
            return

        async def _send():
            client = TelegramClient(StringSession(session_string), api_id, api_hash)
            await client.connect()
            if not await client.is_user_authorized():
                raise Exception("Sessió no vàlida. Torna a fer login.")
            await client.send_message(int(chat_id), command)
            await client.disconnect()

        try:
            asyncio.run(_send())
            self._respond(200, {"ok": True, "sent": command})
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
