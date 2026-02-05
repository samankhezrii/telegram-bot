import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# ✅ توکن فقط از Environment Variable
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Environment variable BOT_TOKEN not set!")

# دکمه‌های منو
keyboard = [
    ["📋 اطلاعات من", "🕒 ساعت"],
    ["❓ راهنما"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# URLها یا لینک‌هایی که میخوای استفاده کنی
# مثلاً برای تصاویر، فایل‌ها یا وبسایت‌ها
INFO_URL = "https://example.com/info"      # جایگزین URL واقعی خودت کن
HELP_URL = "https://example.com/help"      # جایگزین URL واقعی خودت کن

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"سلام {user} 👋\nبه ربات خوش اومدی 🤖\nبرای اطلاعات بیشتر: {INFO_URL}",
        reply_markup=reply_markup
    )

# مدیریت پیام‌های دکمه‌ای
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 اطلاعات من":
        user = update.effective_user
        await update.message.reply_text(
            f"👤 اسم: {user.first_name}\n🆔 آیدی عددی: {user.id}\nبرای جزئیات بیشتر: {INFO_URL}"
        )

    elif text == "🕒 ساعت":
        now = datetime.now().strftime("%H:%M:%S")
        await update.message.reply_text(f"⏰ ساعت الان: {now}")

    elif text == "❓ راهنما":
        await update.message.reply_text(f"از دکمه‌ها استفاده کن 👇\nراهنما: {HELP_URL}")

    else:
        await update.message.reply_text("دستور رو از روی دکمه‌ها انتخاب کن 👇")

# ساخت اپلیکیشن
app = ApplicationBuilder().token(TOKEN).build()

# اضافه کردن handler ها
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

# اجرای ربات
print("Bot is running...")
app.run_polling()
