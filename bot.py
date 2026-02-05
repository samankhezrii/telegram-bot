from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8590616405:AAHldu7tyTWJxGKbMkJdUAV0dnN2XjtE8Xc"

keyboard = [
    ["📋 اطلاعات من", "🕒 ساعت"],
    ["❓ راهنما"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"سلام {user} 👋\nبه ربات خوش اومدی 🤖",
        reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 اطلاعات من":
        user = update.effective_user
        await update.message.reply_text(
            f"👤 اسم: {user.first_name}\n🆔 آیدی عددی: {user.id}"
        )

    elif text == "🕒 ساعت":
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        await update.message.reply_text(f"⏰ ساعت الان: {now}")

    elif text == "❓ راهنما":
        await update.message.reply_text("از دکمه‌ها استفاده کن 👇")

    else:
        await update.message.reply_text("دستور رو از روی دکمه‌ها انتخاب کن 👇")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

print("Bot is running...")
app.run_polling()
