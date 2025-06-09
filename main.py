import os
import asyncio
import nest_asyncio
import re
from telegram import Update, MessageOriginUser, MessageOriginHiddenUser
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

nest_asyncio.apply()

# BOT_TOKEN is now read from the environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables.")

CHANNEL_MAP = {
    -1001709705933: -1002550471058,
}

feedback_count = 0  # Global counter

def process_caption(text: str) -> str:
    if not text:
        return None
    text = re.sub(r"(?i)lucky", "exo", text)
    return text

def get_forwarded_from(msg) -> str:
    origin = msg.forward_origin
    if isinstance(origin, MessageOriginUser):
        user = origin.sender_user
        return f"Feedback from @{user.username}" if user.username else f"Forwarded from {user.full_name}"
    elif isinstance(origin, MessageOriginHiddenUser):
        return f"Feedback from {origin.sender_user_name}"
    return "Feedback message"

async def handle_forwarded_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global feedback_count
    msg = update.effective_message
    if not msg or not msg.forward_origin:
        return

    source_chat_id = update.effective_chat.id
    target_chat_id = CHANNEL_MAP.get(source_chat_id)
    if not target_chat_id:
        return

    feedback_count += 1
    forward_from = get_forwarded_from(msg)
    suffix = f"\n\n#{feedback_count} 🔗 @exgwallhack"

    try:
        if msg.photo:
            caption = process_caption(msg.caption or "")
            final_caption = f"{forward_from}\n\n{caption}{suffix}" if caption else f"{forward_from}{suffix}"
            await context.bot.send_photo(chat_id=target_chat_id, photo=msg.photo[-1].file_id, caption=final_caption)

        elif msg.video:
            caption = process_caption(msg.caption or "")
            final_caption = f"{forward_from}\n\n{caption}{suffix}" if caption else f"{forward_from}{suffix}"
            await context.bot.send_video(chat_id=target_chat_id, video=msg.video.file_id, caption=final_caption)

        elif msg.document:
            caption = process_caption(msg.caption or "")
            final_caption = f"{forward_from}\n\n{caption}{suffix}" if caption else f"{forward_from}{suffix}"
            await context.bot.send_document(chat_id=target_chat_id, document=msg.document.file_id, caption=final_caption)

        elif msg.text:
            caption = process_caption(msg.text)
            final_caption = f"{forward_from}\n\n{caption}{suffix}" if caption else f"{forward_from}{suffix}"
            await context.bot.send_message(chat_id=target_chat_id, text=final_caption)

    except Exception as e:
        print(f"[❌ Error forwarding] {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.FORWARDED, handle_forwarded_feedback))
    print("🤖 Bot is running in Railway (async mode)...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())