import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIG ===
TOKEN = "8219450701:AAF4CKj5ihdN5kAztEhZQVIFPO04MLII_Hs"  # Your bot token
MAIN_BOT_LINK = "https://t.me/faxkh888888888bot"

# មាតិកាគន្លឹះជីវិតប្រចាំថ្ងៃ
LIFE_TIPS = [
    "💡 គន្លឹះទី១៖ រៀបចំភារកិច្ចប្រចាំថ្ងៃរបស់អ្នកតាមអាទិភាព។",
    "💡 គន្លឹះទី២៖ យកពេលសម្រាកខ្លីៗដើម្បីសម្រាកខួរក្បាល។",
    "💡 គន្លឹះទី៣៖ កំណត់គោលដៅតូចៗដែលអាចសម្រេចបានរាល់ថ្ងៃ។",
    "💡 គន្លឹះទី៤៖ តែងតែមានការរៀបចំដោយប្រើបញ្ជីភារកិច្ច (to-do list)។",
    "💡 គន្លឹះទី៥៖ រៀនអ្វីថ្មីៗរាល់ថ្ងៃ ដើម្បីបង្កើនជំនាញរបស់អ្នក។",
]

# តាមដានថាបច្ចុប្បន្នអ្នកប្រើកំពុងនៅលើគន្លឹះណា
user_tip_index = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_tip_index[user_id] = 0  # កំណត់សារថ្មីចាប់ផ្តើមពីគន្លឹះទី១

    keyboard = [
        [InlineKeyboardButton("💡 ទទួលបានគន្លឹះជីវិត", callback_data="tip")],
        [InlineKeyboardButton("🔗 ទៅកាន់បូតចម្បង", url=MAIN_BOT_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "សួស្តី! 👋\n\n"
        "បូតរៀនជីវិត 🌟\n"
        "ស្វែងយល់ពីគន្លឹះប្រចាំថ្ងៃ ដើម្បីបង្កើនជំនាញ និងទម្លាប់ល្អៗ។\n\n"
        "សូមជ្រើសរើសជម្រើសខាងក្រោម៖",
        reply_markup=reply_markup,
    )

# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 ជំនួយ\n\n"
        "💡 ទទួលបានគន្លឹះជីវិត → ទទួលបានគន្លឹះប្រចាំថ្ងៃខ្លីៗ\n"
        "🔗 ទៅកាន់បូតចម្បង → ចូលទៅកាន់មុខងារបន្ថែម\n\n"
        "សូមវាយ /start ដើម្បីចាប់ផ្តើមឡើងវិញ 🌟"
    )

# --- BUTTON HANDLER ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()

    user_id = query.from_user.id

    if query.data == "tip":
        # ទទួលបានគន្លឹះបច្ចុប្បន្ន
        index = user_tip_index.get(user_id, 0)
        tip = LIFE_TIPS[index]

        await query.message.reply_text(tip)

        # រៀបចំសម្រាប់គន្លឹះបន្ទាប់ ឬកំណត់ឡើងវិញ
        if index + 1 < len(LIFE_TIPS):
            user_tip_index[user_id] = index + 1
            keyboard = [
                [InlineKeyboardButton("💡 គន្លឹះបន្ទាប់", callback_data="tip")],
                [InlineKeyboardButton("⬅️ ត្រឡប់ទៅម៉ឺនុយ", callback_data="back")],
                [InlineKeyboardButton("🔗 ទៅកាន់បូតចម្បង", url=MAIN_BOT_LINK)],
            ]
        else:
            user_tip_index[user_id] = 0  # កំណត់ឡើងវិញបន្ទាប់ពីគន្លឹះចុងក្រោយ
            keyboard = [
                [InlineKeyboardButton("⬅️ ត្រឡប់ទៅម៉ឺនុយ", callback_data="back")],
                [InlineKeyboardButton("🔗 ទៅកាន់បូតចម្បង", url=MAIN_BOT_LINK)],
            ]

        await query.message.reply_text(
            "សូមជ្រើសរើសសកម្មភាពបន្ទាប់៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💡 ទទួលបានគន្លឹះជីវិត", callback_data="tip")],
            [InlineKeyboardButton("🔗 ទៅកាន់បូតចម្បង", url=MAIN_BOT_LINK)],
        ]
        await query.message.reply_text(
            "ត្រឡប់ទៅម៉ឺនុយដើម 🌟\nសូមជ្រើសរើសជម្រើស៖",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

# --- MAIN FUNCTION ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("🤖 បូតរៀនជីវិត កំពុងដំណើរការ...")
    app.run_polling()

if __name__ == "__main__":
    main()
