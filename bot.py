import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIG ===
TOKEN = "8219450701:AAF4CKj5ihdN5kAztEhZQVIFPO04MLII_Hs"  # Your bot token

# Tips content (neutral educational / life skills)
LIFE_TIPS = [
    "💡 គន្លឹះទី១៖ រៀបចំកិច្ចការប្រចាំថ្ងៃរបស់អ្នក ដើម្បីមានប្រសិទ្ធភាពកាន់តែប្រសើរ។",
    "💡 គន្លឹះទី២៖ យកពេលសម្រាកខ្លីៗ ដើម្បីធ្វើឱ្យខួរក្បាលស្រស់ស្រាយ។",
    "💡 គន្លឹះទី៣៖ កំណត់គោលដៅតូចៗប្រចាំថ្ងៃ។",
    "💡 គន្លឹះទី៤៖ រៀបចំតារាងការងាររបស់អ្នកឲ្យមានលំដាប់។",
    "💡 គន្លឹះទី៥៖ សិក្សាអ្វីថ្មីៗរាល់ថ្ងៃ ដើម្បីអភិវឌ្ឍជំនាញរបស់អ្នក។",
]

# Track which tip a user is currently on
user_tip_index = {}

# === LOGGING SETUP ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_tip_index[user_id] = 0  # Reset tip index

    keyboard = [
        [InlineKeyboardButton("💡 ទទួលយកគន្លឹះប្រចាំថ្ងៃ", callback_data="tip")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "សួស្តី! 👋\n\n"
        "បូតរៀនជីវិត 🌟\n"
        "ស្វែងយល់ពីគន្លឹះប្រចាំថ្ងៃ ដើម្បីអភិវឌ្ឍជីវិត និងទម្លាប់ល្អ។\n\n"
        "ជ្រើសរើសជម្រើសខាងក្រោម៖",
        reply_markup=reply_markup,
    )

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 ជំនួយ\n\n"
        "💡 ទទួលយកគន្លឹះប្រចាំថ្ងៃ → ទទួលបានគន្លឹះជីវិតជារៀងរាល់ថ្ងៃ\n\n"
        "សូមចុច /start ដើម្បីចាប់ផ្តើមឡើងវិញ 🌟"
    )

# --- BUTTON HANDLER ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()

    user_id = query.from_user.id

    if query.data == "tip":
        index = user_tip_index.get(user_id, 0)
        tip = LIFE_TIPS[index]

        await query.message.reply_text(tip)

        if index + 1 < len(LIFE_TIPS):
            user_tip_index[user_id] = index + 1
            keyboard = [
                [InlineKeyboardButton("💡 គន្លឹះបន្ទាប់", callback_data="tip")],
                [InlineKeyboardButton("⬅️ ត្រឡប់ទៅម៉ឺនុយ", callback_data="back")],
            ]
        else:
            user_tip_index[user_id] = 0
            keyboard = [
                [InlineKeyboardButton("⬅️ ត្រឡប់ទៅម៉ឺនុយ", callback_data="back")],
            ]

        await query.message.reply_text(
            "ជ្រើសរើសសកម្មភាពបន្ទាប់៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💡 ទទួលយកគន្លឹះប្រចាំថ្ងៃ", callback_data="tip")],
        ]
        await query.message.reply_text(
            "ត្រឡប់ទៅម៉ឺនុយដើម 🌟\nជ្រើសរើសជម្រើសថ្មី៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

# --- MAIN FUNCTION ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    # Delete old webhook (important)
    await app.bot.delete_webhook(drop_pending_updates=True)

    # Run webhook mode for Render
    port = int(os.environ.get("PORT", 8443))
    url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    logger.info(f"🤖 Bot is running on webhook URL: {url}")

    await app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
