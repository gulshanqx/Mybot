from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, ChatJoinRequestHandler, CallbackQueryHandler


BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
BOT_USERNAME = "YOUR_BOT_USERNAME_HERE_WITHOUT_@"

CHANNEL1 = "YOUR_CHANNEL_HERE_WITHOUT_@"
CHANNEL2 = "YOUR_CHANNEL_HERE_WITHOUT_@"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    buttons = [
        [
            InlineKeyboardButton("➕ Add me to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("📢 Add me to Channel", url=f"https://t.me/{BOT_USERNAME}?startchannel=true")
        ],
        [
            InlineKeyboardButton("🤖 Bot Updates", url=f"https://t.me/{CHANNEL1}"),
            InlineKeyboardButton("👨‍💻 More Bots", url=f"https://t.me/{CHANNEL2}")
        ],
        [
            InlineKeyboardButton("⚠️ Disclaimer", callback_data="disclaimer")
        ]
    ]

    text = f'Hi <a href="tg://settings">{user.first_name}</a>, I am a <b>Auto Approve Bot</b>. I can approve your channel or group join requests instantly.\n\n<b>Steps:</b>\n\nJust add me as an <b>administrator</b> to your group or channel to set me up!\n\nDisclaimer 👉 /disclaimer\n\nCreated By <b>@CoderAjinkya</b>'

    await update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "<b>📢 Disclaimer – Auto Approve Join Request Bot</b>\n\n🔹 This bot is an <b>automated system</b> that approves join requests in Telegram channels/groups based on predefined rules. By using this bot, you acknowledge and agree to the following:\n\n<b>✅ No Liability</b>\nThe bot owner & developers are <b>not responsible</b> for any unauthorized access, spam, or misuse. Channel/Group admins must configure settings responsibly.\n\n<b>🤖 Automated Decisions</b>\nThe bot works <b>automatically</b> based on set criteria. <b>It does not verify</b> user intent or guarantee member authenticity.\n\n<b>🔧 Admin Responsibility</b>\nChannel/Group admins are <b>fully responsible</b> for moderation. The bot <b>only accepts requests</b> and does not enforce any additional rules.\n\n<b>🚫 No Responsibility for Content</b>\nThe bot <b>does not control, monitor, or endorse any messages, media, or content</b> posted in the group/channel. The <b>channel admins and users are solely responsible</b> for all content shared. The bot owner & developers <b>cannot be held accountable</b> for any violations, illegal content, or disputes arising in the channel/group.\n\n<b>🔒 Privacy Notice</b>\nThe bot <b>does not store or share personal data</b> beyond what’s needed for join request processing.\n\n<b>📌 Ensure responsible usage to keep your channel/group secure!</b>"

    if update.message:
        await update.message.reply_text(
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )


async def disclaimer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    text = "<b>📢 Disclaimer – Auto Approve Join Request Bot</b>\n\n🔹 This bot is an <b>automated system</b> that approves join requests in Telegram channels/groups based on predefined rules. By using this bot, you acknowledge and agree to the following:\n\n<b>✅ No Liability</b>\nThe bot owner & developers are <b>not responsible</b> for any unauthorized access, spam, or misuse. Channel/Group admins must configure settings responsibly.\n\n<b>🤖 Automated Decisions</b>\nThe bot works <b>automatically</b> based on set criteria. <b>It does not verify</b> user intent or guarantee member authenticity.\n\n<b>🔧 Admin Responsibility</b>\nChannel/Group admins are <b>fully responsible</b> for moderation. The bot <b>only accepts requests</b> and does not enforce any additional rules.\n\n<b>🚫 No Responsibility for Content</b>\nThe bot <b>does not control, monitor, or endorse any messages, media, or content</b> posted in the group/channel. The <b>channel admins and users are solely responsible</b> for all content shared. The bot owner & developers <b>cannot be held accountable</b> for any violations, illegal content, or disputes arising in the channel/group.\n\n<b>🔒 Privacy Notice</b>\nThe bot <b>does not store or share personal data</b> beyond what’s needed for join request processing.\n\n<b>📌 Ensure responsible usage to keep your channel/group secure!</b>"

    await query.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    req = update.chat_join_request
    chat = req.chat
    user = req.from_user

    await context.bot.approve_chat_join_request(
        chat_id=chat.id,
        user_id=user.id
    )

    button = [
        [InlineKeyboardButton("ℹ️ Know More", url=f"https://t.me/{BOT_USERNAME}?start=approved")]
    ]

    if chat.type in ["group", "supergroup"]:

        text = f'Hello <a href="tg://user?id={user.id}">{user.first_name}</a>,\n\nYour request to join "{chat.title}" has been approved!\n\nClick <a href="https://t.me/{BOT_USERNAME}?start=approved">/start</a> to Know More.'

        await context.bot.send_message(
            chat_id=chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )

    else:

        text = f'Hello <a href="tg://settings">{user.first_name}</a>,\n\nYour request to join "{chat.title}" has been approved!\n\nClick /start to Know More.\n\nCreated By: <b>@{CHANNEL1}</b>'

        await context.bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True
        )


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("disclaimer", disclaimer))
    app.add_handler(CallbackQueryHandler(disclaimer_callback, pattern="disclaimer"))
    app.add_handler(ChatJoinRequestHandler(approve_request))

    app.run_polling()


if __name__ == "__main__":
    main()
