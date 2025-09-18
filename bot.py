from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIG ===
BOT_TOKEN = "8433743669:AAFZZVnAmY1co3cF7N8K-ZwHMTGrwRlfxRU"            # Yahan apna BotFather token daalo
SUPPORT_CHAT_ID = -1002943341136        # Yahan apna group chat ID daalo

# Dictionary to map group message_id ↔️ user_id
user_message_map = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello 👋\nWelcome to ASISX Support Bot 🚀\n\nType your message, our team will reply soon."
    )

# Handle user messages
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Prepare username display
    username = f"@{user.username}" if user.username else "NoUsername"

    # Forward user message to support group
    sent_msg = await context.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=f"📩 Message from {user.first_name} ({username})\nUser ID: {user.id}\n\n{text}"
    )

    # Map group message id with user id
    user_message_map[sent_msg.message_id] = user.id

    # Confirm to user
    await update.message.reply_text("✅ Your message has been sent to our support team.")

# Handle support group replies
async def handle_group_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        replied_msg_id = update.message.reply_to_message.message_id

        if replied_msg_id in user_message_map:
            user_id = user_message_map[replied_msg_id]

            # Forward reply back to the user
            await context.bot.send_message(
                chat_id=user_id,
                text=f"💬 Support Team: {update.message.text}"
            )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # User messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.Chat(SUPPORT_CHAT_ID), handle_user_message))

    # Group replies
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(SUPPORT_CHAT_ID), handle_group_reply))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()