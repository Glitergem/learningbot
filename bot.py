import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIG ===
TOKEN = "8219450701:AAF4CKj5ihdN5kAztEhZQVIFPO04MLII_Hs"  # Your bot token
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# Tips content (neutral educational / life skills)
LIFE_TIPS = [
    "💡 Tip 1: Prioritize your daily tasks to be more productive.",
    "💡 Tip 2: Take short breaks to refresh your mind.",
    "💡 Tip 3: Set achievable goals every day.",
    "💡 Tip 4: Stay organized by keeping a to-do list.",
    "💡 Tip 5: Learn something new every day to grow your skills.",
]

# Track which tip a user is currently on
user_tip_index = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_tip_index[user_id] = 0  # Reset tip index

    keyboard = [
        [InlineKeyboardButton("💡 Get Life Tips", callback_data="tip")],
        [InlineKeyboardButton("🔗 Go to Main Bot", url=MAIN_BOT_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Hello! 👋\n\n"
        "Life Learning Bot 🌟\n"
        "Discover useful daily tips to improve your skills and habits.\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
    )

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Help\n\n"
        "💡 Get Life Tips → Receive short daily tips\n"
        "🔗 Go to Main Bot → Access additional features\n\n"
        "Press /start to begin again 🌟"
    )

# --- BUTTON HANDLER ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()

    user_id = query.from_user.id

    if query.data == "tip":
        # Get current tip index
        index = user_tip_index.get(user_id, 0)
        tip = LIFE_TIPS[index]

        await query.message.reply_text(tip)

        # Prepare next tip or reset
        if index + 1 < len(LIFE_TIPS):
            user_tip_index[user_id] = index + 1
            keyboard = [
                [InlineKeyboardButton("💡 Next Tip", callback_data="tip")],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back")],
                [InlineKeyboardButton("🔗 Go to Main Bot", url=MAIN_BOT_LINK)],
            ]
        else:
            user_tip_index[user_id] = 0  # Reset after last tip
            keyboard = [
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back")],
                [InlineKeyboardButton("🔗 Go to Main Bot", url=MAIN_BOT_LINK)],
            ]

        await query.message.reply_text(
            "Choose your next action:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💡 Get Life Tips", callback_data="tip")],
            [InlineKeyboardButton("🔗 Go to Main Bot", url=MAIN_BOT_LINK)],
        ]
        await query.message.reply_text(
            "Back to main menu 🌟\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

# --- MAIN FUNCTION ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("🤖 Life Learning Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
