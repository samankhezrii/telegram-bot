import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# 🔹 Firebase
import firebase_admin
from firebase_admin import credentials, db

# ✅ توکن از Environment Variable
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Environment variable BOT_TOKEN not set!")

# 🔹 Firebase initialization
# کلید Firebase که از کنسول دانلود کردی
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mirawater-d7e49-default-rtdb.firebaseio.com/'  # آدرس پروژه Firebase
})

# 🔹 دکمه‌های منو
keyboard = [
    ["📋 اطلاعات من", "🕒 ساعت"],
    ["❓ راهنما"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# URLها یا لینک‌های مفید
INFO_URL = "https://example.com/info"  # جایگزین لینک واقعی خودت
HELP_URL = "https://example.com/help"  # جایگزین لینک واقعی خودت

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"سلام {user} 👋\nبه ربات خوش اومدی 🤖\nبرای اطلاعات بیشتر: {INFO_URL}",
        reply_markup=reply_markup
    )

# مدیریت پیام‌ها و ارسال عکس از Firebase/Google Drive
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()  # اسم وارد شده توسط کاربر
    ref = db.reference("/")  # مسیر اصلی در Firebase

    data = ref.child(text).get()  # بررسی اینکه Key وجود دارد یا خیر

    if data:
        # ارسال عکس از URL Google Drive
        await update.message.reply_photo(data)
    else:
        # بررسی دستورات منو
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
            await update.message.reply_text("عکسی برای این اسم پیدا نشد 😅")

# ساخت اپلیکیشن و Handlerها
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
