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

    await message.forward(ADMIN_ID)

    await message.reply_text(
        "✅ നിങ്ങളുടെ മെസ്സേജ് Admin-ലേക്ക് അയച്ചിരിക്കുന്നു."
    )
    @app.on_message(filters.private & filters.reply)
async def admin_reply(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.reply_to_message.forward_from:
        return await message.reply_text("❌ User message-ന് reply ചെയ്യൂ.")

    user_id = message.reply_to_message.forward_from.id

    try:
        if message.text:
            await app.send_message(user_id, f"💬 Admin:\n\n{message.text}")
        elif message.photo:
            await app.send_photo(
                user_id,
                message.photo.file_id,
                caption=message.caption or ""
            )
        elif message.document:
            await app.send_document(
                user_id,
                message.document.file_id,
                caption=message.caption or ""
            )
        elif message.video:
            await app.send_video(
                user_id,
                message.video.file_id,
                caption=message.caption or ""
            )

        await message.reply_text("✅ Reply sent.")

    except Exception as e:
        await message.reply_text(f"❌ {e}")
        @app.on_message(filters.command("stats") & filters.private)
async def stats(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    total = await get_user_count()
    await message.reply_text(f"👥 Total Users: {total}")


@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/broadcast Your message"
        )

    text = message.text.split(None, 1)[1]

    users = await get_users()

    sent = 0

    for user in users:
        try:
            await app.send_message(user, text)
            sent += 1
        except:
            pass

    await message.reply_text(
        f"✅ Broadcast completed.\n\nSent: {sent}"
    )


print("✅ Support Bot Started")
app.run()
