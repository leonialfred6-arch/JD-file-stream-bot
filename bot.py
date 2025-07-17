import os
from pyrogram import Client, filters
from flask import Flask, send_file
import threading

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://your-domain.com")
DOWNLOAD_FOLDER = "downloads"

app = Flask(__name__)

@app.route("/stream/<filename>")
def stream(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=False)
    return "❌ Not found", 404

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.video | filters.audio | filters.document)
async def handle_file(client, message):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    file_path = await message.download(file_name=DOWNLOAD_FOLDER + "/")
    filename = os.path.basename(file_path)
    url = f"{BASE_URL}/stream/{filename}"
    await message.reply_text(f"✅ Stream here:\n{url}")

def start_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    bot.run()
  
