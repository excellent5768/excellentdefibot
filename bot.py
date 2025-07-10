import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# SECURITY WARNING: Hardcoded token - REVOKE THIS IMMEDIATELY AFTER USE!
BOT_TOKEN = "7597903783:AAEOOsGPcAFCNtlGde4fCtrpQ6C3jKL8T4k"  # <<< REVOKE IN @BOTFATHER LATER!
TELEGRAM_CHANNEL = "@YourAirdropChannel"  # Replace with your channel
TELEGRAM_GROUP = "@YourAirdropGroup"  # Replace with your group
TWITTER_USERNAME = "YourTwitterHandle"  # Replace with your Twitter

# Bot States
START, WAITING_WALLET = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton("✅ Verify Tasks", callback_data="verify")]]
    
    await update.message.reply_text(
        "🎉 Welcome to the SOL Airdrop Bot!\n\n"
        "Complete these steps to claim 10 SOL:\n"
        f"1. Join Telegram Channel: {TELEGRAM_CHANNEL}\n"
        f"2. Join Telegram Group: {TELEGRAM_GROUP}\n"
        f"3. Follow Twitter: https://twitter.com/{TWITTER_USERNAME}\n\n"
        "Click ✅ Verify Tasks when done!",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return START

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "verify":
        await query.edit_message_text("🔑 Enter your Solana wallet address:")
        return WAITING_WALLET
    return START

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    wallet_address = update.message.text
    await update.message.reply_text(
        f"🚀 Congratulations! 10 SOL is on its way to:\n\n`{wallet_address}`\n\n"
        "Note: This is a simulation. No actual crypto will be sent.",
        parse_mode="Markdown"
    )
    return START

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    app.add_error_handler(error)
    
    # Deployment configuration
    if "RENDER" in os.environ:
        PORT = int(os.environ.get("PORT", 5000))
        webhook_url = f"https://your-service-name.onrender.com/{BOT_TOKEN}"
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=webhook_url
        )
        print(f"Webhook running at: {webhook_url}")
    else:
        print("Polling mode active")
        app.run_polling()

if __name__ == "__main__":
    main()
