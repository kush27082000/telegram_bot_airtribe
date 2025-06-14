import os
import threading
import requests
from flask import Flask, request, jsonify

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import httpx
import re


print("this is 1st line of code")
# Flask app for sending messages/photos to Telegram
flask_app = Flask(__name__)


print("this is 2nd line of code")
BOT_TOKEN = ''
CHAT_ID = ''

# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("this is third line of code") 
    raise RuntimeError("BOT_TOKEN and CHAT_ID environment variables must be set.")

def send_text(message):
    print("this is fourth line of code")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    raw_text = message
    print("Raw response from API:")
    print(raw_text)

    # Format the response
    # if raw_text.startswith("Summary:"):
    #     raw_text = raw_text[len("Summary:"):]

    raw_text = raw_text.replace("\\n", "\n").strip()
    raw_text = re.sub(r'\n+', '\n', raw_text)
    formatted_text = re.sub(r'(\s*-\s.*?)(\.)\n', r'\1\n', raw_text)

    print("Formatted response:")
    print(formatted_text)
    payload = {
        'chat_id': CHAT_ID,
        'text': formatted_text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()

def send_image(image, caption=None):
    print("this is 5th line of code")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': image}
    data = {'chat_id': CHAT_ID}
    if caption:
        data['caption'] = caption
    response = requests.post(url, files=files, data=data)
    return response.json()

@flask_app.route('/send', methods=['POST'])
def send():
    print("this is 6th line of code")
    message = request.form.get('message')
    image = request.files.get('image')
    if image:
        result = send_image(image, caption=message)
    else:
        result = send_text(message)
    return jsonify(result)

# Telegram bot handlers
FASTAPI_URL = "https://tangy-roses-design.loca.lt/v1/ask"  # Flask runs on port 5000 by default

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("this is 7th line of code")
    
    user = update.effective_user.first_name
    text = update.message.text
    print(f"Message from {user}: {text}")

    # Send message to GET API with query param
    async with httpx.AsyncClient() as client:
        response = await client.get(
            FASTAPI_URL,
            params={"query": text},
            headers={"accept": "*/*"}
        )

    raw_text = response.text
    print("Raw response from API:")
    print(raw_text)

    # Format the response
    if raw_text.startswith("Summary:"):
        raw_text = raw_text[len("Summary:"):]

    raw_text = raw_text.replace("\\n", "\n").strip()
    raw_text = re.sub(r'\n+', '\n', raw_text)
    formatted_text = re.sub(r'(\s*-\s.*?)(\.)\n', r'\1\n', raw_text)

    print("Formatted response:")
    print(formatted_text)

    # Send the formatted text back to the user
    await update.message.reply_text(
        f"You said: {text}\n\nReceived Response:\n{formatted_text}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("this is 8th line of code")
    await update.message.reply_text("Hello! Send me any message and I’ll print it.")

def run_flask():
    print("this is 9th line of code")
    flask_app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

def run_telegram_bot():
    print("this is 10th line of code")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    print("this is 11th line of code")
    # Run Flask and Telegram bot in parallel
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_telegram_bot()
