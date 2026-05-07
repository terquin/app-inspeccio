"""
api/verify_code.py
Verifica el codi SMS i retorna el session_string complet.
POST /api/verify_code
Body: {
  "api_id": 12345,
  "api_hash": "xxx",
  "phone": "+34612345678",
  "code": "12345",
  "phone_code_hash": "xxx",
  "partial_session": "xxx"
}
"""
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

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

        api_id          = int(body.get("api_id", 0))
        api_hash        = body.get("api_hash", "").strip()
        phone           = body.get("phone", "").strip()
        code            = body.get("code", "").strip()
        phone_code_hash = body.get("phone_code_hash", "").strip()
        partial_session = body.get("partial_session", "").strip()
        password        = body.get("password", "").strip()  # 2FA si cal

        if not all([api_id, api_hash, phone, code, phone_code_hash, partial_session]):
            self._respond(400, {"ok": False, "error": "Falten dades"})
            return

        async def _verify():
            client = TelegramClient(StringSession(partial_session), api_id, api_hash)
            await client.connect()
            try:
                await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
            except SessionPasswordNeededError:
                if not password:
                    raise Exception("2FA_REQUIRED")
                await client.sign_in(password=password)
            session_string = client.session.save()
            me = await client.get_me()
            await client.disconnect()
            return session_string, me.first_name, me.username

        try:
            session_string, first_name, username = asyncio.run(_verify())
            self._respond(200, {
                "ok": True,
                "session_string": session_string,
                "name": first_name,
                "username": username,
            })
        except Exception as e:
            err = str(e)
            if "2FA_REQUIRED" in err:
                self._respond(200, {"ok": False, "needs_2fa": True})
            else:
                self._respond(500, {"ok": False, "error": err})

    def _respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args): pass
