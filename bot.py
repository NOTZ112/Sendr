from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "SupportBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "👋 Welcome!\n\n"
        "Support Bot Ready ✅"
    )


print("✅ Support Bot Started")
app.run()
