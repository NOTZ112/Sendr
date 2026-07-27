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
@app.on_message(filters.command("reply") & filters.private)
async def reply_user(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if len(message.command) < 3:
        return await message.reply_text(
            "Usage:\n/reply user_id message"
        )

    user_id = int(message.command[1])
    reply_text = message.text.split(None, 2)[2]

    try:
        await app.send_message(user_id, f"💬 Admin:\n\n{reply_text}")
        await message.reply_text("✅ Reply sent.")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/broadcast message"
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
        f"✅ Broadcast completed.\nSent: {sent}"
    )


@app.on_message(filters.command("stats") & filters.private)
async def stats(client, message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    total = await get_user_count()

    await message.reply_text(
        f"👥 Total Users: {total}"
    )
app.run()
