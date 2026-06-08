import os
import uuid
import logging
from dotenv import load_dotenv
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ======================== ENVIRONMENT VARIABLES ========================
load_dotenv()  # .env file से values लोड करें (local run के लिए)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))          # Integer में बदलना ज़रूरी है
BOT_USERNAME = os.getenv("BOT_USERNAME")

CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY")
CASHFREE_ENV = os.getenv("CASHFREE_ENV", "TEST")  # TEST or PROD

START_IMAGE = os.getenv("START_IMAGE", "https://i.postimg.cc/MKWZn3Lv/IMG-20260521-163611-172.jpg")
PREMIUM_IMAGE = os.getenv("PREMIUM_IMAGE", "https://i.postimg.cc/x89kTfHG/IMG-20260521-164434-789.jpg")
DEMO_CHANNEL = os.getenv("DEMO_CHANNEL", "https://t.me/demochannlink")
INFO_CHANNEL = os.getenv("INFO_CHANNEL", "https://t.me/howtogetpre")

# Cashfree URL based on environment
if CASHFREE_ENV == "TEST":
    CASHFREE_URL = "https://sandbox.cashfree.com/pg/orders"
else:
    CASHFREE_URL = "https://api.cashfree.com/pg/orders"

# ======================== GLOBALS ========================
users = set()
stats = {99: 0, 149: 0, 249: 0, 499: 0}
active_orders = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================== HELPERS ========================
def create_cashfree_order(order_id: str, amount: float, user_id: int, username: str) -> str | None:
    headers = {
        "x-api-version": "2023-08-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    safe_name = "".join(c for c in username if c.isalnum()) or "User"
    customer_email = f"{safe_name}_{user_id}@tgbot.com"
    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user_id),
            "customer_phone": "9999999999",
            "customer_email": customer_email
        },
        "order_meta": {
            "return_url": f"https://t.me/{BOT_USERNAME}?start=verify_{order_id}"
        }
    }
    try:
        resp = requests.post(CASHFREE_URL, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("payment_link")
        else:
            logger.error(f"Cashfree error {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"Connection error: {e}")
    return None

def check_payment_status(order_id: str) -> str:
    headers = {
        "x-api-version": "2023-08-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }
    try:
        resp = requests.get(f"{CASHFREE_URL}/{order_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("order_status", "PENDING")
    except Exception as e:
        logger.error(f"Status check error: {e}")
    return "ERROR"

# ======================== KEYBOARDS ========================
def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 💎", callback_data="premium")],
        [InlineKeyboardButton("🎬 𝐃𝐄𝐌𝐎 𝐕𝐈𝐃𝐄𝐎𝐒", url=DEMO_CHANNEL)],
        [InlineKeyboardButton("📖 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌", url=INFO_CHANNEL)]
    ])

def plans_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 MS VIDEOS - ₹99", callback_data="plan_99")],
        [InlineKeyboardButton("🔥 EP VIDEOS - ₹149", callback_data="plan_149")],
        [InlineKeyboardButton("📦 ALL IN ONE ( 50+ Group ) - ₹249", callback_data="plan_249")],
        [InlineKeyboardButton("👑 VIP ALL ( 100+ Group ) - ₹499", callback_data="plan_499")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="home")]
    ])

# ======================== HANDLERS ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    if context.args and context.args[0].startswith("verify_"):
        order_id = context.args[0].replace("verify_", "")
        status = check_payment_status(order_id)
        if status == "PAID":
            await update.message.reply_text(
                "✅ **PAYMENT SUCCESSFUL!**\n\nआपका प्रीमियम एक्टिवेट हो गया है। अब आप VIP ग्रुप जॉइन कर सकते हैं।",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Payment pending or failed. कृपया पेमेंट पूरा करें या सपोर्ट से संपर्क करें।")
        return

    caption = "🔥 *PREMIUM VIDEO COLLECTION* 🔥\n\n🎬 5000+ MMS VIDEOS\n💋 2000+ COUPLE COLLECTION\n🔥 15000+ PREMIUM VIDEOS\n📦 100+ VIP COLLECTIONS\n⚡ INSTANT ACCESS"
    await update.message.reply_photo(photo=START_IMAGE, caption=caption, parse_mode="Markdown", reply_markup=home_keyboard())

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return
    total_users = len(users)
    text = f"📊 *BOT STATS*\n\n👥 Total Users: {total_users}\n💎 ₹99 : {stats[99]}\n🔥 ₹149: {stats[149]}\n📦 ₹249: {stats[249]}\n👑 ₹499: {stats[499]}"
    await update.message.reply_text(text, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.message.edit_media(media=InputMediaPhoto(media=START_IMAGE, caption="🔥 *PREMIUM VIDEO COLLECTION* 🔥", parse_mode="Markdown"), reply_markup=home_keyboard())
    elif data == "premium":
        await query.message.edit_media(media=InputMediaPhoto(media=PREMIUM_IMAGE, caption="💎 *SELECT YOUR PLAN* 💎", parse_mode="Markdown"), reply_markup=plans_keyboard())
    elif data.startswith("plan_"):
        amount = int(data.split("_")[1])
        stats[amount] += 1
        user = query.from_user
        order_id = f"ORD_{uuid.uuid4().hex[:10].upper()}"
        payment_link = create_cashfree_order(order_id, amount, user.id, user.first_name or "User")
        if not payment_link:
            await query.message.reply_text("❌ Payment link generate failed. Try again later.")
            return
        active_orders[order_id] = {"user_id": user.id, "amount": amount, "link": payment_link}
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 PAY NOW", url=payment_link)],
            [InlineKeyboardButton("🔄 CHECK STATUS", callback_data=f"check_{order_id}")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="premium")]
        ])
        await query.message.edit_media(media=InputMediaPhoto(media=PREMIUM_IMAGE, caption=f"💸 *PLAN: ₹{amount}*\n\n🆔 Order ID: `{order_id}`\n\n👇 Click below to pay", parse_mode="Markdown"), reply_markup=keyboard)
    elif data.startswith("check_"):
        order_id = data.replace("check_", "")
        status = check_payment_status(order_id)
        if status == "PAID":
            await query.message.edit_caption(caption="✅ **PAYMENT VERIFIED!** आपको जल्द ही एक्सेस मिल जाएगा।", parse_mode="Markdown", reply_markup=None)
        else:
            await query.answer("❌ Payment still pending. Please complete the payment.", show_alert=True)

# ======================== MAIN ========================
def main():
    if not all([TOKEN, ADMIN_ID, BOT_USERNAME, CASHFREE_APP_ID, CASHFREE_SECRET_KEY]):
        logger.error("Missing environment variables! Check your .env or Railway variables.")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
