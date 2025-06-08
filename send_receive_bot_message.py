import os
import threading
import requests
from flask import Flask, request, jsonify

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import httpx

# Flask app for sending messages/photos to Telegram
flask_app = Flask(__name__)

BOT_TOKEN = '7397869585:AAEIY4scwGbkiURELozPmbny5wER1DHK1WU'
CHAT_ID = '5629181035'

# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("BOT_TOKEN and CHAT_ID environment variables must be set.")

def send_text(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

def send_image(image, caption=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': image}
    data = {'chat_id': CHAT_ID}
    if caption:
        data['caption'] = caption
    response = requests.post(url, files=files, data=data)
    return response.json()

@flask_app.route('/send', methods=['POST'])
def send():
    message = request.form.get('message')
    image = request.files.get('image')
    if image:
        result = send_image(image, caption=message)
    else:
        result = send_text(message)
    return jsonify(result)

# Telegram bot handlers
FASTAPI_URL = "https://postman-rest-api-learner.glitch.me/info"  # Flask runs on port 5000 by default

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    text = update.message.text
    print(f"Message from {user}: {text}")

    # Send message to Flask endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FASTAPI_URL,
            data={"name": text}
        )
    status = response.json().get("message", "unknown")
    print(response.json().get("message", "unknown"))
    # status = "Message sent successfully"
    # print(f"Response from Flask: {status}")
    # Reply to the user in Telegram

    await update.message.reply_text(f"You said: {text}\nReceive Response from destination: {status}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me any message and I’ll print it.")

def run_flask():
    flask_app.run(debug=True, use_reloader=False)

def run_telegram_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    # Run Flask and Telegram bot in parallel
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_telegram_bot()
