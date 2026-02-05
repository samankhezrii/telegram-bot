import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
from firebase_admin import credentials, initialize_app, db

# ------------------------------
# 🔹 توکن ربات از Environment Variable
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Environment variable BOT_TOKEN not set!")

# ------------------------------
# 🔹 Firebase از Environment Variable
firebase_key_json = os.getenv("FIREBASE_KEY")
if not firebase_key_json:
    raise ValueError("Environment variable FIREBASE_KEY not set!")

cred = credentials.Certificate(json.loads(firebase_key_json))
initialize_app(cred, {
    'databaseURL': 'https://mirawater-d7e49-default-rtdb.firebaseio.com/'  # جایگزین با پروژه Firebase خودت
})

# ------------------------------
# 🔹 دکمه‌ها و منو
keyboard = [
    ["📋 اطلاعات من", "🕒 ساعت"],
    ["❓ راهنما"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

INFO_URL = "https://example.com/info"      # جایگزین لینک واقعی خودت
HELP_URL = "https://example.com/help"      # جایگزین لینک واقعی خودت

# ------------------------------
# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"سلام {user} 👋\nبه ربات خوش اومدی 🤖\nبرای اطلاعات بیشتر: {INFO_URL}",
        reply_markup=reply_markup
    )

# ------------------------------
# مدیریت پیام‌ها و ارسال عکس از Firebase/Google Drive
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()  # اسم وارد شده توسط کاربر
    ref = db.reference("images")        # مسیر Key ها در Firebase
    data = ref.child(text).get()        # بررسی Key در Firebase

    if data and "url" in data:
        # ارسال عکس از لینک Google Drive
        await update.message.reply_photo(data["url"])
    else:
        # بررسی سایر دستورات منو
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

# ------------------------------
# ساخت اپلیکیشن و Handlerها
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
