import os
import uuid
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== 🔴 YAHAN APNI VALUES DAALO 🔴 ====================
TOKEN = "YOUR_BOT_TOKEN_HERE"              # BotFather se lo
ADMIN_ID = 6648941928                       # Apni Telegram ID (integer)
BOT_USERNAME = "your_bot_username_here"     # bina @ ke, jaise "myvideobot"
CASHFREE_APP_ID = "77152048f182445d66a3602069025177"   # Jo aapke paas hai
CASHFREE_SECRET_KEY = "cfsk_ma_prod_1d43da257fdf34ee6a41ee8d5741444e_bd4de1ad"
CASHFREE_ENV = "TEST"                        # "TEST" ya "PROD"
# =====================================================================

if CASHFREE_ENV == "TEST":
    CASHFREE_URL = "https://sandbox.cashfree.com/pg/orders"
else:
    CASHFREE_URL = "https://api.cashfree.com/pg/orders"

# Images (badal sakte ho)
START_IMAGE = "https://i.postimg.cc/MKWZn3Lv/IMG-20260521-163611-172.jpg"
PREMIUM_IMAGE = "https://i.postimg.cc/x89kTfHG/IMG-20260521-164434-789.jpg"
DEMO_CHANNEL = "https://t.me/demochannlink"
INFO_CHANNEL = "https://t.me/howtogetpre"

users = set()
stats = {99: 0, 149: 0, 249: 0, 499: 0}
active_orders = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_cashfree_order(order_id, amount, user_id, username):
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

def check_payment_status(order_id):
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
        [InlineKeyboardButton("📦 ALL IN ONE - ₹249", callback_data="plan_249")],
        [InlineKeyboardButton("👑 VIP ALL - ₹499", callback_data="plan_499")],
        [InlineKeyboardButton("⬅️ BACK", callback_data="home")]
    ])

async def start(update, context):
    user = update.effective_user
    users.add(user.id)
    if context.args and context.args[0].startswith("verify_"):
        order_id = context.args[0].replace("verify_", "")
        status = check_payment_status(order_id)
        if status == "PAID":
            await update.message.reply_text("✅ **PAYMENT SUCCESSFUL!**\n\nआपका प्रीमियम एक्टिवेट हो गया है।", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Payment pending or failed. Contact support.")
        return
    caption = "🔥 *PREMIUM VIDEO COLLECTION* 🔥\n\n🎬 5000+ MMS VIDEOS\n💋 2000+ COUPLE COLLECTION\n🔥 15000+ PREMIUM VIDEOS\n📦 100+ VIP COLLECTIONS\n⚡ INSTANT ACCESS"
    await update.message.reply_photo(photo=START_IMAGE, caption=caption, parse_mode="Markdown", reply_markup=home_keyboard())

async def stats_command(update, context):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return
    total_users = len(users)
    text = f"📊 *BOT STATS*\n\n👥 Total Users: {total_users}\n💎 ₹99 : {stats[99]}\n🔥 ₹149: {stats[149]}\n📦 ₹249: {stats[249]}\n👑 ₹499: {stats[499]}"
    await update.message.reply_text(text, parse_mode="Markdown")

async def button_callback(update, context):
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
        active_orders[order_id] = {"user_id": user.id, "amount": amount}
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

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
