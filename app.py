import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = os.environ["ADMIN_ID"]

API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message")

    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            "👋 Привет!\n\n"
            "Это анонимная предложка.\n"
            "Напиши своё предложение одним сообщением 👇"
        )
        return "ok"

    if text:
        username = message["from"].get("username")
        user_info = f"@{username}" if username else "без username"

        admin_text = (
            "📩 НОВОЕ ПРЕДЛОЖЕНИЕ\n\n"
            f"👤 Отправитель: {user_info}\n"
            f"🆔 ID: {chat_id}\n\n"
            f"💬 {text}"
        )

        send_message(ADMIN_ID, admin_text)

        send_message(
            chat_id,
            "✅ Предложение отправлено!"
        )

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
