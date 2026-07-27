from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

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


@app.on_message(filters.private & ~filters.command("start"))
async def forward_to_admin(client, message: Message):
    if message.from_user.id == ADMIN_ID:
        return

    await client.forward_messages(
        chat_id=ADMIN_ID,
        from_chat_id=message.chat.id,
        message_ids=message.id
    )

    await message.reply_text(
        "✅ നിങ്ങളുടെ മെസ്സേജ് Admin-ലേക്ക് അയച്ചിരിക്കുന്നു."
    )

print("✅ Support Bot Started")
app.run()
