from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
from database import add_user, get_users, get_user_count

app = Client(
    "SupportBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message: Message):
    await add_user(message.from_user.id)

    await message.reply_text(
        "👋 Welcome!\n\n"
        "📩 നിങ്ങളുടെ മെസ്സേജ് അയയ്ക്കൂ.\n"
        "Admin ഉടൻ Reply നൽകുന്നതാണ്."
    )


@app.on_message(filters.private & ~filters.command("start"))
async def support_message(client, message: Message):
    if message.from_user.id == ADMIN_ID:
        return

    await add_user(message.from_user.id)

    caption = (
        f"📩 New Support Message\n\n"
        f"👤 {message.from_user.first_name}\n"
        f"🆔 `{message.from_user.id}`"
    )

    if message.text:
        caption += f"\n\n💬 {message.text}"

    await app.send_message(ADMIN_ID, caption)

    if message.text:
        await app.send_message(
            ADMIN_ID,
            f"/reply {message.from_user.id} "
            f"{message.text}"
        )

    await message.reply_text(
        "✅ നിങ്ങളുടെ മെസ്സേജ് Admin-ലേക്ക് അയച്ചു."
    )


print("✅ Support Bot Started")
app.run()
